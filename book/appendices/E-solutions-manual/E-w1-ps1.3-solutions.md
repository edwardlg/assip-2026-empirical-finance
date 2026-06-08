# Solutions — Problem Set 1.3 (Bias, Variance, and MSE of Estimators)

*Full worked solutions to `book/weeks/week-01/ps1.3.md`. Notation follows `CONVENTIONS.md`:
$\mu = \mathbb{E}[x_i]$, $\sigma^2 = \operatorname{Var}(x_i)$, $\bar{x} = \frac{1}{N}\sum_i x_i$,
$\xrightarrow{p}$ = convergence in probability. Methods are restricted to Chapter 1.3 and
earlier; LLN/CLT are invoked intuitively only.*

---

## Problem 1 — Unbiasedness of the sample mean (12 pts)

**(a) [4 pts]** By definition,
$$
\mathbb{E}[\bar{x}] = \mathbb{E}\!\left[\frac{1}{N}\sum_{i=1}^N x_i\right]
= \frac{1}{N}\sum_{i=1}^N \mathbb{E}[x_i]
= \frac{1}{N}\sum_{i=1}^N \mu
= \frac{1}{N}\cdot N\mu = \mu .
$$
Step 1 uses that expectation passes through a constant multiple ($\tfrac1N$ comes out) and
through a sum (**linearity of expectation**); step 2 uses the modeling **assumption that every
$x_i$ has the same mean $\mu$**, i.e. all observations are drawn from the target population.
Since $\mathbb{E}[\bar{x}] = \mu$, the bias is $\mathbb{E}[\bar{x}] - \mu = 0$: the sample mean
is unbiased.

Note that independence was *not* needed for unbiasedness — only that each $x_i$ has mean $\mu$.
Independence will matter for the variance (Problem 2), not here.

**(b) [3 pts]** No. The estimate is not biased. Unbiasedness, $\mathbb{E}[\bar{x}] = \mu$, holds
for *every* sample size including $N = 6$ — the proof in (a) never used a large $N$. What is true
at $N = 6$ is that the estimate has a large **variance** ($\sigma^2/6$), so any one estimate may
sit far from $\mu$ by chance; but that is *sampling error*, the unavoidable luck of one draw, not
*bias*, which is a systematic miss of the recipe averaged over all draws. The classmate has
confused a noisy estimate with a crooked one.

**(c) [5 pts]** Let $\pi N$ drivers be the over-sampled metro (mean $\mu + \delta$) and
$(1-\pi)N$ be the rest (mean $\mu$). Then
$$
\mathbb{E}[\bar{x}] = \frac{1}{N}\Big[ \pi N(\mu + \delta) + (1-\pi)N\,\mu \Big]
= \pi(\mu + \delta) + (1-\pi)\mu = \mu + \pi\delta .
$$
The bias is $\mathbb{E}[\bar{x}] - \mu = \pi\delta > 0$: $\bar{x}$ aims **high** by $\pi\delta$.
Collecting more drivers the same way does **not** fix it — the bias $\pi\delta$ does not depend
on $N$, so more data drives $\bar{x}$ confidently toward the wrong number $\mu + \pi\delta$. This
is the "garbage in, garbage in" warning: the math is fine, the *sampling assumption* is broken.

---

## Problem 2 — $\operatorname{Var}(\bar{x}) = \sigma^2/N$ and the price of precision (15 pts)

**(a) [6 pts]** Write $\bar{x} = \frac{1}{N}S$ where $S = \sum_{i=1}^N x_i$. For any constant $a$,
$\operatorname{Var}(aZ) = a^2\operatorname{Var}(Z)$ (pulling a constant out of a variance squares
it, because variance is defined through squared deviations). With $a = 1/N$:
$$
\operatorname{Var}(\bar{x}) = \operatorname{Var}\!\Big(\tfrac{1}{N}S\Big)
= \frac{1}{N^2}\operatorname{Var}(S) .
$$
By independence, the variance of the sum is the sum of the variances (no covariance cross-terms):
$\operatorname{Var}(S) = \sum_{i=1}^N \operatorname{Var}(x_i) = N\sigma^2$. Therefore
$$
\operatorname{Var}(\bar{x}) = \frac{1}{N^2}\cdot N\sigma^2 = \frac{\sigma^2}{N}.
$$
The $1/N^2$ is the $(1/N)^2$ from squaring the constant; one factor of $N$ is then eaten by the
$N$ terms in the sum, leaving $\sigma^2/N$.

**(b) [3 pts]** $\operatorname{se}(\bar{x}) = \sqrt{\sigma^2/N} = \sigma/\sqrt{N}$.
With $\sigma = 240$:
$$
N = 6: \quad \frac{240}{\sqrt{6}} = \frac{240}{2.449} \approx \$98.0 ; \qquad
N = 600: \quad \frac{240}{\sqrt{600}} = \frac{240}{24.49} \approx \$9.80 .
$$

**(c) [4 pts]** Require $\sigma/\sqrt{N} \le 10$, i.e. $\sqrt{N} \ge \sigma/10 = 24$, so
$N \ge 24^2 = 576$. The smallest integer is $\boxed{N = 576}$.
(Check: $240/\sqrt{576} = 240/24 = \$10$ exactly.)

**(d) [2 pts]** Since $\operatorname{se} \propto 1/\sqrt{N}$, halving the standard error requires
$\sqrt{N}$ to **double**, i.e. multiplying $N$ by $\mathbf{4}$. To cut wobble in half you must
*quadruple* the data — the $1/\sqrt{N}$ tax: precision gets expensive at a fixed, punishing rate
because the square root, not $N$ itself, governs the standard error.

---

## Problem 3 — Bias–variance–MSE for two recipes (20 pts)

Throughout, recall $\mathbb{E}[\bar{x}] = \mu$ and $\operatorname{Var}(\bar{x}) = \sigma^2/N$.

**(a) [4 pts]** $\hat{\mu}_A = \bar{x}$ is unbiased (Problem 1a), so $\operatorname{Bias}_A = 0$
and
$$
\operatorname{MSE}(\hat{\mu}_A) = \operatorname{Var}(\bar{x}) + 0^2 = \frac{\sigma^2}{N}.
$$

**(b) [5 pts]** $\hat{\mu}_B = c\,\bar{x}$ is a constant times $\bar{x}$, so
$$
\mathbb{E}[\hat{\mu}_B] = c\,\mathbb{E}[\bar{x}] = c\mu,
\qquad
\operatorname{Bias}(\hat{\mu}_B) = c\mu - \mu = (c-1)\mu,
$$
$$
\operatorname{Var}(\hat{\mu}_B) = c^2\operatorname{Var}(\bar{x}) = \frac{c^2\sigma^2}{N}.
$$
Since $0 < c < 1$ the bias is $(c-1)\mu$, which is nonzero whenever $\mu \neq 0$, and the
variance is *smaller* than A's by the factor $c^2$.

**(c) [5 pts]**
$$
\operatorname{MSE}(\hat{\mu}_B) = \operatorname{Var}(\hat{\mu}_B) + \operatorname{Bias}(\hat{\mu}_B)^2
= \frac{c^2\sigma^2}{N} + (c-1)^2\mu^2 .
$$
At $c = 1$: the second term vanishes and the first becomes $\sigma^2/N$, recovering
$\operatorname{MSE}(\hat{\mu}_A)$. Good — B nests A.

**(d) [6 pts]** We want a $c \in (0,1)$ with
$$
\frac{c^2\sigma^2}{N} + (c-1)^2\mu^2 < \frac{\sigma^2}{N}.
$$

*Easiest demonstration (take $\mu = 0$).* If the true mean is exactly $0$, the bias term
$(c-1)^2\mu^2 = 0$ for any $c$, and the inequality becomes $c^2\sigma^2/N < \sigma^2/N$, i.e.
$c^2 < 1$, which holds for *every* $c \in (0,1)$. So shrinking strictly lowers MSE here. This is
the cleanest case: when the truth is the shrink target, you pay no bias and pocket all the
variance reduction.

*General demonstration (any $\mu$, $c$ just below 1).* Define
$g(c) = \frac{c^2\sigma^2}{N} + (c-1)^2\mu^2$, so $g(1) = \sigma^2/N = \operatorname{MSE}_A$.
Differentiate:
$$
g'(c) = \frac{2c\sigma^2}{N} + 2(c-1)\mu^2,
\qquad
g'(1) = \frac{2\sigma^2}{N} + 0 = \frac{2\sigma^2}{N} > 0 .
$$
Since $g'(1) > 0$, $g$ is strictly increasing at $c = 1$, so for $c$ slightly **less** than $1$
we have $g(c) < g(1) = \operatorname{MSE}_A$. Hence such a $c \in (0,1)$ exists. (For the curious:
setting $g'(c) = 0$ gives the optimum $c^\star = \frac{\mu^2}{\mu^2 + \sigma^2/N} \in (0,1)$, the
classic shrinkage factor — but the problem only asked for existence.)

*Moral (1 sentence):* A deliberately biased estimator can have lower total error than the
unbiased one when the variance it saves exceeds the bias-squared it pays — this is the
bias–variance tradeoff, and it is the seed of shrinkage and regularization (Week 4).

---

## Problem 4 — Unbiased-but-inconsistent vs. biased-but-consistent (16 pts)

**(a) [4 pts]** $\hat{\mu}_1 = x_1$. Unbiasedness: $\mathbb{E}[x_1] = \mu$ for every $N$ (it does
not even look at the other observations). Variance: $\operatorname{Var}(\hat{\mu}_1) = \operatorname{Var}(x_1) = \sigma^2$,
a constant. It does **not** go to zero as $N \to \infty$ — it stays pinned at $\sigma^2$.

**(b) [4 pts]** A recipe concentrates on a single point only if its spread collapses to zero
(Chapter 1.3 §5: unbiased + variance$\to 0$ $\Rightarrow$ consistent). Here the spread is
$\sigma^2$ forever, so the sampling distribution of $\hat{\mu}_1$ never tightens; even as
$N \to \infty$, $\hat{\mu}_1$ keeps jumping around $\mu$ with the *same* variance and never
settles inside any fixed tolerance window with probability $\to 1$. Hence $\hat{\mu}_1$ is **not
consistent**: $\hat{\mu}_1 \not\xrightarrow{p} \mu$. What is "wrong" is that it throws away all
but one observation, so extra data never buys precision.

**(c) [5 pts]** $\hat{\mu}_2 = \frac{1}{N+5}\sum_{i=1}^N x_i = \frac{N}{N+5}\,\bar{x}$. Then
$$
\mathbb{E}[\hat{\mu}_2] = \frac{N}{N+5}\,\mathbb{E}[\bar{x}] = \frac{N}{N+5}\,\mu,
\qquad
\operatorname{Bias}(\hat{\mu}_2) = \frac{N}{N+5}\mu - \mu = -\frac{5}{N+5}\,\mu .
$$
The bias $-\frac{5\mu}{N+5}$ is nonzero for every finite $N$ (assuming $\mu \neq 0$), so
$\hat{\mu}_2$ is **biased at every $N$**. But as $N \to \infty$, $\frac{5}{N+5} \to 0$, so the
bias $\to 0$: the bias vanishes in the limit.

**(d) [3 pts]** Variance:
$$
\operatorname{Var}(\hat{\mu}_2) = \Big(\frac{N}{N+5}\Big)^2 \operatorname{Var}(\bar{x})
= \frac{N^2}{(N+5)^2}\cdot\frac{\sigma^2}{N} = \frac{N}{(N+5)^2}\,\sigma^2 \xrightarrow{N\to\infty} 0 .
$$
Both the bias and the variance go to $0$, so the whole sampling distribution of $\hat{\mu}_2$
collapses onto $\mu$: $\hat{\mu}_2 \xrightarrow{p} \mu$, i.e. $\hat{\mu}_2$ **is consistent**.
*Moral:* unbiasedness (a property at each fixed $N$) and consistency (a property in the limit)
are logically independent — $\hat{\mu}_1$ is unbiased but inconsistent, $\hat{\mu}_2$ is biased
but consistent — and neither implies the other.

---

## Problem 5 — Designing the Monte Carlo (17 pts)

**(a) [7 pts]** Pseudocode/commented Python, mirroring `nb1.3`:

```python
import numpy as np
rng = np.random.default_rng(8000)

# Known true population: lognormal calibrated so mean = $8,000 (the true mu we control).
sigma_log = 0.9
mu_log    = np.log(8000) - sigma_log**2 / 2     # so exp(mu_log + sigma_log^2/2) = 8000
mu_true   = 8000.0
N, R = 200, 10_000

def trimmed_mean(x, p=0.05):                      # drop smallest & largest 5%, then average
    xs = np.sort(x)
    k  = int(np.floor(p * len(xs)))
    return xs[k: len(xs) - k].mean()

mean_estimates, trim_estimates = [], []
for _ in range(R):                                # one "alternate universe" per pass
    x = rng.lognormal(mean=mu_log, sigma=sigma_log, size=N)   # draw ONE sample of N claims
    mean_estimates.append(x.mean())               # store the plain-mean estimate
    trim_estimates.append(trimmed_mean(x))        # store the trimmed-mean estimate

mean_estimates = np.array(mean_estimates)
trim_estimates = np.array(trim_estimates)

for name, est in [("plain mean", mean_estimates), ("trimmed", trim_estimates)]:
    bias = est.mean() - mu_true                   # (i) Monte Carlo bias
    var  = est.var()                              # (ii) Monte Carlo variance (spread of estimates)
    print(f"{name}: bias={bias:,.1f}  var={var:,.0f}  MSE={np.mean((est-mu_true)**2):,.0f}")
```

The three things made explicit: *draw one sample* = `rng.lognormal(..., size=N)`; *what we store
each replication* = the two estimators' values; *how we summarize* = average of stored values
minus `mu_true` for bias, sample variance of stored values for variance.

**(b) [4 pts]** With stored estimates $\hat{\mu}^{(1)}, \dots, \hat{\mu}^{(R)}$ and known $\mu$:
$$
\widehat{\operatorname{Bias}} = \Big(\tfrac{1}{R}\sum_{r=1}^R \hat{\mu}^{(r)}\Big) - \mu,
\qquad
\widehat{\operatorname{MSE}} = \frac{1}{R}\sum_{r=1}^R \big(\hat{\mu}^{(r)} - \mu\big)^2 .
$$
The variance estimate is the spread of the estimates about *their own* average,
$\widehat{\operatorname{Var}} = \frac{1}{R}\sum_r (\hat{\mu}^{(r)} - \bar{\hat{\mu}})^2$ where
$\bar{\hat{\mu}} = \frac1R\sum_r\hat{\mu}^{(r)}$. These satisfy the finite-sample identity
$$
\frac{1}{R}\sum_r (\hat{\mu}^{(r)} - \mu)^2
= \frac{1}{R}\sum_r (\hat{\mu}^{(r)} - \bar{\hat{\mu}})^2 + (\bar{\hat{\mu}} - \mu)^2
= \widehat{\operatorname{Var}} + \widehat{\operatorname{Bias}}^2,
$$
which is exactly the sample analogue of $\operatorname{MSE} = \operatorname{Var} + \operatorname{Bias}^2$.
(This is the same "add and subtract the mean" algebra as the chapter's MSE decomposition, applied
to the $R$ simulated values; it holds exactly, not just approximately, when the same
$\bar{\hat{\mu}}$ and the $\frac1R$ weighting are used in all three quantities.)

**(c) [3 pts]** Bias and variance are properties of the **estimator** — features of the *whole
sampling distribution* across all possible samples — whereas Priya's spreadsheet gives her one
**estimate**, a single realized number with no spread to measure. To see a distribution you need
many draws from a *known* population, which only a simulation provides; from one real sample you
cannot tell whether your number is high because the recipe is biased or just because this draw was
unlucky.

**(d) [3 pts]** On a right-skewed (lognormal) loss distribution the true mean $\mu$ is pulled up
by the heavy right tail of large claims. The 5%-trimmed mean *discards* that upper tail, so it
systematically lands **below** $\mu$ — a substantial negative bias. Trimming does cut the
variance (the volatile big claims are exactly what made $\bar{x}$ jump around), but here
$\operatorname{Bias}^2$ from chopping the tail is *larger* than the variance saved, so by
$\operatorname{MSE} = \operatorname{Var} + \operatorname{Bias}^2$ the trimmed mean ends up with
**higher** MSE. The lesson matches `nb1.3`: a little bias is a bargain only when it buys *enough*
variance, and for estimating the mean of a skewed loss distribution it does not — trimming
estimates a different target (something like a trimmed/typical claim), not $\mu$.

---

## Problem 6 — Sample variance and Bessel's correction (20 pts)

**(a) [5 pts]** With the true mean known,
$$
\mathbb{E}[\tilde{\sigma}^2]
= \mathbb{E}\!\left[\frac{1}{N}\sum_{i=1}^N (x_i - \mu)^2\right]
= \frac{1}{N}\sum_{i=1}^N \mathbb{E}\big[(x_i - \mu)^2\big]
= \frac{1}{N}\sum_{i=1}^N \sigma^2
= \sigma^2 ,
$$
using linearity of expectation and the definition $\sigma^2 = \mathbb{E}[(x_i - \mu)^2]$. So
$\tilde{\sigma}^2$ is unbiased — *when $\mu$ is known*. The trouble starts when we must estimate
$\mu$ too.

**(b) [9 pts]** *Algebraic identity.* Insert $\mu$ by adding and subtracting it inside the square:
$$
\sum_{i=1}^N (x_i - \bar{x})^2 = \sum_{i=1}^N \big[(x_i - \mu) - (\bar{x} - \mu)\big]^2 .
$$
Expand the square term by term:
$$
= \sum_{i=1}^N (x_i - \mu)^2 - 2(\bar{x} - \mu)\sum_{i=1}^N (x_i - \mu) + \sum_{i=1}^N (\bar{x} - \mu)^2 .
$$
Now $\sum_{i=1}^N (x_i - \mu) = \big(\sum_i x_i\big) - N\mu = N\bar{x} - N\mu = N(\bar{x} - \mu)$,
and the last sum has no $i$ inside, so it is $N(\bar{x}-\mu)^2$. Substituting:
$$
= \sum_{i=1}^N (x_i - \mu)^2 - 2(\bar{x}-\mu)\cdot N(\bar{x}-\mu) + N(\bar{x}-\mu)^2
= \sum_{i=1}^N (x_i - \mu)^2 - N(\bar{x}-\mu)^2 ,
$$
which is the claimed identity (the $-2N + N = -N$ collapses the two trailing terms).

*Take expectations.* Using $\mathbb{E}[(x_i-\mu)^2] = \sigma^2$ and
$\mathbb{E}[(\bar{x}-\mu)^2] = \operatorname{Var}(\bar{x}) = \sigma^2/N$ (Problem 2, since
$\mathbb{E}[\bar{x}]=\mu$):
$$
\mathbb{E}\!\left[\sum_{i=1}^N (x_i - \bar{x})^2\right]
= \sum_{i=1}^N \sigma^2 - N\cdot\frac{\sigma^2}{N}
= N\sigma^2 - \sigma^2 = (N-1)\sigma^2 .
$$

**(c) [3 pts]** Therefore
$$
\mathbb{E}[\hat{\sigma}^2_{\text{naive}}]
= \frac{1}{N}\,\mathbb{E}\!\left[\sum_i (x_i-\bar{x})^2\right]
= \frac{N-1}{N}\,\sigma^2 < \sigma^2 .
$$
The naive estimator is **biased downward**: its bias is
$\frac{N-1}{N}\sigma^2 - \sigma^2 = -\frac{\sigma^2}{N}$ (it understates the variance by a factor
$\frac{N-1}{N}$). Dividing instead by $N-1$ removes the factor and gives the unbiased estimator
$$
\boxed{\,s^2 = \frac{1}{N-1}\sum_{i=1}^N (x_i - \bar{x})^2\,},
\qquad \mathbb{E}[s^2] = \sigma^2 ,
$$
which is exactly `np.var(..., ddof=1)` / `np.std(..., ddof=1)`. Intuition for "why $N-1$": using
$\bar{x}$ in place of the unknown $\mu$ makes the deviations $x_i - \bar{x}$ a touch too small on
average (the sample mean sits in the middle of *its own* sample), so the sum of squares is
systematically short by exactly one observation's worth of variance — one *degree of freedom* was
spent estimating $\mu$.

**(d) [3 pts]** At $N = 200$ the naive estimator is off by the factor
$\frac{N-1}{N} = \frac{199}{200} = 0.995$, i.e. it **understates** $\sigma^2$ by about
**0.5%** on average — negligible for practical purposes. Bessel's correction only matters at
*small* $N$ (e.g. $N = 5$ gives $4/5$, a 20% understatement; $N = 2$ gives a 50% understatement);
by the hundreds it is a rounding detail, which is why the default still uses $N-1$ for honesty but
nobody worries about it once samples are large.

---

*Cross-references: bias–variance decomposition and the $\sigma^2/N$ formula are Chapter 1.3 §3–§4;
the trimmed-mean finding in Problem 5(d) matches `nb1.3` on the lognormal loss population
(trimming bias dominates the variance savings for estimating the mean). LLN/CLT (used only
intuitively in Problems 4–5) are proved in Chapter 1.4.*
