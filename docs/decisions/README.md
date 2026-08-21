<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | PROPOSED - index of decision papers. Papers present options; they decide nothing. |
| Version | 2.4.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-21 |
| Review cadence | TBD |

# Decision Papers

A decision paper presents a question the builder must not answer, the options with the strongest
honest case for each including options the builder does not recommend, the consequences of each, and
a recommendation labelled separately with a confidence level.

A paper is not a decision. Decisions live in `docs/DECISION_LOG.md` as ADR entries, issued by the
owner. A paper that resolves its own question has failed.

## Numbering

`DP-NNN`, allocated in this index before drafting. The family is governed by `docs/NAMING_STANDARD.md` s2 and ADR-0040; duplicate allocation is prohibited and mechanically checked by `scripts/check_identifier_families.py`.

**DP-001 through DP-007 are RESERVED** for the Phase G governance decision round planned in the
approved Phase G plan section 8: ownership and ratification, licensing, roadmap and build order,
mission, the knowledge boundary, register precedence, and the D-008 disposition. They are not yet
written. The gap below them is a reservation, not a lost paper, following the same convention the ADR
register uses for ADR-0015 through ADR-0017.

## Index

| ID | Question | Blocks | Status |
|---|---|---|---|
| DP-001 | Q1 named owners and the ratification mechanism | every status header; docs/engine/release-owner designation | **ADDRESSED by ADR-0051** (2026-08-17), accepting this paper's Option B: the ratification-mechanism half answered in part by `ADR-0033` D1 plus the 25-entry precedent; the named-owner half resolved by designating the Project Owner as interim docs/engine/release owner pending explicit delegation. The paper itself is unedited and remains on record as the options considered. |
| DP-002 | Q7 repository licensing given AGPL Swiss Ephemeris | distribution and hosted deployment | RESERVED, not drafted |
| DP-003 | Q8 roadmap and build order | Phase H sequencing | RESERVED, superseded in part by ADR-0020 D6 and `docs/Q8_CLOSURE_MATRIX.md` |
| DP-004 | Q5 ratified mission | constitution sections 1, 2, 4 | RESERVED, not drafted |
| DP-005 | Q6, Q9 and the knowledge boundary | H3, H4, H5 | RESERVED, not drafted |
| DP-006 | precedence between the two decision registers | every future decision entry | RESERVED, not drafted |
| DP-007 | root D-008 disposition | KP tier sequencing | RESERVED, not drafted |
| DP-008 | entity identifier family and pattern | H0 implementation | OPEN, drafted |
| DP-009 | tier classification for panchanga and rise/set | panchanga and rise/set certification | **ADDRESSED by ADR-0052** (2026-08-17), accepting Option B: rise/set Tier-0; panchanga Tier-1; vara explicitly straddles the boundary. The paper remains unedited as the options record. |
| DP-010 | in-repo AI collaboration scaffolding (CLAUDE.md / skills) and repair of stale AI-role documents | `docs/PROJECT_CONSTITUTION.md` s11; `specs/CLAUDE_WORKFLOW.md`; `docs/PROJECT_MASTER.md`; the transfer-bundle handoff convention | ADDRESSED by ADR-0044, narrower than this paper's recommendation (no skills/agents/MCP; the three named stale documents were not repaired, by owner instruction) |
| DP-011 | Rahu Kalam / Yamaganda / Gulika variant-table source, per `ADR-0055` item 2's authorization to draft this paper | FOUNDATION implementation scope (`Q8_CLOSURE_MATRIX.md` s4); Rahu Kalam/Yamaganda/Gulika certification | **ADDRESSED by ADR-0060** (2026-08-20), accepting Option C seeded by Option B: named, profile-selectable variants; PyJHora's convention transcribed and frozen as the seed `PYJHORA_TRIKALAM_V1`. The paper remains unedited as the options record. |
| DP-012 | Civil-date rendering methodology for dasha boundaries | FOUNDATION implementation scope (`Q8_CLOSURE_MATRIX.md` s4); any future dasha-boundary display/report | **ADDRESSED by ADR-0063** (2026-08-20), accepting Option C: deferred entirely until a consuming feature needs it. Not implementation-authorized. The paper remains unedited as the options record. |
| DP-013 | H-02 ingress-classification seam: reproduction methodology and fix option, extracted from `ADR-0020` D5's already-written analysis | FOUNDATION exit criteria (`Q8_CLOSURE_MATRIX.md` s4); MUHURTA entry criteria (s10); `TRANSIT_V1`/varga classification seam | **ADDRESSED by ADR-0064** (reproduction methodology, Option C) **and ADR-0065** (fix option, Option 1: `TransitEvent.declared_division`). The paper remains unedited as the options record. |
| DP-014 | H-01 true-node station-density gap in `find_crossings()`: whether and how to address it, extracted from `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md`'s H-01 finding | FOUNDATION exit criteria (`Q8_CLOSURE_MATRIX.md` s4); `TRANSIT_V1` true-node completeness claim | **ADDRESSED by ADR-0066** (2026-08-21), accepting Option 2: `find_crossings()` refuses `node_policy` other than mean for Rahu/Ketu via `UnsupportedNodePolicyError`. The paper remains unedited as the options record. |
| DP-015 | FOUNDATION "boundary-proximity indicators where sensitivity warrants": scope, governance status, legitimate treatment options | FOUNDATION exit criteria (`Q8_CLOSURE_MATRIX.md` s4) | OPEN, drafted |

## Change history

| Version | Date | Change |
|---|---|---|
| 2.4.0 | 2026-08-21 | Allocated and drafted DP-015 (`DP-015-foundation-boundary-proximity-indicators.md`), investigating the FOUNDATION-scope "boundary-proximity indicators where sensitivity warrants" gap. Options only; decides nothing; not implementation-authorized. |
| 2.3.0 | 2026-08-21 | DP-014 marked ADDRESSED by `ADR-0066` (Option 2 accepted: explicit refusal). |
| 2.2.0 | 2026-08-21 | Allocated and drafted DP-014 (`DP-014-h01-true-node-station-density.md`), extracting `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md`'s H-01 finding. Options only; decides nothing; not implementation-authorized. |
| 2.1.0 | 2026-08-21 | DP-013 marked ADDRESSED by `ADR-0064` (reproduction methodology) and `ADR-0065` (fix option, Option 1). |
| 2.0.0 | 2026-08-20 | Allocated and drafted DP-013 (`DP-013-h02-ingress-classification-seam.md`), extracting `ADR-0020` D5's H-02 analysis per the owner's explicit, scoped authorization. Options only; decides nothing; does not ratify `ADR-0020`. |
| 1.9.0 | 2026-08-20 | DP-012 marked ADDRESSED by `ADR-0063` (Option C accepted: deferred). |
| 1.8.0 | 2026-08-20 | Allocated and drafted DP-012 (`DP-012-civil-date-rendering-dasha-boundaries.md`), per the owner's "if a decision paper is required before implementation, draft that decision paper and register it" instruction. Options only; decides nothing. |
| 1.7.0 | 2026-08-20 | DP-011 marked ADDRESSED by `ADR-0060` (Option C seeded by Option B accepted). |
| 1.6.0 | 2026-08-19 | Allocated and drafted DP-011 (`DP-011-rahu-kalam-yamaganda-gulika-variant-tables.md`), per `ADR-0055` item 2's authorization. Options only; decides nothing. |
| 1.5.0 | 2026-08-17 | DP-009 marked ADDRESSED by `ADR-0052` (Option B accepted). |
| 1.4.0 | 2026-08-17 | DP-001 marked ADDRESSED by `ADR-0051` (Option B accepted). |
| 1.3.0 | 2026-08-17 | DP-001 drafted (`DP-001-owner-ratification-and-mechanism.md`), status RESERVED -> OPEN, drafted. |
| 1.2.0 | 2026-08-17 | DP-010 marked ADDRESSED by ADR-0044. |
| 1.1.0 | 2026-08-14 | Allocated DP-010 before drafting, per s2's before-first-use rule. |
| 1.0.0 | 2026-08-11 | Created with DP-008 and DP-009 on CEO direction. |
