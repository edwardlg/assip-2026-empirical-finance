# Chapter 1.3 — Estimators and Their Sampling Distributions

Priya is interning at a regional insurer. Her supervisor drops a question on her desk that
sounds almost insultingly simple: *what is the average wildfire-related claim we pay out per
policy this season?* There is a true answer somewhere — a single number, $\mu$ dollars,
buried in the behavior of every policyholder, every dry summer, every spark near a power line.
But Priya cannot see it. She can only see the claims that actually came in: a spreadsheet of
$N = 200$ numbers, this season's sample.

So she does the obvious thing. She averages them. The spreadsheet says \$8,410. She writes
that on a sticky note and moves on.

Here is the question this chapter is about, and it is deeper than it looks: **how much should
Priya trust that \$8,410?** Not "is it the right number" — she will never know the right
number. The honest question is: *if the universe had handed her a different 200 claims — same
insurer, same season, same underlying risk, just a different draw of which policies happened
to file — how different would her sticky note be?* If a re-draw would have given her \$8,390,
the \$8,410 is solid. If a re-draw could plausibly have given her \$6,000 or \$11,000, then
\$8,410 is barely more than a rumor.

That "what if the draw had been different" question is the entire content of this chapter. To
answer it we need to stop thinking about Priya's one number and start thinking about the
*rule* that produced it.

---

## 1. The estimator–estimate distinction (say it out loud once)

Here is the result in one sentence, and it is the most important sentence in the chapter:

> An **estimator** is a random rule for turning data into a guess; an **estimate** is the one
> number you get when you feed it the data you happen to have.

The estimator is the recipe. The estimate is the cake you baked today. Confusing the two is
the single most common conceptual error in all of empirical work, so we will be pedantic about
it.

Priya's recipe is "add up the claims and divide by how many there are." Written generally,
with $x_1, x_2, \dots, x_N$ standing for the $N$ claim amounts, the recipe is the **sample
mean**:

$$
\bar{x} = \frac{1}{N}\sum_{i=1}^{N} x_i .
$$

Notice what kind of object $\bar{x}$ is. Each $x_i$ is a random variable — *before* the season
plays out, you do not know which policies will file or for how much, so each claim is a draw
from some distribution. A function of random variables is itself a random variable. Therefore
**$\bar{x}$ is a random variable.** It has an expectation, a variance, and a whole
distribution of its own. That distribution is the star of this chapter, and it has a name we
will earn in a moment.

The number \$8,410 is *not* random. It already happened. It is one realized value of the
random variable $\bar{x}$, the way "4" is one realized value of a die roll. We call that
realized number the **estimate**.

A notation convention we will hold to for the rest of the book, lifting the hat from the
front matter: when we want to name the estimator as a rule we will often write it as
$\hat{\mu}$ — "an estimator of $\mu$." The sample mean is one specific estimator of the
population mean, so $\hat{\mu} = \bar{x}$ here. But it is not the *only* estimator of $\mu$.
Priya could instead use:

- the **median** of the 200 claims,
- the average of just the smallest and largest claim (the "midrange"),
- the constant \$7,500 no matter what the data say (yes, that is a legal estimator — a stupid
  one, but legal),
- or a **trimmed mean** that throws out the top and bottom 5% before averaging.

Each of these is a different recipe, a different random variable, with a different
distribution. The job of this chapter — and really the job of the whole field of econometrics —
is to develop language for saying *which recipes are good and why*. That language has exactly
three words: **bias**, **variance**, and (combining them) **mean squared error**.

---

## 2. Bias: does the recipe aim at the right target?

Run Priya's recipe not once but in your imagination *infinitely many times* — every possible
200-claim sample the universe could have handed her, each weighted by how likely it is. Each
sample produces an estimate. Those estimates form a distribution. The question of **bias** is:
*where is that distribution centered?*

> An estimator $\hat{\mu}$ is **unbiased** for $\mu$ if $\mathbb{E}[\hat{\mu}] = \mu$ — on
> average across all possible samples, it lands exactly on the truth. Its **bias** is
> $\operatorname{Bias}(\hat{\mu}) = \mathbb{E}[\hat{\mu}] - \mu$.

Bias is *not* the error in your particular sample. Priya's \$8,410 might be off from the true
$\mu$ by hundreds of dollars — that is sampling error, and every estimate has it. Bias is about
the *center of the recipe*: if you averaged the errors over all conceivable samples, do they
cancel to zero, or is the recipe systematically aiming high or low?

Let us prove the sample mean is unbiased. Suppose each claim $x_i$ is drawn from a population
with mean $\mathbb{E}[x_i] = \mu$. Then, using only that expectation is linear (it passes
through sums and constants — established in Chapter 1.2):

$$
\mathbb{E}[\bar{x}]
= \mathbb{E}\!\left[\frac{1}{N}\sum_{i=1}^{N} x_i\right]
= \frac{1}{N}\sum_{i=1}^{N}\mathbb{E}[x_i]
= \frac{1}{N}\sum_{i=1}^{N}\mu
= \frac{1}{N}\cdot N\mu
= \mu .
$$

The sample mean is unbiased — full stop, for *any* sample size, even $N=3$. That is a strong
and slightly surprising fact: unbiasedness has nothing to do with having lots of data. A
3-claim average is just as unbiased as a 3-million-claim average. (What changes with $N$ is
something else entirely — the variance — which is the next section, and the heart of the
chapter.)

**Contrast with a biased recipe.** Suppose Priya, worried about a budget meeting, quietly drops
the three biggest claims before averaging "to remove outliers." Now the recipe systematically
discards the right tail of a distribution that is skewed right (a few catastrophic fires, lots
of small claims — insurance losses almost always look like this). Across all possible samples,
this recipe lands *below* $\mu$ on average. It is biased downward. The bias is not a mistake she
made on Tuesday; it is baked into the recipe and would persist no matter how much data she
collected.

**When unbiasedness fails — read the assumption.** The proof above used exactly one thing:
$\mathbb{E}[x_i] = \mu$ for every claim. That quietly assumes the 200 claims are drawn from the
*same* population whose mean Priya cares about. If her spreadsheet over-represents one
high-risk county because that county's broker is more diligent about filing, then the $x_i$ are
not all draws from the target population, $\mathbb{E}[x_i] \neq \mu$, and the proof collapses.
The math did not break; the assumption did. This is the recurring lesson of the book:
**estimators are only as good as the sampling assumption behind them**, and the first thing to
interrogate when a number looks wrong is whether the data you fed the recipe actually came from
the population you meant to study.

---

## 3. Variance: how jumpy is the recipe from sample to sample?

An unbiased recipe aims at the truth on average. But "on average" is cold comfort if any single
sample can be wildly off. Picture two archers. Both are unbiased — their arrows center on the
bullseye. The first archer's arrows land in a tight cluster around the center; the second
archer's are scattered all over the target, just *symmetrically* scattered so they average to
the center. You want the first archer. The spread of an estimator across samples is its
**variance**.

> The **variance** of an estimator, $\operatorname{Var}(\hat{\mu})$, measures how much the
> estimate bounces around from one sample to the next. Its square root, the **standard error**,
> is in the same units as the estimate (here, dollars) and is the number you actually report.

This is the place where sample size finally earns its keep. In Chapter 1.2 we derived the
variance of a sum of *independent* random variables: variances add. If the claims $x_1, \dots,
x_N$ are independent draws from a population with variance $\operatorname{Var}(x_i) =
\sigma^2$, then

$$
\operatorname{Var}\!\left(\sum_{i=1}^{N} x_i\right) = \sum_{i=1}^{N}\operatorname{Var}(x_i) = N\sigma^2 ,
$$

and since $\bar{x} = \frac{1}{N}\sum x_i$, and pulling the constant $\tfrac1N$ out of a variance
squares it (also Chapter 1.2):

$$
\boxed{\;\operatorname{Var}(\bar{x}) = \frac{1}{N^2}\cdot N\sigma^2 = \frac{\sigma^2}{N}\;}
$$

Stare at this formula, because almost everything quantitative in the rest of the book is a
descendant of it. The variance of the sample mean is the population variance *divided by $N$*.
The standard error is therefore

$$
\operatorname{se}(\bar{x}) = \sqrt{\operatorname{Var}(\bar{x})} = \frac{\sigma}{\sqrt{N}} .
$$

The standard error shrinks like $1/\sqrt{N}$ — **not** like $1/N$. This $\sqrt{N}$ is the most
consequential square root in statistics, and it is a little disappointing the first time you
meet it. To cut your standard error in half, you do not double your sample; you *quadruple* it.
To get one more decimal digit of precision (a tenfold drop in the error), you need a
*hundredfold* increase in data. Priya's boss wants the estimate twice as sharp? That is not 400
claims, that is 800. Precision is expensive, and it gets expensive at a very specific,
predictable rate.

**A number, to make it concrete.** Suppose the population standard deviation of claims is
$\sigma = \$12{,}000$ (insurance losses are volatile — most claims small, a few enormous). With
$N = 200$:

$$
\operatorname{se}(\bar{x}) = \frac{12{,}000}{\sqrt{200}} \approx \frac{12{,}000}{14.14} \approx \$849 .
$$

So Priya's \$8,410 carries a standard error of about \$849. A different draw of 200 claims could
easily have nudged her sticky note by several hundred dollars. That is the honest answer to her
boss's implicit question, and it is *quantitative*, derived from one formula. If she had $N =
5{,}000$ claims instead, the standard error would fall to $12{,}000/\sqrt{5000} \approx \$170$.
Same recipe, same unbiasedness, dramatically less jumpiness — purely because $N$ grew.

**Why independence is doing real work here.** The clean formula $\sigma^2/N$ leaned on a single
assumption from Chapter 1.2: that the claims are *independent*, so the variance of their sum is
the sum of their variances with no cross-terms. That assumption is not free, and in insurance it
is precisely the one to worry about. A single wildfire does not file one claim — it files
hundreds, all correlated, all driven by the same fire weather. When observations are positively
correlated, the variance of the sum picks up extra covariance terms (also from Chapter 1.2),
those terms are *positive*, and the true variance of $\bar{x}$ is **larger** than $\sigma^2/N$.
The naive standard error then understates the real wobble — Priya would think her estimate is
sharper than it is. We will not chase this down now, but file it away: the day you see "clustered
standard errors" later in the book, this is the leak they are plugging. The $1/\sqrt{N}$ rate is
a best case that assumes your observations carry genuinely independent information.

---

## 4. Mean squared error: the one number that combines both

Bias asks "do you aim true?" Variance asks "are you steady?" In the real world you usually have
to trade them off, and you need a single scorecard that respects both. That scorecard is the
**mean squared error**.

> The **mean squared error (MSE)** of an estimator is the expected squared distance between the
> estimate and the truth:
> $$\operatorname{MSE}(\hat{\mu}) = \mathbb{E}\!\left[(\hat{\mu} - \mu)^2\right].$$

MSE penalizes both kinds of badness at once: missing the target *and* being unsteady both make
$(\hat{\mu} - \mu)^2$ large on average. The beautiful fact is that MSE splits cleanly into
exactly those two pieces. Here is the decomposition, which you should be able to reproduce.

Start by inserting $\mathbb{E}[\hat{\mu}]$ and subtracting it right back — the classic "add zero
in a clever form" trick:

$$
\operatorname{MSE}(\hat{\mu})
= \mathbb{E}\!\left[\big(\hat{\mu} - \mathbb{E}[\hat{\mu}] + \mathbb{E}[\hat{\mu}] - \mu\big)^2\right].
$$

Group the two halves and expand the square $(A + B)^2 = A^2 + 2AB + B^2$, where $A = \hat{\mu} -
\mathbb{E}[\hat{\mu}]$ (random, mean zero) and $B = \mathbb{E}[\hat{\mu}] - \mu$ (a constant, the
bias):

$$
\operatorname{MSE}(\hat{\mu})
= \underbrace{\mathbb{E}\!\left[A^2\right]}_{\operatorname{Var}(\hat{\mu})}
+ 2\,\mathbb{E}[A]\,B
+ \underbrace{B^2}_{\operatorname{Bias}^2}.
$$

The cross term dies because $\mathbb{E}[A] = \mathbb{E}[\hat{\mu} - \mathbb{E}[\hat{\mu}]] = 0$:
the average deviation of anything from its own mean is zero. What survives is the headline
result:

$$
\boxed{\;\operatorname{MSE}(\hat{\mu}) = \operatorname{Var}(\hat{\mu}) + \operatorname{Bias}(\hat{\mu})^2\;}
$$

Total error equals variance plus bias squared. Read it as a budget. For an *unbiased* estimator
the second term is zero and MSE is just variance — which is why, for the sample mean,
"minimizing variance" and "minimizing MSE" are the same goal.

**Two recipes, scored.** Let's put numbers on the tradeoff so the scorecard isn't abstract. Keep
$\mu = \$8{,}000$ and $N = 200$, and pit two of Priya's recipes against each other.

*Recipe A — the plain sample mean.* Unbiased, so $\operatorname{Bias} = 0$. From §3 its standard
error is about \$849, so its variance is $849^2 \approx 720{,}000$ (dollars-squared). Its MSE is
therefore all variance:
$$
\operatorname{MSE}_A = \operatorname{Var}_A + 0^2 \approx 720{,}000.
$$

*Recipe B — the 5%-trimmed mean*, which drops the largest and smallest 5% of claims before
averaging. On a right-skewed loss distribution this lops off the volatile catastrophe tail, so
suppose simulation shows its variance falls to about $400{,}000$ — but, because it systematically
discards the right tail, it lands about \$300 low on average, a bias of $-300$. Its MSE is
$$
\operatorname{MSE}_B = \operatorname{Var}_B + \operatorname{Bias}_B^2 \approx 400{,}000 + (-300)^2 = 400{,}000 + 90{,}000 = 490{,}000.
$$

Recipe B is *biased* and yet wins decisively — $490{,}000 < 720{,}000$ — because the variance it
saved ($320{,}000$) dwarfs the bias-squared it paid ($90{,}000$). If instead the bias had been a
fat \$700, the penalty would be $490{,}000$ and B would *lose* ($400{,}000 + 490{,}000 =
890{,}000 > 720{,}000$). The whole game is in that arithmetic: a little bias is a bargain only
when it buys enough variance. (Whether B truly beats A for *this* loss distribution is an
empirical question — and it is exactly what you'll measure in `nb1.3`.)

**Why you'd ever accept bias.** The decomposition explains a fact that confuses people:
sometimes a *biased* estimator beats an unbiased one. Recall Priya's trimmed mean, which throws
out the most extreme claims. It is biased — but on a wildly skewed loss distribution, those
extreme claims are exactly what makes $\bar{x}$ jump around from sample to sample, so trimming
can slash the variance. If the variance drop is bigger than the bias-squared you pick up, the
trimmed mean has *lower MSE* and is, by this scorecard, the better recipe. This bias–variance
tradeoff is not a curiosity; it is the engine behind regularization, shrinkage estimators, and
essentially all of machine learning, and we will meet it again in earnest in Week 4. For now,
just hold the picture: a tiny, deliberate bias bought with a big cut in variance can be a
bargain.

---

## 5. Consistency: the recipe that gets it right *eventually*

So far everything has been about a *fixed* $N$. But there is a second, more aspirational virtue
we want from a recipe: as we pour in more and more data, the estimate should home in on the
truth and *stay* there. That virtue is **consistency**.

> An estimator $\hat{\mu}_N$ (now subscripted by sample size to emphasize it changes as $N$
> grows) is **consistent** for $\mu$ if it converges in probability to $\mu$ as $N \to \infty$,
> written
> $$\hat{\mu}_N \xrightarrow{p} \mu, \qquad \text{equivalently} \qquad \operatorname{plim}_{N\to\infty}\hat{\mu}_N = \mu.$$

We will treat $\xrightarrow{p}$ ("converges in probability," sometimes written with the
shorthand operator $\operatorname{plim}$, "probability limit") intuitively here, and *not* prove
the underlying theorem — that is the job of the very next chapter. The intuition is exactly what
the words say:

> $\hat{\mu}_N \xrightarrow{p} \mu$ means: pick any tolerance you like, say "within \$10 of the
> truth." For a large enough $N$, the probability that $\hat{\mu}_N$ lands inside that window is
> as close to $1$ (certainty) as you want. The estimate doesn't just get close on average — it
> gets *reliably, almost-surely* close, and the window can be made arbitrarily tight.

You can actually *see* consistency hiding inside the two formulas we already have. The sample
mean is unbiased, $\mathbb{E}[\bar{x}] = \mu$, so it is always centered on the truth. And its
variance is $\sigma^2/N$, which marches to $0$ as $N \to \infty$. An estimator that is centered
on the target with a spread collapsing to zero has nowhere to go *but* the target: the
distribution of $\bar{x}$ is being squeezed onto the single point $\mu$. That squeezing is
consistency, and the formal theorem that licenses this argument — the **Law of Large Numbers** —
is the first thing we prove in Chapter 1.4. (The precise statement "zero-limiting-bias plus
zero-limiting-variance implies consistency" even has a name, *convergence in mean square*; you
have effectively just seen why it works.)

Two warnings, so you don't over-learn the lesson:

1. **Unbiased and consistent are different properties, and neither implies the other.** A recipe
   can be unbiased at every $N$ yet *inconsistent* — for instance, "just use the first claim,
   $x_1$, and ignore the rest." That is unbiased ($\mathbb{E}[x_1] = \mu$), but its variance is
   $\sigma^2$ forever; pouring in more data never helps because the recipe ignores the new data.
   It never settles down. Conversely, a recipe can be *biased at every finite $N$ but
   consistent*, if its bias shrinks to zero as $N$ grows. Consistency is a statement about the
   limit; unbiasedness is a statement at each fixed $N$.
2. **Consistency does not save a broken sampling assumption.** If Priya's claims systematically
   over-sample one county, more of the same bad data drives $\bar{x}$ toward the *wrong* number
   with ever-greater confidence. A consistent estimator of the wrong thing is still wrong — just
   precisely, confidently wrong. Garbage in, garbage in.

---

## 6. The reveal: the sampling distribution, built by brute force

We have been talking about "the distribution of $\bar{x}$ across all possible samples" as if it
were a real object. It is. It has a name:

> The **sampling distribution** of an estimator is the probability distribution of the estimates
> you would get across all possible samples of a given size $N$ from the population.

Up to now we have only computed two *summaries* of this distribution — its center
($\mathbb{E}[\bar{x}] = \mu$) and its spread ($\operatorname{Var}(\bar{x}) = \sigma^2/N$). But
the full distribution has a shape, and the cleanest way to *see* a shape you cannot compute by
hand is to fake the universe on a computer and just look.

Here is the trick, and it is worth slowing down for because it is the conceptual core of the
entire chapter. In real life Priya gets **one** sample of 200 claims and therefore **one**
estimate, $\bar{x} = 8410$. She can never see the sampling distribution, because she only ever
draws once. But in a *simulation* we are gods: we know the true population, so we can draw a
fresh sample of 200, compute its $\bar{x}$, write it down, throw the sample away, and repeat ten
thousand times. The ten thousand $\bar{x}$ values we collect *are* a picture of the sampling
distribution. We are watching the random variable $\bar{x}$ do its thing, over and over, instead
of seeing it just once.

Let us build it. We will model individual claims with a right-skewed distribution (a
**lognormal**, the standard rough model for insurance losses — many small claims, a thin tail of
catastrophes) calibrated so the population mean is $\mu = \$8{,}000$.

```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(8000)

# --- the "true" population of claims: lognormal, mean = $8,000 ---
# For a lognormal, mean = exp(m + s^2/2). Pick s, then solve for m.
sigma_log = 0.9
mu_log = np.log(8000) - sigma_log**2 / 2
mu_true = np.exp(mu_log + sigma_log**2 / 2)          # = 8000 exactly, by construction

def draw_claims(n):
    return rng.lognormal(mean=mu_log, sigma=sigma_log, size=n)

# --- ONE sample, like Priya's reality ---
priyas_sample = draw_claims(200)
print(f"Priya's single estimate:  x-bar = ${priyas_sample.mean():,.0f}")

# --- the simulation: 10,000 alternate universes, each with its own 200 claims ---
def sampling_distribution(n, n_reps=10_000):
    return np.array([draw_claims(n).mean() for _ in range(n_reps)])

xbars_200 = sampling_distribution(200)
print(f"True mu .......................... ${mu_true:,.0f}")
print(f"Mean of the 10,000 x-bars ........ ${xbars_200.mean():,.0f}   (should ~ mu: unbiased)")
print(f"Std dev of the 10,000 x-bars ..... ${xbars_200.std():,.0f}")
print(f"Theory: sigma/sqrt(N) ............ ${priyas_sample.std(ddof=1)/np.sqrt(200):,.0f}")
```

Two lines of that output deserve a standing ovation. First, the mean of the ten thousand
$\bar{x}$ values lands essentially on \$8,000: the sampling distribution is centered on $\mu$,
exactly as the unbiasedness proof promised — now *seen*, not just derived. Second, the standard
deviation of those ten thousand estimates matches $\sigma/\sqrt{N}$ from §3. That standard
deviation of the sampling distribution has its own famous name — the **standard error** — and the
simulation shows you literally what it measures: the typical sample-to-sample wobble of your
estimate. The formula and the histogram are two views of the same object.

Now the part you cannot get from the formulas — the **shape**, and how it changes with $N$:

```python
fig, axes = plt.subplots(1, 3, figsize=(13, 4), sharey=True)
for ax, n in zip(axes, [10, 50, 500]):
    xbars = sampling_distribution(n)
    ax.hist(xbars, bins=40, density=True, color="#4C72B0", edgecolor="white")
    ax.axvline(mu_true, color="black", lw=2)                 # the truth
    se = xbars.std()
    ax.set_title(f"N = {n}\nse(x-bar) = ${se:,.0f}")
    ax.set_xlim(3000, 14000)
    ax.set_xlabel("estimate  x-bar  ($)")
axes[0].set_ylabel("density")
fig.suptitle("Sampling distribution of the sample mean, by sample size")
fig.tight_layout()
plt.show()
```

Three things jump out of those three panels, and they are the takeaways of the chapter:

1. **All three histograms are centered on the same black line at $\mu = \$8{,}000$.** Growing $N$
   does not move the center, because unbiasedness holds at every $N$. The recipe always aims
   true.
2. **The histograms get dramatically narrower as $N$ grows**, and they narrow at the
   $1/\sqrt{N}$ rate: going from $N=10$ to $N=500$ is a 50-fold jump in data, so the standard
   error should fall by $\sqrt{50} \approx 7$-fold — and it does. This visible collapse onto the
   black line *is* consistency. You are watching $\bar{x} \xrightarrow{p} \mu$ happen.
3. **The shape changes too.** At $N=10$, drawing from a skewed loss distribution, the histogram
   of $\bar{x}$ is still noticeably right-skewed — it remembers the shape of the underlying
   claims. By $N=500$ it has become a clean, symmetric bell, no matter that the individual
   claims are anything but bell-shaped. That is not an accident, and it is not something we have
   earned yet. *Why* does the sampling distribution of a mean become normal, regardless of the
   ugly distribution you started from? That is the **Central Limit Theorem**, and it is the
   second headline result of Chapter 1.4.

---

## 7. Where this is heading

Step back and notice what we did and did not do. We *defined* the sampling distribution and
*observed*, by simulation, two stunning facts about it: as $N$ grows it concentrates on the
truth (point 2 above) and it becomes normal (point 3). We have not yet *explained* either one.
That is deliberate. The two explanations are the two great limit theorems of statistics:

- **The Law of Large Numbers (LLN)** explains the concentration — *why* the distribution piles
  up on $\mu$. It is the rigorous engine behind the word "consistency" we used intuitively in
  §5.
- **The Central Limit Theorem (CLT)** explains the bell shape — *why* the sampling distribution
  of $\bar{x}$ is approximately normal for large $N$ even when the data are skewed, and it tells
  us *how large* the wobble is in standardized units.

Both are the entire subject of **Chapter 1.4**, which is where the $\sigma/\sqrt{N}$ standard
error stops being a formula you trust and becomes the thing you build confidence intervals and,
later (Chapter 1.5), hypothesis tests out of. For now you have the vocabulary that makes those
chapters possible: estimator versus estimate, bias, variance, MSE and its decomposition,
consistency, and — the object tying them all together — the sampling distribution.

Priya, for her part, now writes a better sticky note. Not "\$8,410," but "\$8,410, standard
error about \$850." The first is a rumor. The second is an estimate that knows how much to
trust itself.

---

## Your Turn

Open **`nb1.3` — the sampling-distribution explorer**. The notebook lets you choose a population
(normal, lognormal/insurance-loss, or a heavy-tailed one), a sample size $N$, and a number of
repetitions, then draws the sampling distribution of several competing estimators — the mean,
the median, and a trimmed mean — side by side. You will watch their centers, spreads, and shapes
respond as you turn the dials, and you will rank them by simulated MSE.

**Check questions.**

1. Priya's colleague argues: "Our estimate has a standard error of \$850, which is huge. Let's
   just collect a bigger sample until the standard error is under \$100." Starting from $N = 200$
   with $\sigma = \$12{,}000$, roughly how many claims would he need? Is that realistic for one
   season, and what does your answer say about the *price* of precision?

2. Consider the recipe "ignore all the data and always report \$8,000." Suppose the true mean is
   in fact exactly \$8,000. Is this estimator unbiased? Is it consistent? What is its variance,
   and what is its MSE? Now suppose the true mean is actually \$8,500 — re-answer all four. Use
   your answers to explain in one sentence why MSE is a more honest scorecard than bias alone.

3. In the simulation, the histogram of $\bar{x}$ for $N=10$ from the lognormal claims was
   right-skewed, but for $N=500$ it looked like a symmetric bell. Which of the two great theorems
   coming in Chapter 1.4 is responsible for the *centering* of that bell on $\mu$, and which is
   responsible for its *bell shape*? (You are not asked to prove either — just to attribute them
   correctly.)
