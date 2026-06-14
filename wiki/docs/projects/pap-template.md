---
title: "Pre-Analysis Plan (PAP) Template"
description: >-
  One-page pre-analysis plan template — file before running the main
  specification. Mirrors Chapter 7.3 of the ASSIP textbook.
---

# Pre-Analysis Plan (PAP) Template

A pre-analysis plan is a short document you write **before** you look at the outcome data. It pins down what you expect to find, how you will measure it, and what would *change your mind*. The PAP is what separates a finding from a story; it is what makes the August 12 poster credible to a Mason faculty audience.

The standard we use is described in **Chapter 7.3** of the [textbook](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/) ("Pre-Analysis Plans and the Logic of Pre-Specification"). What follows is the one-pager that ships with this site — filled-in example first so you can see what a complete PAP looks like, then a blank template you can copy into `pap/pap-v1.md` in your repo.

!!! tip "How to file your PAP"
    1. Copy the **blank template** below into `pap/pap-v1.md` in your project repo.
    2. Fill it in (one page; do **not** exceed two pages).
    3. Open a PR titled `PAP v1 — [Project N] — [Your Name]`.
    4. Your pod's RA sub-leader reviews; Prof. Gao signs off.
    5. After merge, tag the commit `pap-v1` so the timestamp is on the record:
       `git tag -a pap-v1 -m "PAP filed" && git push --tags`.
    6. Update your card on the [project tracker](index.md) so the status flips from *Pending* → *Filed*.

---

## Example — filled PAP

> The example below uses Track 1 (Fair Lending) to make the template concrete. Your real PAP will differ in topic, data, and specification, but the **structure** is identical.

### Project title
*Are denial-rate gaps in mortgage lending mediated by lender-level algorithmic underwriting? Evidence from 2018 – 2024 HMDA + Census tracts.*

### Author and pod
Jane Doe, ASSIP 2026 Cohort, Pod B. Mentor: Prof. Lei Gao. Pod RA: [Sub-leader name].

### Research question (one sentence)
Conditional on observable creditworthiness, do Black and Hispanic mortgage applicants face higher denial rates at lenders that have adopted machine-learning underwriting than at lenders that have not?

### Hypothesis
**H₁:** The Black–White denial-rate gap is **smaller** at ML-adopting lenders than at non-adopters (the "fairness through automation" claim).
**H₀:** The Black–White denial-rate gap is **not statistically different** across the two lender groups at the 5% level.

I find H₀ more plausible *a priori* given Bartlett et al. (2022); the test has practical value either way.

### Data sources
- **HMDA Loan Application Register** (CFPB bulk download), 2018 – 2024.
- **ACS Census tract demographics**, 5-year estimates 2018 – 2022.
- **Hand-coded lender-ML-adoption indicator** from 10-K filings of the top-50 mortgage originators by volume (yes/no/ambiguous).

### Sample
First-lien, owner-occupied, conventional home-purchase loan applications, 2018 – 2024, originating in MSAs with at least 100 applications. Drop applications with missing income, race, or census-tract. Expected N ≈ 14 million applications, ≈ 9,500 lender-years.

### Specification
Linear probability model with two-way fixed effects:

`denied_{i,t} = α + β · race_i + γ · (race_i × MLadopt_{l(i),t}) + X_i'δ + φ_{l(i)} + φ_t + ε_{i,t}`

where `race_i` is Black/Hispanic/Asian dummies (White as omitted), `MLadopt` is the lender-level adoption indicator, `X_i` is the standard creditworthiness vector (income, loan-to-income, loan amount, property type), and `φ_l, φ_t` are lender and year fixed effects. Standard errors clustered at the lender level.

### Decision rule
The headline coefficient is **γ** on the (Black × MLadopt) interaction.

- **γ < 0 and p < 0.05** → reject H₀ in favor of H₁ ("fairness through automation" supported).
- **γ > 0 and p < 0.05** → reject H₀ against H₁ (ML *widens* the gap).
- **|t-stat(γ)| < 1.96** → fail to reject H₀; report the precision of the null.

### Robustness checks (committed *before* analysis)
1. Drop the COVID-disruption years (2020 – 2021); rerun.
2. Replace LPM with logit; report average marginal effects.
3. Restrict to MSAs that had at least one ML and one non-ML lender (within-market identification).
4. Recode the ML-adoption indicator using only post-2020 10-K language (robustness to coding date).
5. Permutation test: shuffle the `MLadopt` indicator 1,000 times and report the empirical null distribution of γ.

### What I am *not* going to look at before the PAP is filed
The outcome variable `denied` will not be merged into the analysis sample until **after** this PAP is tagged `pap-v1` in the repo. The merge step is in `code/03_build_sample.R`, which is staged but not executed before the tag.

### Ethical and licensing notes
HMDA is public-domain. ACS is public-domain. The 10-K-derived adoption indicator is my own hand-coding and is published under MIT. I am not using any WRDS data for this project.

---

## Blank template — copy this into `pap/pap-v1.md`

```markdown
# Pre-Analysis Plan v1

**Project title:**

**Author and pod:**

**Date filed (UTC):**  YYYY-MM-DD

---

## 1. Research question (one sentence)

## 2. Hypothesis
- H₁ (what I expect):
- H₀ (what would falsify H₁):

## 3. Data sources
- Primary:
- Secondary:
- Hand-coded / scraped:

## 4. Sample
- Unit of observation:
- Time window:
- Inclusion criteria:
- Exclusion criteria:
- Expected N:

## 5. Specification
Write the headline equation. Define every variable. State the standard-error
assumption (clustered? robust? two-way?).

## 6. Decision rule
What will I conclude if the headline coefficient is positive / negative /
indistinguishable from zero at the 5% level? Be specific *before* you look.

## 7. Robustness checks (pre-committed)
1.
2.
3.
4.
5.

## 8. What I am *not* going to look at before the PAP is filed
List the variable(s) — typically the outcome — that I will not merge into the
analysis sample until this PAP is tagged `pap-v1` in git.

## 9. Ethics and licensing
Data licenses. AI-tool usage (per Ch 6.5). Confidentiality of WRDS data
(stays on GMU infrastructure).

## 10. Sign-off
- Student: ______________________  Date: __________
- Pod RA sub-leader: ____________  Date: __________
- Mentor (Prof. Gao): ___________  Date: __________
```

---

## Why we do this

Pre-specification is not a bureaucratic ritual. It is the single most effective protection against the **garden of forking paths** — the slow drift, never deliberate, by which a researcher who has seen the data ends up running the specification that "works" rather than the specification that was honest. In your eight weeks here you will not have time to fall down that garden path twice. The PAP is the timestamp that lets your August 12 poster claim, credibly, that you knew what you were looking for before you found it.
