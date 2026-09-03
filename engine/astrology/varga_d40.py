"""
D40 Khavedamsa: eighth production varga through the generic registry
(VARGA_D40_V1, ADR-0087 selection, frozen methodology, and
certification-execution authorization).

Classical source (ADR-0087 section 3, Parashara/BPHS - paraphrase-only
citation, disclosed gap, no located verbatim Sanskrit verse): for an
odd source sign (0-based Aries=0, Gemini=2, Leo=4, Libra=6,
Sagittarius=8, Aquarius=10), the first khavedamsa belongs to Aries; for
an even source sign (Taurus=1, Cancer=3, Virgo=5, Scorpio=7,
Capricorn=9, Pisces=11), to Libra. Counting proceeds forward for all
twelve source signs - this is the framework's CyclicVargaRule exactly.

Independently cross-checked against an independently transcribed
reference (validate_d40_holdout.py) and, by read-only source
inspection only (ADR-0087 section 3), PyJHora's own published
khavedamsa_chart() default/Traditional-Parasara method - genuine
oracle execution remains deferred (certification/VARGA_D40_V1_certification.json
Gate C: oracle_executed=false); this production implementation does
not wire D40 into the CI oracle-tier loop, matching ADR-0087's own
explicit non-authorization of that step.

The frozen rule below is preserved exactly as certified
(certification/VARGA_D40_V1_certification.json) - do not alter the
table for implementation convenience; any change requires its own ADR
and recertification.
"""

from engine.astrology.varga_registry import (
    register_varga_rule,
    registered_vargas,
)
from engine.astrology.varga_rules import CyclicVargaRule

#: Odd source signs (0-based Aries=0, Gemini=2, Leo=4, Libra=6,
#: Sagittarius=8, Aquarius=10) start at Aries (0); even source signs
#: (Taurus=1, Cancer=3, Virgo=5, Scorpio=7, Capricorn=9, Pisces=11)
#: start at Libra (6). Frozen literals, verified cell by cell in
#: tests.
D40_KHAVEDAMSA = CyclicVargaRule(
    divisions=40,
    start_sign=(0, 6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 6),
    direction=(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
)

D40_SCHOOL = "parashara"


def ensure_registered() -> None:
    """Register D40 Parashara if not already present (idempotent)."""

    if (40, D40_SCHOOL) not in registered_vargas():
        register_varga_rule(40, D40_SCHOOL, D40_KHAVEDAMSA)


ensure_registered()
