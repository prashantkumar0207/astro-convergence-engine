"""The append-only evidence store, its rule-version references, and the EVD and RUL issuers (ADR-0119).

The store shares one SQLite database with the entity, event and ledger stores, and keeps its own
tables and its own two counters, one per family. A number is taken in the same transaction that
writes the record, so a refused write takes none. Triggers refuse every UPDATE and DELETE.

- Persistence (ADR-0113 s2 E1): an item is immutable. A recomputation is a new item that names the
  one it recomputes; the original stays.
- Joins (AC11): items are joined only when every field of their calculation Provenance agrees.
- Aggregates (AC13): every count returns its members; producing system and domain survive.
- Relationships (AC12): classified only from the items' own recorded inputs, derivation links and
  completeness statements. INDEPENDENT needs positive recorded evidence; anything missing, incomplete
  or unverified is UNKNOWN. CORRELATED is never assigned here. This follows recorded links; it is not
  a convergence algorithm and builds no graph.

Nothing here scores, weights, fits or divides, and nothing writes to calculation state.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from engine.evidence.entity import DataClass, RecordProvenance
from engine.evidence.evidence import (
    CONFIDENCE_COMPONENTS, CalculatedInput, ChartContext, ChartReference, Confidence, DependencyClass, Domain,
    EvidenceItem, EvidenceModelError, Lineage, Performance, Polarity, ProducingSystem, Relationship, RuleReference,
    RuleSpec, RuleVersion, Supplied, TimingContext, TimingKind, provenance_differences,
)
from engine.evidence.evidence_identifiers import EVD_FAMILY, EVD_LAST, RUL_FAMILY, RUL_LAST, EvidenceId, RuleId
from engine.evidence.identifiers import EntityId
from engine.evidence.store import EntityStore, StoreError
from engine.models.provenance import Provenance

SCHEMA_VERSION = "ace-evidence-store-v1"

_APPEND_ONLY = ("rule_versions", "evidence_items", "evidence_relationships")
_SCHEMA = """
CREATE TABLE IF NOT EXISTS evidence_issuers (family TEXT PRIMARY KEY, last_number INTEGER NOT NULL CHECK (last_number >= 0));
CREATE TABLE IF NOT EXISTS rule_versions (
    rule_id TEXT NOT NULL CHECK (rule_id GLOB 'RUL-[0-9][0-9][0-9][0-9][0-9][0-9]'),
    version INTEGER NOT NULL CHECK (version >= 1),
    payload TEXT NOT NULL,
    PRIMARY KEY (rule_id, version)
);
CREATE TABLE IF NOT EXISTS evidence_items (
    evidence_id TEXT PRIMARY KEY CHECK (evidence_id GLOB 'EVD-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    entity_id TEXT NOT NULL,
    recomputes TEXT REFERENCES evidence_items (evidence_id),
    payload TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS evidence_relationships (
    relationship_number INTEGER PRIMARY KEY AUTOINCREMENT,
    first_id TEXT NOT NULL REFERENCES evidence_items (evidence_id),
    second_id TEXT NOT NULL REFERENCES evidence_items (evidence_id),
    payload TEXT NOT NULL
);
CREATE TRIGGER IF NOT EXISTS evidence_issuers_never_decrease BEFORE UPDATE ON evidence_issuers
    WHEN NEW.last_number < OLD.last_number
    BEGIN SELECT RAISE(ABORT, 'an evidence issuer never reuses a number'); END;
CREATE TRIGGER IF NOT EXISTS evidence_issuers_no_delete BEFORE DELETE ON evidence_issuers
    BEGIN SELECT RAISE(ABORT, 'an evidence issuer cannot be removed'); END;
""" + "".join(
    f"CREATE TRIGGER IF NOT EXISTS {table}_no_update BEFORE UPDATE ON {table} "
    f"BEGIN SELECT RAISE(ABORT, '{table} is append-only'); END;\n"
    f"CREATE TRIGGER IF NOT EXISTS {table}_no_delete BEFORE DELETE ON {table} "
    f"BEGIN SELECT RAISE(ABORT, '{table} is append-only'); END;\n"
    for table in _APPEND_ONLY)

#: The fields of each record, at every level. The store refuses any other key (AC16).
ITEM_FIELDS = ("entity", "domain", "question", "producing_system", "rule", "declared_strength", "measured_reliability",
               "lineage", "chart", "chart_context", "timing", "polarity", "confidence", "historical_performance",
               "derived_from", "recomputes", "provenance", "data_class")
RULE_FIELDS = ("rule", "version", "school", "content_hash", "knowledge_snapshot_hash", "declared_strength",
               "synthetic_reference", "provenance", "data_class")
PROVENANCE_FIELDS = tuple(field for field in Provenance.__dataclass_fields__)
RELATIONSHIP_FIELDS = ("first", "second", "dependency", "conflicting", "basis")


def _exact(name: str, data, expected) -> dict:
    if not isinstance(data, dict) or set(data) != set(expected):
        extra = sorted(set(data) - set(expected)) if isinstance(data, dict) else data
        raise StoreError(f"{name} carries only its model fields; refused: {extra}")
    return data


def _record_provenance(provenance: RecordProvenance) -> dict:
    return {"source": provenance.source, "method": provenance.method, "schema_version": provenance.schema_version}


def _record_provenance_from(data) -> RecordProvenance:
    data = _exact("provenance", data, ("source", "method", "schema_version"))
    return RecordProvenance(source=data["source"], method=data["method"], schema_version=data["schema_version"])


def _calculation(provenance: Provenance) -> dict:
    return {name: provenance.__getattribute__(name) for name in PROVENANCE_FIELDS}


def _calculation_from(data) -> Provenance:
    return Provenance(**_exact("calculation provenance", data, PROVENANCE_FIELDS))


def _supplied(value: Supplied | None):
    return None if value is None else {"value": value.value, "provenance": _record_provenance(value.provenance)}


def _supplied_from(data) -> Supplied | None:
    if data is None:
        return None
    data = _exact("a supplied value", data, ("value", "provenance"))
    return Supplied(value=data["value"], provenance=_record_provenance_from(data["provenance"]))


def rule_to_record(rule: RuleVersion) -> dict:
    if not isinstance(rule, RuleVersion):
        raise StoreError("only a RuleVersion can be stored as a rule version")
    spec = rule.spec
    return {"schema": SCHEMA_VERSION, "rule_version": {
        "rule": rule.rule.value, "version": rule.version, "school": spec.school.value,
        "content_hash": spec.content_hash, "knowledge_snapshot_hash": spec.knowledge_snapshot_hash,
        "declared_strength": spec.declared_strength, "synthetic_reference": spec.synthetic_reference,
        "provenance": _record_provenance(spec.provenance), "data_class": spec.data_class.value}}


def rule_from_record(record: dict) -> RuleVersion:
    if not isinstance(record, dict) or set(record) != {"schema", "rule_version"} or record["schema"] != SCHEMA_VERSION:
        raise StoreError("not a rule-version record of this schema")
    data = _exact("a rule version", record["rule_version"], RULE_FIELDS)
    spec = RuleSpec(school=ProducingSystem(data["school"]), content_hash=data["content_hash"],
                    knowledge_snapshot_hash=data["knowledge_snapshot_hash"],
                    declared_strength=data["declared_strength"], provenance=_record_provenance_from(data["provenance"]),
                    data_class=DataClass(data["data_class"]), synthetic_reference=data["synthetic_reference"])
    return RuleVersion(rule=RuleId(data["rule"]), version=data["version"], spec=spec)


def item_to_record(evidence_id: EvidenceId, item: EvidenceItem) -> dict:
    """The stored form of an evidence item, with its EVD identity and schema version, written field by field."""

    if not isinstance(evidence_id, EvidenceId) or not isinstance(item, EvidenceItem):
        raise StoreError("an evidence record is an EVD identifier and an EvidenceItem")
    lineage, context, timing, performance = item.lineage, item.chart_context, item.timing, item.historical_performance
    return {"schema": SCHEMA_VERSION, "id": evidence_id.value, "evidence": {
        "entity": item.entity.value,
        "domain": item.domain.value,
        "question": None,
        "producing_system": item.producing_system.value,
        "rule": {"rule": item.rule.rule.value, "version": item.rule.version},
        "declared_strength": item.declared_strength,
        "measured_reliability": None,
        "lineage": {"inputs": [{"fact": entry.fact, "provenance": _calculation(entry.provenance)}
                               for entry in lineage.inputs],
                    "inputs_complete": lineage.inputs_complete,
                    "derivations_complete": lineage.derivations_complete},
        "chart": {"entity_revision": item.chart.entity_revision, "chart_label": item.chart.chart_label},
        "chart_context": {"varga": context.varga, "planets": list(context.planets), "houses": list(context.houses),
                          "signs": list(context.signs), "significators": list(context.significators)},
        "timing": {"kind": timing.kind.value, "label": timing.label, "start": timing.start, "end": timing.end},
        "polarity": item.polarity.value,
        "confidence": {name: _supplied(item.confidence.__getattribute__(name)) for name in CONFIDENCE_COMPONENTS},
        "historical_performance": None if performance is None else {
            "value": performance.value, "sample_size": performance.sample_size,
            "provenance": _record_provenance(performance.provenance)},
        "derived_from": [link.value for link in item.derived_from],
        "recomputes": None if item.recomputes is None else item.recomputes.value,
        "provenance": _record_provenance(item.provenance),
        "data_class": item.data_class.value,
    }}


def item_from_record(record: dict) -> tuple:
    """Rebuild (EvidenceId, EvidenceItem), refusing any key the model does not define, at any level."""

    if not isinstance(record, dict) or set(record) != {"schema", "id", "evidence"} or \
            record["schema"] != SCHEMA_VERSION:
        raise StoreError("not an evidence record of this schema: it needs its schema version and EVD identity")
    data = _exact("an evidence item", record["evidence"], ITEM_FIELDS)
    lineage = _exact("lineage", data["lineage"], ("inputs", "inputs_complete", "derivations_complete"))
    inputs = tuple(CalculatedInput(fact=_exact("a calculated input", entry, ("fact", "provenance"))["fact"],
                                   provenance=_calculation_from(entry["provenance"])) for entry in lineage["inputs"])
    chart = _exact("chart", data["chart"], ("entity_revision", "chart_label"))
    context = _exact("chart context", data["chart_context"], ("varga", "planets", "houses", "signs", "significators"))
    timing = _exact("timing", data["timing"], ("kind", "label", "start", "end"))
    rule = _exact("rule reference", data["rule"], ("rule", "version"))
    confidence = _exact("confidence", data["confidence"], CONFIDENCE_COMPONENTS)
    performance = data["historical_performance"]
    if performance is not None:
        performance = _exact("historical performance", performance, ("value", "sample_size", "provenance"))
        performance = Performance(value=performance["value"], sample_size=performance["sample_size"],
                                  provenance=_record_provenance_from(performance["provenance"]))
    item = EvidenceItem(
        entity=EntityId(data["entity"]), domain=Domain(data["domain"]), question=data["question"],
        producing_system=ProducingSystem(data["producing_system"]),
        rule=RuleReference(rule=RuleId(rule["rule"]), version=rule["version"]),
        declared_strength=data["declared_strength"], measured_reliability=data["measured_reliability"],
        lineage=Lineage(inputs=inputs, inputs_complete=lineage["inputs_complete"],
                        derivations_complete=lineage["derivations_complete"]),
        chart=ChartReference(entity_revision=chart["entity_revision"], chart_label=chart["chart_label"]),
        chart_context=ChartContext(varga=context["varga"], planets=tuple(context["planets"]),
                                   houses=tuple(context["houses"]), signs=tuple(context["signs"]),
                                   significators=tuple(context["significators"])),
        timing=TimingContext(kind=TimingKind(timing["kind"]), label=timing["label"], start=timing["start"],
                             end=timing["end"]),
        polarity=Polarity(data["polarity"]),
        confidence=Confidence(**{name: _supplied_from(confidence[name]) for name in CONFIDENCE_COMPONENTS}),
        historical_performance=performance,
        derived_from=tuple(EvidenceId(link) for link in data["derived_from"]),
        recomputes=None if data["recomputes"] is None else EvidenceId(data["recomputes"]),
        provenance=_record_provenance_from(data["provenance"]), data_class=DataClass(data["data_class"]))
    return EvidenceId(record["id"]), item


def relationship_to_record(relationship: Relationship) -> dict:
    return {"schema": SCHEMA_VERSION, "relationship": {
        "first": relationship.first.value, "second": relationship.second.value,
        "dependency": relationship.dependency.value, "conflicting": relationship.conflicting,
        "basis": relationship.basis}}


def relationship_from_record(record: dict) -> Relationship:
    if not isinstance(record, dict) or set(record) != {"schema", "relationship"} or \
            record["schema"] != SCHEMA_VERSION:
        raise StoreError("not a relationship record of this schema")
    data = _exact("a relationship", record["relationship"], RELATIONSHIP_FIELDS)
    return Relationship(first=EvidenceId(data["first"]), second=EvidenceId(data["second"]),
                        dependency=DependencyClass(data["dependency"]), conflicting=data["conflicting"],
                        basis=data["basis"])


def _encode(record: dict) -> str:
    return json.dumps(record, sort_keys=True, separators=(",", ":"))


def _conflicting(first: EvidenceItem, second: EvidenceItem) -> bool:
    """Opposite polarity about the same entity, domain and an overlapping timing window."""

    opposite = {first.polarity, second.polarity} == {Polarity.POSITIVE, Polarity.NEGATIVE}
    overlap = first.timing.start <= second.timing.end and second.timing.start <= first.timing.end
    return opposite and overlap and first.entity == second.entity and first.domain == second.domain


class EvidenceStore:
    """An append-only evidence store over the entity database at `path`, with its own EVD and RUL issuers."""

    def __init__(self, path: Path | str):
        self.path = Path(path)
        self.entities = EntityStore(self.path)
        self._db = sqlite3.connect(str(self.path), isolation_level=None, timeout=10.0)
        self._db.executescript(_SCHEMA)
        for family in (EVD_FAMILY, RUL_FAMILY):
            self._db.execute("INSERT OR IGNORE INTO evidence_issuers (family, last_number) VALUES (?, 0)", (family,))

    def close(self) -> None:
        self._db.close()
        self.entities.close()

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        self.close()

    def _issue(self, family: str, last_allowed: int) -> int:
        (last,) = self._db.execute("SELECT last_number FROM evidence_issuers WHERE family = ?", (family,)).fetchone()
        if last >= last_allowed:
            raise StoreError(f"the {family} family is exhausted")
        self._db.execute("UPDATE evidence_issuers SET last_number = ? WHERE family = ?", (last + 1, family))
        return last + 1

    def _transaction(self, work):
        self._db.execute("BEGIN IMMEDIATE")
        try:
            result = work()
            self._db.execute("COMMIT")
        except BaseException:
            self._db.execute("ROLLBACK")
            raise
        return result

    # ------------------------------------------------------------ rule-version references (synthetic)

    def register_rule(self, spec: RuleSpec) -> RuleVersion:
        """Issue a RUL number and record version 1. A synthetic structural reference only (ADR-0119 AC3)."""

        if not isinstance(spec, RuleSpec):
            raise StoreError("a rule version is registered from a RuleSpec")

        def work():
            rule = RuleVersion(rule=RuleId.from_number(self._issue(RUL_FAMILY, RUL_LAST)), version=1, spec=spec)
            self._insert_rule(rule)
            return rule
        return self._transaction(work)

    def register_rule_version(self, rule: RuleId, spec: RuleSpec) -> RuleVersion:
        """Record the next version of an existing rule. Earlier versions stay; the school never changes."""

        if not isinstance(spec, RuleSpec):
            raise StoreError("a rule version is registered from a RuleSpec")

        def work():
            versions = self.rule_versions(rule)
            if spec.school is not versions[-1].spec.school:
                raise StoreError("a rule's school is never changed by a new version")
            new = RuleVersion(rule=rule, version=versions[-1].version + 1, spec=spec)
            self._insert_rule(new)
            return new
        return self._transaction(work)

    def _insert_rule(self, rule: RuleVersion) -> None:
        payload = _encode(rule_to_record(rule))
        rule_from_record(json.loads(payload))
        self._db.execute("INSERT INTO rule_versions (rule_id, version, payload) VALUES (?, ?, ?)",
                         (rule.rule.value, rule.version, payload))

    def rule_versions(self, rule: RuleId) -> list:
        if not isinstance(rule, RuleId):
            raise StoreError("rules are addressed by their RUL identifier")
        rows = self._db.execute("SELECT payload FROM rule_versions WHERE rule_id = ? ORDER BY version",
                                (rule.value,)).fetchall()
        if not rows:
            raise StoreError(f"no such rule: {rule}")
        return [rule_from_record(json.loads(payload)) for (payload,) in rows]

    def rule_version(self, reference: RuleReference) -> RuleVersion:
        if not isinstance(reference, RuleReference):
            raise StoreError("a rule version is addressed by a RuleReference")
        row = self._db.execute("SELECT payload FROM rule_versions WHERE rule_id = ? AND version = ?",
                               (reference.rule.value, reference.version)).fetchone()
        if row is None:
            raise StoreError(f"{reference.rule} version {reference.version} is not registered; evidence names only "
                             f"a registered rule version (H4 s4)")
        return rule_from_record(json.loads(row[0]))

    # ------------------------------------------------------------ evidence items

    def persist(self, item: EvidenceItem) -> EvidenceId:
        """Write a new item and issue its EVD number, in one transaction."""

        if not isinstance(item, EvidenceItem):
            raise StoreError("only an EvidenceItem can be stored as evidence")

        def work():
            self._check(item)
            evidence_id = EvidenceId.from_number(self._issue(EVD_FAMILY, EVD_LAST))
            payload = _encode(item_to_record(evidence_id, item))
            item_from_record(json.loads(payload))
            self._db.execute("INSERT INTO evidence_items (evidence_id, entity_id, recomputes, payload) "
                             "VALUES (?, ?, ?, ?)", (evidence_id.value, item.entity.value,
                                                     None if item.recomputes is None else item.recomputes.value,
                                                     payload))
            return evidence_id
        return self._transaction(work)

    def _check(self, item: EvidenceItem) -> None:
        rule = self.rule_version(item.rule)
        if item.producing_system is not rule.spec.school:
            raise StoreError(f"a {item.producing_system.value} item cannot name a {rule.spec.school.value} rule; "
                             f"systems stay isolated")
        if item.declared_strength != rule.spec.declared_strength:
            raise StoreError("declared strength is the rule version's, recorded as declared (ADR-0113 s2 E2)")
        if item.entity not in self.entities.entity_ids():
            raise StoreError(f"entity {item.entity} is not in this store")
        history = self.entities.history(item.entity)
        if item.chart.entity_revision > len(history):
            raise StoreError(f"{item.entity} has no revision {item.chart.entity_revision}")
        _number, subject, _reason = history[item.chart.entity_revision - 1]
        if item.chart.chart_label not in {chart.label for chart in subject.charts}:
            raise StoreError(f"{item.chart.chart_label!r} is not a chart of {item.entity} at revision "
                             f"{item.chart.entity_revision}")
        for link in item.derived_from:
            self.load(link)
        if item.recomputes is not None:
            original = self.load(item.recomputes)
            if (original.entity, original.rule.rule, original.producing_system) != \
                    (item.entity, item.rule.rule, item.producing_system):
                raise StoreError("a recomputation keeps the entity, rule and system of the item it recomputes")
            if item.recomputes in item.derived_from:
                raise StoreError("a recomputation names its original once, as recomputes")

    def load(self, evidence_id: EvidenceId) -> EvidenceItem:
        if not isinstance(evidence_id, EvidenceId):
            raise StoreError("evidence is addressed by its EVD identifier")
        row = self._db.execute("SELECT payload FROM evidence_items WHERE evidence_id = ?",
                               (evidence_id.value,)).fetchone()
        if row is None:
            raise StoreError(f"no such evidence item: {evidence_id}")
        return item_from_record(json.loads(row[0]))[1]

    def evidence_ids(self) -> list:
        return [EvidenceId(value) for (value,) in self._db.execute(
            "SELECT evidence_id FROM evidence_items ORDER BY evidence_id")]

    def recomputations(self, evidence_id: EvidenceId) -> list:
        """The items that recompute this one, oldest first. The original is never replaced."""

        self.load(evidence_id)
        return [EvidenceId(value) for (value,) in self._db.execute(
            "SELECT evidence_id FROM evidence_items WHERE recomputes = ? ORDER BY evidence_id", (evidence_id.value,))]

    def issued_count(self, family: str) -> int:
        row = self._db.execute("SELECT last_number FROM evidence_issuers WHERE family = ?", (family,)).fetchone()
        if row is None:
            raise StoreError(f"this store issues {EVD_FAMILY} and {RUL_FAMILY} only")
        return row[0]

    # ------------------------------------------------------------ joins and decomposable aggregates

    def join(self, evidence_ids) -> list:
        """The items, only if every field of their calculation provenance agrees (ADR-0119 AC11)."""

        ids = tuple(evidence_ids)
        if not ids or len(set(ids)) != len(ids):
            raise StoreError("a join takes one or more distinct EVD identifiers")
        items = [self.load(evidence_id) for evidence_id in ids]
        differing = provenance_differences(*(entry.provenance for item in items for entry in item.lineage.inputs))
        if differing:
            raise StoreError(f"these items' calculation provenance differs in {', '.join(differing)}; they are not "
                             f"joined (H4 s3)")
        return items

    def counts(self, evidence_ids=None) -> dict:
        """Counts by producing system, domain, polarity and rule, each with its members (AC13). Nothing divides."""

        ids = tuple(self.evidence_ids() if evidence_ids is None else evidence_ids)
        items = self.join(ids)
        partitions = {"producing_system": {}, "domain": {}, "polarity": {}, "rule": {}}
        for evidence_id, item in zip(ids, items):
            for axis, key in (("producing_system", item.producing_system.value), ("domain", item.domain.value),
                              ("polarity", item.polarity.value),
                              ("rule", f"{item.rule.rule.value} v{item.rule.version}")):
                partitions[axis].setdefault(key, []).append(evidence_id)
        return {"total": ids,
                "members": {evidence_id: (item.producing_system.value, item.domain.value)
                            for evidence_id, item in zip(ids, items)},
                **{axis: {key: tuple(members) for key, members in sorted(groups.items())}
                   for axis, groups in partitions.items()}}

    # ------------------------------------------------------------ structural relationships

    def _ancestry(self, evidence_id: EvidenceId) -> tuple:
        """Every item reachable through recorded derivation and recomputation links, and whether every item on
        those paths states its derivation links complete."""

        seen, verified, pending = set(), True, [evidence_id]
        while pending:
            current = self.load(pending.pop())
            verified = verified and current.lineage.derivations_complete
            for link in current.derived_from + (() if current.recomputes is None else (current.recomputes,)):
                if link not in seen:
                    seen.add(link)
                    pending.append(link)
        return seen, verified

    def classify(self, first: EvidenceId, second: EvidenceId) -> Relationship:
        """The structural relationship, from recorded links, inputs and completeness statements (ADR-0119 AC12)."""

        a, b = self.load(first), self.load(second)
        conflicting = _conflicting(a, b)
        ancestors_a, verified_a = self._ancestry(first)
        ancestors_b, verified_b = self._ancestry(second)
        if second in ancestors_a or first in ancestors_b:
            return Relationship(first, second, DependencyClass.DERIVED, conflicting, "a recorded derivation link")
        shared = sorted({(entry.fact, entry.provenance) for entry in a.lineage.inputs} &
                        {(entry.fact, entry.provenance) for entry in b.lineage.inputs}, key=lambda pair: pair[0])
        if shared:
            return Relationship(first, second, DependencyClass.SHARED_ORIGIN, conflicting,
                                "recorded shared input: " + ", ".join(fact for fact, _provenance in shared))
        if ancestors_a & ancestors_b:
            return Relationship(first, second, DependencyClass.SHARED_ORIGIN, conflicting,
                                "a shared recorded ancestor: " + ", ".join(sorted(link.value for link in
                                                                                 ancestors_a & ancestors_b)))
        for missing, reason in ((not (a.lineage.derivations_complete and b.lineage.derivations_complete),
                                 "a derivation link may be missing: not every derivation list is stated complete"),
                                (not (a.lineage.inputs_complete and b.lineage.inputs_complete),
                                 "incomplete lineage: not every input list is stated complete"),
                                (not (verified_a and verified_b),
                                 "an unverified derivation path: an ancestor's derivation list is not stated complete"),
                                (a.producing_system is b.producing_system,
                                 "the same producing system; independence needs different systems")):
            if missing:
                return Relationship(first, second, DependencyClass.UNKNOWN, conflicting, reason)
        return Relationship(first, second, DependencyClass.INDEPENDENT, conflicting,
                            "different systems, complete recorded lineage with disjoint inputs, and no recorded "
                            "derivation path")

    def relate(self, first: EvidenceId, second: EvidenceId) -> Relationship:
        """Classify and record. Each call appends a record, so a later classification never rewrites an earlier."""

        def work():
            relationship = self.classify(first, second)
            payload = _encode(relationship_to_record(relationship))
            relationship_from_record(json.loads(payload))
            self._db.execute("INSERT INTO evidence_relationships (first_id, second_id, payload) VALUES (?, ?, ?)",
                             (first.value, second.value, payload))
            return relationship
        return self._transaction(work)

    def relationships(self) -> list:
        return [relationship_from_record(json.loads(payload)) for (payload,) in self._db.execute(
            "SELECT payload FROM evidence_relationships ORDER BY relationship_number")]

    def relationship_counts(self) -> dict:
        """Recorded relationships by dependency class, each with its pairs. UNKNOWN is its own class."""

        groups = {kind.value: [] for kind in DependencyClass}
        conflicts = []
        for relationship in self.relationships():
            groups[relationship.dependency.value].append((relationship.first, relationship.second))
            if relationship.conflicting:
                conflicts.append((relationship.first, relationship.second))
        return {**{kind: tuple(pairs) for kind, pairs in groups.items()}, "conflicting": tuple(conflicts)}


__all__ = ["SCHEMA_VERSION", "EvidenceStore", "EvidenceModelError", "item_to_record", "item_from_record",
           "rule_to_record", "rule_from_record", "relationship_to_record", "relationship_from_record"]
