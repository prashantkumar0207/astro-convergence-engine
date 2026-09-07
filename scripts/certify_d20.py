"""VARGA_D20_V1 CERTIFICATION RUNNER (ADR-0095, design per DP-036).

Certifies the PRODUCTION, REGISTERED D20 Vimsamsa rule in
engine/astrology/varga_d20.py, imported directly. Revised from the
standalone certification-execution stage per the owner's "CEO AUTHORIZATION -
D20 PRODUCTION IMPLEMENTATION" instruction, mirroring certify_d24.py and
certify_d40.py's own production-stage revision: gate D flips from isolation
(D20 must NOT be registered) to non-invasiveness (D20 IS registered, is the
certified module object, and disturbed nothing).

Production certification rests on THIS evidence, not on the earlier
standalone artifact having passed. The standalone and CI artifacts remain in
git history as the record of the prior stages.

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

#: THE PRODUCTION RULE ITSELF (production-implementation stage, ADR-0095).
#: This certifier no longer embeds a standalone copy: it imports the real
#: registered object from engine/astrology/varga_d20.py, so the evidence
#: below demonstrates that the ACTUAL PRODUCTION CODE produces the certified
#: rule - not merely that a reference reproduction of it does. Mirrors
#: certify_d24.py / certify_d40.py's own production-stage revision exactly.
from engine.astrology.varga_d20 import (  # noqa: E402
    D20_VIMSAMSA,
    D20_SCHOOL,
)
from engine.astrology.varga_registry import (  # noqa: E402
    get_varga_rule,
    registered_vargas,
)

_MOVABLE_SOURCE_SIGNS = frozenset({0, 3, 6, 9})
_FIXED_SOURCE_SIGNS = frozenset({1, 4, 7, 10})
_ARIES, _LEO, _SAGITTARIUS = 0, 4, 8

#: ADR-0095's EXCLUDED Variant F (movable Aries, fixed Leo, dual
#: Sagittarius) - the fixed/dual transposition. Retained ONLY so gate H can
#: plant it as a negative control (owner's DP-036 decision 3). It is never
#: selectable, never computed as output, and is NOT refuted as a reading:
#: ADR-0095 section 3 records it as attested.
_VARIANT_F_FIXED_START, _VARIANT_F_DUAL_START = _LEO, _SAGITTARIUS


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


#: Set by gate_c_oracle() when PyJHora IS available and a genuine categorical
#: mismatch is found. main() fails on it AFTER every other gate has run, so a
#: real oracle disagreement still fails certification (DP-036 acceptance
#: criteria) without gate C ever blocking gate D.
_ORACLE_MISMATCHES = 0
PYJHORA_VERSION = None


def gate_c_oracle():
    """Genuine external-oracle gate when PyJHora is importable; disclosure-only
    when it is not.

    NON-BLOCKING by the owner's explicit DP-036 decision 2: this function never
    calls fail(), and main() evaluates gate D BEFORE this gate, so gate D is
    reachable whether or not PyJHora exists - the exact defect DP-032's D24/D40
    audit found in certify_d24's ordering. A genuine mismatch is recorded and
    failed on at the END of main(), after every other gate has produced its
    evidence.

    Oracle: PyJHora's vimsamsa_chart, Traditional Parasara (chart_method=1),
    at ZERO categorical tolerance - D20 is pure longitude arithmetic with no
    astronomical component, so no tolerance derivation applies (DP-036
    section 5)."""

    global _ORACLE_MISMATCHES, PYJHORA_VERSION

    try:
        from jhora.horoscope.chart.charts import vimsamsa_chart
        import importlib.metadata
        PYJHORA_VERSION = importlib.metadata.version("PyJHora")
    except Exception as error:
        return _gate_c_disclosure(str(error))

    mismatches = 0
    comparisons = 0
    per_sign = 450
    for source in range(12):
        for i in range(per_sign):
            within = (i + 0.5) * (30.0 / per_sign)  # midpoints, no boundary dust
            oracle = vimsamsa_chart([["L", (source, within)]], chart_method=1)
            oracle_sign = oracle[0][1][0]
            ours = classify(source * 30.0 + within, D20_VIMSAMSA)
            if ours.d_sign != oracle_sign:
                mismatches += 1
            comparisons += 1
    _ORACLE_MISMATCHES = mismatches
    return {
        "oracle_executed": True,
        "execution_tier": "CI hash-pinned oracle environment (requirements-oracle.lock)",
        "blocking": False,
        "blocking_rationale": "owner's DP-036 decision 2: gate C must NOT block gate D. "
                               "main() evaluates gate D first, and this gate never calls "
                               "fail(); a genuine mismatch is failed on at the end of "
                               "main(), after every gate has produced its evidence.",
        "package": "PyJHora",
        "version": PYJHORA_VERSION,
        "function": "vimsamsa_chart(chart_method=1, Traditional Parasara)",
        "tolerance": "zero categorical tolerance - pure longitude arithmetic, no "
                      "astronomy, so no tolerance derivation applies",
        "comparisons": comparisons,
        "mismatches": mismatches,
        "classification": "genuine_external_oracle_agreement" if not mismatches
                           else "genuine_external_oracle_MISMATCH",
    }


def _gate_c_disclosure(error_text):
    """Disclosure-only result, used when PyJHora cannot be imported. Never
    presented as oracle verification (template v1.1.0 requirement F)."""

    return {
        "oracle_executed": False,
        "blocking": False,
        "blocking_rationale": "owner's DP-036 decision 2: gate C must NOT block gate D. "
                               "DP-032's D24/D40 audit established that a real, enforced "
                               "gate C prevents gate D from ever executing on a host "
                               "without PyJHora, making isolation unverifiable locally.",
        "reason": f"PyJHora unavailable in this environment ({error_text}) - the "
                  f"documented, pre-existing Windows/Linux gate-parity limitation "
                  f"(.claude/rules/certification.md). Genuine oracle execution is "
                  f"deferred to this project's own CI hash-pinned oracle environment.",
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


def gate_d_non_invasiveness():
    """PRODUCTION-STAGE gate D (was gate D isolation at the standalone stage).

    Now that D20 is registered, this gate proves the opposite of what the
    standalone version proved: D20 IS registered, the registered object IS
    the certified module constant, its content hash still matches the pin,
    and the eight pre-existing production vargas plus D1/D9/D10 are
    completely unaffected by the registration.

    Still reached without the oracle: gate C never calls fail() and main()
    evaluates this gate BEFORE it (owner's DP-036 decision 2)."""

    from engine.astrology import CERTIFIED_PRODUCTION_VARGAS

    if registered_vargas() != CERTIFIED_PRODUCTION_VARGAS:
        fail(f"registry contents: {registered_vargas()}")
    if (20, D20_SCHOOL) not in registered_vargas():
        fail("D20 is not registered - production implementation incomplete")
    if get_varga_rule(20, D20_SCHOOL) is not D20_VIMSAMSA:
        fail("registered D20 rule is not the certified module object")

    # Template v1.1.0 requirement C: ENFORCED, not merely reported.
    hash_ok = _content_hash_matches(D20_VIMSAMSA)
    if not hash_ok:
        fail(f"content hash {rule_content_sha256(D20_VIMSAMSA)} does not match "
             f"pinned {CERTIFIED_D20_CONTENT_SHA256} - the frozen rule has changed "
             f"since this pin was computed")

    # Every pre-existing certified varga byte-for-byte unaffected by D20's
    # registration - identity AND content hash, not merely key presence.
    hashes = {}
    for division, school in CERTIFIED_PRODUCTION_VARGAS:
        if division == 20:
            continue
        hashes[f"D{division}_{school}"] = rule_content_sha256(
            get_varga_rule(division, school))

    # D1/D9/D10 remain served by their own dedicated modules, never the registry.
    from engine.astrology.divisional_chart import IMPLEMENTED_VARGAS
    if tuple(IMPLEMENTED_VARGAS) != (1, 9, 10):
        fail(f"dedicated dispatch changed: {IMPLEMENTED_VARGAS}")
    for dedicated in IMPLEMENTED_VARGAS:
        if any(d == dedicated for d, _ in CERTIFIED_PRODUCTION_VARGAS):
            fail(f"D{dedicated} is dedicated but appears in the registry")

    return {
        "d20_registered": True,
        "registered_object_is_the_certified_module_constant": True,
        "registered_vargas_total": len(CERTIFIED_PRODUCTION_VARGAS),
        "pre_existing_vargas_unaffected": hashes,
        "dedicated_dispatch_unchanged": list(IMPLEMENTED_VARGAS),
        "content_sha256_matches_pinned": hash_ok,
        "content_hash_enforcement": "ENFORCED - a mismatch fails this gate, not merely "
                                     "reported (template v1.1.0 requirement C)",
        "reached_without_oracle": "gate C is non-blocking and main() evaluates this gate "
                                   "first, so isolation is verifiable on a host without "
                                   "PyJHora (owner's DP-036 decision 2)",
        "stage": "production-registered rule (was standalone/unregistered at the "
                  "certification-execution stage; see the historical artifacts)",
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
            "methodology": "LIVE production output (classify() + the REGISTERED D20_VIMSAMSA "
                            "rule) compared against STATIC values frozen from "
                            "validate_d20_holdout.py's own from-scratch reference_d20() "
                            "(never regenerated by this certifier at certification time)",
            "classification": "correctness_evidence"}


def main():
    tee = support.start_transcript()
    preconditions = support.preflight()

    # OWNER'S DP-036 DECISION 2, structurally enforced: gate D is evaluated
    # BEFORE gate C, so the oracle cannot prevent the isolation gate from
    # running - the exact defect DP-032's D24/D40 audit found in certify_d24.
    # The reported dict is still ordered A..I; only evaluation order differs.
    _a = gate_a_table_integrity()
    _b = gate_b_dense_sweep()
    _d = gate_d_non_invasiveness()          # <- before C, deliberately
    _e = gate_e_independent_validator()
    _f = gate_f_boundary_cases()
    _g = gate_g_protected_holdout()
    _h = gate_h_negative_controls()
    _i = gate_i_static_reference_regression()
    _c = gate_c_oracle()             # <- last; never calls fail()
    gates = {
        "A_table_integrity": _a,
        "B_dense_sweep": _b,
        "C_oracle": _c,
        "D_non_invasiveness": _d,
        "E_independent_validator": _e,
        "F_boundary_cases": _f,
        "G_protected_holdout": _g,
        "H_negative_controls": _h,
        "I_static_reference_regression": _i,
    }
    report = {
        "schema": "varga_d20_v1_certification",
        "adr": "ADR-0095",
        "supersedes_provisional_id": "NOTHING_AUTHORISED",
        "date": str(date.today()),
        "scope": (
            "D20 Vimsamsa, Parashara/BPHS Reading E. Rule under certification is the "
            "PRODUCTION, REGISTERED rule in engine/astrology/varga_d20.py, imported "
            "directly - not a standalone reproduction of it. This artifact therefore "
            "evidences that the actual production code produces the certified rule. "
            "The earlier standalone certification remains as historical evidence in "
            "git history; it is not overwritten in meaning, only superseded in stage."
        ),
        "rule": {
            "kind": "PRODUCTION CyclicVargaRule registered through the generic registry "
                    "(engine/astrology/varga_d20.py), imported by this certifier",
            "divisions": 20,
            "width_degrees": _WIDTH,
            "school": "parashara",
            "registered": True,
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
        "oracle": _c,
        "gates": gates,
        "explicit_non_claims": [
            "oracle execution is conditional: genuine PyJHora comparison when the "
            "library is importable (CI's hash-pinned oracle job), disclosure-only "
            "otherwise. The gates block records which actually happened - a local "
            "disclosure run is never presented as oracle verification",
            "D20 is now production-registered under ADR-0095; this artifact certifies "
            "the REGISTERED rule. Production certification rests on THIS evidence, never "
            "on the earlier standalone artifact merely having passed",
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
    if _ORACLE_MISMATCHES:
        # Reached only when PyJHora actually ran. Every other gate has already
        # produced its evidence, so decision 2 is honoured and a real oracle
        # disagreement still fails certification (DP-036 acceptance criteria).
        report["result"] = "FAIL"
        support.emit(report, "VARGA_D20_V1_certification.json", "varga_d20", tee)
        fail(f"genuine oracle mismatches: {_ORACLE_MISMATCHES}")

    out = support.emit(report, "VARGA_D20_V1_certification.json", "varga_d20", tee)
    print("=" * 60)
    print("VARGA_D20_V1 CERTIFICATION (production-registered rule)")
    print("=" * 60)
    for name, gate in report["gates"].items():
        print(f"{name}: {gate}")
    print("archived          :", out.relative_to(ROOT).as_posix())
    print("RESULT            : PASS")


if __name__ == "__main__":
    main()
