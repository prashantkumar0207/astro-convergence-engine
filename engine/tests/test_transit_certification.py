"""
TRANSIT_V1 certification artifact gate (collected by default pytest).

Verifies the artifact exists, claims PASS, and headline behavior
reproduces on a fast sample. Full regeneration (with the PyJHora
anchors) is scripts/certify_transits.py; PyJHora stays oracle-only
and is not imported here.
"""

import json
from pathlib import Path

import swisseph as swe

from engine.astronomy.profile import PARASHARI_LAHIRI
from engine.transits.crossing import RESIDUAL_BOUND_ARCSEC, find_crossings

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "certification" / "TRANSIT_V1_certification.json"


def test_artifact_exists_and_claims_pass():
    assert ARTIFACT.exists(), "run scripts/certify_transits.py"
    report = json.loads(ARTIFACT.read_text())
    assert report["schema"] == "transit_v1_certification"
    assert report["adr"] == "ADR-TRANSIT-001"
    assert report["result"] == "PASS"
    gates = report["gates"]
    assert gates["A_residual_battery"]["max_residual_arcsec"] <= RESIDUAL_BOUND_ARCSEC
    assert gates["C_oracle_anchors"]["anchors"] == 24
    assert gates["C_oracle_anchors"]["worst_delta_over_tolerance"] <= 1.0
    assert gates["D_independent_validator"] == {"result": "PASS"}
    for anchor in gates["C_oracle_anchors"]["details"]:
        assert anchor["delta_days"] <= anchor["derived_tolerance_days"]


def test_headline_behavior_reproduces_on_sample():
    jd0 = swe.julday(2024, 3, 1, 0.0, swe.GREG_CAL)
    events = find_crossings("Sun", 0.0, jd0, jd0 + 61, PARASHARI_LAHIRI)
    assert len(events) == 1
    assert events[0].residual_arcsec <= RESIDUAL_BOUND_ARCSEC
    assert events[0].direction == 1
