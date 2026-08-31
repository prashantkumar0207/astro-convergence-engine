"""
Panch Mahapurusha Yoga (PARASHARI_YOGA_V1, ADR-0081).

Production implementation authorized by the owner's "CEO AUTHORIZATION -
PARASHARI_YOGA_V1 PRODUCTION IMPLEMENTATION" instruction, recorded in
docs/DECISION_LOG.md as a sub-entry under ADR-0081. Certification (all ten
gates A-I) was executed and PASSED against a standalone, unregistered
implementation before this module existed (scripts/certify_parashari_yoga.py,
recorded in the "Certification execution of ADR-0081" sub-entry); this module
implements exactly ADR-0081's own frozen rule and does not extend it. Per
that authorization, production output must be freshly re-verified against
the certifier's independent evidence after this module exists - this
module's own presence is not itself treated as proof.

Classical source: Brihat Parashara Hora Shastra (BPHS), the same root text
already governing every other certified Parashari-school capability in this
project. Exactly five yogas, and only these five: Ruchaka (Mars), Bhadra
(Mercury), Hamsa (Jupiter), Malavya (Venus), Sasa (Saturn) - collectively
"Panch Mahapurusha Yoga." No other yoga is in scope.

Frozen rule (ADR-0081 section 2), for each graha g in the five above:

    yoga_present(g) := house_of(g) in {1, 4, 7, 10}   (whole-sign, from Lagna)
                       AND (is_own_sign(g, sign_of(g)) OR is_exalted(g, sign_of(g)))

Moolatrikona is deliberately excluded (BPHS's own verse names "own, or
exaltation Rasi" only) - independently confirmed inert for these five grahas
(ADR-0081 section 2): each graha's own moolatrikona sign is already a member
of its own own-sign set, so the computed result is identical whether
moolatrikona is separately considered or not.

Production dependencies (reused, not duplicated, per ADR-0081 section 3):
the Tier-0-Locked D1 kernel's own sidereal planet longitudes and Lagna
longitude (engine.calculations.calculations.calculate under the
PARASHARI_LAHIRI profile); engine.astrology.signs.zodiac_sign; engine.
astrology.house.whole_sign_house; engine.astrology.dignity.is_own_sign/
is_exalted. No new astronomical calculation and no new aspect logic of any
kind. engine.astrology.dignity/dignities.json is the PRODUCTION dignity
source here but must never be treated as this capability's own certification
oracle (ADR-0081 section 4) - that independence is the certifier's own
concern, not this module's.

Isolated per the school-separation rule: this module never imports
engine.parashari.drishti, engine.kp, or any Jaimini/Nadi module, and defines
its own profile-guard error rather than reusing drishti's, keeping every
Parashari-school capability independently implemented and independently
evaluated (docs/PROJECT_ROADMAP.md section 3, qualification 3).

Explicit non-claims, carried forward unedited from ADR-0081 section 10:
no bhanga/cancellation logic of any kind; no combustion gating, no qualifier
field at all; retrograde is a disclosed per-graha qualifier only, never a
pass/fail gate (section 6); no strength or graded-presence output - present-
or-absent only; no other yoga; no varga (D9/D10/other divisional chart)
participation - D1 only; no Shadbala/planet_strength.py dependency of any
kind; no interpretive or predictive claim - this module computes only
whether the ratified BPHS formation condition holds, never that a yoga
predicts or correlates with any real-world outcome; the BPHS citation is a
translated-edition citation, not verified against the original Sanskrit or a
second, independent published edition (ADR-0081 section 1).
"""

import hashlib
from dataclasses import dataclass

import swisseph as swe

from engine.astrology.dignity import is_exalted, is_own_sign
from engine.astrology.house import whole_sign_house
from engine.astrology.signs import zodiac_sign
from engine.astronomy.profile import PARASHARI_LAHIRI
from engine.calculations.calculations import calculate
from engine.models.birth_data import BirthData
from engine.models.provenance import Provenance

#: The five Panch Mahapurusha yogas (ADR-0081 section 1). No other graha,
#: no other yoga.
YOGA_GRAHAS = ("Mars", "Mercury", "Jupiter", "Venus", "Saturn")
YOGA_NAMES = {
    "Mars": "Ruchaka",
    "Mercury": "Bhadra",
    "Jupiter": "Hamsa",
    "Venus": "Malavya",
    "Saturn": "Sasa",
}

#: Kendra houses from Lagna, whole-sign (ADR-0081 sections 2/3).
KENDRA_HOUSES = frozenset({1, 4, 7, 10})


class ParashariYogaProfileError(ValueError):
    """Raised when Mahapurusha yoga judgment is requested from a
    non-Parashari snapshot. Independently defined - never imported from
    engine.parashari.drishti's own ParashariProfileError - per this
    module's own school-isolation discipline."""


@dataclass(frozen=True, slots=True)
class MahapurushaYogaResult:
    """
    One graha's own Panch Mahapurusha judgment.

    Attributes
    ----------
    graha
        The graha name (one of YOGA_GRAHAS).
    yoga
        The named yoga this graha's own formation condition would produce
        (e.g. "Ruchaka" for Mars) - a label only; presence is `present`.
    sign_number
        The graha's own 1-based occupied sign.
    house_number
        The graha's own 1-based whole-sign house from the Lagna.
    present
        True iff the graha occupies a kendra house (1, 4, 7, or 10) AND its
        own sign is either its own-sign or its exaltation sign (ADR-0081
        section 2). Moolatrikona is not separately considered (inert for
        these five grahas, confirmed in ADR-0081 section 2).
    retrograde_qualifier
        True if this graha is retrograde at the chart's epoch (speed_
        longitude < 0). A disclosed qualifier only - never affects
        `present` (ADR-0081 section 6).
    """

    graha: str
    yoga: str
    sign_number: int
    house_number: int
    present: bool
    retrograde_qualifier: bool


@dataclass(frozen=True, slots=True)
class MahapurushaYogaChart:
    """
    Complete Panch Mahapurusha Yoga facts for one natal (D1) chart.

    A chart may show zero, one, or more than one yoga simultaneously -
    each graha's own predicate is independent, not mutually exclusive
    (ADR-0081 section 5).
    """

    ascendant_sign: int
    results: tuple
    provenance: Provenance

    @property
    def present_yogas(self) -> tuple:
        """Only the results whose own `present` is True."""

        return tuple(result for result in self.results if result.present)


def _yoga_predicate_from_sign_and_house(graha: str, graha_sign: int, house: int) -> bool:
    """The pure boolean combining logic (kendra AND (own-sign OR exalted)),
    isolated from any longitude/sign-of derivation (ADR-0081 section 2)."""

    return house in KENDRA_HOUSES and (
        is_own_sign(graha, graha_sign) or is_exalted(graha, graha_sign)
    )


def yoga_present(graha: str, graha_longitude: float, ascendant_longitude: float) -> bool:
    """The full rule, from real longitudes, via the production plumbing
    (zodiac_sign, whole_sign_house) ADR-0081 section 3 names."""

    graha_sign = zodiac_sign(graha_longitude)
    house = whole_sign_house(graha_longitude, ascendant_longitude)
    return _yoga_predicate_from_sign_and_house(graha, graha_sign, house)


def graha_mahapurusha_from_snapshot(snapshot) -> MahapurushaYogaChart:
    """Compute Panch Mahapurusha Yoga facts from a certified Parashari
    snapshot. Mirrors engine.parashari.drishti.graha_drishti_from_snapshot's
    own profile-validation discipline, independently implemented."""

    provenance = snapshot.provenance
    if provenance is None:
        raise ParashariYogaProfileError("snapshot carries no provenance")
    if provenance.profile_name != PARASHARI_LAHIRI.name:
        raise ParashariYogaProfileError(
            "Panch Mahapurusha Yoga requires the parashari_lahiri profile, got "
            f"'{provenance.profile_name}'"
        )
    if provenance.ayanamsa_mode != swe.SIDM_LAHIRI:
        raise ParashariYogaProfileError("snapshot ayanamsa does not match Parashari")

    ascendant_longitude = snapshot.houses.ascendant
    ascendant_sign = zodiac_sign(ascendant_longitude)

    results = []
    for graha in YOGA_GRAHAS:
        body = snapshot.sidereal_planets[graha]
        graha_sign = zodiac_sign(body.longitude)
        house = whole_sign_house(body.longitude, ascendant_longitude)
        present = _yoga_predicate_from_sign_and_house(graha, graha_sign, house)
        results.append(MahapurushaYogaResult(
            graha=graha,
            yoga=YOGA_NAMES[graha],
            sign_number=graha_sign,
            house_number=house,
            present=present,
            retrograde_qualifier=body.speed_longitude < 0,
        ))

    return MahapurushaYogaChart(
        ascendant_sign=ascendant_sign,
        results=tuple(results),
        provenance=provenance,
    )


def mahapurusha_yoga(birth_data: BirthData) -> MahapurushaYogaChart:
    """Full validated pipeline from BirthData under PARASHARI_LAHIRI."""

    result = calculate(birth_data, profile=PARASHARI_LAHIRI)
    return graha_mahapurusha_from_snapshot(result.snapshot)


def rule_content_sha256() -> str:
    """Content fingerprint of this module's own frozen rule constants, for
    certification pinning (mirrors engine.kp.significators.rule_content_
    sha256's own pattern). Deliberately does NOT fingerprint any dignity
    table - this module carries none of its own; it consumes production
    engine.astrology.dignity directly (ADR-0081 section 3), and the
    certifier's own separately-transcribed table is certification-only
    (ADR-0081 section 4)."""

    payload = repr((
        sorted(YOGA_GRAHAS),
        sorted(YOGA_NAMES.items()),
        sorted(KENDRA_HOUSES),
    )).encode()
    return hashlib.sha256(payload).hexdigest()
