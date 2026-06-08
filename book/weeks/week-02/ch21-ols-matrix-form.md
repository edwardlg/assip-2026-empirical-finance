# Ch 2.1 — OLS in Matrix Form

Last week you learned to think of a random variable as a vector and of covariance as an inner product. That picture is about to pay an enormous dividend. In this chapter we take the regression you have only ever met as a black box — type two columns into a stats package, get back a slope and an intercept — and rebuild it from the floor up, in the one language that makes everything afterward (efficiency, robust standard errors, instrumental variables, fixed effects) tractable: **matrix algebra**. By the end you will be able to write the entire estimation procedure on a single line, $\hat{\boldsymbol\beta} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$, derive it two completely different ways, and — this is the part that sticks — *see* what it does. It does one thing: it drops a perpendicular.

We anchor everything in a question Sam has been chewing on. Sam trades, follows momentum, and has noticed that on days the whole market jumps, his favorite stock tends to jump too — but not one-for-one. He wants a number for that: if the market moves 1%, how much does his stock move, on average? That number has a name in finance, **beta**, and estimating it is a regression of the stock's return on the market's return. We will set up Sam's regression with a deliberately tiny dataset — small enough that you can invert the matrices by hand and check every claim — and then watch the same machinery scale, unchanged, to thousands of observations and dozens of regressors.

One promise up front. Everything in this chapter is about the *algebra* and *geometry* of the least-squares fit. We are not yet asking whether the fit is any good, whether it is unbiased, or how uncertain $\hat{\boldsymbol\beta}$ is — those questions need assumptions about where the data came from, and they are the whole of Chapters 2.2 through 2.4. Here we ask only: given the numbers in front of us, what is the best-fitting line in the least-squares sense, and why does the formula look the way it does?

## 1. Stacking the data: $\mathbf{y} = \mathbf{X}\boldsymbol\beta + \boldsymbol\varepsilon$

**The result, in one sentence.** A whole dataset's worth of regression equations — one per observation — collapses into a single matrix equation $\mathbf{y} = \mathbf{X}\boldsymbol\beta + \boldsymbol\varepsilon$, where each row of $\mathbf{X}$ is one observation and each column is one regressor.

Start with what you already know, written one observation at a time. Sam has return data for $N$ trading days. On day $i$ his stock returned $y_i$ and the market returned $x_i$. The simple regression model says each day's stock return is a line in the market return plus a leftover:

$$
y_i = \beta_0 + \beta_1 x_i + \varepsilon_i, \qquad i = 1, \dots, N.
$$

Here $\beta_0$ is the intercept (the part of the stock's return unrelated to the market), $\beta_1$ is the slope — Sam's beta, the sensitivity to the market — and $\varepsilon_i$ is the **error** or **disturbance** for day $i$: everything about that day's return the line does not capture (stock-specific news, noise, whatever the market move leaves unexplained). These are population quantities. The $\beta$'s are fixed unknown numbers we want to learn; the $\varepsilon_i$ are unobserved.

Writing this out for every day is repetitive, and repetition is exactly what matrices exist to absorb. Stack the $N$ outcome values into a column vector, stack the errors the same way, and — here is the one mildly clever move — build a matrix $\mathbf{X}$ whose first column is all ones and whose second column holds the market returns:

$$
\underbrace{\begin{pmatrix} y_1 \\ y_2 \\ \vdots \\ y_N \end{pmatrix}}_{\mathbf{y}\ (N\times 1)}
=
\underbrace{\begin{pmatrix} 1 & x_1 \\ 1 & x_2 \\ \vdots & \vdots \\ 1 & x_N \end{pmatrix}}_{\mathbf{X}\ (N\times 2)}
\underbrace{\begin{pmatrix} \beta_0 \\ \beta_1 \end{pmatrix}}_{\boldsymbol\beta\ (2\times 1)}
+
\underbrace{\begin{pmatrix} \varepsilon_1 \\ \varepsilon_2 \\ \vdots \\ \varepsilon_N \end{pmatrix}}_{\boldsymbol\varepsilon\ (N\times 1)}.
$$

Why does the column of ones belong there? Multiply the first row of $\mathbf{X}$ by $\boldsymbol\beta$: you get $1\cdot\beta_0 + x_1\cdot\beta_1 = \beta_0 + \beta_1 x_1$, which is exactly the right-hand side of the first equation. The column of ones is the intercept's "regressor" — a variable that equals 1 for everyone, so its coefficient $\beta_0$ adds the same baseline to every prediction. With that trick the matrix product $\mathbf{X}\boldsymbol\beta$ reproduces all $N$ equations at once, and we write the model as

$$
\mathbf{y} = \mathbf{X}\boldsymbol\beta + \boldsymbol\varepsilon.
$$

This is the master equation of the next four chapters, so fix the shapes and names in your head. We have $N$ observations and $K$ regressors *including the intercept* (so Sam's simple regression has $K = 2$). Then:

- $\mathbf{y}$ is the $N\times 1$ **outcome** (or response, dependent variable) vector.
- $\mathbf{X}$ is the $N\times K$ **design matrix**. Row $i$ is observation $i$; column $j$ is regressor $j$. The first column is usually all ones for the intercept.
- $\boldsymbol\beta$ is the $K\times 1$ vector of unknown **coefficients**.
- $\boldsymbol\varepsilon$ is the $N\times 1$ vector of unobserved **errors**.

Nothing about this is special to two regressors. If Sam later wants to control for, say, the previous day's return and a measure of trading volume, those become extra columns of $\mathbf{X}$, extra entries of $\boldsymbol\beta$, and the equation $\mathbf{y} = \mathbf{X}\boldsymbol\beta + \boldsymbol\varepsilon$ does not change a single symbol. That invariance is the entire reason we work in matrix form: one derivation, done once, covers every linear regression you will ever run.

**Sam's tiny dataset.** To keep the arithmetic visible, suppose Sam pulls just four trading days. The market return $x_i$ and his stock's return $y_i$, in percent, are:

| Day $i$ | Market $x_i$ | Stock $y_i$ |
|---|---|---|
| 1 | $-2$ | $-1$ |
| 2 | $0$ | $0$ |
| 3 | $1$ | $3$ |
| 4 | $1$ | $2$ |

So $N = 4$, $K = 2$, and the pieces are

$$
\mathbf{y} = \begin{pmatrix} -1 \\ 0 \\ 3 \\ 2 \end{pmatrix}, \qquad
\mathbf{X} = \begin{pmatrix} 1 & -2 \\ 1 & 0 \\ 1 & 1 \\ 1 & 1 \end{pmatrix}.
$$

We will carry this example through the whole chapter and recover Sam's beta by hand. Notice already that there is no line passing through all four points (days 3 and 4 share the same market return but different stock returns, so *no* function of $x$ can hit both). There will be leftover error no matter what line we pick — which is precisely why we need a principled rule for choosing the "best" one.

## 2. The least-squares objective

**The result, in one sentence.** Among all candidate coefficient vectors, ordinary least squares picks the one that makes the sum of squared residuals as small as possible.

We do not know $\boldsymbol\beta$, so we *guess* it. Call a candidate guess $\mathbf{b}$ (a plain $K\times 1$ vector of numbers we get to choose). For that guess, the predicted outcome for observation $i$ is the fitted value $\mathbf{x}_i'\mathbf{b}$, where $\mathbf{x}_i'$ is the $i$-th row of $\mathbf{X}$, and the **residual** is the gap between what actually happened and what the guess predicts:

$$
e_i(\mathbf{b}) = y_i - \mathbf{x}_i'\mathbf{b}.
$$

Be careful with two words that look like twins but are not. The **error** $\varepsilon_i = y_i - \mathbf{x}_i'\boldsymbol\beta$ is built from the *true, unknown* $\boldsymbol\beta$ and we never observe it. The **residual** $e_i = y_i - \mathbf{x}_i'\mathbf{b}$ is built from a *guess* $\mathbf{b}$ and we can compute it for any guess we like. The whole game is to choose $\mathbf{b}$ so that the residuals are collectively small; the resulting best guess we will crown $\hat{\boldsymbol\beta}$.

What does "collectively small" mean? We cannot just add the residuals — positive and negative ones would cancel, and a wildly wrong line could score zero. We square them first (killing the signs, and punishing big misses more than small ones), then add. Stacking the residuals into a vector $\mathbf{e}(\mathbf{b}) = \mathbf{y} - \mathbf{X}\mathbf{b}$, the **sum of squared residuals** is

$$
\text{SSR}(\mathbf{b}) = \sum_{i=1}^{N} e_i(\mathbf{b})^2 = \mathbf{e}'\mathbf{e} = (\mathbf{y} - \mathbf{X}\mathbf{b})'(\mathbf{y} - \mathbf{X}\mathbf{b}).
$$

That middle step, $\sum_i e_i^2 = \mathbf{e}'\mathbf{e}$, is worth pausing on: a vector dotted with itself is the sum of its squared entries — its squared length. So SSR is literally the squared length of the residual vector, the squared distance between $\mathbf{y}$ and the prediction $\mathbf{X}\mathbf{b}$. "Least squares" means *shortest residual vector*. Hold that thought; in Section 5 it becomes the entire geometry.

**Ordinary least squares (OLS)** is the rule: choose

$$
\hat{\boldsymbol\beta} = \arg\min_{\mathbf{b}} \ (\mathbf{y} - \mathbf{X}\mathbf{b})'(\mathbf{y} - \mathbf{X}\mathbf{b}).
$$

You met a function shaped like this last week without realizing it would return. When Maya minimized her portfolio's variance, she was minimizing a quadratic in the weight $w$ — a parabola with a genuine bottom. SSR$(\mathbf{b})$ is the same kind of object, a quadratic bowl in the entries of $\mathbf{b}$, and minimizing it is the same calculus move, just done in $K$ dimensions at once. Let us do it.

## 3. The normal equations, by calculus

**The result, in one sentence.** Setting the gradient of SSR to zero gives the **normal equations** $\mathbf{X}'\mathbf{X}\hat{\boldsymbol\beta} = \mathbf{X}'\mathbf{y}$, a tidy linear system the minimizing coefficients must satisfy.

Expand the objective by multiplying it out, treating $\mathbf{b}$ as the variable. Using the rule that $(\mathbf{A}\mathbf{B})' = \mathbf{B}'\mathbf{A}'$ to transpose the products:

$$
\text{SSR}(\mathbf{b}) = (\mathbf{y} - \mathbf{X}\mathbf{b})'(\mathbf{y} - \mathbf{X}\mathbf{b}) = \mathbf{y}'\mathbf{y} - \mathbf{y}'\mathbf{X}\mathbf{b} - \mathbf{b}'\mathbf{X}'\mathbf{y} + \mathbf{b}'\mathbf{X}'\mathbf{X}\mathbf{b}.
$$

The two middle terms are each a single number (a $1\times 1$ matrix), and a number equals its own transpose, so $\mathbf{y}'\mathbf{X}\mathbf{b} = (\mathbf{y}'\mathbf{X}\mathbf{b})' = \mathbf{b}'\mathbf{X}'\mathbf{y}$. They are identical, and we can merge them:

$$
\text{SSR}(\mathbf{b}) = \mathbf{y}'\mathbf{y} - 2\,\mathbf{b}'\mathbf{X}'\mathbf{y} + \mathbf{b}'\mathbf{X}'\mathbf{X}\mathbf{b}.
$$

Now minimize. In one-variable calculus you differentiate and set the derivative to zero; with a vector of variables you do the same to each component at once, which is the **gradient** $\partial/\partial\mathbf{b}$. You need exactly two matrix-calculus facts, and both are direct analogues of scalar rules you already trust. For a constant vector $\mathbf{a}$ and a symmetric matrix $\mathbf{A}$:

$$
\frac{\partial}{\partial \mathbf{b}}\,(\mathbf{a}'\mathbf{b}) = \mathbf{a}
\qquad\text{(the analogue of } \tfrac{d}{db}(ab) = a\text{)},
$$
$$
\frac{\partial}{\partial \mathbf{b}}\,(\mathbf{b}'\mathbf{A}\mathbf{b}) = 2\mathbf{A}\mathbf{b}
\qquad\text{(the analogue of } \tfrac{d}{db}(ab^2) = 2ab\text{)}.
$$

(The matrix $\mathbf{A} = \mathbf{X}'\mathbf{X}$ here is symmetric — check: $(\mathbf{X}'\mathbf{X})' = \mathbf{X}'\mathbf{X}'' = \mathbf{X}'\mathbf{X}$ — so the second rule applies cleanly.) Apply them term by term. The constant $\mathbf{y}'\mathbf{y}$ differentiates to zero, the linear term $-2\mathbf{b}'\mathbf{X}'\mathbf{y}$ gives $-2\mathbf{X}'\mathbf{y}$, and the quadratic term $\mathbf{b}'\mathbf{X}'\mathbf{X}\mathbf{b}$ gives $2\mathbf{X}'\mathbf{X}\mathbf{b}$:

$$
\frac{\partial\,\text{SSR}}{\partial \mathbf{b}} = -2\mathbf{X}'\mathbf{y} + 2\mathbf{X}'\mathbf{X}\mathbf{b}.
$$

Set this gradient to the zero vector and call the solution $\hat{\boldsymbol\beta}$. The $2$'s cancel, and rearranging gives the **normal equations**:

$$
\boxed{\ \mathbf{X}'\mathbf{X}\,\hat{\boldsymbol\beta} = \mathbf{X}'\mathbf{y}\ }
$$

These are $K$ linear equations in the $K$ unknowns of $\hat{\boldsymbol\beta}$. They are called "normal" not because they are ordinary but because "normal" is the old word for *perpendicular* — a clue we will cash out in Section 5. Before solving them, notice we have only verified that the gradient vanishes here, which marks a flat point. Is it a minimum? Yes, and decisively: the second-derivative (Hessian) of SSR is $2\mathbf{X}'\mathbf{X}$, and $\mathbf{X}'\mathbf{X}$ is positive semidefinite (for any vector $\mathbf{v}$, $\mathbf{v}'\mathbf{X}'\mathbf{X}\mathbf{v} = (\mathbf{X}\mathbf{v})'(\mathbf{X}\mathbf{v}) = \lVert\mathbf{X}\mathbf{v}\rVert^2 \ge 0$ — the same "a squared length is never negative" argument that made $\mathbf{\Sigma}$ positive semidefinite last week). A quadratic with a non-negative-definite Hessian is a bowl opening upward, so the flat point is its bottom. No competing maxima or saddles. Least squares has a unique honest minimum, provided we can actually solve the system — which is the content of Section 6.

## 4. The same equations, by orthogonality

**The result, in one sentence.** The normal equations also fall out with no calculus at all, from a single geometric demand: the residual vector must be perpendicular to every regressor.

Calculus is reliable but it can feel like symbol-pushing. Here is the same destination reached by pure reasoning, and it is the version worth remembering. Suppose $\hat{\boldsymbol\beta}$ truly minimizes the squared length of the residual $\hat{\mathbf{e}} = \mathbf{y} - \mathbf{X}\hat{\boldsymbol\beta}$. I claim $\hat{\mathbf{e}}$ must be orthogonal to every column of $\mathbf{X}$.

Why? Suppose it weren't — suppose the residual still had some component lying along one of the regressors, say column $\mathbf{x}_j$. Then we could nudge our fit a little in the $\mathbf{x}_j$ direction and shave off that leftover component, making the residual strictly shorter, which contradicts our having minimized its length. The only way no such improving nudge exists is if the residual has *zero* component along every column of $\mathbf{X}$ — that is, $\hat{\mathbf{e}}$ is perpendicular to the entire column space. (This is the exact analogue of the most familiar fact in plane geometry: the shortest path from a point to a line is the perpendicular dropped to it. Any non-perpendicular drop is longer.)

"Perpendicular to every column of $\mathbf{X}$" is a statement we can write in one stroke. Stacking the dot products of $\hat{\mathbf{e}}$ with each column means $\mathbf{X}'\hat{\mathbf{e}} = \mathbf{0}$. Substitute the definition of the residual:

$$
\mathbf{X}'\hat{\mathbf{e}} = \mathbf{0}
\quad\Longrightarrow\quad
\mathbf{X}'(\mathbf{y} - \mathbf{X}\hat{\boldsymbol\beta}) = \mathbf{0}
\quad\Longrightarrow\quad
\mathbf{X}'\mathbf{y} - \mathbf{X}'\mathbf{X}\hat{\boldsymbol\beta} = \mathbf{0}
\quad\Longrightarrow\quad
\mathbf{X}'\mathbf{X}\hat{\boldsymbol\beta} = \mathbf{X}'\mathbf{y}.
$$

The identical normal equations, with not one derivative taken. The calculus route and the geometry route are two faces of the same coin: minimizing a squared length and dropping a perpendicular are the same act. This is why last week's punchline — "uncorrelated" *is* "orthogonal" — matters so much. OLS hunts for coefficients that leave a residual uncorrelated with (orthogonal to) every regressor. The estimator is, at its heart, an orthogonality machine.

One concrete consequence drops out immediately, and it is a fact people quote constantly. Because the first column of $\mathbf{X}$ is all ones, the first equation in $\mathbf{X}'\hat{\mathbf{e}} = \mathbf{0}$ reads $\sum_i \hat{e}_i = 0$: **whenever the regression includes an intercept, the OLS residuals sum to exactly zero.** Not approximately — exactly, as an algebraic identity, no matter what the data look like. The other equations say $\sum_i x_{ij}\hat{e}_i = 0$ for each regressor $j$: residuals are uncorrelated with every regressor by construction. These are not assumptions or lucky outcomes; they are what "least squares" mechanically forces.

## 5. The estimator, and OLS as projection

**The result, in one sentence.** Solving the normal equations gives $\hat{\boldsymbol\beta} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$, and geometrically this projects $\mathbf{y}$ onto the column space of $\mathbf{X}$ — the fitted values are the shadow $\mathbf{y}$ casts onto the space the regressors can reach.

If the $K\times K$ matrix $\mathbf{X}'\mathbf{X}$ has an inverse (Section 6 pins down exactly when), multiply both sides of the normal equations on the left by $(\mathbf{X}'\mathbf{X})^{-1}$ and the matrix on the left of $\hat{\boldsymbol\beta}$ collapses to the identity:

$$
\boxed{\ \hat{\boldsymbol\beta} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}\ }
$$

There it is — the formula on the front of every econometrics course. It is worth seeing it not as a magic incantation but as the unique solution to "find the coefficients whose residual is perpendicular to the regressors." Everything else in this book is built on top of this one line.

Now the geometry, which is where intuition lives. The fitted values are

$$
\hat{\mathbf{y}} = \mathbf{X}\hat{\boldsymbol\beta} = \mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\,\mathbf{y}.
$$

Think about what $\hat{\mathbf{y}} = \mathbf{X}\hat{\boldsymbol\beta}$ can possibly be. It is $\mathbf{X}$ times some vector of coefficients, which is to say a *linear combination of the columns of* $\mathbf{X}$. The set of all such combinations — every vector you can build by weighting and adding the regressor columns — is a flat subspace of $N$-dimensional space called the **column space** of $\mathbf{X}$, written $\text{col}(\mathbf{X})$. For Sam's $K=2$ example, $\text{col}(\mathbf{X})$ is the 2-dimensional plane inside 4-dimensional space spanned by the all-ones column and the market-return column. The outcome $\mathbf{y}$ is a point in that 4-dimensional space, and it almost never lies *in* the plane (recall: no line fit Sam's four points exactly). So OLS asks: which point in the plane $\text{col}(\mathbf{X})$ is closest to $\mathbf{y}$?

The answer, from plane geometry scaled up, is the **orthogonal projection** of $\mathbf{y}$ onto the plane — the foot of the perpendicular dropped from $\mathbf{y}$ to $\text{col}(\mathbf{X})$. That projected point is $\hat{\mathbf{y}}$, the fitted values. The leftover, $\hat{\mathbf{e}} = \mathbf{y} - \hat{\mathbf{y}}$, is the perpendicular itself, sticking straight out of the plane. This is the same orthogonality from Section 4, now drawn as a picture: $\mathbf{y}$ splits into a piece lying *in* the regressor space (what the regressors can explain, $\hat{\mathbf{y}}$) and a piece *perpendicular* to it (what they cannot, $\hat{\mathbf{e}}$), and these two pieces meet at a right angle.

Because the angle is right, the Pythagorean theorem applies to the lengths, and we get the decomposition every "$R^2$" you have ever seen rests on:

$$
\lVert \mathbf{y} \rVert^2 = \lVert \hat{\mathbf{y}} \rVert^2 + \lVert \hat{\mathbf{e}} \rVert^2,
\qquad\text{equivalently}\qquad
\hat{\mathbf{y}}'\hat{\mathbf{e}} = 0.
$$

Fitted values and residuals are orthogonal. The variation in $\mathbf{y}$ partitions cleanly into an "explained" leg and an "unexplained" leg of a right triangle, and no cross-term contaminates the split — exactly the Pythagorean risk reduction Maya saw when her two assets were perpendicular, now telling us how regression accounts for variation.

## 6. The hat matrix and the residual maker

**The result, in one sentence.** Projection onto $\text{col}(\mathbf{X})$ is itself a matrix, the **hat matrix** $\mathbf{H}$; the complementary projection onto the perpendicular direction is the **residual maker** $\mathbf{M} = \mathbf{I} - \mathbf{H}$; both are symmetric and idempotent, the algebraic fingerprints of "projecting."

Look again at the fitted values: $\hat{\mathbf{y}} = \mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\,\mathbf{y}$. The vector $\mathbf{y}$ sits on the right; everything to its left is a fixed $N\times N$ matrix that depends only on the design $\mathbf{X}$. Give it a name:

$$
\mathbf{H} = \mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}', \qquad \hat{\mathbf{y}} = \mathbf{H}\mathbf{y}.
$$

It is called the **hat matrix** because it is the operator that puts the hat on $\mathbf{y}$ — feed it the outcomes, it returns the fitted values. Geometrically, $\mathbf{H}$ *is* the projection onto $\text{col}(\mathbf{X})$: it takes any vector and returns its shadow on the regressor plane. The residuals get their own operator. Since $\hat{\mathbf{e}} = \mathbf{y} - \hat{\mathbf{y}} = \mathbf{y} - \mathbf{H}\mathbf{y} = (\mathbf{I} - \mathbf{H})\mathbf{y}$, define

$$
\mathbf{M} = \mathbf{I} - \mathbf{H}, \qquad \hat{\mathbf{e}} = \mathbf{M}\mathbf{y}.
$$

$\mathbf{M}$ is the **residual maker** (or annihilator): hand it $\mathbf{y}$ and it returns the residual vector, the part of $\mathbf{y}$ perpendicular to the regressors. Together $\mathbf{H}$ and $\mathbf{M}$ split any vector into its two orthogonal pieces, $\mathbf{y} = \mathbf{H}\mathbf{y} + \mathbf{M}\mathbf{y} = \hat{\mathbf{y}} + \hat{\mathbf{e}}$. They will appear in every remaining chapter of this week — $\mathbf{M}$ runs the partialling-out of Frisch–Waugh–Lovell in 2.3, and the diagonal entries of $\mathbf{H}$ (the "leverages") drive the robust standard errors of 2.4 — so it is worth knowing their two defining properties cold.

**Symmetric.** $\mathbf{H}' = \mathbf{H}$. Transpose it and the symmetric core $(\mathbf{X}'\mathbf{X})^{-1}$ comes back unchanged while the outer $\mathbf{X}$ and $\mathbf{X}'$ swap into place: $\mathbf{H}' = \big(\mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\big)' = \mathbf{X}\big((\mathbf{X}'\mathbf{X})^{-1}\big)'\mathbf{X}' = \mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}' = \mathbf{H}$. And $\mathbf{M}' = (\mathbf{I} - \mathbf{H})' = \mathbf{I} - \mathbf{H} = \mathbf{M}$.

**Idempotent.** $\mathbf{H}\mathbf{H} = \mathbf{H}$ and $\mathbf{M}\mathbf{M} = \mathbf{M}$. Applying a projection twice does nothing new — once you have dropped onto the plane, you are already on the plane, so dropping again leaves you put. Algebraically the inner $\mathbf{X}'\mathbf{X}$ cancels its inverse:

$$
\mathbf{H}\mathbf{H} = \mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}\underbrace{\mathbf{X}'\mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}}_{\mathbf{I}}\mathbf{X}' = \mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}' = \mathbf{H}.
$$

Two more identities you will use constantly fall out for free. First, $\mathbf{H}\mathbf{M} = \mathbf{H}(\mathbf{I}-\mathbf{H}) = \mathbf{H} - \mathbf{H}\mathbf{H} = \mathbf{H} - \mathbf{H} = \mathbf{0}$: the two projections are orthogonal, which is just "the explained and unexplained pieces meet at a right angle" again. Second, $\mathbf{M}\mathbf{X} = (\mathbf{I}-\mathbf{H})\mathbf{X} = \mathbf{X} - \mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{X} = \mathbf{X} - \mathbf{X} = \mathbf{0}$: the residual maker annihilates the regressors themselves (hence "annihilator"), which is the matrix form of "residuals are orthogonal to every regressor."

## 7. When does $\mathbf{X}'\mathbf{X}$ have an inverse?

**The result, in one sentence.** The formula $\hat{\boldsymbol\beta} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$ exists if and only if $\mathbf{X}$ has **full column rank** — no regressor is a perfect linear combination of the others — which is the regression cousin of the singular covariance matrix you met last week.

Everything so far quietly assumed $(\mathbf{X}'\mathbf{X})^{-1}$ exists. When does it? A square matrix is invertible exactly when it is non-singular, and $\mathbf{X}'\mathbf{X}$ is non-singular precisely when the columns of $\mathbf{X}$ are **linearly independent** — when no column can be written as a weighted sum of the others. We say $\mathbf{X}$ has *full column rank* (rank $K$). The failure case has a name econometricians say with a grimace: **perfect multicollinearity**.

Here is the intuition without machinery. If two columns of $\mathbf{X}$ carried the very same information — Sam accidentally includes the market return measured in percent *and* the same return measured in basis points (exactly 100 times the first) — then those columns are proportional, the column space does not actually have the dimension you think, and there is no unique way to split the explained part between the two redundant regressors. Should beta load on the percent column or the basis-points column? Any split that adds up the same gives identical fitted values, so the data cannot choose, and $\hat{\boldsymbol\beta}$ is not pinned down. Algebraically, redundant columns make $\mathbf{X}\mathbf{v} = \mathbf{0}$ for some nonzero $\mathbf{v}$, hence $\mathbf{v}'\mathbf{X}'\mathbf{X}\mathbf{v} = \lVert\mathbf{X}\mathbf{v}\rVert^2 = 0$ with $\mathbf{v}\ne\mathbf{0}$ — the quadratic form has a zero direction, so $\mathbf{X}'\mathbf{X}$ is only positive *semi*definite, singular, and has no inverse. The bowl from Section 3 has a flat-bottomed trough instead of a single low point, and least squares cannot pick one spot in the trough.

This is exactly the wall Ch 1.2 warned you about, met from the other side. There, if one asset was a linear combination of others, the covariance matrix $\mathbf{\Sigma}$ went singular and had no inverse. Here, if one regressor is a linear combination of others, $\mathbf{X}'\mathbf{X}$ — which is built the same way, as a matrix of cross-products that is a close cousin of a covariance matrix — goes singular and has no inverse. Same mathematical event, same cure: do not feed the machine a column that is redundant. Two practical notes. First, full column rank requires at least as many observations as regressors, $N \ge K$ — you cannot fit more coefficients than you have data points, or the columns are forced into dependence. Second, real software almost never sees *perfect* collinearity (it usually arises from a coding mistake, like including a dummy for every category plus an intercept); the more common and more insidious problem is *near*-collinearity, where $\mathbf{X}'\mathbf{X}$ is invertible but barely, its near-zero direction making $\hat{\boldsymbol\beta}$ wildly sensitive to tiny data changes. That sensitivity — the near-singular $\mathbf{\Sigma}$ preview from Ch 1.2 — is a precision problem we will quantify with standard errors in Chapter 2.4.

## 8. Sam's beta, by hand

Time to cash everything out on Sam's four days. We have

$$
\mathbf{X} = \begin{pmatrix} 1 & -2 \\ 1 & 0 \\ 1 & 1 \\ 1 & 1 \end{pmatrix}, \qquad
\mathbf{y} = \begin{pmatrix} -1 \\ 0 \\ 3 \\ 2 \end{pmatrix}.
$$

First build $\mathbf{X}'\mathbf{X}$. The $(1,1)$ entry is the sum of squares of the ones column, $1+1+1+1 = 4$ (which is just $N$). The off-diagonal is the sum of the market returns, $-2+0+1+1 = 0$. The $(2,2)$ entry is the sum of squared market returns, $4+0+1+1 = 6$. So

$$
\mathbf{X}'\mathbf{X} = \begin{pmatrix} 4 & 0 \\ 0 & 6 \end{pmatrix}.
$$

It came out diagonal — a small gift from the fact that the market returns happen to sum to zero, which makes the ones column and the market column orthogonal *in this sample*. (That is not generic; usually $\mathbf{X}'\mathbf{X}$ has nonzero off-diagonals. We arranged the numbers to keep the inversion painless.) Next, $\mathbf{X}'\mathbf{y}$: the first entry is the sum of the $y_i$ (dotting the ones column with $\mathbf{y}$), $-1+0+3+2 = 4$; the second is the dot product of the market column with $\mathbf{y}$, $(-2)(-1) + (0)(0) + (1)(3) + (1)(2) = 2 + 0 + 3 + 2 = 7$. So

$$
\mathbf{X}'\mathbf{y} = \begin{pmatrix} 4 \\ 7 \end{pmatrix}.
$$

Inverting a diagonal matrix just inverts each diagonal entry, so $(\mathbf{X}'\mathbf{X})^{-1} = \begin{pmatrix} 1/4 & 0 \\ 0 & 1/6 \end{pmatrix}$, and

$$
\hat{\boldsymbol\beta} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}
= \begin{pmatrix} 1/4 & 0 \\ 0 & 1/6 \end{pmatrix}\begin{pmatrix} 4 \\ 7 \end{pmatrix}
= \begin{pmatrix} 1 \\ 7/6 \end{pmatrix} \approx \begin{pmatrix} 1.000 \\ 1.167 \end{pmatrix}.
$$

So $\hat\beta_0 = 1$ and $\hat\beta_1 = 7/6 \approx 1.17$. Sam's estimated beta is about $1.17$: when the market rises 1%, his stock rises about 1.17% on average over these four days, plus a 1% baseline that has nothing to do with the market. A beta above 1 means the stock amplifies market moves — consistent with the high-octane, momentum-flavored names Sam likes.

Let us verify the orthogonality we promised. The fitted values are $\hat y_i = 1 + (7/6)x_i$:

$$
\hat{\mathbf{y}} = \begin{pmatrix} 1 + (7/6)(-2) \\ 1 + (7/6)(0) \\ 1 + (7/6)(1) \\ 1 + (7/6)(1) \end{pmatrix}
= \begin{pmatrix} -4/3 \\ 1 \\ 13/6 \\ 13/6 \end{pmatrix},
\qquad
\hat{\mathbf{e}} = \mathbf{y} - \hat{\mathbf{y}} = \begin{pmatrix} -1 + 4/3 \\ 0 - 1 \\ 3 - 13/6 \\ 2 - 13/6 \end{pmatrix}
= \begin{pmatrix} 1/3 \\ -1 \\ 5/6 \\ -1/6 \end{pmatrix}.
$$

Check the two normal-equation identities from Section 4. The residuals sum to $1/3 - 1 + 5/6 - 1/6 = 1/3 - 1 + 4/6 = 1/3 - 1 + 2/3 = 0$ — they cancel exactly, as the intercept guarantees. And the residuals are orthogonal to the market column: $(-2)(1/3) + (0)(-1) + (1)(5/6) + (1)(-1/6) = -2/3 + 5/6 - 1/6 = -2/3 + 4/6 = -2/3 + 2/3 = 0$. Both zero, on the nose. The residual vector is perpendicular to both columns of $\mathbf{X}$, the fit is the orthogonal projection of $\mathbf{y}$ onto the plane the two columns span, and the formula did precisely what the geometry said it would. The notebook reruns this in three lines of NumPy and confirms `statsmodels` returns the same $(1.000,\ 1.167)$.

## Summary

A regression model written one observation at a time, $y_i = \beta_0 + \beta_1 x_i + \varepsilon_i$, stacks into a single matrix equation $\mathbf{y} = \mathbf{X}\boldsymbol\beta + \boldsymbol\varepsilon$, where $\mathbf{X}$ is the $N\times K$ design matrix (a column of ones carries the intercept). Ordinary least squares chooses the coefficients that minimize the sum of squared residuals, $\mathbf{e}'\mathbf{e}$. Minimizing this quadratic bowl — by calculus (set the gradient to zero) or by geometry (demand the residual be perpendicular to every regressor) — gives the same **normal equations** $\mathbf{X}'\mathbf{X}\hat{\boldsymbol\beta} = \mathbf{X}'\mathbf{y}$, and solving them gives $\hat{\boldsymbol\beta} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$. Geometrically OLS projects $\mathbf{y}$ onto the column space of $\mathbf{X}$: the fitted values $\hat{\mathbf{y}} = \mathbf{H}\mathbf{y}$ are the shadow on the regressor plane, the residuals $\hat{\mathbf{e}} = \mathbf{M}\mathbf{y}$ are the perpendicular sticking out, and the two are orthogonal, splitting $\mathbf{y}$ by Pythagoras. The hat matrix $\mathbf{H} = \mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'$ and residual maker $\mathbf{M} = \mathbf{I} - \mathbf{H}$ are both symmetric and idempotent — the algebra of projecting. All of this requires $\mathbf{X}'\mathbf{X}$ to be invertible, which holds exactly when $\mathbf{X}$ has full column rank (no perfect collinearity) — the same singular-matrix wall as last week's covariance matrix $\mathbf{\Sigma}$, seen from the regression side. Sam's four-day example carried the whole machine end to end and recovered a beta of $7/6$ with residuals that sum to zero and sit perpendicular to the market.

## Your Turn

Open **nb2.1 — OLS from scratch with NumPy vs. statsmodels**. You will build $\mathbf{X}$ and $\mathbf{y}$ for Sam's data (and then a larger real return series), compute $\hat{\boldsymbol\beta} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$ by hand with NumPy's `@` and `np.linalg.inv` (and the numerically safer `np.linalg.solve`), form $\mathbf{H}$, $\mathbf{M}$, $\hat{\mathbf{y}}$, and $\hat{\mathbf{e}}$, verify symmetry and idempotency numerically, confirm the residuals are orthogonal to every regressor, and check that your from-scratch coefficients match `statsmodels.OLS` to machine precision.

Check questions before you start:

1. Using Sam's design matrix $\mathbf{X}$, compute the $(1,1)$ entry of the hat matrix $\mathbf{H}$ — that is, $H_{11}$, the leverage of day 1. (Hint: $H_{11} = \mathbf{x}_1'(\mathbf{X}'\mathbf{X})^{-1}\mathbf{x}_1$ where $\mathbf{x}_1' = (1, -2)$ is the first row of $\mathbf{X}$, and $(\mathbf{X}'\mathbf{X})^{-1}$ is diagonal with entries $1/4$ and $1/6$.) Which of the four days has the highest leverage, and does the answer match your intuition about which market return is most unusual?
2. Suppose Sam adds a third regressor to his design: a column equal to the market return *plus* the intercept column, i.e. $x_{i3} = 1 + x_i$. Explain why $\mathbf{X}'\mathbf{X}$ is now singular, and identify the nonzero vector $\mathbf{v}$ for which $\mathbf{X}\mathbf{v} = \mathbf{0}$.
3. Prove from the definitions that $\mathbf{M}$ is idempotent ($\mathbf{M}\mathbf{M} = \mathbf{M}$) using only $\mathbf{M} = \mathbf{I} - \mathbf{H}$ and the fact that $\mathbf{H}$ is idempotent. Then state in one sentence what "$\mathbf{M}$ applied twice equals $\mathbf{M}$ once" means geometrically.
