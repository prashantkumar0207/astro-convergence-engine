<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | EVIDENCE - inspection only. No calculation, certification, governance, or product file was modified to produce this report. Proposes a minimum implementation; decides nothing. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-17 |
| Review cadence | TBD |

# AI collaboration inspection: existing mechanisms and minimum "repository-first Claude Code operating system"

Scope: inspection of the currently loaded Claude Code configuration (this machine, this repository)
against the ten target-architecture requirements given. No calculation, certification, governance, or
product file was touched. Git state at inspection time: branch `phase-g-q17-q21`, HEAD `ee8d1f4`
(`origin/phase-g-q17-q21` ahead by 1 local commit), with `docs/decisions/DP-010-ai-collaboration-scaffolding.md`
and `docs/decisions/README.md` staged uncommitted from a prior session, and the same untracked
transfer-bundle/scratch-file set from the Q17-Q21 batch still present in the repository root.

## 1. Exact files and locations inspected

**Repository-tracked / working tree:**
`CLAUDE.md`, `CLAUDE.local.md` (repo-wide case-insensitive search, no match anywhere including nested
paths); `.claude/settings.json`; `.claude/settings.local.json`; `.gitignore`; `.gitattributes` (absent);
`.git/hooks/` (contents); `docs/PROJECT_CONSTITUTION.md`; `engineering/ENGINEERING_CONSTITUTION.md`;
`specs/CLAUDE_WORKFLOW.md`; `specs/PROJECT_CHARTER.md`; `docs/DOCUMENTATION_STANDARD.md`;
`docs/NAMING_STANDARD.md`; `docs/VALIDATION_STANDARD.md`; `docs/DECISION_LOG.md`; `DECISION_LOG.md`
(root, D-00x register); `docs/OPEN_QUESTIONS.md`; `docs/decisions/README.md`;
`docs/decisions/DP-010-ai-collaboration-scaffolding.md`; `docs/PROJECT_MASTER.md`; `README.md`;
`.github/workflows/ci.yml`; `scripts/*.py` (all 22, listed in section 2); `reports/AI_HANDOFF_CURRENT.md`
(does not exist); `HOLD_REMEDIATION_PROPOSALS.md`; the eleven untracked `ace-*.bundle` /
`adr-*.bundle` / `phase-g-*.bundle` / `*.patch` files and five untracked one-off Python scripts left
from the Q17-Q21 session.

**Machine-level Claude Code configuration (outside the repository):**
`~/.claude/settings.json` (global); `~/.claude.json` (`projects["c:/Users/Nidhi/astro-convergence-engine"]`
entry); `~/.claude/` recursively for `hooks`, `rules`, `skills`, `agents`, `commands` directories (none
found at any depth); `~/.claude/projects/c--Users-Nidhi-astro-convergence-engine/memory/` (exists,
empty - zero memory files written for this project to date).

**External to the filesystem:** `gh api repos/prashantkumar0207/astro-convergence-engine/branches/main/protection`
(branch protection status); `gh auth status`.

## 2. Existing mechanisms found

### 2.1 CLAUDE.md / CLAUDE.local.md
**Absent.** No file of either name exists anywhere in the repository, at any nesting depth. Nothing to
retain or conflict with.

### 2.2 `.claude/`
Present but **entirely untracked** (`git status` reports `?? .claude/`; not listed in `.gitignore`
either - it has simply never been staged). Contains exactly two files:
- `settings.json`: one permission rule, `Bash(git checkout *)`.
- `settings.local.json`: three permission rules, each a single **literal, one-off command string**
  (an exact `pytest` invocation naming one test file; an exact `check_artifact_drift.py` invocation
  naming four specific artifact paths; a literal `echo "exit=$?"`). These are auto-accumulated
  leftovers from the specific commands run in the immediately preceding session, not an authored
  policy - none would match a slightly different but equally safe invocation.

No `.claude/rules/`, `.claude/hooks/`, `.claude/skills/`, `.claude/agents/`, or `.claude/commands/`
directory exists, in this repository or globally under `~/.claude/`.

### 2.3 Hooks
**None configured**, anywhere. `.claude/settings.json` and `~/.claude/settings.json` both carry only a
`permissions` key; neither has a `hooks` key. `.git/hooks/` contains only Git's default `.sample`
files, none installed. No `SessionStart`, `PreToolUse`, `PostToolUse`, or `Stop` hook exists at any
scope.

### 2.4 Settings / permission mode
No `bypassPermissions` or any other non-default `permissionMode` is set anywhere (project entry in
`~/.claude.json` carries no mode override; `hasTrustDialogAccepted: false`; no MCP servers configured).
Requirement 6's constraint is currently satisfied by absence rather than by design - there is no
policy yet, safe or otherwise, tracked in the repository.

### 2.5 Skills
**None.** No `.claude/skills/` directory exists at project or user scope.

### 2.6 AI handoff / current-state mechanisms
- `reports/AI_HANDOFF_CURRENT.md` **does not exist**.
- `README.md` "Current state" section is a well-maintained rolling summary of **certified engine
  capability** (ADR-0005 through ADR-0012), current as of the last certification work. It does not
  cover governance/branch/CI/PR state.
- `docs/DECISION_LOG.md` and `docs/OPEN_QUESTIONS.md` are the real, working project memory -
  versioned, ratification-tracked, evidence-linked. Functioning as designed; this is the actual
  authority, per `docs/PROJECT_CONSTITUTION.md` s7 ("the repository is the single authoritative
  record... anything not in the repository... is input material, not truth").
- An **undocumented, ad hoc git-bundle handoff convention** is in active use: eleven `.bundle`/`.patch`
  files sit untracked in the repository root (evidence packages for CEO/ChatGPT review across the
  Q17-Q21 batch). Referenced exactly once, informally, in `HOLD_REMEDIATION_PROPOSALS.md`. Not named
  in `docs/NAMING_STANDARD.md`, not gitignored, not cleaned up after use.
- `reports/REPOSITORY_AUDIT_REPORT.md` cites a `MASTER_HANDOFF.md` that does not exist anywhere in the
  repository or its git history - evidence an external, non-reproducible handoff package was used once
  (2026-08-08, one-off cloud audit container) and left no trace in-repo.
- Claude Code's own persistent cross-session memory mechanism exists (`~/.claude/projects/.../memory/`)
  but **no memory file has ever been written for this project** - the mechanism is present and unused,
  not yet a source of drift, but also not yet bounded by any written rule.

### 2.7 Git safety mechanisms
- `.git/hooks/`: no hooks installed (default samples only). Nothing locally enforces safe git usage
  independent of the operator's/agent's own discipline.
- **`main` is not a protected branch on GitHub** (`gh api .../branches/main/protection` returns
  `404 Branch not protected`). Force-push, direct push, and history rewrite on `main` are currently
  possible for anyone with write access, with no platform-level gate.
- `.gitignore` covers Python/venv/pytest/IDE/OS/log noise; does not mention `.claude/`.
- No `.gitattributes` - line-ending behaviour is implicit (a CRLF/LF warning was observed while
  staging a file this session, confirming mixed-ending risk exists but is currently unmanaged).
- `.github/workflows/ci.yml` (three jobs: `hermetic` matrix on 3.11/3.12, `oracle` on 3.11 only,
  `governance`) is the real enforcement layer today: no `continue-on-error` anywhere, every `run` block
  is `bash -e`, and four purpose-built gate scripts exist and are wired into CI -
  `scripts/check_adr_numbering.py`, `scripts/check_retired_identifiers.py`,
  `scripts/check_identifier_families.py`, `scripts/check_artifact_drift.py` - each with a committed
  negative control proving it can fail. These are CI-side (remote) and partially Windows-incompatible
  by nature (`certify_current_engine.py` and other `swetest`-dependent certifiers cannot run on this
  Windows host at all; confirmed directly in the prior session). The four gate scripts named above are
  pure Python and do run cleanly on this host.

### 2.8 Existing ACE governance instructions relevant to AI role
- `docs/PROJECT_CONSTITUTION.md` s11 "AI Collaboration Model" is the **only** place the two-AI
  architecture is actually defined (ChatGPT = reviewer/auditor; Claude = builder/executor; owner
  ratifies all decisions; four binding rules). The document is **`Status: DRAFT, Version 0.1.0, dated
  2026-07-11`** - unchanged since before Q1 named an owner, before Tier-0 locked, before ADR-0042
  established the authority hierarchy that places this document above `ENGINEERING_CONSTITUTION.md`.
- `engineering/ENGINEERING_CONSTITUTION.md` Principle 11 ("every implementation generated by AI must be
  reviewed before entering Git") is marked **`Status: ACTIVE, Version 1.1.0`** - the subordinate
  document carries the more authoritative-looking status than the senior one.
- `specs/CLAUDE_WORKFLOW.md` defines Claude's operational role (implementation engineer, handoff-package
  pattern, "two AI systems agreeing is not evidence") but **carries no status header, version, or owner
  field at all**, contrary to `docs/DOCUMENTATION_STANDARD.md` s2's mandatory structure for governing
  documents.
- `docs/decisions/DP-010-ai-collaboration-scaffolding.md` (drafted in the prior session, staged
  uncommitted, registered in `docs/decisions/README.md` as DP-010) already analyses this exact
  question in options form and recommends, at medium-high confidence, an operationally-restated,
  explicitly-cited `CLAUDE.md` plus a small named set of skills - functionally Option B + Option F of
  that paper. **It is explicitly `Status: OPEN ... DECIDES NOTHING ... requires owner approval before
  any file listed here is created or repaired.`** It has not been ratified, superseded, or referenced
  by any decision-log entry.
- `docs/PROJECT_MASTER.md` is stale in a way that actively contradicts ratified decisions (describes a
  Flutter-app pipeline and an `app/` top-level folder; ADR-0041 explicitly excludes `app/` from the
  canonical top-level structure) and, unlike the repository's other stale root documents, carries no
  superseding note.
- `docs/NAMING_STANDARD.md` and `docs/VALIDATION_STANDARD.md` are both `Status: DRAFT`, versions 0.1.0
  and 0.2.0 respectively - any new rule file that normatively cites them is citing unratified drafts,
  which must be stated accurately rather than implied as settled.

## 3. What should be retained

- `docs/DECISION_LOG.md`, root `DECISION_LOG.md`, `docs/OPEN_QUESTIONS.md`, `docs/decisions/` - the
  working project memory. No change needed; this is git-authoritative already and is exactly what
  requirement 9 (git/commits/CI as the evidence bridge) depends on.
- The four CI governance gate scripts (`check_adr_numbering.py`, `check_retired_identifiers.py`,
  `check_identifier_families.py`, `check_artifact_drift.py`) as the deterministic-enforcement substrate
  - new hooks should call these, not reimplement equivalent logic.
- `README.md`'s "Current state" section, unchanged in scope (certified engine capability only).
- `specs/CLAUDE_WORKFLOW.md`'s substantive content (the handoff-package pattern, the
  two-AIs-agreeing-is-not-evidence principle) - sound, just undocumented as a governing artifact.
- `docs/PROJECT_CONSTITUTION.md` s11's substance (the role split itself) - sound; only its status/version
  currency is stale, not its content.

## 4. What should be consolidated

- `docs/PROJECT_CONSTITUTION.md` s11 and `engineering/ENGINEERING_CONSTITUTION.md` Principle 11 say
  compatible but non-identical things at inconsistent status levels. A new `CLAUDE.md` must cite the
  senior document (s11) as the authority and note, not silently repeat, the junior document's narrower
  clause - it must not create a third, slightly different restatement.
- The ad hoc git-bundle handoff convention and the (currently absent) `reports/AI_HANDOFF_CURRENT.md`
  are two answers to the same problem (how state gets handed to an external reviewer). Introducing the
  latter without retiring or formally documenting the former leaves two competing, inconsistent
  mechanisms - one of which (bundles) already left an orphaned reference (`MASTER_HANDOFF.md`) once.
- `docs/decisions/DP-010-ai-collaboration-scaffolding.md` and this request are the same question asked
  twice, once as an options paper and once as a directive. They should be reconciled explicitly (see
  section 6), not left as two parallel, inconsistently-authoritative statements of the same intent.
- The three literal, one-off rules in `.claude/settings.local.json` should be replaced by a small
  number of general, reusable patterns rather than left to keep accumulating one entry per session.

## 5. What should be added (per requirement, minimum only)

1. **Root `CLAUDE.md`, tracked.** Concise (target: one screen). States the operating rules
   (audit-before-modify, evidence over narrative, no self-certification, never weaken a gate, owner
   ratifies all decisions, stop conditions) as actionable instructions, each citing the
   `PROJECT_CONSTITUTION.md` section or spec it derives from - restating, not duplicating as a second
   source of truth. Points to `.claude/rules/*.md` for scoped detail and to
   `reports/AI_HANDOFF_CURRENT.md` for current state.
2. **`.claude/rules/` as a small set of scoped markdown files**, pulled into `CLAUDE.md` via explicit
   `@.claude/rules/<name>.md` import lines. Note: Claude Code does not auto-scan an arbitrary `rules/`
   directory the way it auto-discovers `skills/`/`agents/`/`commands/` - the directory only takes
   effect if `CLAUDE.md` (or an imported file, up to 5 hops) references each file explicitly. Minimum
   set: `governance.md` (ADR/DP process, ratification rule), `certification.md` (gate scripts, "stored
   results are not proof", Windows-`swetest` limitation), `git-safety.md` (no force-push/reset
   --hard/direct-main-push without explicit confirmation, matching what a hook would also enforce
   mechanically), `validation.md` (pointer to `VALIDATION_STANDARD.md`, DRAFT-status caveat).
3. **No new file for memory.** The scope boundary (convenience only - communication-style and
   session-logistics facts; never a substitute for `DECISION_LOG.md`/`OPEN_QUESTIONS.md`/`CLAUDE.md`
   content; never cited as evidence) should be stated as one line in `CLAUDE.md` itself, since the
   memory mechanism already exists and is currently unused - the risk is scope creep, not absence.
4. **`reports/AI_HANDOFF_CURRENT.md`, tracked, regenerated per session.** Concise index only: current
   branch, HEAD SHA, open PR/CI status, next authorized step, pointers into `DECISION_LOG.md` /
   `OPEN_QUESTIONS.md`. Must carry an explicit "this file is an index, not evidence; the commits and CI
   runs it points to are the evidence" statement, matching requirement 9 and preventing it from
   becoming a fifth parallel status document (section 2.6 already found several).
5. **Two hooks, minimum.** (a) A `PreToolUse` guard on `Bash` matching destructive git verbs
   (`push --force`, `push -f`, `reset --hard`, `clean -f`, `branch -D`, direct `push` with the current
   branch resolved to `main`) that blocks and requires an explicit restated confirmation - this is the
   one place a hook closes a real, currently-open gap, since neither local git hooks nor GitHub branch
   protection currently enforce it (section 2.7). (b) A `PostToolUse` hook on edits to
   `docs/DECISION_LOG.md`, `docs/decisions/*`, or `certification/*.json` that re-runs the matching gate
   script from section 2.7 immediately, surfacing a break before commit rather than only at CI. Both
   call existing scripts; neither reimplements gate logic.
6. **A curated, tracked `.claude/settings.json`** replacing the current one-off allow rules with general
   patterns (safe reads: `git status*`, `git diff*`, `git log*`; test/gate execution:
   `python -m pytest*`, `python scripts/check_*.py*`; safe restores: `git checkout -- *`), no
   `permissions.mode` override (default remains active; `bypassPermissions` never set, satisfying
   requirement 6 explicitly rather than by absence), and the destructive verbs from item 5(a) left
   off the allow-list so they still prompt even without the hook (defense in depth). `.claude/settings.local.json`
   added to `.gitignore` as the explicit personal-override layer, instead of sitting untracked by
   omission as it does today.
7. **No action required.** Nothing currently present depends on Claude Desktop (no Desktop-specific MCP
   or config found at any scope inspected); the constraint is already satisfied.
8. **No AI-to-AI conversational handoff channel to add**, and the existing bundle convention should be
   folded into normal branch/PR/`AI_HANDOFF_CURRENT.md` flow rather than formalized as its own
   mechanism - satisfies the requirement by retiring the one file-based pattern that could drift toward
   becoming a side-channel, rather than by adding a new rule against something that doesn't exist yet.
9. **No new file**; state explicitly in `CLAUDE.md` (item 1) that commits, PRs, and CI runs are the
   evidence surface an independent auditor (ChatGPT or the owner) checks against - already true in
   practice (this is exactly how the prior session's ADR-0043 fix was packaged for audit) and only
   needs to be written down as a standing rule rather than re-derived per session.
10. **Governance repair, alongside, not after:** version/status-sync `docs/PROJECT_CONSTITUTION.md` s11
    (or at minimum note its DRAFT status honestly in anything that cites it); add a status header to
    `specs/CLAUDE_WORKFLOW.md`; add a superseding note to (or retire) `docs/PROJECT_MASTER.md`. Doing
    this only after `CLAUDE.md` exists and cites the broken state would mean `CLAUDE.md` launches
    already citing inconsistent sources.

## 6. Conflicts

- **This request substantially duplicates `docs/decisions/DP-010-ai-collaboration-scaffolding.md`**,
  which is staged, unratified, and explicitly states "decides nothing... requires owner approval before
  any file listed here is created." Proceeding to implement without closing DP-010 first (either by
  treating this conversation as the ratifying decision and recording that in a decision-log entry, or
  by formally superseding DP-010) would create exactly the pattern `docs/PROJECT_CONSTITUTION.md` s7
  warns against: a conversation, not the repository, becoming the operative record of approval.
- **Status inconsistency**: `PROJECT_CONSTITUTION.md` s11 (DRAFT) is cited as authoritative by design
  while itself unratified; any `CLAUDE.md` text must say so plainly rather than presenting a DRAFT
  section as settled.
- **`.claude/rules/` is not a Claude Code auto-load mechanism** the way the request's phrasing might
  imply - it must be wired through explicit imports in `CLAUDE.md`, or the files will exist but do
  nothing. This is a design conflict between the requested label and the tool's actual mechanism, not
  a governance conflict, but it would silently fail to achieve requirement 2 if built as a bare
  directory with no importer.
- **Hooks are local-machine-scoped.** They bind this Claude Code installation on this host, not other
  git clients, not other collaborators, not GitHub itself. Presenting them as "Git safety" without also
  noting that `main` has no branch protection (section 2.7) would overstate what requirement 6/9 actually
  guarantee.

## 7. Risks

- **False sense of enforcement.** A `PreToolUse` git-safety hook only covers actions this specific
  Claude Code session takes through its own `Bash` tool. It does not stop a manual `git push --force`
  run outside the tool, and it does not substitute for the GitHub branch protection that is currently
  absent on `main`. Should be documented as a bounded control, not a complete one.
- **Memory scope creep.** The auto-memory mechanism is currently empty and unbounded by any written
  rule; without the one-line scope statement in `CLAUDE.md` (item 3), it is one saved fact away from
  becoming a shadow, non-git-tracked source of "truth" that contradicts s7.
- **CLAUDE.md/rules drift from the constitution they cite.** The exact defect class already found twice
  in this repository (`ENGINEERING_CONSTITUTION.md` vs `PROJECT_CONSTITUTION.md` status; multiple
  citation-drift findings, e.g. L-8 in `docs/DECISION_LOG.md`) will recur here unless citations are
  checked at write time and periodically thereafter; no mechanical gate for this exists yet and is not
  proposed as part of the minimum set.
- **Windows/CI parity gap.** A `PostToolUse` hook that tries to invoke a `swetest`-dependent certifier as
  "verification" would false-fail or hang on this host. The minimum hook design (item 5b) is scoped to
  the four pure-Python gate scripts specifically to avoid this; any expansion of hook scope must
  re-check this constraint.
- **Untracked `.claude/` becoming tracked without review.** `settings.local.json`'s current contents are
  session leftovers, not policy; committing the directory as-is (rather than the curated version in
  item 6) would enshrine noise as if it were a deliberate allowlist.
- **Unresolved handoff debris.** The eleven bundle/patch files and five scratch scripts from the
  Q17-Q21 session remain untracked in the repository root at the time of this inspection; introducing
  `AI_HANDOFF_CURRENT.md` without addressing them leaves both the old and new mechanisms visible
  simultaneously, which is itself confusing for a cold session.

## 8. Recommended minimum implementation (proposal only; nothing executed by this report)

In dependency order:

1. Resolve the DP-010 relationship first (ratify by reference to this conversation and record it as a
   decision-log entry, or formally supersede DP-010 with a new entry) - so what follows has a git-authoritative
   basis rather than resting on conversation alone.
2. Repair the three governance-doc inconsistencies named in section 5, item 10, so nothing new cites
   broken state.
3. Add root `CLAUDE.md` (section 5, item 1) plus the four `.claude/rules/*.md` files it imports
   (item 2), including the one-line memory scope statement (item 3).
4. Add `reports/AI_HANDOFF_CURRENT.md` (item 4) and, in the same pass, resolve the untracked
   transfer-bundle debris (item 8) so only one current-state/handoff mechanism is visible afterward.
5. Add the curated `.claude/settings.json`, gitignore `.claude/settings.local.json`, and the two hooks
   (items 5-6), with explicit confirmation that no `permissions.mode` override is introduced.
6. Verify: full local gate (`python -m pytest`), the four governance check scripts, and a manual
   exercise of both new hooks (one destructive-git attempt that should be blocked; one governance-file
   edit that should trigger the fast-feedback check) before considering the change complete.

## 9. Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-17 | Inspection performed and findings recorded. No implementation performed. |
