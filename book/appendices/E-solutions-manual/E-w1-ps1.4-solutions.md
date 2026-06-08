# Solutions — Problem Set 1.4 (The LLN and the CLT)

*Full worked solutions to `book/weeks/week-01/ps1.4.md`. Notation follows CONVENTIONS §3: the standardized sample mean is $z_N=(\bar{x}-\mu)/(\sigma/\sqrt{N})$, $\xrightarrow{p}$ is convergence in probability, $\xrightarrow{d}$ convergence in distribution. Normal-table values used: $\Pr(Z>1.645)\approx 0.05$, $\Pr(|Z|>1.96)\approx 0.05$, $\Pr(Z>2.33)\approx 0.01$, $\Pr(Z<-2.33)\approx 0.01$, plus $\Pr(Z>0.5)\approx 0.309$, $\Pr(Z>2)\approx 0.0228$, $\Pr(Z>2.5)\approx 0.0062$.*

---

## Problem 1 — Chebyshev forces the Weak Law (14 pts)

**(a) (4 pts)** The sample mean is unbiased and its variance falls like $1/N$:
$$
\mathbb{E}[\bar{x}] = \mu = 42, \qquad \operatorname{Var}(\bar{x}) = \frac{\sigma^2}{N} = \frac{30^2}{N} = \frac{900}{N}.
$$
The fact from Ch 1.3 is that for $N$ **independent** draws, averaging cancels noise so that $\operatorname{Var}(\bar{x})=\sigma^2/N$ exactly (and $\mathbb{E}[\bar{x}]=\mu$).

**(b) (5 pts)** Chebyshev applied to the random variable $\bar{x}$ (which has mean $\mu$ and variance $\sigma^2/N$):
$$
\Pr\!\big(|\bar{x}-\mu|\ge \epsilon\big) \le \frac{\operatorname{Var}(\bar{x})}{\epsilon^2} = \frac{\sigma^2}{N\,\epsilon^2} = \frac{900}{N\cdot 2^2} = \frac{225}{N}.
$$
Set the bound $\le 0.05$:
$$
\frac{225}{N}\le 0.05 \quad\Longrightarrow\quad N \ge \frac{225}{0.05} = 4500.
$$
So Chebyshev *guarantees* the miss-probability is at most $0.05$ once $\boxed{N \ge 4500}$.

*(Remark for graders: $4500$ is large precisely because Chebyshev is loose; the CLT-based answer would be far smaller. Full marks for $N\ge 4500$ with the correct bound.)*

**(c) (3 pts)** The bound $\sigma^2/(N\epsilon^2)$ has $\epsilon$ and $\sigma^2$ fixed and $N$ in the denominator, so it $\to 0$ as $N\to\infty$ for *any* fixed $\epsilon>0$. A probability squeezed below a quantity that vanishes must itself vanish; that is exactly the statement $\bar{x}\xrightarrow{p}\mu$. Looseness is harmless here because we only need an upper bound that goes to zero, not a tight one — a crude bound that vanishes settles the limit just as decisively as a sharp one.

**(d) (2 pts)** The bound is $225/N$; replacing $N$ by $4N$ gives $225/(4N)$, so the bound shrinks by a **factor of 4**. To cut the miss-probability bound to a quarter you must quadruple the sample — the standard error scales like $\sigma/\sqrt{N}$, so halving uncertainty costs a fourfold increase in $N$.

---

## Problem 2 — Standardize a sample mean and read the normal table (16 pts)

**(a) (3 pts)**
$$
\mathbb{E}[\bar{x}] = \mu = 120, \qquad \text{SE}(\bar{x}) = \frac{\sigma}{\sqrt{N}} = \frac{200}{\sqrt{400}} = \frac{200}{20} = 10.
$$

**(b) (4 pts)**
$$
z_N = \frac{\bar{x}-\mu}{\sigma/\sqrt{N}} = \frac{\bar{x}-120}{10} \;\xrightarrow{d}\; N(0,1).
$$
By the CLT, $z_N$ is approximately standard normal for large $N$. The skew of the raw policy costs does **not** block this: the CLT promises that the standardized *average* becomes normal regardless of the population's shape, as long as the population has a **finite mean and finite variance** — both of which hold here. Skewness only slows convergence; it does not prevent it.

**(c) (6 pts)** Standardize the threshold $\bar{x}=130$:
$$
\Pr(\bar{x}>130) = \Pr\!\left(\frac{\bar{x}-120}{10} > \frac{130-120}{10}\right) = \Pr(Z > 1) \approx 0.159.
$$
So there is about a **16% chance** the portfolio's average monthly cost exceeds \$130. (Using $\Pr(Z>1)\approx 0.1587$.)

**(d) (3 pts)** The colleague is wrong. The **Central Limit Theorem** concerns the *average* of the 400 policies, not a single policy. As long as the single-policy cost has a **finite variance** (it does — $\sigma=200$ is large but finite), the standardized average $\bar{x}$ is approximately normal even though each individual cost is wildly skewed. Skew slows the bell's arrival; with $N=400$ it has had ample opportunity to form.

---

## Problem 3 — How large must $N$ be for a skewed population? (18 pts)

**(a) (4 pts)** $\text{SE}(\bar{x}) = \sigma/\sqrt{N} = 40/\sqrt{N}$.

- For SE $=1$: $40/\sqrt{N}=1 \Rightarrow \sqrt{N}=40 \Rightarrow N = 1600$.
- For SE $=0.5$: $40/\sqrt{N}=0.5 \Rightarrow \sqrt{N}=80 \Rightarrow N = 6400$.

Note the fourfold jump ($1600\to 6400$) to halve the SE — the $\sqrt{N}$ law again.

**(b) (5 pts)** We want $\Pr(\bar{x}<0)\le 0.01$. Standardize:
$$
\Pr(\bar{x}<0) = \Pr\!\left(\frac{\bar{x}-\mu}{\sigma/\sqrt{N}} < \frac{0-\mu}{\sigma/\sqrt{N}}\right) = \Pr\!\left(Z < \frac{-5}{40/\sqrt{N}}\right) = \Pr\!\left(Z < -\frac{5\sqrt{N}}{40}\right).
$$
We need $\Pr(Z<-2.33)\approx 0.01$, so require
$$
-\frac{5\sqrt{N}}{40} \le -2.33 \quad\Longrightarrow\quad \frac{5\sqrt{N}}{40}\ge 2.33 \quad\Longrightarrow\quad \sqrt{N} \ge \frac{2.33\cdot 40}{5} = 18.64.
$$
Thus $N \ge 18.64^2 \approx 347.5$, i.e. the smallest integer is $\boxed{N = 348}$.

**(c) (5 pts)** The formula in (a) uses only $\sigma$, and it remains *arithmetically* true even for the jackpot population (same $\mu$ and $\sigma$ would give the same SE). But the answer to (b) relied on the **CLT having already kicked in** — i.e., on $z_N$ actually being approximately normal at $N\approx 348$. With one-in-a-thousand $+\$5{,}000$ jackpots, the population is *savagely* right-skewed: a single jackpot draw can dominate the whole sum, so the standardized mean is still far from normal at $N=348$ (too peaked, too heavy in the right tail), and the normal probability $0.01$ is not trustworthy. The unstated work is being done by the **"$N\ge 30$" folk rule**, which quietly assumes the population is not too skewed or heavy-tailed. Here that assumption is false, so Sam likely needs $N$ in the thousands or more.

**(d) (4 pts)** The standard error $\sigma/\sqrt{N}$ controls how *tight* the cloud is, but the **shape** of the population controls how fast the standardized mean becomes *normal*. The more skewed or heavy-tailed the population, the larger $N$ must be before $z_N$ looks like $N(0,1)$ and a normal-table probability can be trusted. Two populations with identical $\mu$ and $\sigma$ can demand wildly different $N$ for the CLT to bite.

---

## Problem 4 — Devon's heavy-tails hierarchy (18 pts)

**(a) (6 pts)** Using "mean exists iff $\nu>1$, variance finite iff $\nu>2$":

| Model | $\nu$ | Mean exists? | Variance finite? |
|-------|------|--------------|------------------|
| A | 5 | Yes ($5>1$) | Yes ($5>2$) |
| B | 2 | Yes ($2>1$) | **No** ($\nu=2$ not $>2$; variance infinite) |
| C | 1 | **No** ($\nu=1$ not $>1$; Cauchy) | No (undefined) |

**(b) (6 pts)**

- **Model A ($\nu=5$):** Both **LLN and CLT hold** (and are guaranteed). Mean exists $\Rightarrow$ LLN applies; variance finite $\Rightarrow$ CLT applies. Convergence is *slow* (heavy tails) but it does occur.
- **Model B ($\nu=2$):** **LLN holds** (the mean exists, so $\bar{x}\xrightarrow{p}\mu=0$), but the **CLT fails**: the variance is infinite, so there is no $\sigma$ to standardize by and the classical CLT's hypothesis is violated. $z_N$ never settles onto $N(0,1)$.
- **Model C ($\nu=1$, Cauchy):** **Both fail.** The mean does not exist, so the LLN has nothing to converge to; with no mean there is certainly no finite variance, so the CLT fails too.

**(c) (3 pts)** For the Cauchy, the average of $N$ i.i.d. draws has the **same distribution as a single draw** — averaging a million of them is no more informative than looking at one. This is why the chapter calls it the **"canonical horror story"**: the LLN itself fails, so "more data" is not a cure.

**(d) (3 pts)** **Yes**, his sample mean is *eventually* consistent and asymptotically normal: his returns have a finite (if very large) variance, which satisfies both the LLN and the classical CLT, so in the limit $\bar{x}\xrightarrow{p}\mu$ and $z_N\xrightarrow{d}N(0,1)$. But **$N=300$ is not likely enough**: tails heavier than $\nu=5$ make convergence very slow (the chapter notes you may need hundreds-to-thousands even for $\nu=5$), so any normal-table claim at $N=300$ is built on sand.

---

## Problem 5 — Design a Monte Carlo to show CLT convergence (16 pts)

*This is a design problem; full marks for a clear, implementable procedure. A reference design follows; the runnable version lives in **nb1.4**.*

**(a) (8 pts)** A complete loop:

1. **Population.** Draw from the exponential with scale $1$: $\mu = 1$ and $\sigma = 1$. It is strongly right-skewed (piled at zero, long right tail), so it is a good stress test for the CLT.
2. **One replication.** Draw a sample of size $N$ from the exponential. Compute its sample mean $\bar{x}$. Standardize it:
   $$ z_N = \frac{\bar{x}-\mu}{\sigma/\sqrt{N}} = \frac{\bar{x}-1}{1/\sqrt{N}} = (\bar{x}-1)\sqrt{N}. $$
   Store this single number $z_N$.
3. **Many replications.** Repeat step 2 a large number of times — e.g. $\text{reps}=50{,}000$ — to map out the sampling distribution of $z_N$. (More reps = smoother histogram.)
4. **Plot.** Histogram the $50{,}000$ stored $z_N$ values with `density=True` and overlay the standard-normal pdf $N(0,1)$ as a reference curve on the same axes.

Pseudocode:
```
fix seed
for N in N_list:
    z_values = []
    repeat reps times:
        sample = draw N exponential(scale=1) values
        xbar   = mean(sample)
        z      = (xbar - 1) / (1/sqrt(N))
        append z to z_values
    histogram(z_values, density=True)
    overlay standard normal pdf
```

**(b) (4 pts)** Sweep $N \in \{1, 2, 5, 30, 100\}$. Expected appearance vs. the overlaid $N(0,1)$:

- $N=1$: looks like the raw exponential — sharp left wall, long right tail; not bell-like.
- $N=2$: wall softens, peak pulled toward center, still lopsided.
- $N=5$: skew fading, a bell trying to form.
- $N=30$: histogram and normal curve nearly coincide.
- $N=100$: indistinguishable from the bell.

Smallest $N$ where the bell is indistinguishable by eye: about **$N=30$**, matching the "$N\ge 30$" folk rule, which holds for a *mildly* skewed population like the exponential.

**(c) (4 pts)** A quantitative diagnostic (any one):
- **Sample skewness and excess kurtosis** of the stored $z_N$ values: both should head toward $0$ as $N$ grows (standard normal has skew $0$, excess kurtosis $0$). Reporting them as numbers turns "looks bell-shaped" into a measurement.
- *Alternatively:* a **Q–Q plot** of $z_N$ against the standard normal — points hugging the $45^\circ$ line indicate normality, and systematic departure in the tails flags slow convergence.

Either is acceptable with a one-sentence justification.

---

## Problem 6 — Aggregating many small returns (18 pts)

**(a) (4 pts)** For $N=100$:
$$
\mathbb{E}[\bar{r}] = \mu = 0.0004, \qquad \text{SD}(\bar{r}) = \frac{\sigma}{\sqrt{N}} = \frac{0.02}{\sqrt{100}} = \frac{0.02}{10} = 0.002.
$$
Diversification (averaging $N$ independent assets) shrinks volatility from $0.02$ to $0.002$ — a factor of $\sqrt{N}=10$ — because **averaging cancels noise** (the LLN force: $\operatorname{Var}(\bar{r})=\sigma^2/N\to 0$), but the *expected* return is the average of identical means and stays at $\mu$. The LLN drives $\bar{r}$ toward $\mu$; it does not change $\mu$.

**(b) (6 pts)** Standardize the threshold $\bar{r}=0$:
$$
\Pr(\bar{r}<0) = \Pr\!\left(\frac{\bar{r}-\mu}{\sigma/\sqrt{N}} < \frac{0-0.0004}{0.002}\right) = \Pr(Z < -0.2).
$$
From the table $\Pr(Z<-0.2)\approx 0.421$. So there is about a **42% chance** of a negative-return day. (The edge $\mu$ is tiny relative to the daily SE, so a losing day is nearly a coin flip — only slightly better than even.)

**(c) (4 pts)**
- **Dependence (assets move together):** correlation breaks the independence assumption behind $\operatorname{Var}(\bar{r})=\sigma^2/N$. When returns reinforce rather than cancel, the variance of the average falls *slower* than $1/N$ (in the extreme, not at all), so the true SE is **larger than $0.002$** and the "$\sigma/\sqrt{N}$" rate is wrong. *(This is why time-series/clustered standard errors exist — Week 2.)*
- **Fat tails:** even if independent, heavy tails mean a single monster day dominates the average, so the **normal approximation** in (b) fails — $\bar{r}$'s standardized distribution is too peaked and too heavy in the tails at $N=100$, and the $\Pr(Z<-0.2)$ reading is untrustworthy. The mechanism is the CLT's "no single contribution dominates" clause being violated.

**(d) (4 pts)** The **LLN** promises that as $N\to\infty$, $\bar{r}\xrightarrow{p}\mu$ — with enough independent assets the portfolio's average return collapses onto the true mean $0.0004$. The **CLT** adds the *shape*: rescaled by the SE $\sigma/\sqrt{N}$, the misses of $\bar{r}$ around $\mu$ follow the standard normal bell. It is the **CLT** that licenses the calibrated probability statement in (b): without knowing the shape of the cloud around $\mu$, Sam could say where $\bar{r}$ lands but never attach a number like "42%" to how often it dips below zero.

---

*End of solutions for PS 1.4. Cross-references: Ch 1.3 ($\operatorname{Var}(\bar{x})=\sigma^2/N$), Ch 1.4 (LLN, Chebyshev, CLT, fat-tail hierarchy), nb1.4 (simulations for Problem 5). Looks ahead to Ch 1.5, where $\sigma$ is replaced by $\hat\sigma$ and the normal becomes Student's $t$.*
