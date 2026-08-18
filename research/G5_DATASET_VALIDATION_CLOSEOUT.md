<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | RESEARCH CLOSEOUT, **CORRECTED 2026-08-18**. Non-normative per `docs/DOCUMENTATION_STANDARD.md` s1 ("Research notes... lightweight"). The originally-reported completion accounting (section 4) was subsequently identified as incorrect and **must not be relied upon as verified evidence**; section 4a is the corrected executed state. Neither the original nor the corrected counts have been independently reproduced or re-derived by the builder from primary data, because no per-person worksheet or underlying dataset file is currently present in this repository. See "Evidence provenance and reproducibility" (s8) before relying on any count in this document. Companion decision record: `docs/DECISION_LOG.md` `ADR-0047` (PROPOSED, not ratified) and its 2026-08-18 corrective addendum. |
| Version | 2.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-18 |
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

## 4. SUPERSEDED / INCORRECTLY REPORTED CLOSEOUT (as reported 2026-08-17)

> **This section is superseded and must not be relied upon as verified evidence.** The completion
> count below was subsequently identified as incorrect: the sample was **not** 22/22 complete. It is
> preserved here unedited, exactly as originally recorded, so the audit trail shows what was reported
> and later found wrong - not silently converted to the corrected figures. **Use section 4a instead.**

- **22 / 22** of the pre-registered sample were completed (no attrition).
- **16** people were classified independent of ADB, under the rules in section 3.
- **4** people matched ADB (not independent).
- **2** identities remained unresolved (lineage UNKNOWN - counted as neither independent nor matched,
  per section 3's rule).
- **14** genuinely independent, exact-day events were identified across the 16 independent people (not
  one event per person; some people contributed zero eligible events, some contributed more than one).

## 4a. CORRECTED EXECUTED STATE (2026-08-18)

**The pre-registered sample was 22 people. Only 12 of those 22 were actually attempted. The sample is
NOT 22/22 complete and must never again be described as such.**

| Category | Count | Named |
|---|---|---|
| Attempted | 12 / 22 | - |
| Confirmed independent of ADB | 4 | Impanis, Del Prete, Painleve, Esclangon |
| ADB_MATCH (not independent) | 2 | Maldini, Bobet |
| NO_MATCH | 1 | Mounicq |
| AMBIGUOUS | 1 | Charpentier |
| Identity-resolved, ADB never checked | 4 | Scaroni, Bacchelli, Prinzhorn, Ellinger |
| Unattempted | 15 | - |

**The four identity-resolved-but-ADB-unchecked people (Scaroni, Bacchelli, Prinzhorn, Ellinger) are NOT
independent.** Per section 3's own rule, an unmeasured/unchecked relationship is UNKNOWN, never
independent by default. They must not be added to the confirmed-independent count of 4 for any purpose.

**No event-level data accompanies this correction.** The prior "14 independent exact-day events" figure
(section 4) was derived from the now-superseded 16-independent-people figure and does not survive this
correction; no corrected event count or event-domain breakdown was supplied, and none is invented here.
Section 5 below is therefore also superseded, not merely section 4.

Explicitly, per the correction instruction:

- **The per-person worksheet is not currently present in this repository** (unchanged from the original
  closeout - see section 8).
- **These corrected counts remain research-reported, not independently reproduced from underlying raw
  data**, by the builder, from primary source records - the identical evidence-class limitation section
  8 already states for the original (now-superseded) figures.
- **No population-level G5 independence rate may be inferred** from either the original or the
  corrected 22-person sample.
- **No predictive-accuracy claim follows from this research**, in its original or corrected form.

## 5. Event-domain coverage observed (SUPERSEDED - see section 4a)

> This section describes domain coverage for the 14-events/16-independent-people figures that section 4a
> supersedes. It is preserved unedited as historical record. No corrected event-domain breakdown is
> available; none is invented here.

The 14 independent exact-day events covered a **limited** set of domains:

- academic appointment / honor
- military / combat events
- political detention
- family events
- career / administrative / publication events

No claim is made about domains not listed above; their absence from this sample is not evidence they
are absent from the full G5 population (see section 7).

## 6. Finding and decision

> **Correction note (2026-08-18):** the paragraph immediately below cites the now-superseded "fourteen
> independent events... 22-person sample" figures from section 4. It is preserved unedited as the
> historical record of the original finding's stated reasoning. The corrected sample (section 4a: 12/22
> attempted, 4 confirmed independent) is smaller than what this paragraph describes, which supports the
> same conclusion at least as strongly - a smaller confirmed-independent sample is weaker, not stronger,
> grounds for treating G5 as a primary benchmark. The conclusion itself (G5 = SUPPLEMENT ONLY) is
> unchanged by this correction; see `docs/DECISION_LOG.md` `ADR-0047`'s 2026-08-18 evidence addendum.

**The research did not establish sufficient independent, exact-day, multi-domain event coverage for G5
to serve as ACE's primary historical-validation benchmark.** Fourteen independent events across five
domain categories, drawn from a 22-person sample, is evidence of *some* independent signal, not of the
breadth and density a primary protected-validation corpus requires under
`docs/VALIDATION_STANDARD.md`.

**Decision: G5 = SUPPLEMENT ONLY.** Recorded normatively in `docs/DECISION_LOG.md` ADR-0047 (status
PROPOSED - not owner-ratified, not a certification decision - see that entry and its 2026-08-18
corrective addendum for the binding decision text, permitted uses, prohibited uses, and the corrected
evidentiary basis; this document is the supporting research record, not the decision itself).

## 7. Limitations

- **Corrected 2026-08-18: the 22-person sample was only 12/22 attempted, not complete.** Neither the
  attempted 12 nor the full pre-registered 22 may be extrapolated to the full G5 population. See
  section 4a.
- **Domain coverage is limited to what section 5 lists, and section 5 is itself superseded (section
  4a).** No corrected domain-coverage inference is available; none should be drawn from either the
  original or the corrected counts.
- *(Superseded original bullet, preserved as historical record - see section 4a for the corrected
  categories instead):* "The 2 unresolved identities remain unresolved, not independent, not matched.
  Resolving them is future work, not assumed in either direction."
- **Of the corrected categories (section 4a), the 4 identity-resolved-but-ADB-unchecked people
  (Scaroni, Bacchelli, Prinzhorn, Ellinger) remain unresolved as to independence** - UNKNOWN, not
  independent, not matched. `Mounicq` (NO_MATCH) and `Charpentier` (AMBIGUOUS) are their own distinct,
  separately-named outcomes, not merged into "unresolved." Resolving any of these is future work, not
  assumed in either direction.
- **This document does not establish, and must not be cited as, evidence of predictive accuracy** for
  any ACE calculation, rule, or methodology, under either the original or the corrected accounting. It
  is a corpus-suitability finding only.

## 8. Evidence provenance and reproducibility

**No per-person worksheet, source-record list, or raw dataset file for this research is currently
present in this repository**, under `research/` or elsewhere, as of this document's creation, **and
this remains true after the 2026-08-18 correction** - the corrected counts in section 4a are of the
same evidence class as the original, superseded counts in sections 4-5: reported, not reproduced. The
counts in sections 4-5 are recorded here as **reported to the builder** in the session that produced
this closeout (2026-08-17), later identified as an incorrect completion accounting; the counts in
section 4a are recorded as reported in the correcting session (2026-08-18). Neither has been
independently reproduced, recomputed, or spot-checked by the builder against primary source records,
for the direct reason that those records are not available in this environment.

This evidence class is stated explicitly, following the precedent already established in this
repository for reported-but-not-independently-observed evidence (see
`docs/CI_AND_ORACLE_REPRODUCIBILITY_SPEC.md` s7.1's `CEO_REPORTED` evidence class for the same
reasoning applied to a different claim). It is not a criticism of the underlying research; it is a
statement of what this repository can and cannot currently verify about it.

**If the underlying per-person worksheet exists outside this repository, it should be added under
`research/` alongside this document**, so a future independent auditor (per
`docs/PROJECT_CONSTITUTION.md` s11) can re-derive sections 4a/5 rather than take them on report. Until
then, any use of this document as evidence in a certification or decision context should cite it as
**reported, not reproduced** - and, as of 2026-08-18, must cite section 4a's corrected counts, not
section 4's superseded ones.

## 9. Change history

| Version | Date | Change |
|---|---|---|
| 2.0.0 | 2026-08-18 | **Correction.** The 2026-08-17 completion accounting (section 4: 22/22 complete, 16 independent, 4 ADB matches, 2 unresolved, 14 independent events) was identified as an incorrect completion count and must not be relied upon as verified evidence. Section 4 is preserved unedited and marked SUPERSEDED, not deleted or silently rewritten. New section 4a records the corrected executed state: 12/22 attempted, 4 confirmed independent (Impanis, Del Prete, Painleve, Esclangon), 2 ADB_MATCH (Maldini, Bobet), 1 NO_MATCH (Mounicq), 1 AMBIGUOUS (Charpentier), 4 identity-resolved-but-ADB-unchecked and therefore NOT independent (Scaroni, Bacchelli, Prinzhorn, Ellinger), 15 unattempted. Section 5 (event-domain coverage) marked superseded in step with section 4, since it was derived from the same wrong figures; no corrected event-level data was supplied or invented. Sections 6-8 annotated with corrective pointers, original text preserved. Decision (G5 = SUPPLEMENT ONLY) and companion `ADR-0047` (PROPOSED, not ratified) are unchanged in substance; `ADR-0047` gained its own dated corrective addendum, not an edit to its original text. |
| 1.0.0 | 2026-08-17 | Closeout recorded on request. Findings reported to the builder, not independently reproduced (section 8). Companion decision: `ADR-0047` (PROPOSED). |
