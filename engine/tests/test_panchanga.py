"""
Panchanga classification tests (ADR-0055).

Covers tithi/yoga/karana/nakshatra-reuse/vara classification: headline
sanity, boundary/ULP battery, karana/tithi/yoga naming, vara sunrise
rollover and circumpolar indeterminacy, and one genuine negative control
proving the independent reference can actually catch a broken classifier
(not merely that it currently passes).
"""

import math

import pytest
import swisseph as swe

from engine.astrology.nakshatra import nakshatra
from engine.astrology import panchanga as panchanga_module
from engine.astrology.panchanga import (
    KARANA_COUNT,
    KARANA_SPAN_DEGREES,
    TITHI_COUNT,
    TITHI_SPAN_DEGREES,
    YOGA_COUNT,
    YOGA_SPAN_DEGREES,
    Panchanga,
    VaraStatus,
    karana_index,
    nakshatra_index,
    panchanga,
    tithi_index,
    vara,
    yoga_index,
)
from engine.astrology.panchanga_names import (
    KARANA_LAST_FIXED,
    KARANA_MOVABLE_NAMES,
    PAKSHA_KRISHNA,
    PAKSHA_SHUKLA,
    VARA_NAMES,
    YOGA_NAMES,
    karana_name,
    tithi_name,
    tithi_paksha,
    vara_name,
    yoga_name,
)
from engine.astronomy.profile import KP_KRISHNAMURTI, PARASHARI_LAHIRI


# ---------------------------------------------------------------------
# Headline sanity
# ---------------------------------------------------------------------


def test_panchanga_headline_sanity():
    jd = swe.julday(2024, 1, 15, 12.0, swe.GREG_CAL)
    result = panchanga(jd, 28.6139, 77.2090, 0.0, PARASHARI_LAHIRI)

    assert isinstance(result, Panchanga)
    assert 1 <= result.tithi <= 30
    assert 1 <= result.nakshatra <= 27
    assert 1 <= result.yoga <= 27
    assert 1 <= result.karana <= 60
    assert result.vara.status == VaraStatus.OK
    # 2024-01-15 was a Monday (Somavara): independently known fact,
    # cross-checked directly against Python's own calendar below too.
    assert result.vara.index == 1
    assert vara_name(result.vara.index) == "Somavara"


def test_panchanga_nakshatra_reuses_the_certified_primitive():
    for longitude in (0.0, 13.3333333333, 90.0, 179.999999, 359.99999):
        assert nakshatra_index(longitude) == nakshatra(longitude)


# ---------------------------------------------------------------------
# Range coverage across many longitudes / profiles
# ---------------------------------------------------------------------


@pytest.mark.parametrize("sun_deg", [0.0, 15.0, 47.3, 91.0, 180.0, 271.5, 359.9])
@pytest.mark.parametrize("moon_deg", [0.0, 33.0, 88.8, 179.0, 250.0, 300.4, 355.5])
def test_indices_always_within_range(sun_deg, moon_deg):
    assert 1 <= tithi_index(sun_deg, moon_deg) <= TITHI_COUNT
    assert 1 <= yoga_index(sun_deg, moon_deg) <= YOGA_COUNT
    assert 1 <= karana_index(sun_deg, moon_deg) <= KARANA_COUNT


def test_tithi_yoga_karana_profile_independence():
    """ADR-0055 item 1: one boundary convention, no profile parameter.
    tithi/karana are additionally ayanamsa-invariant by construction
    (elongation cancels it); this proves that empirically too."""

    jd = swe.julday(2025, 6, 10, 9.0, swe.GREG_CAL)
    from engine.astronomy.sidereal_planets import sidereal_planet_position

    results = {}
    for profile in (PARASHARI_LAHIRI, KP_KRISHNAMURTI):
        sun = sidereal_planet_position(jd, swe.SUN, profile.ayanamsa_mode, True)
        moon = sidereal_planet_position(jd, swe.MOON, profile.ayanamsa_mode, True)
        results[profile.name] = (
            tithi_index(sun.longitude, moon.longitude),
            karana_index(sun.longitude, moon.longitude),
        )

    assert results["parashari_lahiri"] == results["kp_krishnamurti"]


# ---------------------------------------------------------------------
# Boundary / ULP battery (mirrors the D3/D7 varga boundary discipline)
# ---------------------------------------------------------------------


@pytest.mark.parametrize("k", list(range(1, TITHI_COUNT)))
def test_tithi_boundary_promote_up(k):
    boundary = k * TITHI_SPAN_DEGREES
    just_below = boundary - 1e-11  # inside promote-up tolerance
    just_below_outside = boundary - 1e-9  # outside tolerance

    assert tithi_index(0.0, just_below) == k + 1
    assert tithi_index(0.0, just_below_outside) == k


@pytest.mark.parametrize("k", list(range(1, KARANA_COUNT)))
def test_karana_boundary_promote_up(k):
    boundary = k * KARANA_SPAN_DEGREES
    just_below = boundary - 1e-11
    just_below_outside = boundary - 1e-9

    assert karana_index(0.0, just_below) == k + 1
    assert karana_index(0.0, just_below_outside) == k


@pytest.mark.parametrize("k", list(range(1, YOGA_COUNT)))
def test_yoga_boundary_promote_up(k):
    boundary = k * YOGA_SPAN_DEGREES
    just_below = boundary - 1e-11
    just_below_outside = boundary - 1e-9

    # yoga is a function of sun+moon; hold sun fixed at 0 so moon alone
    # sweeps the boundary, same technique as the tithi/karana cases.
    assert yoga_index(0.0, just_below) == k + 1
    assert yoga_index(0.0, just_below_outside) == k


def test_wraparound_top_clamp_matches_established_convention():
    """The 0/360 wraparound clamps into the LAST division rather than
    promoting into division 0 - engine.astrology.longitude_utils's own
    documented, already-certified convention (shared with nakshatra and
    every varga), not new behaviour introduced here."""

    just_below_360 = -1e-11  # normalizes to 359.99999999989
    assert tithi_index(0.0, just_below_360) == TITHI_COUNT
    assert karana_index(0.0, just_below_360) == KARANA_COUNT


# ---------------------------------------------------------------------
# Naming tables
# ---------------------------------------------------------------------


def test_tithi_naming_and_paksha():
    assert tithi_paksha(1) == PAKSHA_SHUKLA
    assert tithi_paksha(15) == PAKSHA_SHUKLA
    assert tithi_paksha(16) == PAKSHA_KRISHNA
    assert tithi_paksha(30) == PAKSHA_KRISHNA
    assert tithi_name(15) == "Purnima"
    assert tithi_name(30) == "Amavasya"
    assert tithi_name(1) == tithi_name(16) == "Pratipada"
    assert tithi_name(14) == tithi_name(29) == "Chaturdashi"
    for n in range(1, 31):
        assert isinstance(tithi_name(n), str) and tithi_name(n)
    with pytest.raises(ValueError):
        tithi_name(0)
    with pytest.raises(ValueError):
        tithi_name(31)


def test_yoga_naming():
    assert len(YOGA_NAMES) == 27
    assert len(set(YOGA_NAMES)) == 27  # all distinct
    assert yoga_name(1) == "Vishkumbha"
    assert yoga_name(27) == "Vaidhriti"
    with pytest.raises(ValueError):
        yoga_name(0)
    with pytest.raises(ValueError):
        yoga_name(28)


def test_karana_naming_fixed_and_movable_positions():
    assert karana_name(1) == "Kimstughna"
    assert [karana_name(i) for i in (58, 59, 60)] == list(KARANA_LAST_FIXED)
    assert karana_name(2) == KARANA_MOVABLE_NAMES[0]
    assert karana_name(57) == KARANA_MOVABLE_NAMES[-1]
    # movable cycle has period 7 across indices 2-57 (8 full cycles)
    for offset in range(7):
        names_at_offset = {karana_name(2 + offset + 7 * cycle) for cycle in range(8)}
        assert len(names_at_offset) == 1
    for n in range(1, 61):
        assert isinstance(karana_name(n), str) and karana_name(n)
    with pytest.raises(ValueError):
        karana_name(0)
    with pytest.raises(ValueError):
        karana_name(61)


def test_vara_naming():
    assert len(VARA_NAMES) == 7
    assert vara_name(0) == "Ravivara"
    assert vara_name(6) == "Shanivara"
    with pytest.raises(ValueError):
        vara_name(-1)
    with pytest.raises(ValueError):
        vara_name(7)


# ---------------------------------------------------------------------
# Vara: sunrise rollover, circumpolar indeterminacy, known weekdays
# ---------------------------------------------------------------------


@pytest.mark.parametrize(
    "y, m, d",
    [
        (2000, 1, 1),
        (2024, 1, 15),
        (2020, 2, 29),  # leap day
        (1970, 1, 1),   # Unix epoch
    ],
)
def test_vara_matches_python_stdlib_weekday_at_noon_ut(y, m, d):
    """Cross-check against Python's own independent Gregorian calendar
    implementation (not Swiss Ephemeris, not this module's own JD
    arithmetic), for a location/time comfortably after local sunrise
    (Delhi, local noon UT ~= 17:30 IST). Expected weekday is computed
    from `datetime.date`, not hand-transcribed, since a hand-transcribed
    weekday is exactly the kind of unverified claim this discipline
    exists to avoid."""

    from datetime import date as _date

    python_weekday = _date(y, m, d).weekday()  # Monday=0 .. Sunday=6
    expected_vara_index = (python_weekday + 1) % 7  # Sunday=0 .. Saturday=6

    jd = swe.julday(y, m, d, 12.0, swe.GREG_CAL)
    result = vara(jd, 28.6667, 77.2167)
    assert result.status == VaraStatus.OK
    assert result.index == expected_vara_index


def test_vara_rolls_over_exactly_at_anchor_sunrise_not_ut_midnight():
    lat, lon = 28.6667, 77.2167
    midnight = swe.julday(2024, 1, 15, 0.0, swe.GREG_CAL)
    from engine.astronomy.rise_set import RiseSetStatus, sunrise

    today_sunrise = sunrise(midnight, lat, lon)
    assert today_sunrise.status == RiseSetStatus.OK

    one_minute = 60.0 / 86400.0
    before = vara(today_sunrise.julian_day_ut - one_minute, lat, lon)
    after = vara(today_sunrise.julian_day_ut + one_minute, lat, lon)

    assert before.status == after.status == VaraStatus.OK
    assert after.index == (before.index + 1) % 7
    # Just before UT midnight (still the prior panchanga day) must equal
    # "before", not silently roll over early.
    just_before_midnight = vara(midnight - one_minute, lat, lon)
    assert just_before_midnight.index == before.index


def test_vara_circumpolar_is_indeterminate_not_a_guess():
    # Same real-world cases certify_rise_set.py already certifies as
    # NO_SET / NO_RISE.
    midsummer = swe.julday(2024, 6, 21, 12.0, swe.GREG_CAL)
    polar_night = swe.julday(2024, 12, 21, 12.0, swe.GREG_CAL)
    lat, lon = 78.2232, 15.6267

    for jd in (midsummer, polar_night):
        result = vara(jd, lat, lon)
        assert result.status == VaraStatus.INDETERMINATE
        assert result.index is None
        assert result.anchor_sunrise_julian_day_ut is None


def test_panchanga_aggregate_matches_individual_functions():
    jd = swe.julday(2025, 9, 3, 6.0, swe.GREG_CAL)
    lat, lon = 19.0760, 72.8777
    result = panchanga(jd, lat, lon, 0.0, PARASHARI_LAHIRI)

    assert result.tithi == tithi_index(result.sun_longitude, result.moon_longitude)
    assert result.yoga == yoga_index(result.sun_longitude, result.moon_longitude)
    assert result.karana == karana_index(result.sun_longitude, result.moon_longitude)
    assert result.nakshatra == nakshatra_index(result.moon_longitude)
    assert result.vara == vara(jd, lat, lon, 0.0, PARASHARI_LAHIRI)


# ---------------------------------------------------------------------
# Genuine negative control: proves the independent reference can fail
# ---------------------------------------------------------------------


def test_negative_control_broken_division_index_is_caught_by_independent_reference(monkeypatch):
    import validate_panchanga_holdout as validator

    # A value comfortably inside tithi 6 (elongation 61 degrees).
    sun_l, moon_l = 0.0, 61.0
    correct = tithi_index(sun_l, moon_l)
    assert correct == 6

    monkeypatch.setattr(panchanga_module, "division_index", lambda value, size, count: 0)
    broken = tithi_index(sun_l, moon_l)
    assert broken == 1  # visibly wrong: the injected defect

    reference = validator.exact_tithi(sun_l, moon_l)
    assert reference == correct
    assert broken != reference  # the independent reference catches it

    monkeypatch.undo()
    restored = tithi_index(sun_l, moon_l)
    assert restored == correct
