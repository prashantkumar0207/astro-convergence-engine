<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | PROPOSED, C0 RESEARCH. Design proposal only. The convergence algorithm MUST NOT be implemented on the strength of this document. Pending owner approval. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-11 |
| Review cadence | TBD |

# Evidence Independence: representing and computing independent evidence paths

## 1. What this document answers

ADR-0021 D5 establishes that agreement count is not equivalent to independent evidence-path count, and
that convergence must eventually answer "how many genuinely independent evidence paths support this
conclusion". This is the design proposal for representing and computing that.

It is a proposal. No convergence implementation is authorised by it.

## 2. The finding that shapes everything else: independence is relative, not absolute

Every fact in a single-entity analysis descends from one origin moment, one place, and one ephemeris.
The Moon longitude, the ascendant, every varga, every dasha boundary and every transit all trace to
the same root. **At the root, nothing is independent of anything.**

Therefore an unqualified claim that two pieces of evidence are "independent" is meaningless in this
system, and any count that does not say what it is independent *of* is not a number the product can
defend.

**Independence MUST be defined relative to a declared cut in the provenance graph, and the cut MUST be
reported alongside the count.** This is the single most important element of the design, and it is not
a technicality: without it the metric silently means different things in different reports, which is
exactly the failure mode that a decomposable confidence model exists to prevent.

Candidate cut levels, from permissive to strict:

**Ephemeris cut.** Independent above the shared ephemeris and instant. Nearly everything counts as
independent. Almost useless, and worth naming so it is never chosen by default.

**Chart cut.** Independent above the chart, so natal-derived and Varshaphal-derived claims collapse to
one path. Catches the derived relationship that ADR-0020 D4 names.

**Factor cut.** Independent above the individual astronomical factors: this Moon longitude, this
ascendant, this Sun longitude. Two systems both keyed on the Moon collapse to one path. This is the
cut that answers the question a user actually has.

**Rule cut.** Independent above the rule. Almost nothing counts as independent, since agreeing claims
usually share rules.

**Recommendation: the factor cut as the default, always reported, with the others available.**
Confidence: medium-high. It is the level at which "these agree for genuinely different reasons" is a
true statement.

## 3. The provenance graph

A directed acyclic graph. Evidence-creation time is when it is cheap to record; afterwards it is
unrecoverable.

**Node kinds.**

*Input* nodes: the entity's origin moment, place, timezone resolution. Also the question moment for
Prashna, and the candidate moment for Muhurta.

*Astronomical* nodes: a position or event under a named calculation profile. The profile is part of the
node identity, because the same body under two ayanamshas is two different facts and must never be
silently unified.

*Derived-chart* nodes: D1, each varga, a Varshaphal solar-return chart, a KP chain. A Varshaphal chart
node has an incoming edge from its parent natal chart, which is what makes the derived relationship
structural rather than a matter of interpretation.

*Timing* nodes: dasha periods, transit events, panchanga states once they exist.

*Rule* nodes: a registered rule at a version, from `docs/H5_INTERPRETATION_RULE_REGISTRY_SPEC.md`.

*Evidence* nodes: an evidence item from `docs/H4_EVIDENCE_MODEL_SPEC.md`, the leaves that support or
oppose a conclusion.

**Edge kinds.** `DERIVES_FROM` for computation. `APPLIES_TO` for a rule consuming a fact.
`CORRELATED_WITH`, an undirected annotation carrying a measured coefficient and its sample size, added
only from ledger measurement and never asserted at design time.

**What makes this tractable:** the graph is not inferred. Every layer already knows what it consumed.
The work is recording it, not reconstructing it.

## 4. Definition of a path, and of the independent count

**A path** is a directed chain from a node in the declared cut set to an evidence node, through the
`DERIVES_FROM` and `APPLIES_TO` edges that produced it.

**The independent path count** for a set of agreeing evidence nodes is the **maximum number of
vertex-disjoint paths** from the cut set to that evidence set, disjointness taken above the cut.

Vertex-disjointness is the right formalism rather than a convenient one. Two paths sharing any node
above the cut share a point of failure: if that node is wrong, both claims are wrong together, which
is precisely what "not independent" means operationally. The maximum vertex-disjoint path count is
computable by standard max-flow with unit vertex capacities, and by Menger's theorem it equals the
minimum vertex cut, which gives the explanation for free: **the minimum cut is the set of shared facts
that would invalidate the whole cluster of agreement**, and that set is exactly what a user should be
shown.

**Shared-origin nodes** are then not a separate concept requiring separate machinery: they are the
articulation points of the graph, and the ones that matter are the members of the minimum cut.

## 5. Reporting: a bound pair and a cut, never a single number

The design MUST NOT emit one number.

- **Upper bound:** the count of agreeing evidence items. Always available, always an over-estimate.
- **Lower bound:** the vertex-disjoint path count above the declared cut, after applying every known
  dependency and every measured correlation.
- **The cut** at which the lower bound was computed.
- **The minimum cut set**, meaning the shared facts whose failure would take the whole cluster with it.
- **Unknown-relationship count**, the number of pairs whose relationship has never been measured.

Reporting the pair rather than a point value is honest about the epistemic situation: the true
effective count sits between them and cannot currently be resolved further. Collapsing to a single
number would require asserting independence somewhere it has not been established, which D5 prohibits.

## 6. Structural, empirical, or hybrid: hybrid, with a strict directional rule

**Hybrid.** Structure sets the count; measurement may only lower it.

This follows directly from ADR-0021 D5, "absence of measured correlation is not evidence of
independence", and is the design's second most important element:

> **Empirical evidence is admissible only in the direction that REDUCES the independent count.
> Measurement can reveal hidden dependence. Measurement can never establish independence.**

So a measured `CORRELATED_WITH` edge above a declared threshold merges paths and lowers the count. A
measured absence of correlation changes nothing, however large the sample. This is asymmetric on
purpose, and the asymmetry is what stops the metric from being gamed by accumulating null results.

**Correlated relationships** are therefore the only empirical element, they arrive from the historical
ledger, they carry a sample size, and they are absent rather than zero when unmeasured, per
`docs/H4_EVIDENCE_MODEL_SPEC.md` section 10.

## 7. Unknown and unmeasured relationships

Two evidence nodes with no structural relationship and no correlation measurement are **unknown, not
independent.**

Three ways to handle unknown, and the choice is an owner decision:

**Conservative.** Treat unknown as dependent: merge the paths. Lowest count, safest, and can understate
badly when items are genuinely unrelated.

**Reported.** Count them as separate paths in the lower bound but report the unknown-pair count
alongside, so the reader can see how much of the claimed independence rests on the absence of
measurement.

**Tiered.** Structural independence at the declared cut is enough to count as a path; the unknown-pair
count is reported; and a claim is flagged when its independence rests mostly on unmeasured pairs.

**Recommendation: tiered.** Confidence: medium. Conservative is the safest default and would make the
metric useless early, when nothing is measured. Tiered preserves the honesty that matters, which is
visibility of what is unmeasured, without collapsing the metric to one in every early case.

## 8. Conflicting evidence is not part of the count

Conflicts do not subtract from the independent path count, and they MUST NOT be netted against it.
Agreement and disagreement are different outputs, and a single net figure would hide both.

Conflicting evidence gets its own independent-path computation. "Two independent paths support, three
independent paths oppose" is a meaningful statement. "Minus one" is not.

There is a case worth naming: two conflicting claims that share a minimum cut are conflicting *for a
reason inside the system*, most likely a convention or rule disagreement rather than genuine
astrological disagreement. That is diagnostic information about the engine, and the design should
surface it rather than average it away.

## 9. Explanation to the user

The count is worthless if it cannot be explained, and the graph is not the explanation.

The minimum cut set is the explanation. Naming the shared facts that would invalidate a cluster is
both the mathematically correct answer and the humanly useful one.

Shape of the output, not final wording:

> Five findings support this. Above the level of individual astronomical factors they form **two
> independent lines of reasoning**.
>
> Three of the five descend from your Moon's position in Ashwini. If that position is wrong, for
> example if your birth time is off by more than about twelve minutes, all three change together.
> They count as one line.
>
> Two descend from the ascendant and the tenth house, independently of the Moon. They count as a
> second line.
>
> Two of the ten possible pairings have never been measured for correlation, so this may be an
> over-count.
>
> One further finding disagrees, on an independent line of its own.

That last sentence is the point of the whole design. A system that says "five of six agree" when the
honest answer is "two lines agree and one disagrees" is producing its most confident output where its
evidence is thinnest, which is the failure this project exists to avoid.

## 10. Prerequisites in the existing engine

The design is unbuildable today, and the reasons are already recorded in
`reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md`.

Transit events carry a profile-name string and no provenance object, finding M-05, so an astronomical
node cannot be identified with its profile. Drishti provenance mislabels its own house convention,
M-04, so an edge would record the wrong parent. The transit view discards the natal provenance it
validates, so a natal-relative fact cannot be attributed to its natal chart. Dasha timelines record
only a float Julian Day and no civil birth data, so a timeline cannot be attributed to the birth
record that produced it. And D1 and the varga layers disagree about the source sign inside the
boundary window, M-09, so two nodes that should share a parent may not.

Provenance completeness is therefore a hard prerequisite for this design, not an accompaniment to it.

## 11. What must be decided before implementation

The default cut level and whether it is configurable. How unknown relationships are treated, per
section 7. The correlation threshold at which a measured edge merges paths, and the minimum sample
below which a measurement is disregarded. Whether the graph is persisted per analysis or rebuilt on
demand, which is the same reproducibility trade-off `docs/H4_EVIDENCE_MODEL_SPEC.md` section 5 raises
for evidence. Whether the bound pair is exposed to users or only the lower bound with the upper
available on request.

## 12. Verification strategy for the eventual implementation

Hand-constructed graphs with known answers, including the pathological cases: a single chain, a fan
from one factor, two genuinely disjoint chains, and a diamond. A test asserting that a Varshaphal claim
and its parent natal claim yield one path at the chart cut and not two. A test asserting that a
measured null correlation does **not** raise the count. A test asserting that unknown pairs are counted
and reported rather than silently treated as independent. A test asserting conflicts are never netted
against agreement. And a test asserting the minimum cut set returned is genuinely minimal, since an
explanation naming too many shared facts is as misleading as one naming too few.

## 13. Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-11 | Drafted on CEO direction as a design proposal. No implementation authorised. |
