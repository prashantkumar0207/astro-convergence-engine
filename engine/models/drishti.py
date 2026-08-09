"""
Parashari graha drishti models (PARASHARI_DRISHTI_V1, ADR-ASPECT-PAR-001).
"""

from dataclasses import dataclass

from engine.models.provenance import Provenance


@dataclass(frozen=True, slots=True)
class PlanetDrishti:
    """
    Full aspects cast by one graha.

    Signs and houses are 1-based; aspected_houses counts whole-sign
    houses from the lagna. aspected_planets lists grahas occupying
    aspected signs.
    """

    name: str
    sign_number: int
    aspected_signs: tuple
    aspected_houses: tuple
    aspected_planets: tuple


@dataclass(frozen=True, slots=True)
class DrishtiChart:
    """
    Complete graha drishti facts for one chart.

    Aspect-casting covers the seven classical grahas (Sun through
    Saturn). Rahu and Ketu cast no aspects in this certified V1
    (Decision AS-B: traditions disagree; the variant is recorded,
    never silently chosen) but can BE aspected. No strengths, yogas,
    or judgments exist here; facts only.
    """

    ascendant_sign: int
    planet_signs: dict
    drishti: tuple
    provenance: Provenance
