# Data Card — CRSP (Center for Research in Security Prices)

**Provider & what it is.** CRSP, maintained at the University of Chicago Booth School and distributed through WRDS, is the canonical record of U.S. stock prices, returns, shares outstanding, and — its single most valuable feature — *delisting returns* and a survivorship-bias-free universe of listed equities back to 1925. When a finance paper says "we use CRSP monthly returns," this is what it means. The reveal-the-trick point: CRSP is not just "stock prices"; it is a *carefully maintained, point-in-time-correct, survivorship-free* panel — exactly the correctness free sources like Yahoo do not give you. Sam's momentum backtests and every anomaly study in Week 5 rest on it.

## Coverage
- **Span.** Monthly stock file (`crsp.msf`) and daily stock file (`crsp.dsf`) back to **1925/1926**; coverage deepens over time as exchanges were added (NYSE first, then AMEX, then Nasdaq from 1972). [CHECK] exact start dates per exchange.
- **Frequency.** Monthly and daily. (Annual and weekly derived files exist; the two workhorses are `msf` and `dsf`.)
- **Universe.** U.S. common stocks, ADRs, REITs, closed-end funds, and more, listed on NYSE/AMEX/Nasdaq/Arca. Crucially it includes securities that *have since delisted*, so a backtest that uses CRSP does not silently drop the losers — the survivorship-bias fix you study in Ch 7.4.

## Key identifiers
- **PERMNO** — a permanent *security* identifier. Unlike a ticker, it never changes when a firm renames or re-tickers, and it is never reused. This is the join key you carry everywhere.
- **PERMCO** — a permanent *company* identifier (a company can have several PERMNOs, e.g., multiple share classes).
- Tickers and CUSIPs are *also* present but are historical and can change; never join on ticker.
- The link to Compustat's GVKEY runs through the **CRSP/Compustat Merged** table `crsp.ccmxpf_lnkhist` (respect `linktype`, `linkprim`, and the link's valid date range) — a Ch 7.4 crosswalk, not a string match.

## Access path
WRDS is a remote PostgreSQL database; you send SQL to it with the `wrds` package and get back a DataFrame. Credentials come from `.pgpass` or the environment — **never** hard-coded (CONVENTIONS §5).

```python
import os, wrds, pandas as pd, pathlib

db = wrds.Connection(wrds_username=os.environ["WRDS_USERNAME"])  # secret from env

# SELECT only the columns/rows you need; bound the dates. Never SELECT * on msf/dsf.
raw = pathlib.Path("data/raw/crsp_msf_2010_2020.parquet")        # git-ignored dir
if raw.exists():
    msf = pd.read_parquet(raw)
else:
    msf = db.raw_sql("""
        SELECT permno, date, ret, retx, prc, shrout, vol
        FROM   crsp.msf
        WHERE  date BETWEEN '2010-01-01' AND '2020-12-31'
    """, date_cols=["date"])
    # Delisting returns live in a SEPARATE table -- pull and merge them in:
    dl = db.raw_sql("""
        SELECT permno, dlstdt, dlret, dlstcd
        FROM   crsp.msedelist
    """, date_cols=["dlstdt"])
    msf.to_parquet(raw)        # cache the raw pull to GMU infrastructure only
db.close()
```

Explore the schema first with `db.list_tables(library="crsp")` and `db.describe_table("crsp","msf")`.

## License & the "stays on GMU infrastructure" note (CONVENTIONS §5)
CRSP is **licensed**, not public — GMU pays for the right to *use* it under terms that forbid redistributing the raw records. The connection is **read-only**. The hard consequence: you may query CRSP only on **WRDS Cloud** or GMU's **Hopper** cluster, your derived extract is cached to a git-ignored `data/raw/`, and **the licensed bytes are never committed, emailed off campus, posted to a public repo, or pasted into any commercial web service.** What travels is the *recipe* — your query code and your pull log — not the data. Anyone with their own GMU WRDS seat can re-run your code; that is reproducibility done within the license.

## Gotchas
- **`RET` vs. `RETX`.** `RET` includes dividends (total return — what you almost always want); `RETX` excludes them. Using the wrong one silently biases every return-based result.
- **Delisting returns are in a separate table** (`crsp.msedelist`). Ignore them and you get survivorship bias precisely when a firm fails — the worst time to be missing data. Merge `dlret` in.
- **Missing-return codes.** `RET` can carry special non-numeric values (e.g., for halts/missing prices); coerce and inspect, do not blindly cast to float. [CHECK] the current code set.
- **Negative `PRC`** means the price is a *bid/ask midpoint*, not a trade; take the absolute value before using it as a price.
- **Shares outstanding (`shrout`) are in thousands** — market cap = `|prc| * shrout * 1000`.
- **Size of `dsf`.** The daily file is tens of millions of rows; `SELECT *` will time out or exhaust memory. Bound by date and PERMNO.

## "First 10 rows" schema sketch (illustrative — not real CRSP data)

| permno (int) | date (date) | ret (float) | retx (float) | prc (float) | shrout (int, 000s) | vol (float) |
|---|---|---|---|---|---|---|
| 10001 | 2010-01-29 | 0.0312 | 0.0298 | 24.13 | 41200 | 1.2e6 |
| 10001 | 2010-02-26 | -0.0145 | -0.0145 | 23.78 | 41200 | 9.8e5 |
| 10026 | 2010-01-29 | 0.0501 | 0.0501 | 112.40 | 88300 | 4.1e6 |
| 10026 | 2010-02-26 | 0.0088 | 0.0061 | 113.39 | 88300 | 3.7e6 |
| 14593 | 2010-01-29 | 0.0210 | 0.0210 | -56.02 | 901000 | 2.2e7 |
| ... | ... | ... | ... | ... | ... | ... |

(Values invented to show *shape and types*: note the negative `prc` in row 5 — a bid/ask midpoint — and `ret`≠`retx` when a dividend is paid.)

## Which chapter/lab/capstone uses it
- **Week 2, Lab 2** — "Replicate a Textbook Fama–MacBeth on CRSP" (Path A pulls `crsp.msf`; Path B is the synthetic fallback). The lab pins the CRSP snapshot date.
- **Week 5** — nb5.1–nb5.3 (Fama–French 1992/1993 sorts, Jegadeesh–Titman momentum) build portfolios on CRSP/Compustat.
- **Week 7, Ch 7.2** — CRSP is the lead example of the WRDS access pattern and the GMU-infrastructure rule.
- Sam's anomaly/momentum thread; any capstone needing survivorship-free U.S. equity returns.
