| Field | Value |
|---|---|
| Status | DRAFT - pending owner ratification |
| Version | 0.1.0 |
| Owner | TBD (Q1 / DQ-4) |
| Last updated | 2026-07-11 |
| Governed by | docs/QUESTION_REGISTRY_SPEC.md s.8, docs/CANONICAL_QUESTION_SCHEMA.md ($defs.parameter), docs/HLKG_CONSTITUTION.md s.5, CAREER_QUESTION_LIBRARY.md v0.1.0, career.questions.json v0.1.0 |
| Repository path | knowledge/hlkg/domains/career/CAREER_PARAMETER_REGISTRY.md |
| Machine verification | Full sweep of career.questions.json: 105 parameter declarations across 61 records reduce to exactly 4 declaration shapes - subject/required (61/61 records), horizon/required (24: all 22 OCCURRENCE + 2 QUANTITY), horizon/optional (18: all TIMING), option_set/required (2: both SELECTION). Zero parameters outside this registry. |

# Career Parameter Registry

Defines every parameter declared by the 61 career Questions: datatype, structure,
validation, allowed values, binding semantics and usage. Parameters are the deterministic
boundary between a Question (stored concept) and a Query (runtime act): **declarations
live in records; values are bound only at query time and are never stored anywhere in the
registry** (QRS s.3/s.8; no-user-data invariant).

## 1. Parameter Model Recap

- A declaration is `{name, kind, required, constraints?}` per the canonical schema.
- The **parameter test** governs membership: if varying a value changes the answer but not
  what is being asked, it is a parameter (QRS s.8.1).
- A binding MUST NOT change the Question's class or domain (s.8.4); bindings that would
  are actually different Questions.
- The schema's closed kind set is {horizon, subject, option_set, count_threshold,
  locale_of_answer}; career v0.1.0 uses the first three. New kinds are schema MINOR
  changes, never ad-hoc.

## 2. Registry Entries

### 2.1 `subject` (kind: subject) - on 61/61 records, always required

| Aspect | Specification |
|---|---|
| Purpose | Whose career the Query concerns. Subject-neutrality of nodes (Constitution s.5) is achieved by carrying the subject here, not in identity. |
| Logical datatype | `subject_ref`: `{relation}` where relation ∈ {`self`, `other`} ; when `other`, an additional `relation_label` from a controlled list (e.g., spouse, child, parent, sibling, friend) - list ratification pending CPR-3. |
| Validation | relation from the enum; `relation_label` required iff relation=`other`; **no identifying data of any person is ever part of the binding passed to the registry layer** - identity resolution is entirely a consumer concern. |
| Allowed values | `self` unconditionally. `other` is **declaration-supported but acceptance-blocked**: whether other-subject career Queries route to Career or to Family is CDQ-4/HQ-6, unresolved. Until ratified, intake MUST reject relation=`other` for career nodes with an explicit NOT_YET_SUPPORTED outcome (a refusal, not a silent remap). |
| Default | None. `subject` is required on every record; an unbound subject is a malformed Query. |
| Usage | All 61 records, all 7 classes. |

### 2.2 `horizon` (kind: horizon) - on 42/61 records (24 required, 18 optional)

| Aspect | Specification |
|---|---|
| Purpose | The time window a Query scopes the answer to. Mandatory for OCCURRENCE (an occurrence answer without a horizon is malformed - Answer Contract) and for windowed QUANTITY; optional scope-narrowing for TIMING. |
| Logical datatype | `time_window`, one of two forms: **absolute** `{start: date, end: date or OPEN}` or **relative** `{from: QUERY_TIME, duration: ISO-8601 duration}` . Dates ISO-8601; timezone semantics: dates are civil dates of the subject's context, resolved by the consumer before binding. |
| Validation | `end > start` (or duration > 0); OPEN end permitted only where the record does not require boundedness; both bounds within the ephemeris-independent sanity range [query_date - 150y, query_date + 150y]; a horizon may not be empty. Mixed forms in one binding are invalid. |
| Allowed values | Any window passing validation. Maximum span deliberately unratified (CPR-1) - no silent cap. |
| Default | None stored. **Absence semantics (optional case, TIMING only):** scope is "within the answering engine's declared maximum scope", and per the Answer Contract the answer MUST state the scope it used - absence never silently means "forever". |
| Usage | Required: all 22 OCCURRENCE + `transition.job_change_count`, `compensation.level_quantity` (QUANTITY). Optional: all 18 TIMING. Not declared on QUALITY/SELECTION/DESCRIPTION/CAUSAL in v0.1.0. |
| Special note | `exit.early_retirement_occurrence` binds horizon as "the stated expected point": the window end IS the expected retirement point the Query declares - the record's definition says so; no extra parameter kind is needed. |

### 2.3 `option_set` (kind: option_set) - on 2/61 records, always required

| Aspect | Specification |
|---|---|
| Purpose | The enumerable choices a SELECTION answer selects among. SELECTION without bound options is malformed (Answer Contract: "selection only among options bound at query time"). |
| Logical datatype | `option_list`: ordered list of `{option_id, label}`; `option_id` opaque, unique within the binding; `label` free text <= 120 chars. |
| Validation | 2 <= count <= cap (cap unratified, CPR-2); option_ids unique; labels pairwise distinct after constitutional normalisation; labels must not embed further questions (an option is a choice, not a sub-query). |
| Allowed values | Consumer-supplied; the registry never stores option content. Answers reference option_ids only. |
| Default | None; required. |
| Usage | `profession.vocation_direction`, `skill.upskilling_direction`. |

### 2.4 Registered kinds unused in career v0.1.0

- **`count_threshold`**: reserved for Questions parameterised by a number ("more than N
  changes...") - no career record needs it; documented so nobody reinvents it ad-hoc.
- **`locale_of_answer`**: reserved for answer-localisation preference; a consumer/API
  concern in current designs (QQ-5), unused at record level.

## 3. Explicit Non-Parameters (common confusions, ruled here)

| Not a parameter | Why | Where it lives |
|---|---|---|
| QUALITY scale | Scales are declared, versioned artifacts referenced by the Answer Contract, not query-varying values | CDQ-5 scale artifacts |
| "the stated business/condition/conflict" context | Referent identification is consumer context accompanying the Query (QRS s.3 Context); the registry never receives it | Consumer layer |
| Engine choice / methodology hints | Reserved annotations, empty until QQ-2 | Block D |
| Dates inside aliases | Prohibited - parameter values never appear in aliases (Alias Registry conventions) | n/a |

## 4. Usage Matrix (machine-generated from career.questions.json)

| Parameter | TIMING (18) | OCCURRENCE (22) | QUALITY (10) | SELECTION (2) | QUANTITY (2) | DESCRIPTION (3) | CAUSAL (4) |
|---|---|---|---|---|---|---|---|
| subject (req) | 18 | 22 | 10 | 2 | 2 | 3 | 4 |
| horizon (req) | - | 22 | - | - | 2 | - | - |
| horizon (opt) | 18 | - | - | - | - | - | - |
| option_set (req) | - | - | - | 2 | - | - | - |

Declaration-shape totals: 105 declarations, exactly 4 shapes, zero outside this registry.

## 5. Binding and Cross-Parameter Rules

1. A Query binds every required parameter or is rejected with a findings list (fail-fast,
   same philosophy as import validation).
2. Unknown parameter names in a binding are rejected (writer-mode symmetry).
3. Bindings are validated before resolution work begins; validation findings cite this
   registry's rules by section.
4. Cross-rule: `option_set` may only be bound to Questions declaring it (SELECTION);
   binding it elsewhere is a class-changing attempt and is rejected per QRS s.8.4.
5. Bindings are never persisted by registry-layer components; consumers own any Query
   logging under their own policies (out of registry scope by the no-user-data invariant).

## 6. OPEN QUESTIONS (assumptions refused)

| ID | Question | Blocks |
|---|---|---|
| CPR-1 | Maximum horizon span (and whether OPEN-ended windows are allowed on OCCURRENCE at all, vs required-bounded) | horizon validation completeness |
| CPR-2 | option_set cardinality cap (proposed order: single digits; value unratified) | option_set validation |
| CPR-3 | Controlled `relation_label` list for subject=`other` (and its locale strategy) | subject datatype completion |
| CPR-4 | Canonical horizon form: are relative durations normalised to absolute windows at binding time (proposed) or preserved? Affects Query reproducibility statements | binding determinism |
| Inherited | CDQ-4/HQ-6 (other-subject routing), CDQ-5 (scales), QQ-5 (answer locale) | as recorded |

## 7. Self-Audit Record

1. Registry built from a machine sweep, not memory: all 105 declarations across 61
   records enumerate to exactly the 4 shapes documented; zero undeclared parameters found
   (header). The sweep is re-runnable against any future records version.
2. The `early_retirement_occurrence` horizon subtlety ("expected point" as window end) was
   initially drafted as a new parameter kind `expected_point` - rejected on review as
   schema creep; the existing horizon kind expresses it, and the record's definition
   already carries the semantics. Precedent recorded.
3. Absence semantics for optional horizon were nearly left implicit ("engine decides") -
   tightened to "engine's declared maximum scope, and the answer must state the scope
   used", keeping determinism without smuggling in methodology.
4. subject=`other` could easily have been silently allowed (the datatype supports it);
   instead acceptance is explicitly blocked pending CDQ-4 with a mandated refusal outcome
   - the registry does not pre-empt an open owner decision.
5. Known limitation: three numeric policy values (CPR-1, CPR-2 caps; CPR-3 list) are
   genuinely unratifiable from here and are left open rather than guessed.
