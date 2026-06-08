# Data Card — NBER / KPSS Patent–Compustat Links

**Source slug:** `nber-patent-link` · Appendix C (Data Dictionary) · last touched 2026-05-28

## Provider & what it is

This card covers the two *crosswalk* files that turn raw patents into firm-level finance variables — the bridge PatentsView deliberately does not build. There are two distinct public goods here, and students must not confuse them.

1. **The patent-to-firm crosswalk** (the NBER Patent Data Project lineage — Hall, Jaffe & Trajtenberg's original assignee→firm match, and its modern successors). This is a mapping table: each patent's `assignee_id` (or assignee name) ↔ a firm identifier (Compustat `gvkey` / CRSP `permno`). Without it, a patent is owned by "NVIDIA Corporation" the *string*; with it, the patent is owned by `permno 86580` the *tradable firm*, and you can finally run a finance regression.

2. **The KPSS patent-value file** — the *public* dataset released alongside Kogan, Papanikolaou, Seru & Stoffman (2017), giving each patent a **market-based dollar value** estimated from the stock-price reaction to the patent's grant announcement, plus a citation-based value and the firm link. This is the file behind the "innovation as a dollar number" measure the camp builds in Week 6.

The reveal-the-trick point: the *value* in the KPSS file is not measured, it is *estimated from a market reaction inside a short event window*, and the *link* in any crosswalk is a *match*, not a fact — both carry error you inherit silently if you treat the file as ground truth.

## Coverage

The crosswalk and the KPSS file cover **granted U.S. patents matched to publicly listed (CRSP/Compustat) firms**, roughly **1926/1950s–present** for the value series (the KPSS announcement-based measure needs daily returns, so it begins when CRSP daily data begin; the citation-based measure reaches further back) [CHECK exact start year of the public KPSS file and its most recent update vintage]. Only *public* firms with a CRSP `permno` are in scope — private firms, foreign assignees, and individual inventors are absent by construction, which is itself a sample-selection fact to disclose.

## Key identifiers

`patent_num` / `patent_id` (links to PatentsView), `permno` (CRSP) and/or `gvkey` (Compustat) on the firm side, plus the KPSS value columns — typically a nominal dollar value (`xi` / `xi_nominal`), a real (CPI-deflated) value, and a citation-based value `cites` [CHECK exact column names in the current public release]. The join chain is: **PatentsView patent ⟶ (crosswalk) ⟶ permno/gvkey ⟶ (CRSP/Compustat, GMU-licensed) ⟶ firm outcomes.** Note the asymmetry of reproducibility: the crosswalk and KPSS value file are *public and shippable*, but the CRSP/Compustat tables at the end of the chain are *licensed* and must stay on GMU infrastructure (CONVENTIONS §5).

## Access path (bulk download; no key)

These are **bulk flat-file downloads, not APIs**, and they require **no key**.

- The KPSS patent-value data are posted publicly (the authors' / Kelley School data page) as a download — typically CSV/DTA, one row per patent with the value columns and `permno`.
- The NBER-lineage crosswalk ships as a downloadable mapping table (CSV).

```python
import pandas as pd
# Files are downloaded once into data/raw/ and pinned by snapshot date.
kpss = pd.read_csv("data/raw/kpss_2017_public.csv",
                   dtype={"patent_num": "string", "permno": "Int64"})
xwalk = pd.read_csv("data/raw/patent_permno_xwalk.csv",
                    dtype={"patent_num": "string", "permno": "Int64"})
# Aggregate patent-level value to a firm-year panel:
panel = (kpss.merge(xwalk, on=["patent_num", "permno"], how="left")
              .groupby(["permno", "issue_year"])["xi_real"].sum()
              .rename("patent_value").reset_index())
```

No env secret is needed for the public files; the licensed CRSP/Compustat join at the end uses `${WRDS_USERNAME}` via a pinned WRDS pull on GMU infra.

## License (FREE / public) & note

The **KPSS public file** and the **NBER-lineage crosswalk** are released **free for research use** (academic/non-commercial; attribute the source papers) — they are *public* and may be redistributed inside a replication packet's `data/raw/` [CHECK the exact license/terms wording on the current KPSS download page]. The downstream **CRSP/Compustat** data are emphatically **not** public and must never be committed; a packet reconstructs them with a pinned WRDS script (the public-vs-licensed asymmetry from Appendix D.4). Cite KPSS (2017, *QJE*) for the value file and Hall–Jaffe–Trajtenberg / the NBER Patent Data Project for the crosswalk lineage.

## Gotchas

- **The link is a match, not a fact.** The crosswalk resolves messy assignee names to firms with error — missed matches (a patent whose firm exists but isn't linked) and false matches (a patent assigned to the wrong subsidiary/parent). Coverage is also better for large, long-lived firms, so a "patents per firm" panel is non-randomly incomplete.
- **Vintage and assignee-id drift.** PatentsView's `assignee_id` changes across releases (see the `uspto-patentsview` card), so a crosswalk built against one PatentsView vintage may not key cleanly to another. Pin both vintages together.
- **The value is an *estimate from a window*.** KPSS value = (stock reaction in a short window around grant) × adjustments. Any other firm news in that window contaminates it (the same confound Ch 6.1 dissects). It is an unbiased estimate of value *on average*, not the true value of any single patent — never read a single patent's dollar figure as fact.
- **Nominal vs. real, and grant-year dating.** Use the CPI-deflated column for cross-year comparisons, and aggregate to firm-year by **issue/grant year** (consistent with the event measured) — but remember grant-year dating imports the grant-lag truncation from the patent card.
- **`permno` vs `gvkey` and merge keys as strings.** CRSP uses `permno`, Compustat uses `gvkey`; the file may carry one and not the other, requiring the CRSP/Compustat link table. As everywhere in this appendix, read id columns as strings/`Int64`, not floats, or merges silently drop.
- **Selection on listing.** Only public firms are present; a firm that IPOs mid-sample appears only after listing, and de-listed firms vanish — survivorship and entry both bias firm-year innovation trends.

## "First 10 rows" — schema sketch (ILLUSTRATIVE, not real values)

KPSS public patent-value file, one row per patent:

| patent_num | permno | issue_year | filing_year | xi_nominal | xi_real | cites |
|------------|-------:|-----------:|------------:|-----------:|--------:|------:|
| 6000001 | 10107 | 2000 | 1997 | 18.4 | 28.1 | 12 |
| 6000002 | 14593 | 2000 | 1996 | 540.9 | 826.0 | 47 |
| 6000003 | 87445 | 2000 | 1998 | 3.2 | 4.9 | 2 |
| 6000004 | 10107 | 2001 | 1998 | 65.7 | 98.3 | 9 |
| 6000005 | (no match) | 2001 | 1999 | . | . | 5 |

Patent→firm crosswalk, one row per (patent × firm match):

| patent_num | assignee_id | permno | gvkey | match_score |
|------------|-------------|-------:|------:|------------:|
| 6000001 | a3f9... | 10107 | 012141 | 0.98 |
| 6000002 | b1c4... | 14593 | 005047 | 0.95 |
| 6000005 | c8d2... | (no match) | (no match) | 0.41 |

(Illustrative only; do not cite. `xi_real` in millions of CPI-deflated dollars; row 5 shows an unmatched patent — exactly the non-random hole the gotchas warn about.)

## Which chapter / lab / capstone uses it

- **Capstone 3 — Innovation from USPTO PatentsView** — the central enabling files: the crosswalk turns PatentsView patents into a firm-year panel and the KPSS value file supplies the dollar innovation measure, so the capstone's firm-outcome event study (ties to KPSS 2017) is literally built on this card. The selection, vintage, and value-is-an-estimate gotchas are the threats the capstone must name (CONVENTIONS §4).
- **Week 6, Ch 6.1 (Reader's Guide — KPSS 2017)** — Ch 6.1 reads this exact public dataset as research infrastructure; this card is the operational companion to that reading, and the "value is a windowed estimate" caveat is the chapter's "what's vulnerable."
- **Leah's running thread (patents, innovation)** — the firm-linked patent panel is Leah's workbench across Week 6.
- **Appendix D.4 (Replication Packet Standard)** — the public-crosswalk-shippable / licensed-CRSP-not-shippable split is the textbook illustration of D.4's public-vs-licensed asymmetry of reproducibility.
