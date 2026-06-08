# Week 1 Assessment — Probability, Estimation, and Inference

This is the end-of-week assessment for Week 1. It has three parts. **Part A** is seven short-answer
questions on the conceptual spine of the week — conditioning and the two laws, the
expectation/variance/covariance algebra and its geometry, estimators and the bias–variance–MSE
decomposition, the LLN and CLT, and hypothesis testing. **Part B** is a small Monte Carlo you code,
run, and report on. **Part C** is the rubric that says how you will be graded, with explicit point
totals. An instructor answer key follows Part C.

The whole thing is designed for one focused sitting plus the coding task. Methods are limited to
Week 1: no regression, no matrix algebra beyond what Ch 1.2 used, no causal language. Show your
reasoning — a correct number with no argument earns little, and an honest "I am not sure, here is why"
earns more than a confident error.

**Total: 100 points.** Part A = 42, Part B = 48, Presentation/honesty woven through both = 10.

---

## Part A — Short answer (42 points; 6 points each)

Answer in two to five sentences each. Where a calculation is asked for, show the line of algebra.

**A1. (Conditioning and LIE.)** Devon splits on-chain wallets into "whales" (large holders, 20% of
wallets) and "retail" (the other 80%). The mean daily transaction count is 12 for whales and 3 for
retail. Using the Law of Iterated Expectations, compute the overall mean transaction count per
wallet. Then state in one sentence what $\mathbb{E}[\text{count} \mid \text{type}]$ *is* as a
mathematical object — a number or a random variable? — and why.

**A2. (Law of Total Variance, interpretation.)** Priya decomposes the variance of wildfire claim
sizes by county into a within-county piece and an across-county piece, and finds the across-county
piece is only 8% of the total. Her manager concludes: "County barely matters for claim size, so we
can ignore it." Give the one technical sense in which the 8% figure is exactly correct, and the one
modeling reason (from Ch 1.1 §7) the manager's conclusion could still be wrong.

**A3. (Covariance geometry.)** A classmate reports, for two return series, $\operatorname{sd}(X) =
0.10$, $\operatorname{sd}(Y) = 0.04$, and $\operatorname{Cov}(X,Y) = 0.006$. Without computing a
correlation, explain using a single Week-1 result why this triple is impossible, and state the
largest value $\operatorname{Cov}(X,Y)$ could take given those two standard deviations.

**A4. (Bias, variance, MSE.)** Priya considers two estimators of the mean claim $\mu$: the plain
sample mean $\bar{x}$ (unbiased, variance $720{,}000$ in dollars-squared) and a shrinkage rule
$\hat{\mu}_c = 0.9\,\bar{x}$ (which pulls the estimate toward zero). For the shrinkage rule, write its
bias as a function of $\mu$, then write its MSE using the bias–variance decomposition. For what range
of true $\mu$ does the shrinkage rule beat the sample mean on MSE? (You may leave the answer as an
inequality; take $\operatorname{Var}(\hat{\mu}_c) = 0.81 \times 720{,}000$.)

**A5. (LLN/CLT division of labor.)** In one sentence each, state what the Law of Large Numbers
promises about the sample mean and what the Central Limit Theorem additionally promises. Then explain
why, if the LLN were the *whole* story, there would be nothing left to do statistical inference about.

**A6. (Spot the error — heavy tails.)** Devon writes: "My crypto returns have a finite mean, so by the
CLT my sample mean of 200 daily returns is approximately normal and my 95% confidence interval is
trustworthy." Identify the flawed step in this reasoning. Your answer must name the specific
assumption that is doing the real work (not just "fat tails") and explain why "has a finite mean" is
not enough to rescue the argument.

**A7. (Spot the error — p-values.)** Sam tests a trading rule, gets $p = 0.03$ on a one-sided test
$H_0: \mu = 0$ vs. $H_1: \mu > 0$, and writes two sentences: *(i)* "There is a 3% chance the rule has
no real edge." *(ii)* "Since $p < 0.05$, I accept that the rule works." Each sentence contains a
distinct, named Week-1 error. Name both errors and give the corrected interpretation of $p = 0.03$.

---

## Part B — Mini-simulation: the size of a t-test under a skewed population (48 points)

You will measure something tests are *supposed* to control but often do not in finite samples: the
**actual Type I error rate (size)** of a one-sample t-test, and how it behaves when the population is
skewed. This ties together Ch 1.3 (sampling distributions), Ch 1.4 (CLT and its slow arrival under
skew), and Ch 1.5 (size, the t-test, the correct meaning of $\alpha$).

### The setup

A test run at nominal level $\alpha = 0.05$ *claims* that, when the null is true, it falsely rejects
only 5% of the time. The exact $t_{N-1}$ result requires normal data; real data are skewed, so the
true rejection rate can drift from 5%. You will measure that drift by brute-force simulation — the
same "fake the universe and look" move from Ch 1.3 §6.

### Tasks

**B1. Build the engine (12 pts).** Write a function that, for a given population, sample size $N$, and
number of repetitions $R$, draws $R$ samples of size $N$, runs a two-sided one-sample t-test of the
*true* null $H_0: \mu = \mu_{\text{true}}$ on each (you may use `scipy.stats.ttest_1samp`), and
returns the fraction of samples for which $p < 0.05$. Because the null is true by construction, that
fraction is the **empirical size**. Pin your random seed and state it.

**B2. Two populations (12 pts).** Run B1 for two populations, both with a known, finite mean you plug
in as $\mu_{\text{true}}$:

- a **standard normal** (the textbook-friendly baseline), and
- a **lognormal** calibrated to be clearly right-skewed (e.g. `rng.lognormal(mean=0, sigma=1)`),
  whose true mean is $e^{0.5} \approx 1.6487$ — use that exact value as $\mu_{\text{true}}$, not the
  sample mean.

For each population, report empirical size at $N \in \{5, 15, 30, 100, 1000\}$ with $R \ge 20{,}000$.
Present the results as a small table (population $\times$ $N$).

**B3. Report and interpret (16 pts).** In one short paragraph plus one figure (empirical size vs.
$N$, with a horizontal reference line at 0.05 and both populations on the same axes), answer:

- For the normal population, is the empirical size close to 0.05 even at small $N$? Should it be?
- For the lognormal, at which $N$ does the size come within, say, 0.005 of the nominal 0.05? Connect
  this to the Ch 1.4 statement that the CLT arrives *slowly* for skewed populations.
- Which direction does the skew push the size at small $N$ (too many or too few false rejections),
  and why does that make a naive t-test on small skewed samples *not* as safe as its label claims?

**B4. Honest uncertainty (8 pts).** Your empirical size is itself an estimate — it has a standard
error. Using Week-1 tools, give an approximate standard error for an empirical size near 0.05 computed
from $R = 20{,}000$ repetitions, and state whether a gap like "0.05 vs. 0.058" is real signal or
plausibly Monte Carlo noise. (Hint: each repetition is a Bernoulli reject/not-reject; you derived the
standard error of a mean of independent draws in Ch 1.3.)

### Deliverables

A single notebook or script that runs end-to-end on a fresh environment with the stated seed, plus a
short write-up (the paragraph and figure from B3, the table from B2, and the calculation from B4).
Code must be reproducible: same seed, same numbers. State your software versions.

**Optional extension (no extra points, for the curious):** swap the lognormal for a Student's
$t(\nu = 2)$, whose variance is infinite, and report what happens to the empirical size. Explain in
one sentence why this population breaks the test's premise outright rather than merely slowing
convergence.

---

## Part C — Analytic rubric (point allocations explicit)

Each row is scored independently at one of four levels. Part-A rows are graded per question against
the answer key; the four Part-A criteria below describe *how* points within those 42 are awarded.
Part B is graded by the task-point allocation above, refined by the criteria here. The
Presentation/honesty row contributes 10 points spanning both parts.

| Criterion | Excellent | Proficient | Developing | Missing | Points |
|---|---|---|---|---|---|
| **Conceptual correctness (Part A)** | All claims correct; uses the right Week-1 result by name; distinguishes estimator/estimate, $\mathbb{E}[X\mid Y]$ as a random variable, $\Pr(\text{data}\mid H_0)$ vs. $\Pr(H_0\mid\text{data})$ cleanly. | Minor slip in one item; core logic sound. | Right intuition, wrong mechanism or mislabeled law in 2+ items. | Pervasive confusion of the central distinctions. | 24 |
| **Algebra / numerics (Part A)** | LIE, Cauchy–Schwarz bound, and MSE decomposition carried out correctly with shown steps. | One arithmetic error, method correct. | Method partly right, multiple errors. | Not attempted or unrelated. | 18 |
| **Code correctness & reproducibility (Part B)** | Engine correct; null is true by construction; seed pinned; runs end-to-end; same seed reproduces table exactly. | Runs and is essentially correct; minor non-reproducibility (e.g. unseeded plot jitter). | Logic flaw (e.g. tests sample mean instead of $\mu_{\text{true}}$, or too few reps); partial output. | Does not run or wrong target tested. | 24 |
| **Interpretation & communication (Part B3)** | Correctly reads the normal-vs-lognormal contrast, ties slow convergence to the CLT, names the direction of size distortion and why it matters. | Mostly correct reading; one link missing. | Describes the plot without interpreting it. | Absent or wrong. | 14 |
| **Honest treatment of uncertainty (B4 + throughout)** | Correct Monte Carlo SE; correctly judges 0.05-vs-0.058 against it; flags any "looks close" claim with a number. | SE roughly right; judgment sound. | Acknowledges noise but no quantification. | Treats simulated numbers as exact truth. | 10 |
| **Presentation, units, no overclaiming** | Clean prose; units on every number; no "proves," "accepts the null," or significance-equals-importance language. | One stylistic lapse. | Several lapses; verdicts without magnitudes. | Unreadable or rife with banned claims. | 10 |

**Total: 100 points.** (Part A criteria sum to 42; Part B criteria sum to 38; the final two rows of 10
each span both parts, and the rubric is normalized so the maximum awarded is 100.)

A note on the spirit of the last two rows: this course rewards *calibrated* honesty. An answer that
says "my empirical size was 0.058, but with a Monte Carlo standard error around 0.0015 that is a real
gap, not noise" outscores "the size was 0.058, basically 0.05" even though both report the same
number. Knowing how much to trust your own number is the entire point of Week 1.

---

## Instructor answer key / model-answer sketch

**A1.** By LIE, $\mathbb{E}[\text{count}] = \mathbb{E}\big[\mathbb{E}[\text{count}\mid\text{type}]\big]
= 0.20(12) + 0.80(3) = 2.4 + 2.4 = 4.8$ transactions. $\mathbb{E}[\text{count}\mid\text{type}]$ is a
**random variable** — a function of the random type, taking 12 with probability 0.20 and 3 with
probability 0.80 — not a single number; the single numbers are its two realized values per group.
*(Full credit requires both the 4.8 and the "random variable" point.)*

**A2.** Technically correct sense: the across-county term $\operatorname{Var}(\mathbb{E}[\text{claim}
\mid \text{county}])$ genuinely is 8% of the total variance — given *this* county coding, only 8% of
the wobble comes from differences in county means; knowing the county would remove at most that 8%.
Why the conclusion can still fail: the decomposition is only as meaningful as the conditioning
variable (Ch 1.1 §7). If "county" is too coarse (the real structure is finer — fire-zone, vegetation,
building age), genuine across-group variation gets misfiled as within-group noise, so 8% *understates*
how much an informative grouping could explain. The math is exact; the story depends on whether the
grouping carves the world at its joints.

**A3.** By Cauchy–Schwarz (Ch 1.2 §4), $|\operatorname{Cov}(X,Y)| \le
\operatorname{sd}(X)\operatorname{sd}(Y) = 0.10 \times 0.04 = 0.004$. The reported $0.006 > 0.004$ is
impossible (it would force $|\rho| > 1$). The largest possible covariance is $0.004$ (attained only
when $X$ and $Y$ are perfectly linearly related, $\rho = +1$).

**A4.** $\hat{\mu}_c = 0.9\bar{x}$, so $\mathbb{E}[\hat{\mu}_c] = 0.9\mu$ and
$\operatorname{Bias} = 0.9\mu - \mu = -0.1\mu$. Then
$$\operatorname{MSE}(\hat{\mu}_c) = \operatorname{Var}(\hat{\mu}_c) + \operatorname{Bias}^2
= 0.81(720{,}000) + (0.1\mu)^2 = 583{,}200 + 0.01\mu^2.$$
The sample mean has $\operatorname{MSE} = 720{,}000$. Shrinkage wins when
$583{,}200 + 0.01\mu^2 < 720{,}000 \Rightarrow 0.01\mu^2 < 136{,}800 \Rightarrow \mu^2 < 13{,}680{,}000
\Rightarrow |\mu| < 3{,}699$ (dollars). So for true means smaller than about \$3,700 the bias paid is
worth the variance saved; for larger $\mu$ the squared bias dominates and the sample mean wins.
*(Credit the inequality and the correct bias sign; the exact \$3,699 is a bonus.)*

**A5.** LLN: as $N\to\infty$, $\bar{x}\xrightarrow{p}\mu$ — the sample mean concentrates on (converges
in probability to) the true mean. CLT: additionally, the *standardized* mean
$(\bar{x}-\mu)/(\sigma/\sqrt{N})\xrightarrow{d} N(0,1)$ — the rescaled misses have a known bell shape.
If only the LLN held, $\bar{x}$ would for large $N$ be essentially the constant $\mu$ with no
describable spread, so there would be no distribution of "misses" to build confidence intervals or
p-values from; the CLT supplies exactly that shape, keeping inference alive.

**A6.** The flawed step is invoking the CLT as if a finite *mean* were the sufficient condition. The
real load-bearing assumption is **finite variance** (plus enough observations relative to the tail
weight). "Has a finite mean" sits low on the hierarchy: a distribution can have a perfectly good mean
yet infinite variance (e.g. Student's $t$ with $\nu = 2$), in which case there is no $\sigma$ to
standardize by and the CLT does not apply at all; and even with finite-but-large variance (heavy
tails, low-$\nu$ $t$), the CLT arrives so *slowly* that 200 observations need not be nearly enough for
normality. Crypto returns live in that heavy zone, so the interval built on 200 days is "built on
sand." *(Full credit names finite variance specifically and the slow-convergence point.)*

**A7.** Sentence (i) is the **p-value-as-posterior** error: $p = 0.03$ is
$\Pr(\text{a }t\text{ this extreme or more}\mid H_0\text{ true})$, *not* $\Pr(H_0\text{ true}\mid
\text{data})$; swapping the conditional bar requires a prior and Bayes' rule and is unsupported.
Sentence (ii) is the **"accept the null / significance settles it"** error — actually two-in-one: one
never "accepts" anything, and rejecting $H_0$ does not establish the rule "works" (effect could be
tiny, non-causal, or out-of-sample fragile). Correct reading: *if the rule truly had zero edge, a
one-sided t-statistic at least as large as Sam's would occur about 3% of the time by chance* — mild
evidence against the null, no statement about the rule's economic value.

**Part B expected results (for grading).**

- *Engine (B1):* must test against the plugged-in true mean, not the sample mean; size = fraction
  with $p<0.05$. A common bug is calling `ttest_1samp(sample, sample.mean())`, which forces $t=0$ and
  gives size $\approx 0$ — flag this as the logic flaw under "code correctness."
- *Normal (B2/B3):* empirical size should sit near 0.05 at *every* $N$ including $N=5$, because the
  exact $t$ result holds for normal data at all sample sizes. Expect roughly $0.048$–$0.052$.
- *Lognormal (B2/B3):* at small $N$ the size deviates noticeably from 0.05; with this right-skewed
  population the two-sided test is typically **mildly liberal-to-conservative depending on $N$**, and
  students should report the *direction they observe* and tie it to slow CLT convergence. By
  $N \approx 100$–$1000$ the size should be within a few thousandths of 0.05. Accept any internally
  consistent reading that (a) shows the normal is well-behaved at all $N$, (b) shows the lognormal
  converging to 0.05 only as $N$ grows, and (c) attributes the gap to the CLT arriving slowly under
  skew.
- *Uncertainty (B4):* each repetition is Bernoulli($p\approx0.05$); the empirical size is a sample
  mean of $R$ such draws, so its standard error is $\sqrt{p(1-p)/R} = \sqrt{0.05\cdot0.95/20{,}000}
  \approx 0.00154$. A gap of 0.05 vs. 0.058 is $0.008$, about five Monte Carlo standard errors — that
  is **real signal, not noise**. (A gap of 0.05 vs. 0.051 would be noise.)

**Quick grading heuristic.** The two highest-signal items for separating strong from weak work are
A6/A7 (do they correctly locate the assumption and the conditional?) and B1/B4 (is the null true by
construction, and do they put a standard error on a simulated number rather than reading it as exact?).
A student who nails those four has the Week-1 mindset; the rest is execution.
