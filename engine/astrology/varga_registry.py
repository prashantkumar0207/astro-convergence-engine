"""
Varga Registry (Phase A)

Maps (division, school) to a varga rule. School is ALWAYS explicit
in the registry key; a varga's default school is a documented,
per-varga constant resolved by the dispatcher, mirroring the
ayanamsa-profile discipline (nothing silent).

PHASE A REGISTERS NO PRODUCTION VARGA. D1, D9 and D10 remain
hard-wired to their certified implementations in the dispatcher;
this registry exists so future vargas (Phase D of the ADR) can be
added one at a time under the full certification protocol. Any
registration therefore requires an accompanying certification
artifact per the ADR section 5 checklist.
"""

from engine.astrology.varga_rules import (
    CyclicVargaRule,
    SegmentVargaRule,
)


class UnsupportedVargaError(NotImplementedError):
    """Raised when a divisional chart or school is not implemented."""


#: The Parashara rules are the documented default school for every
#: varga this project implements (per-varga overrides are possible
#: but must be registered explicitly).
DEFAULT_SCHOOL = "parashara"

#: (division, school) -> rule. Intentionally EMPTY in Phase A.
_REGISTRY: dict[tuple[int, str], object] = {}


def register_varga_rule(division: int, school: str, rule) -> None:
    """
    Register a rule for (division, school).

    Guarded: only valid rule objects are accepted, duplicates are
    rejected, and divisions 1, 9 and 10 are refused because their
    certified implementations are not routed through the registry
    (ADR migration Phase C is the only sanctioned path to change
    that, and it is explicitly out of Phase A scope).

    Also guarded (B-01, `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md`):
    a rule's own declared division identity must match the division it
    is being registered under - `rule.divisions` for CyclicVargaRule,
    `rule.division` for SegmentVargaRule. Without this a rule built
    for one division could be silently registered under a different
    one, producing a well-formed, fully self-consistent, completely
    wrong classification, undetected by every existing gate (they
    compare registry KEYS only, never rule content).

    `division` must be a positive integer other than 1, 9 or 10; no
    further upper bound is enforced. No document in this repository
    specifies an authoritative maximum (the highest classical varga
    named anywhere here is D60), and inventing one would itself be an
    unauthorised limit of exactly the kind this project's governance
    forbids adding without a cited source.
    """
    if not isinstance(rule, (CyclicVargaRule, SegmentVargaRule)):
        raise TypeError(
            f"rule must be CyclicVargaRule or SegmentVargaRule, "
            f"got {type(rule)!r}"
        )

    if not isinstance(division, int) or isinstance(division, bool):
        raise ValueError(
            f"division must be an int, got {type(division).__name__}"
        )

    if division in (1, 9, 10):
        raise ValueError(
            f"D{division} is served by a certified implementation and "
            "cannot be re-registered through the generic registry "
            "(ADR Phase C governs any migration)."
        )

    if division < 2:
        raise ValueError(f"division must be >= 2, got {division}")

    if not isinstance(school, str) or not school:
        raise ValueError("school must be a non-empty string")

    if isinstance(rule, CyclicVargaRule):
        if rule.divisions != division:
            raise ValueError(
                f"rule.divisions ({rule.divisions}) does not match the "
                f"division it is being registered under (D{division})"
            )
    else:
        if rule.division != division:
            raise ValueError(
                f"rule.division ({rule.division}) does not match the "
                f"division it is being registered under (D{division})"
            )

    key = (division, school)

    if key in _REGISTRY:
        raise ValueError(f"{key} is already registered")

    _REGISTRY[key] = rule


def unregister_varga_rule(division: int, school: str) -> None:
    """Remove a registration (test hygiene; no production use)."""
    _REGISTRY.pop((division, school), None)


def get_varga_rule(division: int, school: str):
    """
    Return the rule for (division, school) or raise
    UnsupportedVargaError naming what IS registered.
    """
    key = (division, school)

    if key not in _REGISTRY:
        registered = sorted(_REGISTRY.keys())
        raise UnsupportedVargaError(
            f"No rule registered for D{division} school '{school}'. "
            f"Registered: {registered if registered else 'none'}; "
            f"D1, D9, D10 are served by certified implementations."
        )

    return _REGISTRY[key]


def registered_vargas() -> tuple[tuple[int, str], ...]:
    """All registered (division, school) keys, sorted."""
    return tuple(sorted(_REGISTRY.keys()))
