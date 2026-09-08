<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents a certification-design PROPOSAL. DECIDES NOTHING. Requires owner approval. **Certification design does NOT itself authorize implementation or certification execution.** |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-09-06 |
| Review cadence | TBD |

# DP-036. Certification-design proposal for D20 (Vimsamsa)

## 0. Authorization and scope

Written under the owner's "CEO AUTHORIZATION - D20 CERTIFICATION DESIGN" instruction, which authorizes
**design only**: draft a certification-design proposal for D20 strictly under ratified `ADR-0095`,
define the proposed architecture, distinguish inherited precedent from D20-specific work, and identify
unresolved design questions rather than silently deciding them.

**This paper is a written plan.** No certifier or validator code was written. Nothing was executed. No
certification artifact exists or is produced. D20 is not implemented, not registered, and
`CERTIFIED_PRODUCTION_VARGAS` is untouched.

**Certification design does NOT authorize implementation or certification execution.** Each is its own
separate, not-yet-given authorization, exactly as `ADR-0095` section 6 states and as `ADR-0089`/
`ADR-0090` required for D16/D4.

**Not in scope, and not done:** D60, D27, `DP-024`, the `check_adr_numbering.py` encoding issue, CI,
and any modification of the existing D2/D3/D7/D12/D24/D30/D40/D45 implementations or artifacts (their
architecture was read for precedent only).

## 1. The frozen methodology this design must certify, restated verbatim from `ADR-0095`

Reproduced unchanged; this paper alters nothing:

- Kind: `CyclicVargaRule`; `divisions = 20`; width exactly **1.5 degrees**
- `start_sign = (0, 8, 4, 0, 8, 4, 0, 8, 4, 0, 8, 4)` (movable -> Aries, fixed -> Sagittarius,
  dual -> Leo)
- `direction = (1,) * 12`
- School key `parashara`; inherited promote-up boundary convention, no D20-specific exception
- Target sign for division index `l` of source sign `s`: `(start_sign[s] + l) % 12`
- **Variant F** (movable Aries, fixed Leo, dual Sagittarius) remains an **explicitly excluded named
  variant**, recorded as attested and not refuted
- **Deity payload remains excluded** under the `ADR-0089` precedent, so this design neither requires nor
  resolves `DP-024`

## 2. What is inherited, and what is D20-specific

### 2.1 Inherited from existing certified-varga precedent (no novelty proposed)

| Element | Precedent |
|---|---|
| Nine-gate A-I structure | D24 (`ADR-0083`), D40 (`ADR-0087`), D16/D4 (`DP-033`) |
| Standalone certification before production implementation | D24's `ADR-0083`; D16/D4's execution stage |
| Frozen rule instantiated **inside the certifier**, never in `engine/astrology/` | D16/D4 |
| Classification through the already-certified generic `varga_classifier.classify` | all registry vargas |
| From-scratch validator importing nothing from `engine.astrology` | D16/D4/D24/D40/D45 |
| Gates A/B/F/G routed through the validator's own reference function | template v1.1.0 req. **B** (from the `DP-032` Part G remediation) |
| Load-bearing pinned content hash (`fail()` on mismatch, not merely reported) | template v1.1.0 req. **C** |
| Negative controls exercising the real enforcement path | template v1.1.0 req. **D** |
| Import-list evidence of validator independence | template v1.1.0 req. **E** |
| Environmental/oracle limitation disclosed, never treated as verification | template v1.1.0 req. **F** |
| Gate I static reference regression, values generated once offline | the `ADR-0079` lesson |
| Artifact regenerated from scratch every run; stored JSON never accepted as proof | `.claude/rules/certification.md` |

### 2.2 D20-specific (genuinely new work)

1. **Boundary representability is exact, unlike D7/D9/D27.** Verified numerically during this design:
   width `30.0/20 = 1.5` is exactly representable, and all nineteen internal boundaries `k * 1.5` for
   `k = 1..19` are exact binary fractions (they are multiples of 0.5). **D20 therefore carries no
   representability error and needs no tolerance-carrying reference**, which `DP-035`/the roadmap
   require for D27. The ULP battery is consequently about the *promote-up convention at exact
   boundaries*, not about floating-point drift - a materially easier case than D7 or D9.
2. **A genuine external oracle is available and exact.** PyJHora exposes `vimsamsa_chart(...,
   chart_method=1)` (Traditional Parasara), and during `DP-035` its arithmetic was compared against
   `ADR-0095`'s frozen table across **all 12 x 20 = 240 cells and found identical**. D20 is pure
   longitude mathematics with no astronomy, so a zero-tolerance categorical oracle comparison is
   possible - the D24 situation, not the D40 one.
3. **Variant F is an excluded variant with a concrete, checkable shape.** Unlike most excluded variants
   (which are named but not expressible), Variant F is exactly
   `start_sign = (0, 4, 8, 0, 4, 8, 0, 4, 8, 0, 4, 8)`. That makes it possible to prove the engine does
   **not** compute it, rather than merely declaring it unclaimed. See the open question in section 11.
4. **The selection carries an explicit, ratified uncertainty statement** (`ADR-0095` section 4: not
   proof of the historical original text). The certification artifact must carry that qualification
   forward rather than presenting D20 as textually settled.

## 3. Proposed Gate A-I structure

| Gate | Name | Purpose | Authoritative input |
|---|---|---|---|
| **A** | Table/constant integrity | The frozen 12-entry `start_sign`/`direction` table matches an independently derived reference cell by cell, and the rule's content hash matches its pin | `validate_d20_holdout.reference_d20()`, imported directly (template req. B) |
| **B** | Dense mathematical sweep | ~51,429-point sweep over 0-360 degrees, every classification compared against the independent reference | same |
| **C** | External oracle | PyJHora `vimsamsa_chart` method 1, **zero categorical tolerance** - pure longitude math, no astronomy, so no tolerance derivation applies | PyJHora, in the hash-pinned oracle environment |
| **D** | Isolation / non-invasiveness | Proves D20 is **not** registered and no `engine/astrology/varga_d20.py` exists; proves the eight registered vargas and D1/D9/D10 are unaffected (fresh D9/D10 sweep hashes); **enforces** the content-hash pin with a real `fail()` | live registry + `hashlib` recompute |
| **E** | Independent validator | Subprocess run of `validate_d20_holdout.py`, requiring its sentinel success string | separate process |
| **F** | Boundary cases | All 19 internal boundaries per sign at exact hit, one ULP below, a coarse step below, three ULPs above; plus normalisation parity (negative, exactly 360, beyond 360) | independent reference |
| **G** | Protected holdout | Distinct sampling stride (`step = 0.0137`, as D16/D4 used) never used for tuning | independent reference |
| **H** | Negative controls | Real planted mutations via `dataclasses.replace()`, each shown to be caught; plus controls exercising the **real** hash-enforcement helper and the exact content-mutation path | the certifier's own enforcement functions |
| **I** | Static reference regression | ~10 hard-coded points generated **once, offline**, from the validator's own output; never regenerated at certification time | frozen constants |

Gate ordering matters: **D must be reachable.** `DP-032`'s D24/D40 audit found D24's Gate C blocks Gate
D on a host without PyJHora. This design therefore proposes that **Gate D not depend on Gate C's
success** - see the open question in section 11.

## 4. Independent-validator strategy

`validate_d20_holdout.py` at the repository root, built to template v1.1.0 requirement A:

- **Imports nothing from `engine.astrology`** - not the rule module, not `varga_classifier`, not
  `varga_registry`. A from-scratch reimplementation of both the classical content and the division
  arithmetic.
- The reference table is **independently typed by sign name**, not copied from `ADR-0095`'s integer
  tuple, and re-derived from the classical statement ("from Aries for movable, Sagittarius for fixed,
  Leo for dual") by a different construction than the certifier uses.
- Exposes `reference_d20(longitude) -> (sign, division)` plus a `STATIC_HOLDOUT`/
  `generate_static_expected()` pair used to seed Gate I offline.
- Prints a sentinel success string; returns non-zero on failure.
- **Independence evidenced, not assumed** (req. E): its import list is checked directly and recorded.

## 5. Oracle / corroboration strategy

**Proposed: genuine PyJHora execution at zero categorical tolerance**, matching D24 rather than D40.
Justification: D20 is deterministic longitude arithmetic with no astronomical component, so oracle
divergence cannot be attributed to ephemeris differences; and the 240-cell agreement already
established in `DP-035` means a mismatch would indicate a real defect, not a convention difference.

**Environmental limitation, disclosed in advance** (req. F): PyJHora cannot execute on the Windows
development host (`No module named 'jhora'`, a documented permanent gate-parity gap). Gate C would
therefore be genuinely exercised **only in CI's oracle job**. The certification artifact must state
which tier actually ran it, and a local PASS must never be represented as oracle-verified. This is the
exact distinction `DP-032`'s D24/D40 audit drew.

## 6. Boundary-test strategy

- The 19 internal boundaries per source sign, all exactly representable (section 2.2), tested at: exact
  hit, one ULP below, a coarse step below, three ULPs above.
- The promote-up convention governs the exact-hit case; because there is no representability error,
  **any** boundary disagreement would indicate a convention or table defect, not floating-point noise -
  a stronger claim than D7/D9 can make.
- Normalisation parity across negative longitudes, exactly 360.0, and beyond 360.
- Sign-transition edges (0 degrees and 30 degrees of each sign).

## 7. Holdout / protected-validation strategy

- Gate G samples on a **distinct stride** (`step = 0.0137`) chosen so its points do not coincide with
  Gate B's sweep or Gate F's boundary set - a genuine holdout, not a re-labelled boundary set.
- Gate I's ~10 static points are generated **once, offline**, from the validator's own output and then
  frozen as literals. They are never regenerated by the certifier at run time (`ADR-0079`).
- **No holdout point is ever used to tune the rule**, which is fixed by `ADR-0095` and cannot change.
- No existing protected validation data is touched.

## 8. Negative controls and mutation-testing strategy

Per template requirement D, controls must exercise the **real** enforcement path, not a simulated
comparison:

1. A planted `start_sign` transcription error, shown to be caught at Gate A.
2. A planted `direction` error, shown to be caught.
3. **A mutation to exactly Variant F's table** - the strongest available control, because it is the one
   wrong answer with genuine attestation behind it (see section 11, question 3).
4. A control calling the certifier's own `_content_hash_matches()` helper against a mutated rule,
   proving the real helper rejects it.
5. A control corrupting only the pinned hash constant, proving Gate D genuinely fails.
6. Confirmation the frozen rule object itself remains unmutated afterward (frozen dataclass;
   `replace()` returns a new instance).

## 9. Provenance, variant handling, and acceptance criteria

**Provenance recorded in the artifact:** `ADR-0095` as the governing decision; `DP-035` (and its Part B)
as the source-adjudication basis; the translated verse as the source of the triple; and - carried
forward verbatim - `ADR-0095` section 4's statement that **the selection is not proof of the historical
original text and primary-source uncertainty is not eliminated**.

**Variant handling:** Variant F named as an excluded variant with its evidentiary status (attested, not
refuted). The artifact must not imply Variant F is refuted.

**Payload:** the artifact must record that deity payload is excluded (`ADR-0089` precedent) and that
`DP-024` is therefore neither required nor resolved.

**Acceptance:** PASS requires **all nine gates** to pass, with Gate C's execution tier stated. **Failure
criteria:** any gate failing, any content-hash mismatch, any oracle categorical mismatch, or a negative
control that fails to fire. A skipped gate is a failure, not a pass (`.claude/rules/validation.md`). A
gate that cannot genuinely be executed must be reported as unexecuted, never as passed.

## 10. Artifact structure, independence and reproducibility

- `certification/VARGA_D20_V1_certification.json`, regenerated from scratch on every run; the stored
  file is never accepted as proof. Human-readable report and console transcript alongside, written by
  `certification_support.emit()` from the same run and same result dict.
- Schema mirrors the existing varga artifacts: schema id, ADR, date, scope, rule block (kind, variant,
  school, `registered: false`, boundary policy), oracle block (package, version, function, execution
  tier), the nine gate results, and the anti-fitting scan.
- **Independence requirement:** the implementation (frozen rule in the certifier), the validator
  (from-scratch, zero `engine.astrology` imports) and the oracle (PyJHora) must be mutually
  independent. Gates A/B/F/G compare against the validator, **not** against a helper shared with the
  rule's own construction - the exact defect `DP-032` Part G remediated.
- **Reproducibility:** two consecutive runs must be byte-identical outside the declared volatile fields;
  the certifier must be registered in `CERTIFIER_SOURCES`/`VALIDATOR_SOURCES` at execution time so the
  anti-fitting scan and artifact-drift gate cover it.

## 11. Unresolved certification-design questions - surfaced, not decided

1. **Standalone-first, or production-first?** This design assumes the D16/D4/D24 pattern: certify a
   standalone frozen rule now, with production implementation a separate later authorization. The
   alternative is to authorize production implementation first and certify the registered rule (D40's
   own production stage). **Not decided here.** The standalone reading follows `ADR-0095` section 6,
   but the owner may sequence otherwise.
2. **Should Gate C block Gate D?** `DP-032` found D24's real PyJHora Gate C prevents Gate D from ever
   running on a non-oracle host. This design proposes decoupling them so isolation is always
   verifiable locally. That is a deliberate divergence from D24's ordering and needs owner
   confirmation, since it changes what a local run proves.
3. **Should a Variant-F refutation gate exist?** Because Variant F is exactly expressible, the certifier
   *could* assert the engine never produces Variant F output for any longitude. That is stronger than a
   prose non-claim - but it also risks implying Variant F has been refuted as a *reading*, which
   `ADR-0095` explicitly denies. **Recommended as a negative control (section 8, item 3), not as a
   standalone gate** - but the owner may prefer either or neither.
4. **Gate count: nine or ten?** Every prior varga used nine. If question 3 became a gate, D20 would have
   ten, breaking the pattern and re-raising the Gate-I naming question `ADR-0088` addressed.
5. **Does the artifact need a machine-readable uncertainty field?** `ADR-0095` section 4's qualification
   is currently prose in the register. Whether the artifact should carry it as a structured field, so
   downstream consumers cannot cite D20 without it, is a design choice with no precedent either way.

## 12. What this paper does not do

Does not implement D20; does not create or modify D20 production code, a certifier, a validator, or any
certification artifact; does not register D20 or modify `CERTIFIED_PRODUCTION_VARGAS`; does not modify
CI; does not run certification; does not resolve `DP-024`; does not touch D60 or D27; does not modify
any existing varga implementation or artifact; does not fix the `check_adr_numbering.py` encoding issue;
does not push, open a PR, or merge.

## Exact CEO decision required

Whether to authorize **certification execution** for D20 on this design - and, if so, the owner's
answers to the five questions in section 11. Authorizing execution would permit writing
`scripts/certify_d20.py` and `validate_d20_holdout.py` and running them to produce an artifact. It
would **not** authorize production implementation or CI wiring, which remain separate.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-09-06 | Created under the owner's "CEO AUTHORIZATION - D20 CERTIFICATION DESIGN" instruction. Proposes the Gate A-I structure, independent-validator strategy, genuine-oracle plan, boundary/holdout strategy, negative controls, provenance/variant handling, acceptance criteria, artifact structure, and independence/reproducibility requirements for D20 under ratified `ADR-0095`, built to `docs/NEW_VARGA_IMPLEMENTATION_TEMPLATE.md` v1.1.0 requirements A-F. Records two D20-specific findings verified during design: all nineteen internal boundaries are exactly binary-representable (no D27-class tolerance needed), and a zero-tolerance PyJHora oracle is available and already 240-cell agreed. Surfaces five unresolved design questions rather than deciding them. A written plan only: no code, nothing executed, no artifact, nothing registered, `DP-024` untouched. |
