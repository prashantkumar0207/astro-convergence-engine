"""
Astronomy Snapshot Engine

Builds a complete deterministic astronomical snapshot
from the lower-level astronomy engines.

Contains no astrological interpretation.
"""

from __future__ import annotations

from engine.astronomy.planet_collection import planet_collection
from engine.astronomy.house_positions import house_positions
from engine.astronomy.ayanamsa import ayanamsa
from engine.astronomy.sidereal_planets import sidereal_planet

from engine.models.astronomy_snapshot import AstronomySnapshot


def astronomy_snapshot(
    julian_day: float,
    latitude: float,
    longitude: float,
):
    """
    Build a deterministic astronomical snapshot.
    """

    planets = planet_collection(julian_day)

    houses = house_positions(
        julian_day=julian_day,
        latitude=latitude,
        longitude=longitude,
    )

    aya = ayanamsa(julian_day)

    sidereal = {
        name: sidereal_planet(position, aya)
        for name, position in planets.planets.items()
    }

    return AstronomySnapshot(
        julian_day=julian_day,
        planets=planets,
        houses=houses,
        ayanamsa=aya,
        sidereal_planets=sidereal,
    )