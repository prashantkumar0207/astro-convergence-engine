"""Negative controls for C2, C3, C4 and C5 (ADR-0099 s5 and s7, ADR-0101, ADR-0107).

A gate that cannot fail is not evidence. Each control plants a real violation and
requires the real enforcement path to reject it for the stated reason. Mutations are
applied to temporary copies or in-memory structures; committed files are never modified.
"""

from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import capability_declarations as declarations  # noqa: E402
import check_reachability as c4  # noqa: E402
import check_scope_coverage as c3  # noqa: E402
import coverage_static  # noqa: E402
from scripts import check_capability_state as c2  # noqa: E402

BACKLOG = ROOT / "docs" / "CERTIFICATION_REMEDIATION_BACKLOG.json"
TRANSIT = "TRANSIT_V1_certification.json"
D45 = "VARGA_D45_V1_certification.json"


@pytest.fixture(scope="module")
def graph():
    return coverage_static.build_graph(ROOT)


@pytest.fixture()
def corpus(tmp_path):
    directory = tmp_path / "certification"
    directory.mkdir()
    for path in (ROOT / "certification").glob("*.json"):
        shutil.copy2(path, directory / path.name)
    backlog = tmp_path / "backlog.json"
    shutil.copy2(BACKLOG, backlog)
    return directory, backlog


def _edit(directory: Path, name: str, change) -> None:
    path = directory / name
    payload = json.loads(path.read_text(encoding="utf-8"))
    change(payload)
    path.write_text(json.dumps(payload), encoding="utf-8")


def _c3_errors(corpus, graph) -> list[str]:
    directory, backlog = corpus
    return c3.check(directory, backlog, ROOT, graph)[0]


def _expect(errors: list[str], code: str, fragment: str = "") -> None:
    assert any(error.startswith(code) and fragment in error for error in errors), errors[:8]


# ------------------------------------------------------------------ C2

def _status_text() -> str:
    return (ROOT / "docs" / "ENGINE_STATUS.md").read_text(encoding="utf-8")


def test_c2_pristine_passes():
    assert c2.check(_status_text()) == []


SUPPORT_LINE = '"certified_support_not_declared": ["SUPPORT_PATHS_V1"]'


def test_c2_support_artifact_is_not_declared():
    """ADR-0099 s2: certified is not declared. It must appear in no declaring list."""

    assert "SUPPORT_PATHS_V1" not in c2.extract_block(_status_text())[0]["declared_production_analytical_inputs"]
    assert "SUPPORT_PATHS_V1" not in c2.extract_block(_status_text())[0]["certified_capabilities"]


@pytest.mark.parametrize("planted", [
    '"certified_support_not_declared": ["SUPPORT_PATHS_V1", "TRANSIT_V1"]',
    '"certified_support_not_declared": ["TRANSIT_V1"]',
    '"certified_support_not_declared": []',
])
def test_c2_rejects_a_document_edit_of_the_support_list(planted):
    """The list cannot be a way to move a declared capability out of the declared set."""

    text = _status_text()
    assert SUPPORT_LINE in text
    _expect(c2.check(text.replace(SUPPORT_LINE, planted)), "F18")


def test_c2_rejects_declaring_the_support_artifact():
    text = _status_text()
    planted = text.replace('"certified_capabilities": [\n', '"certified_capabilities": [\n    "SUPPORT_PATHS_V1",\n', 1)
    assert planted != text
    _expect(c2.check(planted), "F18", "must not be in a declaring list")


def test_c2_declared_union_is_the_three_declaring_lists_and_live_state():
    block, _ = c2.extract_block(_status_text())
    declared = set(block["declared_production_analytical_inputs"])
    expected = {f"D{d}" for d in block["production_registered_vargas"] + block["dedicated_production_vargas"]}
    assert declared == expected | set(block["certified_capabilities"])
    assert "D4" not in declared and "D16" not in declared, "certified but not registered: ADR-0099 s2"
    assert "D27" not in declared and "D60" not in declared


def test_c2_rejects_a_missing_key():
    text = _status_text().replace('"declared_production_analytical_inputs"', '"renamed_key"', 1)
    _expect(c2.check(text), "F10", "declared_production_analytical_inputs")


def test_c2_rejects_a_member_dropped_from_the_union():
    text = _status_text().replace('"D40", "D45"', '"D40"', 1)
    assert text != _status_text()
    _expect(c2.check(text), "F15", "D45")


def test_c2_rejects_an_invented_member():
    text = _status_text().replace('"D1", "D2"', '"D1", "D99", "D2"', 1)
    errors = c2.check(text)
    _expect(errors, "F15", "D99")
    _expect(errors, "F16", "D99")


def _live_inputs():
    artifacts, _errors = c2.live_pass_artifacts()
    return artifacts, c2.live_artifact_payloads(), c2.accepted_decisions()


def test_c2_rejects_a_member_whose_artifact_is_not_pass():
    artifacts, payloads, accepted = _live_inputs()
    errors = c2.check(_status_text(), artifacts=dict(artifacts, VARGA_D45_V1="FAIL"),
                      payloads=payloads, accepted=accepted)
    _expect(errors, "F16", "D45")


def test_c2_rejects_a_dedicated_division_with_no_gated_capability():
    """D9 is the reason this check exists: before Stage B it had no live PASS artifact."""

    artifacts, payloads, accepted = _live_inputs()
    planted = copy.deepcopy(payloads)
    for capability in planted["current_engine"]["capabilities"]:
        if capability["id"] == "vargas.d9":
            for member in capability["members"]:
                member["disposition"] = "SCOPE_NOT_GATED"
    errors = c2.check(_status_text(), artifacts=artifacts, payloads=planted, accepted=accepted)
    _expect(errors, "F16", "vargas.d9")


def test_c2_rejects_an_unratified_decision_entry():
    artifacts, payloads, accepted = _live_inputs()
    errors = c2.check(_status_text(), artifacts=artifacts, payloads=payloads, accepted=accepted - {"ADR-0077"})
    _expect(errors, "F17", "ADR-0077")


def test_c2_accepted_decisions_reads_the_real_status_lines():
    accepted = c2.accepted_decisions()
    assert {"ADR-0005", "ADR-0099", "ADR-0107"} <= accepted
    assert not {"ADR-0004", "ADR-0018", "ADR-0105"} & accepted, "these read PROPOSED"


def test_c2_command_line_fails_on_a_planted_document(tmp_path):
    probe = tmp_path / "status.md"
    probe.write_text(_status_text().replace('"D40", "D45"', '"D40"'), encoding="utf-8")
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_capability_state.py"), str(probe)],
                            capture_output=True, text=True)
    assert result.returncode == 1 and "F15" in result.stdout


# ------------------------------------------------------------------ C3

def test_c3_pristine_passes(corpus, graph):
    assert _c3_errors(corpus, graph) == []


def test_c3_covers_exactly_the_adr_0102_universe():
    # ADR-0102 s2's 22, plus the artifact ADR-0108 s4 item 5's certification route added.
    assert len(c3.SCOPE_BEARING_ARTIFACTS) == 23 and "SUPPORT_PATHS_V1_certification.json" in c3.SCOPE_BEARING_ARTIFACTS
    frozen = c2.FROZEN_EVIDENCE
    assert not frozen & set(c3.SCOPE_BEARING_ARTIFACTS)
    assert set(c3.SCOPE_BEARING_ARTIFACTS) | frozen == {p.name for p in (ROOT / "certification").glob("*.json")}


def test_c3_rejects_a_missing_enumeration(corpus, graph):
    _edit(corpus[0], D45, lambda p: p.pop("capabilities"))
    _expect(_c3_errors(corpus, graph), "S1", D45)


def test_c3_rejects_a_bad_identifier(corpus, graph):
    def change(payload):
        payload["capabilities"][0]["id"] = "three.segment.slug"
    _edit(corpus[0], D45, change)
    _expect(_c3_errors(corpus, graph), "S1", "three.segment.slug")


def test_c3_rejects_a_gate_without_exercises(corpus, graph):
    _edit(corpus[0], D45, lambda p: p["gates"]["B_dense_sweep"].pop("exercises"))
    _expect(_c3_errors(corpus, graph), "S3", "B_dense_sweep")


def test_c3_rejects_an_empty_exercises_with_no_reason(corpus, graph):
    name = "VARGA_D24_V1_certification.json"
    _edit(corpus[0], name, lambda p: p["gates"]["E_independent_validator"].pop("exercises_note"))
    _expect(_c3_errors(corpus, graph), "S3", "E_independent_validator")


def test_c3_rejects_a_scalar_gate_with_no_declaration(corpus, graph):
    name = "VIMSHOTTARI_V1_certification.json"
    _edit(corpus[0], name, lambda p: p["scalar_gate_exercises"].pop("independent_validator"))
    _expect(_c3_errors(corpus, graph), "S3", "independent_validator")


def test_c3_rejects_an_unknown_capability_in_exercises(corpus, graph):
    _edit(corpus[0], D45, lambda p: p["gates"]["B_dense_sweep"]["exercises"].append("vargas.d99"))
    _expect(_c3_errors(corpus, graph), "S4", "vargas.d99")


def test_c3_rejects_an_untracked_scope_overclaim(corpus, graph):
    """ADR-0101 s5 item 3: enumerated, in no gate, not in scope_not_gated."""

    def change(payload):
        payload["capabilities"].append({"id": "vargas.phantom", "members": [{
            "callable": "engine.transits.events.returns", "kind": "callable",
            "disposition": "SCOPE_NOT_GATED", "exercised_by": [], "reason": "planted"}]})
    _edit(corpus[0], D45, change)
    _expect(_c3_errors(corpus, graph), "S5", "vargas.phantom")


@pytest.mark.parametrize("entry", ["OVERCLAIM-TRANSIT-RETURNS", "OVERCLAIM-TRANSIT-NATAL-CONJUNCTIONS",
                                   "OVERCLAIM-TRANSIT-NATAL-VIEW"])
def test_c3_rejects_a_transit_overclaim_the_backlog_stops_tracking(entry, corpus, graph):
    directory, backlog = corpus
    payload = json.loads(backlog.read_text(encoding="utf-8"))
    payload["entries"] = [item for item in payload["entries"] if item["id"] != entry]
    backlog.write_text(json.dumps(payload), encoding="utf-8")
    _expect(_c3_errors(corpus, graph), "S5", entry)


def test_c3_rejects_closing_a_transit_overclaim_without_a_decision(corpus, graph):
    directory, backlog = corpus
    payload = json.loads(backlog.read_text(encoding="utf-8"))
    for item in payload["entries"]:
        if item["id"] == "OVERCLAIM-TRANSIT-RETURNS":
            item["status"] = "CLOSED"
    backlog.write_text(json.dumps(payload), encoding="utf-8")
    _expect(_c3_errors(corpus, graph), "S5", "OVERCLAIM-TRANSIT-RETURNS")


def test_c3_transit_overclaims_are_open_and_not_scope_not_gated():
    """Listing them in scope_not_gated would silently select a DP-040 option (ADR-0107)."""

    payload = json.loads((ROOT / "certification" / TRANSIT).read_text(encoding="utf-8"))
    assert payload["scope_not_gated"] == []
    states = {capability["id"]: capability["members"][0]["disposition"] for capability in payload["capabilities"]}
    for capability in ("transits.returns", "transits.natal_conjunctions", "transits.natal_view"):
        assert states[capability] == "OPEN_SCOPE_OVERCLAIM"


def test_c3_rejects_a_gated_member_with_no_gate(corpus, graph):
    def change(payload):
        payload["capabilities"][0]["members"][0]["exercised_by"] = []
    _edit(corpus[0], D45, change)
    _expect(_c3_errors(corpus, graph), "S6", "GATED")


def test_c3_rejects_a_gate_naming_a_parent_without_a_member(corpus, graph):
    """Stage A: a member must not read as verified because its parent was named."""

    def change(payload):
        payload["gates"]["E_independent_validator"]["exercises"] = ["vargas.d45"]
        for member in payload["capabilities"][0]["members"]:
            if "E_independent_validator" in member["exercised_by"]:
                member["exercised_by"].remove("E_independent_validator")
    _edit(corpus[0], D45, change)
    _expect(_c3_errors(corpus, graph), "S6", "naming a parent")


def test_c3_rejects_a_member_gate_that_does_not_list_the_capability(corpus, graph):
    _edit(corpus[0], D45, lambda p: p["gates"]["B_dense_sweep"].__setitem__("exercises", []))
    errors = _c3_errors(corpus, graph)
    _expect(errors, "S6", "B_dense_sweep")


def test_c3_rejects_a_member_that_does_not_exist(corpus, graph):
    def change(payload):
        payload["capabilities"][0]["members"][1]["callable"] = "engine.astrology.varga_classifier.invented"
    _edit(corpus[0], D45, change)
    _expect(_c3_errors(corpus, graph), "S7", "invented")


def test_c3_rejects_a_scope_not_gated_item_without_a_reason(corpus, graph):
    name = "VIMSHOTTARI_V1_certification.json"
    def change(payload):
        payload["scope_not_gated"][0]["reason"] = "  "
    _edit(corpus[0], name, change)
    _expect(_c3_errors(corpus, graph), "S8", "reason")


@pytest.mark.parametrize("name,gate,member", [
    (D45, "A_table_integrity", "engine.astrology.varga_classifier.classify"),
    ("VARGA_D24_V1_certification.json", "A_table_integrity", "engine.astrology.varga_classifier.classify"),
    (TRANSIT, "C_oracle_anchors", "engine.transits.events.nakshatra_ingresses"),
])
def test_c3_independent_evidence_rejects_an_unsupported_claim(name, gate, member, corpus, graph):
    """S10: a gate may not declare a member the certifier's source never reaches."""

    def change(payload):
        for capability in payload["capabilities"]:
            for item in capability["members"]:
                if item["callable"] == member:
                    item["exercised_by"].append(gate)
                    if capability["id"] not in payload["gates"][gate]["exercises"]:
                        payload["gates"][gate]["exercises"].append(capability["id"])
    _edit(corpus[0], name, change)
    _expect(_c3_errors(corpus, graph), "S10", gate)


def test_c3_command_line_fails_when_the_backlog_is_stripped(corpus, tmp_path):
    directory, backlog = corpus
    payload = json.loads(backlog.read_text(encoding="utf-8"))
    payload["entries"] = []
    backlog.write_text(json.dumps(payload), encoding="utf-8")
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_scope_coverage.py"), str(directory),
                             str(backlog)], capture_output=True, text=True)
    assert result.returncode == 1 and "S5" in result.stdout


def test_emit_refuses_a_report_that_disagrees_with_its_declaration():
    report = {"gates": {"A_table_integrity": {}, "Z_undeclared_gate": {}}}
    with pytest.raises(declarations.DeclarationError, match="Z_undeclared_gate"):
        declarations.apply(report, D45)
    with pytest.raises(declarations.DeclarationError, match="no capability declaration"):
        declarations.apply({"gates": {"A": {}}}, "UNKNOWN_certification.json")


def test_apply_does_not_alias_a_gate_published_under_another_key():
    block = {"mismatches": 0}
    gates = {name: {} for name in json.loads((ROOT / "certification" / D45).read_text(encoding="utf-8"))["gates"]}
    gates["C_oracle"] = block
    report = {"gates": gates, "oracle": block}
    declarations.apply(report, D45)
    assert "exercises" in report["gates"]["C_oracle"]
    assert "exercises" not in report["oracle"], "the published oracle record must not change"


# ------------------------------------------------------------------ C4

def _tree(tmp_path: Path, files: dict[str, str]):
    for relative, text in files.items():
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return coverage_static.build_graph(tmp_path, sorted(files))


FIXTURE = {
    "engine/__init__.py": "",
    "engine/main.py": "from engine.covered import certified\n\ndef route():\n    return certified()\n",
    "engine/covered.py": "def certified():\n    return helper()\n\ndef helper():\n    return 1\n",
    "engine/live.py": "def uncovered():\n    return 2\n",
    "engine/dead.py": "from engine.leaf import only_dead_caller\n\ndef nobody_calls_me():\n    return only_dead_caller()\n",
    "engine/leaf.py": "def only_dead_caller():\n    return 3\n",
    "engine/unused.py": "def not_in_use():\n    return 4\n",
    "engine/klass.py": "class Store:\n    def fetch_value(self):\n        return 5\n",
    "scripts/tool.py": ("from engine.klass import Store\nfrom engine.live import uncovered\n\nMADE = Store()\n\n"
                        "def main(store):\n    uncovered()\n    return store.fetch_value()\n"),
    "scripts/certify_x.py": "from engine.unused import not_in_use\n\ndef gate():\n    return not_in_use()\n",
}


@pytest.fixture()
def fixture_analysis(tmp_path):
    graph = _tree(tmp_path, FIXTURE)
    return c4.analyse(graph, {"engine.covered.certified"})


@pytest.mark.parametrize("name,status", [
    ("engine.covered.certified", "IN_USE_COVERED"),
    ("engine.covered.helper", "IN_USE_COVERED"),
    ("engine.live.uncovered", "IN_USE_UNCOVERED"),
    ("engine.leaf.only_dead_caller", "DEAD_PATH_UNCOVERED"),
    ("engine.klass.Store.fetch_value", "UNKNOWN"),
    ("engine.unused.not_in_use", "NOT_IN_USE"),
    ("engine.dead.nobody_calls_me", "NOT_IN_USE"),
])
def test_c4_classifies_each_status_on_a_known_tree(name, status, fixture_analysis):
    assert fixture_analysis["rows"][name]["status"] == status


def test_c4_a_call_from_the_verification_surface_is_not_use(fixture_analysis):
    """ADR-0099 s3: only scripts/certify_x.py calls not_in_use, and it is inside the surface."""

    assert "callers" not in fixture_analysis["rows"]["engine.unused.not_in_use"]


def test_c4_unknown_is_disclosed_never_absent(fixture_analysis):
    clause = c4.exit_clause_2(fixture_analysis)
    assert clause["unknown_not_established_either_way"] == ["engine.klass.Store.fetch_value"]


def test_c4_an_export_is_use_without_any_caller(tmp_path):
    files = {"engine/api/__init__.py": "from engine.exported import served\n",
             "engine/exported.py": "def served():\n    return 1\n"}
    analysis = c4.analyse(_tree(tmp_path, files), set())
    assert analysis["rows"]["engine.exported.served"]["status"] == "IN_USE_UNCOVERED"
    assert analysis["rows"]["engine.exported.served"]["exported_by"] == ["engine/api/__init__.py"]


def test_c4_all_export_counts(tmp_path):
    files = {"engine/pkg.py": '__all__ = ["public"]\n\ndef public():\n    return 1\n'}
    analysis = c4.analyse(_tree(tmp_path, files), set())
    assert analysis["rows"]["engine.pkg.public"]["status"] == "IN_USE_UNCOVERED"


def test_c4_coverage_does_not_flow_from_callee_to_caller(tmp_path):
    """A delegator is not covered because its delegate is: that is C5's rule (ADR-0099 s5)."""

    files = {"engine/delegate.py": "def certified():\n    return 1\n\ndef wrapper():\n    return certified()\n",
             "scripts/tool.py": "from engine.delegate import wrapper\n\ndef main():\n    return wrapper()\n"}
    analysis = c4.analyse(_tree(tmp_path, files), {"engine.delegate.certified"})
    assert analysis["rows"]["engine.delegate.wrapper"]["status"] == "IN_USE_UNCOVERED"
    assert analysis["rows"]["engine.delegate.certified"]["status"] == "IN_USE_COVERED"


def test_c4_unparsable_source_fails_rather_than_skips(tmp_path):
    files = {"engine/broken.py": "def oops(:\n"}
    graph = _tree(tmp_path, files)
    assert "engine/broken.py" in graph.unparsed
    certification = tmp_path / "certification"
    certification.mkdir()
    _report, errors, _graph = c4.build_report(tmp_path, certification, graph)
    _expect(errors, "R3", "engine/broken.py")


def test_c4_reads_byte_order_marked_source():
    """Three tracked files begin with a BOM. Skipping them would hide navamsa_chart."""

    assert coverage_static.build_graph(ROOT).unparsed == {}


def test_c4_pristine_passes():
    errors, report = c4.check()
    assert errors == []
    assert "IN_USE_UNCOVERED" not in report["summary"], "no live-path uncovered function at this commit"


def test_c4_rejects_an_untracked_finding(corpus):
    """Withdraw the certification that covers it. No backlog entry tracks it, so R1 must fire."""

    directory, backlog = corpus
    (directory / "SUPPORT_PATHS_V1_certification.json").unlink()
    errors, _report = c4.check(certification_dir=directory, backlog_path=backlog)
    _expect(errors, "R1", "to_utc")


def test_c4_rejects_a_stale_finding(tmp_path):
    backlog = json.loads(BACKLOG.read_text(encoding="utf-8"))
    backlog["entries"].append({"id": "REACHABILITY-planted", "callable": "engine.kp.chain.kp_chain",
                               "status": "OPEN", "disposition": "OPEN_REACHABILITY_FINDING"})
    probe = tmp_path / "backlog.json"
    probe.write_text(json.dumps(backlog), encoding="utf-8")
    errors, _report = c4.check(backlog_path=probe)
    _expect(errors, "R2", "kp_chain")


def test_c4_rejects_a_planted_live_uncovered_function(graph):
    """A new production function called from outside the surface, certified by nothing."""

    planted = copy.deepcopy(graph)
    planted.definitions["engine.planted.new_analysis"] = "engine/planted.py"
    planted.owners["scripts.tool"] = "scripts/tool.py"
    planted.edges["scripts.tool"].add("engine.planted.new_analysis")
    members, _errors = c4.gated_members(ROOT / "certification")
    analysis = c4.analyse(planted, members)
    assert analysis["rows"]["engine.planted.new_analysis"]["status"] == "IN_USE_UNCOVERED"
    findings = c4.open_findings(json.loads(BACKLOG.read_text(encoding="utf-8")))
    _expect(c4.evaluate(analysis, findings), "R1", "new_analysis")


def test_c4_withdrawing_all_coverage_uncovers_what_is_in_use(graph):
    """The check reads real coverage: with none, the served pipeline becomes a finding."""

    analysis = c4.analyse(graph, set())
    assert analysis["rows"]["engine.calculations.calculations.calculate"]["status"] == "IN_USE_UNCOVERED"
    assert not [name for name, row in analysis["rows"].items() if row["status"] == "IN_USE_COVERED"]


def test_c4_withdrawing_one_artifact_uncovers_only_what_it_alone_covers(graph):
    """find_crossings is covered only through TRANSIT_V1 and through Vimshottari's use of it, if any."""

    members, _errors = c4.gated_members(ROOT / "certification")
    transit = json.loads((ROOT / "certification" / TRANSIT).read_text(encoding="utf-8"))
    withdrawn = {member["callable"] for capability in transit["capabilities"] for member in capability["members"]
                 if member["disposition"] == "GATED"}
    baseline = c4.analyse(graph, members)["rows"]
    reduced = c4.analyse(graph, members - withdrawn)["rows"]
    assert reduced["engine.transits.events.sign_ingresses"]["covered"] is False
    assert baseline["engine.transits.events.sign_ingresses"]["covered"] is True
    assert reduced["engine.transits.events.sign_ingresses"]["status"] in c4.UNCOVERED


def test_c4_only_gated_members_of_pass_artifacts_are_coverage(tmp_path):
    source = json.loads((ROOT / "certification" / TRANSIT).read_text(encoding="utf-8"))
    directory = tmp_path / "certification"
    directory.mkdir()
    (directory / TRANSIT).write_text(json.dumps(source), encoding="utf-8")
    members, _errors = c4.gated_members(directory)
    assert "engine.transits.crossing.find_crossings" in members
    assert "engine.transits.events.returns" not in members, "an open overclaim is not coverage"
    source["result"] = "FAIL"
    (directory / TRANSIT).write_text(json.dumps(source), encoding="utf-8")
    assert c4.gated_members(directory)[0] == set()


def test_c4_frozen_inventory_is_not_read_as_coverage():
    """ADR-0092: ENGINE_CAPABILITY_INVENTORY has a `capabilities` key, and is not this enumeration."""

    frozen = json.loads((ROOT / "certification" / "ENGINE_CAPABILITY_INVENTORY.json").read_text(encoding="utf-8"))
    assert "capabilities" in frozen and "capability_schema" not in frozen
    assert "ENGINE_CAPABILITY_INVENTORY" not in " ".join(c4.gated_members(ROOT / "certification")[0])


def test_c4_rejects_a_stale_committed_report(tmp_path):
    probe = tmp_path / "report.json"
    probe.write_text(c4.REPORT.read_text(encoding="utf-8").replace("IN_USE_COVERED", "IN_USE_COVERED ", 1),
                     encoding="utf-8")
    errors, _report = c4.check(report_path=probe)
    _expect(errors, "R4", "report.json")


def test_c4_command_line_fails_on_a_planted_stale_finding(tmp_path):
    backlog = json.loads(BACKLOG.read_text(encoding="utf-8"))
    backlog["entries"].append({"id": "REACHABILITY-planted", "callable": "engine.kp.chain.kp_chain",
                               "status": "OPEN", "disposition": "OPEN_REACHABILITY_FINDING"})
    probe = tmp_path / "backlog.json"
    probe.write_text(json.dumps(backlog), encoding="utf-8")
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_reachability.py"), "--backlog", str(probe)],
                            capture_output=True, text=True)
    assert result.returncode == 1 and "R2" in result.stdout


def test_c4_findings_match_the_exit_clause():
    _errors, report = c4.check()
    clause = report["exit_clause_2"]
    open_items = c4.open_findings(json.loads(BACKLOG.read_text(encoding="utf-8")))
    assert set(open_items) == set(clause["live_path_uncovered"]) | set(clause["dead_path_uncovered"])


#: A value of Store exists outside the surface, so the unresolved call may land on it.
UNKNOWN_ONLY = {
    "engine/__init__.py": "",
    "engine/klass.py": "class Store:\n    def fetch_value(self):\n        return 5\n",
    "scripts/tool.py": ("from engine.klass import Store\nMADE = Store()\n"
                        "def main(store):\n    return store.fetch_value()\n"),
}


def test_c4_unknown_alone_refuses_an_exit_pass(tmp_path):
    """The defect the CEO audit found: zero uncovered, one unresolved method, and the old
    rule (`not live and not dead`) called that satisfied."""

    clause = c4.exit_clause_2(c4.analyse(_tree(tmp_path, UNKNOWN_ONLY), set()))
    assert clause["live_path_uncovered"] == [] and clause["dead_path_uncovered"] == []
    assert clause["material_unknown"] == ["engine.klass.Store.fetch_value"]
    assert clause["no_confirmed_violations"] is True
    assert clause["coverage_established"] is False
    assert clause["satisfied"] is False
    assert any("material UNKNOWN" in refusal for refusal in c4.exit_refusals(clause))


def test_c4_exit_can_be_satisfied_when_nothing_is_unresolved(tmp_path):
    """The refusal is not vacuous: without the unresolved use, the same tree passes."""

    files = dict(UNKNOWN_ONLY, **{"scripts/tool.py": "def main():\n    return 1\n"})
    clause = c4.exit_clause_2(c4.analyse(_tree(tmp_path, files), set()))
    assert clause["unknown_not_established_either_way"] == []
    assert clause["satisfied"] is True and c4.exit_refusals(clause) == []


def test_c4_a_covered_unknown_is_not_material(tmp_path):
    analysis = c4.analyse(_tree(tmp_path, UNKNOWN_ONLY), {"engine.klass.Store.fetch_value"})
    clause = c4.exit_clause_2(analysis)
    assert clause["unknown_not_established_either_way"] == ["engine.klass.Store.fetch_value"]
    assert clause["material_unknown"] == [] and clause["satisfied"] is True


def test_c4_real_tree_with_a_planted_unknown_refuses_on_unknown_alone(graph):
    """The same control on real data: one unresolved method, no dead path, and exit is refused."""

    planted = copy.deepcopy(graph)
    planted.escaping.add("engine.knowledge.cache.KnowledgeCache")
    members, _errors = c4.gated_members(ROOT / "certification")
    clause = c4.exit_clause_2(c4.analyse(planted, members))
    assert clause["live_path_uncovered"] == [] and clause["dead_path_uncovered"] == []
    assert clause["no_confirmed_violations"] is True
    assert clause["material_unknown"], "this control needs at least one real UNKNOWN"
    assert clause["satisfied"] is False
    assert any("material UNKNOWN" in refusal for refusal in c4.exit_refusals(clause))


def test_c4_the_ordinary_gate_states_the_exit_clause():
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_reachability.py")],
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stdout
    assert "coverage established: True" in result.stdout
    assert "exit clause 2 satisfied: True" in result.stdout


def test_c4_a_new_unknown_is_reported_as_not_reviewed(graph, tmp_path):
    planted = copy.deepcopy(graph)
    planted.escaping.add("engine.knowledge.cache.KnowledgeCache")
    report, _errors, _graph = c4.build_report(ROOT, ROOT / "certification", planted)
    assert report["unknown_review"]["engine.knowledge.cache.KnowledgeCache.get"] == "NOT REVIEWED"


def test_c4_dasha_period_properties_run_on_the_certified_path(monkeypatch):
    """The committed proof behind RECEIVER_EVIDENCE: run the certified function and record
    what actually reads each property, and on what type of object."""

    from engine.dasha.vimshottari import vimshottari_from_moon
    from engine.models.dasha import DashaPeriod

    reads = {"lord": [], "duration_years": []}

    def recording(name):
        original = vars(DashaPeriod)[name]

        def getter(period):
            reads[name].append((sys._getframe(1).f_code.co_name, type(period)))
            return original.fget(period)

        return property(getter)

    for name in reads:
        monkeypatch.setattr(DashaPeriod, name, recording(name))
    timeline = vimshottari_from_moon(123.4, 2451545.0, depth=2)
    assert timeline.periods
    for name, seen in reads.items():
        assert seen, f"{name} was not read on the certified path"
        assert {caller for caller, _type in seen} == {"_subdivide"}, name
        assert {kind for _caller, kind in seen} == {DashaPeriod}, name


def test_c4_dasha_properties_are_covered_only_through_their_evidence(graph):
    members, _errors = c4.gated_members(ROOT / "certification")
    without = c4.analyse(graph, members)["rows"]
    assert without["engine.models.dasha.DashaPeriod.lord"]["status"] == "UNKNOWN"
    _errors, report = c4.check()
    for name in ("lord", "duration_years"):
        row = report["rows"][f"engine.models.dasha.DashaPeriod.{name}"]
        assert row["status"] == "IN_USE_COVERED" and row["covered"] is True
        assert row["callers"] == ["engine.dasha.vimshottari._subdivide"]
        assert row["receiver_evidence"].endswith("test_c4_dasha_period_properties_run_on_the_certified_path")


def test_c4_coverage_of_a_proven_method_is_withdrawn_with_its_certification(graph):
    """Evidence shows the use, not the coverage: remove the certified caller and it is uncovered."""

    members, _errors = c4.gated_members(ROOT / "certification")
    resolved, errors = c4.apply_receiver_evidence(graph, c4.RECEIVER_EVIDENCE, ROOT)
    assert errors == []
    analysis = c4.analyse(resolved, members - {"engine.dasha.vimshottari.vimshottari_from_moon",
                                               "engine.dasha.vimshottari.vimshottari_from_snapshot"})
    assert analysis["rows"]["engine.models.dasha.DashaPeriod.lord"]["status"] in c4.UNCOVERED


@pytest.mark.parametrize("item,fragment", [
    ({"caller": "engine.kp.chain.kp_chain", "proof": c4._DASHA_PROOF}, "stale receiver evidence"),
    ({"caller": "engine.dasha.vimshottari._subdivide",
      "proof": "engine/tests/test_stage_b_coverage_gates.py::test_invented"}, "no committed proof"),
    ({"caller": "engine.dasha.vimshottari._subdivide", "proof": "engine/tests/absent.py::test_x"}, "no committed proof"),
])
def test_c4_rejects_unsupported_receiver_evidence(item, fragment, graph):
    evidence = {"engine.models.dasha.DashaPeriod.lord": item}
    resolved, errors = c4.apply_receiver_evidence(graph, evidence, ROOT)
    _expect(errors, "R6", fragment)
    assert "engine.models.dasha.DashaPeriod.lord" not in resolved.edges.get(item["caller"], set())


def test_c4_rejects_evidence_for_a_method_that_does_not_exist(graph):
    evidence = {"engine.models.dasha.DashaPeriod.invented": {"caller": "engine.dasha.vimshottari._subdivide",
                                                             "proof": c4._DASHA_PROOF}}
    _expect(c4.apply_receiver_evidence(graph, evidence, ROOT)[1], "R6", "does not exist")


# ------------------------------------------------------------------ C5

def _all_members():
    for name in c3.SCOPE_BEARING_ARTIFACTS:
        payload = json.loads((ROOT / "certification" / name).read_text(encoding="utf-8"))
        for capability in payload["capabilities"]:
            for member in capability["members"]:
                yield name, capability["id"], member


def test_c5_no_inherited_certification_is_claimed_today():
    """ADR-0107: C5 tests are added only where inheritance is claimed. None is."""

    assert [member["callable"] for _n, _c, member in _all_members() if member["disposition"] == c3.INHERITED] == []


@pytest.mark.parametrize("callable_path", ["engine.transits.events.returns", "engine.transits.events.natal_conjunctions",
                                           "engine.transits.view.transit_view"])
def test_c5_transit_delegators_claim_no_inherited_certification(callable_path):
    states = {member["disposition"] for _n, _c, member in _all_members() if member["callable"] == callable_path}
    assert states == {"OPEN_SCOPE_OVERCLAIM"}


def _plant_inherited(payload, **fields):
    capability = payload["capabilities"][0]
    capability["members"].append({"callable": "engine.transits.events.returns", "kind": "callable",
                                  "disposition": c3.INHERITED, "exercised_by": [], **fields})


def test_c5_rejects_inheritance_with_no_committed_test(corpus, graph):
    _edit(corpus[0], D45, lambda p: _plant_inherited(p, delegate="engine.transits.crossing.find_crossings"))
    _expect(_c3_errors(corpus, graph), "S9", "no committed neutrality test")


def test_c5_rejects_inheritance_naming_a_test_that_does_not_exist(corpus, graph):
    _edit(corpus[0], D45, lambda p: _plant_inherited(
        p, delegate="engine.transits.crossing.find_crossings",
        neutrality_test="engine/tests/test_stage_b_coverage_gates.py::test_invented"))
    _expect(_c3_errors(corpus, graph), "S9", "does not exist")


def test_c5_rejects_inheritance_with_no_delegate(corpus, graph):
    _edit(corpus[0], D45, lambda p: _plant_inherited(
        p, neutrality_test="engine/tests/test_stage_b_coverage_gates.py::test_c5_rejects_inheritance_with_no_delegate"))
    _expect(_c3_errors(corpus, graph), "S9", "no delegate")


def test_c5_accepts_inheritance_with_a_delegate_and_a_real_test(corpus, graph):
    _edit(corpus[0], D45, lambda p: _plant_inherited(
        p, delegate="engine.transits.crossing.find_crossings",
        neutrality_test="engine/tests/test_stage_b_coverage_gates.py::test_c5_accepts_inheritance_with_a_delegate_and_a_real_test"))
    assert [error for error in _c3_errors(corpus, graph) if error.startswith("S9")] == []
