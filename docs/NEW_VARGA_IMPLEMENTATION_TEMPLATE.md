<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | PROPOSED - operational template. Descriptive of what the five registry vargas actually carry. Authorises no implementation. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-11 |
| Review cadence | TBD |

# New Varga Implementation Template

Derived by reading what D2, D3, D7, D12 and D30 each actually contain, not from a design document.
Ordered so the non-invasiveness guards land before any correctness claim.

Nothing here authorises adding a varga. See `docs/VARGA_CERTIFICATION_ROADMAP.md` for policy, and
note that framework findings B-01 and B-02 should be resolved first.

## Step 0, before any code

Write the ADR. It must name the classical source, the school key, the rule kind, every non-claimed
variant by name, and the certification gates it commits to. Obtain the ADR number from
`docs/DECISION_LOG.md` before implementation, per ADR-0004.

## Step 1, rule and registration

`engine/astrology/varga_dN.py`, roughly forty to fifty lines: module docstring naming the version,
the ADR, the classical source and the explicit non-claims; the frozen rule literal with every cell
written out and an inline comment mapping source sign to target by name; the school constant; an
idempotent `ensure_registered()` guarded on the registry, because pytest imports modules repeatedly;
and a module-level call to it.

`engine/astrology/__init__.py`: the registering import, and the entry in
`CERTIFIED_PRODUCTION_VARGAS`. The tuple must stay in the order `registered_vargas()` returns, which
is sorted by division then school, so a new division slots between its neighbours rather than at the
end.

`engine/tests/test_varga_dN.py`: the table gate, using a second transcription keyed by sign name and
typed independently of the module literal, plus a re-derivation from the classical statement by a
different construction; the dense sweep; a full ULP boundary battery covering exact hits, one ULP
below, a coarse step below, and three ULPs above; normalisation parity across negative, exactly 360,
and beyond-360 inputs; and the registry state assertions. If the varga has a defining output
property, pin it. D2's two-sign output space, D7's full-zodiac coverage and D30's exclusion of the
luminary signs are the existing examples.

Shrink every still-refused list. There are ten sites across tests and certifiers. Repository
convention is an inline comment recording what was removed and why, never a silent delete.

## Step 2, verification and oracle

`validate_dN_holdout.py` at the repository root: the independent by-name validator. It imports the
classifier and the registry as the subject under test and imports nothing from the rule module. It
prints a sentinel success string and returns non-zero on failure. If the division width is not
binary representable, the reference must carry the boundary tolerance explicitly and say why.

`scripts/certify_dN.py`: preflight, transcript capture, the five gates, and emit. Gate D must include
a fresh D9 and D10 sweep with recorded hashes, proving registration did not disturb the dedicated
modules.

`engine/tests/test_varga_dN_certification.py`: the collected artifact gate asserting schema, decision
entry, result, every gate value, the registry entry, the absence of D1, D9 and D10 from it, the
sweep hash length, and a handful of hand-computed headline placements.

## Step 3, artifacts and cross-gates

Run the certifier and commit the artifact, the human-readable report and the console transcript.

Two cross-gates are easy to miss. Add the artifact to the certification-preconditions test, or it is
never checked for preconditions and transcript retention. And add the new sweep hash to the
sign-convention certification constant **and re-run that certifier**, because it iterates the registry
and its pinned hash set will raise on an unknown key. This ordering dependency between two unrelated
certifications is not obvious and is the most likely thing to be missed.

## Step 4, documentation

The registry specification gains a block matching the existing entries. `docs/ENGINE_STATUS.md` gains
the division in its certified list and loses it from its non-claims. `README.md` gains an additive
paragraph and the two run commands.

## Step 5, gates

The full battery must be green after every commit: the default gate, all validators, all certification
runners regenerating PASS, and the governance job.

## Recommended additions not currently in the template

Assert that the registered rule object is identical to the module constant, which would close audit
finding B-02. Assert that the rule's division count matches the division it is registered under, which
would close B-01. Recompute the sweep hash live rather than reading it from a stored artifact, which
would close B-03 and align with the validation standard's rule that stored results are history, not
proof.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-11 | Created in the G1 work package from a reading of the five registry vargas. |
