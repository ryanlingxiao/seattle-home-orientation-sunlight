# -*- coding: utf-8 -*-
# =============================================================================
# 八方位墙的室内直射进深
# 出自《西雅图买房该选什么朝向？后院八个方向的光照，用 21 年气象数据算了一遍》
# https://xceedwa.com/blog/seattle-home-orientation-sunlight
#
# 算什么   : 太阳直射光水平走进屋里的深度 = 窗顶高 x 该朝向该时段的中位系数。产出文中的正南 3.1 尺 / 1.9 尺、西南 11.4 尺，改 HEAD 参数（7.0 改 9.0）即可得到 10 尺层高的 4.04 尺与 14.58 尺
# 坐标     : 47.61 N / 122.33 W / 海拔 72 m / America/Los_Angeles
# 依赖     : pvlib, pandas, numpy   （pip install pvlib pandas numpy）
# 怎么跑   : python sun_depth_eight_orientations.py
# 输出     : 打印到 stdout
# 原始文件名: 八方位进深计算.py
# 关键参数 : HEAD = 窗头高（英尺）。7.0 对应 8 尺层高，9.0 对应 10 尺层高
# 授权     : 本脚本以 MIT 授权公开。
# =============================================================================

"""八方位墙的室内直射进深。口径对齐项目已发表的两个数：
   正南墙 5-7pm 中位系数 0.27 → 1.9 尺；西南墙 1.62 → 11.4 尺。"""
import sys, numpy as np, pandas as pd, pvlib
sys.stdout.reconfigure(encoding='utf-8')
lat, lon, tz, alt = 47.61, -122.33, 'America/Los_Angeles', 72
loc = pvlib.location.Location(lat, lon, tz, alt)
HEAD = 7.0                      # 窗头高（尺），8 尺层高
DIRS = [("正南 S",180),("西南 SW",225),("正西 W",270),("西北 NW",315),
        ("正北 N",0),("东北 NE",45),("正东 E",90),("东南 SE",135)]

def window(months, h0, h1):
    idx = pd.date_range('2026-01-01', '2026-12-31 23:59', freq='1min', tz=tz)
    idx = idx[idx.month.isin(months)]
    idx = idx[(idx.hour*60+idx.minute >= h0*60) & (idx.hour*60+idx.minute < h1*60)]
    sp = loc.get_solarposition(idx)
    return sp[sp['apparent_elevation'] > 0]

def depth(sp, wall_az):
    d = np.radians(((sp['azimuth'] - wall_az + 180) % 360) - 180)   # 方位差
    el = np.radians(sp['apparent_elevation'])
    hit = (np.abs(d) < np.radians(90))
    k = np.where(hit, np.cos(d)/np.tan(el), 0.0)
    k = np.clip(k, 0, None)
    return k, hit

print("窗头 7 尺（8 尺层高）· 只统计太阳真的照到这面墙的分钟\n")
for label, (mons, h0, h1) in [("傍晚：4 到 9 月 · 17:00 到 19:00", (list(range(4,10)),17,19)),
                              ("正午：夏至前后 · 12:00 到 13:00", ([6],12,13))]:
    sp = window(*[mons,h0,h1])
    print(f"── {label}")
    print(f"{'朝向':<8}{'有直射的比例':>12}{'系数中位':>10}{'进深(尺)':>10}")
    rows=[]
    for name, az in DIRS:
        k, hit = depth(sp, az)
        pct = hit.mean()*100
        med = float(np.median(k[hit])) if hit.any() else 0.0
        rows.append((name, pct, med, med*HEAD))
    for n,p,m,dd in rows:
        print(f"{n:<8}{p:>11.1f}%{m:>10.2f}{dd:>10.1f}")
    print()
