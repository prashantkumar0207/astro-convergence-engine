"""Independent published Astrodienst swetest 2.10.03 fixture.
Source command/output: -b28.12.1946 -ut09:33 -p01 -eswe -sid0.
Official displayed longitudes: Sun 12 sa 3'47.2564; Moon 5 aq 24'0.6672.
Acceptance here is <=0.5 arcsec against the official Swiss-Ephemeris output.
"""
import swisseph as swe

def angular_arcsec(a,b): return abs(((a-b+180)%360)-180)*3600

def test_against_official_astrodienst_swetest_fixture():
    jd=swe.julday(1946,12,28,9+33/60,swe.GREG_CAL)
    swe.set_sid_mode(swe.SIDM_FAGAN_BRADLEY)
    flags=swe.FLG_MOSEPH|swe.FLG_SIDEREAL|swe.FLG_SPEED
    expected={swe.SUN:252+3/60+47.2564/3600, swe.MOON:305+24/60+0.6672/3600}
    errors=[]
    for pid,ref in expected.items():
        got=swe.calc_ut(jd,pid,flags)[0][0]
        errors.append(angular_arcsec(got,ref))
    assert max(errors)<=0.5, errors
