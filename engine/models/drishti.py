"""
Parashari graha drishti models (PARASHARI_DRISHTI_V1, ADR-0012).
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

    @property
    def sign_zero_based(self) -> int:
        """
        The 0-based index of :attr:`sign_number`.

        :attr:`sign_number` is 1-based and CERTIFIED; this accessor is
        additive (ADR-0012, Decision SC-B) and changes no
        stored value.
        """

        return self.sign_number - 1

    @property
    def sign_object(self):
        """:attr:`sign_number` as an explicit Sign (ADR-0012)."""

        from engine.astrology.sign import Sign

        return Sign.from_one_based(self.sign_number)

    @property
    def aspected_signs_zero_based(self) -> tuple:
        """:attr:`aspected_signs` (1-based, certified) as 0-based indexes."""

        return tuple(sign - 1 for sign in self.aspected_signs)


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

    @property
    def ascendant_sign_zero_based(self) -> int:
        """
        The 0-based index of :attr:`ascendant_sign`.

        :attr:`ascendant_sign` is 1-based and CERTIFIED; this accessor is
        additive (ADR-0012, Decision SC-B) and changes no
        stored value.
        """

        return self.ascendant_sign - 1

    @property
    def ascendant_sign_object(self):
        """:attr:`ascendant_sign` as an explicit Sign (ADR-0012)."""

        from engine.astrology.sign import Sign

        return Sign.from_one_based(self.ascendant_sign)
