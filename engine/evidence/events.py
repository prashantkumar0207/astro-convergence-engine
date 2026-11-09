"""The structured event model: the H1 specification v2.0.0, ACCEPTED by ADR-0113, and ADR-0115.

- H1 s3: an event is asserted, never silently inferred; its time is uncertain by default; it is
  immutable once recorded; its class comes from a controlled vocabulary.
- ADR-0113 s2 C2: an event attaches to an ENT entity. A chart reference is optional, explicit and
  provenance-bearing, and records only the context in which the event was asserted. The charts an
  analysis evaluates belong to the analysis, so no such field exists here.
- H1 s5: no interpretation, rule, score or astrological content.
- Confirmation is a separate record (engine/evidence/event_store.py). Nothing here can mark an
  event confirmed, so assertion and confirmation stay apart.

Only synthetic data is permitted (ADR-0113 s2 C3).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, fields
from datetime import datetime
from enum import Enum

from engine.evidence.entity import DataClass, RecordProvenance
from engine.evidence.event_classes import CLASS_DOMAIN, CLASS_PATTERN, registered
from engine.evidence.identifiers import EntityId


class EventModelError(ValueError):
    """An event, time, assertion or confirmation that violates the H1 model."""


class TimeKind(Enum):
    """H1 s3: the four representations an event's time may take."""

    INSTANT = "instant"
    CLOSED_INTERVAL = "closed_interval"
    OPEN_INTERVAL = "open_interval"
    FUZZY_WINDOW = "fuzzy_window"


class TimeUnit(Enum):
    """A precision, and the unit of a stated tolerance. Coarsest first."""

    YEAR = "year"
    MONTH = "month"
    DAY = "day"
    HOUR = "hour"
    MINUTE = "minute"


class WindowShape(Enum):
    """The shape the asserter states for a fuzzy window. Declared, never computed."""

    UNSTATED = "unstated"
    UNIFORM = "uniform"
    TRIANGULAR = "triangular"
    NORMAL = "normal"


class AsserterKind(Enum):
    """H1 s3 and s9: who asserted the event. Public record is distinct from recollection."""

    USER_RECOLLECTION = "user_recollection"
    DOCUMENT = "document"
    PUBLIC_RECORD = "public_record"
    SYSTEM_HYPOTHESIS = "system_hypothesis"


class AsserterCertainty(Enum):
    """The certainty the asserter declares in their own memory (H1 s4). Recorded, never computed."""

    UNSTATED = "unstated"
    UNSURE = "unsure"
    PROBABLE = "probable"
    CERTAIN = "certain"


class ConfirmationState(Enum):
    """H1 s4. An event with no confirmation record is UNCONFIRMED."""

    UNCONFIRMED = "unconfirmed"
    CONFIRMED = "confirmed"
    PARTIALLY_CONFIRMED = "partially_confirmed"
    REJECTED = "rejected"


class ConfirmerKind(Enum):
    """Only a human confirms (H1 s5). There is deliberately no system member."""

    SUBJECT = "subject"
    HUMAN_REVIEWER = "human_reviewer"


_FORMATS = {
    TimeUnit.YEAR: (re.compile(r"\d{4}"), "%Y"),
    TimeUnit.MONTH: (re.compile(r"\d{4}-\d{2}"), "%Y-%m"),
    TimeUnit.DAY: (re.compile(r"\d{4}-\d{2}-\d{2}"), "%Y-%m-%d"),
    TimeUnit.HOUR: (re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}"), "%Y-%m-%dT%H"),
    TimeUnit.MINUTE: (re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}"), "%Y-%m-%dT%H:%M"),
}
_HOUR_KNOWN = (TimeUnit.HOUR, TimeUnit.MINUTE)
_ASSERTED_AT = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
_TOKEN = re.compile(r"[a-z][a-z0-9_]*")


def _text(name: str, value) -> None:
    if not isinstance(value, str) or not value.strip():
        raise EventModelError(f"{name} is required")


def _moment(value: str, precision: TimeUnit) -> datetime:
    """Parse a time value written at exactly `precision`, refusing any other form."""

    pattern, form = _FORMATS[precision]
    if not isinstance(value, str) or pattern.fullmatch(value) is None:
        raise EventModelError(f"{value!r} is not written at {precision.value} precision")
    try:
        return datetime.strptime(value, form)
    except ValueError as exc:
        raise EventModelError(f"{value!r} is not a calendar {precision.value}") from exc


def _timestamp(name: str, value) -> None:
    if not isinstance(value, str) or _ASSERTED_AT.fullmatch(value) is None:
        raise EventModelError(f"{name} must be a UTC timestamp YYYY-MM-DDTHH:MM:SSZ")
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise EventModelError(f"{name} is not a calendar timestamp") from exc


@dataclass(frozen=True, slots=True)
class TimeTolerance:
    """A stated tolerance: plus or minus `amount` of `unit`."""

    amount: int
    unit: TimeUnit

    def __post_init__(self):
        if isinstance(self.amount, bool) or not isinstance(self.amount, int) or self.amount < 1:
            raise EventModelError("a tolerance is a whole number of units, at least 1")
        if not isinstance(self.unit, TimeUnit):
            raise EventModelError("a tolerance needs a TimeUnit")


@dataclass(frozen=True, slots=True)
class EventTime:
    """When an event happened, with its uncertainty stated, never hidden (H1 s3, s4).

    Every value is written at exactly `precision`: a year as 2010, a month as 2010-05, and so on,
    so a value never claims more precision than the asserter has.
    """

    kind: TimeKind
    precision: TimeUnit | None
    timezone: str | None
    timezone_source: str | None
    at: str | None = None
    start: str | None = None
    end: str | None = None
    tolerance: TimeTolerance | None = None
    window_shape: WindowShape = WindowShape.UNSTATED
    birth_time_sensitive: bool = False

    def __post_init__(self):
        if not isinstance(self.kind, TimeKind) or not isinstance(self.window_shape, WindowShape):
            raise EventModelError("time kind and window shape must be their enums")
        present = {"at": self.at is not None, "start": self.start is not None, "end": self.end is not None,
                   "tolerance": self.tolerance is not None}
        required, allowed = {
            TimeKind.INSTANT: ({"at"}, {"at"}),
            TimeKind.CLOSED_INTERVAL: ({"start", "end"}, {"start", "end"}),
            TimeKind.OPEN_INTERVAL: (set(), {"start", "end"}),
            TimeKind.FUZZY_WINDOW: ({"at", "tolerance"}, {"at", "tolerance"}),
        }[self.kind]
        given = {name for name, is_set in present.items() if is_set}
        if not required <= given or not given <= allowed:
            raise EventModelError(f"a {self.kind.value} takes {sorted(allowed)} and needs {sorted(required)}; "
                                  f"given {sorted(given)}")
        if self.kind is TimeKind.OPEN_INTERVAL and present["start"] and present["end"]:
            raise EventModelError("an open interval leaves at least one end open; use a closed interval")
        values = [value for value in (self.at, self.start, self.end) if value is not None]
        if values:
            if not isinstance(self.precision, TimeUnit):
                raise EventModelError("a time with a value states its precision")
            _text("timezone", self.timezone)
            _text("timezone_source", self.timezone_source)
            moments = {value: _moment(value, self.precision) for value in values}
        else:
            if self.precision is not None or self.timezone is not None or self.timezone_source is not None:
                raise EventModelError("an unbounded time has no precision or timezone to state")
            moments = {}
        if self.kind is TimeKind.CLOSED_INTERVAL and moments[self.start] > moments[self.end]:
            raise EventModelError("a closed interval cannot end before it starts")
        if self.tolerance is not None and not isinstance(self.tolerance, TimeTolerance):
            raise EventModelError("a tolerance must be a TimeTolerance")
        if self.window_shape is not WindowShape.UNSTATED and self.kind is not TimeKind.FUZZY_WINDOW:
            raise EventModelError("only a fuzzy window has a shape")
        if not isinstance(self.birth_time_sensitive, bool):
            raise EventModelError("birth_time_sensitive is a flag")
        if self.birth_time_sensitive:
            if self.kind is TimeKind.OPEN_INTERVAL or self.precision not in _HOUR_KNOWN:
                raise EventModelError("an event is birth-time sensitive only when its hour is known")
            if self.tolerance is not None and self.tolerance.unit not in _HOUR_KNOWN:
                raise EventModelError("a birth-time-sensitive window states its tolerance in hours or minutes")


@dataclass(frozen=True, slots=True)
class Assertion:
    """Who asserted the event, when, how, and how sure they say they are (H1 s3, s4, s9)."""

    asserter_kind: AsserterKind
    asserter_reference: str
    asserted_at: str
    method: str
    asserter_certainty: AsserterCertainty

    def __post_init__(self):
        if not isinstance(self.asserter_kind, AsserterKind) or not isinstance(self.asserter_certainty,
                                                                              AsserterCertainty):
            raise EventModelError("asserter kind and certainty must be their enums")
        _text("asserter_reference", self.asserter_reference)
        _text("method", self.method)
        _timestamp("asserted_at", self.asserted_at)
        if self.asserter_kind is AsserterKind.SYSTEM_HYPOTHESIS and \
                self.asserter_certainty is not AsserterCertainty.UNSTATED:
            raise EventModelError("a system hypothesis declares no certainty; only a human holds a memory")


@dataclass(frozen=True, slots=True)
class AssertionContext:
    """The chart under which the event was asserted: optional, explicit, provenance-bearing (ADR-0113 s2 C2).

    It names a revision of the event's own entity, so the reference can never be silently moved by a
    later correction of that entity.
    """

    entity_revision: int
    chart_label: str
    provenance: RecordProvenance

    def __post_init__(self):
        if isinstance(self.entity_revision, bool) or not isinstance(self.entity_revision, int) or \
                self.entity_revision < 1:
            raise EventModelError("an assertion context names an entity revision, from 1")
        _text("chart_label", self.chart_label)
        if not isinstance(self.provenance, RecordProvenance):
            raise EventModelError("an assertion context carries its own provenance")


@dataclass(frozen=True, slots=True)
class EventRecord:
    """One asserted event about one ENT entity. Its EVR identifier comes from the store."""

    entity: EntityId
    event_class: str
    time: EventTime
    assertion: Assertion
    provenance: RecordProvenance
    data_class: DataClass
    subclass: str | None = None
    domain: str | None = None
    assertion_context: AssertionContext | None = None

    def __post_init__(self):
        if not isinstance(self.entity, EntityId):
            raise EventModelError("an event attaches to an ENT entity")
        if not isinstance(self.event_class, str) or CLASS_PATTERN.fullmatch(self.event_class) is None:
            raise EventModelError(f"not an event class identifier: {self.event_class!r}")
        if not registered(self.event_class):
            raise EventModelError(f"{self.event_class} is not a registered event class")
        if not isinstance(self.time, EventTime) or not isinstance(self.assertion, Assertion):
            raise EventModelError("an event has an EventTime and an Assertion")
        if not isinstance(self.provenance, RecordProvenance):
            raise EventModelError("an event carries its provenance")
        if self.data_class is not DataClass.SYNTHETIC:
            raise EventModelError("V1 permits synthetic data only (ADR-0113 s2 C3)")
        if self.subclass is not None and (not isinstance(self.subclass, str) or _TOKEN.fullmatch(self.subclass) is None):
            raise EventModelError("a subclass is a snake_case token")
        if self.domain is not None and self.domain != CLASS_DOMAIN:
            raise EventModelError(f"the registered classes are local to the {CLASS_DOMAIN} domain")
        if self.assertion_context is not None and not isinstance(self.assertion_context, AssertionContext):
            raise EventModelError("an assertion context must be an AssertionContext")


@dataclass(frozen=True, slots=True)
class Confirmation:
    """A human's answer about one revision of an event. Held apart from the assertion (H1 s4, s5)."""

    state: ConfirmationState
    confirmer_kind: ConfirmerKind
    confirmer_reference: str
    confirmed_at: str
    statement: str
    provenance: RecordProvenance

    def __post_init__(self):
        if not isinstance(self.state, ConfirmationState):
            raise EventModelError("a confirmation state must be a ConfirmationState")
        if not isinstance(self.confirmer_kind, ConfirmerKind):
            raise EventModelError("only a human confirms: the confirmer is a subject or a human reviewer")
        _text("confirmer_reference", self.confirmer_reference)
        _timestamp("confirmed_at", self.confirmed_at)
        if not isinstance(self.statement, str):
            raise EventModelError("a statement is text")
        if self.state in (ConfirmationState.PARTIALLY_CONFIRMED, ConfirmationState.REJECTED) and \
                not self.statement.strip():
            raise EventModelError("a partial confirmation or a rejection says what was wrong")
        if not isinstance(self.provenance, RecordProvenance):
            raise EventModelError("a confirmation carries its provenance")


#: Every field each record type may carry. The store refuses any other key, so nothing else can be smuggled in.
EVENT_FIELDS = tuple(f.name for f in fields(EventRecord))
TIME_FIELDS = tuple(f.name for f in fields(EventTime))
ASSERTION_FIELDS = tuple(f.name for f in fields(Assertion))
CONTEXT_FIELDS = tuple(f.name for f in fields(AssertionContext))
CONFIRMATION_FIELDS = tuple(f.name for f in fields(Confirmation))


def validation_input_permitted(record: EventRecord, state: ConfirmationState) -> bool:
    """H1 s3: a system hypothesis is not validation input until a human confirms it. A rejection never is.

    This admits or refuses; it scores nothing. H2 and H4 may add requirements; none is relaxed.
    """

    if not isinstance(record, EventRecord) or not isinstance(state, ConfirmationState):
        raise EventModelError("validation admissibility needs an EventRecord and a ConfirmationState")
    if state is ConfirmationState.REJECTED:
        return False
    if record.assertion.asserter_kind is AsserterKind.SYSTEM_HYPOTHESIS:
        return state in (ConfirmationState.CONFIRMED, ConfirmationState.PARTIALLY_CONFIRMED)
    return True
