"""
KP lordship chain classification (KP_CHAIN_V1, ADR-0006).

Computes the KP hierarchy (SL, NL, SB, SS) for a sidereal longitude
using exact rational arithmetic (see engine/kp/intervals.py for the
numeric contract). Behavior is certified equivalent to the legacy
kernel's kp.chain with zero categorical tolerance.
"""

from engine.astrology.nakshatra_names import NAKSHATRA_NAMES
from engine.astrology.sign_names import SIGN_NAMES
from engine.kp.intervals import to_exact, walk
from engine.kp.tables import KP_LORDS, KP_SIGN_LORDS, NAK_SPAN
from engine.models.kp_chain import KpChain


def kp_chain(longitude) -> KpChain:
    """
    Classify a sidereal longitude into its KP lordship chain.

    Accepts float (ephemeris output; converted via the certified
    decimal-spelling rule), int, Decimal, or Fraction.
    """

    exact = to_exact(longitude) % 360

    sign_index = int(exact // 30)
    nakshatra_index = int(exact // NAK_SPAN)

    position = exact - nakshatra_index * NAK_SPAN
    star_index = nakshatra_index % 9

    sub_index, sub_position, sub_width = walk(position, star_index, NAK_SPAN)
    ss_index, ss_position, ss_width = walk(sub_position, sub_index, sub_width)

    nearest = min(
        position,
        NAK_SPAN - position,
        sub_position,
        sub_width - sub_position,
        ss_position,
        ss_width - ss_position,
    )

    return KpChain(
        sign_number=sign_index + 1,
        sign_name=SIGN_NAMES[sign_index + 1],
        sign_lord=KP_SIGN_LORDS[sign_index],
        nakshatra_number=nakshatra_index + 1,
        nakshatra_name=NAKSHATRA_NAMES[nakshatra_index],
        nakshatra_lord=KP_LORDS[star_index],
        sub_lord=KP_LORDS[sub_index],
        sub_sub_lord=KP_LORDS[ss_index],
        nearest_boundary_arcsec=float(nearest * 3600),
    )
