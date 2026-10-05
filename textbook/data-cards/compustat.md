# Data Card — Compustat (S&P Global Fundamentals)

**Provider & what it is.** Compustat, from S&P Global Market Intelligence and distributed through WRDS, is the standardized record of company *financial statements*: income statement, balance sheet, and cash-flow items re-coded into a consistent variable set so that "total assets" means the same column for every firm in every year. It is the accounting half of empirical finance — the data behind every book-to-market, leverage, profitability, or accruals measure. The reveal-the-trick point: Compustat looks like a clean spreadsheet but hides two traps that have ruined countless student results — **double-counting** if you omit the standard-format filters, and **look-ahead bias** if you ignore the gap between fiscal year-end and when the numbers were public. Priya's insurer fundamentals live here.

## Coverage
- **Span.** North American annual fundamentals (`comp.funda`) back to roughly the **1950s/1960s**; quarterly (`comp.fundq`) from the **1960s**; a separate Global file extends international coverage. [CHECK] exact earliest coverage years.
- **Frequency.** **Annual** (`funda`) and **Quarterly** (`fundq`). Quarterly is what you use for event studies and anything needing within-year timing; annual for slow-moving ratios.
- **Universe.** Tens of thousands of publicly traded firms (and some private filers). Includes firms that have since gone bankrupt or been acquired — but mind that *inactive* firms still appear, so filter on the period you want, not on "firms alive today."

## Key identifiers
- **GVKEY** — a permanent *company* identifier (six digits). Never changes; the join key you carry.
- **datadate** — the fiscal period-end date. A firm-year is `(gvkey, datadate)`; a firm-quarter is `(gvkey, datadate)` in `fundq`. Watch for non-December fiscal year-ends.
- **fyear** / **fyearq, fqtr** — fiscal year and quarter labels (distinct from calendar year).
- The link to CRSP's PERMNO runs through `crsp.ccmxpf_lnkhist` (respect `linktype`, `linkprim`, valid date range) — a Ch 7.4 crosswalk.

## Access path
Same WRDS/`wrds` pattern as CRSP; credentials from `.pgpass` or env (CONVENTIONS §5). The non-obvious must-do is the **standard-format filter**, without which you double-count restated and non-standard records.

```python
import os, wrds, pandas as pd, pathlib

db = wrds.Connection(wrds_username=os.environ["WRDS_USERNAME"])  # secret from env

raw = pathlib.Path("data/raw/comp_funda_2010_2020.parquet")      # git-ignored
if raw.exists():
    funda = pd.read_parquet(raw)
else:
    funda = db.raw_sql("""
        SELECT gvkey, datadate, fyear, at, lt, ceq, ni, sale, dltt, dlc
        FROM   comp.funda
        WHERE  datadate BETWEEN '2010-01-01' AND '2020-12-31'
          AND  indfmt='INDL' AND datafmt='STD'             -- standard format
          AND  popsrc='D'    AND consol='C'                -- domestic, consolidated
    """, date_cols=["datadate"])
    funda.to_parquet(raw)                                  # cache to GMU infra only
db.close()
```

The four filters `indfmt='INDL'`, `datafmt='STD'`, `popsrc='D'`, `consol='C'` are not optional decoration — they select the one canonical record per firm-year. Drop them and a firm can appear several times.

## License & the "stays on GMU infrastructure" note (CONVENTIONS §5)
Compustat is **licensed** (S&P Global), accessed **read-only** via WRDS. Like CRSP, it may be queried only on **WRDS Cloud** or GMU's **Hopper**, cached to a git-ignored `data/raw/`, and **never committed, emailed off campus, posted publicly, or pasted into a commercial LLM/web service.** Your repository holds the query and the pull log; the licensed records stay in the GMU kitchen. A collaborator with their own GMU seat re-runs your code to regenerate the extract.

## Gotchas
- **The reporting lag (the big one).** `datadate` is the fiscal period-*end*, not when the numbers became public. A December 31 10-K is typically filed weeks-to-months later. If you match accounting data to returns, you must lag it — the Fama–French convention is to match June-of-year-*t* returns to accounting data from the fiscal year ending in calendar year *t–1* (a 6-month buffer). Skip the lag and you have used information that was not yet knowable: look-ahead bias.
- **Standard-format filters** (above) — omit them and you double-count.
- **Non-December fiscal year-ends.** Sorting "by year" without using `datadate` mixes timing across firms.
- **Restatements & point-in-time.** Standard Compustat reflects the *latest* restated values, not what was originally reported. For a true point-in-time study use the **Compustat Point-in-Time / Snapshot** files. [CHECK] the exact PIT table name on WRDS.
- **Units and missing.** Most items are in **millions of dollars**; missing is `NULL`/`NaN`, and a missing item is not a zero — never `fillna(0)` a balance-sheet line without thinking.
- **`fundq` flow vs. stock items.** Quarterly *flow* variables (e.g., `saleq`) are per-quarter; some come as year-to-date and need differencing. [CHECK] per-item.

## "First 10 rows" schema sketch (illustrative — not real Compustat data)

| gvkey (str) | datadate (date) | fyear (int) | at (float, $M) | lt (float, $M) | ceq (float, $M) | ni (float, $M) | sale (float, $M) |
|---|---|---|---|---|---|---|---|
| 001045 | 2010-12-31 | 2010 | 25198.0 | 20114.0 | 5084.0 | 1212.0 | 17688.0 |
| 001045 | 2011-12-31 | 2011 | 27021.0 | 21330.0 | 5691.0 | 1340.0 | 18420.0 |
| 002176 | 2010-06-30 | 2010 | 803.4 | 412.1 | 391.3 | 44.7 | 612.9 |
| 006066 | 2010-12-31 | 2010 | 181069.0 | 154170.0 | 26899.0 | 14833.0 | 99870.0 |
| 012141 | 2010-12-31 | 2010 | 86113.0 | 58879.0 | 27234.0 | 18760.0 | 62484.0 |
| ... | ... | ... | ... | ... | ... | ... |

(Numbers invented to show *shape and types*: note the non-December `datadate` in row 3 — a fiscal year-end that will trip up naive "group by calendar year" code.)

## Which chapter/lab/capstone uses it
- **Week 5** — nb5.1/nb5.2 (Fama–French size/value sorts, factor construction) merge Compustat fundamentals to CRSP returns; the reporting-lag convention is taught here.
- **Week 7, Ch 7.2 & 7.4** — Compustat is a core WRDS source; Ch 7.4 covers the CRSP↔Compustat (PERMNO↔GVKEY) crosswalk and the look-ahead discipline.
- Priya's climate/insurer fundamentals thread; any capstone using accounting variables (leverage, profitability, book-to-market).
