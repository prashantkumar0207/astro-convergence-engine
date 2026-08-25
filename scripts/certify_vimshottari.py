"""VIMSHOTTARI_V1 CERTIFICATION RUNNER (ADR-0007).

Regenerates certification/VIMSHOTTARI_V1_certification.json FROM
SCRATCH on every run; the stored JSON is never accepted as proof.

Oracle methodology (D-001/D-007 compliant): PyJHora is the external
oracle for the TIMELINE MATHEMATICS. Its Moon longitude differs from
this engine's swetest-certified Moon by up to ~1-2 arcsec (recorded
below per case); per D-001 swetest remains the numerical authority
and per D-007 an external app's numerical difference does not reopen
Tier-0. The oracle gate therefore injects PYJHORA'S OWN Moon into
this engine's timeline and requires the full dasha-bhukti structure
to match: identical lord sequences (zero categorical tolerance) and
period start instants within 1e-5 day (~0.86 s, float round-trip
allowance).

Requires PyJHora (oracle-only dependency, never imported by
production code). Exit 0 = PASS, 3 = FAIL.
"""

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

sys.path.insert(0, str(ROOT / "scripts"))
import certification_support as support  # noqa: E402

import swisseph as swe  # noqa: E402

from engine.astronomy.profile import KP_KRISHNAMURTI, PARASHARI_LAHIRI  # noqa: E402
from engine.calculations.calculations import calculate  # noqa: E402
from engine.dasha import tables as dasha_tables  # noqa: E402
from engine.dasha.profile import VIMSHOTTARI_MEAN_SIDEREAL_YEAR  # noqa: E402
from engine.dasha.vimshottari import vimshottari_from_moon  # noqa: E402
from engine.models.birth_data import BirthData  # noqa: E402

try:
    from jhora import const as jhora_const
    from jhora import utils as jhora_utils
    from jhora.panchanga import drik
    import jhora.horoscope.dhasa.graha.vimsottari as jhora_vim
    import importlib.metadata
    PYJHORA_VERSION = importlib.metadata.version("PyJHora")
except Exception as error:  # pragma: no cover
    print("KP CERTIFICATION FAIL: PyJHora oracle unavailable:", error)
    sys.exit(3)

HOLDOUT = [
 {"id": "H1_london_1823",     "date": (1823, 4, 17), "time": (3, 21, 7),  "lat": 51.5074,  "lon": -0.1278},
 {"id": "H2_newyork_1900",    "date": (1900, 1, 1),  "time": (0, 0, 0),   "lat": 40.7128,  "lon": -74.0060},
 {"id": "H3_sydney_1946",     "date": (1946, 6, 14), "time": (21, 47, 53), "lat": -33.8688, "lon": 151.2093},
 {"id": "H4_delhi_1979",      "date": (1979, 11, 11), "time": (17, 41, 37), "lat": 28.6667, "lon": 77.2167},
 {"id": "H5_reykjavik_1992",  "date": (1992, 2, 29), "time": (23, 59, 59), "lat": 64.1466, "lon": -21.9426},
 {"id": "H6_quito_2010",      "date": (2010, 7, 21), "time": (5, 5, 5),   "lat": -0.1807,  "lon": -78.4678},
 {"id": "H7_tokyo_2033",      "date": (2033, 9, 3),  "time": (11, 11, 11), "lat": 35.6762, "lon": 139.6503},
 {"id": "H8_mumbai_2077",     "date": (2077, 12, 3), "time": (14, 30, 27), "lat": 19.0760, "lon": 72.8777},
 {"id": "H9_paris_2350",      "date": (2350, 1, 15), "time": (6, 6, 6),   "lat": 48.8566,  "lon": 2.3522},
 # H10/H11 (M-02, ADR-0072): ordinary cases, corrected from their original
 # "boundary_moon" names - measured this session at 6.4587 and 5.0197
 # degrees from the nearest nakshatra boundary respectively, farther than
 # most of this holdout's own ordinary cases. Birth data unchanged; only
 # the misleading label is corrected. Kept as valid, already-oracle-
 # verified ordinary coverage rather than discarded.
 {"id": "H10_delhi_2025a", "date": (2025, 3, 1), "time": (16, 21, 0), "lat": 28.6667, "lon": 77.2167},
 {"id": "H11_delhi_2025b", "date": (2025, 3, 2), "time": (11, 38, 0), "lat": 28.6667, "lon": 77.2167},
]

#: M-02 (ADR-0072): genuine near-boundary Moon cases, root-found via the
#: already-certified engine.transits.crossing.find_crossings() (TRANSIT_V1,
#: ADR-0008) rather than picked by hand - each triple locates a real
#: nakshatra-boundary crossing under its own tagged "profile", then samples
#: 5 minutes before and after it, so the holdout actually exercises a
#: nakshatra-lord change across a genuine boundary, not merely a birth
#: chart that happens to exist. Each case runs ONLY under its own native
#: profile, not both like the ordinary HOLDOUT above: a case root-found
#: near a boundary under one ayanamsa is not, in general, still near a
#: boundary under a different ayanamsa (Lahiri and Krishnamurti differ by
#: a small but non-trivial constant offset) - running it under the other
#: profile would silently test an ordinary case while claiming boundary
#: coverage. Distinct from the ordinary H1-H11 cases by the "B" prefix and
#: by NEAR_BOUNDARY_CASE_IDS below - this distinction is preserved
#: deliberately (DP-019 Option 1 item 3), not merged into the ordinary set.
BOUNDARY_HOLDOUT = [
 {"id": "B1_lahiri_boundary_before", "date": (2025, 1, 16), "time": (5, 41, 41.52955502271652), "lat": 28.6667, "lon": 77.2167, "profile": "parashari_lahiri"},
 {"id": "B2_lahiri_boundary_at",     "date": (2025, 1, 16), "time": (5, 46, 41.52953714132309), "lat": 28.6667, "lon": 77.2167, "profile": "parashari_lahiri"},
 {"id": "B3_lahiri_boundary_after",  "date": (2025, 1, 16), "time": (5, 51, 41.52951925992966), "lat": 28.6667, "lon": 77.2167, "profile": "parashari_lahiri"},
 {"id": "B4_kp_boundary_before",     "date": (2025, 1, 26), "time": (2, 40, 21.100781857967377), "lat": 28.6667, "lon": 77.2167, "profile": "kp_krishnamurti"},
 {"id": "B5_kp_boundary_at",         "date": (2025, 1, 26), "time": (2, 45, 21.100763976573944), "lat": 28.6667, "lon": 77.2167, "profile": "kp_krishnamurti"},
 {"id": "B6_kp_boundary_after",      "date": (2025, 1, 26), "time": (2, 50, 21.10074609518051),  "lat": 28.6667, "lon": 77.2167, "profile": "kp_krishnamurti"},
]

NEAR_BOUNDARY_CASE_IDS = frozenset(case["id"] for case in BOUNDARY_HOLDOUT)

#: Two orders of magnitude tighter than the 5-6 degree distance the M-02
#: audit finding measured for the mislabeled H10/H11 cases this replaces -
#: a case tagged NEAR_BOUNDARY_CASE_IDS must fall within this to count as
#: genuinely exercising boundary-adjacent behaviour.
NEAR_BOUNDARY_THRESHOLD_DEG = 0.1

#: pyjhora planet index -> project lord abbreviation.
PYJHORA_LORD = {0: "Su", 1: "Mo", 2: "Ma", 3: "Me", 4: "Ju", 5: "Ve",
                6: "Sa", 7: "Ra", 8: "Ke"}

PROFILES = [
    ("parashari_lahiri", PARASHARI_LAHIRI, "LAHIRI"),
    ("kp_krishnamurti", KP_KRISHNAMURTI, "KP"),
]

START_TOLERANCE_DAYS = 1e-5


def fail(message):
    print("VIMSHOTTARI CERTIFICATION FAIL:", message)
    sys.exit(3)


def run_case(case, engine_profile, jhora_ayanamsa):
    year, month, day = case["date"]
    hour, minute, second = case["time"]

    # Engine Moon (swetest-certified astronomy), for the delta record.
    snapshot = calculate(
        BirthData(year, month, day, hour, minute, float(second),
                  case["lat"], case["lon"], "UTC"),
        profile=engine_profile,
    ).snapshot
    our_moon = snapshot.sidereal_planets["Moon"].longitude
    jd_utc = snapshot.julian_day

    # Oracle, configured to the same instant (tz 0), ayanamsa, and the
    # pinned MEAN_SIDEREAL_YEAR convention (Decision DA-A).
    drik.set_ayanamsa_mode(jhora_ayanamsa)
    place = drik.Place(case["id"], case["lat"], case["lon"], 0.0)
    jd_local = jhora_utils.julian_day_number(case["date"], case["time"])
    oracle_moon = drik.sidereal_longitude(jd_utc, jhora_const._MOON)
    moon_delta_arcsec = abs(((oracle_moon - our_moon + 180.0) % 360.0) - 180.0) * 3600.0

    _, bhukthis = jhora_vim.get_vimsottari_dhasa_bhukthi(
        jd_local, place,
        dhasa_duration_type=jhora_const.DHASA_YEAR_DURATION.MEAN_SIDEREAL_YEAR,
        dhasa_level_index=jhora_const.MAHA_DHASA_DEPTH.PRATYANTARA,
    )

    # Inject the ORACLE'S Moon into OUR timeline mathematics.
    timeline = vimshottari_from_moon(
        oracle_moon, jd_utc,
        dasha_profile=VIMSHOTTARI_MEAN_SIDEREAL_YEAR, depth=3,
    )
    ours = timeline.pratyantardashas()

    if len(bhukthis) != len(ours) or len(ours) != 729:
        fail(f"{case['id']}: row count {len(bhukthis)} vs {len(ours)}")

    max_start_delta = 0.0
    for our_period, oracle_row in zip(ours, bhukthis):
        (md_index, ad_index, pd_index), (oy, om, od, ohours), _duration = oracle_row
        oracle_lords = (
            PYJHORA_LORD[md_index], PYJHORA_LORD[ad_index], PYJHORA_LORD[pd_index],
        )
        if our_period.lords != oracle_lords:
            fail(f"{case['id']}: lords {our_period.lords} vs {oracle_lords}")
        oracle_jd = swe.julday(oy, om, od, ohours, swe.GREG_CAL)
        delta = abs(our_period.start_jd - oracle_jd)
        max_start_delta = max(max_start_delta, delta)
    if max_start_delta > START_TOLERANCE_DAYS:
        fail(f"{case['id']}: start delta {max_start_delta} d > {START_TOLERANCE_DAYS}")

    within = oracle_moon % dasha_tables.NAK_SPAN
    boundary_distance_deg = min(within, dasha_tables.NAK_SPAN - within)

    if case["id"] in NEAR_BOUNDARY_CASE_IDS and boundary_distance_deg > NEAR_BOUNDARY_THRESHOLD_DEG:
        fail(
            f"{case['id']}: {boundary_distance_deg} deg from the nearest nakshatra "
            f"boundary, exceeds NEAR_BOUNDARY_THRESHOLD_DEG={NEAR_BOUNDARY_THRESHOLD_DEG} "
            "- this case no longer genuinely exercises boundary-adjacent behaviour "
            "(the exact defect M-02/ADR-0072 corrected)"
        )

    # Dasha roadmap step 6 (DP-020 Option 1, ADR-0073): the new
    # VimshottariTimeline.seed_nakshatra_boundary_arcsec field must agree
    # with an INDEPENDENTLY measured distance (the same certifier-side
    # quantity M-02 already computes above, not the field's own formula)
    # to within float round-trip noise - a genuine gate, not a tautology.
    boundary_arcsec_delta = abs(timeline.seed_nakshatra_boundary_arcsec - float(boundary_distance_deg * 3600))
    if boundary_arcsec_delta > 1e-3:
        fail(
            f"{case['id']}: seed_nakshatra_boundary_arcsec "
            f"{timeline.seed_nakshatra_boundary_arcsec} disagrees with the independently "
            f"measured {float(boundary_distance_deg * 3600)} arcsec by {boundary_arcsec_delta} "
            "- DP-020/ADR-0073's own re-expression claim would be false"
        )

    return {
        "case": case["id"],
        "moon_delta_vs_oracle_arcsec": round(moon_delta_arcsec, 6),
        "pratyantar_rows": len(ours),
        "lord_mismatches": 0,
        "max_start_delta_days": max_start_delta,
        "moon_distance_to_nearest_boundary_deg": round(boundary_distance_deg, 6),
        "seed_nakshatra_boundary_arcsec": round(timeline.seed_nakshatra_boundary_arcsec, 6),
    }


def main():
    tee = support.start_transcript()
    preconditions = support.preflight()
    per_profile = {}
    total_rows = 0
    worst_start = 0.0
    worst_moon = 0.0
    for profile_name, engine_profile, jhora_ayanamsa in PROFILES:
        ordinary_cases = [run_case(case, engine_profile, jhora_ayanamsa) for case in HOLDOUT]
        boundary_cases = [
            run_case(case, engine_profile, jhora_ayanamsa)
            for case in BOUNDARY_HOLDOUT
            if case["profile"] == profile_name
        ]
        cases = ordinary_cases + boundary_cases
        per_profile[profile_name] = cases
        total_rows += sum(c["pratyantar_rows"] for c in cases)
        worst_start = max(worst_start, max(c["max_start_delta_days"] for c in cases))
        worst_moon = max(worst_moon, max(c["moon_delta_vs_oracle_arcsec"] for c in cases))

    #: M-02 (ADR-0072): a distinct, self-documenting summary of the genuine
    #: near-boundary cases - separate from the per-case detail already in
    #: `gates.cases`, so a reader (or an auditor) does not have to filter
    #: eleven-plus ordinary cases to confirm boundary coverage exists.
    near_boundary_coverage = [
        {
            "case": c["case"],
            "profile": profile_name,
            "moon_distance_to_nearest_boundary_deg": c["moon_distance_to_nearest_boundary_deg"],
            "lord_mismatches": c["lord_mismatches"],
        }
        for profile_name, cases in per_profile.items()
        for c in cases
        if c["case"] in NEAR_BOUNDARY_CASE_IDS
    ]
    if len(near_boundary_coverage) != len(NEAR_BOUNDARY_CASE_IDS):
        fail("near-boundary coverage count mismatch - a boundary case is missing from its native profile run")

    import subprocess
    validator = subprocess.run(
        [sys.executable, str(ROOT / "validate_vimshottari_holdout.py")],
        capture_output=True, text=True)
    if validator.returncode != 0 or "ALL INDEPENDENT VIMSHOTTARI CASES PASSED" not in validator.stdout:
        fail("independent validator failed")

    report = {
        "schema": "vimshottari_v1_certification",
        "adr": "ADR-0007",
        "date": str(date.today()),
        "scope": "Vimshottari maha/antar/pratyantar timelines, school-explicit seeding",
        "year_convention": {
            "profile": VIMSHOTTARI_MEAN_SIDEREAL_YEAR.name,
            "days": str(VIMSHOTTARI_MEAN_SIDEREAL_YEAR.year_length_days),
            "source": VIMSHOTTARI_MEAN_SIDEREAL_YEAR.source,
        },
        "oracle": {
            "package": "PyJHora",
            "version": PYJHORA_VERSION,
            "methodology": (
                "Oracle's own Moon injected into engine timeline (isolates "
                "timeline mathematics per D-007); engine Moon remains "
                "swetest-certified per D-001. Moon deltas recorded per case."
            ),
            "max_oracle_moon_delta_arcsec": worst_moon,
        },
        "gates": {
            "oracle_pratyantar_rows_compared": total_rows,
            "oracle_lord_mismatches": 0,
            "oracle_max_start_delta_days": worst_start,
            "start_tolerance_days": START_TOLERANCE_DAYS,
            "independent_validator": "PASS",
            "cases": per_profile,
            "near_boundary_coverage": {
                "methodology": (
                    "Cases root-found via engine.transits.crossing.find_crossings() "
                    "(TRANSIT_V1, ADR-0008), sampled at the exact crossing and 5 "
                    "minutes before/after, so the mahadasha lord genuinely changes "
                    "across the boundary. Closes M-02 (ADR-0072): the previously "
                    "named boundary cases (H10/H11) were 6.46 and 5.02 degrees from "
                    "the nearest boundary, farther than most of this holdout's own "
                    "ordinary cases - both corrected and kept as ordinary coverage."
                ),
                "threshold_deg": NEAR_BOUNDARY_THRESHOLD_DEG,
                "cases": near_boundary_coverage,
            },
            "boundary_proximity_indicator": {
                "methodology": (
                    "VimshottariTimeline.seed_nakshatra_boundary_arcsec (Dasha "
                    "roadmap step 6, DP-020 Option 1, ADR-0073) is an exact "
                    "re-expression of seed_elapsed_fraction, no new astronomical "
                    "calculation. Verified per case above (each case's own "
                    "seed_nakshatra_boundary_arcsec is checked against an "
                    "independently measured distance, not the field's own "
                    "formula; see run_case()). Hermetic pinning tests and a "
                    "genuine negative control: engine/tests/"
                    "test_vimshottari_boundary_proximity_indicator.py."
                ),
                "scope": (
                    "Nakshatra (seed) boundary only - does not cover deeper "
                    "period-transition boundaries or any KP-specific level, "
                    "and is not a dasha-date-uncertainty figure (that is "
                    "DP-020 Option 2, not chosen)."
                ),
            },
        },
        "explicit_non_claims": [
            "other dasha systems (Ashtottari, Yogini, ...)",
            "depths beyond pratyantardasha (DA-C)",
            "year conventions other than the certified profile",
            "transit or event overlays",
            (
                "agreement with engine.astrology.nakshatra's tolerance-promoted "
                "classifier at a boundary: seed classification uses the KP "
                "layer's exact [start, end) rule for every school, including "
                "Parashari - a deliberate, ratified convention (H-08, ADR-0071), "
                "not a defect. See VimshottariTimeline.seed_boundary_convention "
                "and engine/tests/test_vimshottari_h08_boundary_convention.py."
            ),
            (
                "any distance-to-boundary claim beyond the nakshatra (seed) "
                "level: seed_nakshatra_boundary_arcsec (Dasha roadmap step 6, "
                "DP-020 Option 1, ADR-0073) does not cover antardasha/"
                "pratyantardasha period-transition boundaries, does not cover "
                "any KP-specific level, and is not a dasha-date-uncertainty "
                "figure. It must not be treated as equivalent to KP's own "
                "nearest_boundary_arcsec (which itself has an unresolved "
                "completeness defect, H-07) or to this certifier's own "
                "moon_distance_to_nearest_boundary_deg diagnostic (M-02)."
            ),
        ],
        "environment": {"python": sys.version.split()[0]},
        "preconditions": preconditions,
        "result": "PASS",
    }
    out = support.emit(report, "VIMSHOTTARI_V1_certification.json", "vimshottari", tee)
    print("=" * 60)
    print("VIMSHOTTARI_V1 CERTIFICATION")
    print("=" * 60)
    print(f"profiles x cases  : 2 x {len(HOLDOUT)} ordinary + {len(BOUNDARY_HOLDOUT)} near-boundary (native profile only)")
    print(f"pratyantar rows   : {total_rows}")
    print(f"lord mismatches   : 0")
    print(f"max start delta   : {worst_start} days (tolerance {START_TOLERANCE_DAYS})")
    print(f"oracle moon delta : {worst_moon} arcsec max (recorded, see D-007)")
    print(f"near-boundary     : {len(NEAR_BOUNDARY_CASE_IDS)} genuine cases (3 per profile, native only), "
          f"max {max(c['moon_distance_to_nearest_boundary_deg'] for c in near_boundary_coverage)} "
          f"deg from boundary (M-02, ADR-0072)")
    print("archived          :", out.relative_to(ROOT).as_posix())
    print("RESULT            : PASS")


if __name__ == "__main__":
    main()
