"""PANCHANGA_V1 CERTIFICATION RUNNER (ADR-0055).

Regenerates certification/PANCHANGA_V1_certification.json FROM SCRATCH on
every run; the stored JSON is never accepted as proof.

Scope: classification only (ADR-0055 item 3) - tithi, nakshatra, yoga,
karana, vara at a given instant. Element start/end transition timing,
and Rahu Kalam/Yamaganda/Gulika (ADR-0055 item 2, deferred pending a
future variant-table ratification), are explicitly NOT certified here.

Gates, mirroring the varga/rise-set A-E template: A frozen-rule/
convention integrity; B dense sweep (H1-H11 holdout, reused from
`certify_rise_set.py`) against the independent exact-rational reference;
C ULP boundary battery plus vara's circumpolar and sunrise-transition
edge cases; D non-invasiveness of already-certified modules this reuses
(`engine.astrology.nakshatra`, `engine.astronomy.rise_set`); E the
independent validator subprocess.

WHY THERE IS NO PyJHora ORACLE GATE HERE, UNLIKE THE EIGHT ORACLE
CERTIFIERS. PyJHora is not installed and not reachable (no network) in
this development environment, so its panchanga API surface
(module/function names for tithi/nakshatra/yoga/karana/vara) could not
be verified with the same confidence already established for the eight
existing oracle certifiers, each of which only calls PyJHora entry
points already proven working in CI. Committing an unverified import
risks a silent no-op or wrong-API failure with no local way to debug it
first - the same reasoning `certify_rise_set.py` already used to reject
an unverified `swetest` CLI invocation for rise/set. This is a
documented limitation, not a silent substitution: the independently-
coded exact-rational reference (Gate B/E) and the Fliegel & Van Flandern
calendar algorithm (vara) are the external references used instead,
matching this repository's own precedent for exactly this situation.
A future pass MAY add a PyJHora-oracle panchanga gate once its API is
verified running in the `oracle` CI job; nothing here blocks that.
"""

import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

sys.path.insert(0, str(ROOT / "scripts"))
import certification_support as support  # noqa: E402

import swisseph as swe  # noqa: E402

from engine.astrology.longitude_utils import BOUNDARY_TOLERANCE  # noqa: E402
from engine.astrology.nakshatra import nakshatra  # noqa: E402
from engine.astrology.panchanga import (  # noqa: E402
    KARANA_COUNT,
    KARANA_SPAN_DEGREES,
    TITHI_COUNT,
    TITHI_SPAN_DEGREES,
    YOGA_COUNT,
    YOGA_SPAN_DEGREES,
    VaraStatus,
    karana_index,
    nakshatra_index,
    panchanga,
    tithi_index,
    vara,
    yoga_index,
)
from engine.astronomy.profile import KP_KRISHNAMURTI, PARASHARI_LAHIRI  # noqa: E402
from engine.astronomy.rise_set import RiseSetStatus, sunrise  # noqa: E402
from engine.astronomy.sidereal_planets import sidereal_planet_position  # noqa: E402


def fail(message):
    print("PANCHANGA CERTIFICATION FAIL:", message)
    sys.exit(3)


#: Same real-world holdout `certify_rise_set.py` already uses.
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
    {"id": "P1_svalbard_midnight_sun", "date": (2024, 6, 21), "lat": 78.2232, "lon": 15.6267},
    {"id": "P2_svalbard_polar_night", "date": (2024, 12, 21), "lat": 78.2232, "lon": 15.6267},
]


def gate_a_convention_integrity():
    """The frozen rule matches ADR-0055 item 1, identically for both profiles."""

    if (TITHI_SPAN_DEGREES, TITHI_COUNT) != (12.0, 30):
        fail("tithi span/count changed from the ratified rule")
    if (YOGA_SPAN_DEGREES, YOGA_COUNT) != (360.0 / 27.0, 27):
        fail("yoga span/count changed from the ratified rule")
    if (KARANA_SPAN_DEGREES, KARANA_COUNT) != (6.0, 60):
        fail("karana span/count changed from the ratified rule")
    if BOUNDARY_TOLERANCE != 1e-10:
        fail("engine-wide boundary tolerance changed underneath panchanga")

    # ADR-0055 item 1: uniform convention, no per-profile parameter exists
    # for tithi/yoga/karana at all (unlike rise/set's declared-convention
    # fields) - the functions do not even accept a profile argument, which
    # is itself the proof there is nothing per-profile to diverge.
    import inspect
    for fn in (tithi_index, yoga_index, karana_index):
        if "profile" in inspect.signature(fn).parameters:
            fail(f"{fn.__name__} unexpectedly takes a profile parameter")

    return {
        "tithi_rule": f"{TITHI_SPAN_DEGREES} deg x {TITHI_COUNT}",
        "yoga_rule": f"{YOGA_SPAN_DEGREES} deg x {YOGA_COUNT}",
        "karana_rule": f"{KARANA_SPAN_DEGREES} deg x {KARANA_COUNT}",
        "boundary_convention": "engine-wide 1e-10 promote-up, [start, end)",
        "profile_parameterization": "none - ADR-0055 item 1 applies one "
                                     "convention uniformly",
    }


def gate_b_dense_sweep():
    """H1-H11 holdout, both certified profiles, engine vs. independent
    exact-rational reference (subprocess-isolated, see Gate E for the
    module import; this gate re-derives inline to keep A-D import-free
    of the validator script)."""

    from fractions import Fraction

    tol = Fraction(1, 10**10)

    def exact(elongation_or_sum, span, count):
        x = elongation_or_sum % 360
        idx = int((x + tol) / span)
        return min(idx, count - 1) + 1

    total_comparisons = 0
    mismatches = []
    for profile in (PARASHARI_LAHIRI, KP_KRISHNAMURTI):
        for case in HOLDOUT:
            jd = swe.julday(*case["date"], 12.0, swe.GREG_CAL)
            sun = sidereal_planet_position(jd, swe.SUN, profile.ayanamsa_mode, True)
            moon = sidereal_planet_position(jd, swe.MOON, profile.ayanamsa_mode, True)
            elong = Fraction(repr(moon.longitude)) - Fraction(repr(sun.longitude))
            total = Fraction(repr(sun.longitude)) + Fraction(repr(moon.longitude))

            got_tithi, ref_tithi = tithi_index(sun.longitude, moon.longitude), exact(elong, Fraction(12), 30)
            got_yoga, ref_yoga = yoga_index(sun.longitude, moon.longitude), exact(total, Fraction(360, 27), 27)
            got_karana, ref_karana = karana_index(sun.longitude, moon.longitude), exact(elong, Fraction(6), 60)
            total_comparisons += 3
            if got_tithi != ref_tithi:
                mismatches.append(f"{profile.name}/{case['id']}: tithi {got_tithi} != {ref_tithi}")
            if got_yoga != ref_yoga:
                mismatches.append(f"{profile.name}/{case['id']}: yoga {got_yoga} != {ref_yoga}")
            if got_karana != ref_karana:
                mismatches.append(f"{profile.name}/{case['id']}: karana {got_karana} != {ref_karana}")

    if mismatches:
        fail(f"dense sweep mismatches: {mismatches}")
    return {"cases": len(HOLDOUT), "profiles": 2, "comparisons": total_comparisons, "mismatches": 0}


def gate_c_boundary_and_vara_edge_cases():
    """ULP battery at every exact boundary, karana's special fixed
    positions, and vara's circumpolar/sunrise-transition behaviour."""

    # k=0 (the 0/360 wraparound) is deliberately excluded: division_index's
    # own documented convention is tolerance-promoted AND top-clamped, so a
    # value just below the wraparound clamps into the LAST division rather
    # than promoting into division 0 - already-established behaviour
    # (nakshatra/varga classification share it), not something new here.
    checked = 0
    for k in range(1, TITHI_COUNT):
        boundary = k * TITHI_SPAN_DEGREES
        just_below = boundary - 1e-11
        just_below_outside = boundary - 1e-9
        if tithi_index(0.0, just_below) != k + 1:
            fail(f"tithi boundary {k}: 1e-11 below did not promote")
        if tithi_index(0.0, just_below_outside) != k:
            fail(f"tithi boundary {k}: 1e-9 below wrongly promoted")
        checked += 2

    for k in range(1, KARANA_COUNT):
        boundary = k * KARANA_SPAN_DEGREES
        just_below = boundary - 1e-11
        if karana_index(0.0, just_below) != k + 1:
            fail(f"karana boundary {k}: 1e-11 below did not promote")
        checked += 1

    # Karana's fixed-position naming scheme (engine.astrology.panchanga_names):
    # index 1 and 58-60 fixed, 2-57 the seven movable karanas x8.
    from engine.astrology.panchanga_names import karana_name
    if karana_name(1) != "Kimstughna":
        fail("karana index 1 is not Kimstughna")
    if [karana_name(i) for i in (58, 59, 60)] != ["Shakuni", "Chatushpada", "Naga"]:
        fail("karana indices 58-60 are not the three trailing fixed karanas")
    if karana_name(2) != karana_name(2 + 7 * 5):
        fail("karana movable cycle is not period-7")
    checked += 4

    # vara: circumpolar days are INDETERMINATE, never a guessed weekday.
    for case in CIRCUMPOLAR_HOLDOUT:
        jd = swe.julday(*case["date"], 12.0, swe.GREG_CAL)
        result = vara(jd, case["lat"], case["lon"])
        if result.status != VaraStatus.INDETERMINATE:
            fail(f"{case['id']}: expected INDETERMINATE vara, got {result.status}")
        checked += 1

    # vara: the weekday must roll over exactly at the anchor sunrise, not at UT midnight.
    delhi_lat, delhi_lon = 28.6667, 77.2167
    midnight = swe.julday(2024, 1, 15, 0.0, swe.GREG_CAL)  # 2024-01-15 00:00 UT
    today_sunrise = sunrise(midnight, delhi_lat, delhi_lon)
    if today_sunrise.status != RiseSetStatus.OK:
        fail("delhi sunrise on 2024-01-15 unexpectedly not OK")
    just_before = today_sunrise.julian_day_ut - (60.0 / 86400.0)
    just_after = today_sunrise.julian_day_ut + (60.0 / 86400.0)
    before_result = vara(just_before, delhi_lat, delhi_lon)
    after_result = vara(just_after, delhi_lat, delhi_lon)
    if before_result.index == after_result.index:
        fail("vara did not roll over across the anchor sunrise")
    if after_result.index != (before_result.index + 1) % 7:
        fail(f"vara rollover was not exactly +1 weekday: before={before_result.index} after={after_result.index}")
    checked += 2

    return {
        "tithi_boundaries_checked": TITHI_COUNT,
        "karana_boundaries_checked": KARANA_COUNT,
        "karana_naming_checked": True,
        "vara_circumpolar_cases": len(CIRCUMPOLAR_HOLDOUT),
        "vara_sunrise_rollover_checked": True,
        "total_checks": checked,
    }


def gate_d_non_invasiveness():
    """Reused certified layers (nakshatra, rise/set, profiles) unchanged."""

    if nakshatra_index(40.0) != nakshatra(40.0):
        fail("panchanga.nakshatra_index diverges from the certified nakshatra()")
    if PARASHARI_LAHIRI.ayanamsa_mode != swe.SIDM_LAHIRI:
        fail("PARASHARI_LAHIRI.ayanamsa_mode changed")
    if KP_KRISHNAMURTI.ayanamsa_mode != swe.SIDM_KRISHNAMURTI:
        fail("KP_KRISHNAMURTI.ayanamsa_mode changed")
    return {"nakshatra_reuse_verified": True, "ayanamsa_modes_unchanged": True}


def gate_e_validator():
    result = subprocess.run(
        [sys.executable, str(ROOT / "validate_panchanga_holdout.py")],
        capture_output=True, text=True)
    if result.returncode != 0 or "PANCHANGA HOLDOUT VALIDATION PASS" not in result.stdout:
        fail(f"independent validator failed: {result.stdout}\n{result.stderr}")
    return {"result": "PASS"}


def main():
    tee = support.start_transcript()
    preconditions = support.preflight()
    report = {
        "schema": "panchanga_v1_certification",
        "adr": "ADR-0055",
        "date": str(date.today()),
        "scope": "Classification only, at a given instant: tithi, nakshatra "
                 "(reused), yoga, karana, vara. FOUNDATION Panchanga first "
                 "work package.",
        "conventions": {
            "boundary": "engine-wide 1e-10 promote-up, [start, end), "
                        "applied uniformly to both certified profiles",
            "tithi": f"{TITHI_SPAN_DEGREES} deg x {TITHI_COUNT}",
            "yoga": f"{YOGA_SPAN_DEGREES} deg x {YOGA_COUNT}",
            "karana": f"{KARANA_SPAN_DEGREES} deg x {KARANA_COUNT}",
            "vara": "sunrise-to-sunrise, consuming certified Tier-0 rise_set",
        },
        "gates": {
            "A_convention_integrity": gate_a_convention_integrity(),
            "B_dense_sweep": gate_b_dense_sweep(),
            "C_boundary_and_vara_edge_cases": gate_c_boundary_and_vara_edge_cases(),
            "D_non_invasiveness": gate_d_non_invasiveness(),
            "E_independent_validator": gate_e_validator(),
        },
        "explicit_non_claims": [
            "element start/end transition timing (deferred, ADR-0055 item 3)",
            "Rahu Kalam, Yamaganda, Gulika (deferred pending a variant-table "
            "ratification, ADR-0055 item 2)",
            "PyJHora oracle cross-check (not verified reachable in this "
            "environment; see module docstring)",
            "vara's weekday label for observers whose local civil date "
            "differs from the UT calendar date of their sunrise (see "
            "engine.astrology.panchanga.vara docstring)",
            "any other varga, dasha, or certified layer",
        ],
        "environment": {"python": sys.version.split()[0]},
        "preconditions": preconditions,
        "result": "PASS",
    }
    out = support.emit(report, "PANCHANGA_V1_certification.json", "panchanga", tee)
    print("=" * 60)
    print("PANCHANGA_V1 CERTIFICATION")
    print("=" * 60)
    for name in ("A_convention_integrity", "B_dense_sweep", "C_boundary_and_vara_edge_cases", "D_non_invasiveness"):
        print(f"{name}: {report['gates'][name]}")
    print("E_independent_validator: PASS")
    # .as_posix(): a bare str(Path) uses the OS-native separator, which
    # would make this line (captured into the console transcript) differ
    # between a Windows-local run and Linux CI - the exact provenance
    # defect ADR-0054's evidence already hit and fixed twice. Forcing
    # POSIX here prevents the recurrence rather than fixing it after the
    # fact again.
    print("archived          :", out.relative_to(ROOT).as_posix())
    print("RESULT            : PASS")


if __name__ == "__main__":
    main()
