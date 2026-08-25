<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents options. DECIDES NOTHING. Requires owner approval. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-25 |
| Review cadence | TBD |

# DP-024. Varga framework architecture: the `step`-field and payload/label-table questions

## 0. Authorization and scope

Authorized by the owner's "CEO direction — proceed with DP-023 resolution" instruction (2026-08-25),
item 1: "Resolve the Varga framework step/payload-table architecture question in a narrow decision
paper/ADR if still genuinely open." This paper investigates whether that question is resolvable from
existing accepted decisions and repository evidence alone; if not, it presents options without deciding.
It does not implement anything and does not modify `engine/astrology/varga_rules.py` or
`varga_registry.py`.

## 1. Exact governing text

`docs/VARGA_CERTIFICATION_ROADMAP.md` (`Status: PROPOSED`, v1.0.0, 2026-08-11, unratified) section 3,
quoted in full:

> **The genuine contract gap is payload, not geometry.** `VargaClassification` carries only the D-sign,
> the division index and the fraction. Several classical vargas have a named per-division payload that
> is the astrological point of the division: D60's shashtiamsa deities, D16 and D20's kalamsa and
> vimsamsa deities, D27's nakshatra lord. Neither rule kind nor either model can express these... Any of
> D16, D20, D27 or D60 entering production as an analytical input needs either a third contract or an
> additive per-division label table. This is the most consequential architectural finding for varga work
> and it should be decided before, not during, the first such varga.
>
> **A cheap option worth its own decision:** add an optional `step: int = 1` field to `CyclicVargaRule`.
> That single field collapses D3 from thirty-six cells to twenty-four, collapses D4 similarly, and
> absorbs every future kendra-stepped or trikona-stepped varga into the compact, cheap-to-audit contract.
> It is strictly additive; existing rules keep `step=1` and hash-identical behaviour. It is proposed here
> and decided nowhere.

## 2. Whether either question is resolvable from existing accepted decisions

**Confirmed not resolved, by direct search:** no entry in `docs/DECISION_LOG.md` addresses either the
`step`-field proposal or the payload/label-table proposal (searched for "step field," "payload," "label
table," "VargaClassification" - no matches). Confirmed directly against live code: `CyclicVargaRule`
(`engine/astrology/varga_rules.py`) carries only `divisions`, `start_sign`, and `direction` - no `step`
field exists. `VargaClassification`'s own shape was not independently re-inspected line-by-line this
task, but the roadmap's own claim ("carries only the D-sign, the division index and the fraction") is
consistent with every certified varga's own output shape reviewed across this session's prior work.

**Both questions are genuinely open** - they are architecture/API design choices affecting how future
divisions get expressed, not astrological methodology disputes, but no existing ADR settles either.

## 3. Whether either question blocks D45 specifically

**Confirmed it does not, on both counts.** D45 (Akshavedamsa) is not named in the payload/label-table
list (only D16, D20, D27, D60 carry a named per-division deity/lord payload per section 3's own text);
D45 uses a plain `CyclicVargaRule` with a uniform 30/45-degree segment width and a standard movable/
fixed/dual start-triple offset (confirmed independently against PyJHora's own `akshavedamsa_chart`
implementation, chart_method=1 - see `ADR-0076`'s own readiness audit for the exact cross-check), needing
neither a multi-sign step nor a per-division label. **D45's own implementation-readiness work does not
depend on resolving either question in this paper.**

## 4. Options, for whichever question the owner wishes to resolve now

**A. The `step`-field question:**
- Option A1: add the proposed `step: int = 1` field to `CyclicVargaRule` now, additive, `step=1`
  everywhere existing, hash-identical behaviour for all five currently-certified registry vargas.
  Benefits D4 (needs a 3-sign step) and any future kendra/trikona-stepped division.
  - Consequence: a schema change to a shared contract, needing its own ADR and a negative-control
    proving existing certified vargas are unaffected, before any division uses it.
- Option A2: defer. D4 can use `SegmentVargaRule` instead (48 cells, "exactly as D3 did" per the
  roadmap's own text) without the new field, at the cost of a larger, harder-to-audit table.
- Option A3: decide only when D4 is actually proposed as a capability - narrowest scope, defers the
  schema-change ceremony until it is load-bearing.

**B. The payload/label-table question:**
- Option B1: add a third rule contract (a payload-carrying variant) before any of D16/D20/D27/D60 is
  proposed.
- Option B2: add an additive per-division label table, separate from the geometric rule, attached
  post-hoc to a `VargaClassification` result.
- Option B3: decide only when one of D16/D20/D27/D60 is actually proposed as a capability - matches
  Option A3's own reasoning; the roadmap's own text calls this "the most consequential architectural
  finding," suggesting it deserves real deliberation, which arguably favors deciding it deliberately
  rather than under the pressure of an already-chosen capability's own implementation.

## 5. Recommendation and confidence

**At medium confidence:** Option A3/B3 (defer both, decide when the relevant division is actually
proposed) is recommended for D45's own near-term path, since neither question blocks it and manufacturing
an architecture decision for divisions not yet authorized risks exactly the kind of premature
specification this project's own governance culture cautions against. **If the owner intends D16, D20,
D27, D60, or D4 to follow D45 soon**, resolving the relevant question now (B1/B2 for the payload
question; A1/A2 for the step question) would remove a known future blocker in advance - a legitimate,
different priority the owner may weigh differently.

## 6. Explicit non-claims

This paper does not choose between A1/A2/A3 or B1/B2/B3. It does not modify `varga_rules.py`,
`varga_registry.py`, or any certified varga. It does not authorize D16, D20, D27, D60, or D4 for
implementation. It does not affect D45's own readiness, confirmed independent of this question in
section 3.

## 7. Exact CEO decision required

1. Resolve now (select A1/A2/A3 and B1/B2/B3), or explicitly defer both until the relevant division is
   proposed (matching the recommendation in section 5).
2. Confirm D45's own implementation-readiness path (`ADR-0076`) is unaffected by this paper's own
   resolution, either way.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-25 | Created. Confirms the `docs/VARGA_CERTIFICATION_ROADMAP.md` section 3 `step`-field and payload/label-table questions are genuinely open (no ADR resolves either; confirmed directly against `docs/DECISION_LOG.md` and live `engine/astrology/varga_rules.py` code), and confirms neither blocks D45 specifically. Presents options for both without deciding; recommends deferring both until the relevant division is actually proposed, at medium confidence. Decides nothing; no code touched; no capability implementation authorized. |
