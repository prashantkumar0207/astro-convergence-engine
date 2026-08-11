# PHASE G COMMIT 1 (G6) FINAL COMPLETION RECORD

Date: 2026-08-11
Subject commit: `a460ba2b7e4eac55f8ac2f51b9e9eb9a35607fda` on branch `phase-g-governance`
Determination: **G6 = PASS** (CEO/technical auditor verdict, 2026-08-11)

Dated evidence. Filed under `reports/` per ADR-0003 item 3. This document records a
completed decision and is not revised in place; later evidence is added by superseding
note. Machine-readable counterpart: `certification/G6_REMOTE_CI_VALIDATION.json`.

## Evidence classes used

**EXECUTED_LOCAL**: run by the builder in its container and directly observed.
**CEO_REPORTED**: observed by the CEO/technical auditor on GitHub Actions and reported to
the builder. The builder has no network access to the Actions API and did NOT
independently observe these. Recorded at this class deliberately rather than presented as
builder-verified.

---

## 1. Local clean-environment verification (EXECUTED_LOCAL, 2026-08-10)

Virtual environments created with `python3 -m venv` and no system site-packages, isolation
asserted before use with `jhora` and `numpy` both invisible.

Oracle tier: `pip install --require-hashes -r requirements-oracle.lock`, the lock alone and
nothing else. 35 packages installed, all 35 hashes satisfied. All eight oracle
certification runners PASS. Regenerated artifacts differ from the committed artifacts in
the `date` field only, every gate value byte-identical.

Hermetic tier, installed from `requirements.lock` alone: default gate 395 passed; legacy
kernel gate 5 of 5; independent holdout validators 11 of 11 PASS; non-oracle certifiers 3
of 3 PASS. The same set re-run under `scripts/ci_no_network.py` gives identical results.
Negative control: a real connection attempt through the guard fails with `NoNetworkError`,
exit 1. `scripts/check_oracle_environment.py` returns 0 in the reproduced environment and 1
in a non-matching one.

## 2. Dependency lock information (EXECUTED_LOCAL)

`requirements-oracle.lock`, SHA-256
`dcd5e7c20f0767f15f50cbc3cc427bdd0190cf84c786a297a822f123d93b354b`. 35 packages pinned, 35
carrying a SHA-256, 100 percent hash coverage. Install command
`python -m pip install --require-hashes -r requirements-oracle.lock`.

Oracle package `PyJHora==4.8.7`, which declares an EMPTY `Requires-Dist`. Its six real
runtime dependencies are therefore invisible to pip and were discovered by iterative
import-failure resolution in an isolated venv: `numpy`, `geocoder`, `pytz`,
`timezonefinder`, `geopy`, `python-dateutil`. An earlier discovery attempt against the
ambient machine had surfaced only three of the six, because the other three happened to be
installed already; the clean-environment requirement doubled the closure and prevented a
lock that would have failed on every fresh runner.

Environment identity: `certification/ORACLE_ENVIRONMENT.json`.

## 3. GitHub Actions run identity (CEO_REPORTED, INCOMPLETE)

| Field | Value |
|---|---|
| Workflow | `engine-ci` |
| Branch | `phase-g-governance` |
| Commit | `a460ba2b7e4eac55f8ac2f51b9e9eb9a35607fda` |
| Overall result | SUCCESS |
| Run URL | **NOT SUPPLIED** |
| Run id | **NOT SUPPLIED** |
| Runner image and OS version | **NOT SUPPLIED** |
| pip version | **NOT SUPPLIED** |

The four missing fields are recorded as absent rather than guessed. Until they are added by
additive amendment, the repository's record of this run carries no resolvable pointer to
it. Stated plainly because this project's standard is that evidence must be traceable: a
PASS without a run identifier is weaker than the standard requires, even when the PASS
itself is not in doubt.

## 4. Hermetic gate, Python 3.11 (CEO_REPORTED)

PASS. This job installs pinned dependencies, records the environment, verifies ephemeris
checksums against `CHECKSUMS.sha256`, runs the default gate, all eleven independent holdout
validators, the legacy kernel gate and the three non-oracle certification runners, then
re-runs a representative subset with the network blocked, then runs the negative control
proving the guard blocks, then asserts no source file was modified by a certification run.
Per-step outputs were not transferred to the builder.

## 5. Hermetic gate, Python 3.12 (CEO_REPORTED)

PASS. Same step sequence as section 4 on the second matrix interpreter.

## 6. PyJHora oracle gate (CEO_REPORTED)

PASS. This is the result G6 existed to obtain. `requirements-oracle.lock` installed under
`--require-hashes` on GitHub-hosted hardware, the environment identity assertion passed
there, ephemeris checksums verified there, and all eight oracle certification runners
passed there.

The predicted risk was that a GitHub runner might resolve different wheels than the
authoring container, since the hashes are CPython 3.11 linux x86_64 artifacts. It did not
materialize. **No hash was relaxed, no dependency version was changed, and the lock was not
regenerated** at any point.

## 7. Artifact and evidence identity (CEO_REPORTED)

Artifact `oracle-certification-evidence` produced, uploaded with `if: always()` so evidence
is captured even on failure. Declared contents: `certification/*.json`,
`reports/certification/*.report.md`, `reports/certification/*.console.txt`.

Artifact contents were not transferred to the builder, so no digest comparison against the
locally regenerated artifacts was performed. That comparison would be the strongest
available confirmation that the remote run reproduced the same numerical gate values, and
it remains available if the artifact is downloaded.

## 8. Zero calculation impact (EXECUTED_LOCAL)

Two independent lines, neither of which is "the tests passed".

Diff evidence: `git diff` over `engine/`, `legacy/`, `validate_*.py`, `scripts/certify_*`
and `certification/*_certification.json` produces **0 lines**. The protected-asset diff,
covering `legacy/`, `reports/`, `LOCK_MANIFEST.json`, `v1_1_engineering_decision.json`,
`CHECKSUMS.sha256`, `swetest`, the three `.se1` files, `brihat_fixtures.py`,
`regression_report.json` and the root `DECISION_LOG.md`, is **EMPTY**.

Fingerprint evidence: a separate `git worktree` of the pristine baseline `1f861f6` was
created and SHA-256 fingerprints computed over a 51,429-point dense sweep plus 1e-9
neighbourhoods of every 0.25 degree boundary, using the same interpreter. All nine are
identical between baseline and the committed tree.

```
D9  sign : deb45a544f04fd44a8c2dffb1663dbd02a2d645f8136877cf293acb8cd23c592
D9  long : f2077f416d3ce9e562f504d48ff15fe1f8e12bc3d08500070aeac95e06d62c18
D10 sign : 3d842088953bf5513274ecbfe6c07056ac1205e85c2109a8b75d39a72d8a92b2
D10 long : 5621f6f83e4613fcc111e2797f9436a06935b26e0830bdd6199ce100daa36747
D2  sign : 99bbd30eeb8f7663b11aa7ffa6965b2759682dc061792cbe403c93da84e2a489
D3  sign : 6473ca0260fddfd6d1b953c8fb1bc375ade1ecccc4e2f4cdca1163b7de4c9b26
D7  sign : 7163e8853f06af3a5b4095d1be0d5b6a0ee72c1bbf98567f46913504b65416bf
D12 sign : dbf62dbba1e4a03cc9000ddce2f09ba2f63f0d0a218533824be7e686df838fa2
D30 sign : baf2af799a02fc3b202e5a0922800170dc8472e73fafad3baf3673b7777cf1a2
```

## 9. Deviations and warnings

**Deviations from the approved plan**, all recorded in the G6 commit message and ADR-0018:

O-1, the `governance` CI job was not added, because its primary check is the
retired-identifier search that cannot pass until Phase G commit 2 (G1) removes the 70
remaining occurrences. O-2, `requirements.lock` gained `jsonschema==4.25.0`, with the three
pre-existing pins unchanged. O-3, two helper scripts were added as the mechanisms for
plan-mandated behaviour. O-4, the oracle lock is self-contained rather than layered, because
`--require-hashes` rejects unhashed requirements. O-5, the decision register header was
corrected and a reserved-numbers note added.

**Technical debt recorded, not fixed:**

TD-CI-001, GitHub Actions Node.js 20 deprecation warnings for the pinned action versions.
Non-blocking, no effect on gate outcomes. By CEO direction the G6 commit MUST NOT be altered
merely to silence them; they belong to a dedicated CI-maintenance task with its own decision
entry.

TD-CI-002, the oracle tier is bound to CPython 3.11 linux x86_64 until a second lock and a
second recorded identity exist. Must never be resolved by relaxing hashes.

TD-CI-003, `scripts/certify_tier0.py` remains broken with `ModuleNotFoundError: astro_kernel`.
Superseded by the current gates and not referenced by the workflow. Disposition belongs to
Phase G commit 6 (G7).

**Open items G6 did not close:** the transit oracle Sun divergence of approximately 20.5
arcsec remains recorded NOT VERIFIED, since G6 recorded it more precisely without explaining
it; ADR-0018 remains PROPOSED and cannot be Accepted while `docs/OPEN_QUESTIONS.md` Q1
(named owners) is open; and the run identity fields of section 3 are outstanding.

## 10. Final determination

**G6 = PASS**, on CEO/technical auditor authority, 2026-08-11.

Basis: local clean-environment reproduction observed by the builder, plus independent
execution on GitHub-hosted runners observed by the CEO. G6's objective, proving the oracle
environment reproducible outside the sandbox that created it, is met.

**Scope limits, stated so this record cannot be misread later.** This is a reproducibility
and infrastructure determination. It certifies no calculation. It promotes no component's
certification level. It is not a C4 or C5 claim about any astrological method, and it says
nothing whatever about predictive validity.

State at the time of this record: `phase-g-governance` is NOT merged into `main`. `main`
remains at `1f861f67bb143bebb2c35c0b9da4c67624c340d6`. Phase G commit 2 (G1), the B-3
identifier reconciliation, has NOT started and awaits CEO approval.
