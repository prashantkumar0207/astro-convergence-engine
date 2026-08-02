"""TIER-0 CERTIFICATION HARNESS (portable, v1.3).
All paths resolve relative to the package root. Certification FAILS LOUDLY (nonzero exit) if:
ephemeris files are absent or checksums mismatch, swetest is absent and cannot be built,
SWIEPH is not actually used, or any Moshier fallback occurs. Stored JSON is never accepted
as proof: every run regenerates all calculations and comparisons from scratch.
Holdout cases were NEVER used to tune or debug the engine (tuning/debug fixtures were
Brihat CASE C 1985 Patna and CASE D 2025 Dehradun only)."""
import sys, os, json, subprocess, re, statistics, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import swisseph as swe
from astro_kernel import engine, kp

EPHE = ROOT / "ephe"
SWETEST = ROOT / "swetest_reference" / "swetest"
SID = "5"  # SE_SIDM_KRISHNAMURTI
BODY_ORDER = ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Uranus","Neptune","Pluto","Rahu"]

HOLDOUT = [
 {"id":"H1_london_1823",    "date":"1823-04-17","time":"03:21:07","lat":51.5074, "lon":-0.1278},
 {"id":"H2_newyork_1900",   "date":"1900-01-01","time":"00:00:00","lat":40.7128, "lon":-74.0060},
 {"id":"H3_sydney_1946",    "date":"1946-06-14","time":"21:47:53","lat":-33.8688,"lon":151.2093},
 {"id":"H4_delhi_1979",     "date":"1979-11-11","time":"17:41:37","lat":28.6667, "lon":77.2167},
 {"id":"H5_reykjavik_1992", "date":"1992-02-29","time":"23:59:59","lat":64.1466, "lon":-21.9426},
 {"id":"H6_quito_2010",     "date":"2010-07-21","time":"05:05:05","lat":-0.1807, "lon":-78.4678},
 {"id":"H7_tokyo_2033",     "date":"2033-09-03","time":"11:11:11","lat":35.6762, "lon":139.6503},
 {"id":"H8_mumbai_2077",    "date":"2077-12-03","time":"14:30:27","lat":19.0760, "lon":72.8777},
 {"id":"H9_paris_2350",     "date":"2350-01-15","time":"06:06:06","lat":48.8566, "lon":2.3522},
 {"id":"H10_boundary_moon_a","date":"2025-03-01","time":"16:21:00","lat":28.6667,"lon":77.2167,"boundary_sensitive":True},
 {"id":"H11_boundary_moon_b","date":"2025-03-02","time":"11:38:00","lat":28.6667,"lon":77.2167,"boundary_sensitive":True},
]

def fail(msg):
    print("CERTIFICATION FAIL:", msg)
    sys.exit(3)

def verify_checksums():
    manifest = EPHE / "CHECKSUMS.sha256"
    if not manifest.exists():
        fail(f"missing {manifest}")
    files = {}
    for line in manifest.read_text().splitlines():
        if not line.strip():
            continue
        want, fname = line.split()
        f = EPHE / fname
        if not f.exists():
            fail(f"required ephemeris file absent: {f}")
        got = hashlib.sha256(f.read_bytes()).hexdigest()
        if got != want:
            fail(f"checksum mismatch {fname}: expected {want} got {got}")
        files[fname] = want
    return files

def resolve_swetest():
    if not (SWETEST.exists() and os.access(SWETEST, os.X_OK)):
        print("bundled swetest not usable; attempting official-source build ...")
        r = subprocess.run(["bash", str(ROOT / "swetest_reference" / "build_swetest.sh")])
        if r.returncode != 0 or not (SWETEST.exists() and os.access(SWETEST, os.X_OK)):
            fail("swetest absent and unbuildable")
    out = subprocess.run([str(SWETEST), "-b1.1.2000", "-ut0", "-p0", "-emos"],
                         capture_output=True, text=True).stdout
    if "version 2.10.03" not in out:
        fail(f"swetest version mismatch (pinned 2.10.03); output head: {out.splitlines()[:2]!r}")
    return "2.10.03"

def run_swetest(case):
    d = case["date"].split("-"); t = case["time"]
    bdate = f"{int(d[2])}.{int(d[1])}.{d[0]}"
    cmd = [str(SWETEST), f"-edir{EPHE}", f"-b{bdate}", f"-ut{t}", "-p0123456789m", "-eswe",
           f"-sid{SID}", f"-house{case['lon']},{case['lat']},P", "-fPl", "-g,", "-head"]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    ref_pl, ref_cu, ref_asc = {}, {}, None
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
            ref_pl["Rahu"] = v
        elif name in BODY_ORDER:
            ref_pl[name] = v
        elif re.match(r"^house\s+\d+$", name):
            ref_cu[name.split()[1]] = v
        elif name == "Ascendant":
            ref_asc = v
    if len(ref_pl) < 11 or len(ref_cu) != 12 or ref_asc is None:
        fail(f"swetest output incomplete for {case['id']}")
    ref_pl["Ketu"] = (ref_pl["Rahu"] + 180.0) % 360.0
    return {"cmd": " ".join(cmd), "planets": ref_pl, "cusps": ref_cu, "ascendant": ref_asc, "raw": out}

def arcsec(a, b):
    return abs(((a - b + 180) % 360) - 180) * 3600

def scan_overfitting():
    """Search engine+kp source for hard-coded per-body corrections / fitted constants.
    Comments/docstrings stripped first. Whitelist = zodiac geometry (30/360/27/40/3),
    Vimshottari years (7,20,6,10,18,16,19,17; total 120), time constants (60/3600/86400),
    Ketu antipode definition (180.0/360.0), small indices and flag values."""
    allowed = {"30","360","27","40","3","120","180","0","1","2","9","12","13","60","86400.0",
               "7","20","6","10","18","16","19","17","1.0","-1.0","3600","180.0","360.0"}
    findings = []
    for f in ("astro_kernel/kp.py", "astro_kernel/engine.py"):
        src = (ROOT / f).read_text()
        src = re.sub(r'"""[\s\S]*?"""', "", src)
        src = re.sub(r"#.*", "", src)
        for n in set(re.findall(r"(?<![\w.])(\d+\.\d+|\d+)(?![\w.])", src)):
            if n not in allowed:
                findings.append({"file": f, "literal": n})
    return findings

def main():
    ephe_files = verify_checksums()
    swetest_version = resolve_swetest()
    report = {"schema": "tier0_certification_v1.3",
              "reference": f"Astrodienst swetest v{swetest_version} (independent C binary, "
                           "package-relative, version-verified at runtime)",
              "ephemeris_files": ephe_files, "cases": [],
              "kp_holdout_hierarchy_mismatches": []}
    all_pl, all_cu, all_asc = [], [], []
    mism = {"SL": 0, "NL": 0, "SB": 0, "SS": 0}
    (ROOT / "reports").mkdir(exist_ok=True)
    raws = []
    fallback_events = 0
    for case in HOLDOUT:
        ref = run_swetest(case)
        raws.append({"id": case["id"], "cmd": ref["cmd"], "output": ref["raw"]})
        try:
            ch = engine.compute(case["date"], case["time"], case["lat"], case["lon"],
                                ayan="KRISHNAMURTI", node="MEAN", tz="UTC",
                                ephe="SWIEPH", ephe_path=str(EPHE), strict_ephe=True)
        except RuntimeError as e:
            fallback_events += 1
            fail(f"Moshier fallback / SWIEPH unavailable in {case['id']}: {e}")
        if ch["profile"]["actual_ephemeris_modes"] != ["SWIEPH"]:
            fallback_events += 1
            fail(f"non-SWIEPH mode recorded in {case['id']}: {ch['profile']['actual_ephemeris_modes']}")
        crow = {"id": case["id"], "planets": {}, "cusps": {},
                "boundary_sensitive": case.get("boundary_sensitive", False)}
        for name, refv in ref["planets"].items():
            got = ch["bodies"][name]["lon_deg"]
            d = arcsec(got, refv)
            all_pl.append((case["id"], name, d))
            hg, hr = kp.chain(got), kp.chain(refv)
            flips = [lv for lv in ("SL", "NL", "SB", "SS") if hg[lv] != hr[lv]]
            for lv in flips:
                mism[lv] += 1
                report["kp_holdout_hierarchy_mismatches"].append(
                    {"case": case["id"], "body": name, "level": lv, "delta_arcsec": d,
                     "nearest_boundary_arcsec": hg["nearest_boundary_arcsec"]})
            crow["planets"][name] = {"ref": refv, "calc": got, "delta_arcsec": round(d, 6),
                                     "hier_flip": flips}
        a = arcsec(ch["bodies"]["Ascendant"]["lon_deg"], ref["ascendant"])
        all_asc.append((case["id"], a))
        crow["ascendant_delta_arcsec"] = round(a, 6)
        for h, refv in ref["cusps"].items():
            d = arcsec(ch["cusps"][h]["lon_deg"], refv)
            all_cu.append((case["id"], h, d))
            hg, hr = kp.chain(ch["cusps"][h]["lon_deg"]), kp.chain(refv)
            flips = [lv for lv in ("SL", "NL", "SB", "SS") if hg[lv] != hr[lv]]
            for lv in flips:
                mism[lv] += 1
                report["kp_holdout_hierarchy_mismatches"].append(
                    {"case": case["id"], "cusp": h, "level": lv, "delta_arcsec": d})
            crow["cusps"][h] = {"ref": refv, "calc": ch["cusps"][h]["lon_deg"],
                                "delta_arcsec": round(d, 6)}
        report["cases"].append(crow)

    pl_ds = [d for _, _, d in all_pl]; cu_ds = [d for _, _, d in all_cu]; as_ds = [d for _, d in all_asc]
    worst_pl = max(all_pl, key=lambda x: x[2]); worst_cu = max(all_cu, key=lambda x: x[2])
    fitting = scan_overfitting()
    report["summary"] = {
        "swetest_version": swetest_version,
        "planetary_holdout_count": len(all_pl),
        "cusp_holdout_count": len(all_cu),
        "ascendant_count": len(as_ds),
        "max_planetary_error_arcsec": round(max(pl_ds), 6),
        "worst_planet": {"case": worst_pl[0], "body": worst_pl[1]},
        "median_planetary_error_arcsec": round(statistics.median(pl_ds), 6),
        "max_ascendant_error_arcsec": round(max(as_ds), 6),
        "max_cusp_error_arcsec": round(max(cu_ds), 6),
        "worst_cusp": {"case": worst_cu[0], "cusp": worst_cu[1]},
        "hierarchy_mismatches": mism,
        "moshier_fallback_events": fallback_events,
        "hardcoded_fitting_findings": fitting,
    }
    json.dump(report, open(ROOT / "reports" / "tier0_certification.json", "w"), indent=1)
    json.dump(raws, open(ROOT / "reports" / "swetest_raw_outputs.json", "w"), indent=1)
    s = report["summary"]
    print(f"certification calculations complete: {s['planetary_holdout_count']} planetary, "
          f"{s['cusp_holdout_count']} cusp, {s['ascendant_count']} ascendant comparisons; "
          f"max errors {s['max_planetary_error_arcsec']}/{s['max_ascendant_error_arcsec']}/"
          f"{s['max_cusp_error_arcsec']} arcsec; hierarchy mismatches {mism}; "
          f"fallback events {fallback_events}; fitting findings {len(fitting)}")

if __name__ == "__main__":
    main()
