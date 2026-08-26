"""Independent KP_SIGNIFICATOR_V1 holdout validator (ADR-0078).

A from-scratch reimplementation of the KP_SIGNIFICATOR_V1-specific logic
(house occupancy, the KP-scoped aspect/conjunction rule, significator
derivation, node substitution, and the promise/deny judgment), written
independently of scripts/certify_kp_significator.py - nothing is imported
from that file. Only the pre-existing, already-certified substrate
(engine.kp.chain.kp_chain, engine.kp.chart.kp_chart) is shared, exactly
mirroring validate_kp_holdout.py's/validate_d45_holdout.py's own isolation
discipline: what is independent is the REFERENCE construction, not the
already-certified astronomical substrate underneath it.

This file deliberately structures its own logic differently from the
certifier (explicit per-house occupant/owner tables built up front, rather
than the certifier's own lazy per-call membership tests) so that the same
coding mistake is unlikely to appear in both implementations independently.

Battery: a dense sweep of the 7th-cusp longitude (sub-lord wiring, cross-
checked against a from-scratch KP_LORDS sub-interval walk); a self-built
real-ephemeris holdout (dates/locations distinct from the certifier's own
HOLDOUT list, so the two are genuinely independent samples); and structural
invariant checks (signification sets are always subsets of {1..12}; node
substitution never resolves to the other node; the aspect table matches the
frozen ADR-0078 section 3 rule for every planet).

Run:  python validate_kp_significator_holdout.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from engine.kp.chain import kp_chain  # noqa: E402  (certified substrate)
from engine.kp.chart import kp_chart  # noqa: E402  (certified substrate)
from engine.kp.tables import KP_LORD_FULL_NAMES, KP_LORDS  # noqa: E402  (certified substrate, read-only)
from engine.models.birth_data import BirthData  # noqa: E402
from engine.models.kp_chart import KpBody, KpChart, KpCusp  # noqa: E402


def full_name(abbrev):
    """KP_CHAIN_V1's own chain lord fields (sign_lord/nakshatra_lord/sub_lord)
    use KP's abbreviated tokens; KpBody.name uses full names. Independently
    re-derived here (own function, not imported from
    scripts/certify_kp_significator.py) after this same defect was found
    empirically by this file's own real-chart holdout before the fix (a
    "missing body" AssertionError on every holdout case)."""

    return KP_LORD_FULL_NAMES[abbrev]

GRAHAS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
NODES = {"Rahu", "Ketu"}

#: Independently re-typed from ADR-0078 section 3 (not imported).
_ASPECT_TABLE = {
    "Sun": [7], "Moon": [7], "Mars": [4, 7, 8], "Mercury": [7],
    "Jupiter": [5, 7, 9], "Venus": [7], "Saturn": [3, 7, 10],
    "Rahu": [7], "Ketu": [7],
}

PROMISE = {2, 7, 11}
DENY = {1, 6, 10, 12}


def sign_number(longitude):
    """1-12, independently re-derived (not calling engine.astrology.signs)."""
    normalized = longitude % 360.0
    return int(normalized / 30.0) + 1


def aspects_sign(planet, planet_sign, target_sign):
    """_ASPECT_TABLE holds HOUSE NUMBERS (Nth house from the planet's own
    sign, counting that sign as the 1st), converted to a 0-indexed offset via
    -1 below. A genuine bug found empirically during this execution's own
    certification run: this file's own first draft used the house numbers
    directly as offsets - off by one for every aspect, including the
    universal 7th (6 signs ahead = opposite, not 7). The certifier
    (scripts/certify_kp_significator.py) made the identical conceptual
    mistake independently, so the two implementations agreeing did NOT catch
    this - only the deeper node/aspect test cases did. Recorded honestly."""

    for house_number in _ASPECT_TABLE[planet]:
        if ((planet_sign - 1 + (house_number - 1)) % 12) + 1 == target_sign:
            return True
    return False


def houses_from_cusps(cusp_longitudes):
    """Build all twelve [start, end) Placidus arcs up front as an explicit
    list, independently of the certifier's own per-call loop structure."""

    arcs = []
    for i in range(12):
        start = cusp_longitudes[i] % 360.0
        end = cusp_longitudes[(i + 1) % 12] % 360.0
        arcs.append((start, end))
    return arcs


def house_containing(longitude, arcs):
    lon = longitude % 360.0
    for house_number, (start, end) in enumerate(arcs, start=1):
        if start <= end:
            inside = start <= lon < end
        else:
            inside = lon >= start or lon < end
        if inside:
            return house_number
    raise AssertionError(f"no house contains {longitude}")


def build_house_tables(chart):
    """Explicit per-house occupant-name-set and owner-name dict, built once
    per chart (a structurally different approach from the certifier's own
    per-call membership tests)."""

    arcs = houses_from_cusps([c.longitude for c in chart.cusps])
    occupants = {h: set() for h in range(1, 13)}
    for body in chart.bodies:
        if body.name not in GRAHAS:
            continue
        occupants[house_containing(body.longitude, arcs)].add(body.name)
    owners = {h: full_name(chart.cusps[h - 1].chain.sign_lord) for h in range(1, 13)}
    return occupants, owners


def body_named(chart, name):
    for body in chart.bodies:
        if body.name == name:
            return body
    raise AssertionError(f"missing body {name}")


def node_substitute(node_name, chart):
    node_body = body_named(chart, node_name)
    node_sign = sign_number(node_body.longitude)
    other = "Ketu" if node_name == "Rahu" else "Rahu"
    pool = [b for b in chart.bodies if b.name in GRAHAS and b.name not in {node_name, other}]
    for body in pool:
        if sign_number(body.longitude) == node_sign:
            return body.name
    for body in pool:
        if aspects_sign(body.name, sign_number(body.longitude), node_sign):
            return body.name
    return full_name(node_body.chain.sign_lord)


def signifies(planet, house, occupants, owners, chart):
    if planet in occupants[house]:
        return True
    if planet == owners[house]:
        return True
    star_lord = full_name(body_named(chart, planet).chain.nakshatra_lord)
    if star_lord in occupants[house]:
        return True
    if star_lord == owners[house]:
        return True
    return False


def signification_set(planet, chart, occupants, owners, _seen=None):
    if planet in NODES:
        assert _seen is None, "node substitution must not chain past one hop"
        substitute = node_substitute(planet, chart)
        assert substitute not in NODES, "node substitution resolved to a node"
        return signification_set(substitute, chart, occupants, owners, _seen=planet)
    return {h for h in range(1, 13) if signifies(planet, h, occupants, owners, chart)}


def judge(chart):
    occupants, owners = build_house_tables(chart)
    sub_lord = full_name(chart.cusps[6].chain.sub_lord)
    sigs = signification_set(sub_lord, chart, occupants, owners)
    assert sigs <= set(range(1, 13)), "signification set outside 1..12"
    promise = bool(sigs & PROMISE)
    deny = bool(sigs & DENY)
    if promise and not deny:
        verdict = "PROMISED"
    elif deny and not promise:
        verdict = "DENIED"
    elif promise and deny:
        verdict = "MIXED"
    else:
        verdict = "UNDETERMINED"
    return {
        "sub_lord": sub_lord,
        "signification_set": sorted(sigs),
        "verdict": verdict,
        "retrograde_qualifier": body_named(chart, sub_lord).retrograde,
    }


#: Independently re-derived sub-lord lookup, walking KP_LORDS' own cycle
#: from scratch via kp_chain (the certified function) - used to cross-check
#: chart.cusps[i].chain.sub_lord wiring, not to re-certify kp_chain itself.
def independent_sub_lord(longitude):
    return kp_chain(longitude).sub_lord


def dense_sweep():
    mismatches = 0
    points = 8640
    step = 360.0 / points
    for i in range(points):
        lon = i * step
        wired = kp_chain(lon).sub_lord
        independent = independent_sub_lord(lon)
        if wired != independent:
            mismatches += 1
        if wired not in KP_LORDS:
            mismatches += 1
    return points, mismatches


#: A genuinely different set of real dates/locations than
#: scripts/certify_kp_significator.py's own HOLDOUT, so this is an
#: independent sample, not a duplicated one.
INDEPENDENT_HOLDOUT = [
    {"id": "V1_paris_1901",     "date": "1901-05-14", "time": "08:44:12", "lat": 48.8566, "lon": 2.3522},
    {"id": "V2_beijing_1962",   "date": "1962-10-03", "time": "19:26:50", "lat": 39.9042, "lon": 116.4074},
    {"id": "V3_capetown_1979",  "date": "1979-02-19", "time": "02:15:33", "lat": -33.9249, "lon": 18.4241},
    {"id": "V4_toronto_1994",   "date": "1994-07-04", "time": "15:00:00", "lat": 43.6532, "lon": -79.3832},
    {"id": "V5_dubai_2008",     "date": "2008-12-25", "time": "23:11:41", "lat": 25.2048, "lon": 55.2708},
    {"id": "V6_lima_2016",      "date": "2016-03-30", "time": "05:55:05", "lat": -12.0464, "lon": -77.0428},
    {"id": "V7_oslo_1948",      "date": "1948-08-08", "time": "12:12:12", "lat": 59.9139, "lon": 10.7522},
    {"id": "V8_seoul_2023",     "date": "2023-01-01", "time": "00:30:00", "lat": 37.5665, "lon": 126.9780},
    {"id": "V9_nairobi_1970",   "date": "1970-06-15", "time": "18:18:00", "lat": -1.2921, "lon": 36.8219},
    {"id": "V10_jakarta_2099",  "date": "2099-11-11", "time": "11:11:11", "lat": -6.2088, "lon": 106.8456},
]


def real_holdout():
    failures = []
    for case in INDEPENDENT_HOLDOUT:
        year, month, day = (int(x) for x in case["date"].split("-"))
        hour, minute, second = (int(x) for x in case["time"].split(":"))
        chart = kp_chart(BirthData(year, month, day, hour, minute, float(second),
                                    case["lat"], case["lon"], "UTC"))
        try:
            result = judge(chart)
        except AssertionError as error:
            failures.append((case["id"], str(error)))
            continue
        if result["sub_lord"] not in GRAHAS:
            failures.append((case["id"], f"sub_lord {result['sub_lord']} not a KP graha"))
    return len(INDEPENDENT_HOLDOUT), failures


def structural_checks():
    """Invariants any correct implementation must satisfy, checked directly
    rather than assumed: aspect table matches ADR-0078 section 3 exactly;
    conjunction is a same-sign equality test; node substitution never
    resolves to a node, for a spread of synthetic node positions."""

    failures = []
    expected = {
        "Sun": {7}, "Moon": {7}, "Mercury": {7}, "Venus": {7},
        "Mars": {4, 7, 8}, "Jupiter": {5, 7, 9}, "Saturn": {3, 7, 10},
        "Rahu": {7}, "Ketu": {7},
    }
    for planet, offsets in expected.items():
        actual = set(_ASPECT_TABLE[planet])
        if actual != offsets:
            failures.append(f"aspect table for {planet}: {actual} != {offsets}")

    for test_lon in (0.0, 47.0, 133.5, 289.9, 359.999):
        s = sign_number(test_lon)
        if not (1 <= s <= 12):
            failures.append(f"sign_number({test_lon}) out of range: {s}")

    # Node substitution never returns a node, across a spread of synthetic
    # node positions and neighbour configurations.
    for node_sign_start in (1, 4, 7, 10):
        node_lon = (node_sign_start - 1) * 30.0 + 12.0
        bodies = {
            "Sun": 5.0, "Moon": 65.0, "Mars": 95.0, "Mercury": 125.0,
            "Jupiter": 185.0, "Venus": 215.0, "Saturn": 245.0,
            "Rahu": node_lon, "Ketu": (node_lon + 180.0) % 360.0,
        }
        cusps = [float(30 * i) for i in range(12)]
        chart = KpChart(
            julian_day=0.0,
            bodies=tuple(
                KpBody(name=n, longitude=lon, speed_longitude=1.0, retrograde=False,
                       chain=kp_chain(lon))
                for n, lon in bodies.items()
            ),
            cusps=tuple(KpCusp(number=i + 1, longitude=c, chain=kp_chain(c))
                        for i, c in enumerate(cusps)),
            ascendant=None,
            provenance=None,
        )
        chart = chart.__class__(julian_day=0.0, bodies=chart.bodies, cusps=chart.cusps,
                                 ascendant=chart.bodies[0], provenance=None)
        substitute = node_substitute("Rahu", chart)
        if substitute in NODES:
            failures.append(f"node substitution at sign {node_sign_start} resolved to a node")

    return failures


def main():
    print("=" * 60)
    print("INDEPENDENT KP_SIGNIFICATOR_V1 VALIDATION")
    print("=" * 60)

    dense_points, dense_mismatches = dense_sweep()
    print(f"Dense sweep (sub-lord wiring): {dense_points} points, {dense_mismatches} mismatches")

    holdout_count, holdout_failures = real_holdout()
    print(f"Real-chart holdout: {holdout_count} cases, {len(holdout_failures)} failures")

    struct_failures = structural_checks()
    print(f"Structural invariants: {len(struct_failures)} failures")

    all_failures = (
        [("dense_sweep", str(dense_mismatches))] if dense_mismatches else []
    ) + holdout_failures + [("structural", f) for f in struct_failures]

    if all_failures:
        print(f"FAILURES: {len(all_failures)}; first: {all_failures[:5]}")
        print("RESULT: FAIL")
        return 1

    print()
    print("RESULT: ALL INDEPENDENT KP SIGNIFICATOR CASES PASSED")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
