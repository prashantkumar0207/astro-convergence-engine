<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | **ACCEPTED (`ADR-0062`) - canonical, machine-checkable current-state record.** Regenerate/refresh on every meaningful implementation task, same discipline as `reports/AI_HANDOFF_CURRENT.md`. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-20 |
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
| `CURRENT_AUTHORIZED_TASK` | Push the 4 local commits below to `origin/phase-g-governance` so CI can confirm `TRIKALAM_V1`'s Gate F under the hash-pinned oracle environment. No other FOUNDATION implementation is authorized right now - civil-date rendering, H-01, H-02, and boundary-proximity indicators all remain unauthorized pending their own decision papers (2026-08-19 FOUNDATION checkpoint audit, `reports/AI_HANDOFF_CURRENT.md`). |
| `TASK_OWNER` | CLAUDE (implementation complete); USER (push authorization pending). |
| `STATUS` | Implementation complete, locally verified (all six gates, 799/799 `pytest`). **Not yet CI-confirmed** - local verification used an isolated, unpinned exploration venv, not CI's hash-pinned oracle environment. |
| `LAST_COMPLETED_ACTION` | Commit `7276bf9` - `TRIKALAM_V1` (`PYJHORA_TRIKALAM_V1`) implemented: `engine.astrology.trikalam`, 21 tests, an independent validator, a Gate A-F certifier (`ADR-0061`). |
| `LAST_COMMIT` | Local HEAD `7276bf9d2425420b482170cb02c16c55c0bbccce`. `origin/phase-g-governance` is at `ce2475f0fbfba348783b829b5d0a2b24fa45ef12` - **4 commits behind local HEAD**: `cb9001f` (FOUNDATION checkpoint audit), `9bbe254` (Panchanga checkpoint accepted; `DP-011` drafted), `bad5b04` (`DP-011` ratified, `ADR-0060`), `7276bf9` (`TRIKALAM_V1` implemented, `ADR-0061`). None of these four are pushed. |
| `LAST_CI_RUN` | `32242462766` (commit `4177d61`) and `32248801410` (commit `ce2475f`) - both green, all four jobs. **No CI run yet exists for any of the 4 unpushed commits above**, including `TRIKALAM_V1`'s own Gate F. |
| `LAST_CEO_DECISION` | `ADR-0060` (2026-08-20): "CEO DECISION - DP-011. RATIFIED: OPTION C, SEEDED BY OPTION B" - named, profile-selectable Rahu Kalam/Yamaganda/Gulika variants, PyJHora's convention as the seed. |
| `NEXT_AUTHORIZED_ACTION` | On explicit USER push authorization: push local HEAD to `origin/phase-g-governance`, monitor the resulting CI run specifically for `certify_trikalam.py`'s execution in the `oracle` job and its `F_external_oracle` result, report the run ID and PASS/FAIL per job (the `ADR-0053`/`ADR-0054`/`ADR-0059` evidence-recovery discipline). |
| `WAITING_FOR` | USER: push authorization for the 4 local commits. |
| `BLOCKER` | None technical. A governance/git-safety checkpoint only (`.claude/rules/git-safety.md`: pushing always needs explicit confirmation). |
| `CEO_APPROVAL_REQUIRED` | **YES** - authorization to push. |
| `CLAUDE_ACTION_REQUIRED` | None until push is authorized. |
| `CHATGPT_ACTION_REQUIRED` | None pending. Once CI confirms `TRIKALAM_V1`, ChatGPT's next audit is that CI run plus whether `TRIKALAM_V1` meets its own FOUNDATION per-capability checkpoint (`Q8_CLOSURE_MATRIX.md` s4), the same checkpoint question already resolved once for Panchanga. |
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
| 1.0.0 | 2026-08-20 | Created (`ADR-0062`): the permanent ACE execution-state mechanism, so repository state - not ChatGPT conversational memory, and not the USER relaying Claude's reports - is sufficient to recover ACE's current state. |
