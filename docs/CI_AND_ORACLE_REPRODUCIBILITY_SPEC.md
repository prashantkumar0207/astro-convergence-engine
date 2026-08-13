<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | PROPOSED - descriptive of the implementation delivered in Phase G commit 1; ADR-0018 is the normative record. Pending owner ratification (docs/OPEN_QUESTIONS.md Q1). |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-10 |
| Review cadence | TBD (see docs/OPEN_QUESTIONS.md Q1) |

# CI and Oracle Reproducibility Specification

Provenance note: this document is descriptive of the continuous-integration and
oracle-reproducibility implementation delivered in Phase G commit 1 (G6). The
normative record is `docs/DECISION_LOG.md` ADR-0018. It resolves audit finding
B-6 (CI coverage was a fraction of the local gate) and the oracle
reproducibility gap recorded in the Phase G plan section 5.

## 1. Problem this specification solves

`docs/VALIDATION_STANDARD.md` s2 rule 4 requires pinned dependencies and
checksummed data assets before any certification run, and s2 rule 5 makes a
skip a failure in a certification suite. Two conditions violated that standard.

First, CI ran the default pytest gate and exactly two of the eleven independent
holdout validators. Nine validators, the legacy kernel gate and all eleven
certification runners never ran in CI. Three of the four installed dependencies
were unpinned.

Second, and more seriously, the oracle environment was not reproducible from
the repository at all. `PyJHora` 4.8.7 declares an EMPTY `Requires-Dist`. Its
runtime imports therefore fail one at a time on a clean machine, and pip cannot
resolve them, because the package does not admit they exist. The certification
artifacts recorded `{"package": "PyJHora", "version": "4.8.7"}` and the Python
version, and nothing else. An engineer with only this repository could not have
recreated the environment that produced the eight oracle certifications.

A certification whose environment cannot be recreated is a report, not proof.

## 2. The two tiers

The gates partition cleanly, verified by inspection: no file under
`engine/tests/` and no `validate_*.py` imports `jhora`.

**Hermetic tier.** The default pytest gate, all eleven independent holdout
validators, the legacy kernel gate, and three certification runners
(`certify_current_engine.py`, `certify_kp_chain.py`,
`certify_sign_convention.py`). No external oracle, no network. Their references
are the bundled `swetest` binary, the certified legacy kernel, and
independently constructed in-file reference implementations.

**Oracle tier.** Eight certification runners that compare against PyJHora:
`certify_d2.py`, `certify_d3.py`, `certify_d7.py`, `certify_d12.py`,
`certify_d30.py`, `certify_vimshottari.py`, `certify_transits.py`,
`certify_parashari_drishti.py`.

The split exists for reproducibility and outage isolation. It MUST NOT be used
to reduce coverage. This change ADDED nine validators, the legacy gate and
three certification runners to CI; it removed nothing.

## 3. Oracle environment identity

`certification/ORACLE_ENVIRONMENT.json` is the machine-readable record. It MUST
carry, and currently carries: operating system and architecture; Python version
and implementation; the ABI constraint that the recorded hashes are CPython
3.11 linux x86_64 wheels; PyJHora version and the explicit statement that it
declares no dependencies; the six undeclared runtime dependencies and how they
were discovered; the Swiss Ephemeris binding version, the reported library
version, and the SHA-256 of the bundled `swetest` reference binary with its
build provenance; the ephemeris asset checksums and the fact that
`certification_support.preflight()` verifies them before every run; the
dependency lock filename, its own SHA-256, the exact install command, and the
full 35-package closure; and the per-runner oracle invocation method.

The oracle invocation record names, for each runner, the exact PyJHora function
compared against, or the methodology where the comparison is not a direct
function call:

- `certify_vimshottari.py` uses the **D-007 Moon-injection methodology**: the
  oracle's own Moon longitude is injected into this engine's timeline so the
  comparison isolates timeline mathematics from oracle astronomy. The engine's
  own Moon remains swetest-certified per D-001. Per-case Moon deltas are
  recorded in the artifact.
- `certify_transits.py` derives tolerances **per event from measured deltas**.
  The oracle Sun differs from the certified Sun by approximately 20.5 arcsec at
  compared instants. The magnitude is consistent with aberration-handling
  differences and **the cause is recorded NOT VERIFIED**. Tolerances are never
  assumed and never widened to absorb the divergence.

PyJHora is a comparison oracle and never astronomical ground truth. Root D-001
fixes the numerical authority as swetest 2.10.03; root D-007 governs how oracle
divergence is handled.

## 4. Dependency lock

`requirements-oracle.lock` pins 35 packages, every one with a SHA-256 hash, and
MUST be installed with `--require-hashes`. It is self-contained: base runtime
pins (`pyswisseph`, `tzdata`, `jsonschema`, `pytest`) are included alongside
PyJHora and its closure, so a single file plus a clean interpreter reproduces
the oracle environment. The base pins agree with `requirements.lock` and
`engine/requirements-lock.txt`.

The six dependencies PyJHora requires but does not declare are `numpy`,
`geocoder`, `pytz`, `timezonefinder`, `geopy` and `python-dateutil`. They were
discovered by iterative import-failure resolution inside a virtual environment
with no system site-packages: install, re-invoke, repeat until the runner
completed. This is recorded because the discovery method is the only reason the
list can be trusted, and because a future PyJHora version may change it.

A different Python minor version or platform MUST get its own lock file and its
own recorded environment identity. It MUST NOT be obtained by relaxing hashes
or by dropping `--require-hashes`.

## 5. CI workflow

`.github/workflows/ci.yml` defines two jobs.

`hermetic` runs on Python 3.11 and 3.12. It installs from `requirements.lock`,
records the environment, verifies ephemeris checksums against
`CHECKSUMS.sha256`, runs the default gate, all eleven validators, the legacy
kernel gate and the three non-oracle certification runners; then re-runs a
representative subset with the network blocked by
`scripts/ci_no_network.py`; then runs a negative control proving the network
guard actually blocks; then asserts no source file was modified by a
certification run.

`oracle` runs on Python 3.11 only, matching the recorded ABI constraint. It
installs from `requirements-oracle.lock` alone with `--require-hashes`, prints
the recorded identity next to the actual runner identity, asserts they match
via `scripts/check_oracle_environment.py`, verifies ephemeris checksums, runs
all eight oracle certification runners, shows the regenerated artifact delta,
and uploads artifacts, human-readable reports and console transcripts as build
evidence.

**Prohibited, and absent from this workflow:** `continue-on-error` anywhere; any
step that converts a failure into a warning; any skip of a validator or
certification runner; removal of a gate that existed before this change.

### 5.1 Hermeticity guarantee, stated exactly

`scripts/ci_no_network.py` blocks `socket.socket.connect`,
`socket.socket.connect_ex`, `socket.create_connection`, `socket.getaddrinfo`
and `socket.gethostbyname` inside the running process, which is the path every
Python HTTP, DNS and database client takes. It deliberately does NOT replace
the `socket.socket` class, because `ssl` subclasses it at import time and
swapping the class produces a false failure rather than a real one.

The guarantee is process-scoped and does not sandbox child processes. The
certification runners launch no network child processes; the only external
binary used anywhere in the gate is the bundled local `swetest`. The negative
control step exists so that a guard which silently stopped working is caught
rather than trusted.

## 6. Regenerating the lock

1. Create a virtual environment with no system site-packages on CPython 3.11,
   linux x86_64.
2. Install the intended base pins and `PyJHora==<version>`.
3. Run one oracle certification runner and install each missing module it
   reports, until the runner completes. Record the resulting list of undeclared
   dependencies.
4. `pip freeze` the environment to obtain the exact closure.
5. Resolve that closure with `pip install --dry-run --ignore-installed
   --report`, and take the SHA-256 of each resolved artifact from
   `download_info.archive_info.hashes`.
6. Write `requirements-oracle.lock` with one `--hash=sha256:` per package.
7. Update `certification/ORACLE_ENVIRONMENT.json`, including the lock file's own
   SHA-256.
8. Prove it: a NEW clean virtual environment, `pip install --require-hashes -r
   requirements-oracle.lock`, then all eight oracle runners must PASS.
9. Record the outcome in a decision entry.

Step 8 is the requirement. An environment that certifies only because packages
happened to already exist on the machine has proved nothing.

## 7. Verification performed for this specification

Executed 2026-08-10 on the baseline tree at `1f861f6`, in a virtual environment
created with no system site-packages:

- Hash-pinned install from `requirements-oracle.lock` alone: 35 packages
  installed, all hashes satisfied.
- All eight oracle certification runners: 8 of 8 PASS.
- Regenerated artifact delta versus the committed artifacts: the `date` field
  only. Every gate value byte-identical.
- Full hermetic set under `scripts/ci_no_network.py`: 395 tests pass, all eleven
  validators pass, legacy gate 5 of 5, all three non-oracle certifiers PASS.
- Negative control: a real connection attempt through the guard fails with
  `NoNetworkError`, exit code 1.
- `scripts/check_oracle_environment.py` returns 0 in the reproduced environment
  and 1 in a non-matching environment.

### 7.1 Remote verification on GitHub Actions, 2026-08-11

Section 7 above is the LOCAL verification and is preserved unchanged as dated
evidence. This subsection records the independent remote verification that
closed G6's remaining gap: proving the oracle environment reproducible outside
the sandbox that created it.

The `engine-ci` workflow executed on GitHub-hosted runners for commit
`a460ba2b7e4eac55f8ac2f51b9e9eb9a35607fda` on branch `phase-g-governance`.
Reported results: `hermetic` PASS on Python 3.11, `hermetic` PASS on Python
3.12, `oracle` PASS, overall workflow SUCCESS, and the
`oracle-certification-evidence` artifact produced.

This means `requirements-oracle.lock` installed with `--require-hashes` on
foreign hardware, the environment identity assertion passed there, and all
eight oracle certification runners passed there. The predicted risk that a
GitHub runner might resolve different wheels than the authoring container did
not materialize. No hash was relaxed, no dependency version changed, and the
lock was not regenerated.

Evidence class, stated exactly: these remote results were observed by the
CEO/technical auditor and reported to the builder. The builder has no network
access to the Actions API and did NOT independently observe them. The run URL,
run id, runner image and pip version were not supplied and are recorded as null
in `certification/G6_REMOTE_CI_VALIDATION.json` rather than guessed. That file
is the machine-readable record of this validation, including the per-item
evidence class for every claim.

## 8. Known limitations

The recorded identity is exact for CPython 3.11 on linux x86_64 and for no
other combination. The hermetic job runs on 3.12 as well, but the oracle job
cannot until a second lock exists.

`scripts/certify_tier0.py` remains broken at HEAD; it targets the historical
`astro_kernel` packaging and is superseded by the current gates. It is not
referenced by this workflow. Its disposition (repair, quarantine or removal by
decision) is Phase G commit 6 (G7) work and is deliberately untouched here.

The hermeticity guarantee is process-scoped, as stated in section 5.1.

Hash pinning protects integrity, not availability: if an index removes a
version, the job fails loudly rather than silently installing something else.
That is the intended behavior.

GitHub Actions emits Node.js 20 deprecation warnings for the action versions
this workflow pins. They are non-blocking and do not affect gate outcomes.
Recorded as technical debt `TD-CI-001` in
`certification/G6_REMOTE_CI_VALIDATION.json` by CEO direction. The G6 commit
MUST NOT be altered merely to silence them; they are addressed by a dedicated
CI-maintenance task with its own decision entry.

The GitHub Actions run identity for the 2026-08-11 validation is incomplete:
run URL, run id, runner image and pip version were not supplied to the builder.
Until they are added by additive amendment, the repository's record of that run
carries no resolvable pointer to it, which is a weaker evidence class than this
project's standard requires.

## 9. Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-10 | Created with Phase G commit 1 (G6). Records the two-tier CI split, the oracle environment identity, the hash-pinned lock, and the clean-environment reproducibility proof. |
| 1.1.0 | 2026-08-11 | Additive: section 7.1 records the remote GitHub Actions verification and its evidence class; section 8 gains the Node.js 20 deprecation technical debt and the incomplete run-identity limitation. Section 7 and all prior text are unmodified. |
