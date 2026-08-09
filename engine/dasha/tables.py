"""
Vimshottari dasha tables (VIMSHOTTARI_V1, ADR-0007).

Classical source: Brihat Parashara Hora Shastra (Vimshottari
adhyaya): lord sequence Ketu, Venus, Sun, Moon, Mars, Rahu, Jupiter,
Saturn, Mercury with years 7, 20, 6, 10, 7, 18, 16, 19, 17 (total
120), mapped to nakshatras cyclically from Ashwini = Ketu.

Deliberately a SEPARATE copy from engine/kp/tables.py (school
isolation: the dasha layer must not import the KP layer); equality of
the two tables is enforced by a cross-consistency test, never by a
cross-import.
"""

from fractions import Fraction

#: Vimshottari lord cycle, dasha order from Ketu (KP-style abbreviations).
DASHA_LORDS = ("Ke", "Ve", "Su", "Mo", "Ma", "Ra", "Ju", "Sa", "Me")

#: Vimshottari years per lord, aligned with DASHA_LORDS.
DASHA_YEARS = (7, 20, 6, 10, 7, 18, 16, 19, 17)

#: Total Vimshottari cycle in years.
TOTAL_YEARS = 120

#: Exact nakshatra span: 13 deg 20 min = 40/3 degrees.
NAK_SPAN = Fraction(40, 3)

YEARS_BY_LORD = dict(zip(DASHA_LORDS, DASHA_YEARS))


def _validate() -> None:
    if len(DASHA_LORDS) != 9 or len(DASHA_YEARS) != 9:
        raise AssertionError("Vimshottari tables must have 9 entries")
    if sum(DASHA_YEARS) != TOTAL_YEARS:
        raise AssertionError("Vimshottari years must sum to 120")


_validate()
