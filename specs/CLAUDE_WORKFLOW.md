| Field | Value |
|---|---|
| Status | **ACCEPTED - ratified as the ACE agent-workflow specification, `ADR-0016`/`ADR-0051` (owner-ratified 2026-08-17).** Subordinate to the `ADR-0042` authority hierarchy (`PROJECT CONSTITUTION` -> `ENGINEERING CONSTITUTION` -> `DECISION LOG / ADR` -> ... -> `SPECIFICATIONS`); MUST NOT be read as an independent source of authority capable of overriding the Constitution or an accepted ADR. Original substantive content (the six-step per-tier workflow) is unedited by ratification; `ADR-0057` added the two new sections below it (interaction mode, session-start audit) as a narrow CEO-audit remediation - see their own note. |
| Version | 1.2.0 |
| Owner | TBD (docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-18 |
| Review cadence | TBD |

# Claude Implementation Workflow

Claude is an implementation engineer, not the methodology authority or final certification authority.
The four-role model (USER, CLAUDE, CHATGPT, CODEX) is defined in `docs/PROJECT_CONSTITUTION.md` s11
(`ADR-0056`) and is not restated here; this document governs the procedural *how* and *when*, not the
*who*.

For each derived tier:

1. ChatGPT/architecture workflow freezes the methodology specification and output schema.
2. Create a handoff package containing the specification, allowed dependencies, frozen upstream interfaces, fixtures, and explicit prohibited shortcuts.
3. Claude implements code, unit tests, and a manifest without modifying locked upstream tiers.
4. Returned code is audited against the specification.
5. Independent adversarial and untouched holdout tests are run.
6. If evidence passes, version and lock the tier. If it fails, record the defect and run a narrow correction iteration.

Two AI systems agreeing is not evidence of correctness. Executable evidence and independent validation are the judge.

## ACE interaction mode (`ADR-0057`)

For ACE work, ChatGPT's default response mode is **execution/audit first, not generic explanation**:

- An audit request results in an audit being performed, not a description of how one would be performed.
- A review request results in a review being performed.
- "What should Claude do next?" results in the exact Claude instruction, not a list of options.
- Lengthy "we should do X/Y/Z" explanations are given only when the owner explicitly asks for
  explanation - not by default when the requested role (audit, review, next-instruction) can be
  directly performed instead.
- Where the needed evidence already exists in Git or in `reports/AI_HANDOFF_CURRENT.md`, it is used
  directly rather than asking the owner to manually relay Claude's terminal output or responses (the
  owner is not a message courier between Claude and ChatGPT; `docs/PROJECT_CONSTITUTION.md` s11 point 3).
- If execution is genuinely impossible (a concrete capability or permission limitation, not a
  preference), state the blocker briefly and give the exact next action required from the user or
  Claude - do not substitute a long explanation for a blocked action.

## Session-start audit (mandatory)

Before any significant ACE audit, review, or implementation task, establish, in this order:

1. Current branch.
2. Current HEAD SHA.
3. Working-tree state (`git status`; uncommitted or untracked changes).
4. The relevant specification/ADR for the task at hand.
5. `reports/AI_HANDOFF_CURRENT.md` (the canonical Claude -> ChatGPT handoff - read it, do not skip it).
6. The last approved decision bearing on the task (`docs/DECISION_LOG.md`).
7. Any unresolved questions bearing on the task (`docs/OPEN_QUESTIONS.md`).

**Never infer approval.** A prior session's conclusion, a stale handoff snapshot, or the mere existence
of a `DRAFT`/`PROPOSED` document is not itself authorization; re-verify against git and the decision log
before treating anything as settled, per `CLAUDE.md`'s "Before modifying anything" section, which this
codifies as a permanent, shared rule rather than tooling-specific habit.

## Change history
| Version | Date | Change |
|---|---|---|
| 1.2.0 | 2026-08-18 | `ADR-0057` (narrow CEO-audit remediation): added "ACE interaction mode" (ChatGPT execution/audit-first response mode) and "Session-start audit (mandatory)" (the shared branch/HEAD/working-tree/spec/handoff/decision/open-questions checklist, binding both AI collaborators, not only Claude's own tooling habit). Original six-step per-tier workflow and its "two AI systems agreeing is not evidence" line are unedited. |
| 1.1.0 | 2026-08-17 | `ADR-0051`: owner-ratified as the ACE agent-workflow specification, subordinate to the `ADR-0042` hierarchy. Substantive content unchanged. |
| 1.0.0 | 2026-08-17 | G7 documentation repair (`docs/Q8_CLOSURE_MATRIX.md` s3): added the mandatory status header required by `docs/DOCUMENTATION_STANDARD.md` s2, previously missing entirely. Substantive content unchanged. |
