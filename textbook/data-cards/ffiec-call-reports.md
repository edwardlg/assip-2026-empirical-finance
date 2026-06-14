# Data Card — Call Reports (FFIEC)

## Provider & what it is

A **Call Report** — formally the *Consolidated Reports of Condition and Income*, regulatory forms
**FFIEC 031 / 041 / 051** — is the quarterly financial statement that essentially every U.S.
commercial bank and savings institution must file with its federal regulator. They are collected
through the **FFIEC** (Federal Financial Institutions Examination Council) and published free on
the **FFIEC Central Data Repository (CDR)** Public Data Distribution site. Here is the reveal: a
Call Report is a bank's balance sheet and income statement, but the line items are *standardized
across all banks* and identified by codes (the "MDRM" / RCFD–RCON series), so you can stack ten
thousand banks into one comparable panel — something free narrative filings cannot give you. This
is the raw material of bank-level empirical work: deposits, loans by type, charge-offs, net
interest income, capital ratios — every quarter, for the whole banking system, going back decades.
The form numbers reflect bank size and foreign offices (031 = with foreign offices, 041 = domestic
only, 051 = streamlined for smaller banks).

## Coverage

All FDIC-insured commercial banks and savings institutions, filed **quarterly** (as of March 31,
June 30, September 30, December 31). The CDR bulk download covers the modern electronic era;
historical Call Report data reaches back much further through the **Federal Reserve Bank of
Chicago**'s long-running archive and the FFIEC. [CHECK: the earliest quarter available in the CDR
bulk "Call Reports — Single Period" download vs. the Chicago Fed historical files.] This is *entity-
level* data — one set of figures per bank per quarter — not branch-level and not loan-level.

## Key identifiers

The primary key is the **RSSD ID** (often `IDRSSD` in the data files) — the Federal Reserve's
permanent, unique identifier for a financial institution in the National Information Center (NIC).
It is permanent across name changes and is the join key to other regulatory data (FR Y-9C, NIC
attributes, the Fed's structure files). Beware the trap: a bank's RSSD ID is **not** the same as its
parent holding company's RSSD ID — relating a subsidiary bank to its holding company is exactly the
crosswalk the FR Y-9C card and Chapter 7.4 handle, and it is out of scope here. Individual financial
line items are identified by **MDRM codes** — e.g. `RCFD2170` (total assets, consolidated) or
`RCON2170` (total assets, domestic offices); the `RCFD`/`RCON` prefix tells you consolidated vs.
domestic-only.

## Access path (download / API; no key required)

Call Reports are free and need **no API key**. Two paths:

```python
import os, io, zipfile, requests, pandas as pd

# Path A — FFIEC CDR bulk download (manual or scripted): the "Call Reports -- Single Period"
# tab-delimited ZIP for a given quarter, pulled from the CDR Public Data Distribution site.
# Save the raw ZIP to data/raw/ and read the period you need.
# url = "<FFIEC CDR bulk-download URL for 2024-12-31>"   # [CHECK exact CDR endpoint/params]
raw = "data/raw/ffiec_call_2024Q4.zip"
with zipfile.ZipFile(raw) as z:
    name = [n for n in z.namelist() if "Schedule RC" in n][0]   # pick the schedule you need
    rc = pd.read_csv(z.open(name), sep="\t", low_memory=False)

# Path B — the FFIEC CDR also exposes a SOAP/web-service API for programmatic pulls
# (it issues a free access token/credential you read from the environment, never hard-coded):
token = os.environ["FFIEC_CDR_TOKEN"]   # export FFIEC_CDR_TOKEN=...   [CHECK exact auth scheme]
```

For a camp project the **bulk ZIP per quarter** is simpler and entirely sufficient; cache the raw
ZIP and read from disk. The SOAP web service exists for automated, large-scale pulls; its exact
endpoint and auth are version-dependent, so verify before relying on it.

## License & GMU-infra note (§5)

**Free and public** U.S. government regulatory data — **no** GMU-infrastructure restriction. Unlike
the WRDS-licensed sources in this appendix, you may pull Call Reports on any machine, cache them,
and commit the cached raw files to git. Apply the CONVENTIONS §5 discipline uniformly anyway —
**pin the reporting quarter, cache the raw ZIP to `data/raw/`, and log the pull in
`logs/pulls.jsonl` with a content hash** — purely for reproducibility, not because a license demands
it. If you script the CDR web service, keep its access token in an env var (§5: it is a credential),
never in code.

## Gotchas

- **MDRM codes drift over time.** Line items are added, retired, and renumbered across years as
  reporting requirements change; a single MDRM code does not always mean the same thing back through
  history. Build series from the FFIEC's MDRM dictionary, do not assume code stability.
- **RCFD vs. RCON.** Consolidated (`RCFD…`) and domestic-only (`RCON…`) versions of the "same" item
  differ for banks with foreign offices. Choosing the wrong prefix silently mismeasures large banks.
- **Bank ≠ holding company.** Summing subsidiary-bank Call Reports does **not** equal the parent's
  FR Y-9C; the consolidation rules differ. Do not mix the two levels without the crosswalk.
- **Restatements and late filings.** Banks amend filings; a quarter pulled today can differ from the
  same quarter pulled later. Pin and log the pull date as well as the reporting quarter.
- **Mergers create discontinuities.** When banks merge, an RSSD disappears or absorbs another's
  balances — a jump in a single bank's series is often a merger, not organic growth.

## "First 10 rows" schema sketch — selected items, one quarter (illustrative — not real data)

| IDRSSD | RCFD2170 | RCFD2122 | RCON2200 | RIAD4340 | report_date |
|-------:|---------:|---------:|---------:|---------:|-------------|
| 100001 | 9852341 | 6120448 | 7421005 | 23110 | 2024-12-31 |
| 100002 | 41200 | 28055 | 34880 | 290 | 2024-12-31 |
| 100003 | 1503882 | 980221 | 1190440 | 4120 | 2024-12-31 |
| 100004 | 287990 | 175004 | 230118 | 905 | 2024-12-31 |
| 100005 | 65432100 | 40221890 | 49880221 | 188400 | 2024-12-31 |
| 100006 | 12044 | 7880 | 9905 | 41 | 2024-12-31 |
| 100007 | 880221 | 540118 | 690004 | 2110 | 2024-12-31 |
| 100008 | 3201998 | 2010554 | 2540118 | 8800 | 2024-12-31 |
| 100009 | 158002 | 99110 | 124880 | 480 | 2024-12-31 |
| 100010 | 22118994 | 13880221 | 17004118 | 61200 | 2024-12-31 |

(RSSD IDs and dollar amounts in $thousands are fabricated for shape illustration only.
`RCFD2170` = total assets, `RCFD2122` = total loans & leases, `RCON2200` = total deposits,
`RIAD4340` = net income — code meanings illustrative.)

## Which chapter / lab uses it

Catalogued in **Appendix C** as a *free* bank-regulation source. It is the entity-level data layer
for any Week-7/Week-8 capstone on **bank regulation, bank risk, deposit behavior, or lending** — a
Maya-style (household-finance/fair-lending) or Priya-style (climate-risk-on-bank-balance-sheets)
extension — and it pairs naturally with HMDA (lending) and the FR Y-9C (holding-company level).
Pull it the §5 way for reproducibility: pin the quarter, cache the raw ZIP, log the hash.
