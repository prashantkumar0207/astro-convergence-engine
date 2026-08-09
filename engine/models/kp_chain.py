"""
KP lordship chain result model (KP_CHAIN_V1, ADR-KP-001).

Lords are KP abbreviations (Ke, Ve, Su, Mo, Ma, Ra, Ju, Sa, Me);
see engine/kp/tables.py for the mapping to engine planet names.
Nakshatra names use the engine's canonical spellings
(engine/astrology/nakshatra_names.py) so the project has a single
naming authority; the lordship logic itself is purely index-based.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class KpChain:
    """
    KP hierarchy for one sidereal longitude.

    Attributes
    ----------
    sign_number
        Sign, 1-12 (Aries=1).
    sign_name
        Sign name.
    sign_lord
        SL: lord of the sign (KP abbreviation).
    nakshatra_number
        Nakshatra, 1-27 (Ashwini=1).
    nakshatra_name
        Canonical engine nakshatra name.
    nakshatra_lord
        NL (star lord): Vimshottari lord of the nakshatra.
    sub_lord
        SB: KP sub lord.
    sub_sub_lord
        SS: KP sub-sub lord.
    nearest_boundary_arcsec
        Distance to the closest owning-interval boundary at any
        level, in arcseconds. Small values mean the classification
        is boundary-critical and upstream longitude precision
        dominates the result.
    """

    sign_number: int
    sign_name: str
    sign_lord: str

    nakshatra_number: int
    nakshatra_name: str
    nakshatra_lord: str

    sub_lord: str
    sub_sub_lord: str

    nearest_boundary_arcsec: float

    @property
    def sign_zero_based(self) -> int:
        """
        The 0-based index of :attr:`sign_number`.

        :attr:`sign_number` is 1-based and CERTIFIED; this accessor is
        additive (ADR-CONVENTION-001, Decision SC-B) and changes no
        stored value.
        """

        return self.sign_number - 1

    @property
    def sign_object(self):
        """:attr:`sign_number` as an explicit Sign (ADR-CONVENTION-001)."""

        from engine.astrology.sign import Sign

        return Sign.from_one_based(self.sign_number)
