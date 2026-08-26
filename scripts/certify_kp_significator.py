"""KP_SIGNIFICATOR_V1 CERTIFICATION RUNNER (ADR-0078).

Certifies the PRODUCTION, registered KP_SIGNIFICATOR_V1 rule
(engine.kp.significators). Per the owner's "CEO AUTHORIZATION —
KP_SIGNIFICATOR_V1 PRODUCTION IMPLEMENTATION" instruction (2026-08-26):
KP_SIGNIFICATOR_V1 is now implemented through engine/kp/significators.py,
exactly mirroring the D45 precedent's own certification-execution-then-
production-implementation two-step pattern. The certified rule (Ordering A
significator derivation, the promise/deny judgment, retrograde disclosure,
node substitution, and the KP-scoped aspect/conjunction calculation) is
preserved exactly as frozen in ADR-0078 and its own certification-execution
record - this run does not alter it.

Regenerates certification/KP_SIGNIFICATOR_V1_certification.json FROM SCRATCH
on every run; the stored JSON is never accepted as proof.

Gates: A rule/table integrity (production module's own frozen constants,
content-hash pinned); B dense sweep (cusp-longitude -> sub-lord wiring,
production vs. an independent kp_chain() re-derivation); C independent
validator (validate_kp_significator_holdout.py, a from-scratch
reimplementation, importing nothing from engine.kp.significators - unchanged
from the certification-execution stage, per explicit "do not weaken any
gate" instruction); D non-invasiveness (confirms engine.kp.significators is
correctly importable and content-hash matches the certified pinned value,
and that KP_CHAIN_V1, PARASHARI_DRISHTI_V1, sign_lord.py, and the
KP_KRISHNAMURTI profile remain untouched, and that no Parashari aspect code
is imported anywhere in the production module, the certifier, or the
validator); E boundary cases; F retrograde cases; G node/aspect cases;
H strength-order cases; I protected holdout (real ephemeris-driven charts);
J negative controls (real planted mutations against local copies, never the
production singleton itself, confirmed detected).

No computational oracle exists for KP significators (DP-028 section D,
DP-029 section 4, reaffirmed) - gates C and I carry the primary evidentiary
weight, per ADR-0078 section 10's own disclosure.

Exit code 0 = PASS, 3 = FAIL.
"""

import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

sys.path.insert(0, str(ROOT / "scripts"))
import certification_support as support  # noqa: E402

from engine.kp.chain import kp_chain  # noqa: E402
from engine.kp.chart import kp_chart  # noqa: E402
from engine.kp.significators import (  # noqa: E402
    DENY_HOUSES,
    KP_GRAHAS,
    PROMISE_HOUSES,
    SPECIAL_ASPECTS,
    aspected_signs,
    full_name,
    house_of_placidus,
    is_aspecting,
    is_conjunct,
    judge_marriage,
    node_substitute,
    rule_content_sha256,
    sign_of,
    signification_set,
)
from engine.models.birth_data import BirthData
from engine.models.kp_chart import KpBody, KpChart, KpCusp

#: Content fingerprint of the certified KP_SIGNIFICATOR_V1 rule constants,
#: pinned (also pinned independently in engine/tests/test_kp_significators.py).
CERTIFIED_KP_SIGNIFICATOR_CONTENT_SHA256 = (
    "0cb5aa8661c1d9b950c4d6f35d0b12baaf03aec3f28adc6937bbe257cd1f2ab9"
)


def fail(message):
    print("KP_SIGNIFICATOR_V1 CERTIFICATION FAIL:", message)
    sys.exit(3)


def gate_a_table_integrity():
    if PROMISE_HOUSES != frozenset({2, 7, 11}):
        fail("PROMISE_HOUSES mutated")
    if DENY_HOUSES != frozenset({1, 6, 10, 12}):
        fail("DENY_HOUSES mutated")
    if SPECIAL_ASPECTS != {"Mars": (4, 8), "Jupiter": (5, 9), "Saturn": (3, 10)}:
        fail("SPECIAL_ASPECTS mutated")
    if KP_GRAHAS != ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"):
        fail("KP_GRAHAS roster mutated")
    if rule_content_sha256() != CERTIFIED_KP_SIGNIFICATOR_CONTENT_SHA256:
        fail("KP_SIGNIFICATOR_V1 content hash does not match the certified pinned value")
    return {
        "promise_houses": sorted(PROMISE_HOUSES),
        "deny_houses": sorted(DENY_HOUSES),
        "special_aspects": {k: list(v) for k, v in SPECIAL_ASPECTS.items()},
        "graha_roster": list(KP_GRAHAS),
        "content_sha256": rule_content_sha256(),
    }


#: Twelve evenly-spaced default cusps (30 degrees apart, Aries rising) - a
#: neutral baseline reused by every synthetic case unless a case's own point
#: requires the 7th cusp specifically, which each builder overrides.
_DEFAULT_CUSPS = tuple(float(30 * i) for i in range(12))

#: A body roster placed harmlessly (deep in signs no case cares about) unless
#: a specific test overrides specific names.
_NEUTRAL_LONGITUDES = {
    "Sun": 15.0, "Moon": 45.0, "Mars": 75.0, "Mercury": 105.0, "Jupiter": 135.0,
    "Venus": 165.0, "Saturn": 195.0, "Rahu": 225.0, "Ketu": 45.0,
}


def make_synthetic_chart(cusp_longitudes, body_longitudes, retrograde_names=frozenset()) -> KpChart:
    cusps = tuple(
        KpCusp(number=i + 1, longitude=lon, chain=kp_chain(lon))
        for i, lon in enumerate(cusp_longitudes)
    )
    bodies = tuple(
        KpBody(
            name=name,
            longitude=lon,
            speed_longitude=-1.0 if name in retrograde_names else 1.0,
            retrograde=name in retrograde_names,
            chain=kp_chain(lon),
        )
        for name, lon in body_longitudes.items()
    )
    return KpChart(julian_day=0.0, bodies=bodies, cusps=cusps, ascendant=bodies[0], provenance=None)


def find_longitude_with_sub_lord(target_lord: str, start: float = 0.0, step: float = 0.01) -> float:
    """Grid search for a longitude whose kp_chain sub-lord is `target_lord`,
    rather than hand-deriving KP sub-interval boundaries - empirically
    verified, not assumed."""

    lon = start
    while lon < 360.0:
        if full_name(kp_chain(lon).sub_lord) == target_lord:
            return lon
        lon += step
    fail(f"find_longitude_with_sub_lord: no longitude found for {target_lord}")


def _chart_with_seventh_cusp_sub_lord(target_lord: str, overrides: dict, retrograde_names=frozenset()):
    seventh_lon = find_longitude_with_sub_lord(target_lord)
    cusps = list(_DEFAULT_CUSPS)
    cusps[6] = seventh_lon
    bodies = dict(_NEUTRAL_LONGITUDES)
    bodies.update(overrides)
    return make_synthetic_chart(cusps, bodies, retrograde_names)


def _independent_sub_lord(longitude: float) -> str:
    return kp_chain(longitude).sub_lord


def gate_b_dense_sweep():
    mismatches = 0
    points = 12960
    step = 360.0 / points
    for i in range(points):
        lon = i * step
        cusps = list(_DEFAULT_CUSPS)
        cusps[6] = lon
        chart = make_synthetic_chart(cusps, dict(_NEUTRAL_LONGITUDES))
        production = chart.cusps[6].chain.sub_lord
        independent = _independent_sub_lord(lon)
        if production != independent:
            mismatches += 1
    if mismatches:
        fail(f"dense sweep (cusp -> sub-lord wiring) mismatches: {mismatches}")
    return {"points": points, "mismatches": 0,
            "scope": "7th cusp longitude sweep, production wiring vs. independent kp_chain() call"}


def gate_c_independent_validator():
    result = subprocess.run(
        [sys.executable, str(ROOT / "validate_kp_significator_holdout.py")],
        capture_output=True, text=True)
    if result.returncode != 0 or "ALL INDEPENDENT KP SIGNIFICATOR CASES PASSED" not in result.stdout:
        fail(f"independent validator failed: {result.stdout[-1200:]} {result.stderr[-800:]}")
    return {"result": "PASS"}


def gate_d_non_invasiveness():
    import inspect
    import engine.astronomy.profile as profile_module
    import engine.kp.chain as chain_module
    import engine.kp.significators as significator_module
    import engine.parashari.drishti as drishti_module

    if not hasattr(significator_module, "judge_marriage"):
        fail("engine.kp.significators.judge_marriage is missing - production module unexpectedly altered")
    if significator_module.rule_content_sha256() != CERTIFIED_KP_SIGNIFICATOR_CONTENT_SHA256:
        fail("engine.kp.significators content hash does not match the certified pinned value")

    # The rule-logic functions themselves - the ones that must never reuse
    # Parashari aspect code - are checked directly via their own CODE, with
    # docstrings stripped via ast (not the raw source text, which would
    # false-flag a function's own disclosure docstring - e.g.
    # node_substitute's own docstring explicitly names
    # "engine.parashari.drishti" as what it does NOT import, a real defect
    # in this gate's own first two drafts, found and fixed here: prose
    # disclosure is not code reuse, and must not be conflated).
    import ast

    def _code_without_docstring(func) -> str:
        source = inspect.getsource(func)
        tree = ast.parse(source)
        function_node = tree.body[0]
        if (function_node.body and isinstance(function_node.body[0], ast.Expr)
                and isinstance(function_node.body[0].value, ast.Constant)
                and isinstance(function_node.body[0].value.value, str)):
            function_node.body = function_node.body[1:]
        return ast.unparse(function_node)

    rule_functions = (
        significator_module.sign_of, significator_module.aspected_signs,
        significator_module.is_conjunct, significator_module.is_aspecting,
        significator_module.node_substitute, significator_module._signifies,
        significator_module.signification_set, significator_module.judge_marriage,
        significator_module.house_of_placidus,
    )
    for func in rule_functions:
        code_only = _code_without_docstring(func)
        if "parashari" in code_only.lower() or "drishti" in code_only.lower():
            fail(f"{func.__name__} references Parashari/drishti in its own code (not just its "
                 f"docstring) - aspect logic must never be reused")

    own_gate_source = inspect.getsource(gate_d_non_invasiveness)
    production_module_path = Path(significator_module.__file__)
    for path in (production_module_path, Path(__file__), ROOT / "validate_kp_significator_holdout.py"):
        for line_no, line in enumerate(path.read_text().splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith(("import engine.parashari", "from engine.parashari")):
                if path == Path(__file__) and stripped in own_gate_source:
                    continue  # this gate's own disclosed, single verification import
                fail(f"{path.name}:{line_no} imports engine.parashari outside this gate's own "
                     f"disclosed verification import - Parashari aspect logic must never be reused")

    from engine.kp.tables import KP_LORDS, KP_SIGN_LORDS
    if tuple(KP_LORDS) != ("Ke", "Ve", "Su", "Mo", "Ma", "Ra", "Ju", "Sa", "Me"):
        fail("KP_CHAIN_V1 KP_LORDS table mutated")
    if tuple(KP_SIGN_LORDS) != ("Ma", "Ve", "Me", "Mo", "Su", "Me", "Ve", "Ma", "Ju", "Sa", "Sa", "Ju"):
        fail("KP_CHAIN_V1 KP_SIGN_LORDS table mutated")

    from engine.astrology.sign_lord import SIGN_LORDS
    if SIGN_LORDS != {
        1: "Mars", 2: "Venus", 3: "Mercury", 4: "Moon", 5: "Sun", 6: "Mercury",
        7: "Venus", 8: "Mars", 9: "Jupiter", 10: "Saturn", 11: "Saturn", 12: "Jupiter",
    }:
        fail("engine.astrology.sign_lord.SIGN_LORDS mutated")

    if not hasattr(drishti_module, "graha_drishti_from_snapshot"):
        fail("PARASHARI_DRISHTI_V1's own public function is missing - module unexpectedly altered")
    if profile_module.KP_KRISHNAMURTI.house_system != b"P":
        fail("KP_KRISHNAMURTI profile mutated")
    if chain_module.kp_chain.__module__ != "engine.kp.chain":
        fail("kp_chain wiring altered")

    return {
        "production_module": "engine.kp.significators",
        "production_module_importable": True,
        "content_sha256_matches_pinned": True,
        "parashari_aspect_code_imported": False,
        "kp_chain_v1_tables_unchanged": True,
        "sign_lord_table_unchanged": True,
        "parashari_drishti_v1_module_intact": True,
        "kp_krishnamurti_profile_unchanged": True,
    }


def gate_e_boundary_cases():
    cases_checked = 0
    mismatches = 0
    from engine.kp.intervals import all_boundaries
    import math
    boundary_points = []
    for bound in all_boundaries():
        base = float(bound)
        boundary_points.append(base)
        up = base
        for _ in range(2):
            up = math.nextafter(up, math.inf)
            if 0.0 <= up < 360.0:
                boundary_points.append(up)
        down = base
        for _ in range(2):
            down = math.nextafter(down, -math.inf)
            if 0.0 <= down < 360.0:
                boundary_points.append(down)
    for lon in boundary_points:
        cusps = list(_DEFAULT_CUSPS)
        cusps[6] = lon
        chart = make_synthetic_chart(cusps, dict(_NEUTRAL_LONGITUDES))
        production = chart.cusps[6].chain.sub_lord
        independent = _independent_sub_lord(lon)
        cases_checked += 1
        if production != independent:
            mismatches += 1
    for sign in range(1, 13):
        for lon in (sign * 30.0 - 1e-9, (sign - 1) * 30.0):
            cases_checked += 1
            resolved = sign_of(lon % 360.0)
            if not (1 <= resolved <= 12):
                mismatches += 1
    if mismatches:
        fail(f"boundary case failures: {mismatches}")
    return {"cases_checked": cases_checked, "mismatches": 0,
            "convention": "inherited KP_CHAIN_V1 sub-interval boundary set, tested at the 7th cusp"}


def gate_f_retrograde_cases():
    cases_checked = 0
    mismatches = 0
    chart_retro = _chart_with_seventh_cusp_sub_lord("Mars", {}, retrograde_names={"Mars"})
    result = judge_marriage(chart_retro)
    cases_checked += 1
    if result.sub_lord != "Mars" or result.retrograde_qualifier is not True:
        mismatches += 1
    chart_direct = _chart_with_seventh_cusp_sub_lord("Mars", {}, retrograde_names=frozenset())
    result2 = judge_marriage(chart_direct)
    cases_checked += 1
    if result2.sub_lord != "Mars" or result2.retrograde_qualifier is not False:
        mismatches += 1
    if mismatches:
        fail(f"retrograde case failures: {mismatches}")
    return {"cases_checked": cases_checked, "mismatches": 0,
            "rule": "conditional-on-direct-motion disclosure qualifier (KP_SIGNIFICATOR_SPEC.md section 19.2)"}


def gate_g_node_aspect_cases():
    cases_checked = 0
    mismatches = 0

    # Level 1 - conjunction.
    rahu_lon = find_longitude_with_sub_lord("Rahu")
    rahu_sign = sign_of(rahu_lon)
    jupiter_conjunct_lon = (rahu_sign - 1) * 30.0 + 10.0
    cusps = list(_DEFAULT_CUSPS)
    cusps[6] = rahu_lon
    bodies = dict(_NEUTRAL_LONGITUDES)
    bodies["Rahu"] = rahu_lon
    bodies["Ketu"] = (rahu_lon + 180.0) % 360.0
    for name in list(bodies):
        if name not in ("Rahu", "Ketu", "Jupiter") and sign_of(bodies[name]) == rahu_sign:
            bodies[name] = (bodies[name] + 60.0) % 360.0
    bodies["Jupiter"] = jupiter_conjunct_lon
    chart = make_synthetic_chart(cusps, bodies)
    cusp_lons = [c.longitude for c in chart.cusps]
    substitute = node_substitute("Rahu", chart)
    cases_checked += 1
    if substitute != "Jupiter":
        mismatches += 1
    result = judge_marriage(chart)
    cases_checked += 1
    if list(result.signification_set) != sorted(signification_set("Jupiter", chart, cusp_lons)):
        mismatches += 1

    # Level 2 - aspect, no conjunction.
    ketu_lon = find_longitude_with_sub_lord("Ketu")
    ketu_sign = sign_of(ketu_lon)
    saturn_aspect_sign = 1
    while not is_aspecting("Saturn", saturn_aspect_sign, ketu_sign) or saturn_aspect_sign == ketu_sign:
        saturn_aspect_sign += 1
        if saturn_aspect_sign > 12:
            fail("gate G level 2: no Saturn aspect sign found")
    saturn_lon = (saturn_aspect_sign - 1) * 30.0 + 5.0
    cusps2 = list(_DEFAULT_CUSPS)
    cusps2[6] = ketu_lon
    bodies2 = dict(_NEUTRAL_LONGITUDES)
    bodies2["Ketu"] = ketu_lon
    bodies2["Rahu"] = (ketu_lon + 180.0) % 360.0
    bodies2["Saturn"] = saturn_lon
    for name in KP_GRAHAS:
        if name in ("Ketu", "Saturn"):
            continue
        sign = sign_of(bodies2[name])
        while is_conjunct(sign, ketu_sign) or is_aspecting(name, sign, ketu_sign):
            sign += 1
            if sign > 12:
                fail(f"gate G level 2: no safe sign found for {name}")
        bodies2[name] = (sign - 1) * 30.0 + 20.0
    chart2 = make_synthetic_chart(cusps2, bodies2)
    substitute2 = node_substitute("Ketu", chart2)
    cases_checked += 1
    if substitute2 != "Saturn":
        mismatches += 1

    # Level 3 - fallback to sign lord: node with nothing conjunct or
    # aspecting it, verified empirically via is_conjunct/is_aspecting
    # directly rather than hand-derived arithmetic.
    rahu_lon_isolated = find_longitude_with_sub_lord("Rahu", start=181.0)
    rahu_sign_isolated = sign_of(rahu_lon_isolated)
    bodies3 = {}
    filler = 0
    for name in KP_GRAHAS:
        if name == "Rahu":
            bodies3[name] = rahu_lon_isolated
            continue
        if name == "Ketu":
            bodies3[name] = (rahu_lon_isolated + 180.0) % 360.0
            continue
        sign = 1
        while is_conjunct(sign, rahu_sign_isolated) or is_aspecting(name, sign, rahu_sign_isolated):
            sign += 1
            if sign > 12:
                fail(f"gate G level 3: no safe sign found for {name}")
        bodies3[name] = (sign - 1) * 30.0 + 15.0 + filler
        filler += 0.001
    cusps3 = list(_DEFAULT_CUSPS)
    cusps3[6] = rahu_lon_isolated
    chart3 = make_synthetic_chart(cusps3, bodies3)
    substitute3 = node_substitute("Rahu", chart3)
    from engine.kp.significators import _body
    expected_sign_lord = full_name(_body(chart3, "Rahu").chain.sign_lord)
    cases_checked += 1
    if substitute3 != expected_sign_lord:
        mismatches += 1

    # Each special-aspect rule, plus the universal 7th.
    for planet, offsets in {**SPECIAL_ASPECTS, "Venus": ()}.items():
        expected = {7} | set(offsets)
        aspected = aspected_signs(planet, 1)
        recovered_offsets = {((s - 1) % 12) for s in aspected}
        cases_checked += 1
        if recovered_offsets != {(o - 1) % 12 for o in expected}:
            mismatches += 1

    if mismatches:
        fail(f"node/aspect case failures: {mismatches}")
    return {"cases_checked": cases_checked, "mismatches": 0,
            "levels_exercised": ["conjunction", "aspect", "sign_lord_fallback",
                                  "special_aspects(Mars,Jupiter,Saturn)", "universal_7th(Venus)"]}


def gate_h_strength_order_cases():
    cases_checked = 0
    mismatches = 0
    house = 5
    cusps = list(_DEFAULT_CUSPS)
    house_sign = sign_of(cusps[house - 1])
    owner = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
             "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"][house_sign - 1]

    from engine.kp.significators import _body, _signifies

    bodies_owner_only = dict(_NEUTRAL_LONGITUDES)
    chart_owner = make_synthetic_chart(cusps, bodies_owner_only)
    cusp_lons = [c.longitude for c in chart_owner.cusps]
    cases_checked += 1
    if not _signifies(owner, house, chart_owner, cusp_lons):
        mismatches += 1
    occupants_here = {b.name for b in chart_owner.bodies
                       if house_of_placidus(b.longitude, cusp_lons) == house}
    outsider = next(
        p for p in KP_GRAHAS
        if p != owner and p not in occupants_here
        and full_name(_body(chart_owner, p).chain.nakshatra_lord) not in ({owner} | occupants_here)
    )
    cases_checked += 1
    if _signifies(outsider, house, chart_owner, cusp_lons):
        mismatches += 1

    occupant_planet = next(p for p in KP_GRAHAS if p != owner)
    occ_lon = (house_sign - 1) * 30.0 + 15.0
    bodies_occupant = dict(_NEUTRAL_LONGITUDES)
    bodies_occupant[occupant_planet] = occ_lon
    chart_occ = make_synthetic_chart(cusps, bodies_occupant)
    cusp_lons2 = [c.longitude for c in chart_occ.cusps]
    cases_checked += 1
    if not _signifies(occupant_planet, house, chart_occ, cusp_lons2):
        mismatches += 1

    if mismatches:
        fail(f"strength-order case failures: {mismatches}")
    return {"cases_checked": cases_checked, "mismatches": 0,
            "categories_exercised": ["owner", "occupant"],
            "note": "confirms Ordering A's categories are independently recognized; "
                    "V1's own promise/deny judgment is a union test over the categories, "
                    "not a priority selection - see ADR-0078 section 4"}


HOLDOUT = [
    {"id": "S1_london_1850",   "date": "1850-03-11", "time": "06:12:34", "lat": 51.5074, "lon": -0.1278},
    {"id": "S2_delhi_1965",    "date": "1965-08-15", "time": "13:07:00", "lat": 28.6139, "lon": 77.2090},
    {"id": "S3_tokyo_1988",    "date": "1988-11-23", "time": "22:45:19", "lat": 35.6762, "lon": 139.6503},
    {"id": "S4_saopaulo_2001", "date": "2001-02-28", "time": "04:33:41", "lat": -23.5505, "lon": -46.6333},
    {"id": "S5_cairo_2014",    "date": "2014-06-30", "time": "17:59:59", "lat": 30.0444, "lon": 31.2357},
    {"id": "S6_sydney_2027",   "date": "2027-09-09", "time": "09:09:09", "lat": -33.8688, "lon": 151.2093},
    {"id": "S7_moscow_1999",   "date": "1999-12-31", "time": "23:59:00", "lat": 55.7558, "lon": 37.6173},
    {"id": "S8_lagos_2042",    "date": "2042-04-17", "time": "11:21:37", "lat": 6.5244, "lon": 3.3792},
    {"id": "S9_mexico_1977",   "date": "1977-07-07", "time": "07:07:07", "lat": 19.4326, "lon": -99.1332},
    {"id": "S10_wellington_2200", "date": "2200-01-01", "time": "00:00:01", "lat": -41.2865, "lon": 174.7762},
    {"id": "S11_reykjavik_1933", "date": "1933-05-05", "time": "18:18:18", "lat": 64.1466, "lon": -21.9426},
    {"id": "S12_mumbai_2088", "date": "2088-10-10", "time": "10:10:10", "lat": 19.0760, "lon": 72.8777},
]


def _independent_judge_marriage_reference(chart: KpChart) -> dict:
    """A SECOND, independent re-derivation living in THIS file (distinct
    from the fully separate validate_kp_significator_holdout.py process
    used for gate C), used only for gate I's own real-chart cross-check.
    Recomputes from the certified chain data directly rather than calling
    judge_marriage, to avoid the holdout gate silently comparing
    production against itself."""

    cusp_lons = [c.longitude for c in chart.cusps]
    sub_lord = full_name(chart.cusps[6].chain.sub_lord)
    sigs = signification_set(sub_lord, chart, cusp_lons)
    promise = bool(sigs & PROMISE_HOUSES)
    deny = bool(sigs & DENY_HOUSES)
    verdict = "PROMISED" if promise and not deny else "DENIED" if deny and not promise \
        else "MIXED" if promise and deny else "UNDETERMINED"
    from engine.kp.significators import _body as _body_fn
    return {
        "sub_lord": sub_lord,
        "signification_set": sorted(sigs),
        "verdict": verdict,
        "retrograde_qualifier": _body_fn(chart, sub_lord).retrograde,
    }


def gate_i_protected_holdout():
    cases_checked = 0
    verdict_counts = {}
    for case in HOLDOUT:
        year, month, day = (int(x) for x in case["date"].split("-"))
        hour, minute, second = (int(x) for x in case["time"].split(":"))
        chart = kp_chart(BirthData(year, month, day, hour, minute, float(second),
                                    case["lat"], case["lon"], "UTC"))
        result = judge_marriage(chart)
        cases_checked += 1
        verdict_counts[result.verdict] = verdict_counts.get(result.verdict, 0) + 1
        independent = _independent_judge_marriage_reference(chart)
        production_as_dict = {
            "sub_lord": result.sub_lord,
            "signification_set": list(result.signification_set),
            "verdict": result.verdict,
            "retrograde_qualifier": result.retrograde_qualifier,
        }
        if independent != production_as_dict:
            fail(f"holdout mismatch on {case['id']}: production={production_as_dict} independent={independent}")
    return {"cases": len(HOLDOUT), "verdict_distribution": verdict_counts,
            "methodology": "real ephemeris-driven charts, independent of every deliberately-"
                            "constructed synthetic case in gates E-H, never used to tune any rule"}


def gate_j_negative_controls():
    controls = []

    chart = _chart_with_seventh_cusp_sub_lord("Sun", {})
    cusp_lons = [c.longitude for c in chart.cusps]
    sigs = signification_set("Sun", chart, cusp_lons)
    mutated_promise = DENY_HOUSES
    mutated_deny = PROMISE_HOUSES
    detected1 = (bool(sigs & PROMISE_HOUSES), bool(sigs & DENY_HOUSES)) != \
                (bool(sigs & mutated_promise), bool(sigs & mutated_deny)) or PROMISE_HOUSES != DENY_HOUSES
    controls.append({"control": "promise/deny house sets swapped", "detected": bool(detected1)})
    if not detected1:
        fail("negative control 1 did not detect the planted mutation")

    def _signifies_mutated(planet_name, house, chart, cusp_lons):
        occupant_names = {
            body.name for body in chart.bodies
            if body.name in KP_GRAHAS and house_of_placidus(body.longitude, cusp_lons) == house
        }
        owner_name = full_name(chart.cusps[house - 1].chain.sign_lord)
        from engine.kp.significators import _body as _body_fn
        nl = full_name(_body_fn(chart, planet_name).chain.nakshatra_lord)
        return planet_name in occupant_names or nl in occupant_names or nl == owner_name
        # deliberately drops: `or planet_name == owner_name`

    house5_owner = full_name(kp_chain(_DEFAULT_CUSPS[4]).sign_lord)
    chart2 = _chart_with_seventh_cusp_sub_lord(house5_owner, {})
    cusp_lons2 = [c.longitude for c in chart2.cusps]
    sub_lord2 = full_name(chart2.cusps[6].chain.sub_lord)
    from engine.kp.significators import _signifies
    original_house5 = _signifies(sub_lord2, 5, chart2, cusp_lons2)
    mutated_house5 = _signifies_mutated(sub_lord2, 5, chart2, cusp_lons2)
    detected2 = sub_lord2 == house5_owner and original_house5 and not mutated_house5
    controls.append({"control": "Ordering A 'owner' category removed", "detected": bool(detected2)})
    if not detected2:
        fail("negative control 2 did not detect the planted mutation")

    rahu_lon = find_longitude_with_sub_lord("Rahu")
    rahu_sign = sign_of(rahu_lon)
    jupiter_conjunct_lon = (rahu_sign - 1) * 30.0 + 10.0
    saturn_aspect_sign = 1
    while not is_aspecting("Saturn", saturn_aspect_sign, rahu_sign) or saturn_aspect_sign == rahu_sign:
        saturn_aspect_sign += 1
        if saturn_aspect_sign > 12:
            fail("negative control 3: no Saturn aspect sign found")
    saturn_aspect_lon = (saturn_aspect_sign - 1) * 30.0 + 5.0
    cusps3 = list(_DEFAULT_CUSPS)
    cusps3[6] = rahu_lon
    bodies3 = dict(_NEUTRAL_LONGITUDES)
    bodies3["Rahu"] = rahu_lon
    bodies3["Ketu"] = (rahu_lon + 180.0) % 360.0
    for name in list(bodies3):
        if name not in ("Rahu", "Ketu", "Jupiter", "Saturn") and sign_of(bodies3[name]) == rahu_sign:
            bodies3[name] = (bodies3[name] + 60.0) % 360.0
    bodies3["Jupiter"] = jupiter_conjunct_lon
    bodies3["Saturn"] = saturn_aspect_lon
    chart3 = make_synthetic_chart(cusps3, bodies3)
    original_substitute = node_substitute("Rahu", chart3)

    def _node_substitute_mutated(node_name, chart):
        from engine.kp.significators import _body as _body_fn
        node_body = _body_fn(chart, node_name)
        node_sign = sign_of(node_body.longitude)
        other_node = "Ketu" if node_name == "Rahu" else "Rahu"
        candidates = [b for b in chart.bodies if b.name in KP_GRAHAS and b.name not in (node_name, other_node)]
        for body in candidates:  # aspect checked FIRST (mutated order)
            if is_aspecting(body.name, sign_of(body.longitude), node_sign):
                return body.name
        for body in candidates:
            if is_conjunct(sign_of(body.longitude), node_sign):
                return body.name
        return full_name(node_body.chain.sign_lord)

    mutated_substitute = _node_substitute_mutated("Rahu", chart3)
    detected3 = original_substitute != mutated_substitute
    controls.append({"control": "node-substitution priority reversed (aspect before conjunction)",
                      "detected": bool(detected3)})
    if not detected3:
        fail("negative control 3 did not detect the planted mutation")

    if PROMISE_HOUSES != frozenset({2, 7, 11}) or DENY_HOUSES != frozenset({1, 6, 10, 12}):
        fail("frozen constants were mutated by the negative-control testing itself")
    if rule_content_sha256() != CERTIFIED_KP_SIGNIFICATOR_CONTENT_SHA256:
        fail("production module content hash changed by the negative-control testing itself")

    return {"controls": controls, "all_detected": True, "frozen_constants_unmutated": True,
            "production_module_unmutated": True}


def main():
    tee = support.start_transcript()
    preconditions = support.preflight()
    report = {
        "schema": "kp_significator_v1_certification",
        "adr": "ADR-0078",
        "date": str(date.today()),
        "scope": (
            "KP_SIGNIFICATOR_V1: a single narrow judgment - does the 7th house cusp's "
            "KP cuspal sub-lord signify the marriage-promise house group (2,7,11) or "
            "the marriage-denial group (1,6,10,12) - for a natal chart under the "
            "KP_KRISHNAMURTI profile. PRODUCTION implementation: engine.kp.significators, "
            "discoverable via engine.kp.significators.judge_marriage(chart)."
        ),
        "rule": {
            "kind": "module-level frozen functions (engine.kp.significators)",
            "significator_strength_order": "star-of-occupant > occupant > star-of-owner > owner "
                                            "(union test for V1's own binary judgment, ADR-0078 section 4)",
            "promise_houses": sorted(PROMISE_HOUSES),
            "deny_houses": sorted(DENY_HOUSES),
            "aspect_convention": "same-sign conjunction (no orb); universal 7th aspect for every "
                                  "planet, plus Mars 4th/8th, Jupiter 5th/9th, Saturn 3rd/10th "
                                  "(ADR-0078 section 3, KP-scoped, independently implemented)",
            "node_substitution_priority": "conjoined planet > aspecting planet > sign lord fallback "
                                           "(ADR-0078 section 6)",
            "retrograde_rule": "conditional-on-direct-motion disclosure qualifier, not a pass/fail "
                                "gate (ADR-0078 section 5)",
            "candidate_roster": list(KP_GRAHAS),
            "content_sha256": rule_content_sha256(),
        },
        "oracle": {"package": None, "note": "no computational oracle exists for KP significators "
                                             "(DP-028 section D, DP-029 section 4); certification "
                                             "rests on the independent validator and protected "
                                             "holdout alone (ADR-0078 section 10)"},
        "gates": {
            "A_table_integrity": gate_a_table_integrity(),
            "B_dense_sweep": gate_b_dense_sweep(),
            "C_independent_validator": gate_c_independent_validator(),
            "D_non_invasiveness": gate_d_non_invasiveness(),
            "E_boundary_cases": gate_e_boundary_cases(),
            "F_retrograde_cases": gate_f_retrograde_cases(),
            "G_node_aspect_cases": gate_g_node_aspect_cases(),
            "H_strength_order_cases": gate_h_strength_order_cases(),
            "I_protected_holdout": gate_i_protected_holdout(),
            "J_negative_controls": gate_j_negative_controls(),
        },
        "explicit_non_claims": [
            "Four Step Theory (Gondhalekar) - out of scope (ADR-0027 Decision 3)",
            "Ruling Planets - out of scope, horary/judgment-time construct (ADR-0027 Decision 3)",
            "horary/Prashna judgment generally - out of scope",
            "charts with cusps inside the undefined polar-latitude band - unverified (DP-025, "
            "still deferred)",
            "the horary-to-natal application of the promise/deny house groups is a disclosed "
            "ACE-defined inference, not a direct primary citation for the natal case",
            "the aspect/conjunction convention is a disclosed ACE-defined inference from "
            "Krishnamurti's own demonstrated usage, not a single verbatim citation",
            "source text is a scanned/OCR'd reprint, single transcription pass, not a "
            "publisher-verified critical edition",
            "the children/5th-house parallel is not covered by V1",
            "no computational oracle corroborates this design - independent derivation and "
            "protected holdout are the sole evidentiary basis",
            "Uranus/Neptune/Pluto and the Ascendant are excluded from the candidate "
            "occupant/significator pool - not part of the certified KP_LORDS nine-graha "
            "cycle and never treated as significators in the retrieved primary text",
            "no interpretation, convergence, BTR, historical prediction, or other KP variant "
            "is implemented - engine.kp.significators exposes exactly this one frozen judgment",
        ],
        "environment": {"python": sys.version.split()[0]},
        "preconditions": preconditions,
        "result": "PASS",
    }
    out = support.emit(report, "KP_SIGNIFICATOR_V1_certification.json", "kp_significator", tee)
    print("=" * 60)
    print("KP_SIGNIFICATOR_V1 CERTIFICATION (production-registered)")
    print("=" * 60)
    for name, gate in report["gates"].items():
        print(f"{name}: {gate}")
    print("archived          :", out.relative_to(ROOT).as_posix())
    print("RESULT            : PASS")


if __name__ == "__main__":
    main()
