<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents readiness state and options. DECIDES NOTHING. Requires owner approval. **Section L records a CEO HOLD disposition on a proposed `PARASHARI_YOGA_V1` ADR/certification-design draft - not itself a ratification; no ADR number assigned. Section M records the owner's authorization to draft the ADR only - drafting is not yet performed, and the ADR is not thereby ratified.** |
| Version | 1.4.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-29 (section M added: the owner's own "proceed" instruction, interpreted narrowly per explicit CEO directive, persisted as authorization to draft the `PARASHARI_YOGA_V1` ADR only - not to ratify it, not to design or execute certification, not to implement, not to integrate with convergence. Binds the future draft to incorporate every applicable section-L correction, named by reference, section L's own text unedited.) |
| Review cadence | TBD |

# DP-027. Parashari yoga/rule-combination-evaluation methodology-specification decision-readiness

## 0. Authorization and scope

Authorized by "CEO direction — proceed with DP-023 resolution," item 4: "Prepare/authorize separate
decision-readiness papers for `D-008` KP significators and Parashari yoga methodology, but do not
implement either." This paper does not draft a Parashari yoga specification - it establishes that, unlike
KP significators, no root decision or checklist exists for it at all, and proposes one by analogy. It
does not implement anything.

## A. What already exists - confirmed absent, not merely undocumented

**No governing decision exists.** Searched `docs/OPEN_QUESTIONS.md`, `docs/DECISION_LOG.md`, and root
`DECISION_LOG.md` for "yoga": no entry addresses combination-yoga methodology (the panchanga "yoga"
anga, an unrelated concept, appears in several places and must not be conflated with this). `docs/
PARASHARI_DRISHTI_SPEC.md` explicitly states "strengths, yogas, and judgments out of scope" for the
already-certified drishti module - the clearest existing statement that yogas are deliberately deferred,
though it neither names a source nor proposes a checklist. **Unlike KP significators, Parashari yoga has
no analogue to root D-008/`ADR-0027` - no checklist, ratified or not, exists anywhere in this
repository.**

**Confirmed zero implementing code**, re-verified this task: `grep -ri yoga` across `engine/**/*.py`
returns only the panchanga anga enum value (`engine/knowledge/models.py` line 38) and provenance
non-claims ("no strengths, yogas, or judgments," `engine/models/drishti.py`) - no combination-yoga-
detection logic anywhere.

## B. Why this is genuinely harder than KP significators

`DP-023`'s own scoring (candidate 13) already found Parashari yoga's source landscape "fragmented" -
classical sources (BPHS, Phaladeepika, Saravali, Jataka Parijata, and modern compilations) name
materially different yoga sets and qualifying/cancellation (bhanga) conditions, with no single founding
authority the way KP has K.S. Krishnamurti's own body of work. Certification difficulty is correspondingly
higher: it is not confirmed whether any external oracle (PyJHora or otherwise) computes classical yogas
in a form directly usable for comparison - not investigated this task, an explicit non-claim below - so
even a frozen methodology might not have an available oracle the way every certified capability in this
repository has had one.

## C. Proposed checklist, by analogy to `ADR-0027` item 4 (not itself a ratified requirement)

A Parashari yoga specification would need, at minimum, by direct analogy to the KP-significator
checklist's own structure: an exact methodology (which yogas, drawn from which named classical source);
source authority (a single chosen text or an explicit, source-attributed set); qualifying conditions per
yoga; cancellation (bhanga) rules per yoga, if the chosen source includes them; house/sign/aspect/varga
dependencies per yoga (all already certified inputs, per `DP-023` section C); strength or graded-presence
treatment, if any (interacting with the currently-refused `planet_strength.py` stub - a yoga specification
that requires strength grading would itself depend on Shadbala, which `DP-023` also found not
methodology-ready); an oracle or independent-verification strategy (genuinely unconfirmed, section B);
school/tradition scope; independent validation protocol; protected holdout; negative controls; acceptance
criteria; explicit non-claims (most importantly, which named yogas are NOT covered by a V1).

**This checklist is this paper's own proposal, constructed by analogy - it has no ratified or even
drafted precedent in this repository, unlike KP's own `ADR-0027`.**

## D. Options

1. **Authorize drafting a Parashari yoga specification decision-readiness task**, using the checklist in
   section C as a starting structure, explicitly flagged as unprecedented in this repository (no `ADR-
   0027`-equivalent exists to build on).
2. **First resolve the oracle-availability question** (section B) as its own narrow research task, since
   a chosen methodology without any verification path would produce a certification gate that cannot
   meaningfully fail - exactly the failure mode `.claude/rules/certification.md` prohibits.
3. **Defer** - `DP-023`'s own scoring already found this the least methodology-ready, highest-variant-
   ambiguity candidate in the full inventory; nothing compels acting on it now.

## E. Recommendation and confidence

**At medium confidence:** resolve the oracle-availability question first (Option 2), before authorizing
specification drafting - a specification with no achievable verification path would not itself be
implementable regardless of how well-drafted it is, per this project's own "a gate that cannot fail is
not evidence" rule. This is a narrower, cheaper research step than full specification drafting and would
materially change how ambitious a first yoga specification could safely be.

## F. Explicit non-claims

This paper does not draft a Parashari yoga specification. It does not choose a classical source. It does
not resolve whether PyJHora or any other tool can serve as an oracle for yoga detection - that
investigation was not performed this task. It does not implement anything.

## H. Oracle-availability decision-readiness research (2026-08-25)

Authorized by the owner's explicit "Oracle-availability research may proceed only as decision-readiness
research; no Parashari yoga specification or implementation is authorized yet" instruction. This section
performs exactly that research and nothing further.

### H.1 Finding: an oracle exists, and is far more extensive than section B assumed

Section B's own "not confirmed whether any external oracle... computes classical yogas" is **superseded
by direct evidence.** The same local PyJHora installation already used as this project's own oracle for
vargas, panchanga, and dasha carries a dedicated `jhora.horoscope.chart.yoga.py` module (12,990 lines)
implementing **233 individually-named yoga-detection functions** (confirmed by direct count:
`grep -c "^def .*_yoga("`), each with its own docstring citing a source. Examples inspected directly:
`vesi_yoga`, `vosi_yoga`, `ubhayachara_yoga`, `nipuna_yoga`, `sunaphaa_yoga`, `anaphaa_yoga`,
`duradhara_yoga`, `kemadruma_yoga`, `chandra_mangala_yoga`, `adhi_yoga`, `ruchaka_yoga`, `bhadra_yoga` -
all genuine, recognizable classical Parashari yoga names, not invented labels.

### H.2 Finding: a single, consistently-cited, named source authority

Every yoga function's own docstring cites a `BVR-N` reference (e.g. "BVR-16," "BVR-49"), sequentially
numbered. Confirmed directly (`grep`): one docstring spells the abbreviation out in full - **"BVR-49
Kalanidhi Yoga (B.V. Raman #49)"** - identifying B.V. Raman, a widely recognized, published 20th-century
Vedic astrology author, as the consistent source for at least the yogas checked. This is a **materially
better source-authority situation than section B's own "fragmented... no single founding authority"
characterization of the classical landscape in general** - PyJHora's own specific implementation draws
from one named, numbered, internally-consistent compilation, not an ad hoc mixture, for the 233 yogas it
implements.

### H.3 What this does and does not establish

**Established:** an oracle-capable reference implementation exists, is already available in this
project's own oracle environment (no new tooling needed), and cites a real, named, checkable source for
at least a large subset of its own 233 yogas. This substantially lowers `DP-023`'s own "certification
difficulty: High, oracle unconfirmed" assessment for Parashari yoga (candidate 13) - an oracle is, in
fact, available.

**Not established, and explicitly not claimed:** that B.V. Raman's own yoga compilation is *the* correct
or only source this project should adopt (BPHS, Phaladeepika, Saravali, and other classical texts remain
independently valid, differently-scoped alternatives, per section B); that PyJHora's own qualifying/
cancellation logic for each of the 233 yogas has been checked against B.V. Raman's own original text
(spot-checked for docstring citation only, not for correctness of implementation); that all 233 yogas'
own docstrings were individually reviewed (a sample was checked; a full audit was not performed - this is
its own future task, not decision-readiness-scope work). **Per the owner's own explicit caution about
D45's own PyJHora finding, restated here for yoga: PyJHora's own implementation is independent
corroboration that a codified, source-cited yoga catalog can exist and be computed - it is not
automatically the normative methodology this project should adopt.** Whether to adopt B.V. Raman's own
233-yoga set (in whole or part) as this project's own certified V1 scope remains a genuine, unmade
methodology choice.

### H.4 Revised recommendation

**At medium-high confidence (raised from section E's own medium, given H.1-H.3's new evidence):** if
Parashari yoga is pursued, B.V. Raman's own compilation, as already codified in PyJHora's `yoga.py`, is
the strongest available starting candidate for "source authority" (`ADR-0027`-style checklist item 2, by
analogy) - named, numbered, internally consistent, and already computationally available - but adopting
it should be its own explicit methodology decision, not inferred silently from oracle convenience. This
paper still does not authorize drafting a specification or beginning implementation.

## I. Exact CEO decision required

1. Authorize the oracle-availability research step (performed in section H) as sufficient for now, or
   direct a fuller audit of PyJHora's own 233 yoga definitions against B.V. Raman's original text before
   proceeding further.
2. Whether to authorize specification-drafting decision-readiness next, using B.V. Raman's own
   PyJHora-codified compilation as the starting source-authority candidate (section H.4), or a different
   classical source, or defer entirely.
3. If specification drafting is authorized: confirm the section C checklist (constructed by analogy) as
   the starting structure, updated with section H's own source-authority finding.

## J. Candidate-yoga decision-readiness research (2026-08-26)

Authorized by the owner's explicit "CEO AUTHORIZATION - BEGIN PARASHARI YOGA V1 DECISION-READINESS"
instruction: a narrowly scoped decision-readiness investigation only, against nine numbered questions,
not assuming PyJHora's 233 functions are authoritative, preferring one or a very small number of
tightly-defined yogas over a large catalog, reusing this paper's own already-settled content rather than
re-deriving it, and not implementing anything. This section answers the nine questions in order.

### J.1 Which yoga(s) have the strongest primary-source support

**Panch Mahapurusha Yoga** (five yogas - Ruchaka, Bhadra, Hamsa, Malavya, Sasa - for Mars, Mercury,
Jupiter, Venus, Saturn respectively). Its base formation rule is stated as a single, direct BPHS verse,
confirmed this task via the same translation family already cited by this project's own
`engine/knowledge/data/dignities.json` (R. Santhanam-lineage editions; astrojyoti.com's own BPHS
translation page returned the identical wording independently): "When Mars, Mercury, Jupiter, Venus and
Saturn, being in their own, or exaltation Rasi, be in Kendra to Lagna, they give rise to Ruchaka, Bhadra,
Hamsa, Malavya and Sasa Yogas." Every secondary source checked (GrahaLab, Satyori, jyotishteachings.com's
own PDF, PanchangBodh, Akashastro, Aradhana) restates this identical core condition without variant. This
is a **stronger** primary-source position than KP significators required (`ADR-0027` had to establish
K.S. Krishnamurti as founder from first principles; here the **same BPHS text** already governs every
certified Parashari-school capability in this repository - D2, D3, D7, D9, D10, D12, D30, D45, and
`engine/astrology/dignity.py` itself).

### J.2 Whether the existing certified ACE foundations are sufficient

Yes, more directly than any prior V1 candidate in this repository. The base rule needs exactly two
already-existing, already-tested primitives applied to the Tier-0-locked D1 kernel's own planet
longitudes and ascendant:

- `engine.astrology.dignity.is_exalted` / `is_own_sign` (`engine/astrology/dignity.py:39,61`) - BPHS-
  cited (`engine/knowledge/data/dignities.json` metadata), independently hand-entered a second time in
  `engine/tests/test_dignity.py` "independently of the JSON data files so a data-entry error in either
  copy surfaces as a failure" (file's own docstring).
- `engine.astrology.house.whole_sign_house` (`engine/astrology/house.py:41-49`) - already the documented
  project decision for Parashari D1 charts ("The Parashari D1 chart builder uses WHOLE SIGN - the
  documented project decision for Rashi charts," same file's own module docstring). Kendra is simply
  house membership in `{1, 4, 7, 10}`.

Zero new astronomical calculation and, unlike `ADR-0078`'s KP-scoped aspect calculation, **zero new
aspect logic of any kind** is required - this is architecturally simpler than KP_SIGNIFICATOR_V1.

**One genuine gap, not a blocker:** `docs/DECISION_LOG.md` line 1912 records that dignity data "sits
outside lock scope" - it is tested but has never been through this project's own certification-gate
process (no `DIGNITY_V1_certification.json` exists). A `PARASHARI_YOGA_V1` certification would need to
either pin dignity.py's seven relevant exaltation/own-sign facts as the new certification's own frozen
content (mirroring how `KP_SIGNIFICATOR_V1` pinned its own frozen rule constants via
`rule_content_sha256()`), or independently re-verify them in a `table_integrity` gate. This is a normal,
narrow certification-design task, not a methodology-readiness obstacle.

### J.3 Which yoga has the least methodological ambiguity

The **base formation condition** (own-sign-or-exaltation-sign + kendra-to-Lagna) has effectively none -
a single verse, unanimous secondary-source restatement, no competing variant found. What genuinely **is**
ambiguous, confirmed this task by targeted search: bhanga (cancellation) conditions are multi-sourced and
contested - one source describes a specific cancellation chain as "an untested concept," and effects are
attributed inconsistently across sites; and retrograde treatment is a live classical disagreement (some
sources hold retrograde strengthens a planet already in its own/exaltation sign; others hold it
destabilizes the yoga) with combustion treated as a modern, non-BPHS-verse addition in every source
checked. **This is the same shape of ambiguity `ADR-0078` already resolved once for KP significators'
own retrograde treatment** - decision-readiness output, not a blocker: exclude bhanga/cancellation and
combustion from V1 entirely, and carry retrograde as a disclosed qualifier, never a pass/fail gate,
directly mirroring `ADR-0078` section 6's own already-certified pattern.

### J.4 Whether PyJHora can serve as useful corroboration/reference

Partially confirmed, not assumed further than the evidence supports. Section H.1 (already recorded, not
re-derived) directly `grep`-confirmed `ruchaka_yoga` and `bhadra_yoga` function names exist in PyJHora's
`yoga.py` (BVR-numbered, 233-function catalog). Hamsa/Malavya/Sasa's own function names were **not**
re-verified this task - the local PyJHora environment's own degraded state (recorded in this session's
prior KP-significator work: `numpy.__version__` raising `AttributeError` under the venv's own
interpreter) was not re-diagnosed here, since doing so is certification-execution-scope work, not
decision-readiness. Recommendation: confirm all five function names and inspect whether their own
qualifying logic matches the base-rule-only V1 scope (i.e., does not silently bake in a bhanga check) as
an early certification-design step - not a blocker to methodology freeze, since the BPHS text itself,
independent of PyJHora, already supports the rule.

### J.5 What an independent validator can independently derive

Everything needed. `engine/tests/test_dignity.py` already proves the seven relevant exaltation/own-sign
facts are a crisply re-derivable, independently-checkable classical table (it re-enters them by hand a
second time, separate from the JSON file, precisely to catch a data-entry divergence). A from-scratch
validator can reimplement both the dignity table and the whole-sign kendra check directly from raw D1
longitudes without importing `engine.astrology.dignity` or `engine.astrology.house` at all - the same
from-scratch discipline already used for `validate_kp_significator_holdout.py` and D45's own validator.

### J.6 Whether a protected holdout is meaningful for the chosen deterministic rule

Yes, same shape as `KP_SIGNIFICATOR_V1`'s own 12-chart protected holdout: real ephemeris-driven natal
charts (reusing the Tier-0-locked kernel), each yoga's presence/absence per relevant planet computed
independently by the validator and compared against the certifier under the frozen rule. Meaningful
because the rule is fully deterministic and the chart data is continuous, real, and not limited to
synthetic edge cases.

### J.7 Boundary/negative-control requirements

**Boundary:** Panch Mahapurusha's own formation condition is stated at the sign (Rasi) level, not the
degree level - own-sign-or-exaltation-**sign**, not moolatrikona span - so degree-level exaltation-decay
boundaries (relevant to Shadbala, not this yoga) do not apply. The real boundaries are sign-membership
edges (a planet at 29d59m59.99s vs 0d00m00.00s of the exaltation sign) and kendra/non-kendra house edges,
both already whole-sign (inherited directly from `whole_sign_house`'s own already-exercised boundary
behavior - no new boundary mathematics). **Negative controls:** planted mutations following the
established pattern - swap a kendra house set for a non-kendra set; swap one planet's own-sign list
entry; swap one planet's exaltation sign - each must change the certification's own frozen content hash
and be independently caught by the validator.

### J.8 The minimum viable V1 scope

The five Panch Mahapurusha yogas only (Ruchaka/Bhadra/Hamsa/Malavya/Sasa), base BPHS formation rule only
(own-sign-or-exaltation-sign AND kendra-to-Lagna via whole-sign houses), for natal D1 charts under the
already-certified Parashari/Lahiri profile. Explicit non-claims, by direct analogy to `ADR-0078` section
9: no bhanga/cancellation logic of any kind; no combustion gating; retrograde as a disclosed qualifier
only, never a pass/fail gate; no strength/grading beyond present-or-absent; no other yoga catalog (Raja
yoga, Dhana yoga, Sunapha/Anapha/Kemadruma, and the remaining ~228 PyJHora-catalogued yogas all
explicitly out of scope for V1); no interpretive or predictive claim about life outcomes - an ACE-
computed structural fact only ("this chart satisfies BPHS's own stated Ruchaka-yoga formation condition"),
never represented as validated astrological or predictive truth, per this project's own C4-is-not-C5 rule
(`docs/DECISION_LOG.md` line 1916-1918).

### J.9 Whether the methodology can be frozen without further owner judgment

Mostly yes for the base rule itself - unlike KP significators, there is no competing checklist variant to
choose between. Two narrow judgment calls remain, both scope decisions rather than open fact-finding
gaps:

1. Confirm V1 excludes bhanga/cancellation and combustion, and treats retrograde as disclosure-only -
   a scope choice needing explicit ratification the same way `ADR-0078` ratified KP's own retrograde
   treatment, not a fact still to be discovered.
2. Confirm `engine/astrology/dignity.py`'s existing BPHS-cited values may serve as the new
   certification's own frozen source-of-truth content (pinned the way `KP_SIGNIFICATOR_V1` pinned its own
   rule constants), given dignity data sits outside Tier-0 lock and has never itself been through this
   project's own certification-gate process (`J.2` above).

### J.10 Dependency check against DP-024/DP-025

No direct dependency found. Panch Mahapurusha's base rule touches only dignity data and whole-sign house
membership, neither of which routes through `DP-024` or `DP-025`'s own still-deferred scope (both
remain untouched, per the owner's own explicit instruction not to reopen them absent a genuine
dependency).

## K. Revised exact CEO decision required (supersedes section I for this candidate)

Section I's own three items remain accurate as a dated record of the state before this task's research
and are **not edited**. This section restates the decision point now that a specific, strongly-supported
candidate exists.

**The next genuine CEO decision point:** whether to authorize drafting a `PARASHARI_YOGA_V1` ADR
(methodology freeze), using:

- The five Panch Mahapurusha yogas (Ruchaka, Bhadra, Hamsa, Malavya, Sasa) as the complete V1 catalog.
- BPHS's own stated formation rule only: own-sign-or-exaltation-sign AND kendra-to-Lagna (whole-sign
  houses), computed from the already-certified/Tier-0-locked D1 kernel plus `engine.astrology.dignity`
  and `engine.astrology.house.whole_sign_house`.
- The explicit non-claims in section J.8 (no bhanga/cancellation, no combustion gating, retrograde as
  disclosure-only, no other yogas, no interpretive/predictive claim).
- `engine/astrology/dignity.py`'s existing values adopted as the new certification's own frozen,
  content-hash-pinned source-of-truth (J.9 item 2), rather than a fresh primary-source re-derivation.
- The same D45/KP process template: research (this section) -> methodology freeze (ADR) -> certification
  design -> certification execution -> production -> CI -> merge, each its own separate owner
  authorization, exactly as already executed for KP_SIGNIFICATOR_V1.

If authorized, the next task would be drafting that ADR itself - not yet performed, since this task's own
authorization was decision-readiness only.

## L. CEO disposition of the proposed `PARASHARI_YOGA_V1` ADR/certification-design draft (2026-08-29) - HOLD

Per "CEO REVIEW - PARASHARI_YOGA_V1" and the subsequent "CEO AUTHORIZATION - PERSIST GOVERNANCE DECISION
ONLY" instruction: this section records the CEO's disposition of a proposed `PARASHARI_YOGA_V1` ADR/
certification-design draft that was produced and revised in conversation (never written to this
repository, never numbered, never ratified) in response to section K's own decision point. **No decision-
log ADR number is assigned by this section.** The proposal remains conversational work product until a future
task explicitly persists an ADR draft to this repository under its own authorization; this section records
only the CEO's own review verdict and the specific methodology/governance corrections that must guide any
future revision.

### L.1 Verdict

**HOLD.** The methodology is approved in principle. **The proposed ADR is NOT ratified. No certification
design, certification execution, or implementation is authorized by this disposition or by anything
recorded in this paper to date.** Conversation alone is not permanent project authorization - this section
exists specifically because that authorization must be persisted here, in the repository, not left to
stand only in a chat transcript.

### L.2 Governance / sequencing

`PARASHARI_YOGA_V1` remains on HOLD until the required authorization and methodology decisions are
explicitly persisted in the repository, section by section, the same way every other certified capability
in this project reached its own ADR. This section is such a persistence step; it is not itself that
authorization.

### L.3 Production code is not the certification oracle

`engine/astrology/dignity.py` may remain a production dependency for any eventual `PARASHARI_YOGA_V1`
implementation. **Production `dignity.py` output must not serve as the certification oracle / expected-
answer source.** A production module that both computes the answer and supplies its own certification's
"expected" answer is exactly the structural defect the `KP_SIGNIFICATOR_V1` certification-integrity repair
(`ADR-0079`) found and corrected - this paper records, in advance, that `PARASHARI_YOGA_V1` must not repeat
it.

### L.4 Dignity table independence - a real distinction, not yet fully satisfied

A certification-side dignity table may be used as a **second independent transcription of the same cited
classical edition** (`dignities.json`'s own citation: BPHS, graha guna chapter, per the R. Santhanam-
lineage published edition). **That transcription MUST NOT be described as source-level independent of
production merely because it is separately typed.** Two distinct claims must never be conflated:

- **Implementation independence** - a second, separately-authored piece of code that does not import or
  call the production module. A fresh transcription of the same cited edition satisfies this.
- **Source/edition independence** - verification against a genuinely different classical source, edition,
  translator, or page, not merely a second copy-out of the identical cited edition. A fresh transcription
  of the SAME edition does **not** satisfy this.

Edition, translator, and page provenance for both the production citation and any certification-side
transcription must be recorded when certification design is eventually authorized - not deferred silently.
**Source-level correctness of the cited edition itself, beyond that one edition, remains an explicit
non-claim unless separately established** (e.g. by cross-checking a second, genuinely different published
edition or the original Sanskrit - not performed, not assumed, not silently claimed).

### L.5 Exhaustive enumeration - space corrected

Any future certification design must use the **actual longitude/sign/house plumbing space**: 5 grahas x 12
graha signs x 12 ascendant signs = **720 cases**. The house result for each case must be **derived through
the specified production plumbing** (the real `whole_sign_house`/sign-of-longitude machinery, exercised
with real values), never supplied as an asserted kendra/non-kendra boolean flag. This corrects and replaces
any prior framing of the enumeration space in the conversational drafts, which is not itself part of this
repository's record.

### L.6 Mutation controls - a specific defect identified, not yet fixed

**A Mercury-exaltation-only mutation is not an acceptable negative control**, because Mercury's exaltation
sign (Virgo) is already a member of Mercury's own own-sign set (Gemini, Virgo) - the `OR` in the formation
predicate (own-sign OR exaltation-sign) can mask a corrupted exaltation value for Mercury specifically,
since the own-sign branch alone still yields the correct answer for Virgo. Any future certification design
must instead use **detectable** mutations, including at minimum:

- A **non-overlapping exaltation mutation** for Mars, Jupiter, Venus, or Saturn (grahas whose exaltation
  sign is not already one of their own signs, so corrupting it changes the predicate's actual result).
- A **Mercury mutation capable of changing the combined own/exaltation condition** - which, given the
  overlap just identified, requires corrupting Mercury's own-sign data as well as (or instead of) its
  exaltation data, since exaltation-only corruption is insufficient for this specific graha.

**Any mutation gate must demonstrate that the relevant certification evidence actually FAILS under the
mutation, run and observed, not merely executed without error.** A gate that runs to completion without
detecting a planted corruption is not evidence of anything, per this project's own "a gate that cannot fail
is not evidence" rule - restated here specifically because the Mercury case shows how easily that failure
mode can hide inside a plausible-looking mutation set.

### L.7 Normative methodology / PyJHora

BPHS remains the sole normative methodology for `PARASHARI_YOGA_V1`. PyJHora is **optional corroboration
only** and must never become the normative oracle. If PyJHora is used at certification-design or -execution
time, any disagreement between BPHS's own stated rule and PyJHora's own computed result must be **explicitly
classified** (e.g. as a PyJHora implementation variant, a translation difference, or a genuine open
question) and must **never silently change the frozen BPHS-sourced methodology**. Only the PyJHora functions
actually verified to exist and to have been inspected may be claimed as corroborating evidence -
`ruchaka_yoga` and `bhadra_yoga` only, per `DP-027` J.4/H.1. **No implication of five-yoga PyJHora coverage
is permitted unless Hamsa/Malavya/Sasa's own function names and logic are separately, actually verified.**

### L.8 D1 calculation / house entrypoint

The eventual production/certification design must explicitly identify and use:

- Sidereal calculation under the `PARASHARI_LAHIRI` profile, via this repository's established calculation
  entrypoint (the certified Tier-0 kernel already used by every other Parashari-school capability in this
  project).
- `zodiac_sign` (`engine.astrology.signs.zodiac_sign`) for 1-based sign assignment - already declared
  `ONE_BASED` in `engine/astrology/sign_conventions.py`'s own `SIGN_FUNCTION_CONVENTIONS` table.
- `whole_sign_house` (`engine.astrology.house.whole_sign_house`) for 1-based whole-sign house assignment
  from the ascendant, per that module's own documented Parashari D1 convention.

The 1-based convention and the house/sign offset relationship (house 1 = the ascendant's own sign; house N
= the sign N-1 positions ahead of the ascendant's sign, mod 12) must be stated explicitly in any future
design, not left implicit. **This entrypoint identification is no longer treated as an unresolved open
question** (it was flagged as open in the conversational drafts) **unless a future repository inspection at
certification-design time reveals evidence contradicting the specific functions named above** - none has
been found as of this section.

### L.9 Moolatrikona - exclusion confirmed inert, not merely excluded

**Record, as an explicit finding, not merely a scoping choice:** exclusion of moolatrikona from the V1
predicate is **inert** for these five yogas specifically, because each relevant graha's own moolatrikona
sign is already a member of that same graha's own-sign set (`engine/knowledge/data/dignities.json`: e.g.
Mars moolatrikona sign 1 = Aries, already in Mars's own_signs {1, 8}; the same containment holds for all
five grahas relevant to Panch Mahapurusha). **Therefore the V1 predicate's actual computed result is
unchanged whether moolatrikona is separately considered or not** - this is a factual finding about this
specific rule's own data, not merely a textual-reading preference, and should be recorded as such in any
future ADR rather than presented only as "the verse doesn't mention it."

### L.10 Certification meaning

Any future `PARASHARI_YOGA_V1` certification PASS must mean **only**: computational correctness of the
implementation of BPHS's own stated Ruchaka/Bhadra/Hamsa/Malavya/Sasa formation condition, verified against
independently-sourced expected data (per L.4's own precise independence distinction). It must **NOT** mean
astrological efficacy, predictive validity, real-world outcome validity, or any proven effect of a yoga on
a person's life. **This distinction must eventually appear in the certification artifact itself** - its own
`result`/`scope` fields - not only in this governance document, mirroring exactly how `KP_SIGNIFICATOR_V1`'s
own certification artifact discloses its own evidentiary limits directly in the artifact.

### L.11 Historical validation

Protected historical validation (this project's `ADR-0047`-style dataset-forensics discipline) is **not
applicable** to V1's structural formation-condition computation, because V1 makes no predictive or
interpretive claim - there is nothing for a historical-outcome dataset to validate against. **If a future
version of this capability makes a predictive or interpretive claim, that is a separate decision requiring
this project's own protected-validation framework** and its own separate authorization; it is not implied
or pre-authorized by anything in this section.

### L.12 Current status - what this section does not do

**This section does NOT authorize:** ADR ratification, certification design, certification execution,
implementation, convergence integration, or product feature work of any kind. It establishes the CEO's own
disposition - HOLD, with the specific corrections above - that must guide the next revision of the
`PARASHARI_YOGA_V1` ADR draft, whenever that revision is separately authorized. **This section does not
silently resolve any certification-design mechanic not explicitly addressed above** (e.g. the exact shape
of the certifier/validator table-sharing question raised in the conversational draft's own open items
remains genuinely open, not decided here).

## M. Authorization to draft the `PARASHARI_YOGA_V1` ADR (2026-08-29)

Per "CEO DIRECTIVE - PERSIST AUTHORIZATION FOR PARASHARI_YOGA_V1 ADR DRAFTING": the owner's own instruction
was the single word **"proceed,"** given in direct response to a directive that itself instructed it be
interpreted **narrowly**, as authorization for the next required governance step only. This section
persists that authorization, and that authorization only. It does not draft the ADR itself.

### M.1 What is authorized

**The owner authorizes drafting the `PARASHARI_YOGA_V1` methodology ADR.** Drafting is the **only** newly
authorized scope at this step. The future ADR, when drafted, is **not thereby ratified** by this
authorization - ratification remains a distinct, later, separately-required owner act, exactly as it was
for every other certified capability in this project (`ADR-0078`'s own drafting and its later, separate
ratification are the direct precedent).

### M.2 What remains separately unauthorized

Certification design, certification execution, implementation, and convergence integration each remain
**separately unauthorized** by this section, exactly as `L.12` already stated and as this directive itself
restates. No ADR number is assigned or reserved by this section - assigning one is a step for the drafting
task itself, per this project's own `check_adr_numbering.py`-mediated "get the next free number at drafting
time" convention, not something to pre-allocate here. No `mahapurusha_yoga.py` or any other `engine/` file
is created or modified by this section, and none is authorized by it.

### M.3 Binding constraint: the future ADR must incorporate every applicable §L correction

This authorization is conditioned on the future ADR draft incorporating **all** applicable corrections
already recorded in section L, restated here by name only, not re-derived or altered - section L's own
text (`L.3`-`L.11`) remains the authoritative detail, unedited:

- BPHS as the sole normative methodology (`L.7`).
- The five Panch Mahapurusha yogas only, base formation rule only - no broader catalog.
- No bhanga/cancellation logic; no combustion gating; retrograde as a disclosed qualifier only, never a
  gate (`L.1`, section J.8, carried forward unedited).
- No predictive or interpretive efficacy claim (`L.10`).
- Production `engine/astrology/dignity.py` must never serve as the certification oracle (`L.3`).
- Certification-side dignity data must be implementation-independent, with its own source/edition
  provenance honestly disclosed - and not described as source/edition-independent merely for being
  separately transcribed (`L.4`).
- If certification is later authorized, exhaustive enumeration is the real 5 x 12 x 12 = 720-case
  longitude/sign/house plumbing space, house-derived through actual production plumbing, never an
  asserted flag (`L.5`).
- The Mercury-exaltation-only mutation is invalid as a negative control; a detectable replacement is
  required (`L.6`).
- PyJHora remains optional corroboration only, never the normative oracle; only the functions actually
  verified (`ruchaka_yoga`, `bhadra_yoga`) may be claimed (`L.7`).
- The D1 calculation/house entrypoint (`PARASHARI_LAHIRI`, `zodiac_sign`, `whole_sign_house`) and its
  1-based convention must be stated explicitly (`L.8`).
- Protected historical validation remains inapplicable to this deterministic formation-condition
  certification (`L.11`).

### M.4 Not decided by this section

This section does not choose the future ADR's own exact wording, does not resolve the certifier/validator
table-sharing question `L.12` already left open, and does not decide when drafting will actually occur -
it records only that the owner has authorized it to occur, on the terms above.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.4.0 | 2026-08-29 | Section M added, per "CEO DIRECTIVE - PERSIST AUTHORIZATION FOR PARASHARI_YOGA_V1 ADR DRAFTING": persists the owner's own "proceed" instruction, interpreted narrowly as authorization to draft the `PARASHARI_YOGA_V1` ADR only. Not a ratification; no ADR number assigned or reserved. Certification design, certification execution, implementation, and convergence integration all remain separately unauthorized. Binds any future draft to incorporate every applicable section-L correction by name; section L's own text unedited. No `engine/` file created or modified; none authorized by this section. |
| 1.3.0 | 2026-08-29 | Section L added: CEO disposition (HOLD) of a proposed `PARASHARI_YOGA_V1` ADR/certification-design draft produced and revised in conversation, never before persisted to this repository - no ADR number assigned, no ratification. Eleven specific corrections recorded verbatim in substance: production `dignity.py` barred from serving as its own certification oracle; certification-side dignity-table independence clarified as implementation-independence only, not source/edition-independence; exhaustive enumeration corrected to the real 720-case longitude/sign/house plumbing space; the Mercury-exaltation-only mutation identified as undetectable and replacement mutations specified; PyJHora confirmed optional/non-normative, limited to the two functions actually verified; the D1 calculation/house entrypoint confirmed; moolatrikona exclusion confirmed factually inert for these five yogas; certification-meaning and historical-validation-inapplicability language specified for the eventual artifact. Authorizes nothing further. |
| 1.2.0 | 2026-08-26 | Section J added: candidate-yoga decision-readiness research per explicit "CEO AUTHORIZATION - BEGIN PARASHARI YOGA V1 DECISION-READINESS" instruction (research only). Identifies Panch Mahapurusha Yoga (Ruchaka/Bhadra/Hamsa/Malavya/Sasa) as the strongest single candidate: a direct, unanimous BPHS verse for the base formation rule, computable entirely from two already-existing, already-tested primitives (`engine.astrology.dignity`, `engine.astrology.house.whole_sign_house`) with zero new astronomical or aspect calculation - architecturally simpler than KP_SIGNIFICATOR_V1. Confirms bhanga/cancellation and retrograde treatment are the genuinely contested elements (mirroring `ADR-0078`'s own already-resolved retrograde-as-disclosure pattern) and scopes them out of V1 accordingly. Confirms no direct dependency on `DP-024`/`DP-025`; neither reopened. Section K restates the exact CEO decision required for this specific candidate, without editing section I. Answers all nine of the owner's numbered decision-readiness questions. Does not draft a specification; does not authorize implementation. | 
| 1.1.0 | 2026-08-25 | Section H added: oracle-availability decision-readiness research, per explicit CEO instruction (research only). Found PyJHora already carries a dedicated 233-function yoga-detection module (`jhora/horoscope/chart/yoga.py`), each function citing a consistent, named, numbered source ("BVR-N" = B.V. Raman) - confirmed directly by inspecting the same local oracle installation already used for this project's other certifications. Materially lowers `DP-023`'s own "oracle unconfirmed" certification-difficulty assessment. Explicitly does not claim PyJHora/B.V. Raman as the normative methodology this project must adopt - independent corroboration only, per the owner's own explicit caution. Raises confidence on the revised recommendation to medium-high. Does not draft a specification; does not authorize implementation. |
| 1.0.0 | 2026-08-25 | Created. Confirms no governing decision or checklist exists for Parashari yoga methodology anywhere in this repository (unlike `D-008`/`ADR-0027` for KP significators) and zero implementing code exists. Proposes a checklist by analogy to `ADR-0027`'s own structure, explicitly flagged as unprecedented. Recommends resolving oracle availability before specification drafting, at medium confidence. Decides nothing; drafts no specification; implements nothing. |
