"""Deterministic explanation of an application record (ADR-0133 I5; Q8 s7; H5 s3; PROPOSED).

render() takes a record and the chart it came from, and nothing else. There is no text input of any kind: the chart
is numbers only and is identified by its origin digest, so no caller or generated text can add a rule, generalise one,
change a calculated value or make a claim (CEO HOLD H1). The record is verified first (application.verify): its content
hash, the published rule it names, the chart's origin, and every evaluation recomputed from that chart (CEO HOLD H2).
Every sentence is then built from the verified record, the chart's certified facts and the evidence-pinned registry,
from fixed templates.

The fixed closing sentence states what the record is not: a prediction, a timing, a confidence or a measured
performance. There is no LLM client and no network access here.
"""

from __future__ import annotations

from engine.interpretation.application import Application, ApplicationRecord, SyntheticChart, verify, verify_application

#: The one sentence every explanation ends with.
NON_CLAIM_TEXT = ("This is not a prediction: no event, timing, window or confidence is stated, no performance has been "
                  "measured, and the chart is synthetic.")
CLAIM_LABELS = {"transcription_fidelity": "transcription fidelity", "source_attribution": "source attribution",
                "applicability_conditions": "applicability", "measured_performance": "measured performance"}


def _pairs(pairs: tuple) -> str:
    return ", ".join(f"{name} {list(value) if isinstance(value, tuple) else value}" for name, value in pairs)


def _claim(value) -> str:
    return "none" if value is None else value.replace("_", " ")


def render(record: ApplicationRecord, chart: SyntheticChart) -> tuple:
    """The explanation of one record, verified against the chart it came from, sentence by sentence."""

    item = verify(record, chart)
    lines = [f"{record.rule} version {record.version}, variant {record.variant} ({record.key}), {record.school} school, "
             f"applied to the synthetic chart with origin digest {record.chart_origin_sha256}.",
             f"Statement, from the evidence-pinned registry: {item.statement}",
             f"Citation: {item.citation.source}, {item.citation.locator}."]
    for index, evaluation in enumerate(record.evaluations):
        role = "Condition" if index == 0 else "Activation condition"
        lines.append(f"{role} {evaluation.kind} ({_pairs(evaluation.parameters)}): from {record.certified_input}, "
                     f"{_pairs(evaluation.facts)}; it {'holds' if evaluation.holds else 'does not hold'}.")
    lines.append(f"Outcome: the rule {'fired' if record.fired else 'did not fire'}; its declared polarity is "
                 f"{record.declared_polarity}.")
    lines.append("Claims: " + "; ".join(f"{CLAIM_LABELS[name]} {_claim(value)}" for name, value in record.claims) + ".")
    lines.append(NON_CLAIM_TEXT)
    return tuple(lines)


def render_application(application: Application, chart: SyntheticChart) -> tuple:
    """Every variant's explanation, in the registry's order, and a statement of disagreement where there is one."""

    verify_application(application, chart)
    lines = []
    for record in application.records:
        lines.extend(render(record, chart))
    if application.variants_disagree:
        variants = ", ".join(f"{record.variant} ({record.declared_polarity})" for record in application.records)
        lines.append(f"The variants disagree in polarity: {variants}. All are kept, and none is preferred.")
    return tuple(lines)
