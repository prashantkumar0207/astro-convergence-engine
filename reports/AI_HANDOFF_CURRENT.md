<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | INDEX ONLY - navigation aid, not evidence. See "What this file is" below. |
| Version | 2.3.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-19 (ADR-0058 drafted; specs/CLAUDE_WORKFLOW.md edit pending commit authorization) |
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

### 2026-08-19 - Execution continuity rule drafted (ADR-0058) - NOT YET COMMITTED
- Branch / commit SHA: `phase-g-governance`, working tree only - **no commit made**, per this task's own
  explicit "do NOT commit or push unless explicitly authorized by the USER."
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
- CEO decision required: **the commit itself.** ADR-0058 is recorded as the owner's ratifying
  instruction, but per that same instruction's item 10, the working-tree change is not persisted to a
  commit until the owner explicitly authorizes it.
- Next authorized action: on explicit owner authorization, stage and commit exactly the three files
  listed above (nothing else) on `phase-g-governance`, then report the resulting commit SHA and update
  this entry's "Branch / commit SHA" field accordingly. Until then, no further action is authorized by
  this entry.

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

## Snapshot as of the last update to this file (2026-08-18, refreshed after the Panchanga CI evidence recovery) - verify before relying on any of this

- Branch: `phase-g-governance`. Parent commit of this update: `695c387564cbd55e0908a730cc8b94f36ae41659`
  ("Commit CI-sourced evidence recovery for KP_CHAIN/SIGN_CONVENTION/RISE_SET/PANCHANGA and the eight
  oracle-tier certifiers"), on top of `389b98c` (ADR-0057), `00319b7` (ADR-0056), `f885693` (ADR-0055).
  **Not merged to `main`**, and `main` remains untouched. `389b98c` and everything before it is pushed to
  `origin/phase-g-governance`; `695c387` and this update's own commit are **not yet pushed** as of this
  writing - confirm with `git status` / `git log origin/phase-g-governance..HEAD` before assuming
  otherwise.
- Most recent decisions: `ADR-0054` (FOUNDATION rise/set, CERTIFIED), `ADR-0055` (Panchanga
  classification-only work authorized; Rahu Kalam/Yamaganda/Gulika explicitly deferred pending a future
  variant-table ratification), the `ADR-0047` G5 restoration addendum (22/22 restored as authoritative,
  the intervening "12/22" correction retracted), `ADR-0056` (four-role AI collaboration model, Codex
  excluded from the ACE workflow), `ADR-0057` (ACE interaction mode and mandatory session-start audit
  added to `specs/CLAUDE_WORKFLOW.md`). No new ADR for the evidence-recovery commit itself (matches the
  `bd71e0d` precedent: a plain evidence commit citing existing ADRs, not a new decision).
- FOUNDATION status: rise/set CERTIFIED (`RISE_SET_V1`). Panchanga classification (tithi, nakshatra,
  yoga, karana, vara at a given instant) implemented and certified (`PANCHANGA_V1`), now with CI-sourced
  evidence (commit `695c387`, CI run `32136604550`) - the "known, separate follow-up" the previous
  snapshot flagged is now closed for all twelve affected artifacts (`current_engine`, `KP_CHAIN_V1`,
  `SIGN_CONVENTION_V1`, `RISE_SET_V1`, `PANCHANGA_V1`, `VARGA_D2/D3/D7/D12/D30_V1`, `VIMSHOTTARI_V1`,
  `PARASHARI_DRISHTI_V1`, `TRANSIT_V1`), all at `modules_scanned: 177`. Not yet directly confirmed by a
  green CI run against `695c387` itself, since it has not been pushed. Rahu Kalam/Yamaganda/Gulika and
  element start/end transition timing remain explicitly NOT authorized (`ADR-0055` items 2-3).
- Known, permanent limitation: `swetest`-dependent certifiers cannot run on a Windows host. Not a
  regression if encountered there.
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
| 2.3.0 | 2026-08-19 | `ADR-0058` drafted (execution continuity rule): added this task's "Task handoff log" entry recording an **uncommitted** working-tree change pending explicit owner commit authorization. Snapshot section not refreshed (no new commit exists yet to refresh it to). |
| 2.2.0 | 2026-08-18 | Panchanga CI evidence recovery: added this task's "Task handoff log" entry; refreshed the snapshot to `695c387`. Structure/status from 2.0.0 unchanged. |
| 2.1.0 | 2026-08-18 | `ADR-0057` (CEO-audit HOLD remediation): added this task's "Task handoff log" entry; refreshed the snapshot to `00319b7` (on top of `f885693`). "INDEX ONLY" status and role-model/task-log structure from 2.0.0 unchanged - this entry is itself an application of that discipline, not a structural change to it. |
| 2.0.0 | 2026-08-18 | `ADR-0056`: added the "Role model" section and the structured, templated "Task handoff log" section (this file is now explicitly the canonical Claude->ChatGPT handoff, not merely a snapshot index); refreshed the stale 2026-08-17 snapshot to `f885693` (FOUNDATION rise/set certified, Panchanga classification implemented and locally certified, `ADR-0047` G5 restoration, this entry itself). |
| 1.2.0 | 2026-08-17 | Snapshot refreshed after ADR-0046: HEAD `f3bec7f3e35d0eef93e115796ddb79ffea242723`, merge commit `d53787e` now noted as historical rather than current, CI run `32011431848` green, highest and latest ADR `ADR-0046` (ADR-0044/0045/0046 all ACCEPTED). Navigation/status sections unchanged. |
| 1.1.0 | 2026-08-17 | Snapshot refreshed post-merge: branch `phase-g-governance`, merge commit `d53787e75048dbadc1a2e3559cf42405c1d56661`, CI run `32007363289` green, highest ADR `ADR-0044` (ACCEPTED). Navigation/status sections unchanged. |
| 1.0.0 | 2026-08-17 | Created as part of the minimum AI-collaboration architecture implementation. |
