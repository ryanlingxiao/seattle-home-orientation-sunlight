# -*- coding: utf-8 -*-
# =============================================================================
# 正北墙傍晚直射的独立复算
# 出自《西雅图买房该选什么朝向？后院八个方向的光照，用 21 年气象数据算了一遍》
# https://xceedwa.com/blog/seattle-home-orientation-sunlight
#
# 算什么   : 用逐分钟太阳位置独立验证「4 到 9 月傍晚正北墙比正南墙拿到更多直射」，并逐月拆开确认优势只集中在 5 到 7 月。产出文中的北墙 18,298 分钟对南墙 13,197 分钟
# 坐标     : 47.61 N / 122.33 W / 海拔 72 m / America/Los_Angeles
# 依赖     : pvlib, pandas, numpy   （pip install pvlib pandas numpy）
# 怎么跑   : python verify_north_evening.py
# 输出     : 打印到 stdout
# 原始文件名: _verify_north.py
# 授权     : 本脚本以 MIT 授权公开。
# =============================================================================

"""复算验证：4 到 9 月傍晚，正北墙是否真的比正南墙拿到更多直射。
口径与 `八方位进深计算.py` 完全一致：47.61N / 122.33W / 72 m /
America/Los_Angeles / 逐分钟 / apparent_elevation > 0。
时间窗对齐 PVGIS 表 4A：本地小时 17、18、19（即 17:00 到 20:00）。
"""
import sys, numpy as np, pandas as pd, pvlib
sys.stdout.reconfigure(encoding='utf-8')

lat, lon, tz, alt = 47.61, -122.33, 'America/Los_Angeles', 72
loc = pvlib.location.Location(lat, lon, tz, alt)
MONTHS = list(range(4, 10))          # 4 到 9 月
WALLS = [("正北 N", 0), ("东北 NE", 45), ("正东 E", 90), ("东南 SE", 135),
         ("正南 S", 180), ("西南 SW", 225), ("正西 W", 270), ("西北 NW", 315)]


def build(year, h0, h1):
    idx = pd.date_range(f'{year}-01-01', f'{year}-12-31 23:59', freq='1min', tz=tz)
    idx = idx[idx.month.isin(MONTHS)]
    m = idx.hour * 60 + idx.minute
    idx = idx[(m >= h0 * 60) & (m < h1 * 60)]
    sp = loc.get_solarposition(idx)
    sp = sp[sp['apparent_elevation'] > 0]
    cs = loc.get_clearsky(sp.index, model='ineichen')
    return sp, cs


def wall_stats(sp, cs, wall_az):
    """垂直墙面。cos(入射角) = cos(高度角) * cos(方位差)。"""
    d = np.radians(((sp['azimuth'] - wall_az + 180) % 360) - 180)
    el = np.radians(sp['apparent_elevation'])
    cos_inc = np.cos(el) * np.cos(d)
    lit = cos_inc > 0
    # 几何量：受照分钟数
    minutes = int(lit.sum())
    # 能量量：晴空 DNI 投到墙面，逐分钟求和（Wh/m²），只是相对比较用
    dni_wall = np.where(lit, cs['dni'].values * cos_inc.values, 0.0)
    energy = dni_wall.sum() / 60.0 / 1000.0     # kWh/m²，19 年不做平均，只做相对比较
    return minutes, energy, float(np.median(cos_inc[lit])) if minutes else 0.0


for year in (2025, 2026):
    for label, h0, h1 in [("傍晚 17:00 到 20:00（对齐 PVGIS 表 4A）", 17, 20),
                          ("傍晚 17:00 到日落（全时段）", 17, 24)]:
        sp, cs = build(year, h0, h1)
        total = len(sp)
        print(f"\n=== {year} 年 · 4 到 9 月 · {label} ===")
        print(f"该窗口内太阳在地平线以上的总分钟数：{total}")
        print(f"{'墙面朝向':<10}{'受直射分钟':>12}{'占窗口比例':>12}{'晴空墙面直射(kWh/m²)':>24}")
        rows = []
        for name, az in WALLS:
            mins, en, med = wall_stats(sp, cs, az)
            rows.append((name, mins, en))
            print(f"{name:<10}{mins:>12}{mins/total*100:>11.1f}%{en:>24.1f}")
        d = {n: (m, e) for n, m, e in rows}
        n_m, n_e = d["正北 N"]
        s_m, s_e = d["正南 S"]
        print(f"\n  正北受直射分钟 {n_m} vs 正南 {s_m} → 正北是正南的 {n_m/s_m:.2f} 倍")
        print(f"  正北墙面直射能量 {n_e:.1f} vs 正南 {s_e:.1f} → 正北是正南的 {n_e/s_e:.2f} 倍")
        print(f"  结论：正北 > 正南 ? {'成立' if n_e > s_e else '不成立'}")

# 逐月拆开看，确认「4 到 9 月」整体成立还是只有盛夏成立
print("\n\n=== 逐月拆解（2026 年 · 17:00 到 20:00 · 晴空墙面直射 kWh/m²）===")
sp, cs = build(2026, 17, 20)
print(f"{'月份':<6}{'正北 N':>12}{'正南 S':>12}{'正西 W':>12}{'北/南':>10}")
for mo in MONTHS:
    mask = sp.index.month == mo
    spm, csm = sp[mask], cs[mask]
    _, n_e, _ = wall_stats(spm, csm, 0)
    _, s_e, _ = wall_stats(spm, csm, 180)
    _, w_e, _ = wall_stats(spm, csm, 270)
    ratio = f"{n_e/s_e:.2f}" if s_e > 0 else "—"
    print(f"{mo:<6}{n_e:>12.2f}{s_e:>12.2f}{w_e:>12.2f}{ratio:>10}")

# 太阳方位角区间，验证「太阳绕到罗盘北半边」
print("\n\n=== 傍晚太阳方位角区间（2026 年 · 4 到 9 月 · 17:00 到日落）===")
sp2, _ = build(2026, 17, 24)
az = sp2['azimuth']
print(f"方位角范围：{az.min():.1f} 度 到 {az.max():.1f} 度")
print(f"方位角 > 270 度（即已过正西、进入罗盘北半边）的分钟数：{int((az > 270).sum())}"
      f"，占 {(az > 270).mean()*100:.1f}%")
print(f"方位角 < 270 度（仍在罗盘南半边）的分钟数：{int((az <= 270).sum())}"
      f"，占 {(az <= 270).mean()*100:.1f}%")
