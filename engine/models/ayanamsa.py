"""
Ayanamsa Model

Immutable data model representing the sidereal offset
returned by the Swiss Ephemeris.

Contains no astrological interpretation.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Ayanamsa:
    """
    Deterministic sidereal offset.

    Attributes
    ----------
    value
        Ayanamsa in degrees.

    mode
        Swiss Ephemeris sidereal mode used
        (example: Lahiri, Raman, KP).
    """

    value: float
    mode: int