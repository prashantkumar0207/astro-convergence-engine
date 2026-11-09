"""The append-only entity store, and the ENT issuer (ADR-0111 s2 item 3; ADR-0114 s3).

The store is one SQLite database. Its counter is the durable, central ENT issuer: a number is
taken in the same transaction that writes the entity, so a failed persistence takes none. Each
store instance is its own issuer, which is how fixtures stay isolated from any other store.

Records are never updated or deleted. Triggers refuse both at the database layer, so even direct
SQL cannot rewrite history. A correction appends a new revision, with its reason.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from engine.evidence.entity import (
    SUBJECT_FIELDS, SUBJECT_TYPES, AstrologicalSubject, ChartCandidate, DataClass, EntityKind, EntityLink,
    OriginCertainty, OriginMoment, ParentLink, RecordProvenance, Shape,
)
from engine.evidence.identifiers import FAMILY, LAST, EntityId

SCHEMA_VERSION = "ace-entity-store-v1"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS issuer (family TEXT PRIMARY KEY, last_number INTEGER NOT NULL CHECK (last_number >= 0));
CREATE TABLE IF NOT EXISTS entity_revisions (
    entity_id TEXT NOT NULL CHECK (entity_id GLOB 'ENT-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    revision INTEGER NOT NULL CHECK (revision >= 1),
    payload TEXT NOT NULL,
    reason TEXT NOT NULL,
    PRIMARY KEY (entity_id, revision)
);
CREATE TABLE IF NOT EXISTS entity_links (
    link_number INTEGER PRIMARY KEY AUTOINCREMENT,
    payload TEXT NOT NULL
);
CREATE TRIGGER IF NOT EXISTS revisions_no_update BEFORE UPDATE ON entity_revisions
    BEGIN SELECT RAISE(ABORT, 'entity revisions are append-only'); END;
CREATE TRIGGER IF NOT EXISTS revisions_no_delete BEFORE DELETE ON entity_revisions
    BEGIN SELECT RAISE(ABORT, 'entity revisions are append-only'); END;
CREATE TRIGGER IF NOT EXISTS links_no_update BEFORE UPDATE ON entity_links
    BEGIN SELECT RAISE(ABORT, 'entity links are append-only'); END;
CREATE TRIGGER IF NOT EXISTS links_no_delete BEFORE DELETE ON entity_links
    BEGIN SELECT RAISE(ABORT, 'entity links are append-only'); END;
CREATE TRIGGER IF NOT EXISTS issuer_never_decreases BEFORE UPDATE ON issuer
    WHEN NEW.last_number < OLD.last_number
    BEGIN SELECT RAISE(ABORT, 'the ENT issuer never reuses a number'); END;
CREATE TRIGGER IF NOT EXISTS issuer_no_delete BEFORE DELETE ON issuer
    BEGIN SELECT RAISE(ABORT, 'the ENT issuer cannot be removed'); END;
"""


class StoreError(RuntimeError):
    """The store refused an operation."""


def _provenance_record(provenance: RecordProvenance) -> dict:
    return {"source": provenance.source, "method": provenance.method, "schema_version": provenance.schema_version}


def _chart_record(chart: ChartCandidate) -> dict:
    origin = chart.origin
    return {
        "label": chart.label,
        "origin": {"local_datetime": origin.local_datetime, "timezone": origin.timezone,
                   "timezone_source": origin.timezone_source, "latitude": origin.latitude,
                   "longitude": origin.longitude, "precision": origin.precision},
        "origin_certainty": chart.origin_certainty.value,
        "provenance": _provenance_record(chart.provenance),
    }


def subject_to_record(subject: AstrologicalSubject) -> dict:
    """The stored form of a subject, written field by field so the schema is explicit."""

    if not isinstance(subject, AstrologicalSubject):
        raise StoreError("only an AstrologicalSubject can be stored")
    parent = subject.parent
    return {"schema": SCHEMA_VERSION, "subject": {
        "kind": subject.kind.value,
        "shape": subject.shape.value,
        "charts": [_chart_record(chart) for chart in subject.charts],
        "applicable_domains": list(subject.applicable_domains),
        "applicable_systems": list(subject.applicable_systems),
        "provenance": _provenance_record(subject.provenance),
        "data_class": subject.data_class.value,
        "parent": None if parent is None else {"parent": parent.parent.value, "parent_chart": parent.parent_chart,
                                               "derivation": parent.derivation},
    }}


def _link_record(link: EntityLink) -> dict:
    return {"source": link.source.value, "relation": link.relation, "target": link.target.value,
            "provenance": _provenance_record(link.provenance)}


def _provenance(data) -> RecordProvenance:
    return RecordProvenance(**data)


def subject_from_record(record: dict) -> AstrologicalSubject:
    """Rebuild a subject, refusing any key the model does not define (H0 s5)."""

    if set(record) != {"schema", "subject"} or record["schema"] != SCHEMA_VERSION:
        raise StoreError("not an entity record of this schema")
    data = record["subject"]
    if not isinstance(data, dict) or set(data) != set(SUBJECT_FIELDS):
        extra = sorted(set(data) - set(SUBJECT_FIELDS)) if isinstance(data, dict) else data
        raise StoreError(f"an entity carries only its model fields; refused: {extra}")
    charts = tuple(
        ChartCandidate(label=chart["label"], origin=OriginMoment(**chart["origin"]),
                       origin_certainty=OriginCertainty(chart["origin_certainty"]),
                       provenance=_provenance(chart["provenance"]))
        for chart in data["charts"])
    parent = data["parent"]
    kind = EntityKind(data["kind"])
    return SUBJECT_TYPES[kind](
        kind=kind, shape=Shape(data["shape"]), charts=charts,
        applicable_domains=tuple(data["applicable_domains"]), applicable_systems=tuple(data["applicable_systems"]),
        provenance=_provenance(data["provenance"]), data_class=DataClass(data["data_class"]),
        parent=None if parent is None else ParentLink(parent=EntityId(parent["parent"]),
                                                      parent_chart=parent["parent_chart"],
                                                      derivation=parent["derivation"]))


def _encode(record: dict) -> str:
    return json.dumps(record, sort_keys=True, separators=(",", ":"))


class EntityStore:
    """An append-only entity store, and that store's own ENT issuer."""

    def __init__(self, path: Path | str):
        self.path = Path(path)
        self._db = sqlite3.connect(str(self.path), isolation_level=None, timeout=10.0)
        self._db.executescript(_SCHEMA)
        self._db.execute("INSERT OR IGNORE INTO issuer (family, last_number) VALUES (?, 0)", (FAMILY,))

    def close(self) -> None:
        self._db.close()

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        self.close()

    def persist(self, subject: AstrologicalSubject, reason: str = "first record") -> EntityId:
        """Write a new entity and issue its ENT number, in one transaction."""

        payload = _encode(subject_to_record(subject))
        subject_from_record(json.loads(payload))  # Refuse anything that would not reload.
        self._db.execute("BEGIN IMMEDIATE")
        try:
            (last,) = self._db.execute("SELECT last_number FROM issuer WHERE family = ?", (FAMILY,)).fetchone()
            if last >= LAST:
                raise StoreError("the ENT family is exhausted")
            entity_id = EntityId.from_number(last + 1)
            self._check_parent(subject, entity_id)
            self._db.execute("INSERT INTO entity_revisions (entity_id, revision, payload, reason) VALUES (?, 1, ?, ?)",
                             (entity_id.value, payload, reason))
            self._db.execute("UPDATE issuer SET last_number = ? WHERE family = ?", (last + 1, FAMILY))
            self._db.execute("COMMIT")
        except BaseException:
            self._db.execute("ROLLBACK")
            raise
        return entity_id

    def append_revision(self, entity_id: EntityId, subject: AstrologicalSubject, reason: str) -> int:
        """Record a correction as a new revision. The superseded revision stays."""

        if not reason or not reason.strip():
            raise StoreError("a correction records its reason")
        payload = _encode(subject_to_record(subject))
        subject_from_record(json.loads(payload))
        self._db.execute("BEGIN IMMEDIATE")
        try:
            row = self._db.execute("SELECT MAX(revision) FROM entity_revisions WHERE entity_id = ?",
                                   (entity_id.value,)).fetchone()
            if row[0] is None:
                raise StoreError(f"no such entity: {entity_id}")
            current = subject_from_record(json.loads(self._db.execute(
                "SELECT payload FROM entity_revisions WHERE entity_id = ? AND revision = ?",
                (entity_id.value, row[0])).fetchone()[0]))
            if current.kind is not subject.kind:
                raise StoreError("a correction cannot change an entity's kind")
            self._check_parent(subject, entity_id)
            self._check_dependents(entity_id, subject)
            self._db.execute("INSERT INTO entity_revisions (entity_id, revision, payload, reason) VALUES (?, ?, ?, ?)",
                             (entity_id.value, row[0] + 1, payload, reason))
            self._db.execute("COMMIT")
        except BaseException:
            self._db.execute("ROLLBACK")
            raise
        return row[0] + 1

    def _latest(self) -> dict:
        """The current revision of every entity, read inside the caller's transaction."""

        rows = self._db.execute(
            "SELECT r.entity_id, r.payload FROM entity_revisions AS r JOIN (SELECT entity_id, MAX(revision) AS top "
            "FROM entity_revisions GROUP BY entity_id) AS m ON r.entity_id = m.entity_id AND r.revision = m.top")
        return {value: subject_from_record(json.loads(payload)) for value, payload in rows}

    def _check_parent(self, subject: AstrologicalSubject, own_id: EntityId) -> None:
        """A derived subject's parent and parent chart must exist in this store, and derivation must not cycle."""

        link = subject.parent
        if link is None:
            return
        if link.parent == own_id:
            raise StoreError(f"{own_id} cannot derive from itself")
        current = self._latest()
        if link.parent.value not in current:
            raise StoreError(f"parent entity {link.parent} is not in this store")
        parent = current[link.parent.value]
        if link.parent_chart not in {chart.label for chart in parent.charts}:
            raise StoreError(f"parent chart {link.parent_chart!r} is not a chart of {link.parent}")
        seen, ancestor = {own_id.value}, parent
        while ancestor.parent is not None:
            if ancestor.parent.parent.value in seen:
                raise StoreError(f"{own_id} would derive from itself through {ancestor.parent.parent}")
            seen.add(ancestor.parent.parent.value)
            ancestor = current[ancestor.parent.parent.value]

    def _check_dependents(self, entity_id: EntityId, subject: AstrologicalSubject) -> None:
        """A correction must not remove a chart that another entity's parent link names."""

        labels = {chart.label for chart in subject.charts}
        for value, other in self._latest().items():
            link = other.parent
            if link is not None and link.parent == entity_id and link.parent_chart not in labels:
                raise StoreError(f"{value} derives from chart {link.parent_chart!r} of {entity_id}; "
                                 f"this correction would remove it")

    def history(self, entity_id: EntityId) -> list:
        rows = self._db.execute(
            "SELECT revision, payload, reason FROM entity_revisions WHERE entity_id = ? ORDER BY revision",
            (entity_id.value,)).fetchall()
        if not rows:
            raise StoreError(f"no such entity: {entity_id}")
        return [(revision, subject_from_record(json.loads(payload)), reason) for revision, payload, reason in rows]

    def load(self, entity_id: EntityId) -> AstrologicalSubject:
        return self.history(entity_id)[-1][1]

    def entity_ids(self) -> list:
        return [EntityId(value) for (value,) in self._db.execute(
            "SELECT DISTINCT entity_id FROM entity_revisions ORDER BY entity_id")]

    def add_link(self, link: EntityLink) -> None:
        if not isinstance(link, EntityLink):
            raise StoreError("only an EntityLink can be stored as a relationship")
        known = {entity.value for entity in self.entity_ids()}
        if link.source.value not in known or link.target.value not in known:
            raise StoreError("a link joins two entities already in this store")
        self._db.execute("INSERT INTO entity_links (payload) VALUES (?)", (_encode(_link_record(link)),))

    def links(self) -> list:
        out = []
        for (payload,) in self._db.execute("SELECT payload FROM entity_links ORDER BY link_number"):
            data = json.loads(payload)
            out.append(EntityLink(source=EntityId(data["source"]), relation=data["relation"],
                                  target=EntityId(data["target"]), provenance=_provenance(data["provenance"])))
        return out

    def issued_count(self) -> int:
        return self._db.execute("SELECT last_number FROM issuer WHERE family = ?", (FAMILY,)).fetchone()[0]
