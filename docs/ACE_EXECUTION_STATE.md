<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | **ACCEPTED (`ADR-0062`) - canonical, machine-checkable current-state record.** Regenerate/refresh on every meaningful implementation task, same discipline as `reports/AI_HANDOFF_CURRENT.md`. |
| Version | 1.1.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-20 (post-push: TRIKALAM_V1 Gate F CI-confirmed PASS; evidence-recovery commit 9e33490 pending push authorization) |
| Review cadence | Refresh at the start of a session if stale; not load-bearing if it isn't. |

# ACE execution state

## What this file is, and is not

This is **the single, terse, unambiguous answer to "where does ACE stand right now"** - a fixed set of
fields, always in the same place, so that state can be recovered from the repository alone, without
requiring ChatGPT's conversational memory and without requiring the USER to copy/paste Claude's reports
between LLMs (`ADR-0062`).

It is **not** a new authority and does **not** rank above anything in the `ADR-0042` hierarchy
(`PROJECT CONSTITUTION -> ENGINEERING CONSTITUTION -> DECISION LOG / ADR -> ... -> SPECIFICATIONS`). If
this file and `docs/DECISION_LOG.md`, git, or CI disagree, **those govern** - this file is a pointer,
exactly like `reports/AI_HANDOFF_CURRENT.md` already is, not a competing source of truth. It complements
that file rather than replacing it:

- **`reports/AI_HANDOFF_CURRENT.md`** - the detailed, append-only, task-by-task LLM handoff log (what
  changed, why, tests, certification evidence, per task).
- **`docs/ACE_EXECUTION_STATE.md` (this file)** - the canonical **current** snapshot only: one set of
  fields, overwritten each time (not append-only), answering "what is true right now" without needing to
  read the whole handoff log's history to find out.
- **`docs/DECISION_LOG.md`** - normative decisions (ADRs), append-only, never overwritten.
- **Git and CI** - evidential truth: commits, diffs, test runs, certification artifacts.

Per `docs/PROJECT_CONSTITUTION.md` s11 point 3 (already ratified, `ADR-0056`): the expected audit path
is **Git -> current branch/commit -> this file / the canonical handoff -> actual diff/code -> tests ->
certification artifacts -> governance records** - never the user relaying Claude's output to ChatGPT by
hand. This file exists to make that path fast: everything ChatGPT (or any auditor) needs to resume
independently is in these fields plus the pointers they name.

## Current state

| Field | Value |
|---|---|
| `CURRENT_PHASE` | FOUNDATION (`docs/Q8_CLOSURE_MATRIX.md` s4). Phase G exited (`ADR-0048`); FOUNDATION entered. |
| `CURRENT_MILESTONE` | Rahu Kalam / Yamaganda / Gulika, seed variant `PYJHORA_TRIKALAM_V1` (`DP-011` / `ADR-0060` / `ADR-0061`). Panchanga classification and rise/set are both already CERTIFIED and CEO-checkpoint-accepted (`ADR-0054`, `ADR-0059` + its checkpoint-acceptance addendum). |
| `CURRENT_AUTHORIZED_TASK` | Push the evidence-recovery commit below to `origin/phase-g-governance` so a clean CI run confirms `TRIKALAM_V1`'s Gate F (and everything else) green. No other FOUNDATION implementation is authorized right now - civil-date rendering, H-01, H-02, and boundary-proximity indicators all remain unauthorized pending their own decision papers (2026-08-19 FOUNDATION checkpoint audit, `reports/AI_HANDOFF_CURRENT.md`). |
| `TASK_OWNER` | CLAUDE (implementation + evidence recovery complete); USER (push authorization pending for the newest commit). |
| `STATUS` | `TRIKALAM_V1` implementation pushed and its Gate F genuinely ran under CI's hash-pinned oracle environment (**PASS**, "Oracle certification runners (all ten)" step succeeded) - but that same CI run (`32353401132`) failed on the expected M-03 drift-assertion step (177 -> 180 `modules_scanned`, the same class `ADR-0053`/`ADR-0054` already document). Evidence-recovery commit `9e33490` fixes this locally (confirmed via `check_artifact_drift.py`: 46 files identical outside volatile fields) but is **not yet pushed**. |
| `LAST_COMPLETED_ACTION` | Commit `9e33490` - CI-sourced evidence recovery for 13 certification artifacts (M-03 scan surface 177 -> 180), following the `ADR-0053`/`ADR-0054` precedent exactly. No source, gate, or certified result changed. |
| `LAST_COMMIT` | Local HEAD `9e33490d7e1186a114773231ff84807e835ededd`. `origin/phase-g-governance` is at `3487add6252f6cc4ebb535c512d390fedbf16494` (pushed and CI-run) - **1 commit behind local HEAD**: `9e33490` (evidence recovery, not yet pushed). |
| `LAST_CI_RUN` | `32353401132` (commit `3487add`, pushed): governance gate PASS; both no-oracle jobs PASS except the drift-assertion step (expected 177->180); oracle job's "Oracle certification runners (all ten)" step PASS - `certify_trikalam.py` genuinely ran Gate F under the hash-pinned environment - but its own drift-assertion step also failed on the same expected field. No CI run yet exists for `9e33490`. |
| `LAST_CEO_DECISION` | `ADR-0060` (2026-08-20): "CEO DECISION - DP-011. RATIFIED: OPTION C, SEEDED BY OPTION B", plus the owner's 2026-08-20 "push authorised" (consumed: `3487add` pushed and CI-run; this evidence-recovery follow-up commit is new and not yet covered by that authorization). |
| `NEXT_AUTHORIZED_ACTION` | On explicit USER push authorization: push `9e33490` to `origin/phase-g-governance`, monitor the resulting CI run for all four jobs green (including the drift-assertion steps), report the run ID and PASS/FAIL per job. |
| `WAITING_FOR` | USER: push authorization for commit `9e33490`. |
| `BLOCKER` | None technical. A governance/git-safety checkpoint only (`.claude/rules/git-safety.md`: pushing always needs explicit confirmation, per-action - the prior authorization covered `3487add`, not this newer commit). |
| `CEO_APPROVAL_REQUIRED` | **YES** - authorization to push `9e33490`. |
| `CLAUDE_ACTION_REQUIRED` | None until push is authorized. |
| `CHATGPT_ACTION_REQUIRED` | None pending. Once CI is fully green on the pushed evidence-recovery commit, ChatGPT's next audit is whether `TRIKALAM_V1` meets its own FOUNDATION per-capability checkpoint (`Q8_CLOSURE_MATRIX.md` s4), the same checkpoint question already resolved once for Panchanga. |
| `USER_ACTION_REQUIRED` | Authorize the push (a single yes/no), or give different instructions. |
| `HANDOFF_REQUIRED` | None beyond this file and `reports/AI_HANDOFF_CURRENT.md`'s latest entry - both already current as of this file's `Last updated` date. |

## How to independently verify every field above

```bash
git branch --show-current                          # current branch
git rev-parse HEAD                                  # local HEAD
git rev-parse origin/<branch>                        # last pushed commit (fetch first)
git log origin/<branch>..HEAD --oneline               # unpushed commits, if any
gh run list --branch <branch> --limit 5               # latest CI runs
python scripts/check_adr_numbering.py                 # highest issued ADR number
```

Never trust this file's field values over a fresh run of the commands above - regenerate, don't recall,
exactly as `reports/AI_HANDOFF_CURRENT.md` already requires of itself.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.1.0 | 2026-08-20 | Refreshed post-push: `3487add` pushed and CI-run (`32353401132`) - governance gate PASS, `TRIKALAM_V1`'s Gate F genuinely ran under the hash-pinned oracle environment and PASSED, but the run's drift-assertion steps failed on the expected M-03 `modules_scanned` field (177->180). Evidence-recovery commit `9e33490` fixes this locally (confirmed clean via `check_artifact_drift.py`); awaiting push authorization. |
| 1.0.0 | 2026-08-20 | Created (`ADR-0062`): the permanent ACE execution-state mechanism, so repository state - not ChatGPT conversational memory, and not the USER relaying Claude's reports - is sufficient to recover ACE's current state. |
