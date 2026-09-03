# Scripts · 方法说明

Every script carries a header stating what it computes, its data source, its dependencies, how to run it and what it outputs. This file is the overview.

每个脚本顶部都有头注，写明算什么、数据源、依赖、怎么跑、输出什么。本文件是总览。

Verified on 2026-09-03: Python 3.12.10, pvlib 0.15.2, pandas 3.0.5, numpy 2.4.6, scipy 1.17.1.

---

## Group A · Solar geometry, no external data

Install dependencies and run. Nothing to download. Each script evaluates solar position minute by minute, so expect 30 to 120 seconds each.

### `solar_position_summary.py`

**Computes.** Sunrise and sunset azimuth and clock time at both solstices; day length; solar noon altitude; how long the sun sits in the northern half of the compass; and, for the first and fifteenth of each month from April through September, the moment the sun crosses due south and the moment it sets.

**Inputs.** None. Location is hard-coded at 47.61 N / 122.33 W, 72 m, `America/Los_Angeles`.

**Outputs.** Printed to stdout.

**Expected figures.** Summer solstice daylight 15 h 55 m; northern half 7 h 01 m = 44.1%; solstice noon 65.8°; winter solstice noon 19.0° and daylight 8 h 22 m; due south crossing between 13:05 and 13:16; earliest sunset 19:18, latest 21:08.

🔴 **Corrected defect, worth reading.** The original version of this script (named `_calc.py`) closed with `min(r[2] for r in rows)`, comparing full timezone-aware timestamps. That compares *which day*, not *what time of day*, so 04-01 with its 19:38 sunset was reported as the "earliest sunset" and the output claimed an earliest later than the latest. The comparison now runs on clock time, and four lines of comment at the bottom of the file record what changed and why. ⚠ Because the sampling grid takes only the first and fifteenth of each month, the latest sunset lands on the sampled 07-01; the true annual peak falls in late June.

### `sun_depth_eight_orientations.py`

**Computes.** How far direct sunlight penetrates horizontally into a room, for all eight wall orientations, in two time windows: evenings from April through September 17:00 to 19:00, and midday around the summer solstice.

**Method.** Depth equals window head height multiplied by the median of `cos(azimuth difference) / tan(solar elevation)`, counting only the minutes when the sun actually strikes that wall.

**Key parameter.** `HEAD`, the window head height in feet. `7.0` corresponds to an 8 ft ceiling, `9.0` to a 10 ft ceiling. Change this one line to reproduce the article's second pair of figures.

**Expected figures.** South evening 1.9 ft, southwest evening 11.4 ft, south at summer noon 3.1 ft. With `HEAD = 9.0`, south noon becomes 4.0 and southwest evening 14.6, matching the article's 4.04 and 14.58 at the script's one-decimal print precision.

### `verify_north_evening.py`

**Computes.** An independent check, using pvlib rather than PVGIS, of the article's most counterintuitive claim: that on April through September evenings a north wall receives more direct beam than a south wall. Reports lit minutes and clear-sky beam energy per wall, breaks the result down month by month, and reports the evening azimuth range.

**Method.** Identical location and time base to `sun_depth_eight_orientations.py`. Wall incidence uses `cos(incidence) = cos(elevation) * cos(azimuth difference)`; clear-sky DNI comes from pvlib's Ineichen model. Energy figures are for **relative comparison only**, not absolute yield.

**Expected figures.** North 18,298 lit minutes against south 13,197 in the 17:00 to 20:00 window, a 1.39x ratio on minutes and 1.07x on clear-sky beam energy. The month-by-month breakdown shows the advantage concentrated in May, June and July, and reversing in April, August and September.

⚠ **What this does and does not establish.** A north wall beating a south wall on these two measures, in this window, in high summer, does **not** make north a better orientation. North's annual total is the lowest of all eight at 24.2 against south's 100, and roughly 181 days from equinox to equinox receive no direct beam at all. The script exists to show the summer evening geometry is real, not to reverse the ranking.

---

## Group B · Cloud observations, 21 years at KSEA

Run in order. `fetch.py` first, then `analyze.py`, then any of the rest.

### `fetch.py`

**Does.** Downloads hourly ASOS / METAR cloud layers, visibility and weather codes for station KSEA from the Iowa State University Environmental Mesonet, covering 2005-01-01 through 2025-12-31, with `report_type=3` (the routine hourly aviation observation).

**Dependencies.** Standard library only. No API key; the endpoint is public.

**Output.** `sea_asos.csv`, about 9 MB, 183,690 rows.

**Why the raw file is not committed.** It is public domain and freely redistributable, so this is purely an engineering choice: a frozen 9 MB mirror is worse evidence than a command that fetches the current official version. The parameters that matter, station, date range and report type, are hard-coded here and are the thing actually worth archiving.

### `analyze.py`

**Does.** Folds each observation's four cloud layers into a single cover grade, `CLR < FEW < SCT < BKN < OVC < VV`, by taking the densest layer. Rounds METAR's HH:53 observation onto the HH+1 hour, which is the aviation convention.

**Output.** `clean.pkl`, read by every script below.

**Expected figures.** 183,674 usable observations across 2005 to 2025.

### `t1.py`

Wet season (November through March) and summer (June through August) cloud cover by hour of day. Writes `t1_wet.csv` and `t3_summer.csv`.

**Expected figures.** Wet-season daylight hours run 79% to 86% at `BKN+OVC+VV`, peaking at 85.6% at 09:00. `CLR` sits near 2% through the middle of the day.

### `t2.py`

Month by local hour matrices, and the morning (09-13) against afternoon (14-18) split. Writes `t2_month_hour_nosun.csv` and `t2_month_hour_ovc.csv`.

**Expected figures.** Wet-season morning exceeds afternoon by 4.27 percentage points. In summer, overcast falls 15.05 points from morning to afternoon, which is the June gloom effect.

### `t4.py`

Hour-over-hour change, wet-season precipitation by hour, visibility by hour, and the conditional question: given a wet-season day already overcast at 10:00, what does it do later.

**Expected figures.** The sharpest single-hour overcast drop is 3.51 points at 14:00. Of 3,091 wet-season days with complete observations, 1,636 are overcast at 10:00, and 66.6% of those are still overcast at 14:00. Precipitation occupies 18.62% of morning hours against 20.34% of afternoon hours. Visibility bottoms at 8.30 statute miles and peaks at 9.23.

### `t5.py`

Recomputes the morning-afternoon gap after discarding hours when the sun sits below 5° of elevation, which removes the winter twilight hours that inflate the raw comparison. Also back-derives an implied "sun disk visible" share as a sanity check against the PVGIS-ERA5 figures.

**Expected figures.** The gap narrows from 4.27 to 3.06 points. `CLR/FEW` runs 8.52% in the morning against 7.96% in the afternoon. The implied sun-disk share comes out near 24%, well under the 63% a prior PVGIS-ERA5 round had suggested, which is how the reanalysis product's direct-beam overstatement was caught.

### `t6.py`

Rebuilds NOAA's clear-day and cloudy-day counts for December from raw ASOS observations, as an independent check on the published values. Also reports ceilometer height coverage.

**Expected figures.** 644 complete December daylight days across the record. Cloudy 83.7%, about 25.9 of 31 days, against NOAA's published 25. Clear 5.7%, about 1.8 days, against NOAA's 2.

🔴 **Corrected defect.** The original version read the cloud grade as `dec.cov` and `g.cov`. Attribute access there resolves to `DataFrame.cov()`, the covariance method, not to the column named `cov`, so the script raised `TypeError` partway through on any pandas version. It now uses `dec["cov"]` and `g["cov"]`, matching how `t7.py` already wrote the same line. Only the column access changed; no logic and no output definition was touched.

### `t7.py`

Wet-season "scattered or better" share by hour, that is the share of observations at `SCT` or clearer, which approximates hours when the sun is likely usable.

### `verify.py`

Calibration pass. Compares the cloud-derived sun-visibility estimate month by month against WRCC's measured percent of possible sunshine, then runs an independent irradiance check against a TMY3 file.

⚠ **Needs `sea.epw`, which is not bundled.** Download station **727930** from the EnergyPlus weather archive or NREL NSRDB and place it in this directory. Without it, the first half of the script still runs and the second half raises `FileNotFoundError`.

**Expected figures.** The WRCC reference row, 23% in December and 47% annually, is in `../data/wrcc_ksea_reference_values.csv`. The TMY3 check reports wet-season midday direct beam above 120 W/m² for roughly 42% of hours, against the 63% a prior PVGIS-ERA5 round had claimed.

### `verify2.py`

Rebuilds clear-day and cloudy-day counts for all twelve months using WRCC's own definition, mean daytime sky cover in tenths, with clear at 0 to 3 and cloudy at 8 to 10, then compares month by month against WRCC's published values.

**Expected result.** Monthly differences run within about 3 days, with the ASOS reconstruction consistently a little lower. The annual cloudy total comes out near 204 against WRCC's 225. That systematic gap is expected: the definitions are close but not identical, and the two records cover different periods. The purpose is to confirm the shape agrees, not to match exactly.

---

## Run order

```
fetch.py  →  analyze.py  →  t1 t2 t4 t5 t6 t7 verify2      (verify.py also needs sea.epw)

solar_position_summary.py            standalone
sun_depth_eight_orientations.py      standalone
verify_north_evening.py              standalone
```

## A note on the two corrected scripts

Two of the thirteen scripts carried defects that would have produced wrong or crashing output for anyone who ran them. Both are documented in place, in the file header and beside the changed line, rather than quietly fixed. `solar_position_summary.py` would have printed an earliest sunset later than its latest; `t6.py` would have stopped with a `TypeError` two thirds of the way through. Publishing code that does not run, in a repository whose entire purpose is "check it yourself", would have turned the strongest claim into the weakest one.
