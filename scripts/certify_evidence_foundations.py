"""EVIDENCE_FOUNDATIONS_V1 CERTIFICATION RUNNER (ADR-0115 s4; ADR-0116 s4).

Regenerates certification/EVIDENCE_FOUNDATIONS_V1_certification.json FROM SCRATCH on every run;
the stored JSON is never accepted as proof.

STRUCTURAL certification of the EVIDENCE foundations: the H0 entity model and store (ADR-0114),
the H1 event model, event store and EVR issuer (ADR-0115), and the H2 historical ledger and its
protected holdouts (ADR-0116). It is NOT astrological-calculation certification and certifies no production analytical input. Every record it uses is synthetic, and
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
  G  H2 structural integrity: admission with outcomes, elicitation, superseding corrections,
     decomposable counts, a reproducible holdout, a protocol, and a clean, durable access log.
  H  H2 refusals: each one the WP-E3 contract requires, triggered for real; refused reads are logged.
  I  the holdout's reproduction check and the leakage check each reject planted wrong inputs.

Exit 0 = PASS, 3 = FAIL.
"""

import dataclasses
import json
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
from engine.evidence.ledger import (  # noqa: E402
    EXCLUDED_FROM_PROTECTED, PROCEDURE, Elicitation, HistoricalLedger, LedgerError, Outcome, Protocol, Purpose,
    content_hash, entry_from_record, entry_to_record, holdout_from_record, holdout_to_record, leakage_findings,
    ordered_selection, protocol_from_record, protocol_to_record, selection_hash,
)

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


# ------------------------------------------------------------------ H2

def _ledger_world(path):
    """A synthetic entity, and an event store, in one database."""

    entities = EntityStore(path)
    owner = entities.persist(_synthetic_subjects()[0])
    events = EventStore(path)
    return entities, events, owner


def _answered(events, owner, day, state=ConfirmationState.CONFIRMED, kind=AsserterKind.USER_RECOLLECTION,
              event_class=SEED[0].class_id):
    identifier = events.persist(_event(owner, EventTime(TimeKind.INSTANT, TimeUnit.DAY, "UTC", "fixture",
                                                        at=f"2010-01-{day:02d}"), kind, event_class=event_class))
    if state is not None:
        events.confirm(identifier, 1, _answer(state, "" if state is ConfirmationState.CONFIRMED else "stated reason"))
    return identifier


def _protocol(holdout, minimum_n):
    return Protocol(holdout=holdout, event_classes=(SEED[0].class_id,), hypotheses=("synthetic hypothesis",),
                    rule_references=(), development_set="entries outside the holdout", hypothesis_count=1,
                    event_count=4, multiple_comparison_method="Bonferroni", effect_size_measures=("risk difference",),
                    negative_controls=("events shifted to random dates",), replication="not feasible: synthetic",
                    minimum_n=minimum_n, provenance=PROVENANCE, data_class=DataClass.SYNTHETIC)


def gate_g_ledger_integrity():
    """H2 structural integrity: admission, elicitation, correction, decomposable counts and the holdout (ADR-0116 s5)."""

    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "evidence.sqlite"
        entities, events, owner = _ledger_world(path)
        ledger = HistoricalLedger(path)
        confirmed = [_answered(events, owner, day) for day in range(1, 9)]
        partial = _answered(events, owner, 9, ConfirmationState.PARTIALLY_CONFIRMED, event_class=SEED[4].class_id)
        rejected = _answered(events, owner, 10, ConfirmationState.REJECTED, AsserterKind.SYSTEM_HYPOTHESIS)
        elicitations = list(Elicitation)
        for index, identifier in enumerate(confirmed + [partial, rejected]):
            ledger.admit(identifier, elicitations[index % len(elicitations)], PROVENANCE)
        audit = ledger.read(Purpose.AUDIT)
        if [entry.outcome for entry in audit].count(Outcome.REJECTED) != 1 or len(audit) != 10:
            fail("the ledger did not admit every answered event with its outcome, rejections included")
        if any(entry_from_record(entry_to_record(entry)) != entry for entry in audit):
            fail("a ledger entry did not round-trip")
        counts = ledger.counts(Purpose.AUDIT)
        for axis in ("event_class", "elicitation", "outcome"):
            parts = [set(members) for members in counts[axis].values()]
            if set().union(*parts) != set(counts["total"]) or sum(len(part) for part in parts) != len(counts["total"]):
                fail(f"the {axis} partition does not decompose the total")
        events.append_revision(partial, dataclasses.replace(events.load(partial), time=EventTime(
            TimeKind.INSTANT, TimeUnit.DAY, "UTC", "fixture", at="2011-02-01")), "recalled 2011")
        events.confirm(partial, 2, _answer(ConfirmationState.CONFIRMED, ""))
        second = ledger.correct(partial, Elicitation.VOLUNTEERED, PROVENANCE, "event corrected and re-answered")
        history = ledger.history(Purpose.AUDIT, partial)
        if len(history) != 2 or history[1][2] != history[0][0] or history[1][0] != second or \
                history[0][1].event_revision != 1 or history[1][1].event_revision != 2:
            fail("a correction did not append a superseding entry beside the one it supersedes")
        number = ledger.freeze_and_select("the eight confirmed entries", confirmed, 3)
        holdout = ledger.holdout(number)
        if not ledger.reproduces(number) or holdout_from_record(holdout_to_record(holdout)) != holdout:
            fail("the holdout does not reproduce from its own record")
        if ordered_selection(holdout.seed, holdout.members, holdout.size) != holdout.selected or \
                content_hash(holdout.members) != holdout.content_hash or ledger.protected() != set(holdout.selected):
            fail("the recorded selection, hash or protection disagrees with the procedure")
        development = {entry.event for entry in ledger.read(Purpose.DEVELOPMENT)}
        if development & set(holdout.selected) or len(development) != 10 - holdout.size:
            fail("a development read saw a protected entry")
        registered = _protocol(number, 3)
        protocol_number = ledger.register_protocol(registered)
        if ledger.protocol(protocol_number) != registered or \
                protocol_from_record(protocol_to_record(registered)) != registered:
            fail("a protocol did not round-trip")
        served = {entry.event for entry in ledger.read(Purpose.PROTECTED_VALIDATION, protocol_number)}
        if served != set(holdout.selected):
            fail("protected validation did not serve exactly the holdout")
        log = ledger.access_log()
        if [row[3] for row in log] != [True] * 5 or log[2][5] != "granted: history" or leakage_findings(path) != []:
            fail("a clean run was not logged as granted reads with no leakage")
        ledger.close()
        events.close()
        entities.close()
        reopened = HistoricalLedger(path)
        durable = reopened.reproduces(number) and reopened.holdout(number) == holdout and \
            len(reopened.access_log()) == len(log)
        reopened.close()
        if not durable:
            fail("the ledger, holdout or access log is not durable across reopening")
    return {"classification": "structural_integrity", "entries_admitted": 10, "outcomes": len(Outcome),
            "elicitation_kinds": len(Elicitation), "count_axes": 3, "corrections_checked": 1, "holdout_members": 8,
            "holdout_selected": 3, "protocols_checked": 1, "access_rows_checked": len(log), "mismatches": 0}


def gate_h_ledger_refusals():
    """Each H2 refusal the WP-E3 contract requires, triggered for real (ADR-0116 s5 AC1 to AC12)."""

    refused = {}

    def refuses(label, action, errors=(LedgerError,), reason=""):
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
        entities, events, owner = _ledger_world(path)
        ledger = HistoricalLedger(path)
        members = [_answered(events, owner, day) for day in range(1, 7)]
        extra = [_answered(events, owner, day) for day in range(7, 9)]
        rejected = _answered(events, owner, 9, ConfirmationState.REJECTED)
        unanswered = _answered(events, owner, 10, None)
        unconfirmed = _answered(events, owner, 11, ConfirmationState.UNCONFIRMED)
        for identifier in members + extra + [rejected]:
            ledger.admit(identifier, Elicitation.VOLUNTEERED, PROVENANCE)
        refuses("admitting an unanswered event", lambda: ledger.admit(unanswered, Elicitation.VOLUNTEERED, PROVENANCE),
                reason="no human answer")
        refuses("admitting an event answered unconfirmed",
                lambda: ledger.admit(unconfirmed, Elicitation.VOLUNTEERED, PROVENANCE), reason="no human answer")
        refuses("admitting an event twice", lambda: ledger.admit(members[0], Elicitation.VOLUNTEERED, PROVENANCE),
                reason="already")
        refuses("admitting without an elicitation", lambda: ledger.admit(unanswered, None, PROVENANCE),
                reason="elicited")
        refuses("a correction that changes nothing",
                lambda: ledger.correct(members[0], Elicitation.VOLUNTEERED, PROVENANCE, "no change"),
                reason="change something")
        refuses("a correction with no reason",
                lambda: ledger.correct(members[0], Elicitation.PROMPTED_FOR_NULL_PERIOD, PROVENANCE, " "),
                reason="reason")
        entry = ledger.read(Purpose.AUDIT, event_id=members[0])[0]
        for key in ("interpretation", "rule_id", "planet", "score", "confidence"):
            planted = entry_to_record(entry)
            planted["entry"][key] = 1
            refuses(f"analytical key {key} on a ledger entry", lambda planted=planted: entry_from_record(planted),
                    reason="refused")
            planted = protocol_to_record(_protocol(1, 1))
            planted["protocol"][key] = 1
            refuses(f"analytical key {key} on a protocol", lambda planted=planted: protocol_from_record(planted),
                    reason="refused")
        refuses("a non-synthetic ledger entry", lambda: dataclasses.replace(entry, data_class="real"),
                reason="synthetic")
        refuses("a protocol citing rules before RUL exists", lambda: dataclasses.replace(
            _protocol(1, 1), rule_references=("a rule",)), reason="RUL")
        refuses("a protocol whose hypothesis count disagrees", lambda: dataclasses.replace(
            _protocol(1, 1), hypothesis_count=2), reason="hypothesis_count")
        refuses("a protocol with no minimum N", lambda: dataclasses.replace(_protocol(1, 1), minimum_n=0),
                reason="minimum_n")
        refuses("a protocol naming no locked holdout", lambda: ledger.register_protocol(_protocol(1, 1)),
                reason="locked holdout")
        refuses("a rejected entry in an eligible set",
                lambda: ledger.freeze_and_select("bad", members[:2] + [rejected], 1), reason="not a confirmed")
        refuses("an event outside the ledger in an eligible set",
                lambda: ledger.freeze_and_select("bad", members[:2] + [unanswered], 1), reason="not a confirmed")
        number = ledger.freeze_and_select("six", members, 3)
        holdout = ledger.holdout(number)
        for label, again in (("refreezing the same set", members), ("refreezing it reordered", members[::-1]),
                             ("refreezing a subset", members[:2]), ("refreezing a superset", members + extra),
                             ("refreezing an overlapping set", members[5:] + extra)):
            refuses(label, lambda again=again: ledger.freeze_and_select("again", again, 1), reason="frozen set")
        if ledger.holdout(number) != holdout or ledger.protected() != set(holdout.selected):
            fail("a refused reselection changed the holdout or its protection")
        refuses("a second selection row for a frozen set", lambda: ledger._db.execute(
            "INSERT INTO holdouts (set_number, after_access, payload) VALUES (1, 0, '{}')"), (sqlite3.IntegrityError,))
        short = ledger.register_protocol(_protocol(number, holdout.size + 1))
        for table in ("ledger_entries", "eligible_sets", "eligible_members", "holdouts", "protected_events",
                      "protocols", "access_log"):
            if not ledger._db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]:
                fail(f"{table} is empty, so a refused update or delete of it would prove nothing")
        for table, column in (("ledger_entries", "reason"), ("eligible_sets", "payload"),
                              ("eligible_members", "set_number"), ("holdouts", "payload"),
                              ("protected_events", "holdout_number"), ("protocols", "payload"),
                              ("access_log", "note")):
            for verb, sql in (("update", f"UPDATE {table} SET {column} = {column}"), ("delete", f"DELETE FROM {table}")):
                refuses(f"{verb} {table}", lambda sql=sql: ledger._db.execute(sql), (sqlite3.DatabaseError,),
                        reason="append-only")
        logged = len(ledger.access_log())
        for purpose in sorted(EXCLUDED_FROM_PROTECTED, key=lambda item: item.value):
            refuses(f"a {purpose.value} read of a protected entry",
                    lambda purpose=purpose: ledger.read(purpose, event_id=holdout.selected[0]), reason="not available")
        refuses("a read with no declared purpose", lambda: ledger.read(None), reason="Purpose")
        refuses("protected validation with no protocol", lambda: ledger.read(Purpose.PROTECTED_VALIDATION),
                reason="registered protocol")
        refuses("protected validation under an unregistered protocol",
                lambda: ledger.read(Purpose.PROTECTED_VALIDATION, LAST_TEST), reason="no protocol")
        refuses("protected validation below the protocol's minimum N",
                lambda: ledger.read(Purpose.PROTECTED_VALIDATION, short), reason="minimum N")
        refuses("an audit read naming a protocol", lambda: ledger.read(Purpose.AUDIT, short), reason="names no protocol")
        # A history read is a ledger read (CEO HOLD on PR #50, defect 1).
        for purpose in sorted(EXCLUDED_FROM_PROTECTED, key=lambda item: item.value):
            refuses(f"a {purpose.value} history read of a protected entry",
                    lambda purpose=purpose: ledger.history(purpose, holdout.selected[0]), reason="not available")
        refuses("a history read with no declared purpose", lambda: ledger.history(None, members[0]), reason="Purpose")
        refuses("a history read naming no event", lambda: ledger.history(Purpose.AUDIT, None), reason="names one event")
        # A malformed request is a logged refusal, never an escape (CEO HOLD on PR #50, defect 2).
        for label, call in (("an event named by text", lambda: ledger.read(Purpose.AUDIT, None, members[0].value)),
                            ("a protocol named by text", lambda: ledger.read(Purpose.PROTECTED_VALIDATION, "1")),
                            ("a protocol named by a bool", lambda: ledger.read(Purpose.PROTECTED_VALIDATION, True)),
                            ("a protocol number beyond 64 bits",
                             lambda: ledger.read(Purpose.PROTECTED_VALIDATION, 2 ** 70))):
            refuses(f"a read with {label}", call, reason="refused")

        def broken(*_args):
            raise RuntimeError("planted failure")

        ledger._visible = broken
        refuses("an unexpected failure while deciding a read", lambda: ledger.read(Purpose.AUDIT),
                reason="malformed request refused")
        del ledger._visible
        log = ledger.access_log()
        if len(log) != logged + 20 or any(row[3] for row in log[logged:]) or \
                log[logged + 4][1] != "undeclared" or log[logged + 13][1] != "undeclared" or \
                any(row[2] is not None for row in log[logged + 15:logged + 19]):
            fail("a refused ledger read was not logged as refused, with its declared purpose and protocol")
        if leakage_findings(path) != []:
            fail("refused reads were reported as leakage")
        # Last, because it plants a raw row: one entry can be superseded only once, so history cannot fork.
        first_entry = ledger.history(Purpose.AUDIT, members[0])[0][0]
        ledger._db.execute("INSERT INTO ledger_entries (event_id, supersedes, payload, reason) VALUES (?, ?, '{}', 'x')",
                           (members[1].value, first_entry))
        refuses("a second entry superseding the same entry", lambda: ledger._db.execute(
            "INSERT INTO ledger_entries (event_id, supersedes, payload, reason) VALUES (?, ?, '{}', 'x')",
            (members[2].value, first_entry)), (sqlite3.IntegrityError,))
        ledger.close()
        events.close()
        entities.close()
    return {"classification": "negative_control", "refusals_verified": len(refused), "refused": sorted(refused)}


#: Fixed, ordered candidate seeds for the "another seed" control. The first whose hash order selects a different set
#: from the real one is used, so the planted record is wrong by construction, whatever seed the store drew.
OTHER_SEEDS = tuple(f"{index:064x}" for index in range(64))


def record_reproduces(holdout):
    """Gate I's reproduction check on a holdout record alone: the procedure, set hash, selection and its hash."""

    return (holdout.procedure == PROCEDURE and holdout.content_hash == content_hash(holdout.members)
            and ordered_selection(holdout.seed, holdout.members, holdout.size) == holdout.selected
            and holdout.selection_hash == selection_hash(holdout.selected))


def planted_selections(holdout):
    """Two holdout records that are wrong by construction, each internally consistent except in its selection.

    - Another seed: the recorded selection is kept, and the seed is replaced by the first fixed candidate whose hash
      order selects a different set.
    - A fixed identifier order: the first `size` members by identifier, or the last `size` where the first equal the
      real selection. With at least twice `size` members the two are disjoint, so one of them always differs. Its
      selection hash is recomputed, so only the ordering can expose it.

    Built with the real procedure, independently of `record_reproduces`, so a broken check cannot shape its own
    controls. Fails, rather than plant a correct record, if no wrong one exists.
    """

    members = tuple(sorted(holdout.members))
    other = next((seed for seed in OTHER_SEEDS if seed != holdout.seed
                  and ordered_selection(seed, members, holdout.size) != holdout.selected), None)
    if other is None:
        fail("no candidate seed selects a different set, so the another-seed control would prove nothing")
    if 2 * holdout.size > len(members):
        fail("the fixed-order control needs at least twice the selection size in members")
    fixed = members[:holdout.size] if members[:holdout.size] != holdout.selected else members[-holdout.size:]
    return (("another seed", dataclasses.replace(holdout, seed=other)),
            ("a fixed identifier order instead of the hash order",
             dataclasses.replace(holdout, selected=fixed, selection_hash=selection_hash(fixed))))


def gate_i_holdout_leakage():
    """The holdout re-derives from its record, and the leakage check flags every planted leak (H2 s5, s8)."""

    controls = {}
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "evidence.sqlite"
        entities, events, owner = _ledger_world(path)
        ledger = HistoricalLedger(path)
        members = [_answered(events, owner, day) for day in range(1, 11)]
        for identifier in members:
            ledger.admit(identifier, Elicitation.PROMPTED_FOR_NULL_PERIOD, PROVENANCE)
        ledger.read(Purpose.DEVELOPMENT)
        number = ledger.freeze_and_select("ten", members, 4)
        holdout = ledger.holdout(number)
        protocol_number = ledger.register_protocol(_protocol(number, 4))
        ledger.read(Purpose.PROTECTED_VALIDATION, protocol_number)
        if not ledger.reproduces(number) or not record_reproduces(holdout) or leakage_findings(path) != []:
            fail("a clean holdout did not reproduce, or a clean log reported leakage")
        for label, planted in planted_selections(holdout):
            if record_reproduces(planted):
                fail(f"the reproduction check accepted a selection from {label}")
            controls[f"selection from {label} rejected"] = True
        outside = sorted(set(members) - set(holdout.selected))[0].value
        db = ledger._db
        for purpose in sorted(EXCLUDED_FROM_PROTECTED, key=lambda item: item.value):
            db.execute("INSERT INTO access_log (purpose, protocol_number, granted, served, note) "
                       "VALUES (?, NULL, 1, ?, 'planted')", (purpose.value, json.dumps([holdout.selected[0].value])))
        db.execute("INSERT INTO access_log (purpose, protocol_number, granted, served, note) "
                   "VALUES ('protected_validation', ?, 1, '[]', 'planted')", (LAST_TEST,))
        db.execute("INSERT INTO access_log (purpose, protocol_number, granted, served, note) "
                   "VALUES ('protected_validation', ?, 1, ?, 'planted')", (protocol_number, json.dumps([outside])))
        db.execute("INSERT INTO access_log (purpose, protocol_number, granted, served, note) "
                   "VALUES ('undeclared', NULL, 1, '[]', 'planted')")
        (last,) = db.execute("SELECT MAX(access_number) FROM access_log").fetchone()
        late = db.execute("INSERT INTO protocols (holdout_number, after_access, payload) VALUES (?, ?, '{}')",
                          (number, last + 1)).lastrowid
        db.execute("INSERT INTO access_log (purpose, protocol_number, granted, served, note) "
                   "VALUES ('protected_validation', ?, 1, '[]', 'planted')", (late,))
        findings = leakage_findings(path)
        planted_leaks = [(f"protected entry served for {purpose.value}", "L1", f"served for {purpose.value}")
                         for purpose in sorted(EXCLUDED_FROM_PROTECTED, key=lambda item: item.value)]
        planted_leaks += [("protected validation with no protocol", "L2", "no registered protocol"),
                          ("protected validation before its protocol", "L2", f"before protocol {late}"),
                          ("protected validation outside its holdout", "L3", outside),
                          ("a granted read with no declared purpose", "L4", "no declared purpose")]
        for label, code, fragment in planted_leaks:
            if not any(finding.startswith(code) and fragment in finding for finding in findings):
                fail(f"the leakage check missed a planted leak: {label}")
            controls[f"planted leak flagged: {label}"] = True
        ledger.close()
        events.close()
        entities.close()
    return {"classification": "negative_control", "controls_rejected": len(controls), "controls": sorted(controls),
            "holdout_members": len(members), "holdout_selected": 4}


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
        "G_ledger_integrity": gate_g_ledger_integrity(),
        "H_ledger_refusals": gate_h_ledger_refusals(),
        "I_holdout_leakage": gate_i_holdout_leakage(),
    }
    report = {
        "schema": "evidence_foundations_v1_certification",
        "adr": "ADR-0115 s4; ADR-0116 s4",
        "date": str(date.today()),
        "scope": ("Structural certification of the EVIDENCE foundations: the H0 entity model, append-only entity store "
                  "and ENT issuer (ADR-0114 WP-E1), and the H1 event model, append-only event store, separate "
                  "confirmation records, EVR issuer and seeded event-class vocabulary (ADR-0115 WP-E2), and the H2 "
                  "historical ledger, protected holdouts, pre-registered protocols and purpose-declared access log "
                  "(ADR-0116 WP-E3)."),
        "reference": {
            "structure": "the model contracts of ADR-0114 s3, ADR-0115 s5 and ADR-0116 s5, exercised on synthetic "
                         "records",
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
            "the ledger's purpose check and leakage check cover reads through the ledger only: EventStore, "
            "EntityStore, the ledger's own database connection and direct SQLite access read protected events "
            "without a purpose and without a log entry, and no such read can be detected here",
            "the store draws the holdout seed and forbids refreezing any frozen event, but cannot stop a caller "
            "recording near-duplicate events to build a new eligible set",
            "no TEST record, performance measurement or validation-run result is certified: they need H4 and H5",
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
