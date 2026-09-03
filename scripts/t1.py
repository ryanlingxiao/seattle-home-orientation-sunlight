# -*- coding: utf-8 -*-
# =============================================================================
# 表一与表三 · 雨季与夏季逐时云况
# 出自《西雅图买房该选什么朝向？后院八个方向的光照，用 21 年气象数据算了一遍》
# https://xceedwa.com/zh/seattle-home-orientation-sunlight
#
# 算什么   : 雨季（11 到 3 月）与夏季（6 到 8 月）各时段的云况占比。产出文中的 79% 到 86% 云盖满、CLR 2%、09:00 峰值 85.6%
# 数据源   : clean.pkl
# 依赖     : pandas, numpy
# 怎么跑   : python t1.py
# 输出     : t1_wet.csv · t3_summer.csv
# 原始文件名: t1.py
# 授权     : 本脚本以 MIT 授权公开；它读取的气象观测数据属于公有领域。
# =============================================================================

import pandas as pd, numpy as np
df = pd.read_pickle("clean.pkl")
pd.set_option("display.width",250)

WET=[11,12,1,2,3]; SUM=[6,7,8]
def table(sub, name):
    ct = pd.crosstab(sub["hour"], sub["lbl"], normalize="index").mul(100)
    for c in ["CLR","FEW","SCT","BKN","OVC","VV"]:
        if c not in ct: ct[c]=0.0
    ct = ct[["CLR","FEW","SCT","BKN","OVC","VV"]]
    ct["BKN+OVC"] = ct["BKN"]+ct["OVC"]
    ct["BKN+OVC+VV"] = ct["BKN+OVC"]+ct["VV"]
    ct["N"] = sub.groupby("hour").size()
    print("\n=== "+name+" ===")
    print(ct.round(2).to_string())
    return ct

w = table(df[df.month.isin(WET)], "WET SEASON Nov-Mar, 2005-2025")
w.to_csv("t1_wet.csv")
s = table(df[df.month.isin(SUM)], "SUMMER Jun-Aug, 2005-2025")
s.to_csv("t3_summer.csv")
