# Solutions — PS 1.1 (Conditional Probability & LIE/LTV Drills)

**Problem set:** `book/weeks/week-01/ps1.1.md` (PS 1.1, Week 1).
**Chapter:** Ch 1.1 — Joint, Conditional, and the Two Laws That Run Everything.

These are full worked solutions, not just answers. Notation follows `CONVENTIONS.md`: $\mathbb{E}[\cdot]$ for expectation, $\operatorname{Var}(\cdot)$ for variance, $\operatorname{Cov}(\cdot,\cdot)$ for covariance, $p(x,y)$ for a joint pmf, $p_{X\mid Y}(x\mid y)$ for a conditional pmf. Rounding: intermediate conditional probabilities are kept exact as fractions where it helps, and final numbers are reported to three decimals.

---

## Problem 1 — Reading a joint table (14 points)

**(a) (3 pts)** A valid joint pmf needs every entry $\ge 0$ (true here) and all entries summing to $1$:
$$
0.55 + 0.05 + 0.25 + 0.15 = 1.00. \checkmark
$$
Marginals come from summing across rows (for $Y$) and down columns (for $X$):
$$
p_Y(L) = 0.55 + 0.05 = 0.60, \qquad p_Y(H) = 0.25 + 0.15 = 0.40,
$$
$$
p_X(0) = 0.55 + 0.25 = 0.80, \qquad p_X(1) = 0.05 + 0.15 = 0.20.
$$
So $60\%$ of insured homes are low-risk, and $20\%$ of all homes file a claim in a given year.

**(b) (4 pts)** Condition on $Y = H$ by dividing the high-risk row by its total $p_Y(H) = 0.40$:
$$
\Pr(X = 0 \mid Y = H) = \frac{0.25}{0.40} = 0.625, \qquad
\Pr(X = 1 \mid Y = H) = \frac{0.15}{0.40} = 0.375.
$$
These sum to $0.625 + 0.375 = 1.000$. $\checkmark$ **The claim rate among high-risk homes is $37.5\%$.**

**(c) (4 pts)** Condition on $Y = L$ by dividing the low-risk row by $p_Y(L) = 0.60$:
$$
\Pr(X = 1 \mid Y = L) = \frac{0.05}{0.60} = 0.0833\ldots \approx 0.083.
$$
The factor by which a high-risk home is more likely to claim is the ratio of the two conditional claim rates:
$$
\frac{\Pr(X=1\mid Y=H)}{\Pr(X=1\mid Y=L)} = \frac{0.375}{0.0833} = 4.5.
$$
**A high-risk home is $4.5\times$ as likely to file a claim as a low-risk home.**

**(d) (3 pts)** $X$ and $Y$ are independent iff $p(x,y) = p_X(x)\,p_Y(y)$ for *every* cell. One failing cell settles it. Test the $(X=1, Y=H)$ cell:
$$
p_X(1)\,p_Y(H) = 0.20 \times 0.40 = 0.08, \quad\text{but the actual joint is } 0.15 \neq 0.08.
$$
So **$X$ and $Y$ are dependent.** An insurer expects exactly this — if claims were independent of flood-zone rating, the rating would carry no information about risk and there would be nothing to price. Equivalently, the conditional claim rates ($37.5\%$ vs. $8.3\%$) differ from the marginal rate ($20\%$), which is the definition of dependence.

---

## Problem 2 — Maya, reverse conditioning, and a fair-lending audit (18 points)

Set up the given quantities. Let $D$ be true default ($D=1$) and $F$ the model's flag ($F=1$). We are told the *base rate* $\Pr(D=1) = 0.10$ (so $\Pr(D=0) = 0.90$) and two *forward* conditionals — flag given truth:
$$
\Pr(F=1 \mid D=1) = 0.80, \qquad \Pr(F=1 \mid D=0) = 0.15.
$$

**(a) (4 pts)** A flagged applicant is either a caught defaulter or a falsely-flagged good borrower. By the multiplication rule, $\Pr(F=1, D=d) = \Pr(F=1\mid D=d)\,\Pr(D=d)$, and summing over the two values of $D$ marginalizes $D$ away:
$$
\Pr(F=1) = \Pr(F=1\mid D=1)\Pr(D=1) + \Pr(F=1\mid D=0)\Pr(D=0)
$$
$$
= (0.80)(0.10) + (0.15)(0.90) = 0.080 + 0.135 = \boxed{0.215}.
$$
The model flags $21.5\%$ of applicants.

**(b) (6 pts)** Maya wants the *reverse* conditional $\Pr(D=1\mid F=1)$. Reverse conditioning routes through the joint and divides by the *other* margin (here $\Pr(F=1)$, which we just found):
$$
\Pr(D=1 \mid F=1) = \frac{\Pr(F=1, D=1)}{\Pr(F=1)} = \frac{\Pr(F=1\mid D=1)\Pr(D=1)}{\Pr(F=1)}
= \frac{(0.80)(0.10)}{0.215} = \frac{0.080}{0.215} = \boxed{0.372}.
$$
So only about **$37.2\%$ of flagged applicants are true defaulters.** (This is exactly Bayes' rule in table form, §2 of the chapter: the numerator is one joint cell, the denominator is the column total.)

**(c) (4 pts)** The two numbers answer different questions. $\Pr(F=1\mid D=1) = 0.80$ asks "*among true defaulters*, how many get flagged?" — it conditions on the small group ($10\%$ of the pool). $\Pr(D=1\mid F=1) = 0.372$ asks "*among the flagged*, how many truly would default?" Because defaulters are rare ($10\%$) and the false-flag rate ($15\%$) is applied to the large pool of good borrowers, the flagged group is dominated by false positives: $0.135$ of the $0.215$ flagged are good borrowers. The base rate dilutes the flag's meaning. **A denied applicant should care about $\Pr(D=1\mid F=1) = 37.2\%$** — given that *they* were flagged, the chance they would actually have defaulted is well under half, so the flag is far from a verdict.

**(d) (4 pts)** The true default rate among the *un*-flagged is, by the same reverse-conditioning move,
$$
\Pr(D=1\mid F=0) = \frac{\Pr(F=0\mid D=1)\Pr(D=1)}{\Pr(F=0)}
= \frac{(0.20)(0.10)}{0.785} = \frac{0.020}{0.785} = \boxed{0.025},
$$
where $\Pr(F=0) = 1 - 0.215 = 0.785$ and $\Pr(F=0\mid D=1) = 1 - 0.80 = 0.20$. **Comparing $0.025$ among the un-flagged to the pool's $0.10$ base rate, the flag clearly carries real information:** un-flagged applicants default at one-quarter the base rate, and flagged applicants ($37.2\%$) default at nearly four times it. The model separates the two groups even though, per (c), being flagged is not a near-certain sentence.

---

## Problem 3 — LIE proved then applied (16 points)

**(a) (8 pts)** We prove $\mathbb{E}\big[\mathbb{E}[X\mid Y]\big] = \mathbb{E}[X]$. The outer expectation averages the random variable $\mathbb{E}[X\mid Y]$ over the distribution of $Y$:
$$
\mathbb{E}\big[\mathbb{E}[X\mid Y]\big] = \sum_y \mathbb{E}[X\mid Y=y]\, p_Y(y). \tag{outer expectation over $Y$}
$$
Substitute the definition of conditional expectation:
$$
= \sum_y \left(\sum_x x\, p_{X\mid Y}(x\mid y)\right) p_Y(y). \tag{def. of $\mathbb{E}[X\mid Y=y]$}
$$
Push $p_Y(y)$ inside the inner sum (it does not depend on $x$) and apply the multiplication rule $p_{X\mid Y}(x\mid y)\,p_Y(y) = p(x,y)$:
$$
= \sum_y \sum_x x\, p_{X\mid Y}(x\mid y)\, p_Y(y) = \sum_y \sum_x x\, p(x,y). \tag{multiplication rule}
$$
Swap the order of summation (a finite double sum, so this is legal) and sum the joint over $y$ to recover the marginal of $X$:
$$
= \sum_x x \sum_y p(x,y) = \sum_x x\, p_X(x). \tag{marginalization}
$$
The last expression is the definition of $\mathbb{E}[X]$:
$$
= \mathbb{E}[X]. \qquad \blacksquare
$$
**Where finiteness is used:** the assumption that $\mathbb{E}[X]$ exists (the sums converge absolutely) is what licenses *swapping the order of summation* in the marginalization step — for a conditionally convergent double sum, reordering can change the value, so without a finite mean the manipulation is not valid. With a finite outcome set, as in every problem on this set, absolute convergence is automatic.

**(b) (8 pts)** Apply LIE with $Y$ the announcement indicator. By the same formula,
$$
\mathbb{E}[X] = \mathbb{E}[X\mid Y=1]\,\Pr(Y=1) + \mathbb{E}[X\mid Y=0]\,\Pr(Y=0)
$$
$$
= (12.0)(0.04) + (-0.25)(0.96) = 0.480 - 0.240 = \boxed{0.24\%}.
$$
**Why the unconditional mean sits so close to the boring $-0.25\%$:** in the LIE formula each conditional mean is *weighted by how often its condition occurs*. The spectacular $+12\%$ announcement day is real, but it is multiplied by its tiny probability $0.04$, so it contributes only $+0.48$ to the average. The non-announcement mean, multiplied by its near-certain weight $0.96$, dominates the blend. The mechanism is the probability weighting $p_Y(y)$ inside LIE: rare states, however dramatic, move the unconditional mean only in proportion to their frequency.

---

## Problem 4 — Sam's regimes and the Law of Total Variance (22 points)

The table (return $X \in \{-3, 0, +3\}$, regime $Y \in \{1,2\}$):

| | $-3$ | $0$ | $+3$ | row total |
|---|---|---|---|---|
| $Y=1$ (calm) | $0.04$ | $0.16$ | $0.40$ | $0.60$ |
| $Y=2$ (stormy) | $0.24$ | $0.10$ | $0.06$ | $0.40$ |

Marginals: $p_Y = (0.60, 0.40)$; column totals give $p_X(-3)=0.28$, $p_X(0)=0.26$, $p_X(+3)=0.46$.

**(a) (4 pts)** Conditional distributions divide each row by its total.

*Calm* ($\div 0.60$): $\big(\tfrac{0.04}{0.60}, \tfrac{0.16}{0.60}, \tfrac{0.40}{0.60}\big) = (0.0667, 0.2667, 0.6667)$.
$$
\mathbb{E}[X\mid Y=1] = (-3)(0.0667) + (0)(0.2667) + (3)(0.6667) = -0.200 + 2.000 = 1.800.
$$
*Stormy* ($\div 0.40$): $\big(\tfrac{0.24}{0.40}, \tfrac{0.10}{0.40}, \tfrac{0.06}{0.40}\big) = (0.60, 0.25, 0.15)$.
$$
\mathbb{E}[X\mid Y=2] = (-3)(0.60) + (0)(0.25) + (3)(0.15) = -1.800 + 0.450 = -1.350.
$$
The conditional-expectation random variable:
$$
\mathbb{E}[X\mid Y] = \begin{cases} 1.800\% & \text{w.p. } 0.60 \ (Y=1),\\[2pt] -1.350\% & \text{w.p. } 0.40 \ (Y=2). \end{cases}
$$

**(b) (5 pts)** Within-regime variances via $\operatorname{Var}(X\mid Y=y) = \mathbb{E}[X^2\mid Y=y] - (\mathbb{E}[X\mid Y=y])^2$. Note $X^2 \in \{9, 0, 9\}$.

*Calm:* $\mathbb{E}[X^2\mid Y=1] = (9)(0.0667) + (0)(0.2667) + (9)(0.6667) = 0.600 + 6.000 = 6.600$, so
$$
\operatorname{Var}(X\mid Y=1) = 6.600 - (1.800)^2 = 6.600 - 3.240 = 3.360.
$$
*Stormy:* $\mathbb{E}[X^2\mid Y=2] = (9)(0.60) + (0)(0.25) + (9)(0.15) = 5.400 + 1.350 = 6.750$, so
$$
\operatorname{Var}(X\mid Y=2) = 6.750 - (-1.350)^2 = 6.750 - 1.8225 = 4.9275.
$$
The within-regime piece is the regime-weighted average:
$$
\mathbb{E}\big[\operatorname{Var}(X\mid Y)\big] = (3.360)(0.60) + (4.9275)(0.40) = 2.016 + 1.971 = \boxed{3.987}.
$$

**(c) (4 pts)** First the overall mean, by LIE: $\mathbb{E}[X] = (1.800)(0.60) + (-1.350)(0.40) = 1.080 - 0.540 = 0.540$. Then
$$
\operatorname{Var}\big(\mathbb{E}[X\mid Y]\big) = (1.800 - 0.540)^2(0.60) + (-1.350 - 0.540)^2(0.40).
$$
Compute each term: $(1.260)^2(0.60) = 1.5876 \times 0.60 = 0.95256$ and $(-1.890)^2(0.40) = 3.5721 \times 0.40 = 1.42884$. So
$$
\operatorname{Var}\big(\mathbb{E}[X\mid Y]\big) = 0.95256 + 1.42884 = \boxed{2.3814}.
$$

**(d) (4 pts)** Add the pieces:
$$
\mathbb{E}\big[\operatorname{Var}(X\mid Y)\big] + \operatorname{Var}\big(\mathbb{E}[X\mid Y]\big) = 3.987 + 2.3814 = 6.3684.
$$
Direct check from the marginal of $X$ (probabilities $(0.28, 0.26, 0.46)$, mean $0.540$):
$$
\mathbb{E}[X^2] = (9)(0.28) + (0)(0.26) + (9)(0.46) = 2.520 + 4.140 = 6.660,
$$
$$
\operatorname{Var}(X) = 6.660 - (0.540)^2 = 6.660 - 0.2916 = 6.3684. \checkmark
$$
The two routes agree exactly: $\boxed{6.3684 = 3.987 + 2.3814}$.

**(e) (5 pts)** The across-regime share is
$$
\frac{\operatorname{Var}(\mathbb{E}[X\mid Y])}{\operatorname{Var}(X)} = \frac{2.3814}{6.3684} = 0.374 \approx 37\%.
$$
In the chapter's strategy the across-regime share was only about $19\%$; here it is nearly double, about $37\%$. **What this tells Sam:** for *this* strategy, a much larger chunk of total risk comes purely from *which regime you are in* — the conditional means ($+1.8\%$ vs. $-1.35\%$) are far apart and the regimes are close to evenly weighted. So regime forecasting is meaningfully more valuable here: perfectly anticipating calm vs. stormy would erase about $37\%$ of the variance, versus only $\sim19\%$ for the chapter's strategy. It is still not a magic bullet — the majority ($63\%$) of the wobble remains *within* regimes — but the payoff to a good calm/stormy timing signal is clearly higher for this strategy than for the chapter's.

---

## Problem 5 — Uncorrelated but dependent (18 points)

Setup: $Y \in \{-1, 0, +1\}$ each w.p. $\tfrac13$, and $X = Y^2 \in \{1, 0, 1\}$.

**(a) (3 pts)** The conditional distribution of $X$ given $Y$ is *degenerate* — $X$ is a function of $Y$, so once $Y$ is known, $X$ is certain:
$$
X\mid (Y=-1): X=1 \text{ w.p. } 1; \quad X\mid(Y=0): X=0 \text{ w.p. }1; \quad X\mid(Y=+1): X=1 \text{ w.p. }1.
$$
These conditional distributions are *not all the same* (given $Y=0$, $X$ is surely $0$; given $Y=\pm1$, $X$ is surely $1$), and they differ from the marginal of $X$. **Knowing $Y$ changes — in fact completely determines — $X$, so $X$ and $Y$ are dependent.**

**(b) (6 pts)** By symmetry $\mathbb{E}[Y] = \tfrac13(-1) + \tfrac13(0) + \tfrac13(1) = 0$. For $\mathbb{E}[XY]$, note $XY = Y^2 \cdot Y = Y^3$, and $Y^3 \in \{-1, 0, 1\}$ at the three points:
$$
\mathbb{E}[XY] = \mathbb{E}[Y^3] = \tfrac13(-1)^3 + \tfrac13(0)^3 + \tfrac13(1)^3 = \tfrac13(-1 + 0 + 1) = 0.
$$
Therefore
$$
\operatorname{Cov}(X,Y) = \mathbb{E}[XY] - \mathbb{E}[X]\,\mathbb{E}[Y] = 0 - (\mathbb{E}[X])(0) = \boxed{0}.
$$
$X$ and $Y$ are **uncorrelated**, regardless of the value of $\mathbb{E}[X]$ (which is $\tfrac23$, but it multiplies $\mathbb{E}[Y]=0$ and drops out).

**(c) (5 pts)** From part (a), $X$ is determined by $Y$, so the conditional expectation just reads off the certain value:
$$
\mathbb{E}[X\mid Y=-1] = 1, \quad \mathbb{E}[X\mid Y=0] = 0, \quad \mathbb{E}[X\mid Y=+1] = 1,
$$
i.e. $\mathbb{E}[X\mid Y] = Y^2$, which takes the value $1$ when $Y = \pm1$ and $0$ when $Y = 0$. The marginal mean is $\mathbb{E}[X] = \tfrac13(1) + \tfrac13(0) + \tfrac13(1) = \tfrac23$, a constant. **So $\mathbb{E}[X\mid Y] = Y^2 \neq \tfrac23 = \mathbb{E}[X]$ — the conditional expectation is *not* the constant marginal mean.** Hence "$\operatorname{Cov}(X,Y)=0$" and "$\mathbb{E}[X\mid Y]=\mathbb{E}[X]$" are *not* the same condition. In plain words: zero covariance only says there is no *linear* (straight-line) relationship — $Y$ does not push $X$ consistently up or down on average. But $\mathbb{E}[X\mid Y]$ here bends (it is a parabola in $Y$): $X$'s mean genuinely depends on $Y$, just in a U-shape that a single covariance number averages out to zero. The conditional mean carries information that covariance cannot see.

**(d) (4 pts)** **No.** Even if a strategy had $\operatorname{Cov}(X, Y) = 0$ between return and a regime indicator, Sam cannot conclude the regime is useless. Zero covariance rules out only a *linear* relationship; as part (c) shows, $\mathbb{E}[X\mid Y]$ can still vary with $Y$ (a nonlinear dependence), in which case the regime *does* help forecast the return even though the covariance is zero. Forecasting power lives in $\mathbb{E}[X\mid Y]$, not in $\operatorname{Cov}(X,Y)$. (For a binary regime indicator the two conditions happen to coincide, but Sam should not generalize the binary-case coincidence into a rule — the safe habit is to check the conditional means directly.)

---

## Problem 6 — Simulation design (pointing to nb1.1) (12 points)

**(a) (5 pts)** Flatten Problem 4's table into six labeled outcomes with their probabilities (summing to $1$):

| outcome $k$ | $(X, Y)$ | prob $q_k$ | cumulative $Q_k$ |
|---|---|---|---|
| 1 | $(-3, \text{calm})$ | $0.04$ | $0.04$ |
| 2 | $(0, \text{calm})$ | $0.16$ | $0.20$ |
| 3 | $(+3, \text{calm})$ | $0.40$ | $0.60$ |
| 4 | $(-3, \text{stormy})$ | $0.24$ | $0.84$ |
| 5 | $(0, \text{stormy})$ | $0.10$ | $0.94$ |
| 6 | $(+3, \text{stormy})$ | $0.06$ | $1.00$ |

Sampling rule (inverse-CDF / "roulette wheel"), repeated $N$ times independently:
1. Draw $u \sim \text{Uniform}[0,1)$.
2. Find the smallest $k$ such that $u < Q_k$ (the first cumulative bucket that $u$ falls into).
3. Record that outcome's $(X, Y)$ pair as one draw.

Because outcome $k$ is selected exactly when $Q_{k-1} \le u < Q_k$, an interval of width $q_k$, outcome $k$ is drawn with probability $q_k$ — reproducing the joint distribution. Repeat for $N$ independent draws to get a sample $\{(X_i, Y_i)\}_{i=1}^N$. (In NumPy this is one call to `rng.choice(6, size=N, p=q)` plus a lookup table, but the uniform-draw logic above is what it does under the hood.)

**(b) (4 pts)** From the simulated sample, estimate by *grouping on the realized regime* $Y_i$:
- For each regime $g \in \{\text{calm, stormy}\}$, take the subsample of days with $Y_i = g$. Compute its sample mean $\bar X_g$ (estimate of $\mathbb{E}[X\mid Y=g]$) and sample variance $\widehat{\operatorname{Var}}_g$ (estimate of $\operatorname{Var}(X\mid Y=g)$). Let $\hat p_g$ be the fraction of the sample in group $g$.
- **Within piece:** $\widehat{\mathbb{E}[\operatorname{Var}(X\mid Y)]} = \sum_g \hat p_g\, \widehat{\operatorname{Var}}_g$ (group-size-weighted average of the within-group variances).
- **Across piece:** $\widehat{\operatorname{Var}(\mathbb{E}[X\mid Y])} = \sum_g \hat p_g\,(\bar X_g - \bar X)^2$, where $\bar X$ is the overall sample mean (the size-weighted average of the $\bar X_g$).

The single equation to check is the Law of Total Variance on the sample:
$$
\widehat{\mathbb{E}[\operatorname{Var}(X\mid Y)]} + \widehat{\operatorname{Var}(\mathbb{E}[X\mid Y])} \;\approx\; \widehat{\operatorname{Var}}(X),
$$
where the right side is the overall sample variance of all $X_i$ ignoring regime. (Use the same variance convention — dividing by $N$ — on both sides so the identity holds exactly in-sample; with an $N-1$ divisor the two sides match only up to the usual finite-sample factor.)

**(c) (3 pts)** As $N$ grows from $10^2$ to $10^6$, the gap between the simulated within-plus-across sum and the exact $\operatorname{Var}(X) = 6.3684$ should *shrink toward zero*, because the sample frequencies and sample moments converge to the true probabilities and moments as the sample grows. It will essentially never be *exactly* zero at finite $N$: any finite sample carries sampling noise, so the estimates wobble around the truth rather than hitting it. The intuition is that more data averages out the randomness — the formal statement (the Law of Large Numbers, and the $1/\sqrt{N}$ rate at which the error shrinks) is the subject of Ch 1.3–1.4.
