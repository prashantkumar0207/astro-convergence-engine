"""WP-E2 acceptance tests (ADR-0115 s5): the H1 event model, the event store and the EVR family.

Every record here is synthetic.
"""

from __future__ import annotations

import dataclasses
import re
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import check_event_identifiers as gate  # noqa: E402
from engine.evidence import event_classes, events as model  # noqa: E402
from engine.evidence.entity import (  # noqa: E402
    ChartCandidate, DataClass, EntityKind, OriginCertainty, OriginMoment, Person, RecordProvenance, Shape,
)
from engine.evidence.event_classes import CLASSES, SEED, ClassOrigin  # noqa: E402
from engine.evidence.event_identifiers import EventRecordId, IdentifierError  # noqa: E402
from engine.evidence.event_store import (  # noqa: E402
    EventStore, confirmation_from_record, confirmation_to_record, event_from_record, event_to_record,
)
from engine.evidence.events import (  # noqa: E402
    Assertion, AssertionContext, AsserterCertainty, AsserterKind, Confirmation, ConfirmationState, ConfirmerKind,
    EventModelError, EventRecord, EventTime, TimeKind, TimeTolerance, TimeUnit, WindowShape,
    validation_input_permitted,
)
from engine.evidence.identifiers import EntityId  # noqa: E402
from engine.evidence.store import StoreError  # noqa: E402

PROV = RecordProvenance(source="synthetic fixture", method="hand-written test data", schema_version="h1-v2")
PROMOTION, LAYOFF = "EV-CAR-003", "EV-CAR-019"


def chart(label):
    return ChartCandidate(label=label, origin=OriginMoment(local_datetime="2000-01-01T12:00:00", timezone="UTC",
                                                           timezone_source="fixture", latitude=10.0, longitude=20.0,
                                                           precision="minute"),
                          origin_certainty=OriginCertainty.REPORTED, provenance=PROV)


def person(*labels):
    return Person(kind=EntityKind.PERSON, shape=Shape.ORIGIN, charts=tuple(chart(label) for label in labels),
                  applicable_domains=("career",), applicable_systems=("parashari",), provenance=PROV,
                  data_class=DataClass.SYNTHETIC)


def day(value="2010-05-12"):
    return EventTime(kind=TimeKind.INSTANT, precision=TimeUnit.DAY, timezone="UTC", timezone_source="fixture", at=value)


def assertion(kind=AsserterKind.USER_RECOLLECTION, certainty=AsserterCertainty.PROBABLE, at="2026-01-01T09:00:00Z"):
    return Assertion(asserter_kind=kind, asserter_reference="synthetic asserter", asserted_at=at,
                     method="interview", asserter_certainty=certainty)


def event(entity, time=None, cls=PROMOTION, claim=None, context=None, **extra):
    return EventRecord(entity=entity, event_class=cls, time=time or day(), assertion=claim or assertion(),
                       provenance=PROV, data_class=DataClass.SYNTHETIC, assertion_context=context, **extra)


def confirmation(state=ConfirmationState.CONFIRMED, statement=""):
    return Confirmation(state=state, confirmer_kind=ConfirmerKind.SUBJECT, confirmer_reference="synthetic subject",
                        confirmed_at="2026-02-01T09:00:00Z", statement=statement, provenance=PROV)


@pytest.fixture()
def store(tmp_path):
    with EventStore(tmp_path / "evidence.sqlite") as instance:
        yield instance


@pytest.fixture()
def entity(store):
    return store.entities.persist(person("natal", "rectified"))


# ------------------------------------------------------------------ AC2 identifiers

@pytest.mark.parametrize("number", [1, 42, 99999999])
def test_ac2_valid_identifiers(number):
    identifier = EventRecordId.from_number(number)
    assert identifier.number == number and len(str(identifier)) == 12 and EventRecordId(str(identifier)) == identifier


@pytest.mark.parametrize("bad", ["EVR-0000001", "EVR-000000001", "evr-00000001", "EVR-0000000a", "EVR-00000000",
                                 " EVR-00000001", "ENT-00000001", "EVR00000001"])
def test_ac2_invalid_identifiers(bad):
    with pytest.raises(IdentifierError):
        EventRecordId(bad)


@pytest.mark.parametrize("number", [0, -1, 10 ** 8, True, 1.0, "1"])
def test_ac2_out_of_range_numbers(number):
    with pytest.raises(IdentifierError):
        EventRecordId.from_number(number)


# ------------------------------------------------------------------ AC3 allocation

def test_ac3_allocation_is_monotone_and_durable(tmp_path):
    path = tmp_path / "evidence.sqlite"
    with EventStore(path) as first:
        owner = first.entities.persist(person("natal"))
        issued = [first.persist(event(owner, day(f"2010-05-{n:02d}"))) for n in range(1, 4)]
    assert [identifier.number for identifier in issued] == [1, 2, 3]
    with EventStore(path) as reopened:
        assert reopened.issued_count() == 3
        assert reopened.persist(event(owner, day("2011-01-01"))).number == 4


def test_ac3_a_refused_persistence_takes_no_number(store, entity):
    store.persist(event(entity))
    before = store.issued_count()
    for bad in (event(entity), event(EntityId.from_number(99)), event(entity, day("2010-06-01"),
                                                                    context=AssertionContext(5, "natal", PROV))):
        with pytest.raises(StoreError):
            store.persist(bad)
    assert store.issued_count() == before
    assert store.persist(event(entity, day("2010-07-01"))).number == before + 1


def test_ac3_two_connections_get_distinct_numbers(tmp_path):
    path = tmp_path / "evidence.sqlite"
    with EventStore(path) as one, EventStore(path) as two:
        owner = one.entities.persist(person("natal"))
        numbers = [one.persist(event(owner, day("2010-01-01"))).number, two.persist(event(owner, day("2010-01-02"))).number,
                   one.persist(event(owner, day("2010-01-03"))).number]
    assert numbers == [1, 2, 3]


def test_ac3_the_issuer_cannot_decrease_or_be_removed(store, entity):
    store.persist(event(entity))
    for sql in ("UPDATE event_issuer SET last_number = 0", "DELETE FROM event_issuer"):
        with pytest.raises(sqlite3.DatabaseError):
            store._db.execute(sql)


def test_ac3_the_evr_issuer_is_separate_from_the_ent_issuer(store, entity):
    store.persist(event(entity))
    assert store.entities.issued_count() == 1 and store.issued_count() == 1
    store.entities.persist(person("natal"))
    assert store.issued_count() == 1


# ------------------------------------------------------------------ AC4 event classes

def test_ac4_the_seed_is_the_47_registry_rows():
    assert len(SEED) == 47 and len(CLASSES) == 47
    origins = [entry.origin for entry in SEED]
    assert origins.count(ClassOrigin.MODEL) == 42 and origins.count(ClassOrigin.PROPOSED_ADDITION) == 5
    assert gate.check_seed(gate.REGISTRY.read_text(encoding="utf-8")) == []


@pytest.mark.parametrize("cls", ["EV-CAR-048", "EV-CAR-000", "EV-RES-001", "promotion", "EV-CAR-3"])
def test_ac4_an_unregistered_class_is_refused(store, entity, cls):
    with pytest.raises(EventModelError):
        event(entity, cls=cls)


def test_ac4_the_seed_check_fails_on_any_disagreement():
    text = gate.REGISTRY.read_text(encoding="utf-8")
    renamed = (dataclasses.replace(SEED[0], name="first_job"),) + SEED[1:]
    reordered = (SEED[1], SEED[0]) + SEED[2:]
    regrouped = (dataclasses.replace(SEED[0], group="exit"),) + SEED[1:]
    reorigined = (dataclasses.replace(SEED[0], origin=ClassOrigin.PROPOSED_ADDITION),) + SEED[1:]
    for planted in (SEED[1:], SEED + (SEED[0],), renamed, reordered, regrouped, reorigined):
        assert any(error.startswith("V4") for error in gate.check_seed(text, planted))
    dropped_row = "\n".join(line for line in text.splitlines() if not line.startswith("| EV-CAR-047 "))
    assert any(error.startswith("V4") for error in gate.check_seed(dropped_row))


def test_ac4_domain_is_the_registered_classes_domain(entity):
    assert event(entity, domain="career").domain == "career"
    with pytest.raises(EventModelError):
        event(entity, domain="residence")
    with pytest.raises(EventModelError):
        event(entity, subclass="Not A Token")


# ------------------------------------------------------------------ AC5 time

TIMES = {
    "instant at year precision": EventTime(TimeKind.INSTANT, TimeUnit.YEAR, "UTC", "fixture", at="2010"),
    "instant at minute precision": EventTime(TimeKind.INSTANT, TimeUnit.MINUTE, "Asia/Kolkata", "fixture",
                                             at="2010-05-12T14:30", birth_time_sensitive=True),
    "closed interval": EventTime(TimeKind.CLOSED_INTERVAL, TimeUnit.MONTH, "UTC", "fixture", start="2010-03",
                                 end="2010-06"),
    "zero-length interval": EventTime(TimeKind.CLOSED_INTERVAL, TimeUnit.DAY, "UTC", "fixture", start="2010-05-12",
                                      end="2010-05-12"),
    "open interval, start only": EventTime(TimeKind.OPEN_INTERVAL, TimeUnit.YEAR, "UTC", "fixture", start="2010"),
    "open interval, end only": EventTime(TimeKind.OPEN_INTERVAL, TimeUnit.DAY, "UTC", "fixture", end="2010-05-12"),
    "unbounded": EventTime(TimeKind.OPEN_INTERVAL, None, None, None),
    "fuzzy window": EventTime(TimeKind.FUZZY_WINDOW, TimeUnit.MONTH, "UTC", "fixture", at="2010-05",
                              tolerance=TimeTolerance(2, TimeUnit.MONTH), window_shape=WindowShape.TRIANGULAR),
    "fuzzy hour window": EventTime(TimeKind.FUZZY_WINDOW, TimeUnit.HOUR, "UTC", "fixture", at="2010-05-12T14",
                                   tolerance=TimeTolerance(3, TimeUnit.HOUR), birth_time_sensitive=True),
}


@pytest.mark.parametrize("label", sorted(TIMES))
def test_ac5_every_time_kind_round_trips(store, entity, label):
    stored = event(entity, TIMES[label])
    assert store.load(store.persist(stored)) == stored


def test_ac5_every_time_kind_is_covered():
    assert {time.kind for time in TIMES.values()} == set(TimeKind)


@pytest.mark.parametrize("build", [
    lambda: EventTime(TimeKind.INSTANT, TimeUnit.DAY, "UTC", "fixture", at="2010-05"),               # wrong precision
    lambda: EventTime(TimeKind.INSTANT, TimeUnit.YEAR, "UTC", "fixture", at="2010-05-12"),           # false precision
    lambda: EventTime(TimeKind.INSTANT, TimeUnit.DAY, "UTC", "fixture", at="2010-02-30"),            # not a date
    lambda: EventTime(TimeKind.INSTANT, None, "UTC", "fixture", at="2010"),                          # no precision
    lambda: EventTime(TimeKind.INSTANT, TimeUnit.YEAR, None, "fixture", at="2010"),                  # no timezone
    lambda: EventTime(TimeKind.INSTANT, TimeUnit.YEAR, "UTC", " ", at="2010"),                       # no tz source
    lambda: EventTime(TimeKind.INSTANT, TimeUnit.YEAR, "UTC", "fixture"),                            # no value
    lambda: EventTime(TimeKind.INSTANT, TimeUnit.YEAR, "UTC", "fixture", at="2010", end="2011"),     # stray bound
    lambda: EventTime(TimeKind.CLOSED_INTERVAL, TimeUnit.YEAR, "UTC", "fixture", start="2011", end="2010"),
    lambda: EventTime(TimeKind.CLOSED_INTERVAL, TimeUnit.YEAR, "UTC", "fixture", start="2010"),
    lambda: EventTime(TimeKind.OPEN_INTERVAL, TimeUnit.YEAR, "UTC", "fixture", start="2010", end="2011"),
    lambda: EventTime(TimeKind.OPEN_INTERVAL, TimeUnit.YEAR, "UTC", "fixture"),                      # unbounded, tz
    lambda: EventTime(TimeKind.FUZZY_WINDOW, TimeUnit.YEAR, "UTC", "fixture", at="2010"),            # no tolerance
    lambda: EventTime(TimeKind.FUZZY_WINDOW, TimeUnit.YEAR, "UTC", "fixture", at="2010",
                      tolerance=TimeTolerance(0, TimeUnit.YEAR)),
    lambda: EventTime(TimeKind.INSTANT, TimeUnit.YEAR, "UTC", "fixture", at="2010",
                      window_shape=WindowShape.NORMAL),                                              # shape off-window
    lambda: EventTime(TimeKind.INSTANT, TimeUnit.DAY, "UTC", "fixture", at="2010-05-12",
                      birth_time_sensitive=True),                                                    # hour unknown
    lambda: EventTime(TimeKind.FUZZY_WINDOW, TimeUnit.HOUR, "UTC", "fixture", at="2010-05-12T14",
                      tolerance=TimeTolerance(1, TimeUnit.DAY), birth_time_sensitive=True),
    lambda: EventTime(TimeKind.OPEN_INTERVAL, TimeUnit.MINUTE, "UTC", "fixture", start="2010-05-12T14:30",
                      birth_time_sensitive=True),
])
def test_ac5_invalid_times_are_refused(build):
    with pytest.raises(EventModelError):
        build()


# ------------------------------------------------------------------ AC6 assertion

@pytest.mark.parametrize("kind", list(AsserterKind))
def test_ac6_every_asserter_kind_round_trips(store, entity, kind):
    certainty = AsserterCertainty.UNSTATED if kind is AsserterKind.SYSTEM_HYPOTHESIS else AsserterCertainty.CERTAIN
    stored = event(entity, claim=assertion(kind, certainty))
    assert store.load(store.persist(stored)).assertion.asserter_kind is kind


def test_ac6_public_record_is_distinct_from_recollection():
    assert AsserterKind.PUBLIC_RECORD is not AsserterKind.USER_RECOLLECTION
    assert {kind.value for kind in AsserterKind} == {"user_recollection", "document", "public_record",
                                                     "system_hypothesis"}


@pytest.mark.parametrize("certainty", [c for c in AsserterCertainty if c is not AsserterCertainty.UNSTATED])
def test_ac6_a_system_hypothesis_declares_no_certainty(certainty):
    with pytest.raises(EventModelError):
        assertion(AsserterKind.SYSTEM_HYPOTHESIS, certainty)


@pytest.mark.parametrize("field,value", [("asserted_at", "2026-01-01"), ("asserted_at", "2026-13-01T00:00:00Z"),
                                         ("asserter_reference", ""), ("method", " ")])
def test_ac6_an_incomplete_assertion_is_refused(field, value):
    with pytest.raises(EventModelError):
        dataclasses.replace(assertion(), **{field: value})


# ------------------------------------------------------------------ AC7 attachment

def test_ac7_an_event_attaches_to_an_existing_entity(store):
    with pytest.raises(StoreError, match="entity"):
        store.persist(event(EntityId.from_number(7)))


def test_ac7_an_assertion_context_names_an_existing_revision_and_chart(store, entity):
    stored = event(entity, context=AssertionContext(1, "rectified", PROV))
    assert store.load(store.persist(stored)).assertion_context == stored.assertion_context
    for context in (AssertionContext(2, "natal", PROV), AssertionContext(1, "no-such-chart", PROV)):
        with pytest.raises(StoreError):
            store.persist(event(entity, day("2011-01-01"), context=context))


def test_ac7_a_context_survives_a_later_entity_correction(store, entity):
    stored = store.persist(event(entity, context=AssertionContext(1, "rectified", PROV)))
    store.entities.append_revision(entity, person("natal"), "rectified chart withdrawn")
    assert store.load(stored).assertion_context.entity_revision == 1
    with pytest.raises(StoreError):
        store.persist(event(entity, day("2011-01-01"), context=AssertionContext(2, "rectified", PROV)))


def test_ac7_no_analysis_candidate_chart_field():
    names = set(model.EVENT_FIELDS)
    assert "assertion_context" in names
    assert not [name for name in names if re.search(r"candidate|evaluated|analysis|charts", name)]


def test_ac7_a_correction_cannot_re_anchor(store, entity):
    other = store.entities.persist(person("natal"))
    stored = store.persist(event(entity, context=AssertionContext(1, "natal", PROV)))
    for moved in (event(other, context=AssertionContext(1, "natal", PROV)),
                  event(entity, context=AssertionContext(1, "rectified", PROV)), event(entity)):
        with pytest.raises(StoreError, match="re-anchor"):
            store.append_revision(stored, moved, "planted re-anchoring")
    assert len(store.history(stored)) == 1


def test_ac7_an_event_is_never_duplicated_across_charts(store, entity):
    store.persist(event(entity, context=AssertionContext(1, "natal", PROV)))
    before = store.issued_count()
    for copy in (event(entity, context=AssertionContext(1, "rectified", PROV)), event(entity),
                 event(entity, context=AssertionContext(1, "natal", PROV))):
        with pytest.raises(StoreError, match="duplicated"):
            store.persist(copy)
    assert store.issued_count() == before


def test_ac7_a_correction_cannot_make_one_event_a_copy_of_another(store, entity):
    store.persist(event(entity))
    second = store.persist(event(entity, day("2011-01-01")))
    with pytest.raises(StoreError, match="duplicated"):
        store.append_revision(second, event(entity), "planted duplication")


# ------------------------------------------------------------------ AC8 immutability

def test_ac8_records_are_frozen(entity):
    stored = event(entity)
    for target, field in ((stored, "event_class"), (stored.time, "at"), (stored.assertion, "asserter_kind"),
                          (confirmation(), "state")):
        with pytest.raises(dataclasses.FrozenInstanceError):
            setattr(target, field, None)


@pytest.mark.parametrize("sql", ["UPDATE event_revisions SET reason = 'x'", "DELETE FROM event_revisions",
                                 "UPDATE event_confirmations SET payload = '{}'", "DELETE FROM event_confirmations"])
def test_ac8_direct_sql_cannot_rewrite_history(store, entity, sql):
    stored = store.persist(event(entity))
    store.confirm(stored, 1, confirmation())
    with pytest.raises(sqlite3.DatabaseError):
        store._db.execute(sql)


def test_ac8_a_correction_appends_with_its_reason(store, entity):
    stored = store.persist(event(entity))
    corrected = event(entity, day("2010-06-12"))
    assert store.append_revision(stored, corrected, "asserter recalled June") == 2
    history = store.history(stored)
    assert [(number, reason) for number, _event, reason in history] == [(1, "first record"), (2, "asserter recalled June")]
    assert history[0][1] == event(entity) and store.load(stored) == corrected
    with pytest.raises(StoreError):
        store.append_revision(stored, corrected, " ")


@pytest.mark.parametrize("change", [{"kind": AsserterKind.PUBLIC_RECORD}, {"at": "2026-01-02T09:00:00Z"}])
def test_ac8_a_correction_cannot_change_the_asserter(store, entity, change):
    stored = store.persist(event(entity))
    with pytest.raises(StoreError, match="asserted"):
        store.append_revision(stored, event(entity, claim=assertion(**change)), "planted laundering")


def test_ac8_a_system_hypothesis_cannot_be_laundered_into_a_human_assertion(store, entity):
    hypothesis = store.persist(event(entity, claim=assertion(AsserterKind.SYSTEM_HYPOTHESIS, AsserterCertainty.UNSTATED)))
    with pytest.raises(StoreError, match="asserted"):
        store.append_revision(hypothesis, event(entity), "planted laundering")
    assert not store.validation_input_permitted(hypothesis)


def test_ac8_no_update_or_delete_api():
    public = {name for name in dir(EventStore) if not name.startswith("_")}
    assert not [name for name in public if re.search(r"update|delete|remove|overwrite|replace|edit", name)]


# ------------------------------------------------------------------ AC9 assertion separate from confirmation

def test_ac9_an_event_starts_unconfirmed_and_confirmation_is_a_separate_record(store, entity):
    stored = store.persist(event(entity))
    assert store.confirmation_state(stored) is ConfirmationState.UNCONFIRMED
    assert "confirmation" not in " ".join(model.EVENT_FIELDS) and "state" not in model.EVENT_FIELDS
    store.confirm(stored, 1, confirmation(ConfirmationState.PARTIALLY_CONFIRMED, "spring, not autumn"))
    assert store.confirmation_state(stored) is ConfirmationState.PARTIALLY_CONFIRMED
    assert store.history(stored)[-1][1] == event(entity)


@pytest.mark.parametrize("state", list(ConfirmationState))
def test_ac9_every_state_round_trips(store, entity, state):
    stored = store.persist(event(entity))
    answer = confirmation(state, "" if state in (ConfirmationState.CONFIRMED, ConfirmationState.UNCONFIRMED) else "why")
    store.confirm(stored, 1, answer)
    assert store.confirmations(stored) == [(1, answer)] and store.confirmation_state(stored) is state


def test_ac9_partial_and_rejected_answers_say_why():
    for state in (ConfirmationState.PARTIALLY_CONFIRMED, ConfirmationState.REJECTED):
        with pytest.raises(EventModelError):
            confirmation(state, " ")


def test_ac9_only_a_human_confirms(store, entity):
    assert {kind.value for kind in ConfirmerKind} == {"subject", "human_reviewer"}
    with pytest.raises(EventModelError):
        dataclasses.replace(confirmation(), confirmer_kind="system")
    record = confirmation_to_record(confirmation())
    record["confirmation"]["confirmer_kind"] = "system"
    with pytest.raises(StoreError, match="human"):
        confirmation_from_record(record)


def test_ac9_a_confirmation_answers_only_its_revision(store, entity):
    stored = store.persist(event(entity))
    store.confirm(stored, 1, confirmation())
    store.append_revision(stored, event(entity, day("2010-06-12")), "asserter recalled June")
    assert store.confirmation_state(stored) is ConfirmationState.UNCONFIRMED
    with pytest.raises(StoreError, match="current revision"):
        store.confirm(stored, 1, confirmation())
    with pytest.raises(StoreError):
        store.confirm(EventRecordId.from_number(9), 1, confirmation())
    assert store.confirmations(stored) == [(1, confirmation())]


def test_ac9_a_system_hypothesis_needs_a_human_confirmation(store, entity):
    hypothesis = store.persist(event(entity, claim=assertion(AsserterKind.SYSTEM_HYPOTHESIS, AsserterCertainty.UNSTATED)))
    assert not store.validation_input_permitted(hypothesis)
    store.confirm(hypothesis, 1, confirmation(ConfirmationState.UNCONFIRMED))
    assert not store.validation_input_permitted(hypothesis)
    store.confirm(hypothesis, 1, confirmation(ConfirmationState.CONFIRMED))
    assert store.validation_input_permitted(hypothesis)


def test_ac9_the_admissibility_table(entity):
    human, system = event(entity), event(entity, claim=assertion(AsserterKind.SYSTEM_HYPOTHESIS,
                                                                 AsserterCertainty.UNSTATED))
    table = {(record is system, state): validation_input_permitted(record, state)
             for record in (human, system) for state in ConfirmationState}
    assert table == {
        (False, ConfirmationState.UNCONFIRMED): True, (False, ConfirmationState.CONFIRMED): True,
        (False, ConfirmationState.PARTIALLY_CONFIRMED): True, (False, ConfirmationState.REJECTED): False,
        (True, ConfirmationState.UNCONFIRMED): False, (True, ConfirmationState.CONFIRMED): True,
        (True, ConfirmationState.PARTIALLY_CONFIRMED): True, (True, ConfirmationState.REJECTED): False,
    }


# ------------------------------------------------------------------ AC10 no analytical content

FORBIDDEN_KEYS = ["interpretation", "rule_id", "planet", "dasha", "score", "weight", "confidence", "prediction"]


@pytest.mark.parametrize("key", FORBIDDEN_KEYS)
@pytest.mark.parametrize("level", ["event", "time", "assertion", "assertion_context", "provenance"])
def test_ac10_analytical_content_is_refused_at_every_level(entity, key, level):
    record = event_to_record(event(entity, context=AssertionContext(1, "natal", PROV)))
    target = record["event"] if level == "event" else record["event"][level]
    target[key] = 1
    with pytest.raises(StoreError, match="refused"):
        event_from_record(record)


@pytest.mark.parametrize("key", FORBIDDEN_KEYS)
def test_ac10_analytical_content_is_refused_on_a_confirmation(key):
    record = confirmation_to_record(confirmation())
    record["confirmation"][key] = 1
    with pytest.raises(StoreError, match="refused"):
        confirmation_from_record(record)


def test_ac10_the_store_refuses_a_planted_payload(store, entity):
    stored = store.persist(event(entity))
    payload = store._db.execute("SELECT payload FROM event_revisions").fetchone()[0]
    store._db.execute("INSERT INTO event_revisions (event_id, revision, entity_id, payload, reason) VALUES (?, 2, ?, ?, ?)",
                      (stored.value, entity.value, payload.replace('"subclass":null', '"subclass":null,"score":1'), "x"))
    with pytest.raises(StoreError, match="refused"):
        store.load(stored)


def test_ac10_no_scoring_interpretation_or_rule_field_in_any_model_dataclass():
    forbidden = re.compile(r"score|weight|confidence|probabilit|fit|rank|interpret|rule|planet|dasha|yoga|house",
                           re.IGNORECASE)
    for module in (model, event_classes):
        for obj in vars(module).values():
            if isinstance(obj, type) and dataclasses.is_dataclass(obj):
                assert not [f.name for f in dataclasses.fields(obj) if forbidden.search(f.name)], obj.__name__


# ------------------------------------------------------------------ AC11 synthetic only

def test_ac11_synthetic_only(entity):
    with pytest.raises(EventModelError):
        dataclasses.replace(event(entity), data_class="real")
    record = event_to_record(event(entity))
    record["event"]["data_class"] = "real"
    with pytest.raises(ValueError):
        event_from_record(record)


# ------------------------------------------------------------------ AC12 round trip

def test_ac12_events_and_confirmations_round_trip(store, entity):
    stored = event(entity, TIMES["fuzzy hour window"], LAYOFF, assertion(AsserterKind.DOCUMENT), subclass="redundancy",
                   domain="career", context=AssertionContext(1, "natal", PROV))
    identifier = store.persist(stored)
    assert event_from_record(event_to_record(stored)) == stored and store.load(identifier) == stored
    answer = confirmation(ConfirmationState.REJECTED, "never happened")
    store.confirm(identifier, 1, answer)
    assert confirmation_from_record(confirmation_to_record(answer)) == answer
    assert store.event_ids() == [identifier] and store.confirmations(identifier) == [(1, answer)]


# ------------------------------------------------------------------ AC1, AC13 the gate and its controls

def test_ac1_the_real_registration_passes():
    assert gate.check_registration(gate.NAMING.read_text(encoding="utf-8")) == []


@pytest.mark.parametrize("old,new", [(r"`EVR-\d{8}` | 8 |", r"`EVR-\d{6}` | 8 |"),
                                     (r"`EVR-\d{8}` | 8 |", r"`EVR-\d{8}` | 10 |")])
def test_ac1_a_wrong_registration_fails(old, new):
    text = gate.NAMING.read_text(encoding="utf-8")
    assert old in text
    assert any(error.startswith("V1") for error in gate.check_registration(text.replace(old, new)))


def test_ac1_a_missing_or_duplicated_registration_fails():
    text = gate.NAMING.read_text(encoding="utf-8")
    row = next(line for line in text.splitlines() if "`EVR-" in line)
    assert gate.check_registration(text.replace(row + "\n", ""))[0].startswith("V1")
    assert gate.check_registration(text.replace(row, row + "\n" + row))[0].startswith("V1")


def test_ac13_a_literal_identifier_in_production_code_fails(tmp_path):
    (tmp_path / "engine").mkdir()
    (tmp_path / "engine" / "planted.py").write_text("X = '" + "EVR-" + "00000001" + "'\n", encoding="utf-8")
    (tmp_path / "engine" / "tests").mkdir()
    (tmp_path / "engine" / "tests" / "fixture.py").write_text("X = '" + "EVR-" + "00000001" + "'\n", encoding="utf-8")
    errors = gate.check_literals(tmp_path, ["engine/planted.py", "engine/tests/fixture.py"])
    assert len(errors) == 1 and errors[0].startswith("V2 engine/planted.py")


def test_ac13_the_real_tree_has_no_literal_identifier():
    assert gate.check_literals(gate.ROOT, gate.tracked_files(gate.ROOT)) == []


def test_ac13_a_real_store_passes_and_a_corrupted_one_fails(tmp_path):
    path = tmp_path / "evidence.sqlite"
    with EventStore(path) as store:
        owner = store.entities.persist(person("natal"))
        first = store.persist(event(owner))
        store.persist(event(owner, day("2011-01-01")))
        store.confirm(first, 1, confirmation())
    assert gate.check_store(path) == []
    db = sqlite3.connect(path)
    db.execute("INSERT INTO event_revisions (event_id, revision, entity_id, payload, reason) VALUES (?, 3, ?, '{}', 'x')",
               (first.value, owner.value))
    db.execute("INSERT INTO event_confirmations (event_id, revision, payload) VALUES (?, 7, '{}')", (first.value,))
    db.execute("DROP TRIGGER event_issuer_never_decreases")
    db.execute("UPDATE event_issuer SET last_number = 1")
    db.commit()
    db.close()
    errors = gate.check_store(path)
    assert any("not 1..n" in error for error in errors)
    assert any("exceeds the issuer" in error for error in errors)
    assert any("does not exist" in error for error in errors)


def test_ac13_the_gate_is_in_the_ci_sweep_with_a_negative_control():
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "python scripts/check_event_identifiers.py" in workflow
    assert "the EVR gate did NOT flag a planted violation" in workflow
