<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | PROPOSED - research and planning only. No varga is authorised for implementation by this document. Pending owner ratification (docs/OPEN_QUESTIONS.md Q1). Section 5's own recommended order is this document's own unratified opinion, not a normative sequencing decision, until this document's own status changes. |
| Version | 1.0.1 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-25 (section 2's B-01/B-02 status corrected - see Change history) |
| Review cadence | TBD |

# Varga Certification Roadmap

## 1. Purpose and the rule this document exists to enforce

**GENERIC FRAMEWORK IS NOT GENERIC CERTIFICATION.**

The Generic Varga framework is infrastructure. It makes adding a varga cheap. It does not make a
varga correct, and it confers nothing on a division that has not been individually certified. Eight
divisions are certified today because eight were individually certified, not because a framework
exists.

D9 and D10 received the deepest treatment first for risk-management reasons: they already had
production implementations and had already exposed concrete correctness defects. That ordering was
about risk, not about importance. Every varga that becomes a production analytical input must
eventually receive its own certification at appropriate depth.

This document records what a new varga costs, which remaining divisions the existing contracts can
express, and in what order they are least risky to attempt. It authorises nothing.

## 2. Current state

Certified: D1 (dedicated), D9 and D10 (dedicated modules, never routed through the registry), and
D2, D3, D7, D12, D30 through the registry under the `parashara` school key. The sanctioned set is
the single constant `engine.astrology.CERTIFIED_PRODUCTION_VARGAS`. Every other division raises
`UnsupportedVargaError` by design.

Not certified and not implemented: D4, D16, D20, D24, D27, D40, D45, D60, and every non-Parashara
variant of every certified division.

Two framework defects recorded by the 2026-08-11 audit must be resolved before the next varga is
added, because both bear directly on the safety of adding one. B-01: the registry never checks that
a rule matches the division it is registered under, so a D4 served by a twelve-division rule would
be accepted silently. B-02: a certified rule can be substituted at runtime and every
non-invasiveness gate still passes, because Gate D compares registry keys and never rule content.
Neither affects any published value. Both make the next registration less safe than it looks.

**Correction (2026-08-25, see Change history v1.0.1): both are resolved.** `ADR-0049`
(`Status: ACCEPTED`, 2026-08-17) remediated B-01 (`register_varga_rule` now cross-checks
`rule.divisions`/`rule.division` against the registered division) and B-02 (`rule_content_sha256`
content-identity pinning, checked by every certifier's own Gate D). Confirmed live in current code
this correction. The paragraph above is left otherwise unedited, per this repository's practice of
correcting rather than silently rewriting stale text; this note supersedes its "must be resolved"
framing specifically for B-01/B-02. The `step`-field and payload/label-table proposals in section 3
remain undecided as of this correction - see `docs/decisions/DP-024-varga-framework-step-payload-
architecture.md`.

## 3. The two rule contracts, and what they cannot express

`CyclicVargaRule` advances the D-sign by exactly one sign per division, forward or backward, from a
per-source-sign anchor. It cannot express multi-sign steps, unequal widths, an output space smaller
than the natural cycle, or per-division direction changes.

`SegmentVargaRule` enumerates `(width, target_sign)` pairs per source sign. It can express anything
geometric, at the cost of a table proportional to twelve times the division count.

**The genuine contract gap is payload, not geometry.** `VargaClassification` carries only the
D-sign, the division index and the fraction. Several classical vargas have a named per-division
payload that is the astrological point of the division: D60's shashtiamsa deities, D16 and D20's
kalamsa and vimsamsa deities, D27's nakshatra lord. Neither rule kind nor either model can express
these. D30 escapes the problem only accidentally, because its target sign encodes its ruling planet,
so its segment table happens to be lossless.

Any of D16, D20, D27 or D60 entering production as an analytical input needs either a third contract
or an additive per-division label table. This is the most consequential architectural finding for
varga work and it should be decided before, not during, the first such varga.

**A cheap option worth its own decision:** add an optional `step: int = 1` field to
`CyclicVargaRule`. That single field collapses D3 from thirty-six cells to twenty-four, collapses D4
similarly, and absorbs every future kendra-stepped or trikona-stepped varga into the compact,
cheap-to-audit contract. It is strictly additive; existing rules keep `step=1` and hash-identical
behaviour. It is proposed here and decided nowhere.

## 4. Expressibility of the remaining divisions

Classical constructions are Parashara or BPHS unless stated. Confidence is stated for the rule
content separately from the contract shape, because those fail differently.

| Varga | Construction | Contract | Shape confidence | Content confidence |
|---|---|---|---|---|
| D4 Chaturthamsa | four parts of 7 degrees 30 minutes to the sign itself and the 4th, 7th, 10th; step +3 signs | Segment, 48 cells, or Cyclic with `step` | High | High |
| D16 Shodashamsa | sixteen parts; movable start Aries, fixed Leo, dual Sagittarius; forward one sign | Cyclic | High | High |
| D20 Vimsamsa | twenty parts; movable Aries, fixed Sagittarius, dual Leo | Cyclic | High | **Medium: the start triple is genuinely disputed**, with respected renditions giving Aries/Leo/Sagittarius instead |
| D24 Siddhamsa | twenty-four parts; odd signs start Leo, even start Cancer | Cyclic | High | High |
| D27 Bhamsa | twenty-seven parts; fiery Aries, earthy Cancer, airy Libra, watery Capricorn | Cyclic | High | High, but see the width note |
| D40 Khavedamsa | forty parts; odd Aries, even Libra | Cyclic | High | High |
| D45 Akshavedamsa | forty-five parts; movable Aries, fixed Leo, dual Sagittarius | Cyclic | High | High |
| D60 Shashtiamsa | sixty parts; Nth sign from the source, forward | Cyclic | High | **Medium: BPHS reverses the deity order for even signs, and whether the sign also reverses is genuinely disputed across implementations** |

**No new rule contract is strictly required for any of the eight.** D4 alone falls outside
`CyclicVargaRule` as it stands, and lands in `SegmentVargaRule` exactly as D3 did.

**Width note.** D27's width of 30/27 is not binary representable, the same class as D7 and D9. Expect
sweep points landing one ULP below a boundary, where the locked promote-up convention governs, and
require the independent reference to carry the tolerance explicitly rather than inheriting it.

## 5. Recommended order, by ascending risk

This is a recommendation for owner decision, not a schedule.

1. **D60**, once the even-sign reversal question is decided. Identity start, simplest shape.
2. **D16 and D45**, sharing the movable/fixed/dual start triple.
3. **D24 and D40**, the parity family.
4. **D20**, only after the disputed start triple is adjudicated and recorded.
5. **D27**, which needs the ULP-sensitive width treatment.
6. **D4**, which needs either the segment table or the `step` field decision.

**Framework work that should precede all of them:** resolve B-01 and B-02, and decide the payload
question in section 3 if any of D16, D20, D27 or D60 is intended as an analytical input rather than
a display chart.

## 6. Per-varga certification requirements

Every production varga must have all of: an authoritative classical source, an explicit school, a
frozen rule table verified cell by cell against a second independent transcription and a
re-derivation from the classical statement, a declared boundary policy, an independent reference
implementation built by a different construction, a dense sweep, a full ULP boundary battery, an
external oracle comparison with zero categorical tolerance, a protected holdout, a regeneration
runner, a collected artifact gate, provenance, an ADR, and a certification artifact.

Deviations from this list are decisions, not conveniences, and belong in an ADR.

## 7. The implementation template

The ordered file-by-file checklist derived from what D2, D3, D7, D12 and D30 each actually carry
lives in `docs/NEW_VARGA_IMPLEMENTATION_TEMPLATE.md`. It is separated because it is operational
detail that changes as the framework changes, whereas this roadmap is a statement of policy.

Two non-obvious traps recorded there and repeated here because they have bitten before: the
`CERTIFIED_PRODUCTION_VARGAS` tuple must stay in the order `registered_vargas()` returns, and adding
a varga requires re-running the **sign-convention** certifier as well as the varga's own, because
that certifier iterates the registry and its pinned hash set will otherwise raise.

## 8. What this roadmap does not authorise

No implementation. No registration. No change to any certified varga, to the framework, or to the
boundary convention. The `step` field, the payload contract and the resolution of B-01 and B-02 are
proposals requiring their own decisions.

## 9. Change history

| Version | Date | Change |
|---|---|---|
| 1.0.1 | 2026-08-25 | **Correction, not a ratification.** Section 2's claim that B-01/B-02 "must be resolved before the next varga is added" was stale - both were remediated by `ADR-0049` (`Status: ACCEPTED`, 2026-08-17), confirmed live in current `engine/astrology/varga_registry.py`/`varga_rules.py` code this correction. A note is added inline (section 2) rather than rewriting the original paragraph, per this repository's practice of correcting rather than silently editing stale text. Status header clarified: section 5's recommended order remains this document's own unratified opinion, not normative, until the document's own status changes - it is not treated as ratified by this correction. Found and corrected per `docs/decisions/DP-023-jataka-first-capability-exact-selection.md` and the owner's explicit "audit the stale VARGA_CERTIFICATION_ROADMAP.md against the accepted ADRs and correct its status only through the appropriate append-only governance mechanism" instruction (2026-08-25). No other content changed; `Status: PROPOSED` unchanged - this document remains unratified and authorises nothing, exactly as before. |
| 1.0.0 | 2026-08-11 | Created in the G1 work package from the 2026-08-11 architecture audit. |
