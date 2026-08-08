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
    """
    if not isinstance(rule, (CyclicVargaRule, SegmentVargaRule)):
        raise TypeError(
            f"rule must be CyclicVargaRule or SegmentVargaRule, "
            f"got {type(rule)!r}"
        )

    if division in (1, 9, 10):
        raise ValueError(
            f"D{division} is served by a certified implementation and "
            "cannot be re-registered through the generic registry "
            "(ADR Phase C governs any migration)."
        )

    if not isinstance(school, str) or not school:
        raise ValueError("school must be a non-empty string")

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
