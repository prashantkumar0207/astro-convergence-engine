<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | EVIDENCE - implementation record. Reports what was built, tested, and committed. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-17 |
| Review cadence | TBD |

# AI collaboration architecture: implementation report

Implements the minimum architecture recommended by `reports/AI_COLLABORATION_INSPECTION.md` and
directed explicitly by the owner in the session of 2026-08-17, recorded as `ADR-0044` in
`docs/DECISION_LOG.md`. This report is the human-readable summary of that entry; `ADR-0044` is the
normative record if the two ever disagree.

## Exact HEAD SHA

`a866ba0723a342bd9b7cd0531260daf24ff595be`, branch `phase-g-q17-q21`.
Parent: `e53be83260b74b947ea9b4b2fad477ba089c10ff` (the prior session's inspection-report commit).

## Exact files changed

New (10):
- `CLAUDE.md`
- `.claude/settings.json`
- `.claude/rules/governance.md`
- `.claude/rules/certification.md`
- `.claude/rules/git-safety.md`
- `.claude/rules/validation.md`
- `.claude/hooks/git_safety_guard.py`
- `.claude/hooks/governance_gate_check.py`
- `reports/AI_HANDOFF_CURRENT.md`
- `docs/decisions/DP-010-ai-collaboration-scaffolding.md` (drafted the prior session, committed here alongside the entry that closes it)

Modified (3):
- `.gitignore` - added `.claude/settings.local.json`.
- `docs/DECISION_LOG.md` - added `ADR-0044`; status header bumped (1.5.1 -> 1.6.0).
- `docs/decisions/README.md` - DP-010 index row marked `ADDRESSED by ADR-0044`; status header bumped (1.1.0 -> 1.2.0).

Not committed (deliberately local-only, gitignored): `.claude/settings.local.json`, cleared to an
empty allow-list (`{"permissions": {"allow": []}}`) as the personal-override layer.

## Exact rationale

Full rationale is in `ADR-0044`'s Context/Decision/Consequences; summarized per file:

- **`CLAUDE.md`** operationalizes `docs/PROJECT_CONSTITUTION.md` s11 for tooling by citation, not
  restatement - states the audit-first, evidence-over-narrative, no-self-certification,
  never-weaken-a-gate, owner-ratifies rules, the memory boundary, and the evidence-bridge principle,
  each pointing at the document it derives from rather than asserting its own authority. Explicitly
  states that `PROJECT_CONSTITUTION.md` is itself `DRAFT`, so nothing is presented as settled that
  isn't.
- **`.claude/rules/*.md`** hold the scoped detail `CLAUDE.md` intentionally keeps out (governance
  process, certification/gate discipline including the Windows/`swetest` limitation, git safety, and
  validation discipline), pulled in via explicit `@` imports - Claude Code does not auto-scan an
  arbitrary `rules/` directory.
- **`.claude/settings.json`** replaces three one-off literal permission strings (a leftover from the
  prior session's specific commands) with general, reusable patterns for genuinely safe operations,
  and deliberately omits `git push` and every destructive git verb so those keep prompting. No
  `permissions.mode` override is set anywhere; `bypassPermissions` is not used, satisfying the explicit
  constraint by design rather than by absence.
- **Two hooks**, both calling existing tooling rather than reimplementing logic: `git_safety_guard.py`
  (`PreToolUse` on `Bash`) mechanically blocks the clearest destructive/unsafe operations for this
  session; `governance_gate_check.py` (`PostToolUse` on `Edit`/`Write`) re-runs
  `check_adr_numbering.py` / `check_retired_identifiers.py` / `check_identifier_families.py` /
  `check_artifact_drift.py` immediately after an edit to a file they cover, scoped away from the
  `swetest`-dependent certifiers that cannot run on this Windows host.
- **`reports/AI_HANDOFF_CURRENT.md`** is headed "INDEX ONLY - navigation aid, not evidence" in its own
  status field and repeats that framing in its body, points at git commands and at
  `docs/DECISION_LOG.md`/`docs/OPEN_QUESTIONS.md` rather than asserting facts of its own, and states
  explicitly that the repository wins if the two disagree.
- **`docs/PROJECT_CONSTITUTION.md`, `engineering/ENGINEERING_CONSTITUTION.md`, `specs/CLAUDE_WORKFLOW.md`,
  `docs/PROJECT_MASTER.md` were not modified.** The owner's instruction was to record their staleness
  (already done in `reports/AI_COLLABORATION_INSPECTION.md` s2.8) rather than repair it in this pass;
  `CLAUDE.md` cites `PROJECT_CONSTITUTION.md`'s actual `DRAFT` status rather than presenting it as
  settled, so nothing new relies on the inconsistency being invisible.
- **`ADR-0044`** is the git-authoritative record of this whole decision, so the architecture rests on a
  decision-log entry rather than only on this conversation, per `docs/PROJECT_CONSTITUTION.md` s7. It
  closes `DP-010` by reference, narrower than that paper's own recommendation (no skills, agents, or
  MCP servers were added, per explicit instruction).

## Tests / checks executed and results

| Check | Result |
|---|---|
| `python -m pytest -q` | **527 passed**, 0 failed, 0 skipped (run three times across the session: before, mid-fix, and against the final committed HEAD) |
| `python scripts/check_adr_numbering.py` | **PASS** - 41 entries, `ADR-0001..ADR-0044`, unique and monotonic |
| `python scripts/check_retired_identifiers.py` | **PASS** - 0 violations, both patterns (after fixing several non-four-digit `ADR-` placeholder tokens found by this same gate during drafting - see "Issues found and fixed" below) |
| `python scripts/check_identifier_families.py` | **PASS** - 10 registered `DP-NNN` identifiers, no unregistered tokens |
| `git diff --check` (staged, final) | **clean** |
| JSON validity, `.claude/settings.json` / `.claude/settings.local.json` | both valid |
| `python -m py_compile` on both hooks | both compile |
| `git_safety_guard.py` smoke tests | 11 original cases (5 block, 6 allow) + 3 cases targeting the heredoc/quote fix specifically (1 regression-repro, 1 confirm-still-blocked, 1 confirm-still-allowed) - **all as expected** |
| `governance_gate_check.py` smoke tests | pass-through on the current valid `docs/DECISION_LOG.md` and `docs/decisions/README.md`; no-op on an unrelated file and on a non-`PostToolUse` event; **negative control**, run twice (once pre-fix, once post-fix against the final text): a duplicate ADR heading was deliberately and temporarily injected into a working copy of `docs/DECISION_LOG.md`, the hook correctly returned exit 2 both times, and the file was restored and re-verified (`check_adr_numbering.py` PASS, `git diff --stat` empty) before proceeding |
| Forbidden-path check (`git diff --cached --name-only \| grep engine/\|legacy/\|certification/\|knowledge/\|certify_\|validate_`) | **no matches** - confirmed no calculation, certification, or product file is in the diff |
| CLAUDE.md `@`-import resolution | all four `.claude/rules/*.md` paths referenced from `CLAUDE.md` exist on disk |

## Issues found and fixed during implementation

1. **Identifier-gate false positives while drafting.** `CLAUDE.md` and `.claude/rules/governance.md`
   originally used a generic four-letter placeholder in place of real digits after the `ADR-` prefix,
   and once used the prefix immediately followed by a descriptive word - both shapes match
   `scripts/check_retired_identifiers.py`'s Pattern B (`ADR-` not followed by exactly four digits).
   Fixed by rephrasing to prose ("a four-digit, zero-padded ADR entry, for example `ADR-0044`")
   instead of a pseudo-token. Caught by the gate itself before any commit was attempted.
2. **A real defect in `git_safety_guard.py`, found on its first live use.** The first actual commit
   attempt of this batch was blocked: the commit message's own descriptive prose (naming `--no-verify`
   and `--no-gpg-sign` as the flags the hook blocks) was pattern-matched as if those were live shell
   flags, because the hook scanned the raw command string including heredoc body text. This is the
   same self-reference defect class this repository has hit before in the retired-identifier gate.
   **Fixed, not bypassed**: the hook now strips heredoc bodies and quoted-string contents before
   scanning for dangerous patterns (`_sanitize()` in `git_safety_guard.py`), re-verified against the
   full smoke-test battery plus three cases targeting the fix directly, and the commit then succeeded
   normally. See `ADR-0044`'s evidence paragraph for the same account in the normative record.

## Unresolved issues

- **`main` still carries no GitHub branch-protection rule.** Neither this implementation nor the
  `PreToolUse` hook changes that; the hook only covers this Claude Code session's own `Bash` tool calls
  on this host. Stated explicitly in `.claude/rules/git-safety.md` and `CLAUDE.md` rather than implied
  away. Not in scope for this pass (would be a GitHub-side change, not a repository file).
- **The three stale/inconsistent AI-role documents remain unrepaired**, by explicit instruction:
  `docs/PROJECT_CONSTITUTION.md` s11 is still `DRAFT` while `engineering/ENGINEERING_CONSTITUTION.md`
  Principle 11 is `ACTIVE`; `specs/CLAUDE_WORKFLOW.md` still has no status header; `docs/PROJECT_MASTER.md`
  still contradicts `ADR-0041` with no superseding note. Recorded in `ADR-0044` and here; not fixed.
- **The eleven untracked transfer-bundle/scratch files from the Q17-Q21 batch are still present** in
  the repository root (`ace-*.bundle`, `*.patch`, five one-off `.py` scripts, `.ace_q17_q21_prechange/`).
  Out of scope for this instruction; the user previously chose to leave them alone (session of
  2026-08-14). `reports/AI_HANDOFF_CURRENT.md` does not reference them as a mechanism to use going
  forward.
- **`.claude/rules/*.md` cite `docs/VALIDATION_STANDARD.md` and `docs/NAMING_STANDARD.md`, both
  themselves `DRAFT`.** Stated as such in the rule files; not a defect, but worth carrying forward as
  the same "citing an unratified document honestly" pattern applied consistently.
- **The keep-in-sync mechanism for `CLAUDE.md`'s citations is manual**, as `DP-010` section 7 already
  flagged as an open item. No mechanical gate checks that `CLAUDE.md`'s claims about
  `PROJECT_CONSTITUTION.md` still match that document's actual text. Not built in this pass; would be a
  reasonable future addition, not a minimum-viable one.

## Working tree / branch state

- Working tree: **not fully clean** - the pre-existing, previously-flagged-and-explicitly-left-alone
  untracked bundle/scratch files from the Q17-Q21 session remain (listed above). No tracked file is
  modified or staged beyond this commit; `git status` shows only those untracked files.
- Branch: `phase-g-q17-q21`, **ahead of `origin/phase-g-q17-q21` by 1 commit** (this one). **Not
  pushed** - pushing was not requested in this session's instructions and is being held for explicit
  confirmation, per `.claude/rules/git-safety.md` ("pushing is a shared-visibility action").
- **Not merged to `main`.**

## Next authorized step

Confirm whether to push `a866ba0723a342bd9b7cd0531260daf24ff595be` to `origin/phase-g-q17-q21`. No
other action is implied by this report; the three unresolved-issue items above are candidates for a
future, separately-authorized pass, not follow-on work implied by this one.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-17 | Implementation completed, verified, and committed as `a866ba0`; report written against that commit. |
