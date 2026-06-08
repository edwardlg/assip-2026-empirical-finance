# Data Card — TRACE (Transaction Reporting and Compliance Engine)

**Provider & what it is.** TRACE, operated by **FINRA** and distributed through WRDS, is the transaction-by-transaction record of **U.S. corporate (and some other) bond trades**: for each reported trade, the price, the par volume, the time, and side flags. Before TRACE, the corporate-bond market was a black box — trades happened over-the-counter with no public tape. TRACE is the microscope that made modern bond-market microstructure and liquidity research possible. The reveal-the-trick point is that TRACE comes in **two forms with different sensitivity** — a **disseminated** (public-facing, partly masked) feed and an **academic/enhanced** version with fields the public feed hides — and the academic version's extra detail is exactly why the on-GMU-only rule bites hardest here.

## Coverage
- **Span.** Corporate-bond transactions from **July 2002** (phased in by bond size/rating through 2005), continuing to the present. The **Enhanced/Academic TRACE** historical file adds masked-field detail. [CHECK] exact phase-in dates and the academic-file lag (academic data is released with a multi-quarter delay).
- **Frequency.** Tick-level — one row per *reported* trade, time-stamped to the second (or finer in recent data).
- **Universe.** TRACE-eligible debt: corporate bonds, and in later expansions agency debt, securitized products, and Treasuries (a separate reporting regime). The core academic-finance use is **corporate bonds**.

## Key identifiers
- **CUSIP** (9-character) — identifies the *bond issue* (the specific security, not the issuer). As with 13F, **CUSIP is a licensed identifier**: use it to merge, do not redistribute a master.
- **bond_sym_id** — TRACE's own bond symbol.
- A trade is otherwise keyed by CUSIP + execution timestamp + a sequence/message field.
- To get *issue characteristics* (coupon, maturity, rating, covenants) you join CUSIP to **Mergent FISD** — see that data card; TRACE is trades, FISD is the bond's biography.

## Access path
Same WRDS/`wrds` pattern; credentials from `.pgpass` or env (CONVENTIONS §5). TRACE is enormous, so bound tightly by date and CUSIP.

```python
import os, wrds, pandas as pd, pathlib

db = wrds.Connection(wrds_username=os.environ["WRDS_USERNAME"])   # secret from env

raw = pathlib.Path("data/raw/trace_subset_2019.parquet")         # git-ignored
if raw.exists():
    trades = pd.read_parquet(raw)
else:
    # Bound by date AND a CUSIP list -- never an unbounded scan of the trade tape.
    trades = db.raw_sql("""
        SELECT cusip_id, trd_exctn_dt, trd_exctn_tm, rptd_pr,
               entrd_vol_qt, rpt_side_cd, trc_st
        FROM   trace.trace_enhanced
        WHERE  trd_exctn_dt BETWEEN '2019-01-01' AND '2019-12-31'
          AND  cusip_id IN ('037833AK6','594918AC8')   -- illustrative
    """, date_cols=["trd_exctn_dt"])
    trades.to_parquet(raw)                                       # GMU infra only
db.close()
```

[CHECK] the exact WRDS library/table for Enhanced TRACE (`trace.trace_enhanced` vs. variants) and the standard **cleaning steps** — TRACE requires deleting cancellations/corrections/reversals before use (see Dick-Nielsen's published cleaning procedure). Raw TRACE without that cleaning is *not* analysis-ready.

## License & the "stays on GMU infrastructure" note (CONVENTIONS §5)
TRACE is **licensed** (FINRA, via WRDS), accessed **read-only**, and the **academic/enhanced** version is *more* sensitive than most WRDS data because it un-masks fields (large-trade volumes, dealer detail) that the public dissemination deliberately caps to protect dealers' positions. So the §5 rule is non-negotiable here: query only on **WRDS Cloud** or GMU's **Hopper**, cache to a git-ignored `data/raw/`, and **never commit, email off campus, post publicly, or paste into a commercial web service.** The un-masked academic fields in particular must not leave GMU infrastructure under any circumstances. Ship the recipe (query + log), not the data; CUSIP masters are not redistributable either.

## Gotchas
- **Cancellations, corrections, and reversals.** A nontrivial share of raw messages are *not* clean executed trades — they cancel or correct an earlier message. Use the published cleaning procedure (drop trades flagged cancelled/corrected/reversed, handle agency double-counting) before computing anything. This is the single biggest TRACE mistake.
- **Disseminated vs. academic volume masking.** The *disseminated* feed caps reported volume above a threshold (e.g., trades over \$5M IG / \$1M HY shown as "5MM+"); the *academic* file un-masks it. Mixing the two, or assuming public volumes are exact, biases liquidity measures.
- **Agency vs. principal trades & double counting.** A single customer trade intermediated by a dealer can generate multiple TRACE reports; net them per the cleaning rules.
- **Price is per \$100 par**, not a dollar price; convert with par.
- **No quotes, only trades.** TRACE is a trade tape; there is no continuous quote. Liquidity proxies (bid-ask, Amihud) must be *estimated* from trades.
- **Academic-file release lag.** The enhanced/academic file is published with a delay, so the most recent quarters are unavailable in academic form. [CHECK] the current lag.

## "First 10 rows" schema sketch (illustrative — not real TRACE data)

| cusip_id (str) | trd_exctn_dt (date) | trd_exctn_tm (time) | rptd_pr (float, /100 par) | entrd_vol_qt (float, par $) | rpt_side_cd (str) | trc_st (str) |
|---|---|---|---|---|---|---|
| 037833AK6 | 2019-03-14 | 09:41:07 | 101.250 | 2000000 | B | T |
| 037833AK6 | 2019-03-14 | 10:02:55 | 101.310 | 5000000 | S | T |
| 037833AK6 | 2019-03-14 | 10:03:12 | 101.310 | 5000000 | B | R |
| 594918AC8 | 2019-03-14 | 13:18:44 | 98.875 | 250000 | S | T |
| ... | ... | ... | ... | ... | ... | ... |

(Values invented to show *shape and types*: row 3 has `trc_st='R'` — a reversal of row 2's trade — and must be removed in cleaning, the classic TRACE trap.)

## Which chapter/lab/capstone uses it
- **Week 7, Ch 7.2** — listed among the core WRDS sources (CRSP/Compustat/IBES/TRACE); the on-GMU-only sensitivity is emphasized.
- A natural data source for any fixed-income capstone (bond liquidity, the credit-spread cross-section), typically merged to **Mergent FISD** for issue characteristics — the kind of project Priya (insurer credit risk) or a fixed-income-minded student might pursue.
- Bond-market microstructure as an advanced extension of the equity-microstructure ideas in the anomalies/momentum thread.
