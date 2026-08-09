"""
KP frozen data tables (KP_CHAIN_V1, ADR-KP-001).

Classical sources
-----------------
Lord order and years: the Vimshottari dasha sequence and durations
(Ketu 7, Venus 20, Sun 6, Moon 10, Mars 7, Rahu 18, Jupiter 16,
Saturn 19, Mercury 17; total 120 years), per Brihat Parashara Hora
Shastra (Vimshottari adhyaya) as adopted by K.S. Krishnamurti,
KP Readers I-III. KP subdivides each nakshatra (13 deg 20 min,
exactly 40/3 degrees) proportionally to these years, recursively
(sub, then sub-sub), starting each level's cycle from that
interval's own lord.

Sign lords: standard sign rulerships (BPHS; identical in KP usage):
Aries/Scorpio Mars, Taurus/Libra Venus, Gemini/Virgo Mercury,
Cancer Moon, Leo Sun, Sagittarius/Pisces Jupiter,
Capricorn/Aquarius Saturn.

These tables are migrated from the certified legacy kernel
(legacy/kp.py) and MUST NOT be edited without recertification
against it (equivalence gate, zero categorical tolerance per
DECISION_LOG D-003).

Terminology note: KP practice abbreviates lords (Ke, Ve, Su, Mo,
Ma, Ra, Ju, Sa, Me); those abbreviations are the KP layer's own
canonical tokens. KP_LORD_FULL_NAMES maps them to the engine's
canonical planet names for cross-layer consistency checks only.
"""

from fractions import Fraction

#: Vimshottari lord cycle, in dasha order starting from Ketu.
KP_LORDS = ("Ke", "Ve", "Su", "Mo", "Ma", "Ra", "Ju", "Sa", "Me")

#: Vimshottari years per lord, aligned with KP_LORDS.
KP_YEARS = (7, 20, 6, 10, 7, 18, 16, 19, 17)

#: Sign lords by 0-based sign index (Aries=0 ... Pisces=11).
KP_SIGN_LORDS = ("Ma", "Ve", "Me", "Mo", "Su", "Me",
                 "Ve", "Ma", "Ju", "Sa", "Sa", "Ju")

#: Exact nakshatra span: 13 deg 20 min = 40/3 degrees.
NAK_SPAN = Fraction(40, 3)

#: KP abbreviation -> engine canonical planet name.
KP_LORD_FULL_NAMES = {
    "Ke": "Ketu", "Ve": "Venus", "Su": "Sun", "Mo": "Moon",
    "Ma": "Mars", "Ra": "Rahu", "Ju": "Jupiter", "Sa": "Saturn",
    "Me": "Mercury",
}


def _validate() -> None:
    if len(KP_LORDS) != 9 or len(KP_YEARS) != 9:
        raise AssertionError("KP lord/year tables must have 9 entries")
    if sum(KP_YEARS) != 120:
        raise AssertionError("Vimshottari years must sum to 120")
    if len(KP_SIGN_LORDS) != 12:
        raise AssertionError("sign lord table must have 12 entries")
    if set(KP_SIGN_LORDS) - set(KP_LORDS):
        raise AssertionError("sign lord not in lord roster")
    if set(KP_LORD_FULL_NAMES) != set(KP_LORDS):
        raise AssertionError("full-name map must cover exactly the lords")


_validate()
