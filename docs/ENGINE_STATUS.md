<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | CURRENT - regenerate on every certified change. Reconciled against live repository evidence 2026-09-05 per `ADR-0093`. Section 6's machine-readable capability block is now mechanically enforced against live sources by `scripts/check_capability_state.py` (`ADR-0094`); **the prose in sections 1-5 is not machine-checked and remains a manual discipline.** |
| Version | 2.4.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-09-07 (D20 PRODUCTION-REGISTERED under `ADR-0095`; registry now nine divisions) |
| Review cadence | TBD (see docs/OPEN_QUESTIONS.md Q1) |

# Consolidated engine status

Date: 2026-09-05
Authoritative commit: 27ba54f8ed42950c779c168ee1a1728200e10b18 (branch `dp032-d16-d27-d4-methodology-readiness`; the 2026-08-09 statement below was compiled against origin/main `61733f342c0cc9eabb71139d3fb90a365ede2118` and is superseded by this reconciliation, `ADR-0093`)
Purpose: the single current-state document for this project. Supersedes nothing; the per-phase ADR plans in `claude/` remain the decision record, and the repository's own certification artifacts remain the evidence. Every figure below was reproduced by execution on a fresh clone of origin/main, not copied from documentation.

## 1. How to verify everything in one sitting

Clone the repository, install the pinned dependencies (`pyswisseph==2.10.3.2`, `pytest==9.1.1`, `tzdata==2025.2`; PyJHora plus its dependencies only if you intend to run the oracle certifiers), then run the default gate, the independent holdout validators, the legacy gate, and the certification runners. The README lists every command. Current reproduced results (2026-09-05): **967 tests pass**; **21 registered validator sources** and **22 registered certifier sources** (`scripts/certification_support.py`'s `VALIDATOR_SOURCES` / `CERTIFIER_SOURCES`); the legacy gate passes 5 of 5. The oracle-tier and `swetest`-dependent runners cannot execute on a Windows host - a documented, permanent platform limitation, not a regression - so full-battery regeneration is confirmed in CI rather than locally. The stored certification JSON files are never accepted as proof; each runner rebuilds its artifact from scratch on every invocation.

## 2. Certified layers

The astronomical kernel is locked and Tier-0 certified. It runs strict Swiss Ephemeris with return-flag inspection so a silent Moshier fallback raises instead of returning mislabelled data, computes a fully sidereal frame including ascendant and cusps, resolves civil time through IANA zones with DST, fold, and historical-offset handling, and stamps every snapshot with provenance recording profile, ayanamsa, frame, house system, node policy, ephemeris mode, and time basis. Certification evidence is the frozen eleven-case holdout matrix run against the bundled swetest 2.10.03 binary under both ratified profiles, 528 comparisons, maximum error 0.000180 arcsecond.

Two calculation profiles are ratified by recorded human sign-off and are the only path to an ayanamsa: `parashari_lahiri` (Lahiri) and `kp_krishnamurti` (Krishnamurti). They are mechanically proven to drive the computation, differing by the expected 5.811 arcminutes. Cross-system reuse of a snapshot computed under the other profile is forbidden, and the KP, dasha, and Parashari layers each enforce that in code by rejecting foreign-profile snapshots.

Divisional charts: D1 Rashi with the documented whole-sign house rule, plus certified D9 Navamsa and D10 Dashamsa served by their own hard-wired production modules, never through the generic registry. **Nine further vargas are certified AND production-registered** through the Generic Varga registry under the `parashara` school key: D2 Hora (`ADR-0011`), D3 Drekkana (`ADR-0009`), D7 Saptamsa (`ADR-0011`), D12 Dwadasamsa (`ADR-0010`), D20 Vimsamsa (`ADR-0095`), D24 Siddhamsa (`ADR-0083`), D30 Trimsamsa (`ADR-0011`), D40 Khavedamsa (`ADR-0087`), and D45 Akshavedamsa (`ADR-0077`). Each carries its own ADR, dual-transcribed frozen rule table, dense sweep, ULP boundary battery, external oracle agreement or a disclosed corroboration gap, independent validator, and certification artifact. The sanctioned registry contents live in the single constant `engine.astrology.CERTIFIED_PRODUCTION_VARGAS`; every unregistered division still raises `UnsupportedVargaError` by design.

**Certified but NOT production-registered: D16 Shodasamsa (`ADR-0089`) and D4 Chaturthamsa (`ADR-0090`).** Both hold PASS certification artifacts (`certification/VARGA_D16_V1_certification.json`, `certification/VARGA_D4_V1_certification.json`), produced against standalone rules instantiated inside their own certifier scripts. Neither has a production module, neither appears in `CERTIFIED_PRODUCTION_VARGAS`, and neither is wired into CI. `divisional_chart(snapshot, 16)` and `divisional_chart(snapshot, 4)` therefore raise `UnsupportedVargaError`, correctly. **Production implementation for both is a separate, not-yet-given authorization.** D20 followed exactly this path and has since been production-registered under `ADR-0095`. Certification is not registration, and this repository does not treat it as such.

The KP layer (`engine/kp/`) provides exact-rational lordship chains (sign lord, star lord, sub lord, sub-sub lord) and KP fact charts under the KP profile, proven equivalent to the certified legacy kernel with zero categorical mismatches across a 51,429-point sweep, 19,679 boundary points, an eleven-case chart holdout, and the 200-field transcribed fixture set.

The dasha layer (`engine/dasha/`) provides Vimshottari timelines to three levels with exact rational period arithmetic, school-explicit seeding, and the year-length convention as an explicit profile field rather than a hidden default. Certified against the external oracle by injecting the oracle's own Moon into this engine's timeline, isolating timeline mathematics from oracle astronomy: 1,782 comparisons, zero lord mismatches.

The transit layer (`engine/transits/`) finds longitude-crossing events by station-aware bisection on the certified position pipeline, so event instants inherit the Tier-0 certification. It covers sign and nakshatra ingresses, returns, and natal conjunctions, handles retrograde multiplicity with direction flags, and provides a profile-guarded natal-relative view.

The Parashari school layer (`engine/parashari/`) provides full graha drishti facts (`PARASHARI_DRISHTI_V1`, `ADR-0012`), the first module of the school-separated aspect architecture, and **Panch Mahapurusha yoga facts (`PARASHARI_YOGA_V1`, `ADR-0081`, `engine/parashari/mahapurusha_yoga.py`)** - the five named yogas only (Ruchaka, Bhadra, Hamsa, Malavya, Sasa), with their own certification artifact. `ADR-0086` records a certification-integrity qualification on that artifact's composition layer; any citation of `PARASHARI_YOGA_V1`'s certification must be read subject to it.

**KP significators are certified (`KP_SIGNIFICATOR_V1`, `ADR-0078`, with the certification-integrity repair recorded in `ADR-0079`).** This supersedes the earlier repository-wide non-claim on significators; four-step, ruling planets and horary remain unclaimed and unimplemented.

FOUNDATION capabilities are certified: rise and set with declared conventions (`RISE_SET_V1`, `ADR-0054`); panchanga classification - tithi, vara, nakshatra as a panchanga element, yoga, karana (`PANCHANGA_V1`, `ADR-0055`); and Rahu Kalam, Yamaganda and Gulika under the named seed variant `PYJHORA_TRIKALAM_V1` (`TRIKALAM_V1`, `ADR-0060`). FOUNDATION was formally exited 2026-08-22 (`ADR-0068`).

Sign conventions are explicit and enforced (`engine/astrology/sign.py` and `sign_conventions.py`). See the open-items section for what this did and deliberately did not change.

The legacy kernel (`legacy/`) remains untouched and continues to describe only itself. Its historical Tier-0 certification artifacts were verified byte-identical across every phase of development.

## 3. Explicit non-claims

*Corrected 2026-09-05 (`ADR-0093`). Two claims previously in this section had become false and are removed below rather than left standing: KP significators and yogas are now certified capabilities. The remainder of each sentence was true and is preserved.*

Nothing in the repository claims KP four-step, ruling planets, or horary. **KP significators are no longer a non-claim** - `KP_SIGNIFICATOR_V1` is certified (`ADR-0078`/`ADR-0079`); the frozen-and-independently-audited methodology that decision D-008 required was produced before implementation. No dasha system other than Vimshottari exists, and no depth beyond pratyantardasha. No fractional sputa drishti, no Jaimini rashi drishti, no Western aspects. **Yogas are no longer a blanket non-claim** - the five Panch Mahapurusha yogas are certified (`PARASHARI_YOGA_V1`, `ADR-0081`); no other yoga is claimed, computed, or implemented. **Strengths and interpretation of any kind remain non-claims**, and `engine/astrology/planet_strength.py` raises `NotImplementedError` by design rather than returning a placeholder that could masquerade as a computed value. No Bhrigu Nandi Nadi, no numerology, no evidence or convergence layer, no API surface beyond a demo endpoint, and no production application. Divisions outside the eleven served in production - D1, D9, D10 and the eight registered vargas - raise rather than compute; that includes D16 and D4, which are certified but deliberately not registered.

## 4. Open items carried forward

Placidus house behavior above the polar circles remains NOT VERIFIED; it is exercised only to 64.1 degrees north, and a specification decision on expected behavior is required before a test can assert anything.

UTC is treated as UT1, bounded by 0.9 second and recorded in provenance. Delta-T-aware handling would remove the caveat.

The sign-index convention split is RESOLVED as of SIGN_CONVENTION_V1 (ADR-0012), which closed the documented convergence-layer prerequisite. Both conventions remain exactly as certified, varga outputs 0-based and rashi-level outputs 1-based, because renumbering would reopen locked behavior. What changed is that the split is now explicit and machine-enforced: an inert `Sign` value type carries the convention, every sign-carrying model exposes the opposite view additively, and `SIGN_FIELD_CONVENTIONS` is a declared registry whose completeness is a test gate. Adding a sign-typed field without declaring its convention fails the default gate, so the debt cannot grow again. Each declaration is proven by a discriminating witness rather than sampled.

Sidereal speeds are Swiss `FLG_SIDEREAL` outputs, adequate for retrograde flags but due review before high-precision speed work. Rahu and Ketu tradition variants for dignity, and the node-aspect variant for drishti, are recorded but not selected by any profile. The `scripts/` legacy certification pipeline still targets the historical packaging and is superseded by the current gates.

## 5. Working method that produced this state

Each phase followed the same discipline and it is worth preserving. An ADR-style plan is written and approved before any code exists, naming the classical source, the decisions requiring owner sign-off, and the certification gates. Implementation is additive; certified files are not modified. Every rule table is written as frozen literals and verified cell by cell against a second independent transcription plus a re-derivation from the classical statement. Every phase adds an independent validator whose reference implementation is built by a different construction from the production code and imports nothing from it. External oracles are used for what they can authoritatively provide and never as astronomical ground truth; where an oracle's own astronomy differs, the divergence is measured, recorded, and worked around rather than absorbed into a widened tolerance. Certified behavior is proven unchanged across every phase by SHA-256 sweeps over dense and ULP-adversarial output sets. Tests that encoded superseded expectations are replaced with the reason documented inline, never quietly deleted. Nothing is called certified without a regenerable artifact.
## 6. Machine-readable capability block

`scripts/check_capability_state.py` parses **only** the delimited block below, and compares it against
live authoritative sources: `engine.astrology.CERTIFIED_PRODUCTION_VARGAS` for registry membership,
the runner-regenerated `certification/*.json` result fields for certification evidence, and
`scripts/certification_support.py`'s `CERTIFIER_SOURCES`/`VALIDATOR_SOURCES` for the source registries.
It never parses the prose above, and it never reads a document's own committed history as evidence.

`certification/ENGINE_CAPABILITY_INVENTORY.json` is **excluded** from those live sources, together with
the other dated evidence files, because `ADR-0092` classifies it as frozen dated historical evidence and
not a current source of truth. That exclusion is asserted by a committed test, not merely intended.

Edit this block whenever certified capability changes; the prose above must be kept consistent with it
by hand, which the gate cannot check.

<!-- CAPABILITY-BLOCK:BEGIN - machine-readable, parsed by scripts/check_capability_state.py. Do not edit the delimiters. -->
```json
{
  "production_registered_vargas": [2, 3, 7, 12, 20, 24, 30, 40, 45],
  "dedicated_production_vargas": [1, 9, 10],
  "certified_not_registered_vargas": [4, 16],
  "not_certified_vargas": [27, 60],
  "certified_capabilities": [
    "current_engine",
    "KP_CHAIN_V1",
    "KP_SIGNIFICATOR_V1",
    "PANCHANGA_V1",
    "PARASHARI_DRISHTI_V1",
    "PARASHARI_YOGA_V1",
    "RISE_SET_V1",
    "SIGN_CONVENTION_V1",
    "TRANSIT_V1",
    "TRIKALAM_V1",
    "VIMSHOTTARI_V1"
  ],
  "non_claims": [
    "planet_strength",
    "interpretation",
    "kp_four_step",
    "kp_ruling_planets",
    "horary",
    "sputa_drishti",
    "jaimini_rashi_drishti",
    "western_aspects",
    "bhrigu_nandi_nadi",
    "numerology"
  ],
  "counts": {
    "certifier_sources": 23,
    "validator_sources": 22
  }
}
```
<!-- CAPABILITY-BLOCK:END -->

## Change history

| Version | Date | Change |
|---|---|---|
| 2.4.0 | 2026-09-07 | **D20 Vimsamsa production implementation (`ADR-0095`).** `engine/astrology/varga_d20.py` created and registered; `CERTIFIED_PRODUCTION_VARGAS` grows 8 -> 9 divisions. The certifier was revised to certify the REGISTERED rule (gate D isolation -> non-invasiveness) and re-run: nine gates PASS, content hash `efd08cea...dac0` unchanged. Capability block: D20 moved from `certified_not_registered_vargas` to `production_registered_vargas`. Prose updated to match. D16 and D4 remain certified-but-unregistered. |
| 2.3.0 | 2026-09-07 | D20 Vimsamsa certified as a STANDALONE, unregistered rule under `ADR-0095` (`certification/VARGA_D20_V1_certification.json`, nine gates PASS). Capability block: D20 moved from `not_certified_vargas` to `certified_not_registered_vargas`; counts 22/21 -> 23/22 for the newly registered certifier and validator sources. Prose updated to match. D20 remains absent from `CERTIFIED_PRODUCTION_VARGAS`; production implementation and CI wiring remain unauthorized. |
| 2.2.1 | 2026-09-05 | Reproduced test count 937 -> 952, raised by the 15 controls committed with the B-1/B-2 gate remediation (second addendum to `ADR-0094`). No capability claim changed; the block itself is unchanged. |
| 2.2.0 | 2026-09-05 | Capability block gains `current_engine`, the Tier-0 astronomical-kernel certification (`ADR-0005`). The independent CEO audit of the gate found it silently excluded from the completeness universe (defect D-1) because it records its verdict at `summary.result` rather than at top level; the gate now reads both paths and the block accounts for it. Reproduced test count 919 -> 937, raised by the 18 new controls committed with the D-1/D-2/D-3 remediation. No other claim changed. |
| 2.1.0 | 2026-09-05 | Section 6 added: the delimited machine-readable capability block that `scripts/check_capability_state.py` parses, per `ADR-0094`. Additive; no claim in sections 1-5 changed except the reproduced test count, 898 -> 919, which the gate's own 21 committed negative controls raised. The block is the only machine-checked part of this document; the prose is not, and the status header now says so rather than implying whole-document enforcement. |
| 2.0.0 | 2026-09-05 | **Capability-state reconciliation against live repository evidence (`ADR-0093`).** MAJOR because two claims in section 3 were affirmatively false, not merely stale: the blanket "no yogas" non-claim (superseded by `PARASHARI_YOGA_V1`, `ADR-0081`) and the "Nothing in the repository claims KP significators" non-claim (superseded by `KP_SIGNIFICATOR_V1`, `ADR-0078`/`ADR-0079`); both are corrected in place with the still-true remainder of each sentence preserved. Registry list corrected from five vargas to the eight actually registered (D24, D40, D45 added). D16 and D4 recorded for the first time as certified but deliberately NOT production-registered. `RISE_SET_V1`, `PANCHANGA_V1`, `TRIKALAM_V1` and the FOUNDATION exit added. Counts corrected: 372 tests -> 898; eleven validators -> 21 registered validator sources; eleven certification runners -> 22 registered certifier sources. Date and authoritative commit updated. Planetary strength non-claim verified still true in code and preserved unchanged. |
| 1.0.0 | 2026-08-09 | Created as the single in-repository current-state document. |
