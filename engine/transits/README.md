# Transit layer

Purpose: Longitude-crossing events: sign and nakshatra ingresses, returns, natal conjunctions, and a natal-relative view.

Specification: `docs/TRANSIT_ENGINE_SPEC.md`. Decision entry: `docs/DECISION_LOG.md` ADR-0008 (PROPOSED pending
owner ratification, Q1). Certification artifact: see `certification/` and the human-readable
report in `reports/certification/`.

Design notes: Event instants are found by station-aware bisection on the certified position pipeline, so they inherit the Tier-0 certification; retrograde multiplicity is reported with direction flags and station contacts follow a documented tangent rule.

Explicit non-claims: aspect-system events, dasha-transit convergence, topocentric variants. Each would require its own specification, decision entry and
certification before being built.
