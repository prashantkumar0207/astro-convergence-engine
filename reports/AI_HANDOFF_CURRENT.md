<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | INDEX ONLY - navigation aid, not evidence. See "What this file is" below. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-17 |
| Review cadence | Regenerate at the start of a session if stale; not load-bearing if it isn't. |

# AI handoff: current state index

## What this file is

**An index, not a source of truth.** Nothing here is evidence of anything. It exists to save a cold
session the work of re-deriving "where do I even look" - every fact below is a pointer to something
git-verifiable, not a claim in its own right. If this file and the actual repository disagree, **the
repository is right**. Per `docs/PROJECT_CONSTITUTION.md` s7, the repository is the single
authoritative record; this file is not part of that record, only a map of it.

This file is expected to go stale between updates. Do not cite it in a decision entry, a certification
claim, or an audit. Regenerate the commands below rather than trusting the numbers already on the
page.

## How to find the real current state

```bash
git branch --show-current                       # current branch
git rev-parse HEAD                               # current commit
git status --porcelain                           # uncommitted / untracked state
git log --oneline -15                             # recent history
gh run list --limit 5                             # latest CI runs, if gh is available
python scripts/check_adr_numbering.py             # highest issued ADR number
```

## Where the actual memory lives

- `docs/DECISION_LOG.md` (+ root `DECISION_LOG.md`, the closed D-00x register) - every ratified and
  proposed decision, with evidence.
- `docs/OPEN_QUESTIONS.md` - every unresolved ambiguity, with resolution criteria.
- `docs/decisions/README.md` - the `DP-NNN` decision-paper index (options only, non-binding).
- `README.md` "Current state" - certified engine capability (which vargas, dashas, KP, transits, etc.
  are certified and under which ADR).
- `CLAUDE.md` and `.claude/rules/*.md` - operating rules for an AI collaborator in this repository.

## Snapshot as of the last update to this file (2026-08-17) - verify before relying on any of this

- Branch: `phase-g-q17-q21`. Not merged to `main`.
- Most recent decisions: ADR-0039 through ADR-0043 (Q17-Q21 governance batch and the certification
  drift-gate fix). Highest issued ADR at last check: `ADR-0043`.
- `docs/decisions/DP-010-ai-collaboration-scaffolding.md` presented options for this file, `CLAUDE.md`,
  and `.claude/rules/`. See `docs/DECISION_LOG.md` for whether and how it was closed.
- `reports/AI_COLLABORATION_INSPECTION.md` records the inspection that preceded the `CLAUDE.md` /
  `.claude/rules/` / hooks implementation.
- Known, permanent limitation: `swetest`-dependent certifiers cannot run on a Windows host. Not a
  regression if encountered there.
- Tier-0 is formally Locked per `ADR-0034`. Do not assume anything else carries that status without
  checking `docs/OPEN_QUESTIONS.md` Q17/Q18 and the specific decision entry.

## What to do if this file looks wrong

Trust `git log`, `docs/DECISION_LOG.md`, and `docs/OPEN_QUESTIONS.md` over this file, always. Update
this file's snapshot section if you notice it's drifted, but that update is a courtesy to the next
session, not a governance act.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-17 | Created as part of the minimum AI-collaboration architecture implementation. |
