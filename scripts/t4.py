# -*- coding: utf-8 -*-
# =============================================================================
# 拐点 · 降水 · 能见度 · 条件概率
# 出自《西雅图买房该选什么朝向？后院八个方向的光照，用 21 年气象数据算了一遍》
# https://xceedwa.com/blog/seattle-home-orientation-sunlight
#
# 算什么   : 逐时变化率（14:00 的 OVC 单跌 3.51 个百分点）、雨季降水时段占比、能见度、以及「上午 10 点已全阴的日子到下午 14 点怎么走」的条件概率 66.6%
# 数据源   : clean.pkl
# 依赖     : pandas, numpy
# 怎么跑   : python t4.py
# 输出     : 打印到 stdout
# 原始文件名: t4.py
# 授权     : 本脚本以 MIT 授权公开；它读取的气象观测数据属于公有领域。
# =============================================================================

import pandas as pd, numpy as np
df = pd.read_pickle("clean.pkl")
pd.set_option("display.width",300)
df["nosun"]=df["cov"].isin([3,4,5]); df["ovc"]=df["cov"].isin([4,5])
df["sunny"]=df["cov"].isin([0,1])
WET=[11,12,1,2,3]; w=df[df.month.isin(WET)]

print("=== Q1: hour-over-hour change in wet-season BKN+OVC+VV and OVC ===")
a=w.groupby("hour")[["nosun","ovc","sunny"]].mean().mul(100)
a["d_nosun"]=a["nosun"].diff(); a["d_ovc"]=a["ovc"].diff()
print(a.round(2).to_string())
print("\nsharpest single-hour DROP in BKN+OVC+VV:", a["d_nosun"].idxmin(), round(a["d_nosun"].min(),2),"pp")
print("sharpest single-hour DROP in OVC:", a["d_ovc"].idxmin(), round(a["d_ovc"].min(),2),"pp")
print("peak hour BKN+OVC+VV:", a["nosun"].idxmax(), round(a["nosun"].max(),2))
print("peak hour OVC:", a["ovc"].idxmax(), round(a["ovc"].max(),2))

print("\n=== Q3: wet-season precipitation by local hour ===")
def isprecip(s):
    s=(s or "").strip().upper()
    if s in ("","M"): return False
    toks=s.split()
    for t in toks:
        if t.startswith("VC"): continue
        if any(k in t for k in ["RA","DZ","SN","PL","GR","GS","IC","UP","SG"]): return True
    return False
w=w.copy(); w["precip"]=w["wxcodes"].map(isprecip)
pr=w.groupby("hour")["precip"].mean().mul(100)
print(pr.round(2).to_string())
print("AM 09-13 precip%%: %.2f   PM 14-18: %.2f  diff %+.2f pp"%(
  w[w.hour.between(9,13)].precip.mean()*100, w[w.hour.between(14,18)].precip.mean()*100,
  (w[w.hour.between(9,13)].precip.mean()-w[w.hour.between(14,18)].precip.mean())*100))
print("\nwet-season vsby mean by hour (statute mi):")
w["v"]=pd.to_numeric(w["vsby"],errors="coerce")
print(w.groupby("hour")["v"].mean().round(2).to_string())

print("\n=== CONDITIONAL TEST: given OVC/VV at 10:00 in Nov-Mar, what happens later? ===")
w2=df[df.month.isin(WET)].copy()
w2["date"]=w2["hr"].dt.date
piv=w2.pivot_table(index="date",columns="hour",values="cov",aggfunc="max")
need=[h for h in range(7,19)]
piv=piv.dropna(subset=need)
base=piv[piv[10]>=4]
print("wet-season days with complete 07-18 obs:",len(piv),"   of which OVC/VV at 10:00:",len(base),
      f"({len(base)/len(piv)*100:.1f}%)")
rows=[]
for h in need:
    rows.append({"hour":h,
      "still OVC/VV %":(base[h]>=4).mean()*100,
      "broken to BKN %":(base[h]==3).mean()*100,
      "SCT or better %":(base[h]<=2).mean()*100,
      "CLR/FEW %":(base[h]<=1).mean()*100})
print(pd.DataFrame(rows).set_index("hour").round(1).to_string())
print("\nSame, but ALL wet-season days (unconditional) for reference:")
rows=[]
for h in need:
    rows.append({"hour":h,"OVC/VV %":(piv[h]>=4).mean()*100,"SCT or better %":(piv[h]<=2).mean()*100,
                 "CLR/FEW %":(piv[h]<=1).mean()*100})
print(pd.DataFrame(rows).set_index("hour").round(1).to_string())

print("\n=== how often does a wet-season day give ANY sun window? ===")
day_am=(piv[[9,10,11]].max(axis=1)<=2); day_pm=(piv[[14,15,16]].max(axis=1)<=2)
print(f"days with SCT-or-better through 09-11 : {day_am.mean()*100:.1f}%")
print(f"days with SCT-or-better through 14-16 : {day_pm.mean()*100:.1f}%")
amc=(piv[[9,10,11]].max(axis=1)<=1); pmc=(piv[[14,15,16]].max(axis=1)<=1)
print(f"days CLR/FEW all of 09-11 : {amc.mean()*100:.1f}%   all of 14-16 : {pmc.mean()*100:.1f}%")
