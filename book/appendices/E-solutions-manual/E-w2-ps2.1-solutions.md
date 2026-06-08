# Solutions — PS 2.1 (Matrix-OLS Derivations & Numerical Inversion)

**Problem set:** `book/weeks/week-02/ps2.1.md` (PS 2.1, Week 2).
**Chapter:** Ch 2.1 — OLS in Matrix Form.

These are full worked solutions, not just answers. Notation follows `CONVENTIONS.md`: bold lowercase for vectors ($\mathbf{y}$, $\boldsymbol\beta$), bold uppercase for matrices ($\mathbf{X}$, $\mathbf{H}$), a hat for estimates and fitted values ($\hat{\boldsymbol\beta}$, $\hat{\mathbf{y}}$), $N$ observations and $K$ regressors (intercept included). Exact fractions are carried wherever they keep the algebra honest; final decimals are reported to three or four places. Every numerical result here was confirmed in NumPy (`np.linalg.inv`, `np.linalg.solve`, `np.linalg.eigvalsh`); the verifying snippets are noted where useful.

---

## Problem 1 — Derive the normal equations from scratch (14 points)

**(a) (4 pts)** Expand the quadratic, treating $\mathbf{b}$ as the variable:
$$
\text{SSR}(\mathbf{b}) = (\mathbf{y} - \mathbf{X}\mathbf{b})'(\mathbf{y} - \mathbf{X}\mathbf{b})
= \mathbf{y}'\mathbf{y} - \mathbf{y}'\mathbf{X}\mathbf{b} - \mathbf{b}'\mathbf{X}'\mathbf{y} + \mathbf{b}'\mathbf{X}'\mathbf{X}\mathbf{b},
$$
where the third term used $(\mathbf{X}\mathbf{b})' = \mathbf{b}'\mathbf{X}'$. Now the merge: each of the two cross-terms $\mathbf{y}'\mathbf{X}\mathbf{b}$ and $\mathbf{b}'\mathbf{X}'\mathbf{y}$ is a $1\times 1$ matrix — a single number — and **a scalar equals its own transpose**, so $\mathbf{y}'\mathbf{X}\mathbf{b} = (\mathbf{y}'\mathbf{X}\mathbf{b})' = \mathbf{b}'\mathbf{X}'\mathbf{y}$. The two terms are therefore the same number, and they add to $-2\,\mathbf{b}'\mathbf{X}'\mathbf{y}$:
$$
\text{SSR}(\mathbf{b}) = \mathbf{y}'\mathbf{y} - 2\,\mathbf{b}'\mathbf{X}'\mathbf{y} + \mathbf{b}'\mathbf{X}'\mathbf{X}\mathbf{b}. \qquad\checkmark
$$

**(b) (4 pts)** Differentiate term by term. The constant $\mathbf{y}'\mathbf{y}$ has gradient $\mathbf{0}$. The linear term $-2\,\mathbf{b}'\mathbf{X}'\mathbf{y}$ is $-2$ times $\mathbf{b}'\mathbf{a}$ with $\mathbf{a} = \mathbf{X}'\mathbf{y}$, so its gradient is $-2\mathbf{X}'\mathbf{y}$. The quadratic term $\mathbf{b}'(\mathbf{X}'\mathbf{X})\mathbf{b}$ has gradient $2(\mathbf{X}'\mathbf{X})\mathbf{b}$ **by the rule $\partial(\mathbf{b}'\mathbf{A}\mathbf{b})/\partial\mathbf{b} = 2\mathbf{A}\mathbf{b}$, which requires $\mathbf{A} = \mathbf{X}'\mathbf{X}$ to be symmetric** — and it is, since $(\mathbf{X}'\mathbf{X})' = \mathbf{X}'(\mathbf{X}')' = \mathbf{X}'\mathbf{X}$. Hence
$$
\frac{\partial\,\text{SSR}}{\partial\mathbf{b}} = -2\mathbf{X}'\mathbf{y} + 2\mathbf{X}'\mathbf{X}\mathbf{b}.
$$
Set this to $\mathbf{0}$ at the minimizer $\hat{\boldsymbol\beta}$, cancel the $2$, and rearrange:
$$
\mathbf{X}'\mathbf{X}\hat{\boldsymbol\beta} = \mathbf{X}'\mathbf{y}. \qquad\checkmark
$$

**(c) (4 pts)** For any vector $\mathbf{v}$,
$$
\mathbf{v}'(\mathbf{X}'\mathbf{X})\mathbf{v} = (\mathbf{X}\mathbf{v})'(\mathbf{X}\mathbf{v}) = \lVert \mathbf{X}\mathbf{v}\rVert^2 \ge 0,
$$
because the squared length of any vector is non-negative. So $\mathbf{X}'\mathbf{X}$ is positive semidefinite, and the Hessian $2\mathbf{X}'\mathbf{X}$ is too. A quadratic function whose Hessian is everywhere positive semidefinite is a bowl that opens upward (never downward in any direction), so its unique flat point is a **global minimum**, not a maximum or a saddle. (When $\mathbf{X}$ has full column rank, $\mathbf{X}\mathbf{v} = \mathbf{0}$ forces $\mathbf{v} = \mathbf{0}$, so the inequality is strict for $\mathbf{v}\ne\mathbf{0}$, the Hessian is positive *definite*, and the minimizer is unique.)

**(d) (2 pts)** The geometric demand is: **the residual $\hat{\mathbf{e}} = \mathbf{y} - \mathbf{X}\hat{\boldsymbol\beta}$ must be perpendicular to every column of $\mathbf{X}$**, i.e. $\mathbf{X}'\hat{\mathbf{e}} = \mathbf{0}$, which expands directly to $\mathbf{X}'\mathbf{X}\hat{\boldsymbol\beta} = \mathbf{X}'\mathbf{y}$. This is the same fact as last week's punchline that **"uncorrelated" is "orthogonal"**: OLS forces the residual to be uncorrelated with (orthogonal to) every regressor.

---

## Problem 2 — A property of the residual maker $\mathbf{M}$ (16 points)

Throughout, take as given (proved in the chapter) that $\mathbf{H}' = \mathbf{H}$ and $\mathbf{H}\mathbf{H} = \mathbf{H}$, and that $\mathbf{I}' = \mathbf{I}$.

**(a) (4 pts)** Transpose distributes over a difference, and $\mathbf{H}$ is symmetric:
$$
\mathbf{M}' = (\mathbf{I} - \mathbf{H})' = \mathbf{I}' - \mathbf{H}' = \mathbf{I} - \mathbf{H} = \mathbf{M}. \qquad\checkmark
$$

**(b) (5 pts)** Multiply $\mathbf{M}$ by itself and expand, using $\mathbf{H}\mathbf{H} = \mathbf{H}$:
$$
\mathbf{M}\mathbf{M} = (\mathbf{I} - \mathbf{H})(\mathbf{I} - \mathbf{H})
= \mathbf{I} - \mathbf{H} - \mathbf{H} + \mathbf{H}\mathbf{H}
= \mathbf{I} - 2\mathbf{H} + \mathbf{H}
= \mathbf{I} - \mathbf{H} = \mathbf{M}. \qquad\checkmark
$$
Geometrically: $\mathbf{M}$ projects a vector onto the direction *perpendicular* to the regressor space (it returns the part of $\mathbf{y}$ the regressors cannot reach). Once you have projected off that space, you are already perpendicular to it, so projecting again changes nothing — applying $\mathbf{M}$ twice equals applying it once.

**(c) (4 pts)** Substitute $\mathbf{H} = \mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'$ and watch the inner $\mathbf{X}'\mathbf{X}$ cancel its inverse:
$$
\mathbf{M}\mathbf{X} = (\mathbf{I} - \mathbf{H})\mathbf{X}
= \mathbf{X} - \mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}\underbrace{\mathbf{X}'\mathbf{X}}_{}\,
= \mathbf{X} - \mathbf{X}\underbrace{(\mathbf{X}'\mathbf{X})^{-1}(\mathbf{X}'\mathbf{X})}_{\mathbf{I}}
= \mathbf{X} - \mathbf{X} = \mathbf{0}. \qquad\checkmark
$$
Reading it column by column, $\mathbf{M}$ sends each regressor column to the zero vector — equivalently $\mathbf{X}'\mathbf{M} = (\mathbf{M}\mathbf{X})' = \mathbf{0}$, which is exactly "the residual maker's output is orthogonal to every regressor," the matrix form of $\mathbf{X}'\hat{\mathbf{e}} = \mathbf{0}$.

**(d) (3 pts)** Start from the true model $\mathbf{y} = \mathbf{X}\boldsymbol\beta + \boldsymbol\varepsilon$ and apply $\mathbf{M}$. By linearity and the annihilator identity $\mathbf{M}\mathbf{X} = \mathbf{0}$ from (c),
$$
\hat{\mathbf{e}} = \mathbf{M}\mathbf{y} = \mathbf{M}(\mathbf{X}\boldsymbol\beta + \boldsymbol\varepsilon) = \underbrace{\mathbf{M}\mathbf{X}}_{\mathbf{0}}\boldsymbol\beta + \mathbf{M}\boldsymbol\varepsilon = \mathbf{M}\boldsymbol\varepsilon. \qquad\checkmark
$$
The systematic part $\mathbf{X}\boldsymbol\beta$ is annihilated, so the residual depends only on the (unobserved) errors. This is precisely why next chapter's variance of $\hat{\boldsymbol\beta}$ can be written purely in terms of the error structure.

---

## Problem 3 — OLS by hand with a non-diagonal $\mathbf{X}'\mathbf{X}$ (20 points)

**(a) (4 pts)**
$$
\mathbf{X} = \begin{pmatrix} 1 & 1 \\ 1 & 2 \\ 1 & 3 \\ 1 & 4 \end{pmatrix}, \qquad
\mathbf{y} = \begin{pmatrix} 1 \\ 3 \\ 4 \\ 6 \end{pmatrix}.
$$
The cross-product entries: $(1,1)$ is $N = 4$; the off-diagonal is $\sum x_i = 1+2+3+4 = 10$; the $(2,2)$ entry is $\sum x_i^2 = 1+4+9+16 = 30$. For $\mathbf{X}'\mathbf{y}$: $\sum y_i = 1+3+4+6 = 14$ and $\sum x_i y_i = 1 + 6 + 12 + 24 = 43$. So
$$
\mathbf{X}'\mathbf{X} = \begin{pmatrix} 4 & 10 \\ 10 & 30 \end{pmatrix}, \qquad
\mathbf{X}'\mathbf{y} = \begin{pmatrix} 14 \\ 43 \end{pmatrix}.
$$

**(b) (5 pts)** The determinant is $\det(\mathbf{X}'\mathbf{X}) = (4)(30) - (10)(10) = 120 - 100 = 20$. Using the $2\times 2$ inverse rule,
$$
(\mathbf{X}'\mathbf{X})^{-1} = \frac{1}{20}\begin{pmatrix} 30 & -10 \\ -10 & 4 \end{pmatrix}
= \begin{pmatrix} 3/2 & -1/2 \\ -1/2 & 1/5 \end{pmatrix}.
$$
(**Keep $\det = 20$ in your pocket for Problem 6's discussion of how a small determinant signals near-singularity.**)

**(c) (4 pts)**
$$
\hat{\boldsymbol\beta} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}
= \frac{1}{20}\begin{pmatrix} 30 & -10 \\ -10 & 4 \end{pmatrix}\begin{pmatrix} 14 \\ 43 \end{pmatrix}
= \frac{1}{20}\begin{pmatrix} 420 - 430 \\ -140 + 172 \end{pmatrix}
= \frac{1}{20}\begin{pmatrix} -10 \\ 32 \end{pmatrix}
= \begin{pmatrix} -1/2 \\ 8/5 \end{pmatrix}.
$$
So $\hat\beta_0 = -1/2 = -0.5$ and $\hat\beta_1 = 8/5 = 1.6$. **Interpretation:** each additional *ten* hours of weekly gig work is associated with a $1.6$-point rise in Maya's stress index, on average over these four students.

**(d) (4 pts)** Fitted values $\hat y_i = -\tfrac12 + \tfrac85 x_i$:
$$
\hat{\mathbf{y}} = \begin{pmatrix} -1/2 + 8/5 \\ -1/2 + 16/5 \\ -1/2 + 24/5 \\ -1/2 + 32/5 \end{pmatrix}
= \begin{pmatrix} 11/10 \\ 27/10 \\ 43/10 \\ 59/10 \end{pmatrix}, \qquad
\hat{\mathbf{e}} = \mathbf{y} - \hat{\mathbf{y}} = \begin{pmatrix} -1/10 \\ 3/10 \\ -3/10 \\ 1/10 \end{pmatrix}.
$$
Check the two identities:
$$
\sum_i \hat e_i = \tfrac{-1+3-3+1}{10} = 0, \qquad\checkmark
$$
$$
\sum_i x_i \hat e_i = 1(-\tfrac{1}{10}) + 2(\tfrac{3}{10}) + 3(-\tfrac{3}{10}) + 4(\tfrac{1}{10}) = \tfrac{-1+6-9+4}{10} = \tfrac{0}{10} = 0. \qquad\checkmark
$$
Both vanish exactly, as the normal equations force.

**(e) (3 pts)** The intercept $\hat\beta_0 = -0.5$ is the model's prediction at $x = 0$ — i.e. for a student with *zero* gig hours — which is an **extrapolation outside the data** (the smallest $x$ in the sample is $1$). The fitted values that the model actually produces over the observed range are all positive ($1.1, 2.7, 4.3, 5.9$), so the index is never predicted negative for any student in the sample. A negative intercept is just the height at which the fitted line, extended leftward, crosses $x = 0$; it carries no claim that any real student's stress is negative.

---

## Problem 4 — Leverage and the diagonal of $\mathbf{H}$ (16 points)

**(a) (3 pts)** With $\mathbf{x} = (-2,-1,0,1,2)'$ and a column of ones: $(1,1)$ entry $= N = 5$; off-diagonal $= \sum x_i = 0$; $(2,2)$ entry $= \sum x_i^2 = 4+1+0+1+4 = 10$. So
$$
\mathbf{X}'\mathbf{X} = \begin{pmatrix} 5 & 0 \\ 0 & 10 \end{pmatrix}, \qquad
(\mathbf{X}'\mathbf{X})^{-1} = \begin{pmatrix} 1/5 & 0 \\ 0 & 1/10 \end{pmatrix}.
$$
It is diagonal because the market returns sum to zero, making the two columns orthogonal in-sample.

**(b) (6 pts)** The $i$-th row of $\mathbf{X}$ is $\mathbf{x}_i' = (1, x_i)$. With the diagonal inverse,
$$
h_{ii} = \mathbf{x}_i'(\mathbf{X}'\mathbf{X})^{-1}\mathbf{x}_i
= (1, x_i)\begin{pmatrix} 1/5 & 0 \\ 0 & 1/10 \end{pmatrix}\begin{pmatrix} 1 \\ x_i \end{pmatrix}
= \frac{1}{5} + \frac{x_i^2}{10}.
$$
Since $\bar x = 0$ here, $N = 5$ and $\sum_k (x_k - \bar x)^2 = \sum_k x_k^2 = 10$, this is exactly $h_{ii} = \frac{1}{N} + \frac{(x_i - \bar x)^2}{\sum_k (x_k-\bar x)^2}$, the claimed closed form. Evaluating:
$$
\begin{aligned}
h_{11} &= \tfrac15 + \tfrac{4}{10} = \tfrac{2}{10} + \tfrac{4}{10} = \tfrac{6}{10} = \tfrac{3}{5}, &
h_{22} &= \tfrac15 + \tfrac{1}{10} = \tfrac{3}{10}, &
h_{33} &= \tfrac15 + 0 = \tfrac{1}{5},\\
h_{44} &= \tfrac15 + \tfrac{1}{10} = \tfrac{3}{10}, &
h_{55} &= \tfrac15 + \tfrac{4}{10} = \tfrac{3}{5}. &&
\end{aligned}
$$

**(c) (3 pts)**
$$
\sum_{i=1}^{5} h_{ii} = \tfrac{3}{5} + \tfrac{3}{10} + \tfrac{1}{5} + \tfrac{3}{10} + \tfrac{3}{5}
= \tfrac{6 + 3 + 2 + 3 + 6}{10} = \tfrac{20}{10} = 2 = K. \qquad\checkmark
$$
(In NumPy: `np.trace(X @ np.linalg.inv(X.T@X) @ X.T)` returns `2.0`.)

**(d) (4 pts)** The highest leverage is shared by **days 1 and 5** ($h = 3/5$), the two most extreme market returns; the lowest is **day 3** ($h = 1/5 = 1/N$), the day sitting exactly at the mean. What drives leverage is the **squared distance of $x_i$ from $\bar x$**: every point gets a baseline $1/N$ just for being in the sample, plus a bonus that grows with how far its regressor value sits from the center. A point with leverage near the maximum of $1$ is a near-isolated extreme in $\mathbf{x}$ whose fitted value is pinned almost entirely by its *own* outcome — the line is forced to chase that single point — so a recording error or one-off shock there can swing the whole fit. That is exactly the kind of observation an analyst should inspect before trusting the regression.

---

## Problem 5 — Orthogonality and the Pythagorean SSR split (16 points)

We reuse $\hat{\mathbf{y}} = (11/10, 27/10, 43/10, 59/10)'$ and $\hat{\mathbf{e}} = (-1/10, 3/10, -3/10, 1/10)'$ from Problem 3, with $\bar y = 14/4 = 7/2$.

**(a) (4 pts)** Numerically,
$$
\hat{\mathbf{y}}'\hat{\mathbf{e}} = \tfrac{1}{100}\big[ 11(-1) + 27(3) + 43(-3) + 59(1)\big]
= \tfrac{1}{100}\big[ -11 + 81 - 129 + 59\big] = \tfrac{0}{100} = 0. \qquad\checkmark
$$
**General proof.** Since $\hat{\mathbf{y}} = \mathbf{X}\hat{\boldsymbol\beta}$, transpose to get $\hat{\mathbf{y}}' = \hat{\boldsymbol\beta}'\mathbf{X}'$. Then
$$
\hat{\mathbf{y}}'\hat{\mathbf{e}} = \hat{\boldsymbol\beta}'\mathbf{X}'\hat{\mathbf{e}} = \hat{\boldsymbol\beta}'(\mathbf{X}'\hat{\mathbf{e}}) = \hat{\boldsymbol\beta}'\mathbf{0} = 0,
$$
using the normal-equation fact $\mathbf{X}'\hat{\mathbf{e}} = \mathbf{0}$. Fitted values and residuals are orthogonal for *any* full-rank design.

**(b) (4 pts)** With $\bar y = 7/2 = 35/10$:
$$
\text{TSS} = \sum_i (y_i - \bar y)^2 = (-\tfrac52)^2 + (-\tfrac12)^2 + (\tfrac12)^2 + (\tfrac52)^2 = \tfrac{25 + 1 + 1 + 25}{4} = \tfrac{52}{4} = 13.
$$
$$
\text{ESS} = \sum_i (\hat y_i - \bar y)^2 = \big(\tfrac{11-35}{10}\big)^2 + \big(\tfrac{27-35}{10}\big)^2 + \big(\tfrac{43-35}{10}\big)^2 + \big(\tfrac{59-35}{10}\big)^2
$$
$$
= \tfrac{(-24)^2 + (-8)^2 + 8^2 + 24^2}{100} = \tfrac{576 + 64 + 64 + 576}{100} = \tfrac{1280}{100} = \tfrac{64}{5} = 12.8.
$$
$$
\text{RSS} = \sum_i \hat e_i^2 = \tfrac{(-1)^2 + 3^2 + (-3)^2 + 1^2}{100} = \tfrac{1 + 9 + 9 + 1}{100} = \tfrac{20}{100} = \tfrac{1}{5} = 0.2.
$$

**(c) (4 pts)** Add: $\text{ESS} + \text{RSS} = \tfrac{64}{5} + \tfrac{1}{5} = \tfrac{65}{5} = 13 = \text{TSS}$. $\checkmark$

**Reason.** Write each centered outcome as the sum of a centered fit and a residual, $y_i - \bar y = (\hat y_i - \bar y) + \hat e_i$ (this is just $y_i = \hat y_i + \hat e_i$ with $\bar y$ subtracted). Square and sum:
$$
\sum_i (y_i - \bar y)^2 = \sum_i (\hat y_i - \bar y)^2 + \sum_i \hat e_i^2 + 2\sum_i (\hat y_i - \bar y)\hat e_i .
$$
The cross-term splits as $\sum_i \hat y_i \hat e_i - \bar y \sum_i \hat e_i$. The first piece is $0$ because fitted values are orthogonal to residuals (part a); the second is $0$ because the intercept forces $\sum_i \hat e_i = 0$. So the cross-term dies entirely and $\text{TSS} = \text{ESS} + \text{RSS}$. (Geometrically, this is the Pythagorean theorem applied to the right triangle whose legs are the explained vector $\hat{\mathbf{y}} - \bar y\mathbf{1}$ and the residual $\hat{\mathbf{e}}$.)

**(d) (4 pts)**
$$
R^2 = \frac{\text{ESS}}{\text{TSS}} = \frac{64/5}{13} = \frac{64}{65} \approx 0.9846.
$$
About **98.5% of the variation in Maya's stress index is accounted for by the fitted line** in gig hours (the rest is residual). And none of this required any probabilistic assumption: TSS, ESS, RSS, the orthogonality, and the Pythagorean split are all consequences of the *least-squares geometry* of the numbers in front of us — they would hold for any data whatever, with no claim about a "true" model, unbiasedness, or randomness.

---

## Problem 6 — Collinearity, the inverse, and the condition number (18 points)

**(a) (4 pts)** With $\mathbf{X}'\mathbf{X} = \begin{pmatrix} 1 & c \\ c & 1\end{pmatrix}$, the determinant is $\det = 1 - c^2 = (1-c)(1+c)$, and
$$
(\mathbf{X}'\mathbf{X})^{-1} = \frac{1}{1 - c^2}\begin{pmatrix} 1 & -c \\ -c & 1 \end{pmatrix}.
$$
As $c \to 1^-$, $\det = 1 - c^2 \to 0$, so **every entry of the inverse blows up to $\pm\infty$**. At $c = 1$ exactly the two columns are identical, $\mathbf{X}'\mathbf{X}$ is singular, the inverse does not exist, and $\hat{\boldsymbol\beta} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$ cannot be formed — the estimator is **not pinned down**, exactly as the chapter warns.

**(b) (4 pts)** Check the eigenvectors: $\begin{pmatrix}1 & c \\ c & 1\end{pmatrix}\begin{pmatrix}1\\1\end{pmatrix} = \begin{pmatrix}1+c\\1+c\end{pmatrix} = (1+c)\begin{pmatrix}1\\1\end{pmatrix}$, and likewise $\begin{pmatrix}1\\-1\end{pmatrix}$ gives eigenvalue $1-c$. So $\lambda_{\max} = 1+c$, $\lambda_{\min} = 1-c$, and the condition number is
$$
\kappa = \frac{\lambda_{\max}}{\lambda_{\min}} = \frac{1+c}{1-c}.
$$
Evaluating: $\kappa(0) = 1$ (perfectly conditioned), $\kappa(0.9) = 1.9/0.1 = 19$, and $\kappa(0.98) = 1.98/0.02 = 99$.

**(c) (6 pts)** At $c = 0.98$, $\det = 1 - 0.98^2 = 1 - 0.9604 = 0.0396 = 99/2500$, so
$$
(\mathbf{X}'\mathbf{X})^{-1} = \frac{1}{0.0396}\begin{pmatrix} 1 & -0.98 \\ -0.98 & 1 \end{pmatrix}.
$$
Solve $\mathbf{X}'\mathbf{X}\,\hat{\boldsymbol\beta} = \mathbf{X}'\mathbf{y}$ for each right-hand side.

For $\mathbf{X}'\mathbf{y} = (1,1)'$: by symmetry the entries are equal, $\hat\beta_1 = \hat\beta_2 = \dfrac{1 - 0.98}{0.0396} = \dfrac{0.02}{0.0396} = \dfrac{50}{99} \approx 0.5051$. So
$$
\hat{\boldsymbol\beta}^{(1)} = \big(\tfrac{50}{99},\ \tfrac{50}{99}\big)' \approx (0.5051,\ 0.5051)'.
$$
For $\mathbf{X}'\mathbf{y} = (1,\ 1.02)'$:
$$
\hat\beta_1 = \frac{1 - 0.98(1.02)}{0.0396} = \frac{1 - 0.9996}{0.0396} = \frac{0.0004}{0.0396} = \tfrac{1}{99} \approx 0.0101,
$$
$$
\hat\beta_2 = \frac{-0.98(1) + 1.02}{0.0396} = \frac{0.04}{0.0396} = \tfrac{100}{99} \approx 1.0101,
$$
so $\hat{\boldsymbol\beta}^{(2)} \approx (0.0101,\ 1.0101)'$.

The change is $\Delta\hat{\boldsymbol\beta} = \hat{\boldsymbol\beta}^{(2)} - \hat{\boldsymbol\beta}^{(1)} = \big(-\tfrac{49}{99},\ \tfrac{50}{99}\big)' \approx (-0.4949,\ 0.5051)'$. As a *relative* change,
$$
\frac{\lVert \Delta\hat{\boldsymbol\beta}\rVert}{\lVert \hat{\boldsymbol\beta}^{(1)}\rVert}
= \frac{\sqrt{0.4949^2 + 0.5051^2}}{\sqrt{0.5051^2 + 0.5051^2}}
\approx \frac{0.7071}{0.7143} \approx 0.990.
$$
**Comment.** The right-hand side moved by a relative amount $\tfrac{\lVert\Delta\mathbf{d}\rVert}{\lVert\mathbf{d}\rVert} = \tfrac{0.02}{\sqrt2} \approx 0.0141$ (about $1.4\%$), yet the solution moved by about $99\%$ — an amplification factor near $70$. This is the condition number in action: the worst-case amplification is bounded by $\kappa = 99$, and we landed close to it. A near-collinear design ($c$ close to $1$) makes $\hat{\boldsymbol\beta}$ violently sensitive to tiny changes in the data, which is the precision problem Ch 2.4 will quantify with standard errors. (NumPy check: `np.linalg.solve(A, [1,1])` and `np.linalg.solve(A, [1,1.02])` with `A=[[1,.98],[.98,1]]` return these vectors; `np.linalg.cond(A)` returns `99.0`.)

**(d) (4 pts)** If the raw second column is exactly $2\times$ the first, write $\mathbf{X} = (\mathbf{x}_1\ \ 2\mathbf{x}_1)$. Take $\mathbf{v} = (2,\ -1)'$:
$$
\mathbf{X}\mathbf{v} = 2\,\mathbf{x}_1 + (-1)(2\mathbf{x}_1) = 2\mathbf{x}_1 - 2\mathbf{x}_1 = \mathbf{0},
$$
a nonzero $\mathbf{v}$ in the null space. Then $\mathbf{v}'(\mathbf{X}'\mathbf{X})\mathbf{v} = \lVert\mathbf{X}\mathbf{v}\rVert^2 = 0$ with $\mathbf{v}\ne\mathbf{0}$, so $\mathbf{X}'\mathbf{X}$ has a zero eigenvalue — it is singular and has no inverse, so $\hat{\boldsymbol\beta} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$ **does not exist at all** (this is the $c \to 1$ limit of part a, not just a large-$\kappa$ imprecision). It is the same wall as Ch 1.2: when one asset's returns were a linear combination of the others, the covariance matrix $\mathbf{\Sigma}$ went singular and could not be inverted; here, when one regressor is a linear combination of another, the close cousin $\mathbf{X}'\mathbf{X}$ goes singular for the identical reason — a redundant column collapses the dimension of the space the columns span.

---

*All numerical answers verified in NumPy. Key results: P3 $\hat{\boldsymbol\beta} = (-1/2, 8/5)$, $\det(\mathbf{X}'\mathbf{X}) = 20$; P4 leverages $(3/5, 3/10, 1/5, 3/10, 3/5)$ summing to $2$; P5 $\text{TSS}=13$, $\text{ESS}=64/5$, $\text{RSS}=1/5$, $R^2 = 64/65 \approx 0.985$; P6 $\kappa(0.98) = 99$ with a $\sim$1.4% RHS nudge producing a $\sim$99% swing in $\hat{\boldsymbol\beta}$.*
