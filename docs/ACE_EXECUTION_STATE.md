<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | **ACCEPTED (`ADR-0062`) - canonical, machine-checkable current-state record.** Regenerate/refresh on every meaningful implementation task, same discipline as `reports/AI_HANDOFF_CURRENT.md`. |
| Version | 2.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-20 (ADR-0063: DP-012 Option C ratified - civil-date rendering deferred, not implementation-authorized; caught and corrected a mismatched prior instruction before any code was written) |
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
| `CURRENT_MILESTONE` | `TRIKALAM_V1` (Rahu Kalam/Yamaganda/Gulika, seed variant `PYJHORA_TRIKALAM_V1`) is **FOUNDATION checkpoint-accepted / production-certified** (`ADR-0061`'s third addendum). Panchanga classification and rise/set are likewise CERTIFIED and checkpoint-accepted (`ADR-0054`, `ADR-0059`). Civil-date rendering for dasha boundaries is **ratified as DEFERRED** (`ADR-0063`, `DP-012` Option C) - not an active milestone, not implementation-authorized. FOUNDATION's remaining implementation-scope items (H-01, H-02) both still lack any ratified decision paper. |
| `CURRENT_AUTHORIZED_TASK` | None. No FOUNDATION implementation is currently authorized - `TRIKALAM_V1` is complete; civil-date rendering is explicitly deferred, not pending; H-01 has no governing document at all; H-02's own investigation methodology (`ADR-0020` D5) is itself unratified. |
| `TASK_OWNER` | CLAUDE (`TRIKALAM_V1` checkpoint and `DP-012` deferral both recorded); USER (name the next task - no FOUNDATION item is currently ready without further ratification). |
| `STATUS` | `TRIKALAM_V1` is done: implemented, CI-confirmed, CEO-audit ULP finding remediated and CI-confirmed, FOUNDATION checkpoint accepted. `DP-012` (civil-date rendering) is **ratified Option C: deferred entirely** until a consuming feature needs it - not implementation-authorized (a prior instruction to "implement Option C" was caught as a mismatch against the paper's actual text - Option C is the defer option - before any code was written, then corrected by the owner). No FOUNDATION capability beyond `TRIKALAM_V1` is authorized to implement; H-01/H-02/boundary-proximity remain unauthorized, unchanged since the last full audit. |
| `LAST_COMPLETED_ACTION` | `ADR-0063`: owner ratified `DP-012` Option C - civil-date rendering for dasha boundaries is deferred, not implementation-authorized. Caught and corrected a mismatched prior instruction (which said "implement Option C") against the paper's actual text before any code was written. |
| `LAST_COMMIT` | Local HEAD - see `git rev-parse HEAD`, made after this file was drafted; not yet pushed. `origin/phase-g-governance` remains at `9424768ebfb2d8567c939743e44efa0547eb32fa`. |
| `LAST_CI_RUN` | `32368698367` (commit `9424768`) - all four jobs green; unchanged by this documentation-only task. |
| `LAST_CEO_DECISION` | "ACE CORRECTION - DP-012 IS DEFERRED" (2026-08-20): the owner ratified `DP-012` Option C and corrected a prior mismatched implementation instruction. |
| `NEXT_AUTHORIZED_ACTION` | None self-executable. No FOUNDATION capability currently has both satisfied prerequisites and a ratified implementation decision. The most promising next decision-paper candidate is a narrow H-02 investigation-methodology paper (extracting `ADR-0020` D5's already-written analysis into its own citable decision, without requiring ratification of `ADR-0020`'s other nine unrelated items) - not drafted, only identified; drafting it would need its own explicit authorization. |
| `WAITING_FOR` | USER: to authorize drafting the H-02 decision paper identified above, or name a different next task. Not blocking - FOUNDATION has no other pending action. |
| `BLOCKER` | None technical. Every remaining FOUNDATION item (H-01, H-02) is blocked on a decision this repository does not yet have the prerequisite ratification to make. |
| `CEO_APPROVAL_REQUIRED` | Not immediately - nothing is queued needing approval right now. |
| `CLAUDE_ACTION_REQUIRED` | None until the owner names a next task. |
| `CHATGPT_ACTION_REQUIRED` | Independent audit of `TRIKALAM_V1`'s evidence trail, `ADR-0063`'s deferral, and the FOUNDATION roadmap state is available now via the standard Git -> state-file path - no report relay needed. |
| `USER_ACTION_REQUIRED` | Name the next task - e.g. authorize drafting the H-02 decision paper, or a different priority. |
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
| 2.0.0 | 2026-08-20 | `ADR-0063`: owner ratified `DP-012` Option C (deferred, not implementation-authorized), correcting a prior mismatched instruction caught before any code was written. Corrected all fields that previously implied civil-date rendering implementation was pending ratification. Identified (not drafted) a narrow H-02 decision-paper candidate as the next FOUNDATION item worth pursuing. |
| 1.9.0 | 2026-08-20 | `DP-012` decision-readiness audit: empirically disproved the fold/gap-ambiguity sub-question (research-resolvable, not a policy choice) via a direct `zoneinfo` test across both 2024 DST transitions; confirmed the LMT-labelling sub-question is genuine. Checked the rest of the FOUNDATION roadmap - nothing else authorized to implement. No option selected, nothing implemented. |
| 1.8.0 | 2026-08-20 | Pushed `eb79b7f`; CI run `32367342027` all four jobs green. Repository fully synced with origin, nothing outstanding except `DP-012` ratification (non-blocking). |
| 1.7.0 | 2026-08-20 | Independently advanced `DP-012` without deciding or implementing anything: empirically probed `zoneinfo`/`tzdata` against `RISE_SET_V1`'s own holdout dates, confirmed pre-standardization instants resolve to genuine Local Mean Time (not approximation), and folded this into the paper's options and s5 sub-decisions. |
| 1.6.0 | 2026-08-20 | Pushed `42d61c3`; CI run `32366108630` all four jobs green. Nothing left requiring immediate CEO approval; `DP-012` ratification is the sole standing, non-blocking open item. |
| 1.5.0 | 2026-08-20 | Owner accepted `TRIKALAM_V1`'s FOUNDATION checkpoint (third `ADR-0061` addendum) - it is now production-certified. `CURRENT_MILESTONE` moved to civil-date rendering for dasha boundaries; `DP-012` drafted and registered presenting its genuine open questions (DST fold/gap at derived instants, pre-1900 tzdata coverage, rendering granularity); implementation not authorized pending ratification. |
| 1.4.0 | 2026-08-20 | Pushed `8e6bb40`; CI run `32361308330` - all four jobs green, oracle-job log confirms the ULP battery genuinely executed (`ulp_boundary_checked: True, ulp_negative_control_verified: True`). CEO-audit finding closed. Refreshed all fields to present the FOUNDATION checkpoint decision as the sole open item. |
| 1.3.0 | 2026-08-20 | CEO audit found `TRIKALAM_V1`'s Gate C was a pinning/tolerance check, not a genuine ULP battery - verified independently, remediated (exact-sunrise-boundary ULP battery with negative control), all six gates re-verified locally (PASS). Awaiting push authorization for CI re-confirmation. |
| 1.2.0 | 2026-08-20 | `bf0d414` confirmed pushed (`origin` matches local HEAD); CI run `32358109807` - **all four jobs green**. `TRIKALAM_V1` is now fully CI-confirmed. No self-executable action remains; refreshed all fields to present the owner's FOUNDATION per-capability checkpoint decision as the sole open item. |
| 1.1.0 | 2026-08-20 | Refreshed post-push: `3487add` pushed and CI-run (`32353401132`) - governance gate PASS, `TRIKALAM_V1`'s Gate F genuinely ran under the hash-pinned oracle environment and PASSED, but the run's drift-assertion steps failed on the expected M-03 `modules_scanned` field (177->180). Evidence-recovery commit `9e33490` fixes this locally (confirmed clean via `check_artifact_drift.py`); awaiting push authorization. |
| 1.0.0 | 2026-08-20 | Created (`ADR-0062`): the permanent ACE execution-state mechanism, so repository state - not ChatGPT conversational memory, and not the USER relaying Claude's reports - is sufficient to recover ACE's current state. |
