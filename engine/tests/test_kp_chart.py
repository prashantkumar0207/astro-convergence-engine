"""
KP chart-level equivalence and isolation gates (Gate 3 of ADR-KP-001).

Compares engine/kp/chart.py against the certified legacy kernel
(legacy/engine.py, oracle only) over the frozen 11-case holdout
matrix under the identical profile: KRISHNAMURTI ayanamsa, mean node,
Placidus, strict SWIEPH, same bundled ephemeris files. Longitudes
must agree within 0.001 arcsec (the certified engine-vs-legacy
agreement bound) and every SL/NL/SB/SS assignment must match exactly
(zero categorical tolerance, DECISION_LOG D-003).
"""

from pathlib import Path

import pytest

from engine.astronomy.profile import PARASHARI_LAHIRI
from engine.calculations.calculations import calculate
from engine.kp.chart import KP_CHART_BODIES, KpProfileError, kp_chart, kp_chart_from_snapshot
from engine.models.birth_data import BirthData

from legacy import engine as legacy_engine

ROOT = Path(__file__).resolve().parents[2]

HOLDOUT = [
    {"id": "H1_london_1823", "date": "1823-04-17", "time": "03:21:07", "lat": 51.5074, "lon": -0.1278},
    {"id": "H2_newyork_1900", "date": "1900-01-01", "time": "00:00:00", "lat": 40.7128, "lon": -74.0060},
    {"id": "H3_sydney_1946", "date": "1946-06-14", "time": "21:47:53", "lat": -33.8688, "lon": 151.2093},
    {"id": "H4_delhi_1979", "date": "1979-11-11", "time": "17:41:37", "lat": 28.6667, "lon": 77.2167},
    {"id": "H5_reykjavik_1992", "date": "1992-02-29", "time": "23:59:59", "lat": 64.1466, "lon": -21.9426},
    {"id": "H6_quito_2010", "date": "2010-07-21", "time": "05:05:05", "lat": -0.1807, "lon": -78.4678},
    {"id": "H7_tokyo_2033", "date": "2033-09-03", "time": "11:11:11", "lat": 35.6762, "lon": 139.6503},
    {"id": "H8_mumbai_2077", "date": "2077-12-03", "time": "14:30:27", "lat": 19.0760, "lon": 72.8777},
    {"id": "H9_paris_2350", "date": "2350-01-15", "time": "06:06:06", "lat": 48.8566, "lon": 2.3522},
    {"id": "H10_boundary_moon_a", "date": "2025-03-01", "time": "16:21:00", "lat": 28.6667, "lon": 77.2167},
    {"id": "H11_boundary_moon_b", "date": "2025-03-02", "time": "11:38:00", "lat": 28.6667, "lon": 77.2167},
]


def _arcsec(a: float, b: float) -> float:
    return abs(((a - b + 180.0) % 360.0) - 180.0) * 3600.0


def _birth(case) -> BirthData:
    year, month, day = (int(part) for part in case["date"].split("-"))
    hour, minute, second = (int(part) for part in case["time"].split(":"))
    return BirthData(year, month, day, hour, minute, float(second),
                     case["lat"], case["lon"], "UTC")


def _legacy(case):
    return legacy_engine.compute(
        case["date"], case["time"], case["lat"], case["lon"],
        ayan="KRISHNAMURTI", node="MEAN", tz="UTC",
        ephe="SWIEPH", ephe_path=str(ROOT), strict_ephe=True,
    )


def _chain_tuple(chain):
    return (chain.sign_lord, chain.nakshatra_lord, chain.sub_lord, chain.sub_sub_lord)


def _legacy_tuple(entry):
    return (entry["SL"], entry["NL"], entry["SB"], entry["SS"])


@pytest.mark.parametrize("case", HOLDOUT, ids=lambda case: case["id"])
def test_holdout_equivalence_with_certified_legacy_kernel(case):
    ours = kp_chart(_birth(case))
    theirs = _legacy(case)

    assert ours.provenance.profile_name == "kp_krishnamurti"
    assert ours.provenance.ephemeris_mode == "swieph"

    for body in ours.bodies:
        legacy_body = theirs["bodies"][body.name]
        assert _arcsec(body.longitude, legacy_body["lon_deg"]) <= 0.001, (
            f"{case['id']} {body.name} longitude"
        )
        assert _chain_tuple(body.chain) == _legacy_tuple(legacy_body), (
            f"{case['id']} {body.name} chain"
        )

    assert _arcsec(ours.ascendant.longitude, theirs["bodies"]["Ascendant"]["lon_deg"]) <= 0.001
    assert _chain_tuple(ours.ascendant.chain) == _legacy_tuple(theirs["bodies"]["Ascendant"])

    assert len(ours.cusps) == 12
    for cusp in ours.cusps:
        legacy_cusp = theirs["cusps"][str(cusp.number)]
        assert _arcsec(cusp.longitude, legacy_cusp["lon_deg"]) <= 0.001, (
            f"{case['id']} cusp {cusp.number} longitude"
        )
        assert _chain_tuple(cusp.chain) == _legacy_tuple(legacy_cusp), (
            f"{case['id']} cusp {cusp.number} chain"
        )


def test_roster_is_the_certified_legacy_roster():
    assert KP_CHART_BODIES == (
        "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
        "Rahu", "Ketu", "Uranus", "Neptune", "Pluto",
    )


def test_kp_rejects_parashari_snapshot():
    result = calculate(
        BirthData(1985, 12, 21, 14, 40, 0.0, 25.6, 85.1333, "Asia/Kolkata"),
        profile=PARASHARI_LAHIRI,
    )
    with pytest.raises(KpProfileError):
        kp_chart_from_snapshot(result.snapshot)


def test_kp_rejects_snapshot_without_provenance():
    class Bare:
        provenance = None

    with pytest.raises(KpProfileError):
        kp_chart_from_snapshot(Bare())


def test_cusp_one_equals_ascendant():
    chart = kp_chart(BirthData(1985, 12, 21, 14, 40, 0.0, 25.6, 85.1333, "Asia/Kolkata"))
    assert chart.cusps[0].longitude == chart.ascendant.longitude


def test_rahu_ketu_opposition_preserved():
    chart = kp_chart(BirthData(1985, 12, 21, 14, 40, 0.0, 25.6, 85.1333, "Asia/Kolkata"))
    body = {b.name: b for b in chart.bodies}
    assert abs(((body["Ketu"].longitude - body["Rahu"].longitude) % 360.0) - 180.0) < 1e-9
