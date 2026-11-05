"""Static call-graph analysis shared by the C3 and C4 gates (ADR-0099 s7, ADR-0107).

This module imports nothing from engine/. It parses tracked Python source with
`ast`, so its evidence is obtained by a different method from the certifiers'
own declarations, which is the point of using it.

What an edge means. A function has an edge to a target when its body names the
target through a resolvable import or a same-module definition. Naming is not
calling: a function passed as a value still produces an edge, and that is
deliberate, because it can then be called.

Receivers it resolves, each from evidence in the source: `self.x` and `cls.x` inside
a class, and a local or parameter whose engine class is established by an annotation,
by a constructor call, or by the return annotation of the call that produced it. A name
given two types, or rebound by anything else, stays unresolved.

`getattr(C, name)` on an engine class is an edge to each of C's public methods. That
over-approximates deliberately, because the name is chosen at runtime.

Containment (`Graph.contained`). An unresolved `x.m` cannot land on C.m if no value of C
can exist outside the verification surface. C is contained only when outside the surface
it is never instantiated, subclassed, assigned, passed or exported, it has no base, metaclass
or non-dataclass decorator, and no star-import can reach it: its name is only ever read as
`C.attr` or `getattr(C, ...)`. Any use not recognised here counts against containment, so
the rule fails toward UNKNOWN.

What it cannot see, and says so. A method call on a value of unknown type
(`obj.get(...)`) names no module, so it cannot be resolved. Such a call is
recorded as AMBIGUOUS against every engine method of that name, never as an
edge. Other dynamic dispatch (`getattr` on a non-class, `importlib`) is recorded per
module and disclosed. Neither is ever treated as proof of absence.
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
    #: dotted engine class -> what opens its hierarchy (bases, metaclass, non-dataclass decorators).
    classes: dict[str, list[str]] = field(default_factory=dict)
    #: dotted function or method -> the engine class its return annotation names.
    returns: dict[str, str] = field(default_factory=dict)
    #: classes a value of which can reach code outside the verification surface.
    escaping: set[str] = field(default_factory=set)

    def has_subclass(self, class_name: str) -> bool:
        leaf = class_name.rsplit(".", 1)[-1]
        return any(base.rsplit(".", 1)[-1] == leaf for opened in self.classes.values() for base in opened)

    def contained(self, class_name: str) -> bool:
        """True when no value of this class can exist outside the verification surface."""

        return (class_name in self.classes and not self.classes[class_name]
                and class_name not in self.escaping and class_name not in self.exports)

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


def _import_base(node: ast.ImportFrom, module: str, is_package: bool) -> str:
    base = node.module or ""
    if node.level:
        parts = module.split(".")
        keep = len(parts) - node.level + (1 if is_package else 0)
        base = ".".join(parts[:keep] + ([node.module] if node.module else []))
    return base


def _imports(tree: ast.Module, module: str, is_package: bool) -> dict[str, str]:
    names: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            base = _import_base(node, module, is_package)
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

    def annotation_class(self, annotation) -> str | None:
        """The engine class an annotation plainly names, if any."""

        if isinstance(annotation, ast.Constant) and isinstance(annotation.value, str):
            try:
                annotation = ast.parse(annotation.value, mode="eval").body
            except SyntaxError:
                return None
        target = self.resolve(annotation) if isinstance(annotation, (ast.Name, ast.Attribute)) else None
        return target if target in self.graph.classes else None

    def value_type(self, value, types: dict, enclosing_class: str | None) -> str | None:
        """The engine class an expression's value is established to be."""

        if isinstance(value, ast.Name):
            return types.get(value.id)
        if not isinstance(value, ast.Call):
            return None
        function = value.func
        if isinstance(function, ast.Name) and function.id == "cls":
            return enclosing_class
        if (isinstance(function, ast.Attribute) and isinstance(function.value, ast.Name)
                and function.value.id in ("cls", "self") and enclosing_class):
            return self.graph.returns.get(f"{enclosing_class}.{function.attr}")
        target = self.resolve(function) if isinstance(function, (ast.Name, ast.Attribute)) else None
        return target if target in self.graph.classes else self.graph.returns.get(target)

    def local_types(self, function, enclosing_class: str | None) -> dict[str, str]:
        """Names in `function` whose engine class is established, flow-insensitively."""

        types: dict[str, str] = {}
        conflicted: set[str] = set()
        arguments = function.args
        for argument in (*arguments.posonlyargs, *arguments.args, *arguments.kwonlyargs):
            established = self.annotation_class(argument.annotation) if argument.annotation else None
            if established:
                types[argument.arg] = established
        assignments = []
        simple_targets = set()
        for node in ast.walk(function):
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                assignments.append((node.targets[0].id, node.value, None))
                simple_targets.add(id(node.targets[0]))
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                assignments.append((node.target.id, node.value, node.annotation))
                simple_targets.add(id(node.target))
        for node in ast.walk(function):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store) and id(node) not in simple_targets:
                conflicted.add(node.id)
            elif isinstance(node, ast.arg) and node.arg not in types:
                conflicted.add(node.arg)  # An inner function's or lambda's parameter shadows the name.
        for _round in range(2):  # A second round lets `b = a.method()` see a type set later in the walk.
            for name, value, annotation in assignments:
                established = self.annotation_class(annotation) if annotation is not None else None
                established = established or self.value_type(value, types, enclosing_class)
                if established is None or types.get(name, established) != established:
                    conflicted.add(name)
                else:
                    types[name] = established
        for nested in ast.walk(function):
            if nested is not function and isinstance(nested, (*_FUNCTIONS, ast.Lambda)):
                inner = nested.args
                conflicted.update(item.arg for item in (*inner.posonlyargs, *inner.args, *inner.kwonlyargs))
        return {name: kind for name, kind in types.items() if name not in conflicted}

    def record_escapes(self) -> None:
        """Mark every engine class this file lets a value of out. See the module docstring."""

        hints = set()
        parents = {}
        for node in ast.walk(self.tree):
            for child in ast.iter_child_nodes(node):
                parents[child] = node
            if isinstance(node, _FUNCTIONS) and node.returns is not None:
                hints.update(ast.walk(node.returns))
            elif isinstance(node, (ast.arg, ast.AnnAssign)) and node.annotation is not None:
                hints.update(ast.walk(node.annotation))
            elif isinstance(node, ast.ImportFrom) and any(alias.name == "*" for alias in node.names):
                base = _import_base(node, self.module, self.relative.endswith("__init__.py"))
                self.graph.escaping.update(name for name in self.graph.classes if name.rsplit(".", 1)[0] == base)
        for node in ast.walk(self.tree):
            if node in hints or not isinstance(node, (ast.Name, ast.Attribute)):
                continue
            parent = parents.get(node)
            if isinstance(node, ast.Name) and node.id == "cls":
                if not (isinstance(parent, ast.Attribute) and parent.value is node):
                    owner = parent
                    while owner is not None and not isinstance(owner, ast.ClassDef):
                        owner = parents.get(owner)
                    if owner is not None:
                        self.graph.escaping.add(f"{self.module}.{owner.name}")
                continue
            target = self.resolve(node)
            if target not in self.graph.classes or not isinstance(node.ctx, ast.Load):
                continue
            if isinstance(parent, ast.Attribute) and parent.value is node and not parent.attr.startswith("__"):
                continue  # `C.attr`: the class value goes no further. `C.__new__` and the like can make one.
            if (isinstance(parent, ast.Call) and isinstance(parent.func, ast.Name) and parent.func.id == "getattr"
                    and parent.args and parent.args[0] is node):
                continue  # An edge to each public method, recorded in `visit`.
            self.graph.escaping.add(target)

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

    def visit(self, owner: str, nodes, enclosing_class: str | None = None, types: dict | None = None) -> None:
        types = types or {}
        self.graph.owners.setdefault(owner, self.relative)
        for root in nodes:
            for node in ast.walk(root):
                if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "getattr"
                        and node.args and isinstance(node.args[0], (ast.Name, ast.Attribute))):
                    subject = self.resolve(node.args[0])
                    if subject in self.graph.classes:
                        for dotted in self.graph.definitions:
                            if (dotted.startswith(f"{subject}.")
                                    and not dotted.rsplit(".", 1)[-1].startswith("_")):
                                self._record(owner, dotted)
                if isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Load):
                    receiver = node.value.id if isinstance(node.value, ast.Name) else None
                    established = self.value_type(node.value, types, enclosing_class)
                    if receiver in ("self", "cls") and enclosing_class is not None and receiver not in types:
                        established = enclosing_class
                    if established is not None:
                        dotted = f"{established}.{node.attr}"
                        if dotted in self.graph.definitions or not self.graph.classes.get(established):
                            self._record(owner, dotted)
                        # The name may be inherited, or the value may be a subclass that overrides it.
                        if self.graph.classes.get(established) or self.graph.has_subclass(established):
                            self.graph.ambiguous[owner].add(node.attr)
                        continue
                    target = self.resolve(node)
                    if target is not None:
                        self._record(owner, target)
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
                self.visit(f"{self.module}.{node.name}", [node], types=self.local_types(node, None))
            elif isinstance(node, ast.ClassDef):
                class_name = f"{self.module}.{node.name}"
                module_level.extend(item for item in node.body if not isinstance(item, _FUNCTIONS))
                for item in node.body:
                    if isinstance(item, _FUNCTIONS):
                        self.visit(f"{class_name}.{item.name}", [item], enclosing_class=class_name,
                                   types=self.local_types(item, class_name))
            else:
                module_level.append(node)
        self.visit(self.module, module_level)


def _open_hierarchy(node: ast.ClassDef) -> list[str]:
    """What can create a class's values implicitly, or supply methods it does not define.
    An Enum's members, for one, exist without any call. `object` and dataclass add neither."""

    opened = [ast.unparse(base) for base in node.bases if ast.unparse(base) != "object"]
    opened += [ast.unparse(keyword) for keyword in node.keywords]
    for decorator in node.decorator_list:
        call = decorator.func if isinstance(decorator, ast.Call) else decorator
        if ast.unparse(call).rsplit(".", 1)[-1] != "dataclass":
            opened.append(f"@{ast.unparse(decorator)}")
    return opened


def _record_returns(scanner: _Scanner) -> None:
    for node in scanner.tree.body:
        if isinstance(node, _FUNCTIONS):
            pairs = [(f"{scanner.module}.{node.name}", node)]
        elif isinstance(node, ast.ClassDef):
            pairs = [(f"{scanner.module}.{node.name}.{item.name}", item)
                     for item in node.body if isinstance(item, _FUNCTIONS)]
        else:
            continue
        for dotted, function in pairs:
            established = scanner.annotation_class(function.returns) if function.returns is not None else None
            if established:
                scanner.graph.returns[dotted] = established


def _record_definitions(graph: Graph, tree: ast.Module, relative: str) -> None:
    module = module_name(relative)
    for node in tree.body:
        if isinstance(node, _FUNCTIONS):
            graph.definitions[f"{module}.{node.name}"] = relative
        elif isinstance(node, ast.ClassDef):
            graph.classes[f"{module}.{node.name}"] = _open_hierarchy(node)
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
    scanners = {relative: _Scanner(graph, tree, relative) for relative, tree in trees.items()}
    for relative, scanner in scanners.items():
        if relative.startswith("engine/") and not relative.startswith("engine/tests/"):
            _record_returns(scanner)
    for relative, scanner in scanners.items():
        if not in_verification_surface(relative):
            scanner.record_escapes()
        scanner.scan()
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
