# Data Card — Capital IQ (S&P Capital IQ via WRDS)

## Provider & what it is

Capital IQ is S&P Global Market Intelligence's company-intelligence platform; on **WRDS** it is
delivered as a family of databases that GMU licenses. Here is what it actually buys you that the
free filings do not: Capital IQ takes the messy, footnote-laden world of corporate disclosure and
*standardizes* it into comparable fields, then layers on things that are genuinely hard to compile
yourself. Three slices matter most for a camp project. (1) **Standardized financials** — income
statement, balance sheet, and cash-flow items normalized so that "revenue" or "EBITDA" means the
same thing across firms and years, with deep coverage of *private* and *international* companies
that CRSP/Compustat do not reach. (2) **Key Developments** — a structured, time-stamped event
feed: a firm announced earnings, named a CEO, got sued, did a buyback, issued guidance — each tagged
with an event type and date, which is gold for event studies because someone already did the
hand-coding. (3) **Transactions** — M&A deals, private placements, and other corporate transactions
with parties, dates, and deal values. Think of Capital IQ as the database that already turned
"things that happened to companies" into rows you can query.

## Coverage

Global, public and private companies. Standardized financials run on an **annual and quarterly**
cadence; Key Developments and Transactions are **event-dated** (a timestamp per event, not a fixed
period). History depth and the exact set of CIQ modules WRDS exposes are vintage- and subscription-
dependent. [CHECK: the specific Capital IQ products and their start years in GMU's current WRDS
license — the platform spans far more than the financials/key-dev/transactions slices named here.]
Treat the start date you actually observe in the table as the operative one and pin it.

## Key identifiers

Capital IQ's spine is the **`companyid`** (CIQ's internal company key); securities and trading
lines carry their own CIQ identifiers beneath it. Like OptionMetrics' `secid`, the `companyid` is
*proprietary to S&P* — it is not a ticker, CUSIP, GVKEY, or PERMNO. So any project that joins
Capital IQ to CRSP/Compustat needs a crosswalk (a CIQ↔GVKEY or CIQ↔CUSIP link; WRDS provides
mapping tables, and CIQ has a documented lineage to Compustat). Building and validating that link
is a Chapter 7.4 task and out of scope for this card. Key Developments rows additionally carry a
`keydevid` and a `keydeveventtypeid`; transactions carry a `transactionid`.

## Access path (Python via WRDS)

Capital IQ lives in WRDS libraries (often named `ciq` / `ciq_*`); you query it like every other
WRDS source — PostgreSQL over the `wrds` package, no key in code:

```python
import os, wrds
db = wrds.Connection(wrds_username=os.environ["WRDS_USERNAME"])  # token cached by the package

# Explore first; library and table names are vintage-dependent.
db.list_libraries()                       # find the ciq* libraries you have
db.list_tables(library="ciq")
db.describe_table("ciq", "ciqkeydev")     # confirm columns before querying

# Key Developments for one company over a bounded window (NEVER SELECT *).
kd = db.raw_sql("""
    SELECT companyid, keydevid, keydeveventtypeid, announceddate, headline
    FROM ciq.wrds_keydev
    WHERE companyid = %(cid)s
      AND announceddate BETWEEN %(d0)s AND %(d1)s
""", params={"cid": 21835, "d0": "2022-01-01", "d1": "2023-12-31"})
```

Table names above (`ciq.wrds_keydev`) and the `companyid` value are *illustrative*; run
`db.list_tables` / `db.describe_table` against your actual vintage rather than trusting these.

## License & GMU-infra note (§5)

**Licensed, not public.** Capital IQ is a paid WRDS/S&P subscription. Per CONVENTIONS §5 the rule
is the same one that governs CRSP and Compustat: **licensed to GMU; analyzed only on GMU
infrastructure (WRDS Cloud or the Hopper cluster); raw data never copied off, never committed to
git, never pasted into a commercial web service or emailed outside GMU.** Commit the *query code*
and the *pull log*; the licensed bytes stay in a git-ignored `data/raw/` on GMU infrastructure.
Pin the WRDS snapshot date in a comment and in `logs/pulls.jsonl`. One extra redistribution caveat:
S&P's company/security *identifier mappings* (and any embedded CUSIPs) are themselves licensed —
use them to merge your own data, but do not publish an identifier master file.

## Gotchas

- **Proprietary keys, mandatory crosswalk.** `companyid` joins to nothing outside CIQ without a
  mapping table; the link can be many-to-one across share classes and one-to-many across history.
- **Event timestamps: announced vs. effective.** Key Developments often carry more than one date
  (announced, entered, effective). For an event study, pick the date the *market learned* and be
  explicit; mixing them silently smears your event window.
- **Survivorship and backfill.** Standardized financials can be restated and backfilled; a value
  "as of today" may differ from what was reported then. For point-in-time work, this matters as
  much as it does for Compustat — pin the snapshot.
- **Definition drift across vendors.** CIQ's "EBITDA" is *its* standardization, not Compustat's
  and not the firm's GAAP figure. Compare like with like and cite the field definition.
- **Coverage is uneven for private firms.** Breadth on private/international companies is a selling
  point, but fields can be sparse — check non-missingness before you build a sample on a field.

## "First 10 rows" schema sketch — Key Developments (illustrative — not real data)

| companyid | keydevid | keydeveventtypeid | announceddate | headline |
|----------:|---------:|------------------:|---------------|----------|
| 10001 | 70011001 | 28 | 2023-01-31 | Company A reports Q4 results |
| 10001 | 70011002 | 80 | 2023-02-15 | Company A announces share repurchase program |
| 10001 | 70011003 | 48 | 2023-04-04 | Company A names new Chief Financial Officer |
| 10002 | 70022510 | 28 | 2023-01-26 | Company B reports Q4 results |
| 10002 | 70022511 | 22 | 2023-03-12 | Company B to acquire Company C |
| 10002 | 70022512 | 55 | 2023-05-09 | Company B issues full-year guidance |
| 10003 | 70033140 | 28 | 2023-02-02 | Company D reports Q4 results |
| 10003 | 70033141 | 31 | 2023-02-28 | Company D announces dividend increase |
| 10003 | 70033142 | 16 | 2023-06-21 | Company D faces shareholder lawsuit |
| 10004 | 70044090 | 28 | 2023-01-19 | Company E reports Q4 results |

(`keydeveventtypeid` codes, IDs, and headlines are fabricated for shape illustration only.)

## Which chapter / lab uses it

Catalogued in **Appendix C** and surveyed among WRDS-licensed sources in **Chapter 7.2**. Its Key
Developments feed is a strong backbone for any Week-7/Week-8 capstone built as an *event study* (a
corporate announcement as the event, returns as the outcome) — for example a Leah-style
(innovation/news) or Devon-style (corporate-disclosure) project. Use it under the same discipline
as CRSP/Compustat: read-only on GMU infrastructure, pinned, cached, logged.
