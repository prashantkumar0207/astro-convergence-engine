"""Synthetic rule application (ADR-0133 I3, I4, I6, I7, I8, I9; PROPOSED).

`apply_rule()` applies every published variant of one rule version, from the evidence-pinned registry, to one
synthetic chart. Each variant gives exactly one record, fired or not fired, and none is chosen over another (H5 s2,
s7). When the variants state different polarities, the application says so and keeps them all.

A rule fires when its condition and every one of its activation conditions hold (H5 s2).

Refused, fail closed, each by one named check:
- a rule version the evidence-pinned registry does not publish. Every genuine rule is in that case: genuine rules are
  published separately, for citation only (ADR-0132 s4), and ADR-0133 D2 is not active;
- a genuine rule, however it arrives (`require_synthetic`; ADR-0132 s4);
- a rule of another school (`require_school`): this package applies Parashari rules only (ADR-0133 I8);
- a rule whose content does not match its content hash (`require_content`);
- a condition kind that conditions.evaluate() does not answer (ADR-0133 I2);
- a chart that is not declared synthetic (`SyntheticChart`; ADR-0133 I7), or whose origin is not nine graha longitudes,
  a Lagna longitude and a calculation provenance (`ChartOrigin`).

A chart carries no caller text. It is identified by the digest of its origin, and its certified facts are always
recomputed from that origin by PARASHARI_HOUSE_LORD_V1, never taken from the caller (CEO HOLD H1, H2 on PR #69).

A record carries no event class, timing, window, issuance, confidence or performance field (I6). It is held in memory
and never persisted, and it is not an evidence item (ADR-0133 D6). Its content hash covers every other field (I9).
verify() and verify_application() check a record, or a whole application, against the chart it came from before
anything renders it: the record must name that chart's origin digest, and its evaluations must equal the ones the
certified function gives for that chart now.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, fields

import engine.evidence.rule_registry as rule_registry
import engine.parashari.house_lord as house_lord
from engine.evidence.entity import DataClass
from engine.evidence.evidence_identifiers import RuleId
from engine.models.provenance import Provenance
from engine.interpretation.conditions import CERTIFIED_INPUT, ConditionError, Evaluation, evaluate

RECORD_SCHEMA = "ace-application-record-v1"
APPLIED_SCHOOL = "parashari"
#: Every field of a record, exactly. check_shape() and gate Y hold the dataclass to this list (ADR-0133 I6).
RECORD_FIELDS = ("schema", "rule", "version", "variant", "key", "school", "registry_snapshot_sha256",
                 "rule_content_hash", "evaluations", "fired", "declared_polarity", "claims", "chart_origin_sha256",
                 "chart_provenance", "certified_input", "input_content_sha256", "data_class", "record_sha256")
#: Field names a record must never carry: each would make it a prediction or a measure of one (ADR-0133 I6).
FORBIDDEN_FIELDS = ("event_class", "timing", "window", "start", "end", "issuance", "issued", "confidence",
                    "performance", "probability", "score", "weight", "prediction")


class ApplicationError(ValueError):
    """A rule, chart, record or application this package refuses."""


def _finite(value) -> bool:
    return type(value) is float and abs(value) < 1e6


@dataclass(frozen=True, slots=True)
class _Body:
    longitude: float


@dataclass(frozen=True, slots=True)
class _Houses:
    ascendant: float


@dataclass(frozen=True, slots=True)
class _Snapshot:
    provenance: Provenance
    houses: _Houses
    sidereal_planets: dict


@dataclass(frozen=True, slots=True)
class ChartOrigin:
    """What a synthetic chart's certified facts are computed from: the Lagna's sidereal longitude, each of the nine
    grahas' sidereal longitudes in PLACED_GRAHAS order, and the calculation provenance. Numbers only: no text."""

    ascendant: float
    longitudes: tuple
    provenance: Provenance

    def __post_init__(self):
        if not _finite(self.ascendant):
            raise ApplicationError("a chart origin's Lagna longitude is a finite float")
        if not isinstance(self.longitudes, tuple) or tuple(
                pair[0] if isinstance(pair, tuple) and len(pair) == 2 else None
                for pair in self.longitudes) != house_lord.PLACED_GRAHAS or not all(
                _finite(value) for _graha, value in self.longitudes):
            raise ApplicationError(f"a chart origin gives a finite float longitude for exactly {house_lord.PLACED_GRAHAS}")
        if type(self.provenance) is not Provenance:
            raise ApplicationError("a chart origin carries its calculation Provenance")

    @classmethod
    def from_snapshot(cls, snapshot) -> "ChartOrigin":
        """The origin of a certified kernel snapshot, or of a synthetic one shaped like it."""

        return cls(ascendant=float(snapshot.houses.ascendant),
                   longitudes=tuple((graha, float(snapshot.sidereal_planets[graha].longitude))
                                    for graha in house_lord.PLACED_GRAHAS),
                   provenance=snapshot.provenance)

    def digest(self) -> str:
        """The deterministic identity of this origin: exact longitudes, in hexadecimal, and every provenance field."""

        data = {"ascendant": self.ascendant.hex(),
                "longitudes": [[graha, value.hex()] for graha, value in self.longitudes],
                "provenance": [[field.name, self.provenance.__getattribute__(field.name)]
                               for field in fields(Provenance)]}
        return hashlib.sha256(json.dumps(data, sort_keys=True, separators=(",", ":"),
                                         ensure_ascii=True).encode("ascii")).hexdigest()

    def chart(self) -> house_lord.HouseLordChart:
        """The certified facts, recomputed from this origin by PARASHARI_HOUSE_LORD_V1."""

        return house_lord.house_lords_from_snapshot(_Snapshot(
            provenance=self.provenance, houses=_Houses(ascendant=self.ascendant),
            sidereal_planets={graha: _Body(longitude=value) for graha, value in self.longitudes}))


@dataclass(frozen=True, slots=True)
class SyntheticChart:
    """A chart origin, declared synthetic by its caller. It has no label and no other text (CEO HOLD H1)."""

    origin: ChartOrigin
    data_class: DataClass

    def __post_init__(self):
        if self.data_class is not DataClass.SYNTHETIC:
            raise ApplicationError("only a chart declared synthetic is applied (ADR-0113 s2 C3; ADR-0133 I7)")
        if type(self.origin) is not ChartOrigin:
            raise ApplicationError(f"a synthetic chart is a ChartOrigin, from which {CERTIFIED_INPUT} computes its facts")

    def chart(self) -> house_lord.HouseLordChart:
        return self.origin.chart()


@dataclass(frozen=True, slots=True)
class ApplicationRecord:
    """One variant of one rule version applied to one synthetic chart."""

    schema: str
    rule: str
    version: int
    variant: str
    key: str
    school: str
    registry_snapshot_sha256: str
    rule_content_hash: str
    evaluations: tuple
    fired: bool
    declared_polarity: str
    claims: tuple
    chart_origin_sha256: str
    chart_provenance: tuple
    certified_input: str
    input_content_sha256: str
    data_class: str
    record_sha256: str


@dataclass(frozen=True, slots=True)
class Application:
    """Every variant of one rule version, applied to one chart. `variants_disagree` is true when their polarities
    differ; every variant is kept either way."""

    rule: str
    version: int
    records: tuple
    variants_disagree: bool


def _evaluation_record(item: Evaluation) -> dict:
    return {"kind": item.kind, "parameters": [[name, list(value) if isinstance(value, tuple) else value]
                                              for name, value in item.parameters],
            "facts": [[name, value] for name, value in item.facts], "holds": item.holds}


def canonical(record: ApplicationRecord) -> bytes:
    """Every field except the record's own hash, in canonical form."""

    data = {name: record.__getattribute__(name) for name in RECORD_FIELDS if name != "record_sha256"}
    data["evaluations"] = [_evaluation_record(item) for item in record.evaluations]
    data["claims"] = [[name, value] for name, value in record.claims]
    data["chart_provenance"] = [[name, value] for name, value in record.chart_provenance]
    return (json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("ascii")


def record_hash(record: ApplicationRecord) -> str:
    return hashlib.sha256(canonical(record)).hexdigest()


def claims_of(item: rule_registry.RegistryRule) -> tuple:
    """The four H5 s4 claims of a published rule, as the record carries them."""

    level = item.certification
    return (("transcription_fidelity", level.transcription_fidelity.value),
            ("source_attribution", level.source_attribution.value),
            ("applicability_conditions", level.applicability_conditions.value),
            ("measured_performance", None))


# --------------------------------------------------------------- admission

def require_synthetic(item: rule_registry.RegistryRule) -> None:
    if item.synthetic is not True:
        raise ApplicationError(f"{item.rule} version {item.version} variant {item.variant!r} is a genuine rule: published "
                               f"for citation only and never applied (ADR-0132 s4); ADR-0133 D2 is not active")


def require_school(item: rule_registry.RegistryRule) -> None:
    if item.school.value != APPLIED_SCHOOL:
        raise ApplicationError(f"{item.rule} belongs to the {item.school.value} school; WP-I1 applies Parashari rules "
                               f"only (ADR-0133 I8)")


def require_content(item: rule_registry.RegistryRule) -> None:
    if item.content_hash != rule_registry.content_hash(item):
        raise ApplicationError(f"{item.rule} version {item.version} variant {item.variant!r}: the content does not match "
                               f"its content hash")


def admit(item: rule_registry.RegistryRule) -> None:
    """Every check a published rule must pass before it is applied."""

    if type(item) is not rule_registry.RegistryRule:
        raise ApplicationError("only a published registry rule is applied")
    require_synthetic(item)
    require_school(item)
    require_content(item)


def _evaluate_all(item: rule_registry.RegistryRule, chart: SyntheticChart) -> tuple:
    try:
        facts = chart.chart()
        return tuple(evaluate(condition, facts) for condition in (item.condition, *item.activation_conditions))
    except (ConditionError, house_lord.HouseLordProfileError) as exc:
        raise ApplicationError(f"{item.rule} version {item.version} variant {item.variant!r}: {exc}") from exc


def _record(item: rule_registry.RegistryRule, registry: rule_registry.RuleRegistry,
            chart: SyntheticChart) -> ApplicationRecord:
    evaluations = _evaluate_all(item, chart)
    provenance = chart.origin.provenance
    draft = ApplicationRecord(
        schema=RECORD_SCHEMA, rule=item.rule.value, version=item.version, variant=item.variant, key=item.key,
        school=item.school.value, registry_snapshot_sha256=registry.snapshot_sha256,
        rule_content_hash=item.content_hash, evaluations=evaluations,
        fired=all(evaluation.holds for evaluation in evaluations), declared_polarity=item.polarity.value,
        claims=claims_of(item), chart_origin_sha256=chart.origin.digest(),
        chart_provenance=tuple((field.name, provenance.__getattribute__(field.name)) for field in fields(provenance)),
        certified_input=CERTIFIED_INPUT, input_content_sha256=house_lord.rule_content_sha256(),
        data_class=DataClass.SYNTHETIC.value, record_sha256="")
    return ApplicationRecord(**{name: draft.__getattribute__(name) for name in RECORD_FIELDS if name != "record_sha256"},
                             record_sha256=record_hash(draft))


def apply_published(chart: SyntheticChart, registry: rule_registry.RuleRegistry, rule: RuleId,
                    version: int) -> Application:
    """Apply every published variant of one rule version from the given registry. apply_rule() is the entry point:
    it passes only the evidence-pinned registry."""

    if type(chart) is not SyntheticChart:
        raise ApplicationError("rules are applied only to a SyntheticChart (ADR-0133 I7)")
    if not isinstance(rule, RuleId):
        raise ApplicationError("a rule is named by its RUL identifier")
    try:
        items = tuple(registry.lookup(rule, version, variant) for variant in registry.variants(rule, version))
    except rule_registry.RegistryError as exc:
        raise ApplicationError(f"{rule} version {version} is not published by the evidence-pinned registry; genuine "
                               f"rules are citation-only (ADR-0132 s4) and ADR-0133 D2 is not active: {exc}") from exc
    for item in items:
        admit(item)
    records = tuple(_record(item, registry, chart) for item in items)
    return Application(rule=rule.value, version=version, records=records,
                       variants_disagree=len({record.declared_polarity for record in records}) > 1)


def apply_rule(chart: SyntheticChart, rule: RuleId, version: int) -> Application:
    """Apply every published variant of one rule version from the evidence-pinned registry to one synthetic chart."""

    return apply_published(chart, rule_registry.pinned(), rule, version)


# --------------------------------------------------------------- verification

def check_shape(record: ApplicationRecord) -> None:
    if type(record) is not ApplicationRecord or tuple(field.name for field in fields(ApplicationRecord)) != RECORD_FIELDS:
        raise ApplicationError("only an ApplicationRecord, with exactly its schema's fields, is accepted")


def check_hash(record: ApplicationRecord) -> None:
    if record.record_sha256 != record_hash(record):
        raise ApplicationError("the record does not match its content hash")


def check_identity(record: ApplicationRecord) -> None:
    if (record.schema, record.data_class, record.certified_input) != (RECORD_SCHEMA, DataClass.SYNTHETIC.value,
                                                                       CERTIFIED_INPUT):
        raise ApplicationError("the record's schema, data class or certified input is not this package's")
    if record.input_content_sha256 != house_lord.rule_content_sha256():
        raise ApplicationError(f"the record was produced from another {CERTIFIED_INPUT} content")


def check_published(record: ApplicationRecord) -> rule_registry.RegistryRule:
    registry = rule_registry.pinned()
    try:
        item = registry.lookup(RuleId(record.rule), record.version, record.variant)
    except (rule_registry.RegistryError, ValueError) as exc:
        raise ApplicationError(f"the record names a rule the evidence-pinned registry does not publish: {exc}") from exc
    admit(item)
    if (record.registry_snapshot_sha256, record.rule_content_hash, record.key, record.school,
            record.declared_polarity, record.claims) != (registry.snapshot_sha256, item.content_hash, item.key,
                                                          item.school.value, item.polarity.value, claims_of(item)):
        raise ApplicationError("the record does not match the published rule")
    return item


def check_origin(record: ApplicationRecord, chart: SyntheticChart) -> None:
    """The record came from this chart: it names this chart's origin digest and provenance (CEO HOLD H2)."""

    if type(chart) is not SyntheticChart:
        raise ApplicationError("a record is verified only against the SyntheticChart it came from")
    provenance = tuple((field.name, chart.origin.provenance.__getattribute__(field.name))
                       for field in fields(chart.origin.provenance))
    if (record.chart_origin_sha256, record.chart_provenance) != (chart.origin.digest(), provenance):
        raise ApplicationError("the record was not produced from this chart")


def check_evaluations(record: ApplicationRecord, item: rule_registry.RegistryRule, chart: SyntheticChart) -> None:
    """Every evaluation equals the one PARASHARI_HOUSE_LORD_V1 gives for this chart now, recomputed from its origin, so
    a record's facts can never be supplied by the record itself (CEO HOLD H2)."""

    if not isinstance(record.evaluations, tuple) or not all(type(item) is Evaluation for item in record.evaluations):
        raise ApplicationError("the record's evaluations are not Evaluations")
    if record.evaluations != _evaluate_all(item, chart):
        raise ApplicationError("the record's evaluations are not the chart's certified facts and answers")
    if record.fired is not all(evaluation.holds for evaluation in record.evaluations):
        raise ApplicationError("the record's outcome does not follow from its evaluations")


def verify(record: ApplicationRecord, chart: SyntheticChart) -> rule_registry.RegistryRule:
    """Check a record against itself, the pinned registry, the certified input and the chart it came from, and return
    the published rule it names. Anything that does not check is refused."""

    check_shape(record)
    check_hash(record)
    check_identity(record)
    item = check_published(record)
    check_origin(record, chart)
    check_evaluations(record, item, chart)
    return item


def check_coverage(application: Application) -> None:
    """Every published variant of the rule version is present, once, in the registry's order (ADR-0133 I3)."""

    variants = rule_registry.pinned().variants(RuleId(application.rule), application.version)
    if tuple(record.variant for record in application.records) != variants:
        raise ApplicationError(f"an application carries every published variant of its rule version, in order: "
                               f"{variants}")


def verify_application(application: Application, chart: SyntheticChart) -> tuple:
    """Check a whole application against the chart it came from: its type, every record, one rule version, full
    variant coverage and the disagreement flag. Returns the published rules, one per record."""

    if type(application) is not Application or not isinstance(application.records, tuple) or not application.records:
        raise ApplicationError("only an Application with at least one record is accepted")
    items = tuple(verify(record, chart) for record in application.records)
    if any((record.rule, record.version) != (application.rule, application.version) for record in application.records):
        raise ApplicationError("an application's records are all of its one rule version")
    check_coverage(application)
    if application.variants_disagree is not (len({record.declared_polarity for record in application.records}) > 1):
        raise ApplicationError("the application's disagreement flag does not follow from its records")
    return items
