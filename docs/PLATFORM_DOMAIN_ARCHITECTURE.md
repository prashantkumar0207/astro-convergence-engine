<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | PROPOSED, C0 RESEARCH. Architecture clarification only. Authorises no implementation in any domain. Pending owner ratification (docs/OPEN_QUESTIONS.md Q1). |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-11 |
| Review cadence | TBD |

# Platform Domain Architecture

## 1. Product identity

Astro Convergence Engine is not a natal horoscope application. The long-term product is:

> A transparent, evidence-driven, multi-domain Jyotisha intelligence platform that evaluates
> analytical methods against historical evidence, measures consistency and confidence, and
> provides qualified future-oriented analysis through convergence of multiple systems.

Five domains are in scope: Jataka (natal), Varshaphal (annual), Muhurta (electional), Prashna
(horary), and Mundane. The permanent USP is unchanged and applies to all five:
PAST to TEST to LEARN to CONFIDENCE to FUTURE.

**This document authorises no implementation.** It records what the architecture must eventually
support so that current decisions do not foreclose it.

## 2. The core correction: the platform is not person-centred

Designing around "person plus birth chart" would embed an assumption that four of the five domains
violate. The core entity is an **astrological entity**: a person, a country, a company, an
institution, a relationship, an event, an election, a business launch, or a question.

```
ENTITY
  |
CHART / CONTEXT
  |
CALCULATION SYSTEMS
  |
EVIDENCE ENGINE
  |
INTERPRETATION
  |
CONVERGENCE
  |
OUTPUT
```

## 3. Entities are not uniform, and the differences are structural

This is the most important analytical point in this document. Generalising "person" to "entity" is
necessary but not sufficient, because the five domains have four genuinely different shapes and a
single entity type would paper over them.

**Shape A, entity with an origin moment.** Person, country, company, institution. A moment and a
place exist, a natal-style chart is cast from them, and the entity persists through time. Birth-time
uncertainty is meaningful. This is the shape the engine already serves.

**Shape B, entity with a derived moment.** Varshaphal. The chart is derived from a parent entity's
chart plus a year, by solar return. It has no independent origin; its accuracy is bounded by its
parent's. Uncertainty is inherited, not independent.

**Shape C, query moment.** Prashna. The chart is cast for the moment a question was asked, at the
place it was asked. There is no birth data and, critically, **no origin-time uncertainty by
construction**: the moment is known exactly because it is the moment of asking.

**Shape D, no entity at all.** General Muhurta. Time and place only, with no chart belonging to
anyone. The subject is a candidate moment being evaluated for a purpose.

### 3.1 Shape D inverts the pipeline

Every other domain takes a moment and produces analysis. General Muhurta takes a purpose and a
window and **searches for moments**. It is a search and ranking problem over the timing engine, not
an analysis problem over a chart.

That has three consequences the architecture must anticipate. The output is a ranked set with
reasons, not a verdict about one chart. The system evaluates many candidates and returns the best,
which is statistically the same shape as BTR candidate search and needs the same honesty discipline
described in section 8. And it is the only domain requiring an optimiser, so the timing engine's
current performance characteristics become a design constraint rather than an implementation detail.

## 4. Per-domain requirements and current state

Nothing in this section exists today. Verified by search: `engine/` contains zero occurrences of
tithi, vara, karana, panchanga, rahu kalam, yamaganda, gulika, muhurta, varshaphal, muntha,
varshesh, saham, tajika, prashna or mundane.

### 4.1 Jataka, natal

The only domain with certified capability. D1, eight vargas, Vimshottari to pratyantar, transits,
Parashari graha drishti. Its gaps are the subject of the existing roadmaps and the 2026-08-11 audit.

### 4.2 Varshaphal, annual

Needs: solar return calculation, Varsha Lagna, Muntha, Varshesh, Tajika aspects, Sahams, Mudda dasha.

One useful connection: solar return is a longitude return, and `engine/transits/events.py` already
implements `returns()`. It is IMPLEMENTED but appears in no certification artifact, so it would need
certifying before Varshaphal could rest on it, not building from scratch.

Two cautions. Tajika aspects are a **different aspect system** from Parashari graha drishti and must
live in its own school-isolated module; they are not a variant of the certified drishti and must
never be routed through it. Mudda dasha is a **new dasha system**, inheriting the entire depth
requirement in `docs/DASHA_CERTIFICATION_ROADMAP.md` rather than sharing Vimshottari's certification.

### 4.3 Muhurta, electional, two modes

**General Muhurta** works without personal birth details: Panchanga (tithi, vara, nakshatra, yoga,
karana), the inauspicious day divisions (Rahu Kalam, Yamaganda, Gulika), and general planetary
conditions.

**Personalised Muhurta** adds D1, relevant vargas, dashas, transits, Moon compatibility, Tara Bala,
Chandra Bala, and purpose-specific rules, combining general suitability with personal compatibility.

Both must explain the recommendation: the favourable factors, the factors avoided, and the
confidence.

**Panchanga is a calculation-layer capability, not a Muhurta feature.** Tithi, vara, nakshatra, yoga
and karana are deterministic functions of Sun and Moon longitudes. They belong in the certified
calculation layer, certified with the same discipline as a varga, and Muhurta consumes them. Placing
them inside a Muhurta module would duplicate them the moment any other domain needs them, and
Prashna needs them immediately.

**Rahu Kalam, Yamaganda and Gulika need sunrise and sunset, which the engine cannot currently
compute.** They are fractional divisions of the day and night. This is a genuine Tier-0 gap: rising
and setting calculation, with its own latitude edge cases at high latitudes where the concept
degrades or fails entirely. It should be treated as astronomical foundation work, certified like the
kernel, and not as an incidental part of a Muhurta feature.

### 4.4 Prashna, horary

Question, time and location. No birth data. The chart is the question's moment.

Architecturally this connects directly to H3 Question Engine: a Prashna question **is** an entity,
which means the question model and the entity model meet here and should be designed together rather
than reconciled later.

BTR does not apply, per section 3 Shape C.

### 4.5 Mundane

Countries, governments, companies, markets, major events. Charts not associated with a person.

Mundane historical validation is simultaneously the **strongest and the most dangerous** evidence
source in the platform, and the architecture should reflect both halves.

Stronger: events are public record, dated, independently verifiable, available in volume, and free of
the memory bias that makes personal event recall unreliable.

More dangerous, for three reasons. Entity chart data is genuinely disputed, most famously the
multiple candidate charts for India's independence, so the entity model must hold **competing charts
for one entity** with their sources, rather than silently picking one. The sample size that makes
mundane data attractive also creates severe multiple-comparison risk: with enough entities, enough
event classes and enough rules, agreement appears by chance, and a platform whose USP is evidential
honesty cannot afford to discover that after publishing results. And events at national scale are
often ambiguously dated and ambiguously classified, so the H1 uncertainty model carries more weight
here than anywhere else.

## 5. Where the domains meet the existing engine

Shared and already certified: the astronomical kernel, calculation profiles, the time pipeline,
provenance, D1 and the vargas, transits.

Shared and needed but absent: panchanga elements, sunrise and sunset, and a domain-aware entity
model.

Isolated per domain and must not be merged: Tajika aspects versus Parashari drishti, Mudda dasha
versus Vimshottari, Prashna rules versus natal rules, and mundane rules versus personal rules. The
school-isolation principle already governs Parashari, KP, Jaimini and the rest; **domain isolation is
a second, orthogonal axis of the same principle**, and the platform now needs both.

## 6. One audit finding is elevated by this vision

`reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` finding H-02 records that transit event instants are
classified into the wrong division by the engine's own certified classifier, because the residual
envelope is 278 times wider than the boundary-promotion window: measured, two of twelve Sun sankranti
instants and twelve of twenty-eight Moon nakshatra ingress instants land in the previous division.

For natal work this is a seam worth fixing. **For Muhurta it is close to blocking.** Muhurta is
precisely the question "which tithi and which nakshatra hold at this candidate moment", evaluated
over many candidate moments, and candidate moments near boundaries are exactly the ones a search will
surface as marginal. A Muhurta engine built on the current seam would give wrong panchanga answers at
the moments where the answer matters most.

The recommendation is unchanged: H-02 needs an owner decision on resolution. This document records
that the Muhurta domain raises its priority substantially.

## 7. Convergence gains a second axis

Convergence today is specified across systems. It must also work across **domains**, and the two are
not the same.

The existing warning in `docs/H8_CONVERGENCE_SPEC.md` applies with more force here: two systems
agreeing because both derive from the same Moon position is weaker evidence than two agreeing from
independent significators. Cross-domain agreement has the same trap in a sharper form, because
Varshaphal derives from the natal chart by construction. Natal and Varshaphal agreeing is **not**
two independent confirmations; they share an origin. A convergence layer that cannot express shared
provenance will systematically overstate confidence in exactly the combination the product most wants
to present.

Evidence must therefore carry its domain alongside its producing system, and convergence must be able
to state not merely that sources agree but whether they could have disagreed.

## 8. Search honesty, applying to Muhurta and BTR alike

Both General Muhurta and BTR evaluate many candidates and report the best. The number of candidates
evaluated, the search space, and the scoring function MUST be recorded and reported. "Best of ten
thousand" and "best of five" are statistically very different claims, and presenting either as
"strongly indicated" without the denominator would be the same class of overclaim the project has
been correcting throughout Phase G.

## 9. BTR applicability by shape

BTR applies to Shape A only, and only where the origin moment is genuinely uncertain.

It does **not** apply to Prashna, where the moment is known by construction. It applies to Varshaphal
only through the parent natal chart, never independently. For mundane entities it applies only where
the origin moment is disputed rather than documented: a company incorporation timestamped by a
registry is a documented fact, and running BTR against it would reintroduce through the back door the
exact failure mode the charter prohibits, namely explaining a failed prediction by deciding the time
was wrong.

The entity model must therefore record, per entity, whether its origin moment is documented,
reported, or uncertain, and BTR must refuse to run where it is documented.

## 10. Development priority, unchanged

1. Complete governance and certification.
2. Strengthen calculation confidence.
3. Build evidence architecture.
4. Build interpretation framework.
5. Build convergence.
6. Add domain modules.

No domain implementation begins until the architecture decisions in section 11 are locked.

## 11. Decisions this document raises and does not make

Whether the entity model is one type with a discriminator or four related types, per section 3.
Whether panchanga and rising and setting are Tier-0 astronomical foundation or a Tier-1 calculation
layer. How competing charts for one mundane entity are represented and selected. What the
multiple-comparison discipline is for mundane validation. Whether cross-domain convergence weights
shared-origin sources differently, and how. Whether H-02's resolution is reprioritised given section
6. And the domain ordering after the current priorities are met.

## 12. Decisions taken (ADR-0020, additive)

Section 11 listed the decisions this document raised. Most are now taken. Recorded here so the
document does not continue to present settled questions as open.

**Taken.** The entity model is a common `AstrologicalSubject` and domain abstraction with
specialised subject types, not one undifferentiated type (D1). Panchanga and rise/set are Tier-0
foundational capabilities requiring independent certification before any dependent production module
relies on them (D2). Competing mundane charts are analysed independently and their disagreement
surfaced, with no silent selection (D3). Convergence must classify evidence relationships as
independent, derived, shared-origin, correlated or conflicting, and explain the classification (D4).
H-02 must be independently reproduced before production Muhurta, and repaired and certified if
confirmed (D5). The domain order is FOUNDATION, JATAKA, EVIDENCE, INTERPRETATION, CONVERGENCE,
VARSHAPHAL, MUHURTA, PRASHNA, MUNDANE, with BTR remaining independent and never a prerequisite for
convergence (D6). Both Muhurta modes are reserved, and Muhurta must expose its search window,
candidate space and selection methodology (D7). Varshaphal is a distinct domain rather than a natal
interpretation layer (D8). Prashna requires no birth details (D9).

**Still open.** The multiple-comparison discipline for mundane validation, which section 4.5
identifies as the sharpest risk in the strongest evidence source. The entity-kind vocabulary beyond
the five named types. Whether relationships between entities are modelled as entities or links. And
whether Q8 is closed by D6, which supplies an order but no entry or exit criteria.

**Two residues recorded in ADR-0020 rather than here**, because they qualify decisions rather than
raise new ones: the Tier-0 lock scope is not retroactively widened by D2, and vara depends on
rise/set because the Jyotisha weekday runs sunrise to sunrise rather than midnight to midnight.

## 13. Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-11 | Created from the CEO multi-domain platform vision. Architecture clarification only. |
| 1.1.0 | 2026-08-11 | Additive section 12: records the ten ADR-0020 decisions against the questions section 11 raised, and what remains open. Sections 1 to 11 unmodified. |
