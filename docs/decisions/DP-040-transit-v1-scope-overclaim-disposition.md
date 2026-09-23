<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Per-callable disposition analysis for the three `TRANSIT_V1` SCOPE OVERCLAIMS. **DECIDES NOTHING.** Requires owner adjudication. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-09-23 |
| Review cadence | TBD |

# DP-040. Disposition of the three `TRANSIT_V1` SCOPE OVERCLAIMS: `returns()`, `natal_conjunctions()`, `transit_view()`

Written under the owner's "CEO AUTHORIZATION — AUTHORIZE P-1 DECISION PAPER ONLY" instruction, which
directed a decision paper only and expressly forbade implementing `C2`-`C5`, changing `TRANSIT_V1`
code, or changing any certification artifact. `DP-040`'s identifier was allocated in
`docs/decisions/README.md` before this paper's substantive content was written, per `ADR-0040`.
**That ordering is not independently proven by the commit graph:** the index row and this paper were
committed together, so the repository evidences only that both exist, not the sequence in which they
were produced. All evidence below was measured against `main` at
`d7092cb3236e3b9fafb7511cddf5bcfdef1ae638`.

**The prior "all three are delegators" framing is not assumed.** Each callable was read at source and
analysed independently. **One of the three is a pure delegator. Two are not.** That is the finding
this paper exists to place on the record.

**This paper decides nothing and selects no option.**

---

## 1. Shared facts, measured

**No `TRANSIT_V1` gate exercises any of the three.** This is established at import level, not by word
matching: `scripts/certify_transits.py` L51-L52 imports exactly

```
from engine.transits.crossing import RESIDUAL_BOUND_ARCSEC, find_crossings
from engine.transits.events import nakshatra_ingresses, sign_ingresses
```

`returns`, `natal_conjunctions` and `transit_view` are **not imported by the certifier at all**, so no
gate body can reach them. The four gates are `A_residual_battery` (L138), `C_oracle_anchors` (L154),
`D_independent_validator` (L233) and `E_declared_division` (L242).

**The independent validator does not cover them either.** `validate_transits_holdout.py` L23-L24
imports only `find_crossings`, `nakshatra_ingresses` and `sign_ingresses`, each marked `# SUBJECT`.
Gate `D_independent_validator` therefore adds no coverage for the three.

**Artifact state at `d7092cb3`**, read live from `certification/TRANSIT_V1_certification.json`:

| Field | Value |
|---|---|
| `adr` | `ADR-0008` |
| `result` | **PASS** |
| `scope` | "longitude-crossing primitive; sign/nakshatra ingresses (with declared_division, H-02 fix Option 1, ADR-0065); **returns; natal conjunctions; natal-relative view**" |
| `gates` | `A_residual_battery`, `C_oracle_anchors`, `D_independent_validator`, `E_declared_division` |
| `scope_not_gated` | **absent** |
| any gate carrying `exercises` | **none** |
| `explicit_non_claims` | aspect-system events; dasha-transit convergence; topocentric/heliocentric variants; interpretation |

**Reachability, measured under `ADR-0099` s3's own verification-surface definition:** all three have
**zero** call sites outside that surface. Each is called twice, only from
`engine/tests/test_transit_events.py`.

**The delegate's `kind` parameter does not branch the search.** `engine/transits/crossing.py` uses
`kind` at exactly two places: L178, where it is copied into the emitted `TransitEvent`, and L196,
where the tangent rule emits a hard-coded `kind="tangent"` regardless of the caller's value. There is
no control flow on `kind`. **Consequence worth noting for any neutrality test:** a call with
`kind="return"` can still yield `kind="tangent"` events, so "all returned events carry
`kind='return'`" would be a false invariant.

---

## 2. `returns()` - `engine/transits/events.py` L65-L76

### A. Actual behaviour

```python
def returns(body, natal_longitude, jd_start, jd_end, profile) -> tuple:
    """Crossings of the body's own natal longitude (returns)."""
    return find_crossings(body, natal_longitude, jd_start, jd_end, profile, kind="return")
```

**A pure delegator, and the only one of the three.** A single expression. No arithmetic, no
post-processing, no reordering, no reshaping. The returned object is the identical tuple
`find_crossings` produced. The sole difference from a bare `find_crossings` call is the `kind` label
carried on non-tangent events, and s1 establishes that `kind` does not branch the search.

### B. Certification coverage

**None directly.** `find_crossings` itself is exercised by `A_residual_battery` (L143),
`E_declared_division` (L273) and the independent validator (L114, L119). `returns()` is covered only
by two non-certification tests: `test_declared_division_is_none_for_events_with_no_division_semantics`
(L58-L66) and `test_solar_return_lands_on_natal_sun` (L125-L129).

### C. Can it legitimately inherit certification?

**Yes, on the evidence - and it is the only one of the three for which the question is even coherent.**
It has a single identifiable delegate whose behaviour is gated, and it adds nothing. `ADR-0099` s5
nevertheless requires that neutrality be **proven by a committed test**, and no such test exists.
Under the ratified rule it does **not** currently inherit.

### D. Is a C5 neutrality test applicable?

**Yes, and it is close to trivial to state:** for representative bodies, targets and windows,
`returns(b, L, s, e, p)` equals `find_crossings(b, L, s, e, p, kind="return")` element-for-element.
The non-obvious part is the `kind="tangent"` case from s1, which a naive invariant would get wrong.

### E. Is direct certification or gating required?

**Not on the evidence, if C5 is taken.** A gate exercising `returns()` would re-test `find_crossings`
through one extra stack frame.

### F. Is `scope_not_gated` an acceptable disposition?

**Yes, defensibly** - with the per-item reason being pure delegation plus a committed neutrality test.
Weaker than (a) but honest, and cheapest.

### G-J

See s5. `returns()` is the one case where every option in `ADR-0099` s4 is genuinely available.

---

## 3. `natal_conjunctions()` - `engine/transits/events.py` L79-L100

### A. Actual behaviour

**Not a pure delegator.** It adds three behaviours of its own:

```python
events = []
for label, longitude in natal_points.items():          # 1. iteration over a caller-supplied mapping
    for event in find_crossings(body, longitude, jd_start, jd_end, profile,
                                kind="natal_conjunction"):
        events.append((label, event))                  # 2. re-shaping: (label, event) PAIRS
events.sort(key=lambda pair: pair[1].julian_day)       # 3. cross-target ordering
return tuple(events)
```

1. **Label attachment.** The label-to-longitude mapping is the caller's `natal_points` dict; the
   pairing is this function's own contract.
2. **A different return shape from its delegate.** `find_crossings` returns `tuple[TransitEvent]`;
   this returns `tuple[(str, TransitEvent)]`. **A neutrality test in the `ADR-0099` s5 sense cannot
   be written between objects of different shape.**
3. **An ordering contract.** The merged sort is across *different* targets, which `find_crossings`
   never performs - it sorts within one target. Python's sort is stable and `dict` preserves insertion
   order, so the result is deterministic **given the caller's dict order**; for events sharing a
   `julian_day`, the output order is therefore a function of caller input order. Nothing records this.

For contrast, the sibling helper `_multi_target` (L33-L40), which `sign_ingresses` and
`nakshatra_ingresses` use, performs the same merged sort - **and that code path is gated**, by
`A_residual_battery` and `E_declared_division`. So the ordering pattern is exercised in the artifact,
but through a different function, on a different shape, over different targets.

### B. Certification coverage

**None.** Covered only by `test_natal_conjunctions_label_events` (L140-L146) and the
`declared_division` test at L70.

### C. Can it legitimately inherit certification?

**No, not in full.** Its delegate's certification can cover the crossing instants. It cannot cover the
label pairing, the return shape, or the cross-target ordering, because the delegate exhibits none of
them.

### D. Is a C5 neutrality test applicable?

**No, not as `ADR-0099` s5 frames it.** Behavioural neutrality means the delegator's output is the
delegate's output. Here they are different types. A *partial* test - "the event component of every
pair equals what `find_crossings` returns for that label's longitude" - is writable and useful, but it
is **not** a neutrality proof and would leave the ordering contract untested.

### E. Is direct certification or gating required?

**On the evidence, yes, for the added behaviours** - the pairing and the ordering. The crossing
arithmetic itself needs no new gate.

### F. Is `scope_not_gated` an acceptable disposition?

**Available, but it would be declaring genuinely uncertified behaviour out of coverage** while the
artifact records `PASS`. Defensible only with a reason stating precisely which behaviours are excluded
and why the risk is accepted.

---

## 4. `transit_view()` - `engine/transits/view.py` L47-L102

### A. Actual behaviour

**Not a delegator at all. It has no delegate.** It is original code with five distinct behaviours:

1. **Profile-isolation guard** (L59-L66): raises `TransitProfileError` when the natal snapshot has no
   provenance, or when `natal_provenance.profile_name != profile.name`. A deliberate methodology
   control refusing mixed-ayanamsa comparison.
2. **Its own angular-separation arithmetic** (L43-L44):
   `_separation(a, b) = abs(((a - b + 180.0) % 360.0) - 180.0)`.
3. **Longitude-set construction** (L77-L83) over `CANONICAL_GRAHAS`, from `astronomy_snapshot`.
4. **Ascendant injection** (L84): `natal_longitudes["Ascendant"] = natal_snapshot.houses.ascendant` -
   an asymmetry, since the transit side carries no Ascendant.
5. **Full cross-product construction** (L86-L94): one `TransitContact` per (transiting x natal) pair,
   including Ascendant on the natal side.

**On `_separation` specifically - stated carefully, because it is the sharpest claim in this paper.**
The repository already contains a *second, independent* angular-separation implementation at
`engine/astronomy/aspects.py` L39-L45, which normalises both inputs to [0,360) **first**, with a
comment recording that this hardening was applied in response to a prior audit finding. `_separation`
does not normalise first.

**Executed comparison at `d7092cb3`**, over 11 adversarial cases (negative, >360, wrap-around,
antipodal, `-1e-16`) and **200,000 random pairs including un-normalised inputs in [-720, 1080]**:

- maximum absolute disagreement between the two implementations: **0.000000e+00**
- `_separation` results outside [0, 180]: **0**

**So `_separation` is not demonstrably defective, and this paper does not claim it is.** What is true
is narrower and still material: it is a **second implementation of a primitive that exists elsewhere
in a deliberately hardened form**, it is **exercised by no gate**, and **no committed test asserts
either its range invariant or its agreement with the other implementation**. A probe run during an
audit is not a gate. `engine/astronomy/aspects.py` is itself imported by no root validator; it is
covered by `engine/tests/test_aspects.py` and `engine/tests/test_boundary_hardening.py`.

### B. Certification coverage

**None.** One non-certification test, `test_transit_view_profile_guard_and_separations` (L154-L171),
which exercises the guard and some separations.

### C. Can it legitimately inherit certification?

**No. The question does not arise.** There is no delegate. `astronomy_snapshot` is certified upstream,
but every behaviour listed in A above is `transit_view`'s own and is not performed by
`astronomy_snapshot`.

### D. Is a C5 neutrality test applicable?

**No. `ADR-0099` s5 does not reach this callable at all.** Neutrality is a relation between a
delegator and a delegate; there is no pair here to relate.

### E. Is direct certification or gating required?

**On the evidence, yes, if it is to remain in `TRANSIT_V1`'s scope.** It contains the only uncertified
numerical primitive in that scope. A gate would plausibly assert the range invariant on
`_separation`, its agreement with `engine.astronomy.aspects`, the contact cross-product's cardinality
and membership, and the profile-mismatch refusal - the last with a negative control, per
`.claude/rules/certification.md`.

### F. Is `scope_not_gated` an acceptable disposition?

**This is the sharpest question in the paper.** Declaring "natal-relative view" as
`scope_not_gated`-with-a-reason would place **uncertified numerical code** outside gate coverage while
`TRANSIT_V1` continues to record `result: PASS`. That is permitted by the letter of `ADR-0099` s4(b).
Whether it is consistent with `docs/VALIDATION_STANDARD.md` s2 rule 3 ("no silent fallback") and rule
8 ("stored results are history, not proof") is a judgement this paper does not make. The alternative
reading - that scope should be narrowed instead, so the artifact stops claiming what it does not gate
- is presented as option 3-C in s5.

---

## 5. Options and consequences

Per callable. **No option is selected.**

### `returns()`

| Option | Consequence |
|---|---|
| **1-A. Gate it** (`ADR-0099` s4(a)) | Strongest. Re-tests `find_crossings` through one extra frame; near-zero new information, small cost. Regenerates `TRANSIT_V1`. |
| **1-B. C5 neutrality test + `scope_not_gated`** | Matches `ADR-0099` s5's intent exactly. Cheapest path that satisfies the ratified rule. Must handle the `kind="tangent"` case (s1) or the test encodes a false invariant. |
| **1-C. `scope_not_gated` alone, reason = pure delegation** | Cheapest. Rests on an inspection finding, which `ADR-0099` s5 says does **not** confer inherited certification - so the artifact would record a weaker basis than the rule contemplates. |

### `natal_conjunctions()`

| Option | Consequence |
|---|---|
| **2-A. Gate the added behaviours** | Covers pairing, shape and cross-target ordering. Requires deciding whether the tie-order contract (caller dict order) is normative or incidental - **a behavioural question nothing currently records**. |
| **2-B. Partial delegation test + `scope_not_gated` for the remainder** | Honest and cheap: asserts the event component matches the delegate, declares pairing/ordering not gated with a reason. Leaves the ordering contract untested. **Note this is not a C5 neutrality test**, and calling it one would misstate the record. |
| **2-C. Narrow `TRANSIT_V1` scope to remove "natal conjunctions"** | The artifact stops claiming it. Requires an `ADR-0008` scope amendment and regeneration, and `Q8_CLOSURE_MATRIX.md` s9's VARSHAPHAL prerequisite note would need re-reading against the narrowed scope. |

### `transit_view()`

| Option | Consequence |
|---|---|
| **3-A. Gate it directly** | The only option that puts the uncertified separation arithmetic, the Ascendant asymmetry and the profile guard under a gate. Largest work item of the three; needs its own negative control for the guard. |
| **3-B. `scope_not_gated` with a per-item reason** | Permitted by `ADR-0099` s4(b). Places uncertified numerical code outside coverage while the artifact records `PASS`. Tension with `VALIDATION_STANDARD.md` s2 rules 3 and 8, noted but not adjudicated here. |
| **3-C. Narrow `TRANSIT_V1` scope to remove "natal-relative view"** | The artifact stops claiming a capability it does not gate. `transit_view()` would then be uncertified **and undeclared**, which is a coherent state - it has zero outside-surface callers. Requires an `ADR-0008` scope amendment and regeneration. |
| **3-D. Deduplicate: route `_separation` to `engine.astronomy.aspects`** | Removes the second implementation, inheriting whatever coverage that module has. **Does not by itself gate anything**, and `aspects.py` is imported by no root validator. Orthogonal to 3-A/3-B/3-C, and combinable with any of them. |

---

## 6. Consequences for the governance records

### G. For `ADR-0099` s4 (ACCEPTED)

s4's **classification is unaffected**: all three are capabilities named in `scope` and exercised by no
gate, so all three are SCOPE OVERCLAIMS. That holds on the corrected facts.

What the corrected facts change is the **assumed remedy**. `ADR-0099` s5 offers inherited
certification proven by a neutrality test; s4's own text describes the three as arising because the
gates "mention none of" four words. **That remedy is available for `returns()` only.** For
`natal_conjunctions()` a neutrality test cannot be written across differing shapes, and for
`transit_view()` there is no delegate at all.

`ADR-0099` s4 does not state that the three are delegators, so **no contradiction with the ratified
text is asserted here**. `N3` was resolved by reclassification - moving `returns()` off the exit track
- and that resolution is unaffected, since it turned on reachability, not on delegation.

### H. For `ADR-0101` s4's remediation backlog (ACCEPTED)

`ADR-0101` s4 requires each backlog entry to carry **artifact identity, deficiency, required
remediation, status and disposition/owner**. This paper's finding is that **"required remediation"
differs per callable within a single artifact**. If the backlog is keyed at artifact granularity,
`TRANSIT_V1` would carry one entry with three different remediations. Whether the backlog schema
should therefore be keyed at capability granularity is a specification question `ADR-0101` s6 already
lists as unresolved; this paper supplies a concrete reason to settle it that way.

### I. For `Q8` / JATAKA exit

**No effect on exit.** `ADR-0099` s4 places SCOPE OVERCLAIM outside `Q8_CLOSURE_MATRIX.md` s5's
criterion, and `ADR-0100` s1 confirms the obligation's authority is `ADR-0099` itself. Clause 2 is
satisfied with respect to all three because none is in use under `ADR-0099` s3 - measured again here,
zero outside-surface callers each.

One reading worth recording without adjudicating: clause 2 is satisfied because the three are
**unreachable**, not because they are **covered**. Options 2-C and 3-C would make scope and coverage
agree; options 2-B and 3-B would leave them disagreeing but declared. **JATAKA exit remains HOLD on
`N1`, `N2` and `N5` regardless**, with no completion report and no exit `ADR` in existence.

### J. Required new decision or amendment

- **Options 2-C and 3-C require an `ADR-0008` scope amendment**, hence a new ADR - `ADR-0008` is
  recorded and the append-only rule (`.claude/rules/governance.md` L23) forbids editing it.
- **Options 1-A, 2-A, 3-A and 3-D change or add code and regenerate `TRANSIT_V1`**, so each needs its
  own authorization and, where a gate changes what can be rejected, its own committed negative
  control.
- **Options 1-B, 1-C, 2-B and 3-B require `scope_not_gated`**, whose key name and shape `ADR-0101` s6
  lists as unresolved. **They cannot be implemented before that is settled.**
- No amendment to `ADR-0099` or `ADR-0101` is required by anything in this paper.

---

## 7. What this paper does not do

It decides nothing and selects no option. It does not modify `TRANSIT_V1` or any other certification
artifact, gate, registry, production module, test or CI job. It does not edit `ADR-0008`, `ADR-0099`,
`ADR-0100`, `ADR-0101`, `DP-038`, `DP-039`, `docs/Q8_CLOSURE_MATRIX.md`,
`docs/VALIDATION_STANDARD.md`, `docs/ENGINE_STATUS.md` or `docs/OPEN_QUESTIONS.md`. It does not
resolve, narrow or reinterpret `N1`, `N2`, `N5`, `N6` or `N7`, all of which remain open. **It
authorizes no part of the `C2`-`C5` programme.** It does not declare, perform or recommend JATAKA
phase exit, which **remains on HOLD**. The three SCOPE OVERCLAIMS **remain open and undisposed**.

---

## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-09-23 | Created under the owner's "CEO AUTHORIZATION - AUTHORIZE P-1 DECISION PAPER ONLY" instruction, following the read-only forensic audit. Analyses `returns()`, `natal_conjunctions()` and `transit_view()` independently at source rather than assuming the prior delegator framing, and finds that only `returns()` is a pure delegator: `natal_conjunctions()` adds label pairing, a different return shape and a cross-target ordering contract, and `transit_view()` has no delegate at all and contains its own separation arithmetic, Ascendant injection and contact cross-product. Records that `scripts/certify_transits.py` does not import any of the three, so no gate can reach them, and that `validate_transits_holdout.py` does not either. Records an executed comparison showing `view._separation` agreeing with `engine.astronomy.aspects` on 11 adversarial cases and 200,000 random pairs with zero disagreement and zero range violations - so the arithmetic is uncertified and duplicated, not demonstrably defective. Presents per-callable options with consequences and **selects none**. Decides nothing; authorizes no implementation; declares no phase exit. |
