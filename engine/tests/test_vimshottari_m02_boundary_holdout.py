"""
M-02 near-boundary Moon holdout coverage (DP-019 Option 1, ADR-0072).

The Vimshottari oracle gate's two cases named H10_boundary_moon_a/
H11_boundary_moon_b were, in fact, 6.46 and 5.02 degrees from the nearest
nakshatra boundary - farther than most of the gate's own ordinary cases,
per the G1 architecture audit's M-02 finding. This file hermetically
verifies (no PyJHora required) the genuine near-boundary replacement cases
added to scripts/certify_vimshottari.py's BOUNDARY_HOLDOUT: that each one
really is close to a boundary, that "before"/"after" pairs genuinely
straddle a nakshatra-lord change (not merely a nearby chart), and - as a
negative control - that the ORIGINAL mislabeled birth data does NOT pass
the same check, proving it is not vacuously true.

Case data is duplicated from scripts/certify_vimshottari.py's HOLDOUT/
BOUNDARY_HOLDOUT (the canonical source, oracle-verified there); this file
does not import scripts/ (matching this suite's existing convention for
engine/tests/test_vimshottari_h08_boundary_convention.py and
test_vimshottari_hermetic_baseline.py, neither of which imports scripts/
either).
"""

from engine.astronomy.profile import KP_KRISHNAMURTI, PARASHARI_LAHIRI
from engine.calculations.calculations import calculate
from engine.dasha import tables as dasha_tables
from engine.dasha.vimshottari import vimshottari_from_moon
from engine.models.birth_data import BirthData

NAK_SPAN = dasha_tables.NAK_SPAN

#: Mirrors scripts/certify_vimshottari.py's NEAR_BOUNDARY_THRESHOLD_DEG -
#: two orders of magnitude tighter than the 5-6 degree distance M-02 found
#: for the cases this replaces.
NEAR_BOUNDARY_THRESHOLD_DEG = 0.1

#: The six genuine near-boundary cases (mirrors BOUNDARY_HOLDOUT), each
#: root-found via engine.transits.crossing.find_crossings() under its own
#: profile and sampled 5 minutes before/at/after the exact crossing.
BOUNDARY_CASES = [
    ("B1_lahiri_boundary_before", (2025, 1, 16), (5, 41, 41.52955502271652), 28.6667, 77.2167, PARASHARI_LAHIRI),
    ("B2_lahiri_boundary_at",     (2025, 1, 16), (5, 46, 41.52953714132309), 28.6667, 77.2167, PARASHARI_LAHIRI),
    ("B3_lahiri_boundary_after",  (2025, 1, 16), (5, 51, 41.52951925992966), 28.6667, 77.2167, PARASHARI_LAHIRI),
    ("B4_kp_boundary_before",     (2025, 1, 26), (2, 40, 21.100781857967377), 28.6667, 77.2167, KP_KRISHNAMURTI),
    ("B5_kp_boundary_at",         (2025, 1, 26), (2, 45, 21.100763976573944), 28.6667, 77.2167, KP_KRISHNAMURTI),
    ("B6_kp_boundary_after",      (2025, 1, 26), (2, 50, 21.10074609518051),  28.6667, 77.2167, KP_KRISHNAMURTI),
]

#: The corrected, accurately-named ordinary cases (mirrors HOLDOUT's
#: H10_delhi_2025a/H11_delhi_2025b) - same birth data as the original
#: mislabeled cases, only the ID changed.
CORRECTED_ORDINARY_CASES = [
    ("H10_delhi_2025a", (2025, 3, 1), (16, 21, 0), 28.6667, 77.2167),
    ("H11_delhi_2025b", (2025, 3, 2), (11, 38, 0), 28.6667, 77.2167),
]


def _moon_and_distance(date, time, lat, lon, profile):
    y, m, d = date
    h, mi, s = time
    snapshot = calculate(
        BirthData(y, m, d, h, mi, float(s), lat, lon, "UTC"), profile=profile
    ).snapshot
    moon = snapshot.sidereal_planets["Moon"].longitude
    within = moon % NAK_SPAN
    distance_deg = min(within, NAK_SPAN - within)
    return moon, distance_deg, snapshot.julian_day


def test_every_boundary_case_is_within_the_near_boundary_threshold():
    """Item 8 (DP-019 Option 1): genuine validation that each selected
    case really is close to a nakshatra boundary - not merely labelled
    as one, the exact defect M-02 found."""

    for case_id, date, time, lat, lon, profile in BOUNDARY_CASES:
        _, distance_deg, _ = _moon_and_distance(date, time, lat, lon, profile)
        assert distance_deg < NEAR_BOUNDARY_THRESHOLD_DEG, (case_id, distance_deg)


def test_at_instant_cases_are_far_tighter_than_the_general_threshold():
    """The two root-found "_at" instants should sit far inside the general
    threshold - confirming find_crossings()'s own root-finding precision,
    not just that the whole triple happens to squeak under 0.1 degrees."""

    for case_id, date, time, lat, lon, profile in BOUNDARY_CASES:
        if not case_id.endswith("_at"):
            continue
        _, distance_deg, _ = _moon_and_distance(date, time, lat, lon, profile)
        assert distance_deg < 0.001, (case_id, distance_deg)


def test_before_after_cross_a_genuine_nakshatra_lord_change():
    """Proves the crossing is real, not coincidental proximity: the
    "before" and "after" instants of each triple must land in different,
    adjacent nakshatras with a different Vimshottari lord."""

    triples = {
        "lahiri": ("B1_lahiri_boundary_before", "B3_lahiri_boundary_after"),
        "kp": ("B4_kp_boundary_before", "B6_kp_boundary_after"),
    }
    by_id = {case[0]: case for case in BOUNDARY_CASES}

    for _label, (before_id, after_id) in triples.items():
        before_moon, _, before_jd = _moon_and_distance(
            by_id[before_id][1], by_id[before_id][2], by_id[before_id][3],
            by_id[before_id][4], by_id[before_id][5],
        )
        after_moon, _, after_jd = _moon_and_distance(
            by_id[after_id][1], by_id[after_id][2], by_id[after_id][3],
            by_id[after_id][4], by_id[after_id][5],
        )
        before_timeline = vimshottari_from_moon(before_moon, before_jd, depth=1)
        after_timeline = vimshottari_from_moon(after_moon, after_jd, depth=1)

        assert before_timeline.seed_nakshatra_number != after_timeline.seed_nakshatra_number
        assert after_timeline.seed_nakshatra_number == before_timeline.seed_nakshatra_number + 1
        assert before_timeline.seed_lord != after_timeline.seed_lord


def test_original_mislabeled_cases_fail_the_same_near_boundary_check():
    """Negative control (item 9): the check above is not vacuously true -
    the ORIGINAL H10_boundary_moon_a/H11_boundary_moon_b birth data (same
    instants as the now-renamed H10_delhi_2025a/H11_delhi_2025b, before
    correction) measurably fails the tight near-boundary threshold,
    exactly reproducing the M-02 finding this file's own positive cases
    were built to fix."""

    original_mislabeled = [
        ("H10_boundary_moon_a (original)", (2025, 3, 1), (16, 21, 0), 28.6667, 77.2167),
        ("H11_boundary_moon_b (original)", (2025, 3, 2), (11, 38, 0), 28.6667, 77.2167),
    ]
    for case_id, date, time, lat, lon in original_mislabeled:
        _, distance_deg, _ = _moon_and_distance(date, time, lat, lon, PARASHARI_LAHIRI)
        assert distance_deg > NEAR_BOUNDARY_THRESHOLD_DEG, (case_id, distance_deg)


def test_renamed_ordinary_cases_reproduce_the_original_unchanged_values():
    """The rename (H10_boundary_moon_a -> H10_delhi_2025a, H11_boundary_
    moon_b -> H11_delhi_2025b) must not change any computed value - same
    birth data, same Moon, same distance, only the label corrected."""

    expected = {
        "H10_delhi_2025a": (339.79198804189934, 6.458654708565996),
        "H11_delhi_2025b": (351.6864032846307, 5.019736617964046),
    }
    for case_id, date, time, lat, lon in CORRECTED_ORDINARY_CASES:
        moon, distance_deg, _ = _moon_and_distance(date, time, lat, lon, PARASHARI_LAHIRI)
        expected_moon, expected_distance = expected[case_id]
        assert moon == expected_moon, case_id
        assert abs(distance_deg - expected_distance) < 1e-9, case_id


def test_boundary_and_ordinary_case_ids_are_disjoint_and_distinguishable():
    """Item 3 (DP-019 Option 1): the distinction between genuine
    boundary-proximity cases and ordinary holdout cases is preserved
    structurally, not just by convention - a "B" prefix never collides
    with an "H" prefix."""

    boundary_ids = {case[0] for case in BOUNDARY_CASES}
    ordinary_ids = {case[0] for case in CORRECTED_ORDINARY_CASES}
    assert boundary_ids.isdisjoint(ordinary_ids)
    assert all(cid.startswith("B") for cid in boundary_ids)
    assert all(cid.startswith("H") for cid in ordinary_ids)
