"""
Zodiac Sign Utilities
"""

from math import floor


def zodiac_sign(longitude: float) -> int:
    """
    Return zodiac sign number (1-12).

    Aries = 1
    Taurus = 2
    ...
    Pisces = 12
    """
    longitude %= 360.0
    return floor(longitude / 30.0) + 1