---
title: "Week 7 — Capstone build (Aug 3 – Aug 7, 2026)"
description: >-
  From research question to pre-analysis plan, data pull, cleaned
  dataset, and signed identification memo.
---

# Week 7 — Capstone build <span class="week-badge upcoming">upcoming</span>

**August 3 – August 7, 2026** · Chapters 7.1 – 7.5 · Lab 7 · Mentor Session 7 · Project deliverables

> Turn a hunch into a falsifiable, pre-registered empirical design with data in hand.

This is the week where the textbook stops being something you read and becomes something you use. By Friday at 5 pm your team has a registered pre-analysis plan, a cleaned analysis dataset that survives reproducibility checks, and a one-page identification memo that names the threats and the responses.

---

## Daily schedule

=== "Mon Aug 3"

    | Block | What |
    |---|---|
    | 9:00 – 12:00 | Read **Ch 7.1 — Idea-Generation Workshop** (so-what filter; cast → dataset map; feasibility/novelty rubric). Work `nb7.1`. |
    | 1:00 – 4:00 | Team kickoff — assign roles (PAP author, data lead, code lead, writing lead). |
    | 4:00 – 5:00 | Office hours |

=== "Tue Aug 4"

    | Block | What |
    |---|---|
    | 9:00 – 12:00 | Read **Ch 7.2 — Data Acquisition in Practice** (WRDS, EDGAR, FRED, HMDA, 13F, PatentsView). Work `nb7.2` (multi-source pull harness). |
    | 1:00 – 4:00 | **Lab 7 (Part A)** — your team's pull script runs end-to-end, with cache + audit log. |
    | 4:00 – 5:00 | Office hours |

=== "Wed Aug 5"

    | Block | What |
    |---|---|
    | 9:00 – 12:00 | Read **Ch 7.3 — Pre-Analysis Plan (Olken 2015 short form)**. Work `nb7.3` (power calc + BH-FDR + PAP emitter). |
    | 2:00 – 3:30 | **Mentor Session 7 — "Pre-registering before peeking"** |
    | 4:00 – 5:00 | Office hours |

=== "Thu Aug 6"

    | Block | What |
    |---|---|
    | 9:00 – 12:00 | Read **Ch 7.4 — Building the Analysis Dataset** (PERMNO/GVKEY/CIK crosswalks, survivorship/look-ahead, winsorizing). Work `nb7.4`. |
    | 1:00 – 4:00 | **Lab 7 (Part B)** — assemble the analysis dataset with `validate=` merges and the `merge_asof` look-ahead guard. |
    | 4:00 – 5:00 | Office hours |

=== "Fri Aug 7"

    | Block | What |
    |---|---|
    | 9:00 – 12:00 | Read **Ch 7.5 — The Identification Memo**. Write yours. |
    | 1:00 – 3:00 | **PAP file + identification memo** submitted; first-look regressions remain *frozen* until the PAP is in. |
    | 3:00 – 4:00 | Demo + Week-8 preview |
    | **5:00 pm** | **Deliverable cutoff** |

---

## What to read

- [Ch 7.1 — Idea-Generation Workshop](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/book/weeks/week-07/ch71-idea-generation-workshop.html)
- [Ch 7.2 — Data Acquisition in Practice](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/book/weeks/week-07/ch72-data-acquisition-in-practice.html)
- [Ch 7.3 — The Pre-Analysis Plan](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/book/weeks/week-07/ch73-pre-analysis-plan.html)
- [Ch 7.4 — Building the Analysis Dataset](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/book/weeks/week-07/ch74-building-the-analysis-dataset.html)
- [Ch 7.5 — The Identification Memo](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/book/weeks/week-07/ch75-identification-memo.html)

**Notebooks:** `notebooks/week-07/`.
**Mentor reading:** Mentor 7 — "Pre-registering before peeking".

---

## What to submit (due Fri Aug 7, 5:00 pm ET) — *team deliverables*

1. **Pull script + data card** in `projects/<team>/data/` ([PS 7.2](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/book/weeks/week-07/ps7.2.html) style).
2. **Pre-Analysis Plan** — registered, time-stamped, in `projects/<team>/pap.md`.
3. **Merged analysis dataset** — passes `pytest -q projects/<team>/tests/`.
4. **Identification memo + threats table** in `projects/<team>/identification-memo.md`.
5. **Per-student journal entry** — `journal/week-07.md`.
6. **Pull requests** — one per team member, against the team branch.

!!! warning "PAP discipline"
    Once your PAP is filed Friday at 5 pm, the primary specification is **frozen**. Anything that deviates in Week 8 must be reported in a deviations log in the final paper. This is not bureaucracy — it is the difference between a finding and a fishing expedition.

---

## Data we touch this week

Whatever your team's charter calls for. The most common combinations:

- [CRSP](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/crsp.html) + [Compustat](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/compustat.html) — corporate-finance and asset-pricing teams.
- [HMDA](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/hmda.html) + [FFIEC Call Reports](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/ffiec-call-reports.html) — fair-lending and bank-regulation teams.
- [USPTO PatentsView](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/uspto-patentsview.html) — innovation teams.
- [EDGAR 10-K/10-Q](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/edgar-10k-10q.html) + [Loughran–McDonald](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/loughran-mcdonald-dict.html) — text-as-data teams.
- [FRED](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/fred.html) — every team, for macro controls.

---

## Next week preview

[**Week 8 — Symposium →**](week-08.md). Specification curve, robustness battery, poster, defense — and Wednesday, August 12, at the GMU ASSIP Symposium.
