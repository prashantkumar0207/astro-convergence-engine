"""
KP interval invariants (Gate 2 of ADR-KP-001).

Ports the certified legacy invariant tests (legacy/test_kp_intervals.py)
into the default gate, plus table and conversion contracts.
"""

from decimal import Decimal
from fractions import Fraction

from engine.astrology.sign_lord import sign_lord
from engine.kp.chain import kp_chain
from engine.kp.intervals import all_boundaries, to_exact, walk
from engine.kp.tables import (
    KP_LORD_FULL_NAMES,
    KP_LORDS,
    KP_SIGN_LORDS,
    KP_YEARS,
    NAK_SPAN,
)


def test_tables_are_the_certified_vimshottari_set():
    assert KP_LORDS == ("Ke", "Ve", "Su", "Mo", "Ma", "Ra", "Ju", "Sa", "Me")
    assert KP_YEARS == (7, 20, 6, 10, 7, 18, 16, 19, 17)
    assert sum(KP_YEARS) == 120
    assert NAK_SPAN == Fraction(40, 3)


def test_kp_sign_lords_agree_with_engine_sign_lords():
    # Separate data per school isolation; agreement verified, never merged.
    for index, abbrev in enumerate(KP_SIGN_LORDS):
        assert KP_LORD_FULL_NAMES[abbrev] == sign_lord(index + 1)


def test_interval_completeness_exact():
    # Sub widths of every nakshatra sum EXACTLY to 40/3; recursively for sub-subs.
    for nak in range(27):
        star_index = nak % 9
        total = Fraction(0)
        for step in range(9):
            index = (star_index + step) % 9
            width = NAK_SPAN * KP_YEARS[index] / 120
            total += width
            inner = Fraction(0)
            for step2 in range(9):
                inner += width * KP_YEARS[(index + step2) % 9] / 120
            assert inner == width
        assert total == NAK_SPAN


def test_boundary_ownership_start_inclusive_end_exclusive():
    eps = Fraction(1, 10**9)  # ~3.6e-6 arcsec
    for boundary in all_boundaries():
        at = kp_chain(boundary)
        above = kp_chain(boundary + eps)
        assert (
            at.nakshatra_lord, at.sub_lord, at.sub_sub_lord,
        ) == (
            above.nakshatra_lord, above.sub_lord, above.sub_sub_lord,
        ), f"at-boundary must own the next interval: {boundary}"
        if boundary > 0:
            below = kp_chain(boundary - eps)
            assert (
                below.sub_sub_lord != at.sub_sub_lord
                or below.sub_lord != at.sub_lord
                or below.nakshatra_lord != at.nakshatra_lord
            ), f"no change across boundary {boundary}"


def test_known_classical_anchors():
    chain = kp_chain(0.0)
    assert (
        chain.sign_lord, chain.nakshatra_lord, chain.sub_lord, chain.sub_sub_lord,
    ) == ("Ma", "Ke", "Ke", "Ke")
    assert (chain.sign_name, chain.nakshatra_name) == ("Aries", "Ashwini")

    chain = kp_chain(Fraction(40, 3))  # exactly Bharani start
    assert (chain.nakshatra_lord, chain.sub_lord, chain.sub_sub_lord) == ("Ve", "Ve", "Ve")
    assert chain.nakshatra_number == 2

    # End of Ashwini's first (Ketu) sub: exactly at -> Venus sub begins.
    end_first_sub = NAK_SPAN * 7 / 120
    chain = kp_chain(end_first_sub)
    assert chain.sub_lord == "Ve" and chain.sub_sub_lord == "Ve"


def test_determinism():
    import random

    random.seed(42)
    points = [random.uniform(0, 360) for _ in range(500)]
    first = [kp_chain(point) for point in points]
    second = [kp_chain(point) for point in points]
    assert first == second


def test_to_exact_preserves_decimal_spelling():
    # The certified conversion rule: decimal spelling, not IEEE-754 expansion.
    assert to_exact(0.1) == Fraction(1, 10)
    assert to_exact(0.1) != Fraction(0.1)
    assert to_exact(13.333333333333334) == Fraction(Decimal("13.333333333333334"))
    assert to_exact(Fraction(40, 3)) == Fraction(40, 3)
    assert to_exact(7) == Fraction(7)
    assert to_exact(Decimal("359.999")) == Fraction(Decimal("359.999"))


def test_walk_covers_span_and_raises_beyond():
    import pytest

    index, offset, width = walk(Fraction(0), 0, NAK_SPAN)
    assert (index, offset) == (0, Fraction(0))
    with pytest.raises(ArithmeticError):
        walk(NAK_SPAN, 0, NAK_SPAN)  # position == span is out of [0, span)


def test_boundary_count_and_range():
    bounds = all_boundaries()
    # 27 nakshatras x (1 + 9 + 81) starts, with nak/sub starts coinciding
    # with the first inner start of their first sub interval.
    assert bounds[0] == 0
    assert all(0 <= b < 360 for b in bounds)
    assert bounds == sorted(set(bounds))
    assert len(bounds) == 27 * 81  # deepest level enumerates every start once


def test_nakshatra_number_agrees_with_engine_off_boundaries():
    # Same 27-fold division as the engine primitive; agreement verified
    # away from boundaries (at exact boundaries the engine float
    # convention and the exact KP rule are documented to differ within
    # 1e-10 deg; see engine/kp/intervals.py numeric contract).
    from engine.astrology.nakshatra import nakshatra

    step = 360.0 / 997
    for i in range(997):
        lon = i * step + 0.001
        assert kp_chain(lon).nakshatra_number == nakshatra(lon)
