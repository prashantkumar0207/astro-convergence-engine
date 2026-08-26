<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents readiness state and options. DECIDES NOTHING. Requires owner approval. |
| Version | 1.2.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-26 (section J added: candidate-yoga decision-readiness research per explicit "CEO AUTHORIZATION - BEGIN PARASHARI YOGA V1 DECISION-READINESS" instruction - research only, no specification or implementation authorized; section K restates the exact CEO decision required, superseding section I for this narrower candidate) |
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

## Change history

| Version | Date | Change |
|---|---|---|
| 1.2.0 | 2026-08-26 | Section J added: candidate-yoga decision-readiness research per explicit "CEO AUTHORIZATION - BEGIN PARASHARI YOGA V1 DECISION-READINESS" instruction (research only). Identifies Panch Mahapurusha Yoga (Ruchaka/Bhadra/Hamsa/Malavya/Sasa) as the strongest single candidate: a direct, unanimous BPHS verse for the base formation rule, computable entirely from two already-existing, already-tested primitives (`engine.astrology.dignity`, `engine.astrology.house.whole_sign_house`) with zero new astronomical or aspect calculation - architecturally simpler than KP_SIGNIFICATOR_V1. Confirms bhanga/cancellation and retrograde treatment are the genuinely contested elements (mirroring `ADR-0078`'s own already-resolved retrograde-as-disclosure pattern) and scopes them out of V1 accordingly. Confirms no direct dependency on `DP-024`/`DP-025`; neither reopened. Section K restates the exact CEO decision required for this specific candidate, without editing section I. Answers all nine of the owner's numbered decision-readiness questions. Does not draft a specification; does not authorize implementation. | 
| 1.1.0 | 2026-08-25 | Section H added: oracle-availability decision-readiness research, per explicit CEO instruction (research only). Found PyJHora already carries a dedicated 233-function yoga-detection module (`jhora/horoscope/chart/yoga.py`), each function citing a consistent, named, numbered source ("BVR-N" = B.V. Raman) - confirmed directly by inspecting the same local oracle installation already used for this project's other certifications. Materially lowers `DP-023`'s own "oracle unconfirmed" certification-difficulty assessment. Explicitly does not claim PyJHora/B.V. Raman as the normative methodology this project must adopt - independent corroboration only, per the owner's own explicit caution. Raises confidence on the revised recommendation to medium-high. Does not draft a specification; does not authorize implementation. |
| 1.0.0 | 2026-08-25 | Created. Confirms no governing decision or checklist exists for Parashari yoga methodology anywhere in this repository (unlike `D-008`/`ADR-0027` for KP significators) and zero implementing code exists. Proposes a checklist by analogy to `ADR-0027`'s own structure, explicitly flagged as unprecedented. Recommends resolving oracle availability before specification drafting, at medium confidence. Decides nothing; drafts no specification; implements nothing. |
