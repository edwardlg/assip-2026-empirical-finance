# Ch 1.2 — Expectations, Variance, Covariance as Geometry

In Chapter 1.1 you met the expectation operator $\mathbb{E}[\cdot]$, conditioning, and the two laws that run iterated expectations and total variance. Sam used them to split a portfolio's variance into a part you can explain and a part you can't. This chapter does something narrower and, in the long run, more useful: it nails down the *algebra* of expectation, variance, and covariance, and then shows you that this algebra is secretly **geometry**. Correlation is not a mysterious number between $-1$ and $1$. It is the cosine of an angle between two vectors. Once you see that, the fact that $|\text{correlation}| \le 1$ stops being a rule to memorize and becomes the same statement as the Pythagorean-flavored Cauchy–Schwarz inequality you already half-know.

We will anchor everything in a question Maya keeps asking. Maya cares about household finance and fair lending, and she has been handed a small, very real problem: she has some money to split between two investments, and she wants to know how risky the *combination* is. Not each piece — the blend. The answer turns out to live entirely in one term, the covariance, and that term is where "diversification" comes from. By the end of the chapter you will be able to compute a portfolio's variance by hand, see why mixing assets can lower risk below either asset alone, draw the whole thing as an angle, and write the covariance matrix $\mathbf{\Sigma}$ that Week 2 needs to do regression in matrix form.

## 1. Linearity of expectation: the one rule that never asks permission

**The result, in one sentence.** Expectation passes straight through sums and constants — $\mathbb{E}[aX + bY] = a\,\mathbb{E}[X] + b\,\mathbb{E}[Y]$ — and this is true *whether or not* $X$ and $Y$ have anything to do with each other.

That last clause is the trick, and it is the most over-looked fact in all of probability. Most operations you know require independence or some special structure. Linearity of expectation does not. $X$ and $Y$ can be the same coin flip counted twice, two assets that move in lockstep, or two utterly unrelated numbers; the expected value of their weighted sum is always the same weighted sum of their expected values.

Why is it true? Think of expectation as a weighted average, where the weights are probabilities. Averaging is a linear operation: if you double every value, the average doubles; if you add two columns of numbers row by row and average the result, you get the same thing as averaging each column and adding. For a discrete random variable $X$ taking values $x_k$ with probabilities $p_k$, $\mathbb{E}[X] = \sum_k x_k p_k$, and

$$
\mathbb{E}[aX + bY] = \sum_{j,k} (a\,x_j + b\,y_k)\,P(X=x_j, Y=y_k) = a\sum_j x_j P(X = x_j) + b\sum_k y_k P(Y = y_k) = a\,\mathbb{E}[X] + b\,\mathbb{E}[Y].
$$

Notice we summed over the *joint* distribution and the cross-terms never needed independence — each value just got weighted by how often the pair $(X,Y)$ actually occurs. The joint structure is fully accounted for, and it simply drops out.

To see that the cross-terms really do vanish, take the most adversarial case: let $Y = X$, two perfectly dependent variables. Then $\mathbb{E}[X + X] = \mathbb{E}[2X] = 2\mathbb{E}[X] = \mathbb{E}[X] + \mathbb{E}[Y]$ — the rule holds even though $X$ and $Y$ could not be *less* independent. Compare what happens to variance: $\operatorname{Var}(X + X) = \operatorname{Var}(2X) = 4\operatorname{Var}(X)$, which is emphatically *not* $\operatorname{Var}(X) + \operatorname{Var}(X) = 2\operatorname{Var}(X)$. Expectation forgives dependence; variance does not. That contrast is the hinge of the whole chapter.

**A number first.** Maya is looking at two assets. Call their one-period returns $R_1$ and $R_2$ — a return is the fractional change in value over the period, so a return of $0.06$ means the money grew by 6%. Suppose her research says $\mathbb{E}[R_1] = 0.08$ (an 8% expected return) and $\mathbb{E}[R_2] = 0.04$. If she puts a fraction $w$ of her money in asset 1 and the remaining $1-w$ in asset 2, her portfolio return is the weighted sum

$$
R_p = w R_1 + (1-w) R_2.
$$

With $w = 0.5$, linearity says the expected portfolio return is $0.5(0.08) + 0.5(0.04) = 0.06$, no matter how the two assets are related. Expected return is *easy*; it is a straight line in the weight $w$. Risk, as we are about to see, is not a straight line, and that curvature is the whole story of diversification.

**Where it fails — sort of.** Linearity never fails for expectation. The trap is assuming the same free pass extends to *nonlinear* functions. In general $\mathbb{E}[XY] \ne \mathbb{E}[X]\,\mathbb{E}[Y]$ (that equality needs uncorrelatedness), and $\mathbb{E}[g(X)] \ne g(\mathbb{E}[X])$ for nonlinear $g$ (that gap is Jensen's inequality, which you will meet again with log returns). Variance involves a square, so it is exactly one of these nonlinear functions — which is why the next section is not a one-liner.

## 2. Variance and covariance algebra

**The result, in one sentence.** Variance measures spread as an expected squared deviation, covariance measures how two variables move together as an expected product of deviations, and the variance of a sum is the sum of variances *plus twice the covariance*.

Start with the definitions. The variance of $X$ is

$$
\operatorname{Var}(X) = \mathbb{E}\!\left[(X - \mathbb{E}[X])^2\right] = \mathbb{E}[X^2] - (\mathbb{E}[X])^2,
$$

the average squared distance of $X$ from its own mean. (The second form follows by expanding the square and using linearity — verify it once by hand and never again.) Its square root is the **standard deviation** $\operatorname{sd}(X) = \sqrt{\operatorname{Var}(X)}$, which lives in the same units as $X$ itself; in finance we call it **volatility**.

The covariance of $X$ and $Y$ is the natural two-variable cousin:

$$
\operatorname{Cov}(X, Y) = \mathbb{E}\!\left[(X - \mathbb{E}[X])(Y - \mathbb{E}[Y])\right] = \mathbb{E}[XY] - \mathbb{E}[X]\,\mathbb{E}[Y].
$$

Read the first form like a story. When $X$ is above its mean, is $Y$ usually above its mean too? Then the product $(X-\mathbb{E}[X])(Y-\mathbb{E}[Y])$ is usually positive, and so is the covariance — the two variables tend to rise and fall together. When one is typically above its mean while the other is below, the product is negative and so is the covariance. If there is no systematic relationship, the positive and negative products wash out and the covariance is near zero. Notice that $\operatorname{Cov}(X, X) = \operatorname{Var}(X)$: a variable's covariance with itself is just its variance. That tiny fact is the seed of the whole matrix picture later.

**A number first, before any Greek.** Suppose two assets each return either $+10\%$ or $-10\%$ in a period, and a simple model of the joint distribution is the four-cell table below — the probability of each combination of outcomes.

| | $R_2 = +0.10$ | $R_2 = -0.10$ |
|---|---|---|
| $R_1 = +0.10$ | $0.40$ | $0.10$ |
| $R_1 = -0.10$ | $0.10$ | $0.40$ |

Each asset is up half the time and down half the time, so $\mathbb{E}[R_1] = \mathbb{E}[R_2] = 0$ and $\operatorname{Var}(R_1) = \operatorname{Var}(R_2) = \mathbb{E}[R^2] = (0.10)^2 = 0.01$. For the covariance we need $\mathbb{E}[R_1 R_2]$, which sums the product $R_1 R_2$ over the four cells weighted by probability: the two "same direction" cells contribute $(0.10)(0.10)(0.40) + (-0.10)(-0.10)(0.40) = +0.008$, and the two "opposite direction" cells contribute $(0.10)(-0.10)(0.10) + (-0.10)(0.10)(0.10) = -0.002$, for $\mathbb{E}[R_1R_2] = 0.006$. Since the means are zero, $\operatorname{Cov}(R_1, R_2) = 0.006 - 0 = 0.006 > 0$: the table's diagonal weight makes the assets move together. We will reuse exactly this kind of computation when we estimate covariances from real return histories in the notebook — there the probabilities become observed frequencies.

**The algebra you will actually use.** Four properties carry almost everything in this book. Each follows from the definitions plus linearity of expectation; I will state them, give the intuition, and let you grind one out in the problem set.

1. **Scaling.** $\operatorname{Var}(aX) = a^2 \operatorname{Var}(X)$. The square is because variance is built from squared deviations; doubling $X$ quadruples its spread-in-squared-units. A constant shift does nothing: $\operatorname{Var}(X + c) = \operatorname{Var}(X)$, because adding $c$ moves $X$ and its mean by the same amount, leaving every deviation unchanged.
2. **Bilinearity of covariance.** Covariance is linear in each argument: $\operatorname{Cov}(aX + bY,\ Z) = a\operatorname{Cov}(X,Z) + b\operatorname{Cov}(Y,Z)$, and likewise in the second slot. Constants slide out, sums split apart. This is the property that makes covariance behave like a *product* — and, as Section 4 reveals, like an inner product.
3. **Symmetry.** $\operatorname{Cov}(X,Y) = \operatorname{Cov}(Y,X)$. Order does not matter.
4. **Variance of a sum.** Combining the above,
$$
\operatorname{Var}(X + Y) = \operatorname{Var}(X) + \operatorname{Var}(Y) + 2\operatorname{Cov}(X, Y).
$$

That last line deserves a slow look, because it is the equation Maya's whole problem rides on. The variance of a sum is *not* just the sum of variances. There is a cross-term, $2\operatorname{Cov}(X,Y)$, and it can be positive, negative, or zero. If the two variables tend to move together, risk compounds; if they tend to move oppositely, risk cancels. Derive it once: write $\operatorname{Var}(X+Y) = \mathbb{E}[((X+Y) - \mathbb{E}[X+Y])^2]$, push the expectation inside using linearity, expand the square into a deviation-in-$X$ squared, a deviation-in-$Y$ squared, and a cross-product, and the three pieces are exactly $\operatorname{Var}(X)$, $\operatorname{Var}(Y)$, and $2\operatorname{Cov}(X,Y)$.

The general weighted version, which is what a portfolio actually needs, follows from scaling plus bilinearity:

$$
\operatorname{Var}(aX + bY) = a^2 \operatorname{Var}(X) + b^2 \operatorname{Var}(Y) + 2ab\operatorname{Cov}(X, Y).
$$

**When the cross-term vanishes.** If $\operatorname{Cov}(X,Y) = 0$ we call $X$ and $Y$ **uncorrelated**, and only then does variance add cleanly: $\operatorname{Var}(X+Y) = \operatorname{Var}(X) + \operatorname{Var}(Y)$. Independence implies uncorrelatedness (independent variables have $\mathbb{E}[XY] = \mathbb{E}[X]\mathbb{E}[Y]$, killing the covariance). The reverse is the classic failure mode: **uncorrelated does not imply independent.** Take $X$ symmetric about zero and $Y = X^2$. They are tightly linked — $Y$ is a deterministic function of $X$ — yet $\operatorname{Cov}(X, X^2) = \mathbb{E}[X^3] - \mathbb{E}[X]\mathbb{E}[X^2] = 0$ when the distribution is symmetric, because covariance only senses *linear* co-movement. Covariance is blind to curved relationships. Hold onto that; it is exactly the limitation that linear regression inherits in Week 2.

## 3. Maya's two-asset budget, worked end to end

Maya has \$1 to allocate (work in fractions; dollars scale trivially). Her two assets have these properties, which we will treat as known population quantities for now and learn to *estimate* in Chapter 1.3:

| Quantity | Asset 1 | Asset 2 |
|---|---|---|
| Expected return $\mathbb{E}[R]$ | $0.08$ | $0.04$ |
| Volatility $\operatorname{sd}(R)$ | $0.20$ | $0.10$ |
| Variance $\operatorname{Var}(R)$ | $0.04$ | $0.01$ |

Asset 1 is the high-octane choice: more expected return, but double the volatility. The piece we have not yet pinned down is how the two move together. Let their covariance be $\operatorname{Cov}(R_1, R_2) = \sigma_{12}$. Maya holds weight $w$ in asset 1 and $1-w$ in asset 2, so by the weighted variance formula,

$$
\operatorname{Var}(R_p) = w^2 (0.04) + (1-w)^2(0.01) + 2w(1-w)\,\sigma_{12}.
$$

Everything interesting is in $\sigma_{12}$, so let us run three scenarios at the even split $w = 0.5$, where $w^2 = (1-w)^2 = 0.25$ and $2w(1-w) = 0.5$.

**Scenario A — assets move together perfectly** ($\sigma_{12} = 0.02$, the largest it can be; we will see why in Section 4). Then
$$
\operatorname{Var}(R_p) = 0.25(0.04) + 0.25(0.01) + 0.5(0.02) = 0.01 + 0.0025 + 0.01 = 0.0225,
$$
so volatility is $\sqrt{0.0225} = 0.15$. The blend sits exactly on the line between $0.20$ and $0.10$: $0.5(0.20) + 0.5(0.10) = 0.15$. **No diversification benefit at all** — when assets move in lockstep, mixing them just averages the risk.

**Scenario B — assets are uncorrelated** ($\sigma_{12} = 0$). The cross-term dies:
$$
\operatorname{Var}(R_p) = 0.01 + 0.0025 + 0 = 0.0125, \qquad \operatorname{sd}(R_p) = \sqrt{0.0125} \approx 0.112.
$$
Volatility dropped from $0.15$ to about $0.112$ — *below the average of the two volatilities* — purely because the cross-term went away. The expected return is unchanged at $0.06$. Maya got lower risk for free; nothing about the individual assets changed, only their relationship.

**Scenario C — assets move oppositely** ($\sigma_{12} = -0.01$). Now the cross-term subtracts:
$$
\operatorname{Var}(R_p) = 0.01 + 0.0025 - 0.005 = 0.0075, \qquad \operatorname{sd}(R_p) \approx 0.087.
$$
Volatility is now $0.087$ — lower than asset 2 alone ($0.10$), the *safer* of the two assets. By blending in some of the riskier asset, Maya built a portfolio less volatile than either ingredient. This is the punchline of diversification, and it lives entirely in the sign of the covariance term.

```python
import numpy as np

var1, var2 = 0.04, 0.01           # asset variances
w = 0.5                            # weight on asset 1
for cov12 in (0.02, 0.0, -0.01):   # together / uncorrelated / opposed
    var_p = w**2*var1 + (1-w)**2*var2 + 2*w*(1-w)*cov12
    print(f"cov={cov12:+.3f}  Var={var_p:.4f}  sd={np.sqrt(var_p):.3f}")
# cov=+0.020  Var=0.0225  sd=0.150
# cov=+0.000  Var=0.0125  sd=0.112
# cov=-0.010  Var=0.0075  sd=0.087
```

**The minimum-risk blend.** Maya does not have to settle for $w = 0.5$. Since $\operatorname{Var}(R_p)$ is a quadratic in $w$, she can find the weight that minimizes it with the calculus she already owns: differentiate $\operatorname{Var}(R_p) = w^2\sigma_1^2 + (1-w)^2\sigma_2^2 + 2w(1-w)\sigma_{12}$ with respect to $w$, set it to zero, and solve, giving $w^\star = (\sigma_2^2 - \sigma_{12}) / (\sigma_1^2 + \sigma_2^2 - 2\sigma_{12})$. In Scenario B ($\sigma_{12} = 0$) this is $w^\star = 0.01 / 0.05 = 0.2$ — she should hold only 20% of the riskier asset — and plugging back in gives $\operatorname{Var}(R_p) = 0.008$, $\operatorname{sd} \approx 0.089$, lower than the even split's $0.112$. The point is not the formula but the shape: risk is a parabola in the weight, it has a genuine bottom, and the location of that bottom is governed by the covariance. Optimization over a quadratic risk surface is the seed of modern portfolio theory, and we will meet the same parabola-with-a-minimum when OLS chooses coefficients in Week 2.

**The lesson Maya takes away.** Expected return is a straight average (linearity, Section 1). Risk is *not*, because of the $2w(1-w)\sigma_{12}$ term. The lower the covariance, the more risk cancels when you combine assets — and a negative covariance can push the portfolio below its safest component. Diversification is not magic and it is not about "spreading out"; it is one term in one quadratic, and that term is the covariance. A lender like the ones Maya studies thinks the same way about a book of loans: defaults that move together (a regional recession hits everyone at once) are far more dangerous than the same number of defaults that move independently, even when each individual loan looks identical on paper.

## 4. Correlation as a cosine: random variables are vectors

We have been treating covariance as a number. Now comes the reveal that reorganizes the whole subject.

**The result, in one sentence.** Random variables (centered to mean zero) behave exactly like vectors in an inner-product space, where covariance *is* the inner product, variance is squared length, standard deviation is length, and **correlation is the cosine of the angle between two variables**.

Here is the dictionary. Recall from geometry that for two ordinary vectors $\mathbf{u}, \mathbf{v}$ the dot product satisfies $\mathbf{u}\cdot\mathbf{v} = \lVert\mathbf{u}\rVert\,\lVert\mathbf{v}\rVert\cos\theta$, where $\theta$ is the angle between them, and the dot product is *bilinear* and *symmetric*. Look back at Section 2: covariance is also bilinear and symmetric, and $\operatorname{Cov}(X,X) = \operatorname{Var}(X) \ge 0$ plays the role of "a vector dotted with itself is its squared length, which is never negative." Those are precisely the axioms of an inner product. So we set up the dictionary by centering each variable, $\tilde{X} = X - \mathbb{E}[X]$:

| Vector world | Random-variable world |
|---|---|
| inner product $\langle \mathbf{u}, \mathbf{v}\rangle$ | $\operatorname{Cov}(X, Y)$ |
| squared length $\lVert \mathbf{u}\rVert^2 = \langle \mathbf{u},\mathbf{u}\rangle$ | $\operatorname{Var}(X)$ |
| length $\lVert \mathbf{u}\rVert$ | $\operatorname{sd}(X)$ |
| cosine $\dfrac{\langle \mathbf{u},\mathbf{v}\rangle}{\lVert\mathbf{u}\rVert\,\lVert\mathbf{v}\rVert}$ | correlation $\rho_{XY}$ |
| perpendicular ($\cos\theta = 0$) | uncorrelated |

That last column gives the definition of **correlation**: it is covariance rescaled by the two standard deviations so the units cancel and only the *shape* of the relationship survives,

$$
\rho_{XY} = \operatorname{Corr}(X,Y) = \frac{\operatorname{Cov}(X,Y)}{\operatorname{sd}(X)\,\operatorname{sd}(Y)} = \frac{\sigma_{XY}}{\sigma_X \sigma_Y}.
$$

Because it is a cosine, it is a pure number in $[-1, 1]$, and the angle $\theta$ between the two variables satisfies $\cos\theta = \rho_{XY}$. Two perfectly correlated variables ($\rho = 1$) point the same way, $\theta = 0^\circ$. Two perfectly anti-correlated variables ($\rho = -1$) point opposite, $\theta = 180^\circ$. Uncorrelated variables are at $\theta = 90^\circ$ — geometrically **perpendicular**. "Uncorrelated" and "orthogonal" are the same word in two languages, and this is not an analogy you should file away as cute. It is the engine of Week 2: ordinary least squares works by projecting the outcome onto the space spanned by the regressors and keeping the perpendicular residual, and "perpendicular" there means exactly "uncorrelated" here.

**Why $|\rho| \le 1$ is Cauchy–Schwarz.** In vector geometry, $\lvert\cos\theta\rvert \le 1$ is equivalent to the **Cauchy–Schwarz inequality**, $\lvert\langle\mathbf{u},\mathbf{v}\rangle\rvert \le \lVert\mathbf{u}\rVert\,\lVert\mathbf{v}\rVert$. Translate through the dictionary and you get, for free,

$$
\lvert\operatorname{Cov}(X,Y)\rvert \le \operatorname{sd}(X)\,\operatorname{sd}(Y), \qquad\text{hence}\qquad \lvert\rho_{XY}\rvert \le 1.
$$

You can prove it without ever saying the word "geometry," and the proof is worth seeing because it is the same one-variable-knob trick that reappears in Gauss–Markov. For any real $t$, the variance of $\tilde{X} - t\tilde{Y}$ cannot be negative — it is an expected square. Expand it:

$$
0 \le \operatorname{Var}(X - tY) = \operatorname{Var}(X) - 2t\operatorname{Cov}(X,Y) + t^2\operatorname{Var}(Y).
$$

The right-hand side is a parabola in $t$ that never dips below zero, so its discriminant must be $\le 0$: $\big(2\operatorname{Cov}(X,Y)\big)^2 - 4\operatorname{Var}(X)\operatorname{Var}(Y) \le 0$, which rearranges to exactly $\operatorname{Cov}(X,Y)^2 \le \operatorname{Var}(X)\operatorname{Var}(Y)$. Equality holds only when some line $X - tY$ has zero variance, i.e. $X$ is an exact linear function of $Y$ — the vectors are parallel, $\rho = \pm 1$. So the boundary of correlation is precisely perfect linearity.

**Back to Maya, now with a picture.** Maya's two assets have $\sigma_1 = 0.20$ and $\sigma_2 = 0.10$, so by Cauchy–Schwarz the covariance is boxed into $\lvert\sigma_{12}\rvert \le (0.20)(0.10) = 0.02$. That is why Scenario A used $\sigma_{12} = 0.02$ exactly — it is the *most* the assets can possibly move together, $\rho = +1$, angle $0^\circ$. Her three scenarios are three angles between two arrows of length $0.20$ and $0.10$:

- **Scenario A** ($\rho = +1$, $\theta = 0^\circ$): arrows point the same way; the combined arrow is as long as it can be — maximum risk, no diversification.
- **Scenario B** ($\rho = 0$, $\theta = 90^\circ$): perpendicular arrows; the combined length obeys the Pythagorean theorem, which is *shorter* than adding the lengths — this is the free risk reduction.
- **Scenario C** ($\sigma_{12} = -0.01$, so $\rho = -0.01/0.02 = -0.5$, $\theta = 120^\circ$): arrows splay apart past a right angle; they partly cancel, and the combined arrow is shorter still.

Portfolio volatility is literally the *length of the vector sum* $w\tilde{R}_1 + (1-w)\tilde{R}_2$, and the law of cosines for that sum is identical, symbol for symbol, to the weighted variance formula of Section 2. Risk adds like vectors, not like numbers, and the angle between assets is the correlation. Diversification is just the triangle inequality doing its job.

## 5. The covariance matrix $\mathbf{\Sigma}$: bookkeeping for many assets

Two assets needed three numbers: two variances and one covariance. Maya's lender tracks thousands of loans; a real portfolio holds dozens of assets. Writing out a separate cross-term for every pair becomes hopeless prose, so we collect them into a matrix — and the matrix is not just storage, it is the object Week 2 multiplies.

**The result, in one sentence.** For a vector of random returns $\mathbf{R} = (R_1, \dots, R_K)'$, the **covariance matrix** $\mathbf{\Sigma}$ stacks every variance on the diagonal and every covariance off it, so that the variance of *any* portfolio is the single tidy expression $\mathbf{w}'\mathbf{\Sigma}\mathbf{w}$.

Define $\mathbf{\Sigma}$ entrywise by $\Sigma_{jk} = \operatorname{Cov}(R_j, R_k)$. The diagonal entries are $\Sigma_{jj} = \operatorname{Cov}(R_j, R_j) = \operatorname{Var}(R_j)$ — variances live on the diagonal, exactly as the "covariance with itself" remark from Section 2 promised. For Maya's two assets,

$$
\mathbf{\Sigma} = \begin{pmatrix} \operatorname{Var}(R_1) & \operatorname{Cov}(R_1,R_2) \\ \operatorname{Cov}(R_2,R_1) & \operatorname{Var}(R_2) \end{pmatrix} = \begin{pmatrix} 0.04 & \sigma_{12} \\ \sigma_{12} & 0.01 \end{pmatrix}.
$$

Two structural facts come along automatically, and both matter later. First, $\mathbf{\Sigma}$ is **symmetric** ($\Sigma_{jk} = \Sigma_{kj}$) because covariance is. Second, it is **positive semidefinite**: for any weight vector $\mathbf{w}$, the quadratic form $\mathbf{w}'\mathbf{\Sigma}\mathbf{w}$ equals a variance and therefore can never be negative. We can show that compactly. Using the same matrix-expectation idea you will formalize in Week 2,

$$
\mathbf{\Sigma} = \mathbb{E}\!\left[(\mathbf{R} - \mathbb{E}[\mathbf{R}])(\mathbf{R} - \mathbb{E}[\mathbf{R}])'\right],
$$

an outer product of the centered return vector with itself, averaged. A portfolio with weights $\mathbf{w}$ (summing to 1) has return $R_p = \mathbf{w}'\mathbf{R}$, and its variance unpacks as

$$
\operatorname{Var}(\mathbf{w}'\mathbf{R}) = \mathbf{w}'\mathbf{\Sigma}\,\mathbf{w} = \sum_{j=1}^{K}\sum_{k=1}^{K} w_j w_k\, \Sigma_{jk}.
$$

Check it on Maya's case with $\mathbf{w} = (w, 1-w)'$ and you recover, term for term, the weighted variance formula from Section 2 — the $w^2\Sigma_{11}$ and $(1-w)^2\Sigma_{22}$ diagonal pieces and the two equal off-diagonal pieces that combine into $2w(1-w)\sigma_{12}$. The matrix has not changed the math; it has packaged it so the same one line, $\mathbf{w}'\mathbf{\Sigma}\mathbf{w}$, works for two assets or two thousand. The positive-semidefinite property is just the statement that no portfolio can have negative variance — geometry forbidding the impossible.

**The failure mode to flag now.** If two assets are perfectly correlated (or one is a linear combination of others — say a fund that is exactly 60% of asset 1 plus 40% of asset 2), the columns of $\mathbf{\Sigma}$ become linearly dependent, the matrix is **singular**, and it has no inverse. That sounds like an abstract nuisance until Week 2, where the OLS estimator is $\hat{\boldsymbol{\beta}} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$ and $\mathbf{X}'\mathbf{X}$ is a close cousin of a covariance matrix. When regressors are perfectly collinear, that inverse does not exist and the regression cannot separate their effects — the same singular-matrix wall, met from the other side. **The covariance matrix you are building here is the very object Week 2's matrix OLS feeds on**; getting comfortable with its symmetry, its positive-semidefiniteness, and the quadratic form $\mathbf{w}'\mathbf{\Sigma}\mathbf{w}$ now means Chapter 2.1 will feel like a sequel rather than a fresh shock.

A last practical note for the notebook. We almost never know $\mathbf{\Sigma}$ exactly; we estimate it from data with the **sample covariance matrix**, and we usually look at the **correlation matrix** — $\mathbf{\Sigma}$ with each entry divided by the product of the relevant standard deviations, so the diagonal is all ones and every off-diagonal entry is a correlation in $[-1,1]$. That rescaled matrix is what a correlation heatmap draws: a grid of cosines, hot where assets move together and cool where they move apart, which is the most honest one-glance picture of where diversification can and cannot help.

## Summary

Expectation is linear and never needs independence, which makes expected portfolio return a simple weighted average. Variance and covariance are nonlinear (they involve a square), so the variance of a sum carries a cross-term $2\operatorname{Cov}(X,Y)$ — and that single term is where diversification comes from, as Maya's three scenarios showed by pushing a portfolio's volatility below its safest asset. Centering variables turns this algebra into geometry: covariance is an inner product, standard deviation is length, correlation is the cosine of the angle between two variables, "uncorrelated" means "perpendicular," and $|\rho| \le 1$ is Cauchy–Schwarz. Stacking all the pairwise covariances gives the symmetric, positive-semidefinite matrix $\mathbf{\Sigma}$, whose quadratic form $\mathbf{w}'\mathbf{\Sigma}\mathbf{w}$ is any portfolio's variance — and which is the same kind of object that Week 2's matrix OLS inverts.

## Your Turn

Open **nb1.2 — Covariance matrices & correlation heatmaps**. You will download returns for a handful of assets, build the sample covariance and correlation matrices, draw a correlation heatmap, and confirm numerically that combining low-correlation assets lowers portfolio volatility — Maya's experiment, but with real data and many assets at once.

Check questions before you start:

1. Maya considers a third weighting, $w = 0.7$ in asset 1, under Scenario C ($\sigma_{12} = -0.01$). Using the data table in Section 3, compute $\mathbb{E}[R_p]$ and $\operatorname{Var}(R_p)$ by hand. Is the portfolio still less volatile than asset 2 alone?
2. Two return series have $\operatorname{sd}(X) = 0.15$ and $\operatorname{sd}(Y) = 0.05$. A classmate reports $\operatorname{Cov}(X,Y) = 0.012$. Without any further computation, explain why that number must be wrong, and state the largest covariance these two series could possibly have.
3. Give an example of two random variables that are uncorrelated but clearly not independent, and explain in one sentence what feature of their relationship covariance fails to see. (Hint: covariance only senses straight lines.)
