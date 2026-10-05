# Data Cards — Appendix C source dictionary

These are the **Appendix C — Data Dictionary Master** cards: one per dataset the camp uses. Each
card follows the same fixed 8-part format (Provider & what it is · Coverage · Key identifiers ·
Access path · License & GMU-infra note · Gotchas · "first 10 rows" schema sketch · which
chapter/lab/capstone uses it). For the full explanation of the format and the index by category,
see the Appendix C front page: [`../book/appendices/C-data-dictionary/README.md`](../book/appendices/C-data-dictionary/README.md).

**Licensing rule (CONVENTIONS §5).** Free/public sources may be pulled, cached, and committed on any
machine — but still pin the vintage and cite the underlying agency. **Licensed sources** (the
WRDS-delivered databases below — CRSP, Compustat, IBES, OptionMetrics, Capital IQ, Thomson 13F, the
TRACE academic file, Mergent FISD — plus any licensed muni/bank file) may be queried **only on GMU
infrastructure** (WRDS Cloud or Hopper), read-only; the raw bytes are cached to a git-ignored
`data/raw/`, **never** committed, emailed off campus, posted publicly, or pasted into a commercial
web service. Credentials come from environment variables only, and every notebook pins its snapshot
date. What travels is the recipe — your query code and pull log — not the data.

## Cards by category

### Markets & corporate data [licensed / WRDS]
- [crsp.md](crsp.md) — survivorship-free U.S. stock prices, returns, and delisting returns.
- [compustat.md](compustat.md) — S&P Global standardized company fundamentals.
- [ibes.md](ibes.md) — analyst earnings estimates (consensus and detail).
- [optionmetrics.md](optionmetrics.md) — historical U.S. option prices, implied vols, Greeks (IvyDB US).
- [capital-iq.md](capital-iq.md) — S&P Capital IQ via WRDS, incl. Key Developments.
- [thomson-13f.md](thomson-13f.md) — cleaned, licensed institutional-holdings panel (s34).
- [trace.md](trace.md) — corporate-bond transaction tape; academic Enhanced TRACE stays GMU-only.
- [mergent-fisd.md](mergent-fisd.md) — fixed-income securities reference and ratings.

### Federal Reserve & bank regulators
- [fred.md](fred.md) — St. Louis Fed macro/financial time-series aggregator.
- [ffiec-call-reports.md](ffiec-call-reports.md) — quarterly regulatory financials for U.S. banks.
- [fr-y9c.md](fr-y9c.md) — consolidated financials for bank holding companies.
- [fdic.md](fdic.md) — BankFind Suite: directory, SDI financials, bank failures.
- [hmda.md](hmda.md) — Home Mortgage Disclosure Act loan-application register.
- [cfpb-complaints.md](cfpb-complaints.md) — consumer-finance complaints with free-text narratives.

### SEC EDGAR (free / public filings)
- [edgar-10k-10q.md](edgar-10k-10q.md) — annual & quarterly reports.
- [edgar-8k.md](edgar-8k.md) — material-event filings.
- [edgar-def14a.md](edgar-def14a.md) — proxy statements (governance, compensation).
- [edgar-13f.md](edgar-13f.md) — institutional holdings, the free parsing path.
- [edgar-nport.md](edgar-nport.md) — registered-fund portfolio holdings.
- [edgar-xbrl.md](edgar-xbrl.md) — structured financial-statement data.

### Treasury, FINRA & municipals
- [treasury-finra.md](treasury-finra.md) — Treasury auctions + daily par-yield curve; public FINRA TRACE tape.
- [msrb-emma.md](msrb-emma.md) — municipal-securities disclosures and trades.

### Census, BLS & BEA (government statistics)
- [census-acs.md](census-acs.md) — ACS demographics/income + County Business Patterns.
- [bls.md](bls.md) — Bureau of Labor Statistics: employment, wages, CPI.
- [bea.md](bea.md) — Bureau of Economic Analysis: national & regional GDP.
- [usaspending.md](usaspending.md) — federal awards (contracts and grants).

### Patents & innovation
- [uspto-patentsview.md](uspto-patentsview.md) — patent bibliographic data via PatentSearch API.
- [nber-patent-link.md](nber-patent-link.md) — patent–Compustat crosswalk + public KPSS value file.

### Climate & disaster
- [noaa-fema.md](noaa-fema.md) — NOAA Billion-Dollar Disasters / Storm Events + FEMA declarations.

### Free finance APIs
- [free-equity-apis.md](free-equity-apis.md) — yfinance / Stooq / Tiingo / Alpha Vantage (CRSP fallback).

### Text & macro
- [fomc-gdelt-text.md](fomc-gdelt-text.md) — FOMC statements/minutes/speeches + GDELT global news.
- [loughran-mcdonald-dict.md](loughran-mcdonald-dict.md) — finance sentiment word lists.

### Crypto
- [crypto-onchain.md](crypto-onchain.md) — Etherscan / CoinGecko / DeFiLlama.

### International
- [international-macro.md](international-macro.md) — ECB SDW · BIS · IMF IFS · World Bank WDI · OECD.Stat.

_34 cards total._
