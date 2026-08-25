<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents an exact candidate, scoring, and a recommendation. DECIDES NOTHING. Requires owner approval. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-25 |
| Review cadence | TBD |

# DP-023. JATAKA first-capability decision: exact candidate selection

## 0. Authorization, scope, and relationship to `DP-021`

Authorized by the owner's explicit "CONTINUE — DP-021 FIRST JATAKA CAPABILITY DECISION" instruction
(2026-08-25), which found `DP-021` section N's "remaining production vargas" recommendation too coarse
and required: individual scoring of every remaining varga (not the family as a block), ten named scoring
axes, an exact varga pick with proof if varga remains first, resolution of the varga risk-order question
from repository evidence (or an explicit admission the repository does not settle it), and polar-
Placidus/M-04 kept architecturally separate from any varga capability. This paper does not contradict
`DP-021` - it deepens section N.2-N.5 with the finer-grained analysis the owner required. `DP-021`
sections A-N remain unedited; this is a new, separately registered paper (`DP-023`, registered before
drafting per `ADR-0040`), cross-referenced from `docs/decisions/README.md`'s own `DP-021` row.

**State audit performed before this investigation began:** branch `phase-g-governance`, local HEAD =
`728da717fed3d248a34f383db37b202bdb2fb048` (the `DP-021` section-N commit), four commits ahead of
`origin/phase-g-governance` (`c4d571a340b4baf873fbefb5661eb195937d2f51`), not yet pushed. Working tree
clean. `origin/main` = `d738520ffc796d07468e24a5b1dddcfba3120c65`. Governance gates clean before this
task began: 75 ADR entries, 22 registered DP identifiers (23 after this paper's own registration). Last
approved decision: `ADR-0075` (`DP-022`'s ILLUSTRATIVE ruling). Governing authorization for candidates
outside `Q8_CLOSURE_MATRIX.md` s5's literal list: `ADR-0075`, confirmed still in force, `Q8_CLOSURE_
MATRIX.md` itself still unedited (v1.1.0).

## A. Exact candidate inventory

| # | Candidate |
|---|---|
| 1-8 | Each remaining production varga individually: D4, D16, D20, D24, D27, D40, D45, D60 |
| 9 | Additional Parashari aspect coverage (fractional/sputa drishti; Rahu/Ketu's own aspects) |
| 10 | Vimshottari depth extension (depth 4+) |
| 11 | Shadbala (planet strength) |
| 12 | Polar-Placidus certification gap + M-04 provenance fix (kept explicitly separate - Tier-0/
    FOUNDATION-tier maintenance, not scored as a JATAKA capability candidate, per the owner's own
    instruction) |
| 13 | Parashari yoga/rule-combination evaluation |
| 14 | KP significators (`D-008`) |
| 15 | Jaimini Chara karakas |

## B. Evidence

**Vargas (candidates 1-8):** `docs/VARGA_CERTIFICATION_ROADMAP.md` (`Status: PROPOSED`, v1.0.0,
2026-08-11, never revised) is the authoritative in-repository source for construction, contract shape,
content confidence, and a recommended risk order. Quoted directly (section 4):

| Varga | Contract | Shape confidence | Content confidence | Payload/label gap (s3) |
|---|---|---|---|---|
| D4 Chaturthamsa | Segment (48 cells) or Cyclic with an undecided `step` field | High | High | No |
| D16 Shodashamsa | Cyclic | High | High | **Yes** - kalamsa deities |
| D20 Vimsamsa | Cyclic | High | **Medium - start triple genuinely disputed** | **Yes** - vimsamsa deities |
| D24 Siddhamsa | Cyclic | High | High | No |
| D27 Bhamsa | Cyclic | High | High (ULP-width note) | **Yes** - nakshatra lord |
| D40 Khavedamsa | Cyclic | High | High | No |
| D45 Akshavedamsa | Cyclic | High | High | No |
| D60 Shashtiamsa | Cyclic | High | **Medium - even-sign reversal genuinely disputed** | **Yes** - shashtiamsa deities |

Section 5's own recommended order (explicitly "a recommendation for owner decision, not a schedule"):
1. D60 (once the reversal question is decided); 2. D16 and D45 (share the movable/fixed/dual start
triple); 3. D24 and D40 (parity family); 4. D20 (only after its own disputed triple is adjudicated); 5.
D27 (ULP-sensitive width); 6. D4 (needs the segment-table-or-`step`-field decision).

**A stale-secondary-source finding, verified directly against `docs/DECISION_LOG.md`:** section 2 of the
roadmap states "Two framework defects... B-01... B-02... must be resolved before the next varga is
added." Both are in fact already resolved - `ADR-0049` (`Status: ACCEPTED`, 2026-08-17) remediated both;
confirmed live in current code (`engine/astrology/varga_registry.py::register_varga_rule` cross-checks
`rule.divisions`/`rule.division` against the registered division; `varga_rules.py` carries
`rule_content_sha256`). The roadmap document itself was never updated after 2026-08-11 and is stale on
this point - its own "must be resolved" framing no longer describes current reality; the underlying
recommended order (section 5) is unaffected by this staleness, since it does not depend on B-01/B-02.
Section 3's `step`-field and payload/label-table proposals remain undecided - confirmed directly: no
`step` field exists on `CyclicVargaRule` (`engine/astrology/varga_rules.py`), and no ADR addressing
either proposal was found in `docs/DECISION_LOG.md`.

**Aspect coverage (candidate 9):** `engine/parashari/drishti.py`'s own module docstring: "Scope decisions
(approved 2026-08-09): full aspects only, fractional sputa drishti deferred (AS-A); Rahu/Ketu cast NO
aspects in V1 (AS-B; the tradition variant... is recorded as a non-claim)." Both remain genuinely
undecided, not merely unimplemented.

**Vimshottari depth extension (candidate 10):** `vimshottari_from_moon()` raises `ValueError` for
`depth not in (1, 2, 3)`; the underlying `_subdivide()` recursion already generalizes (confirmed in
`DP-021` section A, item 12).

**Shadbala (candidate 11):** `engine/astrology/planet_strength.py::planet_strength()` raises
`NotImplementedError` by explicit design (`DP-021` section A, item 18, quoted in full there).

**Polar-Placidus/M-04 (candidate 12, scored separately, not as a JATAKA candidate):** `DP-021` section D
(15-part investigation) and section N.1 (M-04 re-verified live this session against `engine/models/
drishti.py` and `engine/parashari/drishti.py`) remain the evidence base; not re-derived here.

**Parashari yoga (candidate 13):** confirmed again this task - `grep -ri yoga` across `engine/**/*.py`
returns only the panchanga anga (`YOGA` as one of five panchanga elements, `engine/knowledge/models.py`
line 38) and provenance mentions of "no strengths, yogas, or judgments" in `engine/models/drishti.py`.
Zero combination-yoga-detection code exists anywhere. No document in this repository names a chosen
classical source or a candidate oracle for yoga verification.

**KP significators (candidate 14):** `docs/KP_CHAIN_SPEC.md` line 71's own non-claim and `D-008`'s
eleven-element checklist, both already cited in `DP-021` section A item 9 and C.5, re-confirmed unedited
this task.

**Jaimini Chara karakas (candidate 15) - a finding not surfaced in `DP-021`'s own original investigation:**
`specs/PROJECT_CHARTER.md`'s "Analytical systems" section, quoted in full: "Parashari, DOB-based
Pythagorean Numerology, R. G. Rao-style BNN, Umang Taneja-style Nakshatra Nadi, KP with Four-Step
refinement, and CIL when its exact framework is reproducibly specified. Additional systems require their
own specification and isolation rules." **Jaimini is not named in this list.** KP, unlike Jaimini, is
explicitly chartered. Pursuing any Jaimini-school code - including the technically narrow Chara-karaka
ranking - would invoke the charter's own "additional systems require their own specification and
isolation rules" clause, a governance step above and beyond `ADR-0075`'s own ILLUSTRATIVE ruling (which
concerns `Q8_CLOSURE_MATRIX.md` s5's JATAKA-internal implementation scope, not `PROJECT_CHARTER.md`'s
separate, senior-in-hierarchy analytical-systems list).

## C. Dependency graph

Vargas (candidates 1-8) depend only on the already-certified Tier-0 sidereal-longitude kernel - no
dependency on any other candidate in this inventory, and none on each other. Aspect coverage (9) extends
the already-certified `PARASHARI_DRISHTI_V1`. Vimshottari depth extension (10) extends the already-
certified `VIMSHOTTARI_V1`. Shadbala (11) depends on already-certified sign/house/aspect data as raw
input, but its own missing piece is the strength formula, not a data dependency. Polar-Placidus/M-04 (12)
extends the already-certified Tier-0 kernel; it is a genuine, evidenced prerequisite for KP significators
(14) specifically (`D-008`'s own "cusp handling" element) and for nothing else in this inventory.
Parashari yoga (13) depends on already-certified D1/aspects/vargas - zero missing calculation
dependency, entirely blocked on methodology. KP significators (14) depends on already-certified
`KP_CHAIN_V1` plus the still-open polar-Placidus gap (12) plus `D-008`'s own unwritten spec. Jaimini
Chara karakas (15) depends only on already-certified sidereal longitudes - the narrowest technical
footprint of any candidate - but is gated by `PROJECT_CHARTER.md`'s own system-scope clause (section B),
a dependency none of the other fourteen candidates carries.

## D. Scoring matrix (ten required axes)

Scale: **Ready/High** favorable, **Partial/Moderate** mixed, **Not ready/Low** unfavorable, stated
per-candidate rather than numerically, to avoid manufacturing false precision.

| Candidate | 1. Methodology readiness | 2. Source clarity | 3. Dependency readiness | 4. Implementation complexity | 5. Certification difficulty | 6. Regression/blast-radius risk | 7. Architectural leverage | 8. Product value | 9. Variant ambiguity | 10. Meaningful gate achievable |
|---|---|---|---|---|---|---|---|---|---|---|
| D4 | Ready, but contract undecided (Segment vs. `step`) | High | Ready | Moderate | Low (D3 precedent) | Low | Low | Moderate | Low (content); contract choice open | Yes |
| D16 | **Blocked** - payload/label decision undecided | High | Ready | Low | Moderate-High (payload) | Low | Low-moderate | Moderate-high | Payload undecided | Partial only |
| D20 | **Blocked** - start triple disputed | **Medium, disputed** | Ready | Low | High (disputed content + payload) | Low | Low | Moderate | High | No, not yet |
| D24 | Ready | High | Ready | Low | Low | Low | Low | Moderate | None flagged | Yes |
| D27 | Ready, but payload undecided + ULP-width | High | Ready | Moderate | Moderate (ULP, D7/D9-precedented) | Low | Low | Moderate | Payload undecided | Partial only |
| D40 | Ready | High | Ready | Low | Low | Low | Low | Moderate-low | None flagged | Yes |
| D45 | **Ready, no gap** | High | Ready | Low | Low | Low | Low | Moderate | None flagged | **Yes, cleanly** |
| D60 | **Blocked** - reversal disputed | **Medium, disputed** | Ready | Low | Moderate (disputed content + payload) | Low | Low | Moderate | High | No, not yet |
| Aspect coverage | Partial - AS-A/AS-B undecided | Moderate, multiple traditions | Ready | Moderate | Moderate-High | Low-moderate | Moderate | Moderate | **High** (fractional table choice + Rahu/Ketu question) | Uncertain |
| Vimshottari depth | Ready | High (identical to depths 1-3) | Ready | Very low | Low | Low (but reopens a just-closed area) | None | Low | None | Yes |
| Shadbala | **Not ready** | Low-moderate | Ready as input only | High | High | Low | Moderate (long-term) | High (long-term) | **High** | No |
| Parashari yoga | **Not ready** | **Low**, fragmented sources | Ready | High | High, oracle unconfirmed | Low technically, high reputationally | High | **Highest** | **Highest** | Uncertain |
| KP significators | **Not ready**, `D-008` unwritten | Moderate-high once sourced (single founding authority) | Substantially ready | High | High | Low technically, visible | **High**, chartered | High | High | Plausible once sourced (`KP_CHAIN_V1` precedent) |
| Jaimini karakas | Not ready in-repo; core rule comparatively settled | Moderate-high for the rule; **charter-scope gap** | Ready, narrowest footprint | Low | Unknown - no Jaimini precedent exists | Low technically, high strategically (new system) | Low for JATAKA | Low-moderate | Moderate (7 vs. 8 karaka scheme, ties) | Unknown |

## E. Exact first-capability candidate, and why it precedes the alternatives

**D45 (Akshavedamsa)** is the recommended first JATAKA capability.

**Why it precedes the other seven vargas, by repository evidence alone:** applying the owner's own
methodology-first rule (section 0) as an explicit filter first eliminates D20 and D60 - both have a
content confidence the roadmap's own table calls "Medium... genuinely disputed" (D20's start triple; D60's
even-sign reversal), which is precisely a lack of frozen, authoritative methodology. Of the remaining six,
D16, D20 (already excluded), D27 and D60 (already excluded) are named in `docs/VARGA_CERTIFICATION_
ROADMAP.md` section 3 as needing an undecided payload/label-table architecture decision before entering
production as "the astrological point of the division" (its deity payload) would otherwise be
uncomputed and uncertified - leaving D16 and D27 also not cleanly ready. D4 needs its own undecided
contract choice (Segment table vs. the proposed `step` field) before implementation, a smaller but still
real open decision. That leaves **D24, D40, and D45** as the only three of the eight with no disputed
content and no undecided architecture prerequisite. Among these three, the roadmap's own section 5 risk
order places D45 in its second tier (alongside D16, which is excluded here on the payload ground) and
D24/D40 in its third tier - **making D45 the highest-ranked cleanly-ready varga by the repository's own
stated risk order**, once the owner's own methodology-first filter is applied to that order rather than
taking it at face value.

**A limit on this proof, stated honestly:** the roadmap's own text groups D16 and D45 together ("sharing
the movable/fixed/dual start triple") without independently ranking D45 above D16 - the separation
found here (D45 clean, D16 payload-blocked) comes from cross-referencing section 5's ranking against
section 3's separately-stated payload-gap list, not from an explicit statement in section 5 itself that
D45 precedes D16. This paper's own reasoning bridges those two sections; the roadmap document itself
never states the conclusion directly. This is disclosed rather than presented as a verbatim citation.

**A technical note beyond the roadmap's own text, disclosed rather than acted on:** D45's cell width
(30/45 = 2/3 degree) is not exactly binary-representable, arithmetically similar in kind to D27's already-
flagged width concern and to the already-solved D7/D9 precedent - but `docs/VARGA_CERTIFICATION_
ROADMAP.md` section 4 does not flag D45 with the "Width note" it gives D27 explicitly. This paper does
not resolve whether that omission is deliberate (D45's specific sweep/holdout points may not land near a
boundary in practice) or an oversight; it is flagged as something the eventual certification work should
verify, consistent with `docs/VALIDATION_STANDARD.md`'s own rule against assuming a gate would pass
without checking - not treated as a blocker at the decision-readiness stage, since D7 and D9 already
demonstrate this class of issue is solvable within the existing template.

**Why D45 precedes the non-varga candidates:** every non-varga JATAKA-scope candidate in this inventory
(aspect coverage, Shadbala, Parashari yoga, KP significators) fails the owner's own methodology-first
rule outright - each lacks a frozen, authoritative, chosen methodology in this repository today.
Vimshottari depth extension passes the methodology-first rule as cleanly as D45 does, but scores lower
on architectural leverage and product value (section D) and reopens dasha work this session only just
finished formally closing (`ADR-0053`, `ADR-0069`-`ADR-0073`) - a scope-creep-optics consideration the
owner may weigh differently, noted rather than resolved here.

## F. Alternatives, ranked

1. **D24 or D40** - co-equal, both cleanly ready by the same methodology-first filter, ranked one tier
   below D45 in the roadmap's own risk order; either is a defensible substitute if the owner weighs
   product familiarity differently (not itself repository-evidenced either way - see section H's own
   caution against inventing a product-value tiebreaker).
2. **Vimshottari depth extension** - equally methodology-clean, lower architectural leverage and product
   value, reopens a just-closed area.
3. **Parallel, not competing: polar-Placidus + M-04 closure** - kept explicitly separate from any varga
   choice per the owner's own instruction; recommended as worth doing regardless, framed as Tier-0/
   FOUNDATION-tier maintenance, not a JATAKA capability itself.
4. **Parallel, not competing: authorize a dedicated `D-008` methodology-specification decision-readiness
   paper** - the correct next step for the single highest-architectural-leverage, chartered candidate
   (KP significators) found in this inventory, not implementation.
5. **Not recommended for near-term selection:** D4 (contract choice first), D16/D27 (payload-table
   decision first), D20/D60 (disputed content), aspect coverage (AS-A/AS-B undecided), Shadbala
   (highest-risk candidate in the entire inventory), Parashari yoga (highest product value but least
   methodology-ready), Jaimini karakas (charter-scope gap, section B).

## G. Risks

Selecting D45 (or D24/D40) carries the lowest risk profile in this inventory: no disputed content, no
undecided architecture prerequisite, a five-times-proven certification template, and a narrow, additive
blast radius (registry-gated, per `ADR-0049`'s own B-01/B-02 remediation). The main residual risk is the
unflagged width-representability question (section E) and the still-undefined varga "risk order" as an
owner-ratified document (the roadmap itself remains `Status: PROPOSED`, never ratified - this paper's own
reasoning about it is not itself a ratification). Selecting Shadbala, Parashari yoga, or KP significators
without first resolving their own methodology carries the highest risk in this inventory: each would
either require inventing methodology under time pressure (the "manufactured confidence" failure mode
this project's own governance culture is built to prevent) or produce a certification gate that cannot
meaningfully fail, both explicitly prohibited by `.claude/rules/certification.md`.

## H. Certification plan (for D45, if selected)

Per `docs/NEW_VARGA_IMPLEMENTATION_TEMPLATE.md`'s own already-proven checklist (Steps 0-5, used
successfully for D2/D3/D7/D9/D10/D12/D30) and `docs/VARGA_CERTIFICATION_ROADMAP.md` section 6's explicit
requirements list: its own ADR first, naming the classical source (Parashara/BPHS, per section 4's own
citation) and the `parashara` school key; a frozen `CyclicVargaRule` table for D45 (movable Aries/fixed
Leo/dual Sagittarius start, forward direction) verified cell-by-cell against a second independent
transcription and a re-derivation from the classical statement; an independent reference implementation
built by a different construction; a dense sweep; a full ULP boundary battery (explicitly checking the
2/3-degree-width question flagged in section E); an external oracle comparison (PyJHora, already
exercised successfully for D2/D3/D7/D12/D30) with zero categorical tolerance; a protected holdout; a
regeneration runner; a collected artifact gate; provenance; and a certification artifact -
`VARGA_D45_V1_certification.json`, mirroring the existing five artifacts' own shape. A genuine negative
control (a deliberately mutated cell, confirmed to break the gate, confirmed restored) per this session's
own established discipline.

## I. Methodology/source requirements

**For D45 specifically: already satisfied.** Construction (Parashara/BPHS), start-sign triple
(movable/fixed/dual, undisputed per section B), and direction (forward) are all stated in `docs/VARGA_
CERTIFICATION_ROADMAP.md` section 4 with no flagged dispute. No new methodology decision is required
before certification work could begin - only the ordinary implementation/certification sequence itself.

**For every other JATAKA-scope candidate found not methodology-ready in this inventory:** D16/D27 need
the section-3 payload/label-table architecture decision (a project-wide decision, not specific to any one
division); D20/D60 need their own disputed-content adjudication; D4 needs the Segment-vs-`step` contract
choice; aspect coverage needs AS-A/AS-B resolved (fractional-drishti source, Rahu/Ketu aspect-casting);
Shadbala needs a chosen sub-component methodology across all six classical strength types; Parashari yoga
needs a chosen classical source and explicit yoga-by-yoga qualifying/cancellation rules; KP significators
needs `D-008`'s own eleven-element spec; Jaimini karakas needs a from-scratch Jaimini specification plus,
per section B, confirmation the system is even chartered.

## J. Explicit non-claims

This paper does not select D45 or any capability - that remains the owner's act. It does not draft or
authorize a `step`-field or payload/label-table decision for the varga framework generally, though it
identifies both as prerequisites for D16/D27/D4 specifically. It does not resolve D20's or D60's own
disputed content. It does not resolve AS-A/AS-B. It does not draft `D-008`. It does not draft a Parashari
yoga specification. It does not determine whether Jaimini is or should become a chartered system - it
only observes, from `specs/PROJECT_CHARTER.md`'s own current text, that it is not chartered today. It does
not claim `docs/VARGA_CERTIFICATION_ROADMAP.md` section 5's own risk order is ratified - it remains
`Status: PROPOSED`, and this paper's own D45-precedes-D16 reasoning (section E) is this paper's own
inference from that unratified document, not a verbatim citation of an already-stated conclusion. It does
not resolve the D45 width-representability question raised in section E - it flags it for the eventual
certification work. It does not implement anything, modify any production code, modify any certified
artifact, begin polar-Placidus work, begin M-04 remediation, begin KP significators, begin Parashari yoga
implementation, begin Jaimini/BNN/Numerology work, or reopen FOUNDATION or any closed Dasha item.

## K. Recommendation and confidence

**Recommend D45 (Akshavedamsa) as the exact first JATAKA capability, at medium-high confidence** - higher
than `DP-021` section N.3's own "remaining vargas" recommendation, because the candidate is now named
specifically and the elimination reasoning (section E) is directly traceable to repository evidence
rather than a general template-proven-ness argument. Confidence is not "high" rather than "medium-high"
because of two disclosed limits: the roadmap's own D45-above-D16 ranking is this paper's own inference,
not a verbatim citation (section E), and the width-representability question (section E) has not been
independently verified. **In parallel, not in competition:** recommend authorizing polar-Placidus/M-04
closure as Tier-0 maintenance, and a dedicated `D-008` methodology-specification decision-readiness paper
as the correct next step toward the single highest-leverage, chartered, not-yet-ready candidate found in
this inventory (KP significators) - neither is "the first JATAKA capability," both are worth starting in
parallel if the owner wants to invest in the higher-value track sooner rather than later.

## L. Exact CEO decision required

1. **Select the first JATAKA capability**: D45 (recommended), D24, D40, Vimshottari depth extension, or
   direct otherwise.
2. If a varga is selected: authorize its own ADR (naming the classical source and school, per section H),
   and separately confirm whether the varga-framework's own `step`-field and payload/label-table
   questions (section I) should be decided now (benefiting D4/D16/D27 later) or deferred until one of
   those three is actually proposed.
3. Whether to authorize polar-Placidus + M-04 closure now, in parallel, as Tier-0/FOUNDATION-tier
   maintenance (kept explicitly separate from the JATAKA-capability decision, per instruction).
4. Whether to authorize a dedicated `D-008` KP-significator methodology-specification decision-readiness
   paper as a parallel track.
5. Whether a comparable methodology-specification decision-readiness paper should also be authorized for
   Parashari yoga.
6. Whether to treat `docs/VARGA_CERTIFICATION_ROADMAP.md` itself as worth formally ratifying (it remains
   `Status: PROPOSED` throughout this analysis), separate from any single capability decision.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-25 | Created, continuing/deepening `DP-021` section N per the owner's explicit "do not simply repeat 'remaining Vargas'" instruction. Scores all fifteen candidates (eight vargas individually, aspect coverage, Vimshottari depth extension, Shadbala, Parashari yoga, KP significators, Jaimini karakas; polar-Placidus/M-04 kept explicitly separate) against ten required axes. Resolves the varga risk-order question from repository evidence (`docs/VARGA_CERTIFICATION_ROADMAP.md`), applying the owner's own methodology-first rule as an explicit filter to exclude D20/D60 (disputed content) and D16/D27 (undecided payload architecture) and D4 (undecided contract choice), isolating D24/D40/D45 as the only cleanly-ready vargas and naming D45 as the highest-ranked of the three by the roadmap's own (unratified) risk order, with the D45-precedes-D16 inference disclosed as this paper's own reasoning rather than a verbatim citation. Flags a stale claim in `docs/VARGA_CERTIFICATION_ROADMAP.md` itself (B-01/B-02 already resolved by `ADR-0049`, contrary to the roadmap's own unrevised text) and a new finding not surfaced by `DP-021` (Jaimini is not named in `specs/PROJECT_CHARTER.md`'s own analytical-systems list, unlike KP). Recommends D45 at medium-high confidence, with polar-Placidus/M-04 closure and a `D-008` methodology-specification paper recommended in parallel, not in competition. Presents six exact owner decisions required. Decides nothing; no capability selected or implemented; no ADR drafted. |
