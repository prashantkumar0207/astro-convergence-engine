<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | CURRENT - regenerate on every certified change |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-09 |
| Review cadence | TBD (see docs/OPEN_QUESTIONS.md Q1) |

# Consolidated engine status

Date: 2026-08-09
Authoritative commit: origin/main 61733f342c0cc9eabb71139d3fb90a365ede2118
Purpose: the single current-state document for this project. Supersedes nothing; the per-phase ADR plans in `claude/` remain the decision record, and the repository's own certification artifacts remain the evidence. Every figure below was reproduced by execution on a fresh clone of origin/main, not copied from documentation.

## 1. How to verify everything in one sitting

Clone the repository, install the pinned dependencies (`pyswisseph==2.10.3.2`, `pytest==9.1.1`, `tzdata==2025.2`; PyJHora plus its dependencies only if you intend to run the oracle certifiers), then run the default gate, the eleven independent holdout validators, the legacy gate, and the eleven certification runners. The README lists every command. Current reproduced results: 372 tests pass, all eleven validators pass, the legacy gate passes 5 of 5, and all eleven certification runners regenerate their artifacts with PASS. The stored certification JSON files are never accepted as proof; each runner rebuilds its artifact from scratch on every invocation.

## 2. Certified layers

The astronomical kernel is locked and Tier-0 certified. It runs strict Swiss Ephemeris with return-flag inspection so a silent Moshier fallback raises instead of returning mislabelled data, computes a fully sidereal frame including ascendant and cusps, resolves civil time through IANA zones with DST, fold, and historical-offset handling, and stamps every snapshot with provenance recording profile, ayanamsa, frame, house system, node policy, ephemeris mode, and time basis. Certification evidence is the frozen eleven-case holdout matrix run against the bundled swetest 2.10.03 binary under both ratified profiles, 528 comparisons, maximum error 0.000180 arcsecond.

Two calculation profiles are ratified by recorded human sign-off and are the only path to an ayanamsa: `parashari_lahiri` (Lahiri) and `kp_krishnamurti` (Krishnamurti). They are mechanically proven to drive the computation, differing by the expected 5.811 arcminutes. Cross-system reuse of a snapshot computed under the other profile is forbidden, and the KP, dasha, and Parashari layers each enforce that in code by rejecting foreign-profile snapshots.

Divisional charts: D1 Rashi with the documented whole-sign house rule, plus certified D9 Navamsa and D10 Dashamsa served by their own hard-wired production modules, never through the generic registry. Five further vargas are certified through the Generic Varga registry under the `parashara` school key: D2 Hora, D3 Drekkana, D7 Saptamsa, D12 Dwadasamsa, and D30 Trimsamsa. Each carries its own ADR, dual-transcribed frozen rule table, dense sweep, ULP boundary battery, external oracle agreement, independent validator, and certification artifact. The sanctioned registry contents live in the single constant `engine.astrology.CERTIFIED_PRODUCTION_VARGAS`; every unregistered division still raises `UnsupportedVargaError` by design.

The KP layer (`engine/kp/`) provides exact-rational lordship chains (sign lord, star lord, sub lord, sub-sub lord) and KP fact charts under the KP profile, proven equivalent to the certified legacy kernel with zero categorical mismatches across a 51,429-point sweep, 19,679 boundary points, an eleven-case chart holdout, and the 200-field transcribed fixture set.

The dasha layer (`engine/dasha/`) provides Vimshottari timelines to three levels with exact rational period arithmetic, school-explicit seeding, and the year-length convention as an explicit profile field rather than a hidden default. Certified against the external oracle by injecting the oracle's own Moon into this engine's timeline, isolating timeline mathematics from oracle astronomy: 1,782 comparisons, zero lord mismatches.

The transit layer (`engine/transits/`) finds longitude-crossing events by station-aware bisection on the certified position pipeline, so event instants inherit the Tier-0 certification. It covers sign and nakshatra ingresses, returns, and natal conjunctions, handles retrograde multiplicity with direction flags, and provides a profile-guarded natal-relative view.

The Parashari school layer (`engine/parashari/`) provides full graha drishti facts, the first module of the school-separated aspect architecture.

Sign conventions are explicit and enforced (`engine/astrology/sign.py` and `sign_conventions.py`). See the open-items section for what this did and deliberately did not change.

The legacy kernel (`legacy/`) remains untouched and continues to describe only itself. Its historical Tier-0 certification artifacts were verified byte-identical across every phase of development.

## 3. Explicit non-claims

Nothing in the repository claims KP significators, four-step, ruling planets, or horary; per decision D-008 the significator methodology specification must be frozen and independently audited before implementation. No dasha system other than Vimshottari exists, and no depth beyond pratyantardasha. No fractional sputa drishti, no Jaimini rashi drishti, no Western aspects, no yogas, strengths, or interpretation of any kind. No Bhrigu Nandi Nadi, no numerology, no evidence or convergence layer, no API surface beyond a demo endpoint, and no production application. Vargas other than the eight certified ones raise rather than compute. Planetary strength raises `NotImplementedError` by design.

## 4. Open items carried forward

Placidus house behavior above the polar circles remains NOT VERIFIED; it is exercised only to 64.1 degrees north, and a specification decision on expected behavior is required before a test can assert anything.

UTC is treated as UT1, bounded by 0.9 second and recorded in provenance. Delta-T-aware handling would remove the caveat.

The sign-index convention split is RESOLVED as of SIGN_CONVENTION_V1 (ADR-CONVENTION-001), which closed the documented convergence-layer prerequisite. Both conventions remain exactly as certified, varga outputs 0-based and rashi-level outputs 1-based, because renumbering would reopen locked behavior. What changed is that the split is now explicit and machine-enforced: an inert `Sign` value type carries the convention, every sign-carrying model exposes the opposite view additively, and `SIGN_FIELD_CONVENTIONS` is a declared registry whose completeness is a test gate. Adding a sign-typed field without declaring its convention fails the default gate, so the debt cannot grow again. Each declaration is proven by a discriminating witness rather than sampled.

Sidereal speeds are Swiss `FLG_SIDEREAL` outputs, adequate for retrograde flags but due review before high-precision speed work. Rahu and Ketu tradition variants for dignity, and the node-aspect variant for drishti, are recorded but not selected by any profile. The `scripts/` legacy certification pipeline still targets the historical packaging and is superseded by the current gates.

## 5. Working method that produced this state

Each phase followed the same discipline and it is worth preserving. An ADR-style plan is written and approved before any code exists, naming the classical source, the decisions requiring owner sign-off, and the certification gates. Implementation is additive; certified files are not modified. Every rule table is written as frozen literals and verified cell by cell against a second independent transcription plus a re-derivation from the classical statement. Every phase adds an independent validator whose reference implementation is built by a different construction from the production code and imports nothing from it. External oracles are used for what they can authoritatively provide and never as astronomical ground truth; where an oracle's own astronomy differs, the divergence is measured, recorded, and worked around rather than absorbed into a widened tolerance. Certified behavior is proven unchanged across every phase by SHA-256 sweeps over dense and ULP-adversarial output sets. Tests that encoded superseded expectations are replaced with the reason documented inline, never quietly deleted. Nothing is called certified without a regenerable artifact.
## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-09 | Created as the single in-repository current-state document. |
