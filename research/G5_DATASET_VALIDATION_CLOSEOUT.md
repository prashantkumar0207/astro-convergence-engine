<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | RESEARCH CLOSEOUT, REPORTED. Non-normative per `docs/DOCUMENTATION_STANDARD.md` s1 ("Research notes... lightweight"). The findings below are recorded as reported to the builder in the session that closed this research; they have **not** been independently reproduced or re-derived by the builder from primary data, because no per-person worksheet or underlying dataset file is currently present in this repository. See "Evidence provenance and reproducibility" below before relying on any count in this document. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-17 |
| Review cadence | TBD |

# G5 dataset: historical-validation suitability research, closeout

## 0. Naming disambiguation - read this first

**"G5" here names a historical-validation dataset under research.** It is unrelated to, and must not
be confused with, "G5" as used in `docs/Q8_CLOSURE_MATRIX.md` ("G5 certification taxonomy"), which is
an item in the Phase G governance work breakdown (G1-G7) and refers to nothing described in this
document. The collision is coincidental. Neither identifier is renamed by this document; both remain
as they are used in their respective contexts. A reader encountering "G5" elsewhere in this repository
should check which of the two is meant from context, since this repository currently has no naming
convention that prevents the collision (`docs/NAMING_STANDARD.md` s2's ID-Families table does not cover
free-text research/roadmap labels of this kind).

**"ADB"** is used throughout this document as given to the builder: a comparison/reference database
against which candidate G5 records were checked for overlap. Its full name and provenance are **not**
independently confirmed or documented elsewhere in this repository as of this writing. If a canonical
definition, URL, or licensing note for ADB exists outside this repository, it should be added here (or
to a dedicated reference document) before this closeout is relied on for anything beyond what is stated.

## 1. What was tested

Whether the G5 dataset is suitable to serve as ACE's **primary** historical-validation benchmark: a
protected corpus of birth-data-linked, independently-verifiable, exact-day historical events, spanning
multiple domains, sufficient in density and independence to support `docs/VALIDATION_STANDARD.md`-class
protected-holdout validation.

## 2. Sample definition

A **fixed, pre-registered sample of 22 people** was drawn from the publicly accessible G5 dataset before
evaluation began (pre-registration is what makes the completion count below meaningful rather than a
stopping point chosen after seeing results). The full per-person worksheet (identities, source records,
lineage assessment, event lists) is **not currently committed to this repository** - see section 8.

## 3. Independence and lineage rules applied

Per person, and per candidate event, an explicit lineage/independence assessment was required rather
than assumed. This follows the same discipline `docs/H4_EVIDENCE_MODEL_SPEC.md` s10 and
`docs/EVIDENCE_INDEPENDENCE_DESIGN.md` already establish for evidence relationships in this repository
(INDEPENDENT / DERIVED / SHARED-ORIGIN / CORRELATED / CONFLICTING), adapted here to a data-provenance
question rather than an astrological-evidence-relationship question:

- A person/event is **independent of ADB** only when its lineage is explicitly established as such -
  not merely because it appears on a different website, and not merely because it is publicly
  accessible.
- A person/event whose lineage relative to ADB is **unknown remains UNKNOWN** and is never counted as
  independent. This mirrors `docs/H4_EVIDENCE_MODEL_SPEC.md` s10's rule that an unmeasured relationship
  must not default to independent, "because it would overstate confidence in exactly the situations
  where correlation is most likely."
- Agreement between a G5 record and the corresponding ADB record is **not** treated as independent
  confirmation of either.
- Every event counted as evidence requires an **exact day**, not an approximate date, to be eligible.

## 4. Final counts, as reported

- **22 / 22** of the pre-registered sample were completed (no attrition).
- **16** people were classified independent of ADB, under the rules in section 3.
- **4** people matched ADB (not independent).
- **2** identities remained unresolved (lineage UNKNOWN - counted as neither independent nor matched,
  per section 3's rule).
- **14** genuinely independent, exact-day events were identified across the 16 independent people (not
  one event per person; some people contributed zero eligible events, some contributed more than one).

## 5. Event-domain coverage observed

The 14 independent exact-day events covered a **limited** set of domains:

- academic appointment / honor
- military / combat events
- political detention
- family events
- career / administrative / publication events

No claim is made about domains not listed above; their absence from this sample is not evidence they
are absent from the full G5 population (see section 7).

## 6. Finding and decision

**The research did not establish sufficient independent, exact-day, multi-domain event coverage for G5
to serve as ACE's primary historical-validation benchmark.** Fourteen independent events across five
domain categories, drawn from a 22-person sample, is evidence of *some* independent signal, not of the
breadth and density a primary protected-validation corpus requires under
`docs/VALIDATION_STANDARD.md`.

**Decision: G5 = SUPPLEMENT ONLY.** Recorded normatively in `docs/DECISION_LOG.md` ADR-0047 (status
PROPOSED at the time of this closeout - see that entry for the binding decision text, permitted uses,
and prohibited uses; this document is the supporting research record, not the decision itself).

## 7. Limitations

- **The 22-person sample must not be extrapolated to the full G5 population.** It establishes what was
  found in this specific pre-registered sample, not a population-level independence or event-density
  rate.
- **Domain coverage is limited to what section 5 lists.** No inference should be drawn about domains
  outside that list.
- **The 2 unresolved identities remain unresolved**, not independent, not matched. Resolving them is
  future work, not assumed in either direction.
- **This document does not establish, and must not be cited as, evidence of predictive accuracy** for
  any ACE calculation, rule, or methodology. It is a corpus-suitability finding only.

## 8. Evidence provenance and reproducibility

**No per-person worksheet, source-record list, or raw dataset file for this research is currently
present in this repository**, under `research/` or elsewhere, as of this document's creation. The
counts in sections 4-5 are recorded here as **reported to the builder** in the session that produced
this closeout (2026-08-17) and have **not** been independently reproduced, recomputed, or spot-checked
by the builder against primary source records, for the direct reason that those records are not
available in this environment.

This evidence class is stated explicitly, following the precedent already established in this
repository for reported-but-not-independently-observed evidence (see
`docs/CI_AND_ORACLE_REPRODUCIBILITY_SPEC.md` s7.1's `CEO_REPORTED` evidence class for the same
reasoning applied to a different claim). It is not a criticism of the underlying research; it is a
statement of what this repository can and cannot currently verify about it.

**If the underlying per-person worksheet exists outside this repository, it should be added under
`research/` alongside this document**, so a future independent auditor (per
`docs/PROJECT_CONSTITUTION.md` s11) can re-derive sections 4-5 rather than take them on report. Until
then, any use of this document as evidence in a certification or decision context should cite it as
**reported, not reproduced**.

## 9. Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-17 | Closeout recorded on request. Findings reported to the builder, not independently reproduced (section 8). Companion decision: `ADR-0047` (PROPOSED). |
