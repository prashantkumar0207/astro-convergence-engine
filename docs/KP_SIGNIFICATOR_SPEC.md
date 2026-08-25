<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | DRAFT - NOT FROZEN. Research-and-drafting stage only, per "CEO DECISION — DP-028" items 3, 8-10. Structured per `ADR-0027` Decision 4's sixteen-item checklist. Several items cannot be frozen from evidence available to this session (see section 17) - this document identifies exactly which, and why, rather than silently choosing among disputed sources. |
| Version | 0.1.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-25 |
| Review cadence | TBD |

# KP_SIGNIFICATOR_V1 methodology specification (DRAFT)

## 0. Authorization and scope

Authorized by "CEO DECISION — DP-028," items 3-10: proceed with `KP_SIGNIFICATOR_V1` methodology-
specification drafting only, not implementation; freeze V1 around core K.S. Krishnamurti significator
methodology; explicitly exclude Four Step Theory, Ruling Planets, horary-specific extensions, and other
variants from V1; do not implement KP significators; do not begin Parashari yoga implementation;
independently verify every methodology claim against named authoritative sources during drafting and
identify disagreements/variants rather than silently choosing one; continue autonomously; stop only at a
genuine CEO decision point requiring ratification or a substantive methodological choice.

This document is **not** itself a decision paper (`DP-NNN`) - it is the specification artifact
`ADR-0027` Decision 4 requires, structured using that Decision's own sixteen-item checklist (now
`ADR-0027`'s own ratified, governing content, per its amendment/ratification this same task). It **does
not implement anything**. Sections 5 and 6 (four-step; ruling planets) are marked N/A per the owner's
explicit exclusion (item 5) rather than answered.

**Provenance discipline.** Every claim below is tagged **[EXTERNAL]** (secondary/tertiary web sources,
via `WebSearch`/`WebFetch` this task, none of them K.S. Krishnamurti's own primary Reader text - see
section 2) or **[REPOSITORY]** (this project's own already-certified/ratified material). No claim is
presented as settled merely because one source states it; section 17 lists every point where sources
disagreed, rather than resolving the disagreement silently, per explicit instruction (item 8).

## 1. Exact methodology (checklist item 1)

**[EXTERNAL], high confidence - the general architecture, well-converged across independent sources:**
KP significator determination for a house/cusp proceeds in two linked stages:

1. **Which planets signify a house at all** - a planet signifies a house if it is (a) the house's
   occupant, (b) the house's owner (lord of the sign on the cusp), (c) posited in the star (nakshatra) of
   the house's occupant, or (d) posited in the star of the house's owner. These four categories are
   consistently named across every source consulted, though their **relative strength ordering is
   disputed** - see section 17.1.
2. **Whether the house's matter is promised or denied** - governed by the house's **cuspal sub-lord**
   (the sub-lord of the exact cusp degree, using the same sign/star/sub hierarchy this project's own
   certified `KP_CHAIN_V1` already computes). The cuspal sub-lord is described across sources as the
   system's "deciding authority": if the cuspal sub-lord itself signifies (per stage 1's own significator
   test) a house or houses that support the matter under judgment, the matter is promised; if it
   signifies only houses that negate the matter, it is denied. The **exact positive/negative house
   groupings are matter-specific, not a single fixed rule, and are genuinely disputed across sources for
   any single matter** - see section 17.2.

## 2. Source authority (checklist item 2)

**[EXTERNAL].** K.S. Krishnamurti's own foundational works are the six-volume **"Krishnamurti Padhdhati
(KP) Reader"** series (Readers I-VI, published by the early 1970s). Reader I ("Casting the Horoscope")
was directly retrieved and inspected this task (`archive.org`, `docuri.com_6-kp-readers.pdf`) and
confirmed to cover foundational/introductory material only - it does **not** contain the significator
hierarchy or per-matter house tables. Reader III is consistently described across secondary sources as
the volume covering "Predictive Stellar Astrology," including significators, but **Reader III's own text
was not located or directly inspected this task** - every specific claim below therefore rests on
secondary or tertiary restatements, not the primary Reader itself.

The single most substantial, directly-quotable secondary source located is ***K.P. Dynamics* by Sri
Satyanarayana Naik**, retrieved in full (OCR'd text, `archive.org`). Independent secondary description
characterizes the author as "research-oriented," explicitly non-innovative ("does not deviate from the
original concept of the inventor, and does not introduce any new concepts"), and the book as
fundamentals-focused rather than a personal system - the strongest secondary-authority candidate found,
but still **not** K.S. Krishnamurti's own primary text, and its own claims are not independently
cross-checked against Reader III here.

**Determination: source authority is not yet resolved to primary-text confidence.** Section 17.3 states
exactly what would resolve it and the decision this requires.

## 3. Houses considered (checklist item 3)

**[REPOSITORY]/[EXTERNAL], well-converged.** All twelve houses/cusps are in scope generically - the
methodology (stage 1 significator test, stage 2 cuspal-sub-lord judgment) is house-agnostic in mechanism;
only the specific positive/negative house groupings differ per matter (section 17.2). V1 should implement
the **general mechanism** for any house, and, per the narrower-scoping principle this project has applied
repeatedly (`ADR-0027` Decision 3's own "never one vague feature," and `DP-023`'s own per-varga scoring
discipline), certify only a small, explicitly-named, well-evidenced set of **matters** at V1, not all
twelve houses' full traditional question sets at once. See section 17.4 for the recommended narrow V1
matter set.

## 4. Star, sub and sub-sub logic (checklist item 4)

**[REPOSITORY], high confidence, already built.** The star (nakshatra) lord, sub lord, and sub-sub lord
hierarchy `KP_SIGNIFICATOR_V1` needs is **already certified** by `KP_CHAIN_V1` (`docs/KP_CHAIN_SPEC.md`):
sign lord (SL), nakshatra lord (NL), sub lord (SB), sub-sub lord (SS), using the Vimshottari lord order
Ke-Ve-Su-Mo-Ma-Ra-Ju-Sa-Me and exact-rational interval arithmetic. `KP_SIGNIFICATOR_V1` should **consume
`KP_CHAIN_V1`'s own output as a read-only input** (per the system-isolation pattern - section 9), never
recompute or duplicate this hierarchy. This is the strongest-evidenced item in this specification: no
external disagreement was found on the SL/NL/SB/SS structure itself, and this project already has a
certified, zero-mismatch implementation of it.

## 5. Four-step interpretation if applicable (checklist item 5)

**N/A - explicitly excluded from V1**, per "CEO DECISION — DP-028" item 5. `DP-028` section F already
established, externally, that "Four Step Theory" is a separately-authored system (Sunil Gondhalekar,
~1990), not part of Krishnamurti's own original Readers, and is positioned in the literature as an
*alternative* to Ruling Planets rather than a dependency of core significator theory - reaffirmed here,
not re-researched. `KP_SIGNIFICATOR_V1` implements none of it. A future, separately-scoped item (its own
specification, its own ADR, its own certification, per `ADR-0027` Decision 3) would be required before
any four-step logic is implemented.

## 6. Ruling planets if included (checklist item 6)

**N/A - explicitly excluded from V1**, per "CEO DECISION — DP-028" item 5. `DP-028` section C/F already
established Ruling Planets' seven-factor (or, per one source found this task, five-factor - see section
17.5) construct is structurally tied to horary/judgment-time practice (requires the ascendant and Moon
position *at the moment of judgment*, not the natal chart alone), reaffirmed here. `KP_SIGNIFICATOR_V1`
implements none of it and does not compute or expose Ruling Planets. A future PRASHNA-phase capability is
the more natural home for it, per `DP-028`'s own scoping note - not decided here.

## 7. Cusp handling (checklist item 7)

**[REPOSITORY].** Cuspal sub-lord judgment (section 1, stage 2) requires house-cusp longitudes. This
project's cusps come from the FOUNDATION-tier house-cusp calculation, which `DP-025`
([[dp-025-polar-placidus-m04-tier0-maintenance]], still DEFERRED, not reopened by this document) already
found has an undefined-behaviour gap near/inside the true polar circle (~66.5633°N/S) and a provenance
mislabeling gap. Per `DP-028` section E's own determination, reaffirmed here: this dependency is real but
narrow - ordinary (non-polar) natal charts are unaffected, and `KP_SIGNIFICATOR_V1` can proceed without
`DP-025`'s resolution, provided it carries its own explicit non-claim (section 16) that cusp-derived
judgments are unverified for charts with cusps inside the undefined polar-latitude band, mirroring
`RISE_SET_V1`'s own polar non-claim. **[EXTERNAL]:** KP's own house system is consistently reported as
Placidus (unequal-house division) - consistent with this project's own current house-cusp implementation,
no disagreement found on this point.

## 8. Retrograde treatment (checklist item 8)

**[EXTERNAL] - genuinely disputed, not resolved.** Two materially different positions were found:

- Several tertiary/blog sources (synthesized, not directly quoted from a named book) describe retrograde
  as a **secondary, modulating** factor: "the question is not whether the planet is retrograde but what
  it signifies... retrograde status must be judged with caution and with support from the sub lord and
  ruling periods... never treated as an isolated yes-or-no rule." One source adds that "senior KP
  astrologers either remove retrograde RPs from the final verdict or use them to time when a delayed
  event will revive" - itself evidence of **practitioner-level disagreement**, not a single settled rule.
- *K.P. Dynamics* (the more substantial, directly-quoted secondary source, section 2), attributes a
  stronger claim directly to "Prof. KSK": **"a planet in retrogression will not give the result of its
  signification"** - i.e. retrograde as an active denial factor, not merely a modulating one. The same
  source's author flags two possible readings of even this one sentence (no manifestation at all, versus
  opposite/inverted manifestation) as unresolved.

**Determination: not resolved.** V1 cannot freeze a specific retrograde rule from this evidence alone.
Recorded as an explicit non-claim (section 16) and an open item (section 17.6).

## 9. Node treatment (checklist item 9)

**[EXTERNAL], reasonably converged with one open detail.** Multiple sources agree: Rahu and Ketu, having
no owned sign/house of their own in the Parashari sense, signify through a **substitution rule** - the
planet(s) conjunct them, the planet(s) aspecting them, and/or the sign lord of the sign they occupy, with
conjunction/aspect generally taking priority over the bare sign-lord fallback when both are absent. One
source states nodes are "strong in a house if no one is tenanting in their star" (i.e. their own strength
as a *star lord* for other planets depends on occupancy of their own nakshatra), which is a distinct
sub-rule from the substitution rule above, not a contradiction of it.

**[REPOSITORY] tension worth flagging, not yet resolved:** `KP_CHAIN_V1` already assigns Rahu and Ketu
their own SL/NL/SB/SS via the standard 9-lord Vimshottari nakshatra-lordship cycle (`Ke-Ve-Su-Mo-Ma-Ra-Ju-
Sa-Me`), i.e. nodes **do** have their own star/sub in this project's certified chain layer, in the
ordinary sense. Whether `KP_SIGNIFICATOR_V1` needs an *additional*, node-specific substitution rule on
top of consuming `KP_CHAIN_V1`'s own chain output as-is (section 4), or whether the certified chain
output already suffices without special-casing nodes, is genuinely unresolved from the evidence gathered
and is recorded as an open item (section 17.7).

## 10. Boundary behaviour (checklist item 10)

**[REPOSITORY], high confidence - directly inherited, no new question.** `KP_SIGNIFICATOR_V1` consumes
cusp and planetary SL/NL/SB/SS values from `KP_CHAIN_V1` (section 4), which already has a certified,
explicit, documented boundary convention (exact-rational `[start, end)` interval ownership, no float
promotion, per `docs/KP_CHAIN_SPEC.md` Decision KP-A) and a `nearest_boundary_arcsec` disclosure field on
every chain result. `KP_SIGNIFICATOR_V1` needs no new boundary convention of its own - it should surface
the same `nearest_boundary_arcsec` provenance on any significator judgment whose deciding chain value is
boundary-adjacent, mirroring the disclosure-field pattern used for `D45`/`DP-025`.

## 11. School and profile requirements (checklist item 11)

**[REPOSITORY], high confidence.** Per `docs/KP_CHAIN_SPEC.md` Decision KP-B, KP charts always use the
mean node and the ratified `KP_KRISHNAMURTI` profile; `kp_chart()` already asserts this and raises on a
true-node profile. `KP_SIGNIFICATOR_V1` should require the same profile assertion (never silently accept
a Parashari or other-school profile) and should be its own separately-identified, separately-hashed
module - never modifying `engine/kp/` or any certified Parashari file - per the isolation pattern already
established for every Varga/KP addition this project has made (section 9 below expands this).

## 12. Independent validation protocol (checklist item 12)

**[REPOSITORY], feasible, harder than `D45`'s own precedent.** `DP-028` section D already found PyJHora
has **no** dedicated significator-determination function - only a generic lordship-chain calculator. An
independent validator therefore cannot lean on a pre-built external oracle the way `D45`'s own
`validate_d45_holdout.py` could partially cross-check against PyJHora's `akshavedamsa_chart`; it must be
an independent, from-scratch re-derivation of whatever V1's own frozen rule turns out to be (mirroring
the *category* of work already done for `D45`'s own validator, but with no external corroboration point
of the specific kind PyJHora provided there). This raises the certification-difficulty bar for
`KP_SIGNIFICATOR_V1` relative to `D45`, consistent with `DP-028` section A/D's own oracle-availability
finding.

## 13. Protected holdout (checklist item 13)

**[REPOSITORY], mechanically identical in kind to existing precedent.** A prime-step deterministic
sampling holdout, independent of whatever boundary/dense-sweep cases are used for the main gate battery -
the same pattern as `D45`'s own gate G and `KP_CHAIN_V1`'s own holdout. No new mechanism needs inventing;
sizing and exact case selection are implementation-stage decisions, not specification-stage ones.

## 14. Negative controls (checklist item 14)

**[REPOSITORY], mechanically identical in kind to existing precedent.** Planted-mutation detection (e.g.
tampering with a positive/negative house-group table entry, a significator-priority rule, or a content
hash) confirmed genuinely detected - the same pattern as `D45`'s own gate H and `KP_CHAIN_V1`'s own
negative controls. No new mechanism needs inventing.

## 15. Acceptance criteria (checklist item 15)

**Not yet definable precisely** - acceptance criteria depend on which specific matter(s) and which
specific house-group table V1 actually freezes (section 17.2/17.4), which this document does not yet
resolve. In outline, mirroring `D45`'s own eight-gate pattern: table/rule integrity; a dense sweep or
full case enumeration for the frozen matter set; an independent-validator cross-check (section 12);
boundary-case coverage (section 10, inherited from `KP_CHAIN_V1`); a protected holdout (section 13);
genuine negative controls (section 14); zero categorical mismatch tolerance for significator/promise-deny
verdicts, matching `D-003`'s own zero-tolerance standard for the KP hierarchy generally.

## 16. Explicit non-claims (checklist item 16)

A future `KP_SIGNIFICATOR_V1`, when frozen, must state at minimum:
1. **Four Step Theory (Gondhalekar) is out of scope** - a distinct, separately-authored system, not
   implemented (section 5).
2. **Ruling Planets is out of scope** - a horary/judgment-time construct, not implemented, not computed
   (section 6).
3. **Horary/Prashna significator judgment generally is out of scope** (reaffirms `ADR-0027` Decision 3).
4. **Charts with cusps inside the undefined polar-latitude band are unverified/out of scope**, per
   `DP-025`'s own still-deferred gap (section 7).
5. **Retrograde treatment is not implemented in V1** unless/until section 17.6's disagreement is
   resolved by the owner - V1 should either omit retrograde-sensitive judgment entirely or disclose it as
   explicitly unverified, not silently pick one of the two conflicting rules found.
6. **Node (Rahu/Ketu) special-casing beyond `KP_CHAIN_V1`'s own certified chain output is not implemented
   in V1** unless/until section 17.7's open question is resolved.
7. **The specific house-matter(s) certified are limited to whatever narrow set the owner authorizes**
   (section 17.4) - V1 makes no claim to cover marriage, career, children, or any other matter not
   explicitly named in its own certification artifact.
8. **Source citations reflect secondary/tertiary material**, not K.S. Krishnamurti's own primary Reader
   III text, which was sought but not located/inspected this task (section 2) - this is disclosed on the
   chart/result itself, not only in this document.

## 17. Unresolved variants, disagreements, and the exact decision points

This section is the direct output of item 8's instruction ("independently verify every methodology claim
against named authoritative sources and identify disagreements/variants rather than silently choosing
one"). Nothing here is resolved by this document - each item names what was found and what resolving it
would require.

### 17.1 Significator strength order - three different orderings found

- **Ordering A** (converged across the largest number of independent tertiary sources - `kpastrologypro`,
  `kpastroapp`, `jagannathhora`, and directly confirmed by `WebFetch` of the AstroSage tutorial's own
  "Chapter 2: Fundamental Principles"): **star of occupant > occupant > star of owner > owner** (weakest).
  AstroSage's own text explicitly frames this as "grade A to E" and states "KP demotes the lord and
  promotes the planet sitting in the star of an occupant... a significant departure from traditional
  methods."
- **Ordering B** (from a WebSearch-synthesized description attributed to "the original 1965 volume,"
  not independently quote-verified this task): an *exception* to Ordering A applies when the occupant is
  in an enemy's sign or debilitated, or the lord is exalted/well-placed, in which case the owner's own
  star/sub outranks the occupant. This claim is the least directly verified of the three - it was not
  confirmed by direct fetch of a primary or clearly-dated source.
- **Ordering C** (*K.P. Dynamics*, directly quoted, but describing a related-but-distinct concept -
  **static cuspal dignity**, not "which planets signify an already-determined house"): "Sub Lord of a
  Cusp, Star Lord of a Cusp, Lord of the sign" as the *cusp's own* representing factors, with the
  occupant planet described separately as superseding all three as the *dynamic* activator. This may not
  actually conflict with Ordering A (it could be describing cusp-level dignity rather than house-level
  significator ranking), but the text was not clear enough this task to confirm they are the same
  concept under different names versus two genuinely different rules.

**Requires:** primary-source confirmation (Reader III) or an owner-designated single secondary authority
to adopt as V1's frozen rule, with the other orderings recorded as known variants, not implemented.

### 17.2 Positive/negative house groups per matter - genuinely question-granular, not a single list

The clearest, best-evidenced finding of this task. For "marriage" alone, sources gave **materially
different** negative/denial house groups depending on the *specific* question asked, not one settled
list for "marriage" as a whole:

| Specific question | Positive/promise houses | Negative/denial houses | Source |
|---|---|---|---|
| Marriage (normal) | 2, 7, 11 | (not separately listed) | *K.P. Dynamics*, "Interlinking Houses, Sub & Event" table |
| Success in love | 2, 5, 7, 11 | (not separately listed) | *K.P. Dynamics*, same table |
| Divorce | (not separately listed) | 6, 8, 12 | *K.P. Dynamics*, same table |
| Married life disturbed | (not separately listed) | 1, 6, 10 | *K.P. Dynamics*, same table |
| Marriage (general, tertiary sources) | 2, 7, 11 | 1, 6, 10 | multiple tertiary blogs (converged among themselves) |
| Marriage (general, other tertiary source) | 2, 7, 11 | 6, 8, 12 | `jagannathhora.com/mastering-sub-lord-theory` |

The positive group (2, 7, 11) is the single most consistent finding across every source - **high
confidence**. The negative group is genuinely disputed even **within a single source** (*K.P. Dynamics*
itself lists two different negative groups, 6/8/12 and 1/6/10, for two different *specific* questions
that most tertiary sources collapse into one "marriage" answer). This strongly suggests the tertiary
web-tutorial literature is simplifying/collapsing a methodology that is actually more granular
(per-specific-question, not per-house) in its own primary/near-primary form - exactly the kind of
distortion this project's own "never one vague feature" discipline (`ADR-0027` Decision 3) already
warns against, now found empirically to apply one level deeper than that Decision anticipated: even
within "marriage," multiple genuinely distinct questions exist and must not be silently collapsed into
one table.

**Requires:** an owner decision on which specific question(s) V1 actually certifies (see 17.4) and which
source's table governs it, before any table can be frozen.

### 17.3 Source authority - primary text not located

Reader III (the volume secondary sources consistently attribute significator theory to) was not located
or inspected this task; only Reader I (confirmed foundational-only) was directly retrieved. Every
specific claim in sections 1, 8, 9, and 17.1/17.2 rests on secondary or tertiary material.

**Requires an owner decision** among, at minimum: (a) authorize further, deeper search for Reader II/III
specifically (not guaranteed to succeed - it was not found despite a direct, targeted attempt this task);
(b) authorize treating *K.P. Dynamics* as V1's frozen secondary source of record, explicitly disclosed as
non-primary corroboration only - mirroring exactly how this project treated PyJHora for `D45`, never as
ultimate authority, always disclosed; (c) request the owner's own access to a primary Reader (a purchased
or otherwise legitimately obtained copy) if available; (d) narrow V1 enough that only the best-converged
material (section 4's chain hierarchy, the single well-converged 2/7/11 positive group) is used, deferring
everything genuinely disputed to a later, separately-scoped addition.

### 17.4 Recommended V1 matter scope (not decided here)

Given 17.1-17.3, the narrowest, best-evidenced possible V1 - offered as a recommendation, not a decision
- would certify **only**: the general significator-chain mechanism (section 1 stage 1, section 4,
already-certified substrate) plus **one** cuspal-sub-lord promise/deny judgment for **one** well-converged
question: "does the 7th cusp's sub-lord signify houses 2, 7, or 11" (promise) "versus not" (a binary
promise/no-promise judgment, deliberately avoiding the disputed negative-group question entirely by not
asserting a specific denial list). This is narrower than a full "marriage significators" feature and
avoids freezing anything in dispute. **Medium confidence** - the owner may prefer a different matter, or
may prefer resolving 17.1-17.3 first via a broader source-acquisition effort before committing to any
specific matter.

### 17.5 Ruling Planets composition (out of scope for V1, but worth recording as found)

Two different compositions were found for the excluded Ruling Planets construct: a seven-factor version
(day lord + ascendant sign/star/sub lord + Moon sign/star/sub lord, per `DP-028` section C.5) and a
five-factor version (ascendant star lord, ascendant sign lord, Moon star lord, Moon sign lord, day lord -
omitting the sub-lord level entirely, per this task's direct `WebFetch` of the AstroSage tutorial). Not
resolved, and not required to be resolved, since Ruling Planets is excluded from V1 (section 6) - recorded
here only so a future Ruling-Planets-scoped item does not have to re-discover this disagreement.

### 17.6 Retrograde treatment (see section 8) - open

Recorded fully in section 8; not repeated here. Requires an owner decision or further primary-source
verification before any retrograde-sensitive rule can be frozen.

### 17.7 Node (Rahu/Ketu) special-casing versus plain `KP_CHAIN_V1` consumption - open

Recorded fully in section 9; not repeated here. Requires either a determination that `KP_CHAIN_V1`'s
existing certified chain output suffices as-is, or a specification of exactly what additional
substitution logic V1 would need and why.

## 18. Status and the exact CEO decision(s) required to proceed

This specification is **not frozen** and `KP_SIGNIFICATOR_V1` **cannot yet be certified or implemented**.
Per item 10 of "CEO DECISION — DP-028," this is the genuine decision point this task's own research
produced - not because an option exists, but because the methodology-first rule this project has applied
throughout (most recently to exclude D20/D60/D16/D27/D4 from `D45`'s own selection in `DP-023`, precisely
for having undecided source/architecture questions) applies here with real force: sections 17.1-17.3 are
not implementation details, they are the exact methodology, and cannot be responsibly guessed.

**The decisions required, in the order they gate each other:**

1. **Source-authority strategy** (section 17.3): treat *K.P. Dynamics* as V1's frozen secondary source of
   record (disclosed as non-primary), authorize further search for Reader II/III specifically, pursue
   owner-side acquisition of a primary Reader, or narrow V1 to only the best-converged material and defer
   the rest.
2. **V1 matter scope** (section 17.4): which specific question(s) V1 actually certifies - this
   specification recommends the single narrowest option (7th-cusp marriage-promise judgment only, 2/7/11
   positive group only, no denial-group claim) at medium confidence, but does not decide it.
3. **Significator strength order** (section 17.1): which of the three orderings found (or another) governs
   V1, once 1 is resolved enough to check against.
4. **Retrograde and node treatment** (sections 17.6/17.7): freeze a specific rule, or explicitly omit
   retrograde/node-sensitive judgment from V1 entirely (the more conservative option, requiring no further
   resolution).

This document does not implement anything, does not ratify anything, and does not choose among these
options. It is ready for the owner's review and, on any combination of decisions above, can be revised
(as a new version, per this project's own append-and-revise discipline for specification documents) into
a frozen V1 ready for `ADR`-level ratification and certification-design work, mirroring the
`ADR-0076`/`ADR-0077` two-stage pattern already used for `D45`.

## Change history

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-08-25 | Created. Drafted per "CEO DECISION — DP-028" items 3-10, structured against `ADR-0027` Decision 4's sixteen-item checklist. External research (K.S. Krishnamurti's own Reader I directly inspected and confirmed foundational-only; Reader III sought but not located; *K.P. Dynamics* by Sri Satyanarayana Naik retrieved as the most substantial secondary source) independently verified against multiple sources per claim, surfacing genuine, evidenced disagreements rather than silently resolving them: three different significator-strength orderings (17.1); question-granular, source-disputed positive/negative house groups even within "marriage" alone (17.2); a retrograde-treatment tension between "modulating factor" and a direct KSK-attributed "denies its own result" claim (8); an open question on whether nodes need special-casing beyond `KP_CHAIN_V1`'s own certified chain output (9). Four Step Theory and Ruling Planets marked N/A, per explicit exclusion. Does not implement KP significators. Concludes NOT FROZEN - identifies four gated owner decisions (source-authority strategy, V1 matter scope, significator strength order, retrograde/node treatment) required before certification-design work can begin, mirroring the `D45` precedent's own methodology-first rule. |
