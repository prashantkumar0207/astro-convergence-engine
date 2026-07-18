"""
Planet Collection Model

Immutable collection of deterministic planetary positions.

Contains no astrological interpretation.
"""

from dataclasses import dataclass

from .planet_position import PlanetPosition


@dataclass(frozen=True)
class PlanetCollection:
    """
    Collection of deterministic tropical planetary positions.
    """

    planets: dict[str, PlanetPosition]