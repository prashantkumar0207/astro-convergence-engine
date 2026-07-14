| Field | Value |
|---|---|
| Status | DRAFT - pending owner ratification |
| Version | 0.1.0 |
| Owner | TBD (docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-07-11 |
| Review cadence | TBD |
| Governed by | docs/PROJECT_CONSTITUTION.md, docs/DOCUMENTATION_STANDARD.md, docs/VALIDATION_STANDARD.md |

# HLKG Constitution
**Human Life Knowledge Graph - constitutional framework**

This document defines the framework only. It contains no populated question inventory, no
domain payload beyond illustrative examples, and no prediction or domain-analysis logic.
Where a design choice would require an assumption, it is registered in section 21 instead.

---

## 1. Purpose of HLKG

HLKG is the governed, versioned catalogue of **human-life questions**: the canonical set of
things a person may ask about their life (timing of events, outcomes, qualities, choices),
organised so that thousands of questions can coexist without ambiguity, duplication or
drift.

HLKG answers exactly one architectural question for the wider system: *"What is being
asked?"* It deliberately does not answer *"How is it analysed?"* or *"What is the answer?"*
- those belong to other layers behind versioned contracts.

Success criterion: any natural-language life question, in any supported phrasing, resolves
deterministically to exactly one canonical node or to an explicit NO-MATCH.

## 2. Design Principles

1. **One concept, one node.** Every canonical node represents a single, indivisible
   life-question concept. Phrasings are aliases, never nodes.
2. **Determinism.** Identical inputs (text + graph version) resolve to identical nodes.
   No resolution step may depend on unstated context.
3. **Immutable identity.** A node's ID never changes and is never reused, even after
   retirement.
4. **Separation of identity and language.** IDs are language-neutral and opaque to
   meaning-shift; human labels and translations are attached data.
5. **Closed vocabularies.** Classifications and relationship types come only from the
   registries defined here; extending a registry is a governed change, not an edit.
6. **Machine-checkable rules first.** Every rule in this constitution that can be
   validated automatically MUST be (section 14); judgement-based rules are explicitly
   marked as adjudicated.
7. **Additive evolution.** The graph grows by addition and supersession, never by silent
   mutation of meaning.
8. **Evidence discipline inherited.** Claims about the graph (coverage, consistency,
   duplicate-freedom) follow docs/VALIDATION_STANDARD.md - reproducible checks, not
   narrative.

## 3. Scope

- The catalogue of canonical life-question nodes, their metadata, aliases, translations,
  classifications and inter-node relationships.
- The governance machinery: lifecycle, versioning, validation, deprecation.
- Registries required by the above: domain registry, question-class registry,
  relationship-type registry (structures defined here; population is governed data).

## 4. Non-Goals

- **No answering logic.** HLKG never encodes how any question is analysed or answered, in
  any discipline.
- **No user data.** HLKG contains question concepts, never individual people's questions,
  identities or histories.
- **No free taxonomy.** HLKG is not a general ontology of the world; concepts enter only
  as they serve life-question cataloguing.
- **No probabilistic identity.** Similarity tooling may *suggest*; it never *decides*
  node identity (section 15).
- **No embedded domain systems.** No terminology from any analytical tradition appears in
  node identity, classification or relationships.

## 5. Node Philosophy

A node is the answer-invariant core of a question: what remains when phrasing, politeness,
person, tense and language are stripped away.

- **Granularity rule:** two candidate questions are the same node if and only if a correct,
  complete answer to one is necessarily a correct, complete answer to the other. If either
  direction fails, they are distinct nodes (possibly related via `refines`).
- **Composition rule:** compound questions ("When will X happen and will it be good?") are
  not nodes; they decompose into existing nodes joined at query time. HLKG stores atoms.
- **Subject rule:** nodes are subject-neutral (self, family member, third party is a query
  parameter, not a node dimension) unless the subject changes the concept itself - such
  exceptions require adjudication and a recorded rationale.
- **Parameter rule:** quantifiable specifics (dates, counts, names) are parameters, never
  baked into nodes. "Will I relocate before <year>?" parameterises the relocation-timing
  node; it does not create a new node.

## 6. Canonical Naming Rules

Every node carries two identifiers:

1. **Node ID (immutable, primary):** `HLKG-N-XXXXXX` where `XXXXXX` is a zero-padded,
   monotonically increasing integer issued by the registry. Never encodes meaning; never
   reused.
2. **Canonical slug (stable, human-oriented):** `domain.topic.aspect` in lowercase ASCII
   `snake_case` segments joined by dots. Rules:
   - Exactly three segments (domain from the domain registry; topic and aspect free-form
     within the character rules).
   - Segment charset `[a-z0-9_]`, 2-30 characters each; no leading/trailing underscore.
   - Singular nouns; no synonyms, abbreviations or marketing terms; English (section 16).
   - Slugs MAY be corrected for spelling via change management; the Node ID guarantees
     continuity.
3. **Canonical label:** one English sentence in neutral interrogative form, third person
   or subject-neutral, ending in `?`, <= 120 characters. Exactly one per node.

## 7. Alias Policy

- An alias is a surface form (phrasing, synonym, colloquialism, regional variant, common
  misspelling) mapped to exactly one canonical node.
- Aliases are data attached to nodes; they have no independent lifecycle, no relationships
  and no metadata beyond locale and provenance.
- Alias uniqueness is absolute per locale: one normalised alias string maps to at most one
  node graph-wide. A collision is a validation failure that blocks merge (section 14).
- Normalisation (deterministic, applied before all matching): Unicode NFKC, lowercase,
  whitespace collapse, terminal-punctuation strip. The normalisation function is versioned;
  changing it is a MAJOR graph change.
- Aliases never appear in slugs. Removing an alias is a MINOR change; moving an alias
  between nodes is a semantic change requiring adjudication.

## 8. Question Classification

Every node carries exactly one **question class** from the closed registry below. The class
describes the *shape of a complete answer*, not the method of answering.

| Class | Complete answer shape |
|---|---|
| `TIMING` | one or more time intervals/points |
| `OCCURRENCE` | yes/no (with optional qualifier), for a bounded horizon |
| `QUALITY` | graded assessment on a declared scale |
| `SELECTION` | a choice among enumerable declared options |
| `QUANTITY` | a number or numeric range |
| `DESCRIPTION` | a characterisation with no single scalar |
| `CAUSAL` | an explanation linking declared factors to a state |

Extending this registry follows section 17. A node whose honest answer shape spans two
classes is mis-granulated and must be decomposed (section 5).

## 9. Domain Classification

- Every node belongs to exactly one **primary domain** (the first slug segment). Cross-
  domain relevance is expressed through relationships, never through multi-domain
  membership - this keeps counting, coverage and ownership unambiguous.
- Domains live in a separate governed **Domain Registry** artifact (ID, slug segment,
  definition, boundary notes, owner). This constitution fixes the registry's *shape*;
  its population is a ratification decision (section 21, HQ-2).
- Illustrative domain examples (non-binding): `career`, `relationship`, `health`,
  `finance`, `residence`.
- Domain boundary disputes are resolved by the granularity rule: the domain is where the
  *answer* lives, not where the *motivation* lives ("job change for family reasons" is
  `career`).

## 10. Relationship Types

Closed registry of directed, typed edges between canonical nodes:

| Type | Meaning | Constraints |
|---|---|---|
| `REFINES` | source is a strictly narrower question than target | acyclic; single hierarchy per node pair |
| `PRECEDES` | source concept, when realised, characteristically precedes target in a life sequence | acyclic |
| `DEPENDS_ON` | a complete answer to source presupposes an answer to target | acyclic |
| `EXCLUDES` | affirmative resolutions of both are conceptually incompatible | symmetric |
| `RELATES_TO` | adjudicated relevance not expressible above | last resort; requires rationale |
| `SUPERSEDED_BY` | lifecycle pointer from a deprecated node to its replacement(s) | only from DEPRECATED nodes |

Rules: no self-edges; no duplicate (source, target, type) triples; `REFINES`/`PRECEDES`/
`DEPENDS_ON` graphs are each acyclic and validated as such; every `RELATES_TO` and every
adjudicated exception carries a written rationale in the node record.

## 11. Node Lifecycle

`PROPOSED -> REVIEW -> CANONICAL -> DEPRECATED -> RETIRED`

- **PROPOSED:** draft; excluded from resolution; may be edited freely.
- **REVIEW:** frozen draft under duplicate check (section 15) and validation (section 14).
- **CANONICAL:** live; identity immutable; metadata changes via change management only.
- **DEPRECATED:** resolvable for compatibility, flagged, carries `SUPERSEDED_BY` where a
  replacement exists; no new aliases or relationships may target it except supersession.
- **RETIRED:** not resolvable; record preserved forever (IDs never vanish, never reused).

Transitions only move rightward; a DEPRECATED node is never re-canonised - a new node is
created instead. Every transition records actor, date and rationale.

## 12. Versioning

- **Graph version (semver):** MAJOR = meaning-affecting changes (normalisation function,
  registry semantics, granularity-rule changes); MINOR = additive (new CANONICAL nodes,
  aliases, relationships, deprecations); PATCH = editorial (labels, definitions,
  translations, spelling).
- **Node revision:** integer per node, incremented on any change to its record; the (Node
  ID, revision) pair is citable.
- Consumers pin a graph version; resolution behaviour is reproducible per version.
  Released graph versions are immutable artifacts with checksums.

## 13. Change Management

- All changes enter as change requests referencing: affected node(s), lifecycle
  transition(s), validation run output, and - for semantic changes - written rationale.
- Semantic changes (alias reassignment, relationship addition/removal, deprecation,
  granularity decisions) require adjudication by the designated graph owner (HQ-1).
- Editorial changes require review but not adjudication.
- Every merged change appends to the graph's own change log; decisions of precedent value
  are mirrored into docs/DECISION_LOG.md.
- Emergency corrections follow the same path with expedited review - never bypassed.

## 14. Validation Rules

A graph release is blocked unless ALL automated checks pass (skips are failures):

1. Schema validity of every record (structure defined in the storage-format decision, HQ-3).
2. ID format and uniqueness; slug format, uniqueness and three-segment rule.
3. Exactly one canonical label per node; label format rules (section 6.3).
4. Domain segment exists in the Domain Registry; exactly one question class per node from
   the class registry.
5. Alias normalisation idempotence and per-locale global uniqueness.
6. Relationship constraints: registry membership, no self-edges, no duplicate triples,
   acyclicity of `REFINES`, `PRECEDES`, `DEPENDS_ON`.
7. Lifecycle legality: only rightward transitions; DEPRECATED targeting rules;
   `SUPERSEDED_BY` sources are DEPRECATED.
8. Referential integrity: every edge endpoint exists; no edge to RETIRED nodes.
9. Translation completeness rules per section 16.
10. Duplicate-detection advisory report generated and attached (section 15).

Adjudicated rules (granularity, domain placement, alias assignment) are spot-audited each
release; the audit sample and findings ship with the release evidence.

## 15. Duplicate Detection Rules

- **Gate 1 (deterministic, blocking):** normalised canonical label and every normalised
  alias of a candidate node are matched against all existing labels/aliases. Any exact
  match blocks creation - the candidate must become an alias, a `REFINES` child, or be
  withdrawn.
- **Gate 2 (advisory, non-blocking):** similarity tooling (choice of tooling: HQ-4)
  produces a ranked near-duplicate report for every REVIEW node. Suggestions never
  auto-merge; a human adjudicates, and the adjudication (accept-as-duplicate /
  distinct-with-rationale) is recorded on the node.
- **The two-way answer test is final:** section 5's granularity rule, applied in writing,
  is the authority when tooling and intuition disagree.
- Periodic whole-graph duplicate sweeps are part of release validation; their reports are
  retained as evidence.

## 16. Translation Strategy

- **Canonical language: English.** Node identity, slugs and canonical labels are English;
  this is an operational anchor, not a product statement.
- Translations attach to nodes as (locale, translated label, translated aliases) using
  BCP-47 locale codes; they carry translator/provenance metadata.
- Translations never create nodes and never participate in identity; alias uniqueness is
  enforced per locale.
- A locale is either **supported** (validation enforces label completeness for all
  CANONICAL nodes) or **partial** (explicitly flagged; no completeness guarantee).
  Initial supported-locale set: HQ-5.
- Back-translation spot checks are part of the release audit for supported locales.

## 17. Extension Policy

- New **nodes**: standard lifecycle; no cap, but every node passes Gates 1-2 and the
  granularity rule.
- New **domains**: registry change with definition and boundary notes; requires owner
  ratification and a decision log entry (domains reshape slugs and ownership).
- New **question classes** and **relationship types**: constitutional amendments - MAJOR
  version, decision log entry, and a written demonstration that no existing registry
  member covers the need.
- New **attributes** on node records: MINOR if optional and non-semantic; MAJOR otherwise.
- Bulk imports (question inventories from any source) enter as PROPOSED batches through
  the same gates - volume never relaxes rules.

## 18. Deprecation Policy

- A node is deprecated when its meaning is superseded, mis-granulated, or wrongly placed -
  never merely unpopular.
- Deprecation requires: rationale, `SUPERSEDED_BY` edge(s) where any replacement exists,
  and a migration note for consumers.
- Deprecated nodes remain resolvable for a minimum of one MAJOR version before RETIRED
  becomes permissible.
- Mass deprecations (>= 20 nodes or an entire domain) additionally require an ADR in
  docs/DECISION_LOG.md.

## 19. Quality Standards

Per node, at CANONICAL: one-sentence canonical label (6.3); a 1-3 sentence **definition**
stating what the question asks and what a complete answer contains; at least the question
class and primary domain assigned; provenance of the concept recorded; zero open
validation findings.

Per release: 100% automated-check pass; duplicate advisory report reviewed; adjudication
audit sample >= 5% of changed nodes; evidence bundle (reports + transcripts) attached per
docs/VALIDATION_STANDARD.md. Style: plain neutral language; no leading, loaded or
culturally exclusionary phrasing in labels; readability of labels at general-audience level.

## 20. Examples (illustrative only - not seed content)

Seven generic examples showing the machinery. Slugs assume illustrative domains from 9.

| Node ID | Slug | Class | Canonical label |
|---|---|---|---|
| HLKG-N-000101 | `career.job_change.timing` | TIMING | "When is a change of job likely to occur?" |
| HLKG-N-000102 | `career.job_change.occurrence` | OCCURRENCE | "Will a change of job occur within the stated horizon?" |
| HLKG-N-000103 | `relationship.partnership.formation_timing` | TIMING | "When is a committed partnership likely to form?" |
| HLKG-N-000104 | `relationship.partnership.stability` | QUALITY | "How stable is the committed partnership expected to be?" |
| HLKG-N-000105 | `residence.relocation.timing` | TIMING | "When is a change of residence likely to occur?" |
| HLKG-N-000106 | `finance.major_purchase.timing` | TIMING | "When is a major planned purchase likely to occur?" |
| HLKG-N-000107 | `career.vocation.direction` | SELECTION | "Which of the declared vocational directions fits best?" |

Machinery illustrations:
- **Alias:** "When will I get a new job?" -> alias of HLKG-N-000101 (normalised, locale `en`).
- **REFINES:** HLKG-N-000102 `REFINES` nothing here, but a node `career.job_change.international_timing` would `REFINES` HLKG-N-000101.
- **DEPENDS_ON:** HLKG-N-000104 `DEPENDS_ON` HLKG-N-000103 (stability presupposes formation).
- **Decomposition:** "When will I move and will it improve my finances?" resolves to
  HLKG-N-000105 + a finance-quality node at query time; it is not a node.
- **Parameterisation:** "Will I relocate before 2030?" = HLKG-N-000105 with a horizon
  parameter, not a new node.

## 21. OPEN QUESTIONS (assumptions refused)

Mirrored into docs/OPEN_QUESTIONS.md on adoption; HQ-numbered to avoid collision with Q1-Q10.

| ID | Question | Blocks |
|---|---|---|
| HQ-1 | Who is the designated HLKG graph owner/adjudicator? | Change management, adjudicated rules |
| HQ-2 | Ratified Domain Registry seed set (names, definitions, boundaries)? | Slug creation beyond illustrations |
| HQ-3 | Storage/serialisation format and schema technology (e.g. JSON Schema vs SHACL/RDF vs relational DDL)? | Validation rule 1, tooling in /tools |
| HQ-4 | Similarity tooling for Gate-2 duplicate detection (and its pinning/versioning)? | Section 15 Gate 2 |
| HQ-5 | Initial supported-locale set and translation provenance requirements? | Section 16 enforcement |
| HQ-6 | Does subject-relation (self vs specified other) ever change node identity, and if so under what recorded test? | Section 5 subject rule edge cases |
| HQ-7 | Quantitative release gates (e.g. maximum advisory-duplicate backlog) beyond binary checks? | Section 19 release bar |

## 22. Change history

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-11 | Initial constitutional framework; no graph content |
