# Solutions — PS 2.2 (Gauss–Markov: Breaking the Contract on Purpose)

**Linked problem set:** `book/weeks/week-02/ps2.2.md` · Week 2, Chapter 2.2.
These solutions use only Ch 2.2 tools: the five classical assumptions; the contamination identity $\hat{\boldsymbol{\beta}} = \boldsymbol{\beta} + (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\boldsymbol{\varepsilon}$; the variance formula $\sigma^2(\mathbf{X}'\mathbf{X})^{-1}$ and its scalar form; BLUE/efficiency; unbiased-vs-consistent. Forward references (OVB → Ch 2.5; robust/clustered SEs → Ch 2.4; functional form/multicollinearity → Ch 2.3) are *used* but not re-derived, exactly as the problem set permits. Notation follows CONVENTIONS §3.

---

## Problem 1 — Read the contract back to me (12 pts)

**(a) [6 pts]** The five assumptions, each as a falsifiable claim about the data-generating process:

1. **Linearity in parameters.** The truth is $\mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\varepsilon}$: the outcome is a sum of the columns of $\mathbf{X}$ each scaled by a *constant* coefficient, plus an error. The model must be linear in the $\beta$'s — not in the $x$'s, so $x^2$ or $\log x$ as columns are fine; a coefficient in an exponent is not.
2. **Random sampling + full column rank of $\mathbf{X}$.** The $N$ rows are a representative draw from the target population, and no column of $\mathbf{X}$ is an exact linear combination of the others (so $\mathbf{X}'\mathbf{X}$ is invertible).
3. **Zero conditional mean:** $\mathbb{E}[\boldsymbol{\varepsilon}\mid\mathbf{X}] = \mathbf{0}$. Whatever the model leaves out averages to zero at every configuration of the regressors — the error is not systematically related to $\mathbf{X}$.
4. **Homoskedasticity:** $\operatorname{Var}(\boldsymbol{\varepsilon}\mid\mathbf{X}) = \sigma^2\mathbf{I}$. The errors share one variance $\sigma^2$ (constant diagonal) and are uncorrelated across observations (zero off-diagonals).
5. **Normality:** $\boldsymbol{\varepsilon}\mid\mathbf{X} \sim \mathcal{N}(\mathbf{0}, \sigma^2\mathbf{I})$. The errors are Gaussian — an add-on for exact small-sample inference, *not* part of Gauss–Markov.

**(b) [4 pts]**

| # | What you'd see if it fails | Classification |
|---|---|---|
| 1 | Wrong functional form; residuals show a U-/arc-shaped pattern vs. the regressor | **Bias** (the fitted line is the wrong shape, so coefficients are mis-aimed) |
| 2 (rank) | $\mathbf{X}'\mathbf{X}$ singular; software errors or drops a column | **Neither — mechanical**: $(\mathbf{X}'\mathbf{X})^{-1}$ does not exist, so $\hat{\boldsymbol{\beta}}$ is *undefined*, not biased |
| 3 | Coefficient silently absorbs an omitted, correlated effect | **Bias** (the master fault) |
| 4 | Untrustworthy t-stats and confidence intervals; OLS no longer minimum-variance | **Precision/standard-error** (estimate still unbiased) |
| 5 | Exact small-sample $t$/$F$ no longer exact | **Precision/inference** (but CLT rescues large samples) |

The mechanical one is **Assumption 2's full-rank half**: without an invertible $\mathbf{X}'\mathbf{X}$ there is no formula to be biased *or* unbiased — like dividing by zero.

**(c) [2 pts]** **Assumptions 1–3 buy unbiasedness. Adding 4 buys BLUE** (minimum variance among linear unbiased estimators). **Adding 5 buys exact small-sample inference.** Gauss–Markov needs only 1–4; **normality (Assumption 5) is not needed for Gauss–Markov at all.**

---

## Problem 2 — Prove OLS is unbiased, and find the line that breaks (16 pts)

**(a) [7 pts]** Start from the estimator and substitute the true model $\mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\varepsilon}$:
$$
\hat{\boldsymbol{\beta}} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'(\mathbf{X}\boldsymbol{\beta} + \boldsymbol{\varepsilon}).
$$
Distribute across the sum:
$$
= (\mathbf{X}'\mathbf{X})^{-1}(\mathbf{X}'\mathbf{X})\,\boldsymbol{\beta} + (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\boldsymbol{\varepsilon}.
$$
A matrix times its own inverse is the identity, $(\mathbf{X}'\mathbf{X})^{-1}(\mathbf{X}'\mathbf{X}) = \mathbf{I}$, and $\mathbf{I}\boldsymbol{\beta} = \boldsymbol{\beta}$, so
$$
\boxed{\hat{\boldsymbol{\beta}} = \boldsymbol{\beta} + (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\boldsymbol{\varepsilon}.}
$$
Two assumptions were used *silently* just to write this: **Assumption 1 (linearity)**, used the instant we wrote $\mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\varepsilon}$, and **Assumption 2 (full rank)**, used so that $(\mathbf{X}'\mathbf{X})^{-1}$ exists at all.

**(b) [5 pts]** Condition on $\mathbf{X}$. Once $\mathbf{X}$ is fixed, the matrix $(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'$ is a *constant* (it depends only on $\mathbf{X}$, not on the random $\boldsymbol{\varepsilon}$), so it pulls outside the expectation:
$$
\mathbb{E}[\hat{\boldsymbol{\beta}}\mid\mathbf{X}] = \boldsymbol{\beta} + (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\,\mathbb{E}[\boldsymbol{\varepsilon}\mid\mathbf{X}].
$$
By **Assumption 3**, $\mathbb{E}[\boldsymbol{\varepsilon}\mid\mathbf{X}] = \mathbf{0}$, killing the second term:
$$
\mathbb{E}[\hat{\boldsymbol{\beta}}\mid\mathbf{X}] = \boldsymbol{\beta}. \quad\blacksquare
$$
Conditioning on $\mathbf{X}$ is exactly what demotes $(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'$ from "random matrix" to "known constant," which is the only thing that licenses pulling it out (the same move as pulling $\tfrac1N$ out of $\mathbb{E}[\bar x]$). For the unconditional result, apply the **law of total expectation**:
$$
\mathbb{E}[\hat{\boldsymbol{\beta}}] = \mathbb{E}\big[\mathbb{E}[\hat{\boldsymbol{\beta}}\mid\mathbf{X}]\big] = \mathbb{E}[\boldsymbol{\beta}] = \boldsymbol{\beta}.
$$

**(c) [4 pts]**

(i) **Heteroskedasticity does not touch part (b).** The proof used only the *mean* of $\boldsymbol{\varepsilon}$ given $\mathbf{X}$ (Assumption 3), never its *variance*. Nowhere did we invoke $\operatorname{Var}(\boldsymbol{\varepsilon}\mid\mathbf{X})$. So $\hat{\boldsymbol{\beta}}$ remains unbiased no matter how the error spread varies across borrowers — heteroskedasticity damages the variance formula (next problem), not the aim.

(ii) If $\mathbb{E}[\boldsymbol{\varepsilon}\mid\mathbf{X}] = \mathbf{a} \neq \mathbf{0}$, then
$$
\mathbb{E}[\hat{\boldsymbol{\beta}}\mid\mathbf{X}] = \boldsymbol{\beta} + (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\,\mathbb{E}[\boldsymbol{\varepsilon}\mid\mathbf{X}] \neq \boldsymbol{\beta}.
$$
The leftover term $(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\,\mathbb{E}[\boldsymbol{\varepsilon}\mid\mathbf{X}]$ is the **omitted-variable bias** (Ch 2.5). The algebra ran perfectly; what failed was the *empirical claim* $\mathbb{E}[\boldsymbol{\varepsilon}\mid\mathbf{X}] = \mathbf{0}$ — the assumption, not the math.

---

## Problem 3 — The variance formula, by hand (20 pts)

**(a) [6 pts]** With an intercept and one regressor, the rows of $\mathbf{X}$ are $(1, x_i)$, so
$$
\mathbf{X}'\mathbf{X} = \begin{pmatrix} N & \sum x_i \\ \sum x_i & \sum x_i^2 \end{pmatrix}.
$$
For a $2\times2$ matrix the inverse is $\tfrac{1}{\det}\begin{pmatrix} d & -b \\ -c & a\end{pmatrix}$. Here
$$
\det(\mathbf{X}'\mathbf{X}) = N\sum x_i^2 - \big(\textstyle\sum x_i\big)^2 = N\Big(\sum x_i^2 - N\bar x^2\Big) = N\sum (x_i - \bar x)^2,
$$
using $\sum x_i = N\bar x$ and the identity $\sum x_i^2 - N\bar x^2 = \sum(x_i-\bar x)^2$. The inverse is
$$
(\mathbf{X}'\mathbf{X})^{-1} = \frac{1}{N\sum(x_i-\bar x)^2}\begin{pmatrix} \sum x_i^2 & -\sum x_i \\ -\sum x_i & N \end{pmatrix}.
$$
Multiplying by $\sigma^2$ and reading the **bottom-right** entry (the slope's variance) gives the $N$ in the numerator cancelling the $N$ in the determinant:
$$
\operatorname{Var}(\hat{\beta}_1\mid\mathbf{X}) = \sigma^2 \cdot \frac{N}{N\sum(x_i-\bar x)^2} = \frac{\sigma^2}{\sum(x_i-\bar x)^2} = \frac{\sigma^2}{(N-1)s_x^2}, \quad\blacksquare
$$
since $s_x^2 = \tfrac{1}{N-1}\sum(x_i-\bar x)^2$ by definition.

**(b) [6 pts]** With $\sigma = 1.2$, $N = 250$, $s_x = 20$:
$$
\operatorname{Var}(\hat{\beta}_1) = \frac{1.2^2}{(250-1)\cdot 20^2} = \frac{1.44}{249 \times 400} = \frac{1.44}{99{,}600} \approx 1.4458\times 10^{-5}.
$$
$$
\operatorname{se}(\hat{\beta}_1) = \sqrt{1.4458\times 10^{-5}} \approx \boxed{0.003802} \text{ (percentage points per \$1{,}000)}.
$$

**(c) [4 pts]** $\operatorname{Var}(\hat\beta_1)$ has $s_x^2$ in the denominator, so doubling $s_x$ (to $40$) **quarters the variance** (factor $\tfrac14$) and **halves the standard error** (factor $\tfrac12$): $\operatorname{se}$ falls from $0.003802$ to $0.001901$. The chapter calls spread "the multivariate version of sample size" because the only other lever for shrinking $\operatorname{se}$ is $N$, and $\operatorname{se} \propto 1/\sqrt{N}$: to *halve* the standard error through sample size alone you would need to **quadruple $N$** (from $250$ to $1{,}000$). Doubling the income spread buys the same precision as quadrupling the sample.

**(d) [4 pts]** The rival's standard error with $N = 2{,}500$ and $s_x = 4$:
$$
\operatorname{Var}(\hat\beta_1) = \frac{1.2^2}{(2{,}500-1)\cdot 4^2} = \frac{1.44}{2{,}499 \times 16} = \frac{1.44}{39{,}984} \approx 3.601\times 10^{-5},
$$
$$
\operatorname{se}(\hat\beta_1) = \sqrt{3.601\times10^{-5}} \approx \mathbf{0.006001}.
$$
This is **larger (worse) than Maya's $0.003802$** — even though he has *ten times* as many loans. The arithmetic shows why: his denominator is $(N-1)s_x^2 = 2{,}499\times 16 \approx 4.0\times10^4$, *below* Maya's $99{,}600$, because cutting the income spread from $20$ to $4$ shrinks $s_x^2$ by a factor of $25$, and tenfold $N$ only partly compensates. **Maya estimates the slope more precisely** despite her smaller sample. **Moral:** for estimating a slope, *spread in the regressor* is what buys precision; piling up observations inside a narrow income band wastes most of them, because there is no $x$-variation to pin down the line's tilt.

---

## Problem 4 — Why "Best" means minimum variance among a club (16 pts)

**(a) [4 pts]** "Best" is a claim about **minimum variance** (equivalently, since all contestants are unbiased, minimum MSE). The comparison class is every estimator that is both **linear in $\mathbf{y}$** (of the form $\mathbf{C}\mathbf{y}$ with $\mathbf{C}$ depending on $\mathbf{X}$ but not $\mathbf{y}$) **and unbiased**. "Best" is technical, not a compliment, because it asserts *one specific ranking property* (smallest sampling variance) within *one specific, bounded club* — not all-around superiority.

**(b) [5 pts]** Two distinct reasons:

1. **Class restriction.** "Best" only ranks OLS first within the *linear unbiased* club. Estimators *outside* the club can beat it: e.g., **maximum likelihood** with a correctly specified *non-normal* error distribution is nonlinear in $\mathbf{y}$ and can have lower variance. To use it you must give up linearity (and commit to a correct distributional model).
2. **Assumption failure.** **Homoskedasticity (Assumption 4)** is what makes OLS *Best*. If it fails, OLS stays unbiased (Problem 2c-i) but loses the "B": **weighted least squares**, which down-weights the noisy observations, attains lower variance. The fallout — that the classical SE formula is no longer trustworthy — is repaired in **Chapter 2.4** with robust standard errors.

**(c) [5 pts]**

(i) $\sigma^2\mathbf{D}\mathbf{D}'$ is **never negative** because $\mathbf{D}\mathbf{D}'$ is a *sum of squares* (its diagonal entries are squared row-norms of $\mathbf{D}$, and as a quadratic form $\mathbf{v}'\mathbf{D}\mathbf{D}'\mathbf{v} = \|\mathbf{D}'\mathbf{v}\|^2 \ge 0$), and $\sigma^2 > 0$. The *only* way to make it exactly zero is $\mathbf{D} = \mathbf{0}$ — which makes the rival *equal to OLS*. Any genuine deviation strictly adds variance.

(ii) Same shape as bias–variance: there, $\text{MSE} = \text{bias}^2 + \text{variance}$, a target term plus a non-negative penalty, minimized by zeroing the penalty. Here, $\operatorname{Var}(\tilde{\boldsymbol{\beta}}) = \underbrace{\sigma^2(\mathbf{X}'\mathbf{X})^{-1}}_{\text{target}} + \underbrace{\sigma^2\mathbf{D}\mathbf{D}'}_{\text{penalty}\,\ge\,0}$, minimized by setting the penalty ($\mathbf{D}$) to zero. Identical logic: a floor you cannot beat, plus an unavoidable add-on you want gone.

(iii) **Homoskedasticity (Assumption 4)** is the load-bearing one: it is what let us substitute $\operatorname{Var}(\boldsymbol{\varepsilon}\mid\mathbf{X}) = \sigma^2\mathbf{I}$, which is precisely what makes the cross-terms cancel and leaves only $\sigma^2(\mathbf{X}'\mathbf{X})^{-1} + \sigma^2\mathbf{D}\mathbf{D}'$.

**(d) [2 pts]** **False.** BLUE only crowns OLS *within the unbiased club* — the "U" explicitly bars biased estimators. A biased estimator (e.g., ridge/shrinkage, which you may meet later) can have strictly *lower variance and lower MSE* than OLS by trading a little bias for a lot of variance reduction. Gauss–Markov says nothing about that trade because it refuses to consider biased competitors at all.

---

## Problem 5 — Unbiased vs. consistent: build one of each (18 pts)

**(a) [7 pts]** $\hat{\beta}_1^{(5)}$ = OLS slope on only the first 5 loans.

(i) **Unbiased.** The Problem-2 proof never used the sample size: it used Assumption 1 (the true model holds for those 5 rows too), Assumption 2 (the $2\times2$ $\mathbf{X}_5'\mathbf{X}_5$ is invertible — true given income spread among the 5), and Assumption 3 ($\mathbb{E}[\boldsymbol{\varepsilon}\mid\mathbf{X}] = \mathbf{0}$ holds for any subset of rows). So $\mathbb{E}[\hat{\beta}_1^{(5)}\mid\mathbf{X}] = \beta_1$ — exactly the same three-line argument restricted to 5 observations.

(ii) **Inconsistent.** Its variance is the Problem-3 formula on the 5 retained points:
$$
\operatorname{Var}(\hat{\beta}_1^{(5)}\mid\mathbf{X}) = \frac{\sigma^2}{\sum_{i=1}^{5}(x_i - \bar x_5)^2},
$$
a *fixed positive number* that depends only on those 5 incomes. As $N \to \infty$ the estimator ignores every new loan, so this denominator never grows and the variance **never shrinks toward zero**. Consistency requires the sampling distribution to collapse onto $\beta_1$; this one cannot.

(iii) As $N \to \infty$ its sampling distribution stays **centered at $\beta_1$** (unbiased) but keeps a **fixed, non-zero spread** — it does *not* collapse to a point. Unbiased forever, consistent never.

**(b) [7 pts]** $\check{\beta}_1 = \big(1 + \tfrac{10}{N}\big)\hat{\beta}_1$, with $\hat{\beta}_1$ unbiased and consistent.

(i) Since the multiplier is a constant once $N$ is fixed,
$$
\mathbb{E}[\check{\beta}_1\mid\mathbf{X}] = \Big(1 + \tfrac{10}{N}\Big)\mathbb{E}[\hat{\beta}_1\mid\mathbf{X}] = \Big(1 + \tfrac{10}{N}\Big)\beta_1.
$$
The **bias** is
$$
\operatorname{Bias} = \mathbb{E}[\check{\beta}_1\mid\mathbf{X}] - \beta_1 = \frac{10}{N}\,\beta_1,
$$
nonzero at every finite $N$. At $N = 50$: $\operatorname{Bias} = \tfrac{10}{50}\beta_1 = 0.2\,\beta_1$ — a 20% upward bias.

(ii) **Consistent.** As $N \to \infty$, the multiplier $1 + \tfrac{10}{N} \to 1$ (a deterministic constant converging to 1). Combined with $\hat{\beta}_1 \xrightarrow{p} \beta_1$, the product converges in probability: $\check{\beta}_1 = (1 + \tfrac{10}{N})\hat{\beta}_1 \xrightarrow{p} 1\cdot\beta_1 = \beta_1$ (by Slutsky / the product limit rule). The finite-sample bias melts to zero.

(iii) Multiplier at $N = 50$: $1 + \tfrac{10}{50} = 1.2$ (bias $= 0.2\,\beta_1$). At $N = 100{,}000$: $1 + \tfrac{10}{100{,}000} = 1.0001$ (bias $= 0.0001\,\beta_1$, essentially gone).

**(c) [4 pts]** With $100{,}000$ loans, **pick $\check{\beta}_1$** (biased but consistent). At that $N$ its sampling distribution is centered at $1.0001\,\beta_1$ — indistinguishable from $\beta_1$ — *and* its spread is tiny (it inherits OLS's $\sigma^2(\mathbf{X}'\mathbf{X})^{-1}$ variance, which shrinks as $N$ grows). By contrast $\hat{\beta}_1^{(5)}$ is centered at $\beta_1$ but keeps the *same fat spread* it had at $N = 5$, because it discards all $99{,}995$ extra loans. So $\check{\beta}_1$'s distribution is a sharp spike essentially on the truth, while $\hat{\beta}_1^{(5)}$'s is a wide blob around the truth — the biased-but-consistent estimator wins decisively. This is the chapter's slogan in action: with enough data, consistency (collapsing onto the truth) dominates mere unbiasedness (correct center, but never tightening).

---

## Problem 6 — Diagnose the patient: bias or standard errors? (28 pts)

**(a) [8 pts] — Omitted variable (Devon).**

1. Assumption violated: **Assumption 3, zero conditional mean** ($\mathbb{E}[\boldsymbol{\varepsilon}\mid\mathbf{X}]\neq\mathbf{0}$) — the omitted sentiment lives in the error and is correlated with buzz.
2. **Bias problem** — the master fault; the buzz coefficient is aimed at the wrong target.
3. **More data does NOT fix it** — OLS converges *confidently to the biased number*; more days shrink the SE around the wrong value.
4. **Chapter 2.5** (omitted-variable bias).

*Computation.* Using short-slope $\to \beta_{\text{buzz}} + (\text{effect of sentiment})\times\delta$:
$$
\to 0 + (-0.6)(0.7) = \boxed{-0.42}.
$$
It is **not zero**, even though the true direct buzz effect *is* zero — the coefficient is entirely inherited OVB (its sign here is set by the signs of the sentiment effect and $\delta$). Running on $10\times$ more days does **nothing** to move it away from $-0.42$ (that value is the probability limit), while the **standard error shrinks** — so Devon grows *more confident* in a spurious effect. This is the chapter's "number that should frighten you": more data makes a false answer *more precise*, not more correct.

**(b) [8 pts] — Fan-shaped residuals (Maya).**

1. Assumption violated: **Assumption 4, homoskedasticity** (the equal-variance half: $\operatorname{Var}(\varepsilon_i\mid\mathbf{X})$ depends on income).
2. **Standard-error / efficiency problem** — the point estimate is fine; the reported uncertainty and the BLUE guarantee are compromised.
3. **More data does NOT fix the SE formula** — the classical $\sigma^2(\mathbf{X}'\mathbf{X})^{-1}$ stays wrong at every $N$ (though it does shrink the true sampling variance); you fix it by changing the *formula*, not the sample size.
4. **Chapter 2.4** (robust standard errors).

*Why no bias.* The Problem-2 unbiasedness proof used **only** $\mathbb{E}[\boldsymbol{\varepsilon}\mid\mathbf{X}] = \mathbf{0}$ (Assumption 3) at the step $\mathbb{E}[\hat{\boldsymbol{\beta}}\mid\mathbf{X}] = \boldsymbol{\beta} + (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\,\mathbb{E}[\boldsymbol{\varepsilon}\mid\mathbf{X}]$. The *variance* of $\boldsymbol{\varepsilon}$ never appeared, so heteroskedasticity cannot move the center: $\hat{\beta}_1$ still aims at $\beta_1$. What breaks is the *variance* derivation, which substituted $\operatorname{Var}(\boldsymbol{\varepsilon}\mid\mathbf{X}) = \sigma^2\mathbf{I}$ — false here — so $\sigma^2(\mathbf{X}'\mathbf{X})^{-1}$ is the wrong variance and every t-stat built on it is untrustworthy. The repair is **heteroskedasticity-robust standard errors (HC1/HC2/HC3)** from CONVENTIONS §3 / Ch 2.4.

**(c) [6 pts] — Duplicated column (Sam).**

1. Assumption violated: **Assumption 2, full column rank** (no perfect collinearity).
2. Classification: the **third category** — *mechanical*, not bias-vs-SE. The estimator is **undefined**, not merely biased or imprecise.
3. **More data does NOT fix it** — the dependence is exact and structural; adding rows keeps income-in-dollars $= 1000\times$ income-in-thousands forever.
4. **Chapter 2.3** (collinearity diagnostics; the perfect case is mechanical, near-perfect is multicollinearity).

*Why the inverse fails.* The two income columns are an exact linear relationship ($x_{\text{dollars}} = 1000\,x_{\text{thousands}}$), so $\mathbf{X}$ does not have full column rank. Then $\mathbf{X}'\mathbf{X}$ is **singular** — its determinant is zero — and a singular matrix has no inverse. Since $\hat{\boldsymbol{\beta}} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$ requires that inverse, there is literally no number to compute: "undefined, like dividing by zero." It is not a biased estimate of the truth; it is the *absence* of an estimate (the software either errors or silently drops the redundant column to restore rank). No sample size repairs an exact linear dependence.

**(d) [6 pts] — Clustered loans (Priya).**

1. Assumption violated: **Assumption 4, homoskedasticity** — specifically the **off-diagonal-zeros half** (uncorrelated errors). Within-region claims move together, so $\operatorname{Cov}(\varepsilon_i, \varepsilon_j\mid\mathbf{X}) \neq 0$ for $i,j$ in the same region; the variance matrix is no longer $\sigma^2\mathbf{I}$ but has positive off-diagonal blocks.
2. **Standard-error / efficiency problem** — $\hat{\boldsymbol{\beta}}$ stays unbiased (Assumption 3 is intact); only the uncertainty is mis-stated.
3. **More data does NOT fix it** if the new data arrive in the same clustered structure — you fix it with the right SE formula.
4. **Chapter 2.4** (clustered standard errors).

*Why ordinary SEs are too small.* Positively correlated within-cluster errors mean each region contributes far less *independent* information than its raw observation count suggests — the effective sample size is closer to the number of regions than the number of policies. Ordinary standard errors assume every observation is an independent draw, so they treat the sample as more informative than it is and report a standard error that is **too small** (overstating precision, producing falsely narrow confidence intervals and inflated t-stats). The fix is **clustered standard errors** (clustered by region), per CONVENTIONS §3 / Ch 2.4.

---

*End of solutions for PS 2.2.*
