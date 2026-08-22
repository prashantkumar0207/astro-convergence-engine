"""
engine.astronomy.rise_set (ADR-0054).

Full oracle/independent-reference certification is
scripts/certify_rise_set.py; this suite covers unit, boundary,
property and negative-control coverage collected by the default gate.
"""

import sys
from dataclasses import replace
from pathlib import Path

import pytest
import swisseph as swe

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from engine.astronomy.ephemeris import EphemerisFallbackError
from engine.astronomy.profile import PARASHARI_LAHIRI
from engine.astronomy import rise_set as rise_set_module
from engine.astronomy.rise_set import (
    RiseSetStatus,
    UnsupportedRiseSetConventionError,
    horizon_dip_degrees,
    sunrise,
    sunset,
)


def _jd(year, month, day, hour=0.0):
    return swe.julday(year, month, day, hour)


# --- Sanity / headline behaviour --------------------------------------


def test_headline_sunrise_before_sunset_same_day_equator():
    jd = _jd(2024, 3, 20)
    r = sunrise(jd, 0.0, 0.0)
    s = sunset(jd, 0.0, 0.0)
    assert r.status == RiseSetStatus.OK
    assert s.status == RiseSetStatus.OK
    assert r.julian_day_ut < s.julian_day_ut
    # Roughly a 12-hour day at the equinox on the equator.
    assert 0.45 < (s.julian_day_ut - r.julian_day_ut) < 0.55


def test_result_event_field_matches_query():
    jd = _jd(2024, 3, 20)
    assert sunrise(jd, 0.0, 0.0).event == "rise"
    assert sunset(jd, 0.0, 0.0).event == "set"


# --- Circumpolar / NO_RISE / NO_SET -------------------------------------


def test_midnight_sun_returns_no_set_not_an_exception():
    jd = _jd(2024, 6, 21)
    result = sunset(jd, 78.2, 15.6)
    assert result.status == RiseSetStatus.NO_SET
    assert result.julian_day_ut is None


def test_polar_night_returns_no_rise():
    jd = _jd(2024, 12, 21)
    result = sunrise(jd, 78.2, 15.6)
    assert result.status == RiseSetStatus.NO_RISE
    assert result.julian_day_ut is None


def test_polar_night_also_returns_no_set():
    # Verified against the raw swisseph call before this module was
    # written: a day with no sunrise at this latitude also reports no
    # sunset (the sun never comes up in the first place).
    jd = _jd(2024, 12, 21)
    result = sunset(jd, 78.2, 15.6)
    assert result.status == RiseSetStatus.NO_SET
    assert result.julian_day_ut is None


def test_mid_latitude_ordinary_day_has_both_events():
    # Boundary-adjacent: a temperate latitude never goes circumpolar.
    jd = _jd(2024, 6, 21)
    assert sunrise(jd, 51.5, 0.0).status == RiseSetStatus.OK
    assert sunset(jd, 51.5, 0.0).status == RiseSetStatus.OK


# --- Boundary latitudes ---------------------------------------------


@pytest.mark.parametrize("latitude", [-90.0, -66.0, -23.5, 0.0, 23.5, 66.0, 90.0])
def test_extreme_and_tropic_latitudes_do_not_raise(latitude):
    # Every latitude in [-90, 90] must return a structured result
    # (OK or NO_RISE/NO_SET), never an unhandled exception, even at
    # the poles themselves.
    jd = _jd(2024, 3, 20)
    result = sunrise(jd, latitude, 0.0)
    assert result.status in (RiseSetStatus.OK, RiseSetStatus.NO_RISE)


@pytest.mark.parametrize("latitude", [-90.1, 90.1, 180.0])
def test_out_of_range_latitude_rejected(latitude):
    jd = _jd(2024, 3, 20)
    with pytest.raises(ValueError):
        sunrise(jd, latitude, 0.0)


@pytest.mark.parametrize("longitude", [-180.1, 180.1, 360.0])
def test_out_of_range_longitude_rejected(longitude):
    jd = _jd(2024, 3, 20)
    with pytest.raises(ValueError):
        sunrise(jd, 0.0, longitude)


@pytest.mark.parametrize("longitude", [-180.0, 180.0])
def test_longitude_antimeridian_boundary_accepted(longitude):
    jd = _jd(2024, 3, 20)
    result = sunrise(jd, 0.0, longitude)
    assert result.status == RiseSetStatus.OK


# --- Elevation ---------------------------------------------------------


def test_zero_elevation_has_zero_dip():
    assert horizon_dip_degrees(0.0) == 0.0


def test_negative_elevation_has_zero_dip_not_a_negative_one():
    # The standard dip formula is undefined below sea level; this
    # module does not extrapolate it into a negative (raised) horizon.
    assert horizon_dip_degrees(-100.0) == 0.0


def test_dip_increases_with_elevation():
    assert horizon_dip_degrees(100.0) < horizon_dip_degrees(4000.0)
    assert horizon_dip_degrees(4000.0) < horizon_dip_degrees(8848.0)  # Everest


def test_dip_matches_the_documented_meeus_formula():
    # 0.0293 * sqrt(4000) - independently recomputed here, not copied
    # from the module's own internal constant reference by import.
    expected = 0.0293 * (4000.0 ** 0.5)
    assert horizon_dip_degrees(4000.0) == pytest.approx(expected, rel=1e-12)


def test_higher_elevation_sees_sunrise_earlier():
    # Physically required direction: from a mountain you see the sun
    # before someone at sea level on the same meridian does. Verified
    # empirically against raw swe.rise_trans_true_hor before this
    # module was written (487s earlier at 4000m over the equator at
    # equinox); re-checked here as a regression guard, not re-derived.
    jd = _jd(2024, 3, 20)
    sea_level = sunrise(jd, 0.0, 0.0, elevation_m=0.0)
    mountain = sunrise(jd, 0.0, 0.0, elevation_m=4000.0)
    assert mountain.julian_day_ut < sea_level.julian_day_ut


def test_higher_elevation_sees_sunset_later():
    jd = _jd(2024, 3, 20)
    sea_level = sunset(jd, 0.0, 0.0, elevation_m=0.0)
    mountain = sunset(jd, 0.0, 0.0, elevation_m=4000.0)
    assert mountain.julian_day_ut > sea_level.julian_day_ut


def test_below_sea_level_elevation_does_not_raise():
    # E.g. the Dead Sea shore, roughly -430m. No arbitrary lower bound
    # is imposed (ADR-0054); only finiteness is required.
    jd = _jd(2024, 3, 20)
    result = sunrise(jd, 31.5, 35.5, elevation_m=-430.0)
    assert result.status == RiseSetStatus.OK


@pytest.mark.parametrize("elevation", [float("inf"), float("-inf"), float("nan")])
def test_non_finite_elevation_rejected(elevation):
    jd = _jd(2024, 3, 20)
    with pytest.raises(ValueError):
        sunrise(jd, 0.0, 0.0, elevation_m=elevation)


# --- Declared-convention enforcement (ADR-0054) -------------------------


def test_default_profile_carries_the_ratified_conventions():
    from engine.astronomy.profile import (
        RISE_SET_DISC_UPPER_LIMB,
        RISE_SET_REFRACTION_STANDARD,
    )

    assert PARASHARI_LAHIRI.rise_set_disc_reference == RISE_SET_DISC_UPPER_LIMB
    assert PARASHARI_LAHIRI.rise_set_refraction == RISE_SET_REFRACTION_STANDARD


def test_unratified_disc_reference_is_rejected_not_silently_applied():
    bad_profile = replace(PARASHARI_LAHIRI, rise_set_disc_reference="center")
    jd = _jd(2024, 3, 20)
    with pytest.raises(UnsupportedRiseSetConventionError):
        sunrise(jd, 0.0, 0.0, profile=bad_profile)


def test_unratified_refraction_is_rejected_not_silently_applied():
    bad_profile = replace(PARASHARI_LAHIRI, rise_set_refraction="none")
    jd = _jd(2024, 3, 20)
    with pytest.raises(UnsupportedRiseSetConventionError):
        sunrise(jd, 0.0, 0.0, profile=bad_profile)


# --- Strict ephemeris fallback guard -------------------------------------


def test_strict_mode_raises_outside_bundled_ephemeris_range():
    # Year 3000 is well outside the bundled 1800-2399 CE range.
    jd = _jd(3000, 1, 1)
    with pytest.raises(EphemerisFallbackError):
        sunrise(jd, 0.0, 0.0, strict=True)


def test_non_strict_mode_falls_back_instead_of_raising():
    jd = _jd(3000, 1, 1)
    result = sunrise(jd, 0.0, 0.0, strict=False)
    assert result.status == RiseSetStatus.OK


def test_negative_control_strict_guard_actually_distinguishes_modes():
    # Proves the guard in the previous two tests can fail: the same
    # call succeeds non-strict and raises strict, so the assertion is
    # not vacuously true for some unrelated reason (e.g. the whole
    # function always raising, or never raising).
    jd = _jd(3000, 1, 1)
    strict_raised = False
    try:
        sunrise(jd, 0.0, 0.0, strict=True)
    except EphemerisFallbackError:
        strict_raised = True
    non_strict_result = sunrise(jd, 0.0, 0.0, strict=False)
    assert strict_raised is True
    assert non_strict_result.status == RiseSetStatus.OK


# --- Input validation on event routing -----------------------------------


def test_invalid_event_rejected():
    from engine.astronomy.rise_set import _rise_or_set

    jd = _jd(2024, 3, 20)
    with pytest.raises(ValueError):
        _rise_or_set("noon", jd, 0.0, 0.0)


# --- Negative control: proves independent-reference comparison can fail ---


def test_negative_control_broken_elevation_handling_is_caught_by_independent_reference(
    monkeypatch,
):
    """
    ADR-0054: a PASS is meaningful only if the check can fail. Plants a
    genuine defect (elevation silently ignored, exactly the class of
    bug ADR-0054's own design investigation ruled out empirically
    before this module was written) and confirms
    validate_rise_set_holdout.py's independently-coded reference - a
    different method again from this module's own implementation -
    detects the resulting discrepancy, comfortably outside its normal
    tolerance. Restored via monkeypatch teardown; re-verified restored
    explicitly rather than merely assumed.
    """

    import importlib

    validator = importlib.import_module("validate_rise_set_holdout")

    jd = _jd(2024, 3, 20)
    lat, lon, elevation_m = 0.0, 0.0, 4000.0

    # Sanity: the real implementation must already be within tolerance,
    # or this control would prove nothing about the mutation.
    good = sunrise(jd, lat, lon, elevation_m=elevation_m)
    good_ref = validator.reference_rise_set(jd, lat, lon, elevation_m, rising=True)
    assert good.status == RiseSetStatus.OK and good_ref is not None
    good_delta = abs(good.julian_day_ut - good_ref) * 86400.0
    assert good_delta < validator._TOLERANCE_SECONDS

    monkeypatch.setattr(rise_set_module, "horizon_dip_degrees", lambda elevation_m: 0.0)

    broken = sunrise(jd, lat, lon, elevation_m=elevation_m)
    assert broken.status == RiseSetStatus.OK
    broken_delta = abs(broken.julian_day_ut - good_ref) * 86400.0
    assert broken_delta > validator._TOLERANCE_SECONDS, (
        "planted elevation-dip defect was not detected by the independent "
        "reference; the negative control proves nothing"
    )

    monkeypatch.undo()
    restored = sunrise(jd, lat, lon, elevation_m=elevation_m)
    assert restored.julian_day_ut == good.julian_day_ut
