# Solutions — PS 2.3 (Frisch–Waugh–Lovell: Partialling-Out by Hand)

**Linked problem set:** `book/weeks/week-02/ps2.3.md` · Week 2, Chapter 2.3.
These solutions use only Ch 2.3 tools (and Ch 2.1's residual-maker matrix for the proof): the OLS estimator and its orthogonality, the residual-maker $\mathbf{M}_2 = \mathbf{I} - \mathbf{X}_2(\mathbf{X}_2'\mathbf{X}_2)^{-1}\mathbf{X}_2'$ with its symmetric/idempotent/annihilating properties, the simple-regression slope formulas, and the FWL theorem. Notation follows CONVENTIONS §3: $\tilde{\mathbf{y}} = \mathbf{M}_2\mathbf{y}$, $\tilde{\mathbf{X}}_1 = \mathbf{M}_2\mathbf{X}_1$, and $\ddot{x}_i = x_i - \bar{x}_{g(i)}$ for within-group demeaning. All arithmetic was verified in Python.

---

## Problem 1 — State it, then read it (12 pts)

**(a) [4 pts]** **FWL.** For the partitioned regression $\mathbf{y} = \mathbf{X}_1\boldsymbol{\beta}_1 + \mathbf{X}_2\boldsymbol{\beta}_2 + \boldsymbol{\varepsilon}$, the OLS coefficient $\hat{\boldsymbol{\beta}}_1$ on the regressor block $\mathbf{X}_1$ is identical to the OLS coefficient from the *simple* regression of the residualized outcome $\tilde{\mathbf{y}} = \mathbf{M}_2\mathbf{y}$ on the residualized regressor $\tilde{\mathbf{X}}_1 = \mathbf{M}_2\mathbf{X}_1$, where each variable has been residualized by regressing it on the control block $\mathbf{X}_2$ and keeping the residual; moreover the short regression's residuals equal the full regression's residuals.

The graded essentials: (i) you residualize *both* $\mathbf{y}$ and $\mathbf{X}_1$ on $\mathbf{X}_2$; (ii) the claim is the equality of $\hat{\boldsymbol{\beta}}_1^{\text{full}}$ and the leftover-on-leftover slope.

**(b) [4 pts]** The recipe that reproduces $\hat{\beta}_1 = 0.0042$:

1. Regress applicant income on credit score and loan-to-value (and an intercept); keep the residual $\tilde{x}$ — the part of income the two controls cannot explain.
2. Regress repayment... — here, the *outcome* (the dependent variable of the paper) on credit score and loan-to-value (and an intercept); keep the residual $\tilde{y}$.
3. Run the no-intercept simple regression of $\tilde{y}$ on $\tilde{x}$. Its slope is $0.0042$, exactly the multiple-regression coefficient.

"Controlling for credit score and loan-to-value" *is* steps 1–2: subtract out everything those two controls can linearly account for, from both the income variable and the outcome, then look only at the leftovers.

**(c) [4 pts]** **False.** FWL is an algebraic *identity*, true exactly whenever the OLS estimator exists — it holds regardless of whether the controls are weak or strong, and it is never an approximation. (It is not a statement about the data-generating process at all; it is a fact about the arithmetic of least squares.) Contrast: Gauss–Markov's conclusion that OLS is BLUE rests on *modeling assumptions* — in particular homoskedasticity, $\operatorname{Var}(\varepsilon_i) = \sigma^2$ for all $i$ — which genuinely can fail (heteroskedasticity, Ch 2.4), at which point OLS is no longer the minimum-variance linear unbiased estimator even though FWL still holds verbatim.

---

## Problem 2 — Partialling-out by hand: Maya's five borrowers (24 pts)

Setup: $y = (6,5,6,9,14)$, $x = (2,2,3,5,8)$, $z = (1,2,3,4,5)$; $\bar{y}=8$, $\bar{x}=4$, $\bar{z}=3$. The income deviations are $z_i - \bar{z} = (-2,-1,0,1,2)$, so $\operatorname{Var}(z) = \tfrac{1}{5}\sum (z_i-\bar z)^2 = \tfrac{1}{5}(4+1+0+1+4) = \tfrac{10}{5} = 2$. (Using the $1/N$ convention; any constant cancels in the slope ratios, so $1/N$ vs. $1/(N-1)$ is immaterial here.)

**(a) [7 pts] Residualize literacy on income.** The literacy deviations are $x_i - \bar{x} = (-2,-2,-1,1,4)$, so
$$
\operatorname{Cov}(x,z) = \tfrac{1}{5}\sum (x_i-\bar x)(z_i-\bar z) = \tfrac{1}{5}\big[(-2)(-2)+(-2)(-1)+(-1)(0)+(1)(1)+(4)(2)\big] = \tfrac{1}{5}(4+2+0+1+8) = \tfrac{15}{5} = 3.
$$
$$
a_1 = \frac{\operatorname{Cov}(x,z)}{\operatorname{Var}(z)} = \frac{3}{2} = 1.5, \qquad a_0 = \bar{x} - a_1\bar{z} = 4 - 1.5(3) = -0.5.
$$
The fitted values $\hat{x}_i = -0.5 + 1.5\,z_i$ and residuals $\tilde{x}_i = x_i - \hat{x}_i$:

| $i$ | $z_i$ | $\hat{x}_i = -0.5+1.5z_i$ | $x_i$ | $\tilde{x}_i$ |
|---|---|---|---|---|
| 1 | 1 | $1.0$ | 2 | $+1.0$ |
| 2 | 2 | $2.5$ | 2 | $-0.5$ |
| 3 | 3 | $4.0$ | 3 | $-1.0$ |
| 4 | 4 | $5.5$ | 5 | $-0.5$ |
| 5 | 5 | $7.0$ | 8 | $+1.0$ |

Sum: $1.0 - 0.5 - 1.0 - 0.5 + 1.0 = 0$. ✓ These residuals are **the part of financial literacy that income cannot explain** — each borrower's literacy relative to what their income level alone would predict.

**(b) [7 pts] Residualize repayment on income.** The repayment deviations are $y_i - \bar{y} = (-2,-3,-2,1,6)$, so
$$
\operatorname{Cov}(y,z) = \tfrac{1}{5}\big[(-2)(-2)+(-3)(-1)+(-2)(0)+(1)(1)+(6)(2)\big] = \tfrac{1}{5}(4+3+0+1+12) = \tfrac{20}{5} = 4,
$$
$$
c_1 = \frac{\operatorname{Cov}(y,z)}{\operatorname{Var}(z)} = \frac{4}{2} = 2, \qquad c_0 = \bar{y} - c_1\bar{z} = 8 - 2(3) = 2.
$$
Fitted $\hat{y}_i = 2 + 2z_i$, residuals $\tilde{y}_i = y_i - \hat{y}_i$:

| $i$ | $z_i$ | $\hat{y}_i = 2+2z_i$ | $y_i$ | $\tilde{y}_i$ |
|---|---|---|---|---|
| 1 | 1 | $4$ | 6 | $+2$ |
| 2 | 2 | $6$ | 5 | $-1$ |
| 3 | 3 | $8$ | 6 | $-2$ |
| 4 | 4 | $10$ | 9 | $-1$ |
| 5 | 5 | $12$ | 14 | $+2$ |

Sum: $2 - 1 - 2 - 1 + 2 = 0$. ✓ These are repayment beyond what income alone predicts.

**(c) [6 pts] Regress leftover on leftover.** No-intercept simple slope:
$$
\sum_i \tilde{x}_i\tilde{y}_i = (1)(2) + (-0.5)(-1) + (-1)(-2) + (-0.5)(-1) + (1)(2) = 2 + 0.5 + 2 + 0.5 + 2 = 7,
$$
$$
\sum_i \tilde{x}_i^2 = 1 + 0.25 + 1 + 0.25 + 1 = 3.5,
$$
$$
\boxed{\hat{\beta}_1 = \frac{\sum_i \tilde{x}_i\tilde{y}_i}{\sum_i \tilde{x}_i^2} = \frac{7}{3.5} = \frac{7}{7/2} = 2.000.}
$$
No intercept is needed because both residual vectors already sum to zero (residuals from a regression that included an intercept), so their means are zero and there is nothing for an intercept to fit.

**(d) [4 pts]** FWL guarantees this $\hat{\beta}_1 = 2$ is **exactly** the coefficient on literacy in the full three-regressor multiple regression $y = \beta_0 + \beta_1 x + \beta_2 z + \varepsilon$ — not approximately, exactly. One-line check:
```python
import statsmodels.api as sm, numpy as np
sm.OLS(y, sm.add_constant(np.column_stack([x, z]))).fit().params[1]  # -> 2.0
```
(Indeed the full fit is $\hat{\beta}_0 = 3$, $\hat{\beta}_1 = 2$, $\hat{\beta}_2 = -1$.) **Interpretation for Maya:** among borrowers with *more financial literacy than their income would predict*, each extra residual point of literacy is associated with about 2 more points of on-time repayment than their income would predict. The number is purely about the literacy variation that income leaves unexplained.

---

## Problem 3 — The residual-maker proof (20 pts)

**(a) [4 pts] The three properties of $\mathbf{M}_2 = \mathbf{I} - \mathbf{X}_2(\mathbf{X}_2'\mathbf{X}_2)^{-1}\mathbf{X}_2'$.**

- **Symmetric**, $\mathbf{M}_2' = \mathbf{M}_2$: the subtracted piece $\mathbf{X}_2(\mathbf{X}_2'\mathbf{X}_2)^{-1}\mathbf{X}_2'$ is its own transpose because $(\mathbf{X}_2'\mathbf{X}_2)^{-1}$ is symmetric (inverse of a symmetric matrix) and the outer $\mathbf{X}_2(\cdot)\mathbf{X}_2'$ sandwich is symmetric, and $\mathbf{I}$ is symmetric.
- **Idempotent**, $\mathbf{M}_2\mathbf{M}_2 = \mathbf{M}_2$: sweeping out the column space of $\mathbf{X}_2$ once leaves a vector already orthogonal to that space, so sweeping again removes nothing. (Algebraically the cross terms collapse via $(\mathbf{X}_2'\mathbf{X}_2)^{-1}(\mathbf{X}_2'\mathbf{X}_2) = \mathbf{I}$.)
- **Annihilates its own block**, $\mathbf{M}_2\mathbf{X}_2 = \mathbf{0}$: regressing $\mathbf{X}_2$ on itself leaves zero residual, since $\mathbf{X}_2(\mathbf{X}_2'\mathbf{X}_2)^{-1}\mathbf{X}_2'\mathbf{X}_2 = \mathbf{X}_2$, so $\mathbf{M}_2\mathbf{X}_2 = \mathbf{X}_2 - \mathbf{X}_2 = \mathbf{0}$.

**(b) [8 pts]** Start from the full-model fit and left-multiply by $\mathbf{M}_2$:
$$
\mathbf{M}_2\mathbf{y} = \mathbf{M}_2\mathbf{X}_1\hat{\boldsymbol{\beta}}_1 + \mathbf{M}_2\mathbf{X}_2\hat{\boldsymbol{\beta}}_2 + \mathbf{M}_2\hat{\boldsymbol{\varepsilon}}.
$$
Term by term:

- Left side: $\mathbf{M}_2\mathbf{y} = \tilde{\mathbf{y}}$ by definition.
- First term: $\mathbf{M}_2\mathbf{X}_1\hat{\boldsymbol{\beta}}_1 = \tilde{\mathbf{X}}_1\hat{\boldsymbol{\beta}}_1$ by definition of $\tilde{\mathbf{X}}_1 = \mathbf{M}_2\mathbf{X}_1$.
- Second term **dies**: $\mathbf{M}_2\mathbf{X}_2 = \mathbf{0}$ (annihilation), so $\mathbf{M}_2\mathbf{X}_2\hat{\boldsymbol{\beta}}_2 = \mathbf{0}$. This is the heart of the theorem — sweeping out $\mathbf{X}_2$ erases the entire control contribution.
- Third term **survives unchanged**: $\hat{\boldsymbol{\varepsilon}}$ is already orthogonal to $\mathbf{X}_2$ ($\mathbf{X}_2'\hat{\boldsymbol{\varepsilon}} = \mathbf{0}$), so $\mathbf{M}_2\hat{\boldsymbol{\varepsilon}} = \hat{\boldsymbol{\varepsilon}} - \mathbf{X}_2(\mathbf{X}_2'\mathbf{X}_2)^{-1}\underbrace{\mathbf{X}_2'\hat{\boldsymbol{\varepsilon}}}_{=\mathbf{0}} = \hat{\boldsymbol{\varepsilon}}$.

Collecting:
$$
\boxed{\tilde{\mathbf{y}} = \tilde{\mathbf{X}}_1\hat{\boldsymbol{\beta}}_1 + \hat{\boldsymbol{\varepsilon}}.}
$$

**(c) [6 pts]** Left-multiply by $\tilde{\mathbf{X}}_1'$:
$$
\tilde{\mathbf{X}}_1'\tilde{\mathbf{y}} = \tilde{\mathbf{X}}_1'\tilde{\mathbf{X}}_1\,\hat{\boldsymbol{\beta}}_1 + \tilde{\mathbf{X}}_1'\hat{\boldsymbol{\varepsilon}}.
$$
The cross term vanishes. Using symmetry, $\tilde{\mathbf{X}}_1' = (\mathbf{M}_2\mathbf{X}_1)' = \mathbf{X}_1'\mathbf{M}_2'= \mathbf{X}_1'\mathbf{M}_2$, so
$$
\tilde{\mathbf{X}}_1'\hat{\boldsymbol{\varepsilon}} = \mathbf{X}_1'\mathbf{M}_2\hat{\boldsymbol{\varepsilon}} = \mathbf{X}_1'\hat{\boldsymbol{\varepsilon}} = \mathbf{0},
$$
where the middle step uses $\mathbf{M}_2\hat{\boldsymbol{\varepsilon}} = \hat{\boldsymbol{\varepsilon}}$ (from part b) and the last step uses the full-model orthogonality $\mathbf{X}_1'\hat{\boldsymbol{\varepsilon}} = \mathbf{0}$. With the cross term gone, the normal equation of a simple regression remains:
$$
\tilde{\mathbf{X}}_1'\tilde{\mathbf{X}}_1\,\hat{\boldsymbol{\beta}}_1 = \tilde{\mathbf{X}}_1'\tilde{\mathbf{y}} \quad\Longrightarrow\quad \boxed{\hat{\boldsymbol{\beta}}_1 = (\tilde{\mathbf{X}}_1'\tilde{\mathbf{X}}_1)^{-1}\tilde{\mathbf{X}}_1'\tilde{\mathbf{y}}.} \qquad\blacksquare
$$

**(d) [2 pts]** The boxed equation in part (b), $\tilde{\mathbf{y}} = \tilde{\mathbf{X}}_1\hat{\boldsymbol{\beta}}_1 + \hat{\boldsymbol{\varepsilon}}$, shows the *same* $\hat{\boldsymbol{\varepsilon}}$ — the full-model residual — is also the residual of the short (residualized) regression. This matters for Ch 2.4 because the residual sum of squares is therefore identical, so the *point estimate and the residuals* from partialling-out are correct; but the degrees of freedom must be counted as $N - K$ on the **long** regression (counting the partialled-out columns of $\mathbf{X}_2$), not the $N - 1$ or $N - 2$ a naïve short regression would assume. Quote the long regression's standard error, not the short one's.

---

## Problem 4 — What "holding constant" really means (14 pts)

**(a) [5 pts]** The regression cannot hold income fixed: the five borrowers have whatever incomes they have, and nothing wiggles. What it actually did was **subtract** (residualize) the linear influence of income out of *both* literacy and repayment, and then measure how the leftovers move together. So the coefficient is a statement entirely about *leftover* variation: it answers "among borrowers with more literacy than their income predicts, do we see more repayment than their income predicts?" It is built only from the parts of literacy and repayment that income cannot account for — a subtraction, not a filter or an experiment.

**(b) [5 pts]** Residualizing $x$ on a control means subtracting off the part of $x$ the control can predict, leaving $\tilde{x}$. If the control is essentially *unrelated* to $x$, the regression of $x$ on it has near-zero slope, so almost nothing is subtracted: $\tilde{x} \approx x$, and the leftover-on-leftover slope is nearly the original — the coefficient barely moves. If the control is *strongly related* to $x$ (as income is to literacy), residualizing strips out a large chunk of $x$, so $\tilde{x}$ differs substantially from $x$, and the slope of $\tilde{y}$ on $\tilde{x}$ can land far from the raw slope. FWL makes this mechanical: a control matters to the coefficient exactly to the extent that it overlaps with — and therefore gets subtracted from — the regressor of interest.

**(c) [4 pts]** FWL says Priya's coefficient is a clean simple slope in the space orthogonal to *exactly the columns she included* — here, log assets (and the intercept) — and *nothing else*. Residualizing on log assets removes only the part of disclosure quality and of her regressor that runs through firm size as she measured it. It does **not** touch firm age: if age drives both disclosure and size for reasons not captured by log assets, then age's fingerprints remain inside both residualized variables, uncontrolled, and her coefficient is "holding size constant" but *not* holding age constant. This is why CONVENTIONS §4 demands she name her controls and identifying assumption: the list of what she residualized *is* the precise boundary of what "holding constant" covers, and age — outside that list — is a named threat she has not addressed.

---

## Problem 5 — Demeaning is the within transformation (18 pts)

Data: group A (desks 1–3) $x=(2,4,6)$, $y=(3,6,9)$; group B (desks 4–6) $x=(3,5,7)$, $y=(8,11,14)$.

**(a) [4 pts] Group means and demeaned columns.**
$$
\bar{x}_A = \tfrac{2+4+6}{3} = 4, \quad \bar{x}_B = \tfrac{3+5+7}{3} = 5, \quad \bar{y}_A = \tfrac{3+6+9}{3} = 6, \quad \bar{y}_B = \tfrac{8+11+14}{3} = 11.
$$
Subtracting each desk's *own group* mean:

| $i$ | group | $\ddot{x}_i = x_i - \bar{x}_g$ | $\ddot{y}_i = y_i - \bar{y}_g$ |
|---|---|---|---|
| 1 | A | $2-4 = -2$ | $3-6 = -3$ |
| 2 | A | $4-4 = 0$ | $6-6 = 0$ |
| 3 | A | $6-4 = +2$ | $9-6 = +3$ |
| 4 | B | $3-5 = -2$ | $8-11 = -3$ |
| 5 | B | $5-5 = 0$ | $11-11 = 0$ |
| 6 | B | $7-5 = +2$ | $14-11 = +3$ |

Clean integers, and each column sums to zero within each group. ✓

**(b) [5 pts] Within slope.**
$$
\sum_i \ddot{x}_i\ddot{y}_i = (-2)(-3) + 0 + (2)(3) + (-2)(-3) + 0 + (2)(3) = 6 + 6 + 6 + 6 = 24,
$$
$$
\sum_i \ddot{x}_i^2 = 4 + 0 + 4 + 4 + 0 + 4 = 16,
$$
$$
\boxed{\hat{\beta}_1 = \frac{24}{16} = \frac{3}{2} = 1.500.}
$$

**(c) [5 pts]** By FWL, the control block here is $\mathbf{X}_2 = [\boldsymbol{\iota},\ \mathbf{D}]$ — the intercept together with the group dummy $D_i = \mathbf{1}\{i \in \text{B}\}$ (equivalently, a full set of two group indicators). Regressing any variable on a *complete set of group dummies* fits, for each observation, its own group's mean as the predicted value — because the best constant within each group, in least squares, is that group's mean. Hence the residual maker $\mathbf{M}_2$ subtracts the group-specific mean: $(\mathbf{M}_2\mathbf{y})_i = y_i - \bar{y}_{g(i)} = \ddot{y}_i$, and likewise for $x$. So the demeaned columns $\ddot{x}, \ddot{y}$ *are* $\tilde{\mathbf{X}}_1, \tilde{\mathbf{y}}$, and FWL says the slope of $\ddot{y}$ on $\ddot{x}$ equals the coefficient on $x$ in the full regression of $y$ on $x$ plus the group dummy. (Confirmed numerically: that dummy regression returns coefficient $1.5$ on $x$, with a group-B dummy of $3.5$ and intercept $0$.) The two routes give the identical slope because demeaning *is* multiplication by the dummies' residual maker.

**(d) [4 pts]** The **pooled** slope ($1.8$) answers: across *all* desks ignoring strategy type, how does return move with signal strength? — it blends *within*-group variation with *between*-group differences (group B has both higher signal and much higher return, inflating the apparent slope). The **within** slope ($1.5$) answers: holding strategy type constant, how does return move with signal *within* a strategy? — using only deviations from each group's own mean, discarding all between-group variation. This is exactly Ch 2.3's point that "controlling for industry asks a different question than controlling for size": controlling for the group changes *which variation* the slope is built from, so the number changes. This within machinery *is* the **fixed-effects** estimator of Week 3: the group dummy is a desk-type fixed effect, and $y_{ig} = \alpha_g + \beta x_{ig} + \varepsilon_{ig}$ estimated by subtracting group means gives the same $\beta$ as putting in a dummy per group. Packages demean rather than build the dummy matrix because demeaning costs only a group-average computation, whereas the dummy route would invert a matrix with one column per group — prohibitive when there are thousands of groups.

---

## Problem 6 — Short vs. long: FWL as the lens on omitted-variable bias (12 pts)

Maya's five borrowers again: $y=(6,5,6,9,14)$, $x=(2,2,3,5,8)$, $z=(1,2,3,4,5)$; $\bar{x}=4$, $\bar{y}=8$. Long coefficients (from Problem 2 and the full fit): $\hat{\beta}_1^{\text{long}} = 2$, $\hat{\beta}_2^{\text{long}} = -1$.

**(a) [5 pts] Short slope.** From the deviations $x_i-\bar{x} = (-2,-2,-1,1,4)$ and $y_i-\bar{y} = (-2,-3,-2,1,6)$:
$$
\operatorname{Cov}(x,y) = \tfrac{1}{5}\big[(-2)(-2)+(-2)(-3)+(-1)(-2)+(1)(1)+(4)(6)\big] = \tfrac{1}{5}(4+6+2+1+24) = \tfrac{37}{5},
$$
$$
\operatorname{Var}(x) = \tfrac{1}{5}\big[(-2)^2+(-2)^2+(-1)^2+1^2+4^2\big] = \tfrac{1}{5}(4+4+1+1+16) = \tfrac{26}{5},
$$
$$
\boxed{\hat{\beta}_1^{\text{short}} = \frac{\operatorname{Cov}(x,y)}{\operatorname{Var}(x)} = \frac{37/5}{26/5} = \frac{37}{26} \approx 1.423.}
$$
This is **smaller** than the long coefficient $2$.

**(b) [4 pts]** Run the FWL picture in reverse. In the *long* regression, income $z$ was residualized out of literacy, so the slope used only literacy's own income-free variation. In the *short* regression nothing is residualized: the raw literacy variable still carries the income signal inside it (higher-income borrowers tend to have higher literacy). So the short coefficient absorbs not just the genuine literacy effect but also the part of repayment that travels with literacy *through income*. Because income has a **negative** partial association with repayment here ($\hat{\beta}_2^{\text{long}} = -1$) and is **positively** related to literacy, leaving income in pulls the literacy coefficient *down*, from $2$ to about $1.423$. The short coefficient is absorbing income's signal.

**(c) [3 pts]** The auxiliary slope of the omitted control $z$ on the included regressor $x$:
$$
\hat{\delta} = \frac{\operatorname{Cov}(x,z)}{\operatorname{Var}(x)} = \frac{15/5}{26/5} = \frac{15}{26} \approx 0.577,
$$
using $\operatorname{Cov}(x,z) = 3$ (i.e. $15/5$) from Problem 2(a). Plug into the decomposition:
$$
\hat{\beta}_1^{\text{long}} + \hat{\beta}_2^{\text{long}}\cdot\hat{\delta} = 2 + (-1)\cdot\frac{15}{26} = \frac{52}{26} - \frac{15}{26} = \frac{37}{26} = \hat{\beta}_1^{\text{short}}. \quad\checkmark
$$
This recovers the part-(a) number exactly. Ch 2.5 will name the two factors of omitted-variable bias as **(i)** the effect of the omitted variable on the outcome ($\hat{\beta}_2^{\text{long}}$) times **(ii)** the slope relating the omitted variable to the included regressor ($\hat{\delta}$) — bias $= \hat{\beta}_2^{\text{long}}\cdot\hat{\delta}$, both of which you have just seen are residualization quantities.

---

*End of solutions for PS 2.3.*
