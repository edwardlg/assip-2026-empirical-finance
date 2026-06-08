# Data Card — IBES (Institutional Brokers' Estimate System)

**Provider & what it is.** IBES, from Refinitiv/LSEG and distributed through WRDS, is the standard record of **sell-side analyst expectations**: earnings-per-share forecasts, revenue and other line-item forecasts, long-term growth estimates, and buy/hold/sell recommendations. It is how empirical finance measures "what the market expected" before a firm reports — the raw material for earnings-surprise studies, post-earnings-announcement drift, and analyst-disagreement measures. The reveal-the-trick point: IBES gives you the same expectation in two very different shapes — a pre-cooked **consensus** (Summary) and the **detail** of every individual analyst's forecast — and choosing the wrong one, or mismatching its identifier to CRSP/Compustat, is where careful studies go wrong.

## Coverage
- **Span.** U.S. EPS estimates from roughly **1976**; recommendations from the early **1990s**; international coverage in separate files. [CHECK] exact start years per file.
- **Frequency.** Forecasts arrive *irregularly*, whenever analysts issue or revise them; the Summary file snapshots the consensus on a **monthly statistical period** (the third Thursday of each month, by IBES convention). Detail is event-time, per forecast.
- **Universe.** Tens of thousands of firms with analyst coverage (skewed toward larger, more-followed firms — coverage is itself an outcome, not random).

## Key identifiers
- **TICKER** — IBES's *own* internal ticker, **not** the exchange ticker. This is the classic trap: a CRSP ticker and an IBES `ticker` look alike and are not interchangeable.
- **CUSIP** — IBES carries a (historical) CUSIP you can use to bridge to CRSP/Compustat, but it is the *unmasked* CUSIP and changes over time; align on the date.
- **CNAME** — company name (for sanity-checking a match, never for joining).
- The standard bridge to CRSP is via the **IBES–CRSP link** table on WRDS (`wrdsapps.ibcrsphist` or the ICLINK procedure). [CHECK] the current link-table name.

## Access path
Same WRDS/`wrds` pattern; credentials from `.pgpass` or env (CONVENTIONS §5). Decide *consensus vs. detail* first — they live in different tables.

```python
import os, wrds, pandas as pd, pathlib

db = wrds.Connection(wrds_username=os.environ["WRDS_USERNAME"])  # secret from env

raw = pathlib.Path("data/raw/ibes_statsum_2010_2020.parquet")    # git-ignored
if raw.exists():
    cons = pd.read_parquet(raw)
else:
    # CONSENSUS (Summary), U.S. EPS, one-period-ahead forecasts:
    cons = db.raw_sql("""
        SELECT ticker, cusip, statpers, fpedats, meanest, medest,
               numest, stdev, fpi
        FROM   ibes.statsum_epsus
        WHERE  statpers BETWEEN '2010-01-01' AND '2020-12-31'
          AND  fpi = '1'                       -- 1 = next fiscal year end
    """, date_cols=["statpers", "fpedats"])
    cons.to_parquet(raw)                        # cache to GMU infra only
db.close()
```

For the per-analyst **detail** file you query `ibes.detu_epsus` (one row per analyst-forecast), which you need for dispersion, revisions, and analyst-level studies. Use `db.describe_table("ibes", ...)` to confirm columns before a big pull.

## License & the "stays on GMU infrastructure" note (CONVENTIONS §5)
IBES is **licensed** (Refinitiv/LSEG), accessed **read-only** via WRDS. Query only on **WRDS Cloud** or GMU's **Hopper**, cache to a git-ignored `data/raw/`, and **never commit, email off campus, post publicly, or paste into a commercial web service.** As with all WRDS sources, the repository ships the query and the pull log, not the data; a GMU-seated collaborator re-runs the recipe.

## Gotchas
- **Consensus vs. detail.** Summary (`statsum_*`) gives you a ready-made mean/median consensus and is right for surprise measures; Detail (`detu_*`) gives every analyst's forecast and is required for *dispersion* and *revision* studies. Don't reconstruct a consensus from detail unless you must — IBES's own consensus follows specific inclusion rules.
- **The IBES ticker trap.** Joining IBES to CRSP on the *exchange* ticker is wrong; use the IBES `ticker` only within IBES and bridge to PERMNO through the link table.
- **The `fpi` / forecast-period code.** `fpi='1'` is next annual, `'2'` the one after, `'0'`/`'6'` quarterly variants, etc. Mixing horizons silently mixes apples and oranges. [CHECK] the full `fpi` code set.
- **Pre- vs. post-split, and the actuals file.** Forecasts and reported *actuals* must be on the same **adjusted/unadjusted** basis; IBES split-adjusts, and matching a split-adjusted forecast to an unadjusted actual produces nonsense surprises. The realized number lives in the **actuals** file (`ibes.actu_epsus`).
- **Stale/last-revision logic.** A consensus on a given `statpers` reflects forecasts within IBES's lookback window; very stale forecasts may or may not be excluded depending on the file. Read the IBES manual section for your file.
- **Survivorship in coverage.** Firms gain and lose analyst coverage; "firms in IBES today" is a selected sample.

## "First 10 rows" schema sketch (illustrative — not real IBES data)

| ticker (str) | cusip (str) | statpers (date) | fpedats (date) | fpi (str) | meanest (float) | medest (float) | numest (int) | stdev (float) |
|---|---|---|---|---|---|---|---|---|
| AAPL | 03783310 | 2010-01-21 | 2010-09-30 | 1 | 9.42 | 9.50 | 31 | 0.61 |
| AAPL | 03783310 | 2010-02-18 | 2010-09-30 | 1 | 9.58 | 9.55 | 33 | 0.55 |
| MSFT | 59491810 | 2010-01-21 | 2010-06-30 | 1 | 2.05 | 2.06 | 28 | 0.12 |
| XYZ0 | 98412310 | 2010-01-21 | 2010-12-31 | 1 | 1.10 | 1.12 | 4 | 0.31 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

(Values invented to show *shape and types*: note `ticker` is the IBES-internal code, `statpers` is the monthly snapshot date, and `stdev` across `numest` analysts is your raw dispersion measure.)

## Which chapter/lab/capstone uses it
- **Week 5/6** — earnings-surprise and analyst-dispersion measures support the anomaly and text-as-data readings (PEAD, disagreement); IBES is the standard "expectations" input.
- **Week 7, Ch 7.2** — listed among the core WRDS sources alongside CRSP/Compustat/TRACE.
- Any capstone built on earnings surprises, analyst disagreement, or recommendation changes (a natural extension of Sam's anomalies and Devon's event studies).
