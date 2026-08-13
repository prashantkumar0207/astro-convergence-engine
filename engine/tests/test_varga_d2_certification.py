"""
VARGA_D2_V1 certification artifact gate (collected by default pytest).

Added by ADR-0014. Before it, only D3 and D12 pinned their certification
artifact, so the batch-registered vargas (D2, D7, D30) had no gate asserting
that their artifact still claims PASS or still cites the correct decision
entry. That asymmetry is what allowed the retired provisional identifiers to
survive in these artifacts unnoticed.

PyJHora stays oracle-only; not imported here.
"""

import json
from pathlib import Path

from engine.astrology.varga_classifier import classify
from engine.astrology.varga_d2 import D2_PARASHARA

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "certification" / "VARGA_D2_V1_certification.json"


def test_artifact_exists_and_claims_pass():
    assert ARTIFACT.exists(), "run scripts/certify_d2.py"
    report = json.loads(ARTIFACT.read_text())
    assert report["schema"] == "varga_d2_v1_certification"
    assert report["adr"] == "ADR-0011"
    assert report["supersedes_provisional_id"] == "ADR-VARGA-D2-001"
    assert report["result"] == "PASS"
    gates = report["gates"]
    assert gates["A_table_integrity"] == {"cells": 24, "mismatches": 0}
    assert gates["B_dense_sweep"] == {"points": 51429, "mismatches": 0}
    assert gates["C_oracle"]["mismatches"] == 0
    assert [2, "parashara"] in gates["D_non_invasiveness"]["registry"]
    assert not any(entry[0] in (1, 9, 10) for entry in gates["D_non_invasiveness"]["registry"])
    assert len(gates["D_non_invasiveness"]["d9_sweep_sha256"]) == 64
    assert gates["E_independent_validator"] == {"result": "PASS"}


def test_headline_behavior_reproduces_on_sample():
    # Hora: odd sign first half -> Leo, second half -> Cancer; even sign reversed.
    assert (lambda r: (r.d_sign, r.division_number))(classify(5.0, D2_PARASHARA)) == (4, 1)
    assert (lambda r: (r.d_sign, r.division_number))(classify(20.0, D2_PARASHARA)) == (3, 2)
    assert (lambda r: (r.d_sign, r.division_number))(classify(35.0, D2_PARASHARA)) == (3, 1)
    assert (lambda r: (r.d_sign, r.division_number))(classify(50.0, D2_PARASHARA)) == (4, 2)


def test_output_space_is_exactly_two_signs():
    # The deliberately two-sign output space (ADR-0011) is behaviour, not an
    # accident, so it is pinned rather than left implicit.
    observed = {classify(i * 360.0 / 3000.0, D2_PARASHARA).d_sign for i in range(3000)}
    assert observed == {3, 4}
