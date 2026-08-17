<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | INDEX ONLY - navigation aid, not evidence. See "What this file is" below. |
| Version | 1.2.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-17 (refreshed after ADR-0046) |
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

## Snapshot as of the last update to this file (2026-08-17, refreshed after ADR-0046) - verify before relying on any of this

- Branch: `phase-g-governance`, current HEAD `f3bec7f3e35d0eef93e115796ddb79ffea242723`. **Not merged
  to `main`**, and `main` remains untouched. The prior implementation branch, `phase-g-q17-q21`, was
  merged into `phase-g-governance` via PR #2 - merge commit `d53787e75048dbadc1a2e3559cf42405c1d56661`
  - which remains the historical merge point, not the current HEAD; two further non-merge commits have
  since landed on top of it (`ADR-0045`'s correction, then `ADR-0046`'s). GitHub CI run `32011431848`
  succeeded against `f3bec7f` (all four jobs: `no-oracle` 3.11, `no-oracle` 3.12, `governance`, `oracle`).
- Most recent decisions: ADR-0039 through ADR-0046. **`ADR-0044`, `ADR-0045`, and `ADR-0046` are all
  ACCEPTED.** Highest issued and current latest decision: `ADR-0046` (a narrow repair of a second false
  positive in `.claude/hooks/git_safety_guard.py`, found while pushing `ADR-0045`).
- `docs/decisions/DP-010-ai-collaboration-scaffolding.md` presented options for `CLAUDE.md` and
  `.claude/rules/`; marked `ADDRESSED by ADR-0044` in `docs/decisions/README.md`.
- `reports/AI_COLLABORATION_INSPECTION.md` and `reports/AI_COLLABORATION_IMPLEMENTATION.md` record the
  inspection and implementation that produced `CLAUDE.md` / `.claude/rules/` / the two hooks, and the
  two post-merge corrections (`ADR-0045`, `ADR-0046`) since.
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
| 1.2.0 | 2026-08-17 | Snapshot refreshed after ADR-0046: HEAD `f3bec7f3e35d0eef93e115796ddb79ffea242723`, merge commit `d53787e` now noted as historical rather than current, CI run `32011431848` green, highest and latest ADR `ADR-0046` (ADR-0044/0045/0046 all ACCEPTED). Navigation/status sections unchanged. |
| 1.1.0 | 2026-08-17 | Snapshot refreshed post-merge: branch `phase-g-governance`, merge commit `d53787e75048dbadc1a2e3559cf42405c1d56661`, CI run `32007363289` green, highest ADR `ADR-0044` (ACCEPTED). Navigation/status sections unchanged. |
| 1.0.0 | 2026-08-17 | Created as part of the minimum AI-collaboration architecture implementation. |
