# Data Card — FDIC (Institution Directory, SDI financials, and bank failures)

## Provider & what it is

The **Federal Deposit Insurance Corporation (FDIC)** insures deposits at U.S. banks and, as the price of that insurance, collects a quarterly financial report from every insured institution. It publishes three things you will use, all through one free API called **BankFind Suite**:

- **Institution Directory** — the roster of every FDIC-insured bank and thrift: name, charter type, regulator, headquarters location, active/inactive status, and the all-important **CERT** number that identifies the institution. Think of it as the phone book of American banking.
- **SDI (Statistics on Depository Institutions)** — the quarterly *financials*: total assets, deposits, loans, net income, capital ratios, return on assets — the **Call Report** numbers, reshaped into clean fields. This is how you turn "is this bank healthy?" into a number.
- **Failures & assistance** — the historical list of bank *failures* and FDIC-assisted transactions, with the failure date and the acquiring institution. The 2008–2010 wave and the 2023 regional-bank episode both live here.

The reveal: banks look opaque, but they are among the most heavily *disclosed* firms in the economy. Every quarter, every insured bank hands the regulator a standardized balance sheet and income statement, and the FDIC hands it to you for free. The "secret" financial health of a bank is a public download.

## Coverage

- **Institution Directory:** all FDIC-insured institutions, active and historical; inactive banks retain their record with a closing reason. Tens of thousands of CERTs across history; roughly 4,000–5,000 active banks today (the count has fallen steadily through consolidation). `[CHECK]` exact active count for your pinned vintage.
- **SDI financials:** quarterly, with broad coverage from the early 1990s and selected series earlier. Reported each quarter on the Call Report cycle (filings due ~30 days after quarter-end, so the most recent quarter lags). `[CHECK]` earliest quarter per field.
- **Failures:** complete failure list from 1934 onward; the modern, richly-detailed records cluster in the post-2000 period. The famous spikes are 2008–2012 and the March 2023 events (SVB, Signature, First Republic). `[CHECK]` First Republic resolution coding (acquired vs. failed).

## Key identifiers

- **CERT** — the FDIC Certificate number, the primary key for an institution across the Directory, SDI, and failures. Stable for the life of the charter. This is the join key for everything.
- Also present: **RSSD** (the Federal Reserve's institution id, useful to merge with Fed/Call Report data), the bank's **name** and **location** (state, city, FIPS). Holding-company structure is partial here — a bank's parent BHC lives more completely in the Fed's NIC database, so do not assume CERT alone resolves the corporate parent. `[CHECK]` whether RSSD ships in all BankFind endpoints.

## Access path

- **BankFind Suite API**, base `https://banks.data.fdic.gov/api/`. JSON, **no key required**, public. Three endpoints map to the three datasets:
  - `/institutions` — directory records (filter by `STALP` state, `ACTIVE`, etc.)
  - `/financials` — SDI quarterly financials (filter by `CERT` and `REPDTE` report date)
  - `/failures` — the failure list
- Query parameters use a `filters` expression, a `fields` list (to limit columns), and `limit`/`offset` for paging. The API is generous but paginate for bulk pulls rather than requesting everything at once.

```python
import requests, pandas as pd
BASE = "https://banks.data.fdic.gov/api"
# Active banks headquartered in Virginia (public, no key):
r = requests.get(f"{BASE}/institutions",
                 params={"filters": "STALP:VA AND ACTIVE:1",
                         "fields": "NAME,CERT,STALP,CITY,ASSET",
                         "limit": 50}, timeout=60)
banks = pd.json_normalize(r.json()["data"])   # each row nests under 'data'
# Quarterly financials for one bank by CERT:
r2 = requests.get(f"{BASE}/financials",
                  params={"filters": "CERT:3510", "fields": "CERT,REPDTE,ASSET,DEP,NETINC,ROA",
                          "sort_by": "REPDTE", "sort_order": "DESC", "limit": 8}, timeout=60)
```

No secrets needed — the API is fully open. If you wrap it in a script, still follow CONVENTIONS §5 and never hard-code anything that *looks* like a credential.

## License & note

**Free and public.** FDIC data is U.S. government work, effectively public domain; cite the FDIC BankFind Suite and your pinned vintage and you are done. The only real obligation is honesty about *which quarter* you pulled, because SDI is restated — a bank's reported assets for a past quarter can change in a later vintage as corrections flow in. Pin `REPDTE` and the access date.

## Gotchas

- **Restatements.** SDI values for a past quarter can change in a later snapshot. Pin the vintage or your "2019Q4 assets" will not reproduce.
- **Merged-away banks vanish from the active roster but live in the directory.** When you study failures or consolidation, filter on `ACTIVE` deliberately — a survivorship-biased panel of only-currently-active banks will understate distress.
- **The bank is not the holding company.** CERT identifies a *bank charter*; a single holding company can own several CERTs. Aggregating to the parent firm needs the RSSD/NIC crosswalk, not CERT alone.
- **"Failure" has a precise meaning.** A bank acquired in a healthy merger is *not* a failure; only FDIC-resolved closures and assisted transactions appear in `/failures`. Do not conflate consolidation with distress.
- **Field-name soup.** SDI uses terse Call Report codes (`ASSET`, `DEP`, `NETINC`, `RBCT2` …). Keep the FDIC field dictionary open; `[CHECK]` any field meaning before you regress on it.

## First 10 rows (illustrative schema sketch — not real values)

*Institution Directory (`/institutions`), shape only:*

| CERT | NAME | STALP | CITY | ACTIVE | ASSET |
|---|---|---|---|---|---|
| 3510 | Example National Bank | VA | Fairfax | 1 | 18432109 |
| 57890 | Sample Community Bank | MD | Bethesda | 1 | 742118 |
| … | … | … | … | … | … |

*SDI financials (`/financials`), one row per CERT × quarter, shape only:*

| CERT | REPDTE | ASSET | DEP | NETINC | ROA |
|---|---|---|---|---|---|
| 3510 | 2026-03-31 | 18432109 | 14201338 | 52114 | 1.12 |
| 3510 | 2025-12-31 | 18120044 | 13988201 | 49870 | 1.09 |
| … | … | … | … | … | … |

*Failures (`/failures`), shape only:*

| CERT | NAME | FAILDATE | CITY | STALP | ACQINST |
|---|---|---|---|---|---|
| 57053 | Sample Bridge Bank | 2023-03-10 | Santa Clara | CA | Acquiring Bank, N.A. |
| … | … | … | … | … | … |

## Which chapter / lab / capstone uses it

- **Bank financials and the CERT key** support worked examples on firm-level financial-health measures and panel construction — a clean, free alternative to licensed Compustat for *banks specifically*, useful when a student wants real balance-sheet data without a WRDS seat.
- **The failures file** is the natural dataset for an event-study or survival exercise on bank distress (the 2008–2012 and 2023 waves), and a good demonstration of survivorship bias when contrasting active-only vs. full panels (ties to the inference discipline of Weeks 2–4).
- It sits alongside the other public-finance sources (`treasury-finra.md`, `msrb-emma.md`) as a "real institutions, free data, messy keys" source students can use for a self-directed capstone extension when they want banking data outside the five canonical capstone datasets.
