# Data Card — OptionMetrics (IvyDB US)

## Provider & what it is

OptionMetrics is a commercial data vendor; its flagship product, **IvyDB US**, is the
research standard for historical U.S. equity and index *option* data. Here is the trick to
understanding why it exists: raw option quotes off an exchange are a mess, and the "price" of
an option is meaningless without the matching spot price, interest rate, and dividend
assumption. IvyDB does the unglamorous cleaning and, crucially, *backs out the implied
volatility and the Greeks* (delta, gamma, vega, theta) under a documented model, so you do not
have to. What you get is a daily, end-of-day panel: for every listed option, a standardized
record — best bid, best ask, volume, open interest, implied volatility, and the Greeks — plus
companion files of underlying prices, the zero-coupon interest-rate curve, projected dividends,
and a "volatility surface" of model-interpolated implied vols at fixed maturities and deltas.
GMU accesses it through **WRDS**, beside CRSP and Compustat.

## Coverage

U.S. exchange-listed equity options and index options. The history begins in **1996** and runs
to the most recent vintage WRDS has loaded. Frequency is **daily** (end-of-day snapshots; IvyDB
US is not an intraday/tick product — that is a separate, pricier OptionMetrics feed). Cross-
sectional breadth is essentially every optionable U.S. stock and the major index options
(S&P 500, etc.). There are companion international IvyDB products (Europe, Asia); this card is
for **IvyDB US** only — confirm which regions GMU's WRDS subscription actually includes before
you build on them. [CHECK: exact list of IvyDB modules in GMU's current WRDS license.]

## Key identifiers

The spine identifier is **`secid`** — OptionMetrics' own permanent security ID for the
*underlying*. It is not a ticker, not a CUSIP, and not CRSP's PERMNO; it is internal to
OptionMetrics, so the very first thing any IvyDB-to-CRSP project needs is a `secid`↔`permno`
crosswalk (WRDS ships one; building and validating that link is a Chapter 7.4 problem, out of
scope here). An individual *option contract* is identified by `optionid`, or equivalently by the
tuple **`secid` + expiration date + strike price + call/put flag**. The standardized volatility-
surface file keys on `secid` + a fixed `days`-to-maturity + `delta` bucket rather than on real
contracts.

## Access path (Python via WRDS)

IvyDB lives in the `optionm` library on WRDS. You query it exactly like the other WRDS sources —
PostgreSQL over the `wrds` Python package, no API key in code:

```python
import os, wrds
db = wrds.Connection(wrds_username=os.environ["WRDS_USERNAME"])  # token cached by the package

# Explore first — names and years are vintage-dependent.
db.list_tables(library="optionm")

# Pull one underlying's option prices for a bounded window (NEVER SELECT *).
df = db.raw_sql("""
    SELECT secid, date, optionid, cp_flag, strike_price, exdate,
           best_bid, best_offer, volume, open_interest, impl_volatility,
           delta, gamma, vega, theta
    FROM optionm.opprcd2023
    WHERE secid = %(sid)s AND date BETWEEN %(d0)s AND %(d1)s
""", params={"sid": 101594, "d0": "2023-01-01", "d1": "2023-12-31"})
```

Note the table name pattern: the daily option-price file is often partitioned by year
(`opprcd2023`, `opprcd2024`, …); `secid` values above are *illustrative placeholders*, not a
real security. Always bound by `secid` and `date` — the unbounded table is enormous.

## License & GMU-infra note (§5)

**Licensed, not public.** OptionMetrics is a paid WRDS subscription; the license permits use by
GMU-affiliated researchers *on GMU systems only*. Per CONVENTIONS §5 this is the central, non-
negotiable rule: **licensed to GMU; analyzed only on GMU infrastructure (WRDS Cloud or the
Hopper cluster); raw data never copied off and never committed to git.** You may not download
IvyDB to a personal laptop, email it outside GMU, push it to a public repo, or paste it into a
commercial web service. Your repository commits the *query code* and the *pull log*; the licensed
bytes stay in a git-ignored `data/raw/` on GMU infrastructure. Pin the WRDS snapshot/vintage date
in a comment and in `logs/pulls.jsonl`.

## Gotchas

- **Implied vol and Greeks are model outputs, not market facts.** Computed under OptionMetrics'
  documented assumptions; two vendors can report different IVs for the same option. Cite the
  methodology; do not treat the IV as if the exchange published it.
- **`secid` is not a ticker or PERMNO.** Every cross-dataset merge needs the crosswalk, which can
  be one-to-many around ticker changes, mergers, and re-listings.
- **Bid–ask and stale quotes.** Thinly traded contracts have wide spreads and can carry stale or
  crossed quotes; the midpoint can be a fiction. Filter on volume/open interest first.
- **The volatility surface is interpolated** — smoothed and filled at fixed grid points; it is a
  *model*, not raw contracts.
- **Year-partitioned tables drift.** Table and column names change across vintages; run
  `db.describe_table` instead of hard-coding.

## "First 10 rows" schema sketch (illustrative — not real data)

| secid | date | optionid | cp_flag | strike_price | exdate | best_bid | best_offer | volume | open_interest | impl_volatility | delta |
|------:|------|---------:|:-------:|-------------:|--------|---------:|-----------:|-------:|--------------:|----------------:|------:|
| 100001 | 2023-03-01 | 84412001 | C | 150.00 | 2023-06-16 | 6.10 | 6.35 | 412 | 5120 | 0.281 | 0.561 |
| 100001 | 2023-03-01 | 84412002 | P | 150.00 | 2023-06-16 | 5.05 | 5.30 | 198 | 3340 | 0.293 | -0.439 |
| 100001 | 2023-03-01 | 84412003 | C | 160.00 | 2023-06-16 | 2.40 | 2.60 | 880 | 9870 | 0.265 | 0.331 |
| 100001 | 2023-03-02 | 84412001 | C | 150.00 | 2023-06-16 | 6.45 | 6.70 | 365 | 5210 | 0.288 | 0.574 |
| 100002 | 2023-03-01 | 90017505 | C | 75.00 | 2023-04-21 | 1.15 | 1.30 | 1204 | 14002 | 0.402 | 0.402 |
| 100002 | 2023-03-01 | 90017506 | P | 75.00 | 2023-04-21 | 0.95 | 1.10 | 640 | 8800 | 0.418 | -0.598 |
| 100002 | 2023-03-02 | 90017505 | C | 75.00 | 2023-04-21 | 1.05 | 1.20 | 990 | 14110 | 0.395 | 0.388 |
| 100003 | 2023-03-01 | 77230110 | C | 420.00 | 2023-09-15 | 18.20 | 18.90 | 55 | 1220 | 0.221 | 0.612 |
| 100003 | 2023-03-01 | 77230111 | P | 420.00 | 2023-09-15 | 16.40 | 17.10 | 47 | 980 | 0.230 | -0.388 |
| 100003 | 2023-03-02 | 77230110 | C | 420.00 | 2023-09-15 | 19.05 | 19.80 | 61 | 1255 | 0.225 | 0.625 |

(Values are fabricated for shape illustration only.)

## Which chapter / lab uses it

Catalogued in **Appendix C** and surveyed as a WRDS-licensed source in **Chapter 7.2**
(Data Acquisition in Practice). It is the natural data layer for any Week-7/Week-8 capstone on
options, implied volatility, or the volatility risk premium — a Sam-style (markets/trading)
extension. Treat it the same way Ch 7.2 treats CRSP/Compustat: read-only on GMU infrastructure,
pinned, cached, logged.
