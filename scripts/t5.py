# -*- coding: utf-8 -*-
# =============================================================================
# 太阳高度角过滤
# 出自《西雅图买房该选什么朝向？后院八个方向的光照，用 21 年气象数据算了一遍》
# https://xceedwa.com/zh/seattle-home-orientation-sunlight
#
# 算什么   : 剔除太阳高度角 5 度以下的时段后重算上下午差距（4.27 降到 3.06 个百分点），并反推日面可见比例
# 数据源   : clean.pkl
# 依赖     : pandas, numpy
# 怎么跑   : python t5.py
# 输出     : 打印到 stdout
# 原始文件名: t5.py
# 授权     : 本脚本以 MIT 授权公开；它读取的气象观测数据属于公有领域。
# =============================================================================

import pandas as pd, numpy as np
df = pd.read_pickle("clean.pkl")
pd.set_option("display.width",300)
LAT,LON = 47.4444, -122.3139   # KSEA

# NOAA solar position algorithm
t = df["hr"]
# convert local (America/Los_Angeles) to UTC
tl = t.dt.tz_localize("America/Los_Angeles", ambiguous="NaT", nonexistent="NaT")
utc = tl.dt.tz_convert("UTC")
ok = utc.notna()
jd = utc.astype("int64")/86400e9 + 2440587.5
jc = (jd-2451545.0)/36525.0
gml = (280.46646 + jc*(36000.76983+jc*0.0003032)) % 360
gma = 357.52911 + jc*(35999.05029-0.0001537*jc)
ecc = 0.016708634 - jc*(0.000042037+0.0000001267*jc)
ctr = (np.sin(np.radians(gma))*(1.914602-jc*(0.004817+0.000014*jc))
       + np.sin(np.radians(2*gma))*(0.019993-0.000101*jc)
       + np.sin(np.radians(3*gma))*0.000289)
tl_ = gml+ctr
app = tl_ - 0.00569 - 0.00478*np.sin(np.radians(125.04-1934.136*jc))
oblq = 23+(26+((21.448-jc*(46.815+jc*(0.00059-jc*0.001813))))/60)/60
oblc = oblq + 0.00256*np.cos(np.radians(125.04-1934.136*jc))
decl = np.degrees(np.arcsin(np.sin(np.radians(oblc))*np.sin(np.radians(app))))
y = np.tan(np.radians(oblc/2))**2
eot = 4*np.degrees(y*np.sin(2*np.radians(gml)) - 2*ecc*np.sin(np.radians(gma))
      + 4*ecc*y*np.sin(np.radians(gma))*np.cos(2*np.radians(gml))
      - 0.5*y*y*np.sin(4*np.radians(gml)) - 1.25*ecc*ecc*np.sin(2*np.radians(gma)))
mins = utc.dt.hour*60 + utc.dt.minute
tst = (mins + eot + 4*LON) % 1440
ha = np.where(tst/4 < 0, tst/4+180, tst/4-180)
za = np.degrees(np.arccos(np.clip(np.sin(np.radians(LAT))*np.sin(np.radians(decl))
     + np.cos(np.radians(LAT))*np.cos(np.radians(decl))*np.cos(np.radians(ha)),-1,1)))
df["elev"] = 90-za
df.loc[~ok,"elev"]=np.nan

df["nosun"]=df["cov"].isin([3,4,5]); df["ovc"]=df["cov"].isin([4,5]); df["sunny"]=df["cov"].isin([0,1])
WET=[11,12,1,2,3]
w=df[df.month.isin(WET)&df.elev.notna()]
print("=== mean solar elevation, wet season, by local hour (deg) ===")
e=w.groupby("hour")["elev"].agg(["mean","max"])
e["% hours sun above 5deg"]=w.groupby("hour")["elev"].apply(lambda s:(s>5).mean()*100)
print(e.round(1).to_string())

print("\n=== wet season, SUN-UP HOURS ONLY (solar elev > 5 deg) ===")
wu=w[w.elev>5]
g=wu.groupby("hour")[["nosun","ovc","sunny"]].mean().mul(100)
g["N"]=wu.groupby("hour").size()
g["d_nosun"]=g["nosun"].diff(); g["d_ovc"]=g["ovc"].diff()
print(g.round(2).to_string())
am=wu[wu.hour.between(9,13)]; pm=wu[wu.hour.between(14,18)]
print(f"\nsun-up AM(09-13) BKN+OVC+VV={am.nosun.mean()*100:.2f}  PM(14-18)={pm.nosun.mean()*100:.2f}  diff={(am.nosun.mean()-pm.nosun.mean())*100:+.2f}pp")
print(f"sun-up AM OVC={am.ovc.mean()*100:.2f}  PM OVC={pm.ovc.mean()*100:.2f}  diff={(am.ovc.mean()-pm.ovc.mean())*100:+.2f}pp")
print(f"sun-up AM CLR/FEW={am.sunny.mean()*100:.2f}  PM CLR/FEW={pm.sunny.mean()*100:.2f}  diff={(am.sunny.mean()-pm.sunny.mean())*100:+.2f}pp")

print("\n=== ERA5 cross-check: est. share of wet-season 11-13h with usable direct beam ===")
mid=w[w.hour.between(11,13)]
d=mid["cov"].value_counts(normalize=True).mul(100)
print(d.rename({0:"CLR",1:"FEW",2:"SCT",3:"BKN",4:"OVC",5:"VV"}).round(2).to_string())
p_sun={0:1.0,1:0.95,2:0.70,3:0.28,4:0.02,5:0.0}
est=sum(d.get(k,0)*v for k,v in p_sun.items())
print(f"implied 'sun disk visible' share  ~= {est:.1f}%   (ERA5 prior round claimed 63%)")
