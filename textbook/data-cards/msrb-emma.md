# Data Card — MSRB EMMA (Municipal securities disclosures and trades)

## Provider & what it is

The **MSRB** (Municipal Securities Rulemaking Board) runs **EMMA** — the Electronic Municipal Market Access system, the official public repository for the U.S. **municipal bond** market. When a state, city, county, school district, water authority, or other government body borrows by issuing a "muni," its disclosure and trading record lives on EMMA. It is the muni market's EDGAR.

EMMA publishes two things you will use:

- **Disclosures** — the **official statement** (the muni's prospectus: the bonds, issuer, security, use of proceeds), plus ongoing **continuing-disclosure** filings: audited financials, material-event notices (rating changes, defaults, calls). The accounting side of a muni.
- **Trades** — the secondary-market **trade record**: every reported municipal transaction with price, par amount, and time, via the MSRB's Real-Time Transaction Reporting System (RTRS). This is what a muni actually traded at — and, against a benchmark, what *yield* the market demanded of that borrower.

The reveal that motivates the muni thread: a corporate bond's yield reflects one firm's credit risk, but a muni yield is a window onto **how expensively a government can borrow** — a "cost of credit" that varies across issuers and time in ways that are live research (Prof. Gao's *Rainbow of Credits*). EMMA is where that price lives, in public, for free.

## Coverage

- **Trades:** real-time municipal trade reporting from the mid-2000s (RTRS launched 2005; earlier trade data exists in less granular form). Coverage is the reported secondary market, which for munis is **thin and episodic** — many bonds trade rarely. `[CHECK]` exact RTRS start date and pre-2005 trade availability.
- **Disclosures:** EMMA became the centralized disclosure portal in **2009**; official statements and continuing disclosures are broadly available from then, with some earlier documents. `[CHECK]` earliest reliable disclosure year.
- **Universe:** essentially the whole U.S. muni market — roughly a million-plus distinct outstanding CUSIPs across tens of thousands of issuers (states, localities, authorities, school and water districts). Far more *issuers* than the corporate market, and far less liquid per issue.

## Key identifiers

- **CUSIP** (9-character) identifies a specific muni *issue/maturity*. A single bond deal is sold as a *serial* — many CUSIPs, one per maturity — so one borrowing event spans dozens of CUSIPs.
- **Issuer** — the governmental borrower; the link from CUSIP to issuer (and from issuer to state/sector) is the join you need for any cross-issuer study, and it is not always clean.
- **Trade timestamp**, **price**, **par traded**, and a **trade-type flag** (customer-buy, customer-sell, inter-dealer) on the trade side.
- There is no single tidy primary key spanning disclosures and trades except the CUSIP, and disclosures often attach at the *deal/official-statement* level rather than per-CUSIP — reconciling the two is real work.

## Access path

- **EMMA website** (`https://emma.msrb.org`) is the primary public access point: search by issuer or CUSIP, read official statements, view per-bond trade history. **Free, no account** for browsing.
- **Bulk access is the catch.** MSRB offers **no** simple open public API for bulk trade history the way Treasury or FDIC do. Bulk historical trade and reference datasets come through **MSRB subscription/data products** (some mirrored in academic services); the free site is built for one-bond lookups, not large downloads. A real cross-issuer panel uses a licensed muni dataset (MSRB historical files or a vendor feed) on GMU infrastructure (CONVENTIONS §5). `[CHECK]` current MSRB API/bulk-product names and terms, and whether the camp container mirrors a muni trade file.

```python
# EMMA has no clean free bulk API; the disciplined pattern for the camp is to treat
# the public site as a per-CUSIP lookup and use a LICENSED muni trade file (on Hopper /
# the container's read-only mount) for any panel. Pseudocode for the per-bond route:
#
#   1. Search emma.msrb.org by issuer  ->  list of CUSIPs for the deal
#   2. For a CUSIP, pull its trade history and official statement (manually or via the
#      documented endpoint for your pinned vintage)  [CHECK: endpoint + terms]
#   3. Aggregate trades to an issue-level or issuer-level yield/price series
#
# Never scrape the public site for a large panel; use the licensed file instead.
```

## License & note

**Free to browse; restricted for bulk.** The EMMA *public website* is free and open to read — official statements, disclosures, and per-bond trade history cost nothing to view, and the disclosures themselves are public records. But **bulk redistribution of MSRB trade data is governed by MSRB terms**, and large historical datasets sit behind MSRB subscription/data products. So: quote what you read on EMMA freely with a citation; build any *panel* you regress on from a licensed source that stays on GMU infrastructure, and pin its vintage. `[CHECK]` exact MSRB data-product license terms before redistributing anything beyond a screenshot or a cited figure.

## Gotchas

- **Munis barely trade.** Like corporate bonds (see `treasury-finra.md`) but worse — many CUSIPs go weeks or months without a print. A "last price" is often stale; sparse, irregular trading is the data, not a glitch. Yields must be inferred carefully, often from infrequent customer trades.
- **One deal, many CUSIPs.** A serial issue fragments one borrowing into dozens of maturities/CUSIPs. To study the *issuer's* cost of borrowing you must aggregate across CUSIPs within a deal — getting this wrong double-counts or mis-weights.
- **No clean free bulk API.** Unlike Treasury/FDIC/HMDA, EMMA is built for one-bond lookups. A cross-issuer panel needs a licensed file; do not plan a capstone around scraping the public site.
- **Tax status confounds yield.** Muni interest is often federally (and sometimes state) tax-exempt, so muni yields are *not* comparable to taxable Treasury/corporate yields without a tax adjustment. Comparing a raw muni yield to a Treasury yield is a beginner error.
- **Issuer mapping is messy.** CUSIP-to-issuer-to-sector linkage is not always clean; the same governmental borrower can appear under several issuer descriptions.

## First 10 rows (illustrative schema sketch — not real values)

*Trade records (per CUSIP), shape only — note the irregular timestamps (illiquidity):*

| cusip | trade_datetime | trade_type | price | yield | par_traded |
|---|---|---|---|---|---|
| 64971QXX4 | 2026-04-02 11:14:08 | customer_buy | 101.235 | 3.41 | 50000 |
| 64971QXX4 | 2026-02-19 14:52:30 | inter_dealer | 100.980 | 3.47 | 25000 |
| 64971QXX4 | 2025-11-30 10:07:55 | customer_sell | 100.410 | 3.55 | 100000 |
| … | … | … | … | … | … |

*Issuer / disclosure reference (per deal), shape only:*

| issuer_name | state | sector | dated_date | par_amount | official_statement_id |
|---|---|---|---|---|---|
| Example County School District | VA | Education | 2025-09-15 | 48500000 | OS-EX-000123 |
| Sample City Water Authority | MD | Utility | 2024-06-01 | 22000000 | OS-EX-000087 |
| … | … | … | … | … | … |

*Issuer-level cost-of-borrowing series you would build, shape only:*

| issuer_name | state | year | avg_offering_yield | n_deals |
|---|---|---|---|---|
| Example County School District | VA | 2025 | 3.42 | 2 |
| Sample City Water Authority | MD | 2024 | 3.18 | 1 |
| … | … | … | … | … |

## Which chapter / lab / capstone uses it

- **Mentor Session 5 — "Anatomy of a JF paper,"** tied to the **Rainbow of Credits** municipal-borrowing working paper (Gao, Liu & Wang, AEA 2025; target *JF*). The session walks students through a live paper built on muni issuance and secondary-market trade records "of the kind assembled from the MSRB," and EMMA is the public face of exactly that data. This card is the reference for *where that data lives and why it is hard*.
- **The muni-borrowing research thread** more broadly (revisited in Mentor Session 7's project pipeline): municipal cost-of-credit as an outcome, with the institutional features above (illiquidity, serial CUSIPs, tax status) as the texture that makes it a real research setting rather than a clean toy.
- It sits with the other fixed-income public sources — `treasury-finra.md` (the risk-free curve + corporate tape) — to give students the full credit-market picture: government risk-free, corporate credit, and municipal credit, each with its own messiness, each free to *read* and licensed to *bulk*.
