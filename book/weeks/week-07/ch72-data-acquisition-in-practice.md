# Chapter 7.2 — Data Acquisition in Practice

In Chapter 7.1 each of our five students walked out of the idea-generation workshop with a sharpened question and a named dataset. Maya wants to test whether tightened mortgage-lending standards fell harder on first-generation borrowers, so she needs HMDA loan-application records and a macro control series from FRED. Devon wants to know whether a crypto exchange's S-1 disclosures predicted its later token volatility, so he needs SEC filings and a price series. Priya wants to link insurers' climate-risk language to their stock returns, so she needs Compustat fundamentals from WRDS and 10-K text from EDGAR. Sam wants a clean daily price-and-return panel to backtest a momentum rule, which means CRSP if he can get it and yfinance or Stooq if he cannot. Leah wants patent counts by firm-year from USPTO PatentsView, merged later to financials.

Five questions, eight or nine data sources, and one problem they all share: **a question is not a dataset.** Between "I want HMDA data" and "I have a file on disk that I can defend to a referee" lies a whole craft — knowing where the data lives, who owns it, how to ask for it without getting rate-limited or sued, and how to pull it so that *the same command run a year from now gives the same answer.* That craft is this chapter.

We are going to be honest about something the polished final tables in journals hide: getting the data is often the hardest, slowest, and most error-prone part of an empirical project, and almost none of it is glamorous. It is API keys and user-agent headers and pagination and license agreements. But it is also where reproducibility is won or lost. A study whose data pull cannot be re-run is a study no one can check — and Week 7's whole arc, from idea to pre-analysis plan, is about building work that survives checking.

The reveal-the-trick frame for this chapter is slightly different from a math chapter. For each source we will state the same six things, in the same order, so you can compare sources at a glance and so that by source number three you know exactly what to look for:

1. **Coverage** — what is in it, and over what time span.
2. **Key identifiers** — the codes you use to find and later merge a record.
3. **Access path** — the package or API and a short code or workflow pattern.
4. **Licensing and the GMU-infrastructure rule** — who owns it, and whether it may leave the building.
5. **Rate limits and gotchas** — how to get blocked, and how not to.
6. **The reproducible pull** — how to pin a snapshot, cache the raw data, and log the query.

We will *not* cover merging or cleaning the data — joining CRSP to Compustat on the right keys, handling missing values, winsorizing. That is Chapter 7.4, and it is a big enough subject to deserve its own chapter. Here we stop the moment a clean *raw* file is sitting on disk with a log next to it. Each source also has a fuller reference — a **data card** — in Appendix C (the `data-cards/` directory); think of this chapter as the narrated tour and the cards as the spec sheets you return to while coding. The runnable, offline-verified version of every pattern below lives in **nb7.2**, the multi-source data-pull harness; the code here is illustrative and meant to be read, not copy-pasted into production.

---

## 7.2.1 Three rules that apply to every source

Before any specific source, three rules cut across all of them. They come straight from CONVENTIONS §5, and they are the difference between a data pull a referee trusts and one they cannot.

**Rule 1 — Secrets live in environment variables, never in code.** Several sources below require an API key — a string that identifies you to the server. A key is a password. The instant you write `api_key = "abc123..."` into a notebook, that key is in your shell history, your git history, and (if you ever push) on GitHub forever, where bots scrape public repos for exactly such strings. So every key in this chapter is read at runtime from the environment:

```python
import os
FRED_KEY = os.environ["FRED_API_KEY"]   # set once in your shell: export FRED_API_KEY=...
```

You set the variable once in your shell (`export FRED_API_KEY=...`) or, better, in a `.env` file that is listed in `.gitignore` and *never committed*. If `os.environ["FRED_API_KEY"]` raises a `KeyError`, that is the system working: it is refusing to run until you have set the key out-of-band. We will use this pattern without further comment from here on.

**Rule 2 — Licensed data stays on GMU infrastructure.** This is the single rule most likely to get a student into real trouble, so it gets stated in full. CRSP, Compustat, IBES, TRACE, and the other WRDS subscriptions are *licensed*, not public. GMU pays for them; the license permits use by GMU-affiliated researchers *on GMU systems*. That has a hard consequence: **you may not download CRSP or Compustat to your personal laptop, email it to a collaborator outside GMU, post it to a public repo, or paste it into a commercial web service.** The data may be analyzed only inside the walls the license defines — on WRDS Cloud itself, or on GMU's compute (the Hopper cluster), reading from GMU-licensed access. Concretely, for this whole chapter: **licensed raw data is never committed to git.** Your repository commits the *code* that pulls it and a *log* of what was pulled, but the licensed bytes stay in a `data/raw/` directory that your `.gitignore` excludes. Public data (FRED, EDGAR, HMDA, PatentsView, yfinance) has no such restriction and *can* be cached and shared — but the discipline of keeping raw pulls out of git and reproducible-by-script is good practice for those too, so we apply it uniformly.

**Rule 3 — A pull is reproducible only if it is pinned, cached, and logged.** Three sub-rules, and they recur for every source:

- **Pin a snapshot or date.** Live data changes. CRSP gets re-stated; Compustat backfills restatements; FRED revises GDP; firms refile amended 10-Ks; PatentsView updates quarterly. If your "pull everything as of today" gives a different answer next month, your results are not reproducible. So you pin: record the exact WRDS data snapshot date, the FRED observation vintage, the EDGAR filing accession number, the PatentsView data release. A pinned pull says not "the latest data" but "the data *as it stood on 2026-05-15*."
- **Cache the raw data.** Pull once, write the untouched response to disk (Parquet for tables, the raw JSON/HTML for filings), and have every downstream step read from that cached file — never re-hit the API. This makes your analysis fast, makes it independent of the source being up, and — critically — *freezes the input* so a re-run of your analysis gives identical numbers. The raw cache is your ground truth.
- **Log the query.** Write down, in a file, exactly what you asked for: the SQL string, the API URL, the date, the row count returned, and a hash of the result. Six months from now, when a reviewer asks "where did this number come from?", the log answers. This is the data-acquisition twin of the API audit log from Chapter 6.5.

We will fold all three into a tiny helper used throughout the chapter:

```python
import hashlib, json, datetime, pathlib

def log_pull(logfile, source, query, df):
    """Append one JSON line describing a data pull: what, when, how big, and a content hash."""
    record = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source": source,
        "query": query,                                  # SQL string or API URL (NO secrets in it)
        "n_rows": int(len(df)),
        "n_cols": int(df.shape[1]),
        "content_sha256": hashlib.sha256(
            df.to_csv(index=False).encode()).hexdigest(),  # changes if the data changes
    }
    pathlib.Path(logfile).parent.mkdir(parents=True, exist_ok=True)
    with open(logfile, "a") as f:
        f.write(json.dumps(record) + "\n")
```

Two things to notice. The `query` field stores the *request*, never a key — you log the URL or SQL, with any key stripped, so the log is safe to commit even when the data is not. And the `content_sha256` hash is the trick that makes "did the data change?" a one-line check: if two pulls produce the same hash, they are byte-identical; if not, something upstream moved, and you want to know.

---

## 7.2.2 WRDS Cloud — CRSP, Compustat, IBES, TRACE

**Coverage.** WRDS (Wharton Research Data Services) is the front door to the licensed datasets that define empirical finance. The four you will meet most:

- **CRSP** (Center for Research in Security Prices): daily and monthly stock prices, returns, shares outstanding, and — its crown jewel — *delisting returns* and a survivorship-bias-free universe of US-listed equities back to 1925. This is Sam's momentum data, done right.
- **Compustat** (S&P Global): standardized firm financial statements — the Fundamentals Annual and Fundamentals Quarterly files — covering income statement, balance sheet, and cash flow for tens of thousands of public firms, North America back to the 1950s/60s and global thereafter. This is Priya's insurer fundamentals.
- **IBES** (Institutional Brokers' Estimate System): analyst earnings forecasts and recommendations — consensus and detail.
- **TRACE** (Transaction Reporting and Compliance Engine, via FINRA): transaction-by-transaction corporate-bond trades.

**Key identifiers.** Each WRDS dataset has its own primary key, and knowing them is half the battle (the other half, the *crosswalks* between them, is Chapter 7.4). CRSP keys on **PERMNO**, a permanent security identifier that, unlike a ticker, never changes when a firm renames or re-tickers. Compustat keys on **GVKEY**, a permanent company identifier, plus a `datadate`. IBES keys on its own **TICKER** (an IBES-internal code, *not* the exchange ticker — a classic trap). The CRSP/Compustat *Merged* database (CCM) provides the PERMNO↔GVKEY linking table. For now, just know that the keys differ and are not interchangeable.

**Access path.** WRDS runs a PostgreSQL database you query with the `wrds` Python package. You connect, run SQL, get a DataFrame:

```python
import os, wrds

# wrds reads credentials from a ~/.pgpass file or prompts once and caches a token.
# Do NOT put your WRDS password in code. (The package manages it for you.)
db = wrds.Connection(wrds_username=os.environ["WRDS_USERNAME"])

# Pull monthly returns for a date window. Note: we SELECT only the columns we need,
# and we BOUND the date range -- never "SELECT *" on a table with 100M+ rows.
crsp_msf = db.raw_sql("""
    SELECT permno, date, ret, prc, shrout
    FROM crsp.msf
    WHERE date BETWEEN '2010-01-01' AND '2020-12-31'
""", date_cols=["date"])

db.close()
```

The mental model: WRDS is a remote database, and you are writing SQL against tables you do not own. Two habits matter. First, **select only the columns and rows you need** — CRSP's daily stock file has tens of millions of rows, and `SELECT *` will time out or blow your memory. Bound the dates, name the columns. Second, **explore the schema first**: `db.list_libraries()`, `db.list_tables(library="crsp")`, and `db.describe_table("crsp", "msf")` tell you what is there before you guess. The data card for each WRDS source in Appendix C lists the tables and the columns you will most want.

**Licensing — the central case of the GMU rule.** WRDS data is the reason Rule 2 exists. The connection is *read-only* — you cannot write to WRDS — and the data it returns is licensed to GMU. On **WRDS Cloud** itself (a JupyterHub-like environment WRDS hosts), the data never leaves Wharton's servers, which is the cleanest place to work. If you instead pull into GMU's Hopper cluster, the data stays inside GMU's licensed environment. What you must *not* do is pull CRSP to your laptop and push it to GitHub. So: **the CRSP/Compustat DataFrame is cached to `data/raw/` on GMU infrastructure, that directory is git-ignored, and only your query code and pull log are committed.**

**Rate limits and gotchas.** WRDS does not publish a hard request-rate limit, but it enforces practical ones: a query that scans an unindexed full table can run for many minutes and may be killed, and the cluster is shared, so a reckless `SELECT *` is antisocial as well as slow. Pull in bounded chunks (by year, by exchange) for the very large tables. The subtlest gotcha is *which* CRSP variable: `RET` includes dividends and is what you almost always want for a total-return study, while `RETX` excludes them — using the wrong one silently biases every return-based result. And remember delisting returns are in a *separate* table (`crsp.msedelist`); ignoring them is the survivorship bias you will study in Chapter 7.4.

**The reproducible pull.** Pin the snapshot date (WRDS labels each data vintage; record the date you pulled and the snapshot if your group uses one), cache to Parquet, and log:

```python
import pathlib
raw = pathlib.Path("data/raw/crsp_msf_2010_2020.parquet")   # in a git-ignored dir
if raw.exists():
    crsp_msf = pd.read_parquet(raw)                          # use the cache; never re-hit WRDS
else:
    crsp_msf = db.raw_sql(""" ... """, date_cols=["date"])   # the bounded query above
    crsp_msf.to_parquet(raw)
    log_pull("logs/pulls.jsonl", "crsp.msf [snapshot 2026-05-15]",
             "SELECT permno,date,ret,prc,shrout FROM crsp.msf WHERE date BETWEEN ...",
             crsp_msf)
```

That `if raw.exists()` pattern — check the cache, pull only on a miss, then log — is the spine of every reproducible pull in this chapter. We will reuse it for every source.

---

## 7.2.3 SEC EDGAR — full-text search, XBRL, and filings

**Coverage.** EDGAR is the SEC's public archive of every filing by every US public company since 1993/94: 10-Ks (annual reports), 10-Qs (quarterly), 8-Ks (material events), DEF 14A (proxy statements), S-1s (IPO registrations), 13Fs (institutional holdings, §7.2.6), and more. It is *free* and *public* — no license, no GMU restriction — which makes it the workhorse of text-based finance research. This is Priya's 10-K climate language and Devon's exchange S-1.

EDGAR gives you three distinct things, and confusing them wastes hours:
1. **Full-text search (EFTS):** search the *text* of filings (2001–present) for words or phrases, returning matching filings.
2. **Filing documents:** the actual 10-K/8-K/etc. documents (HTML, text), addressed by company **CIK** and **accession number**.
3. **XBRL financial statement datasets:** the *numbers* inside filings — revenue, assets, EPS — tagged in a structured, machine-readable format, available both per-company (the `companyfacts` API) and as bulk quarterly flat files.

**Key identifiers.** The **CIK** (Central Index Key) is EDGAR's permanent company identifier — a number, zero-padded to ten digits in URLs (`0000320193` is Apple). The **accession number** identifies a specific filing (e.g., `0000320193-23-000106`). A ticker maps to a CIK via EDGAR's `company_tickers.json`. Note these are *EDGAR's* keys; mapping CIK to CRSP's PERMNO or Compustat's GVKEY is, again, a Chapter 7.4 crosswalk.

**Access path.** Two routes. The high-level one is **`edgartools`**, a Python package that wraps the messy URL structure into a clean object API:

```python
from edgar import Company, set_identity
# SEC REQUIRES a descriptive User-Agent identifying you. This is the fair-access rule.
set_identity("Maya Rodriguez maya@gmu.edu")   # name + email; read from env in real code

aapl = Company("AAPL")
filings = aapl.get_filings(form="10-K")        # all 10-K filings for this company
latest = filings.latest()
financials = latest.financials                 # structured XBRL financials
```

The low-level route is plain **`requests`** against EDGAR's REST endpoints — useful when you want exactly one JSON file and no dependency. For the structured numbers, the `companyfacts` endpoint returns every XBRL-tagged fact for a company:

```python
import os, requests

# The User-Agent header is MANDATORY. Read it from the environment so it is not hard-coded.
HEADERS = {"User-Agent": os.environ["SEC_USER_AGENT"]}   # e.g. "Maya Rodriguez maya@gmu.edu"

cik = "0000320193"   # Apple, zero-padded to 10 digits
url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
resp = requests.get(url, headers=HEADERS, timeout=30)
resp.raise_for_status()
facts = resp.json()   # nested dict of every tagged financial fact
```

For full-text search, the EFTS endpoint (`https://efts.sec.gov/LATEST/search-index?q=...`) returns the filings whose text matches a query — Priya could search `"climate-related risks"` to find candidate 10-Ks before pulling them.

**The SEC fair-access rule.** This is the gotcha that bites everyone exactly once. The SEC does not require a key, but it *does* require that every request carry a **`User-Agent` header that identifies you** — your name and email, e.g. `"Maya Rodriguez maya@gmu.edu"`. A request with no User-Agent, or a generic one like Python's default, gets a `403 Forbidden` or is blocked outright. This is the SEC's *fair-access* policy: anonymous scraping is banned, identified use is welcome. Set it on every request (as in the snippets above), and read the identifying string from an environment variable (`SEC_USER_AGENT`) so it is configurable and not baked into committed code.

**Rate limits.** The SEC's documented limit is **at most 10 requests per second**, aggregated across all your scripts. Exceed it and you are throttled or temporarily banned by IP. For any loop over many filings, sleep between requests and back off on errors:

```python
import time
for cik in cik_list:
    resp = requests.get(url_for(cik), headers=HEADERS, timeout=30)
    resp.raise_for_status()
    # ... save the response ...
    time.sleep(0.15)   # ~7 req/s, comfortably under the 10/s ceiling
```

`edgartools` handles much of this politeness for you, which is a reason to prefer it for large jobs.

**The reproducible pull.** EDGAR is public, so you *can* cache the raw filings to git, but they are large; cache the raw JSON/HTML to a local `data/raw/edgar/` directory and commit only if size permits, otherwise treat like raw data and commit the pull script + log. The pin that matters for EDGAR is the **accession number**: a 10-K can be amended (a `10-K/A`), so "Apple's FY2023 10-K" is ambiguous, but accession `0000320193-23-000106` is exact. Record the accession number of every filing you used, save the raw document untouched, parse from the saved copy, and log the URL and a content hash. Then if the SEC reformats a page or a firm refiles, your cached raw copy — and your results — do not move.

---

## 7.2.4 FRED — macro and financial time series

**Coverage.** FRED (Federal Reserve Economic Data, St. Louis Fed) is the easiest high-quality data source you will ever use: hundreds of thousands of economic and financial time series — GDP, unemployment, the federal funds rate, CPI, mortgage rates, Treasury yields, exchange rates, the VIX — most updated automatically as the source agencies release them. Free, public, no GMU restriction. This is Maya's macro control (a mortgage-rate or unemployment series to absorb the credit cycle) and a control variable in nearly every project here.

**Key identifiers.** Each series has a short **series ID** — a string like `GDP`, `UNRATE` (unemployment rate), `MORTGAGE30US` (30-year mortgage rate), `DGS10` (10-year Treasury), `FEDFUNDS`. You find IDs by searching FRED's website; the ID *is* the identifier you pass to the API.

**Access path.** Two equivalent routes. `pandas-datareader` needs no key for FRED and returns a tidy DataFrame:

```python
import pandas_datareader.data as web
import datetime
unrate = web.DataReader("UNRATE", "fred",
                        start=datetime.datetime(2010, 1, 1),
                        end=datetime.datetime(2020, 12, 31))
```

The `fredapi` package wants a free API key but gives finer control (release dates, vintages, search):

```python
import os
from fredapi import Fred
fred = Fred(api_key=os.environ["FRED_API_KEY"])   # key from env, never hard-coded
mortgage = fred.get_series("MORTGAGE30US",
                           observation_start="2010-01-01",
                           observation_end="2020-12-31")
```

**Licensing.** FRED data is public, but it *aggregates* series from many original sources (BLS, BEA, OECD), some with their own terms; FRED tags each series with its source and copyright. In practice for student research you can cache and share FRED series freely, but cite the *underlying* source, not just "FRED," per CONVENTIONS §6.

**Rate limits and the revision gotcha.** The FRED API caps you at roughly **120 requests per minute** per key — generous, and only a constraint if you loop over many series. The subtle, important gotcha is **data revision**. Many macro series are *revised* after first release: today's value for 2020 GDP is not the number that was published in 2021. If your study's logic depends on what was *knowable at the time* (a real-time or forecasting design — Sam's backtests, anything event-study-like), pulling the *latest* revised series is a quiet look-ahead bias. FRED solves this with **ALFRED** vintages — `fredapi`'s `get_series_first_release()` or `get_series_as_of_date()` give the number *as it was published then*. For a contemporaneous control variable, the latest series is fine; for anything that pretends to use only past information, pull the vintage.

**The reproducible pull.** Pin the **vintage date** (or note "latest, pulled 2026-05-15"), cache to Parquet, log:

```python
raw = pathlib.Path("data/raw/fred_unrate.parquet")
if raw.exists():
    unrate = pd.read_parquet(raw)
else:
    unrate = web.DataReader("UNRATE", "fred", start, end).reset_index()
    unrate.to_parquet(raw)
    log_pull("logs/pulls.jsonl", "FRED:UNRATE [pulled 2026-05-15, latest vintage]",
             "https://api.stlouisfed.org/.../UNRATE", unrate)
```

Because FRED is small and public, caching it is cheap and there is no excuse not to.

---

## 7.2.5 HMDA — fair-lending data at national scale

**Coverage.** HMDA (the Home Mortgage Disclosure Act data, served by the CFPB) is the near-universe of US mortgage applications: tens of millions of loan *application* records per year, each with the loan amount, the action taken (originated, denied, withdrawn), property location (down to census tract), and — the reason it is the central fair-lending dataset — applicant race, ethnicity, sex, and income. This is Maya's project: did denial rates for first-generation or minority applicants move differently when standards tightened? Public, no license restriction.

**Key identifiers.** HMDA records key on a **Legal Entity Identifier (LEI)** for the lending institution and on geographic codes (state, county, census tract) for location. There is no person-level identifier — these are application records, not a panel of people — which shapes what questions are answerable.

**Access path — and the size problem.** HMDA is *huge*: a single year's national Loan/Application Register (LAR) is several gigabytes and tens of millions of rows. You almost never want all of it. The **CFPB Data Browser API** lets you request *filtered* slices or *pre-aggregated* counts, which is how you keep the pull tractable. The cardinal rule: **aggregate or filter on the server, not after downloading the universe.** The Data Browser's aggregations endpoint returns counts grouped by the variables you specify:

```python
import requests, pandas as pd
# Aggregated counts: applications by action_taken and race, for one state and year.
# This returns a small summary table -- NOT the multi-GB row-level file.
url = "https://ffiec.cfpb.gov/v2/data-browser-api/view/aggregations"
params = {
    "years": "2020",
    "states": "VA",
    "actions_taken": "1,3",          # 1 = originated, 3 = denied
}
resp = requests.get(url, params=params, timeout=60)
resp.raise_for_status()
agg = pd.json_normalize(resp.json()["aggregations"])
```

If you genuinely need row-level data — for a regression with individual controls — pull a *narrow filtered slice* (one state, one year, the columns you need) via the Data Browser's CSV download endpoint, not the full national file. The data card in Appendix C lists the exact endpoints and field codes.

**Licensing.** Public and unrestricted, with one ethical caveat that is not a license term: HMDA contains sensitive demographic data, and although it is published in de-identified form, you should handle it respectfully and never attempt re-identification. No GMU-infrastructure rule applies, but good data hygiene does.

**Rate limits and gotchas.** The CFPB API has no published hard rate limit but will time out on greedy requests, which is itself the lesson: *the throttle is the size.* Ask for an aggregation and you get an instant small table; ask for a state-year of raw records and you get megabytes; ask for the national universe through the API and it will fail. The other gotcha is *schema drift*: HMDA's fields changed materially with the 2018 reporting revision, so a 2017 file and a 2019 file do not have identical columns — pin the year and read that year's data dictionary.

**The reproducible pull.** Pin the **data year** and the exact filter, cache the (small, aggregated) result, log the URL with its query parameters. For HMDA the log is especially valuable because the request *is* the analysis decision — "originated and denied, Virginia, 2020" is a modeling choice you want on the record.

---

## 7.2.6 13F — institutional holdings

**Coverage.** Form 13F is the quarterly report that institutional investment managers with over \$100 million in qualifying US equity assets must file with the SEC, disclosing their long positions: which stocks, how many shares, what market value, as of quarter-end. It is how you see what the big funds *held* — Sam could use it to study whether institutional crowding predicts momentum crashes; Priya could track institutional ownership of climate-exposed insurers. Holdings only, with caveats below.

**Key identifiers.** Holdings are identified by **CUSIP** (a nine-character security identifier) and increasingly by the issuer's name and a count of shares; the filer is identified by CIK. CUSIP is a *licensed* identifier in its full form — a wrinkle that matters for redistribution (below).

**Access path.** Two routes, reflecting two providers. The free, public route is **SEC EDGAR**: 13F filings are just another EDGAR form (`form="13F-HR"`), pulled exactly like the filings in §7.2.3 — same User-Agent rule, same rate limit, same accession-number pinning. The filing's information table (an XML document) lists each holding:

```python
from edgar import Company, set_identity
set_identity(os.environ["SEC_USER_AGENT"])
mgr = Company("0001067983")          # Berkshire Hathaway's CIK, for example
holdings_filings = mgr.get_filings(form="13F-HR")
info_table = holdings_filings.latest().obj().infotable   # one row per holding (CUSIP, shares, value)
```

The licensed, cleaned route is **Thomson Reuters / Refinitiv 13F (the s34 files) on WRDS** — the same holdings, but de-duplicated, with cleaner identifiers and historical depth, and with the same WRDS access pattern and licensing as §7.2.2. Use EDGAR for transparency and exact filings; use the WRDS/Thomson version when you need a clean historical panel (and accept the GMU-infrastructure rule that comes with it).

**Licensing.** The *filings* are public (EDGAR); the *cleaned Thomson panel* is licensed (WRDS, GMU-only). And **CUSIP itself is a licensed identifier** — you can use CUSIPs you obtain to merge your own data, but redistributing a large CUSIP-to-name mapping can violate CUSIP Global Services' license, so do not publish a CUSIP master file. Keep CUSIPs inside your analysis, do not build a product out of them.

**Gotchas — what 13F does *not* tell you.** Three big ones, and they are conceptual, not technical. (1) 13F reports **long positions only** — no shorts, no most derivatives — so it is not the manager's true net exposure. (2) It is filed with a **45-day lag** after quarter-end, so the holdings are stale when you see them; treating a 13F as real-time positioning is a look-ahead error in reverse. (3) Managers can request **confidential treatment** for some positions, so the disclosed table can be incomplete. None of these are bugs in your code; they are limits in the data that your identification has to respect.

**The reproducible pull.** Same as the relevant parent source: for EDGAR 13Fs, pin the accession number and cache the raw XML; for the WRDS/Thomson version, pin the snapshot and keep it on GMU infrastructure. Log the manager CIK (or Thomson key), the quarter, and a content hash.

---

## 7.2.7 USPTO PatentsView — innovation data in bulk

**Coverage.** PatentsView is the USPTO's research-friendly database of US patents: every granted patent and (in recent data) pre-grant application, with inventors, assignees (the firms or people who own the patent), filing and grant dates, citations between patents, and CPC technology classifications, back to 1976 for full text and earlier for metadata. This is Leah's project: patent counts and citation-weighted counts by firm-year as a measure of innovation. Public, no license restriction.

**Key identifiers.** Patents key on a **patent number**; inventors and assignees have PatentsView-assigned **disambiguated IDs** (the database's best guess at "this is the same inventor across patents," which is itself an estimate you should treat with care). The hard part — and it is *the* hard part of patent research — is matching a PatentsView **assignee** to a Compustat firm (a GVKEY), because firm names are messy ("IBM" vs. "International Business Machines Corp" vs. a subsidiary). That match is a Chapter 7.4 problem; PatentsView gives you the assignee name and ID to start from.

**Access path.** PatentsView **migrated to the USPTO Open Data Portal (ODP) on March 20, 2026**; the legacy `api.patentsview.org` endpoints were discontinued in May 2025 and the interim `search.patentsview.org/api/v1` PatentSearch API was paused at the ODP cutover. The current home is `https://api.uspto.gov` (register for a key at `https://data.uspto.gov/apis/getting-started`), and the header name is **`X-API-KEY`** (lowercase). A targeted query looks like:

```python
import os, requests
key = os.environ["USPTO_ODP_API_KEY"]      # env only; CONVENTIONS §5
base = "https://api.uspto.gov"             # pin in config.py
headers = {"X-API-KEY": key}
# The post-cutover patent-search endpoint path is still being finalized on ODP;
# the bulk PatentsView tables are stable today. nb7.2 holds the verified call.
resp = requests.get(f"{base}/api/v1/patent/applications",
                    headers=headers,
                    params={"q": "patentNumber:10000001"},
                    timeout=60)
```

For large extracts — *all* patents for a decade, which is millions of rows — the API is the wrong tool; PatentsView publishes **bulk data downloads** (flat TSV files of the whole database, available today through the ODP "PatentsView Bulk Downloads" page), and you download and load those rather than paginating millions of API calls. Rule of thumb: targeted queries (one firm, one year) go through the API; whole-database extracts come from bulk files. The data card lists both.

**Licensing.** Public domain (US government data); no GMU-infrastructure restriction; cache and share freely. The current ODP API does want a free **API key** (read from `USPTO_ODP_API_KEY`), and the platform has now been versioned and migrated **three** times in two years (legacy → PatentSearch → ODP), so confirm the current endpoint, header name, and path in the data card and the ODP transition guide (`data.uspto.gov/support/transition-guide/patentsview`) before a big run. **[CHECK]** the exact current ODP patent-search endpoint path post-cutover — nb7.2 holds the verified, current call.

**Rate limits and gotchas.** The API enforces per-key rate limits and *pagination* — you must loop through pages, respecting the limit, and a job that ignores this gets throttled. The deeper gotcha is **disambiguation uncertainty**: "the same inventor" and "the same assignee" are statistical guesses, so inventor mobility and firm patent counts inherit that error — a measurement-error issue (Chapter 1.3) you should acknowledge, not paper over. And patents have a **grant lag**: a 2023 *application* may not be *granted* until 2026, so recent years undercount until the data matures — pin your data release and note the truncation.

**The reproducible pull.** Pin the **PatentsView data release** (it updates roughly quarterly; record the release date), cache the raw results (Parquet for API results, the downloaded TSVs for bulk), log the query JSON and a content hash. Because both grant lag and disambiguation change between releases, the release date is a genuine reproducibility pin, not a formality.

---

## 7.2.8 Free alternatives — yfinance, Stooq, Tiingo

Not everyone has WRDS access for every task, and sometimes you just want a quick price series to prototype before committing to the licensed pull. Three free or freemium sources fill that gap — with limits you must understand, because the gap between "free price data" and "research-grade price data" is exactly where naive backtests go to die.

**yfinance.** An unofficial Python wrapper around Yahoo Finance. Free, no key, dead simple:

```python
import yfinance as yf
prices = yf.download("AAPL", start="2010-01-01", end="2020-12-31", auto_adjust=True)
```

The conveniences are real, and so are the dangers. yfinance is *unofficial* — it scrapes an undocumented endpoint that Yahoo can and does change without warning, so a script that works today may break tomorrow (a reproducibility hazard in itself). More seriously for research: Yahoo data has **survivorship bias** (delisted tickers often vanish, so a backtest on "today's tickers" silently drops the losers — exactly the bias CRSP's delisting returns fix), occasional bad ticks and split/dividend-adjustment quirks, and no guaranteed point-in-time integrity. It is fine for learning, prototyping, and teaching; it is not what you submit a finance paper on if CRSP is available.

**Stooq.** A free source of historical daily prices for global stocks, indices, and FX, reachable through `pandas-datareader` (`web.DataReader("AAPL.US", "stooq")`). No key. Coverage is decent and it is a useful *cross-check* against yfinance — if two free sources disagree on a price, you have found a data-quality problem before it found you. Same survivorship and point-in-time caveats apply.

**Tiingo.** A freemium API with a free tier (and a key). It offers cleaner, better-documented end-of-day prices and some fundamentals, with explicit terms of service and rate limits on the free tier (a modest number of requests per hour/day). The key, of course, comes from the environment:

```python
import os, requests
headers = {"Authorization": f"Token {os.environ['TIINGO_API_KEY']}"}   # key from env
resp = requests.get("https://api.tiingo.com/tiingo/daily/AAPL/prices",
                    params={"startDate": "2010-01-01", "endDate": "2020-12-31"},
                    headers=headers, timeout=30)
```

**How to choose, and the honest comparison.** For a *teaching or prototyping* task, or where the asset has no WRDS coverage (some crypto, some foreign small-caps — relevant to Devon), a free source is the right call: it is fast and good enough to develop the pipeline. For a *publishable* equity study where CRSP is available, use CRSP — it is survivorship-bias-free and point-in-time correct, which the free sources are not. The general principle, which is really the theme of this whole chapter: **match the data source to the standard your conclusion must meet.** A backtest you would trade real money on, or a result you would defend to a referee, needs research-grade data; a Tuesday-afternoon prototype does not. Knowing the difference — and disclosing which you used — is the mark of someone who has internalized the craft. And whatever you choose, the reproducible-pull discipline is identical: pin the date you pulled, cache the raw response, log the request. A free source's *instability* makes caching more important, not less, because the only guarantee you have that the numbers will not move is your own cached copy.

```python
raw = pathlib.Path("data/raw/yf_aapl.parquet")
if raw.exists():
    prices = pd.read_parquet(raw)
else:
    prices = yf.download("AAPL", start="2010-01-01", end="2020-12-31", auto_adjust=True)
    prices.to_parquet(raw)
    log_pull("logs/pulls.jsonl", "yfinance:AAPL [pulled 2026-05-15, auto_adjust=True]",
             "yf.download AAPL 2010-2020", prices)
```

---

## 7.2.9 Putting it together — the anatomy of a defensible pull

Step back and notice that every source above, however different its access path, fits the *same* skeleton. That skeleton is the real deliverable of this chapter, and it is worth stating once, cleanly, because it is what you will reuse in PS 7.2 and in your capstone:

1. **Read the data card** (Appendix C) for the source: coverage, identifiers, endpoints, license.
2. **Read secrets from the environment** — keys via `os.environ[...]`, never inline; SEC User-Agent the same way.
3. **Write a bounded, specific query** — only the columns, rows, dates you need; aggregate server-side for huge sources (HMDA), bound dates and select columns for huge tables (CRSP).
4. **Respect the access rules** — the SEC's 10-req/sec ceiling and User-Agent, WRDS's shared-cluster etiquette, each free API's rate limit; sleep and back off.
5. **Pin the snapshot** — WRDS snapshot date, FRED vintage, EDGAR accession number, HMDA data year, PatentsView release. Record *what the data was as of when.*
6. **Cache the raw response to a git-ignored `data/raw/`** and have everything downstream read the cache, never re-hit the source.
7. **Never commit licensed data** (CRSP/Compustat/IBES/TRACE/Thomson) — it stays on GMU infrastructure; commit only the pull code and the log.
8. **Log the pull** — source, query (no secrets), row count, content hash, timestamp — so the request is on the record and changes in the data are detectable.

The directory layout that falls out of this is the one nb7.2 sets up and the one your capstone repo should use:

```
your-project/
├── .gitignore            # excludes data/raw/  and  .env
├── .env                  # your API keys -- NEVER committed
├── code/
│   └── pull_data.py      # the bounded queries; reads keys from env
├── data/
│   └── raw/              # cached raw pulls -- git-ignored; licensed data lives ONLY here
└── logs/
    └── pulls.jsonl       # one line per pull: what, when, how big, content hash
```

A reviewer handed this repository can read `code/pull_data.py` to see *exactly* what you requested, read `logs/pulls.jsonl` to see *when* and *how much*, and — for the public sources — re-run the pull and check the content hash against yours. For the licensed sources they cannot re-run it without GMU access, which is correct: the license forbids you from shipping them the data, but it does not forbid you from shipping the *recipe*, and the recipe plus the log is what makes even licensed-data work as reproducible as the license allows. That asymmetry — public data is fully re-runnable, licensed data is recipe-reproducible-only — is not a loophole; it is the honest best you can do within the rules, and a referee who knows the rules expects exactly that.

One closing reframe of the chapter's whole point. The novice thinks data acquisition is a one-time chore to rush through on the way to the interesting modeling. The researcher knows it is *part of the method* — every pin, every cache, every logged query is a claim about reproducibility that your results stand or fall on, exactly as much as your choice of standard errors or fixed effects. The data card tells you what is possible; the eight-step skeleton tells you how to do it defensibly; and the log on disk is the evidence that you did. Get this right and the rest of Week 7 — the pre-analysis plan, the dataset build, the identification memo — is built on rock. Get it wrong, and you are building on data no one, including future-you, can reconstruct.

---

## Your Turn

**Now open nb7.2 — the multi-source data-pull harness.** It is the runnable, offline-safe version of this chapter: working `log_pull` and cache-or-fetch helpers, a WRDS query stub you can run if you have access (and a cached sample if you do not), live FRED and EDGAR and PatentsView pulls against the public APIs (keys read from the environment), an HMDA aggregation request, and a side-by-side of yfinance vs. Stooq prices so you can *see* the data-quality gaps with your own eyes. By the end you will have a `data/raw/` folder, a `logs/pulls.jsonl` with content hashes, and a `.gitignore` that keeps the licensed bytes where the license requires — the exact scaffolding PS 7.2 asks you to submit for your own source.

**Three questions to carry into the notebook and into your project.**

1. *For your own capstone source, where is the reproducibility most fragile?* Walk your intended pull and find the one place a re-run a year from now would most likely give a different answer — a revised FRED series, an amended 10-K, a re-stated CRSP record, an unstable yfinance endpoint, a new PatentsView release. Name the specific pin (vintage, accession number, snapshot, release date) that would freeze it, and write the one line of your log that would prove you pinned it.

2. *Which of your sources are licensed, and what exactly may you commit?* List each source your project touches and label it public or licensed. For the licensed ones, state precisely what stays on GMU infrastructure and what — code, log, redacted summary — you *can* put in a public repo. If a collaborator outside GMU asked you to "just send the CRSP file," what would you send instead so they could still reproduce your work?

3. *Free or research-grade — and can you defend the choice?* Pick one task in your design where a free source (yfinance/Stooq/Tiingo) and a licensed source (CRSP) both exist. Decide which you will use, and write the two-sentence justification you would put in your methods section — naming the specific data-quality difference (survivorship bias? point-in-time integrity?) that makes your choice the right one for the standard your conclusion must meet.
