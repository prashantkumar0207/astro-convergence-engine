"""
KP chart assembly (KP_CHAIN_V1, ADR-0006).

Methodology isolation (lock sign-off, 2026-08-08): KP work MUST use
the KP_KRISHNAMURTI profile explicitly. This module therefore never
accepts a profile parameter on the public entry point; it computes
its own snapshot under KP_KRISHNAMURTI, and the snapshot-level entry
point verifies provenance and rejects anything else (Decision KP-B:
mean node is asserted, matching the certified legacy KP profile).
"""

import swisseph as swe

from engine.astronomy.profile import KP_KRISHNAMURTI, NODE_POLICY_MEAN
from engine.calculations.calculations import calculate
from engine.kp.chain import kp_chain
from engine.models.birth_data import BirthData
from engine.models.kp_chart import KpBody, KpChart, KpCusp

#: Bodies carried on a KP chart, in the certified legacy kernel order:
#: the nine classical grahas plus the outer planets.
KP_CHART_BODIES = (
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
    "Rahu", "Ketu", "Uranus", "Neptune", "Pluto",
)


class KpProfileError(ValueError):
    """Raised when KP assembly is attempted on a non-KP snapshot."""


def kp_chart_from_snapshot(snapshot) -> KpChart:
    """
    Attach KP chains to an existing snapshot.

    The snapshot MUST have been computed under KP_KRISHNAMURTI with
    the mean node policy; anything else raises KpProfileError
    (cross-system snapshot reuse is forbidden by the lock).
    """

    provenance = snapshot.provenance
    if provenance is None:
        raise KpProfileError("snapshot carries no provenance; KP requires it")
    if provenance.profile_name != KP_KRISHNAMURTI.name:
        raise KpProfileError(
            "KP requires the kp_krishnamurti profile, got "
            f"'{provenance.profile_name}'"
        )
    if provenance.ayanamsa_mode != swe.SIDM_KRISHNAMURTI:
        raise KpProfileError("KP requires the Krishnamurti ayanamsa")
    if provenance.node_policy != NODE_POLICY_MEAN:
        raise KpProfileError("KP requires the mean node (Decision KP-B)")

    bodies = []
    for name in KP_CHART_BODIES:
        position = snapshot.sidereal_planets[name]
        bodies.append(
            KpBody(
                name=name,
                longitude=position.longitude,
                speed_longitude=position.speed_longitude,
                retrograde=position.speed_longitude < 0,
                chain=kp_chain(position.longitude),
            )
        )

    cusps = tuple(
        KpCusp(number=index, longitude=longitude, chain=kp_chain(longitude))
        for index, longitude in enumerate(snapshot.houses.houses[:12], start=1)
    )

    ascendant_longitude = snapshot.houses.ascendant
    ascendant = KpBody(
        name="Ascendant",
        longitude=ascendant_longitude,
        speed_longitude=0.0,
        retrograde=False,
        chain=kp_chain(ascendant_longitude),
    )

    return KpChart(
        julian_day=snapshot.julian_day,
        bodies=tuple(bodies),
        cusps=cusps,
        ascendant=ascendant,
        provenance=provenance,
    )


def kp_chart(birth_data: BirthData) -> KpChart:
    """
    Full validated pipeline from BirthData to a KP fact chart under
    the ratified KP_KRISHNAMURTI profile.
    """

    result = calculate(birth_data, profile=KP_KRISHNAMURTI)
    return kp_chart_from_snapshot(result.snapshot)
