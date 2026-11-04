"""Static call-graph analysis shared by the C3 and C4 gates (ADR-0099 s7, ADR-0107).

This module imports nothing from engine/. It parses tracked Python source with
`ast`, so its evidence is obtained by a different method from the certifiers'
own declarations, which is the point of using it.

What an edge means. A function has an edge to a target when its body names the
target through a resolvable import or a same-module definition. Naming is not
calling: a function passed as a value still produces an edge, and that is
deliberate, because it can then be called.

What it cannot see, and says so. A method call on a value of unknown type
(`obj.get(...)`) names no module, so it cannot be resolved. Such a call is
recorded as AMBIGUOUS against every engine method of that name, never as an
edge. Dynamic dispatch (`getattr`, `importlib`) is recorded per module and
disclosed. Neither is ever treated as proof of absence.
"""

from __future__ import annotations

import ast
import fnmatch
import subprocess
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

#: Names whose use in a module makes its reachability dynamic rather than static.
DYNAMIC_MARKERS = frozenset({"getattr", "__import__", "import_module", "globals", "eval", "exec"})

_FUNCTIONS = (ast.FunctionDef, ast.AsyncFunctionDef)


def in_verification_surface(relative: str) -> bool:
    """ADR-0099 s3's counting rule, applied exactly as written."""

    base = relative.rsplit("/", 1)[-1]
    return (relative.startswith("engine/tests/")
            or fnmatch.fnmatch(relative, "scripts/certify_*.py")
            or fnmatch.fnmatch(base, "validate_*.py")
            or base in ("conftest.py", "brihat_fixtures.py"))


def module_name(relative: str) -> str:
    name = relative[:-3].replace("/", ".")
    return name[: -len(".__init__")] if name.endswith(".__init__") else name


def tracked_python_files(root: Path = ROOT) -> list[str]:
    result = subprocess.run(["git", "-C", str(root), "ls-files", "*.py"],
                            capture_output=True, text=True, check=True)
    return sorted(line for line in result.stdout.splitlines() if line)


@dataclass
class Graph:
    """Everything the gates need to know about the source tree."""

    #: dotted name -> relative path, for every function and method in engine/.
    definitions: dict[str, str] = field(default_factory=dict)
    #: dotted name -> relative path, for module-level names assigned in engine/.
    data: dict[str, str] = field(default_factory=dict)
    #: method name -> dotted names of every engine method carrying it.
    methods: dict[str, list[str]] = field(default_factory=lambda: defaultdict(list))
    #: owner (dotted function, or module for module-level code) -> resolved targets.
    edges: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))
    #: owner -> unresolved method names it uses.
    ambiguous: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))
    #: owner -> relative path of the file it is defined in.
    owners: dict[str, str] = field(default_factory=dict)
    #: module -> names marking dynamic dispatch used in that module.
    dynamic: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))
    #: names exported by a declared public surface (ADR-0099 U2) -> where.
    exports: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))
    #: files that could not be parsed. A gate must fail on these, never skip them.
    unparsed: dict[str, str] = field(default_factory=dict)

    def callers_of(self, name: str) -> set[str]:
        return {owner for owner, targets in self.edges.items() if name in targets}

    def canonical(self, target: str) -> str:
        """Follow `a.b.c` down to a defined function, if it names one."""

        if target in self.definitions:
            return target
        return target

    def closure(self, starts) -> set[str]:
        """Everything reachable from `starts`. Naming a function or its module
        also reaches that module's own import-time code."""

        seen: set[str] = set()
        frontier = list(starts)
        while frontier:
            current = frontier.pop()
            if current in seen:
                continue
            seen.add(current)
            frontier.extend(self.edges.get(current, ()))
            parts = current.split(".")
            for size in range(len(parts) - 1, 0, -1):
                module = ".".join(parts[:size])
                if module in self.edges and module not in seen:
                    frontier.append(module)
                    break
        return seen


def _imports(tree: ast.Module, module: str, is_package: bool) -> dict[str, str]:
    names: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            base = node.module or ""
            if node.level:
                parts = module.split(".")
                keep = len(parts) - node.level + (1 if is_package else 0)
                base = ".".join(parts[:keep] + ([node.module] if node.module else []))
            for alias in node.names:
                if alias.name != "*":
                    names[alias.asname or alias.name] = f"{base}.{alias.name}"
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.asname:
                    names[alias.asname] = alias.name
                else:
                    head = alias.name.split(".")[0]
                    names[head] = head
    return names


class _Scanner:
    def __init__(self, graph: Graph, tree: ast.Module, relative: str):
        self.graph = graph
        self.relative = relative
        self.module = module_name(relative)
        self.imports = _imports(tree, self.module, relative.endswith("__init__.py"))
        self.local = {node.name for node in tree.body if isinstance(node, (*_FUNCTIONS, ast.ClassDef))}
        self.tree = tree

    def resolve(self, expression) -> str | None:
        if isinstance(expression, ast.Name):
            if expression.id in self.imports:
                return self.imports[expression.id]
            if expression.id in self.local:
                return f"{self.module}.{expression.id}"
            return None
        if isinstance(expression, ast.Attribute):
            base = self.resolve(expression.value)
            return f"{base}.{expression.attr}" if base else None
        return None

    def visit(self, owner: str, nodes, enclosing_class: str | None = None) -> None:
        self.graph.owners.setdefault(owner, self.relative)
        for root in nodes:
            for node in ast.walk(root):
                if isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Load):
                    target = self.resolve(node)
                    if target is not None:
                        self._record(owner, target)
                    elif (isinstance(node.value, ast.Name) and node.value.id == "self"
                          and enclosing_class is not None):
                        self._record(owner, f"{enclosing_class}.{node.attr}")
                    else:
                        self.graph.ambiguous[owner].add(node.attr)
                    if node.attr in DYNAMIC_MARKERS:
                        self.graph.dynamic[self.module].add(node.attr)
                elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                    target = self.resolve(node)
                    if target is not None:
                        self._record(owner, target)
                    if node.id in DYNAMIC_MARKERS:
                        self.graph.dynamic[self.module].add(node.id)

    def _record(self, owner: str, target: str) -> None:
        if target.split(".")[0] != "engine":
            return
        self.graph.edges[owner].add(target)
        # Naming `a.b.f` where `a.b` is a module is a reference to that module too.
        parts = target.split(".")
        if len(parts) > 2:
            self.graph.edges[owner].add(".".join(parts[:-1]))

    def scan(self) -> None:
        module_level = []
        for node in self.tree.body:
            if isinstance(node, _FUNCTIONS):
                self.visit(f"{self.module}.{node.name}", [node])
            elif isinstance(node, ast.ClassDef):
                class_name = f"{self.module}.{node.name}"
                module_level.extend(item for item in node.body if not isinstance(item, _FUNCTIONS))
                for item in node.body:
                    if isinstance(item, _FUNCTIONS):
                        self.visit(f"{class_name}.{item.name}", [item], enclosing_class=class_name)
            else:
                module_level.append(node)
        self.visit(self.module, module_level)


def _record_definitions(graph: Graph, tree: ast.Module, relative: str) -> None:
    module = module_name(relative)
    for node in tree.body:
        if isinstance(node, _FUNCTIONS):
            graph.definitions[f"{module}.{node.name}"] = relative
        elif isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, _FUNCTIONS):
                    dotted = f"{module}.{node.name}.{item.name}"
                    graph.definitions[dotted] = relative
                    graph.methods[item.name].append(dotted)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name):
                    graph.data[f"{module}.{target.id}"] = relative
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__" and isinstance(
                        node.value, (ast.List, ast.Tuple)):
                    for item in node.value.elts:
                        if isinstance(item, ast.Constant) and isinstance(item.value, str):
                            graph.exports[f"{module}.{item.value}"].add(f"{relative}:__all__")


def build_graph(root: Path = ROOT, files: list[str] | None = None) -> Graph:
    graph = Graph()
    files = tracked_python_files(root) if files is None else files
    trees = {}
    for relative in files:
        try:
            # utf-8-sig: three tracked files begin with a byte-order mark.
            trees[relative] = ast.parse((root / relative).read_text(encoding="utf-8-sig"))
        except (OSError, SyntaxError, UnicodeDecodeError) as exc:
            graph.unparsed[relative] = str(exc)
    for relative, tree in trees.items():
        if relative.startswith("engine/") and not relative.startswith("engine/tests/"):
            _record_definitions(graph, tree, relative)
    for relative, tree in trees.items():
        _Scanner(graph, tree, relative).scan()
    # ADR-0099 U2: every name engine/api/ or engine/main.py defines or imports is exported.
    for relative, tree in trees.items():
        if relative == "engine/main.py" or relative.startswith("engine/api/"):
            for node in tree.body:
                if isinstance(node, _FUNCTIONS):
                    graph.exports[f"{module_name(relative)}.{node.name}"].add(relative)
                elif isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("engine"):
                    for alias in node.names:
                        graph.exports[f"{node.module}.{alias.name}"].add(relative)
    return graph
