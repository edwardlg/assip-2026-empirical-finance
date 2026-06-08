# Solutions — PS 7.2 (A Working Data-Pull Script and Data Card for One Project Source)

**Problem set:** `book/weeks/week-07/ps7.2.md` (PS 7.2, Week 7).
**Chapter:** Ch 7.2 — Data Acquisition in Practice, read through the six-field source treatment and the eight-step defensible-pull skeleton (§7.2.9), with the three cross-cutting rules of §7.2.1 (secrets→env, licensed-data-stays-on-GMU, pin/cache/log).

This is a **model deliverable**, not a list of short answers. PS 7.2 asks each student to build the data-acquisition layer for *their own* capstone source; here we build the complete, A-grade version for **one concrete source — FRED (Federal Reserve Economic Data, St. Louis Fed)** — chosen because it is free, public, and fully demonstrable end-to-end without any license or restricted credential, so the entire artifact can be shown and verified. The voice and conventions follow `CONVENTIONS.md` §5: Python 3.11; secrets via env vars only; the `data/raw/` + `logs/pulls.jsonl` layout; `log_pull` as the audit twin of the Ch 6.5 API log. **No real downloaded FRED values appear anywhere in this document.** Where rows or counts are shown, they are explicitly labeled illustrative; the only "real" thing a student would have is their own `content_sha256`, which is evidence of a pull, not data.

We model this on **Maya**, whose capstone needs a macro control series (the 30-year mortgage rate, `MORTGAGE30US`) to absorb the credit cycle in her HMDA denial-rate study. So her one source for this sheet is **FRED**, and her one series is `MORTGAGE30US`.

Instructor grading notes appear at the end, including the rubric, the automatic-deduction traps, and what separates an A from a B.

---

## Problem 1 — Choose your source and write the reproducibility-risk plan (15 points)

**(a) (3 pts)** *Source:* **FRED.** *Role:* Maya's HMDA denial-rate study needs a contemporaneous macro control that captures how tight credit was each period; she will merge the **30-year fixed mortgage rate (`MORTGAGE30US`, weekly, percent)** onto her HMDA application-year panel as a right-hand-side control so that a denial-rate change attributable to *the credit cycle* is not mistaken for one attributable to *applicant characteristics*. The field the analysis consumes is a single time series — `date` and the rate value — over **2004-01-01 to 2024-12-31**, the window of her HMDA extract.

**(b) (4 pts)** Six-field header for FRED:

| Field | Maya's FRED entry |
|---|---|
| (i) Coverage | Hundreds of thousands of US macro/financial series; here `MORTGAGE30US`, weekly avg 30-yr fixed mortgage rate, 1971–present. |
| (ii) Key identifiers | The **series ID** string (`MORTGAGE30US`) is the identifier; observations key on `date`. |
| (iii) Access path | `fredapi.Fred` (free key) or `pandas_datareader` (no key); one call returns a tidy Series/DataFrame. |
| (iv) License + GMU rule | **Public**; *no* GMU-infrastructure restriction. Cite the *underlying* source (Freddie Mac PMMS), not just "FRED," per CONVENTIONS §6. |
| (v) Rate limit / gotcha most likely to bite | **Revision / vintage**: the latest series is the *revised* number; for a point-in-time design this is a quiet look-ahead bias. (Rate cap ≈120 req/min is not a constraint for one series.) |
| (vi) Reproducible-pull pin | **Vintage date**: record "latest vintage, pulled 2026-05-15" (or pull an ALFRED `as_of` vintage for a point-in-time design). |

**(c) (5 pts) Reproducibility-risk plan.** The single most fragile point in Maya's pull is **FRED data revision**: `MORTGAGE30US` is comparatively stable, but FRED series in general are re-stated as source agencies revise, and a re-run "as of today" a year from now can return a different vintage of the same dates — so "the latest series" is not reproducible. The pin that freezes it: **record the vintage** in the log (and, if her design ever uses only-past-information, pull an ALFRED `get_series_as_of_date()` vintage rather than the latest). The log line that *proves* the pin (illustrative `n_rows`/hash):

```json
{"timestamp": "2026-05-15T14:02:11.482913+00:00", "source": "FRED:MORTGAGE30US [pulled 2026-05-15, latest vintage]", "query": "https://api.stlouisfed.org/fred/series/observations?series_id=MORTGAGE30US&observation_start=2004-01-01&observation_end=2024-12-31", "n_rows": 1096, "n_cols": 2, "content_sha256": "9f1c0e7a...ILLUSTRATIVE...d3b8"}
```

If a reviewer re-ran the pull and the `content_sha256` did **not** match this line, they would conclude that the underlying data moved between her pull and theirs — a revision, a vintage change, or a different query — and that her analysis must be re-pinned to the exact vintage before her numbers can be reproduced.

**(d) (3 pts)** A "data revision" (or PatentsView "disambiguation uncertainty") is a concrete instance of **Ch 1.3 measurement error**: the recorded value differs from the true point-in-time quantity, and using the revised number where the contemporaneous one belongs is a systematic, direction-known error, not just noise. The `log_pull` line is "the data-acquisition twin" of the **Ch 6.5 API audit log** because both answer the same six-months-later question — *exactly what did I ask for, when, and did the response change?* — by recording the request, the timestamp, the size, and a content hash, so the provenance of every number is reconstructable.

---

## Problem 2 — The working pull script (35 points)

Maya's `code/pull_data.py`. It is env-gated, bounded, polite, cache-first, pinned, and fails safe. (FRED via `pandas_datareader` needs **no key**; she also shows the `fredapi` key-from-env variant in a comment so the env pattern is explicit. Either way, no secret literal appears.)

```python
"""
code/pull_data.py — reproducible FRED pull for Maya's HMDA macro control.
Source: FRED series MORTGAGE30US (30-yr fixed mortgage rate, weekly).
Eight-step defensible pull (Ch 7.2 §7.2.9). Public source; no GMU restriction.
NO hard-coded secrets. NO network at import time.
Run:  python code/pull_data.py      (pandas-datareader path needs no key)
"""

import hashlib
import json
import datetime
import pathlib
import pandas as pd

# ---- (Step 1) Source spec: see data-cards/fred.md ----
SERIES_ID = "MORTGAGE30US"
START = "2004-01-01"        # (Step 5) pin: Maya's HMDA window
END = "2024-12-31"          #          bounded date range -> reproducible scope
RAW = pathlib.Path("data/raw/fred_mortgage30us_2004_2024.parquet")  # git-ignored dir
LOGFILE = "logs/pulls.jsonl"
VINTAGE_NOTE = "pulled 2026-05-15, latest vintage"   # (Step 5) the pin, in words


def log_pull(logfile, source, query, df):
    """(Step 8) Append one JSON line: what, when, how big, content hash. No secrets."""
    record = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source": source,
        "query": query,                 # URL/SQL only; NEVER a key
        "n_rows": int(len(df)),
        "n_cols": int(df.shape[1]),
        # hash over canonical CSV -> stable across machines, changes iff data changes
        "content_sha256": hashlib.sha256(df.to_csv(index=False).encode()).hexdigest(),
    }
    pathlib.Path(logfile).parent.mkdir(parents=True, exist_ok=True)
    with open(logfile, "a") as f:
        f.write(json.dumps(record) + "\n")


def fetch_fred():
    """(Step 2) secrets-from-env, (Step 3) bounded query, (Step 4) respect access rules.

    pandas-datareader's FRED reader needs NO key. If you instead use fredapi, the
    key is read from the environment, never hard-coded:

        # import os
        # from fredapi import Fred
        # fred = Fred(api_key=os.environ["FRED_API_KEY"])   # KeyError if unset = safe
        # s = fred.get_series(SERIES_ID, observation_start=START, observation_end=END)

    requests/readers are imported INSIDE the function so importing this module
    never touches the network.
    """
    import pandas_datareader.data as web   # lazy import: no network at module import
    # (Step 3) bounded: ONE series, the exact date window the analysis needs.
    # FRED's free reader has a generous ~120 req/min cap; one call is far under it,
    # so no sleep/back-off loop is needed here. (A multi-series loop WOULD add
    # time.sleep(...) between requests -- the politeness pattern, shown for the record.)
    s = web.DataReader(SERIES_ID, "fred", START, END)
    df = s.reset_index()
    df.columns = ["date", SERIES_ID.lower()]   # tidy, named columns
    return df


def cache_or_fetch():
    """(Steps 6 & 8) Cache-first: read cache on hit; hit source ONLY on miss, then
    freeze the raw response to disk and log. Downstream reads the cache, never the
    live source -- which makes analysis fast AND freezes the input so a re-run is
    byte-identical."""
    if RAW.exists():
        return pd.read_parquet(RAW), True          # cache HIT: source not touched
    df = fetch_fred()                              # cache MISS: hit the source once
    RAW.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(RAW)                             # write untouched response to cache
    log_pull(
        LOGFILE,
        f"FRED:{SERIES_ID} [{VINTAGE_NOTE}]",      # (Step 5) pin baked into the name
        ("https://api.stlouisfed.org/fred/series/observations"
         f"?series_id={SERIES_ID}&observation_start={START}&observation_end={END}"),
        df,
    )
    return df, False


if __name__ == "__main__":
    # (Step 7) Public source -> the cached Parquet MAY be committed (it is small);
    # were this licensed (CRSP/Compustat), data/raw/ stays git-ignored and only this
    # script + the log are committed.
    df, was_cached = cache_or_fetch()
    print(f"{'cache hit' if was_cached else 'fetched + cached + logged'}: "
          f"{len(df)} rows, columns={list(df.columns)}")
```

**Clause-by-clause defense (mapping to the rubric):**

**(a) (6 pts) Secrets from the environment.** The `pandas-datareader` FRED path needs no key, stated in a comment; the `fredapi` alternative reads `os.environ["FRED_API_KEY"]` and would raise `KeyError` if unset (the safety mechanism). There is **zero** secret string literal; a grep for `api_key=`, `token=`, `password=` assigned to a literal returns nothing.

**(b) (6 pts) Bounded, specific query.** One series, the exact `2004-01-01`–`2024-12-31` window the HMDA panel needs — not "all of FRED," not the full series history. The comment states the bound implements the Problem-1(a) scope.

**(c) (6 pts) Respect the access rules.** FRED's ~120 req/min cap is acknowledged; a single call is far under it, so no sleep is needed — but the comment shows the `time.sleep(...)` politeness pattern that a *multi-series loop* would require, because the *pattern* is what is graded. (Had this been EDGAR, the script would set the `User-Agent` from `SEC_USER_AGENT` on every request and `time.sleep(0.15)` in the loop.)

**(d) (7 pts) Cache-or-fetch.** `cache_or_fetch()` reads `data/raw/fred_mortgage30us_2004_2024.parquet` on a hit and hits FRED only on a miss, then writes the untouched response and logs. The docstring states the dual payoff: fast analysis *and* a frozen input so re-runs are byte-identical.

**(e) (6 pts) Pin the snapshot.** The `START`/`END` bound the data; `VINTAGE_NOTE = "pulled 2026-05-15, latest vintage"` is baked into the logged source name, so the record says "as of when," not "the latest." For a point-in-time design the comment points to the ALFRED `as_of` vintage call.

**(f) (4 pts) Runs end-to-end / fails safe.** Imports of `pandas_datareader` are *inside* `fetch_fred`, so importing the module touches no network. Confirmation a student should report: "Ran `python code/pull_data.py`; first run fetched + cached + logged, second run printed `cache hit` and did not network. Confirmed no import-time network by `python -c 'import pull_data'` with no outbound traffic." (For the `fredapi` variant: `env -i python code/pull_data.py` exits with a clear `KeyError: 'FRED_API_KEY'` and never reaches the network.)

---

## Problem 3 — The audit log and the snapshot proof (15 points)

**(a) (6 pts)** The `log_pull` helper is included in the script above and called on the cache-miss branch. The exact JSON line it writes (illustrative `n_rows`/hash, labeled):

```json
{"timestamp": "2026-05-15T14:02:11.482913+00:00", "source": "FRED:MORTGAGE30US [pulled 2026-05-15, latest vintage]", "query": "https://api.stlouisfed.org/fred/series/observations?series_id=MORTGAGE30US&observation_start=2004-01-01&observation_end=2024-12-31", "n_rows": 1096, "n_cols": 2, "content_sha256": "9f1c0e7a...ILLUSTRATIVE...d3b8"}
```

It carries the UTC timestamp, the source name **with the pin baked in**, the query URL, the row/column counts, and the content hash. The `query` field is safe to commit even when data is not because it stores only the *request* — a public URL with no key (FRED's free reader carries none; the `fredapi` key would ride in a header/param that is *never* placed in the logged string). Logging the recipe is always safe; logging the data is what the license forbids.

**(b) (5 pts)** The `content_sha256` turns "did the data change since I pulled it?" into a one-line check: hash the current pull and compare to the logged hash — equal means byte-identical, unequal means something upstream moved. Operationally, if the *same* query produces two *different* hashes a month apart, the source revised, re-stated, or re-released the data between pulls, and the analysis must be re-pinned to a fixed vintage before its numbers are reproducible. This hash is exactly the alarm that fires when Maya's Problem-1(c) fragile pin (FRED revision) slips.

**(c) (4 pts)** What gets committed for FRED: `code/pull_data.py`, `logs/pulls.jsonl`, `data-cards/fred.md`, and `.gitignore`. Because **FRED is public and `MORTGAGE30US` is tiny**, the cached `data/raw/fred_mortgage30us_2004_2024.parquet` *may* also be committed (size permitting) — there is no license bar. Were the source **licensed** (CRSP/Compustat/Thomson 13F), the `data/raw/` Parquet must **never** be committed; what makes that pull still "recipe-reproducible" to an outside reader is the §7.2.9 asymmetry: they receive the *script + log* (the recipe and the evidence of what was pulled), and although they cannot re-run it without GMU access, the recipe plus the content hash is the honest best the license allows.

---

## Problem 4 — The one-page data card (25 points)

The model `data-cards/fred.md`. (In the repo this is its own file; reproduced here as the deliverable.)

```markdown
# Data Card — FRED (Federal Reserve Economic Data)

**Source slug:** `fred` · **Card owner:** Maya · **Last reviewed:** 2026-05-15
**Series used in this project:** MORTGAGE30US (30-yr fixed mortgage rate, weekly, %)

## Provider and coverage
Aggregator: **FRED, Federal Reserve Bank of St. Louis.** FRED *re-publishes*
hundreds of thousands of series from original agencies; cite the UNDERLYING
source, not "FRED" (CONVENTIONS §6). For MORTGAGE30US the underlying source is
**Freddie Mac, Primary Mortgage Market Survey (PMMS)**. Coverage: 1971-present,
weekly (Thursday), national average 30-yr fixed rate, percent. Most series
update automatically as the source agency releases them.

## Identifiers
- Primary identifier: the **series ID** string, e.g. `MORTGAGE30US`,
  `UNRATE`, `DGS10`, `FEDFUNDS`. The ID *is* what you pass to the API.
- Observations key on `date`.
- Crosswalk note (out of scope here, Ch 7.4): merging a FRED macro series onto a
  firm/loan panel is a date-alignment/frequency-merge problem, not an ID match.

## Access path
- `pandas_datareader` — **no key required**:
  `web.DataReader("MORTGAGE30US", "fred", start, end)`.
- `fredapi` — free key, finer control (vintages, search). Key from env:
  ```python
  import os
  from fredapi import Fred
  fred = Fred(api_key=os.environ["FRED_API_KEY"])   # KeyError if unset = safe
  s = fred.get_series("MORTGAGE30US",
                      observation_start="2004-01-01",
                      observation_end="2024-12-31")
  ```
- No secret literal ever appears in code; the key (if used) is read from
  FRED_API_KEY at runtime.

## License and the GMU note
**PUBLIC.** No GMU-infrastructure restriction; cache and share freely. One
caveat: FRED aggregates series whose underlying sources carry their own terms,
so cite the underlying source (Freddie Mac PMMS here). No license bars
committing the cached file, but apply the data/raw/ discipline uniformly.

## Gotchas
- **Revision / vintage (the big one):** the default series is the *revised*
  number. For any design that may use only-past-information, pull an ALFRED
  vintage (`get_series_as_of_date` / `get_series_first_release`); for a
  contemporaneous control the latest series is fine, but RECORD the vintage.
- **Frequency mismatch:** MORTGAGE30US is weekly; a yearly HMDA panel needs an
  explicit aggregation choice (year mean? year-end?) -- a Ch 7.4 step, flagged here.
- **Rate cap:** ~120 requests/min per key; only a constraint when looping over
  many series.

## First rows (ILLUSTRATIVE — not real pulled data; types/shapes only)
| date (datetime64) | mortgage30us (float64, percent) |
|---|---|
| 2004-01-01        | <float, ~6.x>                   |
| 2004-01-08        | <float, ~6.x>                   |
| 2004-01-15        | <float, ~6.x>                   |
(Schema sketch to show the expected columns and dtypes; values are placeholders,
not quoted from FRED.)

## Where this is used
- Consumed as a macro control in Maya's HMDA denial-rate analysis (Week 7
  capstone build) and demonstrated in nb7.2 (`pull_fred`).
- [CHECK] carried forward from Ch 7.2 §7.2.7 applies to PatentsView, NOT FRED;
  FRED's endpoint/auth are stable. (Noted so the reader knows which card owns the CHECK.)
```

**Section credit:** (a) provider+coverage names Freddie Mac PMMS, not just FRED — 4 pts. (b) identifiers name the series ID and flag the Ch 7.4 crosswalk — 3 pts. (c) access path shows both routes, env-gated, no secrets — 4 pts. (d) license = public + the underlying-source citation — 4 pts. (e) gotchas: revision/vintage, frequency, rate cap — 4 pts. (f) first-rows sketch is labeled illustrative, types only — 3 pts. (g) names the downstream use (capstone + nb7.2) and correctly states the PatentsView `[CHECK]` does not bite FRED — 3 pts.

---

## Problem 5 — Licensing and repository-hygiene check (10 points)

**(a) (4 pts)** FRED is **public**. The `.gitignore` Maya commits:

```gitignore
# secrets and raw pulls
.env
data/raw/
# (FRED is public + tiny, so its cached parquet MAY be force-added if desired:
#   git add -f data/raw/fred_mortgage30us_2004_2024.parquet
#  -- but licensed sources NEVER get this exception.)
```

After a successful pull, `git status` should show the new `data/raw/*.parquet` as **ignored** (not staged, not "untracked" in the changeset) — proving the raw cache is excluded by default — unless Maya deliberately force-adds the public FRED file.

**(b) (3 pts)** If a teammate outside GMU asked Maya to "just send the data file": because FRED is **public**, she may simply send the cached Parquet *and* the `pull_data.py` + `logs/pulls.jsonl` so they can verify the content hash. Were her source **licensed** (CRSP), she would send **only the recipe** — the script and the log — never the bytes, and tell the teammate to re-run it inside their own GMU access; the content hash lets them confirm they reproduced her exact extract.

**(c) (3 pts)** FRED carries no sensitive personal data, so the rule that bites here is **redistribution/attribution**, not re-identification: Maya must cite the *underlying* source (Freddie Mac PMMS), not just "FRED," per CONVENTIONS §6, and she should not pass off the aggregated series as her own collection. (Contrast: had her source been HMDA, the non-license data-hygiene rule would be **never attempt re-identification** of the de-identified applicant demographics, and handle the race/ethnicity/sex/income fields respectfully.)

---

## Problem 6 — Reflection: the one pin you would defend to a referee

Maya's reflection sentence: *"My most fragile point is FRED data revision — the `MORTGAGE30US` series I merged in is the latest vintage, which can be re-stated, so I pin it by recording the pull vintage (`pulled 2026-05-15, latest vintage`) in `logs/pulls.jsonl` with a content hash, and in the methods section I disclose: 'The 30-year mortgage-rate control is taken from FRED (Freddie Mac PMMS) at the latest vintage as of 2026-05-15; because this is a contemporaneous control rather than a real-time forecasting input, the revised vintage is appropriate, and the exact extract is reproducible from the logged query and content hash.'"* That sentence names the data property at stake (revision / point-in-time integrity), the pin that freezes it, and why the choice is defensible for *this* design — the mark of treating acquisition as part of the method.

---

## Instructor grading notes

**Rubric (100 points).** Problem 1: 15 · Problem 2: 35 · Problem 3: 15 · Problem 4: 25 · Problem 5: 10. Problem 6 is required but un-pointed; dock the completeness/professionalism band if it is missing.

**Two automatic large deductions (these dominate the grade).**
1. **Any hard-coded secret** — an `api_key="..."`, a WRDS username/password literal, a token, or a 20+-char hex/base64 string in the script: cap the Problem-2 score at roughly half and flag prominently, regardless of how clean the rest is. Grep every submission for `api_key=`, `token=`, `password=`, `pgpass`, and long literals. (The *only* acceptable key-literal anywhere is the explicit anti-pattern shown as "what NOT to do," and only in prose.)
2. **Committed licensed raw data** — a CRSP/Compustat/Thomson Parquet or CSV tracked in git, or a `data/raw/` that is not git-ignored for a licensed source: this is the CONVENTIONS §5 red line. Cap Problem 5 and dock Problem 2(d)/3(c). Public-source data in `data/raw/` is fine (the FRED exemplar even commits it deliberately); the violation is specifically *licensed* bytes.

**What separates an A from a B.**
- **A:** the cache-or-fetch genuinely hits the source only on a miss *and* the student can state how they verified no import-time network; the pin is baked into the *logged source name* (not just a loose comment); the data card cites the *underlying* source and labels the first-rows sketch illustrative; the reproducibility-risk plan names a *specific* fragile pin and the *exact* log line that freezes it.
- **B:** the script runs and reads keys from env, but the pin is vague ("pulled recently"), the data card omits a section or cites only the aggregator, or the risk plan is generic ("data could change") without naming the pin or the hash check.
- **C and below:** missing log, no cache (re-hits the source every run), or — short of the automatic deductions — a query that is unbounded (`SELECT *`, full-file download) where the source is huge.

**Source-specific allowances.** Students who chose a **licensed** source (CRSP/Compustat) cannot demonstrate a live run; accept a script with a cached-sample fallback (as nb7.2 does) and grade the *discipline* (env gate, snapshot pin, GMU-only note, "commit recipe not data") rather than a live pull. Students who chose **EDGAR/HMDA/PatentsView** must show the `User-Agent`/rate-limit politeness and (for PatentsView) carry the §7.2.7 `[CHECK]` forward rather than silently inventing the endpoint. Students who chose **yfinance/Stooq** must name survivorship bias / point-in-time integrity in the data card's gotchas, not treat the free source as research-grade.

**Common errors to expect.** (i) Logging the full URL *with* an embedded `api_key=` query param — the key leaks into a committable file; require the redaction. (ii) Caching to CSV and hashing the Parquet bytes (or vice-versa) so the hash is unstable across machines — the exemplar hashes canonical CSV for exactly this reason. (iii) A cache that writes *after* a transform, freezing cleaned rather than raw data — the cache must hold the untouched response. (iv) Treating "pin" as the *pull date* alone when the design is point-in-time — for a forecasting/event-study design the vintage (ALFRED `as_of`), not just the calendar date, is the real pin.

**The one-sentence standard.** A submission earns the A when a stranger handed the folder could, for a public source, re-run the script and match the logged content hash — and for a licensed source, read the recipe and the log and know *exactly* what was pulled even though they cannot pull it themselves. That asymmetry, done honestly, is the whole skill.
