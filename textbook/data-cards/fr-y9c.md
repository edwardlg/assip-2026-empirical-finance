# Data Card — FR Y-9C (Bank Holding Company Financials)

## Provider & what it is

The **FR Y-9C** is the *Consolidated Financial Statements for Holding Companies* — the quarterly
report that bank holding companies, savings and loan holding companies, and intermediate holding
companies of foreign banks file with the **Federal Reserve**. Here is the reveal, and why it exists
alongside the Call Reports: a big bank is rarely *one* legal entity. A holding company owns its bank
plus broker-dealers, asset managers, and other subsidiaries. A Call Report shows you the *bank*
subsidiary; the FR Y-9C shows the **whole consolidated holding company**, parent and all
subsidiaries netted together as one economic unit. If your question is about the institution
investors actually buy stock in — the entity in CRSP/Compustat — the FR Y-9C is usually the right
level: consolidated assets, loans, deposits, trading positions, regulatory capital, and income,
every quarter. Its convenient public home is the **Federal Reserve Bank of Chicago**, which hosts
free bulk FR Y-9C data files (the "BHCF" files) going back decades.

## Coverage

Top-tier U.S. bank/savings-and-loan holding companies above the asset-size reporting threshold,
filed **quarterly**. Smaller holding companies file the abbreviated **FR Y-9SP** (semiannual) rather
than the Y-9C; this card is the Y-9C (the consolidated, quarterly, larger-entity form). The Chicago
Fed's BHCF archive provides a deep history. [CHECK: the current asset-size filing threshold for the
FR Y-9C and the earliest quarter in the Chicago Fed BHCF files — both have changed over time.]
This is *consolidated holding-company* level — one record per holding company per quarter.

## Key identifiers

The primary key is the **RSSD ID** — the same Federal Reserve permanent institution identifier used
by the Call Reports and the National Information Center, but here it identifies the **holding
company**, not a subsidiary bank. That is the whole point and the whole trap: the holding company's
RSSD ID and its subsidiary bank's RSSD ID are *different numbers*, and the link between them lives in
the Fed's **NIC structure/relationship files**. Joining a Y-9C parent to its Call Report
subsidiaries — or to CRSP/Compustat via a PERMCO/GVKEY crosswalk — is a Chapter 7.4 task and out of
scope here. Line items use the **MDRM** coding scheme with a **`BHCK…`** prefix (the holding-company
analog of the Call Report's `RCFD`/`RCON`) — e.g. `BHCK2170` for consolidated total assets.

## Access path (download; no key required)

FR Y-9C data is free and needs **no API key**. The simplest path is the Chicago Fed bulk file:

```python
import zipfile, requests, pandas as pd

# Chicago Fed "BHCF" bulk file for one quarter (one ZIP per period).
# url = "<Chicago Fed BHCF download URL for 2024-12-31>"   # [CHECK exact Chicago Fed endpoint]
raw = "data/raw/bhcf_2024Q4.zip"        # cache the raw bytes; read from disk thereafter
with zipfile.ZipFile(raw) as z:
    name = z.namelist()[0]
    y9c = pd.read_csv(z.open(name), sep="^", low_memory=False)   # [CHECK delimiter for the vintage]

# Pull the holding companies and items you need (illustrative codes).
cols = ["RSSD9001", "RSSD9999", "BHCK2170", "BHCK2122", "BHCK2200"]
panel = y9c[cols]    # RSSD9001 = entity RSSD, RSSD9999 = report date
```

The FFIEC CDR also serves the FR Y-9C (the same forms flow through the CDR), but for a camp project
the **Chicago Fed BHCF bulk file per quarter** is the path of least resistance. Cache the raw ZIP and
read the cached copy. The file's delimiter and exact column layout vary by vintage — inspect before
parsing.

## License & GMU-infra note (§5)

**Free and public** U.S. government regulatory data — **no** GMU-infrastructure restriction, like the
Call Reports and unlike the WRDS-licensed sources in this appendix. You may pull, cache, and commit
the raw files anywhere. Apply the CONVENTIONS §5 discipline uniformly for reproducibility, not because
a license requires it: **pin the reporting quarter, cache the raw ZIP to `data/raw/`, and log the
pull in `logs/pulls.jsonl` with a content hash.** No credential is required for the Chicago Fed bulk
files; if you instead script the FFIEC CDR web service, keep its token in an env var (§5).

## Gotchas

- **Holding company ≠ its banks.** The FR Y-9C consolidates the *whole* company; summing the
  subsidiary Call Reports will not reproduce it, and the RSSD IDs differ. Pick the level your
  question actually needs and never mix them without the NIC crosswalk.
- **`BHCK` prefix, and MDRM drift.** Y-9C items use `BHCK…` codes (not the Call Report's `RCFD`/
  `RCON`); like all MDRM codes they are added, retired, and renumbered across years, so build series
  from the dictionary rather than assuming a code means the same thing back through history.
- **Threshold and form changes.** The asset-size threshold for filing the Y-9C (vs. the semiannual
  Y-9SP) has been raised over time, so the *set* of filers changes across the panel — a firm
  entering or leaving the sample may reflect a rule change, not a real event.
- **Restatements and mergers.** Holding companies amend filings, and bank-holding-company mergers
  create discontinuities and RSSD changes — a jump in one entity's series is often a merger.
- **Vintage-specific layout.** Delimiter, header, and column set differ across Chicago Fed file
  vintages; do not hard-code a parser across many years without checking each period.

## "First 10 rows" schema sketch — selected items, one quarter (illustrative — not real data)

| RSSD9001 | RSSD9999 | BHCK2170 | BHCK2122 | BHCK2200 | BHCK4340 |
|---------:|----------|---------:|---------:|---------:|---------:|
| 200001 | 2024-12-31 | 312045880 | 178220110 | 240118004 | 9852110 |
| 200002 | 2024-12-31 | 41880221 | 25004118 | 31220990 | 1180004 |
| 200003 | 2024-12-31 | 1880221004 | 1102004118 | 1450118220 | 52004110 |
| 200004 | 2024-12-31 | 5120998 | 3104221 | 4002118 | 158220 |
| 200005 | 2024-12-31 | 88220110 | 54118004 | 67004221 | 2540118 |
| 200006 | 2024-12-31 | 990221004 | 612118220 | 760004118 | 28220110 |
| 200007 | 2024-12-31 | 22118004 | 13880221 | 17004118 | 612004 |
| 200008 | 2024-12-31 | 450118220 | 280004221 | 350118004 | 12880110 |
| 200009 | 2024-12-31 | 7220998 | 4504118 | 5680221 | 220004 |
| 200010 | 2024-12-31 | 2104880221 | 1280118004 | 1620221110 | 61004220 |

(RSSD IDs and dollar amounts in $thousands are fabricated for shape illustration only.
`BHCK2170` = consolidated total assets, `BHCK2122` = total loans & leases, `BHCK2200` = total
deposits, `BHCK4340` = net income — code meanings illustrative.)

## Which chapter / lab uses it

Catalogued in **Appendix C** as a *free* bank-regulation source, and the holding-company companion to
the FFIEC Call Reports card. It is the right data layer when a Week-7/Week-8 capstone studies the
*publicly traded* banking entity — bank-holding-company risk, capital, or lending — because the Y-9C
level lines up with CRSP/Compustat (via a PERMCO/GVKEY crosswalk, a Ch 7.4 task). A natural fit for a
Maya-style (household-finance/fair-lending) or Priya-style (climate-risk) bank-regulation project.
Pull it the §5 way for reproducibility: pin the quarter, cache the raw ZIP, log the hash.
