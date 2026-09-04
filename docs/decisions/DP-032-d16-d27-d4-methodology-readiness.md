<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents readiness findings and options. DECIDES NOTHING. Requires owner approval. Does not resolve `DP-024`. Does not select, implement, certify, or CI-wire any capability. Part F (added 2026-09-04) records the owner's authorization of future D27 primary-source research only - not a methodology freeze, not a selection. |
| Version | 1.1.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-09-04 (Part F added: D27 research authorization) |
| Review cadence | TBD |

# DP-032. Combined methodology-readiness investigation: D16 (Shodasamsa), D27 (Saptavimsamsa/Nakshatramsa/Bhamsa), D4 (Chaturthamsa)

## 0. Authorization and scope

Authorized by the owner's explicit "ASTRO CONVERGENCE ENGINE — DP-024 METHODOLOGY-READINESS
INVESTIGATION" instruction (2026-09-04): "Conduct a combined methodology-readiness investigation for
D16, D27 and D4 under `DP-024`... does NOT authorize implementation, production registration,
certification, CI wiring, oracle wiring, or merging any engine capability." This paper performs that
investigation only. It does not implement, register, certify, wire CI/oracle, or select a next
capability. It does not resolve `DP-024`.

**State audit performed before this task began:** branch `main`, HEAD `69aa4bf13542d6d6d3f8e1152a1a95307eb52e26`,
working tree clean, `origin/main` identical. Highest ratified ADR: `ADR-0088`. Highest registered DP
before this paper: `DP-031`. `DP-024` (`Status: OPEN`, unedited since 2026-08-25) remains the governing
framework-question paper this investigation feeds; it is not superseded or resolved here.

**Why these three, together:** `DP-031`'s own candidate table (`docs/decisions/DP-031-...md` §A, rows
3/5/7) marks D16, D27 and D4 "still blocked" for a reason distinct from D20/D60 (disputed classical
content) - all three are blocked *only* on `DP-024`'s own deferred architecture questions. This paper
investigates exactly that subset, per the owner's explicit selection.

## 1. Source-discipline notes, read before anything below

Per the owner's evidence-discipline instruction, every claim below is tagged one of:
**SOURCE FACT** (what a named source states), **DERIVATION** (this paper's own mathematics from a
source fact), **ENGINEERING INFERENCE** (what that means for this codebase), or **RECOMMENDATION**
(a labelled, non-binding suggestion). Software behavior (PyJHora) is never cited as classical
authority - it is corroboration only, exactly as `ADR-0082`/`ADR-0087`/`ADR-0077` already established
for D24/D40/D45.

**PyJHora source** was read directly from `naturalstupid/PyJHora`, GitHub, `src/jhora/horoscope/chart/
charts.py` and `src/jhora/const.py` (fetched fresh this task via `gh api`, not executed - this
project's own local PyJHora environment remains degraded, an unchanged, already-disclosed limitation).
This is independent corroboration of a computational convention, never classical authority.

**Classical/secondary source retrieval** used web search this task (`WebSearch`/`WebFetch`, live
2026-09-04). Every retrieved quotation below is explicitly marked with its retrieval class per section
0's instruction (primary/commentary/secondary/software/informal). None was independently checked
against the original Sanskrit; this is a disclosed gap, matching this project's own established
practice for D24/D40 (`ADR-0082`/`ADR-0087`: "no located verbatim Sanskrit verse... only consistent
paraphrase").

---

# PART A: D4 - Chaturthamsa

## A.A Identity

- **Sanskrit/name:** Chaturthamsa (चतुर्थांश, "fourth part"); also Turyamsa.
- **Conventional English name:** D4 chart, "fourth divisional chart."
- **Purpose/signification:** SOURCE FACT (informal/secondary, multiple convergent modern sources -
  laurabaratastrologer.com, ask-oracle.com, anandamoyee.home.blog, retrieved 2026-09-04): fortune,
  property, immovable assets, and general luck (bhagya). Not independently adjudicated here - purpose
  claims are outside this paper's calculation-methodology scope, recorded only for completeness per
  section A of the task's own template.
- **School/tradition:** Parashara/BPHS, the same source family as every certified `parashara`-school
  varga in this repository (D2, D3, D7, D9, D10, D12, D24, D30, D40, D45).

## A.B Authoritative source basis

| Proposition | Source | Class | Citation |
|---|---|---|---|
| "The Lords of the 4 Kendras from a Rasi are the rulers of respective Chaturthamsa of a Rasi, commencing from Aries" | R. Santhanam's English translation of BPHS, chapter 6, verse 9, as quoted by two independent blog transcriptions | **Secondary, via two independent web transcriptions of a named classical-translation edition** | vedicastroguide.blogspot.com (2012) and yourastroguide.wordpress.com (2012), both retrieved 2026-09-04, quoting identical wording - consistent with both copying the same underlying Santhanam translation rather than being independent primary attestations (per the owner's own "do not treat multiple copies of the same tradition as independent evidence" instruction, these two are treated as **one** source-line, not two) |
| Four Kumara deities (Sanaka, Sanandana, Sanatkumara, Sanatana) preside over the four Chaturthamsa parts, in kendra order | Same translation quotation, plus independently corroborated by three further modern secondary sources (blog.indianastrologysoftware.com, and general reference to the Four Kumaras as a distinct Puranic concept, en.wikipedia.org/wiki/Four_Kumaras) | **Secondary / informal, convergent** | Retrieved 2026-09-04 |
| PyJHora's own coded "Traditional Parasara" `chaturthamsa_chart()` construction | `naturalstupid/PyJHora`, `src/jhora/horoscope/chart/charts.py` lines 631-639, `_chaturthamsa_parasara()` | **Software/reference implementation, corroboration only** | Read directly this task via `gh api repos/naturalstupid/PyJHora/contents/...` |

No primary Sanskrit verse text and no recognized traditional commentary (e.g. a named acharya's bhashya)
was located or verified this task - this is a **disclosed gap**, not a claim that none exists.

## A.C Rule extraction

**Zodiac division structure:** 4 equal parts of 30/4 = 7.5 degrees per sign.

**Starting sign / counting convention:** uniform across all twelve source signs - no odd/even, no
movable/fixed/dual, no triplicity distinction. Division `l` (0-indexed, 0-3) of source sign `s` maps to
target sign `(s + 3*l) mod 12` - i.e. the source sign itself (division 0), then its 4th (division 1),
7th (division 2), and 10th (division 3) houses counted from it (the four kendras from the source sign).

**Degree boundary convention:** not stated by the retrieved source beyond the equal 7.5-degree parts;
this paper assumes the engine's own existing 1e-10 promote-up tolerance convention applies unmodified
(section A.F).

**Exact mathematical mapping (independently derived, not copied from PyJHora):**

```
width = 30 / 4 = 7.5 degrees
for source longitude L in [0, 360):
    source_sign = floor(L / 30)
    degree_in_sign = L - 30*source_sign
    division_index = floor(degree_in_sign / width)      # 0..3
    d_sign = (source_sign + 3 * division_index) mod 12
```

**DERIVATION check against PyJHora's own code** (`_chaturthamsa_parasara`, `f2=3`,
`(sign + l*f2) % 12`): identical to the independent derivation above - `f2=3` is exactly the kendra
step this paper derived from the "commencing from Aries [i.e. the source sign], 4th, 7th, 10th" verse
text, not copied from the code (the code was read after the derivation was written, to check agreement,
matching this project's own established "independent derivation, PyJHora corroborates" discipline).

## A.D Conflict analysis

**No competing PRIMARY-tradition variant was found** for the base Chaturthamsa construction itself -
every retrieved source (all secondary/informal) agrees on the kendra-stepping rule. PyJHora itself lists
three further named *computational* variants (`PARIVRITTI_CYCLIC`, `PARIVRITTI_EVEN_REVERSE`,
`SOMANATHA_PARIVRITTI_ALTERNATE` - `D4_CHART_METHOD` enum, `src/jhora/const.py` line ~1838) alongside
its own default `PARASARA_TRADITIONAL`; no source retrieved this task independently describes these
three as classical alternatives with their own named authority, so they are **not evaluated further** -
excluded as non-default, non-primary computational variants only, exactly the treatment D24/D40/D45
gave their own non-default PyJHora methods.

**Substantive:** no. **Resolvable:** yes, on the evidence gathered - one construction, convergently
attested, though only in secondary form.

## A.E Independent derivation

See section A.C. Derived from the retrieved verse paraphrase ("Lords of the 4 Kendras... commencing
from Aries") independently of PyJHora's code, then cross-checked against it - agreement confirmed
above.

## A.F Boundary analysis

**ENGINEERING INFERENCE, computed fresh this task** (Python, exact `Fraction` arithmetic plus a live
floating-point sweep, mirroring the method `ADR-0083`/`ADR-0087` used for D24/D40):

- `30/4 = 15/2` - denominator is a power of two: **exactly representable in IEEE-754 double**, zero
  representation error.
- Absolute-longitude boundary sweep across all 12 source signs x 4 divisions (48 boundaries): at-exact-
  boundary, 3-ULP-above, and 1e-6-below all classify correctly under the engine's existing 1e-10
  promote-up tolerance. **Zero floor-classification mismatches** - computed directly this task, not
  assumed.
- No retrograde relevance (a divisional-chart sign/degree mapping, not a motion-dependent calculation) -
  matches the treatment every other certified varga in this repository already has.
- No degenerate case identified: 0 degrees (Aries 0.0) and 359.999... both classify without incident in
  the same sweep.

**A future certified implementation must**, per this finding: use the engine's existing promote-up
convention unmodified - no D4-specific boundary exception is needed, matching D24's own "cleaner than
D45" result.

## A.G Oracle / reference feasibility

PyJHora implements `chaturthamsa_chart()` with a directly matching default method (section A.C). Genuine
oracle execution is **not performed this task** (PyJHora unavailable in this local environment, an
already-disclosed, unchanged limitation - the same gap every prior varga readiness/certification stage
in this repository has carried until its own CI-oracle stage). This project's own CI hash-pinned oracle
environment (`.github/workflows/ci.yml`, `requirements-oracle.lock`) is the established path to genuine
execution, exactly as used for D24/D40/D45's own eventual oracle gates - not exercised by this paper.

**Distinguishing corroboration types, per the task's own instruction:** an authoritative textual source
was **not** independently obtained (secondary transcription only, section A.B); an independent from-
scratch implementation was written this task for verification purposes only (section A.C), not as a
certification-grade validator; PyJHora is read-only source corroboration; no reference table was
located.

## A.H Certification readiness

| Requirement (per `docs/VARGA_CERTIFICATION_ROADMAP.md` §6 / `docs/NEW_VARGA_IMPLEMENTATION_TEMPLATE.md`) | Status |
|---|---|
| Explicit rule/school | Yes - `parashara`, kendra-step-3 construction |
| Authoritative reference | **Secondary only** - no primary Sanskrit/verified traditional commentary located |
| Independent derivation | Yes, this paper (section A.E), cross-checked against PyJHora |
| Implementation testability | Yes - deterministic, closed-form |
| Boundary tests | Computed clean this task (section A.F); zero mismatches |
| Oracle/reference comparison | PyJHora available as corroboration; not executed (environment gap, deferred to CI as with every sibling capability) |
| Protected holdout feasibility | Yes - identical mechanism to every certified `CyclicVargaRule` varga, once the rule is expressible (see below) |
| Negative controls / mutation detection | Yes - identical mechanism to D24/D40/D45's own established pattern |
| Provenance | Yes - `parashara` school, kendra-step-3, cited above |
| Variant handling | Base construction unanimous across retrieved sources; three non-default PyJHora computational variants excludable as non-claims |
| Reproducibility | Yes - closed-form, deterministic |
| **Architectural fit (`CyclicVargaRule`)** | **NO - genuinely blocked.** Confirmed by direct code inspection (`engine/astrology/varga_rules.py` `CyclicVargaRule.__post_init__`, `engine/astrology/varga_classifier.py::_classify_cyclic`): `direction[source_sign]` is constrained to exactly `+1` or `-1` (`InvalidVargaRuleError` otherwise), and `d_sign = (start + step*index) % 12` uses that single-sign step for every division increment. D4's own construction needs a 3-sign step per division - **not expressible by the current contract as coded**, contrary to `engine/astrology/varga_rules.py`'s own module docstring, which lists D4 among the vargas `CyclicVargaRule` "covers" (line ~10). **This is a genuine documentation inaccuracy, found and disclosed this task, not fixed** (out of this paper's authorized scope - a documentation-only fix to that module docstring would itself be a source-code change, not authorized here). |
| **Payload gap** | **Newly found, not previously flagged.** `docs/VARGA_CERTIFICATION_ROADMAP.md` §3's own payload-gap list names only D16/D20/D27/D60 - it does **not** name D4. Section A.B above independently establishes D4 carries its own named per-division deity payload (the four Kumaras, one per kendra part), convergently attested by multiple secondary sources. **The roadmap's own payload-gap enumeration is therefore incomplete** - a genuine finding, reported per the task's "document, do not fix" instruction. Whether this payload is IN the certified contract is a policy choice, not a calculation question: every varga certified in this repository to date (D2/D3/D7/D9/D10/D12/D24/D30/D40/D45) excludes deity/payload output from `VargaClassification` as an explicit non-claim, so D4 could follow the identical precedent - but that precedent decision has never been made for D4 specifically, and this paper does not make it. |

**`DP-024` applicability for D4:** genuinely blocks the D-sign geometry (Option A - the `step` field, or
Option A2's `SegmentVargaRule` workaround, 48 cells, "exactly as D3 did" per `DP-024` §4). If deity
output is ever required as a certified claim, Option B also applies; if deity output is excluded (as it
was for every sibling varga), Option B does not block D4.

## A.I Readiness verdict

**D4: REQUIRES_OWNER_ADJUDICATION.**

Not `NOT_READY` (the astrological methodology itself is convergently attested and cleanly boundary-
tested) and not `READY_FOR_SELECTION` (a real architectural blocker exists that the owner, not this
paper, must resolve): `CyclicVargaRule` cannot express D4's construction as coded today. The owner must
choose between `DP-024` Option A1 (add the `step` field - benefits every future kendra/trikona-stepped
division, needs its own ADR and non-invasiveness proof) or Option A2 (`SegmentVargaRule`, 48 cells, no
framework change, larger/harder-to-audit table, precisely D3's own precedent) before D4 can proceed to
a selection ADR. This is exactly the choice `DP-024` §4 already framed - this paper adds no new option,
only confirms (by direct code inspection, not merely by citing `DP-024`'s own prose) that the blocker is
real and supplies the newly-found deity-payload disclosure gap above.

---

# PART B: D16 - Shodasamsa

## B.A Identity

- **Sanskrit/name:** Shodasamsa (षोडशांश, "sixteenth part"); also called Kalamsa.
- **Conventional English name:** D16 chart.
- **Purpose/signification:** SOURCE FACT (informal/secondary, convergent - jagannathhora.com,
  astrosight.ai, bejandaruwalla.com, retrieved 2026-09-04): vehicles, comforts, luxuries, general
  happiness. Recorded for completeness only, not adjudicated.
- **School/tradition:** Parashara/BPHS.

## B.B Authoritative source basis

| Proposition | Source | Class | Citation |
|---|---|---|---|
| "The Shodasamsa should be known as commencing from Aries in movable sign, from Leo in a fixed sign and from Sagittarius in dual sign" | R. Santhanam BPHS translation, chapter 6, verse ~16, per two independent blog transcriptions | **Secondary, one source-line (two copies of the same translation, per the "no double-counting copies" instruction)** | vedicastroguide.blogspot.com, yourastroguide.wordpress.com, retrieved 2026-09-04 |
| Movable->Aries/Fixed->Leo/Dual->Sagittarius, independently re-stated with per-category breakdown, "each part = 1 deg 52' 30\"" | Aggregated web search across multiple independent secondary astrology-reference sites | **Secondary, informal, convergent (multiple independent sites, not merely copies of one blog)** | Search retrieved 2026-09-04 (indianastrologysoftware.com, astrologyinquirer.com, cosmicsquares.com, jagannathhora.com, among others) |
| Deities: "Brahma, Vishnu, Shiva and Sun," cycling four times through the sixteen parts for odd signs, reversed for even signs | Same blog transcription as row 1 | **Secondary, one source-line** | Retrieved 2026-09-04 |
| PyJHora's own coded "Traditional Parasara" `shodasamsa_chart()` construction | `src/jhora/horoscope/chart/charts.py` lines 980-1016 | **Software, corroboration only** | Read directly this task |

No primary Sanskrit or traditional commentary located - disclosed gap, matching D24/D40's own precedent
disclosure.

## B.C Rule extraction

**Zodiac division structure:** 16 equal parts of 30/16 = 1.875 degrees per sign.

**Starting sign / counting convention, by triplicity of the source sign (movable/fixed/dual):**
- Movable (Aries, Cancer, Libra, Capricorn): division `l` -> target sign `l mod 12` (start Aries).
- Fixed (Taurus, Leo, Scorpio, Aquarius): division `l` -> target sign `(l + 4) mod 12` (start Leo,
  0-based index 4).
- Dual (Gemini, Virgo, Sagittarius, Pisces): division `l` -> target sign `(l + 8) mod 12` (start
  Sagittarius, 0-based index 8).

Forward counting only (`direction = +1` for all 12 source signs) - no reversal variant in the retrieved
primary-line source; PyJHora's own default agrees (`PARASARA_TRADITIONAL`, no `dirn` variable used in
`shodasamsa_chart`, unlike D12's own explicit even-sign-reversal branch).

**Exact mathematical mapping (independently derived):**

```
width = 30 / 16 = 1.875 degrees
starts = {movable: 0 (Aries), fixed: 4 (Leo), dual: 8 (Sagittarius)}
for source longitude L:
    source_sign = floor(L / 30); degree = L - 30*source_sign
    division_index = floor(degree / width)                # 0..15
    base = starts[triplicity(source_sign)]
    d_sign = (base + division_index) mod 12
```

**DERIVATION check against PyJHora:** `r = l%12` for movable (base 0, matches Aries); `r=(l+HOUSE_5)%12`
for fixed where `HOUSE_5=4` (`src/jhora/const.py` line 164, confirmed by direct read: `HOUSE_5 = 4`) -
matches Leo (0-based index 4); `r=(l+HOUSE_9)%12` for dual where `HOUSE_9=8` (same constants file) -
matches Sagittarius (0-based index 8). **Exact agreement** with the independent derivation above.

## B.D Conflict analysis

**No substantive conflict found.** Every retrieved source (multiple independent sites, not one copied
blog) agrees on movable/fixed/dual -> Aries/Leo/Sagittarius. PyJHora lists three further non-default
computational variants (`PARIVRITTI_EVEN_REVERSE`, `PARIVRITTI_CYCLIC`, `SOMANATHA_PARIVRITTI_ALTERNATE`)
with no independent classical attestation found this task - excluded as non-claims, same treatment as
every sibling certified varga's own non-default methods.

## B.E Independent derivation

See section B.C - derived from the retrieved verse paraphrase, independent of PyJHora's code, then
cross-checked (exact agreement, including the numeric `HOUSE_5`/`HOUSE_9` constants independently
re-derived as "5th sign from Aries = Leo" and "9th sign from Aries = Sagittarius" by direct 0-based
counting, not copied).

## B.F Boundary analysis

**ENGINEERING INFERENCE, computed fresh this task:**

- `30/16 = 15/8` - denominator is a power of two: **exactly representable**, zero representation error.
- Absolute-longitude boundary sweep, all 12 source signs x 16 divisions (192 boundaries): at-boundary,
  3-ULP-above, and 1e-6-below all classify correctly under the existing 1e-10 promote-up tolerance.
  **Zero mismatches.**
- No retrograde relevance; no degenerate case found.

## B.G Oracle / reference feasibility

PyJHora implements `shodasamsa_chart()` (alias `kalamsa_chart()`) with a directly matching default
method. Not executed this task (environment gap, disclosed). No primary textual source or independent
reference table located beyond the secondary transcriptions above.

## B.H Certification readiness

| Requirement | Status |
|---|---|
| Explicit rule/school | Yes - `parashara`, movable/fixed/dual triple-start |
| Authoritative reference | Secondary only (as D4) |
| Independent derivation | Yes, cross-checked against PyJHora, exact agreement |
| Boundary tests | Computed clean this task; zero mismatches |
| Oracle/reference comparison | PyJHora available as corroboration; not executed |
| Provenance/variant handling | Base construction unanimous; three non-default PyJHora variants excludable |
| **Architectural fit (`CyclicVargaRule`)** | **YES - fits the current contract exactly**, confirmed by direct code inspection. A 12-entry `start_sign` table with `start_sign[s] = 0` for movable, `4` for fixed, `8` for dual (exactly the same table SHAPE D16/D24/D40/D45 already use for their own triplicity/parity-based starts) and `direction = (1,)*12` expresses this construction with **no new field, no `step`, no `SegmentVargaRule`**. This is a materially different finding from D4: D16 needs **no** `DP-024` Option A resolution at all. |
| **Payload gap** | **Confirmed real, matches the roadmap's own claim.** The Brahma/Vishnu/Shiva/Sun deity cycle (reversed for even signs) is a named per-division payload `VargaClassification` cannot express, exactly as `docs/VARGA_CERTIFICATION_ROADMAP.md` §3 already states for D16. If deity output is excluded from the certified contract - the precedent every sibling certified varga already follows - this blocker does not apply to the D-sign geometry itself. |

**`DP-024` applicability for D16:** **Option B only** (payload/label-table question), and only if deity
output is ever required as a certified claim. The geometry itself needs no `DP-024` resolution -
`CyclicVargaRule` already expresses it, a materially cleaner finding than D4's.

## B.I Readiness verdict

**D16: READY_FOR_SELECTION**, on the geometry/calculation methodology, **conditional on the owner
accepting the same deity-exclusion precedent every other certified varga in this repository already
uses** (D-sign/division-index/fraction only, no deity output claimed). This is not a new decision this
paper invents - it is the SAME non-claim `ADR-0082`/`ADR-0087`/`ADR-0077` already recorded for D24/D40/
D45's own real classical deity traditions. If the owner instead wants deity/payload output as part of a
certified D16, that is a `DP-024` Option B decision this paper does not make, and D16 would then be
`REQUIRES_OWNER_ADJUDICATION` on that narrower question only.

---

# PART C: D27 - Saptavimsamsa / Nakshatramsa / Bhamsa

## C.A Identity

- **Sanskrit/name:** Saptavimsamsa (सप्तविंशांश, "twenty-seventh part"); also Nakshatramsa (nakshatra-
  linked naming) and Bhamsa.
- **Conventional English name:** D27 chart.
- **Purpose/signification:** SOURCE FACT (informal/secondary, convergent - cosmicsquares.com,
  cosmicinsights.net, retrieved 2026-09-04): physical strength, stamina, resilience under stress.
  Recorded for completeness, not adjudicated.
- **School/tradition:** Parashara/BPHS.

## C.B Authoritative source basis

| Proposition | Source | Class | Citation |
|---|---|---|---|
| "The Saptavimshamsa distribution commences from Aries and other Movable Rasis for all the 12 Rasis" (verses 24-26) | R. Santhanam BPHS translation, per two independent blog transcriptions | **Secondary, one source-line** | vedicastroguide.blogspot.com, yourastroguide.wordpress.com, retrieved 2026-09-04 |
| Fire signs (Aries/Leo/Sagittarius) start Aries; Earth (Taurus/Virgo/Capricorn) start Cancer; Air (Gemini/Libra/Aquarius) start Libra; Water (Cancer/Scorpio/Pisces) start Capricorn | Aggregated web search, multiple independent secondary sites | **Secondary, informal, convergent (multiple independent sites)** | jagannathhora.com, barbarapijan.com, blog.indianastrologysoftware.com, cosmicinsights.net, retrieved 2026-09-04 |
| Twenty-seven nakshatra-presiding deities as per-division lords, beginning Ashvini Kumaras/Yama/Agni/Brahma..., reversed for even signs | Same blog transcription as row 1 | **Secondary, one source-line** | Retrieved 2026-09-04 |
| PyJHora's own coded "Traditional Parasara" `nakshatramsa_chart()` construction | `src/jhora/horoscope/chart/charts.py` lines 1085-1120 | **Software, corroboration only** | Read directly this task |

## C.D Conflict analysis - performed BEFORE section C.C, because it governs which rule is extracted

**A genuine, disclosed textual ambiguity was found**, not silently resolved:

- **Variant 1 (fire/earth/air/water, triplicity-based four-way start):** independently corroborated by
  *multiple, distinct* secondary sites (not copies of one source) and matches PyJHora's own coded
  default exactly.
- **Variant 2 (a single "commences from Aries... for all the 12 Rasis" reading):** the retrieved
  Santhanam-translation quotation (verses 24-26), read literally, could describe a single Aries-start
  rule applied uniformly, rather than a four-way triplicity split - this literal reading would be
  **materially different** from Variant 1 for 9 of 12 source signs.

**Resolution attempted, not assumed:** this paper does **not** have independent access to the primary
Sanskrit or a verified complete English critical edition of BPHS chapter 6 verses 24-26 - a disclosed
gap. Weighing the evidence available:
1. Variant 1 is corroborated by *several independent, non-copying* modern sources, converging
   independently on the identical four-way scheme (fire->Aries, earth->Cancer, air->Libra,
   water->Capricorn) - a materially different, stronger convergence pattern than a single quoted
   sentence.
2. Variant 2's own wording ("commences from Aries **and other** Movable Rasis") is grammatically
   consistent with a compressed/paraphrased translation of a more structured verse that a terse modern
   English rendering could plausibly compress - this paper cannot rule this out, but notes no
   independent source corroborates a genuine "single Aries-start for all signs" tradition as an
   alternative school (unlike, e.g., D20's or D60's own genuinely two-sided, independently-argued
   disputes, which `docs/VARGA_CERTIFICATION_ROADMAP.md` §4 already documents by name).
3. **This paper's own engineering inference:** Variant 2, taken completely literally, is unlikely to be
   the intended classical rule as commonly transmitted - but this is a plausibility judgment, not a
   verified resolution.

**Is the conflict substantive?** Yes, if Variant 2 is read literally. **Does one variant have stronger
authority?** Variant 1 has stronger *convergent secondary* corroboration; neither variant has verified
*primary* authority in this paper's evidence. **Can the conflict be legitimately resolved by this
paper?** **No - marked unresolved.** This paper does not select Variant 1 by default; it flags the
ambiguity for the owner and, separately, for whoever eventually drafts D27's own selection/methodology
ADR, exactly as `ADR-0082`/`ADR-0087` disclosed their own "paraphrase-only, no verbatim Sanskrit"
caveats rather than asserting false certainty.

## C.C Rule extraction (Variant 1, the better-corroborated reading, extracted for analysis purposes only - NOT thereby adopted as decided)

**Zodiac division structure:** 27 equal parts of 30/27 = 10/9 = 1.1111... degrees per sign.

**Starting sign / counting convention, by element (triplicity) of the source sign:**
- Fire (Aries, Leo, Sagittarius): division `l` -> target `l mod 12` (start Aries, index 0).
- Earth (Taurus, Virgo, Capricorn): division `l` -> target `(l + 3) mod 12` (start Cancer, index 3).
- Air (Gemini, Libra, Aquarius): division `l` -> target `(l + 6) mod 12` (start Libra, index 6).
- Water (Cancer, Scorpio, Pisces): division `l` -> target `(l + 9) mod 12` (start Capricorn, index 9).

**DERIVATION check against PyJHora:** `r=l%12` fire (Aries, index 0); `r=(l+HOUSE_4)%12` earth where
`HOUSE_4=3` (Cancer, index 3); `r=(l+HOUSE_7)%12` air where `HOUSE_7=6` (Libra, index 6);
`r=(l+HOUSE_10)%12` water where `HOUSE_10=9` (Capricorn, index 9) - all confirmed by direct read of
`src/jhora/const.py` line 164-165. **Exact agreement** with the independent derivation.

## C.E Independent derivation

Derived from the fire/earth/air/water convergent-secondary-source reading (section C.B row 2),
independent of PyJHora's code, then cross-checked - exact agreement, as C.C states.

## C.F Boundary analysis

**ENGINEERING INFERENCE, computed fresh this task** (relevant regardless of which conflict-analysis
variant is eventually adopted, since both variants share the same 27-way, 30/27-degree division width):

- `30/27 = 10/9` - denominator (9) is **not** a power of two: **not exactly representable** in
  IEEE-754 double, confirmed by direct computation (`Fraction(30,27)` reduces to `10/9`; `10/9` is not a
  dyadic rational). This is the **same representability class as D7 and D9** (`docs/
  VARGA_CERTIFICATION_ROADMAP.md`'s own "width note," now independently confirmed by fresh computation
  rather than merely cited).
- Despite the non-representable width, the **absolute-longitude boundary sweep across all 12 source
  signs x 27 divisions (324 boundaries)** - at-boundary, 3-ULP-above, and 1e-6-below - produced **zero
  floor-classification mismatches** under the engine's existing 1e-10 promote-up tolerance, computed
  fresh this task. This is a materially cleaner empirical result than D45's own three genuine mismatches
  (k=13, 26, 29) despite sharing the "non-representable width" risk category - the tolerance already
  absorbs D27's own rounding error at every internal boundary tested.
- No retrograde relevance; no degenerate case found.

**A future certified implementation must** independently re-verify this boundary result once the
conflict in section C.D is resolved (the boundary positions themselves are identical under both
variants - only the target-sign mapping differs - so this finding is unaffected by which variant is
eventually adopted).

## C.G Oracle / reference feasibility

PyJHora implements `nakshatramsa_chart()` with a default method matching Variant 1. Not executed this
task (environment gap, disclosed). No primary textual source or verified reference table located.
**If Variant 2 turns out to be the correct classical reading, PyJHora's own default would then be
corroborating the WRONG variant** - a risk this paper flags explicitly rather than glossing over,
exactly the caution the owner's "do not call software agreement proof of classical correctness"
instruction requires.

## C.H Certification readiness

| Requirement | Status |
|---|---|
| Explicit rule/school | **Ambiguous** pending section C.D's unresolved conflict |
| Authoritative reference | Secondary only, and internally ambiguous on the one point that matters most (section C.D) |
| Independent derivation | Performed for Variant 1 only (section C.E); Variant 2 not derivable without further primary-source access |
| Boundary tests | Computed clean this task for the shared 27-way division geometry; zero mismatches (unaffected by the C.D conflict) |
| Oracle/reference comparison | PyJHora corroborates Variant 1 only - not dispositive per section C.G |
| **Architectural fit (`CyclicVargaRule`)** | **YES for Variant 1** (four-way `start_sign` table, exactly like D16's own triplicity table - no `step` field needed), confirmed by direct code inspection. Variant 2, if adopted, would need re-derivation but is *simpler* geometrically (a single start value), so it would also fit `CyclicVargaRule` with no framework change. **Either way, no `DP-024` Option A resolution is needed for D27.** |
| **Payload gap** | Confirmed real, matches the roadmap's own claim - 27 nakshatra-lord deities, a named per-division payload `VargaClassification` cannot express. Same exclusion-precedent option as D16/D4 above. |

**`DP-024` applicability for D27:** **Option B only** (payload), same as D16 - **not** blocked by the
`step`-field/geometry question. D27's own blocker, uniquely among these three, is **the unresolved
source-conflict in section C.D**, which `DP-024` does not cover at all (`DP-024` is a framework/contract
question, not a classical-content dispute) - this is closer in kind to D20/D60's own disputed-content
blocker than to a pure `DP-024` architecture question, a distinction this paper flags because the
original task authorization grouped D27 with D4/D16 as "`DP-024`-only" blocked, and this paper's own
findings show that grouping is not entirely accurate for D27.

## C.I Readiness verdict

**D27: NOT_READY.**

Not `REQUIRES_OWNER_ADJUDICATION` in the narrow `DP-024` sense (the payload question alone would make it
that, matching D16), because D27 additionally carries an **unresolved source-conflict this paper could
not close from available evidence** (section C.D) - a correctness-methodology gap, not merely an
architecture-policy choice. Selecting D27 next would require either (a) obtaining reliable access to a
verified primary or critical-edition source to resolve the Variant 1/Variant 2 conflict, or (b) an
explicit owner decision to proceed on Variant 1's convergent-secondary-source weight alone, accepting
the disclosed risk that PyJHora's own oracle corroboration would then be corroborating the same
unverified variant, not an independent check of it. This paper does not recommend (b) merely to make
D27 selectable, per the owner's own standing instruction not to manufacture confidence.

---

# PART D: Combined comparison

| Axis | D16 | D27 | D4 |
|---|---|---|---|
| Source certainty | Secondary only, but internally consistent across all retrieved sources | Secondary only, **internally conflicting** on the starting-sign rule (section C.D) | Secondary only, internally consistent |
| Rule ambiguity | None found | **Genuine, unresolved** (two readings, section C.D) | None found |
| Variant burden (non-default PyJHora methods) | 3, none independently attested as classical | 2, one of which (`PARASARA_EVEN_REVERSE`) is a computational variant only | 3, none independently attested as classical |
| Derivation clarity | Clean, exact agreement with PyJHora | Clean **for Variant 1 only**; Variant 2 not derivable without more source access | Clean, exact agreement with PyJHora |
| Boundary complexity | Exactly representable width (30/16); zero mismatches | **Not** exactly representable (30/27 = 10/9, same class as D7/D9); zero mismatches anyway, computed fresh | Exactly representable width (30/4); zero mismatches |
| Independent reference availability | PyJHora only, not executed | PyJHora only, not executed, and corroborates only one of two candidate readings | PyJHora only, not executed |
| Certification difficulty (methodology) | Low, once payload question is resolved/excluded | **Higher** - the C.D conflict must close first, independent of `DP-024` | Low, once the geometry blocker (below) is resolved |
| Architectural dependency (`DP-024`) | **None for geometry** - fits `CyclicVargaRule` today; payload (Option B) only if deity output is claimed | **None for geometry** - fits `CyclicVargaRule` today (either variant); payload (Option B) only if deity output is claimed | **Real geometry blocker** - needs Option A (`step` field) or the `SegmentVargaRule` workaround; independently confirmed by code inspection, not merely `DP-024`'s own prose |
| Risk of methodology dispute | Low | **High** (section C.D) | Low |
| Suitability as next JATAKA capability | Highest of the three, conditional on the deity-exclusion precedent | Lowest of the three - a genuine open question this paper could not close | Second - blocked on a real but well-understood, already-precedented architecture choice (D3's own `SegmentVargaRule` history) |

**Which are ready for owner selection, which require adjudication, which are blocked:**
- **Ready for owner selection (on the calculation methodology), pending only the standard deity-
  exclusion precedent the owner would be adopting for the Nth time, not the 1st:** D16.
- **Require owner adjudication before a selection ADR could be drafted:** D4 (choose `DP-024` Option A1
  vs A2), and D16/D27 only if the owner wants deity/payload output as a certified claim rather than
  excluded (Option B).
- **Blocked, not merely pending a choice:** D27, on the unresolved section C.D source conflict - this
  is not a `DP-024` question and this paper does not recommend proceeding on unverified evidence.

This paper does **not** choose the next JATAKA capability. If forced to rank readiness only (not a
recommendation to select), the order is **D16, then D4, then D27** - matching `docs/
VARGA_CERTIFICATION_ROADMAP.md` §5's own risk ordering ("D24 and D40, the parity family" ahead of "D20...
D27, which needs the ULP-sensitive width treatment... D4, which needs either the segment table or the
step field decision" placed D27 and D4 in a similar late position; this paper's own finding refines that
- D16 turns out cleaner than the roadmap's un-differentiated grouping suggested, and D27 carries a risk
the roadmap's own text did not previously identify by name).

---

# PART E: Owner decision package

1. **Is `DP-024` sufficiently resolved for D16?** Not by this paper (it decides nothing). This paper
   establishes: D16's geometry needs no `DP-024` resolution at all; only the payload question (Option B)
   applies, and only if deity output is to be a certified claim.
2. **Is `DP-024` sufficiently resolved for D27?** Same answer for the geometry as D16 - no `DP-024`
   Option A question exists for D27. But D27 carries its own, separate, non-`DP-024` blocker (section
   C.D) this paper could not resolve.
3. **Is `DP-024` sufficiently resolved for D4?** No - D4 genuinely needs Option A (step field) or A2
   (`SegmentVargaRule`) resolved before its geometry is expressible at all, confirmed by direct code
   inspection this task, not merely asserted.
4. **Which methodological variants exist?** Documented per division in sections A.D/B.D/C.D. D4 and D16:
   no substantive primary-tradition variant found (only non-attested PyJHora computational alternates).
   D27: a genuine, unresolved two-reading conflict (section C.D).
5. **Which variants, if any, have sufficient authority to adopt?** D4's and D16's single retrieved
   constructions are adoptable at the same evidentiary standard D24/D40 already used (secondary-only,
   disclosed as such). D27's Variant 1 has stronger convergent-secondary support than Variant 2 but
   neither is verified against primary text - this paper does not recommend adopting either without
   further source work or an explicit owner risk-acceptance decision.
6. **Which capabilities can proceed to a future selection ADR?** D16, once the owner confirms the
   deity-exclusion precedent applies (or separately resolves `DP-024` Option B for it). D4, once the
   owner resolves `DP-024` Option A/A2 for it specifically (this paper does not require a *general*
   framework decision - Option A2, `SegmentVargaRule`, needs no framework change at all, mirroring D3's
   own precedent exactly).
7. **Which remain blocked and why?** D27 - a source-conflict this paper could not close, independent of
   `DP-024`. Neither D16 nor D4 is "blocked" in that sense; both have a well-understood, named, resolvable
   question awaiting the owner's decision, not an open dispute.
8. **What exact questions still require owner adjudication?**
   a. For D4: `DP-024` Option A1 (add the `step` field, benefits future kendra/trikona vargas, needs its
      own ADR and non-invasiveness proof) vs Option A2 (`SegmentVargaRule`, 48 cells, no framework
      change, D3's own precedent) vs deferring D4 entirely.
   b. For D16 and D4 (and D27 if C.D is later resolved): whether the newly-disclosed D4 deity payload
      (section A.H) and D16/D27's own already-known deity payloads are excluded from the certified
      contract (matching every sibling certified varga) or require `DP-024` Option B resolution first.
   c. For D27 specifically: whether to commission further primary-source research to resolve section
      C.D before any selection ADR, or to accept Variant 1 on its convergent-secondary weight with the
      disclosed risk stated in section C.G, or to defer D27 indefinitely.
   d. Whether any of D16/D27/D4 should be selected next at all, versus another JATAKA candidate
      (`DP-031` §I items 3-6 remain separately open, unaffected by this paper).

## Part F: D27 research authorization (addendum, 2026-09-04) - NOT a methodology freeze

**Owner instruction, quoted in full part:** "OWNER RATIFICATION - PROCEED WITH ALL THREE, WITH THE
FOLLOWING BOUNDARIES" (2026-09-04), item 3: "Proceed with D27 as a research candidate. Authorize further
primary-source research specifically to resolve the Variant 1 vs Variant 2 source conflict. Do NOT
select either interpretation merely because PyJHora or secondary sources favor it. D27 must remain
blocked from methodology freeze/implementation until the source conflict is properly resolved or I
separately provide explicit risk-acceptance authorization. PyJHora remains corroborative evidence, not
normative authority."

**What this addendum records:** the owner has authorized a **future, separate research task** to attempt
to resolve section C.D's own disclosed conflict (the "commences from Aries... for all the 12 Rasis"
reading vs. the fire/earth/air/water triplicity reading) against better primary-source evidence than this
paper obtained. **This authorization is not itself that research** - no such research is performed by
this addendum, and section C.D's conflict remains exactly as unresolved as this paper's own 1.0.0 version
left it. No interpretation is selected here, by PyJHora's default or by Variant 1's stronger convergent-
secondary count, per the owner's own explicit instruction.

**What remains true regardless of this addendum:** D27 is a JATAKA research candidate, not a selected
capability - unlike D16 (`ADR-0089`, PROPOSED) and D4 (`ADR-0090`, PROPOSED), **no selection or frozen-
methodology ADR is drafted for D27 by this addendum or by any other record as of this entry.** D27 may
not proceed to methodology freeze, certification design, or implementation until section C.D is resolved
by one of the two paths section C.G/Part E already named: genuine primary-source verification, or the
owner's own explicit, separate risk-acceptance authorization naming Variant 1 (or Variant 2) and
disclosing the residual risk. Neither has occurred as of this entry.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.1.0 | 2026-09-04 | Part F added (append-only; Parts A-E and the 1.0.0 change-history row below unedited, confirmed by diff): records the owner's explicit authorization of future D27 primary-source research to resolve section C.D's conflict, per "OWNER RATIFICATION - PROCEED WITH ALL THREE" item 3. Explicitly NOT a methodology freeze, NOT a selection, and does not perform the authorized research itself - section C.D remains exactly as unresolved as version 1.0.0 left it. Companion to `ADR-0089` (D16) and `ADR-0090` (D4), both drafted `PROPOSED` this same task, neither yet ratified. |
| 1.0.0 | 2026-09-04 | Created. Combined methodology-readiness investigation for D16, D27, D4 under the owner's explicit "DP-024 METHODOLOGY-READINESS INVESTIGATION" authorization. Establishes D16 geometry needs no `DP-024` resolution (payload/Option B only); D4 genuinely needs Option A/A2; D27 needs neither `DP-024` option for its geometry but carries its own unresolved source-conflict (section C.D) this paper could not close. Discloses a previously-unflagged D4 deity payload and a `varga_rules.py` module-docstring inaccuracy (lists D4 as `CyclicVargaRule`-covered; the enforced `direction in {+1,-1}` constraint contradicts this for D4's real 3-sign step). Decides nothing; selects nothing; implements nothing; does not resolve `DP-024`. |
