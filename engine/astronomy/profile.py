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

#: ADR-0054: the only currently-ratified rise/set disc reference.
#: Named (rather than a bare bool) so a future variant has somewhere
#: to go without renaming this one.
RISE_SET_DISC_UPPER_LIMB = "upper_limb"

#: ADR-0054: the only currently-ratified rise/set refraction
#: convention - standard atmosphere, auto-derived from observer
#: elevation (Swiss Ephemeris default when atpress/attemp are 0).
RISE_SET_REFRACTION_STANDARD = "standard_atmosphere"


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
    rise_set_disc_reference
        ADR-0054: which point of the solar disc defines "risen"/"set".
        Only `RISE_SET_DISC_UPPER_LIMB` is implemented;
        `engine.astronomy.rise_set` raises on any other value rather
        than silently applying a convention nothing has ratified.
    rise_set_refraction
        ADR-0054: the atmospheric refraction convention. Only
        `RISE_SET_REFRACTION_STANDARD` is implemented, for the same
        reason.
    """

    name: str
    ayanamsa_mode: int
    house_system: bytes
    node_policy: str
    strict_ephemeris: bool = True
    rise_set_disc_reference: str = RISE_SET_DISC_UPPER_LIMB
    rise_set_refraction: str = RISE_SET_REFRACTION_STANDARD


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
