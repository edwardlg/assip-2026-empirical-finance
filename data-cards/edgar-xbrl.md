# Data Card — SEC EDGAR XBRL Financial Statement Data (Structured Financials)

## Provider & what it is
**XBRL** (eXtensible Business Reporting Language) is how the SEC turns the *numbers* inside filings — revenue, total assets, net income, EPS, cash and equivalents — into machine-readable, tagged data instead of prose you have to scrape. Every figure is wrapped in a standardized **tag** (a "concept" from the **US-GAAP taxonomy**, e.g. `Revenues`, `Assets`, `NetIncomeLoss`) with a value, a period or instant, and a unit. The SEC publishes this two ways: (1) the **XBRL Financial Statement Data Sets** — bulk, quarterly flat files (`num`, `sub`, `tag`, `pre`) covering *all* filers, ideal when you want a broad cross-section; and (2) the **`companyfacts` / `companyconcept` REST API** under `data.sec.gov`, which returns every tagged fact for *one* company as JSON, ideal when you want a few firms with no parsing. This is the structured-financials backbone for any fundamentals study — the free, public alternative to Compustat for the figures Compustat would standardize. It ties directly to Week 7's data-acquisition arc and to Priya's insurer-fundamentals need when WRDS is not in reach.

## Coverage
XBRL tagging was phased in by filer size around **2009–2011** and is now universal for U.S. operating companies' 10-Ks and 10-Qs; the bulk Financial Statement Data Sets run from roughly **2009 to the present**, refreshed quarterly. The `companyfacts` API returns the full tagged history the SEC holds for a given company. Coverage is the same population as the 10-K/10-Q filers. **[CHECK]** the exact first quarter of the bulk data sets and the smallest-filer XBRL phase-in date if your sample reaches into 2009–2011.

## Key identifiers (CIK / accession / tag)
- **CIK** — the company's permanent EDGAR identifier; the API path uses the ten-digit zero-padded form (`CIK0000320193`).
- **Accession number** — each tagged fact traces back to the specific filing (and amendment) it came from, so you can pin the source filing exactly.
- **Tag (concept)** — the US-GAAP (or DEI, or company-extension) element name, e.g. `RevenueFromContractWithCustomerExcludingAssessedTax`. The tag *is* the variable; choosing the right one is the central skill (see Gotchas).
- **Unit** (`USD`, `shares`, `USD/shares`) and **period** (a duration like FY2023, or an instant like 2023-09-30) qualify every value.

## Access path
**Free and public, no key.** Same **fair-access rule** as all of EDGAR: every request carries a `User-Agent` header with your name and email, and you stay under **10 requests/second** aggregated across scripts; a missing User-Agent returns `403`.

`companyfacts` for one firm, the cleanest route to structured numbers:

```python
import os, requests
HEADERS = {"User-Agent": os.environ["SEC_USER_AGENT"]}   # e.g. "Priya Nair priya@gmu.edu"
cik = "0000320193"                                         # Apple, zero-padded to 10 digits
url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
r = requests.get(url, headers=HEADERS, timeout=30); r.raise_for_status()
facts = r.json()                                          # nested: facts['us-gaap']['Assets']['units']['USD'] -> list
```

`companyconcept` for *one* tag across a firm's history (smaller payload):

```python
url = (f"https://data.sec.gov/api/xbrl/companyconcept/"
       f"CIK{cik}/us-gaap/Revenues.json")                # just the Revenues series
```

Or `edgartools`, which surfaces XBRL as tidy statements:

```python
from edgar import Company, set_identity
set_identity(os.environ["SEC_USER_AGENT"])
fin = Company("AAPL").get_filings(form="10-K").latest().financials   # income stmt, balance sheet, cash flow
```

For a broad cross-section, download the **quarterly Financial Statement Data Set** ZIP (the `num.txt` / `sub.txt` flat files) and load those rather than hitting the API thousands of times — targeted firms via API, whole-market via bulk files. The reveal: `companyfacts` hands you *every* tagged fact with no HTML parsing at all, which is why it is the antidote to scraping financial tables out of 10-K HTML.

## License & note
**FREE / public domain.** No copyright, no license, no GMU-infrastructure restriction — cache, commit, and share freely. This is the honest free substitute when CRSP/Compustat is unavailable: a fundamentals study built on XBRL `companyfacts` is fully re-runnable by any reviewer, since the data is public and the API is open. The trade-off versus Compustat is *standardization*, not access — see Gotchas.

## Gotchas — why XBRL is not quite Compustat
- **Tag drift and choice.** The same economic quantity can be reported under different tags across firms and years (`Revenues` vs. `RevenueFromContractWithCustomerExcludingAssessedTax` vs. `SalesRevenueNet`). There is no single "revenue" field; you must build a *priority list* of acceptable tags and fall back in order. This is the work Compustat does for you and XBRL does not.
- **Company extensions.** Firms can invent **custom (extension) tags** outside the standard taxonomy for line items, so a concept may simply not exist under the US-GAAP namespace for some filers.
- **Duplicate / overlapping facts.** `companyfacts` returns the *same* number reported in multiple filings (the FY2022 figure appears in both the 2022 and 2023 10-K as a comparative), each tied to a different accession. De-duplicate on (tag, period, unit) and prefer the original-period filing, or you double-count.
- **Period vs. instant.** Flow concepts (revenue, net income) carry a *duration*; stock concepts (assets, cash) carry an *instant*. Mixing them silently breaks ratios.
- **Restatements and amendments.** A later 10-K/A can re-tag a prior figure; pin the accession and decide whether you use as-originally-reported or as-restated.
- **No survivorship fix, no price data.** XBRL gives fundamentals only — no returns, no delisting handling. Pair it with a price source (CRSP, or yfinance for prototyping) for return-based work.

## Structure sketch (illustrative — not real values)
A flattened `companyfacts` extract — one tag, one unit, across periods:

| cik | tag | unit | start | end | val | fy | fp | accession_no |
|-----|-----|------|-------|-----|-----|----|----|--------------|
| 0000320193 | Assets | USD | — | 2023-09-30 | 352,583,000,000 | 2023 | FY | 0000320193-23-000106 |
| 0000320193 | Assets | USD | — | 2022-09-24 | 352,755,000,000 | 2022 | FY | 0000320193-22-000108 |
| 0000320193 | Revenues | USD | 2022-09-25 | 2023-09-30 | 383,285,000,000 | 2023 | FY | 0000320193-23-000106 |
| 0000320193 | NetIncomeLoss | USD | 2022-09-25 | 2023-09-30 | 96,995,000,000 | 2023 | FY | 0000320193-23-000106 |

(*Illustrative.* Tag names are real US-GAAP concepts; the values are fabricated for shape — verify against the live `companyfacts` JSON. Note the empty `start` for the instant concept `Assets` versus the duration for `Revenues`.)

## Where this is used
- **Chapter 7.2** §7.2.3 (SEC EDGAR — XBRL) — the structured-numbers route, `companyfacts` endpoint, and the User-Agent / 10-req-s discipline this card is the spec sheet for.
- **Chapter 7.4** (Building the Analysis Dataset) — XBRL fundamentals merged via CIK→PERMNO/GVKEY crosswalks, with the tag-priority and restatement discipline above.
- Fundamentals-based capstones and Priya's insurer-fundamentals work when WRDS/Compustat is out of reach; the structured complement to the prose-focused **10-K / 10-Q** card and the deliberately-*un*structured **DEF 14A** card.
