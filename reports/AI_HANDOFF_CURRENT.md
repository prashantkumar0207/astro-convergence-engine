<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | INDEX ONLY - navigation aid, not evidence. See "What this file is" below. |
| Version | 7.2.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-22 (ADR-0070 ratifies DP-017 Option 1 - H-06 CLOSED: certified dasha-profile allow-list + year_length_days type enforcement, implemented and tested) |
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

### 2026-08-22 - ADR-0070 ratifies DP-017 Option 1: certified dasha-profile allow-list + year_length_days type enforcement (H-06 CLOSED)
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the implementation).
- Previous approved commit: `e1334132416725dd75ee75cec06b94cd8cd521e6` (`DP-017` drafted) - unpushed,
  together with `0802247`/`bf66e48` beneath it. `main` (via PR #3, merge commit `0e1ef11`) is unaffected
  by this task.
- Task (owner's exact instruction): "CEO DECISION — DP-017 H-06. Ratify DP-017 Option 1. Build the
  certified Dasha-profile protection and type-safety enforcement described by Option 1." Scope: (1)
  `CERTIFIED_DASHA_PROFILES` allow-list; (2) `UnsupportedDashaProfileError` (or the exact type the
  implementation design specifies) for uncertified profiles; (3) enforce `year_length_days`
  type/representation so a float cannot silently enter certified Vimshottari arithmetic; (4) follow the
  certified-varga allow-list/refusal pattern where architecturally appropriate; (5) preserve existing
  certified Vimshottari values and the `VIMSHOTTARI_V1` certification artifact; (6) do not weaken any
  gate; (7) resolve DP-017's two open sub-questions (type-check location; allow-list keying) through the
  narrowest design consistent with existing architecture, recording the reasoning/provenance; (8) genuine
  tests for certified-accepted, uncertified-refused, invalid-`year_length_days`-refused, existing-behaviour-
  unchanged; (9) a genuine negative control; (10)-(12) do not touch H-08/M-02/dasha-boundary-proximity, do
  not begin general JATAKA, do not reopen FOUNDATION; (13) update `ACE_EXECUTION_STATE.md`/this file,
  preserving historical state; (14) run full tests, governance checks, relevant certification checks; (15)
  do not push without separate authorization; continue until the next genuine CEO decision, blocker, or
  push-authorization checkpoint.
- Relevant ADR/specification: `docs/decisions/DP-017-h06-dasha-profile-allow-list.md` (the decision-
  readiness paper this ratifies and implements); `docs/DECISION_LOG.md` `ADR-0070` (the ratifying entry,
  containing the full implementation and reasoning record - authoritative over this summary);
  `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` H-06 (the original finding); `engine/astrology/
  varga_registry.py`/`engine/astrology/__init__.py` (`CERTIFIED_PRODUCTION_VARGAS`/`UnsupportedVargaError`,
  the mirrored precedent); `engine/core/validation.py`/`engine/models/birth_data.py`
  (`validate_birth_data()`, the precedent resolving sub-question 1); `ADR-0053`/`ADR-0069` (H-04/H-05,
  not reopened).
- Files changed: `engine/dasha/profile.py` (added `UnsupportedDashaProfileError`,
  `CERTIFIED_DASHA_PROFILES`, `validate_dasha_profile()`); `engine/dasha/vimshottari.py` (import +
  one-line guard call in `vimshottari_from_moon()`); `engine/tests/test_vimshottari_profile_allow_list.py`
  (new, 7 tests); `docs/DECISION_LOG.md` (`ADR-0070` appended); `docs/decisions/
  DP-017-h06-dasha-profile-allow-list.md` (status header only, marked ADDRESSED); `docs/decisions/
  README.md` (`DP-017` row + change history); `docs/ACE_EXECUTION_STATE.md` (version 5.2.0); this file.
- Implementation summary: `validate_dasha_profile(profile)` performs two independent checks, in this
  order: (1) `isinstance(profile.year_length_days, Fraction)`, raising `UnsupportedDashaProfileError`
  naming the wrong type if it fails; (2) `profile in CERTIFIED_DASHA_PROFILES` (a tuple containing only
  `VIMSHOTTARI_MEAN_SIDEREAL_YEAR`), raising the same error naming what is certified if it fails. Keyed
  on the **full frozen instance** (relying on the dataclass's auto-generated field-by-field `__eq__`),
  not on `name` alone - resolving sub-question 2 by direct analogy to the B-01 lesson (a name-only check
  would let a same-named profile with a different, uncertified `year_length_days` through). The check
  lives in a **separate function**, not `DashaProfile.__post_init__` - resolving sub-question 1 by direct
  analogy to `validate_birth_data()`, this repository's own precedent for validating a frozen
  configuration dataclass via a usage-site function rather than a construction-time guard. Wired into
  `vimshottari_from_moon()` once, immediately after the existing depth-range check - the single choke
  point `vimshottari_from_snapshot()`, `vimshottari_parashari()`, and `vimshottari_kp()` all route
  through, so all four public entry points are covered by one call site.
- Tests executed and results: `python -m pytest -q` - **825 passed, 0 failed, 0 skipped** (up from 818 by
  exactly the 7 new tests in `test_vimshottari_profile_allow_list.py`): certified profile accepted
  directly and via the entry point; uncertified profile refused (both direct and via entry point); float
  `year_length_days` refused even under the certified profile's own name (both direct and via entry
  point); a well-typed-but-uncertified profile refused (proving the identity check, not just the type
  check, catches it); `CERTIFIED_DASHA_PROFILES` contains exactly the one certified instance; the
  existing certified computation (H-05/`ADR-0069`'s own frozen baseline values) reproduces exactly,
  unchanged.
- Negative control: the real `validate_dasha_profile(dasha_profile)` call was temporarily removed from
  `vimshottari_from_moon()` in this session (production code actually broken, not merely described);
  running the new test file then showed **exactly** `test_uncertified_profile_refused` and
  `test_float_year_length_refused` failing with "DID NOT RAISE `UnsupportedDashaProfileError`" on their
  entry-point assertions (their direct `validate_dasha_profile()` assertions still passed, since only the
  call site was removed, not the function). The line was restored; `git diff --stat` against the intended
  final state showed the file exactly as designed, nothing extra.
- Certification executed and results: `python scripts/certify_vimshottari.py`, run in the isolated
  PyJHora exploration venv (`oracle_probe_venv`, since PyJHora is unavailable in the main Windows
  environment) - **PASS, lord mismatches: 0**, unchanged from the pre-existing certified figures.
  Regenerating `certification/VIMSHOTTARI_V1_certification.json` and its console/report transcripts
  produced only the already-documented volatile-field diff (`date`, `environment.python`) plus the known
  Windows-path console-transcript backslash quirk (`certification\X.json` vs the committed
  `certification/X.json`) - discarded via `git checkout --`, not committed. `python
  scripts/certify_kp_chain.py` run as an M-03 anti-fitting scan-surface sanity check (modifying existing
  production files does not change `modules_scanned`; the new test file is excluded from the scan by
  construction) - PASS, same volatile-only diff, discarded.
- Governance checks executed and results: `python scripts/check_adr_numbering.py`,
  `python scripts/check_identifier_families.py`, `python scripts/check_retired_identifiers.py`,
  `git diff --check` - all PASS, both before and after the `docs/DECISION_LOG.md` edit.
  `python scripts/check_artifact_drift.py` - PASS, zero drift (the two regenerated-then-discarded
  certification transcripts left no trace).
- Known issues: none. The Windows-path console-transcript quirk is understood and not a defect (see
  `ADR-0070`'s own Evidence section and this session's prior occurrences for `KP_CHAIN_V1`).
- Unresolved questions: none for H-06. H-08 (owner-decision convention choice), M-02 (near-boundary Moon
  oracle cases), and the dasha boundary-proximity indicator remain open, each requiring its own separate
  owner authorization per the roadmap's established per-step order this session has followed throughout.
- CEO decision required: none to close out this task. The next genuine decision point is authorizing
  H-08 (or a different task), or authorizing a push of this task's commit.
- Next authorized action: none self-executable. Per the owner's own closing instruction, stop here and
  await the next genuine CEO decision, blocker, or push-authorization checkpoint.

### 2026-08-22 - DP-017 drafted: H-06 decision-readiness only, per JATAKA-entry authorization
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the paper).
- Previous approved commit: `0802247c1b92568d2e08aa0d744a91cf5426ed0f` (state-file updates recording
  the FOUNDATION -> `main` merge) - unpushed, together with `bf66e48` beneath it, none newly authorized
  for push. `main` (via PR #3, merge commit `0e1ef11`) is unaffected by this task.
- Task: "Authorize the next JATAKA-entry prerequisite: H-06 decision-readiness... Continue strictly
  according to DASHA_CERTIFICATION_ROADMAP.md's established order: H-06 -> H-08 -> M-02 -> Dasha
  boundary-proximity indicator," with an explicit sixteen-item scope (state audit; re-read `ADR-0068`/
  `ADR-0069`/`ACE_EXECUTION_STATE.md`; re-read `Q8_CLOSURE_MATRIX.md` s5; re-read the complete roadmap;
  inspect all existing H-06 evidence; independently establish the exact problem; classify it; identify
  all legitimate options; determine blast radius and certified-value impact; recommend an option only if
  the evidence supports one; draft a narrow decision paper; do not choose/ratify; do not implement; do
  not begin H-08/M-02/dasha-boundary-proximity/JATAKA; do not reopen FOUNDATION; do not push or merge).
- Relevant ADR/specification: `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` H-06 (the primary finding,
  re-read and independently re-verified in full); `docs/DASHA_CERTIFICATION_ROADMAP.md` (re-read in
  full, still `Status: PROPOSED`); `engine/astrology/varga_registry.py`/`engine/astrology/__init__.py`
  (the `CERTIFIED_PRODUCTION_VARGAS`/`UnsupportedVargaError` precedent H-06's own proposed solution
  names); `ADR-0053`/`ADR-0069` (H-04/H-05, not reopened).
- Files changed: `docs/decisions/DP-017-h06-dasha-profile-allow-list.md` (new), `docs/decisions/
  README.md` (`DP-017` registered), `docs/ACE_EXECUTION_STATE.md` (version 5.1.0), this file.
- **Pre-work performed exactly as mandated:** confirmed branch `phase-g-governance`, working tree clean,
  `origin/main` at `0e1ef11` and `origin/phase-g-governance` at `76ed443` unchanged since the merge task.
  Read `ADR-0068`/`ADR-0069`'s full text and `Q8_CLOSURE_MATRIX.md` s5 fresh. Read `docs/
  DASHA_CERTIFICATION_ROADMAP.md` in full - its own section 5 is the direct source for "follow the
  established order." Inspected, directly, not from memory: `engine/dasha/profile.py` (confirmed
  `DashaProfile` is a plain frozen dataclass with zero validation of any field); all four entry points
  in `engine/dasha/vimshottari.py` (confirmed each forwards `dasha_profile` unchecked); every `engine/
  tests/test_vimshottari_*.py` file (confirmed zero coverage of an uncertified profile or a float year
  length); `certification/VIMSHOTTARI_V1_certification.json`'s `explicit_non_claims` (confirmed it
  already correctly lists "year conventions other than the certified profile" as out of scope - the
  documentation is accurate, only the code enforcement is missing); `engine/astrology/varga_registry.py`
  and `engine/astrology/__init__.py` (the `CERTIFIED_PRODUCTION_VARGAS`/`UnsupportedVargaError` pattern
  H-06's own proposed solution names as the mirror target). Searched `docs/DECISION_LOG.md` and `docs/
  decisions/` for prior H-06 work: zero hits before this paper (only citations noting it remains open).
- **Independent reproduction, not trusted from the audit's own summary:** constructed
  `DashaProfile('i_made_this_up', Fraction(360), 'no source')` and passed it to `vimshottari_from_moon()`
  live - returned a fully-formed `VimshottariTimeline` with `dasha_profile_name: 'i_made_this_up'`, no
  exception. Separately constructed `DashaProfile('float_year', 365.25, 'no source')` (a Python `float`
  for `year_length_days`) - accepted identically, `type(t2.year_length_days)` confirmed `float`.
  Verified the exactness-destruction claim numerically, not just by type: `Fraction(7) * 365.256364`
  (the certified exact convention) versus `Fraction(7) * 365.25` (a plausible but wrong float
  substitute) produce different results (`2556.794548` vs `2556.75`) with **no exception raised either
  way** - Python's numeric tower silently promotes `Fraction * float` to float arithmetic. Searched the
  entire tracked tree for `DashaProfile(` construction sites: **exactly one**, the certified
  `VIMSHOTTARI_MEAN_SIDEREAL_YEAR` instance itself - confirming the gap is entirely latent in the
  current shipped tree, a materially different risk profile from H-05's own reachable mutation
  scenario (which had a concrete, documented injection point already in production code).
- Implementation summary (no code touched - decision-paper drafting only): drafted `DP-017`, structured
  to match this session's established DP template and the task's own explicit determination list.
  **Section A** (exact problem): `DashaProfile` enforces nothing - not the profile's certified identity,
  not the type of its own `year_length_days` field. **Section B** (classification): a certification/
  governance-scope gap combined with a type-safety gap, explicitly NOT a calculation defect - the
  certified profile computes correctly, and its own certification artifact's `explicit_non_claims`
  already correctly disclaims other conventions; the code simply doesn't enforce that documented scope.
  Two genuinely separate sub-gaps are kept distinct: profile-identity certification versus
  `year_length_days` type enforcement - a profile could fail either independently of the other.
  **Section C** (options): Option 1 (build `CERTIFIED_DASHA_PROFILES` + `UnsupportedDashaProfileError`,
  mirroring the varga-registry pattern precisely, plus type enforcement - with two openly-surfaced,
  unresolved sub-questions: where the type check lives, `__post_init__` versus entry-point; and how the
  allow-list is keyed) and Option 2 (defer, given the gap's confirmed latency). **Sections D/E/F**
  (certification implications, blast radius, certified-value impact): stated inline per option - Option
  1 touches only `engine/dasha/profile.py`, `engine/dasha/vimshottari.py`, and `engine/tests/`; zero
  certified-value impact under either option, confirmed directly (the certified profile's own
  `year_length_days` is already `Fraction`-typed and its `name` would trivially be the allow-list's sole
  entry). **Section G** (recommendation): Option 1 at **medium** confidence - explicitly weaker than
  `DP-016`'s own medium-high lean for H-05, because the gap is entirely latent (no reachable production
  path exercises it today) and two genuine implementation sub-questions remain open, unlike H-05 where
  the audit's proposed solution left almost nothing to design. **Section I** (exact owner decision):
  select Option 1 or Option 2; if Option 1, optionally specify a preference on either open sub-question,
  though neither requires owner input per se. No option is chosen by the paper; H-08, M-02, the dasha
  boundary-proximity indicator, and any JATAKA implementation are not started; FOUNDATION is not
  reopened.
- Tests executed and results: `python -m pytest -q` - **818 passed** (unchanged; no code touched).
- Certification executed and results: not applicable - no certified capability touched; `VIMSHOTTARI_V1`'s
  own certification artifact inspected only (its `explicit_non_claims` field), not regenerated.
- Governance checks executed and results: `python scripts/check_adr_numbering.py` - PASS, 69 entries
  unchanged; `python scripts/check_identifier_families.py` - PASS, 17 DP identifiers (up from 16, `DP-017`
  newly registered); `python scripts/check_retired_identifiers.py` - PASS, 0 violations, clean on the
  first pass; `git diff --check` - clean; `engine/tests/test_retired_identifier_gate_scope.py` - 36
  passed.
- Known issues: none.
- Unresolved questions: which of `DP-017`'s two options the owner selects for H-06, and (if Option 1)
  the two open implementation sub-questions, which may be left to implementation judgment.
- CEO decision required: **yes, one** - select Option 1 (build the allow-list and type enforcement) or
  Option 2 (defer) for H-06.
- Next authorized action: none self-authorized. Stopping here per the owner's own "continue until the
  genuine H-06 CEO decision point is reached" instruction - selecting an H-06 option is exactly that
  point. Nothing pushed; nothing merged; FOUNDATION not reopened; no certified dasha behavior modified;
  H-08/M-02/dasha-boundary-proximity/JATAKA implementation not started.

### 2026-08-22 - phase-g-governance MERGED into main (PR #3): FOUNDATION baseline now on main
- Branch / commit SHA: `main` at `0e1ef115a647b8a44bf4d1a7af2a3cf3a8b96e03` (the merge commit, pushed).
  `phase-g-governance` unchanged on the remote (`76ed443`); local `phase-g-governance` HEAD remains
  `bf66e484bbde10906596a614bf4ac17d83062d2e` (still unpushed, still not part of `main`, per instruction).
- Previous `main` SHA: `a3692e7191aa8f9debd2e9e9f0a9383d65096d37` (the PR #1 merge from 2026-08-13, `main`'s
  only commit since then).
- Task: "Approve merge of phase-g-governance into main at the CI-confirmed commit 76ed443. Use 76ed443
  as the merge source. Do NOT include local-only commit bf66e48. Do NOT push bf66e48. Do NOT start H-06
  yet. Perform the merge according to the repository's normal Git workflow," followed by a seven-item
  post-merge verification list (main's SHA; clean merge; clean working tree; origin/main synchronized;
  resulting CI status; FOUNDATION remains formally exited; no H-06/JATAKA work).
- Relevant ADR/specification: `ADR-0068` (FOUNDATION exit), `ADR-0069` (H-05) - both carried into `main`
  unchanged, neither reopened; `.claude/rules/git-safety.md`'s main-merge rule (explicit owner
  authorization for that specific action - given, and scoped to this exact commit).
- Files changed: `docs/ACE_EXECUTION_STATE.md`, this file (both on `phase-g-governance`, recording the
  merge - not part of the merge itself). The merge itself touched 131 files on `main` (already
  catalogued in the prior turn's merge-readiness audit).
- Implementation summary: found no open PRs (`gh pr list`). Created PR #3 (`gh pr create --base main
  --head phase-g-governance`) - since `bf66e48` was never pushed, `origin/phase-g-governance` was
  confirmed still exactly at `76ed443` (`gh pr view --json headRefOid`), so the PR automatically and
  correctly represented only the authorized commit, with no extra step needed to "exclude" `bf66e48` -
  it was simply never on the remote branch the PR was built from. This is the repository's own
  established normal workflow: PR #1 (2026-08-13) was the only prior `phase-g-governance` -> `main`
  merge, and it followed the identical pattern (a GitHub PR, merged as a standard two-parent merge
  commit, title "Merge pull request #N from .../phase-g-governance"). The PR's own creation triggered a
  fresh CI run (`32566896767`, `pull_request` event) - watched to completion, green, `headSha` confirmed
  `76ed443`. Merged via `gh pr merge 3 --merge` (explicit merge-commit strategy, not squash or rebase,
  matching the PR #1 precedent's own commit shape) with an explicit subject/body citing both CI runs and
  the source commit.
- **Post-merge verification, each item checked directly, not assumed:**
  1. `main`'s resulting SHA: `0e1ef115a647b8a44bf4d1a7af2a3cf3a8b96e03`, confirmed via `git fetch` +
     `git rev-parse origin/main` **and** independently via `git ls-remote origin main` (a direct remote
     query, not local cache).
  2. Merge completed cleanly: `gh pr view --json mergeCommit,mergedAt,mergedBy,state` confirms
     `state: MERGED`; `git show --format="%P"` on the merge commit shows exactly two parents,
     `a3692e7` (prior `main` tip) and `76ed443` (the authorized source) - a plain, conflict-free merge,
     matching the merge-readiness audit's own prediction that `main` had no independent work to conflict
     with.
  3. Working tree clean: confirmed on the local `phase-g-governance` branch, which the merge (a
     server-side GitHub operation) does not touch.
  4. `origin/main` synchronized: confirmed twice, via `git fetch` + `rev-parse` and via the independent
     `git ls-remote` query above - both agree.
  5. Resulting CI status: the push to `main` (created by the merge) triggered its own CI run
     (`32567048173`, `push` event, `headBranch: main`, `headSha: 0e1ef11`) - watched to completion,
     `conclusion: success`. Read the actual log, not just the checkmarks: both the 3.11 and 3.12
     `Default gate (engine/tests)` steps printed `818 passed`; the network-guard re-run also printed
     `818 passed`; both negative controls (`the identifier gate must actually fail`, `the numbering gate
     must actually fail`) printed their own "caught" confirmation; all three relevant drift-assertion
     steps printed `PASS: 46 evidence file(s) identical to the committed version outside the volatile
     fields`.
  6. FOUNDATION remains formally exited: `git show origin/main:docs/DECISION_LOG.md` directly confirms
     both `ADR-0068` and `ADR-0069` carry `Status: ACCEPTED` in `main`'s own new content - not inferred
     from the merge succeeding, read from the actual merged file.
  7. No H-06 or JATAKA work: none begun, none touched.
- Tests executed and results: none run locally this task (merge-and-verify only); CI's own `818 passed`
  (both interpreter legs, plus the network-guard re-run) on `main`'s new tip, read directly from the log.
- Certification executed and results: not applicable locally; CI's own `oracle gate (PyJHora, hash-
  pinned)` job on `main`'s new tip confirmed green with zero drift, read directly from its log.
- Governance checks executed and results: CI's own `governance gate (identifier families, document
  structure)` job on `main`'s new tip confirmed green, including both its negative controls genuinely
  firing.
- Known issues: none. Only the same Node.js 20 deprecation annotation noise already seen on every CI run
  this session, unrelated to this repository's own code.
- Unresolved questions: none technical.
- CEO decision required: no, for this entry itself (executes the owner's own merge authorization exactly,
  scoped to the exact commit named). A decision is needed only when the owner is ready to authorize the
  next Dasha-roadmap step.
- Next authorized action: none self-authorized. Per the owner's own explicit "Do NOT start H-06 yet"
  instruction, stopping here. `bf66e48` remains local-only and unpushed, exactly as instructed; H-06,
  H-08, M-02, the dasha boundary-proximity indicator, and any JATAKA implementation remain untouched.

### 2026-08-22 - H-05 (ADR-0069) pushed and CI-confirmed green, run 32565790781
- Branch / commit SHA: `phase-g-governance`, `76ed443bb9a1afa76abb42fab1e6a809c4d2ae9d` - **pushed**,
  confirmed identical to `origin/phase-g-governance` in both directions.
- Previous pushed commit: `e7adeb011b939ae5066faf866216bc5eb1834835`.
- Task: "H-05 implementation is accepted. Prepare the H-05 commit for remote verification. Do NOT merge
  phase-g-governance into main yet. Push authorization is granted for the H-05 commit: 76ed443... Push
  it to origin/phase-g-governance and wait for CI." Followed by an explicit five-step verification list
  (remote SHA; CI result; working-tree/branch sync; H-05 CI-confirmed; do not start H-06; do not merge to
  `main`).
- Relevant ADR/specification: `ADR-0069` (pushed, not re-examined); none reopened.
- Files changed: `docs/ACE_EXECUTION_STATE.md`, this file. No code, no new ADR - this task is push and
  verification only.
- Implementation summary: confirmed `76ed443` was exactly the current local HEAD before pushing (a plain
  fast-forward, no force needed, no divergence to reconcile). Ran `git push origin phase-g-governance`;
  it succeeded (`e7adeb0..76ed443 phase-g-governance -> phase-g-governance`), carrying the full chain of
  ten commits accumulated since the last push (`e7adeb0`) - covering H-01's fix, `DP-015`/boundary-
  proximity, FOUNDATION exit (`ADR-0068`), the `ADR-0063` addendum, and H-05 (`ADR-0069`) itself. Fetched
  and confirmed the remote SHA matches local HEAD exactly, in both directions (`git log origin..HEAD` and
  `git log HEAD..origin` both empty). Located the triggered CI run (`gh run list`), watched it to
  completion (`gh run watch --exit-status`), then independently confirmed its result via `gh run view
  --json status,conclusion,headSha`: `{"conclusion":"success","status":"completed","headSha":"76ed443..."}`.
  Went beyond the green-checkmark summary, per this session's own established discipline: read the actual
  CI log directly (`gh run view --log`) and confirmed both the 3.11 and 3.12 `Default gate (engine/tests)`
  steps printed `818 passed` - matching the local result exactly, proving the two new H-05 tests
  genuinely executed in CI, not merely that the suite as a whole happened to stay green. Also confirmed
  all three relevant drift-assertion steps (`no-oracle` x2, `oracle`) printed `PASS: 46 evidence file(s)
  identical to the committed version outside the volatile fields` - genuinely zero drift, the cleanest
  outcome of any push this session (no evidence-recovery overlay was needed, unlike several earlier
  episodes). Confirmed the working tree clean and the branch fully synced.
- Tests executed and results: none run locally this task (verification-only); CI's own `818 passed` (both
  interpreter legs) read directly from the log, as above.
- Certification executed and results: not applicable - no certification work this task; CI's own oracle
  job (`oracle gate (PyJHora, hash-pinned)`) confirmed green with zero drift, read directly from its log.
- Governance checks executed and results: CI's own `governance gate (identifier families, document
  structure)` job confirmed green.
- Known issues: none. Only CI annotation noise (Node.js 20 deprecation notices on `actions/checkout@v4`/
  `actions/setup-python@v5`/`actions/upload-artifact@v4`, unrelated to this repository's own code).
- Unresolved questions: none technical.
- CEO decision required: no, for this entry itself (executes the owner's own push authorization and
  verification instructions exactly). A decision is needed only when the owner is ready to authorize the
  next Dasha-roadmap step or a `main` merge.
- Next authorized action: none self-authorized. Per the owner's own explicit "Do NOT start H-06 yet,"
  "Do NOT merge into main yet," and "stop at the next genuine repository-governance checkpoint"
  instructions, stopping here. `main` untouched; H-06/H-08/M-02/dasha boundary-proximity not started;
  FOUNDATION and H-01 through H-05 not reopened.

### 2026-08-22 - ADR-0069: DP-016 Option 1 implemented - H-05 CLOSED (hermetic Vimshottari anchor baseline + verified negative control)
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the implementation).
- Previous approved commit: `9ce096c4960975889a7a7b93b27134af7b17ad3f` (`DP-016` drafted, H-05
  decision-readiness only) - unpushed, together with `c221c3f`, `1706a8f`, `b2f696d`, `d026467`,
  `381f6e3`, `7a363e5`, `6a560e1`, `d2a780c` beneath it, none newly authorized for push.
- Task: "CEO DECISION — DP-016 H-05. Ratify DP-016 Option 1: Build the frozen hermetic Vimshottari
  baseline plus the genuine negative control for H-05," with twelve explicit scope constraints: implement
  only what Option 1 requires; do not change shipped calculation or certified values; freeze from
  independently established correct behavior; add a genuine negative control against the known anchor
  sign-flip; preserve existing oracle certification/artifacts; follow `ADR-0053`'s successful pattern; do
  not weaken any gate; do not touch H-06/H-08/M-02/dasha boundary-proximity; do not begin JATAKA; run
  relevant tests; update state records; continue to the next genuine decision point; do not push without
  separate authorization.
- Relevant ADR/specification: `ADR-0069` (new); `DP-016` section E (the analysis this implements);
  `ADR-0007` (`VIMSHOTTARI_V1`, not reopened beyond this additive test); `ADR-0053` (the H-04/M-03
  pattern this implementation deliberately mirrors).
- Files changed: `engine/tests/test_vimshottari_hermetic_baseline.py` (new), `docs/DECISION_LOG.md` (new
  `ADR-0069`, register header updated to 47 ACCEPTED), `docs/decisions/README.md` (`DP-016` marked
  ADDRESSED), `docs/decisions/DP-016-h05-hermetic-dasha-anchor-baseline.md` (header updated to reflect
  ratification, option text unedited), `docs/ACE_EXECUTION_STATE.md`, this file.
  `engine/dasha/vimshottari.py`, `certify_vimshottari.py`, and `VIMSHOTTARI_V1_certification.json`:
  **not touched** in the final committed state (see the in-session mutation-and-revert below).
- Implementation summary: five frozen seed cases (moon longitudes `5.0`/`100.0`/`213.7`/`355.0`/
  `45.6789`, four of them reusing exact values already independently documented elsewhere in this test
  suite - `test_balance_identity`, `test_jd_view_is_consistent_with_exact_offsets`, `test_determinism`,
  `test_wraparound_lord_cycle_from_late_nakshatra` - plus one fresh case; birth JD `2451545.0`, this
  suite's existing J2000.0 convention). **Sourcing methodology, resolving `DP-016`'s own open
  sub-question per the owner's "freeze from the independently established correct behavior"
  instruction:** each expected value was computed by a standalone script re-deriving the anchor formula
  independently (not by calling `vimshottari_from_moon` and trusting its output), then cross-checked to
  match the production function's actual current output exactly, byte-for-byte, for all five cases and
  both fields checked (`anchor_jd`, second-mahadasha `start_jd`) - freezing behaviour already
  independently established correct by `VIMSHOTTARI_V1`'s own oracle-tier gate (`ADR-0007`), not
  re-deriving a fresh correctness claim. `test_hermetic_baseline_matches_frozen_anchor_and_second_
  mahadasha` asserts exact equality against these frozen values, hermetically. `_mutated_anchor_jd()` is
  a local, deliberate reimplementation of the audit's documented mutation (`engine/dasha/
  vimshottari.py:122`'s `-` flipped to `+`) - never imported by production code.
  `test_anchor_sign_flip_negative_control` asserts the mutation produces a >100-day difference for every
  case, then re-asserts the real function still matches frozen.
- **Negative control independently verified beyond what the test file itself proves:** the real
  production line was actually edited in place during this session (`birth_jd - float(...)` ->
  `birth_jd + float(...)`), the new test file was run and both tests **failed** as expected - the
  failure's actual `anchor_jd` value (`2452503.7979555` for the `ashwini_three_eighths_elapsed` case)
  matched the independently pre-computed mutated value exactly - then the line was reverted and
  `git diff --stat engine/dasha/vimshottari.py` confirmed zero diff, byte-identical to the committed
  version. This proves the gate genuinely detects H-05's own documented defect class, not merely that a
  parallel calculation disagrees with itself.
- **Certification impact verified directly, not merely predicted:** `scripts/certify_vimshottari.py` and
  `certification/VIMSHOTTARI_V1_certification.json` were not touched by the implementation - confirmed by
  `git status` showing no changes to either. M-03 anti-fitting scan-surface impact confirmed by reading
  `scripts/certification_support.py::_source_files()` directly: it excludes any path with `"tests"` in
  its parts or a `test_`-prefixed name, matching the new file on both counts. Ran `scripts/
  certify_kp_chain.py` locally (the only certifier runnable without PyJHora on this Windows host) as a
  live sanity check; its regenerated artifact differed from the committed one only in the already-
  understood volatile fields (`date`, `environment.python`) plus a known Windows-path-separator
  console-transcript quirk (the same class of finding already documented once earlier this session) -
  discarded via `git checkout --`, not committed.
- Tests executed and results: `python -m pytest -q` - **818 passed** (up from 816; the two new tests).
  Also directly observed both new tests **failing** against the real, temporarily-mutated production
  code (see above), then passing again after the revert - the strongest form of "this gate actually
  works" evidence used in this session to date.
- Certification executed and results: `certify_vimshottari.py` not run (requires PyJHora, unavailable on
  this host; not needed since nothing oracle-tier changed). `certify_kp_chain.py` run as a sanity check
  only (see above) - PASS, regenerated evidence discarded as volatile-only drift.
- Governance checks executed and results: `python scripts/check_adr_numbering.py` - PASS, 69 entries (up
  from 68, `ADR-0069` newly allocated); `python scripts/check_identifier_families.py` - PASS, 16 DP
  identifiers unchanged; `python scripts/check_retired_identifiers.py` - PASS, 0 violations;
  `git diff --check` - clean; `engine/tests/test_retired_identifier_gate_scope.py` - 36 passed;
  `python scripts/check_artifact_drift.py` - PASS, 46 files identical outside volatile fields (after
  discarding the sanity-check regeneration).
- Known issues: none.
- Unresolved questions: none technical. H-06, H-08, M-02, and the dasha boundary-proximity indicator
  remain open per the Dasha roadmap's own order; none was started, per the owner's explicit scope limits.
- CEO decision required: no, for this entry itself (implements the owner's own ratification exactly).
  A decision is needed only when the owner is ready to authorize the next Dasha-roadmap step.
- Next authorized action: none self-authorized. Per the owner's own "do not begin general Jataka
  implementation yet" and "do not modify H-06, H-08, M-02 or the dasha boundary-proximity item"
  instructions, no further step proceeds without the owner naming it. Nothing pushed; nothing merged to
  `main`; FOUNDATION not reopened; no certified calculation modified.

### 2026-08-22 - DP-016 drafted: H-05 decision-readiness only, the first authorized JATAKA-entry-prerequisite paper
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the paper).
- Previous approved commit: `c221c3f0729dc1a506ae2f75f3a4a2227f07eac0` (`ADR-0068` ratified, FOUNDATION
  formally exited; JATAKA readiness verified) - unpushed, together with `1706a8f`, `b2f696d`, `d026467`,
  `381f6e3`, `7a363e5`, `6a560e1`, `d2a780c` beneath it, none newly authorized for push.
- Task: "Authorize the next JATAKA-entry prerequisite work: H-05 decision-readiness only. Do NOT
  implement H-05 yet. Do NOT begin JATAKA implementation. Do NOT start H-06, H-08, M-02, or the dasha
  boundary-proximity indicator yet. Follow the existing DASHA_CERTIFICATION_ROADMAP.md order." Followed
  by an explicit five-step pre-work mandate (state audit; read `ADR-0068`/`ACE_EXECUTION_STATE.md`; read
  `Q8_CLOSURE_MATRIX.md` s5; read the complete `DASHA_CERTIFICATION_ROADMAP.md`; inspect all existing
  H-05 evidence, code, tests, certification gates, and prior decisions) and a ten-item determination list
  for the paper itself.
- Relevant ADR/specification: `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` H-05 (the primary finding,
  re-read and re-verified in full); `docs/DASHA_CERTIFICATION_ROADMAP.md` (re-read in full, still
  `Status: PROPOSED`); `ADR-0053` (H-04's own closure, the precedent for this exact class of work);
  `ADR-0007` (`VIMSHOTTARI_V1`, not reopened).
- Files changed: `docs/decisions/DP-016-h05-hermetic-dasha-anchor-baseline.md` (new), `docs/decisions/
  README.md` (`DP-016` registered), `docs/ACE_EXECUTION_STATE.md` (version 4.1.0), this file.
- **Pre-work performed exactly as mandated:** confirmed branch `phase-g-governance`, HEAD `c221c3f`,
  clean working tree, `origin/phase-g-governance` still at `e7adeb0` (`git fetch` run to confirm, not
  assumed). Read `ADR-0068`'s full text fresh (both the audit entry and its ratification follow-up) and
  `Q8_CLOSURE_MATRIX.md` s5 fresh. Read `docs/DASHA_CERTIFICATION_ROADMAP.md` in full (not excerpted) -
  its own section 5 "Recommended sequence" is the direct source for "follow the existing roadmap order."
  Inspected, directly, not from memory: `engine/dasha/vimshottari.py` (confirmed line 122's anchor
  formula unchanged since the audit); all four `engine/tests/test_vimshottari_*.py` files (found and read
  the exact JD-consistency and boundary tests the audit names); `validate_vimshottari_holdout.py` (read
  in full - confirmed its `compare()` function never reads a Julian Day, only `Fraction` year offsets);
  `scripts/certify_vimshottari.py` (confirmed unconditional PyJHora import, fail-closed `exit(3)`
  pattern, and that its oracle comparison does read `start_jd` against PyJHora's own independently-
  computed date - this is the one check that WOULD catch the mutation); `.github/workflows/ci.yml`
  (confirmed `certify_vimshottari.py` runs only in the `oracle` job, line 284, never `hermetic`);
  `certification/VIMSHOTTARI_V1_certification.json` (read its schema directly - no lettered gates, only
  oracle-derived fields; its `explicit_non_claims` list does not mention the hermetic-tier gap);
  `brihat_fixtures.py` (the established frozen-fixture precedent - confirmed it holds lord sequences,
  not JD-level instants, so it does not already contain what H-05 needs). Searched `docs/DECISION_LOG.md`
  for prior H-05 work: zero hits before this paper.
- Implementation summary (no code touched - decision-paper drafting only): drafted `DP-016`, structured
  to match this session's established DP template and to answer all ten items the owner's task listed.
  **Section A** (exact problem): the anchor computation has no hermetic-tier coverage that would
  independently confirm its correctness - every existing hermetic check is either self-referential
  (relative to the anchor under test) or structurally blind to Julian Days entirely. **Section B**
  (what "hermetic-tier protected baseline" means): defined by direct reference to this repository's own
  established pattern (`brihat_fixtures.py`, the H1-H11 holdout reused across many certifiers) - a
  committed, independently-sourced, versioned set of expected instant values, checked without PyJHora or
  network access. **Section C** (what the sign-flip demonstrates): both a coverage gap and a
  methodological point that every current hermetic check is, with respect to absolute correctness,
  exactly the kind of self-referential test `.claude/rules/validation.md` itself warns against.
  **Section D** (classification): a certification/governance coverage gap combined with a genuinely
  missing baseline - explicitly NOT a calculation defect, since the shipped formula is confirmed correct
  today. **Section E** (options): Option 1 (build the frozen baseline + negative control, the audit's own
  proposed solution, with two openly-surfaced but unresolved sub-questions - data source, and whether to
  bundle with H-06 - neither answered by this paper) and Option 2 (defer, optionally documenting the gap
  in `explicit_non_claims`). **Sections F/G/H** (certification implications, blast radius, certified-value
  impact): stated inline per option - Option 1 touches `engine/tests/` only, no certifier or artifact
  schema change, and independently confirmed zero certified-value impact (not merely quoting the
  roadmap's own claim, but verifying it against the actual JSON schema and architecture). **Section I**
  (recommendation): Option 1 at medium-high confidence - higher than this session's typical decision-
  paper confidence, because the fix is audit-authored, architecturally identical in class and risk
  profile to H-04/M-03's already-successful `ADR-0053` closure, and JATAKA's own entry criteria name it
  with no textual opening for a `DP-015`-style decoupling (`Q8_CLOSURE_MATRIX.md` s5's wording is a
  plain, non-alternative list, unlike s4's H-01/H-02 carve-out - explicitly noted as a reason NOT to
  invite that treatment here). **Section J** (exact owner decision): select Option 1 or Option 2; if
  Option 1, optionally specify a data-source preference, though this does not require owner input per se.
  No option is chosen by the paper; H-06, H-08, M-02, and the dasha boundary-proximity indicator are not
  started; JATAKA is not implemented.
- Tests executed and results: `python -m pytest -q` - **816 passed** (unchanged; no code touched).
- Certification executed and results: not applicable - no certified capability touched; `VIMSHOTTARI_V1`'s
  own certification artifact inspected only, not regenerated or modified.
- Governance checks executed and results: `python scripts/check_adr_numbering.py` - PASS, 68 entries
  unchanged; `python scripts/check_identifier_families.py` - PASS, 16 DP identifiers (up from 15, `DP-016`
  newly registered); `python scripts/check_retired_identifiers.py` - PASS, 0 violations, clean on the
  first pass; `git diff --check` - clean; `engine/tests/test_retired_identifier_gate_scope.py` - 36
  passed.
- Known issues: none.
- Unresolved questions: which of `DP-016`'s two options the owner selects for H-05, and (if Option 1) the
  data-source sub-question, which may be left to implementation judgment.
- CEO decision required: **yes, one** - select Option 1 (build the frozen hermetic baseline and negative
  control) or Option 2 (defer) for H-05.
- Next authorized action: none self-authorized. Stopping here per the owner's own "continue the research
  and decision-readiness work until the genuine CEO decision point is reached" instruction - selecting an
  H-05 option is exactly that point. Nothing pushed; nothing implemented; FOUNDATION not reopened; no
  certified dasha behavior modified; H-06/H-08/M-02/dasha boundary-proximity/JATAKA implementation not
  started.

### 2026-08-22 - ADR-0068 RATIFIED: FOUNDATION IS FORMALLY EXITED. JATAKA readiness verified: 5 of 6 Dasha-roadmap entry steps remain unmet
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the changes).
- Previous approved commit: `1706a8fde893f99550210cde03dbac6d78dcb661` (`ADR-0068` drafted, PROPOSED;
  fresh FOUNDATION-exit readiness audit) - unpushed, together with `b2f696d`, `d026467`, `381f6e3`,
  `7a363e5`, `6a560e1`, `d2a780c` beneath it, none newly authorized for push.
- Task: "CEO RATIFICATION — FOUNDATION EXIT. I ratify ADR-0068 and declare FOUNDATION EXITED, exactly as
  written in commit 1706a8f. Record the ratification exactly through the repository's prescribed
  decision-log/ADR mechanism... Do NOT modify any certified calculation. Do NOT reopen any completed
  FOUNDATION item. Do NOT reinterpret the Q8 exit criteria further. Do NOT treat this as authorization
  for JATAKA implementation... update ACE_EXECUTION_STATE.md; update AI_HANDOFF_CURRENT.md; verify the
  resulting repository state; identify the exact Q8 §5 JATAKA entry prerequisites that remain unmet;
  prepare the next authorized decision/readiness task for JATAKA entry; do not implement Jataka until
  its governing entry prerequisites are satisfied and authorized."
- Relevant ADR/specification: `ADR-0068` (ratified, status-only edit); new "Ratification of `ADR-0068`:
  FOUNDATION formally EXITED (2026-08-22)" follow-up subsection (new); `Q8_CLOSURE_MATRIX.md` s5
  (JATAKA, re-read fresh); `docs/DASHA_CERTIFICATION_ROADMAP.md` (re-read fresh, still `PROPOSED`);
  `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` H-05/H-06/H-08/M-02 (re-read fresh for accurate citation);
  `ADR-0053` (H-04's own prior closure, discovered this task, not previously connected to the JATAKA
  question in this session's own record).
- Files changed: `docs/DECISION_LOG.md` (`ADR-0068`'s `Status:` line edited PROPOSED->ACCEPTED, nothing
  else in that entry touched; new ratification follow-up subsection; register header version/ACCEPTED
  count/"Still PROPOSED" list/summary paragraph updated), `docs/ACE_EXECUTION_STATE.md`, this file.
  `ADR-0068`'s own Context/Decision/Consequences/Evidence text: **not touched**, matching the same
  discipline just used for the `ADR-0063` addendum.
- **Part 1 - ratification recorded:** added a "#### Ratification of `ADR-0068`: FOUNDATION formally
  EXITED (2026-08-22)" subsection quoting the owner's exact instruction as evidence, then edited only
  `ADR-0068`'s own `Status:` bullet from `PROPOSED - drafted per the owner's own instruction...` to
  `ACCEPTED, on the owner's ratifying instruction recorded in [...] this entry's own text`. Updated the
  register header: `ACCEPTED (45)` -> `ACCEPTED (46)`, range extended to `ADR-0068`, `ADR-0068` removed
  from "Still PROPOSED," and the summary paragraph now states plainly: "FOUNDATION IS FORMALLY EXITED AS
  OF 2026-08-22."
- **Part 2 - repository state verified fresh:** `python -m pytest -q` - 816 passed; `python scripts/
  check_artifact_drift.py` - PASS, 46 files identical outside volatile fields; `git status --short
  certification/` - clean; all four governance gates (`check_adr_numbering.py` - 68 entries;
  `check_identifier_families.py`; `check_retired_identifiers.py`; `git diff --check`) - PASS. No code
  touched, so this is confirmation, not new evidence.
- **Part 3 - JATAKA's exact unmet entry prerequisites, identified individually, not assumed from the
  roadmap document's own summary:** `Q8_CLOSURE_MATRIX.md` s5's entry criteria read: "The Dasha roadmap's
  steps 1 to 6 complete: depth-3 gate, frozen dasha baseline, profile allow-list, the H-08 convention
  decision, near-boundary Moon cases, boundary-proximity indicator." Checked each against the current
  repository state directly:
  - **Step 1 (H-04, Vimshottari depth-3 oracle gate): CLOSED.** `ADR-0053` (2026-08-17, `Status:
    ACCEPTED`) remediated this already, with real CI evidence (oracle job PASS, `oracle_pratyantar_rows_
    compared: 16038`, `oracle_lord_mismatches: 0`) - discovered this task by searching the decision log
    for any prior H-04/H-05/H-06/H-08/M-02 work, not previously connected to "JATAKA readiness"
    explicitly in this session's own record, since it was originally authorized as FOUNDATION *entry*
    gate-integrity work, which happens to be the identical finding the Dasha roadmap's own step 1 names.
  - **Step 2 (H-05, no hermetic-tier protected dasha baseline): OPEN.** `reports/
    G1_ARCHITECTURE_AUDIT_2026-08-11.md` H-05: flipping the anchor sign at `engine/dasha/
    vimshottari.py:122` injects a 4,748-day error into every dasha date and passes every oracle-free
    gate - only the PyJHora oracle job catches it, and "no committed numeric baseline of dasha calendar
    dates exists anywhere in the repository." Confirmed still true: no frozen-baseline test found in
    `engine/tests/test_vimshottari*.py`.
  - **Step 3 (H-06, no dasha-profile allow-list): OPEN.** H-06: `vimshottari_parashari(birth,
    dasha_profile=DashaProfile('i_made_this_up', ...))` returns a fully provenance-stamped timeline -
    nothing rejects it, unlike the varga layer's `CERTIFIED_PRODUCTION_VARGAS`/`UnsupportedVargaError`
    pattern. Confirmed still true: `grep -n "CERTIFIED_DASHA_PROFILES\|UnsupportedDashaProfileError"
    engine/dasha/*.py` - zero matches.
  - **Step 4 (H-08, boundary-convention owner decision): OPEN.** H-08: the KP layer's `[start, end)`
    exact-rational boundary convention is exported into the Parashari-labelled dasha layer via a shared
    `Decimal(str(x))` conversion rule, with no owner decision on record for which convention a
    Parashari-seeded dasha should actually follow. This is explicitly an owner decision, not a builder
    choice, per the audit's own framing.
  - **Step 5 (M-02, no near-boundary Moon oracle cases): OPEN.** M-02: the Vimshottari certification's
    two "boundary" cases sit 6.46 and 5.0 degrees from the nearest nakshatra boundary - farther than a
    case not labelled as one - so the oracle gate has zero genuine near-boundary Moon coverage in "the
    layer where boundary proximity has the largest downstream effect."
  - **Step 6 (dasha-specific boundary-proximity indicator): OPEN.** No mechanism exists anywhere in
    `engine/dasha/` resembling KP's own `nearest_boundary_arcsec` field - confirmed by the same search
    `DP-015` already ran for the FOUNDATION-scope item. This is explicitly a **different** requirement
    from the FOUNDATION-scope "boundary-proximity indicators" item `ADR-0067` already decoupled - `DP-015`
    section 2 itself notes the two are related but textually distinct, so `ADR-0067`'s decoupling does
    **not** close this JATAKA-entry step.
  - **Net: 1 of 6 steps closed, 5 open.** `docs/DASHA_CERTIFICATION_ROADMAP.md` itself remains `Status:
    PROPOSED` throughout - its own document ratification is not itself required to work a given step
    (H-04's own closure, `ADR-0053`, happened without ever ratifying the roadmap document), but no step
    beyond H-04 has been authorized or attempted.
- **Part 4 - next authorized decision/readiness task, prepared, not executed:** per the owner's own
  explicit "do not implement Jataka until its governing entry prerequisites are satisfied and
  authorized" instruction, **no step is begun**. The roadmap's own recommended sequence (`docs/
  DASHA_CERTIFICATION_ROADMAP.md` section 5) orders the remaining five as: H-05 (cheapest, no owner
  decision embedded - pure gate-integrity work of the exact same class H-04/M-03 already closed) -> H-06
  (certified-profile allow-list, same varga-mirroring pattern) -> H-08 (genuine owner decision) -> M-02
  (near-boundary oracle cases) -> the dasha boundary-proximity indicator. This ordering is presented as
  the roadmap's own prior recommendation, not a new recommendation manufactured here, and is not acted
  on - it awaits the owner naming which step (if any) to authorize next.
- Tests executed and results: `python -m pytest -q` - **816 passed** (unchanged; no code touched).
- Certification executed and results: not applicable to this task - no certified capability touched;
  existing artifacts re-verified present and drift-free (see Part 2).
- Governance checks executed and results: `python scripts/check_adr_numbering.py` - PASS, 68 entries
  unchanged; `python scripts/check_identifier_families.py` - PASS, 15 DP identifiers unchanged;
  `python scripts/check_retired_identifiers.py` - PASS, 0 violations; `git diff --check` - clean;
  `engine/tests/test_retired_identifier_gate_scope.py` - 36 passed.
- Known issues: none.
- Unresolved questions: which (if any) Dasha-roadmap step the owner wants pursued next, and in what
  order - this task does not decide or recommend beyond restating the roadmap's own prior sequencing.
- CEO decision required: **yes, one** - name which Dasha-roadmap step (H-05, H-06, H-08, M-02, or the
  dasha boundary-proximity indicator) to authorize next, if any, or direct different work entirely.
- Next authorized action: none self-authorized. Stopping here per the owner's own "continue until the
  next genuine CEO decision or blocker" instruction - naming a JATAKA-readiness step is exactly that
  decision point. Nothing pushed; nothing merged to `main`; JATAKA not started; no certified calculation
  touched; no completed FOUNDATION item (rise/set, panchanga, `TRIKALAM_V1`, H-01, H-02, boundary-
  proximity indicators, civil-date rendering) reopened.

### 2026-08-22 - ADR-0063 addendum ratified; fresh FOUNDATION-exit readiness audit finds no remaining gap; ADR-0068 (FOUNDATION-exit determination) drafted, PROPOSED
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the changes).
- Previous approved commit: `b2f696d48985918206a6954a75d8867b4e6cacd6` (proposed `ADR-0063` addendum,
  civil-date rendering) - unpushed, together with `d026467`, `381f6e3`, `7a363e5`, `6a560e1`, `d2a780c`
  beneath it, none newly authorized for push.
- Task: "CEO RATIFICATION — ADR-0063 ADDENDUM. I ratify the proposed ADR-0063 addendum exactly as
  written in commit b2f696d... Change only the addendum's status from PROPOSED to ACCEPTED through the
  appropriate follow-up decision-log entry, exactly as the addendum specifies." Followed by: update the
  state files; perform the complete FOUNDATION-exit readiness audit against Q8, verifying every scope
  item individually; do NOT declare FOUNDATION exited unless the audit actually establishes all exit
  conditions are satisfied; if it does, record the exact evidence and prepare the formal exit
  determination; do not start JATAKA yet; do not merge to `main`; do not push without separate
  authorization.
- Relevant ADR/specification: the proposed `ADR-0063` addendum (ratified, status-only edit); new
  "Ratification of the proposed `ADR-0063` addendum" follow-up subsection (new); new `ADR-0068` (drafted,
  `Status: PROPOSED`); `Q8_CLOSURE_MATRIX.md` s4/s5 (re-quoted fresh); every FOUNDATION-relevant ADR
  re-verified directly (`ADR-0054`, `ADR-0059`+addendum, `ADR-0060`/`ADR-0061`+addendum, `ADR-0063`+
  addendum, `ADR-0064`-`ADR-0067`).
- Files changed: `docs/DECISION_LOG.md` (addendum's `Status:` line edited PROPOSED->ACCEPTED, nothing
  else in the addendum touched; new ratification follow-up subsection; new `ADR-0068`; register header
  version/summary/"Still PROPOSED" list updated), `docs/ACE_EXECUTION_STATE.md`, this file. `ADR-0063`'s
  own original text and `docs/decisions/DP-012-civil-date-rendering-dasha-boundaries.md`: **not touched**.
- **Part 1 - ratification recorded:** added a "#### Ratification of the proposed `ADR-0063` addendum
  (2026-08-22)" subsection quoting the owner's exact instruction as evidence, then - per the owner's own
  "change only the addendum's status" wording - edited **only** the addendum's `Status:` bullet, from
  `PROPOSED - drafted at the owner's explicit request, not yet ratified` to `ACCEPTED, on the owner's
  ratifying instruction recorded in the [...] entry immediately below`. No other line of the addendum
  (Context, the ten decision terms, Consequences, Evidence, the "Exact CEO ratification required"
  paragraph) was touched. `ADR-0063`'s own pre-existing text remains completely unedited above it.
- **Part 2 - fresh FOUNDATION-exit readiness audit** (re-verified directly against current repository
  state, not reused from the prior task's own conclusions): re-confirmed all four relevant certification
  artifacts present and `result: PASS` with zero uncommitted drift (`RISE_SET_V1`, `PANCHANGA_V1`,
  `TRIKALAM_V1`, `TRANSIT_V1`; `check_artifact_drift.py` - PASS, 46 files); re-confirmed every relevant
  ADR's `Status: ACCEPTED` directly by grep, not memory (`ADR-0054`, `ADR-0059` + its checkpoint
  addendum, `ADR-0060`/`ADR-0061` + its checkpoint addendum, `ADR-0063` + its now-ratified addendum,
  `ADR-0064`, `ADR-0065`, `ADR-0066`, `ADR-0067`); re-quoted `Q8_CLOSURE_MATRIX.md` s4's exact exit
  criteria and its six implementation-scope items fresh. **Finding: every one of the six items now has a
  settled, ratified disposition** - rise/set, panchanga, `TRIKALAM_V1` certified and checkpointed; H-01
  resolved via the exit criteria's own named carve-out (reading confirmed `ADR-0067`); H-02 resolved and
  certified; boundary-proximity indicators and civil-date rendering both explicitly, narrowly decoupled
  from this specific checkpoint by their own ratified owner decisions (`ADR-0067`, and the just-ratified
  `ADR-0063` addendum, respectively). **The audit finds no remaining gap.**
- **Part 3 - `ADR-0068` drafted, `Status: PROPOSED`, not self-ratified:** presents the full item-by-item
  evidence trail above and states "if ratified, this entry would declare: FOUNDATION's exit criteria...
  are satisfied, and FOUNDATION is EXITED." Per the owner's own explicit caution ("do NOT declare
  FOUNDATION exited unless the audit actually establishes...") and `Q8_CLOSURE_MATRIX.md` s4's own "CEO
  approval: ...exit" requirement (exit needs the owner's own explicit ratification, exactly like entry
  and every per-capability checkpoint before it), this entry does **not** itself declare FOUNDATION
  exited - it is prepared and presented for the owner's review and explicit decision, matching the exact
  same "prepare, present, stop" pattern used for the `ADR-0063` addendum itself. The Consequences section
  explicitly states this would **not** authorize JATAKA: `Q8_CLOSURE_MATRIX.md` s5's own entry criteria
  additionally require "the Dasha roadmap's steps 1 to 6 complete" - `docs/
  DASHA_CERTIFICATION_ROADMAP.md` remains `Status: PROPOSED` and none of its six steps is done, so JATAKA
  stays unentered regardless of `ADR-0068`'s own fate. `phase-g-governance` is not merged to `main`.
- Tests executed and results: `python -m pytest -q` - **816 passed** (unchanged; no code touched).
- Certification executed and results: verified fresh, not reused - all four relevant certification
  artifacts present, `result: PASS`, `check_artifact_drift.py` clean (46 files), `git status --short
  certification/` clean.
- Governance checks executed and results: `python scripts/check_adr_numbering.py` - PASS, **68 entries**
  (up from 67 - `ADR-0068` newly allocated; the ratification follow-up is a subsection, not a new
  number); `python scripts/check_identifier_families.py` - PASS, 15 DP identifiers unchanged;
  `python scripts/check_retired_identifiers.py` - PASS, 0 violations; `git diff --check` - clean;
  `engine/tests/test_retired_identifier_gate_scope.py` - 36 passed.
- Known issues: none.
- Unresolved questions: exactly one - whether `ADR-0068`'s FOUNDATION-exit determination, as drafted, is
  acceptable for ratification, or needs further amendment.
- CEO decision required: **yes, one** - ratify (or further amend) `ADR-0068`. The form required,
  matching the `ADR-0063`-addendum precedent just used: an explicit instruction such as "I ratify
  `ADR-0068` and declare FOUNDATION exited, exactly as written in commit `<SHA>`," which would then be
  recorded as its own follow-up entry changing `ADR-0068`'s `Status` line from `PROPOSED` to `ACCEPTED` -
  `ADR-0068`'s own text would not be edited to record that.
- Next authorized action: none self-authorized. Stopping here per the owner's own "do not start JATAKA
  yet... do not merge to `main` yet... do not push without separate push authorization... continue until
  the next genuine CEO decision, blocker, or completion point" - ratifying `ADR-0068` is exactly that
  next decision point. Nothing pushed; nothing merged; JATAKA not started; H-01, H-02, `DP-012`, `DP-015`,
  Panchanga, `TRIKALAM_V1`, and boundary-proximity indicators not reopened or altered in any way.

### 2026-08-22 - Proposed addendum to ADR-0063 drafted: narrow civil-date-rendering resolution, presented for ratification
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the addendum).
- Previous approved commit: `d026467e4fc23a0cd15704b1af7d9d58fe5ae1b5` (`ADR-0067`, `DP-015` fully
  ratified; FOUNDATION-exit readiness audit) - unpushed, together with `381f6e3`, `7a363e5`, `6a560e1`,
  `d2a780c` beneath it, none newly authorized for push.
- Task: "Resolve the remaining FOUNDATION-exit civil-date rendering issue narrowly... Prepare a narrow
  owner-decision amendment for `ADR-0063`/`DP-012`... The proposed resolution must explicitly establish
  [ten specific terms]... Do not implement civil-date rendering. Do not reopen `DP-012`'s technical
  investigation. Do not reinterpret Q8 silently... Prepare the exact proposed decision wording and
  identify the exact CEO ratification required. Do not push or declare FOUNDATION exited yet."
- Relevant ADR/specification: `ADR-0063` (unedited, addendum appended after it); `DP-012` (unedited, not
  reopened); `DP-015` section 3 / `ADR-0067` (the carve-out finding and its equivalent boundary-proximity
  treatment, reused as the direct template for this addendum's structure).
- Files changed: `docs/DECISION_LOG.md` (new "Proposed addendum to `ADR-0063`" subsection, `Status:
  PROPOSED`, plus a brief flag added to the register's own header summary paragraph), `docs/
  ACE_EXECUTION_STATE.md`, this file. `docs/decisions/DP-012-civil-date-rendering-dasha-boundaries.md`
  and `ADR-0063` itself: **not touched**, per the owner's explicit "do not reopen" instruction.
- Implementation summary (no code touched - decision-log addendum only): appended a new "### Proposed
  addendum to `ADR-0063`" subsection directly after `ADR-0063`'s existing text (which remains completely
  unedited above it), matching the exact structural precedent of the `ADR-0059`/`ADR-0061` checkpoint
  addenda - a dated, self-contained subsection under the same ADR number, not a new top-level ADR entry,
  since nothing about `ADR-0063`'s own substance is being changed, only qualified. Set `Status: PROPOSED
  - drafted at the owner's explicit request, not yet ratified`, since the owner asked me to prepare the
  wording, not ratify it. The Decision section states the owner's own ten points verbatim in substance,
  numbered to match: (1) civil-date rendering remains deferred; (2) not certified; (3) `ADR-0063`'s
  original claim of independently satisfying `Q8_CLOSURE_MATRIX.md` s4 must not be relied upon without
  this qualification, since it predates `DP-015`'s carve-out analysis; (4) explicitly tracked as future
  work; (5) does not gate the current FOUNDATION-exit checkpoint, by this explicit owner decision;
  (6) no existing certified calculation or value changes; (7) no current production capability may
  consume it as though certified; (8) any future consumer must, when specified, first certify the
  methodology or explicitly refuse/gate the dependency - a forward-binding rule, explicitly not a present
  code change, mirroring `ADR-0066`'s and `ADR-0067`'s equivalent terms; (9) this addendum does not
  specify or certify the methodology; (10) a future decision paper may establish it, reusing `DP-012`'s
  existing analysis rather than re-deriving it. The Context section is careful to state this addendum
  applies `ADR-0067`'s already-confirmed characterization (c) finding to this one item specifically,
  exactly as `ADR-0067` did for boundary-proximity indicators - it does **not** assert any new reading
  of Q8's carve-out scope, and the Consequences section repeats this explicitly ("does not resolve the
  general Question 2 characterization for any other FOUNDATION scope item"). Ends with an explicit "Exact
  CEO ratification required" line naming the form a ratifying instruction would need to take (matching
  `ADR-0067`'s own "I ratify... exactly as written in commit `<SHA>`" precedent).
- Tests executed and results: `python -m pytest -q` - **816 passed** (unchanged; no code touched).
- Certification executed and results: not applicable - no certified capability touched.
- Governance checks executed and results: `python scripts/check_adr_numbering.py` - PASS, 67 entries
  unchanged (this addendum is a subsection under `ADR-0063`'s existing number, not a new allocation);
  `python scripts/check_identifier_families.py` - PASS, 15 DP identifiers unchanged (`DP-012` not
  reopened, no new DP drafted); `python scripts/check_retired_identifiers.py` - PASS, 0 violations;
  `git diff --check` - clean; `engine/tests/test_retired_identifier_gate_scope.py` - 36 passed.
- Known issues: none.
- Unresolved questions: exactly one - whether the proposed addendum's exact ten-term wording is
  acceptable for ratification as drafted, or needs further amendment.
- CEO decision required: **yes, one** - ratify (or further amend) the proposed `ADR-0063` addendum's
  exact wording. The form required, matching `ADR-0067`'s own precedent: an explicit instruction such as
  "I ratify the proposed `ADR-0063` addendum exactly as written in commit `<SHA>`," which would then be
  recorded as a follow-up dated entry changing the addendum's own `Status` line from `PROPOSED` to
  `ACCEPTED` - the addendum's own text is not edited to record ratification, matching this repository's
  practice throughout.
- Next authorized action: none self-authorized. Stopping here per the owner's own "do not push or
  declare FOUNDATION exited yet" instruction - ratification of this addendum is the exact remaining step
  before a FOUNDATION-exit determination becomes available to make. Nothing pushed; nothing implemented;
  `ADR-0063` and `DP-012` untouched.

### 2026-08-21 - DP-015 fully ratified (ADR-0067); FOUNDATION-exit readiness audit: NOT yet satisfied
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the ADR).
- Previous approved commit: `381f6e3cd030b5098383d674b15cdc60fad80478` (`DP-015` v3.0.0, amended Option 3
  presented for ratification) - unpushed, together with `7a363e5`, `6a560e1`, `d2a780c` beneath it, none
  newly authorized for push.
- Task: "CEO RATIFICATION — DP-015 Q3. I ratify DP-015 §F 'Option 3 (AMENDED)' exactly as written in
  commit 381f6e3," together with re-confirmation of Q1/Q2. Then, per the owner's own numbered
  instructions: (1) record the ratification as an ADR, preserving the exact wording; (2) update the
  canonical state files; (3-6) do not implement, alter certified calculations, or reopen H-01/H-02/
  `DP-012`/Panchanga/Trikalam; (7-8) perform the complete FOUNDATION-exit readiness audit, verifying
  every remaining scope item explicitly; (9-10) determine whether FOUNDATION now satisfies its exit
  criteria and, if so, record that; (11) prepare the next milestone only if entry criteria explicitly
  authorize it, and do not begin JATAKA otherwise; (12) do not push without separate authorization;
  continue until a genuine CEO decision, blocker, external input, or completion point.
- Relevant ADR/specification: `ADR-0067` (new); `Q8_CLOSURE_MATRIX.md` s4 (re-verified line by line);
  `ADR-0054`/`ADR-0059`/`ADR-0061` (rise/set, panchanga, trikalam checkpoints, re-checked); `ADR-0063`
  (civil-date rendering, re-examined - the key finding).
- Files changed: `docs/DECISION_LOG.md` (new `ADR-0067`, register header updated to 45 ACCEPTED),
  `docs/decisions/README.md` (`DP-015` marked ADDRESSED), `docs/decisions/DP-015-...md` (header/section 0
  updated to record ratification - option texts themselves unedited), `docs/ACE_EXECUTION_STATE.md`, this
  file.
- **Part 1 - ratification recorded (`ADR-0067`):** all three questions recorded with the exact ratified
  "Option 3 (AMENDED)" wording preserved verbatim (block-quoted from commit `381f6e3`) inside the ADR
  itself, per the owner's explicit "preserve the exact ratified wording" instruction - not paraphrased.
  The original Option 3 text remains explicitly not ratified. `DP-015`'s own header/section 0 updated to
  point to `ADR-0067` as the binding record; the paper's substantive option text is otherwise unedited.
- **Part 2 - FOUNDATION-exit readiness audit, verified against the exact current repository state, not
  assumed from memory:** checked all six `Q8_CLOSURE_MATRIX.md` s4 implementation-scope items
  individually:
  - **Rise/set (`RISE_SET_V1`):** certification artifact confirmed present and `PASS`
    (`certification/RISE_SET_V1_certification.json`), no uncommitted drift. `ADR-0054`'s ratifying
    instruction ("CEO OWNER AUTHORIZATION - FOUNDATION RISE/SET... ratifying... the complete rise/set
    workstream") combined entry, implementation-review, and exit into one act, unlike Panchanga/
    Trikalam's later, separately-recorded checkpoint addenda - noted as a minor structural difference,
    not treated as a gap, since the owner explicitly reviewed and ratified the complete, already-
    certified evidence in one message.
  - **Panchanga classification (`PANCHANGA_V1`):** certified, `PASS`, and has an explicit, separately-
    recorded "evidence addendum to `ADR-0059` - owner acceptance of the Panchanga per-capability
    FOUNDATION checkpoint (2026-08-19)." Satisfied.
  - **Rahu Kalam/Yamaganda/Gulika (`TRIKALAM_V1`):** certified, `PASS`, and has an explicit third
    addendum to `ADR-0061` recording the owner's checkpoint acceptance. Only the seed variant
    (`PYJHORA_TRIKALAM_V1`) is authorized; a second variant is explicitly not - but the owner accepted
    the checkpoint with this exact scope already on record, so this is not a new gap. Satisfied.
  - **Civil-date rendering:** **NOT certified - explicitly deferred (`ADR-0063`).** Re-reading `ADR-0063`'s
    full text directly (not from memory) surfaced the audit's key finding: its own Consequences section
    states "this entry is the recorded reason it is not being pursued now, **satisfying s4's 'explicitly
    deferred by decision' language** rather than silently dropping it" - an assertion made 2026-08-20,
    **before** `DP-015` section 3's rigorous three-characterization analysis existed. That analysis
    (confirmed by the owner today as characterization (c), "genuinely ambiguous... do not silently
    extend it to unrelated FOUNDATION items") shows the "explicitly deferred by decision" clause is
    textually attached only to the H-01/H-02 sentence in `Q8_CLOSURE_MATRIX.md` s4's exit criteria, not
    a general license `ADR-0063` could safely invoke for any other scope item. `ADR-0063`'s own claim
    of "satisfying s4's language" is exactly the kind of silent generalization the owner just directed
    not be made - it was made in good faith with the analysis available at the time, but that analysis
    did not yet exist. **This is a genuine, unresolved gap, structurally identical to the one boundary-
    proximity indicators had before this session's work, now surfaced but not resolved.**
  - **H-01:** resolved via the deferral-with-blocking carve-out (`ADR-0066`), and the owner has now
    explicitly confirmed (`ADR-0067`) this reading is textually valid, though novel. Satisfied under the
    exit criteria's own named H-01/H-02 carve-out - this carve-out unambiguously applies to H-01 by name,
    unlike civil-date rendering.
  - **H-02:** resolved and certified (`ADR-0064`/`ADR-0065`), CI-confirmed green. Satisfied.
  - **Boundary-proximity indicators:** explicitly decoupled from the current FOUNDATION-exit checkpoint
    by the owner's own decision (`ADR-0067`, "Option 3 (AMENDED)" term 3: "do NOT gate the current
    FOUNDATION-exit CEO checkpoint"). Out of scope for this determination, by decision - not a blocker.
  - Also confirmed: `ADR-0017`'s C0-C5 taxonomy (final definitions in `ADR-0051`) is a general claim-
    classification framework, not an additional per-capability threshold beyond FOUNDATION's own stated
    certification-gates row, which rise/set/panchanga/trikalam already meet in full (multi-gate,
    external oracle, independent validator, negative controls, CI-confirmed).
- **Conclusion (task steps 9-10): FOUNDATION does NOT yet unambiguously satisfy its exit criteria.**
  Five of six scope items are satisfied (rise/set, panchanga, trikalam certified and checkpointed;
  H-01/H-02 resolved per their own named carve-out; boundary-proximity explicitly decoupled by decision).
  The sixth, civil-date rendering, rests on a claim of exit-criteria satisfaction that the owner's own
  subsequent, more rigorous ruling now calls into question. **No FOUNDATION-exit determination is
  recorded**, since one is not yet warranted - recording one now would risk exactly the "silent
  weakening of FOUNDATION certification" the owner has repeatedly guarded against this session. Per
  task step 11, **no JATAKA milestone preparation is begun** - its own prerequisite (FOUNDATION exit) is
  not yet met.
- Tests executed and results: `python -m pytest -q` - **816 passed** (unchanged; no code touched).
- Certification executed and results: verified all four relevant certification artifacts
  (`RISE_SET_V1`, `PANCHANGA_V1`, `TRIKALAM_V1`, `TRANSIT_V1`) present, `PASS`, and free of uncommitted
  drift (`git status --short certification/` clean; `check_artifact_drift.py` - PASS, 46 files identical
  outside volatile fields).
- Governance checks executed and results: `python scripts/check_adr_numbering.py` - PASS, 67 entries;
  `python scripts/check_identifier_families.py` - PASS, 15 DP identifiers unchanged; `python scripts/
  check_retired_identifiers.py` - PASS, 0 violations; `git diff --check` - clean.
- Known issues: none newly introduced. The civil-date-rendering gap identified is pre-existing (dates to
  `ADR-0063`, 2026-08-20) and only now surfaced by this session's more rigorous textual analysis.
- Unresolved questions: exactly one, load-bearing for FOUNDATION exit - does civil-date rendering's
  existing deferral (`ADR-0063`) satisfy FOUNDATION's exit criteria, given the carve-out's general reach
  is now confirmed genuinely ambiguous? This mirrors precisely the treatment boundary-proximity
  indicators just received (`DP-015`/`ADR-0067`) and could plausibly be resolved the same way - by an
  explicit, amended decision with the same class of safeguards (tracked, not certified, forward-binding
  consumer rule) - but this paper does not propose that unilaterally; it surfaces the question.
- CEO decision required: **yes, one** - resolve civil-date rendering's own exit-criteria sufficiency:
  either (a) explicitly confirm the existing `ADR-0063` deferral is sufficient as-is, (b) direct a
  narrow amendment mirroring `DP-015`'s "Option 3 (AMENDED)" treatment, (c) authorize implementation, or
  (d) some other explicit resolution. Once resolved, FOUNDATION-exit can be re-assessed.
- Next authorized action: none self-authorized. Stopping here per the task's own step 12 ("continue
  until a genuine CEO decision, blocker, required external input, or completion point is reached") -
  this is exactly that point. Nothing pushed; nothing implemented; H-01, H-02, `DP-012`, Panchanga, and
  `TRIKALAM_V1` not reopened or altered in any way.

### 2026-08-21 - DP-015 Q1/Q2 CEO-confirmed; original Option 3 rejected; amended Option 3 drafted, presented for ratification
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the paper).
- Previous approved commit: `7a363e5c8dd3a1a102270557bbec0b62c803bd6e` (`DP-015` v2.0.0, the three-
  question package) - unpushed, together with `6a560e1` and `d2a780c` beneath it, none newly authorized
  for push.
- Task: the owner responded to the three-question CEO decision package with: (1) Question 1 confirmed
  as drafted; (2) Question 2 confirmed as characterization (c), genuinely ambiguous, explicitly not to
  be silently extended; (3) an explicit verification request against five named safeguards for
  Question 3's Option 3, with instruction to STOP and present the exact conflict if any safeguard was
  missing rather than implementing or reinterpreting. That verification (prior turn) found two of five
  safeguards missing (explicit future-work tracking; protection against a future consumer silently
  assuming an uncertified signal exists) and stopped without recording anything. This task's owner
  instruction: do not ratify the original Option 3; prepare a narrow amended Option 3 incorporating
  eight specific terms; update `DP-015` only enough to present it clearly, preserving the original as
  historical/unratified text; do not implement anything; do not create a blocking mechanism for a
  nonexistent current consumer; do not push; then stop at the CEO ratification point and report the
  exact amended wording.
- Relevant ADR/specification: `DP-015` itself (amended, not re-investigated); `ADR-0066` (cited only as
  the structural pattern the forward-binding refusal rule mirrors prospectively, not touched);
  `ADR-0063`/`DP-012` (cited only to confirm it is still not treated as precedent).
- Files changed: `docs/decisions/DP-015-foundation-boundary-proximity-indicators.md` (v2.0.0 -> v3.0.0),
  `docs/ACE_EXECUTION_STATE.md`, this file. `docs/decisions/README.md` and `docs/DECISION_LOG.md`
  unchanged - no ADR is written yet, per the owner's own "stop at the CEO ratification point" instruction;
  ratification is a separate, subsequent step.
- Implementation summary (no code touched - decision-paper amendment only): renamed the original Option 3
  heading to "Option 3 (ORIGINAL TEXT - NOT RATIFIED, preserved for the record)," added a note stating
  the owner's verification found it silent on the two named safeguards and directed it not be ratified,
  and block-quoted the original text unedited beneath that note - matching this repository's practice of
  not silently rewriting a considered option. Added "Option 3 (AMENDED)" immediately after, with all
  eight of the owner's specified terms written as explicit, numbered decision terms: (1) boundary-
  proximity indicators remain an unresolved, explicitly tracked future capability within FOUNDATION scope;
  (2) not certified for any capability by this decision or anything currently in the repository; (3) does
  not gate the current FOUNDATION-exit checkpoint - FOUNDATION's other scope items proceed independently;
  (4) no future production capability may consume the signal as if certified - a forward-binding
  constraint on future work, explicitly not a present code change, since no current consumer exists;
  (5) any future consumer must, when specified, either first certify the methodology or explicitly
  refuse/gate that dependency - mirroring `ADR-0066`'s structured-refusal pattern prospectively, without
  building, naming, or implementing that mechanism now; (6) no existing certified value changes, matching
  the paper's existing section D/J; (7) this decision does not itself specify or certify any methodology;
  (8) a future decision paper determines the methodology when a consuming feature needs one. Updated
  section 0 (status banner: Q1/Q2 confirmed, Q3 amended-and-pending), section 5's table (Option 3 row now
  reflects the amended version and its selection under characterization (c)), section L (recommendation
  withdrawn/superseded by CEO direction, no independent recommendation offered on the owner's own terms),
  section M (adds "ratification itself" to what remains undecided), and section N (states the one
  remaining decision precisely: ratify or further amend "Option 3 (AMENDED)"'s exact wording). Header
  status/version bumped to reflect Q1/Q2 as CEO-confirmed and Q3 as pending ratification, not open.
- Tests executed and results: `python -m pytest -q` - **816 passed** (unchanged; no code touched).
- Certification executed and results: not applicable - no certified capability touched.
- Governance checks executed and results: `python scripts/check_adr_numbering.py` - PASS, 66 entries
  unchanged; `python scripts/check_identifier_families.py` - PASS, 15 DP identifiers unchanged;
  `python scripts/check_retired_identifiers.py` - PASS, 0 violations; `git diff --check` - clean;
  `engine/tests/test_retired_identifier_gate_scope.py` - 36 passed.
- Known issues: none.
- Unresolved questions: exactly one - whether "Option 3 (AMENDED)"'s exact wording (`DP-015` section F)
  is acceptable for ratification as drafted, or needs further amendment.
- CEO decision required: **yes, one** - ratify or further amend "Option 3 (AMENDED)"'s exact wording.
  Once ratified, the next steps (recording the ADR, updating state files fully, the FOUNDATION-exit
  readiness audit) follow - all explicitly deferred by this task's own scope.
- Next authorized action: none self-authorized. Stopping here per the owner's own explicit instruction
  ("stop at the CEO ratification point and report the exact amended decision wording") - this is exactly
  that point. Nothing pushed; nothing implemented; no blocking mechanism built for a nonexistent consumer.

### 2026-08-21 - DP-015 restructured into an explicit three-question CEO decision package
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the paper).
- Previous approved commit: `6a560e1f5e4c26546c702229186d340cc5b0273e` (H-01 re-verification; `DP-015`
  v1.0.0) - unpushed, together with `d2a780c` beneath it (H-01 fix Option 2, `ADR-0066`) - **both
  explicitly held back from push**, no new authorization given.
- Task: owner asked for a CEO decision package with three questions kept explicitly, structurally
  separate: (1) confirm the H-01/`ADR-0066` finding as textually valid but novel/unprecedented, not
  representing it as precedent; (2) resolve, from the exact ratified Q8 text, whether the deferral
  carve-out is limited to H-01/H-02, generally applicable, or genuinely ambiguous - with exact
  governing language, surrounding context, and consequences of each, without silently extending the
  carve-out; (3) present boundary-proximity indicators' legitimate treatment options and consequences
  once Question 2 is characterized, explicitly not implementing anything, not treating `DP-012`'s
  civil-date deferral as precedent, and not reopening H-01. No implementation, no ADR choosing an
  option, no push.
- Relevant ADR/specification: `DP-015` itself (restructured, not re-investigated); `ADR-0066` (restated
  only, not touched); `Q8_CLOSURE_MATRIX.md` s3/s4 (re-quoted verbatim); `ADR-0049` (Phase G precedent
  check, unchanged from the prior task); `ADR-0063`/`DP-012` (explicitly de-precedented).
- Files changed: `docs/decisions/DP-015-foundation-boundary-proximity-indicators.md` (v1.0.0 -> v2.0.0),
  `docs/ACE_EXECUTION_STATE.md`, this file. `docs/decisions/README.md` unchanged (DP-015's registration
  row/status did not need updating - still `OPEN, drafted`).
- Implementation summary (no code touched - decision-paper restructuring only): added a new section 0
  ("CEO decision package") stating all three questions in the owner's own terms with a single, precise
  "what the owner must decide" close. Added a new section 4 that restates Question 1 (the H-01/`ADR-0066`
  finding) unchanged from the prior task, explicitly marked "confirmation only - not reopened, not
  reconsidered," and explicitly states it "is not represented as precedent for anything else in this
  paper." Rewrote section 3 (Question 2) to quote the exact governing sentence, its immediate
  surrounding context (the implementation-scope row's own "Resolution of H-01... and H-02..." phrasing
  versus boundary-proximity indicators' bare, un-verbed clause; the certification-gates row defining what
  "production certified" actually requires; Phase G's structurally parallel exit criteria and how
  `ADR-0049` actually resolved it - full remediation, deferral never exercised), then names three
  characterizations explicitly - (a) limited to H-01/H-02 by name, (b) generally applicable to FOUNDATION
  scope, (c) genuinely ambiguous - each with its own textual support and consequences, selecting none.
  Added a structural argument that applies under any characterization: H-01/H-02 are defects in an
  already-built, reachable capability, where "block the dependent domain" names a concrete action (as
  `ADR-0066` did); boundary-proximity indicators was never built at all, so there is nothing reachable
  for a deferral decision to "block," weakening Option 2's textual fit even under the broad reading.
  Added section 5, a compact table cross-referencing each of the three Question-3 treatment options
  against each of Question 2's three characterizations. Revised Option 2 (defer) in section F to
  explicitly state `DP-012`/`ADR-0063` is "a prior case of the owner choosing this same kind of decision
  for a different FOUNDATION scope item" but is "explicitly NOT treated as precedent here that deferral
  satisfies FOUNDATION's exit bar," since under characterization (a) civil-date rendering's own deferral
  is exactly as textually open as this item's would be. Adjusted the Recommendation (section L) to make
  the same point and to make the lean's dependency on Question 2's answer explicit rather than implicit.
  Rewrote section N to state the three decisions in the owner's own numbering, matching section 0 exactly.
- Tests executed and results: `python -m pytest -q` - **816 passed** (unchanged; no code touched).
- Certification executed and results: not applicable - no certified capability touched.
- Governance checks executed and results: `python scripts/check_adr_numbering.py` - PASS, 66 entries
  unchanged; `python scripts/check_identifier_families.py` - PASS, 15 DP identifiers unchanged;
  `python scripts/check_retired_identifiers.py` - PASS, 0 violations, clean on first pass; `git diff
  --check` - clean; `engine/tests/test_retired_identifier_gate_scope.py` - 36 passed.
- Known issues: none.
- Unresolved questions: exactly the three the package states - nothing new raised, nothing resolved.
- CEO decision required: **yes, three, in order** - (1) confirm or correct the H-01/`ADR-0066` finding
  (`DP-015` s4); (2) characterize the Q8 deferral carve-out's reach - (a), (b), (c), or a stated
  alternative (`DP-015` s3); (3) select a boundary-proximity treatment option given that answer
  (`DP-015` s.F, cross-referenced in s5).
- Next authorized action: none self-authorized. Neither `d2a780c` nor `6a560e1` nor this task's own
  commit is pushed - no push authorization has been given for any of them. Stopping here per "stop only
  at the genuine CEO decision point" - `DP-015`'s three questions are exactly that.

### 2026-08-21 - H-01 independent re-verification; boundary-proximity-indicator investigation (DP-015)
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the paper).
- Previous approved commit: `d2a780cd7f0be31c1d18509a757b5b8225af032f` (H-01 fix Option 2, `ADR-0066`) -
  **explicitly held back from push** per this task's own instruction ("Do not push d2a780c yet").
- Task: owner asked for (1) an independent re-verification of the prior task's own H-01/`ADR-0066`
  Q8-exit-criteria reading, without modifying or reopening H-01 code, and (2) a decision-readiness
  investigation of the boundary-proximity-indicator gap only - no implementation, no ADR choosing an
  option, no push.
- Relevant ADR/specification: `ADR-0066` (re-examined, not edited); `Q8_CLOSURE_MATRIX.md` s4 (re-read
  verbatim); `ADR-0049` (Phase G's B-01/B-02/B-03 remediation, checked as precedent); `ADR-0006`/`ADR-
  0037` (KP_CHAIN_V1); `ADR-0027` (PROPOSED, cites H-07); `docs/DASHA_CERTIFICATION_ROADMAP.md`
  (PROPOSED); `docs/H7_BTR_SPEC.md` (checked, no mention of the concept).
- Files changed: `docs/decisions/DP-015-foundation-boundary-proximity-indicators.md` (new), `docs/
  decisions/README.md` (`DP-015` registered, version 2.4.0), `docs/ACE_EXECUTION_STATE.md` (version
  3.0.0), this file.
- **Part 1 - H-01 independent verification (no code touched, no ADR written):** re-read `Q8_CLOSURE_
  MATRIX.md` s4's exact ratified text directly rather than relying on the prior task's own paraphrase.
  The clause reads: "H-01 and H-02 resolved and certified, or explicitly deferred by decision with the
  dependent domains blocked accordingly." Confirmed `ADR-0066` satisfies this literally: it is a
  decision; the dependent domain (true-node transit-event search via `find_crossings()`) is blocked at
  the code level by `UnsupportedNodePolicyError`, which is stronger than a documentation-only deferral.
  New this task: checked whether any prior case in this repository's own history establishes this
  "deferred + blocked" pattern as something the owner has actually accepted before. Found `ADR-0049`
  (Phase G's own exit criteria offered an equivalent, even less restrictive, "resolved or explicitly
  deferred by decision" path for B-01/B-02/B-03) - but all three were fully REMEDIATED per `ADR-0049`,
  never actually deferred, so **no precedent exists** for the owner having accepted a hybrid,
  implemented-as-a-refusal (not a complete fix) treatment as satisfying an exit criterion. Conclusion:
  the reading is textually sound and unchanged from the prior task's own determination, but it is a
  **genuinely novel application**, not a settled or precedented one - restated with this additional
  finding rather than either strengthened or walked back.
- **Part 2 - boundary-proximity-indicator investigation (no implementation, no ADR):** confirmed via
  direct repository-wide search that **nothing ratified governs this FOUNDATION scope item at all** -
  unlike every other FOUNDATION-scope item, it has never appeared in any ADR, any prior decision paper,
  or any code. The only related material found: (a) `engine/kp/chain.py`/`engine/models/kp_chain.py`'s
  `nearest_boundary_arcsec` field (`ADR-0006`, KP_CHAIN_V1 - certified but explicitly stated NOT to be
  a Constitution s12 Locked artifact, distinct from the separately FORMALLY LOCKED Tier-0 scope which
  does not name it), which has its own unresolved defect - `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md`
  H-07, "blind to the sign boundary while its docstring claims all levels," re-verified directly against
  the live code (`chain.py:36-43`'s `nearest` computation has no thirty-degree term; `kp_chain.py:37-41`'s
  docstring claims "at any level") - H-07 is cited only inside `ADR-0027`, itself `Status: PROPOSED`, so
  it too has no ratified decision; (b) `docs/DASHA_CERTIFICATION_ROADMAP.md` (`Status: PROPOSED`),
  which discusses extending the concept to the dasha layer specifically - `Q8_CLOSURE_MATRIX.md` s5
  (JATAKA)'s own entry criteria separately cites this same roadmap item, meaning the FOUNDATION-exit
  item and the JATAKA-entry item are related but textually distinct requirements; (c) `docs/
  H7_BTR_SPEC.md` (BTR being the roadmap's stated primary downstream beneficiary) contains zero mentions
  of the concept, and BTR is phases away regardless (`Q8_CLOSURE_MATRIX.md` s13: orthogonal, reachable
  only after EVIDENCE exits). Drafted `DP-015` covering all six items the task asked to determine
  (Q8's exact requirement text; why it's in scope, assembled from the H-02/H-07/roadmap/BTR evidence
  above; that nothing prior governs it; three legitimate treatment options - implement for named
  capabilities, defer explicitly, or decouple from the exit checkpoint; a low-confidence lean toward
  deferral; and a statement that `DP-015` itself is judged the minimum paper needed, with a second,
  follow-up paper required only if Option 1 is chosen). **DP-015 s3 surfaces a genuinely new textual
  finding**: `Q8_CLOSURE_MATRIX.md` s4's "explicitly deferred... blocked accordingly" alternate path is
  textually scoped to H-01/H-02 by name in the second sentence, not the general rule the first sentence
  states for "every capability above" - meaning a bare deferral decision for boundary-proximity
  indicators (or, on this reading, civil-date rendering's ALREADY-recorded deferral, `ADR-0063`) may not
  by itself satisfy FOUNDATION's exit bar, unless the owner confirms the broader reading (matching Phase
  G's own less-restrictive, non-carved-out phrasing for B-01/B-02/B-03). This paper does not resolve
  that question - it belongs to the owner, and bears on more than just this one scope item.
- Tests executed and results: `python -m pytest -q` - **816 passed** (unchanged; no code touched, only
  decision/documentation files).
- Certification executed and results: not applicable - no certified capability touched.
- Governance checks executed and results: `python scripts/check_adr_numbering.py` - PASS, 66 entries
  unchanged; `python scripts/check_identifier_families.py` - PASS, 15 registered DP identifiers (up
  from 14, `DP-015` newly registered); `python scripts/check_retired_identifiers.py` - PASS, 0
  violations (clean on the first pass this time); `git diff --check` - clean; `engine/tests/
  test_retired_identifier_gate_scope.py` - 36 passed.
- Known issues: none.
- Unresolved questions: both of `DP-015` s.N's decisions, plus the H-01 novelty finding above, which the
  owner should weigh even though it does not change the technical conclusion.
- CEO decision required: **yes, three items** - (1) confirm or correct the H-01 independent-verification
  finding (the interpretation holds but is unprecedented); (2) `DP-015` s3's interpretive question
  (does explicit deferral close FOUNDATION exit for any scope item, or only H-01/H-02 by name - this
  also bears on civil-date rendering's existing deferral); (3) a `DP-015` treatment option for
  boundary-proximity indicators specifically (implement, defer, or decouple from the exit checkpoint).
- Next authorized action: none self-authorized. `d2a780c` remains unpushed per explicit instruction;
  this task's own commit is local-only. Stopping here per "stop at the genuine CEO decision point" -
  reached, since `DP-015`'s decisions and the H-01 confirmation are exactly that.

### 2026-08-21 - H-01 fix Option 2 implemented (ADR-0066): UnsupportedNodePolicyError; FOUNDATION-exit readiness audit
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the implementation).
- Previous approved commit: `cccdfadc87008209926eba84db1eb4fe2e6ff5e6` (H-01 decision-readiness/`DP-014`).
- Task: owner "Ratify DP-014 Option 2. Implement the ratified DP-014 Option 2 exactly as specified. Do
  not implement Option 1. Do not choose Option 3. Do not reopen H-02 or DP-012." - implement `DP-014`
  s.H's Option 2, then determine whether H-01 can be considered closed/deferred under
  `Q8_CLOSURE_MATRIX.md`, and if so perform a FOUNDATION-exit readiness audit.
- Relevant ADR/specification: `ADR-0066` (new); `DP-014` s.H (the analysis this implements); `ADR-0008`
  (`TRANSIT_V1`, not reopened beyond this additive guard).
- Files changed: `engine/transits/crossing.py` (`UnsupportedNodePolicyError(NotImplementedError)`,
  raised from `_resolve_body()` for `node_policy != NODE_POLICY_MEAN` on Rahu/Ketu; `find_crossings`'s
  algorithm itself untouched), `engine/tests/test_transit_crossing.py` (4 new tests), `docs/
  DECISION_LOG.md` (new `ADR-0066`, register header updated), `docs/decisions/README.md` (`DP-014`
  marked ADDRESSED), `docs/decisions/DP-014-h01-true-node-station-density.md` (one wording fix: "ADR-
  numbering" -> "decision-log renumbering", to clear the retired-identifier gate's Pattern B, which
  flags any `ADR-` token not followed by exactly four digits - caught by `test_retired_identifier_gate_
  scope.py`, not by my own pre-commit gate run, since that test scans the tracked tree and the file was
  still untracked at the time of my first manual check), `docs/ACE_EXECUTION_STATE.md`, this file.
- Implementation summary: the guard sits in `_resolve_body()`, the single point every `find_crossings()`
  call for a node body passes through, so it automatically covers every caller built on top of it
  (`sign_ingresses`, `nakshatra_ingresses`, `returns`, `natal_conjunctions`) without touching `engine/
  transits/events.py` at all - matching `DP-014`'s own description of Option 2's blast radius. The
  check is `!= NODE_POLICY_MEAN` (fail-closed on anything but the certified value), not `== "true"`
  (which would fail-open on some future third policy value), matching this repository's existing
  fail-closed convention (`engine/kp/chart.py`'s own `!= NODE_POLICY_MEAN` guard). Mean-node Rahu/Ketu
  resolution is otherwise byte-for-byte identical to before.
- Tests executed and results: `python -m pytest -q` - **816 passed** (up from 812; 4 new tests:
  refusal for Rahu under true-node, refusal for Ketu under true-node, a negative control confirming an
  unrelated body under the SAME true-node profile is unaffected, a negative control confirming the
  certified mean-node Rahu/Ketu path still produces events after the guard was added).
- Certification executed and results: `python scripts/certify_transits.py` (main environment, no
  PyJHora) - correctly `exit(3)`, matching every oracle-tier certifier. Same command in the isolated
  PyJHora exploration venv (`oracle_probe_venv`, already present from a prior session) - **PASS, all
  gates** (`declared_division: 49 cases, negative_control_verified=True`). Regenerating the artifact
  produced exactly one non-volatile diff: `gates.C_oracle_anchors.details[7].derived_tolerance_days`
  differing by a single ULP (`0.007236584941425451` -> `0.00723658494142545`) - the SAME field, same
  direction, as the `ADR-0065` evidence-recovery episode's own unpinned-venv-vs-CI-pinned-lock noise,
  confirming this is pre-existing environment noise, not caused by this change. Discarded the
  regenerated artifact (`git checkout --`) rather than committing it, since committing it would
  reintroduce noise CI's hash-pinned lock does not produce; `check_artifact_drift.py` confirms the
  committed evidence is untouched (46 files identical outside volatile fields).
- Governance checks executed and results: `python scripts/check_adr_numbering.py` - PASS, 66 entries;
  `python scripts/check_identifier_families.py` - PASS, 14 DP identifiers; `python scripts/check_
  retired_identifiers.py` - PASS (after the wording fix above); `git diff --check` - clean.
- Known issues: none.
- Unresolved questions: **the H-01/FOUNDATION-exit determination below is Claude's own reasoned
  interpretation of already-ratified text (`Q8_CLOSURE_MATRIX.md` s4's exit criteria), not itself a new
  ratification - it should be independently checked, not accepted purely on this entry's say-so.**
- **H-01 closure determination (task step 4):** `Q8_CLOSURE_MATRIX.md` s4's exit criteria read: "H-01
  and H-02 resolved and certified, or explicitly deferred by decision with the dependent domains blocked
  accordingly." `ADR-0066` is a decision; the dependent domain (true-node transit-event search) is now
  blocked at the code level by `UnsupportedNodePolicyError`, not merely deferred on paper - stronger
  than a documentation-only deferral. On this reading, **H-01 satisfies the exit criteria's explicit
  carve-out**. This is distinct from "resolved and certified" (which would require Option 1's complete
  fix with its own certification gate) - true-node transit search itself remains uncertified and is
  now actively refused, not working.
- **FOUNDATION-exit readiness audit (task step 5, performed since the determination above is that H-01
  is closed):** checked every item in `Q8_CLOSURE_MATRIX.md` s4's implementation scope directly against
  the decision log and repository state:
  - Rise/set: **CERTIFIED** (`RISE_SET_V1`, `ADR-0054`).
  - Panchanga classification (tithi/vara/nakshatra/yoga/karana): **CERTIFIED, checkpoint-accepted**
    (`ADR-0059` addendum).
  - Rahu Kalam/Yamaganda/Gulika (`TRIKALAM_V1`): **CERTIFIED, checkpoint-accepted** (`ADR-0061` third
    addendum).
  - Civil-date rendering for dasha boundaries: **explicitly DEFERRED by decision** (`ADR-0063`, `DP-012`
    Option C).
  - H-02: **resolved and certified** (`ADR-0064` reproduction, `ADR-0065` fix, CI-confirmed).
  - H-01: **resolved via the explicit-deferral-with-blocking carve-out** (`ADR-0066`, per the
    determination above).
  - Boundary-proximity indicators: **zero decision paper, zero ADR, zero implementation anywhere in the
    repository** - confirmed by grep across `docs/DECISION_LOG.md`, `docs/decisions/`, and `engine/`;
    the only repository mentions are the `Q8_CLOSURE_MATRIX.md` scope-listing citations themselves and
    prior-session notes recording that this item has never been authorized to proceed. **This is the
    one FOUNDATION-scope item with no path chosen at all** - not certified, not implemented, not even
    formally deferred by a decision entry - and is therefore the standing blocker to declaring
    FOUNDATION exit, independent of how the H-01 determination above is ultimately read.
- CEO decision required: **yes, two items** - (1) confirm or correct the H-01 Q8-exit-criteria reading
  above; (2) direct next steps for boundary-proximity indicators (author a decision paper, explicitly
  defer by decision, or otherwise), since FOUNDATION exit cannot be declared while that item has no
  decision of any kind on record.
- Next authorized action: none self-authorized. Per the task's own instruction to "stop only at the next
  genuine CEO decision or blocker" - the boundary-proximity gap is exactly that blocker, reached here.

### 2026-08-21 - H-01 decision-readiness: DP-014 drafted and registered
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the paper).
- Previous approved commit: `9737ddb7f0d6edac99b922f0816867eccd717820`.
- Task: owner "Continue Astro Convergence Engine from the LIVE repository state at e7adeb0... YOUR NEXT
  TASK IS H-01 DECISION-READINESS ONLY" - produce a narrow, evidence-driven H-01 decision paper without
  implementation-authorizing anything. H-02/`DP-013` explicitly not reopened; `DP-012` explicitly not
  revived.
- Relevant ADR/specification: none pre-existing for H-01 specifically (unlike H-02's `ADR-0020` D5,
  confirmed by direct grep of `docs/DECISION_LOG.md` - no ratified or proposed ADR item addresses H-01;
  only `Q8_CLOSURE_MATRIX.md`'s scope citation and two "does not extend to H-01" disclaimers in
  `ADR-0059`/`ADR-0061`). Primary source: `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` finding H-01.
- Files changed: `docs/decisions/DP-014-h01-true-node-station-density.md` (new), `docs/decisions/
  README.md` (DP-014 registered, version 2.2.0), `docs/ACE_EXECUTION_STATE.md` (version 2.8.0),
  this file.
- Implementation summary: re-verified the audit's H-01 finding live against `e7adeb0`, unchanged -
  `engine/transits/speeds.py`'s `grid_step_days("TrueNode")` is still exactly 37.5 days
  (`45.0 / (0.3 * 4.0)`), against a measured true-node station rate of roughly one per 6.25 days, so
  `find_crossings()`'s "at most one station per grid interval" correctness assumption is still violated
  for that body. Traced every one of the eight `node_policy` consumers in the repository directly
  (not assumed): confirmed `engine/astronomy/sidereal_planets.py` and `engine/astronomy/
  planet_collection.py` do plain dict/string lookups with no search algorithm (unaffected by H-01's
  mechanism); `engine/astronomy/astronomy_snapshot.py` and `engine/models/provenance.py` are
  pass-through/metadata only; `scripts/certify_current_engine.py` records `node_policy` in provenance
  output only; and - a new finding this session - `engine/kp/chart.py:51` already raises
  `KpProfileError("KP requires the mean node (Decision KP-B)")` whenever `node_policy != "mean"`, so KP
  independently hard-refuses true node regardless of anything this paper decides. Confirmed via grep
  that no test anywhere in `engine/tests/` exercises `NODE_POLICY_TRUE`. Confirmed neither shipped
  profile (`PARASHARI_LAHIRI`, `KP_KRISHNAMURTI`) selects true-node. `DP-014` presents the audit's own
  two proposed solutions (bound station spacing and re-size the grid; or gate the true-node path behind
  an explicit refusal) plus a third, defer-only option consistent with `DP-012`'s own precedent -
  no fourth, invented option. Recommends Option 2 (explicit refusal) at medium confidence, since it
  requires no new astronomical research and matches KP's own existing refusal precedent, while noting
  Option 1 remains the eventual complete fix and Option 3 is a legitimate zero-cost alternative.
  Decides nothing; not implementation-authorized.
- Tests executed and results: none run - no code changed, only documentation/decision-paper files.
  Governance/drift checks re-run instead (below).
- Certification executed and results: not applicable - no certified capability touched.
- Governance checks executed and results: `python scripts/check_adr_numbering.py` - PASS, 65 entries
  unchanged; `python scripts/check_identifier_families.py` - PASS, 14 registered DP identifiers (up
  from 13, `DP-014` newly registered); `python scripts/check_retired_identifiers.py` - PASS, 0
  violations; `git diff --check` - clean, no whitespace errors.
- Known issues: none.
- Unresolved questions: none technical. The owner's option selection among `DP-014`'s three options is
  the genuine open item this task's own terminal condition defines.
- CEO decision required: **yes** - select one of `DP-014`'s three options (bound station spacing and
  repair `find_crossings()` for the true node; gate the true-node path behind an explicit refusal; or
  defer, optionally with a documentation-only note), to be recorded as a new, numbered decision-log
  entry citing this paper. No option is implementation-authorized by this paper alone.
- Next authorized action: none self-authorized pending the owner's `DP-014` selection, or a different
  next task.

### 2026-08-21 - H-02/DP-013 fully closed: pushed, CI-green, one ULP-noise finding recovered
- Branch / commit SHA: `phase-g-governance`, `9737ddb7f0d6edac99b922f0816867eccd717820` - pushed,
  confirmed identical to `origin/phase-g-governance`.
- Previous approved commit: `09a9065b1ce8278b38597e4e68447028d4a97872`.
- Task: owner "Approve push 09a9065" then "Approve push 9737ddb" - pushed the H-02 fix implementation,
  diagnosed and recovered an incidental CI finding, pushed the fix, verified fully green.
- Relevant ADR/specification: `ADR-0065` (no edit needed - the finding was evidence provenance, not a
  decision); `ADR-0053`/`ADR-0054` (the evidence-recovery precedent reused).
- Files changed: `certification/TRANSIT_V1_certification.json` only (`reports/certification/transit.*`
  turned out byte-identical, so git recorded no change there).
- Implementation summary: pushing `09a9065` triggered CI run `32478112307`, which failed only on the
  drift-assertion step: `gates.C_oracle_anchors.details[7].derived_tolerance_days: 0.00723658494142545
  -> 0.007236584941425451` - a single ULP difference in a PyJHora-derived Gate C value (unrelated to
  Gate E or this session's actual work), caused by generating my local evidence in an unpinned
  exploration venv (matching this session's own established discipline) whose transitive dependency
  versions differ infinitesimally from CI's exact hash-pinned lock. Confirmed Gate E's own result was
  identical and correct in the CI-regenerated artifact (`{"cases_checked": 49, "negative_control_
  verified": true}`) before concluding this was evidence provenance, not a real defect. Downloaded
  `oracle-certification-evidence` from the failed run (still uploaded, `if: always()`) and overlaid it
  over the locally-committed file - exactly the `ADR-0053`/`ADR-0054` evidence-recovery pattern, applied
  here to a genuine floating-point ULP difference rather than the usual `modules_scanned` count. Pushed
  the recovery (`9737ddb`); CI run `32478694212` completed **all four jobs green**, Gate E re-confirmed
  executing from the log directly.
- Tests executed and results: `python -m pytest -q` - 812 passed (unchanged; no code touched by the
  recovery commit).
- Certification executed and results: `TRANSIT_V1` - PASS, all gates (A/C/D/E), CI-confirmed under the
  hash-pinned oracle environment, run `32478694212`.
- Known issues: none. The ULP-level Gate C sensitivity to unpinned-vs-pinned dependency versions is now
  a known characteristic of that gate's PyJHora-derived value, not a defect requiring further action.
- Unresolved questions: none.
- CEO decision required: no - this entry is evidence recovery, not a new decision.
- Next authorized action: none self-authorized. `DP-013`/H-02 is fully closed (reproduced, fixed,
  CI-confirmed). Awaiting the owner's next task - no FOUNDATION capability currently has both satisfied
  prerequisites and a ratified implementation decision.

### 2026-08-21 - H-02 fix Option 1 implemented (ADR-0065): TransitEvent.declared_division
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the implementation).
- Previous approved commit: `5a00dc6604c52ebcfb0a4da456571638e0c200a7`.
- Task: owner "Ratify H-02 Fix Option 1." - implement `DP-013` s6's recommended, ratified option.
- Relevant ADR/specification: `ADR-0065` (new); `DP-013` s6 (the analysis this implements); `ADR-0008`
  (`TRANSIT_V1`, not reopened beyond this additive change).
- Files changed: `engine/models/transit_event.py` (`declared_division: int | None = None`, additive),
  `engine/transits/events.py` (`sign_ingresses`/`nakshatra_ingresses` populate it via `dataclasses.
  replace()`; `find_crossings` itself untouched), `scripts/certify_transits.py` (new Gate E + a
  proactive `.as_posix()` console-transcript path fix, matching this session's established discipline),
  `engine/tests/test_transit_events.py` (4 new tests), `docs/DECISION_LOG.md` (new `ADR-0065`, register
  header updated), `docs/decisions/README.md` (`DP-013` marked ADDRESSED by both `ADR-0064`/`ADR-0065`),
  `docs/ACE_EXECUTION_STATE.md`, this file.
- Implementation summary: exactly matches `DP-013` s6's own analysis. `TransitEvent` gained the field
  with a default, so every existing `find_crossings()` construction call site is unchanged - no
  existing field's value or meaning changes. `sign_ingresses`/`nakshatra_ingresses` (the only two
  functions with a defined division scheme) classify `declared_division` from the EXACT `target_
  longitude`, using the same certified `zodiac_sign`/`nakshatra` every other capability already uses -
  never re-classifying the reported (residual-bounded) `julian_day`. `returns()`/`natal_conjunctions()`
  are untouched, leaving the field `None` where "division" has no defined meaning - avoiding Option 2's
  identified unscoped-call-site complication entirely, since Option 1 never needed `find_crossings`
  itself to know about divisions. `certify_transits.py`'s new Gate E asserts `declared_division` equals
  the certified classifier applied to the target for every Sun/Moon holdout case, asserts `None` for a
  plain crossing, and includes a genuine negative control (temporarily breaks `events.py`'s own
  classifier, confirms the same comparison would then fail to catch the disagreement, restores).
- Tests executed and results: `python -m pytest -q` - **812 passed** (up from 809; 4 new tests).
- Certification executed and results: `python scripts/certify_transits.py` (main environment, no
  PyJHora) - correctly `exit(3)`, matching every oracle-tier certifier. `python scripts/
  certify_transits.py` (isolated exploration venv, PyJHora 4.8.7) - **PASS, all gates (A/C/D/E)**: Gate
  E `{"cases_checked": 49, "negative_control_verified": true}`. M-03 anti-fitting scan surface confirmed
  unchanged (180 - only existing files edited, no new files added under `engine/`).
- Known issues: none.
- Unresolved questions: none technical. Options 2 and 3 remain formally un-chosen (not needed - Option 1
  is what was ratified).
- CEO decision required: no, for this entry itself (implements the owner's own ratification). CI
  confirmation of Gate E is the remaining evidence step.
- Next authorized action: push (needs its own authorization), then monitor CI specifically for Gate E
  executing under the hash-pinned oracle environment and report the result.

### 2026-08-21 - DP-013 fix-option decision-readiness analysis: Option 1 recommended, not chosen
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the analysis).
- Previous approved commit: `77e987b0f45a8c0560573729910eae9f048d6ad8`.
- Task: owner "ACE CONTINUE - H-02 FIX DECISION READINESS" - a narrow technical decision-readiness
  analysis of the three existing fix options only, no implementation, no fourth option, no choice made
  on the owner's behalf.
- Relevant ADR/specification: `DP-013` (v1.1.0 -> v1.2.0, new s6); `ADR-0005`/`ADR-0034` (Tier-0 Locked
  scope, directly re-verified, not assumed).
- Files changed: `docs/decisions/DP-013-h02-ingress-classification-seam.md`, `docs/ACE_EXECUTION_STATE.md`,
  this file. No engine code, no `TRANSIT_V1` change, nothing implemented.
- Implementation summary: verified by direct repository-wide search (not assumed) that `engine.transits`
  (`find_crossings`/`TransitEvent`/`sign_ingresses`/`nakshatra_ingresses`) has **zero production
  consumers today** - only its own certifier/validator and this session's H-02 tooling import it - while
  `division_index` feeds nearly every certified classifier (`house.py`, `nakshatra.py`, `pada.py`,
  `panchanga.py`, `signs.py`, `varga_classifier.py`). For each of the three fix options, determined:
  exact affected interfaces; certified-value impact (Option 1 none, Option 2 real - the certified event
  `julian_day`/`residual_arcsec` change - Option 3 the most severe, global); blast radius (Option 1
  `TRANSIT_V1` only; Option 2 `TRANSIT_V1`'s Gates A/B/C; Option 3 every certified capability);
  required tests (Option 1 a trivial-by-construction assertion plus negative control; Option 2 the full
  existing Gate battery plus a bias-boundedness test; Option 3 full recertification of every
  `division_index` consumer plus a harder negative control); and certification/checkpoint bar (Option 1
  a narrow `TRANSIT_V1` addendum; Option 2 a formal `TRANSIT_V1` change decision; Option 3 - **directly
  re-verified against `ADR-0005`/`ADR-0034`** - reopening the FORMALLY LOCKED Tier-0 scope, since its
  own text names "the certified D9/D10 divisional mathematics" as in-scope, the same mechanism
  `BOUNDARY_TOLERANCE` serves). Also flagged a genuine architectural complication for Option 2:
  `find_crossings` is also called by `returns()`/`natal_conjunctions()` with non-boundary targets, so a
  "bias toward target division" would need explicit scoping to avoid nonsensical application there.
  **Recommends Option 1 at high confidence** (zero certified-value impact, smallest blast radius, lowest
  governance bar); does not choose - the decision remains the owner's.
- Tests executed and results: none applicable - documentation/decision-paper analysis only.
- Certification executed and results: none applicable.
- Known issues: none.
- Unresolved questions: which fix option the owner ratifies (Option 1 recommended), or whether to defer.
- CEO decision required: not for this entry itself (analysis only, decides nothing). A future decision
  is needed to choose (or defer) a fix option.
- Next authorized action: push (needs its own authorization). Awaiting the owner's fix-option decision,
  or a different next task.

### 2026-08-20 - DP-013 Option C executed (ADR-0064): H-02 reproduced for the Sun; PyJHora recorded as a limitation
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the work).
- Previous approved commit: `0dae97657e3a46ebeb85cc796094e5d23c1b742c`.
- Task: owner "ACE EXECUTE - H-02 REPRODUCTION AUTHORIZED" - CEO ratified `DP-013` Option C (both A and
  B) as final for the reproduction methodology; execute now.
- Relevant ADR/specification: `ADR-0064` (new); `DP-013` (unedited); `ADR-0020` D5 (context, not
  reopened); `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` H-02 (the original finding being reproduced).
- Files changed: `scripts/reproduce_h02_ingress_seam.py` (new, Part A), `validate_h02_reproduction.py`
  (new, independent cross-check), `scripts/investigate_h02_pyjhora_precision.py` (new, Part B),
  `engine/tests/test_h02_reproduction.py` (new, 8 tests), `.github/workflows/ci.yml` (two new,
  non-gating steps), `reports/h02_reproduction/*.json` (new evidence artifacts), `docs/DECISION_LOG.md`
  (new `ADR-0064`, register header updated), `docs/ACE_EXECUTION_STATE.md`, this file. `TRANSIT_V1` and
  every other certified capability untouched.
- Implementation summary:
  **Part A** reuses only certified primitives (`engine.transits.events.sign_ingresses`/
  `nakshatra_ingresses` - TRANSIT_V1's own event-finder - and `sidereal_planet_position`) plus one new,
  independently-typed exact-rational (`Fraction`) classifier that never imports `division_index`. A
  second, separately-typed classifier in `validate_h02_reproduction.py` cross-checks via subprocess
  (Gate-E-style). A negative control (synthetic known-mismatch case, checked against the real classifier
  and a deliberately broken one, both at script level and again via `pytest` `monkeypatch`) proves the
  check can actually detect a defect. **Result: 2 of 12 Sun sign-boundary crossings (2024,
  `parashari_lahiri`, full year) misclassify - an EXACT match to the original audit's "2 of 12".** Moon
  (independently-selected 35-day window, not the audit's exact unstated one): 15 of 34 (44%), comparable
  to the audit's 12/28 (43%).
  **Part B** re-verified, with fresh timed measurements, two claims `certify_transits.py`'s own Gate C
  design rationale already recorded: PyJHora's search-based ingress detection converges stably at
  `precision` 0.001 degrees and coarser, but diverges to a wrong answer or is bounded out by this
  investigation's own 45-second per-call timeout at 0.0001 degrees - already 4 orders of magnitude short
  of the H-02 scale (`2.78e-8` degrees). Its direct longitude evaluation (`solar_longitude`, no search)
  carries a `20.57` arcsec systematic bias against this engine's certified ephemeris -
  `~206,000x` the defect's own scale. **Conclusion: PyJHora cannot provide reliable Option B evidence at
  the precision H-02 requires, by either method - recorded as an evidenced limitation, per the owner's
  own explicit fallback instruction, not manufactured agreement.**
  CI wiring: new step "H-02 independent-reference reproduction" in the `hermetic` job (both 3.11/3.12
  legs), new step "H-02 PyJHora reliability investigation" in the `oracle` job - both non-gating
  (investigation evidence, not certification), with their own `upload-artifact` steps. Neither script was
  added to `certification_support.py`'s `CERTIFIER_SOURCES`/`VALIDATOR_SOURCES` (this is investigation
  tooling, not a certified capability) - confirmed the M-03 anti-fitting scan surface is unchanged (180).
- Tests executed and results: `python -m pytest -q` - **809 passed** (up from 801; 8 new tests).
- Certification executed and results: none applicable - no capability is being certified. Part A ran in
  the main environment (no PyJHora needed). Part B ran in an isolated, throwaway, unpinned exploration
  venv (PyJHora 4.8.7) - the same discipline `ADR-0059`/`ADR-0061` established.
- Known issues: none. The Moon holdout window is independently selected (DP-013 s5 flagged this as an
  open methodology detail the ratification did not further specify), so its count does not numerically
  match the original audit, by design, not error.
- Unresolved questions: which of the three original fix options to adopt - explicitly not decided here,
  per the owner's own instruction.
- CEO decision required: no, for this entry itself (implements the owner's own instruction). A future
  decision is needed to choose a fix option, if any.
- Next authorized action: none self-authorized. **Post-push update:** commit `f3399f3` was pushed and CI
  run `32375941348` completed with all four jobs green. Both new steps confirmed genuinely executed from
  the CI log directly (not merely "job succeeded"): the hermetic-job "H-02 independent-reference
  reproduction" step printed the identical Sun 12/2, Moon 34/15 result; the oracle-job "H-02 PyJHora
  reliability investigation" step printed the identical precision-convergence table (0.1/0.01/0.001
  converge to `jd=2460414.14308969`; 0.0001 TIMEOUT at 45.05s) and longitude bias (20.57 arcsec,
  205,697x) - now under the hash-pinned environment, matching the local exploration-venv findings
  exactly. H-02's reproduction methodology is complete and CI-confirmed. The next action is an owner
  decision: choose one of the three original fix options (or defer H-02), not self-executable.

### 2026-08-20 - DP-013 decision-readiness audit: reproduction options, evidence, trade-offs, recommendation
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the audit).
- Previous approved commit: `ae9a08ed2604033e3faf207e087e768f8e052fe9`.
- Task: owner "Claude: read the current DP-013 from the repository and perform the decision-readiness
  audit... Put the exact reproduction options, their evidence, trade-offs, and Claude's recommendation
  into the repository handoff so the CEO can make an informed ratification decision." No option chosen;
  H-02 not implemented.
- Relevant ADR/specification: `DP-013` (v1.0.0 -> v1.1.0).
- Files changed: `docs/decisions/DP-013-h02-ingress-classification-seam.md` (strengthened), this file.
  No engine code, no `ADR-0020` edit, no fix applied.

**For the CEO's ratification decision - the exact reproduction options, evidence, and trade-offs, in one
place (full detail in `DP-013` itself):**

- **Re-verified, not assumed:** `engine/astrology/longitude_utils.py`'s `BOUNDARY_TOLERANCE` is still
  exactly `1e-10` and `engine/transits/crossing.py`'s `RESIDUAL_BOUND_ARCSEC` is still exactly `1e-4`
  arcsec - the original audit's 278x mismatch still holds precisely, unchanged since 2026-08-11. The
  defect has not been silently fixed.
- **Option A - independent-reference validator** (mirrors this session's own `validate_panchanga_
  holdout.py`/`validate_trikalam_holdout.py` pattern): classify sign/nakshatra directly from an
  independently-computed longitude at the exact reported event instant, compared against the engine's
  own classification, across a holdout of real ingress instants. *Evidence:* directly reuses proven,
  already-trusted infrastructure. *Trade-off:* re-derives the same tolerance-mismatch mechanism
  analytically rather than sourcing a second, independently-implemented system.
- **Option B - PyJHora oracle cross-check** (mirrors the `ADR-0059`/`ADR-0061` external-oracle
  mechanism): compare against PyJHora's own ingress detection. *Evidence, newly verified this audit*
  (PyJHora 4.8.7's source directly inspected, not assumed): a reachable API genuinely exists -
  `next_sankranti_date_from_jd`/`previous_sankranti_date_from_jd` (Sun) and
  `next_planet_entry_date_general` (general/nakshatra via its `nakshathra` parameter) - so Option B is a
  real path, not a guess. *Trade-off, newly surfaced this audit:* every one of these functions defaults
  to `precision=0.1` degrees - about four orders of magnitude coarser than the `2.78e-8` degree defect
  being investigated. `precision` is caller-adjustable, but PyJHora's own search loop (a simple
  step-until-within-precision walk) has not been verified to converge reliably at the precision this
  comparison would need - real, boundable, but non-trivial effort, not a one-line parameter change.
- **Option C - both A and B** (Claude's recommendation, confidence medium-high, revised down slightly
  from the first draft now that B's cost is concretely known): A confirms the *mechanism*, B confirms the
  real-world *magnitude*, matching this repository's established Gate B/E-plus-Gate-F template. Claude
  would also accept **Option A alone** as a legitimate, lower-cost reading of "independently reproduced"
  if the owner judges mechanism-level confirmation sufficient without B's additional PyJHora
  precision-tuning effort.
- **Explicitly not decided by this audit or by `DP-013` itself:** which of the original audit's three fix
  options (explicit signed residual + declared division; bias the instant to the target division; widen
  the classifier tolerance) is adopted if reproduction confirms the defect - the audit itself reserved
  that choice for the owner.

- Tests executed and results: none applicable - documentation/decision-paper audit only.
- Certification executed and results: none applicable.
- Known issues: none.
- Unresolved questions: the reproduction-methodology option (A/B/C) and, separately, the fix option -
  both still awaiting ratification.
- CEO decision required: yes - a reproduction-methodology option, to unblock any H-02 investigation work.
  Not required for this entry itself, which decides nothing.
- Next authorized action: push (needs its own authorization). Awaiting the owner's ratification decision
  on `DP-013`, or a different next task.

### 2026-08-20 - DP-013 drafted: H-02 seam extracted from ADR-0020 D5, not ratified
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the draft).
- Previous approved commit: `e062b8e130178ef42e1fe9fba9540782e8c20dbe`.
- Task: owner "ACE CONTINUE - AUTHORIZE H-02 DECISION PAPER" - draft a narrow decision paper strictly
  scoped to `ADR-0020` D5's already-written H-02 analysis, without ratifying `ADR-0020` or resolving
  H-02.
- Relevant ADR/specification: `ADR-0020` D5 (source analysis, itself still `Status: PROPOSED` -
  extracted, not ratified); `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` finding H-02 (the original,
  primary evidence source, read directly rather than trusting `ADR-0020`'s own summary of it).
- Files changed: `docs/decisions/README.md` (`DP-013` registered before drafting, per `ADR-0040`),
  `docs/decisions/DP-013-h02-ingress-classification-seam.md` (new), `docs/ACE_EXECUTION_STATE.md`, this
  file. No engine code, no `ADR-0020` edit.
- Implementation summary: read the G1 audit's original H-02 finding directly (not just `ADR-0020`'s
  summary): the transit root-finder's `1e-4` arcsec residual bound is ~278x wider than the `1e-10`
  degree boundary-promotion window classification uses, so the returned bracket midpoint lands on either
  side of the true root effectively at random. Measured 2024, `parashari_lahiri`: 2/12 Sun sankranti
  instants and 12/28 Moon nakshatra ingress instants misclassified into the previous division. `DP-013`
  preserves this finding and the audit's own three named fix options verbatim in substance, adds three
  reproduction-methodology options (an independent-reference validator mirroring this session's own
  `validate_panchanga_holdout.py`/`validate_trikalam_holdout.py` pattern; a PyJHora oracle cross-check
  mirroring `ADR-0059`/`ADR-0061`'s established mechanism; both), and recommends "both" while explicitly
  declining to recommend among the three fix options - the original audit reserved that choice for the
  owner, and this paper's authorized scope is extraction, not new analysis. States explicitly, in its
  own s1, that `ADR-0020` remains unratified in its entirety and this paper's own future ratification
  (not `ADR-0020`'s) is what would bind anything.
- Tests executed and results: none applicable - documentation/decision-paper only.
- Certification executed and results: none applicable.
- Known issues: none.
- Unresolved questions: `DP-013`'s reproduction-methodology options and the preserved fix options, both
  awaiting ratification.
- CEO decision required: not for drafting itself (implements the owner's own scoped authorization). A
  future decision is needed to ratify a reproduction option before any H-02 investigation work begins.
- Next authorized action: push (needs its own authorization). Separately, awaiting the owner's decision
  on `DP-013`, or a different next task.

### 2026-08-20 - DP-012 Option C ratified: civil-date rendering deferred (ADR-0063); mismatch caught first
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with `ADR-0063`).
- Previous approved commit: `9424768ebfb2d8567c939743e44efa0547eb32fa`.
- Task: owner "ACE CONTINUE - DP-012 OPTION C RATIFIED" asked Claude to *implement* civil-date rendering
  "per DP-012 Option C." Direct re-verification of `DP-012`'s actual text (mandatory before coding, per
  that same task's own instruction) showed Option C is the paper's **defer** option, not an
  implementation path - the detailed implementation requirements in that instruction actually matched
  Option A's content. Claude stopped and asked which was intended, writing zero code. The owner's
  follow-up, "ACE CORRECTION - DP-012 IS DEFERRED," confirmed Option C (defer) was in fact what was
  ratified, and explicitly instructed correcting any wording that implied otherwise.
- Relevant ADR/specification: `ADR-0063` (new); `DP-012` (unedited - paper is not the decision).
- Files changed: `docs/DECISION_LOG.md` (new `ADR-0063`, register header updated, `ADR-0061`'s stale
  "civil-date rendering... lacks a ratified decision paper" line corrected), `docs/decisions/README.md`
  (`DP-012` marked ADDRESSED), `docs/ACE_EXECUTION_STATE.md` (every field that previously implied
  implementation was pending ratification corrected to reflect deferral), this file. No engine code -
  none was ever written for this capability.
- Implementation summary: recorded the owner's Option C ratification as `ADR-0063`. Verified no
  civil-date-rendering code/tests/certification artifacts existed anywhere in the working tree (the
  mismatch was caught before the implementation instruction's steps 3-11 were ever executed). Per the
  correction's own item 6-7, re-audited the FOUNDATION roadmap: no capability has both satisfied
  prerequisites and a ratified implementation decision. Identified (did not draft, since only
  "identify" was asked) the most promising next decision-paper candidate: a narrow H-02
  investigation-methodology paper extracting `ADR-0020` D5's already-written analysis, so the owner
  need not ratify `ADR-0020`'s other nine unrelated items just to unblock H-02. H-01 has no governing
  document at all in this repository - not enough groundwork exists yet to identify a specific DP for
  it.
- Tests executed and results: none applicable - documentation/decision-recording only.
- Certification executed and results: none applicable.
- Known issues: none. This entry documents a self-caught process error (a task instruction's label and
  its content disagreed) rather than a repository defect.
- Unresolved questions: whether to authorize drafting the identified H-02 decision-paper candidate.
- CEO decision required: no, for this entry itself (implements the owner's own correction). Drafting the
  H-02 paper would need its own authorization, per "no silent scope expansion."
- Next authorized action: push (needs its own authorization). Separately, awaiting the owner naming the
  next task - most likely either authorizing the H-02 decision-paper draft, or something else entirely.

### 2026-08-20 - DP-012 decision-readiness audit: one sub-question resolved by research, not decided
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the audit).
- Previous approved commit: `a95948edeed8b3a514607a23ced0d7f807b268ce`.
- Task: owner "ACE CONTINUE - DP-012 DECISION READINESS" - audit whether any of `DP-012`'s open
  questions can be resolved by repository evidence/research alone, without ratifying an option, and
  check the rest of the FOUNDATION roadmap for other authorized work.
- Relevant ADR/specification: `DP-012` (v1.1.0 -> v1.2.0).
- Files changed: `docs/decisions/DP-012-civil-date-rendering-dasha-boundaries.md`, `docs/
  ACE_EXECUTION_STATE.md`, this file. No engine code, no ratification, nothing implemented.
- Implementation summary: `DP-012` v1.0.0's draft assumed dasha-boundary civil-date rendering would need
  the same fold/gap-ambiguity handling `BirthData`/`time_service.py` use for the birth instant. Tested
  this directly: swept `zoneinfo`/`America/New_York` minute-by-minute across the 2024-03-10
  spring-forward gap and 2024-11-03 fall-back fold, converting *from* well-defined UTC instants *to*
  local time (the actual direction dasha-boundary rendering needs - the reverse of `BirthData`'s own
  local-to-UTC problem). Result: `datetime.astimezone()` on an already-unambiguous UTC instant is fully
  deterministic in every case - the gap is simply never an output, and the fold is resolved automatically
  and correctly without any caller-supplied disambiguation. This was a real, mistaken analogy in the
  original draft, now corrected: not a policy choice at all, so removed from `DP-012` s5's sub-decision
  list, and Option A's cost lowered / confidence raised accordingly. The LMT-vs-standardized-zone
  labelling question (added last task) remains genuinely open - confirmed still real, not resolvable by
  research alone (it's a reporting-policy choice about whether/how to surface a distinction that is real
  either way). Checked the rest of FOUNDATION's scope (civil-date rendering, H-01, H-02, boundary-
  proximity) against the 2026-08-19 audit's own findings - nothing has changed; no other capability has
  a ratified path to implementation.
- Tests executed and results: none applicable to the DP-012 edit itself (no engine code touched); the
  `zoneinfo` behaviour was verified by direct interactive testing, reproducible from the commands quoted
  in `DP-012` s2 item 1.
- Certification executed and results: none applicable.
- Known issues: none.
- Unresolved questions: `DP-012` now presents two genuine sub-decisions (LMT labelling; rendering
  granularity) instead of three - still awaiting ratification or explicit deferral.
- CEO decision required: no - this entry decides nothing, per the task's explicit instruction.
- Next authorized action: push (needs its own authorization). `DP-012` ratification remains standing and
  non-blocking.

### 2026-08-20 - DP-012 independently advanced via empirical tzdata research (no decision, no implementation)
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the changes).
- Previous approved commit: `3650fa9c27e6952c302e07b8406c5043d12390ea`.
- Task: owner "ACE CONTINUE - RECORD CEO ACCEPTANCE" - verified commit `42d61c3` and the checkpoint
  record, confirmed both already correct (no unnecessary changes made to them), then independently
  advanced `DP-012` per the instruction to determine what could move forward without ratifying or
  implementing anything.
- Relevant ADR/specification: `DP-012` (v1.0.0 -> v1.1.0); `ADR-0054` (the "declared conventions, never
  silent" discipline this research applies to civil-date rendering).
- Files changed: `docs/decisions/DP-012-civil-date-rendering-dasha-boundaries.md` (strengthened),
  `docs/ACE_EXECUTION_STATE.md`, this file. No engine code, no new ADR, no ratification.
- Implementation summary: verification (items 1-3 of the task) found the committed state already correct
  - `42d61c3` was already pushed and CI-green, the `ADR-0061` checkpoint addendum correctly records the
  owner's exact acceptance instruction, and both state files already identified `DP-012` as the next
  decision item - so nothing was changed there, per the task's own "if the committed state is correct,
  do not create unnecessary changes." For the "advance what can be advanced around DP-012" instruction,
  ran a real `zoneinfo`/`tzdata` probe (not assumed) against `RISE_SET_V1`'s own H1/H4 holdout dates:
  confirmed `Europe/London` on 1823-04-17 resolves to a genuine Local Mean Time offset (`-00:01:15`,
  solar time at that longitude, since standardized zones did not yet exist there), while `Asia/Kolkata`
  on 1979-11-11 resolves to the expected standardized `+05:30`. Folded this into `DP-012`'s options
  analysis and its s5 "what the decision must also settle" list: whichever option is ratified should
  carry an explicit marker distinguishing an LMT-era answer from a standardized-zone one, rather than
  silently blending two different kinds of `zoneinfo` answer into one rendered civil date.
- Tests executed and results: `python -m pytest -q` - 801 passed (unchanged; no code touched).
- Certification executed and results: none applicable.
- Known issues: none.
- Unresolved questions: `DP-012`'s options, unchanged in kind, now better-grounded - still awaiting
  ratification or explicit deferral.
- CEO decision required: no, for this entry - research/documentation only, decides nothing.
- Next authorized action: push (this commit plus the prior `3650fa9`, both currently local-only) needs
  its own authorization. Separately, `DP-012` ratification remains standing and non-blocking.

### 2026-08-20 - TRIKALAM_V1 FOUNDATION checkpoint accepted; DP-012 drafted for the next milestone
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the changes below).
- Previous approved commit: `1423a4bb2aa824115fa1bb7e826d9ac6a96739b6`.
- Task: owner "ACE CONTINUE - CEO CHECKPOINT ACCEPTED" - record the FOUNDATION checkpoint acceptance,
  then determine and act on the next authorized FOUNDATION step.
- Relevant ADR/specification: `ADR-0061` (third evidence addendum); `Q8_CLOSURE_MATRIX.md` s4
  (FOUNDATION implementation scope: civil-date rendering, H-01, H-02 remain); `docs/decisions/README.md`
  (`DP-012` registered).
- Files changed: `docs/DECISION_LOG.md` (new `ADR-0061` addendum, register header updated),
  `docs/decisions/README.md` (`DP-012` registered), `docs/decisions/DP-012-civil-date-rendering-dasha-
  boundaries.md` (new), `docs/ACE_EXECUTION_STATE.md`, this file. No engine code touched.
- Implementation summary: recorded the owner's checkpoint acceptance as `ADR-0061`'s third addendum
  (`TRIKALAM_V1` now FOUNDATION checkpoint-accepted / production-certified, scope explicitly bounded -
  does not authorize a second variant, Muhurta consumption, or close FOUNDATION's own phase-exit
  criteria). Determined the next FOUNDATION item by re-checking prerequisites for every remaining scope
  item (civil-date rendering, H-01, H-02, boundary-proximity): H-02's own investigation methodology
  (`ADR-0020` D5) is itself unratified, H-01 has no governing document at all, boundary-proximity is
  undefined scope - none of these can proceed without a prior, larger ratification this task does not
  authorize. Civil-date rendering is the one item with real existing infrastructure to reason about
  (`engine/services/time_service.py`'s already-audit-remediated `zoneinfo`/`tzdata` mechanism) and a
  genuinely open, DP-worthy methodology question (DST fold/gap handling at a *derived* instant decades
  after birth, not the validated birth instant `time_service.py` already handles; pre-1900 `tzdata`
  coverage, directly relevant given `RISE_SET_V1`'s own 1823-2350 holdout). Drafted `DP-012` presenting
  three options (extend `time_service.py`'s mechanism locally; render in UTC only; defer to a consuming
  feature), recommending Option A with sub-decisions on fold/gap/coverage. Did **not** implement
  anything - `DP-012` decides nothing and is not yet ratified.
- Tests executed and results: none applicable - documentation/decision-paper only.
- Certification executed and results: none applicable.
- Known issues: none.
- Unresolved questions: `DP-012`'s own options, awaiting ratification (or explicit deferral, per its own
  Option C - not blocking).
- CEO decision required: no, for this entry itself (implements the owner's own instruction). `DP-012`
  ratification is a separate, not-yet-requested decision.
- Next authorized action: push (needs its own authorization). Separately, on `DP-012` ratification,
  implement civil-date rendering per whichever option is chosen, following the established certification
  template.

### 2026-08-20 - ULP-battery remediation pushed and CI-confirmed green; FOUNDATION checkpoint re-presented
- Branch / commit SHA: `phase-g-governance`, `8e6bb40567512dd8680c1c567be73310fc235aa2` - pushed,
  confirmed identical to `origin/phase-g-governance`.
- Previous approved commit: `bf0d4140e239fa52200011698b2b132aa1460145`.
- Task: owner "authorised" - pushed the ULP-battery remediation commit, monitored the resulting CI run.
- Relevant ADR/specification: `ADR-0061` (register header updated with CI confirmation).
- Files changed: `docs/DECISION_LOG.md` (register header), `docs/ACE_EXECUTION_STATE.md` (refreshed to
  the CI-confirmed state), this file. No code.
- Implementation summary: `git push` succeeded (`bf0d414..8e6bb40`). CI run `32361308330` completed with
  **all four jobs green**. Did not stop at "conclusion: success" alone - pulled the oracle job's own log
  and confirmed the line `C_boundary_ulp_and_circumpolar: {... 'ulp_boundary_checked': True,
  'ulp_negative_control_verified': True ...}` was actually printed, i.e. the remediated gate genuinely
  executed under the hash-pinned oracle environment, not merely that the job exited 0.
- Tests executed and results: none re-run (no code changed; CI's own run is the evidence).
- Certification executed and results: `TRIKALAM_V1` - PASS, all six gates, CI-confirmed, remediated
  Gate C verified executed from the log directly.
- Known issues: none. The CEO-audit HOLD finding on the missing ULP battery is closed.
- Unresolved questions / CEO decision required: **YES - the same standing question, now on cleaner
  evidence.** Does `TRIKALAM_V1` meet `Q8_CLOSURE_MATRIX.md` s4's per-capability FOUNDATION checkpoint,
  with the ULP-battery gap closed and CI-confirmed? Not self-certified here.
- CEO decision required: **the FOUNDATION per-capability checkpoint acceptance for `TRIKALAM_V1`.**
- Next authorized action: on acceptance, a narrow `ADR-0061`-addendum entry recording it, then a fresh
  audit of remaining FOUNDATION scope (civil-date rendering, H-01, H-02 all still lack a ratified
  decision paper). If the owner names a different next task, that task governs.

### 2026-08-20 - CEO-audit HOLD remediated: genuine ULP battery added to TRIKALAM_V1 Gate C
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the remediation).
- Previous approved commit: `5e34d3b14c46356232b0420330d7072a97ad4249`.
- Task: owner "ACE CONTINUE - DO NOT RELAY REPORT" - a CEO audit placed `TRIKALAM_V1` on HOLD because
  its certification contract requires an explicit ULP battery and the repository evidence did not show
  one.
- Relevant ADR/specification: `ADR-0061` (second evidence addendum); `Q8_CLOSURE_MATRIX.md` s4
  ("frozen rule, second transcription, dense sweep, ULP battery, external oracle, independent
  validator").
- Files changed: `scripts/certify_trikalam.py` (Gate C renamed and extended with a genuine ULP battery
  + negative control), `engine/tests/test_trikalam.py` (2 new tests), `certification/
  TRIKALAM_V1_certification.json` + `reports/certification/trikalam.*` (regenerated), `docs/
  DECISION_LOG.md` (new `ADR-0061` addendum, register header updated), `docs/ACE_EXECUTION_STATE.md`,
  this file.
- Implementation summary: **verified the audit finding independently before acting** (direct source
  re-inspection of the committed `gate_c_boundary_and_circumpolar` confirmed it was pinning + a fixed
  `abs(diff) > 1e-8` tolerance check, with no floating-point-scale perturbation test and no negative
  control - the finding was correct, not assumed). Remediated by testing the one genuine discontinuity
  this variant has - the exact sunrise instant where `panchanga.vara`'s weekday rolls over - perturbed by
  `1e-9` days (~86 microseconds, above the double-precision floor at this JD magnitude, far below the
  >=0.125-day-length jump under test) on both sides, asserting the flip happens exactly there, with a
  negative control that temporarily freezes the weekday selection and confirms the same check would then
  fail to detect a rollover.
- Tests executed and results: `python -m pytest engine/tests/test_trikalam.py -q` - 23 passed (up from
  21). `python -m pytest -q` - **801 passed** (up from 799).
- Certification executed and results: `python scripts/certify_trikalam.py` (main environment, no
  PyJHora) - correctly `exit(3)`. `python scripts/certify_trikalam.py` (rebuilt isolated exploration
  venv, PyJHora 4.8.7) - **PASS, all six gates**; Gate C now reports `ulp_boundary_checked: True`,
  `ulp_negative_control_verified: True`. `python validate_trikalam_holdout.py` - PASS, 24 cases, 72
  comparisons, 0 mismatches. `scripts/check_adr_numbering.py`/`check_retired_identifiers.py`/
  `check_identifier_families.py` - all PASS.
- Known issues: none. M-03 scan surface unaffected (180, unchanged - no new files, only existing files
  edited).
- Unresolved questions: none technical.
- CEO decision required: **the push itself**, per git-safety's per-action confirmation rule, to trigger
  CI re-confirmation of the remediated gate. The separate FOUNDATION per-capability checkpoint question
  for `TRIKALAM_V1` remains open and should follow this CI re-confirmation, not precede it.
- Next authorized action: on push authorization, push, monitor the resulting CI run for all four jobs
  green (including the remediated Gate C under the hash-pinned oracle environment), report the run ID
  and PASS/FAIL per job, and refresh both state files to the confirmed-green state.

### 2026-08-20 - TRIKALAM_V1 fully CI-confirmed (all four jobs green); FOUNDATION checkpoint decision presented
- Branch / commit SHA: `phase-g-governance`, `bf0d4140e239fa52200011698b2b132aa1460145` - confirmed
  identical to `origin/phase-g-governance` (`git fetch` + `git rev-parse` both sides). Nothing unpushed.
- Previous approved commit: `9e33490d7e1186a114773231ff84807e835ededd`.
- Task: owner "Continue ACE execution from the current repository state... perform the next authorized
  action identified by the current state." Session-start audit found `origin/phase-g-governance` already
  equal to local HEAD (`bf0d414`) - the push from the prior turn's request had already occurred outside
  this conversation turn - so the next action was to verify CI, not to request push authorization again.
- Relevant ADR/specification: `ADR-0061` (evidence addendum added, CI confirmation); `Q8_CLOSURE_MATRIX.md`
  s4 (the per-capability checkpoint now presented as the open decision).
- Files changed: `docs/DECISION_LOG.md` (new `### Evidence addendum to ADR-0061`, register header
  updated), `docs/ACE_EXECUTION_STATE.md` (refreshed to the fully-green state), this file. No code.
- Implementation summary: `gh run view 32358109807` confirmed all four jobs (governance, no-oracle 3.11,
  no-oracle 3.12, oracle) green - `certify_trikalam.py` genuinely executed `F_external_oracle` under
  the hash-pinned oracle environment and the drift-assertion step also passed (the `9e33490` overlay was
  correct). `TRIKALAM_V1` is now evidenced to the same CI-confirmed standard as every other certified
  claim in this repository. The addendum records this and explicitly does NOT self-certify the
  FOUNDATION per-capability checkpoint question - that is presented as the next owner decision, mirroring
  `ADR-0059`'s own Panchanga-checkpoint precedent exactly (Claude presents evidence; the owner ratifies).
- Tests executed and results: none re-run (no code changed since `9e33490`'s own full-suite pass, 799
  passed); this task's own verification was `gh run view` log/job inspection, not a fresh local run.
- Certification executed and results: none re-run; `TRIKALAM_V1`'s CI result (PASS, all six gates) stands
  as directly observed in run `32358109807`.
- Known issues: none.
- Unresolved questions / CEO decision required: **YES - exactly one, the same question `ADR-0059`
  resolved for Panchanga.** Does `TRIKALAM_V1` (Rahu Kalam/Yamaganda/Gulika, `PYJHORA_TRIKALAM_V1`
  variant) meet `Q8_CLOSURE_MATRIX.md` s4's per-capability FOUNDATION checkpoint, now that implementation
  is complete and CI-confirmed? Not self-certified here.
- CEO decision required: **the FOUNDATION per-capability checkpoint acceptance for `TRIKALAM_V1`.**
- Next authorized action: on acceptance, the next Claude action is a narrow `ADR-0061`-addendum-style
  entry recording it (no new ADR number), then a fresh audit of what FOUNDATION scope remains (Rahu
  Kalam/Yamaganda/Gulika's own remaining items, if any, or the next capability entirely - civil-date
  rendering, H-01, H-02 all still lack any ratified decision paper). If the owner instead names a
  different next task, that task is what governs.

### 2026-08-20 - Push executed; TRIKALAM_V1 Gate F CI-confirmed PASS; expected M-03 drift recovered
- Branch / commit SHA: `phase-g-governance`, `9e33490d7e1186a114773231ff84807e835ededd` - **not yet
  pushed**, per git-safety's per-action push-confirmation rule (the owner's "push authorised" covered
  `3487add`, which is now pushed; this newer evidence-recovery commit needs its own authorization).
- Previous approved commit: `3487add6252f6cc4ebb535c512d390fedbf16494` (pushed, CI-run).
- Task: owner "push authorised" - pushed the 5 commits from the prior entry, then monitored the
  resulting CI run per the standing evidence-recovery discipline.
- Relevant ADR/specification: `ADR-0053`/`ADR-0054` (the evidence-recovery precedent reused verbatim);
  `ADR-0061` (`TRIKALAM_V1`, whose Gate F this run confirms).
- Files changed (commit `9e33490`): 13 `certification/*_certification.json` and their `reports/
  certification/*.console.txt`/`*.report.md` companions where they actually differed (27 files) -
  CI-sourced overlay only, no source code.
- Implementation summary: `git push origin phase-g-governance` succeeded (`ce2475f..3487add`). CI run
  `32353401132` completed with conclusion `failure`, but the failure was entirely the expected class:
  the "Oracle certification runners (all ten)" step itself **PASSED** - `certify_trikalam.py` genuinely
  executed under the hash-pinned oracle environment and its `F_external_oracle` gate passed for real -
  and the subsequent drift-assertion steps failed only because `TRIKALAM_V1`'s addition legitimately grew
  the M-03 anti-fitting scan surface 177 -> 180, aging every other already-committed artifact's
  `modules_scanned` field, exactly as happened twice before (`ADR-0053`, and this session's own Panchanga
  evidence-recovery). Downloaded `hermetic-certification-evidence-3.11`/`-3.12` and
  `oracle-certification-evidence`; cross-compared 3.11 vs 3.12 (identical outside `environment.python`/
  `run.python`); diffed all 13 affected artifacts against committed HEAD (confirmed `modules_scanned`
  177->180 is the ONLY non-volatile difference in every case, via a small verification script, not by
  assumption); overlaid the CI-sourced files.
- Tests executed and results: `python -m pytest -q` - 799 passed (unchanged; no code touched).
- Certification executed and results: `python scripts/check_artifact_drift.py` - **PASS, 46 evidence
  files identical to committed HEAD outside the volatile fields** (confirms the overlay is exactly
  correct, no other drift). `scripts/check_adr_numbering.py`/`check_retired_identifiers.py`/
  `check_identifier_families.py` - all PASS.
- Known issues: none. The CI failure was diagnosed, not assumed, before any fix was applied (log
  inspection first, per certification-discipline rules).
- Unresolved questions: none technical.
- CEO decision required: **the push itself**, per git-safety's per-action confirmation rule - this is a
  new commit made after the prior "push authorised" was already consumed by `3487add`.
- Next authorized action: on push authorization, push `9e33490`, wait for the resulting CI run, report
  run ID and PASS/FAIL per job, and refresh `docs/ACE_EXECUTION_STATE.md`/this file to the fully-green
  state if it passes.

### 2026-08-20 - Permanent ACE execution-state mechanism implemented (ADR-0062)
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with `ADR-0062`).
- Previous approved commit: `7276bf9d2425420b482170cb02c16c55c0bbccce`
- Task: owner "ACE - IMPLEMENT PERMANENT REPOSITORY-STATE ORCHESTRATION" - make ACE state recoverable
  from the repository alone, without ChatGPT conversational memory and without the user relaying
  Claude's reports to ChatGPT by hand.
- Relevant ADR/specification: `ADR-0062` (new); `docs/PROJECT_CONSTITUTION.md` s11 point 3 (`ADR-0056`,
  already ratified - operationalized, not reopened); `specs/CLAUDE_WORKFLOW.md` "ACE interaction mode"
  (`ADR-0057`, same principle for ChatGPT's own behaviour).
- Files changed: `docs/ACE_EXECUTION_STATE.md` (new - the canonical current-state snapshot),
  `specs/CLAUDE_WORKFLOW.md` (1.3.0 -> 1.4.0, new "Execution-state recovery" section), `docs/
  DECISION_LOG.md` (new `ADR-0062`, register header updated), this file. No code, no calculation,
  certification, Panchanga, or `DP-011`/`TRIKALAM_V1` change - governance/documentation only.
- Implementation summary: reconciled against existing governance first (per the task's own instruction)
  and found the *principle* already ratified (`ADR-0056` s11 point 3) - what was missing was a
  fixed-shape, always-current, machine-checkable snapshot document, not a new rule. `docs/
  ACE_EXECUTION_STATE.md` now carries exactly the fields the owner specified, populated with this
  session's actual, git-verified state (see its own "Current state" table): 4 unpushed local commits
  ahead of `origin/phase-g-governance`, `TRIKALAM_V1` implemented but not yet CI-confirmed, push
  authorization the sole outstanding item. `specs/CLAUDE_WORKFLOW.md` gained an explicit, permanent
  prohibition on relaying reports between Claude and ChatGPT through the user, sharpening (not
  duplicating) the constitution's own language.
- Tests executed and results: none applicable - documentation only. Verified via direct `git`/`gh`
  commands that every field in `docs/ACE_EXECUTION_STATE.md`'s "Current state" table is accurate as of
  this entry (branch, local vs. origin HEAD, unpushed commit list, last two CI runs).
- Certification executed and results: none applicable.
- Known issues: none.
- Unresolved questions: none raised by this entry.
- CEO decision required: no, for this entry itself - implements the owner's own instruction, matching
  the `ADR-0056`/`ADR-0057` precedent of committing a direct, self-contained governance instruction
  without a separate pause. **The standing, pre-existing item is unchanged by this entry: push
  authorization for the 4 unpushed commits** (see `docs/ACE_EXECUTION_STATE.md`).
- Next authorized action: none self-authorized beyond what this entry implements. The next action for
  ACE overall is the standing one - push authorization - not a new action this task created.

### 2026-08-20 - DP-011 ratified (ADR-0060): PyJHora trikalam convention transcribed and frozen
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with `ADR-0060`).
- Previous approved commit: `9bbe25420eab5322b2f5cd50c1a0e686611f1b69`
- Task: owner "CEO DECISION - DP-011. RATIFIED: OPTION C, SEEDED BY OPTION B" - record the decision as
  an ADR, then continue automatically into the variant-definition/certification work it authorizes.
- Relevant ADR/specification: `ADR-0060` (new); `DP-011` (unedited, options record); `ADR-0055` item 2;
  `ADR-0059` (PyJHora provenance/venv-isolation precedent this entry reuses).
- Files changed: `docs/DECISION_LOG.md` (new `ADR-0060`, register header updated), `docs/decisions/
  README.md` (`DP-011` marked ADDRESSED), this file. No engine code yet - implementation follows in the
  next entry.
- Implementation summary: PyJHora 4.8.7 installed into an isolated, throwaway venv
  (`dp011_explore_venv`, network access confirmed available, `pip install PyJHora` succeeded from a
  pre-existing pip cache); `jhora/panchanga/drik.py` read directly; the `trikalam()` function (lines
  ~1433-1464) transcribed verbatim into `ADR-0060` as `PYJHORA_TRIKALAM_V1` - the day-only, 1/8-day-part
  offset table for all three periods, plus two honestly-recorded representational differences (local-hour
  vs JD-UT; today's-calendar-day sunrise for the window vs. `vaara`'s rolled-back weekday for the offset
  lookup - PyJHora's actual mixed behaviour, not corrected).
- Tests executed and results: none yet - decision-recording step only.
- Certification executed and results: none - `ADR-0060` explicitly does not certify anything by itself.
- Known issues: none.
- Unresolved questions: none raised by this entry.
- CEO decision required: no - implements the owner's own instruction.
- Next authorized action: proceed to implement, test, and certify `PYJHORA_TRIKALAM_V1` per `ADR-0060`'s
  Consequences (new `engine.astrology.trikalam` module, tests, certifier, validator, CI wiring) - see the
  next task-log entry.

### 2026-08-20 - TRIKALAM_V1 implemented, all six gates locally verified (ADR-0061), CI pending
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with `ADR-0061`).
- Previous approved commit: `bad5b04936d9bd00ea8daf7e67d18a9bc6457d4b`
- Task: continuation of `ADR-0060`'s authorized variant-definition/certification work, per the owner's
  "continue execution automatically" instruction.
- Relevant ADR/specification: `ADR-0061` (new); `ADR-0060` (authorization); `ADR-0054`/`ADR-0059`
  (isolated-exploration-venv and oracle-provenance precedent this entry reuses exactly).
- Files changed: `engine/astrology/trikalam.py` (new), `engine/tests/test_trikalam.py` (new, 21 tests),
  `validate_trikalam_holdout.py` (new), `scripts/certify_trikalam.py` (new), `scripts/
  certification_support.py` (M-03 scan surface 14/13 -> 15/14), `engine/tests/
  test_certification_preconditions.py` (matching counts; `modules_scanned` floor 177 -> 180),
  `.github/workflows/ci.yml` (`certify_trikalam.py` to the `oracle` job, now ten; `validate_trikalam_
  holdout.py` to the `hermetic` job's validator list, now fourteen), `docs/DECISION_LOG.md` (new
  `ADR-0061`, register header updated), this file. No already-certified module touched.
- Implementation summary: `trikalam_period()` mirrors PyJHora's exact mixed behaviour (today's
  calendar-day sunrise/sunset via certified `rise_set`, `panchanga.vara`'s rolled-back weekday for the
  offset lookup) rather than a more "consistent" rule PyJHora itself does not implement. Gate F calls
  live PyJHora `sunrise`/`sunset`/`vaara` (not the string-formatting `trikalam()` wrapper) and found,
  empirically, a ~4-8.5 minute systematic gap between this engine's rise/set convention (`ADR-0054`) and
  PyJHora's own (`swe.BIT_HINDU_RISING`) across the H1-H11 holdout's latitudes - recorded as an explicit,
  reasoned 20-minute tolerance in the certifier's own docstring, not silently absorbed or ignored.
- Tests executed and results: `python -m pytest -q` - **799 passed** (up from 778; 21 new
  `test_trikalam.py` tests, 0 failures elsewhere). `python validate_trikalam_holdout.py` (main
  environment, no PyJHora needed) - PASS, 24 cases, 72 comparisons, 0 mismatches.
- Certification executed and results: `python scripts/certify_trikalam.py` (main environment, no
  PyJHora) - correctly `exit(3)`, matching every oracle-tier certifier's fail-closed behaviour, confirmed
  correct not defective. `python scripts/certify_trikalam.py` via an isolated, throwaway, **unpinned**
  exploration venv (PyJHora 4.8.7 plus its six documented undeclared dependencies) - **PASS, all six
  gates**: A (frozen table matches `ADR-0060`), B (66/66 comparisons, dense sweep), C (21 weekday/element
  combinations + 2 circumpolar cases), D (non-invasiveness), E (independent validator), F (66/66 oracle
  comparisons within the 20-minute tolerance, negative control verified). `certification/
  TRIKALAM_V1_certification.json` regenerated from this real run - genuine evidence, not backfilled.
  `scripts/check_adr_numbering.py` - PASS, 61 entries.
- Known issues: none. The empirical rise/set convention gap (this engine vs. PyJHora's
  `BIT_HINDU_RISING`) is a recorded, explained design fact, not treated as a defect.
- Unresolved questions / CEO decision required: **only the commit/push itself**, to trigger the CI run
  that would upgrade this evidence from "locally verified, unpinned exploration venv" to "CI-confirmed,
  hash-pinned oracle environment" - the same evidence class every other certified claim in this
  repository relies on. Per `.claude/rules/git-safety.md`, pushing needs explicit confirmation even
  though this task authorized continuing automatically through implementation.
- CEO decision required: **the commit/push itself**, per the above.
- Next authorized action: on explicit owner authorization to commit and push, stage exactly the nine
  files listed above on `phase-g-governance`, commit, push, then monitor the resulting `oracle` job run
  specifically for `certify_trikalam.py`'s new tenth position and `F_external_oracle`'s real result,
  reporting the run ID and PASS/FAIL per job - the same evidence-recovery discipline `ADR-0053`/
  `ADR-0054`/`ADR-0059` already established. Until authorized, no push is made.

### 2026-08-19 - Owner acceptance of Panchanga's FOUNDATION per-capability checkpoint (ADR-0059 addendum)
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits in the same commit as
  the addendum it describes).
- Previous approved commit: `cb9001f47252d12f62e890f6d0b1e1bb03754f95`
- Task: owner-directed "record this narrow checkpoint acceptance as an ADR-0059 addendum" - the owner's
  reply to the prior FOUNDATION checkpoint audit's stop-and-ask.
- Relevant ADR/specification: `ADR-0059` addendum (new, no new ADR number); `Q8_CLOSURE_MATRIX.md` s4.
- Files changed: `docs/DECISION_LOG.md` (new `### Evidence addendum to ADR-0059`, register header
  updated, version 2.9.0 -> 3.0.0), this file. No source/calculation/certification code touched.
- Implementation summary: the addendum records the owner's instruction as the act of ratification
  (matching the `ADR-0052`/`ADR-0055` precedent of treating a direct owner reply as the ratifying
  record), and states explicitly what it does and does not close: Panchanga's own per-capability
  checkpoint is accepted; FOUNDATION's phase-exit criteria are NOT thereby met (Rahu Kalam/Yamaganda/
  Gulika, H-01, H-02 remain outstanding).
- Tests executed and results: none re-run - documentation-only, no code touched.
- Certification executed and results: none applicable.
- Known issues: none.
- Unresolved questions: none raised by this entry.
- CEO decision required: no - this entry implements the owner's own instruction.
- Next authorized action: proceed to determine FOUNDATION's next decision-paper work item (see the
  following entry).

### 2026-08-19 - DP-011 drafted: Rahu Kalam/Yamaganda/Gulika variant-table source
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (committed with the ADR-0059 addendum
  above).
- Previous approved commit: see prior entry.
- Task: per the owner's "continue automatically to determine the next decision-paper work item for
  FOUNDATION... If drafting that decision paper is already authorized by the repository, proceed with
  it" instruction.
- Finding: of the FOUNDATION scope items not yet authorized (Rahu Kalam/Yamaganda/Gulika, civil-date
  rendering, H-01, H-02, boundary-proximity - see the FOUNDATION checkpoint audit entry above), exactly
  one already has explicit repository authorization to draft its decision paper: `ADR-0055` item 2 -
  "this entry authorizes drafting a short `DP-NNN` options paper naming candidate source tables for
  [Rahu Kalam/Yamaganda/Gulika], for separate, later owner ratification." No other remaining FOUNDATION
  item has any such drafting authorization - civil-date rendering, H-01, and H-02 have no governing
  ADR/DP at all, and H-02's own investigation methodology (`ADR-0020` D5) is itself still PROPOSED, not
  ratified, so drafting a paper for any of those would require a fresh decision to even begin.
- Files changed: `docs/decisions/README.md` (DP-011 registered before drafting, per `ADR-0040`; version
  1.5.0 -> 1.6.0), `docs/decisions/DP-011-rahu-kalam-yamaganda-gulika-variant-tables.md` (new).
- Implementation summary: `DP-011` presents four options (single common table; adopt PyJHora's own
  convention; multiple named profile-selectable variants; defer to nearer Muhurta entry) and recommends
  Option C (named, profile-selectable variants) seeded by Option B's PyJHora convention as the first
  variant to verify, confidence medium. It explicitly does **not** assert any specific weekday-to-part
  table as fact - this session has not inspected PyJHora's `rahu_kaalam`/`yamaganda_kaalam`/
  `gulikai_kaalam` source (PyJHora is not installed on this Windows host), and general astrological
  convention is not, on its own, a citable independent reference by this repository's own validation
  rules. Implementation of any of the three remains **NOT authorized** - this paper decides nothing.
- Tests executed and results: none applicable - documentation only.
- Certification executed and results: none applicable.
- Known issues: none.
- Unresolved questions: the four options themselves - awaiting owner ratification of one.
- CEO decision required: **YES** - which option (or a different one) to ratify for Rahu Kalam/
  Yamaganda/Gulika before any implementation may begin. This is a genuine new-owner-decision boundary,
  not something Claude may infer or select.
- Next authorized action: none beyond drafting. Awaiting the owner's decision on `DP-011`, or a new
  authorized task naming a different next step.

### 2026-08-19 - FOUNDATION checkpoint audit (read-only; no code, no new ADR)
- Branch / commit SHA: `phase-g-governance`, `ce2475f0fbfba348783b829b5d0a2b24fa45ef12` - this entry is
  the only edit; no source, calculation, certification, or evidence file touched.
- Previous approved commit: `ce2475f0fbfba348783b829b5d0a2b24fa45ef12`
- Task: owner-directed "ACE - FOUNDATION CHECKPOINT AUDIT" - independently verify the repository's
  current FOUNDATION state against `docs/Q8_CLOSURE_MATRIX.md` s4 (not trusting the prior entry's own
  claims), enumerate remaining FOUNDATION scope, and identify exactly one next authorized step.
- Relevant ADR/specification: `docs/Q8_CLOSURE_MATRIX.md` s4 (authoritative FOUNDATION scope and
  per-capability CEO-approval requirement); `ADR-0054` (rise/set); `ADR-0055` (Panchanga scope);
  `ADR-0059` (Panchanga Gate F); `ADR-0020` (PROPOSED, not ratified - H-02 D5 reproduction requirement
  lives here); `docs/decisions/README.md` (DP index, last updated 2026-08-17, no Rahu Kalam/Yamaganda/
  Gulika DP allocated yet).
- Implementation summary (findings, not code changes): verified independently, not assumed from the
  prior entry:
  1. **HEAD, CI, and the DECISION_LOG register all corroborate the prior entry's claims** - `ce2475f`
     and its two predecessor commits are all CI green (`gh run list`), `ADR-0058`/`ADR-0059` are
     committed (`grep` against the file, not the register summary), and `certify_panchanga.py` at `HEAD`
     genuinely requires PyJHora unconditionally (confirmed by reading the committed source directly).
  2. **FOUNDATION implementation scope, per `Q8_CLOSURE_MATRIX.md` s4** (verbatim): rise/set with
     declared conventions (**CERTIFIED**, `RISE_SET_V1`/`ADR-0054`); Panchanga tithi/vara/nakshatra/
     yoga/karana (**implemented and CI-certified, all six gates including a genuine external oracle**,
     `ADR-0059` - but the phase's own row states "CEO approval: Entry, per-capability checkpoint, exit"
     and no per-capability checkpoint acceptance has been recorded for Panchanga); Rahu Kalam/Yamaganda/
     Gulika (**NOT STARTED, NOT AUTHORIZED** - `ADR-0055` item 2 explicitly defers this pending a DP-NNN
     variant-table paper, and no such paper has been drafted or registered per `docs/decisions/README.md`);
     civil-date rendering for dasha boundaries (**NOT STARTED** - no governing ADR or DP found anywhere
     in `docs/DECISION_LOG.md`); H-01 true-node completeness (**NOT STARTED** - no governing ADR/DP
     found); H-02 ingress classification seam (**NOT STARTED** - flagged high-priority for Muhurta, but
     its own reproduction methodology, `ADR-0020` D5, is itself **Status: PROPOSED**, not owner-ratified,
     so even H-02's *investigation* is not yet authorized); boundary-proximity indicators (**NOT
     STARTED**, no decision).
  3. **Conclusion: no new FOUNDATION *implementation* milestone currently has all prerequisites
     satisfied.** Every remaining capability except Panchanga is blocked on a decision paper and/or
     owner ratification that does not yet exist - starting any of them now would be inventing scope
     `Q8_CLOSURE_MATRIX.md` requires a decision to open. Panchanga alone is implementation-complete and
     evidence-complete; its only remaining gap is the CEO checkpoint acceptance `Q8_CLOSURE_MATRIX.md`
     s4 itself requires per capability - a decision, not further engineering, and not one this entry
     (or any Claude-authored entry) can self-certify.
- Tests executed and results: none re-run - read-only audit, no code touched.
- Certification executed and results: none re-run; no certification claim disputed or changed.
- Known issues: none newly found.
- Unresolved questions / CEO decision required: **YES.** Whether to formally accept Panchanga
  classification (tithi, nakshatra-reuse, yoga, karana, vara at a given instant) as meeting its
  `Q8_CLOSURE_MATRIX.md` s4 per-capability FOUNDATION checkpoint, now that `ADR-0059`'s genuine,
  CI-confirmed external-oracle gate closes the one gap the prior checkpoint identified. This is the
  same open item the immediately preceding task-log entry already flagged; this entry independently
  re-confirms it rather than taking it on faith.
- CEO decision required: **the Panchanga per-capability FOUNDATION checkpoint acceptance**, per
  `Q8_CLOSURE_MATRIX.md` s4's own "CEO approval: Entry, per-capability checkpoint, exit" row.
- Next authorized action: on CEO/owner acceptance of the Panchanga checkpoint, the next Claude action is
  a narrow `ADR-0059`-addendum-style decision-log entry recording that acceptance (not a new ADR number,
  matching the addendum convention already used for `ADR-0047`/`ADR-0058`). No FOUNDATION capability
  beyond Panchanga and rise/set is authorized to begin implementation by this entry - each remaining one
  (Rahu Kalam/Yamaganda/Gulika, civil-date rendering, H-01, H-02, boundary-proximity) needs its own
  decision paper and/or ratification first, per `Q8_CLOSURE_MATRIX.md` s4's per-capability CEO-approval
  requirement.

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
| 7.2.0 | 2026-08-22 | **`ADR-0070` ratifies `DP-017` Option 1 - H-06 CLOSED.** Implemented `CERTIFIED_DASHA_PROFILES` (keyed on the full frozen `DashaProfile` instance, not name alone) and `UnsupportedDashaProfileError`/`validate_dasha_profile()` in `engine/dasha/profile.py`; wired into `vimshottari_from_moon()` (covers all four entry points) in `engine/dasha/vimshottari.py`. Both `DP-017` sub-questions resolved with recorded reasoning (type check as a separate function, matching `validate_birth_data()`'s precedent; allow-list keyed on full-instance equality, applying the B-01 lesson). 7 new tests; negative control verified at the strongest level (production guard actually removed in-session, confirmed genuine test failure, restored, confirmed byte-identical). Zero certified-value impact independently verified (`certify_vimshottari.py` in the isolated PyJHora venv - PASS, 0 lord mismatches; regenerated evidence discarded). 825/825 pytest (up from 818). Governance gates clean (70 ADR entries). H-08/M-02/dasha-boundary-proximity/JATAKA not started; FOUNDATION not reopened. Nothing pushed. |
| 7.1.0 | 2026-08-22 | Owner authorized "H-06 decision-readiness," per the Dasha roadmap's own step order. Performed the mandated pre-work (state audit; re-read `ADR-0068`/`ADR-0069`, `Q8_CLOSURE_MATRIX.md` s5, the complete roadmap; direct inspection of `engine/dasha/profile.py`, all four `vimshottari.py` entry points, existing tests, `explicit_non_claims`, and the varga-registry precedent). Drafted `DP-017`: independently reproduced both H-06 claims live; confirmed `DashaProfile(...)` is constructed exactly once in the tracked tree - the gap is entirely latent, unlike H-05's own reachable scenario. Classifies H-06 as a certification/governance-scope gap plus a type-safety gap, not a defect. Presents Option 1 (build, mirroring the certified varga-registry pattern) and Option 2 (defer), medium-confidence lean toward Option 1. No option chosen; no code touched; H-08/M-02/dasha-boundary-proximity/JATAKA not started. Governance gates and 818/818 pytest re-run clean (17 DP identifiers, up from 16). Nothing pushed or merged. |
| 7.0.0 | 2026-08-22 | **`phase-g-governance` MERGED into `main`** (PR #3), on explicit authorization scoped to commit `76ed443`. Created the PR (automatically excluding unpushed `bf66e48`), watched its own CI green, merged via a standard two-parent merge commit (`0e1ef11`) matching PR #1's own precedent. Verified directly: merge parents exactly `a3692e7` + `76ed443`; `bf66e48` confirmed not an ancestor of the new `main`; `origin/main` re-confirmed via `git ls-remote`; CI on `main` itself (run `32567048173`) green with `818 passed` on both interpreters and zero drift, read from the log; `ADR-0068`/`ADR-0069` both `Status: ACCEPTED` in `main`'s own new content. `main` now recoverable as the current approved ACE baseline. H-06 not started. |
| 6.3.0 | 2026-08-22 | Pushed `76ed443` (H-05, `ADR-0069`) to `origin/phase-g-governance` on explicit push authorization - fast-forward, `e7adeb0..76ed443`, carrying ten commits accumulated since the last push. CI run `32565790781`: all four jobs green, confirmed via `gh run view --json` and by reading the log directly - `818 passed` on both interpreter legs (matching local exactly) and `PASS: 46 evidence file(s) identical...` on all three relevant jobs (genuinely zero drift). Remote SHA confirmed identical to local HEAD, both directions; working tree clean. H-06 not started; `main` not merged, per explicit instruction. |
| 6.2.0 | 2026-08-22 | **`ADR-0069` ratifies `DP-016` Option 1 - H-05 CLOSED.** `engine/tests/test_vimshottari_hermetic_baseline.py` (new) freezes the Vimshottari anchor construction for five seed cases plus a negative control, verified at the strongest available level (real production line actually mutated in-session, new test confirmed to fail with the exact predicted value, then reverted, confirmed byte-identical). Zero certification impact verified directly (`certify_kp_chain.py` sanity check, M-03 scan surface confirmed unaffected). `certify_vimshottari.py`/`VIMSHOTTARI_V1_certification.json` untouched. 818/818 pytest. H-06/H-08/M-02/dasha boundary-proximity not touched; JATAKA not implemented. 69 ADR entries. Nothing pushed. |
| 6.1.0 | 2026-08-22 | Owner authorized "H-05 decision-readiness only." Performed the mandated pre-work (state audit; fresh re-read of `ADR-0068`, `Q8_CLOSURE_MATRIX.md` s5, the complete `DASHA_CERTIFICATION_ROADMAP.md`; direct inspection of all existing H-05 code/tests/validator/certifier/CI wiring/certification-artifact schema). Drafted `DP-016`: independently re-verified every claim in the audit's own H-05 finding against the live tree; classifies H-05 as a coverage/baseline gap, not a defect; presents Option 1 (build a frozen hermetic baseline + negative control, zero certified-value impact) and Option 2 (defer), medium-high-confidence lean toward Option 1. No option chosen; no code touched; H-06/H-08/M-02/dasha boundary-proximity not started; JATAKA not implemented. Governance gates and 816/816 pytest re-run clean (16 DP identifiers, up from 15). Nothing pushed. |
| 6.0.0 | 2026-08-22 | **`ADR-0068` RATIFIED - FOUNDATION IS FORMALLY EXITED.** Recorded ratification (status-only edit, matching the `ADR-0063`-addendum mechanism). Verified repository state fresh (pytest 816/816, drift-check PASS, governance gates PASS). Identified JATAKA's exact unmet entry prerequisites: checked all six Dasha-roadmap steps individually against current repository state - **only step 1 (H-04, `ADR-0053`) is closed**; steps 2-6 (H-05, H-06, H-08, M-02, dasha boundary-proximity indicator) are genuinely untouched, confirmed by direct search. Restated (not newly recommended) the roadmap's own next-step sequencing for the owner's authorization. JATAKA not implemented, not authorized. No code touched; not merged to `main`. Nothing pushed. |
| 5.4.0 | 2026-08-22 | Recorded ratification of the `ADR-0063` addendum (status-only edit, per explicit instruction). Performed a fresh FOUNDATION-exit readiness audit against all six `Q8_CLOSURE_MATRIX.md` s4 scope items, re-verifying on-disk certification artifacts and every relevant ADR's status directly: **finds no remaining gap** - four items certified/resolved, two explicitly decoupled by ratified decision. Drafted `ADR-0068` (`Status: PROPOSED`), presenting this evidence and, if ratified, declaring FOUNDATION exited - not self-ratified, per the owner's own explicit caution. Notes this would not authorize JATAKA (its own entry criteria separately unmet). No code touched; not merged to `main`. Governance gates and 816/816 pytest re-run clean (68 ADR entries, up from 67). Nothing pushed. |
| 5.3.0 | 2026-08-22 | Drafted a proposed addendum to `ADR-0063` (`Status: PROPOSED`, not ratified), per owner instruction, resolving civil-date rendering's FOUNDATION-exit gap narrowly with ten explicit terms mirroring `DP-015`'s "Option 3 (AMENDED)" treatment. `ADR-0063` and `DP-012` both unedited - `DP-012`'s technical investigation not reopened; no new Q8 interpretation asserted. No code touched. Governance gates and 816/816 pytest re-run clean. Nothing pushed. |
| 5.2.0 | 2026-08-21 | `ADR-0067` records `DP-015`'s full ratification (Q1/Q2 confirmed; Q3's "Option 3 (AMENDED)" ratified exactly as written, quoted verbatim in the ADR). FOUNDATION-exit readiness audit performed: rise/set, panchanga, trikalam certified and checkpointed; H-01/H-02 resolved; boundary-proximity explicitly decoupled by decision. **Civil-date rendering's `ADR-0063` deferral asserts it "satisfies s4's exit language" - an assertion made before `DP-015`'s rigorous carve-out analysis existed, now called into question by the owner's own confirmed characterization (c). FOUNDATION does NOT yet unambiguously satisfy its exit criteria.** No exit determination recorded; no JATAKA prep begun. Nothing pushed. |
| 5.1.0 | 2026-08-21 | CEO confirmed `DP-015` Questions 1 and 2 as drafted (novel/no-precedent; characterization (c), genuinely ambiguous). Question 3's original Option 3 rejected after owner verification found it silent on 2 of 5 required safeguards. Amended `DP-015` (v2.0.0 -> v3.0.0): original Option 3 preserved unedited, marked NOT RATIFIED; new "Option 3 (AMENDED)" drafted with all eight owner-specified terms, presented for ratification - not yet ratified, no ADR written. No code touched; no blocking mechanism built for a nonexistent consumer. Governance gates and 816/816 pytest re-run clean. Nothing pushed. |
| 5.0.0 | 2026-08-21 | Restructured `DP-015` (v1.0.0 -> v2.0.0) into an explicit, non-collapsible three-question CEO decision package: Question 1 (H-01/`ADR-0066` finding, confirmation-only) kept visibly separate from Question 2 (Q8 deferral-carve-out scope - three named characterizations with exact governing language and consequences, none selected) and Question 3 (boundary-proximity options, cross-referenced per-characterization). `DP-012`/`ADR-0063` no longer framed as precedent for deferral working here. No code touched; H-01 not reopened; carve-out not extended. Governance gates and 816/816 pytest re-run clean. Nothing pushed. |
| 4.9.0 | 2026-08-21 | Independently re-verified the H-01/`ADR-0066` Q8-exit-criteria reading against the exact ratified text and a Phase G precedent check (holds, but flagged as a novel, unprecedented application - `ADR-0049`'s B-01/B-02/B-03 were fully resolved, never actually deferred, despite an equivalent clause). Investigated the boundary-proximity-indicator gap: nothing ratified governs it; drafted `DP-015`, surfacing a textual ambiguity in `Q8_CLOSURE_MATRIX.md` s4 about whether the deferral-with-blocking carve-out extends beyond H-01/H-02 by name (bearing on this item and on civil-date rendering's existing deferral too). Three treatment options presented, low-confidence lean toward deferral. Decides nothing; not implementation-authorized. `d2a780c` held back from push per explicit instruction. |
| 4.8.0 | 2026-08-21 | `ADR-0066`: H-01 fix Option 2 implemented - `UnsupportedNodePolicyError` raised from `find_crossings()` for any non-mean node policy on Rahu/Ketu (fail-closed, covers every caller automatically). No certified value changed (isolated-venv re-verification: PASS, only known ULP noise + volatile fields differed, discarded not committed). FOUNDATION-exit readiness audit: rise/set, panchanga, trikalam certified; civil-date rendering deferred; H-02 resolved/certified; H-01 now resolved via Q8's explicit-deferral-with-blocking clause (Claude's own reading, flagged for confirmation). Boundary-proximity indicators found completely unaddressed - standing FOUNDATION-exit blocker. Local-only, not pushed. |
| 4.7.0 | 2026-08-21 | H-01 decision-readiness: `DP-014` drafted and registered, extracting `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md`'s H-01 finding, re-verified live (TrueNode grid step still exactly 37.5 days), and tracing the defect's blast radius across all eight `node_policy` consumers - confined to `find_crossings()`'s callers; KP already independently refuses true node. Presents the audit's own two solutions plus a defer option; recommends explicit refusal (Option 2) at medium confidence. Decides nothing, not implementation-authorized. Local-only, not pushed. |
| 4.6.0 | 2026-08-21 | Pushed `9737ddb` (TRANSIT_V1 evidence recovery: one ULP-level Gate C float difference, unpinned-vs-pinned dependency noise, recovered via CI-sourced overlay). CI run `32478694212` all four jobs green, Gate E re-confirmed. `DP-013`/H-02 fully closed. |
| 4.5.0 | 2026-08-21 | `ADR-0065`: H-02 fix Option 1 implemented - `TransitEvent.declared_division` (additive), new Gate E in `certify_transits.py` (49 cases, genuine negative control). All gates green locally (isolated exploration venv), 812/812 pytest, M-03 unchanged. No certified value changed. Push authorization pending. |
| 4.4.0 | 2026-08-21 | `DP-013` s6 (new): fix-option decision-readiness analysis. Verified `engine.transits` has zero production consumers; `division_index` feeds nearly every certified classifier. Option 3 verified to touch the FORMALLY LOCKED Tier-0 scope. Recommends Option 1 (high confidence); does not choose. |
| 4.3.0 | 2026-08-20 | Pushed `f3399f3`; CI run `32375941348` all four jobs green, both H-02 steps confirmed genuinely executed under the hash-pinned oracle environment with results identical to the local runs. H-02 reproduction complete; choosing a fix option is the sole remaining, non-blocking item. |
| 4.2.0 | 2026-08-20 | `ADR-0064`: `DP-013` Option C ratified and executed. H-02 independently reproduced for the Sun (2/12, exact match to the original audit); Moon 15/34 (44%, comparable). PyJHora recorded as an evidenced limitation (search diverges/times out at 0.0001deg; direct longitude carries a 20.57 arcsec bias, ~206,000x the defect's scale) rather than manufactured agreement. New tests (8), negative controls, independent validator, non-gating CI wiring. No fix chosen; TRANSIT_V1 unmodified. Push authorization pending. |
| 4.1.0 | 2026-08-20 | `DP-013` decision-readiness audit: re-verified the 278x tolerance mismatch against live code (unchanged); directly inspected PyJHora's source and confirmed Option B's API is real but its default precision is ~4 orders of magnitude too coarse. Full options/evidence/trade-offs/recommendation laid out in this file for CEO ratification. Nothing decided, nothing implemented. |
| 4.0.0 | 2026-08-20 | `DP-013` drafted and registered: H-02 ingress-classification seam, extracting `ADR-0020` D5's already-written analysis (verified against the original `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` finding directly). 3 reproduction-methodology options, 3 preserved fix options (not recommended among). `ADR-0020` not ratified, H-02 not resolved. |
| 3.9.0 | 2026-08-20 | `ADR-0063`: `DP-012` Option C ratified (civil-date rendering deferred, not authorized) - caught and corrected a prior instruction that mislabeled Option A's content as "Option C" before any code was written. Corrected all state-file wording implying implementation was pending. Identified an H-02 decision-paper candidate; not drafted. |
| 3.8.0 | 2026-08-20 | `DP-012` decision-readiness audit: empirically disproved the fold/gap-ambiguity sub-question (a mistaken analogy to `BirthData`'s opposite-direction problem) - `astimezone()` on an unambiguous UTC instant is fully deterministic. Two genuine sub-decisions remain. Nothing decided, nothing implemented; no other FOUNDATION work found authorized. |
| 3.7.0 | 2026-08-20 | Verified `42d61c3`/checkpoint record/state files already correct, no changes needed. Independently advanced `DP-012` via a real `zoneinfo`/`tzdata` probe (LMT-era vs. standardized-zone distinction) - research only, decides and implements nothing. |
| 3.6.0 | 2026-08-20 | Owner accepted `TRIKALAM_V1`'s FOUNDATION checkpoint (`ADR-0061` third addendum) - production-certified. Drafted and registered `DP-012` (civil-date rendering for dasha boundaries) as the next tractable FOUNDATION item; not implemented, awaiting ratification. |
| 3.5.0 | 2026-08-20 | Pushed `8e6bb40`; CI run `32361308330` all four jobs green, ULP battery confirmed genuinely executed from the oracle-job log directly. CEO-audit HOLD finding closed. FOUNDATION per-capability checkpoint re-presented as the sole open decision. |
| 3.4.0 | 2026-08-20 | CEO audit: `TRIKALAM_V1` Gate C lacked a genuine ULP battery (verified independently, finding correct). Remediated: exact-sunrise-boundary ULP test + negative control. All six gates re-verified locally (PASS), 801/801 pytest. Push authorization pending for CI re-confirmation. |
| 3.3.0 | 2026-08-20 | Confirmed `bf0d414` pushed and CI run `32358109807` fully green (all four jobs). `TRIKALAM_V1` is CI-confirmed. Presented the FOUNDATION per-capability checkpoint as the sole open owner decision, not self-certified. |
| 3.2.0 | 2026-08-20 | Pushed `3487add`; CI run `32353401132` confirmed `TRIKALAM_V1`'s Gate F genuinely PASSED under the hash-pinned oracle environment. Same run's drift-assertion steps failed on the expected M-03 177->180 field; recovered via CI-sourced overlay in commit `9e33490` (not yet pushed). |
| 3.1.0 | 2026-08-20 | `ADR-0062`: added `docs/ACE_EXECUTION_STATE.md` (canonical current-state snapshot) and `specs/CLAUDE_WORKFLOW.md`'s "Execution-state recovery" section; explicit permanent prohibition on relaying reports between Claude and ChatGPT through the user. No approval checkpoint weakened. |
| 3.0.0 | 2026-08-20 | `ADR-0061`: `TRIKALAM_V1` (`PYJHORA_TRIKALAM_V1` variant) implemented - new `engine.astrology.trikalam`, tests, certifier, validator, CI wiring. All six gates locally verified (unpinned exploration venv); 799 tests pass. Not yet committed/pushed/CI-confirmed. |
| 2.9.0 | 2026-08-20 | `ADR-0060`: `DP-011` ratified (Option C seeded by Option B); PyJHora 4.8.7 `trikalam()` convention independently inspected and frozen as `PYJHORA_TRIKALAM_V1`. Implementation/certification work proceeding next. |
| 2.8.0 | 2026-08-19 | Owner accepted Panchanga's FOUNDATION per-capability checkpoint (`ADR-0059` addendum); identified `DP-011` (Rahu Kalam/Yamaganda/Gulika variant-table options) as the sole FOUNDATION decision-paper item already authorized to draft. |
| 2.7.0 | 2026-08-19 | FOUNDATION checkpoint audit (read-only): independently re-verified HEAD/CI/register against `Q8_CLOSURE_MATRIX.md` s4; confirmed no remaining FOUNDATION capability besides Panchanga has satisfied prerequisites for implementation (Rahu Kalam/Yamaganda/Gulika, civil-date rendering, H-01, H-02, boundary-proximity all lack a governing ratified ADR/DP); confirmed the sole open item is Panchanga's per-capability CEO checkpoint acceptance. No code, no new ADR. |
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
