"""Closed condition evaluation (ADR-0133 I2; PROPOSED).

A rule's condition is data (engine/evidence/rule_registry.py, Condition). This module answers it for one chart, and
only for the kinds whose every input is a certified PARASHARI_HOUSE_LORD_V1 fact:

  house_lord_in_house  the lord of house `lord_of` occupies house `house`;
  planet_in_house      `planet` occupies house `house`;
  planet_in_sign       `planet` occupies sign `sign`.

Every other kind is refused, including `cusp_sublord_signifies`, which is a KP condition no certified Parashari fact
answers. The input must be the certified chart type, computed under PARASHARI_LAHIRI. Each evaluation records the
facts it read, so its answer can be checked again from them alone.
"""

from __future__ import annotations

from dataclasses import dataclass

from engine.evidence.rule_registry import Condition
from engine.parashari.house_lord import HouseLordChart

#: The certified artifact every evaluated fact comes from.
CERTIFIED_INPUT = "PARASHARI_HOUSE_LORD_V1"
#: The kinds evaluated here, and nothing else.
EVALUATED_KINDS = ("house_lord_in_house", "planet_in_house", "planet_in_sign")
#: The facts each kind reads, by name, in the order they are recorded.
FACT_NAMES = {
    "house_lord_in_house": ("house_sign", "lord", "lord_house"),
    "planet_in_house": ("planet_house",),
    "planet_in_sign": ("planet_sign",),
}
PROFILE = "parashari_lahiri"


class ConditionError(ValueError):
    """A condition or chart this module does not evaluate."""


@dataclass(frozen=True, slots=True)
class Evaluation:
    """One condition answered for one chart: its kind and parameters, the certified facts read, and the answer."""

    kind: str
    parameters: tuple
    facts: tuple
    holds: bool


def answer(kind: str, parameters: dict, facts: dict) -> bool:
    """The answer a kind gives from recorded facts alone. Used to evaluate, and again to verify a record."""

    if kind == "house_lord_in_house":
        return facts["lord_house"] == parameters["house"]
    if kind == "planet_in_house":
        return facts["planet_house"] == parameters["house"]
    if kind == "planet_in_sign":
        return facts["planet_sign"] == parameters["sign"]
    raise ConditionError(f"condition kind {kind!r} is not evaluated here; only {EVALUATED_KINDS} are (ADR-0133 I2)")


def evaluate(condition: Condition, chart: HouseLordChart) -> Evaluation:
    """Answer one condition from the chart's certified facts. Fails closed on anything undeclared."""

    if not isinstance(condition, Condition):
        raise ConditionError("only a registry Condition is evaluated")
    if type(chart) is not HouseLordChart:
        raise ConditionError(f"conditions are evaluated only from a certified {CERTIFIED_INPUT} chart")
    if chart.provenance is None or chart.provenance.profile_name != PROFILE:
        raise ConditionError(f"the chart was not computed under {PROFILE}")
    if condition.kind not in EVALUATED_KINDS:
        raise ConditionError(f"condition kind {condition.kind!r} is not evaluated here; only {EVALUATED_KINDS} are "
                             f"(ADR-0133 I2)")
    if len(chart.lordships) != 12 or len(chart.placements) != 9:
        raise ConditionError("the chart does not carry twelve lordships and nine placements")
    parameters = dict(condition.parameters)
    if condition.kind == "house_lord_in_house":
        item = chart.lordship(parameters["lord_of"])
        facts = {"house_sign": item.sign, "lord": item.lord, "lord_house": item.lord_house}
    else:
        placed = chart.placement(parameters["planet"])
        facts = {"planet_house": placed.house} if condition.kind == "planet_in_house" else {"planet_sign": placed.sign}
    return Evaluation(kind=condition.kind, parameters=tuple(sorted(condition.parameters)),
                      facts=tuple((name, facts[name]) for name in FACT_NAMES[condition.kind]),
                      holds=answer(condition.kind, parameters, facts))
