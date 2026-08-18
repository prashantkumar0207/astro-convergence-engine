<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | RESEARCH CLOSEOUT, **RESTORED 2026-08-18**. Non-normative per `docs/DOCUMENTATION_STANDARD.md` s1 ("Research notes... lightweight"). Section 4's original 22/22 accounting was briefly, and erroneously, superseded by section 4a's "12/22" figure on 2026-08-18; owner-directed forensic reconciliation the same day found section 4a's figure itself rested on a conflation with an unrelated 5-person pilot, and **section 4b restores the original 22/22 accounting as authoritative**, marking section 4a SUPERSEDED/RETRACTED in turn. None of the three accountings (section 4, 4a, or 4b) has been independently reproduced or re-derived by the builder from primary data within this repository. See "Evidence provenance and reproducibility" (s8) before relying on any count in this document. Companion decision record: `docs/DECISION_LOG.md` `ADR-0047` (PROPOSED, not ratified) and its two 2026-08-18 corrective addenda. |
| Version | 3.0.0 |
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

## 4. ORIGINAL CLOSEOUT (as reported 2026-08-17) - RESTORED AS AUTHORITATIVE (2026-08-18, see section 4b)

> **This section was briefly marked superseded on 2026-08-18 (by a "12/22" correction, section 4a) and
> is now restored as authoritative the same day**, after forensic reconciliation found section 4a's
> figure itself rested on a conflation with an unrelated 5-person pilot (see section 4b for the full
> restoration and explanation). The bulleted figures below are preserved exactly as originally recorded
> throughout - never edited by either correction. **See section 4b for the authoritative statement and
> the reason the intervening "12/22" correction (section 4a) does not stand.**

- **22 / 22** of the pre-registered sample were completed (no attrition).
- **16** people were classified independent of ADB, under the rules in section 3.
- **4** people matched ADB (not independent).
- **2** identities remained unresolved (lineage UNKNOWN - counted as neither independent nor matched,
  per section 3's rule).
- **14** genuinely independent, exact-day events were identified across the 16 independent people (not
  one event per person; some people contributed zero eligible events, some contributed more than one).

## 4a. SUPERSEDED / RETRACTED CORRECTION (as reported 2026-08-18, retracted later the same day)

> **This section is itself superseded and retracted - do not rely on it.** Owner-directed forensic
> reconciliation on 2026-08-18 established that the "12/22 attempted" figure below rests on
> `NEXT_CORPUS_REPORT.md`, an external file that conflated this 22-person sample with an unrelated,
> separately-run 5-person "bridging pilot" (Maldini, Impanis, Mounicq, Del Prete, Charpentier), and that
> mischaracterized four of this sample's people (Scaroni, Bacchelli, Prinzhorn, Ellinger) as never
> ADB-checked when the primary 22-person record shows all four as checked (NONMATCH). It is preserved
> here unedited, exactly as originally recorded, so the audit trail shows what was reported and later
> retracted - not silently removed. **Use section 4b instead.**

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

## 4b. RESTORED AUTHORITATIVE STATE (2026-08-18, forensic reconciliation)

**The pre-registered 22-person sample was completed in full: 22/22. Section 4a's "12/22 attempted"
figure was itself an error and is retracted (see the banner on section 4a). The original section 4
accounting, below, is restored as authoritative.**

| Category | Count | Named |
|---|---|---|
| Attempted | 22 / 22 | - |
| Independent of ADB | 16 | - |
| ADB_MATCH (not independent) | 4 | Fichera, Aimar, Serantoni, Bobet |
| Unresolved identity | 2 | Veen, Perquier |
| Independent, exact-day events | 14 | across the 16 independent people |

**Separate five-person bridging pilot, excluded from the counts above:** Maldini, Impanis, Mounicq, Del
Prete, Charpentier. This is a distinct piece of research with its own separate result; it was never
part of the pre-registered 22-person G5 sample, and the primary record for the 22-person sample states
explicitly that the pilot is "not merged into any count."

**How the error occurred:** an external file (`NEXT_CORPUS_REPORT.md`, not committed to this
repository) produced after both the 22-person closeout and the bridging-pilot report, and postdating
both, incorrectly folded two of the pilot's names (Impanis, Del Prete) into the 22-person sample's
"attempted" count and mischaracterized four of the 22-person sample's own people (Scaroni, Bacchelli,
Prinzhorn, Ellinger) as never ADB-checked, when the primary 22-person record shows all four checked
with an ADB result of NONMATCH. That file's account was the source of section 4a and the corresponding
`ADR-0047` addendum, both now retracted.

**Evidence class, unchanged:** this restoration, like sections 4 and 4a before it, is **reported, not
independently reproduced by the builder from primary records within this repository** - see section 8.
The external files reconciled to reach this restoration are not themselves added to this repository by
this correction.

## 5. Event-domain coverage observed (RESTORED - see section 4b)

> This section describes domain coverage for the 14-events/16-independent-people figures, which section
> 4b restores as authoritative after section 4a's "12/22" figure (which had superseded this section) was
> itself retracted. It is preserved unedited as historical record throughout.

The 14 independent exact-day events covered a **limited** set of domains:

- academic appointment / honor
- military / combat events
- political detention
- family events
- career / administrative / publication events

No claim is made about domains not listed above; their absence from this sample is not evidence they
are absent from the full G5 population (see section 7).

## 6. Finding and decision

> **Correction note (2026-08-18, updated 2026-08-18):** the paragraph immediately below cites "fourteen
> independent events... 22-person sample," which was briefly superseded by section 4a's "12/22" figure
> and has since been **restored as authoritative** by section 4b, after forensic reconciliation found
> section 4a's figure itself rested on a conflation with an unrelated 5-person pilot. The paragraph below
> therefore again reflects the authoritative figures directly, with no downward adjustment needed. The
> conclusion (G5 = SUPPLEMENT ONLY) was unchanged throughout both corrections; see `docs/DECISION_LOG.md`
> `ADR-0047`'s two 2026-08-18 evidence addenda.

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

- **The 22-person sample is complete: 22/22, restored (section 4b) after a brief, erroneous "12/22"
  correction (section 4a, retracted).** The full pre-registered 22 may not be extrapolated to the full
  G5 population.
- **Domain coverage is limited to what section 5 lists (restored, section 4b).** No claim is made about
  domains not listed there.
- The 2 unresolved identities (Veen, Perquier) remain unresolved, not independent, not matched.
  Resolving them is future work, not assumed in either direction.
- *(Bullets from the retracted section 4a correction, preserved as historical record only - do not
  rely on them):* "Of the corrected categories (section 4a), the 4 identity-resolved-but-ADB-unchecked
  people (Scaroni, Bacchelli, Prinzhorn, Ellinger) remain unresolved as to independence... `Mounicq`
  (NO_MATCH) and `Charpentier` (AMBIGUOUS) are their own distinct, separately-named outcomes." These
  four names and the NO_MATCH/AMBIGUOUS outcomes belonged to the conflated, retracted "12/22" accounting
  (section 4a); per section 4b, Scaroni, Bacchelli, Prinzhorn, and Ellinger are ADB-checked with a
  NONMATCH result in the restored 22-person record, and Mounicq/Charpentier are not part of the
  22-person sample at all.
- **This document does not establish, and must not be cited as, evidence of predictive accuracy** for
  any ACE calculation, rule, or methodology, under any of the three accountings (sections 4, 4a, 4b). It
  is a corpus-suitability finding only.

## 8. Evidence provenance and reproducibility

**No per-person worksheet, source-record list, or raw dataset file for this research is currently
committed to this repository**, under `research/` or elsewhere, as of this document's creation, **and
this remains true after both 2026-08-18 corrections** - the counts in section 4b are of the same
evidence class as sections 4 and 4a before them: reported, not reproduced from data committed to this
repository. The counts in sections 4-5 were recorded as **reported to the builder** in the session that
produced this closeout (2026-08-17); the counts in section 4a were reported in a correcting session
later found to be itself in error (2026-08-18); the restoration in section 4b was reached the same day
by owner-directed forensic reconciliation against primary-evidence files supplied outside this
repository (`FINAL_CLOSEOUT_22_SAMPLE.md`, `BRIDGING_MISSION_FINAL_REPORT_v2.md`,
`NEXT_CORPUS_REPORT.md`, and the `G5_CENSUS_REPORT.md` checkpoint series) - a stronger evidentiary basis
than either prior accounting, since it identifies and reads an actual itemized per-person primary
record rather than relying on a summary figure alone, but that record itself remains uncommitted to
this repository. None of the three accountings has been independently reproduced, recomputed, or
spot-checked by the builder against data committed to this repository, because that data is not present
here.

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
| 3.0.0 | 2026-08-18 | **Restoration, retracting version 2.0.0's correction.** Owner-directed forensic reconciliation against primary-evidence files supplied outside this repository (`FINAL_CLOSEOUT_22_SAMPLE.md`, `BRIDGING_MISSION_FINAL_REPORT_v2.md`, `NEXT_CORPUS_REPORT.md`, `G5_CENSUS_REPORT.md` series) established that version 2.0.0's "12/22 attempted" figure (section 4a) was itself incorrect: its source, `NEXT_CORPUS_REPORT.md`, conflated this 22-person sample with an unrelated, separately-run 5-person bridging pilot (Maldini, Impanis, Mounicq, Del Prete, Charpentier), and mischaracterized four of this sample's own people (Scaroni, Bacchelli, Prinzhorn, Ellinger) as never ADB-checked when the primary record shows all four checked (NONMATCH). Section 4a is preserved unedited and marked SUPERSEDED/RETRACTED, not deleted. New section 4b restores the original section-4 accounting as authoritative: 22/22 attempted, 16 independent, 4 ADB_MATCH (Fichera, Aimar, Serantoni, Bobet), 2 unresolved (Veen, Perquier), 14 independent exact-day events; the 5-person bridging pilot is explicitly named as separate and excluded from these counts. Section 5 (event-domain coverage) restored in step with section 4b. Sections 6-8 updated with corrective pointers reflecting the restoration; original text throughout preserved, nothing silently rewritten. Decision (G5 = SUPPLEMENT ONLY) and companion `ADR-0047` (PROPOSED, not ratified) are unchanged in substance; `ADR-0047` gained a second dated corrective addendum, not an edit to any prior text. |
| 2.0.0 | 2026-08-18 | **Correction (later found erroneous - see 3.0.0).** The 2026-08-17 completion accounting (section 4: 22/22 complete, 16 independent, 4 ADB matches, 2 unresolved, 14 independent events) was reported as an incorrect completion count; this was itself wrong. Section 4 was preserved unedited and marked SUPERSEDED (later restored, 3.0.0). New section 4a recorded a "corrected" executed state: 12/22 attempted, 4 confirmed independent (Impanis, Del Prete, Painleve, Esclangon), 2 ADB_MATCH (Maldini, Bobet), 1 NO_MATCH (Mounicq), 1 AMBIGUOUS (Charpentier), 4 identity-resolved-but-ADB-unchecked (Scaroni, Bacchelli, Prinzhorn, Ellinger), 15 unattempted - now itself superseded/retracted by 3.0.0. Section 5 marked superseded in step with section 4 (also later restored). Sections 6-8 annotated with corrective pointers, original text preserved. Decision (G5 = SUPPLEMENT ONLY) and companion `ADR-0047` (PROPOSED, not ratified) were unchanged in substance; `ADR-0047` gained its own dated corrective addendum, not an edit to its original text. |
| 1.0.0 | 2026-08-17 | Closeout recorded on request. Findings reported to the builder, not independently reproduced (section 8). Companion decision: `ADR-0047` (PROPOSED). |
