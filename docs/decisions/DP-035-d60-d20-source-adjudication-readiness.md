<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents source findings and options. DECIDES NOTHING. Requires owner approval. Selects no methodology, freezes no rule, implements nothing, and does not resolve `DP-024`. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-09-05 |
| Review cadence | TBD |

# DP-035. Source-adjudication readiness for D60 (Shashtiamsa) and D20 (Vimsamsa)

## 0. Authorization and scope

Written under the owner's "CEO AUTHORIZATION - DP-035 D60/D20 SOURCE-ADJUDICATION READINESS"
instruction: research only, establishing the classical source basis for the two disputes
`docs/VARGA_CERTIFICATION_ROADMAP.md` section 4 records, identifying the competing readings, tracing
each to its sources, and giving each capability a readiness verdict. The instruction is explicit that
conflicting sources must not be silently reconciled, that no preferred interpretation may be invented,
and that a rule must not be frozen merely because one source is convenient.

**In scope:** the source basis for D60's even-sign reversal question and D20's start-triple question;
which readings exist; what each rests on; whether the evidence suffices for a methodology selection.

**Not in scope, and not done:** selecting either methodology; freezing any rule; implementing D20, D60
or D27; resolving `DP-024`; touching certification artifacts or protected holdout data; registering
any production varga; authorizing D16/D4 production; CI wiring.

**On D27:** the owner permitted incidental research only within `DP-032` Part F's existing scope. This
paper did not need it and did not perform it. `DP-032` section C.D's D27 conflict stands exactly as it
was.

## 1. The two questions

**D60.** `docs/VARGA_CERTIFICATION_ROADMAP.md` section 4 records: *"BPHS reverses the deity order for
even signs, and whether the sign also reverses is genuinely disputed across implementations."* The
question is therefore **what the even-sign reversal applies to** - the sixty deity names only, or the
sign sequence as well.

**D20.** The same section records the construction as *"twenty parts; movable Aries, fixed
Sagittarius, dual Leo"*, with content confidence *"Medium: the start triple is genuinely disputed,
with respected renditions giving Aries/Leo/Sagittarius instead"*. The question is **which start
triple** governs.

## 2. Source inventory

| # | Source | Type | What it was used for |
|---|---|---|---|
| S1 | `docs/VARGA_CERTIFICATION_ROADMAP.md` section 4 | internal, `Status: PROPOSED` | statement of both disputes; not itself evidence of the classical content |
| S2 | PyJHora (`naturalstupid/PyJHora`), `src/jhora/horoscope/chart/charts.py` and `src/jhora/const.py`, read directly at source | third-party implementation | what a mature implementation actually computes, and which variants it considers live |
| S3 | Wikipedia, *Shashtyamsha* | tertiary, paraphrasing BPHS | the BPHS sign rule and the reversal wording, and the explicit ambiguity between them |
| S4 | Multiple independent D20 secondary expositions (see section 6) | secondary | convergent statement of the D20 triple |
| S5 | Secondary D60 deity expositions | secondary | that the *deity* order reverses for even signs |

**No primary Sanskrit text was located for either question.** Everything below rests on translation,
paraphrase, and implementation. That is the same evidentiary position `ADR-0082` (D24) and `ADR-0087`
(D40) already accepted and disclosed - *"no located verbatim Sanskrit verse... only consistent
secondary attestation"* - so it is not disqualifying on its own, but it is stated rather than glossed.

## 3. Source authority assessment

- **S2 (PyJHora) is implementation evidence, not textual authority.** It is valuable precisely because
  it is unambiguous and executable, and because its *enumeration of variants* shows which readings
  practitioners treat as live. It cannot settle what BPHS says.
- **S3 (Wikipedia) is tertiary**, but it quotes the operative instruction closely and - importantly -
  is explicit about what the text does *not* settle. Its value here is the disclosure of ambiguity,
  not the assertion of a reading.
- **S4/S5 are secondary.** Convergence across independent secondary sources is meaningful corroboration
  and is exactly what this project accepted for D24/D40, but convergence is not provenance: secondary
  sources copy each other, and this paper cannot rule that out.
- **S1 is internal and unratified.** It is the statement of the problem, not evidence for any answer.

## 4. D60 findings

### 4.1 Source fact

S3 renders Parashara's sign instruction as: *"ignore the sign position of a planet and take the degrees
etc. it traversed in that sign. Multiply that figure by 2 and divide by 12, then, add 1 to the
remainder which will indicate the sign in which the Shashtiamsa falls."*

S3 renders the reversal instruction as: *"He has listed in a particular order the **names** of the
sixty shashtiamsas falling in odd signs which **order**, he says, should be reversed for even signs."*

S5 corroborates the reversal as applying to the deity sequence: for even signs the sixtieth deity
becomes the first.

### 4.2 The ambiguity, stated precisely

The reversal instruction is attached, in the wording available, to **the order of the names**. The sign
instruction is a separate sentence and says nothing about direction. S3 states outright that the text
**does not clarify** whether the reversal applies to the resulting sign or only to the name ordering.

**A second, independent ambiguity sits in the sign instruction itself.** Read literally, *"ignore the
sign position"* plus *"add 1 to the remainder which will indicate the sign"* yields an **absolute**
sign counted from Aries. But the worked example commonly given alongside it counts the result **from
the natal sign** (Moon at 20°36' in Sagittarius -> ×2 = 41°12' -> 41 mod 12 = 5 -> +1 = 6 -> "sixth
from Sagittarius" -> Taurus). The instruction and its own worked example therefore point at different
origins.

**Inference, labelled as inference, not source fact:** these two axes are independent, giving four
combinations - {origin: Aries | natal sign} × {even signs: forward | reversed}.

### 4.3 Implementation evidence maps exactly onto those four combinations

PyJHora (S2) enumerates precisely four D60 methods, and its code shows they are that Cartesian product:

```python
dirn = -1 if (sign in even_signs and method == PARASARA_EVEN_REVERSE_FROM_SIGN) else 1
seed = 0 if method == PARASARA_CYCLIC_FROM_ARIES else sign
target = (seed + dirn * l) % 12
```

| PyJHora method | Origin | Even signs | Default? |
|---|---|---|---|
| 1 `PARASARA_TRADITIONAL_FROM_SIGN` | natal sign | forward | **yes** |
| 2 `PARASARA_CYCLIC_FROM_ARIES` | Aries | forward | no |
| 3 `PARASARA_EVEN_REVERSE_FROM_ARIES` | Aries | reversed | no |
| 4 `PARASARA_EVEN_REVERSE_FROM_SIGN` | natal sign | reversed | no |

That a mature implementation ships all four, and selects "from sign, forward" as its default, is
evidence that the dispute is live in practice and that no reading has displaced the others.

### 4.4 Competing readings, with the strongest honest case for each

**Reading A - reversal applies to the deity names only; the sign runs forward from the natal sign.**
*Strongest case:* it is the most literal reading of the two sentences as rendered - "order... of the
names" is the grammatical object of "reversed", and the sign sentence carries no directional language
at all. It is PyJHora's default. It matches the roadmap's own primary statement ("Nth sign from the
source, forward"). It keeps D60 in the same shape as every varga this project has already certified.

**Reading B - the reversal applies to the sign sequence as well.** *Strongest case:* the shashtiamsa
and its deity are the same object in the classical scheme; if the deity sequence runs backwards
through an even sign, then the shashtiamsa *positions* run backwards too, and the sign that each
position maps to follows. On this reading, treating the names as reversed while the signs run forward
splits an indivisible construct. PyJHora considers this reading live enough to implement it twice
(methods 3 and 4).

**Reading C - the origin is Aries, not the natal sign.** *Strongest case:* the instruction explicitly
says *"ignore the sign position of a planet"*, which is difficult to reconcile with then counting from
that very sign. On this reading the common worked example is the error, not the instruction.

**Reading D - the origin is the natal sign.** *Strongest case:* the worked examples in circulation
consistently count from the natal sign, and PyJHora's default does the same; "ignore the sign position"
can be read narrowly as "discard the whole-sign component of the longitude before multiplying", which
is arithmetically what the ×2 step needs.

### 4.5 Contradiction, not reconciled

Readings A/B are mutually exclusive; C/D are mutually exclusive; and they are independent, so four
distinct rules are live. **This paper does not choose among them and does not rank them.** The evidence
available - a tertiary paraphrase that flags its own ambiguity, secondary sources speaking only to the
deity order, and an implementation that ships all four - is not sufficient to establish what the
primary text requires.

## 5. D20 findings

### 5.1 Source fact

S4 states the rule in wording that reads as a direct translation: *"The reckoning of Vimsamsa commences
from Aries in movable signs, from Sagittarius in fixed ones and from Leo in signs of dual nature."*
Multiple independent secondary expositions state the same triple and spell out the consequences
(fixed-sign first vimsamsa -> Sagittarius; dual-sign first vimsamsa -> Leo).

S2 (PyJHora) computes exactly this in its Traditional Parasara default:

```python
r = l % 12                                    # movable -> Aries (0)
if sign in dual_signs:    r = (l + HOUSE_5) % 12   # HOUSE_5 = 4 -> Leo
elif sign in fixed_signs: r = (l + HOUSE_9) % 12   # HOUSE_9 = 8 -> Sagittarius
```

Constants verified directly in `src/jhora/const.py`: `HOUSE_5 = 4`, `HOUSE_9 = 8`,
`movable_signs = [0,3,6,9]`, `fixed_signs = [1,4,7,10]`, `dual_signs = [2,5,8,11]`.

### 5.2 The competing reading

A minority rendition gives **movable Aries, fixed Leo, dual Sagittarius** - the fixed and dual starts
transposed. Search across independent expositions surfaced this reading explicitly but attributed it to
a single source against several stating the majority triple.

### 5.3 Competing readings, with the strongest honest case for each

**Reading E - Aries / Sagittarius / Leo (majority).** *Strongest case:* convergent independent
secondary attestation; wording that reads as a direct translation rather than a summary; PyJHora's
default; and agreement with the roadmap's own primary statement.

**Reading F - Aries / Leo / Sagittarius (minority).** *Strongest case:* it is attested, and a minority
reading is not refuted by being outnumbered - this project has repeatedly found the popular reading to
be the copied one. It cannot be dismissed without primary-text access that this paper does not have.

**Observation, labelled inference, not source fact:** Reading F's triple (Aries/Leo/Sagittarius) is
exactly the triple this repository already uses for **D16** (`ADR-0089`) and **D45** (`ADR-0077`). A
plausible explanation is conflation with that far more common pattern. This is a hypothesis about how
an error could arise, **not evidence that Reading F is wrong**, and it must not be treated as
adjudication.

## 6. Implications for implementation, if either were ever selected

Stated for completeness; **nothing here authorizes implementation.**

- **Contract fit is not a blocker for either.** D20 under any triple is a `CyclicVargaRule` with
  `divisions=20`, a 12-entry `start_sign` table and `direction=(1,)*12`. All four D60 variants are also
  expressible: origin is a `start_sign` table choice, and the even-sign reversal is `direction = -1`
  for even signs, which `CyclicVargaRule` permits (its direction is constrained to ±1, confirmed live
  during `DP-032`). **The blocker for both is content, not geometry.**
- **`DP-024` applies to both if either becomes an analytical input**, because D60's shashtiamsa deities
  and D20's vimsamsa deities are exactly the per-division payload `DP-024` concerns. The
  payload-excluded precedent (`ADR-0089` for D16, following `ADR-0082`/`ADR-0087`) is available and
  would avoid `DP-024`, but taking it is an owner decision this paper does not make.
- **Whichever reading is chosen, the rejected ones should be recorded as named, non-claimed variants**,
  matching how `ADR-0082`/`ADR-0087` handled their own excluded variants. That is precedent, not a
  recommendation to proceed.
- D60's width is 0.5° exactly, binary-representable, so it carries none of D27's ULP exposure. D20's
  width is 1.5°, also exact.

## 7. Uncertainty, stated plainly

No primary Sanskrit was located for either question. For D60, the operative wording is available only
through a tertiary paraphrase that explicitly declines to resolve the ambiguity, and the two axes
compound: four live rules, none eliminated. For D20, the majority reading is well corroborated but only
secondarily, and the minority reading is attested rather than refuted. Nothing in this paper should be
read as establishing what BPHS *says*; it establishes what the accessible sources *report*, and where
they disagree.

## 8. Readiness verdicts

**D60 Shashtiamsa: `NOT_READY`.**
Two independent unresolved axes (origin; even-sign direction) produce four live rules. The best
available rendering of the primary instruction is internally inconsistent with its own worked example,
and a tertiary source states outright that the reversal's scope is unspecified. A selection now would
be choosing a convenient source, which the authorizing instruction forbids. This is the same
disposition `DP-032` gave D27, for the same reason.

**D20 Vimsamsa: `REQUIRES_OWNER_ADJUDICATION`.**
The geometry is settled and the contract fits. The evidentiary position for Reading E - convergent
independent secondary attestation plus implementation default, with no primary text - is materially
the same standard the owner already accepted when ratifying D24 (`ADR-0082`) and D40 (`ADR-0087`). It
is therefore adjudicable now, but **only by the owner**, and only as an explicit choice of Reading E
over the attested Reading F, with F recorded as a named excluded variant. The builder does not make
that choice here.

## 9. Owner decisions required

1. **D20:** adopt Reading E (Aries/Sagittarius/Leo) as the selected triple with Reading F recorded as a
   named, non-claimed variant - or decline, and require primary-source work first.
2. **D60:** whether to authorize primary-source research (the `DP-032` Part F treatment given to D27),
   or to shelve D60 until such research is possible, or to accept a named implementation-derived
   variant explicitly as such. This paper recommends none of these.
3. **Payload (`DP-024`):** whether either capability, if ever selected, follows the payload-excluded
   precedent or waits on `DP-024`. Unchanged and still open.

## 10. Recommended next step

The builder's recommendation is confined to **sequencing, not selection**: D20 is the only one of the
two whose evidentiary position is already at the standard the owner has previously accepted, so it is
the one on which an owner decision is possible now. D60 is not, and no amount of further secondary
research is likely to change that - only primary-text access would.

**This paper selects nothing.** Whether to adjudicate D20, and on what basis, is the owner's decision.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-09-05 | Created under the owner's "CEO AUTHORIZATION - DP-035 D60/D20 SOURCE-ADJUDICATION READINESS" instruction. Establishes the source basis for both disputes from PyJHora read directly at source, a tertiary BPHS paraphrase, and convergent secondary expositions; finds D60 carries **two** independent unresolved axes (origin, and whether the even-sign reversal extends beyond the deity names) whose four combinations are exactly the four variants PyJHora ships; finds D20's majority triple (Aries/Sagittarius/Leo) convergently attested with a minority transposition attested but not refuted. Verdicts: D60 `NOT_READY`; D20 `REQUIRES_OWNER_ADJUDICATION`. Decides nothing, selects nothing, freezes nothing, resolves no `DP-024` question. |
