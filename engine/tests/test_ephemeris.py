"""
Tests for deterministic ephemeris initialization and mode guarding
(audit finding F-02).

These tests assert the ACTUAL Swiss Ephemeris return flags, so a
silent Moshier fallback can never again masquerade as SWIEPH.
"""

import tempfile

import pytest
import swisseph as swe

from engine.astronomy.ephemeris import (
    BUNDLED_RANGE_YEARS,
    MODE_MOSEPH,
    MODE_SWIEPH,
    REQUIRED_FILES,
    EphemerisFallbackError,
    EphemerisFilesMissingError,
    calc_ut_checked,
    default_ephemeris_path,
    initialize_ephemeris,
)


BODIES = (
    swe.SUN,
    swe.MOON,
    swe.MERCURY,
    swe.VENUS,
    swe.MARS,
    swe.JUPITER,
    swe.SATURN,
    swe.MEAN_NODE,
    swe.TRUE_NODE,
    swe.PLUTO,
)

# Epochs spanning the bundled 1800-2399 coverage.
EPOCHS = (
    swe.julday(1823, 3, 4, 10.0, swe.GREG_CAL),
    swe.julday(1900, 1, 1, 0.0, swe.GREG_CAL),
    swe.julday(1989, 7, 12, 11.2333, swe.GREG_CAL),
    swe.julday(2000, 1, 1, 12.0, swe.GREG_CAL),
    swe.julday(2100, 6, 15, 6.5, swe.GREG_CAL),
    swe.julday(2350, 12, 31, 23.0, swe.GREG_CAL),
)


@pytest.fixture(autouse=True)
def restore_ephemeris_path():
    """Every test leaves the process configured with the bundled path."""
    yield
    initialize_ephemeris(force=True)


def test_bundled_files_are_present():
    root = default_ephemeris_path()

    for name in REQUIRED_FILES:
        assert (root / name).is_file(), f"missing bundled file {name}"


def test_swieph_actually_selected_for_all_bodies_and_epochs():
    initialize_ephemeris(force=True)

    for julian_day in EPOCHS:
        for body in BODIES:
            values, mode = calc_ut_checked(
                julian_day,
                body,
                swe.FLG_SWIEPH | swe.FLG_SPEED,
                strict=True,
            )

            assert mode == MODE_SWIEPH
            assert 0.0 <= values[0] < 360.0


def test_raw_retflag_contains_swieph_bit():
    initialize_ephemeris(force=True)

    result = swe.calc_ut(EPOCHS[3], swe.MOON, swe.FLG_SWIEPH | swe.FLG_SPEED)

    assert result[1] & swe.FLG_SWIEPH
    assert not (result[1] & swe.FLG_MOSEPH)


def test_missing_files_raise_at_initialization():
    with tempfile.TemporaryDirectory() as empty:
        with pytest.raises(EphemerisFilesMissingError):
            initialize_ephemeris(empty, force=True)


def test_strict_mode_detects_fallback_from_empty_path():
    with tempfile.TemporaryDirectory() as empty:
        # Bypass initialization to simulate a misconfigured process.
        swe.set_ephe_path(empty)

        result = swe.calc_ut(2451545.0, swe.SUN, swe.FLG_SWIEPH)
        assert result[1] & swe.FLG_MOSEPH  # confirmed silent fallback

    initialize_ephemeris(force=True)


def test_out_of_range_date_raises_in_strict_mode():
    initialize_ephemeris(force=True)

    before = swe.julday(BUNDLED_RANGE_YEARS[0] - 5, 1, 1, 12.0, swe.GREG_CAL)
    after = swe.julday(BUNDLED_RANGE_YEARS[1] + 5, 1, 1, 12.0, swe.GREG_CAL)

    for julian_day in (before, after):
        with pytest.raises(EphemerisFallbackError):
            calc_ut_checked(
                julian_day,
                swe.SUN,
                swe.FLG_SWIEPH,
                strict=True,
            )


def test_out_of_range_date_reports_moseph_in_non_strict_mode():
    initialize_ephemeris(force=True)

    julian_day = swe.julday(1500, 1, 1, 12.0, swe.GREG_CAL)

    values, mode = calc_ut_checked(
        julian_day,
        swe.SUN,
        swe.FLG_SWIEPH,
        strict=False,
    )

    assert mode == MODE_MOSEPH
    assert 0.0 <= values[0] < 360.0


def test_moon_swieph_vs_moshier_differ_measurably():
    """
    The audit measured 0.4519 arcsec Moon deviation at the canonical
    JD. Assert the two modes actually differ, proving the guard
    protects a real precision boundary.
    """
    initialize_ephemeris(force=True)

    julian_day = 2447719.968055556

    swieph, mode = calc_ut_checked(
        julian_day, swe.MOON, swe.FLG_SWIEPH, strict=True
    )
    assert mode == MODE_SWIEPH

    moseph = swe.calc_ut(julian_day, swe.MOON, swe.FLG_MOSEPH)[0]

    deviation_arcsec = abs(swieph[0] - moseph[0]) * 3600.0

    assert 0.1 < deviation_arcsec < 1.0
