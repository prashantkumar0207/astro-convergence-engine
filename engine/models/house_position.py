"""
House Position Model

Immutable data model representing deterministic house geometry
computed from the Swiss Ephemeris.

Contains no astrological interpretation.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class HousePosition:
    """
    Deterministic house calculation output.

    Attributes
    ----------
    ascendant
        Ascendant longitude.

    mc
        Midheaven longitude.

    armc
        Right ascension of the meridian.

    vertex
        Vertex longitude.

    equatorial_ascendant
        Equatorial Ascendant.

    co_ascendant
        Co-Ascendant.

    polar_ascendant
        Polar Ascendant.

    houses
        Tuple containing the twelve house cusps.
    """

    ascendant: float
    mc: float
    armc: float
    vertex: float
    equatorial_ascendant: float
    co_ascendant: float
    polar_ascendant: float
    houses: tuple[float, ...]