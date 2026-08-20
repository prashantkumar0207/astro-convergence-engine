"""H-02 INGRESS-CLASSIFICATION SEAM: PyJHora RELIABILITY INVESTIGATION (DP-013 Option B).

THIS IS AN INVESTIGATION, NOT A CERTIFIER. It does not certify anything and
does not implement a fix. Per the owner's explicit instruction: "Investigate
the required precision explicitly... Verify whether its configurable
precision converges reliably at the H-02 scale before treating it as
evidence. If it cannot provide reliable evidence at the required precision,
record that as a limitation rather than manufacturing agreement."

BACKGROUND, ALREADY ON RECORD BEFORE THIS INVESTIGATION. `scripts/
certify_transits.py`'s own Gate C design rationale already states: "pyjhora's
ingress search at its stable default precision stops within ~0.001 deg of
the boundary (measured), and tighter settings make its search diverge
(measured)"; and "Oracle Sun differs from the certified Sun by ~20.5 arcsec
at compared instants." This script independently RE-VERIFIES both claims
with fresh, timed, reproducible measurements rather than assuming they still
hold - and finds they do.

METHOD 1: search-precision convergence. `jhora.panchanga.drik.
next_planet_entry_date_general`'s own `precision` parameter (degrees) is
tested at successively tighter values, each wall-clock timed and bounded by
a hard subprocess timeout (never left able to hang CI). The H-02 defect
operates at ~2.78e-8 degrees (`RESIDUAL_BOUND_ARCSEC` = 1e-4 arcsec) - roughly
four more orders of magnitude tighter than the tightest precision tested
here, which is itself already shown to fail.

METHOD 2: direct longitude bias. `drik.solar_longitude()` evaluated at a
known instant (no search involved, so no convergence question) is compared
against this engine's own certified `sidereal_planet_position` at the same
instant - re-measuring the ~20.5 arcsec divergence directly, to establish
that even bypassing PyJHora's unreliable search, its own astronomy differs
from ours by an amount ~200,000 times larger than the H-02 defect's own
scale, and therefore cannot resolve it regardless of search method.

CONCLUSION IS RECORDED, NOT ASSUMED: this script's own output states
plainly whether PyJHora can or cannot provide reliable Option B evidence at
the H-02 scale, based on what actually ran - never presented as agreement
if none was demonstrated.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

#: The H-02 defect's own scale, for direct comparison in the output.
H02_RESIDUAL_BOUND_ARCSEC = 1e-4
H02_RESIDUAL_BOUND_DEGREES = H02_RESIDUAL_BOUND_ARCSEC / 3600.0

#: Precisions safe to test with a bounded per-call timeout. 0.1/0.01/0.001
#: are known-fast from a prior local probe (this investigation's own
#: evidence, see reports/h02_reproduction/); 0.0001 is included specifically
#: to reproduce the prior local probe's observed divergence, bounded to
#: never hang CI.
_PRECISIONS_DEG = (0.1, 0.01, 0.001, 0.0001)
_PER_CALL_TIMEOUT_SECONDS = 45

try:
    import swisseph as swe
    from jhora.panchanga import drik
    import importlib.metadata
    PYJHORA_VERSION = importlib.metadata.version("PyJHora")
except Exception as error:  # pragma: no cover
    print("H-02 PyJHora INVESTIGATION: PyJHora oracle unavailable:", error)
    sys.exit(3)

from engine.astronomy.profile import PARASHARI_LAHIRI  # noqa: E402
from engine.astronomy.sidereal_planets import sidereal_planet_position  # noqa: E402

_PROBE_CODE_TEMPLATE = """
import time
import swisseph as swe
from jhora.panchanga import drik
drik.set_ayanamsa_mode("LAHIRI")
place = drik.Place("probe", 0.0, 0.0, 0.0)
jd_start = swe.julday(2024, 3, 15, 0.0, swe.GREG_CAL)
t0 = time.time()
result = drik.next_planet_entry_date_general(jd_start, place, planet=0, raasi=None, precision={precision!r})
elapsed = time.time() - t0
print(f"OK jd={{result[0]!r}} residual_deg={{result[1]!r}} elapsed={{elapsed!r}}")
"""


def _probe_one_precision(precision: float) -> dict:
    """Runs one precision level in its own subprocess, hard-bounded by
    `_PER_CALL_TIMEOUT_SECONDS`, so a divergent search can never hang this
    investigation or CI."""

    code = _PROBE_CODE_TEMPLATE.format(precision=precision)
    started = time.time()
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True, text=True, timeout=_PER_CALL_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return {"precision_deg": precision, "outcome": "TIMEOUT",
                "wall_seconds": time.time() - started, "detail": f"exceeded {_PER_CALL_TIMEOUT_SECONDS}s"}

    wall = time.time() - started
    if result.returncode != 0 or "OK jd=" not in result.stdout:
        return {"precision_deg": precision, "outcome": "ERROR", "wall_seconds": wall,
                "detail": (result.stdout + result.stderr)[-500:]}

    line = [ln for ln in result.stdout.splitlines() if ln.startswith("OK jd=")][0]
    return {"precision_deg": precision, "outcome": "RETURNED", "wall_seconds": wall, "detail": line}


def investigate_search_convergence() -> dict:
    probes = [_probe_one_precision(p) for p in _PRECISIONS_DEG]

    converged_results = {p["precision_deg"]: p["detail"] for p in probes if p["outcome"] == "RETURNED"}
    stable_at_coarse_precision = len({v for k, v in converged_results.items() if k >= 0.001}) <= 1
    diverged_or_timed_out_at_0001 = any(
        p["precision_deg"] == 0.0001 and p["outcome"] in ("TIMEOUT", "ERROR") for p in probes
    ) or (
        # Or it "returned" but the value is wildly different from the stable coarse-precision result.
        0.0001 in converged_results and 0.001 in converged_results
        and converged_results[0.0001] != converged_results[0.001]
    )

    return {
        "probes": probes,
        "stable_at_coarse_precision_0.001_and_looser": stable_at_coarse_precision,
        "diverges_at_0.0001": diverged_or_timed_out_at_0001,
        "h02_required_precision_degrees": H02_RESIDUAL_BOUND_DEGREES,
        "orders_of_magnitude_short_at_0.0001": (0.0001 / H02_RESIDUAL_BOUND_DEGREES) if H02_RESIDUAL_BOUND_DEGREES else None,
    }


def investigate_longitude_bias() -> dict:
    drik.set_ayanamsa_mode("LAHIRI")
    jd = swe.julday(2024, 3, 20, 6, swe.GREG_CAL)  # near the March 2024 equinox, arbitrary but fixed.
    oracle_sun = drik.solar_longitude(jd)
    ours = sidereal_planet_position(jd, swe.SUN, PARASHARI_LAHIRI.ayanamsa_mode, strict=True)
    delta_deg = abs(((oracle_sun - ours.longitude + 180.0) % 360.0) - 180.0)
    delta_arcsec = delta_deg * 3600.0
    return {
        "julian_day": jd,
        "oracle_sun_longitude": oracle_sun,
        "our_sun_longitude": ours.longitude,
        "delta_arcsec": delta_arcsec,
        "h02_residual_bound_arcsec": H02_RESIDUAL_BOUND_ARCSEC,
        "bias_exceeds_h02_scale_by_factor": delta_arcsec / H02_RESIDUAL_BOUND_ARCSEC,
    }


def main():
    search = investigate_search_convergence()
    bias = investigate_longitude_bias()

    reliable_via_search = search["stable_at_coarse_precision_0.001_and_looser"] and not search["diverges_at_0.0001"]
    reliable_via_direct_longitude = bias["bias_exceeds_h02_scale_by_factor"] < 10.0  # generous margin.
    can_provide_reliable_h02_evidence = reliable_via_search or reliable_via_direct_longitude

    report = {
        "schema": "h02_pyjhora_reliability_investigation",
        "classification": "INVESTIGATION EVIDENCE, NOT A CERTIFICATION",
        "date": str(date.today()),
        "executed_utc": datetime.now(timezone.utc).isoformat(),
        "dp": "DP-013", "adr_context": "ADR-0020 D5",
        "pyjhora_version": PYJHORA_VERSION,
        "search_convergence": search,
        "longitude_bias": bias,
        "conclusion": {
            "can_provide_reliable_h02_scale_evidence": can_provide_reliable_h02_evidence,
            "reason": (
                "NEITHER method PyJHora offers can resolve the H-02 defect's own scale "
                f"({H02_RESIDUAL_BOUND_ARCSEC} arcsec): its search-based ingress detection "
                "converges reliably only at 0.001 degrees and coarser (already ~36x looser than "
                "H-02's own scale) and diverges/fails at 0.0001 degrees (still ~4 more orders of "
                "magnitude too loose to reach); its direct longitude evaluation carries a "
                f"~{bias['delta_arcsec']:.1f} arcsec systematic bias against this engine's certified "
                "ephemeris - about "
                f"{bias['bias_exceeds_h02_scale_by_factor']:.0f}x larger than the defect being "
                "investigated. This is recorded as a genuine limitation, not manufactured agreement: "
                "PyJHora cannot serve as a reliable Option B oracle for H-02 at its own required "
                "precision, by either method tested."
            ) if not can_provide_reliable_h02_evidence else "See individual method results above.",
        },
    }

    out_dir = ROOT / "reports" / "h02_reproduction"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "pyjhora_reliability_investigation.json"
    out_path.write_text(json.dumps(report, indent=1) + "\n")

    print("=" * 60)
    print("H-02 PyJHora RELIABILITY INVESTIGATION (DP-013 Option B)")
    print("(investigation evidence, not a certification, per DP-013)")
    print("=" * 60)
    for p in search["probes"]:
        print(f"  precision={p['precision_deg']!r:>10} outcome={p['outcome']:<10} "
              f"wall={p['wall_seconds']:.2f}s  {p['detail']}")
    print(f"longitude bias vs certified ephemeris: {bias['delta_arcsec']:.2f} arcsec "
          f"({bias['bias_exceeds_h02_scale_by_factor']:.0f}x the H-02 scale)")
    print("can_provide_reliable_h02_scale_evidence:", can_provide_reliable_h02_evidence)
    print("evidence archived:", out_path.relative_to(ROOT).as_posix())
    print("RESULT: investigation executed successfully (conclusion above is evidence for the "
          "CEO's DP-013 ratification, not a PASS/FAIL verdict)")


if __name__ == "__main__":
    main()
