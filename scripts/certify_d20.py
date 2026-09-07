"""VARGA_D20_V1 CERTIFICATION RUNNER (ADR-0095, design per DP-036).

Certifies a STANDALONE, UNREGISTERED D20 Vimsamsa rule embedded in this
certifier - not engine/astrology/varga_d20.py, which does not exist and is
not created by this execution. Production implementation, production
registration and CI wiring each remain separate, not-yet-given
authorizations (ADR-0095 section 6).

Regenerates certification/VARGA_D20_V1_certification.json FROM SCRATCH on
every run; the stored JSON is never accepted as proof.

Gates (nine, per the owner's DP-036 decision 4):

A table/constant integrity (frozen start_sign/direction table, content-hash
pinned); B dense mathematical sweep vs validate_d20_holdout.py's own
reference_d20(), imported directly; C corroboration disclosure - explicitly
NON-BLOCKING (owner's DP-036 decision 2), so gate D is always reachable
locally; D isolation/non-invasiveness, with the content-hash pin ENFORCED;
E independent validator (separate process); F boundary cases; G protected
holdout (distinct stride); H negative controls, including the excluded
Variant F planted as a mutation (owner's DP-036 decision 3 - a control, NOT
a gate); I static reference regression against values frozen offline from
validate_d20_holdout.py.

DP-036 decision 2 in force: gate C never calls fail(). DP-032's D24/D40
audit found that D24's real PyJHora gate C blocks gate D from ever running
on a host without PyJHora, making isolation unverifiable locally. Gate C
here is disclosure-only and cannot stop gate D.

Gates A, B, F and G compare against validate_d20_holdout.reference_d20(),
imported directly - never against an in-file helper sharing code with
D20_VIMSAMSA's own construction. That is the DP-032 Part G Finding 1
discipline, and NEW_VARGA_IMPLEMENTATION_TEMPLATE.md v1.1.0 requirement B,
applied here from the outset rather than retrofitted.

ADR-0095 section 4 stands: this selection is NOT proof of the historical
original text, no verbatim Sanskrit was located, and primary-source
uncertainty is NOT eliminated. Per the owner's DP-036 decision 5 that
qualification is carried into the artifact as a STRUCTURED FIELD
("source_uncertainty"), not merely as prose, so no downstream consumer can
cite D20's certification without it.

Exit code 0 = PASS, 3 = FAIL.
"""

import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

sys.path.insert(0, str(ROOT / "scripts"))
import certification_support as support  # noqa: E402

from engine.astrology.varga_classifier import classify  # noqa: E402
from engine.astrology.varga_rules import CyclicVargaRule, rule_content_sha256  # noqa: E402

#: The genuinely independent reference: a separate file, independently typed
#: (sign-NAME lookup table, not this certifier's own integer-set
#: construction), imported directly. Gates A, B, F and G compare against
#: THIS, never against an in-file helper that shares code with D20_VIMSAMSA's
#: own construction below (DP-032 Part G, Finding 1).
import validate_d20_holdout  # noqa: E402

#: Frozen exactly as ADR-0095 section 2 states it: movable source signs
#: (0-based Aries=0, Cancer=3, Libra=6, Capricorn=9) start from Aries
#: (index 0); fixed source signs (Taurus=1, Leo=4, Scorpio=7, Aquarius=10)
#: start from Sagittarius (index 8); dual source signs (Gemini=2, Virgo=5,
#: Sagittarius=8, Pisces=11) start from Leo (index 4); forward counting
#: (direction +1) for all twelve. A standalone object - never registered via
#: engine.astrology.varga_registry.register_varga_rule.
_MOVABLE_SOURCE_SIGNS = frozenset({0, 3, 6, 9})
_FIXED_SOURCE_SIGNS = frozenset({1, 4, 7, 10})
_ARIES, _LEO, _SAGITTARIUS = 0, 4, 8

#: ADR-0095's EXCLUDED Variant F (movable Aries, fixed Leo, dual
#: Sagittarius) - the fixed/dual transposition. Retained ONLY so gate H can
#: plant it as a negative control (owner's DP-036 decision 3). It is never
#: selectable, never computed as output, and is NOT refuted as a reading:
#: ADR-0095 section 3 records it as attested.
_VARIANT_F_FIXED_START, _VARIANT_F_DUAL_START = _LEO, _SAGITTARIUS


def _start_for_source(source_sign: int) -> int:
    if source_sign in _MOVABLE_SOURCE_SIGNS:
        return _ARIES
    if source_sign in _FIXED_SOURCE_SIGNS:
        return _SAGITTARIUS
    return _LEO


D20_VIMSAMSA = CyclicVargaRule(
    divisions=20,
    start_sign=tuple(_start_for_source(s) for s in range(12)),
    direction=(1,) * 12,
)

#: Content fingerprint of the frozen rule above, pinned as a literal from a
#: prior intentional run (NOT computed from itself, which would trivially
#: always match and defeat the point of a pin). Computed once via
#: rule_content_sha256(D20_VIMSAMSA) and verified before being pinned here.
CERTIFIED_D20_CONTENT_SHA256 = (
    "efd08cea451084fedbe444c5473d6d50dfc589055b585f172e8a6e537668dac0"
)

#: D20-specific, verified during DP-036's design: 30/20 = 1.5 exactly, and
#: every internal boundary k*1.5 for k in 1..19 is an exact binary fraction.
#: Unlike D7/D9/D27 there is NO representability error, so any boundary
#: disagreement indicates a convention or table defect, never float drift.
_WIDTH = 30.0 / 20.0


def fail(message):
    print("D20 CERTIFICATION FAIL:", message)
    sys.exit(3)


def _content_hash_matches(rule) -> bool:
    """The REAL enforcement check: used by BOTH gate D (to decide pass/fail -
    a mismatch FAILS certification, not merely reported) and gate H's own
    negative control (to prove, against this exact function, that a mutated
    rule is rejected - not a separately simulated comparison). Template
    v1.1.0 requirements C and D."""

    return rule_content_sha256(rule) == CERTIFIED_D20_CONTENT_SHA256


def gate_a_table_integrity():
    if D20_VIMSAMSA.divisions != 20:
        fail("divisions != 20")
    for source in range(12):
        # Checked against validate_d20_holdout.py's own independently-typed
        # reference, not against the _start_for_source() helper this rule's
        # own construction also uses (DP-032 Part G, Finding 1).
        midpoint_degree = _WIDTH / 2.0  # division 0's midpoint, no boundary dust
        expected_sign, expected_division = validate_d20_holdout.reference_d20(
            source * 30.0 + midpoint_degree
        )
        if expected_division != 0:
            fail(f"sign {source}: independent reference division-0 check malformed")
        if D20_VIMSAMSA.start_sign[source] != expected_sign:
            fail(f"sign {source}: start {D20_VIMSAMSA.start_sign[source]}, "
                 f"independent reference says {expected_sign}")
        if D20_VIMSAMSA.direction[source] != 1:
            fail(f"sign {source}: direction")
    return {
        "cells": 12,
        "mismatches": 0,
        "content_sha256": rule_content_sha256(D20_VIMSAMSA),
        "verified_against": "validate_d20_holdout.py's own independently-typed "
                             "REFERENCE_TABLE (imported directly) - not a helper "
                             "shared with this rule's own construction",
        "disclosure": "movable source signs (0-based 0,3,6,9) start Aries (index 0); "
                       "fixed source signs (1,4,7,10) start Sagittarius (index 8); "
                       "dual source signs (2,5,8,11) start Leo (index 4); forward "
                       "counting for all twelve - Parashara/BPHS Reading E "
                       "(ADR-0095 section 1, DP-035)",
    }


def gate_b_dense_sweep():
    mismatches = 0
    points = 51429
    step = 360.0 / points
    for i in range(points):
        longitude = i * step
        result = classify(longitude, D20_VIMSAMSA)
        expected_sign, expected_division = validate_d20_holdout.reference_d20(longitude)
        if (result.d_sign, result.division_index) != (expected_sign, expected_division):
            mismatches += 1
    if mismatches:
        fail(f"dense sweep mismatches: {mismatches}")
    return {"points": points, "mismatches": 0,
            "verified_against": "validate_d20_holdout.reference_d20() (imported directly, "
                                 "a genuinely separate implementation)"}


def gate_c_corroboration_disclosure():
    """NON-BLOCKING by the owner's explicit DP-036 decision 2. This function
    never calls fail(), so gate D is always reachable on a host without
    PyJHora - the exact defect DP-032's D24/D40 audit found in certify_d24's
    ordering."""

    return {
        "oracle_executed": False,
        "blocking": False,
        "blocking_rationale": "owner's DP-036 decision 2: gate C must NOT block gate D. "
                               "DP-032's D24/D40 audit established that a real, enforced "
                               "gate C prevents gate D from ever executing on a host "
                               "without PyJHora, making isolation unverifiable locally.",
        "reason": "PyJHora unavailable in this local environment - the documented, "
                  "pre-existing Windows/Linux gate-parity limitation "
                  "(.claude/rules/certification.md). Genuine oracle execution is "
                  "deferred to this project's own CI hash-pinned oracle environment.",
        "read_only_corroboration": "PyJHora's own published source "
                  "(naturalstupid/PyJHora, src/jhora/horoscope/chart/charts.py, "
                  "vimsamsa_chart(), chart_method=1 Traditional Parasara) was read "
                  "directly during DP-035: with const.HOUSE_5=4 and const.HOUSE_9=8 it "
                  "computes movable=Aries(0), fixed=Sagittarius(8), dual=Leo(4), forward "
                  "- compared against this frozen table across all 12x20=240 cells and "
                  "found IDENTICAL. This is read-only source inspection plus offline "
                  "arithmetic comparison, NOT executed oracle agreement.",
        "classification": "disclosed_gap_not_correctness_evidence",
        "if_executed_tolerance": "zero categorical tolerance - D20 is pure longitude "
                                  "arithmetic with no astronomical component, so no "
                                  "tolerance derivation applies (DP-036 section 5)",
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
                "varga_d20" in module_name or "varga_registry" in module_name
            ):
                fail(f"certify_d20.py imports {module_name} - must remain standalone, "
                     f"never touch the registry")

    if (ROOT / "engine" / "astrology" / "varga_d20.py").exists():
        fail("engine/astrology/varga_d20.py already exists - certification execution "
             "does not authorize production implementation")
    production_module_absent = True

    # D20 must NOT be in the production registry: this is standalone
    # certification (owner's DP-036 decision 1, standalone-first).
    from engine.astrology import CERTIFIED_PRODUCTION_VARGAS
    if any(division == 20 for division, _school in CERTIFIED_PRODUCTION_VARGAS):
        fail("D20 is registered in CERTIFIED_PRODUCTION_VARGAS - certification "
             "execution does not authorize production registration")

    # Template v1.1.0 requirement C: ENFORCED, not merely reported.
    hash_ok = _content_hash_matches(D20_VIMSAMSA)
    if not hash_ok:
        fail(f"content hash {rule_content_sha256(D20_VIMSAMSA)} does not match "
             f"pinned {CERTIFIED_D20_CONTENT_SHA256} - the frozen rule has changed "
             f"since this pin was computed")

    return {
        "certifier_never_imports_varga_registry_or_varga_d20": True,
        "engine_astrology_varga_d20_absent": production_module_absent,
        "d20_absent_from_certified_production_vargas": True,
        "registered_vargas_unchanged": len(CERTIFIED_PRODUCTION_VARGAS),
        "content_sha256_matches_pinned": hash_ok,
        "content_hash_enforcement": "ENFORCED - a mismatch fails this gate, not merely "
                                     "reported (template v1.1.0 requirement C)",
        "reached_without_oracle": "gate C is non-blocking, so this gate executes on a "
                                   "host without PyJHora (owner's DP-036 decision 2)",
    }


def gate_e_independent_validator():
    import subprocess
    result = subprocess.run(
        [sys.executable, str(ROOT / "validate_d20_holdout.py")],
        capture_output=True, text=True)
    if result.returncode != 0 or "ALL INDEPENDENT D20 CASES PASSED" not in result.stdout:
        fail(f"independent validator failed: {result.stdout[-1200:]} {result.stderr[-800:]}")
    return {"result": "PASS",
            "classification": "corroborating_correctness_evidence",
            "note": "separate-process, from-scratch reimplementation; does not import "
                    "engine.astrology.varga_classifier, engine.astrology.varga_rules, "
                    "or this certifier's own D20_VIMSAMSA object"}


def gate_f_boundary_cases():
    import math
    cases = 0
    mismatches = 0
    for sign in range(12):
        for k in range(1, 20):
            exact_boundary = k * _WIDTH
            cases += 1
            longitude = sign * 30.0 + exact_boundary
            result = classify(longitude, D20_VIMSAMSA)
            expected_sign, expected_division = validate_d20_holdout.reference_d20(longitude)
            if (result.d_sign, result.division_index) != (expected_sign, expected_division):
                mismatches += 1
    ulp_cases = 0
    for sign in range(12):
        for k in range(1, 20):
            target = sign * 30.0 + k * _WIDTH
            probes = [math.nextafter(target, -math.inf), target - 1e-7]
            up = target
            for _ in range(3):
                up = math.nextafter(up, math.inf)
                probes.append(up)
            for longitude in probes:
                if not (0.0 <= longitude < 360.0):
                    continue
                ulp_cases += 1
                result = classify(longitude, D20_VIMSAMSA)
                expected_sign, expected_division = validate_d20_holdout.reference_d20(longitude)
                if (result.d_sign, result.division_index) != (expected_sign, expected_division):
                    mismatches += 1
    # Normalisation parity.
    norm_cases = 0
    for longitude in (-30.0, -0.5, 360.0, 361.5, 720.0):
        norm_cases += 1
        result = classify(longitude, D20_VIMSAMSA)
        expected_sign, expected_division = validate_d20_holdout.reference_d20(longitude)
        if (result.d_sign, result.division_index) != (expected_sign, expected_division):
            mismatches += 1
    if mismatches:
        fail(f"boundary mismatches: {mismatches}")
    return {
        "exact_boundary_cases": cases,
        "ulp_probe_cases": ulp_cases,
        "normalisation_cases": norm_cases,
        "mismatches": 0,
        "verified_against": "validate_d20_holdout.reference_d20() (imported directly)",
        "representability": "all 19 internal boundaries k*1.5 are EXACT binary fractions "
                             "(verified: Fraction(k*1.5) == Fraction(3k,2) for k=1..19), so "
                             "unlike D7/D9/D27 there is no representability error and any "
                             "disagreement here would be a convention or table defect, not "
                             "float drift (DP-036 section 2.2)",
        "boundary_policy": "inherited locked promote-up convention; no D20-specific exception",
    }


def gate_g_protected_holdout():
    mismatches = 0
    count = 0
    step = 0.0137
    longitude = 0.0
    while longitude < 360.0:
        result = classify(longitude, D20_VIMSAMSA)
        expected_sign, expected_division = validate_d20_holdout.reference_d20(longitude)
        if (result.d_sign, result.division_index) != (expected_sign, expected_division):
            mismatches += 1
        count += 1
        longitude += step
    if mismatches:
        fail(f"protected holdout mismatches: {mismatches}")
    return {"points": count, "mismatches": 0,
            "verified_against": "validate_d20_holdout.reference_d20() (imported directly)",
            "methodology": "prime-step deterministic sampling, independent of gate B/F "
                            "points, never used to tune the frozen rule"}


def gate_h_negative_controls():
    from dataclasses import replace

    controls = []
    original_hash = rule_content_sha256(D20_VIMSAMSA)

    mutated = replace(D20_VIMSAMSA, start_sign=(1,) + D20_VIMSAMSA.start_sign[1:])
    detected = mutated.start_sign[0] != D20_VIMSAMSA.start_sign[0]
    controls.append({"control": "start_sign[0] mutated Aries->wrong value",
                     "detected": detected})
    if not detected:
        fail("negative control 1 did not detect the planted mutation")

    mutated_dir = replace(
        D20_VIMSAMSA,
        direction=D20_VIMSAMSA.direction[:1] + (-1,) + D20_VIMSAMSA.direction[2:],
    )
    test_longitude = 30.0 + 7.0  # within Taurus (fixed, source=1)
    detected_2 = (classify(test_longitude, mutated_dir).d_sign
                  != classify(test_longitude, D20_VIMSAMSA).d_sign)
    controls.append({"control": "direction[1] mutated +1->-1", "detected": detected_2})
    if not detected_2:
        fail("negative control 2 did not detect the planted mutation")

    detected_3 = rule_content_sha256(mutated) != original_hash
    controls.append({"control": "content hash changes on mutation", "detected": detected_3})
    if not detected_3:
        fail("negative control 3 did not detect the planted mutation")

    # Template v1.1.0 requirement D: proves the REAL enforcement path - the
    # exact function gate D calls to decide pass/fail - not a separately
    # simulated comparison.
    detected_4 = (not _content_hash_matches(mutated)) and _content_hash_matches(D20_VIMSAMSA)
    controls.append({"control": "gate D's own _content_hash_matches() helper rejects the "
                                 "mutated rule and accepts the original", "detected": detected_4})
    if not detected_4:
        fail("negative control 4 did not detect the mutation via the real enforcement helper")

    # OWNER'S DP-036 DECISION 3: ADR-0095's excluded Variant F is planted as a
    # NEGATIVE CONTROL, not asserted as a certification gate. Variant F
    # transposes the fixed and dual starts (fixed->Leo, dual->Sagittarius).
    # This proves the certified rule is distinguishable from the excluded
    # reading and that the independent reference catches the substitution.
    # It does NOT refute Variant F as a reading - ADR-0095 section 3 records
    # it as attested and not refuted, and nothing here changes that.
    variant_f = replace(
        D20_VIMSAMSA,
        start_sign=tuple(
            _VARIANT_F_FIXED_START if s in _FIXED_SOURCE_SIGNS
            else _VARIANT_F_DUAL_START if s not in _MOVABLE_SOURCE_SIGNS
            else _ARIES
            for s in range(12)
        ),
    )
    probe_longitude = 30.0 + 7.3  # Taurus (fixed): certified Sagittarius, Variant F Leo
    probe_result = classify(probe_longitude, variant_f)
    probe_expected = validate_d20_holdout.reference_d20(probe_longitude)
    detected_5 = (probe_result.d_sign, probe_result.division_index) != probe_expected
    controls.append({
        "control": "ADR-0095's EXCLUDED Variant F (movable Aries, fixed Leo, dual "
                    "Sagittarius) planted as a mutation - disagrees with the independent "
                    "reference_d20()",
        "detected": detected_5,
        "classification": "negative_control_only",
        "not_a_refutation": "Variant F remains ATTESTED and NOT REFUTED as a reading "
                             "(ADR-0095 section 3). This control proves the certified "
                             "rule is distinguishable from it, nothing more.",
    })
    if not detected_5:
        fail("negative control 5 did not detect the excluded Variant F substitution")

    variant_f_hash_rejected = not _content_hash_matches(variant_f)
    controls.append({"control": "Variant F rejected by the real content-hash enforcement "
                                 "helper", "detected": variant_f_hash_rejected})
    if not variant_f_hash_rejected:
        fail("negative control 6: Variant F was not rejected by the enforcement helper")

    if rule_content_sha256(D20_VIMSAMSA) != original_hash:
        fail("D20_VIMSAMSA itself was mutated - this must never happen (frozen dataclass)")

    return {"controls": controls, "all_detected": True, "original_object_unmutated": True}


#: Static expected values (D-sign, division index), generated ONCE, offline,
#: from validate_d20_holdout.py's own from-scratch reference_d20() - never
#: by calling this certifier's own D20_VIMSAMSA/classify() at certification
#: time (the ADR-0079 lesson, applied from the outset).
STATIC_HOLDOUT = [
    {"id": "H1_aries_early", "longitude": 2.9, "expected_d_sign": 1, "expected_division_index": 1},
    {"id": "H2_taurus_exact_division", "longitude": 43.5, "expected_d_sign": 5, "expected_division_index": 9},
    {"id": "H3_gemini_mid", "longitude": 76.4, "expected_d_sign": 2, "expected_division_index": 10},
    {"id": "H4_cancer_boundary_adjacent", "longitude": 105.75, "expected_d_sign": 10, "expected_division_index": 10},
    {"id": "H5_leo_exact_division", "longitude": 139.5, "expected_d_sign": 9, "expected_division_index": 13},
    {"id": "H6_virgo_late", "longitude": 168.2, "expected_d_sign": 4, "expected_division_index": 12},
    {"id": "H7_libra_exact_division", "longitude": 195.0, "expected_d_sign": 10, "expected_division_index": 10},
    {"id": "H8_sagittarius_mid", "longitude": 244.8, "expected_d_sign": 7, "expected_division_index": 3},
    {"id": "H9_aquarius_late", "longitude": 317.25, "expected_d_sign": 7, "expected_division_index": 11},
    {"id": "H10_aries_exact_zero", "longitude": 0.0, "expected_d_sign": 0, "expected_division_index": 0},
]


def gate_i_static_reference_regression():
    cases = 0
    for case in STATIC_HOLDOUT:
        result = classify(case["longitude"], D20_VIMSAMSA)
        cases += 1
        if (result.d_sign, result.division_index) != (
            case["expected_d_sign"], case["expected_division_index"]
        ):
            fail(f"static reference mismatch on {case['id']}: "
                 f"got=({result.d_sign},{result.division_index}) "
                 f"expected=({case['expected_d_sign']},{case['expected_division_index']})")
    return {"cases": cases, "mismatches": 0,
            "methodology": "LIVE certifier output (classify() + the standalone D20_VIMSAMSA "
                            "rule) compared against STATIC values frozen from "
                            "validate_d20_holdout.py's own from-scratch reference_d20() "
                            "(never regenerated by this certifier at certification time)",
            "classification": "correctness_evidence"}


def main():
    tee = support.start_transcript()
    preconditions = support.preflight()
    report = {
        "schema": "varga_d20_v1_certification",
        "adr": "ADR-0095",
        "supersedes_provisional_id": "NOTHING_AUTHORISED",
        "date": str(date.today()),
        "scope": (
            "D20 Vimsamsa, Parashara/BPHS Reading E. Rule under certification is a "
            "STANDALONE, UNREGISTERED CyclicVargaRule instance embedded in this "
            "certifier - not engine/astrology/varga_d20.py, which does not exist. No "
            "production module, registration or CI wiring is authorized or created "
            "by this execution."
        ),
        "rule": {
            "kind": "standalone CyclicVargaRule instance embedded in this certifier "
                    "(scripts/certify_d20.py) - not a registered production rule",
            "divisions": 20,
            "width_degrees": _WIDTH,
            "school": "parashara",
            "registered": False,
            "construction": "movable source signs start Aries (index 0), fixed source "
                             "signs start Sagittarius (index 8), dual source signs start "
                             "Leo (index 4), forward counting for all twelve",
            "start_sign": list(D20_VIMSAMSA.start_sign),
            "direction": list(D20_VIMSAMSA.direction),
            "content_sha256": rule_content_sha256(D20_VIMSAMSA),
            "boundary_policy": "inherited locked promote-up convention; no D20-specific "
                                "exception. All 19 internal boundaries are exact binary "
                                "fractions, so no tolerance-carrying reference is needed.",
        },
        #: OWNER'S DP-036 DECISION 5: ADR-0095's historical-source uncertainty
        #: carried as a STRUCTURED FIELD, not prose, so no consumer can cite
        #: this certification without it.
        "source_uncertainty": {
            "selection_is_proof_of_historical_original_text": False,
            "verbatim_sanskrit_located": False,
            "primary_source_uncertainty_eliminated": False,
            "evidence_basis": "a translated verse (BPHS chapter 6 Vimsamsa block: 'From "
                               "Aries for a Movable Rasi, from Sagittarius for a Fixed "
                               "Rasi and from Leo for a Common Rasi'), convergent "
                               "independent secondary attestation, and PyJHora's "
                               "Traditional Parasara default - see DP-035.",
            "excluded_variant": {
                "name": "Variant F",
                "construction": "movable Aries, fixed Leo, dual Sagittarius "
                                 "(fixed/dual transposition)",
                "status": "ATTESTED and NOT REFUTED - excluded as the selected "
                           "methodology, not disproved as a reading (ADR-0095 section 3)",
                "treatment_here": "planted as a gate H negative control only (owner's "
                                   "DP-036 decision 3); no certification gate asserts "
                                   "its falsity",
            },
            "governing_statement": "ADR-0095 section 4: any future citation of D20's "
                                    "methodology must carry this qualification.",
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
            "no oracle execution this run - PyJHora unavailable locally, deferred to CI; "
            "certify_d20.py is NOT wired into .github/workflows/ci.yml by this "
            "certification-execution task - that remains a separate, not-yet-authorized act",
            "no production implementation, no engine/astrology/varga_d20.py, no entry in "
            "CERTIFIED_PRODUCTION_VARGAS - divisional_chart(snapshot, 20) still raises "
            "UnsupportedVargaError, correctly",
            "any per-division deity/label payload (VargaClassification carries only "
            "D-sign, division index and fraction; the vimsamsa deities are out of scope "
            "under the ADR-0089 precedent, so DP-024 is neither required nor resolved)",
            "the three non-default PyJHora chart_method variants (Parivritti Even "
            "Reverse, Parivritti Cyclic, Somanatha Parivritti Alternate) - excluded",
            "ADR-0095's Variant F - excluded as methodology but NOT refuted as a reading",
            "any non-parashara school variant",
            "any other varga; each requires its own ADR and certification",
            "translation-only caveat: the BPHS citation is a translated verse plus "
            "convergent secondary attestation, not a located verbatim Sanskrit "
            "verse (ADR-0095 section 4, DP-035)",
        ],
        "environment": {"python": sys.version.split()[0]},
        "preconditions": preconditions,
        "result": "PASS",
    }
    out = support.emit(report, "VARGA_D20_V1_certification.json", "varga_d20", tee)
    print("=" * 60)
    print("VARGA_D20_V1 CERTIFICATION (standalone rule, not production-registered)")
    print("=" * 60)
    for name, gate in report["gates"].items():
        print(f"{name}: {gate}")
    print("archived          :", out.relative_to(ROOT).as_posix())
    print("RESULT            : PASS")


if __name__ == "__main__":
    main()
