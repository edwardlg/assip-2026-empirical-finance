# Data Card — SEC EDGAR N-PORT (Fund Portfolio Holdings)

## Provider & what it is
**Form N-PORT** is the monthly portfolio-holdings report that registered investment companies — open-end mutual funds, exchange-traded funds (ETFs), and most closed-end funds — file with the SEC. It is the *fund-side* counterpart to the 13F: where 13F shows what large *managers* held in U.S. equities, N-PORT shows what a *fund* held across its **entire portfolio** — equities, bonds, derivatives, cash, repos, and structured products — with far more detail per position (fair value, percentage of net assets, maturity, coupon, counterparty for derivatives, and liquidity classification). The filing that becomes public is the **NPORT-P** ("P" for public): funds file monthly, but only the *third month of each quarter* is published, and on a lag. If a question is about *what a fund owns and how risky/illiquid that portfolio is*, N-PORT is the source — it is the granular holdings data that 13F cannot give you (no bonds, no shorts) and that fund prospectuses summarize only coarsely.

## Coverage
N-PORT replaced the old paper-era **N-Q** form and phased in around **2018–2019**; broad public availability of structured NPORT-P filings dates from roughly **2019 onward**. Coverage is the universe of SEC-registered funds (thousands of funds and share classes). Filing is monthly, but **only the quarter-end month's report is made public**, released after a delay (see Gotchas). **[CHECK]** the exact NPORT-P public-availability start quarter and the precise public-release lag before relying on either in a tight time-series design.

## Key identifiers (CIK / accession)
- **CIK** — the *registrant's* permanent EDGAR identifier (the fund family / trust), zero-padded to ten digits in URLs. Note a single registrant (trust) often houses *many* series (funds) and classes.
- **Accession number** (e.g. `0001145549-24-000123`) — the exact handle for one NPORT-P filing.
- **Series ID** and **Class ID** (EDGAR codes like `S000012345` / `C000067890`) — these identify the specific *fund* and *share class* within the registrant; getting these right is essential because the registrant CIK alone is too coarse.
- On the holdings side, securities carry **CUSIP**, **ISIN**, and increasingly **LEI** for the issuer; CUSIP is a licensed identifier (same caveat as the 13F card).

## Access path
**Free and public, no key.** Same **fair-access rule** as all of EDGAR: every request carries a `User-Agent` header naming you and your email, and you stay under **10 requests/second** aggregated across scripts; a missing User-Agent returns `403`.

```python
import os
from edgar import Company, set_identity
set_identity(os.environ["SEC_USER_AGENT"])        # e.g. "Priya Nair priya@gmu.edu"

fund     = Company("0001145549")                   # the registrant (trust), by CIK
filings  = fund.get_filings(form="NPORT-P")        # public monthly/quarter-end holdings reports
latest   = filings.latest()
holdings = latest.obj()                            # parsed holdings: name, cusip, value, pct_net_assets
```

Low-level `requests` route to the structured XML, polite-sleeping through a loop:

```python
import requests, time
HEADERS = {"User-Agent": os.environ["SEC_USER_AGENT"]}
# resolve the NPORT-P filing folder, then fetch the primary_doc XML (the holdings instance)
r = requests.get(nport_xml_url, headers=HEADERS, timeout=60); r.raise_for_status()
# parse r.content -> general info block + an <invstOrSec> list (one element per holding)
time.sleep(0.15)                                   # ~7 req/s, under the 10/s ceiling
```

The reveal: N-PORT is **structured XML** with a rich, deeply nested schema — a top "general information" block (fund-level totals, returns, flows) plus a long list of holding elements, each with sub-blocks for debt terms, derivative legs, and liquidity. The richness is the point and the trap: it is the most detailed *public* holdings data available, but the XML is large and nested, so parse the specific sub-elements you need rather than flattening blindly.

## License & note
**FREE / public domain.** No copyright, no license, no GMU-infrastructure restriction — cache, commit, and share freely (size permitting; N-PORT files are large, so treat like raw data and cache to `data/raw/edgar/` with the pull script + log committed). The standard caveat: **CUSIP/ISIN identifiers** carried in the holdings are licensed in their full mapped form — use them inside your analysis, do not redistribute a security master built from them.

## Gotchas
- **Monthly filed, quarterly published, lagged.** Funds file every month, but only the **third month of each quarter** is made public, and the public release comes **after a delay** (historically ~60 days after quarter-end). So the holdings you can see are stale and quarterly-spaced, not monthly — a look-ahead trap if you assume monthly public granularity.
- **Series/Class, not just CIK.** One registrant trust files for many funds; you must select the right **Series ID** (and sometimes Class) or you mix portfolios. This is the single most common N-PORT mistake.
- **Schema depth and amendments.** Derivative and debt sub-blocks are intricate; liquidity-classification fields changed by rule over time. Amendments (NPORT-P/A) correct earlier filings — pin the accession number.
- **Valuation date vs. filing date.** The holdings are "as of" the report period-end; the filing/publication date is much later. Use the period-end for the portfolio snapshot, never the filing date.
- **Confidential / delayed items.** Certain liquidity details have had confidential or delayed-disclosure treatment by rule — check the field availability for your sample years.

## Structure sketch (illustrative — not real values)
A flattened holdings extract for one fund-quarter:

| cik | series_id | accession_no | period_end | holding_name | cusip | value_usd | pct_net_assets | asset_cat |
|-----|-----------|--------------|------------|--------------|-------|-----------|----------------|-----------|
| 0001145549 | S000012345 | 0001145549-24-000123 | 2023-12-31 | US TREASURY N/B 4.0% 2030 | 91282CAB1 | 18,400,000 | 3.10 | DBT |
| 0001145549 | S000012345 | 0001145549-24-000123 | 2023-12-31 | APPLE INC | 037833100 | 12,900,000 | 2.17 | EC |
| 0001145549 | S000012345 | 0001145549-24-000123 | 2023-12-31 | MSFT 2.4% 2026 NOTE | 594918BP8 | 9,750,000 | 1.64 | DBT |
| 0001145549 | S000012345 | 0001145549-24-000123 | 2023-12-31 | S&P 500 FUT MAR24 | — | 4,200,000 | 0.71 | DE |

(*Illustrative.* CUSIPs, values, and asset categories are fabricated for shape; verify against the live NPORT-P XML. `asset_cat` codes: EC equity-common, DBT debt, DE derivative.)

## Where this is used
- **Chapter 7.2** §7.2.3 (SEC EDGAR) — N-PORT as the fund-holdings source within the EDGAR family, same User-Agent / 10-req-s / accession-pin discipline as the other filings.
- Fund-portfolio and fund-risk research questions (portfolio liquidity, bond exposure, derivative use, ETF holdings) and any capstone or extension studying mutual-fund/ETF behavior — the granular complement to the **13F** card (which covers manager-level U.S.-equity longs only).
- Priya's climate-exposure angle extended to fund portfolios (which funds hold climate-exposed issuers, and how illiquid those positions are).
