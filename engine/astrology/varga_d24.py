"""
D24 Siddhamsa (Chaturvimshamsha): seventh production varga through the
generic registry (VARGA_D24_V1, ADR-0082 selection/methodology,
ADR-0083 certification).

Classical source (ADR-0083 section 1, BPHS Sarga 6, Shlokas 2-23): for
an odd source sign (0-based Aries=0, Gemini=2, Leo=4, Libra=6,
Sagittarius=8, Aquarius=10), the first siddhamsa belongs to Leo; for an
even source sign (Taurus=1, Cancer=3, Virgo=5, Scorpio=7, Capricorn=9,
Pisces=11), to Cancer. Counting proceeds forward for all twelve source
signs - this is the framework's CyclicVargaRule exactly.

Independently cross-checked against an independently transcribed
reference (validate_d24_holdout.py) and, by read-only source
inspection only (ADR-0083 section 1/8), PyJHora's own published
chaturvimsamsa_chart() default/Traditional-Parasara method - genuine
oracle execution remains deferred to this project's own CI hash-pinned
environment (ADR-0083's own ratification: "Gate C/oracle corroboration
PENDING", not resolved by this production implementation).

The frozen rule below is preserved exactly as certified
(certification/VARGA_D24_V1_certification.json) - do not alter the
table for implementation convenience; any change requires its own ADR
and recertification.
"""

from engine.astrology.varga_registry import (
    register_varga_rule,
    registered_vargas,
)
from engine.astrology.varga_rules import CyclicVargaRule

#: Odd source signs (0-based Aries=0, Gemini=2, Leo=4, Libra=6,
#: Sagittarius=8, Aquarius=10) start at Leo (4); even source signs
#: (Taurus=1, Cancer=3, Virgo=5, Scorpio=7, Capricorn=9, Pisces=11)
#: start at Cancer (3). Frozen literals, verified cell by cell in
#: tests.
D24_SIDDHAMSA = CyclicVargaRule(
    divisions=24,
    start_sign=(4, 3, 4, 3, 4, 3, 4, 3, 4, 3, 4, 3),
    direction=(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
)

D24_SCHOOL = "parashara"


def ensure_registered() -> None:
    """Register D24 Parashara if not already present (idempotent)."""

    if (24, D24_SCHOOL) not in registered_vargas():
        register_varga_rule(24, D24_SCHOOL, D24_SIDDHAMSA)


ensure_registered()
