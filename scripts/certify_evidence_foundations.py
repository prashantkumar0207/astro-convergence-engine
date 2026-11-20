"""EVIDENCE_FOUNDATIONS_V1 CERTIFICATION RUNNER (ADR-0115 s4; ADR-0116 s4; ADR-0119 s3; ADR-0120 s4; ADR-0121;
ADR-0122 s6; ADR-0124; ADR-0125; ADR-0127; ADR-0130).

Regenerates certification/EVIDENCE_FOUNDATIONS_V1_certification.json FROM SCRATCH on every run;
the stored JSON is never accepted as proof.

STRUCTURAL certification of the EVIDENCE foundations: the H0 entity model and store (ADR-0114),
the H1 event model, event store and EVR issuer (ADR-0115), the H2 historical ledger and its
protected holdouts (ADR-0116), the H4 evidence model, its store and the EVD issuer (ADR-0119), and
the H5 rule registry, its pinned snapshot and the governed RUL authoring process (ADR-0120, ADR-0121),
and the provenance graph recorded at evidence-creation time (ADR-0122). It is NOT astrological-calculation certification and certifies no production analytical input. Every record it uses is synthetic, and
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
  J  H4 structural integrity: every polarity, supplied and absent uncertainty and performance, rule
     versions, recomputation, decomposable counts, a clean join, durable and separate issuers.
  K  H4 refusals: each one the WP-E4 contract requires, triggered for real, with its reason checked,
     including a join differing in each field of the calculation Provenance.
  L  relationships from recorded structure, and provenance comparison on every field; each rejects
     planted wrong comparators that are wrong by construction.
  M  H5 registry integrity: every published rule verifies, round-trips and is bound to its issued
     RUL; versions are 1..n; two variants are kept; the authoring process produced the files.
  N  H5 and RUL refusals: unregistered lookups, malformed or free-text records, non-synthetic rules,
     and every way the evidence store could issue, reuse, rebind or bypass a RUL identity.
  O  the snapshot fails closed on each planted violation, even where the pin is made to match.
  P  the provenance graph: every node kind, content-addressed identity separating every provenance
     field, shared nodes recorded once, the parent chart, registry rule nodes, durability.
  Q  provenance-graph refusals: undeclared and correlated edges, disallowed pairs, dangling edges,
     cycles, forged or malformed nodes, rows planted by direct SQL, and UPDATE or DELETE.
  R  the graph's agreement with the evidence: each item reproduced exactly from its graph alone, and
     the graph exactly what the items' records give; broken comparators are distinguishable.
  S  evidence read integrity: rows written around persist() are refused by every read; legitimate records,
     those under an earlier snapshot included, stay readable; each real check, weakened, admits the forgery.
  T  relationship integrity: a persisted relationship is returned only if classifying the same immutable items gives
     exactly its dependency, conflict flag and basis; each real check, weakened, admits the forgery.
  U  historical rule integrity: a rule version recorded under an earlier snapshot is read only as an issued RUL,
     under its school, and a version still published unchanged; genuine history stays readable.
  V  genuine-rule publication: only from an authorized source of the rule's own school, at a precise locator, with
     checked claims verified; published for citation and never projected into evidence, however a row is written.
  W  the explanation boundary: a candidate is references only, refused fail closed otherwise; every sentence is
     rendered from the evidence store's checked reads and the pinned registry, never from the candidate.

Exit 0 = PASS, 3 = FAIL.
"""

import ast
import dataclasses
import hashlib
import json
import re
import shutil
import sqlite3
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

sys.path.insert(0, str(ROOT / "scripts"))
import author_rule_registry  # noqa: E402
import check_rule_registry  # noqa: E402
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
from engine.evidence.evidence import (  # noqa: E402
    CONFIDENCE_COMPONENTS, LATER_PHASE_COMPONENTS, CalculatedInput, ChartContext, ChartReference, Confidence,
    DependencyClass, Domain, EvidenceItem, EvidenceModelError, Lineage, Performance, Polarity, ProducingSystem,
    Relationship, RuleReference, RuleSpec, RuleVersion, Supplied, TimingContext, TimingKind, provenance_differences,
)
from engine.evidence import explanation_boundary  # noqa: E402
from engine.evidence import provenance_graph  # noqa: E402
from engine.evidence import rule_registry  # noqa: E402
from engine.evidence.evidence_identifiers import EvidenceId, RuleId  # noqa: E402
from engine.evidence.evidence_store import (  # noqa: E402
    EvidenceStore, item_from_record, item_to_record, relationship_to_record, rule_from_record, rule_to_record,
)
from engine.models.provenance import Provenance  # noqa: E402

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


# ------------------------------------------------------------------ H4 (ADR-0119)

CALC = Provenance(profile_name="parashari_lahiri", ayanamsa_mode=1, frame="sidereal", house_system="W",
                  node_policy="mean", ephemeris_mode="swieph")
#: One different value for every field of the frozen Provenance (ADR-0119 AC11).
PROVENANCE_VARIANTS = {"profile_name": "kp_krishnamurti", "ayanamsa_mode": 5, "frame": "tropical",
                       "house_system": "P", "node_policy": "true", "ephemeris_mode": "moseph", "time_basis": "TT"}
CERTIFIER_HASH = "c" * 64


#: The registry's synthetic fixture rules the H4 gates register (ADR-0121: rules come only from the pinned registry).
PARASHARI_KEY, KP_KEY = "synthetic.parashari.tenth-lord-in-tenth", "synthetic.kp.tenth-cusp-sublord"
#: The fixture rule published under two named variants.
VARIANTS_KEY = "synthetic.parashari.moon-in-fourth"


def _rule_spec(school, strength="as declared by the synthetic source"):
    """A RuleSpec for model-level refusals only; it is never registered."""

    return RuleSpec(school=school, content_hash=CERTIFIER_HASH, knowledge_snapshot_hash="d" * 64,
                    declared_strength=strength, variant="base", provenance=PROVENANCE, data_class=DataClass.SYNTHETIC)


class _EvidenceWorld:
    """Builds synthetic items for one entity and the rule versions a gate registered in its own store."""

    def __init__(self, owner, label, rules):
        self.owner, self.label, self.rules = owner, label, rules

    def lineage(self, facts, provenance=CALC, inputs_complete=True, derivations_complete=True):
        return Lineage(inputs=tuple(CalculatedInput(fact=fact, provenance=provenance) for fact in facts),
                       inputs_complete=inputs_complete, derivations_complete=derivations_complete)

    def item(self, system=ProducingSystem.PARASHARI, facts=("Moon longitude",), **changes):
        rule = self.rules[system]
        base = EvidenceItem(
            entity=self.owner, domain=Domain.JATAKA, question=None, producing_system=system,
            rule=RuleReference(rule=rule.rule, version=rule.version, variant=rule.spec.variant),
            declared_strength=rule.spec.declared_strength,
            measured_reliability=None, lineage=self.lineage(facts),
            chart=ChartReference(entity_revision=1, chart_label=self.label),
            chart_context=ChartContext(varga="D1", planets=("Moon",), houses=(10,), signs=(4,), significators=()),
            timing=TimingContext(kind=TimingKind.DASHA, label="synthetic period", start="2010-01-01",
                                 end="2012-12-31"),
            polarity=Polarity.POSITIVE,
            confidence=Confidence(**{name: None for name in CONFIDENCE_COMPONENTS}),
            historical_performance=None, derived_from=(), recomputes=None, provenance=PROVENANCE,
            data_class=DataClass.SYNTHETIC)
        return dataclasses.replace(base, **changes)


def evidence_round_trips(evidence_id, item, serialize=None) -> bool:
    """Gate J's round-trip comparator: the stored form rebuilds exactly the identity and item it was made from."""

    record = (serialize or item_to_record)(evidence_id, item)
    return item_from_record(json.loads(json.dumps(record))) == (evidence_id, item)


def partition_failures(counts, ids) -> list:
    """Gate J's decomposition comparator: every axis's partitions cover the members exactly once."""

    failures = []
    for axis in ("producing_system", "domain", "polarity", "rule"):
        parts = [set(members) for members in counts[axis].values()]
        if set().union(*parts) != set(ids) or sum(len(part) for part in parts) != len(ids):
            failures.append(axis)
    return failures


def gate_j_evidence_integrity():
    """H4 structural integrity: every polarity, supplied and absent uncertainty, rule versions, recomputation,
    decomposable counts, a clean join, and durability (ADR-0119 s5)."""

    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "evidence.sqlite"
        store = EvidenceStore(path)
        owner = store.entities.persist(_synthetic_subjects()[0])
        registry = rule_registry.pinned()
        rules = {ProducingSystem.PARASHARI: store.register_rule(registry.rule_version(
                     registry.by_key(PARASHARI_KEY), 1, "base")),
                 ProducingSystem.KP: store.register_rule(registry.rule_version(registry.by_key(KP_KEY), 1, "base"))}
        world = _EvidenceWorld(owner, store.entities.load(owner).charts[0].label, rules)
        supplied = Supplied(value="as supplied by the synthetic source", provenance=PROVENANCE)
        ids = [store.persist(world.item(polarity=polarity)) for polarity in Polarity]
        with_uncertainty = world.item(
            ProducingSystem.KP, facts=("Sun longitude",),
            confidence=Confidence(**{name: (None if name in LATER_PHASE_COMPONENTS else supplied)
                                     for name in CONFIDENCE_COMPONENTS}),
            historical_performance=Performance(value="0", sample_size=12, provenance=PROVENANCE))
        ids.append(store.persist(with_uncertainty))
        ids.append(store.persist(world.item(facts=("Mars longitude",), recomputes=ids[0])))
        second = store.register_rule(registry.rule_version(world.rules[ProducingSystem.PARASHARI].rule, 2, "base"))
        if [rule.version for rule in store.rule_versions(second.rule)] != [1, 2] or \
                rule_from_record(rule_to_record(second)) != second:
            fail("a new rule version did not append beside the first, or did not round-trip")
        for evidence_id in ids:
            if not evidence_round_trips(evidence_id, store.load(evidence_id)):
                fail("an evidence item did not round-trip")
        if [store.load(evidence_id).polarity for evidence_id in ids[:5]] != list(Polarity):
            fail("the five polarities were not all kept")
        loaded = store.load(ids[5])
        if loaded.historical_performance.value != "0" or store.load(ids[0]).historical_performance is not None or \
                loaded.confidence.timing_convergence is not None or loaded.confidence.rule_confidence != supplied:
            fail("supplied and absent uncertainty or performance were not kept apart")
        if store.recomputations(ids[0]) != [ids[6]] or store.load(ids[0]).polarity is not Polarity.POSITIVE:
            fail("a recomputation did not append beside its original")
        counts = store.counts()
        for axis in partition_failures(counts, ids):
            fail(f"the {axis} partition does not decompose the total")
        # Negative controls, invalid by construction (CEO HOLD on PR #54, item 3): each comparator above must
        # reject a planted violation of exactly the property it checks.
        controls = {}

        def lossy(evidence_id, item):
            record = item_to_record(evidence_id, item)
            record["evidence"]["historical_performance"] = None
            return record

        if loaded.historical_performance is None or evidence_round_trips(ids[5], loaded, lossy):
            fail("the round-trip comparator accepted a serializer that drops supplied historical performance")
        controls["a serializer dropping historical performance rejected"] = True
        dropped = {**counts, "polarity": {key: tuple(member for member in members if member != ids[0])
                                          for key, members in counts["polarity"].items()}}
        if ids[0] not in counts["polarity"][Polarity.POSITIVE.value] or partition_failures(dropped, ids) != ["polarity"]:
            fail("the decomposition comparator accepted a partition that loses a member")
        controls["a partition losing a member rejected"] = True
        if set(counts["members"]) != set(ids) or len(store.join(ids)) != len(ids):
            fail("a clean join or the members map lost an item")
        issued = store.issued_count("EVD")
        recorded = store.rule_versions(second.rule)
        try:
            store.issued_count("RUL")
            fail("the evidence store reported a RUL counter; RUL is issued only by the registry (ADR-0121)")
        except StoreError:
            pass
        store.close()
        reopened = EvidenceStore(path)
        durable = reopened.evidence_ids() == ids and reopened.issued_count("EVD") == issued and \
            reopened.load(ids[5]) == loaded and reopened.rule_versions(second.rule) == recorded
        reopened.close()
        if not durable or issued != len(ids):
            fail("the evidence store, its EVD issuer or its recorded rule versions are not durable")
    return {"classification": "structural_integrity", "items_persisted": len(ids), "polarities": len(Polarity),
            "confidence_components": len(CONFIDENCE_COMPONENTS), "rule_versions_checked": 3,
            "recomputations_checked": 1, "count_axes": 4, "mismatches": 0, "controls_rejected": len(controls),
            "controls": sorted(controls)}


def gate_k_evidence_refusals():
    """Each refusal the WP-E4 contract requires, triggered for real, with its reason checked (ADR-0119 s5)."""

    refused = {}

    def refuses(label, action, errors=(EvidenceModelError, StoreError), reason=""):
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
        store = EvidenceStore(path)
        owner = store.entities.persist(_synthetic_subjects()[0])
        registry = rule_registry.pinned()
        rules = {ProducingSystem.PARASHARI: store.register_rule(registry.rule_version(
                     registry.by_key(PARASHARI_KEY), 1, "base")),
                 ProducingSystem.KP: store.register_rule(registry.rule_version(registry.by_key(KP_KEY), 1, "base"))}
        world = _EvidenceWorld(owner, store.entities.load(owner).charts[0].label, rules)
        rule = world.rules[ProducingSystem.PARASHARI]
        for label, change, reason in (
                ("a rule school given as text", {"school": "parashari"}, "ProducingSystem"),
                ("a rule content hash that is not SHA-256", {"content_hash": "C" * 64}, "SHA-256"),
                ("a rule with no knowledge snapshot hash", {"knowledge_snapshot_hash": ""}, "SHA-256"),
                ("a rule with no declared strength", {"declared_strength": " "}, "declared_strength"),
                ("a real rule registration", {"synthetic_reference": False}, "synthetic structural references"),
                ("a non-synthetic rule", {"data_class": "real"}, "synthetic")):
            refuses(label, lambda change=change: dataclasses.replace(_rule_spec(ProducingSystem.PARASHARI), **change),
                    reason=reason)
        for key in ("statement", "condition", "apply"):
            planted = rule_to_record(rule)
            planted["rule_version"][key] = "planted"
            refuses(f"rule {key} in a rule-version record", lambda planted=planted: rule_from_record(planted),
                    reason="refused")
        refuses("a rule version claiming another school", lambda: store.register_rule(dataclasses.replace(
            rule, spec=dataclasses.replace(rule.spec, school=ProducingSystem.KP))), reason="school differs")
        for label, change, reason in (
                ("evidence with no entity", {"entity": None}, "ENT entity"),
                ("evidence with question linkage", {"question": "planted"}, "question linkage"),
                ("evidence with no rule", {"rule": None}, "rule cannot be named"),
                ("evidence with measured reliability", {"measured_reliability": "planted"}, "measured reliability"),
                ("evidence with no lineage", {"lineage": None}, "lineage"),
                ("evidence with no chart reference", {"chart": None}, "chart"),
                ("evidence with no timing", {"timing": None}, "timing"),
                ("evidence with an unknown polarity", {"polarity": "mixed"}, "Polarity"),
                ("non-synthetic evidence", {"data_class": "real"}, "synthetic")):
            refuses(label, lambda change=change: world.item(**change), reason=reason)
        refuses("a profile name instead of provenance", lambda: CalculatedInput(fact="Moon", provenance="parashari"),
                reason="profile name alone")
        refuses("a later-phase confidence component", lambda: Confidence(**{
            name: (Supplied(value="x", provenance=PROVENANCE) if name == "timing_convergence" else None)
            for name in CONFIDENCE_COMPONENTS}), reason="later-phase")
        refuses("performance with no sample size", lambda: Performance(value="0", sample_size=0,
                                                                         provenance=PROVENANCE), reason="sample size")
        refuses("a correlated relationship", lambda: Relationship(
            EvidenceId.from_number(1), EvidenceId.from_number(2), DependencyClass.CORRELATED, False, "planted"),
            reason="CORRELATED")
        refuses("an unregistered rule version", lambda: store.persist(world.item(
            rule=RuleReference(rule=rule.rule, version=9, variant="base"))), reason="not registered")
        refuses("a rule from another system", lambda: store.persist(world.item(
            rule=RuleReference(rule=world.rules[ProducingSystem.KP].rule, version=1, variant="base"))),
                reason="isolated")
        refuses("a strength other than the rule's", lambda: store.persist(world.item(declared_strength="planted")),
                reason="declared strength")
        refuses("a chart the entity does not have", lambda: store.persist(world.item(
            chart=ChartReference(entity_revision=1, chart_label="planted"))), reason="is not a chart")
        refuses("a derivation link to no item", lambda: store.persist(world.item(
            derived_from=(EvidenceId.from_number(LAST_TEST),))), reason="no such evidence")
        first = store.persist(world.item())
        second = store.persist(world.item(ProducingSystem.KP, facts=("Sun longitude",)))
        store.relate(first, second)
        for field, value in sorted(PROVENANCE_VARIANTS.items()):
            other = dataclasses.replace(CALC, **{field: value})
            mismatched = store.persist(world.item(ProducingSystem.KP, facts=(f"{field} probe",),
                                                  lineage=world.lineage((f"{field} probe",), provenance=other)))
            refuses(f"a join differing only in {field}", lambda mismatched=mismatched: store.join([first, mismatched]),
                    reason=f"differs in {field};")
            # CEO HOLD on PR #54, item 2: relating is a join and goes through the same rule.
            refuses(f"a relationship differing only in {field}",
                    lambda mismatched=mismatched: store.relate(first, mismatched),
                    reason=f"differ in calculation provenance ({field})")
        # A persisted relationship joining incompatible items is refused when read, however it was written. Each
        # is planted in its own store, so the refusal names exactly the planted field.
        for field in ("profile_name", "time_basis"):
            separate = EvidenceStore(Path(folder) / f"planted_{field}.sqlite")
            entity = separate.entities.persist(_synthetic_subjects()[0])
            planted_rules = {ProducingSystem.PARASHARI: separate.register_rule(registry.rule_version(
                                 registry.by_key(PARASHARI_KEY), 1, "base")),
                             ProducingSystem.KP: separate.register_rule(registry.rule_version(
                                 registry.by_key(KP_KEY), 1, "base"))}
            planted_world = _EvidenceWorld(entity, separate.entities.load(entity).charts[0].label, planted_rules)
            left = separate.persist(planted_world.item())
            right = separate.persist(planted_world.item(ProducingSystem.KP, lineage=planted_world.lineage(
                ("Sun longitude",), provenance=dataclasses.replace(CALC, **{field: PROVENANCE_VARIANTS[field]}))))
            planted = relationship_to_record(Relationship(left, right, DependencyClass.INDEPENDENT, False, "planted"))
            separate._db.execute("INSERT INTO evidence_relationships (first_id, second_id, payload) VALUES (?, ?, ?)",
                                 (left.value, right.value, json.dumps(planted)))
            refuses(f"reading a persisted relationship differing in {field}", separate.relationships,
                    reason=f"differ in calculation provenance ({field})")
            separate.close()
        record = item_to_record(first, store.load(first))
        for key in ("schema", "id"):
            planted = json.loads(json.dumps(record))
            planted.pop(key)
            refuses(f"an evidence record with no {key}", lambda planted=planted: item_from_record(planted),
                    reason="schema version and EVD identity")
        for path in (("evidence",), ("evidence", "lineage"), ("evidence", "confidence")):
            planted = json.loads(json.dumps(record))
            node = planted
            for key in path:
                node = node[key]
            node["score"] = 1
            refuses(f"an analytical key in {'.'.join(path)}", lambda planted=planted: item_from_record(planted),
                    reason="refused")
        for table in ("registered_rule_versions", "evidence_items", "evidence_relationships"):
            if not store._db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]:
                fail(f"{table} is empty, so a refused update or delete of it would prove nothing")
            for verb, sql in (("update", f"UPDATE {table} SET payload = payload"), ("delete", f"DELETE FROM {table}")):
                refuses(f"{verb} {table}", lambda sql=sql: store._db.execute(sql), (sqlite3.DatabaseError,),
                        reason="append-only")
        store.close()
    return {"classification": "negative_control", "refusals_verified": len(refused), "refused": sorted(refused)}


def gate_l_relationships_and_provenance():
    """Relationships from recorded structure, and provenance mismatch on every field; each comparator rejects
    planted wrong ones that are wrong by construction (ADR-0119 AC11, AC12; the ADR-0118 standard)."""

    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "evidence.sqlite"
        store = EvidenceStore(path)
        owner = store.entities.persist(_synthetic_subjects()[0])
        registry = rule_registry.pinned()
        rules = {ProducingSystem.PARASHARI: store.register_rule(registry.rule_version(
                     registry.by_key(PARASHARI_KEY), 1, "base")),
                 ProducingSystem.KP: store.register_rule(registry.rule_version(registry.by_key(KP_KEY), 1, "base"))}
        world = _EvidenceWorld(owner, store.entities.load(owner).charts[0].label, rules)
        kp = ProducingSystem.KP
        anchor = store.persist(world.item(facts=("Moon longitude",)))
        child = store.persist(world.item(kp, facts=("Sun longitude",), derived_from=(anchor,)))
        sharing = store.persist(world.item(kp, facts=("Moon longitude",)))
        left = store.persist(world.item(facts=("Saturn",), derived_from=(anchor,)))
        right = store.persist(world.item(kp, facts=("Rahu",), derived_from=(anchor,)))
        independent = store.persist(world.item(kp, facts=("Venus",)))
        missing = store.persist(world.item(kp, facts=("Mars",), lineage=world.lineage(("Mars",),
                                                                                     derivations_complete=False)))
        incomplete = store.persist(world.item(kp, facts=("Mercury",), lineage=world.lineage(("Mercury",),
                                                                                           inputs_complete=False)))
        unverified_root = store.persist(world.item(kp, facts=("Ketu",), lineage=world.lineage(
            ("Ketu",), derivations_complete=False)))
        unverified = store.persist(world.item(kp, facts=("Jupiter",), derived_from=(unverified_root,)))
        same_system = store.persist(world.item(facts=("Lagna",)))
        # CEO HOLD on PR #54, item 1: ancestral inputs and their completeness are part of an item's lineage.
        moon_ancestor = store.persist(world.item(kp, facts=("Moon longitude",)))
        ancestral_sharer = store.persist(world.item(kp, facts=("Mercury longitude",), derived_from=(moon_ancestor,)))
        open_ancestor = store.persist(world.item(kp, facts=("Neptune",), lineage=world.lineage(
            ("Neptune",), inputs_complete=False)))
        ancestral_incomplete = store.persist(world.item(kp, facts=("Uranus",), derived_from=(open_ancestor,)))
        expected = {
            "a recorded derivation link": ((anchor, child), DependencyClass.DERIVED),
            "a shared input": ((anchor, sharing), DependencyClass.SHARED_ORIGIN),
            "a shared ancestor": ((left, right), DependencyClass.SHARED_ORIGIN),
            "positive recorded evidence": ((anchor, independent), DependencyClass.INDEPENDENT),
            "a missing link": ((anchor, missing), DependencyClass.UNKNOWN),
            "incomplete lineage": ((anchor, incomplete), DependencyClass.UNKNOWN),
            "an unverified derivation path": ((anchor, unverified), DependencyClass.UNKNOWN),
            "the same producing system": ((anchor, same_system), DependencyClass.UNKNOWN),
            "an ancestor sharing an input": ((anchor, ancestral_sharer), DependencyClass.SHARED_ORIGIN),
            "an ancestor with incomplete inputs": ((anchor, ancestral_incomplete), DependencyClass.UNKNOWN),
            "a derivation link despite incomplete ancestry": ((open_ancestor, ancestral_incomplete),
                                                              DependencyClass.DERIVED),
        }

        def mismatches(classify):
            return [label for label, (pair, wanted) in expected.items() if classify(*pair) is not wanted]

        real = lambda first, second: store.classify(first, second).dependency
        if mismatches(real):
            fail(f"the classification disagrees with the recorded structure: {mismatches(real)}")
        for pair, _wanted in expected.values():
            store.relate(*pair)
        counts = store.relationship_counts()
        if set(counts["unknown"]) & set(counts["independent"]) or len(counts["independent"]) != 1 or \
                counts["correlated"]:
            fail("an UNKNOWN or CORRELATED relationship was counted as INDEPENDENT")
        ancestral_pairs = {expected["an ancestor sharing an input"][0], expected["an ancestor with incomplete inputs"][0]}
        planted_classifiers = {
            "every pair independent": lambda first, second: DependencyClass.INDEPENDENT,
            "unknown treated as independent": lambda first, second: (
                DependencyClass.INDEPENDENT if real(first, second) is DependencyClass.UNKNOWN else real(first, second)),
            "derivation links ignored": lambda first, second: (
                DependencyClass.UNKNOWN if real(first, second) is DependencyClass.DERIVED else real(first, second)),
            "ancestral lineage ignored": lambda first, second: (
                DependencyClass.INDEPENDENT if (first, second) in ancestral_pairs else real(first, second)),
            "shared origin unrecorded": lambda first, second: (
                DependencyClass.INDEPENDENT if real(first, second) is DependencyClass.SHARED_ORIGIN
                else real(first, second)),
        }
        controls = {}
        for label, classify in planted_classifiers.items():
            if not mismatches(classify):
                fail(f"the relationship check accepted a planted classifier: {label}")
            controls[f"planted classifier rejected: {label}"] = True
        for field, value in sorted(PROVENANCE_VARIANTS.items()):
            other = dataclasses.replace(CALC, **{field: value})
            if provenance_differences(CALC, other) != (field,):
                fail(f"the provenance comparison missed or misnamed {field}")
            ignoring = lambda first, second, field=field: tuple(
                name for name in provenance_differences(first, second) if name != field)
            if ignoring(CALC, other) == provenance_differences(CALC, other):
                fail(f"a comparator ignoring {field} was not distinguishable from the real one")
            controls[f"planted comparator ignoring {field} rejected"] = True
        if provenance_differences(CALC, dataclasses.replace(CALC)) != ():
            fail("identical provenance was reported as different")
        store.close()
    return {"classification": "negative_control", "relationship_cases": len(expected),
            "provenance_fields": len(PROVENANCE_VARIANTS), "controls_rejected": len(controls),
            "controls": sorted(controls)}


# ------------------------------------------------------------------ H5 (ADR-0120; ADR-0121)

def registry_round_trips(item) -> bool:
    """Gate M's round-trip comparator: the published record rebuilds exactly the rule, under its own content hash."""

    try:
        rebuilt = rule_registry.rule_from_record({**rule_registry.content_record(item),
                                                  "content_hash": item.content_hash})
    except rule_registry.RegistryError:
        return False
    return rebuilt == item and rule_registry.content_hash(item) == item.content_hash


def files_match(committed: bytes, produced: bytes) -> bool:
    """Gate M's authoring comparator: a committed file is byte for byte what the authoring process produces."""

    return committed == produced


def registry_integrity_failures(registry: rule_registry.RuleRegistry, issued: dict, directory: Path,
                                round_trips=registry_round_trips, same_file=files_match) -> list:
    """Gate M's checks, as a function of what they inspect, so each can be shown to fail on a planted violation
    (CEO HOLD on PR #56, item 2). Returns (check, message) for every failure; an empty list is an intact registry."""

    failures = []
    rules = registry.rules()
    for item in rules:
        label = f"{item.rule} v{item.version} {item.variant!r}"
        if not round_trips(item):
            failures.append(("round_trip", f"{label} does not round-trip or its content hash disagrees"))
        if issued.get(item.rule.number) != (item.key, item.school):
            failures.append(("binding", f"{label} is not bound to the identity the allocation history issued"))
        try:
            retrieved = registry.lookup(item.rule, item.version, item.variant)
            claimed = registry.rule_version(item.rule, item.version, item.variant)
        except rule_registry.RegistryError as exc:
            failures.append(("published", f"{label} is not retrievable as published: {exc}"))
            continue
        if retrieved != item or item.synthetic is not True or item.certification.measured_performance is not None:
            failures.append(("published", f"{label} is not retrievable as published, or is not synthetic"))
        if (claimed.rule, claimed.version, claimed.spec.content_hash, claimed.spec.knowledge_snapshot_hash,
                claimed.spec.variant, claimed.spec.school) != (item.rule, item.version, item.content_hash,
                                                               registry.snapshot_sha256, item.variant, item.school):
            failures.append(("store_view", f"the evidence store's view of {label} disagrees with the rule"))
    identities = [(item.rule, item.version, item.variant) for item in rules]
    if len(set(identities)) != len(identities):
        failures.append(("published", "a rule is published under another rule's identity"))
    rule_ids = sorted({item.rule for item in rules})
    for rule in rule_ids:
        versions = list(registry.versions(rule))
        if versions != list(range(1, len(versions) + 1)):
            failures.append(("versions", f"{rule}'s versions are not 1..n"))
    if not [(rule, version) for rule in rule_ids for version in registry.versions(rule)
            if len(registry.variants(rule, version)) > 1]:
        failures.append(("variants", "no published rule carries two named variants, so variant handling is "
                                     "unexercised"))
    if sorted(issued) != list(range(1, len(issued) + 1)) or sorted(item.number for item in rule_ids) != sorted(issued):
        failures.append(("allocation", "the published rules and the allocation history disagree"))
    try:
        history, snapshot, manifest = author_rule_registry.build(directory)
    except SystemExit as exc:
        failures.append(("authoring", f"the authoring process refuses the committed source: {exc}"))
        return failures
    for name, expected in ((rule_registry.HISTORY_NAME, history), ("snapshot.json", snapshot),
                           (rule_registry.MANIFEST_NAME, manifest)):
        if not same_file((directory / name).read_bytes(), expected):
            failures.append(("authoring", f"{name} is not exactly what the governed authoring process produces"))
    return failures


def _forged_rule(item, **fields):
    """A RegistryRule carrying fields its constructor refuses, built around the constructor on purpose: only Gate M's
    own check can then reject it."""

    planted = object.__new__(type(item))
    for field in dataclasses.fields(item):
        object.__setattr__(planted, field.name, fields[field.name] if field.name in fields else
                           item.__getattribute__(field.name))
    return planted


class _MisreportingRegistry(rule_registry.RuleRegistry):
    """A registry whose evidence-store view names another snapshot than the one it was loaded from."""

    def rule_version(self, rule, version, variant):
        honest = super().rule_version(rule, version, variant)
        return dataclasses.replace(honest, spec=dataclasses.replace(honest.spec, knowledge_snapshot_hash="f" * 64))


def gate_m_registry_integrity():
    """The pinned registry: every published rule verifies, round-trips and is bound to its issued RUL; versions are
    1..n; variants are named and both kept; the four certification claims are separate; the authoring process
    produced exactly the committed files (ADR-0120 AC1 to AC5, AC10, AC11; ADR-0121). Each check then rejects a
    planted violation, wrong by construction, and each comparator is distinguishable from a broken one (CEO HOLD on
    PR #56, item 2)."""

    registry = rule_registry.pinned()
    rules = registry.rules()
    issued = rule_registry.read_history(rule_registry.DATA_DIR / rule_registry.HISTORY_NAME)
    for _check, message in registry_integrity_failures(registry, issued, rule_registry.DATA_DIR):
        fail(message)
    rule_ids = sorted({item.rule for item in rules})
    with_variants = [(rule, version) for rule in rule_ids for version in registry.versions(rule)
                     if len(registry.variants(rule, version)) > 1]

    controls = {}
    snapshot = registry.snapshot_sha256
    first, variants = registry.by_key(PARASHARI_KEY), registry.by_key(VARIANTS_KEY)
    target = registry.lookup(first, 1, "base")
    non_synthetic = _forged_rule(target, synthetic=False)
    non_synthetic = _forged_rule(non_synthetic, content_hash=rule_registry.content_hash(non_synthetic))

    def replacing(old, new):
        return rule_registry.RuleRegistry(tuple(new if item == old else item for item in rules), snapshot)

    def without(predicate):
        return rule_registry.RuleRegistry(tuple(item for item in rules if not predicate(item)), snapshot)

    misfiled = rule_registry.RuleRegistry(rules, snapshot)
    misfiled._rules[(variants, 1, "reading-a")] = registry.lookup(variants, 1, "reading-b")
    hash_disagrees = replacing(target, _forged_rule(target, content_hash="e" * 64))
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)

        def planted_directory(name, mutate):
            directory = root / name
            shutil.copytree(rule_registry.DATA_DIR, directory)
            mutate(directory)
            return directory

        def reformat_manifest(directory):
            data = json.loads((directory / rule_registry.MANIFEST_NAME).read_bytes())
            (directory / rule_registry.MANIFEST_NAME).write_bytes((json.dumps(data, indent=4) + "\n").encode("ascii"))

        def move_school(directory):
            source = json.loads((directory / author_rule_registry.SOURCE_NAME).read_bytes())
            source["rules"][0]["school"] = ProducingSystem.KP.value if source["rules"][0]["school"] != \
                ProducingSystem.KP.value else ProducingSystem.PARASHARI.value
            (directory / author_rule_registry.SOURCE_NAME).write_bytes(
                (json.dumps(source, sort_keys=True, indent=1) + "\n").encode("ascii"))

        reformatted = planted_directory("reformatted", reformat_manifest)
        cases = [
            ("a content hash that disagrees with the content", hash_disagrees, issued, rule_registry.DATA_DIR,
             {"round_trip"}),
            ("content changed under an unchanged hash", replacing(target, _forged_rule(target, statement="planted")),
             issued, rule_registry.DATA_DIR, {"round_trip"}),
            ("a rule bound to another identity than the history issued", registry,
             {**issued, first.number: ("synthetic.planted", target.school)}, rule_registry.DATA_DIR, {"binding"}),
            ("a rule not marked synthetic", replacing(target, non_synthetic), issued, rule_registry.DATA_DIR,
             {"round_trip", "published"}),
            ("measured performance supplied", replacing(target, _forged_rule(target, certification=_forged_rule(
                target.certification, measured_performance="0.9"))), issued, rule_registry.DATA_DIR,
             {"round_trip", "published"}),
            ("a rule filed under another variant's identity", misfiled, issued, rule_registry.DATA_DIR,
             {"published"}),
            ("an evidence-store view naming another snapshot", _MisreportingRegistry(rules, snapshot), issued,
             rule_registry.DATA_DIR, {"store_view"}),
            ("versions not 1..n", without(lambda item: (item.rule, item.version) == (first, 1)), issued,
             rule_registry.DATA_DIR, {"versions"}),
            ("no rule with two named variants", without(lambda item: item.variant == "reading-b"), issued,
             rule_registry.DATA_DIR, {"variants"}),
            ("an issued number no rule publishes", registry,
             {**issued, len(issued) + 1: ("synthetic.planted", target.school)}, rule_registry.DATA_DIR,
             {"allocation"}),
            ("a committed file the authoring process did not produce", registry, issued, reformatted, {"authoring"}),
            ("a source the authoring process refuses", registry, issued,
             planted_directory("school", move_school), {"authoring"}),
        ]
        for label, planted, history, directory, expected in cases:
            found = {check for check, _message in registry_integrity_failures(planted, history, directory)}
            if found != expected:
                fail(f"Gate M did not reject {label} for its intended check: expected {sorted(expected)}, "
                     f"found {sorted(found)}")
            controls[f"{label} rejected"] = True
        # Deliberately broken comparators: each must be distinguishable from the real one on a planted violation.
        for label, planted, directory, broken, check in (
                ("a round-trip comparator comparing a record with itself", hash_disagrees, rule_registry.DATA_DIR,
                 {"round_trips": lambda item: rule_registry.content_record(item) ==
                  rule_registry.content_record(item)}, "round_trip"),
                ("an authoring comparator comparing parsed JSON, not bytes", registry, reformatted,
                 {"same_file": lambda committed, produced: json.loads(committed) == json.loads(produced)},
                 "authoring")):
            real = {found for found, _message in registry_integrity_failures(planted, issued, directory)}
            weak = {found for found, _message in registry_integrity_failures(planted, issued, directory, **broken)}
            if check not in real or check in weak:
                fail(f"{label} was not distinguishable from the real one")
            controls[f"{label} rejected"] = True
    return {"classification": "structural_integrity", "rules_published": len(rule_ids),
            "rule_versions_published": len({(item.rule, item.version) for item in rules}),
            "variant_records": len(rules), "rules_with_two_variants": len(with_variants),
            "schools": len({item.school for item in rules}), "rul_numbers_issued": len(issued),
            "snapshot_sha256": registry.snapshot_sha256, "mismatches": 0, "controls_rejected": len(controls),
            "controls": sorted(controls)}


def gate_n_registry_refusals():
    """Each refusal WP-E5 and ADR-0121 require, triggered for real, with its reason checked: unregistered lookups,
    malformed or free-text records, non-synthetic rules, and every way the evidence store could be made to issue,
    reuse, rebind or bypass a RUL identity (ADR-0120 AC1 to AC4, AC7 to AC11; ADR-0121)."""

    refused = {}

    def refuses(label, action, errors=(rule_registry.RegistryError, StoreError, EvidenceModelError), reason=""):
        try:
            action()
        except errors as exc:
            if reason not in str(exc):
                fail(f"{label} was refused for another reason: {exc}")
            refused[label] = True
            return
        fail(f"not refused: {label}")

    registry = rule_registry.pinned()
    published = registry.rules()[0]
    first = registry.by_key(PARASHARI_KEY)
    refuses("a lookup of a RUL number never issued", lambda: registry.lookup(RuleId.from_number(LAST_TEST // 1000), 1,
                                                                             "base"), reason="is not registered")
    refuses("a lookup of an unpublished version", lambda: registry.lookup(first, 99, "base"), reason="is not registered")
    refuses("a lookup with no explicit variant", lambda: registry.lookup(first, 1, None), reason="explicit variant")
    refuses("a lookup of an unnamed variant", lambda: registry.lookup(first, 1, "default"), reason="is not registered")
    record = {**rule_registry.content_record(published), "content_hash": published.content_hash}
    for field in rule_registry.RECORD_FIELDS:
        planted = {key: value for key, value in record.items() if key != field}
        refuses(f"a published record missing {field}", lambda planted=planted: rule_registry.rule_from_record(planted),
                reason="refused")
    for key in ("rule_text", "llm_output", "code"):
        refuses(f"free text or code as {key}", lambda key=key: rule_registry.rule_from_record({**record, key: "x"}),
                reason="refused")
    for label, change, reason in (
            ("a rule not marked synthetic", {"synthetic": False}, "synthetic rules only"),
            ("a rule with an empty citation locator", {"citation": {"source": "s", "locator": " "}}, "citation locator"),
            ("a condition outside the declared schema", {"condition": {"kind": "eval", "parameters": {}}},
             "not in the declared schema"),
            ("a condition parameter of the wrong type",
             {"condition": {"kind": "planet_in_house", "parameters": {"planet": "Moon", "house": "lambda: 4"}}},
             "number from 1 to 12"),
            ("measured performance supplied",
             {"certification": {**record["certification"], "measured_performance": "0.9"}}, "measured performance"),
            ("an inferred school", {"school": "inferred"}, "unknown value"),
            ("a variant not among the known variants", {"variant": "unlisted"}, "known variants")):
        planted = {**record, **change}
        refuses(label, lambda planted=planted: rule_registry.rule_from_record(planted), reason=reason)
    refuses("a content change under an unchanged hash", lambda: rule_registry.rule_from_record(
        {**record, "statement": "planted"}), reason="content hash does not match")
    with tempfile.TemporaryDirectory() as folder:
        store = EvidenceStore(Path(folder) / "evidence.sqlite")
        good = registry.rule_version(first, 1, "base")
        store.register_rule(good)
        for label, change, reason in (("school", {"school": ProducingSystem.KP}, "school differs"),
                                      ("content hash", {"content_hash": "e" * 64}, "content hash differs"),
                                      ("snapshot hash", {"knowledge_snapshot_hash": "f" * 64}, "snapshot hash differs"),
                                      ("declared strength", {"declared_strength": "planted"}, "declared strength"),
                                      ("variant", {"variant": "reading-a"}, "is not registered")):
            refuses(f"a rule version claiming another {label}", lambda change=change: store.register_rule(
                dataclasses.replace(good, spec=dataclasses.replace(good.spec, **change))), reason=reason)
        refuses("a RUL number the registry never issued", lambda: store.register_rule(dataclasses.replace(
            good, rule=RuleId.from_number(LAST_TEST // 1000))), reason="is not registered")
        refuses("a version the registry never published", lambda: store.register_rule(dataclasses.replace(
            good, version=99)), reason="is not registered")
        refuses("a RUL identity rebound to another rule", lambda: store.register_rule(dataclasses.replace(
            registry.rule_version(registry.by_key(KP_KEY), 1, "base"), rule=first)), reason="differs")
        refuses("a duplicate registration", lambda: store.register_rule(good), reason="already registered")
        refuses("a free-standing rule spec", lambda: store.register_rule(_rule_spec(ProducingSystem.PARASHARI)),
                reason="registry's RuleVersion")
        refuses("the store issuing a RUL number", lambda: store.issued_count("RUL"), reason="issues EVD only")
        store._db.execute("INSERT INTO registered_rule_versions (rule_id, version, variant, payload) VALUES (?, ?, ?, ?)",
                          (first.value, 1, "planted", json.dumps(rule_to_record(dataclasses.replace(
                              good, spec=dataclasses.replace(good.spec, variant="planted", knowledge_snapshot_hash="f" * 64))))))
        owner = store.entities.persist(_synthetic_subjects()[0])
        world = _EvidenceWorld(owner, store.entities.load(owner).charts[0].label, {ProducingSystem.PARASHARI: good})
        refuses("evidence naming a rule from another snapshot", lambda: store.persist(world.item(
            rule=RuleReference(rule=first, version=1, variant="planted"))), reason="another snapshot")
        refuses("evidence naming an unrecorded variant", lambda: store.persist(world.item(
            rule=RuleReference(rule=first, version=1, variant="reading-b"))), reason="is not registered")
        # CEO HOLD on PR #56, item 1: rows written around register_rule that carry the pinned snapshot hash but are
        # not exactly what the pinned registry publishes under the identity the evidence names.
        variants = registry.by_key(VARIANTS_KEY)
        second = registry.rule_version(first, 2, "base")
        reading_b = registry.rule_version(variants, 1, "reading-b")
        unissued = RuleId.from_number(LAST_TEST // 1000)
        unpublished, mismatched = "not published by the pinned registry", "differs from the pinned registry's"
        for label, (rule, version, variant), row, reason in (
                ("a forged variant", (first, 1, "forged"),
                 dataclasses.replace(good, spec=dataclasses.replace(good.spec, variant="forged")), unpublished),
                ("an unissued RUL identity", (unissued, 1, "base"), dataclasses.replace(good, rule=unissued),
                 unpublished),
                ("a payload naming another published identity than its key", (variants, 1, "reading-a"), good,
                 mismatched),
                ("a published identity with forged content", (first, 2, "base"), dataclasses.replace(
                    second, spec=dataclasses.replace(second.spec, content_hash="e" * 64)), mismatched),
                ("a published identity with forged declared strength", (variants, 1, "reading-b"),
                 dataclasses.replace(reading_b, spec=dataclasses.replace(reading_b.spec, declared_strength="planted")),
                 mismatched)):
            if row.spec.knowledge_snapshot_hash != registry.snapshot_sha256:
                fail(f"the {label} control does not carry the pinned snapshot hash, so it tests nothing new")
            store._db.execute("INSERT INTO registered_rule_versions (rule_id, version, variant, payload) "
                              "VALUES (?, ?, ?, ?)", (rule.value, version, variant, json.dumps(rule_to_record(row))))
            refuses(f"evidence naming {label} under the pinned snapshot hash", lambda reference=RuleReference(
                rule=rule, version=version, variant=variant): store.persist(world.item(rule=reference)),
                reason=reason)
        if store.issued_count("EVD") != 0 or store.evidence_ids() != []:
            fail("a refused write took an EVD number or left an item")
        if store.rule_version(RuleReference(rule=first, version=1, variant="planted")).spec.knowledge_snapshot_hash \
                != "f" * 64 or store.persist(world.item()) != EvidenceId.from_number(1):
            fail("a historical snapshot record was not kept readable, or the published rule no longer admits evidence")
        store.close()
    return {"classification": "negative_control", "refusals_verified": len(refused), "refused": sorted(refused)}


def _rehash(record, **changes):
    """Apply changes to a published record and recompute its content hash, so only the intended check can fail."""

    record.update(changes)
    record["content_hash"] = hashlib.sha256(rule_registry.canonical(
        {key: value for key, value in record.items() if key != "content_hash"})).hexdigest()


def gate_o_snapshot_fails_closed():
    """The loader against planted copies of the pinned snapshot: each violation is wrong by construction and must
    fail closed for its stated reason (ADR-0120 AC5, AC6; ADR-0121)."""

    controls = {}
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        pin = rule_registry.PINNED_SNAPSHOT_SHA256

        def planted(name, mutate):
            target = root / name
            shutil.copytree(rule_registry.DATA_DIR, target)
            mutate(target)
            return target

        def rewrite_json(path, change):
            data = json.loads(path.read_bytes())
            change(data)
            path.write_bytes((json.dumps(data, sort_keys=True, indent=1) + "\n").encode("ascii"))

        def snapshot_change(change):
            def mutate(target):
                rewrite_json(target / "snapshot.json", change)
                digest = hashlib.sha256((target / "snapshot.json").read_bytes()).hexdigest()
                rewrite_json(target / rule_registry.MANIFEST_NAME, lambda data: data.update(sha256=digest))
            return mutate

        cases = [
            ("a changed byte", planted("byte", lambda target: (target / "snapshot.json").write_bytes(
                (target / "snapshot.json").read_bytes().replace(b"Synthetic fixture", b"Planted fixture", 1))), pin,
             "do not match the pinned hash"),
            ("a changed pin", rule_registry.DATA_DIR, "0" * 64, "differs from the pinned hash"),
            ("a missing snapshot", planted("nosnap", lambda target: (target / "snapshot.json").unlink()), pin,
             "cannot be read"),
            ("a missing manifest", planted("noman", lambda target: (target / rule_registry.MANIFEST_NAME).unlink()),
             pin, "cannot be read"),
            ("a missing allocation history", planted("nohist", lambda target: (
                target / rule_registry.HISTORY_NAME).unlink()), pin, "cannot be read"),
            ("a manifest naming a path outside the snapshot", planted("escape", lambda target: rewrite_json(
                target / rule_registry.MANIFEST_NAME, lambda data: data.update(snapshot="../knowledge.json"))), pin,
             "not a snapshot manifest"),
        ]
        for label, directory, use_pin, reason in cases:
            try:
                rule_registry.load_registry(directory, use_pin)
            except rule_registry.RegistryError as exc:
                if reason not in str(exc):
                    fail(f"{label} failed closed for another reason: {exc}")
                controls[f"{label} fails closed"] = True
                continue
            fail(f"the loader accepted {label}")
        repinned = [
            ("a schema violation", snapshot_change(lambda data: data.update(extra=1)), "only its schema's fields"),
            ("a number never issued", snapshot_change(lambda data: _rehash(data["rules"][0], rule=LAST_TEST // 1000)),
             "never issued by the authoring process"),
            ("a version published twice", snapshot_change(lambda data: data["rules"].append(data["rules"][0])),
             "published twice"),
            ("versions not 1..n", snapshot_change(lambda data: data.update(rules=data["rules"][1:])),
             "not 1..n"),
            ("an identity rebound in the history", lambda target: rewrite_json(
                target / rule_registry.HISTORY_NAME, lambda data: data["allocations"][2].update(key="planted")),
             "rebinds it"),
            ("a number reused in the history", lambda target: rewrite_json(
                target / rule_registry.HISTORY_NAME, lambda data: data["allocations"][1].update(number=1)),
             "issued once, in order"),
        ]
        for label, mutate, reason in repinned:
            directory = planted(label.replace(" ", "_"), mutate)
            digest = json.loads((directory / rule_registry.MANIFEST_NAME).read_bytes())["sha256"]
            try:
                rule_registry.load_registry(directory, digest)
            except rule_registry.RegistryError as exc:
                if reason not in str(exc):
                    fail(f"{label} failed closed for another reason: {exc}")
                controls[f"{label} fails closed, even with a matching pin"] = True
                continue
            fail(f"the loader accepted {label}")
    tree = ast.parse((ROOT / "engine" / "evidence" / "rule_registry.py").read_text(encoding="utf-8"))
    docstrings = {id(node.body[0].value) for node in ast.walk(tree)
                  if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef)) and node.body
                  and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant)}
    imported = {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names} |         {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}
    reaches = [name for name in imported if name.startswith("engine.knowledge")
               or name.split(".")[0] in {"openai", "anthropic", "requests", "urllib"}]
    evaluates = [node.func.id for node in ast.walk(tree) if isinstance(node, ast.Call)
                 and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "compile", "__import__"}]
    paths = [node.value for node in ast.walk(tree) if isinstance(node, ast.Constant) and isinstance(node.value, str)
             and id(node) not in docstrings and re.search(r"knowledge/|knowledge\\|hlkg", node.value)]
    if reaches or evaluates or paths:
        fail(f"the registry reaches top-level knowledge, an LLM client or dynamic evaluation: "
             f"{reaches + evaluates + paths}")
    controls["no uncontrolled knowledge dependency, LLM client or evaluation in the registry"] = True
    return {"classification": "negative_control", "controls_rejected": len(controls), "controls": sorted(controls)}


# ------------------------------------------------------------------ H4 provenance graph (ADR-0122, WP-E6)

class _GraphWorld:
    """A store over one synthetic subject and a derived subject of it, with registry rules recorded, and a set of
    items that between them reach every node kind, ordered inputs, derivation and recomputation links, incomplete
    lineage and a parent chart."""

    def __init__(self, path):
        self.store = EvidenceStore(path)
        subjects = _synthetic_subjects()
        self.owner = self.store.entities.persist(subjects[0])
        self.label = self.store.entities.load(self.owner).charts[0].label
        annual = dataclasses.replace(subjects[0].charts[0], label="annual")
        self.derived = self.store.entities.persist(_derived(subjects, self.owner, self.label, (annual,)))
        registry = rule_registry.pinned()
        self.rules = {ProducingSystem.PARASHARI: self.store.register_rule(registry.rule_version(
                          registry.by_key(PARASHARI_KEY), 1, "base")),
                      ProducingSystem.KP: self.store.register_rule(registry.rule_version(
                          registry.by_key(KP_KEY), 1, "base"))}
        self.world = _EvidenceWorld(self.owner, self.label, self.rules)

    def populate(self) -> list:
        store, world = self.store, self.world
        ids = [store.persist(world.item(facts=("Sun longitude", "Moon longitude", "Mars longitude")))]
        ids.append(store.persist(world.item(ProducingSystem.KP, facts=("Moon longitude",))))
        ids.append(store.persist(world.item(facts=("Jupiter longitude",), derived_from=(ids[0], ids[1]))))
        ids.append(store.persist(world.item(facts=("Moon longitude",), recomputes=ids[0], derived_from=(ids[2],))))
        ids.append(store.persist(world.item(lineage=world.lineage(("Venus longitude",), inputs_complete=False,
                                                                  derivations_complete=False))))
        ids.append(store.persist(world.item(entity=self.derived, chart=ChartReference(1, "annual"))))
        return ids


def expected_graph(store: EvidenceStore, evidence_id: EvidenceId) -> provenance_graph.Graph:
    """What persist must have recorded for one item, rebuilt by this runner from the store's records: a check of the
    recording, never a recording path (ADR-0122 D2)."""

    item = store.load(evidence_id)
    _number, subject, _reason = store.entities.history(item.entity)[item.chart.entity_revision - 1]
    candidate = [chart for chart in subject.charts if chart.label == item.chart.chart_label][0]
    links = item.derived_from + (() if item.recomputes is None else (item.recomputes,))
    return provenance_graph.record_graph(evidence_id, item, candidate, subject.parent, store.rule_version(item.rule),
                                         {link: store.load(link) for link in links})


def recorded_ancestry(store: EvidenceStore, evidence_id: EvidenceId) -> set:
    """The item and every item its recorded derivation and recomputation links reach."""

    seen, pending = {evidence_id}, [evidence_id]
    while pending:
        item = store.load(pending.pop())
        for link in item.derived_from + (() if item.recomputes is None else (item.recomputes,)):
            if link not in seen:
                seen.add(link)
                pending.append(link)
    return seen


def edge_keys(edges) -> set:
    return {(edge.source.key, edge.kind, edge.target.key, edge.position) for edge in edges}


def graph_reproduces(recorded: provenance_graph.Graph, evidence_id: EvidenceId, item: EvidenceItem,
                     rebuild=provenance_graph.reproduce) -> bool:
    """Gate R's reproduction comparator: the graph alone gives back exactly the item's recorded fields (AC7)."""

    try:
        return rebuild(recorded, evidence_id) == provenance_graph.recorded_fields(item)
    except provenance_graph.GraphError:
        return False


def graph_accounts_for(recorded: provenance_graph.Graph, expected: list, keys=edge_keys) -> bool:
    """Gate R's agreement comparator: the recorded graph is exactly the union of what the items' records give."""

    nodes = {node.key for graph in expected for node in graph.nodes}
    edges = set().union(*(keys(graph.edges) for graph in expected))
    return {node.key for node in recorded.nodes} == nodes and keys(recorded.edges) == edges


def node_round_trips(node: provenance_graph.Node, serialize=provenance_graph.node_to_row) -> bool:
    """Gate P's round-trip comparator: a stored node row rebuilds exactly the node."""

    try:
        return provenance_graph.node_from_row(*serialize(node)) == node
    except provenance_graph.GraphError:
        return False


def gate_p_graph_integrity():
    """The provenance graph recorded at evidence-creation time: every node kind, content-addressed identity that
    shares exactly what agrees and separates every provenance field, the parent chart, the registry's rule version,
    acyclicity, a recomputation leaving the original untouched, round trips and durability (ADR-0122 AC1, AC2, AC5,
    AC8 to AC10). Each comparator rejects a planted violation, wrong by construction."""

    controls = {}
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "evidence.sqlite"
        setting = _GraphWorld(path)
        store: EvidenceStore = setting.store
        first = store.persist(setting.world.item())
        before = store.item_graph(first)
        ids = [first] + setting.populate()
        recorded = store.recorded_graph()
        if {node.kind for node in recorded.nodes} != set(provenance_graph.NodeKind):
            fail("not every node kind was recorded")
        for evidence_id in ids:
            upstream = recorded_ancestry(store, evidence_id)
            if {node.key for node in store.item_graph(evidence_id).nodes} != \
                    {node.key for member in upstream for node in expected_graph(store, member).nodes}:
                fail(f"{evidence_id}'s recorded graph is not what its own and its ancestors' records give")
        inputs = [node for node in recorded.nodes if node.kind is provenance_graph.NodeKind.INPUT]
        rows = store._db.execute("SELECT COUNT(*) FROM graph_nodes WHERE kind = 'input'").fetchone()[0]
        if len(inputs) != 2 or rows != 2:
            fail("the owner's and the derived subject's origins were not each recorded once")
        moon = [node for node in recorded.nodes if node.kind is provenance_graph.NodeKind.ASTRONOMICAL and
                node.fields()["fact"] == "Moon longitude" and node.fields()["chart_label"] == setting.label]
        if len(moon) != 1:
            fail("one fact, on one chart under one provenance, was not recorded as one shared node")
        item = setting.world.item()
        base = provenance_graph.astronomical_node(item.entity, item.chart, item.lineage.inputs[0])
        for name in provenance_graph.PROVENANCE_FIELDS:
            value = CALC.__getattribute__(name)
            other = dataclasses.replace(CALC, **{name: value + 1 if isinstance(value, int) else f"{value}-other"})
            if provenance_graph.astronomical_node(item.entity, item.chart, CalculatedInput(
                    fact=item.lineage.inputs[0].fact, provenance=other)).key == base.key:
                fail(f"facts differing in calculation provenance field {name} were unified")
        parent = provenance_graph.parent_chart_node(store.entities.load(setting.derived).parent)
        child = provenance_graph.chart_node(setting.derived, ChartReference(1, "annual"), "D1")
        if (parent.key, provenance_graph.EdgeKind.DERIVES_FROM, child.key) not in \
                {(edge.source.key, edge.kind, edge.target.key) for edge in recorded.edges}:
            fail("the derived subject's chart does not derive from its parent chart")
        registry = rule_registry.pinned()
        for node in recorded.nodes:
            if node.kind is provenance_graph.NodeKind.RULE:
                identity = node.fields()
                published = registry.rule_version(RuleId(identity["rule"]), identity["version"], identity["variant"])
                if (identity["content_hash"], identity["knowledge_snapshot_hash"]) != \
                        (published.spec.content_hash, registry.snapshot_sha256):
                    fail("a rule node is not the pinned registry's published rule version")
        if store.item_graph(first) != before:
            fail("later items, a recomputation among them, changed an earlier item's recorded graph")
        for node in recorded.nodes:
            if not node_round_trips(node):
                fail("a node did not round-trip through storage")

        def lossy(node):
            key, kind, payload = provenance_graph.node_to_row(node)
            data = json.loads(payload)
            data["identity"].pop(sorted(data["identity"])[0])
            return key, kind, json.dumps(data)

        if node_round_trips(moon[0], lossy):
            fail("the round-trip comparator accepted a serializer that drops an identity field")
        controls["a serializer dropping an identity field rejected"] = True
        first_fact, second_fact = (provenance_graph.astronomical_node(item.entity, item.chart, CalculatedInput(
            fact=fact, provenance=CALC)) for fact in ("Sun longitude", "Moon longitude"))
        kind_only = lambda node: hashlib.sha256(node.kind.value.encode("ascii")).hexdigest()
        if first_fact.key == second_fact.key or kind_only(first_fact) != kind_only(second_fact):
            fail("a key ignoring identity was not distinguishable from the content address")
        controls["a node key ignoring identity rejected"] = True
        counts = (len(recorded.nodes), len(recorded.edges))
        store.close()
        reopened = EvidenceStore(path)
        durable = reopened.recorded_graph() == recorded and reopened.evidence_ids() == ids
        reopened.close()
        if not durable:
            fail("the recorded graph is not durable")
    return {"classification": "structural_integrity", "items_recorded": len(ids), "node_kinds": len(
        provenance_graph.NodeKind), "nodes_recorded": counts[0], "edges_recorded": counts[1],
            "provenance_fields_separated": len(provenance_graph.PROVENANCE_FIELDS), "mismatches": 0,
            "controls_rejected": len(controls), "controls": sorted(controls)}


#: Structurally valid edges between real nodes that no item's records justify: (source, kind, target, position).
FALSE_ANCESTRY = (("other input", "derives_from", "natal chart", 0), ("other input", "derives_from", "natal fact", 0),
                  ("other chart", "derives_from", "natal chart", 0), ("other timing", "derives_from", "first item", 0),
                  ("other fact", "applies_to", "first item", 1), ("second item", "derives_from", "first item", 0))


def _two_chart_items(setting: _GraphWorld) -> tuple:
    """Two items on distinct charts of one synthetic entity, and the real nodes their records justify."""

    store: EvidenceStore = setting.store
    natal_chart, other_chart = store.entities.load(setting.owner).charts[:2]
    here, there = ChartReference(1, natal_chart.label), ChartReference(1, other_chart.label)
    first_id = store.persist(setting.world.item(chart=here))
    second_id = store.persist(setting.world.item(chart=there))
    first, second = store.load(first_id), store.load(second_id)
    owner = setting.owner
    return first_id, second_id, {
        "other input": provenance_graph.input_node(owner, there, other_chart),
        "natal chart": provenance_graph.chart_node(owner, here, "D1"),
        "other chart": provenance_graph.chart_node(owner, there, "D1"),
        "natal fact": provenance_graph.astronomical_node(owner, here, first.lineage.inputs[0]),
        "other fact": provenance_graph.astronomical_node(owner, there, second.lineage.inputs[0]),
        "other timing": provenance_graph.timing_node(owner, there, second.timing),
        "first item": provenance_graph.evidence_node(first_id, first),
        "second item": provenance_graph.evidence_node(second_id, second)}


def _plant_edge(store: EvidenceStore, nodes: dict, source: str, kind: str, target: str, position: int) -> None:
    store._db.execute("INSERT INTO graph_edges (source_key, kind, target_key, position) VALUES (?, ?, ?, ?)",
                      (nodes[source].key, kind, nodes[target].key, position))


def gate_q_graph_refusals():
    """Each refusal WP-E6 requires, triggered for real, with its reason checked: undeclared and correlated edges,
    disallowed pairs, dangling edges, cycles, malformed or forged nodes, rows planted by direct SQL, a graph that
    cannot be written, records the item does not name, and UPDATE or DELETE on the graph tables (ADR-0122 AC1 to
    AC5, AC10)."""

    refused = {}

    def refuses(label, action, errors=(provenance_graph.GraphError, StoreError, sqlite3.DatabaseError), reason=""):
        try:
            action()
        except errors as exc:
            if reason not in str(exc):
                fail(f"{label} was refused for another reason: {exc}")
            refused[label] = True
            return
        fail(f"not refused: {label}")

    with tempfile.TemporaryDirectory() as folder:
        setting = _GraphWorld(Path(folder) / "evidence.sqlite")
        store: EvidenceStore = setting.store
        world = setting.world
        item = world.item()
        candidate = store.entities.load(setting.owner).charts[0]
        kinds = provenance_graph.NodeKind
        origin = provenance_graph.input_node(item.entity, item.chart, candidate)
        chart = provenance_graph.chart_node(item.entity, item.chart, "D1")
        fact = provenance_graph.astronomical_node(item.entity, item.chart, item.lineage.inputs[0])
        timing = provenance_graph.timing_node(item.entity, item.chart, item.timing)
        rule = provenance_graph.rule_node(setting.rules[ProducingSystem.PARASHARI])
        one, two = (provenance_graph.evidence_node(EvidenceId.from_number(n), item) for n in (1, 2))
        derives, applies = provenance_graph.EdgeKind.DERIVES_FROM, provenance_graph.EdgeKind.APPLIES_TO
        Edge = provenance_graph.Edge
        for label, kind in (("a CORRELATED_WITH edge", "correlated_with"), ("an edge kind given as text", "derives_from"),
                            ("an undeclared edge kind", None)):
            refuses(label, lambda kind=kind: Edge(source=origin, kind=kind, target=chart), reason="undeclared edge kind")
        refuses("a CORRELATED_WITH edge read from a row", lambda: provenance_graph.edge_from_row(
            {origin.key: origin, chart.key: chart}, origin.key, "correlated_with", chart.key, 0),
            reason="undeclared edge kind")
        for label, source, kind, target in (
                ("an evidence node deriving an input", one, derives, origin),
                ("a rule deriving evidence", rule, derives, one),
                ("an input applied to evidence", origin, applies, one),
                ("a timing context deriving a chart", timing, derives, chart),
                ("a fact deriving a fact", fact, derives, fact),
                ("a chart applied to a fact", chart, applies, fact)):
            refuses(label, lambda source=source, kind=kind, target=target: Edge(source=source, kind=kind,
                                                                               target=target),
                    reason="not a declared pair")
        refuses("a self-loop", lambda: Edge(source=one, kind=derives, target=one), reason="cycle")
        refuses("a negative position", lambda: Edge(source=origin, kind=derives, target=chart, position=-1),
                reason="position")
        refuses("a dangling edge in a graph", lambda: provenance_graph.Graph(
            nodes=(chart,), edges=(Edge(source=origin, kind=derives, target=chart),)), reason="dangling")
        refuses("a dangling edge read from a row", lambda: provenance_graph.edge_from_row(
            {chart.key: chart}, origin.key, "derives_from", chart.key, 0), reason="dangling")
        refuses("a cycle in a graph", lambda: provenance_graph.Graph(nodes=(one, two), edges=(
            Edge(source=one, kind=derives, target=two), Edge(source=two, kind=derives, target=one))),
                reason="not acyclic")
        refuses("a node of an undeclared kind", lambda: provenance_graph.Node(kind="input", identity=origin.identity),
                reason="undeclared node kind")
        refuses("a node missing an identity field", lambda: provenance_graph.make_node(kinds.RULE, rule=RuleId.from_number(1).value),
                reason="exactly its identity fields")
        refuses("a node with an extra identity field", lambda: provenance_graph.make_node(
            kinds.EVIDENCE, **{**one.fields(), "score": 1}), reason="exactly its identity fields")
        refuses("a node whose identity is not canonical", lambda: provenance_graph.Node(
            kind=kinds.RULE, identity=json.dumps(rule.fields(), indent=1)), reason="canonical")
        refuses("a structured value in a node identity", lambda: provenance_graph.make_node(
            kinds.EVIDENCE, **{**one.fields(), "recomputes": [EvidenceId.from_number(1).value]}), reason="plain value")
        refuses("a fact without its full provenance", lambda: provenance_graph.make_node(
            kinds.ASTRONOMICAL, **{**fact.fields(), "provenance": {"profile_name": "parashari_lahiri"}}),
                reason="every field of its calculation Provenance")
        refuses("a chart with a revision but no varga", lambda: provenance_graph.make_node(
            kinds.DERIVED_CHART, **{**chart.fields(), "varga": None}), reason="parent chart")
        refuses("a stored node under another kind", lambda: provenance_graph.node_from_row(
            origin.key, "timing", provenance_graph.node_to_row(origin)[2]), reason="not a node record")
        refuses("a stored node of another schema", lambda: provenance_graph.node_from_row(
            origin.key, "input", json.dumps({"schema": "v0", "kind": "input", "identity": origin.fields()})),
                reason="not a node record")
        refuses("a stored node whose key is not its hash", lambda: provenance_graph.node_from_row(
            "e" * 64, "input", provenance_graph.node_to_row(origin)[2]), reason="not the hash of its identity")
        refuses("a chart the item does not name", lambda: provenance_graph.record_graph(
            EvidenceId.from_number(1), item, dataclasses.replace(candidate, label="other"), None,
            setting.rules[ProducingSystem.PARASHARI], {}), reason="not the ones the item names")
        refuses("a rule the item does not name", lambda: provenance_graph.record_graph(
            EvidenceId.from_number(1), item, candidate, None, setting.rules[ProducingSystem.KP], {}),
                reason="not the ones the item names")
        refuses("linked items the item does not name", lambda: provenance_graph.record_graph(
            EvidenceId.from_number(1), item, candidate, None, setting.rules[ProducingSystem.PARASHARI],
            {EvidenceId.from_number(LAST_TEST): item}), reason="exactly the ones the item names")
        refuses("a graph read of no items", lambda: store.graph(()), reason="one or more distinct")
        refuses("a graph read naming an item twice", lambda: store.graph((EvidenceId.from_number(1),) * 2),
                reason="one or more distinct")
        # A graph that cannot be written persists nothing and takes no number (AC1).
        store._db.execute("INSERT INTO graph_nodes (node_key, kind, payload) VALUES (?, ?, ?)",
                          (timing.key, "timing", json.dumps({"schema": provenance_graph.GRAPH_SCHEMA,
                                                             "kind": "timing", "identity": {"planted": True}})))
        refuses("a persist whose graph meets a forged node", lambda: store.persist(item),
                reason="recorded node is refused")
        if store.issued_count("EVD") != 0 or store.evidence_ids() != []:
            fail("a refused graph write took an EVD number or left an item")
        store.close()
    with tempfile.TemporaryDirectory() as folder:
        setting = _GraphWorld(Path(folder) / "evidence.sqlite")
        store: EvidenceStore = setting.store
        world = setting.world
        item = world.item(facts=("Mercury longitude",))
        candidate = store.entities.load(setting.owner).charts[0]
        origin = provenance_graph.input_node(item.entity, item.chart, candidate)
        fact = provenance_graph.astronomical_node(item.entity, item.chart, item.lineage.inputs[0])
        for node in (origin, fact):
            store._db.execute("INSERT INTO graph_nodes (node_key, kind, payload) VALUES (?, ?, ?)",
                              provenance_graph.node_to_row(node))
        store._db.execute("INSERT INTO graph_edges (source_key, kind, target_key, position) VALUES (?, ?, ?, 0)",
                          (fact.key, "derives_from", origin.key))
        refuses("an edge that would close a cycle on write", lambda: store.persist(item), reason="would close a cycle")
        if store.issued_count("EVD") != 0:
            fail("a write refused for a cycle took an EVD number")
        store.close()
    with tempfile.TemporaryDirectory() as folder:
        setting = _GraphWorld(Path(folder) / "evidence.sqlite")
        store: EvidenceStore = setting.store
        world = setting.world
        first = store.persist(world.item())
        second = store.persist(world.item(derived_from=(first,)))
        for statement in ("UPDATE graph_nodes SET payload = 'x'", "DELETE FROM graph_nodes",
                          "UPDATE graph_edges SET position = 9", "DELETE FROM graph_edges"):
            refuses(f"direct SQL: {statement}", lambda statement=statement: store._db.execute(statement),
                    reason="append-only")
        keys = [provenance_graph.evidence_node(evidence_id, store.load(evidence_id)).key for evidence_id in
                (first, second)]
        store._db.execute("INSERT INTO graph_edges (source_key, kind, target_key, position) VALUES (?, ?, ?, 0)",
                          ("f" * 64, "derives_from", keys[0]))
        refuses("a dangling edge planted by direct SQL, read", lambda: store.item_graph(first), reason="dangling")
        refuses("a dangling edge planted by direct SQL, read whole", lambda: store.recorded_graph(),
                reason="dangling")
        store.close()
    with tempfile.TemporaryDirectory() as folder:
        setting = _GraphWorld(Path(folder) / "evidence.sqlite")
        store: EvidenceStore = setting.store
        world = setting.world
        first = store.persist(world.item())
        second = store.persist(world.item(derived_from=(first,)))
        keys = [provenance_graph.evidence_node(evidence_id, store.load(evidence_id)).key for evidence_id in
                (first, second)]
        store._db.execute("INSERT INTO graph_edges (source_key, kind, target_key, position) VALUES (?, ?, ?, 0)",
                          (keys[1], "derives_from", keys[0]))
        refuses("a cycle planted by direct SQL, read", lambda: store.item_graph(second), reason="not acyclic")
        refuses("a cycle planted by direct SQL, read whole", lambda: store.recorded_graph(), reason="not acyclic")
        refuses("an incident read across a planted cycle", lambda: store.incident(keys[0]), reason="not acyclic")
        store.close()
    # CEO HOLD on PR #59: a structurally valid, acyclic row no item's records justify is refused by every real read.
    for source, kind, target, position in FALSE_ANCESTRY:
        with tempfile.TemporaryDirectory() as folder:
            setting = _GraphWorld(Path(folder) / "evidence.sqlite")
            store: EvidenceStore = setting.store
            first, _second, nodes = _two_chart_items(setting)
            store.item_graph(first)
            _plant_edge(store, nodes, source, kind, target, position)
            for read, action in (("item_graph", lambda: store.item_graph(first)),
                                 ("graph", lambda: store.graph((first,))),
                                 ("recorded_graph", lambda: store.recorded_graph()),
                                 ("incident", lambda: store.incident(nodes[target].key)),
                                 ("reproduce", lambda: store.reproduce(first))):
                refuses(f"{read} of an unaccounted edge from {source} to {target}", action,
                        reason="do not account for it")
            store.close()
    return {"classification": "negative_control", "refusals_verified": len(refused), "refused": sorted(refused)}


def gate_r_graph_agreement():
    """The graph's agreement with the evidence: from its graph alone each item's inputs, chart, varga, timing, rule
    and links are reproduced exactly; completeness statements sit on its node; the recorded graph is exactly what the
    items' records give; incident reads agree with it (ADR-0122 AC6, AC7, AC11). Each comparator rejects planted
    violations, and a deliberately broken comparator is distinguishable from the real one."""

    controls = {}
    with tempfile.TemporaryDirectory() as folder:
        setting = _GraphWorld(Path(folder) / "evidence.sqlite")
        store: EvidenceStore = setting.store
        ids = setting.populate()
        for evidence_id in ids:
            item = store.load(evidence_id)
            if not graph_reproduces(store.item_graph(evidence_id), evidence_id, item) or \
                    store.reproduce(evidence_id) != provenance_graph.recorded_fields(item):
                fail(f"{evidence_id} is not reproduced exactly from its recorded graph")
            node = provenance_graph.evidence_node(evidence_id, item).fields()
            if (node["inputs_complete"], node["derivations_complete"]) != (item.lineage.inputs_complete,
                                                                          item.lineage.derivations_complete):
                fail("an item's completeness statements are not on its evidence node")
        recorded = store.recorded_graph()
        expected = [expected_graph(store, evidence_id) for evidence_id in ids]
        if not graph_accounts_for(recorded, expected) or store.graph(ids) != recorded:
            fail("the recorded graph is not exactly what the items' records give")
        for node in recorded.nodes:
            incoming, outgoing = store.incident(node.key)
            if edge_keys(incoming) != edge_keys(edge for edge in recorded.edges if edge.target.key == node.key) or \
                    edge_keys(outgoing) != edge_keys(edge for edge in recorded.edges if edge.source.key == node.key):
                fail("an incident read disagrees with the recorded graph")
        # Negative controls, invalid by construction: each planted graph loses or bends exactly one recorded fact.
        first, linked, recomputed = ids[0], ids[2], ids[3]
        for label, evidence_id, drop in (
                ("a graph losing one input", first, lambda edge: edge.source.kind is
                 provenance_graph.NodeKind.ASTRONOMICAL and edge.position == 2),
                ("a graph losing a derivation link", linked, lambda edge: edge.source.kind is
                 provenance_graph.NodeKind.EVIDENCE and edge.position == 1),
                ("a graph losing the recomputation link", recomputed, lambda edge: edge.source.kind is
                 provenance_graph.NodeKind.EVIDENCE and edge.source.fields()["evidence"] == first.value),
                ("a graph losing its rule", first, lambda edge: edge.source.kind is provenance_graph.NodeKind.RULE)):
            full = store.item_graph(evidence_id)
            target = provenance_graph.evidence_node(evidence_id, store.load(evidence_id)).key
            planted = provenance_graph.Graph(nodes=full.nodes, edges=tuple(
                edge for edge in full.edges if not (edge.target.key == target and drop(edge))))
            if len(planted.edges) != len(full.edges) - 1 or graph_reproduces(planted, evidence_id,
                                                                             store.load(evidence_id)):
                fail(f"the reproduction comparator accepted {label}")
            controls[f"{label} rejected"] = True
        full = store.item_graph(first)
        swapped = provenance_graph.Graph(nodes=full.nodes, edges=tuple(
            dataclasses.replace(edge, position={0: 1, 1: 0}[edge.position])
            if edge.source.kind is provenance_graph.NodeKind.ASTRONOMICAL and edge.position in (0, 1) else edge
            for edge in full.edges))
        if graph_reproduces(swapped, first, store.load(first)):
            fail("the reproduction comparator accepted inputs out of their recorded order")
        controls["inputs out of their recorded order rejected"] = True
        itself = lambda graph, evidence_id: provenance_graph.recorded_fields(store.load(evidence_id))
        lossy = provenance_graph.Graph(nodes=full.nodes, edges=tuple(
            edge for edge in full.edges if edge.source.kind is not provenance_graph.NodeKind.TIMING))
        if graph_reproduces(lossy, first, store.load(first)) or not graph_reproduces(lossy, first, store.load(first),
                                                                                     itself):
            fail("a reproduction comparator reading the item instead of the graph was not distinguishable")
        controls["a reproduction comparator reading the item, not the graph, rejected"] = True
        extra_edge = provenance_graph.Edge(
            source=[node for node in recorded.nodes if node.kind is provenance_graph.NodeKind.TIMING and
                    node.fields()["chart_label"] == "annual"][0],
            kind=provenance_graph.EdgeKind.DERIVES_FROM,
            target=provenance_graph.evidence_node(ids[1], store.load(ids[1])), position=0)
        if edge_keys([extra_edge]) <= edge_keys(recorded.edges):
            fail("the planted extra edge is already recorded, so it tests nothing")
        padded = provenance_graph.Graph(nodes=recorded.nodes, edges=recorded.edges + (extra_edge,))
        nodes_only = lambda edges: set()
        if graph_accounts_for(padded, expected) or not graph_accounts_for(padded, expected, nodes_only):
            fail("an agreement comparator ignoring edges was not distinguishable from the real one")
        controls["an edge the records do not account for rejected"] = True
        controls["an agreement comparator ignoring edges rejected"] = True
        unexpected = provenance_graph.make_node(provenance_graph.NodeKind.TIMING, **{
            **[node for node in recorded.nodes if node.kind is provenance_graph.NodeKind.TIMING][0].fields(),
            "label": "planted"})
        if graph_accounts_for(provenance_graph.Graph(nodes=recorded.nodes + (unexpected,), edges=recorded.edges),
                              expected):
            fail("the agreement comparator accepted a node the records do not account for")
        controls["a node the records do not account for rejected"] = True
        # The comparator every persisted read uses (CEO HOLD on PR #59), against planted graphs.
        moved = next(edge for edge in recorded.edges if edge.position == 0)
        if provenance_graph.unjustified_rows(recorded, expected) != ():
            fail("the read comparator rejected a graph the items' records justify")
        for label, planted, reason in (
                ("an edge no record justifies", padded, "unaccounted edge"),
                ("a node no record justifies", provenance_graph.Graph(nodes=recorded.nodes + (unexpected,),
                                                                      edges=recorded.edges), "unaccounted node"),
                ("every recorded node gone missing", provenance_graph.Graph(nodes=(), edges=()), "missing node"),
                ("a recorded edge gone missing", provenance_graph.Graph(nodes=recorded.nodes, edges=recorded.edges[1:]),
                 "missing edge"),
                ("an edge at another position", provenance_graph.Graph(nodes=recorded.nodes, edges=tuple(
                    dataclasses.replace(edge, position=9) if edge is moved else edge for edge in recorded.edges)),
                 "unaccounted edge")):
            if not any(reason in row for row in provenance_graph.unjustified_rows(planted, expected)):
                fail(f"the read comparator accepted {label}")
            controls[f"the read comparator rejects {label}"] = True
        store.close()
    # The real read path: the planted false ancestry is refused, and each deliberately weakened comparator, put in the
    # real comparator's place, lets the same read accept it. The refusal is therefore the comparator's doing.
    with tempfile.TemporaryDirectory() as folder:
        setting = _GraphWorld(Path(folder) / "evidence.sqlite")
        store: EvidenceStore = setting.store
        first, _second, nodes = _two_chart_items(setting)
        _plant_edge(store, nodes, "other input", "derives_from", "natal chart", 0)
        false_edge = (nodes["other input"].key, nodes["natal chart"].key)

        def direct_edges_only(recorded_rows, justified):
            direct = lambda edges: {(edge.source.key, edge.kind, edge.target.key, edge.position) for edge in edges
                                    if edge.target.kind is provenance_graph.NodeKind.EVIDENCE}
            return tuple(direct(recorded_rows.edges) ^ direct(edge for each in justified for edge in each.edges))

        def missing_rows_only(recorded_rows, justified):
            return tuple(row for row in provenance_graph.unjustified_rows(recorded_rows, justified)
                         if row.startswith("missing"))

        for label, weak in (("checking only edges into evidence nodes", direct_edges_only),
                            ("reporting only missing rows", missing_rows_only)):
            try:
                store.item_graph(first)
                fail("the real read accepted an edge no item's records justify")
            except StoreError as exc:
                if "do not account for it" not in str(exc):
                    fail(f"the real read refused the planted edge for another reason: {exc}")
            store._unjustified = weak
            accepted = store.item_graph(first)
            del store._unjustified
            if false_edge not in {(edge.source.key, edge.target.key) for edge in accepted.edges}:
                fail(f"a comparator {label} was not distinguishable from the real one on the real read path")
            controls[f"a read comparator {label} rejected"] = True
        store.close()
    return {"classification": "structural_integrity", "items_reproduced": len(ids), "mismatches": 0,
            "controls_rejected": len(controls), "controls": sorted(controls)}


# ------------------------------------------------------------------ evidence read integrity (ADR-0124, finding F1)

FORGED_ID, FORGED_PARENT_ID = EvidenceId.from_number(500), EvidenceId.from_number(499)


class _Forgery:
    """Writes rows straight into the tables, around persist(), as a forger with database access would."""

    def __init__(self, setting: _GraphWorld):
        self.setting, self.store, self.world = setting, setting.store, setting.world
        self.parashari, self.kp = setting.rules[ProducingSystem.PARASHARI], setting.rules[ProducingSystem.KP]
        self.candidate = setting.store.entities.load(setting.owner).charts[0]
        self.unissued = RuleId.from_number(LAST_TEST // 1000)
        self.good = setting.store.persist(setting.world.item())

    def row(self, item, evidence_id=FORGED_ID, payload_id=None, entity=None, recomputes=None) -> None:
        recorded = None if item.recomputes is None else item.recomputes.value
        self.store._db.execute(
            "INSERT INTO evidence_items (evidence_id, entity_id, recomputes, payload) VALUES (?, ?, ?, ?)",
            (evidence_id.value, entity or item.entity.value, recorded if recomputes is None else recomputes,
             json.dumps(item_to_record(payload_id or evidence_id, item))))

    def graph(self, item, rule, evidence_id=FORGED_ID, linked=None) -> None:
        built = provenance_graph.record_graph(evidence_id, item, self.candidate, None, rule, linked or {})
        for node in built.nodes:
            self.store._db.execute("INSERT OR IGNORE INTO graph_nodes (node_key, kind, payload) VALUES (?, ?, ?)",
                                   provenance_graph.node_to_row(node))
        for edge in built.edges:
            self.store._db.execute("INSERT OR IGNORE INTO graph_edges (source_key, kind, target_key, position) "
                                   "VALUES (?, ?, ?, ?)", (edge.source.key, edge.kind.value, edge.target.key,
                                                           edge.position))

    def reference(self, rule=None, variant="base"):
        return RuleReference(rule=rule or self.unissued, version=1, variant=variant)

    def unregistered(self, evidence_id=FORGED_ID):
        rule = dataclasses.replace(self.parashari, rule=self.unissued)
        item = self.world.item(rule=self.reference())
        self.row(item, evidence_id)
        self.graph(item, rule, evidence_id)
        return item


def _forge_unregistered_no_graph(forgery: _Forgery) -> str:
    forgery.row(forgery.world.item(rule=forgery.reference()))
    return "missing graph"


def _forge_unregistered_with_graph(forgery: _Forgery) -> str:
    forgery.unregistered()
    return "is not registered"


def _forge_registered_no_graph(forgery: _Forgery) -> str:
    forgery.row(forgery.world.item(facts=("Saturn longitude",)))
    return "missing graph"


def _forge_other_school(forgery: _Forgery) -> str:
    kp = forgery.kp
    item = forgery.world.item(rule=RuleReference(rule=kp.rule, version=kp.version, variant=kp.spec.variant),
                              declared_strength=kp.spec.declared_strength)
    forgery.row(item)
    forgery.graph(item, kp)
    return "systems stay isolated"


def _forge_other_strength(forgery: _Forgery) -> str:
    item = forgery.world.item(declared_strength="planted")
    forgery.row(item)
    forgery.graph(item, forgery.parashari)
    return "declared strength"


def _forge_unpublished_variant(forgery: _Forgery) -> str:
    base = forgery.parashari
    rule = dataclasses.replace(base, spec=dataclasses.replace(base.spec, variant="forged"))
    forgery.store._db.execute("INSERT INTO registered_rule_versions (rule_id, version, variant, payload) VALUES "
                              "(?, ?, ?, ?)", (rule.rule.value, 1, "forged", json.dumps(rule_to_record(rule))))
    item = forgery.world.item(rule=forgery.reference(rule.rule, "forged"))
    forgery.row(item)
    forgery.graph(item, rule)
    return "not published by the pinned registry"


def _forge_payload_of_another_item(forgery: _Forgery) -> str:
    forgery.row(forgery.world.item(), payload_id=forgery.good)
    return "does not match its row"


def _forge_entity_column(forgery: _Forgery) -> str:
    item = forgery.world.item(facts=("Venus longitude",))
    forgery.row(item, entity=forgery.setting.derived.value)
    forgery.graph(item, forgery.parashari)
    return "does not match its row"


def _forge_recomputes_column(forgery: _Forgery) -> str:
    item = forgery.world.item(facts=("Venus longitude",))
    forgery.row(item, recomputes=forgery.good.value)
    forgery.graph(item, forgery.parashari)
    return "does not match its row"


def _forge_ancestor(forgery: _Forgery) -> str:
    parent = forgery.unregistered(FORGED_PARENT_ID)
    item = forgery.world.item(facts=("Mercury longitude",), derived_from=(FORGED_PARENT_ID,))
    forgery.row(item)
    forgery.graph(item, forgery.parashari, linked={FORGED_PARENT_ID: parent})
    return "is not registered"


FORGERIES = (("a rule never registered, with no graph", _forge_unregistered_no_graph),
             ("a rule never registered, with a matching forged graph", _forge_unregistered_with_graph),
             ("a registered rule, with no graph", _forge_registered_no_graph),
             ("another school's rule", _forge_other_school),
             ("another declared strength", _forge_other_strength),
             ("an unpublished variant at the pinned snapshot", _forge_unpublished_variant),
             ("a payload naming another item", _forge_payload_of_another_item),
             ("an entity column that disagrees", _forge_entity_column),
             ("a recomputes column that disagrees", _forge_recomputes_column),
             ("a forged ancestor", _forge_ancestor))


def gate_s_evidence_read_integrity():
    """Every evidence read refuses a row written around persist() that breaks the registered-rule or graph-integrity
    requirements, and still serves legitimate records, those under an earlier snapshot included. Each real check is then
    weakened in turn, and the same read accepts the forgery (ADR-0124; H4 s4; ADR-0122 AC5, AC7)."""

    refused, controls, preserved = {}, {}, {}

    def refuses(label, action, reason=""):
        try:
            action()
        except StoreError as exc:
            if reason not in str(exc):
                fail(f"{label} was refused for another reason: {exc}")
            refused[label] = True
            return
        fail(f"not refused: {label}")

    for label, plant in FORGERIES:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as folder:
            setting = _GraphWorld(Path(folder) / "evidence.sqlite")
            store: EvidenceStore = setting.store
            forgery = _Forgery(setting)
            good, reason = forgery.good, plant(forgery)
            refuses(f"load of {label}", lambda: store.load(FORGED_ID), reason)
            for read, action in (("evidence_ids", lambda: store.evidence_ids()),
                                 ("join", lambda: store.join((good, FORGED_ID))),
                                 ("counts", lambda: store.counts()),
                                 ("classify", lambda: store.classify(good, FORGED_ID)),
                                 ("relate", lambda: store.relate(good, FORGED_ID)),
                                 ("item_graph", lambda: store.item_graph(FORGED_ID)),
                                 ("reproduce", lambda: store.reproduce(FORGED_ID)),
                                 ("recorded_graph", lambda: store.recorded_graph())):
                refuses(f"{read} with {label}", action)
            if store.load(good) != setting.world.item() or store.item_graph(good).nodes == ():
                fail(f"{label} took a legitimate item down with it")
            preserved[f"a legitimate item beside {label}"] = True
            store.close()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as folder:
        setting = _GraphWorld(Path(folder) / "evidence.sqlite")
        store: EvidenceStore = setting.store
        forgery = _Forgery(setting)
        forgery.unregistered(FORGED_PARENT_ID)
        refuses("persist naming a forged parent", lambda: store.persist(setting.world.item(
            derived_from=(FORGED_PARENT_ID,))), "is not registered")
        if store.issued_count("EVD") != 1:
            fail("a refused persist took an EVD number")
        forgery.row(setting.world.item(rule=forgery.reference(), recomputes=forgery.good))
        refuses("recomputations listing a forged recomputation", lambda: store.recomputations(forgery.good))
        record = relationship_to_record(Relationship(forgery.good, FORGED_ID, DependencyClass.UNKNOWN, False, "planted"))
        store._db.execute("INSERT INTO evidence_relationships (first_id, second_id, payload) VALUES (?, ?, ?)",
                          (forgery.good.value, FORGED_ID.value, json.dumps(record)))
        refuses("relationships naming a forged item", lambda: store.relationships())
        refuses("relationship_counts naming a forged item", lambda: store.relationship_counts())
        store.close()
    # Legitimate records stay readable, those recorded under an earlier snapshot included.
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as folder:
        setting = _GraphWorld(Path(folder) / "evidence.sqlite")
        store: EvidenceStore = setting.store
        ids = setting.populate()
        items = [store.load(evidence_id) for evidence_id in ids]
        store.relate(ids[0], ids[1])
        if store.evidence_ids() != ids or store.join(ids) != items or store.recomputations(ids[0]) != [ids[3]] or \
                len(store.relationships()) != 1 or set(store.counts()["total"]) != set(ids):
            fail("a legitimate record was not served by every read")
        preserved["legitimate items through every read"] = True
        in_force = rule_registry.pinned
        later = rule_registry.RuleRegistry(in_force().rules(), "0" * 64)
        rule_registry.pinned = lambda: later
        try:
            if [store.load(evidence_id) for evidence_id in ids] != items or store.evidence_ids() != ids or \
                    not store.recorded_graph().nodes:
                fail("evidence recorded under an earlier snapshot is no longer readable")
            preserved["evidence recorded under an earlier snapshot"] = True
            refuses("new evidence under an earlier snapshot", lambda: store.persist(setting.world.item()),
                    "another snapshot")

            def too_strict(item):
                rule = store.rule_version(item.rule)
                if rule.spec.knowledge_snapshot_hash != later.snapshot_sha256:
                    raise StoreError("another snapshot")
                return rule

            store._admitted_rule = too_strict
            refuses("a planted check demanding the snapshot in force, on legitimate history",
                    lambda: store.load(ids[0]), "another snapshot")
            del store._admitted_rule
            controls["a read check demanding the snapshot in force rejected: it refuses legitimate history"] = True
        finally:
            rule_registry.pinned = in_force
        store.close()
    # Each real check does the refusing: weakened in turn, the same read accepts the forgery.
    for label, plant, check, weak in (
            ("the registered-rule lookup", _forge_unregistered_with_graph, "_admitted_rule",
             lambda forgery: lambda item: dataclasses.replace(forgery.parashari, rule=forgery.unissued)),
            ("the rule's fit to the item", _forge_other_strength, "_require_fit",
             lambda forgery: lambda item, rule: None),
            ("the exact-publication check", _forge_unpublished_variant, "_require_published",
             lambda forgery: lambda item, rule, registry: None),
            ("the row identity check", _forge_entity_column, "_require_row_identity",
             lambda forgery: lambda *row: None),
            ("the graph check", _forge_registered_no_graph, "graph", lambda forgery: lambda evidence_ids: None)):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as folder:
            setting = _GraphWorld(Path(folder) / "evidence.sqlite")
            store: EvidenceStore = setting.store
            forgery = _Forgery(setting)
            reason = plant(forgery)
            refuses(f"the real read, before weakening {label}", lambda: store.load(FORGED_ID), reason)
            store.__setattr__(check, weak(forgery))
            if store.load(FORGED_ID) is None:
                fail(f"weakening {label} did not change the read")
            controls[f"{label}, weakened, admits the forgery on the real read path"] = True
            store.close()
    return {"classification": "negative_control", "forgeries": len(FORGERIES), "refusals_verified": len(refused),
            "legitimate_reads_preserved": len(preserved), "controls_rejected": len(controls),
            "refused": sorted(refused), "preserved": sorted(preserved), "controls": sorted(controls)}


# ------------------------------------------------------------------ relationship integrity (ADR-0125, finding F2)

RELATIONSHIP_PAIRS = {"derived": DependencyClass.DERIVED, "shared origin": DependencyClass.SHARED_ORIGIN,
                      "independent": DependencyClass.INDEPENDENT,
                      "independent and conflicting": DependencyClass.INDEPENDENT, "unknown": DependencyClass.UNKNOWN}


def _relationship_pairs(setting: _GraphWorld) -> dict:
    """One legitimate pair of synthetic items for each relationship the store can classify."""

    store: EvidenceStore = setting.store
    world = setting.world

    def put(*args, **changes):
        return store.persist(world.item(*args, **changes))

    sun, jupiter, venus = put(facts=("Sun longitude",)), put(facts=("Jupiter longitude",)), put(facts=("Venus longitude",))
    return {"derived": (sun, put(facts=("Mars longitude",), derived_from=(sun,))),
            "shared origin": (jupiter, put(ProducingSystem.KP, facts=("Jupiter longitude",))),
            "independent": (venus, put(ProducingSystem.KP, facts=("Mercury longitude",))),
            "independent and conflicting": (venus, put(ProducingSystem.KP, facts=("Saturn longitude",),
                                                       polarity=Polarity.NEGATIVE)),
            "unknown": (put(facts=("Rahu longitude",)), put(facts=("Ketu longitude",)))}


def _plant_relationship(store: EvidenceStore, first_id: str, second_id: str, payload: str) -> None:
    store._db.execute("INSERT INTO evidence_relationships (first_id, second_id, payload) VALUES (?, ?, ?)",
                      (first_id, second_id, payload))


def _relationship_forgeries(store: EvidenceStore, pairs: dict, other_id, forged_id) -> list:
    """Each forgery as (label, first column, second column, payload, the reason it must be refused for)."""

    def true_record(name):
        return json.loads(json.dumps(relationship_to_record(store.classify(*pairs[name]))))

    out = []
    for name, truth in RELATIONSHIP_PAIRS.items():
        first, second = (value.value for value in pairs[name])
        for kind in DependencyClass:
            if kind is not truth:
                record = true_record(name)
                record["relationship"]["dependency"] = kind.value
                out.append((f"{kind.value} forged on a {name} pair", first, second, json.dumps(record),
                            "measured evidence" if kind is DependencyClass.CORRELATED else
                            "not supported by its source evidence"))
        record = true_record(name)
        record["relationship"]["conflicting"] = not record["relationship"]["conflicting"]
        out.append((f"a forged conflict flag on a {name} pair", first, second, json.dumps(record), "conflict flag"))
        record = true_record(name)
        record["relationship"]["basis"] = "planted explanation"
        out.append((f"a forged explanation on a {name} pair", first, second, json.dumps(record), "basis"))
    first, second = (value.value for value in pairs["derived"])

    def changed(change):
        record = true_record("derived")
        change(record)
        return json.dumps(record)

    out += [
        ("the payload naming the pair in the other order", first, second, changed(lambda r: r["relationship"].update(
            first=second, second=first)), "does not match its row"),
        ("the row's columns naming another item", first, pairs["unknown"][0].value, changed(lambda r: None),
         "does not match its row"),
        ("an item that does not exist", first, other_id.value, changed(lambda r: r["relationship"].update(
            second=other_id.value)), "no such evidence item"),
        ("one item related to itself", first, first, changed(lambda r: r["relationship"].update(second=first)),
         "two different evidence items"),
        ("an item that fails the read checks", first, forged_id.value, changed(lambda r: r["relationship"].update(
            second=forged_id.value)), "missing graph"),
        ("a payload that is not JSON", first, second, "{not json", "is refused"),
        ("another schema", first, second, changed(lambda r: r.update(schema="v0")), "not a relationship record"),
        ("a missing field", first, second, changed(lambda r: r["relationship"].pop("basis")), "only its model fields"),
        ("an extra field", first, second, changed(lambda r: r["relationship"].update(score=1)), "only its model fields"),
        ("an undeclared class", first, second, changed(lambda r: r["relationship"].update(dependency="proven")),
         "is refused"),
        ("a conflict flag that is not boolean", first, second, changed(lambda r: r["relationship"].update(
            conflicting="no")), "conflict is recorded"),
        ("an empty explanation", first, second, changed(lambda r: r["relationship"].update(basis=" ")), "basis"),
    ]
    return out


def gate_t_relationship_integrity():
    """A persisted relationship is returned only if its identities match its row, both items pass the evidence read
    checks, their provenance agrees, and classifying the same immutable items gives exactly the recorded dependency,
    conflict flag and basis. Legitimate relationships, UNKNOWN among them, stay readable. Each real check is then
    weakened in turn, and the same read accepts the forgery (ADR-0125; H4 s10; ADR-0021 D5)."""

    refused, controls, preserved = {}, {}, {}

    def refuses(label, action, reason=""):
        try:
            action()
        except StoreError as exc:
            if reason not in str(exc):
                fail(f"{label} was refused for another reason: {exc}")
            refused[label] = True
            return
        fail(f"not refused: {label}")

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as folder:
        root = Path(folder)
        base = root / "base.sqlite"
        setting = _GraphWorld(base)
        store: EvidenceStore = setting.store
        pairs = _relationship_pairs(setting)
        other_id, forged_id = EvidenceId.from_number(900), EvidenceId.from_number(901)
        unregistered = setting.world.item(rule=RuleReference(rule=RuleId.from_number(LAST_TEST // 1000), version=1,
                                                             variant="base"))
        forgeries = _relationship_forgeries(store, pairs, other_id, forged_id)
        recorded = [store.relate(*pairs[name]) for name in RELATIONSHIP_PAIRS]
        if [item.dependency for item in recorded] != list(RELATIONSHIP_PAIRS.values()) or store.relationships() != recorded:
            fail("a legitimate relationship did not read back as recorded")
        preserved["every legitimate relationship reads back as recorded"] = True
        counts = store.relationship_counts()
        if counts[DependencyClass.UNKNOWN.value] != (pairs["unknown"],) or counts[DependencyClass.INDEPENDENT.value] != (
                pairs["independent"], pairs["independent and conflicting"]) or \
                counts["conflicting"] != (pairs["independent and conflicting"],):
            fail("the relationship counts do not keep UNKNOWN, INDEPENDENT and conflict apart")
        preserved["UNKNOWN stays its own class, never counted as INDEPENDENT"] = True
        store.close()

        def copy_of(name: str) -> Path:
            target = root / f"{name}.sqlite"
            shutil.copyfile(base, target)
            return target

        for index, (label, first_id, second_id, payload, reason) in enumerate(forgeries):
            forged: EvidenceStore = EvidenceStore(copy_of(f"forged{index}"))
            forged._db.execute("INSERT INTO evidence_items (evidence_id, entity_id, recomputes, payload) VALUES "
                               "(?, ?, NULL, ?)", (forged_id.value, unregistered.entity.value,
                                                   json.dumps(item_to_record(forged_id, unregistered))))
            _plant_relationship(forged, first_id, second_id, payload)
            refuses(f"relationships with {label}", lambda: forged.relationships(), reason)
            refuses(f"relationship_counts with {label}", lambda: forged.relationship_counts(), reason)
            forged.close()
        # Legitimate history: appended records, both orders, later evidence, a reopen, and a later snapshot.
        kept: EvidenceStore = EvidenceStore(copy_of("kept"))
        first, second = pairs["shared origin"]
        history = recorded + [kept.relate(first, second), kept.relate(first, second), kept.relate(second, first)]
        if kept.relationships() != history:
            fail("appended relationship history did not read back in order")
        preserved["appended history, both orders of a pair"] = True
        kept.persist(setting.world.item(facts=("Neptune longitude",), derived_from=(pairs["derived"][1],)))
        if kept.relationships() != history:
            fail("later evidence changed what an earlier relationship reads as")
        preserved["a relationship beside later evidence"] = True
        in_force = rule_registry.pinned
        later = rule_registry.RuleRegistry(in_force().rules(), "0" * 64)
        rule_registry.pinned = lambda: later
        try:
            if kept.relationships() != history:
                fail("a relationship under an earlier snapshot is no longer readable")
        finally:
            rule_registry.pinned = in_force
        preserved["a relationship under an earlier snapshot"] = True
        kept.close()
        reopened: EvidenceStore = EvidenceStore(root / "kept.sqlite")
        if reopened.relationships() != history:
            fail("a relationship did not survive a reopen")
        preserved["a relationship after a reopen"] = True
        reopened.close()

        def ignoring(field):
            def compare(mine, supported):
                return tuple(name for name, one, other in (("dependency", mine.dependency, supported.dependency),
                                                           ("conflict flag", mine.conflicting, supported.conflicting),
                                                           ("basis", mine.basis, supported.basis))
                             if one != other and name != field)
            return compare

        # Each real check does the refusing: weakened in turn, the same read accepts the forgery.
        by_label = {label: (first_id, second_id, payload) for label, first_id, second_id, payload, _reason in forgeries}
        for label, forgery, check, weak in (
                ("the dependency comparison", "independent forged on a derived pair", "_unsupported_fields",
                 ignoring("dependency")),
                ("the conflict-flag comparison", "a forged conflict flag on a derived pair", "_unsupported_fields",
                 ignoring("conflict flag")),
                ("the explanation comparison", "a forged explanation on a derived pair", "_unsupported_fields",
                 ignoring("basis")),
                ("the row identity check", "the row's columns naming another item", "_require_relationship_row",
                 lambda *row: None)):
            target: EvidenceStore = EvidenceStore(copy_of(f"weak{len(controls)}"))
            _plant_relationship(target, *by_label[forgery])
            refuses(f"the real read, before weakening {label}", lambda: target.relationships())
            target.__setattr__(check, weak)
            if len(target.relationships()) != len(recorded) + 1:
                fail(f"weakening {label} did not change the read")
            controls[f"{label}, weakened, admits the forgery on the real read path"] = True
            target.close()
        strict: EvidenceStore = EvidenceStore(copy_of("strict"))
        strict.__setattr__("_unsupported_fields", lambda mine, supported: (
            ("dependency",) if mine.dependency is DependencyClass.UNKNOWN else ()))
        refuses("a planted check refusing every UNKNOWN record", lambda: strict.relationships(), "dependency")
        controls["a check refusing legitimate UNKNOWN records rejected"] = True
        strict.close()
        lenient: EvidenceStore = EvidenceStore(copy_of("lenient"))
        _plant_relationship(lenient, *by_label["independent forged on a derived pair"])
        lenient.__setattr__("_unsupported_fields", lambda mine, supported: ())
        if lenient.relationship_counts()[DependencyClass.INDEPENDENT.value].count(pairs["derived"]) != 1:
            fail("a comparator accepting everything was not distinguishable from the real one")
        controls["a comparator accepting everything would report a false INDEPENDENT"] = True
        lenient.close()
    return {"classification": "negative_control", "forgeries": len(forgeries), "refusals_verified": len(refused),
            "legitimate_reads_preserved": len(preserved), "controls_rejected": len(controls),
            "refused": sorted(refused), "preserved": sorted(preserved), "controls": sorted(controls)}


# ------------------------------------------------------------------ historical rule integrity (ADR-0127, limit L1)

EARLIER_SNAPSHOT = "f" * 64


def _earlier(rule: RuleVersion, **spec) -> RuleVersion:
    """A rule version as recorded under an earlier snapshot, with any planted change."""

    return dataclasses.replace(rule, spec=dataclasses.replace(rule.spec, **{"knowledge_snapshot_hash": EARLIER_SNAPSHOT,
                                                                          **spec}))


def _plant_historical(forgery: _Forgery, rule: RuleVersion, system=ProducingSystem.PARASHARI):
    forgery.store._db.execute("INSERT INTO registered_rule_versions (rule_id, version, variant, payload) VALUES "
                              "(?, ?, ?, ?)", (rule.rule.value, rule.version, rule.spec.variant,
                                               json.dumps(rule_to_record(rule))))
    item = forgery.world.item(system, rule=RuleReference(rule=rule.rule, version=rule.version, variant=rule.spec.variant),
                              declared_strength=rule.spec.declared_strength)
    forgery.row(item)
    forgery.graph(item, rule)
    return item


def _published(key: str, version: int, variant: str) -> RuleVersion:
    registry = rule_registry.pinned()
    return registry.rule_version(registry.by_key(key), version, variant)


HISTORICAL_FORGERIES = (
    ("a RUL never issued", lambda forgery: _plant_historical(forgery, dataclasses.replace(
        _earlier(_published(PARASHARI_KEY, 2, "base")), rule=forgery.unissued)), "never issued"),
    ("a school the allocation history contradicts", lambda forgery: _plant_historical(
        forgery, _earlier(_published(VARIANTS_KEY, 1, "reading-a"), school=ProducingSystem.KP), ProducingSystem.KP),
     "by the allocation history"),
    ("a version never published", lambda forgery: _plant_historical(forgery, dataclasses.replace(
        _earlier(_published(PARASHARI_KEY, 2, "base")), version=99)), "never withdrawn"),
    ("a variant never published", lambda forgery: _plant_historical(
        forgery, _earlier(_published(PARASHARI_KEY, 1, "base"), variant="forged")), "never withdrawn"),
    ("rewritten content", lambda forgery: _plant_historical(
        forgery, _earlier(_published(PARASHARI_KEY, 2, "base"), content_hash="e" * 64)),
     "contradicts its immutable publication"),
    ("a rewritten declared strength", lambda forgery: _plant_historical(
        forgery, _earlier(_published(VARIANTS_KEY, 1, "reading-b"), declared_strength="planted")),
     "contradicts its immutable publication"),
)


def gate_u_historical_rule_integrity():
    """A rule version recorded under an earlier snapshot is read only as what the governed records prove: an RUL the
    allocation history issued, under its school, and a version still published unchanged, because a published version is
    never withdrawn or rewritten. Genuine history stays readable without the current snapshot hash. Each real check is
    then weakened in turn (ADR-0127; H4 s4; ADR-0121; ADR-0120 AC2)."""

    refused, controls, preserved = {}, {}, {}

    def refuses(label, action, reason=""):
        try:
            action()
        except StoreError as exc:
            if reason not in str(exc):
                fail(f"{label} was refused for another reason: {exc}")
            refused[label] = True
            return
        fail(f"not refused: {label}")

    for label, plant, reason in HISTORICAL_FORGERIES:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as folder:
            setting = _GraphWorld(Path(folder) / "evidence.sqlite")
            store: EvidenceStore = setting.store
            forgery = _Forgery(setting)
            good = forgery.good
            plant(forgery)
            refuses(f"load of {label}", lambda: store.load(FORGED_ID), reason)
            for read, action in (("evidence_ids", lambda: store.evidence_ids()),
                                 ("join", lambda: store.join((good, FORGED_ID))),
                                 ("counts", lambda: store.counts()),
                                 ("classify", lambda: store.classify(good, FORGED_ID)),
                                 ("relate", lambda: store.relate(good, FORGED_ID)),
                                 ("item_graph", lambda: store.item_graph(FORGED_ID)),
                                 ("reproduce", lambda: store.reproduce(FORGED_ID)),
                                 ("recorded_graph", lambda: store.recorded_graph())):
                refuses(f"{read} with {label}", action, reason)
            if store.load(good) != setting.world.item():
                fail(f"{label} took a legitimate item down with it")
            preserved[f"a legitimate item beside {label}"] = True
            store.close()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as folder:
        setting = _GraphWorld(Path(folder) / "evidence.sqlite")
        store: EvidenceStore = setting.store
        forgery = _Forgery(setting)
        item = _plant_historical(forgery, _earlier(_published(PARASHARI_KEY, 2, "base")))
        if store.load(FORGED_ID) != item or FORGED_ID not in store.evidence_ids() or \
                store.reproduce(FORGED_ID) != provenance_graph.recorded_fields(item) or \
                len(store.join((forgery.good, FORGED_ID))) != 2 or not store.recorded_graph().nodes:
            fail("a genuinely issued version recorded under an earlier snapshot was not readable")
        preserved["a genuinely issued version recorded under an earlier snapshot"] = True

        def too_strict(entry):
            rule = store.rule_version(entry.rule)
            if rule.spec.knowledge_snapshot_hash != rule_registry.pinned().snapshot_sha256:
                raise StoreError("another snapshot")
            return rule

        store._admitted_rule = too_strict
        refuses("a planted check demanding the current snapshot, on genuine history", lambda: store.load(FORGED_ID),
                "another snapshot")
        del store._admitted_rule
        controls["a check demanding the current snapshot rejected: it refuses genuine history"] = True
        store.close()
    # Each real check does the refusing: weakened, the same read accepts the forgery, or another check takes over.
    for label, index, weakened, outcome in (
            ("the publication check", 2, {"_require_unchanged_publication": lambda rule, registry: None}, "admitted"),
            ("the publication check, on rewritten content", 4,
             {"_require_unchanged_publication": lambda rule, registry: None}, "admitted"),
            ("both the history and publication checks", 0, {"_require_issued": lambda rule, issued: None,
                                                            "_require_unchanged_publication": lambda rule, registry: None},
             "admitted"),
            ("the history check alone", 0, {"_require_issued": lambda rule, issued: None}, "never withdrawn")):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as folder:
            setting = _GraphWorld(Path(folder) / "evidence.sqlite")
            store: EvidenceStore = setting.store
            forgery = _Forgery(setting)
            _name, plant, reason = HISTORICAL_FORGERIES[index]
            plant(forgery)
            refuses(f"the real read, before weakening {label}", lambda: store.load(FORGED_ID), reason)
            for check, weak in weakened.items():
                store.__setattr__(check, weak)
            if outcome == "admitted":
                if store.load(FORGED_ID) is None:
                    fail(f"weakening {label} did not change the read")
                controls[f"{label}, weakened, admits the forgery on the real read path"] = True
            else:
                refuses(f"the read with {label} weakened", lambda: store.load(FORGED_ID), outcome)
                controls[f"{label}, weakened, leaves the publication check refusing: the checks are layered"] = True
            store.close()
    return {"classification": "negative_control", "forgeries": len(HISTORICAL_FORGERIES),
            "refusals_verified": len(refused), "legitimate_reads_preserved": len(preserved),
            "controls_rejected": len(controls), "refused": sorted(refused), "preserved": sorted(preserved),
            "controls": sorted(controls)}


# ------------------------------------------------------------------ INTERPRETATION prerequisites, Stage 1 (ADR-0130)

GENUINE_KEY = "genuine.test.parashari.tenth-lord-in-first"
#: A test source for the publication mechanism. It is not a real edition and the genuine test rule quotes nothing.
TEST_SOURCE = {"id": "SRC-TEST-0001", "school": "parashari", "work": "Test work, written for these checks",
               "edition": "Test edition", "language": "test", "witness_url": "https://example.invalid/witness",
               "witness_sha256": "0" * 64, "rights_basis": "test fixture; contains no source text"}
TEST_LOCATOR = "chapter 24, verse 109, page 325"


def _write_json(path: Path, data) -> None:
    path.write_bytes((json.dumps(data, sort_keys=True, indent=1) + "\n").encode("ascii"))


def sourced_copy(root: Path, name: str, change=None, history_change=None) -> tuple:
    """A copy of the pinned registry, rewritten as a sourced snapshot that publishes one genuine test rule from the test
    source, then changed by `change`. Returns the directory and the digest that loads it."""

    target = root / name
    shutil.copytree(rule_registry.DATA_DIR, target)
    history = json.loads((target / rule_registry.HISTORY_NAME).read_bytes())
    number = len(history["allocations"]) + 1
    history["allocations"].append({"key": GENUINE_KEY, "number": number, "school": "parashari"})
    if history_change:
        history_change(history)
    _write_json(target / rule_registry.HISTORY_NAME, history)
    snapshot = json.loads((target / "snapshot.json").read_bytes())
    base = rule_registry.pinned().lookup(rule_registry.pinned().by_key(PARASHARI_KEY), 1, "base")
    record = {**rule_registry.content_record(base), "rule": number, "key": GENUINE_KEY, "known_variants": ["base"],
              "citation": {"source": TEST_SOURCE["id"], "locator": TEST_LOCATOR},
              "statement": "Test statement written for these checks; it quotes no source.",
              "declared_strength": "not stated", "synthetic": False}
    _rehash(record)
    document = {"schema": rule_registry.SOURCED_SNAPSHOT_SCHEMA, "rules": snapshot["rules"] + [record],
                "sources": [dict(TEST_SOURCE)], "verifications": []}
    if change:
        change(document)
    _write_json(target / "snapshot.json", document)
    digest = hashlib.sha256((target / "snapshot.json").read_bytes()).hexdigest()
    manifest = json.loads((target / rule_registry.MANIFEST_NAME).read_bytes())
    manifest["sha256"] = digest
    _write_json(target / rule_registry.MANIFEST_NAME, manifest)
    return target, digest


def _genuine(document) -> dict:
    return document["rules"][-1]


def _claim_checked(document) -> None:
    _rehash(_genuine(document), certification={**_genuine(document)["certification"],
                                               "transcription_fidelity": "independently_checked"})


def _verification(document, **changes) -> dict:
    rule = _genuine(document)
    entry = {"rule": rule["rule"], "version": rule["version"], "variant": rule["variant"], "verifier": "test verifier",
             "transcription_sha256": rule_registry.statement_digest(rule["statement"]),
             "reviewed": list(rule_registry.VERIFIED_ASPECTS)}
    entry.update(changes)
    return entry


def _genuine_projection(registry: rule_registry.RuleRegistry, key: str = GENUINE_KEY) -> RuleVersion:
    """What a forger would write for a genuine rule: the shape of a projection, built around rule_version()."""

    item = registry.lookup(registry.by_key(key), 1, "base")
    return RuleVersion(rule=item.rule, version=1, spec=RuleSpec(
        school=item.school, content_hash=item.content_hash, knowledge_snapshot_hash=registry.snapshot_sha256,
        declared_strength=item.declared_strength, variant="base",
        provenance=RecordProvenance(source="the pinned rule registry", method="published snapshot",
                                    schema_version=rule_registry.SNAPSHOT_SCHEMA), data_class=DataClass.SYNTHETIC))


def gate_v_genuine_rule_publication():
    """The publication-only mechanism: a genuine rule is published only from an authorized source of its own school, at
    a precise locator, with any independent-checked claim backed by a matching verification; it is published for
    citation and never projected into evidence, by registration or by a row forged directly into the database. The
    pinned snapshot and its pin are unchanged, and a sourced snapshot keeps every earlier publication intact under G3
    (ADR-0130; ADR-0120 D1, AC11 as narrowed)."""

    refused, controls, preserved = {}, {}, {}

    def refuses(label, action, reason=""):
        try:
            action()
        except (rule_registry.RegistryError, StoreError) as exc:
            if reason not in str(exc):
                fail(f"{label} was refused for another reason: {exc}")
            refused[label] = True
            return
        fail(f"not refused: {label}")

    pinned = rule_registry.pinned()
    if pinned.sources() or [item for item in pinned.rules() if item.synthetic is not True] or \
            pinned.snapshot_sha256 != rule_registry.PINNED_SNAPSHOT_SHA256:
        fail("the pinned snapshot lists a source or a genuine rule; Stage 1 publishes none")
    preserved["the pinned snapshot lists no source and publishes synthetic rules only"] = True
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as folder:
        root = Path(folder)
        directory, digest = sourced_copy(root, "clean")
        registry = rule_registry.load_registry(directory, digest)
        genuine = registry.lookup(registry.by_key(GENUINE_KEY), 1, "base")
        if genuine.synthetic or genuine.citation.source != TEST_SOURCE["id"] or len(registry.sources()) != 1:
            fail("a genuine rule from an authorized source was not published for citation")
        preserved["a genuine rule from an authorized source is published for citation"] = True
        refuses("projecting a genuine rule into evidence", lambda: registry.rule_version(genuine.rule, 1, "base"),
                "never projected into evidence")
        previous = (json.loads((rule_registry.DATA_DIR / rule_registry.HISTORY_NAME).read_bytes()),
                    json.loads((rule_registry.DATA_DIR / "snapshot.json").read_bytes()))
        if check_rule_registry.check_against(*previous, directory) != []:
            fail("a sourced snapshot rewrote or withdrew an earlier publication (G3)")
        preserved["every earlier publication is unchanged under G3"] = True
        for label, change, reason in (
                ("a genuine rule citing an unlisted source",
                 lambda d: _rehash(_genuine(d), citation={"source": "SRC-OTHER", "locator": TEST_LOCATOR}),
                 "synthetic rules only"),
                ("a genuine rule citing a source of another school",
                 lambda d: d["sources"][0].update(school="kp"), "synthetic rules only"),
                ("a locator with no chapter or page", lambda d: _rehash(_genuine(d), citation={
                    "source": TEST_SOURCE["id"], "locator": "BPHS 24.109"}), "names chapter, verse and page"),
                ("a locator with a chapter only", lambda d: _rehash(_genuine(d), citation={
                    "source": TEST_SOURCE["id"], "locator": "chapter 24"}), "names chapter, verse and page"),
                ("a locator with no chapter", lambda d: _rehash(_genuine(d), citation={
                    "source": TEST_SOURCE["id"], "locator": "verse 109, page 325"}), "names chapter, verse and page"),
                ("an independently checked claim with no verification", _claim_checked, "no independent verification"),
                ("a verification whose transcription does not match", lambda d: (_claim_checked(d), d["verifications"].append(
                    _verification(d, transcription_sha256="1" * 64))), "does not match the published statement"),
                ("a verification that does not review every aspect", lambda d: (_claim_checked(d), d["verifications"].append(
                    _verification(d, reviewed=["statement"]))), "reviews exactly"),
                ("a verification naming a synthetic rule", lambda d: d["verifications"].append(
                    {**_verification(d), "rule": 1, "version": 1, "variant": "base"}), "one published genuine rule"),
                ("an authorized source listed twice", lambda d: d["sources"].append(dict(TEST_SOURCE)), "listed once"),
                ("a source whose witness is not pinned", lambda d: d["sources"][0].update(witness_sha256="unpinned"),
                 "pins its witness"),
                ("a source missing its rights basis", lambda d: d["sources"][0].pop("rights_basis"),
                 "only its schema's fields"),
                ("a sourced snapshot under the plain schema name",
                 lambda d: d.update(schema=rule_registry.SNAPSHOT_SCHEMA), "not a rule snapshot of this schema")):
            planted, planted_digest = sourced_copy(root, f"planted{len(refused)}", change)
            refuses(f"a sourced snapshot with {label}", lambda: rule_registry.load_registry(planted, planted_digest),
                    reason)
        unissued, unissued_digest = sourced_copy(root, "unissued", history_change=lambda h: h["allocations"].pop())
        refuses("a genuine rule whose number the allocation history never issued",
                lambda: rule_registry.load_registry(unissued, unissued_digest), "never issued")
        record = {**rule_registry.content_record(genuine), "content_hash": genuine.content_hash}
        refuses("a genuine rule read with no authorized source", lambda: rule_registry.rule_from_record(record),
                "synthetic rules only")
        # Evidence: a genuine rule cannot be registered, and a row forged for one is refused by every read, whether the
        # row claims the snapshot in force or an earlier one.
        in_force = rule_registry.pinned
        rule_registry.pinned = lambda: registry
        try:
            projection = _genuine_projection(registry)
            for index, (hash_, label, reasons) in enumerate((
                    (registry.snapshot_sha256, "the pinned snapshot hash", ("never projected into evidence",)),
                    ("f" * 64, "an earlier snapshot hash", ("never issued", "never projected into evidence")))):
                store: EvidenceStore = EvidenceStore(root / f"evidence{index}.sqlite")
                owner = store.entities.persist(_synthetic_subjects()[0])
                candidate = store.entities.load(owner).charts[0]
                if index == 0:
                    refuses("registering a genuine rule as evidence", lambda: store.register_rule(projection),
                            "never projected into evidence")
                parashari = store.register_rule(registry.rule_version(registry.by_key(PARASHARI_KEY), 1, "base"))
                world = _EvidenceWorld(owner, candidate.label, {ProducingSystem.PARASHARI: parashari})
                good = store.persist(world.item())
                forged_rule = dataclasses.replace(projection, spec=dataclasses.replace(
                    projection.spec, knowledge_snapshot_hash=hash_))
                evidence_id = EvidenceId.from_number(800 + index)
                item = world.item(facts=("Forged longitude",),
                                  rule=RuleReference(rule=forged_rule.rule, version=1, variant="base"),
                                  declared_strength=forged_rule.spec.declared_strength)
                store._db.execute("INSERT INTO registered_rule_versions (rule_id, version, variant, payload) VALUES "
                                  "(?, ?, ?, ?)", (forged_rule.rule.value, 1, "base",
                                                   json.dumps(rule_to_record(forged_rule))))
                store._db.execute("INSERT INTO evidence_items (evidence_id, entity_id, recomputes, payload) VALUES "
                                  "(?, ?, NULL, ?)", (evidence_id.value, item.entity.value,
                                                      json.dumps(item_to_record(evidence_id, item))))
                built = provenance_graph.record_graph(evidence_id, item, candidate, None, forged_rule, {})
                for node in built.nodes:
                    store._db.execute("INSERT OR IGNORE INTO graph_nodes (node_key, kind, payload) VALUES (?, ?, ?)",
                                      provenance_graph.node_to_row(node))
                for edge in built.edges:
                    store._db.execute("INSERT OR IGNORE INTO graph_edges (source_key, kind, target_key, position) "
                                      "VALUES (?, ?, ?, ?)", (edge.source.key, edge.kind.value, edge.target.key,
                                                              edge.position))
                for read, action in (("load", lambda: store.load(evidence_id)),
                                     ("evidence_ids", lambda: store.evidence_ids()),
                                     ("join", lambda: store.join((good, evidence_id))),
                                     ("classify", lambda: store.classify(good, evidence_id)),
                                     ("reproduce", lambda: store.reproduce(evidence_id))):
                    reason = next((text for text in reasons if _refusal(action, text)), None)
                    if reason is None:
                        fail(f"{read} of a row forged for a genuine rule at {label} was not refused for its reason")
                    refused[f"{read} of a row forged for a genuine rule at {label}"] = True
                if index == 0:
                    # Control: a projection that lets a genuine rule through is what this refusal rests on.
                    weak = rule_registry.RuleRegistry(registry.rules(), registry.snapshot_sha256)
                    weak.rule_version = lambda rule, version, variant: projection if rule == projection.rule else \
                        registry.rule_version(rule, version, variant)
                    rule_registry.pinned = lambda: weak
                    if store.load(evidence_id).rule.rule != projection.rule:
                        fail("a projection admitting genuine rules was not distinguishable from the real one")
                    controls["a rule_version() that projects genuine rules admits the forged evidence"] = True
                    rule_registry.pinned = lambda: registry
                store.close()
        finally:
            rule_registry.pinned = in_force
        # Controls: each publication check, weakened, admits what it refuses.
        unlisted, unlisted_digest = sourced_copy(root, "control-unlisted", lambda d: _rehash(_genuine(d), citation={
            "source": "SRC-OTHER", "locator": TEST_LOCATOR}))
        authorize = rule_registry._require_authorized
        rule_registry._require_authorized = lambda data, sources: None
        try:
            rule_registry.load_registry(unlisted, unlisted_digest)
            controls["the source check, weakened, publishes a rule from an unlisted source"] = True
        except rule_registry.RegistryError as exc:
            fail(f"weakening the source check did not change the load: {exc}")
        finally:
            rule_registry._require_authorized = authorize
        unverified, unverified_digest = sourced_copy(root, "control-unverified", _claim_checked)
        verify = rule_registry._require_verified
        rule_registry._require_verified = lambda rules, verifications: None
        try:
            rule_registry.load_registry(unverified, unverified_digest)
            controls["the verification check, weakened, publishes an unverified checked claim"] = True
        except rule_registry.RegistryError as exc:
            fail(f"weakening the verification check did not change the load: {exc}")
        finally:
            rule_registry._require_verified = verify
    return {"classification": "negative_control", "refusals_verified": len(refused),
            "legitimate_reads_preserved": len(preserved), "controls_rejected": len(controls),
            "refused": sorted(refused), "preserved": sorted(preserved), "controls": sorted(controls)}


def _refusal(action, reason: str) -> bool:
    """Whether `action` is refused by the store or the registry with `reason` in its message."""

    try:
        action()
    except (rule_registry.RegistryError, StoreError) as exc:
        return reason in str(exc)
    return False


def _candidate(scope, segments) -> dict:
    return {"schema": explanation_boundary.EXPLANATION_SCHEMA, "scope": [value.value for value in scope],
            "segments": segments}


def gate_w_explanation_boundary():
    """The explanation boundary refuses, fail closed, any candidate that is not made of references alone, and renders
    every sentence from the evidence store's checked reads and the pinned registry. Each check, weakened, admits what it
    refuses, and no planted text ever reaches the rendered output (ADR-0130; H5 s3; Q8 s7)."""

    refused, controls, preserved = {}, {}, {}
    BoundaryError = explanation_boundary.BoundaryError

    def refuses(label, action, reason=""):
        try:
            action()
        except BoundaryError as exc:
            if reason not in str(exc):
                fail(f"{label} was refused for another reason: {exc}")
            refused[label] = True
            return
        fail(f"not refused: {label}")

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as folder:
        setting = _GraphWorld(Path(folder) / "evidence.sqlite")
        store: EvidenceStore = setting.store
        ids = setting.populate()
        registry = rule_registry.pinned()
        first, second = ids[0], ids[1]
        item = store.load(first)
        segments = [{"kind": "rule_statement", "evidence": first.value},
                    {"kind": "rule_citation", "evidence": first.value},
                    {"kind": "chart_fact", "evidence": first.value, "field": "planets"},
                    {"kind": "calculated_input", "evidence": first.value, "index": 0},
                    {"kind": "timing", "evidence": second.value}, {"kind": "polarity", "evidence": second.value},
                    {"kind": "uncertainty", "evidence": first.value, "field": "historical_performance"},
                    {"kind": "no_answer"}]
        lines = explanation_boundary.render(_candidate((first, second), segments), store, registry)
        published = registry.lookup(item.rule.rule, item.rule.version, item.rule.variant)
        if not (published.statement in lines[0] and published.citation.locator in lines[1] and
                all(planet in lines[2] for planet in item.chart_context.planets) and
                item.lineage.inputs[0].fact in lines[3] and store.load(second).timing.label in lines[4] and
                lines[7] == explanation_boundary.ABSTENTION_TEXT):
            fail("a rendered sentence does not come from the evidence and the registry")
        preserved["every kind renders from the evidence and the pinned registry"] = True
        # A no-answer segment over valid, non-conflicting evidence renders the neutral abstention and nothing else.
        if item.polarity is Polarity.CONTRADICTORY or store.relationships():
            fail("the no-answer cases need evidence that records no conflict")
        if explanation_boundary.render(_candidate((first,), [{"kind": "no_answer"}]), store, registry) != (
                explanation_boundary.ABSTENTION_TEXT,):
            fail("a no-answer segment rendered more than the neutral abstention")
        preserved["a no-answer segment renders only the neutral abstention"] = True
        good = segments[:1]
        cases = [
            ("a candidate that is text", "the tenth lord in the first house gives fame", {}, "carries exactly"),
            ("a candidate with a free-text field", {**_candidate((first,), good), "text": "a new rule"}, {},
             "carries exactly"),
            ("a candidate missing its scope", {"schema": explanation_boundary.EXPLANATION_SCHEMA, "segments": good}, {},
             "carries exactly"),
            ("another schema", {**_candidate((first,), good), "schema": "v0"}, {}, "this schema"),
            ("an empty scope", _candidate((), good), {}, "names the evidence in its scope"),
            ("an item in scope twice", _candidate((first, first), good), {}, "in scope once"),
            ("no segments", _candidate((first,), []), {}, "at least one segment"),
            ("a segment that is text", _candidate((first,), ["Saturn in the tenth brings delay"]), {}, "names its kind"),
            ("an undeclared kind", _candidate((first,), [{"kind": "rule_application", "evidence": first.value}]), {},
             "undeclared segment kind"),
            ("a rule statement given in the candidate", _candidate((first,), [
                {"kind": "rule_statement", "evidence": first.value, "statement": "an invented rule"}]), {},
             "carries exactly"),
            ("a rule identifier given in the candidate", _candidate((first,), [
                {"kind": "rule_citation", "evidence": first.value, "rule": RuleId.from_number(2).value}]), {},
             "carries exactly"),
            ("a polarity given in the candidate", _candidate((first,), [
                {"kind": "polarity", "evidence": first.value, "value": "negative"}]), {}, "carries exactly"),
            ("an overridden calculated value", _candidate((first,), [
                {"kind": "calculated_input", "evidence": first.value, "index": 0, "value": "Moon 12 Aries"}]), {},
             "carries exactly"),
            ("a chart field the contract does not define", _candidate((first,), [
                {"kind": "chart_fact", "evidence": first.value, "field": "effect"}]), {}, "names one of"),
            ("an uncertainty field the contract does not define", _candidate((first,), [
                {"kind": "uncertainty", "evidence": first.value, "field": "score"}]), {}, "names one of"),
            ("an input index that is not a number", _candidate((first,), [
                {"kind": "calculated_input", "evidence": first.value, "index": "first"}]), {}, "by its index"),
            ("an input index that is a boolean", _candidate((first,), [
                {"kind": "calculated_input", "evidence": first.value, "index": True}]), {}, "by its index"),
            ("a negative input index", _candidate((first,), [
                {"kind": "calculated_input", "evidence": first.value, "index": -1}]), {}, "by its index"),
            ("an evidence reference that is not an identifier", _candidate((first,), [
                {"kind": "polarity", "evidence": "the first item"}]), {}, "not an EVD identifier"),
            ("an evidence reference that is not text", _candidate((first,), [
                {"kind": "polarity", "evidence": {"id": first.value}}]), {}, "an EVD identifier"),
            ("a no-answer segment with its own words", _candidate((first,), [
                {"kind": "no_answer", "reason": "the stars are unclear"}]), {}, "carries exactly"),
            ("a no-answer segment naming evidence", _candidate((first,), [
                {"kind": "no_answer", "evidence": first.value}]), {}, "carries exactly"),
            *((f"a candidate-selected reason, {reason}, over valid non-conflicting evidence", _candidate((first,), [
                {"kind": "polarity", "evidence": first.value}, {"kind": "no_answer", "reason": reason}]), {},
               "carries exactly")
              for reason in ("no_evidence", "incomplete_lineage", "conflicting_evidence", "outside_scope")),
            ("evidence outside the scope", _candidate((first,), [{"kind": "polarity", "evidence": second.value}]), {},
             "not in the explanation's scope"),
            ("an input the item does not record", _candidate((first,), [
                {"kind": "calculated_input", "evidence": first.value, "index": 99}]), {}, "records no calculated input"),
            ("an item that does not exist", _candidate((EvidenceId.from_number(990),), [
                {"kind": "polarity", "evidence": EvidenceId.from_number(990).value}]), {}, "fails the evidence read"),
            ("a rule the pinned registry does not publish", _candidate((first,), good),
             {"registry": rule_registry.RuleRegistry(tuple(rule for rule in registry.rules() if rule.rule != item.rule.rule),
                                                     registry.snapshot_sha256)}, "is not registered"),
        ]
        for label, candidate, options, reason in cases:
            use = options["registry"] if "registry" in options else registry
            refuses(f"{label}", lambda candidate=candidate, use=use: explanation_boundary.render(candidate, store, use),
                    reason)
        # An intact row whose recorded graph is missing: only the store's full read refuses it.
        planted_id = EvidenceId.from_number(991)
        store._db.execute("INSERT INTO evidence_items (evidence_id, entity_id, recomputes, payload) VALUES "
                          "(?, ?, NULL, ?)", (planted_id.value, item.entity.value,
                                              json.dumps(item_to_record(planted_id, item))))
        if store._stored_item(planted_id) != item:
            fail("the planted row does not read cleanly on its own")
        refuses("an intact row whose recorded graph is missing", lambda: explanation_boundary.render(
            _candidate((planted_id,), [{"kind": "polarity", "evidence": planted_id.value}]), store, registry),
            "fails the evidence read")
        # Controls: each check, weakened, admits what it refuses; no planted text ever reaches the output.
        planted = "PLANTED: an invented rule"
        exact = explanation_boundary._exact
        explanation_boundary._exact = lambda name, data, keys: data
        try:
            rendered = explanation_boundary.render({**_candidate((first,), [
                {"kind": "rule_statement", "evidence": first.value, "statement": planted}]), "text": planted},
                store, registry)
        finally:
            explanation_boundary._exact = exact
        controls["the structural parse, weakened, admits a candidate carrying free text"] = True
        if any(planted in line for line in rendered):
            fail("the renderer echoed text from a candidate")
        controls["even then, the renderer never echoes a candidate's text"] = True
        # Control: a parse that drops a candidate's reason instead of refusing it admits the reason; even then, no reason
        # reaches the output, so the evidence is never said to conflict.
        strict = explanation_boundary._exact
        explanation_boundary._exact = lambda name, data, keys: strict(name, {
            key: value for key, value in data.items() if key != "reason"} if name == "a no_answer segment" and
            isinstance(data, dict) else data, keys)
        try:
            rendered = explanation_boundary.render(_candidate((first,), [
                {"kind": "no_answer", "reason": "conflicting_evidence"}]), store, registry)
        finally:
            explanation_boundary._exact = strict
        controls["a parse that ignores a candidate's reason, weakened, admits it"] = True
        if rendered != (explanation_boundary.ABSTENTION_TEXT,):
            fail("a candidate-selected reason reached the rendered output")
        controls["even then, no candidate-selected reason reaches the output"] = True
        published_check = explanation_boundary._published
        explanation_boundary._published = lambda entry, registry_: _forged_rule(
            published_check(entry, registry_), statement=planted)
        try:
            weak_lines = explanation_boundary.render(_candidate((first,), good), store, registry)
        finally:
            explanation_boundary._published = published_check
        if planted not in weak_lines[0]:
            fail("rule statements did not come through the registry lookup")
        controls["rule statements come only through the registry lookup"] = True
        scope_check = explanation_boundary.admit
        explanation_boundary.admit = lambda explanation, store_, registry_: {
            value: store_.load(value) for value in (first, second)}
        try:
            explanation_boundary.render(_candidate((first,), [{"kind": "polarity", "evidence": second.value}]), store,
                                        registry)
            controls["the scope check, weakened, admits evidence outside the scope"] = True
        except BoundaryError as exc:
            fail(f"weakening the scope check did not change the render: {exc}")
        finally:
            explanation_boundary.admit = scope_check
        store.close()
    tree = ast.parse((ROOT / "engine" / "evidence" / "explanation_boundary.py").read_text(encoding="utf-8"))
    imported = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module} | \
        {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
    if not imported <= {"__future__", "dataclasses", "enum", "engine.evidence.rule_registry", "engine.evidence.evidence",
                        "engine.evidence.evidence_identifiers", "engine.evidence.evidence_store",
                        "engine.evidence.store"}:
        fail(f"the explanation boundary imports beyond the evidence layer: {sorted(imported)}")
    controls["no LLM client, network or calculation module is imported by the boundary"] = True
    return {"classification": "negative_control", "refusals_verified": len(refused),
            "legitimate_reads_preserved": len(preserved), "controls_rejected": len(controls),
            "refused": sorted(refused), "preserved": sorted(preserved), "controls": sorted(controls)}


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
        "J_evidence_integrity": gate_j_evidence_integrity(),
        "K_evidence_refusals": gate_k_evidence_refusals(),
        "L_relationships_and_provenance": gate_l_relationships_and_provenance(),
        "M_registry_integrity": gate_m_registry_integrity(),
        "N_registry_refusals": gate_n_registry_refusals(),
        "O_snapshot_fails_closed": gate_o_snapshot_fails_closed(),
        "P_graph_integrity": gate_p_graph_integrity(),
        "Q_graph_refusals": gate_q_graph_refusals(),
        "R_graph_agreement": gate_r_graph_agreement(),
        "S_evidence_read_integrity": gate_s_evidence_read_integrity(),
        "T_relationship_integrity": gate_t_relationship_integrity(),
        "U_historical_rule_integrity": gate_u_historical_rule_integrity(),
        "V_genuine_rule_publication": gate_v_genuine_rule_publication(),
        "W_explanation_boundary": gate_w_explanation_boundary(),
    }
    report = {
        "schema": "evidence_foundations_v1_certification",
        "adr": "ADR-0115 s4; ADR-0116 s4; ADR-0119 s3, s5; ADR-0120 s4, s6; ADR-0121; ADR-0122 s4, s6; ADR-0124; ADR-0125; ADR-0127; ADR-0130",
        "date": str(date.today()),
        "scope": ("Structural certification of the EVIDENCE foundations: the H0 entity model, append-only entity store "
                  "and ENT issuer (ADR-0114 WP-E1), and the H1 event model, append-only event store, separate "
                  "confirmation records, EVR issuer and seeded event-class vocabulary (ADR-0115 WP-E2), and the H2 "
                  "historical ledger, protected holdouts, pre-registered protocols and purpose-declared access log "
                  "(ADR-0116 WP-E3), and the H4 evidence model, append-only evidence store, EVD and RUL issuers, "
                  "provenance-checked joins, decomposable aggregates and structural relationship records "
                  "(ADR-0119 WP-E4), and the H5 interpretation rule registry, its hash-pinned fail-closed snapshot "
                  "and the governed RUL authoring process (ADR-0120 WP-E5; ADR-0121), and the provenance graph "
                  "recorded at evidence-creation time (ADR-0122 WP-E6)."),
        "reference": {
            "structure": "the model contracts of ADR-0114 s3, ADR-0115 s5, ADR-0116 s5, ADR-0119 s5, ADR-0120 s6 "
                         "and ADR-0122 s6, exercised on synthetic records",
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
            "no TEST record, performance measurement or validation-run result is certified: they need H5 and rule "
            "application",
            "rule-version references are synthetic structural references: not proof of registration or validation "
            "in a future real-rule registry, and they authorize no interpretation",
            "every rule the pinned snapshot publishes is a synthetic fixture rule: no real rule is transcribed, sourced "
            "or attributed, and the registry's certification claims are all not_assessed. The publication mechanism for "
            "genuine rules is exercised only on test snapshots with a test source (ADR-0130)",
            "a genuine rule, once published, is never projected into evidence; the explanation boundary renders only "
            "trusted data and contains no LLM client, so no generated text is evaluated here",
            "no rule condition is evaluated against a chart and no rule is applied; that belongs to INTERPRETATION",
            "RUL issuance is append-only against the base commit in CI; the gate cannot see allocations made in an "
            "unreviewed fork that was never merged",
            "no rule is applied and no chart is interpreted: evidence items are synthetic records exercising the model",
            "confidence components and historical performance are carried as supplied or absent, never computed; "
            "measured reliability, cross-method and timing convergence are absent",
            "relationships are classified only from each item's own recorded inputs, derivation links and completeness "
            "statements; no convergence count or bound is computed, and CORRELATED is never assigned",
            "the store cannot verify that a producer's completeness statements are true; it only refuses to call a "
            "pair INDEPENDENT without them",
            "the provenance graph is recorded, not computed over: no path, independent count, cut, score, weight or "
            "ratio is computed, and relationship classification does not read it",
            "the graph records only what each item and the store's records state; it cannot show that a producer's "
            "recorded inputs are all it consumed, and records incompleteness where the producer states it",
            "no CORRELATED_WITH edge is recorded: correlation is measured, and nothing in EVIDENCE measures",
            "a persisted graph read refuses rows the items' stored records do not account for; it cannot detect a "
            "forged evidence record whose own graph rows were forged to agree with it",
            "a rule version recorded under another snapshot is read as history, because no earlier snapshot is archived "
            "to check it against: a forged row claiming another snapshot, with matching forged graph rows, is not detected",
            "a persisted relationship is checked against what the recorded items support; it shows agreement with the "
            "recorded structure, and does not show that two items are independent in fact",
            "the graph's node and edge kinds adopt the recording schema of docs/EVIDENCE_INDEPENDENCE_DESIGN.md s3 "
            "only (ADR-0122 D1); that document stays PROPOSED in every other respect",
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
