# Data Card — HMDA (Home Mortgage Disclosure Act Loan Application Register)

## Provider & what it is

The **HMDA Loan Application Register (LAR)** is the public, near-census record of mortgage applications in the United States. Under the Home Mortgage Disclosure Act, most lenders must report **nearly every mortgage application they receive** — not just loans made, but ones denied, withdrawn, or fallen through. Per application you get the **action taken** (originated, approved-not-accepted, denied, withdrawn, closed-for-incompleteness), the **loan amount**, the **property location** (state, county, census tract), and **applicant demographics** (race, ethnicity, sex, income). Since 2018 you also get a richer file: interest rate, points, debt-to-income, loan-to-value, property value, and more.

The provider is the **CFPB** (Consumer Financial Protection Bureau), which runs the modern public **HMDA Data Browser**, with the **FFIEC** (Federal Financial Institutions Examination Council) publishing the per-year bulk files. It is one of the **largest public microdatasets in U.S. finance** — tens of millions of records per year.

The reveal is also the limitation the whole fair-lending literature turns on: **HMDA records who applied, where, for how much, and what happened — but not the applicant's credit score.** It can show you *that* denial rates differ by race; it cannot tell you whether that gap is discrimination or unseen differences in creditworthiness. That single missing column is why fair-lending work leans on *design*, not more controls (Ch 6.4; Gao & Sun, 2019).

## Coverage

- **Years:** modern Data Browser coverage from **2007** forward, with the **2018 schema expansion** (Dodd-Frank/Regulation C) as a hard break: pre-2018 and post-2018 files have different fields and codings. The new fields (rate, DTI, LTV, property value, NMLS id) start in 2018.
- **Universe:** depository and non-depository lenders above a reporting threshold; smaller lenders are exempt, so HMDA is *near*-census, not total. The threshold has changed across years — `[CHECK]` the exact loan-count threshold for your pinned vintage, because it affects which small lenders appear.
- **Size:** multiple gigabytes per nationwide year. **Never download the full national LAR to a laptop.**
- **Revisions:** a year is published, then re-published with corrections. The vintage matters; pin it.

## Key identifiers

- **Geography:** the county is the **5-digit FIPS** code; the tract is the **11-digit census-tract** code; plus the two-letter **state**. These are your panel keys for aggregating to county-year or tract-year.
- **Lender:** the institution is identified by **LEI** (Legal Entity Identifier) in the modern file, replacing the older **respondent ID + agency code** pair used pre-2018.
- **Action taken:** the coded outcome (1 = originated, 2 = approved-not-accepted, 3 = denied, 4 = withdrawn, 5 = closed-incomplete, …). The denial-rate outcome is built from these codes.
- There is **no person identifier** — HMDA is application-level, not borrower-panel; you cannot follow an individual across applications.

## Access path

Two disciplined routes, both **free, no key**:

1. **CFPB Data Browser API** — best for a handful of states/years. The **aggregation endpoint** lets the server count actions by your chosen dimensions so you never move the microdata: base `https://ffiec.cfpb.gov/v2/data-browser-api/`. There is also a filtered-records endpoint for pulling raw rows when you must.
2. **FFIEC bulk files** — best for the whole country. Per-year pipe-delimited LAR files; download once to the **camp container's read-only data area** and aggregate in chunks with `pyarrow`/`pandas`. The container mirrors these so you are not re-downloading gigabytes.

```python
import requests, pandas as pd
# CFPB HMDA Data Browser AGGREGATION endpoint (public, no key).
# Ask the server to count actions by state, so the multi-GB microdata never moves.
HMDA_AGG = "https://ffiec.cfpb.gov/v2/data-browser-api/view/aggregations"
def fetch_hmda(states, year):
    params = {"years": year, "states": ",".join(states),
              "actions_taken": "1,3"}          # 1 = originated, 3 = denied
    r = requests.get(HMDA_AGG, params=params, timeout=60); r.raise_for_status()
    df = pd.json_normalize(r.json()["aggregations"]); df["year"] = year
    return df
# raw = fetch_hmda(["VA","MD","NC"], 2021)   # run on the container, pinned vintage
```

**Aggregate server-side whenever you can.** CFPB pre-counts by state × action (and finer geographies), so pull *counts*, not microdata, and build the denial-rate panel from those. `[CHECK]` exact parameter names against the live API docs for your pinned vintage — CFPB has renamed fields across releases, so the snippet is the *pattern*, not a stable contract.

## License & note

**Free and public.** HMDA LAR is published by the FFIEC/CFPB as public data; cite the CFPB HMDA Data Browser (and the FFIEC bulk file if used) plus your pinned vintage and access date. No key, no redistribution restriction. The non-negotiable obligation: **name the vintage**, because the API serves whatever snapshot CFPB currently hosts and the same query returns different numbers across re-publications. Per CONVENTIONS §5, the gigabyte-scale bulk files stay on GMU infrastructure; you aggregate *down* first.

## Gotchas

- **No credit score.** The single most important caveat. A raw denial-rate or pricing gap by race confounds discrimination with unobserved creditworthiness (Week 2 OVB). This is *why* Gao & Sun (2019) reached for a clean design, and why Bartlett et al. and BHR are notable for getting at the score from outside HMDA (Ch 6.4).
- **The 2018 schema break.** Pre- and post-2018 files differ in fields and codings. Do not splice a pre-2018 series to a post-2018 series without reconciling the schema — the "new" rate/DTI/LTV fields simply do not exist before 2018.
- **It's enormous.** Never pull the national file to a laptop; aggregate server-side or in chunks on the container.
- **Thin cells are noise.** A rural county with 40 applications has a wildly swinging denial rate. Filter out cells below a minimum decided-application count (e.g., 100) so sampling noise in tiny geographies does not dominate the panel.
- **The denominator is a choice you must state.** "Denied / (originated + denied)" excludes withdrawn and incomplete applications — defensible, but a referee will ask. Write it into the spec (CONVENTIONS §4).
- **Vintage drift.** Quote no figure without naming the snapshot it came from. `[CHECK]` the exact snapshot date on the camp container before citing a number.

## First 10 rows (illustrative schema sketch — not real values)

*Aggregation response (CFPB Data Browser), shape only — counts, not microdata:*

| state | actions_taken | count | year |
|---|---|---|---|
| VA | 1 | 412903 | 2021 |
| VA | 3 | 51277 | 2021 |
| MD | 1 | 298140 | 2021 |
| MD | 3 | 44011 | 2021 |
| … | … | … | … |

*Raw LAR record (post-2018 filtered pull), shape only — one row per application:*

| activity_year | lei | state_code | county_code | census_tract | action_taken | loan_amount | derived_race | applicant_income | interest_rate |
|---|---|---|---|---|---|---|---|---|---|
| 2021 | EXAMPLELEI000000000 | VA | 51059 | 51059482101 | 3 | 325000 | Black or African American | 78 | NA |
| 2021 | EXAMPLELEI000000000 | VA | 51059 | 51059482102 | 1 | 410000 | White | 142 | 3.125 |
| … | … | … | … | … | … | … | … | … | … |

*Derived county-year denial-rate panel (what you actually regress on), shape only:*

| county | year | denied | apps_decided | denial_rate |
|---|---|---|---|---|
| 51059 | 2021 | 1842 | 19204 | 9.59 |
| 51013 | 2021 | 1130 | 14072 | 8.03 |
| … | … | … | … | … |

## Which chapter / lab / capstone uses it

- **Week 4, Lab 4 — Clean DiD on HMDA + a state policy shock.** The lab's Path A builds exactly the county-year denial-rate panel above from the Data Browser API, then runs TWFE → event study → Callaway–Sant'Anna against clean controls. The card's aggregation pattern *is* the lab's recipe.
- **Week 6, Ch 6.4 — fair lending in the algorithmic era** (Bartlett, Morse, Stanton & Wallace; Bhutta, Hizmo & Ringo). HMDA is the spine of both papers, and the chapter's whole pivot is what HMDA *cannot* see (the credit score) and how those authors get it from outside HMDA.
- **Capstone 1 — Fair Lending on HMDA.** The terminal use: a real disparity-plus-clean-design paper. The student pins a vintage, builds the panel on GMU infrastructure, and defends a parallel-trends or matched-design identifying assumption.
- **Gao & Sun (2019, *PNAS*)** is the anchor paper across this thread (Mentor Session 4, Lab 4, Capstone 1): same-sex-borrower lending studied with a *design* precisely because HMDA-family data lacks the score.
