"""
VARGA_D12_V1 certification artifact gate (collected by default pytest).
PyJHora stays oracle-only; not imported here.
"""

import json
from pathlib import Path

from engine.astrology.varga_classifier import classify
from engine.astrology.varga_d12 import D12_PARASHARA

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "certification" / "VARGA_D12_V1_certification.json"


def test_artifact_exists_and_claims_pass():
    assert ARTIFACT.exists(), "run scripts/certify_d12.py"
    report = json.loads(ARTIFACT.read_text())
    assert report["schema"] == "varga_d12_v1_certification"
    assert report["adr"] == "ADR-0010"
    assert report["supersedes_provisional_id"] == "ADR-VARGA-D12-001"
    assert report["result"] == "PASS"
    gates = report["gates"]
    assert gates["A_table_integrity"] == {"cells": 24, "mismatches": 0}
    assert gates["B_dense_sweep"] == {"points": 51429, "mismatches": 0}
    assert gates["C_oracle"]["mismatches"] == 0
    assert [12, "parashara"] in gates["D_non_invasiveness"]["registry"]
    assert not any(entry[0] in (1, 9, 10) for entry in gates["D_non_invasiveness"]["registry"])
    assert len(gates["D_non_invasiveness"]["d9_sweep_sha256"]) == 64
    assert gates["E_independent_validator"] == {"result": "PASS"}


def test_headline_behavior_reproduces_on_sample():
    # 13.4 deg Aries: 6th dwadasamsa -> Virgo (5), matching the oracle.
    result = classify(13.4, D12_PARASHARA)
    assert (result.d_sign, result.division_number) == (5, 6)
    # 27 deg Scorpio (source 7): 11th dwadasamsa -> Virgo (5).
    result = classify(7 * 30.0 + 27.0, D12_PARASHARA)
    assert (result.d_sign, result.division_number) == (5, 11)
