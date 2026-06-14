---
title: "Week 2 — The OLS Engine (Jun 29 – Jul 2, 2026)"
description: >-
  OLS in matrix form, the Gauss–Markov theorem, the Frisch–Waugh–Lovell
  partialling-out trick, and the three ways the textbook story breaks.
---

# Week 2 — The OLS Engine <span class="week-badge upcoming">upcoming</span>

**June 29 – July 2, 2026** (4-day week — Fri Jul 3 is the Independence Day observance)
Chapters 2.1 – 2.5 · Lab 2 · Mentor Session 2 · Problem Set 2

> Ordinary least squares in matrix form, its guarantees (Gauss–Markov, FWL), and the three ways the textbook story breaks (heteroskedasticity, clustering, misspecification).

By Thursday close you should be able to derive $\hat{\boldsymbol{\beta}} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$ on a whiteboard, run Fama–MacBeth on real CRSP returns, and tell the story of Petersen (2009) on standard errors.

---

## Daily schedule

=== "Mon Jun 29"

    | Block | What |
    |---|---|
    | 9:00 – 12:00 | Read **Ch 2.1 — OLS in Matrix Form**. Work `nb2.1` (OLS from scratch, NumPy vs. statsmodels). |
    | 1:00 – 4:00 | Live derivation on Zoom: normal equations, hat matrix, projection geometry. |
    | 4:00 – 5:00 | Office hours |

=== "Tue Jun 30"

    | Block | What |
    |---|---|
    | 9:00 – 12:00 | Read **Ch 2.2 — Gauss–Markov and the Meaning of "Best"**. Work `nb2.2` (Monte Carlo). |
    | 1:00 – 4:00 | Read **Ch 2.3 — Frisch–Waugh–Lovell**. Work `nb2.3` (residualization). |
    | 4:00 – 5:00 | Office hours |

=== "Wed Jul 1"

    | Block | What |
    |---|---|
    | 9:00 – 12:00 | Read **Ch 2.4 — Heteroskedasticity, Clustering, HC/HAC**. Work `nb2.4` (Petersen 2009 reproduction; t collapses from 5.70 to 2.19 under firm clustering). |
    | 2:00 – 3:30 | **Mentor Session 2 — "The standard-error ballgame"** |
    | 4:00 – 5:00 | Office hours |

=== "Thu Jul 2"

    | Block | What |
    |---|---|
    | 9:00 – 12:00 | Read **Ch 2.5 — Misspecification: OVB, Measurement Error, Functional Form**. Work `nb2.5`. |
    | 1:00 – 3:00 | **Lab 2 — Fama–MacBeth on CRSP** (2 hours live, build the rolling cross-sectional regressions). |
    | 3:00 – 4:30 | Wrap PS 2.1 – 2.5. Open the Week-2 PR. |
    | 4:30 – 5:00 | Retro + Week-3 preview |
    | **5:00 pm** | **Deliverable cutoff** (note: Friday is holiday) |

=== "Fri Jul 3"

    **HOLIDAY** — Independence Day observance. No meetings, no Slack expectations.

---

## What to read

- [Ch 2.1 — OLS in Matrix Form](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/book/weeks/week-02/ch21-ols-matrix-form.html)
- [Ch 2.2 — Gauss–Markov](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/book/weeks/week-02/ch22-gauss-markov.html)
- [Ch 2.3 — Frisch–Waugh–Lovell](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/book/weeks/week-02/ch23-frisch-waugh-lovell.html)
- [Ch 2.4 — Heteroskedasticity, Clustering, HC/HAC](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/book/weeks/week-02/ch24-heteroskedasticity-clustering-hac.html)
- [Ch 2.5 — Misspecification (OVB, Measurement Error)](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/book/weeks/week-02/ch25-misspecification-ovb-measurement-error.html)

**Notebooks** (`notebooks/week-02/`): nb2.1 through nb2.5.
**Lab:** [Lab 2 — Fama–MacBeth on CRSP](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/book/weeks/week-02/lab2-fama-macbeth-crsp.html).
**Mentor reading:** [Mentor 2 — "Standard-error ballgame"](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/book/weeks/week-02/mentor2-standard-error-ballgame.html).

---

## What to submit (due Thu Jul 2, 5:00 pm ET)

1. **Problem Set 2** ([PS 2.1](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/book/weeks/week-02/ps2.1.html) · [PS 2.2](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/book/weeks/week-02/ps2.2.html) · [PS 2.3](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/book/weeks/week-02/ps2.3.html) · [PS 2.4](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/book/weeks/week-02/ps2.4.html) · [PS 2.5](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/book/weeks/week-02/ps2.5.html)).
2. **Lab 2 notebook** with the Fama–MacBeth coefficient series + Newey–West-adjusted t-stat reported.
3. **Journal entry** — `journal/week-02.md`.
4. **Pull request** — `week-02 — <your name>`.

!!! warning "WRDS access required"
    Lab 2 pulls CRSP daily returns. You must have your GMU WRDS account active before Wednesday — see [Resources → Data access](../resources/data-access.md). If WRDS is not ready, the lab includes a deterministic synthetic-CRSP fallback so you can still complete it.

---

## Data we touch this week

- [CRSP (daily / monthly stock files)](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/crsp.html) — first live pull
- [FRED (risk-free rate, macro)](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/data-cards/fred.html) — for excess returns

---

## Next week preview

[**Week 3 — Causal Inference I →**](week-03.md). The Rubin causal model, propensity-score matching, entropy balancing, 2SLS, and the weak-IV pathology.
