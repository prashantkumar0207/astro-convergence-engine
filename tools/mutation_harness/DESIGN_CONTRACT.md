# WP-RD-B mutation harness — design contract

| Field | Value |
|---|---|
| Status | IMPLEMENTED FOR FIXTURE TESTING ONLY. Not approved for any ACE production mutation. |
| Work package | WP-RD-B (certification mutation harness rebuild) |
| Design baseline | `WP-N1-RD-01-R1_Corrected_Design_Packet.md`, SHA-256 `b3ed57865c1986cd7d24f85d4513aee31389f58ffc7c9ccf066ed4c622efac82` (12-section design; revisions RD-C1 to RD-C6; governance clarification G-1) |
| Binding amendments | CEO amendments A (restoration-state precedence) and B (D45 classifier-sign control), accepted after R1; they override contradictory R1 wording |
| Execution order | CEO directive WP-RD-B-IMP-01, issued on the owner's explicit WP-RD-B implementation authorization; corrected by CEO directive WP-RD-B-F1 (owner-approved; §4a) |
| Governance status | Not a decision entry. Not ratified. Formal governance recording and any merge remain subject to owner approval. |

This file records the contract the code in this directory implements. It does not decide anything
for the project. The decision register (`docs/DECISION_LOG.md`) is not modified by this work package.

## 1. Authorized scope

The owner's authorization covers only:
- local implementation under `tools/mutation_harness/`;
- fixture testing in disposable temporary repositories, with harmless simulated mutations;
- one local commit on branch `wp-rd-b-mutation-harness`, created from `main` at
  `6538930c2832b49de54c31edad4614e265a86695`.

**Forbidden:**
- push, pull request, merge, force push, or any change to `main`;
- fetch, pull, rebase or reset to reconcile an unexpected baseline;
- any ACE production mutation, or running this harness against an ACE target;
- executing ACE certifiers or validators, or regenerating certification artifacts;
- WP-N2, WP-0b, WP-RD-A (D45 validator/certifier changes), D24 discharge, Gate H remediation, C2–C5;
- cleanup of retained WP-N1 worktrees, or deletion of historical evidence;
- tolerance changes, ADR ratification, decision-log edits, or a JATAKA exit declaration.

**Code-level enforcement of the target restriction.** `harness.Runner` refuses any target worktree
that contains the ACE markers `engine/astrology` or `scripts/certify_d45.py` (`ACE_TARGET_MARKERS`).
Lifting that guard requires a separate owner authorization. It is not a configuration option.

## 2. Outcome vocabulary (unchanged from WP-N1)

| Outcome | Meaning |
|---|---|
| DETECTED | The designated gate alone exits with the registered failure code, a stdout line starts with the registered failure prefix, and the validator output contains every registered expectation string. |
| DETECTED-OTHER | The designated gate alone passes, but the end-to-end run or an excluded gate fails. |
| UNDETECTED | The designated gate alone passes, and the end-to-end run and every excluded gate pass. |
| EQUIVALENT | The pre-check shows the mutation changes no inspected value. The mutation is not applied. |
| VOID | The baseline is not clean; or the designated gate fails for a reason other than the registered one; or **(R1/Amendment A)** the mutation observation is invalidated (an S6 attestation failure, timeout, or a hash state that is not the registered mutated hash). |

An outcome recorded in S6 is never rewritten by a later restoration failure. Outcome, restoration
status and experiment validity are separate dimensions.

## 3. Restoration status and precedence (Amendment A)

`restoration_status` takes one of: `NOT-APPLICABLE` (no edit applied), `RESTORED-VERIFIED`,
`RESTORATION-FAILED`, `INDETERMINATE`.

Precedence, highest first: **INDETERMINATE > RESTORATION-FAILED > RESTORED-VERIFIED**. The highest
applicable status wins and is never downgraded.

| Condition | Status |
|---|---|
| Restored target bytes match neither the baseline SHA-256 nor the registered mutated SHA-256 | INDETERMINATE (fixture C5 → T10) |
| Interruption or exception during a state transition after the mutation write was intended | INDETERMINATE. Re-hashing afterwards is evidence collection only, never an upgrade. |
| Git status execution error or porcelain parse error | INDETERMINATE |
| S8 timeout, target hash a known value | RESTORATION-FAILED |
| S8 timeout, target hash unknown | INDETERMINATE |
| S8 missing, corrupt, mismatching or inconclusive code attestation | RESTORATION-FAILED, unless an INDETERMINATE condition also applies |
| Target still equals the registered mutated hash after restore | RESTORATION-FAILED |
| Collateral or new-ignored change in the worktree after restore | RESTORATION-FAILED |
| Designated gate or end-to-end rerun fails after restore | RESTORATION-FAILED |
| S6 attestation failure | outcome VOID (restoration is still performed and verified) |

**INDETERMINATE consequences:** experiment INVALID, batch HALT, worktree quarantined (marker written
to the configured quarantine directory), and all evidence preserved. No further code is executed in
the worktree for that run.

## 4. Experiment validity

`experiment_validity = VALID` iff **all** of the following hold:
- the outcome is not VOID;
- the restoration status is RESTORED-VERIFIED or NOT-APPLICABLE;
- every mandatory code attestation passed in every phase;
- evidence is complete under the **WP-RD-B-F1 two-phase finalization** protocol (§4a): a verified
  pending candidate, then a durable and verified FINAL record binding the candidate's SHA-256, then
  atomic no-replace publication of `result.json`, then confirmation through the consumer contract.

Otherwise `INVALID`. **Batch rule (conservative simplification of R1 T4b):** the batch continues only
after a VALID experiment; any INVALID experiment halts the batch. The design's "continue only if the
error is local to the pre-check" option is not implemented. Every pre-check error halts.

## 4a. Durable evidence finalization (WP-RD-B-F1, CEO directive WP-RD-B-F1)

**Invariant.** An authoritative persisted result never reports VALID unless all mandatory evidence
for that verdict has already been finalized and verified.

**Defect corrected (commit `4318b31`).** `_finalize()` wrote, fsynced and verified `result.json`
(L729–L733) **before** appending the mandatory FINAL journal record (L734). If that append failed, the
function returned INVALID/HALT, but the persisted `result.json` still said VALID/CONTINUE.

**Protocol (`harness.Runner._finalize`):**

| Stage | Action | On failure |
|---|---|---|
| A — prepare | Serialize the candidate. Exclusively create `result.pending.json`, fsync it, fsync the directory, re-read and verify its SHA-256. | INVALID / HALT; no FINAL is written |
| B — finalize | Append `S9 FINAL` (`run_id`, `candidate_sha256`, `result_sha256`; meaning: *mandatory evidence finalized, publication pending*), fsync it, and verify the record is the durable journal tail. | INVALID / HALT; `S9 FINALIZATION-FAILED` is appended after it |
| C — publish | `os.link(pending, result.json)`: an atomic, same-directory, **no-replace** publication. Then fsync the directory and check `samefile`. | INVALID / HALT; our own just-published `result.json` is **retracted** (its bytes remain in the pending file) |
| D — confirm | `validate_run_evidence()` must report COMPLETE, with the persisted result equal to the candidate. Only then is the candidate returned. | as C |

**The durable commit point** is the creation of the name `result.json`. That happens only after the FINAL
record (Stage B) is durable and verified. A FINAL record without `result.json` is **not** a complete
experiment.

**Failure handling.** Every failure goes to `_finalization_failed()`:
- the returned result is INVALID / HALT, with `evidence_complete: false` and
  `finalization.state = FAILED` (`UNCERTAIN` if a published result could neither be retracted nor
  marked);
- `FINALIZATION_FAILED.json` is created exclusively, with the failure result;
- `S9 FINALIZATION-FAILED` is appended to the journal;
- quarantine applies when a mutation was applied;
- the observed outcome and the restoration status are **never rewritten**.

A pre-existing `result.json` is never overwritten. Publishing the failure marker is not a prerequisite
for halting; the returned HALT stands on its own.

**Consumer contract (`harness.validate_run_evidence(run_dir)`, machine-checkable):**

| State | Condition |
|---|---|
| COMPLETE | All of: `result.json` exists and parses; it declares protocol `wp-rd-b-f1-two-phase-v1` and `evidence_complete: true`; validity and batch action are consistent (VALID/CONTINUE or INVALID/HALT); the journal is fully parseable and gap-free from seq 1; its **last** record is `S9 FINAL`, binding `sha256(result.json)` and the run id; no failure marker exists; any pending candidate is byte-identical. |
| PENDING | No `result.json`, but a pending candidate exists. **Never authoritative.** |
| FAILED | `FINALIZATION_FAILED.json` is present. |
| INCOMPLETE | Anything else. |

Only COMPLETE is authoritative. The invariant checker of every state-machine test enforces this
contract, and F1-T9 enforces it on 13 constructed evidence variants.

**Crash-interval analysis** (what an observer can find, and why it is never a false VALID):

| # | Interval | Possible on-disk state | Consumer verdict |
|---|---|---|---|
| 1 | before the pending file is created | journal ends with the S9 intent record | INCOMPLETE |
| 2 | during pending write / fsync | partial or complete pending file only | PENDING |
| 3 | after pending verified, before FINAL | pending file only | PENDING |
| 4 | during FINAL append / fsync | journal has a partial final line, or a FINAL line that may not be durable; no `result.json` | INCOMPLETE / PENDING |
| 5 | after FINAL, before publication | FINAL is the journal tail; no `result.json` | PENDING (F1-T7a) |
| 6 | during `os.link` | atomic: either no `result.json`, or a `result.json` that is the bound, fsynced inode | PENDING, or COMPLETE with valid binding |
| 7 | after link, before directory fsync / confirmation | `result.json` may or may not survive a crash. If it survives it is the bound candidate, and its FINAL was already durable (journal data and directory entry fsynced). | COMPLETE (genuinely complete) or PENDING; never a false VALID |

**Residual limitations (not eliminated by this narrow change):**
- Directory fsync is implemented only on POSIX. Elsewhere `_fsync_dir()` raises, so finalization fails
  closed (INVALID). It never claims durability.
- Durability ultimately depends on the filesystem honouring `fsync`. A filesystem without hard links
  makes publication fail closed.
- If, after a successful publication, a later step fails **and** both the retraction and the failure
  marker fail, `finalization.state = UNCERTAIN`: the returned result is INVALID / HALT, but a COMPLETE
  `result.json` may remain. In that case the evidence genuinely is complete (FINAL durable, binding
  valid), so it is not a *false* VALID. It is reported as UNCERTAIN, not as success.
- A `SIGKILL` of the harness process ends at whichever interval it hits. The table above shows that
  none of them produces a false VALID.

## 5. Bytecode isolation (R1 §7.3, with the CEO implementation clarification)

- Each top-level command (phase process tree) gets **one fresh, empty `PYTHONPYCACHEPREFIX`
  directory**, together with `PYTHONDONTWRITEBYTECODE=1`. Child processes inherit both through the
  environment. **The guarantee is "one fresh empty prefix per top-level process tree, bytecode
  writes disabled throughout the tree, prefix verified empty afterwards". It is not "one prefix per
  process".**
- The interpreter probe must show `pycache_prefix` equal to the expected directory,
  `dont_write_bytecode`, and `isolated`, `ignore_environment`, `no_site` and `optimize` all 0. The
  probe also requires that no `sitecustomize` or `usercustomize` is importable without the hook.
- The flags `-I`, `-E`, `-S`, `-O` and `-X pycache_prefix` are refused in command argv. The
  environment variables `PYTHONPATH`, `PYTHONSAFEPATH`, `PYTHONOPTIMIZE`, `PYTHONPYCACHEPREFIX`,
  `PYTHONDONTWRITEBYTECODE`, `PYTHONINSPECT` and `ACE_ATTEST_*` are refused in the base environment.
- `PYTHONDONTWRITEBYTECODE=1` alone does **not** prevent reading an existing stale `.pyc` (test D2).

## 6. Code-identity attestation (R1 RD-C6)

- Verdict-bearing commands run exactly as registered (no wrapper, no `runpy`).
- `attest_hook/sitecustomize.py` is injected through `PYTHONPATH` and is inert unless
  `ACE_ATTEST_OUT` is set. It writes `<pid>.start.json` at interpreter start-up and `<pid>.end.json`
  from `atexit`. It never prints, never changes the exit status, and never imports a target. It reads
  targets only from `sys.modules`, through `__dict__` lookups.
- Code identity is compared **structurally**: `co_code`, constants (recursively), names, varnames,
  line and position tables, flags and argument counts. It is not compared by `marshal` bytes.
- The harness fails closed on any of these:
  - a missing start or end record (including timeout, `SIGKILL`, `os._exit`, default `SIGTERM`);
  - malformed or unexpected record files;
  - a hook error record;
  - a hook SHA-256 mismatch;
  - a process outside the observed process tree;
  - a Python child count that does not match the registered expectation;
  - a required target not loaded;
  - a loaded digest that differs from the expected digest (computed by the harness from the bytes it
    expects on disk), or a hook-reported disk mismatch;
  - interpreter flags in a start record that differ from the protocol;
  - a non-empty cache prefix.
- **A child is "directly attested" only when its own valid start and end records exist.** Inheriting
  the environment is not attestation. A child started with `-I`, `-E` or `-S` bypasses the hook, and is
  caught only by the registered child-count rule.
- **ACE process accounting is not hard-coded.** Each command carries an explicitly registered
  expectation (`children_on_pass`, `children_min_on_fail`). There is no default; a missing expectation
  fails closed.

## 7. Git status (R1 §5.3, RD-C2, RD-C3)

`git status --porcelain=v2 -z --untracked-files=all --ignored=matching --no-renames`, captured as raw
bytes (never `.strip()`). `split_records`, `parse_records` and `classify` validate every field. A
record is allowed only as a type-1 `.M` change on an **exact** allow-listed path. Untracked,
renamed/copied, unmerged, staged and deleted records are outside the allow-list. New ignored paths are
reported separately. A git failure or parse error is never an empty success.

**Observed granularity (git 2.43):** `--ignored=matching` reports a wholly ignored directory as **one
collapsed entry** (for example `__pycache__/`), not per file. A new file inside an already-ignored
directory therefore produces no new entry. Two measures compensate:
- S0 requires an **empty** ignored set before the baseline (the hygiene rule, test C7d), so any ignored
  entry that appears later is new;
- the harness separately scans the worktree for `__pycache__` and `.pyc` files.

The CEO-mandated flag is unchanged.

## 8. Required acceptance evidence

Parser tests T1–T18; the rename matrix RN-1 to RN-6b; parser mutants MP-1 to MP-10 (including MP-3b,
MP-4b, MP-7b), applied as exact-once source mutations of `gitstatus.py`; bytecode tests D1–D9;
equivalence tests E1–E14; state-machine tests C1–C13 (C5 → T10; C7a, C7b, C7c-1 to C7c-4, C7d, C8b);
the 16-case restoration-validity truth table; and the integrated fixture demonstration. The withdrawn
`.strip()` parser control is not reinstated.

## 9. Amendment B (recorded for design consistency only)

For the future WP-RD-A work package, `classifier_sign_shared` is expected to be detected by
`verify_composition()` only. The ordinary dense sweep stays a separate check of the unmodified
classifier, and must not be claimed to have observed a mutation introduced later. Attribution must
report a classification defect when the chart matches the mutated classifier but disagrees with the
independent reference. **No D45 change is made under WP-RD-B.**

## 10. Recorded deviations from the R1 text

| Item | R1 text | Implementation | Reason |
|---|---|---|---|
| C7a legacy reproduction | Load `apply_edits` / `sh` "unmodified from `wpn1_harness.py`" | `fixtures/legacy_wpn1.py` contains a verbatim transcription of `sh()`, `apply_edits()` and `git()` (archived L180–L188, L204–L214), plus a characterization of the L274–L305/L336 sequence | The archived harness is historical WP-N1 evidence outside the repository, and committing it is not authorized. AST equality of the transcribed functions with the archived file was checked at implementation time (see `IMPLEMENTATION_EVIDENCE.md`). |
| Batch rule T4b | Continue if the pre-check error is local | Every INVALID experiment halts | A conservative simplification (§4) |
| Edits | Multiple files possible in principle | One target file per experiment; several whole-line edits in that file are allowed | This keeps the baseline/mutated/unknown hash classification of Amendment A exact. |
| Prefix per process | "One fresh prefix per process" | One fresh prefix per top-level process tree | §5; the CEO implementation clarification |
| Additional controls | Not in R1 | Harness mutant-kill matrix HM-1 to HM-10 (exact-once source mutations of `harness.py`), and an S6 attestation-failure test | They give the restoration rules the same "the detector can fail" evidence that the parser has |
| Additional files | Six test files listed | `tests/helpers.py` (shared non-test helpers); `fixtures/__init__.py`, `fixture_repo.py`, `legacy_wpn1.py`, `run_demo.py` | Shared fixture code and the Phase 5 demonstration. No `conftest.py` is added: each test module sets its own import path explicitly, so collection has no implicit side effects. |
| Default-mode control runs | Not specified | They use a disposable copy of the hook (`tests/helpers.disposable_hook_dir`) | Without `PYTHONDONTWRITEBYTECODE`, CPython writes a `.pyc` of the hook into its own directory, which `verify_hook` correctly refuses. This was observed during implementation. |

## 11. Unresolved owner decisions

- The repository location is authorized for this branch only. Whether it merges remains an owner
  decision (OQ-1).
- ADR-0099 s3 interaction (OQ-10): the harness is outside the verification surface. See
  `IMPLEMENTATION_EVIDENCE.md` for the name-matched call-site review.
- Adoption of the `restoration_status` / `experiment_validity` vocabulary as project vocabulary
  (OQ-4).
- Any use against an ACE target (WP-N2 or a pristine U-vs-H equivalence run). Not authorized.
- Recording this work in `docs/DECISION_LOG.md` (OQ-6). Not done; owner decision.
