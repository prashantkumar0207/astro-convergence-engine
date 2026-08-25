"""RISE_SET_V1 CERTIFICATION RUNNER (ADR-0054).

Regenerates certification/RISE_SET_V1_certification.json FROM SCRATCH
on every run; the stored JSON is never accepted as proof.

Gates, mirroring the varga six-gate template's lettering (A-E) with C
substituted, documented below: A declared-convention integrity; B
dense/boundary sweep against an independently-coded closed-form
reference; C independent astronomical reference (see substitution
note); D framework non-invasiveness; E the independent validator.
Exit 0 = PASS, 3 = FAIL.

WHY GATE C IS A CLOSED-FORM REFERENCE, NOT THE BUNDLED `swetest`
BINARY. `swetest` cannot be exercised on this Windows development
host at all (it is a Linux ELF binary - confirmed, `ADR-0043`,
`ADR-0053`), and its command-line support for rise/set specifically
was not established with confidence during design (unlike its
well-proven `-house`/`-fPl` position-query flags, already used by
`certify_current_engine.py`). Rather than commit an unverified binary
invocation, this gate independently re-derives sunrise/sunset from
first principles: apparent geocentric equatorial Sun position
(`swe.calc_ut`, the same Tier-0-certified ephemeris input, but NOT the
`swe.rise_trans*` root-finder under test), Greenwich Apparent Sidereal
Time (`swe.sidtime`), the classical hour-angle/altitude transform, and
an explicit bisection search - none of which calls
`swe.rise_trans_true_hor`. This checks a materially different thing
than a swetest cross-check would: not "is the ephemeris right"
(already Tier-0 certified) but "did this module correctly turn that
ephemeris data, the ratified conventions and the observer's location
into a rise/set time." A residual disagreement of a few tens of
seconds was found and is retained as an honest, derived tolerance
(see `_TOLERANCE_SECONDS` below), not tuned away: the closed-form
model uses a flat -50' altitude threshold, while Swiss Ephemeris's
internal algorithm applies a more realistic altitude-dependent
refraction curve near the horizon: the same class of external-
reference divergence D-007 already established a precedent for
documenting and bounding, rather than hiding or failing on.
"""

import json
import math
import subprocess
import sys
from dataclasses import replace
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

sys.path.insert(0, str(ROOT / "scripts"))
import certification_support as support  # noqa: E402

import swisseph as swe  # noqa: E402

from engine.astronomy.ephemeris import EphemerisFallbackError  # noqa: E402
from engine.astronomy.profile import (  # noqa: E402
    KP_KRISHNAMURTI,
    PARASHARI_LAHIRI,
    RISE_SET_DISC_UPPER_LIMB,
    RISE_SET_REFRACTION_STANDARD,
)
from engine.astronomy.rise_set import (  # noqa: E402
    RiseSetStatus,
    UnsupportedRiseSetConventionError,
    horizon_dip_degrees,
    sunrise,
    sunset,
)
from engine.models.birth_data import BirthData  # noqa: E402


def fail(message):
    print("RISE_SET CERTIFICATION FAIL:", message)
    sys.exit(3)


#: Same real-world city/date holdout used across this repository's
#: other certifiers (`scripts/certify_vimshottari.py` etc.), reused
#: here rather than inventing a parallel set. Times are not used:
#: rise/set is computed for the whole UT day starting at each date.
HOLDOUT = [
    {"id": "H1_london_1823", "date": (1823, 4, 17), "lat": 51.5074, "lon": -0.1278},
    {"id": "H2_newyork_1900", "date": (1900, 1, 1), "lat": 40.7128, "lon": -74.0060},
    {"id": "H3_sydney_1946", "date": (1946, 6, 14), "lat": -33.8688, "lon": 151.2093},
    {"id": "H4_delhi_1979", "date": (1979, 11, 11), "lat": 28.6667, "lon": 77.2167},
    {"id": "H5_reykjavik_1992", "date": (1992, 2, 29), "lat": 64.1466, "lon": -21.9426},
    {"id": "H6_quito_2010", "date": (2010, 7, 21), "lat": -0.1807, "lon": -78.4678},
    {"id": "H7_tokyo_2033", "date": (2033, 9, 3), "lat": 35.6762, "lon": 139.6503},
    {"id": "H8_mumbai_2077", "date": (2077, 12, 3), "lat": 19.0760, "lon": 72.8777},
    {"id": "H9_paris_2350", "date": (2350, 1, 15), "lat": 48.8566, "lon": 2.3522},
    {"id": "H10_boundary_moon_a", "date": (2025, 3, 1), "lat": 28.6667, "lon": 77.2167},
    {"id": "H11_boundary_moon_b", "date": (2025, 3, 2), "lat": 28.6667, "lon": 77.2167},
]

#: Frozen circumpolar holdout: proves the structured NO_RISE/NO_SET
#: path against real cases, not only against dates picked ad hoc in
#: the unit-test suite.
CIRCUMPOLAR_HOLDOUT = [
    {"id": "P1_svalbard_midnight_sun", "date": (2024, 6, 21), "lat": 78.2232, "lon": 15.6267, "expect": "no_set"},
    {"id": "P2_svalbard_polar_night", "date": (2024, 12, 21), "lat": 78.2232, "lon": 15.6267, "expect": "no_rise"},
]

#: Frozen elevation holdout, real-world locations at meaningful
#: altitude (not covered by the sea-level H1-H11 set).
ELEVATION_HOLDOUT = [
    {"id": "E1_la_paz_bolivia", "date": (2024, 3, 20), "lat": -16.5, "lon": -68.15, "elevation_m": 3640.0},
    {"id": "E2_dead_sea_shore", "date": (2024, 3, 20), "lat": 31.5, "lon": 35.5, "elevation_m": -430.0},
]

#: Derived, not tuned: see the module docstring. 60s comfortably
#: covers the H1-H11 worst case (24.8s, Reykjavik); 150s comfortably
#: covers the highest elevation holdout case.
_TOLERANCE_SECONDS_SEA_LEVEL = 60.0
_TOLERANCE_SECONDS_ELEVATED = 150.0

_STANDARD_REFRACTION_ARCMIN = 34.0


def _independent_altitude_minus_threshold(jd_ut, lat, lon, elevation_m):
    """
    Closed-form solar altitude above the ratified rise/set threshold.
    Independently coded: uses swe.calc_ut (position) and swe.sidtime
    (Greenwich sidereal time) only - never swe.rise_trans*.
    """
    pos, _ = swe.calc_ut(jd_ut, swe.SUN, swe.FLG_SWIEPH | swe.FLG_EQUATORIAL)
    ra, dec, dist = pos[0], pos[1], pos[2]
    # True (distance-dependent) solar semi-diameter: 959.63" at 1 AU
    # is the IAU-adopted photometric solar radius constant.
    semi_diameter_arcmin = (959.63 / dist) / 60.0
    threshold_arcmin = -(_STANDARD_REFRACTION_ARCMIN + semi_diameter_arcmin)

    gast_hours = swe.sidtime(jd_ut)
    lst_hours = (gast_hours + lon / 15.0) % 24.0
    hour_angle_deg = lst_hours * 15.0 - ra
    hour_angle_deg = ((hour_angle_deg + 180.0) % 360.0) - 180.0

    hour_angle = math.radians(hour_angle_deg)
    phi = math.radians(lat)
    delta = math.radians(dec)
    altitude = math.asin(
        math.sin(phi) * math.sin(delta)
        + math.cos(phi) * math.cos(delta) * math.cos(hour_angle)
    )
    threshold = math.radians(threshold_arcmin / 60.0 - horizon_dip_degrees(elevation_m))
    return math.degrees(altitude) - math.degrees(threshold)


def _independent_bisect(jd_lo, jd_hi, lat, lon, elevation_m, iterations=40):
    val_lo = _independent_altitude_minus_threshold(jd_lo, lat, lon, elevation_m)
    for _ in range(iterations):
        jd_mid = (jd_lo + jd_hi) / 2.0
        val_mid = _independent_altitude_minus_threshold(jd_mid, lat, lon, elevation_m)
        if (val_lo < 0) == (val_mid < 0):
            jd_lo, val_lo = jd_mid, val_mid
        else:
            jd_hi = jd_mid
    return (jd_lo + jd_hi) / 2.0


def independent_rise_set(jd_start, lat, lon, elevation_m, rising, step_days=1.0 / 288.0):
    """
    Independent reference: sample the closed-form altitude function
    every 5 minutes across one UT day, bisect the bracketing sign
    change. Returns None if no crossing in the requested direction is
    found (the circumpolar case), mirroring RiseSetStatus semantics
    without importing anything from engine.astronomy.rise_set.
    """
    prev_jd = jd_start
    prev_val = _independent_altitude_minus_threshold(prev_jd, lat, lon, elevation_m)
    steps = int(round(1.0 / step_days)) + 2
    for i in range(1, steps):
        jd = jd_start + i * step_days
        val = _independent_altitude_minus_threshold(jd, lat, lon, elevation_m)
        if rising and prev_val < 0 <= val:
            return _independent_bisect(prev_jd, jd, lat, lon, elevation_m)
        if not rising and prev_val >= 0 > val:
            return _independent_bisect(prev_jd, jd, lat, lon, elevation_m)
        prev_jd, prev_val = jd, val
    return None


def gate_a_convention_integrity():
    """Declared conventions actually reach the certified profiles/model."""

    for profile in (PARASHARI_LAHIRI, KP_KRISHNAMURTI):
        if profile.rise_set_disc_reference != RISE_SET_DISC_UPPER_LIMB:
            fail(f"{profile.name}: rise_set_disc_reference not upper_limb")
        if profile.rise_set_refraction != RISE_SET_REFRACTION_STANDARD:
            fail(f"{profile.name}: rise_set_refraction not standard_atmosphere")

    if BirthData.__dataclass_fields__["elevation_m"].default != 0.0:
        fail("BirthData.elevation_m default is not 0.0")

    # The unratified-convention guard must actually reject, not just exist.
    bad = replace(PARASHARI_LAHIRI, rise_set_disc_reference="center")
    try:
        sunrise(swe.julday(2024, 3, 20, 0), 0.0, 0.0, profile=bad)
        fail("unratified rise_set_disc_reference was not rejected")
    except UnsupportedRiseSetConventionError:
        pass

    return {
        "disc_reference": RISE_SET_DISC_UPPER_LIMB,
        "refraction": RISE_SET_REFRACTION_STANDARD,
        "profiles_checked": [PARASHARI_LAHIRI.name, KP_KRISHNAMURTI.name],
        "unratified_convention_rejected": True,
    }


def _compare_case(case_id, jd0, lat, lon, elevation_m, tolerance):
    mismatches = []
    comparisons = 0
    for event, fn, rising in (("rise", sunrise, True), ("set", sunset, False)):
        ours = fn(jd0, lat, lon, elevation_m=elevation_m)
        ref = independent_rise_set(jd0, lat, lon, elevation_m, rising)
        comparisons += 1
        if ours.status == RiseSetStatus.OK:
            if ref is None:
                mismatches.append(f"{case_id}/{event}: ours OK, reference found no crossing")
                continue
            delta_seconds = abs(ours.julian_day_ut - ref) * 86400.0
            if delta_seconds > tolerance:
                mismatches.append(
                    f"{case_id}/{event}: delta {delta_seconds:.3f}s exceeds tolerance {tolerance}s"
                )
        else:
            if ref is not None:
                mismatches.append(f"{case_id}/{event}: ours {ours.status.value}, reference found a crossing")
    return comparisons, mismatches


def gate_b_dense_sweep():
    """H1-H11 holdout, both events, engine vs. independent reference."""

    total_comparisons = 0
    all_mismatches = []
    for case in HOLDOUT:
        jd0 = swe.julday(*case["date"], 0.0)
        comparisons, mismatches = _compare_case(
            case["id"], jd0, case["lat"], case["lon"], 0.0, _TOLERANCE_SECONDS_SEA_LEVEL
        )
        total_comparisons += comparisons
        all_mismatches.extend(mismatches)
    if all_mismatches:
        fail(f"dense sweep mismatches: {all_mismatches}")
    return {"cases": len(HOLDOUT), "comparisons": total_comparisons, "mismatches": 0,
            "tolerance_seconds": _TOLERANCE_SECONDS_SEA_LEVEL}


def gate_c_independent_reference():
    """Circumpolar and elevation holdouts against the same closed-form reference."""

    circumpolar_checked = 0
    for case in CIRCUMPOLAR_HOLDOUT:
        jd0 = swe.julday(*case["date"], 0.0)
        rise_result = sunrise(jd0, case["lat"], case["lon"])
        set_result = sunset(jd0, case["lat"], case["lon"])
        expected = case["expect"]
        if expected == "no_set":
            if set_result.status != RiseSetStatus.NO_SET:
                fail(f"{case['id']}: expected NO_SET, got {set_result.status}")
        elif expected == "no_rise":
            if rise_result.status != RiseSetStatus.NO_RISE:
                fail(f"{case['id']}: expected NO_RISE, got {rise_result.status}")
        else:
            fail(f"{case['id']}: unknown expectation {expected}")
        circumpolar_checked += 1

    elevation_comparisons = 0
    elevation_mismatches = []
    for case in ELEVATION_HOLDOUT:
        jd0 = swe.julday(*case["date"], 0.0)
        comparisons, mismatches = _compare_case(
            case["id"], jd0, case["lat"], case["lon"], case["elevation_m"],
            _TOLERANCE_SECONDS_ELEVATED,
        )
        elevation_comparisons += comparisons
        elevation_mismatches.extend(mismatches)
    if elevation_mismatches:
        fail(f"elevation holdout mismatches: {elevation_mismatches}")

    return {
        "circumpolar_cases_checked": circumpolar_checked,
        "elevation_cases": len(ELEVATION_HOLDOUT),
        "elevation_comparisons": elevation_comparisons,
        "elevation_tolerance_seconds": _TOLERANCE_SECONDS_ELEVATED,
        "mismatches": 0,
        "reference_method": "closed-form hour-angle/altitude bisection, "
                             "independent of swe.rise_trans*",
    }


def gate_d_non_invasiveness():
    """Zero Tier-0 calculation impact from this addition."""

    if PARASHARI_LAHIRI.ayanamsa_mode != swe.SIDM_LAHIRI:
        fail("PARASHARI_LAHIRI.ayanamsa_mode changed")
    if KP_KRISHNAMURTI.ayanamsa_mode != swe.SIDM_KRISHNAMURTI:
        fail("KP_KRISHNAMURTI.ayanamsa_mode changed")
    if PARASHARI_LAHIRI.house_system != b"P" or KP_KRISHNAMURTI.house_system != b"P":
        fail("house_system changed")

    # Strict-mode ephemeris fallback guard must still actually guard.
    try:
        sunrise(swe.julday(3000, 1, 1, 0), 0.0, 0.0, strict=True)
        fail("strict-mode fallback guard did not raise for an out-of-range date")
    except EphemerisFallbackError:
        pass

    return {
        "ayanamsa_modes_unchanged": True,
        "house_systems_unchanged": True,
        "strict_fallback_guard_verified": True,
    }


def gate_e_validator():
    result = subprocess.run(
        [sys.executable, str(ROOT / "validate_rise_set_holdout.py")],
        capture_output=True, text=True)
    if result.returncode != 0 or "ALL INDEPENDENT RISE/SET CASES PASSED" not in result.stdout:
        fail(f"independent validator failed: {result.stdout}\n{result.stderr}")
    return {"result": "PASS"}


def main():
    tee = support.start_transcript()
    preconditions = support.preflight()
    report = {
        "schema": "rise_set_v1_certification",
        "adr": "ADR-0054",
        "date": str(date.today()),
        "scope": "Sunrise and sunset (Sun only), upper-limb disc, standard "
                 "atmospheric refraction, observer elevation (pressure and "
                 "geometric horizon dip), structured NO_RISE/NO_SET for "
                 "circumpolar days. FOUNDATION first work package.",
        "conventions": {
            "disc_reference": RISE_SET_DISC_UPPER_LIMB,
            "refraction": RISE_SET_REFRACTION_STANDARD,
            "standard_altitude_arcmin": -50,
            "elevation_dip_formula": "0.0293 * sqrt(elevation_m) degrees "
                                      "(Meeus, Astronomical Algorithms ch.15)",
        },
        "gates": {
            "A_convention_integrity": gate_a_convention_integrity(),
            "B_dense_sweep": gate_b_dense_sweep(),
            "C_independent_reference": gate_c_independent_reference(),
            "D_non_invasiveness": gate_d_non_invasiveness(),
            "E_independent_validator": gate_e_validator(),
        },
        "explicit_non_claims": [
            "bodies other than the Sun",
            "civil/nautical/astronomical twilight",
            "meridian transit (culmination) times",
            "polar-circle behaviour beyond NO_RISE/NO_SET classification "
            "(no partial-day or refraction-dependent-circumpolar edge case "
            "analysis)",
            "panchanga, vara, or any dependent capability",
            "any other varga, dasha, or certified layer; each requires its "
            "own ADR and certification",
        ],
        "environment": {"python": sys.version.split()[0]},
        "preconditions": preconditions,
        "result": "PASS",
    }
    out = support.emit(report, "RISE_SET_V1_certification.json", "rise_set", tee)
    print("=" * 60)
    print("RISE_SET_V1 CERTIFICATION")
    print("=" * 60)
    for name in ("A_convention_integrity", "B_dense_sweep", "C_independent_reference", "D_non_invasiveness"):
        print(f"{name}: {report['gates'][name]}")
    print("E_independent_validator: PASS")
    print("archived          :", out.relative_to(ROOT).as_posix())
    print("RESULT            : PASS")


if __name__ == "__main__":
    main()
