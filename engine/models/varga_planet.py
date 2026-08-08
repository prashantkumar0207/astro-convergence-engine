from dataclasses import dataclass


@dataclass(frozen=True)
class VargaPosition:
    """
    Authoritative varga placement of a point (Phase A generic model).

    The classification (sign, division_number, fraction) is the
    canonical output; no expanded D-space longitude is carried,
    because longitude projection is a per-varga convention owned by
    certified modules (ADR refinement).

    Attributes
    ----------
    source_longitude
        The sidereal D1 longitude that was classified, in degrees.
    sign
        0-based sign in the divisional chart (matching the certified
        D9/D10 convention).
    division_number
        1-based division within the source sign (generic name for
        what D9 calls navamsa_number and D10 calls segment).
    fraction
        Position within the division, in [0, 1).
    """

    source_longitude: float
    sign: int
    division_number: int
    fraction: float


@dataclass(frozen=True)
class VargaPlanet:
    """A named planet's varga placement."""

    name: str
    source_longitude: float
    sign: int
    division_number: int
    fraction: float
