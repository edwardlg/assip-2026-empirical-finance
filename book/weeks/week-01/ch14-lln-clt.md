# Ch 1.4 — The LLN and the CLT, Shown Not Asserted

In the last chapter we built a machine and watched it work. We took a population with a known mean $\mu$ and standard deviation $\sigma$, drew a sample of size $N$, and computed the sample mean $\bar{x}$. Then we did it again. And again — ten thousand times — and looked at the histogram of all those $\bar{x}$ values. That histogram is the *sampling distribution of the mean*: the spread of estimates we could have gotten, if luck had dealt us a different sample. We found two things by simulation. First, that histogram sat centered on $\mu$ (the sample mean is unbiased). Second, it got narrower as $N$ grew, and in fact its variance was exactly $\operatorname{Var}(\bar{x}) = \sigma^2 / N$.

Those were observations. We saw them happen on the screen, but we never said *why* they must happen, and we never said what *shape* that tightening histogram was settling into. This chapter pays both debts. There are two great facts of statistics hiding in that simulation, and almost everything you will do for the rest of this book — every standard error, every $t$-statistic, every confidence interval — rests on them.

The first fact is the **Law of Large Numbers (LLN)**: as $N$ grows, $\bar{x}$ stops wandering and homes in on the true $\mu$. That is *why* the histogram concentrates. The second is the **Central Limit Theorem (CLT)**: once you rescale $\bar{x}$ the right way, the shape of its sampling distribution becomes the bell curve — the normal distribution — no matter what messy distribution the raw data came from. That is *which* shape the histogram is settling into.

We will do these in the spirit of the whole book: state the result plainly, show why it works with intuition and then a simulation, and then — this is the part most courses skip — show you exactly when it breaks. Because the CLT does not always arrive on time. Devon, who spends his evenings pulling crypto price data off-chain, is about to discover that averaging crypto returns is a very different experience from averaging coin flips, and the reason is one of the most important cautionary tales in all of empirical finance.

---

## 1. The Weak Law of Large Numbers

### State it

Let $x_1, x_2, \dots, x_N$ be independent draws from some population with mean $\mu$ and finite variance $\sigma^2$. Form the sample mean

$$
\bar{x} = \frac{1}{N}\sum_{i=1}^{N} x_i .
$$

The **Weak Law of Large Numbers** says that as $N$ grows, $\bar{x}$ converges in probability to $\mu$:

$$
\bar{x} \xrightarrow{p} \mu .
$$

In words: for any tolerance you name — call it $\epsilon$, say one-tenth of a cent — the probability that $\bar{x}$ lands more than $\epsilon$ away from $\mu$ can be driven as close to zero as you like, simply by taking $N$ large enough. The sample mean is *consistent* for the population mean. This is the precise version of the intuition we leaned on in Ch 1.3: more data, less luck.

Two cautions on the name. "Weak" distinguishes this from the *Strong* Law, which makes a subtly stronger promise about a single infinite sequence of draws settling down forever; the distinction is real but it will not matter for anything we do, so we use the Weak Law and move on. And "converges in probability," written $\xrightarrow{p}$, is not the ordinary limit from calculus. $\bar{x}$ is random; it does not approach $\mu$ the way $1/N$ approaches $0$. What shrinks to zero is the *probability of a meaningful miss*.

### Why it works: Chebyshev does the heavy lifting

We will not prove the LLN with full rigor, but we can make it feel inevitable with one tool you can carry for the rest of your life: **Chebyshev's inequality**. It says that no random variable strays far from its own mean very often, where "far" is measured in standard deviations. Formally, for any random variable $Y$ with mean $\mu_Y$ and variance $\sigma_Y^2$, and any $\epsilon > 0$,

$$
\Pr\!\big(|Y - \mu_Y| \ge \epsilon\big) \le \frac{\sigma_Y^2}{\epsilon^2}.
$$

You do not need to memorize the proof, but the idea is worth a sentence: variance is the average squared distance from the mean, so if a lot of probability sat far out at distance $\epsilon$ or more, the variance would have to be large. Turn that around and a small variance *forbids* much probability from sitting far out. Chebyshev is deliberately crude — it makes no assumption at all about the *shape* of the distribution, only that it has a finite variance, and a guarantee that has to cover every conceivable shape cannot be tight for any particular one. The bound it gives is almost always loose: for a genuinely normal variable, Chebyshev allows up to $1/4$ of the probability beyond two standard deviations, when the true figure is about $5\%$. But loose is exactly what we want here, because we are not trying to nail down a probability — we are trying to prove one *vanishes*, and a crude upper bound that goes to zero settles that question just as decisively as a sharp one would.

Now apply Chebyshev to $Y = \bar{x}$. Here is the whole trick in one line. We already know — this was the punchline of Ch 1.3 — that the sample mean has mean $\mu$ and variance $\sigma^2 / N$. So Chebyshev hands us:

$$
\Pr\!\big(|\bar{x} - \mu| \ge \epsilon\big) \le \frac{\operatorname{Var}(\bar{x})}{\epsilon^2} = \frac{\sigma^2}{N\,\epsilon^2}.
$$

Stare at the right-hand side. The tolerance $\epsilon$ is whatever you fixed, $\sigma^2$ is a property of the population and does not change, but $N$ sits in the denominator. As $N \to \infty$, that bound goes to zero. The probability of missing $\mu$ by more than $\epsilon$ is squeezed to nothing. That *is* the Weak Law, and we got it almost for free, because the real work — establishing $\operatorname{Var}(\bar{x}) = \sigma^2 / N$ — was done last chapter.

Notice what the engine of the LLN is: **averaging cancels noise.** Each draw $x_i$ has its own variance $\sigma^2$, but when you average $N$ independent draws, the wiggles partly cancel, and the variance of the average falls like $1/N$. The independence assumption is what makes the cancellation work: when draws are independent, their deviations from $\mu$ are as likely to offset as to reinforce, so the sum of $N$ deviations grows only like $\sqrt{N}$ rather than like $N$, and dividing by $N$ to form the average leaves something that shrinks. (If the draws were instead strongly *correlated* — every observation echoing the last, as happens with a trending time series — the deviations would reinforce instead of cancel, the $1/N$ rate would degrade, and the LLN would arrive far more slowly or not at all. That is a foreshadowing of why time-series data demand special standard errors in Week 2.)

The $\sqrt{N}$ that you have surely seen attached to standard errors is this same fact wearing different clothes: the standard deviation of $\bar{x}$ is $\sigma/\sqrt{N}$, so to halve your uncertainty you must *quadruple* your sample. Diminishing returns are baked into the mathematics, and they are worth internalizing as a researcher's reflex — when someone tells you they doubled their sample and expected their error bars to halve, you should already know they will be disappointed.

### See it: a Monte Carlo of one running mean

The cleanest way to watch the LLN is not the ten-thousand-histograms picture from last chapter; it is to follow a *single* sample as it grows and plot the running mean. Imagine Sam simulating fair die rolls, where the population mean is $\mu = 3.5$. We draw one die, then a second, then a third, and after each new roll we recompute the average of everything so far. Then we plot that average against the number of rolls.

```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)        # reproducible: pin the seed
N = 5000
rolls = rng.integers(1, 7, size=N)     # uniform on {1,...,6}, mu = 3.5

running_mean = np.cumsum(rolls) / np.arange(1, N + 1)

plt.plot(running_mean)
plt.axhline(3.5, linestyle="--")       # the true mu
plt.xscale("log")                      # so early wildness is visible
plt.xlabel("number of rolls (N)")
plt.ylabel("running sample mean")
plt.show()
```

What you see is a curve that starts out jagged and undisciplined — after three rolls the average might be $2.0$ or $5.3$, anything is possible — and then, as $N$ climbs into the hundreds and thousands, flattens out and presses against the dashed line at $3.5$. It never lands exactly on $3.5$ and stays there; it keeps making tiny corrections forever. But the size of the wandering shrinks, visibly, like $1/\sqrt{N}$. That picture is the Weak Law made of pixels: not a promise that $\bar{x}$ equals $\mu$, but a promise that the room it has to wander in keeps closing.

A useful sanity check you can run yourself: change the seed and watch a *different* jagged path settle onto the same dashed line. The destination is a property of the population; only the route is random.

---

## 2. The Central Limit Theorem

The LLN tells us *where* $\bar{x}$ ends up. It says nothing about the *shape* of the cloud of possible $\bar{x}$ values around that destination. That shape is the CLT's job, and it is, frankly, one of the most surprising facts in mathematics.

### State it

Take the same independent draws $x_1, \dots, x_N$ from a population with mean $\mu$ and finite variance $\sigma^2$. We saw that $\bar{x}$ has mean $\mu$ and standard deviation $\sigma/\sqrt{N}$. Now **standardize** it — subtract its mean and divide by its standard deviation, so we are left with a quantity measured in "standard errors away from the truth":

$$
z_N = \frac{\bar{x} - \mu}{\sigma / \sqrt{N}} .
$$

The **Central Limit Theorem** says that as $N$ grows, the distribution of $z_N$ converges to the standard normal:

$$
\frac{\bar{x} - \mu}{\sigma / \sqrt{N}} \;\xrightarrow{d}\; N(0, 1).
$$

The symbol $\xrightarrow{d}$ means *convergence in distribution*: the entire shape of $z_N$'s histogram — not just its center or width, but its whole silhouette — approaches the standard normal bell curve. And here is the astonishing clause: this happens **regardless of the shape of the original population**, as long as it has a finite mean and a finite variance. The raw data can be skewed, lumpy, bounded, discrete, U-shaped — it does not matter. Average enough of it, standardize, and you get the same universal bell.

That universality is why the normal distribution is everywhere in statistics. It is not that nature loves bell curves. It is that we spend our lives looking at *averages and sums* of many small independent pieces — and the CLT says averages of almost anything look normal.

### Why it works: the intuition before the algebra

Why should this be true? A full proof uses a device called the characteristic function and is beyond us here, but the intuition is reachable and it is the part worth owning.

Think about what an average does. Each draw $x_i$ contributes some quirky deviation from $\mu$ — maybe it is far above, maybe just below. When you add up many such deviations, two forces act. First, the deviations partly cancel (the LLN force). Second, and this is the CLT's secret, the particular *combination* of pluses and minuses that survives is built from a huge number of independent little contributions, no single one of which dominates. Mathematics has a strong tendency: whenever a quantity is a sum of many small independent influences of comparable size, the histogram of that sum smooths toward the normal curve. The lumps and skews of any one source get averaged away in the aggregation; the only thing that survives the limit is the smooth, symmetric bell.

A second angle on the same intuition explains why the bell is the *unique* destination rather than one of many possibilities. Suppose you average $N$ draws and then, separately, average another $N$ draws, and combine the two groups into one average of $2N$. The shape of the sampling distribution should not care whether you did it in one batch or two — averaging is averaging. The normal distribution is essentially the only shape with finite variance that is *stable* under this kind of self-combination: a normal averaged with a normal is again normal, just narrower. Any distribution flexible enough to be the limit of repeated averaging is forced, by this self-consistency, into the normal form. You do not have to make that argument rigorous to feel its pull: the bell is not an arbitrary fixed point, it is the only one the algebra of summing-and-rescaling will tolerate.

The phrase "no single one of which dominates" is doing quiet but crucial work — hold onto it, because it is exactly the clause that crypto returns will violate in Section 4.

### See it: from a hard-to-believe population to a perfect bell

The honest way to be convinced is to start from a population that looks *nothing* like a normal distribution and watch the bell emerge anyway. Priya is studying insurance claims, which are notoriously skewed — most policies cost the insurer nothing in a given month, a few cost a fortune. A clean stand-in for that shape is the **exponential distribution**: it is strongly right-skewed, piled up near zero with a long tail to the right. Its mean and standard deviation both equal a scale parameter; take the scale to be $1$, so $\mu = 1$ and $\sigma = 1$.

Here is the experiment, which is the heart of notebook **nb1.4**. We pick a sample size $N$. We draw $N$ exponential values, compute $\bar{x}$, standardize it to $z_N$, and store that one number. We repeat that whole process, say, $50{,}000$ times to map out the sampling distribution of $z_N$. Then we histogram those $50{,}000$ standardized means and overlay the standard normal curve. Finally we redo the entire thing for several values of $N$ — say $N = 1, 2, 5, 30, 100$ — and watch the histogram morph.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

rng = np.random.default_rng(7)
mu, sigma = 1.0, 1.0                 # exponential(scale=1): right-skewed
reps = 50_000
grid = np.linspace(-4, 4, 200)

for N in [1, 2, 5, 30, 100]:
    samples = rng.exponential(scale=1.0, size=(reps, N))
    xbar = samples.mean(axis=1)
    z = (xbar - mu) / (sigma / np.sqrt(N))      # the standardization
    plt.hist(z, bins=60, density=True, alpha=0.4, label=f"N = {N}")

plt.plot(grid, stats.norm.pdf(grid), "k--", label="N(0,1)")
plt.xlabel(r"$(\bar{x} - \mu)\,/\,(\sigma/\sqrt{N})$")
plt.ylabel("density")
plt.legend()
plt.show()
```

Describe to yourself what comes out, panel by panel, because this sequence of pictures *is* the CLT:

- **$N = 1$.** The standardized mean is just a single standardized exponential draw. It looks exactly like the exponential: a sharp wall on the left, a long tail dragging off to the right. Nothing bell-like about it.
- **$N = 2$.** Averaging two draws already softens the wall and pulls the peak toward center, but it is still visibly lopsided.
- **$N = 5$.** The skew is fading. A bell is trying to form; the left side has rounded off and the right tail is shorter.
- **$N = 30$.** The histogram and the dashed normal curve are now nearly on top of each other. This is the origin of the folk rule "$N \ge 30$ is enough for the CLT" — for a mildly skewed distribution like this one, thirty is plenty.
- **$N = 100$.** Indistinguishable from the normal curve by eye.

The lesson lands hardest if you remember where we started: a violently skewed pile-up-at-zero distribution. Average a hundred of them, standardize, and you cannot tell the result from a perfect bell. That is the CLT, shown not asserted.

### The folk rule, and why it is only a folk rule

"$N \ge 30$" is a teaching crutch, not a theorem. How fast the bell arrives depends on how skewed and heavy-tailed the original population is. For a symmetric, well-behaved population, $N = 5$ might already look normal. For Priya's mildly skewed exponential, thirty is comfortable. For a savagely skewed population — one rare giant claim among thousands of zeros — you might need thousands of observations before the standardized mean looks normal. The folk rule quietly assumes your data are not *too* wild. The next section is about what happens when that assumption is not just strained but *false*.

---

## 3. Reading the two laws together

Before we break the CLT, fix the division of labor in your head, because students mix these up constantly and the rest of the book depends on keeping them straight.

The **LLN** is a statement about a *point*: $\bar{x}$ collapses onto the single number $\mu$. If that were the whole story, then for large $N$ the sample mean would be essentially constant and there would be nothing left to do inference about — no uncertainty to quantify.

The **CLT** is what keeps inference alive. It says that *before* the collapse is complete, the cloud around $\mu$ has a precise, knowable shape. Zoom in on $\bar{x}$ with a microscope whose magnification is $\sqrt{N}$ — which is exactly what dividing by $\sigma/\sqrt{N}$ does — and you do not see a shrinking dot, you see a stable bell that never goes away. The LLN says the cloud shrinks; the CLT says that under the microscope the cloud always looks like $N(0,1)$.

Put them together and you have the engine of frequentist statistics. We know $\bar{x}$ is near $\mu$ (LLN), and we know *exactly how its misses are distributed* (CLT). That second part is what lets us make calibrated statements like "I am 95% confident the true mean is in this interval." Hold that thought: it is the literal subject of the next chapter.

---

## 4. When the CLT is slow — or fails entirely

Every assumption in the two theorems is load-bearing. The one that breaks most dramatically in finance — and the one Devon is about to walk into — is the innocent-looking clause **"finite variance."** When the variance is enormous, the CLT is merely *slow*. When the variance is *infinite*, the CLT does not apply at all, and the sample mean can betray you no matter how much data you collect.

### Devon's discovery: averaging crypto returns

Devon has been pulling daily returns for a basket of cryptocurrencies. He has read the last two chapters and reasons confidently: "Returns are returns. I will average a few hundred daily returns, the CLT kicks in around $N = 30$, my sample mean is approximately normal, and I will slap a confidence interval on the average daily return." He runs it. The confidence interval comes out absurdly narrow on one sample and wildly different on the next month of data. Something is wrong, and it is not his code.

The problem is **fat tails** — a distribution whose extreme values are far more probable than a normal curve of the same width would allow. Equity returns are already heavier-tailed than the normal distribution: big moves happen more often than a bell curve predicts, which is the quantitative reason October 1987 and March 2020 were not supposed to be possible under the models of their day. Crypto returns are heavier still. A single day can post a $+40\%$ or $-50\%$ move that, under a normal model fit to ordinary days, should occur perhaps once in the lifetime of the universe — and yet on-chain you find several such days in a single year. These are not rounding errors out in the tail; they are the part of the distribution that contains most of the action. In a fat-tailed return series, the typical day tells you almost nothing about the average; a handful of catastrophic or euphoric days do most of the work, and any statistic that hopes to summarize the series has to reckon with them honestly.

Here is why fat tails poison the average. Recall the CLT's secret clause from Section 2: the bell emerges only when the sum is built from many small contributions, *no single one of which dominates*. In a fat-tailed series, that clause fails. On most days the return is a small wiggle, but every so often one monster day arrives whose magnitude is comparable to the sum of everything around it. When you average $N$ returns and one of them is a $-50\%$ day, that single observation yanks $\bar{x}$ around all by itself. The averaging never gets to do its noise-cancelling job, because one term refuses to be small relative to the rest.

### "Has a mean" is not the same as "the CLT bites quickly"

This is the distinction Devon needs, and it is subtle enough to deserve its own paragraph. There is a hierarchy of bad behavior, and you must locate your data on it.

A distribution can have a perfectly well-defined mean $\mu$ and still have a *gigantic* — or even *infinite* — variance. The mean and the variance are separate integrals; the first can converge while the second blows up. The tail probabilities are what decide it. A family of distributions that makes this concrete is the **Student's $t$** with $\nu$ degrees of freedom, which finance routinely uses as a stand-in for fat-tailed returns:

- For $\nu > 2$ (say $\nu = 5$, a common fit for daily equity returns), the variance is finite, so the CLT *does* eventually hold — but slowly. The tails are heavy enough that you might need $N$ in the hundreds or low thousands, not thirty, before the standardized mean looks normal.
- For $\nu = 2$, the mean still exists but the variance is *infinite*. The CLT's hypothesis is violated outright. There is no $\sigma$ to standardize by, and the standardized-mean histogram never settles onto the bell.
- For $\nu = 1$ — the **Cauchy distribution**, the canonical horror story — even the *mean* fails to exist. The integral that should define $\mu$ does not converge. The sample mean of $N$ Cauchy draws has *the same distribution as a single draw*: averaging a million of them is no more informative than looking at one. The LLN itself fails. This is the pathological extreme, and it is worth seeing once so the rest of the hierarchy makes sense.

So "the distribution has a mean" buys you, at most, the *hope* that the LLN works. It does not buy you a fast CLT, and if the variance is infinite it does not buy you the CLT at all. Devon's crypto returns live somewhere in the heavy but finite-variance zone — closer to low-$\nu$ Student's $t$ than to a normal — which means his sample mean *is* eventually consistent and asymptotically normal, but "eventually" might require far more data than he has, and any confidence interval he builds from a few hundred observations is built on sand.

### See it: the bell that refuses to form

The simulation that makes this unforgettable is the exact CLT experiment from Section 2, rerun with a fat-tailed population in place of the exponential. Devon does it with a Student's $t$ at a few degrees of freedom — heavy enough to misbehave, with a finite variance so the comparison to the normal is at least defined.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

rng = np.random.default_rng(2024)
nu = 3                                  # Student-t: heavy tails, finite var for nu>2
sigma = np.sqrt(nu / (nu - 2))          # true sd of t_nu  (= sqrt(3) here)
reps = 50_000
grid = np.linspace(-4, 4, 200)

for N in [30, 100, 1000, 5000]:
    samples = rng.standard_t(df=nu, size=(reps, N))   # mu = 0
    xbar = samples.mean(axis=1)
    z = (xbar - 0.0) / (sigma / np.sqrt(N))
    plt.hist(z, bins=80, range=(-4, 4), density=True, alpha=0.4, label=f"N = {N}")

plt.plot(grid, stats.norm.pdf(grid), "k--", label="N(0,1)")
plt.legend(); plt.show()
```

Compare this picture to Priya's. With the exponential, $N = 30$ already matched the bell. Here, at $N = 30$, the histogram is far too *peaked in the middle and too heavy in the tails* — there is still way too much probability piled up past $\pm 3$ standard errors, because the occasional monster draw keeps throwing $\bar{x}$ far out. By $N = 100$ it is better but still visibly off. You have to push $N$ into the thousands before the histogram finally agrees with the dashed normal curve. Same theorem, same standardization, drastically slower convergence — and the only thing that changed is the weight in the tails.

For the truly pathological case, swap `rng.standard_t(df=nu, ...)` for `rng.standard_cauchy(...)` and run the *running-mean* plot from Section 1. Instead of settling onto a line, the running average jumps around forever, occasionally leaping to a wild new level when a giant draw arrives, never converging to anything. That is the LLN failing in front of you — the visual proof that "more data" is not a universal cure.

### What Devon should actually do

The point of this section is not to make Devon give up; it is to make him honest about what his tools can promise. The practical responses, all of which you will meet later in the book, are: report that returns are fat-tailed and quantify it rather than assuming normality; lean on the median or other robust summaries that are not hostage to a single monster day; use far larger samples before trusting a normal approximation; and when he eventually builds standard errors, use ones that do not silently assume thin tails. The single most valuable habit is the cheapest: before trusting any average, *plot the data and look at the tails.* If a histogram of the raw returns has fat tails or outliers that dwarf the bulk, treat every CLT-based claim as provisional until you have checked how fast — or whether — the bell actually forms.

---

## 5. Where this is going

You now have the two pillars. The LLN guarantees that with enough honest data the sample mean lands on the truth. The CLT guarantees that the misses, properly rescaled by $\sigma/\sqrt{N}$, follow the standard normal bell — provided the data are not so fat-tailed that the bell never gets a chance to form.

Hold onto the standardized quantity $\dfrac{\bar{x}-\mu}{\sigma/\sqrt{N}}$, because the next chapter is built entirely on it. In Ch 1.5 we confront the one thing we have been quietly cheating on: in real life we *do not know* $\sigma$ and have to estimate it from the same sample. Replacing the true $\sigma$ with an estimate $\hat{\sigma}$ turns that normal into a slightly fatter-tailed cousin — **Student's $t$ distribution**, the very family we just used to break the CLT — and from it we will derive the $t$-test and the confidence interval, the two workhorses of empirical inference. Everything we test for the rest of the program is, underneath, an application of the two laws you just watched converge.

---

## Your Turn

Open **nb1.4 — CLT/LLN convergence animations** and make these convergences move:

1. **Watch the LLN wander.** Reproduce the running-mean plot for fair dice, then overlay five different seeds on the same axes. Confirm that all five paths funnel toward $\mu = 3.5$ and that the width of the funnel shrinks like $1/\sqrt{N}$. Now swap the dice for `rng.standard_cauchy()` and watch the running mean refuse to settle.

2. **Animate the bell forming.** Rebuild the Section 2 experiment for the exponential population, but loop $N$ from $1$ to $100$ and save one histogram-plus-normal-overlay frame per $N$. Stitch the frames into an animation. Identify, by eye, the smallest $N$ at which you can no longer distinguish the histogram from the $N(0,1)$ curve.

3. **Race the tails.** Run the exponential and the Student-$t(\nu=3)$ experiments side by side and find, for each, the $N$ at which the standardized mean first looks normal. Report the ratio. That ratio is your personal, simulated measure of how much heavy tails cost you.

### Check questions

1. The Weak Law follows from Chebyshev's inequality applied to $\bar{x}$ once you know one fact from Ch 1.3. What is that fact, and why does plugging it into Chebyshev force the miss-probability to zero as $N \to \infty$?

2. A classmate says, "The CLT proves that any large dataset is normally distributed." State precisely what the CLT actually claims, and explain why your classmate's sentence is wrong on two counts (what object becomes normal, and what assumption is required).

3. Two return series both have a well-defined mean $\mu$. Series A is drawn from a Student's $t$ with $\nu = 8$; series B from a Student's $t$ with $\nu = 2$. For which series does the CLT eventually apply to the standardized sample mean, and why does the answer hinge on the *variance* rather than the *mean*?
