# System Architecture

1. Input and place/timezone resolution
2. Tier 0 astronomical numerical core
3. Exact KP interval hierarchy: SL -> NL -> SB -> SS
4. Versioned derived rule engines
   - KP_SIGNIFICATOR_V1
   - FOUR_STEP_V1
   - CIL_V1
5. Isolated methodology engines
6. Past-event verification layer
7. Frozen per-system results
8. Cross-system convergence layer
9. Explanation/report layer
10. API and app integration

## Dependency rule

Derived rule disagreement must never be fixed by contaminating Tier 0. Every derived engine has its own formal specification, fixtures, tests, version, and certification status.
