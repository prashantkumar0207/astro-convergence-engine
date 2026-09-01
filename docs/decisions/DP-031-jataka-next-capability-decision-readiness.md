<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents options and a recommendation. DECIDES NOTHING. Requires owner approval. Section J records a narrowly scoped D24-vs-D40 comparative study finding the evidence genuinely tied - no winner manufactured. |
| Version | 1.1.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-09-01 (section J added: D24 vs D40 comparative methodology study, per "CEO AUTHORIZATION — D24 vs D40 METHODOLOGY ADJUDICATION"; sections A-I unedited) |
| Review cadence | TBD |

# DP-031. Next JATAKA capability decision-readiness

## 0. Authorization and scope

Authorized by the owner's explicit "CEO AUTHORIZATION — DP-031 NEXT JATAKA CAPABILITY DECISION-READINESS"
instruction (2026-09-01). This is a decision-readiness/research authorization only - **it does not
implement anything, does not create an ADR, does not modify production code, does not modify any
certification artifact, does not create an implementation specification, and does not select a
capability.** Per `docs/decisions/README.md`'s own rule, "a paper that resolves its own question has
failed" - that discipline is followed here exactly as it was in `DP-021` and `DP-023`.

**State audit performed before this investigation began:** branch `phase-g-governance`, local HEAD =
`cc11660251f0fb1fd3f2953072935de234b40467`, working tree clean, tree content identical to `origin/main`
at `60748b3204ffff0c8f728708caf593d1a16af43d` (confirmed via `git diff --stat`, zero output). Governance
gates clean before this task began. Highest ratified ADR: `ADR-0081`. Highest registered DP: `DP-030`
(31 after this paper's own registration, per `ADR-0040`, in `docs/decisions/README.md` before drafting).

**Relationship to `DP-021`/`DP-023`:** those papers remain unedited and are the historical record of the
first JATAKA-capability selection. This paper does not repeat their reasoning where nothing has changed;
it re-verifies every load-bearing claim directly against current repository state rather than assuming
`DP-021`/`DP-023` are still accurate, per the owner's own explicit instruction not to assume another
Varga is automatically next or that D45's prior selection determines this answer.

**The single fact that changes everything since `DP-023`:** three JATAKA capabilities are now
implemented and certified - `D45` (`ADR-0077`, commit `2cb9f30`), `KP_SIGNIFICATOR_V1` (`ADR-0078`/
`ADR-0079`, commit `c6f58f5`), and `PARASHARI_YOGA_V1` (`ADR-0081`, commit `9accfb7`). Verified directly
this task, not assumed:

```
$ python -c "from engine.astrology import CERTIFIED_PRODUCTION_VARGAS; print(CERTIFIED_PRODUCTION_VARGAS)"
((2, 'parashara'), (3, 'parashara'), (7, 'parashara'), (12, 'parashara'), (30, 'parashara'), (45, 'parashara'))
```
`engine/kp/significators.py` and `engine/parashari/mahapurusha_yoga.py` both exist and are registered
production modules (confirmed by direct file read, not inferred from a certification artifact alone -
`certification/*.json` existing does not by itself imply a production module exists, as this project's
own KP/Parashari-yoga history twice demonstrated).

## A. Updated candidate inventory

Status vocabulary as `DP-021` established: **certified and production-usable** / **not ready** /
**blocked, named reason** / **explicitly deferred by a recorded decision**.

| # | Candidate | Status since `DP-023` | Evidence |
|---|---|---|---|
| 1 | D24 Siddhamsa | **Unimplemented, cleanly ready** (unchanged) | `engine/astrology/` has no `varga_d24.py`; `docs/VARGA_CERTIFICATION_ROADMAP.md` s4: contract Cyclic, shape confidence High, content confidence High, no payload gap |
| 2 | D40 Khavedamsa | **Unimplemented, cleanly ready** (unchanged) | Same roadmap row: Cyclic, High, High, no payload gap; no `varga_d40.py` |
| 3 | D16 Shodashamsa | **Still blocked** - payload/label-table architecture undecided | `docs/VARGA_CERTIFICATION_ROADMAP.md` s3; `DP-024` remains `DEFERRED`, re-confirmed this task (section E below) |
| 4 | D20 Vimsamsa | **Still blocked** - start-triple content genuinely disputed, plus payload gap | Roadmap s4: content confidence "Medium... genuinely disputed" |
| 5 | D27 Bhamsa | **Still blocked** - payload gap plus ULP-width note | Roadmap s3/s4 |
| 6 | D60 Shashtiamsa | **Still blocked** - even-sign reversal disputed, plus payload gap | Roadmap s4: "Medium... genuinely disputed" |
| 7 | D4 Chaturthamsa | **Still blocked** - Segment-vs-`step` contract choice undecided | Roadmap s3 |
| 8 | D45 Akshavedamsa | **DONE** | `ADR-0077`; `engine/astrology/varga_d45.py`, commit `2cb9f30` |
| 9 | Vimshottari depth extension (depth 4+) | **Unimplemented, still methodology-ready** (unchanged) | `vimshottari_from_moon()` still raises `ValueError` for `depth not in (1,2,3)`, re-confirmed this task |
| 10 | Parashari aspect coverage extension (fractional/sputa drishti; Rahu/Ketu's own aspects) | **Still not ready** - Decisions AS-A/AS-B remain undecided (unchanged) | `engine/parashari/drishti.py` docstring, re-confirmed unedited this task |
| 11 | Shadbala (planet strength) | **Still not ready**, unchanged, highest risk of any candidate | `engine/astrology/planet_strength.py::planet_strength()` still raises `NotImplementedError` by explicit design, re-confirmed this task |
| 12 | Jaimini Chara karakas | **Still blocked** - `specs/PROJECT_CHARTER.md`'s own analytical-systems list still does not name Jaimini, re-confirmed this task | Charter text unchanged since `DP-023` |
| 13 | Polar-Placidus certification gap + M-04 provenance fix | **Still open, still explicitly not a JATAKA candidate** (Tier-0/FOUNDATION-tier maintenance) | Root `DECISION_LOG.md` D-0008 entry: "M-04 and M-05... not authorised for remediation," re-confirmed this task, unchanged since `DP-021`/`DP-023` |
| 14 | `KP_SIGNIFICATOR_V1` | **DONE** | `ADR-0078`/`ADR-0079`; `engine/kp/significators.py`, commit `c6f58f5` |
| 15 | `PARASHARI_YOGA_V1` | **DONE** | `ADR-0081`; `engine/parashari/mahapurusha_yoga.py`, commit `9accfb7` |
| 16 | KP significator extensions (Four Step Theory, Ruling Planets, horary) - a further KP capability, newly evaluable now that V1 exists | **Not ready, never methodology-researched** | `ADR-0078` section (frozen V1 scope) explicitly excludes all three; `docs/KP_SIGNIFICATOR_SPEC.md` v0.2.0 sections 5/6 marked "N/A per the owner's explicit exclusion," not answered |
| 17 | Parashari yoga extensions (any yoga beyond the five Panch Mahapurusha - Raja yoga, Dhana yoga, Sunapha/Anapha/Kemadruma/Adhi, bhanga/cancellation logic for the existing five) - a further Parashari capability, newly evaluable now that V1 exists | **Not ready, and now doubly evidenced as high-risk by V1's own experience** | `ADR-0081` section 10 explicitly excludes bhanga, combustion, and every other yoga from V1; `DP-027` section B's fragmented-source finding (dozens to hundreds of named yogas, materially different qualifying conditions between texts) was not merely theoretical - PARASHARI_YOGA_V1's own five-yoga certification required a full independent-transcription/oracle-integrity design effort per graha; extending to any additional yoga repeats that full cost per yoga, not a marginal extension |

## B. Evidence for the two newly-evaluable "extension" candidates (not scored by `DP-021`/`DP-023`, since neither V1 existed yet)

**KP significator extensions:** `docs/KP_SIGNIFICATOR_SPEC.md` v0.2.0 (the governing specification for
`KP_SIGNIFICATOR_V1`) states, in its own section 0: "Sections 5 and 6 (four-step; ruling planets) are
marked N/A per the owner's explicit exclusion (item 5) rather than answered." No methodology-readiness
research has ever been performed for Four Step Theory or Ruling Planets specifically - `DP-028` section H
found "PyJHora audited and found to lack any dedicated significator/ruling-planet/four-step function,"
meaning even the *oracle* question for these extensions is open, not merely the methodology question.
Horary generally remains excluded by `ADR-0027` Decision 3, unchanged.

**Parashari yoga extensions:** `ADR-0081` section 10, unedited, lists among its non-claims: "no bhanga/
cancellation logic of any kind... no other yoga - Raja/Dhana/Sunapha/Anapha/Kemadruma/Adhi and the
remaining PyJHora-catalogued yogas are all out of scope." `DP-027` section B, drafted before any yoga
work began, already flagged "classical sources name materially different yoga sets and qualifying/
cancellation (bhanga) conditions, with no single founding authority the way KP has K.S. Krishnamurti's
own body of work" - `PARASHARI_YOGA_V1`'s own execution now provides direct, first-hand confirmation of
that risk rather than a prediction: certifying five yogas sharing one simple structural pattern (kendra
AND own-sign-or-exaltation) required an independently-transcribed dignity table, a from-scratch validator,
a Mercury-specific mutation-masking defect discovered and corrected mid-design, and explicit PyJHora-
corroboration-only treatment (only two of five yogas' PyJHora functions were ever confirmed to exist).
Extending to structurally different yoga families (Raja yoga's own dozens of sub-varieties; Dhana yoga;
bhanga/cancellation logic layered on top of the five already-certified yogas) is not a small increment on
this base - each family would need its own source selection, its own independent transcription, and its
own oracle-availability research from scratch, exactly the process `DP-027`/`ADR-0081` performed once
for a single, comparatively simple five-yoga family.

## C. Dependency graph (updated)

D24/D40 depend only on the already-certified Tier-0 sidereal-longitude kernel - unchanged, no dependency
on any other candidate, none on each other, none on D45's own completion. Vimshottari depth extension
depends only on the already-certified, already-generalizing `_subdivide()` recursion. Aspect coverage
extension depends on the already-certified `PARASHARI_DRISHTI_V1`. Shadbala depends on already-certified
sign/house/aspect data as raw input only; its blocker is the strength formula, not a data dependency.
Jaimini karakas depend only on already-certified sidereal longitudes but are gated by `specs/
PROJECT_CHARTER.md`'s own system-scope clause, a governance dependency none of the varga/dasha/aspect
candidates carry. KP significator extensions depend on the already-certified `KP_CHAIN_V1` and the now-
certified `KP_SIGNIFICATOR_V1` production module, plus an unwritten methodology specification for each
extension and an unresolved oracle question (`DP-028`'s own finding). Parashari yoga extensions depend on
already-certified D1/aspects/vargas (zero missing calculation dependency, exactly as the original five
yogas had) plus, per family, an unwritten methodology specification and its own independent-transcription/
oracle-availability research.

## D. Preservation of `DP-024`'s deferral

`DP-024` (varga `step`-field and payload/label-table architecture) remains **DEFERRED by owner
instruction**, re-confirmed directly this task (`docs/decisions/README.md` DP-024 row, unedited since
2026-08-25). **This paper does not resolve it, and no candidate scored below requires resolving it**: D24
and D40 (section E's recommendation) have no payload gap and no undecided contract, exactly like D45
before them - the same reason `DP-024`'s deferral did not block D45 continues to hold for D24/D40. D16,
D20, D27, D60, and D4 remain excluded from near-term selection precisely *because* they would require
resolving `DP-024` (or, for D20/D60, a separate disputed-content adjudication) - consistent with the
owner's own explicit instruction not to resolve `DP-024` merely to make a candidate selectable.

## E. Scoring matrix (the owner's own ten required axes)

Scale: **Ready/Low-risk** favorable, **Partial/Moderate** mixed, **Not ready/High-risk** unfavorable,
stated per-candidate rather than numerically, matching `DP-023`'s own discipline against manufactured
precision.

| Candidate | 1. Methodology maturity | 2. Source/authority status | 3. Unresolved interpretive questions | 4. Architectural dependencies | 5. Certification feasibility | 6. Independence/oracle requirements | 7. JATAKA-scope eligibility (`ADR-0075`) | 8. Implementation complexity | 9. Risk of premature framework decisions | 10. Expected value to JATAKA foundation |
|---|---|---|---|---|---|---|---|---|---|---|
| **D24 Siddhamsa** | Ready - construction undisputed | High - Parashara/BPHS, roadmap confidence High | None flagged | Tier-0 only, none on other candidates | Low - six-times-proven `NEW_VARGA_IMPLEMENTATION_TEMPLATE.md` template (D2/D3/D7/D9/D10/D12/D30/D45) | Low - PyJHora oracle path already exercised eight times | Named in `Q8_CLOSURE_MATRIX.md` s5 literally ("remaining production vargas") - no `ADR-0075` interpretive work even required | Low | **None** - no framework decision needed, `DP-024` untouched | Moderate - incremental analytical depth, same class of value D45 already delivered |
| **D40 Khavedamsa** | Ready - construction undisputed | High - roadmap confidence High | None flagged | Tier-0 only | Low - same template | Low - PyJHora path proven | Named in `Q8_CLOSURE_MATRIX.md` s5 literally | Low | **None** | Moderate-low - roadmap's own third tier, same as D24 |
| D16 Shodashamsa | Blocked | High for construction, but payload undecided | Deity-payload architecture (`DP-024`) | Requires resolving `DP-024` first | Moderate-High (payload) | Unconfirmed pending payload design | Named in s5, but not selectable without `DP-024` | Low-moderate | **High if selected now** - would force `DP-024` resolution under this candidate's own time pressure | Moderate-high, but not realizable without the deferred decision |
| D20 Vimsamsa | Blocked | Medium, genuinely disputed start triple | Which start triple is correct (unresolved, no adjudication path proposed anywhere) | Requires content adjudication AND `DP-024` | High | Unconfirmed | Named in s5, but content-disputed | Low technically, high on the disputed question | **High** - the disputed-content question is exactly the kind of "under time pressure" decision this project's governance culture prohibits | Moderate, undermined by dispute risk |
| D27 Bhamsa | Blocked | High for construction, payload undecided, ULP-width flagged | Deity-payload architecture; ULP-sensitive width | Requires `DP-024` | Moderate (ULP, D7/D9-precedented) | Low once payload resolved | Named in s5, blocked on `DP-024` | Moderate | **High if selected now**, same reason as D16 | Moderate |
| D60 Shashtiamsa | Blocked | Medium, genuinely disputed even-sign reversal | Reversal question; deity-payload architecture | Requires content adjudication AND `DP-024` | Moderate | Unconfirmed | Named in s5, content-disputed | Low technically, high on the disputed question | **High** | Moderate, undermined by dispute risk |
| D4 Chaturthamsa | Blocked | High for construction, contract choice undecided (Segment vs. `step`) | Segment-table vs. `step`-field architecture choice | Requires the contract decision (a narrower cousin of `DP-024`) | Low (D3 precedent) once chosen | Low | Named in s5, blocked on contract choice | Moderate | **Moderate** - narrower than `DP-024` itself but still a framework choice | Moderate |
| Vimshottari depth extension | Ready - mechanical continuation, zero new methodology | High - identical rule to depths 1-3 | None | `VIMSHOTTARI_V1` only | Low | Low | Named in s5 literally | Very low | **None** | **Low** - finer granularity only, unlocks nothing, reopens an area six ADRs (`ADR-0053`, `ADR-0069`-`ADR-0073`) just formally closed |
| Parashari aspect coverage extension | Not ready - AS-A/AS-B undecided | Moderate, multiple classical traditions for fractional drishti; whether nodes cast aspects is school-dependent | Which fractional-aspect table; whether Rahu/Ketu cast aspects at all | Extends `PARASHARI_DRISHTI_V1` only | Moderate-High - needs a new degree-of-influence oracle comparison, not binary presence | Uncertain - not investigated whether an oracle exists for degree-of-influence values | Named in s5 literally | Moderate | Moderate - AS-A/AS-B were deliberately left "deferred-not-decided," not accidentally unresolved | Moderate - some real leverage toward future yoga-strength work, per `DP-021` |
| Shadbala | Not ready | Low-moderate - six classically-varying sub-components, no single authority | Which sub-components; which textual tradition per sub-component | Sign/house/aspect data only, as raw input | High - most complex certification design of any candidate in this inventory | High - unclear an oracle exists for composite strength values | Named in s5 literally | High | **Highest of any candidate** - this project's own governance culture already names Shadbala as the canonical example of what NOT to implement without real methodology | High long-term, but not realizable without first resolving methodology risk that has never been reduced |
| Jaimini Chara karakas | Not ready in-repo | Moderate-high for the core ranking rule, but charter-scope gap unresolved | Whether Jaimini is even a chartered system (unresolved, above `ADR-0075`'s own authority) | Sidereal longitudes only - narrowest footprint of any candidate | Unknown - no Jaimini precedent exists anywhere in this project | Unknown | **Not resolved by `ADR-0075`** - that ruling concerns `Q8_CLOSURE_MATRIX.md` s5's JATAKA-internal scope, not `PROJECT_CHARTER.md`'s separate, senior-in-hierarchy analytical-systems list, which still does not name Jaimini | Low for the math, high for opening a fourth analytical system | Moderate-high strategically (new system), low technically | Low-moderate - narrow technical value, disproportionate governance commitment |
| KP significator extensions (Four Step, Ruling Planets, horary) | **Not ready, unresearched** | Unknown - never independently sourced the way `KP_SIGNIFICATOR_V1`'s core methodology was (`DP-028`) | Which of several documented "Four Step" variant traditions; ruling-planets' own horary-adjacent scope boundary | `KP_CHAIN_V1` and `KP_SIGNIFICATOR_V1` both already certified | Unknown - `DP-028` found PyJHora lacks any dedicated function for any of the three | High - no confirmed oracle path exists for any of the three | Eligible in principle (KP is chartered, and `ADR-0078` already performed KP's own JATAKA-scope interpretive work once) but each extension needs its own methodology-readiness paper first, exactly as `D-008` needed one before V1 | High - each is its own documented variant-tradition problem | High - identical risk class to Parashari yoga extensions, now with one additional confirmed data point (`DP-028`'s own oracle-absence finding) | High in principle (chartered, product-named), unrealizable without dedicated readiness work first |
| Parashari yoga extensions (further yogas, bhanga) | **Not ready, and now empirically confirmed high-cost per family** | Low - fragmented across sources, no single founding authority, confirmed in practice by `PARASHARI_YOGA_V1`'s own build | Which classical source per yoga family; qualifying and cancellation (bhanga) conditions, explicitly contested even within V1's own five-yoga scope (excluded, not resolved) | Already-certified D1/aspects/vargas only - zero missing calculation dependency, same as before | High - each new yoga family needs its own independent-transcription and oracle-availability research, proven costly even for the simplest case (Panch Mahapurusha) | Uncertain per family - only `ruchaka_yoga`/`bhadra_yoga` were ever confirmed to exist as PyJHora functions; no other yoga family's oracle coverage has been checked | Eligible in principle (`ADR-0081` already performed the JATAKA-scope interpretive work once for Parashari yoga generally) but each family needs its own methodology-readiness paper | High per family | High - picking a yoga family under time pressure is exactly the "authoritative-sounding but silently arbitrary" failure mode `DP-027`/`ADR-0081` were built to avoid | Highest per-item value if successful (most recognizably "Jataka"), but highest manufactured-confidence risk of any candidate in this inventory |
| *Polar-Placidus + M-04 (scored for completeness, not as a JATAKA candidate, matching `DP-021`/`DP-023`'s own explicit exclusion)* | Bounded, not fully ready | N/A - engineering gap, not a methodology question | What a certified system returns outside the verified domain | Extends the Tier-0 kernel only | Moderate - `RISE_SET_V1`'s own `NO_RISE`/`NO_SET` pattern applies directly | Low - `swetest` already the Tier-0 oracle | **Not a JATAKA-scope item at all** - Tier-0/FOUNDATION-tier maintenance, per `DP-021`/`DP-023`'s own explicit framing, unchanged | Low-moderate | Low | Narrow but real - the one confirmed prerequisite for KP significator extensions specifically (cusp-handling), not for any Parashari-track candidate |

## F. Ranked recommendation

1. **D24 (Siddhamsa) or D40 (Khavedamsa) - co-equal, recommended, medium-high confidence.** These are the
   only two candidates in this entire inventory, including the two newly-evaluable extension tracks, that
   are simultaneously methodology-ready, low-certification-difficulty, dependency-clean, require zero
   framework decision, and are literally named in `Q8_CLOSURE_MATRIX.md` s5's own text (no `ADR-0075`
   interpretive burden at all). This is the same reasoning `DP-023` applied to isolate D45 from D16/D20/
   D24/D27/D40/D60 - reapplied here now that D45 is done, D24 and D40 are what remains at that same tier.
   Confidence is medium-high, not high, because `docs/VARGA_CERTIFICATION_ROADMAP.md` itself remains
   `Status: PROPOSED`, never ratified, and its own section 5 risk order groups D24 and D40 together without
   ranking one above the other - this paper does not manufacture a tiebreaker between them.
2. **Vimshottari depth extension** - equally methodology-clean and dependency-free, but lowest expected
   value of any ready candidate and reopens a track this session only just formally closed (six ADRs).
   Worth naming as a fallback, not as a co-recommendation.
3. **Not recommended for selection now, and not because of any framework-architecture question requiring
   resolution:** aspect coverage extension (AS-A/AS-B genuinely undecided, not merely unimplemented).
4. **Not recommended - would force `DP-024` resolution under time pressure:** D16, D27 (payload
   architecture), D4 (narrower contract-choice cousin of the same problem). Per the owner's own explicit
   instruction, this paper does not resolve `DP-024` to make any of these selectable.
5. **Not recommended - disputed content, not merely undecided architecture:** D20, D60.
6. **Not recommended - highest risk in the entire inventory, unchanged since `DP-023`:** Shadbala.
7. **Not recommended - governance gate above `ADR-0075`'s own authority, unresolved:** Jaimini Chara
   karakas (charter-scope gap).
8. **Not recommended for direct selection, but flagged as the two highest-value tracks if the owner wants
   to invest in extending an already-certified system rather than adding a new one:** KP significator
   extensions and Parashari yoga extensions. Both are eligible in principle under `ADR-0075` (each parent
   V1 already performed the JATAKA-scope interpretive work once), but **neither has ever had its own
   methodology-readiness research performed** - unlike D-008's own eleven-element checklist that existed
   before `KP_SIGNIFICATOR_V1` began, no equivalent checklist exists for Four Step Theory, Ruling Planets,
   or any additional Parashari yoga family. Selecting either for direct implementation now would repeat
   exactly the manufactured-confidence risk `DP-026`/`DP-027`/`DP-028` were built to prevent for their own
   parent capabilities. **If the owner wants to pursue either, the correct next step is a dedicated
   methodology-readiness paper for the specific extension (mirroring `DP-026`→`DP-028`'s own KP pattern),
   not implementation and not this paper's own recommendation slot.**

**Not recommended, out of JATAKA scope entirely, matching `DP-021`/`DP-023`'s own treatment:** polar-
Placidus + M-04 closure remains worth doing as Tier-0/FOUNDATION-tier maintenance, independent of whichever
JATAKA capability is chosen next - not itself a JATAKA candidate, not scored competitively above.

## G. Risks

Selecting D24 or D40 carries the same low risk profile D45 carried: no disputed content, no undecided
architecture, a now-six-times-proven certification template, narrow additive blast radius (registry-
gated). The main residual risk, disclosed rather than hidden, is identical in kind to D45's own: the
roadmap document itself remains unratified `Status: PROPOSED`, so this paper's own reliance on its risk
order and confidence columns is evidence, not ratified fact. Selecting either KP or Parashari-yoga
extensions without first commissioning their own dedicated methodology-readiness paper carries the
highest risk in this inventory - both would either require inventing methodology under time pressure or
produce a certification gate that cannot meaningfully fail, the exact failure mode `.claude/rules/
certification.md` prohibits, now doubly evidenced by the real cost `PARASHARI_YOGA_V1`'s own five-yoga
build already demonstrated.

## H. Explicit non-claims

This paper does not select D24, D40, or any other capability - that remains the owner's act. It does not
create an ADR. It does not resolve `DP-024`'s deferred varga-framework architecture question, and does
not require resolving it for either recommended candidate. It does not resolve D20's or D60's disputed
content. It does not resolve AS-A/AS-B. It does not draft a methodology-readiness paper for KP
significator extensions or Parashari yoga extensions - it only identifies that such a paper would be the
correct next step if the owner wants to pursue either track. It does not determine whether Jaimini is or
should become a chartered system. It does not implement anything, modify any production code, modify any
certification artifact, or touch FOUNDATION, Tier-0, or any already-closed Dasha item. It does not treat
`docs/VARGA_CERTIFICATION_ROADMAP.md` as ratified merely by relying on its evidence, consistent with
`DP-023`'s own identical disclosure.

## I. Exact CEO decision required

1. **Select the next JATAKA capability**: D24, D40 (co-recommended, section F.1), Vimshottari depth
   extension (fallback, section F.2), or direct otherwise - including, if the owner prefers, authorizing a
   dedicated methodology-readiness paper for a KP or Parashari-yoga extension track instead of selecting a
   Varga at all.
2. If D24 or D40 is selected: confirm which of the two (this paper does not manufacture a tiebreaker), and
   authorize that capability's own ADR, naming the classical source and school per the established
   template.
3. If neither D24 nor D40 is wanted: state whether `DP-024`'s deferred varga-framework architecture
   question should now be resolved to unblock D16/D27/D4 (or D20/D60's own content dispute separately
   adjudicated) - this paper does not recommend doing so merely to widen the candidate set, per the
   owner's own explicit instruction.
4. Whether to authorize a dedicated KP significator-extension methodology-readiness paper (Four Step
   Theory and/or Ruling Planets), mirroring `DP-026`→`DP-028`'s own pattern - not implementation.
5. Whether to authorize a dedicated Parashari yoga-extension methodology-readiness paper (a named further
   yoga family, or bhanga/cancellation logic for the existing five), mirroring `DP-027`'s own pattern - not
   implementation.
6. Whether polar-Placidus + M-04 closure should now be authorized as Tier-0/FOUNDATION-tier maintenance,
   independent of whichever JATAKA capability is chosen (unchanged open item from `DP-021`/`DP-023`).

## J. D24 vs D40 comparative methodology study (resumption, 2026-09-01)

Authorized by the owner's explicit "CEO AUTHORIZATION — D24 vs D40 METHODOLOGY ADJUDICATION" instruction:
"DP-031 is accepted as decision-readiness work. Its conclusion that D24 and D40 are the two strongest
remaining candidates is accepted without treating either as selected. Perform a narrowly scoped
comparative methodology study of D24 and D40 only." Sections A-I above are unedited. This section does
not select a capability, does not create an ADR, does not implement anything, and does not resolve
`DP-024`. Per the owner's own explicit instruction, `DP-024`'s general Varga step/payload architecture is
resolved for neither candidate here - section J.3 below states why that was found unnecessary, not
assumed.

**Method note:** since `PyJHora` cannot be executed locally on this Windows host (its own environment
remains degraded - numpy import failure, a pre-existing, already-disclosed limitation, unchanged since
`ADR-0081`/`PARASHARI_YOGA_V1`), corroboration below was obtained by (a) direct primary-source retrieval
of Brihat Parashara Hora Shastra commentary/translation pages via web search and fetch, and (b) direct
reading of `PyJHora`'s own published source code (`naturalstupid/PyJHora`, GitHub, `charts.py`), not by
running it. This is read-only verification of external sources, not a repository change and not a claim
of executed oracle agreement - genuine oracle execution (matching `ADR-0077`'s own PyJHora cross-check for
D45) would still need to happen in this project's own CI hash-pinned oracle environment, exactly as every
other oracle-tier certifier in this project already requires.

### J.1 Per-candidate findings against the owner's thirteen required items

**D24 (Siddhamsa / Chaturvimshamsha):**

1. **Authoritative source/rule basis:** Parashara/BPHS, matching `docs/VARGA_CERTIFICATION_ROADMAP.md`
   section 4's own citation. A verbatim verse citation was located and retrieved this task (not merely a
   secondary paraphrase): "The Chaturvimshamsha distribution commences from Simha and Karkata,
   respectively, for an odd and an even Rashi," cited to BPHS Sarga 6, Shlokas 2-23 (via
   barbarapijan.com's own BPHS-sourced page). At least three independent modern sources, checked
   separately, agree on this exact construction.
2. **Competing schools or variants:** none found for the core sign-mapping rule. `PyJHora`'s own
   `chaturvimsamsa_chart()` function (read directly from its published source) offers three named
   `chart_method` variants: the default/Traditional method (odd -> Leo, even -> Cancer, both forward,
   `even_dirn=1`), `PARASARA_EVEN_REVERSE` (even-sign counting direction reversed), and
   `PARASARA_EVEN_DOUBLE_REVERSE` (even signs start from Leo's own base instead of Cancer's). **These
   exist as named alternate options in an independently-authored library, not as evidence the mainstream
   construction is disputed** - every external primary/secondary source independently retrieved this task
   describes only the plain forward-forward construction, with no source found describing the reversed
   variants as a competing textual tradition. This mirrors D45's own precedent exactly: `ADR-0077` found
   three non-Traditional-Parasara `PyJHora` chart methods for D45 and excluded them as non-claims without
   treating their existence as evidence of dispute in the certified construction.
3. **Unresolved interpretive disputes:** none in the sign-mapping itself. A real, but payload-only,
   convention exists and was not previously surfaced by `docs/VARGA_CERTIFICATION_ROADMAP.md`'s own "No"
   payload-gap claim for D24: BPHS names twelve presiding deities (Skanda, Parusdhara, Anala, Vishwakarma,
   Bhaga, Mitra, Maya, Antaka, Vrisha-Dwaja, Govinda, Madana, Bhima) that repeat twice per sign, and for
   **even** signs specifically, the deity sequence itself runs in reverse (starting from Bhima) - this is
   the actual referent of "reverse" in the classical tradition, not the sign-mapping direction, confirmed
   across multiple independently-retrieved sources. See J.3 for why this does not create a `DP-024`
   dependency.
4. **Exact computational rule:** `d_sign = (base + direction * division_index) mod 12`, `base = 4`
   (Leo, 0-indexed) for odd source signs, `base = 3` (Cancer, 0-indexed) for even source signs,
   `direction = +1` (forward) for both - a `CyclicVargaRule`, structurally simpler than D45's own
   three-category (movable/fixed/dual) construction, since D24 has only two categories (odd/even).
5. **Boundary/interval behaviour:** cell width = 30/24 = 5/4 = 1.25 degrees exactly. **Measured directly
   this task via exact rational (`Fraction`) arithmetic, mirroring `ADR-0077`'s own method for D45:** 1.25
   degrees is exactly representable in IEEE-754 double precision (`Fraction(float(Fraction(30,24)))` equals
   the exact fraction `5/4`) - **zero representation error, zero floor-classification boundary mismatches
   across all 23 internal per-sign boundaries**, computed directly, not assumed. This is a materially
   cleaner result than D45's own measured 3.553e-15-degree error and three genuine floor-classification
   mismatches (k=13, 26, 29) - D24 needs no special boundary-convention justification beyond the engine's
   own existing, already-certified promote-up tolerance.
6. **Required dependencies:** Tier-0 sidereal-longitude kernel only, already certified. No dependency on
   any other candidate or on D24's own deity payload.
7. **Contract freezable without general Varga architecture:** **Yes.** The D-sign classification (item 4)
   requires no payload/label-table decision. The deity finding in item 3 is real but, per this project's
   own established and unbroken precedent, out of scope: `VargaClassification` (`engine/astrology/
   varga_classifier.py`, read directly this task) carries only `d_sign`, `division_index`, `fraction` for
   every certified varga today, including D45, D30, and every other already-certified division - none
   exposes a deity/lord payload despite most classical vargas, D24 included, having their own named
   deity or lord traditions. D24's own future ADR can scope deity output as an explicit non-claim,
   mirroring `ADR-0077` section 10's identical treatment for D45 ("No interpretive/deity-based reading of
   D45 results is claimed"). This is a disclosed scoping choice, not an avoided architecture question -
   flagged for the eventual ADR to state explicitly, not silently omitted the way `docs/
   VARGA_CERTIFICATION_ROADMAP.md`'s own "No" payload-gap entry currently does.
8. **Oracle/reference availability:** `PyJHora`'s own `chaturvimsamsa_chart()` exists, confirmed by direct
   source read, with an identifiable default/Traditional-Parasara method matching the frozen construction
   (item 4). Not executed locally (method note above); execution would occur in CI's own hash-pinned
   oracle environment, matching every other oracle-tier certifier.
9. **Independent-validation feasibility:** straightforward - a from-scratch two-category modular
   reimplementation, the same shape of validator already built five times for D2/D3/D7/D12/D30/D45.
10. **Certification-gate feasibility:** fits the existing, six-times-proven `docs/
    NEW_VARGA_IMPLEMENTATION_TEMPLATE.md` checklist directly; `CyclicVargaRule`, no new contract needed.
11. **Historical/holdout validation feasibility:** standard established pattern (real ephemeris-driven
    protected holdout, drawn independently of boundary cases) applies without modification.
12. **Implementation complexity and risk:** Low - simpler than D45's own three-category rule, with a
    cleaner (zero-error) boundary result than D45's own measured result.
13. **JATAKA-scope basis under `ADR-0075`:** not needed - D24 is literally named in `Q8_CLOSURE_MATRIX.md`
    s5's own "remaining production vargas" text; no interpretive JATAKA-scope work is required, unlike
    `PARASHARI_YOGA_V1`/`KP_SIGNIFICATOR_V1`.

**D40 (Khavedamsa):**

1. **Authoritative source/rule basis:** Parashara/BPHS, matching the roadmap's own citation. Multiple
   independent modern sources retrieved this task agree: "the knowledge of the Lords of Khavedamsha in
   respect of odd signs is to be commencing from Aries and for even signs from Libra" - attributed to BPHS
   but, unlike D24, no verbatim Sanskrit-verse/Sarga-and-Shloka citation was located in the sources
   retrieved this task, only consistent paraphrase across independent sites. This is a real, if narrower,
   evidentiary gap relative to D24's own located verbatim citation - disclosed, not glossed over.
2. **Competing schools or variants:** `PyJHora`'s own `khavedamsa_chart()` (read directly from source)
   offers four named `chart_method` variants: the default/Traditional method (odd -> Aries, even -> Libra,
   both forward), Parivritti Cyclic, Even Reverse, and Parivritti Alternate. As with D24, no source
   retrieved this task describes the non-default variants as a competing reading of the same construction
   rather than a separate, clearly-labelled alternate tradition - mirroring D45's own precedent of
   excluding non-Traditional-Parasara methods as explicit non-claims, not evidence of dispute.
3. **Unresolved interpretive disputes:** none in the sign-mapping. D40 also carries a real classical deity
   tradition not mentioned in the roadmap's own "No" payload-gap entry: twelve deities (Vishnu, Chandra,
   Marichi, Twashta, Dhata, Siva, Ravi, Yama, Yakeshesha, Gandharva, Kala, Varuna) cycling through the
   forty divisions - but, unlike D24, **in the same order for all signs**, with no even-sign reversal of
   any kind (sign mapping or deity sequence) found in any source retrieved this task. D40's own overall
   structure is therefore marginally simpler than D24's (no reversal anywhere), though this has no effect
   on the certified D-sign contract, which excludes deity output for both, per J.1(D24) item 7's reasoning
   applied identically here.
4. **Exact computational rule:** `d_sign = (base + division_index) mod 12`, `base = 0` (Aries) for odd
   source signs, `base = 6` (Libra, 0-indexed) for even source signs, forward only - a `CyclicVargaRule`,
   the simplest two-category shape in this comparison (no direction variable needed at all, since both
   categories count forward).
5. **Boundary/interval behaviour:** cell width = 30/40 = 3/4 = 0.75 degrees exactly. **Measured directly
   this task, mirroring D24's own method:** exactly representable in IEEE-754 double precision - **zero
   representation error, zero floor-classification boundary mismatches across all 39 internal per-sign
   boundaries.** Identical clean result to D24, both materially better than D45's own measured result.
6. **Required dependencies:** Tier-0 sidereal-longitude kernel only, identical to D24.
7. **Contract freezable without general Varga architecture:** **Yes**, for the identical reason given for
   D24 (item 7 there) - `VargaClassification`'s own established D-sign-only scope, with deity output as a
   disclosed non-claim for D40's own future ADR.
8. **Oracle/reference availability:** `PyJHora`'s own `khavedamsa_chart()` exists, confirmed by direct
   source read, with an identifiable default/Traditional-Parasara method matching the frozen construction.
   Same execution caveat as D24 (method note above).
9. **Independent-validation feasibility:** straightforward, arguably the simplest of any candidate
   evaluated in this project's own JATAKA-varga work (no direction variable, only an offset).
10. **Certification-gate feasibility:** fits the existing template directly, identical to D24.
11. **Historical/holdout validation feasibility:** standard established pattern, unmodified.
12. **Implementation complexity and risk:** Low, marginally simpler in shape than D24 (no reversal
    anywhere in either the sign-mapping or, per item 3, the deity sequence), though this simplicity does
    not translate into a certification-relevant advantage since deity output is out of scope for both.
13. **JATAKA-scope basis under `ADR-0075`:** not needed, identical to D24 - literally named in
    `Q8_CLOSURE_MATRIX.md` s5.

### J.2 Direct comparison, methodology-first criteria (mirroring `DP-023`'s own filter)

| Axis | D24 | D40 | Differentiated? |
|---|---|---|---|
| Source clarity | High; verbatim BPHS verse citation located | High; consistent paraphrase across sources, no verbatim verse located | Marginal edge, D24 (stronger citation) |
| Sign-mapping dispute | None found | None found | Tied |
| Deity/payload tradition | Real, with an even-sign reversal in the deity sequence specifically | Real, no reversal anywhere | Marginal edge, D40 (simpler structure), but irrelevant to the certified D-sign scope (both excluded identically) |
| Computational rule complexity | Two-category, with a direction variable (though both categories are forward in the default method) | Two-category, no direction variable | Marginal edge, D40 (simpler) |
| Boundary/interval cleanliness | Exact representability, zero mismatches (measured) | Exact representability, zero mismatches (measured) | Tied |
| Dependencies | Tier-0 only | Tier-0 only | Tied |
| Freezable without `DP-024` | Yes, via disclosed non-claim | Yes, via disclosed non-claim | Tied |
| Oracle availability (source-confirmed, not executed) | Confirmed via `PyJHora` source read | Confirmed via `PyJHora` source read | Tied |
| Certification-template fit | Direct, six-times-proven | Direct, six-times-proven | Tied |
| JATAKA-scope basis | Literal `Q8_CLOSURE_MATRIX.md` s5 naming | Literal `Q8_CLOSURE_MATRIX.md` s5 naming | Tied |

### J.3 Conclusion: no selection can yet be justified between D24 and D40

**The evidence is genuinely tied.** The two marginal differences found this task (D24's stronger verbatim
source citation; D40's structurally simpler two-category rule with no reversal anywhere) point in opposite
directions and are each too narrow to serve as a real tiebreaker - neither affects certification
feasibility, dependency readiness, boundary cleanliness (both measured identically clean), or JATAKA-scope
eligibility, all of which are exactly equal. `docs/VARGA_CERTIFICATION_ROADMAP.md` section 5 itself groups
D24 and D40 together in its own risk order without ranking one above the other, and this task's own
deeper, independently-sourced investigation does not surface a reason to break that tie either. **Per the
owner's own explicit instruction not to manufacture a winner: this paper does not recommend D24 over D40
or D40 over D24.** If a choice is wanted despite the tie, it would have to rest on a basis this repository
does not currently evidence one way or the other (product-value preference, implementation-order
convenience, or simply the owner's own direction) - not on methodology, source authority, or certification
readiness, all four of which are equal.

**`DP-024` is not resolved, and was found unnecessary to resolve for either candidate** (J.1 item 7,
both): the newly-discovered deity-payload traditions for both D24 and D40 are real but excludable via the
same disclosed-non-claim scoping this project has already applied to every certified varga, D45 included.
No part of `DP-024`'s general architecture question needed to be answered to reach this conclusion, per
the owner's own explicit instruction.

### J.4 Explicit non-claims (this section)

Does not select D24 or D40. Does not create an ADR. Does not resolve `DP-024`. Does not claim `PyJHora`
execution or oracle agreement was performed - only that named, source-confirmed functions exist for both,
corroborating the frozen construction's own shape; genuine oracle comparison remains future certification-
execution work, in CI's own hash-pinned environment. Does not claim the BPHS citations retrieved this task
were checked against the original Sanskrit or a second independently-published English edition - both
remain translated-edition citations, consistent with this project's own standing disclosure discipline
(`ADR-0081` section 1's identical caveat for its own BPHS citation). Does not modify any production code,
certification artifact, or existing ADR. Does not treat `docs/VARGA_CERTIFICATION_ROADMAP.md` as ratified.

### J.5 Exact CEO decision required (this section)

1. Whether to select D24, D40, both (in either order), or neither, given the tied evidence (J.3) - this
   section does not recommend one over the other.
2. If a tiebreaker is wanted despite the tie, on what basis (this section identifies none the repository
   itself currently evidences).
3. Whether the newly-found deity-payload traditions for D24 and D40 (J.1 item 3, both) should be recorded
   anywhere before either capability's own ADR is drafted, or left for that ADR's own non-claims section,
   matching `ADR-0077`'s own precedent for D45.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.1.0 | 2026-09-01 | Section J added, per "CEO AUTHORIZATION — D24 vs D40 METHODOLOGY ADJUDICATION": a narrowly scoped comparative methodology study of D24 and D40 only, against the owner's own thirteen required items. Retrieved a verbatim BPHS verse citation for D24 (Sarga 6, Shlokas 2-23) and consistent-paraphrase corroboration for D40, both via external web research; read PyJHora's own published source code directly (not executed locally, per this host's already-disclosed degraded PyJHora environment) confirming named D24/D40 chart functions with an identifiable Traditional-Parasara default matching the frozen construction for both, with non-default variants excluded as non-claims mirroring ADR-0077's own D45 precedent; measured cell-width representability and floor-classification boundary behaviour for both via exact-rational (Fraction) arithmetic, finding both exactly representable with zero boundary mismatches - cleaner than D45's own measured result. Discovered a real classical deity/payload tradition for both D24 and D40, not previously flagged by docs/VARGA_CERTIFICATION_ROADMAP.md's own "No" payload-gap entries; found this does not create an unavoidable DP-024 dependency for either, since VargaClassification's own established scope already excludes deity output for every certified varga including D45 - a disclosed non-claim, not an avoided architecture question. Concludes the evidence between D24 and D40 is genuinely tied across every axis compared; does not manufacture a winner, per explicit instruction. Sections A-I unedited. No ADR drafted, no capability selected, no code implemented, DP-024 not resolved. |
| 1.0.0 | 2026-09-01 | Created. Re-evaluates the JATAKA candidate set now that D45, `KP_SIGNIFICATOR_V1`, and `PARASHARI_YOGA_V1` are each implemented and certified. Confirms D24/D40 remain unimplemented and, by the same methodology-first filter `DP-023` applied to select D45, are the only candidates simultaneously methodology-ready, dependency-clean, and free of any framework decision. Explicitly does not resolve `DP-024`'s deferred Varga step/payload architecture, and does not select another Varga merely by roadmap-ordering inertia - reasoning is re-derived from current repository evidence, not assumed carried over from `DP-023`. Newly scores two extension tracks not evaluable at `DP-023`'s time (KP significator extensions: Four Step Theory, Ruling Planets, horary; Parashari yoga extensions: further yoga families, bhanga/cancellation logic) against the owner's own ten required axes, finding both eligible in principle under `ADR-0075` but neither methodology-ready, each requiring its own dedicated readiness paper before selection. Recommends D24/D40 (co-equal, medium-high confidence) as the next capability if a Varga is wanted, with Vimshottari depth extension as a lower-value fallback. Options and a recommendation only; decides nothing; no capability selected, no ADR drafted, no code implemented. |
