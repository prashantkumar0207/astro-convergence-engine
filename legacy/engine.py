"""Canonical astronomy/cusp kernel. No prediction logic."""
import os
import swisseph as swe
from datetime import datetime
from zoneinfo import ZoneInfo
from . import kp

BODIES=[("Sun",swe.SUN),("Moon",swe.MOON),("Mars",swe.MARS),("Mercury",swe.MERCURY),("Jupiter",swe.JUPITER),("Venus",swe.VENUS),("Saturn",swe.SATURN),("Rahu",None),("Ketu",None),("Uranus",swe.URANUS),("Neptune",swe.NEPTUNE),("Pluto",swe.PLUTO)]

def to_utc(date_str,time_str,tz="Asia/Kolkata"):
    d=datetime.fromisoformat(f"{date_str}T{time_str}").replace(tzinfo=ZoneInfo(tz))
    return d.astimezone(ZoneInfo("UTC"))

def julday(u): return swe.julday(u.year,u.month,u.day,u.hour+u.minute/60+u.second/3600, swe.GREG_CAL)

def configure_ephemeris(ephe_path=None):
    if ephe_path:
        if not os.path.isdir(ephe_path): raise FileNotFoundError(ephe_path)
        swe.set_ephe_path(ephe_path)
    else:
        swe.set_ephe_path(None)

def compute(date_str,time_str,lat,lon,ayan="KRISHNAMURTI",node="MEAN",tz="Asia/Kolkata",ephe="MOSEPH",ephe_path=None,strict_ephe=False):
    configure_ephemeris(ephe_path)
    u=to_utc(date_str,time_str,tz); jd=julday(u)
    swe.set_sid_mode(getattr(swe,f"SIDM_{ayan}"))
    ephflag=swe.FLG_SWIEPH if ephe=="SWIEPH" else swe.FLG_MOSEPH
    flags=ephflag|swe.FLG_SIDEREAL|swe.FLG_SPEED
    node_id=swe.TRUE_NODE if node=="TRUE" else swe.MEAN_NODE
    out={"schema":"astro_kernel_chart_v1.1","input":{"date":date_str,"time":time_str,"timezone":tz,"lat":lat,"lon":lon,"utc":u.isoformat(),"jd_ut":jd},"profile":{"ayanamsha":ayan,"ayanamsha_value_deg":swe.get_ayanamsa_ut(jd),"node_mode":node,"delta_t_sec":swe.deltat(jd)*86400.0,"requested_ephemeris":ephe,"houses":"Placidus"},"bodies":{},"cusps":{}}
    rahu=None; actual_modes=set()
    for name,pid in BODIES:
        if name=="Rahu":
            r,ret=swe.calc_ut(jd,node_id,flags); rahu=r[0]; L,spd=rahu,r[3]
        elif name=="Ketu": L,spd=(rahu+180.0)%360.0,-1.0; ret=flags
        else: r,ret=swe.calc_ut(jd,pid,flags); L,spd=r[0],r[3]
        actual_modes.add("SWIEPH" if ret&swe.FLG_SWIEPH else "MOSEPH" if ret&swe.FLG_MOSEPH else "OTHER")
        out["bodies"][name]={"lon_deg":L,"speed":spd,"retro":bool(spd<0),**kp.chain(L)}
    if strict_ephe and ephe=="SWIEPH" and actual_modes!={"SWIEPH"}: raise RuntimeError(f"Swiss ephemeris files unavailable/fallback detected: {sorted(actual_modes)}")
    out["profile"]["actual_ephemeris_modes"]=sorted(actual_modes)
    cusps,ascmc=swe.houses_ex(jd,lat,lon,b"P",swe.FLG_SIDEREAL)
    cl=list(cusps); cl=cl[1:] if len(cl)==13 else cl
    for i,c in enumerate(cl,start=1): out["cusps"][str(i)]={"lon_deg":c,**kp.chain(c)}
    out["bodies"]["Ascendant"]={"lon_deg":ascmc[0],**kp.chain(ascmc[0])}
    return out
