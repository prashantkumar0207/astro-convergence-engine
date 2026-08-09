"""
Transit event model (TRANSIT_V1, ADR-TRANSIT-001).
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TransitEvent:
    """
    One longitude-crossing event.

    Attributes
    ----------
    body
        Canonical body name.
    target_longitude
        The sidereal longitude that was crossed, degrees.
    julian_day
        Event instant (UT Julian Day), refined by bisection to the
        certified tolerance (1e-6 day, Decision TR-A).
    direction
        +1 if the body crossed the target moving direct, -1 if
        retrograde, 0 for a tangent contact at a station (the body
        touched the target and reversed without crossing).
    residual_arcsec
        |certified longitude at julian_day - target| in arcseconds;
        certification requires <= 1e-4 arcsec for crossings.
    kind
        Event label: "crossing", "sign_ingress", "nakshatra_ingress",
        "return", "natal_conjunction", or "tangent".
    profile_name
        CalculationProfile that produced the positions.
    """

    body: str
    target_longitude: float
    julian_day: float
    direction: int
    residual_arcsec: float
    kind: str
    profile_name: str
