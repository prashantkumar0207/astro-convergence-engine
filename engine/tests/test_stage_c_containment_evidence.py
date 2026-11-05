"""Per-method evidence for the five methods containment places NOT_IN_USE (ADR-0109 s2).

Absence of a name proves little on its own, so each method gets three things: its U1 and U2
exclusion from the analyser, the receiver or value route behind every unresolved site, and
controls that plant a real use in a copy of the real tree and require the status to change.
"""

from __future__ import annotations

import ast
import json
import shutil
import sys
from functools import lru_cache
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import check_reachability as c4  # noqa: E402
import coverage_static  # noqa: E402

CACHE, REGISTRY = "engine.knowledge.cache", "engine.knowledge.registry"
RESOLVER, VALIDATOR = "engine.knowledge.resolver", "engine.knowledge.validator"
FIVE = (
    (CACHE, "KnowledgeCache", "get"),
    (CACHE, "KnowledgeCache", "clear"),
    (REGISTRY, "KnowledgeRegistry", "clear"),
    (RESOLVER, "KnowledgeResolver", "resolve"),
    (VALIDATOR, "SchemaValidator", "validate"),
)
IDS = [f"{cls}.{method}" for _module, cls, method in FIVE]
#: The only outside-surface modules that import each module. This is what can name the class at all.
IMPORTERS = {CACHE: set(), REGISTRY: {"engine/knowledge/resolver.py"}, RESOLVER: set(), VALIDATOR: set()}


@lru_cache(maxsize=1)
def _outside() -> dict:
    return {relative: ast.parse((ROOT / relative).read_text(encoding="utf-8-sig"))
            for relative in coverage_static.tracked_python_files(ROOT)
            if not coverage_static.in_verification_surface(relative)}


def _sites(name: str) -> set[tuple[str, str]]:
    """(file, receiver) for every outside-surface read of `.name`, call or not."""

    return {(relative, ast.unparse(node.value)) for relative, tree in _outside().items() for node in ast.walk(tree)
            if isinstance(node, ast.Attribute) and node.attr == name and isinstance(node.ctx, ast.Load)}


# ------------------------------------------------------------------ U1 and U2

@pytest.mark.parametrize("module,cls,method", FIVE, ids=IDS)
def test_no_outside_call_path_and_no_export(module, cls, method):
    dotted = f"{module}.{cls}.{method}"
    graph = coverage_static.build_graph(ROOT)
    outside_callers = [owner for owner, targets in graph.edges.items() if dotted in targets
                       and not coverage_static.in_verification_surface(graph.owners.get(owner, "engine/tests/x"))]
    assert outside_callers == [], "U1"
    assert not graph.exports.get(dotted) and not graph.exports.get(f"{module}.{cls}"), "U2"
    row = json.loads((ROOT / "reports" / "c4_reachability.json").read_text(encoding="utf-8"))["rows"][dotted]
    assert row["status"] == "NOT_IN_USE" and "callers" not in row and "exported_by" not in row
    assert graph.contained(f"{module}.{cls}")


def test_the_knowledge_package_exports_nothing():
    assert (ROOT / "engine" / "knowledge" / "__init__.py").read_text(encoding="utf-8").strip() == ""


# ------------------------------------------------------------------ value routes

@pytest.mark.parametrize("module", sorted(IMPORTERS))
def test_only_the_named_modules_import_the_class_at_all(module):
    package, leaf = module.rsplit(".", 1)
    importers = set()
    for relative, tree in _outside().items():
        this = coverage_static.module_name(relative)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import) and any(alias.name.startswith(module) for alias in node.names):
                importers.add(relative)
            elif isinstance(node, ast.ImportFrom):
                base = coverage_static._import_base(node, this, relative.endswith("__init__.py"))
                if base == module or (base == package and any(alias.name in (leaf, "*") for alias in node.names)):
                    importers.add(relative)
    assert importers == IMPORTERS[module]


def test_the_one_outside_use_of_a_class_name_is_an_attribute_read():
    uses = []
    for relative, tree in _outside().items():
        parents = {child: node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id in {cls for _m, cls, _f in FIVE}:
                parent = parents[node]
                uses.append((relative, node.id, parent.attr if isinstance(parent, ast.Attribute) else type(parent).__name__))
    assert uses == [("engine/knowledge/resolver.py", "KnowledgeRegistry", "get")]


def test_no_dynamic_route_names_these_classes_or_modules():
    """Text that could feed import_module or getattr. Declarations are data that C3 reads statically."""

    names = ("KnowledgeCache", "KnowledgeRegistry", "KnowledgeResolver", "SchemaValidator",
             "knowledge.cache", "knowledge.registry", "knowledge.resolver", "knowledge.validator")
    holders = {relative for relative, tree in _outside().items() for node in ast.walk(tree)
               if isinstance(node, ast.Constant) and isinstance(node.value, str)
               and any(name in node.value for name in names)}
    assert holders <= {"scripts/capability_declarations.py"}


def test_the_engine_getattr_dispatch_targets_only_the_repository():
    """The one dynamic dispatch in engine production code cannot reach the five."""

    sites = [ast.unparse(node.args[0]) for relative, tree in _outside().items() if relative.startswith("engine/")
             for node in ast.walk(tree)
             if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "getattr"]
    assert sites == ["KnowledgeRepository"]


# ------------------------------------------------------------------ receivers, method by method

def test_every_clear_site_is_on_a_dict():
    assert _sites("clear") == {("engine/knowledge/cache.py", "self._cache"), ("engine/knowledge/registry.py", "cls._cache")}
    annotations = []
    for relative in ("engine/knowledge/cache.py", "engine/knowledge/registry.py"):
        annotations += [ast.unparse(node.annotation) for node in ast.walk(_outside()[relative])
                        if isinstance(node, ast.AnnAssign) and ast.unparse(node.target) in ("self._cache", "_cache")]
    assert annotations == ["dict[str, Any]", "dict[str, Any]"]


def test_the_only_validate_site_is_on_a_jsonschema_validator():
    assert _sites("validate") == {("engine/knowledge/validator.py", "validator")}
    tree = _outside()["engine/knowledge/validator.py"]
    assigned = [ast.unparse(node.value) for node in ast.walk(tree) if isinstance(node, ast.Assign)
                and ast.unparse(node.targets[0]) == "validator"]
    assert assigned == ["Draft202012Validator(schema)"]
    assert any(isinstance(node, ast.ImportFrom) and node.module == "jsonschema"
               and "Draft202012Validator" in [alias.name for alias in node.names] for node in ast.walk(tree))


def test_every_resolve_site_is_on_a_path_or_the_scanner():
    unusual = {site for site in _sites("resolve") if not site[1].startswith(("Path(", "pathlib.Path("))}
    assert unusual == {("scripts/coverage_static.py", "self"),  # _Scanner, which defines its own resolve.
                       ("tools/mutation_harness/fixtures/run_demo.py", "out"),
                       ("tools/mutation_harness/harness.py", "path"),
                       ("tools/mutation_harness/harness.py", "unresolved")}


def test_every_get_site_in_engine_production_code_is_named():
    """Dicts, FastAPI's app, and a resolved edge. Sites outside engine/ sit in modules that do not import it."""

    sites = {site for site in _sites("get") if site[0].startswith("engine/")}
    assert sites == {("engine/astrology/dignity.py", "record"),
                     ("engine/astrology/sign_conventions.py", "SIGN_FIELD_CONVENTIONS"),
                     ("engine/dasha/vimshottari.py", "_SCHOOL_BY_PROFILE"),
                     ("engine/knowledge/resolver.py", "KnowledgeRegistry"),
                     ("engine/kp/significators.py", "SPECIAL_ASPECTS"),
                     ("engine/main.py", "app")}


# ------------------------------------------------------------------ controls on a copy of the real tree

PLANTS = {
    "instantiated": ("scripts/planted.py", "from {module} import {cls}\nMADE = {cls}()\n"),
    "exported": ("engine/api/planted.py", "from {module} import {cls}\n"),
    "direct": ("scripts/planted.py", "from {module} import {cls}\ndef main(x: {cls}):\n    return x.{method}()\n"),
    "getattr": ("scripts/planted.py", "from {module} import {cls}\ndef main(name):\n    return getattr({cls}, name)\n"),
}


@pytest.fixture(scope="module")
def real_copy(tmp_path_factory):
    root = tmp_path_factory.mktemp("real_tree")
    files = coverage_static.tracked_python_files(ROOT)
    for relative in files:
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)
    return root, files, c4.gated_members(ROOT / "certification")[0]


def _status(real_copy, dotted, plant=None):
    root, files, members = real_copy
    if plant is None:
        return c4.analyse(coverage_static.build_graph(root, files), members)["rows"][dotted]
    relative, text = plant
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    try:
        return c4.analyse(coverage_static.build_graph(root, [*files, relative]), members)["rows"][dotted]
    finally:
        path.unlink()


@pytest.mark.parametrize("module,cls,method", FIVE, ids=IDS)
def test_the_unplanted_copy_agrees_with_the_report(real_copy, module, cls, method):
    assert _status(real_copy, f"{module}.{cls}.{method}")["status"] == "NOT_IN_USE"


@pytest.mark.parametrize("kind", ["instantiated", "exported"])
@pytest.mark.parametrize("module,cls,method", FIVE, ids=IDS)
def test_a_value_getting_out_restores_unknown(real_copy, module, cls, method, kind):
    relative, text = PLANTS[kind]
    row = _status(real_copy, f"{module}.{cls}.{method}", (relative, text.format(module=module, cls=cls, method=method)))
    assert row["status"] == "UNKNOWN"
    assert row["ambiguous_owner_count"] >= 1


@pytest.mark.parametrize("kind", ["direct", "getattr"])
@pytest.mark.parametrize("module,cls,method", FIVE, ids=IDS)
def test_a_real_use_is_counted_as_in_use(real_copy, module, cls, method, kind):
    relative, text = PLANTS[kind]
    row = _status(real_copy, f"{module}.{cls}.{method}", (relative, text.format(module=module, cls=cls, method=method)))
    assert row["status"] in ("IN_USE_COVERED", "IN_USE_UNCOVERED")
    assert "scripts.planted.main" in row["callers"]


# ------------------------------------------------------------------ runtime corroboration

def test_the_served_module_imports_nothing_from_the_knowledge_package():
    imported = {node.module for node in ast.walk(_outside()["engine/main.py"]) if isinstance(node, ast.ImportFrom)}
    assert {name for name in imported if name and name.startswith("engine")} == {
        "engine.calculations.calculations", "engine.models.birth_data", "engine.version"}


def test_the_served_and_certified_paths_never_dispatch_to_the_five(monkeypatch):
    """Executed paths only, so this corroborates the static evidence and cannot prove absence."""

    import importlib

    from engine.astrology.chart_builder import build_chart
    from engine.astrology.dignity import is_exalted, is_own_sign
    from engine.calculations.calculations import calculate
    from engine.dasha.vimshottari import vimshottari_kp, vimshottari_parashari
    from engine.kp.chart import kp_chart
    from engine.models.birth_data import BirthData

    def forbidden(*_args, **_kwargs):
        raise AssertionError("a contained method was dispatched to")

    classes = []
    for module, cls, method in FIVE:
        klass = getattr(importlib.import_module(module), cls)
        monkeypatch.setattr(klass, method, forbidden)
        classes.append((klass, method))
    for klass, method in classes:  # The tripwire must fire when it is reached.
        with pytest.raises(AssertionError, match="contained method"):
            getattr(klass, method)()

    # engine/main.py imports fastapi, which the gate environment does not install, so its routes are not
    # executed here. /engine/test is calculate() on this input, and that is what runs.
    served = BirthData(1989, 7, 12, 16, 44, 0.0, 25.5941, 85.1376, "Asia/Kolkata")
    assert calculate(served).snapshot
    birth = BirthData(1988, 11, 23, 18, 45, 30.0, 51.5, -0.1, "UTC")
    snapshot = calculate(birth).snapshot
    assert build_chart(snapshot) and kp_chart(birth)
    assert vimshottari_parashari(birth, depth=1).periods and vimshottari_kp(birth, depth=1).periods
    assert is_exalted("Sun", 1) in (True, False) and is_own_sign("Sun", 5) in (True, False)
