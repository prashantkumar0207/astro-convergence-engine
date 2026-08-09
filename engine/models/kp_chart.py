"""
KP chart models (KP_CHAIN_V1, ADR-KP-001).

A KP chart is the KP lordship chain attached to every body, every
Placidus cusp, and the ascendant of an AstronomySnapshot computed
under the ratified KP_KRISHNAMURTI profile. Facts only; no
significators, houses-signified, or predictive content exists here.
"""

from dataclasses import dataclass

from engine.models.kp_chain import KpChain
from engine.models.provenance import Provenance


@dataclass(frozen=True, slots=True)
class KpBody:
    """One body (or the ascendant) with its KP chain."""

    name: str
    longitude: float
    speed_longitude: float
    retrograde: bool
    chain: KpChain


@dataclass(frozen=True, slots=True)
class KpCusp:
    """One Placidus house cusp with its KP chain."""

    number: int
    longitude: float
    chain: KpChain


@dataclass(frozen=True, slots=True)
class KpChart:
    """
    Complete KP fact chart.

    bodies covers the nine classical grahas plus the outer planets
    (matching the certified legacy kernel roster); ascendant is
    carried separately. provenance is the snapshot provenance and
    always records the kp_krishnamurti profile.
    """

    julian_day: float
    bodies: tuple
    cusps: tuple
    ascendant: KpBody
    provenance: Provenance
