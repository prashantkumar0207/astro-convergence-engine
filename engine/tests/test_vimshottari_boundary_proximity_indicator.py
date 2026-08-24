"""
Dasha-specific boundary-proximity indicator (Dasha roadmap step 6, DP-020
Option 1, ADR-0073).

VimshottariTimeline.seed_nakshatra_boundary_arcsec reports the birth
Moon's distance to the nearest nakshatra boundary, in arcseconds - an
exact re-expression of the already-certified seed_elapsed_fraction, no
new astronomical calculation. This file hermetically verifies (no
PyJHora required, matching H-05's own precedent for a quantity that is a
pure derivation of an already oracle-validated value): the field
discriminates near-boundary from far-from-boundary cases; it agrees with
an independent measurement for each of M-02's own six near-boundary
holdout cases; it is genuinely computed, not a hardcoded or vacuous
constant (a real negative control mutating the production formula's own
NAK_SPAN dependency); and the field's own narrow scope - explicitly NOT
equivalent to KP's nearest_boundary_arcsec or to M-02's own certifier-only
diagnostic - is preserved structurally, not just by convention.
"""

from fractions import Fraction

import engine.dasha.vimshottari as vimshottari_module
from engine.dasha import tables as dasha_tables
from engine.dasha.vimshottari import vimshottari_from_moon

NAK_SPAN = dasha_tables.NAK_SPAN
BIRTH_JD = 2451545.0  # J2000.0, matching this suite's existing convention

#: M-02's own six root-found, oracle-verified near-boundary cases
#: (ADR-0072) - reused here, not re-derived, as the independent evidence
#: base for this field's own correctness.
NEAR_BOUNDARY_MOONS = {
    "B1_lahiri_boundary_before": 119.95579900,
    "B2_lahiri_boundary_at": 120.00019227829686,
    "B3_lahiri_boundary_after": 120.04419694,
    "B4_kp_boundary_before": 239.95548332,
    "B5_kp_boundary_at": 240.0,
    "B6_kp_boundary_after": 240.04452081,
}


def _independent_distance_arcsec(moon: float) -> float:
    """Reference computation, deliberately NOT sharing code with the
    production field: measures distance-to-boundary directly from the
    raw longitude, the same shape as scripts/certify_vimshottari.py's
    own moon_distance_to_nearest_boundary_deg diagnostic (M-02), not via
    seed_elapsed_fraction."""

    within = moon % float(NAK_SPAN)
    distance_deg = min(within, float(NAK_SPAN) - within)
    return distance_deg * 3600.0


def test_near_boundary_cases_agree_with_an_independent_measurement():
    for case_id, moon in NEAR_BOUNDARY_MOONS.items():
        timeline = vimshottari_from_moon(moon, BIRTH_JD, depth=1)
        independent = _independent_distance_arcsec(moon)
        assert abs(timeline.seed_nakshatra_boundary_arcsec - independent) < 1e-6, case_id


def test_near_boundary_cases_are_all_within_a_few_hundred_arcsec():
    """Sanity bound matching M-02's own NEAR_BOUNDARY_THRESHOLD_DEG (0.1
    degrees = 360 arcsec)."""

    for case_id, moon in NEAR_BOUNDARY_MOONS.items():
        timeline = vimshottari_from_moon(moon, BIRTH_JD, depth=1)
        assert timeline.seed_nakshatra_boundary_arcsec < 360.0, case_id


def test_far_from_boundary_case_reports_a_large_value():
    """H-05's own frozen baseline case (ADR-0069, moon=5.0) is nowhere
    near a boundary - proves the field actually discriminates, not a
    constant or vacuous small value regardless of input."""

    timeline = vimshottari_from_moon(5.0, BIRTH_JD, depth=1)
    assert timeline.seed_nakshatra_boundary_arcsec == 18000.0


def test_at_instant_cases_are_the_tightest():
    """The two root-found "_at" instants (M-02) should report the
    smallest values of the six near-boundary cases - both sides of a
    crossing bracket the true boundary, the "_at" instant sits closest
    to it by construction."""

    at_values = [
        vimshottari_from_moon(NEAR_BOUNDARY_MOONS[cid], BIRTH_JD, depth=1).seed_nakshatra_boundary_arcsec
        for cid in ("B2_lahiri_boundary_at", "B5_kp_boundary_at")
    ]
    other_values = [
        vimshottari_from_moon(NEAR_BOUNDARY_MOONS[cid], BIRTH_JD, depth=1).seed_nakshatra_boundary_arcsec
        for cid in NEAR_BOUNDARY_MOONS
        if not cid.endswith("_at")
    ]
    assert max(at_values) < min(other_values)


def test_negative_control_pin_would_catch_a_broken_formula(monkeypatch):
    """Proves the field is genuinely computed, not hardcoded: mutating
    the real production dependency (NAK_SPAN, as bound in
    engine.dasha.vimshottari's own namespace) changes the reported
    value, confirming the pin would fail under an actual regression."""

    baseline = vimshottari_from_moon(5.0, BIRTH_JD, depth=1).seed_nakshatra_boundary_arcsec
    assert baseline == 18000.0

    monkeypatch.setattr(vimshottari_module, "NAK_SPAN", Fraction(1, 1))
    mutated = vimshottari_from_moon(5.0, BIRTH_JD, depth=1).seed_nakshatra_boundary_arcsec
    assert mutated != baseline

    monkeypatch.undo()
    restored = vimshottari_from_moon(5.0, BIRTH_JD, depth=1).seed_nakshatra_boundary_arcsec
    assert restored == baseline


def test_field_is_exactly_and_only_a_reexpression_of_seed_elapsed_fraction():
    """Confirms the "zero new astronomical calculation" claim directly:
    the field's own value is fully reproducible from seed_elapsed_
    fraction alone, using only the certified NAK_SPAN constant."""

    for moon in (*NEAR_BOUNDARY_MOONS.values(), 5.0):
        timeline = vimshottari_from_moon(moon, BIRTH_JD, depth=1)
        elapsed = timeline.seed_elapsed_fraction
        derived = float(min(elapsed, 1 - elapsed) * NAK_SPAN * 3600)
        assert timeline.seed_nakshatra_boundary_arcsec == derived


def test_scope_is_not_silently_widened_to_deeper_levels_or_other_signals():
    """Structural guard against scope creep (item 5/6 of DP-020 Option
    1's own ratification): VimshottariTimeline exposes exactly one new
    boundary-proximity-shaped field, not an amplified days-of-uncertainty
    figure (Option 2, not chosen) and not a KP-style multi-level field."""

    import dataclasses

    from engine.models.dasha import VimshottariTimeline

    field_names = {f.name for f in dataclasses.fields(VimshottariTimeline)}
    assert "seed_nakshatra_boundary_arcsec" in field_names
    assert not any("uncertainty" in name for name in field_names)  # Option 2, not chosen
    assert not any(
        name.startswith(("sign_", "sub_")) for name in field_names
    )  # no KP-style multi-level fields
