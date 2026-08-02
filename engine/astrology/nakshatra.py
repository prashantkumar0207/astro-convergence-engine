"""
Nakshatra Utilities
"""


def nakshatra(longitude: float) -> int:
    """
    Returns Nakshatra number (1-27).
    """
    longitude %= 360.0
    return int(longitude // (360 / 27)) + 1