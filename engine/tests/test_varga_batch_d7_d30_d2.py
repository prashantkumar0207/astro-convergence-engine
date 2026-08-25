"""
VARGA_D7_V1 / VARGA_D30_V1 / VARGA_D2_V1 gates 1, 2, 4
(ADR-0011, ADR-0011, ADR-0011).
"""

import math

import pytest

from engine.astrology import CERTIFIED_PRODUCTION_VARGAS
from engine.astrology.divisional_chart import divisional_chart
from engine.astrology.varga_classifier import classify
from engine.astrology.varga_d2 import D2_PARASHARA
from engine.astrology.varga_d7 import D7_PARASHARA
from engine.astrology.varga_d30 import D30_PARASHARA
from engine.astrology.varga_registry import (
    UnsupportedVargaError,
    get_varga_rule,
    register_varga_rule,
    registered_vargas,
    unregister_varga_rule,
)
from engine.astrology.varga_rules import CyclicVargaRule, rule_content_sha256
from engine.calculations.calculations import calculate
from engine.models.birth_data import BirthData

BIRTH = BirthData(1985, 12, 21, 14, 40, 0.0, 25.6, 85.1333, "Asia/Kolkata")

SIGNS = ("Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces")

# ---------------------------------------------------------------- Gate 1
# Second independent transcriptions, by sign NAME.

D7_START_TRANSCRIPTION = {  # odd signs from themselves, even from the 7th
    "Aries": "Aries", "Taurus": "Scorpio", "Gemini": "Gemini",
    "Cancer": "Capricorn", "Leo": "Leo", "Virgo": "Pisces",
    "Libra": "Libra", "Scorpio": "Taurus", "Sagittarius": "Sagittarius",
    "Capricorn": "Cancer", "Aquarius": "Aquarius", "Pisces": "Virgo",
}

D30_ODD_TRANSCRIPTION = (
    (5.0, "Mars", "Aries"), (5.0, "Saturn", "Aquarius"),
    (8.0, "Jupiter", "Sagittarius"), (7.0, "Mercury", "Gemini"),
    (5.0, "Venus", "Libra"),
)
D30_EVEN_TRANSCRIPTION = (
    (5.0, "Venus", "Taurus"), (7.0, "Mercury", "Virgo"),
    (8.0, "Jupiter", "Pisces"), (5.0, "Saturn", "Capricorn"),
    (5.0, "Mars", "Scorpio"),
)
RULERSHIPS = {  # sign -> classical ruler, for the re-derivation
    "Aries": "Mars", "Scorpio": "Mars", "Taurus": "Venus", "Libra": "Venus",
    "Gemini": "Mercury", "Virgo": "Mercury", "Sagittarius": "Jupiter",
    "Pisces": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn",
}


def test_d7_start_table_matches_second_transcription():
    assert D7_PARASHARA.divisions == 7
    for index, name in enumerate(SIGNS):
        start = D7_PARASHARA.start_sign[index]
        assert SIGNS[start] == D7_START_TRANSCRIPTION[name], name
        assert D7_PARASHARA.direction[index] == 1
        # Re-derivation: odd signs self-start, even signs 7th.
        assert start == (index if index % 2 == 0 else (index + 6) % 12)


def test_d30_tables_match_second_transcription_and_rulership():
    for index in range(12):
        segments = D30_PARASHARA.segments[index]
        transcription = D30_ODD_TRANSCRIPTION if index % 2 == 0 else D30_EVEN_TRANSCRIPTION
        assert len(segments) == 5
        for (width, target), (t_width, planet, t_sign) in zip(segments, transcription):
            assert width == t_width
            assert SIGNS[target] == t_sign
            # Rulership re-derivation: the target is ruled by the
            # segment's classical planet and matches the source
            # sign's gender (odd targets odd signs, even even).
            assert RULERSHIPS[t_sign] == planet
            assert target % 2 == index % 2
        assert sum(width for width, _ in segments) == 30.0


def test_d2_tables_match_transcription_and_two_sign_space():
    leo, cancer = 4, 3
    for index in range(12):
        segments = D2_PARASHARA.segments[index]
        assert len(segments) == 2
        assert all(width == 15.0 for width, _ in segments)
        first, second = segments[0][1], segments[1][1]
        if index % 2 == 0:
            assert (first, second) == (leo, cancer), index
        else:
            assert (first, second) == (cancer, leo), index
        assert {first, second} == {leo, cancer}


# ---------------------------------------------------------------- Gate 2

def _d7_expected(longitude):
    source = int(longitude // 30.0)
    # Independent rule under the locked convention: values within
    # 1e-10 below a division boundary promote up (D7's 30/7 widths
    # are not exactly representable in binary, so grid points can
    # land one ULP below a boundary; the certified classifier
    # promotes them, and so must this reference).
    division = int(((longitude - source * 30.0) + 1e-10) / (30.0 / 7.0))
    if division > 6:
        division = 6
    start = source if source % 2 == 0 else (source + 6) % 12
    return (start + division) % 12, division


def _d30_expected(longitude):
    source = int(longitude // 30.0)
    within = longitude - source * 30.0
    table = D30_ODD_TRANSCRIPTION if source % 2 == 0 else D30_EVEN_TRANSCRIPTION
    cumulative = 0.0
    for division, (width, _planet, t_sign) in enumerate(table):
        cumulative += width
        if within < cumulative or division == 4:
            return SIGNS.index(t_sign), division
    raise AssertionError


def _d2_expected(longitude):
    source = int(longitude // 30.0)
    half = 0 if (longitude - source * 30.0) < 15.0 else 1
    leo, cancer = 4, 3
    if source % 2 == 0:
        return (leo, 0) if half == 0 else (cancer, 1)
    return (cancer, 0) if half == 0 else (leo, 1)


@pytest.mark.parametrize("rule,expected_fn", [
    (D7_PARASHARA, _d7_expected),
    (D30_PARASHARA, _d30_expected),
    (D2_PARASHARA, _d2_expected),
], ids=["d7", "d30", "d2"])
def test_dense_sweep_against_independent_rule(rule, expected_fn):
    step = 360.0 / 51429
    for i in range(51429):
        longitude = i * step
        result = classify(longitude, rule)
        assert (result.d_sign, result.division_index) == expected_fn(longitude), longitude
        assert 0.0 <= result.fraction < 1.0


def _boundaries(rule):
    if rule is D7_PARASHARA:
        return [s * 30.0 + d * (30.0 / 7.0) for s in range(12) for d in range(7)]
    if rule is D30_PARASHARA:
        out = []
        for s in range(12):
            widths = [w for w, _ in D30_PARASHARA.segments[s]]
            cumulative = 0.0
            for width in widths:
                out.append(s * 30.0 + cumulative)
                cumulative += width
        return out
    return [s * 30.0 + h * 15.0 for s in range(12) for h in range(2)]


@pytest.mark.parametrize("rule", [D7_PARASHARA, D30_PARASHARA, D2_PARASHARA],
                         ids=["d7", "d30", "d2"])
def test_ulp_boundary_battery(rule):
    # Locked convention: at-boundary owns the new division; ULP
    # neighbors above agree; clearly-below stays in the previous
    # division (or previous sign's last, at sign boundaries).
    for boundary in _boundaries(rule):
        at = classify(boundary, rule)
        assert at.fraction == 0.0 or boundary % 30.0 != 0.0

        up = boundary
        for _ in range(3):
            up = math.nextafter(up, math.inf)
            if up >= 360.0:
                break
            result = classify(up, rule)
            assert (result.d_sign, result.division_index) == (
                at.d_sign, at.division_index), boundary

        clearly_below = boundary - 1e-6
        if clearly_below >= 0.0 and boundary % 360.0 != 0.0:
            below = classify(clearly_below, rule)
            assert (below.d_sign, below.division_index) != (
                at.d_sign, at.division_index) or at.division_index != 0, boundary

        just_below = boundary - 1e-11
        if just_below >= 0.0 and boundary > 0.0:
            promoted = classify(just_below, rule)
            if boundary % 30.0 == 0.0:  # sign boundary: no promotion
                assert promoted.division_index == len(
                    rule.segments[int(just_below // 30.0)]) - 1 if hasattr(
                    rule, "segments") else promoted.division_index == rule.divisions - 1
            else:  # intra-sign boundary: promoted up
                assert (promoted.d_sign, promoted.division_index) == (
                    at.d_sign, at.division_index), boundary


def test_d2_output_space_is_only_leo_and_cancer():
    step = 360.0 / 4999
    for i in range(4999):
        assert classify(i * step, D2_PARASHARA).d_sign in (3, 4)


# ---------------------------------------------------------------- Gate 4

def test_registry_is_exactly_the_certified_set():
    assert registered_vargas() == CERTIFIED_PRODUCTION_VARGAS
    for division in (2, 3, 7, 12, 30):
        assert (division, "parashara") in registered_vargas()


def test_certified_d1_d9_d10_dispatch_unchanged():
    snapshot = calculate(BIRTH).snapshot
    assert type(divisional_chart(snapshot, 9)).__name__ == "NavamsaChart"
    assert type(divisional_chart(snapshot, 10)).__name__ == "DashamsaChart"


def test_remaining_vargas_still_refused():
    # D45 is excluded: certified and registered (ADR-0077, VARGA_D45_V1).
    snapshot = calculate(BIRTH).snapshot
    for division in (4, 16, 20, 24, 27, 40, 60):
        with pytest.raises(UnsupportedVargaError):
            divisional_chart(snapshot, division)


def test_batch_vargas_served_with_provenance():
    snapshot = calculate(BIRTH).snapshot
    for division in (2, 7, 30):
        chart = divisional_chart(snapshot, division)
        assert chart.varga == division
        assert chart.school == "parashara"
        assert chart.provenance is snapshot.provenance


# ------------------------------------------------------- Gate 4, B-02
# reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md.

#: Content fingerprints of the certified D7/D30/D2 tables, pinned.
CERTIFIED_CONTENT_SHA256 = {
    7: "42c0f474138d98a37e1a9963866a2d0f86621fa67c73069e897fef48024aeead",
    30: "deacd958cf19b7641c4f8cb086ad27d8a5efaeb6e38b594dc0cd4113a25794d3",
    2: "b78745de5d815b6635cca62d9d872c6dd7acd0a8cdbc5e5ecf53a0bc78ee1859",
}

_PRODUCTION_RULES = {7: D7_PARASHARA, 30: D30_PARASHARA, 2: D2_PARASHARA}


@pytest.mark.parametrize("division", [7, 30, 2])
def test_registered_rule_identity_is_the_certified_object(division):
    assert get_varga_rule(division, "parashara") is _PRODUCTION_RULES[division]


@pytest.mark.parametrize("division", [7, 30, 2])
def test_registered_rule_content_hash_matches_pinned_value(division):
    rule = _PRODUCTION_RULES[division]
    assert rule_content_sha256(rule) == CERTIFIED_CONTENT_SHA256[division]


def _tampered(rule):
    import dataclasses

    if isinstance(rule, CyclicVargaRule):
        tampered_start = ((rule.start_sign[0] + 1) % 12,) + rule.start_sign[1:]
        return dataclasses.replace(rule, start_sign=tampered_start)
    tampered_segments = (
        ((rule.segments[0][0][0], (rule.segments[0][0][1] + 1) % 12),)
        + rule.segments[0][1:],
    ) + rule.segments[1:]
    return dataclasses.replace(rule, segments=tampered_segments)


@pytest.mark.parametrize("division", [7, 30, 2])
def test_negative_control_substituted_rule_is_detected(division):
    """Prove the identity and content checks above can actually fail."""

    certified = _PRODUCTION_RULES[division]
    tampered = _tampered(certified)
    # Still a structurally valid, legitimately-registrable rule for
    # this division (only a target/start-sign cell changed, not the
    # division identity) - only B-02's checks catch the substitution.
    if isinstance(certified, CyclicVargaRule):
        assert tampered.divisions == division
    else:
        assert tampered.division == division

    unregister_varga_rule(division, "parashara")
    try:
        register_varga_rule(division, "parashara", tampered)

        assert get_varga_rule(division, "parashara") is not certified
        assert (
            rule_content_sha256(get_varga_rule(division, "parashara"))
            != CERTIFIED_CONTENT_SHA256[division]
        )
    finally:
        unregister_varga_rule(division, "parashara")
        register_varga_rule(division, "parashara", certified)

    assert get_varga_rule(division, "parashara") is certified
    assert rule_content_sha256(certified) == CERTIFIED_CONTENT_SHA256[division]
