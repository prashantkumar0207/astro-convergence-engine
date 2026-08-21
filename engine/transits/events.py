"""
Transit event types (TRANSIT_V1, ADR-0008).

Every event type is the certified crossing primitive applied to a
documented target set. Boundary targets use the same exact rational
boundaries as the certified classification layers (float of k*30 and
k*40/3), so Gate 2 can require that classification immediately after
an ingress agrees with the certified sign/nakshatra/KP primitives.

`declared_division` (H-02 fix Option 1, ADR-0065): `sign_ingresses`/
`nakshatra_ingresses` populate each event's `declared_division` from the
EXACT `target_longitude` they searched for, via the same certified
`zodiac_sign`/`nakshatra` classifiers every other capability uses - never
by re-classifying the reported `julian_day`'s own (residual-bounded, and
therefore occasionally boundary-adjacent) longitude. `find_crossings`
itself is unchanged; this module classifies only after the fact, using
information (which boundary was searched for) only these two functions
have.
"""

from dataclasses import replace
from fractions import Fraction

from engine.astrology.nakshatra import nakshatra as _classify_nakshatra
from engine.astrology.signs import zodiac_sign as _classify_sign
from engine.astronomy.profile import CalculationProfile
from engine.transits.crossing import find_crossings

_SIGN_BOUNDARIES = tuple(float(30 * k) for k in range(12))
_NAKSHATRA_BOUNDARIES = tuple(float(Fraction(40, 3) * k) for k in range(27))


def _multi_target(body, targets, jd_start, jd_end, profile, kind, classify=None):
    events = []
    for target in targets:
        found = find_crossings(body, target, jd_start, jd_end, profile, kind=kind)
        if classify is not None:
            found = tuple(replace(event, declared_division=classify(event.target_longitude)) for event in found)
        events.extend(found)
    return tuple(sorted(events, key=lambda event: event.julian_day))


def sign_ingresses(
    body: str, jd_start: float, jd_end: float, profile: CalculationProfile,
) -> tuple:
    """All sidereal sign-boundary crossings in the window. Each event's
    `declared_division` is the sign (1-12) it crosses into, classified
    from the exact boundary target, not the reported instant."""

    return _multi_target(body, _SIGN_BOUNDARIES, jd_start, jd_end, profile, "sign_ingress", _classify_sign)


def nakshatra_ingresses(
    body: str, jd_start: float, jd_end: float, profile: CalculationProfile,
) -> tuple:
    """All nakshatra-boundary crossings in the window. Each event's
    `declared_division` is the nakshatra (1-27) it crosses into,
    classified from the exact boundary target, not the reported instant."""

    return _multi_target(
        body, _NAKSHATRA_BOUNDARIES, jd_start, jd_end, profile, "nakshatra_ingress", _classify_nakshatra,
    )


def returns(
    body: str,
    natal_longitude: float,
    jd_start: float,
    jd_end: float,
    profile: CalculationProfile,
) -> tuple:
    """Crossings of the body's own natal longitude (returns)."""

    return find_crossings(
        body, natal_longitude, jd_start, jd_end, profile, kind="return",
    )


def natal_conjunctions(
    body: str,
    natal_points: dict,
    jd_start: float,
    jd_end: float,
    profile: CalculationProfile,
) -> tuple:
    """
    Crossings of named natal longitudes (exact transit-to-natal
    conjunctions). ``natal_points`` maps a label (e.g. "Moon",
    "Ascendant") to its natal sidereal longitude; labels are attached
    to the returned events via the target_longitude they carry.
    """

    events = []
    for label, longitude in natal_points.items():
        for event in find_crossings(
            body, longitude, jd_start, jd_end, profile, kind="natal_conjunction",
        ):
            events.append((label, event))
    events.sort(key=lambda pair: pair[1].julian_day)
    return tuple(events)
