<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | PROPOSED, C0 RESEARCH. Specification only. No implementation is authorised by this document. Pending owner ratification (docs/OPEN_QUESTIONS.md Q1). |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-11 |
| Review cadence | TBD |

# H1. Structured Event Model

## 1. Purpose

An event is a thing that happened to a person at a time, asserted by someone, with a confidence. It
is the atom of the product's core claim: PAST BEFORE FUTURE. Everything downstream, the ledger, the
validation scoring, BTR, and the prediction feedback loop, is built on this type, so its fields
decide what the system can ever say.

This document specifies the model. It authorises no code.

## 2. Why this is first

H2 the ledger stores events. H4 evidence is scored against events. H7 BTR consumes confirmed events
as its only legitimate signal. H6 the prediction ledger compares predictions to events. Getting a
field wrong here propagates into four layers, so H1 is written before any of them.

## 3. Non-negotiable properties

**Events are asserted, never inferred silently.** Every event MUST record who asserted it: the user,
a document, a public record, or the system as a hypothesis awaiting confirmation. A
system-hypothesised event MUST NOT be usable as validation evidence until a human confirms it.
Collapsing these two is the single most dangerous shortcut available in this design, because it
lets the system validate itself.

**Time is uncertain by default.** Most remembered life events are not instants. The model MUST
represent an instant, a closed interval, an open-ended interval, and a fuzzy window with a
distribution or at least a stated tolerance. A model that only holds instants forces every user to
lie about precision, and that lie propagates into every score computed from it.

**Events are immutable once recorded.** Corrections append a superseding record and never overwrite.
This mirrors the register discipline already used for ADRs and dated evidence.

**Event class is a controlled vocabulary, not free text.** Scoring by event class is required by the
historical-validation design, and that is impossible over free text. The vocabulary MUST be a
registry with its own identifier family and its own governance, because adding a class changes what
every historical score means.

## 4. Fields

Identity: a stable identifier from a declared family, and a schema version.

Subject: which person, and which birth-data record the event is anchored to. Recording the birth
record matters because BTR will produce candidate birth times, and an event asserted under one must
not silently be reinterpreted under another.

Classification: event class from the registry, optional subclass, and optional domain.

Time: representation kind, the values it requires, the timezone and its source, and an explicit
statement of precision. A birth-time-sensitive event, for example one whose hour is known, is worth
flagging, because those are the events BTR can actually use.

Assertion: asserter, assertion timestamp, method by which it was obtained, and a confidence the
asserter holds in their own memory. Human memory of dates is unreliable in known, systematic ways,
and a model that cannot express "I am sure it was that year but not that month" will silently
overstate its own inputs.

Confirmation state: confirmed, rejected, partially confirmed, or unconfirmed. Partially confirmed is
not decoration. A user saying "yes that happened but in the spring not the autumn" is the most
common real answer and the model must hold it without forcing it into a binary.

Provenance: the same discipline the calculation layers already use. Where the assertion came from,
under what schema version, and by what process.

## 5. What the model MUST NOT do

It MUST NOT store an interpretation, a score, or any astrological content. An event is a fact about a
life. The moment a rule identifier or a planetary factor enters this type, the separation between
CALCULATION, RULE, INTERPRETATION and EVIDENCE that the charter requires is lost, and it is lost in
the one place that would be hardest to detect later.

It MUST NOT allow the system to mark its own hypothesis as confirmed.

## 6. Open questions requiring an owner decision

The identifier family and its pattern, which needs a `docs/NAMING_STANDARD.md` s2 entry before first
use. The initial event-class vocabulary, which is a domain decision and interacts with the existing
HLKG career registries. Whether events are stored per person or per birth record. The retention and
privacy posture, which is a legal question this document does not answer and should not.

## 7. Verification strategy for the eventual implementation

Round-trip serialisation. Immutability enforcement including an attempt to mutate a stored record.
Rejection of system-asserted events as validation input. Time-representation coverage for every kind
including the degenerate cases of a zero-length interval and an unbounded one. A negative test
proving an interpretation field cannot be smuggled in.

## 8. Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-11 | Created in the G1 work package as Phase H preparation. |
