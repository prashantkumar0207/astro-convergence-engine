"""
Astronomy Snapshot Model

Immutable deterministic astronomical snapshot.

Contains no astrological interpretation.
"""

from dataclasses import dataclass

from .planet_collection import PlanetCollection
from .house_position import HousePosition
from .ayanamsa import Ayanamsa
from .sidereal_planet_position import SiderealPlanetPosition


@dataclass(frozen=True)
class AstronomySnapshot:
    """
    Complete deterministic astronomical snapshot.
    """

    julian_day: float

    planets: PlanetCollection

    houses: HousePosition

    ayanamsa: Ayanamsa

    sidereal_planets: dict[str, SiderealPlanetPosition]