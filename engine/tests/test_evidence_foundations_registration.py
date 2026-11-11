"""EVIDENCE_FOUNDATIONS_V1's registration under C2, C3 and C4 (ADR-0115 s4; AC14).

Each control plants a misregistration and requires the real enforcement path to reject it for the
stated reason. Mutations go to temporary copies or in-memory text; committed files are not modified.
"""

from __future__ import annotations

import json
import shutil
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

ARTIFACT = "EVIDENCE_FOUNDATIONS_V1"
FILE = f"{ARTIFACT}_certification.json"
BACKLOG = ROOT / "docs" / "CERTIFICATION_REMEDIATION_BACKLOG.json"
STRUCTURE_LINE = f'"certified_evidence_structure_not_calculation": ["{ARTIFACT}"]'


def _status_text() -> str:
    return (ROOT / "docs" / "ENGINE_STATUS.md").read_text(encoding="utf-8")


def _expect(errors: list[str], code: str, fragment: str = "") -> None:
    assert any(error.startswith(code) and fragment in error for error in errors), errors[:8]


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


# ------------------------------------------------------------------ C2: its own list, never a calculation

def test_c2_registers_it_as_evidence_structure_only():
    block, _ = c2.extract_block(_status_text())
    assert block["certified_evidence_structure_not_calculation"] == [ARTIFACT]
    for key in ("declared_production_analytical_inputs", "certified_capabilities", "certified_support_not_declared"):
        assert ARTIFACT not in block[key], key
    assert c2.EVIDENCE_STRUCTURE == frozenset({ARTIFACT}) and not c2.EVIDENCE_STRUCTURE & c2.NON_DECLARING_SUPPORT
    assert c2.check(_status_text()) == []


@pytest.mark.parametrize("planted", [
    '"certified_evidence_structure_not_calculation": []',
    f'"certified_evidence_structure_not_calculation": ["{ARTIFACT}", "TRANSIT_V1"]',
    '"certified_evidence_structure_not_calculation": ["TRANSIT_V1"]',
])
def test_c2_rejects_an_edit_of_the_structure_list(planted):
    text = _status_text()
    assert STRUCTURE_LINE in text
    _expect(c2.check(text.replace(STRUCTURE_LINE, planted)), "F19")


def test_c2_rejects_a_missing_structure_list():
    text = _status_text().replace(STRUCTURE_LINE + ",\n", "", 1)
    assert STRUCTURE_LINE not in text
    _expect(c2.check(text), "F19")


def test_c2_rejects_classifying_it_as_astrological_calculation():
    text = _status_text()
    planted = text.replace('"certified_capabilities": [\n', f'"certified_capabilities": [\n    "{ARTIFACT}",\n', 1)
    assert planted != text
    _expect(c2.check(planted), "F19", "not astrological calculation")


def test_c2_rejects_classifying_it_as_certified_support():
    text = _status_text()
    planted = text.replace('"certified_support_not_declared": ["SUPPORT_PATHS_V1"]',
                           f'"certified_support_not_declared": ["SUPPORT_PATHS_V1", "{ARTIFACT}"]', 1)
    assert planted != text
    errors = c2.check(planted)
    _expect(errors, "F18")
    _expect(errors, "F19", "support list")


# ------------------------------------------------------------------ C3: scope-bearing, with its own declarations

def test_c3_reads_it_with_its_own_certifier():
    assert FILE in c3.SCOPE_BEARING_ARTIFACTS and c3.CERTIFIERS[FILE] == "certify_evidence_foundations.py"
    capabilities = [capability["id"] for capability in declarations.ARTIFACT_DECLARATIONS[FILE]["capabilities"]]
    assert capabilities == ["evidence.entity_foundations", "evidence.event_records", "evidence.event_class_seed",
                            "evidence.historical_ledger",  # added by ADR-0116 s4 (WP-E3)
                            "evidence.evidence_model"]  # added by ADR-0119 s3 (WP-E4)


def test_c3_rejects_a_withdrawn_enumeration(corpus, graph):
    path = corpus[0] / FILE
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload.pop("capabilities")
    path.write_text(json.dumps(payload), encoding="utf-8")
    _expect(c3.check(corpus[0], corpus[1], ROOT, graph)[0], "S1", FILE)


def test_c3_rejects_a_missing_artifact(corpus, graph):
    (corpus[0] / FILE).unlink()
    _expect(c3.check(corpus[0], corpus[1], ROOT, graph)[0], "S1", FILE)


def test_c3_rejects_a_member_its_gate_does_not_reach(corpus, graph):
    path = corpus[0] / FILE
    payload = json.loads(path.read_text(encoding="utf-8"))
    events = next(capability for capability in payload["capabilities"] if capability["id"] == "evidence.event_records")
    events["members"][0]["exercised_by"] = ["E_event_class_registry"]
    payload["gates"]["E_event_class_registry"]["exercises"].append("evidence.event_records")
    path.write_text(json.dumps(payload), encoding="utf-8")
    _expect(c3.check(corpus[0], corpus[1], ROOT, graph)[0], "S10", "EventRecordId.from_number")


# ------------------------------------------------------------------ C4: its members are coverage

def test_c4_counts_it_as_coverage(corpus):
    """Withdraw it, and the event model's in-use functions are uncovered and untracked: R1 must fire."""

    directory, backlog = corpus
    (directory / FILE).unlink()
    errors, _report = c4.check(certification_dir=directory, backlog_path=backlog)
    _expect(errors, "R1", "engine.evidence.event")


def test_c4_it_alone_covers_the_h0_foundations(corpus):
    """SUPPORT_PATHS_V1 is kept (ADR-0115 s4); this shows the replacement's H0 coverage without it."""

    directory, backlog = corpus
    (directory / "SUPPORT_PATHS_V1_certification.json").unlink()
    errors, _report = c4.check(certification_dir=directory, backlog_path=backlog)
    assert errors and not [error for error in errors if "engine.evidence." in error], errors[:8]
