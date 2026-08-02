"""
Pada Utilities
"""


def pada(longitude: float) -> int:
    """
    Returns Pada number (1-4).
    """
    part = longitude % (360 / 27)
    return int(part // (360 / 108)) + 1