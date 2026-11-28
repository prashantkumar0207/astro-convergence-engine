"""The append-only evidence store, its registered rule versions, its provenance graph, and the EVD issuer (ADR-0119;
ADR-0121; ADR-0122).

The store shares one SQLite database with the entity, event and ledger stores, and keeps its own
tables and its own EVD counter. An EVD number is taken in the same transaction that writes the item,
so a refused write takes none. Triggers refuse every UPDATE and DELETE.

- Rule identity (ADR-0121): the store issues no RUL number. The governed registry authoring process
  is the only RUL issuer, and the store records a rule version only if it matches, exactly, a rule
  the pinned registry publishes: RUL identifier, version, school, explicit variant, content hash and
  snapshot hash. Evidence names only such a registered version, from the pinned snapshot in force, and only if
  the recorded row is, field for field, the rule the pinned registry publishes under that identity.

- Persistence (ADR-0113 s2 E1): an item is immutable. A recomputation is a new item that names the
  one it recomputes; the original stays.
- Joins (AC11): items are joined only when every field of their calculation Provenance agrees.
- Aggregates (AC13): every count returns its members; producing system and domain survive.
- Relationships (AC12): classified only from the items' recorded inputs, derivation links and
  completeness statements, their ancestors' included. INDEPENDENT needs positive recorded evidence;
  anything missing, incomplete or unverified, in an item or any ancestor, is UNKNOWN. Items whose
  calculation provenance differs are never related, and a persisted relationship joining them is
  refused when read (AC11). CORRELATED is never assigned here. This follows recorded links; it is not
  a convergence algorithm and builds no graph. A persisted relationship is returned only if classifying the same
  immutable items gives exactly its dependency, conflict flag and basis, however the row was written (ADR-0125).

- Provenance graph (ADR-0122, WP-E6): persisting an item writes the nodes and edges it consumed, in the same
  transaction as the item and its EVD number, from the item and the records already checked for it
  (engine/evidence/provenance_graph.py). A node is stored once, under the hash of what it is, so a node two items
  share is recorded as shared. No API adds a node or edge afterwards, and every read refuses a node whose key is not
  its hash, a dangling or undeclared edge, a cycle, and any row the items' stored records do not account for, however
  the rows were written. A read returns only recorded rows: the comparison never fills in a missing one.
- Read integrity (ADR-0124): every read of an evidence item, however the row was written, refuses a row that disagrees
  with its own key, names a rule version that is not registered or does not fit the item, or has no accounted-for
  graph. A rule version recorded under an earlier snapshot stays readable: only new evidence needs the snapshot in force.
  It must still be what the governed records prove (ADR-0127): its RUL issued by the allocation history, under that
  school, and the version published, unchanged, because a published version is never withdrawn or rewritten.

- Untimed natal evidence (ADR-0134; H4 s13): an item whose timing is `UntimedNatal` is stored under its own record schema,
  v4; dated items, rule versions and relationships keep v3, unchanged. A store accepts untimed items only when it is
  constructed with the natal verifier, which re-derives each one from its entity chart's recorded birth input through the
  certified kernel. This module cannot run the kernel itself (AC14), so the verifier is handed in; a store without it
  refuses every untimed item, on write and on every read, so no direct call bypasses the check. A dated and an untimed
  item never conflict by timing; two untimed items conflict only as opposite-polarity variants of one rule version on one
  chart; and an untimed item is never independent of another item about the same entity (D6-c).

Nothing here scores, weights, fits or divides, and nothing writes to calculation state.
"""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

from engine.evidence.entity import ChartCandidate, DataClass, ParentLink, RecordProvenance
from engine.evidence.evidence import (
    CONFIDENCE_COMPONENTS, CalculatedInput, ChartContext, ChartReference, Confidence, DependencyClass, Domain,
    EvidenceItem, EvidenceModelError, Lineage, Performance, Polarity, ProducingSystem, Relationship, RuleReference,
    RuleSpec, RuleVersion, Supplied, TimingContext, TimingKind, UntimedBasis, UntimedNatal, provenance_differences,
)
from engine.evidence.evidence_identifiers import EVD_FAMILY, EVD_LAST, EvidenceId, RuleId
import engine.evidence.provenance_graph as provenance_graph
import engine.evidence.rule_registry as rule_registry
from engine.evidence.identifiers import EntityId
from engine.evidence.store import EntityStore, StoreError
from engine.models.provenance import Provenance

#: v2 (ADR-0121): rule versions carry an explicit variant and are recorded, never issued; evidence names a variant.
#: v3 (ADR-0122 D4): the provenance graph's node and edge tables. No v1 or v2 store exists outside temporary test
#: databases; an earlier database's records carry their own schema version and are refused when read.
SCHEMA_VERSION = "ace-evidence-store-v3"
#: v4 (ADR-0134 D6-b): an untimed natal item's record. Every other record, dated items included, stays v3.
UNTIMED_SCHEMA_VERSION = "ace-evidence-store-v4"
UNTIMED_KIND = "untimed_natal"
#: The only condition kinds an untimed item's rule may have: each is a natal placement (ADR-0134 U2).
NATAL_PLACEMENT_KINDS = ("house_lord_in_house", "planet_in_house", "planet_in_sign")
#: The one natal verifier a store may hold: the governed `verify_natal_item` of engine/projection/natal.py (ADR-0134 U6).
#: It is found by identity in the already-loaded module, never imported here: this module may not import the kernel (AC14).
GOVERNED_NATAL_VERIFIER = ("engine.projection.natal", "verify_natal_item")


def require_governed_verifier(verifier) -> None:
    """Refuse any natal verifier but the governed one, by identity: a permissive callback, a wrapper or a copy is refused
    (ADR-0134 U6; CEO HOLD on PR #70)."""

    module_name, function_name = GOVERNED_NATAL_VERIFIER
    module = sys.modules[module_name] if module_name in sys.modules else None
    governed = module.__dict__[function_name] if module is not None and function_name in module.__dict__ else None
    if governed is None or verifier is not governed:
        raise StoreError(f"a store's natal verifier is only the governed {module_name}.{function_name}; any other "
                         f"callback is refused (ADR-0134 U6)")

_APPEND_ONLY = ("registered_rule_versions", "evidence_items", "evidence_relationships", "graph_nodes",
                "graph_edges")
_SCHEMA = """
CREATE TABLE IF NOT EXISTS evidence_issuers (family TEXT PRIMARY KEY, last_number INTEGER NOT NULL CHECK (last_number >= 0));
CREATE TABLE IF NOT EXISTS registered_rule_versions (
    rule_id TEXT NOT NULL CHECK (rule_id GLOB 'RUL-[0-9][0-9][0-9][0-9][0-9][0-9]'),
    version INTEGER NOT NULL CHECK (version >= 1),
    variant TEXT NOT NULL,
    payload TEXT NOT NULL,
    PRIMARY KEY (rule_id, version, variant)
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
CREATE TABLE IF NOT EXISTS graph_nodes (
    node_key TEXT PRIMARY KEY CHECK (length(node_key) = 64),
    kind TEXT NOT NULL,
    payload TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS graph_edges (
    edge_number INTEGER PRIMARY KEY AUTOINCREMENT,
    source_key TEXT NOT NULL REFERENCES graph_nodes (node_key),
    kind TEXT NOT NULL,
    target_key TEXT NOT NULL REFERENCES graph_nodes (node_key),
    position INTEGER NOT NULL CHECK (position >= 0),
    UNIQUE (source_key, kind, target_key)
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
RULE_FIELDS = ("rule", "version", "school", "content_hash", "knowledge_snapshot_hash", "declared_strength", "variant",
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
        "declared_strength": spec.declared_strength, "variant": spec.variant,
        "synthetic_reference": spec.synthetic_reference,
        "provenance": _record_provenance(spec.provenance), "data_class": spec.data_class.value}}


def rule_from_record(record: dict) -> RuleVersion:
    if not isinstance(record, dict) or set(record) != {"schema", "rule_version"} or record["schema"] != SCHEMA_VERSION:
        raise StoreError("not a rule-version record of this schema")
    data = _exact("a rule version", record["rule_version"], RULE_FIELDS)
    spec = RuleSpec(school=ProducingSystem(data["school"]), content_hash=data["content_hash"],
                    knowledge_snapshot_hash=data["knowledge_snapshot_hash"],
                    declared_strength=data["declared_strength"], variant=data["variant"],
                    provenance=_record_provenance_from(data["provenance"]),
                    data_class=DataClass(data["data_class"]), synthetic_reference=data["synthetic_reference"])
    return RuleVersion(rule=RuleId(data["rule"]), version=data["version"], spec=spec)


def item_to_record(evidence_id: EvidenceId, item: EvidenceItem) -> dict:
    """The stored form of an evidence item, with its EVD identity and schema version, written field by field."""

    if not isinstance(evidence_id, EvidenceId) or not isinstance(item, EvidenceItem):
        raise StoreError("an evidence record is an EVD identifier and an EvidenceItem")
    lineage, context, timing, performance = item.lineage, item.chart_context, item.timing, item.historical_performance
    untimed = type(timing) is UntimedNatal
    return {"schema": UNTIMED_SCHEMA_VERSION if untimed else SCHEMA_VERSION, "id": evidence_id.value, "evidence": {
        "entity": item.entity.value,
        "domain": item.domain.value,
        "question": None,
        "producing_system": item.producing_system.value,
        "rule": {"rule": item.rule.rule.value, "version": item.rule.version, "variant": item.rule.variant},
        "declared_strength": item.declared_strength,
        "measured_reliability": None,
        "lineage": {"inputs": [{"fact": entry.fact, "provenance": _calculation(entry.provenance)}
                               for entry in lineage.inputs],
                    "inputs_complete": lineage.inputs_complete,
                    "derivations_complete": lineage.derivations_complete},
        "chart": {"entity_revision": item.chart.entity_revision, "chart_label": item.chart.chart_label},
        "chart_context": {"varga": context.varga, "planets": list(context.planets), "houses": list(context.houses),
                          "signs": list(context.signs), "significators": list(context.significators)},
        "timing": {"kind": UNTIMED_KIND, "basis": timing.basis.value} if untimed else
                  {"kind": timing.kind.value, "label": timing.label, "start": timing.start, "end": timing.end},
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


def untimed_timing_from(data) -> dict:
    """A v4 record's timing: exactly the untimed kind and its basis (ADR-0134 D6-b, U3)."""

    timing = _exact("untimed timing (v4)", data, ("kind", "basis"))
    if timing["kind"] != UNTIMED_KIND:
        raise StoreError(f"a v4 record's timing is {UNTIMED_KIND!r}; a dated timing is a v3 record (ADR-0134 D6-b)")
    return timing


def item_from_record(record: dict) -> tuple:
    """Rebuild (EvidenceId, EvidenceItem), refusing any key the model does not define, at any level."""

    if not isinstance(record, dict) or set(record) != {"schema", "id", "evidence"} or \
            record["schema"] not in (SCHEMA_VERSION, UNTIMED_SCHEMA_VERSION):
        raise StoreError("not an evidence record of this schema: it needs its schema version and EVD identity")
    data = _exact("an evidence item", record["evidence"], ITEM_FIELDS)
    untimed = record["schema"] == UNTIMED_SCHEMA_VERSION
    lineage = _exact("lineage", data["lineage"], ("inputs", "inputs_complete", "derivations_complete"))
    inputs = tuple(CalculatedInput(fact=_exact("a calculated input", entry, ("fact", "provenance"))["fact"],
                                   provenance=_calculation_from(entry["provenance"])) for entry in lineage["inputs"])
    chart = _exact("chart", data["chart"], ("entity_revision", "chart_label"))
    context = _exact("chart context", data["chart_context"], ("varga", "planets", "houses", "signs", "significators"))
    if untimed:
        timing = untimed_timing_from(data["timing"])
    else:
        timing = _exact("timing", data["timing"], ("kind", "label", "start", "end"))
    rule = _exact("rule reference", data["rule"], ("rule", "version", "variant"))
    confidence = _exact("confidence", data["confidence"], CONFIDENCE_COMPONENTS)
    performance = data["historical_performance"]
    if performance is not None:
        performance = _exact("historical performance", performance, ("value", "sample_size", "provenance"))
        performance = Performance(value=performance["value"], sample_size=performance["sample_size"],
                                  provenance=_record_provenance_from(performance["provenance"]))
    item = EvidenceItem(
        entity=EntityId(data["entity"]), domain=Domain(data["domain"]), question=data["question"],
        producing_system=ProducingSystem(data["producing_system"]),
        rule=RuleReference(rule=RuleId(rule["rule"]), version=rule["version"], variant=rule["variant"]),
        declared_strength=data["declared_strength"], measured_reliability=data["measured_reliability"],
        lineage=Lineage(inputs=inputs, inputs_complete=lineage["inputs_complete"],
                        derivations_complete=lineage["derivations_complete"]),
        chart=ChartReference(entity_revision=chart["entity_revision"], chart_label=chart["chart_label"]),
        chart_context=ChartContext(varga=context["varga"], planets=tuple(context["planets"]),
                                   houses=tuple(context["houses"]), signs=tuple(context["signs"]),
                                   significators=tuple(context["significators"])),
        timing=UntimedNatal(basis=UntimedBasis(timing["basis"])) if untimed else
        TimingContext(kind=TimingKind(timing["kind"]), label=timing["label"], start=timing["start"], end=timing["end"]),
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


def _untimed(item: EvidenceItem) -> bool:
    return type(item.timing) is UntimedNatal


def untimed_conflict(first: EvidenceItem, second: EvidenceItem) -> bool:
    """D6-c, where either item is untimed: a conflict only between two untimed, opposite-polarity variants of one rule
    version on one chart of one entity and domain. A dated and an untimed item never conflict by timing."""

    opposite = {first.polarity, second.polarity} == {Polarity.POSITIVE, Polarity.NEGATIVE}
    return (opposite and _untimed(first) and _untimed(second) and first.entity == second.entity and
            first.domain == second.domain and first.chart == second.chart and
            (first.rule.rule, first.rule.version) == (second.rule.rule, second.rule.version))


def withholds_independence(first: EvidenceItem, second: EvidenceItem) -> bool:
    """D6-c: an untimed natal item is never independent of another item about the same entity, whose chart origin it
    shares."""

    return (_untimed(first) or _untimed(second)) and first.entity == second.entity


def _conflicting(first: EvidenceItem, second: EvidenceItem) -> bool:
    """Opposite polarity about the same entity, domain and an overlapping timing window. An untimed item has no window: it
    never conflicts with a dated item by timing, and two untimed items conflict only as variants of one rule version on
    one chart (ADR-0134 D6-c)."""

    if _untimed(first) or _untimed(second):
        return untimed_conflict(first, second)
    opposite = {first.polarity, second.polarity} == {Polarity.POSITIVE, Polarity.NEGATIVE}
    overlap = first.timing.start <= second.timing.end and second.timing.start <= first.timing.end
    return opposite and overlap and first.entity == second.entity and first.domain == second.domain


class EvidenceStore:
    """An append-only evidence store over the entity database at `path`, with its own EVD issuer. It issues no RUL."""

    def __init__(self, path: Path | str, natal_verifier=None):
        """`natal_verifier(item, candidate)` re-derives an untimed item from its chart through the certified kernel and
        raises if it differs (engine/projection/natal.py). Without it, every untimed item is refused (ADR-0134 U6)."""

        if natal_verifier is not None:
            require_governed_verifier(natal_verifier)
        self.path = Path(path)
        self._natal_verifier = natal_verifier
        self.entities = EntityStore(self.path)
        self._db = sqlite3.connect(str(self.path), isolation_level=None, timeout=10.0)
        self._db.executescript(_SCHEMA)
        self._db.execute("INSERT OR IGNORE INTO evidence_issuers (family, last_number) VALUES (?, 0)", (EVD_FAMILY,))

    def close(self) -> None:
        self._db.close()
        self.entities.close()

    @property
    def natal_verifier(self):
        """The verifier this store checks untimed items with, or None: then it refuses every untimed item."""

        return self._natal_verifier

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

    # ------------------------------------------------------------ registered rule versions (ADR-0121)

    def register_rule(self, claimed: RuleVersion) -> RuleVersion:
        """Record a rule version the pinned registry publishes. Every field must match the published rule exactly:
        RUL identifier, version, school, explicit variant, content hash, snapshot hash, declared strength and the
        synthetic marking. The store issues nothing, and a version is recorded once."""

        if not isinstance(claimed, RuleVersion):
            raise StoreError("a rule version is registered from the registry's RuleVersion")
        try:
            published = rule_registry.pinned().rule_version(claimed.rule, claimed.version, claimed.spec.variant)
        except rule_registry.RegistryError as exc:
            raise StoreError(f"{exc}; the store records only rules the pinned registry publishes (ADR-0121)") from exc
        for name, mine, theirs in (("school", claimed.spec.school, published.spec.school),
                                   ("content hash", claimed.spec.content_hash, published.spec.content_hash),
                                   ("snapshot hash", claimed.spec.knowledge_snapshot_hash,
                                    published.spec.knowledge_snapshot_hash),
                                   ("declared strength", claimed.spec.declared_strength,
                                    published.spec.declared_strength),
                                   ("synthetic marking", claimed.spec.synthetic_reference,
                                    published.spec.synthetic_reference)):
            if mine != theirs:
                raise StoreError(f"{claimed.rule} v{claimed.version} {claimed.spec.variant!r}: the {name} differs "
                                 f"from the pinned registry's; the store records only the published rule")

        def work():
            payload = _encode(rule_to_record(published))
            rule_from_record(json.loads(payload))
            try:
                self._db.execute("INSERT INTO registered_rule_versions (rule_id, version, variant, payload) "
                                 "VALUES (?, ?, ?, ?)", (published.rule.value, published.version,
                                                         published.spec.variant, payload))
            except sqlite3.IntegrityError as exc:
                raise StoreError(f"{published.rule} v{published.version} {published.spec.variant!r} is already "
                                 f"registered; a rule version is recorded once") from exc
            return published
        return self._transaction(work)

    def rule_versions(self, rule: RuleId) -> list:
        if not isinstance(rule, RuleId):
            raise StoreError("rules are addressed by their RUL identifier")
        rows = self._db.execute("SELECT payload FROM registered_rule_versions WHERE rule_id = ? "
                                "ORDER BY version, variant", (rule.value,)).fetchall()
        if not rows:
            raise StoreError(f"no such rule: {rule}")
        return [rule_from_record(json.loads(payload)) for (payload,) in rows]

    def rule_version(self, reference: RuleReference) -> RuleVersion:
        if not isinstance(reference, RuleReference):
            raise StoreError("a rule version is addressed by a RuleReference")
        row = self._db.execute("SELECT payload FROM registered_rule_versions WHERE rule_id = ? AND version = ? "
                               "AND variant = ?", (reference.rule.value, reference.version,
                                                   reference.variant)).fetchone()
        if row is None:
            raise StoreError(f"{reference.rule} version {reference.version} variant {reference.variant!r} is not "
                             f"registered; evidence names only a registered rule version (H4 s4)")
        return rule_from_record(json.loads(row[0]))

    # ------------------------------------------------------------ evidence items

    def persist(self, item: EvidenceItem) -> EvidenceId:
        """Write a new item, issue its EVD number and record its provenance graph, in one transaction: if any part
        fails, nothing is written and no number is taken (ADR-0122 AC1)."""

        if not isinstance(item, EvidenceItem):
            raise StoreError("only an EvidenceItem can be stored as evidence")

        def work():
            rule, candidate, parent = self._check(item)
            evidence_id = EvidenceId.from_number(self._issue(EVD_FAMILY, EVD_LAST))
            payload = _encode(item_to_record(evidence_id, item))
            item_from_record(json.loads(payload))
            self._db.execute("INSERT INTO evidence_items (evidence_id, entity_id, recomputes, payload) "
                             "VALUES (?, ?, ?, ?)", (evidence_id.value, item.entity.value,
                                                     None if item.recomputes is None else item.recomputes.value,
                                                     payload))
            links = item.derived_from + (() if item.recomputes is None else (item.recomputes,))
            try:
                graph = provenance_graph.record_graph(evidence_id, item, candidate, parent, rule,
                                                      {link: self.load(link) for link in links})
            except provenance_graph.GraphError as exc:
                raise StoreError(f"the provenance graph cannot be recorded: {exc}") from exc
            self._write_graph(graph)
            return evidence_id
        return self._transaction(work)

    def _write_graph(self, graph: provenance_graph.Graph) -> None:
        """Record a new item's nodes and edges. Called only by persist(), inside its transaction (ADR-0122 AC1). A
        node already recorded must be the same node; a shared edge must be the same edge; an edge that would close
        a cycle is refused (AC4)."""

        for node in graph.nodes:
            key, kind, payload = provenance_graph.node_to_row(node)
            row = self._db.execute("SELECT kind, payload FROM graph_nodes WHERE node_key = ?", (key,)).fetchone()
            if row is None:
                self._db.execute("INSERT INTO graph_nodes (node_key, kind, payload) VALUES (?, ?, ?)",
                                 (key, kind, payload))
            elif self._node_from(key, row) != node:
                raise StoreError(f"node {key} is recorded with another identity")
        for edge in graph.edges:
            row = self._db.execute("SELECT position FROM graph_edges WHERE source_key = ? AND kind = ? AND "
                                   "target_key = ?", (edge.source.key, edge.kind.value, edge.target.key)).fetchone()
            if row is not None:
                if row[0] != edge.position:
                    raise StoreError("an edge is recorded with another position")
                continue
            if self._reaches(edge.target.key, edge.source.key):
                raise StoreError(f"an edge {edge.source.key} -> {edge.target.key} would close a cycle (ADR-0122 AC4)")
            self._db.execute("INSERT INTO graph_edges (source_key, kind, target_key, position) VALUES (?, ?, ?, ?)",
                             (edge.source.key, edge.kind.value, edge.target.key, edge.position))

    def _reaches(self, start: str, goal: str) -> bool:
        """Whether recorded edges lead from start to goal. A traversal; nothing is counted."""

        seen, pending = {start}, [start]
        while pending:
            current = pending.pop()
            if current == goal:
                return True
            for (successor,) in self._db.execute("SELECT target_key FROM graph_edges WHERE source_key = ?",
                                                 (current,)).fetchall():
                if successor not in seen:
                    seen.add(successor)
                    pending.append(successor)
        return False

    @staticmethod
    def _require_published(item: EvidenceItem, rule: RuleVersion, registry: rule_registry.RuleRegistry) -> None:
        """A recorded row is trusted only as far as the pinned registry publishes it, exactly, under the identity the
        evidence names: a matching snapshot hash alone does not admit a forged variant, an unissued RUL identity, a row
        whose payload names another identity than its key, or changed content (CEO HOLD on PR #56, item 1)."""

        try:
            published = registry.rule_version(item.rule.rule, item.rule.version, item.rule.variant)
        except rule_registry.RegistryError as exc:
            raise StoreError(f"{exc}: the recorded rule version is not published by the pinned registry; evidence "
                             f"names only a published rule (ADR-0120 AC7, AC8; ADR-0121)") from exc
        if rule_to_record(rule) != rule_to_record(published):
            raise StoreError(f"{item.rule.rule} v{item.rule.version} {item.rule.variant!r}: the recorded rule version "
                             f"differs from the pinned registry's publication; evidence names only the published "
                             f"rule (ADR-0120 AC7, AC8; ADR-0121)")

    @staticmethod
    def _require_fit(item: EvidenceItem, rule: RuleVersion) -> None:
        if item.producing_system is not rule.spec.school:
            raise StoreError(f"a {item.producing_system.value} item cannot name a {rule.spec.school.value} rule; "
                             f"systems stay isolated")
        if item.declared_strength != rule.spec.declared_strength:
            raise StoreError("declared strength is the rule version's, recorded as declared (ADR-0113 s2 E2)")

    @staticmethod
    def _require_issued(rule: RuleVersion, issued: dict) -> None:
        """The allocation history issued this RUL number, bound to this school (ADR-0121)."""

        identity: RuleId = rule.rule
        if identity.number not in issued:
            raise StoreError(f"{identity} was never issued by the governed authoring process; a recorded rule version "
                             f"names only an issued RUL (H4 s4; ADR-0121; ADR-0127)")
        _key, school = issued[identity.number]
        if school is not rule.spec.school:
            raise StoreError(f"{identity} is bound to {school.value} by the allocation history; a recorded "
                             f"{rule.spec.school.value} version contradicts it (ADR-0121; ADR-0127)")

    @staticmethod
    def _require_unchanged_publication(rule: RuleVersion, registry: rule_registry.RuleRegistry) -> None:
        """A published version is never withdrawn or rewritten (ADR-0120 AC2; the registry gate's G3), so a genuine
        historical version is still published, with everything but its snapshot hash unchanged."""

        identity: RuleId = rule.rule
        try:
            published = registry.rule_version(identity, rule.version, rule.spec.variant)
        except rule_registry.RegistryError as exc:
            raise StoreError(f"{exc}: a published version is never withdrawn, so this recorded version was never "
                             f"published (ADR-0120 AC2; ADR-0127)") from exc
        mine, theirs = rule_to_record(rule)["rule_version"], rule_to_record(published)["rule_version"]
        if {**mine, "knowledge_snapshot_hash": None} != {**theirs, "knowledge_snapshot_hash": None}:
            raise StoreError(f"{identity} v{rule.version} {rule.spec.variant!r}: the recorded version contradicts its "
                             f"immutable publication (ADR-0120 AC2; ADR-0127)")

    def _admitted_rule(self, item: EvidenceItem) -> RuleVersion:
        """The registered rule version a stored item names, refused unless it fits the item (H4 s4; ADR-0124). A row
        claiming the snapshot in force must be exactly what that snapshot publishes. A row recorded under an earlier
        snapshot is legitimate history, and stays readable, but only as what the governed records prove: an issued
        RUL, under its school, and a version still published unchanged (ADR-0127)."""

        rule = self.rule_version(item.rule)
        registry = rule_registry.pinned()
        if rule.spec.knowledge_snapshot_hash == registry.snapshot_sha256:
            self._require_published(item, rule, registry)
        else:
            self._require_issued(rule, rule_registry.read_history(rule_registry.DATA_DIR.joinpath(rule_registry.HISTORY_NAME)))
            self._require_unchanged_publication(rule, registry)
        self._require_fit(item, rule)
        return rule

    def _require_untimed(self, item: EvidenceItem, candidate: ChartCandidate) -> None:
        """An untimed item is admitted only by a store holding the natal verifier, only for a rule whose every condition
        is a natal placement, and only if the verifier re-derives it exactly (ADR-0134 U2, U6)."""

        if self._natal_verifier is None:
            raise StoreError("an untimed natal item is written and read only by a store holding the natal verifier "
                             "(ADR-0134 U6)")
        require_governed_verifier(self._natal_verifier)
        published = rule_registry.pinned().lookup(item.rule.rule, item.rule.version, item.rule.variant)
        kinds = [condition.kind for condition in (published.condition, *published.activation_conditions)]
        if any(kind not in NATAL_PLACEMENT_KINDS for kind in kinds):
            raise StoreError(f"an untimed item's rule has only natal placement conditions; {item.rule.rule} needs "
                             f"{kinds} (ADR-0134 U2)")
        try:
            self._natal_verifier(item, candidate)
        except (ValueError, KeyError, TypeError) as exc:
            raise StoreError(f"the untimed item is not its chart's certified natal evidence: {exc}") from exc

    def _candidate(self, item: EvidenceItem) -> ChartCandidate:
        history = self.entities.history(item.entity)
        if item.chart.entity_revision > len(history):
            raise StoreError(f"{item.entity} has no revision {item.chart.entity_revision}")
        _number, subject, _reason = history[item.chart.entity_revision - 1]
        candidates = [chart for chart in subject.charts if chart.label == item.chart.chart_label]
        if not candidates:
            raise StoreError(f"{item.chart.chart_label!r} is not a chart of {item.entity}")
        return candidates[0]

    def _check(self, item: EvidenceItem) -> tuple:
        """Every refusal before an item is written. Returns the records its graph is recorded from: the registered
        rule version, the chart it names at its entity revision, and that revision's parent link."""

        rule = self.rule_version(item.rule)
        registry = rule_registry.pinned()
        if rule.spec.knowledge_snapshot_hash != registry.snapshot_sha256:
            raise StoreError(f"{item.rule.rule} v{item.rule.version} was registered from another snapshot; new evidence "
                             f"names only rules of the pinned snapshot in force (ADR-0120 AC8)")
        self._require_published(item, rule, registry)
        self._require_fit(item, rule)
        if item.entity not in self.entities.entity_ids():
            raise StoreError(f"entity {item.entity} is not in this store")
        history = self.entities.history(item.entity)
        if item.chart.entity_revision > len(history):
            raise StoreError(f"{item.entity} has no revision {item.chart.entity_revision}")
        _number, subject, _reason = history[item.chart.entity_revision - 1]
        candidates = [chart for chart in subject.charts if chart.label == item.chart.chart_label]
        if not candidates:
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
        candidate: ChartCandidate = candidates[0]
        parent: ParentLink | None = subject.parent
        if _untimed(item):
            self._require_untimed(item, candidate)
        return rule, candidate, parent

    # ------------------------------------------------------------ the provenance graph (ADR-0122)

    @staticmethod
    def _node_from(key: str, row) -> provenance_graph.Node:
        try:
            return provenance_graph.node_from_row(key, row[0], row[1])
        except provenance_graph.GraphError as exc:
            raise StoreError(f"a recorded node is refused: {exc}") from exc

    def _stored_node(self, key: str) -> provenance_graph.Node:
        row = self._db.execute("SELECT kind, payload FROM graph_nodes WHERE node_key = ?", (key,)).fetchone()
        if row is None:
            raise StoreError(f"a dangling edge or a missing graph: node {key} is not recorded")
        return self._node_from(key, row)

    @staticmethod
    def _graph_of(nodes: dict, rows) -> provenance_graph.Graph:
        try:
            edges = [provenance_graph.edge_from_row(nodes, *row) for row in rows]
            return provenance_graph.Graph(nodes=tuple(nodes[key] for key in sorted(nodes)), edges=tuple(sorted(
                edges, key=lambda edge: (edge.target.key, edge.kind.value, edge.source.key))))
        except provenance_graph.GraphError as exc:
            raise StoreError(f"the recorded provenance graph is refused: {exc}") from exc

    @staticmethod
    def _unjustified(recorded: provenance_graph.Graph, expected) -> tuple:
        return provenance_graph.unjustified_rows(recorded, expected)

    def _justified_by(self, evidence_id: EvidenceId) -> provenance_graph.Graph:
        """What one item's stored records justify. Used only to check recorded rows, never returned by a read."""

        item = self._stored_item(evidence_id)
        rule = self._admitted_rule(item)
        history = self.entities.history(item.entity)
        if item.chart.entity_revision > len(history):
            raise StoreError(f"{item.entity} has no revision {item.chart.entity_revision}")
        _number, subject, _reason = history[item.chart.entity_revision - 1]
        candidates = [chart for chart in subject.charts if chart.label == item.chart.chart_label]
        if not candidates:
            raise StoreError(f"{item.chart.chart_label!r} is not a chart of {item.entity}")
        links = item.derived_from + (() if item.recomputes is None else (item.recomputes,))
        return provenance_graph.record_graph(evidence_id, item, candidates[0], subject.parent, rule,
                                             {link: self._stored_item(link) for link in links})

    def _checked_against_records(self, recorded: provenance_graph.Graph, evidence_ids) -> provenance_graph.Graph:
        """`recorded`, only if it is exactly what these items and their recorded ancestors justify (CEO HOLD on PR
        #59): a structurally valid row that no item's records account for is not provenance."""

        seen, pending, expected = set(evidence_ids), list(evidence_ids), []
        try:
            while pending:
                current = pending.pop()
                expected.append(self._justified_by(current))
                item = self._stored_item(current)
                for link in item.derived_from + (() if item.recomputes is None else (item.recomputes,)):
                    if link not in seen:
                        seen.add(link)
                        pending.append(link)
        except provenance_graph.GraphError as exc:
            raise StoreError(f"the recorded provenance graph is refused: {exc}") from exc
        differences = self._unjustified(recorded, expected)
        if differences:
            raise StoreError(f"the recorded provenance graph is refused: the items' records do not account for it "
                             f"({differences[0]}; {len(differences)} in all)")
        return recorded

    def graph(self, evidence_ids) -> provenance_graph.Graph:
        """The recorded graph the items consumed: their evidence nodes and everything recorded upstream of them,
        ancestors' included, refused unless the items' records account for every row. It returns its members; nothing
        is computed over it (ADR-0122 AC5, AC7, AC11)."""

        ids = tuple(evidence_ids)
        if not ids or len(set(ids)) != len(ids) or not all(isinstance(value, EvidenceId) for value in ids):
            raise StoreError("a graph read takes one or more distinct EVD identifiers")
        pending = [provenance_graph.evidence_node(evidence_id, self._stored_item(evidence_id)).key
                   for evidence_id in ids]
        nodes, rows = {}, []
        for key in pending:
            nodes[key] = self._stored_node(key)
        while pending:
            current = pending.pop()
            for row in self._db.execute("SELECT source_key, kind, target_key, position FROM graph_edges WHERE "
                                        "target_key = ? ORDER BY edge_number", (current,)).fetchall():
                rows.append(row)
                if row[0] not in nodes:
                    nodes[row[0]] = self._stored_node(row[0])
                    pending.append(row[0])
        return self._checked_against_records(self._graph_of(nodes, rows), ids)

    def item_graph(self, evidence_id: EvidenceId) -> provenance_graph.Graph:
        return self.graph((evidence_id,))

    def incident(self, node_key: str) -> tuple:
        """A node's recorded edges, as (incoming, outgoing), read from the whole recorded graph so that every row is
        accounted for."""

        self._stored_node(node_key)
        graph = self.recorded_graph()
        return (tuple(edge for edge in graph.edges if edge.target.key == node_key),
                tuple(edge for edge in graph.edges if edge.source.key == node_key))

    def recorded_graph(self) -> provenance_graph.Graph:
        """Every recorded node and edge, each validated as it is read and accounted for by the items' records."""

        nodes = {key: self._node_from(key, (kind, payload)) for key, kind, payload in
                 self._db.execute("SELECT node_key, kind, payload FROM graph_nodes ORDER BY node_key").fetchall()}
        rows = self._db.execute("SELECT source_key, kind, target_key, position FROM graph_edges "
                                "ORDER BY edge_number").fetchall()
        return self._checked_against_records(self._graph_of(nodes, rows), self._stored_ids())

    def reproduce(self, evidence_id: EvidenceId) -> dict:
        """What the item's recorded graph alone says of it (ADR-0122 AC7)."""

        try:
            return provenance_graph.reproduce(self.item_graph(evidence_id), evidence_id)
        except provenance_graph.GraphError as exc:
            raise StoreError(f"{evidence_id}'s recorded graph does not reproduce it: {exc}") from exc

    @staticmethod
    def _require_row_identity(evidence_id: EvidenceId, stored_id: EvidenceId, item: EvidenceItem, entity_id: str,
                              recomputes) -> None:
        """A stored row's key and indexed columns are the ones its own record states."""

        if stored_id != evidence_id or item.entity.value != entity_id or \
                (None if item.recomputes is None else item.recomputes.value) != recomputes:
            raise StoreError(f"the stored record of {evidence_id} does not match its row (ADR-0124)")

    def _stored_item(self, evidence_id: EvidenceId) -> EvidenceItem:
        """The item a row records, with its identity checked. Only the read checks use this directly."""

        if not isinstance(evidence_id, EvidenceId):
            raise StoreError("evidence is addressed by its EVD identifier")
        row = self._db.execute("SELECT entity_id, recomputes, payload FROM evidence_items WHERE evidence_id = ?",
                               (evidence_id.value,)).fetchone()
        if row is None:
            raise StoreError(f"no such evidence item: {evidence_id}")
        stored_id, item = item_from_record(json.loads(row[2]))
        self._require_row_identity(evidence_id, stored_id, item, row[0], row[1])
        if _untimed(item):
            self._require_untimed(item, self._candidate(item))
        return item

    def load(self, evidence_id: EvidenceId) -> EvidenceItem:
        """A stored item, only if its row is intact, it names a registered rule version that fits it, and its recorded
        graph is accounted for, ancestors' included, however the row was written (H4 s4; ADR-0122; ADR-0124)."""

        item = self._stored_item(evidence_id)
        self.graph((evidence_id,))
        return item

    def _stored_ids(self) -> list:
        return [EvidenceId(value) for (value,) in self._db.execute(
            "SELECT evidence_id FROM evidence_items ORDER BY evidence_id").fetchall()]

    def evidence_ids(self) -> list:
        """Every item's identifier. One row that fails the read checks refuses the listing: it is never hidden."""

        ids = self._stored_ids()
        if ids:
            self.graph(ids)
        return ids

    def recomputations(self, evidence_id: EvidenceId) -> list:
        """The items that recompute this one, oldest first. The original is never replaced."""

        self.load(evidence_id)
        found = [EvidenceId(value) for (value,) in self._db.execute(
            "SELECT evidence_id FROM evidence_items WHERE recomputes = ? ORDER BY evidence_id",
            (evidence_id.value,)).fetchall()]
        for link in found:
            self.load(link)
        return found

    def issued_count(self, family: str) -> int:
        if family != EVD_FAMILY:
            raise StoreError(f"this store issues {EVD_FAMILY} only; RUL is issued by the rule registry's authoring "
                             f"process (ADR-0121)")
        return self._db.execute("SELECT last_number FROM evidence_issuers WHERE family = ?", (family,)).fetchone()[0]

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
        """What an item's recorded links reach: (ancestors, every calculated input of the item and its ancestors,
        whether every ancestor states its derivation list complete, whether every ancestor states its input list
        complete). It follows recorded derivation and recomputation links only."""

        item = self.load(evidence_id)
        seen, inputs = set(), {(entry.fact, entry.provenance) for entry in item.lineage.inputs}
        derivations_verified = inputs_verified = True
        pending = list(item.derived_from + (() if item.recomputes is None else (item.recomputes,)))
        seen.update(pending)
        while pending:
            current = self.load(pending.pop())
            derivations_verified = derivations_verified and current.lineage.derivations_complete
            inputs_verified = inputs_verified and current.lineage.inputs_complete
            inputs.update((entry.fact, entry.provenance) for entry in current.lineage.inputs)
            for link in current.derived_from + (() if current.recomputes is None else (current.recomputes,)):
                if link not in seen:
                    seen.add(link)
                    pending.append(link)
        return seen, inputs, derivations_verified, inputs_verified

    @staticmethod
    def _compatible(first: EvidenceId, second: EvidenceId, inputs_a, inputs_b) -> None:
        """Refuse two items whose recorded calculation provenance, their ancestors' included, differs (AC11)."""

        differing = provenance_differences(*(provenance for _fact, provenance in inputs_a | inputs_b))
        if differing:
            raise StoreError(f"{first} and {second} differ in calculation provenance ({', '.join(differing)}); "
                             f"they are not related (H4 s3)")

    def classify(self, first: EvidenceId, second: EvidenceId) -> Relationship:
        """The structural relationship, from recorded links, inputs and completeness statements (ADR-0119 AC12).

        An item's recorded inputs include its ancestors' inputs, and its lineage is complete only if every
        ancestor's is. A stronger recorded relationship (DERIVED, then SHARED-ORIGIN) is reported first; otherwise
        anything missing, incomplete or unverified is UNKNOWN, and INDEPENDENT needs positive recorded evidence.
        """

        a, b = self.load(first), self.load(second)
        conflicting = _conflicting(a, b)
        ancestors_a, inputs_a, derivations_a, ancestral_inputs_a = self._ancestry(first)
        ancestors_b, inputs_b, derivations_b, ancestral_inputs_b = self._ancestry(second)
        self._compatible(first, second, inputs_a, inputs_b)
        if second in ancestors_a or first in ancestors_b:
            return Relationship(first, second, DependencyClass.DERIVED, conflicting, "a recorded derivation link")
        shared = sorted(inputs_a & inputs_b, key=lambda pair: pair[0])
        if shared:
            return Relationship(first, second, DependencyClass.SHARED_ORIGIN, conflicting,
                                "recorded shared input, own or ancestral: " +
                                ", ".join(fact for fact, _provenance in shared))
        if ancestors_a & ancestors_b:
            return Relationship(first, second, DependencyClass.SHARED_ORIGIN, conflicting,
                                "a shared recorded ancestor: " + ", ".join(sorted(link.value for link in
                                                                                 ancestors_a & ancestors_b)))
        for missing, reason in ((withholds_independence(a, b),
                                 "an untimed natal item and another item about the same entity share its chart's origin; "
                                 "independence is not established (ADR-0134 D6-c)"),
                                (not (a.lineage.derivations_complete and b.lineage.derivations_complete),
                                 "a derivation link may be missing: not every derivation list is stated complete"),
                                (not (a.lineage.inputs_complete and b.lineage.inputs_complete),
                                 "incomplete lineage: not every input list is stated complete"),
                                (not (ancestral_inputs_a and ancestral_inputs_b),
                                 "incomplete ancestral lineage: an ancestor's input list is not stated complete"),
                                (not (derivations_a and derivations_b),
                                 "an unverified derivation path: an ancestor's derivation list is not stated complete"),
                                (a.producing_system is b.producing_system,
                                 "the same producing system; independence needs different systems")):
            if missing:
                return Relationship(first, second, DependencyClass.UNKNOWN, conflicting, reason)
        return Relationship(first, second, DependencyClass.INDEPENDENT, conflicting,
                            "different systems, complete recorded lineage, ancestors' included, with disjoint "
                            "inputs, and no recorded derivation path")

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

    @staticmethod
    def _require_relationship_row(relationship: Relationship, first_id: str, second_id: str) -> None:
        if (relationship.first.value, relationship.second.value) != (first_id, second_id):
            raise StoreError(f"a persisted relationship's record does not match its row: {first_id}, {second_id}")

    @staticmethod
    def _unsupported_fields(recorded: Relationship, supported: Relationship) -> tuple:
        """The fields of a recorded relationship that its source evidence does not support."""

        return tuple(name for name, mine, theirs in (("dependency", recorded.dependency, supported.dependency),
                                                     ("conflict flag", recorded.conflicting, supported.conflicting),
                                                     ("basis", recorded.basis, supported.basis)) if mine != theirs)

    def _supported_relationship(self, first_id: str, second_id: str, payload: str) -> Relationship:
        """A persisted relationship, only if its identities match its row, both items pass the evidence read checks,
        their calculation provenance agrees, and classifying them again gives exactly what is recorded. The items and
        their recorded ancestors are immutable, so a legitimate record always agrees (H4 s10; ADR-0021 D5; ADR-0125)."""

        try:
            relationship = relationship_from_record(json.loads(payload))
        except (ValueError, TypeError, KeyError) as exc:
            raise StoreError(f"a persisted relationship record is refused: {exc}") from exc
        self._require_relationship_row(relationship, first_id, second_id)
        self._compatible(relationship.first, relationship.second, self._ancestry(relationship.first)[1],
                         self._ancestry(relationship.second)[1])
        unsupported = self._unsupported_fields(relationship, self.classify(relationship.first, relationship.second))
        if unsupported:
            raise StoreError(f"the persisted relationship of {first_id} and {second_id} is not supported by its source "
                             f"evidence: {', '.join(unsupported)} (ADR-0125)")
        return relationship

    def relationships(self) -> list:
        """Every recorded relationship, oldest first. A persisted relationship its immutable source evidence does not
        support is refused, however it was written (AC11; ADR-0125)."""

        return [self._supported_relationship(first_id, second_id, payload)
                for first_id, second_id, payload in self._db.execute(
                    "SELECT first_id, second_id, payload FROM evidence_relationships "
                    "ORDER BY relationship_number").fetchall()]

    def relationship_counts(self) -> dict:
        """Recorded relationships by dependency class, each with its pairs. UNKNOWN is its own class."""

        groups = {kind.value: [] for kind in DependencyClass}
        conflicts = []
        for relationship in self.relationships():
            groups[relationship.dependency.value].append((relationship.first, relationship.second))
            if relationship.conflicting:
                conflicts.append((relationship.first, relationship.second))
        return {**{kind: tuple(pairs) for kind, pairs in groups.items()}, "conflicting": tuple(conflicts)}


__all__ = ["SCHEMA_VERSION", "UNTIMED_SCHEMA_VERSION", "NATAL_PLACEMENT_KINDS", "GOVERNED_NATAL_VERIFIER",
           "require_governed_verifier", "EvidenceStore", "EvidenceModelError", "item_to_record", "item_from_record",
           "rule_to_record", "rule_from_record", "relationship_to_record", "relationship_from_record"]
