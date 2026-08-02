"""
House Utilities
"""


def house_from_longitude(
    longitude: float,
    ascendant: float,
) -> int:
    """
    Determine the whole-sign house number from a longitude
    relative to the Ascendant.

    Returns a value from 1 to 12.
    """
    longitude %= 360.0
    ascendant %= 360.0

    diff = (longitude - ascendant) % 360.0

    return int(diff // 30.0) + 1