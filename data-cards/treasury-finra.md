# Data Card — U.S. Treasury (TreasuryDirect + Daily Yield Curve) and FINRA TRACE

## Provider & what it is

Two providers on the same shelf: the **risk-free curve** and the **corporate-bond tape**.

- **U.S. Department of the Treasury** runs two things you will use. **TreasuryDirect** is the record of Treasury security *auctions* — every bill, note, bond, TIPS, and FRN sold, with auction date, high yield, bid-to-cover ratio, and CUSIP. The **Daily Treasury Par Yield Curve** is a separate, daily table of constant-maturity yields (1-month to 30-year), the canonical "risk-free rate today" series that anchors discounting and the macro event studies of Capstone 5.
- **FINRA** (Financial Industry Regulatory Authority) runs **TRACE** — the Trade Reporting and Compliance Engine, which since 2002 requires dealers to report secondary-market trades in corporate (now also agency/securitized) bonds. The *public dissemination* feed is the post-trade tape: price, size (capped), and time per transaction, on a delay. This is how a high-schooler can see that corporate bonds, unlike stocks, trade rarely and in lumps.

The reveal: the "interest rate" is not one number. It is a *curve* the Treasury republishes every afternoon, and the spread between a corporate bond's TRACE price and the matching point on that curve is the credit risk premium you spend Week 3 onward learning to measure.

## Coverage

- **TreasuryDirect auctions:** all marketable Treasury auctions; the API goes back to the late 1970s for some series, with consistent coverage from the late 1990s. `[CHECK]` exact earliest date per security type.
- **Daily Treasury Yield Curve:** business days from 1990 to present for the par yield curve; the constant-maturity (CMT) tenors are 1, 2, 3, 4, and 6 months and 1, 2, 3, 5, 7, 10, 20, and 30 years (some tenors begin later — the 20-year and 4-month were added in different decades). `[CHECK]` tenor start dates.
- **TRACE public dissemination:** corporate bonds from July 2002 (phased in by issue size, fully disseminated by 2005); agency debt and later securitized products added afterward. The free public view is end-of-day / delayed and **trade-size-capped** (large trades show "$5MM+" rather than the true size). The full, uncapped, real-time academic file is a separate licensed WRDS product, not the free feed.

## Key identifiers

- **CUSIP** (9-character security id) is the spine for both Treasury auctions and TRACE bonds. A bond's CUSIP links its TRACE trades to its issuance terms.
- For yields, the join key is **(date, tenor)** — there is no CUSIP, because the par curve is a synthetic constant-maturity construct, not a tradable security.
- TRACE adds a **bond symbol** and the **trade timestamp**; the issuer ties back to a parent company via a separate mapping (you will need a CUSIP-to-issuer crosswalk, which the free feed does not give you).

## Access path

- **Treasury Fiscal Data API** (auctions, debt, rates): base `https://api.fiscaldata.treasury.gov/services/api/fiscal_service/`. JSON, paginated, **no key required**, generous rate limits. Auctions live under an `/v1/accounting/od/auctions_query` style endpoint. `[CHECK]` exact endpoint slug for your pinned vintage.
- **Daily Treasury Yield Curve:** published as XML/CSV at `https://home.treasury.gov/...` and also queryable through the Fiscal Data API; the most reproducible route for the camp is `pandas_datareader` against **FRED** (series like `DGS10`, `DGS2`, `DGS3MO`), which mirrors the Treasury CMT series and is what nb appears to use for the macro labs. No key for the CSV; a free FRED key for the FRED route, via env var `${FRED_API_KEY}`.
- **FINRA TRACE public feed:** the human-facing tool is the FINRA Fixed Income / Market Data site (`finra-markets.morningstar.com`-style pages, migrating to FINRA's own portal). There is **no clean, free, programmatic bulk API** for the public delayed tape; you query a bond at a time, or you use the licensed WRDS *Enhanced TRACE* file on GMU infrastructure for any real panel. `[CHECK]` current public-feed URL after FINRA's site migration.

```python
import requests
BASE = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service"
# Recent Treasury auctions, newest first (public, no key):
r = requests.get(f"{BASE}/v1/accounting/od/auctions_query",
                 params={"sort": "-auction_date", "page[size]": 10}, timeout=60)
auctions = r.json()["data"]   # list of dicts; see schema sketch below
```

## License & note

Both are **free and public**. Treasury data is U.S. government work, effectively public domain — cite it, no permission needed. FINRA's *public dissemination* tape is free to view under SEC-approved rules, but **bulk TRACE redistribution is restricted**, and the uncapped Academic/Enhanced TRACE file carries a WRDS/FINRA license. Rule of thumb: the *delayed, capped public view* is free to quote; any *panel* of corporate trades you regress on should come from the licensed WRDS file on Hopper (CONVENTIONS §5).

## Gotchas

- **The yield curve is *par* yields, not spot/zero rates.** For multi-year discounting you bootstrap a zero curve from the par curve — quoting the 10-year par yield as if it were the 10-year spot rate is a beginner error.
- **TRACE size is capped.** The public feed shows "1MM+" or "5MM+" for large trades, so you cannot sum reported volume and get true volume. Do not compute "total traded" from the free feed.
- **TRACE is delayed and bonds barely trade.** Most bonds go days without a print; a "stale" last price is the norm, not a data error. This illiquidity is the lesson, not a nuisance.
- **CUSIP, not ticker.** A company has one stock ticker but dozens of bond CUSIPs (different maturities/coupons). You must aggregate to the issuer yourself.
- **CMT tenors changed over time.** The 20-year was discontinued (2002) then reintroduced (2020); the 4-month was added in 2022. A long time series has structural gaps — `[CHECK]` before charting a single tenor across decades.

## First 10 rows (illustrative schema sketch — not real values)

*TreasuryDirect auctions (Fiscal Data API), shape only:*

| cusip | security_type | auction_date | maturity_date | high_yield | bid_to_cover_ratio | offering_amt |
|---|---|---|---|---|---|---|
| 912797XX1 | Bill | 2026-05-21 | 2026-08-20 | 5.210 | 2.84 | 80000000000 |
| 91282CXX3 | Note | 2026-05-14 | 2036-05-15 | 4.382 | 2.51 | 42000000000 |
| … | … | … | … | … | … | … |

*Daily Treasury par yield curve (one row per date), shape only:*

| date | dgs1mo | dgs3mo | dgs2 | dgs5 | dgs10 | dgs30 |
|---|---|---|---|---|---|---|
| 2026-05-26 | 5.31 | 5.22 | 4.61 | 4.20 | 4.39 | 4.71 |
| … | … | … | … | … | … | … |

*FINRA TRACE public print (per trade, size capped), shape only:*

| trade_datetime | cusip | symbol | price | yield | size_indicator |
|---|---|---|---|---|---|
| 2026-05-26 14:31:07 | 037833XX2 | AAPL4.xx | 98.412 | 4.55 | 1MM+ |
| … | … | … | … | … | … |

## Which chapter / lab / capstone uses it

- **Daily Treasury Yield Curve** is the risk-free anchor for **Capstone 5 (FRED Macro Event Study)** and any discounting/term-premium discussion; the FRED `DGSxx` route is the reproducible path.
- **TreasuryDirect auctions** support fixed-income worked examples and the bid-to-cover "demand for safety" intuition behind the risk-free rate.
- **FINRA TRACE** is the public window onto corporate-bond illiquidity, a contrast to equity markets (Week 2 returns work) and a feed into the credit-spread framing that connects to the municipal-market thread (`msrb-emma.md`) and **Mentor Session 5**. For any *panel*, swap the capped public feed for the licensed WRDS Enhanced TRACE file on GMU infrastructure.
