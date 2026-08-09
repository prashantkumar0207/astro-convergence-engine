"""KP_CHAIN_V1 CERTIFICATION RUNNER (Gate 6 of ADR-0006).

Regenerates certification/KP_CHAIN_V1_certification.json FROM SCRATCH
on every run; the stored JSON is never accepted as proof. Collects:

  A. Legacy-oracle equivalence (dense sweep + full boundary battery)
  B. Chart-level 11-case holdout vs the certified legacy kernel
  C. Transcribed-fixture structural check (200 fields)
  D. Independent validator invocation (validate_kp_holdout.py)

Exit code 0 = PASS, 3 = FAIL.
"""

import json
import math
import subprocess
import sys
from datetime import date
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import swisseph as swe  # noqa: E402

from engine.kp.chain import kp_chain  # noqa: E402
from engine.kp.chart import kp_chart  # noqa: E402
from engine.kp.intervals import all_boundaries  # noqa: E402
from engine.models.birth_data import BirthData  # noqa: E402
from legacy import engine as legacy_engine  # noqa: E402
from legacy import kp as legacy_kp  # noqa: E402
import brihat_fixtures  # noqa: E402

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
 {"id": "H10_boundary_moon_a", "date": "2025-03-01", "time": "16:21:00", "lat": 28.6667, "lon": 77.2167},
 {"id": "H11_boundary_moon_b", "date": "2025-03-02", "time": "11:38:00", "lat": 28.6667, "lon": 77.2167},
]


def fail(message):
    print("KP CERTIFICATION FAIL:", message)
    sys.exit(3)


def arcsec(a, b):
    return abs(((a - b + 180.0) % 360.0) - 180.0) * 3600.0


def chain_tuple(chain):
    return (chain.sign_lord, chain.nakshatra_lord, chain.sub_lord, chain.sub_sub_lord)


def legacy_tuple(entry):
    return (entry["SL"], entry["NL"], entry["SB"], entry["SS"])


def gate_a_oracle_equivalence():
    mismatches = 0
    step = 360.0 / 51429
    dense = 51429
    for i in range(dense):
        lon = i * step
        if chain_tuple(kp_chain(lon)) != legacy_tuple(legacy_kp.chain(lon)):
            mismatches += 1
    boundary_points = 0
    eps = Fraction(1, 10**9)
    for bound in all_boundaries():
        points = [bound, bound + eps]
        if bound > 0:
            points.append(bound - eps)
        base = float(bound)
        down = up = base
        for _ in range(3):
            down = math.nextafter(down, -math.inf)
            up = math.nextafter(up, math.inf)
            points.extend(p for p in (down, up) if 0.0 <= p < 360.0)
        for point in points:
            if chain_tuple(kp_chain(point)) != legacy_tuple(legacy_kp.chain(point)):
                mismatches += 1
            boundary_points += 1
    if mismatches:
        fail(f"oracle equivalence: {mismatches} mismatches")
    return {"dense_points": dense, "boundary_points": boundary_points,
            "mismatches": 0}


def gate_b_holdout_charts():
    max_arcsec = 0.0
    chain_checks = 0
    chain_mismatches = 0
    for case in HOLDOUT:
        year, month, day = (int(x) for x in case["date"].split("-"))
        hour, minute, second = (int(x) for x in case["time"].split(":"))
        ours = kp_chart(BirthData(year, month, day, hour, minute,
                                  float(second), case["lat"], case["lon"], "UTC"))
        theirs = legacy_engine.compute(
            case["date"], case["time"], case["lat"], case["lon"],
            ayan="KRISHNAMURTI", node="MEAN", tz="UTC",
            ephe="SWIEPH", ephe_path=str(ROOT), strict_ephe=True)
        pairs = [(body.longitude, body.chain, theirs["bodies"][body.name])
                 for body in ours.bodies]
        pairs.append((ours.ascendant.longitude, ours.ascendant.chain,
                      theirs["bodies"]["Ascendant"]))
        pairs.extend((cusp.longitude, cusp.chain, theirs["cusps"][str(cusp.number)])
                     for cusp in ours.cusps)
        for longitude, chain, legacy_entry in pairs:
            max_arcsec = max(max_arcsec, arcsec(longitude, legacy_entry["lon_deg"]))
            chain_checks += 1
            if chain_tuple(chain) != legacy_tuple(legacy_entry):
                chain_mismatches += 1
    if max_arcsec > 0.001:
        fail(f"holdout longitude divergence {max_arcsec} arcsec > 0.001")
    if chain_mismatches:
        fail(f"holdout chain mismatches: {chain_mismatches}")
    return {"cases": len(HOLDOUT), "chain_comparisons": chain_checks,
            "chain_mismatches": 0, "max_longitude_delta_arcsec": max_arcsec}


def gate_c_fixture_structural():
    fields = 0
    mismatches = 0
    for case in (brihat_fixtures.CASE_C, brihat_fixtures.CASE_D):
        for items in (case["planets"], case["cusps"]):
            for _, (dms, sl, nl, sb, ss) in items.items():
                deg, minute, second = (int(x) for x in dms.split(":"))
                exact = Fraction(deg) + Fraction(minute, 60) + Fraction(second, 3600)
                if chain_tuple(kp_chain(exact)) != (sl, nl, sb, ss):
                    mismatches += 1
                fields += 4
    if mismatches:
        fail(f"fixture structural mismatches: {mismatches}")
    if fields != 200:
        fail(f"fixture field count {fields} != 200")
    return {"fields": fields, "mismatches": 0}


def gate_d_independent_validator():
    result = subprocess.run(
        [sys.executable, str(ROOT / "validate_kp_holdout.py")],
        capture_output=True, text=True)
    if result.returncode != 0 or "ALL INDEPENDENT KP CHAIN CASES PASSED" not in result.stdout:
        fail(f"independent validator failed: {result.stdout[-400:]}")
    return {"result": "PASS"}


def main():
    report = {
        "schema": "kp_chain_v1_certification",
        "adr": "ADR-0006",
        "date": str(date.today()),
        "scope": "KP lordship chain (SL/NL/SB/SS) and KP fact charts under kp_krishnamurti",
        "explicit_non_claims": [
            "significators (Tier-1 KP_SIGNIFICATOR_V1; spec must be frozen first, D-008)",
            "four-step", "ruling planets", "horary", "dashas",
        ],
        "environment": {
            "python": sys.version.split()[0],
            "swisseph": getattr(swe, "version", "unknown"),
        },
        "gates": {
            "A_legacy_oracle_equivalence": gate_a_oracle_equivalence(),
            "B_holdout_chart_equivalence": gate_b_holdout_charts(),
            "C_fixture_structural_200": gate_c_fixture_structural(),
            "D_independent_validator": gate_d_independent_validator(),
        },
        "result": "PASS",
    }
    out = ROOT / "certification" / "KP_CHAIN_V1_certification.json"
    out.write_text(json.dumps(report, indent=1) + "\n")
    print("=" * 60)
    print("KP_CHAIN_V1 CERTIFICATION")
    print("=" * 60)
    for name, gate in report["gates"].items():
        print(f"{name}: {gate}")
    print("archived          :", out.relative_to(ROOT))
    print("RESULT            : PASS")


if __name__ == "__main__":
    main()
