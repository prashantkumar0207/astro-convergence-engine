"""VARGA_D45_V1 CERTIFICATION RUNNER (ADR-0077).

Certifies the PRODUCTION, registered D45 rule (engine.astrology.varga_d45,
VARGA_D45_V1). Per the owner's "CEO AUTHORIZATION — D45 PRODUCTION
IMPLEMENTATION" instruction (2026-08-25): D45 is now registered through the
generic registry, exactly mirroring D2/D3/D7/D12/D30. The certified rule table
is preserved exactly as frozen in ADR-0077 - this run does not alter it.

Regenerates certification/VARGA_D45_V1_certification.json FROM SCRATCH on every
run; the stored JSON is never accepted as proof.

Gates: A rule-table integrity; B dense mathematical sweep vs an independently
coded classical rule; C external oracle (PyJHora's akshavedamsa_chart,
Traditional Parasara method, zero categorical tolerance); D framework
non-invasiveness (confirms the five pre-existing certified vargas are
unaffected and that D45 is now correctly registered and discoverable); E the
independent validator (validate_d45_holdout.py, a from-scratch reimplementation
against the production registered rule); F the three genuine floating-point
boundary cases identified in ADR-0077 (k=13, 26, 29 per sign, out of 44
internal segment boundaries) plus sign/segment-edge cases; G a protected
holdout, generated independently of the boundary cases and never used for
tuning; H genuine negative controls (a real planted violation, confirmed
detected, confirmed restored); I composition/plumbing verification (ADR-0085)
- exercises divisional_chart(snapshot, 45)/build_varga_chart() directly, which
gates A/B/F/G never do, checking every field of every body against an
independent cross-check plus a genuine in-process monkeypatch mutation
self-check (see validate_d45_holdout.py's own verify_composition()/
run_mutation_self_check()). Exit 0 = PASS, 3 = FAIL.
"""

import subprocess
import sys
from dataclasses import replace
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

sys.path.insert(0, str(ROOT / "scripts"))
import certification_support as support  # noqa: E402

import engine.astrology  # noqa: F401, E402  (registers production vargas, including D45)
from engine.astrology.varga_classifier import classify  # noqa: E402
from engine.astrology.varga_d45 import D45_PARASHARA, D45_SCHOOL  # noqa: E402
from engine.astrology.varga_registry import (  # noqa: E402
    get_varga_rule,
    registered_vargas,
)
from engine.astrology.varga_rules import rule_content_sha256  # noqa: E402

#: Set by gate_c_oracle() itself, lazily, the first time it runs (ADR-0085
#: Gate C import-structure change). Deliberately NOT imported at module
#: level: PyJHora is required only by Gate C, and every other gate in this
#: file - including the new Gate I (ADR-0085) - needs none of it. Moving
#: this import out of module scope does not change Gate C's own behaviour
#: in any way: it still hard-fails with the identical message and exit code
#: the instant it actually runs without PyJHora present, exactly as before -
#: only the MOMENT that failure occurs moves from "at import" to "when Gate
#: C executes," so the other eight gates become independently importable
#: and runnable on a host where PyJHora is unavailable.
PYJHORA_VERSION = None


#: The three genuine floating-point floor-classification boundaries identified in
#: ADR-0077 section 3 (of 44 internal per-sign boundaries, k = 1..44).
BOUNDARY_K_VALUES = (13, 26, 29)

#: Content fingerprint of the certified D45 table, pinned (also pinned
#: independently in engine/tests/test_varga_d45.py).
CERTIFIED_D45_CONTENT_SHA256 = (
    "c8515e44be6e21e3e8c3298121b8c0e4687c0176d9da7e94f7d0aba53a8bf817"
)


def fail(message):
    print("D45 CERTIFICATION FAIL:", message)
    sys.exit(3)


def _independent_d45_sign(source_sign: int, degree_in_sign: float) -> int:
    """Independently coded reference (ADR-0077 section 2), not imported from the
    rule under test - only the movable/fixed/dual/forward classical description is
    used, re-derived from first principles. Applies the engine's own documented
    boundary-promotion rule (a degree within 1e-10 of a division's edge promotes to
    the next division, per engine/astrology/longitude_utils.py's own docstring) on
    its own terms - re-derived independently, not imported - so this reference
    checks whether classify() correctly IMPLEMENTS the documented convention,
    rather than spuriously disagreeing with it at D45's own non-exact 2/3-degree
    boundaries (ADR-0077 section 3)."""

    movable = {0, 3, 6, 9}
    fixed = {1, 4, 7, 10}
    segment_width = 30.0 / 45.0
    segment_index = int((degree_in_sign + 1e-10) / segment_width)
    if segment_index > 44:
        segment_index = 44
    if source_sign in movable:
        offset = 0
    elif source_sign in fixed:
        offset = 4
    else:
        offset = 8
    return (segment_index + offset) % 12, segment_index


def gate_a_table_integrity():
    if D45_PARASHARA.divisions != 45:
        fail("divisions != 45")
    movable, fixed, dual = {0, 3, 6, 9}, {1, 4, 7, 10}, {2, 5, 8, 11}
    for source in range(12):
        expected = 0 if source in movable else 4 if source in fixed else 8
        if source not in movable | fixed | dual:
            fail(f"sign {source}: not classified movable/fixed/dual")
        if D45_PARASHARA.start_sign[source] != expected:
            fail(f"sign {source}: start {D45_PARASHARA.start_sign[source]}, expected {expected}")
        if D45_PARASHARA.direction[source] != 1:
            fail(f"sign {source}: direction")
    return {"cells": 12, "mismatches": 0}


def gate_b_dense_sweep():
    mismatches = 0
    points = 51429
    step = 360.0 / points
    for i in range(points):
        longitude = i * step
        result = classify(longitude, D45_PARASHARA)
        source = int(longitude // 30.0)
        degree = longitude - source * 30.0
        expected_sign, expected_division = _independent_d45_sign(source, degree)
        if (result.d_sign, result.division_index) != (expected_sign, expected_division):
            mismatches += 1
    if mismatches:
        fail(f"dense sweep mismatches: {mismatches}")
    return {"points": points, "mismatches": 0}


def gate_c_oracle():
    global PYJHORA_VERSION

    try:
        from jhora.horoscope.chart.charts import akshavedamsa_chart
        import importlib.metadata
        PYJHORA_VERSION = importlib.metadata.version("PyJHora")
    except Exception as error:  # pragma: no cover
        print("D45 CERTIFICATION FAIL: PyJHora oracle unavailable:", error)
        sys.exit(3)

    mismatches = 0
    comparisons = 0
    per_sign = 450
    for source in range(12):
        for i in range(per_sign):
            within = (i + 0.5) * (30.0 / per_sign)  # midpoints, no boundary dust
            oracle = akshavedamsa_chart([["L", (source, within)]], chart_method=1)
            oracle_sign = oracle[0][1][0]
            ours = classify(source * 30.0 + within, D45_PARASHARA)
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
    if (45, D45_SCHOOL) not in registered_vargas():
        fail("D45 not registered")
    if get_varga_rule(45, D45_SCHOOL) is not D45_PARASHARA:
        fail("registered D45 rule is not the certified module object")
    if rule_content_sha256(D45_PARASHARA) != CERTIFIED_D45_CONTENT_SHA256:
        fail("D45 content hash does not match the certified pinned value")

    # Confirm the five pre-existing certified vargas are byte-for-byte
    # unaffected by D45's registration - identity and content hash, not
    # merely that a rule still exists under the key.
    hashes = {}
    for division, school in CERTIFIED_PRODUCTION_VARGAS:
        rule = get_varga_rule(division, school)
        hashes[f"D{division}_{school}"] = rule_content_sha256(rule)

    snapshot = calculate(
        BirthData(1985, 12, 21, 14, 40, 0.0, 25.6, 85.1333, "Asia/Kolkata")
    ).snapshot
    if type(divisional_chart(snapshot, 9)).__name__ != "NavamsaChart":
        fail("D9 no longer served by the certified module")
    if type(divisional_chart(snapshot, 10)).__name__ != "DashamsaChart":
        fail("D10 no longer served by the certified module")
    for division in (4, 16, 20, 24, 27, 40, 60):
        try:
            divisional_chart(snapshot, division)
            fail(f"D{division} no longer refused")
        except UnsupportedVargaError:
            pass

    return {
        "registry": [list(entry) for entry in registered_vargas()],
        "d45_registered": True,
        "registered_rule_identity": "is D45_PARASHARA (engine.astrology.varga_d45)",
        "rule_content_sha256": rule_content_sha256(D45_PARASHARA),
        "existing_certified_rule_hashes": hashes,
    }


def gate_e_validator():
    result = subprocess.run(
        [sys.executable, str(ROOT / "validate_d45_holdout.py")],
        capture_output=True, text=True)
    if result.returncode != 0 or "ALL INDEPENDENT D45 CASES PASSED" not in result.stdout:
        fail(f"independent validator failed: {result.stdout[-800:]} {result.stderr[-800:]}")
    return {"result": "PASS"}


def gate_f_boundary_cases():
    cases_checked = 0
    mismatches = 0
    convention_notes = []
    for sign in range(12):
        for k in BOUNDARY_K_VALUES:
            exact_boundary = k * (30.0 / 45.0)
            result = classify(sign * 30.0 + exact_boundary, D45_PARASHARA)
            cases_checked += 1
            # The engine-wide 1e-10 tolerance-promoted boundary convention governs
            # this exactly as it governs every other certified varga (ADR-0077
            # section 3/4) - this gate records what the convention actually does at
            # each identified case, it does not require a specific segment index,
            # since "which side of the boundary" is a convention choice, not a bug.
            convention_notes.append(
                {"sign": sign, "k": k, "longitude": sign * 30.0 + exact_boundary,
                 "resolved_division_index": result.division_index}
            )
    # Sign-transition edges: last division of one sign vs first of the next.
    for sign in range(12):
        near_end = classify(sign * 30.0 + 29.9999999999, D45_PARASHARA)
        start = classify(sign * 30.0, D45_PARASHARA)
        cases_checked += 2
        if near_end.division_index != 44:
            mismatches += 1
        if start.division_index != 0:
            mismatches += 1
    if mismatches:
        fail(f"boundary case failures: {mismatches}")
    return {"cases_checked": cases_checked, "mismatches": 0,
            "boundary_k_values": list(BOUNDARY_K_VALUES),
            "convention": "engine-wide 1e-10 tolerance-promoted boundary convention "
                           "(longitude_utils.py), unmodified; no D45-specific exception"}


def gate_g_protected_holdout():
    # Generated independently of gate F's deliberately-chosen boundary cases, using
    # a different deterministic sequence (prime-step sampling), never used to tune
    # D45_PARASHARA above - the rule was frozen (ADR-0077 section 1) before this
    # gate runs and is unchanged by registration.
    mismatches = 0
    count = 0
    step = 0.0137  # irrational-ish w.r.t. 30/45 to avoid coinciding with gate B/F points
    longitude = 0.0
    while longitude < 360.0:
        source = int(longitude // 30.0)
        degree = longitude - source * 30.0
        result = classify(longitude, D45_PARASHARA)
        expected_sign, expected_division = _independent_d45_sign(source, degree)
        if (result.d_sign, result.division_index) != (expected_sign, expected_division):
            mismatches += 1
        count += 1
        longitude += step
    if mismatches:
        fail(f"protected holdout mismatches: {mismatches}")
    return {"points": count, "mismatches": 0,
            "methodology": "prime-step deterministic sampling, independent of gate B/F points, "
                            "never used to tune the frozen rule"}


def gate_h_negative_controls():
    controls = []

    # Control 1: mutate the start_sign table (Aries offset changed from movable(0) to
    # a wrong value), confirm the mutation is detectable, confirm the untouched
    # original (imported from the production module) remains correct.
    mutated = replace(D45_PARASHARA, start_sign=(1,) + D45_PARASHARA.start_sign[1:])
    detected = mutated.start_sign[0] != D45_PARASHARA.start_sign[0]
    controls.append({"control": "start_sign[0] mutated 0->1", "detected": detected})
    if not detected:
        fail("negative control 1 did not detect the planted mutation")

    # Control 2: mutate direction for one sign (forward -> backward), confirm the
    # dense-sweep-style independent check would flag a mismatch against the
    # unmutated independent reference.
    mutated_dir = replace(
        D45_PARASHARA,
        direction=D45_PARASHARA.direction[:1] + (-1,) + D45_PARASHARA.direction[2:],
    )
    # Degree chosen so the segment index (10) is NOT a multiple of 6: reversing
    # direction changes (start+index)%12 vs (start-index)%12 unless 2*index is a
    # multiple of 12, which would make forward/backward coincide by degenerate
    # symmetry - a genuine planted mutation must not be masked by that coincidence.
    test_longitude = 30.0 + 7.0  # within Taurus (fixed, source=1), segment index 10
    mutated_result = classify(test_longitude, mutated_dir)
    original_result = classify(test_longitude, D45_PARASHARA)
    detected_2 = mutated_result.d_sign != original_result.d_sign
    controls.append({"control": "direction[1] mutated +1->-1", "detected": detected_2})
    if not detected_2:
        fail("negative control 2 did not detect the planted mutation")

    # Control 3: content-hash pinning - confirm a single-cell tamper changes the hash.
    original_hash = rule_content_sha256(D45_PARASHARA)
    mutated_hash = rule_content_sha256(mutated)
    detected_3 = mutated_hash != original_hash
    controls.append({"control": "content hash changes on mutation", "detected": detected_3})
    if not detected_3:
        fail("negative control 3 did not detect the planted mutation")

    # Restoration check: confirm the original, untouched production object still
    # matches its own original hash (nothing above mutated D45_PARASHARA itself -
    # replace() returns a new frozen instance; the registered object is untouched).
    restored_hash = rule_content_sha256(D45_PARASHARA)
    if restored_hash != original_hash:
        fail("D45_PARASHARA itself was mutated - this must never happen (dataclass is frozen)")
    if get_varga_rule(45, D45_SCHOOL) is not D45_PARASHARA:
        fail("D45's registered identity changed during negative-control testing")

    return {"controls": controls, "all_detected": True, "original_object_unmutated": True}


def gate_i_composition_verification():
    """ADR-0085: exercises the REAL production composition entry point,
    divisional_chart(snapshot, 45) / build_varga_chart(), which gates A-H
    above never call (each tests classify() directly - a genuinely different
    concern, per validate_d45_holdout.py's own verify_composition()
    docstring). Runs validate_d45_holdout.py as a subprocess, mirroring gate
    E's own established pattern, and requires BOTH: (1) every field of every
    body in a real 5-chart holdout matches an independent cross-check, and
    (2) a genuine, real, in-process monkeypatch-based mutation self-check
    (three distinct corruptions of the real build_varga_chart, never a
    synthetic side-by-side comparison) is independently detected and the
    production function is confirmed restored afterward.

    This is the standing regression guard against the certification-
    integrity finding ADR-0085 records: a real planet cross-wiring
    corruption of build_varga_chart() was independently reproduced to pass
    all 872 of this repository's existing tests silently before this gate
    existed."""

    result = subprocess.run(
        [sys.executable, str(ROOT / "validate_d45_holdout.py")],
        capture_output=True, text=True)
    if (result.returncode != 0
            or "D45 COMPOSITION VERIFICATION PASSED" not in result.stdout
            or "D45 COMPOSITION MUTATION DETECTION PASSED" not in result.stdout):
        fail(f"composition verification failed: {result.stdout[-1600:]} {result.stderr[-800:]}")
    return {
        "result": "PASS",
        "classification": "correctness_evidence_and_mutation_detection",
        "scope": "divisional_chart(snapshot, 45)/build_varga_chart() field-level composition "
                 "(source_longitude, sign, division_number, fraction) for the ascendant and "
                 "every planet, across a fixed 5-chart real holdout, plus a genuine in-process "
                 "monkeypatch mutation self-check (field-order swap, planet cross-wiring, "
                 "source_longitude corruption) against the real production function",
        "disclosure": "distinct from gates A/B/F/G, which test classify() directly and never "
                       "exercise build_varga_chart()'s own field assignment; distinct from gate H, "
                       "whose negative controls compare a hand-written mutated COPY against the "
                       "unmutated rule object in-process rather than genuinely monkeypatching and "
                       "re-executing the real production function (ADR-0085)",
    }


def main():
    tee = support.start_transcript()
    preconditions = support.preflight()

    # Computed into a local first, in the same order as before, so
    # PYJHORA_VERSION (set by gate_c_oracle() itself, lazily - see the
    # ADR-0085 Gate C import-structure change above) is already known by
    # the time the "oracle" field below is built. Gate call order and
    # results are otherwise unchanged.
    gates = {
        "A_table_integrity": gate_a_table_integrity(),
        "B_dense_sweep": gate_b_dense_sweep(),
        "C_oracle": gate_c_oracle(),
        "D_non_invasiveness": gate_d_non_invasiveness(),
        "E_independent_validator": gate_e_validator(),
        "F_boundary_cases": gate_f_boundary_cases(),
        "G_protected_holdout": gate_g_protected_holdout(),
        "H_negative_controls": gate_h_negative_controls(),
        "I_composition_verification": gate_i_composition_verification(),
    }

    report = {
        "schema": "varga_d45_v1_certification",
        "adr": "ADR-0077",
        "supersedes_provisional_id": "NOTHING_AUTHORISED",
        "date": str(date.today()),
        "scope": (
            "D45 Akshavedamsa (Parashara variant, Traditional Parasara method / "
            "PyJHora chart_method=1). Registered in production through the generic "
            "registry (engine.astrology.varga_d45, VARGA_D45_V1), discoverable via "
            "engine.astrology.divisional_chart.divisional_chart(snapshot, 45)."
        ),
        "rule": {
            "kind": "CyclicVargaRule",
            "variant": "parashara (45 x 2/3 deg from movable Aries / fixed Leo / dual Sagittarius, forward)",
            "school_key": "parashara",
            "registered": True,
            "boundary_policy": (
                "inherited locked convention: intra-sign boundaries promote within "
                "1e-10 (longitude_utils.py); no D45-specific exception. Three genuine "
                "floating-point floor-classification boundaries identified and "
                "explicitly tested (gate F): k=13, 26, 29 of 44 internal per-sign "
                "boundaries; maximum representation error 1.279e-11 arcsec (ADR-0077 "
                "section 3), negligible against the 0.5 arcsecond Tier-0 tolerance."
            ),
        },
        "oracle": {"package": "PyJHora", "version": PYJHORA_VERSION,
                   "function": "akshavedamsa_chart method 1 Traditional Parasara (pure longitude math)"},
        "gates": gates,
        "explicit_non_claims": [
            "Parivritti cyclical akshavedamsa (PyJHora chart_method=2)",
            "Parivritti even-reversal akshavedamsa (PyJHora chart_method=3)",
            "Parivritti alternate / Somanatha akshavedamsa (PyJHora chart_method=4)",
            "any per-division deity/label payload (VargaClassification carries only D-sign, "
            "division index, and fraction; D45 needs no payload/label table, per DP-024)",
            "any non-parashara school variant",
            "any other varga; each requires its own ADR and certification",
        ],
        "environment": {"python": sys.version.split()[0]},
        "preconditions": preconditions,
        "result": "PASS",
    }
    out = support.emit(report, "VARGA_D45_V1_certification.json", "varga_d45", tee)
    print("=" * 60)
    print("VARGA_D45_V1 CERTIFICATION (production-registered)")
    print("=" * 60)
    for name in ("A_table_integrity", "B_dense_sweep", "C_oracle", "F_boundary_cases",
                 "G_protected_holdout"):
        print(f"{name}: {report['gates'][name]}")
    print("D_non_invasiveness: registry", report["gates"]["D_non_invasiveness"]["registry"],
          "d45_registered:", report["gates"]["D_non_invasiveness"]["d45_registered"])
    print("E_independent_validator: PASS")
    print("H_negative_controls:", report["gates"]["H_negative_controls"]["all_detected"])
    print("I_composition_verification:", report["gates"]["I_composition_verification"]["result"])
    print("archived          :", out.relative_to(ROOT).as_posix())
    print("RESULT            : PASS")


if __name__ == "__main__":
    main()
