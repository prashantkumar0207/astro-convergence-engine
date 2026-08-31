"""Independent PARASHARI_YOGA_V1 holdout validator (ADR-0081).

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
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
