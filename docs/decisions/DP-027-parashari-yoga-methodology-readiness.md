<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents readiness state and options. DECIDES NOTHING. Requires owner approval. |
| Version | 1.1.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-25 (section H added: oracle-availability decision-readiness research, per explicit CEO instruction - research only, no specification or implementation authorized) |
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

## Change history

| Version | Date | Change |
|---|---|---|
| 1.1.0 | 2026-08-25 | Section H added: oracle-availability decision-readiness research, per explicit CEO instruction (research only). Found PyJHora already carries a dedicated 233-function yoga-detection module (`jhora/horoscope/chart/yoga.py`), each function citing a consistent, named, numbered source ("BVR-N" = B.V. Raman) - confirmed directly by inspecting the same local oracle installation already used for this project's other certifications. Materially lowers `DP-023`'s own "oracle unconfirmed" certification-difficulty assessment. Explicitly does not claim PyJHora/B.V. Raman as the normative methodology this project must adopt - independent corroboration only, per the owner's own explicit caution. Raises confidence on the revised recommendation to medium-high. Does not draft a specification; does not authorize implementation. |
| 1.0.0 | 2026-08-25 | Created. Confirms no governing decision or checklist exists for Parashari yoga methodology anywhere in this repository (unlike `D-008`/`ADR-0027` for KP significators) and zero implementing code exists. Proposes a checklist by analogy to `ADR-0027`'s own structure, explicitly flagged as unprecedented. Recommends resolving oracle availability before specification drafting, at medium confidence. Decides nothing; drafts no specification; implements nothing. |
