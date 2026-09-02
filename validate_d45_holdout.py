"""Independent D45 Akshavedamsa holdout validator (ADR-0077, ADR-0085).

Validates the PRODUCTION, registered D45 rule (engine.astrology.varga_d45,
VARGA_D45_V1) against a reference built INDEPENDENTLY inside this file: a
per-sign lookup table constructed by direct sign-name enumeration (movable/
fixed/dual triads), not the framework's own modular-arithmetic offsets.

ADR-0085 addition: this file also verifies the COMPOSITION/PLUMBING layer -
engine.astrology.divisional_chart.divisional_chart(snapshot, 45) /
engine.astrology.varga_chart_builder.build_varga_chart() - which the
classify()-only checks above (and every gate in scripts/certify_d45.py) never
exercise. See verify_composition() and run_mutation_self_check() below. This
targets a class of defect distinct from classify()'s own correctness (already
covered by the dense/boundary batteries above and by certify_d45.py's own
gates A/B/F/G): whether build_varga_chart() correctly WIRES each already-
correct classify() result into the right VargaPosition/VargaPlanet slot for
the right body, without swapping fields or cross-wiring planets. A real,
independently-reproduced planet cross-wiring mutation was shown (this task's
own governing investigation, recorded in ADR-0085) to pass all 872 tests in
this repository's existing suite silently - this is the standing regression
guard against that specific defect class.

Run:  python validate_d45_holdout.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import engine.astrology  # noqa: F401  (registers production vargas, including D45)
from engine.astrology.varga_classifier import classify  # framework (SUBJECT)
from engine.astrology.varga_registry import get_varga_rule

SIGNS = ("Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces")

#: Independent reference, built by direct enumeration (not offset arithmetic):
#: for a movable-sign source, the 45-part sequence starts at Aries and repeats
#: the twelve signs in zodiacal order; fixed starts at Leo; dual starts at
#: Sagittarius. Materialized as an explicit 45-entry table per source sign.
_MOVABLE_START, _FIXED_START, _DUAL_START = "Aries", "Leo", "Sagittarius"
_MOVABLE, _FIXED, _DUAL = (
    {"Aries", "Cancer", "Libra", "Capricorn"},
    {"Taurus", "Leo", "Scorpio", "Aquarius"},
    {"Gemini", "Virgo", "Sagittarius", "Pisces"},
)

REFERENCE_TABLE = {}
for _source_name in SIGNS:
    if _source_name in _MOVABLE:
        _start = SIGNS.index(_MOVABLE_START)
    elif _source_name in _FIXED:
        _start = SIGNS.index(_FIXED_START)
    else:
        _start = SIGNS.index(_DUAL_START)
    REFERENCE_TABLE[_source_name] = tuple(
        SIGNS[(_start + _k) % 12] for _k in range(45)
    )


#: Independently re-derived from the engine's own documented, already-locked
#: boundary rule (engine/astrology/longitude_utils.py's own docstring: "a degree
#: within BOUNDARY_TOLERANCE below a division's edge promotes to the next
#: division"), not imported from that module - this validator applies the SAME
#: documented convention on its own terms, so it checks whether classify()
#: correctly IMPLEMENTS the documented rule, not whether it matches a naive,
#: unpromoted floor (which would spuriously "fail" at every one of D45's own
#: non-exact 2/3-degree boundaries, per ADR-0077 section 3).
_BOUNDARY_TOLERANCE = 1e-10


def reference_d45(longitude: float):
    longitude = longitude % 360.0
    source = int(longitude // 30.0)
    degree = longitude - source * 30.0
    width = 30.0 / 45.0
    division = int((degree + _BOUNDARY_TOLERANCE) / width)
    if division > 44:
        division = 44
    return SIGNS.index(REFERENCE_TABLE[SIGNS[source]][division]), division


#: Real, fixed holdout birth data for the composition/plumbing check
#: (ADR-0085) - distinct from the dense/boundary sweeps above, which need no
#: real chart at all. Chosen fresh for this check, spanning both hemispheres
#: and a range of eras, never used to tune classify() or the frozen rule.
COMPOSITION_HOLDOUT = [
    {"id": "C1_delhi_1990", "year": 1990, "month": 5, "day": 15, "hour": 10,
     "minute": 30, "second": 0.0, "lat": 28.6139, "lon": 77.2090},
    {"id": "C2_newyork_1972", "year": 1972, "month": 11, "day": 3, "hour": 4,
     "minute": 17, "second": 22.0, "lat": 40.7128, "lon": -74.0060},
    {"id": "C3_johannesburg_2005", "year": 2005, "month": 2, "day": 27, "hour": 19,
     "minute": 52, "second": 8.0, "lat": -26.2041, "lon": 28.0473},
    {"id": "C4_reykjavik_2018", "year": 2018, "month": 8, "day": 9, "hour": 1,
     "minute": 3, "second": 44.0, "lat": 64.1466, "lon": -21.9426},
    {"id": "C5_singapore_1961", "year": 1961, "month": 6, "day": 21, "hour": 15,
     "minute": 40, "second": 12.0, "lat": 1.3521, "lon": 103.8198},
]


def _composition_snapshot(case):
    from engine.astronomy.profile import PARASHARI_LAHIRI
    from engine.calculations.calculations import calculate
    from engine.models.birth_data import BirthData

    bd = BirthData(case["year"], case["month"], case["day"], case["hour"],
                    case["minute"], case["second"], case["lat"], case["lon"], "UTC")
    return calculate(bd, profile=PARASHARI_LAHIRI).snapshot


def verify_composition(cases=COMPOSITION_HOLDOUT):
    """
    Exercise the REAL production composition entry point -
    engine.astrology.divisional_chart.divisional_chart(snapshot, 45), which
    calls engine.astrology.varga_chart_builder.build_varga_chart() - and
    check every field of every resulting VargaPosition/VargaPlanet, not just
    a derived boolean or the chart-level varga/school/provenance metadata
    every existing check (certify_d45.py, engine/tests/test_varga_d45.py,
    the original production-implementation commit's own manual check)
    stops at.

    This is deliberately NOT a re-test of classify()'s own correctness
    (already covered exhaustively above and by certify_d45.py's gates A/B/
    F/G): the "expected" value for each body is obtained by calling the SAME
    already-verified classify() a second time, directly, on that body's OWN
    real longitude - a legitimate wiring cross-check, not a self-comparison,
    exactly mirroring the established gate_b2/gate_g pattern already used by
    this project's PARASHARI_YOGA_V1 certifier (docs/DECISION_LOG.md,
    ADR-0081) to catch plumbing bugs that classify()'s own correctness tests
    cannot see. A genuine corruption of build_varga_chart() (a field swap,
    or - the more severe case demonstrated in ADR-0085's own governing
    investigation - assigning one body's classification to a different
    body) changes classify()'s SECOND, independent call's result relative to
    what the (corrupted) chart actually stored, and is therefore caught
    here, deterministically.

    Returns a list of mismatch descriptions; empty means every field of
    every body in every case matched exactly.
    """
    from engine.astrology.divisional_chart import divisional_chart

    rule = get_varga_rule(45, "parashara")
    mismatches = []

    for case in cases:
        snapshot = _composition_snapshot(case)
        chart = divisional_chart(snapshot, 45)

        if chart.varga != 45 or chart.school != "parashara":
            mismatches.append(f"{case['id']}: chart.varga={chart.varga} chart.school={chart.school}")
        if chart.provenance is not snapshot.provenance:
            mismatches.append(f"{case['id']}: chart.provenance is not the snapshot's own provenance")

        bodies = [("ascendant", snapshot.houses.ascendant, chart.ascendant)]
        for name, planet in snapshot.sidereal_planets.items():
            bodies.append((name, planet.longitude, chart.planets[name]))

        for label, source_longitude, position in bodies:
            expected = classify(source_longitude, rule)
            if position.source_longitude != source_longitude:
                mismatches.append(
                    f"{case['id']}/{label}: source_longitude={position.source_longitude!r} "
                    f"expected={source_longitude!r}")
            if position.sign != expected.d_sign:
                mismatches.append(
                    f"{case['id']}/{label}: sign={position.sign} expected={expected.d_sign}")
            if position.division_number != expected.division_number:
                mismatches.append(
                    f"{case['id']}/{label}: division_number={position.division_number} "
                    f"expected={expected.division_number}")
            if position.fraction != expected.fraction:
                mismatches.append(
                    f"{case['id']}/{label}: fraction={position.fraction!r} "
                    f"expected={expected.fraction!r}")

    return mismatches


def _corrupt_build_varga_chart_field_swap():
    """A realistic wrong-implementation mistake: sign and division_number
    swapped inside the per-planet/ascendant VargaPosition/VargaPlanet
    construction. Disguised as source-level code (module/name/qualname
    preserved), matching scripts/check_mutation_detection.py's own
    established disguise convention for engine.kp.* corruptions - a wrong
    implementation actually written into the module carries exactly this
    metadata, unlike a naive runtime monkeypatch."""

    from engine.astrology.varga_classifier import classify as _classify
    from engine.models.varga_chart import VargaChart
    from engine.models.varga_planet import VargaPlanet, VargaPosition

    def corrupted(snapshot, division, rule, school):
        asc = _classify(snapshot.houses.ascendant, rule)
        ascendant = VargaPosition(
            source_longitude=snapshot.houses.ascendant,
            sign=asc.division_number,        # swapped
            division_number=asc.d_sign,       # swapped
            fraction=asc.fraction,
        )
        planets = {}
        for name, planet in snapshot.sidereal_planets.items():
            c = _classify(planet.longitude, rule)
            planets[name] = VargaPlanet(
                name=name,
                source_longitude=planet.longitude,
                sign=c.division_number,        # swapped
                division_number=c.d_sign,       # swapped
                fraction=c.fraction,
            )
        return VargaChart(varga=division, school=school, ascendant=ascendant,
                           planets=planets, provenance=snapshot.provenance)

    import engine.astrology.varga_chart_builder as builder_module
    pristine = builder_module.build_varga_chart
    corrupted.__module__ = pristine.__module__
    corrupted.__name__ = pristine.__name__
    corrupted.__qualname__ = getattr(pristine, "__qualname__", pristine.__name__)
    return pristine, corrupted


def _corrupt_build_varga_chart_cross_wiring():
    """A second, independently realistic mistake: each planet after the
    first receives the PREVIOUS planet's own classification instead of its
    own (a loop-variable-reuse error). Every field stays within its own
    valid range - unlike the field-swap corruption above, no generic range/
    convention check anywhere in this repository's own test suite happens
    to catch this one (verified directly in the governing investigation,
    ADR-0085: 872/872 tests passed under this exact corruption)."""

    from engine.astrology.varga_classifier import classify as _classify
    from engine.models.varga_chart import VargaChart
    from engine.models.varga_planet import VargaPlanet, VargaPosition

    def corrupted(snapshot, division, rule, school):
        asc = _classify(snapshot.houses.ascendant, rule)
        ascendant = VargaPosition(
            source_longitude=snapshot.houses.ascendant,
            sign=asc.d_sign, division_number=asc.division_number, fraction=asc.fraction,
        )
        planets = {}
        previous = None
        for name, planet in snapshot.sidereal_planets.items():
            c = _classify(planet.longitude, rule)
            use = previous if previous is not None else c
            planets[name] = VargaPlanet(
                name=name,
                source_longitude=planet.longitude,
                sign=use.d_sign, division_number=use.division_number, fraction=use.fraction,
            )
            previous = c
        return VargaChart(varga=division, school=school, ascendant=ascendant,
                           planets=planets, provenance=snapshot.provenance)

    import engine.astrology.varga_chart_builder as builder_module
    pristine = builder_module.build_varga_chart
    corrupted.__module__ = pristine.__module__
    corrupted.__name__ = pristine.__name__
    corrupted.__qualname__ = getattr(pristine, "__qualname__", pristine.__name__)
    return pristine, corrupted


def _corrupt_build_varga_chart_source_longitude():
    """A third, distinct corruption: source_longitude corrupted to always
    record the ASCENDANT's own longitude for every planet, while sign/
    division_number/fraction remain correctly derived from the planet's own
    real longitude - a realistic "wrong variable captured" mistake that
    leaves the classification itself right but the audit-trail field wrong."""

    from engine.astrology.varga_classifier import classify as _classify
    from engine.models.varga_chart import VargaChart
    from engine.models.varga_planet import VargaPlanet, VargaPosition

    def corrupted(snapshot, division, rule, school):
        asc = _classify(snapshot.houses.ascendant, rule)
        ascendant = VargaPosition(
            source_longitude=snapshot.houses.ascendant,
            sign=asc.d_sign, division_number=asc.division_number, fraction=asc.fraction,
        )
        planets = {}
        for name, planet in snapshot.sidereal_planets.items():
            c = _classify(planet.longitude, rule)
            planets[name] = VargaPlanet(
                name=name,
                source_longitude=snapshot.houses.ascendant,  # corrupted: wrong body's longitude
                sign=c.d_sign, division_number=c.division_number, fraction=c.fraction,
            )
        return VargaChart(varga=division, school=school, ascendant=ascendant,
                           planets=planets, provenance=snapshot.provenance)

    import engine.astrology.varga_chart_builder as builder_module
    pristine = builder_module.build_varga_chart
    corrupted.__module__ = pristine.__module__
    corrupted.__name__ = pristine.__name__
    corrupted.__qualname__ = getattr(pristine, "__qualname__", pristine.__name__)
    return pristine, corrupted


_MUTATION_CONTROLS = (
    ("field_order_swap", _corrupt_build_varga_chart_field_swap),
    ("planet_cross_wiring", _corrupt_build_varga_chart_cross_wiring),
    ("source_longitude_corruption", _corrupt_build_varga_chart_source_longitude),
)


def run_mutation_self_check():
    """
    Genuine, real, in-process monkeypatch-and-re-execution mutation
    detection (ADR-0085) - mirroring scripts/check_mutation_detection.py's
    own established methodology (built for the ADR-0079/DP-030
    KP_SIGNIFICATOR_V1 repair), applied here to
    engine.astrology.varga_chart_builder.build_varga_chart. This is NOT a
    synthetic side-by-side comparison of a hand-written "corrupted" copy
    (the weakness ADR-0085 itself found in every existing negative-control
    gate this repository has, including this D45 certifier's own gate H):
    the REAL production function is replaced in-process, the REAL
    verify_composition() is re-run against the REAL (corrupted) code path,
    and a genuine mismatch is observed - then the pristine function is
    restored and verify_composition() is re-confirmed to pass again.

    Never touches any file on disk. Returns (all_detected: bool, results:
    list of per-control dicts).
    """
    import engine.astrology.varga_chart_builder as builder_module

    clean = verify_composition()
    if clean:
        raise AssertionError(
            f"cannot run the mutation self-check: verify_composition() already reports "
            f"mismatches against the PRISTINE production code: {clean[:5]}"
        )

    results = []
    all_detected = True
    for control_name, corrupt_factory in _MUTATION_CONTROLS:
        pristine, corrupted = corrupt_factory()
        builder_module.build_varga_chart = corrupted
        try:
            mismatches_under_mutation = verify_composition()
        finally:
            builder_module.build_varga_chart = pristine

        detected = bool(mismatches_under_mutation)
        results.append({
            "control": control_name,
            "detected": detected,
            "sample_mismatch": mismatches_under_mutation[0] if mismatches_under_mutation else None,
        })
        if not detected:
            all_detected = False

    restored = verify_composition()
    if restored:
        raise AssertionError(
            f"production build_varga_chart was not correctly restored after mutation "
            f"testing: {restored[:5]}"
        )

    return all_detected, results


def main() -> int:
    rule = get_varga_rule(45, "parashara")
    failures = []

    dense = 0
    step = 360.0 / 51429
    for i in range(51429):
        longitude = i * step
        result = classify(longitude, rule)
        expected_sign, expected_division = reference_d45(longitude)
        if (result.d_sign, result.division_index) != (expected_sign, expected_division):
            failures.append(("dense", longitude))
        dense += 1

    boundary = 0
    for k in range(540):  # 45 divisions x 12 signs
        base = k * (30.0 / 45.0)
        points = [base]
        up = base
        import math
        for _ in range(3):
            up = math.nextafter(up, math.inf)
            points.append(up)
        for longitude in points:
            if longitude >= 360.0:
                continue
            result = classify(longitude, rule)
            expected_sign, expected_division = reference_d45(longitude)
            if (result.d_sign, result.division_index) != (expected_sign, expected_division):
                failures.append(("boundary", longitude))
            boundary += 1

    print("=" * 60)
    print("INDEPENDENT D45 AKSHAVEDAMSA VALIDATION")
    print("=" * 60)
    print(f"Dense cases    : {dense}")
    print(f"Boundary cases : {boundary}")
    if failures:
        print(f"FAILURES: {len(failures)}; first: {failures[:5]}")
        print("RESULT: FAIL")
        return 1
    print()
    print("RESULT: ALL INDEPENDENT D45 CASES PASSED")

    print()
    print("=" * 60)
    print("D45 COMPOSITION/PLUMBING VERIFICATION (ADR-0085)")
    print("=" * 60)
    composition_mismatches = verify_composition()
    print(f"Composition cases checked: {len(COMPOSITION_HOLDOUT)} charts x "
          f"(1 ascendant + N planets), every field")
    if composition_mismatches:
        print(f"FAILURES: {len(composition_mismatches)}; first: {composition_mismatches[:5]}")
        print("RESULT: D45 COMPOSITION VERIFICATION FAILED")
        return 1
    print("RESULT: D45 COMPOSITION VERIFICATION PASSED")

    print()
    print("=" * 60)
    print("D45 COMPOSITION MUTATION SELF-CHECK (ADR-0085)")
    print("=" * 60)
    all_detected, mutation_results = run_mutation_self_check()
    for result in mutation_results:
        status = "DETECTED" if result["detected"] else "MISSED (BAD)"
        print(f"  {result['control']:28s} {status}")
        if not result["detected"]:
            print(f"    (no mismatch reported under this corruption)")
    if not all_detected:
        print("RESULT: D45 COMPOSITION MUTATION SELF-CHECK FAILED - "
              "at least one control was not detected")
        return 1
    print("RESULT: D45 COMPOSITION MUTATION DETECTION PASSED")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
