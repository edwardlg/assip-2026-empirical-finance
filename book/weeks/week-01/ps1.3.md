# Problem Set 1.3 — Bias, Variance, and MSE of Estimators

*Pairs with Chapter 1.3 (Estimators and Their Sampling Distributions) and the notebook
`nb1.3`. Use only tools through Chapter 1.3: linearity of expectation, the variance of a sum
of independent variables, $\operatorname{Var}(\bar{x}) = \sigma^2/N$, the bias–variance
decomposition of MSE, and the definitions of unbiasedness and consistency. You may invoke the
Law of Large Numbers and the Central Limit Theorem **intuitively** — for example, "the variance
goes to zero so the estimator concentrates on the truth" — but you are not asked to prove
either; those proofs belong to Chapter 1.4.*

**Notation (from `CONVENTIONS.md`).** Population mean $\mu = \mathbb{E}[x_i]$, population
variance $\sigma^2 = \operatorname{Var}(x_i)$. An estimator is written $\hat{\mu}$ (a random
rule); a particular realized number is the estimate. $\mathbb{E}[\cdot]$, $\operatorname{Var}(\cdot)$,
$\operatorname{Cov}(\cdot,\cdot)$ are expectation, variance, covariance. $\xrightarrow{p}$
denotes convergence in probability. The sample mean is $\bar{x} = \frac{1}{N}\sum_{i=1}^{N} x_i$.

**Total: 100 points across 6 problems.** Each problem is self-contained. Show your steps;
a correct number with no derivation earns little credit.

---

## Problem 1 — Unbiasedness of the sample mean, the long way and the short way (12 points)

Maya is studying the gig-economy: she has $N$ weekly earnings figures $x_1, \dots, x_N$ from a
panel of food-delivery drivers, and she models them as independent draws from a population with
mean $\mathbb{E}[x_i] = \mu$ (the "typical" weekly take) and variance
$\operatorname{Var}(x_i) = \sigma^2$. She uses the sample mean
$\bar{x} = \frac{1}{N}\sum_{i=1}^{N} x_i$ to estimate $\mu$.

**(a) [4 pts]** Prove from the definition that $\mathbb{E}[\bar{x}] = \mu$. State explicitly,
in one sentence, which property of expectation you use at each step and which assumption about
the $x_i$ the proof relies on.

**(b) [3 pts]** Maya only has $N = 6$ drivers' data. A classmate says, "Six is way too few — your
estimate must be biased." Is the classmate right that the estimate is *biased*? Answer yes or no
and justify in two sentences, distinguishing bias from sampling error.

**(c) [5 pts]** Now suppose Maya's panel accidentally over-samples drivers from one high-pay
metro area — the recruiting flyer was posted mostly in that city — so that for the over-sampled
drivers $\mathbb{E}[x_i] = \mu + \delta$ with $\delta > 0$, while the rest satisfy
$\mathbb{E}[x_i] = \mu$. If a fraction $\pi$ of the $N$ drivers are from the over-sampled metro,
find $\mathbb{E}[\bar{x}]$ and the bias of $\bar{x}$. Does collecting more drivers *the same way*
fix the problem? Explain in one sentence, and connect your answer to the difference between
*sampling error* (which shrinks with $N$) and *bias from a broken sampling frame* (which does
not).

---

## Problem 2 — Deriving $\operatorname{Var}(\bar{x}) = \sigma^2/N$ and the price of precision (15 points)

Stick with Maya's setup: $x_1, \dots, x_N$ independent, each with variance $\sigma^2$.

**(a) [6 pts]** Starting from $\operatorname{Var}\!\left(\sum_{i=1}^N x_i\right) = \sum_{i=1}^N \operatorname{Var}(x_i)$
(the variance-of-a-sum-of-independents result from Chapter 1.2), derive
$\operatorname{Var}(\bar{x}) = \sigma^2/N$. Show clearly where the factor $1/N^2$ comes from and
why pulling the constant $1/N$ outside the variance squares it.

**(b) [3 pts]** Hence write the standard error $\operatorname{se}(\bar{x})$ in terms of $\sigma$
and $N$. Suppose weekly earnings have $\sigma = \$240$. Compute the standard error for $N = 6$
and for $N = 600$.

**(c) [4 pts]** Maya wants the standard error to be at most \$10. Using $\sigma = \$240$, what
is the smallest $N$ that achieves this? Show the inequality you solve.

**(d) [2 pts]** Maya currently has $N = 600$ with a standard error of (your answer from part b).
She wants to *halve* it. By what factor must she multiply her sample size? Explain in one
sentence why this is the "$1/\sqrt{N}$ tax" on precision.

---

## Problem 3 — The bias–variance–MSE decomposition, applied to two recipes (20 points)

A population has true mean $\mu$ and variance $\sigma^2$, and you draw $N$ independent
observations. Recall the decomposition $\operatorname{MSE}(\hat{\mu}) = \operatorname{Var}(\hat{\mu}) + \operatorname{Bias}(\hat{\mu})^2$.

Consider two estimators of $\mu$:

- **Recipe A:** the plain sample mean, $\hat{\mu}_A = \bar{x}$.
- **Recipe B:** a *shrinkage* estimator that pulls the sample mean a fraction of the way toward
  a fixed guess of zero: $\hat{\mu}_B = c\,\bar{x}$, for a constant $0 < c < 1$.

**(a) [4 pts]** Show that $\hat{\mu}_A$ is unbiased and write its MSE in terms of $\sigma^2$
and $N$.

**(b) [5 pts]** Find $\mathbb{E}[\hat{\mu}_B]$ and hence the bias of $\hat{\mu}_B$. Find
$\operatorname{Var}(\hat{\mu}_B)$. (Hint: $\hat{\mu}_B$ is a constant times $\bar{x}$.)

**(c) [5 pts]** Write $\operatorname{MSE}(\hat{\mu}_B)$ in terms of $c$, $\mu$, $\sigma^2$, and
$N$. Confirm it reduces to your answer from (a) when $c = 1$.

**(d) [6 pts]** Show that there exists a value of $c$ strictly between $0$ and $1$ for which
$\operatorname{MSE}(\hat{\mu}_B) < \operatorname{MSE}(\hat{\mu}_A)$ — i.e. a *biased* estimator
beats the unbiased one. You do not need the optimal $c$; it is enough to evaluate the MSE at one
specific $c < 1$ (for instance, take $\mu = 0$ exactly, or take $c$ very close to $1$) and show
the inequality holds. State in one sentence what this says about the bias–variance tradeoff.

---

## Problem 4 — Unbiased but inconsistent; biased but consistent (16 points)

Devon is estimating the mean of a crypto token's daily return, with population mean $\mu$ and
variance $\sigma^2$, from $N$ independent daily observations $x_1, \dots, x_N$.

**(a) [4 pts]** Devon's lazy estimator is "just use the first day: $\hat{\mu}_1 = x_1$, ignore
the rest." Show $\hat{\mu}_1$ is unbiased for every $N$. Compute its variance. Does its variance
go to zero as $N \to \infty$?

**(b) [4 pts]** Using your variance from (a) and the intuition from Chapter 1.3 §5 (an estimator
concentrates on a point only if its spread collapses to zero), argue that $\hat{\mu}_1$ is **not
consistent**. In one sentence, say what is "wrong" with the recipe even though it is unbiased.

**(c) [5 pts]** Now consider a *biased* estimator: $\hat{\mu}_2 = \frac{1}{N+5}\sum_{i=1}^N x_i$
(it divides by $N + 5$ instead of $N$). Find $\mathbb{E}[\hat{\mu}_2]$ and its bias. Show the
bias is nonzero for every finite $N$ but tends to $0$ as $N \to \infty$.

**(d) [3 pts]** Find $\operatorname{Var}(\hat{\mu}_2)$ and argue that $\hat{\mu}_2$ **is**
consistent (its bias vanishes and its variance goes to zero). State the one-sentence moral:
unbiasedness and consistency are different properties, and neither implies the other.

---

## Problem 5 — Designing a Monte Carlo to measure bias and variance (17 points)

You have read in Chapter 1.3 that in real life you only ever draw *one* sample, so you can never
*see* the sampling distribution — but on a computer you can play god and draw thousands of
samples from a known population. In this problem you **design** (do not run) such an experiment;
it mirrors what `nb1.3` actually does.

Priya wants to compare two estimators of the mean claim size $\mu$ on a right-skewed
(lognormal) loss population whose true mean she sets to $\mu = \$8{,}000$: the plain sample mean
$\bar{x}$ and the 5%-trimmed mean (which discards the smallest and largest 5% of claims before
averaging), at sample size $N = 200$.

**(a) [7 pts]** Write clear pseudocode (or commented Python in the style of Chapter 1.3) for a
Monte Carlo with $R = 10{,}000$ replications that, for *each* of the two estimators, produces a
simulated estimate of (i) its bias and (ii) its variance. Your pseudocode must make explicit:
how you draw one sample, what you store on each replication, and how you turn the stored values
into a bias estimate and a variance estimate at the end. Use the known true $\mu$.

**(b) [4 pts]** Write the formula you would use to turn your $R$ stored estimates
$\hat{\mu}^{(1)}, \dots, \hat{\mu}^{(R)}$ into (i) a Monte Carlo estimate of the bias and (ii) a
Monte Carlo estimate of the MSE, given the known $\mu$. Confirm that your MSE estimate is
consistent with $\widehat{\operatorname{MSE}} \approx \widehat{\operatorname{Var}} + \widehat{\operatorname{Bias}}^2$.

**(c) [3 pts]** Why must this be a *simulation* rather than something Priya can compute from her
one real spreadsheet of 200 claims? Answer in two sentences, using the estimator/estimate
distinction.

**(d) [3 pts]** The notebook `nb1.3` reports that on this particular lognormal loss population,
the 5%-trimmed mean has **higher** MSE than the plain mean for estimating $\mu$. Explain, using
the bias–variance decomposition, *why* trimming can lose here even though it cuts the variance.
(Hint: which way does trimming push the estimate on a right-skewed distribution, and what is the
true target?)

---

## Problem 6 — Priya's variance estimator and Bessel's correction (20 points)

Priya now wants not the mean claim but a sense of how *spread out* claims are: she needs to
estimate the population variance $\sigma^2$ from her sample $x_1, \dots, x_N$ of independent
claims with mean $\mu$ and variance $\sigma^2$. A tempting recipe divides by $N$:

$$
\hat{\sigma}^2_{\text{naive}} = \frac{1}{N}\sum_{i=1}^N (x_i - \bar{x})^2 .
$$

This problem shows why the standard software default divides by $N-1$ instead (this is
*Bessel's correction*, the `ddof=1` you saw in the Chapter 1.3 code).

**(a) [5 pts]** As a warm-up, suppose for a moment that Priya magically knew the true mean $\mu$,
and used $\tilde{\sigma}^2 = \frac{1}{N}\sum_{i=1}^N (x_i - \mu)^2$. Show this is unbiased for
$\sigma^2$, i.e. $\mathbb{E}[\tilde{\sigma}^2] = \sigma^2$. (Use the definition
$\sigma^2 = \mathbb{E}[(x_i - \mu)^2]$ and linearity of expectation.)

**(b) [9 pts]** Now use the actual $\bar{x}$, not $\mu$. Prove the algebraic identity

$$
\sum_{i=1}^N (x_i - \bar{x})^2 = \sum_{i=1}^N (x_i - \mu)^2 - N(\bar{x} - \mu)^2 ,
$$

and then take expectations of both sides to show

$$
\mathbb{E}\!\left[\sum_{i=1}^N (x_i - \bar{x})^2\right] = (N-1)\,\sigma^2 .
$$

(You will need $\mathbb{E}[(x_i - \mu)^2] = \sigma^2$ and
$\mathbb{E}[(\bar{x} - \mu)^2] = \operatorname{Var}(\bar{x}) = \sigma^2/N$ from Problem 2.)

**(c) [3 pts]** Conclude that $\hat{\sigma}^2_{\text{naive}}$ (dividing by $N$) is **biased**,
report the exact direction and size of its bias, and write down the corrected, unbiased
estimator $s^2$. This is the estimator with `ddof=1`.

**(d) [3 pts]** For Priya's $N = 200$ claims, by what percentage does the naive estimator
under- or over-state $\sigma^2$ on average? Is Bessel's correction a big deal at $N = 200$, and
at what kind of $N$ does it actually start to matter? Answer in two sentences.

---

*Solutions: see Appendix E, `E-w1-ps1.3-solutions.md`. To check parts of Problems 3, 5, and 6
empirically, open `nb1.3` and turn the dials — set the population to lognormal, fix the true
mean, and read off the simulated bias, variance, and MSE for each estimator.*
