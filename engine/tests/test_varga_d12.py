"""
VARGA_D12_V1 gates 1, 2, 4 (ADR-0010).
"""

import math

import pytest

from engine.astrology import CERTIFIED_PRODUCTION_VARGAS
from engine.astrology.divisional_chart import divisional_chart
from engine.astrology.varga_classifier import classify
from engine.astrology.varga_d12 import D12_PARASHARA, D12_SCHOOL, ensure_registered
from engine.astrology.varga_registry import (
    UnsupportedVargaError,
    get_varga_rule,
    register_varga_rule,
    registered_vargas,
    unregister_varga_rule,
)
from engine.astrology.varga_rules import rule_content_sha256
from engine.calculations.calculations import calculate
from engine.models.birth_data import BirthData

BIRTH = BirthData(1985, 12, 21, 14, 40, 0.0, 25.6, 85.1333, "Asia/Kolkata")

SIGN_ORDER = ("Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
              "Libra", "Scorpio", "Sagittarius", "Capricorn",
              "Aquarius", "Pisces")

#: SECOND INDEPENDENT TRANSCRIPTION (Gate 1): "the first dwadasamsa
#: is the sign itself", transcribed by sign NAME.
SECOND_TRANSCRIPTION_START = {
    "Aries": "Aries", "Taurus": "Taurus", "Gemini": "Gemini",
    "Cancer": "Cancer", "Leo": "Leo", "Virgo": "Virgo",
    "Libra": "Libra", "Scorpio": "Scorpio",
    "Sagittarius": "Sagittarius", "Capricorn": "Capricorn",
    "Aquarius": "Aquarius", "Pisces": "Pisces",
}


def test_table_matches_second_transcription_cell_by_cell():
    assert D12_PARASHARA.divisions == 12
    for source_index, source_name in enumerate(SIGN_ORDER):
        start = D12_PARASHARA.start_sign[source_index]
        assert SIGN_ORDER[start] == SECOND_TRANSCRIPTION_START[source_name]
        assert D12_PARASHARA.direction[source_index] == 1


def test_full_target_grid_re_derivation():
    # Independent re-derivation: division k of sign s lands on
    # (s + k) mod 12, for all 144 cells.
    for source in range(12):
        for division in range(12):
            probe = source * 30.0 + division * 2.5 + 1.25
            result = classify(probe, D12_PARASHARA)
            assert result.division_index == division
            assert result.d_sign == (source + division) % 12


def test_dense_sweep_against_independent_classical_rule():
    step = 360.0 / 51429
    for i in range(51429):
        longitude = i * step
        result = classify(longitude, D12_PARASHARA)
        source = int(longitude // 30.0)
        division = int((longitude - source * 30.0) // 2.5)
        assert result.division_index == division, longitude
        assert result.d_sign == (source + division) % 12, longitude
        assert 0.0 <= result.fraction < 1.0


def test_ulp_boundary_battery():
    # All 144 boundaries at 2.5 degree spacing. Locked convention as
    # verified in the D3 phase: intra-sign boundaries promote within
    # 1e-10; sign boundaries carry no tolerance in the source-sign
    # decomposition (documented pre-existing behavior).
    for k in range(144):
        boundary = k * 2.5
        at = classify(boundary, D12_PARASHARA)
        expected_division = k % 12
        assert at.division_index == expected_division, boundary
        assert at.fraction == 0.0

        just_below = boundary - 1e-11
        if just_below >= 0.0:
            promoted = classify(just_below, D12_PARASHARA)
            if k % 12 == 0:  # sign boundary: stays in previous sign's last division
                previous_sign = (k // 12 - 1) % 12
                assert promoted.division_index == 11, boundary
                assert promoted.d_sign == (previous_sign + 11) % 12, boundary
            else:
                assert (promoted.d_sign, promoted.division_index) == (
                    at.d_sign, at.division_index), boundary

        clearly_below = boundary - 1e-6
        if clearly_below >= 0.0:
            below = classify(clearly_below, D12_PARASHARA)
            assert below.division_index == (k - 1) % 12, boundary

        up = boundary
        for _ in range(3):
            up = math.nextafter(up, math.inf)
            result = classify(up, D12_PARASHARA)
            assert (result.d_sign, result.division_index) == (
                at.d_sign, at.division_index), boundary


def test_normalization_parity():
    for longitude in (-0.1, 360.0, 720.5, -720.5, 359.9999999999999):
        result = classify(longitude, D12_PARASHARA)
        reference = classify(longitude % 360.0, D12_PARASHARA)
        assert (result.d_sign, result.division_index) == (
            reference.d_sign, reference.division_index)


# ---------------------------------------------------------------- Gate 4

def test_registry_is_exactly_the_certified_set():
    ensure_registered()
    assert registered_vargas() == CERTIFIED_PRODUCTION_VARGAS
    assert (12, D12_SCHOOL) in registered_vargas()


def test_certified_d1_d9_d10_dispatch_unchanged():
    snapshot = calculate(BIRTH).snapshot
    assert type(divisional_chart(snapshot, 9)).__name__ == "NavamsaChart"
    assert type(divisional_chart(snapshot, 10)).__name__ == "DashamsaChart"


def test_other_vargas_still_refused():
    # D45 is excluded: certified and registered (ADR-0077, VARGA_D45_V1).
    snapshot = calculate(BIRTH).snapshot
    for division in (4, 16, 20, 27, 40, 60):  # D24 excluded: certified/registered (ADR-0082/0083, VARGA_D24_V1)
        with pytest.raises(UnsupportedVargaError):
            divisional_chart(snapshot, division)


def test_d12_served_through_dispatcher_with_provenance():
    snapshot = calculate(BIRTH).snapshot
    chart = divisional_chart(snapshot, 12)
    assert chart.varga == 12
    assert chart.school == D12_SCHOOL
    assert chart.provenance is snapshot.provenance


def test_reregistration_refused():
    with pytest.raises(ValueError):
        register_varga_rule(12, D12_SCHOOL, D12_PARASHARA)


# ------------------------------------------------------- Gate 4, B-02
# reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md.

#: Content fingerprint of the certified D12 table, pinned.
CERTIFIED_D12_CONTENT_SHA256 = (
    "224ece371b1fd024a49d545556e2f9b842343c44c17b9af666b7052b5e6cd195"
)


def test_registered_rule_identity_is_the_certified_object():
    ensure_registered()
    assert get_varga_rule(12, D12_SCHOOL) is D12_PARASHARA


def test_registered_rule_content_hash_matches_pinned_value():
    assert rule_content_sha256(D12_PARASHARA) == CERTIFIED_D12_CONTENT_SHA256


def test_negative_control_substituted_rule_is_detected():
    """Prove the identity and content checks above can actually fail."""

    import dataclasses

    # Aries' start sign changed from itself (0) to Taurus (1) - still a
    # structurally valid CyclicVargaRule (divisions unchanged), so only
    # B-02's checks catch it.
    tampered_start = (1,) + D12_PARASHARA.start_sign[1:]
    tampered = dataclasses.replace(D12_PARASHARA, start_sign=tampered_start)
    assert tampered.divisions == 12  # still a legitimate D12 registration

    unregister_varga_rule(12, D12_SCHOOL)
    try:
        register_varga_rule(12, D12_SCHOOL, tampered)

        assert get_varga_rule(12, D12_SCHOOL) is not D12_PARASHARA
        assert (
            rule_content_sha256(get_varga_rule(12, D12_SCHOOL))
            != CERTIFIED_D12_CONTENT_SHA256
        )
    finally:
        unregister_varga_rule(12, D12_SCHOOL)
        register_varga_rule(12, D12_SCHOOL, D12_PARASHARA)

    assert get_varga_rule(12, D12_SCHOOL) is D12_PARASHARA
    assert rule_content_sha256(D12_PARASHARA) == CERTIFIED_D12_CONTENT_SHA256
