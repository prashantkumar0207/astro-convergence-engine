"""
Transit crossing primitive gates (Gate 1 of ADR-0008):
residuals, completeness vs an independent dense scan, direction
flags, retrograde multiplicity, guards.
"""

import pytest
import swisseph as swe

from engine.astronomy.profile import KP_KRISHNAMURTI, PARASHARI_LAHIRI
from engine.astronomy.sidereal_planets import sidereal_planet_position
from engine.transits.crossing import (
    RESIDUAL_BOUND_ARCSEC,
    TIME_TOLERANCE_DAYS,
    find_crossings,
)

JD_2024 = swe.julday(2024, 1, 1, 0.0, swe.GREG_CAL)


def _longitude(body_id, julian_day, mode):
    return sidereal_planet_position(julian_day, body_id, mode).longitude


def _scan_count(body_id, target, jd0, jd1, mode, step=0.01):
    """Independent brute-force crossing counter (fine fixed grid)."""

    def diff(julian_day):
        delta = _longitude(body_id, julian_day, mode) - target
        return -((-delta + 180.0) % 360.0 - 180.0)

    count = 0
    previous = diff(jd0)
    cursor = jd0 + step
    while cursor <= jd1:
        current = diff(cursor)
        if previous * current < 0 and abs(previous - current) < 180.0:
            count += 1
        previous = current
        cursor += step
    return count


def test_residuals_within_certification_bound():
    events = []
    events += find_crossings("Sun", 0.0, JD_2024, JD_2024 + 366, PARASHARI_LAHIRI)
    events += find_crossings("Moon", 100.0, JD_2024, JD_2024 + 60, PARASHARI_LAHIRI)
    events += find_crossings("Mercury", 355.0, JD_2024, JD_2024 + 200, PARASHARI_LAHIRI)
    assert events
    for event in events:
        assert event.residual_arcsec <= RESIDUAL_BOUND_ARCSEC, event


def test_mercury_retrograde_triple_crossing_with_directions():
    events = find_crossings(
        "Mercury", 355.0,
        swe.julday(2024, 3, 1, 0.0, swe.GREG_CAL),
        swe.julday(2024, 6, 15, 0.0, swe.GREG_CAL),
        PARASHARI_LAHIRI,
    )
    assert [event.direction for event in events] == [1, -1, 1]
    for previous, current in zip(events, events[1:]):
        assert current.julian_day > previous.julian_day + TIME_TOLERANCE_DAYS


def test_completeness_matches_independent_scan():
    cases = [
        ("Mercury", swe.MERCURY, 355.0, JD_2024, JD_2024 + 200),
        ("Moon", swe.MOON, 100.0, JD_2024, JD_2024 + 60),
        ("Sun", swe.SUN, 0.0, JD_2024, JD_2024 + 366),
        ("Mars", swe.MARS, 150.0, JD_2024, JD_2024 + 400),
    ]
    for body, body_id, target, jd0, jd1 in cases:
        found = [
            event for event in find_crossings(body, target, jd0, jd1, PARASHARI_LAHIRI)
            if event.direction != 0
        ]
        expected = _scan_count(body_id, target, jd0, jd1, PARASHARI_LAHIRI.ayanamsa_mode)
        assert len(found) == expected, (body, target, len(found), expected)


def test_event_longitude_actually_equals_target():
    for event in find_crossings("Sun", 123.456, JD_2024, JD_2024 + 366, PARASHARI_LAHIRI):
        longitude = _longitude(swe.SUN, event.julian_day, PARASHARI_LAHIRI.ayanamsa_mode)
        delta = abs(((longitude - event.target_longitude + 180.0) % 360.0) - 180.0)
        assert delta * 3600.0 <= RESIDUAL_BOUND_ARCSEC


def test_ketu_events_oppose_rahu_events():
    # Derive a target on Rahu's actual path (mean node moves about
    # -19.35 deg/year), then require Ketu to cross the opposite point
    # at the same instants.
    mode = PARASHARI_LAHIRI.ayanamsa_mode
    start = _longitude(swe.MEAN_NODE, JD_2024, mode)
    end = _longitude(swe.MEAN_NODE, JD_2024 + 400, mode)
    target = (start - 0.5 * ((start - end) % 360.0)) % 360.0
    rahu = find_crossings("Rahu", target, JD_2024, JD_2024 + 400, PARASHARI_LAHIRI)
    ketu = find_crossings("Ketu", (target + 180.0) % 360.0, JD_2024, JD_2024 + 400,
                          PARASHARI_LAHIRI)
    assert len(rahu) == len(ketu) >= 1
    for rahu_event, ketu_event in zip(rahu, ketu):
        assert abs(rahu_event.julian_day - ketu_event.julian_day) < 60 * TIME_TOLERANCE_DAYS


def test_profiles_shift_event_times():
    lahiri = find_crossings("Sun", 0.0, JD_2024, JD_2024 + 366, PARASHARI_LAHIRI)
    kp = find_crossings("Sun", 0.0, JD_2024, JD_2024 + 366, KP_KRISHNAMURTI)
    assert len(lahiri) == len(kp) == 1
    # The Krishnamurti ayanamsa is ~5.8 arcmin SMALLER than Lahiri,
    # so the KP sidereal Sun runs ahead and its zodiac ingress comes
    # EARLIER: about 5.8 arcmin / ~59 arcmin-per-day = ~0.1 day.
    delta_days = lahiri[0].julian_day - kp[0].julian_day
    assert 0.05 < delta_days < 0.2


def test_empty_window_rejected():
    with pytest.raises(ValueError):
        find_crossings("Sun", 0.0, JD_2024, JD_2024, PARASHARI_LAHIRI)


def test_events_carry_profile_and_kind():
    event = find_crossings("Sun", 0.0, JD_2024, JD_2024 + 366, PARASHARI_LAHIRI)[0]
    assert event.profile_name == "parashari_lahiri"
    assert event.kind == "crossing"
    assert event.body == "Sun"
