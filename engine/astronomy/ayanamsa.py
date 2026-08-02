"""
Ayanamsa Engine

Computes the sidereal offset using the configured
Swiss Ephemeris sidereal mode.

Contains no astrological interpretation.
"""

from __future__ import annotations

import swisseph as swe

from engine.models.ayanamsa import Ayanamsa


DEFAULT_SIDEREAL_MODE = swe.SIDM_LAHIRI


def ayanamsa(
    julian_day: float,
    mode: int = DEFAULT_SIDEREAL_MODE,
) -> Ayanamsa:
    """
    Compute the ayanamsa for a Julian Day.
    """

    if not isinstance(julian_day, (int, float)):
        raise TypeError("julian_day must be numeric.")

    if not isinstance(mode, int):
        raise TypeError("mode must be an integer.")

    swe.set_sid_mode(mode)

    value = swe.get_ayanamsa_ut(julian_day)

    return Ayanamsa(
        value=value,
        mode=mode,
    )