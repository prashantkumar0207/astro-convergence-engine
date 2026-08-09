"""
Transit event types (TRANSIT_V1, ADR-TRANSIT-001).

Every event type is the certified crossing primitive applied to a
documented target set. Boundary targets use the same exact rational
boundaries as the certified classification layers (float of k*30 and
k*40/3), so Gate 2 can require that classification immediately after
an ingress agrees with the certified sign/nakshatra/KP primitives.
"""

from fractions import Fraction

from engine.astronomy.profile import CalculationProfile
from engine.transits.crossing import find_crossings

_SIGN_BOUNDARIES = tuple(float(30 * k) for k in range(12))
_NAKSHATRA_BOUNDARIES = tuple(float(Fraction(40, 3) * k) for k in range(27))


def _multi_target(body, targets, jd_start, jd_end, profile, kind):
    events = []
    for target in targets:
        events.extend(find_crossings(body, target, jd_start, jd_end, profile, kind=kind))
    return tuple(sorted(events, key=lambda event: event.julian_day))


def sign_ingresses(
    body: str, jd_start: float, jd_end: float, profile: CalculationProfile,
) -> tuple:
    """All sidereal sign-boundary crossings in the window."""

    return _multi_target(body, _SIGN_BOUNDARIES, jd_start, jd_end, profile, "sign_ingress")


def nakshatra_ingresses(
    body: str, jd_start: float, jd_end: float, profile: CalculationProfile,
) -> tuple:
    """All nakshatra-boundary crossings in the window."""

    return _multi_target(
        body, _NAKSHATRA_BOUNDARIES, jd_start, jd_end, profile, "nakshatra_ingress",
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
