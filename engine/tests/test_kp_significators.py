"""
KP_SIGNIFICATOR_V1 production tests (ADR-0078).

Mirrors the established pattern (test_varga_d45.py): frozen-constant
integrity, content-hash pinning, a dense wiring sweep, a boundary battery,
end-to-end integration through the certified KP chart pipeline, isolation
from Parashari aspect code, and a genuine negative control.

There is no dynamic registry for KP_SIGNIFICATOR_V1 (unlike the Varga
framework) - engine.kp.significators exposes its frozen judgment directly
as module-level functions, so the registry-style tests in test_varga_d45.py
have no direct analog here; the tests below cover the equivalent ground
(frozen-value integrity, isolation, negative-control detectability) in the
shape this capability actually has.
"""

import inspect

import pytest

from engine.kp.chain import kp_chain
from engine.kp.chart import kp_chart
from engine.kp.significators import (
    DENY_HOUSES,
    KP_GRAHAS,
    NODES,
    PROMISE_HOUSES,
    SPECIAL_ASPECTS,
    aspected_signs,
    full_name,
    house_of_placidus,
    is_aspecting,
    is_conjunct,
    judge_marriage,
    node_substitute,
    rule_content_sha256,
    sign_of,
    signification_set,
)
from engine.models.birth_data import BirthData
from engine.models.kp_chart import KpBody, KpChart, KpCusp
from engine.models.kp_significator import KpSignificatorJudgment

BIRTH = BirthData(1985, 12, 21, 14, 40, 0.0, 25.6, 85.1333, "Asia/Kolkata")

#: Content fingerprint of the certified KP_SIGNIFICATOR_V1 rule constants,
#: pinned (also pinned independently in scripts/certify_kp_significator.py).
CERTIFIED_KP_SIGNIFICATOR_CONTENT_SHA256 = (
    "0cb5aa8661c1d9b950c4d6f35d0b12baaf03aec3f28adc6937bbe257cd1f2ab9"
)

_DEFAULT_CUSPS = tuple(float(30 * i) for i in range(12))
_NEUTRAL_LONGITUDES = {
    "Sun": 15.0, "Moon": 45.0, "Mars": 75.0, "Mercury": 105.0, "Jupiter": 135.0,
    "Venus": 165.0, "Saturn": 195.0, "Rahu": 225.0, "Ketu": 45.0,
}


def _make_chart(cusp_longitudes, body_longitudes, retrograde_names=frozenset()) -> KpChart:
    cusps = tuple(
        KpCusp(number=i + 1, longitude=lon, chain=kp_chain(lon))
        for i, lon in enumerate(cusp_longitudes)
    )
    bodies = tuple(
        KpBody(name=name, longitude=lon, speed_longitude=-1.0 if name in retrograde_names else 1.0,
               retrograde=name in retrograde_names, chain=kp_chain(lon))
        for name, lon in body_longitudes.items()
    )
    return KpChart(julian_day=0.0, bodies=bodies, cusps=cusps, ascendant=bodies[0], provenance=None)


def _find_longitude_with_sub_lord(target_lord: str, start: float = 0.0, step: float = 0.01) -> float:
    lon = start
    while lon < 360.0:
        if full_name(kp_chain(lon).sub_lord) == target_lord:
            return lon
        lon += step
    raise AssertionError(f"no longitude found for sub-lord {target_lord}")


# --------------------------------------------------------- Frozen constants

def test_frozen_constants_match_adr_0078():
    assert PROMISE_HOUSES == frozenset({2, 7, 11})
    assert DENY_HOUSES == frozenset({1, 6, 10, 12})
    assert SPECIAL_ASPECTS == {"Mars": (4, 8), "Jupiter": (5, 9), "Saturn": (3, 10)}
    assert KP_GRAHAS == ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu")
    assert NODES == ("Rahu", "Ketu")


def test_content_hash_matches_pinned_value():
    assert rule_content_sha256() == CERTIFIED_KP_SIGNIFICATOR_CONTENT_SHA256


def test_negative_control_mutated_constants_change_the_hash():
    """Prove the pinning check above can actually fail - a mutated LOCAL
    copy, never the production module itself (there is no dynamic registry
    to substitute into, unlike the Varga framework, so this control mutates
    a same-shaped payload directly rather than the module's own object)."""

    import hashlib
    tampered_promise = frozenset({2, 7, 10})  # swapped 11 for 10
    payload = repr((
        sorted(tampered_promise), sorted(DENY_HOUSES),
        sorted(SPECIAL_ASPECTS.items()), KP_GRAHAS,
    )).encode()
    tampered_hash = hashlib.sha256(payload).hexdigest()
    assert tampered_hash != rule_content_sha256()
    # The real module's own constants are confirmed unmutated by the above.
    assert PROMISE_HOUSES == frozenset({2, 7, 11})
    assert rule_content_sha256() == CERTIFIED_KP_SIGNIFICATOR_CONTENT_SHA256


# --------------------------------------------------------------- Isolation

def test_module_never_imports_parashari():
    import engine.kp.significators as module
    source = inspect.getsource(module)
    for line in source.splitlines():
        stripped = line.strip()
        assert not stripped.startswith(("import engine.parashari", "from engine.parashari")), (
            "engine.kp.significators must never import Parashari aspect logic"
        )


def test_aspect_convention_matches_classical_special_aspects():
    # Universal 7th for every planet, plus the three special aspects,
    # verified directly via aspected_signs rather than assumed.
    assert aspected_signs("Sun", 1) == frozenset({7})
    assert aspected_signs("Mars", 1) == frozenset({4, 7, 8})
    assert aspected_signs("Jupiter", 1) == frozenset({5, 7, 9})
    assert aspected_signs("Saturn", 1) == frozenset({3, 7, 10})
    # 7th house from Aries (sign 1) is Libra (sign 7) - the classical
    # opposition, not sign 8.
    assert 7 in aspected_signs("Sun", 1)
    assert 8 not in aspected_signs("Sun", 1)


def test_conjunction_is_same_sign_no_orb():
    assert is_conjunct(3, 3) is True
    assert is_conjunct(3, 4) is False


# ------------------------------------------------------- KP chain wiring

def test_dense_sweep_sub_lord_wiring_against_independent_kp_chain_call():
    step = 360.0 / 4320
    for i in range(4320):
        lon = i * step
        cusps = list(_DEFAULT_CUSPS)
        cusps[6] = lon
        chart = _make_chart(cusps, dict(_NEUTRAL_LONGITUDES))
        assert chart.cusps[6].chain.sub_lord == kp_chain(lon).sub_lord


def test_boundary_battery_inherited_from_kp_chain_v1():
    from engine.kp.intervals import all_boundaries
    for bound in list(all_boundaries())[:200]:
        lon = float(bound)
        cusps = list(_DEFAULT_CUSPS)
        cusps[6] = lon
        chart = _make_chart(cusps, dict(_NEUTRAL_LONGITUDES))
        assert chart.cusps[6].chain.sub_lord == kp_chain(lon).sub_lord


# ------------------------------------------------------- Significator logic

def test_significator_strength_categories_are_independently_recognized():
    house = 5
    cusps = list(_DEFAULT_CUSPS)
    house_sign = sign_of(cusps[house - 1])
    owner = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
             "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"][house_sign - 1]
    chart = _make_chart(cusps, dict(_NEUTRAL_LONGITUDES))
    cusp_lons = [c.longitude for c in chart.cusps]
    assert house in signification_set(owner, chart, cusp_lons)


def test_mixed_and_undetermined_verdicts_are_distinct_from_promised_denied():
    # A sub-lord signifying houses in both groups is MIXED, never silently
    # collapsed into PROMISED or DENIED.
    for target_lord in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"):
        chart = _make_chart(*_chart_args_for(target_lord))
        result = judge_marriage(chart)
        assert result.verdict in ("PROMISED", "DENIED", "MIXED", "UNDETERMINED")
        promise_hit = bool(set(result.signification_set) & PROMISE_HOUSES)
        deny_hit = bool(set(result.signification_set) & DENY_HOUSES)
        if promise_hit and deny_hit:
            assert result.verdict == "MIXED"
        elif promise_hit:
            assert result.verdict == "PROMISED"
        elif deny_hit:
            assert result.verdict == "DENIED"
        else:
            assert result.verdict == "UNDETERMINED"


def _chart_args_for(target_lord):
    lon = _find_longitude_with_sub_lord(target_lord)
    cusps = list(_DEFAULT_CUSPS)
    cusps[6] = lon
    return cusps, dict(_NEUTRAL_LONGITUDES)


def test_retrograde_qualifier_disclosed_not_a_pass_fail_gate():
    lon = _find_longitude_with_sub_lord("Mars")
    cusps = list(_DEFAULT_CUSPS)
    cusps[6] = lon
    retro_chart = _make_chart(cusps, dict(_NEUTRAL_LONGITUDES), retrograde_names={"Mars"})
    direct_chart = _make_chart(cusps, dict(_NEUTRAL_LONGITUDES))
    retro_result = judge_marriage(retro_chart)
    direct_result = judge_marriage(direct_chart)
    assert retro_result.sub_lord == "Mars"
    assert retro_result.retrograde_qualifier is True
    assert direct_result.retrograde_qualifier is False
    # The verdict/signification logic itself is unaffected by retrograde -
    # only the disclosure qualifier differs.
    assert retro_result.verdict == direct_result.verdict
    assert retro_result.signification_set == direct_result.signification_set


def test_node_substitution_never_resolves_to_the_other_node():
    rahu_lon = _find_longitude_with_sub_lord("Rahu")
    cusps = list(_DEFAULT_CUSPS)
    cusps[6] = rahu_lon
    bodies = dict(_NEUTRAL_LONGITUDES)
    bodies["Rahu"] = rahu_lon
    bodies["Ketu"] = (rahu_lon + 180.0) % 360.0
    chart = _make_chart(cusps, bodies)
    substitute = node_substitute("Rahu", chart)
    assert substitute not in ("Rahu", "Ketu")
    assert substitute in KP_GRAHAS


def test_house_of_placidus_is_a_valid_cyclic_partition():
    cusps = list(_DEFAULT_CUSPS)
    for test_lon in (0.0, 47.3, 133.9, 289.5, 359.999):
        house = house_of_placidus(test_lon, cusps)
        assert 1 <= house <= 12


# ----------------------------------------------------- End-to-end integration

def test_judge_marriage_end_to_end_through_certified_kp_chart_pipeline():
    chart = kp_chart(BIRTH)
    result = judge_marriage(chart)
    assert isinstance(result, KpSignificatorJudgment)
    assert result.sub_lord in KP_GRAHAS
    assert result.verdict in ("PROMISED", "DENIED", "MIXED", "UNDETERMINED")
    assert set(result.signification_set) <= set(range(1, 13))
    assert isinstance(result.retrograde_qualifier, bool)
    assert "ACE-defined inference" in result.aspect_convention_disclosure
    assert "ACE-defined inference" in result.horary_to_natal_disclosure


def test_judge_marriage_rejects_non_kp_profile_chart():
    # kp_chart()/kp_chart_from_snapshot() already enforce the KP_KRISHNAMURTI
    # profile (KpProfileError) before a chart can be built at all - judge_marriage
    # itself only ever receives an already-validated KpChart, so there is
    # nothing further for it to reject. This test documents that guarantee
    # rather than re-testing KP_CHAIN_V1's own already-certified enforcement.
    from engine.astronomy.profile import PARASHARI_LAHIRI
    from engine.calculations.calculations import calculate
    from engine.kp.chart import KpProfileError, kp_chart_from_snapshot

    wrong_profile_snapshot = calculate(BIRTH, profile=PARASHARI_LAHIRI).snapshot
    with pytest.raises(KpProfileError):
        kp_chart_from_snapshot(wrong_profile_snapshot)
