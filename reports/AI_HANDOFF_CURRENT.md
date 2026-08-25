<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | INDEX ONLY - navigation aid, not evidence. See "What this file is" below. |
| Version | 9.4.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-25 (**D45 (Akshavedamsa) IS NOW LIVE ON `main`** - PR #5 merged, merge commit `c49336d`. `main`'s own post-merge CI (`32825473827`) all four jobs green, confirmed directly: 857/857 pytest, 6 certified vargas, D45 5400/0 mismatches, artifact-drift clean both tiers. All six preconditions and eight post-merge checks the owner named independently verified. Task complete.) |
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

### 2026-08-25 - D45 JATAKA milestone merged to main: PR #5, merge commit c49336d, post-merge CI fully verified
- Branch / commit SHA: `phase-g-governance` (local), `main` now at `c49336dd501301dde720aa8297fa181506fe64bd`
  on `origin` - the merge commit itself (parents `d738520` + `c85284a`).
- Previous approved commit: `c85284a` on `phase-g-governance` (the CI-green CI-drift-fix commit, already
  pushed); `d738520` on `main` (the prior JATAKA-entry merge, PR #4).
- Task (owner's exact instruction): "CEO AUTHORIZATION — MERGE D45 JATAKA MILESTONE. Merge the current
  CI-green phase-g-governance state into main. Preconditions: verify current branch and exact SHA; verify
  working tree; verify origin/phase-g-governance is exactly the CI-confirmed c85284a state; verify CI run
  32822832747 is successful; verify no uncommitted tracked changes; verify main has no unexpected
  independent work. Execute a standard two-parent merge via PR. No squash, no rebase, no force-push.
  After merge: verify resulting origin/main SHA; verify source branch is contained in main; inspect the
  resulting CI run directly to completion; confirm 857/857 tests, governance PASS, oracle PASS, D45
  certification PASS and artifact-drift PASS; confirm D45 remains registered as the sixth certified
  production Varga; confirm no unrelated production capability was introduced; confirm working tree
  state. Do not start DP-024, DP-025, DP-026 or DP-027 yet. Do not modify production code during the
  merge."
- Relevant ADR/specification: `ADR-0074` (JATAKA entry), `ADR-0076`/`ADR-0077` (D45 readiness/
  certification, both already ratified/merged), none reopened this task.
- Files changed: none beyond the standard merge commit itself (`c49336d`, a plain two-parent merge, no
  file edits by Claude as part of the merge action); `docs/ACE_EXECUTION_STATE.md` (version 7.3.0 ->
  7.4.0), this file, as the post-merge documentation refresh.
- Method: verified all six named preconditions directly before acting - `git branch --show-current`,
  `git rev-parse HEAD`, `git status --porcelain`, `git fetch` + `git rev-parse origin/phase-g-governance`
  (confirmed exactly `c85284a1db59d85cc12f46094a1c2f7c0e0bb129` - local HEAD was actually `df8d65a`, one
  commit ahead with a documentation-only entry never pushed; correctly excluded from this merge since the
  owner's own instruction explicitly named `c85284a` as "the CI-confirmed state" to merge), `gh run view
  32822832747 --json conclusion,headSha` (confirmed `"success"` for that exact SHA), and `git log
  origin/phase-g-governance..origin/main --oneline` (confirmed only `main`'s own three historical merge
  commits, no independent work). Created the PR via `gh pr create --base main --head phase-g-governance`
  (PR #5) - since nothing was pushed beyond `c85284a`, this correctly picked up the remote branch's own
  current tip, not local HEAD; confirmed via `gh pr view 5 --json headRefOid` that the PR's own head SHA
  was exactly `c85284a`. Waited for the PR's own CI run (`32825195900`) to complete green before merging -
  did not merge on the strength of the earlier push-triggered run alone. Merged via `gh pr merge 5
  --merge` (no `--squash`, no `--rebase`, no `-f`). Verified the resulting merge commit's own parents
  directly (`git log -1 --format="%H%nparents: %P"` on `origin/main`) to confirm a genuine two-parent
  merge, not a squash or fast-forward.
- Key findings (post-merge verification, each independently confirmed, not assumed): resulting
  `origin/main` SHA `c49336dd501301dde720aa8297fa181506fe64bd`, parents `d738520ffc796d07468e24a5b1
  dddcfba3120c65` + `c85284a1db59d85cc12f46094a1c2f7c0e0bb129`. `git merge-base --is-ancestor c85284a
  origin/main` returned true - the source branch's own tip is genuinely contained in `main`. `main`'s own
  post-merge CI run (`32825473827`) watched to completion via `gh run watch --exit-status`, then its own
  conclusion independently re-confirmed via `gh run view --json conclusion` (`"success"`) and by pulling
  specific evidence lines directly from the full log (`gh run view --log`), not inferred from checkmarks:
  `857 passed` on all four legs (both Python versions, both the default gate and the network-guard
  re-run); the governance gate's own `Certified varga registry matches its declared constant` step -
  present in this CI configuration for the first time observed this session - printed `PASS: 6 certified
  vargas, each with a PASS artifact citing a compliant decision entry`, independent CI-side confirmation
  that D45 is the sixth certified varga with a compliant artifact and decision entry; `77 ADR entries`;
  `27 registered DP identifiers`; the oracle gate's own `Oracle certification runners (all eleven)` step
  showed D45's own `C_oracle: {'comparisons': 5400, 'mismatches': 0}` and `KP_CHAIN_V1`'s own `lord
  mismatches: 0`; both drift-assertion steps (oracle-tier and no-oracle-tier) printed `PASS: 49 evidence
  file(s) identical to the committed version outside the volatile fields`, and the no-oracle-tier step
  additionally printed `no tracked source file was modified by any certification run`. Directly inspected
  `origin/main`'s own committed tree via `git show origin/main:engine/astrology/__init__.py` and `git show
  origin/main:engine/astrology/varga_d45.py` to confirm `CERTIFIED_PRODUCTION_VARGAS` carries all six
  entries (`2, 3, 7, 12, 30, 45`) and the D45 module itself is present, not merely inferred from the CI
  log. Computed the full `git diff --stat d738520 c49336d` (75 files total; 23 under `engine/`/`scripts/`)
  and confirmed the `engine/`/`scripts/` scope is exactly D45's own certification/implementation footprint
  (the new module, its registration, its certifier/validator, the `.as_posix()` fixes, and the pinning-
  test updates this segment's own work required) - no other production capability, no D24/D40/etc, no
  Jaimini/BNN/Numerology/KP-significator/yoga code anywhere in the diff. Confirmed `git status --porcelain`
  clean both before and after the merge.
- Implementation summary: no production code modified by Claude as part of this task - the merge itself
  is a standard, content-neutral two-parent merge commit; all engine/scripts content had already been
  committed, certified, and CI-confirmed in prior tasks.
- Tests executed and results: confirmed via `main`'s own post-merge CI log (857 passed, all four legs);
  not re-run locally this task since nothing changed locally beyond the merge action itself (executed via
  GitHub's own merge API, not a local `git merge`).
- Certification executed and results: confirmed via `main`'s own post-merge CI log - all eleven oracle-
  tier certifiers PASS (D45 5400/0 mismatches; KP_CHAIN 0 lord mismatches); artifact-drift PASS in both
  tiers.
- Governance checks executed and results: confirmed via `main`'s own post-merge CI log - 77 ADR entries,
  27 registered DP identifiers, 6 certified vargas each with a compliant artifact/decision entry, all
  PASS.
- Known issues: none.
- Unresolved questions: none for this task. `DP-024`-`DP-027` each remain open, separately-authorized
  items, explicitly not started this task, per the owner's own instruction.
- CEO decision required: none - this task's own explicit stop condition ("stop after the merge and CI
  verification and report") is satisfied by full completion, not a pending decision. The natural next
  decisions (`DP-024`-`DP-027` disposition; the next JATAKA capability) remain open for the owner's own
  future direction.
- Next authorized action: none self-executable. Awaiting the owner's next instruction.

### 2026-08-25 - phase-g-governance fully green on origin: CI-drift fix pushed and confirmed
- Branch / commit SHA: `phase-g-governance`, `c85284a1db59d85cc12f46094a1c2f7c0e0bb129` - **pushed and
  confirmed identical on `origin/phase-g-governance`** (fast-forward `2cb9f30..c85284a`).
- Previous approved commit: `2cb9f30` (D45 production implementation), already pushed.
- Task (owner's exact instruction, continuing from the same "AUTHORIZE PUSH" message as the immediately
  preceding entry): watch CI to completion, inspect the actual logs, and stop at the next genuine CEO
  decision point.
- Relevant ADR/specification: none reopened. `main` untouched - no merge performed or requested.
- Files changed: none beyond the immediately preceding entry's own fix commit; this entry documents its
  push and CI confirmation, plus `docs/ACE_EXECUTION_STATE.md` (version 7.2.0 -> 7.3.0), this file.
- Method: `git push origin phase-g-governance` (plain push); verified `git rev-parse HEAD` and
  `git rev-parse origin/phase-g-governance` byte-identical; located the new run via `gh run list`; watched
  it via `gh run watch <id> --exit-status`, which exited zero this time; independently confirmed via
  `gh run view <id> --json conclusion,status,headSha` (`"success"`, headSha matching the pushed commit
  exactly); pulled specific evidence lines directly from the full log (`gh run view <id> --log`) rather
  than trusting the green checkmarks alone.
- Key findings: all four jobs green. Oracle gate: `Oracle certification runners (all eleven)` shows every
  certifier's own `RESULT: PASS`, including D45's own `C_oracle: {'comparisons': 5400, 'mismatches': 0}`
  and `KP_CHAIN_V1`'s `lord mismatches: 0`; `Assert regenerated artifacts drifted only in the volatile
  fields` shows `PASS: 49 evidence file(s) identical to the committed version outside the volatile fields
  (19 machine-readable, 30 rendered)`. Both no-oracle-tier legs (Python 3.11, 3.12): `857 passed` in the
  default gate and again under the network-guard re-run; `Assert regenerated artifacts did not drift, then
  that no source changed` shows `no tracked source file was modified by any certification run`.
  Governance gate: `PASS: 77 ADR entries`, `PASS: 27 registered DP identifiers`, and a governance step not
  previously observed this session, `Certified varga registry matches its declared constant`, which
  printed `PASS: 6 certified vargas, each with a PASS artifact citing a compliant decision entry` - an
  independent, CI-side confirmation (not something this session wrote or ran locally) that D45 is
  correctly recognized as the sixth certified production varga with a compliant artifact and decision
  entry.
- Implementation summary: none this entry - documentation and verification only.
- Tests executed and results: confirmed via CI log (857 passed, both legs); not re-run locally this entry
  since nothing changed since the immediately preceding local verification.
- Certification executed and results: confirmed via CI log (all eleven oracle-tier certifiers PASS; drift
  checks clean in both tiers).
- Governance checks executed and results: confirmed via CI log (77 ADR entries, 27 DP identifiers, 6
  certified vargas with compliant artifacts/decisions - all PASS).
- Known issues: none.
- Unresolved questions: none for this task. Open, separately-authorized items remain: `DP-024` (varga
  framework `step`/payload-table question), `DP-025` (polar-Placidus/M-04 Tier-0 maintenance), `DP-026`
  (`ADR-0027`/KP-significator provenance follow-up), `DP-027` (Parashari-yoga oracle/specification
  follow-up), and whether/when to merge `phase-g-governance` into `main` (not requested or assumed here).
- CEO decision required: none - this task's own explicit stop condition ("stop at the next genuine CEO
  decision point") is satisfied by the task itself being complete, not by a pending decision. The natural
  next decisions (merge to `main`; `DP-024`-`DP-027` disposition; next JATAKA capability) remain open for
  the owner's own future direction, not urgent or blocking.
- Next authorized action: none self-executable. Awaiting the owner's next instruction.

### 2026-08-25 - Push authorized and executed; CI genuinely failed on real drift; root-caused, fixed, and re-pushed
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the CI-drift fix,
  on top of `2cb9f30`, the pushed D45 production-implementation commit).
- Previous approved commit: `2cb9f30` (D45 production implementation) - pushed to `origin/phase-g-
  governance` this task, confirmed byte-identical remote SHA (`c4d571a..2cb9f30`, fast-forward).
- Task (owner's exact instruction): "AUTHORIZE PUSH — push the current nine local commits to
  phase-g-governance, verify remote SHA, run/watch CI to completion, inspect the actual logs, and stop at
  the next genuine CEO decision point. Do not merge to main unless separately authorized."
- Relevant ADR/specification: none reopened. Cites the established "TRANSIT_V1 evidence recovery"/CI-
  sourced-overlay precedent from earlier this session, applied again here for two files.
- Files changed (this fix, on top of the pushed commit): `scripts/certify_current_engine.py`,
  `certify_d2.py`, `certify_d3.py`, `certify_d7.py`, `certify_d12.py`, `certify_d30.py`, `certify_d45.py`,
  `certify_kp_chain.py`, `certify_parashari_drishti.py`, `certify_rise_set.py`,
  `certify_sign_convention.py`, `certify_vimshottari.py` (each: one `print()` call fixed to use
  `.as_posix()`), `certification/KP_CHAIN_V1_certification.json`, `PANCHANGA_V1_certification.json`,
  `PARASHARI_DRISHTI_V1_certification.json`, `RISE_SET_V1_certification.json`,
  `TRANSIT_V1_certification.json`, `TRIKALAM_V1_certification.json`, `VIMSHOTTARI_V1_certification.json`,
  `current_engine_certification.json` (all regenerated or CI-recovered), plus their corresponding
  `reports/certification/*.report.md`/`*.console.txt` files, `docs/ACE_EXECUTION_STATE.md` (version
  7.1.0 -> 7.2.0), this file.
- Method: pushed via `git push origin phase-g-governance` (plain push, no force); verified
  `git rev-parse HEAD` and `git rev-parse origin/phase-g-governance` byte-identical; located the new run
  via `gh run list --branch phase-g-governance`; watched it via `gh run watch <id> --exit-status`, which
  exited nonzero - a genuine failure, not assumed clean from the push succeeding. Pulled the actual
  failure text via `gh run view <id> --log-failed`, not just the pass/fail summary, and read every line
  of the drift-check output directly. Diagnosed cause 1 (`modules_scanned` project-wide shift) by
  recognizing the exact number (183) matched the three new files added to the scan-scope tuples two tasks
  ago, and confirming which artifacts were NOT among those regenerated at that time. Diagnosed cause 2
  (Windows path separator) by directly comparing the committed backslash-containing console lines against
  CI's own forward-slash lines in the same failure log. Regenerated every affected non-swetest,
  non-ULP-sensitive artifact locally, using the same local PyJHora installation (via `PYTHONPATH`) already
  used for D45's own certification work. For the two exceptions - `current_engine_certification.json`
  (needs the bundled Linux-ELF `swetest` binary, unrunnable on this Windows host) and
  `TRANSIT_V1_certification.json` (a field-level Windows/Linux floating-point ULP discrepancy, confirmed
  by direct three-way comparison: committed value, this session's own local Windows regeneration, and
  CI's own regeneration - the committed and CI values matched exactly; only the local Windows value
  differed) - downloaded the failed run's own uploaded artifacts (`gh run download <id> -n <artifact-
  name> --dir <path>`, using the correct per-job artifact: `hermetic-certification-evidence-3.11` for the
  no-oracle-tier `current_engine_certification.json`, `oracle-certification-evidence` for the oracle-tier
  `TRANSIT_V1_certification.json`), diffed each field-by-field against the committed version to confirm
  the only differences were volatile fields plus the one understood, deliberate change, then copied those
  CI-produced files into place rather than trusting a locally-drifted regeneration.
- Key findings: both CI failures were real, diagnosable, and entirely attributable to this session's own
  prior work - not flakiness, not an environment problem to route around. The `modules_scanned` ripple
  effect is a genuine class of risk worth naming going forward: changing `certification_support.py`'s own
  scan-scope tuples has a project-wide effect on every certifier's own reported precondition count, not
  just the certifier(s) directly being worked on - any future change to those tuples must regenerate
  every certifier's own artifact, not only the ones under direct edit. The Windows-path-separator bug was
  pre-existing in most of these scripts (not introduced this session, except for the one instance in the
  newly-written `certify_d45.py`) but had simply never been triggered before, since this project's own
  established practice is normally to regenerate certifiers only in the CI environment or to accept the
  documented Windows/Linux gate-parity gap for swetest-dependent runs - running this many non-swetest
  certifiers locally on Windows, back-to-back, surfaced it for the first time.
- Implementation summary: twelve one-line `print()` fixes (no calculation logic touched). Nine
  certification artifacts (plus their reports/transcripts) regenerated or CI-recovered, all differing from
  the previously-committed versions only in the two understood, deliberate respects.
- Tests executed and results: `python -m pytest -q` - 857/857 passed, unchanged.
- Certification executed and results: `python scripts/check_artifact_drift.py` - every remaining diff
  confirmed to be exactly the two understood changes (`modules_scanned` 180->183; backslash->forward-slash
  console paths), nothing unexplained.
- Governance checks executed and results: `python scripts/check_adr_numbering.py` (77 ADR entries,
  unchanged), `python scripts/check_identifier_families.py` (27 DP identifiers, unchanged), `python
  scripts/check_retired_identifiers.py` (0 violations) - all PASS.
- Known issues: none new - both causes fully understood and fixed, not worked around.
- Unresolved questions: whether the second CI run (after this fix is pushed) passes clean - to be
  confirmed directly, not assumed, before this task's own genuine stopping point is reached.
- CEO decision required: none yet - per the owner's own explicit "continue until the next genuine CEO
  decision point" instruction, this task continues past this fix's own commit into pushing it and
  watching the second CI run to completion, within the same turn.
- Next authorized action: commit this fix, push it to `origin/phase-g-governance`, watch the resulting CI
  run to completion, inspect its actual logs, and report the genuine result - continuing the same
  authorized task.

### 2026-08-25 - D45 production implementation complete: JATAKA's first production capability, sixth certified varga
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the production-
  implementation's own files, on top of `d83b3b0`).
- Previous approved commit: `d83b3b0` (the `ADR-0077`-ratification/certification-execution commit,
  local-only, eight commits ahead of `origin/phase-g-governance`'s
  `c4d571a340b4baf873fbefb5661eb195937d2f51`).
- Task (owner's exact instruction, abridged): "CEO AUTHORIZATION — D45 PRODUCTION IMPLEMENTATION. I
  authorize production implementation of D45 based on the successfully completed and certified ADR-0077
  execution. Implement engine/astrology/varga_d45.py and perform the minimum required registry/model/
  integration work necessary to make D45 a production-usable certified Varga. Preserve the certified rule
  exactly. Do not change the certified D45 mathematics merely for implementation convenience. Required:
  production implementation; registry integration; provenance/variant declaration; tests; independent
  regression coverage; certification-artifact drift protection; re-run the complete certification suite;
  verify existing certified Vargas remain unchanged; verify D45 is now correctly discoverable/usable
  through the production registry; genuine negative-control verification; full CI. Do not begin D24/D40/
  D16/D27/etc. Do not touch DP-024/025/026/027. Do not touch Foundation, closed Dasha items, H-03 or
  H10/H11. Do not begin interpretation, convergence, BTR, historical prediction or other Jataka
  capabilities. Do not push or merge without separate authorization."
- Relevant ADR/specification: `ADR-0077` (the certified design this implementation follows exactly);
  `docs/NEW_VARGA_IMPLEMENTATION_TEMPLATE.md`/`engine/astrology/varga_d12.py` (the established production-
  registration pattern mirrored precisely); `docs/VARGA_CERTIFICATION_ROADMAP.md` section 7 (the
  documented sign-convention-recertification trap, encountered and correctly handled).
- Files changed: `engine/astrology/varga_d45.py` (new - the production module), `engine/astrology/
  __init__.py` (registers D45, extends `CERTIFIED_PRODUCTION_VARGAS`), `engine/tests/test_varga_d45.py`
  (new - 13 tests), `engine/tests/test_varga_batch_d7_d30_d2.py`, `test_varga_d12.py`, `test_varga_d3.py`,
  `test_varga_framework.py` (each had a hardcoded "still refused" division list needing `45` removed),
  `engine/tests/test_sign_convention_certification.py` (new pinned `D45_parashara` sweep hash),
  `scripts/certify_d45.py` (gate D rewritten to assert D45 is registered), `validate_d45_holdout.py`
  (now validates the production registered rule), `certification/VARGA_D45_V1_certification.json` and its
  reports (regenerated, production-registered framing), `certification/VARGA_D2/D3/D7/D12/D30_V1_
  certification.json` and their reports (regenerated, byte-identical certified values, registry list now
  shows six entries), `certification/SIGN_CONVENTION_V1_certification.json` and its reports (regenerated,
  new D45 entry, five pre-existing hashes unchanged), `docs/ACE_EXECUTION_STATE.md` (version 7.0.0 ->
  7.1.0), this file.
- Method: mirrored `engine/astrology/varga_d12.py`'s exact structure for the new production module -
  same frozen-rule-then-`ensure_registered()`-at-import pattern. Before writing any registry-integration
  code, read `engine/astrology/divisional_chart.py` and `varga_chart_builder.py` directly and confirmed
  both are fully generic (built during Phase A "so Phase D vargas plug in without new plumbing") - no
  registry-dispatch or provenance-propagation code needed writing or changing; verified this empirically
  by calling `divisional_chart(snapshot, 45)` directly and inspecting the returned `VargaChart`'s own
  `varga`/`school`/`provenance` fields before writing any tests. Wrote `engine/tests/test_varga_d45.py`
  by directly adapting `test_varga_d12.py`'s own test-by-test structure, computing D45's own genuine
  content hash (`c8515e44be6e21e3e8c3298121b8c0e4687c0176d9da7e94f7d0aba53a8bf817`) rather than inventing
  one. Searched the full tree for every other consumer that iterates the registry or hardcodes a varga
  count, to avoid missing a legitimate required update (found and fixed four "still refused" test lists);
  ran the full pytest suite BEFORE assuming completeness, which caught the sign-convention certifier's
  own pinned-hash dependency - the exact trap `docs/VARGA_CERTIFICATION_ROADMAP.md` section 7 documents by
  name - and fixed it by computing the genuine fresh hash via the certifier's own function, not by
  guessing or disabling the check.
- Key findings: registry integration, provenance propagation, and dispatch discoverability required zero
  new plumbing beyond the two-file registration pattern (`varga_d45.py` + `__init__.py`) - the generic
  Phase-A infrastructure already handled everything else, confirmed empirically rather than assumed. The
  sign-convention certifier's own registry-iteration dependency (documented but easy to miss) was
  encountered for real and handled correctly: a genuinely fresh hash was computed and pinned, not
  fabricated. All five pre-existing certified vargas and D9/D10 were independently reconfirmed byte-
  identical across two independent verification paths (each varga's own certifier, and the sign-
  convention certifier's own cross-layer sweep) - no certified value changed anywhere.
- Implementation summary: production code written and registered for the first time as part of JATAKA
  (`engine/astrology/varga_d45.py`, `engine/astrology/__init__.py`). The certified rule table is
  byte-for-byte identical to `ADR-0077`'s own frozen values - confirmed both by direct comparison and by
  the content-hash pin matching the certification-execution run's own recorded hash.
- Tests executed and results: `python -m pytest -q` - 857/857 passed (844 + 13 new from
  `test_varga_d45.py`; four pre-existing tests updated for the legitimate `45`-now-supported change).
- Certification executed and results: `python scripts/certify_d45.py` - PASS, all eight gates, now
  confirming D45 **is** registered with the correct identity/content hash. `python scripts/certify_d2.py`/
  `certify_d3.py`/`certify_d7.py`/`certify_d12.py`/`certify_d30.py` - all PASS, D9/D10 hashes byte-
  identical, registry list now shows six entries as expected. `python scripts/certify_sign_convention.py`
  - PASS, D45's own genuine sweep hash computed and recorded, five pre-existing hashes unchanged.
- Governance checks executed and results: `python scripts/check_adr_numbering.py` (77 ADR entries,
  unchanged), `python scripts/check_identifier_families.py` (27 DP identifiers, unchanged - no new DP
  registered), `python scripts/check_retired_identifiers.py` (0 violations) - all PASS.
- Known issues: none new.
- Unresolved questions: what JATAKA capability or maintenance item to pursue next - `DP-024` (varga
  framework `step`/payload-table question), `DP-025` (polar-Placidus/M-04 Tier-0 maintenance), `DP-026`
  (`ADR-0027`/KP-significator provenance follow-up), `DP-027` (Parashari-yoga oracle/specification
  follow-up) all remain open and untouched, per explicit instruction.
- CEO decision required: this task's own new genuine stopping point, per the owner's explicit closing
  instruction - review the evidence and decide whether to authorize a push of this task's commits. No
  D24/D40/D16/D27/etc. work was begun; `DP-024`-`DP-027` were not touched; no interpretation/convergence/
  BTR/historical-prediction/other-JATAKA-capability work was begun - all per explicit instruction.
- Next authorized action: none self-executable. Awaiting the owner's review and, separately, authorization
  to push this task's commits if desired.

### 2026-08-25 - ADR-0077 RATIFIED; D45 certification EXECUTED, all eight gates PASS; engine/astrology/varga_d45.py still does not exist
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the certification
  execution's own files, on top of `5113eac`).
- Previous approved commit: `5113eac` (the `ADR-0076`-ratification/`ADR-0077`-design commit, local-only,
  seven commits ahead of `origin/phase-g-governance`'s `c4d571a340b4baf873fbefb5661eb195937d2f51`).
- Task (owner's exact instruction, abridged): "CEO RATIFICATION — ADR-0077. I ratify ADR-0077 exactly as
  drafted. Authorize execution of the D45 certification work only: write the frozen D45 rule; build the
  independent validator; execute the defined oracle comparison; execute the defined boundary cases,
  including k=13, 26, 29; execute the protected holdout; execute genuine negative controls; generate the
  machine-readable certification artifact and human-readable report; establish artifact-drift protection
  and CI coverage; preserve the explicit non-claims and provenance. Do not create or modify
  engine/astrology/varga_d45.py yet. Production D45 implementation remains a separate authorization after
  certification execution establishes the required evidence. Do not ratify DP-026 or DP-027... Do not
  work on DP-024 or DP-025. Do not reopen Foundation, closed Dasha items, H-03, or H10/H11. Do not push or
  merge without separate authorization. Continue until the next genuine CEO decision, certification
  failure/blocker, or production-implementation authorization point."
- Relevant ADR/specification: `ADR-0077` (ratified via a new sub-entry); `docs/NEW_VARGA_IMPLEMENTATION_
  TEMPLATE.md`/`docs/VARGA_CERTIFICATION_ROADMAP.md` section 6 (the certification-requirements template
  this run's gate structure mirrors); `ADR-0049` (negative-control precedent).
- Files changed: `docs/DECISION_LOG.md` (`ADR-0077` ratification sub-entry), `scripts/certify_d45.py`
  (new - the certifier), `validate_d45_holdout.py` (new - the independent validator),
  `certification/VARGA_D45_V1_certification.json` (new - the machine-readable artifact),
  `reports/certification/varga_d45.report.md` (new - human-readable), `reports/certification/
  varga_d45.console.txt` (new - console transcript), `scripts/certification_support.py` (added
  `certify_d45.py`/`validate_d45_holdout.py` to the anti-fitting scan scope), `.github/workflows/ci.yml`
  (added `certify_d45.py` to the oracle-tier certifier loop, "all ten" -> "all eleven"),
  `engine/tests/test_certification_preconditions.py` and `engine/tests/test_retired_identifier_gate_
  scope.py` (updated pre-existing pinned counts - a correct, required consequence of legitimately adding
  a sixth varga certifier, not a bypass), `docs/ACE_EXECUTION_STATE.md` (version 6.9.0 -> 7.0.0), this
  file. **`engine/astrology/varga_d45.py` was NOT created; `engine/astrology/varga_registry.py` and
  `varga_rules.py` were NOT modified**, per explicit instruction.
- Method: the frozen D45 rule (a `CyclicVargaRule(divisions=45, start_sign=(0,4,8,0,4,8,0,4,8,0,4,8),
  direction=(1,)*12)`) was defined as a module-level constant inside `scripts/certify_d45.py` itself -
  never imported into or registered via `engine/astrology/varga_registry.py` - and passed directly to
  the existing, already-certified, general-purpose `engine.astrology.varga_classifier.classify(longitude,
  rule)` function, which accepts any rule object directly and has no registry dependency at all. This let
  every gate run against the real, exact frozen rule without ever registering it. PyJHora was invoked via
  a local installation found in the working session's own scratchpad (`oracle_probe_venv`, from earlier
  this session's own D45 readiness research) - the main Python environment has no PyJHora installed, so
  every certifier/validator run this task added that venv's `site-packages` to `PYTHONPATH` explicitly;
  CI itself needs no such adjustment, since its own oracle-tier job installs PyJHora directly via
  `requirements-oracle.lock` into the job's own environment.
- Key findings (two genuine defects found and fixed during execution, not hidden or worked around -
  itself evidence the gates are not rubber-stamps): (1) the independent validator's own first-draft
  reference formula (a naive floor, `int(degree // width)`) disagreed with `classify()`'s own already-
  correct, already-locked boundary-tolerance convention (`engine/astrology/longitude_utils.py`'s own
  "promote within 1e-10" rule) at 347 boundary-adjacent points during the validator's own boundary-case
  battery - not a defect in `classify()`, but a gap in the validator's own independent re-derivation,
  which had not yet accounted for the documented convention; fixed by independently re-implementing that
  same documented rule (`(degree + 1e-10) / width`) inside the validator's own code, sourced from the
  convention's own written documentation, not by importing the production function. (2) During gate H
  (negative controls), a planted direction-reversal mutation initially targeted the wrong tuple index
  (`direction[0]`, Aries, while the test longitude was in Taurus) and, once corrected to the right index,
  the first-chosen test longitude (segment index 18) landed on a mathematically degenerate point where
  `(start+index)%12` and `(start-index)%12` coincide whenever `index` is a multiple of 6 - both errors
  found and fixed (correct index targeted; a non-degenerate test longitude, segment index 10, chosen), the
  control then re-confirmed to genuinely detect its own planted mutation.
- Implementation summary: no calculation-engine production code touched (`engine/astrology/varga_d45.py`
  does not exist; `varga_registry.py`/`varga_rules.py` unmodified). Certification-execution work only:
  two new certifier/validator scripts, three new evidence files, two shared certification-infrastructure
  files updated (scan scope, CI loop), two pre-existing governance-pinning tests updated to reflect the
  legitimate new count.
- Tests executed and results: `python -m pytest -q` - 844/844 passed (both updated pinning-test
  assertions now pass for the correct, updated reason, not bypassed).
- Certification executed and results: `python scripts/certify_d45.py` (via `PYTHONPATH`-injected PyJHora)
  - **RESULT: PASS**, all eight gates green: A table integrity (12 cells, 0 mismatches); B dense sweep
  (51,429 points, 0 mismatches); C oracle (5,400 comparisons against PyJHora's `akshavedamsa_chart`, 0
  mismatches); D non-invasiveness (five existing certified vargas' own content hashes unchanged; D45
  confirmed genuinely unregistered - `get_varga_rule(45, "parashara")` still raises
  `UnsupportedVargaError`); E independent validator PASS; F boundary cases (60 checked, including k=13,
  26, 29 for all 12 signs, 0 mismatches); G protected holdout (26,278 points, prime-step sampling
  independent of the boundary cases, 0 mismatches); H negative controls (three planted mutations, all
  detected; the frozen rule object itself confirmed unmutated, since `CyclicVargaRule` is frozen).
  `python scripts/check_artifact_drift.py` - PASS, 46 pre-existing evidence files unaffected (the new D45
  files are not yet tracked at HEAD, so drift protection activates once committed).
- Governance checks executed and results: `python scripts/check_adr_numbering.py` (77 ADR entries,
  unchanged - `ADR-0077` was already counted when drafted), `python scripts/check_identifier_families.py`
  (27 DP identifiers, unchanged - no new DP registered this task), `python scripts/
  check_retired_identifiers.py` (0 violations) - all PASS.
- Known issues: none new.
- Unresolved questions: whether to authorize production implementation (writing and registering
  `engine/astrology/varga_d45.py`) - the explicit next stage both `ADR-0076` and `ADR-0077` reserved as a
  separate act, not performed this task.
- CEO decision required: this task's own new genuine stopping point, per the owner's explicit closing
  instruction - review the certification evidence (`certification/VARGA_D45_V1_certification.json`,
  `reports/certification/varga_d45.report.md`) and decide whether to authorize production implementation.
  No production code was written; `DP-024`/`DP-025`/`DP-026`/`DP-027` were not touched, per explicit
  instruction; no ADR beyond `ADR-0077` was ratified.
- Next authorized action: none self-executable. Awaiting the owner's review of the certification evidence
  and, separately, authorization to push this task's commits if desired.

### 2026-08-25 - ADR-0076 RATIFIED; ADR-0077 (D45 certification design) drafted; DP-024/DP-025 deferred; ADR-0027 provenance audited, not ratified; PyJHora yoga oracle found
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with this task's own
  files, on top of `1fc70fc`).
- Previous approved commit: `1fc70fc` (the `ADR-0076`/`DP-024`-`027` commit, local-only, six commits
  ahead of `origin/phase-g-governance`'s `c4d571a340b4baf873fbefb5661eb195937d2f51`).
- Task (owner's exact instruction, abridged, nine numbered items): "CEO DECISION. 1. RATIFY ADR-0076. D45
  (Akshavedamsa) certification work is authorized to begin. This authorizes certification work only, not
  production implementation beyond what is strictly required by the already-defined certification scope.
  2. DP-024 — DEFER. 3. DP-025 — DEFER for now... keep it as a separate Tier-0 maintenance item. 4.
  DP-026 — DO NOT ratify ADR-0027 yet. First perform the necessary independent audit of ADR-0027's
  provenance/source basis and determine whether it should become the governing KP-significator
  methodology authority. You may prepare decision-readiness, but do not implement KP significators. 5.
  DP-027 — DO NOT authorize yoga implementation. Oracle-availability research may proceed only as
  decision-readiness research... 6. D45 certification: proceed through the established certification
  workflow: freeze the exact rule/source; establish the authoritative reference; independently derive the
  calculation; resolve/measure the 30/45 cell-width representability issue rather than assuming it is
  acceptable; define boundary cases; define protected holdout; define negative controls; establish oracle
  comparison; establish artifact/drift protection; define explicit non-claims; prepare the certification
  ADR/artifacts. Important: Do not silently turn the PyJHora implementation into the normative authority
  merely because it agrees with the roadmap. It is independent corroboration, not automatically normative
  authority. Do not push or merge. Do not ratify any other ADR. Continue until the next genuine CEO
  decision, methodology/source blocker, or certification-design question requiring my decision."
- Relevant ADR/specification: `ADR-0076` (ratified via a new sub-entry); `ADR-0077` (new, PROPOSED - D45
  certification design); `DP-024`/`DP-025` (marked DEFERRED); `DP-026`/`DP-027` (extended with new
  sections); `ADR-0049` (negative-control precedent cited in `ADR-0077`); root `DECISION_LOG.md` D-002/
  D-003 (tolerance/zero-categorical-tolerance principles cited in `ADR-0077`).
- Files changed: `docs/DECISION_LOG.md` (`ADR-0076` ratification sub-entry; new `ADR-0077` entry),
  `docs/decisions/README.md` (`DP-024`/`DP-025` marked DEFERRED), `docs/decisions/DP-026-d008-kp-
  significator-methodology-readiness.md` (new section H, provenance audit; version 1.0.0 -> 1.1.0),
  `docs/decisions/DP-027-parashari-yoga-methodology-readiness.md` (new section H, oracle-availability
  research; version 1.0.0 -> 1.1.0), `docs/ACE_EXECUTION_STATE.md` (version 6.8.0 -> 6.9.0), this file.
  No file under `docs/decisions/DP-024...`/`DP-025...` was edited beyond their own README.md status row -
  both remain exactly as originally drafted, per the owner's own "defer" instruction requiring no further
  work on either.
- Method: direct investigation and genuine numerical verification, no subagent launched. **`ADR-0076`
  ratification:** recorded via the established "ratification of a PROPOSED entry" sub-entry mechanism (mirroring
  `ADR-0068`/`ADR-0074`), since `ADR-0076` was itself already drafted `PROPOSED` awaiting exactly this.
  **`ADR-0027` provenance audit (`DP-026` section H):** re-read `ADR-0027`'s own Decision 4 text and
  counted its semicolon-separated items directly, one by one, rather than trusting this session's own
  prior citations - found sixteen, not eleven, a self-propagated miscount traced back through `DP-023`
  and `DP-021`; re-read `ADR-0027`'s own Evidence line and confirmed it names no external KP-astrology
  source; cross-referenced the checklist's own structural pattern against `ADR-0021` D1 (Mundane
  validation) and `docs/VARGA_CERTIFICATION_ROADMAP.md` section 6 (varga certification requirements) to
  establish it is this project's own repeated internal pattern, not a KP-authority citation. **PyJHora
  yoga oracle research (`DP-027` section H):** located `jhora/horoscope/chart/yoga.py` in the same local
  oracle venv already used for D45 (and for this project's other certifications); counted 233
  individually-defined yoga functions (`grep -c "^def .*_yoga("`); read several docstrings directly,
  finding a consistent "BVR-N" citation pattern; found one docstring spelling it out in full ("BVR-49
  Kalanidhi Yoga (B.V. Raman #49)"), confirming the abbreviation's identity. **D45 certification design
  (`ADR-0077`):** wrote a scratchpad-only (never committed to the repository) Python script implementing
  the D45 rule entirely from the classical description, without importing PyJHora, then imported PyJHora
  separately in the same script to cross-check 36 spot-check points spanning all three sign categories
  and four segment positions each - zero mismatches. Used exact `Fraction` arithmetic (not floats) to
  compute the true mathematical value at each of the 44 internal per-sign segment boundaries and compared
  against the floating-point-computed segment index at each - found a maximum representation error of
  3.553e-15 degrees (1.279e-11 arcsec) and exactly three boundaries (k=13, 26, 29) where the naive
  floating-point floor computation disagrees with the exact-rational one by one segment; then separately
  confirmed both the independent from-scratch derivation AND PyJHora's own implementation agree with EACH
  OTHER at all three of those specific boundary values, establishing this is a boundary-convention
  question (for the project's own existing tolerance-promotion convention), not an oracle-agreement risk.
  Read `certification/VARGA_D12_V1_certification.json`'s own top-level schema directly (again, confirming
  it from `ADR-0076`'s own earlier citation) to ensure `ADR-0077`'s own artifact-structure section is
  accurate.
- Key findings: `ADR-0027`'s checklist has sixteen items, not eleven, and cites no external KP authority -
  its process-structure is this project's own repeated pattern, its domain vocabulary genuine but never
  externally checked; recommended for future independent verification, not ratified this task, per
  explicit instruction. PyJHora already implements 233 classical yogas citing B.V. Raman by name -
  materially better oracle-availability evidence than `DP-027`'s own original assessment, explicitly
  treated as corroboration only, per the owner's own explicit caution, not as authority to adopt. D45's
  cell-width representability question is now genuinely resolved: negligible numerical error, and a real
  but well-understood three-boundary floor-classification effect that the project's own existing
  tolerance convention already knows how to handle - not a blocker, and not silently assumed away either.
- Implementation summary: no engine/scripts/certification code touched; `engine/astrology/varga_d45.py`
  does not exist and was not created. The scratchpad verification script lives outside the repository
  entirely (session scratchpad directory), per instruction not to modify production code or certified
  artifacts.
- Tests executed and results: `python -m pytest -q` - 844/844 passed, unchanged.
- Certification executed and results: none - no certification artifact touched, generated, or
  regenerated; `ADR-0077` is a design, not an executed certification run.
- Governance checks executed and results: `python scripts/check_adr_numbering.py` (77 ADR entries, up
  from 76 - `ADR-0077` added), `python scripts/check_identifier_families.py` (27 DP identifiers,
  unchanged - no new DP registered this task), `python scripts/check_retired_identifiers.py` (0
  violations, clean on the first pass) - all PASS.
- Known issues: none new - the cell-width question, previously open, is now resolved with a concrete
  disposition (existing tolerance convention applies; three named boundary test cases required).
- Unresolved questions: whether to ratify `ADR-0077` (which would authorize D45's own certification-
  execution step - the actual writing and registration of the frozen rule, oracle comparison, and
  artifact generation - as a separate, subsequent act); `DP-026`'s own further disposition (an
  independent KP-source cross-check of `ADR-0027`'s checklist, and whether to ratify `ADR-0027` once that
  is done); `DP-027`'s own further disposition (a fuller audit of PyJHora's 233 yoga definitions, and
  whether to authorize specification-drafting decision-readiness next).
- CEO decision required: this task's own new genuine stopping point, per the owner's explicit closing
  instruction ("Continue until the next genuine CEO decision, methodology/source blocker, or
  certification-design question requiring my decision") - review `ADR-0077` and rule on it, and/or act on
  `DP-026`/`DP-027`'s own further items. No ADR beyond `ADR-0076` is ratified (per explicit instruction);
  no capability is implemented.
- Next authorized action: none self-executable. Awaiting the owner's review of `ADR-0077` and of
  `DP-026`/`DP-027`'s own new findings, and, separately, authorization to push this task's commits if
  desired.

### 2026-08-25 - ADR-0076 (D45 implementation-readiness, PROPOSED) + DP-024/DP-025/DP-026/DP-027 drafted; roadmap staleness corrected
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with this task's own
  files, on top of `759af32`).
- Previous approved commit: `759af32` (the `DP-023` commit, local-only, five commits ahead of
  `origin/phase-g-governance`'s `c4d571a340b4baf873fbefb5661eb195937d2f51`).
- Task (owner's exact instruction, abridged, eight numbered items): "CEO direction — proceed with DP-023
  resolution. Treat D45 (Akshavedamsa) as the recommended first JATAKA capability and prepare the
  necessary ADR/implementation-readiness path, but do not implement D45 yet. Before implementation: 1.
  Resolve the Varga framework step/payload-table architecture question in a narrow decision paper/ADR if
  still genuinely open. 2. Audit the stale VARGA_CERTIFICATION_ROADMAP.md against the accepted ADRs and
  correct its status only through the appropriate append-only governance mechanism. 3. Keep polar-
  Placidus/M-04 completely separate as Tier-0 maintenance; prepare its own decision-readiness only. 4.
  Prepare/authorize separate decision-readiness papers for D-008 KP significators and Parashari yoga
  methodology, but do not implement either. 5. Do not treat the unratified Varga roadmap's ranking as
  normative until its status is resolved. 6. Do not modify production code or certified artifacts yet.
  7. Do not ratify any ADR yourself. 8. Continue until the next genuine CEO decision point." For D45
  specifically, twelve items required verification before drafting its implementation ADR (classical
  source/rule, school/tradition, mathematical formula, sign/segment conventions, boundary behaviour,
  variant handling, authoritative oracle/reference, independent validator design, protected holdout,
  certification artifact structure, explicit non-claims, dependency on the varga framework architecture).
  Explicit instruction: if the step/payload architecture can be resolved from existing accepted
  decisions and repository evidence, resolve it and continue; if it requires an owner choice, stop and
  report the exact choice required.
- Relevant ADR/specification: `ADR-0076` (new, PROPOSED - the D45 audit); `DP-024`/`DP-025`/`DP-026`/
  `DP-027` (new); `docs/VARGA_CERTIFICATION_ROADMAP.md` (corrected, v1.0.0 -> v1.0.1); `ADR-0049` (cited,
  confirms B-01/B-02 remediated); root `DECISION_LOG.md` D-008 and `docs/DECISION_LOG.md` `ADR-0027`
  (both cited in full for `DP-026`); `docs/PARASHARI_DRISHTI_SPEC.md` (cited for `DP-027`).
- Files changed: `docs/DECISION_LOG.md` (new `ADR-0076` entry), `docs/VARGA_CERTIFICATION_ROADMAP.md`
  (staleness correction, append-only), `docs/decisions/DP-024-varga-framework-step-payload-
  architecture.md` (new), `docs/decisions/DP-025-polar-placidus-m04-tier0-maintenance.md` (new), `docs/
  decisions/DP-026-d008-kp-significator-methodology-readiness.md` (new), `docs/decisions/DP-027-
  parashari-yoga-methodology-readiness.md` (new), `docs/decisions/README.md` (registered `DP-024`-
  `DP-027` before drafting, per `ADR-0040`; version 3.9.0 -> 4.0.0), `docs/ACE_EXECUTION_STATE.md`
  (version 6.7.0 -> 6.8.0), this file.
- Method: direct investigation. Confirmed via `grep`/direct reads that no ADR resolves the varga
  framework's own `step`-field or payload/label-table proposals, and via direct inspection of `engine/
  astrology/varga_rules.py` that no `step` field exists on `CyclicVargaRule`; cross-referenced `docs/
  VARGA_CERTIFICATION_ROADMAP.md` section 3's own payload-list (D16/D20/D27/D60 only) to confirm D45 is
  not on it. Read root `DECISION_LOG.md` D-008 and `docs/DECISION_LOG.md` `ADR-0027` in full, then
  searched for any later ratification of `ADR-0027` specifically - none found, confirming it remains
  `Status: PROPOSED`. Searched `docs/OPEN_QUESTIONS.md`/`docs/DECISION_LOG.md`/root `DECISION_LOG.md` for
  "yoga" - no governing decision found for Parashari yoga at all. **A genuine local oracle probe
  performed for D45 specifically:** located an already-installed PyJHora package in a local scratchpad
  venv (`oracle_probe_venv`), confirmed `jhora.horoscope.chart.charts.akshavedamsa_chart` exists (D45's
  own dedicated function, matching the established per-division-named-function pattern already used for
  D2/D3/D7/D12/D30's own certifiers), read its full implementation directly, and independently derived
  that its `chart_method=1` ("Traditional Parasara Method") movable/fixed/dual offset arithmetic
  (`+0`/`+4`/`+8`, using `jhora.const`'s own 0-indexed `movable_signs`/`fixed_signs`/`dual_signs` tuples)
  corresponds exactly to Aries/Leo/Sagittarius - an exact, independent match to `docs/VARGA_
  CERTIFICATION_ROADMAP.md` section 4's own stated construction. Read `certification/
  VARGA_D12_V1_certification.json`'s own top-level schema directly to confirm the certification-artifact
  structure `ADR-0076` describes for D45 is accurate, not assumed.
- Key findings: the varga-framework `step`/payload-table questions are genuinely open but do not block
  D45 (`DP-024`). `docs/VARGA_CERTIFICATION_ROADMAP.md` was stale on its own B-01/B-02 claim - corrected
  inline plus an append-only change-history row; its `Status: PROPOSED` and non-normative ranking status
  both explicitly preserved, per the owner's own instruction not to treat it as ratified. `ADR-0027`, the
  actual source of the "eleven-element checklist" this project has repeatedly cited as authoritative for
  `D-008`/KP significators, is itself still `Status: PROPOSED`, never ratified - a finding not previously
  surfaced in `DP-021` or `DP-023`'s own earlier citations of this material. Parashari yoga has no
  governing decision or checklist of any kind, unlike KP significators - a materially different readiness
  state between the two "high-value but not methodology-ready" candidates `DP-023` had grouped together.
  D45's own twelve readiness items: eleven satisfied, one (cell-width representability, 30/45 = 2/3
  degree) explicitly deferred to the certification gates' own dense-sweep/ULP-battery rather than assumed
  either way, mirroring how the already-solved D7/D9 precedent was itself resolved empirically rather
  than assumed beforehand.
- Implementation summary: no engine/scripts/certification code touched; no production code or certified
  artifact modified, per explicit instruction. Governance-record, decision-paper, and one documentation
  correction only.
- Tests executed and results: `python -m pytest -q` - 844/844 passed, unchanged.
- Certification executed and results: none - no certification artifact touched or regenerated.
- Governance checks executed and results: `python scripts/check_adr_numbering.py` (76 ADR entries, up
  from 75 - `ADR-0076` added), `python scripts/check_identifier_families.py` (27 DP identifiers, up from
  23 - `DP-024` through `DP-027` registered), `python scripts/check_retired_identifiers.py` (0
  violations, clean on the first pass) - all PASS.
- Known issues: D45's own cell-width representability question remains open, deferred to the eventual
  certification gates by design, not resolved this task.
- Unresolved questions: whether to ratify `ADR-0076` (which would authorize D45's own certification work
  to begin as a separate, subsequent act - not itself implementation); `DP-024`'s own step/payload-table
  timing; `DP-025`'s polar-Placidus/M-04 authorization; `DP-026`'s `ADR-0027`-ratification and/or
  `KP_SIGNIFICATOR_V1` specification-drafting authorization; `DP-027`'s oracle-availability-research
  and/or specification-drafting authorization.
- CEO decision required: this task's own new genuine stopping point, per the owner's explicit item 8
  ("Continue until the next genuine CEO decision point") - review `ADR-0076`, `DP-024`, `DP-025`,
  `DP-026`, `DP-027` and rule on any of their items. No ADR is self-ratified (per explicit item 7); no
  capability is implemented (per explicit item 6/8).
- Next authorized action: none self-executable. Awaiting the owner's review of the five new documents,
  and, separately, authorization to push this task's commits if desired.

### 2026-08-25 - DP-023 drafted: exact first-JATAKA-capability selection (D45 recommended), genuine CEO decision point
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with `DP-023`'s own
  file and registration, on top of `728da71`).
- Previous approved commit: `728da71` (the `DP-021` section-N resumption, local-only, four commits ahead
  of `origin/phase-g-governance`'s `c4d571a340b4baf873fbefb5661eb195937d2f51`).
- Task (owner's exact instruction, abridged): "CONTINUE — DP-021 FIRST JATAKA CAPABILITY DECISION. Do
  not stop at the DP-022 ratification. Continue the already-authorized DP-021 investigation until the
  actual first-capability CEO decision point... Evaluate at minimum: each remaining production Varga
  candidate individually, not merely the Varga family; additional Parashari aspect coverage; Vimshottari
  depth extension; Shadbala; polar-Placidus/M-04 maintenance separately; Parashari yoga methodology-
  readiness; KP/D-008 significator methodology-readiness; Jaimini Chara karakas... Score each against
  [ten named axes]... Do not simply repeat 'remaining Vargas' as the recommendation. Determine which
  exact Varga, if Varga remains first, and prove why it should precede the alternatives. Resolve the
  previously open Varga risk-order question from repository evidence. If the repository does not contain
  enough evidence to determine the order, explicitly say so and create a narrower decision-readiness
  paper rather than inventing an order. Likewise, do not treat polar-Placidus/M-04 as automatically part
  of the Varga capability... Methodology-first rule: if the recommended capability lacks a frozen,
  authoritative methodology, stop before implementation and produce the required methodology decision-
  readiness paper. Do not write production code merely because the calculation is technically easy."
  Required deliverable: a registered decision paper with exact candidate inventory, evidence, dependency
  graph, scoring matrix, exact first-capability candidate, alternatives, risks, certification plan,
  methodology/source requirements, explicit non-claims, recommendation and confidence, exact CEO decision
  required. Hard boundary: no implementation of any candidate, no production/certified-artifact
  modification, no polar-Placidus/M-04/KP-significator/Parashari-yoga/Jaimini-BNN-Numerology work begun,
  no reopening FOUNDATION or any closed Dasha item.
- Relevant ADR/specification: `DP-021` (extended, not contradicted - sections A-N unedited), `DP-022`/
  `ADR-0075` (the governance ruling making non-listed candidates eligible), `docs/VARGA_CERTIFICATION_
  ROADMAP.md` (the primary new evidence source this task), `ADR-0049` (B-01/B-02 remediation, used to
  find the roadmap document stale on one point), `specs/PROJECT_CHARTER.md` (Jaimini-scope finding).
- Files changed: `docs/decisions/DP-023-jataka-first-capability-exact-selection.md` (new), `docs/
  decisions/README.md` (registered `DP-023` before drafting, per `ADR-0040`; version 3.8.0 -> 3.9.0),
  `docs/ACE_EXECUTION_STATE.md` (version 6.6.0 -> 6.7.0), this file.
- Method: direct investigation (no subagent launched - the required evidence was concentrated in one
  already-known document, `docs/VARGA_CERTIFICATION_ROADMAP.md`, plus targeted greps/reads against
  `docs/DECISION_LOG.md`, `engine/astrology/varga_registry.py`, `varga_rules.py`, and `specs/
  PROJECT_CHARTER.md`). Read `docs/VARGA_CERTIFICATION_ROADMAP.md` in full (sections 1-9); cross-checked
  its own section 2 claim that B-01/B-02 "must be resolved before the next varga is added" against
  `ADR-0049`'s own text (already read earlier this session) and against live code
  (`register_varga_rule`'s division cross-check, `rule_content_sha256`) - confirmed the roadmap document
  is stale on this specific point (B-01/B-02 resolved 2026-08-17, roadmap never updated since
  2026-08-11); confirmed no `step` field exists on `CyclicVargaRule` and no ADR resolves the section-3
  payload/label-table proposal; grepped `engine/**/*.py` for "yoga" (only the panchanga anga and
  provenance non-claims found, zero combination-yoga code, consistent with `DP-021`'s own earlier
  finding); re-read `specs/PROJECT_CHARTER.md`'s "Analytical systems" section specifically checking for
  Jaimini - confirmed absent, a finding not made in `DP-021`'s own original three-agent investigation.
- Key findings: applying the owner's own methodology-first rule as an explicit filter to `docs/
  VARGA_CERTIFICATION_ROADMAP.md` section 4's own confidence table excludes D20 and D60 (both flagged
  "Medium... genuinely disputed" content confidence - D20's start triple, D60's even-sign reversal) and,
  cross-referencing section 3's separately-stated payload/label-table gap list, also excludes D16 and D27
  (need an undecided architecture decision - kalamsa/vimsamsa deities, nakshatra lord - before being a
  legitimate analytical input) and D4 (needs an undecided Segment-vs-`step` contract choice) - leaving
  D24, D40, and D45 as the only three of the eight remaining vargas with no disputed content and no
  undecided architecture prerequisite. Of these three, the roadmap's own section 5 risk order places D45
  in its second tier (grouped with D16 in the roadmap's own text, but D16 is excluded here on the payload
  ground) while D24/D40 sit in the third tier - **making D45 (Akshavedamsa) the highest-ranked cleanly-
  ready varga**, an inference this paper's own section E discloses as bridging two separate sections of
  an unratified document, not a verbatim citation of an already-stated conclusion. Every non-varga
  JATAKA-scope candidate investigated (aspect coverage, Shadbala, Parashari yoga, KP significators) fails
  the methodology-first rule outright; Vimshottari depth extension passes as cleanly as D45 but scores
  lower on architectural leverage/product value and reopens a just-closed area. Polar-Placidus/M-04 was
  scored separately, on its own terms, per explicit instruction - not folded into the varga pick.
- Implementation summary: no engine/scripts/certification code touched. Decision paper only.
- Tests executed and results: `python -m pytest -q` - 844/844 passed, unchanged (105.87s).
- Certification executed and results: none - no certification artifact touched or regenerated.
- Governance checks executed and results: `python scripts/check_adr_numbering.py` (75 ADR entries,
  unchanged), `python scripts/check_identifier_families.py` (23 DP identifiers, up from 22 - `DP-023`
  registered), `python scripts/check_retired_identifiers.py` (0 violations, clean on the first pass) -
  all PASS.
- Known issues: D45's own cell width (30/45 = 2/3 degree, not exactly binary-representable) is flagged as
  an unresolved technical question the roadmap's own section 4 table does not address for D45 the way it
  explicitly does for D27 - disclosed, not resolved, in section E; the eventual certification work should
  verify it.
- Unresolved questions: all six items in `DP-023` section L - the first-capability selection itself; the
  varga-framework `step`-field/payload-table timing; whether polar-Placidus/M-04 closure gets its own
  JATAKA-labelled ADR or proceeds as Tier-0 maintenance; whether to authorize a `D-008` methodology paper;
  whether a comparable Parashari-yoga paper should also be authorized; whether `docs/VARGA_CERTIFICATION_
  ROADMAP.md` itself should be formally ratified.
- CEO decision required: this task's own genuine stopping point, per the owner's explicit instruction -
  review `DP-023` and act on any or all of its six items (section L). No capability is selected, no ADR
  is drafted, and no implementation is authorized by this task.
- Next authorized action: none self-executable. Awaiting the owner's review of `DP-023`, and, separately,
  authorization to push this task's commits (this one plus the three preceding it) if desired.

### 2026-08-25 - DP-021 resumed (section N): first-JATAKA-capability recommendation reached, genuine CEO decision point
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with `DP-021`'s new
  section N, on top of `fe6ae02`).
- Previous approved commit: `fe6ae02` (the `ADR-0075` ratification commit, local-only, three commits
  ahead of `origin/phase-g-governance`'s `c4d571a340b4baf873fbefb5661eb195937d2f51`).
- Task (owner's exact instruction, continuing directly from the same "CEO DECISION — DP-022" message):
  "After ratification, continue automatically into the next decision-readiness task: resume DP-021 and
  determine the strongest candidate for the first JATAKA capability. Do not implement that capability.
  The next stopping point must be the genuine CEO decision point where you present: candidate
  capabilities, dependencies, methodology readiness, certification difficulty, architectural leverage,
  risk, recommended first capability, alternatives, exact CEO decision required. Do not stop merely
  because the DP-022 ratification commit is complete. Continue until that next genuine CEO decision
  point, blocker, or separate push-authorization checkpoint."
- Relevant ADR/specification: `DP-021` (resumed, section N added, sections A-M unedited); `ADR-0075`
  (the governance ruling that made all candidates, not just the four literally named in `Q8_CLOSURE_
  MATRIX.md` s5, eligible for consideration); `D-008` (cited as the correct next step for the
  KP-significator track, not implemented).
- Files changed: `docs/decisions/DP-021-jataka-first-capability-decision-readiness.md` (new section N;
  version 1.0.0 -> 1.1.0), `docs/ACE_EXECUTION_STATE.md` (version 6.5.0 -> 6.6.0), this file.
- Method: direct synthesis of evidence already gathered in `DP-021` sections A-M (no new research agents
  launched - the original three-agent investigation's evidence remained current), plus one targeted,
  read-only code verification this task performed directly: re-checked the M-04 finding (`DrishtiChart`
  provenance mislabeling), which `DP-021` section H.4 had flagged as "apparently still open, not
  confirmed," against live source. Confirmed still live: `engine/models/drishti.py`'s own docstring
  states `aspected_houses` "counts whole-sign houses from the lagna"; `engine/parashari/
  drishti.py::graha_drishti_from_snapshot()` (line 84) computes `aspected_houses` via pure whole-sign
  counting from the ascendant sign with no Placidus reference, while reusing `snapshot.provenance`
  unmodified (line 63); the certified `PARASHARI_LAHIRI` profile hardcodes `house_system=b"P"`. No file
  under `engine/` was modified - read-only verification only.
- Key findings: scored all candidates (remaining vargas, Vimshottari depth extension, aspect-coverage
  extension, karakas in all three senses, bhava/house-cusp gap-closure, Parashari yogas, KP significators,
  planet strength) against the owner's six required axes in a comparison table (`DP-021` section N.2).
  **Remaining production vargas** is the only candidate simultaneously methodology-ready (classical
  formulas fixed and uncontested per division), low-certification-difficulty (five-times-proven template),
  and low-risk - recommended as the first JATAKA capability at medium-high confidence, with the caveat
  that no varga "risk order" is defined anywhere in this repository, so a short follow-up sub-decision
  (which division first) would still be needed. **Polar-Placidus + M-04 closure** is recommended in
  parallel, explicitly framed as Tier-0/FOUNDATION-tier certification-completion work rather than a new
  JATAKA capability in its own right (it lives inside the already-locked Tier-0 kernel certification, not
  a JATAKA-scope artifact), since it is narrow, `RISE_SET_V1`-precedented, and the one concretely
  evidenced prerequisite for KP significators specifically. **Parashari yogas and KP significators are
  the highest product-value candidates found, and both are genuinely not implementable yet** - neither is
  missing calculation infrastructure (both build on already-certified sign/house/aspect/varga data); both
  are missing a frozen, source-cited, owner-ratified methodology specification. Recommends authorizing a
  dedicated `D-008` KP-significator methodology-specification decision-readiness paper (now confirmed
  scope-eligible under `ADR-0075`, removing the doubt `DP-021`'s original section H.1 raised) as the
  correct next step for that track - not implementation of either capability.
- Implementation summary: no engine/scripts/certification code touched (the M-04 check was read-only).
  Decision-paper resumption only.
- Tests executed and results: `python -m pytest -q` - 844/844 passed, unchanged.
- Certification executed and results: none - no certification artifact touched or regenerated.
- Governance checks executed and results: `python scripts/check_adr_numbering.py` (75 ADR entries,
  unchanged), `python scripts/check_identifier_families.py` (22 DP identifiers, unchanged),
  `python scripts/check_retired_identifiers.py` (0 violations, clean on the first pass this time) - all
  PASS.
- Known issues: none new. The M-04 finding is now confirmed live (not merely flagged) but was not fixed
  this task - fixing it would be implementation, outside this task's own decision-readiness scope.
- Unresolved questions: all five items in `DP-021` section N.5 - the first-capability selection itself;
  the varga risk-order follow-up if vargas is chosen; whether polar-Placidus/M-04 closure should carry
  its own JATAKA-labelled ADR or proceed as ordinary Tier-0 maintenance; whether to authorize a `D-008`
  methodology-specification paper; whether a comparable Parashari-yoga methodology paper should also be
  authorized.
- CEO decision required: this task's own genuine stopping point, per the owner's explicit instruction -
  review `DP-021` section N and act on any or all of its five items (N.5). No capability is selected, no
  ADR is drafted, and no implementation is authorized by this task.
- Next authorized action: none self-executable. Awaiting the owner's review of `DP-021` section N, and,
  separately, authorization to push this task's commits (this one plus the preceding `ADR-0075`
  ratification commit) if desired.

### 2026-08-25 - ADR-0075 RATIFIED: DP-022's ILLUSTRATIVE interpretation adopted; Q8 unedited
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the `ADR-0075`
  entry and `DP-022` README-index update, on top of `ba5dbab`).
- Previous approved commit: `ba5dbab1aba88ea69d6cea4354c13bcbd4a49684` (the `DP-022` commit, local-only,
  two commits ahead of `origin/phase-g-governance`'s `c4d571a340b4baf873fbefb5661eb195937d2f51`).
- Task (owner's exact instruction, abridged): "CEO DECISION — DP-022. I ratify DP-022's ILLUSTRATIVE
  interpretation. Record the following as the owner's decision: 1. Q8_CLOSURE_MATRIX.md s5's
  Implementation Scope list is ILLUSTRATIVE, not exhaustive. 2. A JATAKA capability not named in that
  list may be proposed through its own decision-readiness -> ADR -> owner-ratification pathway without
  first amending Q8 merely because it is absent from s5. 3. This interpretation does not itself
  authorize implementation of any unlisted capability. 4. Every capability remains subject to its own
  methodology specification, dependency analysis, system isolation, certification requirements, ADR and
  explicit owner authorization. 5. s15's separate phase/capability authorization principle remains fully
  in force. 6. Q8 should only be amended when a future decision actually requires changing an explicit
  Q8 requirement or architectural boundary. 7. DP-021 should now be resumed for capability selection. 8.
  Do not implement any capability as part of this ratification. 9. Do not reopen Foundation, H-03,
  H10/H11, or any closed Dasha item." Required work: record via the established ADR/decision mechanism;
  draft/update the appropriate ADR; preserve DP-022's original text; update state/handoff append-only;
  run governance and full regression tests; do not push/merge without separate authorization. Then
  continue automatically into resuming DP-021 for first-capability decision-readiness, stopping only at
  the next genuine CEO decision point (candidates, dependencies, methodology readiness, certification
  difficulty, architectural leverage, risk, recommendation, alternatives, exact CEO decision required) -
  not merely because the ratification commit is complete.
- Relevant ADR/specification: `ADR-0075` (new, this entry); `DP-022` (ratified, text preserved);
  `Q8_CLOSURE_MATRIX.md` s5/s15 (unedited); `ADR-0048`, `ADR-0021` D3, `ADR-0063`, `ADR-0067` (the
  precedent basis cited in `ADR-0075`'s own Evidence section).
- Files changed: `docs/DECISION_LOG.md` (new `ADR-0075` entry, appended after `ADR-0074`'s ratification
  sub-entry, ascending order preserved), `docs/decisions/DP-022-jataka-q8-implementation-scope-
  governance.md` (three mechanical placeholder-identifier corrections only - see below), `docs/decisions/
  README.md` (`DP-022` row marked ADDRESSED by `ADR-0075`; version 3.7.0 -> 3.8.0), `docs/
  ACE_EXECUTION_STATE.md` (version 6.4.0 -> 6.5.0), this file.
- Mechanism used: a new, top-level numbered ADR (`ADR-0075`), not the "ratification of a `PROPOSED`
  entry" sub-entry mechanism used for `ADR-0068`/`ADR-0074` (that mechanism applies when the original
  document was itself drafted as a `PROPOSED` ADR awaiting a status-only ratification edit; `DP-022` was
  a decision paper, never itself an ADR, so the correct precedent is `ADR-0067`'s own treatment of
  `DP-015` - a fresh ADR number that records the ratification and quotes the owner's decision in full).
  All nine of the owner's numbered points recorded verbatim as `ADR-0075`'s own Decision section, none
  reinterpreted, narrowed, or extended.
- **A governance-hook finding, disclosed and corrected in-session:** the repository's own
  `PostToolUse:Edit` governance hook (`scripts/check_retired_identifiers.py`, Pattern B) flagged, on
  editing `docs/DECISION_LOG.md`, three pre-existing violations in `DP-022`'s own already-committed text
  (two compound words, each combining a bare "ADR-" prefix with an ordinary English word, matching the
  bare-`ADR-`-prefix pattern the hook exists to catch) that had not been caught when `DP-022` was first
  written via the `Write` tool in the prior task (the hook appears to trigger on `Edit` calls, not
  `Write`). Corrected mechanically - reworded to avoid the bare prefix entirely - with **no change to the
  paper's own analysis, arguments, evidence, or conclusions**, matching this session's own established
  `DP-018` precedent for exactly this class of correction. A fourth occurrence surfaced in `docs/
  decisions/README.md`'s own new `DP-022` index row (quoting the flagged phrases) and was corrected the
  same way before governance gates passed clean.
- Implementation summary: no engine/scripts/certification code touched. Governance-record and
  decision-paper-index changes only.
- Tests executed and results: `python -m pytest -q` - 844/844 passed, unchanged.
- Certification executed and results: none - no certification artifact touched or regenerated.
- Governance checks executed and results: `python scripts/check_adr_numbering.py` (75 ADR entries, up
  from 74 - `ADR-0075` added), `python scripts/check_identifier_families.py` (22 DP identifiers,
  unchanged), `python scripts/check_retired_identifiers.py` (0 violations, after the three-plus-one
  mechanical corrections above) - all PASS.
- Known issues: none new.
- Unresolved questions: none for this specific ratification - all nine of the owner's points were
  recorded without ambiguity. The broader question of which JATAKA capability to select is the subject
  of the immediately following, resumed `DP-021` task (see next entry).
- CEO decision required: none for this ratification - fully executed per explicit, unambiguous
  instruction. Per the owner's own explicit "continue automatically" instruction, this task does not stop
  here; it proceeds directly into resuming `DP-021`.
- Next authorized action: continue directly into resuming `DP-021`'s own capability-selection question,
  per explicit instruction - see the immediately following task-log entry.

### 2026-08-25 - DP-022 drafted: JATAKA/Q8 implementation-scope governance question (EXHAUSTIVE vs. ILLUSTRATIVE, decides nothing)
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the `DP-022` file
  and registration, on top of `06ff564`).
- Previous approved commit: `06ff564ba1628e8f694e58d07cce1f60c7de6d12` (the `DP-021` commit, local-only,
  one commit ahead of `origin/phase-g-governance`'s `c4d571a340b4baf873fbefb5661eb195937d2f51`).
  `origin/main` unchanged at `d738520ffc796d07468e24a5b1dddcfba3120c65` (PR #4 merge).
- Task (owner's exact instruction, abridged): "CEO AUTHORIZATION — RESOLVE JATAKA/Q8
  IMPLEMENTATION-SCOPE GOVERNANCE QUESTION. Begin the next decision-readiness task arising from DP-021.
  Do not implement any capability. Do not modify production code. Do not select or ratify a JATAKA
  capability. Investigate only whether Q8_CLOSURE_MATRIX.md s5's 'Implementation scope' list is: 1.
  EXHAUSTIVE... or 2. ILLUSTRATIVE..." Required method: session-start audit; independent inspection of
  Q8 s5/s15, `PROJECT_CHARTER`, governance standards, phase-entry/implementation-authorization ADRs, and
  any prior example of work outside an initial roadmap list being subsequently authorized; trace
  governance precedent across FOUNDATION exit, H-01/H-02, the Dasha roadmap, `ADR-0074`, `DP-021` itself;
  specifically investigate whether an ADR can authorize a new JATAKA capability outside s5 without first
  amending Q8; explicit instruction not to treat technical sensibility as governance authorization and
  not to treat Claude Web's recommendation as authority (not applicable to this paper directly - no
  external input was cited). Required output: a new `DP-0XX`, registered before drafting under
  `ADR-0040`, containing exact governing text, evidence for each interpretation, arguments for
  EXHAUSTIVE, arguments for ILLUSTRATIVE, precedent analysis, consequences of each, interaction with s15,
  interaction with `ADR-0074`, whether a Q8 amendment is required, whether an ADR alone is sufficient,
  recommendation with confidence, explicit non-claims, exact CEO decision required. Hard scope boundary:
  no implementation of any named capability, no H-03/H10-H11/FOUNDATION/closed-Dasha-item modification,
  no self-amendment of Q8, no self-ratification. Run the full relevant governance/regression tests; code
  and certified values must remain untouched. Update canonical state/handoff records append-only. Stop
  only at the genuine CEO decision point.
- Relevant ADR/specification: none reopened or created. Cites `ADR-0048` (Q8 ratification), `ADR-0021`
  D2/D3, `ADR-0067`/`DP-015` (the closest analogous-ambiguity precedent), `ADR-0074`, `ADR-0063`,
  `specs/PROJECT_CHARTER.md`, `docs/PROJECT_CONSTITUTION.md`, `.claude/rules/governance.md` - all
  read-only citations, none edited.
- Files changed: `docs/decisions/DP-022-jataka-q8-implementation-scope-governance.md` (new),
  `docs/decisions/README.md` (registered `DP-022` before drafting, per `ADR-0040`; version 3.6.0 ->
  3.7.0), `docs/ACE_EXECUTION_STATE.md` (version 6.3.0 -> 6.4.0), this file.
- Method: direct investigation (not delegated to a subagent, given the narrower, textual/precedent-
  analysis nature of this task compared to `DP-021`'s broad capability inventory) - read
  `Q8_CLOSURE_MATRIX.md` in full; grepped `docs/DECISION_LOG.md` for `ADR-0048`, `ADR-0021`, `ADR-0067`,
  `ADR-0074` and read each in full; grepped `specs/PROJECT_CHARTER.md` for its "Analytical systems"
  text; grepped `docs/PROJECT_CONSTITUTION.md` and `docs/DOCUMENTATION_STANDARD.md` for "amend"/
  "amendment" (no defined procedure found in either); confirmed `Q8_CLOSURE_MATRIX.md`'s own two-version
  change history has never touched sections 3-14.
- Key findings: `Q8_CLOSURE_MATRIX.md` s5's "Each is a separate ADR and none is implied by phase entry"
  sentence's grammatical antecedent is the four named items - it governs *how* they get authorized, and
  is silent on whether unlisted items are eligible at all. FOUNDATION's own exit criterion ("every
  capability above... production certified") textually ties phase exit to its own implementation-scope
  list, supporting EXHAUSTIVE by structural analogy. `specs/PROJECT_CHARTER.md`'s own "additional systems
  require their own specification and isolation rules" (senior in the `ADR-0042` hierarchy) and `ADR-0021`
  D3's entity-vocabulary "provisional and extensible... a new entity kind requires an explicit
  architectural decision" (the closest structural precedent found, though never yet exercised and at a
  different governance layer) both support ILLUSTRATIVE. **No ADR has ever amended `Q8_CLOSURE_MATRIX.md`
  sections 3-14**, and every capability actually pursued during FOUNDATION and the Dasha roadmap was
  already named in its phase's own ratified text before being pursued - meaning there is no true
  precedent, in either direction, of a phase-scope row being extended to cover something not originally
  named. The one directly relevant, on-point precedent is `DP-015`/`ADR-0067`: it resolved an analogous
  "does this Q8 phrase's reach extend beyond its literal named scope" ambiguity **narrowly, per-item**,
  via a fresh addendum ADR layered on top of Q8 (never rewriting Q8's own text), and explicitly declined
  to generalize that resolution to other items ("It is not silently generalized to any other FOUNDATION
  item"). `ADR-0074` and s15 were both checked directly and found silent on this specific question -
  neither supports nor forecloses either reading.
- Implementation summary: no engine/scripts/certification code touched. Decision paper only.
- Tests executed and results: `python -m pytest -q` - 844/844 passed, unchanged, confirming the
  documentation-only change made no regression.
- Certification executed and results: none - no certification artifact touched or regenerated.
- Governance checks executed and results: `python scripts/check_adr_numbering.py` (74 ADR entries,
  unchanged), `python scripts/check_identifier_families.py` (22 DP identifiers, up from 21 - `DP-022`
  registered), `python scripts/check_retired_identifiers.py` (0 violations) - all PASS.
- Known issues: none new.
- Unresolved questions: all of `DP-022` section M - principally the EXHAUSTIVE-vs-ILLUSTRATIVE ruling
  itself; if EXHAUSTIVE, how a Q8 amendment should be enacted (no formal procedure currently exists); if
  ILLUSTRATIVE, whether the ruling applies generally or should be resolved narrowly per candidate
  capability, matching the `ADR-0067` precedent's own stated preference; whether to resume `DP-021`'s own
  capability-selection question now or wait for this paper's ratification first.
- CEO decision required: rule on `DP-022`'s exhaustive-vs-illustrative question (or defer it per-
  capability, per the `ADR-0067` precedent); this task deliberately stops at the decision point, per the
  owner's own explicit instruction - no interpretation is adopted, no ADR is drafted, no capability is
  selected or implementation-authorized.
- Next authorized action: none self-executable. Awaiting CEO ruling on `DP-022`, resumption of `DP-021`'s
  capability-selection work once that ruling is made, and a push authorization for this task's own
  commit.

### 2026-08-24 - DP-021 drafted: JATAKA first-capability decision-readiness (options only, no ADR, no implementation)
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the `DP-021` file
  and registration, on top of `c4d571a` post-merge).
- Previous approved commit: `c4d571a340b4baf873fbefb5661eb195937d2f51`, merged into `main` this session
  via PR #4 (merge commit `d738520ffc796d07468e24a5b1dddcfba3120c65`, both PR CI run `32758690945` and
  `main`'s own post-merge CI run `32759008459` green).
- Task (owner's exact instruction, abridged): "CEO AUTHORIZATION — BEGIN JATAKA ARCHITECTURE /
  CAPABILITY DECISION-READINESS INVESTIGATION... You are authorized to BEGIN THE JATAKA ARCHITECTURE /
  CAPABILITY DECISION-READINESS INVESTIGATION. You are NOT authorized to implement a Jataka capability
  yet." Supplied an "IMPORTANT INDEPENDENT INPUT" from a separate Claude Web audit (six claims about
  bhava/house-cusp methodology, karakas, Parashari yogas, KP significators), explicitly framed as **not
  predecided** and requiring testing against the repository. Required twelve investigation sections
  (capability inventory; dependency graph; deep bhava/house-cusp investigation naming the "previously
  identified polar-Placidus question"; candidate first capabilities A-E; system separation; certification
  design; variant handling; JATAKA phase boundaries; sequencing; governance/DP registration; explicit
  no-implementation constraints; a formal decision paper, sections A-M). Explicit stop condition: "Stop
  at the genuine CEO decision point. Do not implement anything. Do not ratify your own recommendation.
  Do not push anything without explicit push authorization. Do not merge anything."
- Relevant ADR/specification: none reopened or created. Cites `ADR-0074` (JATAKA entry),
  `Q8_CLOSURE_MATRIX.md` s5 (implementation scope), `docs/DECISION_LOG.md` D-008 (KP significator
  methodology-freeze requirement), `docs/KP_CHAIN_SPEC.md`, `specs/PROJECT_CHARTER.md`, `docs/
  PROJECT_ROADMAP.md` s1/s3, `docs/NEW_VARGA_IMPLEMENTATION_TEMPLATE.md`, `docs/
  DASHA_CERTIFICATION_ROADMAP.md` - all read-only citations, none edited.
- Files changed: `docs/decisions/DP-021-jataka-first-capability-decision-readiness.md` (new, sections
  A-M as specified), `docs/decisions/README.md` (registered `DP-021` before drafting, per `ADR-0040`;
  version 3.5.0 -> 3.6.0), `docs/ACE_EXECUTION_STATE.md` (version 6.1.0 -> 6.3.0), this file.
- Method: three parallel, read-only Explore-agent research passes (isolated worktrees, no risk to the
  working tree) - (1) full capability inventory across ~20 named areas, cross-checked against every
  `certification/*.json` artifact's own `"result"` field and live source, not documentation inference;
  (2) a dedicated 15-part deep investigation of house-cusp/bhava methodology; (3) a survey of every
  JATAKA-relevant governing specification document and its own Status header. Synthesis, evidence
  weighing, and paper authorship performed directly, not delegated.
- Key findings: whole-sign D1 house assignment (Parashari) and Placidus cusp geometry with a full
  SL/NL/SB/SS lordship chain (KP) are **both already certified** at different scopes - the genuine
  remaining house-cusp gap is narrow: Placidus certification stops at 64.1 degrees N/S, polar behaviour
  is explicitly undefined and unverified (documented consistently across 7+ repository files), and
  `RISE_SET_V1`'s own certified `NO_RISE`/`NO_SET` structured-status pattern is a directly applicable,
  unused precedent for handling it. Parashari yoga/rule evaluation and KP significators are both
  genuinely absent (zero code); their real blocker in both cases is a **missing ratified methodology
  specification** (for KP significators, `D-008`'s own eleven-element checklist, not yet started), not
  missing calculation infrastructure, which is largely already built and certified. "Karakas" names three
  unrelated concepts with zero shared code. Corrected one stale secondary source
  (`certification/ENGINE_CAPABILITY_INVENTORY.json`, dated 2026-08-11) that still cited closed finding
  H-04 as open. Tested the independent Claude Web audit's six claims individually against this evidence:
  one confirmed strongly (KP significators genuinely need the polar-Placidus question resolved, per
  `D-008`'s own "cusp handling" requirement), several found overstated or mis-scoped (Parashari yogas do
  not actually depend on cusp geometry at all; "build bhava" overstates what remains, since most of it is
  already certified). **Headline finding not present in the independent input:** `Q8_CLOSURE_MATRIX.md`
  s5's own "Implementation scope" row names exactly four items (remaining vargas, Vimshottari depth/
  convention extensions, aspect coverage, planet strength) - none of bhava, karakas, Parashari yogas, or
  KP significators appears in that list, making it an open, load-bearing governance question (section H.1/
  M.1 of the paper) whether that list is exhaustive or illustrative, prior to any capability choice.
- Implementation summary: no engine/scripts/certification code touched. Decision paper only.
- Tests executed and results: none run - no code changed; prior 844/844 pytest baseline unaffected.
- Certification executed and results: none - no certification artifact touched or regenerated.
- Governance checks executed and results: `python scripts/check_adr_numbering.py` (74 ADR entries,
  unchanged), `python scripts/check_identifier_families.py` (21 DP identifiers, up from 20 - `DP-021`
  registered), `python scripts/check_retired_identifiers.py` (0 violations) - all PASS.
- Known issues: the M-04 finding (`DrishtiChart` provenance mislabels its own house-convention field)
  was found apparently still present during the bhava investigation; whether a since-closed decision
  supersedes it was not conclusively established and is flagged in the paper (section H.4) as requiring
  independent verification, not resolved here.
- Unresolved questions: all of section M in `DP-021` - principally whether `Q8_CLOSURE_MATRIX.md` s5's
  implementation-scope list is exhaustive or illustrative; which of the four presented options to pursue;
  varga risk order if a varga is chosen; whether polar-Placidus closure is FOUNDATION-tier maintenance or
  a JATAKA-scoped decision; whether to authorize follow-up dedicated papers for `D-008` (KP significators)
  and/or a Parashari yoga-rule specification.
- CEO decision required: review `DP-021`; resolve the governing-scope question; select an option (or
  request a narrower follow-up paper); this task deliberately stops at "DECISION PAPER READY," per the
  owner's own explicit stop condition - no option is chosen, no ADR is drafted, no capability is
  implementation-authorized.
- Next authorized action: none self-executable. Awaiting CEO review of `DP-021` and a push authorization
  for this task's own commit.

### 2026-08-24 - phase-g-governance MERGED into main (PR #4): JATAKA-entry state now on main
- Branch / commit SHA: `main` after merge = `d738520ffc796d07468e24a5b1dddcfba3120c65` (parents
  `0e1ef115a647b8a44bf4d1a7af2a3cf3a8b96e03` + `c4d571a340b4baf873fbefb5661eb195937d2f51`).
- Previous approved commit: `c4d571a340b4baf873fbefb5661eb195937d2f51` on `phase-g-governance`
  (the CI-discrepancy-resolution + merge-readiness-audit commit, local-only at authorization time).
- Task (owner's exact instruction, abridged): "CEO AUTHORIZATION — MERGE JATAKA-ENTRY STATE TO MAIN. I
  authorize the merge of the current phase-g-governance state into main." Named source HEAD `931b6d0`;
  required: merge via normal PR/standard process, no squash/rebase/force-push, no unrelated file changes,
  no JATAKA capability implementation, no H-03/cross-certifier-finding/FOUNDATION/closed-Dasha-item work
  in the same task; full post-merge verification and reporting; explicit instruction not to start JATAKA
  architecture work in the same task.
- Discrepancy flagged before acting: local HEAD was actually `c4d571a` (one commit ahead of the named
  `931b6d0`), containing exactly the CI-discrepancy-resolution work the owner's own stated preconditions
  and output requirement #11 presupposed as already present - pushed `c4d571a` to `phase-g-governance`
  first (verified CI green, run `32758370489`) before opening the PR, with the reasoning disclosed to the
  user prior to acting.
- Relevant ADR/specification: `ADR-0074` (the state being merged), `Q8_CLOSURE_MATRIX.md` s5 - neither
  reopened or edited by this task.
- Files changed: none beyond the merge commit itself (a standard two-parent git merge, no file edits by
  Claude in this task).
- Execution: `gh pr create --base main --head phase-g-governance` (PR #4); waited for its own CI run
  (`32758690945`, all four jobs green, read from the log); `gh pr merge 4 --merge` (standard merge commit,
  not squash, not rebase, no force-push) - resulting `main` SHA `d738520`.
- Post-merge verification, each performed directly, not assumed: `main`'s own CI run `32759008459` - all
  four jobs green (844 passed both interpreters, 0 lord mismatches, drift PASS, 74 ADR entries, 20 DP
  identifiers at merge time); `git show origin/main:docs/DECISION_LOG.md` confirms `ADR-0074` `Status:
  ACCEPTED`; `git show origin/main:docs/ACE_EXECUTION_STATE.md` confirms `CURRENT_PHASE: JATAKA ENTERED`;
  `grep -rn "JATAKA\|jataka" engine/ scripts/` on `main` excluding test files - zero hits, no JATAKA
  production code; engine/scripts/certification content otherwise unchanged.
- Tests executed and results: 844/844 pytest, confirmed via `main`'s own CI run `32759008459`.
- Certification executed and results: oracle gate 0 lord mismatches, drift PASS on all relevant jobs -
  confirmed via `main`'s own CI run.
- Governance checks executed and results: 74 ADR entries, 20 DP identifiers - confirmed via `main`'s own
  CI run.
- Known issues: none new.
- Unresolved questions: which JATAKA capability, if any, to authorize next (deferred to the subsequent
  `DP-021` task, see entry above).
- CEO decision required: none for the merge itself - fully executed per explicit authorization. JATAKA
  capability selection remained open, addressed by the immediately following `DP-021` task.
- Next authorized action: per the owner's own explicit instruction, JATAKA architecture work was not
  begun in this same task - it followed as a separate, subsequent, explicitly-authorized task (`DP-021`,
  see entry above).

### 2026-08-24 - JATAKA phase pre-flight: CI-run-ID discrepancy resolved (no fabrication); main-vs-phase-g-governance merge-readiness audit (READY, not performed)
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the
  reconciliation record, on top of `931b6d0`).
- Previous approved commit: `931b6d09bf331773781ec357a305c412d4c0da04` (`ADR-0074` ratification record)
  - pushed and CI-confirmed this session (run `32756205364`). `main` (`0e1ef115a647b8a44bf4d1a7af2a3cf3a8b96e03`,
  via PR #3) is unaffected by this task.
- Task (owner's exact instruction): "JATAKA PHASE PRE-FLIGHT — EVIDENCE RECONCILIATION + MAINLINE
  SYNCHRONIZATION. Do NOT begin Jataka architecture or implementation yet. An independent Claude Web
  audit... identified two items." **Task 1** - resolve a CI-run-ID discrepancy: the session's own report
  cited run `32756205364`, canonical repository records repeatedly cited `32752248185`, and `32756205364`
  "does not appear in the repository." Required: query GitHub Actions directly; inspect both runs (exist?
  headSha? branch? conclusion? jobs? test counts? oracle result? drift result?); determine which
  corresponds to `931b6d0`; do not assume either is correct; do not silently rewrite historical records;
  if `32756205364` was an erroneous reference, document the discrepancy and correct the canonical record
  via the established append-only mechanism; if the runs genuinely conflict, stop and report rather than
  decide unilaterally; preserve the evidence of what actually happened. **Task 2** - after Task 1, a
  merge-readiness audit of `origin/main` vs `origin/phase-g-governance`: current SHAs; commits/files that
  would merge; whether `main` has independent work; conflicts; whether the source branch is CI-green;
  unapproved work; accidental JATAKA production implementation; whether the merge would preserve the
  accepted JATAKA-entry state - explicitly NOT a merge, NOT a push to `main`, NOT a self-authorization to
  merge, NOT JATAKA implementation or architecture work; the purpose is to prepare a CEO merge decision.
  **Task 3** - verify working tree, local HEAD, both remote SHAs, `ADR-0074` status, `CURRENT_PHASE`, all
  six Dasha ADRs, current CI evidence, absence of JATAKA production code; do not modify closed Dasha/
  FOUNDATION decisions, H-03, or the eight `H10`/`H11` cross-certifier findings. Required output: exact
  discrepancy resolution; correct CI run(s); any required append-only correction; exact main-vs-phase-g
  state; merge-readiness result (READY/NOT READY); existing merge commit/PR info if any; remaining
  blockers; explicit statement that no merge was performed. Stop; no JATAKA architecture until separate
  merge authorization.
- Relevant ADR/specification: none reopened - this task is a verification/reconciliation task, not a
  decision. `ADR-0074` (its own `32752248185` citation checked and left unaltered, confirmed accurate for
  when it was drafted); `ADR-0053`, `ADR-0069` through `ADR-0073` (all six Dasha-roadmap ADRs, re-verified
  `ACCEPTED`, not reopened).
- Files changed: `docs/ACE_EXECUTION_STATE.md` (version 6.1.0 - `LAST_COMMIT`/`LAST_CI_RUN` snapshot
  fields corrected via the file's own designed overwrite mechanism, plus an append-only Change History
  row explaining the correction; merge-readiness findings recorded), this file.
- **Task 1 findings, verified directly against GitHub Actions, not assumed:** `gh run view 32752248185
  --json databaseId,headSha,headBranch,conclusion,status,event,createdAt,jobs` - exists, `conclusion:
  success`, `headSha: f0eb220d4b5e05a8f8fcf7798810f6f195981a29`, `headBranch: phase-g-governance`,
  `event: push`, `createdAt: 2026-08-24T16:41:07Z`, all four jobs `success`. `gh run view 32756205364`
  (same fields) - exists, `conclusion: success`, `headSha: 931b6d09bf331773781ec357a305c412d4c0da04`
  (current HEAD), `headBranch: phase-g-governance`, `event: push`, `createdAt: 2026-08-24T17:22:01Z`
  (later than the other run), all four jobs `success`. Both runs' logs independently re-inspected for
  test counts/oracle/drift: `32752248185` - `844 passed` (both interpreter legs, both the default and
  network-guard re-run), `lord mismatches: 0`, `PASS: 46 evidence file(s) identical...` (both no-oracle
  legs and the oracle gate); `32756205364` - identical shape (`844 passed`, `lord mismatches: 0`, drift
  PASS), as expected since the intervening commit touched only documentation. **Neither run is
  erroneous or fabricated; there is no evidentiary conflict between them** - they are two genuine,
  correctly-conclusive CI runs for two different, sequential commits on the same branch. Searched every
  committed file (`docs/`, `reports/`) for both numbers: `32752248185` appears repeatedly, always
  correctly attributed to `f0eb220`, in `docs/ACE_EXECUTION_STATE.md`, `docs/DECISION_LOG.md` (inside
  `ADR-0074`'s own evidence section, describing the CI state available when that entry was drafted -
  before `931b6d0` existed), and `reports/AI_HANDOFF_CURRENT.md`. `32756205364` appears in **zero**
  committed files - it was reported only in this session's own chat output after the `931b6d0` push, and
  never written into any tracked document. **Root cause: not an error, a recording gap** - `docs/
  ACE_EXECUTION_STATE.md`'s `LAST_COMMIT`/`LAST_CI_RUN` snapshot fields were last written while drafting
  the `931b6d0` commit itself (before that commit was pushed), so they still named the *previous* commit/
  run (`f0eb220`/`32752248185`) as "current" even after `931b6d0` was pushed and its own CI run
  (`32756205364`) completed successfully - the push-confirmation step never looped back to update the
  snapshot file. Per the owner's own item 7, corrected the canonical state/handoff record: `docs/
  ACE_EXECUTION_STATE.md`'s `LAST_COMMIT (phase-g-governance)` and `LAST_CI_RUN` fields updated to
  `931b6d0`/`32756205364`, via this file's own designed mechanism (a current-state snapshot, explicitly
  "overwritten each time, not append-only," per its own "What this file is" section) - the append-only
  record of *why* it changed is the new Change History row plus this task-log entry. `ADR-0074`'s own
  entry in `docs/DECISION_LOG.md` was **not** edited - its citation of `32752248185` was accurate
  evidence for the state that existed when that entry was drafted, and remains historically correct as
  written; nothing there was rewritten.
- **Task 2 findings (merge-readiness audit), each verified directly, none assumed:** `origin/main` =
  `0e1ef115a647b8a44bf4d1a7af2a3cf3a8b96e03`; `origin/phase-g-governance` = `931b6d09bf331773781ec357a30
  5c412d4c0da04`. `git merge-base --is-ancestor origin/main origin/phase-g-governance` returns false
  (not a simple fast-forward ancestor) - investigated directly rather than treated as a red flag:
  `main`'s own tip is merge commit `0e1ef11` with parents `a3692e7` (main's prior tip) and `76ed443`
  (phase-g-governance's tip at PR #3 merge time); `git merge-base --is-ancestor 76ed443 origin/phase-g-
  governance` returns **true** - confirming `phase-g-governance`'s current tip is a linear descendant of
  everything that was merged into `main`, with zero lost or diverged content; the only reason `main`
  isn't a strict git-ancestor is the expected, normal topology of a feature branch that kept receiving
  commits after its own merge commit was created on the target branch. `git log origin/phase-g-
  governance..origin/main --oneline` - exactly two commits, both `main`'s own historical merge commits
  (PR #3, PR #1) - **no independent content work on `main`**. `git log origin/main..origin/phase-g-
  governance --oneline` - exactly 13 commits, enumerated and each individually matched against this
  session's own ratified ADRs (H-05 push-record, the PR #3 merge-record, `DP-017`/`ADR-0070` H-06,
  `DP-018`/`ADR-0071` H-08, `DP-019`/`ADR-0072` M-02 plus its CI-tolerance fix, `DP-020`/`ADR-0073`
  boundary-proximity indicator, the `ADR-0074` audit and its ratification) - **no unapproved work found**.
  `git diff --stat origin/main origin/phase-g-governance` - 20 files, `4111(+)/65(-)`. `git merge-tree
  --write-tree origin/main origin/phase-g-governance` - returned a single tree hash, exit 0, **no
  conflict markers or file list - a clean, conflict-free merge is available**. `gh pr list --head
  phase-g-governance --state all` - only the two historical, already-merged PRs (#1, #3); **no PR
  currently open** for this 13-commit set. `grep -rn "JATAKA\|jataka" engine/ scripts/` excluding test
  files - **zero hits**; no accidental JATAKA production implementation exists. **Merge-readiness
  result: READY** (mechanically - clean ancestry, no conflicts, all work ratified, CI-green source
  branch). **The merge would preserve the accepted JATAKA-entry state**, since `ADR-0074`'s own
  acceptance and `CURRENT_PHASE: JATAKA ENTERED` already live on `phase-g-governance` and would simply
  be carried into `main` by the merge. **No merge was performed. No PR was created. No self-authorization
  to merge was taken or implied.**
- **Task 3 findings (state re-verification), each re-run fresh this task:** working tree clean
  (`git status --porcelain` limited to `??` untracked pre-existing items); local HEAD = `origin/phase-g-
  governance` = `931b6d09bf331773781ec357a305c412d4c0da04`; `origin/main` unchanged at `0e1ef115a647b8a4
  4bf4d1a7af2a3cf3a8b96e03`; `ADR-0074` `Status: ACCEPTED, on the owner's ratifying instruction recorded
  in the "Ratification of..."` entry; `CURRENT_PHASE` reads `JATAKA ENTERED`; all six Dasha-roadmap ADRs
  (`ADR-0053`, `ADR-0069` through `ADR-0073`) re-confirmed `ACCEPTED`, unchanged; `python scripts/
  check_adr_numbering.py` - 74 ADR entries; `python scripts/check_identifier_families.py` - 20 DP
  identifiers; no JATAKA production code (re-confirmed, same search as Task 2). H-03 and the eight
  `ADR-0072` cross-certifier findings: confirmed untouched, not referenced by any change this task made
  beyond the same read-only citations already in `ADR-0074`'s own unedited text.
- Implementation summary: no code touched. Corrected `docs/ACE_EXECUTION_STATE.md`'s current-snapshot
  fields (its own designed function) and added an append-only Change History row explaining the
  correction's cause and resolution; added this task-log entry recording the full reconciliation and
  merge-readiness audit. `docs/DECISION_LOG.md` was **not** edited - no entry required correction, since
  `ADR-0074`'s own citation was accurate for its own drafting-time evidence.
- Tests executed and results: `python -m pytest -q` last confirmed at 844/844 as part of the immediately
  preceding `931b6d0` push/CI-confirmation; not re-run this task since no code changed.
- Certification executed and results: none - no code or certification artifact touched this task; both
  CI runs' own oracle-gate and drift results were read directly from their logs as evidence (see Task 1
  findings above), not regenerated locally.
- Governance checks executed and results: `python scripts/check_adr_numbering.py` (74 ADR entries,
  unchanged), `python scripts/check_identifier_families.py` (20 DP identifiers, unchanged),
  `python scripts/check_retired_identifiers.py`, `git diff --check` - all PASS.
- Known issues: none new. The stale `DECISION_LOG.md` register-header summary and the eight flagged
  cross-certifier findings remain exactly as previously characterized - non-blocking, not addressed this
  task, per the owner's own explicit instruction not to touch them.
- Unresolved questions: whether the owner authorizes the `main` merge (mechanically READY, per this
  task's own audit); if so, whether via a new PR (matching the PR #1/#3 precedent) or another mechanism;
  which JATAKA capability, if any, to authorize next; whether to push this task's own commit.
- CEO decision required: whether to authorize the `main` merge - this task deliberately stops short of
  it, per the owner's own explicit instruction ("Do NOT merge into main... Do NOT authorize yourself to
  merge... STOP"). Separately, whether to begin JATAKA architecture/implementation for any specific
  capability remains open and undecided.
- Next authorized action: none self-executable. Per the owner's own explicit instruction, this task does
  not merge, does not push to `main`, does not begin JATAKA architecture or implementation, and stops
  here having produced the required reconciliation and readiness output.

### 2026-08-24 - ADR-0074 RATIFIED: JATAKA ENTRY CRITERIA FORMALLY SATISFIED, JATAKA ENTERED
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the ratification
  record and state-file updates, on top of `2f26eee`).
- Previous approved commit: `2f26eee675742b4b672e9af00b50bd1550848548` (`ADR-0074` audit drafted,
  `PROPOSED`) - unpushed, together with `f0eb220` (Dasha roadmap step 6, pushed and CI-confirmed)
  beneath it. `main` (via PR #3, merge commit `0e1ef11`) is unaffected by this task.
- Task (owner's exact instruction): "CEO RATIFICATION — ADR-0074. I ratify ADR-0074 exactly as written
  in commit: 2f26eee. I formally declare the JATAKA entry criteria satisfied under Q8_CLOSURE_MATRIX.md
  §5." The instruction individually confirmed: (1) the FOUNDATION-exit prerequisite is satisfied; (2)
  all six Dasha-roadmap entry steps are satisfied and individually ratified (H-04/`ADR-0053`,
  H-05/`ADR-0069`, H-06/`ADR-0070`, H-08/`ADR-0071`, M-02/`ADR-0072`, boundary-proximity indicator/
  `ADR-0073`); (3) H-03 remains open, separately tracked, and is not a JATAKA-entry prerequisite; (4)
  the eight `H10`/`H11` cross-certifier findings from `ADR-0072` remain separate future work and do not
  block entry; (5) the "six steps, not the roadmap document" interpretation is ratified; (6) the stale
  `DECISION_LOG.md` register-header summary is non-blocking documentation hygiene, not an entry gate;
  (7) this decision authorizes JATAKA phase entry only; (8) it does not authorize any individual
  capability's implementation; (9) every JATAKA capability still needs its own specification, decision/
  ADR, implementation, certification, and CEO approval; (10) JATAKA implementation is not begun as part
  of this ratification. Further instructed: do not begin JATAKA implementation; record the ratification
  via the established ADR follow-up mechanism; update canonical execution-state and handoff records; do
  not push/merge without separate authorization; perform a final JATAKA-entry state verification and
  stop.
- Relevant ADR/specification: `docs/DECISION_LOG.md` `ADR-0074` (the entry ratified, its Status line
  changed from `PROPOSED` to `ACCEPTED`, no other text edited) and its new `#### Ratification of
  ADR-0074` follow-up sub-entry (the ratifying record itself - authoritative over this summary);
  `ADR-0068`'s own "Ratification of ADR-0068" sub-entry (the precedent this task's own mechanism mirrors
  exactly); `Q8_CLOSURE_MATRIX.md` s5 (the criteria formally declared satisfied); `ADR-0053`, `ADR-0069`
  through `ADR-0073` (the six Dasha-roadmap ADRs this ratification confirms, not reopened).
- Files changed: `docs/DECISION_LOG.md` (`ADR-0074`'s Status line updated; new `#### Ratification of
  ADR-0074` sub-entry added), `docs/ACE_EXECUTION_STATE.md` (version 6.0.0, `CURRENT_PHASE` updated to
  JATAKA ENTERED), this file.
- Implementation summary: recorded the ratification using the exact mechanism `ADR-0068`'s own
  ratification established as precedent in this repository - a minimal Status-line edit on the original
  entry ("PROPOSED" -> "ACCEPTED, on the owner's ratifying instruction recorded in the follow-up entry
  below"), plus a new, separate `####`-level "Ratification of ADR-0074" sub-entry (not a new top-level
  numbered ADR) quoting the owner's full instruction verbatim and individually restating each of the ten
  items it enumerated, none reinterpreted, narrowed, or extended beyond what `ADR-0074` itself already
  stated. `docs/ACE_EXECUTION_STATE.md`'s `CURRENT_PHASE` field updated from "FOUNDATION EXITED... JATAKA
  NOT entered" to "JATAKA ENTERED (`ADR-0074`, ratified 2026-08-24)," explicitly noting entry authorizes
  the phase only - no individual capability.
- Tests executed and results: `python -m pytest -q` - **844 passed, 0 failed, 0 skipped**, unchanged (no
  code touched this task - a governance-record ratification only).
- Certification executed and results: none - no code or certification artifact touched this task.
- Governance checks executed and results: `python scripts/check_adr_numbering.py` (**74 ADR entries,
  unchanged** - the ratification is a sub-entry within `ADR-0074`, not a new numbered ADR, matching the
  `ADR-0068` precedent exactly), `python scripts/check_identifier_families.py` (20 DP identifiers,
  unchanged), `python scripts/check_retired_identifiers.py`, `git diff --check` - all PASS.
- Known issues: none new. The stale `DECISION_LOG.md` register-header summary (flagged in `ADR-0074`
  itself, and explicitly confirmed non-blocking by the owner's own item 6) remains uncorrected, by
  design, as does the eight-certifier `H10`/`H11` finding from `ADR-0072` - both remain available for
  their own separate, future follow-up.
- Final JATAKA-entry state verification (performed fresh this task, per the owner's own closing
  instruction): `ADR-0074`'s `Status` field reads `ACCEPTED`; its own "Ratification of ADR-0074"
  sub-entry is present and quotes the owner's instruction verbatim; all six Dasha-roadmap ADRs'
  `Status` fields remain `ACCEPTED` (unchanged by this task); `docs/ACE_EXECUTION_STATE.md`'s
  `CURRENT_PHASE` reads `JATAKA ENTERED`; no file under `engine/` was touched this task
  (`git status --porcelain` limited to the two documentation files plus this one); governance gates
  clean (74 ADR entries, 20 DP identifiers); full test suite 844/844 unchanged. **JATAKA is formally
  entered. No JATAKA capability implementation has been authorized or begun.**
- Unresolved questions: which, if any, JATAKA capability the owner wishes to authorize next (a specific
  varga, a Vimshottari extension, aspect coverage, planet strength, or something else - each requires
  its own separate specification/decision/ADR per `Q8_CLOSURE_MATRIX.md` s5); whether the flagged
  cross-certifier finding or the stale register header warrant their own follow-up work; whether/when to
  push the now-two unpushed commits (`2f26eee`, this task's own) or merge `phase-g-governance` to `main`.
- CEO decision required: none to close out this task - the ratification itself was the decision point,
  now recorded. The next genuine decision point is authorizing a specific JATAKA capability, authorizing
  a push, or directing other work.
- Next authorized action: none self-executable. Per the owner's own explicit instruction, this task does
  not begin JATAKA implementation and does not push - it performs the final state verification above and
  stops here.

### 2026-08-24 - Pushed f0eb220 (Dasha roadmap step 6, ADR-0073), CI-confirmed (run 32752248185); ADR-0074 drafted: JATAKA-entry readiness audit (PROPOSED, not self-ratified)
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the audit's
  documentation updates, on top of `f0eb220`).
- Previous approved commit: `f0eb220d4b5e05a8f8fcf7798810f6f195981a29` (Dasha roadmap step 6, `ADR-0073`)
  - now pushed and CI-confirmed (this task's first half). `main` (via PR #3, merge commit `0e1ef11`) is
  unaffected by this task.
- Task, part 1 (push authorization): "Approve push of the final Dasha-roadmap commit... Push only this
  commit to origin/phase-g-governance... After pushing: verify the remote SHA; wait for CI; inspect the
  actual CI logs; confirm all four jobs are green; confirm the new boundary-proximity tests actually
  execute in CI; confirm the Vimshottari oracle certification remains clean; confirm artifact drift is
  clean; confirm zero change to pre-existing certified values; confirm the six Dasha roadmap steps are
  represented correctly in the canonical state; report the exact CI run and final repository state; stop
  after CI confirmation."
- Push executed: `git push origin phase-g-governance` - fast-forward `d18e7ff..f0eb220`. Verified
  `origin/phase-g-governance` == local HEAD == `f0eb220d4b5e05a8f8fcf7798810f6f195981a29`, both
  directions. CI run **`32752248185`** (headSha `f0eb220`) - **all four jobs green**, read directly from
  the log: `governance gate` - 73 ADR entries, 20 DP identifiers, all checks PASS. `oracle gate
  (PyJHora, hash-pinned)` - `pratyantar rows: 20412`, `lord mismatches: 0`, drift `PASS: 46 evidence
  file(s) identical to the committed version outside the volatile fields`. `no-oracle gate (3.11)` and
  `(3.12)` - `844 passed` on each (both the default run and the network-guard re-run subset, up from 837,
  exactly matching the 7 new boundary-proximity-indicator tests, confirming they genuinely executed),
  drift PASS on each. Working tree confirmed clean.
- **Dasha roadmap step 6, and the full six-step Dasha roadmap, is now fully CI-confirmed with zero
  certified-value impact, closing the task's first half.**
- Task, part 2 (JATAKA entry readiness audit): "JATAKA ENTRY READINESS AUDIT — DO NOT IMPLEMENT YET,"
  with all six Dasha-roadmap ADRs restated (`ADR-0053`, `ADR-0069` through `ADR-0073`), the final CI run
  and HEAD SHA cited, and an explicit thirteen-item audit scope: read `Q8_CLOSURE_MATRIX.md` s5 in full;
  verify every JATAKA entry requirement literally; verify all six Dasha prerequisites and their accepted
  ADRs; verify their CI evidence and certification artifacts; verify FOUNDATION remains formally exited;
  verify current `main`/`phase-g` branch state and CI; search the entire repository for H-03 and
  determine its disposition without inventing a requirement; reconcile the eight `H10`/`H11`
  cross-certifier findings from `ADR-0072`, determining whether any actually blocks JATAKA entry; search
  for any other explicit JATAKA-entry prerequisite outside the six Dasha steps; verify no uncertified
  calculation/methodology/dependency is silently promoted into JATAKA scope; verify no JATAKA
  implementation already exists accidentally; identify any remaining governance/architecture/
  certification/specification prerequisite; do not reinterpret ambiguous text silently - quote the
  governing language and present any ambiguity as an owner decision. Produce a formal readiness report;
  if satisfied, prepare a narrow JATAKA entry decision paper/ADR for CEO ratification, without
  self-ratifying; do not implement JATAKA; do not modify closed Dasha/FOUNDATION items; do not modify the
  eight flagged findings unless proven an actual blocker; do not push/merge without separate
  authorization; stop at the genuine CEO decision point.
- Relevant ADR/specification: `docs/Q8_CLOSURE_MATRIX.md` s5 (JATAKA), s14 (cross-phase invariants), s15
  (Q8 closure framing - "No phase is thereby authorised"), all re-read in full; `docs/
  DASHA_CERTIFICATION_ROADMAP.md` (re-read in full, still `Status: PROPOSED`, Version 1.0.0);
  `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` H-03 (read in full, the primary source for the H-03
  determination); `ADR-0068` (FOUNDATION-exit readiness, the direct precedent this audit's own shape and
  `ADR-0074`'s own `PROPOSED`-then-ratify pattern mirrors); `ADR-0053`, `ADR-0069` through `ADR-0073`
  (all six Dasha-roadmap ADRs, each `Status` field re-verified directly, not reopened); `ADR-0072`
  (the eight flagged cross-certifier findings, reconciled not reopened).
- Files changed: `docs/DECISION_LOG.md` (`ADR-0074` appended, `Status: PROPOSED`), `docs/
  ACE_EXECUTION_STATE.md` (version 5.9.0), this file.
- **Audit performed exactly as mandated, each item independently verified against the live repository:**
  confirmed branch `phase-g-governance`, local HEAD == `origin/phase-g-governance` == `f0eb220`, working
  tree clean, `origin/main` at `0e1ef11` unchanged (`phase-g-governance` not yet merged to `main` - a
  factual state, explicitly found not to block entry under the entry-criteria text, mirroring the
  `ADR-0068` precedent where FOUNDATION was itself ratified while still unmerged). Re-read `Q8_CLOSURE_
  MATRIX.md` s5 fresh, quoted directly. Re-verified all six Dasha-roadmap ADRs' own `Status` fields
  directly in `docs/DECISION_LOG.md` (not trusted from the register-header summary, which was found stale
  - see below): all six `ACCEPTED`, each with its own explicit owner-instruction citation. Re-inspected
  CI run `32752248185`'s full job list and log content. Re-inspected `certification/
  VIMSHOTTARI_V1_certification.json`'s `result`/`oracle_lord_mismatches`/`near_boundary_coverage`/
  `boundary_proximity_indicator` fields directly, and ran `check_artifact_drift.py` fresh (clean against
  the current committed state). Re-verified `ADR-0068`'s own `Status` field directly (its entry title
  retains historical "PROPOSED" phrasing per this repository's "change only the Status line" discipline;
  the Status field itself is unambiguous - `ACCEPTED`).
- **H-03 determination:** `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` H-03 - "The transit oracle gate
  cannot detect a systematic astronomical bias," `scripts/certify_transits.py`'s tolerance derived from
  the same quantity it is meant to bound. Repository-wide search confirmed H-03 is named nowhere in
  `docs/DASHA_CERTIFICATION_ROADMAP.md`'s own findings list, nowhere in `Q8_CLOSURE_MATRIX.md`'s
  FOUNDATION or JATAKA sections, and never claimed resolved by any of this session's six Dasha-roadmap
  ADRs. **Determination: genuinely absent from JATAKA's entry criteria and the Dasha roadmap - not
  renamed, superseded, retired, or incorporated - a real, separate, still-open `TRANSIT_V1` finding, not
  invented as a requirement here.**
- **H10/H11 cross-certifier determination:** the eight certifiers `ADR-0072` flagged (`certify_
  trikalam.py`, `certify_panchanga.py`, `certify_rise_set.py`, `certify_tier0.py`, `certify_kp_chain.py`,
  `certify_parashari_drishti.py`, `certify_current_engine.py`, `test_kp_chart.py`) re-confirmed: none is
  a Dasha-roadmap item, none is named in JATAKA's entry-criteria text, and none of the six Dasha-roadmap
  ADRs' own closure depended on any of their case correctness (verified directly for H-08 and M-02
  specifically, the two most plausibly adjacent). **Determination: does not block JATAKA entry; remains a
  genuine, separate future item, exactly as `ADR-0072` characterized it - not touched.**
- **Other findings:** no accidental JATAKA implementation - zero "JATAKA" hits anywhere in `engine/`;
  `engine/astrology/planet_strength.py` exists (named in JATAKA's own future implementation-scope text)
  but is pre-existing legacy code from 2026-07-30/08-08, predating Phase G/FOUNDATION/this session
  entirely, with zero production consumers (only its own test references it) - not new work, not silently
  promoted into use. A textual interpretation point presented explicitly, not resolved silently: `docs/
  DASHA_CERTIFICATION_ROADMAP.md` itself remains `Status: PROPOSED` as a planning document, but `Q8_
  CLOSURE_MATRIX.md` s5's own text requires only that the six named **steps** be complete, not that the
  parent document be ratified - each step carries its own separate, explicitly owner-ratified ADR, and
  this reading has been applied consistently across all six steps this session, with the roadmap's own
  `PROPOSED` status visible in every decision-readiness paper at ratification time. A non-blocking
  governance-hygiene gap found and flagged, not silently fixed: `docs/DECISION_LOG.md`'s own register-
  header summary line was not updated after `ADR-0070` through `ADR-0073`, still reading "ACCEPTED (47):
  ..., ADR-0048 through ADR-0069" - each entry's own `Status` field is independently correct regardless.
- Implementation summary: drafted `ADR-0074` (`Status: PROPOSED`, mirroring `ADR-0068`'s own FOUNDATION-
  exit-readiness shape exactly, next free ADR number confirmed via `check_adr_numbering.py`), presenting
  every finding above with its own evidence, and explicitly stating it does not authorize JATAKA
  implementation even if ratified (`Q8_CLOSURE_MATRIX.md` s5's own "Implementation scope"/"CEO approval"
  rows require separate, per-capability authorization). One placeholder-identifier false positive (a
  prose phrase beginning with the `ADR-` prefix but not an actual identifier) caught by the governance
  hook and corrected mechanically before commit.
- Tests executed and results: `python -m pytest -q` - **844 passed, 0 failed, 0 skipped**, unchanged (no
  code touched this task - documentation and audit only).
- Certification executed and results: none regenerated this task - `certification/
  VIMSHOTTARI_V1_certification.json` inspected directly (read-only) and `check_artifact_drift.py` run
  fresh (clean against the current committed state); no certifier re-run, since CI's own run
  (`32752248185`) already provides fresh, independent confirmation.
- Governance checks executed and results: `python scripts/check_adr_numbering.py` (**74 ADR entries, up
  from 73**), `python scripts/check_identifier_families.py` (20 DP identifiers, unchanged),
  `python scripts/check_retired_identifiers.py`, `git diff --check` - all PASS (after the one mechanical
  placeholder-identifier fix above).
- Known issues: the stale `DECISION_LOG.md` register-header summary (flagged above) remains uncorrected,
  by design - fixing it was judged outside this task's own explicit scope (audit + decision paper only),
  offered as a small, separate action on request.
- Unresolved questions: whether the owner ratifies `ADR-0074`'s JATAKA-entry determination as drafted, or
  amends it; if ratified, when/whether to authorize general JATAKA implementation (a separate act
  regardless); whether the flagged cross-certifier and stale-header findings warrant their own follow-up
  work.
- CEO decision required: ratify (or amend) `ADR-0074`'s JATAKA-entry-readiness determination. This is the
  genuine CEO decision point the owner's own closing instruction asked this task to stop at.
- Next authorized action: none self-executable. Per the owner's own explicit instruction, this task does
  not implement JATAKA, does not push, and stops here awaiting the owner's own ratifying instruction (or
  amendment, or other direction).

### 2026-08-24 - ADR-0073 ratifies DP-020 Option 1: narrow seed-only seed_nakshatra_boundary_arcsec field (DASHA ROADMAP FULLY CLOSED - all six steps)
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the boundary-
  proximity-indicator implementation, on top of `4512061`).
- Previous approved commit: `45120614854ccb78cdb584a4be0f695c57a5835a` (`DP-020` drafted, dasha
  boundary-proximity-indicator decision-readiness) - unpushed, together with `d18e7ff` (M-02, pushed and
  CI-confirmed) beneath it. `main` (via PR #3, merge commit `0e1ef11`) is unaffected by this task.
- Task (owner's exact instruction): "CEO DECISION — DP-020 FINAL DASHA ROADMAP STEP. Ratify DP-020
  Option 1 exactly as proposed: Build the narrow, seed-only dasha boundary-proximity field using the
  already-certified seed_elapsed_fraction / M-02 evidence, with the methodology and certification scope
  explicitly defined by DP-020." Constraints: (1) implement only the narrow seed-only capability; (2)
  reuse seed_elapsed_fraction, no new astronomical calculations unless explicitly required (none were);
  (3) do not copy KP's nearest_boundary_arcsec implementation, given H-07's own incompleteness; (4) do
  not treat KP's field, M-02's diagnostic, or any other existing signal as certified merely because it
  produces a number; (5) define and record exactly what the indicator means and does not claim; (6) do
  not add Option 2's amplified days-of-uncertainty semantic; (7) do not use disclosure-only treatment;
  (8) do not implement Option 4's unreachable refusal mechanism; (9) do not defer; (10) preserve existing
  certified values; (11)-(13) do not modify H-04/H-05/H-06/H-08/M-02, do not reopen FOUNDATION, do not
  modify the eight cross-certifier findings; (14) do not begin general JATAKA; (15) genuine tests proving
  the field's semantics and scope; (16) negative controls so the gate can meaningfully fail; (17) produce
  the appropriate certification artifact and provenance; (18) run full regression/governance/oracle/
  drift checks; (19) update the ADR/decision paper and canonical records; (20) do not weaken any gate;
  (21) do not push without separate authorization.
- Relevant ADR/specification: `docs/decisions/DP-020-dasha-boundary-proximity-indicator.md` sections F
  (Option 1) and G (the recommendation this ratifies); `docs/DECISION_LOG.md` `ADR-0073` (the ratifying
  entry, containing the full implementation and reasoning record - authoritative over this summary);
  `docs/DASHA_CERTIFICATION_ROADMAP.md` section 4/5 step 6; `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md`
  H-07 (the KP-indicator completeness defect this design deliberately avoids repeating); `ADR-0069`
  (H-05's hermetic-verification precedent, applied here since the field has no independent oracle
  equivalent to compare against); `ADR-0072` (M-02's own near-boundary evidence, reused for this field's
  own correctness verification); `ADR-0053`/`ADR-0070`/`ADR-0071` (H-04/H-06/H-08, not reopened).
- Files changed: `engine/models/dasha.py` (added `VimshottariTimeline.seed_nakshatra_boundary_arcsec`,
  fully documented scope/non-claims); `engine/dasha/vimshottari.py` (computed the field from the already-
  computed `elapsed` local variable, module docstring updated); `engine/tests/
  test_vimshottari_boundary_proximity_indicator.py` (new, 7 tests); `scripts/certify_vimshottari.py`
  (`run_case()` gained a per-case self-check and `seed_nakshatra_boundary_arcsec` recording; `main()`
  gained a `gates.boundary_proximity_indicator` artifact section; `explicit_non_claims` gained one entry);
  `certification/VIMSHOTTARI_V1_certification.json`, `reports/certification/vimshottari.report.md`,
  `reports/certification/vimshottari.console.txt` (regenerated; console-txt's Windows path-separator
  quirk corrected before commit); `docs/DECISION_LOG.md` (`ADR-0073` appended); `docs/decisions/
  DP-020-dasha-boundary-proximity-indicator.md` (status header updated); `docs/decisions/README.md`
  (`DP-020` row + change history); `docs/ACE_EXECUTION_STATE.md` (version 5.8.0); this file.
- Implementation summary: `seed_nakshatra_boundary_arcsec` is computed as `float(min(elapsed, 1 -
  elapsed) * NAK_SPAN * 3600)` inside `vimshottari_from_moon()`, reusing the exact same `elapsed` local
  variable already computed for `seed_elapsed_fraction` - exact `Fraction` arithmetic throughout, float
  only at the final step, matching this project's own established convention. Deliberately **not**
  modelled on KP's own `nearest_boundary_arcsec` computation (a minimum over three levels via `to_exact`/
  `walk()`): that field's own docstring claims coverage "at any level" while its implementation omits the
  sign boundary (H-07, an open, unresolved defect, independently reproduced live this task:
  `kp_chain(29.999999999)` returns `sign_lord='Ma'` with `nearest_boundary_arcsec=380.0000036`). The new
  field's own name and docstring instead state its scope explicitly and narrowly - nakshatra/seed
  boundary only, not deeper period-transition boundaries, not any KP-specific level, and not a
  dasha-date-uncertainty figure (Option 2, not chosen) - and explicitly cross-reference both KP's own
  field and M-02's own certifier-only diagnostic as separate signals that must not be silently conflated
  with it.
- Tests executed and results: `python -m pytest -q` - **844 passed, 0 failed, 0 skipped** (up from 837 by
  exactly the 7 new tests): the six near-boundary cases M-02 already root-found and oracle-verified
  (`ADR-0072`) each agree with an independent measurement computed by a deliberately different code path;
  all six report values under M-02's own 360-arcsec `NEAR_BOUNDARY_THRESHOLD_DEG`; the H-05 baseline case
  (`moon=5.0`, `ADR-0069`) reports `18000.0` arcsec, proving the field discriminates near from far, not a
  constant; the two root-found `"_at"` instants report the tightest values of the six, matching the
  expected shape of a genuine boundary crossing; a direct re-derivation check confirms the field's own
  value is exactly reproducible from `seed_elapsed_fraction` alone; a genuine negative control
  (`monkeypatch.setattr(vimshottari_module, "NAK_SPAN", Fraction(1, 1))`, verified as the correct patch
  target this task since `vimshottari.py` binds `NAK_SPAN` via `from ... import`) confirms the H-05
  baseline's pinned value changes under the mutation and is restored afterward; a structural guard
  confirms `VimshottariTimeline` carries no "uncertainty"-named field and no KP-style multi-level fields.
- Certification executed and results: `python scripts/certify_vimshottari.py`, run in the isolated
  PyJHora exploration venv - **PASS, lord mismatches: 0** across all 17 cases, including the new
  per-case self-check comparing `seed_nakshatra_boundary_arcsec` against an independently measured
  distance (a genuine, potentially-failing gate, not a tautological self-comparison). Structured
  comparison of the regenerated artifact against the previously committed one: every pre-existing case's
  own recorded result byte-identical (excluding the new, always-present `seed_nakshatra_boundary_arcsec`
  diagnostic field). `python scripts/check_artifact_drift.py` run against the regenerated-but-uncommitted
  artifact correctly flagged exactly the intended changes (`explicit_non_claims` length `5 -> 6`,
  `gates.boundary_proximity_indicator: added`, the new field added to all 28 per-case entries) and
  nothing else. The regenerated console transcript's Windows-path backslash artifact was corrected to the
  committed forward-slash convention before commit. `python scripts/certify_kp_chain.py` run as an M-03
  anti-fitting scan-surface sanity check - PASS, only the same class of volatile-field diff, discarded via
  `git checkout --`, not committed.
- Governance checks executed and results: `python scripts/check_adr_numbering.py` (**73 ADR entries, up
  from 72**), `python scripts/check_identifier_families.py` (20 DP identifiers, unchanged),
  `python scripts/check_retired_identifiers.py`,
  `python -m pytest engine/tests/test_retired_identifier_gate_scope.py -q` (36 passed) - all PASS.
- Known issues: none. `DP-015`/`ADR-0067`'s own, textually distinct FOUNDATION-scope boundary-proximity
  decision remains untouched - the terminology overlap is documented explicitly in both `DP-020` and
  `ADR-0073` to prevent future conflation.
- Unresolved questions: whether the flagged cross-certifier "H10/H11" mislabeling in 8 other certifiers
  (`ADR-0072`) warrants its own future investigation; whether/when general JATAKA implementation is
  authorized.
- CEO decision required: **the Dasha roadmap (all six steps) is now fully closed.** `Q8_CLOSURE_
  MATRIX.md` s5's own JATAKA entry-criteria text is satisfied on its own plain terms - but this does not
  itself authorize beginning JATAKA implementation. The next genuine decision point is authorizing general
  JATAKA implementation (or a different task), authorizing a push of this task's commit, or deciding on
  the flagged cross-certifier finding.
- Next authorized action: none self-executable. Per the owner's own closing instruction, stop here and
  await the next genuine CEO decision, blocker, or push-authorization checkpoint.

### 2026-08-24 - Pushed d18e7ff (M-02 CI-fix), fully CI-confirmed (run 32711122102); DP-020 drafted: dasha boundary-proximity-indicator decision-readiness only
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the DP-020 paper
  and state-file updates, on top of `d18e7ff`).
- Previous approved commits: `53ec25e` (M-02 implementation, `ADR-0072`) and `d18e7ff` (the CI-fix
  follow-up) - both now pushed and CI-confirmed (this task's first half). `main` (via PR #3, merge commit
  `0e1ef11`) is unaffected by this task.
- Task, part 1 (push authorization for the CI-fix): "Approve the CI-fix commit and push... commit the
  fix; push the new commit to origin/phase-g-governance; wait for CI; inspect the actual CI logs; confirm
  all four jobs are green; confirm the oracle gate remains 0 lord mismatches and artifact drift remains
  clean; confirm 837/837 (or the corresponding CI count) passes; report the exact new commit SHA and CI
  run." (This followed an earlier, self-contained diagnosis: CI run `32709856831` on commit `53ec25e`
  failed on both no-oracle gate legs because a new M-02 test asserted bit-exact equality on a raw
  swetest/pyswisseph-derived Moon longitude, which differed from this Windows host's own value by 3 ULPs
  (~1.7e-13 degrees) - ordinary cross-platform trigonometric-library noise, confirmed by the oracle gate
  and 836 of 837 other tests passing cleanly on the same commit. Fixed by using a `1e-9` tolerance instead
  of `==`, matching the tolerance already used on the adjacent assertion in the same test - a test-only
  change, no production code, certification artifact, or gate touched.)
- CI-fix committed as `d18e7ffa54a5cbb673df66defa4308f88aff1f45` and pushed - fast-forward
  `53ec25e..d18e7ff`. **CI run `32711122102`** (headSha `d18e7ff`) - **all four jobs green**, read
  directly from the log: `governance gate` - 72 ADR entries, 19 DP identifiers, all checks PASS.
  `no-oracle gate (3.11)` and `(3.12)` - `837 passed` on each (both the default run and the network-guard
  re-run subset), including `Near-boundary cases: 216 PASSED` in the independent holdout validators;
  drift check `PASS: 46 evidence file(s) identical to the committed version outside the volatile fields`
  on each. `oracle gate (PyJHora, hash-pinned)` - `pratyantar rows: 20412`, `lord mismatches: 0`,
  `near-boundary: 6 genuine cases (3 per profile, native only), max 0.044714 deg from boundary`; drift
  check PASS. Remote SHA confirmed identical to local HEAD, both directions. Working tree confirmed clean
  of all tracked changes.
- **M-02 is now fully CI-confirmed, with zero certified-value impact, closing the task's first half.**
- Task, part 2 (dasha boundary-proximity-indicator decision-readiness): "AUTHORIZE FINAL DASHA-ROADMAP
  ITEM — DECISION-READINESS ONLY," with the current verified state restated (FOUNDATION exited;
  `phase-g-governance` merged to `main`; H-04/H-05/H-06/H-08 closed and CI-confirmed; M-02 closed and
  CI-confirmed at `d18e7ff`, CI run `32711122102` fully green; this is the final remaining item in the
  six-step Dasha roadmap) and an explicit twenty-three-item scope: verify branch/HEAD/origin/working-tree
  state; read `Q8_CLOSURE_MATRIX.md` s5; read the complete `DASHA_CERTIFICATION_ROADMAP.md`; locate and
  inspect every reference to the dasha-specific boundary-proximity indicator; inspect all relevant
  Vimshottari/nakshatra/boundary code, certification artifacts, holdouts, tests, and prior decisions;
  independently reproduce the underlying finding/evidence; determine exactly what the indicator would
  mean and claim; determine whether the architecture already has a related signal that must not be
  silently treated as equivalent; classify the issue precisely; identify all legitimate options; determine
  blast radius and interaction with certified values; determine whether the indicator should be
  implemented and certified, explicitly deferred, explicitly refused until certified, or otherwise
  treated; review H-05/H-06/H-08/M-02 as precedents without mechanically copying them; draft a narrow
  decision paper with exact owner decision wording; do not select/ratify; do not implement anything; do
  not reopen FOUNDATION or H-04/H-05/H-06/H-08/M-02; do not begin general JATAKA; do not modify the eight
  cross-certifier `H10`/`H11` findings from `ADR-0072`; do not weaken any gate; preserve canonical state
  and historical records; do not push without separate authorization.
- Relevant ADR/specification: `docs/DASHA_CERTIFICATION_ROADMAP.md` section 4 ("Boundary sensitivity as
  an output") and section 5 step 6 (re-read in full, still `Status: PROPOSED`); `reports/
  G1_ARCHITECTURE_AUDIT_2026-08-11.md` H-07 (the KP boundary-indicator completeness defect, re-verified
  live); `engine/kp/chain.py`/`engine/models/kp_chain.py` (the existing `nearest_boundary_arcsec`
  precedent and its own known gap); `engine/models/dasha.py` (confirming no proximity field exists on
  `VimshottariTimeline`); `docs/decisions/DP-015-foundation-boundary-proximity-indicators.md` and
  `ADR-0067` (the textually distinct, already-closed FOUNDATION-scope item and its own forward-binding
  rule, not reopened); `docs/Q8_CLOSURE_MATRIX.md` (JATAKA's own entry-criteria text and BTR's position
  at section 13); `ADR-0053`/`ADR-0069`/`ADR-0070`/`ADR-0071`/`ADR-0072` (H-04/H-05/H-06/H-08/M-02, not
  reopened).
- Files changed: `docs/decisions/DP-020-dasha-boundary-proximity-indicator.md` (new), `docs/decisions/
  README.md` (`DP-020` registered before drafting, per `ADR-0040`), `docs/ACE_EXECUTION_STATE.md`
  (version 5.7.0), this file.
- **Pre-work performed exactly as mandated:** confirmed branch `phase-g-governance`, local HEAD ==
  `origin/phase-g-governance` == `d18e7ff`, working tree clean of tracked changes, `origin/main` at
  `0e1ef11` unchanged. Read `Q8_CLOSURE_MATRIX.md` s5 fresh (JATAKA's own six-step entry-criteria text
  names "boundary-proximity indicator" plainly, with no carve-out clause). Read `docs/
  DASHA_CERTIFICATION_ROADMAP.md` in full - section 4's "Boundary sensitivity as an output" is the direct
  source for step 6, textually distinct from the separate, not-in-the-six-step-list "Boundaries in time"
  (period-transition membership) group. Inspected, directly, not from memory: `engine/kp/chain.py`'s
  `nearest_boundary_arcsec` computation (a minimum over nakshatra/sub/sub-sub edges, omitting the sign
  edge - H-07); every field on `VimshottariTimeline` (confirming none is a proximity signal);
  `scripts/certify_vimshottari.py`'s new `moon_distance_to_nearest_boundary_deg` diagnostic (confirming
  it is certifier-only, not a production signal); `DP-015`/`ADR-0067`'s own "Option 3 (AMENDED)" full
  text (confirming its forward-binding rule and its own anticipation of "a future decision paper... when
  a consuming feature actually needs one" - this paper is that kind of follow-up, for the dasha-specific
  instance, not a reopening); `docs/Q8_CLOSURE_MATRIX.md` section 13 (confirming BTR, the roadmap's own
  stated motivating consumer, sits downstream of EVIDENCE, which itself requires JATAKA exit first - no
  current consumer exists, mirroring `DP-015`'s own finding independently re-confirmed here). Searched
  `docs/DECISION_LOG.md` and `docs/decisions/` for prior work on the dasha-specific item: zero hits beyond
  open-roadmap-step citations and `DP-015`'s own textually distinct item.
- **Independent reproduction, not trusted from either document's own summary:** `kp_chain(29.999999999)`
  live - returns `sign_lord='Ma'` with `nearest_boundary_arcsec=380.0000036`, matching the audit's own
  reported case (H-07) exactly, confirming KP's own indicator remains incomplete today. Verified a
  boundary-proximity value is **exactly and losslessly derivable from `seed_elapsed_fraction` alone**,
  with zero new astronomical calculation: for M-02's own `B1_lahiri_boundary_before` case (Moon
  `119.95579900`), `min(elapsed, 1-elapsed) * NAK_SPAN` yields `0.044201` degrees, matching a direct
  measurement of the same Moon longitude to nine decimal places - concrete evidence for Option 1's own
  low blast radius, and the basis for identifying `seed_elapsed_fraction` as a "related signal that must
  not be silently treated as equivalent" (the owner's own item 8).
- Implementation summary (no code touched - decision-paper drafting only): registered `DP-020` in `docs/
  decisions/README.md`'s index first, per `ADR-0040`, then drafted it, structured to match this session's
  established DP template (sections 1, 2, A-I, change history). **Section A** (what the indicator would
  mean): how close the birth Moon was to a nakshatra boundary, and therefore how sensitive the whole
  mahadasha sequence is - the roadmap's own "amplification" framing suggests the value lies not just in a
  raw distance but in a dasha-specific, lord-multiplier-amplified days-of-uncertainty figure. **Section
  B** (related signals): `seed_elapsed_fraction` and M-02's own certifier-only diagnostic, neither
  purpose-built or certified for this use. **Section C** (classification): a missing capability plus a
  methodology gap, not a defect. **Section E** reviews H-05/H-06/H-08/M-02 as precedents explicitly,
  finding H-08's own additive-disclosure-field shape the closest structural match, and explicitly
  declining to mechanically copy KP's own `nearest_boundary_arcsec` given its unresolved H-07 defect.
  **Section F** presents five options: Option 1 (build a narrow, seed-only field, reusing M-02's own six
  `BOUNDARY_HOLDOUT` cases for certification, zero certified-value impact, two open sub-questions -
  amplification figure, naming); Option 2 (Option 1 plus the amplified figure, resolved now); Option 3
  (disclosure-only, mirroring H-08's status-quo-plus-documentation shape, but requiring its own fresh
  interpretive ruling since JATAKA's text lacks FOUNDATION's carve-out clause); Option 4 (an explicit but
  currently-unreachable refusal mechanism, since no consumer exists yet to refuse); Option 5 (defer -
  explicitly found NOT to unblock JATAKA the way `ADR-0067` unblocked FOUNDATION, a materially weaker
  position than `DP-015`'s own equivalent choice). **Section G** recommends Option 1 at medium confidence.
  Section H explicitly confirms `DP-015`/`ADR-0067`, H-04/H-05/H-06/H-08/M-02, the eight flagged
  cross-certifier findings, and general JATAKA are all untouched and not reopened.
- Tests executed and results: none run for this decision-paper-only task (no code touched); the
  reproduction above was interactive verification, not a committed test. Full test suite last confirmed
  at 837/837 as part of the immediately preceding M-02 CI-fix push/confirmation (this task's own first
  half).
- Certification executed and results: none - no code or certification artifact touched this task.
- Governance checks executed and results: `python scripts/check_adr_numbering.py` (72 ADR entries,
  unchanged), `python scripts/check_identifier_families.py` (**20 registered DP identifiers, up from
  19**, no unregistered tokens), `python scripts/check_retired_identifiers.py`,
  `python -m pytest engine/tests/test_retired_identifier_gate_scope.py -q` (36 passed, confirming no
  repeat of the placeholder-identifier issue found in an earlier task) - all PASS.
- Known issues: none. The distinction between this item and `DP-015`/`ADR-0067`'s own FOUNDATION-scope
  boundary-proximity item is recorded explicitly and prominently in the paper itself (both in its opening
  section and throughout) to prevent future conflation - the two share terminology but are textually and
  procedurally distinct decisions.
- Unresolved questions: which of `DP-020`'s five options the owner selects; if Option 1 or 2, whether the
  amplification figure is resolved now or left open, and what the field is named/what units it uses.
- CEO decision required: select `DP-020`'s Option 1, 2, 3, 4, or 5 for the dasha boundary-proximity
  indicator - the sixth and final Dasha-roadmap step.
- Next authorized action: none self-executable. Per the owner's own closing instruction, continue until
  the genuine CEO decision point - reached here; awaiting the owner's option selection. Once decided (in
  whichever direction), the six-step Dasha roadmap will be fully resolved, though JATAKA's own general
  implementation would still require its own separate, explicit authorization regardless.

### 2026-08-24 - ADR-0072 ratifies DP-019 Option 1: genuine root-found near-boundary oracle-gate cases + H10/H11 correction (M-02 CLOSED)
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the M-02
  implementation, on top of `6055399`).
- Previous approved commit: `60553994eaba0a0d5cc4e3fc6dac9edcef445eb6` (`DP-019` drafted, M-02
  decision-readiness) - unpushed, together with `19dbc6b` (H-08, pushed and CI-confirmed) beneath it.
  `main` (via PR #3, merge commit `0e1ef11`) is unaffected by this task.
- Task (owner's exact instruction): "CEO DECISION — DP-019 M-02. Ratify DP-019 Option 1: Root-find
  genuine Moon/nakshatra-boundary oracle-gate holdout cases and correct the mislabeled existing boundary
  cases as part of the same work." Scope: (1) add genuine cases using the already-verified root-finding
  approach; (2) correct `H10_boundary_moon_a`/`H11_boundary_moon_b` labels/data as required by the
  evidence; (3) preserve the distinction between genuine boundary-proximity and ordinary cases; (4) use
  the oracle-gate methodology, do not substitute hermetic-only coverage; (5) preserve existing certified
  Vimshottari values; (6) do not alter production calculation logic unless a genuine defect is
  demonstrated (none was); (7) preserve the certification artifact's structure/provenance; (8) add
  genuine tests proving the cases are actually at the intended boundary; (9) include appropriate negative
  controls; (10) verify existing cases unchanged except the authorized corrections; (11)-(13) do not
  start the boundary-proximity indicator, general JATAKA, or reopen H-04/H-05/H-06/H-08; (14) do not
  weaken any gate; (15) update ADR/decision records and canonical state/handoff files; (16) run the full
  test suite, oracle certification, governance gates, and artifact-drift checks; (17) do not push without
  separate authorization; continue until M-02 reaches its genuine implementation/CI or CEO decision
  checkpoint.
- Relevant ADR/specification: `docs/decisions/DP-019-m02-vimshottari-oracle-boundary-coverage.md`
  sections E (Option 1) and F (the recommendation this ratifies); `docs/DECISION_LOG.md` `ADR-0072` (the
  ratifying entry, containing the full implementation and reasoning record - authoritative over this
  summary); `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` M-02; `engine.transits.crossing.
  find_crossings()` (`TRANSIT_V1`, `ADR-0008`, the already-certified mechanism this implementation uses);
  `ADR-0053`/`ADR-0069`/`ADR-0070`/`ADR-0071` (H-04/H-05/H-06/H-08, not reopened).
- Files changed: `scripts/certify_vimshottari.py` (added `BOUNDARY_HOLDOUT`, `NEAR_BOUNDARY_CASE_IDS`,
  `NEAR_BOUNDARY_THRESHOLD_DEG`; renamed `H10`/`H11`; profile-scoped boundary-case execution; a live
  self-check in `run_case()`; a `near_boundary_coverage` artifact section); `certification/
  VIMSHOTTARI_V1_certification.json`, `reports/certification/vimshottari.report.md`,
  `reports/certification/vimshottari.console.txt` (regenerated); `engine/tests/
  test_vimshottari_m02_boundary_holdout.py` (new, 6 tests); `engine/tests/
  test_vimshottari_certification.py` (pinned row-count updated, test-only); `docs/DECISION_LOG.md`
  (`ADR-0072` appended); `docs/decisions/DP-019-m02-vimshottari-oracle-boundary-coverage.md` (status
  header only, marked ADDRESSED); `docs/decisions/README.md` (`DP-019` row + change history);
  `docs/ACE_EXECUTION_STATE.md` (version 5.6.0); this file.
- Implementation summary: root-found two real nakshatra-boundary crossings via `find_crossings("Moon",
  target, jd_start, jd_end, profile)` - `120` degrees under `PARASHARI_LAHIRI` (nakshatra 9/10) and `240`
  degrees under `KP_KRISHNAMURTI` (nakshatra 18/19), both at sub-microarcsecond residual, in January
  2025. Each crossing sampled at the exact instant and 5 minutes before/after, confirmed (directly, via
  `vimshottari_from_moon()`) to cross a genuine lord change (`Me` -> `Ke` at both). **A genuine
  architectural correction found during implementation, not assumed in advance:** an initial version
  tested every `BOUNDARY_HOLDOUT` case under both certified profiles (mirroring the ordinary `HOLDOUT`'s
  own loop structure) - the certifier's own new self-check immediately and correctly failed
  (`B4_kp_boundary_before: 0.141... deg`, exceeding the `0.1` degree threshold) when a KP-rooted case was
  evaluated under Lahiri's different ayanamsa. Restructured so each boundary case runs only under its own
  tagged native `"profile"`, not both - architecturally correct (Lahiri and Krishnamurti ayanamsa differ
  by a non-trivial constant), not a weakening. `H10_boundary_moon_a`/`H11_boundary_moon_b` renamed to
  `H10_delhi_2025a`/`H11_delhi_2025b`; birth data byte-identical.
- Tests executed and results: `python -m pytest -q` - **837 passed, 0 failed, 0 skipped** (up from 831 by
  exactly the 6 new tests): every `BOUNDARY_HOLDOUT` case confirmed within `0.1` degrees of a nakshatra
  boundary; the two `"_at"` cases confirmed within `0.001` degrees (root-finding precision specifically);
  `"before"`/`"after"` pairs confirmed to land in different, adjacent nakshatras with different
  Vimshottari lords; a genuine negative control reconstructing the *original* `H10_boundary_moon_a`/
  `H11_boundary_moon_b` birth data and confirming it fails the identical threshold the new cases pass;
  the renamed cases confirmed to reproduce their original Moon longitude/boundary distance exactly; the
  `"B"`/`"H"` ID prefixes confirmed structurally disjoint.
- Certification executed and results: `python scripts/certify_vimshottari.py`, run in the isolated
  PyJHora exploration venv - **PASS, lord mismatches: 0** across all 17 cases under their native
  profile(s); the six new cases individually recorded at `0.044009`-`0.044714` degrees (before/after) and
  `0.000192`-`0.000193` degrees (at) from the nearest boundary. Structured comparison of the regenerated
  artifact against the previously committed one: `H1_london_1823` through `H9_paris_2350`'s recorded
  results byte-identical (excluding the new, always-present `moon_distance_to_nearest_boundary_deg`
  diagnostic field); the renamed `H10`/`H11` entries carry identical numeric results under their new IDs.
  `python scripts/check_artifact_drift.py` run against the regenerated-but-uncommitted artifact correctly
  flagged exactly the intended changes (`gates.cases.*` length `11 -> 14`, `gates.near_boundary_coverage:
  added`, `gates.oracle_pratyantar_rows_compared: 16038 -> 20412`) and nothing else. The regenerated
  console transcript's Windows-path backslash artifact was corrected to the committed forward-slash
  convention before commit. `python scripts/certify_kp_chain.py` run as an M-03 anti-fitting scan-surface
  sanity check - PASS, only the same class of volatile-field diff, discarded via `git checkout --`, not
  committed (`scripts/certify_vimshottari.py` is outside `engine/`, the default M-03 scan target, so it
  was never in the scan surface).
- Governance checks executed and results: `python scripts/check_adr_numbering.py` (**72 ADR entries, up
  from 71**), `python scripts/check_identifier_families.py` (19 DP identifiers, unchanged),
  `python scripts/check_retired_identifiers.py`, `git diff --check` - all PASS.
- Known issues / related finding, explicitly not acted on: a repository-wide search found the same
  `H10_boundary_moon_a`/`H11_boundary_moon_b` birth data and ID convention reused as a "boundary_
  sensitive" holdout case in at least eight other certifiers/validators (`certify_trikalam.py`,
  `certify_panchanga.py`, `certify_rise_set.py`, `certify_tier0.py`, `certify_kp_chain.py`,
  `certify_parashari_drishti.py`, `certify_current_engine.py`, `engine/tests/test_kp_chart.py`). Whether
  those are similarly mislabeled relative to their own domain-specific "boundary" claims (sunrise/sunset
  instant, tithi/yoga boundary, etc. - different quantities from nakshatra-longitude distance) was **not**
  investigated - `DP-019`'s evidence base and this ratification are scoped strictly to the Vimshottari
  oracle gate. Recorded in `ADR-0072` as a candidate for a future, separate decision paper; not acted on
  here to avoid an unauthorized scope expansion.
- Unresolved questions: whether the flagged cross-certifier "H10/H11" mislabeling pattern warrants its
  own future investigation and decision paper.
- CEO decision required: none to close out this task. The next genuine decision point is authorizing the
  dasha boundary-proximity indicator (the roadmap's final step) or a different task, authorizing a push
  of this task's commit, or deciding whether to investigate the flagged cross-certifier finding.
- Next authorized action: none self-executable. Per the owner's own closing instruction, stop here and
  await the next genuine CEO decision, blocker, or push-authorization checkpoint.

### 2026-08-22 - Pushed 19dbc6b (H-08, ADR-0071), CI-confirmed (run 32572406495); DP-019 drafted: M-02 decision-readiness only
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the DP-019 paper
  and state-file updates, on top of `19dbc6b`).
- Previous approved commit: `19dbc6bcd7c5260e2d03daf1864836407853b2bc` (H-08 implementation, `ADR-0071`) -
  now pushed and CI-confirmed (this task's first half). `main` (via PR #3, merge commit `0e1ef11`) is
  unaffected by this task.
- Task, part 1 (push authorization): "Approve push of H-08 commit 19dbc6bcd7c5260e2d03daf1864836407853b2bc.
  Push only this H-08 commit to origin/phase-g-governance. Do not push or commit any unrelated/untracked
  files. Do not start M-02. Do not start the dasha boundary-proximity indicator. Do not begin Jataka
  implementation. After pushing: verify origin/phase-g-governance exactly matches the pushed commit; wait
  for CI; inspect the actual CI logs, not merely the checkmarks; confirm all relevant test, governance,
  oracle/certification and artifact-drift gates; confirm the H-08 disclosure and six-boundary tests
  actually execute in CI; confirm no certified-value changes; report the exact CI run and final repository
  state; stop at the next genuine decision point."
- Push executed: `git push origin phase-g-governance` - fast-forward `cc02f37..19dbc6b`, carrying the two
  commits accumulated since the last push (`badf2cc`, `19dbc6b`); no untracked files touched (untracked
  files never travel with a push regardless). Verified `origin/phase-g-governance` == local HEAD ==
  `19dbc6bcd7c5260e2d03daf1864836407853b2bc`, both directions, via `git fetch` + `git rev-parse`.
- CI run **`32572406495`** (headSha `19dbc6b`) - **all four jobs green**, read directly from the log
  transcript: `oracle gate (PyJHora, hash-pinned)` - `lord mismatches: 0`; drift-assertion step `PASS: 46
  evidence file(s) identical to the committed version outside the volatile fields`, confirming CI's own
  independent PyJHora regeneration reproduces the committed certification artifact **including the new
  H-08 `explicit_non_claims` entry**. `no-oracle gate (3.11)` and `(3.12)` - `831 passed` on each (up
  from 825, matching exactly the six new tests in `test_vimshottari_h08_boundary_convention.py`, the only
  test file this commit added), plus a network-guard re-run subset also `831 passed` on each, plus drift
  PASS on each. `governance gate` - `71 ADR entries`, `18 DP identifiers` (at commit time), status-header
  and varga-registry checks all PASS. Working tree confirmed clean of all tracked changes post-push; the
  same pre-existing, unrelated untracked items remain untouched.
- **H-08 is now CI-confirmed, closing the task's first half.** No certified-value change: every
  calculated figure in the oracle-gate output (lord mismatches, tolerances, cases) is identical to
  before; the only non-volatile content difference anywhere is the intended `explicit_non_claims`
  disclosure line.
- Task, part 2 (M-02 decision-readiness): "Authorize M-02 decision-readiness as the next Dasha/
  Jataka-entry prerequisite," with the current verified state restated (FOUNDATION exited; `phase-g-
  governance` merged to `main`; H-04/H-05/H-06/H-08 closed, H-08 CI-confirmed at `19dbc6b`, CI run
  `32572406495` green; the Dasha roadmap's remaining items are M-02 then the dasha boundary-proximity
  indicator; JATAKA unauthorized) and an explicit twenty-two-item scope: verify branch/HEAD/origin/
  working-tree state; read `ACE_EXECUTION_STATE.md`/`AI_HANDOFF_CURRENT.md`; read `Q8_CLOSURE_MATRIX.md`
  s5; read the complete `DASHA_CERTIFICATION_ROADMAP.md`; locate and inspect every M-02 reference;
  independently reproduce the M-02 finding rather than relying on the roadmap summary; establish the
  exact problem and its evidence; classify it precisely (defect/certification gap/oracle-holdout gap/
  governance gap/boundary-coverage gap/other); determine whether existing certified Vimshottari values
  are affected; identify the legitimate options; determine blast radius and certification consequences
  for each; check H-04/H-05/H-06/H-08 as precedents without blindly applying them; recommend an option
  only if the evidence supports one; draft a narrow decision paper; do not select/ratify; do not
  implement M-02 yet; do not start the boundary-proximity indicator; do not begin general JATAKA; do not
  reopen FOUNDATION or any closed Dasha item; do not weaken any gate; preserve historical state; do not
  push without separate authorization.
- Relevant ADR/specification: `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` M-02 (the primary finding,
  re-read and independently re-verified in full, including its exact reported distances); `docs/
  DASHA_CERTIFICATION_ROADMAP.md` step 5 (re-read in full, still `Status: PROPOSED`); `scripts/
  certify_vimshottari.py`'s `HOLDOUT` list (the two mislabeled cases and the other nine, all measured
  directly); `engine.transits.crossing.find_crossings()` (`TRANSIT_V1`, `ADR-0008` - the already-certified
  mechanism verified live for Option 1's feasibility); `docs/KP_CHAIN_SPEC.md` and `docs/
  ACE_EXECUTION_STATE.md`'s own change history (the `KP_CHAIN_V1`/`TRIKALAM_V1` boundary-battery
  precedent, found by inspection rather than named by the owner's list); `docs/decisions/
  DP-015-foundation-boundary-proximity-indicators.md` (cites M-02 as supporting evidence for a distinct,
  not-reopened FOUNDATION-scope item); `ADR-0053`/`ADR-0069`/`ADR-0070`/`ADR-0071` (H-04/H-05/H-06/H-08,
  checked as precedents per the owner's own item 12, not reopened).
- Files changed: `docs/decisions/DP-019-m02-vimshottari-oracle-boundary-coverage.md` (new), `docs/
  decisions/README.md` (`DP-019` registered before drafting, per `ADR-0040`), `docs/ACE_EXECUTION_
  STATE.md` (version 5.5.0), this file.
- **Pre-work performed exactly as mandated:** confirmed branch `phase-g-governance`, local HEAD ==
  `origin/phase-g-governance` == `19dbc6b`, working tree clean of tracked changes, `origin/main` at
  `0e1ef11` unchanged. Read `Q8_CLOSURE_MATRIX.md` s5 fresh. Read `docs/DASHA_CERTIFICATION_ROADMAP.md`
  in full - its own section 5 step 5 names "near-boundary Moon cases to the oracle gate, closing M-02" as
  the required action. Inspected, directly, not from memory: `scripts/certify_vimshottari.py`'s full
  `HOLDOUT` list and `run_case()`/`main()` methodology; `engine/tests/
  test_vimshottari_hermetic_baseline.py` and `test_vimshottari_h08_boundary_convention.py` (confirming
  neither contains a realistic, ephemeris-derived near-boundary case - H-05's cases are anchor-JD
  regression coverage, H-08's are synthetic exact-boundary floats no real ephemeris Moon lands on);
  `certification/VIMSHOTTARI_V1_certification.json`'s `explicit_non_claims` (confirmed it does not
  disclose the missing near-boundary coverage); `docs/decisions/DP-015-*.md` (confirming it cites M-02 as
  supporting evidence for a distinct roadmap item, without resolving M-02 itself). Searched `docs/
  DECISION_LOG.md` and `docs/decisions/` for prior M-02 work: zero hits before this paper beyond that one
  citation.
- **Independent reproduction, not trusted from the audit's own summary:** computed the sidereal Moon
  longitude for `H10_boundary_moon_a` and `H11_boundary_moon_b` through the same `engine.calculations.
  calculations.calculate()` path the certifier itself uses, then their distance to the nearest nakshatra
  boundary - **6.4587 and 5.0197 degrees**, matching the audit's "6.46 degrees and 5.0 degrees" exactly.
  Computed the same distance for all nine other holdout cases (`H1`-`H9`) - every one is closer to a
  boundary than `H10`; eight of the nine are closer than `H11` too (only `H6_quito_2010` at 5.5014 degrees
  is farther than `H11`, though still closer than `H10`) - independently confirming "both are farther
  from a boundary than a case not labelled as one," not merely accepting the audit's own count.
  Additionally verified Option 1's technical feasibility live, not merely proposed it: `find_crossings(
  "Moon", NAK_SPAN * 5, jd_start, jd_end, PARASHARI_LAHIRI)` over a one-month window located one real
  crossing at `residual_arcsec` ~1.0e-6 - confirming this already-certified `TRANSIT_V1` mechanism can
  root-find a genuine near-boundary Moon instant to sub-microarcsecond precision, at low, additive,
  test/certifier-script-only blast radius.
- Implementation summary (no code touched - decision-paper drafting only): registered `DP-019` in `docs/
  decisions/README.md`'s index first, per `ADR-0040`, then drafted it, structured to match this session's
  established DP template (sections 1, 2, A-H, change history). **Section A** (exact problem): the two
  cases named "boundary_moon" are 6.46/5.02 degrees from any boundary - farther than most ordinary cases
  - so the oracle gate has zero genuine near-boundary coverage despite claiming it. **Section B**
  (classification): primarily an oracle/holdout coverage gap, with a secondary label-accuracy defect -
  not a calculation defect; the certified computation itself is not implicated. **Section C**: no existing
  certified value is affected under any option. **Section D**: explicitly checked H-04 (closest in kind:
  a missing-but-designed gate), H-05 (closest in remedy shape, but hermetic-only, found insufficient for
  M-02's oracle-gate-specific wording), H-06/H-08 (procedural precedent only), and identified `KP_CHAIN_
  V1`/`TRIKALAM_V1`'s own boundary-battery methodology as the more directly applicable shape - found by
  inspecting the codebase, not named by the owner's list. **Section E** presents four options: Option 1
  (root-find genuine cases via `find_crossings()`, correcting the mislabeled cases as part of the same
  work); Option 2 (hermetic-only, faster but does not satisfy the oracle-gate-specific wording); Option 3
  (label-fix only, defer genuine coverage); Option 4 (defer entirely). **Section F** recommends Option 1
  at medium-high confidence, with Option 3's label correction folded into it rather than pursued
  separately. Section G explicitly confirms the dasha boundary-proximity indicator, JATAKA, `DP-015`, and
  every already-closed Dasha item are untouched and not reopened.
- Tests executed and results: none run for this decision-paper-only task (no code touched); the
  reproduction above (boundary-distance measurement, `find_crossings()` feasibility check) was
  interactive verification, not a committed test. Full test suite last confirmed at 831/831 as part of
  the immediately preceding H-08 push/CI-confirmation (this task's own first half).
- Certification executed and results: none - no code or certification artifact touched this task.
- Governance checks executed and results: `python scripts/check_adr_numbering.py` (71 ADR entries,
  unchanged), `python scripts/check_identifier_families.py` (**19 registered DP identifiers, up from
  18**, no unregistered tokens), `python scripts/check_retired_identifiers.py`,
  `python -m pytest engine/tests/test_retired_identifier_gate_scope.py -q` (36 passed, confirming no
  repeat of the placeholder-identifier issue found in the previous task) - all PASS.
- Known issues: none. The distinction between M-02 (this paper) and the dasha boundary-proximity
  indicator (a separate, later roadmap step that `DP-015` also cites M-02 alongside) is recorded
  explicitly in the paper itself to prevent future conflation.
- Unresolved questions: which of `DP-019`'s four options the owner selects for M-02; if Option 1, how
  many boundaries/offsets to sample and what becomes of `H10`/`H11`'s names.
- CEO decision required: select `DP-019`'s Option 1, 2, 3, or 4 for M-02.
- Next authorized action: none self-executable. Per the owner's own closing instruction, continue until
  the genuine M-02 CEO decision point - reached here; awaiting the owner's option selection.

### 2026-08-22 - ADR-0071 ratifies DP-018 Option 3: status quo ratified + seed_boundary_convention disclosure field + pinning test (H-08 CLOSED)
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the H-08
  implementation, on top of `badf2cc`).
- Previous approved commit: `badf2ccb9338e740a8ad54551f35114bb63de56b` (`DP-018` drafted, H-08
  decision-readiness) - unpushed, together with `cc02f37` (H-06, pushed and CI-confirmed) beneath it.
  `main` (via PR #3, merge commit `0e1ef11`) is unaffected by this task.
- Task (owner's exact instruction): "CEO DECISION — DP-018 H-08. Ratify DP-018 Option 3: Ratify the
  existing H-08 boundary convention/status quo and add the proposed additive disclosure field/
  documentation exactly as specified by DP-018 Option 3." Decision intent: (1) preserve existing
  certified numerical behaviour; (2) do not change Parashari seeding; (3) do not alter the KP `[start,
  end)` boundary rule; (4) pin the existing convention explicitly; (5) add the additive disclosure/
  provenance field following the `ADR-0065` H-02 precedent; (6) make the known six-boundary seam explicit
  rather than silently implying equivalence between the school conventions; (7) do not treat the seam as
  a calculation defect; (8) do not reopen H-05 or H-06; (9) do not weaken any certification gate; (10) do
  not defer H-08; (11) do not begin M-02, the boundary-proximity indicator, or general JATAKA yet.
  Implementation must remain additive and must not change existing certified values. Resolve only the
  implementation details necessary to implement Option 3 exactly as written, recording rationale and
  provenance; update the ADR/decision record; add tests; verify certified values unchanged; run
  certification/regression tests; run governance gates; update state/handoff records; determine H-08
  closure status; do not push without separate authorization.
- Relevant ADR/specification: `docs/decisions/DP-018-h08-parashari-dasha-boundary-convention.md` sections
  C (Options 1 and 3) and G (the recommendation this ratifies); `docs/DECISION_LOG.md` `ADR-0071` (the
  ratifying entry, containing the full implementation and reasoning record - authoritative over this
  summary); `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` H-08; `ADR-0065` (the `TransitEvent.
  declared_division` H-02 precedent this field mirrors); `ADR-0053`/`ADR-0069`/`ADR-0070` (H-04/H-05/H-06,
  not reopened).
- Files changed: `engine/models/dasha.py` (added `SEED_BOUNDARY_CONVENTION_KP_EXACT` and
  `VimshottariTimeline.seed_boundary_convention`); `engine/dasha/vimshottari.py` (import, explicit field
  population at the one construction site, H-08 docstring paragraph); `engine/tests/
  test_vimshottari_h08_boundary_convention.py` (new, 6 tests); `scripts/certify_vimshottari.py`
  (`explicit_non_claims` gained one entry); `certification/VIMSHOTTARI_V1_certification.json`,
  `reports/certification/vimshottari.report.md`, `reports/certification/vimshottari.console.txt`
  (regenerated to reflect the `explicit_non_claims` addition; console-txt's Windows path-separator
  quirk corrected to match the committed convention before commit); `docs/DECISION_LOG.md` (`ADR-0071`
  appended); `docs/decisions/DP-018-h08-parashari-dasha-boundary-convention.md` (status header updated,
  plus one placeholder-identifier correction the governance hook caught); `docs/decisions/README.md`
  (`DP-018` row + change history); `docs/ACE_EXECUTION_STATE.md` (version 5.4.0); this file.
- Implementation summary: `SEED_BOUNDARY_CONVENTION_KP_EXACT = "kp_exact_start_end"` is a named constant
  in `engine/models/dasha.py`, fully documented (what it means, why it is the only value today, where
  the six known divergent boundaries are pinned, cross-referencing `ADR-0071`). `VimshottariTimeline`
  gained `seed_boundary_convention: str = SEED_BOUNDARY_CONVENTION_KP_EXACT` - defaulted (matching
  `ADR-0065`'s own `declared_division: int | None = None` pattern), appended last in field order (valid
  dataclass ordering since no field follows it without a default), but still passed explicitly at the
  one real production construction site in `vimshottari_from_moon()`, matching this file's existing style
  of never relying on defaults at the actual call site. No classification or arithmetic logic touched -
  `_to_exact()`, the KP `[start, end)` rule, and Parashari seeding are all byte-for-byte unchanged.
  `scripts/certify_vimshottari.py`'s `explicit_non_claims` gained one entry naming the seam explicitly by
  H-08/`ADR-0071`, cross-referencing the new field and the new test file - closing the documentation gap
  `DP-018` identified (unlike H-06's own artifact, this one had not already disclosed the seam).
- Tests executed and results: `python -m pytest -q` - **831 passed, 0 failed, 0 skipped** (up from 825
  by exactly the 6 new tests in `test_vimshottari_h08_boundary_convention.py`): exactly the six
  previously-reproduced boundary floats (`k = 7, 11, 14, 17, 22, 25`) diverge from `engine.astrology.
  nakshatra.nakshatra()`, satisfying the audit's own "Tests required" line directly; each divergence is
  off by exactly one nakshatra; the other 21 boundary floats still agree exactly (a negative control on
  the pin itself, proving the first assertion is not vacuous); a genuine negative control -
  `monkeypatch` sets `engine.astrology.longitude_utils.BOUNDARY_TOLERANCE` to `0.0` mid-test, confirms
  the divergent set changes from the pinned six (verified this session: to `{17}` alone), then restores
  and re-confirms the pinned six - proving the pin would actually catch a real convention change, not
  merely describe today's numbers; the new `seed_boundary_convention` field is present and explicit on
  timelines from all three call shapes (`vimshottari_from_moon()` directly, `vimshottari_parashari()`,
  `vimshottari_kp()`), confirming it is independent of which school seeded the timeline; H-05's own frozen
  baseline (`ADR-0069`) reproduces exactly, unchanged.
- Certification executed and results: `python scripts/certify_vimshottari.py`, run in the isolated
  PyJHora exploration venv - **PASS, lord mismatches: 0, max start delta: 1.86e-09 days, oracle moon
  delta: 0.745776 arcsec max**, every calculated figure identical to the pre-existing certified evidence.
  `python scripts/check_artifact_drift.py` run against the regenerated-but-uncommitted artifact correctly
  flagged exactly one non-volatile change - `explicit_non_claims: length 4 -> 5` - and nothing else,
  confirming the change is exactly and only the intended, now-recorded disclosure addition. The
  regenerated console transcript's Windows-path backslash artifact was corrected to the committed
  forward-slash convention before commit, matching the same understood cross-platform quirk documented
  in `ADR-0069`'s and `ADR-0070`'s own evidence sections. `python scripts/certify_kp_chain.py` run as an
  M-03 anti-fitting scan-surface sanity check - PASS, only the same class of volatile-field diff,
  discarded via `git checkout --`, not committed.
- Governance checks executed and results: `python scripts/check_adr_numbering.py` (**71 ADR entries, up
  from 70**), `python scripts/check_identifier_families.py` (18 DP identifiers, unchanged),
  `python scripts/check_retired_identifiers.py`, `git diff --check` - all PASS. One genuine violation was
  caught and fixed mid-task: the repository's `PostToolUse` governance hook (which runs `check_retired_
  identifiers.py` after every edit to `docs/DECISION_LOG.md`) flagged a placeholder token (`ADR-` followed
  by a non-4-digit placeholder) that had been sitting in `DP-018`'s own already-committed text since the
  prior task, plus a copy of it introduced into the new `ADR-0071` entry's own prose describing that fix -
  both corrected to non-identifier-shaped prose (a mechanical correction, not a substantive edit to any
  option, evidence claim, or recommendation), then all gates re-run clean.
- Known issues: none. The Windows-path console-transcript quirk is understood and not a defect, per this
  session's established precedent.
- Unresolved questions: none for H-08. M-02 (near-boundary Moon oracle cases) and the dasha
  boundary-proximity indicator remain open, each requiring its own separate owner authorization per the
  roadmap's established per-step order this session has followed throughout. M-01 (the sibling, not-in-
  scope KP-layer pinning-test finding) remains open and unaddressed, as before this task.
- CEO decision required: none to close out this task. The next genuine decision point is authorizing
  M-02 or the dasha boundary-proximity indicator (or a different task), or authorizing a push of this
  task's commit.
- Next authorized action: none self-executable. Per the owner's own closing instruction, stop here and
  await the next genuine CEO decision, blocker, or push-authorization checkpoint.

### 2026-08-22 - Pushed cc02f37 (H-06, ADR-0070), CI-confirmed (run 32571001995); DP-018 drafted: H-08 decision-readiness only
- Branch / commit SHA: `phase-g-governance`, see `git log -1` (this entry commits with the DP-018 paper
  and state-file updates, on top of `cc02f37`).
- Previous approved commit: `cc02f370203f8b11b85688b3c33da2247eb0b5cf` (H-06 implementation, `ADR-0070`) -
  now pushed and CI-confirmed (this task's first half). `main` (via PR #3, merge commit `0e1ef11`) is
  unaffected by this task.
- Task, part 1 (push authorization): "Approve push of H-06 commit cc02f370... Push only this H-06 commit
  to origin/phase-g-governance. Do not push or commit the unrelated untracked files. Do not start H-08
  yet. After pushing: verify remote SHA; wait for CI; verify all CI jobs and relevant logs; confirm H-06
  is CI-confirmed; confirm working tree state; report the exact CI run and resulting state."
- Push executed: `git push origin phase-g-governance` - fast-forward `76ed443..cc02f37`, carrying the four
  commits accumulated since the last push (`bf66e48`, `0802247`, `e133413`, `cc02f37`); no new commits
  created, no untracked files touched (untracked files never travel with a push regardless). Verified
  `origin/phase-g-governance` == local HEAD == `cc02f370203f8b11b85688b3c33da2247eb0b5cf`, both directions,
  via `git fetch` + `git rev-parse`.
- CI run **`32571001995`** (headSha `cc02f37`) - **all four jobs green**, read directly from the log
  transcript, not inferred from the checkmark: `oracle gate (PyJHora, hash-pinned)` - `lord mismatches: 0`;
  drift-assertion step `PASS: 46 evidence file(s) identical to the committed version outside the volatile
  fields (18 machine-readable, 28 rendered)`. `no-oracle gate (3.11)` - `825 passed in 27.88s`; all
  fourteen independent holdout validators PASSED, including `RESULT: ALL INDEPENDENT VIMSHOTTARI CASES
  PASSED`. `no-oracle gate (3.12)` - `825 passed` (initial run) and `825 passed` again (network-guard
  re-run subset); same drift-check PASS. `governance gate` - identifier-family conformance clean. Working
  tree confirmed clean of all tracked changes post-push; the 27 pre-existing, unrelated untracked items
  (bundles, `.codex/`, `AGENTS.md`, misc scripts/reports) remain exactly as before, untouched.
- **H-06 is now CI-confirmed, closing the task's first half.**
- Task, part 2 (H-08 decision-readiness): "Authorize H-08 decision-readiness as the next Dasha/
  Jataka-entry prerequisite," with the current verified state restated (FOUNDATION exited under
  `ADR-0068`; `phase-g-governance` merged to `main` via PR #3; H-04/H-05/H-06 closed, H-06 CI-confirmed at
  `cc02f37`, CI run `32571001995` green) and an explicit twenty-item scope: verify branch/HEAD/working-
  tree/remote state; read `ACE_EXECUTION_STATE.md`/`AI_HANDOFF_CURRENT.md`; read `Q8_CLOSURE_MATRIX.md`
  s5; read the complete `DASHA_CERTIFICATION_ROADMAP.md`; inspect every existing H-08 reference/evidence/
  code/tests/certification/prior decision; independently establish the exact problem; classify it
  precisely (defect/certification gap/governance gap/convention ambiguity/missing protection/other);
  determine all legitimate options; determine blast radius and certified-value impact; identify any
  interaction with H-05/H-06 without reopening them; recommend an option only if the evidence supports
  one; draft a narrow decision paper; do not choose/ratify; do not implement H-08 yet; do not start M-02
  or the dasha boundary-proximity item; do not begin general JATAKA; do not reopen FOUNDATION; preserve
  all certification gates; update canonical state/handoff records preserving historical state; do not
  push without separate authorization.
- Relevant ADR/specification: `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` H-08 (the primary finding,
  re-read and independently re-verified in full, including its exact reported cardinality); `docs/
  DASHA_CERTIFICATION_ROADMAP.md` step 4 (re-read in full, still `Status: PROPOSED`); `engine/astrology/
  nakshatra.py`/`longitude_utils.py` (the Parashari engine's own classifier and its `1e-10` tolerance-
  promotion convention); `engine/kp/intervals.py` (the KP layer's exact `[start, end)` rule, `ADR-0006`);
  `docs/KP_CHAIN_SPEC.md` s7 (the related but distinct M-01 promise, not addressed here); `ADR-0065`
  (H-02's `declared_division` additive-disclosure precedent, cited as a candidate pattern for Option 3);
  `ADR-0053`/`ADR-0069`/`ADR-0070` (H-04/H-05/H-06, not reopened).
- Files changed: `docs/decisions/DP-018-h08-parashari-dasha-boundary-convention.md` (new), `docs/
  decisions/README.md` (`DP-018` registered before drafting, per `ADR-0040`), `docs/ACE_EXECUTION_
  STATE.md` (version 5.3.0), this file.
- **Pre-work performed exactly as mandated:** confirmed branch `phase-g-governance`, local HEAD ==
  `origin/phase-g-governance` == `cc02f37`, working tree clean of tracked changes, `origin/main` at
  `0e1ef11` unchanged. Read `Q8_CLOSURE_MATRIX.md` s5 fresh (JATAKA entry criteria explicitly names "the
  H-08 convention decision" as one of six required steps). Read `docs/DASHA_CERTIFICATION_ROADMAP.md` in
  full - its own section 5 step 4 states H-08 is "an owner decision about which convention a
  Parashari-seeded dasha follows, not a builder choice," the direct source for this paper's framing.
  Inspected, directly, not from memory: `engine/dasha/vimshottari.py`'s `_to_exact()` (the KP-style exact
  `Decimal(str(x))` conversion, used unconditionally regardless of seeding school); `engine/astrology/
  nakshatra.py` and `longitude_utils.py` (the Parashari engine's own `1e-10`-degree tolerance-promoted
  `division_index()` rule, a deliberately different convention for a different purpose - absorbing
  ephemeris float noise, per F-04/A-3 remediation); `engine/kp/intervals.py` (confirming the identical
  exact-boundary rule and its own separate, deliberate justification under `Decision KP-A`/`D-003`);
  `engine/tests/test_vimshottari_consistency.py` in full (confirming `test_seed_agrees_with_certified_
  kp_chain_everywhere()`'s own docstring locks in today's cross-school behaviour as deliberate, and that
  its sibling off-boundary test never checks agreement with the Parashari classifier at or near a
  boundary); `certification/VIMSHOTTARI_V1_certification.json`'s `explicit_non_claims` (confirmed it does
  NOT disclose this seam - a materially different starting position from H-06's own artifact); `docs/
  KP_CHAIN_SPEC.md` s7 (confirming M-01 is a related but distinct, not-in-scope finding); `engine/models/
  dasha.py` (confirming `VimshottariTimeline` has no field recording which boundary convention produced
  the seed classification - the same structural absence `ADR-0065` remedied for H-02). Searched `docs/
  DECISION_LOG.md` and `docs/decisions/` for prior H-08 work: zero hits before this paper (only citations
  noting it remains open).
- **Independent reproduction, not trusted from the audit's own summary:** iterated `moon = float(NAK_SPAN
  * k)` for `k` in `0..26` (the literal boundary floats, exactly the construction the existing
  cross-layer test already uses) and compared `nakshatra(moon)` against `vimshottari_from_moon(moon,
  ...).seed_nakshatra_number` for each - **exactly six mismatches**, at `k = 7, 11, 14, 17, 22, 25`
  (longitudes 93.333..., 146.666..., 186.666..., 226.666..., 293.333..., 333.333... degrees), matching the
  audit's own reported cardinality exactly, not merely a plausible re-derivation. Additionally ran a
  broader synthetic probe (a fixed tiny offset below every one of the 26 non-zero boundaries) which showed
  all 26 diverge - clarifying that the audit's "six" figure is about which naturally-occurring
  `float(k * 360/27)` spellings happen to fall inside the `1e-10` promotion window, not a claim that only
  six boundaries are structurally at risk.
- Implementation summary (no code touched - decision-paper drafting only): registered `DP-018` in `docs/
  decisions/README.md`'s index first, per `ADR-0040`, then drafted it, structured to match this session's
  established DP template (sections 1, 2, A-I, change history). **Section A** (exact problem):
  `vimshottari_from_moon()` uses the KP exact-boundary rule for every school; the Parashari classifier
  uses a materially different rule; six specific floats diverge, changing the seed nakshatra and therefore
  the entire mahadasha sequence for Parashari-seeded timelines. **Section B** (classification): a
  convention ambiguity across a school-isolation seam, combined with a documentation gap (mirroring the
  audit's own framing exactly) and a test-coverage gap - not a calculation defect, and (per the audit's
  own statement) not currently a certification gap in the unverified-claim sense, since nothing certified
  currently promises cross-classifier boundary agreement. **Section C** presents four options: Option 1
  (ratify the status quo explicitly, document + pin, zero certified-value impact - matches the audit's own
  proposed solution almost exactly); Option 2 (make Parashari seeding follow its own engine's classifier,
  a genuine narrow certified-value change requiring PyJHora oracle re-verification before certification,
  not yet investigated); Option 3 (Option 1 plus an additive convention-disclosure field on
  `VimshottariTimeline`, directly mirroring `ADR-0065`'s own `declared_division` precedent for the
  structurally identical H-02 seam); Option 4 (defer - assessed as having a weak cost/benefit case, since
  Option 1 is nearly free and `Q8_CLOSURE_MATRIX.md` s5's own wording gives no carve-out opening, matching
  `DP-016`/`DP-017`'s own prior finding on that point). **Section G** recommends Option 1 or its Option 3
  enhancement at medium-high confidence - stronger than `DP-017`'s own H-06 lean, since H-08's zero-impact
  option leaves almost no open design question, unlike H-06's two genuinely open sub-questions. Section H
  explicitly confirms H-05/H-06/M-02/dasha-boundary-proximity/JATAKA/FOUNDATION are untouched and not
  reopened.
- Tests executed and results: none run for this decision-paper-only task (no code touched); the
  reproduction above was interactive verification, not a committed test. Full test suite last confirmed
  at 825/825 as part of the immediately preceding H-06 push/CI-confirmation (this task's own first half).
- Certification executed and results: none - no code or certification artifact touched this task.
- Governance checks executed and results: `python scripts/check_adr_numbering.py` (70 ADR entries,
  unchanged), `python scripts/check_identifier_families.py` (**18 registered DP identifiers, up from 17**,
  no unregistered tokens), `python scripts/check_retired_identifiers.py` - all PASS.
- Known issues: none. The distinction between H-08 (this paper) and M-01 (the sibling, not-in-scope
  KP-layer pinning-test promise) is recorded explicitly in the paper itself to prevent future conflation.
- Unresolved questions: which of `DP-018`'s four options the owner selects for H-08; whether Option 3's
  additive disclosure field is worth its slightly larger blast radius if Option 1 alone is chosen.
- CEO decision required: select `DP-018`'s Option 1, 2, 3, or 4 for H-08.
- Next authorized action: none self-executable. Per the owner's own closing instruction, continue until
  the genuine H-08 CEO decision point - reached here; awaiting the owner's option selection.

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
| 8.1.0 | 2026-08-24 | **CI-run-ID discrepancy resolved (no fabrication); `main`-vs-`phase-g-governance` merge-readiness audit performed (READY, not performed).** Independent audit flagged this session's chat citation of CI run `32756205364` vs committed records citing only `32752248185`. Resolved by direct `gh run view` query: both runs genuine and `success` - `32752248185` -> `f0eb220` (16:41 UTC), `32756205364` -> `931b6d0` (17:22 UTC, later, current HEAD). Root cause: `ACE_EXECUTION_STATE.md`'s snapshot fields were never updated after the `931b6d0` push; `32756205364` had only been reported in chat, never committed. Corrected via the file's own designed overwrite mechanism, `ADR-0074` left unedited (its own citation was accurate when drafted). Merge-readiness audit: confirmed `main`'s merge-commit second parent is an ancestor of current `phase-g-governance` (no lost content, normal continued-branch topology); `main` has no independent work beyond its own two historical merges; `git merge-tree` reports a clean, conflict-free merge; all 13 ahead-of-main commits individually ratified; zero JATAKA production code found; no PR currently open. Result: READY. **No merge performed, no PR created, no self-authorization taken.** No code touched. Governance gates clean (74 ADR entries). H-03, the eight cross-certifier findings, and all closed Dasha/FOUNDATION items untouched. No JATAKA implementation begun. |
| 8.0.0 | 2026-08-24 | **`ADR-0074` RATIFIED — JATAKA ENTRY CRITERIA FORMALLY SATISFIED, JATAKA ENTERED.** Owner: "CEO RATIFICATION — ADR-0074. I ratify ADR-0074 exactly as written in commit 2f26eee. I formally declare the JATAKA entry criteria satisfied under Q8_CLOSURE_MATRIX.md s5," individually confirming all ten items enumerated (FOUNDATION prerequisite satisfied; all six Dasha-roadmap steps satisfied and individually ratified; H-03 not a JATAKA-entry prerequisite; the eight `ADR-0072` cross-certifier findings non-blocking; the "six steps, not the roadmap document" interpretation ratified; the stale header confirmed non-blocking; phase entry only; every JATAKA capability still needs its own authorization; implementation not begun). Recorded via the established "Ratification of ADR-<number>" mechanism, mirroring `ADR-0068`'s own FOUNDATION-exit ratification exactly - Status line only edited, a new follow-up sub-entry added. `CURRENT_PHASE` updated to JATAKA ENTERED. No code touched; 844/844 pytest unchanged; governance gates clean (74 ADR entries). No JATAKA capability implementation begun; no closed Dasha or FOUNDATION item reopened; the eight cross-certifier findings untouched; the stale register-header summary left unfixed. Nothing pushed. |
| 7.9.0 | 2026-08-24 | Pushed `f0eb220` (Dasha roadmap step 6, `ADR-0073`) to `origin/phase-g-governance` on explicit push authorization - fast-forward `d18e7ff..f0eb220`. CI run `32752248185`: all four jobs green, read directly from the log (governance gate clean; both no-oracle legs 844 passed, confirming the 7 new boundary-proximity tests executed; oracle gate 0 lord mismatches, 20412 rows, drift PASS). **Full six-step Dasha roadmap fully CI-confirmed, zero certified-value impact.** Owner then authorized a formal JATAKA-entry readiness audit. Drafted `ADR-0074` (`Status: PROPOSED`, not self-ratified, mirroring `ADR-0068`'s own precedent): independently reverified all six Dasha-roadmap ADRs' own `Status` fields directly - all `ACCEPTED`. `Q8_CLOSURE_MATRIX.md` s5's entry-criteria text found satisfied on its own plain terms. Searched for H-03: confirmed genuinely absent from JATAKA's entry criteria and the Dasha roadmap - a separate, still-open `TRANSIT_V1` finding, not invented as a requirement. Reconciled the eight `ADR-0072` cross-certifier findings: confirmed non-blocking, remain untouched. Confirmed no accidental JATAKA implementation (`planet_strength.py` is pre-Phase-G legacy code). Flagged, not fixed, a stale `DECISION_LOG.md` register-header summary. Presented the Dasha-roadmap-document's own unratified status as an explicit textual point. Determination: entry criteria satisfied; a separate CEO entry decision is the only remaining authorization. No code touched; 844/844 pytest unchanged; governance gates clean (74 ADR entries). No JATAKA implementation begun; no closed Dasha or FOUNDATION item reopened; the eight cross-certifier findings untouched. |
| 7.8.0 | 2026-08-24 | **`ADR-0073` ratifies `DP-020` Option 1 - DASHA ROADMAP FULLY CLOSED (all six steps).** Added `VimshottariTimeline.seed_nakshatra_boundary_arcsec`, an exact re-expression of the already-computed `elapsed` fraction (zero new astronomical calculation), deliberately scoped narrower than KP's own `nearest_boundary_arcsec` (nakshatra/seed boundary only) after independently reproducing that field's own unresolved completeness defect (H-07) live. 7 new hermetic tests including a genuine negative control (`NAK_SPAN` monkeypatched, pinned value changes). `certify_vimshottari.py` gained a real per-case self-check plus a new `boundary_proximity_indicator` artifact section. Zero certified-value impact verified via structured before/after comparison and `check_artifact_drift.py`. 844/844 pytest (up from 837). Governance gates clean (73 ADR entries). `Q8_CLOSURE_MATRIX.md` s5's JATAKA entry-criteria text is now satisfied on its own plain terms - general JATAKA implementation is NOT thereby authorized, still requires its own separate authorization. H-04/H-05/H-06/H-08/M-02/`DP-015`/FOUNDATION not touched; the eight flagged cross-certifier findings untouched. Nothing pushed. |
| 7.7.0 | 2026-08-24 | Pushed `d18e7ff` (M-02 CI-fix) to `origin/phase-g-governance` on explicit push authorization - fast-forward `53ec25e..d18e7ff`. CI run `32711122102`: all four jobs green, read directly from the log (governance gate clean; both no-oracle legs 837 passed including `Near-boundary cases: 216 PASSED`; oracle gate 0 lord mismatches, 20412 rows, drift PASS). **M-02 fully CI-confirmed, zero certified-value impact.** Owner then authorized dasha-boundary-proximity-indicator decision-readiness only - the sixth and final Dasha-roadmap step. Drafted `DP-020`: independently reproduced KP's own `nearest_boundary_arcsec` completeness defect (H-07) live; confirmed a proximity value is exactly derivable from `seed_elapsed_fraction` with zero new calculation, flagging this and M-02's own certifier-only diagnostic as signals not to be silently treated as certified; explicitly distinguished this item from `DP-015`/`ADR-0067`'s own FOUNDATION-scope item without reopening it; confirmed JATAKA's own entry-criteria text has no deferral-with-blocking carve-out, so deferring this step would not unblock JATAKA the way `ADR-0067` unblocked FOUNDATION. Reviewed H-05/H-06/H-08/M-02 as precedents without mechanically copying KP's own flawed pattern. Presents five options (build a narrow seed-only field, reusing M-02's own evidence; build it plus an amplified days-of-uncertainty figure; disclosure-only; an unreachable refusal mechanism; defer), medium-confidence lean toward Option 1. No option chosen; no code touched; H-04/H-05/H-06/H-08/M-02/`DP-015`/FOUNDATION not reopened; the eight flagged cross-certifier findings untouched; general JATAKA not started. Governance gates clean (20 DP identifiers, up from 19). |
| 7.6.0 | 2026-08-24 | **`ADR-0072` ratifies `DP-019` Option 1 - M-02 CLOSED.** Six genuine near-boundary Moon cases root-found via `engine.transits.crossing.find_crossings()` (`TRANSIT_V1`) added to the Vimshottari oracle gate's `BOUNDARY_HOLDOUT` - two crossings (Lahiri nakshatra 9/10, KP nakshatra 18/19), each sampled 5 minutes before/at/after, confirmed to cross a genuine Vimshottari-lord change. Each case runs only under its own native profile after discovering mid-implementation that a case near-boundary under one ayanamsa is not, in general, near-boundary under the other (the certifier's own new self-check caught this in an earlier attempt, confirming the gate is real). `H10_boundary_moon_a`/`H11_boundary_moon_b` renamed to `H10_delhi_2025a`/`H11_delhi_2025b`, data unchanged. 6 new hermetic tests including a genuine negative control using the original mislabeled birth data. Zero certified-value impact verified via structured before/after comparison. 837/837 pytest (up from 831). Governance gates clean (72 ADR entries). Flagged, not fixed: the same mislabeled data is reused in 8 other certifiers - out of scope, recorded for a possible future decision. H-04/H-05/H-06/H-08/dasha-boundary-proximity/JATAKA not touched; FOUNDATION not reopened. Nothing pushed. |
| 7.5.0 | 2026-08-22 | Pushed `19dbc6b` (H-08, `ADR-0071`) to `origin/phase-g-governance` on explicit push authorization - fast-forward `cc02f37..19dbc6b`. CI run `32572406495`: all four jobs green, read directly from the log (oracle gate 0 lord mismatches + drift PASS confirming the new `explicit_non_claims` entry reproduces; both no-oracle legs 831 passed, up from 825, matching exactly the 6 new H-08 tests; governance gate clean). Remote SHA confirmed identical to local HEAD; working tree clean. **H-08 CI-confirmed, no certified-value change.** Owner then authorized "M-02 decision-readiness." Drafted `DP-019`: independently reproduced the audit's own exact boundary-distance figures for `H10_boundary_moon_a`/`H11_boundary_moon_b` (6.4587/5.0197 degrees), plus measured all nine other holdout cases, confirming eight of nine are closer to a boundary than at least one "boundary" case; independently verified Option 1's feasibility using already-certified `TRANSIT_V1` (`find_crossings()`), locating a real boundary crossing at sub-microarcsecond residual; checked H-04/H-05/H-06/H-08 as precedents, finding H-05's hermetic-only shape would not satisfy M-02's oracle-gate-specific wording, and identifying `KP_CHAIN_V1`'s/`TRIKALAM_V1`'s own boundary-battery precedent as more directly applicable. Classifies M-02 as an oracle/holdout coverage gap plus a label-accuracy defect - not a calculation defect. Presents four options (root-find genuine oracle-gate cases with label correction folded in; hermetic-only; label-fix only; defer), medium-high-confidence lean toward Option 1. No option chosen; no code touched; H-04/H-05/H-06/H-08/dasha-boundary-proximity/JATAKA not reopened or started. Governance gates clean (19 DP identifiers, up from 18). |
| 7.4.0 | 2026-08-22 | **`ADR-0071` ratifies `DP-018` Option 3 - H-08 CLOSED.** Ratified the existing KP `[start, end)` seed-classification convention as deliberate for every school (no calculated value changed). Added `SEED_BOUNDARY_CONVENTION_KP_EXACT` and `VimshottariTimeline.seed_boundary_convention` (additive, defaulted, mirroring `ADR-0065`'s `declared_division`); populated explicitly at the one production construction site. New pinning test file (6 tests): exactly the six previously-reproduced boundaries pinned, off by exactly one nakshatra each; the other 21 confirmed to agree; a genuine negative control (`BOUNDARY_TOLERANCE` monkeypatched to 0, divergent set changes, proving the pin is not vacuous); disclosure field confirmed across all three call shapes; H-05's baseline reproduces unchanged. `explicit_non_claims` gained one entry disclosing the seam - regenerated via the isolated PyJHora venv, PASS, only the intended addition plus known volatile fields differ. Fixed one placeholder-identifier violation the governance hook caught (mechanical correction, not substantive). 831/831 pytest (up from 825). Governance gates clean (71 ADR entries). H-05/H-06/M-02/dasha-boundary-proximity/JATAKA not touched; FOUNDATION not reopened. Nothing pushed. |
| 7.3.0 | 2026-08-22 | Pushed `cc02f37` (H-06, `ADR-0070`) to `origin/phase-g-governance` on explicit push authorization - fast-forward `76ed443..cc02f37`. CI run `32571001995`: all four jobs green, read directly from the log (oracle gate 0 lord mismatches + drift PASS; both no-oracle legs 825 passed with all fourteen holdout validators PASSED; governance gate clean). Remote SHA confirmed identical to local HEAD; working tree clean. **H-06 CI-confirmed.** Owner then authorized "H-08 decision-readiness." Drafted `DP-018`: independently reproduced the audit's own exact six-boundary cardinality (`k = 7, 11, 14, 17, 22, 25`) where the KP layer's exact-boundary rule (used unconditionally by `vimshottari_from_moon()`) disagrees with the Parashari engine's own tolerance-promoted `nakshatra()` classifier; confirmed the current cross-school behaviour is deliberate (a committed test asserts it), not accidental; confirmed the certification artifact's `explicit_non_claims` does not disclose the seam (unlike H-06's own artifact); confirmed zero interaction with H-05/H-06. Classifies H-08 as a convention ambiguity across a school-isolation seam - the roadmap's own text states this is "not a builder choice." Presents four options (ratify + pin, zero impact; change Parashari seeding to match its classifier, a genuine narrow certified-value change; the first plus an additive disclosure field mirroring `ADR-0065`'s H-02 precedent; defer), medium-high-confidence lean toward the zero-impact options. No option chosen; no code touched; H-05/H-06/M-02/dasha-boundary-proximity/JATAKA not reopened or started. Governance gates clean (18 DP identifiers, up from 17). Nothing pushed this half of the task. |
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
