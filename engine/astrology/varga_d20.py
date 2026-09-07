"""
D20 Vimsamsa: ninth production varga through the generic registry
(VARGA_D20_V1, ADR-0095 selection and frozen methodology, DP-036
certification design, certification-execution and CI-oracle evidence).

Classical source (ADR-0095 section 1, Parashara/BPHS "Reading E",
translated-verse citation): "From Aries for a Movable Rasi, from
Sagittarius for a Fixed Rasi and from Leo for a Common Rasi: this is how
the calculations of Vimshamsas (1/20th of a Rasi, or 1 deg 30 min each)
are to commence." So movable source signs (0-based Aries=0, Cancer=3,
Libra=6, Capricorn=9) start at Aries (0); fixed source signs (Taurus=1,
Leo=4, Scorpio=7, Aquarius=10) start at Sagittarius (8); dual/common
source signs (Gemini=2, Virgo=5, Sagittarius=8, Pisces=11) start at Leo
(4). Counting proceeds forward for all twelve - the framework's
CyclicVargaRule exactly.

SOURCE UNCERTAINTY IS NOT ELIMINATED (ADR-0095 section 4). No verbatim
Sanskrit was located; the basis is a translated verse plus convergent
secondary attestation plus PyJHora's Traditional Parasara default. This
selection is NOT proof of the historical original text, and every
citation of D20's methodology must carry that qualification. The
certification artifact carries it as a structured `source_uncertainty`
field so it cannot be cited away.

VARIANT F IS EXCLUDED, NOT REFUTED (ADR-0095 section 3). The minority
reading - movable Aries, fixed Leo, dual Sagittarius, i.e. the fixed/dual
transposition, `start_sign=(0, 4, 8, ...)` - is attested and has NOT been
disproved. It is excluded as the selected methodology and is never
computed, never offered, and must not silently become an alternative
production interpretation. `scripts/certify_d20.py` plants it as a gate H
negative control precisely so that any drift toward it fails loudly.

DEITY PAYLOAD IS EXCLUDED (ADR-0095 section 5, following ADR-0089).
`VargaClassification` carries the D-sign, division index and fraction
only; the vimsamsa deities are out of scope, so DP-024's payload question
is neither required nor resolved here.

Genuine external-oracle agreement WAS obtained for this rule, unlike D40:
PyJHora 4.8.7 `vimsamsa_chart(chart_method=1)`, 5,400 comparisons, 0
mismatches, at zero categorical tolerance, in CI run 34115135184's
hash-pinned oracle job.

The frozen rule below is preserved exactly as certified
(certification/VARGA_D20_V1_certification.json, content hash
efd08cea451084fedbe444c5473d6d50dfc589055b585f172e8a6e537668dac0) - do
not alter the table for implementation convenience; any change requires
its own ADR and recertification.
"""

from engine.astrology.varga_registry import (
    register_varga_rule,
    registered_vargas,
)
from engine.astrology.varga_rules import CyclicVargaRule

#: Movable source signs (0-based Aries=0, Cancer=3, Libra=6,
#: Capricorn=9) start at Aries (0); fixed source signs (Taurus=1, Leo=4,
#: Scorpio=7, Aquarius=10) start at Sagittarius (8); dual source signs
#: (Gemini=2, Virgo=5, Sagittarius=8, Pisces=11) start at Leo (4).
#: Frozen literals, verified cell by cell in tests. Width is exactly
#: 30/20 = 1.5 degrees, and every internal boundary k*1.5 is an exact
#: binary fraction, so D20 carries no representability exposure.
D20_VIMSAMSA = CyclicVargaRule(
    divisions=20,
    start_sign=(0, 8, 4, 0, 8, 4, 0, 8, 4, 0, 8, 4),
    direction=(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
)

D20_SCHOOL = "parashara"


def ensure_registered() -> None:
    """Register D20 Parashara if not already present (idempotent)."""

    if (20, D20_SCHOOL) not in registered_vargas():
        register_varga_rule(20, D20_SCHOOL, D20_VIMSAMSA)


ensure_registered()
