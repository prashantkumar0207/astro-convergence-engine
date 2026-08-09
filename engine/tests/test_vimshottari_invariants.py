"""
Vimshottari exact-arithmetic invariants (Gate 1 of ADR-0007).
"""

from fractions import Fraction

import pytest

from engine.dasha.profile import VIMSHOTTARI_MEAN_SIDEREAL_YEAR
from engine.dasha.tables import DASHA_LORDS, DASHA_YEARS, NAK_SPAN, TOTAL_YEARS
from engine.dasha.vimshottari import vimshottari_from_moon


def _timeline(moon, depth=3):
    return vimshottari_from_moon(moon, 2451545.0, depth=depth)


def test_tables_are_the_certified_vimshottari_set():
    assert DASHA_LORDS == ("Ke", "Ve", "Su", "Mo", "Ma", "Ra", "Ju", "Sa", "Me")
    assert DASHA_YEARS == (7, 20, 6, 10, 7, 18, 16, 19, 17)
    assert sum(DASHA_YEARS) == TOTAL_YEARS == 120
    assert NAK_SPAN == Fraction(40, 3)
    assert VIMSHOTTARI_MEAN_SIDEREAL_YEAR.year_length_days == Fraction(365256364, 1000000)


def test_cycle_closes_at_exactly_120_years():
    timeline = _timeline(123.456)
    mahas = timeline.mahadashas()
    assert len(mahas) == 9
    assert mahas[0].start_years == 0
    assert mahas[-1].end_years == Fraction(120)
    for previous, current in zip(mahas, mahas[1:]):
        assert previous.end_years == current.start_years


def test_children_sum_exactly_to_parent_at_every_level():
    timeline = _timeline(200.125)
    by_parent = {}
    for period in timeline.periods:
        if period.level > 1:
            by_parent.setdefault(period.lords[:-1], []).append(period)
    parents = {p.lords: p for p in timeline.periods}
    assert by_parent, "no child periods generated"
    for parent_lords, children in by_parent.items():
        parent = parents[parent_lords]
        assert len(children) == 9
        assert children[0].start_years == parent.start_years
        assert children[-1].end_years == parent.end_years
        total = sum((c.duration_years for c in children), Fraction(0))
        assert total == parent.duration_years
        for previous, current in zip(children, children[1:]):
            assert previous.end_years == current.start_years


def test_period_counts_by_depth():
    assert len(_timeline(10.0, depth=1).periods) == 9
    assert len(_timeline(10.0, depth=2).periods) == 9 + 81
    assert len(_timeline(10.0, depth=3).periods) == 9 + 81 + 729


def test_each_level_cycle_starts_from_its_own_lord():
    timeline = _timeline(77.7)
    for period in timeline.periods:
        if period.level > 1:
            parent_lord = period.lords[-2]
            siblings = [p for p in timeline.periods
                        if p.level == period.level and p.lords[:-1] == period.lords[:-1]]
            assert siblings[0].lord == parent_lord


def test_balance_identity():
    timeline = _timeline(5.0)  # inside Ashwini (Ketu, 7y)
    elapsed_years = timeline.seed_elapsed_fraction * 7
    assert timeline.balance_years + elapsed_years == 7
    assert timeline.seed_lord == "Ke"
    # 5.0 deg into Ashwini: elapsed = 5 / (40/3) = 3/8 exactly (decimal spelling 5.0).
    assert timeline.seed_elapsed_fraction == Fraction(3, 8)
    assert timeline.balance_years == Fraction(35, 8)


def test_moon_exactly_on_boundary_starts_full_dasha():
    # [start, end): Moon exactly at Bharani start owns Bharani (Venus), elapsed 0.
    timeline = _timeline(Fraction(40, 3))
    assert timeline.seed_nakshatra_number == 2
    assert timeline.seed_lord == "Ve"
    assert timeline.seed_elapsed_fraction == 0
    assert timeline.balance_years == 20
    assert timeline.anchor_jd == timeline.birth_jd


def test_wraparound_lord_cycle_from_late_nakshatra():
    # Revati (27th) -> Mercury; sequence wraps to Ketu.
    timeline = _timeline(355.0)
    assert timeline.seed_lord == "Me"
    assert [p.lord for p in timeline.mahadashas()] == [
        "Me", "Ke", "Ve", "Su", "Mo", "Ma", "Ra", "Ju", "Sa",
    ]


def test_jd_view_is_consistent_with_exact_offsets():
    timeline = _timeline(100.0)
    year_length = timeline.year_length_days
    for period in timeline.periods:
        assert period.start_jd == timeline.anchor_jd + float(period.start_years * year_length)
        assert period.end_jd == timeline.anchor_jd + float(period.end_years * year_length)


def test_determinism():
    first = _timeline(213.7)
    second = _timeline(213.7)
    assert first == second


def test_invalid_depth_rejected():
    with pytest.raises(ValueError):
        _timeline(10.0, depth=4)
    with pytest.raises(ValueError):
        _timeline(10.0, depth=0)
