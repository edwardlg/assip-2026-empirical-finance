---
title: "Week 4 — Causal Inference II (Jul 13 – Jul 17, 2026)"
description: >-
  Difference-in-differences (including the staggered-adoption crisis),
  regression discontinuity, synthetic control, and shift-share.
---

# Week 4 — Causal Inference II <span class="week-badge upcoming">upcoming</span>

**July 13 – July 17, 2026** · Chapters 4.1 – 4.5 · Lab 4 · Mentor Session 4 · Problem Set 4

> The modern panel/quasi-experimental toolkit — and the recent literature showing the "obvious" estimators are often wrong.

You will see, with your own simulation, a two-way fixed-effects DiD estimator return **+0.40** when the true effect is **−2.57** — and then you will fix it with Callaway–Sant'Anna. This is the single most important methodological week of the program.

---

## Daily schedule

=== "Mon Jul 13"

    | Block | What |
    |---|---|
    | 9:00 – 12:00 | Read **Ch 4.1 — Difference-in-Differences & Event Studies** (parallel trends, leads/lags). Work `nb4.1`. |
    | 1:00 – 4:00 | Live whiteboard on parallel-trends testing. |
    | 4:00 – 5:00 | Office hours |

=== "Tue Jul 14"

    | Block | What |
    |---|---|
    | 9:00 – 12:00 | Read **Ch 4.2 — The Staggered-Adoption Crisis** (Goodman-Bacon, negative weights, CS, Sun–Abraham, BJS). Work `nb4.2`. |
    | 1:00 – 4:00 | **Lab 4 — Staggered-DiD bake-off**: same data, four estimators, compare. |
    | 4:00 – 5:00 | Office hours |

=== "Wed Jul 15"

    | Block | What |
    |---|---|
    | 9:00 – 12:00 | Read **Ch 4.3 — Regression Discontinuity** (sharp/fuzzy, CCT bandwidth, McCrary). Work `nb4.3`. |
    | 2:00 – 3:30 | **Mentor Session 4 — "Reading staggered-DiD papers in 2026"** |
    | 4:00 – 5:00 | Office hours |

=== "Thu Jul 16"

    | Block | What |
    |---|---|
    | 9:00 – 12:00 | Read **Ch 4.4 — Synthetic Control & Synthetic DiD**. Work `nb4.4` (Abadie + Arkhangelsky). |
    | 1:00 – 4:00 | Read **Ch 4.5 — Bartik / Shift-Share Designs**. Work `nb4.5` (Rotemberg weights reassemble the 2SLS estimate). |
    | 4:00 – 5:00 | Office hours |

=== "Fri Jul 17"

    | Block | What |
    |---|---|
    | 9:00 – 12:00 | Wrap PS 4.1 – 4.5. |
    | 1:00 – 3:00 | **Capstone team formation** — final 3 teams of 4–5 students each declared. |
    | 3:00 – 4:00 | Demo + Week-5 preview |
    | **5:00 pm** | **Deliverable cutoff** |

---

## What to read

- [Ch 4.1 — DiD & Event Studies](../../../book/weeks/week-04/ch41-did-event-studies.md)
- [Ch 4.2 — The Staggered-Adoption Crisis](../../../book/weeks/week-04/ch42-staggered-adoption-crisis.md)
- [Ch 4.3 — Regression Discontinuity](../../../book/weeks/week-04/ch43-regression-discontinuity.md)
- [Ch 4.4 — Synthetic Control & Synthetic DiD](../../../book/weeks/week-04/ch44-synthetic-control.md)
- [Ch 4.5 — Bartik / Shift-Share](../../../book/weeks/week-04/ch45-bartik-shift-share.md)

**Notebooks:** `notebooks/week-04/`.
**Lab:** Lab 4 — Staggered-DiD bake-off.
**Mentor reading:** Mentor 4 — "Reading staggered-DiD papers".

---

## What to submit (due Fri Jul 17, 5:00 pm ET)

1. **Problem Set 4** — PS 4.1 through 4.5.
2. **Lab 4 notebook** comparing TWFE, CS, Sun–Abraham, BJS on the same staggered panel.
3. **Capstone team declaration** — your team's name + your slot in the team in `cohort/teams.md`.
4. **Journal entry** — `journal/week-04.md`.
5. **Pull request** — `week-04 — <your name>`.

---

## Data we touch this week

- [CRSP](../../../data-cards/crsp.md) + [Compustat](../../../data-cards/compustat.md) — policy-shock event studies.
- [USPTO PatentsView](../../../data-cards/uspto-patentsview.md) — for the Bartik example.
- [USA Spending](../../../data-cards/usaspending.md) — for shift-share exposure construction.

---

## Next week preview

[**Week 5 — Reading the Frontier I →**](week-05.md). One classic paper per day — Fama & French 1992/1993, Jegadeesh & Titman 1993, Petersen 2009, Bertrand–Duflo–Mullainathan 2004.
