"""
Calculation Profiles

Remediates audit ambiguity A-1: the ayanamsa (and the rest of the
astronomical configuration) must be an explicit, recorded choice
per astrological system, never a hidden global default.

A CalculationProfile freezes every convention the astronomy layer
needs: ayanamsa mode, house system, node policy, and ephemeris
strictness. Downstream systems request the profile they require:

- Parashari work conventionally uses the Lahiri (Chitrapaksha)
  ayanamsa.
- KP (Krishnamurti Paddhati) requires the Krishnamurti ayanamsa;
  this matches the legacy certified kernel profile recorded in
  LOCK_MANIFEST.json.

Neither choice is "the" default truth; they are named, documented
alternatives. PARASHARI_LAHIRI is the engine default purely for
backward compatibility with the pre-remediation Lahiri behavior.
"""

from dataclasses import dataclass

import swisseph as swe


NODE_POLICY_MEAN = "mean"
NODE_POLICY_TRUE = "true"


@dataclass(frozen=True)
class CalculationProfile:
    """
    Frozen astronomical calculation conventions.

    Attributes
    ----------
    name
        Stable identifier recorded as provenance.
    ayanamsa_mode
        Swiss Ephemeris sidereal mode (swe.SIDM_*).
    house_system
        Swiss Ephemeris house system code (bytes, e.g. b"P").
    node_policy
        Which lunar node represents Rahu: "mean" or "true".
        Ketu is always derived as Rahu + 180 degrees.
    strict_ephemeris
        When True, silent ephemeris fallback raises instead of
        returning mislabelled data (see engine.astronomy.ephemeris).
    """

    name: str
    ayanamsa_mode: int
    house_system: bytes
    node_policy: str
    strict_ephemeris: bool = True


PARASHARI_LAHIRI = CalculationProfile(
    name="parashari_lahiri",
    ayanamsa_mode=swe.SIDM_LAHIRI,
    house_system=b"P",
    node_policy=NODE_POLICY_MEAN,
)

KP_KRISHNAMURTI = CalculationProfile(
    name="kp_krishnamurti",
    ayanamsa_mode=swe.SIDM_KRISHNAMURTI,
    house_system=b"P",
    node_policy=NODE_POLICY_MEAN,
)

DEFAULT_PROFILE = PARASHARI_LAHIRI
