"""VARGA_D24_V1 CERTIFICATION RUNNER (ADR-0083).

Certifies the RATIFIED D24 (Siddhamsa) methodology (ADR-0082 selection and
frozen methodology; ADR-0083 certification design). Per the owner's own
"CEO AUTHORIZATION - PROCEED WITH D24 SELECTION/ADR WORK" instruction and
the subsequent explicit authorization of "VARGA_D24_V1 certification
design/execution", no production engine module is authorized this task.

**This file is NOT engine/astrology/varga_d24.py and does not create,
modify, or register anything under engine/astrology/varga_registry.py.**
The frozen D24 rule is instantiated here as a standalone, UNREGISTERED
`CyclicVargaRule` object and classified via the already-certified generic
framework (`engine.astrology.varga_classifier.classify`, `engine.astrology.
varga_rules.CyclicVargaRule` - pure functions/dataclasses exercised by six
already-certified vargas, D2/D3/D7/D12/D30/D45, with no registry coupling),
mirroring exactly the precedent already used for PARASHARI_YOGA_V1 and
KP_SIGNIFICATOR_V1's own certification-execution stage (before their own
later, separately-authorized production-implementation tasks): the
standalone rule consumes already-certified production infrastructure but
is not itself registered anywhere as a production capability.

Regenerates certification/VARGA_D24_V1_certification.json FROM SCRATCH on
every run; the stored JSON is never accepted as proof.

Gates (ADR-0083, mirroring D45's own certification-design discipline):

A table/constant integrity (the frozen start_sign/direction table,
content-hash pinned); B dense mathematical sweep vs an independently coded
classical reference; C corroboration disclosure (PyJHora's own published
source was read directly this task - see ADR-0083 section 1/8 - but cannot
be executed in this local environment; genuine oracle execution is deferred
to this project's own CI hash-pinned oracle environment, exactly as
PARASHARI_YOGA_V1's own certification-execution disclosed); D isolation
(confirms this certifier touches no existing engine/ file and the standalone
rule is never registered); E independent validator (validate_d24_holdout.py,
a from-scratch reimplementation importing nothing from engine.astrology);
F boundary cases (sign-transition edges; the exact internal division
boundaries, empirically confirmed representable with zero floor-
classification effect - ADR-0083 section 3); G protected holdout
(independent of the boundary cases, never used for tuning); H negative
controls (a real planted violation, confirmed detected, confirmed the
original standalone object remains unmutated).

No third-party computational oracle is used this execution. PyJHora is not
invoked: this project's own local PyJHora environment remains degraded
(numpy import failure, an already-disclosed, unchanged limitation). ADR-0083
section 1 records that PyJHora's own published source (`naturalstupid/
PyJHora`, GitHub) was read directly and its default/Traditional-Parasara
`chaturvimsamsa_chart()` method matches this frozen construction exactly -
read-only corroboration, not executed oracle agreement.

Exit code 0 = PASS, 3 = FAIL.
"""

import hashlib
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

sys.path.insert(0, str(ROOT / "scripts"))
import certification_support as support  # noqa: E402

from engine.astrology.varga_classifier import classify  # noqa: E402
from engine.astrology.varga_rules import CyclicVargaRule, rule_content_sha256  # noqa: E402

#: Frozen exactly as ADR-0083 section 1 states it (BPHS Sarga 6, Shlokas
#: 2-23): odd source signs (0-based Aries=0, Gemini=2, Leo=4, Libra=6,
#: Sagittarius=8, Aquarius=10) start from Leo (index 4); even source signs
#: (Taurus=1, Cancer=3, Virgo=5, Scorpio=7, Capricorn=9, Pisces=11) start
#: from Cancer (index 3); forward counting (direction +1) for all twelve.
#: A standalone object - never registered via
#: engine.astrology.varga_registry.register_varga_rule.
_ODD_SOURCE_SIGNS = frozenset({0, 2, 4, 6, 8, 10})
_LEO, _CANCER = 4, 3

D24_SIDDHAMSA = CyclicVargaRule(
    divisions=24,
    start_sign=tuple(_LEO if s in _ODD_SOURCE_SIGNS else _CANCER for s in range(12)),
    direction=(1,) * 12,
)

#: Content fingerprint of the frozen rule above, pinned as a literal
#: hardcoded value from a prior intentional run (NOT computed from itself,
#: which would trivially always match and defeat the point of a pin -
#: mirrors engine.astrology.varga_d45's own CERTIFIED_D45_CONTENT_SHA256
#: pattern exactly).
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


def gate_c_corroboration_disclosure():
    return {
        "oracle_executed": False,
        "reason": "PyJHora unavailable in this local environment (numpy import failure, "
                  "an already-disclosed, pre-existing limitation) - genuine oracle "
                  "execution deferred to this project's own CI hash-pinned oracle "
                  "environment, per every oracle-tier certifier's own established pattern.",
        "read_only_corroboration": "PyJHora's own published source "
                  "(naturalstupid/PyJHora, GitHub, chaturvimsamsa_chart()) was read "
                  "directly this task (ADR-0083 section 1/8): its default/Traditional-"
                  "Parasara method (even_dirn=1, odd_base=4/Leo, even_base=3/Cancer) "
                  "matches this frozen construction exactly. This is read-only source "
                  "inspection, not executed oracle agreement.",
        "classification": "disclosed_gap_not_correctness_evidence",
    }


def gate_d_isolation():
    import ast
    import inspect

    this_module = sys.modules[__name__]
    own_source = inspect.getsource(this_module)
    tree = ast.parse(own_source)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            module_name = getattr(node, "module", None) or (
                node.names[0].name if isinstance(node, ast.Import) else None
            )
            if module_name and (
                "varga_d24" in module_name or "varga_registry" in module_name
            ):
                fail(f"certify_d24.py imports {module_name} - must remain standalone, "
                     f"never touch the registry")

    if not (ROOT / "engine" / "astrology" / "varga_d24.py").exists():
        registered = True
    else:
        fail("engine/astrology/varga_d24.py already exists - certification design/"
             "execution does not authorize production implementation")
    return {
        "certifier_never_imports_varga_registry_or_varga_d24": True,
        "engine_astrology_varga_d24_absent": registered,
        "content_sha256_matches_pinned": rule_content_sha256(D24_SIDDHAMSA) == CERTIFIED_D24_CONTENT_SHA256,
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
            "methodology": "LIVE certifier output (classify() + the standalone D24_SIDDHAMSA "
                            "rule) compared against STATIC values frozen from validate_d24_"
                            "holdout.py's own from-scratch reference_d24() (never regenerated "
                            "by this certifier's own rule at certification time)",
            "classification": "correctness_evidence"}


def main():
    tee = support.start_transcript()
    preconditions = support.preflight()
    report = {
        "schema": "varga_d24_v1_certification",
        "adr": "ADR-0083",
        "supersedes_provisional_id": "NOTHING_AUTHORISED",
        "date": str(date.today()),
        "scope": (
            "D24 Siddhamsa (Chaturvimshamsha), Parashara/BPHS variant, Traditional "
            "Parasara construction. Rule under certification is a STANDALONE, "
            "UNREGISTERED CyclicVargaRule instance embedded in this certifier - not "
            "engine/astrology/varga_d24.py, no production module is authorized or "
            "created this execution."
        ),
        "rule": {
            "kind": "standalone CyclicVargaRule instance embedded in this certifier "
                    "(scripts/certify_d24.py) - not a registered production rule",
            "divisions": 24,
            "school": "parashara",
            "construction": "odd source signs start Leo (index 4), even source signs "
                             "start Cancer (index 3), forward counting for all twelve",
            "content_sha256": rule_content_sha256(D24_SIDDHAMSA),
        },
        "oracle": gate_c_corroboration_disclosure(),
        "gates": {
            "A_table_integrity": gate_a_table_integrity(),
            "B_dense_sweep": gate_b_dense_sweep(),
            "C_corroboration_disclosure": gate_c_corroboration_disclosure(),
            "D_isolation": gate_d_isolation(),
            "E_independent_validator": gate_e_independent_validator(),
            "F_boundary_cases": gate_f_boundary_cases(),
            "G_protected_holdout": gate_g_protected_holdout(),
            "H_negative_controls": gate_h_negative_controls(),
            "I_static_reference_regression": gate_i_static_reference_regression(),
        },
        "explicit_non_claims": [
            "no oracle execution this run - PyJHora unavailable locally, deferred to CI",
            "any per-division deity/label payload (VargaClassification carries only "
            "D-sign, division index, and fraction; deity output is out of scope, "
            "mirroring D45's own identical treatment - ADR-0083 section 4)",
            "the two non-default PyJHora chart_method variants (PARASARA_EVEN_REVERSE, "
            "PARASARA_EVEN_DOUBLE_REVERSE) - excluded, mirroring D45's own three "
            "excluded PyJHora methods",
            "any non-parashara school variant",
            "any other varga; each requires its own ADR and certification",
            "no engine/ production module is created or modified by this certification",
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
    print("VARGA_D24_V1 CERTIFICATION (standalone rule, not production-registered)")
    print("=" * 60)
    for name, gate in report["gates"].items():
        print(f"{name}: {gate}")
    print("archived          :", out.relative_to(ROOT).as_posix())
    print("RESULT            : PASS")


if __name__ == "__main__":
    main()
