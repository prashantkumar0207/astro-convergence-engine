<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | **ACCEPTED (`ADR-0062`) - canonical, machine-checkable current-state record.** Regenerate/refresh on every meaningful implementation task, same discipline as `reports/AI_HANDOFF_CURRENT.md`. |
| Version | 2.7.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-21 (H-02/DP-013 fully closed: pushed and CI-confirmed green, run 32478694212; awaiting the owner's next task) |
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
| `CURRENT_MILESTONE` | `TRIKALAM_V1` is **FOUNDATION checkpoint-accepted / production-certified**. Civil-date rendering is **ratified as DEFERRED** (`ADR-0063`). H-02: reproduction methodology executed and CI-confirmed (`ADR-0064`); **fix Option 1 ratified and implemented** (`ADR-0065`) - `TransitEvent.declared_division`, additive, no certified value changes. H-01 still has no governing document of any kind. |
| `CURRENT_AUTHORIZED_TASK` | None self-executable. `ADR-0065`'s implementation is complete and locally verified; CI confirmation of the new Gate E is the only remaining step, pending push authorization. |
| `TASK_OWNER` | CLAUDE (`ADR-0065` implemented, locally verified); USER (push authorization). |
| `STATUS` | `TRIKALAM_V1` done. `DP-012` deferred. `DP-013` fully resolved: Option C (reproduction, `ADR-0064`) and Option 1 (fix, `ADR-0065`) both ratified, implemented, and **CI-confirmed green** (run `9737ddb`, all four jobs, Gate E genuinely executed under the hash-pinned oracle environment: `declared_division : 49 cases, negative_control_verified=True`). One incidental finding along the way, diagnosed and recovered, not a defect: the locally-committed `TRANSIT_V1_certification.json` (regenerated in an unpinned exploration venv) differed from CI's hash-pinned regeneration by a single ULP in one Gate C `derived_tolerance_days` value - recovered via the standard CI-sourced evidence overlay (`ADR-0053`/`ADR-0054` precedent). No existing certified value actually changed; Options 2/3 not chosen; Tier-0 Locked scope not touched. |
| `LAST_COMPLETED_ACTION` | Pushed `9737ddb` (TRANSIT_V1 evidence recovery) and verified CI run `32478694212` - all four jobs green, Gate E confirmed genuinely executed from the log directly. |
| `LAST_COMMIT` | `9737ddb7f0d6edac99b922f0816867eccd717820` - pushed; `origin/phase-g-governance` identical. |
| `LAST_CI_RUN` | **`32478694212`** (commit `9737ddb`) - all four jobs green, directly confirmed via `gh run view`/`gh run --log`. |
| `LAST_CEO_DECISION` | "Ratify H-02 Fix Option 1." (2026-08-21): the owner chose Option 1 from `DP-013` s6's analysis. |
| `NEXT_AUTHORIZED_ACTION` | None self-executable. `DP-013` (H-02) is fully closed: reproduced, fixed, CI-confirmed. No FOUNDATION capability currently has both satisfied prerequisites and a ratified implementation decision - H-01 has no governing document; civil-date rendering is deferred. |
| `WAITING_FOR` | USER: name the next task. Not blocking. |
| `BLOCKER` | None. |
| `CEO_APPROVAL_REQUIRED` | Not immediately - nothing is queued needing approval right now. |
| `CLAUDE_ACTION_REQUIRED` | None until the owner names a next task. |
| `CHATGPT_ACTION_REQUIRED` | Independent audit of the `declared_division` implementation, Gate E, and its negative control is available now via the standard Git -> state-file path - no report relay needed. |
| `USER_ACTION_REQUIRED` | Name the next task - `DP-013`/H-02 is fully closed. |
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
| 2.7.0 | 2026-08-21 | Pushed `9737ddb` (TRANSIT_V1 evidence recovery: one ULP-level Gate C float difference between an unpinned local run and CI's pinned regeneration, recovered via CI-sourced overlay); CI run `32478694212` all four jobs green, Gate E confirmed genuinely executed. `DP-013`/H-02 is fully closed - reproduced, fixed, CI-confirmed. Nothing currently requires CEO approval. |
| 2.6.0 | 2026-08-21 | `ADR-0065`: H-02 fix Option 1 ratified and implemented. `TransitEvent.declared_division` (additive, default `None`), populated by `sign_ingresses`/`nakshatra_ingresses` from the exact target longitude. New Gate E in `certify_transits.py` (49 cases, genuine negative control) - PASS locally, all gates green, M-03 unchanged. 4 new tests, 812/812 pytest. No certified value changed. Push authorization pending. |
| 2.5.0 | 2026-08-21 | `DP-013` s6 (new): fix-option decision-readiness analysis. Verified `engine.transits` has zero production consumers today; `division_index` feeds nearly every certified classifier. Option 1 (additive field): near-zero regression risk, narrow `TRANSIT_V1` addendum. Option 2 (bias event instant): changes certified values, needs `TRANSIT_V1` recertification, has an unscoped-call-site complication. Option 3 (widen tolerance): verified to touch the FORMALLY LOCKED Tier-0 scope (`ADR-0005`/`ADR-0034`), global blast radius - not recommended. Recommends Option 1, high confidence; does not choose. |
| 2.4.0 | 2026-08-20 | Pushed `f3399f3`; CI run `32375941348` all four jobs green, both new H-02 steps confirmed genuinely executed under the hash-pinned oracle environment, identical results to the local runs. H-02's reproduction methodology is complete and CI-confirmed; choosing a fix option is the sole remaining, non-blocking item. |
| 2.3.0 | 2026-08-20 | `ADR-0064`: `DP-013` Option C (both A and B) ratified and executed. H-02 independently reproduced for the Sun (2/12, exact match); Moon 15/34 (44%), comparable to the audit's 43%. PyJHora recorded as an evidenced limitation (search diverges at 0.0001deg, direct longitude carries a 20.57 arcsec bias) rather than manufactured agreement. New tests, negative controls, independent validator, CI wiring (non-gating). No fix chosen; TRANSIT_V1 unmodified. Push authorization pending. |
| 2.2.0 | 2026-08-20 | `DP-013` decision-readiness audit: re-verified the 278x mismatch against live code; directly inspected PyJHora's source, confirming Option B's API is real but its default precision is ~4 orders of magnitude too coarse - a genuine, previously-unstated cost. Full options/evidence/trade-offs/recommendation placed in `reports/AI_HANDOFF_CURRENT.md` for CEO ratification. No option chosen, nothing implemented. |
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
