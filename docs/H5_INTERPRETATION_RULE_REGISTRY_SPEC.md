<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | ACCEPTED (`ADR-0113`, 2026-11-07). Specification only: no implementation is authorised by this document, and EVIDENCE entry needs CEO approval and the owner's explicit authorization. |
| Version | 2.0.0 |
| Owner | Project Owner (`ADR-0051` D4) |
| Last updated | 2026-11-07 |
| Review cadence | On amendment |

# H5. Interpretation Rule Registry

## 1. Purpose

The registry is the closed set of astrological rules the system is permitted to apply. If a rule is
not in it, the system cannot use it. This is what makes interpretation auditable and what stops an
LLM inventing astrology.

## 2. What a rule record must carry

A stable identifier and version. The school it belongs to, which is mandatory and never inferred.
The classical or documentary source, cited precisely enough to be checked by someone who owns the
text. The rule statement in the source's own terms, and separately the machine-applicable condition.
The activation conditions: what must be true of the chart for it to fire. The claimed effect,
polarity and domain. Known variants and disagreements, named. And its certification level.

**Variants must be named, never silently chosen.** The repository already has three live examples:
the D20 start triple, D60's even-sign reversal, and node-cast aspects in drishti. Each is a genuine
disagreement between respected sources, and the existing practice of recording the variant rather
than picking one quietly is correct and should be the registry's default behaviour.

## 3. The LLM boundary

An LLM may explain a rule, phrase its output, and help a user understand why the system said
something. It MUST NOT invent a rule, generalise a rule beyond its registered conditions, apply an
unregistered rule, or override a calculated value. This boundary is not a style preference; it is
the difference between an auditable system and a plausible-sounding one.

## 4. Rule certification

Rules need their own graded evidence, distinct from calculation certification. A rule can be
faithfully transcribed from a source and still have no demonstrated predictive value, and the
vocabulary must keep those apart. Transcription fidelity, source attribution, applicability
conditions and measured historical performance are four different claims.

The 2026-08-11 audit is instructive: the Parashari drishti offsets are transcribed four times inside
the repository and validated against a classical source zero times. Four copies is not four sources.
The registry must make that distinction structural rather than leaving it to reviewer vigilance.

## 5. Open questions requiring an owner decision

The identifier family. Whether rules are data or code, which interacts directly with DP-005 and with
the engineering constitution's principle that knowledge must never be hardcoded into algorithms, a
principle every current rule table violates by deliberate choice. How a variant is selected at
runtime, and whether a chart may be analysed under two variants simultaneously and the disagreement
surfaced, which would be the honest treatment.

## 6. Verification strategy

Refusal of unregistered rules. Source-citation completeness. A negative test proving generated text
cannot introduce a rule. Variant coverage.

## 7. Ratified decisions (ADR-0113)

This section controls. No earlier sentence conflicts with it, so nothing is superseded.

**Decided.**
- **Identity:** `RUL-\d{6}`, with each version identified separately from the rule's ID. Both are under the same
  pre-first-use governance as every new family.
- **Rules are data:** interpretation rules are data, in a pinned, schema-validated registry, reached through the
  immutable knowledge snapshot (`ADR-0112`, DP-005 D-1 and D-3). Certified calculation rule tables are unchanged.
- **Variants:** variant selection is explicit, and disagreement between variants is preserved, consistent with s2.

## 8. Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-11 | Created in the G1 work package as Phase H preparation. |
| 2.0.0 | 2026-11-07 | **Promoted to ACCEPTED by `ADR-0113`.** Additive decisions section; superseded wording named, not deleted. |
