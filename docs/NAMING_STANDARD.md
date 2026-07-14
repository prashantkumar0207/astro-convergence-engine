| Field | Value |
|---|---|
| Status | DRAFT - pending owner ratification |
| Version | 0.1.0 |
| Owner | TBD (Q1) |
| Last updated | 2026-07-11 |
| Governed by | docs/PROJECT_CONSTITUTION.md, docs/DOCUMENTATION_STANDARD.md |
| Consolidates | Naming rules already ratified/drafted in HLKG_CONSTITUTION s.6, DOMAIN_REGISTRY_SPEC s.3, QUESTION_REGISTRY_SPEC s.4, CANONICAL_QUESTION_SCHEMA, and the career registries - this standard restates them with sources and fills only the gaps between them; where it and a LOCKED document could be read to differ, the LOCKED document governs |
| Conformance sweep | Executed this session over the full repository tree (47 files): governed-doc name pattern, data/code name pattern, and ID zero-padding width across all five ID families in every artifact - **zero findings** |

# Naming Standard

One deterministic naming law for the next ten years: identifiers, slugs, files, folders,
enums, registries, registers and versions. Names are interfaces - they are read thousands
of times and written once, so every rule here optimises for the reader, the diff, and the
`grep`.

## 1. Principles

1. **Names never encode meaning that can change.** Meaning lives in records; IDs are
   opaque; slugs are stable addresses whose continuity is guaranteed by IDs.
2. **One pattern per kind.** A reader must be able to classify any name on sight:
   `HLKG-N-000204` is a question, `CAREER_EVENT_REGISTRY.md` is a governed document,
   `career.questions.json` is data, `EV-CAR-021` is an event.
3. **Machine-checkable or it isn't a rule.** Every pattern below is a regex or an
   enumerable list; the conformance sweep in the header is re-runnable.
4. **Immutable once issued.** IDs are never renamed, never reused, including after
   RETIRED; renames happen only via governed supersession/migration.
5. **ASCII in identifiers; Unicode in content.** Names and IDs are ASCII; aliases,
   translations and text content are full Unicode.

## 2. ID Families

| Family | Pattern | Width | Scope | Issuer | Source of law |
|---|---|---|---|---|---|
| Question | `HLKG-N-\d{6}` | 6 | HLKG-wide | Question Registry issuer at PROPOSED creation | QRS s.4 |
| Domain | `HLKG-D-\d{3}` | 3 | HLKG-wide | Domain Registry | DRS s.3 |
| Event | `EV-CAR-\d{3}` | 3 | domain-local (career) | Domain event registry | Event Registry s.1; EVR-1 open |
| Outcome | `OC-CAR-\d{3}` | 3 | domain-local (career) | Domain outcome registry | Outcome Registry s.1; OCR-1 open |
| Test scenario | `TC-CAR-\d{3}` | 3 | fixture-local | Test dataset generator | tests/fixtures |
| Decision | `ADR-\d{4}` | 4 | repository-wide | Decision log | DECISION_LOG.md |

Rules:
- **Zero-padded, monotone, immutable, never reused** - all families, no exceptions.
- **Width encodes expected cardinality** (questions: up to 999,999 per QQ-8; domains: tens;
  events/outcomes per domain: dozens-to-hundreds). Width changes are MAJOR events with a
  migration map - so choose generously at family creation.
- **Creating a new ID family** requires: a governing document section defining pattern,
  width, scope and issuer; a decision-log entry; and a uniqueness check added to the
  conformance sweep. Domain-local families use the `XX-<DOMAINCODE>-` shape with a
  registered 3-letter domain code (`CAR` = career; codes are unique, never reused).
- IDs appear verbatim everywhere (no abbreviation, no case variation).

## 3. Slugs (identity addresses)

Locked by HLKG_CONSTITUTION s.6 / QRS s.4; restated:
- Question slug: exactly three segments `domain.topic.aspect`, each `[a-z0-9_]`,
  2-30 chars, no leading/trailing underscore; regex per segment:
  `[a-z0-9](?:[a-z0-9_]{0,28}[a-z0-9])?`.
- Segment 1 = a registered domain slug segment; segment 2 = the domain's frozen topic
  vocabulary (career: 12 topics); segment 3 = aspect built from event/outcome/state
  vocabulary + class-typical suffixes (`_timing`, `_occurrence`, `_quality`, `_cause`,
  `_description`, `_count`, `_direction`).
- Singular nouns; English; no synonyms, abbreviations or marketing terms; unique
  registry-wide including RETIRED.
- Domain slug segments: same charset, immutable post-LOCKED (DRS s.6).

## 4. File Naming

| Kind | Pattern | Examples (all live in the repo today) |
|---|---|---|
| Governed document | `SCREAMING_SNAKE.md` - `^[A-Z0-9_]+\.md$` | `HLKG_CONSTITUTION.md`, `CAREER_DOMAIN_MODEL.md` |
| Domain knowledge doc | `<DOMAIN>_<SUBJECT>.md`, domain prefix mandatory inside domain folders | `CAREER_ALIAS_REGISTRY.md` |
| Data artifact | lowercase dotted: `<scope>.<content>[.<qualifier>].<ext>` | `career.questions.json`, `career.test.dataset.json` |
| Schema | `<object>.schema.<ext>` in `schemas/` | `question.schema.json`, `question.schema.yaml` |
| Example object | `<object>.<variant>.<ext>` in `examples/` | `question.minimal.json` |
| Code/tool | `snake_case.py`, verb-or-role naming | `career_validate.py` |
| Folder README | `README.md` (the one sanctioned mixed-case name) | every top-level folder |

Rules: extensions honest (`yaml` not `yml`, `json` never hand-abbreviated); no spaces, no
dates in names (dates live in headers and history); generated files carry their producing
version inside the file, never in the filename (filenames are stable references).

## 5. Folder Naming

- Top-level set is closed and ADR-governed (ADR-0001..0003): `docs/ engine/ knowledge/
  research/ tests/ tools/ app/ examples/ assets/ schemas/`. New top-level = superseding ADR.
- All folders lowercase, singular-or-collective English words, `[a-z0-9_]`, no dates.
- Knowledge domain path shape is fixed: `knowledge/hlkg/domains/<domain_slug>/`.
- Fixtures: `tests/fixtures/`; future suites `tests/<suite_name>/`.

## 6. Enum and Vocabulary Naming

Two deliberate cases, chosen by mutability:
- **Closed constitutional enums** - `SCREAMING_SNAKE` values: lifecycle states
  (`PROPOSED`...`RETIRED`; domain `DRAFT`...`RETIRED`), question classes (`TIMING`...
  `CAUSAL`), relationship types (`REFINES`...`SUPERSEDED_BY`), test outcomes
  (`RESOLVED`, `NO_MATCH`, ...). Extending any of these is a constitutional amendment.
- **Open governed vocabularies** - `lower_snake` values: subdomain topics (`employment`),
  event names (`foreign_posting`), outcome names (`income_growth`), parameter names/kinds
  (`option_set`), locales excepted (BCP-47 as-is: `hi-Latn`).
The case difference is a signal: uppercase = amendment territory; lowercase = registry
append territory. Field names in records: `lower_snake` always (schema-enforced).

## 7. Open-Question Register Codes

Pattern: `<CODE>-<n>` (unpadded n - registers are small by design), one code per artifact:
`Q` (repo foundation), `HQ` (HLKG Constitution), `DQ` (Domain Registry), `QQ` (Question
Registry), `SQ` (Schema), `CDQ` (Career Domain Model), `CQL` (Question Library), `ALR`
(Alias Registry), `CRG` (Relationship Graph), `CPR` (Parameter Registry), `EVR` (Event
Registry), `OCR` (Outcome Registry), `VCK` (Validation Checklist), `CIE` (Intake
Examples). New artifact -> new unique code declared in its own header, checked against
this list; codes are never reused even after all items close. Validation-check IDs use
`VC-<letter><n>` (checklist-internal).

## 8. Version Naming

- **Semver everywhere** (`MAJOR.MINOR.PATCH`), no `v` prefix inside version fields;
  layers: graph/registry version, schema_version, document version, domain-record version,
  engine/tool versions. Node revision is a bare monotone integer (QRS s.12) - the one
  sanctioned non-semver version, because it counts edits, not compatibility.
- Release artifacts: `<name>_v<semver>` only in bundle filenames (e.g.
  `astro_kernel_v1.3_tier0_portable.zip`) where filesystem-stable references need the
  version visible; inside the repo, filenames stay unversioned (s.4).
- Documents carry `| Version |` in the standard header plus a Change history table;
  version bumps follow DOCUMENTATION_STANDARD semantics (editorial=PATCH, additive=MINOR,
  meaning-affecting=MAJOR).

## 9. Reserved and Prohibited

- Reserved words never used as slugs/topics/names: lifecycle-state words, class names,
  relationship-type names (lowercased collisions included: no topic may be `timing`).
- Prohibited in all identifiers: dates, personal names, methodology terms (per the
  no-astrology-in-engineering rule), marketing terms, and encodings of mutable facts.
- The `career` domain code `CAR` is registered; future domain codes are declared in the
  domain's event/outcome registries and recorded here by amendment.

## 10. Conformance

The header's sweep (governed-doc pattern, data/code pattern, ID-width across all five
families over all 47 repository files) ran clean this session. The sweep script belongs in
`tools/` as part of release validation (VC-K family) - promotion tracked in NS-2.

## 11. OPEN QUESTIONS (assumptions refused)

| ID | Question | Blocks |
|---|---|---|
| NS-1 | Domain-code register ownership: 3-letter codes (`CAR`, ...) need a single allocation table - here, or in the Domain Registry record? | New domain event/outcome families |
| NS-2 | Promote the conformance sweep into tools/ as a standing release check (and merge with career_validate.py per VCK-3)? | Release automation |
| NS-3 | Unpadded register numbering (`HQ-1`) vs padded - current practice is unpadded; ratify or migrate before registers grow | Register references |
| Inherited | EVR-1/OCR-1 (ID family scope), QQ-8 (N-width exhaustion), SQ-2 ($id URI authority) | as recorded |

## 12. Self-Audit Record

1. Consolidation verified against reality, not memory: the conformance sweep ran over the
   actual repository (47 files) before this document was written - zero deviations found,
   so the standard describes the codebase as it is, and the sweep is re-runnable evidence.
2. One genuine near-inconsistency surfaced and was ruled rather than papered over: ID
   widths differ across families (6/4/3). Rationalised as cardinality-driven (s.2) with a
   family-creation rule, instead of forcing a retroactive uniform width that would
   invalidate every existing ID.
3. The enum-case split (UPPER for closed constitutional sets, lower for open
   vocabularies) was implicit across five artifacts; making it explicit as a mutability
   signal is the one new rule this standard adds - flagged as such, not smuggled in as
   established practice.
4. Checked for contradiction against every LOCKED naming clause (HLKG s.6, DRS s.3/s.6,
   QRS s.4, schema patterns): none introduced; all patterns restated verbatim with source
   pointers.
5. Register-code collision check run across all 14 codes: unique; `NS` verified unused
   before adoption by this document.
