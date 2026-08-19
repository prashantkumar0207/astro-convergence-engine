<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | INDEX ONLY - navigation aid, not evidence. See "What this file is" below. |
| Version | 2.6.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-19 (PANCHANGA_V1 Gate F committed, pushed, CI-confirmed under the hash-pinned oracle environment - CI run 32242462766 green) |
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

**This IS the canonical Claude -> ChatGPT handoff** (`docs/PROJECT_CONSTITUTION.md` s11, `ADR-0056`).
Claude updates it after every meaningful implementation task. No other file plays this role; do not
create a competing one.

## Role model (docs/PROJECT_CONSTITUTION.md s11, formalized ADR-0056)

- **USER** - product owner, final ratifying authority.
- **CLAUDE** - the primary and sole ACE builder/executor: all ACE coding, repository editing, test
  execution, certification execution, and commits. Updates this file after every meaningful task.
- **CHATGPT** - independent ACE CEO / technical auditor: audits architecture, specifications,
  governance, code, tests, certification evidence, provenance, and claims; determines PASS / HOLD /
  FAIL; gives Claude the exact next action when remediation is required. Not a builder; does not
  commit.
- **CODEX** - not part of the ACE workflow, unless the user explicitly changes it in a future decision
  entry.
- **Git is the source of truth** for all of the above. This file is an evidence/index record, not a
  substitute for it.

Expected ChatGPT audit path: Git (current branch/commit) -> this handoff -> actual diff/code -> tests
-> certification artifacts -> governance records. The user should not need to manually relay Claude's
terminal output when that evidence already exists in Git or here.

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

## Task handoff log (Claude -> ChatGPT, most recent first)

Claude appends one entry here after every meaningful implementation task, using this template. Entries
are append-only history, like `docs/DECISION_LOG.md`; do not edit a prior entry's substance - if a
later task supersedes one, say so in the new entry.

**Template:**
```
### <date> - <short task title>
- Branch / commit SHA: <branch>, <full SHA>
- Previous approved commit: <full SHA>
- Task: <what was asked>
- Relevant ADR/specification: <IDs and paths>
- Files changed: <list or "see commit">
- Implementation summary: <what changed, why>
- Tests executed and results: <commands, pass/fail counts>
- Certification executed and results: <certifier(s), PASS/FAIL, gate summary>
- Known issues: <anything unresolved>
- Unresolved questions: <anything needing owner/ChatGPT input>
- CEO decision required: <yes/no, and exactly what if yes>
- Next authorized action: <what Claude may do next without re-asking>
```

### 2026-08-19 - PANCHANGA_V1 Gate F committed, pushed, CI-confirmed under the hash-pinned oracle environment
- Branch / commit SHA: `phase-g-governance`, `4177d6108236e64d07f6b23499307001f0d7c421` ("Add PyJHora
  external oracle gate for Panchanga V1"), pushed and equal to `origin/phase-g-governance` (confirmed
  `git rev-parse HEAD` = `git rev-parse origin/phase-g-governance` immediately after push).
- Previous approved commit: `20a9589e3d567bbf86e36b13bf2d61ca734e728e`
- Task: CEO authorization "Approve commit and push" for the seven files the prior entry describes,
  followed by CI oracle verification and, if it passes, a certification-status determination.
- Relevant ADR/specification: `ADR-0059` (unedited by this entry - it already recorded the
  implementation and explicitly deferred CI confirmation to this step).
- Files changed in commit `4177d61`: exactly the seven authorized files (`scripts/certify_panchanga.py`,
  `.github/workflows/ci.yml`, `certification/PANCHANGA_V1_certification.json`, `reports/certification/
  panchanga.report.md`, `reports/certification/panchanga.console.txt`, `docs/DECISION_LOG.md`, this
  file) - confirmed via `git status --porcelain` before staging, `git add --` by explicit path (not `-A`
  or `.`), and `git diff --cached` reviewed before commit; no pre-existing untracked file was staged.
  **A second, small follow-up (this entry) overlays the CI-oracle-regenerated `certification/
  PANCHANGA_V1_certification.json` and its two `reports/certification/panchanga.*` companions** in place
  of the locally-produced (unpinned exploration venv) versions committed in `4177d61` - diffed first and
  confirmed to differ from the CI-sourced version in exactly the one legitimately-volatile
  `environment.python` field (`3.12.10` local vs `3.11.15` CI) and nothing else, matching the
  `ADR-0053`/`ADR-0054` evidence-recovery precedent of always preferring CI-sourced canonical evidence
  over a local run once CI evidence exists.
- CI run: **`32242462766`**
  (`https://github.com/prashantkumar0207/astro-convergence-engine/actions/runs/32242462766`), triggered
  by commit `4177d61`, all four jobs green:
  1. **governance gate** - PASS (10s).
  2. **no-oracle gate (3.11)** - PASS (2m14s). `certify_panchanga.py` confirmed **absent** (0 occurrences
     in the job log) - correctly excluded now that it requires PyJHora. `validate_panchanga_holdout.py`
     (Gate E, no PyJHora needed) ran and printed `PANCHANGA HOLDOUT VALIDATION PASS: 24 cases, 90
     comparisons, 0 mismatches`.
  3. **no-oracle gate (3.12)** - PASS (2m41s), same shape as 3.11.
  4. **oracle gate (PyJHora, hash-pinned)** - PASS (52s). Environment-identity step printed
     `pyswisseph reports 2.10.03` and `PyJHora 4.8.7`; the assertion step printed "environment identity
     verified: python 3.11, PyJHora 4.8.7, 35 packages match the lock, 3 ephemeris assets match
     checksums" - the hash-pin is genuinely verified, not merely installed. `scripts/certify_panchanga.py`
     ran as the **ninth and last** runner in "Oracle certification runners (all nine)", printing
     `F_external_oracle: {'cases': 11, 'profiles': 2, 'elements': ['tithi', 'yoga', 'karana'],
     'comparisons': 66, 'mismatches': 0, 'negative_control_verified': True, ...}` - genuinely executed,
     not skipped. The drift-assertion step printed
     `PASS: 43 evidence file(s) identical to the committed version outside the volatile fields (17
     machine-readable, 26 rendered)`, and the preceding `git diff --stat` showed `certification/
     PANCHANGA_V1_certification.json | 2 +-` - i.e., exactly the volatile-field-sized diff expected, no
     unexpected drift.
- Tests executed and results: full `pytest` (`Default gate (engine/tests)` step) passed in both no-oracle
  jobs (job succeeded; per-step failure would have failed the whole job, which it did not). Independent
  holdout validators (all thirteen, including `validate_panchanga_holdout.py`) passed in both no-oracle
  jobs.
- Certification executed and results: `PANCHANGA_V1` - **PASS, all six gates, under CI's hash-pinned
  oracle environment** - the evidence class every other certified claim in this repository already
  relies on. Gate F: 66 comparisons, 0 mismatches, negative control genuinely detected the injected
  defect and the real function was confirmed restored and re-agreeing with the oracle.
- Known issues: none. The cosmetic PyJHora import-time stdout noise noted in the prior entry does not
  appear in the CI console transcript either (confirmed: the archived `panchanga.console.txt` begins at
  the `====` header, same as the local run).
- Unresolved questions: none technical. **Certification-status determination, per this task's own
  instruction:** `PANCHANGA_V1` classification (tithi, nakshatra-reuse, yoga, karana, vara at a given
  instant) can now be presented as satisfying the `DP-009` s5 / `ADR-0052` / `Q8_CLOSURE_MATRIX.md` s4
  varga-template methodology **for the scope `ADR-0055` authorized** - frozen rule, second transcription,
  dense sweep, ULP battery, external oracle (now genuinely present, CI-verified), independent validator,
  protected holdout, regenerable artifact, ADR. Rahu Kalam/Yamaganda/Gulika and element transition timing
  remain explicitly unauthorized and uncertified (`ADR-0055` items 2-3) - this determination does **not**
  extend to them. Whether this now clears `Q8_CLOSURE_MATRIX.md` s4's FOUNDATION per-capability checkpoint
  for Panchanga specifically (as opposed to FOUNDATION's overall phase exit, which also needs rise/set,
  Rahu Kalam/Yamaganda/Gulika, H-01, H-02) is a CEO/owner determination, not self-certified here.
- CEO decision required: **whether to formally accept Panchanga classification as meeting its
  per-capability FOUNDATION checkpoint** (`Q8_CLOSURE_MATRIX.md` s4's "CEO approval: entry,
  per-capability checkpoint, exit"), now that the one identified gap is closed with CI evidence. This
  entry presents the evidence; it does not itself constitute that approval.
- Next authorized action: none self-authorized beyond what is recorded here. Awaiting the CEO checkpoint
  decision above, or a new authorized task naming the next FOUNDATION capability (Rahu Kalam/Yamaganda/
  Gulika variant-table ratification remains separately pending per `ADR-0055` item 2; H-01/H-02 remain
  unresolved).

### 2026-08-19 - PANCHANGA_V1 external-oracle Gate F implemented (ADR-0059), locally verified, CI pending
- Branch / commit SHA: `phase-g-governance`, working tree only - **no commit made**, per this task's
  explicit "Do not commit or push unless separately authorized by CEO/user."
- Previous approved commit: `20a9589e3d567bbf86e36b13bf2d61ca734e728e`
- Task: CEO-approved "ACE EXECUTION CONTINUITY - PANCHANGA PYJHORA EXTERNAL-ORACLE GATE" - close the
  gap the prior checkpoint found (no external-oracle gate for tithi/yoga/karana) by implementing and
  CI-verifying a genuine PyJHora oracle gate, Option (b) of that checkpoint's two remedies.
- Relevant ADR/specification: `ADR-0059` (this implementation); `ADR-0055` (Panchanga scope, unchanged);
  `ADR-0052`/`DP-009` s5 (the methodology this closes); `ADR-0054` (the analogous rise/set precedent,
  cited for why the CI-job-move design was chosen); the existing oracle mechanism in `certify_d2.py`,
  `certify_vimshottari.py`, `certify_transits.py` (reused, not reinvented).
- Files changed (working tree, uncommitted): `scripts/certify_panchanga.py` (new Gate F -
  `gate_f_external_oracle()` - plus a module-level unconditional PyJHora import guard, an `oracle`
  report block, and an updated `explicit_non_claims` entry replacing the old "not verified reachable"
  line); `.github/workflows/ci.yml` (moved `certify_panchanga.py` from the `hermetic` job's non-oracle
  runners and network-guard list to the `oracle` job's runner list, now nine); `certification/
  PANCHANGA_V1_certification.json` and its `reports/certification/panchanga.report.md`/`.console.txt`
  companions (regenerated, genuinely including Gate F's real PyJHora results); `docs/DECISION_LOG.md`
  (new `ADR-0059`, register header updated); this file.
- Implementation summary: `jhora.panchanga.drik.tithi(jd, place)[0]`/`yogam(...)`[0]`/`karana(...)[0]`
  located and empirically verified this session (an isolated, throwaway, unpinned exploration venv,
  distinct from the hash-pinned `requirements-oracle.lock`) to be 1-based and identical in convention to
  this module's own indices; `place.timezone` fixed at `0.0` uniformly (empirically shown irrelevant to
  the result at that setting across the full holdout, after one arbitrary large offset was observed to
  change a result in exploratory testing - not left as an unexamined default). Gate F runs 66
  comparisons (11 H1-H11 holdout cases x 2 profiles x 3 elements: tithi/yoga/karana), using
  `drik.set_ayanamsa_mode("LAHIRI"|"KP")` to align PyJHora with each profile, matching the exact
  convention `certify_vimshottari.py`/`certify_transits.py` already use. A genuine negative control
  (temporarily replaces the real `tithi_index` with a function guaranteed to disagree with the real
  oracle value, confirms the SAME comparison logic flags it, restores, re-verifies agreement) mirrors
  `test_panchanga.py`'s own established pattern. Nakshatra is deliberately excluded (already
  Tier-0-certified reuse, not new code; scoped out by the prior checkpoint) - recorded in the gate's own
  `nakshatra_excluded_reason` field, not silently omitted. `certify_panchanga.py`'s PyJHora import is now
  unconditional (hard `sys.exit(3)` if unavailable), matching every one of the eight existing oracle
  certifiers exactly - so the certifier moved from the `hermetic` job to the `oracle` job's runner list.
  This was a deliberate, reasoned choice: `scripts/check_artifact_drift.py` compares one committed
  artifact per file against whatever regenerated it, with no per-job "oracle executed" exception: running
  Gate F conditionally in two jobs would make the canonical artifact legitimately differ by job, which is
  exactly the calculated-content drift `.claude/rules/certification.md` forbids treating as volatile
  without its own decision. `validate_panchanga_holdout.py` (Gate E) needs no PyJHora and stays in the
  `hermetic` job's validator list, unchanged. Gates A-E's own logic and results are untouched.
- Tests executed and results: `python -m pytest -q` - 778 passed, 0 failed (unchanged from baseline;
  no `engine/` code touched). `python -m pytest engine/tests/test_panchanga.py -q` - 179 passed.
  `python validate_panchanga_holdout.py` (main env, no PyJHora needed) - PASS, 24 cases, 90 comparisons,
  0 mismatches.
- Certification executed and results: `python scripts/certify_panchanga.py` in the main (no-PyJHora)
  environment - correctly `exit(3)` ("PyJHora oracle unavailable"), matching every other oracle-tier
  certifier's behaviour without PyJHora - confirmed as the CORRECT fail-closed behaviour, not a defect.
  `python scripts/certify_panchanga.py` via the isolated exploration venv (PyJHora 4.8.7 present) -
  **PASS, all six gates**, including `F_external_oracle`: 66 comparisons, 0 mismatches, negative control
  verified. `certification/PANCHANGA_V1_certification.json` regenerated from this real run - genuine
  evidence, not backfilled. `scripts/check_adr_numbering.py` - PASS, 59 entries.
  `scripts/check_retired_identifiers.py`, `scripts/check_identifier_families.py` - PASS. `git diff
  --check` - clean (CRLF-normalization warnings only, expected on this Windows checkout).
- Known issues: PyJHora prints internal diagnostic noise to stdout during its own config
  initialization (observed: lines like "panchanga C:\Users added to system path [...]"); this happens
  at import time, before `certification_support.start_transcript()` begins capturing, so it does not
  pollute the archived console transcript - confirmed by inspecting `reports/certification/
  panchanga.console.txt` after the run. Cosmetic only; not a defect in the certifier or its evidence.
- Unresolved questions / CEO decision required: **only the commit/push itself, and the CI run it would
  trigger.** This session's local verification used an isolated, throwaway, **unpinned** exploration
  venv (PyJHora 4.8.7, matching the version pinned in `requirements-oracle.lock`, but not hash-verified
  and not the CI-pinned Python 3.11/Linux environment) - this is genuine, real oracle evidence, but it
  is explicitly **not** the hash-pinned CI oracle-environment evidence class `RISE_SET_V1` and the eight
  existing varga oracle certifiers rely on for their own committed claims. `ADR-0059`'s own Consequences
  section states this distinction; do not describe `PANCHANGA_V1` as CI-oracle-confirmed until a pushed
  commit's `oracle` job run actually passes.
- CEO decision required: **the commit/push itself**, to trigger the CI run that would upgrade this
  evidence from "locally verified, unpinned" to "CI-confirmed, hash-pinned oracle environment" - the
  same evidence class every other certified claim in this repository already carries.
- Next authorized action: on explicit owner authorization to commit and push, stage exactly the seven
  files listed above (`scripts/certify_panchanga.py`, `.github/workflows/ci.yml`, `certification/
  PANCHANGA_V1_certification.json`, `reports/certification/panchanga.report.md`,
  `reports/certification/panchanga.console.txt`, `docs/DECISION_LOG.md`, this file) on
  `phase-g-governance`, commit, push, then monitor the resulting `oracle` job run specifically for
  `certify_panchanga.py`'s new ninth position and `F_external_oracle`'s real result, and report the run
  ID and PASS/FAIL per job - the same evidence-recovery discipline `ADR-0053`/`ADR-0054` already
  established. Until authorized, no further action beyond this record is taken.

### 2026-08-19 - Panchanga production-certification checkpoint (audit only, no commit)
- Branch / commit SHA: `phase-g-governance`, `20a9589e3d567bbf86e36b13bf2d61ca734e728e` - **read-only
  audit task; no implementation or certification code changed.** This entry and its two mechanical
  `docs/DECISION_LOG.md` `ADR-0058` corrections (see below) are the only edits, and remain **uncommitted**
  per this task's explicit "Do NOT: ... commit ... push."
- Previous approved commit: `20a9589e3d567bbf86e36b13bf2d61ca734e728e`
- Task: owner-directed "ACE EXECUTION CONTINUITY - PANCHANGA PRODUCTION-CERTIFICATION CHECKPOINT" -
  determine whether `PANCHANGA_V1`'s existing green certification actually satisfies the FOUNDATION
  phase's declared production-certification requirements (`docs/Q8_CLOSURE_MATRIX.md` s4, `DP-009`,
  `ADR-0017`/`ADR-0051` C0-C5 framework, `ADR-0055`), not merely whether the gate script exits 0.
- Relevant ADR/specification: `ADR-0055` (Panchanga classification scope); `ADR-0052` (DP-009 Option B:
  rise/set Tier-0, panchanga Tier-1); `ADR-0054` (rise/set's closely analogous oracle-substitution
  precedent); `ADR-0051` Decision 3 (binding C0-C5 table); `docs/Q8_CLOSURE_MATRIX.md` s4 (FOUNDATION
  certification-gates row, names "external oracle" explicitly for the classification parts);
  `docs/decisions/DP-009-panchanga-riseset-tier.md` s5 ("the varga template: frozen rule, second
  transcription, dense sweep, ULP battery, external oracle, independent validator").
- Files changed (working tree, uncommitted): `docs/DECISION_LOG.md` (two mechanical corrections to the
  already-committed `ADR-0058` entry's Status/Consequences text and the register header, marking its
  commit `20a9589` confirmed - the text had gone stale the moment the owner committed it directly, since
  it still read "not yet committed"), `reports/AI_HANDOFF_CURRENT.md` (this entry, plus the matching
  correction to the prior entry above and the refreshed snapshot below). No source, calculation,
  certification, or evidence file touched.
- Implementation summary (findings, not code changes):
  1. **Scope, methodology, negative control, holdout, and vara's rise/set dependency all check out
     against `ADR-0055`/`DP-009`/`ADR-0052`** - classification-only scope is correctly and explicitly
     bounded in code (`panchanga.py`, `certify_panchanga.py`'s `explicit_non_claims`) and governance;
     the Fraction-exact independent reference (Gates B/E) is genuinely independent (never calls
     `division_index`); one genuine negative control exists and is demonstrated catching a real,
     reintroduced defect before being undone (`test_negative_control_broken_division_index_is_caught_by_independent_reference`);
     the H1-H11/P1-P2 holdout is the same protected, frozen holdout reused across this repository's
     other certifiers; vara correctly consumes (never reimplements) certified `rise_set.sunrise()`.
  2. **One genuine, unresolved gap: `PANCHANGA_V1` has no external-oracle gate for tithi/yoga/karana,
     and this specific omission was never separately presented to the owner for ratification**, unlike
     its exact structural analogue. `docs/decisions/DP-009-panchanga-riseset-tier.md` s5 (the
     recommendation `ADR-0052` accepted as Option B) explicitly names "external oracle" as part of "the
     varga template" panchanga's classification parts need, and `docs/Q8_CLOSURE_MATRIX.md` s4's
     FOUNDATION certification-gates row repeats "external oracle... for the classification parts"
     verbatim. `certify_panchanga.py`'s own docstring and `explicit_non_claims` list honestly disclose
     that no PyJHora oracle gate exists (API surface not verified reachable in this environment) and
     substitute only the independently-coded Fraction-exact reference instead. **This substitution
     precisely mirrors what `certify_rise_set.py` already does for its own Gate C** (an independently-
     coded closed-form reference in place of the unreachable/unverified `swetest` binary) - but rise/
     set's substitution was explicitly named, justified in detail, and owner-ratified as part of
     `ADR-0054`'s "CEO OWNER AUTHORIZATION - FOUNDATION RISE/SET" ("the complete rise/set workstream").
     `ADR-0055`'s four bundled, owner-authorized items (boundary convention; Rahu Kalam/Yamaganda/Gulika
     deferred; classification-only scope; vara consumes rise/set) do **not** mention the oracle-gate
     substitution at all - it was a builder (Claude) methodology choice, disclosed in code and the
     certification artifact, but never itself put to the owner as a decision the way the identical
     rise/set case was.
- Tests executed and results: none re-run (no code changed since the last full `pytest` pass, 778
  passed, recorded in the 2026-08-18 evidence-recovery entry above); this task's own verification was
  document/artifact inspection (`certify_panchanga.py`, `certify_rise_set.py`, `PANCHANGA_V1_certification.json`
  / `panchanga.report.md`, `DP-009`, `ADR-0052`/`ADR-0054`/`ADR-0055`, `docs/Q8_CLOSURE_MATRIX.md` s4),
  not a fresh run.
- Certification executed and results: none re-run; `PANCHANGA_V1`'s existing `RESULT: PASS` (2026-08-18,
  CI-confirmed per the prior entry) stands unchanged and is not disputed - the finding above is about
  certified *scope*, not about the gates that exist being wrong.
- Known issues: the `ADR-0058` staleness described above (now corrected in this same pass).
- Unresolved questions / CEO decision required: **YES - exactly one.** Whether `PANCHANGA_V1`'s
  independently-coded-reference substitution for the external-oracle gate (tithi/yoga/karana) is
  accepted for Panchanga classification the same way the structurally identical substitution was
  explicitly ratified for rise/set in `ADR-0054`, OR whether a real PyJHora oracle gate must first be
  added and verified running in CI's `oracle` job (Linux, PyJHora already installed and already used by
  the eight existing varga oracle certifiers) before Panchanga classification can be described as
  meeting the FOUNDATION phase's own stated certification-gates requirement. Until one of those two
  paths is decided, `PANCHANGA_V1` should be described as **certified to the level actually evidenced
  (independently-coded reference, genuine negative control, protected holdout, dense sweep, ULP
  battery, independent validator - materially equivalent to C3 "independently externally cross-checked"
  is NOT yet met for the specific "external oracle" sense `DP-009`/`Q8` use, though C2 "implemented and
  internally validated" is comfortably met)**, not as having satisfied the full varga-template
  methodology `DP-009`/`ADR-0052` named for panchanga's classification parts.
- Next authorized action: **await the owner's decision on the oracle-gate question above.** No
  implementation change was made silently. If the owner ratifies the substitution (mirroring `ADR-0054`),
  the next Claude action is a narrow `ADR-0055`-addendum-style decision-log entry recording that
  ratification, and updating `certify_panchanga.py`'s docstring/`explicit_non_claims` to cite it instead
  of describing the gap as merely undecided. If the owner instead requires a real oracle gate, the next
  Claude action is a scoped implementation task to add and CI-verify a PyJHora-based Gate for tithi/
  yoga/karana/nakshatra, explicitly not authorized to begin without that decision.

### 2026-08-19 - Execution continuity rule drafted and committed (ADR-0058)
- Branch / commit SHA: `phase-g-governance`, `20a9589e3d567bbf86e36b13bf2d61ca734e728e` ("Formalize ACE
  execution continuity rule"). **Correction to this entry, made during the following task's mandatory
  session-start audit:** this entry originally read "NOT YET COMMITTED" / "no commit made," reflecting
  the state at drafting time; the owner committed the three files directly, and the commit's existence
  was confirmed at `HEAD` before the next task began. `docs/DECISION_LOG.md`'s `ADR-0058` Status line
  carries the matching correction.
- Previous approved commit: `300e6267a2738b160e140e502a8765ec1711935a`
- Task: owner-directed "ACE EXECUTION - PERSIST EXECUTION CONTINUITY GOVERNANCE" - add a permanent rule
  that ACE work continues past analysis/recommendation/partial-result stopping points until one of five
  terminal conditions (user input required, Claude input required with a complete instruction, blocked,
  CEO approval required, task complete) actually occurs.
- Relevant ADR/specification: `ADR-0058` (drafted, see status note - ACCEPTED in substance per the
  owner's direct instruction, but its file edit is uncommitted); `specs/CLAUDE_WORKFLOW.md` (new
  "Execution continuity" section, placed after `ADR-0057`'s sections).
- Files changed (working tree, uncommitted): `specs/CLAUDE_WORKFLOW.md` (1.2.0 -> 1.3.0),
  `docs/DECISION_LOG.md` (new `ADR-0058`, register header updated), `reports/AI_HANDOFF_CURRENT.md`
  (this entry).
- Implementation summary: new "Execution continuity (do not stop prematurely)" section added to
  `specs/CLAUDE_WORKFLOW.md`, same document `ADR-0057` used for the same class of procedural rule.
  States the five terminal stop conditions verbatim in substance, the "convert 'you should do X' into
  the next instruction" rule, and an explicit non-override clause: this rule governs response
  behaviour only, does not authorize anything governance hasn't already authorized, and does not
  weaken `docs/PROJECT_CONSTITUTION.md` s11 rule (a) (owner ratifies all decisions) - a CEO-approval
  checkpoint is not overridden by "keep going." `docs/PROJECT_CONSTITUTION.md` s11 and `ADR-0056`/
  `ADR-0057` not reopened.
- Tests executed and results: `python -m pytest -q` - see this task's execution report for the exact
  count; `scripts/check_adr_numbering.py`, `scripts/check_retired_identifiers.py`,
  `scripts/check_identifier_families.py` - run against the working tree (uncommitted state);
  `git diff --check` - run against the working tree.
- Certification executed and results: none applicable - governance/documentation only, no certified
  capability, gate, threshold, or evidence file touched.
- Known issues: none.
- Unresolved questions: none raised by this task.
- CEO decision required: no - the owner's own commit of `20a9589` closes the item that previously made
  this a pending decision.
- Next authorized action: none granted by this entry beyond what it implements.

### 2026-08-18 - Panchanga CI evidence recovery (KP_CHAIN/SIGN_CONVENTION/RISE_SET/PANCHANGA + oracle-tier)
- Branch / commit SHA: `phase-g-governance`, `695c387564cbd55e0908a730cc8b94f36ae41659`
- Previous approved commit: `389b98cc20e715edc8f9656a200b9e7f0d4bfb8c`
- Task: close the CI-sourced evidence-recovery follow-up for `KP_CHAIN_V1`, `SIGN_CONVENTION_V1`,
  `RISE_SET_V1`, `PANCHANGA_V1`, using the `ADR-0053`/`ADR-0054` evidence-recovery pattern.
- Relevant ADR/specification: `ADR-0053`, `ADR-0054`, `ADR-0055` (cited in the commit; no new ADR -
  matches the precedent commit `bd71e0d`, itself a plain evidence commit, not a new decision).
- Files changed: 26 files - 12 `certification/*.json` (`current_engine`, `KP_CHAIN_V1`,
  `SIGN_CONVENTION_V1`, `RISE_SET_V1`, `PANCHANGA_V1`, `VARGA_D2/D3/D7/D12/D30_V1`, `VIMSHOTTARI_V1`,
  `PARASHARI_DRISHTI_V1`, `TRANSIT_V1`) and their `reports/certification/*.console.txt`/`*.report.md`
  companions where those actually differed. No source code, no `.github/workflows/ci.yml`.
- Implementation summary: pushing `389b98c` surfaced (CI run `32136604550`) that Panchanga's addition
  legitimately grew M-03's anti-fitting scan surface `173 -> 177`, so every existing certification
  artifact's `preconditions.anti_fitting.modules_scanned` differed from committed HEAD - the same
  expected drift class `ADR-0053`/`ADR-0054` already documented. Downloaded
  `hermetic-certification-evidence-3.11`/`-3.12` and `oracle-certification-evidence` from that run;
  cross-compared 3.11 vs 3.12 (byte-identical outside volatile fields); diffed each against committed
  HEAD (identical except that one field, nothing else) before committing. Task named 4 artifacts; the
  8 oracle-tier artifacts share the identical cause/fix and were already downloaded, so recovered in
  the same commit rather than left CI-red - same already-ratified procedure, not new scope.
  `PANCHANGA_V1`'s own local (Windows) evidence was independently confirmed byte-identical to the
  CI-regenerated version before being replaced with the CI-sourced copy anyway, per instruction not to
  treat local-Windows as equivalent by assumption.
- Tests executed and results: `python -m pytest -q` - 778 passed, 0 failed, 0 skipped.
- Certification executed and results: none re-run in this task (evidence-recovery only, no code
  changed); `scripts/check_adr_numbering.py`, `scripts/check_retired_identifiers.py`,
  `scripts/check_identifier_families.py` - all PASS; `git diff --check` - clean.
- CI run identifier/evidence: GitHub Actions run `32136604550` (commit `389b98c`,
  `https://github.com/prashantkumar0207/astro-convergence-engine/actions/runs/32136604550`) - governance
  gate PASS; both hermetic-job legs (3.11, 3.12) and the oracle job passed every step except their
  drift-assertion step, which failed exactly and only on the expected `173 -> 177` field across all
  twelve artifacts (confirmed by direct log inspection, not assumed). Artifacts
  `hermetic-certification-evidence-3.11` (sha256 `43bbeaa0...`), `hermetic-certification-evidence-3.12`
  (sha256 `116e7007...`), `oracle-certification-evidence` (sha256 `04fb382f...`) downloaded and used as
  the source of the evidence committed here.
- Known issues: none. **CONFIRMED 2026-08-18 post-push:** `c16bf7f` (which carries `695c387`) was pushed
  and CI run `32143067593` (head SHA `c16bf7f`) completed with all four jobs GREEN - governance gate,
  oracle gate, and both no-oracle (3.11/3.12) legs, including every drift-assertion step ("43 evidence
  file(s) identical to the committed version outside the volatile fields") and `KP_CHAIN_V1`/
  `SIGN_CONVENTION_V1`/`RISE_SET_V1`/`PANCHANGA_V1`/`current_engine`'s own `RESULT: PASS`. Directly
  observed, not inferred.
- Unresolved questions: none.
- CEO decision required: **NO.**
- Next authorized action: this follow-up is closed. No new FOUNDATION capability (Rahu Kalam,
  Yamaganda, Gulika, element transition timing, or any later phase)
  is authorized by this entry.

### 2026-08-18 - CEO-audit HOLD remediation: ACE interaction mode and mandatory session-start audit
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry is committed in the same
  commit as the remediation it describes).
- Previous approved commit: `00319b7c6e249a36d675e5c3cf06f0576fe2aab8`
- Task: owner-relayed "ACE CEO AUDIT RESULT: HOLD" - three required protections not yet permanently
  encoded. Inspection found four of the six required rules already encoded by `ADR-0056`; the two
  genuinely missing were an ACE interaction/response mode for ChatGPT and a mandatory, shared
  session-start audit checklist. Explicit instruction: use the existing `specs/CLAUDE_WORKFLOW.md` /
  `CLAUDE.md` / `reports/AI_HANDOFF_CURRENT.md` / ADR governance, do not create a competing workflow.
- Relevant ADR/specification: `ADR-0057`; `specs/CLAUDE_WORKFLOW.md` (new "ACE interaction mode" and
  "Session-start audit (mandatory)" sections); `docs/PROJECT_CONSTITUTION.md` s11 / `ADR-0056`
  (cross-referenced for the role model, not reopened).
- Files changed: `specs/CLAUDE_WORKFLOW.md`, `docs/DECISION_LOG.md`, `reports/AI_HANDOFF_CURRENT.md`
  (this file). `docs/PROJECT_CONSTITUTION.md` and `CLAUDE.md` deliberately **not** touched - already
  correct per `ADR-0056`, not reopened.
- Implementation summary: `specs/CLAUDE_WORKFLOW.md` (1.1.0 -> 1.2.0) gained "ACE interaction mode"
  (execution/audit-first default, explanation only on request, use existing Git/handoff evidence
  rather than the owner relaying Claude's output, state genuine blockers briefly) and "Session-start
  audit (mandatory)" (branch, HEAD, working tree, relevant spec/ADR, this handoff file, last approved
  decision, unresolved questions - never infer approval), both cross-referencing `ADR-0056`'s role
  model rather than duplicating it. Original six-step per-tier workflow unedited.
- Tests executed and results: `python -m pytest -q` - 778 passed. `scripts/check_adr_numbering.py` -
  PASS, 57 entries. `scripts/check_retired_identifiers.py`, `scripts/check_identifier_families.py` -
  PASS. `scripts/check_artifact_drift.py` - PASS, 43 files unaffected. `git diff --check` - clean.
- Certification executed and results: none applicable - governance/documentation only; confirmed via
  the drift check above that no certification artifact changed.
- Known issues: none introduced by this entry.
- Unresolved questions: none raised by this entry. The untracked `.codex/`/`AGENTS.md` disposition
  noted in the prior entry remains open and unrelated to this remediation.
- CEO decision required: no - this entry implements an explicit CEO audit result the owner relayed.
- Next authorized action: none granted by this entry beyond what it implements. Panchanga's CI-sourced
  evidence-recovery follow-up (noted in the prior entry) remains separate and not yet executed.

### 2026-08-18 - ACE governance change: formal four-role AI collaboration model
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry is committed in the same
  commit as the role-model change it describes).
- Previous approved commit: `f885693d5169ec6656337476d598202ea3c2c18e`
- Task: owner-directed "ACE GOVERNANCE CHANGE - PERMANENT LLM ROLE SEPARATION" - formalize USER /
  CLAUDE / CHATGPT / CODEX roles, exclude Codex from the ACE workflow, establish this file as the
  canonical, disciplined Claude -> ChatGPT handoff.
- Relevant ADR/specification: `ADR-0056`; `docs/PROJECT_CONSTITUTION.md` s11; `CLAUDE.md`.
- Files changed: `docs/PROJECT_CONSTITUTION.md`, `docs/DECISION_LOG.md`, `CLAUDE.md`,
  `reports/AI_HANDOFF_CURRENT.md` (this file).
- Implementation summary: s11 rewritten from two-AI prose into the explicit five-point role model
  (rules a-d retained unchanged); `CLAUDE.md`'s "Your role here" updated to match; this file restructured
  to add the "Role model" section above and this "Task handoff log" section/template, and its stale
  2026-08-17 snapshot refreshed below. No production/calculation code touched.
- Tests executed and results: `python -m pytest -q`; `scripts/check_adr_numbering.py`;
  `scripts/check_retired_identifiers.py`; `scripts/check_identifier_families.py`; `git diff --check` -
  see this commit's message for exact pass/fail counts.
- Certification executed and results: none applicable - governance/documentation only, no certified
  capability touched.
- Known issues: none introduced by this entry.
- Unresolved questions: the untracked `.codex/`/`AGENTS.md` artifacts already present in this working
  tree (not created by this entry) are unaddressed by this entry - their disposition is a separate
  matter.
- CEO decision required: no - this entry implements an explicit, self-contained owner instruction.
- Next authorized action: none granted by this entry beyond what it implements. Panchanga's remaining
  FOUNDATION follow-up (CI-sourced evidence recovery for KP_CHAIN/SIGN_CONVENTION/RISE_SET/PANCHANGA's
  own oracle-tier gap; see `ADR-0055` and the commit preceding this one) remains a separate, already-
  authorized but not-yet-executed step, unrelated to this governance change.

## Snapshot as of the last update to this file (2026-08-19, refreshed after PANCHANGA_V1 Gate F was committed, pushed, and CI-confirmed) - verify before relying on any of this

- Branch: `phase-g-governance`. HEAD: `4177d6108236e64d07f6b23499307001f0d7c421` ("Add PyJHora external
  oracle gate for Panchanga V1"), pushed and equal to `origin/phase-g-governance`. CI run `32242462766`
  green on all four jobs (governance, no-oracle 3.11, no-oracle 3.12, oracle). **This entry's own overlay
  of the CI-sourced `PANCHANGA_V1` evidence (differing from the prior local commit only in the volatile
  `environment.python` field) is an uncommitted working-tree change as of this snapshot** - the next
  authorized action is to commit and push exactly that small evidence-only follow-up. **Not merged to
  `main`**, and `main` remains untouched.
- Most recent decisions: `ADR-0059` (PANCHANGA_V1 Gate F, genuine PyJHora external-oracle comparison for
  tithi/yoga/karana - CEO-approved, implemented, committed `4177d61`, pushed, **CI-confirmed green** under
  the hash-pinned oracle environment), `ADR-0058` (execution continuity rule, committed `20a9589`),
  `ADR-0057` (ACE interaction mode and mandatory session-start audit), `ADR-0056` (four-role AI
  collaboration model, Codex excluded), `ADR-0055` (Panchanga classification-only work authorized),
  `ADR-0054` (FOUNDATION rise/set, CERTIFIED), `ADR-0052` (DP-009 Option B: rise/set Tier-0, panchanga
  Tier-1).
- FOUNDATION status: rise/set CERTIFIED (`RISE_SET_V1`), CI-confirmed green. **Panchanga classification
  (tithi, nakshatra-reuse, yoga, karana, vara at a given instant) now certified with all six gates
  including Gate F (genuine PyJHora external-oracle comparison), CI-confirmed under the hash-pinned
  oracle environment (run `32242462766`)** - 66 comparisons, 0 mismatches, negative control verified,
  drift-check PASS (43 evidence files identical outside volatile fields). `certify_panchanga.py` now
  requires PyJHora unconditionally and runs as the ninth `oracle`-job certifier, matching the eight
  pre-existing ones; it can no longer run standalone in the `hermetic` job or on this Windows host
  without PyJHora. **Panchanga classification now meets the `DP-009`/`ADR-0052`/`Q8_CLOSURE_MATRIX.md`
  s4 varga-template methodology for the scope `ADR-0055` authorized; a CEO checkpoint decision on
  formally accepting this as the per-capability FOUNDATION checkpoint is the open item** (see the latest
  task-log entry). Rahu Kalam/Yamaganda/Gulika and element start/end transition timing remain explicitly
  NOT authorized (`ADR-0055` items 2-3) and this determination does not extend to them.
- Known, permanent limitation: `swetest`- and PyJHora-dependent certifiers (now including
  `certify_panchanga.py`) cannot run on this Windows host. Not a regression if encountered there.
- Tier-0 is formally Locked per `ADR-0034`. Do not assume anything else carries that status without
  checking `docs/OPEN_QUESTIONS.md` Q17/Q18 and the specific decision entry.

## What to do if this file looks wrong

Trust `git log`, `docs/DECISION_LOG.md`, and `docs/OPEN_QUESTIONS.md` over this file, always. Update
this file's snapshot and task-handoff-log sections if you notice it's drifted or a task completed
without an entry, but that update is a courtesy to the next session/auditor, not itself a governance
act.

## Change history

| Version | Date | Change |
|---|---|---|
| 2.6.0 | 2026-08-19 | Committed (`4177d61`) and pushed the Gate F work; CI run `32242462766` green on all four jobs, oracle job confirmed Gate F genuinely executed (66 comparisons, 0 mismatches, negative control verified) under the hash-pinned environment; overlaid CI-sourced canonical evidence over the local one (differs only in the volatile `environment.python` field); added this task's entry with full CI evidence; refreshed the snapshot; flagged the remaining CEO checkpoint (formal per-capability acceptance). |
| 2.5.0 | 2026-08-19 | `ADR-0059`: CEO approved building a genuine PyJHora external-oracle gate (Gate F) for `PANCHANGA_V1`'s tithi/yoga/karana; implemented, locally verified (66/66 comparisons, negative control verified), certifier moved to the CI `oracle` job; added this task's entry; refreshed the snapshot. Uncommitted; CI verification pending. |
| 2.4.0 | 2026-08-19 | Panchanga production-certification checkpoint (audit only): corrected the prior 2.3.0 entry's stale "not yet committed" language now that the owner committed `ADR-0058` directly (`20a9589`); added this task's own entry recording one open CEO decision (Panchanga's missing external-oracle gate vs. `ADR-0054`'s ratified rise/set precedent); refreshed the snapshot to `20a9589`. |
| 2.3.0 | 2026-08-19 | `ADR-0058` drafted (execution continuity rule): added this task's "Task handoff log" entry recording an **uncommitted** working-tree change pending explicit owner commit authorization. Snapshot section not refreshed (no new commit exists yet to refresh it to). |
| 2.2.0 | 2026-08-18 | Panchanga CI evidence recovery: added this task's "Task handoff log" entry; refreshed the snapshot to `695c387`. Structure/status from 2.0.0 unchanged. |
| 2.1.0 | 2026-08-18 | `ADR-0057` (CEO-audit HOLD remediation): added this task's "Task handoff log" entry; refreshed the snapshot to `00319b7` (on top of `f885693`). "INDEX ONLY" status and role-model/task-log structure from 2.0.0 unchanged - this entry is itself an application of that discipline, not a structural change to it. |
| 2.0.0 | 2026-08-18 | `ADR-0056`: added the "Role model" section and the structured, templated "Task handoff log" section (this file is now explicitly the canonical Claude->ChatGPT handoff, not merely a snapshot index); refreshed the stale 2026-08-17 snapshot to `f885693` (FOUNDATION rise/set certified, Panchanga classification implemented and locally certified, `ADR-0047` G5 restoration, this entry itself). |
| 1.2.0 | 2026-08-17 | Snapshot refreshed after ADR-0046: HEAD `f3bec7f3e35d0eef93e115796ddb79ffea242723`, merge commit `d53787e` now noted as historical rather than current, CI run `32011431848` green, highest and latest ADR `ADR-0046` (ADR-0044/0045/0046 all ACCEPTED). Navigation/status sections unchanged. |
| 1.1.0 | 2026-08-17 | Snapshot refreshed post-merge: branch `phase-g-governance`, merge commit `d53787e75048dbadc1a2e3559cf42405c1d56661`, CI run `32007363289` green, highest ADR `ADR-0044` (ACCEPTED). Navigation/status sections unchanged. |
| 1.0.0 | 2026-08-17 | Created as part of the minimum AI-collaboration architecture implementation. |
