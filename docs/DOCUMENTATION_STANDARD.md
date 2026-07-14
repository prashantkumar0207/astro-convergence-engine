<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | DRAFT - placeholder skeleton, content pending |
| Version | 0.1.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-07-11 |
| Review cadence | TBD |

# Documentation Standard

## 1. Document classes
| Class | Location | Authority | Review |
|---|---|---|---|
| Governing (architecture, specs, standards, roadmap, decisions) | `docs/` | Normative | PR + named reviewer |
| Component docs (README.md per folder/module) | co-located | Descriptive | PR |
| Research notes | `research/` | Non-normative | lightweight |

## 2. Mandatory structure for governing documents
1. Status header table: Status, Version, Owner, Last updated, Review cadence.
2. Numbered sections; one purpose per document.
3. `TBD` allowed **only** with a matching entry in OPEN_QUESTIONS.md.
4. Change history table at the bottom; semantic versioning of documents (MAJOR = meaning
   change, MINOR = additive, PATCH = editorial).

## 3. Style rules
- Plain, direct professional language; no filler.
- Every normative statement uses MUST/SHOULD/MAY (RFC 2119 sense).
- Claims link evidence (VALIDATION_STANDARD.md); no adjectives in place of numbers.
- Diagrams: source-controlled text formats preferred (Mermaid/PlantUML); binary images only
  with committed source.
- File names: UPPER_SNAKE for governing docs, README.md elsewhere.

## 4. Lifecycle
DRAFT -> REVIEW -> RATIFIED -> SUPERSEDED. Status transitions require PR review; RATIFIED
documents change only alongside a decision log entry.

## 5. Change history
| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-11 | Skeleton created |
