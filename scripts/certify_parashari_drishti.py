"""PARASHARI_DRISHTI_V1 CERTIFICATION RUNNER (ADR-0012).

Regenerates certification/PARASHARI_DRISHTI_V1_certification.json
FROM SCRATCH on every run. Gates: A table integrity; B combinatorial
12x12 exhaustion; C external oracle (PyJHora graha_drishti_from_chart
fed OUR certified D1 placements for the 11-case holdout; pure
combinatorics, zero categorical tolerance across the seven classical
grahas; the oracle's 7th-aspect-for-nodes convention is the approved
AS-B variant divergence and is recorded, not compared); D independent
validator. Exit 0 = PASS, 3 = FAIL.
"""

import json
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.calculations.calculations import calculate  # noqa: E402
from engine.models.birth_data import BirthData  # noqa: E402
from engine.parashari.drishti import (  # noqa: E402
    ASPECTABLE_GRAHAS,
    DRISHTI_OFFSETS,
    aspected_signs,
    parashari_drishti,
)

try:
    from jhora.horoscope.chart.house import graha_drishti_from_chart
    import importlib.metadata
    PYJHORA_VERSION = importlib.metadata.version("PyJHora")
except Exception as error:  # pragma: no cover
    print("DRISHTI CERTIFICATION FAIL: PyJHora oracle unavailable:", error)
    sys.exit(3)

HOLDOUT = [
 ("H1_london_1823", 1823, 4, 17, 3, 21, 7, 51.5074, -0.1278),
 ("H2_newyork_1900", 1900, 1, 1, 0, 0, 0, 40.7128, -74.0060),
 ("H3_sydney_1946", 1946, 6, 14, 21, 47, 53, -33.8688, 151.2093),
 ("H4_delhi_1979", 1979, 11, 11, 17, 41, 37, 28.6667, 77.2167),
 ("H5_reykjavik_1992", 1992, 2, 29, 23, 59, 59, 64.1466, -21.9426),
 ("H6_quito_2010", 2010, 7, 21, 5, 5, 5, -0.1807, -78.4678),
 ("H7_tokyo_2033", 2033, 9, 3, 11, 11, 11, 35.6762, 139.6503),
 ("H8_mumbai_2077", 2077, 12, 3, 14, 30, 27, 19.0760, 72.8777),
 ("H9_paris_2350", 2350, 1, 15, 6, 6, 6, 48.8566, 2.3522),
 ("H10_boundary_moon_a", 2025, 3, 1, 16, 21, 0, 28.6667, 77.2167),
 ("H11_boundary_moon_b", 2025, 3, 2, 11, 38, 0, 28.6667, 77.2167),
]

#: Our graha name -> pyjhora planet index (classical seven).
PYJHORA_INDEX = {"Sun": 0, "Moon": 1, "Mars": 2, "Mercury": 3,
                 "Jupiter": 4, "Venus": 5, "Saturn": 6}
PYJHORA_ALL = {**PYJHORA_INDEX, "Rahu": 7, "Ketu": 8}


def fail(message):
    print("DRISHTI CERTIFICATION FAIL:", message)
    sys.exit(3)


def gate_a_table_integrity():
    expected = {"Sun": (7,), "Moon": (7,), "Mars": (4, 7, 8),
                "Mercury": (7,), "Jupiter": (5, 7, 9), "Venus": (7,),
                "Saturn": (3, 7, 10)}
    if DRISHTI_OFFSETS != expected:
        fail("offset table drift")
    return {"planets": 7, "mismatches": 0}


def gate_b_combinatorial():
    checked = 0
    for planet, offsets in DRISHTI_OFFSETS.items():
        for sign in range(1, 13):
            expected = tuple(((sign - 1 + o - 1) % 12) + 1 for o in offsets)
            if aspected_signs(planet, sign) != expected:
                fail(f"{planet} in {sign}")
            checked += 1
    return {"planet_sign_pairs": checked, "mismatches": 0}


def gate_c_oracle():
    comparisons = 0
    for case in HOLDOUT:
        _id, year, month, day, hour, minute, second, lat, lon = case
        chart = parashari_drishti(
            BirthData(year, month, day, hour, minute, float(second), lat, lon, "UTC"))

        # Build the oracle's house_to_planet chart from OUR certified
        # D1 placements (pure combinatorics from here on).
        houses = [""] * 12
        for name, index in PYJHORA_ALL.items():
            sign_index = chart.planet_signs[name] - 1
            houses[sign_index] = (houses[sign_index] + "/" if houses[sign_index] else "") + str(index)
        asc_index = chart.ascendant_sign - 1
        houses[asc_index] = (houses[asc_index] + "/" if houses[asc_index] else "") + "L"

        arp, _ahp, app = graha_drishti_from_chart(houses)

        drishti = {d.name: d for d in chart.drishti}
        for name, index in PYJHORA_INDEX.items():
            ours_signs = sorted((s - 1) for s in drishti[name].aspected_signs)
            oracle_signs = sorted(arp[index])
            if ours_signs != oracle_signs:
                fail(f"{_id} {name}: signs {ours_signs} vs {oracle_signs}")
            ours_planets = sorted(PYJHORA_ALL[p] for p in drishti[name].aspected_planets)
            oracle_planets = sorted(set(app[index]))
            if ours_planets != oracle_planets:
                fail(f"{_id} {name}: planets {ours_planets} vs {oracle_planets}")
            comparisons += 2
    return {"cases": len(HOLDOUT), "comparisons": comparisons, "mismatches": 0,
            "node_divergence_note": (
                "oracle gives Rahu/Ketu a 7th aspect; V1 excludes node-cast "
                "aspects per approved Decision AS-B (recorded variant)")}


def gate_d_validator():
    result = subprocess.run(
        [sys.executable, str(ROOT / "validate_parashari_drishti_holdout.py")],
        capture_output=True, text=True)
    if result.returncode != 0 or "ALL INDEPENDENT DRISHTI CASES PASSED" not in result.stdout:
        fail("independent validator failed")
    return {"result": "PASS"}


def main():
    report = {
        "schema": "parashari_drishti_v1_certification",
        "adr": "ADR-0012",
        "date": str(date.today()),
        "scope": "Parashari graha drishti, full (purna) aspects; facts only",
        "decisions": {
            "AS-A": "full aspects only; sputa drishti (fractional) deferred",
            "AS-B": "no node-cast aspects in V1; variant recorded",
            "AS-C": "whole-sign inclusive counting; signs/houses/planets reported",
        },
        "oracle": {"package": "PyJHora", "version": PYJHORA_VERSION,
                   "function": "graha_drishti_from_chart (pure combinatorics on our certified placements)"},
        "gates": {
            "A_table_integrity": gate_a_table_integrity(),
            "B_combinatorial_12x12": gate_b_combinatorial(),
            "C_oracle": gate_c_oracle(),
            "D_independent_validator": gate_d_validator(),
        },
        "explicit_non_claims": [
            "sputa/fractional drishti strengths",
            "node-cast aspects (recorded variant)",
            "Jaimini rashi drishti (separate school module)",
            "Western aspects (separate module)",
            "yogas, strengths, interpretation",
        ],
        "environment": {"python": sys.version.split()[0]},
        "result": "PASS",
    }
    out = ROOT / "certification" / "PARASHARI_DRISHTI_V1_certification.json"
    out.write_text(json.dumps(report, indent=1) + "\n")
    print("=" * 60)
    print("PARASHARI_DRISHTI_V1 CERTIFICATION")
    print("=" * 60)
    for name in ("A_table_integrity", "B_combinatorial_12x12", "C_oracle", "D_independent_validator"):
        gate = dict(report["gates"][name])
        gate.pop("node_divergence_note", None)
        print(f"{name}: {gate}")
    print("archived          :", out.relative_to(ROOT))
    print("RESULT            : PASS")


if __name__ == "__main__":
    main()
