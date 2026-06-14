# Data Card — International Macro: ECB SDW · BIS · IMF IFS · World Bank WDI · OECD.Stat

**Provider & what it is.** Five official statistical agencies that publish *cross-country* macroeconomic and financial series — the data you reach for when your question spans more than one country (exchange rates, interest rates, GDP, inflation, credit, debt, banking). **ECB SDW** (European Central Bank Statistical Data Warehouse, now the **ECB Data Portal**) serves euro-area and EU monetary, financial, and banking series. **BIS** (Bank for International Settlements) is the central banks' bank: policy rates, effective exchange rates, credit-to-GDP gaps, debt securities, and the property-price and global-liquidity statistics. **IMF IFS** (International Financial Statistics, via the IMF Data portal) is the classic cross-country panel of balance-of-payments, monetary, exchange-rate, and national-accounts series. **World Bank WDI** (World Development Indicators) is the broad development panel — GDP, population, financial-sector depth, poverty, governance — for nearly every country and decades of years. **OECD.Stat** (now the OECD Data Explorer) covers OECD and partner economies across national accounts, labor, finance, and more. The reveal: these are the *free* public counterparts to Bloomberg's international terminal — each is authoritative for its niche, none is a perfect superset of the others, and the entire craft is knowing which provider owns the series you need and joining them on consistent country codes.

**Coverage.** Country × indicator × time (mostly annual or quarterly; some monthly/daily for financial series). World Bank WDI: ~200+ countries, 1960–present, thousands of indicators. IMF IFS: ~190 members, monthly/quarterly/annual back decades. BIS: dozens of reporting countries, varying start dates by dataset. ECB: euro area / EU, with deep monthly financial detail. OECD: ~38 members plus partners. All are revised over time — pin a vintage where the level matters.

**Key identifiers.** The join key is the **country code**, and the *standards differ by provider*, which is the classic merge bug. World Bank uses **ISO 3-letter** codes (`USA`, `DEU`, `JPN`) and its own region/income aggregates; IMF uses ISO codes *and* its own numeric **IFS country codes**; OECD and ECB use ISO/2- or 3-letter plus SDMX dimension codes; BIS uses ISO 2-letter in many datasets. Series themselves are identified by an **indicator code** (World Bank: `NY.GDP.MKTP.CD`; IMF: an SDMX series key) and a **frequency** (`A`/`Q`/`M`). Build an explicit country-code crosswalk before merging across providers, and keep codes as strings.

**Access path.** All free, mostly no key. Several speak the **SDMX** standard, and `pandasdmx`/`sdmx1` can talk to ECB, OECD, IMF, and others; the World Bank has a simple REST API (and the `wbgapi`/`world_bank_data` packages):

```python
import requests
import wbgapi as wb   # World Bank — no key

# World Bank WDI: GDP (current US$) for a few countries, tidy long format
gdp = wb.data.DataFrame("NY.GDP.MKTP.CD", ["USA", "DEU", "JPN"], time=range(2015, 2024))

# IMF IFS via the SDMX/JSON API (no key); series key is provider-specific
imf = requests.get("https://dataservices.imf.org/REST/SDMX_JSON.svc/"
                   "CompactData/IFS/Q.US.PMP_IX",  # [CHECK] exact IFS series key
                   timeout=60).json()

# ECB Data Portal (SDMX): e.g., euro-area MRO policy rate
ecb = requests.get("https://data-api.ecb.europa.eu/service/data/FM/"
                   "B.U2.EUR.4F.KR.MRR_FR.LEV",   # [CHECK] exact key
                   params={"format": "jsondata"}, timeout=60).json()
```

Most need no credential. Where a provider does issue an API key (some OECD/usage tiers), read it from the environment, never hard-code it (CONVENTIONS §5).

**License & note.** These are *open data* with attribution terms that vary by provider. **World Bank WDI** is released under **CC BY 4.0** — redistributable with attribution. **OECD**, **ECB**, **IMF**, and **BIS** publish under their own open-terms (generally free for non-commercial/research use with citation; some BIS series carry redistribution conditions) `[CHECK exact license per provider before redistributing]`. In practice for student research you may cache and share, but **cite the originating provider and the access/vintage date** — and where a provider re-publishes another's series, cite the original (the same discipline FRED forces, per CONVENTIONS §6).

**Gotchas.**
- **Country codes do not match across providers.** The number-one merge bug. `DEU`/`DE`/numeric IMF code all mean Germany; aggregates like "Euro area" or "World" sneak into country columns. Crosswalk explicitly; drop or label aggregates deliberately.
- **The same indicator is defined differently across sources.** "GDP" can be nominal vs. real, local currency vs. USD vs. PPP, SA vs. NSA. Two providers' "GDP growth" need not agree. Read the metadata, not just the column name.
- **Revisions and vintages.** Macro series are revised; today's value for 2020 is not what was published in 2021. For a real-time or forecasting design, you need the vintage, not the latest — the same look-ahead trap as FRED's ALFRED (Ch 7.2).
- **Coverage holes and breaks.** Poorer/smaller countries have gaps; definitional breaks (a euro changeover, a methodology revision, a country split) create discontinuities. A balanced-panel `dropna()` can silently bias your sample toward rich, well-measured countries.
- **SDMX keys are finicky.** The dimension order and codes in a series key are provider-specific and easy to get wrong; verify against the provider's data structure definition `[CHECK exact keys above]`.

**First 10 rows — schema sketch (illustrative; values invented, not real statistics).**

| iso3 | country | provider | indicator_code | indicator | freq | period | value | unit |
|---|---|---|---|---|---|---|---|---|
| USA | United States | WorldBank | NY.GDP.MKTP.CD | GDP, current US$ | A | 2022 | 2.54e13 | USD |
| DEU | Germany | WorldBank | NY.GDP.MKTP.CD | GDP, current US$ | A | 2022 | 4.08e12 | USD |
| JPN | Japan | WorldBank | NY.GDP.MKTP.CD | GDP, current US$ | A | 2022 | 4.23e12 | USD |
| USA | United States | IMF_IFS | FPOLM_PA | Policy rate | M | 2023-11 | 5.33 | percent |
| DEU | Germany | ECB | MRR_FR.LEV | ECB MRO rate | M | 2023-11 | 4.50 | percent |
| GBR | United Kingdom | BIS | CBPOL | Central bank policy rate | M | 2023-11 | 5.25 | percent |
| FRA | France | OECD | CPALTT01 | CPI, all items | M | 2023-11 | 4.0 | pct YoY |
| JPN | Japan | IMF_IFS | ENDA_XDC_USD | Exchange rate, JPY/USD | M | 2023-11 | 149.7 | JPY/USD |
| BRA | Brazil | WorldBank | FR.INR.LEND | Lending rate | A | 2022 | 39.6 | percent |
| IND | India | WorldBank | NY.GDP.MKTP.CD | GDP, current US$ | A | 2022 | 3.39e12 | USD |

(Note the same `iso3` join key spanning providers — and that the policy-rate definitions are *not* identical across IMF/ECB/BIS.)

**Which chapter/lab/capstone uses it.** These power any *cross-country* project. The methods are the panel and event-study tools from **Week 3–4** (fixed effects, DiD) and the inference discipline of **Week 5** (clustering — note these are country panels, so cluster thoughtfully, Ch 5.4 Petersen). A natural fit is a macro/monetary **capstone** in the spirit of **Capstone 5 (FRED Macro Event Study)** extended internationally — e.g., how do exchange rates or credit growth respond across countries to a policy shock — or any comparative finance question where one country is not enough. You acquire and document the series through the **Ch 7.2 / Lab 7** reproducible-pull discipline: build the country-code crosswalk, pin the vintage, cache the raw responses, and cite each originating provider. (For U.S.-only macro, prefer FRED; reach for these when the question crosses borders.)
