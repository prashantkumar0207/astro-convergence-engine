"""The entity model (docs/H0_ENTITY_MODEL_SPEC.md, ACCEPTED by ADR-0113).

- ADR-0020 D1: a common AstrologicalSubject, with specialised subject types.
- ADR-0021 D3: five provisional kinds; a new kind needs an ADR.
- ADR-0020 D3: competing charts are held in full, with provenance per chart; nothing selects one.
- ADR-0021 D4: relationships are explicit links between entities, not entities.

An entity carries no interpretation, evidence, score, weight or confidence (H0 s5). Records are
frozen; the store appends and never overwrites. Only synthetic data is permitted (ADR-0113 s2 C3).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field, fields
from enum import Enum

from engine.evidence.identifiers import EntityId


class EntityKind(Enum):
    """ADR-0021 D3. Provisional, and extended only by an ADR."""

    PERSON = "person"
    ORGANISATION = "organisation"
    GEOGRAPHIC = "geographic"
    EVENT = "event"
    QUESTION = "question"


class Shape(Enum):
    """H0 s3. Shape D (general Muhurta, no entity) is deliberately absent: it is not an entity."""

    ORIGIN = "A"
    DERIVED = "B"
    QUERY = "C"


class OriginCertainty(Enum):
    """H0 s4. Documented origins are never rectified."""

    DOCUMENTED = "documented"
    REPORTED = "reported"
    UNCERTAIN = "uncertain"


class DataClass(Enum):
    """ADR-0113 s2 C3: V1 permits synthetic data only, so there is only one member."""

    SYNTHETIC = "synthetic"


class EntityModelError(ValueError):
    """A subject, chart or link that violates the H0 model."""


@dataclass(frozen=True, slots=True)
class RecordProvenance:
    """Where a record came from (H0 s4): its source, how it was obtained, and the schema it uses."""

    source: str
    method: str
    schema_version: str

    def __post_init__(self):
        for name, value in (("source", self.source), ("method", self.method),
                            ("schema_version", self.schema_version)):
            if not isinstance(value, str) or not value.strip():
                raise EntityModelError(f"provenance.{name} is required")


@dataclass(frozen=True, slots=True)
class OriginMoment:
    """A moment and place, with the timezone's source and a stated precision (H0 s4)."""

    local_datetime: str
    timezone: str
    timezone_source: str
    latitude: float
    longitude: float
    precision: str

    def __post_init__(self):
        if not -90.0 <= self.latitude <= 90.0 or not -180.0 <= self.longitude <= 180.0:
            raise EntityModelError("origin place is out of range")
        for name, value in (("local_datetime", self.local_datetime), ("timezone", self.timezone),
                            ("timezone_source", self.timezone_source), ("precision", self.precision)):
            if not isinstance(value, str) or not value.strip():
                raise EntityModelError(f"origin.{name} is required")


@dataclass(frozen=True, slots=True)
class ChartCandidate:
    """One defensible chart of an entity, with its own source and provenance (ADR-0020 D3)."""

    label: str
    origin: OriginMoment
    origin_certainty: OriginCertainty
    provenance: RecordProvenance


@dataclass(frozen=True, slots=True)
class ParentLink:
    """Shape B: which entity and chart this derives from, and by what derivation (H0 s4)."""

    parent: EntityId
    parent_chart: str
    derivation: str


@dataclass(frozen=True)
class AstrologicalSubject:
    """The common subject abstraction (ADR-0020 D1). Construct a specialised type, not this."""

    kind: EntityKind
    shape: Shape
    charts: tuple
    applicable_domains: tuple
    applicable_systems: tuple
    provenance: RecordProvenance
    data_class: DataClass
    parent: ParentLink | None = None

    #: The shapes each specialised type may take. Set by every subclass.
    ALLOWED_SHAPES = ()
    KIND = None

    def __post_init__(self):
        if type(self) is AstrologicalSubject:
            raise EntityModelError("construct a specialised subject type (ADR-0020 D1)")
        if self.kind is not self.KIND:
            raise EntityModelError(f"{type(self).__name__} must have kind {self.KIND}")
        if self.shape not in self.ALLOWED_SHAPES:
            raise EntityModelError(f"{type(self).__name__} cannot take shape {self.shape.value}")
        if self.data_class is not DataClass.SYNTHETIC:
            raise EntityModelError("V1 permits synthetic data only (ADR-0113 s2 C3)")
        if not isinstance(self.charts, tuple) or not all(isinstance(c, ChartCandidate) for c in self.charts):
            raise EntityModelError("charts must be a tuple of ChartCandidate")
        labels = [chart.label for chart in self.charts]
        if len(set(labels)) != len(labels):
            raise EntityModelError("chart labels must be unique within a subject")
        if self.shape is Shape.DERIVED:
            if self.parent is None:
                raise EntityModelError("a derived subject needs its parent link (H0 s4)")
        elif self.parent is not None:
            raise EntityModelError("only a derived subject has a parent link")
        if self.shape in (Shape.ORIGIN, Shape.DERIVED) and not self.charts:
            raise EntityModelError(f"a shape {self.shape.value} subject needs at least one chart (H0 s4)")
        if self.shape is Shape.QUERY and len(self.charts) != 1:
            raise EntityModelError("a query moment has exactly one chart: the moment of asking")
        for name, value in (("applicable_domains", self.applicable_domains),
                            ("applicable_systems", self.applicable_systems)):
            if not isinstance(value, tuple) or not value or not all(isinstance(v, str) and v for v in value):
                raise EntityModelError(f"{name} must be declared, never inferred (H0 s5)")

    def chart(self, label: str) -> ChartCandidate:
        for candidate in self.charts:
            if candidate.label == label:
                return candidate
        raise KeyError(label)


@dataclass(frozen=True)
class Person(AstrologicalSubject):
    """A person (ADR-0020 D1)."""

    KIND = EntityKind.PERSON
    ALLOWED_SHAPES = (Shape.ORIGIN, Shape.DERIVED)


@dataclass(frozen=True)
class Organisation(AstrologicalSubject):
    """An organisation or company (ADR-0020 D1)."""

    KIND = EntityKind.ORGANISATION
    ALLOWED_SHAPES = (Shape.ORIGIN, Shape.DERIVED)


@dataclass(frozen=True)
class GeographicEntity(AstrologicalSubject):
    """A geographic or national entity (ADR-0020 D1)."""

    KIND = EntityKind.GEOGRAPHIC
    ALLOWED_SHAPES = (Shape.ORIGIN, Shape.DERIVED)


@dataclass(frozen=True)
class EventEntity(AstrologicalSubject):
    """An event as a subject of analysis, such as an election (ADR-0020 D1)."""

    KIND = EntityKind.EVENT
    ALLOWED_SHAPES = (Shape.ORIGIN, Shape.DERIVED)


@dataclass(frozen=True)
class Question(AstrologicalSubject):
    """A Prashna question: a query moment, which cannot be rectified (ADR-0020 D1, H0 s3)."""

    KIND = EntityKind.QUESTION
    ALLOWED_SHAPES = (Shape.QUERY,)


SUBJECT_TYPES = {cls.KIND: cls for cls in (Person, Organisation, GeographicEntity, EventEntity, Question)}

#: Every field a subject may carry. The store refuses any other key, so analytical content cannot be stored.
SUBJECT_FIELDS = tuple(f.name for f in fields(AstrologicalSubject))


def rectification_permitted(subject: AstrologicalSubject, chart_label: str) -> bool:
    """H0 s3 and s4: a query moment cannot be rectified, and a documented origin is never rectified."""

    if subject.shape is Shape.QUERY:
        return False
    return subject.chart(chart_label).origin_certainty is not OriginCertainty.DOCUMENTED


_RELATION = re.compile(r"[A-Z][A-Z0-9_]*")


@dataclass(frozen=True, slots=True)
class EntityLink:
    """A relationship as an explicit link between two entities (ADR-0021 D4)."""

    source: EntityId
    relation: str
    target: EntityId
    provenance: RecordProvenance = field(compare=True)

    def __post_init__(self):
        if _RELATION.fullmatch(self.relation) is None:
            raise EntityModelError(f"relation must be an UPPER_SNAKE name: {self.relation!r}")
        if self.source == self.target:
            raise EntityModelError("a link joins two different entities")
