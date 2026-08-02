"""
Sidereal Planet Engine

Converts a tropical planetary position into a sidereal position.

Contains no astrological interpretation.
"""

from __future__ import annotations

from engine.models.ayanamsa import Ayanamsa
from engine.models.planet_position import PlanetPosition
from engine.models.sidereal_planet_position import SiderealPlanetPosition


def sidereal_planet(
    tropical: PlanetPosition,
    ayanamsa: Ayanamsa,
) -> SiderealPlanetPosition:
    """
    Convert a tropical position to a sidereal position.
    """

    longitude = (tropical.longitude - ayanamsa.value) % 360.0

    return SiderealPlanetPosition(
        longitude=longitude,
        latitude=tropical.latitude,
        distance=tropical.distance,
        speed_longitude=tropical.speed_longitude,
        speed_latitude=tropical.speed_latitude,
        speed_distance=tropical.speed_distance,
    )