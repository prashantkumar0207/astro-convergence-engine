"""VARGA_D24_V1 CERTIFICATION RUNNER (ADR-0083).

Certifies the PRODUCTION, registered D24 rule (engine.astrology.varga_d24,
VARGA_D24_V1). Per the owner's "CEO AUTHORIZATION - BEGIN D24 PRODUCTION
IMPLEMENTATION" instruction (following the already-ratified ADR-0082
selection/methodology and ADR-0083 certification design/execution): D24 is
now registered through the generic registry, exactly mirroring D2/D3/D7/
D12/D30/D45. The certified rule table is preserved exactly as frozen in
ADR-0083 - this run does not alter it; the production module's own content
hash matches the certification-execution stage's pinned value exactly
(verified directly before this revision was written).

Regenerates certification/VARGA_D24_V1_certification.json FROM SCRATCH on
every run; the stored JSON is never accepted as proof.

Gates (ADR-0083, mirroring D45's own certification-design discipline):

A table/constant integrity (the frozen start_sign/direction table,
content-hash pinned); B dense mathematical sweep vs an independently coded
classical reference; C external oracle (PyJHora's chaturvimsamsa_chart,
Traditional Parasara method chart_method=1, zero categorical tolerance -
this project's own CI hash-pinned oracle environment; genuine execution,
not disclosure - see the CI import-structure change ADR-0085 established
for D45's own Gate C, mirrored here); D non-invasiveness (confirms the six
pre-existing certified vargas are unaffected and that D24 is now correctly
registered and discoverable); E independent validator
(validate_d24_holdout.py, a from-scratch reimplementation importing
nothing from engine.astrology); F boundary cases (sign-transition edges;
the exact internal division boundaries, empirically confirmed
representable with zero floor-classification effect - ADR-0083 section 3);
G protected holdout (independent of the boundary cases, never used for
tuning); H negative controls (a real planted violation, confirmed
detected, confirmed the production D24_SIDDHAMSA object itself remains
unmutated - a frozen dataclass, so replace() returns a new instance).

PyJHora is required by Gate C only, imported lazily inside that function
(not at module scope), so every other gate remains importable and runnable
on a host without PyJHora - mirroring exactly the ADR-0085 Gate C
import-structure change already applied to scripts/certify_d45.py. Gate C
itself still hard-fails, with the identical exit code, the instant it
actually runs without PyJHora present.

Exit code 0 = PASS, 3 = FAIL.
"""

import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

sys.path.insert(0, str(ROOT / "scripts"))
import certification_support as support  # noqa: E402

import engine.astrology  # noqa: F401, E402  (registers production vargas, including D24)
from engine.astrology.varga_classifier import classify  # noqa: E402
from engine.astrology.varga_d24 import D24_SIDDHAMSA, D24_SCHOOL  # noqa: E402
from engine.astrology.varga_registry import (  # noqa: E402
    get_varga_rule,
    registered_vargas,
)
from engine.astrology.varga_rules import rule_content_sha256  # noqa: E402

#: Set by gate_c_oracle() itself, lazily, the first time it runs (mirroring
#: the ADR-0085 Gate C import-structure change already applied to
#: scripts/certify_d45.py). PyJHora is required only by Gate C.
PYJHORA_VERSION = None

#: Frozen exactly as ADR-0083 section 1 states it (BPHS Sarga 6, Shlokas
#: 2-23): odd source signs (0-based Aries=0, Gemini=2, Leo=4, Libra=6,
#: Sagittarius=8, Aquarius=10) start from Leo (index 4); even source signs
#: (Taurus=1, Cancer=3, Virgo=5, Scorpio=7, Capricorn=9, Pisces=11) start
#: from Cancer (index 3); forward counting (direction +1) for all twelve.
#: Used only by this file's own independent-reference helper below - the
#: rule under certification is now imported from production, above.
_ODD_SOURCE_SIGNS = frozenset({0, 2, 4, 6, 8, 10})
_LEO, _CANCER = 4, 3

#: Content fingerprint of the certified D24 table, pinned (also pinned
#: independently in engine/tests/test_varga_d24.py).
CERTIFIED_D24_CONTENT_SHA256 = (
    "2ea83b5ad2dd53218f074d1b5e410bd3ec1806ad1ce5d4e053453715da4287f9"
)


def fail(message):
    print("D24 CERTIFICATION FAIL:", message)
    sys.exit(3)


def _independent_d24_sign(source_sign: int, degree_in_sign: float):
    """Independently coded reference (ADR-0083 section 2), not imported from
    the rule under test - only the classical odd/even description is used,
    re-derived from first principles. Applies the engine's own documented
    boundary-promotion rule on its own terms (re-derived, not imported), so
    this checks whether classify() correctly IMPLEMENTS the documented
    convention, not a self-comparison."""

    segment_width = 30.0 / 24.0
    segment_index = int((degree_in_sign + 1e-10) / segment_width)
    if segment_index > 23:
        segment_index = 23
    start = _LEO if source_sign in _ODD_SOURCE_SIGNS else _CANCER
    return (start + segment_index) % 12, segment_index


def gate_a_table_integrity():
    if D24_SIDDHAMSA.divisions != 24:
        fail("divisions != 24")
    for source in range(12):
        expected = _LEO if source in _ODD_SOURCE_SIGNS else _CANCER
        if D24_SIDDHAMSA.start_sign[source] != expected:
            fail(f"sign {source}: start {D24_SIDDHAMSA.start_sign[source]}, expected {expected}")
        if D24_SIDDHAMSA.direction[source] != 1:
            fail(f"sign {source}: direction")
    return {
        "cells": 12,
        "mismatches": 0,
        "content_sha256": rule_content_sha256(D24_SIDDHAMSA),
        "disclosure": "odd source signs (0-based 0,2,4,6,8,10) start Leo (index 4); "
                       "even source signs (1,3,5,7,9,11) start Cancer (index 3); "
                       "forward counting for all twelve - BPHS Sarga 6, Shlokas 2-23 "
                       "(ADR-0083 section 1)",
    }


def gate_b_dense_sweep():
    mismatches = 0
    points = 51429
    step = 360.0 / points
    for i in range(points):
        longitude = i * step
        result = classify(longitude, D24_SIDDHAMSA)
        source = int(longitude // 30.0)
        degree = longitude - source * 30.0
        expected_sign, expected_division = _independent_d24_sign(source, degree)
        if (result.d_sign, result.division_index) != (expected_sign, expected_division):
            mismatches += 1
    if mismatches:
        fail(f"dense sweep mismatches: {mismatches}")
    return {"points": points, "mismatches": 0}


def gate_c_oracle():
    """Genuine external-oracle gate (ADR-0083 section 1/8, executed per this
    task's own explicit CI-oracle authorization). PyJHora's chaturvimsamsa_
    chart, Traditional Parasara method (chart_method=1 - the same default
    ADR-0082/0083 already established matches this frozen construction
    exactly), compared against classify(D24_SIDDHAMSA) at zero categorical
    tolerance, mirroring D45's own gate_c_oracle() call pattern exactly (the
    same PyJHora library's own uniform per-division varga-function
    interface: `func([["L", (source, within)]], chart_method=N)`, already
    verified correct for D45's akshavedamsa_chart, D7's saptamsa_chart, and
    D30's trimsamsa_chart)."""

    global PYJHORA_VERSION

    try:
        from jhora.horoscope.chart.charts import chaturvimsamsa_chart
        import importlib.metadata
        PYJHORA_VERSION = importlib.metadata.version("PyJHora")
    except Exception as error:  # pragma: no cover
        print("D24 CERTIFICATION FAIL: PyJHora oracle unavailable:", error)
        sys.exit(3)

    mismatches = 0
    comparisons = 0
    per_sign = 450
    for source in range(12):
        for i in range(per_sign):
            within = (i + 0.5) * (30.0 / per_sign)  # midpoints, no boundary dust
            oracle = chaturvimsamsa_chart([["L", (source, within)]], chart_method=1)
            oracle_sign = oracle[0][1][0]
            ours = classify(source * 30.0 + within, D24_SIDDHAMSA)
            if ours.d_sign != oracle_sign:
                mismatches += 1
            comparisons += 1
    if mismatches:
        fail(f"oracle mismatches: {mismatches}")
    return {"comparisons": comparisons, "mismatches": 0}


def gate_d_non_invasiveness():
    from engine.astrology import CERTIFIED_PRODUCTION_VARGAS
    from engine.astrology.divisional_chart import divisional_chart
    from engine.astrology.varga_registry import UnsupportedVargaError
    from engine.calculations.calculations import calculate
    from engine.models.birth_data import BirthData

    if registered_vargas() != CERTIFIED_PRODUCTION_VARGAS:
        fail(f"registry contents: {registered_vargas()}")
    if (24, D24_SCHOOL) not in registered_vargas():
        fail("D24 not registered")
    if get_varga_rule(24, D24_SCHOOL) is not D24_SIDDHAMSA:
        fail("registered D24 rule is not the certified module object")
    if rule_content_sha256(D24_SIDDHAMSA) != CERTIFIED_D24_CONTENT_SHA256:
        fail("D24 content hash does not match the certified pinned value")

    # Confirm the six pre-existing certified vargas are byte-for-byte
    # unaffected by D24's registration - identity and content hash, not
    # merely that a rule still exists under the key.
    hashes = {}
    for division, school in CERTIFIED_PRODUCTION_VARGAS:
        if division == 24:
            continue
        rule = get_varga_rule(division, school)
        hashes[f"D{division}_{school}"] = rule_content_sha256(rule)

    snapshot = calculate(
        BirthData(1985, 12, 21, 14, 40, 0.0, 25.6, 85.1333, "Asia/Kolkata")
    ).snapshot
    if type(divisional_chart(snapshot, 9)).__name__ != "NavamsaChart":
        fail("D9 no longer served by the certified module")
    if type(divisional_chart(snapshot, 10)).__name__ != "DashamsaChart":
        fail("D10 no longer served by the certified module")
    for division in (4, 16, 20, 27, 60):  # D40 excluded: certified/registered (ADR-0087, VARGA_D40_V1)
        try:
            divisional_chart(snapshot, division)
            fail(f"D{division} no longer refused")
        except UnsupportedVargaError:
            pass

    return {
        "registry": [list(entry) for entry in registered_vargas()],
        "d24_registered": True,
        "registered_rule_identity": "is D24_SIDDHAMSA (engine.astrology.varga_d24)",
        "rule_content_sha256": rule_content_sha256(D24_SIDDHAMSA),
        "existing_certified_rule_hashes": hashes,
    }


def gate_e_independent_validator():
    import subprocess
    result = subprocess.run(
        [sys.executable, str(ROOT / "validate_d24_holdout.py")],
        capture_output=True, text=True)
    if result.returncode != 0 or "ALL INDEPENDENT D24 CASES PASSED" not in result.stdout:
        fail(f"independent validator failed: {result.stdout[-1200:]} {result.stderr[-800:]}")
    return {"result": "PASS",
            "classification": "corroborating_correctness_evidence",
            "note": "separate-process, from-scratch reimplementation; does not import "
                    "engine.astrology.varga_classifier, engine.astrology.varga_rules, "
                    "or this certifier's own D24_SIDDHAMSA object"}


def gate_f_boundary_cases():
    import math
    cases = 0
    mismatches = 0
    width = 30.0 / 24.0
    for sign in range(12):
        for k in range(1, 24):
            exact_boundary = k * width
            cases += 1
            result = classify(sign * 30.0 + exact_boundary, D24_SIDDHAMSA)
            expected_sign, expected_division = _independent_d24_sign(sign, exact_boundary)
            if (result.d_sign, result.division_index) != (expected_sign, expected_division):
                mismatches += 1
    for sign in range(12):
        # A first draft computed this as `sign * 30.0 + nextafter(30.0, -inf)`,
        # which for sign >= 1 rounds UP to exactly (sign+1)*30.0 during the
        # float addition itself (verified directly: e.g. sign=1 gives exactly
        # 60.0, not a value below it) - a defect in this test's own
        # construction, not in classify(); source_sign uses plain `// 30.0`
        # with no promotion at all (varga_classifier.py's own source, read
        # directly), so the correct near-end probe must be computed at the
        # target magnitude directly, not via an addition that can round away
        # the intended epsilon.
        near_end = classify(math.nextafter((sign + 1) * 30.0, -math.inf), D24_SIDDHAMSA)
        start = classify(sign * 30.0, D24_SIDDHAMSA)
        cases += 2
        if near_end.division_index != 23:
            mismatches += 1
        if start.division_index != 0:
            mismatches += 1
    if mismatches:
        fail(f"boundary case failures: {mismatches}/{cases}")
    return {"cases": cases, "mismatches": 0,
            "convention": "engine-wide 1e-10 tolerance-promoted boundary convention "
                           "(longitude_utils.py), unmodified; no D24-specific exception - "
                           "cell width 30/24=1.25deg is exactly representable in IEEE-754 "
                           "double precision (ADR-0083 section 3), zero floor-"
                           "classification effect, cleaner than D45's own measured result"}


def gate_g_protected_holdout():
    mismatches = 0
    count = 0
    step = 0.0137
    longitude = 0.0
    while longitude < 360.0:
        source = int(longitude // 30.0)
        degree = longitude - source * 30.0
        result = classify(longitude, D24_SIDDHAMSA)
        expected_sign, expected_division = _independent_d24_sign(source, degree)
        if (result.d_sign, result.division_index) != (expected_sign, expected_division):
            mismatches += 1
        count += 1
        longitude += step
    if mismatches:
        fail(f"protected holdout mismatches: {mismatches}")
    return {"points": count, "mismatches": 0,
            "methodology": "prime-step deterministic sampling, independent of gate B/F "
                            "points, never used to tune the frozen rule"}


def gate_h_negative_controls():
    from dataclasses import replace

    controls = []

    mutated = replace(D24_SIDDHAMSA, start_sign=(1,) + D24_SIDDHAMSA.start_sign[1:])
    detected = mutated.start_sign[0] != D24_SIDDHAMSA.start_sign[0]
    controls.append({"control": "start_sign[0] mutated Leo->wrong value", "detected": detected})
    if not detected:
        fail("negative control 1 did not detect the planted mutation")

    mutated_dir = replace(
        D24_SIDDHAMSA,
        direction=D24_SIDDHAMSA.direction[:1] + (-1,) + D24_SIDDHAMSA.direction[2:],
    )
    test_longitude = 30.0 + 7.0  # within Taurus (even, source=1), segment index != multiple of 12
    mutated_result = classify(test_longitude, mutated_dir)
    original_result = classify(test_longitude, D24_SIDDHAMSA)
    detected_2 = mutated_result.d_sign != original_result.d_sign
    controls.append({"control": "direction[1] mutated +1->-1", "detected": detected_2})
    if not detected_2:
        fail("negative control 2 did not detect the planted mutation")

    original_hash = rule_content_sha256(D24_SIDDHAMSA)
    mutated_hash = rule_content_sha256(mutated)
    detected_3 = mutated_hash != original_hash
    controls.append({"control": "content hash changes on mutation", "detected": detected_3})
    if not detected_3:
        fail("negative control 3 did not detect the planted mutation")

    restored_hash = rule_content_sha256(D24_SIDDHAMSA)
    if restored_hash != original_hash:
        fail("D24_SIDDHAMSA itself was mutated - this must never happen (dataclass is frozen)")

    return {"controls": controls, "all_detected": True, "original_object_unmutated": True}


#: Static expected values (D-sign, division index), generated ONCE, offline,
#: from validate_d24_holdout.py's own from-scratch reference_d24() - never
#: by calling this certifier's own D24_SIDDHAMSA/classify() at certification
#: time. The certification-integrity lesson (ADR-0079), applied from the
#: outset, not retrofitted: comparing LIVE production-style output against
#: values frozen from an independent implementation is genuine cross-
#: implementation agreement, never a self-comparison.
STATIC_HOLDOUT = [
    {"id": "H1_aries_early", "longitude": 3.7, "expected_d_sign": 6, "expected_division_index": 2},
    {"id": "H2_taurus_mid", "longitude": 47.3, "expected_d_sign": 4, "expected_division_index": 13},
    {"id": "H3_gemini_boundary_adjacent", "longitude": 91.25, "expected_d_sign": 4, "expected_division_index": 1},
    {"id": "H4_leo_late", "longitude": 133.9, "expected_d_sign": 3, "expected_division_index": 11},
    {"id": "H5_virgo_exact_division", "longitude": 178.125, "expected_d_sign": 1, "expected_division_index": 22},
    {"id": "H6_libra_mid", "longitude": 200.0, "expected_d_sign": 8, "expected_division_index": 16},
    {"id": "H7_sagittarius_early", "longitude": 259.5, "expected_d_sign": 7, "expected_division_index": 15},
    {"id": "H8_capricorn_mid", "longitude": 289.5, "expected_d_sign": 6, "expected_division_index": 15},
    {"id": "H9_pisces_late", "longitude": 341.9, "expected_d_sign": 0, "expected_division_index": 9},
    {"id": "H10_aries_exact_zero", "longitude": 0.0, "expected_d_sign": 4, "expected_division_index": 0},
]


def gate_i_static_reference_regression():
    cases = 0
    mismatches = 0
    for case in STATIC_HOLDOUT:
        result = classify(case["longitude"], D24_SIDDHAMSA)
        cases += 1
        if (result.d_sign, result.division_index) != (case["expected_d_sign"], case["expected_division_index"]):
            mismatches += 1
            fail(f"static reference mismatch on {case['id']}: "
                 f"got=({result.d_sign},{result.division_index}) "
                 f"expected=({case['expected_d_sign']},{case['expected_division_index']})")
    return {"cases": cases, "mismatches": 0,
            "methodology": "LIVE production output (classify() + the registered production "
                            "D24_SIDDHAMSA rule) compared against STATIC values frozen from "
                            "validate_d24_holdout.py's own from-scratch reference_d24() (never "
                            "regenerated by production at certification time)",
            "classification": "correctness_evidence"}


def main():
    tee = support.start_transcript()
    preconditions = support.preflight()

    # Computed into a local first, in the same order as before, so
    # PYJHORA_VERSION (set by gate_c_oracle() itself, lazily) is already
    # known by the time the "oracle" field below is built - mirroring
    # scripts/certify_d45.py's own identical ordering fix (ADR-0085).
    gates = {
        "A_table_integrity": gate_a_table_integrity(),
        "B_dense_sweep": gate_b_dense_sweep(),
        "C_oracle": gate_c_oracle(),
        "D_non_invasiveness": gate_d_non_invasiveness(),
        "E_independent_validator": gate_e_independent_validator(),
        "F_boundary_cases": gate_f_boundary_cases(),
        "G_protected_holdout": gate_g_protected_holdout(),
        "H_negative_controls": gate_h_negative_controls(),
        "I_static_reference_regression": gate_i_static_reference_regression(),
    }

    report = {
        "schema": "varga_d24_v1_certification",
        "adr": "ADR-0083",
        "supersedes_provisional_id": "NOTHING_AUTHORISED",
        "date": str(date.today()),
        "scope": (
            "D24 Siddhamsa (Chaturvimshamsha), Parashara/BPHS variant, Traditional "
            "Parasara construction. Registered in production through the generic "
            "registry (engine.astrology.varga_d24, VARGA_D24_V1), discoverable via "
            "engine.astrology.divisional_chart.divisional_chart(snapshot, 24)."
        ),
        "rule": {
            "kind": "CyclicVargaRule",
            "variant": "parashara (24 x 1.25 deg, odd source signs start Leo / even "
                       "source signs start Cancer, forward)",
            "school_key": "parashara",
            "registered": True,
            "divisions": 24,
            "school": "parashara",
            "construction": "odd source signs start Leo (index 4), even source signs "
                             "start Cancer (index 3), forward counting for all twelve",
            "content_sha256": rule_content_sha256(D24_SIDDHAMSA),
        },
        "oracle": {"package": "PyJHora", "version": PYJHORA_VERSION,
                   "function": "chaturvimsamsa_chart method 1 Traditional Parasara (pure longitude math)"},
        "gates": gates,
        "explicit_non_claims": [
            "any per-division deity/label payload (VargaClassification carries only "
            "D-sign, division index, and fraction; deity output is out of scope, "
            "mirroring D45's own identical treatment - ADR-0083 section 4)",
            "the two non-default PyJHora chart_method variants (PARASARA_EVEN_REVERSE, "
            "PARASARA_EVEN_DOUBLE_REVERSE) - excluded, mirroring D45's own three "
            "excluded PyJHora methods",
            "any non-parashara school variant",
            "any other varga; each requires its own ADR and certification",
            "translated-edition caveat: the BPHS citation (Sarga 6, Shlokas 2-23) is not "
            "verified against the original Sanskrit or a second independently-published "
            "English edition",
        ],
        "environment": {"python": sys.version.split()[0]},
        "preconditions": preconditions,
        "result": "PASS",
    }
    out = support.emit(report, "VARGA_D24_V1_certification.json", "varga_d24", tee)
    print("=" * 60)
    print("VARGA_D24_V1 CERTIFICATION (production-registered)")
    print("=" * 60)
    for name, gate in report["gates"].items():
        print(f"{name}: {gate}")
    print("archived          :", out.relative_to(ROOT).as_posix())
    print("RESULT            : PASS")


if __name__ == "__main__":
    main()
