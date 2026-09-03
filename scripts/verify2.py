# -*- coding: utf-8 -*-
# =============================================================================
# 校准二 · 按 WRCC 原始定义逐月对表
# 出自《西雅图买房该选什么朝向？后院八个方向的光照，用 21 年气象数据算了一遍》
# https://xceedwa.com/zh/seattle-home-orientation-sunlight
#
# 算什么   : 按 WRCC/NCDC 的「白天平均云量十分制」定义重建晴天与阴天日数，逐月与 WRCC 发表值对照
# 数据源   : clean.pkl
# 依赖     : pandas, numpy
# 怎么跑   : python verify2.py
# 输出     : 打印到 stdout
# 原始文件名: verify2.py
# 授权     : 本脚本以 MIT 授权公开；它读取的气象观测数据属于公有领域。
# =============================================================================

import pandas as pd, numpy as np
df = pd.read_pickle("clean.pkl")
# WRCC/NCDC definition: mean DAYTIME sky cover in tenths.
# clear 0-3/10, partly cloudy 4-7/10, cloudy 8-10/10
frac={0:0.0, 1:1.5/8, 2:3.5/8, 3:6.0/8, 4:1.0, 5:1.0}
df["f"]=df["cov"].map(frac)
df["date"]=df["hr"].dt.date
# daylight window per month (sun above horizon at KSEA)
win={1:(8,16),2:(8,17),3:(7,18),4:(7,19),5:(6,20),6:(5,21),
     7:(6,21),8:(6,20),9:(7,19),10:(8,18),11:(8,16),12:(8,16)}
wrcc_cloudy={1:24,2:21,3:22,4:20,5:18,6:17,7:11,8:12,9:13,10:19,11:23,12:25}
wrcc_clear ={1:3,2:3,3:3,4:3,5:4,6:5,7:10,8:9,9:8,10:4,11:2,12:2}
print(f"{'mo':4s}{'ASOS cloudy':>12s}{'WRCC':>7s}{'diff':>7s}   {'ASOS clear':>11s}{'WRCC':>7s}{'diff':>7s}")
tot_c=tot_w=0
for mo in range(1,13):
    s=df[(df.month==mo)&(df.hour.between(*win[mo]))]
    d=s.groupby("date")["f"].agg(["mean","count"])
    d=d[d["count"]>=win[mo][1]-win[mo][0]-1]
    days_in={1:31,2:28.25,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}[mo]
    cl=(d["mean"]>=0.75).mean()*days_in     # 8/10 rounds from 0.75
    cr=(d["mean"]<=0.35).mean()*days_in     # 3/10 rounds up to 0.35
    tot_c+=cl; tot_w+=wrcc_cloudy[mo]
    print(f"{mo:<4d}{cl:>12.1f}{wrcc_cloudy[mo]:>7d}{cl-wrcc_cloudy[mo]:>+7.1f}   {cr:>11.1f}{wrcc_clear[mo]:>7d}{cr-wrcc_clear[mo]:>+7.1f}")
print(f"{'ann':4s}{tot_c:>12.1f}{tot_w:>7d}{tot_c-tot_w:>+7.1f}")
