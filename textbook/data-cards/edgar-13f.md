# Data Card — SEC EDGAR 13F (Institutional Holdings, the Free Path)

## Provider & what it is
**Form 13F** is the quarterly report that institutional investment managers with over **\$100 million** in qualifying U.S. equity assets under management must file with the SEC, disclosing their **long positions** in 13(f)-listed securities: which stocks, how many shares, and the market value, as of quarter-end. It is how you observe what the big funds *held*. The form filed each quarter is the **13F-HR** (holdings report); a **13F-NT** is a notice that the holdings are reported by another filer. This card covers the **free, public path via SEC EDGAR** — deliberately contrasted with the **licensed, cleaned path** (Thomson Reuters / Refinitiv "s34" files on WRDS), because the choice between them is the whole point. EDGAR gives you the *exact filing*; Thomson gives you a *cleaned historical panel* with a license attached. This source anchors **Capstone 2 — Common Ownership from 13F** (ties to Gao, Han, Kim & Pan 2024, *JCF* 84:102520 — overlapping institutional ownership along the supply chain and earnings management of supplier firms).

## Coverage
EDGAR holds 13F filings from the mid-1990s to the present, one per qualifying manager per quarter. The set of filers is the population of large institutions — mutual fund complexes, hedge funds, pensions, bank trust departments, insurers. A major change: since the SEC's **structured-data mandate (filings from 2013 onward)**, the holdings information table is an **XML** document, which is clean to parse; older filings embedded the table in free text or rough HTML and are far messier. **[CHECK]** the exact quarter the XML information-table requirement became mandatory if your sample reaches back before ~2013.

## Key identifiers (CIK / accession / CUSIP)
- **CIK** — the *manager's* permanent EDGAR identifier (Berkshire Hathaway's is `0001067983`), zero-padded to ten digits in URLs.
- **Accession number** (e.g. `0001067983-24-000004`) — the exact handle for one quarter's 13F-HR.
- **CUSIP** — the nine-character security identifier on each holding row; this is how you know *which stock* a position is. CUSIP is itself a **licensed identifier** in its full form — usable inside your analysis, but you may not redistribute a large CUSIP-to-name master file (CUSIP Global Services' license). Mapping CUSIP onward to PERMNO/GVKEY is a Chapter 7.4 crosswalk.
- The **period of report** (quarter-end date) and **filing date** matter because of the reporting lag (see Gotchas).

## Access path
**Free and public, no key** — it is just another EDGAR form. Same **fair-access rule**: every request carries a `User-Agent` header naming you and your email, and you stay under **10 requests/second** aggregated across scripts; a missing User-Agent returns `403`.

```python
import os
from edgar import Company, set_identity
set_identity(os.environ["SEC_USER_AGENT"])        # e.g. "Sam Okafor sam@gmu.edu"

mgr      = Company("0001067983")                   # Berkshire Hathaway, by CIK
filings  = mgr.get_filings(form="13F-HR")          # quarterly holdings reports
infotable = filings.latest().obj().infotable       # one row per holding: CUSIP, name, shares, value
```

Low-level `requests` route to the information-table XML, polite-sleeping through a loop of managers:

```python
import requests, time
HEADERS = {"User-Agent": os.environ["SEC_USER_AGENT"]}
# resolve the filing folder from the submissions JSON, then fetch the information-table XML
r = requests.get(infotable_xml_url, headers=HEADERS, timeout=30); r.raise_for_status()
# parse r.content as XML -> rows of (cusip, nameOfIssuer, shares, value, ...)
time.sleep(0.15)                                   # ~7 req/s, under the 10/s ceiling
```

The reveal — **EDGAR vs. Thomson/WRDS**: use EDGAR when you want *transparency and the exact filing as filed* (and you are willing to de-duplicate and clean yourself). Use the **Thomson/Refinitiv s34 files on WRDS** when you need a *clean, de-duplicated historical panel* with consistent manager identifiers — accepting the GMU-infrastructure rule and the licensed-data discipline that comes with WRDS (same access pattern as the CRSP/Compustat card). For a teaching project, the free EDGAR path is usually right.

## License & note
The **filings themselves are FREE / public** (EDGAR — cache, commit, share, size permitting). The **Thomson/Refinitiv panel is licensed** (WRDS, GMU-only, never committed to git). And **CUSIP is a licensed identifier**: keep CUSIPs inside your analysis to merge your own data, but do not publish a CUSIP master file. So a 13F study built from EDGAR XML is reproducible-by-rerun for the *filings*, while the *CUSIP mapping* is the one piece you must not redistribute.

## Gotchas — what 13F does *not* tell you
These are conceptual limits your identification must respect, not code bugs:
- **Long positions only.** No short positions, no most derivatives — so a 13F is *not* the manager's true net exposure.
- **45-day reporting lag.** The filing is due up to **45 days after quarter-end**, so holdings are stale when you see them. Treating a 13F as real-time positioning is a look-ahead error in reverse.
- **Confidential treatment.** Managers can request to delay or omit some positions, so a disclosed table can be *incomplete* — and later amendments may reveal them.
- **Manager identity drift and duplicates.** The same firm can file under related entities or amend (13F-HR/A); the raw EDGAR feed is not de-duplicated, which is exactly why the cleaned Thomson panel exists.
- **13(f) security list.** Only securities on the SEC's official 13(f) list are reportable; ordinary common stock is in, but many instruments are out.

## Structure sketch (illustrative — not real values)
The information-table rows for one manager-quarter:

| cik | accession_no | period | cusip | name_of_issuer | shares | value_usd_000 |
|-----|--------------|--------|-------|----------------|--------|---------------|
| 0001067983 | 0001067983-24-000004 | 2023-12-31 | 037833100 | APPLE INC | 905,560,000 | 174,300,000 |
| 0001067983 | 0001067983-24-000004 | 2023-12-31 | 060505104 | BANK OF AMERICA | 1,032,852,000 | 33,500,000 |
| 0001067983 | 0001067983-24-000004 | 2023-12-31 | 191216100 | COCA COLA CO | 400,000,000 | 23,600,000 |
| 0001067983 | 0001067983-24-000004 | 2023-12-31 | 166764100 | CHEVRON CORP | 126,093,000 | 18,800,000 |

(*Illustrative.* CUSIPs, share counts, and values are fabricated for shape; verify against the live information table.)

## Where this is used
- **Capstone 2 — Common Ownership from 13F** — constructing common-ownership measures and a disclosure/competition outcome (a student-track sibling of the anchor paper's earnings-management outcome); ties to Gao, Han, Kim & Pan (2024), "Overlapping institutional ownership along the supply chain and earnings management of supplier firms," *JCF*, 84:102520.
- **Chapter 7.2** §7.2.6 (13F) — the narrated EDGAR-vs-Thomson comparison this card is the spec sheet for, with the same User-Agent / 10-req-s / accession-pin discipline.
- Mentor Session 6 (Lei Gao) — supply-chain common ownership and disclosure, the research line this dataset supports.
