"""WP-E1 acceptance criteria (ADR-0114 s3): the H0 entity model, the append-only store and the ENT family.

Every record here is synthetic. No person, organisation or place in these fixtures is real data.
"""

from __future__ import annotations

import dataclasses
import json
import re
import sqlite3
import subprocess
import sys
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import check_entity_identifiers as gate  # noqa: E402
from engine.evidence import entity as model  # noqa: E402
from engine.evidence.entity import (  # noqa: E402
    ChartCandidate, DataClass, EntityKind, EntityLink, EntityModelError, EventEntity, GeographicEntity,
    Organisation, OriginCertainty, OriginMoment, ParentLink, Person, Question, RecordProvenance, Shape,
    rectification_permitted,
)
from engine.evidence.identifiers import EntityId, IdentifierError  # noqa: E402
from engine.evidence.store import EntityStore, StoreError, subject_from_record, subject_to_record  # noqa: E402

PROV = RecordProvenance(source="synthetic fixture", method="hand-written test data", schema_version="h0-v2")


def origin(day="2000-01-01T12:00:00"):
    return OriginMoment(local_datetime=day, timezone="UTC", timezone_source="fixture", latitude=10.0,
                        longitude=20.0, precision="minute")


def chart(label, certainty=OriginCertainty.REPORTED, day="2000-01-01T12:00:00"):
    return ChartCandidate(label=label, origin=origin(day), origin_certainty=certainty, provenance=PROV)


def person(*charts, shape=Shape.ORIGIN, parent=None):
    return Person(kind=EntityKind.PERSON, shape=shape, charts=charts or (chart("only"),),
                  applicable_domains=("jataka",), applicable_systems=("parashari",), provenance=PROV,
                  data_class=DataClass.SYNTHETIC, parent=parent)


@pytest.fixture()
def store(tmp_path):
    with EntityStore(tmp_path / "entities.sqlite") as instance:
        yield instance


# ------------------------------------------------------------------ AC2 identifiers

@pytest.mark.parametrize("text", ["ENT-00000001", "ENT-99999999", "ENT-00012345"])
def test_ac2_valid_identifiers(text):
    assert EntityId(text).value == text


@pytest.mark.parametrize("text", ["ENT-0000001", "ENT-000000001", "ent-00000001", "ENT-0000000A", "ENT00000001",
                                  "EVR-00000001", " ENT-00000001", "ENT-00000000", "", None, 1])
def test_ac2_invalid_identifiers(text):
    with pytest.raises(IdentifierError):
        EntityId(text)


@pytest.mark.parametrize("number", [0, -1, 10 ** 8, True, 1.0])
def test_ac2_numbers_out_of_range(number):
    with pytest.raises(IdentifierError):
        EntityId.from_number(number)


# ------------------------------------------------------------------ AC3 allocation

def test_ac3_allocation_is_monotone_and_durable(tmp_path):
    path = tmp_path / "entities.sqlite"
    with EntityStore(path) as first:
        issued = [first.persist(person()) for _ in range(3)]
    with EntityStore(path) as reopened:
        issued.append(reopened.persist(person()))
    assert [entity.number for entity in issued] == [1, 2, 3, 4]


def test_ac3_a_failed_persistence_consumes_no_number(store, monkeypatch):
    store.persist(person())
    import engine.evidence.store as store_module

    real = store_module._encode

    def broken(record):
        raise StoreError("planted failure before the write")

    monkeypatch.setattr(store_module, "_encode", broken)
    with pytest.raises(StoreError):
        store.persist(person())
    monkeypatch.setattr(store_module, "_encode", real)
    assert store.persist(person()).number == 2


def test_ac3_a_failure_inside_the_transaction_rolls_back(store):
    store.persist(person())
    store._db.execute("CREATE TRIGGER planted BEFORE INSERT ON entity_revisions BEGIN SELECT RAISE(ABORT, 'x'); END")
    with pytest.raises(sqlite3.DatabaseError):
        store.persist(person())
    store._db.execute("DROP TRIGGER planted")
    assert store.issued_count() == 1 and store.persist(person()).number == 2


def test_ac3_two_connections_get_distinct_numbers(tmp_path):
    path = tmp_path / "entities.sqlite"
    EntityStore(path).close()
    issued, lock = [], threading.Lock()

    def worker():
        with EntityStore(path) as own:
            for _ in range(10):
                entity = own.persist(person())
                with lock:
                    issued.append(entity.number)

    threads = [threading.Thread(target=worker) for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert sorted(issued) == list(range(1, 21))


def test_ac3_the_issuer_never_decreases(store):
    store.persist(person())
    with pytest.raises(sqlite3.DatabaseError):
        store._db.execute("UPDATE issuer SET last_number = 0")


def test_ac3_fixture_stores_are_isolated_issuers(tmp_path):
    with EntityStore(tmp_path / "a.sqlite") as one, EntityStore(tmp_path / "b.sqlite") as two:
        one.persist(person())
        assert two.persist(person()).number == 1


# ------------------------------------------------------------------ AC4, AC5 model

@pytest.mark.parametrize("cls,kind", [(Person, EntityKind.PERSON), (Organisation, EntityKind.ORGANISATION),
                                      (GeographicEntity, EntityKind.GEOGRAPHIC), (EventEntity, EntityKind.EVENT)])
def test_ac4_specialised_types_for_origin_kinds(cls, kind):
    subject = cls(kind=kind, shape=Shape.ORIGIN, charts=(chart("a"),), applicable_domains=("mundane",),
                  applicable_systems=("parashari",), provenance=PROV, data_class=DataClass.SYNTHETIC)
    assert isinstance(subject, model.AstrologicalSubject) and subject.kind is kind


def test_ac4_exactly_five_kinds():
    assert {kind.value for kind in EntityKind} == {"person", "organisation", "geographic", "event", "question"}
    assert set(model.SUBJECT_TYPES) == set(EntityKind)


def test_ac4_the_common_abstraction_is_not_constructed_directly():
    with pytest.raises(EntityModelError):
        model.AstrologicalSubject(kind=EntityKind.PERSON, shape=Shape.ORIGIN, charts=(chart("a"),),
                                  applicable_domains=("jataka",), applicable_systems=("parashari",), provenance=PROV,
                                  data_class=DataClass.SYNTHETIC)


def test_ac4_a_kind_cannot_be_borrowed():
    with pytest.raises(EntityModelError):
        Person(kind=EntityKind.ORGANISATION, shape=Shape.ORIGIN, charts=(chart("a"),), applicable_domains=("x",),
               applicable_systems=("y",), provenance=PROV, data_class=DataClass.SYNTHETIC)


def question():
    return Question(kind=EntityKind.QUESTION, shape=Shape.QUERY, charts=(chart("asked", OriginCertainty.DOCUMENTED),),
                    applicable_domains=("prashna",), applicable_systems=("kp",), provenance=PROV,
                    data_class=DataClass.SYNTHETIC)


def test_ac5_shape_validity():
    assert not rectification_permitted(question(), "asked")
    documented = person(chart("registry", OriginCertainty.DOCUMENTED), chart("recalled", OriginCertainty.UNCERTAIN))
    assert not rectification_permitted(documented, "registry")
    assert rectification_permitted(documented, "recalled")
    with pytest.raises(EntityModelError):
        Question(kind=EntityKind.QUESTION, shape=Shape.ORIGIN, charts=(chart("a"),), applicable_domains=("p",),
                 applicable_systems=("kp",), provenance=PROV, data_class=DataClass.SYNTHETIC)
    with pytest.raises(EntityModelError):
        Question(kind=EntityKind.QUESTION, shape=Shape.QUERY, charts=(chart("a"), chart("b")),
                 applicable_domains=("p",), applicable_systems=("kp",), provenance=PROV, data_class=DataClass.SYNTHETIC)


def test_ac5_shape_d_is_not_an_entity():
    assert {shape.value for shape in Shape} == {"A", "B", "C"}


def test_ac5_derived_subjects_need_a_parent_and_others_must_not_have_one():
    link = ParentLink(parent=EntityId.from_number(1), parent_chart="natal", derivation="varshaphal 2026")
    assert person(shape=Shape.DERIVED, parent=link).parent == link
    with pytest.raises(EntityModelError):
        person(shape=Shape.DERIVED)
    with pytest.raises(EntityModelError):
        person(parent=link)


def test_ac5_applicability_is_declared_never_empty():
    with pytest.raises(EntityModelError):
        Person(kind=EntityKind.PERSON, shape=Shape.ORIGIN, charts=(chart("a"),), applicable_domains=(),
               applicable_systems=("parashari",), provenance=PROV, data_class=DataClass.SYNTHETIC)


# ------------------------------------------------------------------ AC6, AC11 competing charts and round trip

def test_ac6_competing_charts_are_all_held_with_their_own_provenance(store):
    rival = RecordProvenance(source="second synthetic source", method="fixture", schema_version="h0-v2")
    subject = GeographicEntity(
        kind=EntityKind.GEOGRAPHIC, shape=Shape.ORIGIN,
        charts=(chart("midnight", OriginCertainty.DOCUMENTED, "1950-01-01T00:00:00"),
                dataclasses.replace(chart("noon", OriginCertainty.REPORTED, "1950-01-01T12:00:00"), provenance=rival)),
        applicable_domains=("mundane",), applicable_systems=("parashari", "kp"), provenance=PROV,
        data_class=DataClass.SYNTHETIC)
    loaded = store.load(store.persist(subject))
    assert loaded == subject
    assert [c.label for c in loaded.charts] == ["midnight", "noon"]
    assert loaded.chart("noon").provenance == rival
    assert not any("select" in name for name in model.SUBJECT_FIELDS)


def test_ac6_duplicate_chart_labels_are_refused():
    with pytest.raises(EntityModelError):
        person(chart("same"), chart("same"))


@pytest.mark.parametrize("make", [person, question])
def test_ac11_round_trip(store, make):
    subject = make()
    assert store.load(store.persist(subject)) == subject
    assert subject_from_record(json.loads(json.dumps(subject_to_record(subject)))) == subject


# ------------------------------------------------------------------ AC7 relationships

def test_ac7_relationships_are_links_between_stored_entities(store):
    a, b = store.persist(person()), store.persist(person())
    link = EntityLink(source=a, relation="LEADS", target=b, provenance=PROV)
    store.add_link(link)
    assert store.links() == [link]
    assert "RELATIONSHIP" not in {kind.name for kind in EntityKind}


def test_ac7_bad_links_are_refused(store):
    a = store.persist(person())
    with pytest.raises(EntityModelError):
        EntityLink(source=a, relation="leads", target=EntityId.from_number(2), provenance=PROV)
    with pytest.raises(EntityModelError):
        EntityLink(source=a, relation="SELF", target=a, provenance=PROV)
    with pytest.raises(StoreError):
        store.add_link(EntityLink(source=a, relation="LEADS", target=EntityId.from_number(99), provenance=PROV))


# ------------------------------------------------------------------ AC8 immutability

def test_ac8_records_are_frozen():
    subject = person()
    with pytest.raises(dataclasses.FrozenInstanceError):
        subject.shape = Shape.DERIVED


@pytest.mark.parametrize("sql", ["UPDATE entity_revisions SET reason = 'rewritten'", "DELETE FROM entity_revisions",
                                 "UPDATE entity_links SET payload = '{}'", "DELETE FROM entity_links",
                                 "DELETE FROM issuer"])
def test_ac8_the_database_refuses_rewrites(store, sql):
    a, b = store.persist(person()), store.persist(person())
    store.add_link(EntityLink(source=a, relation="KNOWS", target=b, provenance=PROV))
    with pytest.raises(sqlite3.DatabaseError):
        store._db.execute(sql)
    assert len(store.history(a)) == 1 and len(store.links()) == 1


def test_ac8_a_correction_appends_with_its_reason(store):
    entity_id = store.persist(person(chart("first")))
    revision = store.append_revision(entity_id, person(chart("first"), chart("second")), "second candidate found")
    history = store.history(entity_id)
    assert revision == 2 and [r for r, _s, _why in history] == [1, 2]
    assert history[0][1] == person(chart("first")) and history[1][2] == "second candidate found"
    with pytest.raises(StoreError):
        store.append_revision(entity_id, person(), "")
    with pytest.raises(StoreError):
        store.append_revision(entity_id, question(), "a kind change is not a correction")


def test_ac8_the_store_has_no_update_or_delete_api():
    names = {name for name in dir(EntityStore) if not name.startswith("_")}
    assert not {n for n in names if re.search(r"update|delete|remove|overwrite|replace|set_", n)}


# ------------------------------------------------------------------ AC9 analytical content, AC10 synthetic only

@pytest.mark.parametrize("key", ["interpretation", "evidence", "score", "weight", "confidence", "prediction"])
def test_ac9_analytical_content_cannot_be_stored(key):
    record = subject_to_record(person())
    record["subject"][key] = "planted"
    with pytest.raises(StoreError):
        subject_from_record(record)
    with pytest.raises(TypeError):
        Person(kind=EntityKind.PERSON, shape=Shape.ORIGIN, charts=(chart("a"),), applicable_domains=("j",),
               applicable_systems=("p",), provenance=PROV, data_class=DataClass.SYNTHETIC, **{key: 1})


def test_ac10_only_synthetic_data_is_accepted():
    assert [member.value for member in DataClass] == ["synthetic"]
    record = subject_to_record(person())
    record["subject"]["data_class"] = "real"
    with pytest.raises(ValueError):
        subject_from_record(record)
    with pytest.raises(EntityModelError):
        Person(kind=EntityKind.PERSON, shape=Shape.ORIGIN, charts=(chart("a"),), applicable_domains=("j",),
               applicable_systems=("p",), provenance=PROV, data_class="real")


# ------------------------------------------------------------------ AC14 no scoring field

def test_ac14_no_scoring_weighting_or_confidence_field():
    forbidden = re.compile(r"score|weight|confidence|probabilit|fit|rank", re.IGNORECASE)
    for obj in vars(model).values():
        if isinstance(obj, type) and dataclasses.is_dataclass(obj):
            assert not [f.name for f in dataclasses.fields(obj) if forbidden.search(f.name)], obj.__name__


# ------------------------------------------------------------------ AC1, AC12 the uniqueness gate and its controls

def test_ac1_the_real_registration_passes():
    assert gate.check_registration(gate.NAMING.read_text(encoding="utf-8")) == []


@pytest.mark.parametrize("old,new", [(r"`ENT-\d{8}` | 8 |", r"`ENT-\d{6}` | 8 |"), (r"`ENT-\d{8}` | 8 |", r"`ENT-\d{8}` | 6 |")])
def test_ac1_a_wrong_registration_fails(old, new):
    text = gate.NAMING.read_text(encoding="utf-8")
    assert old in text
    assert any(error.startswith("E1") for error in gate.check_registration(text.replace(old, new)))


def test_ac1_a_missing_or_duplicated_registration_fails():
    text = gate.NAMING.read_text(encoding="utf-8")
    row = next(line for line in text.splitlines() if "`ENT-" in line)
    assert gate.check_registration(text.replace(row + "\n", ""))[0].startswith("E1")
    assert gate.check_registration(text.replace(row, row + "\n" + row))[0].startswith("E1")


def test_ac12_a_literal_identifier_in_production_code_fails(tmp_path):
    (tmp_path / "engine").mkdir()
    literal = "ENT-" + "00000007"
    (tmp_path / "engine" / "planted.py").write_text(f"X = '{literal}'\n", encoding="utf-8")
    assert gate.check_literals(tmp_path, ["engine/planted.py"])[0].startswith("E2")
    assert gate.check_literals(ROOT, gate.tracked_files(ROOT)) == []


def test_ac12_a_real_store_passes_and_a_planted_duplicate_fails(tmp_path):
    path = tmp_path / "entities.sqlite"
    with EntityStore(path) as real:
        a = real.persist(person())
        real.append_revision(a, person(), "fixed")
        real.persist(person())
    assert gate.check_store(path) == []
    # The schema's own primary key already refuses a duplicate (entity, revision): the defence one layer down.
    db = sqlite3.connect(str(path))
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("INSERT INTO entity_revisions VALUES ('ENT-' || '00000001', 1, '{}', 'planted')")
    # Corruptions the schema cannot block, planted only by dropping the store's own triggers.
    db.execute("DROP TRIGGER revisions_no_update")
    db.execute("DROP TRIGGER issuer_never_decreases")
    db.execute("UPDATE entity_revisions SET revision = 5 WHERE entity_id = 'ENT-' || '00000002'")
    db.execute("UPDATE issuer SET last_number = 1")
    db.commit()
    db.close()
    errors = gate.check_store(path)
    assert any("revisions are not 1..n" in error for error in errors)
    assert any("exceeds the issuer's counter" in error for error in errors)


def test_ac12_the_command_line_gate_passes_on_the_real_tree():
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_entity_identifiers.py")],
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stdout
