# Data Card — U.S. Bureau of Economic Analysis (BEA)

**Source slug:** `bea` · Appendix C (Data Dictionary) · last touched 2026-05-28

## Provider & what it is

The Bureau of Economic Analysis, part of the Department of Commerce, is the agency that builds the **national accounts** — GDP and everything that hangs off it. Where BLS measures prices and jobs, BEA measures *output and income*. Two BEA products do the work in this book. **Regional GDP** (the "GDP by state" and "GDP by county/metro" accounts) gives output by industry for each state, metro area, and county — the local-economy denominator that lets you ask whether a place is growing. **Fixed Assets** (the Fixed Assets Accounts, and the related capital-stock tables) give the value of the nation's accumulated capital — equipment, structures, intellectual property products — by industry and by type, which is the macro counterpart to the firm-level investment a finance student usually studies. The reveal-the-trick point: BEA numbers are *constructed estimates assembled from dozens of source datasets*, not direct measurements, and they get revised heavily. A BEA series is a model output wearing a data costume.

## Coverage

National GDP (NIPA) is quarterly and annual back to 1929 (annual) / 1947 (quarterly). Regional GDP by state is annual from 1963 and quarterly from 2005; GDP by county is annual and relatively recent (county estimates begin around 2001 [CHECK exact first county-GDP year]). Fixed Assets tables are annual, back to 1925 for some aggregates. Values come in both **current dollars** (nominal) and **chained dollars** / real terms, plus quantity and price indexes. Geography spans nation, BEA region, state, metro area, and county.

## Key identifiers

BEA's API is organized by **dataset** (`Regional`, `FixedAssets`, `NIPA`, etc.), and within a dataset you select a **table** (`TableName`, e.g. `SAGDP2N` for state annual GDP by industry), a **LineCode** (the specific row/industry within that table), a **GeoFIPS** (state/county/metro FIPS, with `STATE`, `COUNTY`, `MSA` wildcards), and a **Year**. So the joint key for a regional observation is roughly (TableName, LineCode, GeoFIPS, Year). GeoFIPS aligns with the Census FIPS codes — the same zero-padding-as-string discipline applies, and BEA county FIPS even reuses Census county codes, so a regional GDP table can be joined to ACS/CBP on FIPS.

## Access path (API; key via env)

The BEA API lives at `https://apps.bea.gov/api/data` and requires a free **UserID** key (request it on the BEA site; it arrives by email). It is a GET with a `method` parameter (`GetData`, `GetParameterValues`, `GetParameterList` for discovering valid LineCodes).

```python
import os, requests
key = os.environ["BEA_API_KEY"]  # env only; CONVENTIONS §5
params = {"UserID": key, "method": "GetData",
          "datasetname": "Regional", "TableName": "SAGDP2N",
          "LineCode": "1", "GeoFIPS": "STATE", "Year": "2022",
          "ResultFormat": "JSON"}
r = requests.get("https://apps.bea.gov/api/data", params=params).json()
# r["BEAAPI"]["Results"]["Data"] is the list of records
```

There is no first-party Python SDK we depend on; `requests` + `pandas.json_normalize` is the standard path. Many BEA headline series are also mirrored on FRED for quick exploration.

## License (FREE / public) & note

BEA data are **U.S. Government works in the public domain** — free to use, redistribute, and republish with attribution; no row-level license and no GMU-only constraint, so they belong in a packet's `data/raw/`. Cite as "U.S. Bureau of Economic Analysis, GDP by State, table SAGDP2N, retrieved [date]." The API's terms ask for attribution and reasonable use (cache, do not hammer).

## Gotchas

- **Heavy revisions and comprehensive (benchmark) updates.** BEA revises quarterly GDP three times, then again in annual updates, then periodically rewrites *the entire history* in a comprehensive benchmark revision (methodology and base year change at once). The 2018 series you pulled in 2019 may not exist in today's API. As with BLS, this is a vintage problem — record the snapshot date or risk look-ahead bias.
- **Nominal vs. real, and chained-dollar non-additivity.** Chained-dollar (real) components do *not* sum to their chained-dollar total — a property of the chaining method that surprises everyone the first time. Sum nominal components; use the published real total.
- **LineCode is opaque.** You must call `GetParameterValues` to learn which LineCode is "All industry total" vs. a specific NAICS sector. Guessing a LineCode silently returns the wrong industry.
- **County GDP is modeled and noisy.** County estimates are statistically derived from state totals and are far less reliable than state numbers; treat them as indicative, not precise, and never as the dependent variable in a high-stakes design without caveat.
- **GeoFIPS formatting.** Wildcards (`STATE`, `COUNTY`) and explicit FIPS behave differently; explicit county FIPS must be 5-digit zero-padded strings.
- **Table renames.** Table names occasionally change across vintages; a stale `TableName` returns an error rather than data.

## "First 10 rows" — schema sketch (ILLUSTRATIVE, not real values)

Regional GDP by state, all-industry total (`SAGDP2N`, LineCode 1), current dollars:

| Code | GeoFIPS | GeoName | TimePeriod | CL_UNIT | UNIT_MULT | DataValue |
|------|---------|---------|-----------|---------|-----------|----------:|
| SAGDP2N-1 | 06000 | California | 2022 | USD | 6 | 3641000 |
| SAGDP2N-1 | 48000 | Texas | 2022 | USD | 6 | 2356000 |
| SAGDP2N-1 | 51000 | Virginia | 2022 | USD | 6 | 649000 |
| SAGDP2N-1 | 36000 | New York | 2022 | USD | 6 | 2053000 |
| SAGDP2N-1 | 50000 | Vermont | 2022 | USD | 6 | 38000 |

Fixed Assets, net stock by type (`FAAt201`, illustrative LineCode), current dollars:

| Code | LineDescription | TimePeriod | UNIT_MULT | DataValue |
|------|-----------------|-----------|-----------|----------:|
| FAAt201-2 | Equipment | 2022 | 9 | 8200 |
| FAAt201-3 | Structures | 2022 | 9 | 25600 |
| FAAt201-4 | Intellectual property products | 2022 | 9 | 5400 |

(Illustrative magnitudes only; do not cite. `UNIT_MULT = 6` means values are in millions; the chained-dollar non-additivity caveat applies if you switch `CL_UNIT` to real.)

## Which chapter / lab / capstone uses it

- **Capstone 5 — FRED Macro Event Study** — GDP releases are major macro announcements, and BEA's revision schedule is the textbook case of the vintage/look-ahead trap the capstone's inference must respect.
- **Week 4, Ch 4.5 (Shift-Share) and macro controls** — state/metro regional GDP supplies a local-output denominator and growth control; Fixed Assets by industry supplies the capital-stock context for industry-level shocks, complementing the Census/CBP shares and BLS shifts.
- **Week 6, Capstone 3 — Innovation from USPTO PatentsView** — BEA Fixed Assets' "intellectual property products" line is the macro mirror of the firm-level patent-value measure (KPSS 2017), useful as an aggregate sanity check on whether a constructed innovation measure tracks national IP investment.
- **Week 7, Ch 7.2 (Data Acquisition in Practice)** — BEA API appears as a worked free-source pull (key-by-email, LineCode discovery, vintage discipline).
