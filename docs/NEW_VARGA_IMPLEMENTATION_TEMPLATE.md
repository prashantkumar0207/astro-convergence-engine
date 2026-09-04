<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | PROPOSED - operational template. Descriptive of what the five registry vargas actually carry, plus the independent-reference discipline established by the DP-032 D16/D4 remediation. Authorises no implementation. |
| Version | 1.1.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-09-04 |
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

`validate_dN_holdout.py` at the repository root: the independent by-name validator. **Stale as of
2026-08-11, corrected below (DP-032 remediation, 2026-09-04):** it must import **nothing from
`engine.astrology` at all** - not the classifier, not the registry, not the rule module - a genuine
from-scratch reimplementation of both the classical content (an independently-typed reference table,
by sign name) and the boundary/division arithmetic, not merely an independent table run through the
real `classify()`. It prints a sentinel success string and returns non-zero on failure. If the
division width is not binary representable, the reference must carry the boundary tolerance
explicitly and say why.

`scripts/certify_dN.py`: preflight, transcript capture, the gates (A through I in current practice,
not the five this template originally described), and emit. Gate D must include a fresh D9 and D10
sweep with recorded hashes, proving registration did not disturb the dedicated modules. See "Step 2a,
independent-reference discipline" below for what gates A, B, F, and G must each verify against.

## Step 2a, independent-reference discipline (DP-032 remediation, 2026-09-04)

An adversarial self-audit of the standalone D16/D4 certifiers (`docs/decisions/DP-032-d16-d27-d4-
methodology-readiness.md` Part G) found, and closed, two genuine gate-strength weaknesses that had
gone undetected through D24's and D40's own prior certification-execution stages. Both are now
**required**, not merely recommended, for every future standalone or production varga certifier:

**A. Independent reference/validator, precisely.** `validate_dN_holdout.py` must not import the
production varga implementation, `engine.astrology.varga_classifier`, or `engine.astrology.
varga_registry` - confirmed for every certifier this requirement applies to by direct inspection of
its import list, not merely asserted in prose.

**B. Gates A, B, F, and G must exercise that same independent reference directly**, imported into the
certifier itself (`import validate_dN_holdout`), rather than reconstructing "expected" values through
an in-file helper function or constant that the rule under test's own construction also uses. An
audit found this exact failure mode: a certifier's own `_independent_dN_sign()`-style helper sharing
its start-sign/offset content with the rule object it was meant to check, so a real content-
transcription bug passed gates A, B, C, D, E, F, G, and H undetected, caught only by a static Gate I.
Routing A/B/F/G through the already-independent validator file closes this without adding a parallel
check. **Gate I remains its own, separate requirement** (below) even after this fix - it is not made
redundant by it.

**C. Pinned content hashes must be load-bearing.** A `CERTIFIED_DN_CONTENT_SHA256`-style pin, once
introduced, must be checked with a real failure path (`if computed != pinned: fail(...)`) inside the
gate that reports it - not merely computed and included in the artifact as an informational field. An
audit found a certifier where this field was present and correctly computed, but no `fail()` was ever
conditioned on it, so a genuine mismatch would not have stopped certification on its own.

**D. Adversarial/negative controls should exercise the real enforcement path.** Where a gate's own
pass/fail decision rests on a specific helper function or comparison (as with C above), the
certifier's own Gate H should call that *same* function against a deliberately mutated object and
assert it correctly rejects the mutation - proving the actual code path, not a separately simulated
comparison that could drift from what the real gate does.

**E. Validator/reference independence must be evidenced, not assumed.** Before relying on
`validate_dN_holdout.py` as the independent reference for A/B/F/G/I, confirm and record its import
list directly (`grep -n "^import\|^from"` or equivalent) - this is a one-line check that closes a
class of finding an audit otherwise has to discover empirically.

**F. Environmental/oracle limitations must be disclosed, never silently treated as verification.** If
a gate's own oracle dependency (e.g. PyJHora) is unavailable in the environment running the
certifier, or if that dependency blocks a *later* gate in execution order from ever running (as Gate
C's own PyJHora requirement does for Gate D in `scripts/certify_d24.py` on a host without PyJHora -
confirmed during the DP-032 D24/D40 audit, 2026-09-04), this must be stated explicitly in the gate's
own report and in any audit relying on local execution - never presented as though the blocked gate
had run and passed.

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
| 1.1.0 | 2026-09-04 | CEO AUTHORIZATION - TEMPLATE UPDATE ONLY. Corrected Step 2's validator-independence description (was: imports the classifier/registry as subject under test; now: imports nothing from `engine.astrology`) and its stale "five gates" reference. Added Step 2a, the independent-reference discipline (requirements A-F) established by the DP-032 D16/D4 self-audit and remediation (`docs/decisions/DP-032-d16-d27-d4-methodology-readiness.md` Part G): independent-import discipline, gates A/B/F/G routed through the real reference, load-bearing content-hash enforcement, negative controls on the real enforcement path, evidenced validator independence, and disclosure of environmental/oracle limitations rather than silent pass. Documentation-only change; no certifier, certification artifact, production registration, or CI file touched. |
