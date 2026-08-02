"""
Planet Mapping Utilities
"""

from engine.astrology.signs import zodiac_sign
from engine.astrology.degrees import degree_in_sign
from engine.astrology.house import house_from_longitude


def map_planet(
    longitude: float,
    ascendant: float,
) -> dict:
    """
    Map a planet's longitude into
    sign, degree within sign, and whole-sign house.
    """

    return {
        "longitude": longitude,
        "sign": zodiac_sign(longitude),
        "degree": degree_in_sign(longitude),
        "house": house_from_longitude(
            longitude,
            ascendant,
        ),
    }