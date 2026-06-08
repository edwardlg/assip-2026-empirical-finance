# Appendix C — Data Dictionary Master

This appendix is the camp's catalog of the datasets you will actually touch. There is one *data
card* per source. A data card is a one-page briefing that tells you what a dataset is, what it
covers, how to pull it without leaking secrets, and — most importantly — the specific ways it will
quietly mislead you if you are careless. The cards exist so that when a chapter, lab, or capstone
says "use CRSP monthly returns" or "pull `UNRATE` from FRED," you can flip here and learn the source
on its own terms instead of guessing. They are reference pages, not tutorials: read the relevant
card before you write the pull script, and keep it open while you debug the join.

## What every card looks like (the fixed 8-part format)

Every card in this appendix follows the same eight-part structure, in the same order. Once you have
read two or three, you know where to look on all 34.

1. **Provider & what it is** — who maintains the data, what one row means, and the
   *reveal-the-trick* point: the single thing about this source that separates someone who uses it
   correctly from someone who gets a plausible-looking but wrong answer.
2. **Coverage** — the span (how far back), the frequency (daily/monthly/quarterly/…), and the
   universe (which firms, people, securities, or geographies are in and which are silently out).
3. **Key identifiers** — the primary key you query and join on (e.g. CRSP's `PERMNO`, a FRED series
   ID, an SEC `CIK`/accession number), and which "obvious" identifiers (tickers, raw CUSIPs) will
   betray you if you join on them.
4. **Access path** — a runnable Python snippet using the Chapter 7.2 pattern: credentials from the
   environment (never hard-coded), a bounded query (never `SELECT *`), and the cache-or-fetch idiom
   so a re-run reads from disk instead of hammering the source.
5. **License & GMU-infrastructure note (§5)** — whether the source is free/public or licensed, and
   exactly what you may and may not do with the bytes. See the rule below.
6. **Gotchas** — the concrete traps: missing-value codes, revisions and look-ahead bias, frequency
   mismatches, sign conventions, coverage breaks. This is the part that saves your capstone.
7. **"First 10 rows" schema sketch** — an *illustrative* table showing the shape and types of the
   data. Every such table is explicitly labeled fabricated; the numbers are invented to teach a
   gotcha, not to be cited as real data.
8. **Which chapter / lab / capstone uses it** — where the source shows up in the curriculum and
   which member of the student cast (Maya, Devon, Priya, Sam, Leah) leans on it.

## The licensing rule that governs this appendix (CONVENTIONS §5)

The sources here split into two kinds, and the difference is not cosmetic.

**Free / public sources** (FRED, SEC EDGAR, Census/BLS/BEA, Treasury, PatentsView, the free equity
APIs, and the rest) you may pull on your own laptop, cache, and even commit the raw file to git if
you like. The discipline still applies uniformly anyway — pin the snapshot or vintage, cache to
`data/raw/`, log the pull, and cite the *underlying* agency, not just the delivery service — because
reproducibility, not licensing, is the reason.

**Licensed sources** (the WRDS-delivered databases — CRSP, Compustat, IBES, OptionMetrics, Capital
IQ, Thomson 13F, the TRACE academic file, Mergent FISD — plus any licensed muni or bank file) are
different. GMU pays for the *right to use* them under terms that forbid redistributing the raw
records. The hard consequences of CONVENTIONS §5:

- You may query licensed data **only on GMU infrastructure** — WRDS Cloud or the **Hopper** cluster
  — and the connection is **read-only**.
- Your derived extract is cached to a **git-ignored** `data/raw/` directory.
- The licensed bytes are **never** committed to a repo, emailed off campus, posted publicly, or
  pasted into any commercial web service (including consumer AI chatbots).
- Credentials live in **environment variables** only (e.g. `${WRDS_USERNAME}`), never hard-coded.
- Every notebook that touches licensed data **pins its snapshot date** (the CRSP/Compustat vintage).

What travels between people is the **recipe** — your query code and your pull log — not the data.
Anyone with their own GMU WRDS seat can re-run your code and regenerate the extract; that is
reproducibility done *within* the license. When a card says "stays on GMU infrastructure," this is
the rule it means.

## Index of cards

Links point to the card files in `../../../data-cards/`. Cards marked **[licensed / WRDS]** are
governed by the §5 rule above.

### Markets & corporate data [licensed / WRDS]

- [CRSP](../../../data-cards/crsp.md) — survivorship-free U.S. stock prices, returns, and delisting returns back to 1925/26.
- [Compustat](../../../data-cards/compustat.md) — S&P Global standardized company fundamentals (balance sheet, income, cash flow).
- [IBES](../../../data-cards/ibes.md) — analyst earnings estimates: consensus and detail (broker-level) forecasts.
- [OptionMetrics (IvyDB US)](../../../data-cards/optionmetrics.md) — historical U.S. equity/index option prices, implied vols, and Greeks.
- [Capital IQ](../../../data-cards/capital-iq.md) — S&P Capital IQ via WRDS, including the Key Developments event feed.
- [Thomson Reuters / SEC 13F](../../../data-cards/thomson-13f.md) — the cleaned, licensed institutional-holdings panel (s34).
- [TRACE](../../../data-cards/trace.md) — corporate-bond transaction tape; the academic Enhanced TRACE stays GMU-only.
- [Mergent FISD](../../../data-cards/mergent-fisd.md) — fixed-income securities reference and ratings; pairs with TRACE.

### Federal Reserve & bank regulators

- [FRED](../../../data-cards/fred.md) — St. Louis Fed's free macro/financial time-series aggregator (cite the underlying agency).
- [FFIEC Call Reports](../../../data-cards/ffiec-call-reports.md) — quarterly regulatory financials for every U.S. commercial bank.
- [FR Y-9C](../../../data-cards/fr-y9c.md) — consolidated financial statements for bank holding companies.
- [FDIC](../../../data-cards/fdic.md) — BankFind Suite: institution directory, SDI financials, and bank-failure history.
- [HMDA](../../../data-cards/hmda.md) — Home Mortgage Disclosure Act loan-application register; the fair-lending workhorse.
- [CFPB Consumer Complaints](../../../data-cards/cfpb-complaints.md) — consumer-finance complaint database with free-text narratives.

### SEC EDGAR (free / public filings)

- [EDGAR 10-K / 10-Q](../../../data-cards/edgar-10k-10q.md) — annual and quarterly reports; the primary disclosure documents.
- [EDGAR 8-K](../../../data-cards/edgar-8k.md) — material-event filings; the text corpus for Capstone 4 classification.
- [EDGAR DEF 14A](../../../data-cards/edgar-def14a.md) — proxy statements: governance, compensation, pay-vs-performance.
- [EDGAR 13F](../../../data-cards/edgar-13f.md) — institutional holdings, the free parsing path (vs. the licensed Thomson panel).
- [EDGAR N-PORT](../../../data-cards/edgar-nport.md) — registered-fund portfolio holdings.
- [EDGAR XBRL](../../../data-cards/edgar-xbrl.md) — structured (machine-readable) financial-statement data.

### Treasury, FINRA & municipals

- [U.S. Treasury + FINRA TRACE](../../../data-cards/treasury-finra.md) — Treasury auctions and the daily par-yield curve, plus the public FINRA TRACE tape.
- [MSRB EMMA](../../../data-cards/msrb-emma.md) — municipal-securities disclosures and trades; bulk muni data stays on GMU infra.

### Census, BLS & BEA (government statistics)

- [Census ACS + County Business Patterns](../../../data-cards/census-acs.md) — demographics, income, and county-level establishment counts.
- [BLS](../../../data-cards/bls.md) — Bureau of Labor Statistics: employment, wages, CPI.
- [BEA](../../../data-cards/bea.md) — Bureau of Economic Analysis: national and regional (county) GDP.
- [USAspending.gov](../../../data-cards/usaspending.md) — federal awards (contracts and grants); UEI/DUNS recipient keys.

### Patents & innovation

- [USPTO PatentsView](../../../data-cards/uspto-patentsview.md) — patent bibliographic data via the PatentSearch API.
- [NBER / KPSS Patent–Compustat Links](../../../data-cards/nber-patent-link.md) — crosswalk from patents to firms, with the public KPSS patent-value file.

### Climate & disaster

- [NOAA + FEMA](../../../data-cards/noaa-fema.md) — NOAA Billion-Dollar Disasters / Storm Events and FEMA disaster declarations.

### Free finance APIs

- [Free equity price APIs](../../../data-cards/free-equity-apis.md) — yfinance / Stooq / Tiingo / Alpha Vantage; the CRSP fallback, with its survivorship caveat.

### Text & macro

- [FOMC text + GDELT](../../../data-cards/fomc-gdelt-text.md) — FOMC statements/minutes/speeches and the GDELT global-news corpus.
- [Loughran–McDonald dictionary](../../../data-cards/loughran-mcdonald-dict.md) — finance-tuned sentiment word lists; the transparent cousin of an LLM label.

### Crypto

- [Crypto / on-chain](../../../data-cards/crypto-onchain.md) — Etherscan / CoinGecko / DeFiLlama for on-chain activity and prices.

### International

- [International macro](../../../data-cards/international-macro.md) — ECB SDW · BIS · IMF IFS · World Bank WDI · OECD.Stat.

---

**Count: 34 cards.** Every link above resolves to a real file in `data-cards/`; no card implied by
this index is missing.
