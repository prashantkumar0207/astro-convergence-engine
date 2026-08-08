"""
Varga Mirror Tables (Phase B of the Generic Varga Architecture ADR)

VERIFICATION ARTIFACTS ONLY. These tables express the certified D9
and D10 rules as explicit CyclicVargaRule data so the generic
classifier can be PROVEN equivalent to the certified modules. They
are:

- NOT registered in the varga registry (which structurally refuses
  divisions 9 and 10);
- NOT reachable from the dispatcher;
- NOT a production calculation path.

engine/astrology/navamsa_chart.py and dashamsa_chart.py remain the
production authority for D9 and D10. Any future cutover is ADR
Phase C, gated by the full Tier-0 lock battery, and explicitly not
performed here.

The tables below are hand-derived from the classical rules and
written as LITERALS, cell by cell, because the table itself is the
artifact under verification (ADR decision: data, not functions; the
original D10 defect was a wrong start-sign function).

D9 Navamsa (Parashara): the first navamsa of a
- movable sign (Aries, Cancer, Libra, Capricorn) is the sign itself;
- fixed sign (Taurus, Leo, Scorpio, Aquarius) is the 9th sign from it;
- dual sign (Gemini, Virgo, Sagittarius, Pisces) is the 5th sign
  from it.

D10 Dashamsa (Traditional Parashara): the first dashamsa of an
- odd sign (Aries, Gemini, Leo, Libra, Sagittarius, Aquarius; 0-based
  even indices) is the sign itself;
- even sign (Taurus, Cancer, Virgo, Scorpio, Capricorn, Pisces;
  0-based odd indices) is the 9th sign from it.

Sign indices are 0-based (0 = Aries ... 11 = Pisces), matching the
certified modules.
"""

from engine.astrology.varga_rules import CyclicVargaRule


#: D9 start-sign table, one literal per source sign:
#:   Aries       -> Aries (0)      movable, itself
#:   Taurus      -> Capricorn (9)  fixed, 9th from Taurus
#:   Gemini      -> Libra (6)      dual, 5th from Gemini
#:   Cancer      -> Cancer (3)     movable, itself
#:   Leo         -> Aries (0)      fixed, 9th from Leo
#:   Virgo       -> Capricorn (9)  dual, 5th from Virgo
#:   Libra       -> Libra (6)      movable, itself
#:   Scorpio     -> Cancer (3)     fixed, 9th from Scorpio
#:   Sagittarius -> Aries (0)      dual, 5th from Sagittarius
#:   Capricorn   -> Capricorn (9)  movable, itself
#:   Aquarius    -> Libra (6)      fixed, 9th from Aquarius
#:   Pisces      -> Cancer (3)     dual, 5th from Pisces
D9_PARASHARA_MIRROR = CyclicVargaRule(
    divisions=9,
    start_sign=(0, 9, 6, 3, 0, 9, 6, 3, 0, 9, 6, 3),
)


#: D10 start-sign table, one literal per source sign:
#:   Aries       -> Aries (0)       odd, itself
#:   Taurus      -> Capricorn (9)   even, 9th from Taurus
#:   Gemini      -> Gemini (2)      odd, itself
#:   Cancer      -> Pisces (11)     even, 9th from Cancer
#:   Leo         -> Leo (4)         odd, itself
#:   Virgo       -> Taurus (1)      even, 9th from Virgo
#:   Libra       -> Libra (6)       odd, itself
#:   Scorpio     -> Cancer (3)      even, 9th from Scorpio
#:   Sagittarius -> Sagittarius (8) odd, itself
#:   Capricorn   -> Virgo (5)       even, 9th from Capricorn
#:   Aquarius    -> Aquarius (10)   odd, itself
#:   Pisces      -> Scorpio (7)     even, 9th from Pisces
D10_PARASHARA_MIRROR = CyclicVargaRule(
    divisions=10,
    start_sign=(0, 9, 2, 11, 4, 1, 6, 3, 8, 5, 10, 7),
)
