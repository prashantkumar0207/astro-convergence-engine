"""
Transit event model (TRANSIT_V1, ADR-0008; `declared_division` field,
H-02 fix Option 1, ADR-0065).
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
    declared_division
        H-02 fix (ADR-0065, DP-013 Option 1). For "sign_ingress" and
        "nakshatra_ingress" events, the sign (1-12) or nakshatra (1-27)
        this event is a crossing INTO, classified from the EXACT
        `target_longitude` (never subject to the root-finder's own
        residual) rather than by re-classifying the noisy `julian_day`
        longitude after the fact - the seam `division_index` promotion
        (`1e-10` degrees) and `find_crossings`' own residual guarantee
        (`1e-4` arcsec, ~278x wider) could otherwise disagree on. `None`
        for every other `kind`, where "division" has no defined meaning
        (a return/natal-conjunction/plain-crossing target is not
        necessarily a division boundary) - never guessed.
    """

    body: str
    target_longitude: float
    julian_day: float
    direction: int
    residual_arcsec: float
    kind: str
    profile_name: str
    declared_division: int | None = None
