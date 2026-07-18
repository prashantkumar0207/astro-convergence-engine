"""
Ayanamsa Engine

Computes deterministic sidereal offsets using
Swiss Ephemeris.
"""

from __future__ import annotations

import swisseph as swe

from engine.models.ayanamsa import Ayanamsa


def ayanamsa(
    julian_day: float,
    mode: int = swe.SIDM_LAHIRI,
) -> Ayanamsa:
    """
    Compute the ayanamsa for a Julian Day.

    Parameters
    ----------
    julian_day
        Julian Day in UTC.

    mode
        Swiss Ephemeris sidereal mode.

    Returns
    -------
    Ayanamsa
        Deterministic sidereal offset.
    """

    if not isinstance(julian_day, (int, float)):
        raise TypeError("julian_day must be numeric.")

    if not isinstance(mode, int):
        raise TypeError("mode must be a Swiss Ephemeris sidereal mode.")

    swe.set_sid_mode(mode)

    value = swe.get_ayanamsa_ut(julian_day)

    return Ayanamsa(
        value=value,
        mode=mode,
    )