"""Certification threshold tests. These are MANDATORY: a missing report or missing
package-relative artifact is a FAIL, never a skip (correction-iteration requirement 10)."""
import json, os, sys
from pathlib import Path
import pytest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
REP = ROOT / "reports" / "tier0_certification.json"

def test_certification_report_exists_from_this_run():
    assert REP.exists(), "reports/tier0_certification.json absent - run ./run_all.sh (certify step must precede pytest)"

def test_tier0_thresholds():
    assert REP.exists(), "certification JSON missing - mandatory FAIL"
    s = json.load(open(REP))["summary"]
    assert s["max_planetary_error_arcsec"] <= 0.5
    assert s["max_ascendant_error_arcsec"] <= 0.5
    assert s["max_cusp_error_arcsec"] <= 0.5
    assert all(v == 0 for v in s["hierarchy_mismatches"].values())
    assert s["moshier_fallback_events"] == 0
    assert s["hardcoded_fitting_findings"] == []

def test_ephemeris_bundle_present_and_strict_mode_blocks_fallback():
    ephe = ROOT / "ephe"
    assert ephe.is_dir(), "package-relative ephe/ absent - mandatory FAIL"
    for f in ("sepl_18.se1", "semo_18.se1", "CHECKSUMS.sha256"):
        assert (ephe / f).exists(), f"missing {f} - mandatory FAIL"
    from astro_kernel import engine
    ch = engine.compute("1985-12-21", "14:40:00", 25.6, 85.1333, ephe="SWIEPH",
                        ephe_path=str(ephe), strict_ephe=True)
    assert ch["profile"]["actual_ephemeris_modes"] == ["SWIEPH"]
    with pytest.raises(RuntimeError):
        engine.compute("1985-12-21", "14:40:00", 25.6, 85.1333, ephe="SWIEPH",
                       ephe_path=None, strict_ephe=True)

def test_brihat_categorical_regression_from_fresh_run():
    rep = ROOT / "reports" / "regression_report.json"
    assert rep.exists(), "regression_report.json absent - run ./run_all.sh - mandatory FAIL"
    data = json.load(open(rep))
    for c in data["cases"]:
        st = c["structural_check_on_fixture_longitudes"]
        assert (st["SL"], st["NL"], st["SB"], st["SS"]) == (st["total"],) * 4, c["label"]
        assert st["boundary_flags"] == []
