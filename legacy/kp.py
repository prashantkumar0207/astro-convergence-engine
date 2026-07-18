"""Deterministic KP interval hierarchy. Internal ownership is exact rational [start,end)."""
from fractions import Fraction
from decimal import Decimal

LORDS  = ["Ke","Ve","Su","Mo","Ma","Ra","Ju","Sa","Me"]
YEARS  = [7,20,6,10,7,18,16,19,17]
SIGN_LORDS = ["Ma","Ve","Me","Mo","Su","Me","Ve","Ma","Ju","Sa","Sa","Ju"]
SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
NAKS = ["Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu","Pushya","Ashlesha","Magha","P.Phalguni","U.Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha","Mula","P.Ashadha","U.Ashadha","Shravana","Dhanishta","Shatabhisha","P.Bhadrapada","U.Bhadrapada","Revati"]
NAK_SPAN = Fraction(40, 3)

def _frac(x):
    if isinstance(x, Fraction): return x
    if isinstance(x, Decimal): return Fraction(x)
    if isinstance(x, int): return Fraction(x)
    # IMPORTANT: preserve the decimal spelling of an ephemeris float rather than
    # the exact binary IEEE-754 expansion Fraction(float).
    if isinstance(x, float): return Fraction(Decimal(str(x)))
    return Fraction(Decimal(str(x)))

def _walk(pos, start_idx, span):
    acc = Fraction(0)
    for k in range(9):
        i = (start_idx + k) % 9
        w = span * YEARS[i] / 120
        if pos < acc + w:
            return i, pos - acc, w
        acc += w
    raise ArithmeticError("interval walk fell through")

def chain(lon):
    L = _frac(lon) % 360
    sign = int(L // 30); nak = int(L // NAK_SPAN)
    pos = L - nak * NAK_SPAN; si = nak % 9
    sub_i, sub_pos, sub_w = _walk(pos, si, NAK_SPAN)
    ss_i, ss_pos, ss_w = _walk(sub_pos, sub_i, sub_w)
    near = min(pos, NAK_SPAN-pos, sub_pos, sub_w-sub_pos, ss_pos, ss_w-ss_pos)
    return {"sign": SIGNS[sign], "SL": SIGN_LORDS[sign], "nakshatra": NAKS[nak], "NL": LORDS[si], "SB": LORDS[sub_i], "SS": LORDS[ss_i], "nearest_boundary_arcsec": float(near*3600)}

def all_boundaries():
    bounds=set()
    for nak in range(27):
        base=nak*NAK_SPAN; bounds.add(base); si=nak%9; acc=Fraction(0)
        for k in range(9):
            i=(si+k)%9; w=NAK_SPAN*YEARS[i]/120; sub_start=base+acc; bounds.add(sub_start); acc2=Fraction(0)
            for k2 in range(9):
                j=(i+k2)%9; w2=w*YEARS[j]/120; bounds.add(sub_start+acc2); acc2+=w2
            acc+=w
    return sorted(bounds)
