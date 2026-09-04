# -*- coding: utf-8 -*-
# =============================================================================
# 雨季 SCT 以上占比
# 出自《西雅图买房该选什么朝向？后院八个方向的光照，用 21 年气象数据算了一遍》
# https://xceedwa.com/blog/seattle-home-orientation-sunlight
#
# 算什么   : 雨季逐时「疏云或更好」的占比，以及上下午差
# 数据源   : clean.pkl
# 依赖     : pandas, numpy
# 怎么跑   : python t7.py
# 输出     : 打印到 stdout
# 原始文件名: t7.py
# 授权     : 本脚本以 MIT 授权公开；它读取的气象观测数据属于公有领域。
# =============================================================================

import pandas as pd
df = pd.read_pickle("clean.pkl")
dec=df[(df.month==12)&(df.hour.between(9,16))]
print("Dec daylight 09-16 BKN+OVC+VV share: %.1f%%"%((dec["cov"]>=3).mean()*100))
w=df[df.month.isin([11,12,1,2,3])].copy()
w["sctplus"]=(w["cov"]<=2)
print("\nwet season 'SCT or better' by local hour (%):")
print(w.groupby("hour")["sctplus"].mean().mul(100).round(2).to_string())
print("\nAM09-13 %.2f   PM14-18 %.2f  diff %+.2f"%(
 w[w.hour.between(9,13)].sctplus.mean()*100, w[w.hour.between(14,18)].sctplus.mean()*100,
 (w[w.hour.between(14,18)].sctplus.mean()-w[w.hour.between(9,13)].sctplus.mean())*100))
