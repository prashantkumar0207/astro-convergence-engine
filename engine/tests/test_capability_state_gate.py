"""Negative controls for the capability-state consistency gate (ADR-0093).

A gate that cannot fail is not evidence. These controls plant the exact
divergences the 2026-09-05 reconciliation audit found in the real repository -
a production-registered varga missing from the documented list, and a
non-claim contradicted by a PASS artifact - and require the gate to reject
each one.

They drive the REAL enforcement path: `check()` is the same function the CLI
calls, and the process-boundary tests invoke the actual script. Nothing here
re-implements the comparison, because a control that simulates the check
proves only that the simulation works (DP-032 Part G, Finding 2).

Mutations are applied to an in-memory or temp-file COPY. The committed
document is never modified.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts import check_capability_state as gate  # noqa: E402

DOCUMENT = ROOT / "docs" / "ENGINE_STATUS.md"
SCRIPT = ROOT / "scripts" / "check_capability_state.py"


def _text() -> str:
    return DOCUMENT.read_text()


def _block(text: str) -> dict:
    block, errors = gate.extract_block(text)
    assert block is not None, errors
    return block


def _rewrite(text: str, block: dict) -> str:
    """Put a mutated block back into the document text, delimiters intact."""

    match = gate._BLOCK.search(text)
    assert match is not None
    replacement = match.group(0).replace(
        match.group("json"), "\n" + json.dumps(block, indent=2) + "\n"
    )
    return text[: match.start()] + replacement + text[match.end() :]


# ---------------------------------------------------------------------------
# Baseline: the real document, against real live state.
# ---------------------------------------------------------------------------


def test_real_document_passes_against_live_state():
    assert gate.check(_text()) == []


def test_cli_exits_zero_on_the_real_document():
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(DOCUMENT)], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stdout + result.stderr


# ---------------------------------------------------------------------------
# Control 1: a production-registered varga removed from the documented block.
# ---------------------------------------------------------------------------


def test_control_removing_d40_is_rejected():
    text = _text()
    block = _block(text)
    assert 40 in block["production_registered_vargas"], "precondition: D40 documented"

    block["production_registered_vargas"] = [
        d for d in block["production_registered_vargas"] if d != 40
    ]
    errors = gate.check(_rewrite(text, block))

    assert errors, "removing a registered varga was NOT rejected"
    assert any(e.startswith("F1") and "D40" in e for e in errors), errors


def test_control_removing_d40_fails_through_the_process_boundary(tmp_path):
    text = _text()
    block = _block(text)
    block["production_registered_vargas"] = [
        d for d in block["production_registered_vargas"] if d != 40
    ]
    target = tmp_path / "ENGINE_STATUS.md"
    target.write_text(_rewrite(text, block))

    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(target)], capture_output=True, text=True
    )
    assert result.returncode != 0, "the gate exited zero on a mutated document"
    assert "F1" in result.stdout and "D40" in result.stdout, result.stdout


# ---------------------------------------------------------------------------
# Control 2: a false "no yogas" non-claim, while PARASHARI_YOGA_V1 is PASS.
# This is the exact defect ADR-0093 corrected in ENGINE_STATUS.md and README.md.
# ---------------------------------------------------------------------------


def test_precondition_parashari_yoga_is_actually_passing():
    """The control below proves nothing unless this really is PASS."""

    artifacts, _ = gate.live_pass_artifacts()
    assert artifacts.get("PARASHARI_YOGA_V1") == "PASS"


def test_control_false_no_yogas_non_claim_is_rejected():
    text = _text()
    block = _block(text)
    assert "yogas" not in block["non_claims"], "precondition: not currently claimed"

    block["non_claims"] = block["non_claims"] + ["yogas"]
    errors = gate.check(_rewrite(text, block))

    assert errors, "a non-claim contradicted by a PASS artifact was NOT rejected"
    assert any(
        e.startswith("F3") and "PARASHARI_YOGA_V1" in e for e in errors
    ), errors


def test_control_false_no_yogas_fails_through_the_process_boundary(tmp_path):
    text = _text()
    block = _block(text)
    block["non_claims"] = block["non_claims"] + ["yogas"]
    target = tmp_path / "ENGINE_STATUS.md"
    target.write_text(_rewrite(text, block))

    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(target)], capture_output=True, text=True
    )
    assert result.returncode != 0, "the gate exited zero on a false non-claim"
    assert "F3" in result.stdout, result.stdout


# ---------------------------------------------------------------------------
# Control 3: restoration. Both mutations reverted, the gate passes again.
# ---------------------------------------------------------------------------


def test_control_restored_document_passes_again(tmp_path):
    text = _text()
    block = _block(text)

    mutated = dict(block)
    mutated["production_registered_vargas"] = [
        d for d in block["production_registered_vargas"] if d != 40
    ]
    mutated["non_claims"] = block["non_claims"] + ["yogas"]
    assert gate.check(_rewrite(text, mutated)), "mutations must fail before restoring"

    target = tmp_path / "ENGINE_STATUS.md"
    target.write_text(_rewrite(text, block))
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(target)], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert gate.check(_text()) == [], "the committed document must be untouched"


# ---------------------------------------------------------------------------
# The remaining failure conditions, each shown reachable.
# ---------------------------------------------------------------------------


def test_control_claiming_an_unregistered_division_is_rejected():
    text = _text()
    block = _block(text)
    block["production_registered_vargas"] = block["production_registered_vargas"] + [16]
    errors = gate.check(_rewrite(text, block))
    assert any(e.startswith("F2") and "D16" in e for e in errors), errors


def test_control_listing_a_certified_varga_as_not_certified_is_rejected():
    text = _text()
    block = _block(text)
    block["not_certified_vargas"] = block["not_certified_vargas"] + [45]
    errors = gate.check(_rewrite(text, block))
    assert any(e.startswith("F4") and "D45" in e for e in errors), errors


def test_control_wrong_source_count_is_rejected():
    text = _text()
    block = _block(text)
    block["counts"]["certifier_sources"] = block["counts"]["certifier_sources"] + 1
    errors = gate.check(_rewrite(text, block))
    assert any(e.startswith("F5") and "certifier_sources" in e for e in errors), errors


def test_control_omitting_a_passing_capability_is_rejected():
    """Completeness: a document must not pass by simply staying silent."""

    text = _text()
    block = _block(text)
    block["certified_capabilities"] = [
        c for c in block["certified_capabilities"] if c != "KP_SIGNIFICATOR_V1"
    ]
    errors = gate.check(_rewrite(text, block))
    assert any(e.startswith("F6") and "KP_SIGNIFICATOR_V1" in e for e in errors), errors


def test_control_claiming_an_uncertified_capability_is_rejected():
    text = _text()
    block = _block(text)
    block["certified_capabilities"] = block["certified_capabilities"] + ["SHADBALA_V1"]
    errors = gate.check(_rewrite(text, block))
    assert any(e.startswith("F7") and "SHADBALA_V1" in e for e in errors), errors


def test_control_misstating_the_certified_not_registered_distinction_is_rejected():
    """D16/D4 are certified but NOT registered. Both halves are enforced."""

    text = _text()
    block = _block(text)
    block["certified_not_registered_vargas"] = block[
        "certified_not_registered_vargas"
    ] + [45]
    errors = gate.check(_rewrite(text, block))
    assert any(e.startswith("F8") and "D45" in e for e in errors), errors


def test_control_deleted_block_is_rejected():
    """A gate that passes when its input has been deleted is not a gate."""

    errors = gate.check("# Engine status\n\nno block here\n")
    assert errors
    assert any("no CAPABILITY-BLOCK found" in e for e in errors), errors


# ---------------------------------------------------------------------------
# ADR-0092: the frozen inventory must never become a live source of truth.
# ---------------------------------------------------------------------------


def test_frozen_evidence_is_excluded_from_live_sources():
    artifacts, _ = gate.live_pass_artifacts()
    assert "ENGINE_CAPABILITY_INVENTORY.json" in gate.FROZEN_EVIDENCE
    assert "ENGINE_CAPABILITY_INVENTORY" not in artifacts


def test_frozen_inventory_cannot_influence_the_verdict(tmp_path):
    """Even a corrupted inventory must not change the gate's answer."""

    real = ROOT / "certification"
    staged = tmp_path / "certification"
    staged.mkdir()
    for path in real.glob("*.json"):
        (staged / path.name).write_bytes(path.read_bytes())

    (staged / "ENGINE_CAPABILITY_INVENTORY.json").write_text(
        json.dumps({"result": "PASS", "capabilities": {"nonsense": True}})
    )

    assert gate.live_pass_artifacts(staged) == gate.live_pass_artifacts(real)


@pytest.mark.parametrize("name", sorted(gate.FROZEN_EVIDENCE))
def test_every_frozen_file_is_really_dated_evidence(name):
    """Guards the exclusion list itself: these must not be runner-regenerated."""

    path = ROOT / "certification" / name
    if not path.is_file():
        pytest.skip(f"{name} not present")
    payload = json.loads(path.read_text())
    assert "date" in payload, f"{name} carries no date; is it really frozen evidence?"


# ---------------------------------------------------------------------------
# D-1: the Tier-0 artifact must be inside the completeness universe, and no
# non-frozen artifact may ever again be skipped for an unrecognised schema.
# ---------------------------------------------------------------------------


def test_tier0_current_engine_is_in_the_live_universe():
    """It records its verdict at summary.result, not at top level. Missing that
    is what silently excluded the repository's most foundational certification."""

    artifacts, errors = gate.live_pass_artifacts()
    assert errors == []
    assert artifacts.get("current_engine") == "PASS"


def test_tier0_is_not_classified_as_frozen_evidence():
    """It is runner-regenerated: registered in CERTIFIER_SOURCES and run in CI."""

    from scripts.certification_support import CERTIFIER_SOURCES

    assert "current_engine_certification.json" not in gate.FROZEN_EVIDENCE
    assert "scripts/certify_current_engine.py" in CERTIFIER_SOURCES


def test_control_omitting_tier0_from_the_block_is_rejected():
    text = _text()
    block = _block(text)
    block["certified_capabilities"] = [
        c for c in block["certified_capabilities"] if c != "current_engine"
    ]
    errors = gate.check(_rewrite(text, block))
    assert any(e.startswith("F6") and "current_engine" in e for e in errors), errors


def test_control_artifact_with_no_locatable_verdict_is_rejected(tmp_path):
    """A non-frozen artifact whose verdict cannot be found must fail loudly,
    not be skipped. Silent skipping is precisely how D-1 stayed hidden."""

    staged = tmp_path / "certification"
    staged.mkdir()
    for path in (ROOT / "certification").glob("*.json"):
        (staged / path.name).write_bytes(path.read_bytes())
    (staged / "MYSTERY_V1_certification.json").write_text(json.dumps({"schema": "x"}))

    artifacts, errors = gate.live_pass_artifacts(staged)
    assert "MYSTERY_V1" not in artifacts
    assert any(e.startswith("F9") and "MYSTERY_V1" in e for e in errors), errors


# ---------------------------------------------------------------------------
# D-2: required keys. Omitting a key must fail, never silently disable a check.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("key", sorted(gate.REQUIRED_KEYS))
def test_control_dropping_any_required_key_is_rejected(key):
    text = _text()
    block = _block(text)
    del block[key]
    errors = gate.check(_rewrite(text, block))
    assert any(e.startswith("F10") and key in e for e in errors), (key, errors)


@pytest.mark.parametrize("key", sorted(gate.REQUIRED_COUNTS))
def test_control_dropping_any_required_count_is_rejected(key):
    text = _text()
    block = _block(text)
    del block["counts"][key]
    errors = gate.check(_rewrite(text, block))
    assert any(e.startswith("F10") and key in e for e in errors), (key, errors)


def test_control_emptied_counts_no_longer_passes():
    """The exact D-2 bypass: counts = {} previously returned PASS."""

    text = _text()
    block = _block(text)
    block["counts"] = {}
    errors = gate.check(_rewrite(text, block))
    assert errors, "an emptied counts block was NOT rejected"


# ---------------------------------------------------------------------------
# D-3: non-claim vocabulary. An unknown or misspelled token must fail.
# ---------------------------------------------------------------------------


def test_control_misspelled_non_claim_is_rejected():
    """The exact D-3 bypass: 'kp_significator' (singular) silently exempted the
    line from F3, because only 'kp_significators' is mapped."""

    text = _text()
    block = _block(text)
    block["non_claims"] = block["non_claims"] + ["kp_significator"]
    errors = gate.check(_rewrite(text, block))
    assert any(e.startswith("F11") and "kp_significator" in e for e in errors), errors


def test_control_invented_non_claim_token_is_rejected():
    text = _text()
    block = _block(text)
    block["non_claims"] = block["non_claims"] + ["tier0", "astronomical_kernel"]
    errors = gate.check(_rewrite(text, block))
    assert sum(e.startswith("F11") for e in errors) == 2, errors


def test_known_vocabulary_covers_every_token_actually_in_use():
    """The committed block must not depend on tokens the gate cannot classify."""

    block = _block(_text())
    unknown = [t for t in block["non_claims"] if t not in gate.KNOWN_NON_CLAIMS]
    assert unknown == [], unknown


def test_refutable_and_unrefutable_vocabularies_are_disjoint():
    """A token must be one or the other, or F3's meaning becomes ambiguous."""

    assert not (set(gate.NON_CLAIM_ARTIFACTS) & gate.UNREFUTABLE_NON_CLAIMS)
