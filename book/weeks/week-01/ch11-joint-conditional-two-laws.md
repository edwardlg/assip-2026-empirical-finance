# Ch 1.1 — Joint, Conditional, and the Two Laws That Run Everything

Almost every finding in empirical finance is, when you strip the jargon away, a statement about how one random thing behaves *once you know something else*. Does a stock's return next month depend on whether the market was calm or stormy this month? Does a borrower's default risk depend on their income? Does a portfolio's wildness depend on what "regime" the market is in? Each of these is a question about a **conditional distribution** — the distribution of one quantity given the value of another. And nearly every tool you will build over the next eight weeks — regression, causal inference, standard errors, the whole machine — is a sophisticated way of estimating a conditional expectation and then arguing about how trustworthy your estimate is.

So we start here, at the bottom of the stack. This chapter introduces joint, marginal, and conditional distributions; defines independence and conditional expectation carefully; and then proves the two identities that quietly power everything downstream: the **Law of Iterated Expectations** and the **Law of Total Variance**. We will anchor the whole thing in a problem Sam cares about — decomposing the variance of a trading portfolio's return into the part that comes from being in different market *regimes* and the part that lives *inside* each regime. By the end you will be able to look at a messy source of risk and say, precisely, "this much of the wobble is across regimes, this much is within."

We keep the algebra of variance and covariance light here on purpose. Ch 1.2 ("Expectations, Variance, Covariance as Geometry") formalizes that algebra and gives you the geometric picture — covariance as an inner product, correlation as a cosine. This chapter's job is to get conditioning and the two laws solid, with just enough expectation machinery to prove them.

---

## 1. Two random quantities at once: the joint distribution

A **random variable** is a number whose value is not yet determined — it depends on the outcome of some random experiment. We write random variables with capital letters, $X$ and $Y$, and the specific values they might take with lowercase letters, $x$ and $y$. When Sam records "yesterday's S&P 500 return" that is a value $x$; the not-yet-observed return for a random future day is the random variable $X$.

Most interesting questions involve *two* random quantities measured together. Let me make Sam's running example concrete. Sam is interested in momentum — the tendency, documented in the trading literature, for recent price moves to extend over short horizons. Sam builds a toy daily strategy and, for each trading day, records two things:

- $Y$ = the **market regime** that day, coded $1$ for a "calm" day (low volatility) and $2$ for a "stormy" day (high volatility). This is a discrete variable taking two values.
- $X$ = the **return on Sam's momentum portfolio** that day, in percent.

The **joint distribution** of $X$ and $Y$ describes how the *pair* $(X, Y)$ behaves — the probability of every combination of regime and return occurring together. To keep the arithmetic clean and the logic visible, we will first pretend $X$ is also discrete, taking only a few values; everything generalizes to continuous $X$ by replacing sums with integrals, which we will do at the end.

Suppose Sam has enough history to estimate the following table. Each cell is the **joint probability** $p(x, y) = \Pr(X = x,\, Y = y)$ — the probability that the portfolio earns return $x$ *and* the day is in regime $y$:

| | $X = -2\%$ | $X = 0\%$ | $X = +2\%$ | row total |
|---|---|---|---|---|
| **$Y = 1$ (calm)** | $0.05$ | $0.35$ | $0.30$ | $0.70$ |
| **$Y = 2$ (stormy)** | $0.15$ | $0.10$ | $0.05$ | $0.30$ |
| **column total** | $0.20$ | $0.45$ | $0.35$ | $1.00$ |

A valid joint distribution must satisfy two rules: every entry is at least zero, and all the entries sum to one. Check: the six cells add to $0.05 + 0.35 + 0.30 + 0.15 + 0.10 + 0.05 = 1.00$. Good — this is a legitimate description of a little universe.

Read the table like a map of co-occurrence. The cell in the calm row under $+2\%$ is $0.30$: on $30\%$ of all days, the market is calm *and* Sam's portfolio is up $2\%$. The cell in the stormy row under $-2\%$ is $0.15$: on $15\%$ of all days, it is stormy *and* the portfolio is down $2\%$. Already you can see the shape of the story — gains cluster in calm days, losses cluster in stormy days. The rest of this chapter is about turning that visual impression into exact statements.

### Marginals: collapsing one variable away

The numbers in the margins of the table — the row and column totals — are the **marginal distributions**. The marginal distribution of $Y$ tells you how often each regime occurs, *ignoring* the return. You get it by summing across the row, which collapses the $X$ dimension away:

$$
p_Y(y) = \sum_x p(x, y).
$$

From the row totals, $\Pr(Y = 1) = 0.70$ and $\Pr(Y = 2) = 0.30$: calm days are about twice as common as stormy ones. Likewise, the marginal distribution of $X$ comes from summing down each column, collapsing the regime away: $\Pr(X = -2\%) = 0.20$, $\Pr(X = 0\%) = 0.45$, $\Pr(X = +2\%) = 0.35$.

The word "marginal" is literal — these distributions live in the *margins* of the table, and the operation is exactly the one a 19th-century clerk did by hand to total up rows and columns. Nothing deep yet; just bookkeeping. The deep idea is the next one.

---

## 2. Conditioning: the move that makes finance possible

> **The result in one sentence.** The *conditional distribution* of $X$ given $Y = y$ is what the table tells you about $X$ once you restrict attention to a single row and rescale it back up to a valid distribution.

**Intuition.** A marginal distribution answers "what does a random day look like?" A conditional distribution answers a sharper question: "given that today is *stormy*, what does the portfolio return look like?" That second question is the one a trader, a lender, or a risk manager actually asks. You almost never get to act on the unconditional average; you act on what you know *right now*. Conditioning is the mathematical name for "using what you know."

Here is the mechanics. To condition on $Y = 2$ (stormy), walk into the stormy row of the table:

$$
\Pr(X = -2\%,\, Y = 2) = 0.15, \quad \Pr(X = 0\%,\, Y = 2) = 0.10, \quad \Pr(X = +2\%,\, Y = 2) = 0.05.
$$

Those three numbers describe what happens on stormy days, but they only add to $0.30$, not $1$ — because stormy days are only $30\%$ of all days. To turn them into a proper probability distribution *over the stormy world*, divide each by that row total $0.30$. That gives the **conditional distribution of $X$ given $Y = 2$**:

$$
p_{X\mid Y}(x \mid y) = \frac{p(x, y)}{p_Y(y)}, \qquad \text{valid whenever } p_Y(y) > 0.
$$

Doing the division for the stormy row:

$$
\Pr(X = -2\% \mid Y = 2) = \frac{0.15}{0.30} = 0.50, \quad
\Pr(X = 0\% \mid Y = 2) = \frac{0.10}{0.30} \approx 0.333, \quad
\Pr(X = +2\% \mid Y = 2) = \frac{0.05}{0.30} \approx 0.167.
$$

These three now sum to $1$: a clean distribution describing the portfolio's behavior *on the subset of days that are stormy*. Repeat for the calm row, dividing by $0.70$:

$$
\Pr(X = -2\% \mid Y = 1) = \frac{0.05}{0.70} \approx 0.071, \quad
\Pr(X = 0\% \mid Y = 1) = \frac{0.35}{0.70} = 0.50, \quad
\Pr(X = +2\% \mid Y = 1) \approx 0.429.
$$

Look at what conditioning revealed. Unconditionally, the portfolio is up $2\%$ about $35\%$ of the time. But *given a calm day*, it is up $2\%$ about $43\%$ of the time, and *given a stormy day*, only $17\%$ of the time. The regime genuinely shifts the return distribution — that is the empirical content of "momentum behaves differently across volatility regimes," stated as a precise comparison of two conditional distributions. The general definition $p_{X\mid Y}(x\mid y) = p(x,y)/p_Y(y)$ rearranges into the **multiplication rule** $p(x, y) = p_{X\mid Y}(x\mid y)\, p_Y(y)$, which we will lean on constantly: a joint probability is "probability of the condition, times probability of the outcome given the condition."

### Conditioning runs both directions

Notice that we conditioned $X$ on $Y$ — return given regime — because that matched Sam's decision problem: see the regime, forecast the return. But the same table answers the *reverse* question, and the reverse is often the one a risk manager wants. Suppose Sam observes a bad day, $X = -2\%$, and asks: *how likely is it that the market was actually in the stormy regime?* That is $\Pr(Y = 2 \mid X = -2\%)$, conditioning $Y$ on $X$ — reading *up a column* of the table rather than *across a row*. The recipe is identical: take the joint cell and divide by the relevant total, except now the relevant total is the *column* total. From the table, $\Pr(X = -2\%) = 0.20$, so

$$
\Pr(Y = 2 \mid X = -2\%) = \frac{\Pr(X = -2\%,\, Y = 2)}{\Pr(X = -2\%)} = \frac{0.15}{0.20} = 0.75.
$$

Three-quarters of Sam's $-2\%$ days are stormy days, even though stormy days are only $30\%$ of all days overall. Conditioning on the bad return *updated* Sam's belief about the regime, from a baseline $30\%$ up to $75\%$. This flip — going from $\Pr(X \mid Y)$ to $\Pr(Y \mid X)$ by rerouting through the joint — is exactly **Bayes' rule** in table form, and it is the same logic a fraud model, a default model, or a medical test uses to turn "probability of the symptom given the disease" into "probability of the disease given the symptom." We will not formalize Bayes here, but keep the two-way symmetry in mind: a single joint distribution contains the answer to the question *and* its converse, and which one you call "the conditional" is just a matter of what you happened to observe first.

**When it fails.** The definition divides by $p_Y(y)$, so it is silent when $p_Y(y) = 0$ — you cannot condition on an event that never happens. For discrete $Y$ this is a harmless edge case. For *continuous* $Y$, though, every single value has probability zero, so the naïve ratio is $0/0$ and the definition needs to be rebuilt with densities (we do this in §6). Keep this in the back of your mind: "condition on $Y = y$" is doing real work that is easy to take for granted.

---

## 3. Independence: when knowing one tells you nothing

> **The result in one sentence.** $X$ and $Y$ are *independent* when conditioning on $Y$ does not change the distribution of $X$ at all.

**Intuition.** Independence is the special case where the conditioning move from §2 is a no-op. If learning the regime tells you nothing about the return — the calm-day return distribution is identical to the stormy-day one — then $X$ and $Y$ are independent. Formally, $X$ and $Y$ are **independent** if their joint distribution factors into the product of the marginals for every pair of values:

$$
p(x, y) = p_X(x)\, p_Y(y) \quad \text{for all } x, y.
$$

Equivalently, $p_{X\mid Y}(x\mid y) = p_X(x)$: the conditional equals the marginal, so conditioning teaches you nothing.

**Worked check.** Are Sam's $X$ and $Y$ independent? Test the easiest cell. If they were independent, the calm/$+2\%$ cell would have to equal $p_X(+2\%)\, p_Y(1) = 0.35 \times 0.70 = 0.245$. The actual joint probability is $0.30 \neq 0.245$. One failing cell is enough: regime and return are **dependent**. That is the whole point of Sam's strategy — if returns were independent of the regime, there would be nothing for a regime-aware trader to exploit.

**When it fails — the subtle trap.** Independence is strictly stronger than "uncorrelated." Two variables can have zero covariance yet still be dependent, because covariance only detects *linear* association. Picture a variable $Y$ that is equally likely to be $-1, 0, +1$, and set $X = Y^2$. Knowing $Y$ pins down $X$ exactly — they are about as dependent as two variables can be — yet a quick calculation gives $\operatorname{Cov}(X, Y) = 0$ because the relationship is symmetric and bends rather than slopes. So "uncorrelated" never licenses you to assume "independent." Ch 1.2 makes covariance precise; for now, hold onto the warning, because conflating the two is one of the most common analytical errors in applied work.

---

## 4. Conditional expectation: the single most useful object in the course

We now combine conditioning with averaging. First, recall the **expectation** (or **mean**) of a discrete random variable — its probability-weighted average value:

$$
\mathbb{E}[X] = \sum_x x\, p_X(x).
$$

For Sam's portfolio, the unconditional expected daily return is

$$
\mathbb{E}[X] = (-2)(0.20) + (0)(0.45) + (2)(0.35) = -0.40 + 0 + 0.70 = 0.30\%.
$$

On an average day, Sam's strategy earns $0.30\%$. Fine — but Sam never trades on "an average day." Sam wakes up and *sees the regime*. So the relevant object is the **conditional expectation** of $X$ given $Y = y$: the mean of $X$ computed inside the conditional distribution from §2,

$$
\mathbb{E}[X \mid Y = y] = \sum_x x\, p_{X\mid Y}(x \mid y).
$$

Compute it in each regime. On calm days,

$$
\mathbb{E}[X \mid Y = 1] = (-2)(0.071) + (0)(0.50) + (2)(0.429) = -0.143 + 0 + 0.857 = 0.714\%.
$$

On stormy days,

$$
\mathbb{E}[X \mid Y = 2] = (-2)(0.50) + (0)(0.333) + (2)(0.167) = -1.00 + 0 + 0.333 = -0.667\%.
$$

This is a real finding stated cleanly: Sam's momentum strategy earns about $+0.71\%$ on a calm day and *loses* about $0.67\%$ on a stormy day. The single unconditional number $0.30\%$ was a blend that hid two opposite stories.

### Conditional expectation is itself a random variable

Here is the conceptual jump that everything later depends on, so slow down for it. We just computed *two* numbers, one per regime. But the regime $Y$ is itself random — before the day starts, Sam does not know which it will be. So the quantity "the expected return *for whatever regime today turns out to be*" is not a fixed number; it is a random variable. We call it $\mathbb{E}[X \mid Y]$ — note: conditioning on the random variable $Y$, not on a specific value $y$.

Concretely, $\mathbb{E}[X \mid Y]$ is the function that outputs $0.714\%$ when $Y = 1$ and $-0.667\%$ when $Y = 2$. Since $Y = 1$ with probability $0.70$ and $Y = 2$ with probability $0.30$, the random variable $\mathbb{E}[X\mid Y]$ takes:

$$
\mathbb{E}[X \mid Y] = \begin{cases} 0.714\% & \text{with probability } 0.70, \\[2pt] -0.667\% & \text{with probability } 0.30. \end{cases}
$$

It is a random variable that is a *function of $Y$ alone* — once you know the regime, you know its value. That is the precise sense in which $\mathbb{E}[X\mid Y]$ is "the best forecast of $X$ you can make using only $Y$." This object — the conditional expectation function — is, quite literally, what regression estimates. Hold that thought all the way to Week 2.

---

## 5. The first law: Iterated Expectations

> **The result in one sentence.** The average of the conditional averages, weighted by how often each condition occurs, equals the overall average: $\mathbb{E}[X] = \mathbb{E}\big[\mathbb{E}[X \mid Y]\big]$.

This is the **Law of Iterated Expectations** (LIE), sometimes called the tower property. The inner $\mathbb{E}[X\mid Y]$ is the random variable from §4; the outer $\mathbb{E}[\cdot]$ averages it over the distribution of $Y$.

**Intuition.** You can compute an overall average in two stages: first average within each group, then average those group-averages, weighting each group by its size. A school's average test score equals the enrollment-weighted average of its classrooms' average scores. Sam's overall expected return equals the regime-frequency-weighted average of the per-regime expected returns. The law says these two routes always land on the same number — splitting into groups and recombining loses nothing.

**Worked example.** Take the conditional means from §4 and average them over the regime frequencies:

$$
\mathbb{E}\big[\mathbb{E}[X\mid Y]\big] = (0.714\%)(0.70) + (-0.667\%)(0.30) = 0.500\% - 0.200\% = 0.30\%.
$$

That is exactly the $\mathbb{E}[X] = 0.30\%$ we got in §4 the direct way. The two-stage route and the one-stage route agree, to the penny. Not a coincidence — a theorem.

**The algebra.** The proof is three honest lines. Start from the outer expectation, written as a sum over the values of $Y$, then substitute the definition of conditional expectation, then use the multiplication rule $p(x,y) = p_{X\mid Y}(x\mid y)\,p_Y(y)$:

$$
\mathbb{E}\big[\mathbb{E}[X\mid Y]\big]
= \sum_y \mathbb{E}[X\mid Y = y]\, p_Y(y)
= \sum_y \Big(\sum_x x\, p_{X\mid Y}(x\mid y)\Big) p_Y(y).
$$

Push $p_Y(y)$ inside the inner sum, and the product $p_{X\mid Y}(x\mid y)\,p_Y(y)$ collapses to the joint $p(x,y)$:

$$
= \sum_y \sum_x x\, \underbrace{p_{X\mid Y}(x\mid y)\, p_Y(y)}_{=\,p(x,y)}
= \sum_x x \sum_y p(x, y)
= \sum_x x\, p_X(x)
= \mathbb{E}[X].
$$

The last step summed the joint over $y$ to recover the marginal $p_X(x)$ — the marginalization move from §1. That is the entire proof: conditioning splits the sum into groups; iterating expectations puts the groups back together.

**Why you will use this constantly.** LIE is the formal license for the single most common phrase in econometrics: "control for $Y$." When you compute an average *within* groups and then ask what it implies on average, LIE guarantees you have not accidentally changed the overall mean. It is also the engine behind regression's claim to estimate $\mathbb{E}[X\mid Y]$, behind the "no omitted-variable bias" arguments of Week 2, and behind the causal-identification logic of Weeks 3–4. A surprising number of proofs in this book are "apply LIE, then simplify."

**When it fails.** LIE is essentially always true — *provided $\mathbb{E}[X]$ exists in the first place.* The catch is that for sufficiently heavy-tailed variables the expectation can be infinite or undefined, and then there is no finite number for the two routes to agree on. You will meet exactly this pathology in Ch 1.4, when Devon's crypto returns have tails heavy enough to threaten the Law of Large Numbers. For any variable with a finite mean — every example in this chapter — LIE holds with no further assumptions.

---

## 6. The continuous case, briefly

Everything above survives the jump to continuous variables; you only swap probability mass functions for **probability density functions** and sums for integrals. If $X$ and $Y$ have a joint density $f(x, y)$, the marginal density of $Y$ is $f_Y(y) = \int f(x, y)\, dx$, and the conditional density is

$$
f_{X\mid Y}(x \mid y) = \frac{f(x, y)}{f_Y(y)}, \qquad f_Y(y) > 0.
$$

The conditional expectation becomes $\mathbb{E}[X \mid Y = y] = \int x\, f_{X\mid Y}(x\mid y)\, dx$, and the Law of Iterated Expectations reads identically, $\mathbb{E}[X] = \mathbb{E}\big[\mathbb{E}[X\mid Y]\big]$, with the same three-line proof and integrals in place of sums. The one genuinely new subtlety is the §2 warning: a continuous $Y$ has $\Pr(Y = y) = 0$ for every $y$, so "conditioning on $Y = y$" is defined through densities, not by literally restricting to an event of positive probability. The intuition — "look at the slice of the world where $Y = y$, then average $X$ over that slice" — is exactly right; the machinery just has to be built with densities to be rigorous. We will use the discrete picture for the rest of this chapter because the arithmetic stays visible.

---

## 7. The second law: Total Variance — Sam's risk decomposition

Now we get to the result Sam actually wants. A trader does not only care about the *average* return; the trader cares about the *risk* — the variance of returns — and, crucially, *where the risk comes from*. The **Law of Total Variance** (LTV) answers exactly that.

First, the **variance** of a random variable measures how spread out it is around its mean:

$$
\operatorname{Var}(X) = \mathbb{E}\big[(X - \mathbb{E}[X])^2\big] = \mathbb{E}[X^2] - \big(\mathbb{E}[X]\big)^2.
$$

The second form ("mean of the square minus square of the mean") is the one we compute with.

> **The result in one sentence.** Total variance splits cleanly into the average variance *inside* the groups plus the variance *across* the group means:
> $$\operatorname{Var}(X) = \underbrace{\mathbb{E}\big[\operatorname{Var}(X\mid Y)\big]}_{\text{within-regime risk}} + \underbrace{\operatorname{Var}\big(\mathbb{E}[X\mid Y]\big)}_{\text{across-regime risk}}.$$

**Intuition.** The portfolio bounces around for two distinct reasons. First, *within* any given regime, returns still vary day to day — even among calm days, some are up $2\%$ and some down $2\%$. That is the within-regime piece, $\mathbb{E}[\operatorname{Var}(X\mid Y)]$: the average, over regimes, of the day-to-day variance inside each regime. Second, the regimes themselves have *different average returns* ($+0.71\%$ vs. $-0.67\%$), so just by switching regimes the portfolio's center of gravity moves. That is the across-regime piece, $\operatorname{Var}(\mathbb{E}[X\mid Y])$: the variance of the conditional means. LTV says total risk is exactly the sum of "risk you'd still face if you knew the regime" plus "risk that comes purely from not knowing which regime you're in." Nothing is double-counted; nothing leaks.

This is genuinely useful to Sam. If the across-regime piece dominates, the smart move is regime forecasting — predict the storm and you have killed most of the variance. If the within-regime piece dominates, knowing the regime barely helps, and Sam needs a different edge. The decomposition tells Sam *which kind of problem they have*.

### Worked example: doing the decomposition

We need three ingredients, all already partly computed.

**Step 1 — within-regime variances.** Compute $\operatorname{Var}(X\mid Y = y)$ in each regime using $\mathbb{E}[X^2\mid Y=y] - (\mathbb{E}[X\mid Y=y])^2$.

*Calm ($Y=1$),* with conditional probabilities $(0.071, 0.50, 0.429)$ on $(-2, 0, 2)$ and conditional mean $0.714$:

$$
\mathbb{E}[X^2 \mid Y=1] = (4)(0.071) + (0)(0.50) + (4)(0.429) = 0.286 + 1.714 = 2.000,
$$
$$
\operatorname{Var}(X \mid Y=1) = 2.000 - (0.714)^2 = 2.000 - 0.510 = 1.490.
$$

*Stormy ($Y=2$),* with conditional probabilities $(0.50, 0.333, 0.167)$ and conditional mean $-0.667$:

$$
\mathbb{E}[X^2 \mid Y=2] = (4)(0.50) + (0)(0.333) + (4)(0.167) = 2.000 + 0.667 = 2.667,
$$
$$
\operatorname{Var}(X \mid Y=2) = 2.667 - (-0.667)^2 = 2.667 - 0.444 = 2.222.
$$

**Step 2 — the within-regime piece** is the regime-weighted average of those two variances:

$$
\mathbb{E}\big[\operatorname{Var}(X\mid Y)\big] = (1.490)(0.70) + (2.222)(0.30) = 1.043 + 0.667 = 1.710.
$$

**Step 3 — the across-regime piece** is the variance of the conditional-mean random variable $\mathbb{E}[X\mid Y]$, which takes value $0.714$ w.p. $0.70$ and $-0.667$ w.p. $0.30$. Its overall mean is $\mathbb{E}[X] = 0.30$ (we proved this with LIE in §5), so

$$
\operatorname{Var}\big(\mathbb{E}[X\mid Y]\big) = (0.714 - 0.30)^2(0.70) + (-0.667 - 0.30)^2(0.30).
$$

Computing each term: $(0.414)^2(0.70) = 0.171\times0.70 = 0.120$ and $(-0.967)^2(0.30) = 0.935\times0.30 = 0.280$, so

$$
\operatorname{Var}\big(\mathbb{E}[X\mid Y]\big) = 0.120 + 0.280 = 0.400.
$$

**Add them up:**

$$
\mathbb{E}\big[\operatorname{Var}(X\mid Y)\big] + \operatorname{Var}\big(\mathbb{E}[X\mid Y]\big) = 1.710 + 0.400 = 2.110.
$$

**Check against the direct calculation.** Compute $\operatorname{Var}(X)$ from the marginal of $X$ — probabilities $(0.20, 0.45, 0.35)$ on $(-2, 0, 2)$, with mean $0.30$:

$$
\mathbb{E}[X^2] = (4)(0.20) + (0)(0.45) + (4)(0.35) = 0.80 + 1.40 = 2.200,
$$
$$
\operatorname{Var}(X) = 2.200 - (0.30)^2 = 2.200 - 0.090 = 2.110.
$$

It matches: $2.110 = 1.710 + 0.400$. The decomposition is exact.

**The code.** The whole decomposition is a few lines once you treat the table as data. The snippet below builds Sam's joint distribution, computes the conditional means and variances by grouping on the regime, and verifies $\mathbb{E}[\operatorname{Var}(X\mid Y)] + \operatorname{Var}(\mathbb{E}[X\mid Y]) = \operatorname{Var}(X)$ exactly — no simulation noise, because we are working with the true probabilities rather than a sample.

```python
import numpy as np

# Sam's universe: return values (in %) and the joint probability table.
x_vals = np.array([-2.0, 0.0, 2.0])
# rows = regime (0: calm, 1: stormy); columns = return value
joint = np.array([[0.05, 0.35, 0.30],    # calm
                  [0.15, 0.10, 0.05]])   # stormy

p_y = joint.sum(axis=1)                   # marginal of Y (regime): [0.70, 0.30]
p_x = joint.sum(axis=0)                   # marginal of X (return): [0.20, 0.45, 0.35]

# Conditional distribution of X within each regime: divide each row by its total.
p_x_given_y = joint / p_y[:, None]

# Conditional mean and variance of X in each regime.
cond_mean = (p_x_given_y * x_vals).sum(axis=1)                       # E[X | Y]
cond_var  = (p_x_given_y * (x_vals - cond_mean[:, None])**2).sum(1)  # Var(X | Y)

# The two LTV pieces, each averaged/varied over the regime distribution p_y.
within  = (p_y * cond_var).sum()                                    # E[Var(X|Y)]
mean_X  = (p_y * cond_mean).sum()                                   # E[X] via LIE
across  = (p_y * (cond_mean - mean_X)**2).sum()                     # Var(E[X|Y])

# Direct total variance from the marginal of X.
var_X = (p_x * (x_vals - mean_X)**2).sum()

print(f"E[X]                = {mean_X:.3f}")          # 0.300
print(f"within  E[Var(X|Y)] = {within:.3f}")         # 1.710
print(f"across  Var(E[X|Y]) = {across:.3f}")         # 0.400
print(f"within + across     = {within + across:.3f}")# 2.110
print(f"Var(X) direct       = {var_X:.3f}")          # 2.110
assert np.isclose(within + across, var_X)            # the law, checked
```

The notebook `nb1.1` takes this one step further: instead of the exact table it *draws* samples from this joint distribution and shows the grouped estimates converging to these numbers as the sample grows — which is the bridge to the sampling-distribution ideas of Ch 1.3.

**Reading the answer.** Of Sam's total daily return variance ($2.110$), the within-regime risk is $1.710$ — about $81\%$ — and the across-regime risk is only $0.400$, about $19\%$. The blunt takeaway: even if Sam could perfectly forecast tomorrow's regime, only about a fifth of the portfolio's variance would go away. Most of the wobble is *inside* the regimes, not *between* them. A regime-timing overlay alone will not tame this strategy; Sam needs an edge that works within regimes too. That single sentence — actionable, quantitative, defensible — is what the Law of Total Variance buys you.

### The algebra

The proof is just LIE applied twice plus the definition of variance. Start from the definition of each piece. The across-regime term, using $\operatorname{Var}(Z) = \mathbb{E}[Z^2] - (\mathbb{E}[Z])^2$ on $Z = \mathbb{E}[X\mid Y]$ and noting $\mathbb{E}\big[\mathbb{E}[X\mid Y]\big] = \mathbb{E}[X]$ by LIE:

$$
\operatorname{Var}\big(\mathbb{E}[X\mid Y]\big) = \mathbb{E}\Big[\big(\mathbb{E}[X\mid Y]\big)^2\Big] - \big(\mathbb{E}[X]\big)^2.
$$

The within-regime term, using $\operatorname{Var}(X\mid Y) = \mathbb{E}[X^2\mid Y] - \big(\mathbb{E}[X\mid Y]\big)^2$ inside an outer expectation, and LIE again to turn $\mathbb{E}\big[\mathbb{E}[X^2\mid Y]\big]$ into $\mathbb{E}[X^2]$:

$$
\mathbb{E}\big[\operatorname{Var}(X\mid Y)\big] = \mathbb{E}\big[\mathbb{E}[X^2\mid Y]\big] - \mathbb{E}\Big[\big(\mathbb{E}[X\mid Y]\big)^2\Big] = \mathbb{E}[X^2] - \mathbb{E}\Big[\big(\mathbb{E}[X\mid Y]\big)^2\Big].
$$

Now add the two terms. The middle quantity $\mathbb{E}\big[(\mathbb{E}[X\mid Y])^2\big]$ appears once with a plus and once with a minus and cancels exactly:

$$
\mathbb{E}\big[\operatorname{Var}(X\mid Y)\big] + \operatorname{Var}\big(\mathbb{E}[X\mid Y]\big) = \mathbb{E}[X^2] - \big(\mathbb{E}[X]\big)^2 = \operatorname{Var}(X). \qquad \blacksquare
$$

That cancellation *is* the law. The within piece "gives up" the term $\mathbb{E}[(\mathbb{E}[X\mid Y])^2]$ and the across piece "claims" it; together they reconstruct the total variance with nothing left over.

**When it fails — and a warning about interpretation.** Mechanically, LTV is an identity: it holds for any $X$ with finite variance, full stop. It cannot fail as algebra. Where people go wrong is in *interpretation*. First, the same finiteness caveat as LIE — if $\operatorname{Var}(X)$ is infinite (heavy tails again, Ch 1.4), there is nothing finite to decompose. Second, and more insidious: the decomposition is only as meaningful as your choice of conditioning variable $Y$. If Sam's two-bucket "calm/stormy" coding is too coarse — if there are really five regimes, not two — then variation that is genuinely *across* finer regimes gets misfiled as *within*-regime noise, and the $81\%$ figure overstates how irreducible the risk really is. The math is always exact; the *story* it tells depends entirely on whether $Y$ carves the world at its real joints. Choosing $Y$ well is a modeling decision, not a theorem, and it is where empirical judgment lives.

---

## 8. Why these two laws run everything

Step back and look at what you now have. Conditioning is the act of using information. The conditional expectation $\mathbb{E}[X\mid Y]$ is the best forecast of $X$ from $Y$, and it is a random variable in its own right — the very object regression will estimate. The Law of Iterated Expectations says you can build up an overall average from conditional averages without distortion, which is the backbone of every "control for $Y$" argument you will make for the rest of the program. The Law of Total Variance says risk splits cleanly into a within-group part and an across-group part, which is how you reason about *where* uncertainty comes from — and, in Week 2, how you will understand what a regression's residual variance is actually measuring.

These are not isolated tricks. They are the two structural identities that let you decompose a complicated random quantity along the lines of something you know, and put it back together with a guarantee that nothing was lost. Every later chapter is, in some sense, a special case or an application. Ch 1.2 takes the next step: it formalizes expectation, variance, and covariance as *geometry* — expectation as a kind of projection, covariance as an inner product, correlation as the cosine of an angle — which will turn the algebra you saw flickering through these proofs into pictures you can reason with directly.

---

## Your Turn

Open **`notebooks/week-01/nb1.1`** ("LIE/LTV by simulation"). There you will rebuild Sam's regime table as a NumPy simulation: draw a few hundred thousand $(X, Y)$ pairs from the joint distribution, estimate the conditional means and variances by simple grouping (`groupby` on the regime), and watch the simulated within-plus-across sum converge to the directly computed $\operatorname{Var}(X) = 2.110$ as the sample grows. You will also run the "Your Turn" extension: refine the two-regime coding into a finer grid and see for yourself how the within/across split shifts — the §7 warning made concrete.

**Check your understanding** (full set in PS 1.1):

1. Using Sam's table, compute $\Pr(Y = 2 \mid X = -2\%)$ — the probability the day was stormy *given* the portfolio lost $2\%$. (Hint: this reverses the conditioning direction of §2; you are reading *up* a column instead of *across* a row.)
2. Suppose Sam discovers a third regime, "transition" days, and re-estimates the table. Without recomputing anything, explain what must happen to the across-regime variance term $\operatorname{Var}(\mathbb{E}[X\mid Y])$ if the new regime has a conditional mean return that differs from the existing two — does the term go up, down, or is it ambiguous? Why?
3. True or false, with a one-line reason: "If $\operatorname{Cov}(X, Y) = 0$, then knowing the regime $Y$ cannot help Sam forecast the return $X$." (Re-read §3 before answering.)
