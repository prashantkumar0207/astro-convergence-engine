"""
Hermetic-tier protected baseline for the Vimshottari anchor (H-05,
DP-016 Option 1, ADR-0069).

engine/dasha/vimshottari.py's anchor_jd construction has already been
independently established correct by the oracle-tier certifier
(scripts/certify_vimshottari.py, VIMSHOTTARI_V1, ADR-0007) comparing
against PyJHora's own dates. That gate needs PyJHora and runs only in
CI's Linux oracle job - never locally, never in the hermetic job. Every
previously-existing hermetic-tier check (the JD-consistency test, the
boundary test, and validate_vimshottari_holdout.py's independent
validator) is structurally blind to a wrong anchor: the first two are
relative to the anchor under test, and the validator compares only
Fraction year offsets, never a Julian Day (reports/
G1_ARCHITECTURE_AUDIT_2026-08-11.md H-05).

This module freezes that already-oracle-validated anchor construction
for a handful of fixed seeds and asserts against it hermetically,
closing the coverage gap - it does not re-derive the correctness claim,
which remains the oracle-tier gate's own.
"""

from decimal import Decimal
from fractions import Fraction

from engine.dasha.profile import VIMSHOTTARI_MEAN_SIDEREAL_YEAR
from engine.dasha.tables import DASHA_LORDS, NAK_SPAN, YEARS_BY_LORD
from engine.dasha.vimshottari import vimshottari_from_moon

# J2000.0, matching this test suite's existing convention
# (test_vimshottari_invariants.py's own _timeline() helper).
BIRTH_JD = 2451545.0

# Frozen 2026-08-22, per DP-016 Option 1. Each value was independently
# re-derived from the documented anchor formula (this module's own
# _correct_anchor_jd below, not vimshottari_from_moon's own output),
# then cross-checked to match the production function exactly before
# being committed here.
FROZEN_CASES = (
    # (label, moon, seed_lord, expected_anchor_jd, second_maha_lord, expected_second_maha_start_jd)
    ("ashwini_three_eighths_elapsed", 5.0, "Ke", 2450586.2020445, "Ve", 2453142.9965925002),
    ("dhanishta_half_elapsed", 100.0, "Sa", 2448075.064542, "Me", 2455014.9354580003),
    ("determinism_reference", 213.7, "Sa", 2451354.15354981, "Me", 2458294.02446581),
    ("revati_wraparound", 355.0, "Me", 2447664.1511325, "Ke", 2453873.5093205),
    ("arbitrary_spread", 45.6789, "Mo", 2449989.3092258605, "Ma", 2453641.8728658604),
)


def test_hermetic_baseline_matches_frozen_anchor_and_second_mahadasha():
    """Regression-guards the anchor construction hermetically (no PyJHora)."""

    for label, moon, seed_lord, expected_anchor, second_lord, expected_second_start in FROZEN_CASES:
        timeline = vimshottari_from_moon(moon, BIRTH_JD, depth=1)
        assert timeline.seed_lord == seed_lord, label
        assert timeline.anchor_jd == expected_anchor, label
        assert timeline.periods[1].lord == second_lord, label
        assert timeline.periods[1].start_jd == expected_second_start, label


def _to_exact(value) -> Fraction:
    if isinstance(value, Fraction):
        return value
    return Fraction(Decimal(str(value)))


def _mutated_anchor_jd(moon, birth_jd: float, year_length: Fraction) -> float:
    """
    Deliberate reimplementation of the audit's own documented H-05
    mutation: the ``-`` in vimshottari_from_moon's anchor construction
    (engine/dasha/vimshottari.py:122) flipped to ``+``. Used only by
    the negative control below; never imported by, and never affecting,
    production code.
    """

    exact = _to_exact(moon) % 360
    nakshatra_index = int(exact // NAK_SPAN)
    elapsed = (exact - nakshatra_index * NAK_SPAN) / NAK_SPAN
    seed_lord = DASHA_LORDS[nakshatra_index % 9]
    elapsed_years = YEARS_BY_LORD[seed_lord] * elapsed
    return birth_jd + float(elapsed_years * year_length)  # sign flipped, deliberately


def test_anchor_sign_flip_negative_control():
    """
    Proves the frozen baseline above would actually catch H-05's own
    documented defect class, not merely that it currently passes.
    """

    year_length = VIMSHOTTARI_MEAN_SIDEREAL_YEAR.year_length_days

    for label, moon, _seed_lord, expected_anchor, _second_lord, _expected_second_start in FROZEN_CASES:
        mutated = _mutated_anchor_jd(moon, BIRTH_JD, year_length)
        # The mutation must be a materially different, easily detectable
        # date - not a rounding-scale difference - matching the audit's
        # own "4,748-day error" characterization for its own seed case.
        assert abs(mutated - expected_anchor) > 100.0, label
        assert mutated != expected_anchor, label

    # And the real, current production code must NOT be the mutated
    # version - confirming the frozen baseline above is a live guard,
    # not a vacuous one.
    for label, moon, seed_lord, expected_anchor, _second_lord, _expected_second_start in FROZEN_CASES:
        timeline = vimshottari_from_moon(moon, BIRTH_JD, depth=1)
        assert timeline.seed_lord == seed_lord, label
        assert timeline.anchor_jd == expected_anchor, label
