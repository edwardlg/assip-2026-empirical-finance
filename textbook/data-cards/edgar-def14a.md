# Data Card — SEC EDGAR DEF 14A (Proxy Statements)

## Provider & what it is
A **DEF 14A** is the *definitive proxy statement* a U.S. public company files with the SEC ahead of its shareholder meeting (the "DEF" means definitive, as opposed to a preliminary **PRE 14A**). It is the single richest public document for **corporate governance and executive compensation**. Inside one DEF 14A you find: the board's director nominees and their independence, committee structure (audit, compensation, nominating), the **Summary Compensation Table** (CEO and named-executive-officer salary, bonus, stock and option awards, total pay), the **pay-versus-performance** disclosure, beneficial-ownership tables (who owns >5%), the matters up for a vote (say-on-pay, director elections, auditor ratification), and related-party transactions. If a research question involves *who runs the firm and how they are paid*, this is the source. It is the natural companion to the 10-K, which often *incorporates by reference* its governance and compensation items from the proxy rather than printing them.

## Coverage
EDGAR holds proxy statements from the mid-1990s to the present, filed annually by essentially every U.S.-listed operating company that holds a shareholder meeting. Disclosure content has *grown* over time by rule: the modern executive-compensation tables date from the SEC's **2006** compensation-disclosure overhaul, **say-on-pay** votes arrived with Dodd–Frank (votes from **2011**), and the **pay-versus-performance** table is newer still (filings beginning **fiscal 2022 / 2023 proxy season**). A panel spanning these dates is therefore *not* uniformly structured. **[CHECK]** the exact first proxy season for the pay-versus-performance table before relying on it in early years.

## Key identifiers (CIK / accession)
- **CIK** — the filer's permanent EDGAR company identifier, zero-padded to ten digits in URLs.
- **Accession number** (e.g. `0000320193-24-000007`) — the exact handle for one proxy filing; a firm files roughly one DEF 14A per year, but pin it anyway because preliminary (PRE 14A) and additional soliciting materials (DEFA14A) clutter the index.
- The **filing date** and the meeting date inside the body matter for any event study around the annual meeting or a contested vote.
- There is no person-level executive identifier in the filing itself; named executives are matched by name (messy), or you cross to a licensed database like Execucomp (WRDS, GMU-only) — a Chapter 7.4 crosswalk.

## Access path
**Free and public, no key.** Same **fair-access rule** as all of EDGAR: every request carries a `User-Agent` header with your name and email, and you stay under **10 requests/second** aggregated across scripts. Missing User-Agent returns `403`.

```python
from edgar import Company, set_identity
set_identity("Maya Rodriguez maya@gmu.edu")      # fair-access identity; read from env in real code

co     = Company("KO")
proxy  = co.get_filings(form="DEF 14A").latest()  # note the SPACE in the form name
text   = proxy.markdown()                          # full proxy text, all tables and narrative
```

Low-level `requests` route, polite-sleeping through a loop:

```python
import os, requests, time
HEADERS = {"User-Agent": os.environ["SEC_USER_AGENT"]}
url = f"https://data.sec.gov/submissions/CIK{int(cik):010d}.json"
r = requests.get(url, headers=HEADERS, timeout=30); r.raise_for_status()
# filter r.json()['filings']['recent'] where form == 'DEF 14A'
time.sleep(0.15)                                  # ~7 req/s, under the 10/s ceiling
```

The reveal: the compensation *numbers* you want live in HTML tables embedded in the proxy, and — unlike the 10-K's financial statements — they are **not reliably XBRL-tagged**, so you usually parse the HTML table directly rather than getting clean structured facts. Pay-versus-performance and a few items have structured tagging in recent years; the older Summary Compensation Table generally does not.

## License & note
**FREE / public domain.** No copyright, no license, no GMU-infrastructure rule — cache, commit, and share freely (size permitting). The compensation tables are public, so a governance/comp study built purely on DEF 14A data is fully re-runnable by any reviewer — the kind of clean reproducibility the data-acquisition chapter prizes. The only caveat is that *cleaned, panelized* comp data (Execucomp) is a licensed WRDS product; if you use it for convenience, the GMU-infrastructure rule applies to *that* file, not to the underlying free proxies.

## Gotchas
- **Form-name spaces and siblings.** The form is literally `DEF 14A` (with a space). Do not confuse it with **PRE 14A** (preliminary), **DEFA14A** (additional soliciting material), **DEFR14A** (revised), or **DEFC14A** (contested/proxy-fight). Filtering loosely pulls in noise.
- **Tables, not text, carry the data.** The Summary Compensation Table is an HTML table with merged cells, footnotes, and multi-year rows; naive text extraction scrambles columns. Parse the table structure, and read the footnotes — option-award "fair value" assumptions and one-time grants live there.
- **Boilerplate.** Governance prose ("the Board believes…", director-independence language) is heavily templated across firms and dominates a naive bag-of-words.
- **Incorporation by reference goes both ways.** The 10-K may pull comp/governance from the proxy; conversely the proxy may reference the 10-K. Track which document actually *contains* the item you cite.
- **Restated / additional materials** can supersede figures; pin the accession number and prefer the definitive DEF 14A over later DEFA14A soliciting addenda.

## Structure sketch (illustrative — not real values)
A flattened Summary Compensation extract — the shape a comp study builds:

| cik | accession_no | fiscal_year | executive | role | salary | stock_awards | option_awards | total_comp |
|-----|--------------|-------------|-----------|------|--------|--------------|---------------|------------|
| 0000021344 | 0000021344-24-000007 | 2023 | J. Doe | CEO | 1,600,000 | 14,200,000 | 3,500,000 | 22,800,000 |
| 0000021344 | 0000021344-24-000007 | 2023 | A. Smith | CFO | 850,000 | 5,100,000 | 1,200,000 | 8,400,000 |
| 0000021344 | 0000021344-24-000007 | 2022 | J. Doe | CEO | 1,550,000 | 13,000,000 | 3,100,000 | 20,900,000 |
| 0000021344 | 0000021344-24-000007 | 2022 | A. Smith | CFO | 820,000 | 4,700,000 | 1,000,000 | 7,600,000 |

(*Illustrative.* Names, accession number, and dollar figures are fabricated for shape; verify against the live proxy.)

## Where this is used
- **Chapter 7.2** §7.2.3 (SEC EDGAR) — proxy statements as a governance/compensation source, same fair-access and accession-pinning discipline as 10-Ks.
- Governance- and pay-focused research questions (board independence, CEO pay-for-performance, say-on-pay outcomes) and any capstone or extension that links executive compensation or board structure to firm outcomes.
- Companion to the **10-K / 10-Q** card (Items often incorporated by reference) and to the **XBRL** card (proxy tables are largely *not* XBRL, in deliberate contrast).
