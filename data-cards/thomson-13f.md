# Data Card — Thomson Reuters / SEC 13F Institutional Holdings

**Provider & what it is.** Form 13F is the quarterly report that institutional investment managers with over **\$100 million** in qualifying U.S. equity assets must file with the SEC, disclosing their long equity positions: which stocks, how many shares, what market value, as of quarter-end. There are two ways to get it. The **free, public** route is **SEC EDGAR** (the raw filings). The **licensed, cleaned** route is the **Thomson Reuters / Refinitiv s34 institutional-holdings files on WRDS** — the same disclosures, de-duplicated, with cleaner identifiers and a long historical panel. The reveal-the-trick point is that 13F is how you *see what the big funds held*, which lets you build **common-ownership** measures — pairs of firms held by the same institutions — the construct behind Capstone 2 and Gao, Han, Kim & Pan (2024).

## Coverage
- **Span.** EDGAR 13F filings are public from the mid-**1990s** onward; the Thomson/WRDS s34 panel extends the cleaned history back to **1980** (institutional holdings). [CHECK] exact Thomson s34 start year and any known post-2013 coverage break.
- **Frequency.** **Quarterly**, as of calendar quarter-end, filed within 45 days after.
- **Universe.** All 13F-filing managers (banks, mutual funds, hedge funds, pensions, insurers) and the U.S. exchange-traded equities and options on the SEC's 13F security list. Holdings only — no shorts, no most derivatives.

## Key identifiers
- **CUSIP** (9-character security identifier) — how each *holding* is identified. **CUSIP is itself a licensed identifier**: you may use CUSIPs you obtain to merge your own data, but redistributing a large CUSIP-to-name master can violate CUSIP Global Services' license. Keep CUSIPs inside your analysis; do not publish a CUSIP master file.
- **CIK** — the EDGAR identifier of the *filing manager*.
- **MGRNO** (Thomson manager number) and Thomson security keys in the s34 files.
- Bridge CUSIP → CRSP PERMNO via the historical-CUSIP fields in CRSP (`crsp.msenames`) — a Ch 7.4 crosswalk, aligned on date.

## Access path
**Public (EDGAR)** — same User-Agent and 10-req/sec rules as any EDGAR pull; pin the accession number:

```python
import os
from edgar import Company, set_identity
set_identity(os.environ["SEC_USER_AGENT"])          # "Name email@gmu.edu" from env
mgr = Company("0001067983")                          # a manager's CIK, e.g.
info = mgr.get_filings(form="13F-HR").latest().obj().infotable  # one row per holding
```

**Licensed (Thomson s34 on WRDS)** — the cleaned panel; same `wrds` pattern, credentials from `.pgpass`/env:

```python
import os, wrds, pandas as pd, pathlib
db = wrds.Connection(wrds_username=os.environ["WRDS_USERNAME"])   # secret from env
raw = pathlib.Path("data/raw/tr_13f_holdings_2018_2020.parquet") # git-ignored
if raw.exists():
    hold = pd.read_parquet(raw)
else:
    hold = db.raw_sql("""
        SELECT mgrno, cusip, rdate, fdate, shares, prc, shrout2
        FROM   tr_13f.s34
        WHERE  rdate BETWEEN '2018-01-01' AND '2020-12-31'
    """, date_cols=["rdate", "fdate"])
    hold.to_parquet(raw)                                          # GMU infra only
db.close()
```

[CHECK] the current Thomson 13F library/table name on WRDS (`tr_13f.s34` vs. `tfn.s34`) — it has been renamed across vintages.

## License & the "stays on GMU infrastructure" note (CONVENTIONS §5)
The **filings** are public (EDGAR — cache and share freely). The **cleaned Thomson panel is licensed** (WRDS, GMU-only), accessed **read-only**: query on **WRDS Cloud** or GMU's **Hopper**, cache to a git-ignored `data/raw/`, and **never commit, email off campus, post publicly, or paste into a commercial web service.** Separately, **CUSIP** is licensed regardless of route — do not redistribute a CUSIP master. Ship the recipe (query + log), not the licensed bytes.

## Gotchas — what 13F does *not* tell you
- **Long positions only.** No shorts, no most derivatives — so a 13F is *not* the manager's true net exposure.
- **45-day reporting lag.** Holdings are stale by the time you see them; treating a 13F as real-time positioning is a look-ahead error in reverse.
- **Confidential treatment.** Managers can request to withhold some positions, so a disclosed table can be incomplete.
- **The "who is one manager" problem.** Family-of-funds and sub-advisor structures mean the *same* assets can appear under several CIKs/MGRNOs; common-ownership measures are sensitive to how you aggregate managers. This is a modeling choice you must state, not a data field.
- **Thomson coverage break.** A well-known data-quality drop in the Thomson s34 file around 2013 prompted many researchers to rebuild from raw EDGAR for recent quarters. [CHECK] before using post-2013 Thomson data.
- **Amendments (`13F-HR/A`).** A quarter can be refiled; pin the accession number you used.

## "First 10 rows" schema sketch (illustrative — not real 13F data)

| mgrno (int) | cusip (str) | rdate (date) | fdate (date) | shares (int) | prc (float) | shrout2 (int, 000s) |
|---|---|---|---|---|---|---|
| 11030 | 037833100 | 2018-12-31 | 2019-02-14 | 250000000 | 157.74 | 4715280 |
| 11030 | 594918104 | 2018-12-31 | 2019-02-14 | 18000000 | 101.57 | 7677000 |
| 11030 | 17275R102 | 2018-12-31 | 2019-02-14 | 9000000 | 42.66 | 4601000 |
| 90457 | 037833100 | 2018-12-31 | 2019-02-12 | 5400000 | 157.74 | 4715280 |
| ... | ... | ... | ... | ... | ... | ... |

(Values invented to show *shape and types*: rows 1 and 4 are two managers holding the **same** CUSIP — the raw ingredient of a common-ownership pair.)

## Which chapter/lab/capstone uses it
- **Capstone 2 — Common Ownership from 13F** (TOC): constructing common-ownership measures and a disclosure/competition outcome (a student-track sibling of the anchor paper's earnings-management outcome); ties to **Gao, Han, Kim & Pan (2024)**, "Overlapping institutional ownership along the supply chain and earnings management of supplier firms," *JCF*, 84:102520.
- **Week 6, Mentor Session 6** — the Gao et al. (2024) overlapping-ownership / earnings-management paper anchors the stretch questions.
- **Week 7, Ch 7.2 (§7.2.6)** — 13F is the worked example of "public EDGAR vs. licensed Thomson," the CUSIP-licensing caveat, and the long-only/45-day-lag/confidential-treatment limits.
