# Seattle Home Orientation & Sunlight

**Reproducible evidence for a long-form article on how house orientation affects sunlight in Seattle.**
Every number in the article can be recomputed from the scripts and data in this repository.

**这是一篇文章的可复算证据。文章里的每一个数字，你都可以自己跑一遍。**

- **Article / 文章**: <https://xceedwa.com/blog/seattle-home-orientation-sunlight>
- **Video / 视频**: <https://www.youtube.com/watch?v=teF-Q4JQ-E8>
- **Author / 作者**: Ryan Xu· Xceed Realty · Bellevue, WA
- **License**: MIT for code, CC BY 4.0 for data and documentation. See [Licensing](#licensing--授权).

---

## Table of contents

- [English](#english)
  - [What this is](#what-this-is)
  - [Quick start](#quick-start)
  - [Which script produces which number](#which-script-produces-which-number)
  - [Repository layout](#repository-layout)
  - [Data sources](#data-sources)
  - [Known limitations](#known-limitations)
  - [What this repository deliberately does not contain](#what-this-repository-deliberately-does-not-contain)
  - [Licensing](#licensing--授权)
- [中文](#中文)

---

# English

## What this is

This is **not a software project**. It is the evidence pack behind one article: a study of how the eight compass orientations of a Seattle house perform for daylight, using 21 years of airport cloud observations and minute-by-minute solar geometry.

It exists so that a reader does not have to take any number on trust. Install three packages, run three scripts, and you should get the article's figures to the digit.

Location used throughout: Seattle, 47.61 N / 122.33 W, elevation 72 m, `America/Los_Angeles`. Cloud observations come from the Sea-Tac Airport station (KSEA, 47.4444 N / 122.3139 W).

## Quick start

Requires Python 3.9 or newer. Tested on Python 3.12.10.

```bash
git clone https://github.com/ryanlingxiao/seattle-home-orientation-sunlight.git
cd seattle-home-orientation-sunlight
pip install -r requirements.txt
cd scripts
```

### Group A: solar geometry, no external data needed

These three run immediately after installing dependencies. Each takes roughly 30 to 120 seconds because the solar position is evaluated minute by minute.

```bash
python solar_position_summary.py        # solstices, day length, noon altitude, sunset times
python sun_depth_eight_orientations.py  # how deep direct beam reaches indoors, eight orientations
python verify_north_evening.py          # independent recomputation of the north wall in the evening
```

Expected output, matching the article exactly:

| Script | Key expected values |
|---|---|
| `solar_position_summary.py` | Summer solstice daylight **15 h 55 m**; sun in the northern half of the compass **7 h 01 m = 44.1%**; solstice noon altitude **65.8°**; winter solstice noon **19.0°**, daylight **8 h 22 m**; earliest sunset **19:18**, latest **21:08** |
| `sun_depth_eight_orientations.py` | South evening depth **1.9 ft**; southwest evening **11.4 ft**; south at summer noon **3.1 ft**. Change `HEAD = 7.0` to `9.0` (a 10 ft ceiling) and these become **4.0** and **14.6** |
| `verify_north_evening.py` | North wall lit **18,298 minutes** vs south **13,197** in Apr to Sep 17:00 to 20:00; clear-sky beam ratio **1.07**; the advantage sits almost entirely in May, June and July |

### Group B: cloud observations, fetch about 9 MB first

The raw observation file is **not** stored in this repository, on purpose. `fetch.py` pulls the current official copy straight from Iowa State University, which is more trustworthy than a frozen mirror. The download takes a few minutes.

```bash
python fetch.py     # downloads sea_asos.csv, about 9 MB, 183,690 rows
python analyze.py   # cleans and grades cloud cover, writes clean.pkl
python t1.py        # wet-season and summer cloud cover by hour
python t2.py        # month x hour matrix, morning vs afternoon
python t4.py        # hourly inflection, precipitation, visibility, conditional probability
python t5.py        # same, after filtering out sun elevations below 5 degrees
python t6.py        # rebuild NOAA clear/cloudy day counts from ASOS as a cross-check
python t7.py        # wet-season "scattered or better" share by hour
python verify2.py   # month-by-month check against WRCC published day counts
```

`analyze.py` must run before `t1` through `t7` and `verify2`, since they all read `clean.pkl`.

`verify.py` additionally needs `sea.epw`, a TMY3 typical-meteorological-year file that is **not** bundled here for licensing reasons. Download station **727930** from the EnergyPlus weather archive or NREL NSRDB, place it in `scripts/`, then run `python verify.py`.

### Reproducibility check

`t1.py` and `t2.py` write four CSV files. On a clean run from freshly fetched data, they should come out **byte-identical** to the copies committed in `data/`. That comparison is the fastest way to confirm your environment reproduces the published tables:

```bash
for f in t1_wet.csv t3_summer.csv t2_month_hour_nosun.csv t2_month_hour_ovc.csv; do
  cmp -s "$f" "../data/$f" && echo "OK  $f" || echo "DIFFERS  $f"
done
```

## Which script produces which number

Left column is a claim as it appears in the article. Right column is the command that produces it.

### Solar geometry and indoor depth

| Claim in the article | Script |
|---|---|
| Summer solstice daylight is 15 h 55 m | `python solar_position_summary.py` |
| The sun spends 7 h 01 m, or 44.1% of the solstice day, in the northern half of the compass | `python solar_position_summary.py` |
| Solstice noon altitude 65.8°, winter solstice noon 19.0° | `python solar_position_summary.py` |
| Sunset ranges from 19:18 at the earliest to 21:08 at the latest across Apr to Sep | `python solar_position_summary.py` |
| The sun crosses due south between 13:05 and 13:16 | `python solar_position_summary.py` |
| Direct beam through a south wall reaches 3.1 ft indoors at summer noon | `python sun_depth_eight_orientations.py` |
| In the evening, south reaches 1.9 ft while southwest reaches 11.4 ft | `python sun_depth_eight_orientations.py` |
| Raising the ceiling from 8 ft to 10 ft moves those to 4.04 ft and 14.58 ft | `python sun_depth_eight_orientations.py` with `HEAD = 9.0` |
| The north wall gets 18,298 lit minutes against the south wall's 13,197 | `python verify_north_evening.py` |
| That north-wall advantage comes almost entirely from May, June and July | `python verify_north_evening.py` |

### Cloud observations, 21 years at KSEA

All of these require `fetch.py` then `analyze.py` first.

| Claim in the article | Script |
|---|---|
| 183,690 rows downloaded, 183,674 usable observations | `python analyze.py` |
| Wet-season daytime is 79% to 86% fully clouded | `python t1.py` |
| Genuinely clear sky is only about 2% of wet-season daylight hours | `python t1.py` |
| 09:00 is the cloudiest hour of the day at 85.6% | `python t1.py` |
| Morning beats afternoon by 4.27 percentage points in the wet season | `python t2.py` |
| June gloom: overcast drops 15.05 points from morning to afternoon in summer | `python t2.py` |
| 14:00 shows the single sharpest overcast drop, 3.51 points | `python t4.py` |
| Of 1,636 wet-season days already overcast at 10:00, 66.6% are still overcast at 14:00 | `python t4.py` |
| Precipitation occupies 18.62% of morning hours against 20.34% of afternoon hours | `python t4.py` |
| Visibility averages 8.30 statute miles at its worst hour against 9.23 at its best | `python t4.py` |
| Filtering out sun elevations below 5°, the morning-afternoon gap shrinks to 3.06 points | `python t5.py` |
| `CLR/FEW` runs 8.52% in the morning against 7.96% in the afternoon | `python t5.py` |
| ASOS-rebuilt December clear and cloudy day counts agree with NOAA's published values | `python t6.py` |
| Measured percent of possible sunshine is 23% in December and 47% for the year | `python verify.py` against `data/wrcc_ksea_reference_values.csv` |
| Month-by-month clear and cloudy day counts reconcile with WRCC | `python verify2.py` |

### Tables that ship as data rather than as a script

| Claim in the article | File |
|---|---|
| Table A, annual total irradiance index for all eight orientations, south = 100 | `data/eight_orientations_seattle.csv` |
| Table B, evening irradiance index for all eight orientations, west = 100 | `data/eight_orientations_seattle.csv` |
| Southwest reaches 95.6% of south annually and 4.70x south in the evening | `data/eight_orientations_seattle.csv` |
| West is first in the evening but falls to 74.5% of south annually | `data/eight_orientations_seattle.csv` |
| Northwest is second in the evening at 175.03 but only 42.9 annually | `data/eight_orientations_seattle.csv` |
| Southeast, east and northeast all land on 16.79 kWh/m² in the evening | `data/eight_orientations_seattle.csv` |
| The five-tier ranking of the eight orientations | `data/eight_orientations_seattle.csv`, `tier` column |
| Great Rooms containing a kitchen area 77.2%, a breakfast nook 61.4% | `data/nahb_2019_table3_great_room_contents.csv` |

⚠ **On the Table A and Table B values.** These come from PVGIS v5.3 (PVGIS-ERA5, 2005 to 2023, vertical surface, terrain off), queried through the European Commission's public interface. They are not regenerated by a script in this repository; the CSV is the machine-readable archive of that query, and `verify_north_evening.py` independently confirms its most counterintuitive row using pvlib rather than PVGIS.

## Repository layout

```
seattle-home-orientation-sunlight/
├── README.md
├── LICENSE                 MIT, applies to the code
├── LICENSE-DATA            CC BY 4.0, applies to data and documentation
├── requirements.txt
├── .gitignore
├── scripts/                13 scripts, each with a header stating what it computes
│   ├── README.md           per-script method notes
│   ├── fetch.py            step 1, download raw observations
│   ├── analyze.py          step 2, clean and grade cloud cover
│   ├── t1.py t2.py t4.py t5.py t6.py t7.py
│   ├── verify.py verify2.py
│   ├── solar_position_summary.py
│   ├── sun_depth_eight_orientations.py
│   └── verify_north_evening.py
├── data/                   aggregate tables only, no raw observations
│   ├── README.md           data dictionary and provenance
│   ├── eight_orientations_seattle.csv
│   ├── nahb_2019_table3_great_room_contents.csv
│   ├── t1_wet.csv t3_summer.csv
│   ├── t2_month_hour_nosun.csv t2_month_hour_ovc.csv
│   └── wrcc_ksea_reference_values.csv
└── sources/
    ├── SOURCES.md          every institution, year, table number and official URL
    └── three screenshots of the NOAA and pvlib source pages
```

## Data sources

Full detail, including year, sampling frame and table number for each, is in [`sources/SOURCES.md`](sources/SOURCES.md).

| Source | Institution · year | Used for | Rights |
|---|---|---|---|
| ASOS / METAR cloud observations, station KSEA | Iowa State University Environmental Mesonet, 2005-01-01 to 2025-12-30 | Every cloud-cover conclusion | Public domain, free to use and redistribute; attribution appreciated, not required |
| Vertical-surface irradiance, eight azimuths | European Commission PVGIS v5.3, PVGIS-ERA5, 2005 to 2023 | Table A and Table B | Free to use, attribution required |
| Solar position, NREL SPA | pvlib, minute-by-minute | Solar geometry, indoor depth, north-wall check | pvlib is BSD-3-Clause |
| Percent of possible sunshine; clear and cloudy day counts | Western Regional Climate Center, Sea-Tac | Calibration of the cloud-derived estimates | Underlying NCDC/NOAA observations are US federal works, public domain |
| Comparative Climatic Data | NOAA / NCEI, station 24233 | Published clear and cloudy day counts | US federal work, public domain |
| *Spaces in New Homes*, Table 3 | NAHB, Paul Emrath, 2019-03-14, 153 builders | Great Room composition | Facts re-keyed under fair use; the report itself is not redistributed here |

## Known limitations

These three apply to every number in this repository and in the article. **Please carry them with any figure you quote.**

1. **The cloud observations come from the Sea-Tac Airport weather station.** That station sits roughly 15 to 25 miles from Bellevue, Kirkland and Redmond, with Lake Washington in between. The conclusions hold strictly for the Sea-Tac area.
2. **Every geometric and irradiance figure is an upper bound.** It is what a plot facing that direction could receive, with no trees, no neighbouring houses and no eaves. A real house receives that ceiling multiplied by an obstruction discount, and that discount is frequently larger than the gap between orientations.
3. **The MLS `Home Faces` sample is too small to support any price conclusion, and none is drawn.** Of 1,051 Bellevue closings examined, only 396 (37.7%) had the orientation field filled in. The article states this and stops there.

A fourth caveat applies to Table A and Table B specifically: PVGIS-ERA5 is a reanalysis product and was found to overstate direct beam relative to the TMY3 cross-check in `verify.py`. The eight orientations are compared against each other on a single consistent basis, so the **ratios** are the usable output, not the absolute kWh/m² values.

## What this repository deliberately does not contain

Naming what was left out, and why, is part of the evidence.

| Not included | Reason |
|---|---|
| `sea_asos.csv`, the 9 MB raw observation file | Public domain and freely redistributable, but it is a derived copy. `fetch.py` retrieves the current official version in one command, which is better than a frozen mirror. Excluded on engineering grounds only. |
| `sea.epw`, the TMY3 typical meteorological year | Third-party distributed weather file with more complex terms. Download station 727930 from EnergyPlus or NREL NSRDB. |
| `clean.pkl` | Intermediate artifact, rebuilt by one run of `analyze.py`. |
| The NAHB report PDF and full-page scans | Third-party copyrighted work. Table 3's facts are re-keyed into a CSV with the source cited and the official link given; facts themselves are not copyrightable. |
| NWMLS Matrix screenshots | The screenshot shows the MLS system interface. Publishing it is outside the scope of member authorization, and it would add nothing: the article states the field name and all eight of its values in text, and RESO Data Dictionary 1.7 `DirectionFaces` is publicly checkable by anyone. |
| Verbatim saved WRCC web pages | The pages carry their own copyright notice. The Sea-Tac values are re-keyed into `data/wrcc_ksea_reference_values.csv` with the official URL given, the same treatment applied to the NAHB table. |
| One information card from the video, `c08` | It carries an incorrect denominator: it read NAHB's 77.2% and 61.4% as shares of all homes, when the base is Great Rooms specifically. The card is retired, the article corrects the figure in text, and the card is not republished anywhere. |
| Any client, listing-level or commercial data | Never in scope. |

## Licensing · 授权

**Recommendation, and the reasoning behind it: MIT for the code, CC BY 4.0 for the data and documentation.**

- **Code → MIT.** The scripts are short analytical utilities whose value is that people run and adapt them without friction. MIT is the lowest-friction permissive license, it is what every script header already declares, and it sits comfortably alongside pvlib's BSD-3-Clause. A copyleft license here would deter exactly the casual reuse the repository is built to invite.
- **Data and documentation → CC BY 4.0.** The point of the eight-orientation table is that other people quote it. CC BY 4.0 permits that freely while **requiring attribution**, which is the one thing worth asking for: it keeps the figures tied to their source and their caveats rather than drifting loose. MIT would technically cover data too, but it is written for software and reads oddly on a CSV, so a Creative Commons license states the intent more clearly.

Note that CC BY 4.0 covers **this project's compilation and derived values**. The underlying observations from Iowa State Environmental Mesonet, NOAA / NCEI and WRCC are in the public domain and carry no such condition.

Suggested citation:

> Ryan Xu (2026). *Seattle Home Orientation & Sunlight: reproducible evidence.* https://github.com/ryanlingxiao/seattle-home-orientation-sunlight

## Contact

Ryan Xu
Xceed Realty · Bellevue, WA
Washington State real estate broker, license **20108301**
<ryan@xceedwa.com> · <https://xceedwa.com/>

Issues and corrections are welcome. If you find a number that does not reproduce, please open an issue with your Python and library versions.

---

# 中文

## 这是什么

这**不是一个软件项目**，是一篇文章的证明素材。那篇文章研究的是：西雅图一栋房子的八个朝向，在采光上各自表现如何。依据是 21 年的机场云观测，加上逐分钟的太阳几何计算。

它存在的意义是，读者不必相信任何一个数字。装三个包，跑三个脚本，你应该拿到与文章一字不差的结果。

全文坐标：Seattle，47.61 N / 122.33 W，海拔 72 m，`America/Los_Angeles`。云观测取自 Sea-Tac 机场气象站（KSEA，47.4444 N / 122.3139 W）。

## 怎么跑

需要 Python 3.9 或更高版本。实测环境为 Python 3.12.10。

```bash
git clone https://github.com/ryanlingxiao/seattle-home-orientation-sunlight.git
cd seattle-home-orientation-sunlight
pip install -r requirements.txt
cd scripts
```

### A 组：太阳几何，不需要任何外部数据

装完依赖直接能跑。每个脚本大约 30 到 120 秒，因为太阳位置是逐分钟算的。

```bash
python solar_position_summary.py        # 夏至冬至、白昼长度、正午高度角、日落时刻
python sun_depth_eight_orientations.py  # 八个朝向的室内直射进深
python verify_north_evening.py          # 正北墙傍晚直射的独立复算
```

跑完应当与文章完全一致：

| 脚本 | 预期数值 |
|---|---|
| `solar_position_summary.py` | 夏至白昼 **15 小时 55 分**；太阳待在罗盘北半边 **7 小时 01 分，占 44.1%**；夏至正午 **65.8 度**；冬至正午 **19.0 度**，白昼 **8 小时 22 分**；日落最早 **19:18**、最晚 **21:08** |
| `sun_depth_eight_orientations.py` | 正南傍晚进深 **1.9 英尺**；西南傍晚 **11.4 英尺**；正南夏至正午 **3.1 英尺**。把 `HEAD = 7.0` 改成 `9.0`（10 尺层高），两个数字变成 **4.0** 与 **14.6** |
| `verify_north_evening.py` | 4 到 9 月 17:00 到 20:00，北墙受直射 **18,298 分钟**，南墙 **13,197 分钟**；晴空直射能量比 **1.07**；优势几乎全部来自 5、6、7 三个月 |

### B 组：云观测，要先抓约 9 MB 原始数据

原始观测文件**刻意不放进本仓库**。`fetch.py` 会直接从 Iowa State University 拉取官方当前版本，比一份冻结的副本更可信。下载需要几分钟。

```bash
python fetch.py     # 下载 sea_asos.csv，约 9 MB，183,690 行
python analyze.py   # 清洗与云量分级，产出 clean.pkl
python t1.py        # 雨季与夏季逐时云况
python t2.py        # 逐月逐时矩阵，上午对下午
python t4.py        # 逐时拐点、降水、能见度、条件概率
python t5.py        # 同上，但先剔除太阳高度角 5 度以下的时段
python t6.py        # 从 ASOS 侧重建 NOAA 的晴阴天日数，做交叉验证
python t7.py        # 雨季逐时「疏云或更好」的占比
python verify2.py   # 逐月对 WRCC 发表的晴阴天日数
```

`analyze.py` 必须先跑，`t1` 到 `t7` 与 `verify2` 都读它产出的 `clean.pkl`。

`verify.py` 另外还要 `sea.epw`，那是一份 TMY3 典型气象年文件，因授权较复杂**未随包分发**。请从 EnergyPlus 气象档案或 NREL NSRDB 下载站号 **727930**，放进 `scripts/` 再跑。

### 复现自检

`t1.py` 与 `t2.py` 会写出四个 CSV。从新抓的数据跑一遍干净流程，这四个文件应当与 `data/` 里已提交的副本**逐字节相同**。拿这个比对来确认你的环境复现得出已发表的表格，是最快的办法。

## 每个数字对应哪个脚本

左边是文章里的结论，右边是产出它的命令。完整对照表见上方英文小节 [Which script produces which number](#which-script-produces-which-number)，此处列出中文读者最常查的几条：

| 文章里的结论 | 脚本 |
|---|---|
| 夏至白昼 15 小时 55 分 | `python solar_position_summary.py` |
| 太阳有 7 小时 01 分在罗盘北半边，占 44.1% | `python solar_position_summary.py` |
| 夏至正午 65.8 度，冬至正午 19.0 度 | `python solar_position_summary.py` |
| 日落最早 19:18、最晚 21:08 | `python solar_position_summary.py` |
| 正南傍晚 1.9 英尺，西南傍晚 11.4 英尺 | `python sun_depth_eight_orientations.py` |
| 8 尺层高升到 10 尺，两个数字变成 4.04 与 14.58 | 同上，`HEAD = 9.0` |
| 北墙 18,298 分钟对南墙 13,197 分钟 | `python verify_north_evening.py` |
| 183,690 行，可用观测 183,674 条 | `python analyze.py` |
| 雨季白天 79% 到 86% 云盖满，真正万里无云只有 2% | `python t1.py` |
| 09:00 是全天最阴的一小时，85.6% | `python t1.py` |
| 上午对下午差 4.27 个百分点 | `python t2.py` |
| June gloom 掉 15.05 个百分点 | `python t2.py` |
| 14:00 的 `OVC` 单跌 3.51 个百分点 | `python t4.py` |
| 1,636 天里 66.6% 阴到下午 | `python t4.py` |
| 降水 18.62% 对 20.34%，能见度 8.30 对 9.23 | `python t4.py` |
| 剔除太阳高度角 5 度以下后差距只剩 3.06 个百分点 | `python t5.py` |
| 西南全年拿到正南的 95.6%，傍晚是正南的 4.7 倍 | `data/eight_orientations_seattle.csv` |
| 正西傍晚第一，全年总量只有正南的 74.5% | `data/eight_orientations_seattle.csv` |
| 东南、正东、东北傍晚都是 16.79 kWh/m² | `data/eight_orientations_seattle.csv` |
| Great Room 含厨房 77.2%，含早餐角 61.4% | `data/nahb_2019_table3_great_room_contents.csv` |

⚠ **表 A 与表 B 的数值说明**：它们取自 PVGIS v5.3（PVGIS-ERA5，2005 到 2023，垂直墙面，关地形），通过 European Commission 的公开接口查得，**不由本仓库的脚本重新生成**。那个 CSV 是这次查询的机读存档；其中最反直觉的那一行（正北傍晚高于正南），由 `verify_north_evening.py` 用 pvlib 而非 PVGIS 独立复核过。

## 数据出处

逐条的机构、年份、口径与表号见 [`sources/SOURCES.md`](sources/SOURCES.md)。

| 数据源 | 机构 · 年份 | 用它算什么 | 授权 |
|---|---|---|---|
| ASOS / METAR 云观测，站点 KSEA | Iowa State University Environmental Mesonet，2005-01-01 到 2025-12-30 | 全部云观测结论 | 公有领域，可自由使用与再分发，署名鼓励但非必须 |
| 垂直墙面辐照，八个方位 | European Commission PVGIS v5.3，PVGIS-ERA5，2005 到 2023 | 表 A 与表 B | 可自由使用，须署名 |
| 太阳位置，NREL SPA 算法 | pvlib，逐分钟 | 太阳几何、室内进深、正北复算 | pvlib 为 BSD-3-Clause |
| 实测日照百分率、晴阴天日数 | Western Regional Climate Center，Sea-Tac | 校准云观测反推值 | 底层 NCDC / NOAA 观测为美国联邦作品，公有领域 |
| Comparative Climatic Data | NOAA / NCEI，站点 24233 | 发表的晴阴天日数 | 美国联邦作品，公有领域 |
| 《Spaces in New Homes》Table 3 | NAHB，Paul Emrath，2019-03-14，样本 153 家建商 | Great Room 构成 | 事实数据重新录入，报告原文不在本仓库转载 |

## 三条贯穿全部数字的限制

引用任何一个数字时请一并带上。

1. **云观测来自 Sea-Tac 机场气象站。** 该站离 Bellevue、Kirkland、Redmond 约 15 到 25 英里，中间隔着 Lake Washington。结论只对 Sea-Tac 一带严格成立。
2. **一切几何与辐照数字都是上限值。** 它是「这块地朝这个方向能拿到的天花板」，不含树、不含邻居的房子、不含屋檐。真实房子拿到的是这个上限乘以一个遮挡折扣，而那个折扣往往比朝向本身的差距还大。
3. **MLS 的 `Home Faces` 样本过小，本文不做任何价格结论。** 考察的 1,051 笔 Bellevue 成交里，只有 396 笔（37.7%）填了朝向字段。文章把这件事说清楚，然后就停在那里。

另有一条只针对表 A 与表 B：PVGIS-ERA5 是再分析产品，`verify.py` 的 TMY3 交叉核对显示它高报直射。八个朝向是在同一套口径下互相比较的，所以可用的输出是**比值**，不是绝对的 kWh/m² 数值。

## 本仓库刻意不收什么

把没收什么、为什么没收写清楚，本身就是证据的一部分。完整表格见上方英文小节 [What this repository deliberately does not contain](#what-this-repository-deliberately-does-not-contain)。摘要：

- **9 MB 原始观测**：公有领域可以放，但它是派生副本，`fetch.py` 一条命令就能拿到官方当前版本。纯工程理由。
- **`sea.epw` 典型气象年**：第三方分发文件，授权较复杂，改从官方取站号 727930。
- **NAHB 报告 PDF 与整页截图**：第三方版权作品。只把 Table 3 的事实数据重新录入成 CSV，注明出处并给官方链接。事实本身不受版权保护。
- **NWMLS Matrix 截图**：那是 MLS 系统界面，公开发布不在会员授权范围内；而且它一点用都没有，文章已经用文字给出字段名与全部八个取值，RESO Data Dictionary 1.7 的 `DirectionFaces` 任何人都能上官网核对。
- **WRCC 网页原样存档**：页面自带版权声明，改为把 Sea-Tac 那几行重新录入成 CSV，与 NAHB 那张表同一处理。
- **视频里的 `c08` 信息卡**：⛔ 禁用图，它把 NAHB 的 77.2% 与 61.4% 说成了「所有房子」的占比，而原始出处的分母是 Great Room 本身。文章已在正文纠正，该图不在任何地方重新发布。
- **任何客户信息、房源级数据与商业数据**：从来不在范围内。

## 授权

**推荐：代码用 MIT，数据与文档用 CC BY 4.0。理由如下。**

- **代码走 MIT。** 这些脚本是短小的分析工具，它们的价值就在于别人能毫无摩擦地跑起来、改起来。MIT 是摩擦最低的宽松授权，每个脚本头注里写的也是它，与 pvlib 的 BSD-3-Clause 并存也不冲突。这里若用传染性授权，恰好会劝退本仓库最想吸引的那种随手复用。
- **数据与文档走 CC BY 4.0。** 八方位那张表存在的意义就是被别人引用。CC BY 4.0 允许自由引用，同时**要求署名**，而署名正是这里唯一值得要的东西：它让这些数字始终连着出处与限制条件，不至于脱缰漂走。MIT 技术上也能盖住数据，但它是为软件写的，套在一个 CSV 上读起来很别扭，用 Creative Commons 把意图说得更清楚。

⚠ CC BY 4.0 覆盖的是**本项目的汇编与派生值**。底层来自 Iowa State Environmental Mesonet、NOAA / NCEI 与 WRCC 的观测属于公有领域，不带这项条件。

建议的引用格式：

> Ryan Xu（2026）。《Seattle Home Orientation & Sunlight：可复算证据》。https://github.com/ryanlingxiao/seattle-home-orientation-sunlight

## 联系方式

Ryan Xu
Xceed Realty · Bellevue, WA
Washington State 地产经纪执照 **20108301**
<ryan@xceedwa.com> · <https://xceedwa.com/>

欢迎提 issue 与更正。若某个数字复现不出来，请连同你的 Python 与库版本一起开一个 issue。
