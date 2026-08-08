"""
Zodiac Sign Utilities
"""

from engine.astrology.longitude_utils import (
    division_index,
    normalize_longitude,
)


def zodiac_sign(longitude: float) -> int:
    """
    Return zodiac sign number (1-12).

    Aries = 1
    Taurus = 2
    ...
    Pisces = 12

    Uses the project boundary convention (see
    engine.astrology.longitude_utils): exact sign boundaries
    belong to the next sign, and tiny negative inputs normalize
    to 0 degrees Aries.
    """
    longitude = normalize_longitude(longitude)

    return division_index(longitude, 30.0, 12) + 1
