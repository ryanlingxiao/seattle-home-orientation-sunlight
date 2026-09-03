# Sources · 数据出处

Every institution, year, table number and official URL behind the article's figures.

文章里每个数字的机构、年份、表号与官方链接。

⚠ **Links rot; the figures do not.** If a URL below stops resolving, the institution, year, table number and sample size are still recorded here, which is what makes a figure traceable.
⚠ **链接会随机构改版失效，但失效不等于数字失效。** 上面那几样才是可追溯性的根。

---

## Screenshots in this directory

Three source-page captures, kept as evidence that these data sources were actually consulted rather than cited from memory.

| File | What it shows | Rights |
|---|---|---|
| `noaa_ncei_lcd_ksea.png` | NOAA / NCEI Local Climatological Data access page for KSEA | US federal government work, public domain |
| `noaa_ncei_lcd_product_page.png` | The same product's description page | US federal government work, public domain |
| `pvlib_solarposition_docs.png` | pvlib official documentation for the solar position algorithm | pvlib is BSD-3-Clause |

⛔ **Not included, and why.** A screenshot of the NWMLS Matrix search form was captured during research and is deliberately withheld. It contains no listing record, no address, no price, no MLS number and no personal data, but it depicts the MLS system interface, and republishing that interface is outside the scope of member authorization. It would also add nothing: the article states the field name and all eight of its values in text, and RESO Data Dictionary 1.7's `DirectionFaces` enumeration is publicly checkable by anyone.

---

## Primary sources, with what each one supports

| Source | Institution · year · scope | Used for | Official URL |
|---|---|---|---|
| ASOS / METAR archive | Iowa State University Environmental Mesonet, station KSEA, 2005-01-01 to 2025-12-30, `report_type=3`, 183,690 rows | Every cloud-cover conclusion: wet-season 79% to 86%, `CLR` 2%, the 09:00 peak of 85.6%, the 14:00 drop of 3.51 points, the 66.6% conditional, the 3.06 to 4.27 point morning-afternoon gap, precipitation shares, visibility, June gloom | <https://mesonet.agron.iastate.edu/request/download.phtml> |
| PVGIS v5.3 | European Commission Joint Research Centre, PVGIS-ERA5 reanalysis, 2005 to 2023, 19 years; vertical surface, eight azimuths, terrain off | Table A annual index, Table B evening index, southwest at 95.6%, west at 74.5%, the 4.7x evening ratio, the three eastern orientations at 16.79 kWh/m² | <https://re.jrc.ec.europa.eu/pvg_tools/en/> |
| pvlib, NREL SPA algorithm | Minute-by-minute, 47.61 N / 122.33 W | Solstice noon altitudes of 65.8° and 19.0°, 7 h 01 m and 44.1%, azimuth tables, sunset times, indoor depth, north-wall recomputation | <https://pvlib-python.readthedocs.io/> |
| Comparative Climatic Data | NOAA / NCEI, station 24233, 51-year record, data through 2023 | Annual clear 58, partly cloudy 82, cloudy 226 days; December clear 2 and cloudy 25 | <https://www.ncei.noaa.gov/sites/default/files/2024-11/clpcdy23.txt> |
| Percent of possible sunshine | NOAA / NCEI, station 24233. ⚠ Period of record 1965-03 to 1983-12, the instrument has been retired | December 20%, July 64%, annual 45%. ⚠ Must be cited with its period of record | <https://www.ncei.noaa.gov/sites/default/files/2024-11/pctpos23.txt> |
| Measured percent of possible sunshine | Western Regional Climate Center, Sea-Tac, sunshine recorder | December 23%, annual 47% | <https://wrcc.dri.edu/Climate/comp_table_show.php?stype=sun_mean_pct> |
| *Spaces in New Homes*, Table 3 | NAHB, Paul Emrath, 2019-03-14, 153 single-family builders | Great Rooms containing a kitchen area 77.2%, a breakfast nook 61.4% | <https://www.nahb.org/-/media/224EC507D1B94735B1BDBC6C39B1E8E6.ashx> |
| Overhang parameters | NREL/TP-463-7904, 1995, Seattle station WBAN 24233 | Projection 0.749, PF 0.565, 45 inches | <https://docs.nrel.gov/docs/legosti/old/7904.pdf> |
| Ceiling height history | Wharton Working Paper #678, Rybczynski, 2009. ⚠ A narrative paper, cited for history, not used as data | Where the 8 ft ceiling came from | <https://realestate.wharton.upenn.edu/wp-content/uploads/2017/03/678.pdf> |
| RECS 2020 state air conditioning | US EIA, 2020 cycle, final release 2023-03, state level | Washington 53%, national 89% | <https://www.eia.gov/consumption/residential/data/2020/state/pdf/State%20Air%20Conditioning.pdf> |
| Washington State Energy Code, 2006 edition | Washington State Building Code Council, Section 602.7.1 and Table 6-1 | The 2006 Option I glazing area cap of 10% | <https://sbcc.wa.gov/sites/default/files/2019-12/WSEC06.pdf> |
| Window head height and daylight depth | Reinhart 2005, IBPSA Montreal, Radiance simulation | Glazing below the work plane contributes nothing to daylight | <https://publications.ibpsa.org/proceedings/bs/2005/papers/bs2005_1011_1018.pdf> |
| Sunrise and sunset times | US Naval Observatory | Solstice sunrise and sunset, used as an independent check on the pvlib output | <https://aa.usno.navy.mil/data/RS_OneYear> |
| MLS orientation field | RESO Data Dictionary 1.7, `DirectionFaces` enumeration | Confirms the eight-value orientation enumeration is an industry standard anyone can verify | <https://ddwiki.reso.org/> |

---

## Evidence grading used throughout the article

| Grade | Meaning |
|---|---|
| **A** | A published figure from a named institution, quoted as published |
| **B** | Computed by this project from published inputs, with the method stated and the code available here |
| **C** | Experience-based judgment with no supporting data. The article labels these explicitly wherever they appear |

Everything reproducible from this repository is grade B, built on grade A inputs. No grade C claim depends on anything in this repository.

---

## Sources cited in the article but not reproducible here

These are published figures quoted as published. They need no script, and none is provided: NAHB *What Home Buyers Really Want* (Rose Quint, 2021-03); NEEA Residential Building Stock Assessment window-to-floor ratios (Ecotope 2012, Cadmus 2016-17, 2,487 homes across ID, MT, OR and WA); Do et al. 2025 in *Scientific Reports* 15:39507 (⚠ modelled at Hanoi, 21 N, so the magnitude comparison transfers but the absolute values do not); Reinhart 2006 in *LEUKOS* 3(1); DOE Building America Measure Guideline 2012; NOAA / NCEI and Washington State Department of Health reporting on the 2021 heat dome; BLS American Time Use Survey 2025; EPA *Exposure Factors Handbook* 2011 Table 16-15; Mitra et al. 2020 in *Energy and Buildings* 210:109713; Oregon State University Extension EM 9175 and EC 1521; City of Seattle Trees for Neighborhoods, USDA Forest Service Silvics and FEIS, NC State Extension, WSU EB0440.
