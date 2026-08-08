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
        Ascendant ecliptic longitude in degrees, in the frame
        recorded by the `frame` attribute.

    mc
        Midheaven ecliptic longitude in degrees.

    armc
        Right ascension of the meridian in degrees. NOTE: this is
        an EQUATORIAL coordinate, unlike the ecliptic longitudes in
        the neighbouring fields.

    vertex
        Vertex ecliptic longitude in degrees.

    equatorial_ascendant
        Equatorial Ascendant in degrees.

    co_ascendant
        Co-Ascendant (Walter Koch definition) in degrees.

    polar_ascendant
        Polar Ascendant (Michael Munkasey definition) in degrees.

    houses
        Tuple of exactly twelve house cusp ecliptic longitudes in
        degrees, ZERO-INDEXED: houses[0] is the 1st house cusp.

    house_system
        Swiss Ephemeris house system code that produced the cusps
        (for example "P" for Placidus).

    frame
        Reference frame of all ecliptic longitudes in this model:
        "sidereal" or "tropical". The production pipeline always
        produces sidereal (audit finding F-01); synthetic fixtures
        default to sidereal.
    """

    ascendant: float
    mc: float
    armc: float
    vertex: float
    equatorial_ascendant: float
    co_ascendant: float
    polar_ascendant: float
    houses: tuple[float, ...]
    house_system: str = "P"
    frame: str = "sidereal"