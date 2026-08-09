"""
KP_CHAIN_V1 certification artifact gate (collected by default pytest).

The archived JSON is never accepted as proof (project rule); this test
verifies the artifact exists, claims PASS, and that its headline
claims REPRODUCE on a fast sample in the current tree. The full
regeneration is scripts/certify_kp_chain.py.
"""

import json
from fractions import Fraction
from pathlib import Path

from engine.kp.chain import kp_chain

from legacy import kp as legacy_kp

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "certification" / "KP_CHAIN_V1_certification.json"


def test_artifact_exists_and_claims_pass():
    assert ARTIFACT.exists(), "run scripts/certify_kp_chain.py"
    report = json.loads(ARTIFACT.read_text())
    assert report["schema"] == "kp_chain_v1_certification"
    assert report["adr"] == "ADR-0006"
    assert report["result"] == "PASS"
    gates = report["gates"]
    assert gates["A_legacy_oracle_equivalence"]["mismatches"] == 0
    assert gates["A_legacy_oracle_equivalence"]["dense_points"] == 51429
    assert gates["B_holdout_chart_equivalence"]["chain_mismatches"] == 0
    assert gates["B_holdout_chart_equivalence"]["cases"] == 11
    assert gates["C_fixture_structural_200"] == {"fields": 200, "mismatches": 0}
    assert gates["D_independent_validator"] == {"result": "PASS"}
    assert "significators (Tier-1 KP_SIGNIFICATOR_V1; spec must be frozen first, D-008)" in report["explicit_non_claims"]


def test_headline_claims_reproduce_on_sample():
    step = 360.0 / 997
    for i in range(997):
        lon = i * step
        ours = kp_chain(lon)
        theirs = legacy_kp.chain(lon)
        assert (
            ours.sign_lord, ours.nakshatra_lord, ours.sub_lord, ours.sub_sub_lord,
        ) == (theirs["SL"], theirs["NL"], theirs["SB"], theirs["SS"])

    chain = kp_chain(Fraction(280))
    assert (chain.sign_lord, chain.nakshatra_lord, chain.sub_lord, chain.sub_sub_lord) == (
        "Sa", "Mo", "Mo", "Mo",
    )
