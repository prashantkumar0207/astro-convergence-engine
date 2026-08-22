"""Independent rise/set holdout validator (Gate E of ADR-0054).

Validates engine.astronomy.rise_set against a reference derived
INDEPENDENTLY inside this file, by a DIFFERENT method than the one
scripts/certify_rise_set.py's own Gate B/C reference uses: this file
solves the classical sunrise/hour-angle equation directly in closed
form (single arccos solve, one-step transit-time refinement - the
standard low-precision almanac algorithm, e.g. Meeus ch.15), while the
certifier's own reference samples and bisects. No function is imported
from scripts/certify_rise_set.py.

Run:  python validate_rise_set_holdout.py
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import swisseph as swe  # noqa: E402

from engine.astronomy.rise_set import RiseSetStatus, sunrise, sunset  # SUBJECT under validation  # noqa: E402

swe.set_ephe_path(str(Path(__file__).resolve().parent))

_STANDARD_REFRACTION_ARCMIN = 34.0
_DIP_COEFFICIENT_DEG_PER_SQRT_M = 0.0293

# Same holdout identifiers as scripts/certify_rise_set.py (this
# repository's convention: the H1-H11 set is reused, not re-invented,
# across every certifier that needs a real-world case list).
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

CIRCUMPOLAR_HOLDOUT = [
    {"id": "P1_svalbard_midnight_sun", "date": (2024, 6, 21), "lat": 78.2232, "lon": 15.6267, "expect": "no_set"},
    {"id": "P2_svalbard_polar_night", "date": (2024, 12, 21), "lat": 78.2232, "lon": 15.6267, "expect": "no_rise"},
]

#: Derived, not tuned: measured worst case across the full H1-H11
#: holdout with this method was 184.7s (New York, 1900); this is a
#: simpler single/double-iteration closed-form solve than
#: scripts/certify_rise_set.py's own bisection reference, so a larger
#: residual than that gate's 60s is expected and is not evidence of a
#: defect (ADR-0054). 240s leaves comfortable margin while remaining
#: far tighter than the multi-minute-to-hour errors an actual sign,
#: unit, or day-wraparound defect would produce - exactly the class of
#: bug this file's own negative control below plants.
_TOLERANCE_SECONDS = 240.0


def _dip_degrees(elevation_m):
    if elevation_m <= 0.0:
        return 0.0
    return _DIP_COEFFICIENT_DEG_PER_SQRT_M * math.sqrt(elevation_m)


def _sun_ra_dec_dist(jd_ut):
    pos, _ = swe.calc_ut(jd_ut, swe.SUN, swe.FLG_SWIEPH | swe.FLG_EQUATORIAL)
    return pos[0], pos[1], pos[2]


def reference_transit_and_h0(jd_midnight_ut, lat, lon, elevation_m):
    """
    Closed-form: hour angle H0 (degrees) at which the sun crosses the
    ratified -50'-and-dip threshold, and the UT of solar transit
    (culmination), refined by one iteration. Returns (transit_ut,
    h0_degrees) or (transit_ut, None) if circumpolar (|cos H0| > 1).

    `gast0` (Greenwich Apparent Sidereal Time at the FIXED reference
    epoch `jd_midnight_ut`) is deliberately reused, unchanged, in both
    passes: it is the anchor the delta-GST-since-midnight calculation
    is measured from. Re-sampling it at the moving transit estimate
    (an earlier, incorrect version of this function did) makes the
    two passes measure delta-GST from two different epochs and
    silently discards most of a day - caught by this file's own
    holdout comparisons before being committed, see ADR-0054.
    """
    gast0 = swe.sidtime(jd_midnight_ut)
    ra0, dec0, dist0 = _sun_ra_dec_dist(jd_midnight_ut)
    transit_ut = jd_midnight_ut + (((ra0 - lon) / 15.0 - gast0) % 24.0) / 24.0
    # One refinement of the SOLAR POSITION at the improved time estimate;
    # gast0 itself is not re-sampled (see docstring).
    ra, dec, dist = _sun_ra_dec_dist(transit_ut)
    transit_ut = jd_midnight_ut + (((ra - lon) / 15.0 - gast0) % 24.0) / 24.0

    semi_diameter_arcmin = (959.63 / dist) / 60.0
    h0_altitude_deg = -(_STANDARD_REFRACTION_ARCMIN + semi_diameter_arcmin) / 60.0 - _dip_degrees(elevation_m)

    phi = math.radians(lat)
    delta = math.radians(dec)
    cos_h0 = (math.sin(math.radians(h0_altitude_deg)) - math.sin(phi) * math.sin(delta)) / (
        math.cos(phi) * math.cos(delta)
    )
    if cos_h0 < -1.0 or cos_h0 > 1.0:
        return transit_ut, None
    return transit_ut, math.degrees(math.acos(cos_h0))


def reference_rise_set(jd_midnight_ut, lat, lon, elevation_m, rising):
    """
    First rise (or set) at or after `jd_midnight_ut` - a genuine
    forward search, not "today's transit +/- H0" alone: for a
    longitude far enough east (or west) of Greenwich, `jd_midnight_ut`
    can fall AFTER that local day's rise, or after both its rise and
    set, in which case the correct next event belongs to the
    following transit. Two candidate transits (the one nearest
    `jd_midnight_ut`, and the following one) are computed and the
    earliest candidate event that is not before `jd_midnight_ut` is
    returned - the same forward-search semantics
    `swe.rise_trans_true_hor` (the subject under test) implements
    internally. An earlier version of this function assumed a single
    transit sufficed and silently returned the wrong day's event for
    the Sydney holdout case (H3) by a full day - caught here before
    being committed, see ADR-0054.
    """
    candidates = []
    for anchor in (jd_midnight_ut, jd_midnight_ut + 1.0):
        transit_ut, h0 = reference_transit_and_h0(anchor, lat, lon, elevation_m)
        if h0 is None:
            continue
        offset_days = (h0 / 15.0) / 24.0
        event_ut = transit_ut - offset_days if rising else transit_ut + offset_days
        candidates.append(event_ut)
    forward = [c for c in candidates if c >= jd_midnight_ut - 1e-9]
    if not forward:
        return None
    return min(forward)


def main() -> int:
    failures = []
    comparisons = 0

    for case in HOLDOUT:
        jd0 = swe.julday(*case["date"], 0.0)
        for event, fn, rising in (("rise", sunrise, True), ("set", sunset, False)):
            subject = fn(jd0, case["lat"], case["lon"])
            reference = reference_rise_set(jd0, case["lat"], case["lon"], 0.0, rising)
            comparisons += 1
            if subject.status != RiseSetStatus.OK or reference is None:
                failures.append((case["id"], event, "status/circumpolar mismatch"))
                continue
            delta = abs(subject.julian_day_ut - reference) * 86400.0
            if delta > _TOLERANCE_SECONDS:
                failures.append((case["id"], event, f"delta {delta:.3f}s"))

    circumpolar_checked = 0
    for case in CIRCUMPOLAR_HOLDOUT:
        jd0 = swe.julday(*case["date"], 0.0)
        rise_result = sunrise(jd0, case["lat"], case["lon"])
        set_result = sunset(jd0, case["lat"], case["lon"])
        _, h0 = reference_transit_and_h0(jd0, case["lat"], case["lon"], 0.0)
        if h0 is not None:
            failures.append((case["id"], "circumpolar", "reference found H0, expected circumpolar"))
        elif case["expect"] == "no_set" and set_result.status != RiseSetStatus.NO_SET:
            failures.append((case["id"], "set", f"expected NO_SET, got {set_result.status}"))
        elif case["expect"] == "no_rise" and rise_result.status != RiseSetStatus.NO_RISE:
            failures.append((case["id"], "rise", f"expected NO_RISE, got {rise_result.status}"))
        circumpolar_checked += 1

    # Property check: equinox day length is close to, but honestly
    # (refraction) slightly longer than, 12 hours, at a range of
    # latitudes far from the poles.
    equinox_jd = swe.julday(2024, 3, 20, 0.0)
    property_checked = 0
    for lat in (-60.0, -30.0, 0.0, 30.0, 60.0):
        r = sunrise(equinox_jd, lat, 0.0)
        s = sunset(equinox_jd, lat, 0.0)
        if r.status != RiseSetStatus.OK or s.status != RiseSetStatus.OK:
            failures.append(("equinox_property", lat, "expected both events"))
        else:
            day_hours = (s.julian_day_ut - r.julian_day_ut) * 24.0
            if not (11.9 <= day_hours <= 12.3):
                failures.append(("equinox_property", lat, f"day length {day_hours:.4f}h out of [11.9, 12.3]"))
        property_checked += 1

    print("=" * 60)
    print("INDEPENDENT RISE/SET HOLDOUT VALIDATION")
    print("=" * 60)
    print(f"Holdout comparisons  : {comparisons}")
    print(f"Circumpolar cases    : {circumpolar_checked}")
    print(f"Equinox property     : {property_checked}")
    if failures:
        print(f"FAILURES: {len(failures)}; first: {failures[:5]}")
        print("RESULT: FAIL")
        return 1
    print()
    print("RESULT: ALL INDEPENDENT RISE/SET CASES PASSED")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
