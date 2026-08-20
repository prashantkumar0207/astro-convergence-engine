<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | **ACCEPTED (`ADR-0062`) - canonical, machine-checkable current-state record.** Regenerate/refresh on every meaningful implementation task, same discipline as `reports/AI_HANDOFF_CURRENT.md`. |
| Version | 1.2.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-20 (TRIKALAM_V1 fully CI-confirmed, all four jobs green, run 32358109807; awaiting owner FOUNDATION-checkpoint decision) |
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
| `CURRENT_AUTHORIZED_TASK` | None self-executable remains for `TRIKALAM_V1` - implementation is complete and CI-confirmed. The only open item is an owner decision (see `WAITING_FOR`). No other FOUNDATION implementation is authorized - civil-date rendering, H-01, H-02, and boundary-proximity indicators all remain unauthorized pending their own decision papers (2026-08-19 FOUNDATION checkpoint audit). |
| `TASK_OWNER` | CLAUDE (implementation, evidence recovery, and CI confirmation all complete); USER (the FOUNDATION checkpoint decision). |
| `STATUS` | **`TRIKALAM_V1` fully CI-confirmed.** Commit `bf0d414` is pushed and `origin/phase-g-governance` matches local HEAD exactly. CI run `32358109807` completed with **all four jobs green** - governance gate, both no-oracle legs, and the oracle gate (including `certify_trikalam.py`'s genuine Gate F execution and the drift-assertion step). No uncommitted or unpushed work remains. |
| `LAST_COMPLETED_ACTION` | Evidence addendum to `ADR-0061` recording CI confirmation (run `32358109807`, all four jobs green) and the recovered, expected M-03 drift finding. |
| `LAST_COMMIT` | `bf0d4140e239fa52200011698b2b132aa1460145` - local HEAD and `origin/phase-g-governance` are identical; nothing unpushed. |
| `LAST_CI_RUN` | **`32358109807`** (commit `bf0d414`) - **all four jobs green**, directly observed via `gh run view`. `certify_trikalam.py` genuinely executed under the hash-pinned oracle environment; `F_external_oracle` passed for real. |
| `LAST_CEO_DECISION` | `ADR-0060` (2026-08-20): "CEO DECISION - DP-011. RATIFIED: OPTION C, SEEDED BY OPTION B." (The prior "push authorised" instruction has been fully consumed - both `3487add` and the follow-up evidence-recovery commit are pushed and CI-green.) |
| `NEXT_AUTHORIZED_ACTION` | None self-executable. Awaiting the owner's decision on `TRIKALAM_V1`'s FOUNDATION per-capability checkpoint (below). On acceptance, the next Claude action is a narrow `ADR-0061`-addendum-style entry recording it (matching the `ADR-0059` Panchanga-checkpoint precedent exactly), and a new FOUNDATION task-selection audit for whatever the owner names next. |
| `WAITING_FOR` | **USER/CEO decision:** does `TRIKALAM_V1` (Rahu Kalam/Yamaganda/Gulika, `PYJHORA_TRIKALAM_V1` variant) meet `Q8_CLOSURE_MATRIX.md` s4's per-capability FOUNDATION checkpoint ("CEO approval: Entry, per-capability checkpoint, exit"), now that its implementation is complete and CI-confirmed under the hash-pinned oracle environment - the same question already resolved once for Panchanga (`ADR-0059`'s checkpoint addendum). This is a genuine ratification decision under `docs/PROJECT_CONSTITUTION.md` s11 rule (a); Claude does not self-certify it. |
| `BLOCKER` | None. |
| `CEO_APPROVAL_REQUIRED` | **YES** - the per-capability FOUNDATION checkpoint decision above. |
| `CLAUDE_ACTION_REQUIRED` | None until the checkpoint decision is made. |
| `CHATGPT_ACTION_REQUIRED` | Independent audit of `TRIKALAM_V1`'s evidence (this file, `ADR-0061` + its addendum, CI run `32358109807`) is available now via the standard Git -> state-file -> diff/tests/certification path - no report relay needed. |
| `USER_ACTION_REQUIRED` | Decide the FOUNDATION checkpoint question above, or name a different next task. |
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
| 1.2.0 | 2026-08-20 | `bf0d414` confirmed pushed (`origin` matches local HEAD); CI run `32358109807` - **all four jobs green**. `TRIKALAM_V1` is now fully CI-confirmed. No self-executable action remains; refreshed all fields to present the owner's FOUNDATION per-capability checkpoint decision as the sole open item. |
| 1.1.0 | 2026-08-20 | Refreshed post-push: `3487add` pushed and CI-run (`32353401132`) - governance gate PASS, `TRIKALAM_V1`'s Gate F genuinely ran under the hash-pinned oracle environment and PASSED, but the run's drift-assertion steps failed on the expected M-03 `modules_scanned` field (177->180). Evidence-recovery commit `9e33490` fixes this locally (confirmed clean via `check_artifact_drift.py`); awaiting push authorization. |
| 1.0.0 | 2026-08-20 | Created (`ADR-0062`): the permanent ACE execution-state mechanism, so repository state - not ChatGPT conversational memory, and not the USER relaying Claude's reports - is sufficient to recover ACE's current state. |
