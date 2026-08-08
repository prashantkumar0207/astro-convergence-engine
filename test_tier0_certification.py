"""Certification threshold tests for the LEGACY certified kernel.

These are MANDATORY when run: a missing report or missing
package-relative artifact is a FAIL, never a skip
(correction-iteration requirement 10).

Remediation notes (audit F-07/F-17):
- ROOT previously resolved to the PARENT of the repository
  (parents[1] from a root-level file); fixed to the repository
  root itself.
- The certified kernel now lives in legacy/ (the historical
  `astro_kernel` package name); the ephemeris files live at the
  repository root. Paths updated to where the artifacts actually
  are, so this gate is runnable again:
      python -m pytest test_tier0_certification.py
- This file certifies the LEGACY kernel and its archived reports.
  The CURRENT engine's certification gate is the default pytest
  suite (engine/tests), including test_reference_astronomy.py and
  test_ephemeris.py. See CURRENT_ENGINE_CERTIFICATION_STATUS.md.
"""
import json, os, sys
from pathlib import Path
import pytest
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
REP = ROOT / "reports" / "tier0_certification.json"

def test_certification_report_exists_from_this_run():
    assert REP.exists(), "reports/tier0_certification.json absent - mandatory FAIL"

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
    for f in ("sepl_18.se1", "semo_18.se1", "CHECKSUMS.sha256"):
        assert (ROOT / f).exists(), f"missing {f} - mandatory FAIL"
    from legacy import engine
    ch = engine.compute("1985-12-21", "14:40:00", 25.6, 85.1333, ephe="SWIEPH",
                        ephe_path=str(ROOT), strict_ephe=True)
    assert ch["profile"]["actual_ephemeris_modes"] == ["SWIEPH"]
    # An empty ephemeris directory forces the Moshier fallback,
    # which strict mode must block. (ephe_path=None was previously
    # used here, but swisseph's default search can find the files
    # in the working directory, making that variant environment
    # dependent.)
    import tempfile
    with tempfile.TemporaryDirectory() as empty:
        with pytest.raises(RuntimeError):
            engine.compute("1985-12-21", "14:40:00", 25.6, 85.1333, ephe="SWIEPH",
                           ephe_path=empty, strict_ephe=True)

def test_brihat_categorical_regression_from_fresh_run():
    # The archived report lives at the repository root in this
    # layout (reports/ holds the other certification artifacts).
    rep = ROOT / "regression_report.json"
    if not rep.exists():
        rep = ROOT / "reports" / "regression_report.json"
    assert rep.exists(), "regression_report.json absent - mandatory FAIL"
    data = json.load(open(rep))
    for c in data["cases"]:
        st = c["structural_check_on_fixture_longitudes"]
        assert (st["SL"], st["NL"], st["SB"], st["SS"]) == (st["total"],) * 4, c["label"]
        assert st["boundary_flags"] == []
