---
title: "Week 3 — Causal Inference I (Jul 6 – Jul 10, 2026)"
description: >-
  Potential outcomes, selection on observables, instrumental variables,
  and the weak-IV pathology.
---

# Week 3 — Causal Inference I <span class="week-badge upcoming">upcoming</span>

**July 6 – July 10, 2026** · Chapters 3.1 – 3.5 · Lab 3 · Mentor Session 3 · Problem Set 3

> Correlation is cheap; the Rubin causal model makes "effect" precise, and we earn causal claims through design, not control variables.

By Friday you should be able to read a fair-lending paper, identify the threat to identification in one sentence, and say whether matching, weighting, or IV is the right knife — and what fails when it isn't.

---

## Daily schedule

=== "Mon Jul 6"

    | Block | What |
    |---|---|
    | 9:00 – 12:00 | Read **Ch 3.1 — Potential Outcomes, SUTVA, and the Fundamental Problem**. Work `nb3.1` (potential outcomes & selection bias). |
    | 1:00 – 4:00 | Live problem-solving on $\mathbb{E}[Y_1 - Y_0]$ identification. |
    | 4:00 – 5:00 | Office hours |

=== "Tue Jul 7"

    | Block | What |
    |---|---|
    | 9:00 – 12:00 | Read **Ch 3.2 — Matching & Propensity Scores**. Work `nb3.2` (PSM with balance diagnostics). |
    | 1:00 – 4:00 | Read **Ch 3.3 — Entropy Balancing & Doubly-Robust**. Work `nb3.3`. |
    | 4:00 – 5:00 | Office hours |

=== "Wed Jul 8"

    | Block | What |
    |---|---|
    | 9:00 – 12:00 | Read **Ch 3.4 — Instrumental Variables** (relevance/exclusion, 2SLS-as-FWL, LATE). Work `nb3.4`. |
    | 2:00 – 3:30 | **Mentor Session 3 — "Earning a causal claim"** |
    | 4:00 – 5:00 | Office hours |

=== "Thu Jul 9"

    | Block | What |
    |---|---|
    | 9:00 – 12:00 | Read **Ch 3.5 — Reading IV in the Wild + Weak-IV Pathology**. Work `nb3.5` (conventional coverage 0.80 vs. Anderson–Rubin 0.97). |
    | 1:00 – 4:00 | **Lab 3 — PSM + 2SLS on HMDA** (fair-lending mortgage panel). |
    | 4:00 – 5:00 | Office hours |

=== "Fri Jul 10"

    | Block | What |
    |---|---|
    | 9:00 – 12:00 | Wrap PS 3.1 – 3.5. |
    | 1:00 – 3:00 | **Project-question shortlist** — each student submits 3 candidate research questions with feasibility/novelty scores. |
    | 3:00 – 4:00 | Friday demo + Week-4 preview |
    | **5:00 pm** | **Deliverable cutoff** |

---

## What to read

- [Ch 3.1 — Potential Outcomes & SUTVA](../../../book/weeks/week-03/ch31-potential-outcomes-sutva.md)
- [Ch 3.2 — Matching & Propensity Scores](../../../book/weeks/week-03/ch32-matching-propensity-scores.md)
- [Ch 3.3 — Entropy Balancing & Doubly-Robust](../../../book/weeks/week-03/ch33-entropy-balancing-doubly-robust.md)
- [Ch 3.4 — Instrumental Variables](../../../book/weeks/week-03/ch34-instrumental-variables.md)
- [Ch 3.5 — Reading IV in the Wild + Weak-IV Pathology](../../../book/weeks/week-03/ch35-reading-iv-weak-iv-pathology.md)

**Notebooks:** `notebooks/week-03/` — nb3.1 through nb3.5.
**Lab:** Lab 3 — PSM + 2SLS on HMDA.
**Mentor reading:** Mentor 3 — "Earning a causal claim".

---

## What to submit (due Fri Jul 10, 5:00 pm ET)

1. **Problem Set 3** — PS 3.1 through 3.5.
2. **Lab 3 notebook** with balance table, ATT estimate, first-stage F, and Anderson–Rubin CI.
3. **Project-question shortlist** — three questions in `projects/<your-name>-shortlist.md`, scored on feasibility and novelty.
4. **Journal entry** — `journal/week-03.md`.
5. **Pull request** — `week-03 — <your name>`.

---

## Data we touch this week

- [HMDA (Home Mortgage Disclosure Act)](../../../data-cards/hmda.md) — fair-lending panel for Lab 3.
- [CRSP](../../../data-cards/crsp.md) and [Compustat](../../../data-cards/compustat.md) — for the PSM example.

---

## Next week preview

[**Week 4 — Causal Inference II →**](week-04.md). Difference-in-differences (including the staggered-adoption crisis), regression discontinuity, synthetic control, and shift-share designs.
