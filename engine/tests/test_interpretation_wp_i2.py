"""WP-I2 (ADR-0134): explicitly untimed natal evidence, projected from a verified, fired application record and
re-derived from the entity chart by the certified kernel on every write and read. Synthetic charts only."""

import dataclasses
import json
import sys
from pathlib import Path

import pytest

from engine.evidence import provenance_graph, rule_registry
from engine.evidence.entity import (ChartCandidate, DataClass, EntityKind, OriginCertainty, OriginMoment, Person,
                                    RecordProvenance, Shape)
from engine.evidence.evidence import (ChartReference, DependencyClass, Domain, EvidenceModelError, Polarity,
                                      TimingContext, TimingKind, UntimedBasis, UntimedNatal)
from engine.evidence.evidence_identifiers import RuleId
from engine.evidence.evidence_store import (SCHEMA_VERSION, UNTIMED_SCHEMA_VERSION, EvidenceStore, item_from_record,
                                            item_to_record)
from engine.evidence.store import StoreError
from engine.interpretation import application
from engine.projection import natal

PROV = RecordProvenance(source="WP-I2 test fixture", method="constructed", schema_version="h1-v2")
FIRING, SUBSTITUTE, QUIET = "2021-01-28T05:40:00", "2021-01-29T05:40:00", "1983-06-08T11:30:00"
ONE, THREE = RuleId.from_number(1), RuleId.from_number(3)
AT = ChartReference(1, "natal")


def _chart(when):
    return ChartCandidate(label="natal", origin=OriginMoment(local_datetime=when, timezone="UTC",
                                                             timezone_source="fixture", latitude=13.0827,
                                                             longitude=80.2707, precision="second"),
                          origin_certainty=OriginCertainty.REPORTED, provenance=PROV)


def _person(when):
    return Person(kind=EntityKind.PERSON, shape=Shape.ORIGIN, charts=(_chart(when),), applicable_domains=("synthetic",),
                  applicable_systems=("parashari",), provenance=PROV, data_class=DataClass.SYNTHETIC)


@pytest.fixture
def world(tmp_path):
    store = natal.natal_store(tmp_path / "evidence.sqlite")
    owner = store.entities.persist(_person(FIRING))
    registry = rule_registry.pinned()
    for rule, version, variant in ((ONE, 1, "base"), (ONE, 2, "base"), (THREE, 1, "reading-a"), (THREE, 1, "reading-b")):
        store.register_rule(registry.rule_version(rule, version, variant))
    chart = natal.kernel_chart(natal.entity_chart(store, owner, AT))
    yield store, owner, chart, tmp_path / "evidence.sqlite"
    store.close()


def _project(store, owner, chart, rule, version, index=0):
    record = application.apply_rule(chart, rule, version).records[index]
    return natal.project(store, record, chart, owner, AT)


def test_untimed_basis_is_closed_and_untimed_items_are_jataka_parashari_d1(world):
    store, owner, chart, _path = world
    with pytest.raises(EvidenceModelError, match="NATAL_PLACEMENT"):
        UntimedNatal(basis="unknown")
    item = store.load(_project(store, owner, chart, ONE, 1))
    assert item.timing == UntimedNatal(UntimedBasis.NATAL_PLACEMENT)
    with pytest.raises(EvidenceModelError, match="D1 chart"):
        dataclasses.replace(item, domain=Domain.MUHURTA)
    with pytest.raises(EvidenceModelError, match="D1 chart"):
        dataclasses.replace(item, chart_context=dataclasses.replace(item.chart_context, varga="D9"))


def test_untimed_records_are_v4_and_dated_records_stay_v3(world):
    store, owner, chart, _path = world
    untimed_id = _project(store, owner, chart, ONE, 1)
    untimed = store.load(untimed_id)
    record = item_to_record(untimed_id, untimed)
    assert record["schema"] == UNTIMED_SCHEMA_VERSION
    assert record["evidence"]["timing"] == {"kind": "untimed_natal", "basis": "natal_placement"}
    dated = dataclasses.replace(untimed, timing=TimingContext(TimingKind.WINDOW, "w", "2010-01-01", "2011-01-01"))
    dated_id = store.persist(dated)
    dated_record = item_to_record(dated_id, store.load(dated_id))
    assert dated_record["schema"] == SCHEMA_VERSION == "ace-evidence-store-v3"
    assert dated_record["evidence"]["timing"] == {"kind": "window", "label": "w", "start": "2010-01-01",
                                                  "end": "2011-01-01"}
    with pytest.raises(StoreError):
        item_from_record({**record, "schema": SCHEMA_VERSION})
    with pytest.raises(StoreError):
        item_from_record({**dated_record, "schema": UNTIMED_SCHEMA_VERSION})


def test_a_plain_store_refuses_untimed_items_on_write_and_read(world):
    store, owner, chart, path = world
    untimed_id = _project(store, owner, chart, ONE, 1)
    plain = EvidenceStore(path)
    with pytest.raises(StoreError, match="holding the natal verifier"):
        plain.load(untimed_id)
    with pytest.raises(StoreError, match="holding the natal verifier"):
        plain.persist(store.load(untimed_id))
    plain.close()


def test_forged_facts_and_rows_are_refused_on_write_and_read(world):
    store, owner, chart, _path = world
    untimed_id = _project(store, owner, chart, ONE, 1)
    item = store.load(untimed_id)
    first = item.lineage.inputs[0]
    forged = dataclasses.replace(item, lineage=dataclasses.replace(item.lineage, inputs=(
        dataclasses.replace(first, fact=first.fact.replace("lord_house 10", "lord_house 3")),)))
    with pytest.raises(StoreError, match="certified natal evidence"):
        store.persist(forged)
    with pytest.raises(StoreError, match="certified natal evidence"):
        store.persist(dataclasses.replace(item, polarity=Polarity.NEGATIVE))
    row = item_to_record(untimed_id, forged)
    store._db.execute("INSERT INTO evidence_items (evidence_id, entity_id, recomputes, payload) VALUES (?, ?, ?, ?)",
                      ("EVD-0000000099", owner.value, None,
                       json.dumps({**row, "id": "EVD-0000000099"}, sort_keys=True, separators=(",", ":"))))
    from engine.evidence.evidence_identifiers import EvidenceId
    with pytest.raises(StoreError, match="certified natal evidence"):
        store.load(EvidenceId("EVD-0000000099"))


def test_projection_refuses_substituted_charts_and_rules_that_did_not_fire(world):
    store, owner, chart, _path = world
    substitute = natal.kernel_chart(_chart(SUBSTITUTE))
    with pytest.raises(natal.ProjectionError, match="kernel's recomputation"):
        natal.project(store, application.apply_rule(substitute, ONE, 1).records[0], substitute, owner, AT)
    quiet_owner = store.entities.persist(_person(QUIET))
    quiet_chart = natal.kernel_chart(natal.entity_chart(store, quiet_owner, AT))
    quiet = application.apply_rule(quiet_chart, ONE, 1).records[0]
    assert not quiet.fired
    with pytest.raises(natal.ProjectionError, match="did not fire"):
        natal.project(store, quiet, quiet_chart, quiet_owner, AT)


def test_d6c_variants_disagree_without_independence_or_timing_conflict(world):
    store, owner, chart, _path = world
    reading_a = _project(store, owner, chart, THREE, 1, 0)
    reading_b = _project(store, owner, chart, THREE, 1, 1)
    base = _project(store, owner, chart, ONE, 1)
    readings = store.classify(reading_a, reading_b)
    assert readings.dependency is DependencyClass.SHARED_ORIGIN and readings.conflicting
    other = store.classify(base, reading_b)
    assert not other.conflicting and other.dependency is not DependencyClass.INDEPENDENT
    dated = store.persist(dataclasses.replace(store.load(base), polarity=Polarity.NEGATIVE, timing=TimingContext(
        TimingKind.WINDOW, "w", "2010-01-01", "2011-01-01")))
    assert not store.classify(dated, base).conflicting


def test_the_graph_records_one_untimed_node_and_reproduces_the_item(world):
    store, owner, chart, _path = world
    untimed_id = _project(store, owner, chart, ONE, 2)
    kinds = [node.kind for node in store.item_graph(untimed_id).nodes]
    assert kinds.count(provenance_graph.NodeKind.UNTIMED) == 1 and provenance_graph.NodeKind.TIMING not in kinds
    assert store.reproduce(untimed_id) == provenance_graph.recorded_fields(store.load(untimed_id))


def test_gate_z_passes_with_its_refusals_and_controls():
    root = Path(__file__).resolve().parents[2]
    sys.path[:0] = [str(root), str(root / "scripts")]
    import certify_evidence_foundations

    result = certify_evidence_foundations.gate_z_untimed_natal_evidence()
    assert (result["refusals_verified"], result["legitimate_reads_preserved"], result["controls_rejected"]) == (33, 7, 10)
