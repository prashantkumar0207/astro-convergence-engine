"""
D3 Drekkana: first production varga through the generic registry
(VARGA_D3_V1, ADR-VARGA-D3-001).

Classical source (Decision VD-A): Brihat Parashara Hora Shastra,
drekkana description: each sign divides into three equal parts of 10
degrees; the first drekkana belongs to the sign itself, the second to
the FIFTH sign from it, the third to the NINTH sign from it (the
trines: all three targets share the source sign's element). Only
this Parashara variant is certified; Jagannatha, Somnath, and
parivritti drekkanas are explicit non-claims.

Rule shape: the framework's CyclicVargaRule steps ONE sign per
division, which cannot express the drekkana's four-sign jumps, so
the rule is a SegmentVargaRule: per source sign, three explicit
10-degree segments with literal target signs. Tables, not functions,
per the framework ADR: every cell below is written out and verified
cell by cell against a second independent transcription and an
in-test re-derivation from the trine rule.

Boundary policy (Decision VD-B): inherited unchanged from the locked
framework classifier (normalization, 1e-10 promote-up, [start, end)
ownership, top clamp). No new policy exists here.

Registration (Decision VD-C): importing this module registers the
rule under (division 3, school "parashara"). Registration is proven
non-invasive: D1/D9/D10 dispatch remains hard-wired to the certified
modules (the registry refuses those divisions by contract), and every
other varga keeps raising UnsupportedVargaError.
"""

from engine.astrology.varga_registry import (
    register_varga_rule,
    registered_vargas,
)
from engine.astrology.varga_rules import SegmentVargaRule

#: 0-based signs: 0 Aries, 1 Taurus, 2 Gemini, 3 Cancer, 4 Leo,
#: 5 Virgo, 6 Libra, 7 Scorpio, 8 Sagittarius, 9 Capricorn,
#: 10 Aquarius, 11 Pisces.
D3_PARASHARA = SegmentVargaRule(segments=(
    ((10.0, 0), (10.0, 4), (10.0, 8)),    # Aries: Aries, Leo, Sagittarius
    ((10.0, 1), (10.0, 5), (10.0, 9)),    # Taurus: Taurus, Virgo, Capricorn
    ((10.0, 2), (10.0, 6), (10.0, 10)),   # Gemini: Gemini, Libra, Aquarius
    ((10.0, 3), (10.0, 7), (10.0, 11)),   # Cancer: Cancer, Scorpio, Pisces
    ((10.0, 4), (10.0, 8), (10.0, 0)),    # Leo: Leo, Sagittarius, Aries
    ((10.0, 5), (10.0, 9), (10.0, 1)),    # Virgo: Virgo, Capricorn, Taurus
    ((10.0, 6), (10.0, 10), (10.0, 2)),   # Libra: Libra, Aquarius, Gemini
    ((10.0, 7), (10.0, 11), (10.0, 3)),   # Scorpio: Scorpio, Pisces, Cancer
    ((10.0, 8), (10.0, 0), (10.0, 4)),    # Sagittarius: Sagittarius, Aries, Leo
    ((10.0, 9), (10.0, 1), (10.0, 5)),    # Capricorn: Capricorn, Taurus, Virgo
    ((10.0, 10), (10.0, 2), (10.0, 6)),   # Aquarius: Aquarius, Gemini, Libra
    ((10.0, 11), (10.0, 3), (10.0, 7)),   # Pisces: Pisces, Cancer, Scorpio
))

D3_SCHOOL = "parashara"


def ensure_registered() -> None:
    """Register D3 Parashara if not already present (idempotent)."""

    if (3, D3_SCHOOL) not in registered_vargas():
        register_varga_rule(3, D3_SCHOOL, D3_PARASHARA)


ensure_registered()
