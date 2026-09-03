# -*- coding: utf-8 -*-
# =============================================================================
# 第 2 步 · 清洗与云量分级
# 出自《西雅图买房该选什么朝向？后院八个方向的光照，用 21 年气象数据算了一遍》
# https://xceedwa.com/zh/seattle-home-orientation-sunlight
#
# 算什么   : 把每条观测的 4 层云况折成一个总云量等级（CLR<FEW<SCT<BKN<OVC<VV），并把 METAR 的 HH:53 归到 HH+1 整点
# 数据源   : 上一步产出的 sea_asos.csv
# 依赖     : pandas, numpy
# 怎么跑   : python analyze.py（须先跑 fetch.py）
# 输出     : clean.pkl 中间产物，后续所有脚本都读它
# 原始文件名: analyze.py
# 授权     : 本脚本以 MIT 授权公开；它读取的气象观测数据属于公有领域。
# =============================================================================

import pandas as pd, numpy as np, re

df = pd.read_csv("sea_asos.csv", dtype=str, keep_default_na=False)
df["valid"] = pd.to_datetime(df["valid"], errors="coerce")
df = df.dropna(subset=["valid"])

# round to nearest hour (METAR at HH:53/56 is the HH+1 aviation observation)
df["hr"] = (df["valid"] + pd.Timedelta(minutes=4)).dt.round("h")
df["hour"] = df["hr"].dt.hour
df["month"] = df["hr"].dt.month
df["year"] = df["hr"].dt.year

RANK = {"CLR":0,"SKC":0,"NSC":0,"NCD":0,"FEW":1,"SCT":2,"BKN":3,"OVC":4,"VV":5}
def clean(s):
    s = (s or "").strip().upper()
    return s
cols = ["skyc1","skyc2","skyc3","skyc4"]
for c in cols:
    df[c] = df[c].map(clean)

def total_cover(row):
    best = -1
    for c in cols:
        v = row[c]
        if v in RANK:
            if RANK[v] > best: best = RANK[v]
    return best
df["cov"] = df[cols].apply(lambda r: max([RANK.get(v,-1) for v in r]), axis=1)
df = df[df["cov"] >= 0].copy()

LBL = {0:"CLR",1:"FEW",2:"SCT",3:"BKN",4:"OVC",5:"VV"}
df["lbl"] = df["cov"].map(LBL)

print("rows usable:", len(df))
print("year range:", df.year.min(), "-", df.year.max())
print("obs per year:\n", df.groupby("year").size().to_string())
print("\ncover distribution overall:\n", df["lbl"].value_counts(normalize=True).mul(100).round(2).to_string())

df.to_pickle("clean.pkl")
