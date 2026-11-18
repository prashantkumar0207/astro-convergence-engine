"""The F2 correction (ADR-0125): a persisted relationship is returned only if its immutable source evidence supports its
dependency, conflict flag, basis and identities, however the row was written. Every record here is synthetic."""

from __future__ import annotations

import copy
import dataclasses
import json
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "engine" / "tests"))
sys.path.insert(0, str(ROOT / "scripts"))

import certify_evidence_foundations as certifier  # noqa: E402
from test_evidence_wp_e4 import CALC, World  # noqa: E402

from engine.evidence import rule_registry  # noqa: E402
from engine.evidence.evidence import DependencyClass, Polarity, ProducingSystem, RuleReference  # noqa: E402
from engine.evidence.evidence_identifiers import EvidenceId, RuleId  # noqa: E402
from engine.evidence.evidence_store import EvidenceStore, item_to_record, relationship_to_record  # noqa: E402
from engine.evidence.store import StoreError  # noqa: E402

KP = ProducingSystem.KP
PAIRS = ("derived", "shared origin", "independent", "independent and conflicting", "unknown")
TRUE_CLASS = {"derived": DependencyClass.DERIVED, "shared origin": DependencyClass.SHARED_ORIGIN,
              "independent": DependencyClass.INDEPENDENT, "independent and conflicting": DependencyClass.INDEPENDENT,
              "unknown": DependencyClass.UNKNOWN}
UNSUPPORTED = "not supported by its source evidence"


class Pairs:
    """One legitimate pair of items for each relationship the store can classify."""

    def __init__(self, world):
        self.world, self.store = world, world.store
        put = lambda *args, **changes: world.store.persist(world.item(*args, **changes))
        sun = put(facts=("Sun longitude",))
        jupiter = put(facts=("Jupiter longitude",))
        venus = put(facts=("Venus longitude",))
        self.ids = {"derived": (sun, put(facts=("Mars longitude",), derived_from=(sun,))),
                    "shared origin": (jupiter, put(KP, facts=("Jupiter longitude",))),
                    "independent": (venus, put(KP, facts=("Mercury longitude",))),
                    "independent and conflicting": (venus, put(KP, facts=("Saturn longitude",),
                                                               polarity=Polarity.NEGATIVE)),
                    "unknown": (put(facts=("Rahu longitude",)), put(facts=("Ketu longitude",)))}

    def record(self, name):
        return copy.deepcopy(relationship_to_record(self.store.classify(*self.ids[name])))

    def plant(self, record, first=None, second=None):
        data = record["relationship"] if isinstance(record, dict) and "relationship" in record else {}
        payload = record if isinstance(record, str) else json.dumps(record)
        self.store._db.execute("INSERT INTO evidence_relationships (first_id, second_id, payload) VALUES (?, ?, ?)",
                               (first or data["first"], second or data["second"], payload))


@pytest.fixture()
def world(tmp_path):
    instance = World(tmp_path / "evidence.sqlite")
    yield instance
    instance.store.close()


def _refused(store, match):
    for read in (store.relationships, store.relationship_counts):
        with pytest.raises(StoreError, match=match):
            read()


FORGED_CLASSES = [(pair, kind) for pair in PAIRS for kind in DependencyClass if kind is not TRUE_CLASS[pair]]


@pytest.mark.parametrize("pair,kind", FORGED_CLASSES, ids=lambda value: getattr(value, "value", value))
def test_a_forged_dependency_is_refused(world, pair, kind):
    pairs = Pairs(world)
    record = pairs.record(pair)
    record["relationship"]["dependency"] = kind.value
    pairs.plant(record)
    _refused(world.store, "measured evidence" if kind is DependencyClass.CORRELATED else UNSUPPORTED)


@pytest.mark.parametrize("pair", PAIRS)
def test_a_forged_conflict_flag_is_refused(world, pair):
    pairs = Pairs(world)
    record = pairs.record(pair)
    record["relationship"]["conflicting"] = not record["relationship"]["conflicting"]
    pairs.plant(record)
    _refused(world.store, "conflict flag")


@pytest.mark.parametrize("pair", PAIRS)
def test_a_forged_explanation_is_refused(world, pair):
    pairs = Pairs(world)
    record = pairs.record(pair)
    record["relationship"]["basis"] = "planted explanation"
    pairs.plant(record)
    _refused(world.store, "basis")


def _swapped(pairs):
    record = pairs.record("derived")
    first, second = pairs.ids["derived"]
    data = record["relationship"]
    data["first"], data["second"] = data["second"], data["first"]
    pairs.plant(record, first.value, second.value)


def _other_columns(pairs):
    pairs.plant(pairs.record("derived"), second=pairs.ids["unknown"][0].value)


def _absent_item(pairs):
    record = pairs.record("derived")
    record["relationship"]["second"] = EvidenceId.from_number(900).value
    pairs.plant(record)


def _same_item_twice(pairs):
    record = pairs.record("derived")
    record["relationship"]["second"] = record["relationship"]["first"]
    pairs.plant(record)


def _forged_item(pairs):
    forged = EvidenceId.from_number(901)
    item = pairs.world.item(rule=RuleReference(rule=RuleId.from_number(999999), version=1, variant="base"))
    pairs.store._db.execute("INSERT INTO evidence_items (evidence_id, entity_id, recomputes, payload) VALUES (?, ?, NULL, ?)",
                            (forged.value, item.entity.value, json.dumps(item_to_record(forged, item))))
    record = pairs.record("derived")
    record["relationship"]["second"] = forged.value
    pairs.plant(record)


def _differing_provenance(pairs):
    other = dataclasses.replace(CALC, ayanamsa_mode=CALC.ayanamsa_mode + 1)
    item = pairs.store.persist(pairs.world.item(facts=("Uranus longitude",), provenance=other))
    record = pairs.record("derived")
    record["relationship"]["second"] = item.value
    pairs.plant(record)


def _malformed(pairs):
    first, second = pairs.ids["derived"]
    pairs.plant("{not json", first.value, second.value)


def _field(change):
    def plant(pairs):
        record = pairs.record("derived")
        change(record)
        pairs.plant(record, *[value.value for value in pairs.ids["derived"]])
    return plant


IDENTITY_FORGERIES = {
    "the payload names the pair in the other order": (_swapped, "does not match its row"),
    "the row's columns name another item": (_other_columns, "does not match its row"),
    "an item that does not exist": (_absent_item, "no such evidence item"),
    "one item related to itself": (_same_item_twice, "two different evidence items"),
    "an item that fails the read checks": (_forged_item, "missing graph"),
    "items whose calculation provenance differs": (_differing_provenance, "calculation provenance"),
    "a payload that is not JSON": (_malformed, "is refused"),
    "another schema": (_field(lambda record: record.update(schema="v0")), "not a relationship record"),
    "a missing field": (_field(lambda record: record["relationship"].pop("basis")), "only its model fields"),
    "an extra field": (_field(lambda record: record["relationship"].update(score=1)), "only its model fields"),
    "an undeclared class": (_field(lambda record: record["relationship"].update(dependency="proven")), "is refused"),
    "a conflict flag that is not boolean": (_field(lambda record: record["relationship"].update(conflicting="no")),
                                            "conflict is recorded"),
    "an empty explanation": (_field(lambda record: record["relationship"].update(basis=" ")), "basis"),
}


@pytest.mark.parametrize("case", IDENTITY_FORGERIES)
def test_an_invalid_record_is_refused_for_its_own_reason(world, case):
    plant, reason = IDENTITY_FORGERIES[case]
    pairs = Pairs(world)
    plant(pairs)
    _refused(world.store, reason)


# ------------------------------------------------------------------ legitimate relationships stay readable

def test_every_legitimate_relationship_reads_back_as_recorded(world):
    pairs = Pairs(world)
    recorded = [world.store.relate(*pairs.ids[pair]) for pair in PAIRS]
    assert world.store.relationships() == recorded
    assert [item.dependency for item in recorded] == [TRUE_CLASS[pair] for pair in PAIRS]
    counts = world.store.relationship_counts()
    assert counts[DependencyClass.UNKNOWN.value] == (pairs.ids["unknown"],)
    assert counts["conflicting"] == (pairs.ids["independent and conflicting"],)


def test_unknown_stays_unknown_and_is_never_treated_as_independent(world):
    pairs = Pairs(world)
    world.store.relate(*pairs.ids["unknown"])
    assert world.store.relationships()[0].dependency is DependencyClass.UNKNOWN
    assert world.store.relationship_counts()[DependencyClass.INDEPENDENT.value] == ()


def test_history_is_appended_and_both_orders_of_a_pair_are_legitimate(world):
    pairs = Pairs(world)
    first, second = pairs.ids["shared origin"]
    records = [world.store.relate(first, second), world.store.relate(first, second), world.store.relate(second, first)]
    assert world.store.relationships() == records


def test_a_relationship_survives_later_evidence_a_reopen_and_a_later_snapshot(world, tmp_path, monkeypatch):
    pairs = Pairs(world)
    recorded = world.store.relate(*pairs.ids["derived"])
    world.store.persist(world.item(facts=("Neptune longitude",), derived_from=(pairs.ids["derived"][1],)))
    assert world.store.relationships() == [recorded]
    with EvidenceStore(tmp_path / "evidence.sqlite") as reopened:
        assert reopened.relationships() == [recorded]
    later = rule_registry.RuleRegistry(rule_registry.pinned().rules(), "0" * 64)
    monkeypatch.setattr(rule_registry, "pinned", lambda: later)
    assert world.store.relationships() == [recorded]


def test_reading_writes_nothing_and_history_stays_append_only(world):
    pairs = Pairs(world)
    world.store.relate(*pairs.ids["derived"])
    world.store.relationships(), world.store.relationship_counts()
    assert world.store._db.execute("SELECT COUNT(*) FROM evidence_relationships").fetchone()[0] == 1
    for statement in ("UPDATE evidence_relationships SET payload = 'x'", "DELETE FROM evidence_relationships"):
        with pytest.raises(sqlite3.DatabaseError, match="append-only"):
            world.store._db.execute(statement)


# ------------------------------------------------------------------ each check does the refusing

def _ignoring(field):
    return lambda recorded, supported: tuple(name for name, mine, theirs in (
        ("dependency", recorded.dependency, supported.dependency),
        ("conflict flag", recorded.conflicting, supported.conflicting),
        ("basis", recorded.basis, supported.basis)) if mine != theirs and name != field)


WEAKENED = {"dependency": lambda data: data.update(dependency="independent"),
            "conflict flag": lambda data: data.update(conflicting=True),
            "basis": lambda data: data.update(basis="planted explanation")}


@pytest.mark.parametrize("field", WEAKENED)
def test_a_comparator_ignoring_one_field_lets_the_same_read_accept_the_forgery(world, field):
    pairs = Pairs(world)
    record = pairs.record("derived")
    WEAKENED[field](record["relationship"])
    pairs.plant(record)
    with pytest.raises(StoreError, match=UNSUPPORTED):
        world.store.relationships()
    world.store._unsupported_fields = _ignoring(field)
    assert len(world.store.relationships()) == 1


def test_weakening_the_row_identity_check_lets_the_same_read_accept_the_forgery(world):
    pairs = Pairs(world)
    _other_columns(pairs)
    with pytest.raises(StoreError, match="does not match its row"):
        world.store.relationships()
    world.store._require_relationship_row = lambda *row: None
    assert len(world.store.relationships()) == 1


def _refuse_unknown(recorded, supported):
    return ("dependency",) if recorded.dependency is DependencyClass.UNKNOWN else ()


REAL_GATE_CONTROLS = {
    "no support check": ("_unsupported_fields", staticmethod(lambda recorded, supported: ())),
    "dependency ignored": ("_unsupported_fields", staticmethod(_ignoring("dependency"))),
    "conflict flag ignored": ("_unsupported_fields", staticmethod(_ignoring("conflict flag"))),
    "basis ignored": ("_unsupported_fields", staticmethod(_ignoring("basis"))),
    "no row identity check": ("_require_relationship_row", staticmethod(lambda *row: None)),
    "legitimate UNKNOWN refused": ("_unsupported_fields", staticmethod(_refuse_unknown)),
}


@pytest.mark.parametrize("control", REAL_GATE_CONTROLS)
def test_the_real_gate_t_fails_when_a_store_check_is_weakened(monkeypatch, control):
    name, weakened = REAL_GATE_CONTROLS[control]
    monkeypatch.setattr(EvidenceStore, name, weakened)
    with pytest.raises((SystemExit, StoreError)):
        certifier.gate_t_relationship_integrity()


def test_the_real_gate_t_passes_on_the_real_store():
    result = certifier.gate_t_relationship_integrity()
    assert result["refusals_verified"] >= 80 and result["controls_rejected"] >= 6
