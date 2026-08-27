<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | DRAFT - NOT FROZEN, but substantially resolved via direct primary-source retrieval (section 19), per "CEO AUTHORIZATION — CONTINUE KP METHODOLOGY EVIDENCE RESOLUTION." Structured per `ADR-0027` Decision 4's sixteen-item checklist. Section 17's v0.1.0 disagreements are superseded by section 19 for the specific matter/question section 19 resolves; genuinely residual items are named in section 18. |
| Version | 0.2.1 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-28 (section 19.4's residual caveat updated with a pointer to `DP-030` section 11: Reader IV directly re-read, corroborating the same rule in a general, non-horary chapter; the horary-to-natal caveat itself is preserved, not resolved) |
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

**v0.2.0 continuation.** Authorized by "CEO AUTHORIZATION — CONTINUE KP METHODOLOGY EVIDENCE
RESOLUTION": continue from `fb4b2c6` (v0.1.0); do not implement; do not arbitrarily select among the
v0.1.0 disagreements; continue targeted primary-source research, especially Reader II and Reader III;
construct a source/claim matrix; determine whether the disagreements can be resolved from authoritative
evidence; if resolvable, update the specification with explicit provenance and variant boundaries and
stop at the genuine ratification point; if not, document the irreducible variants and recommend the
narrowest defensible V1 or deferral; do not switch to Parashari yoga merely because KP research is
difficult - only recommend switching if the evidence establishes KP cannot responsibly be frozen while
Parashari yoga is sufficiently ready; no production code, no certification execution, no push/merge.
Section 19 records what this continuation found: **direct, primary K.S. Krishnamurti Reader text was
located, retrieved, and read this task** (not merely secondary/tertiary restatement), resolving most of
v0.1.0's open disagreements with genuine textual evidence. This determination is stated plainly: **the
evidence establishes KP significators CAN responsibly be frozen for a narrow V1** - the instruction's own
condition for recommending a switch to Parashari yoga is therefore **not met**, and no such switch is
recommended.

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

**Determination (v0.1.0): not resolved.** V1 cannot freeze a specific retrograde rule from this evidence
alone. Recorded as an explicit non-claim (section 16) and an open item (section 17.6).

**Superseded by section 19.2 (v0.2.0).** Direct retrieval of K.S. Krishnamurti's own Reader III text
resolved this with a primary-source rule more precise than either v0.1.0 position: retrograde does not
flatly deny, nor merely "modulate" - it makes a promised result **conditional and reversible until the
planet stations direct**. See section 19.2 for the verbatim quotes and the resulting V1 rule.

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

**Superseded by section 19.3 (v0.2.0).** Direct retrieval of K.S. Krishnamurti's own Reader III text
resolved this: **yes, node-specific substitution logic is needed**, with an explicit, repeatedly-stated
primary-source priority order (conjoined planet, then aspecting planet, then sign lord), on top of - not
instead of - `KP_CHAIN_V1`'s own existing star/sub assignment. See section 19.3 for the verbatim quotes.

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

## 17. Unresolved variants, disagreements, and the exact decision points (v0.1.0 - see section 19 for resolution)

This section is the direct output of item 8's instruction ("independently verify every methodology claim
against named authoritative sources and identify disagreements/variants rather than silently choosing
one"). It is preserved unedited as the v0.1.0 record of what secondary/tertiary sources alone could
establish. **Section 19 (v0.2.0) supersedes 17.1, 17.2, and most of 17.3-17.4 with direct primary-source
findings** - each subsection below now carries a pointer to where it was resolved.

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

**RESOLVED - see section 19.1.** Reader III text, retrieved directly, confirms Ordering A explicitly and
repeatedly, in its own words, across at least six independent passages in different topical contexts.

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

**RESOLVED for one specific question - see section 19.4.** Reader III's own horary chapter gives an
explicit, primary-source cuspal-sub-lord house list for "will marriage happen with this specific party":
positive 2, 7, 11 (with Krishnamurti's own stated classical rationale); negative 1, 6, 10, 12 (with a
rich, explicit per-additional-house elaboration of *why*, not merely *whether*). The question-granularity
finding itself is also directly confirmed: Reader III has genuinely distinct rule structures for "is
marriage promised" versus "marriage promised but late" versus this horary question - three different
chapters, three different rule shapes, not one collapsed list. The children/5th-house parallel remains
unresolved - see section 19.5.

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

**LARGELY RESOLVED - see section 19.0.** Reader II, Reader III, and Reader IV (K.S. Krishnamurti's own
volumes, option (a) above) were located and directly retrieved this task via a persistent, targeted
search that the v0.1.0 attempt did not exhaust. Residual caveat: retrieval was of scanned/OCR'd reprints,
not a critical edition - section 19.0 discloses this precisely rather than claiming perfect fidelity.

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

**SUPERSEDED - see section 19.6.** With 17.1-17.3 now resolved for the horary marriage-promise question,
the recommended V1 scope is upgraded from a bare promise/no-promise binary (no denial-group claim) to the
full, primary-source-confirmed promise/deny judgment (2/7/11 positive, 1/6/10/12 negative), at
correspondingly higher confidence.

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

## 19. Primary-source resolution (2026-08-25, this continuation task)

Per "CEO AUTHORIZATION — CONTINUE KP METHODOLOGY EVIDENCE RESOLUTION": continued, persistent, targeted
search located and directly retrieved K.S. Krishnamurti's own Reader II, Reader III, and Reader IV -
genuine primary text, not secondary restatement. This section is the source/claim matrix and resolution
the instruction required, with every claim tagged **[PRIMARY]** (K.S. Krishnamurti's own Reader text,
this task) or carried forward from v0.1.0 as **[EXTERNAL]**/**[REPOSITORY]**.

### 19.0 Retrieval provenance and its own limits

Located via `archive.org` item `kp-readers` (a six-Reader collection, `Prof. K.S. Krishnamurti` credited
directly) and the standalone item `kpreader-4-marriage-married-life-children`. Reader III
("Predictive Stellar Astrology") and, separately, a partial excerpt of Reader IV ("Marriage, Married Life
& Children") were extracted to plain text locally (`pdftotext`, since no OCR/rendering tool was available
to re-derive text from an image-only PDF) and searched directly for the disputed claims.

**Disclosed limits, precisely, not glossed over:**
- These are **scanned/OCR'd reprints**, not a critical edition - visible OCR artifacts exist (e.g.
  running-header mis-scans like "KRISHNAMURTI PADHDHATI" rendered variously, and at least one digit-level
  corruption, "0112" for "or 12," corrected here by context and cross-reference within the same
  paragraph, not assumed).
- The `kp-readers` collection's own copy of Reader IV (a different scan than the standalone item) had a
  corrupted custom font encoding that made its text non-recoverable by any tool available this task; the
  standalone item's own `_text.pdf` variant extracted cleanly but is itself only a partial excerpt
  (roughly pages 186-200 of the book, two worked examples, not the full text) - the specific
  positive/negative house list for marriage was **not** found in that Reader IV excerpt; it was found
  instead in Reader III's own horary chapter (section 19.4), which independently addresses the same
  question.
- No independent second reader verified these OCR transcriptions - this document's own reading of them is
  itself a single-pass transcription, the same caution this project applies to every other single-source
  claim.

These are primary-source retrievals of real evidentiary weight, well above v0.1.0's secondary/tertiary
material - but they are not a publisher-verified critical edition, and that distinction is preserved
rather than erased.

### 19.1 Significator strength order - RESOLVED (Ordering A confirmed)

Reader III states this explicitly and repeatedly, in different topical contexts, with no contrary passage
found anywhere in the retrieved text:

- "Planets in the constellation of the occupants of these houses are very strong to give the matters of
  these houses" (general house-matter chapter).
- "Occupants or owners do not offer the results of the houses but they offer the results of the lord of
  the Constellation in which they are deposited" - i.e. the star lord is the operative mechanism, not bare
  occupancy/ownership.
- "Planets occupying or owning the house are weaker in strength than the planets in the constellation of
  the occupants and owner" (health/disease chapter) - a direct, unambiguous ranking statement.
- "The planets, in the constellation of the occupants of the Bhadhakasthana, are the stronger evils: next,
  the occupants of Bhadhakasthana; next those in the constellation of the lords of the Bhadhakasthana, and
  lastly the lords of these evil houses" (longevity chapter) - a complete, explicit four-level ranking,
  strongest to weakest.
- "Planets posited in the constellation of the occupants in the houses 2, 6, 10 or 11 are the strongest to
  give wealth" (finance chapter).

Reader IV's own excerpt independently states the same rule in near-identical language: "Occupant of the
constellation of [the house's occupant] is stronger than the occupant. Occupant of a house is stronger
than the lord of the house."

**Ordering A is confirmed at high confidence: star of occupant > occupant > star of owner > owner.**
Orderings B and C (section 17.1) were not found anywhere in the retrieved primary text and are treated as
not part of Krishnamurti's own stated rule - Ordering B in particular (the "occupant in an enemy's sign"
exception) remains unverified and is not adopted.

### 19.2 Retrograde treatment - RESOLVED (more precise than either v0.1.0 position)

Reader III states, in a worked example: **"A planet, in direct motion, gives a result and confirms it. A
planet, in retrogression, will produce a result which will fall through when it takes direct motion."**
A second worked example corroborates directly: an 11th-lord Jupiter, retrograde, denies recovery of lost
property specifically **"during the period of Jupiter's retrograde motion"**, becoming available only
after the date it is calculated to station direct.

**This is neither v0.1.0's "modulating factor only" nor its "flatly denies" reading - it is a third,
more precise primary rule: a retrograde significator's promised result is conditional, and typically
fails or reverses if/while the planet remains retrograde, with the promise reinstated once it stations
direct.** One further passage (the Ketu/theft example) shows this can also manifest as a *durable* denial
when the retrograde significator represents an undesired claim (the thief's own claim to stolen property)
rather than a desired outcome - i.e. the rule is about the *reliability* of what the retrograde planet
signifies, applied consistently in both directions, not a simple universal "good" or "bad" tag.

**V1 rule:** a retrograde-planet significator's promise is disclosed as *conditional on direct motion*
rather than treated as equivalent to a direct-motion promise - implementable as a disclosed qualifier on
the judgment output, not a silent pass/fail.

### 19.3 Node (Rahu/Ketu) treatment - RESOLVED

Reader III states this rule for nodes four separate times, in near-identical wording each time, e.g.:
**"As Rahu does not own any sign, find out with which planet it is conjoined or aspected by and the sign
and the constellation where it was at birth... Rahu or Kethu will give the results of the planets with
which it is conjoined, then those of the planet which aspects them. Lastly, those of the lord of the sign
[it occupies]."**

**Confirmed priority order, explicit and repeated: conjoined planet > aspecting planet > sign lord
(fallback only when neither applies).** This is layered on top of, not a replacement for, `KP_CHAIN_V1`'s
own existing SL/NL/SB/SS assignment for nodes (section 4/9) - the substitution rule governs *what houses
a node signifies* (since it owns no sign of its own), while the node's own star/sub position (which stars
it rules, what its own SL/NL/SB/SS is) is unaffected and needs no special-casing.

### 19.4 Positive/negative house groups for "will marriage happen with this party" - RESOLVED

Reader III's own horary chapter (Q12, "how to find out why a marriage which was about to be settled was
prevented from fructifying") states the rule directly:

> "The sub-lord of the 7th cusp should be the significator of the houses 1, 6, 10 or 12. It shows that
> the marriage will not take place with the party in question."

The positive group is separately, explicitly stated (general marriage-timing chapter, with its own
classical rationale, not merely asserted): **"By marriage, it is meant that one more member is added to
the family which is indicated by the second house. This addition is an agreement which is denoted by the
seventh... and such an additional member brings permanent tie of friendship for pleasure and progeny,
shown by the 11th house. That is why houses 2, 7 and 11 are examined."**

**Confirmed: positive = 2, 7, 11; negative = 1, 6, 10, 12**, for this specific question. The same chapter
goes further than a bare binary: if the sub-lord signifying 1/6/10/12 *also* signifies a further specific
house, that names the specific *reason* for the denial (2 -> lack of money; 3 -> neighbour/cousin
interference; 4 -> maternal interference or property disagreement; 5 -> prior love affair exposed; 1&6
together -> ill-health/servants/secret enemy; 7 -> a pending lawsuit; 8 -> insufficient dowry or a
relative's death; 9 -> travel/examination prevents attendance; 1&10 together -> elder/officer
interference; 11 -> friend/elder-brother interference; 12&1 together -> secret enemies/false propaganda) -
elaboration of *why*, not a change to *whether*.

**Question-granularity independently reconfirmed from primary text, not only secondary sources**: this
exact chapter is structurally distinct from the separate "marriage promised but late" chapter (a
different, non-house-list, planet-condition-based rule - Saturn/Mars/Moon placements) and from the general
"is marriage celebrated in youth" chapter (a rich ~20-item classical combination catalogue, not a clean
positive/negative binary at all). Three genuinely different rule shapes for three genuinely different
questions, confirmed directly in Krishnamurti's own text - v0.1.0's hypothesis (17.2) that tertiary
sources were collapsing a more granular primary structure is now itself primary-source-confirmed.

**One honest residual caveat:** the 1/6/10/12 passage is presented via a horary illustration (a querist's
horary number). No separately-stated natal-chart version of the identical house list was found in the
retrieved text. KP's own house-signification mechanism is presented as chart-type-agnostic everywhere else
in Reader III (only chart *erection* differs between horary and natal, not what a house or its sub-lord
signifies once cusps are known), and no competing natal-specific list was found, so applying this rule to
natal charts is a reasonable, disclosed inference, not an unqualified primary-source natal citation. This
is recorded as V1's own explicit non-claim addition (section 19.7).

**Update (2026-08-28), per `DP-030` section 11:** Reader IV, re-fetched directly and read (not merely
searched via a summarising pipeline), independently corroborates this exact rule and its classical
rationale in a general, non-horary chapter ("TIME OF MARRIAGE," p.70) and in several worked chart
examples with real data - not only in Reader III's own horary chapter as previously recorded here. This
strengthens the rule's own evidentiary basis (a second independent primary Reader agrees) but **does not
resolve the caveat above**: no passage found in either Reader is unambiguously and exclusively natal in
framing, so the horary-to-natal application remains a reasoned inference, not an unqualified primary
citation. See `DP-030` section 11 for the full finding.

### 19.5 Children/5th-house parallel - NOT resolved, not pursued further

The 5th-house/children positive-negative equivalent was searched for in the retrieved Reader III/IV text
and not found with comparable clarity. Not required for the recommended narrow V1 (section 19.6), and not
pursued further this task to stay within scope - recorded as a named gap, not silently omitted.

### 19.6 Updated V1 recommendation

Given 19.1-19.4, the recommended V1 (upgraded from section 17.4's hedged binary) is: the general
significator-chain mechanism (section 1 stage 1, section 4) plus **one** fully-specified cuspal-sub-lord
judgment - "does the 7th cusp's sub-lord signify the marriage-promise houses (2, 7, 11) or the
marriage-denial houses (1, 6, 10, 12)" - using Ordering A (19.1) for significator determination, the
conditional-retrograde disclosure rule (19.2), and the node substitution rule (19.3) where applicable.
**Confidence: medium-high** (raised from v0.1.0's medium) - the remaining uncertainty is the horary-versus-
natal inference (19.4's own caveat) and the single-transcription-pass OCR risk (19.0), not open
methodological disagreement.

### 19.7 Updated explicit non-claims (additive to section 16)

9. The marriage-promise/denial house rule (2/7/11 vs 1/6/10/12) is drawn from a horary illustration in
   Krishnamurti's own Reader III; its application to natal charts is a disclosed, reasoned inference, not
   an unqualified primary citation for the natal case specifically (section 19.4).
10. Source text is a scanned/OCR'd reprint, single-transcription-pass, not a publisher-verified critical
    edition (section 19.0) - disclosed on the chart/result itself, not only in this document.
11. The children/5th-house parallel is not covered by V1 (section 19.5).

## 18. Status and the exact CEO decision(s) required to proceed

**Updated determination (v0.2.0): most of v0.1.0's disagreements are now resolved from direct primary-
source evidence (section 19), not merely narrowed by recommendation.** Per the CEO's own explicit
instruction, this determination is stated plainly: **the evidence establishes that KP significators CAN
responsibly be frozen for a narrow V1** - the condition for recommending a switch to Parashari yoga is
not met, and no such switch is recommended. `KP_SIGNIFICATOR_V1` is closer to ready for `ADR`-level
ratification than v0.1.0 found, but is **still not frozen** - three items remain genuinely open, all
narrower in scope than v0.1.0's four:

1. **Ratify the primary-source resolution itself** (section 19): accept Ordering A, the conditional-
   retrograde rule, the node substitution rule, and the 2/7/11 vs 1/6/10/12 marriage judgment as V1's
   frozen methodology, on the evidentiary basis section 19 discloses (genuine Reader text, single-pass
   OCR, horary-to-natal inference) - or require independent re-verification of the OCR transcription
   before treating it as frozen.
2. **Confirm the V1 matter scope** (section 19.6): the single 7th-cusp marriage-promise/denial judgment,
   at medium-high confidence, or a different/broader scope.
3. **Confirm the horary-to-natal inference** (section 19.4's own caveat): accept it as reasonable, or
   require it treated as a disclosed non-claim/caveat on every V1 result rather than a settled rule.

Sections 17.5 (Ruling Planets composition, out of scope, not required) and 19.5 (children/5th house, not
pursued) remain open but do not gate V1.

This document does not implement anything, does not ratify anything, and does not choose among the three
items above. It is ready for the owner's review and, on any combination of decisions above, can be
revised (as a new version) into a frozen V1 ready for `ADR`-level ratification and certification-design
work, mirroring the `ADR-0076`/`ADR-0077` two-stage pattern already used for `D45`.

## Change history

| Version | Date | Change |
|---|---|---|
| 0.2.1 | 2026-08-28 | Per "CEO AUTHORIZATION - DP-030 OPTION 1": section 19.4's residual caveat updated with a pointer to `DP-030` section 11 - Reader IV, re-fetched directly and read (not via a summarising pipeline), independently corroborates the marriage-grouping rule and its classical rationale in a general, non-horary chapter and several worked examples with real chart data. The caveat itself (horary-to-natal application is a reasoned inference, not an unqualified citation) is explicitly preserved, not resolved - no passage found in either Reader is unambiguously natal-only. No other section edited; no methodology, frozen rule, or certification artifact changed. |
| 0.2.0 | 2026-08-25 | Per "CEO AUTHORIZATION — CONTINUE KP METHODOLOGY EVIDENCE RESOLUTION": continued, persistent, targeted search located and directly retrieved K.S. Krishnamurti's own Reader II, Reader III, and Reader IV (`archive.org`, `kp-readers` collection and the standalone `kpreader-4-marriage-married-life-children` item), extracted to plain text locally and searched directly - genuine primary source, not secondary restatement, with retrieval limits (scanned/OCR reprint, single transcription pass, partial Reader IV excerpt) disclosed precisely in new section 19.0. Constructed the source/claim matrix the instruction required (section 19) and resolved, with direct verbatim primary-source quotes: the significator strength order (19.1, Ordering A confirmed at high confidence across six independent passages); retrograde treatment (19.2, a third, more precise "conditional on direct motion" rule, neither v0.1.0 position); node treatment (19.3, explicit conjoined-planet > aspecting-planet > sign-lord priority, confirmed four times); and the marriage promise/denial house groups for one specific, well-scoped question (19.4, positive 2/7/11, negative 1/6/10/12, with Krishnamurti's own classical rationale for the positive group and a rich per-additional-house elaboration of denial reasons) - independently reconfirming, from primary text, v0.1.0's own question-granularity hypothesis. Determined explicitly, per the instruction's own branching condition, that the evidence establishes KP CAN responsibly be frozen for a narrow V1, so no switch to Parashari yoga is recommended. Updated the V1 recommendation to medium-high confidence (19.6) and narrowed section 18's decision point from four gated items to three, all narrower than v0.1.0's. Does not implement KP significators. Does not ratify anything. Sections 17 and its own v0.1.0 findings preserved unedited as the prior-state record, each with an explicit pointer to where section 19 superseded it. |
| 0.1.0 | 2026-08-25 | Created. Drafted per "CEO DECISION — DP-028" items 3-10, structured against `ADR-0027` Decision 4's sixteen-item checklist. External research (K.S. Krishnamurti's own Reader I directly inspected and confirmed foundational-only; Reader III sought but not located; *K.P. Dynamics* by Sri Satyanarayana Naik retrieved as the most substantial secondary source) independently verified against multiple sources per claim, surfacing genuine, evidenced disagreements rather than silently resolving them: three different significator-strength orderings (17.1); question-granular, source-disputed positive/negative house groups even within "marriage" alone (17.2); a retrograde-treatment tension between "modulating factor" and a direct KSK-attributed "denies its own result" claim (8); an open question on whether nodes need special-casing beyond `KP_CHAIN_V1`'s own certified chain output (9). Four Step Theory and Ruling Planets marked N/A, per explicit exclusion. Does not implement KP significators. Concludes NOT FROZEN - identifies four gated owner decisions (source-authority strategy, V1 matter scope, significator strength order, retrograde/node treatment) required before certification-design work can begin, mirroring the `D45` precedent's own methodology-first rule. |
