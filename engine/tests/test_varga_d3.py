"""
VARGA_D3_V1 gates 1, 2, 4 (ADR-0009): table integrity,
mathematical verification, and framework non-invasiveness.
"""

import math

import pytest

from engine.astrology import varga_d3  # noqa: F401  (registers D3)
from engine.astrology.divisional_chart import divisional_chart
from engine.astrology.varga_classifier import classify
from engine.astrology.varga_d3 import D3_PARASHARA, D3_SCHOOL, ensure_registered
from engine.astrology.varga_registry import (
    UnsupportedVargaError,
    get_varga_rule,
    register_varga_rule,
    registered_vargas,
    unregister_varga_rule,
)
from engine.astrology.varga_rules import rule_content_sha256
from engine.astronomy.profile import PARASHARI_LAHIRI
from engine.calculations.calculations import calculate
from engine.models.birth_data import BirthData

BIRTH = BirthData(1985, 12, 21, 14, 40, 0.0, 25.6, 85.1333, "Asia/Kolkata")

#: SECOND INDEPENDENT TRANSCRIPTION (Gate 1): the classical statement
#: "first drekkana of the sign itself, second of the 5th, third of
#: the 9th", transcribed by sign NAME, independently of the literals
#: in varga_d3.py.
SECOND_TRANSCRIPTION = {
    "Aries": ("Aries", "Leo", "Sagittarius"),
    "Taurus": ("Taurus", "Virgo", "Capricorn"),
    "Gemini": ("Gemini", "Libra", "Aquarius"),
    "Cancer": ("Cancer", "Scorpio", "Pisces"),
    "Leo": ("Leo", "Sagittarius", "Aries"),
    "Virgo": ("Virgo", "Capricorn", "Taurus"),
    "Libra": ("Libra", "Aquarius", "Gemini"),
    "Scorpio": ("Scorpio", "Pisces", "Cancer"),
    "Sagittarius": ("Sagittarius", "Aries", "Leo"),
    "Capricorn": ("Capricorn", "Taurus", "Virgo"),
    "Aquarius": ("Aquarius", "Gemini", "Libra"),
    "Pisces": ("Pisces", "Cancer", "Scorpio"),
}
SIGN_ORDER = ("Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
              "Libra", "Scorpio", "Sagittarius", "Capricorn",
              "Aquarius", "Pisces")


def test_table_matches_second_transcription_cell_by_cell():
    for source_index, source_name in enumerate(SIGN_ORDER):
        segments = D3_PARASHARA.segments[source_index]
        assert len(segments) == 3
        for division_index, (width, target) in enumerate(segments):
            assert width == 10.0
            expected = SECOND_TRANSCRIPTION[source_name][division_index]
            assert SIGN_ORDER[target] == expected, (source_name, division_index)


def test_table_matches_trine_re_derivation():
    # Independent re-derivation: the three drekkana lords of a sign
    # are its trines: targets are source + 4k mod 12 and all share
    # the source's element (sign index mod 4).
    for source in range(12):
        for division, (_width, target) in enumerate(D3_PARASHARA.segments[source]):
            assert target == (source + 4 * division) % 12
            assert target % 4 == source % 4  # same element


def test_dense_sweep_against_independent_classical_rule():
    step = 360.0 / 51429
    for i in range(51429):
        longitude = i * step
        result = classify(longitude, D3_PARASHARA)
        source = int(longitude // 30.0)
        division = int((longitude - source * 30.0) // 10.0)
        assert result.division_index == division, longitude
        assert result.d_sign == (source + 4 * division) % 12, longitude
        assert 0.0 <= result.fraction < 1.0


def test_ulp_boundary_battery_promote_up():
    # Every 10-degree boundary in [0, 360): exact hit owns the new
    # division. The locked convention, exactly as certified for
    # D9/D10 and proven bit-identical in the framework mirrors:
    # INTRA-SIGN boundaries promote values within 1e-10 below them;
    # SIGN boundaries do not (the source-sign decomposition carries
    # no tolerance), so dust 1e-11 below a sign boundary stays in
    # the previous sign's LAST division. Pre-existing locked
    # behavior, verified here for D3 and recorded in the artifact.
    for k in range(36):
        boundary = k * 10.0
        at = classify(boundary, D3_PARASHARA)
        expected_division = k % 3
        assert at.division_index == expected_division, boundary
        assert at.fraction == 0.0

        just_below = boundary - 1e-11  # inside promote-up tolerance
        if just_below >= 0.0:
            promoted = classify(just_below, D3_PARASHARA)
            if k % 3 == 0:  # sign boundary: no promotion by design
                previous_sign = (k // 3 - 1) % 12
                assert promoted.division_index == 2, boundary
                assert promoted.d_sign == (previous_sign + 8) % 12, boundary
            else:  # intra-sign boundary: promoted up
                assert (promoted.d_sign, promoted.division_index) == (
                    at.d_sign, at.division_index), boundary

        clearly_below = boundary - 1e-6
        if clearly_below >= 0.0:
            below = classify(clearly_below, D3_PARASHARA)
            previous_division = (k - 1) % 3
            assert below.division_index == previous_division, boundary

        up = boundary
        for _ in range(3):
            up = math.nextafter(up, math.inf)
            result = classify(up, D3_PARASHARA)
            assert (result.d_sign, result.division_index) == (
                at.d_sign, at.division_index), boundary


def test_normalization_parity():
    for longitude in (-0.1, 360.0, 720.5, -720.5, 359.9999999999999):
        result = classify(longitude, D3_PARASHARA)
        reference = classify(longitude % 360.0, D3_PARASHARA)
        assert (result.d_sign, result.division_index) == (
            reference.d_sign, reference.division_index)


# ---------------------------------------------------------------- Gate 4

def test_registry_contains_the_certified_set_including_d3():
    ensure_registered()
    from engine.astrology import CERTIFIED_PRODUCTION_VARGAS

    assert registered_vargas() == CERTIFIED_PRODUCTION_VARGAS
    assert (3, D3_SCHOOL) in registered_vargas()


def test_certified_d1_d9_d10_dispatch_unchanged():
    snapshot = calculate(BIRTH, profile=PARASHARI_LAHIRI).snapshot
    d1 = divisional_chart(snapshot, 1)
    d9 = divisional_chart(snapshot, 9)
    d10 = divisional_chart(snapshot, 10)
    # Certified module types, NOT the generic VargaChart.
    assert type(d9).__name__ == "NavamsaChart"
    assert type(d10).__name__ == "DashamsaChart"
    assert type(d1).__name__ not in ("VargaChart",)


def test_other_vargas_still_refused():
    snapshot = calculate(BIRTH, profile=PARASHARI_LAHIRI).snapshot
    for division in (4, 16, 20, 24, 27, 40, 45, 60):
        with pytest.raises(UnsupportedVargaError):
            divisional_chart(snapshot, division)


def test_d3_served_through_dispatcher_with_provenance():
    snapshot = calculate(BIRTH, profile=PARASHARI_LAHIRI).snapshot
    chart = divisional_chart(snapshot, 3)
    assert chart.varga == 3
    assert chart.school == D3_SCHOOL
    assert chart.provenance is snapshot.provenance
    assert set(chart.planets) == set(snapshot.sidereal_planets)


def test_reregistration_refused_and_certified_divisions_blocked():
    with pytest.raises(ValueError):
        register_varga_rule(3, D3_SCHOOL, D3_PARASHARA)
    for division in (1, 9, 10):
        with pytest.raises(ValueError):
            register_varga_rule(division, D3_SCHOOL, D3_PARASHARA)


# ------------------------------------------------------- Gate 4, B-02
# reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md: a certified rule could be
# swapped at runtime while every non-invasiveness gate stayed green,
# because nothing checked object identity or content, only registry
# keys. These two checks close that; the negative control after them
# proves both can actually fail.

#: Content fingerprint of the certified D3 table, pinned. Any edit to
#: the literals in varga_d3.py that is not accompanied by updating
#: this constant (and recertifying) makes this test fail.
CERTIFIED_D3_CONTENT_SHA256 = (
    "11c561c05413ebc9d8b791c0c22e42e6a91efe2cbdaceaa1f6eeac66d9e957f4"
)


def test_registered_rule_identity_is_the_certified_object():
    ensure_registered()
    assert get_varga_rule(3, D3_SCHOOL) is D3_PARASHARA


def test_registered_rule_content_hash_matches_pinned_value():
    assert rule_content_sha256(D3_PARASHARA) == CERTIFIED_D3_CONTENT_SHA256


def test_negative_control_substituted_rule_is_detected():
    """Prove the identity and content checks above can actually fail."""

    import dataclasses

    # A single-cell edit: Aries' first segment now targets Taurus (1)
    # instead of Aries (0). Still a structurally valid SegmentVargaRule
    # (widths still sum to 30), so only B-02's checks catch it - B-01's
    # invariant is division/cardinality, not per-cell content.
    tampered_segments = (
        ((10.0, 1), (10.0, 4), (10.0, 8)),
    ) + D3_PARASHARA.segments[1:]
    tampered = dataclasses.replace(D3_PARASHARA, segments=tampered_segments)
    assert tampered.division == 3  # still a legitimate D3 registration

    unregister_varga_rule(3, D3_SCHOOL)
    try:
        register_varga_rule(3, D3_SCHOOL, tampered)

        # Identity check now fails: a different object is registered.
        assert get_varga_rule(3, D3_SCHOOL) is not D3_PARASHARA

        # Content check now fails: the tampered table hashes differently.
        assert (
            rule_content_sha256(get_varga_rule(3, D3_SCHOOL))
            != CERTIFIED_D3_CONTENT_SHA256
        )
    finally:
        unregister_varga_rule(3, D3_SCHOOL)
        register_varga_rule(3, D3_SCHOOL, D3_PARASHARA)

    # State fully restored: both checks pass again.
    assert get_varga_rule(3, D3_SCHOOL) is D3_PARASHARA
    assert rule_content_sha256(D3_PARASHARA) == CERTIFIED_D3_CONTENT_SHA256
