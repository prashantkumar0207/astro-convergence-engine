"""
Aspect Model

Represents a deterministic angular relationship between two
celestial bodies.

Contains no astrological interpretation.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Aspect:
    """
    Deterministic aspect between two planets.
    """

    body1: int
    body2: int
    angle: float