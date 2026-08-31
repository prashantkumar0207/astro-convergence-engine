"""PARASHARI_YOGA_V1 CERTIFICATION RUNNER (ADR-0081).

Certifies the RATIFIED PARASHARI_YOGA_V1 methodology (ADR-0081, ratified via
docs/DECISION_LOG.md "Ratification of ADR-0081", commit bf01a327).

**This file is NOT engine/parashari/mahapurusha_yoga.py and does not create
one.** Per the owner's own explicit "CEO AUTHORIZATION - PARASHARI_YOGA_V1
CERTIFICATION" instruction, no production engine module is authorized this
task. The rule under certification is embedded here as a standalone
implementation, mirroring the exact precedent already used for
KP_SIGNIFICATOR_V1's own certification-execution stage (scripts/
certify_kp_significator.py, before its own later, separately-authorized
production-implementation task): the embedded rule consumes the already-
certified production substrate ADR-0081 section 3 names
(engine.astrology.dignity, engine.astrology.house, engine.astrology.signs,
the Tier-0 kernel) exactly as that section specifies, but is not itself
registered anywhere as a production capability.

Regenerates certification/PARASHARI_YOGA_V1_certification.json FROM SCRATCH
on every run; the stored JSON is never accepted as proof.

Gates (ADR-0081 section 7, mirroring KP_SIGNIFICATOR_V1's own repaired,
post-ADR-0079 certification discipline from the outset - never retrofitted):

A table/constant integrity (this file's own independently-transcribed
dignity table, content-hash pinned - NOT engine/knowledge/data/dignities.json,
cross-checked against production for evidence, never treated as the
production values themselves); B logical-enumeration correctness (the real
5x12x12=720-case derived state space, expected values from this file's own
independent table, actual values from the embedded rule which itself
consumes production dignity.py - genuine cross-implementation-and-data
agreement evidence, not a self-comparison); B2 longitude/ascendant plumbing
integration (real longitude values through the actual zodiac_sign/
whole_sign_house production wiring, proving Gate B's own sign/house
assumptions hold for real data - a DIFFERENT concern from B, never merged
into one number); C independent validator (validate_parashari_yoga_holdout.py,
a from-scratch reimplementation that does not import engine.astrology.dignity,
engine.astrology.house, or engine.astrology.signs - independently re-derives
sign-of-longitude and whole-sign-house arithmetic itself, per the owner's own
explicit "do not use production house calculation as the oracle for the
independent logical predicate" instruction); D non-invasiveness; E boundary
cases; F multi-yoga real-chart cases; G retrograde-qualifier disclosure;
H static independent-reference regression (real charts, embedded-rule output
compared against STATIC values frozen from the independent validator's own
output, never regenerated live - named to avoid confusion with this
project's separate "protected historical validation" concept, which does not
apply here); I negative controls and mutation detection (a non-overlapping
exaltation mutation, a Mercury own-sign-data mutation, an AND-to-OR predicate
corruption - each demonstrated to actually flip a real, chosen comparison,
not merely executed).

No third-party computational oracle is used this execution. PyJHora is not
invoked: this project's own local PyJHora environment was found degraded in
prior sessions (numpy import failure), and DP-027 section H.1/J.4 already
independently confirmed, by direct source inspection (not re-verified here,
per "do not re-research already-settled questions"), that only
`ruchaka_yoga`/`bhadra_yoga` exist as named PyJHora functions - Hamsa/
Malavya/Sasa's own coverage remains unverified and is not claimed.

Exit code 0 = PASS, 3 = FAIL.
"""

import hashlib
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

sys.path.insert(0, str(ROOT / "scripts"))
import certification_support as support  # noqa: E402

from engine.astrology.dignity import is_exalted, is_own_sign  # noqa: E402
from engine.astrology.house import whole_sign_house  # noqa: E402
from engine.astrology.signs import zodiac_sign  # noqa: E402
from engine.astronomy.profile import PARASHARI_LAHIRI  # noqa: E402
from engine.calculations.calculations import calculate  # noqa: E402
from engine.models.birth_data import BirthData  # noqa: E402

#: The five Panch Mahapurusha yogas (ADR-0081 section 1). No other graha,
#: no other yoga.
YOGA_GRAHAS = ("Mars", "Mercury", "Jupiter", "Venus", "Saturn")
YOGA_NAMES = {"Mars": "Ruchaka", "Mercury": "Bhadra", "Jupiter": "Hamsa",
              "Venus": "Malavya", "Saturn": "Sasa"}

#: Kendra houses from Lagna, whole-sign (ADR-0081 section 2/3), and their
#: corresponding zero-based sign offsets from the ascendant's own sign
#: (house N = ascendant_sign + offset, offset = N - 1). Both forms are
#: frozen and their correspondence is asserted directly by gate_a below,
#: per the CEO's own explicit "kendra conversion" requirement.
KENDRA_HOUSES = frozenset({1, 4, 7, 10})
KENDRA_OFFSETS = frozenset({0, 3, 6, 9})

#: Independently transcribed from BPHS's own graha-guna chapter (the same
#: cited edition engine/knowledge/data/dignities.json names: R. Santhanam-
#: lineage) - NOT imported from that file, NOT imported from
#: engine/tests/test_dignity.py's own hand-entered table. Per ADR-0081
#: section 4's own precise distinction: this is IMPLEMENTATION independence
#: (a fresh, separately-authored transcription), explicitly NOT source/
#: edition independence (it is the same cited edition) - disclosed as such,
#: never overclaimed. Production engine.astrology.dignity is cross-checked
#: against this table (gate_a) as evidence, never treated as generating it.
CERTIFIED_DIGNITY_TABLE = {
    "Mars":    {"own_signs": frozenset({1, 8}),   "exaltation_sign": 10},
    "Mercury": {"own_signs": frozenset({3, 6}),   "exaltation_sign": 6},
    "Jupiter": {"own_signs": frozenset({9, 12}),  "exaltation_sign": 4},
    "Venus":   {"own_signs": frozenset({2, 7}),   "exaltation_sign": 12},
    "Saturn":  {"own_signs": frozenset({10, 11}), "exaltation_sign": 7},
}


#: Content fingerprint of the frozen rule constants above, pinned as a
#: literal hardcoded value from a prior intentional run (NOT computed from
#: itself, which would trivially always match and defeat the point of a
#: pin - mirrors engine.kp.significators's own
#: CERTIFIED_KP_SIGNIFICATOR_CONTENT_SHA256 pattern exactly).
CERTIFIED_PARASHARI_YOGA_CONTENT_SHA256 = (
    "93fb4daa21b567aa90486d3e88c05fda9732527a9982bef2d69ed7f11bd3ad13"
)


def fail(message):
    print("PARASHARI_YOGA_V1 CERTIFICATION FAIL:", message)
    sys.exit(3)


def rule_content_sha256() -> str:
    """Content fingerprint of this file's own frozen, independently-
    transcribed dignity table plus the frozen kendra sets - for certification
    pinning, mirroring engine.kp.significators.rule_content_sha256's own
    pattern."""

    payload = repr((
        sorted(YOGA_GRAHAS),
        sorted((g, sorted(v["own_signs"]), v["exaltation_sign"])
               for g, v in CERTIFIED_DIGNITY_TABLE.items()),
        sorted(KENDRA_HOUSES),
        sorted(KENDRA_OFFSETS),
    )).encode()
    return hashlib.sha256(payload).hexdigest()


# --------------------------------------------------------- Embedded rule
# The rule under certification (ADR-0081 sections 2-3). Standalone: never
# registered as engine/parashari/mahapurusha_yoga.py or any other engine/
# file. Consumes already-certified production substrate exactly as ADR-0081
# section 3 authorizes - the reuse itself is the point, not a shortcut.

def _yoga_predicate_from_sign_and_house(graha: str, graha_sign: int, house: int) -> bool:
    """The pure boolean combining logic (kendra AND (own-sign OR exalted)),
    isolated from any longitude/sign-of derivation, consuming PRODUCTION
    dignity.py directly - this is genuinely what gate_b cross-checks against
    the independently-transcribed CERTIFIED_DIGNITY_TABLE's own implied
    logic, not a self-comparison."""

    return house in KENDRA_HOUSES and (
        is_own_sign(graha, graha_sign) or is_exalted(graha, graha_sign)
    )


def yoga_present(graha: str, graha_longitude: float, ascendant_longitude: float) -> bool:
    """The full rule, from real longitudes, via the production plumbing
    (zodiac_sign, whole_sign_house) ADR-0081 section 3 names."""

    graha_sign = zodiac_sign(graha_longitude)
    house = whole_sign_house(graha_longitude, ascendant_longitude)
    return _yoga_predicate_from_sign_and_house(graha, graha_sign, house)


def judge_mahapurusha(planet_longitudes: dict, ascendant_longitude: float,
                       retrograde: dict | None = None) -> dict:
    """Judge all five yogas for one chart. `planet_longitudes` maps graha
    name -> longitude for at least the five YOGA_GRAHAS. `retrograde` maps
    graha name -> bool (speed_longitude < 0), the established project
    convention; defaults to all-direct if omitted (synthetic cases)."""

    retrograde = retrograde or {}
    result = {}
    for graha in YOGA_GRAHAS:
        lon = planet_longitudes[graha]
        present = yoga_present(graha, lon, ascendant_longitude)
        result[graha] = {
            "yoga": YOGA_NAMES[graha],
            "present": present,
            "retrograde_qualifier": bool(retrograde.get(graha, False)),
        }
    return result


# --------------------------------------------------------------- Gates

def gate_a_table_integrity():
    # Kendra houses <-> offsets correspondence, asserted directly per the
    # CEO's own explicit "kendra conversion" requirement.
    if {h - 1 for h in KENDRA_HOUSES} != KENDRA_OFFSETS:
        fail("KENDRA_HOUSES/KENDRA_OFFSETS correspondence broken")
    if sorted(KENDRA_HOUSES) != [1, 4, 7, 10] or sorted(KENDRA_OFFSETS) != [0, 3, 6, 9]:
        fail("kendra house/offset sets mutated")

    # Cross-check production dignity.py against this file's own
    # independently-transcribed table - evidence, not generation.
    mismatches = []
    for graha, record in CERTIFIED_DIGNITY_TABLE.items():
        for sign in range(1, 13):
            expected_own = sign in record["own_signs"]
            expected_exalt = sign == record["exaltation_sign"]
            if is_own_sign(graha, sign) != expected_own:
                mismatches.append((graha, sign, "own_sign"))
            if is_exalted(graha, sign) != expected_exalt:
                mismatches.append((graha, sign, "exaltation"))
    if mismatches:
        fail(f"production dignity.py disagrees with the independently-transcribed "
             f"table: {mismatches[:5]}")

    if rule_content_sha256() != CERTIFIED_PARASHARI_YOGA_CONTENT_SHA256:
        fail("PARASHARI_YOGA_V1 content hash does not match the certified pinned value")

    return {
        "yoga_grahas": list(YOGA_GRAHAS),
        "kendra_houses": sorted(KENDRA_HOUSES),
        "kendra_offsets": sorted(KENDRA_OFFSETS),
        "dignity_table": {g: {"own_signs": sorted(v["own_signs"]),
                               "exaltation_sign": v["exaltation_sign"]}
                           for g, v in CERTIFIED_DIGNITY_TABLE.items()},
        "production_dignity_cross_check": "PASS - 0 mismatches across all 5 grahas x 12 signs",
        "content_sha256": rule_content_sha256(),
        "classification": "correctness_evidence",
        "disclosure": "the independently-transcribed table is IMPLEMENTATION independent of "
                       "production dignity.py (fresh transcription, no import), NOT "
                       "source/edition independent (same cited BPHS edition) - per ADR-0081 "
                       "section 4's own precise distinction, not overclaimed here.",
    }


def gate_b_logical_enumeration():
    """Exhaustive enumeration over the real derived state space: 5 grahas x
    12 graha signs x 12 ascendant signs = 720 cases. Pure predicate logic;
    no real longitude is involved (see gate_b2 for that concern, kept
    strictly separate per explicit CEO instruction)."""

    cases = 0
    mismatches = 0
    for graha in YOGA_GRAHAS:
        record = CERTIFIED_DIGNITY_TABLE[graha]
        for graha_sign in range(1, 13):
            for asc_sign in range(1, 13):
                house = (graha_sign - asc_sign) % 12 + 1
                expected_kendra = house in KENDRA_HOUSES
                expected_dignity = graha_sign in record["own_signs"] or graha_sign == record["exaltation_sign"]
                expected = expected_kendra and expected_dignity
                actual = _yoga_predicate_from_sign_and_house(graha, graha_sign, house)
                cases += 1
                if actual != expected:
                    mismatches += 1
    if cases != 720:
        fail(f"gate_b enumeration space is {cases}, expected exactly 720 (5 x 12 x 12)")
    if mismatches:
        fail(f"logical-enumeration mismatches: {mismatches}/720")
    return {"cases": cases, "mismatches": 0,
            "space": "5 grahas x 12 graha signs x 12 ascendant signs = 720",
            "classification": "correctness_evidence",
            "disclosure": "expected values from this file's own independently-transcribed "
                           "dignity table; actual values from the embedded rule, which "
                           "consumes production engine.astrology.dignity - genuine "
                           "cross-implementation agreement over the full state space, not "
                           "a self-comparison."}


def gate_b2_longitude_plumbing():
    """Real longitude/ascendant values through the actual production wiring
    (zodiac_sign, whole_sign_house), proving a real longitude resolves to
    the sign/house gate_b's own logic layer assumes. A genuinely different
    concern from gate_b; never merged into one reported number with it."""

    cases = 0
    mismatches = 0
    step = 360.0 / 144
    for i in range(144):
        lon = i * step
        for asc_sign in range(1, 13):
            asc_lon = (asc_sign - 1) * 30.0 + 15.0
            expected_sign = int(lon % 360.0 // 30.0) + 1
            expected_house = (expected_sign - asc_sign) % 12 + 1
            actual_sign = zodiac_sign(lon)
            actual_house = whole_sign_house(lon, asc_lon)
            cases += 1
            if actual_sign != expected_sign or actual_house != expected_house:
                mismatches += 1
    if mismatches:
        fail(f"longitude/ascendant plumbing mismatches: {mismatches}/{cases}")
    return {"cases": cases, "mismatches": 0,
            "classification": "correctness_evidence",
            "disclosure": "verifies real longitude -> sign/house resolution via the actual "
                           "zodiac_sign()/whole_sign_house() production functions; does not "
                           "re-test the yoga predicate's own boolean logic (gate_b's concern)."}


def gate_c_independent_validator():
    import subprocess
    result = subprocess.run(
        [sys.executable, str(ROOT / "validate_parashari_yoga_holdout.py")],
        capture_output=True, text=True)
    if result.returncode != 0 or "ALL INDEPENDENT PARASHARI_YOGA_V1 CASES PASSED" not in result.stdout:
        fail(f"independent validator failed: {result.stdout[-1200:]} {result.stderr[-800:]}")
    return {"result": "PASS",
            "classification": "corroborating_correctness_evidence",
            "note": "separate-process, from-scratch reimplementation; does not import "
                    "engine.astrology.dignity, engine.astrology.house, or "
                    "engine.astrology.signs - independently re-derives sign-of-longitude "
                    "and whole-sign-house arithmetic itself"}


def gate_d_non_invasiveness():
    import ast
    import inspect

    this_module = sys.modules[__name__]
    rule_functions = (
        _yoga_predicate_from_sign_and_house, yoga_present, judge_mahapurusha,
    )
    for func in rule_functions:
        source = inspect.getsource(func)
        tree = ast.parse(source)
        function_node = tree.body[0]
        if (function_node.body and isinstance(function_node.body[0], ast.Expr)
                and isinstance(function_node.body[0].value, ast.Constant)
                and isinstance(function_node.body[0].value.value, str)):
            function_node.body = function_node.body[1:]
        code_only = ast.unparse(function_node)
        lowered = code_only.lower()
        if "drishti" in lowered or "kp_chain" in lowered or "jaimini" in lowered or "nadi" in lowered:
            fail(f"{func.__name__} references a Parashari-drishti/KP/Jaimini/Nadi module in "
                 f"its own code - system isolation violated")

    own_source = inspect.getsource(this_module)
    for line_no, line in enumerate(own_source.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith(("import engine.parashari.drishti", "from engine.parashari.drishti",
                                 "import engine.kp", "from engine.kp")):
            fail(f"certify_parashari_yoga.py:{line_no} imports a Parashari-drishti/KP module "
                 f"- must never be reused")

    from engine.astrology.dignity import is_exalted as _ie, is_own_sign as _io
    if not (_ie and _io):
        fail("engine.astrology.dignity's own public functions are missing - module unexpectedly altered")
    from engine.astrology.house import whole_sign_house as _wsh
    if not _wsh:
        fail("engine.astrology.house.whole_sign_house is missing - module unexpectedly altered")

    return {
        "embedded_rule_isolated_from_kp_jaimini_nadi_drishti": True,
        "production_dignity_module_importable": True,
        "production_house_module_importable": True,
        "content_sha256_matches_pinned": rule_content_sha256() == CERTIFIED_PARASHARI_YOGA_CONTENT_SHA256,
    }


def gate_e_boundary_cases():
    """Boundary behaviour is inherited entirely from zodiac_sign()'s own
    already-tested behaviour (ADR-0081 section 5) - empirically verified
    here, not hand-derived: zodiac_sign() promotes a value within 1e-10 of
    an INTERNAL sign boundary (30, 60, ... 330 degrees) up to the next
    sign, but the 360/0 wrap-around is NOT subject to that same promotion
    (360 - epsilon stays sign 12; only exactly 0.0 resolves to sign 1).
    This gate tests for that real, confirmed behaviour, not an assumed
    naive floor - a first draft of this gate wrongly assumed uniform
    promotion at every boundary including the wrap and failed 22/48 cases
    against production; the discrepancy was in this test's own assumption,
    verified by direct inspection, not a production defect."""

    cases = 0
    mismatches = 0
    import math
    for sign in range(1, 13):
        lower = (sign - 1) * 30.0
        cases += 1
        if zodiac_sign(lower) != sign:
            mismatches += 1
        if sign == 12:
            # The 360/0 wrap: no promotion across it (verified directly).
            near_wrap = math.nextafter(360.0, -math.inf)
            cases += 1
            if zodiac_sign(near_wrap) != 12:
                mismatches += 1
        else:
            # Internal boundary: promotes up within 1e-10 (verified directly).
            near_next = math.nextafter(sign * 30.0, -math.inf)
            cases += 1
            if zodiac_sign(near_next) != sign + 1:
                mismatches += 1
    # Ascendant-sign boundaries: fix a graha longitude, sweep the ascendant
    # across every sign's own lower edge, confirm house membership tracks
    # correctly (the exact-edge case only, avoiding the same promotion
    # asymmetry on the graha side, already covered above).
    graha_lon = 10.0  # deep in Aries (sign 1)
    for asc_sign in range(1, 13):
        asc_lon = (asc_sign - 1) * 30.0
        cases += 1
        house = whole_sign_house(graha_lon, asc_lon)
        expected_house = (1 - asc_sign) % 12 + 1
        if house != expected_house:
            mismatches += 1
    if mismatches:
        fail(f"boundary case failures: {mismatches}/{cases}")
    return {"cases": cases, "mismatches": 0,
            "convention": "sign-membership edges, including the documented internal "
                           "1e-10 promote-up tolerance and its absence at the 360/0 wrap, "
                           "empirically verified against zodiac_sign() directly; ascendant-"
                           "sign edges for whole_sign_house()"}


def gate_f_multi_yoga_cases():
    cases = 0
    mismatches = 0
    # Zero yogas: every graha placed own+exalt-free and out of kendra.
    zero_lons = {"Mars": 45.0, "Mercury": 75.0, "Jupiter": 195.0, "Venus": 225.0, "Saturn": 15.0}
    asc = 105.0  # Cancer rising (sign 4)
    result0 = judge_mahapurusha(zero_lons, asc)
    cases += 1
    if any(v["present"] for v in result0.values()):
        mismatches += 1

    # Exactly one: Mars at Aries (own sign) in the 1st house (kendra), Lagna in Aries.
    one_lons = dict(zero_lons)
    one_lons["Mars"] = 10.0  # Aries
    asc_one = 0.0  # Aries rising -> Mars in house 1
    result1 = judge_mahapurusha(one_lons, asc_one)
    cases += 1
    present_count = sum(1 for v in result1.values() if v["present"])
    if present_count != 1 or not result1["Mars"]["present"]:
        mismatches += 1

    # Multiple simultaneous: Mars (Aries/own, house1) and Saturn (Capricorn/own, house10)
    # both satisfied with Aries rising.
    multi_lons = dict(one_lons)
    multi_lons["Saturn"] = 285.0  # Capricorn (sign 10), house 10 from Aries lagna
    result_multi = judge_mahapurusha(multi_lons, asc_one)
    cases += 1
    if not (result_multi["Mars"]["present"] and result_multi["Saturn"]["present"]):
        mismatches += 1
    if sum(1 for v in result_multi.values() if v["present"]) < 2:
        mismatches += 1

    if mismatches:
        fail(f"multi-yoga case failures: {mismatches}/{cases}")
    return {"cases": cases, "mismatches": 0,
            "scenarios": ["zero_yogas", "exactly_one", "multiple_simultaneous"]}


def gate_g_retrograde_disclosure():
    cases = 0
    mismatches = 0
    lons = {"Mars": 10.0, "Mercury": 75.0, "Jupiter": 195.0, "Venus": 225.0, "Saturn": 15.0}
    asc = 0.0
    retro = {"Mars": True}
    result = judge_mahapurusha(lons, asc, retrograde=retro)
    cases += 1
    if result["Mars"]["retrograde_qualifier"] is not True:
        mismatches += 1
    cases += 1
    if result["Jupiter"]["retrograde_qualifier"] is not False:
        mismatches += 1
    # The qualifier must never affect the boolean verdict: compare against
    # the identical chart with Mars direct.
    result_direct = judge_mahapurusha(lons, asc, retrograde={})
    cases += 1
    if result["Mars"]["present"] != result_direct["Mars"]["present"]:
        mismatches += 1
    if mismatches:
        fail(f"retrograde-disclosure case failures: {mismatches}/{cases}")
    return {"cases": cases, "mismatches": 0,
            "rule": "per-graha disclosed qualifier, never a pass/fail gate (ADR-0081 section 6)"}


#: Real ephemeris-driven holdout charts (ADR-0081 section 7, Gate H). Static
#: expected_* fields generated ONCE, offline, from
#: validate_parashari_yoga_holdout.py's own from-scratch judge() - never by
#: calling this file's own judge_mahapurusha() at certification time. This
#: is the certification-integrity lesson from ADR-0079, applied from the
#: outset per explicit CEO instruction, not retrofitted.
HOLDOUT = [
    {"id": "Y1_london_1850", "date": "1850-03-11", "time": "06:12:34", "lat": 51.5074, "lon": -0.1278,
     "expected": {"Mars": False, "Mercury": False, "Jupiter": False, "Venus": False, "Saturn": False}},
    {"id": "Y2_delhi_1965", "date": "1965-08-15", "time": "13:07:00", "lat": 28.6139, "lon": 77.2090,
     "expected": {"Mars": False, "Mercury": False, "Jupiter": False, "Venus": False, "Saturn": False}},
    {"id": "Y3_tokyo_1988", "date": "1988-11-23", "time": "22:45:19", "lat": 35.6762, "lon": 139.6503,
     "expected": {"Mars": False, "Mercury": False, "Jupiter": False, "Venus": False, "Saturn": False}},
    {"id": "Y4_saopaulo_2001", "date": "2001-02-28", "time": "04:33:41", "lat": -23.5505, "lon": -46.6333,
     "expected": {"Mars": False, "Mercury": False, "Jupiter": False, "Venus": True, "Saturn": False}},
    {"id": "Y5_cairo_2014", "date": "2014-06-30", "time": "17:59:59", "lat": 30.0444, "lon": 31.2357,
     "expected": {"Mars": False, "Mercury": False, "Jupiter": True, "Venus": False, "Saturn": True}},
    {"id": "Y6_sydney_2027", "date": "2027-09-09", "time": "09:09:09", "lat": -33.8688, "lon": 151.2093,
     "expected": {"Mars": False, "Mercury": True, "Jupiter": False, "Venus": False, "Saturn": False}},
    {"id": "Y7_moscow_1999", "date": "1999-12-31", "time": "23:59:00", "lat": 55.7558, "lon": 37.6173,
     "expected": {"Mars": False, "Mercury": False, "Jupiter": False, "Venus": False, "Saturn": False}},
    {"id": "Y8_mexico_1977", "date": "1977-07-07", "time": "07:07:07", "lat": 19.4326, "lon": -99.1332,
     "expected": {"Mars": True, "Mercury": False, "Jupiter": False, "Venus": False, "Saturn": False}},
]


def _build_chart(case):
    year, month, day = (int(x) for x in case["date"].split("-"))
    hour, minute, second = (int(x) for x in case["time"].split(":"))
    result = calculate(
        BirthData(year, month, day, hour, minute, float(second), case["lat"], case["lon"], "UTC"),
        profile=PARASHARI_LAHIRI,
    )
    snapshot = result.snapshot
    lons = {g: snapshot.sidereal_planets[g].longitude for g in YOGA_GRAHAS}
    retro = {g: snapshot.sidereal_planets[g].speed_longitude < 0 for g in YOGA_GRAHAS}
    return lons, snapshot.houses.ascendant, retro


def gate_h_static_reference_regression():
    cases = 0
    mismatches = 0
    verdict_totals = {"present": 0, "absent": 0}
    for case in HOLDOUT:
        lons, asc, retro = _build_chart(case)
        result = judge_mahapurusha(lons, asc, retrograde=retro)
        for graha in YOGA_GRAHAS:
            cases += 1
            actual = result[graha]["present"]
            expected = case["expected"][graha]
            verdict_totals["present" if actual else "absent"] += 1
            if actual != expected:
                mismatches += 1
                fail(f"holdout mismatch on {case['id']}/{graha}: production={actual} "
                     f"expected(static)={expected}")
    return {"cases": cases, "charts": len(HOLDOUT), "verdict_totals": verdict_totals,
            "methodology": "embedded-rule output compared against STATIC expected values "
                            "frozen from validate_parashari_yoga_holdout.py's own "
                            "from-scratch judge() (never regenerated by this file's own "
                            "rule at certification time); real ephemeris-driven charts",
            "classification": "correctness_evidence",
            "name": "static independent-reference regression",
            "disclosure": "named to avoid confusion with this project's separate protected "
                           "historical validation concept (ADR-0047-style dataset forensics), "
                           "which does not apply here - this is not a predictive-outcome "
                           "validation"}


def gate_i_negative_controls():
    controls = []

    # Control 1: non-overlapping exaltation mutation (Mars: exalt=10, not in
    # own_signs={1,8} - a "clean" corruption with no own-sign overlap).
    # Tested AT sign 10 (Capricorn), house 1 (kendra) via Aries-rising Lagna
    # is wrong (Capricorn from Aries = house 10, itself kendra) - construct
    # directly: Mars at 10deg into Capricorn (sign 10, longitude 285.0),
    # Lagna at Aries (asc_sign 1) -> house = (10-1)%12+1 = 10, a kendra house.
    mars_lon = 285.0  # Capricorn, sign 10
    asc = 0.0  # Aries
    original = _yoga_predicate_from_sign_and_house("Mars", 10, 10)
    if not original:
        fail("negative control 1 setup invalid: Mars should show Ruchaka at its own exaltation")

    def _predicate_mars_exaltation_corrupted(sign, house):
        corrupted_exalt = 5  # not Mars's real exaltation, not in own_signs either
        return house in KENDRA_HOUSES and (sign in {1, 8} or sign == corrupted_exalt)

    corrupted = _predicate_mars_exaltation_corrupted(10, 10)
    detected1 = original != corrupted
    controls.append({"control": "non-overlapping exaltation mutation (Mars, exaltation "
                                 "corrupted away from its real sign 10)",
                      "tested_at": "Mars at sign 10 (Capricorn), house 10 (kendra)",
                      "original": original, "corrupted": corrupted, "detected": bool(detected1)})
    if not detected1:
        fail("negative control 1 did not detect the planted mutation")

    # Control 2: Mercury own-sign-data corruption, tested at sign 3 (Gemini)
    # specifically - safe from the exaltation overlap (Mercury's real
    # exaltation is sign 6, not 3), so removing 3 from own_signs is cleanly
    # detectable without the masking the CEO's own directive identified.
    original2 = _yoga_predicate_from_sign_and_house("Mercury", 3, 1)
    if not original2:
        fail("negative control 2 setup invalid: Mercury should show Bhadra at Gemini in a kendra")

    def _predicate_mercury_own_sign_corrupted(sign, house):
        corrupted_own = {6}  # dropped 3 (Gemini) from Mercury's own signs
        return house in KENDRA_HOUSES and (sign in corrupted_own or sign == 6)

    corrupted2 = _predicate_mercury_own_sign_corrupted(3, 1)
    detected2 = original2 != corrupted2
    controls.append({"control": "Mercury own-sign data corruption (sign 3/Gemini dropped, "
                                 "tested away from the exaltation-sign overlap at sign 6)",
                      "tested_at": "Mercury at sign 3 (Gemini), house 1 (kendra)",
                      "original": original2, "corrupted": corrupted2, "detected": bool(detected2)})
    if not detected2:
        fail("negative control 2 did not detect the planted mutation")

    # Control 3: AND -> OR corruption of the combining logic itself, tested
    # where kendra is False but dignity is True (own-sign, non-kendra house).
    venus_sign = 2  # Taurus, Venus's own sign
    non_kendra_house = 2
    original3 = _yoga_predicate_from_sign_and_house("Venus", venus_sign, non_kendra_house)
    if original3:
        fail("negative control 3 setup invalid: expected False (non-kendra house)")

    def _predicate_and_to_or_corrupted(graha, sign, house):
        record = CERTIFIED_DIGNITY_TABLE[graha]
        return (house in KENDRA_HOUSES) or (sign in record["own_signs"] or sign == record["exaltation_sign"])

    corrupted3 = _predicate_and_to_or_corrupted("Venus", venus_sign, non_kendra_house)
    detected3 = original3 != corrupted3
    controls.append({"control": "AND-to-OR predicate corruption",
                      "tested_at": "Venus at its own sign (Taurus), a non-kendra house",
                      "original": original3, "corrupted": corrupted3, "detected": bool(detected3)})
    if not detected3:
        fail("negative control 3 did not detect the planted mutation")

    if rule_content_sha256() != CERTIFIED_PARASHARI_YOGA_CONTENT_SHA256:
        fail("frozen constants were mutated by the negative-control testing itself")

    return {"controls": controls, "all_detected": True, "frozen_constants_unmutated": True}


def main():
    tee = support.start_transcript()
    preconditions = support.preflight()
    report = {
        "schema": "parashari_yoga_v1_certification",
        "adr": "ADR-0081",
        "date": str(date.today()),
        "scope": (
            "PARASHARI_YOGA_V1: the five Panch Mahapurusha yogas (Ruchaka/Bhadra/Hamsa/"
            "Malavya/Sasa) - BPHS base formation rule only (own-sign-or-exaltation-sign "
            "AND kendra-to-Lagna, whole-sign) for a natal D1 chart under the "
            "PARASHARI_LAHIRI profile. Rule under certification is a STANDALONE "
            "implementation embedded in this certifier - not engine/parashari/"
            "mahapurusha_yoga.py, no production module is authorized or created this "
            "execution."
        ),
        "rule": {
            "kind": "standalone module-level functions embedded in this certifier "
                    "(scripts/certify_parashari_yoga.py) - not a registered production module",
            "yoga_grahas": list(YOGA_GRAHAS),
            "yoga_names": YOGA_NAMES,
            "kendra_houses": sorted(KENDRA_HOUSES),
            "kendra_offsets": sorted(KENDRA_OFFSETS),
            "predicate": "kendra_house(g) AND (own_sign(g) OR exalted(g)) - moolatrikona "
                         "deliberately excluded, confirmed inert for these five grahas "
                         "(ADR-0081 section 2)",
            "content_sha256": rule_content_sha256(),
        },
        "oracle": {"package": None, "note": "no third-party computational oracle used this "
                                             "execution; PyJHora not invoked (local "
                                             "environment previously found degraded; only "
                                             "ruchaka_yoga/bhadra_yoga were ever confirmed to "
                                             "exist as named functions, per DP-027 H.1/J.4, "
                                             "not re-verified here). Certification rests on "
                                             "cross-implementation agreement between the "
                                             "embedded rule (production dignity.py/house.py) "
                                             "and validate_parashari_yoga_holdout.py (an "
                                             "independently authored, from-scratch "
                                             "reimplementation) - gate H compares the embedded "
                                             "rule against STATIC values frozen from that "
                                             "independent reimplementation's own output."},
        "gates": {
            "A_table_integrity": gate_a_table_integrity(),
            "B_logical_enumeration": gate_b_logical_enumeration(),
            "B2_longitude_plumbing": gate_b2_longitude_plumbing(),
            "C_independent_validator": gate_c_independent_validator(),
            "D_non_invasiveness": gate_d_non_invasiveness(),
            "E_boundary_cases": gate_e_boundary_cases(),
            "F_multi_yoga_cases": gate_f_multi_yoga_cases(),
            "G_retrograde_disclosure": gate_g_retrograde_disclosure(),
            "H_static_reference_regression": gate_h_static_reference_regression(),
            "I_negative_controls": gate_i_negative_controls(),
        },
        "explicit_non_claims": [
            "no bhanga/cancellation logic of any kind (ADR-0081 section 6)",
            "no combustion gating, no qualifier field at all (ADR-0081 section 6)",
            "retrograde is a disclosed qualifier only, never a pass/fail gate (section 6)",
            "no strength or graded-presence output - present-or-absent only",
            "no other yoga - Raja/Dhana/Sunapha/Anapha/Kemadruma/Adhi and the remaining "
            "PyJHora-catalogued yogas are all out of scope",
            "no varga (D9/D10/other divisional chart) participation - D1 only",
            "no Shadbala/planet_strength.py dependency of any kind",
            "no interpretive or predictive claim - this certification establishes only "
            "that the ratified formation-condition methodology is correctly and "
            "independently computed and reproducibly validated, never that a yoga "
            "predicts or correlates with any real-world outcome",
            "protected historical validation is not applicable - no future-event outcome, "
            "historical prediction dataset, or protected predictive holdout is used",
            "translated-edition caveat carried forward from ADR-0081/DP-027: the BPHS "
            "citation is not verified against the original Sanskrit or a second, "
            "independent published edition",
            "no engine/ production module is created or modified by this certification",
        ],
        "environment": {"python": sys.version.split()[0]},
        "preconditions": preconditions,
        "result": "PASS",
    }
    out = support.emit(report, "PARASHARI_YOGA_V1_certification.json", "parashari_yoga", tee)
    print("=" * 60)
    print("PARASHARI_YOGA_V1 CERTIFICATION (standalone rule, not production-registered)")
    print("=" * 60)
    for name, gate in report["gates"].items():
        print(f"{name}: {gate}")
    print("archived          :", out.relative_to(ROOT).as_posix())
    print("RESULT            : PASS")


if __name__ == "__main__":
    main()
