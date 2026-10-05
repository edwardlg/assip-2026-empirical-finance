# Data Card — CFPB Consumer Complaint Database

## Provider & what it is

The **Consumer Financial Protection Bureau (CFPB)** publishes the **Consumer Complaint Database**: a public record of complaints that consumers have filed against financial companies — credit cards, mortgages, student loans, debt collection, credit reporting, bank accounts, "buy now pay later," and more. When a person complains to the CFPB about a financial product, the complaint is routed to the company for a response; the CFPB then publishes a de-identified version of the record, including the **product** and **sub-product**, the **issue** the consumer raised, the **company** named, the consumer's **state/ZIP prefix**, the **company's response**, and — when the consumer opts in — a **free-text narrative** describing what happened.

The reveal here is twofold. First, it is a rare public dataset where the *outcome variable is text*: the narrative field is a natural training and evaluation set for the text-as-data and LLM-labeling work of Week 6, because a human can read a complaint and a model can try to classify it. Second, it is **complaints, not incidence** — it measures who *complained*, which is a selected, voluntary signal, not the true rate of financial harm. Treating complaint counts as if they were harm rates is the trap the whole card exists to warn against.

## Coverage

- **Time:** complaints from **December 2011** to present, updated roughly daily as new complaints clear the publication process. `[CHECK]` exact update cadence for your pinned vintage.
- **Size:** millions of complaints cumulatively; hundreds of thousands per recent year. Large but laptop-tractable when filtered by product/date — not a multi-GB-per-year file like HMDA.
- **Narratives:** only a *subset* of complaints include a published free-text narrative — the consumer must opt in to publication, and the CFPB scrubs personal identifiers. So the text-analysis sample is a selected slice of the already-selected complaint population. `[CHECK]` current share of complaints with published narratives.
- **Products:** the product taxonomy has changed over time (categories added, renamed, split — e.g., the credit-reporting and BNPL categories evolved), so a long time series needs the taxonomy reconciled.

## Key identifiers

- **Complaint ID** — a unique integer per complaint, the primary key.
- **Company** — the named financial company (a string; the same firm can appear under spelling/affiliate variants, so company-level aggregation needs cleaning).
- **Product / Sub-product / Issue / Sub-issue** — the categorical labels, the natural grouping dimensions.
- **State** and **ZIP code** (3-digit prefix only, for privacy) — coarse geography.
- **Date received** and **Date sent to company** — timing fields.
- There is **no person identifier** and no household linkage; narratives are de-identified.

## Access path

- **Public API**, base `https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/`. JSON, **no key required**, supports filtering by date range, product, company, state, and a full-text search over narratives, with paging.
- **Bulk download** of the full CSV/JSON is also offered from the same data-research page — fine to pull filtered, but pin the download date.

```python
import requests, pandas as pd
BASE = "https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/"
# Student-loan complaints in 2024 that include a published narrative (public, no key):
params = {"product": "Student loan", "date_received_min": "2024-01-01",
          "date_received_max": "2024-12-31", "has_narrative": "true",
          "size": 100, "no_aggs": "true"}
r = requests.get(BASE, params=params, timeout=60); r.raise_for_status()
hits = r.json()["hits"]["hits"]           # each record under _source
df = pd.json_normalize([h["_source"] for h in hits])
```

`[CHECK]` exact parameter names (`date_received_min`, `has_narrative`, `size`) against the live API docs for your pinned vintage — the endpoint is Elasticsearch-backed and its parameter surface has shifted across releases. No secrets; the API is fully open.

## License & note

**Free and public**, published as U.S. government open data. Cite the CFPB Consumer Complaint Database and your pinned download/access date. The CFPB's own published caveat is the important one to repeat to students: the Bureau **does not verify** all the facts a consumer alleges, and publication is not a finding that a company did anything wrong. A complaint is an *allegation*, routed and answered, not an adjudicated fact. Quote complaint patterns as "what consumers reported," never as proven misconduct.

## Gotchas

- **Complaints measure complaining, not harm.** Counts reflect who knew to file, had time to file, and chose to — a large, salient firm with many customers will rack up complaints without being worse per-customer. Normalize by something (accounts, deposits, loans) before comparing companies, and even then be careful.
- **Allegations, not verified facts.** The CFPB does not confirm the underlying claims. Do not present complaint volume as evidence of wrongdoing.
- **Narrative selection on selection.** Published narratives require consumer opt-in *and* CFPB scrubbing, on top of the already-voluntary act of complaining. Any text model trained on narratives generalizes only to *complaints with published narratives*, not to consumers at large — a textbook external-validity caveat.
- **Company-name messiness.** The same firm appears under affiliates and spelling variants; firm-level analysis needs a cleaning/crosswalk step.
- **Taxonomy drift.** Product/issue categories were added and renamed over time; reconcile the taxonomy before building a long panel.
- **Coarse geography.** Only state and 3-digit ZIP prefix — fine for state-level work, useless for tract-level fair-lending geography (use HMDA for that).

## First 10 rows (illustrative schema sketch — not real values)

*Complaint records (API `_source` fields), shape only — one row per complaint:*

| complaint_id | date_received | product | sub_product | issue | company | state | zip_code | company_response | has_narrative |
|---|---|---|---|---|---|---|---|---|---|
| 8000001 | 2024-03-14 | Student loan | Federal student loan servicing | Dealing with your lender or servicer | Example Servicing LLC | VA | 220xx | Closed with explanation | true |
| 8000002 | 2024-03-14 | Credit card | General-purpose credit card | Problem with a purchase shown on your statement | Sample Bank, N.A. | TX | 750xx | Closed with monetary relief | false |
| 8000003 | 2024-03-15 | Credit reporting | Credit reporting | Incorrect information on your report | Example Credit Bureau | CA | 941xx | In progress | true |
| … | … | … | … | … | … | … | … | … | … |

*Narrative text field (only when `has_narrative = true`), shape only:*

| complaint_id | consumer_complaint_narrative |
|---|---|
| 8000001 | "I have called my servicer XXXX times about an income-driven repayment recalculation and …" |
| 8000003 | "There is an account on my report that is not mine. I disputed it on XX/XX/XXXX and …" |
| … | … |

## Which chapter / lab / capstone uses it

- **Week 6 text-as-data and AI modules.** The narrative field is a natural corpus for LLM-labeling and text-classification exercises: a model proposes a label (the issue, the sentiment, whether a monetary remedy is implied), and you evaluate it against the CFPB's own categorical labels with the precision/recall harness from the Reading Guide Pack 6 / AI Lab Manual. The selection caveats make it an honest teaching case for *responsible-use and external-validity disclosure*.
- **Maya's student-debt and consumer-finance thread.** Complaints about student-loan servicing and credit reporting are directly relevant to the household-finance examples that run through the camp, and pair with HMDA (`hmda.md`) as the two CFPB-published consumer-finance sources — one application-level and near-census, one complaint-level and voluntary.
- A self-directed **capstone extension** source for a student who wants a text-heavy project outside the five canonical capstone datasets, with the standing warning that complaint counts are a selected signal, not a harm rate.
