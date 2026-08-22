"""Tests for engine.astrology.trikalam (ADR-0060, PYJHORA_TRIKALAM_V1)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import swisseph as swe

from engine.astrology import trikalam as trikalam_module
from engine.astrology.panchanga import VaraStatus, _midnight_ut, vara
from engine.astrology.trikalam import (
    PERIOD_FRACTION,
    PYJHORA_TRIKALAM_V1,
    TrikalamElement,
    TrikalamStatus,
    trikalam_period,
)
from engine.astronomy.profile import KP_KRISHNAMURTI, PARASHARI_LAHIRI
from engine.astronomy.rise_set import RiseSetStatus, sunrise, sunset

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import validate_trikalam_holdout as validator  # noqa: E402

_HOLDOUT = validator._HOLDOUT_DATES
_CIRCUMPOLAR = validator._CIRCUMPOLAR_HOLDOUT
_PROFILES = (PARASHARI_LAHIRI, KP_KRISHNAMURTI)
_ELEMENTS = (TrikalamElement.RAHU_KALAM, TrikalamElement.YAMAGANDA, TrikalamElement.GULIKA)

#: Transcribed independently a THIRD time here, directly from ADR-0060's
#: quoted PyJHora source, to pin the frozen table against silent drift -
#: this is the "collected pinning test" Q8_CLOSURE_MATRIX.md s4 requires.
_EXPECTED_OFFSETS = {
    TrikalamElement.RAHU_KALAM: (0.875, 0.125, 0.75, 0.5, 0.625, 0.375, 0.25),
    TrikalamElement.GULIKA: (0.75, 0.625, 0.5, 0.375, 0.25, 0.125, 0.0),
    TrikalamElement.YAMAGANDA: (0.5, 0.375, 0.25, 0.125, 0.0, 0.75, 0.625),
}


def test_frozen_offset_table_matches_adr_0060_transcription():
    table = trikalam_module._OFFSETS[PYJHORA_TRIKALAM_V1]
    for element, expected in _EXPECTED_OFFSETS.items():
        assert table[element] == expected, element


def test_period_fraction_is_one_eighth():
    assert PERIOD_FRACTION == 0.125


@pytest.mark.parametrize("profile", _PROFILES, ids=lambda p: p.name)
def test_dense_sweep_matches_independent_validator(profile):
    for holdout_id, (y, m, d), lat, lon in _HOLDOUT:
        jd = swe.julday(y, m, d, 12.0, swe.GREG_CAL)
        for element in _ELEMENTS:
            result = trikalam_period(element, jd, lat, lon, 0.0, profile, True, PYJHORA_TRIKALAM_V1)
            ref = validator.exact_trikalam(element.value, jd, lat, lon, 0.0, profile, True)

            assert result.status == TrikalamStatus.OK, (holdout_id, element)
            assert ref.determinate
            assert result.start_julian_day_ut == ref.start_julian_day_ut, (holdout_id, element)
            assert result.end_julian_day_ut == ref.end_julian_day_ut, (holdout_id, element)


@pytest.mark.parametrize("holdout_id,date_tuple,lat,lon", _HOLDOUT, ids=[h[0] for h in _HOLDOUT])
def test_period_duration_is_exactly_one_eighth_of_day_length(holdout_id, date_tuple, lat, lon):
    y, m, d = date_tuple
    jd = swe.julday(y, m, d, 12.0, swe.GREG_CAL)
    midnight = _midnight_ut(jd)
    rise = sunrise(midnight, lat, lon, 0.0, PARASHARI_LAHIRI, True)
    set_ = sunset(midnight, lat, lon, 0.0, PARASHARI_LAHIRI, True)
    assert rise.status == RiseSetStatus.OK and set_.status == RiseSetStatus.OK
    day_duration = set_.julian_day_ut - rise.julian_day_ut

    for element in _ELEMENTS:
        result = trikalam_period(element, jd, lat, lon, 0.0, PARASHARI_LAHIRI, True, PYJHORA_TRIKALAM_V1)
        assert result.status == TrikalamStatus.OK
        assert result.end_julian_day_ut - result.start_julian_day_ut == pytest.approx(
            PERIOD_FRACTION * day_duration, abs=1e-8
        )


def test_all_21_weekday_element_combinations_pin_to_the_frozen_table():
    """A calendar week (7 consecutive days) starting from a known Sunday,
    at a mid-latitude reference location, exercises every weekday for
    every element - checks the offset actually used, not just that some
    number was returned."""

    lat, lon = 28.6667, 77.2167  # Delhi, matches H4/H10/H11's location.
    sunday_jd = swe.julday(2025, 3, 2, 12.0, swe.GREG_CAL)  # 2025-03-02 is a Sunday.

    for day_offset in range(7):
        jd = sunday_jd + day_offset
        weekday = vara(jd, lat, lon, 0.0, PARASHARI_LAHIRI, True)
        assert weekday.status == VaraStatus.OK
        assert weekday.index == day_offset, "holdout date arithmetic assumption broke"

        midnight = _midnight_ut(jd)
        rise = sunrise(midnight, lat, lon, 0.0, PARASHARI_LAHIRI, True)
        set_ = sunset(midnight, lat, lon, 0.0, PARASHARI_LAHIRI, True)
        day_duration = set_.julian_day_ut - rise.julian_day_ut

        for element in _ELEMENTS:
            result = trikalam_period(element, jd, lat, lon, 0.0, PARASHARI_LAHIRI, True, PYJHORA_TRIKALAM_V1)
            expected_start = rise.julian_day_ut + day_duration * _EXPECTED_OFFSETS[element][day_offset]
            assert result.start_julian_day_ut == pytest.approx(expected_start, abs=1e-9)


@pytest.mark.parametrize("holdout_id,date_tuple,lat,lon", _CIRCUMPOLAR, ids=[h[0] for h in _CIRCUMPOLAR])
def test_circumpolar_is_indeterminate(holdout_id, date_tuple, lat, lon):
    y, m, d = date_tuple
    jd = swe.julday(y, m, d, 12.0, swe.GREG_CAL)
    for element in _ELEMENTS:
        result = trikalam_period(element, jd, lat, lon, 0.0, PARASHARI_LAHIRI, True, PYJHORA_TRIKALAM_V1)
        assert result.status == TrikalamStatus.INDETERMINATE
        assert result.start_julian_day_ut is None
        assert result.end_julian_day_ut is None
        assert result.weekday_index is None


def test_unknown_variant_raises():
    jd = swe.julday(2025, 3, 2, 12.0, swe.GREG_CAL)
    with pytest.raises(ValueError):
        trikalam_period(TrikalamElement.RAHU_KALAM, jd, 28.6667, 77.2167, variant="NOT_A_REAL_VARIANT")


def test_pre_sunrise_instant_mirrors_pyjhora_mixed_behaviour():
    """ADR-0060 Decision item 7(b): the window is computed from the query
    instant's OWN calendar-day sunrise/sunset (not rolled back), but the
    offset is selected using panchanga.vara's rolled-back weekday. An
    instant a few hours before a day's sunrise must therefore: (a) use
    that SAME day's sunrise/sunset for the window, and (b) use the
    PREVIOUS day's weekday to select the offset."""

    lat, lon = 28.6667, 77.2167
    midnight = swe.julday(2025, 3, 2, 0.0, swe.GREG_CAL)  # 2025-03-02 00:00 UT, a Sunday.
    day_rise = sunrise(midnight, lat, lon, 0.0, PARASHARI_LAHIRI, True)
    assert day_rise.status == RiseSetStatus.OK

    before_sunrise = day_rise.julian_day_ut - (1.0 / 24.0)  # one hour earlier, still 2025-03-02 UT.
    weekday = vara(before_sunrise, lat, lon, 0.0, PARASHARI_LAHIRI, True)
    assert weekday.status == VaraStatus.OK
    assert weekday.index == 6, "expected Saturday (rolled back from Sunday)"

    result = trikalam_period(
        TrikalamElement.RAHU_KALAM, before_sunrise, lat, lon, 0.0, PARASHARI_LAHIRI, True, PYJHORA_TRIKALAM_V1
    )
    assert result.status == TrikalamStatus.OK
    assert result.weekday_index == 6

    day_set = sunset(midnight, lat, lon, 0.0, PARASHARI_LAHIRI, True)
    day_duration = day_set.julian_day_ut - day_rise.julian_day_ut
    expected_start = day_rise.julian_day_ut + day_duration * _EXPECTED_OFFSETS[TrikalamElement.RAHU_KALAM][6]
    assert result.start_julian_day_ut == pytest.approx(expected_start, abs=1e-9), (
        "window must use THIS calendar day's sunrise, not the rolled-back day's"
    )


#: ULP-scale epsilon for the boundary battery below - roughly 86 microseconds
#: in JD-day units, comfortably above this magnitude's double-precision
#: floor (~2.5e-10 days near JD 2,460,000) so the test is not flaky, but far
#: smaller than any real-world tolerance (the discontinuity under test is a
#: weekday-offset jump of at least 0.125 x day-length, typically 60+ minutes).
_ULP_EPSILON_DAYS = 1e-9


def test_ulp_boundary_at_the_exact_sunrise_weekday_rollover():
    """A genuine ULP battery, not a tolerance check: perturbs the query
    instant by _ULP_EPSILON_DAYS on either side of the EXACT sunrise Julian
    Day where panchanga.vara's weekday rolls over, and asserts the offset
    selection flips at exactly that instant - the discontinuity ADR-0060
    item 7(b) documents, tested at floating-point resolution rather than a
    coarse (e.g. one-hour) approximation of it."""

    lat, lon = 28.6667, 77.2167
    midnight = swe.julday(2025, 3, 2, 0.0, swe.GREG_CAL)  # 2025-03-02, a Sunday.
    day_rise = sunrise(midnight, lat, lon, 0.0, PARASHARI_LAHIRI, True)
    assert day_rise.status == RiseSetStatus.OK
    exact_sunrise = day_rise.julian_day_ut

    just_before = exact_sunrise - _ULP_EPSILON_DAYS
    just_at_or_after = exact_sunrise  # panchanga.vara's own boundary is `>=`.

    before = trikalam_period(TrikalamElement.RAHU_KALAM, just_before, lat, lon, 0.0, PARASHARI_LAHIRI, True, PYJHORA_TRIKALAM_V1)
    at_boundary = trikalam_period(TrikalamElement.RAHU_KALAM, just_at_or_after, lat, lon, 0.0, PARASHARI_LAHIRI, True, PYJHORA_TRIKALAM_V1)

    assert before.status == TrikalamStatus.OK and at_boundary.status == TrikalamStatus.OK
    assert before.weekday_index == 6, "1 ULP before sunrise must still be the rolled-back weekday (Saturday)"
    assert at_boundary.weekday_index == 0, "at/after sunrise must already be the new weekday (Sunday)"
    # A genuine discontinuity: the two starts must differ by roughly a full
    # offset-table step (0.125 x day-length, at least ~30 minutes at any
    # holdout latitude), not by anything resembling the 1e-9 day input
    # perturbation - proving the flip is a real logic branch, not noise.
    assert abs(at_boundary.start_julian_day_ut - before.start_julian_day_ut) > 0.02


def test_negative_control_ulp_boundary_battery_actually_fails_on_a_broken_rollback(monkeypatch):
    """Demonstrates the ULP test above is failure-capable: temporarily
    breaks panchanga.vara's rollback (so the weekday no longer flips at the
    sunrise boundary), confirms the SAME assertion this file's ULP test
    uses would then fail, restores the real function, and re-verifies the
    boundary is precise again. Mirrors this repository's established
    negative-control pattern (test_panchanga.py, certify_panchanga.py's
    Gate F)."""

    lat, lon = 28.6667, 77.2167
    midnight = swe.julday(2025, 3, 2, 0.0, swe.GREG_CAL)
    day_rise = sunrise(midnight, lat, lon, 0.0, PARASHARI_LAHIRI, True)
    exact_sunrise = day_rise.julian_day_ut
    just_before = exact_sunrise - _ULP_EPSILON_DAYS

    import engine.astrology.trikalam as trikalam_module

    real_vara = trikalam_module.vara

    def _always_same_weekday(*args, **kwargs):
        # Always report the pre-rollover weekday - the rollback never happens.
        result = real_vara(*args, **kwargs)
        if result.status != VaraStatus.OK:
            return result
        from dataclasses import replace
        return replace(result, index=6)

    monkeypatch.setattr(trikalam_module, "vara", _always_same_weekday)
    try:
        broken_before = trikalam_period(TrikalamElement.RAHU_KALAM, just_before, lat, lon, 0.0, PARASHARI_LAHIRI, True, PYJHORA_TRIKALAM_V1)
        broken_at = trikalam_period(TrikalamElement.RAHU_KALAM, exact_sunrise, lat, lon, 0.0, PARASHARI_LAHIRI, True, PYJHORA_TRIKALAM_V1)
        negative_control_caught = broken_at.weekday_index != 0  # would fail the real test's assertion
        assert negative_control_caught, "negative control: broken rollback was NOT caught by the ULP boundary check"
    finally:
        monkeypatch.undo()

    assert trikalam_module.vara is real_vara
    restored_before = trikalam_period(TrikalamElement.RAHU_KALAM, just_before, lat, lon, 0.0, PARASHARI_LAHIRI, True, PYJHORA_TRIKALAM_V1)
    restored_at = trikalam_period(TrikalamElement.RAHU_KALAM, exact_sunrise, lat, lon, 0.0, PARASHARI_LAHIRI, True, PYJHORA_TRIKALAM_V1)
    assert restored_before.weekday_index == 6
    assert restored_at.weekday_index == 0


def test_negative_control_broken_offset_table_is_caught_by_independent_reference(monkeypatch):
    """Demonstrates the independent validator (validate_trikalam_holdout,
    a genuinely separate re-typed table) actually catches a corrupted
    engine table, then confirms it is undone and agreement is restored -
    mirrors test_panchanga.py's established negative-control pattern."""

    jd = swe.julday(2025, 3, 2, 12.0, swe.GREG_CAL)  # H10, a Sunday.
    lat, lon = 28.6667, 77.2167

    broken_table = {
        PYJHORA_TRIKALAM_V1: {
            TrikalamElement.RAHU_KALAM: (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),  # wrong on purpose
            TrikalamElement.GULIKA: trikalam_module._OFFSETS[PYJHORA_TRIKALAM_V1][TrikalamElement.GULIKA],
            TrikalamElement.YAMAGANDA: trikalam_module._OFFSETS[PYJHORA_TRIKALAM_V1][TrikalamElement.YAMAGANDA],
        }
    }
    monkeypatch.setattr(trikalam_module, "_OFFSETS", broken_table)

    broken_result = trikalam_period(
        TrikalamElement.RAHU_KALAM, jd, lat, lon, 0.0, PARASHARI_LAHIRI, True, PYJHORA_TRIKALAM_V1
    )
    ref = validator.exact_trikalam("rahu_kalam", jd, lat, lon, 0.0, PARASHARI_LAHIRI, True)
    assert broken_result.start_julian_day_ut != ref.start_julian_day_ut, (
        "negative control did not actually break anything - test is vacuous"
    )

    monkeypatch.undo()

    restored_result = trikalam_period(
        TrikalamElement.RAHU_KALAM, jd, lat, lon, 0.0, PARASHARI_LAHIRI, True, PYJHORA_TRIKALAM_V1
    )
    assert restored_result.start_julian_day_ut == ref.start_julian_day_ut
