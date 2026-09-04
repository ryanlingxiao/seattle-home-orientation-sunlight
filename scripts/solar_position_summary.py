# -*- coding: utf-8 -*-
# =============================================================================
# 太阳位置汇总（夏至 / 冬至 / 四到九月傍晚）
# 出自《西雅图买房该选什么朝向？后院八个方向的光照，用 21 年气象数据算了一遍》
# https://xceedwa.com/blog/seattle-home-orientation-sunlight
#
# 算什么   : 夏至冬至的日出日落方位与时刻、白昼长度、正午高度角、太阳待在罗盘北半边的时长（7 小时 01 分占 44.1%）、以及 4 到 9 月太阳过正南与日落的逐日时刻
# 坐标     : 47.61 N / 122.33 W / 海拔 72 m / America/Los_Angeles
# 依赖     : pvlib, pandas, numpy   （pip install pvlib pandas numpy）
# 怎么跑   : python solar_position_summary.py
# 输出     : 打印到 stdout
# 原始文件名: _calc.py
# 🔴 本版已修正原始脚本末尾「最早日落」比较错误，详见文件末尾注释。
# 授权     : 本脚本以 MIT 授权公开。
# =============================================================================

"""新卡用到的太阳几何，全部 pvlib（NREL SPA）现算。Seattle 47.61N / 122.33W / 72 m。"""
import sys, numpy as np, pandas as pd, pvlib
sys.stdout.reconfigure(encoding='utf-8')
lat, lon, tz, alt = 47.61, -122.33, 'America/Los_Angeles', 72
loc = pvlib.location.Location(lat, lon, tz, alt)

def day(d):
    idx = pd.date_range(f'{d} 00:00', f'{d} 23:59', freq='1min', tz=tz)
    sp = loc.get_solarposition(idx)
    return sp[sp['apparent_elevation'] > 0]

# 1 夏至：日出日落方位、东北西北时长
sp = day('2025-06-21')
rise, sett = sp.index[0], sp.index[-1]
daylen = len(sp)
north = sp[(sp['azimuth'] < 90) | (sp['azimuth'] > 270)]
noon = sp['apparent_elevation'].idxmax()
print("== 夏至 2025-06-21")
print(f"日出 {rise.strftime('%H:%M')} 方位 {sp['azimuth'].iloc[0]:.1f}°  日落 {sett.strftime('%H:%M')} 方位 {sp['azimuth'].iloc[-1]:.1f}°")
print(f"白昼 {daylen//60} 小时 {daylen%60} 分  东北+西北 {len(north)//60} 小时 {len(north)%60} 分  占 {len(north)/daylen*100:.1f}%")
print(f"正午 {noon.strftime('%H:%M')} 高度角 {sp['apparent_elevation'].max():.1f}° 方位 {sp.loc[noon,'azimuth']:.1f}°")
print("整点位置（方位°, 高度°）:")
for h in range(5, 22):
    t = pd.Timestamp(f'2025-06-21 {h:02d}:00', tz=tz)
    if t in sp.index:
        print(f"  {h:02d}:00  az {sp.loc[t,'azimuth']:.1f}  el {sp.loc[t,'apparent_elevation']:.1f}")

# 2 冬至正午
sp2 = day('2025-12-21')
n2 = sp2['apparent_elevation'].idxmax()
print("\n== 冬至 2025-12-21")
print(f"正午 {n2.strftime('%H:%M')} 高度角 {sp2['apparent_elevation'].max():.1f}°  日出方位 {sp2['azimuth'].iloc[0]:.1f}° 日落方位 {sp2['azimuth'].iloc[-1]:.1f}°  白昼 {len(sp2)//60} 小时 {len(sp2)%60} 分")

# 3 回归线：夏至太阳赤纬
dec = pvlib.solarposition.declination_spencer71(pd.Timestamp('2025-06-21', tz=tz).dayofyear)
print(f"\n== 夏至太阳赤纬 {np.degrees(dec):.2f}°（直射点在北回归线 23.44°N）；Seattle 比它再往北 {47.61-23.44:.2f}°；几何正午高度 = 90-(47.61-23.44) = {90-(47.61-23.44):.2f}°")

# 4 四到九月：太阳转到西半边（方位过 180°）的时刻与日落时刻
print("\n== 四到九月 太阳在西半边天的时段（方位 >180° 到日落）")
rows = []
for m in range(4, 10):
    for dd in (1, 15):
        d = f'2025-{m:02d}-{dd:02d}'
        s = day(d)
        west = s[s['azimuth'] > 180]
        rows.append((d, west.index[0], west.index[-1]))
        print(f"  {d}  过正南 {west.index[0].strftime('%H:%M')}  日落 {west.index[-1].strftime('%H:%M')}")
# 🔴 已修正的缺陷：原版这一行写的是 min/max(r[2] for r in rows)，直接比较带时区的完整
# 时间戳，比的是「哪一天」而不是「几点几分」，于是 04-01 那天（日落 19:38）被误判成
# 「最早日落」。正确做法是按时钟时刻比较。修正后得到最早 19:18（9 月中）、最晚 21:08。
# ⚠ 采样网格只取每月 1 日与 15 日，所以最晚日落落在采样点 07-01 上（真实峰值在 6 月底）。
_clock = lambda t: (t.hour, t.minute)
t1min = min((r[2] for r in rows), key=_clock); t1max = max((r[2] for r in rows), key=_clock)
print(f"  最早过正南 {min(r[1].strftime('%H:%M') for r in rows)} · 最晚过正南 {max(r[1].strftime('%H:%M') for r in rows)}")
print(f"  最早日落 {t1min.strftime('%H:%M')} · 最晚日落 {t1max.strftime('%H:%M')}")
