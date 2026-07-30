# Data Card — SEC EDGAR 8-K (Material Events)

## Provider & what it is
The **8-K** is the SEC's "something just happened" form. Where the 10-K and 10-Q are scheduled annual and quarterly reports, the 8-K is filed *on demand* whenever a material corporate event occurs — and it must usually be filed **within four business days** of the event. That timeliness is exactly what makes it the natural raw material for an **event study**: the filing date is a sharp, machine-readable timestamp for "new information hit the market." Each 8-K is organized by numbered **Items** that name the event type — Item 2.02 (results of operations / earnings release), Item 5.02 (departure or appointment of directors and officers), Item 1.01 (entry into a material agreement), Item 2.01 (completion of an acquisition), Item 8.01 (other events), and so on. This is the source behind **Capstone 4 — SEC 8-K Text Classification**, where you classify the event type from the text and study the return reaction around the filing.

## Coverage
EDGAR holds 8-Ks from the mid-1990s to the present, filed by essentially every U.S.-listed operating company. A typical large firm files anywhere from a handful to dozens of 8-Ks a year. The modern Item-numbering scheme (the 1.0x / 2.0x / 5.0x structure) dates from the SEC's **August 2004** 8-K overhaul; filings before that use an older, coarser item taxonomy, so a sample spanning 2004 is *not* coded consistently. **[CHECK]** the exact pre-2004 item codes if your study reaches back that far.

## Key identifiers (CIK / accession)
- **CIK** — the filer's permanent EDGAR company identifier, zero-padded to ten digits in URLs.
- **Accession number** (e.g. `0000320193-23-000045`) — the exact handle for one 8-K. Because a firm files many 8-Ks per year, the accession number, not "the 2023 8-K," is the only unambiguous reference.
- **Item numbers** inside the filing are the *event* identifiers (2.02, 5.02, …); they are the labels your classifier in Capstone 4 either predicts or validates against.
- The **filing date** (and, for some events, an event date in the body) is the timestamp your event window centers on.

## Access path
**Free and public, no key.** Same **fair-access rule** as all of EDGAR: every request carries a `User-Agent` header naming you and your email, and you stay under **10 requests/second** aggregated across scripts. A missing User-Agent returns `403`.

```python
from edgar import Company, set_identity
set_identity("Sam Okafor sam@gmu.edu")           # fair-access identity; read from env in real code

co = Company("TSLA")
eightks = co.get_filings(form="8-K")              # all 8-Ks for the company
recent  = eightks.head(20)
text    = recent[0].markdown()                    # full text of one 8-K, items included
```

Or the low-level `requests` route, sleeping between calls so a loop stays polite:

```python
import os, requests, time
HEADERS = {"User-Agent": os.environ["SEC_USER_AGENT"]}
for cik in cik_list:
    url = f"https://data.sec.gov/submissions/CIK{int(cik):010d}.json"
    r = requests.get(url, headers=HEADERS, timeout=30); r.raise_for_status()
    # filter r.json()['filings']['recent'] where form == '8-K' ...
    time.sleep(0.15)                              # ~7 req/s, under the 10/s ceiling
```

For *finding* event filings by language, the **full-text search** endpoint (EFTS, 2001–present) returns filings whose text matches a query — useful to assemble a candidate set before you pull and classify. `edgartools` exposes the same throttling-aware machinery, so prefer it for large jobs.

## License & note
**FREE / public domain.** No copyright, no license, no GMU-infrastructure restriction — cache and commit freely (size permitting). Note for the AI module: when you feed 8-K text to an LLM classifier, the *filings* are public, but your **API calls to a commercial LLM are not free of obligations** — log them, disclose AI use per the capstone's responsible-use checklist (Reading Guide Pack 6), and never paste licensed data (none here) into a vendor. The reveal: the data is free, but reproducibility of a *stochastic* LLM label is not automatic — pin the model version and temperature, and cache the model's output alongside the raw filing.

## Gotchas
- **Multiple events per filing.** One 8-K can carry several Items at once (e.g. 2.02 *and* 9.01 exhibits). Your label is therefore multi-label, not single-label — a classic Capstone 4 modeling decision, not a bug.
- **Earnings releases hide in Exhibit 99.1.** Item 2.02 8-Ks usually point to the actual press release as **Exhibit 99.1**; the body of the 8-K is a one-line pointer, and the *content* lives in the exhibit. Pull the exhibit, not just the cover.
- **Boilerplate cover language** ("furnished, not filed" disclaimers, forward-looking-statement safe-harbor paragraphs) repeats across firms and will dominate a naive bag-of-words unless you strip it.
- **Amendments (8-K/A)** correct or supplement an earlier 8-K; pin the accession number and decide which you study.
- **Filing-time vs. event-time.** The four-business-day window means the *filing date* can lag the *event*; for a tight event study, read the body for the event date and be explicit about which clock you use (a look-ahead trap).

## Structure sketch (illustrative — not real values)
A parsed 8-K event table, the shape Capstone 4 builds:

| cik | accession_no | filing_date | items | exhibit_991 | event_label |
|-----|--------------|-------------|-------|-------------|-------------|
| 0001318605 | 0001318605-23-000045 | 2023-10-18 | 2.02, 9.01 | yes | earnings |
| 0001318605 | 0001318605-23-000051 | 2023-11-02 | 5.02 | no | exec_change |
| 0001318605 | 0001318605-23-000060 | 2023-12-07 | 1.01, 9.01 | no | material_agreement |
| 0001318605 | 0001318605-24-000003 | 2024-01-24 | 8.01 | no | other |
| 0001318605 | 0001318605-24-000009 | 2024-02-12 | 2.01 | yes | acquisition_complete |

(*Illustrative.* Accession numbers, dates, and item combinations are fabricated for shape; verify against live filings.)

## Where this is used
- **Capstone 4 — SEC 8-K Text Classification** — classify event type from 8-K text with out-of-sample validation, then study the return reaction around the filing date.
- **Week 6 AI module** (Ch 6.5, the AI Co-Pilot) and Reading Guide Pack 6 — LLM text classification with OOS validation, leakage audits, and the responsible-use/disclosure checklist that Capstone 4 must satisfy.
- **Chapter 7.2** §7.2.3 (SEC EDGAR) — the access pattern, fair-access rule, and accession-number pinning this card details.
