"""
Transit event types and cross-layer consistency
(Gates 1-2 of ADR-0008).
"""

import math

import pytest
import swisseph as swe

from engine.astrology.nakshatra import nakshatra
from engine.astrology.signs import zodiac_sign
from engine.astronomy.profile import PARASHARI_LAHIRI
from engine.astronomy.sidereal_planets import sidereal_planet_position
from engine.calculations.calculations import calculate
from engine.kp.chain import kp_chain
from engine.models.birth_data import BirthData
from engine.transits.events import (
    natal_conjunctions,
    nakshatra_ingresses,
    returns,
    sign_ingresses,
)
from engine.transits.view import TransitProfileError, TransitView, transit_view

JD_2024 = swe.julday(2024, 1, 1, 0.0, swe.GREG_CAL)
BIRTH = BirthData(1985, 12, 21, 14, 40, 0.0, 25.6, 85.1333, "Asia/Kolkata")


def _sun_longitude(julian_day):
    return sidereal_planet_position(
        julian_day, swe.SUN, PARASHARI_LAHIRI.ayanamsa_mode,
    ).longitude


def test_sun_has_exactly_12_sign_ingresses_per_year():
    events = sign_ingresses("Sun", JD_2024, JD_2024 + 366, PARASHARI_LAHIRI)
    assert len(events) == 12
    assert all(event.kind == "sign_ingress" for event in events)
    boundaries = sorted(event.target_longitude for event in events)
    assert boundaries == [30.0 * k for k in range(12)]


def test_classification_after_ingress_matches_certified_primitives():
    # Epsilon after each Sun sign ingress, the certified sign, nakshatra,
    # and KP chain classifications must all agree with the boundary
    # just crossed (Gate 2).
    for event in sign_ingresses("Sun", JD_2024, JD_2024 + 366, PARASHARI_LAHIRI):
        after = _sun_longitude(event.julian_day + 0.05)  # ~0.05 deg later
        expected_sign = int(round(event.target_longitude / 30.0)) % 12 + 1
        assert zodiac_sign(after) == expected_sign
        assert kp_chain(after).sign_number == expected_sign


def test_moon_nakshatra_ingress_agrees_with_kp_chain():
    events = nakshatra_ingresses("Moon", JD_2024, JD_2024 + 28, PARASHARI_LAHIRI)
    assert len(events) >= 27  # full sidereal month
    for event in events[:29]:
        moon_after = sidereal_planet_position(
            event.julian_day + 0.002, swe.MOON, PARASHARI_LAHIRI.ayanamsa_mode,
        ).longitude
        boundary_index = int(round(event.target_longitude / (40.0 / 3.0))) % 27
        expected = boundary_index + 1
        assert nakshatra(moon_after) == expected
        assert kp_chain(moon_after).nakshatra_number == expected


def test_solar_return_lands_on_natal_sun():
    natal = calculate(BIRTH, profile=PARASHARI_LAHIRI).snapshot
    natal_sun = natal.sidereal_planets["Sun"].longitude
    window_start = swe.julday(2024, 11, 1, 0.0, swe.GREG_CAL)
    events = returns("Sun", natal_sun, window_start, window_start + 90, PARASHARI_LAHIRI)
    assert len(events) == 1
    event = events[0]
    assert event.kind == "return"
    # Solar return 2024 for a Dec-21 (tropical) birth: sidereal natal Sun
    # is crossed within days of the birthday.
    year, month, day, _hours = swe.revjul(event.julian_day, swe.GREG_CAL)
    assert (year, month) == (2024, 12)
    assert abs(day - 21) <= 3


def test_natal_conjunctions_label_events():
    natal = calculate(BIRTH, profile=PARASHARI_LAHIRI).snapshot
    points = {
        "Sun": natal.sidereal_planets["Sun"].longitude,
        "Ascendant": natal.houses.ascendant,
    }
    labelled = natal_conjunctions("Moon", points, JD_2024, JD_2024 + 28, PARASHARI_LAHIRI)
    labels = {label for label, _event in labelled}
    assert labels == {"Sun", "Ascendant"}
    for label, event in labelled:
        assert event.kind == "natal_conjunction"
        assert event.residual_arcsec <= 1e-4


def test_transit_view_profile_guard_and_separations():
    natal = calculate(BIRTH, profile=PARASHARI_LAHIRI).snapshot
    view = transit_view(natal, JD_2024, 25.6, 85.1333, PARASHARI_LAHIRI)
    assert isinstance(view, TransitView)
    assert view.provenance.profile_name == "parashari_lahiri"
    contact = {(c.transiting, c.natal): c.separation for c in view.contacts}
    # Separation is symmetric wrap distance in [0, 180].
    for value in contact.values():
        assert 0.0 <= value <= 180.0
    # Self-check: separation(Sun natal, Sun natal) computed from the
    # view's own tables matches the wrap formula.
    sun_sun = abs(((view.transit_longitudes["Sun"] - view.natal_longitudes["Sun"] + 180.0) % 360.0) - 180.0)
    assert math.isclose(contact[("Sun", "Sun")], sun_sun)

    from engine.astronomy.profile import KP_KRISHNAMURTI

    with pytest.raises(TransitProfileError):
        transit_view(natal, JD_2024, 25.6, 85.1333, KP_KRISHNAMURTI)
