---
title: "Week 1 — Foundations (Jun 22 – Jun 26, 2026)"
description: >-
  Probability, sampling, and the logic of inference — the foundation
  for everything else in the eight weeks.
---

# Week 1 — Foundations <span class="week-badge active">active</span>

**June 22 – June 26, 2026** · Chapters 1.1 – 1.5 · Lab 1 · Mentor Session 1 · Problem Set 1 (five problems)

> Rebuild probability and frequentist inference from the ground up, using simulation as the microscope, so OLS in Week 2 rests on solid foundations.

By the end of Friday you should be able to write — in code, by hand, and on a napkin — what an estimator's *sampling distribution* is, why the central limit theorem is the reason any of this works, and why a 95% confidence interval is a statement about the procedure, not the parameter.

---

## Daily schedule

All times Eastern. **Morning** = independent reading + notebook follow-along. **Afternoon** = live cohort time on Zoom. **4–5 pm** = office hours and stand-up.

=== "Mon Jun 22"

    | Block | What | Where |
    |---|---|---|
    | 9:00 – 12:00 | Read **Ch 1.1 — Joint, Conditional, and the Two Laws That Run Everything**. Work through `nb1.1` (LIE/LTV by simulation). | Textbook + your fork of the repo |
    | 1:00 – 4:00 | Kick-off Zoom (1:00 – 2:00) · Pair-debug `nb1.1` (2:00 – 4:00) | Zoom |
    | 4:00 – 5:00 | Sub-team stand-up + office hours | Zoom breakout |

=== "Tue Jun 23"

    | Block | What | Where |
    |---|---|---|
    | 9:00 – 12:00 | Read **Ch 1.2 — Expectations, Variance, Covariance as Geometry**. Work `nb1.2` (covariance matrices, correlation heatmaps). | Textbook + repo |
    | 1:00 – 4:00 | Start **PS 1.1** + **PS 1.2** drills. | Async, with Slack channel staffed |
    | 4:00 – 5:00 | Office hours — Prof. Gao | Zoom |

=== "Wed Jun 24"

    | Block | What | Where |
    |---|---|---|
    | 9:00 – 12:00 | Read **Ch 1.3 — Estimators and Their Sampling Distributions**. Work `nb1.3` (sampling-distribution explorer). | Textbook + repo |
    | 1:00 – 2:00 | Lunch / async | — |
    | 2:00 – 3:30 | **Mentor Session 1 — "What is a finding?"** (Prof. Gao, all 14) | Zoom |
    | 3:30 – 5:00 | PS 1.3 work block + office hours | Zoom |

=== "Thu Jun 25"

    | Block | What | Where |
    |---|---|---|
    | 9:00 – 12:00 | Read **Ch 1.4 — The LLN and the CLT, Shown Not Asserted**. Work `nb1.4` (LLN/CLT convergence). | Textbook + repo |
    | 1:00 – 4:00 | **Lab 1 — Coin-Flip Universe**: build a NumPy simulation that shows the LLN by *eye* and the CLT by *animation*. | Zoom + repo |
    | 4:00 – 5:00 | Office hours + sub-team check-in | Zoom |

=== "Fri Jun 26"

    | Block | What | Where |
    |---|---|---|
    | 9:00 – 12:00 | Read **Ch 1.5 — Hypothesis Testing Done Right**. Work `nb1.5` (power curves, t-test from scratch). | Textbook + repo |
    | 1:00 – 3:00 | Wrap **PS 1.1 – 1.5**. Commit, push, open the week-1 PR for review. | Repo |
    | 3:00 – 4:00 | Friday demo — one sub-team presents their cleanest CLT figure. | Zoom |
    | 4:00 – 5:00 | Week-1 retro + Week-2 preview | Zoom |
    | **5:00 pm** | **Deliverable cutoff** | — |

---

## What to read

The textbook is the primary text. Open the chapter, then the notebook of the same number side-by-side.

- [Ch 1.1 — Joint, Conditional, and the Two Laws That Run Everything](../../../book/weeks/week-01/ch11-joint-conditional-two-laws.md) (LIE, LTV)
- [Ch 1.2 — Expectations, Variance, Covariance as Geometry](../../../book/weeks/week-01/ch12-expectation-variance-geometry.md)
- [Ch 1.3 — Estimators and Their Sampling Distributions](../../../book/weeks/week-01/ch13-estimators-sampling-distributions.md)
- [Ch 1.4 — The LLN and the CLT, Shown Not Asserted](../../../book/weeks/week-01/ch14-lln-clt.md)
- [Ch 1.5 — Hypothesis Testing Done Right](../../../book/weeks/week-01/ch15-hypothesis-testing.md)

**Notebooks** (`notebooks/week-01/` in the repo): nb1.1 · nb1.2 · nb1.3 · nb1.4 · nb1.5. All run headless with `numpy.random.default_rng(42)`; no network access required.

**Lab:** [Lab 1 — Build a Coin-Flip Universe](../../../book/weeks/week-01/lab1-coin-flip-universe.md).

**Mentor reading** for Wednesday: [Mentor 1 — "What Is a Finding?"](../../../book/weeks/week-01/mentor1-what-is-a-finding.md).

---

## What to submit (due Fri Jun 26, 5:00 pm ET)

1. **Problem Set 1** — five problems committed to your fork:
    - [PS 1.1 — Conditional probability & LIE/LTV](../../../book/weeks/week-01/ps1.1.md)
    - [PS 1.2 — Expectation, variance, covariance geometry](../../../book/weeks/week-01/ps1.2.md)
    - [PS 1.3 — Bias, variance, MSE of estimators](../../../book/weeks/week-01/ps1.3.md)
    - [PS 1.4 — CLT / LLN by simulation](../../../book/weeks/week-01/ps1.4.md)
    - [PS 1.5 — Power, size, confidence intervals](../../../book/weeks/week-01/ps1.5.md)
2. **Lab 1 notebook** (`notebooks/week-01/lab1.ipynb`) — runs end-to-end on `numpy.random.default_rng(42)`.
3. **Journal entry** — one paragraph in `journal/week-01.md`: what clicked, what is still murky, the one question you would ask Prof. Gao if you could only ask one.
4. **Pull request** — open a PR titled `week-01 — <your name>` from your fork against `main`. A sub-leader will code-review before Monday.

!!! warning "Reproducibility check"
    Before you push, run `pytest -q notebooks/week-01/` from the repo root. If anything errors out, fix it locally — do not push red.

---

## Data we touch this week

None. Week 1 is all simulated data — that is the point. We need the universe to be one we control so the LLN and CLT are visible, not asserted.

A preview of where real data starts next week:

- [Data card — CRSP (daily/monthly stock files)](../../../data-cards/crsp.md) — comes online in Week 2.
- [Data card — FRED](../../../data-cards/fred.md) — your first FRED pull is in Week 2's Lab.

---

## Stuck? Office-hours playbook

If you are stuck for more than ~20 minutes:

1. Post in `#help` on Slack with a minimal reproducible example.
2. Tag your sub-leader (not Prof. Gao first — sub-leader first).
3. If still stuck, drop into the 4:00 – 5:00 pm office hour.

Office hours are on Mon, Tue, Wed, Thu at 4:00 pm ET. Friday's 4:00 pm slot is the demo + retro.

---

## Next week preview

[**Week 2 — The OLS Engine →**](week-02.md). Matrix-form OLS, Gauss–Markov, FWL, and the three ways the textbook story breaks (heteroskedasticity, clustering, misspecification). Real CRSP data starts on Wednesday.
