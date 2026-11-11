"""WP-E3 acceptance tests (ADR-0116 s5): the historical ledger, protected holdouts and protocols.

Every record here is synthetic.
"""

from __future__ import annotations

import dataclasses
import json
import re
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from engine.evidence import ledger as model  # noqa: E402
from engine.evidence.entity import (  # noqa: E402
    ChartCandidate, DataClass, EntityKind, OriginCertainty, OriginMoment, Person, RecordProvenance, Shape,
)
from engine.evidence.event_classes import SEED  # noqa: E402
from engine.evidence.event_identifiers import EventRecordId  # noqa: E402
from engine.evidence.events import (  # noqa: E402
    Assertion, AsserterCertainty, AsserterKind, Confirmation, ConfirmationState, ConfirmerKind, EventRecord,
    EventTime, TimeKind, TimeUnit,
)
from engine.evidence.ledger import (  # noqa: E402
    PROCEDURE, Elicitation, HistoricalLedger, LedgerError, Outcome, Protocol, Purpose, content_hash,
    entry_from_record, entry_to_record, holdout_from_record, holdout_to_record, leakage_findings, ordered_selection,
    protocol_from_record, protocol_to_record,
)

PROV = RecordProvenance(source="synthetic fixture", method="hand-written test data", schema_version="h2-v2")
VOL, EXPECT, NULL = Elicitation.VOLUNTEERED, Elicitation.PROMPTED_BY_EXPECTATION, Elicitation.PROMPTED_FOR_NULL_PERIOD


def person():
    chart = ChartCandidate(label="natal", origin=OriginMoment(local_datetime="2000-01-01T12:00:00", timezone="UTC",
                                                              timezone_source="fixture", latitude=10.0, longitude=20.0,
                                                              precision="minute"),
                           origin_certainty=OriginCertainty.REPORTED, provenance=PROV)
    return Person(kind=EntityKind.PERSON, shape=Shape.ORIGIN, charts=(chart,), applicable_domains=("career",),
                  applicable_systems=("parashari",), provenance=PROV, data_class=DataClass.SYNTHETIC)


def answer(state, statement=""):
    if state in (ConfirmationState.PARTIALLY_CONFIRMED, ConfirmationState.REJECTED) and not statement:
        statement = "stated reason"
    return Confirmation(state=state, confirmer_kind=ConfirmerKind.SUBJECT, confirmer_reference="synthetic subject",
                        confirmed_at="2026-02-01T09:00:00Z", statement=statement, provenance=PROV)


class World:
    """A ledger over one synthetic entity, with helpers to make answered events."""

    def __init__(self, path):
        self.ledger = HistoricalLedger(path)
        self.entity = self.ledger.events.entities.persist(person())
        self.made = 0

    def event(self, state=ConfirmationState.CONFIRMED, cls=0, kind=AsserterKind.USER_RECOLLECTION):
        self.made += 1
        certainty = AsserterCertainty.UNSTATED if kind is AsserterKind.SYSTEM_HYPOTHESIS else AsserterCertainty.CERTAIN
        record = EventRecord(entity=self.entity, event_class=SEED[cls].class_id,
                             time=EventTime(TimeKind.INSTANT, TimeUnit.DAY, "UTC", "fixture",
                                            at=f"2010-01-{self.made:02d}"),
                             assertion=Assertion(asserter_kind=kind, asserter_reference="synthetic asserter",
                                                 asserted_at="2026-01-01T09:00:00Z", method="interview",
                                                 asserter_certainty=certainty),
                             provenance=PROV, data_class=DataClass.SYNTHETIC)
        identifier = self.ledger.events.persist(record)
        if state is not None:
            self.ledger.events.confirm(identifier, 1, answer(state))
        return identifier

    def admitted(self, count, elicitation=VOL, **kwargs):
        out = []
        for _ in range(count):
            identifier = self.event(**kwargs)
            self.ledger.admit(identifier, elicitation, PROV)
            out.append(identifier)
        return out


def protocol(holdout, minimum_n=2, **changes):
    base = Protocol(holdout=holdout, event_classes=(SEED[0].class_id,), hypotheses=("synthetic hypothesis",),
                    rule_references=(), development_set="entries outside the holdout", hypothesis_count=1,
                    event_count=4, multiple_comparison_method="Bonferroni", effect_size_measures=("risk difference",),
                    negative_controls=("events shifted to random dates",), replication="not feasible: synthetic",
                    minimum_n=minimum_n, provenance=PROV, data_class=DataClass.SYNTHETIC)
    return dataclasses.replace(base, **changes)


@pytest.fixture()
def world(tmp_path):
    instance = World(tmp_path / "evidence.sqlite")
    yield instance
    instance.ledger.close()


# ------------------------------------------------------------------ AC1 admission

@pytest.mark.parametrize("state,outcome", [(ConfirmationState.CONFIRMED, Outcome.PAST_CONFIRMED),
                                           (ConfirmationState.PARTIALLY_CONFIRMED, Outcome.PAST_PARTIALLY_CONFIRMED),
                                           (ConfirmationState.REJECTED, Outcome.REJECTED)])
def test_ac1_an_answered_event_is_admitted_with_its_outcome(world, state, outcome):
    identifier = world.event(state)
    world.ledger.admit(identifier, VOL, PROV)
    (entry,) = world.ledger.read(Purpose.AUDIT)
    assert (entry.event, entry.event_revision, entry.answer_index, entry.outcome) == (identifier, 1, 1, outcome)
    assert entry.event_class == SEED[0].class_id


@pytest.mark.parametrize("state", [None, ConfirmationState.UNCONFIRMED])
def test_ac1_an_unanswered_event_is_refused(world, state):
    identifier = world.event(state)
    with pytest.raises(LedgerError, match="no human answer"):
        world.ledger.admit(identifier, VOL, PROV)


def test_ac1_an_event_corrected_since_its_answer_is_unanswered(world):
    identifier = world.event()
    record = world.ledger.events.load(identifier)
    world.ledger.events.append_revision(identifier, dataclasses.replace(
        record, time=EventTime(TimeKind.INSTANT, TimeUnit.DAY, "UTC", "fixture", at="2011-01-01")), "recalled 2011")
    with pytest.raises(LedgerError, match="no human answer"):
        world.ledger.admit(identifier, VOL, PROV)


def test_ac1_an_event_is_admitted_once(world):
    (identifier,) = world.admitted(1)
    with pytest.raises(LedgerError, match="already"):
        world.ledger.admit(identifier, VOL, PROV)
    with pytest.raises(StoreErrorType):
        world.ledger.admit(EventRecordId.from_number(99), VOL, PROV)


StoreErrorType = model.StoreError


# ------------------------------------------------------------------ AC2 elicitation

@pytest.mark.parametrize("elicitation", list(Elicitation))
def test_ac2_every_elicitation_kind_is_recorded(world, elicitation):
    world.admitted(1, elicitation)
    assert world.ledger.read(Purpose.AUDIT)[0].elicitation is elicitation


@pytest.mark.parametrize("bad", [None, "volunteered", "prompted"])
def test_ac2_a_missing_or_unknown_elicitation_is_refused(world, bad):
    identifier = world.event()
    with pytest.raises(LedgerError, match="elicited"):
        world.ledger.admit(identifier, bad, PROV)
    record = entry_to_record(dataclasses.replace(world.ledger._entry_for(identifier, VOL, PROV)))
    record["entry"]["elicitation"] = "prompted"
    with pytest.raises(ValueError):
        entry_from_record(record)


def test_ac2_the_populations_are_counted_apart(world):
    world.admitted(2, VOL)
    world.admitted(1, EXPECT)
    world.admitted(3, NULL)
    counts = world.ledger.counts(Purpose.DEVELOPMENT)["elicitation"]
    assert {key: len(members) for key, members in counts.items()} == {
        "volunteered": 2, "prompted_by_expectation": 1, "prompted_for_null_period": 3}


# ------------------------------------------------------------------ AC3 rejections

def test_ac3_a_rejected_hypothesis_is_retained_and_counted(world):
    rejected = world.admitted(2, kind=AsserterKind.SYSTEM_HYPOTHESIS, state=ConfirmationState.REJECTED)
    world.admitted(1)
    for purpose in Purpose:
        if purpose is Purpose.PROTECTED_VALIDATION:
            continue
        assert world.ledger.counts(purpose)["outcome"]["rejected"] == tuple(rejected)
    with pytest.raises(sqlite3.DatabaseError):
        world.ledger._db.execute("DELETE FROM ledger_entries")


def test_ac3_no_api_removes_or_hides_an_entry():
    public = {name for name in dir(HistoricalLedger) if not name.startswith("_")}
    assert not [name for name in public if re.search(r"delete|remove|clear|hide|drop|unprotect|update|edit", name)]


# ------------------------------------------------------------------ AC4 append-only, correction

@pytest.mark.parametrize("table", ["ledger_entries", "eligible_sets", "eligible_members", "holdouts",
                                   "protected_events", "protocols", "access_log"])
def test_ac4_direct_sql_cannot_rewrite_any_table(world, table):
    members = world.admitted(4)
    holdout = world.ledger.freeze_and_select("all four", members, 2)
    world.ledger.register_protocol(protocol(holdout))
    world.ledger.read(Purpose.AUDIT)
    column = {"ledger_entries": "reason", "eligible_sets": "payload", "eligible_members": "set_number",
              "holdouts": "payload", "protected_events": "holdout_number", "protocols": "payload",
              "access_log": "note"}[table]
    for sql in (f"UPDATE {table} SET {column} = {column}", f"DELETE FROM {table}"):
        with pytest.raises(sqlite3.DatabaseError, match="append-only"):
            world.ledger._db.execute(sql)


def test_ac4_a_correction_appends_and_keeps_the_superseded_entry(world):
    identifier = world.event()
    first = world.ledger.admit(identifier, VOL, PROV)
    record = world.ledger.events.load(identifier)
    world.ledger.events.append_revision(identifier, dataclasses.replace(
        record, time=EventTime(TimeKind.INSTANT, TimeUnit.DAY, "UTC", "fixture", at="2011-01-01")), "recalled 2011")
    world.ledger.events.confirm(identifier, 2, answer(ConfirmationState.PARTIALLY_CONFIRMED, "spring, not autumn"))
    second = world.ledger.correct(identifier, VOL, PROV, "event corrected and re-answered")
    history = world.ledger.history(Purpose.AUDIT, identifier)
    assert [(number, supersedes, reason) for number, _entry, supersedes, reason in history] == [
        (first, None, "first record"), (second, first, "event corrected and re-answered")]
    assert history[0][1].event_revision == 1 and history[1][1].event_revision == 2
    assert world.ledger.read(Purpose.AUDIT)[0].outcome is Outcome.PAST_PARTIALLY_CONFIRMED
    with pytest.raises(LedgerError, match="change something"):
        world.ledger.correct(identifier, VOL, PROV, "no change")
    with pytest.raises(LedgerError):
        world.ledger.correct(identifier, VOL, PROV, " ")
    with pytest.raises(sqlite3.IntegrityError):
        world.ledger._db.execute("INSERT INTO ledger_entries (event_id, supersedes, payload, reason) VALUES (?, ?, ?, ?)",
                                 (identifier.value, first, "{}", "a second branch"))


def test_ac4_a_correction_can_change_the_elicitation_record(world):
    (identifier,) = world.admitted(1)
    world.ledger.correct(identifier, NULL, PROV, "it was prompted for a null period")
    assert world.ledger.read(Purpose.AUDIT)[0].elicitation is NULL
    assert len(world.ledger.history(Purpose.AUDIT, identifier)) == 2


# ------------------------------------------------------------------ AC5 decomposable counts, nothing computed

def test_ac5_every_count_returns_its_members_and_the_partitions_sum(world):
    world.admitted(2, cls=0)
    world.admitted(1, cls=4, state=ConfirmationState.PARTIALLY_CONFIRMED)
    world.admitted(1, cls=4, state=ConfirmationState.REJECTED, elicitation=EXPECT)
    counts = world.ledger.counts(Purpose.AUDIT)
    total = set(counts["total"])
    assert len(total) == 4
    for axis in ("event_class", "elicitation", "outcome"):
        parts = [set(members) for members in counts[axis].values()]
        assert set().union(*parts) == total and sum(len(part) for part in parts) == len(total)
    assert {key: len(value) for key, value in counts["event_class"].items()} == {SEED[0].class_id: 2,
                                                                                  SEED[4].class_id: 2}


def test_ac5_nothing_scores_or_divides():
    forbidden = re.compile(r"score|weight|confidence|probabilit|fit|rank|rate|ratio|accuracy|percent|mean",
                           re.IGNORECASE)
    for obj in vars(model).values():
        if isinstance(obj, type) and dataclasses.is_dataclass(obj):
            assert not [f.name for f in dataclasses.fields(obj) if forbidden.search(f.name)], obj.__name__
    public = [name for name in dir(HistoricalLedger) if not name.startswith("_")]
    assert not [name for name in public if forbidden.search(name)]
    source = (ROOT / "engine" / "evidence" / "ledger.py").read_text(encoding="utf-8")
    assert not re.search(r"[A-Za-z_)\]] / [A-Za-z_(]", source), "the ledger divides nothing"


# ------------------------------------------------------------------ AC6, AC7 freeze and selection, locked together

def test_ac6_a_frozen_set_records_criteria_members_and_hash(world):
    members = world.admitted(5)
    number = world.ledger.freeze_and_select("first five confirmed", reversed(members), 2)
    holdout = world.ledger.holdout(number)
    assert holdout.criteria == "first five confirmed" and holdout.members == tuple(sorted(members))
    assert holdout.content_hash == content_hash(members) and holdout.procedure == PROCEDURE
    assert holdout_from_record(holdout_to_record(holdout)) == holdout


def test_ac7_the_selection_reproduces_from_its_record(world):
    members = world.admitted(8)
    number = world.ledger.freeze_and_select("eight", members, 3)
    holdout = world.ledger.holdout(number)
    assert ordered_selection(holdout.seed, holdout.members, holdout.size) == holdout.selected
    assert world.ledger.reproduces(number) and world.ledger.protected() == frozenset(holdout.selected)
    assert len(holdout.selected) == 3 and set(holdout.selected) <= set(members)


def test_ac7_the_procedure_is_seed_sensitive_and_deterministic():
    members = [EventRecordId.from_number(n) for n in range(1, 41)]
    assert ordered_selection("a" * 64, members, 10) == ordered_selection("a" * 64, list(reversed(members)), 10)
    assert ordered_selection("a" * 64, members, 10) != ordered_selection("b" * 64, members, 10)
    for size in (0, 41):
        with pytest.raises(LedgerError):
            ordered_selection("a" * 64, members, size)


def test_ac7_the_store_draws_the_seed(world):
    first = world.ledger.holdout(world.ledger.freeze_and_select("one", world.admitted(3), 1))
    second = world.ledger.holdout(world.ledger.freeze_and_select("two", world.admitted(3), 1))
    assert first.seed != second.seed and re.fullmatch(r"[0-9a-f]{64}", first.seed)
    assert "seed" not in HistoricalLedger.freeze_and_select.__code__.co_varnames[:4]


@pytest.mark.parametrize("variant", ["same set", "reordered", "subset", "superset", "overlap"])
def test_ac7_no_reselection_through_an_equivalent_or_overlapping_set(world, variant):
    members = world.admitted(4)
    extra = world.admitted(2)
    world.ledger.freeze_and_select("first", members, 2)
    before = world.ledger.holdout(1)
    again = {"same set": members, "reordered": list(reversed(members)), "subset": members[:2],
             "superset": members + extra, "overlap": members[3:] + extra}[variant]
    with pytest.raises(LedgerError, match="frozen set"):
        world.ledger.freeze_and_select("again", again, 1)
    assert world.ledger.holdout(1) == before and world.ledger.protected() == frozenset(before.selected)
    with pytest.raises(LedgerError):
        world.ledger.holdout(2)


def test_ac7_a_second_selection_of_a_frozen_set_is_refused_by_the_database(world):
    world.ledger.freeze_and_select("first", world.admitted(3), 1)
    with pytest.raises(sqlite3.IntegrityError):
        world.ledger._db.execute("INSERT INTO holdouts (set_number, after_access, payload) VALUES (1, 0, '{}')")


@pytest.mark.parametrize("make", ["rejected", "not admitted", "duplicate", "empty", "size"])
def test_ac6_only_confirmed_ledger_entries_are_eligible(world, make):
    members = world.admitted(2)
    if make == "rejected":
        members += world.admitted(1, state=ConfirmationState.REJECTED)
    elif make == "not admitted":
        members.append(world.event())
    elif make == "duplicate":
        members.append(members[0])
    elif make == "empty":
        members = []
    with pytest.raises(LedgerError):
        world.ledger.freeze_and_select("bad", members, 5 if make == "size" else 1)
    assert world.ledger.protected() == frozenset()


# ------------------------------------------------------------------ AC8 protection

def test_ac8_protection_cannot_be_cleared_and_survives_a_correction(world):
    members = world.admitted(4)
    holdout = world.ledger.holdout(world.ledger.freeze_and_select("four", members, 2))
    target = holdout.selected[0]
    for sql in ("DELETE FROM protected_events", "UPDATE protected_events SET holdout_number = 9"):
        with pytest.raises(sqlite3.DatabaseError):
            world.ledger._db.execute(sql)
    world.ledger.events.confirm(target, 1, answer(ConfirmationState.REJECTED, "on reflection, no"))
    world.ledger.correct(target, VOL, PROV, "answer changed")
    assert target in world.ledger.protected() and world.ledger.reproduces(1)
    assert target not in {entry.event for entry in world.ledger.read(Purpose.DEVELOPMENT)}


# ------------------------------------------------------------------ AC9 purpose-declared access, logging, leakage

@pytest.mark.parametrize("purpose", sorted(model.EXCLUDED_FROM_PROTECTED, key=lambda p: p.value))
def test_ac9_excluded_purposes_never_see_a_protected_entry(world, purpose):
    members = world.admitted(6)
    holdout = world.ledger.holdout(world.ledger.freeze_and_select("six", members, 2))
    visible = {entry.event for entry in world.ledger.read(purpose)}
    assert visible == set(members) - set(holdout.selected)
    with pytest.raises(LedgerError, match="not available"):
        world.ledger.read(purpose, event_id=holdout.selected[0])
    assert set(world.ledger.counts(purpose)["total"]) == visible
    log = world.ledger.access_log()
    assert [(row[1], row[3]) for row in log] == [(purpose, True), (purpose, False), (purpose, True)]
    assert log[1][4] == (holdout.selected[0].value,)
    assert leakage_findings(world.ledger.path) == []


def test_ac9_a_read_must_declare_a_purpose_and_an_undeclared_one_is_logged(world):
    (identifier,) = world.admitted(1)
    for bad in (None, "audit"):
        with pytest.raises(LedgerError, match="Purpose"):
            world.ledger.read(bad, event_id=identifier)
    assert [(row[1], row[3], row[4]) for row in world.ledger.access_log()] == [
        (model.UNDECLARED, False, (identifier.value,))] * 2
    assert leakage_findings(world.ledger.path) == []
    world.ledger._db.execute("INSERT INTO access_log (purpose, protocol_number, granted, served, note) "
                             "VALUES ('undeclared', NULL, 1, '[]', 'planted')")
    assert any(f.startswith("L4") for f in leakage_findings(world.ledger.path))


def test_ac9_the_leakage_check_flags_planted_leaks(world):
    members = world.admitted(6)
    holdout = world.ledger.holdout(world.ledger.freeze_and_select("six", members, 2))
    world.ledger.register_protocol(protocol(1))
    world.ledger.read(Purpose.PROTECTED_VALIDATION, 1)
    assert leakage_findings(world.ledger.path) == []
    db = world.ledger._db
    leaked, outside = holdout.selected[0].value, (set(members) - set(holdout.selected)).pop().value
    db.execute("INSERT INTO access_log (purpose, protocol_number, granted, served, note) VALUES (?, NULL, 1, ?, 'x')",
               ("tuning", json.dumps([leaked])))
    db.execute("INSERT INTO access_log (purpose, protocol_number, granted, served, note) VALUES (?, 7, 1, '[]', 'x')",
               ("protected_validation",))
    db.execute("INSERT INTO access_log (purpose, protocol_number, granted, served, note) VALUES (?, 1, 1, ?, 'x')",
               ("protected_validation", json.dumps([outside])))
    (last,) = db.execute("SELECT MAX(access_number) FROM access_log").fetchone()
    db.execute("INSERT INTO protocols (holdout_number, after_access, payload) VALUES (1, ?, '{}')", (last + 5,))
    db.execute("INSERT INTO access_log (purpose, protocol_number, granted, served, note) VALUES (?, 2, 1, '[]', 'x')",
               ("protected_validation",))
    findings = leakage_findings(world.ledger.path)
    assert any(f.startswith("L1") and leaked in f for f in findings)
    assert any(f.startswith("L2") and "no registered protocol" in f for f in findings)
    assert any(f.startswith("L2") and "before protocol 2" in f for f in findings)
    assert any(f.startswith("L3") and outside in f for f in findings)


def test_ac9_a_development_read_before_the_lock_is_not_a_leak(world):
    members = world.admitted(4)
    world.ledger.read(Purpose.DEVELOPMENT)
    world.ledger.freeze_and_select("four", members, 2)
    assert leakage_findings(world.ledger.path) == []


def test_ac9_disclosed_limit_reads_outside_the_ledger_are_not_controlled(world):
    """CEO clarification 2: the purpose check covers ledger reads only. This test records that limit."""

    members = world.admitted(3)
    holdout = world.ledger.holdout(world.ledger.freeze_and_select("three", members, 1))
    before = len(world.ledger.access_log())
    assert world.ledger.events.load(holdout.selected[0]).event_class == SEED[0].class_id
    assert world.ledger._db.execute("SELECT COUNT(*) FROM event_revisions").fetchone()[0] == 3
    assert len(world.ledger.access_log()) == before
    assert "does NOT control" in model.__doc__ and "never that no process anywhere" in model.__doc__


# CEO HOLD on PR #50, defect 1: history() served protected entries with no purpose and no log row.

def _locked_with_protocol(world, count=6, size=2):
    members = world.admitted(count)
    holdout = world.ledger.holdout(world.ledger.freeze_and_select("set", members, size))
    world.ledger.register_protocol(protocol(1, minimum_n=size))
    outside = sorted(set(members) - set(holdout.selected))
    return members, holdout, outside


@pytest.mark.parametrize("purpose", sorted(model.EXCLUDED_FROM_PROTECTED, key=lambda p: p.value))
def test_ac9_history_of_a_protected_event_is_refused_and_logged_for_excluded_purposes(world, purpose):
    _members, holdout, outside = _locked_with_protocol(world)
    target = holdout.selected[0]
    before = len(world.ledger.access_log())
    with pytest.raises(LedgerError, match="not available"):
        world.ledger.history(purpose, target)
    assert len(world.ledger.history(purpose, outside[0])) == 1
    log = world.ledger.access_log()[before:]
    assert [(row[1], row[3], row[4]) for row in log] == [(purpose, False, (target.value,)),
                                                         (purpose, True, (outside[0].value,))]
    assert log[1][5] == "granted: history"
    assert leakage_findings(world.ledger.path) == []


def test_ac9_a_protected_events_superseded_history_is_never_served_to_excluded_purposes(world):
    _members, holdout, _outside = _locked_with_protocol(world)
    target = holdout.selected[0]
    world.ledger.events.confirm(target, 1, answer(ConfirmationState.REJECTED, "on reflection, no"))
    world.ledger.correct(target, VOL, PROV, "answer changed")
    for purpose in model.EXCLUDED_FROM_PROTECTED:
        with pytest.raises(LedgerError, match="not available"):
            world.ledger.history(purpose, target)
    assert len(world.ledger.history(Purpose.AUDIT, target)) == 2


def test_ac9_history_for_audit_and_protected_validation_follows_read(world):
    _members, holdout, outside = _locked_with_protocol(world)
    target = holdout.selected[0]
    assert world.ledger.history(Purpose.AUDIT, target)[0][1].event == target
    assert world.ledger.history(Purpose.PROTECTED_VALIDATION, target, 1)[0][1].event == target
    for refused, match in ((lambda: world.ledger.history(Purpose.PROTECTED_VALIDATION, outside[0], 1), "not available"),
                           (lambda: world.ledger.history(Purpose.PROTECTED_VALIDATION, target), "registered protocol"),
                           (lambda: world.ledger.history(None, target), "Purpose"),
                           (lambda: world.ledger.history(Purpose.AUDIT, None), "names one event"),
                           (lambda: world.ledger.history(Purpose.AUDIT, EventRecordId.from_number(99999999)),
                            "not available")):
        before = len(world.ledger.access_log())
        with pytest.raises(LedgerError, match=match):
            refused()
        log = world.ledger.access_log()
        assert len(log) == before + 1 and log[-1][3] is False
    assert world.ledger.access_log()[-3][1] == model.UNDECLARED
    assert leakage_findings(world.ledger.path) == []


# CEO HOLD on PR #50, defect 2: a malformed read could raise past the log, or log the wrong protocol.

MALFORMED = [
    ("event_id as text", {"event_id": "EVR-00000001"}),
    ("event_id as a number", {"event_id": 1}),
    ("protocol as text that SQLite would match", {"protocol": "1"}),
    ("protocol as a bool", {"protocol": True}),
    ("protocol as a float", {"protocol": 1.0}),
    ("protocol zero", {"protocol": 0}),
    ("protocol negative", {"protocol": -1}),
    ("protocol beyond 64 bits", {"protocol": 2 ** 70}),
    ("protocol at the 64-bit limit", {"protocol": 2 ** 63}),
]


#: counts() takes no event_id, so those requests cannot be expressed through it and are not generated.
MALFORMED_CASES = [(method, label, request_) for method in ("read", "counts", "history")
                   for label, request_ in MALFORMED if not (method == "counts" and "event_id" in request_)]


@pytest.mark.parametrize("method,label,request_", MALFORMED_CASES,
                         ids=[f"{method}-{label}" for method, label, _ in MALFORMED_CASES])
def test_ac9_a_malformed_request_is_a_logged_refusal(world, method, label, request_):
    _members, holdout, _outside = _locked_with_protocol(world)
    kwargs = {"protocol": 1, **request_}
    if method == "history":
        kwargs.setdefault("event_id", holdout.selected[0])
        call = lambda: world.ledger.history(Purpose.PROTECTED_VALIDATION, kwargs["event_id"], kwargs["protocol"])
    elif method == "counts":
        call = lambda: world.ledger.counts(Purpose.PROTECTED_VALIDATION, kwargs["protocol"])
    else:
        call = lambda: world.ledger.read(Purpose.PROTECTED_VALIDATION, kwargs["protocol"], kwargs.get("event_id"))
    before = len(world.ledger.access_log())
    with pytest.raises(LedgerError, match="refused"):
        call()
    log = world.ledger.access_log()
    assert len(log) == before + 1, label
    number, purpose, logged_protocol, granted, served, _note = log[-1]
    assert (purpose, granted) == (Purpose.PROTECTED_VALIDATION, False)
    assert logged_protocol == (1 if "protocol" not in request_ else None)
    assert served == (() if "event_id" in request_ or method != "history" else (holdout.selected[0].value,))
    assert leakage_findings(world.ledger.path) == []


def test_ac9_an_unexpected_failure_while_deciding_is_a_logged_refusal(world, monkeypatch):
    (identifier,) = world.admitted(1)

    def broken(*_args):
        raise RuntimeError("planted failure")

    monkeypatch.setattr(world.ledger, "_visible", broken)
    for call in (lambda: world.ledger.read(Purpose.AUDIT), lambda: world.ledger.history(Purpose.AUDIT, identifier)):
        before = len(world.ledger.access_log())
        with pytest.raises(LedgerError, match="malformed request refused: RuntimeError: planted failure"):
            call()
        log = world.ledger.access_log()
        assert len(log) == before + 1 and log[-1][3] is False
    monkeypatch.undo()
    assert world.ledger.read(Purpose.AUDIT)[0].event == identifier


# ------------------------------------------------------------------ AC10 protocols

def test_ac10_a_protocol_records_every_field_and_is_immutable(world):
    world.ledger.freeze_and_select("four", world.admitted(4), 2)
    registered = protocol(1)
    number = world.ledger.register_protocol(registered)
    assert world.ledger.protocol(number) == registered
    assert protocol_from_record(protocol_to_record(registered)) == registered
    assert set(model.PROTOCOL_FIELDS) >= {"event_classes", "hypotheses", "rule_references", "development_set",
                                          "holdout", "hypothesis_count", "event_count", "multiple_comparison_method",
                                          "effect_size_measures", "negative_controls", "replication", "minimum_n"}
    with pytest.raises(sqlite3.DatabaseError):
        world.ledger._db.execute("UPDATE protocols SET payload = '{}'")


@pytest.mark.parametrize("change", [{"minimum_n": 0}, {"hypothesis_count": 2}, {"hypotheses": ()},
                                    {"rule_references": ("a rule",)}, {"event_classes": ("EV-CAR-999",)},
                                    {"multiple_comparison_method": " "}, {"effect_size_measures": ()},
                                    {"negative_controls": ()}, {"replication": ""}, {"data_class": "real"}])
def test_ac10_an_incomplete_protocol_is_refused(change):
    with pytest.raises(LedgerError):
        protocol(1, **change)


def test_ac10_a_protocol_names_a_locked_holdout(world):
    with pytest.raises(LedgerError, match="locked holdout"):
        world.ledger.register_protocol(protocol(1))


def test_ac10_protected_validation_needs_a_protocol_and_its_minimum_n(world):
    world.ledger.freeze_and_select("first", world.admitted(4), 2)
    world.ledger.freeze_and_select("second", world.admitted(4), 3)
    small, large = world.ledger.register_protocol(protocol(1, minimum_n=3)), world.ledger.register_protocol(protocol(2))
    with pytest.raises(LedgerError, match="registered protocol"):
        world.ledger.read(Purpose.PROTECTED_VALIDATION)
    with pytest.raises(LedgerError, match="no protocol 9"):
        world.ledger.read(Purpose.PROTECTED_VALIDATION, 9)
    with pytest.raises(LedgerError, match="minimum N"):
        world.ledger.read(Purpose.PROTECTED_VALIDATION, small)
    served = {entry.event for entry in world.ledger.read(Purpose.PROTECTED_VALIDATION, large)}
    assert served == set(world.ledger.holdout(2).selected)
    for purpose in (Purpose.AUDIT, Purpose.TUNING):
        with pytest.raises(LedgerError, match="names no protocol"):
            world.ledger.read(purpose, large)
    assert [row[3] for row in world.ledger.access_log()] == [False, False, False, True, False, False]
    assert leakage_findings(world.ledger.path) == []


# ------------------------------------------------------------------ AC11 disclosure

def test_ac11_only_audit_and_protected_validation_counts_include_protected_entries(world):
    members = world.admitted(5)
    holdout = world.ledger.holdout(world.ledger.freeze_and_select("five", members, 2))
    number = world.ledger.register_protocol(protocol(1))
    for purpose in Purpose:
        total = set(world.ledger.counts(purpose, number if purpose is Purpose.PROTECTED_VALIDATION else None)["total"])
        if purpose is Purpose.AUDIT:
            assert total == set(members)
        elif purpose is Purpose.PROTECTED_VALIDATION:
            assert total == set(holdout.selected)
        else:
            assert total == set(members) - set(holdout.selected)


# ------------------------------------------------------------------ AC12 data limits

@pytest.mark.parametrize("key", ["interpretation", "rule_id", "planet", "score", "weight", "confidence"])
def test_ac12_analytical_content_is_refused(world, key):
    (identifier,) = world.admitted(1)
    record = entry_to_record(world.ledger.read(Purpose.AUDIT)[0])
    record["entry"][key] = 1
    with pytest.raises(LedgerError, match="refused"):
        entry_from_record(record)
    planted = protocol_to_record(protocol(1))
    planted["protocol"][key] = 1
    with pytest.raises(LedgerError, match="refused"):
        protocol_from_record(planted)
    record = entry_to_record(world.ledger.read(Purpose.AUDIT)[0])
    record["entry"]["provenance"][key] = 1
    with pytest.raises(LedgerError, match="refused"):
        entry_from_record(record)


def test_ac12_synthetic_only(world):
    (identifier,) = world.admitted(1)
    entry = world.ledger.read(Purpose.AUDIT)[0]
    with pytest.raises(LedgerError, match="synthetic"):
        dataclasses.replace(entry, data_class="real")


def test_ac12_no_new_identifier_family():
    source = (ROOT / "engine" / "evidence" / "ledger.py").read_text(encoding="utf-8")
    assert not re.search(r'FAMILY\s*=|re\.compile\(r"[A-Z]{2,}-\\d', source)
    naming = (ROOT / "docs" / "NAMING_STANDARD.md").read_text(encoding="utf-8")
    families = re.findall(r"^\| [^|]+\| `([A-Z][A-Z-]*)-", naming, re.MULTILINE)
    # EVD and RUL are registered by ADR-0119 (WP-E4), not by the ledger; the ledger still defines no family.
    assert sorted(families) == sorted(["HLKG-N", "HLKG-D", "EV-CAR", "OC-CAR", "TC-CAR", "ADR", "DP", "ENT", "EVR",
                                       "EVD", "RUL"])


# ------------------------------------------------------------------ AC13 round trip

def test_ac13_every_record_round_trips(world):
    members = world.admitted(3)
    entry = world.ledger.read(Purpose.AUDIT)[0]
    assert entry_from_record(json.loads(json.dumps(entry_to_record(entry)))) == entry
    holdout = world.ledger.holdout(world.ledger.freeze_and_select("three", members, 1))
    assert holdout_from_record(json.loads(json.dumps(holdout_to_record(holdout)))) == holdout
    registered = protocol(1, minimum_n=1)
    assert world.ledger.protocol(world.ledger.register_protocol(registered)) == registered
    log = world.ledger.access_log()
    assert log[0][1] is Purpose.AUDIT and log[0][3] is True and log[0][4] == tuple(sorted(m.value for m in members))


def test_ac13_the_ledger_is_durable_across_reopening(tmp_path):
    path = tmp_path / "evidence.sqlite"
    world = World(path)
    members = world.admitted(4)
    number = world.ledger.freeze_and_select("four", members, 2)
    selected = world.ledger.holdout(number).selected
    world.ledger.close()
    with HistoricalLedger(path) as reopened:
        assert reopened.holdout(number).selected == selected and reopened.reproduces(number)
        assert {entry.event for entry in reopened.read(Purpose.DEVELOPMENT)} == set(members) - set(selected)
