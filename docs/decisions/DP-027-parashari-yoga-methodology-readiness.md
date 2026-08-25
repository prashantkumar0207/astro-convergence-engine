<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents readiness state and options. DECIDES NOTHING. Requires owner approval. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-25 |
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

## G. Exact CEO decision required

1. Authorize the oracle-availability research step (recommended), specification-drafting directly, or
   defer entirely.
2. If specification drafting is authorized: confirm the section C checklist (constructed by analogy, no
   precedent) as the starting structure, or direct a different one.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-25 | Created. Confirms no governing decision or checklist exists for Parashari yoga methodology anywhere in this repository (unlike `D-008`/`ADR-0027` for KP significators) and zero implementing code exists. Proposes a checklist by analogy to `ADR-0027`'s own structure, explicitly flagged as unprecedented. Recommends resolving oracle availability before specification drafting, at medium confidence. Decides nothing; drafts no specification; implements nothing. |
