# tools/mutation_harness — WP-RD-B certification mutation harness

**Status: FIXTURE-TESTED ONLY. This is NOT an approved production-mutation harness.**

This harness has been exercised only against disposable fixture repositories. It refuses any
ACE target: `harness.ACE_TARGET_MARKERS` detects `engine/astrology` or `scripts/certify_d45.py`.
Using it against ACE code (WP-N2, or a pristine equivalence run) requires a separate owner
authorization and a deliberate code change. The governing contract is
[`DESIGN_CONTRACT.md`](DESIGN_CONTRACT.md); the verification record is
[`IMPLEMENTATION_EVIDENCE.md`](IMPLEMENTATION_EVIDENCE.md).

## What it does

It runs one mutation experiment as a fail-closed state machine, S0 to S9 (`harness.py`):
1. preregister;
2. run a clean attested baseline;
3. run the pre-check;
4. take a byte backup;
5. apply the registered mutation;
6. run the attested observation;
7. restore from the backup (never by reverse text edit);
8. run the verification (hash, exact allow-list git status, designated gate, end-to-end, final hash,
   final status);
9. finalise the evidence.

It reports three separate dimensions:
- `outcome`: the unchanged WP-N1 vocabulary;
- `restoration_status`: INDETERMINATE > RESTORATION-FAILED > RESTORED-VERIFIED, with NOT-APPLICABLE
  when no mutation was applied;
- `experiment_validity`.

A batch halts after any INVALID experiment.

| Module | Responsibility |
|---|---|
| `gitstatus.py` | `git status --porcelain=v2 -z --untracked-files=all --ignored=matching --no-renames`, captured as raw bytes, with strict record parsing and exact allow-list classification |
| `pyenv.py` | Protocol environment: one fresh empty `PYTHONPYCACHEPREFIX` per top-level process tree, plus `PYTHONDONTWRITEBYTECODE=1`. Also the interpreter probes, structural code identity, process-group execution, and fail-closed attestation evaluation. |
| `attest_hook/sitecustomize.py` | Code-identity attestation hook, injected through `PYTHONPATH`; inert unless `ACE_ATTEST_OUT` is set |
| `harness.py` | State machine, write-ahead journal, quarantine markers, batch control, test-only fault points |
| `fixtures/` | Disposable fixture repository builder, the verbatim legacy WP-N1 transcription (for C7a), and the integrated demonstration |
| `tests/` | The acceptance suites (below), plus `helpers.py`, a shared non-test helper |

## Running the fixture tests

They need a POSIX host: process groups, `SIGTERM` semantics and file modes are used. The verified
environment is WSL2 Ubuntu 24.04, CPython 3.11.17 (with pytest 9.1.1) and git 2.43.0. No package is
installed by these tests.

```sh
cd <repository root>
PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider -q tools/mutation_harness/tests
```

`PYTHONDONTWRITEBYTECODE=1` and `-p no:cacheprovider` keep the checkout free of `__pycache__` and
`.pytest_cache`. The repository's default gate (`python -m pytest -q`) does **not** collect these tests,
because `pytest.ini` sets `testpaths = engine/tests`. All temporary repositories are created under the
pytest temporary directory.

| Suite | Contents |
|---|---|
| `test_gitstatus.py` | Parser and classification tests T1–T18 |
| `test_gitstatus_mutants.py` | Parser mutant-kill matrix MP-1 to MP-10 (exact-once source mutations of `gitstatus.py`) |
| `test_rename_matrix.py` | Rename matrix RN-1 to RN-6b on real git, plus the ignored-entry granularity tests |
| `test_bytecode.py` | Bytecode isolation D1–D9, plus hook/harness structural-identity agreement |
| `test_hook_equivalence.py` | Hook equivalence E1–E14, the probe, and hook inertness |
| `test_state_machine.py` | State machine C1–C13 (amended C5, C7a–C7d, C8b), the 16-case truth table, precedence, validity, harness mutant-kill matrix HM-1 to HM-10, and the guards |
| `test_finalization.py` | WP-RD-B-F1 durable finalization: F1-T1 to F1-T10, plus finalization mutant-kill matrix FM-1 to FM-6 |

## Reading results: the consumer contract (WP-RD-B-F1)

A run's `result.json` is authoritative **only** if `harness.validate_run_evidence(run_dir)` returns
`state == "COMPLETE"`:
- the journal ends with the `S9 FINAL` record that binds `sha256(result.json)` and the run id;
- no `FINALIZATION_FAILED.json` marker exists;
- the result declares the two-phase protocol and `evidence_complete: true`.

The other states are never a success:
- `result.pending.json` alone is a non-authoritative candidate (`PENDING`);
- a failure marker gives `FAILED`;
- anything else is `INCOMPLETE`.

Do not read `result.json` without this check. See `DESIGN_CONTRACT.md` §4a.

Integrated demonstration (writes evidence outside the repository; the output must be under the
system temporary directory):

```sh
PYTHONDONTWRITEBYTECODE=1 python tools/mutation_harness/fixtures/run_demo.py /tmp/wprdb-demo-<stamp>
```

## What it does not establish

- Nothing about any ACE capability. It certifies nothing, and discharges no ADR-0083, ADR-0085 or
  ADR-0086 qualification.
- Direct attestation of ACE certifier child processes. The child-process accounting is
  fixture-verified, and ACE child counts are not registered (see the evidence file).
- Behaviour on Windows, or on CPython 3.12 (CI's second interpreter). Neither was run.
