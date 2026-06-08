# Data Card — SEC EDGAR 10-K / 10-Q (Annual & Quarterly Reports)

## Provider & what it is
The U.S. Securities and Exchange Commission (SEC) runs **EDGAR** (Electronic Data Gathering, Analysis, and Retrieval), the public archive where every domestic public company files its mandatory disclosures. The **10-K** is the comprehensive *annual* report: audited financial statements plus the long prose sections — Item 1 (Business), Item 1A (Risk Factors), Item 7 (Management's Discussion and Analysis, "MD&A"), and Item 7A (market risk). The **10-Q** is the lighter *quarterly* report filed for Q1–Q3, with *unaudited* condensed financials and a shorter narrative. Together they are the workhorse of text-based and fundamentals-based finance research: one document carries both the numbers (revenue, assets, debt) and the words (how management frames risk and performance). This is the source behind Priya's "climate-risk language in insurer 10-Ks" idea and Week 6's reader's guides on 10-K text (Hoberg–Phillips TNIC, Loughran–McDonald sentiment).

## Coverage
EDGAR holds electronic filings from **1993–1994 to the present**; mandatory electronic filing phased in over 1993–1996, so coverage before ~1996 is partial. Roughly every U.S.-listed operating company files a 10-K annually and three 10-Qs per year. Foreign private issuers file a **20-F** (annual) and **6-K** (interim) instead — a trap if you assume everyone files 10-Ks. Smaller reporting companies get scaled disclosure but still file the same form types. **[CHECK]** the exact 1993-vs-1994 cutoff for the earliest fully-electronic filings if your sample reaches that far back.

## Key identifiers (CIK / accession)
- **CIK** (Central Index Key): EDGAR's *permanent* company identifier, an integer zero-padded to ten digits in URLs (`0000320193` = Apple). Unlike a ticker, it never changes on rename or re-listing.
- **Accession number**: identifies one specific filing, formatted `0000320193-23-000106`. This is the pin that makes a citation exact — see Gotchas on amendments.
- A ticker maps to a CIK through EDGAR's `company_tickers.json`. Mapping CIK onward to CRSP's PERMNO or Compustat's GVKEY is a separate crosswalk (Chapter 7.4), not something EDGAR gives you.

## Access path
EDGAR is **free and public — no API key, no registration.** What it *does* require is the SEC **fair-access rule**: every HTTP request must carry a descriptive `User-Agent` header with your name and email, e.g. `"Priya Nair priya@gmu.edu"`. A missing or generic User-Agent earns a `403 Forbidden`. The documented rate ceiling is **at most 10 requests/second**, aggregated across all your scripts; exceed it and your IP is throttled.

High-level route — the `edgartools` package wraps EDGAR's messy URLs into objects:

```python
from edgar import Company, set_identity
set_identity("Priya Nair priya@gmu.edu")     # the fair-access identity; read from env in real code

co = Company("AAPL")
tenk = co.get_filings(form="10-K").latest()   # most recent annual report
mdna = tenk.markdown()                         # full text, including MD&A and risk factors
fin  = tenk.financials                         # structured XBRL financials (see the XBRL card)
```

Low-level route — plain `requests` against EDGAR's submissions endpoint when you want one JSON file and no dependency:

```python
import os, requests, time
HEADERS = {"User-Agent": os.environ["SEC_USER_AGENT"]}   # e.g. "Priya Nair priya@gmu.edu"
cik = "0000320193"
url = f"https://data.sec.gov/submissions/CIK{cik}.json"   # filing index for the company
resp = requests.get(url, headers=HEADERS, timeout=30); resp.raise_for_status()
filings = resp.json()                                      # form types, accession numbers, dates
time.sleep(0.15)                                           # ~7 req/s, comfortably under 10/s
```

The trick `edgartools` hides: a filing is a *folder* of documents (the primary HTML, exhibits, the XBRL instance), addressed by CIK and accession number at `https://www.sec.gov/Archives/edgar/data/<cik>/<accession-no-dashes>/`. For large loops, prefer `edgartools` — it builds in the politeness throttling for you.

## License & note
**FREE / public domain.** SEC filings carry no copyright and no license restriction — unlike CRSP/Compustat, this data may be cached, committed, and shared. The only obligation is operational: identify yourself (User-Agent) and stay under 10 req/s. There is no GMU-infrastructure rule here. The practical limit is *size*, not law: full-text caches grow fast, so store raw HTML/text under a `data/raw/edgar/` directory and commit only if size permits.

## Gotchas
- **Amendments.** A 10-K can be amended as a **10-K/A**, and a 10-Q as **10-Q/A**. "Apple's FY2023 10-K" is ambiguous; accession `0000320193-23-000106` is exact. Always pin and record the accession number, and decide explicitly whether you use the original or the amendment.
- **Boilerplate and incorporation by reference.** Large stretches of a 10-K — especially Item 1A risk factors — are repeated near-verbatim year to year, and items can be *incorporated by reference* from the proxy (DEF 14A) rather than printed, so the section you want may not be in the document you pulled.
- **Parsing.** Modern filings are HTML with inline XBRL tags woven in; older ones are plain text or crude HTML. Naive `BeautifulSoup` stripping leaves table gibberish and XBRL artifacts. Extract section-by-section (by Item heading), not by blind tag-stripping, and expect to clean.
- **10-Q financials are unaudited** and use condensed statements; do not treat a 10-Q balance sheet as comparable in rigor to the audited 10-K.

## Structure sketch (illustrative — not real values)
A "filings index" table for one company, the shape you iterate over:

| cik | accession_no | form | filing_date | period_of_report | primary_doc |
|-----|--------------|------|-------------|------------------|-------------|
| 0000320193 | 0000320193-23-000106 | 10-K | 2023-11-03 | 2023-09-30 | aapl-20230930.htm |
| 0000320193 | 0000320193-23-000077 | 10-Q | 2023-08-04 | 2023-07-01 | aapl-20230701.htm |
| 0000320193 | 0000320193-23-000064 | 10-Q | 2023-05-05 | 2023-04-01 | aapl-20230401.htm |
| 0000320193 | 0000320193-23-000006 | 10-Q | 2023-02-03 | 2022-12-31 | aapl-20221231.htm |
| 0000320193 | 0000320193-22-000108 | 10-K | 2022-10-28 | 2022-09-24 | aapl-20220924.htm |

(*Illustrative.* Real accession numbers, dates, and document names differ; verify against the live filing index.)

## Where this is used
- **Week 6** opening narrative ("When the data is words") and the text reader's guides — Hoberg–Phillips (Ch 6.2, 10-K cosine similarity) and Loughran–McDonald (Ch 6.3, finance sentiment dictionaries).
- **Chapter 7.2** (Data Acquisition in Practice) §7.2.3 — the narrated EDGAR tour this card is the spec sheet for.
- Priya's running example (climate-risk 10-K language linked to returns) and any capstone using disclosure text or fundamentals.
