# Data Card — Free Equity Price APIs: yfinance / Stooq / Tiingo / Alpha Vantage

**Provider & what it is.** Four free (or freemium) sources of daily stock prices and returns — the laptop-friendly alternatives to CRSP when you do not have a WRDS seat or just want to prototype before you spend cluster time. **yfinance** is an *unofficial* Python wrapper around Yahoo Finance; no key, dead simple, scrapes an undocumented endpoint. **Stooq** is a free Polish data service offering historical daily prices for global stocks, indices, and FX, reachable through `pandas-datareader`; no key. **Tiingo** is a freemium API with a generous free tier (and a key) offering cleaner, better-documented end-of-day prices and some fundamentals, with explicit terms of service. **Alpha Vantage** is a freemium API (free key, tight rate limit) covering equities, FX, crypto, and a library of technical indicators. The reveal that runs through this whole card: these sources are *good enough to build a pipeline and learn a method*, but they are **not survivorship-bias-free and not point-in-time correct**, which is precisely what CRSP buys you. Match the data source to the standard your conclusion must meet — a Tuesday prototype and a result you defend to a referee have different needs.

**Coverage.** yfinance: most U.S. and many international tickers Yahoo lists, daily (and intraday for recent windows), history back decades for large names. Stooq: global equities/indices/FX, daily, decent depth, a useful independent cross-check. Tiingo: U.S. equities + ETFs end-of-day with long history, plus IEX intraday and some fundamentals/news. Alpha Vantage: global equities, FX, crypto; daily/weekly/monthly and intraday. None guarantees a *complete delisted universe* — the central caveat below.

**Key identifiers.** The **ticker symbol** (e.g., `AAPL`), sometimes with a suffix denoting exchange/source (Stooq wants `AAPL.US`; international names use suffixes like `.L`, `.TO`). Tickers are *not* permanent identifiers — they get reused and reassigned when firms merge, delist, or rename, so a ticker today may point to a different company than the same ticker five years ago. This is why CRSP uses a stable `PERMNO`; the free sources do not have one. Map carefully and pin a date.

**Access path.** Keys via environment variables, never hard-coded (CONVENTIONS §5):

```python
import os, yfinance as yf
import pandas_datareader.data as web
import requests

# yfinance — no key, auto_adjust folds splits/dividends into the price
px = yf.download("AAPL", start="2010-01-01", end="2020-12-31", auto_adjust=True)

# Stooq — no key, via pandas-datareader (a good independent cross-check)
px_stooq = web.DataReader("AAPL.US", "stooq")

# Tiingo — key from the environment
headers = {"Authorization": f"Token {os.environ['TIINGO_API_KEY']}"}
r = requests.get("https://api.tiingo.com/tiingo/daily/AAPL/prices",
                 params={"startDate": "2010-01-01", "endDate": "2020-12-31"},
                 headers=headers, timeout=60)

# Alpha Vantage — key from the environment
av_key = os.environ["ALPHAVANTAGE_API_KEY"]
r2 = requests.get("https://www.alphavantage.co/query",
                  params={"function": "TIME_SERIES_DAILY_ADJUSTED",
                          "symbol": "AAPL", "outputsize": "full", "apikey": av_key},
                  timeout=60)
```

**License & note.** These are *terms-of-service*, not open-data licenses, and they differ. **yfinance** scrapes Yahoo, whose ToS does not contemplate programmatic redistribution — treat the data as for personal research, and never redistribute the raw pulls as "your" dataset. **Stooq** permits personal/non-commercial use. **Tiingo** and **Alpha Vantage** have explicit free-tier terms (attribution, no resale); read them. Because none of this is cleanly redistributable, **cache it for your own reproducibility but do not publish the raw bytes as a dataset** — publish the *code and the pinned pull date* instead. Cite the provider and the access date.

**Gotchas.**
- **Survivorship bias — the big one.** Delisted tickers often *vanish* from Yahoo/Stooq, so a backtest on "today's tickers" silently drops the losers and inflates returns. This is exactly the bias CRSP's delisting returns fix (Ch 7.4). For any return study, name this in your methods section.
- **yfinance is unofficial and unstable.** It scrapes an endpoint Yahoo can change without notice; a script that works today may break tomorrow. That instability makes *caching the raw response more important, not less* — your cache is the only guarantee the numbers will not move.
- **Adjustment quirks.** `auto_adjust=True` back-adjusts for splits and dividends, so historical prices change every time a dividend is paid; two pulls on different dates can disagree. Decide raw vs. adjusted and pin it.
- **Rate limits.** Alpha Vantage free is the tightest — on the order of a few calls per minute and a small daily cap `[CHECK]`; Tiingo free is a modest hourly/daily cap; yfinance/Stooq have no published limit but will throttle or block aggressive scraping. Loop politely: sleep, back off on errors, batch.
- **Cross-check two sources.** If yfinance and Stooq disagree on a price, you have found a data-quality problem before it found you.

**First 10 rows — schema sketch (illustrative; values invented, not real quotes).**

| date | ticker | open | high | low | close | adj_close | volume | source |
|---|---|---|---|---|---|---|---|---|
| 2020-01-02 | AAPL | 74.06 | 75.15 | 73.80 | 75.09 | 73.12 | 135480400 | yfinance |
| 2020-01-03 | AAPL | 74.29 | 75.14 | 74.13 | 74.36 | 72.41 | 146322800 | yfinance |
| 2020-01-06 | AAPL | 73.45 | 74.99 | 73.19 | 74.95 | 72.99 | 118387200 | yfinance |
| 2020-01-07 | AAPL | 74.96 | 75.22 | 74.37 | 74.60 | 72.65 | 108872000 | yfinance |
| 2020-01-08 | AAPL | 74.29 | 76.11 | 74.29 | 75.80 | 73.82 | 132079200 | yfinance |
| 2020-01-02 | AAPL.US | 74.06 | 75.15 | 73.80 | 75.09 | — | 135480400 | stooq |
| 2020-01-03 | AAPL.US | 74.29 | 75.14 | 74.13 | 74.36 | — | 146322800 | stooq |
| 2020-01-02 | AAPL | 74.06 | 75.15 | 73.80 | 75.09 | 73.10 | 135480400 | tiingo |
| 2020-01-02 | MSFT | 158.78 | 160.73 | 158.33 | 160.62 | 154.20 | 22622100 | tiingo |
| 2020-01-02 | TSLA | 28.30 | 28.71 | 28.11 | 28.68 | 28.68 | 142981500 | alphavantage |

(Note the small price disagreement and the missing `adj_close` from Stooq — the kind of gap a two-source cross-check surfaces.)

**Which chapter/lab/capstone uses it.** This is **Sam's** fallback data. The detailed treatment is **Ch 7.2 §7.2.8** ("Free alternatives — yfinance, Stooq, Tiingo"), and the **nb7.2** multi-source pull harness shows a side-by-side of yfinance vs. Stooq so you can *see* the data-quality gaps. It powers Sam's **Week 5** momentum/anomaly work (the portfolio-sort and factor-regression notebooks behind the Fama–French and Jegadeesh–Titman reading guides) when CRSP is unavailable, and his **Week 7** capstone question — *do past-12-month winners outperform losers next month?* (Ch 7.1 cast table). The Ch 7.1 §7.1.6 note is explicit: Sam prototypes on `yfinance` on a laptop and reaches for CRSP on WRDS (read-only, snapshot-dated) only for the long, survivorship-bias-free history. Whichever he uses, he discloses which and why — that disclosure is the **Lab 7** data card.
