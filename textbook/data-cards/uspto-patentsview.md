# Data Card — USPTO PatentsView (now USPTO Open Data Portal)

**Source slug:** `uspto-patentsview` · Appendix C (Data Dictionary) · last touched 2026-05-30

## Provider & what it is

PatentsView is a research-facing platform built for the U.S. Patent and Trademark Office (USPTO) to make the patent record *queryable and disambiguated*. The raw USPTO bulk files are an enormous pile of grant and application documents; PatentsView's contribution is to clean them and resolve who is who and what is what. It exposes the things an innovation researcher actually needs: **patents** (grant number, title, filing date, grant date, technology class); **inventors** (the people named on a patent, with a disambiguated `inventor_id` so "J. Smith" at two firms is correctly split or merged); **assignees** (the organization that owns the patent — the firm, with a disambiguated `assignee_id`); and **citations** (which patents cite which, the raw material for impact measures). The reveal-the-trick point: a patent dataset looks like clean structured data, but the two hardest things in it — *which named entity is the same entity* and *when did the innovation actually happen* — are not given to you. They are inferred, and the inference can be wrong.

## Coverage

Granted U.S. utility patents from **1976 to the present** for the full structured detail (some fields, like backward citations and classifications, extend coverage; pre-1976 patents exist only as images, not parsed text). Pre-grant **published applications** are also available (from 2001 onward, when the U.S. began publishing applications). The data are updated on a roughly quarterly cadence. Geography is global at the inventor/assignee level (U.S. patents are filed by inventors worldwide), but the *grant* is always a U.S. patent.

## Key identifiers

`patent_id` (the grant number, e.g. `10000000`), `inventor_id` and `assignee_id` (PatentsView's *disambiguated* entity keys — the whole reason to use PatentsView over raw bulk), CPC/USPC technology classification codes, and the citation edge list (`citation_patent_id` → `cited_patent_id`). For finance work the load-bearing join is **assignee → firm**: PatentsView gives you a disambiguated assignee organization name and id, and you must crosswalk that to a Compustat `gvkey` / CRSP `permno` to study firm outcomes (see the companion `nber-patent-link` card — PatentsView does *not* ship a firm-identifier link itself).

## Access path (bulk + ODP API; key via env)

**The API moved — twice in two years.** As of May 2026 the current product is the **USPTO Open Data Portal (ODP)**, base URL `https://api.uspto.gov` (registration and key request at `https://data.uspto.gov/apis/getting-started`), and every request requires an **`X-API-KEY`** header (lowercase header name; the value is the key string). The **legacy** PatentsView API (`api.patentsview.org/...`) was discontinued **May 1, 2025** and now returns HTTP 410 Gone. The intermediate **PatentSearch API** at `https://search.patentsview.org/api/v1` (which used the same `X-Api-Key` header) was paused on **March 20, 2026**, the date PatentsView migrated to ODP; some search functions, visualizations, and support were paused at the cutover and are being reintroduced on ODP "as the transition progresses" (USPTO subscription notice). Pin the base URL and header name in `config.py` so a single edit re-points the whole packet when ODP reintroduces the patent-search endpoint(s).

```python
import os, requests
key = os.environ["USPTO_ODP_API_KEY"]      # env only; CONVENTIONS §5
base = "https://api.uspto.gov"             # ODP; pin in config.py
headers = {"X-API-KEY": key}               # lowercase header name per ODP docs

# The ODP patent-search endpoint path is being finalized post-cutover [CHECK
# the current path under `${base}/api/v1/...` against data.uspto.gov when you
# run]; the bulk PatentsView tables are stable on ODP today.
r = requests.get(f"{base}/api/v1/patent/applications",
                 headers=headers, params={"q": "patentNumber:10000001"},
                 timeout=60)
```

For panel-scale work, pull the **bulk PatentsView tables** (flat TSV/parquet downloads of patents, inventors, assignees, citations) — they are already available through the ODP "PatentsView Bulk Downloads" page and are the right tool for whole-decade extracts. The API is for targeted queries; bulk files are for building the whole panel.

## License (FREE / public) & note

PatentsView data are derived from the public U.S. patent record and released for free use; the underlying patent documents are **U.S. Government works in the public domain**, and PatentsView's disambiguated tables are distributed under an open attribution license [CHECK exact license string against the ODP "PatentsView Bulk Downloads" landing page — historically CC-BY, but confirm post-March-2026 ODP terms]. Free to redistribute in a replication packet; cite PatentsView (and the disambiguation method paper) as the source of the *disambiguated* ids, not just "USPTO." No GMU-only constraint; the ODP API key is free but rate-limited, so cache and pin a snapshot date.

## Gotchas

- **Disambiguation is a *model*, not ground truth.** `inventor_id` and `assignee_id` are produced by a machine-learning disambiguation algorithm. It makes two kinds of errors: *splitting* one real entity into two ids, and *lumping* two real entities into one. Both bias any count you build (inventor productivity, firm patent stock). The reveal-the-trick lesson is to treat the id as an estimate with error, and to sanity-check the biggest assignees by hand. The disambiguation also changes between data vintages, so an `assignee_id` is **not stable across releases** — pin the vintage.
- **Grant lag.** A patent's *filing* date and its *grant* date can be years apart (commonly 2–4 years, sometimes much longer). If you date innovation by grant date you systematically push it forward in time and truncate recent years (the "right-censoring" / *truncation* problem: recent applications haven't been granted yet, so recent years look artificially low). KPSS-style value measures key off the *grant* announcement for the market reaction but date the *invention* by filing — keep the two dates distinct, and never compute a "patents per year" trend on grant date without correcting for truncation.
- **Citation truncation.** Forward citations accumulate over time, so newer patents *mechanically* have fewer citations. Comparing raw citation counts across cohorts is the classic apples-to-oranges error; deflate by cohort (or use a fixed citation window).
- **Assignee ≠ firm, and ownership moves.** The named assignee is the entity at grant; patents get reassigned, subsidiaries file under their own names, and the parent-firm rollup is *your* job (see `nber-patent-link`). Foreign and individual assignees will not match any Compustat firm.
- **API shape changed twice.** Field names, nesting (`assignees.assignee_organization`), and pagination differ between the legacy `api.patentsview.org` endpoints (discontinued May 2025), the interim `search.patentsview.org/api/v1` PatentSearch API (paused March 20, 2026), and the current `api.uspto.gov` ODP endpoints. Old tutorials, StackOverflow answers, and even early-2026 blog posts target dead endpoints; confirm against the ODP "Transition Guide" at `data.uspto.gov/support/transition-guide/patentsview` before copying any sample code.

## "First 10 rows" — schema sketch (ILLUSTRATIVE, not real values)

`patent` endpoint, flattened one row per (patent × assignee):

| patent_id | patent_title | patent_date | filing_date | assignee_organization | assignee_id | cpc_section |
|-----------|--------------|-------------|-------------|-----------------------|-------------|-------------|
| 10000001 | Method for battery thermal mgmt | 2018-06-19 | 2015-03-02 | Tesla, Inc. | a9f3... | H |
| 10000002 | Neural network accelerator | 2018-06-19 | 2014-11-20 | NVIDIA Corporation | b2c1... | G |
| 10000003 | Lipid nanoparticle formulation | 2018-06-19 | 2013-09-10 | Moderna, Inc. | c7e8... | A |
| 10000004 | Payment tokenization system | 2018-06-19 | 2016-01-15 | Visa International | d4a2... | G |
| 10000005 | Drilling fluid composition | 2018-06-19 | 2012-07-30 | (individual inventor) | e9b0... | C |

Citation edge list (`g_us_patent_citation`-style):

| citing_patent_id | cited_patent_id | citation_date |
|------------------|-----------------|---------------|
| 10000002 | 8500000 | 2018-06-19 |
| 10000002 | 9100000 | 2018-06-19 |
| 10000003 | 7800000 | 2018-06-19 |

(Illustrative only; do not cite. Note `patent_date` − `filing_date` ≈ 3 years per row — that is the grant lag, drawn deliberately.)

## Which chapter / lab / capstone uses it

- **Week 6, Ch 6.1 (Reader's Guide — Kogan, Papanikolaou, Seru & Stoffman 2017)** — PatentsView supplies the patent universe, grant dates, and citations behind the KPSS market-based patent-value construction; the grant-lag and citation-truncation gotchas above are the exact measurement traps Ch 6.1 dissects in "what's vulnerable," and the disambiguation caveat anchors the Week-1 construct-vs-measure thread.
- **Capstone 3 — Innovation from USPTO PatentsView** — the headline source: students build a patent-based innovation measure and run a firm-outcome event study on grant dates (ties to KPSS 2017), confronting truncation and the assignee→firm crosswalk head-on.
- **Leah's running thread (patents, innovation, text analysis)** — Leah is the cast member anchored to this dataset across Week 6 worked examples.
- **Week 7, Ch 7.2 (Data Acquisition in Practice)** — PatentsView is named explicitly as a free-source pull, with rate-limit and bulk-vs-API discussion.
