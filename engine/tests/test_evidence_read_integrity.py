"""The F1 correction (ADR-0124): every evidence read enforces the registered-rule and graph-integrity requirements, however
a row was written. Every record here is synthetic."""

from __future__ import annotations

import dataclasses
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "engine" / "tests"))

from test_evidence_wp_e4 import World, person  # noqa: E402

from engine.evidence import provenance_graph as graph  # noqa: E402
from engine.evidence import rule_registry  # noqa: E402
from engine.evidence.evidence import DependencyClass, RuleReference  # noqa: E402
from engine.evidence.evidence_identifiers import EvidenceId, RuleId  # noqa: E402
from engine.evidence.evidence_store import item_to_record, relationship_to_record, rule_to_record  # noqa: E402
from engine.evidence.evidence import Relationship  # noqa: E402
from engine.evidence.identifiers import EntityId  # noqa: E402
from engine.evidence.store import StoreError  # noqa: E402

FORGED = EvidenceId.from_number(500)
PARENT = EvidenceId.from_number(499)
UNISSUED = RuleId.from_number(999999)


class Forge:
    """Writes rows straight into the tables, around persist(), as a forger with database access would."""

    def __init__(self, world):
        self.world, self.store = world, world.store
        self.good = world.store.persist(world.item())

    def row(self, item, evidence_id=FORGED, payload_id=None, entity=None, recomputes=None):
        recorded = None if item.recomputes is None else item.recomputes.value
        self.store._db.execute(
            "INSERT INTO evidence_items (evidence_id, entity_id, recomputes, payload) VALUES (?, ?, ?, ?)",
            (evidence_id.value, entity or item.entity.value, recorded if recomputes is None else recomputes,
             json.dumps(item_to_record(payload_id or evidence_id, item))))

    def graph(self, item, rule, evidence_id=FORGED, linked=None):
        built = graph.record_graph(evidence_id, item, person().charts[0], None, rule, linked or {})
        for node in built.nodes:
            self.store._db.execute("INSERT OR IGNORE INTO graph_nodes (node_key, kind, payload) VALUES (?, ?, ?)",
                                   graph.node_to_row(node))
        for edge in built.edges:
            self.store._db.execute("INSERT OR IGNORE INTO graph_edges (source_key, kind, target_key, position) "
                                   "VALUES (?, ?, ?, ?)", (edge.source.key, edge.kind.value, edge.target.key,
                                                           edge.position))


def unregistered_without_a_graph(forge):
    forge.row(forge.world.item(rule=RuleReference(rule=UNISSUED, version=1, variant="base")))
    return "missing graph"


def _unregistered(forge, evidence_id=FORGED):
    rule = dataclasses.replace(forge.world.parashari, rule=UNISSUED)
    item = forge.world.item(rule=RuleReference(rule=UNISSUED, version=1, variant="base"))
    forge.row(item, evidence_id)
    forge.graph(item, rule, evidence_id)
    return item


def unregistered_with_a_matching_graph(forge):
    _unregistered(forge)
    return "is not registered"


def registered_without_a_graph(forge):
    forge.row(forge.world.item(facts=("Saturn longitude",)))
    return "missing graph"


def another_schools_rule(forge):
    kp = forge.world.kp
    item = forge.world.item(rule=RuleReference(rule=kp.rule, version=kp.version, variant=kp.spec.variant),
                            declared_strength=kp.spec.declared_strength)
    forge.row(item)
    forge.graph(item, kp)
    return "systems stay isolated"


def another_declared_strength(forge):
    item = forge.world.item(declared_strength="planted")
    forge.row(item)
    forge.graph(item, forge.world.parashari)
    return "declared strength"


def an_unpublished_variant_at_the_pinned_snapshot(forge):
    base = forge.world.parashari
    rule = dataclasses.replace(base, spec=dataclasses.replace(base.spec, variant="forged"))
    forge.store._db.execute("INSERT INTO registered_rule_versions (rule_id, version, variant, payload) VALUES "
                            "(?, ?, ?, ?)", (rule.rule.value, 1, "forged", json.dumps(rule_to_record(rule))))
    item = forge.world.item(rule=RuleReference(rule=rule.rule, version=1, variant="forged"))
    forge.row(item)
    forge.graph(item, rule)
    return "not published"


def a_payload_naming_another_item(forge):
    forge.row(forge.world.item(), payload_id=forge.good)
    return "does not match its row"


def an_entity_column_that_disagrees(forge):
    item = forge.world.item(facts=("Venus longitude",))
    forge.row(item, entity=EntityId.from_number(7).value)
    forge.graph(item, forge.world.parashari)
    return "does not match its row"


def a_recomputes_column_that_disagrees(forge):
    item = forge.world.item(facts=("Venus longitude",))
    forge.row(item, recomputes=forge.good.value)
    forge.graph(item, forge.world.parashari)
    return "does not match its row"


def a_forged_ancestor(forge):
    parent = _unregistered(forge, PARENT)
    item = forge.world.item(facts=("Mercury longitude",), derived_from=(PARENT,))
    forge.row(item)
    forge.graph(item, forge.world.parashari, linked={PARENT: parent})
    return "is not registered"


FORGERIES = [unregistered_without_a_graph, unregistered_with_a_matching_graph, registered_without_a_graph,
             another_schools_rule, another_declared_strength, an_unpublished_variant_at_the_pinned_snapshot,
             a_payload_naming_another_item, an_entity_column_that_disagrees, a_recomputes_column_that_disagrees,
             a_forged_ancestor]
READS = {"load": lambda forge: forge.store.load(FORGED),
         "evidence_ids": lambda forge: forge.store.evidence_ids(),
         "join": lambda forge: forge.store.join((forge.good, FORGED)),
         "counts": lambda forge: forge.store.counts(),
         "classify": lambda forge: forge.store.classify(forge.good, FORGED),
         "relate": lambda forge: forge.store.relate(forge.good, FORGED),
         "item_graph": lambda forge: forge.store.item_graph(FORGED),
         "reproduce": lambda forge: forge.store.reproduce(FORGED),
         "recorded_graph": lambda forge: forge.store.recorded_graph()}


@pytest.fixture()
def world(tmp_path):
    instance = World(tmp_path / "evidence.sqlite")
    yield instance
    instance.store.close()


def _rows(store):
    return tuple(store._db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] for table in (
        "evidence_items", "evidence_relationships", "graph_nodes", "graph_edges", "registered_rule_versions"))


@pytest.mark.parametrize("plant", FORGERIES, ids=lambda plant: plant.__name__)
def test_a_forged_row_is_refused_for_its_own_reason(world, plant):
    forge = Forge(world)
    reason = plant(forge)
    with pytest.raises(StoreError, match=reason):
        world.store.load(FORGED)


@pytest.mark.parametrize("read", READS)
@pytest.mark.parametrize("plant", FORGERIES, ids=lambda plant: plant.__name__)
def test_every_evidence_read_refuses_a_forged_row(world, plant, read):
    forge = Forge(world)
    plant(forge)
    before = _rows(world.store)
    with pytest.raises(StoreError):
        READS[read](forge)
    assert _rows(world.store) == before


@pytest.mark.parametrize("plant", FORGERIES, ids=lambda plant: plant.__name__)
def test_a_forged_row_does_not_take_a_legitimate_item_down_with_it(world, plant):
    forge = Forge(world)
    plant(forge)
    assert world.store.load(forge.good) == world.item()
    assert world.store.reproduce(forge.good) == graph.recorded_fields(world.item())


def test_persist_refuses_new_evidence_naming_a_forged_parent(world):
    forge = Forge(world)
    _unregistered(forge, PARENT)
    with pytest.raises(StoreError, match="is not registered"):
        world.store.persist(world.item(derived_from=(PARENT,)))
    assert world.store.issued_count("EVD") == 1


def test_recomputations_refuses_a_forged_recomputation_of_a_legitimate_item(world):
    forge = Forge(world)
    forge.row(world.item(rule=RuleReference(rule=UNISSUED, version=1, variant="base"), recomputes=forge.good))
    with pytest.raises(StoreError):
        world.store.recomputations(forge.good)


@pytest.mark.parametrize("read", ["relationships", "relationship_counts"])
def test_a_recorded_relationship_naming_a_forged_item_is_refused(world, read):
    forge = Forge(world)
    unregistered_without_a_graph(forge)
    record = relationship_to_record(Relationship(forge.good, FORGED, DependencyClass.UNKNOWN, False, "planted"))
    world.store._db.execute("INSERT INTO evidence_relationships (first_id, second_id, payload) VALUES (?, ?, ?)",
                            (forge.good.value, FORGED.value, json.dumps(record)))
    with pytest.raises(StoreError):
        {"relationships": world.store.relationships, "relationship_counts": world.store.relationship_counts}[read]()


# ------------------------------------------------------------------ legitimate records stay readable

def _chain(world):
    first = world.store.persist(world.item(facts=("Sun longitude", "Moon longitude")))
    second = world.store.persist(world.item(facts=("Mars longitude",), derived_from=(first,)))
    third = world.store.persist(world.item(facts=("Moon longitude",), recomputes=first))
    return first, second, third


def test_legitimate_chains_read_through_every_path(world):
    ids = list(_chain(world))
    store = world.store
    assert store.evidence_ids() == ids and [store.load(value) for value in ids] == store.join(ids)
    assert store.recomputations(ids[0]) == [ids[2]] and set(store.counts()["total"]) == set(ids)
    store.relate(ids[0], ids[1])
    assert len(store.relationships()) == 1 and store.classify(ids[0], ids[1]).dependency is DependencyClass.DERIVED
    assert {node.key for node in store.graph(ids).nodes} == {node.key for node in store.recorded_graph().nodes}


def test_evidence_under_an_earlier_snapshot_stays_readable_but_new_evidence_is_refused(world, monkeypatch):
    ids = list(_chain(world))
    before = [world.store.load(value) for value in ids]
    later = rule_registry.RuleRegistry(rule_registry.pinned().rules(), "0" * 64)
    monkeypatch.setattr(rule_registry, "pinned", lambda: later)
    assert [world.store.load(value) for value in ids] == before and world.store.evidence_ids() == ids
    assert world.store.recorded_graph().nodes and world.store.counts()["total"] == tuple(ids)
    with pytest.raises(StoreError, match="another snapshot"):
        world.store.persist(world.item())


# ------------------------------------------------------------------ each check does the refusing

WEAKENED = {
    "_admitted_rule": (unregistered_with_a_matching_graph, lambda world: lambda item: dataclasses.replace(
        world.parashari, rule=UNISSUED)),
    "_require_fit": (another_declared_strength, lambda world: lambda item, rule: None),
    "_require_published": (an_unpublished_variant_at_the_pinned_snapshot, lambda world: lambda item, rule, registry: None),
    "_require_row_identity": (an_entity_column_that_disagrees, lambda world: lambda *row: None),
    "graph": (registered_without_a_graph, lambda world: lambda ids: None),
}


@pytest.mark.parametrize("check", WEAKENED)
def test_weakening_one_real_check_lets_the_same_read_accept_the_forgery(world, check):
    plant, weak = WEAKENED[check]
    forge = Forge(world)
    plant(forge)
    with pytest.raises(StoreError):
        world.store.load(FORGED)
    world.store.__setattr__(check, weak(world))
    assert world.store.load(FORGED) is not None


def test_a_check_demanding_the_snapshot_in_force_would_refuse_legitimate_history(world, monkeypatch):
    first = world.store.persist(world.item())
    later = rule_registry.RuleRegistry(rule_registry.pinned().rules(), "0" * 64)
    monkeypatch.setattr(rule_registry, "pinned", lambda: later)
    assert world.store.load(first) == world.item()

    def too_strict(item):
        rule = world.store.rule_version(item.rule)
        if rule.spec.knowledge_snapshot_hash != later.snapshot_sha256:
            raise StoreError("another snapshot")
        return rule

    world.store._admitted_rule = too_strict
    with pytest.raises(StoreError, match="another snapshot"):
        world.store.load(first)
