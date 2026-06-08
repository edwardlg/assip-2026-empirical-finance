# PS 7.2 — A Working Data-Pull Script and Data Card for One Project Source

**Course:** 8-Week Empirical Finance Camp · Week 7 · Problem Set 7.2
**Covers:** Ch 7.2 (Data Acquisition in Practice), read through the chapter's two organizing devices — the **six-field source treatment** (*coverage · key identifiers · access path · licensing and the GMU-infrastructure rule · rate limits and gotchas · the reproducible pull*) and the **eight-step defensible-pull skeleton** of §7.2.9. It also leans on the three cross-cutting rules of §7.2.1 (secrets live in environment variables; licensed data stays on GMU infrastructure; a pull is reproducible only if it is pinned, cached, and logged), the `log_pull` audit helper, and the `data/raw/` repository layout. It reaches back to **Week 6** (Ch 6.5's API audit log — `log_pull` is its data-acquisition twin) and **Week 1** (Ch 1.3's measurement error, which several "gotchas" are concrete instances of). The runnable, offline-verified reference for every pattern you will use is **nb7.2**, the multi-source data-pull harness (`notebooks/week-07/nb7.2-multi-source-data-pull-harness.ipynb`).

**Tools and constraints allowed:** only what Ch 7.2 and the prior weeks have given you — Python 3.11 with `pandas`, `requests`, `pyarrow`, and whichever single source-specific package your chosen source needs (`fredapi` or `pandas-datareader`, `edgartools`, `wrds`, `yfinance`); the `os.environ[...]` pattern for reading keys; the cache-or-fetch `if raw.exists():` idiom; the `log_pull` JSONL helper from §7.2.1; the `.gitignore` / `data/raw/` / `logs/pulls.jsonl` layout of §7.2.9; and the six-field data-card template. You do **not** need any merging, cleaning, winsorizing, or crosswalk logic — that is Chapter 7.4. You stop the moment a clean *raw* file sits on disk with a log line beside it.

**Total: 100 points.** Point values are stated per deliverable component. This is a *project-scaffolding* problem set, not a numerical one: you are building the actual data-acquisition layer of your capstone, and we grade the **reproducibility and discipline** of what you build, not a final answer. A script that runs but hard-codes a key, or a data card that omits the license, loses heavily even if it "works."

**A note on the numbers.** Do **not** paste any real downloaded values into this submission. Where your data card sketches the first few rows of a source, that sketch must be **illustrative and explicitly labeled** — column names and plausible *shapes* of values (a date, a float, a category code), never actual rows you pulled. The point of the first-rows sketch is to show you know the *schema*, not to redistribute data (which, for a licensed source, you may not do at all). If you genuinely ran your script against a public API, your `logs/pulls.jsonl` content hash is the evidence that you pulled — the values stay out of the writeup.

**The two non-negotiables (read before you write a line of code).** These come straight from CONVENTIONS §5 and Ch 7.2 §7.2.1, and violating either is an automatic large deduction regardless of how polished the rest is:

1. **Never hard-code a key.** No API key, password, token, or WRDS username appears as a string literal anywhere in your script. Every secret is read at runtime from an environment variable (`os.environ["..."]`). The SEC `User-Agent` identity string is read the same way. If the variable is unset, your script should fail loudly (a `KeyError` or a clear message) — that is the safety mechanism working, not a bug.
2. **Never commit licensed raw data.** If your source is licensed (CRSP, Compustat, IBES, TRACE, the Thomson/Refinitiv 13F panel), the raw bytes live only in a git-ignored `data/raw/` directory on GMU infrastructure; you commit the *pull script* and the *log*, never the data. Public sources (FRED, EDGAR, HMDA, PatentsView, yfinance/Stooq) have no such restriction, but you apply the same `data/raw/` discipline uniformly.

**What you are building.** Pick **one** data source that your capstone project will actually use. (If your project touches several, pick the one you are least sure how to pull — that is where this practice pays off.) For that one source you will produce two artifacts: a **working, reproducible pull script** and a **one-page data card**. Together they are the data-acquisition layer a referee or a future-you can pick up and re-run. The five-student cast from Ch 7.1–7.2 is your model: Maya→HMDA or FRED, Devon→EDGAR (an exchange S-1), Priya→Compustat (licensed) or EDGAR 10-K text, Sam→CRSP (licensed) or yfinance/Stooq, Leah→USPTO PatentsView. Choose yours and commit to it for the whole sheet.

**The difficulty curve.** Problem 1 is the design decision — *which* source, and a written reproducibility-risk plan before you touch code. Problem 2 is the heart: the actual pull script, graded clause by clause against the eight-step skeleton. Problem 3 is the audit log and the snapshot pin — the evidence layer. Problem 4 is the one-page data card. Problem 5 is the licensing and repo-hygiene check that decides what may be committed. Problem 6 is a short reflection that ties your source's single most fragile pin to a sentence you could defend in a methods section.

---

## Problem 1 — Choose your source and write the reproducibility-risk plan (15 points)

Before any code, the design decision and the honest accounting of where it can go wrong.

**(a) (3 pts)** Name the **one** source you are building for and, in two sentences, state the *specific* role it plays in your capstone — not "I need price data" but "I need a daily total-return series for my momentum backtest universe, 2010–2024." Name the variable(s) or fields your analysis ultimately consumes, so the pull's scope is pinned to the question.

**(b) (4 pts)** Fill in the **six-field header** for your source, one short line each, exactly as Ch 7.2 frames every source: (i) coverage (what is in it and over what span), (ii) key identifiers (the codes you query and later merge on), (iii) access path (the package or endpoint), (iv) licensing and the GMU rule (public, or licensed-and-GMU-only?), (v) the single rate-limit-or-gotcha most likely to bite *you*, and (vi) the reproducible-pull pin you will use (snapshot date / FRED vintage / EDGAR accession number / HMDA data year / PatentsView release). This is the spec you will then implement.

**(c) (5 pts) The reproducibility-risk plan.** Walk your intended pull and identify the **one place** a re-run a year from now would most likely give a *different* answer — a revised FRED series, an amended 10-K, a re-stated CRSP record, an unstable yfinance endpoint, a new PatentsView release. Name the specific pin that would freeze it, and write the **one line of `logs/pulls.jsonl`** (the JSON record) that would *prove* you pinned it. Then state in one sentence what a reviewer would conclude if they re-ran your pull and the `content_sha256` did **not** match the one in your log.

**(d) (3 pts)** State, in one sentence each: which Week-1 idea a "data revision" or "disambiguation uncertainty" gotcha is a concrete instance of (Ch 1.3), and why your `log_pull` audit line is "the data-acquisition twin" of the Week-6 API audit log (Ch 6.5) — i.e., what question both logs let you answer six months later.

---

## Problem 2 — The working pull script (35 points)

Write `code/pull_data.py` (or a single notebook cell) that pulls your one source. It must run end-to-end on a fresh env *given the right environment variables*, and must follow the eight-step skeleton of §7.2.9. Submit the script and a short note on how you ran it (or, if you have no key/access, how it would run). Grading is by clause:

**(a) (6 pts) Secrets from the environment.** Read every key, token, password, or identity string from `os.environ[...]` — never a literal. If your source needs no key (FRED via `pandas-datareader`, yfinance, Stooq), say so explicitly in a comment and show the one access detail that *is* required instead (e.g., the SEC `User-Agent` for EDGAR, read from `SEC_USER_AGENT`). Your script must contain **zero** secret string literals; a grader will grep for `api_key=`, `token=`, `password=` assigned to a literal and for any 20+-character hex/base64 string.

**(b) (6 pts) A bounded, specific query.** Request only the columns, rows, and dates you need. For a huge source, push the work to the server: aggregate server-side for HMDA, bound the dates and `SELECT` only named columns for CRSP — never `SELECT *` on a 100M-row table, never download the national HMDA file to filter locally. State in a comment *why* your query is bounded the way it is (which Problem-1(a) scope it implements).

**(c) (6 pts) Respect the access rules.** Honor your source's etiquette: the SEC `User-Agent` header on every request plus a `time.sleep(0.15)` in any loop to stay under the 10-requests-per-second ceiling; WRDS shared-cluster manners (bounded chunks, `db.close()`); each free API's rate limit. Show the back-off or sleep, even if your demo pulls only one object — it is the *pattern* that is graded.

**(d) (7 pts) Cache-or-fetch.** Implement the §7.2 spine: check a `data/raw/<file>.parquet` cache, read it on a hit, hit the source *only* on a miss, then write the untouched response to the cache. Everything downstream reads the cache, never the live source. Use the `if raw.exists():` idiom (or the `cache_or_fetch` helper from nb7.2). Explain in one comment why this both makes your analysis fast *and* freezes the input so a re-run gives identical numbers.

**(e) (6 pts) Pin the snapshot.** Encode your Problem-1(b)(vi) pin into the pull: the WRDS snapshot date in a comment and the log; the FRED `observation_end` / vintage call; the exact EDGAR accession number; the HMDA `years=` parameter; the PatentsView data-release note. The pinned pull must say "the data *as of when*," not "the latest data."

**(f) (4 pts) Runs end-to-end / fails safe.** The script must either complete cleanly when the env vars are set, or fail with a clear, single message when they are not — and must *not* network at import time. State which behavior yours exhibits and how you confirmed it (e.g., "ran with `env -i python pull_data.py` and it exited with a clear `KeyError` naming the missing var, never touching the network").

---

## Problem 3 — The audit log and the snapshot proof (15 points)

The log is the evidence layer. This problem is about `logs/pulls.jsonl` and the pin it records.

**(a) (6 pts)** Include the `log_pull` helper (from §7.2.1 / nb7.2) and call it after your cache-miss pull. Show the **exact JSON line** your pull writes (illustrative values are fine for `n_rows`/hash if you did not actually run it, clearly labeled). It must contain: a UTC timestamp, the source name *with the pin baked in* (e.g., `"FRED:MORTGAGE30US [pulled 2026-05-15, latest vintage]"`), the query **with any secret stripped**, the row and column counts, and a `content_sha256`. State in one sentence why the `query` field is safe to commit even when the data is not.

**(b) (5 pts)** Explain the `content_sha256` move in two sentences: how a single hash turns "did the data change since I pulled it?" into a one-line check, and what it means operationally if the same query produces two *different* hashes a month apart. Then connect this to your Problem-1(c) fragile pin — the hash is the alarm that goes off when that pin slips.

**(c) (4 pts)** State precisely *what gets committed to git* for your source's pull: the script, the log, the `.gitignore`. For a public source, may the cached `data/raw/` Parquet also be committed (size permitting)? For a licensed source, why must it never be — and what, then, makes even your licensed-data pull "recipe-reproducible" to an outside reader (the asymmetry of §7.2.9)?

---

## Problem 4 — The one-page data card (25 points)

Write `data-cards/<your-source-slug>.md` — the spec sheet a teammate returns to while coding, the fuller reference Ch 7.2 calls the "data card in Appendix C." One page, the sections below, each a short paragraph or tight list. Grading is by section presence *and* correctness.

**(a) (4 pts) Provider and coverage.** Who publishes it (the *underlying* agency, not just the aggregator — cite BLS/BEA, not only "FRED," per CONVENTIONS §6), what is in it, and the time span and frequency.

**(b) (3 pts) Identifiers.** The primary key(s) you query and later merge on, named exactly (PERMNO, GVKEY, CIK + accession, LEI + census tract, patent number + disambiguated assignee ID, FRED series ID), and one line on which crosswalk to *another* dataset's key is a Chapter 7.4 problem (so the reader knows it is out of scope here).

**(c) (4 pts) Access path.** The package or endpoint, the auth mechanism (which `os.environ` var, or "no key — `User-Agent` required"), and a two-to-four-line code skeleton of the call (env-gated, no secrets).

**(d) (4 pts) License and the GMU note.** Public or licensed. If public, a one-line note on the underlying source's terms and the citation you owe. If licensed, the full sentence of the GMU-infrastructure rule: stays on WRDS Cloud / Hopper, never to a laptop, never to a public repo, never pasted into a commercial web service.

**(e) (4 pts) Gotchas.** The two or three traps specific to this source — the ones from Ch 7.2 plus any you found — each in one line: e.g., RET-vs-RETX and separate delisting table (CRSP); FRED revision / ALFRED vintage; HMDA 2018 schema drift; EDGAR fair-access `User-Agent` 403; 13F long-only / 45-day lag; PatentsView grant lag and disambiguation uncertainty; yfinance survivorship bias.

**(f) (3 pts) First-rows sketch.** An **illustrative, labeled** sketch of the first few rows: the column names you will actually receive and the *type/shape* of each value (a `date`, a `float64` return, a category code), with a one-line "ILLUSTRATIVE — not real pulled data" caption. No real downloaded values.

**(g) (3 pts) Which chapter/lab/notebook uses it.** Name where this source is consumed downstream in *your* project (which chapter's analysis, nb7.2, your capstone build step), so the card is wired into the project, not orphaned. Carry forward any `[CHECK]` the chapter flagged (e.g., the PatentsView base-URL/auth `[CHECK]` from §7.2.7) rather than silently resolving it.

---

## Problem 5 — Licensing and repository-hygiene check (10 points)

The discipline that keeps you out of real trouble.

**(a) (4 pts)** Label your source **public** or **licensed**, and write the `.gitignore` lines that protect this project (at minimum `data/raw/` and `.env`). State in one sentence what a `git status` should show *after* a successful pull — i.e., that the new Parquet under `data/raw/` is *untracked-and-ignored*, not staged.

**(b) (3 pts)** Answer the §7.2.9 collaborator question for *your* source: if a teammate outside GMU asked you to "just send the data file," what would you send instead so they could still reproduce your work? Be specific to whether your source is public (you can send the cached file) or licensed (you can send only the recipe — script + log).

**(c) (3 pts)** HMDA-style ethics, even where no license restricts you: if your source carries sensitive demographic or personal data (HMDA's applicant race/ethnicity/sex/income), state the one data-hygiene rule that is *not* a license term but you follow anyway (no re-identification attempts; handle respectfully). If your source has no such data, say so and name instead the one *redistribution* caveat that does bite it (e.g., CUSIP master files cannot be republished; FRED series owe the underlying-source citation).

---

## Problem 6 — Reflection: the one pin you would defend to a referee (deliverable, ungraded-for-points, required for submission)

In three to four sentences, name the single most fragile point in your pull (your Problem-1(c) answer), the exact pin that freezes it, and the one sentence you would put in your capstone's methods section to disclose it — naming the specific data property at stake (revision / point-in-time integrity / survivorship bias / amendment / disambiguation). This is the sentence that tells a referee you treated data acquisition as *part of the method*, not a chore. (Required; a submission without it is incomplete.)

---

## Submission checklist

Submit a single folder (or a link to a git repo) containing, at minimum:

- [ ] `code/pull_data.py` — the env-gated, cache-or-fetch, logged pull script (Problem 2). **No secret literals.**
- [ ] `logs/pulls.jsonl` — at least one pull record with the pin in the source name and a `content_sha256` (Problem 3). **No secrets in the `query` field.**
- [ ] `data-cards/<your-source-slug>.md` — the one-page data card, all seven sections (Problem 4).
- [ ] `.gitignore` — excludes `data/raw/` and `.env` (Problem 5).
- [ ] A short `README.md` or top-of-script note: your Problem-1 source choice + role, your Problem-1(c) reproducibility-risk plan, the Problem-5 public/licensed label, and the Problem-6 reflection sentence.
- [ ] **Confirm and state explicitly:** no API key, token, password, or username appears as a string literal anywhere; and (if licensed) no raw data bytes are committed — only the script and the log.

**Point summary.** Problem 1: 15 · Problem 2: 35 · Problem 3: 15 · Problem 4: 25 · Problem 5: 10 · **Total: 100.** Problem 6 is a required (un-pointed) reflection; an incomplete submission without it is marked down for completeness.

---

*End of PS 7.2. When you have built everything, check yourself against `book/appendices/E-solutions-manual/E-w7-ps7.2-solutions.md`, which works the whole deliverable end-to-end for one concrete free public source (FRED) at the A-grade standard — an env-gated cache-or-fetch pull script, a complete one-page data card, and the log line that proves the pin. The runnable, offline-safe reference for every pattern here is `nb7.2` (`notebooks/week-07/nb7.2-multi-source-data-pull-harness.ipynb`); your job in this problem set is to take one of its source stubs and turn it into the real, documented, committed-with-discipline data layer of your own project.*
