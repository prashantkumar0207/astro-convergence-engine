"""D20 Vimsamsa production tests (VARGA_D20_V1, ADR-0095).

Mirrors test_varga_d40.py's structure exactly: a second independent
transcription keyed by sign NAME, a full target-grid re-derivation, a
dense sweep, a boundary battery, normalisation parity, registry state,
B-02 identity/content pinning, and a genuine negative control.

ADR-0095 section 3: Variant F (movable Aries, fixed LEO, dual
SAGITTARIUS - the fixed/dual transposition) is EXCLUDED as the selected
methodology but is ATTESTED and NOT REFUTED. A dedicated test below
proves the production rule is distinguishable from it, so Variant F
cannot silently become an alternative production interpretation. That
test refutes nothing about the reading itself.
"""

import dataclasses
import math

import pytest

from engine.astrology import CERTIFIED_PRODUCTION_VARGAS
from engine.astrology.divisional_chart import divisional_chart
from engine.astrology.varga_classifier import classify
from engine.astrology.varga_d20 import D20_VIMSAMSA, D20_SCHOOL, ensure_registered
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

MOVABLE_SIGNS = {"Aries", "Cancer", "Libra", "Capricorn"}
FIXED_SIGNS = {"Taurus", "Leo", "Scorpio", "Aquarius"}
DUAL_SIGNS = {"Gemini", "Virgo", "Sagittarius", "Pisces"}

#: SECOND INDEPENDENT TRANSCRIPTION (ADR-0095 section 1, the translated
#: BPHS verse): "From Aries for a Movable Rasi, from Sagittarius for a
#: Fixed Rasi and from Leo for a Common Rasi" - transcribed by sign NAME,
#: not the numeric 0/8/4 offsets the production rule stores.
SECOND_TRANSCRIPTION_START = {}
for _name in SIGN_ORDER:
    if _name in MOVABLE_SIGNS:
        SECOND_TRANSCRIPTION_START[_name] = "Aries"
    elif _name in FIXED_SIGNS:
        SECOND_TRANSCRIPTION_START[_name] = "Sagittarius"
    else:
        SECOND_TRANSCRIPTION_START[_name] = "Leo"

#: ADR-0095's EXCLUDED Variant F, transcribed by name for the
#: distinguishability test below. Never used as a reference for
#: correctness - only to prove the production rule is not this.
VARIANT_F_START = {}
for _name in SIGN_ORDER:
    if _name in MOVABLE_SIGNS:
        VARIANT_F_START[_name] = "Aries"
    elif _name in FIXED_SIGNS:
        VARIANT_F_START[_name] = "Leo"
    else:
        VARIANT_F_START[_name] = "Sagittarius"

WIDTH = 30.0 / 20.0
TOLERANCE = 1e-10


def _independent_division(source_name: str, degree: float) -> tuple:
    """Independent re-derivation, applying the engine's own documented
    boundary-promotion convention (a degree within 1e-10 of a division's
    edge promotes to the next division) on its own terms, not imported."""

    start_name = SECOND_TRANSCRIPTION_START[source_name]
    start_index = SIGN_ORDER.index(start_name)
    index = int((degree + TOLERANCE) / WIDTH)
    if index > 19:
        index = 19
    return SIGN_ORDER[(start_index + index) % 12], index


def test_table_matches_second_transcription_cell_by_cell():
    assert D20_VIMSAMSA.divisions == 20
    for source_index, source_name in enumerate(SIGN_ORDER):
        expected_start_name = SECOND_TRANSCRIPTION_START[source_name]
        start = D20_VIMSAMSA.start_sign[source_index]
        assert SIGN_ORDER[start] == expected_start_name
        assert D20_VIMSAMSA.direction[source_index] == 1


def test_full_target_grid_re_derivation():
    for source_index, source_name in enumerate(SIGN_ORDER):
        for division in range(20):
            degree = division * WIDTH + WIDTH / 2.0  # midpoint, no boundary dust
            result = classify(source_index * 30.0 + degree, D20_VIMSAMSA)
            expected_sign_name, expected_division = _independent_division(source_name, degree)
            assert result.division_index == division
            assert result.d_sign == SIGN_ORDER.index(expected_sign_name)


def test_dense_sweep_against_independent_classical_rule():
    step = 360.0 / 51429
    for i in range(51429):
        longitude = i * step
        result = classify(longitude, D20_VIMSAMSA)
        source_index = int(longitude // 30.0)
        degree = longitude - source_index * 30.0
        expected_sign_name, expected_division = _independent_division(
            SIGN_ORDER[source_index], degree)
        assert result.division_index == expected_division, longitude
        assert result.d_sign == SIGN_ORDER.index(expected_sign_name), longitude
        assert 0.0 <= result.fraction < 1.0


def test_boundary_battery():
    # Boundary battery over all 20 divisions of one sign (Taurus, a
    # FIXED source sign, so it exercises the Sagittarius start that
    # Variant F would have made Leo). ADR-0095/DP-036: the 30/20 = 1.5
    # degree cell width and every internal boundary k*1.5 are EXACT
    # binary fractions, so there is no representability effect at all.
    source_index = 1
    for k in range(20):
        boundary = k * WIDTH
        at = classify(source_index * 30.0 + boundary, D20_VIMSAMSA)
        assert at.fraction < 1.0

        up = boundary
        for _ in range(3):
            up = math.nextafter(up, math.inf)
            result = classify(source_index * 30.0 + up, D20_VIMSAMSA)
            assert (result.d_sign, result.division_index) == (
                at.d_sign, at.division_index), boundary


def test_every_internal_boundary_is_exactly_representable():
    """D20-specific: unlike D7/D9/D27 there is no representability error,
    so a boundary disagreement could only be a table/convention defect."""

    from fractions import Fraction

    assert Fraction(WIDTH) == Fraction(3, 2)
    for k in range(1, 20):
        assert Fraction(k * WIDTH) == Fraction(3 * k, 2), k


def test_normalization_parity():
    for longitude in (-0.1, 360.0, 720.5, -720.5, 359.9999999999999):
        result = classify(longitude, D20_VIMSAMSA)
        reference = classify(longitude % 360.0, D20_VIMSAMSA)
        assert (result.d_sign, result.division_index) == (
            reference.d_sign, reference.division_index)


# ---------------------------------------------------------------- Registry

def test_registry_is_exactly_the_certified_set():
    ensure_registered()
    assert registered_vargas() == CERTIFIED_PRODUCTION_VARGAS
    assert (20, D20_SCHOOL) in registered_vargas()


def test_certified_d1_d9_d10_dispatch_unchanged():
    snapshot = calculate(BIRTH).snapshot
    assert type(divisional_chart(snapshot, 9)).__name__ == "NavamsaChart"
    assert type(divisional_chart(snapshot, 10)).__name__ == "DashamsaChart"


def test_other_vargas_still_refused():
    snapshot = calculate(BIRTH).snapshot
    for division in (4, 16, 27, 60):  # D24/D40 excluded: certified/registered; D20 now registered (ADR-0095)
        with pytest.raises(UnsupportedVargaError):
            divisional_chart(snapshot, division)


def test_d20_served_through_dispatcher_with_provenance():
    snapshot = calculate(BIRTH).snapshot
    chart = divisional_chart(snapshot, 20)
    assert chart.varga == 20
    assert chart.school == D20_SCHOOL
    assert chart.provenance is snapshot.provenance


def test_reregistration_refused():
    with pytest.raises(ValueError):
        register_varga_rule(20, D20_SCHOOL, D20_VIMSAMSA)


# ------------------------------------------------------- B-02 (ADR-0049)

#: Content fingerprint of the certified D20 table, pinned. Identical to
#: the value ADR-0095 froze and scripts/certify_d20.py enforces.
CERTIFIED_D20_CONTENT_SHA256 = (
    "efd08cea451084fedbe444c5473d6d50dfc589055b585f172e8a6e537668dac0"
)


def test_registered_rule_identity_is_the_certified_object():
    ensure_registered()
    assert get_varga_rule(20, D20_SCHOOL) is D20_VIMSAMSA


def test_registered_rule_content_hash_matches_pinned_value():
    assert rule_content_sha256(D20_VIMSAMSA) == CERTIFIED_D20_CONTENT_SHA256


def test_production_rule_is_not_the_excluded_variant_f():
    """ADR-0095 section 3: Variant F must not silently become an
    alternative production interpretation. This proves the registered
    rule is distinguishable from it. It refutes NOTHING about Variant F
    as a reading - that remains attested and not refuted."""

    for source_index, source_name in enumerate(SIGN_ORDER):
        certified_start = SIGN_ORDER[D20_VIMSAMSA.start_sign[source_index]]
        assert certified_start == SECOND_TRANSCRIPTION_START[source_name]
        if source_name in FIXED_SIGNS or source_name in DUAL_SIGNS:
            # exactly where the two readings disagree
            assert certified_start != VARIANT_F_START[source_name], source_name

    # And the disagreement is observable in real output, not just the table.
    taurus_probe = 30.0 + 7.3   # Taurus (fixed): certified Sagittarius, Variant F Leo
    variant_f = dataclasses.replace(
        D20_VIMSAMSA,
        start_sign=tuple(SIGN_ORDER.index(VARIANT_F_START[n]) for n in SIGN_ORDER),
    )
    assert classify(taurus_probe, variant_f).d_sign != classify(taurus_probe, D20_VIMSAMSA).d_sign
    assert rule_content_sha256(variant_f) != CERTIFIED_D20_CONTENT_SHA256


def test_negative_control_substituted_rule_is_detected():
    """Prove the identity and content checks above can actually fail."""

    # Taurus' start sign changed from Sagittarius (8) to Leo (4) - that is
    # exactly Variant F's transposition for a fixed sign, and it remains a
    # structurally valid CyclicVargaRule (divisions unchanged), so only the
    # identity/content checks catch it.
    tampered_start = (D20_VIMSAMSA.start_sign[0], 4) + D20_VIMSAMSA.start_sign[2:]
    tampered = dataclasses.replace(D20_VIMSAMSA, start_sign=tampered_start)
    assert tampered.divisions == 20  # still a legitimate D20-shaped registration

    unregister_varga_rule(20, D20_SCHOOL)
    try:
        register_varga_rule(20, D20_SCHOOL, tampered)

        assert get_varga_rule(20, D20_SCHOOL) is not D20_VIMSAMSA
        assert (
            rule_content_sha256(get_varga_rule(20, D20_SCHOOL))
            != CERTIFIED_D20_CONTENT_SHA256
        )
    finally:
        unregister_varga_rule(20, D20_SCHOOL)
        register_varga_rule(20, D20_SCHOOL, D20_VIMSAMSA)

    assert get_varga_rule(20, D20_SCHOOL) is D20_VIMSAMSA
    assert rule_content_sha256(D20_VIMSAMSA) == CERTIFIED_D20_CONTENT_SHA256
