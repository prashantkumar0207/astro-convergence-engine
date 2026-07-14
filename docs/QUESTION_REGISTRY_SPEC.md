| Field | Value |
|---|---|
| Status | DRAFT - pending owner ratification |
| Version | 0.1.0 |
| Owner | TBD (Q1 / HQ-1) |
| Last updated | 2026-07-11 |
| Review cadence | TBD |
| Governed by | docs/HLKG_CONSTITUTION.md, docs/DOMAIN_REGISTRY_SPEC.md, docs/PROJECT_CONSTITUTION.md, docs/VALIDATION_STANDARD.md |
| Position | Constitutional specification of the canonical HLKG Question record. Where this document and the HLKG Constitution could be read to differ, the Constitution governs and this document maps to it explicitly. |

# Question Registry Specification

Defines what a Question **is**: its representation, identity, metadata, classification,
answer contracts, relationships, lifecycle, versioning, validation and governance. It
populates nothing, chooses no technology, and contains no analytical methodology. It is
written to remain valid at 50,000+ questions, multiple methodologies, multiple languages
and multiple storage generations without conceptual change.

---

## 1. Purpose

The Question Registry is the authoritative store of canonical HLKG Questions - the
system's answer to *"what can be asked?"* expressed as governed records.

Relationships to neighbouring artifacts:

| Neighbour | Relationship |
|---|---|
| **HLKG Constitution** | Supreme law: node philosophy, identity rules, class and relationship registries, lifecycle, versioning all originate there. This spec operationalises them at record level. |
| **Domain Registry** | Every Question carries exactly one `primary_domain` that MUST be an APPROVED/LOCKED domain; domain slugs anchor Question slugs; migrations follow the Domain Registry's migration-map machinery. |
| **Translation layer** | Translations and locale aliases attach to Questions (Constitution s.16); this spec fixes where they live in the record and how they validate. |
| **Future engines** | Engines consume Questions read-only through the API contract (s.17) and return answers conforming to the Answer Contract (s.7). Engines never write registry content; the registry never encodes engine logic. Multiple methodologies can answer the same Question because the contract fixes the *shape* of an answer, not its derivation. |

## 2. Design Principles

1. **One Question = One Concept** - the constitutional granularity rule (two-way complete-
   answer test) is the identity criterion.
2. **Atomicity** - composites are decomposed; the registry stores atoms only.
3. **Deterministic identity** - same text + same locale + same graph version resolves to
   the same Question or an explicit NO_MATCH, always.
4. **Machine-readable and human-readable** - every record is fully processable by tools
   and fully understandable by a reviewer without tooling.
5. **Immutable identity** - IDs never change, never get reused; meaning evolves by
   supersession.
6. **Single source of truth** - one record per Question; everything else (translations,
   aliases, annotations) hangs off it; no shadow copies.
7. **Future-proof by neutrality** - no field encodes a methodology, technology or product;
   additions are additive (s.12).
8. **Explainable** - every adjudicated decision (identity, placement, relationship) is
   written on the record it affects.
9. **Version-controlled** - every change is a versioned, auditable event (s.12, s.18).

## 3. What is a Question?

**Formal definition.** A *Question* is the answer-invariant core of a human-life inquiry:
the unique concept that remains after removing phrasing, language, person, tense,
politeness and all quantifiable specifics, such that a complete answer to it (per its
question class) is well-defined. Formally: Q1 = Q2 iff every complete answer to Q1 is
necessarily a complete answer to Q2 and vice versa (HLKG Constitution s.5).

Distinctions (normative):

| Term | Definition | Registry status |
|---|---|---|
| **Question** | Canonical concept as above | Node - owns identity |
| **Query** | A concrete runtime act of asking: (Question ID, parameter bindings, context, locale, graph version) | Never stored in the registry; exists only at consumption time |
| **Alias** | A surface phrasing mapped to exactly one Question in one locale | Attached data; no identity, no lifecycle of its own |
| **Parameter** | A quantifiable specific (horizon, subject, count, named option set) bound at query time | Declared *slots* on the Question; values never in the registry |
| **Context** | Session/user circumstances accompanying a Query | Never registry content (no user data - Constitution s.4) |
| **Composite Question** | User utterance containing >= 2 atomic concepts | Prohibited as a node; decomposed (s.9) |
| **Atomic Question** | A Question that cannot be split without losing a well-defined complete answer | The only storable unit |

## 4. Question Identity

| Element | Rule |
|---|---|
| **Question ID** | `HLKG-N-XXXXXX`, zero-padded monotone integer, registry-issued; primary key; immutable; never reused (capacity 999,999 - see QQ-8 for exhaustion policy). |
| **Canonical Slug** | `domain.topic.aspect` exactly three `snake_case` segments, `[a-z0-9_]`, 2-30 chars each; first segment = an APPROVED/LOCKED domain slug; unique registry-wide including RETIRED; spelling corrections permitted via change management (ID guarantees continuity); domain-segment rewrites occur only through domain migration maps. |
| **Canonical Label** | Exactly one; English; neutral interrogative, subject-neutral or third person; ends `?`; <= 120 chars. |
| **Human Title** | Optional short display name (<= 60 chars) for UI listings; carries no identity; freely editable (PATCH). |
| **Machine identity** | The pair (Question ID, node revision) is the citable machine identity; (Question ID, graph version) pins resolution behaviour. |
| **Uniqueness** | ID unique; slug unique; normalised canonical label unique; every normalised alias unique per locale across the whole graph. |
| **Immutability** | ID always; slug segments post-CANONICAL except via governed migration; class and primary domain changes are semantic events (s.18), never edits. |

## 5. Question Metadata

Field model. Blocks A-C are normative now; block D fields are **reserved**: their slots
exist, their value semantics are deliberately unratified (QQ-2) so that no methodology or
product assumption leaks into the registry.

**Block A - Identity** (s.4): `question_id`, `slug`, `canonical_label`, `human_title`.

**Block B - Classification & structure**

| Field | Purpose | Type | Validation | Req |
|---|---|---|---|---|
| `primary_domain` | Single owning domain | domain_id ref | exists; status APPROVED/LOCKED; equals slug segment 1 | R |
| `question_class` | Answer shape (s.6) | enum | member of class registry | R |
| `parameters` | Declared bindable slots | list of parameter defs (s.8) | each: name, type, required flag, allowed range/set where enumerable | O |
| `relationships` | Typed edges (s.10) | list of (type, target_id, rationale?) | registry types only; constraints s.10 | O |
| `definition` | 1-3 sentences: what is asked, what a complete answer contains | string | non-empty at CANONICAL | R@CANONICAL |

**Block C - Governance & lineage**

| Field | Purpose | Type | Validation | Req |
|---|---|---|---|---|
| `lifecycle_state` | s.11 state | enum | legal transitions only | R |
| `version` | Node revision | integer >= 1 | monotone | R |
| `owner` | Accountable adjudicator/owner | string | non-empty at CANONICAL | R@CANONICAL |
| `source` / `provenance` | Where the concept came from (proposal, import batch, decision link) | string | non-empty | R |
| `created_at` / `modified_at` | Timestamps | ISO-8601 UTC | modified >= created | R |
| `review_status` | Latest review outcome ref | string ref | present at/after REVIEW | R@REVIEW |
| `deprecation` | Rationale + `SUPERSEDED_BY` target(s) + migration note | struct | mandatory iff DEPRECATED | C |
| `history` | Append-only event log | list | never shrinks | R |
| `aliases` | Per-locale surface forms | list of (locale, text, provenance) | normalisation + uniqueness rules | O |
| `translations` | Per-locale labels/definitions | list (s.15) | completeness per supported locale | C |

**Block D - Reserved annotations** (`priority`, `sensitivity`, `predictability`,
`actionability`, `confidence_default`): Purpose - future triage, ethics handling and
engine hints. Type/validation/vocabularies: **unratified; fields MUST remain empty until
QQ-2 is decided.** Defining, e.g., "predictability" today would smuggle methodology
assumptions into a methodology-neutral registry - refused.

## 6. Question Classification

The closed class registry (HLKG Constitution s.8) is adopted verbatim; the class names the
*shape of a complete answer*, never the method:

`TIMING` (when), `OCCURRENCE` (whether, within a horizon), `QUALITY` (how good/stable, on
a declared scale), `SELECTION` (which of declared options), `QUANTITY` (how many/much),
`DESCRIPTION` (what is it like), `CAUSAL` (why / what factors).

Rules: exactly one class per Question; a Question whose honest answer spans two classes is
mis-granulated and MUST be decomposed; classification is validated automatically for
registry membership and adjudicated for fit. **Extension** = constitutional amendment:
MAJOR graph version + ADR + written proof no existing class covers the need (Constitution
s.17). This spec adds no classes and reserves no shadow classes.

## 7. Answer Contract

Implementation-neutral logical contracts. Common envelope for every answer:
`{question_id, node_revision, graph_version, engine_id, engine_version, produced_at,
parameters_bound, payload, confidence?}` - `confidence` semantics are engine-layer and
unstandardised here (QQ-3); the envelope only reserves the slot.

| Class | `payload` contract |
|---|---|
| `TIMING` | **Timeline Object**: ordered list of `{interval_start, interval_end, precision_declared, strength_label?}`; empty list = "not indicated within scope"; granularity claimed MUST NOT exceed `precision_declared`. |
| `OCCURRENCE` | `{value: yes/no/not_established, horizon: {start,end}, qualifier?}` - horizon is mandatory; an occurrence answer without a horizon is malformed. |
| `QUALITY` | **Rating Object**: `{scale_id, scale_definition_ref, value, band?, caveats[]}` - scales are declared artifacts, never implicit numbers. |
| `SELECTION` | `{options_declared[], selected[], ranking?, abstained?}` - selection only among options bound at query time. |
| `QUANTITY` | `{value or range, unit, basis_note}` |
| `DESCRIPTION` | **Structured Narrative**: `{facets: [{facet_name, statement}], summary}` - facet names free but each statement self-contained. |
| `CAUSAL` | `{factors: [{factor, direction, weight_label?}], explanation, counterfactual_note?}` |

Universal rules: `not_established` is a first-class honest outcome in every class; payload
fields never reference methodology internals; contracts version with the graph MAJOR.

## 8. Parameters

Deterministic boundary between concept and specifics:

1. **Parameter test:** if varying a value changes the *answer* but not *what is being
   asked*, it is a parameter. "Relocation before 2030?" and "before 2035?" ask the same
   thing - horizon is a parameter of the relocation-timing/occurrence Questions.
2. Standard parameter kinds: `horizon` (time window), `subject` (self | specified-other -
   identity is bound at query time, never stored), `option_set` (for SELECTION),
   `count/threshold`, `locale-of-answer`. New kinds are MINOR additions.
3. Parameters are **declared** on the Question (name, type, required?, constraints) and
   **bound** only in Queries. Registry stores declarations; never bindings, never values.
4. A parameter MUST NOT change the question class or domain of the Question; if a binding
   would, the case is two Questions (e.g., "when?" vs "will it, before X?" are TIMING vs
   OCCURRENCE - distinct nodes, typically `RELATES_TO`/`REFINES`-linked).
5. Unparameterisable specifics baked into a candidate ("...in <named city>") are
   normalised to a parameter during proposal; refusal to parameterise requires
   adjudication with recorded rationale.

## 9. Composite Questions

- Detection: a candidate containing >= 2 atomic concepts (fails the single complete-answer
  test) is composite. Canonical signal: its honest answer is a conjunction of complete
  answers of different Questions.
- Handling: decompose at intake into constituent atomic Questions; the composite itself is
  **never** created as a node, never given an ID, never aliased.
- "When will I marry and relocate?" -> resolves to the partnership-formation-timing
  Question + the relocation-timing Question as two Query targets; any packaging of the two
  answers is a consumer concern.
- Recurring composites MAY be recorded as **decomposition patterns** (alias-layer routing
  data: composite surface form -> ordered list of Question IDs) - patterns own no identity
  and cannot appear in relationships. Pattern governance parameters: QQ-4.

## 10. Relationships

The constitutional closed registry is adopted verbatim; the brief's vocabulary maps onto
it rather than adding types (adding types = constitutional amendment):

| Brief term | Canonical type | Notes |
|---|---|---|
| Parent / Child | `REFINES` (child REFINES parent) | single hierarchy per pair; acyclic |
| Depends On | `DEPENDS_ON` | acyclic |
| Related | `RELATES_TO` | last resort; written rationale mandatory |
| Excludes | `EXCLUDES` | symmetric |
| Supersedes / Replacement | `SUPERSEDED_BY` | only from DEPRECATED nodes, pointing at replacement(s) |
| (sequence) | `PRECEDES` | acyclic |

Constraints (validated): no self-edges; no duplicate (source, target, type); acyclicity of
`REFINES`/`PRECEDES`/`DEPENDS_ON` each; endpoints exist and are not RETIRED; edges to
DEPRECATED nodes only of type `SUPERSEDED_BY`; every `RELATES_TO` carries rationale.
Relationship changes are semantic events (s.18).

## 11. Lifecycle

**The constitutional node lifecycle governs:** `PROPOSED -> REVIEW -> CANONICAL ->
DEPRECATED -> RETIRED` (HLKG Constitution s.11). The brief's six-state ladder maps as:
Proposal->PROPOSED, Review->REVIEW, **Approved and Locked -> CANONICAL** (the Constitution
defines a single production state for nodes). Whether nodes should gain a provisional
APPROVED sub-state analogous to the Domain Registry's APPROVED/LOCKED pair would be a
constitutional amendment - registered as QQ-1, not assumed here.

Allowed transitions: exactly the four rightward arrows. Forbidden: any leftward move; any
skip except PROPOSED->withdrawn (deletion of a never-reviewed draft is permitted and
logged; anything at/after REVIEW is permanent record); re-canonising a DEPRECATED node
(create a successor instead); RETIRED earlier than one MAJOR version after deprecation.
Each transition records actor, date, rationale, evidence link.

## 12. Versioning

| Layer | Scheme | Meaning |
|---|---|---|
| **Question (node revision)** | integer | increments on ANY record change; (ID, revision) citable |
| **Registry/Graph version** | semver, shared with HLKG graph | MAJOR: meaning-affecting (normalisation fn, class/relationship registries, contract shapes, domain migrations); MINOR: additive (new CANONICAL Questions, aliases, relationships, deprecations, new parameter kinds); PATCH: editorial |
| **Compatibility** | consumers pin a graph version; releases are immutable, checksummed artifacts | a Query is reproducible iff it states its graph version |
| **Migration** | MAJOR releases ship machine-readable maps (old slug -> new slug; deprecated ID -> successor IDs); forwarding tables keep DEPRECATED slugs resolvable through their grace window | maps validated for totality and single-target rules per Domain Registry s.6 |

## 13. Validation

A Question release-gates only when ALL pass (automated A / adjudicated J; skips are
failures per VALIDATION_STANDARD.md):

1. **Identity** (A): ID/slug/label format, uniqueness, slug-domain agreement.
2. **Metadata** (A): required fields per state; types; timestamps; reserved Block-D fields
   empty while QQ-2 open.
3. **Relationship** (A): s.10 constraint set incl. three acyclicity proofs.
4. **Classification** (A+J): registry membership (A); class-fit adjudication sample (J).
5. **Duplicate** (A+J): s.14 gates run and recorded.
6. **Translation** (A): s.15 completeness for supported locales; per-locale alias
   uniqueness; normalisation idempotence.
7. **Lifecycle** (A): legal state, legal history, transition records complete.
8. **Dependency** (A): every `DEPENDS_ON` target CANONICAL; no dependency on DEPRECATED
   except via documented migration window.
9. **Completeness** (A): definition present, parameters well-formed, provenance non-empty,
   adjudication rationales present wherever mandated.

## 14. Duplicate Detection

Adopts the constitutional two-gate design, specified operationally:

1. **Gate 1 - deterministic, blocking** (A): normalise (NFKC, lowercase, whitespace
   collapse, terminal-punctuation strip - the versioned constitutional function) the
   candidate's label and all aliases; exact-match against every existing label/alias in
   every locale. Hit => creation blocked; outcomes: become-alias, become-`REFINES`-child,
   or withdraw.
2. **Gate 2 - similarity, advisory** (A->J): pinned similarity tooling (HQ-4) emits a
   ranked near-duplicate report for every REVIEW node; nothing auto-merges.
3. **Human review** (J): adjudicator applies the two-way complete-answer test in writing.
4. **Decision recording**: outcome (duplicate-of | distinct-because) with rationale is
   written onto BOTH records and is precedent for future intake.
5. **Conflict resolution**: tooling-vs-adjudicator disagreement -> the written granularity
   test is final; adjudicator-vs-adjudicator -> escalation to registry owner; all rulings
   accrete as recorded precedent. Whole-graph sweeps run each release; reports retained.

## 15. Translation Strategy

Adopts Constitution s.16: identity is English-anchored; translations never create nodes.

- Record placement: `translations[] = {locale (BCP-47), label, definition?, provenance,
  translator, reviewed_by?}` and `aliases[]` carry locale.
- Validation: supported locales require 100% CANONICAL-label coverage (A); partial locales
  are flagged and excluded from resolution guarantees; per-locale alias uniqueness is
  global (A); back-translation spot checks per release (J).
- Resolution: a Query declares its locale; matching uses that locale's aliases + labels,
  then English fallback only if the Query permits it (fallback default: QQ-5).
- Initial supported-locale set and translator provenance requirements remain HQ-5.

## 16. Storage Model

Implementation-neutral logical schema (technology selection remains HQ-3):

- **Record structure**: one logical Question record = Identity block + Blocks B/C/D +
  `aliases[]` + `translations[]` + `relationships[]` + `history[]`. Relationships are
  stored on the source record and index-mirrored for reverse lookup; the source record is
  authoritative.
- **Canonical serialisation**: a deterministic canonical form (defined field order, UTF-8,
  stable list ordering rules) exists solely so that record and release **checksums** are
  reproducible; any storage technology must be able to emit it.
- **Append-only zones**: `history[]`, boundary/adjudication rationales, and release
  artifacts never mutate; corrections append.
- **Unknown-field policy**: readers MUST ignore unknown optional fields (forward
  compatibility); writers MUST NOT emit fields outside the ratified schema version.
- **Version compatibility**: each release artifact embeds its graph version + schema
  version; consumers refuse records whose MAJOR exceeds their supported MAJOR.

## 17. API Contract

Logical operations only; transport/auth/implementation out of scope (QQ-6). All
operations are read-only for external systems and version-pinned.

| Operation | Signature (logical) | Guarantees |
|---|---|---|
| `get` | (question_id, graph_version?) -> record | latest revision within pinned version; RETIRED -> gone-with-history |
| `resolve` | (text, locale, graph_version) -> {question_id} \| {question_ids[] via decomposition pattern} \| NO_MATCH | deterministic per (inputs, version); never guesses - NO_MATCH is a contract outcome, thresholds QQ-4/QQ-7 |
| `search` | (terms, filters{domain, class, state}, graph_version) -> ranked list | ranking function versioned so identical inputs give identical order (QQ-7) |
| `translate` | (question_id, locale) -> localized label/definition or explicit UNTRANSLATED | never silent fallback |
| `validate` | (candidate record) -> findings[] | runs s.13 automated checks; advisory for intake tooling |
| `deprecation_lookup` | (question_id \| slug) -> {state, superseded_by[], migration_note, grace_window} | forwarding for DEPRECATED per s.12 |
| `version_lookup` | () -> {graph_version, schema_version, checksums, release_date} | release provenance |

## 18. Change Management

- **Creation**: intake (proposal or bulk batch - batches get no rule relaxations) ->
  PROPOSED -> Gates -> REVIEW -> ratification -> CANONICAL. Every step evidenced.
- **Modification**: editorial (label typo, title, translation) = review-only, PATCH;
  **semantic** (class, domain, parameters, relationships, alias reassignment) =
  adjudication + rationale, MINOR/MAJOR per s.12.
- **Deprecation / Replacement**: rationale + `SUPERSEDED_BY` + migration note; grace >=
  one MAJOR.
- **Merge** (A,B -> C): C created; A,B DEPRECATED with `SUPERSEDED_BY` -> C; aliases of A,B
  re-point to C; answers history unaffected (IDs persist).
- **Split** (A -> B,C): B,C created; A DEPRECATED with `SUPERSEDED_BY` -> both; every alias
  of A adjudicated to exactly one successor.
- **History & audit**: every event appends {actor, timestamp, change type, diff ref,
  rationale, evidence link} to `history[]`; registry-wide change log per release;
  precedent-setting rulings mirrored to docs/DECISION_LOG.md.
- **Approval authority**: owner/adjudicator model per HQ-1/DQ-4.

## 19. Quality Standards

A Question becomes CANONICAL only when: identity complete and collision-free; definition
written (1-3 sentences, states the complete-answer shape); exactly one class and one
APPROVED/LOCKED domain, both adjudication-checked; >= 1 English alias beyond the label
(demonstrates resolvability); parameters declared wherever the concept admits them; all
mandated rationales present; both duplicate gates recorded; zero open validation findings;
provenance and owner set; evidence bundle attached. Label style: plain, neutral,
non-leading, general-audience readability, no cultural exclusivity.

## 20. Registry Invariants

MUST always hold, machine-verified every release:

1. Every Question has exactly one canonical identity (ID, slug, label) - no duplicates
   under normalisation.
2. Every Question has exactly one Primary Domain, and it equals slug segment 1.
3. Every Question has exactly one question class from the closed registry.
4. Aliases never own identity; every alias maps to exactly one Question per locale.
5. Composite questions never become nodes; decomposition patterns never own identity.
6. No cycles in `REFINES`, `PRECEDES`, `DEPENDS_ON`; no self-edges anywhere.
7. IDs and slugs are never reused, including after RETIRED.
8. Lifecycle moves only rightward; nothing at/after REVIEW is ever deleted.
9. `history[]` never shrinks; release artifacts never mutate.
10. Reserved annotation fields stay empty until their semantics are ratified.
11. No record contains user data, methodology logic, or technology bindings.
12. Every semantic change carries a written rationale and appears in the audit trail.
13. A released graph version is immutable and checksum-stable.

## 21. Examples (illustrative only - not seed content)

Twelve generic Questions demonstrating the record machinery (domains from the Domain
Registry's non-binding examples; IDs placeholders):

| ID | Slug | Class | Canonical label | Declared parameters |
|---|---|---|---|---|
| HLKG-N-000201 | `career.job_change.timing` | TIMING | "When is a change of job likely to occur?" | subject, horizon |
| HLKG-N-000202 | `career.job_change.occurrence` | OCCURRENCE | "Will a change of job occur within the stated horizon?" | subject, horizon(required) |
| HLKG-N-000203 | `career.foreign_posting.occurrence` | OCCURRENCE | "Will a work posting abroad occur within the stated horizon?" | subject, horizon(required) |
| HLKG-N-000204 | `relationship.partnership.formation_timing` | TIMING | "When is a committed partnership likely to form?" | subject, horizon |
| HLKG-N-000205 | `relationship.partnership.stability` | QUALITY | "How stable is the committed partnership expected to be?" | subject, scale(declared) |
| HLKG-N-000206 | `family.child.count` | QUANTITY | "How many children are indicated?" | subject |
| HLKG-N-000207 | `residence.relocation.timing` | TIMING | "When is a change of residence likely to occur?" | subject, horizon |
| HLKG-N-000208 | `residence.relocation.destination` | SELECTION | "Which of the declared destinations fits a prospective relocation best?" | subject, option_set(required) |
| HLKG-N-000209 | `finance.major_purchase.timing` | TIMING | "When is a major planned purchase likely to occur?" | subject, horizon |
| HLKG-N-000210 | `health.recovery.timing` | TIMING | "When is recovery from the stated condition likely?" | subject, horizon |
| HLKG-N-000211 | `education.qualification.completion_occurrence` | OCCURRENCE | "Will the stated qualification be completed within the horizon?" | subject, horizon(required) |
| HLKG-N-000212 | `career.vocation.direction` | SELECTION | "Which of the declared vocational directions fits best?" | subject, option_set(required) |

Machinery demonstrations:
- **Alias:** "kab naukri badlegi" (locale `hi`) -> alias of HLKG-N-000201; owns nothing.
- **REFINES:** 000203 `REFINES` 000202 (narrower occurrence).
- **DEPENDS_ON:** 000205 `DEPENDS_ON` 000204.
- **EXCLUDES:** none among these - illustrating that EXCLUDES is rare and never forced.
- **Parameterisation:** "Will I move before 2030?" = 000207's sibling 
  occurrence-Question with horizon bound - and note 000207 (TIMING) vs that OCCURRENCE
  node are *distinct Questions* per s.8 rule 4.
- **Composite:** "When will I marry and relocate?" -> Query targets 000204 + 000207; no node.
- **Answer contract:** an engine answering 000202 must return
  `{value, horizon:{start,end}, qualifier?}` in the envelope - regardless of methodology.

## 22. OPEN QUESTIONS (assumptions refused)

QQ-numbered; mirrored into docs/OPEN_QUESTIONS.md on adoption.

| ID | Question | Blocks |
|---|---|---|
| QQ-1 | Should the node lifecycle gain a provisional APPROVED sub-state (constitutional amendment), or does single-state CANONICAL stand? | s.11 mapping refinement |
| QQ-2 | Semantics, vocabularies and scales for reserved annotations (`priority`, `sensitivity`, `predictability`, `actionability`, `confidence_default`) | Block D activation |
| QQ-3 | Standardised confidence semantics in the answer envelope (scale, calibration duty, cross-engine comparability) | s.7 envelope `confidence` |
| QQ-4 | Decomposition-pattern governance: who ratifies patterns, resolve() multi-target thresholds | s.9, s.17 resolve |
| QQ-5 | Locale fallback default in resolution (English fallback opt-in or opt-out) | s.15, s.17 |
| QQ-6 | API non-functional contract (auth, rate limits, transport, deprecation policy for API versions) | s.17 productionisation |
| QQ-7 | Deterministic search-ranking function and NO_MATCH thresholds (must be versioned artifacts) | s.17 search/resolve |
| QQ-8 | ID-space exhaustion policy beyond 999,999 (widen format vs new series) - far horizon, decide before 500,000 | s.4 capacity |

## 23. Change history

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-11 | Initial constitutional specification; registry unpopulated |
