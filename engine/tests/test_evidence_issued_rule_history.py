"""The L1 correction (ADR-0127): a rule version recorded under an earlier snapshot is read only as what the governed records
prove: an issued RUL, under its school, and a version still published unchanged. Every record here is synthetic."""

from __future__ import annotations

import dataclasses
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "engine" / "tests"))
sys.path.insert(0, str(ROOT / "scripts"))

import certify_evidence_foundations as certifier  # noqa: E402
from test_evidence_read_integrity import FORGED, READS, Forge  # noqa: E402
from test_evidence_wp_e4 import World  # noqa: E402

from engine.evidence import provenance_graph as graph  # noqa: E402
from engine.evidence import rule_registry  # noqa: E402
from engine.evidence.evidence import ProducingSystem, RuleReference  # noqa: E402
from engine.evidence.evidence_identifiers import RuleId  # noqa: E402
from engine.evidence.evidence_store import EvidenceStore, rule_to_record  # noqa: E402
from engine.evidence.store import StoreError  # noqa: E402

EARLIER = "f" * 64
PINNED = rule_registry.pinned()
FIRST = RuleId.from_number(1)
VARIANTS = PINNED.by_key("synthetic.parashari.moon-in-fourth")


def published(rule, version, variant):
    return PINNED.rule_version(rule, version, variant)


def earlier(rule_version, **spec):
    """The same rule version as recorded under an earlier snapshot, with any planted change."""

    return dataclasses.replace(rule_version, spec=dataclasses.replace(
        rule_version.spec, **{"knowledge_snapshot_hash": EARLIER, **spec}))


def plant(forge, rule, system=ProducingSystem.PARASHARI):
    forge.store._db.execute("INSERT INTO registered_rule_versions (rule_id, version, variant, payload) VALUES "
                            "(?, ?, ?, ?)", (rule.rule.value, rule.version, rule.spec.variant,
                                             json.dumps(rule_to_record(rule))))
    item = forge.world.item(system, rule=RuleReference(rule=rule.rule, version=rule.version, variant=rule.spec.variant),
                            declared_strength=rule.spec.declared_strength)
    forge.row(item)
    forge.graph(item, rule)
    return item


def a_rul_never_issued(forge):
    plant(forge, dataclasses.replace(earlier(published(FIRST, 2, "base")), rule=RuleId.from_number(999999)))
    return "never issued"


def a_school_the_history_contradicts(forge):
    plant(forge, earlier(published(VARIANTS, 1, "reading-a"), school=ProducingSystem.KP), ProducingSystem.KP)
    return "by the allocation history"


def a_version_never_published(forge):
    plant(forge, dataclasses.replace(earlier(published(FIRST, 2, "base")), version=99))
    return "never withdrawn"


def a_variant_never_published(forge):
    plant(forge, earlier(published(FIRST, 1, "base"), variant="forged"))
    return "never withdrawn"


def rewritten_content(forge):
    plant(forge, earlier(published(FIRST, 2, "base"), content_hash="e" * 64))
    return "contradicts its immutable publication"


def a_rewritten_declared_strength(forge):
    plant(forge, earlier(published(VARIANTS, 1, "reading-b"), declared_strength="planted"))
    return "contradicts its immutable publication"


FORGERIES = [a_rul_never_issued, a_school_the_history_contradicts, a_version_never_published, a_variant_never_published,
             rewritten_content, a_rewritten_declared_strength]


@pytest.fixture()
def world(tmp_path):
    instance = World(tmp_path / "evidence.sqlite")
    yield instance
    instance.store.close()


@pytest.mark.parametrize("plant_forgery", FORGERIES, ids=lambda case: case.__name__)
def test_a_forged_historical_rule_is_refused_for_its_own_reason(world, plant_forgery):
    forge = Forge(world)
    reason = plant_forgery(forge)
    with pytest.raises(StoreError, match=reason):
        world.store.load(FORGED)


@pytest.mark.parametrize("read", READS)
@pytest.mark.parametrize("plant_forgery", FORGERIES, ids=lambda case: case.__name__)
def test_every_evidence_read_refuses_a_forged_historical_rule(world, plant_forgery, read):
    forge = Forge(world)
    plant_forgery(forge)
    with pytest.raises(StoreError):
        READS[read](forge)


@pytest.mark.parametrize("plant_forgery", FORGERIES, ids=lambda case: case.__name__)
def test_a_forged_historical_rule_does_not_take_a_legitimate_item_down(world, plant_forgery):
    forge = Forge(world)
    plant_forgery(forge)
    assert world.store.load(forge.good) == world.item()


# ------------------------------------------------------------------ genuine history stays readable

def test_a_genuinely_issued_version_recorded_under_an_earlier_snapshot_reads_through_every_path(world):
    forge = Forge(world)
    item = plant(forge, earlier(published(FIRST, 2, "base")))
    store = world.store
    assert store.load(FORGED) == item and FORGED in store.evidence_ids()
    assert store.join((forge.good, FORGED)) == [world.item(), item] and set(store.counts()["total"]) == {forge.good, FORGED}
    assert store.reproduce(FORGED) == graph.recorded_fields(item) and store.recorded_graph().nodes
    store.relate(forge.good, FORGED)
    assert len(store.relationships()) == 1


def test_history_does_not_need_the_current_snapshot_hash(world, monkeypatch):
    ids = [world.store.persist(world.item()), world.store.persist(world.item(facts=("Sun longitude",)))]
    before = [world.store.load(value) for value in ids]
    later = rule_registry.RuleRegistry(PINNED.rules(), "0" * 64)
    monkeypatch.setattr(rule_registry, "pinned", lambda: later)
    assert [world.store.load(value) for value in ids] == before and world.store.evidence_ids() == ids


# ------------------------------------------------------------------ each check does the refusing

def test_without_the_publication_check_a_never_published_version_is_admitted(world):
    forge = Forge(world)
    a_version_never_published(forge)
    with pytest.raises(StoreError, match="never withdrawn"):
        world.store.load(FORGED)
    world.store._require_unchanged_publication = lambda rule, registry: None
    assert world.store.load(FORGED).rule.version == 99


def test_the_history_and_publication_checks_are_layered(world):
    forge = Forge(world)
    a_rul_never_issued(forge)
    world.store._require_issued = lambda rule, issued: None
    with pytest.raises(StoreError, match="never withdrawn"):
        world.store.load(FORGED)
    world.store._require_unchanged_publication = lambda rule, registry: None
    assert world.store.load(FORGED).rule.rule == RuleId.from_number(999999)


def test_a_check_demanding_the_current_snapshot_would_refuse_genuine_history(world):
    forge = Forge(world)
    plant(forge, earlier(published(FIRST, 2, "base")))
    assert world.store.load(FORGED) is not None

    def too_strict(item):
        rule = world.store.rule_version(item.rule)
        if rule.spec.knowledge_snapshot_hash != PINNED.snapshot_sha256:
            raise StoreError("another snapshot")
        return rule

    world.store._admitted_rule = too_strict
    with pytest.raises(StoreError, match="another snapshot"):
        world.store.load(FORGED)


def _too_strict(self, item):
    rule = self.rule_version(item.rule)
    if rule.spec.knowledge_snapshot_hash != rule_registry.pinned().snapshot_sha256:
        raise StoreError("another snapshot")
    return rule


REAL_GATE_CONTROLS = {
    "no allocation-history check": ("_require_issued", staticmethod(lambda rule, issued: None)),
    "no publication check": ("_require_unchanged_publication", staticmethod(lambda rule, registry: None)),
    "a check that refuses genuine history": ("_admitted_rule", _too_strict),
}


@pytest.mark.parametrize("control", REAL_GATE_CONTROLS)
def test_the_real_gate_u_fails_when_a_store_check_is_weakened(monkeypatch, control):
    name, weakened = REAL_GATE_CONTROLS[control]
    monkeypatch.setattr(EvidenceStore, name, weakened)
    with pytest.raises((SystemExit, StoreError)):
        certifier.gate_u_historical_rule_integrity()


def test_the_real_gate_u_passes_on_the_real_store():
    result = certifier.gate_u_historical_rule_integrity()
    assert result["forgeries"] == len(FORGERIES) and result["refusals_verified"] >= 54 and result["controls_rejected"] >= 4
