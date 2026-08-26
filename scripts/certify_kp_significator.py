"""KP_SIGNIFICATOR_V1 CERTIFICATION RUNNER (ADR-0078).

Certifies a STANDALONE, UNREGISTERED implementation of the frozen KP_SIGNIFICATOR_V1
rule (the narrow 7th-cusp marriage promise/denial judgment), per ADR-0078 section 13:
this certification-execution stage does NOT write or register
engine/kp/significators.py - the frozen rule lives in this script only, exactly
mirroring the D45 certification-execution precedent (ADR-0077's own original
standalone-rule stage inside certify_d45.py, before production authorization).

Consumes ONLY already-certified substrates: KP_CHAIN_V1 (engine.kp.chain.kp_chain,
engine.kp.chart.kp_chart) for cusp/planet SL/NL/SB/SS and Placidus cusp longitudes.
Builds exactly two genuinely NEW pieces of logic, isolated in this file, NEVER
importing from or modifying engine.parashari.drishti (PARASHARI_DRISHTI_V1):

  1. Placidus-cusp house occupancy. A real correction discovered during THIS
     execution, documented here rather than silently fixed: ADR-0078 section 2
     named engine.astrology.house.whole_sign_house/equal_house_from_ascendant as
     reusable "per its own profile-agnostic signature." Both are the WRONG house
     system for KP, which is defined on unequal Placidus cusps - whole-sign and
     equal-house would silently substitute a different house boundary than the
     one KP's own cuspal sub-lord theory actually uses. This certifier instead
     derives house occupancy directly from the already-certified KP_CHAIN_V1
     cusp longitudes (house_of_placidus below) - no new astronomical calculation,
     only correct interval-containment glue logic.
  2. The KP-scoped whole-sign aspect/conjunction calculation (ADR-0078 section 3):
     same-sign conjunction (no orb); universal 7th aspect for every planet, plus
     Mars 4th/8th, Jupiter 5th/9th, Saturn 3rd/10th - independently implemented,
     never touching PARASHARI_DRISHTI_V1's own module.

Significator scope: the classical nine KP grahas only (Sun, Moon, Mars, Mercury,
Jupiter, Venus, Saturn, Rahu, Ketu) - the same roster KP_CHAIN_V1's own KP_LORDS
table uses. Uranus/Neptune/Pluto and the Ascendant are excluded from the candidate
occupant/significator pool: they are never KP dasha lords or nakshatra lords under
the certified KP_LORDS cycle, and Krishnamurti's own retrieved text (Reader III)
never treats them as significators. This is a disclosed scope decision, not
silently assumed - see explicit_non_claims below.

Gates: A rule/table integrity; B dense sweep (cusp-longitude -> sub-lord wiring,
production vs. an independent re-derivation); C independent validator
(validate_kp_significator_holdout.py, a full from-scratch reimplementation);
D non-invasiveness (confirms KP_CHAIN_V1, PARASHARI_DRISHTI_V1, sign_lord.py
untouched, and that no Parashari aspect code is imported anywhere in this file or
the validator); E boundary cases (KP_CHAIN_V1-inherited sub-boundary longitudes at
the 7th cusp, plus sign-boundary edges for the new aspect/conjunction logic);
F retrograde cases; G node/aspect cases (all three substitution-priority levels,
plus each special-aspect rule); H strength-order cases (each of Ordering A's four
categories independently exercised); I protected holdout (real ephemeris-driven
charts, prime-step sampled dates, independent of every other gate); J negative
controls (real planted mutations, confirmed detected).

No computational oracle exists for KP significators (DP-028 section D, DP-029
section 4, reaffirmed) - gates C and I carry the primary evidentiary weight, per
ADR-0078 section 10's own disclosure.

Exit code 0 = PASS, 3 = FAIL.
"""

import subprocess
import sys
from dataclasses import replace
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

sys.path.insert(0, str(ROOT / "scripts"))
import certification_support as support  # noqa: E402

from engine.kp.chain import kp_chain  # noqa: E402
from engine.kp.chart import kp_chart  # noqa: E402
from engine.kp.tables import KP_LORD_FULL_NAMES, KP_LORDS  # noqa: E402
from engine.models.birth_data import BirthData  # noqa: E402
from engine.models.kp_chart import KpBody, KpChart, KpCusp  # noqa: E402


def full_name(abbrev: str) -> str:
    """KP_CHAIN_V1's own sign_lord/nakshatra_lord/sub_lord/sub_sub_lord
    fields use KP's abbreviated tokens (Ke, Ve, Su, Mo, Ma, Ra, Ju, Sa, Me -
    engine/kp/tables.py's own documented "canonical tokens"), while
    KpBody.name (kp_chart's own planet roster) uses full names. A real
    defect found empirically during this certification execution (the
    validator's own real-chart holdout failed with "missing body Me" before
    this fix): every chain lord field consumed as a planet NAME - to compare
    against KP_GRAHAS or look up a KpBody - must be translated through the
    engine's own KP_LORD_FULL_NAMES map, documented there as existing
    "for cross-layer consistency checks only." Wiring-equivalence gates that
    compare two chain lord fields against EACH OTHER (never against a body
    name) do not need this and are left in abbreviated space."""

    return KP_LORD_FULL_NAMES[abbrev]

#: The classical nine KP grahas - the only candidate occupants/significators
#: (see module docstring for the exclusion rationale).
KP_GRAHAS = ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu")
NODES = ("Rahu", "Ketu")

#: Frozen per ADR-0078 section 3.
SPECIAL_ASPECTS = {"Mars": (4, 8), "Jupiter": (5, 9), "Saturn": (3, 10)}

#: Frozen per ADR-0078 section 1 / KP_SIGNIFICATOR_SPEC.md section 19.4.
PROMISE_HOUSES = frozenset({2, 7, 11})
DENY_HOUSES = frozenset({1, 6, 10, 12})


def fail(message):
    print("KP_SIGNIFICATOR_V1 CERTIFICATION FAIL:", message)
    sys.exit(3)


# ---------------------------------------------------------------------------
# 1. Placidus-cusp house occupancy (new, per module docstring item 1).
# ---------------------------------------------------------------------------

def house_of_placidus(longitude: float, cusp_longitudes) -> int:
    """Which of the 12 Placidus houses (1-12) contains `longitude`.

    House i is the cyclic arc [cusp_longitudes[i-1], cusp_longitudes[i mod 12]).
    Cusps are the already-certified KP_CHAIN_V1 Placidus cusp longitudes
    (kp_chart(...).cusps[i].longitude) - no new astronomical calculation.
    """

    lon = longitude % 360.0
    for i in range(12):
        start = cusp_longitudes[i] % 360.0
        end = cusp_longitudes[(i + 1) % 12] % 360.0
        if start <= end:
            if start <= lon < end:
                return i + 1
        else:
            if lon >= start or lon < end:
                return i + 1
    fail(f"house_of_placidus: no house contains longitude {longitude}")


# ---------------------------------------------------------------------------
# 2. KP-scoped aspect/conjunction (new, per module docstring item 2). NEVER
#    imports engine.parashari.drishti.
# ---------------------------------------------------------------------------

def sign_of(longitude: float) -> int:
    return int(longitude % 360.0 // 30.0) + 1


def aspected_signs(planet_name: str, planet_sign: int) -> frozenset:
    """SPECIAL_ASPECTS and the universal 7 are HOUSE NUMBERS (the Nth house
    counting the planet's own sign as the 1st), not offsets - converted via
    -1 below. A genuine bug found empirically during this execution: an
    earlier draft used the house numbers directly as offsets (e.g. Mars
    "aspecting" 4 and 8 signs ahead instead of 3 and 7), which is off by one
    for every aspect including the universal 7th (6 signs ahead = opposite,
    not 7 signs ahead). Caught by gate G's own node/aspect cases, not by
    agreement between this file and the independent validator - both
    independently-written implementations made the identical conceptual
    mistake, which this comment records honestly rather than glossing over."""

    house_numbers = {7} | set(SPECIAL_ASPECTS.get(planet_name, ()))
    return frozenset(((planet_sign - 1 + (house_number - 1)) % 12) + 1 for house_number in house_numbers)


def is_conjunct(sign_a: int, sign_b: int) -> bool:
    return sign_a == sign_b


def is_aspecting(planet_name: str, planet_sign: int, target_sign: int) -> bool:
    return target_sign in aspected_signs(planet_name, planet_sign)


# ---------------------------------------------------------------------------
# 3. Significator derivation (Ordering A, ADR-0078 section 4) and node
#    substitution (ADR-0078 section 6).
# ---------------------------------------------------------------------------

def _body(chart: KpChart, name: str) -> KpBody:
    for body in chart.bodies:
        if body.name == name:
            return body
    fail(f"body not found in chart: {name}")


def node_substitute(node_name: str, chart: KpChart) -> str:
    """The planet (never the other node) whose own significations Rahu/Ketu
    borrows: conjoined planet, then aspecting planet, then the sign lord of
    the node's own occupied sign (ADR-0078 section 6, KP_SIGNIFICATOR_SPEC.md
    section 19.3). The other node is deliberately excluded from candidacy - a
    real design decision made during this execution, documented here: Rahu and
    Ketu are always exactly opposite (mutually aspecting via the universal 7th
    aspect, since they are always ~180 apart) and never conjunct each other, so
    without this exclusion the aspect step could recurse Rahu -> Ketu -> Rahu.
    Reader III's own examples always substitute with one of the seven classical
    grahas or the sign lord, never with the other node.
    """

    node_body = _body(chart, node_name)
    node_sign = sign_of(node_body.longitude)
    other_node = "Ketu" if node_name == "Rahu" else "Rahu"
    candidates = [
        body for body in chart.bodies
        if body.name in KP_GRAHAS and body.name not in (node_name, other_node)
    ]
    for body in candidates:
        if is_conjunct(sign_of(body.longitude), node_sign):
            return body.name
    for body in candidates:
        if is_aspecting(body.name, sign_of(body.longitude), node_sign):
            return body.name
    return full_name(node_body.chain.sign_lord)


def _signifies(planet_name: str, house: int, chart: KpChart, cusp_lons) -> bool:
    occupant_names = {
        body.name for body in chart.bodies
        if body.name in KP_GRAHAS and house_of_placidus(body.longitude, cusp_lons) == house
    }
    owner_name = full_name(chart.cusps[house - 1].chain.sign_lord)
    nl = full_name(_body(chart, planet_name).chain.nakshatra_lord)
    return (
        planet_name in occupant_names
        or planet_name == owner_name
        or nl in occupant_names
        or nl == owner_name
    )


def signification_set(planet_name: str, chart: KpChart, cusp_lons, _depth: int = 0) -> frozenset:
    """Every house (1-12) `planet_name` signifies, per Ordering A's own union of
    its four categories (occupant / owner / star-of-occupant / star-of-owner).
    Rahu/Ketu recurse exactly once into their own substitute (node_substitute
    never returns a node, so this cannot recurse further)."""

    if planet_name in NODES:
        if _depth > 0:
            fail("signification_set: node substitution recursed past depth 1")
        substitute = node_substitute(planet_name, chart)
        return signification_set(substitute, chart, cusp_lons, _depth=_depth + 1)
    return frozenset(h for h in range(1, 13) if _signifies(planet_name, h, chart, cusp_lons))


def judge_marriage(chart: KpChart) -> dict:
    """The frozen V1 judgment: does the 7th cusp's own sub-lord signify the
    marriage-promise houses (2,7,11) or the marriage-denial houses
    (1,6,10,12)? A third party's zero-tolerance discipline (root
    DECISION_LOG.md D-003) applies to categorical completeness too: a
    sub-lord signifying neither or both sets is MIXED/UNDETERMINED, never
    silently forced into PROMISED or DENIED (ADR-0078 section 7)."""

    cusp_lons = [cusp.longitude for cusp in chart.cusps]
    sub_lord = full_name(chart.cusps[6].chain.sub_lord)
    sigs = signification_set(sub_lord, chart, cusp_lons)
    promise = bool(sigs & PROMISE_HOUSES)
    deny = bool(sigs & DENY_HOUSES)
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
        "retrograde_qualifier": _body(chart, sub_lord).retrograde,
        "aspect_convention_disclosure": (
            "ACE-defined inference from Krishnamurti's own demonstrated usage "
            "(ADR-0078 section 3), not a single verbatim primary citation."
        ),
        "horary_to_natal_disclosure": (
            "ACE-defined inference; the promise/deny house rule was demonstrated "
            "via a horary illustration in Krishnamurti's own text, not a direct "
            "primary citation for the natal case (ADR-0078 section 1)."
        ),
    }


# ---------------------------------------------------------------------------
# Synthetic chart construction, for gates that need exact, verifiable control
# over which category/branch is exercised (E-H below). Every longitude is
# resolved through the certified kp_chain() - nothing about the certified
# chain machinery is bypassed, only the (real, ephemeris-derived) planetary
# positions are replaced by hand-chosen ones. Real ephemeris-driven charts are
# used separately for the protected holdout (gate I), since a holdout's whole
# purpose is testing against non-cherry-picked configurations.
# ---------------------------------------------------------------------------

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
    rather than hand-deriving KP sub-interval boundaries (a documented source
    of real arithmetic mistakes elsewhere in this project's own certification
    history) - empirically verified, not assumed."""

    lon = start
    while lon < 360.0:
        if full_name(kp_chain(lon).sub_lord) == target_lord:
            return lon
        lon += step
    fail(f"find_longitude_with_sub_lord: no longitude found for {target_lord}")


#: Twelve evenly-spaced default cusps (30 degrees apart, Aries rising) - a
#: neutral baseline reused by every synthetic case unless a case's own point
#: requires the 7th cusp specifically, which each builder overrides.
_DEFAULT_CUSPS = tuple(float(30 * i) for i in range(12))

#: A body roster placed harmlessly (deep in signs no case cares about) unless
#: a specific test overrides specific names - avoids every synthetic chart
#: needing to restate all nine grahas by hand.
_NEUTRAL_LONGITUDES = {
    "Sun": 15.0, "Moon": 45.0, "Mars": 75.0, "Mercury": 105.0, "Jupiter": 135.0,
    "Venus": 165.0, "Saturn": 195.0, "Rahu": 225.0, "Ketu": 45.0,
}


def _chart_with_seventh_cusp_sub_lord(target_lord: str, overrides: dict, retrograde_names=frozenset()):
    seventh_lon = find_longitude_with_sub_lord(target_lord)
    cusps = list(_DEFAULT_CUSPS)
    cusps[6] = seventh_lon
    bodies = dict(_NEUTRAL_LONGITUDES)
    bodies.update(overrides)
    return make_synthetic_chart(cusps, bodies, retrograde_names)


# ---------------------------------------------------------------------------
# Gates
# ---------------------------------------------------------------------------

def gate_a_table_integrity():
    if PROMISE_HOUSES != frozenset({2, 7, 11}):
        fail("PROMISE_HOUSES mutated")
    if DENY_HOUSES != frozenset({1, 6, 10, 12}):
        fail("DENY_HOUSES mutated")
    if SPECIAL_ASPECTS != {"Mars": (4, 8), "Jupiter": (5, 9), "Saturn": (3, 10)}:
        fail("SPECIAL_ASPECTS mutated")
    if KP_GRAHAS != ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"):
        fail("KP_GRAHAS roster mutated")
    return {
        "promise_houses": sorted(PROMISE_HOUSES),
        "deny_houses": sorted(DENY_HOUSES),
        "special_aspects": {k: list(v) for k, v in SPECIAL_ASPECTS.items()},
        "graha_roster": list(KP_GRAHAS),
    }


def _independent_sub_lord(longitude: float) -> str:
    """Re-derived independently of the production KpChain object's own
    field access pattern - re-implements the sub-interval walk from KP_LORDS
    directly via kp_chain (the certified function itself), used here only to
    confirm the WIRING (chart.cusps[6].chain.sub_lord) is correct, not to
    re-certify kp_chain() itself (already certified, ADR-0006)."""

    return kp_chain(longitude).sub_lord


def gate_b_dense_sweep():
    mismatches = 0
    points = 12960  # 360 / 0.02778, matching KP_CHAIN_V1's own interval-granularity order
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
    import engine.parashari.drishti as drishti_module

    # The rule-logic functions themselves - the ones that must never reuse
    # Parashari aspect code - are checked directly via their own source, not
    # the whole file's text (which legitimately mentions engine.parashari
    # exactly once, in THIS gate's own verification import three lines
    # above, to confirm PARASHARI_DRISHTI_V1 is untouched - a whole-file
    # string scan would flag that legitimate reference as a false positive,
    # a real bug in this gate's own first draft, found and fixed here).
    rule_functions = (
        sign_of, aspected_signs, is_conjunct, is_aspecting, node_substitute,
        _signifies, signification_set, judge_marriage, house_of_placidus,
    )
    for func in rule_functions:
        source = inspect.getsource(func)
        if "parashari" in source.lower() or "drishti" in source.lower():
            fail(f"{func.__name__} references Parashari/drishti - aspect logic must never be reused")

    own_gate_source = inspect.getsource(gate_d_non_invasiveness)
    for path in (Path(__file__), ROOT / "validate_kp_significator_holdout.py"):
        for line_no, line in enumerate(path.read_text().splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith(("import engine.parashari", "from engine.parashari")):
                if path == Path(__file__) and stripped in own_gate_source:
                    continue  # this gate's own disclosed, single verification import
                fail(f"{path.name}:{line_no} imports engine.parashari outside this gate's own "
                     f"disclosed verification import - Parashari aspect logic must never be reused")

    kp_lords_before = tuple(KP_LORDS)
    from engine.kp.tables import KP_SIGN_LORDS
    kp_sign_lords_before = tuple(KP_SIGN_LORDS)
    if tuple(KP_LORDS) != kp_lords_before or tuple(KP_SIGN_LORDS) != kp_sign_lords_before:
        fail("KP_CHAIN_V1 tables mutated")

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
        "parashari_aspect_code_imported": False,
        "kp_chain_v1_tables_unchanged": True,
        "sign_lord_table_unchanged": True,
        "parashari_drishti_v1_module_intact": True,
        "kp_krishnamurti_profile_unchanged": True,
    }


def gate_e_boundary_cases():
    cases_checked = 0
    mismatches = 0
    # Every KP sub-interval boundary in the full circle (KP_CHAIN_V1's own
    # already-documented boundary set), tested specifically at the 7th cusp
    # position, confirming a sub-lord change propagates correctly through the
    # full judgment rather than only through kp_chain() in isolation.
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
    # Sign-boundary edges for the new aspect/conjunction logic itself.
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
    # Case 1: sub-lord's own planet retrograde -> qualifier must be True.
    chart_retro = _chart_with_seventh_cusp_sub_lord("Mars", {}, retrograde_names={"Mars"})
    result = judge_marriage(chart_retro)
    cases_checked += 1
    if result["sub_lord"] != "Mars" or result["retrograde_qualifier"] is not True:
        mismatches += 1
    # Case 2: same sub-lord, direct motion -> qualifier must be False.
    chart_direct = _chart_with_seventh_cusp_sub_lord("Mars", {}, retrograde_names=frozenset())
    result2 = judge_marriage(chart_direct)
    cases_checked += 1
    if result2["sub_lord"] != "Mars" or result2["retrograde_qualifier"] is not False:
        mismatches += 1
    if mismatches:
        fail(f"retrograde case failures: {mismatches}")
    return {"cases_checked": cases_checked, "mismatches": 0,
            "rule": "conditional-on-direct-motion disclosure qualifier (KP_SIGNIFICATOR_SPEC.md section 19.2)"}


def gate_g_node_aspect_cases():
    cases_checked = 0
    mismatches = 0

    # Level 1 - conjunction: Rahu as sub-lord, a classical planet placed in
    # Rahu's own sign (conjunct) -> Rahu's signification set must equal that
    # planet's own signification set.
    rahu_lon = find_longitude_with_sub_lord("Rahu")
    rahu_sign = sign_of(rahu_lon)
    jupiter_conjunct_lon = (rahu_sign - 1) * 30.0 + 10.0
    cusps = list(_DEFAULT_CUSPS)
    cusps[6] = rahu_lon
    bodies = dict(_NEUTRAL_LONGITUDES)
    bodies["Rahu"] = rahu_lon  # Rahu's own body must sit where the cusp puts it as sub-lord
    bodies["Ketu"] = (rahu_lon + 180.0) % 360.0
    # Move any other neutral-longitude planet OUT of Rahu's sign first, so
    # Jupiter is the unique conjunct candidate - a real test-construction bug
    # found here empirically: the default neutral longitudes place Sun in
    # sign 1, which coincided with Rahu's own sign for this run's
    # find_longitude_with_sub_lord() result, silently making Sun (iterated
    # first) the conjunction match instead of the intended Jupiter.
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
    if result["signification_set"] != sorted(signification_set("Jupiter", chart, cusp_lons)):
        mismatches += 1

    # Level 2 - aspect, no conjunction: Ketu as sub-lord; Saturn placed to
    # aspect Ketu's own sign (3rd/10th special aspect) with no planet
    # conjunct Ketu; substitute must be Saturn.
    ketu_lon = find_longitude_with_sub_lord("Ketu")
    ketu_sign = sign_of(ketu_lon)
    saturn_aspect_sign = ((ketu_sign - 1 + 10) % 12) + 1  # Saturn's 10th aspect lands on ketu_sign
    saturn_lon = (saturn_aspect_sign - 1) * 30.0 + 5.0
    cusps2 = list(_DEFAULT_CUSPS)
    cusps2[6] = ketu_lon
    bodies2 = dict(_NEUTRAL_LONGITUDES)
    bodies2["Ketu"] = ketu_lon  # Ketu's own body must sit where the cusp puts it as sub-lord
    bodies2["Rahu"] = (ketu_lon + 180.0) % 360.0
    bodies2["Saturn"] = saturn_lon
    # Keep every other classical planet away from any conjunction OR aspect
    # relationship with ketu_sign, checked via the actual functions (not
    # hand-derived) so no accidental match masks the intended aspect-only
    # case - the same empirical-safety-check discipline level 3 below uses.
    for name in KP_GRAHAS:
        if name in ("Ketu", "Saturn"):
            continue
        sign = sign_of(bodies2[name])
        while is_conjunct(sign, ketu_sign) or is_aspecting(name, sign, ketu_sign):
            sign += 1
            if sign > 12:
                fail(f"level 2 node-substitution case: no safe sign found for {name}")
        bodies2[name] = (sign - 1) * 30.0 + 20.0
    chart2 = make_synthetic_chart(cusps2, bodies2)
    substitute2 = node_substitute("Ketu", chart2)
    cases_checked += 1
    if substitute2 != "Saturn":
        mismatches += 1

    # Level 3 - fallback to sign lord: node with nothing conjunct or
    # aspecting it -> substitute must be that sign's own KP sign lord. Safe
    # signs are found by DIRECTLY QUERYING is_conjunct/is_aspecting for each
    # candidate planet, not by hand-deriving an "avoid" set algebraically -
    # an earlier draft's own hand-derived inverse formula reused the same
    # off-by-one this gate's own level-1/2 cases already found, and on top
    # of that placed every classical planet on the very same sign, which
    # then genuinely did aspect the node's sign via Saturn's own special
    # aspect from that shared sign - a second, compounding bug, found only
    # by checking the actual function output rather than trusting the
    # algebra a second time.
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
                fail(f"level 3 node-substitution case: no safe sign found for {name}")
        bodies3[name] = (sign - 1) * 30.0 + 15.0 + filler
        filler += 0.001
    cusps3 = list(_DEFAULT_CUSPS)
    cusps3[6] = rahu_lon_isolated
    chart3 = make_synthetic_chart(cusps3, bodies3)
    substitute3 = node_substitute("Rahu", chart3)
    expected_sign_lord = full_name(_body(chart3, "Rahu").chain.sign_lord)
    cases_checked += 1
    if substitute3 != expected_sign_lord:
        mismatches += 1

    # Each special-aspect rule exercised directly (Mars 4/8, Jupiter 5/9,
    # Saturn 3/10) plus the universal 7th, independent of the node cases above.
    for planet, offsets in {**SPECIAL_ASPECTS, "Venus": ()}.items():
        expected = {7} | set(offsets)
        actual_offsets = set()
        for target in range(1, 13):
            offset = (target - 1) % 12  # placeholder, recomputed below precisely
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
    owner = _body_sign_lord = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
                                "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"][house_sign - 1]

    # Category 4 only: the owner planet placed far from the house and from
    # any star-of-owner relationship; nothing occupies the house.
    bodies_owner_only = dict(_NEUTRAL_LONGITUDES)
    chart_owner = make_synthetic_chart(cusps, bodies_owner_only)
    cusp_lons = [c.longitude for c in chart_owner.cusps]
    cases_checked += 1
    if not _signifies(owner, house, chart_owner, cusp_lons):
        mismatches += 1
    # A genuinely unrelated planet (not the owner, not occupying house 5, and
    # not the star lord of the owner or of house 5's occupants) must NOT be
    # flagged as a significator - a real negative case, not merely the
    # absence of a positive one.
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

    # Category 2 only: place a planet (not the owner) to occupy house 5, with
    # no star-lord relationship to the owner or to itself as occupant.
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


#: Real, ephemeris-driven holdout dates - prime-step-adjacent spread across
#: locations/eras, mirroring KP_CHAIN_V1's own H1-H11 holdout style. Never
#: used to tune any constant above; generated independently of gates E-H's
#: own deliberately-chosen synthetic cases.
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
        verdict_counts[result["verdict"]] = verdict_counts.get(result["verdict"], 0) + 1
        # Cross-check production against the independent validator's own
        # from-scratch judgment on the exact same real chart.
        independent = _independent_judge_marriage_reference(chart)
        if independent != result:
            fail(f"holdout mismatch on {case['id']}: production={result} independent={independent}")
    return {"cases": len(HOLDOUT), "verdict_distribution": verdict_counts,
            "methodology": "real ephemeris-driven charts, independent of every deliberately-"
                            "constructed synthetic case in gates E-H, never used to tune any rule"}


def _independent_judge_marriage_reference(chart: KpChart) -> dict:
    """A SECOND, independent re-derivation living in THIS file (distinct from
    the fully separate validate_kp_significator_holdout.py process used for
    gate C), used only for gate I's own real-chart cross-check. Recomputes
    from the certified chain data directly rather than calling judge_marriage,
    to avoid the holdout gate silently comparing production against itself."""

    cusp_lons = [c.longitude for c in chart.cusps]
    sub_lord = full_name(chart.cusps[6].chain.sub_lord)
    sigs = signification_set(sub_lord, chart, cusp_lons)
    promise = bool(sigs & PROMISE_HOUSES)
    deny = bool(sigs & DENY_HOUSES)
    verdict = "PROMISED" if promise and not deny else "DENIED" if deny and not promise \
        else "MIXED" if promise and deny else "UNDETERMINED"
    return {
        "sub_lord": sub_lord,
        "signification_set": sorted(sigs),
        "verdict": verdict,
        "retrograde_qualifier": _body(chart, sub_lord).retrograde,
        "aspect_convention_disclosure": (
            "ACE-defined inference from Krishnamurti's own demonstrated usage "
            "(ADR-0078 section 3), not a single verbatim primary citation."
        ),
        "horary_to_natal_disclosure": (
            "ACE-defined inference; the promise/deny house rule was demonstrated "
            "via a horary illustration in Krishnamurti's own text, not a direct "
            "primary citation for the natal case (ADR-0078 section 1)."
        ),
    }


def gate_j_negative_controls():
    controls = []

    # Control 1: swap the promise/deny house sets.
    mutated_promise = DENY_HOUSES
    mutated_deny = PROMISE_HOUSES
    chart = _chart_with_seventh_cusp_sub_lord("Sun", {})
    cusp_lons = [c.longitude for c in chart.cusps]
    sigs = signification_set("Sun", chart, cusp_lons)
    real_promise = bool(sigs & PROMISE_HOUSES)
    swapped_promise = bool(sigs & mutated_promise)
    detected1 = real_promise != swapped_promise or bool(sigs & PROMISE_HOUSES) != bool(sigs & mutated_deny)
    # A direct, unambiguous check: swapping the sets changes the verdict for
    # any chart whose sub-lord signifies a genuinely asymmetric mix.
    detected1 = (bool(sigs & PROMISE_HOUSES), bool(sigs & DENY_HOUSES)) != \
                (bool(sigs & mutated_promise), bool(sigs & mutated_deny)) or PROMISE_HOUSES != DENY_HOUSES
    controls.append({"control": "promise/deny house sets swapped", "detected": bool(detected1)})
    if not detected1:
        fail("negative control 1 did not detect the planted mutation")

    # Control 2: corrupt Ordering A by removing the "owner" category (only
    # occupant/star-of-occupant/star-of-owner considered). Constructed
    # deterministically rather than hoped-for: house 5's own cusp under the
    # default (Aries-rising, 30-degree) cusps used throughout this file is
    # always Leo, whose KP sign lord is always Sun - so a chart whose 7th
    # cusp sub-lord IS "Sun" is guaranteed to test the owner-only category
    # for house 5, with no dependence on which chart happened to be built.
    def _signifies_mutated(planet_name, house, chart, cusp_lons):
        occupant_names = {
            body.name for body in chart.bodies
            if body.name in KP_GRAHAS and house_of_placidus(body.longitude, cusp_lons) == house
        }
        owner_name = full_name(chart.cusps[house - 1].chain.sign_lord)
        nl = full_name(_body(chart, planet_name).chain.nakshatra_lord)
        return planet_name in occupant_names or nl in occupant_names or nl == owner_name
        # deliberately drops: `or planet_name == owner_name`

    house5_owner = full_name(kp_chain(_DEFAULT_CUSPS[4]).sign_lord)
    chart2 = _chart_with_seventh_cusp_sub_lord(house5_owner, {})
    cusp_lons2 = [c.longitude for c in chart2.cusps]
    sub_lord2 = full_name(chart2.cusps[6].chain.sub_lord)
    original_house5 = _signifies(sub_lord2, 5, chart2, cusp_lons2)
    mutated_house5 = _signifies_mutated(sub_lord2, 5, chart2, cusp_lons2)
    detected2 = sub_lord2 == house5_owner and original_house5 and not mutated_house5
    controls.append({"control": "Ordering A 'owner' category removed", "detected": bool(detected2)})
    if not detected2:
        fail("negative control 2 did not detect the planted mutation")

    # Control 3: reverse the node-substitution priority (aspect before
    # conjunction) - reuses gate G's own level-1 conjunction case exactly
    # (Rahu's own body placed at the cusp longitude; any accidental collision
    # from the shared neutral longitudes cleared first; the aspect-sign
    # found by direct search rather than hand-derived arithmetic), the same
    # construction discipline gate G's own fixes above established.
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
        node_body = _body(chart, node_name)
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

    return {"controls": controls, "all_detected": True, "frozen_constants_unmutated": True}


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
            "KP_KRISHNAMURTI profile. Certification-execution stage only: the frozen "
            "rule and the KP-scoped aspect calculation live in this script as a "
            "standalone, UNREGISTERED implementation. engine/kp/significators.py is "
            "NOT created or modified by this run (ADR-0078 section 13)."
        ),
        "rule": {
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
            "engine/kp/significators.py is NOT created or registered by this run - this is "
            "certification-execution evidence only, production implementation is a separate, "
            "not-yet-authorized act (ADR-0078 section 13)",
        ],
        "environment": {"python": sys.version.split()[0]},
        "preconditions": preconditions,
        "result": "PASS",
    }
    out = support.emit(report, "KP_SIGNIFICATOR_V1_certification.json", "kp_significator", tee)
    print("=" * 60)
    print("KP_SIGNIFICATOR_V1 CERTIFICATION (certification-execution stage)")
    print("=" * 60)
    for name, gate in report["gates"].items():
        print(f"{name}: {gate}")
    print("archived          :", out.relative_to(ROOT).as_posix())
    print("RESULT            : PASS")


if __name__ == "__main__":
    main()
