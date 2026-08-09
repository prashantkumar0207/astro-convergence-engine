"""
Phase A generic Varga framework tests.

These test the FRAMEWORK ONLY (rule contracts, classifier, registry,
dispatcher plumbing, provenance propagation, boundary-convention
reuse). No production varga is registered, and nothing here implies
that any new varga is implemented. All rules used below are
synthetic test fixtures.
"""

import dataclasses

import pytest

from engine.astrology.divisional_chart import (
    IMPLEMENTED_VARGAS,
    UnsupportedVargaError,
    divisional_chart,
)
from engine.astrology.longitude_utils import BOUNDARY_TOLERANCE
from engine.astrology.varga_chart_builder import build_varga_chart
from engine.astrology.varga_classifier import classify
from engine.astrology.varga_registry import (
    DEFAULT_SCHOOL,
    get_varga_rule,
    register_varga_rule,
    registered_vargas,
    unregister_varga_rule,
)
from engine.astrology.varga_rules import (
    CyclicVargaRule,
    InvalidVargaRuleError,
    SegmentVargaRule,
)

IDENTITY_12 = tuple(range(12))
FORWARD = (1,) * 12

# Synthetic 5-division cyclic rule: each sign starts from itself.
SYNTHETIC_CYCLIC = CyclicVargaRule(divisions=5, start_sign=IDENTITY_12)

# Synthetic non-uniform segment rule: widths 5/5/8/7/5 (the D30 width
# pattern) with arbitrary but valid synthetic targets, same for all
# signs. This is a FIXTURE, not the classical D30 rule.
SYNTHETIC_SEGMENTS = SegmentVargaRule(
    segments=tuple(
        ((5.0, 0), (5.0, 10), (8.0, 8), (7.0, 2), (5.0, 6))
        for _ in range(12)
    )
)


# ---------------- rule contract validation ----------------


def test_cyclic_rule_valid_construction_and_frozen():
    rule = CyclicVargaRule(divisions=9, start_sign=IDENTITY_12)

    assert rule.divisions == 9
    with pytest.raises(dataclasses.FrozenInstanceError):
        rule.divisions = 10


@pytest.mark.parametrize(
    "kwargs",
    [
        {"divisions": 0, "start_sign": IDENTITY_12},
        {"divisions": -3, "start_sign": IDENTITY_12},
        {"divisions": 9, "start_sign": tuple(range(11))},
        {"divisions": 9, "start_sign": tuple(range(13))},
        {"divisions": 9, "start_sign": (12,) + tuple(range(11))},
        {"divisions": 9, "start_sign": (-1,) + tuple(range(11))},
        {"divisions": 9, "start_sign": IDENTITY_12, "direction": (1,) * 11},
        {"divisions": 9, "start_sign": IDENTITY_12,
         "direction": (0,) + (1,) * 11},
        {"divisions": 9, "start_sign": IDENTITY_12,
         "direction": (2,) + (1,) * 11},
    ],
)
def test_cyclic_rule_invalid_construction_rejected(kwargs):
    with pytest.raises(InvalidVargaRuleError):
        CyclicVargaRule(**kwargs)


def test_segment_rule_valid_construction():
    assert len(SYNTHETIC_SEGMENTS.segments) == 12


@pytest.mark.parametrize(
    "segments",
    [
        # only 11 sign entries
        tuple(((30.0, 0),) for _ in range(11)),
        # widths sum to 29
        tuple(((29.0, 0),) for _ in range(12)),
        # widths sum to 31
        tuple(((16.0, 0), (15.0, 1)) for _ in range(12)),
        # zero width
        tuple(((0.0, 0), (30.0, 1)) for _ in range(12)),
        # negative width
        tuple(((-5.0, 0), (35.0, 1)) for _ in range(12)),
        # target sign out of range
        tuple(((30.0, 12),) for _ in range(12)),
        # empty per-sign tuple
        tuple(() for _ in range(12)),
    ],
)
def test_segment_rule_invalid_construction_rejected(segments):
    with pytest.raises(InvalidVargaRuleError):
        SegmentVargaRule(segments=segments)


# ---------------- classifier ----------------


def test_cyclic_classification_basics():
    # 5 divisions of 6 deg; 14.5 deg into sign 2 (Gemini) is
    # division index 2, fraction (14.5-12)/6.
    c = classify(2 * 30.0 + 14.5, SYNTHETIC_CYCLIC)

    assert c.division_index == 2
    assert c.division_number == 3
    assert c.d_sign == (2 + 2) % 12
    assert abs(c.fraction - 2.5 / 6.0) < 1e-12


def test_cyclic_reverse_direction():
    rule = CyclicVargaRule(
        divisions=5,
        start_sign=IDENTITY_12,
        direction=(-1,) * 12,
    )

    c = classify(2 * 30.0 + 14.5, rule)  # index 2, counted backward

    assert c.d_sign == (2 - 2) % 12


def test_segment_classification_non_uniform_widths():
    # Widths 5/5/8/7/5: degree 11.0 falls in the third segment
    # (5+5 <= 11 < 18), target sign 8, fraction (11-10)/8.
    c = classify(11.0, SYNTHETIC_SEGMENTS)

    assert c.division_index == 2
    assert c.d_sign == 8
    assert abs(c.fraction - 1.0 / 8.0) < 1e-12

    # Degree 4.999...: first segment; degree 29.9: last segment.
    assert classify(4.9, SYNTHETIC_SEGMENTS).division_index == 0
    last = classify(29.9, SYNTHETIC_SEGMENTS)
    assert last.division_index == 4
    assert last.d_sign == 6


def test_classifier_rejects_unknown_rule_types():
    with pytest.raises(TypeError):
        classify(10.0, object())


# ---------------- boundary convention reuse ----------------


def test_normalization_reuse_tiny_negative_and_360():
    # The locked convention: tiny negatives normalize to 0 Aries.
    for x in (-1e-16, -1e-14, 360.0, 720.0, -360.0):
        c = classify(x, SYNTHETIC_CYCLIC)
        assert c.d_sign == SYNTHETIC_CYCLIC.start_sign[0]
        assert c.division_index == 0
        assert c.fraction == 0.0


def test_boundary_promote_up_convention_cyclic():
    # A value within the locked tolerance below a division edge
    # belongs to the NEXT division at fraction 0 (identical to the
    # certified D9/D10 convention).
    edge = 6.0  # first division edge of the 5-division rule
    below = edge - BOUNDARY_TOLERANCE / 2

    c = classify(below, SYNTHETIC_CYCLIC)

    assert c.division_index == 1
    assert c.fraction == 0.0

    # Outside the tolerance stays put.
    c2 = classify(edge - 1e-9, SYNTHETIC_CYCLIC)
    assert c2.division_index == 0


def test_boundary_promote_up_convention_segments():
    # Same convention at a non-uniform segment edge (edge at 10.0).
    below = 10.0 - BOUNDARY_TOLERANCE / 2

    c = classify(below, SYNTHETIC_SEGMENTS)

    assert c.division_index == 2
    assert c.fraction == 0.0

    c2 = classify(10.0 - 1e-9, SYNTHETIC_SEGMENTS)
    assert c2.division_index == 1


def test_exact_boundaries_belong_to_next_division():
    c = classify(6.0, SYNTHETIC_CYCLIC)
    assert c.division_index == 1

    c2 = classify(10.0, SYNTHETIC_SEGMENTS)
    assert c2.division_index == 2


def test_fraction_always_in_range():
    import math

    x = 0.0
    while x < 360.0:
        for rule in (SYNTHETIC_CYCLIC, SYNTHETIC_SEGMENTS):
            c = classify(x, rule)
            assert 0.0 <= c.fraction < 1.0
            assert 0 <= c.d_sign <= 11
        x += 0.173

    # ULP dust just below sign edges.
    for edge in (30.0, 90.0, 360.0):
        y = math.nextafter(edge, 0.0)
        for rule in (SYNTHETIC_CYCLIC, SYNTHETIC_SEGMENTS):
            c = classify(y, rule)
            assert 0.0 <= c.fraction < 1.0


# ---------------- registry ----------------


def test_registry_contains_exactly_the_certified_production_vargas():
    # REPLACED (was: registry empty in Phase A): certified production
    # vargas are registered per their approved ADRs; the registry
    # must contain exactly the sanctioned set (single source of
    # truth: engine.astrology.CERTIFIED_PRODUCTION_VARGAS).
    from engine.astrology import CERTIFIED_PRODUCTION_VARGAS

    assert registered_vargas() == CERTIFIED_PRODUCTION_VARGAS


def test_registry_lookup_roundtrip_and_cleanup():
    register_varga_rule(9999, "test_school", SYNTHETIC_CYCLIC)
    try:
        assert get_varga_rule(9999, "test_school") is SYNTHETIC_CYCLIC
        assert (9999, "test_school") in registered_vargas()
    finally:
        unregister_varga_rule(9999, "test_school")

    # REPLACED (was: registry empty after cleanup): the certified
    # production entries remain.
    from engine.astrology import CERTIFIED_PRODUCTION_VARGAS

    assert registered_vargas() == CERTIFIED_PRODUCTION_VARGAS


def test_registry_rejects_duplicates_and_bad_input():
    register_varga_rule(9999, "test_school", SYNTHETIC_CYCLIC)
    try:
        with pytest.raises(ValueError):
            register_varga_rule(9999, "test_school", SYNTHETIC_CYCLIC)
    finally:
        unregister_varga_rule(9999, "test_school")

    with pytest.raises(TypeError):
        register_varga_rule(9999, "test_school", "not a rule")

    with pytest.raises(ValueError):
        register_varga_rule(9999, "", SYNTHETIC_CYCLIC)


def test_registry_refuses_certified_divisions():
    for division in IMPLEMENTED_VARGAS:
        with pytest.raises(ValueError):
            register_varga_rule(division, "anything", SYNTHETIC_CYCLIC)


def test_unsupported_school_lookup_raises():
    with pytest.raises(UnsupportedVargaError):
        get_varga_rule(7, "parashara")

    with pytest.raises(UnsupportedVargaError):
        get_varga_rule(9999, "no_such_school")


# ---------------- dispatcher ----------------


def make_snapshot():
    from engine.calculations.calculations import calculate
    from engine.models.birth_data import BirthData

    return calculate(
        BirthData(1989, 7, 12, 16, 44, 0.0, 25.5941, 85.1376,
                  "Asia/Kolkata")
    ).snapshot


def test_dispatcher_certified_paths_unchanged():
    from engine.models.chart import Chart
    from engine.models.dashamsa_chart import DashamsaChart
    from engine.models.navamsa_chart import NavamsaChart

    snapshot = make_snapshot()

    assert isinstance(divisional_chart(snapshot, 1), Chart)
    assert isinstance(divisional_chart(snapshot, 9), NavamsaChart)
    assert isinstance(divisional_chart(snapshot, 10), DashamsaChart)

    # Explicit default school is equivalent to None.
    d9_default = divisional_chart(snapshot, 9)
    d9_explicit = divisional_chart(snapshot, 9, school=DEFAULT_SCHOOL)
    assert d9_default == d9_explicit


def test_dispatcher_rejects_non_default_school_for_certified_vargas():
    snapshot = make_snapshot()

    for division in IMPLEMENTED_VARGAS:
        with pytest.raises(UnsupportedVargaError):
            divisional_chart(snapshot, division, school="somnath")


def test_dispatcher_rejects_unimplemented_vargas_with_and_without_school():
    snapshot = make_snapshot()

    # REPLACED (was: included 3 and 12): D3 and D12 are certified
    # registry entries; every other recognized varga must still
    # refuse.
    for division in (2, 4, 7, 16, 20, 24, 27, 30, 40, 45, 60):
        with pytest.raises(UnsupportedVargaError):
            divisional_chart(snapshot, division)

    with pytest.raises(UnsupportedVargaError):
        divisional_chart(snapshot, 7, school="parashara")

    with pytest.raises(UnsupportedVargaError):
        divisional_chart(snapshot, 13)  # not a varga at all


def test_dispatcher_routes_registered_rule_and_reports_school():
    from engine.models.varga_chart import VargaChart

    snapshot = make_snapshot()

    register_varga_rule(9999, "test_school", SYNTHETIC_CYCLIC)
    try:
        chart = divisional_chart(snapshot, 9999, school="test_school")
    finally:
        unregister_varga_rule(9999, "test_school")

    assert isinstance(chart, VargaChart)
    assert chart.varga == 9999
    assert chart.school == "test_school"
    assert len(chart.planets) == 14


# ---------------- provenance propagation ----------------


def test_varga_chart_carries_snapshot_provenance():
    snapshot = make_snapshot()

    chart = build_varga_chart(
        snapshot, 9999, SYNTHETIC_CYCLIC, "test_school"
    )

    assert chart.provenance is snapshot.provenance
    assert chart.provenance.profile_name == "parashari_lahiri"
    assert chart.provenance.frame == "sidereal"
    assert chart.provenance.ephemeris_mode == "swieph"

    sun = chart.planets["Sun"]
    assert sun.source_longitude == snapshot.sidereal_planets[
        "Sun"
    ].longitude
    assert 1 <= sun.division_number <= SYNTHETIC_CYCLIC.divisions
    assert 0 <= chart.ascendant.sign <= 11
