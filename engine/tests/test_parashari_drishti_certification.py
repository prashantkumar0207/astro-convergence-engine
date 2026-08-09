"""
PARASHARI_DRISHTI_V1 certification artifact gate (collected by
default pytest). PyJHora stays oracle-only; not imported here.
"""

import json
from pathlib import Path

from engine.parashari.drishti import aspected_signs

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "certification" / "PARASHARI_DRISHTI_V1_certification.json"


def test_artifact_exists_and_claims_pass():
    assert ARTIFACT.exists(), "run scripts/certify_parashari_drishti.py"
    report = json.loads(ARTIFACT.read_text())
    assert report["schema"] == "parashari_drishti_v1_certification"
    assert report["adr"] == "ADR-0012"
    assert report["result"] == "PASS"
    gates = report["gates"]
    assert gates["A_table_integrity"] == {"planets": 7, "mismatches": 0}
    assert gates["B_combinatorial_12x12"] == {"planet_sign_pairs": 84, "mismatches": 0}
    assert gates["C_oracle"]["mismatches"] == 0
    assert gates["C_oracle"]["cases"] == 11
    assert "node" in gates["C_oracle"]["node_divergence_note"]
    assert gates["D_independent_validator"] == {"result": "PASS"}
    assert "node-cast aspects (recorded variant)" in report["explicit_non_claims"]


def test_headline_behavior_reproduces_on_sample():
    # Saturn in Scorpio (8): 3rd Capricorn (10), 7th Taurus (2), 10th Leo (5).
    assert aspected_signs("Saturn", 8) == (10, 2, 5)
    # Jupiter in Capricorn (10): 5th Taurus (2), 7th Cancer (4), 9th Virgo (6).
    assert aspected_signs("Jupiter", 10) == (2, 4, 6)
    # Sun anywhere casts exactly the 7th.
    assert aspected_signs("Sun", 1) == (7,)
