"""
Sidereal Planet Engine

Transforms tropical planetary positions into sidereal
planetary positions using an Ayanamsa.

No astrological interpretation is performed here.
"""

from __future__ import annotations

from engine.models.planet_position import PlanetPosition
from engine.models.ayanamsa import Ayanamsa
from engine.models.sidereal_planet_position import SiderealPlanetPosition


def sidereal_planet(
    planet: PlanetPosition,
    ayanamsa: Ayanamsa,
) -> SiderealPlanetPosition:
    """
    Convert a tropical planetary position into
    a sidereal planetary position.
    """

    if not isinstance(planet, PlanetPosition):
        raise TypeError("planet must be a PlanetPosition.")

    if not isinstance(ayanamsa, Ayanamsa):
        raise TypeError("ayanamsa must be an Ayanamsa.")

    longitude = (planet.longitude - ayanamsa.value) % 360.0

    return SiderealPlanetPosition(
        longitude=longitude,
        latitude=planet.latitude,
        distance=planet.distance,
        speed_longitude=planet.speed_longitude,
        speed_latitude=planet.speed_latitude,
        speed_distance=planet.speed_distance,
    )