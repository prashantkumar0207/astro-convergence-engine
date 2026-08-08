"""
Astronomy Snapshot Model

Immutable deterministic astronomical snapshot.

Contains no astrological interpretation.
"""

from dataclasses import dataclass

from .planet_collection import PlanetCollection
from .house_position import HousePosition
from .ayanamsa import Ayanamsa
from .provenance import Provenance
from .sidereal_planet_position import SiderealPlanetPosition


@dataclass(frozen=True)
class AstronomySnapshot:
    """
    Complete deterministic astronomical snapshot.

    Attributes
    ----------
    julian_day
        Julian Day in UT (derived from UTC; see Provenance).

    planets
        Tropical positions for all supported bodies.

    houses
        House geometry. In the production pipeline this is
        SIDEREAL (houses.frame == "sidereal").

    ayanamsa
        The sidereal offset that was applied, with its mode.

    sidereal_planets
        Sidereal positions keyed by canonical planet name.

    provenance
        How this snapshot was computed (profile, frame, ayanamsa,
        house system, ephemeris mode). Optional only for synthetic
        test fixtures; the production pipeline always sets it.
    """

    julian_day: float

    planets: PlanetCollection

    houses: HousePosition

    ayanamsa: Ayanamsa

    sidereal_planets: dict[str, SiderealPlanetPosition]

    provenance: Provenance | None = None