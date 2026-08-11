<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | DRAFT - placeholder skeleton, content pending |
| Version | 0.1.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-07-11 |
| Review cadence | TBD |

# Open Questions Register

Ambiguities are decided by the owner, never by silent assumption. Each question blocks the
artifacts listed against it. Resolution = decision log entry + this register updated.

| ID | Question | Why it matters | Blocks | Status |
|---|---|---|---|---|
| Q1 | Who are the named owners/maintainers (docs owner, engine owner, release owner)? | Accountability for a 10+ year artifact | All status headers | OPEN |
| Q2 | Branch/review model (trunk-based vs GitFlow; required reviewers; protection rules)? | Merge discipline | CONTRIBUTING.md | OPEN |
| Q3 | Versioning and release policy (repo-wide semver vs per-component; tagging; changelog scope)? | Long-term compatibility management | CHANGELOG.md, engine releases | OPEN |
| Q4 | Authoritative expansion, scope and mutual boundary of **HLKG** and **AKG**? | Two specification skeletons cannot be filled without inventing meaning | HLKG_SPEC.md, AKG_SPEC.md, knowledge/ layout | OPEN |
| Q5 | One-paragraph ratified project mission (what the system is and is not)? | Anchors MASTER_ARCHITECTURE section 1 | MASTER_ARCHITECTURE.md | OPEN |
| Q6 | May `engine/` ever read `knowledge/` at runtime, or is knowledge strictly an app-layer concern? | Hard dependency rule | MASTER_ARCHITECTURE.md section 4 | OPEN |
| Q7 | Repository license, given upstream dual-licensed dependencies (e.g. AGPL-3.0 Swiss Ephemeris) and possible commercial deployment? | Legal viability of the whole repo | LICENSE (intentionally absent until decided) | OPEN |
| Q8 | Ratified roadmap phases with entry/exit criteria? | Prevents narrative-driven "done" | PROJECT_ROADMAP.md | OPEN |
| Q9 | Should the existing certified calculation kernel (astro_kernel v1.3, Tier-0 portably certified) be imported into `engine/` as-is as the first component, and under what module name? | Avoids re-implementation; preserves certification lineage | engine/ population | OPEN |
| Q10 | CI provider and mandatory pipeline stages (validation standard is CI-ready but no provider is chosen)? | Automation of the gates | tools/, repository settings | OPEN |

## Q8 closure criteria (ADR-0021 D2)

Q8 remains **OPEN**. ADR-0020 D6 supplies a preferred domain order (FOUNDATION, JATAKA, EVIDENCE,
INTERPRETATION, CONVERGENCE, VARSHAPHAL, MUHURTA, PRASHNA, MUNDANE) and that order is explicitly
**not** authorisation to begin implementation.

Q8 closes only when the roadmap defines, for every implementation phase: prerequisites, entry
criteria, implementation scope, certification gates, exit criteria, and CEO approval requirements.

No roadmap document in this repository authorises implementation. `docs/PROJECT_ROADMAP.md`,
`docs/VARGA_CERTIFICATION_ROADMAP.md`, `docs/DASHA_CERTIFICATION_ROADMAP.md` and
`docs/PLATFORM_DOMAIN_ARCHITECTURE.md` each state orders or sequences and each says so; this note
records it at register level so the point survives reading any one of them in isolation.

## Decision papers and design proposals drafted (2026-08-11)

Drafted on CEO direction. Each presents options; none decides. All four matters remain OPEN.

| Matter | Document | Status |
|---|---|---|
| Entity identifier family and pattern | `docs/decisions/DP-008-entity-identifier-family.md` | OPEN, options presented, recommendation labelled |
| Tier classification for panchanga and rise/set | `docs/decisions/DP-009-panchanga-riseset-tier.md` | OPEN, options presented, recommendation labelled |
| Independent evidence-path representation and computation | `docs/EVIDENCE_INDEPENDENCE_DESIGN.md` | OPEN, design proposal; convergence must not be implemented on it |
| Q8 phase criteria | `docs/Q8_CLOSURE_MATRIX.md` | **Q8 REMAINS OPEN**; candidate matrix for ratification |

`docs/decisions/README.md` indexes the paper series and records that DP-001 through DP-007 are
reserved for the Phase G governance round and are not yet drafted.

## Resolution log
| ID | Resolved by | Date | Decision link |
|---|---|---|---|
| - | - | - | - |
