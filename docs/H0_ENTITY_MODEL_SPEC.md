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

# H0. Astrological Entity Model

## 1. Why this document is numbered zero

H1 through H8 were written assuming the subject of analysis is a person with a birth chart. The
multi-domain platform vision makes that assumption wrong in four of five domains. This document
supplies the abstraction the others depend on, so it sits beneath H1 rather than beside it.

It is additive. It does not invalidate H1 through H8; it generalises their subject.

## 2. What an entity is

An entity is anything a chart can be cast for and evidence accumulated about: a person, a country, a
government, a company, an institution, a market, a relationship, an event, an election, a business
launch, or a question.

An entity is not a chart. It **has** charts, possibly several, possibly disputed. It has historical
evidence, applicable systems, applicable rules, predictions and validation results.

## 3. The four shapes, and why one type may not be enough

`docs/PLATFORM_DOMAIN_ARCHITECTURE.md` section 3 establishes four structurally different shapes:

**A. Origin moment.** Person, country, company. A moment and place exist; the entity persists.
**B. Derived moment.** Varshaphal. Derived from a parent entity's chart plus a year.
**C. Query moment.** Prashna. The chart is the moment of asking; no origin-time uncertainty exists.
**D. No entity.** General Muhurta. Time and place only, evaluating a candidate moment.

Whether these are one type with a discriminator or four related types is an open decision. What is
NOT open is that the differences must be representable, because they change what operations are
valid. Shape C cannot be rectified. Shape B's uncertainty is inherited rather than independent. Shape
D has no subject at all.

## 4. Required fields

**Identity.** A stable identifier from a declared family, and a schema version.

**Entity kind.** From a controlled vocabulary, not free text. Kind determines applicable domains,
applicable systems, and which operations are valid.

**Shape.** A, B, C or D per section 3, or whatever representation the section 3 decision produces.

**Origin moment, where one exists.** Date, time, place, timezone and its source, and precision.

**Origin certainty.** Documented, reported, or uncertain. **This field gates BTR.** A company
incorporation timestamped by a registry is documented; running rectification against it would
reintroduce the prohibited failure mode of explaining a failed prediction by deciding the time was
wrong. BTR MUST refuse where origin certainty is documented.

**Charts.** One or more, each with its own source, its own provenance and its own confidence.

Competing charts are a first-class requirement, not an edge case. Mundane entities routinely have
several defensible candidate charts, most famously India's independence. The model MUST hold them all
with their sources rather than silently selecting one, and analysis MUST be attributable to the chart
that produced it.

**Parent linkage, for shape B.** Which entity and chart this derives from, and by what derivation.

**Applicable domains and systems.** Which of the five domains and which analytical systems are
declared applicable to this entity kind. A rule written for personal natal analysis is not
automatically valid for a country, and the model should make the claim explicit rather than letting
it be assumed by absence.

**Provenance.** Where the entity record came from, under what schema version, by what process.

## 5. Prohibitions

An entity MUST NOT carry interpretation, evidence or scores. It is the subject of analysis, not a
container for it. The same separation H1 enforces for events applies here, and for the same reason:
once analytical content leaks into the subject model, the CALCULATION, RULE, INTERPRETATION, EVIDENCE
separation is lost in the hardest place to detect it.

Original entity data is immutable. Corrections and candidate origin moments append; nothing
overwrites.

An entity's applicable-systems declaration MUST NOT be inferred from what happens to run
successfully. Applicability is a recorded decision.

## 6. Consequences for H1 through H8

**H1 Event Model.** The subject field generalises from person to entity, and the birth-record anchor
generalises to a chart reference. Mundane events additionally need a public-source assertion path
distinct from the personal-memory path, because their reliability characteristics are different in
both directions: better dated, but more ambiguously classified.

**H2 Historical Event Ledger.** Events attach to entities. Performance partitioning gains entity kind
and domain as dimensions. The multiple-comparison discipline for mundane validation belongs here.

**H3 Question Engine.** A Prashna question is itself an entity, so the question model and the entity
model meet and should be designed together rather than reconciled afterwards.

**H4 Evidence Model.** Evidence gains entity, chart reference and domain alongside producing system.
Shared-origin detection becomes possible only if the chart reference is carried.

**H6 Prediction Ledger.** Predictions attach to entities, and to the specific chart that produced
them.

**H7 BTR.** Scoped by shape and gated by origin certainty, per section 4.

**H8 Convergence.** Gains the cross-domain axis, and needs the chart reference to detect that two
apparently independent sources share an origin.

## 7. Open questions requiring an owner decision

The identifier family and its pattern. Whether shapes are one type or four. The entity-kind
vocabulary. How competing charts are selected for a given analysis, and whether analysis runs across
all of them and surfaces the disagreement, which would be the more honest treatment and is also more
expensive. Whether relationships between entities, for example a person and their company, are
modelled as entities themselves or as links.

## 8. Verification strategy for the eventual implementation

Immutability enforcement. A negative test proving analytical content cannot be stored on an entity.
BTR refusal where origin certainty is documented. Competing-chart round-trip with attribution
preserved. Shape-invalid operation rejection, for example attempting rectification on a query moment.

## 9. Decisions taken (ADR-0020, additive)

Two questions this document listed as open in section 7 are now decided.

**Shape representation, D1.** Not one undifferentiated generic entity. A common
`AstrologicalSubject` and domain abstraction, with **specialised subject types** where semantics
differ: Person, Organisation/Company, Geographic/National entity, Event, Question. The point of the
decision is stated in the decision itself and is worth repeating: shared infrastructure without
pretending that all subject types have identical chart semantics.

Section 3's four shapes remain the analytical basis for which operations are valid. They are not
superseded by D1; they describe behaviour, while D1 decides representation.

**Competing charts, D3.** No silent chart selection. Entity to candidate chart set, provenance per
chart, independent analysis per chart, then comparison and explicit disagreement. The system must be
able to say that different defensible charts produce different conclusions. This is the more
expensive of the two options section 7 offered, and it was chosen deliberately.

One consequence worth naming: D3 is a requirement on a layer that does not exist. Nothing in
`engine/models/` represents a subject today, let alone a subject carrying competing charts.

Still open from section 7: the identifier family and pattern, the entity-kind vocabulary beyond the
five named types, and whether relationships between entities are modelled as entities or as links.

### 9.1 Further decisions (ADR-0021)

**Entity vocabulary, D3.** The five kinds are provisional and the ontology is deliberately NOT
frozen: Person, Organisation/Company, Geographic/National Entity, Event, Question. A new kind
requires an explicit architectural decision, because kind determines which rules are applicable and
therefore what the system may claim about that subject.

**Relationships are links, D4.** RESOLVES the last open question in section 7. Relationships are
modelled as explicit links between entities rather than as entities in their own right:

```
Entity A  --[ RELATIONSHIP ]-->  Entity B

Person   --[ LEADS ]-->          Organisation
Person   --[ CANDIDATE_IN ]-->   Election
Company  --[ OPERATES_IN ]-->    Country
Event    --[ OCCURS_IN ]-->      GeographicEntity
```

A relationship MAY be promoted to an entity later, and only if it requires all of its own lifecycle,
identity, evidence, provenance, temporal state and independent analysis.

The promotion criteria are recorded rather than assumed because relationships in this domain
genuinely can acquire those properties. A marriage has a beginning, sometimes an end, its own events,
and in some traditions its own chart. Recording the criteria makes promotion a decision rather than a
drift, which is the same discipline applied to entity kinds and to identifier families.

Section 7's remaining open item is therefore the identifier family and pattern.

## 10. Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-11 | Created from the CEO multi-domain platform vision, as the abstraction beneath H1 through H8. |
| 1.1.0 | 2026-08-11 | Additive section 9: records ADR-0020 D1 and D3, which decide two of the section 7 open questions. Sections 1 to 8 unmodified. |
| 1.2.0 | 2026-08-11 | Additive section 9.1: ADR-0021 D3 extensible vocabulary and D4 relationships as links, resolving the last section 7 question but one. |
