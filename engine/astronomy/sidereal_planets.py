"""
Sidereal Planet Engine

Produces sidereal planetary positions.

Contains no astrological interpretation.

Convention note (audit remediation, F-01 follow-up): the Swiss
Ephemeris FLG_SIDEREAL computation is the authoritative sidereal
convention in this project. It matches the certified legacy kernel
and the independent swetest reference binary to sub-milliarcsecond
level. Subtracting the ayanamsa from a TRUE tropical longitude
differs from it by the nutation-related term (measured 9.57 arcsec
at JD 2447719.968), which is far above the frozen 0.5 arcsec
tolerance. The arithmetic form is therefore retained only as a
documented approximation for synthetic fixtures.
"""

from __future__ import annotations

import swisseph as swe

from engine.astronomy.ephemeris import calc_ut_checked
from engine.models.ayanamsa import Ayanamsa
from engine.models.planet_position import PlanetPosition
from engine.models.sidereal_planet_position import SiderealPlanetPosition


def sidereal_planet_position(
    julian_day: float,
    body: int,
    mode: int,
    strict: bool = True,
) -> SiderealPlanetPosition:
    """
    Compute a sidereal position directly via Swiss FLG_SIDEREAL.

    The caller must supply the sidereal mode explicitly; it is set
    before computation, so the result does not depend on ambient
    process state.
    """

    swe.set_sid_mode(mode)

    values, _mode = calc_ut_checked(
        julian_day,
        body,
        swe.FLG_SWIEPH | swe.FLG_SPEED | swe.FLG_SIDEREAL,
        strict=strict,
    )

    return SiderealPlanetPosition(
        longitude=values[0],
        latitude=values[1],
        distance=values[2],
        speed_longitude=values[3],
        speed_latitude=values[4],
        speed_distance=values[5],
    )


def sidereal_planet_collection(
    julian_day: float,
    mode: int,
    node_policy: str = "mean",
    strict: bool = True,
) -> dict[str, SiderealPlanetPosition]:
    """
    Compute sidereal positions for all supported bodies, including
    the canonical Rahu/Ketu pair (Ketu derived as Rahu + 180 with
    Rahu's speed; see engine.astronomy.planet_collection).
    """

    from engine.astronomy.planet_collection import PLANET_BODIES

    sidereal = {
        name: sidereal_planet_position(julian_day, body, mode, strict)
        for name, body in PLANET_BODIES.items()
    }

    rahu = sidereal["MeanNode" if node_policy == "mean" else "TrueNode"]

    sidereal["Rahu"] = rahu
    sidereal["Ketu"] = SiderealPlanetPosition(
        longitude=(rahu.longitude + 180.0) % 360.0,
        latitude=-rahu.latitude,
        distance=rahu.distance,
        speed_longitude=rahu.speed_longitude,
        speed_latitude=-rahu.speed_latitude,
        speed_distance=rahu.speed_distance,
    )

    return sidereal


def sidereal_planet(
    tropical: PlanetPosition,
    ayanamsa: Ayanamsa,
) -> SiderealPlanetPosition:
    """
    APPROXIMATION ONLY: convert a tropical position to sidereal by
    subtracting the ayanamsa.

    This omits the nutation-related difference (~10 arcsec) between
    plain subtraction and the authoritative FLG_SIDEREAL result.
    The production pipeline does NOT use this function; it exists
    for synthetic fixtures and educational comparison.
    """

    longitude = (tropical.longitude - ayanamsa.value) % 360.0

    return SiderealPlanetPosition(
        longitude=longitude,
        latitude=tropical.latitude,
        distance=tropical.distance,
        speed_longitude=tropical.speed_longitude,
        speed_latitude=tropical.speed_latitude,
        speed_distance=tropical.speed_distance,
    )
