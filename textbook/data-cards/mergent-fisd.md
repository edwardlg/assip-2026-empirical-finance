# Data Card — Mergent FISD (Fixed Income Securities Database)

**Provider & what it is.** Mergent FISD, distributed through WRDS, is the reference database of **corporate-bond issue characteristics**: coupon, maturity, offering amount and date, seniority, security/collateral, callability and other embedded options, covenants, and the agencies' ratings history. If **TRACE** is the *trade tape* — what happened to a bond's price — FISD is the bond's *biography* — what the bond *is*. The reveal-the-trick point is that you almost never use FISD alone: it is the lookup table you join to a TRACE trade so that "this CUSIP traded at 101.25" becomes "a 10-year, BBB, callable, senior unsecured note traded at 101.25." Most of the variables that explain a credit spread live in FISD, not in the price.

## Coverage
- **Span.** U.S. corporate and agency debt issues, with deep historical coverage of issues outstanding from roughly the **1990s** forward and many earlier issues; rating histories from the agencies over the issue's life. [CHECK] exact earliest reliable coverage and the universe of agency/MTN inclusion.
- **Frequency.** **Issue-level reference data** (mostly static per issue), plus *event* tables that are time-stamped: rating changes, calls, and amendments. Not a price series — there is no daily frequency.
- **Universe.** Corporate bonds, medium-term notes, and agency debt issued or registered for U.S. markets; both currently outstanding and matured/retired issues.

## Key identifiers
- **CUSIP** (9-character) — the issue-level join key to TRACE and to holdings data. As elsewhere, **CUSIP is a licensed identifier**; use it to merge, do not redistribute a master.
- **ISSUE_ID** — FISD's own internal issue identifier (stable within FISD; use it for joins *within* the FISD tables, e.g., issue → rating history).
- **ISSUER_ID** / issuer CUSIP (6-char) — the FISD issuer key; one issuer has many issues. Bridge issuer to Compustat GVKEY via name/CUSIP matching — a Ch 7.4 crosswalk, and a messy one.

## Access path
Same WRDS/`wrds` pattern; credentials from `.pgpass` or env (CONVENTIONS §5). FISD is split across an *issue* table and several *event* tables (ratings, etc.), joined on `ISSUE_ID`.

```python
import os, wrds, pandas as pd, pathlib

db = wrds.Connection(wrds_username=os.environ["WRDS_USERNAME"])   # secret from env

raw = pathlib.Path("data/raw/fisd_issues.parquet")               # git-ignored
if raw.exists():
    issues = pd.read_parquet(raw)
else:
    issues = db.raw_sql("""
        SELECT issue_id, complete_cusip, issuer_cusip, offering_date,
               offering_amt, coupon, maturity, security_level,
               bond_type, callable, convertible
        FROM   fisd.fisd_mergedissue
        WHERE  bond_type IN ('CDEB','CMTN')        -- corp debentures / MTNs
    """, date_cols=["offering_date", "maturity"])
    issues.to_parquet(raw)                                       # GMU infra only

    # Rating history is a SEPARATE event table, joined on issue_id:
    ratings = db.raw_sql("""
        SELECT issue_id, rating_date, rating, rating_type
        FROM   fisd.fisd_ratings
    """, date_cols=["rating_date"])
db.close()
```

[CHECK] the exact WRDS table names (`fisd.fisd_mergedissue`, `fisd.fisd_ratings`, the issuer table) — naming has varied across vintages; confirm with `db.list_tables(library="fisd")` and `db.describe_table(...)`.

## License & the "stays on GMU infrastructure" note (CONVENTIONS §5)
Mergent FISD is **licensed** (via WRDS), accessed **read-only**. Query only on **WRDS Cloud** or GMU's **Hopper**, cache to a git-ignored `data/raw/`, and **never commit, email off campus, post publicly, or paste into a commercial web service.** CUSIP is separately licensed — no CUSIP master leaves the building. As with every WRDS source, the repository ships the query and the pull log; a GMU-seated collaborator re-runs the recipe to regenerate the extract.

## Gotchas
- **It is reference data, not prices.** FISD tells you what a bond *is*; pair it with TRACE for what it *did*. The whole point is the join.
- **Issue-level vs. issuer-level.** One issuer (`issuer_id`) has many issues; aggregating to the issuer requires deciding how to weight (by offering amount? equally?). State the choice.
- **`bond_type` filtering.** FISD mixes corporate debentures, MTNs, convertibles, asset-backed, and more. A "corporate bond" sample needs an explicit `bond_type` filter; including convertibles or ABS by accident contaminates a credit-spread study.
- **Ratings: which agency, which scale, and timing.** The ratings table has multiple agencies and rating *types*; you must map letter grades to a numeric scale yourself and respect the `rating_date` so you use the rating *in force* at your event, not the latest one (a look-ahead trap).
- **Embedded options change the analysis.** A callable or convertible bond's spread is not comparable to a straight bond's; the `callable`/`convertible` flags are not optional context — they change which bonds belong in your sample.
- **Maturity/retirement.** A matured or called bond stops trading; align FISD's maturity/call events with the TRACE window.

## "First 10 rows" schema sketch (illustrative — not real FISD data)

| issue_id (int) | complete_cusip (str) | issuer_cusip (str) | offering_date (date) | offering_amt ($000s) | coupon (float) | maturity (date) | security_level (str) | callable (str) |
|---|---|---|---|---|---|---|---|---|
| 480211 | 037833AK6 | 037833 | 2013-05-03 | 2000000 | 2.400 | 2023-05-03 | SEN | N |
| 480212 | 037833AL4 | 037833 | 2013-05-03 | 3000000 | 3.850 | 2043-05-03 | SEN | Y |
| 512744 | 594918AC8 | 594918 | 2012-11-07 | 750000 | 2.125 | 2022-11-07 | SEN | N |
| 601233 | 17275RAH5 | 17275R | 2015-03-03 | 1500000 | 3.450 | 2025-03-03 | SUB | Y |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

(Values invented to show *shape and types*: rows 1–2 are two issues from the **same** issuer with different maturities and call features — why you cannot collapse an issuer to "one bond.")

## Which chapter/lab/capstone uses it
- **Week 7, Ch 7.2** — part of the WRDS fixed-income toolkit; pairs with the TRACE card.
- The standard companion to **TRACE** for any fixed-income capstone (credit-spread cross-section, bond liquidity, rating-change event studies): FISD supplies the issue characteristics and rating history that the controls and sample filters require — an advanced extension beyond the equity-focused anomaly thread.
