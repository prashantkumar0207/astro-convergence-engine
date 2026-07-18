"""
Planet Position Model

Immutable data model representing the raw tropical astronomical
position returned by the Planet Position Engine.

This model contains only deterministic astronomical values.
No astrological interpretation belongs here.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PlanetPosition:
    """
    Raw astronomical position of a celestial body.

    Attributes
    ----------
    longitude : float
        Tropical ecliptic longitude in degrees.

    latitude : float
        Ecliptic latitude in degrees.

    distance : float
        Distance from Earth (Swiss Ephemeris units).

    speed_longitude : float
        Daily motion in longitude.

    speed_latitude : float
        Daily motion in latitude.

    speed_distance : float
        Daily change in distance.
    """

    longitude: float
    latitude: float
    distance: float
    speed_longitude: float
    speed_latitude: float
    speed_distance: float