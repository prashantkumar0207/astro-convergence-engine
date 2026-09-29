<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Forensic evidence brief for CEO adjudication of `DP-041` **Q-E** only. **DECIDES NOTHING.** Selects none of 26 / 22 / mixed. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-09-29 |
| Review cadence | TBD |

# DP-042. Q-E: which certification artifacts does `ADR-0101` s2/s3 bind?

Written under the owner's "CEO DIRECTIVE - BEGIN DP-041 Q-E ADJUDICATION PREPARATION" instruction.
`DP-042`'s identifier was allocated in `docs/decisions/README.md` before this paper's substantive
content was written, per `ADR-0040`. **That ordering is not independently proven by the commit graph:**
the index row and this paper were committed together. Every fact below was re-read or re-measured at
`main` `c47faa9cac219c80607b099172985dd155fa3a41`; **no figure is carried over from a prior report.**

**This paper adjudicates nothing and selects none of the three readings.** Where the evidence
conflicts it is preserved as conflicting, not reconciled.

---

## 1. The question

`ADR-0101` s2 and s3 (ACCEPTED) impose obligations **on certification artifacts**: each must carry a
machine-readable capability enumeration, and each of its gates must carry an `exercises` array.
`ADR-0101` s4 applies those obligations "universally to the certification corpus".

> **Q-E. Which artifacts must satisfy `ADR-0101` s2 and s3?**
>
> All **26** files in `certification/`? The **22** that are runner-regenerated and scope-bearing? Or a
> **mixed** reading in which s4's backlog spans 26 while s2/s3 bind 22?

`DP-041` s10 states Q-E in the 26/22/mixed form. This paper reconstructs it from the instruments
themselves and reaches the same question by a different route, with one correction to `DP-041`'s
evidence (s7 below).

---

## 2. Authoritative sources, with exact locations

All line numbers are `main` at `c47faa9c`.

| Source | Status | Location | Operative text |
|---|---|---|---|
| `ADR-0101` s2 | ACCEPTED | `docs/DECISION_LOG.md` **L9107-9108** | "A certification artifact **must explicitly enumerate the production capabilities to which its certification scope applies, using stable machine-readable capability identifiers.**" |
| `ADR-0101` s3 | ACCEPTED | **L9124-9125** | "**Each certification gate must explicitly declare, in an `exercises` array, the stable capability identifiers it exercises or covers.**" |
| `ADR-0101` s4 | ACCEPTED | **L9145** | "The requirements in sections 2 and 3 apply **universally to the certification corpus.**" |
| `ADR-0101` s4 | ACCEPTED | **L9147-9148** | "**must not be silently grandfathered. Permanent grandfathering is not permitted.**" |
| `ADR-0101` s4 | ACCEPTED | **L9159-9163** | "**Measured starting position at `f8f13607`** ... **26** certification artifacts, of which **22** carry a non-empty `scope` ... The **corpus** uses **26 distinct `schema` values**, one per artifact" |
| `ADR-0101` s6 | ACCEPTED | **L9189** | "The **remediation sequence** across the **22 scope-bearing artifacts**, and who owns each entry." |
| `ADR-0101` Consequences | ACCEPTED | **L9216** | "the **22 scope-bearing artifacts** are unchanged and uncompliant on the day of ratification" |
| `ADR-0101` ratification sub-entry | ACCEPTED | **L9249-9250** | "The requirements apply **universally** to the certification corpus." |
| `ADR-0101` ratification sub-entry | ACCEPTED | **L9259-9262** | "the **26-artifact corpus** was not regenerated. Measured at ratification ...: 26 artifacts, 22 with a non-empty `scope`" |
| `ADR-0092` s1 | ACCEPTED | **L7551-7555** | The inventory "**is frozen, dated historical evidence** ... **not** a live current-state register, is not to be regenerated on capability change, and **is not stale**" |
| `ADR-0092` s1 | ACCEPTED | **L7567-7569** | "**This entry classifies the artifact. It does not ratify the artifact's contents.**" |
| `ADR-0092` s2 | ACCEPTED | **L7573-7575** | "The inventory **is not a current source of truth for any purpose** and **must not be used by any future capability-consistency gate as a live-state authority.** Any such gate must name it in its exclusion list **alongside the other non-current material**, and must draw live state only from the sanctioned live sources" |
| `ADR-0092` Status | ACCEPTED | L7530 | Owner instruction includes "**Do not modify `ENGINE_CAPABILITY_INVENTORY.json`.**" |
| `ADR-0092` Consequences | ACCEPTED | L7629-7635 | "the repository still has **no** live capability inventory, by decision" |
| **`ADR-0094` s4** | **ACCEPTED** | **L7821-7827** | "`FROZEN_EVIDENCE` excludes `ENGINE_CAPABILITY_INVENTORY.json` (citing `ADR-0092`), **plus `ORACLE_ENVIRONMENT.json`, `G6_REMOTE_CI_VALIDATION.json` and `CURRENT_ENGINE_LOCK.json`.** Two committed tests enforce this" |
| `scripts/check_capability_state.py` | code | **L81-L89** | The `FROZEN_EVIDENCE` frozenset, with the comment "`ADR-0092` decides this for the capability inventory specifically; **the other three share its shape** (a date, a source commit or environment, and **no runner that regenerates them**)" |
| `scripts/check_capability_state.py` | code | **L199** | The **single** use: `if path.name in FROZEN_EVIDENCE: continue`, while building that gate's verdict map |
| `scripts/check_capability_state.py` | code | **L51-L55** | Docstring: "FROZEN historical evidence is excluded **from the live sources**" |
| `engine/tests/test_capability_state_gate.py` | code | **L248, L254, L270-278, L296** | Four committed controls, incl. `test_every_frozen_file_is_really_dated_evidence` parametrized over all four, and `test_frozen_inventory_cannot_influence_the_verdict` (byte-identical verdict with a corrupted copy staged) |

---

## 3. Measured facts

Re-measured at `c47faa9c`. **These are not in dispute under any reading.**

| Measurement | Value |
|---|---|
| Files in `certification/*.json` | **26** |
| Named in `FROZEN_EVIDENCE` | **4** - `ENGINE_CAPABILITY_INVENTORY.json`, `ORACLE_ENVIRONMENT.json`, `G6_REMOTE_CI_VALIDATION.json`, `CURRENT_ENGINE_LOCK.json` |
| Carrying a non-empty `scope` | **22** |
| Carrying `_slug` / `_artifact_name` | **22** |
| Carrying `gates` | **21** |
| Carrying `scope_not_gated` | **0** |
| Gates carrying an `exercises` array | **0** |
| `CERTIFIER_SOURCES` registered | **22** |
| Distinct `schema` values | **26** - one per artifact |

**The decisive structural measurement.** For each of the 26, whether a certifier that is registered
**and** executed by `.github/workflows/ci.yml` writes it:

```
non-frozen (22) : with a CI-run writer = 22    without = 0
frozen      (4) : with a CI-run writer =  0    without = 4
```

**The 22/4 split is not arbitrary. It tracks a measurable property - runner-regenerated or not - and
the four frozen files are exactly the four with no runner, exactly the four with no `scope`, and
exactly the four named in `ADR-0094` s4.** All three sets coincide.

Per-artifact detail: all 21 `*_V1_certification.json` files plus `current_engine_certification.json`
have a CI-run writer (`certify_transits.py`, `certify_d2.py` ... `certify_vimshottari.py`,
`certify_current_engine.py`). None of the four frozen files does.

---

## 4. The three concepts, explicitly separated

**U1 - the measured corpus.** The 26 files in `certification/*.json`. Established by measurement.
`ADR-0101` s4 L9162 and the ratification sub-entry L9259 both call this "the corpus" and count it at
26.

**U2 - the live enforcement universe of `check_capability_state.py`.** The 22, produced by that
script's own `FROZEN_EVIDENCE` constant at its single call site L199. Its scope is stated in its own
docstring at L51: exclusion **from the live sources** - i.e. from what the gate *reads as authority*.
Recorded in ACCEPTED `ADR-0094` s4 and protected by four committed tests.

**U3 - the `ADR-0101` normative obligation universe.** The artifacts that must **carry** an enumeration
and `exercises` arrays. **No instrument states this set.** U3 is what Q-E asks for.

**The distinction that generates the ambiguity.** U2 governs **reading**: which artifacts a gate may
treat as live authority. U3 governs **containing**: what an artifact must hold. `ADR-0092` and
`ADR-0094` s4 both speak to reading. `ADR-0101` s2/s3 speak to containing. **No ratified text joins
them**, and nothing in `ADR-0092` or `ADR-0094` says a frozen artifact is exempt from carrying
anything.

---

## 5. Evidence matrix

| # | Item | Class | Evidence |
|---|---|---|---|
| E1 | s2/s3 impose obligations on artifacts, in force | ratified text | L9107-9108, L9124-9125 |
| E2 | s4 says s2/s3 apply "universally to the certification corpus" | ratified text | L9145; restated L9249-9250 |
| E3 | `ADR-0101` calls the corpus **26** | ratified text | L9162, L9259-9260 |
| E4 | `ADR-0101` s6 frames the remediation sequence over **22** | ratified text | **L9189** |
| E5 | `ADR-0101` Consequences frames day-one non-compliance over **22** | ratified text | **L9216** |
| E6 | Silent and permanent grandfathering both forbidden | ratified text | L9147-9148 |
| E7 | The inventory is not a current source of truth **for any purpose** | ratified text | L7573 |
| E8 | `ADR-0092` forbids **modifying** the inventory | ratified text | L7530 |
| E9 | `ADR-0092` contemplates "**other non-current material**" without naming it | ratified text | L7574 |
| E10 | `ADR-0094` s4 **names all four** frozen files | ratified text | **L7821-7827** |
| E11 | `FROZEN_EVIDENCE`'s single use is excluding files from that gate's **live sources** | code | L51, L199 |
| E12 | Four committed controls guard the exclusion list | code, executed | `test_capability_state_gate.py`; 7 passed |
| E13 | All 22 non-frozen artifacts have a CI-run writer; all 4 frozen have none | measured | s3 above |
| E14 | The four frozen files carry **no `scope`** | measured | s3 above |
| E15 | No instrument states U3 | absence, verified by full-entry sweep of `ADR-0101` L9064-9250 | s2 above |

**Contradiction preserved, not reconciled.** **E2+E3 point at 26. E4+E5 point at 22.** All four are
ratified text inside the same entry. `ADR-0101` is **internally divided** on its own applicability: its
universality clause and corpus measurement say 26, while its own s6 and Consequences block describe
remediation and day-one compliance over 22. **This is an intra-ADR ambiguity, not merely a gap**, and
it is the core of Q-E.

---

## 6. Candidate interpretations

### 6.1 Reading E-1 - U3 = 26

**Supporting text.** L9145 "universally to the certification corpus"; L9162 and L9259 counting the
corpus at 26; L9249-9250 restating universality in the ratification sub-entry.

**What it explains.** The plain meaning of "universally", and why s4 recorded a 26-file starting
position at all.

**What it conflicts with.** L9189 and L9216, which frame remediation and day-one compliance over 22.
And structurally: three frozen files have **no runner** (E13) so nothing can write an enumeration into
them, while `ADR-0092` **forbids modifying** the fourth (E8). Under E-1 four artifacts acquire an
obligation none can discharge except by permanent backlog residence - which must be squared with
L9147-9148's "**permanent grandfathering is not permitted**", unless indefinite backlog residence is
held to be distinct from grandfathering.

**Interpretation required?** Yes - of L9147-9148, to permit terminal backlog entries.
**Revision of an existing ADR?** Not necessarily. **New ADR?** Yes: append-only
(`.claude/rules/governance.md` L23) forbids editing `ADR-0101` or `ADR-0092`.

### 6.2 Reading E-2 - U3 = 22

**Supporting text.** L9189 and L9216, both ratified, both framing the work over 22. Structurally: a
SCOPE OVERCLAIM cannot arise in an artifact with no `scope`, and all four frozen files have none
(E14), so s2/s3 have no subject matter there.

**What it explains.** Why `ADR-0101` s6 and its Consequences speak of 22; why the 22/4 split tracks a
real property (E13); and it is the only reading under which every member can actually comply.

**What it conflicts with.** L9145's "universally" and L9162/L9259's corpus-at-26. It also extends a
frozen-evidence exemption from the surface `ADR-0092`/`ADR-0094` addressed - reading as authority - to
a different surface they did not address (s4 above). `ADR-0092` L7573's "**for any purpose**" is the
strongest text for the extension, and it still concerns the inventory's use as a *source*, not what it
must *contain*.

**Interpretation required?** Yes - of L9145, reading "the certification corpus" as narrower than s4's
own count. **Revision?** Arguably an extension of `ADR-0092`/`ADR-0094` to a new surface.
**New ADR?** Yes.

### 6.3 Reading E-3 - mixed: s4's backlog spans 26, s2/s3 bind 22

**Supporting text.** All of E2-E5 simultaneously: s4's universality and 26-count attach to the
**backlog**; s6's and the Consequences' 22 attach to **s2/s3 compliance**. Note the sentence structure
at L9145: "The requirements **in sections 2 and 3**" - s4 is the instrument applying s2/s3, and its
backlog is a separate mechanism in its own bullets at L9149-9151.

**What it explains.** The internal division in E2-E5 without discarding any of it, and it is the only
reading under which nothing is silently exempt **and** nothing is required of an artifact that cannot
produce it. The four frozen files appear in the backlog with a deficiency of "frozen dated evidence;
enumeration not applicable" rather than an unsatisfiable obligation.

**What it conflicts with.** It introduces a backlog entry class that closes **by classification rather
than by remediation**, which L9150's required field "the **required remediation**" does not obviously
accommodate. It is also the most complex schema.

**Interpretation required?** Yes - a distinction between s4's backlog scope and s2/s3's binding scope
that the text permits but does not state. **Revision?** No. **New ADR?** Yes.

### 6.4 Reading E-4 - decline to interpret; state the universe directly

A new ADR fixes U3 by decision rather than by reading `ADR-0101`. Slowest; clearest record; **no
interpretation of existing text is asserted.** Note that **E-1, E-2 and E-3 also require a new
appended entry**, so E-4 differs in framing rather than in mechanism.

---

## 7. Correction to `DP-041`'s evidence, preserved as contradictory record

`DP-041` v1.1.0 is on `main` and states, at L101 and again in its 1.1.0 change-history row at L525:

> `ORACLE_ENVIRONMENT.json`, `G6_REMOTE_CI_VALIDATION.json` and `CURRENT_ENGINE_LOCK.json` are frozen
> **by a builder's shape-based inference recorded in a code comment**, not by any ratified decision ...
> backed by **no** `ADR`.

**That is incorrect.** `ADR-0094` is **ACCEPTED** and its s4 at **L7821-7827** names all four files
explicitly (E10), and four committed tests enforce the list (E12). The builder who wrote `DP-041`
v1.1.0 - this builder - checked `ADR-0092` and the code comment but did not check `ADR-0094`.

**`DP-041` is not edited by this paper.** The misstatement stands there as the dated record of what was
claimed; this section is the correction, recorded additively. **The correction does not dissolve Q-E**:
`ADR-0094` s4 records the exclusion for *that gate's live sources* (E11), not for `ADR-0101`'s
containing obligations, so U3 remains unstated either way. What changes is the footing of Reading E-2,
which is better supported than `DP-041` represents.

A second, smaller understatement: `DP-041` s10 describes `ADR-0092` as exempting "one file from one
enforcement surface". `ADR-0092` L7573 is broader in wording - "not a current source of truth **for any
purpose**" - though still about use as a source.

---

## 8. What the repository says / enforces / follows normatively / remains ambiguous

**What it currently says.** s2/s3 bind "certification artifacts" and "certification gates" (E1). s4
applies them "universally to the certification corpus" (E2) and counts that corpus at 26 (E3). s6 and
the Consequences describe the work over 22 (E4, E5). `ADR-0092` and `ADR-0094` s4 classify four
artifacts as frozen dated evidence and exclude them from a gate's live sources (E7, E10).

**What it currently enforces.** Only U2, and only inside one script: `check_capability_state.py` skips
four names at L199 when building its verdict map (E11), guarded by four committed tests (E12). **No
gate enforces s2, s3 or s4 at all** - `scope_not_gated`, capability enumerations and `exercises` arrays
are at **0** across all 26 (s3). `C3` does not exist.

**What follows normatively from existing ratified authority.** That s2/s3 are in force; that silent and
permanent grandfathering are forbidden; that a declared backlog with five named fields is required;
that the inventory may not be modified; that the four frozen files are excluded from that one gate's
live sources. **It does not follow that U3 is 26, 22, or mixed** - E2/E3 and E4/E5 are both ratified
and point opposite ways.

**What remains genuinely ambiguous.** U3. And, under E-1 or E-3, whether a terminal or indefinite
backlog entry is compatible with L9147-9148.

---

## 9. Downstream dependency map

| Depends on Q-E | How |
|---|---|
| **`DP-041` question 7 / s8.6** | "How the obligation universe enters compliance" cannot be sequenced over an unknown set |
| **`Q-D`** migration sequence | `DP-041` s10 records the dependency explicitly |
| **`Q-B`** backlog location, *practically* | Option 4-B (per-artifact certifier-written key) **cannot represent the four frozen files**: no runner (E13), and modification forbidden (E8). Whether that disqualifies 4-B depends entirely on Q-E |
| **`C3`** specification | Needs an iteration set. *`C3` independently also needs `Q-A`* |

| Does **not** depend on Q-E | Why |
|---|---|
| **`Q-A`** identifier grammar | Concerns how a capability is named, not which artifacts are bound |
| **`Q-C`** `owner` semantics | Blocked on `Q1`, unrelated |
| **`Q-F`** backlog-completeness gating | Concerns enforcement of the backlog, not its membership |
| **`C2`** | Concerns `ADR-0099` s2's declaring union in `ENGINE_STATUS.md` s6, not per-artifact enumeration |
| **`C4`, `C5`** | Reachability and delegator neutrality; unrelated |
| **`DP-040`** dispositions | `TRANSIT_V1` is scope-bearing and runner-regenerated, so it is inside U3 under **every** reading. Q-E does not touch the three overclaims |

**Consequences for the 26 artifacts.** Under E-1: all 26 acquire the obligation; 4 cannot discharge it.
Under E-2: 22 acquire it; 4 are outside it. Under E-3: 22 acquire it; all 26 appear in the backlog, 4
terminally. **Under all three, today's state is identical and unchanged: 0 enumerations, 0 `exercises`
arrays, 0 `scope_not_gated`, no backlog, no `C3`.**

**Consequences for `C2`-`C5`.** `C2`, `C4`, `C5` unaffected. `C3`'s iteration set is fixed by Q-E; its
identifier space is fixed by `Q-A`. No option authorizes any of them.

---

## 10. The exact CEO decision required

> **Fix U3 - the set of certification artifacts that `ADR-0101` s2 and s3 bind - by selecting E-1 (26),
> E-2 (22), E-3 (mixed: s4's backlog spans 26, s2/s3 bind 22), or E-4 (state the universe directly
> rather than interpret).**
>
> **And, if E-1 or E-3 is selected, state whether an indefinite or terminal remediation-backlog entry is
> compatible with `ADR-0101` s4 L9147-9148's prohibition on permanent grandfathering.** That
> sub-question does not arise under E-2.

**Can Q-E be resolved without owner-level interpretation or amendment?** **No.** The boundary is exact:
`ADR-0101` contains ratified text on both sides (E2/E3 vs E4/E5), `.claude/rules/governance.md` L23
forbids editing it, and no other instrument states U3. **Every one of E-1 through E-4 requires a new
appended decision entry.** A builder reading cannot settle which ratified sentence governs.

**Is a new ADR or DP required?** A **new `ADR`** is required under every option, drafted PROPOSED and
ratified by the established sub-entry mechanism. **No further `DP` is required** - this paper is the
evidence base. Whether that new entry should also record the s7 correction to `DP-041` is the owner's
call; it is not necessary to resolving Q-E.

---

## 11. What this paper does not do

It decides nothing and selects none of E-1 through E-4. It does not modify `ADR-0092`, `ADR-0094`,
`ADR-0099`, `ADR-0100`, `ADR-0101`, `docs/ENGINE_STATUS.md`, `docs/OPEN_QUESTIONS.md`,
`docs/Q8_CLOSURE_MATRIX.md`, `docs/DECISION_LOG.md`, any certification artifact, `engine/`, `scripts/`,
`.github/`, `DP-039`, `DP-040` or `DP-041`. It creates no capability enumeration, `exercises` array,
`scope_not_gated` array or remediation backlog, and no gate. It does not implement `C2`, `C3`, `C4` or
`C5`. It does not touch `Q-A`, `Q-B`, `Q-C`, `Q-D` or `Q-F`, nor the three `TRANSIT_V1` SCOPE
OVERCLAIMS, nor `N1`, `N2`, `N5`, `N6`, `N7`, `Q1` or `Q12`. It does not declare, perform or recommend
JATAKA phase exit, which **remains on HOLD**.

---

## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-09-29 | Created under the owner's "CEO DIRECTIVE - BEGIN DP-041 Q-E ADJUDICATION PREPARATION" instruction. Forensic evidence brief for `Q-E` only, built from a fresh source-level reading at `c47faa9c` with no figure carried from a prior report. Separates the measured corpus (U1 = 26), `check_capability_state.py`'s live enforcement universe (U2 = 22, its single use at L199 being exclusion from that gate's live *sources*), and the `ADR-0101` normative obligation universe (U3), which **no instrument states**. Establishes the decisive structural measurement: **all 22 non-frozen artifacts have a certifier registered and run in CI; all 4 frozen artifacts have none**, and the frozen four are exactly the four with no `scope` and exactly the four named in `ADR-0094` s4 - the three sets coincide. Preserves rather than reconciles an **intra-`ADR-0101` contradiction**: L9145 and L9162/L9259 point at 26 while L9189 and L9216, equally ratified, frame remediation and day-one compliance over 22. Records four candidate readings with supporting text, what each explains, what each conflicts with, and whether each needs interpretation, revision or a new `ADR`. Corrects, additively and without editing `DP-041`, that paper's v1.1.0 statement that three of the four frozen files are "backed by **no** `ADR`": **`ADR-0094` s4 (ACCEPTED) names all four** and four committed tests enforce the list. States the exact CEO decision required, that Q-E **cannot** be resolved without owner-level interpretation or amendment, and that a new `ADR` is required under every option. Decides nothing; authorizes no `C2`-`C5` work; declares no phase exit. |
