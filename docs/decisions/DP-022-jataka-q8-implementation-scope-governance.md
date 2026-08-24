<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents interpretations and evidence. DECIDES NOTHING. Requires owner approval. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-25 |
| Review cadence | TBD |

# DP-022. JATAKA/Q8 implementation-scope governance question: is `Q8_CLOSURE_MATRIX.md` s5's
implementation-scope row exhaustive or illustrative?

## 0. Authorization and scope

Authorized by the owner's explicit "CEO AUTHORIZATION — RESOLVE JATAKA/Q8 IMPLEMENTATION-SCOPE
GOVERNANCE QUESTION" instruction (2026-08-25), arising directly from `DP-021` sections H.1 and M.1
(`docs/decisions/DP-021-jataka-first-capability-decision-readiness.md`), which identified that none of
the four JATAKA-candidate capabilities discussed there - bhava/house-cusp gap-closure, karakas, Parashari
yogas, KP significators - appear in `Q8_CLOSURE_MATRIX.md` s5's own "Implementation scope" row, and that
this is the single most consequential unresolved item before any of those candidates is even eligible
for its own ADR. This paper investigates the interpretive question only. It does not select a JATAKA
capability, does not implement anything, does not amend `Q8_CLOSURE_MATRIX.md`, and does not ratify
itself.

**State audit performed before this investigation began:** branch `phase-g-governance`, local HEAD =
`06ff564ba1628e8f694e58d07cce1f60c7de6d12` (the `DP-021` commit), one commit ahead of
`origin/phase-g-governance` (`c4d571a340b4baf873fbefb5661eb195937d2f51`), not yet pushed. Working tree
clean of tracked changes. `origin/main` = `d738520ffc796d07468e24a5b1dddcfba3120c65` (the JATAKA-entry
merge, PR #4). Governance gates clean before this task began: 74 ADR entries (`ADR-0001`-`ADR-0074`), 21
registered DP identifiers. Last approved decision: `ADR-0074` (JATAKA entry, ratified 2026-08-24) and,
operationally, the PR #4 merge to `main`. Unresolved question this task addresses: `DP-021` section
M.1. `DP-022` registered in `docs/decisions/README.md` before drafting, per `ADR-0040` (22 DP identifiers
confirmed registered, governance gate clean, before this file was written).

## A. Exact governing text

`docs/Q8_CLOSURE_MATRIX.md` s5, JATAKA, quoted in full and unedited:

> | Field | Content |
> |---|---|
> | Prerequisites | FOUNDATION exit. |
> | Entry criteria | The Dasha roadmap's steps 1 to 6 complete: depth-3 gate, frozen dasha baseline,
>   profile allow-list, the H-08 convention decision, near-boundary Moon cases, boundary-proximity
>   indicator. |
> | **Implementation scope** | **Remaining production vargas in the roadmap's risk order. Vimshottari
>   depth and convention extensions if decided. Aspect coverage beyond full graha drishti if decided.
>   Planet strength if decided. Each is a separate ADR and none is implied by phase entry.** |
> | Certification gates | The per-varga template in `docs/NEW_VARGA_IMPLEMENTATION_TEMPLATE.md`. For
>   dashas, the requirements in `docs/DASHA_CERTIFICATION_ROADMAP.md` section 4. |
> | Exit criteria | Every capability declared a production analytical input is individually certified.
>   No capability is in use that a certification artifact does not cover. |
> | CEO approval | Entry, per capability, exit. A varga or dasha extension is never entered on the
>   strength of phase entry alone. |

The Implementation-scope sentence in full, parsed: four named work items ("Remaining production vargas
in the roadmap's risk order," "Vimshottari depth and convention extensions if decided," "Aspect coverage
beyond full graha drishti if decided," "Planet strength if decided"), followed by one governing sentence
attached to that list: **"Each is a separate ADR and none is implied by phase entry."**

Grammatically, "Each" has the four preceding items as its antecedent. The sentence states an
authorization *mechanism* for each of the four named items (its own ADR; not auto-authorized by phase
entry alone) - it does not, on its face, state whether items **outside** that list are eligible for the
same mechanism. This is the textual crux of the whole question: the sentence that governs *how* the
four listed items get authorized says nothing explicit about whether a fifth, unlisted item could be
authorized the same way.

For comparison, FOUNDATION's own s4 Implementation-scope row: "Rise and set with declared conventions.
Panchanga: tithi, vara, nakshatra as a panchanga element, yoga, karana. Rahu Kalam, Yamaganda, Gulika
with variant tables recorded. Civil-date rendering for dasha boundaries. Resolution of H-01 true-node
completeness and H-02 the ingress classification seam. Boundary-proximity indicators where sensitivity
warrants." No comparable "each is a separate ADR" sentence follows it, but FOUNDATION's own **exit
criteria** row states: "Every capability above at the level ADR-0017 defines as production certified."
- "above" refers to FOUNDATION's own implementation-scope list, and ties phase **exit** (not eligibility
for new work) to that list's completion.

## B. Evidence for each interpretation

**For EXHAUSTIVE:**
- FOUNDATION's exit criteria explicitly bind phase exit to "every capability **above**" (its own
  implementation-scope list) - textually treating that list as the complete, closed set of things the
  phase exists to build, at least for exit-gating purposes.
- `docs/Q8_CLOSURE_MATRIX.md` s1 states Q8 closure (`ADR-0048`) required, per phase, "prerequisites,
  entry criteria, **implementation scope**, certification gates, exit criteria, and CEO approval" - named
  as one of six required, specific fields established by `ADR-0021` D2. Requiring a specific,
  enumerated field suggests the field was meant to answer "what may this phase build," not merely
  gesture at examples.
- No document found anywhere in this repository states, for JATAKA specifically or for phase-scope rows
  generally, that these lists are non-exhaustive, provisional, or illustrative-only. Silence on
  extensibility, where extensibility is stated explicitly elsewhere in this repository's own governance
  writing when intended (see section C), is itself evidence.
- `ADR-0048` Decision 1: "**No word of its phase definitions (sections 3 through 14) is altered by this
  entry.**" The matrix was ratified *as written*, textually fixed at that moment - any reading that
  treats its lists as open runs against the spirit of a document whose own ratification emphasized
  exactness of wording.

**For ILLUSTRATIVE:**
- `Q8_CLOSURE_MATRIX.md` s1 itself: "This document **proposed** that matrix so the owner would have
  something concrete to amend or reject" - describing the matrix's own drafting purpose as something to
  be worked with and refined, not a permanently frozen enumeration, even though s1 also records it was
  ultimately "ratified... as written," with no amendment made at ratification time.
- `specs/PROJECT_CHARTER.md`'s own "Analytical systems" section (a higher governing document, per the
  `ADR-0042` hierarchy: OWNER -> PROJECT CONSTITUTION -> ENGINEERING CONSTITUTION -> DECISION LOG/ADR ->
  ... -> SPECIFICATIONS) names Parashari, Numerology, BNN, Nakshatra Nadi, KP with Four-Step refinement,
  and CIL as in-scope analytical systems, then states explicitly: **"Additional systems require their
  own specification and isolation rules."** This is direct, explicit textual precedent, in a document
  senior to `Q8_CLOSURE_MATRIX.md` in the ratified hierarchy, for the pattern "a named list plus an
  explicit path for adding to it via a fresh decision" - the opposite of a closed enumeration.
- `ADR-0021` D3 (ratified): "The entity vocabulary is **provisional and extensible**. Current kinds:
  Person, Organisation/Company, Geographic/National Entity, Event, Question. The ontology is
  deliberately **NOT frozen** at this stage. **A new entity kind requires an explicit architectural
  decision.**" This is the closest structural analogue found anywhere in this repository to "a named
  list, extensible via its own ADR, without rewriting the list's own source document" - though it
  concerns a different governance layer (an entity ontology, not a phase's implementation scope) and has
  never actually been exercised (no new entity kind has been added; EVIDENCE, where the entity vocabulary
  lives, has not begun per `Q8_CLOSURE_MATRIX.md` s6's own JATAKA-exit prerequisite).

## C. Precedent analysis

**No ADR has ever amended `Q8_CLOSURE_MATRIX.md`'s own substantive phase-definition text (sections
3-14).** Confirmed directly: the document's own Change History (s16) lists exactly two versions - 1.0.0
(drafted, `Status: PROPOSED`, 2026-08-11) and 1.1.0 (ratified as written, `ADR-0048`, 2026-08-17). No
version has ever touched sections 3-14. This is a genuine absence of precedent in either direction: no
capability has ever been added to a phase's scope beyond what was originally named, and no capability
has ever been formally excluded either - because, as the FOUNDATION and current JATAKA history below
shows, every capability actually pursued during FOUNDATION and (so far) JATAKA was already named in its
phase's own implementation-scope row at ratification time.

**FOUNDATION's own six implementation-scope items were all pre-named and none was added.** Rise/set,
panchanga elements, Rahu Kalam/Yamaganda/Gulika, civil-date rendering, H-01/H-02 resolution, and
boundary-proximity indicators were all named in `Q8_CLOSURE_MATRIX.md` s4 at ratification (2026-08-17,
before any of that work began). Every subsequent FOUNDATION-phase ADR (`ADR-0059`-`ADR-0061` and their
addenda for panchanga/trikalam, `ADR-0063` for civil-date rendering, `ADR-0064`-`ADR-0066` for H-02/H-01,
`ADR-0067` for boundary-proximity) mapped to one of those six named items. **No FOUNDATION-phase ADR
ever introduced a capability not already named in s4.**

**The Dasha roadmap's six steps were likewise all pre-named in JATAKA's own entry-criteria row before any
of the six was closed.** `Q8_CLOSURE_MATRIX.md` s5's entry-criteria text ("depth-3 gate, frozen dasha
baseline, profile allow-list, the H-08 convention decision, near-boundary Moon cases, boundary-proximity
indicator") already named all six at ratification (2026-08-17); `ADR-0053`, `ADR-0069`-`ADR-0073` each
closed one of those six pre-named items. This is the entry-criteria row, not the implementation-scope
row, but the same pattern holds: nothing was pursued that had not already been named in the ratified
text.

**The one directly relevant precedent for resolving genuine ambiguity in a Q8 phase-scope row is
`DP-015`/`ADR-0067`, and it is instructive on method, not on outcome.** `DP-015` investigated whether
`Q8_CLOSURE_MATRIX.md` s4's "explicitly deferred by decision" carve-out (textually attached only to
H-01/H-02 in FOUNDATION's exit-criteria sentence) extended to cover a different, unnamed treatment of
boundary-proximity indicators - a textually analogous question to this paper's own (does a Q8 phrase's
reach extend beyond its literal named scope?). The owner's ratified answer (`ADR-0067` Decision 2): the
carve-out's general reach is **"genuinely ambiguous"** - `DP-015` section 3's characterization (c) -
**resolved narrowly, for that one item only**, via an explicit, separately-ratified addendum ("Option 3
AMENDED"), and expressly **not generalized**: "It is not silently generalized to any other FOUNDATION
item... that question remains exactly as open as it was before this entry, for any future task to raise
explicitly if it becomes load-bearing." Two operational facts follow directly from this precedent: (1)
when this project has previously hit a genuine ambiguity of this shape, the owner's own practice was to
resolve it item-by-item, not with a single global ruling; and (2) the resolution mechanism used was a
fresh, explicit ADR/addendum **layered on top of** `Q8_CLOSURE_MATRIX.md`, without editing that
document's own sections 3-14 text - consistent with `ADR-0063`'s civil-date-rendering addendum, which
also left `Q8_CLOSURE_MATRIX.md` itself untouched.

**No formal "amendment procedure" for a ratified governance document is defined anywhere in this
repository.** Searched `docs/PROJECT_CONSTITUTION.md`, `docs/DOCUMENTATION_STANDARD.md`, and
`.claude/rules/governance.md` for "amend"/"amendment": no defined procedure exists. The only two
observed instances of a ratified Q8 phase-row's practical effect being adjusted (civil-date rendering,
boundary-proximity) both used the same *ad hoc but consistent* pattern: a decision paper, then an owner
ratification recorded as a *new*, separately-numbered ADR (or an addendum within an existing ADR's own
entry, per this repository's "change only what needs to change, append rather than rewrite" discipline)
- never a rewrite of `Q8_CLOSURE_MATRIX.md`'s own sections 3-14.

## D. Arguments for EXHAUSTIVE

1. FOUNDATION's exit criteria ("every capability **above**... production certified") textually treats
   its own implementation-scope list as the complete work-set gating exit - if JATAKA's list works the
   same way, JATAKA's own exit criterion ("Every capability declared a production analytical input is
   individually certified. No capability is in use that a certification artifact does not cover")
   plausibly reads the same way: the phase's job is to finish what s5 names, not to discover new work.
2. `ADR-0021` D2's requirement that every phase state an "implementation scope" as one of six specific,
   named governance fields implies the field was meant to bound the phase's own work, consistent with
   how `docs/VALIDATION_STANDARD.md`'s and this project's general anti-scope-creep discipline (cross-phase
   invariant, s14: "No phase may introduce a second convention for anything that already has one") treats
   phase boundaries as deliberate, not casual.
3. Reading it as illustrative risks converting a ratified, closed-form governance document into an
   open licence for any technically-plausible JATAKA-adjacent work to be proposed under the umbrella of
   "JATAKA is entered," which is exactly the "phase entry does not imply authorisation of every capability
   inside that phase" discipline `ADR-0048` Decision 4 was written to prevent - EXHAUSTIVE is the more
   conservative reading and errs toward requiring an explicit, visible governance act (a Q8 amendment)
   before scope grows, rather than trusting each individual ADR's own drafter (Claude) to correctly judge
   eligibility.

## E. Arguments for ILLUSTRATIVE

1. `specs/PROJECT_CHARTER.md`'s own, senior-in-hierarchy "Additional systems require their own
   specification and isolation rules" sentence directly names an ADR-level (not charter-amendment-level)
   path for scope growth at the *system* level - and JATAKA's implementation-scope row is arguably
   analogous in kind (a list of expected initial work, not a permanent ceiling), just at the
   *capability*, not system, level.
2. `ADR-0021` D3's entity-vocabulary pattern ("provisional and extensible... a new entity kind requires
   an explicit architectural decision") is the closest structural precedent in this repository's own
   governance writing for "named list, growable via its own ADR, without rewriting the source document" -
   and this project has shown, repeatedly (varga registry, DP-registration, ADR numbering), a general
   preference for additive, ADR-gated extensibility over rigid enumeration.
3. `Q8_CLOSURE_MATRIX.md` s1's own framing ("something concrete to amend or reject") and its emphasis
   throughout ("Each is a separate ADR and none is implied by phase entry," repeated near-verbatim for
   FOUNDATION) reads, in context, primarily as a warning against **auto-authorization from phase entry
   alone** - not as a warning against ever adding a fifth item. The sentence's actual work is "don't
   treat naming = building"; it is silent on additions, which under ordinary reading of governing text
   means it neither permits nor forbids them explicitly.
4. Treating the list as exhaustive would mean a capability like KP significators - explicitly in-scope
   at the PROJECT_CHARTER (system) level ("KP with Four-Step refinement") - could never be pursued during
   JATAKA at all without a formal Q8 amendment, even though PROJECT_CHARTER itself, a document senior to
   Q8, already contemplates it. This textual tension (a senior document naming a system Q8's own JATAKA
   row does not) is itself evidence the JATAKA row was not drafted with an intent to exhaustively
   foreclose everything charter-level work anticipates.

## F. Consequences of each interpretation

**If EXHAUSTIVE:** none of bhava/house-cusp gap-closure, karakas, Parashari yogas, or KP significators may
receive its own ADR under the current JATAKA authorization path until `Q8_CLOSURE_MATRIX.md` s5 is
itself amended by a fresh, explicit, owner-ratified decision (since no amendment procedure exists, this
would itself need to be a novel governance act, presumably following the pattern established by
`ADR-0048`'s own ratification-of-a-drafted-document precedent). Only the four named items (vargas,
Vimshottari extensions, aspect coverage, planet strength) remain eligible for their own ADR in the
interim. `DP-021`'s own "Track 1" options remain fully available without further governance work;
`DP-021`'s "Track 2" options are blocked until a Q8 amendment.

**If ILLUSTRATIVE:** any JATAKA-appropriate capability, including those `DP-021` investigated, may
receive its own ADR directly - provided that ADR itself explicitly confronts and states why the
capability is within JATAKA's own scope (mirroring the `DP-015`/`ADR-0067` precedent of resolving
ambiguity explicitly rather than silently assuming it), since even under this reading nothing is
self-authorizing and every capability still needs "its own separate ADR... none is implied by phase
entry." `DP-021`'s Track 1 and Track 2 options both become available without a separate Q8-amendment
step, subject to each capability's own ADR doing this interpretive work explicitly.

## G. Interaction with s15

`Q8_CLOSURE_MATRIX.md` s15's governing text: **"Q8 is CLOSED. No phase is thereby authorised - phase
authorisation remains a separate, per-phase, per-capability owner act."** This sentence is a floor, not
a ceiling, on either interpretation: it establishes that closing Q8 (ratifying the matrix) never
auto-authorizes anything, which both EXHAUSTIVE and ILLUSTRATIVE already respect (both require a further,
separate ADR before any capability is built). s15 does not itself speak to whether the *set of
capabilities eligible* for such a per-capability act is closed or open - it is silent on exactly the
question this paper investigates. No tension between s15 and either reading was found.

## H. Interaction with `ADR-0074`

`ADR-0074` (JATAKA entry, ratified 2026-08-24) audited and confirmed only the Dasha roadmap's six
*entry-criteria* items - it did not discuss, interpret, or rely on s5's *implementation-scope* row at
all (confirmed by direct re-reading; the entry's own item-by-item audit addresses only the entry-criteria
sentence, quoted in full in its Context section). `ADR-0074` therefore neither supports nor forecloses
either interpretation of the implementation-scope row - it is silent on this specific question, not a
data point for either side. `DP-021` (the paper that first surfaced this question) likewise reached no
conclusion on it, presenting it as section H.1/M.1's open item.

## I. Whether an amendment to Q8 is required

Depends entirely on which interpretation is ratified. If EXHAUSTIVE is confirmed, yes - some form of
explicit, owner-ratified change reaching `Q8_CLOSURE_MATRIX.md` s5's own scope (via a new governance act,
since no formal amendment procedure exists to reuse) would be a precondition for any of the four
non-listed candidates. If ILLUSTRATIVE is confirmed, no amendment to `Q8_CLOSURE_MATRIX.md` itself is
structurally required - consistent with the `DP-015`/`ADR-0063` precedent of resolving Q8-adjacent
ambiguity via a fresh ADR/addendum layered on top of the matrix, never by rewriting sections 3-14.

## J. Whether an ADR alone is sufficient

Under ILLUSTRATIVE: yes, provided the ADR does the interpretive work explicitly (states plainly that the
capability falls within JATAKA's scope and why), mirroring `ADR-0067`'s own explicit, non-silent
resolution of an analogous ambiguity - an ADR that simply proceeds to build a non-listed capability
without addressing this question at all would repeat exactly the "silent generalization" `ADR-0067`
Decision 2 explicitly declined to do, and should not be treated as having resolved it. Under EXHAUSTIVE:
no - an ADR proposing a non-listed capability would itself be the vehicle that also has to amend Q8's own
scope (a two-part decision, not one), since the capability is not eligible for authorization until the
scope question is settled first.

## K. Recommendation (NOT a decision)

**At medium confidence:** the evidence leans toward ILLUSTRATIVE, primarily on the strength of
`specs/PROJECT_CHARTER.md`'s own explicit "additional systems require their own specification and
isolation rules" language (a senior governing document already contemplating growth via ADR, not
amendment) and the `ADR-0021` D3 entity-vocabulary structural precedent, both of which show this
project's general governance instinct is toward additive, ADR-gated extensibility rather than closed
enumeration. This is tempered by two genuine counter-considerations that keep confidence at medium
rather than high: (1) JATAKA's own implementation-scope sentence, unlike the entity-vocabulary or charter
text, contains no explicit "provisional"/"extensible"/"additional X require Y" language of its own - its
silence could reflect either "this is closed" or "this simply wasn't addressed," and nothing in the
drafting history disambiguates which; (2) FOUNDATION's own exit criterion binding phase completion to
"every capability above" shows this project has, at least once, treated a phase's implementation-scope
list as the operative complete work-set for exit purposes, which cuts toward EXHAUSTIVE for symmetry.
Regardless of which interpretation is ratified, the `DP-015`/`ADR-0067` precedent is strong on **method**:
resolve this per-capability, explicitly, in each capability's own ADR (or in this paper's own
resolution, if the owner prefers a single global ruling) - not silently, and not by inferring
authorization from a capability's technical merit alone.

## L. Explicit non-claims

This paper does not decide whether `Q8_CLOSURE_MATRIX.md` s5's implementation-scope row is exhaustive or
illustrative. It does not amend `Q8_CLOSURE_MATRIX.md`. It does not select, implement, or certify any
JATAKA capability - not bhava, not polar Placidus, not KP significators, not Parashari yogas, not
Jaimini, not any varga, not planet strength. It does not modify H-03, the `ADR-0072` H10/H11
cross-certifier findings, or any closed Dasha/FOUNDATION item. It does not reopen `ADR-0074`, `ADR-0068`,
or any prior ratified entry. It does not treat `DP-021`'s own technical capability analysis as governance
authority, and it does not treat any external ("Claude Web") recommendation as authoritative on this
governance question - none was cited or relied upon in this paper. It does not claim the
`ADR-0021`/PROJECT_CHARTER precedents are directly on-point rather than analogous - both are presented
as the closest available structural precedent, explicitly flagged as being at a different governance
layer (entity ontology and product-system scope, not phase implementation-scope) and, in the entity-
vocabulary case, never yet actually exercised.

## M. Exact owner decision required

1. **The governing question itself:** is `Q8_CLOSURE_MATRIX.md` s5's "Implementation scope" row
   EXHAUSTIVE (only remaining vargas, Vimshottari extensions, aspect coverage, and planet strength may
   proceed through the existing JATAKA authorization path, until Q8 is amended) or ILLUSTRATIVE (other
   JATAKA-appropriate capabilities, named in this paper or `DP-021`, may receive their own ADR without a
   prior Q8 amendment)?
2. If EXHAUSTIVE: how should a Q8 amendment be enacted, given no formal amendment procedure currently
   exists (a fresh governance act to be defined, or an owner-specified process)?
3. If ILLUSTRATIVE: should this ruling be treated as a **general** interpretation of JATAKA's own s5 row
   going forward, or, matching the `ADR-0067` precedent's own explicit preference, should it instead be
   resolved **narrowly, per candidate capability**, each time one is proposed?
4. Whether to resume `DP-021`'s own capability-selection work now that this governance question has an
   evidence base (even if not yet ratified), or to wait for this paper's own ratification first.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-25 | Created. Investigates whether `Q8_CLOSURE_MATRIX.md` s5's implementation-scope row is exhaustive or illustrative, per the owner's explicit decision-readiness-only authorization arising from `DP-021` section H.1/M.1. Quotes the exact governing text; presents evidence and arguments for both EXHAUSTIVE and ILLUSTRATIVE; traces precedent (no ADR has ever amended `Q8_CLOSURE_MATRIX.md` sections 3-14; FOUNDATION's and the Dasha roadmap's own work items were all pre-named before being pursued; the one directly relevant precedent, `DP-015`/`ADR-0067`, resolved an analogous ambiguity narrowly, per-item, via a fresh ADR/addendum layered on top of Q8 rather than by rewriting it); analyzes interaction with s15 and `ADR-0074` (both found silent on this specific question); addresses whether a Q8 amendment or an ADR alone suffices under each reading; recommends ILLUSTRATIVE at medium confidence, primarily on `PROJECT_CHARTER.md`'s own "additional systems require their own specification" language and the `ADR-0021` D3 entity-vocabulary precedent, tempered by JATAKA's own scope sentence lacking equivalent explicit extensibility language and by FOUNDATION's exit criterion binding completion to its own full list. Decides nothing; does not amend Q8; no capability selected or implemented; no ADR drafted. |
