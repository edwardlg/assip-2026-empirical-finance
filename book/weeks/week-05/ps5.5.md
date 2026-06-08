# Problem Set 5.5 — Reproduce a BDM Placebo-DiD False Positive

**Covers Chapter 5.5 (Reader's Guide: Bertrand, Duflo & Mullainathan, 2004).** This set turns the
Reader's-Guide reading of **Bertrand, Duflo & Mullainathan (2004)** into a reproduction you reason about
on paper and then run for real in the companion notebook `nb5.5`. The methods you need were all built in
earlier weeks: the **size of a test** as the true Type-I-error rate $\alpha$ you promised to honor and
the simulation logic for measuring it (Week 1); the **cluster-robust standard error** with its
block-diagonal residual covariance $\boldsymbol\Omega$ and the **few-clusters** caution (Chapter 2.4 and
Week 4); and the **two-way fixed-effects difference-in-differences** regression with treatment assigned
at the state level and standard errors clustered by the unit of treatment (Week 4). Notation follows the
Conventions. The DiD specification under study, carried throughout, is

$$
Y_{st} \;=\; \alpha_s \;+\; \lambda_t \;+\; \beta\, D_{st} \;+\; u_{st},
$$

where $s$ indexes states, $t$ indexes years, $\alpha_s$ are state fixed effects, $\lambda_t$ are year
fixed effects, $D_{st} = \mathbf 1\{\text{state } s \text{ is "treated" in year } t\}$ is the law dummy,
and $u_{st}$ is the within-state error. A **placebo law** is a $D_{st}$ assigned at random with **no real
intervention behind it**, so the true coefficient is $\beta = 0$ **by construction**.

Six problems, escalating, **100 points total**. No computer is needed for Problems 1–5 — every number you
need is supplied or derivable by hand; the companion notebook `nb5.5` lets you *generate* the rejection
rates in Problems 1, 4, and 5 yourself. **The grading rule of this set:** a claim about a standard error,
a rejection rate, or a t-statistic reported *without naming what assumption it rests on and whether that
assumption is true in the placebo world* earns half credit at most. As in Week 1, the *reasoning about why
the test mis-sizes* is the skill, not the arithmetic. When you name a threat, name the design that
addresses it (spec discipline, Conventions §4).

> **Illustrative-number warning, read once.** Bertrand, Duflo & Mullainathan (2004) report a headline
> placebo rejection rate for the conventional standard error that is **far above the nominal 5%** — many
> times too large. Do **not** quote a precise figure from the paper from memory; the Reader's Guide flags
> the often-cited number as `[CHECK]`. Where this set needs a concrete rejection rate to reason about, it
> uses **clearly-labeled illustrative values from *your own* simulated panel in `nb5.5`** — principally a
> naive rejection rate of about **0.35** at AR(1) persistence $\rho = 0.8$ over $T = 20$ years with 50
> states. These are properties of *that* data-generating process, not universal constants and not BDM's
> exact table numbers. The robust, transportable fact is the *direction and severity*: conventional DiD
> standard errors over-reject badly, and clustering, collapsing, and the block bootstrap pull the
> rejection rate back toward 0.05.

---

## Problem 1 — The placebo experiment as a size test (Week 1 bridge) (16 points)

This problem is pure reasoning — no arithmetic. It pins down *what* the placebo-law experiment measures
and *why* that is exactly the Week-1 notion of test size.

**(a)** [4 pts] In one sentence each, define the **size** of a test and the **power** of a test in the
Week-1 sense (in terms of a true null, a false null, and the probability of rejecting). Then state, in
one sentence, what value the size *should* equal if a researcher runs the DiD regression above and calls
$|t| > 1.96$ "significant at 5%."

**(b)** [4 pts] Explain why, in the placebo experiment, **every** rejection is *necessarily* a false
positive (a Type-I error) — with no ambiguity about what "should" have happened. Use the phrase "true
effect zero by construction," and say which step of building the placebo guarantees it.

**(c)** [4 pts] Describe the placebo Monte Carlo as a *size-measurement procedure*: across $R$
replications, each assigning a fresh random placebo law to a real (serially correlated) panel and
recording whether $|t| > 1.96$, what does the **fraction of replications that reject** estimate? Name the
quantity precisely, and explain in one sentence why this is the same logical move as the Week-1 coin-flip
lab (a universe where you *know* the coin is fair, counting how often the test wrongly calls it biased).

**(d)** [4 pts] State the experiment's punchline as a decision rule: if the placebo rejection rate comes
back near 0.05, what do you conclude about the conventional standard error; and if it comes back far above
0.05, what have you caught the standard error doing? Use the words "honest" and "too small" in your
answer, and connect "too small SE" $\Rightarrow$ "too large $t$" $\Rightarrow$ "over-rejection" in one
chain.

---

## Problem 2 — Reading a placebo rejection rate well above 5% (14 points)

You run the placebo Monte Carlo of Problem 1 on a simulated state-year panel with strong within-state
serial correlation ($\rho = 0.8$, $T = 20$, 50 states), using the **conventional (classical) standard
error** that assumes the $u_{st}$ are independent across years within a state. Over $R = 600$ replications
you observe an empirical rejection rate of (illustrative, from `nb5.5`):

$$
\widehat{\text{size}}_{\text{naive}} \;=\; 0.35 \quad(\text{nominal } \alpha = 0.05).
$$

**(a)** [4 pts] Interpret this number for a reader who has never seen the paper: in plain English, what
does "0.35" mean about a researcher who uses this specification and reports significance at the 5% level?
Use a concrete framing — "out of 100 pure-noise placebo laws, about how many would be declared
significant?" — and contrast it with how many *should* be.

**(b)** [3 pts] A skeptic says: "0.35 is just sampling noise in the Monte Carlo — run more replications
and it will drift back to 0.05." Refute this in two or three sentences. Compute the approximate Monte
Carlo standard error of an estimated rejection rate $\hat p$ from $R = 600$ independent replications using
$\text{SE}(\hat p) = \sqrt{\hat p(1-\hat p)/R}$, and state how many standard errors $0.35$ sits above
$0.05$. (This is the Week-1 standard error of a proportion, reused.)

**(c)** [4 pts] Translate the rejection rate into the language of *false discoveries*. If this
specification were the field default and 200 researchers each studied a genuinely-null policy (no real
effect anywhere), roughly how many would publish a "significant" finding? Explain in one sentence why this
is precisely the mechanism by which a broken standard-error formula can populate a literature with effects
that are not there — the worry that motivated BDM.

**(d)** [3 pts] State carefully what $0.35$ does **not** tell you. Does the over-rejection mean the *point
estimate* $\hat\beta$ is biased? Distinguish, in one or two sentences, between a problem of **inference**
(the standard error / t-stat) and a problem of **estimation** (the coefficient itself), and say which one
the placebo experiment indicts. (Hint: the placebo $\hat\beta$ is centered at zero on average; it is the
*spread* of $\hat\beta$ that the formula mismeasures.)

---

## Problem 3 — Why serial correlation inflates the t-stat: an AR(1) argument (20 points)

Now the mechanism. This is the analytical heart of the set: *why* positively serially correlated errors
make the conventional standard error too small. We reason with a deliberately stripped-down version of the
problem — a single treated state's after-period mean — so the algebra is by-hand.

Let a state's post-treatment error sequence be $u_1, u_2, \dots, u_T$, each with mean $0$ and variance
$\sigma^2$, following a stationary **AR(1)** process

$$
u_t \;=\; \rho\, u_{t-1} \;+\; e_t, \qquad |\rho| < 1,\quad \operatorname{Var}(e_t)=\sigma^2(1-\rho^2),
$$

so that $\operatorname{Var}(u_t) = \sigma^2$ for every $t$ and the lag-$k$ autocorrelation is
$\operatorname{Corr}(u_t, u_{t+k}) = \rho^{|k|}$. A DiD comparison leans on the **average** error over the
post period, $\bar u = \frac1T\sum_{t=1}^T u_t$, because that average is what contaminates $\hat\beta$.

**(a)** [4 pts] Write down the variance of the sample mean $\bar u$ that the **conventional** formula
*assumes* — i.e., the variance you would get if the $u_t$ were **independent**. (This is the Week-1
$\sigma^2/n$ fact; state it with $n = T$.)

**(b)** [8 pts] Now derive the **true** variance of $\bar u$ under AR(1) correlation. Start from
$\operatorname{Var}(\bar u) = \frac{1}{T^2}\sum_{t}\sum_{r}\operatorname{Cov}(u_t,u_r)$, substitute
$\operatorname{Cov}(u_t,u_r) = \sigma^2\rho^{|t-r|}$, and show that

$$
\operatorname{Var}(\bar u) \;=\; \frac{\sigma^2}{T}\left[\,1 \;+\; \frac{2}{T}\sum_{k=1}^{T-1}(T-k)\,\rho^{k}\,\right].
$$

Then evaluate the bracketed inflation factor for the concrete small case $T = 3$, $\rho = 0.8$: compute
the true $\operatorname{Var}(\bar u)$ and the ratio to the independence value from (a). (Show the three
covariance "rings": one diagonal, and the off-diagonal lag-1 and lag-2 terms.)

**(c)** [4 pts] Take the limit intuition. As $T$ grows with $\rho$ fixed and positive, the bracketed
factor approaches the constant $\dfrac{1+\rho}{1-\rho}$ (you may use this; it is the long-run-variance
ratio). Evaluate it at $\rho = 0.8$. Then complete the sentence: "Ignoring serial correlation makes the
reported variance of $\bar u$ too small by a factor of about ___, so the reported standard error is too
small by a factor of about ___, and the t-statistic is therefore too **large** by a factor of about ___."
(Standard errors are square roots of variances — keep that straight.)

**(d)** [4 pts] Tie it to **effective sample size**. The independence formula treats all $T$ observations
as $T$ *independent* pieces of information. Define the **effective number of independent observations** as
$T_{\text{eff}} = T \big/ \big[\text{inflation factor}\big]$. Using the long-run factor from (c), compute
$T_{\text{eff}}$ for $T = 20$, $\rho = 0.8$. Explain in two sentences why "20 serially correlated years
carry only about $T_{\text{eff}}$ years' worth of independent information" is the cleanest one-line
statement of *why* the conventional standard error lies — and connect it to the Reader's-Guide claim that
**longer panels make the over-rejection worse**.

---

## Problem 4 — The three fixes: what each one does and why it works (22 points)

Having diagnosed the disease, name and reason about the cures. Hold the data-generating process fixed at
the strongly-serially-correlated setting of Problem 2 ($\rho = 0.8$, $T = 20$, 50 states). Rerunning the
placebo Monte Carlo with each fix in `nb5.5` produces these illustrative rejection rates side by side:

| Standard-error method | Placebo rejection rate (illustrative, `nb5.5`) |
|:---|:---:|
| Conventional (classical), assumes independence | $\approx 0.35$ |
| Cluster by state | $\approx 0.05$ |
| Collapse to pre/post (two periods per state) | $\approx 0.055$ |
| Block bootstrap (resample whole states) | $\approx 0.05$–$0.06$ |

**(a)** [6 pts] **Cluster by state.** State precisely what the cluster-robust standard error does to the
residual covariance: write the assumed $\boldsymbol\Omega$ as **block-diagonal with one block per state**,
and say in words what is allowed *within* a block versus *across* blocks. Explain in two sentences why this
is exactly the right shape for the serial-correlation disease — i.e., why "let each state's residuals be
arbitrarily correlated across all its own years" is precisely the pattern Problem 3 showed the
conventional formula misreads. (This is the Chapter 2.4 fix, and the reason Priya clustered by state in
Week 4.)

**(b)** [6 pts] **Collapse to pre/post.** Describe the operation: average each state's data into one
"before" number and one "after" number, reducing the panel to effectively two periods per state, then run
the simple comparison. Explain in two sentences *why* this restores honest size — what happens to the
within-period serial correlation when there is only one observation per state per period? Then state the
**cost** the Reader's Guide is upfront about, naming it as a Week-1 trade-off: what does collapsing do to
**power**, and why? (Use the words "discarded information" and "Type-II error.")

**(c)** [6 pts] **Block bootstrap.** Contrast it with a *naive* bootstrap that resamples individual
state-year observations. Explain in two sentences why resampling **whole states** (each state's entire
time series kept intact) is what makes the block bootstrap valid here, and why the naive
observation-level resample would *fail* in exactly the same way the conventional formula fails. (Use the
phrase "preserves each state's serial-correlation structure.")

**(d)** [4 pts] Step back and unify. All three fixes drag the rejection rate from $\approx 0.35$ back to
$\approx 0.05$, but they do it by different routes. In one sentence each, classify each fix as either
**"model the dependence honestly"** (estimate the right standard error while keeping all the data) or
**"remove the dependence by destroying the structure that carries it"** — and assign clustering, the
block bootstrap, and the collapse to the right category. Then state which single fix you would default to
when you have many states and want to keep power, and why.

---

## Problem 5 — The few-clusters caution (Week 4 bridge) (16 points)

The cures of Problem 4 are not universal. They lean on having **many** clusters, and a great many real
DiD designs do not. This problem makes the caveat precise.

**(a)** [4 pts] As a stretch in `nb5.5` you shrink the number of states from 50 down to a handful (say 6)
while keeping $\rho = 0.8$, and rerun the placebo Monte Carlo *with clustering by state*. The clustered
rejection rate, which was an honest $\approx 0.05$ with 50 states, climbs back **well above** $0.05$.
Explain the mechanism: the cluster-robust formula estimates the within-cluster correlation from variation
*across* clusters, so with few clusters there is *not enough of it*. Why does "too few clusters to
estimate the between-cluster variation" make the clustered standard error itself **too small again**, and
the test over-reject? State the rule-of-thumb cluster count (the "30-to-50" zone) from Chapter 2.4 / Week
4.

**(b)** [4 pts] Connect to the designs that need the cure most. The Reader's Guide notes that an enormous
share of influential DiD studies have **few treated units** — recall Priya's *single* treated state and
the essentially-one-treated-unit Card–Krueger design. Explain the uncomfortable implication in two
sentences: does BDM's recommended cure (cluster / block bootstrap) actually reach those designs, or does
it quietly assume the easy case of many states?

**(c)** [4 pts] Name the further corrections. The Reader's Guide points to the **wild cluster bootstrap of
Cameron, Gelbach & Miller (2008)** and few-cluster $t$ adjustments as the tools for the small-number-of-
clusters regime. In one sentence, state what these are *for* (not how they work in detail): what do they
fix that plain clustering cannot when clusters are few?

**(d)** [4 pts] State the spec-discipline takeaway (Conventions §4) as a one-line rule a referee would
apply to *any* DiD table: clustering must be done **at the level the treatment varies**, *and* the
honesty of the resulting standard error depends on a quantity that is not the sample size $N$ — name that
quantity, and explain in one sentence why a table reporting "$N = 1{,}000{,}000$ borrower-months,
clustered by state, 6 states" can still have untrustworthy t-stats.

---

## Problem 6 — Replication design: specify the placebo Monte Carlo for `nb5.5` (12 points)

The payoff: write the *recipe* for the simulation you will run, in enough detail that a classmate could
implement it. This is the BDM placebo-law experiment, rebuilt on a clean simulated panel rather than the
proprietary CPS extract — the *spirit* of the paper, identical mechanism.

**(a)** [4 pts] **Specify the data-generating process.** In the Conventions §4 format, name the pieces of
the *null* panel you will build: the dimensions (number of states, number of years $T$), the structure of
the outcome $Y_{st} = \mu_s + \lambda_t + u_{st}$ (state effects, year effects, AR(1) within-state errors
with persistence $\rho$), and — the load-bearing point — **what the true treatment effect is and why**.
State in one sentence why the panel must contain **no treatment term at all** for the experiment to
measure size.

**(b)** [4 pts] **Specify the placebo-assignment and estimation loop.** Describe one replication
end-to-end: how a random placebo law is assigned (which states, what onset timing), the regression that is
then run (write the spec: outcome · treatment · fixed effects · standard-error flavor · sample), the
statistic recorded, and the rejection rule. Then say what is averaged over the $R$ replications to produce
the headline number, and why each replication must draw a **fresh** placebo assignment.

**(c)** [4 pts] **Specify the two sweeps that prove the mechanism.** The headline number alone could be
dismissed as "maybe just noise." Describe the **two dial-turning experiments** that pin the blame on
serial correlation rather than chance: (i) sweep the AR(1) persistence $\rho$ from $0$ (independent
errors) toward $1$ and plot the naive rejection rate against $\rho$; (ii) the fixes comparison from
Problem 4 overlaid. State precisely what the $\rho = 0$ endpoint should show if your simulation is correct
(the value it must return), and what the rising curve demonstrates — i.e., why these two plots together
constitute *evidence the culprit is autocorrelation*, exactly the Reader's-Guide reading order of symptom
→ mechanism → cure.

---

*End of Problem Set 5.5. Solutions: Appendix E, `E-w5-ps5.5-solutions.md`. The companion notebook `nb5.5`
(`notebooks/week-05/nb5.5-bdm-placebo-law.ipynb`) lets you generate the rejection rates in Problems 1, 4,
and 5 yourself: build the serially correlated null panel, run the placebo experiment across standard-error
flavors, read the false-positive rate off your own output, sweep $\rho$ to expose the mechanism, then
shrink the cluster count until clustering itself breaks — rediscovering the few-clusters caveat with your
own simulation. The single discipline to carry forward: on a persistent panel, a small standard error is
not the same as an honest one, and the only way to know which you have is to ask whether the formula
respects the dependence the data actually contain — the lesson of Bertrand, Duflo & Mullainathan (2004).*
