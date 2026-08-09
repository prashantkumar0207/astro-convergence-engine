"""
PARASHARI_DRISHTI_V1 gates 1, 2, 4 (ADR-ASPECT-PAR-001).
"""

import pytest

from engine.astronomy.profile import KP_KRISHNAMURTI
from engine.calculations.calculations import calculate
from engine.models.birth_data import BirthData
from engine.parashari.drishti import (
    ASPECTABLE_GRAHAS,
    DRISHTI_OFFSETS,
    ParashariProfileError,
    aspected_signs,
    graha_drishti_from_snapshot,
    parashari_drishti,
)

BIRTH = BirthData(1985, 12, 21, 14, 40, 0.0, 25.6, 85.1333, "Asia/Kolkata")

#: SECOND INDEPENDENT TRANSCRIPTION (Gate 1): the classical statement
#: by graha name: all grahas the 7th; Mars also 4th and 8th; Jupiter
#: also 5th and 9th; Saturn also 3rd and 10th.
SECOND_TRANSCRIPTION = {
    "Sun": {7}, "Moon": {7}, "Mercury": {7}, "Venus": {7},
    "Mars": {4, 7, 8}, "Jupiter": {5, 7, 9}, "Saturn": {3, 7, 10},
}


def test_offset_table_matches_second_transcription():
    assert set(DRISHTI_OFFSETS) == set(SECOND_TRANSCRIPTION)
    for planet, offsets in DRISHTI_OFFSETS.items():
        assert set(offsets) == SECOND_TRANSCRIPTION[planet], planet
        assert 7 in offsets  # every graha casts the 7th aspect
        assert all(2 <= offset <= 10 for offset in offsets)


def test_special_aspects_re_derivation():
    # Re-derivation from the classical statement: only the three
    # special-aspect grahas have more than the 7th; their extras are
    # symmetric around 6 (4+8=12, 5+9=14? no: Mars 4/8 symmetric
    # around 6; Jupiter 5/9 symmetric around 7; Saturn 3/10 is the
    # classical exception pair). Pin the exact sets instead of a
    # false symmetry: Mars kendra-from-4th, Jupiter trikona, Saturn
    # 3rd/10th.
    assert set(DRISHTI_OFFSETS["Mars"]) - {7} == {4, 8}
    assert set(DRISHTI_OFFSETS["Jupiter"]) - {7} == {5, 9}
    assert set(DRISHTI_OFFSETS["Saturn"]) - {7} == {3, 10}
    for planet in ("Sun", "Moon", "Mercury", "Venus"):
        assert set(DRISHTI_OFFSETS[planet]) == {7}


def test_combinatorial_12x12_against_independent_rule():
    # Gate 2: every (planet, occupied sign) pair; aspected signs
    # match an independently coded inclusive-counting rule.
    for planet, offsets in DRISHTI_OFFSETS.items():
        for sign in range(1, 13):
            expected = tuple(((sign - 1 + offset - 1) % 12) + 1 for offset in offsets)
            assert aspected_signs(planet, sign) == expected


def test_seventh_aspect_is_mutual_and_never_own_sign():
    for planet in DRISHTI_OFFSETS:
        for sign in range(1, 13):
            signs = aspected_signs(planet, sign)
            assert sign not in signs  # full drishti never hits own sign
            seventh = ((sign - 1 + 6) % 12) + 1
            assert seventh in signs
            # Mutuality at sign level: the 7th of the 7th is the origin.
            assert ((seventh - 1 + 6) % 12) + 1 == sign


def test_chart_integration_hand_derived_case_c():
    # Case C (1985-12-21 14:40 IST Patna, Lahiri): placements
    # verified against the certified D1; expectations hand-derived.
    chart = parashari_drishti(BIRTH)
    assert chart.ascendant_sign == 2  # Taurus lagna
    drishti = {d.name: d for d in chart.drishti}
    assert chart.planet_signs["Mars"] == 7  # Libra
    assert drishti["Mars"].aspected_signs == (10, 1, 2)
    assert drishti["Mars"].aspected_houses == (9, 12, 1)
    assert set(drishti["Mars"].aspected_planets) == {"Moon", "Jupiter", "Rahu"}
    assert drishti["Saturn"].aspected_signs == (10, 2, 5)
    assert drishti["Sun"].aspected_signs == (3,)
    # Moon in Aries aspects Libra where Mars and Ketu sit.
    assert set(drishti["Moon"].aspected_planets) == {"Mars", "Ketu"}


def test_nodes_cast_no_aspects_but_can_be_aspected():
    chart = parashari_drishti(BIRTH)
    casters = {d.name for d in chart.drishti}
    assert casters == set(DRISHTI_OFFSETS)
    assert "Rahu" not in casters and "Ketu" not in casters
    aspected = set().union(*(d.aspected_planets for d in chart.drishti))
    assert aspected & {"Rahu", "Ketu"}  # nodes appear as targets in this chart
    assert "Rahu" in ASPECTABLE_GRAHAS and "Ketu" in ASPECTABLE_GRAHAS


def test_outers_absent_entirely():
    chart = parashari_drishti(BIRTH)
    everything = set(chart.planet_signs) | {d.name for d in chart.drishti}
    everything |= set().union(*(d.aspected_planets for d in chart.drishti))
    assert not everything & {"Uranus", "Neptune", "Pluto"}


def test_profile_guard_rejects_kp_snapshot():
    snapshot = calculate(BIRTH, profile=KP_KRISHNAMURTI).snapshot
    with pytest.raises(ParashariProfileError):
        graha_drishti_from_snapshot(snapshot)


def test_provenance_carried():
    chart = parashari_drishti(BIRTH)
    assert chart.provenance.profile_name == "parashari_lahiri"
