# PS 1.2 — Expectation/Variance Algebra & Correlation Geometry

**Course:** ASSIP 2026 · 8-Week Empirical Finance Track · Week 1 · Problem Set 1.2
**Covers:** Ch 1.2 (expectation linearity, variance/covariance algebra, two-asset portfolio variance, correlation as cosine / Cauchy–Schwarz, the covariance matrix $\mathbf{\Sigma}$ and its quadratic form, minimum-variance weights).
**Total:** 104 points across 6 problems. Each problem is self-contained.

**Ground rules.** Use only tools through Chapter 1.2: linearity of expectation, the definitions of variance and covariance, scaling, bilinearity, symmetry, $\operatorname{Var}(aX+bY) = a^2\operatorname{Var}(X) + b^2\operatorname{Var}(Y) + 2ab\operatorname{Cov}(X,Y)$, correlation $\rho = \sigma_{XY}/(\sigma_X\sigma_Y)$, Cauchy–Schwarz, and the quadratic form $\mathbf{w}'\mathbf{\Sigma}\mathbf{w}$. No regression, no calculus of several variables beyond one-variable differentiation, no distributional assumptions you are not handed. Show every step; a correct number with no reasoning earns little. Work in fractions/decimals (a return of $0.06$ means $+6\%$), not percent signs, to keep the algebra clean.

---

## Problem 1 — Linearity warm-up: Devon's three wallets (12 points)

Devon tracks three on-chain assets over one week. His research desk hands him the expected weekly returns $\mathbb{E}[R_A] = 0.05$, $\mathbb{E}[R_B] = -0.02$, $\mathbb{E}[R_C] = 0.011$. He is not told *anything* about how the three assets move together — no covariances, no independence, nothing.

**(a) [4 pts]** Devon builds a portfolio with weights $0.5$ on $A$, $0.3$ on $B$, and $0.2$ on $C$. Compute the expected portfolio return $\mathbb{E}[R_p]$ where $R_p = 0.5\,R_A + 0.3\,R_B + 0.2\,R_C$. State explicitly which property of expectation lets you answer this with no information about the joint distribution.

**(b) [4 pts]** A friend insists, "You can't compute that — you don't know if the assets are correlated." In two or three sentences, explain precisely why the friend is wrong for the *expected return* but would be right if the question had instead asked for the portfolio's *variance*. Tie your answer to the difference between a linear operation and a nonlinear one.

**(c) [4 pts]** Devon now considers a leveraged position: he borrows so that his weights become $1.5$ on $A$ and $-0.5$ on $B$ (a short position in $B$), with nothing in $C$. The weights still sum to $1$. Compute $\mathbb{E}[R_p]$ for this position. Does the negative weight cause any trouble for linearity? Explain in one sentence.

---

## Problem 2 — Covariance algebra from the definitions (16 points)

Let $X$ and $Y$ be any two random variables with finite variance, and let $a, b, c, d$ be constants.

**(a) [6 pts]** Prove the bilinearity-plus-shift identity
$$
\operatorname{Cov}(aX + c,\ bY + d) = ab\,\operatorname{Cov}(X, Y).
$$
Start from the definition $\operatorname{Cov}(U,V) = \mathbb{E}[(U - \mathbb{E}[U])(V - \mathbb{E}[V])]$ and use linearity of expectation. Explain in one sentence *why* the additive constants $c$ and $d$ disappear.

**(b) [6 pts]** Using only the result of part (a), the symmetry of covariance, and $\operatorname{Cov}(Z,Z) = \operatorname{Var}(Z)$, derive the general weighted formula
$$
\operatorname{Var}(aX + bY) = a^2\operatorname{Var}(X) + b^2\operatorname{Var}(Y) + 2ab\,\operatorname{Cov}(X,Y).
$$
(Hint: write $\operatorname{Var}(aX+bY) = \operatorname{Cov}(aX+bY,\ aX+bY)$ and expand using bilinearity in *both* slots.)

**(c) [4 pts]** A classmate claims that because variance "is just a kind of average," $\operatorname{Var}(X - Y) = \operatorname{Var}(X) - \operatorname{Var}(Y)$. Give the correct formula for $\operatorname{Var}(X - Y)$, then construct a one-line numerical counterexample showing the classmate's version can even produce a *negative* "variance," which is impossible. (Use any small numbers you like.)

---

## Problem 3 — Maya's two-asset portfolio and diversification (20 points)

Maya, who studies household finance and fair lending, is splitting \$1 between two assets. As stipulated population quantities (she will learn to estimate these in Ch 1.3) — note these are a *new* pair of assets, with different numbers from the chapter's worked example, so re-derive rather than quoting Ch 1.2's results:

| Quantity | Asset 1 | Asset 2 |
|---|---|---|
| $\mathbb{E}[R]$ | $0.09$ | $0.03$ |
| $\operatorname{Var}(R)$ | $0.0400$ | $0.0025$ |
| $\operatorname{sd}(R)$ | $0.20$ | $0.05$ |

She holds weight $w$ in asset 1 and $1-w$ in asset 2. Let $\sigma_{12} = \operatorname{Cov}(R_1, R_2)$.

**(a) [3 pts]** Write $\mathbb{E}[R_p]$ and $\operatorname{Var}(R_p)$ as functions of $w$ and $\sigma_{12}$. Why is $\mathbb{E}[R_p]$ a straight line in $w$ but $\operatorname{Var}(R_p)$ a parabola?

**(b) [6 pts]** Fix the even split $w = 0.5$. Compute $\operatorname{sd}(R_p)$ for three cases: $\sigma_{12} = +0.010$ (positively related), $\sigma_{12} = 0$ (uncorrelated), and $\sigma_{12} = -0.008$ (oppositely related). Report all three volatilities to three decimals.

**(c) [5 pts]** In which of the three cases (if any) is the *blended* portfolio less volatile than asset 2 alone (whose volatility is $0.05$)? For each case, state in one sentence what the sign of the covariance is doing to the cross-term.

**(d) [6 pts]** Maya's professor frames a book of mortgages the same way: each loan looks identical on paper, but defaults can move together (a regional recession) or independently. Explain, in three or four sentences and referencing the cross-term $2w(1-w)\sigma_{12}$, why a lender holding 100 loans whose defaults move *together* faces more total risk than a lender holding 100 otherwise-identical loans whose defaults move *independently* — even though every individual loan has the same default variance.

---

## Problem 4 — Correlation is a cosine; prove $|\rho| \le 1$ (22 points)

**(a) [10 pts]** Prove the Cauchy–Schwarz inequality for random variables,
$$
\operatorname{Cov}(X,Y)^2 \le \operatorname{Var}(X)\,\operatorname{Var}(Y),
$$
using the one-variable-knob method from the chapter: for centered variables $\tilde X = X - \mathbb{E}[X]$ and $\tilde Y = Y - \mathbb{E}[Y]$ and any real $t$, the quantity $\operatorname{Var}(X - tY) = \mathbb{E}[(\tilde X - t\tilde Y)^2]$ cannot be negative. Expand it as a quadratic in $t$, and use the fact that a downward-or-upward parabola that is never negative must have discriminant $\le 0$. Then state, in one sentence, the exact condition under which equality holds (i.e. $|\rho| = 1$) and what it means geometrically.

**(b) [4 pts]** Conclude that $-1 \le \rho_{XY} \le 1$ where $\rho_{XY} = \operatorname{Cov}(X,Y) / (\operatorname{sd}(X)\operatorname{sd}(Y))$. Identify which step of part (a) is the random-variable translation of $|\cos\theta| \le 1$.

**(c) [4 pts]** Sam is studying two momentum signals with $\operatorname{sd}(X) = 0.15$ and $\operatorname{sd}(Y) = 0.04$. A data vendor reports $\operatorname{Cov}(X,Y) = 0.006$. Using the geometric picture, find the implied correlation $\rho$ and the angle $\theta$ between the two signals (in degrees, $\cos\theta = \rho$). Then explain why a *reported* covariance of $0.006$ is at the very edge of what is possible for these two standard deviations, and give a specific covariance value the vendor could *not* legitimately report.

**(d) [4 pts]** Sam now builds a third signal $Z = X^2$, where $X$ is symmetric about zero (so $\mathbb{E}[X] = \mathbb{E}[X^3] = 0$). Show that $\operatorname{Cov}(X, Z) = 0$, so $\rho_{XZ} = 0$ and the two are *uncorrelated* — yet $Z$ is a deterministic function of $X$ and so the two are about as dependent as variables can be. In one sentence, name the geometric reason correlation reports "no relationship" here: what kind of relationship can a cosine-of-an-angle measure see, and what kind is it blind to?

---

## Problem 5 — A covariance matrix: symmetry, PSD, and the quadratic form (18 points)

Priya, who works on climate and insurance risk, models three lines of business with the candidate covariance matrix (entries in squared-return units)
$$
\mathbf{\Sigma} = \begin{pmatrix} 0.04 & 0.01 & 0.000 \\ 0.01 & 0.09 & -0.018 \\ 0.000 & -0.018 & 0.01 \end{pmatrix}.
$$

**(a) [3 pts]** State the two structural properties every legitimate covariance matrix must have. Verify the first (symmetry) by inspection, and read off the three line-of-business *variances* and their standard deviations.

**(b) [5 pts]** Compute the three pairwise correlations $\rho_{12}, \rho_{13}, \rho_{23}$ from $\mathbf{\Sigma}$. Which pair would help Priya diversify the most, and why? Confirm each $|\rho| \le 1$ as a sanity check (this is the matrix being well-behaved on each pair).

**(c) [6 pts]** Priya proposes the equal-weight portfolio $\mathbf{w} = (1/3,\ 1/3,\ 1/3)'$. Compute the portfolio variance $\mathbf{w}'\mathbf{\Sigma}\mathbf{w}$ by expanding the double sum $\sum_{j}\sum_{k} w_j w_k \Sigma_{jk}$ (there are 9 terms; group the 3 diagonal and 6 off-diagonal). Report the portfolio standard deviation.

**(d) [4 pts]** Priya's colleague suggests adding a fourth line that is *exactly* the sum of lines 1 and 2 (a reinsurance contract bundling them). Without computing a determinant, explain why the resulting $4\times 4$ covariance matrix would be **singular** (not invertible) and only positive *semi*definite rather than positive definite. Name the weight vector $\mathbf{w}$ (with the fourth asset) for which $\mathbf{w}'\mathbf{\Sigma}\mathbf{w} = 0$, and say in one sentence why this same phenomenon will block the matrix inverse in Week 2's OLS.

---

## Problem 6 — Deriving the minimum-variance weight (16 points)

Return to a generic two-asset world with variances $\sigma_1^2$, $\sigma_2^2$ and covariance $\sigma_{12}$, weights $w$ and $1-w$.

**(a) [7 pts]** Starting from $\operatorname{Var}(R_p) = w^2\sigma_1^2 + (1-w)^2\sigma_2^2 + 2w(1-w)\sigma_{12}$, use single-variable calculus to derive the variance-minimizing weight
$$
w^\star = \frac{\sigma_2^2 - \sigma_{12}}{\sigma_1^2 + \sigma_2^2 - 2\sigma_{12}}.
$$
Show your differentiation, set the derivative to zero, solve for $w$, and verify via the second derivative that this is a minimum (not a maximum).

**(b) [5 pts]** Apply the formula to Maya's Problem 3 numbers ($\sigma_1^2 = 0.04$, $\sigma_2^2 = 0.0025$) in the uncorrelated case $\sigma_{12} = 0$. Find $w^\star$, the resulting $\operatorname{Var}(R_p)$ and $\operatorname{sd}(R_p)$, and the expected return $\mathbb{E}[R_p]$ at that weight (using $\mathbb{E}[R_1]=0.09$, $\mathbb{E}[R_2]=0.03$). Confirm that this volatility is lower than the even-split volatility you found in Problem 3(b).

**(c) [4 pts]** Examine the formula's two extremes. (i) If the assets are perfectly positively correlated and $\sigma_{12} = \sigma_1\sigma_2$, what does $w^\star$ simplify to, and why does this make economic sense? (You may assume $\sigma_1 \neq \sigma_2$.) (ii) Explain in one sentence why the chapter says this same "parabola with a genuine bottom" reappears when OLS chooses its coefficients in Week 2.

---

*Solutions: see `book/appendices/E-solutions-manual/E-w1-ps1.2-solutions.md`.*
