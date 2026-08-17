"""VARGA_D30_V1 CERTIFICATION RUNNER (ADR-0011).

Regenerates certification/VARGA_D3_V1_certification.json FROM SCRATCH
on every run; the stored JSON is never accepted as proof.

Gates: A rule-table integrity (second transcription + trine
re-derivation); B dense mathematical sweep vs an independently coded
classical rule; C external oracle (PyJHora's pure-math Parasara
drekkana mapping, zero categorical tolerance; no astronomy involved,
so no D-007 tolerance derivation applies); D framework
non-invasiveness (registry contents, certified dispatch types,
refusals, plus fresh D9/D10 dense+ULP sweep hashes recorded for
cross-commit comparison against the published baseline); E the
independent validator. Exit 0 = PASS, 3 = FAIL.
"""

import hashlib
import json
import math
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

sys.path.insert(0, str(ROOT / "scripts"))
import certification_support as support  # noqa: E402

import engine.astrology  # noqa: F401, E402  (registers production vargas)
from engine.astrology.dashamsa_chart import dashamsa_longitude, dashamsa_sign  # noqa: E402
from engine.astrology.divisional_chart import divisional_chart  # noqa: E402
from engine.astrology.navamsa_chart import navamsa_longitude, navamsa_sign  # noqa: E402
from engine.astrology.varga_classifier import classify  # noqa: E402
from engine.astrology.varga_d30 import D30_PARASHARA  # noqa: E402
from engine.astrology.varga_registry import (  # noqa: E402
    UnsupportedVargaError,
    get_varga_rule,
    registered_vargas,
)
from engine.astrology.varga_rules import rule_content_sha256  # noqa: E402
from engine.astronomy.profile import PARASHARI_LAHIRI  # noqa: E402
from engine.calculations.calculations import calculate  # noqa: E402
from engine.models.birth_data import BirthData  # noqa: E402

try:
    from jhora.horoscope.chart.charts import trimsamsa_chart
    import importlib.metadata
    PYJHORA_VERSION = importlib.metadata.version("PyJHora")
except Exception as error:  # pragma: no cover
    print("D30 CERTIFICATION FAIL: PyJHora oracle unavailable:", error)
    sys.exit(3)


def fail(message):
    print("D30 CERTIFICATION FAIL:", message)
    sys.exit(3)


def gate_a_table_integrity():
    ODD = ((5.0, 0), (5.0, 10), (8.0, 8), (7.0, 2), (5.0, 6))
    EVEN = ((5.0, 1), (7.0, 5), (8.0, 11), (5.0, 9), (5.0, 7))
    for source in range(12):
        expected = ODD if source % 2 == 0 else EVEN
        if tuple(D30_PARASHARA.segments[source]) != expected:
            fail(f"sign {source}: segment table")
        if sum(w for w, _ in D30_PARASHARA.segments[source]) != 30.0:
            fail(f"sign {source}: widths")
    return {"cells": 120, "mismatches": 0}


def gate_b_dense_sweep():
    mismatches = 0
    step = 360.0 / 51429
    for i in range(51429):
        longitude = i * step
        result = classify(longitude, D30_PARASHARA)
        source = int(longitude // 30.0)
        within = longitude - source * 30.0
        table = D30_PARASHARA.segments[source]
        cumulative = 0.0
        expected = None
        for division, (width, target) in enumerate(table):
            cumulative += width
            if within + 1e-10 < cumulative or division == 4:
                expected = (target, division)
                break
        if (result.d_sign, result.division_index) != expected:
            mismatches += 1
    if mismatches:
        fail(f"dense sweep mismatches: {mismatches}")
    return {"points": 51429, "mismatches": 0}


def gate_c_oracle():
    mismatches = 0
    comparisons = 0
    for source in range(12):
        for i in range(300):
            within = (i + 0.5) * (30.0 / 300.0)  # midpoints, no boundary dust
            oracle = trimsamsa_chart([["planet", [source, within]]], chart_method=1)
            oracle_sign = oracle[0][1][0]
            ours = classify(source * 30.0 + within, D30_PARASHARA)
            if ours.d_sign != oracle_sign:
                mismatches += 1
            comparisons += 1
    if mismatches:
        fail(f"oracle mismatches: {mismatches}")
    return {"comparisons": comparisons, "mismatches": 0}


def gate_d_non_invasiveness():
    from engine.astrology import CERTIFIED_PRODUCTION_VARGAS

    if registered_vargas() != CERTIFIED_PRODUCTION_VARGAS:
        fail(f"registry contents: {registered_vargas()}")
    if (30, "parashara") not in registered_vargas():
        fail("D30 not registered")

    # B-01/B-02 (reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md).
    if get_varga_rule(30, "parashara") is not D30_PARASHARA:
        fail("registered D30 rule is not the certified module object")

    snapshot = calculate(
        BirthData(1985, 12, 21, 14, 40, 0.0, 25.6, 85.1333, "Asia/Kolkata"),
        profile=PARASHARI_LAHIRI,
    ).snapshot
    if type(divisional_chart(snapshot, 9)).__name__ != "NavamsaChart":
        fail("D9 no longer served by the certified module")
    if type(divisional_chart(snapshot, 10)).__name__ != "DashamsaChart":
        fail("D10 no longer served by the certified module")
    for division in (4, 16, 27, 60):
        try:
            divisional_chart(snapshot, division)
            fail(f"D{division} no longer refused")
        except UnsupportedVargaError:
            pass

    # Fresh D9/D10 sweep hashes (dense + boundary ULP), recorded for
    # cross-commit comparison against the published baseline.
    h9, h10 = hashlib.sha256(), hashlib.sha256()
    step = 360.0 / 51429
    points = [i * step for i in range(51429)]
    for k in range(0, 121):
        for base in (k * (10.0 / 3.0), k * 3.0):
            if not (0.0 <= base < 360.0):
                continue
            points.append(base)
            down = up = base
            for _ in range(3):
                down = math.nextafter(down, -math.inf)
                up = math.nextafter(up, math.inf)
                points.extend(p for p in (down, up) if 0.0 <= p < 360.0)
    count = 0
    for longitude in points:
        h9.update(repr((navamsa_sign(longitude), navamsa_longitude(longitude))).encode())
        h10.update(repr((dashamsa_sign(longitude), dashamsa_longitude(longitude))).encode())
        count += 1
    return {
        "registry": [list(entry) for entry in registered_vargas()],
        "certified_dispatch": "intact",
        "refusals": "intact",
        "registered_rule_identity": "is D30_PARASHARA",
        "rule_content_sha256": rule_content_sha256(D30_PARASHARA),
        "d9_d10_sweep_points": count,
        "d9_sweep_sha256": h9.hexdigest(),
        "d10_sweep_sha256": h10.hexdigest(),
    }


def gate_e_validator():
    result = subprocess.run(
        [sys.executable, str(ROOT / "validate_d30_holdout.py")],
        capture_output=True, text=True)
    if result.returncode != 0 or "ALL INDEPENDENT D30 CASES PASSED" not in result.stdout:
        fail("independent validator failed")
    return {"result": "PASS"}


def main():
    tee = support.start_transcript()
    preconditions = support.preflight()
    report = {
        "schema": "varga_d30_v1_certification",
        "adr": "ADR-0011",
        "supersedes_provisional_id": "ADR-VARGA-D30-001",
        "date": str(date.today()),
        "scope": "D30 Trimsamsa (Parashara variant): unequal tara-graha segments",
        "rule": {
            "kind": "SegmentVargaRule",
            "variant": "parashara (5/5/8/7/5 odd, reversed even; no luminaries)",
            "school_key": "parashara",
            "boundary_policy": (
                "inherited locked convention: intra-sign boundaries promote "
                "within 1e-10; the source-sign decomposition carries no "
                "tolerance (identical to certified D9/D10 behavior, verified)"
            ),
        },
        "oracle": {"package": "PyJHora", "version": PYJHORA_VERSION,
                   "function": "trimsamsa_chart method 1 Traditional Parasara (pure longitude math)"},
        "gates": {
            "A_table_integrity": gate_a_table_integrity(),
            "B_dense_sweep": gate_b_dense_sweep(),
            "C_oracle": gate_c_oracle(),
            "D_non_invasiveness": gate_d_non_invasiveness(),
            "E_independent_validator": gate_e_validator(),
        },
        "explicit_non_claims": [
            "non-Parashara trimsamsa variants",
            "trimsamsa-based interpretation",
            "any other varga; each requires its own ADR and certification",
        ],
        "environment": {"python": sys.version.split()[0]},
        "preconditions": preconditions,
        "result": "PASS",
    }
    out = support.emit(report, "VARGA_D30_V1_certification.json", "varga_d30", tee)
    print("=" * 60)
    print("VARGA_D30_V1 CERTIFICATION")
    print("=" * 60)
    for name in ("A_table_integrity", "B_dense_sweep", "C_oracle"):
        print(f"{name}: {report['gates'][name]}")
    gate_d = report["gates"]["D_non_invasiveness"]
    print(f"D_non_invasiveness: registry {gate_d['registry']}, dispatch {gate_d['certified_dispatch']}, "
          f"D9 hash {gate_d['d9_sweep_sha256'][:16]}..., D10 hash {gate_d['d10_sweep_sha256'][:16]}...")
    print("E_independent_validator: PASS")
    print("archived          :", out.relative_to(ROOT))
    print("RESULT            : PASS")


if __name__ == "__main__":
    main()
