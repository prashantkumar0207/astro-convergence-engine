<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | EVIDENCE. Independent adversarial audit of ADR-0013 through ADR-0036 and of the CI workflow, conducted 2026-08-13. Findings are recorded; remediation of the authorised subset is recorded in ADR-0037. Unremediated findings are OPEN. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-13 |
| Review cadence | TBD |

# Phase G governance and certification audit, 2026-08-13

## 1. Method, and why it is worth stating

Two independent read-only audits were run by separate agents that did not see
each other's work, one over `.github/workflows/ci.yml` and the scripts it
invokes, one over every decision entry from ADR-0013 to ADR-0036. Both were
instructed to find over-claiming rather than to confirm. Every finding below was
then re-checked against the working tree before being recorded here.

This matters because the alternative, the builder auditing its own register, is
the circularity the project charter section 11 exists to prevent. Several
findings below are defects in entries this same builder wrote, and they were not
found by re-reading them.

**Baseline established independently:** default gate 420 passed, zero skipped;
11 certification artifacts, all `result: PASS`, all with a matching `.report.md`
and `.console.txt`; 11 holdout validators; ADR numbering 33 entries,
`1..14, 18..36`, unique and monotonic.

## 2. Verdict

**No BLOCKER.** No calculation, tolerance, holdout, certified artifact or gate
produces a wrong result. Every finding is governance, traceability, or evidence
scope. That is the honest headline and it should not be inflated in either
direction: the mechanics are sound, and the claims made about them were in
several places wider than the mechanics support.

**The over-claims cluster in one place and it is worth naming.** They are
concentrated in the *evidence citations* of the governance entries, ADR-0022
through ADR-0028, and in three CI step names. They are not in the certification
entries. Governance prose was written to a lower evidential standard than the
certification work it governs, which is the wrong way round.

## 3. Findings, ranked, with disposition

Disposition key: **FIXED** in this batch; **OPEN, OWNER** needs an owner
decision; **OPEN, RECORDED** verified and left, with the blocker stated.

### HIGH

**H-1. An unauthorised decision-identifier family is in use right now.**
`docs/decisions/DP-008-...md`, `DP-009-...md` and `docs/decisions/README.md` use
and reserve a `DP-NNN` family. `docs/NAMING_STANDARD.md` section 2's ID-Families
table has no `DP-` row, `docs/DECISION_LOG.md` contains no `DP-0` occurrence, and
no uniqueness check exists. `NAMING_STANDARD.md` requires all three **before
first use**. This is the identical defect class ADR-0004 retired, recreated on
2026-08-11, and it passes CI because the gate's family regex only matches
`ADR-`-prefixed tokens. ADR-0014 D5's claim that "the family regex is the
operative one, because the defect class is an unauthorised identifier family" is
therefore false as a statement about the repository's actual exposure.
**Disposition: OPEN, OWNER.** Registering a family is a change to a STANDARD,
and extending the gate to flag `DP-` would turn CI red immediately. Recorded as
**Q19**.

**H-2. The retired-identifier gate had an unvalidated escape hatch.**
`SUPERSESSION_FIELD_RE` scrubbed the whole line for the authorised supersession
key without checking the value, so any token passed in that position, including
an invented family and a retired identifier belonging to a different division.
**Disposition: FIXED.** The value must now be one of the ten strings ADR-0004
retired, and where a division can be read off the path it must be the identifier
ADR-0014 D1's replacement map assigns to that division. Five probes verified,
including one that must still pass. Committed controls in
`engine/tests/test_retired_identifier_gate_scope.py`.

**H-3. `.github/` is an undeclared top-level folder, and ADR-0028 certifies the
opposite.** `.github/` is tracked and holds the entire CI apparatus. It appears
in no ADR's declared top-level set. **Ratified** ADR-0001 fixes the set with the
word "exactly" and requires a superseding ADR for additions; ADR-0003 repeats the
requirement. ADR-0028's row for ADR-0003 asserts the tree "matches the entry's
consequences **exactly**". It does not: ADR-0003's consequences also omit
`schemas/`, which ADR-0003 D1 itself restored and which exists on disk. The one
entry whose job was the repository-wide consistency audit got the folder set
wrong. **Disposition: OPEN, OWNER.** A ratified decision cannot be amended by the
builder. Recorded as **Q20**, with a drafted superseding entry described there.

**H-4. A real CI loophole: a step whose name asserted an invariant it could not
enforce.** The oracle job ran `git --no-pager diff -- certification/ reports/`
under the step name "run date is the only expected change". `git diff` without
`--exit-code` always exits 0, so a changed comparison count, a changed maximum
error, a widened tolerance or a removed holdout case would have printed into the
log and the job would have gone green. **Disposition: FIXED.**
`scripts/check_artifact_drift.py` now enforces it, permitting difference only in
`date`, `run.executed_utc`, `run.source_revision` and `run.working_tree_dirty`.
Thirteen negative controls committed in
`engine/tests/test_artifact_drift_gate.py`.

### MEDIUM

**M-1. "hermetic (no oracle, no network)" claimed more than it delivered.** The
job has full egress, which it must in order to `pip install`. The guard patches
five socket entry points inside one Python process and is applied to six
invocations; nine of the eleven validators and the legacy gate are never re-run
under it. The workflow header said "each also re-run with the network blocked".
`docs/CI_AND_ORACLE_REPRODUCIBILITY_SPEC.md` was honest about this ("a
representative subset"); ADR-0018's evidence paragraph was not ("the same set").
**Disposition: FIXED, documentation.** The job is renamed and the header states
the scope, including that child processes are not sandboxed.

**M-2. The network negative control could pass without the guard working.** It
asserted only a nonzero exit, which is also satisfied by a missing probe file, a
renamed guard, or a runner with no egress at all, and it never established that
the probe would otherwise succeed. **Disposition: FIXED.** The control now runs
the probe **unguarded first** and requires success, then requires the guarded run
to fail **with `NoNetworkError` named in the output**. Both halves verified
locally.

**M-3. The source-immutability step destroyed its own evidence.** It ran
`git checkout -- certification/ reports/` before anything examined them, so
artifact drift in that tier was discarded rather than asserted. Its path list also
covered four path sets only. **Disposition: FIXED.** Drift is now checked before
the restore, and the path list covers `docs/`, root-level `*.py`,
`CHECKSUMS.sha256`, both lock files, `.github/`, the ephemeris files and the
`swetest` binary.

**M-4. The ADR numbering gate had no negative control.** Its PASS proved only
that it ran. **Disposition: FIXED (Q14).** The check moved to
`scripts/check_adr_numbering.py` so the gate and its control execute the same
code against different input, rather than the control duplicating the rule. A CI
control plants a duplicate and an out-of-order entry into a copy and requires
both to be rejected, and 15 committed tests cover the same ground on every
default gate.

**M-5. ADR-0023 asserts two standards "are narrowed" while changing neither.**
`engineering/ENGINEERING_CONSTITUTION.md` and `docs/KNOWLEDGE_STANDARDS.md`
contain zero references to ADR-0023 or to any ADR. The unqualified prohibition
still stands in both, and a reader of either cannot discover the narrowing.
Worse, `engineering/ENGINEERING_CONSTITUTION.md` is **not placed anywhere in
ADR-0022's authority hierarchy**, which names "PROJECT CONSTITUTION", so it is not
established that an ADR can narrow it at all. **Disposition: OPEN, OWNER**, and
this is the one the CEO directive's item H.4 anticipated: an unratified ADR must
not silently override a higher-level standard. Recorded as **Q21**.

**M-6. ADR-0023 D4's architecture rationale rests on two documents that never
mention the knowledge layer.** The note it wrote into
`docs/REPOSITORY_ARCHITECTURE.md` claims `ASTROLOGY_ARCHITECTURE.md` and
`PLATFORM_DOMAIN_ARCHITECTURE.md` "each separate" prediction and interpretation
from knowledge; both contain zero occurrences of the word. One of them is then
designated authoritative "for layering", of a layer it does not discuss. And a
genuinely conflicting fourth document, `docs/ARCHITECTURE.md` ("Knowledge is the
single source of truth... Python modules must never duplicate knowledge data"),
is counted in no conflict and covered by no narrowing. **Disposition: OPEN,
RECORDED.** Folded into Q21, since the remedy is the same decision.

**M-7. ADR-0025 and ADR-0030's `legacy/` dependency claim is wrong as worded.**
"Imported by five test modules only and by no production module" is repo-wide in
phrasing and `engine/`-scoped in evidence. The importer set is **seven**: the four
`engine/tests/` modules it names, plus root-level `test_tier0_certification.py`,
plus **`scripts/certify_kp_chain.py`, which is a certification runner and not a
test module at all**. The substantive claim, that no production module imports
`legacy/`, is true. **Disposition: OPEN, RECORDED.** Correcting a ratified-adjacent
committed entry is not available to the builder; the correction is stated in
ADR-0037 and the entries are left intact.

**M-8. `CURRENT_ENGINE_LOCK.json` and the certification artifact named different
certified commits.** `ratification.certified_tree` read `d951caf` while the
artifact it cites recorded `source_revision: ac78072`. No numerical consequence,
because the implementation trees are hash-identical, but the lock record went
stale one commit after the provenance protocol was adopted to prevent exactly
this. **Disposition: FIXED.** The field now points at the artifact's
`run.source_revision` as the single source of truth rather than duplicating a SHA
that must be maintained by hand.

### LOW

**L-1. ADR-0022's evidence claim about D-003 and D-004 is false.** "D-001, D-002,
D-003, D-007 cited live in `scripts/certify_*.py`": `D-003` and `D-004` appear
zero times under `scripts/`. D-003 is cited live, but in `engine/kp/intervals.py`,
`engine/kp/tables.py` and two KP tests. The substantive point, that D-001 to
D-007 are operative rather than historical, stands; the cited proof does not.

**L-2. ADR-0014's preserved-citation counts are wrong and unbounded.**
`reports/ALIGNMENT_REVIEW.md` has three occurrences on one line, not one: the
entry switched from counting occurrences to counting lines mid-paragraph.
`docs/DECISION_LOG.md` has grown from the claimed 10 to 36, and the allowlist
imposes no count, so an allowlisted file can accumulate retired identifiers
indefinitely.

**L-3. The status-header gate asserts "complete" but checks presence only.** It
never tests that a value is non-empty or meaningful. All nine required documents
carry `| Owner | TBD |`, which is exactly the state Q1 describes.

**L-4. `certify_tier0.py` is broken and excluded, and the count hides it.** It
raises `ModuleNotFoundError: astro_kernel`. Twelve certifiers exist; eleven run.
"All eleven certification runners" is self-consistent only if the reader already
knows one is excluded. Disclosed in the spec and in
`G6_REMOTE_CI_VALIDATION.json`, not in the count.

**L-5. `requirements.lock` is version-pinned but not hash-pinned**, and is
installed without `--require-hashes` by two of the three jobs. `pip` itself is
upgraded unpinned in all three, so even the oracle environment is
lock-plus-unpinned-pip. Neither ADR-0018 nor the spec says so. **Disposition:
documented in the workflow header; the pinning itself is OPEN, OWNER** since
hash-pinning the hermetic lock changes the dependency contract.

**L-6. The oracle identity check verifies less than the recorded identity.** It
omits the OS, the Python patch level, the implementation, the `swetest` binary
SHA-256, the dependency lock's own SHA-256 and the ephemeris manifest hash. Since
the lock's hash is unverified, the lock could be edited and the check still pass.

**L-7. The `swetest` reference binary is never checksum-verified.** Its SHA-256 is
recorded in `certification/ORACLE_ENVIRONMENT.json` and read by nothing. What is
checked is a version string, which any binary can print. ADR-0032's phrasing,
that this "proves the ORACLE is the pinned build", overstates it: the D-001
numerical authority is the one asset in the gate with recorded-but-unverified
integrity. `CHECKSUMS.sha256` itself is likewise unverified.

**L-8. Citation drift, four instances.** `ENGINEERING_CONSTITUTION.md:46-50`
excludes the operative sentence at `:52`. `repository.py:16` is `planets()`, the
dignities load is at `:28`; `dignity.py:5` is a docstring, the import is at `:17`.
`PLATFORM_DOMAIN_ARCHITECTURE.md s13` and `H0_ENTITY_MODEL_SPEC.md s10` are
change-history sections; the cited content is at s12 and s9.

**L-9. ADR-0032 counts three committed ephemeris negative controls; two exist.**
The third, the manifest-covers-`REQUIRED_FILES` assertion, is a positive
assertion. Both real controls are properly constructed with a positive check
first.

**L-10. ADR-0035 ratifies a D7 numerical caveat that is not in the D7 artifact.**
The "six sweep points, one ULP below a boundary" finding is in
`docs/VARGA_REGISTRY_SPEC.md`, the certification roadmap and a test comment, but
`certification/VARGA_D7_V1_certification.json` records only a generic
`boundary_policy` string.

**L-11. Resolved questions never reached the documents they block.**
`docs/MASTER_ARCHITECTURE.md` still records the knowledge dependency as
`TBD (Q6)` though ADR-0024 and ADR-0030 resolved Q6. C-01, C-02 and C-05 remain
verified stale. Related: ADR-0003's obligation to **re-run** the naming
conformance sweep cannot be discharged, because no sweep script exists in
`tools/` or `scripts/`; `NAMING_STANDARD.md` NS-2 still proposes creating one.

**L-12. A residual circularity in the evidence-agreement gate.**
`test_certification_evidence_agreement.py` verifies each report against the same
`certification_support._render` that produced it. It proves
`report == _render(artifact)`; it cannot detect a defect inside `_render`, where
both files would agree on a wrong number. Given the charter's anti-circularity
rule this deserves recording as the analogue of Q14 for that gate. Recorded as
**Q22**.

### NOT DETERMINABLE from the repository

Whether any CI run at HEAD passes on GitHub-hosted runners. **This is the most
consequential documentation defect found.** The only remote-CI evidence in the
repository, ADR-0018's addendum and `G6_REMOTE_CI_VALIDATION.json`, attests
commit `a460ba2`, which is the **two-job** version of the workflow. `ci.yml` was
rewritten at `c18150b` to add the `governance` job, and further commits have
landed since. The addendum's evidence class is `CEO_REPORTED` with `run_url`,
`run_id`, `runner_image` and `pip_version` all null, which the repository
commendably flags as sub-standard, but the compounding staleness is flagged
nowhere. **No remote CI run record exists for the three-job workflow at all.**

## 4. What the audits confirmed, checked and found sound

Recorded because an audit that lists only defects misrepresents the artifact.

Ephemeris integrity is genuinely well-built: enforced twice in CI and again
inside every certifier through `preflight()`, with coverage against
`REQUIRED_FILES` asserted and corruption and deletion controls that check the
copies pass first. Hash-pinning of the oracle lock is complete, 35 packages, 35
hashes, under `--require-hashes`. Failure propagation is sound: no
`continue-on-error` anywhere, every `run` block is `bash -e`, every bounded
`set +e` region checks its return code, and all three heredocs render at column
zero and propagate their exit codes. The identifier gate's CI negative control is
mechanically correct and fails safe. Legacy equivalence runs, including under the
network guard. The evidence-agreement gate's floor of eleven pairs and its
explicit naming of the Tier-0 pair genuinely prevent a discovery bug from turning
it into a no-op. ADR-0034's tree-hash table was recomputed at four commits and is
correct. Every number in ADR-0034 D4 matches the artifact at full precision.
ADR-0026's Phase 1 count of nineteen unchecked items is exact. ADR-0019's absence
sweep re-ran clean across all fifteen terms.

And the register is unusually candid. ADR-0028's own C-01 to C-07, ADR-0029's
Q14, ADR-0031's Q15, ADR-0033's authentication gap, ADR-0035 D4's asymmetry and
ADR-0036 D3's refusal to infer a lock are all self-recorded defects that a less
careful register would have buried.

## 5. Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-13 | Created from two independent adversarial audits. Findings recorded; authorised remediation carried out under ADR-0037. |
