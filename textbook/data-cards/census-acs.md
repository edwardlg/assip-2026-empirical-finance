# Data Card — U.S. Census Bureau: ACS + County Business Patterns

**Source slug:** `census-acs` · Appendix C (Data Dictionary) · last touched 2026-05-28

## Provider & what it is

The U.S. Census Bureau is the federal statistical agency that counts who and what lives where. Two of its products do almost all the work in this book. The **American Community Survey (ACS)** is the rolling replacement for the old long-form census: a continuous survey of roughly 3.5 million addresses per year that yields demographic and economic estimates — median household income, educational attainment, race/ethnicity, poverty rate, homeownership, commute, industry of employment — for every geography down to the census-tract and block-group level. **County Business Patterns (CBP)** is a different animal entirely: it is not a survey of households but an annual administrative tabulation of *establishments* (a single physical business location), counting employment, payroll, and number of firms by industry (NAICS) for each county. The trick to keep straight: ACS describes *people where they live*, CBP describes *jobs where they are located*. A shift-share design needs both.

## Coverage

ACS ships in two flavors. The **1-year estimates** cover geographies with population ≥ 65,000 and are released the September after the survey year. The **5-year estimates** pool sixty months of interviews and reach *every* geography, including small tracts and block groups; the cost is that the headline label ("2018–2022 ACS") is a five-year average, not a single year. CBP runs annually from roughly 1986 to the present at the county-by-NAICS level (earlier years use SIC codes). For this camp's purposes treat ACS as 2005–present (the program's modern form) and CBP as 1998–present in NAICS [CHECK exact first NAICS year]. Both are national in scope — all 50 states, DC, and Puerto Rico (with caveats).

## Key identifiers

Everything keys on **FIPS codes** — the Federal Information Processing Standard geographic codes. A 2-digit state FIPS (`51` = Virginia), a 3-digit county FIPS, a 6-digit tract, a 1-digit block-group. Concatenated, a full tract GEOID is 11 digits (`51` + `059` + `452602`). CBP additionally keys on **NAICS** industry codes (2- to 6-digit). The single most common merge bug in this whole appendix is treating FIPS as integers: `01` (Alabama) becomes `1` and silently fails to join. Always read FIPS as strings, zero-padded.

## Access path (API; key via env)

The Census Data API lives at `https://api.census.gov/data`. A request names the dataset, the year, the variables (`get=`), and the geography (`for=` / `in=`). Example, median household income (`B19013_001E`) by county in Virginia:

```python
import os, requests
key = os.environ["CENSUS_API_KEY"]  # never hard-code; see CONVENTIONS §5
url = "https://api.census.gov/data/2022/acs/acs5"
params = {"get": "NAME,B19013_001E", "for": "county:*",
          "in": "state:51", "key": key}
rows = requests.get(url, params=params).json()
# rows[0] is the header; rows[1:] are records
```

CBP swaps the dataset path to `.../2021/cbp` with `get=ESTAB,EMP,PAYANN,NAICS2017`. A key is technically optional under 500 calls/day but you should register one (instant, free) and store it as `CENSUS_API_KEY`. `pandas` can wrap the JSON directly; there is no official Census Python SDK we rely on, though the community `census` package exists.

## License (FREE / public) & note

Census products are **U.S. Government works in the public domain** — free to use, redistribute, and republish, including in a student paper, with attribution. There is no row-level licensing and nothing here touches the GMU-only WRDS constraint from CONVENTIONS §5; ACS/CBP can ship *inside* a replication packet's `data/raw/`. Cite as "U.S. Census Bureau, American Community Survey 5-Year Estimates, table B19013, 2018–2022."

## Gotchas

- **ACS estimates carry margins of error.** Every `...E` (estimate) variable has a matching `...M` (90% margin of error). For a small tract the MOE can be larger than the estimate. Do not treat ACS like a census of truth; it is a *survey*, and the reveal-the-trick lesson is that ignoring the MOE quietly imports measurement error (Ch 2.5) into your regressors.
- **5-year overlap.** Consecutive 5-year files (2017–2021, 2018–2022) share four years of data, so they are *not* independent observations. Never run a panel that treats them as annual.
- **CBP suppression.** To protect individual firms, CBP withholds employment in thin county-industry cells and reports a *flag* (an employment-size class like "100–249") instead of a number. Blindly coercing the flag column to numeric yields NaNs exactly where small industries live — a non-random hole.
- **Boundary changes.** County and tract definitions shift between vintages (Connecticut's 2022 planning-region switch is the famous recent one). Joining a 2010-vintage shapefile to 2022 data drops or duplicates units.
- **Variable codes are not human-readable.** `B19013_001E` is median household income; you must consult the variables endpoint (`.../variables.json`) or you will pull the wrong column with full confidence.

## "First 10 rows" — schema sketch (ILLUSTRATIVE, not real values)

ACS 5-year county pull (`acs/acs5`, VA, median income):

| NAME | B19013_001E | B19013_001M | state | county | GEOID |
|------|------------:|------------:|-------|--------|-------|
| Fairfax County, Virginia | 145165 | 1342 | 51 | 059 | 51059 |
| Arlington County, Virginia | 137980 | 3211 | 51 | 013 | 51013 |
| Loudoun County, Virginia | 170463 | 2890 | 51 | 107 | 51107 |
| Richmond city, Virginia | 60686 | 2104 | 51 | 760 | 51760 |
| Norton city, Virginia | 38500 | 6450 | 51 | 720 | 51720 |

CBP county-by-NAICS pull (`cbp`):

| GEO_ID | NAICS2017 | ESTAB | EMP | PAYANN | EMPFLAG | state | county |
|--------|-----------|------:|----:|-------:|---------|-------|--------|
| 0500000US51059 | 52 (Finance) | 1820 | 38400 | 4120000 | | 51 | 059 |
| 0500000US51059 | 54 (Prof svc) | 6410 | 210300 | 28900000 | | 51 | 059 |
| 0500000US51720 | 52 (Finance) | 4 | 0 | 0 | C (1–19) | 51 | 720 |

(Illustrative magnitudes only; do not cite. `EMPFLAG = C` shows the suppression-flag pattern.)

## Which chapter / lab / capstone uses it

- **Week 4, Ch 4.5 (Bartik / Shift-Share Designs)** and **PS 4.5** — CBP baseline county-by-industry employment *shares* $s_{rk}$ and national industry *shifts* $g_k$ are the literal raw material of the shift-share instrument $B_r=\sum_k s_{rk} g_k$; the data card's suppression and FIPS-string gotchas are exactly the reproducibility traps that bite when building those exposure weights.
- **Fair-lending thread (Week 2 Ch 2.5; Week 4 Lab 4 + Mentor 4; Capstone 1)** — ACS tract demographics and median income are the *neighborhood controls* that HMDA lacks, used to address the omitted-variable threat in Maya's running approval/pricing regressions (the "name the threat" discipline of CONVENTIONS §4).
- **Week 7, Ch 7.2 (Data Acquisition in Practice)** — Census API appears as a worked free-source pull alongside FRED and HMDA.
