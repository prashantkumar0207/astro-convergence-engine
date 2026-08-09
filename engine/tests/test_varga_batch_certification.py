"""
VARGA D7/D30/D2 certification artifact gates (collected by default
pytest). PyJHora stays oracle-only; not imported here.
"""

import json
from pathlib import Path

import pytest

from engine.astrology.varga_classifier import classify
from engine.astrology.varga_d2 import D2_PARASHARA
from engine.astrology.varga_d7 import D7_PARASHARA
from engine.astrology.varga_d30 import D30_PARASHARA

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("division,cells", [(7, 24), (30, 120), (2, 24)])
def test_artifacts_exist_and_claim_pass(division, cells):
    artifact = ROOT / "certification" / f"VARGA_D{division}_V1_certification.json"
    assert artifact.exists(), f"run scripts/certify_d{division}.py"
    report = json.loads(artifact.read_text())
    assert report["schema"] == f"varga_d{division}_v1_certification"
    assert report["result"] == "PASS"
    gates = report["gates"]
    assert gates["A_table_integrity"] == {"cells": cells, "mismatches": 0}
    assert gates["B_dense_sweep"] == {"points": 51429, "mismatches": 0}
    assert gates["C_oracle"]["mismatches"] == 0
    assert [division, "parashara"] in gates["D_non_invasiveness"]["registry"]
    assert not any(entry[0] in (1, 9, 10)
                   for entry in gates["D_non_invasiveness"]["registry"])
    assert gates["E_independent_validator"] == {"result": "PASS"}


def test_headline_behavior_reproduces_on_sample():
    # D7: 20 deg Taurus (even sign, start Scorpio): division 4 -> Pisces (11).
    result = classify(30.0 + 20.0, D7_PARASHARA)
    assert (result.d_sign, result.division_number) == (11, 5)
    # D30: 12 deg Leo (odd): third segment (Jupiter) -> Sagittarius (8).
    result = classify(4 * 30.0 + 12.0, D30_PARASHARA)
    assert (result.d_sign, result.division_number) == (8, 3)
    # D30: 3 deg Virgo (even): first segment (Venus) -> Taurus (1).
    result = classify(5 * 30.0 + 3.0, D30_PARASHARA)
    assert (result.d_sign, result.division_number) == (1, 1)
    # D2: 20 deg Aries: Moon hora -> Cancer (3); 10 deg Taurus: Moon hora too.
    assert classify(20.0, D2_PARASHARA).d_sign == 3
    assert classify(40.0, D2_PARASHARA).d_sign == 3
    assert classify(10.0, D2_PARASHARA).d_sign == 4
