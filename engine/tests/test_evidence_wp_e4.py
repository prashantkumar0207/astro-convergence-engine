"""WP-E4 acceptance tests (ADR-0119 s5): the evidence model, its store, the EVD and RUL families, joins,
decomposable aggregates and structural relationships. Every record here is synthetic.
"""

from __future__ import annotations

import ast
import dataclasses
import json
import re
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import check_evidence_identifiers as gate  # noqa: E402
from engine.evidence import evidence as model  # noqa: E402
from engine.evidence.entity import (  # noqa: E402
    ChartCandidate, DataClass, EntityKind, OriginCertainty, OriginMoment, Person, RecordProvenance, Shape,
)
from engine.evidence.evidence import (  # noqa: E402
    CONFIDENCE_COMPONENTS, CalculatedInput, ChartContext, ChartReference, Confidence, DependencyClass, Domain,
    EvidenceItem, EvidenceModelError, Lineage, Performance, Polarity, ProducingSystem, Relationship, RuleReference,
    RuleSpec, Supplied, TimingContext, TimingKind, provenance_differences,
)
from engine.evidence.evidence_identifiers import (  # noqa: E402
    EVD_FAMILY, RUL_FAMILY, EvidenceId, IdentifierError, RuleId,
)
from engine.evidence.evidence_store import (  # noqa: E402
    EvidenceStore, item_from_record, item_to_record, relationship_from_record, relationship_to_record,
    rule_from_record, rule_to_record,
)
from engine.evidence.store import StoreError  # noqa: E402
from engine.models.provenance import Provenance  # noqa: E402

PROV = RecordProvenance(source="synthetic fixture", method="hand-written test data", schema_version="h4-v1")
CALC = Provenance(profile_name="parashari_lahiri", ayanamsa_mode=1, frame="sidereal", house_system="W",
                  node_policy="mean", ephemeris_mode="swieph")
HASH_A, HASH_B = "a" * 64, "b" * 64
EVIDENCE_MODULES = ("evidence.py", "evidence_store.py", "evidence_identifiers.py")


def person():
    chart = ChartCandidate(label="natal", origin=OriginMoment(local_datetime="2000-01-01T12:00:00", timezone="UTC",
                                                              timezone_source="fixture", latitude=10.0, longitude=20.0,
                                                              precision="minute"),
                           origin_certainty=OriginCertainty.REPORTED, provenance=PROV)
    return Person(kind=EntityKind.PERSON, shape=Shape.ORIGIN, charts=(chart,), applicable_domains=("career",),
                  applicable_systems=("parashari", "kp"), provenance=PROV, data_class=DataClass.SYNTHETIC)


def spec(school=ProducingSystem.PARASHARI, **changes):
    base = RuleSpec(school=school, content_hash=HASH_A, knowledge_snapshot_hash=HASH_B, declared_strength="strong",
                    provenance=PROV, data_class=DataClass.SYNTHETIC)
    return dataclasses.replace(base, **changes)


def absent_confidence(**supplied):
    return Confidence(**{name: supplied[name] if name in supplied else None for name in CONFIDENCE_COMPONENTS})


class World:
    """An evidence store over one synthetic entity, with a Parashari and a KP rule registered."""

    def __init__(self, path):
        self.store = EvidenceStore(path)
        self.entity = self.store.entities.persist(person())
        self.parashari = self.store.register_rule(spec())
        self.kp = self.store.register_rule(spec(ProducingSystem.KP))

    def item(self, system=ProducingSystem.PARASHARI, facts=("Moon longitude",), provenance=CALC, **changes):
        rule = self.parashari if system is ProducingSystem.PARASHARI else self.kp
        base = EvidenceItem(
            entity=self.entity, domain=Domain.JATAKA, question=None, producing_system=system,
            rule=RuleReference(rule=rule.rule, version=rule.version), declared_strength=rule.spec.declared_strength,
            measured_reliability=None,
            lineage=Lineage(inputs=tuple(CalculatedInput(fact=fact, provenance=provenance) for fact in facts),
                            inputs_complete=True, derivations_complete=True),
            chart=ChartReference(entity_revision=1, chart_label="natal"),
            chart_context=ChartContext(varga="D1", planets=("Moon",), houses=(10,), signs=(4,), significators=()),
            timing=TimingContext(kind=TimingKind.DASHA, label="Vimshottari Moon", start="2010-01-01",
                                 end="2012-12-31"),
            polarity=Polarity.POSITIVE, confidence=absent_confidence(), historical_performance=None, derived_from=(),
            recomputes=None, provenance=PROV, data_class=DataClass.SYNTHETIC)
        return dataclasses.replace(base, **changes)

    def lineage(self, facts, inputs_complete=True, derivations_complete=True, provenance=CALC):
        return Lineage(inputs=tuple(CalculatedInput(fact=fact, provenance=provenance) for fact in facts),
                       inputs_complete=inputs_complete, derivations_complete=derivations_complete)


@pytest.fixture()
def world(tmp_path):
    instance = World(tmp_path / "evidence.sqlite")
    yield instance
    instance.store.close()


# ------------------------------------------------------------------ AC1, AC2 identifier families

@pytest.mark.parametrize("kind,family,width", [(EvidenceId, EVD_FAMILY, 10), (RuleId, RUL_FAMILY, 6)])
def test_ac1_ac2_identifiers_are_exact_and_zero_padded(kind, family, width):
    assert kind.from_number(7).value == f"{family}-{7:0{width}d}" and kind.from_number(7).number == 7
    for bad in (f"{family}-{'1' * (width - 1)}", f"{family}-{'0' * width}", f"{family.lower()}-{'1' * width}", 5):
        with pytest.raises(IdentifierError):
            kind(bad)
    for bad in (0, -1, 10 ** width, True, "1"):
        with pytest.raises(IdentifierError):
            kind.from_number(bad)


def test_ac1_ac2_each_family_has_its_own_durable_issuer(tmp_path):
    path = tmp_path / "evidence.sqlite"
    world = World(path)
    first = world.store.persist(world.item())
    assert (world.store.issued_count(EVD_FAMILY), world.store.issued_count(RUL_FAMILY)) == (1, 2)
    world.store.close()
    again = World(path)  # reopens the same database and registers two more rules
    second = again.store.persist(again.item())
    assert (first.number, second.number, again.parashari.rule.number) == (1, 2, 3)
    with pytest.raises(StoreError):
        again.store.issued_count("EVR")
    for sql in ("UPDATE evidence_issuers SET last_number = 0", "DELETE FROM evidence_issuers"):
        with pytest.raises(sqlite3.DatabaseError):
            again.store._db.execute(sql)
    again.store.close()


def test_ac1_ac2_a_refused_write_takes_no_number(world):
    before = world.store.issued_count(EVD_FAMILY)
    with pytest.raises(StoreError):
        world.store.persist(world.item(rule=RuleReference(rule=world.parashari.rule, version=9)))
    assert world.store.issued_count(EVD_FAMILY) == before


def test_ac1_ac2_both_families_are_registered_and_the_gate_passes():
    naming = (ROOT / "docs" / "NAMING_STANDARD.md").read_text(encoding="utf-8")
    assert gate.check_registration(naming) == []
    assert gate.check_literals(ROOT, gate.tracked_files(ROOT)) == []


@pytest.mark.parametrize("family,old,new", [("EVD", "`EVD-\\d{10}`", "`EVD-\\d{8}`"),
                                            ("RUL", "`RUL-\\d{6}`", "`RUL-\\d{5}`")])
def test_ac1_ac2_the_gate_rejects_a_wrong_registration(family, old, new):
    naming = (ROOT / "docs" / "NAMING_STANDARD.md").read_text(encoding="utf-8")
    assert old in naming
    errors = gate.check_registration(naming.replace(old, new, 1))
    assert any(error.startswith(f"V1 registered {family} pattern") for error in errors)
    row = next(line for line in naming.splitlines() if f"`{family}-" in line)
    assert any("exactly one" in error for error in gate.check_registration(naming.replace(row, "", 1)))


def test_ac1_ac2_the_gate_rejects_a_planted_literal(tmp_path):
    for family, literal in (("EVD", "EVD-" + "0000000001"), ("RUL", "RUL-" + "000001")):
        (tmp_path / "probe.py").write_text(f"VALUE = '{literal}'\n", encoding="utf-8")
        errors = gate.check_literals(tmp_path, ["probe.py"])
        assert errors and literal in errors[0], family


def test_ac1_ac2_the_store_check_passes_a_real_store_and_flags_a_planted_one(world):
    world.store.persist(world.item())
    assert gate.check_store(world.store.path) == []
    world.store._db.execute("INSERT INTO rule_versions (rule_id, version, payload) VALUES (?, 3, '{}')",
                            (world.kp.rule.value,))
    assert any("versions are not 1..n" in error for error in gate.check_store(world.store.path))


# ------------------------------------------------------------------ AC3 the rule-version reference

@pytest.mark.parametrize("change", [{"school": "parashari"}, {"content_hash": "A" * 64}, {"content_hash": "a" * 63},
                                    {"knowledge_snapshot_hash": ""}, {"declared_strength": " "},
                                    {"provenance": None}, {"data_class": "real"}, {"synthetic_reference": False}])
def test_ac3_every_rule_field_is_required(change):
    with pytest.raises(EvidenceModelError):
        spec(**change)


def test_ac3_a_new_version_is_a_new_record_and_the_school_never_changes(world):
    second = world.store.register_rule_version(world.parashari.rule, spec(declared_strength="moderate"))
    assert (second.rule, second.version) == (world.parashari.rule, 2)
    assert [rule.spec.declared_strength for rule in world.store.rule_versions(world.parashari.rule)] == \
        ["strong", "moderate"]
    with pytest.raises(StoreError, match="school"):
        world.store.register_rule_version(world.parashari.rule, spec(ProducingSystem.KP))
    for sql in ("UPDATE rule_versions SET payload = payload", "DELETE FROM rule_versions"):
        with pytest.raises(sqlite3.DatabaseError):
            world.store._db.execute(sql)


@pytest.mark.parametrize("key", ["statement", "condition", "activation_conditions", "apply", "interpretation"])
def test_ac3_rule_text_conditions_and_application_are_refused(world, key):
    record = rule_to_record(world.parashari)
    record["rule_version"][key] = "planted"
    with pytest.raises(StoreError, match="refused"):
        rule_from_record(record)


def test_ac3_rule_references_are_marked_synthetic(world):
    assert world.parashari.spec.synthetic_reference is True
    doc = " ".join(model.__doc__.split())
    assert "synthetic structural references only" in doc and "they authorize no interpretation" in doc


# ------------------------------------------------------------------ AC4 no evidence without its fields

FIELD_BREAKS = {
    "entity": "ENT-00000001", "domain": "jataka", "producing_system": "parashari", "rule": None,
    "declared_strength": "", "lineage": None, "chart": None, "chart_context": None, "timing": None,
    "polarity": "positive", "confidence": None, "provenance": None, "data_class": "real",
    "derived_from": ["EVD-0000000001"], "recomputes": "EVD-0000000001",
}


@pytest.mark.parametrize("name", sorted(FIELD_BREAKS))
def test_ac4_each_required_field_is_refused_when_missing_or_wrong(world, name):
    with pytest.raises(EvidenceModelError):
        world.item(**{name: FIELD_BREAKS[name]})


def test_ac4_a_profile_name_alone_is_not_provenance():
    with pytest.raises(EvidenceModelError, match="profile name alone"):
        CalculatedInput(fact="Moon longitude", provenance="parashari_lahiri")
    with pytest.raises(EvidenceModelError, match="at least one"):
        Lineage(inputs=(), inputs_complete=True, derivations_complete=True)


@pytest.mark.parametrize("key", ["schema", "id"])
def test_ac4_a_record_needs_its_schema_version_and_evd_identity(world, key):
    record = item_to_record(world.store.persist(world.item()) , world.item())
    record.pop(key)
    with pytest.raises(StoreError, match="schema version and EVD identity"):
        item_from_record(record)


def test_ac4_the_store_refuses_unknown_entities_charts_rules_and_mismatches(world):
    from engine.evidence.identifiers import EntityId
    cases = [(world.item(entity=EntityId.from_number(99)), "not in this store"),
             (world.item(chart=ChartReference(entity_revision=2, chart_label="natal")), "no revision 2"),
             (world.item(chart=ChartReference(entity_revision=1, chart_label="d9")), "is not a chart"),
             (world.item(rule=RuleReference(rule=RuleId.from_number(99), version=1)), "not registered"),
             (world.item(rule=RuleReference(rule=world.kp.rule, version=1)), "systems stay isolated"),
             (world.item(declared_strength="weak"), "declared strength"),
             (world.item(derived_from=(EvidenceId.from_number(42),)), "no such evidence")]
    for item, message in cases:
        with pytest.raises(StoreError, match=message):
            world.store.persist(item)


# ------------------------------------------------------------------ AC5, AC6 question linkage and polarity

def test_ac5_question_linkage_is_explicitly_absent(world):
    with pytest.raises(EvidenceModelError, match="question linkage"):
        world.item(question="QST-1")
    record = item_to_record(world.store.persist(world.item()), world.item())
    assert record["evidence"]["question"] is None
    record["evidence"]["question"] = "QST-1"
    with pytest.raises(EvidenceModelError):
        item_from_record(record)


def test_ac6_all_five_polarities_round_trip_and_are_counted_apart(world):
    ids = [world.store.persist(world.item(polarity=polarity)) for polarity in Polarity]
    assert [world.store.load(evidence_id).polarity for evidence_id in ids] == list(Polarity)
    counts = world.store.counts()
    assert {key: len(members) for key, members in counts["polarity"].items()} == {p.value: 1 for p in Polarity}
    with pytest.raises(EvidenceModelError):
        world.item(polarity="mixed")


# ------------------------------------------------------------------ AC7, AC8, AC9 uncertainty, performance, strength

def test_ac7_confidence_components_are_supplied_or_explicitly_absent(world):
    supplied = Supplied(value="high", provenance=PROV)
    item = world.item(confidence=absent_confidence(calculation_confidence=supplied, data_completeness=supplied))
    loaded = world.store.load(world.store.persist(item))
    assert loaded.confidence.calculation_confidence == supplied and loaded.confidence.rule_confidence is None
    assert tuple(field.name for field in dataclasses.fields(Confidence)) == CONFIDENCE_COMPONENTS
    for name in ("cross_method_convergence", "timing_convergence"):
        with pytest.raises(EvidenceModelError, match="later-phase"):
            absent_confidence(**{name: supplied})
    with pytest.raises(EvidenceModelError):
        Supplied(value="0.9", provenance=None)


def test_ac7_ac13_nothing_computes_scores_or_divides():
    forbidden = re.compile(r"score|weight|probabilit|rank|ratio|percent|mean|average", re.IGNORECASE)
    for obj in vars(model).values():
        if isinstance(obj, type) and dataclasses.is_dataclass(obj):
            assert not [f.name for f in dataclasses.fields(obj) if forbidden.search(f.name)], obj.__name__
    public = [name for name in dir(EvidenceStore) if not name.startswith("_")]
    assert not [name for name in public if forbidden.search(name)]
    for name in EVIDENCE_MODULES:
        tree = ast.parse((ROOT / "engine" / "evidence" / name).read_text(encoding="utf-8"))
        arithmetic = [ast.unparse(node) for node in ast.walk(tree) if isinstance(node, (ast.BinOp, ast.AugAssign))
                      and isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mult, ast.Mod, ast.MatMult))]
        assert arithmetic == [], (name, arithmetic)


def test_ac8_absent_performance_is_distinguishable_from_a_measured_zero(world):
    absent = world.store.load(world.store.persist(world.item()))
    zero = world.store.load(world.store.persist(world.item(
        historical_performance=Performance(value="0", sample_size=12, provenance=PROV))))
    assert absent.historical_performance is None and zero.historical_performance.value == "0"
    for bad in (0, -1, True, "12"):
        with pytest.raises(EvidenceModelError):
            Performance(value="0", sample_size=bad, provenance=PROV)


def test_ac9_strength_is_declared_and_reliability_is_absent(world):
    loaded = world.store.load(world.store.persist(world.item()))
    assert loaded.declared_strength == world.parashari.spec.declared_strength and loaded.measured_reliability is None
    with pytest.raises(EvidenceModelError, match="measured reliability"):
        world.item(measured_reliability="0.7")


# ------------------------------------------------------------------ AC10 persistence

@pytest.mark.parametrize("table", ["rule_versions", "evidence_items", "evidence_relationships"])
def test_ac10_every_table_is_append_only(world, table):
    first, second = world.store.persist(world.item()), world.store.persist(world.item(ProducingSystem.KP))
    world.store.relate(first, second)
    assert world.store._db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    for sql in (f"UPDATE {table} SET payload = payload", f"DELETE FROM {table}"):
        with pytest.raises(sqlite3.DatabaseError, match="append-only"):
            world.store._db.execute(sql)


def test_ac10_records_round_trip_with_strict_keys(world):
    item = world.item(historical_performance=Performance(value="3 of 12", sample_size=12, provenance=PROV))
    evidence_id = world.store.persist(item)
    record = item_to_record(evidence_id, item)
    assert item_from_record(json.loads(json.dumps(record))) == (evidence_id, item)
    paths = [("evidence",), ("evidence", "lineage"), ("evidence", "chart"), ("evidence", "chart_context"),
             ("evidence", "timing"), ("evidence", "confidence"), ("evidence", "rule"), ("evidence", "provenance"),
             ("evidence", "historical_performance")]
    for path in paths:
        planted = json.loads(json.dumps(record))
        node = planted
        for key in path:
            node = node[key]
        node["score"] = 1
        with pytest.raises(StoreError, match="refused"):
            item_from_record(planted)
    planted = json.loads(json.dumps(record))
    planted["evidence"]["lineage"]["inputs"][0]["provenance"]["extra"] = 1
    with pytest.raises(StoreError, match="refused"):
        item_from_record(planted)


def test_ac10_the_store_is_durable_across_reopening(tmp_path):
    path = tmp_path / "evidence.sqlite"
    world = World(path)
    evidence_id = world.store.persist(world.item())
    item = world.store.load(evidence_id)
    world.store.close()
    reopened = EvidenceStore(path)
    assert reopened.load(evidence_id) == item and reopened.evidence_ids() == [evidence_id]
    reopened.close()


def test_ac10_a_recomputation_is_a_new_linked_record_and_the_original_stays(world):
    original = world.store.persist(world.item())
    again = world.store.persist(world.item(recomputes=original, polarity=Polarity.NEUTRAL))
    assert again != original and world.store.load(original).polarity is Polarity.POSITIVE
    assert world.store.recomputations(original) == [again]
    with pytest.raises(StoreError, match="keeps the entity, rule and system"):
        world.store.persist(world.item(ProducingSystem.KP, recomputes=original))


# ------------------------------------------------------------------ AC11 provenance mismatch on every field

DIFFERENT = {"profile_name": "kp_krishnamurti", "ayanamsa_mode": 5, "frame": "tropical", "house_system": "P",
             "node_policy": "true", "ephemeris_mode": "moseph", "time_basis": "TT"}


def test_ac11_the_comparison_covers_every_field_of_the_frozen_provenance():
    assert set(DIFFERENT) == {field.name for field in dataclasses.fields(Provenance)}


@pytest.mark.parametrize("field", sorted(DIFFERENT))
def test_ac11_a_join_across_differing_provenance_is_refused_and_names_the_field(world, field):
    other = dataclasses.replace(CALC, **{field: DIFFERENT[field]})
    assert provenance_differences(CALC, other) == (field,)
    first = world.store.persist(world.item())
    second = world.store.persist(world.item(ProducingSystem.KP, facts=("Sun longitude",), provenance=other))
    with pytest.raises(StoreError, match=f"differs in {field};"):
        world.store.join([first, second])
    with pytest.raises(StoreError, match=field):
        world.store.counts([first, second])
    with pytest.raises(EvidenceModelError, match=field):
        Lineage(inputs=(CalculatedInput(fact="Moon", provenance=CALC), CalculatedInput(fact="Sun", provenance=other)),
                inputs_complete=True, derivations_complete=True)


def test_ac11_every_differing_field_is_named(world):
    other = dataclasses.replace(CALC, **DIFFERENT)
    assert provenance_differences(CALC, other) == tuple(field.name for field in dataclasses.fields(Provenance))


def test_ac11_identical_provenance_joins(world):
    first = world.store.persist(world.item())
    second = world.store.persist(world.item(ProducingSystem.KP, facts=("Sun longitude",),
                                            provenance=dataclasses.replace(CALC)))
    assert len(world.store.join([first, second])) == 2


# ------------------------------------------------------------------ AC12 relationships

def test_ac12_derived_exactly_when_a_derivation_link_is_recorded(world):
    base = world.store.persist(world.item())
    child = world.store.persist(world.item(ProducingSystem.KP, facts=("Sun",), derived_from=(base,)))
    grandchild = world.store.persist(world.item(facts=("Mars",), derived_from=(child,)))
    recomputed = world.store.persist(world.item(facts=("Venus",), recomputes=base))
    for first, second in ((base, child), (child, base), (base, grandchild), (base, recomputed)):
        assert world.store.classify(first, second).dependency is DependencyClass.DERIVED


def test_ac12_shared_origin_from_a_shared_input_or_ancestor(world):
    first = world.store.persist(world.item(facts=("Moon longitude", "Lagna")))
    second = world.store.persist(world.item(ProducingSystem.KP, facts=("Moon longitude",)))
    relationship = world.store.classify(first, second)
    assert relationship.dependency is DependencyClass.SHARED_ORIGIN and "Moon longitude" in relationship.basis
    root = world.store.persist(world.item(facts=("Jupiter",)))
    left = world.store.persist(world.item(facts=("Saturn",), derived_from=(root,)))
    right = world.store.persist(world.item(ProducingSystem.KP, facts=("Rahu",), derived_from=(root,)))
    assert world.store.classify(left, right).dependency is DependencyClass.SHARED_ORIGIN


def test_ac12_independent_only_on_positive_recorded_evidence(world):
    first = world.store.persist(world.item(facts=("Moon longitude",)))
    second = world.store.persist(world.item(ProducingSystem.KP, facts=("Sun longitude",)))
    assert world.store.classify(first, second).dependency is DependencyClass.INDEPENDENT


@pytest.mark.parametrize("case,message", [
    ("missing link", "derivation link may be missing"),
    ("incomplete lineage", "incomplete lineage"),
    ("unverified derivation path", "unverified derivation path"),
    ("same system", "same producing system"),
])
def test_ac12_anything_missing_incomplete_or_unverified_is_unknown(world, case, message):
    first = world.store.persist(world.item(facts=("Moon longitude",)))
    if case == "missing link":
        second = world.store.persist(world.item(ProducingSystem.KP, lineage=world.lineage(
            ("Sun longitude",), derivations_complete=False)))
    elif case == "incomplete lineage":
        second = world.store.persist(world.item(ProducingSystem.KP, lineage=world.lineage(
            ("Sun longitude",), inputs_complete=False)))
    elif case == "unverified derivation path":
        ancestor = world.store.persist(world.item(ProducingSystem.KP, lineage=world.lineage(
            ("Mars",), derivations_complete=False)))
        second = world.store.persist(world.item(ProducingSystem.KP, facts=("Sun longitude",), derived_from=(ancestor,)))
    else:
        second = world.store.persist(world.item(facts=("Sun longitude",)))
    relationship = world.store.classify(first, second)
    assert relationship.dependency is DependencyClass.UNKNOWN and message in relationship.basis


def test_ac12_correlated_is_refused(world):
    first, second = world.store.persist(world.item()), world.store.persist(world.item(ProducingSystem.KP))
    with pytest.raises(EvidenceModelError, match="CORRELATED"):
        Relationship(first, second, DependencyClass.CORRELATED, False, "planted")
    record = relationship_to_record(world.store.relate(first, second))
    record["relationship"]["dependency"] = "correlated"
    with pytest.raises(EvidenceModelError, match="CORRELATED"):
        relationship_from_record(record)


def test_ac12_conflict_is_recorded_separately_from_dependency(world):
    positive = world.store.persist(world.item(facts=("Moon longitude",)))
    negative = world.store.persist(world.item(ProducingSystem.KP, facts=("Moon longitude",),
                                              polarity=Polarity.NEGATIVE))
    relationship = world.store.relate(positive, negative)
    assert (relationship.dependency, relationship.conflicting) == (DependencyClass.SHARED_ORIGIN, True)
    later = world.store.persist(world.item(ProducingSystem.KP, facts=("Sun",), polarity=Polarity.NEGATIVE,
                                           timing=TimingContext(kind=TimingKind.WINDOW, label="later",
                                                                start="2020-01-01", end="2020-12-31")))
    assert world.store.classify(positive, later).conflicting is False


def test_ac12_unknown_is_never_counted_as_independent(world):
    first = world.store.persist(world.item(facts=("Moon longitude",)))
    independent = world.store.persist(world.item(ProducingSystem.KP, facts=("Sun longitude",)))
    unknown = world.store.persist(world.item(ProducingSystem.KP, lineage=world.lineage(("Mars",),
                                                                                         inputs_complete=False)))
    world.store.relate(first, independent)
    world.store.relate(first, unknown)
    counts = world.store.relationship_counts()
    assert counts["independent"] == ((first, independent),) and counts["unknown"] == ((first, unknown),)
    assert len(world.store.relationships()) == 2


# ------------------------------------------------------------------ AC13 decomposable aggregates

def test_ac13_every_count_returns_its_members_and_the_partitions_sum(world):
    ids = [world.store.persist(world.item(polarity=Polarity.POSITIVE)),
           world.store.persist(world.item(ProducingSystem.KP, polarity=Polarity.NEGATIVE)),
           world.store.persist(world.item(domain=Domain.VARSHAPHAL, polarity=Polarity.NEUTRAL))]
    counts = world.store.counts()
    assert counts["total"] == tuple(ids)
    for axis in ("producing_system", "domain", "polarity", "rule"):
        parts = [set(members) for members in counts[axis].values()]
        assert set().union(*parts) == set(ids) and sum(len(part) for part in parts) == len(ids)
    assert counts["members"][ids[1]] == ("kp", "jataka") and counts["members"][ids[2]] == ("parashari", "varshaphal")


# ------------------------------------------------------------------ AC14, AC15 one direction; no invented rules

CALCULATION_PACKAGES = ("engine.astronomy", "engine.astrology", "engine.dasha", "engine.transits", "engine.kp",
                        "engine.parashari", "engine.panchanga", "engine.api", "engine.knowledge")


def _imports(name):
    tree = ast.parse((ROOT / "engine" / "evidence" / name).read_text(encoding="utf-8"))
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            found.add(node.module)
        elif isinstance(node, ast.Import):
            found.update(alias.name for alias in node.names)
    return found


@pytest.mark.parametrize("name", EVIDENCE_MODULES)
def test_ac14_ac15_evidence_imports_no_calculation_writer_and_no_llm(name):
    imports = _imports(name)
    assert not [module for module in imports if module.startswith(CALCULATION_PACKAGES)], imports
    assert not [module for module in imports
                if module.split(".")[0] in {"anthropic", "openai", "requests", "networkx", "graphlib"}]
    assert {module for module in imports if module.startswith("engine.")} <= {
        "engine.evidence.entity", "engine.evidence.evidence", "engine.evidence.evidence_identifiers",
        "engine.evidence.identifiers", "engine.evidence.store", "engine.models.provenance"}


def test_ac15_evidence_names_only_a_registered_rule_version(world):
    with pytest.raises(StoreError, match="not registered"):
        world.store.persist(world.item(rule=RuleReference(rule=world.parashari.rule, version=2)))
    assert not {"rule_text", "statement", "condition"} & {field.name for field in dataclasses.fields(EvidenceItem)}


# ------------------------------------------------------------------ AC16, AC17 existing refusals; synthetic only

def test_ac16_ac17_records_refuse_other_keys_and_real_data(world):
    record = item_to_record(world.store.persist(world.item()), world.item())
    record["evidence"]["interpretation"] = "planted"
    with pytest.raises(StoreError, match="refused"):
        item_from_record(record)
    with pytest.raises(EvidenceModelError, match="synthetic"):
        world.item(data_class="real")
    with pytest.raises(EvidenceModelError, match="synthetic"):
        spec(data_class="real")
