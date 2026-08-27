# DP-030 - KP_SIGNIFICATOR_V1 remediation readiness

| Field | Value |
|---|---|
| Status | DRAFT. Section 10 records that the certification-integrity defect this paper diagnosed has since been repaired under explicit CEO directive (2026-08-27) - see `ADR-0079`. Section 11 records that section 4 item 2's own claim (Reader IV surfaced no worked example or verbatim grouping statement) is now corrected by direct evidence - Reader IV does contain both. **Section 5 Option 1 is now CLOSED, per the owner's own "CEO decision: close DP-030 §5 Option 1 as sufficiently resolved for KP_SIGNIFICATOR_V1" - see `ADR-0080` (`ACCEPTED`).** Section 5's own remaining three options are not thereby chosen or ruled out by this paper; the horary-to-natal caveat is preserved, not withdrawn. No production module or certification artifact changed. |
| Version | 1.2.1 |
| Last updated | 2026-08-28 (Status line only: records `ADR-0080`'s closure of section 5 Option 1, per the owner's own exact decision instruction - recorded there, not by editing section 5's own text here) |
| Supersedes | Nothing. Extends `DP-029` section 4 and `ADR-0078`. |
| Audited tree | `fef113022d51923b54665c7cf48d88ce3fffc19b` (`main`) |

## 1. Why this paper exists

An external forensic experiment (2026-08-26) established by execution, not by
reading, that **every runnable correctness gate in `certify_kp_significator.py`
reports PASS while every sub-lord the engine computes is wrong.**

Method: `engine.kp.chain.kp_chain` was replaced with a version rotating
`sub_lord` one step along `KP_LORDS` - wrong at 3600/3600 sampled longitudes -
with `__module__`/`__name__` preserved so the corruption is indistinguishable
from a wrong implementation written into the module. Each gate was then run in
an isolated process.

| Variant | B | E | F | G | H | J | D |
|---|---|---|---|---|---|---|---|
| pristine (baseline) | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| corrupted, disguised | **PASS** | **PASS** | **PASS** | **PASS** | **PASS** | **PASS** | **PASS** |
| control: reference restored to truth | FAIL 12960 | FAIL 10933 | PASS | PASS | PASS | PASS | FAIL |

The control proves the comparisons are live: the identical loops reporting
**0 mismatches** under real corruption report **12,960** and **10,933** the
moment the two sides genuinely differ.

Gate D fires only on undisguised replacement. Its check is
`chain_module.kp_chain.__module__ != "engine.kp.chain"` - a module-identity
tamper detector, not a correctness check. A wrong implementation written into
`engine/kp/chain.py` keeps that attribute intact and evades it, as the
disguised run confirms.

Gate I was additionally shown non-detecting by direct execution: under
corruption the judgment changed from `Mercury / MIXED` to `Ketu / PROMISED` -
a different marriage verdict - and the gate passed identically in both runs.

## 2. Root cause (one sentence)

**Every gate sources its expected value from the same runtime that produces
the actual value**, so both sides move together and each comparison reduces to
`x != x`. This is structural: no quantity of additional cases repairs it.

Three concrete instances:

- **Gates B/E**: `make_synthetic_chart` builds cusps via `chain=kp_chain(lon)`;
  `_independent_sub_lord(lon)` returns `kp_chain(longitude).sub_lord`.
- **Gate I**: `_independent_judge_marriage_reference` imports
  `signification_set`, `full_name`, `PROMISE_HOUSES`, `DENY_HOUSES` and `_body`
  from `engine.kp.significators` - the module under test - and makes the
  identical `signification_set(...)` call `judge_marriage` makes. Only the
  verdict ternary is rewritten. Its docstring asserts the opposite.
- **`HOLDOUT`**: all twelve entries carry only `id`, `date`, `time`, `lat`,
  `lon`. **No expected sub-lord, no expected verdict, no expected signification
  set.** There is nothing for a result to be wrong against; it is a fixture
  list, not a holdout.

## 3. Correction to `DP-029` section 4's evidentiary basis

`DP-029` section 4 concluded "no computational oracle exists," while recording
that "none was searched for again this task, per the instruction not to." The
conclusion was therefore inherited, not established.

That broader search was performed for this paper. Findings, layer by layer:

| Layer | Oracle status |
|---|---|
| Cuspal sub-lord | **Oracle-backed already.** This is `kp_chain(cusp longitude)`, certified as `KP_CHAIN_V1` against PyJHora at 0.001 arcsec. Numerous external KP calculators also compute it. Not the gap. |
| Four-fold significator set | **No turnkey oracle located.** Commercial KP APIs return sub-lords and star-lords but explicitly require the caller to implement the four-fold scheme. |
| Marriage promise/deny verdict | **No oracle located.** |

**`DP-029`'s conclusion is upheld for the two layers that matter, despite the
inadequate search that produced it.** This is recorded because the reasoning
was not sound at the time, even though the answer was.

## 4. Primary-source position

**Item 2 below is superseded by section 11 (2026-08-28): Reader IV was re-fetched directly (its own
`djvu.txt` OCR output, bypassing the corrupted-font-encoding PDF path this section's own retrieval used)
and DOES contain both worked examples with real chart data and a verbatim statement of the grouping,
found in multiple locations. This section's own text is preserved unedited below as the dated record of
what was true at the time this paper was drafted; a reader relying on item 2's claim should read it
together with section 11.**

`KP_SIGNIFICATOR_SPEC.md` section 2 records Reader I as retrieved and
"source authority is not yet resolved to primary-text confidence." This paper
extends that:

1. **Reader III** (Predictive Stellar Astrology) full text was retrieved and
   examined. It contains **no worked examples with birth data**, and refers
   marriage judgment onward: *"For details study read IV reader, 'Marriage
   and Married Life'"*.
2. **Reader IV** (Marriage, Married Life and Children) full text was retrieved
   from **two independent copies**. Neither surfaced any worked example with
   explicit birth data, nor a verbatim statement of the 2/7/11 vs 1/6/10/12
   grouping. **Caveat: both are OCR'd scans read through a summarising
   fetch pipeline; this is evidence of absence, not proof.**
3. Reader IV contains a chapter heading **"Sub Lord of the 7th cusp" (p. 89)**
   whose body could not be read through that pipeline. **This is the
   doctrinal locus for the exact rule V1 freezes and is the single highest-value
   page to read directly from the PDF.**
4. `KP_SIGNIFICATOR_SPEC.md` section 1 already records that the per-matter house
   groupings are **"genuinely disputed across sources."** The verdict rule V1
   freezes therefore rests on doctrine the project's own research classes as
   unsettled.

## 5. Options

**Option 1 - Source real ground truth, then re-certify.**
Read Reader IV p. 89 and locate worked examples in the KP corpus; transcribe
10-20 cases with expected sub-lord, signification set and verdict; commit them
before running the engine against them. Strongest outcome. Blocked on whether
such examples exist in retrievable form - currently unestablished.

**Option 2 - Scope V1 down to what is certifiable; refuse the verdict.**
Certify the significator-set derivation as a declared rule application. Make
`judge_marriage` refuse to emit PROMISED/DENIED, in the manner `ADR-0066` made
`find_crossings()` raise `UnsupportedNodePolicyError` - converting an
unvalidatable judgment into an explicit refusal rather than a confident string.
Consistent with the project's own anti-manufactured-confidence rule and with
section 4.4's disputed-doctrine finding. Smaller product, honest.

**Option 3 - Purchase/obtain a significator oracle.**
No turnkey source located (section 3). Would require building the four-fold
scheme against a second independent implementation - which is re-derivation,
not oracle comparison, and reproduces the original problem unless authored
independently.

**Option 4 - Revoke `KP_SIGNIFICATOR_V1` outright**, returning KP to
`KP_CHAIN_V1` scope pending a future paper.

This paper does **not** select among these.

## 6. Independent of the option chosen

Three corrections are required under every option and are not decisions:

1. **`HOLDOUT` must carry expected values** or stop being described as a
   protected holdout. Its current `methodology` string - "real ephemeris-driven
   charts ... never used to tune any rule" - is true but omits that nothing is
   compared against.
2. **`_independent_judge_marriage_reference` must stop importing the module it
   checks**, or its docstring's independence claim must be withdrawn. The
   working pattern already exists in `validate_d9_holdout.py` and
   `validate_vimshottari_holdout.py`.
3. **Gates B and E must be reclassified as wiring checks** and their counts
   removed from the artifact's headline evidence. Gate B's own `scope` string
   already says this: *"production wiring vs. independent kp_chain() call."*

## 7. Proposed standing gate: `scripts/check_mutation_detection.py`

Drafted and attached with this paper. It corrupts a certified computation and
requires the certifier's correctness gates to detect it. Verified in both
directions:

- against `fef1130` as it stands: **FAIL (exit 1)**, all six correctness gates blind;
- with a genuinely independent reference substituted: **PASS (exit 0)**.

So it is not a constant-FAIL, and it would have caught this defect before
ratification. It generalises to every future capability - which matters because
**Jaimini, BNN, numerology, yoga evaluation, interpretation and convergence are
all expected to lack computational oracles**, making this the defect class most
likely to recur.

**Consequence requiring a decision:** wiring this into CI now turns CI red until
the certification is repaired. That is the honest state of the tree, but it is
the owner's call whether to gate immediately or after remediation. It is
therefore delivered unwired, with the single line needed to enable it recorded
in section 8.

## 8. Recommended sequence

1. Ratify a disposition for the existing `KP_SIGNIFICATOR_V1` certification
   (an ACCEPTED artifact recording PASS on vacuous evidence is currently
   standing in the register).
2. Read Reader IV p. 89 directly and determine whether Option 1 is live.
3. Choose among options 1/2/4.
4. Apply section 6's three corrections regardless.
5. Add to `.github/workflows/ci.yml`, hermetic tier:
   `python scripts/check_mutation_detection.py kp_significator`
6. Extend the mutation gate to the remaining certifiers, newest first.

## 9. Non-claims

- Does not establish that `judge_marriage` is *wrong*. It establishes that the
  certification does not show it is *right*. Those are different, and the
  distinction is the point.
- Does not re-audit `KP_CHAIN_V1`, which remains independently oracle-certified
  and is not implicated.
- Does not implicate any FOUNDATION-layer certification. The varga, dasha,
  rise/set, panchanga and trikalam certifiers were checked for this defect
  class and have genuinely load-bearing gates.
- Proves nothing about Reader IV's full contents; section 4's caveat stands.

## 10. Certification-integrity repair executed (2026-08-27)

Per the owner's explicit "CEO DIRECTIVE - KP_SIGNIFICATOR_V1 CERTIFICATION REPAIR" instruction, section 6's
three "independent of the option chosen" corrections were applied, and the section 7 mutation gate was
extended and proven both ways (see `ADR-0079` for the full account and evidence):

1. **`HOLDOUT` now carries static expected values** - generated once, offline, from
   `validate_kp_significator_holdout.py`'s own from-scratch `judge()`, never from
   `engine.kp.significators`. `gate_i_protected_holdout` compares live production output against them.
2. **`_independent_judge_marriage_reference` (the function that imported and called the module under
   test) is removed.** `validate_kp_significator_holdout.py` still imports nothing from
   `engine.kp.significators` (unchanged, verified directly).
3. **Gates B and E are honestly reclassified** as `wiring_coverage_not_correctness_evidence` in their
   own returned data and in the module docstring, with their counts preserved (not removed) but no
   longer presented as correctness evidence.
4. **The mutation gate now targets the significator computation itself** (`scripts/
   check_mutation_detection.py kp_significator_logic`, corrupting `engine.kp.significators._signifies`),
   in addition to the original substrate-level target, and both now report `RESULT: PASS` (detection
   confirmed) where the original target previously reported `RESULT: FAIL` (blind) before the repair.
   A literal on-disk edit-run-revert of `engine/kp/significators.py`, run as a real subprocess, confirmed
   pristine -> PASS (exit 0), corrupted -> FAIL (exit 3), restored -> PASS (exit 0).
5. **No separate methodological defect was found**: production (`judge_marriage`) and the independent
   validator (`judge`) were directly re-compared on all twelve real holdout charts after the repair and
   agree on every field. The already-ratified production module, `engine/kp/significators.py`, is
   therefore unchanged by this repair (net of the literal mutation test above, which was reverted).

**This section does not resolve section 5's own four options.** Those address whether the frozen
verdict rule has sufficient primary-source support at all (section 4's "genuinely disputed" finding,
Reader IV p.89 unread) - a separate, deeper question this repair was not authorized to touch and did
not touch. That decision remains fully open.

## 11. Reader IV primary-source evidence (2026-08-28)

Per "CEO AUTHORIZATION — DP-030 OPTION 1": investigated only whether Reader IV provides sufficiently
explicit, reproducible ground truth for the disputed marriage-grouping rule. This section records what
was found, using primary material already identified in section 4/`KP_SIGNIFICATOR_SPEC.md` section 19 -
no new search strategy, only a different retrieval path for the same named source.

**Retrieval.** Section 4 item 3's own `kp-readers` collection copy of Reader IV, previously blocked by a
corrupted PDF font encoding, was fetched directly as its own `djvu.txt` OCR output (487KB,
`archive.org/download/kp-readers/J_KP reader_4_Marriage-married-Life-Children_djvu.txt`) - a different
extraction pipeline than the PDF-text path that failed before, not a new source. Read directly (`grep`/
manual inspection of the raw text), not through a summarising fetch pipeline.

**Findings, each independently verifiable at the URL above:**

1. **A general (non-horary) chapter, "TIME OF MARRIAGE" (printed page 70), states the classical
   rationale for the grouping in near-verbatim agreement with Reader III's own passage already quoted in
   `KP_SIGNIFICATOR_SPEC.md` section 19.4**: *"By Marriage, it is meant that one more member is added to
   the family which is indicated by the second house. This addition is on an agreement which is denoted
   by the seventh house and such an additional member brings permanent tie of friendship for pleasure and
   progeny, shown by the 11th house. That is why houses 2, 7 and 11 are examined to find out whether -
   (a) marriage is promised or not..."* This directly contradicts section 4 item 2's claim that Reader IV
   surfaced no verbatim statement of the grouping.
2. **An explicit operative statement of the positive group**, in a worked chart example under the
   heading "Is Marriage Premised?": *"Note the sub-lord of the 7th cusp. If it is a significator of house
   7 or 2 or 11, marriage is promised."* Followed by real chart data (occupied houses, nakshatra lords,
   node substitution) applying the rule to a specific chart - a genuine worked example with data, which
   section 4 item 2 also claimed was absent.
3. **The negative group stated operatively**, in a separate worked passage: *"if the sub is lord of 1, 6,
   10 and is the significator of 12 houses, marriage cannot take place."* The same 1/6/10/12 set recurs
   repeatedly elsewhere in the book in closely related contexts (marital discord, separation).
4. **Several further worked examples** ("Is marriage promised?" - four separate occurrences of this
   exact heading, with real dates and dasha periods) apply the identical 2/7/11 vs 1/6/10/12 test outside
   any horary "query number" framing.
5. **Not resolved by this reading**: the TOC-listed chapter itself, "Sub Lord of the 7th cusp" (item 30,
   printed page 91 per the TOC - not page 89 as section 4 item 3 states; the discrepancy is unexplained
   and not investigated further, out of this task's own scope), could not be isolated as a single
   contiguous block in the OCR text (page markers in that range did not extract as clean boundaries). The
   findings above come from elsewhere in the same book, not from that specific chapter.
6. **The horary-versus-natal question, per this task's own explicit instruction, is NOT treated as
   resolved.** No passage found in this reading is unambiguously and exclusively natal in framing - the
   worked examples found interleave general chart-timing questions with query-time refinements (e.g.
   ruling-planets-based selection among competing significators, already correctly excluded from V1's own
   scope) in the same sections, without a clean structural separation between "horary illustration" and
   "natal illustration" the way modern secondary sources frame it. This is itself evidence of a kind - it
   is consistent with `KP_SIGNIFICATOR_SPEC.md` section 19.4's own prior observation that Krishnamurti's
   own house-signification mechanism is presented chart-type-agnostically throughout - but it does not
   itself constitute an explicit natal-only citation. **`KP_SIGNIFICATOR_SPEC.md` section 19.4's own
   disclosed non-claim (the horary-to-natal application is a reasoned inference, not an unqualified
   primary citation) is accordingly preserved, not withdrawn**, now on a materially stronger evidentiary
   footing (a second independent primary Reader, including a general non-horary chapter, corroborates the
   identical rule).

**What this section does and does not establish.** It establishes that section 4 item 2's specific
factual claim was inaccurate and corrects it (per section 4's own superseding note above, without editing
that section's text). It does not select among section 5's four remediation options. It does not close
this paper. It does not change the frozen rule, the production module, or any certification artifact -
none was touched by this task.

## Revision history

| Version | Date | Note |
|---|---|---|
| 1.2.1 | 2026-08-28 | Status line updated only: records `ADR-0080` (`ACCEPTED`), the owner's own "CEO decision: close DP-030 §5 Option 1 as sufficiently resolved for KP_SIGNIFICATOR_V1." Section 5's own text is not edited - the closure is recorded in the Status line and in `ADR-0080` itself, not by rewriting this paper's options. Section 5's remaining three options are not chosen or ruled out. No production code, frozen methodology, or certification artifact changed. |
| 1.2.0 | 2026-08-28 | Section 11 added, per "CEO AUTHORIZATION - DP-030 OPTION 1": Reader IV re-fetched directly (djvu.txt OCR output, bypassing the corrupted-font-encoding path that blocked section 4's own attempt) and read directly, not through a summarising pipeline. Corrects section 4 item 2's claim - Reader IV does contain a verbatim grouping statement (found in a general, non-horary "TIME OF MARRIAGE" chapter, p.70, near-identical to Reader III's own already-quoted rationale) and worked examples with real chart data. Section 4's own text preserved unedited, with a superseding pointer added. The TOC-listed "Sub Lord of the 7th cusp" chapter itself (page 91, not 89) remains unread - not isolated in the OCR text. The horary-to-natal caveat is explicitly preserved, not resolved: no passage found is unambiguously natal-only. Does not select among section 5's options; does not close this paper; no production code, frozen rule, or certification artifact touched. |
| 1.1.0 | 2026-08-27 | Section 10 added: records the certification-integrity repair executed under explicit CEO directive, independently re-verified (static holdout, reclassified wiring gates, extended mutation gate proven both directions, literal on-disk pristine/corrupted/restored proof, no discrepancy found between production and the independent validator on any of the twelve holdout charts). Section 5's own four options, addressing the separate primary-source question, remain undecided - not touched by this repair. |
| 1.0.0 | 2026-08-26 | Created following the forensic mutation experiment against `fef1130`. Records the executed evidence, identifies the structural root cause, corrects `DP-029` section 4's evidentiary basis while upholding its conclusion, extends the primary-source position to Readers III and IV, presents four options without selecting, and attaches a verified mutation-detection gate. Decides nothing; ratifies nothing; changes no production code. |
