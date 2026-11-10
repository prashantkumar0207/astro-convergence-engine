"""The historical event ledger and its protected holdouts (the H2 specification v2.0.0, ADR-0113; ADR-0116).

- PAST (H2 s2): an entry admits an H1 event only once a human has answered its current revision.
  Confirmed and partially confirmed events are past. A rejected event is kept as a rejection, with
  the same permanence (H2 s4).
- Elicitation (H2 s4): every entry records whether the event was volunteered or prompted, and on
  what basis, so the two populations are never mixed.
- Correction without destruction (H2 s6): an entry pins the event revision and answer it relies on.
  A correction appends a superseding entry with its reason; the superseded entry stays.
- Holdouts (H2 s5; ADR-0113 s2 D1): an eligible set is frozen, and in the same transaction the store
  draws its own seed and selects the holdout by a recorded, reproducible hash ordering. An event can
  belong to one frozen set only, ever, so no equivalent or overlapping set can be frozen again under
  another seed. Protection is set once, at selection, and nothing clears it.
- Access (H2 s5, s9): every ledger read, an entry's history included, declares a purpose and is
  logged, granted or refused; a malformed request is logged as a refusal, never let past the log.
  Protected entries are never served for selection, tuning, rectification or development. Protected
  validation needs a protocol registered after the holdout was locked and before the read, naming
  that holdout, with the holdout holding at least the protocol's minimum N.
- Protocols (ADR-0021 D1; ADR-0113 s2 D2): every pre-registration field, fixed before testing, and
  immutable. No RUL family is registered, so rule references stay empty (ADR-0116 s4).

What this does NOT control. The purpose check governs reads through this ledger only. The same
events can be read without any purpose through EventStore and EntityStore, through this object's
database connection, or by opening the SQLite file directly; none of those reads is logged. The
leakage check therefore proves only that no ledger read leaked, never that no process anywhere read
a protected event.

Nothing here scores, weights, fits, ranks by merit, or computes a rate, ratio or confidence. Counts
are returned with their members, so every count decomposes. Synthetic data only.
"""

from __future__ import annotations

import hashlib
import json
import secrets
import sqlite3
from dataclasses import dataclass, fields
from enum import Enum
from pathlib import Path

from engine.evidence.entity import DataClass, RecordProvenance
from engine.evidence.event_classes import registered
from engine.evidence.event_identifiers import EventRecordId
from engine.evidence.event_store import EventStore
from engine.evidence.events import ConfirmationState
from engine.evidence.store import StoreError

SCHEMA_VERSION = "ace-ledger-v1"
#: The selection procedure, recorded with every holdout so it can be re-derived.
PROCEDURE = "ace-holdout-sha256-order-v1"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS ledger_entries (
    entry_number INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT NOT NULL,
    supersedes INTEGER UNIQUE REFERENCES ledger_entries (entry_number),
    payload TEXT NOT NULL,
    reason TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS eligible_sets (
    set_number INTEGER PRIMARY KEY AUTOINCREMENT,
    content_hash TEXT NOT NULL UNIQUE,
    payload TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS eligible_members (
    event_id TEXT PRIMARY KEY,
    set_number INTEGER NOT NULL REFERENCES eligible_sets (set_number)
);
CREATE TABLE IF NOT EXISTS holdouts (
    holdout_number INTEGER PRIMARY KEY AUTOINCREMENT,
    set_number INTEGER NOT NULL UNIQUE REFERENCES eligible_sets (set_number),
    after_access INTEGER NOT NULL,
    payload TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS protected_events (
    event_id TEXT PRIMARY KEY,
    holdout_number INTEGER NOT NULL REFERENCES holdouts (holdout_number)
);
CREATE TABLE IF NOT EXISTS protocols (
    protocol_number INTEGER PRIMARY KEY AUTOINCREMENT,
    holdout_number INTEGER NOT NULL REFERENCES holdouts (holdout_number),
    after_access INTEGER NOT NULL,
    payload TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS access_log (
    access_number INTEGER PRIMARY KEY AUTOINCREMENT,
    purpose TEXT NOT NULL,
    protocol_number INTEGER,
    granted INTEGER NOT NULL CHECK (granted IN (0, 1)),
    served TEXT NOT NULL,
    note TEXT NOT NULL
);
"""
_APPEND_ONLY = ("ledger_entries", "eligible_sets", "eligible_members", "holdouts", "protected_events", "protocols",
                "access_log")
_TRIGGERS = "".join(
    f"CREATE TRIGGER IF NOT EXISTS {table}_no_update BEFORE UPDATE ON {table} "
    f"BEGIN SELECT RAISE(ABORT, '{table} is append-only'); END;\n"
    f"CREATE TRIGGER IF NOT EXISTS {table}_no_delete BEFORE DELETE ON {table} "
    f"BEGIN SELECT RAISE(ABORT, '{table} is append-only'); END;\n"
    for table in _APPEND_ONLY)


class LedgerError(StoreError):
    """The ledger refused an operation."""


class Elicitation(Enum):
    """H2 s4: how the event reached the ledger. The populations have different evidential standing."""

    VOLUNTEERED = "volunteered"
    PROMPTED_BY_EXPECTATION = "prompted_by_expectation"
    PROMPTED_FOR_NULL_PERIOD = "prompted_for_null_period"


class Outcome(Enum):
    """What the human answer made of the event. Derived by the ledger, never supplied."""

    PAST_CONFIRMED = "past_confirmed"
    PAST_PARTIALLY_CONFIRMED = "past_partially_confirmed"
    REJECTED = "rejected"


class Purpose(Enum):
    """Why a ledger read is made. Declared on every read, and logged."""

    SELECTION = "selection"
    TUNING = "tuning"
    RECTIFICATION = "rectification"
    DEVELOPMENT = "development"
    PROTECTED_VALIDATION = "protected_validation"
    AUDIT = "audit"


#: How a read made with no declared Purpose is logged. It is always refused.
UNDECLARED = "undeclared"
#: Purposes that may never see a protected entry (H2 s5, s9).
EXCLUDED_FROM_PROTECTED = frozenset({Purpose.SELECTION, Purpose.TUNING, Purpose.RECTIFICATION, Purpose.DEVELOPMENT})
#: Purposes whose counts may include protected entries (ADR-0113 s2 D3).
DISCLOSES_PROTECTED = frozenset({Purpose.AUDIT, Purpose.PROTECTED_VALIDATION})

_OUTCOMES = {ConfirmationState.CONFIRMED: Outcome.PAST_CONFIRMED,
             ConfirmationState.PARTIALLY_CONFIRMED: Outcome.PAST_PARTIALLY_CONFIRMED,
             ConfirmationState.REJECTED: Outcome.REJECTED}


def _text(name: str, value) -> None:
    if not isinstance(value, str) or not value.strip():
        raise LedgerError(f"{name} is required")


def _texts(name: str, value, allow_empty: bool = False) -> None:
    if not isinstance(value, tuple) or (not value and not allow_empty):
        raise LedgerError(f"{name} is a {'' if allow_empty else 'non-empty '}tuple")
    for item in value:
        _text(name, item)


def _count(name: str, value) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise LedgerError(f"{name} is a whole number, at least 1")


@dataclass(frozen=True, slots=True)
class LedgerEntry:
    """One event's standing in the ledger, pinned to the revision and the answer it relies on."""

    event: EventRecordId
    event_revision: int
    answer_index: int
    outcome: Outcome
    event_class: str
    elicitation: Elicitation
    provenance: RecordProvenance
    data_class: DataClass

    def __post_init__(self):
        if not isinstance(self.event, EventRecordId):
            raise LedgerError("a ledger entry names an EVR event")
        _count("event_revision", self.event_revision)
        _count("answer_index", self.answer_index)
        if not isinstance(self.outcome, Outcome) or not isinstance(self.elicitation, Elicitation):
            raise LedgerError("outcome and elicitation must be their enums")
        if not registered(self.event_class):
            raise LedgerError(f"{self.event_class!r} is not a registered event class")
        if not isinstance(self.provenance, RecordProvenance):
            raise LedgerError("a ledger entry carries its provenance")
        if self.data_class is not DataClass.SYNTHETIC:
            raise LedgerError("V1 permits synthetic data only (ADR-0113 s2 C3)")


@dataclass(frozen=True, slots=True)
class Holdout:
    """A frozen eligible set and the holdout selected from it, as recorded at the freeze."""

    criteria: str
    members: tuple
    content_hash: str
    seed: str
    procedure: str
    size: int
    selected: tuple
    selection_hash: str


@dataclass(frozen=True, slots=True)
class Protocol:
    """A pre-registered validation protocol: every ADR-0021 D1 field, and a minimum N (ADR-0113 s2 D2)."""

    holdout: int
    event_classes: tuple
    hypotheses: tuple
    rule_references: tuple
    development_set: str
    hypothesis_count: int
    event_count: int
    multiple_comparison_method: str
    effect_size_measures: tuple
    negative_controls: tuple
    replication: str
    minimum_n: int
    provenance: RecordProvenance
    data_class: DataClass

    def __post_init__(self):
        _count("holdout", self.holdout)
        _texts("event_classes", self.event_classes)
        for event_class in self.event_classes:
            if not registered(event_class):
                raise LedgerError(f"{event_class!r} is not a registered event class")
        _texts("hypotheses", self.hypotheses)
        if self.rule_references != ():
            raise LedgerError("no RUL family is registered, so a protocol cannot cite rules yet (ADR-0116 s4)")
        _text("development_set", self.development_set)
        _count("hypothesis_count", self.hypothesis_count)
        if self.hypothesis_count != len(self.hypotheses):
            raise LedgerError("hypothesis_count must equal the hypotheses declared")
        _count("event_count", self.event_count)
        _text("multiple_comparison_method", self.multiple_comparison_method)
        _texts("effect_size_measures", self.effect_size_measures)
        _texts("negative_controls", self.negative_controls)
        _text("replication", self.replication)
        _count("minimum_n", self.minimum_n)
        if not isinstance(self.provenance, RecordProvenance):
            raise LedgerError("a protocol carries its provenance")
        if self.data_class is not DataClass.SYNTHETIC:
            raise LedgerError("V1 permits synthetic data only (ADR-0113 s2 C3)")


ENTRY_FIELDS = tuple(f.name for f in fields(LedgerEntry))
HOLDOUT_FIELDS = tuple(f.name for f in fields(Holdout))
PROTOCOL_FIELDS = tuple(f.name for f in fields(Protocol))


def content_hash(members) -> str:
    """The identity of a frozen set: SHA-256 over its sorted EVR identifiers."""

    return hashlib.sha256("\n".join(sorted(member.value for member in members)).encode("ascii")).hexdigest()


def ordered_selection(seed: str, members, size: int) -> tuple:
    """The recorded procedure: order members by SHA-256 of procedure, seed and identifier; take `size`.

    A pure function of its arguments, independent of any library's random generator, so anyone holding
    the record can re-derive the selection on any platform.
    """

    if not isinstance(seed, str) or not seed or not 1 <= size <= len(members):
        raise LedgerError("a selection needs a seed and a size between 1 and the set's size")
    order = sorted(members, key=lambda member: hashlib.sha256(
        f"{PROCEDURE}|{seed}|{member.value}".encode("ascii")).hexdigest())
    return tuple(sorted(order[:size]))


def selection_hash(selected) -> str:
    return content_hash(selected)


def _provenance_record(provenance: RecordProvenance) -> dict:
    return {"source": provenance.source, "method": provenance.method, "schema_version": provenance.schema_version}


def _exact(name: str, data, expected) -> dict:
    if not isinstance(data, dict) or set(data) != set(expected):
        extra = sorted(set(data) - set(expected)) if isinstance(data, dict) else data
        raise LedgerError(f"{name} carries only its model fields; refused: {extra}")
    return data


def _provenance(data) -> RecordProvenance:
    data = _exact("provenance", data, ("source", "method", "schema_version"))
    return RecordProvenance(source=data["source"], method=data["method"], schema_version=data["schema_version"])


def entry_to_record(entry: LedgerEntry) -> dict:
    if not isinstance(entry, LedgerEntry):
        raise LedgerError("only a LedgerEntry can be stored as an entry")
    return {"schema": SCHEMA_VERSION, "entry": {
        "event": entry.event.value, "event_revision": entry.event_revision, "answer_index": entry.answer_index,
        "outcome": entry.outcome.value, "event_class": entry.event_class, "elicitation": entry.elicitation.value,
        "provenance": _provenance_record(entry.provenance), "data_class": entry.data_class.value}}


def entry_from_record(record: dict) -> LedgerEntry:
    if not isinstance(record, dict) or set(record) != {"schema", "entry"} or record["schema"] != SCHEMA_VERSION:
        raise LedgerError("not a ledger entry of this schema")
    data = _exact("a ledger entry", record["entry"], ENTRY_FIELDS)
    return LedgerEntry(event=EventRecordId(data["event"]), event_revision=data["event_revision"],
                       answer_index=data["answer_index"], outcome=Outcome(data["outcome"]),
                       event_class=data["event_class"], elicitation=Elicitation(data["elicitation"]),
                       provenance=_provenance(data["provenance"]), data_class=DataClass(data["data_class"]))


def holdout_to_record(holdout: Holdout) -> dict:
    return {"schema": SCHEMA_VERSION, "holdout": {
        "criteria": holdout.criteria, "members": [member.value for member in holdout.members],
        "content_hash": holdout.content_hash, "seed": holdout.seed, "procedure": holdout.procedure,
        "size": holdout.size, "selected": [member.value for member in holdout.selected],
        "selection_hash": holdout.selection_hash}}


def holdout_from_record(record: dict) -> Holdout:
    if not isinstance(record, dict) or set(record) != {"schema", "holdout"} or record["schema"] != SCHEMA_VERSION:
        raise LedgerError("not a holdout record of this schema")
    data = _exact("a holdout", record["holdout"], HOLDOUT_FIELDS)
    return Holdout(criteria=data["criteria"], members=tuple(EventRecordId(value) for value in data["members"]),
                   content_hash=data["content_hash"], seed=data["seed"], procedure=data["procedure"],
                   size=data["size"], selected=tuple(EventRecordId(value) for value in data["selected"]),
                   selection_hash=data["selection_hash"])


def protocol_to_record(protocol: Protocol) -> dict:
    if not isinstance(protocol, Protocol):
        raise LedgerError("only a Protocol can be registered")
    return {"schema": SCHEMA_VERSION, "protocol": {
        "holdout": protocol.holdout, "event_classes": list(protocol.event_classes),
        "hypotheses": list(protocol.hypotheses), "rule_references": list(protocol.rule_references),
        "development_set": protocol.development_set, "hypothesis_count": protocol.hypothesis_count,
        "event_count": protocol.event_count, "multiple_comparison_method": protocol.multiple_comparison_method,
        "effect_size_measures": list(protocol.effect_size_measures),
        "negative_controls": list(protocol.negative_controls), "replication": protocol.replication,
        "minimum_n": protocol.minimum_n, "provenance": _provenance_record(protocol.provenance),
        "data_class": protocol.data_class.value}}


def protocol_from_record(record: dict) -> Protocol:
    if not isinstance(record, dict) or set(record) != {"schema", "protocol"} or record["schema"] != SCHEMA_VERSION:
        raise LedgerError("not a protocol record of this schema")
    data = _exact("a protocol", record["protocol"], PROTOCOL_FIELDS)
    return Protocol(
        holdout=data["holdout"], event_classes=tuple(data["event_classes"]), hypotheses=tuple(data["hypotheses"]),
        rule_references=tuple(data["rule_references"]), development_set=data["development_set"],
        hypothesis_count=data["hypothesis_count"], event_count=data["event_count"],
        multiple_comparison_method=data["multiple_comparison_method"],
        effect_size_measures=tuple(data["effect_size_measures"]), negative_controls=tuple(data["negative_controls"]),
        replication=data["replication"], minimum_n=data["minimum_n"], provenance=_provenance(data["provenance"]),
        data_class=DataClass(data["data_class"]))


#: Stands in for a history read that names no event, so the refusal is decided, and logged, like any other.
_MISSING = object()
#: SQLite stores a signed 64-bit integer; a protocol number outside 1 .. 2**63 - 1 is malformed.
_PROTOCOL_LIMIT = 2 ** 63


def _protocol_number(value) -> bool:
    """A well-formed protocol number: a plain int (not bool) that SQLite can store, and positive."""

    return type(value) is int and 0 < value < _PROTOCOL_LIMIT


def _encode(record: dict) -> str:
    return json.dumps(record, sort_keys=True, separators=(",", ":"))



class HistoricalLedger:
    """The append-only ledger over the event database at `path`, with its holdouts, protocols and access log."""

    def __init__(self, path: Path | str):
        self.path = Path(path)
        self.events = EventStore(self.path)
        self._db = sqlite3.connect(str(self.path), isolation_level=None, timeout=10.0)
        self._db.executescript(_SCHEMA + _TRIGGERS)

    def close(self) -> None:
        self._db.close()
        self.events.close()

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        self.close()

    # ------------------------------------------------------------ admission and correction

    def _entry_for(self, event_id: EventRecordId, elicitation: Elicitation, provenance: RecordProvenance) -> LedgerEntry:
        """Build the entry from the event's current revision and its latest human answer."""

        history = self.events.history(event_id)
        revision, event, _reason = history[-1]
        answers = self.events.confirmations(event_id)
        state = self.events.confirmation_state(event_id)
        if state not in _OUTCOMES:
            raise LedgerError(f"{event_id} revision {revision} has no human answer; only answered events are admitted")
        index = max(position for position, (answered, _answer) in enumerate(answers, 1) if answered == revision)
        return LedgerEntry(event=event_id, event_revision=revision, answer_index=index, outcome=_OUTCOMES[state],
                           event_class=event.event_class, elicitation=elicitation, provenance=provenance,
                           data_class=DataClass.SYNTHETIC)

    def admit(self, event_id: EventRecordId, elicitation: Elicitation, provenance: RecordProvenance) -> int:
        """Admit an answered event. Returns the entry number."""

        if not isinstance(elicitation, Elicitation):
            raise LedgerError("every entry records how the event was elicited (H2 s4)")
        entry = self._entry_for(event_id, elicitation, provenance)
        self._db.execute("BEGIN IMMEDIATE")
        try:
            if self._current_number(event_id) is not None:
                raise LedgerError(f"{event_id} is already in the ledger; record a correction instead")
            cursor = self._db.execute("INSERT INTO ledger_entries (event_id, supersedes, payload, reason) "
                                      "VALUES (?, NULL, ?, 'first record')",
                                      (event_id.value, _encode(entry_to_record(entry))))
            self._db.execute("COMMIT")
        except BaseException:
            self._db.execute("ROLLBACK")
            raise
        return cursor.lastrowid

    def correct(self, event_id: EventRecordId, elicitation: Elicitation, provenance: RecordProvenance,
                reason: str) -> int:
        """Append a superseding entry from the event's current revision and answer (H2 s6)."""

        _text("reason", reason)
        if not isinstance(elicitation, Elicitation):
            raise LedgerError("every entry records how the event was elicited (H2 s4)")
        entry = self._entry_for(event_id, elicitation, provenance)
        self._db.execute("BEGIN IMMEDIATE")
        try:
            previous = self._current_number(event_id)
            if previous is None:
                raise LedgerError(f"{event_id} is not in the ledger; admit it first")
            if entry == self._entry(previous):
                raise LedgerError("a correction must change something")
            cursor = self._db.execute("INSERT INTO ledger_entries (event_id, supersedes, payload, reason) "
                                      "VALUES (?, ?, ?, ?)",
                                      (event_id.value, previous, _encode(entry_to_record(entry)), reason))
            self._db.execute("COMMIT")
        except BaseException:
            self._db.execute("ROLLBACK")
            raise
        return cursor.lastrowid

    def _current_number(self, event_id: EventRecordId):
        row = self._db.execute(
            "SELECT entry_number FROM ledger_entries WHERE event_id = ? AND entry_number NOT IN "
            "(SELECT supersedes FROM ledger_entries WHERE supersedes IS NOT NULL)", (event_id.value,)).fetchone()
        return None if row is None else row[0]

    def _entry(self, number: int) -> LedgerEntry:
        (payload,) = self._db.execute("SELECT payload FROM ledger_entries WHERE entry_number = ?", (number,)).fetchone()
        return entry_from_record(json.loads(payload))

    def _current(self) -> dict:
        rows = self._db.execute(
            "SELECT event_id, payload FROM ledger_entries WHERE entry_number NOT IN "
            "(SELECT supersedes FROM ledger_entries WHERE supersedes IS NOT NULL) ORDER BY event_id")
        return {value: entry_from_record(json.loads(payload)) for value, payload in rows}

    def history(self, purpose: Purpose, event_id: EventRecordId, protocol: int | None = None) -> list:
        """Every entry this event has had, oldest first: (entry number, entry, supersedes, reason).

        A history read is a ledger read: it declares a purpose, sees only what that purpose may see, and is
        logged whether granted or refused. A protected event's history, superseded entries included, is
        never served for selection, tuning, rectification or development.
        """

        def serve(visible):
            (value,) = visible
            return [(number, entry_from_record(json.loads(payload)), supersedes, reason)
                    for number, payload, supersedes, reason in self._db.execute(
                        "SELECT entry_number, payload, supersedes, reason FROM ledger_entries "
                        "WHERE event_id = ? ORDER BY entry_number", (value,))]

        if event_id is None:
            event_id = _MISSING
        return self._gated(purpose, protocol, event_id, serve, "granted: history")

    # ------------------------------------------------------------ holdouts

    def freeze_and_select(self, criteria: str, members, size: int) -> int:
        """Freeze an eligible set and select its holdout, in one transaction. Returns the holdout number.

        The store draws the seed itself, so no caller chooses it, and the seed, the set and the selection
        are recorded together before anything can read them. An event belongs to at most one frozen set,
        ever, so the same events cannot be frozen again as an equivalent or overlapping set under another
        seed.
        """

        _text("criteria", criteria)
        members = tuple(members)
        if not members or not all(isinstance(member, EventRecordId) for member in members) or \
                len(set(members)) != len(members):
            raise LedgerError("an eligible set is a non-empty collection of distinct EVR identifiers")
        _count("size", size)
        self._db.execute("BEGIN IMMEDIATE")
        try:
            current = self._current()
            for member in members:
                if member.value not in current or current[member.value].outcome is Outcome.REJECTED:
                    raise LedgerError(f"{member} is not a confirmed ledger entry, so it is not eligible")
            frozen = sorted(members)
            seed = secrets.token_hex(32)
            selected = ordered_selection(seed, frozen, size)
            holdout = Holdout(criteria=criteria, members=tuple(frozen), content_hash=content_hash(frozen), seed=seed,
                              procedure=PROCEDURE, size=size, selected=selected, selection_hash=selection_hash(selected))
            set_number = self._db.execute("INSERT INTO eligible_sets (content_hash, payload) VALUES (?, ?)",
                                          (holdout.content_hash, _encode({"criteria": criteria}))).lastrowid
            for member in frozen:
                self._db.execute("INSERT INTO eligible_members (event_id, set_number) VALUES (?, ?)",
                                 (member.value, set_number))
            (last_access,) = self._db.execute("SELECT COALESCE(MAX(access_number), 0) FROM access_log").fetchone()
            number = self._db.execute(
                "INSERT INTO holdouts (set_number, after_access, payload) VALUES (?, ?, ?)",
                (set_number, last_access, _encode(holdout_to_record(holdout)))).lastrowid
            for member in selected:
                self._db.execute("INSERT INTO protected_events (event_id, holdout_number) VALUES (?, ?)",
                                 (member.value, number))
            self._db.execute("COMMIT")
        except sqlite3.IntegrityError as exc:
            self._db.execute("ROLLBACK")
            raise LedgerError(f"an event in this set is already in a frozen set, or the set is: {exc}") from exc
        except BaseException:
            self._db.execute("ROLLBACK")
            raise
        return number

    def holdout(self, number: int) -> Holdout:
        row = self._db.execute("SELECT payload FROM holdouts WHERE holdout_number = ?", (number,)).fetchone()
        if row is None:
            raise LedgerError(f"no holdout {number}")
        return holdout_from_record(json.loads(row[0]))

    def reproduces(self, number: int) -> bool:
        """Re-derive the holdout from its own record: the set's hash, the selection and the protected rows."""

        holdout = self.holdout(number)
        protected = {value for (value,) in self._db.execute(
            "SELECT event_id FROM protected_events WHERE holdout_number = ?", (number,))}
        return (holdout.procedure == PROCEDURE and holdout.content_hash == content_hash(holdout.members)
                and ordered_selection(holdout.seed, holdout.members, holdout.size) == holdout.selected
                and holdout.selection_hash == selection_hash(holdout.selected)
                and protected == {member.value for member in holdout.selected})

    def protected(self) -> frozenset:
        return frozenset(EventRecordId(value) for (value,) in self._db.execute("SELECT event_id FROM protected_events"))

    # ------------------------------------------------------------ protocols

    def register_protocol(self, protocol: Protocol) -> int:
        """Pre-register a protocol against a locked holdout. Immutable once registered."""

        payload = _encode(protocol_to_record(protocol))
        protocol_from_record(json.loads(payload))
        self._db.execute("BEGIN IMMEDIATE")
        try:
            if self._db.execute("SELECT 1 FROM holdouts WHERE holdout_number = ?",
                                (protocol.holdout,)).fetchone() is None:
                raise LedgerError(f"a protocol names a locked holdout; there is no holdout {protocol.holdout}")
            (last_access,) = self._db.execute("SELECT COALESCE(MAX(access_number), 0) FROM access_log").fetchone()
            number = self._db.execute("INSERT INTO protocols (holdout_number, after_access, payload) VALUES (?, ?, ?)",
                                      (protocol.holdout, last_access, payload)).lastrowid
            self._db.execute("COMMIT")
        except BaseException:
            self._db.execute("ROLLBACK")
            raise
        return number

    def protocol(self, number: int) -> Protocol:
        row = self._db.execute("SELECT payload FROM protocols WHERE protocol_number = ?", (number,)).fetchone()
        if row is None:
            raise LedgerError(f"no protocol {number}")
        return protocol_from_record(json.loads(row[0]))

    # ------------------------------------------------------------ purpose-declared reads

    def _log(self, purpose, protocol, granted: bool, served, note: str) -> int:
        label = purpose.value if isinstance(purpose, Purpose) else UNDECLARED
        return self._db.execute(
            "INSERT INTO access_log (purpose, protocol_number, granted, served, note) VALUES (?, ?, ?, ?, ?)",
            (label, protocol if _protocol_number(protocol) else None, 1 if granted else 0, json.dumps(sorted(served)),
             note)).lastrowid

    def _decide(self, purpose, protocol, event_id) -> dict:
        """Check the request's shape, then return what `purpose` may see. Raises LedgerError on any refusal."""

        if not isinstance(purpose, Purpose):
            raise LedgerError("every ledger read declares a Purpose")
        if protocol is not None and not _protocol_number(protocol):
            raise LedgerError(f"a protocol is named by a positive protocol number; refused {protocol!r:.60}")
        if event_id is _MISSING:
            raise LedgerError("a history read names one event")
        if event_id is not None and not isinstance(event_id, EventRecordId):
            raise LedgerError(f"an event is named by its EventRecordId; refused {event_id!r:.60}")
        visible = self._visible(purpose, protocol)
        if event_id is not None:
            if event_id.value not in visible:
                raise LedgerError(f"{event_id} is not available for a {purpose.value} read")
            visible = {event_id.value: visible[event_id.value]}
        return visible

    def _gated(self, purpose, protocol, event_id, serve, note: str):
        """Decide, log and serve one access attempt in one transaction.

        Every attempt is logged. A refusal is logged as refused; any other failure while deciding or serving
        is logged as a refused malformed request and raised as a LedgerError, so no attempt escapes the log.
        """

        self._db.execute("BEGIN IMMEDIATE")
        try:
            try:
                visible = self._decide(purpose, protocol, event_id)
                result = serve(visible)
            except Exception as exc:
                refusal = exc if isinstance(exc, LedgerError) else LedgerError(
                    f"malformed request refused: {type(exc).__name__}: {exc}")
                requested = [event_id.value] if isinstance(event_id, EventRecordId) else []
                self._log(purpose, protocol, False, requested, str(refusal)[:200])
                self._db.execute("COMMIT")
                if refusal is exc:
                    raise
                raise refusal from exc
            self._log(purpose, protocol, True, visible, note)
            self._db.execute("COMMIT")
        except LedgerError:
            raise
        except BaseException:
            self._db.execute("ROLLBACK")
            raise
        return result

    def _visible(self, purpose: Purpose, protocol) -> dict:
        """The current entries `purpose` may see, or a refusal. Called inside the read's transaction."""

        current = self._current()
        protected = {value for (value,) in self._db.execute("SELECT event_id FROM protected_events")}
        if purpose in EXCLUDED_FROM_PROTECTED:
            if protocol is not None:
                raise LedgerError(f"a {purpose.value} read names no protocol")
            return {value: entry for value, entry in current.items() if value not in protected}
        if purpose is Purpose.AUDIT:
            if protocol is not None:
                raise LedgerError("an audit read names no protocol")
            return current
        if protocol is None:
            raise LedgerError("protected validation needs a registered protocol")
        row = self._db.execute("SELECT holdout_number, payload FROM protocols WHERE protocol_number = ?",
                               (protocol,)).fetchone()
        if row is None:
            raise LedgerError(f"no protocol {protocol} is registered")
        holdout_number, payload = row
        minimum = protocol_from_record(json.loads(payload)).minimum_n
        selected = {value for (value,) in self._db.execute(
            "SELECT event_id FROM protected_events WHERE holdout_number = ?", (holdout_number,))}
        if len(selected) < minimum:
            raise LedgerError(f"holdout {holdout_number} holds {len(selected)} entries; the protocol's minimum N is "
                              f"{minimum}")
        return {value: entry for value, entry in current.items() if value in selected}

    def read(self, purpose: Purpose, protocol: int | None = None, event_id: EventRecordId | None = None) -> list:
        """The current entries `purpose` may see, or one of them. Logged whether granted or refused."""

        return self._gated(purpose, protocol, event_id, lambda visible: [visible[value] for value in sorted(visible)],
                           "granted")

    def counts(self, purpose: Purpose, protocol: int | None = None) -> dict:
        """Counts by event class, elicitation and outcome, each with its members (Q8 s6: decomposability).

        A count is the length of its member tuple. Nothing is divided, weighted or compared.
        """

        entries = self.read(purpose, protocol)
        partitions = {"event_class": {}, "elicitation": {}, "outcome": {}}
        for entry in entries:
            for axis, key in (("event_class", entry.event_class), ("elicitation", entry.elicitation.value),
                              ("outcome", entry.outcome.value)):
                partitions[axis].setdefault(key, []).append(entry.event)
        return {"total": tuple(entry.event for entry in entries),
                **{axis: {key: tuple(members) for key, members in sorted(groups.items())}
                   for axis, groups in partitions.items()}}

    def access_log(self) -> list:
        """Every logged read: (number, purpose, protocol, granted, served identifiers, note).

        A read made with no declared purpose is logged, refused, as UNDECLARED.
        """

        return [(number, UNDECLARED if purpose == UNDECLARED else Purpose(purpose), protocol, bool(granted),
                 tuple(json.loads(served)), note)
                for number, purpose, protocol, granted, served, note in self._db.execute(
                    "SELECT access_number, purpose, protocol_number, granted, served, note FROM access_log "
                    "ORDER BY access_number")]


def leakage_findings(path: Path | str) -> list:
    """Read-only audit of a ledger database's access log (H2 s8: holdout-leakage detection).

    Flags: a protected entry served to an excluded purpose after its holdout was locked; a protected-
    validation read with no protocol, before its protocol's registration, or serving entries outside
    that protocol's holdout. It inspects ledger reads only: reads outside the ledger are not logged,
    so they cannot be detected here.
    """

    db = sqlite3.connect(f"file:{Path(path).as_posix()}?mode=ro", uri=True)
    try:
        locked = {value: (holdout, after) for value, holdout, after in db.execute(
            "SELECT p.event_id, p.holdout_number, h.after_access FROM protected_events AS p "
            "JOIN holdouts AS h ON p.holdout_number = h.holdout_number")}
        protocols = {number: (holdout, after) for number, holdout, after in db.execute(
            "SELECT protocol_number, holdout_number, after_access FROM protocols")}
        log = db.execute("SELECT access_number, purpose, protocol_number, granted, served FROM access_log "
                         "ORDER BY access_number").fetchall()
    finally:
        db.close()
    excluded = {purpose.value for purpose in EXCLUDED_FROM_PROTECTED}
    findings = []
    for number, purpose, protocol, granted, served in log:
        if purpose == UNDECLARED and granted:
            findings.append(f"L4 access {number}: a read with no declared purpose was granted")
        if not granted:
            continue
        served = json.loads(served)
        if purpose in excluded:
            for value in served:
                if value in locked and locked[value][1] < number:
                    findings.append(f"L1 access {number}: protected {value} served for {purpose}")
        elif purpose == Purpose.PROTECTED_VALIDATION.value:
            if protocol not in protocols:
                findings.append(f"L2 access {number}: protected validation with no registered protocol")
                continue
            holdout, after = protocols[protocol]
            if after >= number:
                findings.append(f"L2 access {number}: protected validation before protocol {protocol} was registered")
            for value in served:
                if value not in locked or locked[value][0] != holdout:
                    findings.append(f"L3 access {number}: {value} is outside protocol {protocol}'s holdout")
    return findings
