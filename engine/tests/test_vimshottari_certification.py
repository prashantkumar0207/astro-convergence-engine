"""
VIMSHOTTARI_V1 certification artifact gate (collected by default pytest).

The archived JSON is never accepted as proof; this test verifies the
artifact exists, claims PASS under the pinned year convention, and
that headline behavior reproduces on a fast sample. Full regeneration
(including the PyJHora oracle comparison) is scripts/certify_vimshottari.py;
PyJHora is an oracle-only dependency and is deliberately NOT imported
here so the default gate stays oracle-free.
"""

import json
from fractions import Fraction
from pathlib import Path

from engine.dasha.vimshottari import vimshottari_from_moon

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "certification" / "VIMSHOTTARI_V1_certification.json"


def test_artifact_exists_and_claims_pass():
    assert ARTIFACT.exists(), "run scripts/certify_vimshottari.py"
    report = json.loads(ARTIFACT.read_text())
    assert report["schema"] == "vimshottari_v1_certification"
    assert report["adr"] == "ADR-0007"
    assert report["result"] == "PASS"
    assert report["year_convention"]["profile"] == "vimshottari_mean_sidereal_year"
    assert report["year_convention"]["days"] == "91314091/250000"  # 365.256364 exact
    gates = report["gates"]
    assert gates["oracle_lord_mismatches"] == 0
    # H-04 (ADR-0053): the oracle comparison now runs at pratyantar depth
    # (3), not antardasha depth (2). 2 profiles x 11 cases x 729 rows/case.
    assert gates["oracle_pratyantar_rows_compared"] == 16038
    assert gates["oracle_max_start_delta_days"] <= gates["start_tolerance_days"]
    assert gates["independent_validator"] == "PASS"
    # Oracle astronomy divergence is recorded, bounded, and does not
    # reopen Tier-0 (D-001/D-007).
    assert report["oracle"]["max_oracle_moon_delta_arcsec"] < 2.0


def test_year_convention_constant_is_exact():
    assert Fraction(365256364, 1000000) == Fraction(91314091, 250000)


def test_headline_behavior_reproduces_on_sample():
    timeline = vimshottari_from_moon(5.0, 2451545.0)
    assert timeline.seed_lord == "Ke"
    assert timeline.balance_years == Fraction(35, 8)
    assert [p.lord for p in timeline.mahadashas()] == [
        "Ke", "Ve", "Su", "Mo", "Ma", "Ra", "Ju", "Sa", "Me",
    ]
    assert timeline.mahadashas()[-1].end_years == 120
    assert len(timeline.periods) == 819
