# Week 2 — The OLS Engine

Ordinary least squares in matrix form, its guarantees (Gauss–Markov, FWL), and the three ways the
textbook story breaks (heteroskedasticity, clustering, misspecification). See
[`../../TOC.md`](../../TOC.md) for the full plan.

## Chapters
1. [Ch 2.1 — OLS in Matrix Form](ch21-ols-matrix-form.md) (normal equations, hat matrix, projection)
2. [Ch 2.2 — Gauss–Markov and the Meaning of "Best"](ch22-gauss-markov.md) (BLUE, unbiased vs. consistent)
3. [Ch 2.3 — The Frisch–Waugh–Lovell Theorem](ch23-frisch-waugh-lovell.md) (partialling-out, demeaning = fixed effects)
4. [Ch 2.4 — Heteroskedasticity, Clustering, HC/HAC](ch24-heteroskedasticity-clustering-hac.md) (robust SEs; Petersen 2009)
5. [Ch 2.5 — Misspecification: OVB, Measurement Error, Functional Form](ch25-misspecification-ovb-measurement-error.md) (bridge to causal inference)

## Notebooks (`../../../notebooks/week-02/`)
- nb2.1 OLS from scratch (NumPy vs. statsmodels) · nb2.2 Gauss–Markov Monte Carlo · nb2.3 FWL residualization · nb2.4 SE flavors on a clustered panel · nb2.5 Biased-estimator lab (OVB & attenuation)
- All verified to run headless; nb2.4 reproduces the t-stat collapse (classical t≈5.70 → firm-cluster t≈2.19).

## Problem sets (solutions in [Appendix E](../../appendices/E-solutions-manual/))
- [PS 2.1](ps2.1.md) Matrix-OLS derivations · [PS 2.2](ps2.2.md) Gauss–Markov diagnostics · [PS 2.3](ps2.3.md) FWL partialling-out · [PS 2.4](ps2.4.md) Robust/clustered/HAC SEs · [PS 2.5](ps2.5.md) OVB & measurement error

## Lab, mentor, assessment
- [Lab 2 — Replicate a Textbook Fama–MacBeth on CRSP](lab2-fama-macbeth-crsp.md) (real WRDS path + seeded synthetic fallback)
- [Mentor Session 2 — "Why your standard error is the whole ballgame"](mentor2-standard-error-ballgame.md) (Petersen 2009; Gao et al. 2024 JCF)
- [Week 2 Assessment + Rubric](assessment2.md)
