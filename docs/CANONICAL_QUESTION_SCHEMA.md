| Field | Value |
|---|---|
| Status | DRAFT - pending owner ratification |
| Version | 1.0.0 (schema_version anchor) |
| Owner | TBD (Q1 / HQ-1) |
| Last updated | 2026-07-11 |
| Governed by | docs/QUESTION_REGISTRY_SPEC.md, docs/HLKG_CONSTITUTION.md, docs/DOMAIN_REGISTRY_SPEC.md, docs/VALIDATION_STANDARD.md |
| Companion artifacts | schemas/question.schema.json (normative), schemas/question.schema.yaml (parity copy), examples/question.{minimal,complete,example}.json, examples/question.example.yaml |
| Evidence | Schema validated against the JSON Schema 2020-12 metaschema; all shipped examples machine-validated; six negative cases correctly rejected; JSON/YAML parity machine-verified (generated from one source) |

# Canonical Question Schema

Machine-readable representation of exactly one HLKG Question. Defines structure only - no
methodology, no prediction, no population. Every future API, database, client model,
validation engine, search engine and AI layer derives from this schema; none may extend it
informally.

---

## 1. Canonical Record Philosophy

**One Question, one canonical representation.** The registry's invariants (identity
uniqueness, checksummable releases, deterministic resolution) are only enforceable if a
Question has a single authoritative byte-for-byte reproducible form. Two representations
of one Question would make duplicate detection, audit and checksum verification undecidable.

**Serialization neutrality.** The canonical record is a *logical* object. JSON and YAML
files here are projections of the same logical model (machine-verified identical); a
relational row set, a document, a graph node or an in-memory model are equally valid
projections **iff** they can re-emit the canonical serialization (s.6) losslessly. No
projection is "the database schema" - technology remains unchosen (HQ-3).

## 2. Logical Object Model

| Component | Content | Source of law |
|---|---|---|
| Identity | `question_id`, `slug`, `canonical_label`, `human_title` | QUESTION_REGISTRY_SPEC s.4 |
| Metadata | `primary_domain`, `question_class`, `definition`, governance fields (`owner`, `provenance`, `review_status`, timestamps) | QRS s.5 Blocks B-C |
| Relationships | typed edges, closed registry, per-edge rationale where mandated | HLKG Constitution s.10 |
| Parameters | declared bindable slots (never values) | QRS s.8 |
| Aliases | per-locale surface forms | Constitution s.7 |
| Translations | per-locale labels/definitions with provenance | Constitution s.16 |
| History | append-only event log | QRS s.5/ s.18 |
| Validation hooks | conditional requirements keyed on lifecycle state | QRS s.13 |
| Reserved fields | `reserved_annotations` - present, null-only until QQ-2 | QRS s.5 Block D |
| Deprecation | rationale + successors + migration note, mandatory at DEPRECATED/RETIRED | QRS s.18 |
| Versioning | `schema_version` (this document), `version` (node revision) | QRS s.12 |

## 3. Physical Record

Complete canonical field table. R = required always; R@X = required from state X; C =
conditional; O = optional. Defaults: this schema defines **no implicit defaults** - absent
means absent (s.6); the single normative default is `reserved_annotations` values = null.

| Field | Purpose | Type | Validation | Req |
|---|---|---|---|---|
| `schema_version` | Schema this record conforms to | string | semver pattern | R |
| `question_id` | Immutable PK | string | `^HLKG-N-[0-9]{6}$`; unique (registry) | R |
| `slug` | Human-oriented address | string | 3 segments, `[a-z0-9_]` 2-30 each, no edge underscores; segment 1 = domain slug (registry) | R |
| `canonical_label` | The one English interrogative | string | 6-120 chars, ends `?`; normalised-unique (registry) | R |
| `human_title` | UI display name | string | <= 60 | O |
| `primary_domain` | Owning domain | string | `^HLKG-D-[0-9]{3}$`; APPROVED/LOCKED (registry) | R |
| `question_class` | Answer shape | enum | closed 7-member registry | R |
| `definition` | What is asked; what a complete answer contains | string | 20-600 chars | R@CANONICAL |
| `parameters[]` | Declared slots | array<parameter> | name pattern; kind enum {horizon, subject, option_set, count_threshold, locale_of_answer}; required flag; optional constraints note | O |
| `relationships[]` | Typed edges | array<relationship> | type in closed 6-member registry; target ID pattern; rationale mandatory for RELATES_TO; SUPERSEDED_BY only on DEPRECATED/RETIRED records; acyclicity/endpoint-state checks at registry level | O |
| `aliases[]` | Surface forms | array<alias> | locale (BCP-47 pragmatic pattern), text 2-200, provenance; per-locale global uniqueness (registry) | O |
| `translations[]` | Localised labels | array<translation> | locale, label, provenance, translator required; reviewed_by optional | C (supported locales) |
| `lifecycle_state` | Constitutional state | enum | PROPOSED/REVIEW/CANONICAL/DEPRECATED/RETIRED; rightward-only transitions (registry) | R |
| `version` | Node revision | integer | >= 1, monotone (registry) | R |
| `owner` | Accountable owner | string | non-empty | R@CANONICAL |
| `review_status` | Latest review outcome ref | string | non-empty | R@REVIEW |
| `provenance` | Concept origin | string | non-empty | R |
| `created_at` / `modified_at` | Timestamps | string | RFC 3339 UTC; modified >= created (registry) | R |
| `deprecation` | Supersession record | object | rationale, superseded_by[] (ID pattern), migration_note, deprecated_at | C (DEPRECATED/RETIRED) |
| `history[]` | Audit trail | array<history_event> | >= 1; event enum; actor; timestamp; append-only (registry) | R |
| `reserved_annotations` | QQ-2 placeholders | object | exactly the 5 named keys permitted; every value MUST be null | O |

Sub-object shapes (`parameter`, `relationship`, `alias`, `translation`, `deprecation`,
`history_event`) are normatively defined in the schema's `$defs` - the JSON Schema file is
the byte-level authority; this table is its human projection.

## 4. JSON Schema

Normative artifact: **`schemas/question.schema.json`** - JSON Schema **draft 2020-12**,
metaschema-validated. Design notes:

- `additionalProperties: false` throughout = **writer mode** (s.6 explains reader mode).
- Lifecycle-conditional requirements via `allOf`/`if`/`then`: CANONICAL requires
  `definition` + `owner` + `review_status`; REVIEW and later require `review_status`;
  DEPRECATED/RETIRED require `deprecation`; a `SUPERSEDED_BY` edge forces state in
  {DEPRECATED, RETIRED} (guarded with `required` so the conditional cannot fire vacuously -
  a defect found and fixed by negative testing, see Evidence).
- Reserved annotations are structurally enforced: the five keys exist, each `type: null`.
- What JSON Schema **cannot** express is explicitly delegated to registry-level
  validators and listed in s.7: cross-record uniqueness, domain-status and slug-segment
  agreement, acyclicity, history append-only, timestamp ordering, full BCP-47 validity.

## 5. YAML Representation

**`schemas/question.schema.yaml`** is generated from the identical in-memory definition as
the JSON artifact and machine-verified equal on every regeneration (parity is a build
check, not a promise). YAML exists for human review ergonomics; JSON is the tie-breaker if
the parity check is ever bypassed. Example objects likewise ship in both projections with
round-trip validation.

## 6. Serialization Rules

1. **Encoding:** UTF-8, no BOM. Unicode normalisation for *matching* is the constitutional
   NFKC function; stored text preserves author form.
2. **Canonical form (for checksums):** RFC 8785 (JSON Canonicalization Scheme) applied to
   the record with these array-order preconditions: `parameters` sorted by `name`;
   `relationships` by (`type`,`target`); `aliases` by (`locale`, NFKC(text));
   `translations` by `locale`; `history` in event order (semantic order - never sorted).
3. **Checksums:** SHA-256 over the canonical form; record checksums roll up into the
   release manifest (s.11).
4. **Null handling:** null is never a substitute for absent. The only lawful nulls are
   `reserved_annotations` values.
5. **Empty arrays:** never emitted in canonical form; an optional collection is present
   iff non-empty.
6. **Optional fields:** absent means "not stated"; no reader may invent a default.
7. **Unknown fields:** **writers** MUST NOT emit any (schema enforces); **readers** MUST
   ignore unknown *optional* fields when consuming records whose `schema_version` MINOR is
   newer than their own (forward compatibility), and MUST refuse records with a newer
   MAJOR (backward-compatibility boundary).
8. **Compatibility rule of thumb:** old reader + new MINOR record = works, extras ignored;
   new reader + old record = works, absents respected; MAJOR mismatch = explicit refusal.

## 7. Validation Rules

Two enforcement tiers; both mandatory before release (skips are failures):

**Tier 1 - Schema-expressible (the JSON Schema enforces):** identity formats; enum
membership; lifecycle-conditional requirements; reserved-field nullity; sub-object shapes;
RELATES_TO rationale; SUPERSEDED_BY state coupling; writer-mode field closure.

**Tier 2 - Registry-level validators (cross-record / cross-artifact):** ID, slug and
normalised-label uniqueness incl. RETIRED; per-locale alias uniqueness graph-wide; slug
segment 1 == primary domain's slug segment and domain status APPROVED/LOCKED; relationship
endpoints exist, are not RETIRED, DEPRECATED targets only via SUPERSEDED_BY; acyclicity of
REFINES/PRECEDES/DEPENDS_ON; `modified_at >= created_at`; history append-only vs prior
release; translation completeness for supported locales; duplicate gates run and recorded;
`version` monotonicity; `schema_version` known to the release toolchain.

Lifecycle validation = Tier 1 state legality + Tier 2 transition legality against the
previous release. Reserved-field validation = Tier 1 nullity + Tier 2 "still-reserved"
check against the QQ-2 decision status.

## 8. Example Objects

Shipped and machine-validated (see Evidence header):

- `examples/question.minimal.json` - a lawful PROPOSED record: the 12 always-required
  fields only. Demonstrates that a proposal needs no definition, owner or review status yet.
- `examples/question.complete.json` - a CANONICAL record exercising every component:
  parameters, both rationale-bearing and plain relationships, multi-locale aliases, a
  reviewed translation, null-populated reserved block, four-event history.
- `examples/question.example.json` / `.yaml` - the representative record in both
  projections, round-trip-validated.

All examples are generic life-questions consistent with earlier illustrative IDs; none is
seed content.

## 9. Migration Rules

- **Schema evolution:** `schema_version` semver. MINOR = additive optional fields or new
  enum members in open sets; PATCH = descriptions/constraint tightening that no existing
  valid record violates; MAJOR = anything else (field removal/rename, requiredness
  changes, enum removal, canonical-form changes).
- **Deprecated fields:** never deleted in a MINOR; marked deprecated in `$comment` +this
  document, emitted until the next MAJOR, ignored by new readers.
- **New fields:** enter optional-first; may become required only at a MAJOR with a
  migration script that populates them for the whole registry in one release.
- **Breaking changes:** require an ADR, a machine-readable record-migration map, and a
  dual-emission window of one MAJOR (release carries old+new canonical checksums).
- **Philosophy:** records outlive technologies; every migration is a total function over
  the existing registry, executed and evidenced in one release - never lazy, never partial.

## 10. Import Rules

1. **Intake order (fail-fast, deterministic):** (1) parse; (2) Tier-1 schema validation;
   (3) normalisation; (4) duplicate Gate 1 (blocking exact-match); (5) Tier-2 field/ref
   checks; (6) duplicate Gate 2 advisory report; (7) queue for adjudication.
2. **Temporary IDs:** imports arrive with `question_id` ABSENT and a batch-local
   `provenance` reference; records carrying a canonical-looking ID that the registry did
   not issue are rejected outright.
3. **Canonical ID assignment:** performed solely by the registry issuer at PROPOSED
   creation, monotone, transactional - an ID is burned even if the proposal is later
   withdrawn (never reused).
4. **Failure handling:** any Tier-1 failure rejects the record with the full findings
   list; batch imports are all-or-nothing per record, never per batch (one bad record
   cannot poison a batch, one batch cannot force a bad record through). Every rejection is
   logged with evidence.
5. **Duplicate handling:** Gate-1 hits convert to alias-proposals against the existing
   node by default; the importer may instead withdraw. Gate-2 advisories attach to the
   REVIEW queue - volume never relaxes adjudication (QRS s.17/s.14).

## 11. Export Rules

- **No information loss:** an export is the full canonical record set + registry metadata;
  projections that drop fields must label themselves `partial` and are never re-importable.
- **Stable serialization:** exports emit canonical form (s.6); identical registry state =>
  byte-identical export => identical checksums, machine-verifiable by third parties.
- **Version tagging:** every export embeds `{graph_version, schema_version, release_date}`.
- **Checksums:** per-record SHA-256 + a release manifest (sorted record checksums +
  registry files) with a top-level release checksum; the manifest ships inside the export.

## 12. API Compatibility

Transport-agnostic consumption rules (REST/GraphQL/gRPC/files all conform equally):

- APIs expose the logical operations of QUESTION_REGISTRY_SPEC s.17; every response
  carrying a Question carries it as (a projection of) this canonical record plus the
  triple `{graph_version, schema_version, node_revision}`.
- Partial responses (field selection) are permitted for reads but MUST be labelled partial
  and MUST NOT be re-submittable as records.
- Write paths (intake tooling only) accept candidate records in writer mode - unknown
  fields rejected, Tier-1 enforced at the boundary.
- Pagination/streaming chunking is transport business; record boundaries are inviolable
  (no partial records on the wire).
- API versioning follows the record's compatibility rule: an API MAY serve any
  `schema_version` MINOR within its MAJOR; MAJOR bumps are new API surfaces (non-functional
  contract remains QQ-6).

## 13. Performance Considerations

Technology-neutral obligations at 50,000+ records:

- **Record independence:** every record is self-contained (relationships by ID, not
  embedding), so the registry shards, caches and streams trivially; nothing requires
  whole-graph loading except the Tier-2 global validators.
- **Streaming:** canonical exports are record-streamable (one record = one unit); release
  validation is designed as bounded-memory passes (uniqueness via sorted streams,
  acyclicity via edge lists) rather than resident object graphs.
- **Indexing guidance (non-binding):** resolution needs normalised-alias -> ID and
  normalised-label -> ID maps per locale; search needs class/domain/state filters; both
  derive mechanically from records and are rebuildable, never authoritative.
- **Caching:** releases are immutable + checksummed, therefore infinitely cacheable by
  `graph_version`; only unreleased working state needs invalidation logic.
- **History growth:** `history[]` is unbounded by design (audit beats compactness);
  projections MAY lazily load history - it is never needed for resolution.

## 14. Security Considerations

- **Integrity:** per-record and release checksums (s.6/s.11) make any post-release
  mutation detectable; consumers SHOULD verify the release checksum before trust.
- **Tamper evidence:** append-only `history[]` plus checksum chaining across releases
  (each manifest records its predecessor's checksum) yields a verifiable lineage; a
  rewritten past breaks the chain visibly. (Cryptographic signing of manifests: SQ-3.)
- **Version validation:** consumers refuse unknown MAJOR `schema_version` and unknown
  `graph_version` values - downgrade/confusion attacks fail closed.
- **Content safety:** records contain no user data by invariant; imports are validated,
  never executed - records are inert data everywhere.
- Authentication/authorisation are out of scope here (QQ-6).

## 15. Quality Standards

A Question **object** is production-ready iff: Tier-1 valid in writer mode; Tier-2 clean
in its release run; canonical-form checksum reproduces on independent re-serialization;
all QUESTION_REGISTRY_SPEC s.19 content standards met (definition, adjudication records,
duplicate gates, provenance, owner); shipped inside a release whose manifest checksum
verifies; and its examples/documentation nowhere contradict the four governing documents.
Anything less is a working draft.

## 16. OPEN QUESTIONS (assumptions refused)

SQ-numbered; mirrored into docs/OPEN_QUESTIONS.md on adoption.

| ID | Question | Blocks |
|---|---|---|
| SQ-1 | Adopt RFC 8785 (JCS) as ratified canonicalization, or specify an in-house canonical form? (JCS proposed above as the standard-based default - ratification required since checksum stability is constitutional-grade) | s.6, s.11, M0-style certification of the registry |
| SQ-2 | `$id` URI authority for schemas (namespace/domain ownership) | schema publication |
| SQ-3 | Cryptographic signing of release manifests (key custody, algorithm) beyond checksums | s.14 tamper evidence |
| SQ-4 | Formal machine-readable spec for Tier-2 validators (which language/framework-neutral notation) | tools/ validator build |
| SQ-5 | History compaction policy far-horizon (never vs archival snapshots) - proposed: never compact; requires ratification | s.13 history growth |
| Inherited | HQ-3 (storage tech), QQ-2 (reserved semantics), QQ-6 (API non-functional), QQ-8 (ID capacity) | as before |

## 17. Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-07-11 | Initial canonical schema; JSON+YAML artifacts generated from single source; examples validated; six negative cases verified rejected |
