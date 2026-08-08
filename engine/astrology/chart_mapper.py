"""
Chart Mapping Utilities
"""

from engine.astrology.planet_mapper import map_planet
from engine.models.astronomy_snapshot import AstronomySnapshot


def map_chart(snapshot: AstronomySnapshot) -> list[dict]:
    """
    Map every sidereal planet into
    sign, degree and house.
    """

    ascendant = snapshot.houses.ascendant

    return [
        map_planet(
            longitude=planet.longitude,
            ascendant=ascendant,
        )
        for planet in snapshot.sidereal_planets.values()
    ]