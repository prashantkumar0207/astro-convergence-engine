<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | IMPLEMENTED AND CERTIFIED - decision entry ADR-0012 PROPOSED pending owner ratification (Q1) |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-09 |
| Review cadence | TBD (see docs/OPEN_QUESTIONS.md Q1) |

# Sign-convention declaration and enforcement specification

> **Provenance and normative status.** This specification was authored as a plan,
> approved by the owner conversationally, and implemented before being lifted into
> `docs/`. `docs/PROJECT_CONSTITUTION.md` s7 states that anything not in the repository
> is input material and not truth, so the out-of-repository original carried no
> authority; this file is the resident specification. The governing decision is recorded
> in `docs/DECISION_LOG.md` at ADR-0012, whose status is PROPOSED pending owner
> ratification (Q1). The text below is DESCRIPTIVE of the certified implementation and
> of the decisions actually taken; the ADR is the normative record. Sections retain the
> numbering of the original plan, including its implementation and publication records,
> which are preserved as dated evidence.

Date: 2026-08-09
Status: PROPOSED. Implementation starts only after explicit approval.
Base: origin/main 7d170f8 (PARASHARI_DRISHTI_V1 certified and published).

## 1. Why this phase, now

The repository has carried one documented architectural debt since the original remediation: the sign-index convention is split. This audit measured it precisely rather than trusting the note. Every varga sign output is 0-based, including the certified D9 and D10 production modules and all five registry vargas. Every rashi-level sign output is 1-based, including `zodiac_sign`, the KP chain's `sign_number`, and drishti's sign and house numbers. Confirmed by execution: for 15 degrees of Aries, `zodiac_sign` returns 1 and `kp_chain().sign_number` returns 1, while `navamsa_sign` returns 4 and the D3 classifier returns 4, all three of the latter meaning Leo.

Nothing is wrong today because each layer is internally consistent and separately certified. The hazard is joining facts across layers, which is exactly what the evidence and convergence layers exist to do. A single off-by-one there would be a silent, plausible-looking error of one zodiac sign, the hardest class of defect to detect downstream. The debt also grows with every phase: it now spans eight certified varga surfaces against three rashi-level surfaces, and the documentation already names its resolution as the prerequisite for convergence.

## 2. The binding constraint

The certified varga outputs are LOCKED. `navamsa_sign` and `dashamsa_sign` return 0-based values that are certified by artifact and proven bit-identical across every development phase by SHA-256 sweep. The registry vargas' `d_sign` is likewise certified. Therefore unification must not change a single certified return value. This rules out the obvious approach of renumbering, and it is the reason this phase is worth planning carefully rather than doing casually.

## 3. Proposed approach: make the convention explicit and machine-checked, not renumbered

Decision SC-A, the core design. Introduce one small shared module defining the sign concept explicitly, with named constructors and named accessors, so no value crosses a layer boundary without its convention attached. Concretely: a frozen `Sign` value type constructed only by `Sign.from_zero_based(i)` or `Sign.from_one_based(n)`, exposing `zero_based`, `one_based`, and `name`, with equality and ordering. It carries no arithmetic that could hide a shift; sign stepping stays in the layers that own their rules.

Decision SC-B, additive adoption only. Existing fields keep their exact current values and names, so every certified output is untouched and every existing caller keeps working. Alongside them, each layer gains an explicitly named accessor: varga positions gain `sign_one_based` (and, where clearer, a `sign_object`), rashi-level models gain `sign_zero_based`. Field-level docstrings state the convention for every sign-typed field. Nothing is deprecated in this phase; deprecation, if ever wanted, is a separate decision after the convergence layer exists and can be migrated deliberately.

Decision SC-C, enforcement rather than documentation alone. A collected test walks the public surface of every layer, asserts the declared convention of every sign-typed field against a registry of declarations kept in one place, and fails if a new field appears without a declaration. This converts a documentation convention into a gate, so the debt cannot silently grow in the next phase, which is the actual objective. A cross-layer consistency test additionally asserts that, for a dense set of longitudes, the 1-based and 0-based views of the same fact agree after exactly one conversion through `Sign`, in both directions, across D1, KP, drishti, certified D9 and D10, and all five registry vargas.

## 4. Certification gates

Gate 1, non-invasiveness, run first and weighted highest: certified D9 and D10 outputs bit-identical to published main across the 53,019-point dense-plus-ULP sweep by SHA-256, the same method used in the original repository audit; all five registry vargas byte-identical over their dense sweeps; the complete existing battery of 356 tests, eleven validators, and ten certification runners green and unchanged.

Gate 2, `Sign` type correctness: exhaustive over all twelve signs in both constructions, round-trip identity, rejection of out-of-range and wrong-type inputs, immutability, and no arithmetic surface that could silently shift a value.

Gate 3, declaration coverage: every sign-typed field on every public model across the astrology, KP, dasha, transit, and parashari layers appears in the declaration registry with the convention that its live value actually exhibits, verified by execution against real charts rather than by inspection. A new undeclared sign-typed field must fail the gate.

Gate 4, cross-layer agreement: dense-longitude agreement between conventions in both directions across all ten sign-producing surfaces, including exact sign boundaries and ULP neighbors, where the documented promote-up nuance already recorded in the D3 and D12 phases applies.

Gate 5, artifact: `certification/SIGN_CONVENTION_V1_certification.json` regenerated from scratch by its own runner, recording the declaration registry as certified data so a future reader sees the conventions as evidence rather than prose, plus a collected pinning test and an additive README entry.

## 5. Risks

The real risk is scope creep into renumbering, which would reopen certified behavior; Decision SC-B forecloses it and Gate 1 detects any accidental drift. A secondary risk is over-engineering the `Sign` type into a general astrology-arithmetic object; the plan deliberately keeps it inert. There is no classical or astrological content in this phase, so there is no tradition variant to adjudicate and no external oracle is applicable; verification is entirely internal, exhaustive, and mechanical.

## 6. What I need from you

Approve or amend: SC-A (an explicit inert `Sign` value type as the shared convention carrier), SC-B (purely additive adoption, no certified value or existing field changed), SC-C (a declaration registry enforced by a collected gate so the debt cannot grow). One word, approved, covers all.

Alternative if you would rather build features first: this phase can be deferred, and the honest consequence is that the next feature layers add more sign-producing surfaces to reconcile later, and the convergence layer stays blocked on it either way.

## Implementation record (2026-08-09) - BUILT AND VERIFIED, PENDING PUBLICATION

Built on branch sign-convention-v1 (one commit on top of published main 7d170f8; tip 61733f342c0cc9eabb71139d3fb90a365ede2118). Additive: the README plus eleven model files that gained accessor properties only; no field, value, or certified behavior changed.

Approved decisions executed. SC-A: an inert `Sign` type with named constructors and accessors, no arithmetic, no `__int__` or `__index__`, verified inert by test. SC-B: additive accessors on all thirteen sign-carrying model classes, using deferred imports because `engine.astrology`'s package import registers vargas that import these same models. SC-C: `sign_conventions.py` as the single declared source of truth, recorded into the certification artifact so the conventions read as evidence.

Design change made during implementation and recorded for honesty: the plan's Gate 3 asked for exhaustive twelve-value coverage per field. One chart-derived field, DashamsaChart.ascendant_sign, reached eleven of twelve on a fixed sweep grid, and demanding full coverage would have made the gate fragile in a way a future maintainer could only "fix" by weakening it. The criterion was replaced with a discriminating-witness proof: observed values must lie in the declared range and must include the value impossible under the other convention (0 proves zero-based, 12 proves one-based). That pair of conditions is necessary and sufficient, so each declaration is proven rather than sampled, and an unproven declaration fails loudly. Coverage breadth is still recorded as data.

Gate results. Gate A, weighted highest: SHA-256 sweeps over 54,697 dense and ULP-adversarial points for certified D9, D10, and all five registry vargas are byte-identical at published main and at this commit, verified by one identical script run against both worktrees. Gate B: exhaustive twelve-sign correctness plus adversarial input rejection and inertness. Gate C: seventeen index fields proven across 192 real charts at two locations, zero mismatches, undeclared-field and stale-declaration detection both active. Gate D: 59,988 cross-layer surface checks, with D1 and the KP chain proven to name the same rashi after exactly one conversion. Full battery: 372 tests, eleven independent validators, legacy gate 5/5, eleven certification runners regenerate PASS.

## Publication record (2026-08-09)

Published via owner bundle relay: origin/sign-convention-v1 pushed, main fast-forwarded 7d170f8 -> 61733f342c0cc9eabb71139d3fb90a365ede2118. Fresh-clone post-publication verification (EXECUTED): 372 tests, eleven independent validators PASS, legacy gate 5/5, eleven certification runners regenerate PASS, tree clean. SIGN_CONVENTION_V1 is CERTIFIED and PUBLISHED. The documented convergence-layer prerequisite is closed, and the convention split is now machine-enforced: a new sign-typed field added without a declaration fails the default gate.
## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-09 | Lifted into docs/ from the out-of-repository plan document(s): SIGN_CONVENTION_PLAN.md. Content preserved; header, provenance note and change history added per docs/DOCUMENTATION_STANDARD.md s2. |
