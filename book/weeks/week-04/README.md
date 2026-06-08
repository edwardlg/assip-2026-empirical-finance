# Week 4 — Causal Inference II: DiD, RD, Synthetic Control, and Shift-Share

The modern panel/quasi-experimental toolkit — and the recent literature showing the "obvious"
estimators are often wrong. See [`../../TOC.md`](../../TOC.md) for the full plan.

## Chapters
1. [Ch 4.1 — Difference-in-Differences & Event Studies](ch41-did-event-studies.md) (parallel trends, leads/lags)
2. [Ch 4.2 — The Staggered-Adoption Crisis](ch42-staggered-adoption-crisis.md) (Goodman-Bacon, negative weights, Callaway–Sant'Anna, Sun–Abraham, BJS)
3. [Ch 4.3 — Regression Discontinuity](ch43-regression-discontinuity.md) (sharp/fuzzy, local polynomial, IK/CCT bandwidth, McCrary)
4. [Ch 4.4 — Synthetic Control & Synthetic DiD](ch44-synthetic-control.md) (Abadie, placebo inference, Arkhangelsky et al.)
5. [Ch 4.5 — Bartik / Shift-Share Designs](ch45-bartik-shift-share.md) (GPSS shares vs. BHJ shifts; Rotemberg weights)

## Notebooks (`../../../notebooks/week-04/`)
- nb4.1 Event-study & parallel-trends tests · nb4.2 Staggered DiD: TWFE vs. Callaway–Sant'Anna (`differences`) · nb4.3 RD with `rdrobust` (CCT) · nb4.4 Synthetic control & synthetic DiD (`pysyncon`) · nb4.5 Bartik decomposition
- All verified to run headless. nb4.2 reproduces the TWFE sign-flip (+0.40) vs. CS (−2.571); nb4.5's Rotemberg weights reassemble the 2SLS estimate (−1.50).

## Problem sets (solutions in [Appendix E](../../appendices/E-solutions-manual/))
- [PS 4.1](ps4.1.md) 2×2 DiD & event study · [PS 4.2](ps4.2.md) Goodman-Bacon decomposition · [PS 4.3](ps4.3.md) RD & bandwidth · [PS 4.4](ps4.4.md) Synthetic control & placebo · [PS 4.5](ps4.5.md) Shift-share & identification critique

## Lab, mentor, assessment
- [Lab 4 — A Clean DiD on HMDA + a State Policy Shock](lab4-hmda-did.md) (real CFPB HMDA path + seeded synthetic fallback; Callaway–Sant'Anna)
- [Mentor Session 4 — "Detecting discrimination with a clean design"](mentor4-detecting-discrimination.md) (Gao & Sun 2019, *PNAS*)
- [Week 4 Assessment + Rubric](assessment4.md)
