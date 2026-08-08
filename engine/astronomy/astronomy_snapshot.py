"""
Astronomy Snapshot Engine

Builds a complete deterministic astronomical snapshot
from the lower-level astronomy engines.

Contains no astrological interpretation.

Frame policy (remediates audit finding F-01): every ecliptic
longitude in the snapshot, planets AND houses AND ascendant, is
SIDEREAL under the profile's ayanamsa. Houses are computed by the
Swiss Ephemeris with FLG_SIDEREAL (matching the certified legacy
kernel), and planets are converted from tropical by subtracting
the ayanamsa; each value is transformed exactly once.

The ayanamsa is computed FIRST because swe.set_sid_mode is
process-global state that the sidereal house computation depends
on. This ordering is load-bearing; do not reorder.
"""

from __future__ import annotations

import swisseph as swe

from engine.astronomy.ayanamsa import ayanamsa
from engine.astronomy.ephemeris import MODE_SWIEPH, initialize_ephemeris
from engine.astronomy.house_positions import house_positions
from engine.astronomy.planet_collection import planet_collection
from engine.astronomy.profile import DEFAULT_PROFILE, CalculationProfile
from engine.astronomy.sidereal_planets import sidereal_planet_collection
from engine.models.astronomy_snapshot import AstronomySnapshot
from engine.models.provenance import Provenance


def astronomy_snapshot(
    julian_day: float,
    latitude: float,
    longitude: float,
    profile: CalculationProfile = DEFAULT_PROFILE,
):
    """
    Build a deterministic astronomical snapshot for a profile.

    All longitudes in the returned snapshot are sidereal under
    profile.ayanamsa_mode. The snapshot carries Provenance so the
    facts are self-describing (audit finding F-20).
    """

    initialize_ephemeris()

    # 1. Ayanamsa first: sets the process sidereal mode used by the
    #    sidereal house computation below.
    aya = ayanamsa(julian_day, mode=profile.ayanamsa_mode)

    # 2. Sidereal houses and angles (F-01 fix): FLG_SIDEREAL, same
    #    mechanism as the certified legacy kernel.
    houses = house_positions(
        julian_day=julian_day,
        latitude=latitude,
        longitude=longitude,
        house_system=profile.house_system,
        flags=swe.FLG_SIDEREAL,
    )

    # 3. Tropical planets, plus authoritative sidereal positions
    #    computed directly with FLG_SIDEREAL (the certified
    #    convention; see engine.astronomy.sidereal_planets).
    planets = planet_collection(julian_day, node_policy=profile.node_policy)

    sidereal = sidereal_planet_collection(
        julian_day,
        mode=profile.ayanamsa_mode,
        node_policy=profile.node_policy,
        strict=profile.strict_ephemeris,
    )

    provenance = Provenance(
        profile_name=profile.name,
        ayanamsa_mode=profile.ayanamsa_mode,
        frame="sidereal",
        house_system=profile.house_system.decode("ascii"),
        node_policy=profile.node_policy,
        ephemeris_mode=MODE_SWIEPH if profile.strict_ephemeris else "unverified",
    )

    return AstronomySnapshot(
        julian_day=julian_day,
        planets=planets,
        houses=houses,
        ayanamsa=aya,
        sidereal_planets=sidereal,
        provenance=provenance,
    )
