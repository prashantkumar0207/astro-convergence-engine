"""Provenance-graph recording (ADR-0122 s4 to s6, ratified; WP-E6).

The graph an evidence item consumed, recorded when the item is persisted and in the same transaction
(D2 A). Its schema is the recording schema of docs/EVIDENCE_INDEPENDENCE_DESIGN.md s3 and nothing else
of that document (D1 A): six node kinds and two edge kinds. CORRELATED_WITH is not an edge kind here:
it is measured, and nothing in EVIDENCE measures.

- Identity (D3 A): a node is the SHA-256 of its kind and canonical identity record. Two items share a
  node exactly when every identity field agrees, full calculation provenance included. Evidence and
  rule nodes carry their EVD and RUL identity. No new identifier family is issued.
- Not inferred (AC5): record_graph builds an item's nodes and edges only from the item and the records
  the store hands it: the chart the item names at its entity revision, that revision's H0 parent link,
  the registered rule version, and the linked items. It reads nothing else.
- Completeness (AC6): an item's statements that its inputs or derivations are incomplete sit on its
  evidence node. The graph never adds a node or edge to make an item look complete.
- Decomposable (AC7): reproduce() rebuilds, from a graph alone, the item's calculated inputs, chart
  reference, varga, timing, rule reference and derivation and recomputation links.

Edges run from what was consumed to what consumed it: an edge (source, DERIVES_FROM, target) records
that target was computed from source, and (source, APPLIES_TO, target) records the rule application an
evidence item is, consuming its rule and its calculated facts. Nothing here counts paths, computes an
independent count, a cut, a score, a weight or a ratio, or classifies a relationship (AC11, AC12).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum

from engine.evidence.entity import ChartCandidate, ParentLink
from engine.evidence.evidence import (
    CalculatedInput, ChartReference, EvidenceItem, Lineage, RuleReference, RuleVersion, TimingContext, TimingKind,
)
from engine.evidence.evidence_identifiers import EvidenceId, RuleId
from engine.evidence.identifiers import EntityId
from engine.models.provenance import Provenance

#: The stored form's schema. A node record carries it; its key does not, so identity outlives a format change.
GRAPH_SCHEMA = "ace-provenance-graph-v1"
PROVENANCE_FIELDS = tuple(name for name in Provenance.__dataclass_fields__)


class GraphError(ValueError):
    """A node, edge or graph this module refuses."""


class NodeKind(Enum):
    """The independence design's s3 node kinds (ADR-0122 D1 A)."""

    INPUT = "input"
    ASTRONOMICAL = "astronomical"
    DERIVED_CHART = "derived_chart"
    TIMING = "timing"
    RULE = "rule"
    EVIDENCE = "evidence"


class EdgeKind(Enum):
    """The two recorded edge kinds. CORRELATED_WITH is measured, never recorded here (ADR-0122 s4)."""

    DERIVES_FROM = "derives_from"
    APPLIES_TO = "applies_to"


#: Each node kind's identity fields (AC2). A chart's origin, a fact and a timing context are each tied to the chart
#: the item names, so facts of two charts are never silently unified.
IDENTITY_FIELDS = {
    NodeKind.INPUT: ("entity", "entity_revision", "chart_label", "local_datetime", "timezone", "timezone_source",
                     "latitude", "longitude", "precision", "origin_certainty"),
    NodeKind.ASTRONOMICAL: ("entity", "entity_revision", "chart_label", "fact", "provenance"),
    NodeKind.DERIVED_CHART: ("entity", "entity_revision", "chart_label", "varga"),
    NodeKind.TIMING: ("entity", "entity_revision", "chart_label", "kind", "label", "start", "end"),
    NodeKind.RULE: ("rule", "version", "variant", "content_hash", "knowledge_snapshot_hash"),
    NodeKind.EVIDENCE: ("evidence", "inputs_complete", "derivations_complete", "recomputes"),
}

#: The declared node-kind pairs of each edge kind (AC3). Anything else is refused.
ALLOWED_PAIRS = {
    EdgeKind.DERIVES_FROM: frozenset({
        (NodeKind.INPUT, NodeKind.ASTRONOMICAL),            # a calculated fact from its chart's origin
        (NodeKind.INPUT, NodeKind.DERIVED_CHART),           # a chart from its origin
        (NodeKind.DERIVED_CHART, NodeKind.DERIVED_CHART),   # a derived subject's chart from its parent chart (H0)
        (NodeKind.DERIVED_CHART, NodeKind.EVIDENCE),        # the item, from the chart and varga it reads
        (NodeKind.TIMING, NodeKind.EVIDENCE),               # the item, within its timing context
        (NodeKind.EVIDENCE, NodeKind.EVIDENCE),             # derivation and recomputation links
    }),
    EdgeKind.APPLIES_TO: frozenset({
        (NodeKind.RULE, NodeKind.EVIDENCE),                 # the registered rule version the item applies
        (NodeKind.ASTRONOMICAL, NodeKind.EVIDENCE),         # a fact that application consumed
    }),
}


def canonical(data) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _scalar(value) -> bool:
    return value is None or isinstance(value, (str, int, float, bool))


def _identity_valid(kind: NodeKind, identity: dict) -> None:
    if set(identity) != set(IDENTITY_FIELDS[kind]):
        raise GraphError(f"a {kind.value} node carries exactly its identity fields "
                         f"{list(IDENTITY_FIELDS[kind])}; refused: {sorted(identity)}")
    for name, value in identity.items():
        if name == "provenance":
            if not isinstance(value, dict) or set(value) != set(PROVENANCE_FIELDS) or \
                    not all(_scalar(item) for item in value.values()):
                raise GraphError("an astronomical node carries every field of its calculation Provenance")
        elif not _scalar(value):
            raise GraphError(f"a {kind.value} node's {name} is a plain value")
    if kind is NodeKind.DERIVED_CHART and (identity["entity_revision"] is None) != (identity["varga"] is None):
        raise GraphError("only a parent chart, as an H0 parent link names it, leaves both revision and varga "
                         "unrecorded")


@dataclass(frozen=True, slots=True)
class Node:
    """One node: its kind and canonical identity record. Its key is derived, never assigned (D3 A)."""

    kind: NodeKind
    identity: str
    key: str = field(init=False, compare=False)

    def __post_init__(self):
        if not isinstance(self.kind, NodeKind):
            raise GraphError(f"an undeclared node kind: {self.kind!r}")
        if not isinstance(self.identity, str):
            raise GraphError("a node's identity is its canonical record")
        try:
            identity = json.loads(self.identity)
        except ValueError as exc:
            raise GraphError("a node's identity is canonical JSON") from exc
        if not isinstance(identity, dict) or canonical(identity) != self.identity:
            raise GraphError("a node's identity is a canonical JSON object")
        _identity_valid(self.kind, identity)
        object.__setattr__(self, "key", hashlib.sha256(
            canonical({"kind": self.kind.value, "identity": identity}).encode("ascii")).hexdigest())

    def fields(self) -> dict:
        return json.loads(self.identity)


def make_node(node_kind: NodeKind, /, **identity) -> Node:
    return Node(kind=node_kind, identity=canonical(identity))


@dataclass(frozen=True, slots=True)
class Edge:
    """One directed edge between two nodes, of a declared kind and pair. `position` is the order an item recorded
    its inputs or derivation links in; it is 0 otherwise."""

    source: Node
    kind: EdgeKind
    target: Node
    position: int = 0

    def __post_init__(self):
        if not isinstance(self.kind, EdgeKind):
            raise GraphError(f"an undeclared edge kind: {self.kind!r}; CORRELATED_WITH is measured, never recorded "
                             f"here (ADR-0122 s4)")
        if not isinstance(self.source, Node) or not isinstance(self.target, Node):
            raise GraphError("an edge joins two nodes")
        if (self.source.kind, self.target.kind) not in ALLOWED_PAIRS[self.kind]:
            raise GraphError(f"a {self.kind.value} edge from a {self.source.kind.value} node to a "
                             f"{self.target.kind.value} node is not a declared pair")
        if self.source.key == self.target.key:
            raise GraphError("an edge from a node to itself closes a cycle")
        if isinstance(self.position, bool) or not isinstance(self.position, int) or self.position < 0:
            raise GraphError("an edge position is an integer from 0")


@dataclass(frozen=True, slots=True)
class Graph:
    """Nodes and edges as recorded, each read returning its members."""

    nodes: tuple
    edges: tuple

    def __post_init__(self):
        keys = {node.key for node in self.nodes}
        if len(keys) != len(self.nodes):
            raise GraphError("a graph holds each node once")
        for edge in self.edges:
            if edge.source.key not in keys or edge.target.key not in keys:
                raise GraphError("a dangling edge: an edge names a node the graph does not hold")
        if len({(edge.source.key, edge.kind, edge.target.key) for edge in self.edges}) != len(self.edges):
            raise GraphError("a graph holds each edge once")
        cycle = _cycle(self.edges)
        if cycle:
            raise GraphError(f"the graph is not acyclic: a cycle through {cycle}")


def _cycle(edges) -> str:
    """A node on a directed cycle, or the empty string. Depth-first colouring; nothing is counted."""

    outgoing = {}
    for edge in edges:
        outgoing.setdefault(edge.source.key, []).append(edge.target.key)
    state = {}
    for start in sorted(outgoing):
        if start in state:
            continue
        stack = [(start, iter(outgoing[start]))]
        state[start] = "open"
        while stack:
            current, successors = stack[-1]
            advanced = False
            for successor in successors:
                if successor in state and state[successor] == "open":
                    return successor
                if successor not in state:
                    state[successor] = "open"
                    stack.append((successor, iter(outgoing[successor] if successor in outgoing else ())))
                    advanced = True
                    break
            if not advanced:
                state[current] = "closed"
                stack.pop()
    return ""


# ------------------------------------------------------------------ the node of each recorded field

def _chart_identity(entity: EntityId, chart: ChartReference) -> dict:
    return {"entity": entity.value, "entity_revision": chart.entity_revision, "chart_label": chart.chart_label}


def input_node(entity: EntityId, chart: ChartReference, candidate: ChartCandidate) -> Node:
    origin = candidate.origin
    return make_node(NodeKind.INPUT, **_chart_identity(entity, chart), local_datetime=origin.local_datetime,
                     timezone=origin.timezone, timezone_source=origin.timezone_source, latitude=origin.latitude,
                     longitude=origin.longitude, precision=origin.precision,
                     origin_certainty=candidate.origin_certainty.value)


def astronomical_node(entity: EntityId, chart: ChartReference, calculated: CalculatedInput) -> Node:
    provenance = calculated.provenance
    return make_node(NodeKind.ASTRONOMICAL, **_chart_identity(entity, chart), fact=calculated.fact,
                     provenance={name: provenance.__getattribute__(name) for name in PROVENANCE_FIELDS})


def chart_node(entity: EntityId, chart: ChartReference, varga: str) -> Node:
    return make_node(NodeKind.DERIVED_CHART, **_chart_identity(entity, chart), varga=varga)


def parent_chart_node(parent: ParentLink) -> Node:
    """The parent chart exactly as the H0 parent link names it: an entity and a chart label, no revision or varga."""

    return make_node(NodeKind.DERIVED_CHART, entity=parent.parent.value, entity_revision=None,
                     chart_label=parent.parent_chart, varga=None)


def timing_node(entity: EntityId, chart: ChartReference, timing: TimingContext) -> Node:
    return make_node(NodeKind.TIMING, **_chart_identity(entity, chart), kind=timing.kind.value, label=timing.label,
                     start=timing.start, end=timing.end)


def rule_node(rule: RuleVersion) -> Node:
    identity: RuleId = rule.rule
    return make_node(NodeKind.RULE, rule=identity.value, version=rule.version, variant=rule.spec.variant,
                     content_hash=rule.spec.content_hash, knowledge_snapshot_hash=rule.spec.knowledge_snapshot_hash)


def evidence_node(evidence_id: EvidenceId, item: EvidenceItem) -> Node:
    recomputes: EvidenceId | None = item.recomputes
    return make_node(NodeKind.EVIDENCE, evidence=evidence_id.value,
                     inputs_complete=item.lineage.inputs_complete,
                     derivations_complete=item.lineage.derivations_complete,
                     recomputes=None if recomputes is None else recomputes.value)


def record_graph(evidence_id: EvidenceId, item: EvidenceItem, candidate: ChartCandidate, parent: ParentLink | None,
                 rule: RuleVersion, linked: dict) -> Graph:
    """The nodes and edges `item` consumed, from its own fields and the records the store holds for it (D2 A, AC5):
    the chart it names at its entity revision, that revision's parent link, its registered rule version, and the
    items it links to. Nothing is added for a field the item does not carry."""

    if not isinstance(item, EvidenceItem) or not isinstance(candidate, ChartCandidate) or \
            not isinstance(rule, RuleVersion) or (parent is not None and not isinstance(parent, ParentLink)):
        raise GraphError("a graph is recorded from an item, its chart, its parent link and its registered rule")
    reference = RuleReference(rule=rule.rule, version=rule.version, variant=rule.spec.variant)
    if candidate.label != item.chart.chart_label or reference != item.rule:
        raise GraphError("the records handed in are not the ones the item names")
    links = item.derived_from + (() if item.recomputes is None else (item.recomputes,))
    if set(linked) != set(links) or not all(isinstance(value, EvidenceItem) for value in linked.values()):
        raise GraphError("the linked items are exactly the ones the item names")
    entity, chart = item.entity, item.chart
    origin, read, target = input_node(entity, chart, candidate), chart_node(entity, chart, item.chart_context.varga), \
        evidence_node(evidence_id, item)
    nodes, edges = {target.key: target}, []

    def add(source: Node, kind: EdgeKind, position: int = 0) -> None:
        nodes[source.key] = source
        edges.append(Edge(source=source, kind=kind, target=target, position=position))

    nodes[origin.key] = origin
    nodes[read.key] = read
    edges.append(Edge(source=origin, kind=EdgeKind.DERIVES_FROM, target=read))
    if parent is not None:
        parent_chart = parent_chart_node(parent)
        nodes[parent_chart.key] = parent_chart
        edges.append(Edge(source=parent_chart, kind=EdgeKind.DERIVES_FROM, target=read))
    for position, calculated in enumerate(item.lineage.inputs):
        fact = astronomical_node(entity, chart, calculated)
        nodes[fact.key] = fact
        edges.append(Edge(source=origin, kind=EdgeKind.DERIVES_FROM, target=fact))
        add(fact, EdgeKind.APPLIES_TO, position)
    add(read, EdgeKind.DERIVES_FROM)
    add(timing_node(entity, chart, item.timing), EdgeKind.DERIVES_FROM)
    add(rule_node(rule), EdgeKind.APPLIES_TO)
    for position, link in enumerate(item.derived_from):
        add(evidence_node(link, linked[link]), EdgeKind.DERIVES_FROM, position)
    if item.recomputes is not None:
        add(evidence_node(item.recomputes, linked[item.recomputes]), EdgeKind.DERIVES_FROM)
    return Graph(nodes=tuple(nodes[key] for key in sorted(nodes)), edges=tuple(edges))


# ------------------------------------------------------------------ reproduction from a graph alone (AC7)

def _one(edges, kind: NodeKind, label: str):
    found = [edge for edge in edges if edge.source.kind is kind]
    if len(found) != 1:
        raise GraphError(f"an evidence node records exactly one {label}; found {len(found)}")
    return found[0].source.fields()


def reproduce(graph: Graph, evidence_id: EvidenceId) -> dict:
    """What `graph` alone records of one item: its entity, chart reference, varga, lineage, timing, rule reference,
    derivation links and recomputation link. Nothing is read from the item itself."""

    targets = [node for node in graph.nodes if node.kind is NodeKind.EVIDENCE and
               node.fields()["evidence"] == evidence_id.value]
    if len(targets) != 1:
        raise GraphError(f"the graph holds no single evidence node for {evidence_id}")
    target = targets[0]
    record = target.fields()
    incoming = [edge for edge in graph.edges if edge.target.key == target.key]
    chart = _one(incoming, NodeKind.DERIVED_CHART, "chart")
    timing = _one(incoming, NodeKind.TIMING, "timing context")
    rule = _one(incoming, NodeKind.RULE, "rule version")
    facts = sorted((edge for edge in incoming if edge.source.kind is NodeKind.ASTRONOMICAL),
                   key=lambda edge: edge.position)
    if [edge.position for edge in facts] != list(range(len(facts))) or \
            any(edge.kind is not EdgeKind.APPLIES_TO for edge in facts):
        raise GraphError("an evidence node's facts are recorded once each, in order, as applied")
    for fact in facts:
        identity = fact.source.fields()
        if (identity["entity"], identity["entity_revision"], identity["chart_label"]) != \
                (chart["entity"], chart["entity_revision"], chart["chart_label"]):
            raise GraphError("a fact recorded for another chart than the one the item reads")
    links = [edge for edge in incoming if edge.source.kind is NodeKind.EVIDENCE]
    recomputes = record["recomputes"]
    derived = sorted((edge for edge in links if edge.source.fields()["evidence"] != recomputes),
                     key=lambda edge: edge.position)
    if recomputes is not None and len(links) - len(derived) != 1:
        raise GraphError("a recomputation's original is recorded as one derivation edge")
    if [edge.position for edge in derived] != list(range(len(derived))):
        raise GraphError("an evidence node's derivation links are recorded once each, in order")
    return {
        "entity": EntityId(chart["entity"]),
        "chart": ChartReference(entity_revision=chart["entity_revision"], chart_label=chart["chart_label"]),
        "varga": chart["varga"],
        "lineage": Lineage(inputs=tuple(CalculatedInput(fact=edge.source.fields()["fact"],
                                                        provenance=Provenance(**edge.source.fields()["provenance"]))
                                        for edge in facts),
                           inputs_complete=record["inputs_complete"],
                           derivations_complete=record["derivations_complete"]),
        "timing": TimingContext(kind=TimingKind(timing["kind"]), label=timing["label"], start=timing["start"],
                                end=timing["end"]),
        "rule": RuleReference(rule=RuleId(rule["rule"]), version=rule["version"], variant=rule["variant"]),
        "derived_from": tuple(EvidenceId(edge.source.fields()["evidence"]) for edge in derived),
        "recomputes": None if recomputes is None else EvidenceId(recomputes),
    }


def recorded_fields(item: EvidenceItem) -> dict:
    """The same fields, read from the item: what reproduce() must equal (AC7)."""

    return {"entity": item.entity, "chart": item.chart, "varga": item.chart_context.varga, "lineage": item.lineage,
            "timing": item.timing, "rule": item.rule, "derived_from": item.derived_from,
            "recomputes": item.recomputes}


# ------------------------------------------------------------------ recorded rows against the items' records

def unjustified_rows(recorded: Graph, expected) -> tuple:
    """Every way `recorded` differs from what the items' stored records justify: a node or edge they do not account
    for, or one they require that is not recorded. An edge is its source, kind, target and position. This compares;
    it never supplies a missing row, so it is no substitute for recording at creation (ADR-0122 D2, AC5, AC7)."""

    def identity(edge: Edge) -> tuple:
        return edge.source.key, edge.kind.value, edge.target.key, edge.position

    graphs = tuple(expected)
    held_nodes, held_edges = {node.key for node in recorded.nodes}, {identity(edge) for edge in recorded.edges}
    nodes = {node.key for graph in graphs for node in graph.nodes}
    edges = {identity(edge) for graph in graphs for edge in graph.edges}
    return tuple([f"unaccounted node {key}" for key in sorted(held_nodes - nodes)] +
                 [f"unaccounted edge {edge}" for edge in sorted(held_edges - edges)] +
                 [f"missing node {key}" for key in sorted(nodes - held_nodes)] +
                 [f"missing edge {edge}" for edge in sorted(edges - held_edges)])


# ------------------------------------------------------------------ the stored form

def node_to_row(node: Node) -> tuple:
    return node.key, node.kind.value, canonical({"schema": GRAPH_SCHEMA, "kind": node.kind.value,
                                                 "identity": node.fields()})


def node_from_row(key: str, kind: str, payload: str) -> Node:
    """Rebuild a stored node, refusing a row whose payload, kind or key disagree, however it was written."""

    try:
        data = json.loads(payload)
    except ValueError as exc:
        raise GraphError(f"node {key}: its payload is not JSON") from exc
    if not isinstance(data, dict) or set(data) != {"schema", "kind", "identity"} or data["schema"] != GRAPH_SCHEMA \
            or data["kind"] != kind or not isinstance(data["identity"], dict):
        raise GraphError(f"node {key}: not a node record of this schema")
    try:
        node = Node(kind=NodeKind(kind), identity=canonical(data["identity"]))
    except ValueError as exc:
        raise GraphError(f"node {key}: {exc}") from exc
    if node.key != key:
        raise GraphError(f"node {key}: its key is not the hash of its identity; a node is found from what it is")
    return node


def edge_from_row(nodes: dict, source: str, kind: str, target: str, position: int) -> Edge:
    """Rebuild a stored edge against the nodes read with it; a dangling or undeclared edge is refused."""

    if source not in nodes or target not in nodes:
        raise GraphError(f"a dangling edge: {source} -> {target} names a node that is not recorded")
    try:
        edge_kind = EdgeKind(kind)
    except ValueError as exc:
        raise GraphError(f"an undeclared edge kind {kind!r}; CORRELATED_WITH is measured, never recorded here "
                         f"(ADR-0122 s4)") from exc
    return Edge(source=nodes[source], kind=edge_kind, target=nodes[target], position=position)


__all__ = ["GRAPH_SCHEMA", "ALLOWED_PAIRS", "IDENTITY_FIELDS", "Edge", "EdgeKind", "Graph", "GraphError", "Node",
           "NodeKind", "unjustified_rows", "astronomical_node", "canonical", "chart_node", "edge_from_row", "evidence_node",
           "input_node", "make_node", "node_from_row", "node_to_row", "parent_chart_node", "record_graph",
           "recorded_fields", "reproduce", "rule_node", "timing_node"]
