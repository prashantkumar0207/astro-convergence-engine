<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | IMPLEMENTED AND CERTIFIED - decision entry ADR-0007 PROPOSED pending owner ratification (Q1) |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-09 |
| Review cadence | TBD (see docs/OPEN_QUESTIONS.md Q1) |

# Vimshottari dasha layer specification

> **Provenance and normative status.** This specification was authored as a plan,
> approved by the owner conversationally, and implemented before being lifted into
> `docs/`. `docs/PROJECT_CONSTITUTION.md` s7 states that anything not in the repository
> is input material and not truth, so the out-of-repository original carried no
> authority; this file is the resident specification. The governing decision is recorded
> in `docs/DECISION_LOG.md` at ADR-0007, whose status is PROPOSED pending owner
> ratification (Q1). The text below is DESCRIPTIVE of the certified implementation and
> of the decisions actually taken; the ADR is the normative record. Sections retain the
> numbering of the original plan, including its implementation and publication records,
> which are preserved as dated evidence.

Date: 2026-08-09
Status: PROPOSED. Implementation starts only after explicit approval.
Base: origin/main d0d79fe (KP_CHAIN_V1 certified and published).

## 1. Objective and scope

Build VIMSHOTTARI_V1: the Vimshottari dasha timeline (mahadasha, antardasha, pratyantardasha) seeded from the birth Moon's nakshatra position, as a new isolated engine/dasha/ package. This is the roadmap's next layer and everything it depends on is already certified: the boundary-hardened Moon nakshatra classification, the exact Vimshottari tables (certified in engine/kp/tables.py), and the provenance-stamped astronomy.

Explicit non-goals of V1: no other dasha systems (Ashtottari, Yogini, and the rest come later, each with its own ADR), no transit or event overlays, no interpretation, no KP-specific dasha refinements beyond the shared Vimshottari mathematics.

## 2. The mathematics (all exact rational until final date conversion)

The birth Moon's fraction elapsed within its nakshatra determines the balance of the first mahadasha: the nakshatra's Vimshottari lord runs years_lord x (1 - elapsed_fraction) from birth. Mahadashas then follow the fixed 9-lord cycle totaling 120 years. Each mahadasha subdivides proportionally by the same year weights for antardashas, and again for pratyantardashas, exactly the recursive proportional structure already certified in the KP sub-lord tables. All proportions stay in Fraction arithmetic; only the final conversion from elapsed years to calendar dates touches floats, through the Julian Day pipeline.

## 3. Decisions that need your explicit sign-off

Decision DA-A, the year-length convention. This is the one genuinely open classical convention in Vimshottari: traditions and software variously use a 365.25-day year, the sidereal year (about 365.2564 days), the tropical year (about 365.2422 days), or a 360-day savana year, and the choice shifts period boundaries by days to months over a lifetime. There is no legacy in-repo oracle for dashas, so I recommend: implement year length as an explicit field on a DashaProfile (no hidden default, same philosophy as CalculationProfile), certify V1 against the pyjhora external oracle under whatever year convention pyjhora documents (pyjhora is already this project's accepted external oracle from the D9/D10 certification), and record that convention in every dasha output's provenance. Additional conventions can be certified later as named profiles without touching the certified one. The alternative is picking one convention from literature without an oracle, which would leave V1 with no independent check; I advise against that.

Decision DA-B, seeding profiles. The Moon longitude that seeds the dasha depends on the ayanamsa. Parashari dasha work must seed from a PARASHARI_LAHIRI snapshot and KP dasha work from a KP_KRISHNAMURTI snapshot; the package exposes school-explicit entry points (dasha timelines record which profile seeded them in provenance) and refuses profile-less input, mirroring the KP layer's isolation discipline.

Decision DA-C, timeline depth. V1 certifies three levels (maha, antar, pratyantar). Deeper levels (sookshma, prana) are mathematically trivial extensions but multiply the oracle-comparison surface; I recommend deferring them to keep the certification tight, with the recursion written so depth is a parameter.

## 4. Certification gates

Gate 1, exact-arithmetic invariants: every level's periods sum exactly to the parent period (Fraction equality); the 120-year cycle closes exactly; balance-of-dasha plus remaining mahadashas equals 120 years minus elapsed; boundary cases (Moon exactly on a nakshatra boundary, exact interval starts per the certified [start, end) rule) behave per the documented convention.

Gate 2, cross-layer consistency: the seeding nakshatra and its lord must agree with the certified KP chain and the certified engine nakshatra classification on the same longitude, including at boundaries.

Gate 3, external oracle: pyjhora as the independent reference. Frozen comparison set: the 11-case holdout matrix (both profiles where applicable) plus dedicated Moon-boundary cases; compare mahadasha lord sequence and start/end instants within a documented tolerance derived from the oracle's own precision, with categorical (lord sequence) tolerance zero.

Gate 4, independent validator: root-level validate_vimshottari_holdout.py with an in-file reference implementation built differently from the production code (closed-form prefix sums rather than recursive subdivision), zero-tolerance on lord sequences and exact-rational period arithmetic.

Gate 5, certification artifact plus regression-proof battery: certification/VIMSHOTTARI_V1_certification.json regenerated from scratch by a runner; full existing battery (267 tests, three validators, legacy gate, both certifiers) must pass untouched.

## 5. Implementation order

Step 1: tables/engine (exact rational core) with Gates 1 and 2. Step 2: calendar conversion through the JD pipeline plus DashaProfile with the pinned year convention. Step 3: oracle comparison battery (Gate 3) and independent validator (Gate 4). Step 4: certification runner, artifact, additive docs (Gate 5). Publication by bundle relay or PAT, then fresh-clone verification. Each step commits only after the full battery passes.

## 6. Risks

pyjhora installation brings heavy dependencies and its own ephemeris handling; it will be used strictly as an oracle in comparison scripts, never imported by production code, and pinned by exact version in the certification artifact. Year-convention ambiguity is contained by Decision DA-A (explicit profile field, oracle-pinned certification). Timezone-to-JD subtleties are already certified in Tier-0 and reused, not reimplemented.

## 7. What I need from you

Approve or amend: the overall plan, DA-A (year length as explicit profile field, V1 certified against the pyjhora-documented convention), DA-B (school-explicit seeding profiles), DA-C (three levels in V1). One word, approved, covers all four.

## Implementation record (2026-08-09) - BUILT AND VERIFIED, PENDING PUBLICATION

Built on branch vimshottari-v1 (two commits on top of published main d0d79fe; tip 7394441ce0c933f7f6d3b82e661f4234f8c5d1d6). Provably additive: only README.md modified, everything else new files.

Approved decisions executed: DA-A year length pinned as explicit DashaProfile (mean sidereal year, exactly 91314091/250000 days, PyJHora const.sidereal_year, passed explicitly to the oracle as MEAN_SIDEREAL_YEAR); DA-B school-explicit seeding with provenance guards; DA-C depths 1-3.

Key methodology finding, recorded per D-001/D-007: PyJHora's Moon differs from the engine's swetest-certified Moon by up to 0.75 arcsec across the holdout (about 1 arcsec on the Case C spot check). Since dasha start times amplify Moon error by roughly a factor of 190, a naive date comparison would be dominated by the oracle's astronomy. The certified gate therefore injects the oracle's own Moon into the engine's timeline mathematics: 1,782 dasha-bhukti rows across 11 cases x 2 profiles, zero lord mismatches, max start delta 1.4e-9 days. Independent closed-form validator: 1,081 Moon cases, 819 exact periods each on the dense set, zero failures. Full battery: 287 tests, four independent validators, legacy gate 5/5, all certifiers regenerate PASS.

## Publication record (2026-08-09)

Published via owner bundle relay: origin/vimshottari-v1 pushed, main fast-forwarded d0d79fe -> 7394441ce0c933f7f6d3b82e661f4234f8c5d1d6. Fresh-clone post-publication verification (EXECUTED): 287 tests, all four independent validators PASS (D9, D10, KP, Vimshottari), legacy gate 5/5, all three certification runners regenerate PASS, tree clean. VIMSHOTTARI_V1 is CERTIFIED and PUBLISHED.
## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-09 | Lifted into docs/ from the out-of-repository plan document(s): VIMSHOTTARI_DASHA_PLAN.md. Content preserved; header, provenance note and change history added per docs/DOCUMENTATION_STANDARD.md s2. |
