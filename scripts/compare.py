"""Regression comparison against Brihat transcription fixtures. Produces reports/regression_report.json"""
import sys, os, json, statistics
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import swisseph as swe
from astro_kernel import engine, kp
from astro_kernel.profile import PROFILE, PLACES
from fixtures.brihat_fixtures import CASE_C, CASE_D, CASES_META_ONLY

def dms_to_deg(s):
    d, m, sec = s.split(":")
    return int(d) + int(m)/60 + int(sec)/3600

def wrap(a, b):
    return ((a - b + 180) % 360) - 180

AYAN_CANDIDATES = ["LAHIRI", "KRISHNAMURTI"] + (["KRISHNAMURTI_VP291"] if hasattr(swe, "SIDM_KRISHNAMURTI_VP291") else [])
NODE_CANDIDATES = ["TRUE", "MEAN"]

def compare_case(case):
    place = PLACES[case["place"]]
    fixture_pl = {k: dms_to_deg(v[0]) for k, v in case["planets"].items()}

    # PROFILE IDENTIFICATION PROBE (documented diagnostic; no per-planet constants, no input reverse-solving)
    probes = []
    for ay in AYAN_CANDIDATES:
        for nd in NODE_CANDIDATES:
            ch = engine.compute(case["date"], case["time"], place["lat"], place["lon"], ayan=ay, node=nd)
            ds = []
            for name, flon in fixture_pl.items():
                if name == "Ascendant":
                    continue
                ds.append(abs(wrap(ch["bodies"][name]["lon_deg"], flon)) * 3600)
            probes.append({"ayanamsha": ay, "node": nd,
                           "mean_abs_arcsec": round(statistics.mean(ds), 2),
                           "median_abs_arcsec": round(statistics.median(ds), 2),
                           "max_abs_arcsec": round(max(ds), 2)})
    best = min(probes, key=lambda p: p["median_abs_arcsec"])

    # PRIMARY detailed run (declared profile: KRISHNAMURTI + TRUE node)
    ch = engine.compute(case["date"], case["time"], place["lat"], place["lon"],
                        ayan="KRISHNAMURTI", node="MEAN")
    rows_pl, rows_cu = [], []
    hier_match = {"SL": 0, "NL": 0, "SB": 0, "SS": 0}
    hier_total = 0
    for name, (dms, SL, NL, SB, SS) in case["planets"].items():
        got = ch["bodies"][name]
        d = wrap(got["lon_deg"], dms_to_deg(dms)) * 3600
        m = [got["SL"] == SL, got["NL"] == NL, got["SB"] == SB, got["SS"] == SS]
        for k, ok in zip(("SL", "NL", "SB", "SS"), m):
            hier_match[k] += ok
        hier_total += 1
        rows_pl.append({"body": name, "fixture_dms": dms, "computed_deg": round(got["lon_deg"], 6),
                        "delta_arcsec": round(d, 1),
                        "fx_lords": f"{SL}/{NL}/{SB}/{SS}",
                        "calc_lords": f"{got['SL']}/{got['NL']}/{got['SB']}/{got['SS']}",
                        "lords_match": "".join("Y" if x else "N" for x in m)})
    for h, (dms, SL, NL, SB, SS) in case["cusps"].items():
        got = ch["cusps"][h]
        d = wrap(got["lon_deg"], dms_to_deg(dms)) * 3600
        m = [got["SL"] == SL, got["NL"] == NL, got["SB"] == SB, got["SS"] == SS]
        rows_cu.append({"cusp": h, "fixture_dms": dms, "computed_deg": round(got["lon_deg"], 6),
                        "delta_arcsec": round(d, 1),
                        "fx_lords": f"{SL}/{NL}/{SB}/{SS}",
                        "calc_lords": f"{got['SL']}/{got['NL']}/{got['SB']}/{got['SS']}",
                        "lords_match": "".join("Y" if x else "N" for x in m)})

    # STRUCTURAL CHECK: run OUR interval engine on the FIXTURE's own (display-rounded) longitudes
    structural = {"SL": 0, "NL": 0, "SB": 0, "SS": 0, "total": 0, "boundary_flags": []}
    for coll in (case["planets"], case["cusps"]):
        for key, (dms, SL, NL, SB, SS) in coll.items():
            c = kp.chain(dms_to_deg(dms))
            structural["total"] += 1
            structural["SL"] += c["SL"] == SL
            structural["NL"] += c["NL"] == NL
            structural["SB"] += c["SB"] == SB
            structural["SS"] += c["SS"] == SS
            mism = [lv for lv, a, b in (("SL", c["SL"], SL), ("NL", c["NL"], NL),
                                        ("SB", c["SB"], SB), ("SS", c["SS"], SS)) if a != b]
            if mism:
                structural["boundary_flags"].append({"item": key, "mismatch_levels": mism,
                    "nearest_boundary_arcsec": round(c["nearest_boundary_arcsec"], 2),
                    "within_display_rounding": c["nearest_boundary_arcsec"] <= 1.5})
    pl_ds = [abs(r["delta_arcsec"]) for r in rows_pl]
    cu_ds = [abs(r["delta_arcsec"]) for r in rows_cu]
    return {"label": case["label"], "place_used": place,
            "profile_probe": probes, "best_probe": best,
            "planets": rows_pl, "cusps": rows_cu,
            "summary": {
              "planets_mean_abs_arcsec": round(statistics.mean(pl_ds), 1),
              "planets_max_abs_arcsec": round(max(pl_ds), 1),
              "cusps_mean_abs_arcsec": round(statistics.mean(cu_ds), 1),
              "cusps_max_abs_arcsec": round(max(cu_ds), 1),
              "hierarchy_match_primary": hier_match, "hierarchy_total": hier_total},
            "structural_check_on_fixture_longitudes": structural}

def main():
    rep = {"schema": "astro_kernel_regression_v1", "profile": PROFILE,
           "cases": [compare_case(CASE_C), compare_case(CASE_D)],
           "meta_only_cases": CASES_META_ONLY}
    samples = {}
    for lbl, m in CASES_META_ONLY.items():
        p = PLACES[m["place"]]
        samples[lbl] = engine.compute(m["date"], m["time"], p["lat"], p["lon"])
    os.makedirs("reports", exist_ok=True)
    json.dump(rep, open("reports/regression_report.json", "w"), indent=1)
    json.dump(samples, open("reports/sample_outputs_cases_AB.json", "w"), indent=1)
    for c in rep["cases"]:
        print("==", c["label"], "best probe:", c["best_probe"])
        print("   primary summary:", c["summary"])
        s = c["structural_check_on_fixture_longitudes"]
        print("   structural on fixture lons: SL %d NL %d SB %d SS %d of %d; flags: %d" %
              (s["SL"], s["NL"], s["SB"], s["SS"], s["total"], len(s["boundary_flags"])))
        for f in s["boundary_flags"]:
            print("     flag:", f)

if __name__ == "__main__":
    main()
