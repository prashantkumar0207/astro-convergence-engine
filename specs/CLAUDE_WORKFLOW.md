| Field | Value |
|---|---|
| Status | **ACCEPTED - ratified as the ACE agent-workflow specification, `ADR-0016`/`ADR-0051` (owner-ratified 2026-08-17).** Subordinate to the `ADR-0042` authority hierarchy (`PROJECT CONSTITUTION` -> `ENGINEERING CONSTITUTION` -> `DECISION LOG / ADR` -> ... -> `SPECIFICATIONS`); MUST NOT be read as an independent source of authority capable of overriding the Constitution or an accepted ADR. Original substantive content (the six-step per-tier workflow) is unedited by ratification; `ADR-0057` added the interaction-mode/session-start-audit sections; `ADR-0058` added "Execution continuity" below it; `ADR-0062` added "Execution-state recovery" below that - all narrow, additive remediations, see their own notes. |
| Version | 1.4.0 |
| Owner | TBD (docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-20 |
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

## Execution continuity (`ADR-0058`): do not stop prematurely

For ACE tasks, do not stop after giving an analysis, recommendation, partial result, or list of possible
next actions. Continue executing the authorized workflow step by step until one of these five terminal
conditions actually occurs:

1. **USER INPUT REQUIRED** - a genuine decision, approval, credential, file, command output, or other
   user action is needed and nothing else can substitute for it.
2. **CLAUDE INPUT REQUIRED** - the next step is implementation/research/execution ChatGPT cannot itself
   perform. Give Claude the complete next execution instruction (repository context, objective,
   constraints, required checks, expected output, and the handoff-update requirement), not merely a
   description of what should happen. If the next step is already obvious from repository governance
   and the current authorized milestone, issue it - do not stop to ask "what next?" first.
3. **BLOCKED** - a genuine external/environmental limitation prevents progress (a missing credential, an
   unreachable service, a platform limitation already documented elsewhere in this repository). State
   the precise blocker and the exact unblock action; do not re-explain a blocker already stated.
4. **CEO APPROVAL REQUIRED** - a governance or certification checkpoint requires explicit user/CEO
   approval under existing rules (`docs/PROJECT_CONSTITUTION.md` s11 rule (a); `.claude/rules/*.md`).
5. **TASK COMPLETE** - all authorized work and its required verification are actually finished.

Outside those five, do not stop. Never end a response with "you should do X" when X can instead be
issued as the next executable instruction. Never re-ask for confirmation of a step already authorized.
Never restart or re-explain completed work unless resolving an actual contradiction requires it. Every
iteration must materially advance the current milestone, not repeat established context.

This section governs response *behaviour* (when to stop vs. continue); it does not itself authorize any
work that repository governance has not already authorized, and it does not weaken `docs/
PROJECT_CONSTITUTION.md` s11 rule (a) - the owner still ratifies all decisions, and condition 4 above is
not overridden by the general "keep going" instruction.

## Execution-state recovery (`ADR-0062`): repository state, not conversational memory

**Repository state is authoritative for reconstructing ACE's current execution state.** Neither AI
collaborator's conversational memory is required, or reliable, for this - a fresh ChatGPT session and a
fresh Claude session must each be able to determine exactly where ACE stands from the repository alone,
per `docs/PROJECT_CONSTITUTION.md` s7 and s11 point 3 (already ratified, `ADR-0056`; not reopened here -
this section operationalizes it).

- **`docs/ACE_EXECUTION_STATE.md`** is the canonical current-state record: one overwritten snapshot
  (`CURRENT_PHASE`, `CURRENT_MILESTONE`, `STATUS`, `WAITING_FOR`, `CEO_APPROVAL_REQUIRED`, and the other
  fields it defines), not a history. Read it first when resuming ACE work cold.
- **`reports/AI_HANDOFF_CURRENT.md`** remains the detailed, append-only, task-by-task LLM handoff log -
  unchanged in role by this section.
- **`docs/DECISION_LOG.md` (ADRs) and `docs/decisions/*` (DPs)** remain the normative decision authority;
  neither state file outranks or substitutes for a decision entry.
- **Git and CI remain evidential truth.** Both state files are pointers into git/CI, never a replacement
  for reading the actual commit, diff, test run, or certification artifact they name.
- **The USER is a decision/approval boundary, not a report-transfer layer.** A permanent, explicit rule,
  sharpening `docs/PROJECT_CONSTITUTION.md` s11 point 3's already-ratified language into an unconditional
  prohibition:

  > **Never ask the user to copy/paste Claude's execution report to ChatGPT, or ChatGPT's findings to
  > Claude.** Claude persists the necessary state in `docs/ACE_EXECUTION_STATE.md` and
  > `reports/AI_HANDOFF_CURRENT.md` before stopping. ChatGPT recovers state from the repository via
  > those files, not from the user relaying Claude's output.

This section does not weaken any existing approval checkpoint, does not change the four-role model, and
does not authorize Codex - `docs/PROJECT_CONSTITUTION.md` s11 rule (a) and the roles above govern exactly
as before; this section only says *where* current state lives, not *who* may approve what.

## Change history
| Version | Date | Change |
|---|---|---|
| 1.4.0 | 2026-08-20 | `ADR-0062` (permanent execution-state mechanism): added "Execution-state recovery" - `docs/ACE_EXECUTION_STATE.md` as the canonical current-state snapshot, `reports/AI_HANDOFF_CURRENT.md`'s role unchanged, ADRs/DPs remain normative, git/CI remain evidential, and an explicit permanent prohibition on the user relaying reports between Claude and ChatGPT (sharpens `docs/PROJECT_CONSTITUTION.md` s11 point 3, already ratified `ADR-0056` - not reopened). No approval checkpoint weakened; role model unchanged; Codex not authorized. |
| 1.3.0 | 2026-08-19 | `ADR-0058` (narrow governance remediation): added "Execution continuity (do not stop prematurely)" - the five terminal stop conditions (user input, Claude input with a complete next instruction, genuine blocker, CEO approval checkpoint, task complete) and the "convert 'you should do X' into the next executable instruction" rule. Explicitly does not override s11 rule (a) (owner ratifies all decisions) or any existing approval checkpoint. Prior sections unedited. |
| 1.2.0 | 2026-08-18 | `ADR-0057` (narrow CEO-audit remediation): added "ACE interaction mode" (ChatGPT execution/audit-first response mode) and "Session-start audit (mandatory)" (the shared branch/HEAD/working-tree/spec/handoff/decision/open-questions checklist, binding both AI collaborators, not only Claude's own tooling habit). Original six-step per-tier workflow and its "two AI systems agreeing is not evidence" line are unedited. |
| 1.1.0 | 2026-08-17 | `ADR-0051`: owner-ratified as the ACE agent-workflow specification, subordinate to the `ADR-0042` hierarchy. Substantive content unchanged. |
| 1.0.0 | 2026-08-17 | G7 documentation repair (`docs/Q8_CLOSURE_MATRIX.md` s3): added the mandatory status header required by `docs/DOCUMENTATION_STANDARD.md` s2, previously missing entirely. Substantive content unchanged. |
