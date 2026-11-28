"""WP-E6 acceptance tests (ADR-0122 s6, ratified): provenance-graph recording. Every record here is synthetic."""

from __future__ import annotations

import ast
import dataclasses
import hashlib
import json
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "engine" / "tests"))

from test_evidence_wp_e4 import CALC, PROV, World, person  # noqa: E402

from engine.evidence import provenance_graph as graph  # noqa: E402
from engine.evidence import rule_registry  # noqa: E402
from engine.evidence.entity import ChartCandidate, EntityKind, ParentLink, Person, Shape  # noqa: E402
from engine.evidence.evidence import CalculatedInput, ChartReference, Lineage  # noqa: E402
from engine.evidence.evidence_identifiers import EvidenceId  # noqa: E402
from engine.evidence.evidence_store import EvidenceStore  # noqa: E402
from engine.evidence.provenance_graph import Edge, EdgeKind, Graph, GraphError, NodeKind  # noqa: E402
from engine.evidence.store import StoreError  # noqa: E402
from engine.models.provenance import Provenance  # noqa: E402

GRAPH_MODULE = ROOT / "engine" / "evidence" / "provenance_graph.py"
STORE_MODULE = ROOT / "engine" / "evidence" / "evidence_store.py"


@pytest.fixture()
def world(tmp_path):
    instance = World(tmp_path / "evidence.sqlite")
    yield instance
    instance.store.close()


def _counts(store):
    return tuple(store._db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                 for table in ("evidence_items", "graph_nodes", "graph_edges"))


def _expected(store, evidence_id):
    """What persist must have recorded for one item, rebuilt here from the store's own records (a check, not a
    recording path)."""

    item = store.load(evidence_id)
    _number, subject, _reason = store.entities.history(item.entity)[item.chart.entity_revision - 1]
    candidate = [chart for chart in subject.charts if chart.label == item.chart.chart_label][0]
    links = item.derived_from + (() if item.recomputes is None else (item.recomputes,))
    return graph.record_graph(evidence_id, item, candidate, subject.parent, store.rule_version(item.rule),
                              {link: store.load(link) for link in links})


def _edge_keys(edges):
    return {(edge.source.key, edge.kind, edge.target.key, edge.position) for edge in edges}


# ------------------------------------------------------------------ AC1 recorded at creation

def test_ac1_persist_writes_the_item_and_its_graph_together(world):
    before = _counts(world.store)
    first = world.store.persist(world.item(facts=("Moon longitude", "Sun longitude")))
    items, nodes, edges = _counts(world.store)
    assert (items, before[1], before[2]) == (1, 0, 0) and nodes > 0 and edges > 0
    recorded = world.store.item_graph(first)
    assert {node.key for node in recorded.nodes} == {node.key for node in _expected(world.store, first).nodes}


def test_ac1_a_graph_that_cannot_be_written_persists_nothing_and_takes_no_number(world):
    item = world.item()
    origin = graph.input_node(item.entity, item.chart, person().charts[0])
    world.store._db.execute("INSERT INTO graph_nodes (node_key, kind, payload) VALUES (?, ?, ?)",
                            (origin.key, "input", json.dumps({"schema": graph.GRAPH_SCHEMA, "kind": "input",
                                                              "identity": {"planted": True}})))
    before = _counts(world.store)
    with pytest.raises(StoreError, match="recorded node is refused"):
        world.store.persist(item)
    assert _counts(world.store) == before and world.store.issued_count("EVD") == 0


def test_ac1_no_api_adds_a_node_or_edge_after_persist():
    tree = ast.parse(STORE_MODULE.read_text(encoding="utf-8"))
    store = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "EvidenceStore")
    writers = {method.name for method in store.body if isinstance(method, ast.FunctionDef) and any(
        isinstance(node, ast.Constant) and isinstance(node.value, str) and "INSERT INTO graph_" in node.value
        for node in ast.walk(method))}
    assert writers == {"_write_graph"}
    callers = {method.name for method in store.body if isinstance(method, ast.FunctionDef) and any(
        isinstance(node, ast.Attribute) and node.attr == "_write_graph" for node in ast.walk(method))}
    assert callers == {"persist"}
    public = [name for name in dir(EvidenceStore) if not name.startswith("_")]
    assert not [name for name in public if any(word in name for word in ("add", "write", "insert", "link", "attach"))]


# ------------------------------------------------------------------ AC2 node kinds and identity

def test_ac2_six_kinds_each_declare_identity_fields_and_keys_are_content_hashes():
    # The six kinds of the dated recording schema (ADR-0122 D1), and UNTIMED, added by ADR-0134 for untimed natal items.
    assert set(NodeKind) == set(graph.IDENTITY_FIELDS) and {kind.value for kind in NodeKind} == {
        "input", "astronomical", "derived_chart", "timing", "rule", "evidence", "untimed"}
    node = graph.make_node(NodeKind.RULE, rule="RUL-000001", version=1, variant="base", content_hash="a" * 64,
                           knowledge_snapshot_hash="b" * 64)
    assert node.key == hashlib.sha256(graph.canonical({"kind": "rule", "identity": node.fields()}).encode()).hexdigest()
    with pytest.raises(GraphError, match="exactly its identity fields"):
        graph.make_node(NodeKind.RULE, rule="RUL-000001", version=1)
    with pytest.raises(GraphError, match="exactly its identity fields"):
        graph.make_node(NodeKind.RULE, **node.fields(), weight=1)
    with pytest.raises(GraphError, match="undeclared node kind"):
        graph.Node(kind="rule", identity=node.identity)


@pytest.mark.parametrize("field", graph.PROVENANCE_FIELDS)
def test_ac2_the_same_fact_under_provenance_differing_in_one_field_is_two_nodes(world, field):
    value = CALC.__getattribute__(field)
    changed = dataclasses.replace(CALC, **{field: value + 1 if isinstance(value, int) else f"{value}-other"})
    item = world.item()
    one = graph.astronomical_node(item.entity, item.chart, CalculatedInput(fact="Moon longitude", provenance=CALC))
    two = graph.astronomical_node(item.entity, item.chart, CalculatedInput(fact="Moon longitude", provenance=changed))
    assert one.key != two.key
    first = world.store.persist(item)
    second = world.store.persist(world.item(provenance=changed))
    facts = lambda evidence_id: {node.key for node in world.store.item_graph(evidence_id).nodes
                                 if node.kind is NodeKind.ASTRONOMICAL}
    assert facts(first) == {one.key} and facts(second) == {two.key}


def test_ac2_identical_identity_fields_across_items_give_one_node(world):
    first = world.store.persist(world.item())
    second = world.store.persist(world.item())
    shared = {node.key for node in world.store.item_graph(first).nodes} & \
        {node.key for node in world.store.item_graph(second).nodes}
    kinds = {node.kind for node in world.store.recorded_graph().nodes if node.key in shared}
    assert kinds == {NodeKind.INPUT, NodeKind.ASTRONOMICAL, NodeKind.DERIVED_CHART, NodeKind.TIMING, NodeKind.RULE}
    rows = world.store._db.execute("SELECT COUNT(*) FROM graph_nodes WHERE kind = 'input'").fetchone()[0]
    assert rows == 1


# ------------------------------------------------------------------ AC3 edges

def _nodes(world):
    item = world.item()
    return (graph.input_node(item.entity, item.chart, person().charts[0]),
            graph.evidence_node(EvidenceId.from_number(1), item), graph.rule_node(world.parashari))


def test_ac3_only_two_edge_kinds_exist_and_correlated_with_is_refused(world):
    assert {kind.value for kind in EdgeKind} == {"derives_from", "applies_to"}
    origin, target, _rule = _nodes(world)
    for kind in ("correlated_with", "CORRELATED_WITH", "derives_from"):
        with pytest.raises(GraphError, match="undeclared edge kind"):
            Edge(source=origin, kind=kind, target=target)
    with pytest.raises(GraphError, match="undeclared edge kind"):
        graph.edge_from_row({origin.key: origin, target.key: target}, origin.key, "correlated_with", target.key, 0)


def test_ac3_a_disallowed_pair_is_refused(world):
    origin, target, rule = _nodes(world)
    with pytest.raises(GraphError, match="not a declared pair"):
        Edge(source=origin, kind=EdgeKind.APPLIES_TO, target=target)
    with pytest.raises(GraphError, match="not a declared pair"):
        Edge(source=target, kind=EdgeKind.DERIVES_FROM, target=origin)
    with pytest.raises(GraphError, match="not a declared pair"):
        Edge(source=rule, kind=EdgeKind.DERIVES_FROM, target=target)


def test_ac3_a_dangling_edge_is_refused(world):
    origin, target, _rule = _nodes(world)
    with pytest.raises(GraphError, match="dangling"):
        Graph(nodes=(target,), edges=(Edge(source=origin, kind=EdgeKind.DERIVES_FROM,
                                           target=graph.chart_node(target_entity(world), ChartReference(1, "natal"),
                                                                   "D1")),))
    with pytest.raises(GraphError, match="dangling"):
        graph.edge_from_row({target.key: target}, origin.key, "derives_from", target.key, 0)


def target_entity(world):
    return world.item().entity


# ------------------------------------------------------------------ AC4 acyclic

def test_ac4_a_cycle_is_refused_in_a_graph(world):
    first, second = (graph.evidence_node(EvidenceId.from_number(n), world.item()) for n in (1, 2))
    with pytest.raises(GraphError, match="not acyclic"):
        Graph(nodes=(first, second), edges=(Edge(source=first, kind=EdgeKind.DERIVES_FROM, target=second),
                                            Edge(source=second, kind=EdgeKind.DERIVES_FROM, target=first)))
    with pytest.raises(GraphError, match="cycle"):
        Edge(source=first, kind=EdgeKind.DERIVES_FROM, target=first)


def test_ac4_an_edge_that_would_close_a_cycle_is_refused_on_write(world):
    item = world.item(facts=("Mars longitude",))
    origin = graph.input_node(item.entity, item.chart, person().charts[0])
    fact = graph.astronomical_node(item.entity, item.chart, item.lineage.inputs[0])
    for node in (origin, fact):
        world.store._db.execute("INSERT INTO graph_nodes (node_key, kind, payload) VALUES (?, ?, ?)",
                                graph.node_to_row(node))
    world.store._db.execute("INSERT INTO graph_edges (source_key, kind, target_key, position) VALUES (?, ?, ?, 0)",
                            (fact.key, "derives_from", origin.key))
    with pytest.raises(StoreError, match="would close a cycle"):
        world.store.persist(item)
    assert world.store.issued_count("EVD") == 0


def test_ac4_a_cycle_or_dangling_edge_planted_by_direct_sql_is_refused_when_read(world):
    first = world.store.persist(world.item())
    second = world.store.persist(world.item(derived_from=(first,)))
    keys = [graph.evidence_node(evidence_id, world.store.load(evidence_id)).key for evidence_id in (first, second)]
    world.store._db.execute("INSERT INTO graph_edges (source_key, kind, target_key, position) VALUES (?, ?, ?, 0)",
                            (keys[1], "derives_from", keys[0]))
    with pytest.raises(StoreError, match="not acyclic"):
        world.store.item_graph(second)
    with pytest.raises(StoreError, match="not acyclic"):
        world.store.recorded_graph()


def test_ac4_a_dangling_edge_planted_by_direct_sql_is_refused_when_read(world):
    first = world.store.persist(world.item())
    key = graph.evidence_node(first, world.store.load(first)).key
    world.store._db.execute("INSERT INTO graph_edges (source_key, kind, target_key, position) VALUES (?, ?, ?, 0)",
                            ("f" * 64, "derives_from", key))
    with pytest.raises(StoreError, match="dangling"):
        world.store.item_graph(first)
    with pytest.raises(StoreError, match="dangling"):
        world.store.recorded_graph()


def test_ac4_a_node_row_whose_key_is_not_its_hash_is_refused_when_read(world):
    first = world.store.persist(world.item())
    forged = graph.make_node(NodeKind.TIMING, entity="ENT-0000000001", entity_revision=1, chart_label="natal",
                             kind="dasha", label="planted", start="2010-01-01", end="2010-01-02")
    world.store._db.execute("INSERT INTO graph_nodes (node_key, kind, payload) VALUES (?, ?, ?)",
                            ("e" * 64, "timing", graph.node_to_row(forged)[2]))
    with pytest.raises(StoreError, match="not the hash of its identity"):
        world.store.recorded_graph()
    assert world.store.item_graph(first).nodes


# ------------------------------------------------------------------ AC5 not inferred

def test_ac5_the_graph_code_reads_no_other_source():
    tree = ast.parse(GRAPH_MODULE.read_text(encoding="utf-8"))
    imported = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module} | \
        {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
    assert imported == {"__future__", "hashlib", "json", "dataclasses", "enum", "engine.evidence.entity",
                        "engine.evidence.evidence", "engine.evidence.evidence_identifiers",
                        "engine.evidence.identifiers", "engine.models.provenance"}
    calls = {node.func.id for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}
    assert not calls & {"open", "eval", "exec", "compile", "__import__", "getattr"}


def test_ac5_every_node_and_edge_comes_from_a_recorded_field(world):
    first = world.store.persist(world.item())
    recorded = world.store.item_graph(first)
    expected = _expected(world.store, first)
    assert {node.key for node in recorded.nodes} == {node.key for node in expected.nodes}
    assert _edge_keys(recorded.edges) == _edge_keys(expected.edges)
    kinds = sorted(node.kind.value for node in recorded.nodes)
    assert kinds == ["astronomical", "derived_chart", "evidence", "input", "rule", "timing"]


def test_ac5_record_graph_refuses_records_the_item_does_not_name(world):
    item = world.item()
    candidate = person().charts[0]
    with pytest.raises(GraphError, match="not the ones the item names"):
        graph.record_graph(EvidenceId.from_number(1), item, dataclasses.replace(candidate, label="other"), None,
                           world.parashari, {})
    with pytest.raises(GraphError, match="not the ones the item names"):
        graph.record_graph(EvidenceId.from_number(1), item, candidate, None, world.kp, {})
    with pytest.raises(GraphError, match="exactly the ones the item names"):
        graph.record_graph(EvidenceId.from_number(1), item, candidate, None, world.parashari,
                           {EvidenceId.from_number(9): item})


# ------------------------------------------------------------------ AC6 completeness recorded, never filled

def test_ac6_incompleteness_is_on_the_evidence_node_and_nothing_is_added(world):
    complete = world.store.persist(world.item())
    partial = world.store.persist(world.item(lineage=world.lineage(("Moon longitude",), inputs_complete=False,
                                                                     derivations_complete=False)))
    node = graph.evidence_node(partial, world.store.load(partial)).fields()
    assert (node["inputs_complete"], node["derivations_complete"]) == (False, False)
    reproduced = world.store.reproduce(partial)["lineage"]
    assert (reproduced.inputs_complete, reproduced.derivations_complete) == (False, False)
    shape = lambda evidence_id: sorted((edge.source.kind.value, edge.kind.value)
                                       for edge in world.store.item_graph(evidence_id).edges)
    assert shape(partial) == shape(complete)


# ------------------------------------------------------------------ AC7 agreement with the evidence

def test_ac7_each_item_is_reproduced_exactly_from_its_graph_alone(world):
    first = world.store.persist(world.item(facts=("Sun longitude", "Moon longitude", "Mars longitude")))
    second = world.store.persist(world.item(facts=("Jupiter longitude",), derived_from=(first,)))
    third = world.store.persist(world.item(facts=("Saturn longitude",), derived_from=(second, first)))
    fourth = world.store.persist(world.item(facts=("Moon longitude",), recomputes=first, derived_from=(third,)))
    for evidence_id in (first, second, third, fourth):
        assert world.store.reproduce(evidence_id) == graph.recorded_fields(world.store.load(evidence_id))


def test_ac7_the_graph_holds_nothing_the_records_do_not_account_for(world):
    ids = [world.store.persist(world.item())]
    ids.append(world.store.persist(world.item(facts=("Sun longitude",), derived_from=(ids[0],))))
    ids.append(world.store.persist(world.item(facts=("Moon longitude",), recomputes=ids[0])))
    expected_nodes, expected_edges = {}, set()
    for evidence_id in ids:
        expected = _expected(world.store, evidence_id)
        expected_nodes.update({node.key: node for node in expected.nodes})
        expected_edges |= _edge_keys(expected.edges)
    recorded = world.store.recorded_graph()
    assert {node.key for node in recorded.nodes} == set(expected_nodes)
    assert _edge_keys(recorded.edges) == expected_edges
    assert recorded == world.store.graph(ids)


def test_ac7_nodes_round_trip_through_storage(world):
    first = world.store.persist(world.item())
    for node in world.store.item_graph(first).nodes:
        assert graph.node_from_row(*graph.node_to_row(node)) == node


def test_ac7_a_graph_losing_an_input_does_not_reproduce_the_item(world):
    first = world.store.persist(world.item(facts=("Sun longitude", "Moon longitude")))
    full = world.store.item_graph(first)
    lossy = Graph(nodes=full.nodes, edges=tuple(edge for edge in full.edges if not (
        edge.source.kind is NodeKind.ASTRONOMICAL and edge.position == 1)))
    assert graph.reproduce(lossy, first) != graph.recorded_fields(world.store.load(first))


# ------------------------------------------------------------------ AC5, AC7 unaccounted-for rows (CEO HOLD, PR #59)

class TwoCharts:
    """Two synthetic items on distinct charts of one entity, and the nodes each item's records justify."""

    def __init__(self, world):
        self.store = world.store
        natal = person().charts[0]
        other = dataclasses.replace(natal, label="other", origin=dataclasses.replace(
            natal.origin, local_datetime="1990-06-15T06:30:00", latitude=-5.0, longitude=70.0))
        owner = world.store.entities.persist(dataclasses.replace(person(), charts=(natal, other)))
        here, there = ChartReference(1, "natal"), ChartReference(1, "other")
        self.first = world.store.persist(world.item(entity=owner, chart=here))
        self.second = world.store.persist(world.item(entity=owner, chart=there))
        first, second = world.store.load(self.first), world.store.load(self.second)
        self.nodes = {"other input": graph.input_node(owner, there, other),
                      "natal chart": graph.chart_node(owner, here, "D1"),
                      "other chart": graph.chart_node(owner, there, "D1"),
                      "natal fact": graph.astronomical_node(owner, here, first.lineage.inputs[0]),
                      "other fact": graph.astronomical_node(owner, there, second.lineage.inputs[0]),
                      "other timing": graph.timing_node(owner, there, second.timing),
                      "first item": graph.evidence_node(self.first, first),
                      "second item": graph.evidence_node(self.second, second)}

    def plant(self, source, kind, target, position=0):
        self.store._db.execute("INSERT INTO graph_edges (source_key, kind, target_key, position) VALUES (?, ?, ?, ?)",
                               (self.nodes[source].key, kind, self.nodes[target].key, position))


FALSE_ANCESTRY = [("other input", "derives_from", "natal chart", 0), ("other input", "derives_from", "natal fact", 0),
                  ("other chart", "derives_from", "natal chart", 0), ("other timing", "derives_from", "first item", 0),
                  ("other fact", "applies_to", "first item", 1), ("second item", "derives_from", "first item", 0)]
READS = {"item_graph": lambda two, target: two.store.item_graph(two.first),
         "graph": lambda two, target: two.store.graph((two.first,)),
         "recorded_graph": lambda two, target: two.store.recorded_graph(),
         "incident": lambda two, target: two.store.incident(two.nodes[target].key),
         "reproduce": lambda two, target: two.store.reproduce(two.first)}


@pytest.mark.parametrize("planted", FALSE_ANCESTRY, ids=lambda case: f"{case[0]} to {case[2]}")
@pytest.mark.parametrize("read", READS)
def test_ac5_ac7_a_structurally_valid_unjustified_edge_is_refused_by_every_read(world, planted, read):
    two = TwoCharts(world)
    assert READS[read](two, planted[2]) is not None
    two.plant(*planted)
    with pytest.raises(StoreError, match="do not account for it"):
        READS[read](two, planted[2])


def test_ac5_ac7_an_item_the_planted_edge_does_not_reach_still_reads(world):
    two = TwoCharts(world)
    clean = two.store.item_graph(two.second)
    two.plant("other input", "derives_from", "natal chart")
    assert two.store.item_graph(two.second) == clean
    assert two.store.reproduce(two.second) == graph.recorded_fields(two.store.load(two.second))


def test_ac5_a_node_no_items_records_account_for_is_refused(world):
    two = TwoCharts(world)
    orphan = graph.make_node(NodeKind.TIMING, **{**two.nodes["other timing"].fields(), "label": "planted"})
    two.store._db.execute("INSERT INTO graph_nodes (node_key, kind, payload) VALUES (?, ?, ?)",
                          graph.node_to_row(orphan))
    with pytest.raises(StoreError, match="unaccounted node"):
        two.store.recorded_graph()


def test_ac7_a_missing_recorded_edge_is_refused_and_never_filled_in(world):
    two = TwoCharts(world)
    key = two.nodes["first item"].key
    two.store._db.execute("DROP TRIGGER graph_edges_no_delete")
    two.store._db.execute("DELETE FROM graph_edges WHERE target_key = ? AND source_key = ?",
                          (key, two.nodes["natal chart"].key))
    before = _counts(two.store)
    with pytest.raises(StoreError, match="missing (node|edge)"):
        two.store.item_graph(two.first)
    assert _counts(two.store) == before


def test_ac1_accounting_on_read_writes_nothing(world):
    two = TwoCharts(world)
    before = _counts(two.store)
    two.store.recorded_graph(), two.store.item_graph(two.first), two.store.incident(two.nodes["natal chart"].key)
    assert _counts(two.store) == before


def test_ac7_the_accounting_comparator_sees_each_kind_of_difference(world):
    two = TwoCharts(world)
    recorded = two.store.recorded_graph()
    expected = [_expected(two.store, two.first), _expected(two.store, two.second)]
    assert graph.unjustified_rows(recorded, expected) == ()
    assert any("missing node" in difference for difference in graph.unjustified_rows(Graph(nodes=(), edges=()), expected))
    false = Edge(source=two.nodes["other input"], kind=EdgeKind.DERIVES_FROM, target=two.nodes["natal chart"])
    moved = next(edge for edge in recorded.edges if edge.position == 0)
    for planted, reason in ((Graph(nodes=recorded.nodes, edges=recorded.edges + (false,)), "unaccounted edge"),
                            (Graph(nodes=recorded.nodes, edges=recorded.edges[1:]), "missing edge"),
                            (Graph(nodes=recorded.nodes, edges=tuple(
                                dataclasses.replace(edge, position=9) if edge is moved else edge
                                for edge in recorded.edges)), "unaccounted edge")):
        assert any(reason in difference for difference in graph.unjustified_rows(planted, expected))


def test_ac5_ac7_a_weakened_comparator_on_the_real_read_path_admits_the_false_ancestry(world):
    """The refusal comes from the comparator: weakened to check only edges into evidence nodes, which is all that
    reproduce() reads, the same real read accepts the planted false ancestry."""

    def direct_edges_only(recorded, expected):
        direct = lambda edges: {(edge.source.key, edge.kind, edge.target.key, edge.position) for edge in edges
                                if edge.target.kind is NodeKind.EVIDENCE}
        return tuple(direct(recorded.edges) ^ direct(edge for each in expected for edge in each.edges))

    two = TwoCharts(world)
    two.plant("other input", "derives_from", "natal chart")
    with pytest.raises(StoreError, match="do not account for it"):
        two.store.item_graph(two.first)
    two.store._unjustified = direct_edges_only
    accepted = two.store.item_graph(two.first)
    assert (two.nodes["other input"].key, two.nodes["natal chart"].key) in {
        (edge.source.key, edge.target.key) for edge in accepted.edges}
    assert two.store.reproduce(two.first) == graph.recorded_fields(two.store.load(two.first))


# ------------------------------------------------------------------ AC8 derived subjects

def test_ac8_a_derived_subjects_chart_derives_from_its_parent_chart(world):
    parent_chart = person().charts[0]
    annual = dataclasses.replace(parent_chart, label="annual 2010")
    link = ParentLink(parent=world.entity, parent_chart=parent_chart.label, derivation="annual chart")
    derived = world.store.entities.persist(Person(
        kind=EntityKind.PERSON, shape=Shape.DERIVED, charts=(annual,), applicable_domains=("career",),
        applicable_systems=("parashari",), provenance=PROV, data_class=person().data_class, parent=link))
    first = world.store.persist(world.item(entity=derived, chart=ChartReference(1, "annual 2010")))
    recorded = world.store.item_graph(first)
    parent = graph.parent_chart_node(link)
    child = graph.chart_node(derived, ChartReference(1, "annual 2010"), "D1")
    assert (parent.key, EdgeKind.DERIVES_FROM, child.key) in {(edge.source.key, edge.kind, edge.target.key)
                                                               for edge in recorded.edges}
    natal = world.store.persist(world.item())
    assert not [node for node in world.store.item_graph(natal).nodes if node.kind is NodeKind.DERIVED_CHART and
                node.fields()["entity_revision"] is None]


# ------------------------------------------------------------------ AC9 rule nodes from the registry

def test_ac9_the_rule_node_is_the_verified_registered_version(world):
    first = world.store.persist(world.item())
    rules = [node.fields() for node in world.store.item_graph(first).nodes if node.kind is NodeKind.RULE]
    published = rule_registry.pinned().rule_version(world.parashari.rule, 1, "base")
    assert rules == [{"rule": published.rule.value, "version": 1, "variant": "base",
                      "content_hash": published.spec.content_hash,
                      "knowledge_snapshot_hash": rule_registry.PINNED_SNAPSHOT_SHA256}]


def test_ac9_rows_from_another_snapshot_stay_as_recorded(world):
    from engine.evidence.evidence_store import rule_to_record
    stale = dataclasses.replace(world.parashari, spec=dataclasses.replace(
        world.parashari.spec, variant="stale", knowledge_snapshot_hash="f" * 64))
    world.store._db.execute("INSERT INTO registered_rule_versions (rule_id, version, variant, payload) VALUES "
                            "(?, ?, ?, ?)", (stale.rule.value, 1, "stale", json.dumps(rule_to_record(stale))))
    world.store.persist(world.item())
    assert stale in world.store.rule_versions(world.parashari.rule)


# ------------------------------------------------------------------ AC10 immutability

@pytest.mark.parametrize("statement", ["UPDATE graph_nodes SET payload = 'x'", "DELETE FROM graph_nodes",
                                       "UPDATE graph_edges SET position = 9", "DELETE FROM graph_edges"])
def test_ac10_graph_tables_refuse_update_and_delete_by_direct_sql(world, statement):
    world.store.persist(world.item())
    with pytest.raises(sqlite3.DatabaseError, match="append-only"):
        world.store._db.execute(statement)


def test_ac10_a_recomputation_leaves_the_originals_graph_untouched(world):
    first = world.store.persist(world.item())
    before = world.store.item_graph(first)
    again = world.store.persist(world.item(recomputes=first, facts=("Moon longitude", "Sun longitude")))
    assert world.store.item_graph(first) == before
    assert graph.evidence_node(again, world.store.load(again)).key not in {node.key for node in before.nodes}


# ------------------------------------------------------------------ AC11 nothing computed over the graph

def test_ac11_no_count_cut_score_weight_or_ratio_is_computed():
    forbidden = ("count", "independent", "cut", "score", "weight", "ratio", "flow", "disjoint", "menger", "path")
    for module in (GRAPH_MODULE, STORE_MODULE):
        tree = ast.parse(module.read_text(encoding="utf-8"))
        names = {node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
        graph_names = names if module == GRAPH_MODULE else {
            name for name in names if name in {"graph", "item_graph", "incident", "recorded_graph", "reproduce",
                                               "_write_graph", "_reaches", "_stored_node", "_graph_of"}}
        assert not [name for name in graph_names if any(word in name.lower() for word in forbidden)], module.name
    assert [field.name for field in dataclasses.fields(Graph)] == ["nodes", "edges"]


# ------------------------------------------------------------------ AC12, AC13 classification and holdouts

def test_ac12_classification_reads_no_graph():
    tree = ast.parse(STORE_MODULE.read_text(encoding="utf-8"))
    store = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "EvidenceStore")
    for method in store.body:
        if isinstance(method, ast.FunctionDef) and method.name in {"classify", "_ancestry", "_compatible", "relate",
                                                                    "relationships", "relationship_counts"}:
            text = ast.unparse(method)
            assert "graph" not in text and "provenance_graph" not in text, method.name


def test_ac12_correlated_is_still_never_assigned(world):
    first = world.store.persist(world.item())
    second = world.store.persist(world.item(facts=("Sun longitude",)))
    assert world.store.classify(first, second).dependency.value != "correlated"


def test_ac13_the_graph_code_and_the_store_import_no_ledger():
    for module in (GRAPH_MODULE, STORE_MODULE):
        tree = ast.parse(module.read_text(encoding="utf-8"))
        imported = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module} | \
            {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
        assert not [name for name in imported if "ledger" in name], module.name


# ------------------------------------------------------------------ AC14, AC16 fixed artifacts; scope

def test_ac14_the_pinned_registry_snapshot_is_unchanged():
    assert rule_registry.PINNED_SNAPSHOT_SHA256 == "ea8d185ff0786e1c2d68b8010b45b9721367e8e55efca49a4c1a4b8402643d0d"
    assert rule_registry.pinned().snapshot_sha256 == rule_registry.PINNED_SNAPSHOT_SHA256


def test_ac16_no_correlated_with_edge_and_no_prediction_or_llm_path():
    text = GRAPH_MODULE.read_text(encoding="utf-8")
    assert "CORRELATED_WITH =" not in text and not hasattr(EdgeKind, "CORRELATED_WITH")
    tree = ast.parse(text)
    imported = {alias.name.split(".")[0] for node in ast.walk(tree) if isinstance(node, ast.Import)
                for alias in node.names}
    assert not imported & {"openai", "anthropic", "requests", "urllib", "networkx", "graphlib"}
    assert not [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
                and any(word in node.name for word in ("predict", "forecast", "issue"))]


def test_ac16_every_item_in_the_graph_is_synthetic(world):
    first = world.store.persist(world.item())
    assert world.store.load(first).data_class.value == "synthetic"
