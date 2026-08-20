<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | **ACCEPTED (`ADR-0062`) - canonical, machine-checkable current-state record.** Regenerate/refresh on every meaningful implementation task, same discipline as `reports/AI_HANDOFF_CURRENT.md`. |
| Version | 2.1.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-20 (DP-013 drafted: H-02 reproduction-methodology and fix-option paper, extracted from ADR-0020 D5; awaiting ratification) |
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
| `CURRENT_MILESTONE` | `TRIKALAM_V1` is **FOUNDATION checkpoint-accepted / production-certified**. Civil-date rendering is **ratified as DEFERRED** (`ADR-0063`, `DP-012` Option C). H-02's ingress-classification seam now has a decision paper drafted and registered (`DP-013`, extracted from `ADR-0020` D5's already-written analysis) - presenting a reproduction methodology and a fix-option choice, both still owner decisions. H-01 still has no governing document of any kind. |
| `CURRENT_AUTHORIZED_TASK` | None self-executable. `DP-013` is drafted and awaiting owner ratification (or explicit deferral). No H-02 reproduction work, fix, or implementation is authorized by drafting the paper alone - `ADR-0020` itself, and all its other items, remain unratified and unreopened. |
| `TASK_OWNER` | CLAUDE (`DP-013` drafted and registered); USER (ratify a reproduction option in `DP-013`, or name a different next task). |
| `STATUS` | `TRIKALAM_V1` done and checkpoint-accepted. `DP-012` ratified Option C (deferred). `DP-013` (H-02 reproduction methodology and fix option) drafted per explicit, narrowly-scoped owner authorization - extracts only `ADR-0020` D5's existing analysis (the measured 2/12 Sun sankranti and 12/28 Moon nakshatra ingress misclassifications, and the residual-vs-tolerance mechanism G1's original audit identified), presents 3 reproduction options (independent reference; PyJHora oracle cross-check; both) and separately preserves the audit's own 3 fix options without recommending among them (out of this paper's authorized scope). Does not ratify `ADR-0020`, resolve H-02, or authorize any implementation. |
| `LAST_COMPLETED_ACTION` | `DP-013` drafted and registered: H-02 reproduction-methodology and fix-option decision paper, extracted from `ADR-0020` D5's existing analysis per explicit, scoped owner authorization. `ADR-0020` and its other items remain unratified and unreopened. |
| `LAST_COMMIT` | Local HEAD - see `git rev-parse HEAD`, made after this file was drafted; not yet pushed. `origin/phase-g-governance` remains at `e062b8e130178ef42e1fe9fba9540782e8c20dbe`. |
| `LAST_CI_RUN` | `32370032282` (commit `e062b8e`) - all four jobs green; unchanged by this documentation-only task. |
| `LAST_CEO_DECISION` | "ACE CONTINUE - AUTHORIZE H-02 DECISION PAPER" (2026-08-20): the owner authorized drafting the narrow H-02 paper, strictly scoped to `ADR-0020` D5's existing analysis. |
| `NEXT_AUTHORIZED_ACTION` | None self-executable. `DP-013` presents 3 reproduction-methodology options (independent reference; PyJHora oracle cross-check; both) and preserves the original audit's 3 fix options without recommending among them. On ratification of a reproduction option, the next Claude action is executing that reproduction (not a fix, not implementation) and reporting whether the original 2/12 and 12/28 findings are confirmed. |
| `WAITING_FOR` | USER: ratify a `DP-013` reproduction option (or defer H-02 entirely), or name a different next task. Not blocking. |
| `BLOCKER` | None technical. H-01 still has no governing document; H-02 now has a citable decision paper but no ratified option. |
| `CEO_APPROVAL_REQUIRED` | Not immediately - nothing is queued needing approval right now. |
| `CLAUDE_ACTION_REQUIRED` | None until the owner ratifies a `DP-013` option or names a different task. |
| `CHATGPT_ACTION_REQUIRED` | Independent audit of `DP-013`'s fidelity to `ADR-0020` D5 and the original G1 audit finding is available now via the standard Git -> state-file path - no report relay needed. |
| `USER_ACTION_REQUIRED` | Ratify a `DP-013` reproduction option (or defer), or name a different next task. |
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
| 2.1.0 | 2026-08-20 | `DP-013` drafted and registered: H-02 ingress-classification seam, extracting `ADR-0020` D5's already-written analysis (measured 2/12 Sun sankranti and 12/28 Moon nakshatra misclassifications; the 278x residual-vs-tolerance mismatch mechanism) per explicit, narrowly-scoped owner authorization. Presents 3 reproduction-methodology options and preserves the original audit's 3 fix options without recommending among them. Does not ratify ADR-0020 or resolve H-02. |
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
