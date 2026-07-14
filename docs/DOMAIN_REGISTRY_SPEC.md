| Field | Value |
|---|---|
| Status | DRAFT - pending owner ratification |
| Version | 0.1.0 |
| Owner | TBD (docs/OPEN_QUESTIONS.md Q1 / HQ-1) |
| Last updated | 2026-07-11 |
| Review cadence | TBD |
| Governed by | docs/HLKG_CONSTITUTION.md (sections 6, 9, 17), docs/PROJECT_CONSTITUTION.md, docs/VALIDATION_STANDARD.md |
| Extends | HLKG Constitution section 9 (Domain Classification); resolves the *shape* of HQ-2, not its population |

# Domain Registry Specification

Governance framework for HLKG Primary Domains. This document defines HOW domains are
created, bounded, changed and retired. It does not populate the registry (population is a
ratification act, HQ-2), contains no question inventory, and no analytical-tradition
content of any kind.

---

## 1. Purpose

The Domain Registry is the single authoritative, versioned list of HLKG Primary Domains
and their boundary definitions. Its job is to make the constitution's rule - *every node
has exactly one Primary Domain* - operable at a scale of thousands of nodes:

1. **Deterministic placement:** any candidate node can be assigned to exactly one domain
   by written rules, reproducibly, by different people.
2. **Stable addressing:** domain slug segments anchor every node slug; the registry
   guarantees those anchors do not drift.
3. **Accountable ownership:** every domain has a named owner responsible for its boundary.
4. **Auditable evolution:** every domain change is versioned, evidenced and reversible in
   history (never in identity).

## 2. Design Principles

1. **One Primary Domain per node** (constitutional; restated here as the registry's prime
   directive). Cross-domain relevance is expressed via node relationships, never dual
   membership.
2. **Flat classification space.** Primary Domains form a flat set for classification
   purposes; any grouping is navigational metadata with zero classification semantics
   (section 12, `parent` field; deeper hierarchy is DQ-2).
3. **Boundaries are written, not intuited.** A domain without explicit Scope, Out-of-Scope
   and boundary notes cannot leave Draft.
4. **Answer-locus rule.** A node belongs to the domain where its *complete answer* lives,
   not where its motivation, cause or consequence lives (inherited from HLKG Constitution
   section 9).
5. **Identity immutability.** Domain IDs and slug segments, once Locked, never change and
   are never reused; evolution happens by supersession.
6. **Small and orthogonal beats large and overlapping.** A new domain must demonstrate
   that no existing domain covers it (section 7); overlap is a defect, not a feature.
7. **Ownership with adjudication.** Domain owners decide placements inside their boundary;
   inter-domain disputes escalate to the registry adjudicator (HQ-1/DQ-4).
8. **Registry changes are graph events.** Every registry change maps to a graph semver
   impact (section 6) and ships with validation evidence.

## 3. Domain Definition Standard

A domain record is complete only with ALL of the following:

| Field | Rule |
|---|---|
| **Domain ID** | `HLKG-D-NNN`, zero-padded, monotonically issued, immutable, never reused |
| **Slug segment** | `[a-z0-9_]`, 2-30 chars, singular, English; immutable once Locked; unique |
| **Domain Name** | Human display name, <= 40 chars; renameable (section 6) |
| **Description** | 1-3 sentences: what life area the domain's questions concern |
| **Scope** | Bulleted positive enumeration of question territories included |
| **Out of Scope** | Bulleted exclusions, each naming the domain that DOES own the excluded territory |
| **Boundary notes** | Written resolutions of known hard cases (minimum 3 at approval; grows over time) |
| **Owner** | Named accountable owner (person/role) |
| **Version** | Domain-record semver (section 6) |
| **Status** | One lifecycle state (section 5) |
| **Provenance** | Origin of the domain proposal + link to its approval decision |

Out-of-Scope entries MUST be reciprocal: if domain A excludes territory T "-> see B",
domain B's Scope must claim T. Validation enforces this (section 7).

## 4. Boundary Rules

**4.1 Placement algorithm (deterministic, applied in order):**
1. Apply the **answer-locus rule**: identify what a complete answer (per the node's
   question class) is *about*; that subject's domain wins.
2. If two domains still claim it, consult both domains' **boundary notes**; a written
   precedent binds.
3. If no precedent exists, the case is an **ambiguity**: it goes to adjudication; the
   ruling MUST be written into the boundary notes of BOTH domains before the node leaves
   REVIEW. Ambiguity resolution therefore permanently shrinks future ambiguity.
4. If adjudication concludes both claims are genuinely correct, the node is
   mis-granulated: decompose it (HLKG Constitution section 5) until each atom has one
   locus.

**4.2 Overlap handling:** discovered Scope overlaps between Locked domains are registry
defects. Remedy: boundary-note precedent (preferred), Scope amendment (MINOR), or - if the
overlap is structural - merge/split per section 6. Overlaps are never resolved by dual
membership.

**4.3 Prohibitions:** no domain may be defined by an analysis method, a data source, or a
demographic; domains are defined only by life-question subject matter.

## 5. Domain Lifecycle

`DRAFT -> REVIEW -> APPROVED -> LOCKED -> DEPRECATED -> RETIRED`

| State | Meaning | Node attachment |
|---|---|---|
| DRAFT | Under authorship; freely editable | Forbidden |
| REVIEW | Frozen candidate under section-7 validation | Forbidden |
| APPROVED | Ratified; slug reserved; provisional operation | PROPOSED/REVIEW nodes only |
| LOCKED | Identity immutable; full production state | All node states |
| DEPRECATED | Closed to new attachments; migration underway | Existing nodes only, pending migration |
| RETIRED | Historical record; zero attached CANONICAL nodes | Forbidden |

Transitions are rightward-only; actor, date, rationale and evidence are recorded per
transition. APPROVED exists deliberately: a domain proves itself on real proposed nodes
before its slug becomes permanent at LOCKED. A DEPRECATED domain is never re-approved; a
successor domain is created instead.

## 6. Domain Versioning

Domain-record semver, with graph-version coupling:

| Change | Domain version | Graph version impact | Rules |
|---|---|---|---|
| Editorial (description wording, added boundary note) | PATCH | PATCH | Review only |
| Scope refinement without node movement | MINOR | MINOR | Owner + reciprocity check |
| Scope change moving existing nodes | MAJOR | MAJOR | Migration map required |
| **Rename** (Display Name) | MINOR | PATCH | Free; slug untouched |
| **Rename** (slug segment) | Prohibited after LOCKED | - | Create successor domain instead |
| **Merge** (A + B -> C) | A,B: DEPRECATED; C: new record | MAJOR | Migration map A->C, B->C; node slugs rewritten under the MAJOR release; Node IDs unchanged |
| **Split** (A -> B + C) | A: DEPRECATED; B,C: new | MAJOR | Every node of A assigned to exactly one successor in the migration map; no orphan, no dual assignment |

Migration maps are machine-readable, shipped with the release, and validated: total
coverage of affected nodes, single target per node, no targets outside APPROVED/LOCKED
domains.

## 7. Domain Validation

A domain passes REVIEW only when ALL checks pass (automated where marked A, adjudicated
where marked J):

1. (A) Record completeness per section 3; ID/slug format and uniqueness.
2. (A) Reciprocity: every Out-of-Scope pointer is claimed by the pointed-to domain's Scope.
3. (A) Slug collision scan against all domains in every state including RETIRED.
4. (J) **Necessity test:** written demonstration that no existing domain's Scope plus a
   boundary note could host the candidate's territory.
5. (J) **Orthogonality test:** the candidate's Scope produces no unresolvable claim
   against any existing Scope for a fixed probe set of sample questions (probe-set size
   and composition: DQ-5). Sample placements are recorded as the domain's first boundary
   notes.
6. (J) Owner assigned and accepted; provenance recorded.
7. (A) Evidence bundle attached per docs/VALIDATION_STANDARD.md (reports, transcripts,
   adjudication records); skips are failures.

## 8. Cross-Domain Rules

1. Domains have **no dependency edges**. There is no domain-level `DEPENDS_ON`; therefore
   domain-level circular dependency is impossible by construction.
2. The only permitted inter-domain link is the symmetric, purely documentary
   `ADJACENT_TO` annotation, which exists solely to require and index shared boundary
   notes between domains with a live boundary (e.g., `career` ADJACENT_TO `finance`). It
   carries no classification or runtime semantics.
3. All semantic cross-domain structure lives at **node level** via the constitutional
   relationship registry (`REFINES`, `PRECEDES`, `DEPENDS_ON`, ...), whose acyclicity is
   already validated there. Domains inherit no edges from their nodes.
4. Consumers MUST NOT infer domain relationships from node relationships; coverage or
   adjacency analytics over node edges are reporting, never registry content.

## 9. Extension Policy

- **New domain:** full lifecycle from DRAFT; passes section 7; ratified by the owner with
  a decision-log entry (constitutional requirement, HLKG Constitution section 17); enters
  APPROVED, and is LOCKED only after it hosts at least one CANONICAL node cohort without
  boundary defects (cohort threshold: DQ-5).
- **Evolving an existing domain:** Scope grows by MINOR amendments with reciprocity
  maintained; hard cases accrete into boundary notes, making the registry more
  deterministic over time, not more complex.
- **Anti-sprawl guard:** the registry targets a small flat set; any proposal taking the
  registry past a ratified ceiling (ceiling value: DQ-3) triggers a mandatory
  consolidation review before approval.
- Bulk domain imports are prohibited; domains enter one at a time, each with its own
  evidence.

## 10. Deprecation Policy

1. Grounds: superseded by merge/split, structurally overlapping, or empty of purpose -
   never mere low usage.
2. Sequence: deprecation decision (ADR) -> migration map published -> nodes migrated under
   a MAJOR graph release (Node IDs stable, slugs rewritten) -> zero-attachment audit ->
   RETIRED no earlier than one MAJOR version after deprecation.
3. During DEPRECATED: no new node attachments; resolution of existing slugs continues via
   the migration map's forwarding table.
4. RETIRED records are preserved forever with their full history; IDs and slug segments
   remain permanently reserved.

## 11. Quality Standards

A domain is official (LOCKED) only when: record 100% complete per section 3; >= 3 boundary
notes at approval and every adjudicated ambiguity since is written back; reciprocity
holds registry-wide; owner active (responds to placement escalations within the SLA -
value DQ-4); zero open validation findings; at least one clean CANONICAL node cohort
hosted; all evidence bundles retained. Language: plain, neutral, non-method, non-
demographic phrasing throughout; every Scope bullet testable against a concrete sample
question.

## 12. Registry Structure

Canonical registry table (one row per domain; machine-readable serialisation format
follows HQ-3):

| Field | Type | Constraints |
|---|---|---|
| `domain_id` | string | `HLKG-D-NNN`; PK; immutable |
| `slug_segment` | string | unique incl. RETIRED; immutable post-LOCKED |
| `name` | string | <= 40 chars; renameable |
| `description` | string | 1-3 sentences |
| `scope` | list | >= 3 bullets |
| `out_of_scope` | list | reciprocal pointers `(territory, domain_id)` |
| `boundary_notes` | list | append-only `(case, ruling, date, adjudicator)` |
| `parent` | string / null | **navigational grouping only; zero classification semantics** (deeper hierarchy: DQ-2) |
| `adjacent_to` | list | symmetric `domain_id` refs (section 8.2) |
| `owner` | string | named person/role |
| `status` | enum | section 5 states |
| `version` | semver | section 6 |
| `provenance` | string | proposal origin + decision link |
| `notes` | string | free text, non-normative |
| `history` | list | append-only transition/change records |

Registry-level invariants (validated every release): PK uniqueness; slug uniqueness;
reciprocity closure; `adjacent_to` symmetry; `parent` (if used) points to a grouping
label, never creates classification paths; append-only fields never shrink.

## 13. Illustrative Examples

**Non-binding examples** (12) showing the record shape at summary level. These are NOT the
ratified seed set (that is HQ-2/DQ-1); IDs are placeholders.

| Domain ID | Slug | Name | Description (abbrev.) | Example Out-of-Scope pointer |
|---|---|---|---|---|
| HLKG-D-001 | `career` | Career | Employment, vocation, professional standing | earnings level -> `finance` |
| HLKG-D-002 | `education` | Education | Formal and informal learning outcomes | career use of a degree -> `career` |
| HLKG-D-003 | `relationship` | Relationship | Committed partnerships and their course | wedding costs -> `finance` |
| HLKG-D-004 | `family` | Family | Parents, children, kinship matters | partner bond itself -> `relationship` |
| HLKG-D-005 | `health` | Health | Physical and mental wellbeing states | treatment costs -> `finance` |
| HLKG-D-006 | `finance` | Finance | Money, assets, obligations | property enjoyment/location -> `property`/`residence` |
| HLKG-D-007 | `property` | Property | Acquisition/disposal of real assets | financing of purchase -> `finance` |
| HLKG-D-008 | `residence` | Residence | Where one lives; relocation | buying the home -> `property` |
| HLKG-D-009 | `travel` | Travel | Temporary journeys, foreign stays | permanent move -> `residence` |
| HLKG-D-010 | `legal` | Legal | Disputes, proceedings, compliance events | dispute's financial recovery -> `finance` |
| HLKG-D-011 | `reputation` | Reputation | Public standing, recognition | professional rank -> `career` |
| HLKG-D-012 | `inner_life` | Inner Life | Meaning, practice, personal development | community role -> `reputation` |

Boundary-note illustration (machinery, not content): *"Will a foreign work posting
occur?"* - answer locus is the posting (employment event) -> `career`; recorded reciprocally
in `career`/`travel`/`residence` notes with the rule "duration-bounded stays -> travel;
open-ended settlement -> residence; the employment event itself -> career."

## 14. OPEN QUESTIONS (assumptions refused)

Mirrored into docs/OPEN_QUESTIONS.md on adoption; DQ-numbered.

| ID | Question | Blocks |
|---|---|---|
| DQ-1 | Ratified seed set of domains (which, how many, exact Scopes) - supersedes/answers HQ-2 | Registry population; any LOCKED domain |
| DQ-2 | Is hierarchical classification ever permitted (semantic `parent`), or is the flat set constitutional forever? | `parent` semantics beyond navigation |
| DQ-3 | Registry size ceiling triggering consolidation review (proposed order of magnitude: tens, not hundreds - value unratified) | Section 9 anti-sprawl guard |
| DQ-4 | Ownership model: single registry adjudicator vs per-domain owners + adjudicator; escalation SLA | Sections 2.7, 4.1, 11 |
| DQ-5 | Quantitative validation parameters: orthogonality probe-set size/composition; LOCK cohort threshold | Sections 7.5, 9 |
| DQ-6 | May LOCKED domains receive editorial description changes without owner ratification, or is every LOCKED-record change gated? | Section 6 editorial row |

## 15. Change history

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-11 | Initial governance framework; registry unpopulated |
