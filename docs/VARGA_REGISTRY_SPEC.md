<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | IMPLEMENTED AND CERTIFIED - decision entry ADR-0009, ADR-0010 and ADR-0011 PROPOSED pending owner ratification (Q1) |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-09 |
| Review cadence | TBD (see docs/OPEN_QUESTIONS.md Q1) |

# Generic Varga registry production specifications (D3, D12, D7, D30, D2)

> **Provenance and normative status.** This specification was authored as a plan,
> approved by the owner conversationally, and implemented before being lifted into
> `docs/`. `docs/PROJECT_CONSTITUTION.md` s7 states that anything not in the repository
> is input material and not truth, so the out-of-repository original carried no
> authority; this file is the resident specification. The governing decision is recorded
> in `docs/DECISION_LOG.md` at ADR-0009, ADR-0010 and ADR-0011, whose status is PROPOSED pending owner
> ratification (Q1). The text below is DESCRIPTIVE of the certified implementation and
> of the decisions actually taken; the ADR is the normative record. Sections retain the
> numbering of the original plan, including its implementation and publication records,
> which are preserved as dated evidence.

Date: 2026-08-09
Status: PROPOSED. Implementation starts only after explicit approval.
Base: origin/main b6a9d2c (TRANSIT_V1 certified and published).

## 1. Objective and why D3 first

Register the first production varga into the Generic Varga framework: D3 Drekkana (VARGA_D3_V1). This phase has double significance. It delivers a new certified divisional chart, and it is the FIRST PRODUCTION USE of the Generic Varga registry, which until now is certified infrastructure with an empty registry. The framework-first-use gates below are as important as the D3 mathematics themselves.

D3 is the right first entry: its classical rule is short, uncontested in the Parashara tradition, expressible exactly as the framework's existing CyclicVargaRule contract (no new rule type needed), and pyjhora provides an external oracle for it. Per the constitution, one varga at a time, each with its own source, rule table, independent reference, tests, and certification artifact.

## 2. Classical rule (source identification)

Brihat Parashara Hora Shastra, drekkana adhyaya: each sign divides into three equal parts of 10 degrees. The first drekkana belongs to the sign itself, the second to the 5th sign from it, the third to the 9th sign from it. As a CyclicVargaRule: 3 divisions per sign, start sign table = the sign itself for every sign, direction forward, with the division-to-sign step being 4 signs per division (sign, sign+4, sign+8). I will verify during implementation which exact parameterization the certified framework contract expects (start-sign table plus per-division stepping) and express the rule as frozen 12-entry literals, mirror-verified cell by cell against a second independent transcription, the same discipline Phase B used for the D9/D10 mirror tables.

## 3. Decisions that need your explicit sign-off

Decision VD-A, rule variant: the Parashara drekkana above (sign, 5th, 9th). Other traditions exist (Jagannatha and Somnath drekkanas, and Parivritti cyclic); V1 certifies the Parashara variant only, registered under the parashara school key. Other variants are explicit non-claims and would be separate registry entries with their own ADRs if ever wanted.

Decision VD-B, boundary policy: D3 inherits the project-wide unified convention already locked into the framework classifier (1e-10 promote-up, [start, end) ownership, top clamp). No new policy; the certification includes a full ULP boundary battery at every 10 degree boundary proving it.

Decision VD-C, registration semantics (framework first use): registering D3 must be provably non-invasive. The registry currently refuses D1/D9/D10 and the dispatcher serves the certified production modules for them; after registering D3, those behaviors must be bit-identical (guard tests plus my independent cross-commit hash sweep of D9/D10 outputs, the same 53,019-point SHA-256 method used in the repository audit). D3 becomes reachable through the dispatcher under the parashara school; every other unimplemented varga keeps raising UnsupportedVargaError.

## 4. Certification gates

Gate 1, rule-table integrity: frozen literals validated at construction; mirror verification against a second independent transcription and an in-test re-derivation from the classical rule (cell by cell, all 12 signs x 3 divisions).

Gate 2, mathematical verification: dense sweep (51,429 points) against an independently coded classical rule; full ULP-adversarial battery at every 10 degree boundary plus tiny negatives and 360 multiples; range invariants.

Gate 3, external oracle: pyjhora D3 (Traditional Parasara method) over dense midpoint grids, zero categorical tolerance; oracle astronomy is not involved because varga classification is pure longitude mathematics, so no D-007 tolerance derivation is needed here.

Gate 4, framework non-invasiveness (Decision VD-C): D1/D9/D10 dispatch bit-identical before and after registration (my independent SHA-256 sweep at both commits plus in-repo guard tests); UnsupportedVargaError preserved for everything else; registry contents exactly ("D3", parashara).

Gate 5, independent validator: root-level validate_d3_holdout.py, in-file lookup-table reference built by a different construction, zero tolerance.

Gate 6, certification artifact plus full-battery regression proof: certification/VARGA_D3_V1_certification.json regenerated from scratch, collected artifact-pinning test, additive README update; the entire existing battery (303 tests, five validators, four certifiers) must pass untouched.

## 5. Implementation order

Step 1: rule literals plus registration, Gates 1 and 4 (registration guards first, before any correctness claims). Step 2: mathematical verification, Gates 2 and 3. Step 3: independent validator, runner, artifact, docs, Gates 5 and 6. Publication by bundle relay, then fresh-clone verification. Full battery after every commit.

## 6. Risks

The framework classifier is certified infrastructure but has never fed a production chart; any latent contract mismatch surfaces here, which is exactly why Gate 4 runs first and why D3, the simplest possible entry, goes before anything else. The chart-assembly path for registry vargas (VargaChart models) gets its first production exercise; its outputs will be validated against the same snapshot facts the certified D9/D10 charts use.

## 7. What I need from you

Approve or amend: VD-A (Parashara drekkana variant only), VD-B (inherited unified boundary convention), VD-C (provably non-invasive registration with bit-identical D1/D9/D10 guards). One word, approved, covers all.

## Implementation record (2026-08-09) - BUILT AND VERIFIED, PENDING PUBLICATION

Built on branch varga-d3-v1 (two commits on top of published main b6a9d2c; tip 594201d395dcf866dda202255aac136a3c94104f). Modified files beyond new ones: README.md (additive), engine/astrology/__init__.py (registers production vargas on import; framework contracts untouched), and four Phase A/B tests that asserted the empty-registry state, replaced with documented inline rationale to assert the newly sanctioned certified set. No certified calculation file modified.

Contract finding: the framework's CyclicVargaRule steps one sign per division and cannot express the Parashara drekkana's four-sign jumps; D3 is therefore a SegmentVargaRule with all 36 cells as explicit literals, exactly within the certified contract.

Boundary finding, verified rather than assumed: the locked convention promotes intra-sign division boundaries within 1e-10, but the source-sign decomposition carries no tolerance, so sign-boundary dust stays in the previous sign's last division, exactly matching certified D9/D10; the D1 zodiac_sign primitive promotes such dust. This divergence inside 1e-10 dust is pre-existing locked behavior, now recorded in tests and the artifact.

Gates: 36-cell table verified against a second transcription and trine re-derivation; 51,429-point dense sweep zero mismatches; full ULP boundary battery; PyJHora pure-math oracle 3,600/3,600; registration proven non-invasive (registry exactly (3, parashara), certified dispatch types intact, refusals intact, D9/D10 bit-identical across registration by 53,019-point SHA-256 sweep at both commits); independent by-name validator 51,573 cases zero failures. Full battery: 315 tests, six independent validators, legacy gate 5/5, five certification runners regenerate PASS.

## Publication record (2026-08-09)

Published via owner bundle relay: origin/varga-d3-v1 pushed, main fast-forwarded b6a9d2c -> 594201d395dcf866dda202255aac136a3c94104f. Fresh-clone post-publication verification (EXECUTED): 315 tests, six independent validators PASS, legacy gate 5/5, five certification runners regenerate PASS, tree clean. VARGA_D3_V1 is CERTIFIED and PUBLISHED; the Generic Varga registry is in certified production use.

---

Date: 2026-08-09
Status: PROPOSED. Implementation starts only after explicit approval.
Base: origin/main 594201d (VARGA_D3_V1 certified and published).

## 1. Objective and why D12 next

Register the second production varga: D12 Dwadasamsa (VARGA_D12_V1). Beyond its own value (the parents/ancestry varga in Parashari practice), D12 completes the framework's production coverage: D3 exercised the SegmentVargaRule contract; D12 is a textbook CyclicVargaRule (twelve 2.5 degree divisions starting from the sign itself, advancing ONE sign per division), so this phase puts the framework's second and last rule type into certified production use. After D12, every future varga follows one of two production-proven paths.

## 2. Classical rule (source identification)

Brihat Parashara Hora Shastra, dwadasamsa description: each sign divides into twelve parts of 2.5 degrees; the first dwadasamsa belongs to the sign itself and each subsequent part to the next sign in order. As a CyclicVargaRule: divisions = 12, start_sign[s] = s for all twelve signs, direction forward everywhere. Frozen 12-entry literals, verified cell by cell against a second independent transcription and an in-test re-derivation (target = source + division index, mod 12).

## 3. Decisions that need your explicit sign-off

Decision V12-A, rule variant: the Parashara dwadasamsa above, registered under the parashara school key. Variant traditions are explicit non-claims.

Decision V12-B, boundary policy: inherited locked convention, verified by a full ULP battery at every 2.5 degree boundary (144 boundaries), including the documented sign-boundary nuance recorded during the D3 phase.

Decision V12-C, non-invasiveness: same discipline as D3. After registration the registry must contain exactly ((3, parashara), (12, parashara)); D1/D9/D10 dispatch bit-identical across registration (SHA-256 sweep at both commits); all other vargas keep refusing. The registry-state tests updated during the D3 phase are extended to the new certified set, documented inline.

## 4. Certification gates

Same six-gate template as ADR-VARGA-D3-001, now production-proven: table integrity (second transcription + re-derivation), 51,429-point dense sweep against an independently coded rule, full ULP boundary battery, PyJHora pure-math oracle (its Parasara dwadasamsa function) with zero categorical tolerance, framework non-invasiveness with cross-commit D9/D10 hashes, independent by-name validator (validate_d12_holdout.py), regenerated certification artifact (certification/VARGA_D12_V1_certification.json) with collected pinning test and additive README update. Full existing battery (315 tests, six validators, five certifiers) must pass untouched.

## 5. Implementation order and risks

Step 1 rule plus registration with non-invasiveness gates first; Step 2 mathematical verification and oracle; Step 3 validator, runner, artifact, docs. Publication by bundle relay, then fresh-clone verification. Risk profile is lower than D3's: the only genuinely new surface is the CyclicVargaRule production path, which Phase B already proved bit-identical to certified D9/D10 behavior through the mirror tables; its first registry-served use gets the same guard treatment anyway.

## 6. What I need from you

Approve or amend: V12-A (Parashara dwadasamsa only), V12-B (inherited convention with full ULP battery), V12-C (non-invasive registration extending the certified set). One word, approved, covers all.

## Implementation record (2026-08-09) - BUILT AND VERIFIED, PENDING PUBLICATION

Built on branch varga-d12-v1 (two commits on top of published main 594201d; tip fc74d2cb30f6577cf087f5000723138352950885). First production use of the CyclicVargaRule path; both certified rule contracts now carry production traffic. Introduced engine.astrology.CERTIFIED_PRODUCTION_VARGAS as the single source of truth for the sanctioned registry state, with all registry-state assertions and the D3 certifier reconciled to it (documented inline) and the D3 artifact regenerated by its own runner (gate results unchanged, D9/D10 hashes identical).

Gates: 24-cell table verified against a second transcription plus a full 144-cell target re-derivation; 51,429-point dense sweep zero mismatches; ULP battery at all 144 boundaries including the documented sign-boundary nuance; PyJHora Traditional Parasara oracle 3,600/3,600; non-invasiveness proven (registry exactly the certified set, certified dispatch intact, refusals intact, D9/D10 bit-identical by SHA-256 sweep); independent by-name validator 52,005 cases zero failures. Full battery: 327 tests, seven independent validators, legacy gate 5/5, six certification runners regenerate PASS.

## Publication record (2026-08-09)

Published via owner bundle relay: origin/varga-d12-v1 pushed, main fast-forwarded 594201d -> fc74d2cb30f6577cf087f5000723138352950885. Fresh-clone post-publication verification (EXECUTED): 327 tests, seven independent validators PASS, legacy gate 5/5, six certification runners regenerate PASS, tree clean. VARGA_D12_V1 is CERTIFIED and PUBLISHED; both framework rule contracts are in certified production use.

---

Date: 2026-08-09
Status: PROPOSED. Implementation starts only after explicit approval.
Base: origin/main fc74d2c (VARGA_D12_V1 certified and published; both rule contracts in production use).

## 1. Objective and shape of the batch

Three more classical vargas through the production-proven template. Engineering stays one-varga-at-a-time per the constitution: each chart gets its own ADR identity, rule module, gates, independent validator, certifier, and certification artifact, implemented and committed sequentially on one branch. Publication happens once at the end (one bundle, one push round for you). Each varga's battery must be green before the next begins.

## 2. Classical rules (source identification, all BPHS, Parashara variants only)

D7 Saptamsa: seven divisions of 30/7 degrees. Odd signs count from the sign itself; even signs count from the seventh sign from it; forward in both cases. This is a CyclicVargaRule with start_sign[s] = s for odd signs and (s+6) mod 12 for even signs.

D30 Trimsamsa: unequal segments ruled by the five tara grahas, no luminaries. Odd signs: 5 degrees Mars (target Aries), 5 Saturn (Aquarius), 8 Jupiter (Sagittarius), 7 Mercury (Gemini), 5 Venus (Libra). Even signs, reversed order: 5 Venus (Taurus), 7 Mercury (Virgo), 8 Jupiter (Pisces), 5 Saturn (Capricorn), 5 Mars (Scorpio). This is a SegmentVargaRule; widths sum to exactly 30 per sign.

D2 Hora: two 15 degree halves. Odd signs: first half the Sun's hora (mapped to Leo), second half the Moon's (Cancer); even signs the reverse. This is a SegmentVargaRule with a deliberately two-sign output space (only Leo and Cancer ever appear), which the framework's contract supports and the tests will pin explicitly.

Every table is written as frozen literals and verified cell by cell against a second independent by-name transcription plus an in-test re-derivation from the classical statement, the same discipline as D3 and D12.

## 3. Decisions that need your explicit sign-off

Decision VB-A, variants: Parashara only for all three, registered under the parashara school key. Named alternatives (parivritti saptamsa variants, Jagannatha horas, and the rest) are explicit non-claims.

Decision VB-B, conventions: the locked boundary convention inherited unchanged for all three, each with a full ULP battery at its own boundary set (D7's irrational-width 30/7 boundaries get particular ULP attention since they are not exactly representable in binary; the framework's certified uniform-division arithmetic already handles this shape for D9's 10/3 widths).

Decision VB-C, non-invasiveness and publication: after each registration the registry must equal the grown CERTIFIED_PRODUCTION_VARGAS constant exactly, D1/D9/D10 dispatch must stay bit-identical (SHA-256 sweep at the batch's base and tip), refusal behavior must hold for everything unregistered, and the whole batch publishes as one bundle.

## 4. Gates per varga (the proven six-gate template)

Table integrity; 51,429-point dense sweep against an independently coded rule; full ULP boundary battery; PyJHora pure-math oracle (its Parasara-method saptamsa, trimsamsa, and hora functions) with zero categorical tolerance; framework non-invasiveness; independent by-name root validator; regenerated certification artifact with collected pinning test; additive README entry. The complete existing battery (327 tests, seven validators, six certifiers) must pass untouched after every commit.

## 5. Risks

D30's unequal-segment tables are where transcription errors classically hide; that is exactly what the dual-transcription and oracle gates exist for, and the trimsamsa target signs are also constrained by an in-test rulership re-derivation (each segment's target is a sign ruled by its classical planet, odd targets male signs, even targets female signs). D2's two-sign output space is unusual downstream; the chart model carries it fine, and tests pin that no sign outside Leo/Cancer can ever appear. D7's start-sign parity rule is the first non-identity start table through the cyclic path; the 24-cell table gets the same cell-by-cell treatment.

## 6. What I need from you

Approve or amend: VB-A (Parashara variants only), VB-B (inherited conventions with per-varga ULP batteries), VB-C (non-invasive sequential registration, single publication bundle). One word, approved, covers all.

## Implementation record (2026-08-09) - BUILT AND VERIFIED, PENDING PUBLICATION

Built on branch varga-batch-v1 (one commit on top of published main fc74d2c; tip 3633db2f4efc21582bcfd25c4ac069600113cfa8). All three transcriptions confirmed against the PyJHora Parasara oracles behaviorally before any table was written.

Findings: D7's 30/7 widths are not binary-representable and six dense-grid points land one ULP below a boundary, where the locked promote-up convention correctly promotes; the independent references carry the documented tolerance explicitly. D30 verified additionally by a rulership-and-gender re-derivation. D2's two-sign output space pinned by test.

Per varga: dual-transcribed literals, 51,429-point dense sweep (0 mismatches), ULP boundary battery, PyJHora oracle 3,600/3,600, independent by-name validator (0 failures), regenerated certification artifact with collected pinning tests. Non-invasiveness: registry exactly the five-entry certified set, certified dispatch types intact, D9/D10 bit-identical (hashes ca444f10..., 78cd000f...), remaining vargas refuse. Full battery: 345 tests, ten independent validators, legacy gate 5/5, nine certification runners regenerate PASS.

## Publication record (2026-08-09)

Published via owner bundle relay: origin/varga-batch-v1 pushed, main fast-forwarded fc74d2c -> 3633db2f4efc21582bcfd25c4ac069600113cfa8. Fresh-clone post-publication verification (EXECUTED): 345 tests, ten independent validators PASS, legacy gate 5/5, nine certification runners regenerate PASS, tree clean. VARGA_D7_V1, VARGA_D30_V1, and VARGA_D2_V1 are CERTIFIED and PUBLISHED. The registry serves D2, D3, D7, D12, D30 under parashara alongside the hard-wired certified D1/D9/D10.
## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-09 | Lifted into docs/ from the out-of-repository plan document(s): VARGA_D3_PLAN.md, VARGA_D12_PLAN.md, VARGA_BATCH_D7_D30_D2_PLAN.md. Content preserved; header, provenance note and change history added per docs/DOCUMENTATION_STANDARD.md s2. |
