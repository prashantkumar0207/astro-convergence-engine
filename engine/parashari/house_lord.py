"""
House lordship and whole-sign placement (PARASHARI_HOUSE_LORD_V1, ADR-0133 D3, D5; PROPOSED).

For a natal D1 chart under the PARASHARI_LAHIRI profile this module gives, for each of the twelve houses, the
house's sign, its lord, and the sign and house the lord occupies; and, for each of the nine grahas, the sign and
house it occupies. These are the facts a `house_lord_in_house`, `planet_in_house` or `planet_in_sign` rule
condition reads (engine/evidence/rule_registry.py CONDITION_SCHEMA). Nothing here evaluates a rule.

Frozen convention (ADR-0133 D3), the project's existing documented one, so no second convention is introduced:

    house_sign(h)  := ((lagna_sign - 1) + (h - 1)) mod 12 + 1     (whole-sign: the Lagna's sign is house 1)
    lord(h)        := sign_lord(house_sign(h))                    (engine.astrology.sign_lord, the seven classical lords)
    lord_house(h)  := whole_sign_house(longitude(lord(h)), lagna)  (engine.astrology.house)

Production dependencies, reused rather than duplicated: the Tier-0-Locked D1 kernel's sidereal longitudes and Lagna
(engine.calculations.calculations.calculate under PARASHARI_LAHIRI), engine.astrology.signs.zodiac_sign,
engine.astrology.house.whole_sign_house and engine.astrology.sign_lord.sign_lord.

Isolated per the school-separation rule: this module imports no drishti, KP, Jaimini or Nadi module.

Explicit non-claims: no Rahu or Ketu co-lordship of Scorpio or Aquarius (the seven classical lords only); no
bhava-chalit, equal-house or cusp-based houses; no varga other than D1; no strength, dignity or aspect; and no
interpretive or predictive claim. A house lord's placement is a calculated fact, never an indication of anything.
"""

import hashlib
from dataclasses import dataclass

import swisseph as swe

from engine.astrology.house import whole_sign_house
from engine.astrology.sign_lord import SIGN_LORDS, sign_lord
from engine.astrology.signs import zodiac_sign
from engine.astronomy.profile import PARASHARI_LAHIRI
from engine.calculations.calculations import calculate
from engine.models.birth_data import BirthData
from engine.models.provenance import Provenance

#: The nine grahas whose placement is reported, in the order the registry's condition schema names them.
PLACED_GRAHAS = ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu")
#: The twelve houses, whole-sign from the Lagna.
HOUSES = tuple(range(1, 13))


class HouseLordProfileError(ValueError):
    """Raised when house lordship is requested from a non-Parashari snapshot. Defined here, never imported from
    another Parashari module, per the school-isolation discipline."""


@dataclass(frozen=True, slots=True)
class GrahaPlacement:
    """One graha's 1-based occupied sign and its whole-sign house from the Lagna."""

    graha: str
    sign: int
    house: int


@dataclass(frozen=True, slots=True)
class HouseLordship:
    """One house: its sign, its lord, and the sign and whole-sign house the lord occupies."""

    house: int
    sign: int
    lord: str
    lord_sign: int
    lord_house: int


@dataclass(frozen=True, slots=True)
class HouseLordChart:
    """The house-lord and placement facts of one natal D1 chart, with the provenance they were computed under."""

    ascendant_sign: int
    placements: tuple
    lordships: tuple
    provenance: Provenance

    def placement(self, graha: str) -> GrahaPlacement:
        found = [item for item in self.placements if item.graha == graha]
        if len(found) != 1:
            raise KeyError(f"no placement for {graha!r}")
        return found[0]

    def lordship(self, house: int) -> HouseLordship:
        found = [item for item in self.lordships if item.house == house]
        if len(found) != 1:
            raise KeyError(f"no lordship for house {house!r}")
        return found[0]


def house_sign(house: int, ascendant_sign: int) -> int:
    """The sign of a whole-sign house: the Lagna's sign is house 1, and each following sign one house further."""

    return (ascendant_sign - 1 + house - 1) % 12 + 1


def house_lord(house: int, ascendant_sign: int) -> str:
    """The lord of a whole-sign house: the classical lord of that house's sign."""

    return sign_lord(house_sign(house, ascendant_sign))


def house_lords_from_snapshot(snapshot) -> HouseLordChart:
    """House-lord and placement facts from a certified Parashari snapshot. Refuses any other profile."""

    provenance = snapshot.provenance
    if provenance is None:
        raise HouseLordProfileError("snapshot carries no provenance")
    if provenance.profile_name != PARASHARI_LAHIRI.name:
        raise HouseLordProfileError(
            f"house lordship requires the parashari_lahiri profile, got '{provenance.profile_name}'")
    if provenance.ayanamsa_mode != swe.SIDM_LAHIRI:
        raise HouseLordProfileError("snapshot ayanamsa does not match Parashari")

    ascendant = snapshot.houses.ascendant
    ascendant_sign = zodiac_sign(ascendant)
    longitudes = {graha: snapshot.sidereal_planets[graha].longitude for graha in PLACED_GRAHAS}
    placements = tuple(GrahaPlacement(graha=graha, sign=zodiac_sign(longitudes[graha]),
                                      house=whole_sign_house(longitudes[graha], ascendant))
                       for graha in PLACED_GRAHAS)
    lordships = []
    for house in HOUSES:
        lord = house_lord(house, ascendant_sign)
        lordships.append(HouseLordship(house=house, sign=house_sign(house, ascendant_sign), lord=lord,
                                       lord_sign=zodiac_sign(longitudes[lord]),
                                       lord_house=whole_sign_house(longitudes[lord], ascendant)))
    return HouseLordChart(ascendant_sign=ascendant_sign, placements=placements, lordships=tuple(lordships),
                          provenance=provenance)


def house_lords(birth_data: BirthData) -> HouseLordChart:
    """The full validated pipeline from BirthData under PARASHARI_LAHIRI."""

    result = calculate(birth_data, profile=PARASHARI_LAHIRI)
    return house_lords_from_snapshot(result.snapshot)


def rule_content_sha256() -> str:
    """Content fingerprint of the frozen constants this capability depends on, for certification pinning. It
    includes the production sign-lord table, since this module's facts are only as right as that table."""

    payload = repr((PLACED_GRAHAS, HOUSES, sorted(SIGN_LORDS.items()))).encode()
    return hashlib.sha256(payload).hexdigest()
