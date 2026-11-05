"""Stage C: negative controls for the analyser's new evidence, and proofs of what it found.

Each analyser rule gets a control both ways: the use it recognises, and the nearest case it
must not recognise. Containment is the rule that removes a status, so its controls plant every
way a value can get out and require UNKNOWN. Runtime tests prove the resolved paths by a second
method, because a static reading is not its own proof.
"""

from __future__ import annotations

import copy
import json
import re
import shutil
import subprocess
import sys
from datetime import timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import certify_sign_convention  # noqa: E402
import certify_support_paths as support_paths  # noqa: E402
import check_reachability as c4  # noqa: E402
import check_scope_coverage as c3  # noqa: E402
import coverage_static  # noqa: E402

SUPPORT = "SUPPORT_PATHS_V1_certification.json"
BACKLOG = ROOT / "docs" / "CERTIFICATION_REMEDIATION_BACKLOG.json"


def _tree(tmp_path: Path, files: dict[str, str]):
    for relative, text in files.items():
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return coverage_static.build_graph(tmp_path, sorted(files))


def _rows(tmp_path, files, members=frozenset()):
    return c4.analyse(_tree(tmp_path, files), set(members))["rows"]


KLASS = "class Store:\n    def fetch_value(self):\n        return 5\n"
FACTORY = 'from engine.klass import Store\ndef make() -> Store:\n    return Store()\n'


# ------------------------------------------------------------------ receivers

@pytest.mark.parametrize("body", [
    "def main():\n    x = Store()\n    return x.fetch_value()\n",
    "def main(x: Store):\n    return x.fetch_value()\n",
    'def main(x: "Store"):\n    return x.fetch_value()\n',
    "def main():\n    return Store().fetch_value()\n",
    "def main():\n    x: Store = build()\n    return x.fetch_value()\n",
])
def test_an_established_receiver_is_an_edge(tmp_path, body):
    graph = _tree(tmp_path, {"engine/__init__.py": "", "engine/klass.py": KLASS,
                             "scripts/tool.py": f"from engine.klass import Store\n{body}"})
    assert "engine.klass.Store.fetch_value" in graph.edges["scripts.tool.main"]
    assert "fetch_value" not in graph.ambiguous["scripts.tool.main"]


def test_a_return_annotation_establishes_a_receiver(tmp_path):
    graph = _tree(tmp_path, {"engine/__init__.py": "", "engine/klass.py": KLASS, "engine/factory.py": FACTORY,
                             "scripts/tool.py": ("from engine.factory import make\n"
                                                 "def main():\n    x = make()\n    return x.fetch_value()\n")})
    assert "engine.klass.Store.fetch_value" in graph.edges["scripts.tool.main"]


@pytest.mark.parametrize("body", [
    "def main(other):\n    x = Store()\n    x = other\n    return x.fetch_value()\n",
    "def main(items):\n    x = Store()\n    for x in items:\n        pass\n    return x.fetch_value()\n",
    "def main(items):\n    x = Store()\n    return [x.fetch_value() for x in items]\n",
    "def main():\n    x = Store()\n    return (lambda x: x.fetch_value())(1)\n",
    "def main(x):\n    return x.fetch_value()\n",
    "def main(x: dict):\n    return x.fetch_value()\n",
    "def main():\n    x = untyped()\n    return x.fetch_value()\n",
])
def test_an_unestablished_receiver_stays_ambiguous(tmp_path, body):
    """A rebinding, a shadowing or a missing type must never become an edge to the wrong method."""

    graph = _tree(tmp_path, {"engine/__init__.py": "", "engine/klass.py": KLASS,
                             "scripts/tool.py": f"from engine.klass import Store\n{body}"})
    assert "engine.klass.Store.fetch_value" not in graph.edges["scripts.tool.main"]
    assert "fetch_value" in graph.ambiguous["scripts.tool.main"]


def test_cls_resolves_only_to_its_own_class(tmp_path):
    source = ("class A:\n    @classmethod\n    def helper(cls):\n        return 1\n"
              "    @classmethod\n    def caller(cls):\n        return cls.helper()\n"
              "class B:\n    @classmethod\n    def helper(cls):\n        return 2\n")
    graph = _tree(tmp_path, {"engine/__init__.py": "", "engine/two.py": source})
    assert "engine.two.A.helper" in graph.edges["engine.two.A.caller"]
    assert "engine.two.B.helper" not in graph.edges["engine.two.A.caller"]


def test_an_inherited_name_stays_ambiguous_rather_than_vanishing(tmp_path):
    source = ("from engine.base import Base\nclass A(Base):\n"
              "    def caller(self):\n        return self.inherited()\n")
    graph = _tree(tmp_path, {"engine/__init__.py": "", "engine/base.py": "class Base:\n    def inherited(self):\n        return 1\n",
                             "engine/child.py": source})
    assert "inherited" in graph.ambiguous["engine.child.A.caller"]


def test_a_typed_receiver_does_not_hide_a_subclass_override(tmp_path):
    """`x: Base` may hold a Child, so Child.m keeps its unresolved evidence."""

    source = ("class Base:\n    def fetch_value(self):\n        return 1\n"
              "class Child(Base):\n    def fetch_value(self):\n        return 2\n"
              "MADE = Child()\n")
    rows = _rows(tmp_path, {"engine/__init__.py": "", "engine/two.py": source,
                            "scripts/tool.py": ("from engine.two import Base\n"
                                                "def main(x: Base):\n    return x.fetch_value()\n")})
    assert rows["engine.two.Child.fetch_value"]["status"] == "UNKNOWN"
    assert rows["engine.two.Base.fetch_value"]["callers"] == ["scripts.tool.main"]


def test_getattr_on_an_engine_class_reaches_each_public_method(tmp_path):
    source = ("class Repo:\n    @classmethod\n    def alpha(cls):\n        return 1\n"
              "    @classmethod\n    def beta(cls):\n        return 2\n"
              "    @classmethod\n    def _private(cls):\n        return 3\n"
              "def get(name):\n    return getattr(Repo, name)()\n")
    graph = _tree(tmp_path, {"engine/__init__.py": "", "engine/repo.py": source})
    assert {"engine.repo.Repo.alpha", "engine.repo.Repo.beta"} <= graph.edges["engine.repo.get"]
    assert "engine.repo.Repo._private" not in graph.edges["engine.repo.get"]


def test_getattr_on_a_non_class_adds_no_edge_and_stays_disclosed(tmp_path):
    source = "class Repo:\n    def alpha(self):\n        return 1\ndef get(thing, name):\n    return getattr(thing, name)\n"
    graph = _tree(tmp_path, {"engine/__init__.py": "", "engine/repo.py": source})
    assert "engine.repo.Repo.alpha" not in graph.edges["engine.repo.get"]
    assert "getattr" in graph.dynamic["engine.repo"]


# ------------------------------------------------------------------ containment

def _with_ambiguous_use(tool: str = "") -> dict[str, str]:
    return {"engine/__init__.py": "", "engine/klass.py": KLASS,
            "scripts/caller.py": "def main(unknown):\n    return unknown.fetch_value()\n",
            "scripts/tool.py": tool or "X = 1\n"}


NAME = "engine.klass.Store.fetch_value"


def test_a_contained_class_is_not_reached_by_an_unresolved_call(tmp_path):
    assert _rows(tmp_path, _with_ambiguous_use())[NAME]["status"] == "NOT_IN_USE"


def test_a_test_only_instance_does_not_break_containment(tmp_path):
    """ADR-0099 s3: the verification surface does not make anything in use."""

    files = _with_ambiguous_use()
    files["engine/tests/test_klass.py"] = "from engine.klass import Store\nMADE = Store()\n"
    assert _rows(tmp_path, files)[NAME]["status"] == "NOT_IN_USE"


def test_an_annotation_alone_does_not_break_containment(tmp_path):
    tool = "from engine.klass import Store\nX = 1\ndef other(store: Store) -> Store:\n    return store\n"
    assert _rows(tmp_path, _with_ambiguous_use(tool))[NAME]["status"] == "NOT_IN_USE"


@pytest.mark.parametrize("label,tool", [
    ("instantiated", "from engine.klass import Store\nMADE = Store()\n"),
    ("instantiated through a module", "import engine.klass as k\nMADE = k.Store()\n"),
    ("aliased", "from engine.klass import Store\nALIAS = Store\n"),
    ("passed as a value", "from engine.klass import Store\ndef f(g):\n    return g(Store)\n"),
    ("subclassed", "from engine.klass import Store\nclass Child(Store):\n    pass\n"),
    ("tested with isinstance", "from engine.klass import Store\ndef f(x):\n    return isinstance(x, Store)\n"),
    ("star-imported", "from engine.klass import *\n"),
    ("made through a dunder", "from engine.klass import Store\nMAKE = Store.__new__\n"),
])
def test_every_way_a_value_can_get_out_breaks_containment(tmp_path, label, tool):
    assert _rows(tmp_path, _with_ambiguous_use(tool))[NAME]["status"] == "UNKNOWN", label


@pytest.mark.parametrize("label,klass", [
    ("a base", "from enum import Enum\nclass Store(Enum):\n    A = 1\n    def fetch_value(self):\n        return 5\n"),
    ("a metaclass", "class Meta(type):\n    pass\nclass Store(metaclass=Meta):\n    def fetch_value(self):\n        return 5\n"),
    ("a decorator", "def wrap(c):\n    return c\n@wrap\nclass Store:\n    def fetch_value(self):\n        return 5\n"),
    ("a self-constructing classmethod", "class Store:\n    @classmethod\n    def make(cls):\n        return cls()\n"
                                        "    def fetch_value(self):\n        return 5\n"),
    ("a class handed out by a classmethod", "class Store:\n    @classmethod\n    def me(cls):\n        return cls\n"
                                            "    def fetch_value(self):\n        return 5\n"),
])
def test_a_class_that_can_make_values_itself_is_not_contained(tmp_path, label, klass):
    files = _with_ambiguous_use()
    files["engine/klass.py"] = klass
    assert _rows(tmp_path, files)[NAME]["status"] == "UNKNOWN", label


def test_an_export_breaks_containment(tmp_path):
    files = _with_ambiguous_use()
    files["engine/klass.py"] = '__all__ = ["Store"]\n' + KLASS
    assert _rows(tmp_path, files)[NAME]["status"] == "UNKNOWN"


def test_a_dataclass_decorator_alone_does_not_open_a_class(tmp_path):
    files = _with_ambiguous_use()
    files["engine/klass.py"] = "from dataclasses import dataclass\n@dataclass\n" + KLASS
    assert _rows(tmp_path, files)[NAME]["status"] == "NOT_IN_USE"


def test_containment_never_hides_a_direct_caller(tmp_path):
    """The dead-path rule stands. Containment removes only unresolved evidence."""

    source = ("class Store:\n    @staticmethod\n    def fetch_value():\n        return 5\n"
              "    @staticmethod\n    def dead_caller():\n        return Store.fetch_value()\n")
    rows = _rows(tmp_path, {"engine/__init__.py": "", "engine/klass.py": source})
    assert rows[NAME]["status"] == "DEAD_PATH_UNCOVERED"
    assert rows[NAME]["callers"] == ["engine.klass.Store.dead_caller"]


#: Regex, not AST: a method independent of the analyser, for the classes whose containment matters.
CONTAINED = ("KnowledgeCache", "KnowledgeRegistry", "KnowledgeRepository", "KnowledgeResolver", "SchemaValidator")


@pytest.mark.parametrize("name", CONTAINED)
def test_containment_of_the_knowledge_classes_by_a_second_method(name):
    tracked = subprocess.run(["git", "-C", str(ROOT), "ls-files", "*.py"], capture_output=True, text=True,
                             check=True).stdout.split()
    uses = []
    for relative in tracked:
        if coverage_static.in_verification_surface(relative) or relative.startswith("scripts/check_reachability"):
            continue
        for line in (ROOT / relative).read_text(encoding="utf-8-sig").splitlines():
            stripped = re.sub(r'"[^"]*"', '""', line.strip())
            if not re.search(rf"\b{name}\b", stripped) or stripped.startswith(("#", "from ", "import ", f"class {name}")):
                continue
            if re.search(rf"\b{name}\.\w+", stripped) or re.search(rf"getattr\({name},", stripped):
                continue
            uses.append(f"{relative}: {stripped}")
    assert uses == [], f"{name} is used as a value outside the surface"


def test_the_knowledge_classes_are_contained_by_the_analyser(graph=None):
    graph = coverage_static.build_graph(ROOT)
    for name, module in (("KnowledgeCache", "cache"), ("KnowledgeRegistry", "registry"),
                         ("KnowledgeRepository", "repository"), ("KnowledgeResolver", "resolver"),
                         ("SchemaValidator", "validator")):
        assert graph.contained(f"engine.knowledge.{module}.{name}"), name


def test_withdrawing_containment_on_real_data_restores_unknown_and_refuses_exit():
    graph = copy.deepcopy(coverage_static.build_graph(ROOT))
    graph.escaping.add("engine.knowledge.cache.KnowledgeCache")
    members, _errors = c4.gated_members(ROOT / "certification")
    analysis = c4.analyse(graph, members)
    assert analysis["rows"]["engine.knowledge.cache.KnowledgeCache.get"]["status"] == "UNKNOWN"
    clause = c4.exit_clause_2(analysis)
    assert "engine.knowledge.cache.KnowledgeCache.get" in clause["material_unknown"]
    assert clause["satisfied"] is False


# ------------------------------------------------------------------ runtime proofs of the resolved paths

def test_varga_division_number_runs_on_the_certified_path(monkeypatch):
    from engine.astrology.varga_chart_builder import build_varga_chart
    from engine.astrology.varga_classifier import VargaClassification
    from engine.astrology.varga_registry import get_varga_rule, registered_vargas
    from engine.calculations.calculations import calculate
    from engine.models.birth_data import BirthData

    reads = []
    original = vars(VargaClassification)["division_number"]

    def getter(value):
        reads.append((sys._getframe(1).f_code.co_name, type(value)))
        return original.fget(value)

    monkeypatch.setattr(VargaClassification, "division_number", property(getter))
    snapshot = calculate(BirthData(2000, 1, 1, 12, 0, 0.0, 0.0, 0.0, "UTC")).snapshot
    division, school = sorted(registered_vargas())[0]
    build_varga_chart(snapshot, division, get_varga_rule(division, school), school)
    assert ("build_varga_chart", VargaClassification) in reads


def test_the_knowledge_loader_runs_on_the_certified_path(monkeypatch):
    from engine.astrology.dignity import is_exalted
    from engine.knowledge.loader import KnowledgeLoader

    loaded = []
    original = KnowledgeLoader.load

    def recording(path):
        loaded.append(Path(path).name)
        return original(path)

    monkeypatch.setattr(KnowledgeLoader, "load", staticmethod(recording))
    is_exalted("Sun", 1)
    assert loaded == ["dignities.json"]


def test_the_analyser_sees_that_path_too():
    graph = coverage_static.build_graph(ROOT)
    reach = graph.closure({"engine.astrology.dignity.is_exalted"})
    assert {"engine.knowledge.repository.KnowledgeRepository.load_json",
            "engine.knowledge.loader.KnowledgeLoader.load"} <= reach


def test_the_snapshot_wrapper_equals_the_gated_function_without_the_oracle():
    from engine.astronomy.profile import KP_KRISHNAMURTI, PARASHARI_LAHIRI
    from engine.calculations.calculations import calculate
    from engine.dasha.vimshottari import vimshottari_from_moon, vimshottari_from_snapshot
    from engine.models.birth_data import BirthData

    for profile, school in ((PARASHARI_LAHIRI, "parashari"), (KP_KRISHNAMURTI, "kp")):
        snapshot = calculate(BirthData(1988, 11, 23, 18, 45, 30.0, 51.5, -0.1, "UTC"), profile=profile).snapshot
        direct = vimshottari_from_moon(snapshot.sidereal_planets["Moon"].longitude, snapshot.julian_day, depth=2,
                                       school=school, provenance=snapshot.provenance)
        assert vimshottari_from_snapshot(snapshot, depth=2) == direct


# ------------------------------------------------------------------ the gates can fail

@pytest.mark.parametrize("attribute,replacement,gate", [
    ("equal_house_from_ascendant", support_paths.whole_sign_house, support_paths.gate_a_equal_house),
    ("map_planet", lambda longitude, ascendant: {"sign": 1}, support_paths.gate_b_map_planet),
    ("to_utc", lambda value: value.replace(tzinfo=timezone.utc), support_paths.gate_c_to_utc),
    ("rashi_chart", lambda snapshot: snapshot, support_paths.gate_f_rashi_chart),
])
def test_each_support_gate_fails_on_a_wrong_function(monkeypatch, attribute, replacement, gate):
    monkeypatch.setattr(support_paths, attribute, replacement)
    with pytest.raises(SystemExit) as stop:
        gate()
    assert stop.value.code == 3


def test_the_knowledge_gate_fails_when_the_loader_is_wrong(monkeypatch):
    original = support_paths.KnowledgeLoader.load

    def wrong(path):
        return dict(original(path), tampered=True)

    monkeypatch.setattr(support_paths.KnowledgeLoader, "load", staticmethod(wrong))
    with pytest.raises(SystemExit) as stop:
        support_paths.gate_d_knowledge_access()
    assert stop.value.code == 3


def test_the_knowledge_gate_fails_when_the_registry_stops_caching(monkeypatch):
    monkeypatch.setattr(support_paths.KnowledgeRegistry, "get",
                        classmethod(lambda cls, name: getattr(support_paths.KnowledgeRepository, name)()))
    with pytest.raises(SystemExit) as stop:
        support_paths.gate_d_knowledge_access()
    assert stop.value.code == 3


def test_the_relationship_comparator_reads_the_oracle_tables():
    """Hand-built tables, so this runs without PyJHora. A wrong table entry must count."""

    from engine.astrology.dignity import natural_relationship, Relationship

    groups = {Relationship.FRIEND: [], Relationship.NEUTRAL: [], Relationship.ENEMY: []}
    for source in support_paths.GRAHAS:
        row = {kind: [] for kind in groups}
        for index, target in enumerate(support_paths.GRAHAS):
            if target != source:
                row[natural_relationship(source, target)].append(index)
        for kind in groups:
            groups[kind].append(row[kind])
    friends, neutrals, enemies = groups[Relationship.FRIEND], groups[Relationship.NEUTRAL], groups[Relationship.ENEMY]
    assert support_paths.relationship_mismatches(natural_relationship, friends, neutrals, enemies) == 0
    swapped = [list(row) for row in friends]
    swapped[1], swapped_neutrals = [0], [list(row) for row in neutrals]  # Moon no longer calls Mercury a friend.
    swapped_neutrals[1] = swapped_neutrals[1] + [3]
    assert support_paths.relationship_mismatches(natural_relationship, swapped, swapped_neutrals, enemies) == 1


def test_the_relationship_comparator_refuses_an_unclassified_pair():
    empty = [[] for _ in support_paths.GRAHAS]
    with pytest.raises(SystemExit):
        support_paths.relationship_mismatches(lambda source, target: None, empty, empty, empty)


@pytest.mark.parametrize("attribute", ["one_based", "name"])
def test_the_sign_gate_fails_when_the_newly_declared_accessor_is_wrong(monkeypatch, attribute):
    """Declaring them GATED is only true if the existing gate would catch them being wrong."""

    from engine.astrology.sign import Sign

    wrong = 1 if attribute == "one_based" else "Wrong"
    monkeypatch.setattr(Sign, attribute, property(lambda self: wrong))
    with pytest.raises(SystemExit) as stop:
        certify_sign_convention.gate_b_sign_type()
    assert stop.value.code != 0


def test_the_declared_support_members_are_supported_by_the_static_reading():
    """S10: a declaration the certifier's own gates do not reach would fail C3."""

    payload = json.loads((ROOT / "certification" / SUPPORT).read_text(encoding="utf-8"))
    graph = coverage_static.build_graph(ROOT)
    assert c3.check_independent_evidence(SUPPORT, payload, graph, ROOT) == []
    planted = copy.deepcopy(payload)
    planted["capabilities"][0]["members"][0]["exercised_by"] = ["C_to_utc_reference"]
    errors = c3.check_independent_evidence(SUPPORT, planted, graph, ROOT)
    assert any("equal_house_from_ascendant" in error for error in errors)


# ------------------------------------------------------------------ the real tree

#: The 11 ADR-0108 findings. Each stays in use, by a real caller: nothing here was exempted.
ORIGINAL_DEAD_PATHS = (
    "engine.astrology.house.equal_house_from_ascendant", "engine.astrology.planet_mapper.map_planet",
    "engine.astrology.rashi_chart.rashi_chart", "engine.astrology.sign.Sign.name",
    "engine.astrology.sign.Sign.one_based", "engine.core.timezone_engine.to_utc",
    "engine.dasha.vimshottari.vimshottari_from_snapshot", "engine.knowledge.loader.KnowledgeLoader.load",
    "engine.knowledge.registry.KnowledgeRegistry.get",
    "engine.knowledge.repository.KnowledgeRepository.natural_relationships",
    "engine.knowledge.validator.SchemaValidator.load_json",
)


@pytest.mark.parametrize("name", ORIGINAL_DEAD_PATHS)
def test_each_original_finding_is_covered_and_still_counted_as_in_use(name):
    _errors, report = c4.check()
    row = report["rows"][name]
    assert row["status"] == "IN_USE_COVERED" and row["covered"] is True
    assert row["callers"], "U1 is preserved: the call site still counts"


def test_no_finding_is_open_and_the_clause_is_established():
    errors, report = c4.check()
    assert errors == []
    clause = report["exit_clause_2"]
    assert clause["live_path_uncovered"] == [] and clause["dead_path_uncovered"] == []
    assert clause["material_unknown"] == []
    assert clause["satisfied"] is True
    assert c4.open_findings(json.loads(BACKLOG.read_text(encoding="utf-8"))) == {}


def test_the_three_transit_overclaims_are_untouched():
    backlog = json.loads(BACKLOG.read_text(encoding="utf-8"))
    entries = {entry["id"]: entry for entry in backlog["entries"]}
    for entry in ("OVERCLAIM-TRANSIT-RETURNS", "OVERCLAIM-TRANSIT-NATAL-CONJUNCTIONS", "OVERCLAIM-TRANSIT-NATAL-VIEW"):
        assert entries[entry]["status"] == "OPEN"
        assert entries[entry]["disposition"] == "OPEN_SCOPE_OVERCLAIM"


def test_withdrawing_the_support_artifact_reopens_the_findings_through_the_command_line(tmp_path):
    directory = tmp_path / "certification"
    directory.mkdir()
    for path in (ROOT / "certification").glob("*.json"):
        if path.name != SUPPORT:
            shutil.copy2(path, directory / path.name)
    script = str(ROOT / "scripts" / "check_reachability.py")
    gate = subprocess.run([sys.executable, script, "--certification-dir", str(directory)],
                          capture_output=True, text=True)
    assert gate.returncode == 1
    assert "R1 engine.core.timezone_engine.to_utc is DEAD_PATH_UNCOVERED" in gate.stdout
    exit_check = subprocess.run([sys.executable, script, "--certification-dir", str(directory), "--exit-criterion"],
                                capture_output=True, text=True)
    assert exit_check.returncode == 1
    assert "EXIT CRITERION: REFUSED" in exit_check.stdout
    assert "dead-path uncovered: engine.core.timezone_engine.to_utc" in exit_check.stdout


def test_a_failed_support_artifact_is_not_coverage(tmp_path):
    directory = tmp_path / "certification"
    directory.mkdir()
    for path in (ROOT / "certification").glob("*.json"):
        shutil.copy2(path, directory / path.name)
    payload = json.loads((directory / SUPPORT).read_text(encoding="utf-8"))
    payload["result"] = "FAIL"
    (directory / SUPPORT).write_text(json.dumps(payload), encoding="utf-8")
    errors, _report = c4.check(certification_dir=directory)
    assert any(error.startswith("R1") and "to_utc" in error for error in errors)


def test_the_exit_command_answers_clause_2_and_never_jataka_exit():
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_reachability.py"), "--exit-criterion"],
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stdout
    assert "clause 2 satisfied" in result.stdout
    assert "not JATAKA exit" in result.stdout
