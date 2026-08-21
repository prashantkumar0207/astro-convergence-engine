<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | **ACCEPTED (`ADR-0062`) - canonical, machine-checkable current-state record.** Regenerate/refresh on every meaningful implementation task, same discipline as `reports/AI_HANDOFF_CURRENT.md`. |
| Version | 3.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-21 (H-01 independent verification complete (ADR-0066 read confirmed, flagged as novel, no precedent); DP-015 drafted for boundary-proximity indicators; not implementation-authorized; awaiting owner on both) |
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
| `CURRENT_MILESTONE` | `TRIKALAM_V1` **FOUNDATION checkpoint-accepted**. Civil-date rendering **DEFERRED** (`ADR-0063`). H-02 **resolved and certified** (`ADR-0064`/`ADR-0065`). H-01 **ratified and implemented, `ADR-0066`, Option 2** - independently re-verified this task against the exact ratified `Q8_CLOSURE_MATRIX.md` s4 text: the reading holds, but is flagged as a **novel application with no prior precedent** in this repository (Phase G's own B-01/B-02/B-03 were fully resolved, never actually deferred, despite having an equivalent clause available). Boundary-proximity indicators: **investigated this task, `DP-015` drafted** - nothing governs it, and the exit criteria's "explicitly deferred... blocked accordingly" carve-out is textually scoped to H-01/H-02 by name, raising an open question about whether deferral alone can close ANY other FOUNDATION scope item, including this one and civil-date rendering's own already-recorded deferral. |
| `CURRENT_AUTHORIZED_TASK` | None self-executable. `DP-015` presents three treatment options plus a prior interpretive question (`DP-015` s3) the owner must resolve before the substantive choice is even well-posed. |
| `TASK_OWNER` | CLAUDE (`DP-015` drafted, H-01 independently re-verified); USER (both decisions in `DP-015` s.N). |
| `STATUS` | H-01 independent verification (this task, not a new ADR): re-read `Q8_CLOSURE_MATRIX.md` s4's exact ratified text directly. Confirms `ADR-0066` satisfies the literal "H-01... explicitly deferred by decision with the dependent domain blocked accordingly" clause - it is a decision, and the dependent domain (true-node transit-event search) is blocked at the code level, stronger than a documentation-only deferral. New finding this task: checked for repository precedent and found **none** - Phase G's own exit criteria offered an equivalent "resolved or explicitly deferred by decision" path for B-01/B-02/B-03 (`ADR-0049`), but all three were fully REMEDIATED, never actually deferred, so no prior case establishes that the owner accepts a hybrid "implemented-as-a-refusal-not-a-fix" treatment as satisfying an exit criterion. The interpretation is judged textually sound but genuinely novel, not settled by precedent - restated, not weakened, from the prior task's own flagging. **Boundary-proximity investigation (this task):** confirmed via repository-wide search that nothing ratified governs this FOUNDATION scope item - the only related material is KP_CHAIN_V1's own `nearest_boundary_arcsec` field (`ADR-0006`, certified but explicitly NOT Constitution s12 Locked) which has its own unresolved, unratified defect (H-07, cited only inside `ADR-0027` which is itself `Status: PROPOSED`), and `docs/DASHA_CERTIFICATION_ROADMAP.md` (`PROPOSED`), which discusses a dasha-specific instance of the same concept as a JATAKA-entry item, not this FOUNDATION-exit item. `docs/H7_BTR_SPEC.md` (BTR being the stated downstream beneficiary) never mentions the concept, and BTR is phases away regardless. Drafted `DP-015`, presenting a genuinely prior, separate textual question (does the exit criteria's deferral-with-blocking carve-out even extend to non-H-01/H-02 items, including this one AND civil-date rendering's existing `ADR-0063` deferral?) plus three treatment options (implement for named capabilities; defer explicitly; decouple from the exit checkpoint), with a low-confidence lean toward deferral. Decides nothing. |
| `LAST_COMPLETED_ACTION` | Independently re-verified the H-01/`ADR-0066` Q8-exit-criteria reading against the exact ratified text plus a Phase G precedent check; investigated and drafted `DP-015` (boundary-proximity indicators); governance gates and full test suite (816/816) re-run clean. |
| `LAST_COMMIT` | `d2a780cd7f0be31c1d18509a757b5b8225af032f` - local only, **not pushed** (explicit instruction: "Do not push d2a780c yet"). `origin/phase-g-governance` remains at `e7adeb0`. This task's own commit (`DP-015` + README/state-file updates) is local-only, ahead of `d2a780c`, also not pushed - see `reports/AI_HANDOFF_CURRENT.md`'s latest entry for its exact SHA. |
| `LAST_CI_RUN` | **`32478694212`** (commit `9737ddb`, the last *pushed* commit) - all four jobs green. Neither `d2a780c` nor this task's own commit has been pushed, so neither has a CI run yet. |
| `LAST_CEO_DECISION` | "Ratify DP-014 Option 2." (2026-08-21). No CEO decision yet on `DP-015` or on the section-3 interpretive question it raises. |
| `NEXT_AUTHORIZED_ACTION` | None self-executable. Both `DP-015`'s interpretive question and its three treatment options need the owner's input before any further step is authorized. |
| `WAITING_FOR` | USER: (a) confirm or correct the H-01 independent-verification finding above; (b) resolve `DP-015` s3's interpretive question; (c) select a `DP-015` treatment option (implement/defer/decouple). Not blocking other, unrelated work. |
| `BLOCKER` | **Boundary-proximity indicators** (FOUNDATION implementation scope) remain ungoverned - `DP-015` is ready for owner decision but nothing is chosen yet. FOUNDATION exit cannot be declared while this is true, and per `DP-015` s3, possibly not until the interpretive question is resolved either. |
| `CEO_APPROVAL_REQUIRED` | Yes, two decisions in `DP-015` s.N: (1) the section-3 interpretive question (does explicit deferral close FOUNDATION exit for items other than H-01/H-02?); (2) a `DP-015` treatment option for boundary-proximity indicators specifically. |
| `CLAUDE_ACTION_REQUIRED` | None until the owner responds to `DP-015`. |
| `CHATGPT_ACTION_REQUIRED` | Independent audit of the H-01 re-verification and of `DP-015`'s evidence base (especially section 3's textual argument) is available now via the standard Git -> state-file path - no report relay needed. |
| `USER_ACTION_REQUIRED` | Respond to `DP-015`'s two decisions (s.N), or otherwise direct next steps. |
| `HANDOFF_REQUIRED` | None beyond this file and `reports/AI_HANDOFF_CURRENT.md`'s latest entry, both refreshed as part of this task. |

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
| 3.0.0 | 2026-08-21 | Independently re-verified the H-01/`ADR-0066` Q8-exit-criteria reading against the exact ratified text (holds, but flagged as novel - no repository precedent for "deferred + blocked" satisfying an exit criterion; Phase G's B-01/B-02/B-03 were fully resolved, not deferred, despite an equivalent clause). Investigated boundary-proximity indicators: nothing ratified governs it; only related material is KP_CHAIN_V1's own unfinished `nearest_boundary_arcsec` (H-07, unratified) and `DASHA_CERTIFICATION_ROADMAP.md` (PROPOSED, JATAKA-scoped, not this item). Drafted `DP-015`, surfacing a textual ambiguity in `Q8_CLOSURE_MATRIX.md` s4 (does the deferral-with-blocking carve-out extend beyond H-01/H-02 by name - bearing on this item AND civil-date rendering's existing deferral) plus three treatment options, low-confidence lean toward deferral. Decides nothing; not implementation-authorized. `d2a780c` explicitly held back from push per instruction. |
| 2.9.0 | 2026-08-21 | `ADR-0066`: H-01 fix Option 2 ratified and implemented - `UnsupportedNodePolicyError` raised from `find_crossings()` for any non-mean node policy on Rahu/Ketu. No certified value changed (isolated-venv re-verification: only known ULP noise + volatile fields differed; discarded, not committed). Performed the FOUNDATION-exit readiness audit: rise/set, panchanga, trikalam certified; civil-date rendering deferred; H-02 resolved/certified; H-01 now resolved via the Q8 exit criteria's explicit-deferral-with-blocking clause (Claude's own read, flagged for independent confirmation). Boundary-proximity indicators found completely unaddressed (no paper, no ADR, no code) - identified as the standing FOUNDATION-exit blocker. Local-only, not pushed. |
| 2.8.0 | 2026-08-21 | H-01 decision-readiness: `DP-014` drafted and registered (`docs/decisions/DP-014-h01-true-node-station-density.md`), extracting `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md`'s H-01 finding, re-verified live against `e7adeb0` (`speeds.py`'s TrueNode grid step still exactly 37.5 days, unchanged), and tracing H-01's blast radius across all eight `node_policy` consumers - confirming the defect is confined to `find_crossings()`'s callers, that KP already hard-refuses true node independently, and that no shipped profile reaches the affected path. Presents the audit's own two proposed solutions plus a defer option; recommends explicit refusal (Option 2) at medium confidence; decides nothing, not implementation-authorized. Governance gates re-run clean. Local-only, not pushed. |
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
