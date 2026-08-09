# KP layer

Purpose: Exact-rational KP lordship chains (sign, star, sub, sub-sub lord) and KP fact charts.

Specification: `docs/KP_CHAIN_SPEC.md`. Decision entry: `docs/DECISION_LOG.md` ADR-0006 (PROPOSED pending
owner ratification, Q1). Certification artifact: see `certification/` and the human-readable
report in `reports/certification/`.

Design notes: Consumes AstronomySnapshot facts computed EXPLICITLY under the kp_krishnamurti profile and rejects any other; preserves the certified legacy [start, end) interval ownership and Decimal(str(x)) conversion rule, which deliberately differ from the engine-wide 1e-10 promote-up convention.

Explicit non-claims: significators, four-step, ruling planets, horary, dashas. Each would require its own specification, decision entry and
certification before being built.
