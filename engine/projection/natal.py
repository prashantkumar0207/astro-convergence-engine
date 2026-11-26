"""Verified natal projection and the evidence store's natal verifier (ADR-0134 U2, U5, U6; H4 s13).

An untimed natal evidence item has exactly one correct form for its chart and its rule, and expected_item() builds it:
the entity chart's recorded birth input is run through the certified kernel (engine.calculations.calculate under
PARASHARI_LAHIRI, then PARASHARI_HOUSE_LORD_V1), the published synthetic Parashari rule's conditions are evaluated on
that chart, and the rule must fire. A rule that does not fire is not evidence of its opposite, and no item is made.

- verify_natal_item() is the store's natal verifier: on every persist and every checked read of an untimed item, it
  rebuilds the expected item from the entity chart and refuses any difference. Forged facts, chart context, polarity,
  strength, completeness statements or chart are refused however the row was written.
- natal_store() opens an evidence store that holds this verifier. A store without it refuses every untimed item.
- project() turns one verified, fired application record into evidence, only if the record's chart is the kernel's
  recomputation of the entity chart's recorded birth input: a substituted chart is refused.

The timing is always UntimedNatal(NATAL_PLACEMENT): no date, window or label is ever produced. No genuine rule is
applied (`rule_version()` and `application.admit` both refuse one; ADR-0132 s4; ADR-0133 D2 inactive). Nothing here
predicts, scores or computes confidence, and every chart is synthetic.
"""

from __future__ import annotations

import re
from dataclasses import fields
from pathlib import Path

import engine.evidence.rule_registry as rule_registry
from engine.astronomy.profile import PARASHARI_LAHIRI
from engine.calculations.calculations import calculate
from engine.evidence.entity import ChartCandidate, DataClass, RecordProvenance
from engine.evidence.evidence import (
    CONFIDENCE_COMPONENTS, CalculatedInput, ChartContext, ChartReference, Confidence, Domain, EvidenceItem, Lineage,
    ProducingSystem, RuleReference, UntimedBasis, UntimedNatal,
)
from engine.evidence.evidence_identifiers import EvidenceId, RuleId
from engine.evidence.evidence_store import UNTIMED_SCHEMA_VERSION, EvidenceStore
from engine.evidence.identifiers import EntityId
from engine.interpretation import application
from engine.interpretation.conditions import Evaluation, evaluate
from engine.models.birth_data import BirthData

#: Where every projected item says it came from.
PROJECTION_PROVENANCE = RecordProvenance(source="the verified natal projection (ADR-0134)",
                                         method="certified-kernel recomputation of the entity chart",
                                         schema_version=UNTIMED_SCHEMA_VERSION)
_LOCAL_DATETIME = re.compile(r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})")


class ProjectionError(ValueError):
    """A record, chart or item the natal projection refuses."""


def birth_data(candidate: ChartCandidate) -> BirthData:
    """The kernel's input, exactly as the entity chart records it: local date and time to the second, IANA timezone,
    latitude and longitude. Anything else is refused, never guessed."""

    if type(candidate) is not ChartCandidate:
        raise ProjectionError("a natal projection reads an entity's recorded ChartCandidate")
    origin = candidate.origin
    match = _LOCAL_DATETIME.fullmatch(origin.local_datetime)
    if match is None:
        raise ProjectionError(f"the chart's recorded local time {origin.local_datetime!r} is not YYYY-MM-DDTHH:MM:SS")
    year, month, day, hour, minute, second = (int(part) for part in match.groups())
    return BirthData(year, month, day, hour, minute, float(second), origin.latitude, origin.longitude, origin.timezone)


def kernel_chart(candidate: ChartCandidate) -> application.SyntheticChart:
    """The entity chart, recomputed from its recorded birth input by the certified kernel."""

    snapshot = calculate(birth_data(candidate), profile=PARASHARI_LAHIRI).snapshot
    return application.SyntheticChart(application.ChartOrigin.from_snapshot(snapshot), DataClass.SYNTHETIC)


def fact_text(evaluation: Evaluation) -> str:
    """One evaluation's certified facts, as the item's calculated input records them."""

    return (f"{evaluation.kind} ({', '.join(f'{name} {value}' for name, value in evaluation.parameters)}): "
            f"{', '.join(f'{name} {value}' for name, value in evaluation.facts)}")


def natal_context(evaluations: tuple) -> ChartContext:
    """The D1 planets, houses and signs the evaluations name, sorted."""

    planets, houses, signs = set(), set(), set()
    for evaluation in evaluations:
        parameters, facts = dict(evaluation.parameters), dict(evaluation.facts)
        if evaluation.kind == "house_lord_in_house":
            planets.add(facts["lord"])
            houses.update((parameters["lord_of"], parameters["house"], facts["lord_house"]))
            signs.add(facts["house_sign"])
        elif evaluation.kind == "planet_in_house":
            planets.add(parameters["planet"])
            houses.update((parameters["house"], facts["planet_house"]))
        else:
            planets.add(parameters["planet"])
            signs.update((parameters["sign"], facts["planet_sign"]))
    return ChartContext(varga="D1", planets=tuple(sorted(planets)), houses=tuple(sorted(houses)),
                        signs=tuple(sorted(signs)), significators=())


def expected_item(entity: EntityId, chart: ChartReference, candidate: ChartCandidate, rule: RuleReference) -> EvidenceItem:
    """The one untimed item the certified kernel and the published rule give for this chart. Refused when the rule is
    not a published synthetic Parashari rule, or does not fire on the chart."""

    registry = rule_registry.pinned()
    try:
        published = registry.lookup(rule.rule, rule.version, rule.variant)
        version = registry.rule_version(rule.rule, rule.version, rule.variant)
    except rule_registry.RegistryError as exc:
        raise ProjectionError(f"{rule.rule} v{rule.version} {rule.variant!r} is not a published synthetic rule: {exc}") from exc
    try:
        application.admit(published)
        facts = kernel_chart(candidate).chart()
        evaluations = tuple(evaluate(condition, facts)
                            for condition in (published.condition, *published.activation_conditions))
    except ValueError as exc:
        raise ProjectionError(f"{rule.rule} cannot be applied to this chart: {exc}") from exc
    if not all(evaluation.holds for evaluation in evaluations):
        raise ProjectionError(f"{rule.rule} v{rule.version} {rule.variant!r} does not fire on this chart; a rule that does "
                              f"not fire is not evidence of its opposite (ADR-0134 U5)")
    provenance = facts.provenance
    texts = []
    for evaluation in evaluations:
        if fact_text(evaluation) not in texts:
            texts.append(fact_text(evaluation))
    return EvidenceItem(
        entity=entity, domain=Domain.JATAKA, question=None, producing_system=ProducingSystem.PARASHARI, rule=rule,
        declared_strength=version.spec.declared_strength, measured_reliability=None,
        lineage=Lineage(inputs=tuple(CalculatedInput(fact=text, provenance=provenance) for text in texts),
                        inputs_complete=True, derivations_complete=True),
        chart=chart, chart_context=natal_context(evaluations),
        timing=UntimedNatal(basis=UntimedBasis.NATAL_PLACEMENT), polarity=published.polarity,
        confidence=Confidence(**{name: None for name in CONFIDENCE_COMPONENTS}), historical_performance=None,
        derived_from=(), recomputes=None, provenance=PROJECTION_PROVENANCE, data_class=DataClass.SYNTHETIC)


def verify_natal_item(item: EvidenceItem, candidate: ChartCandidate) -> None:
    """The evidence store's natal verifier: the item must be exactly expected_item() for its entity, chart and rule."""

    if type(item) is not EvidenceItem or type(item.timing) is not UntimedNatal:
        raise ProjectionError("the natal verifier checks untimed natal evidence items only")
    expected = expected_item(item.entity, item.chart, candidate, item.rule)
    differing = [field.name for field in fields(EvidenceItem)
                 if item.__getattribute__(field.name) != expected.__getattribute__(field.name)]
    if differing:
        raise ProjectionError(f"the item differs from its chart's certified natal evidence in {', '.join(differing)}")


def natal_store(path: Path | str) -> EvidenceStore:
    """An evidence store that admits untimed natal items, each verified by verify_natal_item on write and on read."""

    return EvidenceStore(path, natal_verifier=verify_natal_item)


def entity_chart(store: EvidenceStore, entity: EntityId, chart: ChartReference) -> ChartCandidate:
    """The chart an entity records at a revision, from the store's own entity records."""

    history = store.entities.history(entity)
    if chart.entity_revision > len(history):
        raise ProjectionError(f"{entity} has no revision {chart.entity_revision}")
    _number, subject, _reason = history[chart.entity_revision - 1]
    found = [candidate for candidate in subject.charts if candidate.label == chart.chart_label]
    if len(found) != 1:
        raise ProjectionError(f"{chart.chart_label!r} is not one chart of {entity}")
    return found[0]


def require_fired(record: application.ApplicationRecord) -> None:
    if record.fired is not True:
        raise ProjectionError("a rule that did not fire is not evidence of its opposite; nothing is projected (ADR-0134 U5)")


def require_entity_chart(chart: application.SyntheticChart, candidate: ChartCandidate) -> None:
    if chart.origin.digest() != kernel_chart(candidate).origin.digest():
        raise ProjectionError("the record's chart is not the certified kernel's recomputation of the entity chart's "
                              "recorded birth input (ADR-0134 U5)")


def project(store: EvidenceStore, record: application.ApplicationRecord, chart: application.SyntheticChart,
            entity: EntityId, at: ChartReference) -> EvidenceId:
    """Persist the untimed evidence of one verified, fired application record, made on the entity chart's kernel
    recomputation. Everything else is refused (ADR-0134 U5)."""

    if store.natal_verifier is not verify_natal_item:
        raise ProjectionError("natal evidence is projected only into a store holding the natal verifier (natal_store)")
    try:
        application.verify(record, chart)
    except application.ApplicationError as exc:
        raise ProjectionError(f"the application record does not verify against its chart: {exc}") from exc
    require_fired(record)
    candidate = entity_chart(store, entity, at)
    require_entity_chart(chart, candidate)
    reference = RuleReference(rule=RuleId(record.rule), version=record.version, variant=record.variant)
    return store.persist(expected_item(entity, at, candidate, reference))
