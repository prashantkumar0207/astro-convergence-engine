"""The append-only event store, its confirmations, and the EVR issuer (ADR-0113 s2 B, C; ADR-0115 s3).

The store shares one SQLite database with the EntityStore whose entities its events attach to, and
keeps its own tables and its own issuer. A number is taken in the same transaction that writes the
event, so a failed or refused persistence takes none. Each store instance is its own issuer, which
is how fixtures stay isolated.

Nothing is ever updated or deleted: triggers refuse both at the database layer. A correction
appends a revision, with its reason. A confirmation is a separate record naming the revision it
answers, so confirming never rewrites an assertion, and a correction is never confirmed by an
answer given about an earlier revision.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from engine.evidence.entity import DataClass, RecordProvenance
from engine.evidence.event_identifiers import FAMILY, LAST, EventRecordId
from engine.evidence.events import (
    ASSERTION_FIELDS, CONFIRMATION_FIELDS, CONTEXT_FIELDS, EVENT_FIELDS, TIME_FIELDS, Assertion, AssertionContext,
    AsserterCertainty, AsserterKind, Confirmation, ConfirmationState, ConfirmerKind, EventRecord, EventTime,
    TimeKind, TimeTolerance, TimeUnit, WindowShape, validation_input_permitted,
)
from engine.evidence.identifiers import EntityId
from engine.evidence.store import EntityStore, StoreError

SCHEMA_VERSION = "ace-event-store-v1"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS event_issuer (family TEXT PRIMARY KEY, last_number INTEGER NOT NULL CHECK (last_number >= 0));
CREATE TABLE IF NOT EXISTS event_revisions (
    event_id TEXT NOT NULL CHECK (event_id GLOB 'EVR-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    revision INTEGER NOT NULL CHECK (revision >= 1),
    entity_id TEXT NOT NULL,
    payload TEXT NOT NULL,
    reason TEXT NOT NULL,
    PRIMARY KEY (event_id, revision)
);
CREATE TABLE IF NOT EXISTS event_confirmations (
    confirmation_number INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT NOT NULL,
    revision INTEGER NOT NULL,
    payload TEXT NOT NULL
);
CREATE TRIGGER IF NOT EXISTS event_revisions_no_update BEFORE UPDATE ON event_revisions
    BEGIN SELECT RAISE(ABORT, 'event revisions are append-only'); END;
CREATE TRIGGER IF NOT EXISTS event_revisions_no_delete BEFORE DELETE ON event_revisions
    BEGIN SELECT RAISE(ABORT, 'event revisions are append-only'); END;
CREATE TRIGGER IF NOT EXISTS confirmations_no_update BEFORE UPDATE ON event_confirmations
    BEGIN SELECT RAISE(ABORT, 'confirmations are append-only'); END;
CREATE TRIGGER IF NOT EXISTS confirmations_no_delete BEFORE DELETE ON event_confirmations
    BEGIN SELECT RAISE(ABORT, 'confirmations are append-only'); END;
CREATE TRIGGER IF NOT EXISTS event_issuer_never_decreases BEFORE UPDATE ON event_issuer
    WHEN NEW.last_number < OLD.last_number
    BEGIN SELECT RAISE(ABORT, 'the EVR issuer never reuses a number'); END;
CREATE TRIGGER IF NOT EXISTS event_issuer_no_delete BEFORE DELETE ON event_issuer
    BEGIN SELECT RAISE(ABORT, 'the EVR issuer cannot be removed'); END;
"""


def _provenance_record(provenance: RecordProvenance) -> dict:
    return {"source": provenance.source, "method": provenance.method, "schema_version": provenance.schema_version}


def _time_record(time: EventTime) -> dict:
    tolerance = time.tolerance
    return {
        "kind": time.kind.value,
        "precision": None if time.precision is None else time.precision.value,
        "timezone": time.timezone,
        "timezone_source": time.timezone_source,
        "at": time.at,
        "start": time.start,
        "end": time.end,
        "tolerance": None if tolerance is None else {"amount": tolerance.amount, "unit": tolerance.unit.value},
        "window_shape": time.window_shape.value,
        "birth_time_sensitive": time.birth_time_sensitive,
    }


def event_to_record(event: EventRecord) -> dict:
    """The stored form of an event, written field by field so the schema is explicit."""

    if not isinstance(event, EventRecord):
        raise StoreError("only an EventRecord can be stored as an event")
    assertion, context = event.assertion, event.assertion_context
    return {"schema": SCHEMA_VERSION, "event": {
        "entity": event.entity.value,
        "event_class": event.event_class,
        "time": _time_record(event.time),
        "assertion": {"asserter_kind": assertion.asserter_kind.value,
                      "asserter_reference": assertion.asserter_reference, "asserted_at": assertion.asserted_at,
                      "method": assertion.method, "asserter_certainty": assertion.asserter_certainty.value},
        "provenance": _provenance_record(event.provenance),
        "data_class": event.data_class.value,
        "subclass": event.subclass,
        "domain": event.domain,
        "assertion_context": None if context is None else {
            "entity_revision": context.entity_revision, "chart_label": context.chart_label,
            "provenance": _provenance_record(context.provenance)},
    }}


def _exact(name: str, data, expected) -> dict:
    """Refuse any key the model does not define, at every level (H1 s5)."""

    if not isinstance(data, dict) or set(data) != set(expected):
        extra = sorted(set(data) - set(expected)) if isinstance(data, dict) else data
        raise StoreError(f"{name} carries only its model fields; refused: {extra}")
    return data


def _provenance(data) -> RecordProvenance:
    data = _exact("provenance", data, ("source", "method", "schema_version"))
    return RecordProvenance(source=data["source"], method=data["method"], schema_version=data["schema_version"])


def _time(data) -> EventTime:
    data = _exact("time", data, TIME_FIELDS)
    tolerance = data["tolerance"]
    if tolerance is not None:
        tolerance = _exact("tolerance", tolerance, ("amount", "unit"))
        tolerance = TimeTolerance(amount=tolerance["amount"], unit=TimeUnit(tolerance["unit"]))
    return EventTime(kind=TimeKind(data["kind"]),
                     precision=None if data["precision"] is None else TimeUnit(data["precision"]),
                     timezone=data["timezone"], timezone_source=data["timezone_source"], at=data["at"],
                     start=data["start"], end=data["end"], tolerance=tolerance,
                     window_shape=WindowShape(data["window_shape"]), birth_time_sensitive=data["birth_time_sensitive"])


def event_from_record(record: dict) -> EventRecord:
    """Rebuild an event, refusing any key the model does not define, at any level."""

    if not isinstance(record, dict) or set(record) != {"schema", "event"} or record["schema"] != SCHEMA_VERSION:
        raise StoreError("not an event record of this schema")
    data = _exact("an event", record["event"], EVENT_FIELDS)
    assertion = _exact("an assertion", data["assertion"], ASSERTION_FIELDS)
    context = data["assertion_context"]
    if context is not None:
        context = _exact("an assertion context", context, CONTEXT_FIELDS)
        context = AssertionContext(entity_revision=context["entity_revision"], chart_label=context["chart_label"],
                                   provenance=_provenance(context["provenance"]))
    return EventRecord(
        entity=EntityId(data["entity"]), event_class=data["event_class"], time=_time(data["time"]),
        assertion=Assertion(asserter_kind=AsserterKind(assertion["asserter_kind"]),
                            asserter_reference=assertion["asserter_reference"],
                            asserted_at=assertion["asserted_at"], method=assertion["method"],
                            asserter_certainty=AsserterCertainty(assertion["asserter_certainty"])),
        provenance=_provenance(data["provenance"]), data_class=DataClass(data["data_class"]),
        subclass=data["subclass"], domain=data["domain"], assertion_context=context)


def confirmation_to_record(confirmation: Confirmation) -> dict:
    if not isinstance(confirmation, Confirmation):
        raise StoreError("only a Confirmation can be stored as a confirmation")
    return {"schema": SCHEMA_VERSION, "confirmation": {
        "state": confirmation.state.value, "confirmer_kind": confirmation.confirmer_kind.value,
        "confirmer_reference": confirmation.confirmer_reference, "confirmed_at": confirmation.confirmed_at,
        "statement": confirmation.statement, "provenance": _provenance_record(confirmation.provenance)}}


def confirmation_from_record(record: dict) -> Confirmation:
    """Rebuild a confirmation. A system confirmer is not a ConfirmerKind, so it cannot be rebuilt."""

    if not isinstance(record, dict) or set(record) != {"schema", "confirmation"} or \
            record["schema"] != SCHEMA_VERSION:
        raise StoreError("not a confirmation record of this schema")
    data = _exact("a confirmation", record["confirmation"], CONFIRMATION_FIELDS)
    try:
        confirmer = ConfirmerKind(data["confirmer_kind"])
    except ValueError as exc:
        raise StoreError(f"only a human confirms; refused confirmer {data['confirmer_kind']!r}") from exc
    return Confirmation(state=ConfirmationState(data["state"]), confirmer_kind=confirmer,
                        confirmer_reference=data["confirmer_reference"], confirmed_at=data["confirmed_at"],
                        statement=data["statement"], provenance=_provenance(data["provenance"]))


def _encode(record: dict) -> str:
    return json.dumps(record, sort_keys=True, separators=(",", ":"))


def _without_context(payload: str) -> str:
    """An event's stored form with its assertion context removed: equal ones are the same assertion."""

    data = json.loads(payload)
    data["event"]["assertion_context"] = None
    return _encode(data)


class EventStore:
    """An append-only event store over the entity database at `path`, and this store's own EVR issuer."""

    def __init__(self, path: Path | str):
        self.path = Path(path)
        self.entities = EntityStore(self.path)
        self._db = sqlite3.connect(str(self.path), isolation_level=None, timeout=10.0)
        self._db.executescript(_SCHEMA)
        self._db.execute("INSERT OR IGNORE INTO event_issuer (family, last_number) VALUES (?, 0)", (FAMILY,))

    def close(self) -> None:
        self._db.close()
        self.entities.close()

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        self.close()

    @staticmethod
    def _payload(event: EventRecord) -> str:
        payload = _encode(event_to_record(event))
        event_from_record(json.loads(payload))  # Refuse anything that would not reload.
        return payload

    def persist(self, event: EventRecord, reason: str = "first record") -> EventRecordId:
        """Write a new event and issue its EVR number, in one transaction."""

        payload = self._payload(event)
        self._db.execute("BEGIN IMMEDIATE")
        try:
            (last,) = self._db.execute("SELECT last_number FROM event_issuer WHERE family = ?", (FAMILY,)).fetchone()
            if last >= LAST:
                raise StoreError("the EVR family is exhausted")
            event_id = EventRecordId.from_number(last + 1)
            self._check_attachment(event)
            self._check_not_duplicated(event_id, event.entity, payload)
            self._db.execute("INSERT INTO event_revisions (event_id, revision, entity_id, payload, reason) "
                             "VALUES (?, 1, ?, ?, ?)", (event_id.value, event.entity.value, payload, reason))
            self._db.execute("UPDATE event_issuer SET last_number = ? WHERE family = ?", (last + 1, FAMILY))
            self._db.execute("COMMIT")
        except BaseException:
            self._db.execute("ROLLBACK")
            raise
        return event_id

    def append_revision(self, event_id: EventRecordId, event: EventRecord, reason: str) -> int:
        """Record a correction as a new revision. The superseded revision stays, and so do its confirmations."""

        if not isinstance(reason, str) or not reason.strip():
            raise StoreError("a correction records its reason")
        payload = self._payload(event)
        self._db.execute("BEGIN IMMEDIATE")
        try:
            revision, current = self._current(event_id)
            if event.entity != current.entity:
                raise StoreError("a correction cannot re-anchor an event to another entity")
            if event.assertion_context != current.assertion_context:
                raise StoreError("a correction cannot re-anchor an event to another assertion context")
            before, after = current.assertion, event.assertion
            if (after.asserter_kind, after.asserter_reference, after.asserted_at) != \
                    (before.asserter_kind, before.asserter_reference, before.asserted_at):
                raise StoreError("a correction cannot change who asserted the event, or when")
            self._check_not_duplicated(event_id, event.entity, payload)
            self._db.execute("INSERT INTO event_revisions (event_id, revision, entity_id, payload, reason) "
                             "VALUES (?, ?, ?, ?, ?)", (event_id.value, revision + 1, event.entity.value, payload,
                                                        reason))
            self._db.execute("COMMIT")
        except BaseException:
            self._db.execute("ROLLBACK")
            raise
        return revision + 1

    def confirm(self, event_id: EventRecordId, revision: int, confirmation: Confirmation) -> int:
        """Record a human's answer about one revision. Only the current revision can be answered."""

        payload = _encode(confirmation_to_record(confirmation))
        confirmation_from_record(json.loads(payload))
        self._db.execute("BEGIN IMMEDIATE")
        try:
            current, _event = self._current(event_id)
            if revision != current:
                raise StoreError(f"{event_id} is at revision {current}; a confirmation answers the current revision")
            cursor = self._db.execute("INSERT INTO event_confirmations (event_id, revision, payload) VALUES (?, ?, ?)",
                                      (event_id.value, revision, payload))
            self._db.execute("COMMIT")
        except BaseException:
            self._db.execute("ROLLBACK")
            raise
        return cursor.lastrowid

    def _current(self, event_id: EventRecordId) -> tuple:
        if not isinstance(event_id, EventRecordId):
            raise StoreError("events are addressed by their EVR identifier")
        row = self._db.execute("SELECT revision, payload FROM event_revisions WHERE event_id = ? "
                               "ORDER BY revision DESC LIMIT 1", (event_id.value,)).fetchone()
        if row is None:
            raise StoreError(f"no such event: {event_id}")
        return row[0], event_from_record(json.loads(row[1]))

    def _check_attachment(self, event: EventRecord) -> None:
        """The entity exists here; an assertion context names one of its revisions and a chart of that revision.

        Entity revisions are append-only, so a reference valid now stays valid.
        """

        if event.entity not in self.entities.entity_ids():
            raise StoreError(f"entity {event.entity} is not in this store")
        context = event.assertion_context
        if context is None:
            return
        history = self.entities.history(event.entity)
        if context.entity_revision > len(history):
            raise StoreError(f"{event.entity} has no revision {context.entity_revision}")
        _number, subject, _reason = history[context.entity_revision - 1]
        if context.chart_label not in {chart.label for chart in subject.charts}:
            raise StoreError(f"{context.chart_label!r} is not a chart of {event.entity} at revision "
                             f"{context.entity_revision}")

    def _check_not_duplicated(self, event_id: EventRecordId, entity: EntityId, payload: str) -> None:
        """Refuse an assertion already recorded for this entity, under this chart context or another (ADR-0113 s2 C2)."""

        key = _without_context(payload)
        rows = self._db.execute(
            "SELECT r.event_id, r.payload FROM event_revisions AS r JOIN (SELECT event_id, MAX(revision) AS top "
            "FROM event_revisions WHERE entity_id = ? GROUP BY event_id) AS m "
            "ON r.event_id = m.event_id AND r.revision = m.top", (entity.value,))
        for other, other_payload in rows:
            if other != event_id.value and _without_context(other_payload) == key:
                raise StoreError(f"this assertion is already recorded as {other}; an event is never duplicated "
                                 f"across charts")

    def history(self, event_id: EventRecordId) -> list:
        rows = self._db.execute(
            "SELECT revision, payload, reason FROM event_revisions WHERE event_id = ? ORDER BY revision",
            (event_id.value,)).fetchall()
        if not rows:
            raise StoreError(f"no such event: {event_id}")
        return [(revision, event_from_record(json.loads(payload)), reason) for revision, payload, reason in rows]

    def load(self, event_id: EventRecordId) -> EventRecord:
        return self.history(event_id)[-1][1]

    def event_ids(self) -> list:
        return [EventRecordId(value) for (value,) in self._db.execute(
            "SELECT DISTINCT event_id FROM event_revisions ORDER BY event_id")]

    def confirmations(self, event_id: EventRecordId) -> list:
        """Every confirmation of every revision, in the order given: (revision, Confirmation)."""

        self.history(event_id)
        return [(revision, confirmation_from_record(json.loads(payload))) for revision, payload in self._db.execute(
            "SELECT revision, payload FROM event_confirmations WHERE event_id = ? ORDER BY confirmation_number",
            (event_id.value,))]

    def confirmation_state(self, event_id: EventRecordId) -> ConfirmationState:
        """The latest answer about the current revision. A revision nobody has answered is UNCONFIRMED."""

        current, _event = self._current(event_id)
        answers = [confirmation.state for revision, confirmation in self.confirmations(event_id) if revision == current]
        return answers[-1] if answers else ConfirmationState.UNCONFIRMED

    def validation_input_permitted(self, event_id: EventRecordId) -> bool:
        return validation_input_permitted(self.load(event_id), self.confirmation_state(event_id))

    def issued_count(self) -> int:
        return self._db.execute("SELECT last_number FROM event_issuer WHERE family = ?", (FAMILY,)).fetchone()[0]
