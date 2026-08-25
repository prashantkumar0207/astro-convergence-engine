"""CURRENT-ENGINE HOLDOUT CERTIFICATION (Phase 1 gate).

Runs the frozen 11-case holdout matrix (identical cases to the legacy
Tier-0 certification in scripts/certify_tier0.py; those cases were
never used to tune the engine) against the CURRENT modular engine
under BOTH named CalculationProfiles, comparing every planet, the
Ascendant, and all 12 Placidus cusps against the independent
Astrodienst swetest 2.10.03 C binary bundled at the repository root.

Certification FAILS LOUDLY (nonzero exit) if the swetest binary or
ephemeris files are unusable, if any Moshier fallback occurs (the
engine's strict mode raises), or if any comparison exceeds the frozen
0.5 arcsecond tolerance (DECISION_LOG D-002).

Results are archived machine-readably in
certification/current_engine_certification.json, human-readably in
reports/certification/current_engine.report.md, and the exact console
transcript in reports/certification/current_engine.console.txt. All three
are written by certification_support.emit() from THE SAME run and THE SAME
result dict, satisfying PROJECT_CONSTITUTION.md s12 condition 3 (audit
finding C-03). Stored JSON is never accepted as proof: every run
regenerates everything from scratch.

Usage: python scripts/certify_current_engine.py
"""

import datetime
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import certification_support as support  # noqa: E402
import swisseph as swe  # noqa: E402

from engine.astronomy.profile import (  # noqa: E402
    KP_KRISHNAMURTI,
    PARASHARI_LAHIRI,
)
from engine.calculations.calculations import calculate  # noqa: E402
from engine.models.birth_data import BirthData  # noqa: E402
from engine.version import ENGINE_VERSION  # noqa: E402

TOLERANCE_ARCSEC = 0.5

BODY_ORDER = [
    "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn",
    "Uranus", "Neptune", "Pluto", "Rahu",
]

PROFILES = {
    "parashari_lahiri": (PARASHARI_LAHIRI, "1"),
    "kp_krishnamurti": (KP_KRISHNAMURTI, "5"),
}

HOLDOUT = [
 {"id": "H1_london_1823",     "date": "1823-04-17", "time": "03:21:07", "lat": 51.5074,  "lon": -0.1278},
 {"id": "H2_newyork_1900",    "date": "1900-01-01", "time": "00:00:00", "lat": 40.7128,  "lon": -74.0060},
 {"id": "H3_sydney_1946",     "date": "1946-06-14", "time": "21:47:53", "lat": -33.8688, "lon": 151.2093},
 {"id": "H4_delhi_1979",      "date": "1979-11-11", "time": "17:41:37", "lat": 28.6667,  "lon": 77.2167},
 {"id": "H5_reykjavik_1992",  "date": "1992-02-29", "time": "23:59:59", "lat": 64.1466,  "lon": -21.9426},
 {"id": "H6_quito_2010",      "date": "2010-07-21", "time": "05:05:05", "lat": -0.1807,  "lon": -78.4678},
 {"id": "H7_tokyo_2033",      "date": "2033-09-03", "time": "11:11:11", "lat": 35.6762,  "lon": 139.6503},
 {"id": "H8_mumbai_2077",     "date": "2077-12-03", "time": "14:30:27", "lat": 19.0760,  "lon": 72.8777},
 {"id": "H9_paris_2350",      "date": "2350-01-15", "time": "06:06:06", "lat": 48.8566,  "lon": 2.3522},
 {"id": "H10_boundary_moon_a", "date": "2025-03-01", "time": "16:21:00", "lat": 28.6667, "lon": 77.2167, "boundary_sensitive": True},
 {"id": "H11_boundary_moon_b", "date": "2025-03-02", "time": "11:38:00", "lat": 28.6667, "lon": 77.2167, "boundary_sensitive": True},
]


def fail(msg: str):
    print("CERTIFICATION FAIL:", msg)
    sys.exit(3)


def source_revision() -> dict:
    """The revision this run executed against, observed, never asserted.

    Recorded so that the two evidence files state what was actually
    verified. `dirty` matters more than the hash: a certification run over
    a modified working tree is evidence about that tree and not about the
    named commit, and the report must say so rather than imply otherwise.
    If git is unavailable the fields say `unavailable`; they are never
    guessed.
    """

    def git(*args) -> str:
        try:
            done = subprocess.run(
                ["git", "-C", str(ROOT), *args],
                capture_output=True, text=True, check=True,
            )
        except (OSError, subprocess.CalledProcessError):
            return "unavailable"
        return done.stdout.strip()

    head = git("rev-parse", "HEAD")
    status = git("status", "--porcelain")
    if head == "unavailable" or status == "unavailable":
        return {"commit": "unavailable", "dirty": "unavailable"}
    return {"commit": head, "dirty": bool(status)}


def arcsec(a: float, b: float) -> float:
    return abs(((a - b + 180.0) % 360.0) - 180.0) * 3600.0


def resolve_swetest() -> Path:
    """Copy the bundled binary to a temp dir and make it executable
    (the repository copy stays byte- and mode-untouched)."""
    bundled = ROOT / "swetest"
    if not bundled.exists():
        fail("bundled swetest binary absent")

    workdir = Path(tempfile.mkdtemp(prefix="swetest_"))
    target = workdir / "swetest"
    shutil.copy2(bundled, target)
    target.chmod(target.stat().st_mode | stat.S_IXUSR)

    out = subprocess.run(
        [str(target), "-b1.1.2000", "-ut0", "-p0", "-emos"],
        capture_output=True, text=True,
    ).stdout
    if "version 2.10.03" not in out:
        fail(f"swetest version mismatch (pinned 2.10.03): {out.splitlines()[:2]!r}")
    return target


#: Q15. Placeholders substituted into the RECORDED command so the artifact is
#: byte-reproducible across runs, machines and checkouts. The command actually
#: EXECUTED is unchanged; only the recorded string is normalised. Root D-005
#: removed exactly this class of environment-specific absolute-path dependency
#: from the legacy Tier-0 package, and it had reappeared here.
BUNDLED_BINARY_PLACEHOLDER = "<bundled>/swetest"
REPO_ROOT_PLACEHOLDER = "<repo-root>"


def recorded_command(cmd: list[str], binary: Path) -> str:
    """The invocation, with the run's temp dir and the checkout path removed.

    Two runs of identical code over identical data must produce identical
    bytes, otherwise the artifact cannot be diffed across runs to show that
    nothing changed. Substitution is exact-string and applied only to the two
    volatile components, so every argument that affects the computation, the
    date, the time, the body list, the sidereal mode and the house
    specification, is recorded verbatim.
    """

    normalised = []
    for argument in cmd:
        if argument == str(binary):
            normalised.append(BUNDLED_BINARY_PLACEHOLDER)
        elif argument == f"-edir{ROOT}":
            normalised.append(f"-edir{REPO_ROOT_PLACEHOLDER}")
        else:
            normalised.append(argument)
    return " ".join(normalised)


def run_swetest(binary: Path, case: dict, sid: str) -> dict:
    d = case["date"].split("-")
    bdate = f"{int(d[2])}.{int(d[1])}.{d[0]}"
    cmd = [
        str(binary), f"-edir{ROOT}", f"-b{bdate}", f"-ut{case['time']}",
        "-p0123456789m", "-eswe", f"-sid{sid}",
        f"-house{case['lon']},{case['lat']},P", "-fPl", "-g,", "-head",
    ]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout

    planets, cusps, asc = {}, {}, None
    for line in out.splitlines():
        parts = [x.strip() for x in line.split(",")]
        if len(parts) < 2:
            continue
        name, val = parts[0], parts[1]
        try:
            v = float(val)
        except ValueError:
            continue
        if name == "mean Node":
            planets["Rahu"] = v
        elif name in BODY_ORDER:
            planets[name] = v
        elif re.match(r"^house\s+\d+$", name):
            cusps[name.split()[1]] = v
        elif name == "Ascendant":
            asc = v

    if len(planets) < 11 or len(cusps) != 12 or asc is None:
        fail(f"swetest output incomplete for {case['id']} sid{sid}")

    planets["Ketu"] = (planets["Rahu"] + 180.0) % 360.0
    return {"cmd": recorded_command(cmd, binary), "planets": planets,
            "cusps": cusps, "ascendant": asc}


def engine_case(case: dict, profile) -> dict:
    y, m, d = (int(x) for x in case["date"].split("-"))
    hh, mm, ss = (int(x) for x in case["time"].split(":"))
    birth = BirthData(
        year=y, month=m, day=d, hour=hh, minute=mm, second=float(ss),
        latitude=case["lat"], longitude=case["lon"], timezone="UTC",
    )
    snap = calculate(birth, profile).snapshot

    name_map = {n: snap.sidereal_planets[n].longitude
                for n in BODY_ORDER + ["Ketu"]}
    return {
        "planets": name_map,
        "ascendant": snap.houses.ascendant,
        "cusps": {str(i + 1): c for i, c in enumerate(snap.houses.houses)},
        "ayanamsa_value": snap.ayanamsa.value,
        "ayanamsa_mode": snap.ayanamsa.mode,
        "provenance": {
            "profile": snap.provenance.profile_name,
            "frame": snap.provenance.frame,
            "ephemeris_mode": snap.provenance.ephemeris_mode,
            "house_system": snap.provenance.house_system,
            "node_policy": snap.provenance.node_policy,
        },
        "moon_nakshatra": _moon_classification(snap),
    }


def _moon_classification(snap) -> dict:
    from engine.astrology.nakshatra import nakshatra
    from engine.astrology.pada import pada

    moon = snap.sidereal_planets["Moon"].longitude
    return {"longitude": moon, "nakshatra": nakshatra(moon),
            "nakshatra_pada": pada(moon)}


def exact_nakshatra_reference(longitude: float) -> dict:
    """Independent exact-arithmetic classification of a longitude."""
    from fractions import Fraction

    span = Fraction(360, 27)
    tol = Fraction(1, 10**10)
    x = Fraction(repr(longitude)) % 360
    idx = min(int((x + tol) / span), 26)
    within = x - idx * span
    if within < 0:
        within = Fraction(0)
    p = min(int((within + tol) / Fraction(360, 108)), 3)
    return {"nakshatra": idx + 1, "nakshatra_pada": p + 1}


def main():
    # Capture the console transcript from the first line, so the retained
    # transcript is the whole run rather than the part after setup.
    tee = support.start_transcript()

    # Q16 / VALIDATION_STANDARD s2 rules 4 and 6. Verifying the swetest
    # binary's version string proves the ORACLE is the pinned one; it proves
    # nothing about the ephemeris DATA that both the oracle and the engine
    # read. Both resolve to the repository root, and CHECKSUMS.sha256 covers
    # exactly the three files engine.astronomy.ephemeris.REQUIRED_FILES
    # declares, so this is the integrity check for the data the run depends
    # on. It runs FIRST: a certification claim over unverified reference data
    # is worth nothing, however good the numbers look.
    try:
        preconditions = support.preflight()
    except support.CertificationFailure as exc:
        fail(f"precondition failed, refusing to certify: {exc}")

    binary = resolve_swetest()
    revision = source_revision()

    report = {
        "schema": "current_engine_certification_v1",
        "adr": "ADR-0005",
        "date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
        "scope": "Current modular engine, Tier-0 astronomical kernel: sidereal "
                 "planetary longitudes, Ascendant and 12 Placidus cusps, under "
                 "both ratified calculation profiles, against the bundled "
                 "independent swetest 2.10.03 binary over the frozen 11-case "
                 "holdout.",
        "engine": "engine/ (modular), version from engine/version.py",
        "reference": "Astrodienst swetest v2.10.03 (independent C binary, "
                     "bundled, version-verified at runtime)",
        "tolerance_arcsec": TOLERANCE_ARCSEC,
        "preconditions": preconditions,
        "run": {
            "source_revision": revision["commit"],
            "working_tree_dirty": revision["dirty"],
            "engine_version": ENGINE_VERSION,
            "executed_utc": datetime.datetime.now(
                datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "python": sys.version.split()[0],
            "holdout_cases": ", ".join(case["id"] for case in HOLDOUT),
            "reference_binary": "swetest 2.10.03 (bundled, version-verified "
                                "at runtime)",
        },
        "profiles": {},
    }

    overall_max = {"planets": 0.0, "ascendant": 0.0, "cusps": 0.0}
    failures = []

    for profile_name, (profile, sid) in PROFILES.items():
        prof_block = {"sid_mode": int(sid), "cases": [],
                      "max_planet_error_arcsec": 0.0,
                      "max_ascendant_error_arcsec": 0.0,
                      "max_cusp_error_arcsec": 0.0,
                      "planet_comparisons": 0, "cusp_comparisons": 0}

        for case in HOLDOUT:
            ref = run_swetest(binary, case, sid)
            got = engine_case(case, profile)

            planet_errors = {
                name: arcsec(got["planets"][name], ref["planets"][name])
                for name in BODY_ORDER + ["Ketu"]
            }
            asc_error = arcsec(got["ascendant"], ref["ascendant"])
            cusp_errors = {
                k: arcsec(got["cusps"][k], ref["cusps"][k])
                for k in ref["cusps"]
            }

            worst_planet = max(planet_errors.values())
            worst_cusp = max(cusp_errors.values())

            entry = {
                "id": case["id"],
                "swetest_cmd": ref["cmd"],
                "ayanamsa_value_deg": got["ayanamsa_value"],
                "provenance": got["provenance"],
                "max_planet_error_arcsec": worst_planet,
                "ascendant_error_arcsec": asc_error,
                "max_cusp_error_arcsec": worst_cusp,
                "planet_errors_arcsec": planet_errors,
                "cusp_errors_arcsec": cusp_errors,
            }

            if case.get("boundary_sensitive"):
                exact = exact_nakshatra_reference(
                    ref["planets"]["Moon"]
                )
                entry["moon_boundary_check"] = {
                    "engine": got["moon_nakshatra"],
                    "exact_reference_on_swetest_moon": exact,
                    "agrees": (
                        got["moon_nakshatra"]["nakshatra"] == exact["nakshatra"]
                        and got["moon_nakshatra"]["nakshatra_pada"]
                        == exact["nakshatra_pada"]
                    ),
                }
                if not entry["moon_boundary_check"]["agrees"]:
                    failures.append(f"{profile_name}/{case['id']}: Moon "
                                    "nakshatra classification mismatch")

            for label, err in (("planet", worst_planet),
                               ("ascendant", asc_error),
                               ("cusp", worst_cusp)):
                if err > TOLERANCE_ARCSEC:
                    failures.append(
                        f"{profile_name}/{case['id']}: {label} error "
                        f"{err:.6f} arcsec > {TOLERANCE_ARCSEC}"
                    )

            prof_block["cases"].append(entry)
            prof_block["max_planet_error_arcsec"] = max(
                prof_block["max_planet_error_arcsec"], worst_planet)
            prof_block["max_ascendant_error_arcsec"] = max(
                prof_block["max_ascendant_error_arcsec"], asc_error)
            prof_block["max_cusp_error_arcsec"] = max(
                prof_block["max_cusp_error_arcsec"], worst_cusp)
            prof_block["planet_comparisons"] += len(planet_errors)
            prof_block["cusp_comparisons"] += len(cusp_errors)

        report["profiles"][profile_name] = prof_block
        overall_max["planets"] = max(overall_max["planets"],
                                     prof_block["max_planet_error_arcsec"])
        overall_max["ascendant"] = max(overall_max["ascendant"],
                                       prof_block["max_ascendant_error_arcsec"])
        overall_max["cusps"] = max(overall_max["cusps"],
                                   prof_block["max_cusp_error_arcsec"])

    # A-1 verification: the two profiles must differ by the known
    # Lahiri-vs-Krishnamurti offset (roughly 5-6 arcmin), proving the
    # profile system actually drives the computation.
    lahiri_asc = report["profiles"]["parashari_lahiri"]["cases"][0]
    kp_asc = report["profiles"]["kp_krishnamurti"]["cases"][0]
    aya_diff_arcmin = abs(lahiri_asc["ayanamsa_value_deg"]
                          - kp_asc["ayanamsa_value_deg"]) * 60.0
    report["ayanamsa_profile_check"] = {
        "lahiri_value_deg_H1": lahiri_asc["ayanamsa_value_deg"],
        "krishnamurti_value_deg_H1": kp_asc["ayanamsa_value_deg"],
        "difference_arcmin": aya_diff_arcmin,
        "expected_band_arcmin": [3.0, 10.0],
    }
    if not 3.0 < aya_diff_arcmin < 10.0:
        failures.append(
            f"ayanamsa profile difference {aya_diff_arcmin:.3f} arcmin "
            "outside the expected 3-10 arcmin band"
        )

    report["summary"] = {
        "cases_per_profile": len(HOLDOUT),
        "profiles_certified": list(PROFILES),
        "total_planet_comparisons": sum(
            p["planet_comparisons"] for p in report["profiles"].values()),
        "total_cusp_comparisons": sum(
            p["cusp_comparisons"] for p in report["profiles"].values()),
        "max_planet_error_arcsec": overall_max["planets"],
        "max_ascendant_error_arcsec": overall_max["ascendant"],
        "max_cusp_error_arcsec": overall_max["cusps"],
        "moshier_fallback_events": 0,  # strict mode: any fallback raises
        "failures": failures,
        "result": "PASS" if not failures else "FAIL",
    }

    # PROJECT_CONSTITUTION.md s12 condition 3, audit finding C-03: the
    # machine-readable artifact, the human-readable report and the console
    # transcript are all produced here, by this run, from THIS dict. The
    # report is derived from the serialised object rather than written
    # alongside it, so the two cannot drift apart.
    outfile = support.emit(
        report,
        artifact_name="current_engine_certification.json",
        slug="current_engine",
        tee=tee,
    )

    s = report["summary"]
    print("=" * 64)
    print("CURRENT-ENGINE HOLDOUT CERTIFICATION")
    print("=" * 64)
    print(f"ephemeris verified: {preconditions['data_assets']['assets_verified']} "
          "assets against CHECKSUMS.sha256")
    print(f"anti-fitting scan : {preconditions['anti_fitting']['modules_scanned']} "
          f"modules, {len(preconditions['anti_fitting']['findings'])} findings")
    print(f"profiles          : {', '.join(PROFILES)}")
    print(f"cases per profile : {s['cases_per_profile']}")
    print(f"planet comparisons: {s['total_planet_comparisons']}")
    print(f"cusp comparisons  : {s['total_cusp_comparisons']}")
    print(f"max planet error  : {s['max_planet_error_arcsec']:.6f} arcsec")
    print(f"max asc error     : {s['max_ascendant_error_arcsec']:.6f} arcsec")
    print(f"max cusp error    : {s['max_cusp_error_arcsec']:.6f} arcsec")
    print(f"ayanamsa Lahiri/KP: {aya_diff_arcmin:.3f} arcmin apart")
    print(f"archived          : {outfile.relative_to(ROOT).as_posix()}")
    print(f"RESULT            : {s['result']}")
    if failures:
        for f_ in failures:
            print("  FAIL:", f_)
        sys.exit(3)


if __name__ == "__main__":
    main()
