# WP-RD-B implementation evidence (fixture testing only)

**Builder-produced verification record. Not a certification result and not CEO approval.**
Nothing here certifies any ACE capability or discharges any qualification. Every result below
was executed, not projected. Raw logs and demonstration evidence are kept **outside** the
repository; their SHA-256 values are listed so they can be checked.

## 1. Baseline and environment

| Item | Value |
|---|---|
| Branch / base | `wp-rd-b-mutation-harness`, created from `main` = `origin/main` = `6538930c2832b49de54c31edad4614e265a86695`, in a new isolated worktree |
| Design baseline | R1 packet, SHA-256 `b3ed57865c1986cd7d24f85d4513aee31389f58ffc7c9ccf066ed4c622efac82` (verified before implementation), plus CEO amendments A and B |
| Test host | WSL2 Ubuntu 24.04.5 (Linux 6.18.54.1-microsoft-standard-WSL2), CPython 3.11.17 (`~/ace-mut/venv-base`), pytest 9.1.1, git 2.43.0. No package was installed or upgraded. |
| ACE code executed | **None.** No ACE certifier, validator, gate or engine module was run, imported or mutated. The harness refuses ACE targets (`ACE_TARGET_MARKERS`). |

## 2. Test execution (final run, frozen source)

Command, run from the worktree root (`/mnt/c/Users/Nidhi/ace-wt/wp-rd-b-mutation-harness`):

```
PYTHONDONTWRITEBYTECODE=1 ~/ace-mut/venv-base/bin/python -m pytest -p no:cacheprovider -q -rA \
    --junitxml=<logs>/<suite>.junit.xml tools/mutation_harness/tests/<suite>.py
```

| Suite | Tests | Passed | Failed | Errors | Skipped | Exit |
|---|---|---|---|---|---|---|
| test_gitstatus | 25 | 25 | 0 | 0 | 0 | 0 |
| test_gitstatus_mutants | 16 | 16 | 0 | 0 | 0 | 0 |
| test_rename_matrix | 11 | 11 | 0 | 0 | 0 | 0 |
| test_bytecode | 10 | 10 | 0 | 0 | 0 | 0 |
| test_hook_equivalence | 24 | 24 | 0 | 0 | 0 | 0 |
| test_state_machine | 43 | 43 | 0 | 0 | 0 | 0 |
| **Total** | **129** | **129** | 0 | 0 | **0** | — |

Logs and JUnit files (SHA-256; kept outside the repository):

```
11cff2c7c1c6d88803895a8164970f2102cf989eb7043bc661248d12b1c4771b  test_gitstatus.log
4ef964163ee0ca2e870b4cfe58bcd650d163938f74670437c0dac5966a676b57  test_gitstatus.junit.xml
a800ed72babd29fb5c16cb83d457079f15fe49dd0a25a85fcde2813fc3c51212  test_gitstatus_mutants.log
a77b536ea7dbd9639aa23c4e1484087ae627e47083ec8ec48dc091ff1fdd0b6b  test_gitstatus_mutants.junit.xml
c529bc42233b585dbf4ae96ea8e447bc7df448af8568ca4aac148fef519ad1e1  test_rename_matrix.log
9643a197993c35aa4f93a11cea3b4e39821279cd7ccaac14262a6ca7a148d685  test_rename_matrix.junit.xml
5ad72ffe311be4ab36d7d85160e98e48276b2d1fd3edce730fca99eb41ae0474  test_bytecode.log
85b3c470a2e4d2b7221c7d91220510f6fc57857956050a979d190c806534c86c  test_bytecode.junit.xml
fb417aedffffc31a35307d5c0e2cc73c039723564ec97849dfc1c6ff4ed6f191  test_hook_equivalence.log
9e7ad106cbc33bdcb43cf4d4611a8fb146a6dea14b8023807b5f59741b594b28  test_hook_equivalence.junit.xml
c035d5a40cfb8339b5a6a9241b10dcfad830d525e85bd0d07e1821e2d64b96db  test_state_machine.log
7e9a45e6fd30611a019410b863018ddd939e7fd713d2a010d11b17a42b10d89d  test_state_machine.junit.xml
8d2265581d8b1e994bab4bef847739a739c62cb74e4432ddf187aa5b55219ec8  exit_codes.txt
2623afa775116e41371c7c1dca7df9e906d61ad3c3b9ce291583acf6fbf3b3e8  interpreter.txt
```

After every run, the worktree was checked for `__pycache__`, `*.pyc` and `.pytest_cache`. None
were found.

## 3. Negative controls

### 3.1 Parser mutants (exact-once source mutations of `gitstatus.py`; all killed)

| Mutant | Defect introduced | Designated detector | Kill evidence |
|---|---|---|---|
| MP-1 | path taken without `maxsplit` | T7b | AssertionError (truncated path allowed) |
| MP-2 | short type-1 record accepted | T11 | AssertionError (no parse error) |
| MP-3 | rename origin token not consumed | T6 | StatusParseError / AssertionError |
| MP-3b | type-2 records dropped | T6 | AssertionError |
| MP-4 | allow-list entry used as a prefix | T15 | AssertionError |
| MP-4b | directory-prefix acceptance (the WP-N1 rule) | T16 | AssertionError |
| MP-5 | XY ignored | T5 | AssertionError |
| MP-6 | untracked records discarded | T3 | AssertionError |
| MP-7 | ignored records discarded | T12 | AssertionError |
| MP-7b | ignored-baseline comparison inverted | T12 | AssertionError |
| MP-8 | unknown record type tolerated | T14 | AssertionError |
| MP-9 | truncated output tolerated | T13 | AssertionError |
| MP-10 | git failure read as empty output | T17 | AssertionError |

Each detector also passed against the unmutated module in the same test (the pristine control).
Mutants are compiled from mutated source **text** in memory; `gitstatus.py` on disk is never changed.
The withdrawn `.strip()` control is not used. It is shown to be equivalent on well-formed v2 `-z`
output.

### 3.2 Restoration-rule mutants (exact-once source mutations of `harness.py`; all killed)

| Mutant | Defect introduced | Designated detector | Result |
|---|---|---|---|
| HM-1 | INDETERMINATE no longer dominates | dominance table | killed |
| HM-2 | a check that did not run counts as passed | dominance table | killed |
| HM-3 | unknown restored bytes become RESTORATION-FAILED (Amendment A) | C5 | killed |
| HM-4 | validity ignores restoration status | 16-case truth table | killed |
| HM-5 | interruption after mutation upgrades to RESTORED-VERIFIED | C9 | killed |
| HM-6 | S8 attestation failure ignored | C7c-3 | killed |
| HM-7 | S6 attestation failure does not void the observation | S6 attestation test | killed |
| HM-8 | batch continues after INVALID | C12 | killed |
| HM-9 | S7 restores from an unverified backup | C4 | killed |
| HM-10 | S8 timeout with unknown hash classified as failed | C8b | killed |

A kill requires an `AssertionError` from the detector. Any other exception fails the test.

### 3.3 Bytecode and attestation controls

- **D1, D2, D4 and D8-control** reproduce stale-bytecode execution, and the hook reports
  `disk_match: false` in each.
- **D8-protocol and E11(c)** show that a planted, header-valid stale `.pyc` is bypassed under the
  protocol and left byte-identical.
- **E9 / E10 / E12 / E13 / E14:**
  - timeout, `os._exit` and `SIGTERM` (no `atexit`) each fail closed;
  - deleted, truncated, field-missing and foreign-pid records each fail closed;
  - an `-I` child is not attested and fails the child-count rule;
  - a child-count deviation fails;
  - a hook SHA-256 mismatch fails, and a polluted hook directory is refused.

## 4. Failures observed during implementation, and repairs (all within the harness scope)

1. **`--ignored=matching` granularity** (test expectation corrected). The first version of the
   ignored-entry test expected per-file entries. Git 2.43 reports a wholly ignored directory as one
   collapsed entry (`__pycache__/`). The CEO-mandated flag was kept. The test now asserts the observed
   behaviour, and a second test documents the limitation; S0's empty-ignored-set hygiene rule (C7d)
   and the harness's own `.pyc` scan compensate.
2. **Hook-directory pollution in default-mode control runs** (test design corrected). Running the hook
   *without* the protocol made CPython write `attest_hook/__pycache__/sitecustomize.cpython-311.pyc`.
   `verify_hook()` refused the polluted directory, which is correct behaviour. Control runs now use a
   disposable copy of the hook. The generated file was removed from this new worktree only.
3. **Emergency-restore defect** (implementation bug, found by C9). `_emergency_restore` passed
   `action=` to `Journal.append`, whose positional parameter is also named `action`. The resulting
   `TypeError` meant the safety restore never executed after an interruption. The run still failed
   closed (INDETERMINATE / INVALID / HALT, quarantined), but the target stayed mutated. The field was
   renamed `restore_action`. C9 now asserts that the emergency restore happened and that no
   emergency-restore failure was recorded. HM-5 guards the status rule.
4. **Symlink guard defect** (found by builder self-audit). The symlink check ran on the already
   resolved path, so it could never fire. It now checks the unresolved path; test
   `test_symlinked_target_is_refused` was added.

## 5. Integrated fixture demonstration (Phase 5)

`fixtures/run_demo.py`, run on the frozen source, exited 0. Evidence archive:
`WPRDB_DEMO_EVIDENCE.tar.gz`, SHA-256 `be0f54311e896691c112ee386b3fc35d7d05a7f3dfeb8232ca9d33266555aba3`.
Summary SHA-256: `c240405a6d39e06ce3d86e38554e401e44e713031044120fc2b37e5d620b5594`.

| Scenario | outcome | restoration_status | validity | batch | Next experiment in batch | Quarantined |
|---|---|---|---|---|---|---|
| 1 detected | DETECTED | RESTORED-VERIFIED | VALID | CONTINUE | ran (DETECTED, VALID) | no |
| 2 undetected | UNDETECTED | RESTORED-VERIFIED | VALID | CONTINUE | ran | no |
| 3 equivalent | EQUIVALENT | NOT-APPLICABLE | VALID | CONTINUE | ran | no |
| 4 known restoration-verification failure | DETECTED | RESTORATION-FAILED | INVALID | HALT | NOT-STARTED | yes |
| 5 unknown restored bytes | DETECTED | INDETERMINATE | INVALID | HALT | NOT-STARTED | yes |
| 6 missing attestation | DETECTED | RESTORATION-FAILED | INVALID | HALT | NOT-STARTED | yes |
| 7 legacy method | DETECTED (legacy) | `restoration_ok: false`, hash matched | (not represented) | legacy: no halt | — | — |
| 7 protocol, same forced timing | DETECTED | RESTORED-VERIFIED | VALID | CONTINUE | — | no |

**Scenario 7, legacy run:**
- the restored gate exited 3, with the mutated signature `house_number=10 expected=4`;
- the fixture `.pyc` header matched the restored source;
- the cached code was structurally equal to the **mutated** text, and not to the restored text.

**Scenario 7, protocol run:** zero `.pyc` files in its repository.

## 6. Legacy transcription check

`fixtures/legacy_wpn1.py` functions `sha`, `sh`, `git` and `apply_edits` are **AST-identical** to
the archived WP-N1 harness (`wpn1_harness.py`, SHA-256
`62d0a1156b336c49690a7c8a8013ef17429bf5c0777660dbeaec2098d1e8efd1`, read-only, from the closeout
copy). `legacy_sequence` is a characterization and is not verbatim.

## 7. Governance review (ADR-0099 "in use")

- **No call path into ACE code.** The harness and its tests import nothing from `engine/`, `scripts/`
  or any `validate_*.py` (verified by search), so no call path into an ACE capability exists (U1).
  None of their names is exported through an ACE public surface (U2).
- **Name-matched collisions.** Under ADR-0099 s3's name-matched counting rule (`\b<name>\s*\(`), seven
  identifiers in this directory coincide with names of callables defined in non-test `engine/`
  modules:
  - `classify` (the directive-mandated parser function; engine `classify` is the varga classifier);
  - `get`, `set`, `resolve` (Python built-ins and methods; engine `knowledge` cache/registry methods);
  - `main`, `walk` (`ast.walk`), `__init__`.

  These are textual collisions only. The engine capabilities are not called. **This is recorded as an
  ambiguity of the regex counting rule** (C4, the executed reachability check, remains unauthorized).
  It is not treated as making any capability "in use".
- **Corpus membership.** The directory is outside ADR-0099's verification surface. It writes nothing
  into `certification/` or `reports/certification/`, and adds no member to the ADR-0102 26-file
  corpus.

## 8. ACE child-process accounting: what is and is not established

From read-only source inspection at `6538930`:
- `scripts/certification_support.py` spawns no subprocess, but registers `atexit` handlers. The hook's
  handler, registered earlier at `site` import, runs after them.
- No production `engine/` module uses `subprocess`.
- The certifiers' Python children are `subprocess.run([sys.executable, validator])` without `env=`
  (`certify_d45.py` L237, L375; `certify_parashari_yoga.py` L312, L694). They would therefore inherit
  the protocol and the hook.
- **Not established:** whether third-party code (for example PyJHora in D45 Gate C) starts Python
  subprocesses. **No ACE child count is registered.** Using the harness on ACE requires an
  authorized pristine equivalence run to establish those counts.

## 9. Known limitations (builder disclosure)

- **POSIX only, and narrowly verified.** Verified on one host with CPython 3.11.17. Windows and
  CPython 3.12 were not run.
- **Directory-granular ignored reporting** (§4.1). It is mitigated, not eliminated.
- **PID reuse** within one attested command is not handled.
- ~~**The result file can disagree with the journal on one rare path.**~~ **Corrected by
  WP-RD-B-F1 (§10).** In `4318b31`, if appending FINAL failed after `result.json` had been written, the
  persisted file still said VALID. That ordering is replaced by two-phase finalization, under which no
  `result.json` exists before a durable, verified FINAL record. This was the CEO audit's blocking
  finding RD-B-F1.
- **A duplicate `run_id`** raises from `run_batch` before anything executes. It fails closed, but
  produces no result record.
- **`SIGKILL` of the harness process** leaves a write-ahead journal without FINAL and may leave the
  target mutated. Recovery is manual, guided by the journal and the retained backup.
- **The harness process's own bytecode** is not controlled by the harness. The README instructs
  `PYTHONDONTWRITEBYTECODE=1`.
- **The fixture certifier imitates only the shape of ACE Gate I/J.** Behaviour on ACE certifiers is
  unverified.

## 10. WP-RD-B-F1 correction: durable finalization before VALID publication

Sections 2–9 describe the original WP-RD-B run at `4318b31`. This section records the owner-approved
correction under CEO directive WP-RD-B-F1. The protocol is specified in `DESIGN_CONTRACT.md` §4a.

**Root cause (at `4318b31`, `harness.py`).** In `_finalize()`, `result.json` was written, fsynced and
verified (L729–L733) before the mandatory `S9 FINAL` journal append (L734). The failure branch
(L738–L748) changed only the returned dict, so a FINAL failure left a persisted VALID/CONTINUE
`result.json`.

**Correction.** Two-phase finalization:
1. a pending candidate;
2. a durable, verified FINAL record binding the candidate's SHA-256;
3. atomic, no-replace `os.link` publication of `result.json`;
4. confirmation by the consumer contract `validate_run_evidence()`.

Supporting changes:
- fail-closed `_finalization_failed()`: INVALID / HALT, a retraction of our own publication, the
  `FINALIZATION_FAILED.json` marker, and a journal note;
- the journal directory is fsynced at creation;
- the SIGTERM handler now also covers finalization.

The invariant checker of every state-machine test now also enforces the consumer contract.

**Regression demonstration.** F1-T1 was run against the original `4318b31` `harness.py`, exported from
the committed tree (blob `b0172c024648f3ff04697ceb69e3b1201e66a049`), with the new test files overlaid:
- **rc 1, FAILED**: "an authoritative result.json existed before the FINAL record was attempted"
  (log `ed9c423d…ba9d`, JUnit `ae0ef43f…c827`);
- the same test against the corrected code: **rc 0, PASSED** (log `7a2d0742…74d8`).

**Final run** (frozen source; same host, interpreter and command form as §2):

| Suite | Tests | Passed | Failed | Skipped | Exit | Log SHA-256 |
|---|---|---|---|---|---|---|
| test_gitstatus | 25 | 25 | 0 | 0 | 0 | `7565ae8d76c82ac32695384ae1e68ab93d82465a0f2098ce679cf07dd888dd2b` |
| test_gitstatus_mutants | 16 | 16 | 0 | 0 | 0 | `9c0e417773b69ca0f59804d8c0d7017fb92e6f8f8e90cd8e392fd8c560764206` |
| test_rename_matrix | 11 | 11 | 0 | 0 | 0 | `6336602ee46a0e370fb42d1923cd10bccd58babd8e944b71999df90d1ab44f14` |
| test_bytecode | 10 | 10 | 0 | 0 | 0 | `02f6fadab98fd0c335438ad17e38333d783d7803b48541c6f1b381399e0ff63c` |
| test_hook_equivalence | 24 | 24 | 0 | 0 | 0 | `977c69d9fa872858f8954d41e02a30aee0e1cf8ae243ee6d3b702c3340f22b32` |
| test_state_machine | 43 | 43 | 0 | 0 | 0 | `3e64fb7c1a6f4d34729c46a0ea6cd14e362b16aa9226ddf2cb1df879e769d18a` |
| test_finalization (new) | 18 | 18 | 0 | 0 | 0 | `2234659a9b25c1175a16f2401d1d36bdc2b9cabe74ffef386cb4db9e49f524f1` |
| **Total** | **147** | **147** | 0 | **0** | — | `exit_codes.txt` `4e6dfee7…0c81` |

**F1 negative controls** (exact-once source mutations of `harness.py`). Every pristine detector
passed, and every mutant was killed by an AssertionError (`fm_kill_evidence.jsonl` `acffb79c…2ae2`):

| Mutant | Defect | Detector | Killing assertion |
|---|---|---|---|
| FM-1 | original premature ordering (publish before FINAL) | F1-T1 | result.json existed before FINAL was attempted |
| FM-2 | FINAL durability verification removed | F1-T2b | failure stage is not `final-verify` |
| FM-3 | pending-candidate integrity check bypassed | F1-T4 | the corrupt candidate was bound by FINAL; it failed later, at `confirm` |
| FM-4 | consumer ignores the FINAL binding | F1-T9 | variant `final-binds-other-bytes` accepted |
| FM-5 | publication overwrites an existing `result.json` | F1-T8 | the pre-existing file was not preserved |
| FM-6 | a published result is not retracted after a later failure | F1-T7b | the persisted result.json claims VALID |

All 13 parser mutants and 10 restoration mutants remain killed (the suites above).

**Integrated demonstration** (corrected code, rc 0). The same seven scenario results as §5. The
consumer contract reports **COMPLETE** for every scenario's evidence, including the INVALID
experiments, whose INVALID verdicts are themselves fully finalized. Evidence:
- `WPRDB_F1_DEMO_EVIDENCE.tar.gz`, SHA-256 `74d85840e7b657c838eed3762d487a6d5a50ff9b99832c46f5512d52751b8d71`;
- consumer check `e25dd6b3…d837`;
- summary `714abeb2…eadb`.

**Unresolved and not remediated here** (they need separate authorization): the ADR-0099 name-matching
ambiguity, ACE child-process counts, cross-version/Windows testing, PID reuse, a duplicate `run_id`
raising, and the residual windows listed in `DESIGN_CONTRACT.md` §4a.
