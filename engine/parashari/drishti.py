"""
Parashari graha drishti, full aspects (PARASHARI_DRISHTI_V1,
ADR-ASPECT-PAR-001).

Classical source: Brihat Parashara Hora Shastra, drishti adhyaya,
purna (full) aspects: every graha aspects the seventh sign from its
own; Mars additionally the fourth and eighth; Jupiter the fifth and
ninth; Saturn the third and tenth. Counting is inclusive whole-sign
counting from the aspecting planet's occupied sign (Decision AS-C,
consistent with the certified D1 house rule).

Scope decisions (approved 2026-08-09): full aspects only, fractional
sputa drishti deferred (AS-A); Rahu/Ketu cast NO aspects in V1
(AS-B; the tradition variant, including the external oracle's
7th-aspect-for-nodes convention, is recorded as a non-claim); the
outer planets are outside the classical drishti system entirely.

Methodology isolation: this is Parashari-school code; snapshots must
carry the parashari_lahiri profile.
"""

import swisseph as swe

from engine.astrology.signs import zodiac_sign
from engine.astronomy.profile import PARASHARI_LAHIRI
from engine.calculations.calculations import calculate
from engine.models.birth_data import BirthData
from engine.models.drishti import DrishtiChart, PlanetDrishti

#: Frozen full-aspect offsets (inclusive counting: 7 means the
#: seventh sign counting the planet's own sign as first).
DRISHTI_OFFSETS = {
    "Sun": (7,),
    "Moon": (7,),
    "Mars": (4, 7, 8),
    "Mercury": (7,),
    "Jupiter": (5, 7, 9),
    "Venus": (7,),
    "Saturn": (3, 7, 10),
}

#: Grahas that can BE aspected (occupy signs in the classical system).
ASPECTABLE_GRAHAS = (
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
    "Rahu", "Ketu",
)


class ParashariProfileError(ValueError):
    """Raised when drishti is requested from a non-Parashari snapshot."""


def aspected_signs(planet: str, sign_number: int) -> tuple:
    """1-based signs fully aspected by ``planet`` occupying ``sign_number``."""

    offsets = DRISHTI_OFFSETS[planet]
    return tuple(((sign_number - 1) + (offset - 1)) % 12 + 1 for offset in offsets)


def graha_drishti_from_snapshot(snapshot) -> DrishtiChart:
    """Compute full-aspect facts from a certified Parashari snapshot."""

    provenance = snapshot.provenance
    if provenance is None:
        raise ParashariProfileError("snapshot carries no provenance")
    if provenance.profile_name != PARASHARI_LAHIRI.name:
        raise ParashariProfileError(
            "Parashari drishti requires the parashari_lahiri profile, got "
            f"'{provenance.profile_name}'"
        )
    if provenance.ayanamsa_mode != swe.SIDM_LAHIRI:
        raise ParashariProfileError("snapshot ayanamsa does not match Parashari")

    planet_signs = {
        name: zodiac_sign(snapshot.sidereal_planets[name].longitude)
        for name in ASPECTABLE_GRAHAS
    }
    ascendant_sign = zodiac_sign(snapshot.houses.ascendant)

    results = []
    for name, _offsets in DRISHTI_OFFSETS.items():
        own_sign = planet_signs[name]
        signs = aspected_signs(name, own_sign)
        houses = tuple(((sign - ascendant_sign) % 12) + 1 for sign in signs)
        planets = tuple(
            other for other in ASPECTABLE_GRAHAS
            if other != name and planet_signs[other] in signs
        )
        results.append(PlanetDrishti(
            name=name,
            sign_number=own_sign,
            aspected_signs=signs,
            aspected_houses=houses,
            aspected_planets=planets,
        ))

    return DrishtiChart(
        ascendant_sign=ascendant_sign,
        planet_signs=planet_signs,
        drishti=tuple(results),
        provenance=provenance,
    )


def parashari_drishti(birth_data: BirthData) -> DrishtiChart:
    """Full validated pipeline from BirthData under PARASHARI_LAHIRI."""

    result = calculate(birth_data, profile=PARASHARI_LAHIRI)
    return graha_drishti_from_snapshot(result.snapshot)
