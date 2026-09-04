# -*- coding: utf-8 -*-
# =============================================================================
# 第 1 步 · 抓取 KSEA 原始云观测
# 出自《西雅图买房该选什么朝向？后院八个方向的光照，用 21 年气象数据算了一遍》
# https://xceedwa.com/blog/seattle-home-orientation-sunlight
#
# 算什么   : 从 Iowa State Mesonet 下载 KSEA 站 2005 到 2025 的逐时 ASOS/METAR 云量、能见度与天气现象码
# 数据源   : Iowa State University Environmental Mesonet · ASOS/METAR 存档 · 站点 KSEA · 2005-01-01 到 2025-12-30（公有领域）
# 依赖     : 仅标准库（urllib）
# 怎么跑   : python fetch.py
# 输出     : sea_asos.csv（约 9 MB，183,690 行）
# 原始文件名: fetch.py
# 授权     : 本脚本以 MIT 授权公开；它读取的气象观测数据属于公有领域。
# =============================================================================

import urllib.request, time, sys

url = ("https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?"
       "station=SEA"
       "&data=skyc1&data=skyl1&data=skyc2&data=skyc3&data=skyc4"
       "&data=vsby&data=wxcodes"
       "&year1=2005&month1=1&day1=1"
       "&year2=2025&month2=12&day2=31"
       "&tz=America%2FLos_Angeles"
       "&format=onlycomma&latlon=no&report_type=3")

print("GET", url)
t0=time.time()
try:
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 research"})
    with urllib.request.urlopen(req, timeout=900) as r:
        data = r.read()
    print("HTTP", r.status, "bytes", len(data), "sec", round(time.time()-t0,1))
    open("sea_asos.csv","wb").write(data)
except Exception as e:
    print("FAIL", type(e).__name__, e)
    sys.exit(1)
