<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | **ACCEPTED (`ADR-0062`) - canonical, machine-checkable current-state record.** Regenerate/refresh on every meaningful implementation task, same discipline as `reports/AI_HANDOFF_CURRENT.md`. |
| Version | 1.3.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-20 (CEO-audit ULP-battery finding remediated in Gate C; locally verified all six gates; push authorization pending) |
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
| `CURRENT_AUTHORIZED_TASK` | Push the ULP-battery remediation commit (below) so CI re-confirms `TRIKALAM_V1` with the corrected Gate C. No other FOUNDATION implementation is authorized - civil-date rendering, H-01, H-02, and boundary-proximity indicators all remain unauthorized pending their own decision papers (2026-08-19 FOUNDATION checkpoint audit). |
| `TASK_OWNER` | CLAUDE (remediation complete, locally verified); USER (push authorization pending). |
| `STATUS` | A CEO audit found `TRIKALAM_V1`'s Gate C (as CI-confirmed in run `32358109807`) was a pinning/tolerance check, not a genuine ULP battery. **Verified independently** (direct source re-inspection confirmed the finding), then remediated: Gate C now perturbs the exact sunrise weekday-rollover instant by a `1e-9`-day epsilon on both sides with a real negative control. All six gates re-verified locally (isolated exploration venv) - **PASS**, `ulp_boundary_checked: True`, `ulp_negative_control_verified: True`. `pytest` 801/801. **Not yet pushed/CI-confirmed** with the remediated gate. |
| `LAST_COMPLETED_ACTION` | Second `ADR-0061` evidence addendum: genuine ULP battery added to Gate C (`gate_c_boundary_ulp_and_circumpolar`), remediating the CEO-audit finding. `engine/tests/test_trikalam.py` gained matching ULP + negative-control tests. |
| `LAST_COMMIT` | Local HEAD - see `git rev-parse HEAD`, made after this file was drafted; not yet pushed. `origin/phase-g-governance` remains at `bf0d4140e239fa52200011698b2b132aa1460145` (the pre-remediation state CI last confirmed). |
| `LAST_CI_RUN` | `32358109807` (commit `bf0d414`) - all four jobs green, but for the **pre-remediation** Gate C (pinning/tolerance only, no ULP battery). No CI run yet exists for the remediated gate. |
| `LAST_CEO_DECISION` | The CEO audit's HOLD finding on `TRIKALAM_V1`'s missing ULP battery (relayed 2026-08-20), now remediated pending re-verification. |
| `NEXT_AUTHORIZED_ACTION` | On explicit USER push authorization: push local HEAD to `origin/phase-g-governance`, monitor the resulting CI run for all four jobs green including the remediated Gate C, report the run ID and PASS/FAIL per job. |
| `WAITING_FOR` | USER: push authorization for the ULP-battery remediation commit. |
| `BLOCKER` | None technical. A governance/git-safety checkpoint only (per-action push confirmation). |
| `CEO_APPROVAL_REQUIRED` | **YES** - authorization to push. The FOUNDATION per-capability checkpoint question (does `TRIKALAM_V1` meet `Q8_CLOSURE_MATRIX.md` s4) remains separately open and should await this remediation's own CI confirmation first. |
| `CLAUDE_ACTION_REQUIRED` | None until push is authorized. |
| `CHATGPT_ACTION_REQUIRED` | Independent re-audit of the remediated Gate C (this file, the new `ADR-0061` addendum, `scripts/certify_trikalam.py`) is available now via the standard Git -> state-file path - no report relay needed. |
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
| 1.3.0 | 2026-08-20 | CEO audit found `TRIKALAM_V1`'s Gate C was a pinning/tolerance check, not a genuine ULP battery - verified independently, remediated (exact-sunrise-boundary ULP battery with negative control), all six gates re-verified locally (PASS). Awaiting push authorization for CI re-confirmation. |
| 1.2.0 | 2026-08-20 | `bf0d414` confirmed pushed (`origin` matches local HEAD); CI run `32358109807` - **all four jobs green**. `TRIKALAM_V1` is now fully CI-confirmed. No self-executable action remains; refreshed all fields to present the owner's FOUNDATION per-capability checkpoint decision as the sole open item. |
| 1.1.0 | 2026-08-20 | Refreshed post-push: `3487add` pushed and CI-run (`32353401132`) - governance gate PASS, `TRIKALAM_V1`'s Gate F genuinely ran under the hash-pinned oracle environment and PASSED, but the run's drift-assertion steps failed on the expected M-03 `modules_scanned` field (177->180). Evidence-recovery commit `9e33490` fixes this locally (confirmed clean via `check_artifact_drift.py`); awaiting push authorization. |
| 1.0.0 | 2026-08-20 | Created (`ADR-0062`): the permanent ACE execution-state mechanism, so repository state - not ChatGPT conversational memory, and not the USER relaying Claude's reports - is sufficient to recover ACE's current state. |
