# Solutions — PS 1.2 (Expectation/Variance Algebra & Correlation Geometry)

**Linked problem set:** `book/weeks/week-01/ps1.2.md` · Week 1, Chapter 1.2.
These solutions use only Ch 1.2 tools: linearity of expectation, the definitions of variance and covariance, scaling/bilinearity/symmetry, the weighted variance formula, correlation $\rho = \sigma_{XY}/(\sigma_X\sigma_Y)$, Cauchy–Schwarz, and the quadratic form $\mathbf{w}'\mathbf{\Sigma}\mathbf{w}$. Notation follows CONVENTIONS §3.

---

## Problem 1 — Linearity warm-up: Devon's three wallets (12 pts)

**(a) [4 pts]** Linearity of expectation passes straight through any weighted sum, with no need to know the joint distribution:
$$
\mathbb{E}[R_p] = 0.5\,\mathbb{E}[R_A] + 0.3\,\mathbb{E}[R_B] + 0.2\,\mathbb{E}[R_C] = 0.5(0.05) + 0.3(-0.02) + 0.2(0.011).
$$
$$
= 0.025 - 0.006 + 0.0022 = \boxed{0.0212} \quad (2.12\% \text{ expected weekly return}).
$$
The property is **linearity of expectation**: $\mathbb{E}[aX+bY+cZ] = a\mathbb{E}[X]+b\mathbb{E}[Y]+c\mathbb{E}[Z]$ holds *whether or not* the variables are related, because expectation is a probability-weighted average and averaging is linear.

**(b) [4 pts]** The friend is wrong for expected return because expectation is a **linear** operator: the cross-terms in the joint distribution are fully accounted for by the joint probabilities and simply drop out, so no covariance information is needed. The friend would be right for variance because variance is built from a **square** — a nonlinear function — and $\operatorname{Var}(aX+bY+\dots)$ carries cross-terms $2ab\operatorname{Cov}(X,Y)$ that genuinely depend on how the assets co-move. Linear operations forgive dependence; nonlinear ones (the square inside variance) do not.

**(c) [4 pts]** With weights $1.5$ on $A$ and $-0.5$ on $B$:
$$
\mathbb{E}[R_p] = 1.5(0.05) + (-0.5)(-0.02) = 0.075 + 0.010 = \boxed{0.085}.
$$
The negative weight causes no trouble: linearity of expectation holds for *any* real constants, positive or negative, so a short position is handled by the same rule. (Negative weights matter only for *variance*, where a $-0.5$ would be squared and would flip signs on a cross-term — but that is a Section-2 issue, not a linearity issue.)

---

## Problem 2 — Covariance algebra from the definitions (16 pts)

**(a) [6 pts]** Let $U = aX + c$ and $V = bY + d$. By linearity, $\mathbb{E}[U] = a\mathbb{E}[X] + c$ and $\mathbb{E}[V] = b\mathbb{E}[Y] + d$. The centered versions are
$$
U - \mathbb{E}[U] = aX + c - (a\mathbb{E}[X] + c) = a\big(X - \mathbb{E}[X]\big), \qquad V - \mathbb{E}[V] = b\big(Y - \mathbb{E}[Y]\big).
$$
Therefore
$$
\operatorname{Cov}(U,V) = \mathbb{E}\big[(U-\mathbb{E}[U])(V-\mathbb{E}[V])\big] = \mathbb{E}\big[ab(X-\mathbb{E}[X])(Y-\mathbb{E}[Y])\big] = ab\,\operatorname{Cov}(X,Y). \quad\blacksquare
$$
The additive constants $c, d$ disappear because covariance is built from **deviations from the mean**, and shifting a variable by a constant shifts its mean by the same constant, leaving every deviation unchanged.

**(b) [6 pts]** Write the variance as a covariance with itself and expand using bilinearity in both slots:
$$
\operatorname{Var}(aX + bY) = \operatorname{Cov}(aX + bY,\ aX + bY).
$$
Expand the first slot:
$$
= a\,\operatorname{Cov}(X,\ aX+bY) + b\,\operatorname{Cov}(Y,\ aX+bY).
$$
Expand the second slot in each term:
$$
= a\big[a\operatorname{Cov}(X,X) + b\operatorname{Cov}(X,Y)\big] + b\big[a\operatorname{Cov}(Y,X) + b\operatorname{Cov}(Y,Y)\big].
$$
Use $\operatorname{Cov}(X,X) = \operatorname{Var}(X)$, $\operatorname{Cov}(Y,Y) = \operatorname{Var}(Y)$, and symmetry $\operatorname{Cov}(X,Y) = \operatorname{Cov}(Y,X)$:
$$
= a^2\operatorname{Var}(X) + ab\operatorname{Cov}(X,Y) + ab\operatorname{Cov}(X,Y) + b^2\operatorname{Var}(Y) = a^2\operatorname{Var}(X) + b^2\operatorname{Var}(Y) + 2ab\operatorname{Cov}(X,Y). \quad\blacksquare
$$

**(c) [4 pts]** The correct formula uses $a = 1$, $b = -1$ in the result of (b):
$$
\operatorname{Var}(X - Y) = \operatorname{Var}(X) + \operatorname{Var}(Y) - 2\operatorname{Cov}(X,Y).
$$
The classmate dropped the $+\operatorname{Var}(Y)$ and the cross-term. **Counterexample:** let $Y = X$, with $\operatorname{Var}(X) = 4$. The classmate's formula gives $\operatorname{Var}(X) - \operatorname{Var}(Y) = 4 - 4 = 0$, but actually $\operatorname{Var}(X - X) = \operatorname{Var}(0) = 0$ — coincidentally correct here. So pick instead $\operatorname{Var}(X) = 1$, $\operatorname{Var}(Y) = 4$: the classmate's version yields $1 - 4 = -3 < 0$, which is impossible since a variance (an expected square) can never be negative. The true formula with, say, $\operatorname{Cov}(X,Y)=0$ gives $1 + 4 - 0 = 5 \ge 0$, as it must.

---

## Problem 3 — Maya's two-asset portfolio and diversification (20 pts)

**(a) [3 pts]** With $R_p = wR_1 + (1-w)R_2$:
$$
\mathbb{E}[R_p] = w(0.09) + (1-w)(0.03) = 0.03 + 0.06\,w,
$$
$$
\operatorname{Var}(R_p) = w^2(0.04) + (1-w)^2(0.0025) + 2w(1-w)\sigma_{12}.
$$
$\mathbb{E}[R_p]$ is **linear** in $w$ (degree 1) because expectation passes through the weighted sum untouched. $\operatorname{Var}(R_p)$ is a **parabola** (degree 2) because variance squares the weights: the $w^2$, $(1-w)^2$, and $w(1-w)$ terms are all quadratic in $w$.

**(b) [6 pts]** At $w = 0.5$: $w^2 = (1-w)^2 = 0.25$ and $2w(1-w) = 0.5$. The fixed part is $0.25(0.04) + 0.25(0.0025) = 0.010 + 0.000625 = 0.010625$. Add $0.5\,\sigma_{12}$:

| $\sigma_{12}$ | $\operatorname{Var}(R_p)$ | $\operatorname{sd}(R_p)$ |
|---|---|---|
| $+0.010$ | $0.010625 + 0.005 = 0.015625$ | $\sqrt{0.015625} = \mathbf{0.125}$ |
| $0$ | $0.010625 + 0 = 0.010625$ | $\sqrt{0.010625} \approx \mathbf{0.103}$ |
| $-0.008$ | $0.010625 - 0.004 = 0.006625$ | $\sqrt{0.006625} \approx \mathbf{0.081}$ |

**(c) [5 pts]** Asset 2's volatility is $0.05$. Comparing:
- $\sigma_{12} = +0.010$: $\operatorname{sd} = 0.125 > 0.05$ — **not** below asset 2. The positive covariance *adds* to the cross-term, so risks reinforce.
- $\sigma_{12} = 0$: $\operatorname{sd} \approx 0.103 > 0.05$ — **not** below asset 2. The cross-term vanishes, but asset 1's large $0.04$ variance still dominates the blend.
- $\sigma_{12} = -0.008$: $\operatorname{sd} \approx 0.081 > 0.05$ — still **not** below asset 2. The negative covariance *subtracts* from the cross-term and cuts risk substantially, but not enough to beat asset 2 at this even split.

So at $w = 0.5$ none of the three blends beats asset 2 alone: with such a low-variance asset 2 ($0.0025$) and an equal 50% stake in the volatile asset 1, the even split is simply too heavy in the risky asset. (Problem 6 shows the *right* weight gets very close to asset 2's volatility.) The sign of the covariance shifts the cross-term up ($+$), to zero ($0$), or down ($-$), exactly tracking how much risk reinforces versus cancels.

**(d) [6 pts]** Total portfolio (book-level) risk is governed by the sum of variances *plus* the cross-terms $2w_jw_k\sigma_{jk}$ across every pair of loans. When defaults move **together**, every pairwise covariance $\sigma_{jk}$ is positive, so the cross-term $2w(1-w)\sigma_{12}$ (and all its analogues across 100 loans) *adds* to the total — risk compounds, because a regional recession knocks down many loans at once. When defaults move **independently**, every $\sigma_{jk} = 0$, the cross-terms vanish, and the variances merely add; spreading the same dollar exposure over 100 independent loans drives the aggregate volatility down sharply (the independent losses partly cancel). Even though each individual loan has identical default variance, it is the covariance term — not the individual variances — that decides whether the book is dangerously concentrated or safely diversified.

---

## Problem 4 — Correlation is a cosine; prove $|\rho| \le 1$ (22 pts)

**(a) [10 pts]** Fix any real $t$. Because $\operatorname{Var}(X - tY) = \mathbb{E}[(\tilde X - t\tilde Y)^2]$ is the expectation of a square, it is $\ge 0$. Expand using bilinearity (Problem 2b style), writing $\sigma_X^2 = \operatorname{Var}(X)$, $\sigma_Y^2 = \operatorname{Var}(Y)$, $\sigma_{XY} = \operatorname{Cov}(X,Y)$:
$$
0 \le \operatorname{Var}(X - tY) = \sigma_X^2 - 2t\,\sigma_{XY} + t^2 \sigma_Y^2 \equiv q(t).
$$
This is an upward-opening parabola in $t$ (coefficient $\sigma_Y^2 \ge 0$) that is never negative. A quadratic $q(t) = \sigma_Y^2 t^2 - 2\sigma_{XY} t + \sigma_X^2$ that stays $\ge 0$ for all $t$ must have a non-positive discriminant:
$$
\Delta = (-2\sigma_{XY})^2 - 4\,\sigma_Y^2\,\sigma_X^2 \le 0 \;\Longrightarrow\; 4\sigma_{XY}^2 \le 4\sigma_X^2\sigma_Y^2 \;\Longrightarrow\; \boxed{\operatorname{Cov}(X,Y)^2 \le \operatorname{Var}(X)\operatorname{Var}(Y)}. \quad\blacksquare
$$
(If $\sigma_Y^2 = 0$ then $Y$ is constant, $\sigma_{XY} = 0$, and the inequality holds trivially as $0 \le 0$.)

**Equality condition.** $\Delta = 0$ exactly when the parabola touches zero at some $t = t^\star$, i.e. $\operatorname{Var}(X - t^\star Y) = 0$. A variable with zero variance is constant, so $X - t^\star Y = \text{const}$: **$X$ is an exact linear function of $Y$.** Geometrically the two centered variables are **parallel vectors** (angle $0^\circ$ or $180^\circ$), so $|\rho| = 1$.

**(b) [4 pts]** Divide the Cauchy–Schwarz inequality by $\sigma_X^2\sigma_Y^2 > 0$ (assuming both nonzero):
$$
\frac{\sigma_{XY}^2}{\sigma_X^2\sigma_Y^2} \le 1 \;\Longrightarrow\; \rho_{XY}^2 = \left(\frac{\sigma_{XY}}{\sigma_X\sigma_Y}\right)^2 \le 1 \;\Longrightarrow\; -1 \le \rho_{XY} \le 1. \quad\blacksquare
$$
The discriminant step $\sigma_{XY}^2 \le \sigma_X^2\sigma_Y^2$ — equivalently $|\sigma_{XY}| \le \sigma_X\sigma_Y$ — is the random-variable translation of $|\langle \mathbf{u},\mathbf{v}\rangle| \le \|\mathbf{u}\|\,\|\mathbf{v}\|$, which is exactly $|\cos\theta| \le 1$.

**(c) [4 pts]** Max possible covariance magnitude is $\sigma_X\sigma_Y = (0.15)(0.04) = 0.006$. The reported value is
$$
\rho = \frac{0.006}{(0.15)(0.04)} = \frac{0.006}{0.006} = 1.0, \qquad \theta = \arccos(1.0) = 0^\circ.
$$
A covariance of $0.006$ sits at the **very edge** of Cauchy–Schwarz: $\rho = 1$ means the two signals are perfectly, positively, *linearly* related — geometrically parallel ($\theta = 0^\circ$). Any reported covariance with magnitude *above* $0.006$ would violate $|\sigma_{XY}| \le \sigma_X\sigma_Y$ and is therefore impossible: for example, the vendor could **not** legitimately report $\operatorname{Cov}(X,Y) = 0.008$ (that would imply $\rho = 0.008/0.006 \approx 1.33 > 1$). A plausible interior report would be something like $0.003$ (giving $\rho = 0.5$, $\theta = 60^\circ$).

**(d) [4 pts]** With $Z = X^2$ and $X$ symmetric about $0$, use the second form of covariance:
$$
\operatorname{Cov}(X, Z) = \mathbb{E}[XZ] - \mathbb{E}[X]\mathbb{E}[Z] = \mathbb{E}[X \cdot X^2] - \mathbb{E}[X]\mathbb{E}[X^2] = \mathbb{E}[X^3] - 0 \cdot \mathbb{E}[X^2] = 0 - 0 = 0,
$$
since symmetry gives $\mathbb{E}[X]=0$ and $\mathbb{E}[X^3]=0$ (every odd moment of a symmetric-about-zero distribution vanishes). Hence $\rho_{XZ} = 0/(\sigma_X\sigma_Z) = 0$: the two are **uncorrelated**, even though $Z = X^2$ is a perfect deterministic function of $X$ (knowing $X$ pins down $Z$ exactly). The geometric reason: correlation is a **cosine**, and a cosine measures only the *linear* (straight-line) alignment between two centered variables; it is completely **blind to curved relationships** like the parabola $Z = X^2$, where above-mean $X$ and below-mean $X$ both push $Z$ up and the positive and negative cross-products cancel. This is exactly the limitation linear regression inherits in Week 2.

---

## Problem 5 — A covariance matrix: symmetry, PSD, and the quadratic form (18 pts)

$$
\mathbf{\Sigma} = \begin{pmatrix} 0.04 & 0.01 & 0.000 \\ 0.01 & 0.09 & -0.018 \\ 0.000 & -0.018 & 0.01 \end{pmatrix}.
$$

**(a) [3 pts]** Every legitimate covariance matrix must be **(i) symmetric** ($\Sigma_{jk} = \Sigma_{kj}$, because $\operatorname{Cov}(R_j,R_k) = \operatorname{Cov}(R_k,R_j)$) and **(ii) positive semidefinite** ($\mathbf{w}'\mathbf{\Sigma}\mathbf{w} \ge 0$ for all $\mathbf{w}$, because that quadratic form is a variance). Symmetry holds by inspection: the $(1,2)$ and $(2,1)$ entries are both $0.01$, $(1,3)=(3,1)=0$, $(2,3)=(3,2)=-0.018$. The diagonal gives the variances and their standard deviations:
$$
\operatorname{Var}(R_1)=0.04 \Rightarrow \sigma_1 = 0.20, \quad \operatorname{Var}(R_2)=0.09 \Rightarrow \sigma_2 = 0.30, \quad \operatorname{Var}(R_3)=0.01 \Rightarrow \sigma_3 = 0.10.
$$

**(b) [5 pts]** Using $\rho_{jk} = \Sigma_{jk}/(\sigma_j\sigma_k)$:
$$
\rho_{12} = \frac{0.01}{(0.20)(0.30)} = \frac{0.01}{0.06} \approx \mathbf{0.167}, \quad \rho_{13} = \frac{0.000}{(0.20)(0.10)} = \mathbf{0}, \quad \rho_{23} = \frac{-0.018}{(0.30)(0.10)} = \frac{-0.018}{0.03} = \mathbf{-0.6}.
$$
All satisfy $|\rho| \le 1$ (Cauchy–Schwarz holds on each pair). Lines **2 and 3** diversify best: their correlation $-0.6$ is the most negative, so their cross-term *subtracts* the most from portfolio variance — negatively related lines partly cancel each other's risk. (Lines 1 and 3, at $\rho=0$, only avoid adding risk; lines 2 and 3 actively cancel it.)

**(c) [6 pts]** With $\mathbf{w} = (1/3,1/3,1/3)'$, each $w_jw_k = 1/9$, so $\mathbf{w}'\mathbf{\Sigma}\mathbf{w} = \tfrac{1}{9}\sum_j\sum_k \Sigma_{jk}$ = $\tfrac19$ times the sum of *all nine* entries.

*Diagonal* (variances): $0.04 + 0.09 + 0.01 = 0.14$.
*Off-diagonal* (each covariance appears twice): $2(0.01) + 2(0.000) + 2(-0.018) = 0.02 + 0 - 0.036 = -0.016$.
Sum of all entries $= 0.14 - 0.016 = 0.124$. Then
$$
\mathbf{w}'\mathbf{\Sigma}\mathbf{w} = \frac{0.124}{9} \approx \mathbf{0.01378}, \qquad \operatorname{sd}(R_p) = \sqrt{0.01378} \approx \mathbf{0.1174}.
$$
(Note this is below the average diagonal volatility, thanks to the negative $\rho_{23}$ pulling the off-diagonal sum down.)

**(d) [4 pts]** If line 4 is *exactly* $R_4 = R_1 + R_2$, then $R_4$ is a deterministic linear combination of existing lines: it carries no new randomness. In the $4\times 4$ covariance matrix the fourth row/column is the corresponding linear combination of rows/columns 1 and 2, so the **columns are linearly dependent** — the matrix is **singular** (determinant $0$, no inverse). It remains positive *semi*definite (variances are still $\ge 0$) but not positive *definite*, because there exists a nonzero weight vector giving zero variance. That vector is
$$
\mathbf{w} = (-1,\ -1,\ 0,\ 1)', \quad\text{since}\quad \mathbf{w}'\mathbf{R} = -R_1 - R_2 + R_4 = R_4 - (R_1+R_2) = 0 \;\Rightarrow\; \mathbf{w}'\mathbf{\Sigma}\mathbf{w} = \operatorname{Var}(0) = 0.
$$
This is the same wall met from the other side in Week 2: when regressors are perfectly collinear, $\mathbf{X}'\mathbf{X}$ (a covariance-matrix cousin) is singular, so $(\mathbf{X}'\mathbf{X})^{-1}$ in $\hat{\boldsymbol\beta} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$ does not exist and OLS cannot separate the collinear effects.

---

## Problem 6 — Deriving the minimum-variance weight (16 pts)

**(a) [7 pts]** Let $f(w) = w^2\sigma_1^2 + (1-w)^2\sigma_2^2 + 2w(1-w)\sigma_{12}$. Differentiate term by term (chain rule on the middle term, product rule on the last):
$$
f'(w) = 2w\sigma_1^2 - 2(1-w)\sigma_2^2 + 2\sigma_{12}\big[(1-w) - w\big] = 2w\sigma_1^2 - 2(1-w)\sigma_2^2 + 2\sigma_{12}(1 - 2w).
$$
Set $f'(w) = 0$ and divide by 2:
$$
w\sigma_1^2 - (1-w)\sigma_2^2 + \sigma_{12}(1 - 2w) = 0.
$$
Collect the $w$ terms on one side:
$$
w\sigma_1^2 + w\sigma_2^2 - 2w\sigma_{12} = \sigma_2^2 - \sigma_{12} \;\Longrightarrow\; w\big(\sigma_1^2 + \sigma_2^2 - 2\sigma_{12}\big) = \sigma_2^2 - \sigma_{12},
$$
$$
\boxed{w^\star = \frac{\sigma_2^2 - \sigma_{12}}{\sigma_1^2 + \sigma_2^2 - 2\sigma_{12}}}.
$$
**Second-derivative check:** $f''(w) = 2\sigma_1^2 + 2\sigma_2^2 - 4\sigma_{12} = 2(\sigma_1^2 + \sigma_2^2 - 2\sigma_{12})$. Since $\sigma_1^2 + \sigma_2^2 - 2\sigma_{12} = \operatorname{Var}(R_1 - R_2) \ge 0$ (it is a variance!), $f''(w) \ge 0$, confirming a **minimum**. (Strictly positive unless the two assets are perfectly correlated, $\rho=1$.)

**(b) [5 pts]** With $\sigma_1^2 = 0.04$, $\sigma_2^2 = 0.0025$, $\sigma_{12} = 0$:
$$
w^\star = \frac{0.0025 - 0}{0.04 + 0.0025 - 0} = \frac{0.0025}{0.0425} \approx \mathbf{0.0588}.
$$
So Maya holds about 5.88% in the volatile asset 1 and 94.12% in asset 2. Plug back in (cross-term is zero):
$$
\operatorname{Var}(R_p) = (0.0588)^2(0.04) + (0.9412)^2(0.0025) \approx 0.0001384 + 0.0022145 = \mathbf{0.002353},
$$
$$
\operatorname{sd}(R_p) = \sqrt{0.002353} \approx \mathbf{0.0485}, \qquad \mathbb{E}[R_p] = 0.0588(0.09) + 0.9412(0.03) \approx \mathbf{0.0335}.
$$
This volatility, $0.0485$, is far below the even-split (uncorrelated) volatility $\approx 0.103$ from Problem 3(b) — and even dips slightly below asset 2's own $0.05$, the diversification payoff Problem 3(c) could not reach at $w=0.5$.

**(c) [4 pts]** **(i)** If $\sigma_{12} = \sigma_1\sigma_2$ (perfect positive correlation, $\rho = 1$), then
$$
w^\star = \frac{\sigma_2^2 - \sigma_1\sigma_2}{\sigma_1^2 + \sigma_2^2 - 2\sigma_1\sigma_2} = \frac{\sigma_2(\sigma_2 - \sigma_1)}{(\sigma_1 - \sigma_2)^2} = \frac{-\sigma_2(\sigma_1 - \sigma_2)}{(\sigma_1 - \sigma_2)^2} = \frac{-\sigma_2}{\sigma_1 - \sigma_2} = \frac{\sigma_2}{\sigma_2 - \sigma_1}.
$$
Economically this makes sense: when two assets are perfectly correlated, no diversification is possible by simply averaging — the minimum-variance "portfolio" goes to an extreme (here a leveraged long/short combination $\sigma_2/(\sigma_2-\sigma_1)$, which can be negative or above 1) that *exactly cancels* the common risk, since perfectly correlated returns differ only by a deterministic scaling and can be hedged to zero variance.

**(ii)** OLS minimizes the sum of squared residuals, which — like portfolio variance — is a **quadratic** (a parabola/paraboloid) in the coefficients; differentiating that quadratic and setting the derivative to zero locates its genuine bottom, exactly as setting $f'(w)=0$ located the minimum-variance weight here.

---

*End of solutions for PS 1.2.*
