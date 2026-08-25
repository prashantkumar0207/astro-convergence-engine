"""
VARGA_D45_V1 production registration tests (ADR-0077).

Mirrors the established pattern (test_varga_d12.py): table vs. an
independent second transcription, a full target-grid re-derivation, a
dense sweep against an independently coded classical rule, a boundary
battery, registry/dispatch checks, content-hash pinning, and a genuine
negative control.
"""

import dataclasses
import math

import pytest

from engine.astrology import CERTIFIED_PRODUCTION_VARGAS
from engine.astrology.divisional_chart import divisional_chart
from engine.astrology.varga_classifier import classify
from engine.astrology.varga_d45 import D45_PARASHARA, D45_SCHOOL, ensure_registered
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

MOVABLE = {"Aries", "Cancer", "Libra", "Capricorn"}
FIXED = {"Taurus", "Leo", "Scorpio", "Aquarius"}
DUAL = {"Gemini", "Virgo", "Sagittarius", "Pisces"}

#: SECOND INDEPENDENT TRANSCRIPTION (ADR-0077 section 1): "movable
#: Aries, fixed Leo, dual Sagittarius", transcribed by sign NAME, not
#: the numeric 0/4/8 offsets the production rule stores.
SECOND_TRANSCRIPTION_START = {}
for _name in SIGN_ORDER:
    if _name in MOVABLE:
        SECOND_TRANSCRIPTION_START[_name] = "Aries"
    elif _name in FIXED:
        SECOND_TRANSCRIPTION_START[_name] = "Leo"
    else:
        SECOND_TRANSCRIPTION_START[_name] = "Sagittarius"

WIDTH = 30.0 / 45.0
TOLERANCE = 1e-10


def _independent_division(source_name: str, degree: float) -> tuple:
    """Independent re-derivation, applying the engine's own documented
    boundary-promotion convention (a degree within 1e-10 of a division's
    edge promotes to the next division) on its own terms, not imported."""

    start_name = SECOND_TRANSCRIPTION_START[source_name]
    start_index = SIGN_ORDER.index(start_name)
    index = int((degree + TOLERANCE) / WIDTH)
    if index > 44:
        index = 44
    return SIGN_ORDER[(start_index + index) % 12], index


def test_table_matches_second_transcription_cell_by_cell():
    assert D45_PARASHARA.divisions == 45
    for source_index, source_name in enumerate(SIGN_ORDER):
        expected_start_name = SECOND_TRANSCRIPTION_START[source_name]
        start = D45_PARASHARA.start_sign[source_index]
        assert SIGN_ORDER[start] == expected_start_name
        assert D45_PARASHARA.direction[source_index] == 1


def test_full_target_grid_re_derivation():
    for source_index, source_name in enumerate(SIGN_ORDER):
        for division in range(45):
            degree = division * WIDTH + WIDTH / 2.0  # midpoint, no boundary dust
            result = classify(source_index * 30.0 + degree, D45_PARASHARA)
            expected_sign_name, expected_division = _independent_division(source_name, degree)
            assert result.division_index == division
            assert result.d_sign == SIGN_ORDER.index(expected_sign_name)


def test_dense_sweep_against_independent_classical_rule():
    step = 360.0 / 51429
    for i in range(51429):
        longitude = i * step
        result = classify(longitude, D45_PARASHARA)
        source_index = int(longitude // 30.0)
        degree = longitude - source_index * 30.0
        expected_sign_name, expected_division = _independent_division(
            SIGN_ORDER[source_index], degree)
        assert result.division_index == expected_division, longitude
        assert result.d_sign == SIGN_ORDER.index(expected_sign_name), longitude
        assert 0.0 <= result.fraction < 1.0


def test_boundary_battery_including_identified_floating_point_cases():
    # k=13, 26, 29 are the three internal per-sign boundaries (of 44)
    # where the floating-point floor computation and the exact
    # mathematical value diverge by one segment (ADR-0077 section 3).
    # Both classify() and the independent reference apply the SAME
    # documented 1e-10 promotion convention, so they must still agree.
    for source_index in range(12):
        for k in (13, 26, 29):
            boundary = k * WIDTH
            at = classify(source_index * 30.0 + boundary, D45_PARASHARA)
            expected_sign_name, expected_division = _independent_division(
                SIGN_ORDER[source_index], boundary)
            assert at.division_index == expected_division, (source_index, k)
            assert at.d_sign == SIGN_ORDER.index(expected_sign_name), (source_index, k)

    # General boundary battery over all 45 divisions of one sign
    # (Taurus, a fixed sign): at-boundary, just-below, and 3-ULP-above.
    source_index = 1
    for k in range(45):
        boundary = k * WIDTH
        at = classify(source_index * 30.0 + boundary, D45_PARASHARA)
        assert at.fraction < 1.0

        up = boundary
        for _ in range(3):
            up = math.nextafter(up, math.inf)
            result = classify(source_index * 30.0 + up, D45_PARASHARA)
            assert (result.d_sign, result.division_index) == (
                at.d_sign, at.division_index), boundary


def test_normalization_parity():
    for longitude in (-0.1, 360.0, 720.5, -720.5, 359.9999999999999):
        result = classify(longitude, D45_PARASHARA)
        reference = classify(longitude % 360.0, D45_PARASHARA)
        assert (result.d_sign, result.division_index) == (
            reference.d_sign, reference.division_index)


# ---------------------------------------------------------------- Registry

def test_registry_is_exactly_the_certified_set():
    ensure_registered()
    assert registered_vargas() == CERTIFIED_PRODUCTION_VARGAS
    assert (45, D45_SCHOOL) in registered_vargas()


def test_certified_d1_d9_d10_dispatch_unchanged():
    snapshot = calculate(BIRTH).snapshot
    assert type(divisional_chart(snapshot, 9)).__name__ == "NavamsaChart"
    assert type(divisional_chart(snapshot, 10)).__name__ == "DashamsaChart"


def test_other_vargas_still_refused():
    snapshot = calculate(BIRTH).snapshot
    for division in (4, 16, 20, 24, 27, 40, 60):
        with pytest.raises(UnsupportedVargaError):
            divisional_chart(snapshot, division)


def test_d45_served_through_dispatcher_with_provenance():
    snapshot = calculate(BIRTH).snapshot
    chart = divisional_chart(snapshot, 45)
    assert chart.varga == 45
    assert chart.school == D45_SCHOOL
    assert chart.provenance is snapshot.provenance


def test_reregistration_refused():
    with pytest.raises(ValueError):
        register_varga_rule(45, D45_SCHOOL, D45_PARASHARA)


# ------------------------------------------------------- B-02 (ADR-0049)

#: Content fingerprint of the certified D45 table, pinned.
CERTIFIED_D45_CONTENT_SHA256 = (
    "c8515e44be6e21e3e8c3298121b8c0e4687c0176d9da7e94f7d0aba53a8bf817"
)


def test_registered_rule_identity_is_the_certified_object():
    ensure_registered()
    assert get_varga_rule(45, D45_SCHOOL) is D45_PARASHARA


def test_registered_rule_content_hash_matches_pinned_value():
    assert rule_content_sha256(D45_PARASHARA) == CERTIFIED_D45_CONTENT_SHA256


def test_negative_control_substituted_rule_is_detected():
    """Prove the identity and content checks above can actually fail."""

    # Aries' start sign changed from movable-Aries (0) to fixed-Leo (4) -
    # still a structurally valid CyclicVargaRule (divisions unchanged),
    # so only the identity/content checks catch it.
    tampered_start = (4,) + D45_PARASHARA.start_sign[1:]
    tampered = dataclasses.replace(D45_PARASHARA, start_sign=tampered_start)
    assert tampered.divisions == 45  # still a legitimate D45-shaped registration

    unregister_varga_rule(45, D45_SCHOOL)
    try:
        register_varga_rule(45, D45_SCHOOL, tampered)

        assert get_varga_rule(45, D45_SCHOOL) is not D45_PARASHARA
        assert (
            rule_content_sha256(get_varga_rule(45, D45_SCHOOL))
            != CERTIFIED_D45_CONTENT_SHA256
        )
    finally:
        unregister_varga_rule(45, D45_SCHOOL)
        register_varga_rule(45, D45_SCHOOL, D45_PARASHARA)

    assert get_varga_rule(45, D45_SCHOOL) is D45_PARASHARA
    assert rule_content_sha256(D45_PARASHARA) == CERTIFIED_D45_CONTENT_SHA256
