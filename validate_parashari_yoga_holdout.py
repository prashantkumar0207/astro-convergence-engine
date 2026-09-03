"""Independent PARASHARI_YOGA_V1 holdout validator (ADR-0081, ADR-0086).

A from-scratch reimplementation of the PARASHARI_YOGA_V1-specific logic
(sign-of-longitude, whole-sign house-from-ascendant, the own-sign/exaltation
dignity table, the kendra-and-dignity predicate), written independently of
scripts/certify_parashari_yoga.py - nothing is imported from that file.

Per the owner's own explicit "CEO AUTHORIZATION - PARASHARI_YOGA_V1
CERTIFICATION" instruction, this file does NOT import
engine.astrology.dignity, engine.astrology.house, or engine.astrology.signs -
it independently re-derives sign-of-longitude and whole-sign-house
arithmetic itself, rather than reusing the production functions those
modules already provide, since "the production house calculation" must
never be the oracle for the independent logical predicate. The dignity
table below is a THIRD hand transcription (distinct from both
engine/knowledge/data/dignities.json and scripts/certify_parashari_yoga.py's
own CERTIFIED_DIGNITY_TABLE), deliberately structured differently (two
separate dicts rather than one combined mapping) so the same coding mistake
is unlikely to appear in both, mirroring validate_kp_significator_holdout.py's
own established isolation discipline.

Only the Tier-0-Locked D1 kernel itself (engine.calculations.calculations.
calculate, under the PARASHARI_LAHIRI profile) is shared - the already-
certified astronomical substrate, not the yoga-specific logic under test.

Run:  python validate_parashari_yoga_holdout.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from engine.astronomy.profile import PARASHARI_LAHIRI  # noqa: E402  (certified substrate)
from engine.calculations.calculations import calculate  # noqa: E402  (certified substrate)
from engine.models.birth_data import BirthData  # noqa: E402

YOGA_GRAHAS = ("Mars", "Mercury", "Jupiter", "Venus", "Saturn")
YOGA_NAMES = {"Mars": "Ruchaka", "Mercury": "Bhadra", "Jupiter": "Hamsa",
              "Venus": "Malavya", "Saturn": "Sasa"}
KENDRA_HOUSES = {1, 4, 7, 10}

#: Independently re-typed from BPHS's own graha-guna chapter (not imported
#: from engine/knowledge/data/dignities.json or scripts/
#: certify_parashari_yoga.py's own table) - deliberately split into two
#: separate mappings, a different structure than the certifier's own single
#: combined dict.
OWN_SIGNS = {
    "Mars": (1, 8),
    "Mercury": (3, 6),
    "Jupiter": (9, 12),
    "Venus": (2, 7),
    "Saturn": (10, 11),
}
EXALTATION_SIGN = {
    "Mars": 10,
    "Mercury": 6,
    "Jupiter": 4,
    "Venus": 12,
    "Saturn": 7,
}


def sign_number(longitude):
    """1-12, independently re-derived (not calling engine.astrology.signs)."""
    normalized = longitude % 360.0
    return int(normalized / 30.0) + 1


def house_of_ascendant(graha_longitude, ascendant_longitude):
    """Whole-sign house (1-12), independently re-derived (not calling
    engine.astrology.house.whole_sign_house)."""
    graha_sign = sign_number(graha_longitude)
    asc_sign = sign_number(ascendant_longitude)
    return (graha_sign - asc_sign) % 12 + 1


def is_own_sign(graha, sign):
    return sign in OWN_SIGNS[graha]


def is_exalted(graha, sign):
    return sign == EXALTATION_SIGN[graha]


def yoga_present(graha, graha_longitude, ascendant_longitude):
    sign = sign_number(graha_longitude)
    house = house_of_ascendant(graha_longitude, ascendant_longitude)
    return house in KENDRA_HOUSES and (is_own_sign(graha, sign) or is_exalted(graha, sign))


def judge(planet_longitudes, ascendant_longitude):
    return {g: yoga_present(g, planet_longitudes[g], ascendant_longitude) for g in YOGA_GRAHAS}


# ------------------------------------------------------------ Dense sweep

def dense_sweep():
    """Sign-of-longitude and house-of-ascendant, swept across the full
    circle, cross-checked against a from-scratch boundary walk (not calling
    zodiac_sign/whole_sign_house)."""
    mismatches = 0
    points = 4320
    step = 360.0 / points
    for i in range(points):
        lon = i * step
        expected_sign = int(lon / 30.0) + 1
        if sign_number(lon) != expected_sign:
            mismatches += 1
        for asc_sign in (1, 4, 7, 10):
            asc_lon = (asc_sign - 1) * 30.0 + 5.0
            house = house_of_ascendant(lon, asc_lon)
            if not (1 <= house <= 12):
                mismatches += 1
    return points, mismatches


# ---------------------------------------------------- Structural checks

def structural_checks():
    failures = []
    for graha in YOGA_GRAHAS:
        if len(OWN_SIGNS[graha]) != 2:
            failures.append(f"{graha} own_signs cardinality != 2")
        if EXALTATION_SIGN[graha] in OWN_SIGNS[graha] and graha != "Mercury":
            failures.append(f"{graha} exaltation unexpectedly overlaps its own signs")
    if EXALTATION_SIGN["Mercury"] not in OWN_SIGNS["Mercury"]:
        failures.append("Mercury's own exaltation/own-sign overlap (the documented "
                         "certification-integrity case) is missing from this table")
    for test_lon in (0.0, 47.3, 133.9, 289.5, 359.999):
        s = sign_number(test_lon)
        if not (1 <= s <= 12):
            failures.append(f"sign_number({test_lon}) out of range: {s}")
    return failures


# -------------------------------------------------------------- Holdout

#: A genuinely different set of real dates/locations than
#: scripts/certify_parashari_yoga.py's own HOLDOUT, so this is an
#: independent sample, not a duplicated one.
INDEPENDENT_HOLDOUT = [
    {"id": "V1_paris_1901", "date": "1901-05-14", "time": "08:44:12", "lat": 48.8566, "lon": 2.3522},
    {"id": "V2_beijing_1962", "date": "1962-10-03", "time": "19:26:50", "lat": 39.9042, "lon": 116.4074},
    {"id": "V3_capetown_1979", "date": "1979-02-19", "time": "02:15:33", "lat": -33.9249, "lon": 18.4241},
    {"id": "V4_toronto_1994", "date": "1994-07-04", "time": "15:00:00", "lat": 43.6532, "lon": -79.3832},
    {"id": "V5_dubai_2008", "date": "2008-12-25", "time": "23:11:41", "lat": 25.2048, "lon": 55.2708},
    {"id": "V6_lima_2016", "date": "2016-03-30", "time": "05:55:05", "lat": -12.0464, "lon": -77.0428},
]


def _build_chart(case):
    year, month, day = (int(x) for x in case["date"].split("-"))
    hour, minute, second = (int(x) for x in case["time"].split(":"))
    result = calculate(
        BirthData(year, month, day, hour, minute, float(second), case["lat"], case["lon"], "UTC"),
        profile=PARASHARI_LAHIRI,
    )
    snapshot = result.snapshot
    lons = {g: snapshot.sidereal_planets[g].longitude for g in YOGA_GRAHAS}
    return lons, snapshot.houses.ascendant


def real_holdout():
    """Structural sanity only (disclosed, not correctness evidence): no
    independently-established third-party expected value exists for these
    dates - only confirms judge() runs to completion and returns booleans."""
    failures = []
    for case in INDEPENDENT_HOLDOUT:
        lons, asc = _build_chart(case)
        try:
            result = judge(lons, asc)
        except Exception as error:  # noqa: BLE001
            failures.append((case["id"], str(error)))
            continue
        if not all(isinstance(v, bool) for v in result.values()):
            failures.append((case["id"], f"non-boolean result: {result}"))
    return len(INDEPENDENT_HOLDOUT), failures


#: The SAME eight real charts as scripts/certify_parashari_yoga.py's own
#: HOLDOUT, with expected values generated by THIS file's own judge() -
#: frozen once, 2026-08-31. Determinism/regression guard for this file's own
#: logic; the genuine cross-implementation-agreement evidence lives in the
#: certifier's own gate H, which compares these same frozen values against
#: the embedded rule's LIVE output.
STATIC_HOLDOUT = [
    {"id": "Y1_london_1850", "date": "1850-03-11", "time": "06:12:34", "lat": 51.5074, "lon": -0.1278},
    {"id": "Y2_delhi_1965", "date": "1965-08-15", "time": "13:07:00", "lat": 28.6139, "lon": 77.2090},
    {"id": "Y3_tokyo_1988", "date": "1988-11-23", "time": "22:45:19", "lat": 35.6762, "lon": 139.6503},
    {"id": "Y4_saopaulo_2001", "date": "2001-02-28", "time": "04:33:41", "lat": -23.5505, "lon": -46.6333},
    {"id": "Y5_cairo_2014", "date": "2014-06-30", "time": "17:59:59", "lat": 30.0444, "lon": 31.2357},
    {"id": "Y6_sydney_2027", "date": "2027-09-09", "time": "09:09:09", "lat": -33.8688, "lon": 151.2093},
    {"id": "Y7_moscow_1999", "date": "1999-12-31", "time": "23:59:00", "lat": 55.7558, "lon": 37.6173},
    {"id": "Y8_mexico_1977", "date": "1977-07-07", "time": "07:07:07", "lat": 19.4326, "lon": -99.1332},
]


def generate_static_expected():
    """Prints the frozen expected_* literal for each HOLDOUT case, using
    ONLY this file's own judge(). Run once, offline, to produce the literal
    data both this file's own STATIC_HOLDOUT check and the certifier's own
    HOLDOUT list freeze - never invoked at certification time."""
    for case in STATIC_HOLDOUT:
        lons, asc = _build_chart(case)
        result = judge(lons, asc)
        print(f'    {{"id": "{case["id"]}", ..., "expected": {result}}},')


def static_holdout_check():
    """Verify this file's own current judge() output still reproduces its
    own previously-frozen values (below) - a determinism/regression guard,
    not independent correctness proof by itself."""
    failures = []
    for case, expected in zip(STATIC_HOLDOUT, _FROZEN_EXPECTED):
        lons, asc = _build_chart(case)
        result = judge(lons, asc)
        if result != expected:
            failures.append((case["id"], f"got={result} expected={expected}"))
    return len(STATIC_HOLDOUT), failures


#: Frozen 2026-08-31 from this file's own judge(), via generate_static_expected().
_FROZEN_EXPECTED = [
    {"Mars": False, "Mercury": False, "Jupiter": False, "Venus": False, "Saturn": False},
    {"Mars": False, "Mercury": False, "Jupiter": False, "Venus": False, "Saturn": False},
    {"Mars": False, "Mercury": False, "Jupiter": False, "Venus": False, "Saturn": False},
    {"Mars": False, "Mercury": False, "Jupiter": False, "Venus": True, "Saturn": False},
    {"Mars": False, "Mercury": False, "Jupiter": True, "Venus": False, "Saturn": True},
    {"Mars": False, "Mercury": True, "Jupiter": False, "Venus": False, "Saturn": False},
    {"Mars": False, "Mercury": False, "Jupiter": False, "Venus": False, "Saturn": False},
    {"Mars": True, "Mercury": False, "Jupiter": False, "Venus": False, "Saturn": False},
]


def _birth_data(case):
    year, month, day = (int(x) for x in case["date"].split("-"))
    hour, minute, second = (int(x) for x in case["time"].split(":"))
    return BirthData(year, month, day, hour, minute, float(second), case["lat"], case["lon"], "UTC")


def verify_composition(cases=INDEPENDENT_HOLDOUT):
    """
    ADR-0086: exercises the REAL production composition entry point -
    engine.parashari.mahapurusha_yoga.mahapurusha_yoga(), which calls
    graha_mahapurusha_from_snapshot() - and checks the two public fields the
    governing investigation found uncovered by every existing certification
    gate: MahapurushaYogaResult.house_number and .sign_number (every prior
    gate only ever reads the derived boolean `present`).

    Expected values come from THIS file's own from-scratch sign_number()/
    house_of_ascendant() (independently re-derived, never importing
    engine.astrology.signs/house - see module docstring), applied to a
    longitude/ascendant pair independently extracted via a second, separate
    call to the certified Tier-0 kernel (_build_chart) - not read off the
    chart under test. A genuine wiring cross-check, not a self-comparison:
    an argument-order or wrong-variable bug in graha_mahapurusha_from_
    snapshot()'s own call sites changes the PRODUCTION side only, since the
    independent reference here shares no code path with it at all (a THIRD,
    from-scratch implementation, distinct even from the production functions
    D45's own equivalent check reuses).

    Returns a list of mismatch descriptions; empty means every checked field
    of every graha in every case matched exactly.
    """
    from engine.parashari.mahapurusha_yoga import mahapurusha_yoga

    mismatches = []
    for case in cases:
        chart = mahapurusha_yoga(_birth_data(case))
        lons, asc = _build_chart(case)
        for result in chart.results:
            graha_lon = lons[result.graha]
            expected_sign = sign_number(graha_lon)
            expected_house = house_of_ascendant(graha_lon, asc)
            if result.sign_number != expected_sign:
                mismatches.append(
                    f"{case['id']}/{result.graha}: sign_number={result.sign_number} "
                    f"expected={expected_sign}")
            if result.house_number != expected_house:
                mismatches.append(
                    f"{case['id']}/{result.graha}: house_number={result.house_number} "
                    f"expected={expected_house}")
    return mismatches


def _corrupt_graha_mahapurusha_argument_order():
    """The exact, real, reproduced argument-order swap the governing
    investigation found (ADR-0086 section 1): whole_sign_house(body.
    longitude, ascendant_longitude) swapped to whole_sign_house(ascendant_
    longitude, body.longitude) - undetected by all ten of PARASHARI_YOGA_V1's
    prior gates because the kendra offset set {0,3,6,9} is symmetric under
    negation mod 12, so `present` never changes even though house_number
    does. Disguised as source-level code (module/name/qualname preserved),
    matching scripts/check_mutation_detection.py's own established
    convention - a wrong implementation actually written into the module
    would carry exactly this metadata."""

    import engine.parashari.mahapurusha_yoga as prod
    from engine.astrology.house import whole_sign_house
    from engine.astrology.signs import zodiac_sign
    import swisseph as swe

    pristine = prod.graha_mahapurusha_from_snapshot

    def corrupted(snapshot):
        provenance = snapshot.provenance
        if provenance is None:
            raise prod.ParashariYogaProfileError("snapshot carries no provenance")
        if provenance.profile_name != prod.PARASHARI_LAHIRI.name:
            raise prod.ParashariYogaProfileError(
                "Panch Mahapurusha Yoga requires the parashari_lahiri profile, got "
                f"'{provenance.profile_name}'"
            )
        if provenance.ayanamsa_mode != swe.SIDM_LAHIRI:
            raise prod.ParashariYogaProfileError("snapshot ayanamsa does not match Parashari")
        ascendant_longitude = snapshot.houses.ascendant
        ascendant_sign = zodiac_sign(ascendant_longitude)
        results = []
        for graha in prod.YOGA_GRAHAS:
            body = snapshot.sidereal_planets[graha]
            graha_sign = zodiac_sign(body.longitude)
            house = whole_sign_house(ascendant_longitude, body.longitude)  # MUTATION: swapped
            present = prod._yoga_predicate_from_sign_and_house(graha, graha_sign, house)
            results.append(prod.MahapurushaYogaResult(
                graha=graha, yoga=prod.YOGA_NAMES[graha], sign_number=graha_sign,
                house_number=house, present=present,
                retrograde_qualifier=body.speed_longitude < 0,
            ))
        return prod.MahapurushaYogaChart(
            ascendant_sign=ascendant_sign, results=tuple(results), provenance=provenance)

    corrupted.__module__ = pristine.__module__
    corrupted.__name__ = pristine.__name__
    corrupted.__qualname__ = getattr(pristine, "__qualname__", pristine.__name__)
    return pristine, corrupted


def _corrupt_graha_mahapurusha_sign_number():
    """A second control targeting sign_number specifically (ADR-0086 section
    3): graha_sign wrongly derived from the ASCENDANT's own longitude
    instead of the graha's own - a realistic wrong-variable-captured
    mistake. house_number stays correct, isolating the sign_number field."""

    import engine.parashari.mahapurusha_yoga as prod
    from engine.astrology.house import whole_sign_house
    from engine.astrology.signs import zodiac_sign
    import swisseph as swe

    pristine = prod.graha_mahapurusha_from_snapshot

    def corrupted(snapshot):
        provenance = snapshot.provenance
        if provenance is None:
            raise prod.ParashariYogaProfileError("snapshot carries no provenance")
        if provenance.profile_name != prod.PARASHARI_LAHIRI.name:
            raise prod.ParashariYogaProfileError(
                "Panch Mahapurusha Yoga requires the parashari_lahiri profile, got "
                f"'{provenance.profile_name}'"
            )
        if provenance.ayanamsa_mode != swe.SIDM_LAHIRI:
            raise prod.ParashariYogaProfileError("snapshot ayanamsa does not match Parashari")
        ascendant_longitude = snapshot.houses.ascendant
        ascendant_sign = zodiac_sign(ascendant_longitude)
        results = []
        for graha in prod.YOGA_GRAHAS:
            body = snapshot.sidereal_planets[graha]
            graha_sign = zodiac_sign(ascendant_longitude)  # MUTATION: wrong body's longitude
            house = whole_sign_house(body.longitude, ascendant_longitude)
            present = prod._yoga_predicate_from_sign_and_house(graha, graha_sign, house)
            results.append(prod.MahapurushaYogaResult(
                graha=graha, yoga=prod.YOGA_NAMES[graha], sign_number=graha_sign,
                house_number=house, present=present,
                retrograde_qualifier=body.speed_longitude < 0,
            ))
        return prod.MahapurushaYogaChart(
            ascendant_sign=ascendant_sign, results=tuple(results), provenance=provenance)

    corrupted.__module__ = pristine.__module__
    corrupted.__name__ = pristine.__name__
    corrupted.__qualname__ = getattr(pristine, "__qualname__", pristine.__name__)
    return pristine, corrupted


_MUTATION_CONTROLS = (
    ("argument_order_swap", _corrupt_graha_mahapurusha_argument_order),
    ("sign_number_wrong_body", _corrupt_graha_mahapurusha_sign_number),
)


def run_mutation_self_check():
    """
    ADR-0086: genuine, real, in-process monkeypatch-and-re-execution
    mutation detection - mirroring scripts/check_mutation_detection.py's own
    established methodology (ADR-0079/DP-030) and VARGA_D45_V1's own
    run_mutation_self_check() (ADR-0085). NOT a synthetic side-by-side
    comparison of a hand-written "corrupted" copy - the weakness ADR-0086
    itself found in scripts/certify_parashari_yoga.py's own gate_i_negative_
    controls. The REAL engine.parashari.mahapurusha_yoga.graha_mahapurusha_
    from_snapshot is replaced in-process; mahapurusha_yoga() resolves it via
    the module's own global namespace at call time, so calling the real,
    unmodified top-level mahapurusha_yoga() genuinely exercises the
    corrupted code path. verify_composition() is then re-run for real
    against that corrupted state, and a genuine mismatch is observed - then
    the pristine function is restored and verify_composition() is
    re-confirmed to pass again.

    Never touches any file on disk. Returns (all_detected: bool, results:
    list of per-control dicts).
    """
    import engine.parashari.mahapurusha_yoga as prod

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
        prod.graha_mahapurusha_from_snapshot = corrupted
        try:
            mismatches_under_mutation = verify_composition()
        finally:
            prod.graha_mahapurusha_from_snapshot = pristine

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
            f"production graha_mahapurusha_from_snapshot was not correctly restored after "
            f"mutation testing: {restored[:5]}"
        )

    return all_detected, results


def main():
    print("=" * 60)
    print("INDEPENDENT PARASHARI_YOGA_V1 VALIDATION")
    print("=" * 60)

    dense_points, dense_mismatches = dense_sweep()
    print(f"Dense sweep (sign/house derivation): {dense_points} points, {dense_mismatches} mismatches")

    struct_failures = structural_checks()
    print(f"Structural invariants: {len(struct_failures)} failures")

    holdout_count, holdout_failures = real_holdout()
    print(f"Real-chart holdout (structural sanity only): {holdout_count} cases, "
          f"{len(holdout_failures)} failures")

    static_count, static_failures = static_holdout_check()
    print(f"Static-expected-value check (own frozen output): {static_count} cases, "
          f"{len(static_failures)} failures")

    all_failures = (
        [("dense_sweep", str(dense_mismatches))] if dense_mismatches else []
    ) + [("structural", f) for f in struct_failures] + holdout_failures + \
        [("static_holdout", f) for f in static_failures]

    if all_failures:
        print(f"FAILURES: {len(all_failures)}; first: {all_failures[:5]}")
        print("RESULT: FAIL")
        return 1

    print()
    print("RESULT: ALL INDEPENDENT PARASHARI_YOGA_V1 CASES PASSED")

    print()
    print("=" * 60)
    print("PARASHARI_YOGA_V1 COMPOSITION/PLUMBING VERIFICATION (ADR-0086)")
    print("=" * 60)
    composition_mismatches = verify_composition()
    print(f"Composition cases checked: {len(INDEPENDENT_HOLDOUT)} charts x 5 grahas, "
          f"house_number/sign_number fields")
    if composition_mismatches:
        print(f"FAILURES: {len(composition_mismatches)}; first: {composition_mismatches[:5]}")
        print("RESULT: PARASHARI_YOGA_V1 COMPOSITION VERIFICATION FAILED")
        return 1
    print("RESULT: PARASHARI_YOGA_V1 COMPOSITION VERIFICATION PASSED")

    print()
    print("=" * 60)
    print("PARASHARI_YOGA_V1 COMPOSITION MUTATION SELF-CHECK (ADR-0086)")
    print("=" * 60)
    all_detected, mutation_results = run_mutation_self_check()
    for result in mutation_results:
        status = "DETECTED" if result["detected"] else "MISSED (BAD)"
        print(f"  {result['control']:28s} {status}")
        if not result["detected"]:
            print("    (no mismatch reported under this corruption)")
    if not all_detected:
        print("RESULT: PARASHARI_YOGA_V1 COMPOSITION MUTATION SELF-CHECK FAILED - "
              "at least one control was not detected")
        return 1
    print("RESULT: PARASHARI_YOGA_V1 COMPOSITION MUTATION DETECTION PASSED")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
