"""The evidence item: the H4 specification's model (s3, s8, s10, s11), as ADR-0119 fixes it for WP-E4.

- Separation (H4 s2): an evidence item names the rule that produced it, the system it belongs to and
  the full provenance of every calculated input. It never carries a conclusion without its rule.
- Rule identity (ADR-0119 D1, AC3): a rule-version reference with its school, content hash,
  knowledge snapshot hash and source-declared strength. WP-E4 references are synthetic structural
  references only, never proof of registration or validation in the future rule registry, and they
  authorize no interpretation. No rule text, condition or application logic exists here.
- Systems (D3): the Charter's systems. Jaimini is added only with its approved specification, and
  CIL only once its framework is reproducibly specified, as the Charter conditions it.
- Uncertainty (AC7, AC8): the eight confidence components and historical performance are recorded as
  supplied, with provenance, or explicitly absent. Nothing here computes them. Cross-method and
  timing convergence belong to a later phase and are always absent.
- Lineage (AC12): an item records its calculated inputs and states whether that list, and its list
  of derivation links, is complete. Independence is never assumed from what is missing.

Nothing here scores, weights, fits, ranks or divides. Synthetic data only.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, fields
from enum import Enum

from engine.evidence.entity import DataClass, RecordProvenance
from engine.evidence.evidence_identifiers import EvidenceId, RuleId
from engine.evidence.identifiers import EntityId
from engine.models.provenance import Provenance

_HASH = re.compile(r"[0-9a-f]{64}")
_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


class EvidenceModelError(ValueError):
    """An evidence record that the model does not admit."""


class Domain(Enum):
    """The five domains (Charter, "Complete product contract" s2; H4 s8)."""

    JATAKA = "jataka"
    VARSHAPHAL = "varshaphal"
    MUHURTA = "muhurta"
    PRASHNA = "prashna"
    MUNDANE = "mundane"


class ProducingSystem(Enum):
    """The Charter's analytical systems (ADR-0119 D3; ADR-0106 OR-2). CIL is withheld until its framework is
    reproducibly specified, and Jaimini until its specification is approved."""

    PARASHARI = "parashari"
    PYTHAGOREAN_NUMEROLOGY = "pythagorean_numerology"
    BNN = "bnn"
    NAKSHATRA_NADI = "nakshatra_nadi"
    KP = "kp"


class Polarity(Enum):
    """All five are required (H4 s3): contradictory and insufficient evidence is kept, never misfiled."""

    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    CONTRADICTORY = "contradictory"
    INSUFFICIENT = "insufficient"


class TimingKind(Enum):
    DASHA = "dasha"
    TRANSIT = "transit"
    WINDOW = "window"


class DependencyClass(Enum):
    """How two items depend on each other (H4 s10, s11; ADR-0119 D4 A). Conflict is recorded separately."""

    INDEPENDENT = "independent"
    DERIVED = "derived"
    SHARED_ORIGIN = "shared_origin"
    CORRELATED = "correlated"
    UNKNOWN = "unknown"


#: CORRELATED is assigned only from measured evidence, and nothing in EVIDENCE measures it (ADR-0113 s2 A).
UNMEASURABLE_HERE = frozenset({DependencyClass.CORRELATED})
#: The eight decomposed components (H4 s3). The last two of the first five are later-phase values.
CONFIDENCE_COMPONENTS = ("calculation_confidence", "rule_confidence", "historical_fit", "cross_method_convergence",
                         "timing_convergence", "birth_data_consistency", "contradictory_evidence_present",
                         "data_completeness")
LATER_PHASE_COMPONENTS = frozenset({"cross_method_convergence", "timing_convergence"})


def _text(name: str, value) -> None:
    if not isinstance(value, str) or not value.strip():
        raise EvidenceModelError(f"{name} must be non-empty text")


def _synthetic(data_class) -> None:
    if data_class is not DataClass.SYNTHETIC:
        raise EvidenceModelError("only synthetic data is permitted (ADR-0113 s2 C3)")


def _member(name: str, value, enum) -> None:
    if not isinstance(value, enum):
        raise EvidenceModelError(f"{name} must be a {enum.__name__}")


@dataclass(frozen=True, slots=True)
class RuleSpec:
    """What is registered for one rule version. No rule text, condition or application logic is admitted."""

    school: ProducingSystem
    content_hash: str
    knowledge_snapshot_hash: str
    declared_strength: str
    provenance: RecordProvenance
    data_class: DataClass
    synthetic_reference: bool = True

    def __post_init__(self):
        _member("school", self.school, ProducingSystem)
        for name in ("content_hash", "knowledge_snapshot_hash"):
            value = self.__getattribute__(name)
            if not isinstance(value, str) or _HASH.fullmatch(value) is None:
                raise EvidenceModelError(f"{name} must be a 64-character lowercase SHA-256 hex digest")
        _text("declared_strength", self.declared_strength)
        if not isinstance(self.provenance, RecordProvenance):
            raise EvidenceModelError("a rule version records its provenance")
        _synthetic(self.data_class)
        if self.synthetic_reference is not True:
            raise EvidenceModelError("WP-E4 rule versions are synthetic structural references only; registering a real "
                                     "rule belongs to the rule registry (ADR-0119 D1, AC3)")


@dataclass(frozen=True, slots=True)
class RuleVersion:
    """A registered rule version: its RUL identifier, its version number and what was registered."""

    rule: RuleId
    version: int
    spec: RuleSpec

    def __post_init__(self):
        if not isinstance(self.rule, RuleId):
            raise EvidenceModelError("a rule version is named by its RUL identifier")
        if isinstance(self.version, bool) or not isinstance(self.version, int) or self.version < 1:
            raise EvidenceModelError("a rule version number is an integer from 1")
        if not isinstance(self.spec, RuleSpec):
            raise EvidenceModelError("a rule version carries its RuleSpec")


@dataclass(frozen=True, slots=True)
class RuleReference:
    """Which registered rule version an evidence item names."""

    rule: RuleId
    version: int

    def __post_init__(self):
        if not isinstance(self.rule, RuleId):
            raise EvidenceModelError("evidence names its rule by its RUL identifier")
        if isinstance(self.version, bool) or not isinstance(self.version, int) or self.version < 1:
            raise EvidenceModelError("evidence names a rule version number from 1")


@dataclass(frozen=True, slots=True)
class CalculatedInput:
    """One calculated fact an item consumed, with the full provenance it was computed under (H4 s3)."""

    fact: str
    provenance: Provenance

    def __post_init__(self):
        _text("fact", self.fact)
        if not isinstance(self.provenance, Provenance):
            raise EvidenceModelError("a calculated input carries its full Provenance; a profile name alone is not "
                                     "provenance (H4 s3)")


@dataclass(frozen=True, slots=True)
class Lineage:
    """What an item consumed, and whether its producer states the input and derivation lists are complete."""

    inputs: tuple
    inputs_complete: bool
    derivations_complete: bool

    def __post_init__(self):
        if not isinstance(self.inputs, tuple) or not self.inputs or \
                not all(isinstance(item, CalculatedInput) for item in self.inputs):
            raise EvidenceModelError("an evidence item records at least one calculated input")
        if len({item.fact for item in self.inputs}) != len(self.inputs):
            raise EvidenceModelError("each calculated input is recorded once")
        for name in ("inputs_complete", "derivations_complete"):
            if not isinstance(self.__getattribute__(name), bool):
                raise EvidenceModelError(f"{name} is stated, true or false")
        differing = provenance_differences(*(item.provenance for item in self.inputs))
        if differing:
            raise EvidenceModelError(f"one item's inputs differ in {', '.join(differing)}; facts computed under "
                                     f"different provenance are never silently joined (H4 s3)")


@dataclass(frozen=True, slots=True)
class ChartReference:
    """Which chart produced the evidence (H4 s8): a chart of the entity at a stated entity revision."""

    entity_revision: int
    chart_label: str

    def __post_init__(self):
        if isinstance(self.entity_revision, bool) or not isinstance(self.entity_revision, int) or \
                self.entity_revision < 1:
            raise EvidenceModelError("a chart reference names an entity revision from 1")
        _text("chart_label", self.chart_label)


@dataclass(frozen=True, slots=True)
class ChartContext:
    """Which chart or varga, and which planets, houses, signs and significators (H4 s3). Structured, not prose."""

    varga: str
    planets: tuple
    houses: tuple
    signs: tuple
    significators: tuple

    def __post_init__(self):
        _text("varga", self.varga)
        for name in ("planets", "significators"):
            value = self.__getattribute__(name)
            if not isinstance(value, tuple) or not all(isinstance(item, str) and item.strip() for item in value):
                raise EvidenceModelError(f"{name} is a tuple of names")
        for name in ("houses", "signs"):
            value = self.__getattribute__(name)
            if not isinstance(value, tuple) or not all(
                    not isinstance(item, bool) and isinstance(item, int) and 1 <= item <= 12 for item in value):
                raise EvidenceModelError(f"{name} is a tuple of numbers from 1 to 12")
        if not (self.planets or self.houses or self.signs or self.significators):
            raise EvidenceModelError("a chart context names at least one planet, house, sign or significator")


@dataclass(frozen=True, slots=True)
class TimingContext:
    """Which dasha period, transit or window (H4 s3). A field, never decoration."""

    kind: TimingKind
    label: str
    start: str
    end: str

    def __post_init__(self):
        _member("kind", self.kind, TimingKind)
        _text("label", self.label)
        for name in ("start", "end"):
            if not isinstance(self.__getattribute__(name), str) or _DATE.fullmatch(self.__getattribute__(name)) is None:
                raise EvidenceModelError(f"timing {name} is a YYYY-MM-DD date")
        if self.start > self.end:
            raise EvidenceModelError("a timing window cannot end before it starts")


@dataclass(frozen=True, slots=True)
class Supplied:
    """A value supplied to EVIDENCE, kept as given, with where it came from. EVIDENCE never computes one."""

    value: str
    provenance: RecordProvenance

    def __post_init__(self):
        _text("value", self.value)
        if not isinstance(self.provenance, RecordProvenance):
            raise EvidenceModelError("a supplied value records its provenance")


@dataclass(frozen=True, slots=True)
class Confidence:
    """The eight components, each Supplied or None (explicitly absent). There is no single confidence field."""

    calculation_confidence: Supplied | None
    rule_confidence: Supplied | None
    historical_fit: Supplied | None
    cross_method_convergence: Supplied | None
    timing_convergence: Supplied | None
    birth_data_consistency: Supplied | None
    contradictory_evidence_present: Supplied | None
    data_completeness: Supplied | None

    def __post_init__(self):
        for name in CONFIDENCE_COMPONENTS:
            value = self.__getattribute__(name)
            if value is not None and not isinstance(value, Supplied):
                raise EvidenceModelError(f"{name} is Supplied or explicitly absent")
            if value is not None and name in LATER_PHASE_COMPONENTS:
                raise EvidenceModelError(f"{name} is a later-phase value and is absent in EVIDENCE (H4 s11)")


@dataclass(frozen=True, slots=True)
class Performance:
    """Measured historical performance as supplied, with its sample size. Absent is None, never zero (H4 s3)."""

    value: str
    sample_size: int
    provenance: RecordProvenance

    def __post_init__(self):
        _text("value", self.value)
        if isinstance(self.sample_size, bool) or not isinstance(self.sample_size, int) or self.sample_size < 1:
            raise EvidenceModelError("supplied historical performance states its sample size, from 1")
        if not isinstance(self.provenance, RecordProvenance):
            raise EvidenceModelError("supplied historical performance records its provenance")


@dataclass(frozen=True, slots=True)
class EvidenceItem:
    """One evidence item. Its EVD identity and schema version are given by the store at persistence."""

    entity: EntityId
    domain: Domain
    question: None
    producing_system: ProducingSystem
    rule: RuleReference
    declared_strength: str
    measured_reliability: None
    lineage: Lineage
    chart: ChartReference
    chart_context: ChartContext
    timing: TimingContext
    polarity: Polarity
    confidence: Confidence
    historical_performance: Performance | None
    derived_from: tuple
    recomputes: EvidenceId | None
    provenance: RecordProvenance
    data_class: DataClass

    def __post_init__(self):
        if not isinstance(self.entity, EntityId):
            raise EvidenceModelError("evidence attaches to an ENT entity")
        _member("domain", self.domain, Domain)
        if self.question is not None:
            raise EvidenceModelError("question linkage is explicitly absent until a question model exists "
                                     "(ADR-0119 D2, AC5)")
        _member("producing_system", self.producing_system, ProducingSystem)
        if not isinstance(self.rule, RuleReference):
            raise EvidenceModelError("an evidence item whose rule cannot be named is not evidence (H4 s3)")
        _text("declared_strength", self.declared_strength)
        if self.measured_reliability is not None:
            raise EvidenceModelError("measured reliability is absent in WP-E4, and never derived from strength "
                                     "(ADR-0119 AC9)")
        for name, kind in (("lineage", Lineage), ("chart", ChartReference), ("chart_context", ChartContext),
                           ("timing", TimingContext), ("confidence", Confidence), ("provenance", RecordProvenance)):
            if not isinstance(self.__getattribute__(name), kind):
                raise EvidenceModelError(f"an evidence item requires its {name} ({kind.__name__})")
        _member("polarity", self.polarity, Polarity)
        if self.historical_performance is not None and not isinstance(self.historical_performance, Performance):
            raise EvidenceModelError("historical performance is Performance or explicitly absent")
        if not isinstance(self.derived_from, tuple) or not all(isinstance(item, EvidenceId)
                                                               for item in self.derived_from) or \
                len(set(self.derived_from)) != len(self.derived_from):
            raise EvidenceModelError("derivation links are a tuple of distinct EVD identifiers")
        if self.recomputes is not None and not isinstance(self.recomputes, EvidenceId):
            raise EvidenceModelError("a recomputation names the EVD identifier it recomputes")
        _synthetic(self.data_class)


@dataclass(frozen=True, slots=True)
class Relationship:
    """A recorded structural relationship between two items, with its basis. Conflict is a separate flag."""

    first: EvidenceId
    second: EvidenceId
    dependency: DependencyClass
    conflicting: bool
    basis: str

    def __post_init__(self):
        if not isinstance(self.first, EvidenceId) or not isinstance(self.second, EvidenceId) or \
                self.first == self.second:
            raise EvidenceModelError("a relationship joins two different evidence items")
        _member("dependency", self.dependency, DependencyClass)
        if self.dependency in UNMEASURABLE_HERE:
            raise EvidenceModelError("CORRELATED is assigned only from measured evidence, and nothing in EVIDENCE "
                                     "measures correlation (ADR-0113 s2 A; ADR-0119 AC12)")
        if not isinstance(self.conflicting, bool):
            raise EvidenceModelError("conflict is recorded, true or false")
        _text("basis", self.basis)


def provenance_differences(*provenances: Provenance) -> tuple:
    """Every field of the frozen Provenance on which the given provenances do not all agree (ADR-0119 AC11)."""

    if not provenances or not all(isinstance(item, Provenance) for item in provenances):
        raise EvidenceModelError("provenance comparison needs Provenance objects")
    return tuple(field.name for field in fields(Provenance)
                 if len({item.__getattribute__(field.name) for item in provenances}) > 1)
