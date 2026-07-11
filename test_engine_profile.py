import pytest
from astro_kernel.engine import compute

def test_moshier_mode_is_reported():
    c=compute('1985-12-21','14:40:00',25.6,85.1333,ephe='MOSEPH')
    assert c['profile']['actual_ephemeris_modes']==['MOSEPH']

def test_strict_swieph_never_silently_falls_back(tmp_path):
    with pytest.raises(RuntimeError):
        compute('1985-12-21','14:40:00',25.6,85.1333,ephe='SWIEPH',ephe_path=str(tmp_path),strict_ephe=True)
