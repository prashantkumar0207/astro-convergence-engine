"""
Vimshottari dasha timeline models (VIMSHOTTARI_V1, ADR-DASHA-001).

Exact rational bookkeeping: every period carries its start and end as
EXACT year offsets (Fractions) from the first mahadasha's start; the
float Julian Days are derived views for calendar use. Lords use the
project's Vimshottari abbreviations (Ke, Ve, Su, Mo, Ma, Ra, Ju, Sa,
Me).
"""

from dataclasses import dataclass
from fractions import Fraction

from engine.models.provenance import Provenance


@dataclass(frozen=True, slots=True)
class DashaPeriod:
    """
    One period at any depth.

    lords is the chain from mahadasha downward: ("Ke",) for a
    mahadasha, ("Ke", "Ve") for an antardasha, ("Ke", "Ve", "Su")
    for a pratyantardasha. level == len(lords).
    """

    level: int
    lords: tuple
    start_years: Fraction
    end_years: Fraction
    start_jd: float
    end_jd: float

    @property
    def lord(self) -> str:
        return self.lords[-1]

    @property
    def duration_years(self) -> Fraction:
        return self.end_years - self.start_years


@dataclass(frozen=True, slots=True)
class VimshottariTimeline:
    """
    Complete Vimshottari timeline (one full 120-year cycle from the
    birth mahadasha's start).

    school records which astrological system's profile seeded the
    Moon ("parashari" or "kp"); dasha_profile_name and
    year_length_days record the timing convention (Decision DA-A);
    seed_* record the exact classification that anchored the cycle;
    balance_years is the remaining portion of the first mahadasha at
    birth (exact).
    """

    school: str
    dasha_profile_name: str
    year_length_days: Fraction

    birth_jd: float
    anchor_jd: float

    seed_moon_longitude: float
    seed_nakshatra_number: int
    seed_lord: str
    seed_elapsed_fraction: Fraction
    balance_years: Fraction

    periods: tuple
    provenance: Provenance

    def mahadashas(self) -> tuple:
        return tuple(p for p in self.periods if p.level == 1)

    def antardashas(self) -> tuple:
        return tuple(p for p in self.periods if p.level == 2)

    def pratyantardashas(self) -> tuple:
        return tuple(p for p in self.periods if p.level == 3)
