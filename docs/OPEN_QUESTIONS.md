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

## Resolution log
| ID | Resolved by | Date | Decision link |
|---|---|---|---|
| - | - | - | - |
