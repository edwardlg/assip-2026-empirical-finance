# Data Card — FRED (Federal Reserve Economic Data)

## Provider & what it is

FRED is the **Federal Reserve Bank of St. Louis**' free public database of economic time series.
Here is the trick to using it well: FRED is mostly an *aggregator*, not the original source. It
gathers series that other agencies actually produce — the unemployment rate from the **Bureau of
Labor Statistics (BLS)**, GDP from the **Bureau of Economic Analysis (BEA)**, Treasury yields from
the U.S. Treasury, mortgage rates from Freddie Mac — and re-publishes them under one clean, stable
API with one consistent date index. That convenience is exactly why CONVENTIONS §6 makes you cite
the *underlying* agency, not just "FRED": FRED is the delivery truck, BLS/BEA is the factory. What
you get per series is a tidy two-column table — a date and a value — at the series' native
frequency, plus rich metadata (units, seasonal adjustment, frequency, the source). FRED also has a
sibling, **ALFRED** (ArchivaL FRED), which serves *vintages*: the value of a series *as it was
reported on a past date*, before later revisions. ALFRED is the difference between a reproducible
point-in-time study and an accidental look-ahead.

## Coverage

Hundreds of thousands of U.S. and international macro/financial series. Frequencies range from
**daily** (e.g. Treasury constant-maturity yields, `DGS10`) through **weekly** (e.g. the 30-year
mortgage rate, `MORTGAGE30US`) to **monthly** (e.g. the unemployment rate, `UNRATE`; CPI) and
**quarterly/annual** (e.g. GDP, `GDP`). History depth is per series — some monthly series reach
back to the 1940s–50s; many newer indicators start far later. Each series page states its own span,
units, and seasonal-adjustment status; read it rather than assuming.

## Key identifiers

The one identifier you need is the **series ID** — a short uppercase string such as `UNRATE`,
`MORTGAGE30US`, `DGS10`, `CPIAUCSL`, or `GDP`. It is the primary key you query on and the thing you
record in your code and log. There is no cross-record join inside a single series (it is just a time
series); the *crosswalk that bites* is the one to another dataset — e.g. lining FRED's monthly index
up to a daily price panel, or merging a county-level FRED series to NOAA/FEMA county codes. That
alignment (frequency conversion, date joins) is a Chapter 7.4 task and out of scope for this card.

## Access path (Python; key via env)

Two clean paths. The lightweight one needs **no key**; the fuller one needs a **free** API key,
read from the environment (never hard-coded — CONVENTIONS §5):

```python
# Path A — pandas-datareader, no API key required.
import pandas_datareader.data as web
unrate = web.DataReader("UNRATE", "fred", start="2000-01-01", end="2026-05-15")

# Path B — fredapi, free key from the environment.
import os
from fredapi import Fred
fred = Fred(api_key=os.environ["FRED_API_KEY"])   # export FRED_API_KEY=... in your shell
mortgage = fred.get_series("MORTGAGE30US", observation_start="2000-01-01")

# Point-in-time / reproducible: pull a VINTAGE via ALFRED, not the latest value.
gdp_vintage = fred.get_series("GDP", realtime_start="2026-05-15", realtime_end="2026-05-15")
```

Get the free key from the St. Louis Fed's API page; set it once with `export FRED_API_KEY=...` (or a
git-ignored `.env`). If `os.environ["FRED_API_KEY"]` raises `KeyError`, that is the system refusing
to run until you supply the key out-of-band — exactly the behavior you want.

## License & GMU-infra note (§5)

**Free and public** — the opposite of the licensed WRDS sources in this appendix. FRED carries
**no** GMU-infrastructure restriction: you may pull it on a laptop, cache it, and (unlike CRSP or
OptionMetrics) *commit the cached raw file* to git if you wish. The discipline of CONVENTIONS §5
still applies *uniformly* anyway — pin the snapshot/vintage, cache to `data/raw/fred_*.parquet`, and
log the pull in `logs/pulls.jsonl` with a content hash — because reproducibility, not licensing, is
the point. Two honest caveats remain: keep the *API key* in an env var (§5, it is a credential), and
honor the redistribution courtesy — when you re-publish a FRED series, **cite the underlying source**
(BLS, BEA, Treasury, Freddie Mac), per §6.

## Gotchas

- **Series get revised.** GDP, payrolls, and many others are restated months after first release.
  A "pull the latest" today gives different numbers next quarter. For any point-in-time or event-
  study design, pull an **ALFRED vintage**, not the current value — otherwise you are quietly using
  data that did not exist on your event date (look-ahead bias).
- **Cite the factory, not the truck.** "Source: FRED" alone violates §6. Cite BLS/BEA/Treasury and
  give the FRED series ID for reproducibility.
- **Frequency and seasonal adjustment.** `UNRATE` is monthly and seasonally adjusted; `DGS10` is
  daily; mixing frequencies without explicit resampling silently misaligns your panel. The same
  concept often exists in both SA and NSA versions under *different* IDs — pick deliberately.
- **Rate limit.** Roughly **~120 requests/minute per key** [CHECK current published limit]; batch
  your series and cache so a re-run reads from disk, not the API.
- **Discontinued/renamed series.** Series can be discontinued or superseded by a new ID; a script
  hard-coding an old ID will silently return stale or empty data. Pin and log the ID you used.

## "First 10 rows" schema sketch — `UNRATE`, monthly (illustrative — not real data)

| date | UNRATE |
|------|-------:|
| 2024-01-01 | 3.8 |
| 2024-02-01 | 3.9 |
| 2024-03-01 | 3.8 |
| 2024-04-01 | 4.0 |
| 2024-05-01 | 4.0 |
| 2024-06-01 | 4.1 |
| 2024-07-01 | 4.2 |
| 2024-08-01 | 4.2 |
| 2024-09-01 | 4.1 |
| 2024-10-01 | 4.1 |

(Values are fabricated for shape illustration only — do not cite these as real unemployment data.)

## Which chapter / lab uses it

This is the **worked example** for the data-card template in **Lab 7** (Your Data, Reproducibly),
the headline free source in **Chapter 7.2** (Data Acquisition in Practice), and the dataset behind
**Capstone 5 — FRED Macro Event Study** (Week 8), where macro/monetary-announcement series drive a
proper event-study inference. It is **Priya's** macro-control source for her Week-7 climate-and-
insurance DiD (NOAA storm events + FEMA declarations + a FRED/CPI insurance-cost proxy), and the
generic macro-control layer for any cast member's capstone. Pull it the §5 way: pinned (ALFRED
vintage when point-in-time matters), cached, logged — and cite the underlying agency.
