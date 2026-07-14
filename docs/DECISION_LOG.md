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

# Decision Log (ADR register)

Append-only. Entries are never edited after acceptance; they are superseded by later entries.
Template at the bottom. Numbering: ADR-XXXX, monotonically increasing.

---

## ADR-0001 - Canonical repository structure
- **Date:** 2026-07-11
- **Status:** Accepted
- **Context:** A long-term project needs a stable, minimal top-level layout that separates
  normative documents, deterministic engine code, governed knowledge, non-normative research,
  verification, tooling and product code.
- **Decision:** Adopt exactly these top-level folders: `docs/ engine/ knowledge/ research/
  tests/ tools/ app/`, with dependency rules as recorded in MASTER_ARCHITECTURE.md section 4.
- **Consequences:** New top-level folders require a superseding ADR. All ambiguous
  foundational items are tracked in OPEN_QUESTIONS.md rather than assumed.

---

## ADR-0002 - Foundation additions per M1 repository audit
- **Date:** 2026-07-11
- **Status:** Accepted
- **Context:** External M1 audit (reviewer: ChatGPT) required five additions before M1
  lock: PROJECT_CONSTITUTION.md, /examples, /assets, LICENSE placeholder, SECURITY.md.
  ADR-0001 requires a superseding ADR for any new top-level folder.
- **Decision:** Add top-level `examples/` and `assets/` (illustrative and media layers -
  neither may be a runtime dependency of engine/knowledge/app), add the constitution as
  the highest governing document, add a no-grant LICENSE placeholder pending Q7, and add
  SECURITY.md with contact pending Q1. No existing folder, specification or standard is
  modified.
- **Consequences:** Canonical top-level set is now: docs, engine, knowledge, research,
  tests, tools, app, examples, assets. README layout table extended accordingly.
- **Evidence:** M1_REPOSITORY_AUDIT_FIXES.md (audit input, retained with project records).

---

## ADR template (copy, do not edit above the line)

## ADR-XXXX - <title>
- **Date:** YYYY-MM-DD
- **Status:** Proposed | Accepted | Superseded by ADR-YYYY
- **Context:** <forces, constraints, problem>
- **Decision:** <the binding choice, stated imperatively>
- **Consequences:** <positive, negative, follow-up obligations>
- **Evidence:** <links to validation runs where applicable>
