# Data · 数据字典与出处

Aggregate tables only. No raw observations, no listing-level data, no personal data.

只放聚合表。不含原始观测、不含房源级数据、不含个人信息。

---

## `eight_orientations_seattle.csv`

The core table of the article. Eight orientations, two different indices.

| Column | Meaning |
|---|---|
| `orientation_code` | `N` `NE` `E` `SE` `S` `SW` `W` `NW` |
| `orientation_en` / `orientation_zh` | Orientation name in English and Chinese |
| `azimuth_deg` | Wall azimuth, degrees clockwise from true north |
| `annual_wall_irradiance_kwh_m2` | Annual irradiance on a vertical surface facing that azimuth, kWh/m² |
| `annual_index_south100` | The above, indexed with south = 100 (article Table A) |
| `evening_wall_irradiance_kwh_m2` | Irradiance in the evening window, kWh/m² |
| `evening_index_west100` | The above, indexed with west = 100, rounded (article Table B) |
| `evening_index_west100_unrounded` | The same index before rounding |
| `tier` | 1 to 5, the article's five-tier ranking. 1 is best |
| `notes` | What the row means and what it does not mean |

**Source.** European Commission PVGIS v5.3, PVGIS-ERA5 reanalysis, 2005 to 2023, 19 years. Vertical surface (`angle=90`), eight azimuths, terrain shading off. <https://re.jrc.ec.europa.eu/pvg_tools/en/>

⚠ **Read the `notes` column before quoting a row.** In particular, north's evening index of 17 slightly exceeding south's 15 does **not** make north the better orientation. It happens because the summer sunset azimuth reaches 305°, swinging behind the house. North's annual total is the lowest of all eight at 24.2.

⚠ **North's absolute evening value is deliberately blank.** It was not archived in the source ledger, and back-deriving it from a rounded index would manufacture a figure that was never measured. The blank is honest; a filled cell would not be.

⚠ **Use the ratios, not the absolute kWh/m².** `verify.py` cross-checks PVGIS-ERA5 against a TMY3 file and finds it overstates direct beam. All eight orientations were queried on one consistent basis, so their relationship to each other survives that bias; the absolute levels do not.

---

## `nahb_2019_table3_great_room_contents.csv`

Which spaces builders fold into a Great Room. Ten space types across three home-size bands.

| Column | Meaning |
|---|---|
| `space_type` | Kitchen Area, Family Area, Breakfast Nook, and so on |
| `share_homes_under_2500sqft_pct` | Share for homes under 2,500 sq ft |
| `share_all_pct` | Share across the full sample |
| `share_homes_3500sqft_plus_pct` | Share for homes of 3,500 sq ft and up |

**Source.** NAHB, *Spaces in New Homes*, Paul Emrath, 2019-03-14, Table 3. Sample of 153 single-family builders. <https://www.nahb.org/-/media/224EC507D1B94735B1BDBC6C39B1E8E6.ashx>

**Why this is re-keyed rather than screenshotted.** The report is a third-party copyrighted work and is not redistributed here. Facts and data are not themselves copyrightable; what is protected is the expression and arrangement. Re-keying takes only the facts, avoids copying the layout, cites the source, links to the original, and has the side benefit of being machine-readable.

🔴 **The denominator matters, and it has been got wrong before.** The 77.2% and 61.4% figures are shares **of Great Rooms**, not of all homes. The correct phrasing is: among new homes that have a Great Room, 77.2% of those Great Rooms include a kitchen area and 61.4% include a breakfast nook. ⛔ The two figures must never be multiplied together.

⚠ **An inconsistency inside the NAHB report itself, noted for anyone citing it.** The body text repeatedly says "less than 2,500 square feet" while footnote 3 says "The cut-offs at 2,000 and 3,500 square feet". This CSV names its columns after the body-text wording. The inconsistency does not affect the 77.2% and 61.4% figures used in the article, which are full-sample values and not broken out by size band.

---

## `wrcc_ksea_reference_values.csv`

Reference values used to calibrate the cloud-derived estimates, for the Seattle-Tacoma AP station.

| Column | Meaning |
|---|---|
| `station` | `SEATTLE-TACOMA AP` |
| `measure` | `percent_of_possible_sunshine_pct`, `mean_clear_days`, `mean_cloudy_days` |
| `jan` through `dec`, `annual` | Monthly and annual values |

**Source.** Western Regional Climate Center comparative tables, derived from NCDC / NOAA observations. <https://wrcc.dri.edu/Climate/comp_table_show.php?stype=sun_mean_pct>

**Article figures that come from here.** Measured percent of possible sunshine, 23% in December and 47% for the year. Clear days 58 and cloudy days 226 annually.

**Why the WRCC pages themselves are not archived here.** The saved pages carry their own copyright notice and are full HTML documents covering every US station. The same treatment applied to the NAHB table was applied here: take the facts for the one station in question, cite the source, link to the original. `verify.py` and `verify2.py` carry these same values inline as comparison baselines, so no script reads this file; it exists so a reader can see where those inline values came from.

---

## `t1_wet.csv` and `t3_summer.csv`

Cloud cover by hour of day, produced by `scripts/t1.py`.

Rows are local hour 0 through 23. Columns are the share of observations at each cover grade, in percent, plus two rollups and a count.

| Column | Meaning |
|---|---|
| `CLR` `FEW` `SCT` `BKN` `OVC` `VV` | Share of observations at that cover grade, percent |
| `BKN+OVC` | Broken plus overcast |
| `BKN+OVC+VV` | The above plus vertical visibility, the article's "fully clouded" measure |
| `N` | Number of observations in that hour across the 21 years |

`t1_wet.csv` covers November through March. `t3_summer.csv` covers June through August.

---

## `t2_month_hour_nosun.csv` and `t2_month_hour_ovc.csv`

Month by local hour matrices, produced by `scripts/t2.py`. Rows are local hour, columns are the eight months of interest, values are percentages.

`t2_month_hour_nosun.csv` reports `BKN+OVC+VV`. `t2_month_hour_ovc.csv` reports `OVC+VV` only.

---

## Provenance for all four generated tables

All four come from the same base: hourly ASOS / METAR observations for station KSEA (47.4444 N / 122.3139 W), 2005-01-01 to 2025-12-30, `report_type=3`, retrieved from the Iowa State University Environmental Mesonet. 183,690 rows downloaded, 183,674 usable after cleaning.

**These four are reproducible byte for byte.** Run `fetch.py`, then `analyze.py`, then `t1.py` and `t2.py`, and the files written into `scripts/` should be identical to the copies here. That comparison was verified on 2026-09-03.

**Rights.** The Iowa Environmental Mesonet states its material is in the public domain and may be used freely by anyone for any lawful purpose, with attribution appreciated but not required. The underlying NOAA / NWS observations are United States federal government works and are likewise in the public domain.
