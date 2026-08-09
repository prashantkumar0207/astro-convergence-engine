# ASTRO CONVERGENCE ENGINE - INDEPENDENT REPOSITORY AUDIT REPORT

Date: 2026-08-08
Auditor: Claude (read-only reconstruction and adversarial audit, per PROJECT_CONSTITUTION.md FIRST TASK)
Repository: https://github.com/prashantkumar0207/astro-convergence-engine
Environment: clean cloud container, Python 3.11.15, pyswisseph 2.10.3.2, pytest 9.1.1, bundled swetest 2.10.03 binary and DE431 ephemeris files from the repository itself.

No code was modified, no branches were merged, and no history was rewritten during this audit. All executions were read-only reruns.

## 1. Method and evidence classes

Every claim below is tagged with one of the evidence classes required by the constitution: EXECUTED (I ran it in this clean environment), CODE-INSPECTED (I read the source), GIT-VERIFIED (confirmed by commit hashes and diffs), DOC-ONLY (asserted in documents, not independently reproduced), or NOT VERIFIED.

## 2. Git state reconstruction (GIT-VERIFIED, confidence: certain)

origin/main is at 16ccea227fa7c89491a3d34c238e63bea8f18dd2 (Harden D9 Navamsa boundary normalization), matching MASTER_HANDOFF.md and remote_main.txt exactly. The full history below 16ccea2 matches git_log_all.txt.

origin/incoming is at 8cfb6a527ed7e9e22e7fcb5cd48ece10cccc53f7. The merge base of main and incoming is exactly 16ccea2, so the candidate chain is a clean linear continuation with no divergence. All 12 candidate commits match the documented chain hash for hash:

5b77472, 8c143c7, 5ff57ca, 4e9830d, 36c9d6f, a0affad, dfe1ca2, f2cda10, ffe0e31, bfae088, 72f8171, 8cfb6a5.

Locked artifact integrity: git diff from 16ccea2 to 8cfb6a5 restricted to legacy/, reports/, LOCK_MANIFEST.json, v1_1_engineering_decision.json, DECISION_LOG.md, swetest, the .se1 ephemeris files, CHECKSUMS.sha256, both holdout validators, brihat_fixtures.py, test_official_swetest_reference.py, and regression_report.json is EMPTY. The locked legacy certification evidence is genuinely untouched across the entire candidate chain.

## 3. Independent execution results

### 3.1 Main baseline 16ccea2 (EXECUTED)

The default gate passes 99 tests, matching the documented pre-remediation count. Both D9 (108 midpoint + 312 boundary) and D10 (462 cases) holdout validators pass. Ephemeris file checksums match CHECKSUMS.sha256.

The two BLOCKER findings from the original audit are real and were reproduced live, not taken on faith. F-02: a swe.calc_ut call requesting FLG_SWIEPH returned a flag with the MOSEPH bit set and raised nothing, because the engine at main never sets an ephemeris path; the silent Moshier fallback is demonstrable in one line. F-01: house_positions.py calls swe.houses_ex with no sidereal flag (tropical ascendant and cusps) while sidereal_planets.py subtracts ayanamsa from tropical longitudes; the frame mixing is visible in source. F-07: the legacy Tier-0 gate fails 4 of 5 at main because it resolves ROOT to the repository's parent directory and imports a nonexistent astro_kernel package.

Conclusion: main as published is the defective pre-remediation baseline. Its D9/D10 modules are healthy, but its astronomy pipeline must not be used for production output.

### 3.2 Incoming tip 8cfb6a5 (EXECUTED)

| Claimed | My independent rerun | Verdict |
|---|---|---|
| 233 tests pass | 233 passed | CONFIRMED |
| D9 holdout validator passes | 108 + 312 PASSED | CONFIRMED |
| D10 holdout validator passes | 462 PASSED | CONFIRMED |
| Legacy gate repaired, passes | 5 passed (4 tier0 + 1 swetest ref) | CONFIRMED |
| Holdout matrix: max planet 0.000179, asc 0.000176, cusp 0.000180 arcsec, 264+264 comparisons, both profiles | Regenerated from scratch by scripts/certify_current_engine.py against the bundled swetest binary: identical figures to the last digit | CONFIRMED |
| Lahiri vs KP profiles separate by 5.811 arcmin | 5.811 arcmin, live | CONFIRMED |
| Ephemeris strict swieph, sidereal frame, provenance stamped | provenance shows ephemeris_mode swieph, frame sidereal, ayanamsa mode, house system | CONFIRMED |
| Varga registry empty; dispatcher raises UnsupportedVargaError | registry () live; D7 dispatch raises with a correct message | CONFIRMED |
| Mirror tables unreachable from production | varga_mirrors is not referenced by divisional_chart, navamsa_chart, or dashamsa_chart | CONFIRMED |
| 186 tests at lock commit bfae088 | 186 passed | CONFIRMED |

### 3.3 Adversarial equivalence checks I designed myself (EXECUTED)

These did not reuse the repository's own equivalence tests. I wrote an independent sweep of 53,019 points (51,429 dense grid plus exact boundaries and up to 3 ULPs on both sides of every D9 and D10 boundary) and hashed the complete ordered outputs with SHA-256 at three commits.

D9 and D10 at locked bfae088 versus incoming tip 8cfb6a5: hashes identical for both vargas. Phase A and Phase B provably changed nothing in certified behavior, confirming the additive-only claim.

D9 at main 16ccea2 versus incoming 8cfb6a5: hashes identical. The claim that D9 remains bit-identical to the certified baseline holds against my own sweep.

D10 at main 16ccea2 versus incoming 8cfb6a5: hashes differ, and this is the documented deliberate F-18/F-19 change, not a regression. Point-by-point comparison shows 324 mismatches out of 52,266 points, every single one at ULP-adjacent points immediately below a 3 degree boundary, where incoming promotes to the boundary per the unified 1e-10 promote-up convention. Zero mismatches anywhere in the dense sweep. The behavior change is bounded to sub-1e-10 degree neighborhoods and was recertified in-chain.

### 3.4 Documented figures reconciled

The apparent 181 versus 186 test-count contradiction across documents is resolved: 99 at main, 181 at the end of remediation (dfe1ca2, when TEST_RESULTS.md was written), 186 at the lock (ffe0e31 added the collected certification gate), 223 after Phase A, 233 after Phase B. Each step was confirmed by execution or by the verified commit messages. Not a contradiction.

## 4. Current architecture map (CODE-INSPECTED)

Pipeline at incoming: BirthData, then core/validation, then services/time_service (IANA, DST, fold, gap rejection), then core/julian_day (GREG_CAL explicit), then astronomy_snapshot under an explicit CalculationProfile (strict SWIEPH ephemeris via engine/astronomy/ephemeris.py, sidereal frame via FLG_SIDEREAL, Placidus cusp data, provenance stamped on every snapshot), then D1 (whole-sign, documented decision), then D9/D10 via the certified production modules through the dispatcher, which raises UnsupportedVargaError for everything else.

The Generic Varga framework (varga_rules, varga_classifier, varga_registry, varga_chart_builder, models/varga_chart, models/varga_planet) is pure infrastructure: frozen rule contracts with constructor validation, classification-first outputs, an empty registry that refuses D1/D9/D10 registration, and a school-aware dispatcher defaulting to parashara. varga_mirrors.py holds D9/D10 rule tables as verification artifacts only, unregistered and unreachable from production paths.

Strict school separation holds: nothing in engine/ implements KP, Jaimini, BNN, or numerology; legacy/kp.py remains the untouched migration reference; the two ayanamsa profiles are isolated by methodology per the recorded human sign-off.

## 5. Certified components (evidence-backed)

Tier-0 astronomical kernel of the current engine at bfae088 and unchanged through 8cfb6a5: EXECUTED, reproduced in this environment (528 comparisons, max error 0.000180 arcsec, both profiles, 11 holdout cases). Certified D9 Navamsa: EXECUTED plus my independent cross-commit hash equivalence to 16ccea2. Certified D10 Dashamsa: EXECUTED, recertified in-chain after the documented boundary unification; my sweep localizes the entire behavior change to ULP boundary points. Legacy astro_kernel Tier-0: GIT-VERIFIED as untouched; its own gate passes at incoming; its certification remains historical evidence for legacy/ only. Calculation profiles and ayanamsa isolation: EXECUTED (5.811 arcmin separation, provenance stamping). Boundary convention: CODE-INSPECTED as single-sourced in longitude_utils.py and EXECUTED via the ULP sweep.

## 6. Not certified, framework-only, or missing

Framework-only, no production use: Generic Varga framework and mirror tables. Not built at all: all vargas beyond D1/D9/D10, all dasha systems, transits, KP engine layer (legacy reference only), Jaimini, BNN/Nadi, numerology, evidence/convergence layers, real API surface, production app (the Flutter stub remains fake and release-blocking, F-22). Known open technical items: polar-circle Placidus behavior NOT VERIFIED (docs are honest about this), UTC treated as UT1 (documented, bounded 0.9 s), sidereal speed semantics (documented caveat), Rahu/Ketu dignity tradition variants recorded but no selecting profile, D1 signs 1-based versus varga signs 0-based (documented split, must be unified before any convergence layer), scripts/ legacy pipeline still targets old packaging (superseded by the engine gate).

## 7. Risks and findings from this audit

Finding R-1 (was the top risk, now mitigated): until today the entire remediation and certification chain existed only on one workstation. It is now pushed as origin/incoming. Residual risk: main on GitHub still serves the defective baseline to anyone who clones it.

Finding R-2: the Claude Project doc collection contains most files twice under identical names (uploaded once per snapshot), and only the newer copy is readable. With the Git history now published this ambiguity is harmless, but the duplicates should be cleaned to avoid a future reader trusting the wrong generation.

Finding R-3: the environment pin says python==3.12.3; this audit ran on 3.11.15 and everything passed, consistent with the CI matrix (3.11/3.12), but the certification environment statement should name both.

Finding R-4: certification/current_engine_certification.json is regenerated on every run by design. My rerun regenerated it with identical headline figures, which is the correct behavior, but note that a git status after running the certifier will show this file modified; do not commit an audit-run regeneration casually.

No evidence of hidden convention changes, duplicate boundary policies, silent defaults, fitting to references, or certification claims without artifacts was found. Commit messages were spot-checked against actual diffs and matched.

## 8. Verdict on the candidate chain

The incoming chain 5b77472 through 8cfb6a5 is internally coherent, additive, honest about its non-claims, and every major certification claim I tested reproduced exactly in a clean environment. The chain fixes two live BLOCKER defects that are demonstrably present on main. I found no reason to reject it and multiple independently verified reasons to adopt it.

Recommendation: fast-forward main to 8cfb6a5. This is a publication decision reserved for the project owner and requires your explicit approval; I have not merged anything.

## 9. Recommended roadmap and next safest development gate

After the merge decision, the safest order, consistent with ARCHITECTURE_STATUS.md and the constitution: first the merge/publication gate (owner approval, fast-forward, no code change); then KP migration from legacy/kp.py into an isolated engine/kp/ package under the KP_KRISHNAMURTI profile, preserving the Fraction-based hierarchy math, with the legacy module as the equivalence oracle (this is the next milestone with an existing certified reference to test against, which is what makes it safest); then Vimshottari dasha seeded by the boundary-hardened Moon nakshatra; then transits; then additional vargas one at a time through the Generic Varga registry, each with its own classical source, rule table, independent reference, and certification artifact; aspect systems per school after that. Before the convergence layer, resolve the 1-based/0-based sign convention split. Polar-circle house policy needs a specification decision before any test can assert behavior.

Next safest single milestone: the merge/publication gate, because it changes no calculation, removes the risk of the defective baseline being consumed, and unblocks everything else.

## 10. Decisions requested from the owner

Decision 1: approve or reject fast-forwarding main to 8cfb6a5. Decision 2: approve KP migration as the next development phase, or name a different priority. Decision 3: whether to clean the duplicate docs in the Claude Project.

## Addendum: publication record (2026-08-09)

Following owner approval: the incoming chain was pushed as origin/incoming, three verified cleanup commits were added on top (c50178f removal of decoupled HLKG product remnants, 5ae8ee7 removal of the Flutter fake-math stub resolving F-22, 45ea7bf truthful README), and main was fast-forwarded from 16ccea2 to 45ea7bf. Post-publication verification on a fresh clone of origin/main (EXECUTED): 233/233 default gate, D9 holdout 108+312 PASS, D10 holdout 462 PASS, legacy gate 5/5, ephemeris checksums OK, holdout certification matrix regenerated PASS at 0.000179 arcsec max planet error. The full battery was also rerun after each individual cleanup commit before publication. Protected assets diff against 8cfb6a5: empty. Finding R-1 is closed. The Claude Project's duplicate doc uploads were removed; GitHub is the single source of truth (finding R-2 closed).

New open item O-1: scripts/certify_current_engine.py line 90 chmods the locked swetest binary on every run, leaving a mode-only diff on a protected artifact (content hash unaffected). Decision needed before or during the next phase: commit the executable bit once, or make the certifier copy the binary to a temp path. Also note the certifier regenerates certification/current_engine_certification.json on every run by design; audit-run regenerations must not be committed (existing R-4 guidance, now stated in the README).

Next approved direction per the roadmap: KP migration from legacy/kp.py into an isolated engine KP package under the kp_krishnamurti profile, with legacy as the equivalence oracle. Implementation plan requires owner approval before coding.
