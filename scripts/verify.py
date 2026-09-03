# -*- coding: utf-8 -*-
# =============================================================================
# 校准一 · 对 WRCC 实测日照百分率与 TMY3 辐照
# 出自《西雅图买房该选什么朝向？后院八个方向的光照，用 21 年气象数据算了一遍》
# https://xceedwa.com/zh/seattle-home-orientation-sunlight
#
# 算什么   : 把云观测反推的日面可见比例逐月对 WRCC 实测日照百分率；并用 TMY3 (sea.epw) 独立核对辐照，检出 PVGIS-ERA5 高报直射
# 数据源   : clean.pkl 与 sea.epw
# 依赖     : pandas, numpy
# 怎么跑   : python verify.py（sea.epw 须自行从 EnergyPlus 或 NREL NSRDB 下载 KSEA / 站号 727930 的 TMY3，本包未随附）
# 输出     : 打印到 stdout
# 原始文件名: verify.py
# 授权     : 本脚本以 MIT 授权公开；它读取的气象观测数据属于公有领域。
# =============================================================================

import pandas as pd, numpy as np
df = pd.read_pickle("clean.pkl")
p_sun={0:1.0,1:0.95,2:0.70,3:0.28,4:0.02,5:0.0}
print("=== cloud-derived 'sun disk visible' vs WRCC measured % possible sunshine (KSEA) ===")
wrcc={1:28,2:40,3:50,4:52,5:56,6:56,7:65,8:65,9:62,10:43,11:28,12:23}
print(f"{'month':6s}{'cloud-derived':>15s}{'WRCC measured':>15s}{'diff':>8s}")
for mo in [11,12,1,2,3,6,7,8]:
    sub=df[(df.month==mo)]
    # daylight window per month, sun above ~5 deg
    hrs={11:(9,16),12:(9,16),1:(9,16),2:(8,17),3:(8,18),6:(6,20),7:(6,20),8:(7,19)}[mo]
    sub=sub[sub.hour.between(*hrs)]
    d=sub["cov"].value_counts(normalize=True).mul(100)
    est=sum(d.get(k,0)*v for k,v in p_sun.items())
    print(f"{mo:<6d}{est:>14.1f}%{wrcc[mo]:>14d}%{est-wrcc[mo]:>+8.1f}")

print("\n=== TMY (sea.epw) independent irradiance check, NOT ERA5 ===")
rows=[]
with open("sea.epw") as f:
    for i,l in enumerate(f):
        if i<8: continue
        p=l.split(",")
        rows.append((int(p[1]),int(p[3]),float(p[13]),float(p[14]),float(p[15])))
e=pd.DataFrame(rows,columns=["month","hour","ghi","dni","dhi"])
print("source line 1 of epw:", open("sea.epw").readline().strip()[:120])
for lbl,mos in [("Dec",[12]),("wet Nov-Mar",[11,12,1,2,3]),("Jun-Aug",[6,7,8])]:
    s=e[e.month.isin(mos)]
    day=s[s.ghi>0]
    mid=s[s.hour.between(11,13)]
    print(f"{lbl:12s} daylight hrs DNI>120: {(day.dni>120).mean()*100:5.1f}%   "
          f"11-13h DNI>120: {(mid.dni>120).mean()*100:5.1f}%   "
          f"diffuse share of GHI: {s.dhi.sum()/s.ghi.sum()*100:5.1f}%")
print("\n(prior round claimed: wet-season midday 63% of hours DNI>120; NSRDB Dec diffuse share 66%; ERA5 53%)")
