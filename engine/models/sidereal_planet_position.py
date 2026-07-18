"""
Sidereal Planet Position Model

Immutable data model representing deterministic sidereal
planetary positions.

Contains no astrological interpretation.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SiderealPlanetPosition:
    """
    Deterministic sidereal planetary position.

    Attributes
    ----------
    longitude
        Sidereal ecliptic longitude.

    latitude
        Ecliptic latitude.

    distance
        Distance from Earth.

    speed_longitude
        Daily motion in longitude.

    speed_latitude
        Daily motion in latitude.

    speed_distance
        Daily motion in distance.
    """

    longitude: float
    latitude: float
    distance: float
    speed_longitude: float
    speed_latitude: float
    speed_distance: float