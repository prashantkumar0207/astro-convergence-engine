"""
Vimshottari dasha timeline models (VIMSHOTTARI_V1, ADR-0007).

Exact rational bookkeeping: every period carries its start and end as
EXACT year offsets (Fractions) from the first mahadasha's start; the
float Julian Days are derived views for calendar use. Lords use the
project's Vimshottari abbreviations (Ke, Ve, Su, Mo, Ma, Ra, Ju, Sa,
Me).
"""

from dataclasses import dataclass
from fractions import Fraction

from engine.models.provenance import Provenance

#: Value for `VimshottariTimeline.seed_boundary_convention` (H-08, DP-018
#: Option 3, ADR-0071): seed nakshatra classification used the KP layer's
#: exact [start, end) boundary-ownership rule (Decimal(str(x)), no
#: float-noise tolerance) - the same rule and cardinality contract as
#: `engine.kp.intervals`. This is currently the ONLY convention
#: VIMSHOTTARI_V1 uses, for every seeding school including Parashari - a
#: deliberate, ratified choice (`ADR-0071`), not an accidental leak. It
#: can differ from what `engine.astrology.nakshatra.nakshatra()` (the
#: Parashari engine's own, differently-tolerant classifier) reports for
#: the identical longitude, at six documented boundary floats; see
#: `engine/tests/test_vimshottari_h08_boundary_convention.py`, which pins
#: exactly where and why. This field exists so a consumer can see which
#: convention produced `seed_nakshatra_number` without re-deriving it -
#: mirroring `engine.models.transit_event.TransitEvent.declared_division`
#: (H-02, `ADR-0065`).
SEED_BOUNDARY_CONVENTION_KP_EXACT = "kp_exact_start_end"


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
    birth (exact); seed_boundary_convention (H-08, ADR-0071) names
    which boundary-ownership rule produced seed_nakshatra_number.

    seed_nakshatra_boundary_arcsec (Dasha roadmap step 6, DP-020
    Option 1, ADR-0073): distance from the birth Moon to the nearest
    NAKSHATRA boundary, in arcseconds - an exact re-expression of
    seed_elapsed_fraction (min(elapsed, 1 - elapsed) * NAK_SPAN *
    3600, Fraction arithmetic until the final float step), not a new
    astronomical calculation. Scope, deliberately narrower than KP's
    own engine.models.kp_chain.KpChain.nearest_boundary_arcsec:

    - Covers ONLY the nakshatra (seed) boundary that determines
      seed_lord and therefore the entire mahadasha/antardasha/
      pratyantardasha structure. It does NOT cover deeper period-
      transition boundaries (antardasha/pratyantardasha starts and
      ends - the roadmap's own separate, unaddressed "boundaries in
      time" interval-membership problem), and it does NOT cover any
      KP-specific level (sign/sub/sub-sub) - unlike
      nearest_boundary_arcsec, whose own docstring claims coverage
      "at any level" while its implementation omits the sign
      boundary (H-07, an open, unresolved defect this field does not
      inherit because it makes no such broader claim).
    - Reports proximity only. It is NOT a dasha-date-uncertainty
      figure: no lord-specific days-per-degree amplification
      (docs/DASHA_CERTIFICATION_ROADMAP.md s1) is applied - that is
      DP-020 Option 2, explicitly not chosen.
    - MUST NOT be treated as equivalent to KP's own
      nearest_boundary_arcsec, or to scripts/certify_vimshottari.py's
      own moon_distance_to_nearest_boundary_deg certifier diagnostic
      (M-02, ADR-0072) - each is a separate signal with its own scope
      and provenance; see engine/tests/
      test_vimshottari_boundary_proximity_indicator.py.
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
    seed_nakshatra_boundary_arcsec: float
    balance_years: Fraction

    periods: tuple
    provenance: Provenance

    seed_boundary_convention: str = SEED_BOUNDARY_CONVENTION_KP_EXACT

    def mahadashas(self) -> tuple:
        return tuple(p for p in self.periods if p.level == 1)

    def antardashas(self) -> tuple:
        return tuple(p for p in self.periods if p.level == 2)

    def pratyantardashas(self) -> tuple:
        return tuple(p for p in self.periods if p.level == 3)
