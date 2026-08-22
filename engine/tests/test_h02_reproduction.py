"""Tests for scripts/reproduce_h02_ingress_seam.py (DP-013 Option A).

Investigation tooling, not a certified capability - these tests protect the
reproduction's own correctness (the classifier, the comparison, the
negative control), not a production capability.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import swisseph as swe

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import reproduce_h02_ingress_seam as repro  # noqa: E402
import validate_h02_reproduction as validator  # noqa: E402

from engine.astronomy.profile import PARASHARI_LAHIRI  # noqa: E402


def test_classify_sign_matches_production_convention_at_ordinary_points():
    # Well inside a division: no boundary ambiguity possible.
    assert repro.classify_sign(15.0) == 0
    assert repro.classify_sign(45.0) == 1
    assert repro.classify_sign(359.9) == 11


def test_classify_sign_promotes_within_tolerance_and_clamps_at_the_top():
    boundary = 90.0
    assert repro.classify_sign(boundary - 1e-11) == 3  # within BOUNDARY_TOLERANCE: promotes.
    assert repro.classify_sign(boundary - 1e-8) == 2  # outside tolerance: previous division.
    assert repro.classify_sign(360.0 - 1e-11) == 11  # wraparound clamps to the top, not division 0.


def test_classify_nakshatra_boundary_convention():
    span = 360.0 / 27.0
    boundary = span * 5
    assert repro.classify_nakshatra(boundary - 1e-11) == 5
    assert repro.classify_nakshatra(boundary - 1e-8) == 4


def test_negative_control_passes():
    assert repro.negative_control() is True


def test_negative_control_pytest_level_monkeypatch(monkeypatch):
    """A second, independent demonstration (pytest's own monkeypatch, not
    the script's internal swap) that a broken classifier is caught: forces
    classify_sign to always agree with the target, then confirms
    check_event() would then report NO mismatch for a case built to
    definitely be one."""

    jd0 = swe.julday(2024, 1, 1, 0.0, swe.GREG_CAL)
    from engine.transits.events import sign_ingresses
    events = sign_ingresses("Sun", jd0, jd0 + 366, PARASHARI_LAHIRI)
    assert len(events) == 12

    real_result = repro.check_event(events[0], swe.SUN, repro.classify_sign)
    target_division = repro.classify_sign(events[0].target_longitude)

    def _always_agrees(longitude):
        return target_division  # deliberately broken: ignores the input entirely.

    monkeypatch.setattr(repro, "classify_sign", _always_agrees)
    broken_result = repro.check_event(events[0], swe.SUN, repro.classify_sign)
    assert broken_result["mismatch"] is False

    monkeypatch.undo()
    restored_result = repro.check_event(events[0], swe.SUN, repro.classify_sign)
    assert restored_result == real_result


def test_full_reproduction_matches_the_original_audit_for_sun():
    """The Sun holdout (one full 2024 calendar year, unambiguous - the Sun
    crosses each sign boundary exactly once) reproduces the original
    audit's exact figure: 2 of 12 sankranti instants misclassified."""

    report = repro.run()
    assert report["sun_sign_ingresses"]["cases"] == 12
    assert report["sun_sign_ingresses"]["mismatches"] == 2
    assert report["cross_validator"]["agrees_exactly"] is True
    assert report["negative_control_verified"] is True


def test_full_reproduction_moon_shows_a_comparable_mismatch_rate():
    """The Moon holdout window is independently chosen (this reproduction's
    own 35-day window, not the original audit's unstated exact window - see
    DP-013 s5), so an exact count match is not expected; a comparably high
    mismatch rate is the meaningful reproduction signal."""

    report = repro.run()
    moon = report["moon_nakshatra_ingresses"]
    assert moon["cases"] >= 27  # at least one full nakshatra cycle.
    assert moon["mismatch_rate"] > 0.2  # comparable order of magnitude to the audit's ~43%.


def test_validator_independently_reproduces_the_same_counts():
    result = validator._run()
    assert result["sun_cases"] == 12
    assert result["sun_mismatches"] == 2
