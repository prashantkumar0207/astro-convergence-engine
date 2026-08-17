<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | PROPOSED - index of decision papers. Papers present options; they decide nothing. |
| Version | 1.2.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-17 |
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
| DP-001 | Q1 named owners and the ratification mechanism | every status header; ratification of all PROPOSED ADRs | RESERVED, not drafted |
| DP-002 | Q7 repository licensing given AGPL Swiss Ephemeris | distribution and hosted deployment | RESERVED, not drafted |
| DP-003 | Q8 roadmap and build order | Phase H sequencing | RESERVED, superseded in part by ADR-0020 D6 and `docs/Q8_CLOSURE_MATRIX.md` |
| DP-004 | Q5 ratified mission | constitution sections 1, 2, 4 | RESERVED, not drafted |
| DP-005 | Q6, Q9 and the knowledge boundary | H3, H4, H5 | RESERVED, not drafted |
| DP-006 | precedence between the two decision registers | every future decision entry | RESERVED, not drafted |
| DP-007 | root D-008 disposition | KP tier sequencing | RESERVED, not drafted |
| DP-008 | entity identifier family and pattern | H0 implementation | OPEN, drafted |
| DP-009 | tier classification for panchanga and rise/set | panchanga and rise/set certification | OPEN, drafted |
| DP-010 | in-repo AI collaboration scaffolding (CLAUDE.md / skills) and repair of stale AI-role documents | `docs/PROJECT_CONSTITUTION.md` s11; `specs/CLAUDE_WORKFLOW.md`; `docs/PROJECT_MASTER.md`; the transfer-bundle handoff convention | ADDRESSED by ADR-0044, narrower than this paper's recommendation (no skills/agents/MCP; the three named stale documents were not repaired, by owner instruction) |

## Change history

| Version | Date | Change |
|---|---|---|
| 1.2.0 | 2026-08-17 | DP-010 marked ADDRESSED by ADR-0044. |
| 1.1.0 | 2026-08-14 | Allocated DP-010 before drafting, per s2's before-first-use rule. |
| 1.0.0 | 2026-08-11 | Created with DP-008 and DP-009 on CEO direction. |
