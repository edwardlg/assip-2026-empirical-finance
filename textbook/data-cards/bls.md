# Data Card — U.S. Bureau of Labor Statistics (BLS)

**Source slug:** `bls` · Appendix C (Data Dictionary) · last touched 2026-05-28

## Provider & what it is

The Bureau of Labor Statistics is the Department of Labor's statistical agency, and it is the official scorekeeper for two things every macro story needs: **prices** and **jobs**. The four products this book leans on are the **Consumer Price Index (CPI)** — the inflation number you read in the headlines, the price of a fixed basket of goods a typical urban household buys; the **Producer Price Index (PPI)** — the prices producers *receive* at the factory gate, an earlier-in-the-pipeline cousin of CPI; the **Current Employment Statistics (CES)**, a monthly survey of ~120,000 businesses that produces nonfarm payroll employment, hours, and earnings (the "jobs report"); and the **unemployment rate** from the Current Population Survey / Local Area Unemployment Statistics. The reveal-the-trick framing for the whole agency: BLS does not publish "the inflation rate," it publishes an *index level*, and inflation is something *you* compute from two index levels. Confusing the level with the growth rate is the single most common beginner error here.

## Coverage

CPI runs monthly from 1913 (the all-items U.S. city average series is among the longest economic time series the government keeps). PPI's modern commodity and industry series run monthly from the 1970s–1980s depending on the series. CES nonfarm payrolls run monthly from 1939. Unemployment from the CPS runs monthly from 1948. Geography ranges from a single national number to metro-area and (for LAUS) state and county series. Frequency is overwhelmingly monthly, occasionally annual.

## Key identifiers

Everything is a **series ID** — a single packed string that encodes the survey, seasonal-adjustment flag, area, item, and base. `CUUR0000SA0` is CPI-U (`CU`), not seasonally adjusted (`UR`), U.S. city average (`0000`), all items (`SA0`). `CES0000000001` is total nonfarm employment, seasonally adjusted. `LNS14000000` is the headline unemployment rate. The trick is that the *structure* of the ID is the metadata: a survey-specific code book maps each character block. Get one character wrong and you silently pull a different series (seasonally adjusted vs. not is the classic foot-gun — `CUUR` vs `CUSR`).

## Access path (API; key via env)

The BLS Public Data API v2 lives at `https://api.bls.gov/publicAPI/v2/timeseries/data/`. It is a *POST* of JSON, not a GET of query params — a frequent stumble. Register a free API key for v2 (higher limits: 500 queries/day, 50 series and 20 years per query, vs. v1's stingier unregistered tier).

```python
import os, requests
key = os.environ["BLS_API_KEY"]  # env only; CONVENTIONS §5
payload = {"seriesid": ["CUUR0000SA0", "CES0000000001"],
           "startyear": "2015", "endyear": "2024",
           "registrationkey": key}
r = requests.post("https://api.bls.gov/publicAPI/v2/timeseries/data/",
                  json=payload).json()
# r["Results"]["series"][i]["data"] is a list of period records
```

For quick exploration, `pandas_datareader` exposes BLS-adjacent data through FRED (FRED re-publishes most major BLS series under tidy mnemonics like `CPIAUCSL`), which is often the path of least resistance for a student notebook. Bulk flat files are also posted at `https://download.bls.gov/pub/time.series/`.

## License (FREE / public) & note

BLS data are **U.S. Government works, public domain** — free to download, redistribute, and republish with attribution; no row-level license, no GMU-only constraint. They can live in a replication packet's `data/raw/`. Cite as "U.S. Bureau of Labor Statistics, CPI-U, series CUUR0000SA0, retrieved [date]." Note the **terms-of-service courtesy**: BLS asks that you not hammer the API and that you cache rather than re-pull, which is also good reproducibility hygiene (pin a snapshot date).

## Gotchas

- **Index level vs. inflation rate.** CPI returns a level (e.g., 314.5). Inflation is $(P_t/P_{t-12}-1)$ for year-over-year. Students routinely regress on the *level* and discover a spurious trend.
- **Seasonal adjustment.** Many series exist in both SA and NSA forms with nearly identical IDs. Mixing them in one regression injects a seasonal cycle into your residuals. Pick one and label it.
- **Revisions.** CES payrolls are revised for two months after first release and re-benchmarked annually. The number you pulled last month is not the number in the API today. This is a *vintage* problem: for any forecasting or event-study exercise you must record which vintage you used, or you are quietly using information that did not exist on the event date (a look-ahead bias).
- **Rebasing.** Index series have a reference base (1982–84 = 100 for CPI). Splicing across a rebasing without converting breaks the level.
- **POST not GET, and rate limits.** The v2 API rejects GETs to the data endpoint, and unregistered callers hit a hard daily cap fast. Register the key.
- **Discontinued / renamed series.** Series get retired; a dead `seriesid` returns an empty result, not an error, so a typo and a discontinued series look identical.

## "First 10 rows" — schema sketch (ILLUSTRATIVE, not real values)

CPI-U all-items (`CUUR0000SA0`), monthly level, as returned and flattened:

| seriesID | year | period | periodName | value | footnotes |
|----------|------|--------|------------|------:|-----------|
| CUUR0000SA0 | 2024 | M01 | January | 308.417 | |
| CUUR0000SA0 | 2024 | M02 | February | 310.326 | |
| CUUR0000SA0 | 2024 | M03 | March | 312.332 | |
| CUUR0000SA0 | 2024 | M04 | April | 313.548 | |
| CES0000000001 | 2024 | M01 | January | 157200 | P (preliminary) |
| CES0000000001 | 2024 | M02 | February | 157450 | P |
| LNS14000000 | 2024 | M01 | January | 3.7 | |
| LNS14000000 | 2024 | M02 | February | 3.9 | |
| WPUFD4 (PPI final demand) | 2024 | M01 | January | 143.2 | |
| WPUFD4 | 2024 | M02 | February | 143.5 | |

(Illustrative magnitudes only; do not cite. `period = M13` would be an annual average; the `P` footnote shows the preliminary/revision flag.)

## Which chapter / lab / capstone uses it

- **Capstone 5 — FRED Macro Event Study** — CPI/CES/unemployment surprises (the gap between the announced number and the consensus forecast) are the canonical macro-announcement events; the *vintage/revision* gotcha above is precisely the look-ahead trap the capstone must avoid, and BLS releases come through the FRED pipeline that capstone already uses.
- **Week 4 macro/shift-share controls** — national industry employment growth (CES by NAICS / supersector) supplies the "shifts" $g_k$ that pair with Census/CBP "shares," and CPI is the standard real-vs-nominal deflator for any dollar outcome.
- **Week 7, Ch 7.2 (Data Acquisition in Practice)** — BLS API (and its FRED mirror) appears as a worked free-source pull with rate-limit and POST-vs-GET discussion.
