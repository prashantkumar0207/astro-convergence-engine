"""
Planet Collection Engine

Computes deterministic tropical positions for all supported
celestial bodies.
"""

from __future__ import annotations

import swisseph as swe

from engine.astronomy.planet_positions import planet_position
from engine.models.planet_collection import PlanetCollection


_PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO,
    "MeanNode": swe.MEAN_NODE,
    "TrueNode": swe.TRUE_NODE,
}


def planet_collection(julian_day: float) -> PlanetCollection:
    """
    Compute deterministic tropical positions
    for all supported planets.
    """

    if not isinstance(julian_day, (int, float)):
        raise TypeError("julian_day must be numeric.")

    planets = {
        name: planet_position(julian_day, body)
        for name, body in _PLANETS.items()
    }

    return PlanetCollection(planets=planets)