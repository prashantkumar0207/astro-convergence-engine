"""
VARGA_D3_V1 certification artifact gate (collected by default pytest).
PyJHora stays oracle-only; not imported here.
"""

import json
from pathlib import Path

from engine.astrology.varga_classifier import classify
from engine.astrology.varga_d3 import D3_PARASHARA

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "certification" / "VARGA_D3_V1_certification.json"


def test_artifact_exists_and_claims_pass():
    assert ARTIFACT.exists(), "run scripts/certify_d3.py"
    report = json.loads(ARTIFACT.read_text())
    assert report["schema"] == "varga_d3_v1_certification"
    assert report["adr"] == "ADR-VARGA-D3-001"
    assert report["result"] == "PASS"
    gates = report["gates"]
    assert gates["A_table_integrity"] == {"cells": 36, "mismatches": 0}
    assert gates["B_dense_sweep"] == {"points": 51429, "mismatches": 0}
    assert gates["C_oracle"]["mismatches"] == 0
    assert [3, "parashara"] in gates["D_non_invasiveness"]["registry"]
    assert not any(entry[0] in (1, 9, 10) for entry in gates["D_non_invasiveness"]["registry"])
    assert len(gates["D_non_invasiveness"]["d9_sweep_sha256"]) == 64
    assert gates["E_independent_validator"] == {"result": "PASS"}


def test_headline_behavior_reproduces_on_sample():
    # 15 deg Aries: second drekkana -> Leo (4).
    result = classify(15.0, D3_PARASHARA)
    assert (result.d_sign, result.division_number) == (4, 2)
    # 25 deg Scorpio (source 7): third drekkana -> Cancer (3).
    result = classify(7 * 30.0 + 25.0, D3_PARASHARA)
    assert (result.d_sign, result.division_number) == (3, 3)
