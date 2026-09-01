<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents options and a recommendation. DECIDES NOTHING. Requires owner approval. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-09-01 |
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

## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-09-01 | Created. Re-evaluates the JATAKA candidate set now that D45, `KP_SIGNIFICATOR_V1`, and `PARASHARI_YOGA_V1` are each implemented and certified. Confirms D24/D40 remain unimplemented and, by the same methodology-first filter `DP-023` applied to select D45, are the only candidates simultaneously methodology-ready, dependency-clean, and free of any framework decision. Explicitly does not resolve `DP-024`'s deferred Varga step/payload architecture, and does not select another Varga merely by roadmap-ordering inertia - reasoning is re-derived from current repository evidence, not assumed carried over from `DP-023`. Newly scores two extension tracks not evaluable at `DP-023`'s time (KP significator extensions: Four Step Theory, Ruling Planets, horary; Parashari yoga extensions: further yoga families, bhanga/cancellation logic) against the owner's own ten required axes, finding both eligible in principle under `ADR-0075` but neither methodology-ready, each requiring its own dedicated readiness paper before selection. Recommends D24/D40 (co-equal, medium-high confidence) as the next capability if a Varga is wanted, with Vimshottari depth extension as a lower-value fallback. Options and a recommendation only; decides nothing; no capability selected, no ADR drafted, no code implemented. |
