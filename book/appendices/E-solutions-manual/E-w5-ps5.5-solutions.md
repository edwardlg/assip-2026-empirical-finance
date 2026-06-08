# Solutions — Problem Set 5.5 (Reproduce a BDM Placebo-DiD False Positive)

Full worked solutions to `book/weeks/week-05/ps5.5.md`, covering Chapter 5.5 (Reader's Guide:
**Bertrand, Duflo & Mullainathan, 2004**). Notation follows the Conventions. The DiD specification under
study is

$$
Y_{st} \;=\; \alpha_s \;+\; \lambda_t \;+\; \beta\, D_{st} \;+\; u_{st},
$$

$s$ = state, $t$ = year, $\alpha_s$ state fixed effects, $\lambda_t$ year fixed effects,
$D_{st}=\mathbf 1\{\text{state }s\text{ "treated" in year }t\}$, $u_{st}$ the within-state error. A
**placebo law** assigns $D_{st}$ at random with **no real intervention**, so $\beta = 0$ by construction.
The recurring theme of the key: **the placebo experiment measures the *size* of the test (Week 1); a
rejection rate far above 0.05 catches the conventional standard error being too small; the cause is
positive within-state serial correlation, which shrinks the effective sample and inflates the
$t$-statistic; the cures (cluster by state, collapse to pre/post, block bootstrap) restore honest size,
but all lean on having many clusters (Week 4's few-clusters caution).**

**Illustrative numbers.** Where a concrete rejection rate is used it is a labeled value from the
companion simulation `nb5.5` (naive $\approx 0.35$ at $\rho = 0.8$, $T = 20$, 50 states; clustered /
collapsed / block-bootstrapped $\approx 0.05$), **not** a figure quoted from BDM's tables. The
transportable fact is the direction and severity. The AR(1) variance algebra below was verified in
`python3` (exact double-sum of the covariance matrix versus the closed form).

---

## Problem 1 — The placebo experiment as a size test (Week 1 bridge) (16 pts)

**(a)** [4 pts] **Size** is the probability the test rejects the null *when the null is true* — the
Type-I-error rate, the $\alpha$ you set in advance. **Power** is the probability the test rejects *when
the null is false* — one minus the Type-II-error rate, the chance of catching a real effect. If a
researcher calls $|t| > 1.96$ "significant at 5%," she is promising the size equals **$0.05$**: on data
where the true $\beta = 0$, the test should wrongly fire only 5% of the time.

**(b)** [4 pts] In the placebo experiment the law is invented — a random subset of states is *declared*
treated in a random year, but **no real intervention ever happened to them**, so the **true effect is
zero by construction**. The step that guarantees it is the assignment itself: $D_{st}$ is drawn at random
and laid on top of an outcome that was generated with *no* dependence on $D$. Because $\beta = 0$ is
*known* (you authored it), there is no counterfactual ambiguity: any run that returns $|t| > 1.96$ has
rejected a null that is true, which is the textbook definition of a false positive / Type-I error. Every
rejection is, with certainty, a mistake.

**(c)** [4 pts] Across $R$ replications, the **fraction that reject** is a Monte Carlo estimate of the
**true (empirical) size of the test** — the actual Type-I-error rate of the conventional-SE DiD procedure
on a serially correlated panel, $\widehat{\text{size}} = \frac1R\sum_{r=1}^{R}\mathbf 1\{|t_r| > 1.96\}$.
This is exactly the Week-1 coin-flip lab logic: there you built a universe with a *genuinely fair* coin
and counted how often your test wrongly called it biased, recovering the real size of that test; here you
build a universe with a *genuinely null* law and count how often DiD wrongly calls it real. In both, you
play God so that the right answer is known, then audit the procedure against it.

**(d)** [4 pts] **Decision rule.** If the placebo rejection rate comes back near $0.05$, the conventional
standard error is **honest** — it is sized as advertised, rejecting true nulls at the promised 5%. If it
comes back far above $0.05$, you have caught the standard error being **too small**: the chain is *SE too
small $\Rightarrow$ $t = \hat\beta/\text{SE}$ too large $\Rightarrow$ the inflated $t$ crosses $1.96$ far
more often than 5% of the time $\Rightarrow$ over-rejection.* The placebo design converts the abstract
worry "I suspect the SEs are wrong" into the measured number "here is the false-positive rate."

---

## Problem 2 — Reading a placebo rejection rate well above 5% (14 pts)

**(a)** [4 pts] $0.35$ means: out of 100 pure-noise placebo laws — laws with *no real effect whatsoever* —
this specification would declare **about 35** "statistically significant at the 5% level." It should
declare about **5**. The test that advertises a 1-in-20 false-positive rate actually fires on better than
1-in-3 of genuinely null data. The advertised 5% test is, in truth, close to a coin-flip-ish test: its
"significance" stamp is worth a small fraction of what it claims.

**(b)** [3 pts] **Refutation.** This is not Monte Carlo noise — it is a real bias in the *test*, and more
replications would only sharpen the estimate of $0.35$, not move it toward $0.05$. The Monte Carlo
standard error of $\hat p = 0.35$ over $R = 600$ independent runs is
$$
\text{SE}(\hat p) = \sqrt{\frac{\hat p(1-\hat p)}{R}} = \sqrt{\frac{0.35 \times 0.65}{600}} \approx \sqrt{0.000379} \approx 0.019.
$$
So $0.35$ sits about $(0.35 - 0.05)/0.019 \approx 15.4$ Monte Carlo standard errors above the nominal
$0.05$ — an astronomically improbable gap if the true size were really $0.05$. Adding replications shrinks
that $0.019$ toward zero and makes the verdict *more* damning, not less. (This is the Week-1 standard
error of a proportion, reused.)

**(c)** [4 pts] If this were the field default and 200 researchers each studied a genuinely-null policy,
roughly $200 \times 0.35 \approx \mathbf{70}$ would publish a "significant" finding — 70 discoveries of
effects that do not exist. With an honest test only about $200 \times 0.05 = 10$ false alarms would slip
through. This is precisely the mechanism by which a broken standard-error formula can populate a
literature with phantom effects: each individual study looks rigorous (it cleared $|t| > 1.96$), but the
threshold it cleared was never the 5% gate it claimed to be, so false positives accumulate at the
$35\%$ rate instead of the $5\%$ rate. That accumulation across hundreds of DiD papers is the danger BDM
set out to measure.

**(d)** [3 pts] $0.35$ does **not** say the point estimate $\hat\beta$ is biased. Over the placebo
replications $\hat\beta$ is centered at zero on average — the *estimate* is fine, because the placebo
truly has no effect and the regression's coefficient is, on average, right. What is wrong is the **spread
of $\hat\beta$**: it bounces around far more than the conventional formula's standard error claims, so the
$t = \hat\beta/\text{SE}$ is too big too often. This is a problem of **inference** (the standard error /
$t$-stat), not of **estimation** (the coefficient itself). The placebo experiment indicts the standard
error, not $\hat\beta$.

---

## Problem 3 — Why serial correlation inflates the t-stat: an AR(1) argument (20 pts)

**(a)** [4 pts] **Assumed (independence) variance.** If $u_1,\dots,u_T$ were independent each with
variance $\sigma^2$, the sample mean $\bar u = \frac1T\sum_t u_t$ would have
$$
\operatorname{Var}_{\text{indep}}(\bar u) = \frac{\sigma^2}{T}.
$$
(The Week-1 $\sigma^2/n$ fact with $n = T$: averaging $T$ independent draws shrinks the variance by a
factor of $T$.)

**(b)** [8 pts] **True variance under AR(1).** Start from the exact formula for the variance of a sum:
$$
\operatorname{Var}(\bar u) = \frac{1}{T^2}\sum_{t=1}^{T}\sum_{r=1}^{T}\operatorname{Cov}(u_t,u_r),
\qquad \operatorname{Cov}(u_t,u_r) = \sigma^2\rho^{|t-r|}.
$$
Group the $T^2$ terms by the lag $k = |t-r|$. There are $T$ diagonal terms ($k=0$, each $\sigma^2$), and
for each lag $k = 1,\dots,T-1$ there are $2(T-k)$ off-diagonal terms (each $\sigma^2\rho^k$). Hence
$$
\operatorname{Var}(\bar u) = \frac{\sigma^2}{T^2}\left[\,T + 2\sum_{k=1}^{T-1}(T-k)\rho^{k}\,\right]
= \frac{\sigma^2}{T}\left[\,1 + \frac{2}{T}\sum_{k=1}^{T-1}(T-k)\rho^{k}\,\right]. \qquad\blacksquare
$$
The bracket is the **inflation factor** — it equals $1$ only when $\rho = 0$; for $\rho > 0$ every term is
positive, so it exceeds $1$.

*Concrete case $T = 3$, $\rho = 0.8$, $\sigma^2 = 1$.* The three covariance "rings":
- **diagonal** ($k=0$): $3$ terms $\times\,1 = 3$;
- **lag-1** ($k=1$): $2(3-1) = 4$ terms $\times\,\rho = 4(0.8) = 3.2$;
- **lag-2** ($k=2$): $2(3-2) = 2$ terms $\times\,\rho^2 = 2(0.64) = 1.28$.

Sum of covariances $= 3 + 3.2 + 1.28 = 7.48$, so
$$
\operatorname{Var}(\bar u) = \frac{7.48}{3^2} = \frac{7.48}{9} \approx \mathbf{0.8311}.
$$
The independence value from (a) is $\sigma^2/T = 1/3 \approx 0.3333$, so the **ratio** is
$$
\frac{0.8311}{0.3333} \approx \mathbf{2.49}.
$$
Even at $T = 3$ the true variance of the mean is about $2.5\times$ what the conventional formula assumes.

**(c)** [4 pts] **Long-run factor.** As $T \to \infty$ with $\rho$ fixed, the bracket converges to
$\dfrac{1+\rho}{1-\rho}$. At $\rho = 0.8$:
$$
\frac{1+0.8}{1-0.8} = \frac{1.8}{0.2} = \mathbf{9}.
$$
Filling in the sentence: "Ignoring serial correlation makes the reported variance of $\bar u$ too small
by a factor of about **9**, so the reported standard error is too small by a factor of about
$\sqrt 9 = \mathbf 3$, and the t-statistic is therefore too **large** by a factor of about **3**." (The
variance is off by $9\times$; the standard error, being its square root, by $3\times$; and since
$t = \hat\beta/\text{SE}$, dividing by an SE that is one-third the honest size triples the $t$.)

**(d)** [4 pts] **Effective sample size.** The independence formula treats $T$ correlated years as $T$
independent pieces of information. The honest count is
$$
T_{\text{eff}} = \frac{T}{\text{inflation factor}} = \frac{T(1-\rho)}{1+\rho}.
$$
At $T = 20$, $\rho = 0.8$: $T_{\text{eff}} = 20/9 \approx \mathbf{2.2}$. So *twenty* serially correlated
years carry only about *two* years' worth of independent information: because each year's shock largely
carries over to the next, consecutive observations are near-duplicates and the panel contains far less
news than its raw length suggests. The conventional formula divides the variance by the full $T = 20$
when it should divide by $\approx 2.2$, which is *exactly* why it reports a standard error too small by
$\sqrt{20/2.2} = \sqrt 9 = 3$. This is also why **longer panels make the over-rejection worse**: as $T$
grows with $\rho$ fixed, the gap between $T$ and the capped $T_{\text{eff}} \to T(1-\rho)/(1+\rho)$ widens,
so the formula's overcounting of independent information — and the resulting $t$-inflation — grows with
panel length, just as the Reader's Guide claims.

---

## Problem 4 — The three fixes: what each one does and why it works (22 pts)

**(a)** [6 pts] **Cluster by state.** The cluster-robust standard error replaces the conventional
$\operatorname{Var}(\hat{\boldsymbol\beta}) = \sigma^2(\mathbf X'\mathbf X)^{-1}$ with a sandwich built on
a **block-diagonal** residual covariance $\boldsymbol\Omega$ — **one block per state**:
$$
\boldsymbol\Omega = \begin{pmatrix}\boldsymbol\Omega_1 & & \\ & \ddots & \\ & & \boldsymbol\Omega_{50}\end{pmatrix},
$$
where each within-state block $\boldsymbol\Omega_s$ is left **unrestricted** — the residuals within a
state may be correlated *arbitrarily* across all of that state's years — while across states (off the
blocks) residuals are assumed independent (zero). This is exactly the right shape for the disease:
Problem 3 showed the damage comes from positive correlation *within* a state's own time series, the very
$\rho^{|t-r|}$ pattern the conventional formula sets to zero. Clustering by state stops assuming that
within-state independence and instead estimates the within-block correlation from the data, so the
reported standard error finally accounts for the $9\times$ variance inflation. This is the Chapter 2.4
cluster-robust fix with the cluster set to the **unit of treatment assignment** (the state) — the reason
Priya clustered by state in Week 4.

**(b)** [6 pts] **Collapse to pre/post.** Average each state's outcome over all its pre-law years into one
"before" number and over all its post-law years into one "after" number, leaving **two observations per
state**, then run the simple before/after DiD on this collapsed panel. Why this restores honest size: with
only one observation per state per period, there is **no within-period time dimension left** — you cannot
have serial correlation *within* a single averaged number, so there is no $\rho^{|t-r|}$ structure for the
formula to misread. The persistence has been integrated out into the two cell means. The **cost** is a
Week-1 size–power trade-off: collapsing **discards information** — you have thrown away every year-to-year
movement within each period — so the test loses **power**, and the probability of a **Type-II error**
(missing a real effect when one exists) rises. You buy honest size by spending power; you cannot drive
both error rates to zero with fixed data.

**(c)** [6 pts] **Block bootstrap.** A *naive* bootstrap resamples individual state-year observations with
replacement and recomputes $\hat\beta$ each time to build a sampling distribution. That fails here for the
*same* reason the conventional formula fails: drawing observations independently **shatters each state's
serial-correlation structure**, manufacturing a bootstrap world in which the within-state years behave as
if independent — so the bootstrap standard error inherits the very independence assumption that is false,
and comes out too small. The **block** bootstrap instead resamples **whole states** — each selected
state's entire time series is kept intact as one block — which **preserves each state's serial-correlation
structure** in every resample. The bootstrap distribution of $\hat\beta$ then reflects the true
year-to-year dependence, and the resulting standard error is honest. (The "block" is the unit whose
internal dependence you must not break — here, the state.)

**(d)** [4 pts] **Unification.** Two routes to the same honest size:
- **Cluster by state** — *model the dependence honestly*: it keeps **all** the data and estimates the
  correct (larger) standard error by allowing arbitrary within-state correlation.
- **Block bootstrap** — *model the dependence honestly*: it likewise keeps all the data and lets the
  resampling distribution carry the within-state correlation.
- **Collapse to pre/post** — *remove the dependence by destroying the structure that carries it*: it
  averages away the within-period time dimension, so there is no serial correlation left to misread.

**Default with many states:** cluster by state. It restores honest size while keeping all the data, so —
unlike the collapse — it sacrifices the least power, and unlike the block bootstrap it is a single
closed-form computation. (This is why clustering by the treatment unit became the field's default.)

---

## Problem 5 — The few-clusters caution (Week 4 bridge) (16 pts)

**(a)** [4 pts] **Mechanism.** The cluster-robust formula estimates the within-cluster correlation
*indirectly*, from how the cluster-level sums vary **across** clusters. With many states, there are plenty
of clusters to learn that across-cluster variability from, and the estimate is reliable. With only a
handful of states there is **not enough across-cluster variation to estimate** — the sandwich's
"meat" is a sum over only a few cluster terms, which understates the true variability (it has too few
pieces and is biased downward in finite samples). So the clustered standard error becomes **too small
again**, the $t$-stat re-inflates, and the test over-rejects — the honest $\approx 0.05$ with 50 states
climbs back well above $0.05$ with 6. The Chapter 2.4 / Week-4 rule of thumb is that clustering needs on
the order of **30 to 50 clusters** to be trustworthy.

**(b)** [4 pts] **The designs that need the cure most.** An enormous share of influential DiD studies have
**few treated units** — Priya's wildfire-regulation design had a *single* treated state, and Card–Krueger
had essentially one. The uncomfortable implication: BDM's recommended cure (cluster / block bootstrap)
**works best precisely where it is needed least** — when there are many states (50), exactly the regime
that was *least* in danger. In the small-number-of-treated-units designs that need help most, the very fix
can itself over-reject. The cure is a large-number-of-clusters cure; it quietly assumes the easy case.

**(c)** [4 pts] **Further corrections.** The **wild cluster bootstrap of Cameron, Gelbach & Miller
(2008)** and **few-cluster $t$ adjustments** are *for* the small-number-of-clusters regime: they fix the
fact that plain cluster-robust standard errors are biased downward — and the reference $t$ distribution is
wrong — when clusters are few, restoring something closer to honest size where ordinary clustering has too
few clusters to do so on its own.

**(d)** [4 pts] **Spec-discipline takeaway (Conventions §4).** The referee's one-line rule: clustering
must be done **at the level the treatment varies** — *and* the honesty of the resulting standard error
depends not on the sample size $N$ but on the **number of clusters** (here, the number of states / treated
units). A table reporting "$N = 1{,}000{,}000$ borrower-months, clustered by state, 6 states" can still
have untrustworthy $t$-stats because, with only **6 clusters**, the cluster-robust formula has too little
across-cluster variation to estimate the within-cluster correlation — the million rows are not a million
independent pieces of information, they are 6 highly-correlated blocks, and it is the *6*, not the million,
that governs whether inference is honest.

---

## Problem 6 — Replication design: specify the placebo Monte Carlo for `nb5.5` (12 pts)

**(a)** [4 pts] **Data-generating process (Conventions §4 format).** Build a *null* state-year panel:

- **Dimensions:** $S = 50$ states $\times$ $T = 20$ years (a long panel, where serial correlation does its
  worst).
- **Outcome:** $Y_{st} = \mu_s + \lambda_t + u_{st}$, with **state effects** $\mu_s$ (one persistent
  level per state), **year effects** $\lambda_t$ (one common shock per year), and **AR(1) within-state
  errors** $u_{st} = \rho\,u_{s,t-1} + e_{st}$ with persistence $\rho$ (innovation variance scaled to keep
  $\operatorname{Var}(u_{st})$ constant as $\rho$ varies, so $\rho$ changes only the *correlation*, not the
  noise level).
- **True treatment effect:** **zero — there is no treatment term in the DGP at all.** The panel must
  contain no $D_{st}$ and no $\beta$, because the experiment measures *size*, which is defined only under a
  true null: if any real effect were baked in, a rejection might be a true positive and the rejection rate
  would no longer be a clean Type-I-error rate.

**(b)** [4 pts] **Placebo-assignment and estimation loop (one replication).**
1. **Assign a placebo law:** draw a random subset of states (e.g. half) to be "treated," and for each a
   random onset year; set $D_{st} = 1$ from that state's onset onward, $0$ otherwise. Nothing in $Y$
   depends on this $D$ — it is laid on top of the null panel.
2. **Estimate the spec:** outcome $Y_{st}$ · treatment $D_{st}$ · fixed effects = state ($\alpha_s$) + year
   ($\lambda_t$) · standard-error flavor = **conventional/classical** (the one under audit) · sample = all
   $S \times T$ cells. I.e. run $Y_{st} = \alpha_s + \lambda_t + \beta D_{st} + u_{st}$.
3. **Record the statistic:** $t_r = \hat\beta / \text{SE}(\hat\beta)$, and the rejection indicator
   $\mathbf 1\{|t_r| > 1.96\}$.

Over $R$ replications, average the rejection indicators:
$\widehat{\text{size}} = \frac1R\sum_r \mathbf 1\{|t_r| > 1.96\}$ — the headline placebo rejection rate.
Each replication must draw a **fresh** placebo assignment so that the $R$ rejection indicators are
independent draws from the test's true sampling behavior; reusing one assignment would give $R$ copies of a
single draw and estimate nothing.

**(c)** [4 pts] **The two mechanism sweeps.**
- **(i) Persistence sweep.** Re-run the headline Monte Carlo for $\rho \in \{0, 0.2, 0.4, 0.6, 0.8, 0.9\}$
  and plot the naive rejection rate against $\rho$. **At $\rho = 0$ the rate must return $\approx 0.05$** —
  with independent errors the conventional formula is correct, so an honest simulation *has* to reproduce
  the nominal size there (if it does not, the code is wrong, not the theory). As $\rho$ rises, the rate must
  **climb** (toward $\approx 0.35$ at $\rho = 0.8$).
- **(ii) Fixes overlay.** On the same axes (or a companion bar chart) overlay the Problem-4 fixes —
  cluster-by-state and collapse-to-pre/post — which stay flat near $0.05$ across all $\rho$.

Together these two plots constitute *evidence the culprit is autocorrelation, not chance*: the naive rate
rises monotonically **with the one thing being dialed** (serial correlation), pinned to $0.05$ at $\rho =
0$ and worsening as persistence grows, while the fixes that *target* within-state dependence flatten it back
to nominal. That is the Reader's-Guide reading order made operational — **symptom** (the headline
over-rejection), **mechanism** ($\rho$ sweep isolates serial correlation as cause), **cure** (the fixes
restore size).

---

*End of solutions for Problem Set 5.5. The thread from Week 1 to Week 4 runs straight through: the placebo
experiment is a Week-1 size measurement; the over-rejection is caused by within-state serial correlation,
which by the AR(1) algebra inflates $\operatorname{Var}(\bar u)$ by the factor $\frac{1+\rho}{1-\rho}$
($=9$ at $\rho = 0.8$), tripling the $t$-stat and cutting 20 years down to $\approx 2.2$ years of effective
information; the cures (cluster by state — the Chapter 2.4 block-diagonal $\boldsymbol\Omega$; collapse to
pre/post; block bootstrap) restore honest size; and all the cluster-based cures inherit Week 4's
few-clusters caution, so they reach the many-state designs that needed help least and require the wild
cluster bootstrap (Cameron, Gelbach & Miller, 2008) where treated units are few. The single discipline:
on a persistent panel a small standard error is not the same as an honest one — the lesson of
Bertrand, Duflo & Mullainathan (2004), which you reproduce on your own laptop in `nb5.5`.*
