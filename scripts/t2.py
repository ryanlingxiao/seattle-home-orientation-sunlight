# -*- coding: utf-8 -*-
# =============================================================================
# 表二 · 逐月逐时矩阵与上下午切分
# 出自《西雅图买房该选什么朝向？后院八个方向的光照，用 21 年气象数据算了一遍》
# https://xceedwa.com/zh/seattle-home-orientation-sunlight
#
# 算什么   : 月份 × 本地小时的云况矩阵，以及上午 09-13 对下午 14-18 的差距。产出雨季 4.27 个百分点与 June gloom 那组数字
# 数据源   : clean.pkl
# 依赖     : pandas, numpy
# 怎么跑   : python t2.py
# 输出     : t2_month_hour_nosun.csv · t2_month_hour_ovc.csv
# 原始文件名: t2.py
# 授权     : 本脚本以 MIT 授权公开；它读取的气象观测数据属于公有领域。
# =============================================================================

import pandas as pd, numpy as np
df = pd.read_pickle("clean.pkl")
pd.set_option("display.width",300)
df["nosun"] = df["cov"].isin([3,4,5])   # BKN OVC VV
df["ovc"]   = df["cov"].isin([4,5])     # OVC VV

WET=[11,12,1,2,3]
MN={11:"Nov",12:"Dec",1:"Jan",2:"Feb",3:"Mar",6:"Jun",7:"Jul",8:"Aug"}

print("=== TABLE 2A: BKN+OVC+VV %, month x local hour ===")
m = df[df.month.isin(WET+[6,7,8])]
p = m.pivot_table(index="hour", columns="month", values="nosun", aggfunc="mean").mul(100)
p = p[[11,12,1,2,3,6,7,8]]; p.columns=[MN[c] for c in p.columns]
print(p.round(1).to_string())
p.to_csv("t2_month_hour_nosun.csv")

print("\n=== TABLE 2B: OVC(+VV) only %, month x local hour ===")
p2 = m.pivot_table(index="hour", columns="month", values="ovc", aggfunc="mean").mul(100)
p2 = p2[[11,12,1,2,3,6,7,8]]; p2.columns=[MN[c] for c in p2.columns]
print(p2.round(1).to_string())
p2.to_csv("t2_month_hour_ovc.csv")

print("\n=== Q2: 09-13 vs 14-18, local clock ===")
def seg(sub,label):
    am = sub[sub.hour.between(9,13)]; pm = sub[sub.hour.between(14,18)]
    print(f"{label:12s} AM(09-13) BKN+OVC+VV={am.nosun.mean()*100:6.2f}  PM(14-18)={pm.nosun.mean()*100:6.2f}  diff={(am.nosun.mean()-pm.nosun.mean())*100:+6.2f}pp"
          f" | OVC only AM={am.ovc.mean()*100:6.2f} PM={pm.ovc.mean()*100:6.2f} diff={(am.ovc.mean()-pm.ovc.mean())*100:+6.2f}pp")
seg(df[df.month.isin(WET)],"WET Nov-Mar")
for mo in WET: seg(df[df.month==mo], MN[mo])
seg(df[df.month.isin([6,7,8])],"SUM Jun-Aug")
for mo in [6,7,8]: seg(df[df.month==mo], MN[mo])

print("\n=== Q2b: daylight-safe split, 09-12 vs 13-16 (Dec sunset ~16:20) ===")
def seg2(sub,label):
    am = sub[sub.hour.between(9,12)]; pm = sub[sub.hour.between(13,16)]
    print(f"{label:12s} AM(09-12)={am.nosun.mean()*100:6.2f}  PM(13-16)={pm.nosun.mean()*100:6.2f}  diff={(am.nosun.mean()-pm.nosun.mean())*100:+6.2f}pp"
          f" | OVC AM={am.ovc.mean()*100:6.2f} PM={pm.ovc.mean()*100:6.2f} diff={(am.ovc.mean()-pm.ovc.mean())*100:+6.2f}pp")
seg2(df[df.month.isin(WET)],"WET Nov-Mar")
for mo in WET: seg2(df[df.month==mo], MN[mo])
