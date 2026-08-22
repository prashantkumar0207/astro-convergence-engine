| Field | Value |
|---|---|
| Status | DRAFT - pending owner ratification |
| Version | 0.1.2 |
| Owner | TBD (docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-18 |
| Review cadence | TBD |

# Project Constitution

The highest-level governing document. Where this constitution and any other document
conflict, the constitution governs; changes to it require a decision log entry and owner
ratification.

## 1. Project Vision
TBD - owner ratification required (docs/OPEN_QUESTIONS.md Q5). Deliberately not invented.

## 2. Mission
TBD - owner ratification required (Q5).

## 3. Core Principles
1. **Evidence over narrative.** Nothing is true in this project because a document says so;
   it is true because a reproducible run proves it.
2. **Decisions over assumptions.** Ambiguity is registered (OPEN_QUESTIONS.md) and decided
   by the owner, never silently resolved.
3. **Determinism.** Same inputs, same versions, same outputs - bit-for-bit where achievable.
4. **Separation of concerns.** Calculation, knowledge, research and product never blur.
5. **Longevity.** Every choice is made for a 10+ year maintenance horizon: boring
   technology, pinned versions, portable paths, written reasons.

## 4. Scope
TBD - bound to the ratified mission (Q5). Until ratified, only foundation work (structure,
standards, certification tooling) is in scope.

## 5. Non-Goals
Standing non-goals (independent of Q5):
- No unvalidated claims of accuracy, ever, in any artifact.
- No business/domain logic without a ratified specification.
- No dependency on any single machine, person, or unstated configuration.

## 6. Project Philosophy
Build a small, certified, immutable core; grow outward through governed layers; let
research explore freely but promote nothing without evidence. Slow is smooth; smooth is fast.

## 7. Repository as Source of Truth
The repository is the single authoritative record: code, specifications, decisions,
evidence. Anything not in the repository (chats, screenshots, memories, private notes) is
input material, not truth. External claims enter only through fixtures or decision entries.

## 8. Engineering Principles
- Frozen profiles: behaviour-affecting configuration is versioned and immutable per version.
- Loud failure: degraded modes must be impossible to miss in certification contexts.
- Portability: repository-relative paths only; pinned dependencies; checksummed data assets.
- Boundary rigour: interval/threshold logic is tested below/at/above every boundary.
- One-command reproducibility for every gate that matters.

## 9. Documentation Philosophy
Documents are code: status headers, versioned changes, review, and the TBD-requires-a-
registered-question rule (docs/DOCUMENTATION_STANDARD.md governs mechanics).

## 10. Validation Philosophy
Independent references, untouched holdouts, skips-are-failures, anti-fitting scans,
stored-results-are-history-not-proof (docs/VALIDATION_STANDARD.md governs mechanics).

## 11. AI Collaboration Model
*Status note (G7 repair, `docs/Q8_CLOSURE_MATRIX.md` s3): this document is still `DRAFT` while
`engineering/ENGINEERING_CONSTITUTION.md` carries `Status: ACTIVE` - a subordinate document should not
read as more settled than the one that governs it. `ADR-0042` (`docs/DECISION_LOG.md`) ratified the
authority hierarchy **OWNER -> PROJECT CONSTITUTION -> ENGINEERING CONSTITUTION -> ...**, so this
document governs `engineering/ENGINEERING_CONSTITUTION.md` regardless of either document's own status
label. `ADR-0042` ratifies the *hierarchy*, not this constitution's own content, which remains
unratified pending Q5 (`docs/OPEN_QUESTIONS.md`).*

*Status note (`ADR-0056`, 2026-08-18): the role model below formalizes, on explicit owner instruction,
the two-AI prose this section previously carried. The four roles restate and sharpen what was already
true (builder/executor, reviewer/auditor, owner ratification); rules (a)-(d) at the end are unchanged
and remain the governing principles the roles below operationalize.*

Four parties operate under human ownership. **Git - this repository's commits, tests, certification
artifacts, and governance records - is the single source of truth for all of them** (section 7).
Conversation text with any AI collaborator is input material, never authoritative project memory,
however detailed or confident.

1. **USER - product owner, final ratifying authority.** Significant architectural, certification,
   phase, and governance decisions require the user's approval wherever this constitution or
   `docs/DECISION_LOG.md` requires it. No AI collaborator ratifies on the user's behalf.
2. **CLAUDE - the primary and sole ACE builder/executor.** All ACE coding, repository editing, test
   execution, certification execution, and commits are performed by Claude. Claude implements, runs,
   measures, and returns executable evidence; it never accepts its own prior output as proof. Claude
   updates the canonical Claude -> ChatGPT handoff (`reports/AI_HANDOFF_CURRENT.md`, or its successor
   only if a future decision entry renames it) after every meaningful implementation task, and must
   not create a competing handoff mechanism.
3. **CHATGPT - independent ACE CEO / technical auditor.** Reviews Claude's work independently: audits
   architecture, specifications, governance, code, tests, certification evidence, provenance, and
   claims; determines PASS / HOLD / FAIL; and, when remediation is required, provides the exact next
   action/instruction for Claude. ChatGPT is **not** an ACE implementation/builder and does not commit
   to this repository. ChatGPT must not require the user to manually relay Claude's terminal output or
   responses when the needed evidence already exists in Git or the canonical handoff - the expected
   audit path is Git -> current branch/commit -> canonical handoff -> actual diff/code -> tests ->
   certification artifacts -> governance records, not the user acting as message courier between the
   two AI collaborators.
4. **CODEX - not part of the ACE workflow.** ACE implementation is Claude's; ACE auditing is ChatGPT's.
   No third AI worker is introduced into ACE building or auditing under this section. This exclusion
   holds unless the user explicitly changes the ACE workflow in a future decision entry.

Rules (unchanged, read together with the four roles above): (a) the human owner ratifies all
decisions - AI output is proposal, not authority; (b) audit findings are verified against the artifact,
not trusted; (c) each iteration is narrow, evidenced, and recorded; (d) neither AI may weaken targets or
redefine "done".

## 12. Definition of "Locked"
An artifact is **Locked** only when ALL hold:
1. A written specification or frozen profile exists for it.
2. A reproducible verification run passes per VALIDATION_STANDARD.md (fresh environment,
   one command, zero skips, independent reference where applicable).
3. Machine-readable results and a human-readable report were generated by that same run
   and agree exactly.
4. A decision log entry records the lock, its version, and its evidence.
Anything short of all four is, at most, "reported" - and must be labelled so.

## 13. Milestone Workflow
1. Milestone defined with explicit entry/exit criteria (PROJECT_ROADMAP.md).
2. Build in narrow iterations; every claim carries evidence.
3. Independent audit (reviewer AI and/or owner) against the exit criteria.
4. Correction iterations: narrow, scoped, no redesign.
5. Lock per section 12; record ADR; tag/release per versioning policy (Q3).

## 14. Future Expansion Principles
- New top-level structure requires a superseding ADR (see ADR-0001/0002).
- New domains enter as specifications first, code second, claims last.
- Backwards compatibility of published contracts is the default; breaking changes require
  a major version and a migration note.
- The constitution itself may grow, but sections 3, 5, 8, 10 and 12 may only be
  strengthened, never weakened.

## 15. Change history
| Version | Date | Change |
|---|---|---|
| 0.1.2 | 2026-08-18 | `ADR-0056`: formalized s11's AI Collaboration Model into an explicit four-role structure (USER, CLAUDE, CHATGPT, CODEX), stated Git as the single source of truth for all AI collaborators, and excluded Codex from the ACE workflow unless a future decision entry changes it. Rules (a)-(d) unchanged; the roles operationalize them, do not replace them. |
| 0.1.1 | 2026-08-17 | G7 documentation repair (`docs/Q8_CLOSURE_MATRIX.md` s3): added a status-precedence cross-reference note to s11 citing `ADR-0042`'s authority hierarchy, so this document's own `DRAFT` status is not misread against `engineering/ENGINEERING_CONSTITUTION.md`'s `ACTIVE` status. No substantive content changed. |
| 0.1.0 | 2026-07-11 | Initial constitution (vision/mission/scope pending Q5) |
