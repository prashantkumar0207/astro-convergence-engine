"""
Degree Utilities
"""


def degree_in_sign(longitude: float) -> float:
    """
    Returns longitude within its zodiac sign.

    Examples:
        35° -> 5°
        182° -> 2°
    """
    return longitude % 30.0