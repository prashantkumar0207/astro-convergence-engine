"""
VARGA_D30_V1 certification artifact gate (collected by default pytest).

Added by ADR-0014; see test_varga_d2_certification.py for why the batch
vargas previously had no artifact gate.

PyJHora stays oracle-only; not imported here.
"""

import json
from pathlib import Path

from engine.astrology.varga_classifier import classify
from engine.astrology.varga_d30 import D30_PARASHARA

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "certification" / "VARGA_D30_V1_certification.json"


def test_artifact_exists_and_claims_pass():
    assert ARTIFACT.exists(), "run scripts/certify_d30.py"
    report = json.loads(ARTIFACT.read_text())
    assert report["schema"] == "varga_d30_v1_certification"
    assert report["adr"] == "ADR-0011"
    assert report["supersedes_provisional_id"] == "ADR-VARGA-D30-001"
    assert report["result"] == "PASS"
    gates = report["gates"]
    assert gates["A_table_integrity"] == {"cells": 120, "mismatches": 0}
    assert gates["B_dense_sweep"] == {"points": 51429, "mismatches": 0}
    assert gates["C_oracle"]["mismatches"] == 0
    assert [30, "parashara"] in gates["D_non_invasiveness"]["registry"]
    assert not any(entry[0] in (1, 9, 10) for entry in gates["D_non_invasiveness"]["registry"])
    assert len(gates["D_non_invasiveness"]["d9_sweep_sha256"]) == 64
    assert gates["E_independent_validator"] == {"result": "PASS"}


def test_headline_behavior_reproduces_on_sample():
    # Trimsamsa: unequal tara-graha segments 5/5/8/7/5, reversed for even signs.
    for lon, expected in (
        (2.0, (0, 1)), (8.0, (10, 2)), (15.0, (8, 3)), (20.0, (2, 4)), (25.0, (6, 5)),
        (32.0, (1, 1)), (38.0, (5, 2)), (45.0, (11, 3)), (50.0, (9, 4)), (55.0, (7, 5)),
    ):
        result = classify(lon, D30_PARASHARA)
        assert (result.d_sign, result.division_number) == expected, lon


def test_luminary_signs_are_never_produced():
    # The five segments are ruled by the tara grahas (Mars, Saturn, Jupiter,
    # Mercury, Venus), so Cancer and Leo cannot appear. This is a defining
    # property of the rule, not an incidental one, so it is pinned.
    observed = {classify(i * 360.0 / 20000.0, D30_PARASHARA).d_sign for i in range(20000)}
    assert 3 not in observed and 4 not in observed
    assert observed == {0, 1, 2, 5, 6, 7, 8, 9, 10, 11}
