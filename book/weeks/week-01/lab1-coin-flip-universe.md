# Lab 1 — Build a Coin-Flip Universe

This is the capstone of Week 1. Everything you read about across Chapters 1.3–1.5 — estimators, sampling distributions, the Law of Large Numbers, the Central Limit Theorem, and the machinery of a hypothesis test — was about quantities you cannot see: a population mean $\mu$, the spread of an estimator across hypothetical re-draws of the universe, the true error rate of a decision rule. In a real study you get *one* sample, and you have to reason about the infinity of samples you did not get.

A simulation lets you cheat. You will *build* the universe yourself, fix its true parameter, and then draw from it as many times as you like. Because you know the true answer, you can check whether the tools actually do what the chapters claim. You will watch a sampling distribution tighten like $1/\sqrt{N}$ and go normal. You will write a one-proportion test from scratch and then *measure* — not assume — its false-positive rate and its power. And you will run a small p-hacking experiment that shows, in numbers, why a lone significant result pulled from many tries means almost nothing.

The running object is the simplest random thing there is: a coin. Sam wants to know whether a coin (or a trading signal that is "right" with some probability $p$, or a fair-lending audit asking whether an approval rate is really $0.5$) is fair. A coin flip is a **Bernoulli trial** — an experiment with two outcomes, $1$ ("heads") with probability $p$ and $0$ ("tails") with probability $1-p$. The mean of a Bernoulli is exactly $p$, and its variance is $p(1-p)$. That clean, known structure is what makes the coin the perfect teaching universe: every quantity you estimate has a true value you can write down.

---

## Learning goals

By the end of this lab you will be able to:

1. Build a Bernoulli population with a known parameter $p$ and draw repeated samples from it reproducibly.
2. Construct the **sampling distribution** of the estimator $\hat{p}$ by Monte Carlo, and show empirically that its spread falls like $1/\sqrt{N}$ and its shape converges to a normal (the CLT for a proportion).
3. Write a one-proportion z-test *from scratch* — test statistic, decision rule, p-value — and check it against a library.
4. **Measure** the empirical **size** of your test (its actual false-positive rate under the null) and confirm it lands near the $\alpha$ you chose.
5. **Measure** the empirical **power** of your test under an alternative and trace a power curve as the true effect and the sample size change.
6. (Stretch) Demonstrate how running many tests and reporting only the "winner" inflates the false-positive rate — a hands-on p-hacking experiment.

Throughout, the discipline is the one from Chapter 1.5: a number is only as convincing as the procedure behind it. Here you get to *audit the procedure*.

---

## Setup

Per the Conventions, every code block must run end-to-end on a fresh environment. Create and activate a conda environment, then install the three libraries this lab needs.

```bash
conda create -n week01-lab python=3.11 -y
conda activate week01-lab
pip install numpy scipy matplotlib
```

Open a notebook (`notebooks/week-01/lab1-coin-flip-universe.ipynb`) or a script, and start every run with the same header. Two rules of reproducibility you will follow without exception:

- **Pin the seed.** Use `numpy`'s modern generator, `rng = np.random.default_rng(SEED)`, *not* the old global `np.random.seed` / `np.random.rand`. A pinned seed means anyone who reruns your code gets your exact figures.
- **Draw all randomness from that one `rng`.** Do not mix in `random.random()` or a second generator; a single source of randomness is what makes a run replayable.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

SEED = 20260526            # any fixed integer; write it down
rng = np.random.default_rng(SEED)
```

One honest caveat before you start, because it will save you confusion later. Monte Carlo estimates are themselves random. When you "measure" a size and get $0.0487$ instead of exactly $0.05$, that gap is not a bug — it is sampling error in the *measurement of the procedure*. The fix is the same as everywhere else in this book: more reps, and a sense of the Monte Carlo standard error (we will compute it). Reruns with a *different* seed will wobble; reruns with the *same* seed will be bit-for-bit identical.

---

## Step 1 — Build a coin universe with known $p$

**What to do.** Write a function that draws one sample of $N$ Bernoulli($p$) trials and returns the sample proportion $\hat{p}$ — the fraction of heads. Because *you* set $p$, you hold the ground truth the rest of the lab is graded against.

The cleanest way to draw $N$ coin flips is `rng.binomial(n=1, p=p, size=N)`, which returns an array of $0$s and $1$s; their mean is $\hat{p}$. (A single Binomial$(N, p)$ draw divided by $N$ gives the same $\hat{p}$ and is faster, but the array of flips is more transparent the first time.)

**Code skeleton.**

```python
def draw_phat(p, N, rng):
    """One sample of N coin flips; return the sample proportion p-hat."""
    flips = rng.binomial(n=1, p=p, size=N)   # array of 0/1
    return flips.mean()                       # this is p-hat

# Sanity check against the known truth:
p_true = 0.5
for N in [10, 100, 10_000]:
    print(N, draw_phat(p_true, N, rng))
```

**What to expect.** With $p = 0.5$, a single $\hat{p}$ from $N = 10$ might be $0.3$ or $0.7$ — wildly off. At $N = 100$ it should sit within a few hundredths of $0.5$. At $N = 10{,}000$ it should pin $0.5$ to two or three decimals. You are watching the Law of Large Numbers in one line: $\hat{p} \xrightarrow{p} p$ as $N$ grows. The estimator is *consistent* for the true proportion.

**Reflection.** $\hat{p}$ is an estimator — a random rule — and each number you printed is one *estimate*. Before you ran the code, $\hat{p}$ had a whole distribution; afterward it is a single realized value. Which line of Chapter 1.3 is this distinction, and why does it matter that $\hat{p}$ for $N=10$ "could have been" something else?

---

## Step 2 — The sampling distribution of $\hat{p}$, and the CLT

**What to do.** One $\hat{p}$ is a dot. To see its *distribution*, repeat the draw thousands of times and histogram the results. Do this for several sample sizes and overlay them. You are reconstructing, by brute force, the sampling distribution that Chapter 1.3 defined and Chapter 1.4 gave a shape to.

Two facts you will verify, not assume:

- **It tightens like $1/\sqrt{N}$.** Theory says $\operatorname{Var}(\hat{p}) = p(1-p)/N$, so the standard deviation of $\hat{p}$ across samples is $\sqrt{p(1-p)/N}$. That is the **standard error** of a proportion. Quadruple $N$ and the spread should halve.
- **It goes normal.** The CLT says the standardized $\hat{p}$ converges to $N(0,1)$. A proportion is just a mean of $0/1$ draws, so the CLT applies directly — and you can watch the bell appear.

**Code skeleton.**

```python
def sampling_dist(p, N, reps, rng):
    """reps independent p-hats, each from N flips. Vectorized."""
    flips = rng.binomial(n=1, p=p, size=(reps, N))
    return flips.mean(axis=1)                  # array of length reps

p_true = 0.3            # try an off-center p too; the bell still comes
reps = 20_000

for N in [10, 40, 160]:
    phats = sampling_dist(p_true, N, reps, rng)
    emp_sd = phats.std(ddof=1)
    theo_se = np.sqrt(p_true * (1 - p_true) / N)
    print(f"N={N:4d}  empirical SD={emp_sd:.4f}  theory 1/sqrtN SE={theo_se:.4f}")
    plt.hist(phats, bins=50, density=True, alpha=0.4, label=f"N={N}")

plt.axvline(p_true, color="k", linestyle="--")
plt.xlabel(r"$\hat{p}$")
plt.ylabel("density")
plt.legend()
plt.show()
```

To see the CLT cleanly, standardize each $\hat{p}$ — subtract $p$, divide by the theoretical standard error — and overlay the standard normal, exactly as in Chapter 1.4:

```python
N = 160
phats = sampling_dist(p_true, N, reps, rng)
z = (phats - p_true) / np.sqrt(p_true * (1 - p_true) / N)

grid = np.linspace(-4, 4, 200)
plt.hist(z, bins=60, density=True, alpha=0.4, label=f"standardized $\\hat p$, N={N}")
plt.plot(grid, stats.norm.pdf(grid), "k--", label="N(0,1)")
plt.xlabel(r"$(\hat{p}-p)\,/\,\sqrt{p(1-p)/N}$")
plt.ylabel("density")
plt.legend()
plt.show()
```

**What to expect.** Three things. First, all three histograms center on $p$ (the estimator is unbiased). Second, the empirical SD column should track the $1/\sqrt{N}$ theory column closely: going $N = 10 \to 40 \to 160$ (each step a $4\times$) should roughly *halve* the spread each time. Third, the standardized histogram at $N = 160$ should lie almost exactly under the normal curve.

There is one subtlety worth chasing. At small $N$ the histogram of $\hat{p}$ is visibly *lumpy* — with $N = 10$ flips, $\hat{p}$ can only be $0, 0.1, 0.2, \dots, 1.0$, eleven discrete spikes — and if $p$ is near $0$ or $1$ it is also skewed (it cannot go below $0$ or above $1$, so one tail is squashed). The CLT still wins as $N$ grows, but it arrives *slower* the closer $p$ is to an edge. Try $p = 0.05$ with $N = 30$ and you will see a clearly non-normal pile-up; the "$N \ge 30$" folk rule from Chapter 1.4 quietly assumed a $p$ not too near the boundary. A common practitioner's check is whether $Np$ and $N(1-p)$ are both at least about $10$.

**Reflection.** You computed the standard error two ways: empirically (the SD of 20,000 simulated $\hat{p}$'s) and theoretically ($\sqrt{p(1-p)/N}$). Why are these the same quantity, and which one would you have access to if you only had a single real sample rather than a simulator? This is the whole reason standard-error *formulas* exist.

---

## Step 3 — Write your own one-proportion test

**What to do.** Now build the decision machine of Chapter 1.5 with your own hands, specialized to a proportion. Sam's question: is the coin fair? Frame it as the test

$$H_0: p = p_0, \qquad H_1: p \neq p_0,$$

with $p_0 = 0.5$ for a fairness test (a two-sided alternative, the honest default). The test statistic is the same idea as the t-statistic — estimate, minus null value, divided by standard error — but for a large-sample proportion we use a **z-statistic**, because under $H_0$ the standard error is *known*: it uses $p_0$, not an estimated $s$.

$$z = \frac{\hat{p} - p_0}{\sqrt{p_0(1 - p_0)/N}}.$$

The denominator uses $p_0$ deliberately: under the null we are pretending $p = p_0$ is true, so we plug in the null value's standard error. By the CLT, $z \xrightarrow{d} N(0,1)$ under $H_0$, so for a two-sided test at level $\alpha$ the p-value is the two-tailed normal area beyond $|z|$.

**Code skeleton.** Fill in the two `...` lines yourself — they are the heart of the test, and the point of the lab is that *you* write them.

```python
def one_prop_test(flips, p0=0.5):
    """One-proportion z-test. Returns (z, p_value, reject_at_05)."""
    N = flips.size
    phat = flips.mean()
    se0 = ...                       # standard error UNDER THE NULL (uses p0)
    z = ...                         # the z-statistic
    p_value = 2 * stats.norm.sf(abs(z))    # two-sided: both tails
    return z, p_value, (p_value < 0.05)

# Try it on one honest coin and one biased coin:
fair = rng.binomial(1, 0.5, size=200)
rigged = rng.binomial(1, 0.62, size=200)
print("fair  ->", one_prop_test(fair))
print("rigged->", one_prop_test(rigged))
```

Then check yourself against a library. `scipy.stats` does not ship a one-proportion z-test directly, but the exact `binomtest` is a good cross-check, and `statsmodels.stats.proportion.proportions_ztest` (if you add `statsmodels`) reproduces your z and p almost exactly:

```python
k = int(rigged.sum()); n = rigged.size
print(stats.binomtest(k, n, p=0.5, alternative="two-sided").pvalue)
```

**What to expect.** The fair coin should usually return a large (insignificant) p-value; the rigged coin (true $p = 0.62$, $N = 200$) should usually reject. Your hand-coded p-value should match `binomtest` to within a small amount — they will not be *identical*, because your z-test is the large-sample normal approximation and `binomtest` is exact, but at $N = 200$ they should agree closely. If they are wildly different, your `se0` or `z` line has a bug.

**Reflection.** You used $p_0 = 0.5$ in the standard error, not $\hat{p}$. Suppose you had used $\hat{p}$ instead. Argue from the *definition of a p-value* in Chapter 1.5 — "computed assuming the null is true" — why the null value belongs there. (This is exactly the move that distinguishes a test's standard error from a confidence interval's standard error.)

---

## Step 4 — Measure the empirical SIZE (does it really fire at rate $\alpha$?)

**What to do.** Here is the payoff of owning a simulator. The **size** of a test is its probability of a Type I error: rejecting $H_0$ when $H_0$ is *true*. Chapter 1.5 *defined* size as $\alpha$ and asserted a well-built test rejects a true null about $\alpha$ of the time. You will now *measure* it. Build a universe where the null is exactly true — a genuinely fair coin, $p = p_0 = 0.5$ — run your test thousands of times, and count how often it rejects.

**Code skeleton.**

```python
def empirical_size(p0, N, alpha, reps, rng):
    """Fraction of rejections when the null is TRUE (data drawn at p0)."""
    rejects = 0
    for _ in range(reps):
        flips = rng.binomial(1, p0, size=N)
        _, p_value, _ = one_prop_test(flips, p0=p0)
        rejects += (p_value < alpha)
    return rejects / reps

reps = 20_000
size = empirical_size(p0=0.5, N=200, alpha=0.05, reps=reps, rng=rng)
mc_se = np.sqrt(0.05 * 0.95 / reps)          # Monte Carlo SE of the estimate
print(f"empirical size = {size:.4f}  (target 0.05, MC SE ~ {mc_se:.4f})")
```

**What to expect.** The empirical size should land *close* to $0.05$ — within a few Monte Carlo standard errors (the MC SE at 20,000 reps is about $0.0015$, so expect something in the rough neighborhood of $0.05$–$0.056$). You have essentially *verified* that your from-scratch test controls its false-positive rate near the advertised level. This is the single most important property of a test, and you just confirmed it without anyone having to take it on faith. Do not be alarmed if it sits a hair *above* $0.05$: the normal-approximation z-test on discrete coin data is known to be slightly liberal (it over-rejects a touch) at moderate $N$, because the smooth normal does not perfectly match the lumpy Binomial. That small gap is itself a finding — it is the approximation showing its seams — and it shrinks as $N$ grows. The exact `binomtest` would instead come in at or below $0.05$.

Now stress it. Re-measure the size with a *small* sample and an *off-center* null, say $N = 25$ and $p_0 = 0.1$. You will likely find the empirical size drifts away from $0.05$ — often *below* it (conservative) because of the discreteness you saw in Step 2, sometimes erratically. This is the normal approximation breaking down exactly where Step 2 warned it would, when $Np_0$ is small.

**Reflection.** A true null produces $p < 0.05$ about $5\%$ of the time *by construction* — Chapter 1.5 even proved the p-value is uniform on $[0,1]$ under the null. Run your reps once more and histogram the p-values from the fair-coin runs. What shape do you expect, and what does that shape predict the fraction below any threshold $\alpha$ should be? (This is the seed of Step 6.)

---

## Step 5 — Measure the POWER and trace a power curve

**What to do.** Size asks how often you cry wolf when there is no wolf. **Power** asks the opposite: when there *is* a wolf — when $H_1$ is true — how often do you catch it? Power is $1 - \beta = \Pr(\text{reject } H_0 \mid H_1 \text{ true})$. To measure it, change one thing: draw the data from a coin whose true $p$ is *not* $p_0$, then run the same test and count rejections.

**Code skeleton.** This is your size function with the data-generating $p$ pulled apart from the null $p_0$.

```python
def empirical_power(p_true, p0, N, alpha, reps, rng):
    """Fraction of rejections when the data come from p_true != p0."""
    rejects = 0
    for _ in range(reps):
        flips = rng.binomial(1, p_true, size=N)   # truth is p_true
        _, p_value, _ = one_prop_test(flips, p0=p0)  # but we test against p0
        rejects += (p_value < alpha)
    return rejects / reps

print(empirical_power(p_true=0.6, p0=0.5, N=200, alpha=0.05,
                      reps=20_000, rng=rng))
```

Notice that `empirical_size` is just `empirical_power` with `p_true == p0`. Size is power evaluated *at the null* — they are the same machine pointed at different truths. That is worth pausing on.

Now trace a **power curve**: hold $p_0 = 0.5$, $\alpha = 0.05$, $N$ fixed, and sweep the true $p$ across a grid. Then redo the sweep for a few values of $N$ and overlay the curves.

```python
p_grid = np.linspace(0.30, 0.70, 17)
for N in [50, 200, 800]:
    powers = [empirical_power(pt, 0.5, N, 0.05, 4_000, rng) for pt in p_grid]
    plt.plot(p_grid, powers, marker="o", label=f"N={N}")

plt.axhline(0.05, color="grey", linestyle=":")   # at p=0.5, power == size
plt.axvline(0.5, color="grey", linestyle=":")
plt.xlabel("true p (data-generating)")
plt.ylabel("power = P(reject)")
plt.legend()
plt.show()
```

**What to expect.** Each curve is a valley. At the bottom, $p = 0.5$: there the null is true, so "power" equals the *size* — about $0.05$, the dotted line. As the true $p$ moves away from $0.5$ in either direction, power climbs toward $1.0$: bigger effects are easier to detect, just as Chapter 1.5 said. And the larger-$N$ curves are *steeper and narrower* — with $N = 800$ even a small bias like $p = 0.55$ is caught most of the time, while at $N = 50$ that same bias slips past more often than not. This picture is the four power levers of Chapter 1.5 made visible: effect size (horizontal distance from $0.5$) and sample size (which curve) both buy power.

**Reflection.** Read off the curve: at $N = 50$, roughly how far from $0.5$ must the true $p$ be before you catch the bias $80\%$ of the time? Now connect this to the "fail to reject is not accept" rule. If Sam runs the $N = 50$ test on a coin that is truly $p = 0.54$ and fails to reject, what is the *correct* sentence to write — and what does the power curve say about why a non-rejection here proves so little?

---

## Step 6 (Stretch) — A p-hacking mini-experiment

**What to do.** This is the warning from Section 1.5.10, turned into an experiment you run yourself. Imagine Sam is screening trading signals — or Leah is testing many candidate keywords for "predicting" a patent's success — and *every one of them is truly worthless*. Each individual test, run honestly, falsely fires only $5\%$ of the time. But Sam runs *many* and reports only the best. How often does at least one worthless signal look "significant"?

Build a universe of $m$ independent fair coins (all null true, $p = 0.5$), test each one, and record whether *any* of them rejected. Repeat the whole screen thousands of times and measure the fraction of screens with at least one false positive.

**Code skeleton.**

```python
def any_false_positive(m, N, alpha, reps, rng):
    """Run m honest tests on m TRUE nulls; fraction of screens with >=1 reject."""
    hits = 0
    for _ in range(reps):
        any_reject = False
        for _ in range(m):
            flips = rng.binomial(1, 0.5, size=N)      # every coin is fair
            _, p_value, _ = one_prop_test(flips, p0=0.5)
            if p_value < alpha:
                any_reject = True
        hits += any_reject
    return hits / reps

for m in [1, 5, 20, 50]:
    emp = any_false_positive(m, N=200, alpha=0.05, reps=5_000, rng=rng)
    theory = 1 - (1 - 0.05) ** m          # independent-tests formula
    print(f"m={m:3d}  empirical P(>=1 FP)={emp:.3f}  formula={theory:.3f}")
```

**What to expect.** Your empirical numbers should track the formula $1 - (1-\alpha)^m$ from Chapter 1.5: about $0.05$ at $m=1$, $0.23$ at $m=5$, $0.64$ at $m=20$, and $0.92$ at $m=50$. With fifty worthless signals you are *almost guaranteed* a spurious "winner." Print the p-value of the best-looking coin in a screen that produced a false positive — it will look perfectly respectable, maybe $0.01$, and it will be a complete artifact of having tried fifty times.

**Optional fix — Bonferroni.** Re-run with the per-test bar tightened to $\alpha/m$ instead of $\alpha$. The family-wide false-positive rate should drop back toward $0.05$ regardless of $m$. You have just implemented, in three characters, the crudest multiple-testing correction — and confirmed it works.

**Reflection.** The reported p-value of the "winner" is a lie because it ignores the silent attempts behind it. Write down, in one sentence each: (a) what question you should always ask when someone shows you a single significant signal, and (b) why pre-registration — committing to the test before seeing data — defeats this particular cheat. Tie both back to Section 1.5.10.

---

## You're done when…

Use this checklist. A box is checked only when you can point to the number or figure that proves it.

- [ ] **Step 1.** `draw_phat` returns a sensible $\hat{p}$, and you can show $\hat{p}$ pinning the true $p$ ever more tightly as $N$ goes $10 \to 100 \to 10{,}000$.
- [ ] **Step 2.** Your empirical SD column matches the $\sqrt{p(1-p)/N}$ theory column, and the spread roughly halves each time $N$ quadruples. The standardized histogram at large $N$ lies under the $N(0,1)$ curve. You can also exhibit a *small-$N$, near-edge* case where the bell has **not** yet arrived, and explain why.
- [ ] **Step 3.** Your `one_prop_test` uses $p_0$ (not $\hat{p}$) in the standard error, and its p-value agrees with `binomtest` at $N = 200$. You can state, in p-value terms, why $p_0$ belongs in the denominator.
- [ ] **Step 4.** Measured size at $N = 200$, $p_0 = 0.5$ lands within about $2$ Monte Carlo SEs of $0.05$, and you reported the MC SE. The fair-coin p-values are roughly uniform on $[0,1]$.
- [ ] **Step 5.** Your power curves are valleys bottoming at $\approx 0.05$ when $p = p_0$ and rising toward $1$ as the true $p$ departs; larger $N$ gives a steeper, narrower valley. You read a concrete detectable-effect size off the $N = 50$ curve.
- [ ] **Step 6 (stretch).** Your measured $\Pr(\ge 1 \text{ false positive})$ tracks $1 - (1-\alpha)^m$ across $m$, and Bonferroni pulls it back to $\approx 0.05$.
- [ ] **Reproducibility.** Every figure regenerates identically from a single pinned `SEED` and one `rng`; rerunning the whole notebook top-to-bottom produces the same numbers, and you can name your seed.

---

## Where this connects

You have now done, with your own hands, the thing the chapters could only describe. The sampling distribution stopped being a definition and became a histogram you built; the CLT stopped being a theorem and became a bell that assembled itself on your screen; size and power stopped being Greek letters and became fractions you counted. Most importantly, you learned the simulation habit that runs through the rest of the program: *when you are unsure whether a statistical tool does what it claims, build a universe where you know the truth and check.*

In Week 2 the object under test changes from a proportion to a regression coefficient $\hat{\beta}$, and the test statistic becomes $t = (\hat{\beta} - 0)/\widehat{\operatorname{se}}(\hat{\beta})$ — the same estimate-minus-null-over-standard-error machine you just built and audited here. The size-and-power simulator you wrote will return, almost unchanged, to stress-test whether OLS standard errors are honest under heteroskedasticity, clustering, and serial correlation. The p-hacking experiment will grow into the full treatment of multiple-testing corrections and the false discovery rate. Keep this notebook; you will reuse its skeletons.
