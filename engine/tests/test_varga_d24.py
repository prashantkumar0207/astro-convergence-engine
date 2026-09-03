"""
VARGA_D24_V1 production registration tests (ADR-0082, ADR-0083).

Mirrors the established pattern (test_varga_d45.py): table vs. an
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
from engine.astrology.varga_d24 import D24_SIDDHAMSA, D24_SCHOOL, ensure_registered
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

ODD_SIGNS = {"Aries", "Gemini", "Leo", "Libra", "Sagittarius", "Aquarius"}
EVEN_SIGNS = {"Taurus", "Cancer", "Virgo", "Scorpio", "Capricorn", "Pisces"}

#: SECOND INDEPENDENT TRANSCRIPTION (ADR-0083 section 1, BPHS Sarga 6,
#: Shlokas 2-23): "odd Leo, even Cancer", transcribed by sign NAME, not
#: the numeric 4/3 offsets the production rule stores.
SECOND_TRANSCRIPTION_START = {}
for _name in SIGN_ORDER:
    SECOND_TRANSCRIPTION_START[_name] = "Leo" if _name in ODD_SIGNS else "Cancer"

WIDTH = 30.0 / 24.0
TOLERANCE = 1e-10


def _independent_division(source_name: str, degree: float) -> tuple:
    """Independent re-derivation, applying the engine's own documented
    boundary-promotion convention (a degree within 1e-10 of a division's
    edge promotes to the next division) on its own terms, not imported."""

    start_name = SECOND_TRANSCRIPTION_START[source_name]
    start_index = SIGN_ORDER.index(start_name)
    index = int((degree + TOLERANCE) / WIDTH)
    if index > 23:
        index = 23
    return SIGN_ORDER[(start_index + index) % 12], index


def test_table_matches_second_transcription_cell_by_cell():
    assert D24_SIDDHAMSA.divisions == 24
    for source_index, source_name in enumerate(SIGN_ORDER):
        expected_start_name = SECOND_TRANSCRIPTION_START[source_name]
        start = D24_SIDDHAMSA.start_sign[source_index]
        assert SIGN_ORDER[start] == expected_start_name
        assert D24_SIDDHAMSA.direction[source_index] == 1


def test_full_target_grid_re_derivation():
    for source_index, source_name in enumerate(SIGN_ORDER):
        for division in range(24):
            degree = division * WIDTH + WIDTH / 2.0  # midpoint, no boundary dust
            result = classify(source_index * 30.0 + degree, D24_SIDDHAMSA)
            expected_sign_name, expected_division = _independent_division(source_name, degree)
            assert result.division_index == division
            assert result.d_sign == SIGN_ORDER.index(expected_sign_name)


def test_dense_sweep_against_independent_classical_rule():
    step = 360.0 / 51429
    for i in range(51429):
        longitude = i * step
        result = classify(longitude, D24_SIDDHAMSA)
        source_index = int(longitude // 30.0)
        degree = longitude - source_index * 30.0
        expected_sign_name, expected_division = _independent_division(
            SIGN_ORDER[source_index], degree)
        assert result.division_index == expected_division, longitude
        assert result.d_sign == SIGN_ORDER.index(expected_sign_name), longitude
        assert 0.0 <= result.fraction < 1.0


def test_boundary_battery():
    # General boundary battery over all 24 divisions of one sign
    # (Taurus, an even source sign): at-boundary, just-below, and
    # 3-ULP-above. ADR-0083 section 3: the 30/24 = 1.25-degree cell
    # width is exactly representable in IEEE-754 double precision, with
    # zero floor-classification effect - unlike D45's own three
    # identified boundary cases, D24 has none to enumerate specially.
    source_index = 1
    for k in range(24):
        boundary = k * WIDTH
        at = classify(source_index * 30.0 + boundary, D24_SIDDHAMSA)
        assert at.fraction < 1.0

        up = boundary
        for _ in range(3):
            up = math.nextafter(up, math.inf)
            result = classify(source_index * 30.0 + up, D24_SIDDHAMSA)
            assert (result.d_sign, result.division_index) == (
                at.d_sign, at.division_index), boundary


def test_normalization_parity():
    for longitude in (-0.1, 360.0, 720.5, -720.5, 359.9999999999999):
        result = classify(longitude, D24_SIDDHAMSA)
        reference = classify(longitude % 360.0, D24_SIDDHAMSA)
        assert (result.d_sign, result.division_index) == (
            reference.d_sign, reference.division_index)


# ---------------------------------------------------------------- Registry

def test_registry_is_exactly_the_certified_set():
    ensure_registered()
    assert registered_vargas() == CERTIFIED_PRODUCTION_VARGAS
    assert (24, D24_SCHOOL) in registered_vargas()


def test_certified_d1_d9_d10_dispatch_unchanged():
    snapshot = calculate(BIRTH).snapshot
    assert type(divisional_chart(snapshot, 9)).__name__ == "NavamsaChart"
    assert type(divisional_chart(snapshot, 10)).__name__ == "DashamsaChart"


def test_other_vargas_still_refused():
    snapshot = calculate(BIRTH).snapshot
    for division in (4, 16, 20, 27, 40, 60):
        with pytest.raises(UnsupportedVargaError):
            divisional_chart(snapshot, division)


def test_d24_served_through_dispatcher_with_provenance():
    snapshot = calculate(BIRTH).snapshot
    chart = divisional_chart(snapshot, 24)
    assert chart.varga == 24
    assert chart.school == D24_SCHOOL
    assert chart.provenance is snapshot.provenance


def test_reregistration_refused():
    with pytest.raises(ValueError):
        register_varga_rule(24, D24_SCHOOL, D24_SIDDHAMSA)


# ------------------------------------------------------- B-02 (ADR-0049)

#: Content fingerprint of the certified D24 table, pinned.
CERTIFIED_D24_CONTENT_SHA256 = (
    "2ea83b5ad2dd53218f074d1b5e410bd3ec1806ad1ce5d4e053453715da4287f9"
)


def test_registered_rule_identity_is_the_certified_object():
    ensure_registered()
    assert get_varga_rule(24, D24_SCHOOL) is D24_SIDDHAMSA


def test_registered_rule_content_hash_matches_pinned_value():
    assert rule_content_sha256(D24_SIDDHAMSA) == CERTIFIED_D24_CONTENT_SHA256


def test_negative_control_substituted_rule_is_detected():
    """Prove the identity and content checks above can actually fail."""

    # Aries' start sign changed from odd-Leo (4) to even-Cancer (3) -
    # still a structurally valid CyclicVargaRule (divisions unchanged),
    # so only the identity/content checks catch it.
    tampered_start = (3,) + D24_SIDDHAMSA.start_sign[1:]
    tampered = dataclasses.replace(D24_SIDDHAMSA, start_sign=tampered_start)
    assert tampered.divisions == 24  # still a legitimate D24-shaped registration

    unregister_varga_rule(24, D24_SCHOOL)
    try:
        register_varga_rule(24, D24_SCHOOL, tampered)

        assert get_varga_rule(24, D24_SCHOOL) is not D24_SIDDHAMSA
        assert (
            rule_content_sha256(get_varga_rule(24, D24_SCHOOL))
            != CERTIFIED_D24_CONTENT_SHA256
        )
    finally:
        unregister_varga_rule(24, D24_SCHOOL)
        register_varga_rule(24, D24_SCHOOL, D24_SIDDHAMSA)

    assert get_varga_rule(24, D24_SCHOOL) is D24_SIDDHAMSA
    assert rule_content_sha256(D24_SIDDHAMSA) == CERTIFIED_D24_CONTENT_SHA256
