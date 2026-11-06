<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents options and recommends one. DECIDES NOTHING. Requires owner approval. |
| Version | 1.0.0 |
| Owner | Project Owner (`ADR-0051` D4) |
| Last updated | 2026-11-06 |
| Review cadence | On decision |

# DP-005. The knowledge boundary for the question, evidence and interpretation layers (H3, H4, H5)

## 1. The question

`docs/decisions/README.md` reserved this paper for "Q6, Q9 and the knowledge boundary", as the blocker for H3, H4 and H5.
`ADR-0111` has now settled Q6 and Q9. This paper asks only what those rulings leave open for the layers that will
consume knowledge.

## 2. Already decided, and not reopened here

| Settled point | Authority |
|---|---|
| `engine/` must not have an uncontrolled runtime dependency on top-level `knowledge/`. A controlled interface needs its own decision, defining version pinning, schema validation, failure behaviour and certification effect | `ADR-0030` clause 1, ratified by `ADR-0111` |
| `engine/knowledge/` is implementation-owned rule data, and is permitted | `ADR-0024` D2, ratified by `ADR-0111` |
| `engine/` is the authoritative certified kernel. `legacy/` is retained, and retiring it needs separate authorization and completed migration certification | `ADR-0030` clause 2 (a) to (c), ratified by `ADR-0111` |
| The top-level directory set is closed and decision-governed | `ADR-0041` |
| Persisted entities use `ENT-00000001` identifiers | `ADR-0111` (DP-008 Option B) |

`ADR-0024` D3 (dependency direction) and D4 ("future inference, question and convergence layers MAY consume governed
knowledge") are **not** ratified. D4 is the gap this paper exists to close.

## 3. The decisions that are genuinely missing

### D-1. May H3, H4 and H5 consume top-level `knowledge/` at runtime?

- **Option A. No.** These layers use only implementation-owned data, as `engine/` does today.
- **Option B. Yes, through one controlled interface,** specified to `ADR-0030` clause 1's four requirements, and read live.
- **Option C. Yes, through a pinned snapshot.** A versioned snapshot of the knowledge used is fixed at build time, and each
  evidence item records its content hash in provenance.

**Recommendation: C.** It meets clause 1, and it keeps the reproducibility that H4 s5 asks about: evidence can be audited
against the exact knowledge that produced it. This repository already pins rule content by hash with
`rule_content_sha256` for the varga rules and the KP and Yoga rules. B gives live reads, but makes evidence depend on a
moving source. A rules out governed knowledge altogether, which H5 needs for interpretation rules.

### D-2. Where do the H4 and H5 layers live?

- **Option A. Inside `engine/`,** for example `engine/evidence/`, bound by `ADR-0030` clause 1 and reaching knowledge only
  through D-1.
- **Option B. In a new top-level package,** which `ADR-0041` would need to authorize.

**Recommendation: A.** The certification, provenance and C4 machinery already covers `engine/`, and a new top-level
package adds governance cost for no gain at entry.

### D-3. Are interpretation rules data or code? (H5 s5)

- **Option A. Data:** a schema-validated rule registry under D-1, each rule carrying its identifier and content hash.
- **Option B. Code:** Python rule tables with pinned content hashes, the current practice for certified rule tables.
- **Option C. Data for interpretation rules, while certified calculation rule tables stay as they are.**

**Recommendation: C.** Interpretation rules are what the registry exists to govern, and the engineering constitution's
principle that knowledge is not hard-coded applies to them directly. Leaving the certified calculation tables untouched
avoids recertifying anything to satisfy a new layer.

## 4. What this paper does not do

It decides nothing. It reopens neither Q6 nor Q9. It does not cover H3's other content: H3 is not an EVIDENCE entry
criterion. It authorizes no implementation, no top-level directory and no interface.

## 5. Exact owner decision required

Choose an option for each of D-1, D-2 and D-3, to be recorded in one ADR. The recommendation is C, A and C.

## 6. Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-11-06 | Drafted under `ADR-0111`, on the identifier registered in `docs/decisions/README.md`. Decides nothing. |
