# Data Card — FOMC Text (statements / minutes / speeches) + GDELT Global News

**Provider & what it is.** Two free sources of *text as data* — raw language you turn into numbers and feed to a regression. **FOMC text** is the public communication of the U.S. Federal Open Market Committee, published by the Federal Reserve Board: the post-meeting **statements** (a few hundred words, released the day of the rate decision), the **minutes** (released three weeks later, a detailed account), the **speeches** and testimony of Fed officials, and — released with a five-year lag — the full meeting **transcripts**. Because each item is precisely dated and the FOMC moves markets, the text is a workhorse for monetary-policy and tone studies: you score a statement's *hawkishness* (a sentiment measure, Ch 6.3) and ask whether it predicts the market reaction in a tight window. **GDELT** (the Global Database of Events, Language, and Tone) is a massive, continuously updated index of the world's news media — every monitored article tagged with a timestamp, detected themes, named entities, locations, and an *average tone* score. The reveal: both are firehoses of unstructured text, and the entire skill is turning that text into a *validated measurement* (a sentiment score, an event count) without fooling yourself — exactly the Week 6 lesson.

**Coverage.** FOMC: statements and minutes from the mid-1990s to present (the Fed began releasing statements in 1994); speeches archive going back decades; transcripts 1936–present but lagged five years. Eight scheduled meetings a year, plus occasional intermeeting actions. GDELT: global news, GDELT 1.0 from 1979 and the richer GDELT 2.0 updating every 15 minutes since early 2015, hundreds of languages (machine-translated), billions of rows.

**Key identifiers.** For FOMC: the **meeting date** (and release date — *not* the same for minutes, which matters for any event study). For GDELT: the **GKG record id** and a 15-minute timestamp; events are keyed by date, actor codes (CAMEO), location (FIPS/geo), and source URL. The common spine for joining either to market data is the **date/timestamp** — and for FOMC you must be careful *which* date (decision day vs. minutes-release day).

**Access path.** Both free, no key required for the core data.

```python
import requests, pandas as pd

# FOMC: pages are public HTML/PDF on federalreserve.gov; scrape politely.
# Use a descriptive User-Agent and sleep between requests.
hdr = {"User-Agent": "GMU-research student leigao.gmu@gmail.com"}
url = "https://www.federalreserve.gov/newsevents/pressreleases/monetary20231101a.htm"
html = requests.get(url, headers=hdr, timeout=60).text  # then parse out the statement text

# GDELT 2.0: query the GKG via the public DOC 2.0 API (JSON), no key
gdelt = requests.get("https://api.gdeltproject.org/api/v2/doc/doc",
                     params={"query": "Federal Reserve interest rates",
                             "mode": "ArtList", "format": "json",
                             "startdatetime": "20231101000000",
                             "enddatetime": "20231102000000"},
                     timeout=60).json()
```

GDELT also ships raw bulk files (the Events, Mentions, and GKG tables) as CSV on a public server, and the whole corpus is mirrored as a public **Google BigQuery** dataset (`gdelt-bq.gdeltv2.*`) — useful when the volume is too big to download. No key for the raw files; BigQuery uses your Google Cloud credentials (`GOOGLE_APPLICATION_CREDENTIALS` from the environment, never in code).

**License & note.** FOMC materials are U.S. federal government works, effectively **public domain** — cache, redistribute, and commit freely; cite "Board of Governors of the Federal Reserve System." **GDELT** is distributed free for any use (the project states it is open) `[CHECK exact license terms and any attribution requirement`; cite GDELT and the access window. Both being open is a relief after the licensed WRDS world — but note GDELT *links to* news articles it does not own, so you store the metadata and tone, not the copyrighted article bodies.

**Gotchas.**
- **Which FOMC date?** A statement is released on decision day; the minutes for that meeting come out ~3 weeks later and are *new information on their own release date*. An event study that times the minutes to the meeting date instead of the release date has a look-ahead/timing bug (Ch 1.5). Pin both dates.
- **Tone is a noisy instrument.** GDELT's "average tone" and any dictionary score (Ch 6.3) is a *measurement* of sentiment, not sentiment itself — validate it against hand labels out of sample before it enters a regression (Ch 6.5). A confident score is not a true score.
- **GDELT volume and dedup.** The same story appears in hundreds of outlets; raw article counts measure *media attention/syndication* as much as events. Decide whether you want events or coverage, and deduplicate.
- **Machine translation and coverage drift.** GDELT's language and source coverage expanded over time, so a rising count is partly better monitoring, not just more news. GDELT 1.0 vs 2.0 are not seamlessly comparable across the 2015 boundary.
- **HTML/PDF parsing is researcher discretion (DOF).** How you strip boilerplate from an FOMC page or PDF changes your word counts. Fix and document the parser; respect the SEC-style etiquette (descriptive User-Agent, sleep, back off) on federalreserve.gov.

**First 10 rows — schema sketch (illustrative; values invented, not real records).**

| doc_id | source | doc_type | event_date | release_date | n_words | tone | hawk_score | url |
|---|---|---|---|---|---|---|---|---|
| FOMC-2023-11-01-S | FOMC | statement | 2023-11-01 | 2023-11-01 | 412 | -0.8 | 0.31 | federalreserve.gov/...20231101a.htm |
| FOMC-2023-11-01-M | FOMC | minutes | 2023-11-01 | 2023-11-22 | 9120 | -1.2 | 0.44 | federalreserve.gov/...minutes20231101.htm |
| FOMC-2023-12-13-S | FOMC | statement | 2023-12-13 | 2023-12-13 | 401 | 0.3 | 0.18 | federalreserve.gov/...20231213a.htm |
| FOMC-SPEECH-7741 | FOMC | speech | 2023-11-09 | 2023-11-09 | 3180 | -0.5 | 0.52 | federalreserve.gov/...powell20231109.htm |
| GKG-20231101-0931 | GDELT | news | 2023-11-01 | 2023-11-01 | — | -2.7 | — | reuters.com/...fed-holds-rates |
| GKG-20231101-1015 | GDELT | news | 2023-11-01 | 2023-11-01 | — | 1.4 | — | bloomberg.com/...powell-presser |
| GKG-20231101-1042 | GDELT | news | 2023-11-01 | 2023-11-01 | — | -0.6 | — | ft.com/...rate-decision |
| GKG-20231101-1130 | GDELT | news | 2023-11-01 | 2023-11-01 | — | -3.1 | — | wsj.com/...markets-react |
| GKG-20231213-1402 | GDELT | news | 2023-12-13 | 2023-12-13 | — | 2.9 | — | cnbc.com/...fed-signals-cuts |
| GKG-20231213-1455 | GDELT | news | 2023-12-13 | 2023-12-13 | — | 0.2 | — | apnews.com/...fomc-statement |

(`hawk_score` here is an *illustrative* dictionary tone you would compute and then validate; GDELT rows carry GDELT's own `tone` instead.)

**Which chapter/lab/capstone uses it.** This is **Week 6** text-as-data territory. The methods come from Ch 6.3 (Loughran–McDonald finance sentiment — the transparent dictionary you would apply to FOMC statements) and Ch 6.5 (the AI co-pilot, where an LLM tone label is treated as a *measurement* to be validated), with Mentor Session 6 ("Text as data, and AI without fooling yourself") tying it together. A monetary-policy **capstone** in the spirit of **Capstone 5 (FRED Macro Event Study)** is the natural home: score FOMC statement tone, line it up with the rate decision date and a tight market-reaction window, and run a properly-inferred event study — or use GDELT news tone around the announcement as an alternative measure and cross-check the two. You would acquire and document it via the **Ch 7.2 / Lab 7** reproducible-pull discipline (pin both the decision and release dates; cache the parsed text).
