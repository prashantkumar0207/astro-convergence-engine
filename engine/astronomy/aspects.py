"""
Aspect Engine

Computes the angular relationship between two celestial bodies.

Contains no astrological interpretation.
"""

from __future__ import annotations

from engine.models.aspect import Aspect


def aspect(
    body1: int,
    longitude1: float,
    body2: int,
    longitude2: float,
) -> Aspect:
    """
    Compute the deterministic angular separation between two bodies.
    """

    if not isinstance(body1, int):
        raise TypeError("body1 must be an integer.")

    if not isinstance(body2, int):
        raise TypeError("body2 must be an integer.")

    if not isinstance(longitude1, (int, float)):
        raise TypeError("longitude1 must be numeric.")

    if not isinstance(longitude2, (int, float)):
        raise TypeError("longitude2 must be numeric.")

    angle = abs(longitude1 - longitude2)

    if angle > 180.0:
        angle = 360.0 - angle

    return Aspect(
        body1=body1,
        body2=body2,
        angle=angle,
    )