"""EVIDENCE_FOUNDATIONS_V1 CERTIFICATION RUNNER (ADR-0115 s4).

Regenerates certification/EVIDENCE_FOUNDATIONS_V1_certification.json FROM SCRATCH on every run;
the stored JSON is never accepted as proof.

STRUCTURAL certification of the EVIDENCE foundations: the H0 entity model and store (ADR-0114),
and the H1 event model, event store and EVR issuer (ADR-0115). It is NOT astrological-calculation
certification and certifies no production analytical input. Every record it uses is synthetic, and
nothing it runs scores, weights, fits or computes confidence. It needs no oracle.

Gates:
  A  H0 structural integrity: every kind round-trips, competing charts are held, corrections
     append, derived subjects keep valid parent links, and the ENT issuer is durable.
  B  H0 refusals: each one the WP-E1 contract requires, triggered for real.
  C  H1 structural integrity: every time kind, both degenerate cases, every asserter kind and
     every confirmation state round-trip; corrections append; a confirmation answers only its
     revision; the EVR issuer is durable and separate from the ENT issuer.
  D  H1 refusals: each one the WP-E2 contract requires, triggered for real, with no number taken
     and no revision written by a refused operation.
  E  the event-class seed against the career event registry, read here independently.
  F  every comparator above rejects a planted wrong function. A gate that cannot fail is not
     evidence.

Exit 0 = PASS, 3 = FAIL.
"""

import dataclasses
import re
import sqlite3
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

sys.path.insert(0, str(ROOT / "scripts"))
import certification_support as support  # noqa: E402

from engine.evidence.entity import (  # noqa: E402
    ChartCandidate, DataClass, EntityKind, EntityLink, EntityModelError, EventEntity, GeographicEntity,
    Organisation, OriginCertainty, OriginMoment, ParentLink, Person, Question, RecordProvenance, Shape,
    rectification_permitted,
)
from engine.evidence.event_classes import REGISTRY_PATH, SEED, registered  # noqa: E402
from engine.evidence.event_identifiers import EventRecordId  # noqa: E402
from engine.evidence.event_store import (  # noqa: E402
    EventStore, confirmation_from_record, confirmation_to_record, event_from_record, event_to_record,
)
from engine.evidence.events import (  # noqa: E402
    Assertion, AssertionContext, AsserterCertainty, AsserterKind, Confirmation, ConfirmationState, ConfirmerKind,
    EventModelError, EventRecord, EventTime, TimeKind, TimeTolerance, TimeUnit, WindowShape,
    validation_input_permitted,
)
from engine.evidence.identifiers import EntityId, IdentifierError  # noqa: E402
from engine.evidence.store import EntityStore, StoreError, subject_from_record, subject_to_record  # noqa: E402

#: A number no certifier store reaches, for the dangling-reference controls.
LAST_TEST = 99999999
#: The registry's s3 group heading, read here without the code's own parsing.
REGISTRY_GROUP = re.compile(r"^## 3\.\d+ Group: (\w+) \((\d+) events\)\s*$")
PROVENANCE = RecordProvenance(source="synthetic certifier fixture", method="constructed", schema_version="h1-v2")


def fail(message):
    print("EVIDENCE_FOUNDATIONS CERTIFICATION FAIL:", message)
    sys.exit(3)


# ------------------------------------------------------------------ H0

def _synthetic_subjects():
    """One synthetic subject of each of the five kinds. No real person, place or organisation."""

    def chart(label, certainty):
        return ChartCandidate(label=label, origin=OriginMoment(local_datetime="2000-01-01T12:00:00", timezone="UTC",
                                                               timezone_source="fixture", latitude=10.0,
                                                               longitude=20.0, precision="minute"),
                              origin_certainty=certainty, provenance=PROVENANCE)

    common = {"applicable_domains": ("synthetic",), "applicable_systems": ("parashari",), "provenance": PROVENANCE,
              "data_class": DataClass.SYNTHETIC}
    two_charts = (chart("documented", OriginCertainty.DOCUMENTED), chart("reported", OriginCertainty.REPORTED))
    return [
        Person(kind=EntityKind.PERSON, shape=Shape.ORIGIN, charts=two_charts, **common),
        Organisation(kind=EntityKind.ORGANISATION, shape=Shape.ORIGIN, charts=two_charts, **common),
        GeographicEntity(kind=EntityKind.GEOGRAPHIC, shape=Shape.ORIGIN, charts=two_charts, **common),
        EventEntity(kind=EntityKind.EVENT, shape=Shape.ORIGIN, charts=two_charts, **common),
        Question(kind=EntityKind.QUESTION, shape=Shape.QUERY, charts=(chart("asked", OriginCertainty.DOCUMENTED),),
                 **common),
    ]


def _derived(subjects, parent, parent_chart, charts):
    return Person(kind=EntityKind.PERSON, shape=Shape.DERIVED, charts=charts,
                  applicable_domains=subjects[0].applicable_domains,
                  applicable_systems=subjects[0].applicable_systems, provenance=PROVENANCE,
                  data_class=DataClass.SYNTHETIC,
                  parent=ParentLink(parent=parent, parent_chart=parent_chart, derivation="annual chart"))


def gate_a_entity_model_integrity():
    """H0 structural integrity: the model, the append-only store and the ENT issuer (ADR-0114 s3)."""

    subjects = _synthetic_subjects()
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "evidence.sqlite"
        store = EntityStore(path)
        issued = [store.persist(subject) for subject in subjects]
        if [entity.number for entity in issued] != list(range(1, len(subjects) + 1)):
            fail("ENT numbers are not issued 1..n")
        if EntityId.from_number(len(subjects)).number != len(subjects):
            fail("an ENT identifier's number does not round-trip")
        for entity, subject in zip(issued, subjects):
            if store.load(entity) != subject or subject_from_record(subject_to_record(subject)) != subject:
                fail(f"{entity} did not round-trip")
        if store.append_revision(issued[0], subjects[0], "certifier correction") != 2 or \
                [number for number, _subject, _reason in store.history(issued[0])] != [1, 2]:
            fail("a correction did not append a revision")
        derived = _derived(subjects, issued[0], "documented", subjects[0].charts[:1])
        if store.load(store.persist(derived)) != derived:
            fail("a derived subject with a valid parent link did not round-trip")
        if store.append_revision(issued[0], subjects[0], "keeps the referenced chart") != 3:
            fail("a parent correction that keeps the referenced chart was refused")
        link = EntityLink(source=issued[0], relation="LEADS", target=issued[1], provenance=PROVENANCE)
        store.add_link(link)
        if store.links() != [link] or store.entity_ids()[:len(issued)] != issued:
            fail("links or entity listing did not round-trip")
        store.close()
        reopened = EntityStore(path)
        durable = (reopened.issued_count() == len(subjects) + 1
                   and reopened.persist(subjects[1]).number == len(subjects) + 2)
        reopened.close()
        if not durable:
            fail("the ENT issuer is not durable across reopening")
    if rectification_permitted(subjects[0], "documented") or not rectification_permitted(subjects[0], "reported"):
        fail("a documented origin must not be rectified; a reported one may be")
    if rectification_permitted(subjects[4], "asked"):
        fail("a query moment must not be rectified")
    return {"classification": "structural_integrity", "kinds": len(subjects), "round_trips": len(subjects) + 1,
            "competing_charts_held": 2, "revisions_checked": 3, "derived_links_checked": 1, "links_checked": 1,
            "mismatches": 0}


def gate_b_entity_store_refusals():
    """Each H0 refusal the WP-E1 contract requires, triggered for real (ADR-0114 s3)."""

    subjects = _synthetic_subjects()
    refused = {}
    with tempfile.TemporaryDirectory() as folder:
        store = EntityStore(Path(folder) / "evidence.sqlite")
        first = store.persist(subjects[0])
        second = store.persist(subjects[1])
        store.add_link(EntityLink(source=first, relation="LEADS", target=second, provenance=PROVENANCE))
        for label, sql in (("update an entity revision", "UPDATE entity_revisions SET reason = 'x'"),
                           ("delete an entity revision", "DELETE FROM entity_revisions"),
                           ("update a link", "UPDATE entity_links SET payload = '{}'"),
                           ("delete a link", "DELETE FROM entity_links"),
                           ("lower the ENT issuer", "UPDATE issuer SET last_number = 0"),
                           ("delete the ENT issuer", "DELETE FROM issuer")):
            try:
                store._db.execute(sql)
                fail(f"the entity store allowed: {label}")
            except sqlite3.DatabaseError:
                refused[label] = True
        record = subject_to_record(subjects[0])
        for key in ("interpretation", "score", "weight", "confidence"):
            try:
                subject_from_record({"schema": record["schema"], "subject": dict(record["subject"], **{key: 1})})
                fail(f"the entity store accepted analytical content: {key}")
            except StoreError:
                refused[f"entity analytical key {key}"] = True
        try:
            subject_from_record({"schema": record["schema"], "subject": dict(record["subject"], data_class="real")})
            fail("the entity store accepted non-synthetic data")
        except ValueError:
            refused["non-synthetic entity"] = True
        try:
            store.append_revision(first, subjects[4], "a kind change")
            fail("a correction changed an entity's kind")
        except StoreError:
            refused["kind change"] = True
        family = "ENT" + "-"
        for label, bad in (("seven digits", family + "0" * 6 + "1"), ("lower-case family", family.lower() + "0" * 7 + "1"),
                           ("number zero", family + "0" * 8)):
            try:
                EntityId(bad)
                fail(f"accepted an invalid ENT identifier: {label}")
            except IdentifierError:
                refused[f"ENT identifier: {label}"] = True
        before = store.issued_count()
        try:
            store.persist("not a subject")
            fail("persisted a non-subject")
        except StoreError:
            refused["non-subject"] = True
        try:
            _derived(subjects, first, "documented", ())
            fail("a shape B subject was built with no chart")
        except EntityModelError:
            refused["shape B with no chart"] = True
        charts = subjects[0].charts[:1]
        for label, subject in (("dangling parent entity", _derived(subjects, EntityId.from_number(LAST_TEST),
                                                                   "documented", charts)),
                               ("dangling parent chart", _derived(subjects, first, "no-such-chart", charts))):
            try:
                store.persist(subject)
                fail(f"the entity store accepted a {label}")
            except StoreError:
                refused[label] = True
        if store.issued_count() != before:
            fail("a failed entity persistence consumed an ENT number")
        child = store.persist(_derived(subjects, first, "documented", charts))
        for label, correction, target in (
                ("self-derivation", _derived(subjects, child, "documented", charts), child),
                ("dangling parent in a correction", _derived(subjects, first, "no-such-chart", charts), child),
                ("parent correction removing a referenced chart",
                 dataclasses.replace(subjects[0], charts=subjects[0].charts[1:]), first)):
            revisions = len(store.history(target))
            try:
                store.append_revision(target, correction, label)
                fail(f"the entity store accepted a {label}")
            except StoreError:
                refused[label] = True
            if len(store.history(target)) != revisions:
                fail(f"a refused {label} still wrote a revision")
        store.close()
    return {"classification": "negative_control", "refusals_verified": len(refused), "refused": sorted(refused)}


# ------------------------------------------------------------------ H1

def _times():
    """Every time kind, and both degenerate cases."""

    return {
        "instant": EventTime(TimeKind.INSTANT, TimeUnit.MINUTE, "UTC", "fixture", at="2010-05-12T14:30",
                             birth_time_sensitive=True),
        "closed interval": EventTime(TimeKind.CLOSED_INTERVAL, TimeUnit.MONTH, "UTC", "fixture", start="2010-03",
                                     end="2010-06"),
        "zero-length interval": EventTime(TimeKind.CLOSED_INTERVAL, TimeUnit.DAY, "UTC", "fixture",
                                          start="2010-05-12", end="2010-05-12"),
        "open interval": EventTime(TimeKind.OPEN_INTERVAL, TimeUnit.YEAR, "UTC", "fixture", start="2010"),
        "unbounded": EventTime(TimeKind.OPEN_INTERVAL, None, None, None),
        "fuzzy window": EventTime(TimeKind.FUZZY_WINDOW, TimeUnit.MONTH, "UTC", "fixture", at="2010-05",
                                  tolerance=TimeTolerance(2, TimeUnit.MONTH), window_shape=WindowShape.UNIFORM),
    }


def _assertion(kind, at="2026-01-01T09:00:00Z"):
    certainty = AsserterCertainty.UNSTATED if kind is AsserterKind.SYSTEM_HYPOTHESIS else AsserterCertainty.PROBABLE
    return Assertion(asserter_kind=kind, asserter_reference="synthetic asserter", asserted_at=at, method="constructed",
                     asserter_certainty=certainty)


def _event(entity, time, kind=AsserterKind.USER_RECOLLECTION, context=None, event_class=SEED[4].class_id):
    return EventRecord(entity=entity, event_class=event_class, time=time, assertion=_assertion(kind),
                       provenance=PROVENANCE, data_class=DataClass.SYNTHETIC, assertion_context=context)


def _answer(state, statement="stated reason"):
    return Confirmation(state=state, confirmer_kind=ConfirmerKind.HUMAN_REVIEWER, confirmer_reference="synthetic reviewer",
                        confirmed_at="2026-02-01T09:00:00Z", statement=statement, provenance=PROVENANCE)


def round_trip_mismatches(encode, decode, records) -> int:
    """How many records do not survive encode then decode unchanged."""

    return sum(1 for record in records if decode(encode(record)) != record)


def gate_c_event_model_integrity():
    """H1 structural integrity: the event model, the append-only event store and the EVR issuer (ADR-0115 s5)."""

    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "evidence.sqlite"
        entities = EntityStore(path)
        owner = entities.persist(_synthetic_subjects()[0])
        store = EventStore(path)
        records = [_event(owner, time) for time in _times().values()]
        records += [_event(owner, _times()["closed interval"], kind) for kind in AsserterKind
                    if kind is not AsserterKind.USER_RECOLLECTION]
        records.append(_event(owner, _times()["instant"], context=AssertionContext(1, "reported", PROVENANCE),
                              event_class=SEED[20].class_id))
        if round_trip_mismatches(event_to_record, event_from_record, records):
            fail("an event record did not round-trip")
        issued = [store.persist(record) for record in records]
        if [identifier.number for identifier in issued] != list(range(1, len(records) + 1)):
            fail("EVR numbers are not issued 1..n")
        if EventRecordId.from_number(len(records)).number != len(records) or store.event_ids() != issued:
            fail("EVR identifiers or the event listing did not round-trip")
        if [store.load(identifier) for identifier in issued] != records:
            fail("a stored event did not reload equal")
        if entities.issued_count() != 1:
            fail("issuing EVR numbers moved the ENT issuer")
        answers = [_answer(state, "" if state is ConfirmationState.CONFIRMED else "stated reason")
                   for state in ConfirmationState]
        if round_trip_mismatches(confirmation_to_record, confirmation_from_record, answers):
            fail("a confirmation record did not round-trip")
        for answer in answers:
            store.confirm(issued[0], 1, answer)
        if store.confirmations(issued[0]) != [(1, answer) for answer in answers] or \
                store.confirmation_state(issued[0]) is not answers[-1].state:
            fail("confirmations did not round-trip, or the latest answer is not the current state")
        corrected = dataclasses.replace(records[1], time=EventTime(TimeKind.CLOSED_INTERVAL, TimeUnit.MONTH, "UTC",
                                                                   "fixture", start="2010-04", end="2010-06"))
        if store.append_revision(issued[1], corrected, "asserter narrowed the interval") != 2 or \
                [number for number, _event, _reason in store.history(issued[1])] != [1, 2] or \
                store.history(issued[1])[0][1] != records[1]:
            fail("a correction did not append a revision beside the one it supersedes")
        store.confirm(issued[1], 2, _answer(ConfirmationState.CONFIRMED, ""))
        hypothesis = issued[len(_times()) + 2]
        admissible_before = store.validation_input_permitted(hypothesis)
        store.confirm(hypothesis, 1, _answer(ConfirmationState.CONFIRMED, ""))
        if admissible_before or not store.validation_input_permitted(hypothesis):
            fail("a system hypothesis must be inadmissible until a human confirms it, then admissible")
        store.close()
        entities.close()
        reopened = EventStore(path)
        durable = (reopened.issued_count() == len(records)
                   and reopened.persist(_event(owner, _times()["open interval"], event_class=SEED[0].class_id)).number
                   == len(records) + 1
                   and reopened.confirmation_state(issued[1]) is ConfirmationState.CONFIRMED)
        reopened.close()
        if not durable:
            fail("the EVR issuer or the confirmations are not durable across reopening")
    if not registered(SEED[0].class_id) or registered("EV-CAR-" + "999"):
        fail("the class registry admits the wrong identifiers")
    return {"classification": "structural_integrity", "time_kinds": len(set(t.kind for t in _times().values())),
            "time_cases": len(_times()), "asserter_kinds": len(AsserterKind),
            "confirmation_states": len(ConfirmationState), "round_trips": len(records) + len(answers),
            "revisions_checked": 2, "assertion_contexts_checked": 1, "mismatches": 0}


def gate_d_event_store_refusals():
    """Each H1 refusal the WP-E2 contract requires, triggered for real (ADR-0115 s5 AC2 to AC11)."""

    refused = {}

    def refuses(label, action, errors=(StoreError,), reason=""):
        """`action` must raise one of `errors`, and, where several refusals are possible, for `reason`."""

        try:
            action()
        except errors as exc:
            if reason not in str(exc):
                fail(f"{label} was refused for another reason: {exc}")
            refused[label] = True
            return
        fail(f"not refused: {label}")

    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "evidence.sqlite"
        entities = EntityStore(path)
        owner = entities.persist(_synthetic_subjects()[0])
        other = entities.persist(_synthetic_subjects()[1])
        store = EventStore(path)
        times = _times()
        anchored = _event(owner, times["instant"], context=AssertionContext(1, "reported", PROVENANCE))
        first = store.persist(anchored)
        store.confirm(first, 1, _answer(ConfirmationState.CONFIRMED, ""))
        for label, sql in (("update an event revision", "UPDATE event_revisions SET reason = 'x'"),
                           ("delete an event revision", "DELETE FROM event_revisions"),
                           ("update a confirmation", "UPDATE event_confirmations SET payload = '{}'"),
                           ("delete a confirmation", "DELETE FROM event_confirmations"),
                           ("lower the EVR issuer", "UPDATE event_issuer SET last_number = 0"),
                           ("delete the EVR issuer", "DELETE FROM event_issuer")):
            refuses(label, lambda sql=sql: store._db.execute(sql), (sqlite3.DatabaseError,))
        record = event_to_record(anchored)
        for level in ("event", "time", "assertion", "assertion_context", "provenance"):
            for key in ("interpretation", "rule_id", "planet", "score", "confidence"):
                planted = event_to_record(anchored)
                target = planted["event"] if level == "event" else planted["event"][level]
                target[key] = 1
                refuses(f"analytical key {key} on the {level}", lambda planted=planted: event_from_record(planted))
        planted = confirmation_to_record(_answer(ConfirmationState.CONFIRMED, ""))
        planted["confirmation"]["score"] = 1
        refuses("analytical key score on a confirmation", lambda: confirmation_from_record(planted))
        planted = confirmation_to_record(_answer(ConfirmationState.CONFIRMED, ""))
        planted["confirmation"]["confirmer_kind"] = "system"
        refuses("a system confirmer", lambda: confirmation_from_record(planted), reason="only a human confirms")
        refuses("a system confirmer in the model",
                lambda: dataclasses.replace(_answer(ConfirmationState.CONFIRMED, ""), confirmer_kind="system"),
                (EventModelError,))
        refuses("non-synthetic event", lambda: event_from_record(
            {"schema": record["schema"], "event": dict(record["event"], data_class="real")}), (ValueError,))
        refuses("unregistered event class", lambda: dataclasses.replace(anchored, event_class="EV-CAR-" + "999"),
                (EventModelError,))
        refuses("system hypothesis with a declared certainty", lambda: dataclasses.replace(
            _assertion(AsserterKind.SYSTEM_HYPOTHESIS), asserter_certainty=AsserterCertainty.CERTAIN),
            (EventModelError,))
        for label, build in (
                ("closed interval ending before it starts", lambda: EventTime(
                    TimeKind.CLOSED_INTERVAL, TimeUnit.YEAR, "UTC", "fixture", start="2011", end="2010")),
                ("value more precise than its stated precision", lambda: EventTime(
                    TimeKind.INSTANT, TimeUnit.YEAR, "UTC", "fixture", at="2010-05-12")),
                ("time value without a timezone", lambda: EventTime(
                    TimeKind.INSTANT, TimeUnit.YEAR, None, "fixture", at="2010")),
                ("fuzzy window without a tolerance", lambda: EventTime(
                    TimeKind.FUZZY_WINDOW, TimeUnit.YEAR, "UTC", "fixture", at="2010")),
                ("birth-time sensitivity without a known hour", lambda: EventTime(
                    TimeKind.INSTANT, TimeUnit.DAY, "UTC", "fixture", at="2010-05-12", birth_time_sensitive=True))):
            refuses(label, build, (EventModelError,))
        event_family = "EVR" + "-"
        for label, bad in (("seven digits", event_family + "0" * 6 + "1"),
                           ("lower-case family", event_family.lower() + "0" * 7 + "1"),
                           ("number zero", event_family + "0" * 8)):
            refuses(f"EVR identifier: {label}", lambda bad=bad: EventRecordId(bad), (IdentifierError,))
        before = store.issued_count()
        for label, bad in (
                ("non-event", "not an event"),
                ("dangling entity", _event(EntityId.from_number(LAST_TEST), times["open interval"])),
                ("dangling context revision", _event(owner, times["open interval"],
                                                     context=AssertionContext(LAST_TEST, "reported", PROVENANCE))),
                ("dangling context chart", _event(owner, times["open interval"],
                                                  context=AssertionContext(1, "no-such-chart", PROVENANCE))),
                ("exact duplicate", anchored),
                ("duplicate under another chart", dataclasses.replace(
                    anchored, assertion_context=AssertionContext(1, "documented", PROVENANCE))),
                ("duplicate with no chart", dataclasses.replace(anchored, assertion_context=None))):
            reason = {"non-event": "only an EventRecord", "dangling entity": "is not in this store",
                      "dangling context revision": "has no revision",
                      "dangling context chart": "is not a chart of"}[label] if "duplicate" not in label else "duplicated"
            refuses(label, lambda bad=bad: store.persist(bad), reason=reason)
        if store.issued_count() != before:
            fail("a refused event persistence consumed an EVR number")
        hypothesis = store.persist(_event(owner, times["fuzzy window"], AsserterKind.SYSTEM_HYPOTHESIS))
        twin = store.persist(_event(owner, times["closed interval"], AsserterKind.SYSTEM_HYPOTHESIS))
        for label, target, correction, reason in (
                ("re-anchoring to another entity", first, dataclasses.replace(anchored, entity=other), "another entity"),
                ("re-anchoring to another chart", first, dataclasses.replace(
                    anchored, assertion_context=AssertionContext(1, "documented", PROVENANCE)), "assertion context"),
                ("changing the asserter", first, dataclasses.replace(
                    anchored, assertion=_assertion(AsserterKind.PUBLIC_RECORD)), "who asserted"),
                ("laundering a system hypothesis", hypothesis, _event(owner, times["fuzzy window"]), "who asserted"),
                ("a correction duplicating another event", twin,
                 _event(owner, times["fuzzy window"], AsserterKind.SYSTEM_HYPOTHESIS), "duplicated")):
            revisions = len(store.history(target))
            refuses(label, lambda target=target, correction=correction: store.append_revision(target, correction, label),
                    reason=reason)
            if len(store.history(target)) != revisions:
                fail(f"a refused {label} still wrote a revision")
        answers = len(store.confirmations(first))
        store.append_revision(first, dataclasses.replace(anchored, time=times["closed interval"]), "certifier correction")
        refuses("confirming a superseded revision",
                lambda: store.confirm(first, 1, _answer(ConfirmationState.CONFIRMED, "")), reason="current revision")
        refuses("confirming a missing event", lambda: store.confirm(EventRecordId.from_number(LAST_TEST), 1,
                                                                    _answer(ConfirmationState.CONFIRMED, "")),
                reason="no such event")
        if len(store.confirmations(first)) != answers or store.confirmation_state(first) is not \
                ConfirmationState.UNCONFIRMED:
            fail("a correction must leave the new revision unconfirmed, and a refused answer writes nothing")
        if store.validation_input_permitted(hypothesis):
            fail("an unconfirmed system hypothesis was admitted as validation input")
        store.confirm(hypothesis, 1, _answer(ConfirmationState.REJECTED))
        if store.validation_input_permitted(hypothesis):
            fail("a rejected event was admitted as validation input")
        refused["unconfirmed or rejected system hypothesis as validation input"] = True
        store.close()
        entities.close()
    return {"classification": "negative_control", "refusals_verified": len(refused), "refused": sorted(refused)}


# ------------------------------------------------------------------ the registry

def registry_rows(text: str) -> tuple:
    """The registry's s3 rows, (identifier, name, group, origin), and each group's stated count."""

    section = text.split("\n## 4.")[0]
    rows, group, stated = [], None, {}
    for line in section.splitlines():
        heading = REGISTRY_GROUP.match(line)
        if heading:
            group = heading.group(1).lower()
            stated[group] = int(heading.group(2))
        elif line.startswith("| EV-CAR-"):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            rows.append((cells[0], cells[1].strip("`"), group, cells[5]))
    return rows, stated


def seed_mismatches(seed, rows) -> int:
    """Positions where the seed and the registry disagree, plus any difference in length."""

    code = [(entry.class_id, entry.name, entry.group, entry.origin.value) for entry in seed]
    return sum(1 for left, right in zip(code, rows) if left != right) + abs(len(code) - len(rows))


def gate_e_event_class_registry():
    """The seed is exactly the registry's s3 rows (ADR-0113 s2 C1; ADR-0115 s3)."""

    rows, stated = registry_rows((ROOT / REGISTRY_PATH).read_text(encoding="utf-8"))
    counted = {}
    for _identifier, _name, group, _origin in rows:
        counted[group] = counted.setdefault(group, 0) + 1
    if counted != stated:
        fail(f"the registry's group headings {stated} disagree with its rows {counted}")
    mismatches = seed_mismatches(SEED, rows)
    if mismatches:
        fail(f"the event-class seed differs from the registry at {mismatches} position(s)")
    origins = [row[3] for row in rows]
    return {"classification": "registry_conformance", "registry": REGISTRY_PATH, "classes": len(rows),
            "groups": len(stated), "origin_model": origins.count("MODEL"),
            "origin_proposed_addition": origins.count("PROPOSED-ADDITION"), "mismatches": mismatches}


# ------------------------------------------------------------------ negative controls

def gate_f_negative_controls():
    """Every comparator above rejects a planted wrong function, so none of them is vacuous."""

    controls = {}
    owner = EntityId.from_number(1)
    records = [_event(owner, time) for time in _times().values()]

    def drop_tolerance(record):
        """Lossy but valid: a fuzzy window comes back as a bare instant."""

        data = event_to_record(record)
        time = data["event"]["time"]
        if time["kind"] == TimeKind.FUZZY_WINDOW.value:
            time["kind"], time["tolerance"] = TimeKind.INSTANT.value, None
            time["window_shape"] = WindowShape.UNSTATED.value
        return data

    def coarsen_precision(record):
        data = event_to_record(record)
        time = data["event"]["time"]
        if time["kind"] == TimeKind.CLOSED_INTERVAL.value and time["precision"] == TimeUnit.MONTH.value:
            time["precision"], time["start"], time["end"] = TimeUnit.YEAR.value, "2010", "2010"
        return data

    for label, encode in (("serializer that drops a tolerance", drop_tolerance),
                          ("serializer that coarsens a precision", coarsen_precision)):
        if round_trip_mismatches(encode, event_from_record, records) == 0:
            fail(f"the round-trip comparator accepted a {label}")
        controls[label] = True
    rows, _stated = registry_rows((ROOT / REGISTRY_PATH).read_text(encoding="utf-8"))
    for label, planted in (("seed missing a class", SEED[1:]), ("seed with an extra class", SEED + (SEED[0],)),
                           ("seed with a renamed class", (dataclasses.replace(SEED[0], name="first_job"),) + SEED[1:]),
                           ("seed in another order", (SEED[1], SEED[0]) + SEED[2:])):
        if seed_mismatches(planted, rows) == 0:
            fail(f"the registry comparator accepted a {label}")
        controls[label] = True
    hypothesis = _event(owner, _times()["fuzzy window"], AsserterKind.SYSTEM_HYPOTHESIS)
    for label, permissive in (("admit everything", lambda record, state: True),
                              ("ignore the asserter", lambda record, state: state is not ConfirmationState.REJECTED)):
        if permissive(hypothesis, ConfirmationState.UNCONFIRMED) == validation_input_permitted(
                hypothesis, ConfirmationState.UNCONFIRMED):
            fail(f"the admissibility check cannot tell the real rule from one that would {label}")
        controls[f"admissibility rule that would {label}"] = True
    return {"classification": "negative_control", "controls_rejected": len(controls), "controls": sorted(controls)}


def main():
    tee = support.start_transcript()
    preconditions = support.preflight()
    gates = {
        "A_entity_model_integrity": gate_a_entity_model_integrity(),
        "B_entity_store_refusals": gate_b_entity_store_refusals(),
        "C_event_model_integrity": gate_c_event_model_integrity(),
        "D_event_store_refusals": gate_d_event_store_refusals(),
        "E_event_class_registry": gate_e_event_class_registry(),
        "F_negative_controls": gate_f_negative_controls(),
    }
    report = {
        "schema": "evidence_foundations_v1_certification",
        "adr": "ADR-0115 s4",
        "date": str(date.today()),
        "scope": ("Structural certification of the EVIDENCE foundations: the H0 entity model, append-only entity store "
                  "and ENT issuer (ADR-0114 WP-E1), and the H1 event model, append-only event store, separate "
                  "confirmation records, EVR issuer and seeded event-class vocabulary (ADR-0115 WP-E2)."),
        "reference": {
            "structure": "the model contracts of ADR-0114 s3 and ADR-0115 s5, exercised on synthetic records",
            "event_classes": f"{REGISTRY_PATH} s3, read by this runner independently of the code",
        },
        "gates": gates,
        "explicit_non_claims": [
            "structural certification only: this is not astrological-calculation certification",
            "declares no production analytical input, and is served by no API",
            "makes no analytical claim: nothing here scores, weights, fits or computes confidence",
            "every record used is synthetic; no real personal data is certified or permitted",
            "the event-class seed is certified equal to the registry, not the registry's classes correct; the "
            "registry stays DRAFT and its origin column is carried, not ratified",
            "admissibility as validation input is a gate on system hypotheses and rejections only; H2 and H4 may add "
            "requirements",
            "SUPPORT_PATHS_V1 gates H and I still certify the H0 foundations; this artifact does not retire them",
        ],
        "environment": {"python": sys.version.split()[0]},
        "preconditions": preconditions,
        "result": "PASS",
    }
    out = support.emit(report, "EVIDENCE_FOUNDATIONS_V1_certification.json", "evidence_foundations", tee)
    print("=" * 60)
    print("EVIDENCE_FOUNDATIONS_V1 CERTIFICATION")
    print("=" * 60)
    for name, block in report["gates"].items():
        print(f"{name}: {block.get('mismatches', block.get('refusals_verified', block.get('controls_rejected')))}")
    print("archived:", out.relative_to(ROOT).as_posix())
    print("RESULT  : PASS")


if __name__ == "__main__":
    main()
