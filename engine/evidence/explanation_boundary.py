"""The explanation boundary (ADR-0130; H5 s3; the Charter's "Complete product contract" s7; Q8 s7 entry criterion).

An explanation is never accepted as text. It is a structured candidate that only names references: the evidence items
in scope, and for each segment a closed kind and, where the kind needs one, a closed field or an input index. There is
no free-text field anywhere in the contract, so generated text has nowhere to state a rule, apply one, or override a
calculated value.

A no-answer segment names its kind and nothing else, and renders one neutral abstention. A candidate never selects a
reason for not answering: every such reason would be a claim about the evidence or the question that the candidate
chose and the boundary cannot verify, so a candidate that offers one is refused.

- parse() reads a candidate strictly and fails closed: any key, kind, field or type the contract does not define is
  refused, as is any string where a reference is required.
- admit() resolves every reference through trusted data only: each item through the evidence store's checked reads
  (ADR-0124, ADR-0125, ADR-0127), each rule statement or citation through the pinned registry. Anything that does not
  resolve is refused.
- render() produces every sentence deterministically from that trusted data. Nothing in a candidate becomes text.

There is no LLM client and no network access here. A later LLM may only submit a candidate; what a user reads is
always what render() produces from the evidence and the registry.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import engine.evidence.rule_registry as rule_registry
from engine.evidence.evidence import CONFIDENCE_COMPONENTS, EvidenceItem
from engine.evidence.evidence_identifiers import EvidenceId, IdentifierError
from engine.evidence.evidence_store import EvidenceStore
from engine.evidence.store import StoreError

EXPLANATION_SCHEMA = "ace-explanation-candidate-v1"


class BoundaryError(ValueError):
    """A candidate explanation the boundary refuses."""


class SegmentKind(Enum):
    RULE_STATEMENT = "rule_statement"
    RULE_CITATION = "rule_citation"
    CHART_FACT = "chart_fact"
    CALCULATED_INPUT = "calculated_input"
    TIMING = "timing"
    POLARITY = "polarity"
    UNCERTAINTY = "uncertainty"
    NO_ANSWER = "no_answer"


#: The one sentence a no-answer segment renders. It asserts nothing about the evidence, the rules or the question.
ABSTENTION_TEXT = "No answer is given."
CHART_FIELDS = ("varga", "planets", "houses", "signs", "significators")
UNCERTAINTY_FIELDS = CONFIDENCE_COMPONENTS + ("historical_performance",)
#: Each kind's keys, exactly. Nothing else may appear in a segment.
SEGMENT_KEYS = {
    SegmentKind.RULE_STATEMENT: ("kind", "evidence"),
    SegmentKind.RULE_CITATION: ("kind", "evidence"),
    SegmentKind.CHART_FACT: ("kind", "evidence", "field"),
    SegmentKind.CALCULATED_INPUT: ("kind", "evidence", "index"),
    SegmentKind.TIMING: ("kind", "evidence"),
    SegmentKind.POLARITY: ("kind", "evidence"),
    SegmentKind.UNCERTAINTY: ("kind", "evidence", "field"),
    SegmentKind.NO_ANSWER: ("kind",),
}
FIELDS = {SegmentKind.CHART_FACT: CHART_FIELDS, SegmentKind.UNCERTAINTY: UNCERTAINTY_FIELDS}
CANDIDATE_KEYS = ("schema", "scope", "segments")


@dataclass(frozen=True, slots=True)
class Segment:
    """One reference. `field` is one of the closed field names for its kind; it is never text to show."""

    kind: SegmentKind
    evidence: EvidenceId | None = None
    field: str | None = None
    index: int | None = None


@dataclass(frozen=True, slots=True)
class Explanation:
    scope: tuple
    segments: tuple


def _exact(name: str, data, keys: tuple) -> dict:
    if not isinstance(data, dict) or set(data) != set(keys):
        found = sorted(data) if isinstance(data, dict) else type(data).__name__
        raise BoundaryError(f"{name} carries exactly {list(keys)}; refused: {found}. A candidate holds references, "
                            f"never text (ADR-0130)")
    return data


def _evidence_id(value) -> EvidenceId:
    if not isinstance(value, str):
        raise BoundaryError("an evidence reference is an EVD identifier")
    try:
        return EvidenceId(value)
    except IdentifierError as exc:
        raise BoundaryError(f"not an EVD identifier: {value!r}") from exc


def parse(candidate) -> Explanation:
    """Read a candidate strictly. Every key, kind, field and type must be the contract's own; anything else fails."""

    data = _exact("a candidate explanation", candidate, CANDIDATE_KEYS)
    if data["schema"] != EXPLANATION_SCHEMA:
        raise BoundaryError("not a candidate explanation of this schema")
    if not isinstance(data["scope"], list) or not data["scope"]:
        raise BoundaryError("a candidate names the evidence in its scope")
    scope = tuple(_evidence_id(value) for value in data["scope"])
    if len(set(scope)) != len(scope):
        raise BoundaryError("each evidence item is in scope once")
    if not isinstance(data["segments"], list) or not data["segments"]:
        raise BoundaryError("a candidate has at least one segment")
    segments = []
    for raw in data["segments"]:
        if not isinstance(raw, dict) or "kind" not in raw or not isinstance(raw["kind"], str):
            raise BoundaryError("a segment names its kind")
        try:
            kind = SegmentKind(raw["kind"])
        except ValueError as exc:
            raise BoundaryError(f"an undeclared segment kind: {raw['kind']!r}") from exc
        raw = _exact(f"a {kind.value} segment", raw, SEGMENT_KEYS[kind])
        if kind is SegmentKind.NO_ANSWER:
            segments.append(Segment(kind=kind))
            continue
        evidence = _evidence_id(raw["evidence"])
        field = index = None
        if kind in FIELDS:
            if raw["field"] not in FIELDS[kind]:
                raise BoundaryError(f"a {kind.value} segment names one of {list(FIELDS[kind])}; refused: "
                                    f"{raw['field']!r}")
            field = raw["field"]
        if kind is SegmentKind.CALCULATED_INPUT:
            index = raw["index"]
            if isinstance(index, bool) or not isinstance(index, int) or index < 0:
                raise BoundaryError("a calculated-input segment names an input by its index")
        segments.append(Segment(kind=kind, evidence=evidence, field=field, index=index))
    return Explanation(scope=scope, segments=tuple(segments))


def _published(item: EvidenceItem, registry: rule_registry.RuleRegistry) -> rule_registry.RegistryRule:
    try:
        return registry.lookup(item.rule.rule, item.rule.version, item.rule.variant)
    except rule_registry.RegistryError as exc:
        raise BoundaryError(f"{exc}: a rule is explained only as the pinned registry publishes it") from exc


def admit(explanation: Explanation, store: EvidenceStore, registry: rule_registry.RuleRegistry) -> dict:
    """Resolve every reference through trusted data, or refuse. Returns the scope's items, read through the store's
    checked reads. Nothing is taken from the candidate but its references."""

    if not isinstance(explanation, Explanation):
        raise BoundaryError("only a parsed explanation is admitted")
    items = {}
    for evidence_id in explanation.scope:
        try:
            items[evidence_id] = store.load(evidence_id)
        except StoreError as exc:
            raise BoundaryError(f"{evidence_id} fails the evidence read checks: {exc}") from exc
    for segment in explanation.segments:
        if segment.kind is SegmentKind.NO_ANSWER:
            continue
        if segment.evidence not in items:
            raise BoundaryError(f"{segment.evidence} is not in the explanation's scope")
        item = items[segment.evidence]
        if segment.kind in (SegmentKind.RULE_STATEMENT, SegmentKind.RULE_CITATION):
            _published(item, registry)
        if segment.kind is SegmentKind.CALCULATED_INPUT and segment.index >= len(item.lineage.inputs):
            raise BoundaryError(f"{segment.evidence} records no calculated input {segment.index}")
    return items


def _join(values) -> str:
    return ", ".join(str(value) for value in values) if values else "none recorded"


def render_segment(segment: Segment, item: EvidenceItem | None, registry: rule_registry.RuleRegistry) -> str:
    """One sentence, built only from the evidence item and the pinned registry."""

    if segment.kind is SegmentKind.NO_ANSWER:
        return ABSTENTION_TEXT
    reference = item.rule
    if segment.kind is SegmentKind.RULE_STATEMENT:
        published = _published(item, registry)
        return f"{reference.rule} v{reference.version} ({reference.variant}): {published.statement}"
    if segment.kind is SegmentKind.RULE_CITATION:
        published = _published(item, registry)
        return f"{reference.rule} v{reference.version} ({reference.variant}) is cited to {published.citation.source}, " \
               f"{published.citation.locator}."
    if segment.kind is SegmentKind.CHART_FACT:
        value = item.chart_context.__getattribute__(segment.field)
        shown = value if isinstance(value, str) else _join(value)
        return f"{segment.evidence} reads {segment.field} {shown} in chart {item.chart.chart_label}."
    if segment.kind is SegmentKind.CALCULATED_INPUT:
        calculated = item.lineage.inputs[segment.index]
        return f"{segment.evidence} uses {calculated.fact}, calculated under {calculated.provenance.profile_name}."
    if segment.kind is SegmentKind.TIMING:
        timing = item.timing
        return f"{segment.evidence} applies to the {timing.kind.value} period {timing.label}, {timing.start} to {timing.end}."
    if segment.kind is SegmentKind.POLARITY:
        return f"{segment.evidence} is recorded as {item.polarity.value}."
    if segment.field == "historical_performance":
        performance = item.historical_performance
        return f"{segment.evidence}: historical performance " + \
            ("is absent." if performance is None else f"is {performance.value} over {performance.sample_size} cases.")
    supplied = item.confidence.__getattribute__(segment.field)
    return f"{segment.evidence}: {segment.field} " + ("is absent." if supplied is None else f"is {supplied.value}.")


def render(candidate, store: EvidenceStore, registry: rule_registry.RuleRegistry) -> tuple:
    """Parse, admit and render a candidate. Every sentence returned comes from trusted data."""

    explanation = parse(candidate)
    items = admit(explanation, store, registry)
    return tuple(render_segment(segment, None if segment.evidence is None else items[segment.evidence], registry)
                 for segment in explanation.segments)


__all__ = ["ABSTENTION_TEXT", "EXPLANATION_SCHEMA", "BoundaryError", "Explanation", "Segment", "SegmentKind", "admit",
           "parse", "render", "render_segment"]
