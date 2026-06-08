# PS 2.1 — Matrix-OLS Derivations & Numerical Inversion

**Course:** 8-Week Empirical Finance Camp · Week 2 · Problem Set 2.1
**Covers:** Ch 2.1 (OLS in Matrix Form).
**Methods allowed:** only what is built through Ch 2.1 — the stacked model $\mathbf{y} = \mathbf{X}\boldsymbol\beta + \boldsymbol\varepsilon$, the least-squares objective $\text{SSR}(\mathbf{b}) = (\mathbf{y}-\mathbf{X}\mathbf{b})'(\mathbf{y}-\mathbf{X}\mathbf{b})$, the normal equations $\mathbf{X}'\mathbf{X}\hat{\boldsymbol\beta}=\mathbf{X}'\mathbf{y}$, the estimator $\hat{\boldsymbol\beta}=(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$, the hat matrix $\mathbf{H}=\mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'$, the residual maker $\mathbf{M}=\mathbf{I}-\mathbf{H}$, orthogonality of residuals to regressors, the Pythagorean split, and the full-column-rank condition for invertibility. You do **not** need any statistical assumption about where the data came from — no unbiasedness, no variance of $\hat{\boldsymbol\beta}$, no Gauss–Markov (that is Ch 2.2). This whole sheet is *algebra and geometry of the fit*, nothing more.

**Total: 100 points.** Point values are stated per problem. Show your reasoning — a correct final number with no derivation earns roughly half credit, because the reasoning *is* the skill we are grading. Solutions are in Appendix E (`E-w2-ps2.1-solutions.md`); try every part before you look.

A note on the difficulty curve: Problem 1 is a five-minute warm-up. Problems 2 and 3 are the core mechanical drills you must be able to do in your sleep before Ch 2.2. Problems 5 and 6 are the genuinely hard ones — Problem 6 in particular is where the intuition that will matter for standard errors gets built. Budget your time accordingly. Throughout, $N$ is the number of observations and $K$ the number of regressors *including the intercept*, exactly as in the chapter.

---

## Problem 1 — Derive the normal equations from scratch (14 points)

This is the chapter's central derivation, done in your own hand so the moving parts stick. Let $\mathbf{y}$ be $N\times 1$, $\mathbf{X}$ be $N\times K$ with full column rank, and $\mathbf{b}$ a $K\times 1$ vector of candidate coefficients. Define the sum of squared residuals
$$
\text{SSR}(\mathbf{b}) = (\mathbf{y} - \mathbf{X}\mathbf{b})'(\mathbf{y} - \mathbf{X}\mathbf{b}).
$$

**(a) (4 pts)** Multiply out the product and use the transpose rule $(\mathbf{A}\mathbf{B})' = \mathbf{B}'\mathbf{A}'$ to show that
$$
\text{SSR}(\mathbf{b}) = \mathbf{y}'\mathbf{y} - 2\,\mathbf{b}'\mathbf{X}'\mathbf{y} + \mathbf{b}'\mathbf{X}'\mathbf{X}\mathbf{b}.
$$
In one sentence, justify the step that merged the two cross-terms into a single $-2\,\mathbf{b}'\mathbf{X}'\mathbf{y}$. (Hint: each cross-term is a $1\times 1$ matrix, and a scalar equals its own transpose.)

**(b) (4 pts)** Using the two matrix-calculus facts $\frac{\partial}{\partial\mathbf{b}}(\mathbf{a}'\mathbf{b}) = \mathbf{a}$ and $\frac{\partial}{\partial\mathbf{b}}(\mathbf{b}'\mathbf{A}\mathbf{b}) = 2\mathbf{A}\mathbf{b}$ (for symmetric $\mathbf{A}$), take the gradient $\partial\,\text{SSR}/\partial\mathbf{b}$, set it to the zero vector, and derive the normal equations $\mathbf{X}'\mathbf{X}\hat{\boldsymbol\beta} = \mathbf{X}'\mathbf{y}$. State explicitly where you used the symmetry of $\mathbf{X}'\mathbf{X}$.

**(c) (4 pts)** A flat point of a function is not automatically a minimum. The Hessian (matrix of second derivatives) of SSR is $2\mathbf{X}'\mathbf{X}$. Show that for *any* vector $\mathbf{v}$, $\mathbf{v}'(\mathbf{X}'\mathbf{X})\mathbf{v} \ge 0$, and explain in one sentence why this guarantees the flat point you found in (b) is a minimum rather than a maximum or a saddle.

**(d) (2 pts)** The equations are called "normal" — an old word for *perpendicular*. Without doing the calculus again, state the one-sentence geometric demand (from §4 of the chapter) that produces the identical equations. Which fact about last week's notion of "uncorrelated" is this the same as?

---

## Problem 2 — A property of the residual maker $\mathbf{M}$ (16 points)

The residual maker $\mathbf{M} = \mathbf{I} - \mathbf{H}$, with $\mathbf{H} = \mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'$, is the operator that turns outcomes into residuals: $\hat{\mathbf{e}} = \mathbf{M}\mathbf{y}$. Prove its defining properties from scratch. You may use that $\mathbf{H}$ is symmetric and idempotent (you do **not** need to re-derive those).

**(a) (4 pts)** Prove $\mathbf{M}$ is symmetric: $\mathbf{M}' = \mathbf{M}$.

**(b) (5 pts)** Prove $\mathbf{M}$ is idempotent: $\mathbf{M}\mathbf{M} = \mathbf{M}$. Then state in one sentence what "applying $\mathbf{M}$ twice equals applying it once" means geometrically.

**(c) (4 pts)** Prove the annihilator identity $\mathbf{M}\mathbf{X} = \mathbf{0}$ (an $N\times K$ matrix of zeros). Explain in one sentence why this is just the matrix form of "the residuals are orthogonal to every regressor."

**(d) (3 pts)** Use part (c) to show in two lines that the residual vector $\hat{\mathbf{e}} = \mathbf{M}\mathbf{y}$ is unchanged if you instead apply $\mathbf{M}$ to the *errors* $\boldsymbol\varepsilon$ rather than to $\mathbf{y}$ — that is, $\mathbf{M}\mathbf{y} = \mathbf{M}\boldsymbol\varepsilon$. (Start from the true model $\mathbf{y} = \mathbf{X}\boldsymbol\beta + \boldsymbol\varepsilon$. This little identity is the engine of every variance calculation you will do next chapter, so it is worth seeing now.)

---

## Problem 3 — OLS by hand with a non-diagonal $\mathbf{X}'\mathbf{X}$ (20 points)

Maya is studying how gig-economy work hours relate to missed student-loan payments. For four classmates she records $x_i$ = average gig hours worked per week (in tens of hours) and $y_i$ = a stress index she built from missed-payment counts:

| Student $i$ | Gig hours $x_i$ | Stress index $y_i$ |
|---|---|---|
| 1 | $1$ | $1$ |
| 2 | $2$ | $3$ |
| 3 | $3$ | $4$ |
| 4 | $4$ | $6$ |

She fits $y_i = \beta_0 + \beta_1 x_i + \varepsilon_i$ by OLS. Unlike Sam's chapter example, the market column here does **not** sum to zero, so $\mathbf{X}'\mathbf{X}$ will *not* be diagonal — you will have to invert a genuine $2\times 2$ matrix. Keep everything in exact fractions until the last step.

**(a) (4 pts)** Write the design matrix $\mathbf{X}$ and outcome vector $\mathbf{y}$, then compute $\mathbf{X}'\mathbf{X}$ and $\mathbf{X}'\mathbf{y}$.

**(b) (5 pts)** Invert $\mathbf{X}'\mathbf{X}$ using the $2\times 2$ rule $\begin{pmatrix} a & b \\ c & d\end{pmatrix}^{-1} = \frac{1}{ad-bc}\begin{pmatrix} d & -b \\ -c & a\end{pmatrix}$. Report the determinant $\det(\mathbf{X}'\mathbf{X})$ as well — you will reuse it in Problem 6.

**(c) (4 pts)** Compute $\hat{\boldsymbol\beta} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$. Interpret $\hat\beta_1$ in one sentence in Maya's units (remember $x$ is in *tens* of hours).

**(d) (4 pts)** Compute the four fitted values $\hat y_i$ and the four residuals $\hat e_i$. Verify the two normal-equation identities directly: $\sum_i \hat e_i = 0$ and $\sum_i x_i \hat e_i = 0$.

**(e) (3 pts)** Maya's friend claims the intercept $\hat\beta_0 = -0.5$ is "obviously wrong because a stress index can't be negative." In one or two sentences, explain why a negative *intercept* is not a contradiction here, distinguishing what the intercept means from what the fitted values are.

---

## Problem 4 — Leverage and the diagonal of $\mathbf{H}$ (16 points)

Devon pulls five daily returns for an altcoin and regresses them on the market return $x_i$ (in percent). The five market returns are
$$
\mathbf{x} = (-2,\ -1,\ 0,\ 1,\ 2)',
$$
with an intercept, so $\mathbf{X}$ is $5\times 2$. The $i$-th diagonal entry of the hat matrix, $h_{ii} = \mathbf{x}_i'(\mathbf{X}'\mathbf{X})^{-1}\mathbf{x}_i$ where $\mathbf{x}_i'$ is the $i$-th row of $\mathbf{X}$, is called the **leverage** of observation $i$: it measures how much that point's own outcome pulls its own fitted value.

**(a) (3 pts)** Compute $\mathbf{X}'\mathbf{X}$ and its inverse. (The market returns sum to zero, so this is diagonal — use that.)

**(b) (6 pts)** For a simple regression with an intercept, leverage has the clean closed form
$$
h_{ii} = \frac{1}{N} + \frac{(x_i - \bar x)^2}{\sum_{k=1}^{N}(x_k - \bar x)^2}.
$$
Derive this from $h_{ii} = \mathbf{x}_i'(\mathbf{X}'\mathbf{X})^{-1}\mathbf{x}_i$ for the case $\bar x = 0$ (which holds here), then evaluate it for all five days. Report each $h_{ii}$ as an exact fraction.

**(c) (3 pts)** Verify that $\sum_{i=1}^{5} h_{ii} = K = 2$. (This "leverages sum to the number of regressors" identity is exact for any design with full column rank; here just confirm it numerically.)

**(d) (4 pts)** Which day(s) have the highest leverage, and which the lowest? Explain in two or three sentences what drives leverage — and why a point with leverage near its maximum possible value of $1$ would be one an analyst should look at hard before trusting the fit. (You do not need the formula for the maximum; reason from the structure of $h_{ii}$.)

---

## Problem 5 — Orthogonality and the Pythagorean SSR split (16 points)

Stay with Maya's data and fitted values from Problem 3 (so $\hat{\boldsymbol\beta} = (-1/2,\ 8/5)$, and you have $\hat{\mathbf{y}}$ and $\hat{\mathbf{e}}$ already). This problem makes the geometry of §5 concrete and proves the decomposition that every $R^2$ rests on.

**(a) (4 pts)** Verify numerically that the fitted-value vector and the residual vector are orthogonal: $\hat{\mathbf{y}}'\hat{\mathbf{e}} = 0$. Then prove it *in general* (for any full-rank $\mathbf{X}$, with an intercept) in two or three lines, using only $\hat{\mathbf{y}} = \mathbf{X}\hat{\boldsymbol\beta}$ and the normal-equation fact $\mathbf{X}'\hat{\mathbf{e}} = \mathbf{0}$.

**(b) (4 pts)** Because the regression includes an intercept, the residuals sum to zero, which lets you center everything on $\bar y$. Define the three sums of squares
$$
\text{TSS} = \sum_i (y_i - \bar y)^2, \quad \text{ESS} = \sum_i (\hat y_i - \bar y)^2, \quad \text{RSS} = \sum_i \hat e_i^2 .
$$
Compute all three for Maya's data (use $\bar y = 7/2$).

**(c) (4 pts)** Confirm the Pythagorean identity $\text{TSS} = \text{ESS} + \text{RSS}$ for your numbers. Then give the two-line *reason* it must hold: write $y_i - \bar y = (\hat y_i - \bar y) + \hat e_i$, square and sum, and explain which orthogonality fact kills the cross-term. (Hint: you need both $\sum_i \hat e_i = 0$ and $\sum_i \hat y_i \hat e_i = 0$, both of which you have established.)

**(d) (4 pts)** Compute $R^2 = \text{ESS}/\text{TSS}$. In one sentence, state what it means here — and in a second sentence, explain why nothing you have done in this problem required any assumption about randomness, unbiasedness, or the "true" model (it is pure geometry of the fit).

---

## Problem 6 — Collinearity, the inverse, and the condition number (18 points)

This is the hard one, and the most important for what comes later. Priya wants to predict an insurer's catastrophe losses from two climate indices. Her two regressors are highly redundant: index B is almost a rescaled copy of index A. After standardizing both regressors to have unit length and dropping the intercept for simplicity, her cross-product matrix takes the clean form
$$
\mathbf{X}'\mathbf{X} = \begin{pmatrix} 1 & c \\ c & 1 \end{pmatrix},
\qquad 0 \le c < 1,
$$
where $c$ is the sample correlation between the two standardized indices. The closer the indices, the closer $c$ is to $1$.

**(a) (4 pts)** Compute $(\mathbf{X}'\mathbf{X})^{-1}$ as a function of $c$, and write down $\det(\mathbf{X}'\mathbf{X})$. What happens to every entry of the inverse as $c \to 1^-$? Connect this in one sentence to the chapter's statement that the estimator "is not pinned down" under perfect collinearity.

**(b) (4 pts)** The eigenvalues of $\begin{pmatrix} 1 & c \\ c & 1\end{pmatrix}$ are $\lambda_{\max} = 1+c$ and $\lambda_{\min} = 1-c$. (You may verify this by checking that $(1,1)'$ and $(1,-1)'$ are eigenvectors.) The **condition number** of a symmetric positive-definite matrix is $\kappa = \lambda_{\max}/\lambda_{\min}$; it measures how close the matrix is to singular. Compute $\kappa$ as a function of $c$, and evaluate it at $c = 0$, $c = 0.9$, and $c = 0.98$.

**(c) (6 pts)** A large condition number means the solution of $\mathbf{X}'\mathbf{X}\,\hat{\boldsymbol\beta} = \mathbf{X}'\mathbf{y}$ is *hypersensitive* to small wiggles in the right-hand side. Take $c = 0.98$. Solve the system for the two right-hand sides
$$
\mathbf{X}'\mathbf{y} = \begin{pmatrix} 1 \\ 1 \end{pmatrix}
\qquad\text{and}\qquad
\mathbf{X}'\mathbf{y} = \begin{pmatrix} 1 \\ 1.02 \end{pmatrix},
$$
i.e. a $2\%$ nudge in the second entry. Report both solution vectors $\hat{\boldsymbol\beta}$, and compute the relative change in the solution. Comment in one or two sentences on how the size of that change compares to the size of the nudge, and how it relates to $\kappa$ from part (b).

**(d) (4 pts)** Now suppose index B were *exactly* twice index A, so the raw design has a second column equal to $2\times$ the first. Show that there is a nonzero vector $\mathbf{v}$ with $\mathbf{X}\mathbf{v} = \mathbf{0}$, and explain in two sentences why this makes $\mathbf{X}'\mathbf{X}$ singular and the OLS estimator non-existent — not merely imprecise. Tie this back to the same singular-matrix wall Priya's covariance matrix hit in Ch 1.2.

---

*End of PS 2.1. When you have attempted everything, check yourself against `book/appendices/E-solutions-manual/E-w2-ps2.1-solutions.md`. The numerical parts can all be confirmed in a few lines of NumPy — `np.linalg.inv`, `np.linalg.solve`, and `np.linalg.eigvalsh` — and you are encouraged to do so after working them by hand.*
