"""
Aspect Engine

Computes deterministic angular separation between two
planetary longitudes.

Contains no astrological interpretation.
"""

from engine.models.aspect import Aspect


def aspect(
    body1: int,
    longitude1: float,
    body2: int,
    longitude2: float,
) -> Aspect:
    """
    Compute angular separation between two planets.
    """

    difference = abs(longitude1 - longitude2)

    if difference > 180:
        difference = 360 - difference

    return Aspect(
        body1=body1,
        body2=body2,
        angle=difference,
    )