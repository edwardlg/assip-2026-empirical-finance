# Data Card — NOAA Billion-Dollar Disasters / Storm Events + FEMA Disaster Declarations

**Provider & what it is.** Two U.S. federal sources that together let you measure *where and when a climate or weather shock hit*, at the county level. **NOAA** (National Oceanic and Atmospheric Administration) publishes two things you will use. First, the **Billion-Dollar Weather and Climate Disasters** product (from NOAA NCEI): a curated list of U.S. events whose total damages exceeded \$1 billion (CPI-adjusted), with a type (hurricane, wildfire, drought, severe storm, flooding, winter storm), a date range, a cost estimate, and the states affected. Second, the **Storm Events Database**: a far more granular record of individual storm episodes and events — tornadoes, hail, flash floods, heat — with county FIPS codes, begin/end timestamps, and (often) property/crop damage estimates. **FEMA** (Federal Emergency Management Agency) publishes, through its **OpenFEMA** program, the **Disaster Declarations Summaries**: every presidentially declared disaster (major disaster "DR", emergency "EM", fire-management "FM") since 1953, with the declaration date, incident type, and the *list of declared counties*. The reveal: NOAA tells you what the weather did; FEMA tells you when the government officially recognized it as a disaster for a specific place — and that official, dated, place-specific declaration is exactly the kind of clean treatment switch a difference-in-differences design needs.

**Coverage.** Billion-Dollar Disasters: U.S., 1980–present, updated quarterly, event-level (a few hundred events). Storm Events: U.S., 1950–present (completeness and the set of recorded event types improve over time), county-level, millions of rows. FEMA Disaster Declarations: U.S. states, territories, and tribal nations, 1953–present, declaration-by-county. All three are updated on a rolling basis, so a re-pull next year will have more recent rows — pin your snapshot.

**Key identifiers.** The linking key across these and to almost every other U.S. dataset (HMDA, Census, BEA) is the **county FIPS code** — a 5-digit string: 2-digit state + 3-digit county (e.g., `06037` = Los Angeles County, CA). Keep it as a *zero-padded string*, never an integer (leading zeros vanish and `06037` becomes `6037`). FEMA also has its own `disasterNumber` (a unique integer per declaration) and `femaDeclarationString`. NOAA Storm Events uses `EVENT_ID`/`EPISODE_ID`. Billion-Dollar events carry an event name/ID and a state list rather than counties, so you often map them to counties via the storm or declaration data.

**Access path.** All free, no license fee. FEMA OpenFEMA is a clean REST/JSON API — no key required:

```python
import os, requests
# OpenFEMA: presidentially declared disasters, JSON, no key needed
url = "https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries"
params = {"$filter": "fyDeclared eq 2023", "$top": 1000, "$format": "json"}
resp = requests.get(url, params=params, timeout=60)
declarations = resp.json()["DisasterDeclarationsSummaries"]
```

NOAA NCEI distributes Storm Events as yearly bulk CSV files (`https://www.ncei.noaa.gov/.../StormEvents_details-...csv.gz`) you download and concatenate; Billion-Dollar Disasters has a downloadable table and a JSON time-series endpoint. The NCEI **Climate Data Online (CDO)** API (for weather *observations*, not the disaster lists) does require a token, which — like every credential in this book — comes from the environment, never the code:

```python
token = os.environ["NOAA_CDO_TOKEN"]   # set in your shell / .env, never hard-coded
headers = {"token": token}
```

**License & note.** U.S. federal government works are generally in the **public domain** (not copyrighted), so you may cache, redistribute, and commit these freely — a welcome contrast to the licensed WRDS data that must stay on GMU infrastructure. Cite the *originating agency* (NOAA NCEI; FEMA), not a re-host, per CONVENTIONS §6. NOAA asks that the Billion-Dollar product be cited as Smith (NOAA NCEI) with the access date `[CHECK]` exact citation form.

**Gotchas.**
- **FIPS as string, always.** The single most common bug. Also: a handful of FIPS codes change over time (county splits/renames, e.g. parts of Alaska, Shannon County SD → Oglala Lakota `46102`); pin a crosswalk year.
- **Declaration ≠ damage.** A FEMA declaration is a *political/administrative* event, correlated with damage but also with whether a governor requested aid and how the request was processed. If your treatment is "got a declaration," name that the declaration — not the storm — is what you are actually using, and consider it a *proxy* for the shock (a measurement-error issue, Ch 1.3).
- **A disaster spans many counties and dates.** One `disasterNumber` expands to many county rows; one Billion-Dollar event spans multiple states. Decide your unit (county-year? county-event?) before merging or you will double-count.
- **Storm Events completeness drifts.** Older years record fewer event types; a rising count of "events" over time is partly better recording, not just worse weather. Do not read a raw time trend as climate signal.
- **Damage fields are sparse and unit-inconsistent** (`"5.00K"`, `"2.50M"` as strings). Parse carefully; many rows are blank.

**First 10 rows — schema sketch (illustrative; values invented, not real records).**

| disasterNumber | state | fipsStateCode | fipsCountyCode | fips5 | incidentType | declarationType | declarationDate | incidentBeginDate | designatedArea |
|---|---|---|---|---|---|---|---|---|---|
| 4610 | CA | 06 | 037 | 06037 | Fire | DR | 2023-08-14 | 2023-08-01 | Los Angeles (County) |
| 4610 | CA | 06 | 071 | 06071 | Fire | DR | 2023-08-14 | 2023-08-01 | San Bernardino (County) |
| 4611 | FL | 12 | 086 | 12086 | Hurricane | DR | 2023-09-30 | 2023-09-26 | Miami-Dade (County) |
| 4611 | FL | 12 | 011 | 12011 | Hurricane | DR | 2023-09-30 | 2023-09-26 | Broward (County) |
| 4612 | TX | 48 | 201 | 48201 | Severe Storm | DR | 2023-05-22 | 2023-05-18 | Harris (County) |
| 4613 | LA | 22 | 071 | 22071 | Flood | DR | 2023-06-04 | 2023-05-29 | Orleans (Parish) |
| 4614 | NC | 37 | 119 | 37119 | Hurricane | EM | 2023-09-12 | 2023-09-10 | Mecklenburg (County) |
| 4615 | CO | 08 | 031 | 08031 | Winter Storm | DR | 2023-12-20 | 2023-12-15 | Denver (County) |
| 4616 | NY | 36 | 061 | 36061 | Flood | EM | 2023-07-10 | 2023-07-09 | New York (County) |
| 4617 | OK | 40 | 109 | 40109 | Tornado | DR | 2023-04-26 | 2023-04-19 | Oklahoma (County) |

**Which chapter/lab/capstone uses it.** This is **Priya's** data. The pairing drives her running example through **Week 4** (Ch 4.1 difference-in-differences, Ch 4.2 staggered adoption, Ch 4.4 synthetic control) and the **Week 7** project workshop: in Ch 7.1 her worked example asks *"do counties hit by federally declared disasters see homeowner-insurance costs rise faster than comparable un-hit counties?"* — a county-year **DiD** with treated = counties with a FEMA declaration, control = comparable un-hit counties, county and year fixed effects, clustering by county (the spec in Ch 7.1 §worked-example-B). You acquire it in **Ch 7.2** (Data Acquisition in Practice) and document it in your **Lab 7** data card; it is a natural spine for a climate-insurance **capstone** in the spirit of the Capstone Gallery. Pair it with FRED (insurance-cost proxy) and, if you have it, Compustat insurer fundamentals on WRDS.
