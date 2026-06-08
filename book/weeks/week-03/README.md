# Week 3 — Causal Inference I: Potential Outcomes, Selection-on-Observables, and Instruments

Correlation is cheap; the Rubin causal model makes "effect" precise, and we earn causal claims
through design, not control variables. See [`../../TOC.md`](../../TOC.md) for the full plan.

## Chapters
1. [Ch 3.1 — Potential Outcomes, SUTVA, and the Fundamental Problem](ch31-potential-outcomes-sutva.md)
2. [Ch 3.2 — Selection on Observables I: Matching & Propensity Scores](ch32-matching-propensity-scores.md)
3. [Ch 3.3 — Selection on Observables II: Entropy Balancing & Doubly-Robust](ch33-entropy-balancing-doubly-robust.md)
4. [Ch 3.4 — Instrumental Variables](ch34-instrumental-variables.md) (relevance/exclusion, 2SLS-as-FWL, LATE, weak IV)
5. [Ch 3.5 — Reading IV in the Wild + The Weak-IV Pathology](ch35-reading-iv-weak-iv-pathology.md) (Anderson–Rubin, many-instruments bias)

## Notebooks (`../../../notebooks/week-03/`)
- nb3.1 Potential outcomes & selection bias · nb3.2 PSM with balance diagnostics · nb3.3 Entropy balancing vs. IPW vs. AIPW · nb3.4 2SLS with first-stage F · nb3.5 Weak-IV pathology (conventional coverage 0.80 vs. Anderson–Rubin 0.97)
- All verified to run headless; numbers reproduce the chapters bit-for-bit.

## Problem sets (solutions in [Appendix E](../../appendices/E-solutions-manual/))
- [PS 3.1](ps3.1.md) Potential-outcomes algebra · [PS 3.2](ps3.2.md) Matching & propensity scores · [PS 3.3](ps3.3.md) Entropy balancing & AIPW · [PS 3.4](ps3.4.md) 2SLS & weak-IV F · [PS 3.5](ps3.5.md) Anderson–Rubin & validity critique

## Lab, mentor, assessment
- [Lab 3 — Reproduce a Weak-IV Pathology](lab3-weak-iv-pathology.md) (pure simulation; AR CIs as the fix)
- [Mentor Session 3 — "Natural experiments: finding the lever nature pulled"](mentor3-natural-experiments.md) (Deng, Gao & Kim 2020, *JCF*)
- [Week 3 Assessment + Rubric](assessment3.md)
