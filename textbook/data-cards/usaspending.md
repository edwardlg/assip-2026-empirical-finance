# Data Card — USAspending.gov (Federal Awards)

**Source slug:** `usaspending` · Appendix C (Data Dictionary) · last touched 2026-05-28

## Provider & what it is

USAspending.gov is the U.S. Treasury's official public record of how the federal government spends money. Mandated by the DATA Act, it consolidates every reportable **federal award** — prime contracts, grants, loans, direct payments, and the sub-awards beneath them — into one searchable, downloadable system. For a finance student it is the cleanest free window into the *government as a customer*: which firms win federal contracts, how much, for what, where, and from which agency. The reveal-the-trick point is that USAspending is an *administrative aggregation* of what hundreds of agencies report about themselves, so its completeness and accuracy inherit every agency's reporting quality; it is a record of *reported* spending, not audited truth, and the recipient identity is exactly where the joins get hard.

## Coverage

Contract and assistance transactions from **fiscal year 2008** onward (the modern, reliable window; some series claim earlier coverage with degrading quality). Updated continuously as agencies report (with reporting lags of weeks to months). Scope is the entire federal government — all agencies, all award types — with awards tagged to recipient location and place-of-performance down to the congressional-district and county level (FIPS), so it can be merged geographically to Census/BEA.

## Key identifiers

The recipient identity is the crux. The legacy key was the **DUNS number** (a 9-digit Dun & Bradstreet id). On **April 4, 2022** the government replaced DUNS with the **UEI (Unique Entity Identifier)** — a 12-character alphanumeric code issued and managed in **SAM.gov**. Current data carry `recipient_uei` (and `recipient_parent_uei` for the corporate parent); older records carry `recipient_duns`. Both may appear during the transition window. Awards also key on a **`generated_unique_award_id`** / `award_id` (the stable award key), the awarding/funding **agency** and sub-agency codes, **NAICS** and **PSC** (Product/Service Code) for what was bought, and **CFDA / Assistance Listing** numbers for grants. The hard join — UEI/DUNS → a public-firm `gvkey`/`permno` — is *not* provided; a private contractor often has no stock-market identifier at all.

## Access path (free API)

The USAspending API lives at `https://api.usaspending.gov/api/v2/`. It is **free and requires no API key** — a refreshing exception in this appendix. Most useful endpoints are POSTs with a JSON `filters` body; bulk extracts come from the **download** endpoints or the bulk-download page.

```python
import requests  # no key needed
url = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
body = {
    "filters": {
        "time_period": [{"start_date": "2023-10-01", "end_date": "2024-09-30"}],
        "award_type_codes": ["A", "B", "C", "D"],  # contract types
        "recipient_search_text": ["Lockheed Martin"],
    },
    "fields": ["Award ID", "Recipient Name", "Award Amount",
               "recipient_uei", "Awarding Agency", "NAICS Code"],
    "page": 1, "limit": 100,
}
r = requests.post(url, json=body, timeout=60).json()
# r["results"] is the page of award records
```

No first-party Python SDK is relied on; `requests` + pagination is standard. For panel-scale work prefer the bulk award downloads over deep API pagination.

## License (FREE / public) & note

USAspending data are **U.S. Government works in the public domain** — free to use, redistribute, and republish with attribution; no key, no row-level license, no GMU-only constraint, so they belong in a packet's `data/raw/`. Cite as "USAspending.gov, prime award transactions, FY2024, retrieved [date]." The API asks only for reasonable use; cache and pin a snapshot date because the underlying data are continuously revised.

## Gotchas

- **DUNS → UEI transition.** Records straddling April 2022 mix the two ids; a panel joined only on DUNS silently drops post-transition recipients, and a panel joined only on UEI drops pre-transition ones. Build a DUNS↔UEI crosswalk (SAM.gov publishes the mapping) before keying a time series on recipient.
- **Recipient name is messy free text.** "Lockheed Martin Corp.", "LOCKHEED MARTIN CORPORATION", and a dozen subsidiaries are different strings; the *parent* rollup (`recipient_parent_uei`) helps but is incomplete. This is the same disambiguation problem as patents — counting "awards to Firm X" requires entity resolution you must do yourself, and naive name-matching over- or under-counts non-randomly.
- **Prime vs. sub-award double-counting.** A prime contract and its sub-awards both appear; summing across both inflates totals. Decide which level you are studying and filter `award_type_codes` accordingly.
- **Obligation vs. outlay vs. award ceiling.** "Award amount" can mean the obligated amount, the potential ceiling, or actual outlays — three very different numbers. Pick the field that matches your question and label it.
- **Reporting lag and revisions.** Recent fiscal years are incomplete and get backfilled; an event study on contract-award dates must respect that the record at the time differs from the record today (a vintage / look-ahead concern).
- **No firm-market link.** Most recipients are private; only a minority map to a CRSP/Compustat firm, so a firm-outcome design on contracts has heavy, non-random sample selection.

## "First 10 rows" — schema sketch (ILLUSTRATIVE, not real values)

`spending_by_award` (contracts), one row per prime award:

| Award ID | Recipient Name | recipient_uei | recipient_parent_uei | Award Amount | Awarding Agency | NAICS Code | pop_state | period_of_performance_start |
|----------|----------------|---------------|----------------------|-------------:|-----------------|------------|-----------|------------------------------|
| CONT_AWD_001 | LOCKHEED MARTIN CORP | ABC12DEF34GH | ABC12DEF34GH | 412000000 | Dept of Defense | 336411 | TX | 2023-10-15 |
| CONT_AWD_002 | LEIDOS INC | XYZ98UVW76RS | XYZ98UVW76RS | 88000000 | Dept of Defense | 541512 | VA | 2023-11-02 |
| CONT_AWD_003 | SMALL TECH LLC | QWE45RTY67UI | (blank) | 1250000 | Dept of Energy | 541715 | CA | 2024-01-20 |
| ASST_AWD_004 | STATE UNIVERSITY | LMN23OPQ45ST | LMN23OPQ45ST | 4500000 | NIH (grant) | (CFDA 93.847) | MD | 2024-02-01 |
| CONT_AWD_005 | (legacy record) | (blank) | (blank) | 670000 | GSA | 561720 | DC | 2021-08-11 |

(Illustrative only; do not cite. Row 5 shows a pre-transition record with `recipient_duns` populated but `recipient_uei` blank; row 3 shows a missing parent rollup.)

## Which chapter / lab / capstone uses it

- **Week 4, Ch 4.5 (Shift-Share) and policy-shock designs** — geographic federal-spending shocks (awards by county/agency) are a natural local-shock variable, joinable to Census/BEA on FIPS; the recipient-disambiguation and prime-vs-sub gotchas are live reproducibility traps.
- **Capstone 3 — Innovation from USPTO PatentsView** — federal R&D contracts/grants to a firm are a plausible input to (or instrument for) innovation, letting a student connect government funding to the patent-based innovation measure — but only after confronting the no-firm-market-link selection problem.
- **Capstone 1 — Fair Lending / public-data thread** and the broader **public-source toolkit** — USAspending is the worked example of a *key-free* free API, useful for contrast against the keyed Census/BLS/BEA/PatentsView pulls.
- **Week 7, Ch 7.2 (Data Acquisition in Practice)** — USAspending appears as a free, no-key API in the reproducible-pull discussion.
