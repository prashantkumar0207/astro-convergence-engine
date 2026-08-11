"""
VARGA_D7_V1 certification artifact gate (collected by default pytest).

Added by ADR-0014; see test_varga_d2_certification.py for why the batch
vargas previously had no artifact gate.

PyJHora stays oracle-only; not imported here.
"""

import json
from pathlib import Path

from engine.astrology.varga_classifier import classify
from engine.astrology.varga_d7 import D7_PARASHARA

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "certification" / "VARGA_D7_V1_certification.json"


def test_artifact_exists_and_claims_pass():
    assert ARTIFACT.exists(), "run scripts/certify_d7.py"
    report = json.loads(ARTIFACT.read_text())
    assert report["schema"] == "varga_d7_v1_certification"
    assert report["adr"] == "ADR-0011"
    assert report["supersedes_provisional_id"] == "ADR-VARGA-D7-001"
    assert report["result"] == "PASS"
    gates = report["gates"]
    assert gates["A_table_integrity"] == {"cells": 24, "mismatches": 0}
    assert gates["B_dense_sweep"] == {"points": 51429, "mismatches": 0}
    assert gates["C_oracle"]["mismatches"] == 0
    assert [7, "parashara"] in gates["D_non_invasiveness"]["registry"]
    assert not any(entry[0] in (1, 9, 10) for entry in gates["D_non_invasiveness"]["registry"])
    assert len(gates["D_non_invasiveness"]["d9_sweep_sha256"]) == 64
    assert gates["E_independent_validator"] == {"result": "PASS"}


def test_headline_behavior_reproduces_on_sample():
    # Saptamsa: odd signs count from the sign itself, even signs from the seventh.
    assert (lambda r: (r.d_sign, r.division_number))(classify(0.0, D7_PARASHARA)) == (0, 1)
    assert (lambda r: (r.d_sign, r.division_number))(classify(25.0, D7_PARASHARA)) == (5, 6)
    assert (lambda r: (r.d_sign, r.division_number))(classify(30.0, D7_PARASHARA)) == (7, 1)


def test_output_space_covers_the_whole_zodiac():
    observed = {classify(i * 360.0 / 5000.0, D7_PARASHARA).d_sign for i in range(5000)}
    assert observed == set(range(12))
