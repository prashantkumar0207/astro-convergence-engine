"""Current-engine certification gate.

Asserts the archived holdout certification results
(certification/current_engine_certification.json, produced by
scripts/certify_current_engine.py against the independent swetest
binary) meet the frozen thresholds. A missing or failing archive is a
FAIL, never a skip.

To regenerate the archive from scratch:
    python scripts/certify_current_engine.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "certification" / "current_engine_certification.json"

TOLERANCE_ARCSEC = 0.5


def _load():
    assert REPORT.exists(), (
        "certification/current_engine_certification.json absent - run "
        "scripts/certify_current_engine.py - mandatory FAIL"
    )
    return json.load(open(REPORT))


def test_certification_result_is_pass():
    report = _load()

    assert report["summary"]["result"] == "PASS"
    assert report["summary"]["failures"] == []


def test_certification_thresholds():
    s = _load()["summary"]

    assert s["max_planet_error_arcsec"] <= TOLERANCE_ARCSEC
    assert s["max_ascendant_error_arcsec"] <= TOLERANCE_ARCSEC
    assert s["max_cusp_error_arcsec"] <= TOLERANCE_ARCSEC
    assert s["moshier_fallback_events"] == 0


def test_certification_covers_both_profiles_and_all_cases():
    report = _load()

    assert set(report["profiles"]) == {
        "parashari_lahiri",
        "kp_krishnamurti",
    }

    for profile in report["profiles"].values():
        assert len(profile["cases"]) == 11
        # 12 bodies (11 + Ketu) and 12 cusps per case.
        assert profile["planet_comparisons"] == 11 * 12
        assert profile["cusp_comparisons"] == 11 * 12


def test_ayanamsa_profile_separation_verified():
    check = _load()["ayanamsa_profile_check"]

    low, high = check["expected_band_arcmin"]
    assert low < check["difference_arcmin"] < high


def test_boundary_sensitive_moon_cases_agree_with_exact_reference():
    report = _load()

    checked = 0
    for profile in report["profiles"].values():
        for case in profile["cases"]:
            if "moon_boundary_check" in case:
                assert case["moon_boundary_check"]["agrees"], case["id"]
                checked += 1

    assert checked == 4  # 2 boundary cases x 2 profiles
