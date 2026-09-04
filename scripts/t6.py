# -*- coding: utf-8 -*-
# =============================================================================
# 12 月阴天日数交叉验证
# 出自《西雅图买房该选什么朝向？后院八个方向的光照，用 21 年气象数据算了一遍》
# https://xceedwa.com/blog/seattle-home-orientation-sunlight
#
# 算什么   : 用 NOAA 的「阴天 / 晴天」日定义，从 ASOS 侧独立重建 12 月的晴阴天数，与 NOAA CCD 发表值对照
# 数据源   : clean.pkl
# 依赖     : pandas, numpy
# 怎么跑   : python t6.py
# 输出     : 打印到 stdout
# 原始文件名: t6.py
# 修正     : 原版末两处写成 dec.cov / g.cov，属性取值会命中 DataFrame.cov() 这个方法而不是名为 cov 的列，
#            在任何 pandas 版本上都会抛 TypeError。已改为 dec["cov"] / g["cov"]，与 t7.py 的写法一致。
#            只改取列方式，计算逻辑与输出口径一字未动。（2026-09-03）
# 授权     : 本脚本以 MIT 授权公开；它读取的气象观测数据属于公有领域。
# =============================================================================

import pandas as pd, numpy as np
df = pd.read_pickle("clean.pkl")
df["date"]=df["hr"].dt.date
# ceilometer height check
h=pd.to_numeric(df["skyl1"],errors="coerce")
print("skyl1 max ft:",h.max(),"  99.9pct:",round(h.quantile(0.999)),"  n>12000:",(h>12000).sum())

dec=df[(df.month==12)&(df.hour.between(9,16))]
piv=dec.pivot_table(index="date",columns="hour",values="cov",aggfunc="max").dropna()
print("\nDecember, 2005-2025, complete 09-16 daylight days:",len(piv))
cloudy=((piv>=3).sum(axis=1)>=6)
ovcday=((piv>=4).sum(axis=1)>=6)
clearday=((piv<=1).sum(axis=1)>=6)
print(f"days BKN+ for >=6 of 8 daylight hours (=NOAA 'cloudy'): {cloudy.mean()*100:.1f}%  -> {cloudy.mean()*31:.1f} of 31 days")
print(f"days OVC for >=6 of 8 daylight hours:                   {ovcday.mean()*100:.1f}%  -> {ovcday.mean()*31:.1f} of 31")
print(f"days CLR/FEW for >=6 of 8 daylight hours (=NOAA 'clear'):{clearday.mean()*100:.1f}%  -> {clearday.mean()*31:.1f} of 31")
print("Dec daylight 09-16 BKN+OVC+VV share: %.1f%%"%((dec["cov"]>=3).mean()*100))

# wet season "sun usable" = SCT or better
w=df[df.month.isin([11,12,1,2,3])]
s=w.groupby("hour").apply(lambda g:(g["cov"]<=2).mean()*100, include_groups=False)
print("\nwet season 'SCT or better' (sun likely usable) by hour:")
print(s.round(2).to_string())
