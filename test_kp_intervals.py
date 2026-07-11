import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fractions import Fraction
from astro_kernel import kp

def test_interval_completeness_exact():
    # widths of the 9 subs of every nakshatra sum EXACTLY to 13d20m; same recursively for sub-subs
    for nak in range(27):
        si = nak % 9
        total = Fraction(0)
        for k in range(9):
            i = (si + k) % 9
            w = kp.NAK_SPAN * kp.YEARS[i] / 120
            total += w
            inner = Fraction(0)
            for k2 in range(9):
                inner += w * kp.YEARS[(i + k2) % 9] / 120
            assert inner == w
        assert total == kp.NAK_SPAN

def test_boundary_ownership_start_inclusive_end_exclusive():
    eps = Fraction(1, 10**9)  # ~3.6e-6 arcsec
    bounds = kp.all_boundaries()
    for B in bounds:
        at = kp.chain(B)
        above = kp.chain(B + eps)
        assert (at["NL"], at["SB"], at["SS"]) == (above["NL"], above["SB"], above["SS"]), f"at-boundary must own next interval: {B}"
        if B > 0:
            below = kp.chain(B - eps)
            # below must differ from at in at least the deepest level
            assert (below["SS"] != at["SS"]) or (below["SB"] != at["SB"]) or (below["NL"] != at["NL"]), f"no change across boundary {B}"

def test_known_anchor_values():
    c = kp.chain(0.0)
    assert (c["SL"], c["NL"], c["SB"], c["SS"]) == ("Ma", "Ke", "Ke", "Ke")
    c = kp.chain(Fraction(40, 3))  # exactly Bharani start
    assert (c["NL"], c["SB"], c["SS"]) == ("Ve", "Ve", "Ve")
    # First sub of Ashwini is Ketu, width 7/120*13d20m = 46m40s; just below its end -> SS = last of Ketu cycle
    end_first_sub = kp.NAK_SPAN * 7 / 120
    c = kp.chain(end_first_sub)          # exactly at -> Venus sub begins
    assert c["SB"] == "Ve" and c["SS"] == "Ve"

def test_determinism():
    import random
    random.seed(42)
    pts = [random.uniform(0, 360) for _ in range(500)]
    a = [kp.chain(x) for x in pts]
    b = [kp.chain(x) for x in pts]
    assert a == b
