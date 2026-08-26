"""
KP_SIGNIFICATOR_V1 (ADR-0078, certified per the certification-execution
recorded in docs/DECISION_LOG.md).

A single, narrow, frozen judgment: does the 7th house cusp's KP cuspal
sub-lord signify the marriage-promise house group (2, 7, 11) or the
marriage-denial group (1, 6, 10, 12), for a natal chart under the
KP_KRISHNAMURTI profile. The frozen rule, its own primary-source
provenance, and every disclosed non-claim are recorded in ADR-0078 and
KP_SIGNIFICATOR_SPEC.md; this module implements exactly that rule and
does not extend it.

Isolated per the school-separation rule (matching engine/kp/__init__.py's
own discipline): this module NEVER imports engine.parashari (no Parashari
aspect logic is reused - the KP-scoped aspect/conjunction calculation
below is independently implemented, sharing only the classical angular
rules Krishnamurti's own text demonstrates) and is never imported by
Parashari, Varga, or Tier-0 modules. It consumes only the already-
certified KP_CHAIN_V1 substrate (engine.kp.chain, engine.kp.chart) and
the classical sign-lordship table (engine.astrology.sign_lord).

Explicit non-claims, preserved exactly as certified: Four Step Theory and
Ruling Planets are out of scope (ADR-0027 Decision 3); horary/Prashna
judgment generally is out of scope; charts with cusps inside the
undefined polar-latitude band are unverified (DP-025, still deferred);
the horary-to-natal application of the promise/deny house groups is a
disclosed ACE-defined inference, not a direct primary citation for the
natal case; the aspect/conjunction convention is likewise a disclosed
ACE-defined inference from Krishnamurti's own demonstrated usage, not a
single verbatim citation; the children/5th-house parallel is not
covered; no computational oracle corroborates this design - certification
rests on an independent validator and a protected holdout alone;
Uranus/Neptune/Pluto and the Ascendant are excluded from the candidate
occupant/significator pool.
"""

import hashlib

from engine.kp.tables import KP_LORD_FULL_NAMES
from engine.models.kp_chart import KpChart
from engine.models.kp_significator import KpSignificatorJudgment

#: The classical nine KP grahas - the only candidate occupants/
#: significators. Uranus/Neptune/Pluto and the Ascendant are excluded:
#: they are never KP dasha lords or nakshatra lords under the certified
#: KP_LORDS cycle (engine.kp.tables), and are never treated as
#: significators in the retrieved primary text (ADR-0078 module docstring
#: non-claims).
KP_GRAHAS = ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu")
NODES = ("Rahu", "Ketu")

#: Frozen per ADR-0078 section 3: house numbers (the Nth house counting a
#: planet's own sign as the 1st), not offsets - converted via -1 wherever
#: consumed (aspected_signs below).
SPECIAL_ASPECTS = {"Mars": (4, 8), "Jupiter": (5, 9), "Saturn": (3, 10)}

#: Frozen per ADR-0078 section 1 / KP_SIGNIFICATOR_SPEC.md section 19.4.
PROMISE_HOUSES = frozenset({2, 7, 11})
DENY_HOUSES = frozenset({1, 6, 10, 12})

_ASPECT_CONVENTION_DISCLOSURE = (
    "ACE-defined inference from Krishnamurti's own demonstrated usage "
    "(ADR-0078 section 3), not a single verbatim primary citation."
)
_HORARY_TO_NATAL_DISCLOSURE = (
    "ACE-defined inference; the promise/deny house rule was demonstrated "
    "via a horary illustration in Krishnamurti's own text, not a direct "
    "primary citation for the natal case (ADR-0078 section 1)."
)


def full_name(abbrev: str) -> str:
    """KP_CHAIN_V1's own sign_lord/nakshatra_lord/sub_lord/sub_sub_lord
    fields use KP's abbreviated tokens (engine/kp/tables.py's own
    documented "canonical tokens"), while KpBody.name uses full planet
    names. Every chain lord field consumed as a planet name - to compare
    against KP_GRAHAS or look up a KpBody - must be translated through
    the engine's own KP_LORD_FULL_NAMES map, documented there as existing
    "for cross-layer consistency checks only"."""

    return KP_LORD_FULL_NAMES[abbrev]


def house_of_placidus(longitude: float, cusp_longitudes) -> int:
    """Which of the 12 Placidus houses (1-12) contains `longitude`.

    House i is the cyclic arc [cusp_longitudes[i-1], cusp_longitudes[i mod
    12]). `cusp_longitudes` are the already-certified KP_CHAIN_V1 Placidus
    cusp longitudes (kp_chart(...).cusps[i].longitude) - no new
    astronomical calculation. KP's own cuspal sub-lord theory is defined
    on unequal Placidus cusps, not the whole-sign or equal-house systems
    used elsewhere in this project's Parashari layer."""

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
    raise ValueError(f"house_of_placidus: no house contains longitude {longitude}")


def sign_of(longitude: float) -> int:
    return int(longitude % 360.0 // 30.0) + 1


def aspected_signs(planet_name: str, planet_sign: int) -> frozenset:
    """The classical whole-sign Vedic graha-drishti scheme (ADR-0078
    section 3), independently implemented - never imported from or
    reusing engine.parashari.drishti (PARASHARI_DRISHTI_V1). SPECIAL_ASPECTS
    and the universal 7 are HOUSE NUMBERS, converted to a zodiacal offset
    via -1 (the 7th house from a sign is 6 signs ahead - opposite - not 7
    signs ahead)."""

    house_numbers = {7} | set(SPECIAL_ASPECTS.get(planet_name, ()))
    return frozenset(((planet_sign - 1 + (house_number - 1)) % 12) + 1 for house_number in house_numbers)


def is_conjunct(sign_a: int, sign_b: int) -> bool:
    """Same-sign occupancy - no orb, per ADR-0078 section 3's own resolution."""

    return sign_a == sign_b


def is_aspecting(planet_name: str, planet_sign: int, target_sign: int) -> bool:
    return target_sign in aspected_signs(planet_name, planet_sign)


def _body(chart: KpChart, name: str):
    for body in chart.bodies:
        if body.name == name:
            return body
    raise ValueError(f"body not found in chart: {name}")


def node_substitute(node_name: str, chart: KpChart) -> str:
    """The planet (never the other node) whose own significations Rahu/Ketu
    borrows: conjoined planet, then aspecting planet, then the sign lord of
    the node's own occupied sign (ADR-0078 section 6). The other node is
    deliberately excluded from candidacy: Rahu and Ketu are always exactly
    opposite (mutually aspecting via the universal 7th aspect) and never
    conjunct each other, so without this exclusion the aspect step could
    recurse Rahu -> Ketu -> Rahu. Reader III's own examples always
    substitute with one of the seven classical grahas or the sign lord,
    never with the other node."""

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
    """Every house (1-12) `planet_name` signifies, per Ordering A's own
    union of its four categories: star of occupant, occupant, star of
    owner, owner (ADR-0078 section 4, strongest to weakest - a union test
    for this V1's own binary promise/deny judgment, not a priority
    selection). Rahu/Ketu recurse exactly once into their own substitute
    (node_substitute never returns a node, so this cannot recurse
    further)."""

    if planet_name in NODES:
        if _depth > 0:
            raise AssertionError("signification_set: node substitution recursed past depth 1")
        substitute = node_substitute(planet_name, chart)
        return signification_set(substitute, chart, cusp_lons, _depth=_depth + 1)
    return frozenset(h for h in range(1, 13) if _signifies(planet_name, h, chart, cusp_lons))


def judge_marriage(chart: KpChart) -> KpSignificatorJudgment:
    """The frozen KP_SIGNIFICATOR_V1 judgment (ADR-0078): does the 7th
    cusp's own sub-lord signify the marriage-promise houses (2, 7, 11) or
    the marriage-denial houses (1, 6, 10, 12)? A sub-lord signifying
    neither or both sets is MIXED/UNDETERMINED, never silently forced into
    PROMISED or DENIED (ADR-0078 section 7; root DECISION_LOG.md D-003's
    zero-tolerance discipline extended to categorical completeness).

    `chart` must be a KpChart built under the ratified KP_KRISHNAMURTI
    profile (engine.kp.chart.kp_chart/kp_chart_from_snapshot already
    enforce this)."""

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
    return KpSignificatorJudgment(
        sub_lord=sub_lord,
        signification_set=tuple(sorted(sigs)),
        verdict=verdict,
        retrograde_qualifier=_body(chart, sub_lord).retrograde,
        aspect_convention_disclosure=_ASPECT_CONVENTION_DISCLOSURE,
        horary_to_natal_disclosure=_HORARY_TO_NATAL_DISCLOSURE,
    )


def rule_content_sha256() -> str:
    """Content fingerprint of the frozen rule constants, for certification
    pinning (mirrors engine.astrology.varga_rules.rule_content_sha256's
    own pattern, independently implemented here rather than imported,
    since that function is scoped to CyclicVargaRule objects, a different
    shape of frozen data)."""

    payload = repr((
        sorted(PROMISE_HOUSES),
        sorted(DENY_HOUSES),
        sorted(SPECIAL_ASPECTS.items()),
        KP_GRAHAS,
    )).encode()
    return hashlib.sha256(payload).hexdigest()
