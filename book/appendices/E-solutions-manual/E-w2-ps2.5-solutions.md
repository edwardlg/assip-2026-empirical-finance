# Solutions — Problem Set 2.5 (OVB Sign Predictions and the Measurement-Error Simulation)

Full worked solutions to `book/weeks/week-02/ps2.5.md`, covering Chapter 2.5. Notation follows the
Conventions: the true (long) model is $y = \beta_0 + \beta_1 x + \beta_2 z + \varepsilon$ with
$\mathbb{E}[\varepsilon \mid x,z] = 0$; the short model is $y = \tilde\beta_0 + \tilde\beta_1 x + u$; the
auxiliary slope is $\delta_1 = \operatorname{Cov}(x,z)/\operatorname{Var}(x)$; for measurement error
$x = x^\* + m$ and $\lambda = \sigma_{x^\*}^2/(\sigma_{x^\*}^2 + \sigma_m^2)$. The recurring theme of the
key: **bias lives in the probability limit and moves the center of the sampling distribution; precision
lives in the standard error and controls only the spread. No amount of data, and no standard-error
flavor, fixes a biased center — only a research design does.**

---

## Problem 1 — Derive the OVB formula, then read the bias term (14 pts)

**(a)** [6 pts] By definition the short-regression slope is
$$\hat{\tilde\beta}_1 = \frac{\widehat{\operatorname{Cov}}(x,y)}{\widehat{\operatorname{Var}}(x)}.$$
Substitute the true model $y = \beta_0 + \beta_1 x + \beta_2 z + \varepsilon$ into the covariance.
Covariance is linear in each argument and ignores additive constants ($\operatorname{Cov}(x,\beta_0)=0$),
so
$$\operatorname{Cov}(x,y) = \operatorname{Cov}(x,\ \beta_0 + \beta_1 x + \beta_2 z + \varepsilon)
= \beta_1 \operatorname{Var}(x) + \beta_2 \operatorname{Cov}(x,z) + \operatorname{Cov}(x,\varepsilon).$$
The last term is zero because the long model is well-specified: $\mathbb{E}[\varepsilon\mid x,z]=0$
implies $\operatorname{Cov}(x,\varepsilon)=0$. Divide through by $\operatorname{Var}(x)$:
$$\frac{\operatorname{Cov}(x,y)}{\operatorname{Var}(x)}
= \beta_1 + \beta_2 \cdot \frac{\operatorname{Cov}(x,z)}{\operatorname{Var}(x)} = \beta_1 + \beta_2\,\delta_1,$$
recognizing the fraction as the slope $\delta_1$ from the auxiliary regression of the omitted $z$ on the
included $x$. The **Law of Large Numbers** (Chapter 1.4) guarantees the sample covariance and variance
converge in probability to their population counterparts, so the *sample* slope inherits the limit:
$$\hat{\tilde\beta}_1 \xrightarrow{p} \beta_1 + \beta_2\,\delta_1.$$

**(b)** [4 pts] The bias is the *product* $\beta_2\,\delta_1$; a product is zero whenever *either* factor
is zero. So OVB requires the omitted variable to **both** genuinely affect the outcome ($\beta_2 \neq 0$)
**and** be correlated with the included regressor ($\delta_1 \neq 0$). Example of harmless omission: a
variable that drives $y$ but is *uncorrelated* with $x$ — say, omitting a firm's headquarters time zone
from a return regression on momentum, when the time zone affects returns through some channel but is
unrelated to the momentum signal. Here $\delta_1 = 0$, so the bias term vanishes and $\hat{\tilde\beta}_1$
stays consistent. The cost is *not* bias but **precision**: the omitted relevant variable sits in the
error, inflating $\operatorname{Var}(u)$ and therefore the standard error of $\hat{\tilde\beta}_1$.

**(c)** [4 pts] The short-model error is $u = \beta_2 z + \varepsilon$. Then
$$\operatorname{Cov}(x,u) = \beta_2 \operatorname{Cov}(x,z) + \operatorname{Cov}(x,\varepsilon)
= \beta_2 \operatorname{Cov}(x,z),$$
which is nonzero whenever $\beta_2 \neq 0$ and $\operatorname{Cov}(x,z)\neq 0$ — i.e. whenever
$\delta_1 \neq 0$ (and $z$ matters). A nonzero $\operatorname{Cov}(x,u)$ means $\mathbb{E}[u\mid x]\neq 0$:
$x$ carries information about the error. This is exactly the failure of the Chapter 2.2
zero-conditional-mean assumption — **OVB is endogeneity** caused by banishing a relevant, correlated
variable into the error term, and it is the canonical example of why $\mathbb{E}[\varepsilon\mid x]=0$
breaks.

---

## Problem 2 — The two-sign rule in three finance scenarios (20 pts)

The rule: sign of bias $= \operatorname{sign}(\beta_2)\times\operatorname{sign}(\delta_1)$. "Same signs
push up, opposite signs push down." A *downward* bias makes the coefficient too negative; an *upward*
bias makes it too positive — relative to the included regressor's own true effect.

**(a)** [7 pts] **Maya.**
(i) Omitted variable: creditworthiness $C$.
(ii) $\beta_2 > 0$ — more creditworthy applicants are approved more often.
(iii) $\delta_1 < 0$ — regressing $C$ on $D$ gives a negative slope because the $D=1$ group has lower
average measured creditworthiness in this sample.
(iv) Bias $= (+)(-) = -$: biased **downward**, too negative. As an estimate of $D$'s *own* effect on
approval, the short coefficient is **too negative** — it *overstates* the approval penalty against the
$D=1$ group, because part of the lower approval is really the lender responding to lower measured $C$,
which the regression mistakenly loads onto $D$.
(v) Honest conclusion: *"The raw $D$ coefficient is an upper bound (in magnitude) on the disadvantage
attributable to $D$ itself; it is contaminated by omitted creditworthiness, and I cannot separate
discrimination from creditworthiness without controlling for $C$ — or, better, a design (Week 4) that
compares applicants identical on $C$."* Note we have **not** shown there is no discrimination; we have
shown the number is biased.

**(b)** [7 pts] **Sam.**
(i) Omitted variable: firm size, entered as "smallness."
(ii) $\beta_2 > 0$ — smaller firms earn higher returns (smallness raises return), by stipulation.
(iii) $\delta_1 > 0$ — momentum scores are higher for smaller firms, so regressing smallness on
momentum gives a positive slope.
(iv) Bias $= (+)(+) = +$: biased **upward**, too positive. Sam's momentum coefficient *overstates*
momentum's own profitability — a structural cause of the kind of mirage the multiple-testing discussion
warned about.
(v) Honest conclusion: *"The momentum coefficient is biased upward by omitted size; some of the apparent
momentum premium is the small-firm premium traveling with the momentum signal. I should control for
size (a bet) or use a design that isolates momentum variation orthogonal to size."*
Caveat: the empirical sign of the size–momentum relationship must be verified in the *actual* sample
before asserting it in print — the mechanics of the two-sign rule hold regardless of which sign is true,
but the *direction of the conclusion* depends on the real $\delta_1$.

**(c)** [6 pts] **Priya.**
Omitted variable: physical climate exposure. $\beta_2 > 0$ (higher exposure raises premiums).
$\delta_1 > 0$ (high-ESG firms tend to have higher physical exposure in her sample). Bias
$= (+)(+) = +$: the ESG coefficient is biased **upward**. If the true ESG effect on premiums is negative
or zero, the upward bias pulls the estimate toward positive, which **undercuts** a naive "ESG lowers
premiums" claim — the omitted exposure is masking (or even reversing) the apparent ESG effect. Priya
cannot claim ESG reduces premiums until physical exposure is held fixed (control, or a design that does
so).

---

## Problem 3 — OVB does not shrink with N (the precisely-wrong number) (16 pts)

**(a)** [4 pts] By the OVB formula,
$$\hat{\tilde\beta}_1 \xrightarrow{p} \beta_1 + \beta_2\,\delta_1 = 0 + (0.30)(-0.50) = -0.15.$$
Maya reads a $-0.15$ coefficient on $D$ — apparently a $15$-percentage-point approval penalty against the
$D=1$ group — **in a world with literally zero discrimination** ($\beta_1 = 0$). The entire "effect" is
borrowed from creditworthiness through the correlation between $C$ and $D$.

**(b)** [5 pts]
(i) The point estimate $\hat{\tilde\beta}_1$ stays centered on $-0.15$ at *both* sample sizes. Bias is a
property of the probability limit; it does not depend on $N$. At $N = 5{,}000{,}000$ the estimate is, if
anything, *more reliably* $-0.15$ — the wrong number, measured precisely.
(ii) The standard error shrinks like $1/\sqrt{N}$. Multiplying $N$ by $1000$ divides the standard error
by $\sqrt{1000} \approx 31.6$. So the wobble around $-0.15$ collapses by a factor of about $31.6$.
Punchline: the larger sample buys her a tighter confidence interval **around the wrong center** — more
precision, zero reduction in bias.

**(c)** [4 pts] As $N$ grows, the standard error shrinks while the (biased) estimate stays at $-0.15$, so
$t = \hat{\tilde\beta}_1/\widehat{\operatorname{se}}$ explodes into the hundreds. This is exactly Maya's
"$t = 4.1$" from the chapter opening, only louder: a giant t-statistic certifies that the estimate is far
from zero *and measured sharply*, but says nothing about whether the estimate is the *right* quantity. A
precise estimate of a biased number is still a wrong answer. This problem lives entirely in the **Bias**
column of the §2.5.11 ledger — the column no standard-error machinery can touch.

**(d)** [3 pts] If $\delta_1 = 0$ (the omitted variable is relevant but uncorrelated with $D$), then the
bias term $\beta_2\delta_1 = 0$ and $\hat{\tilde\beta}_1$ is **consistent** — it converges to the true
$\beta_1$. The cost of omitting it is only that it sits in the error and inflates $\operatorname{Var}(u)$,
widening the standard error. There, more data **does** help: the standard error shrinks like $1/\sqrt{N}$
and the estimate homes in on the truth. That scenario belongs to the **SE** column of the ledger, not the
bias column.

---

## Problem 4 — Classical measurement error: derive $\lambda$, predict the attenuated slope (18 pts)

**(a)** [8 pts] Substitute $x^\* = x - m$ into the true model:
$$y = \beta_0 + \beta_1(x - m) + \varepsilon = \beta_0 + \beta_1 x + (\varepsilon - \beta_1 m).$$
We OLS-regress $y$ on the observed $x$, so the probability limit of the slope is
$\operatorname{Cov}(x,y)/\operatorname{Var}(x)$.

*Numerator.* Using $x = x^\* + m$ and $y = \beta_0 + \beta_1 x^\* + \varepsilon$,
$$\operatorname{Cov}(x,y) = \operatorname{Cov}(x^\* + m,\ \beta_0 + \beta_1 x^\* + \varepsilon)
= \beta_1 \operatorname{Var}(x^\*) + \beta_1\operatorname{Cov}(m,x^\*) + \operatorname{Cov}(x^\*,\varepsilon)
+ \operatorname{Cov}(m,\varepsilon).$$
Under CEV the last three covariances are zero: $\operatorname{Cov}(m,x^\*)=0$ (error uncorrelated with
the truth), $\operatorname{Cov}(x^\*,\varepsilon)=0$ (long model well-specified), and
$\operatorname{Cov}(m,\varepsilon)=0$ (error uncorrelated with the equation error). So
$\operatorname{Cov}(x,y) = \beta_1\sigma_{x^\*}^2$.

*Denominator.* Because $x^\*$ and $m$ are uncorrelated, the variance splits:
$$\operatorname{Var}(x) = \operatorname{Var}(x^\* + m) = \sigma_{x^\*}^2 + \sigma_m^2.$$

*Ratio.*
$$\hat\beta_1 \xrightarrow{p} \frac{\beta_1 \sigma_{x^\*}^2}{\sigma_{x^\*}^2 + \sigma_m^2}
= \beta_1 \cdot \lambda, \qquad \lambda = \frac{\sigma_{x^\*}^2}{\sigma_{x^\*}^2 + \sigma_m^2}.$$
Since variances are non-negative, the denominator is at least the numerator, so $0 < \lambda \le 1$
(strictly less than 1 whenever $\sigma_m^2 > 0$). Multiplying by $\lambda \in (0,1)$ shrinks the magnitude
toward zero regardless of the sign of $\beta_1$ — this is **attenuation bias**, and its direction (toward
zero) is always known under CEV.

**(b)** [4 pts] With $\beta_1 = 1.0$ and $\lambda = 0.6$: $\hat\beta_1 \xrightarrow{p} 1.0 \times 0.6 =
0.6$. Now set $\sigma_m^2 = \tfrac{1}{4}\sigma_{x^\*}^2$. Then
$$\lambda = \frac{\sigma_{x^\*}^2}{\sigma_{x^\*}^2 + \tfrac14\sigma_{x^\*}^2}
= \frac{1}{1 + 0.25} = \frac{1}{1.25} = 0.8,$$
so the new probability limit is $1.0 \times 0.8 = 0.8$ — halving the noise variance moved the estimate
from $0.6$ up toward the truth $1.0$, but it is still attenuated.

**(c)** [3 pts] Attenuation is a bias in the **probability limit** — the *center* of the sampling
distribution sits at $\beta_1\lambda$, not at $\beta_1$. Sampling noise is the *spread* around that
center, and it averages out: more data shrinks the spread like $1/\sqrt{N}$. But more data only makes
$\hat\beta_1$ converge more tightly onto the *biased* center $\beta_1\lambda$. Attenuation is the bias,
not the noise; $N$ does not touch it.

**(d)** [3 pts] Threat: *classical measurement error in the activity regressor, biasing its coefficient
toward zero by the reliability factor $\lambda$.* Fixes: (1) **measurement** — get a less-noisy measure
of true activity (a more reliable scraper, validated on-chain ground truth); (2) **design** — instrument
for $x^\*$ (Week 4 IV). A valid instrument would have to be correlated with true activity $x^\*$ but
uncorrelated with both the equation error $\varepsilon$ and the measurement error $m$ — for example, a
*second, independent* measurement of activity, which under CEV provides exactly the leverage to undo
$\lambda$.

---

## Problem 5 — Mismeasured $y$ versus mismeasured $x$: bias versus standard error (16 pts)

**(a)** [6 pts] With clean regressor $x = x^\*$ and observed outcome $y = y^\* + v$, substitute the true
relation $y^\* = \beta_0 + \beta_1 x^\* + \varepsilon$:
$$y = y^\* + v = \beta_0 + \beta_1 x^\* + \varepsilon + v = \beta_0 + \beta_1 x + (\varepsilon + v).$$
The composite error is $\varepsilon + v$. Under the classical assumption $v$ is uncorrelated with $x$,
and $\varepsilon$ already is, so $\operatorname{Cov}(x,\ \varepsilon + v) = 0$ and
$\mathbb{E}[\varepsilon + v\mid x] = 0$: the zero-conditional-mean assumption **survives**. Hence
$\hat\beta_1$ remains **consistent** — it still converges to $\beta_1$. The only cost is a larger error
variance, $\operatorname{Var}(\varepsilon + v) = \sigma_\varepsilon^2 + \sigma_v^2$, which inflates the
**standard error** of $\hat\beta_1$ (wider confidence intervals), a *precision* loss, not bias.

**(b)** [4 pts]

| Mismeasured quantity (classical) | Biases $\hat\beta_1$? | Direction | Bias or SE problem? |
|---|---|---|---|
| regressor $x$ | Yes | toward zero (attenuation, factor $\lambda$) | **Bias** |
| outcome $y$ | No | — | **SE** (wider intervals) |

Rule: **classical noise in $x$ biases the slope toward zero; classical noise in $y$ does not bias it at
all — it only widens the standard error.** The asymmetry comes from *where the noise lands*: noise in $x$
enters both the regressor and the error and correlates them; noise in $y$ enters only the error and stays
uncorrelated with $x$.

**(c)** [3 pts] A noisily-measured *control* is worse than a noisy $y$ because the control's job is to
*absorb confounding* from the key regressor. A noisy proxy only *partially* removes that confounding —
the regression controls for the noisy proxy, not the true confounder — so residual confounding leaks back
onto the coefficient of the key regressor, **biasing** it (re-opening OVB in the OVB direction). The name
from Section 2.5.7: *a noisily-measured control is a **partially-omitted control**.* This is why "I
controlled for it" and "I controlled for it *well*" are different claims.

**(d)** [3 pts] The "classical" assumption requires $v$ uncorrelated with $x$. A **non-classical** case
in Devon's setting: suppose return is mismeasured because high-activity wallets (high $x$) are reported on
exchanges that systematically over-state realized returns — then the outcome error $v$ is *correlated*
with $x$, $\operatorname{Cov}(x,v)\neq 0$, the zero-conditional-mean assumption fails, and $\hat\beta_1$
is **biased** (in an unknown direction). The protection in part (a) was the classical assumption, not the
mere fact that the error was in $y$.

---

## Problem 6 — Functional form, RESET, and a Monte Carlo design (16 pts)

**(a)** [5 pts]
(i) If the truth is $y = \beta_0 + \beta_1 x + \beta_2 x^2 + \varepsilon$ but Priya fits
$y = \tilde\beta_0 + \tilde\beta_1 x + u$, then the fitted error must absorb the dropped term:
$u = \beta_2 x^2 + \varepsilon$. Since $x^2$ is a deterministic function of $x$, it is correlated with
$x$ (for non-symmetric or non-zero-mean $x$, $\operatorname{Cov}(x,x^2)\neq 0$), so
$\operatorname{Cov}(x,u)\neq 0$ and $\mathbb{E}[u\mid x]\neq 0$. This is "the same disease as OVB": a
relevant, correlated variable — here $x^2$, a transformation of a variable she already has — has been
banished into the error term, breaking $\mathbb{E}[\varepsilon\mid x]=0$.
(ii) Because the truth is convex ($\beta_2 > 0$), the best straight line **understates** the premium's
sensitivity at high emissions (where the curve is steep) and **overstates** it at low emissions (where
the curve is flat). The single slope $\hat{\tilde\beta}_1$ is a misleading average that matches the true
marginal effect $\partial y/\partial x = \beta_1 + 2\beta_2 x$ at *neither* low nor high $x$.

**(b)** [4 pts]
(i) $p = 0.001$ on the linear fit: **reject** the null of correct functional form — there is curvature
the straight line is not capturing; "the shape is wrong." $p = 0.42$ on the quadratic fit: **fail to
reject** — the $x^2$ term has soaked up the detectable curvature, so "the shape now looks right." RESET
flagged the problem and confirmed the fix.
(ii) A clean RESET does **not** rule out **omitted variable bias** (or measurement error). For example,
a confounder like firm industry or physical climate exposure could still bias the emissions coefficient.
RESET is structurally blind to it because RESET only checks for *neglected curvature among the variables
already in the model* — it builds its test regressors from powers of the fitted values $\hat y$, which
are functions of the included regressors only. It can say nothing about a variable that is not in the
data at all. "Passing RESET means the shape looks right, not that the coefficient is causal."

**(c)** [7 pts] A correct design earns full marks if it specifies all five required pieces unambiguously.
Two model answers follow; either suffices.

**Model answer — OVB simulation.**
- *DGP.* Choose true parameters $\beta_0 = 1$, $\beta_1 = 0$ (the demographic effect, set to zero so any
  nonzero short coefficient is *pure bias*), $\beta_2 = 0.30$. Draw $x \sim \mathcal{N}(0,1)$ (the
  included regressor, e.g. group indicator standardized). Generate the omitted $z$ *correlated with $x$*
  via $z = \delta_1 x + \nu$ with $\delta_1 = -0.50$ and $\nu \sim \mathcal{N}(0,1)$ independent — this
  $\delta_1$ is the auxiliary slope by construction. Draw $\varepsilon \sim \mathcal{N}(0,1)$ independent
  of $x,z$. Form $y = \beta_0 + \beta_1 x + \beta_2 z + \varepsilon$. Use $N = 50{,}000$.
- *Two regressions.* **Long:** $y$ on $x$ and $z$ (should recover $\hat\beta_1 \approx 0$). **Short:**
  $y$ on $x$ alone (should recover $\hat{\tilde\beta}_1 \approx \beta_1 + \beta_2\delta_1$).
- *Theoretical prediction.* $\hat{\tilde\beta}_1 \xrightarrow{p} \beta_1 + \beta_2\delta_1 = 0 +
  (0.30)(-0.50) = -0.15$; the long-model coefficient $\to 0$.
- *Sweep.* Flip the sign of $\delta_1$ to $+0.50$. By the two-sign rule the bias flips sign: predict the
  short coefficient moves from $-0.15$ to $+0.15$ *before* running. Optionally sweep $\delta_1$ over a
  grid and plot $\hat{\tilde\beta}_1$ against $\beta_2\delta_1$ — points should lie on the 45° line.
- *Single run vs. many replications.* A single fixed-$N$ run gives one $\hat{\tilde\beta}_1$ near $-0.15$
  with sampling wobble; averaging over many (say 1000) Monte Carlo replications shows the *mean* of
  $\hat{\tilde\beta}_1$ sits at $-0.15$ — i.e. the bias is in the **center** of the sampling distribution,
  not its spread. (More replications sharpen the estimate of the center; they do not move it.)

**Model answer — attenuation simulation.**
- *DGP.* True $\beta_1 = 2$, $\beta_0 = 1$. Draw $x^\* \sim \mathcal{N}(0,1)$ so $\sigma_{x^\*}^2 = 1$,
  $\varepsilon \sim \mathcal{N}(0,1)$, $y = \beta_0 + \beta_1 x^\* + \varepsilon$. Corrupt the regressor:
  $x = x^\* + m$, $m \sim \mathcal{N}(0,\sigma_m^2)$ independent of $x^\*$ and $\varepsilon$.
  $N = 50{,}000$.
- *Two regressions.* **Clean:** $y$ on $x^\*$ (recovers $\hat\beta_1 \approx 2$). **Mismeasured:** $y$ on
  $x$ (recovers $\hat\beta_1 \approx 2\lambda$).
- *Theoretical prediction.* $\hat\beta_1 \xrightarrow{p} \beta_1\lambda$ with
  $\lambda = 1/(1 + \sigma_m^2)$ (since $\sigma_{x^\*}^2 = 1$).
- *Sweep.* Run $\sigma_m \in \{0, 0.5, 1.0, 2.0\}$. Predict, before running, that $\hat\beta_1$ slides
  $2.00 \to 1.60 \to 1.00 \to 0.40$ (i.e. $\beta_1\lambda$ for $\lambda = 1, 0.8, 0.5, 0.2$). Plot
  $\hat\beta_1$ against $\lambda$ — a straight line through the origin with slope $\beta_1$.
- *Single run vs. many replications.* One run at fixed $N$ gives a noisy $\hat\beta_1$ near $\beta_1\lambda$;
  averaging over many replications shows the mean estimate equals $\beta_1\lambda$ — confirming attenuation
  is a shift of the distribution's center, while $N$ (or replication count) only tightens the spread.

A full-credit answer states the *expected pattern before running* (the prediction is the point of the
exercise) and articulates the center-versus-spread distinction in the last bullet.

---

*End of solutions for Problem Set 2.5. Every "Bias"-column threat rehearsed here — OVB, attenuation,
mismeasured controls, functional form — is answered not by a better standard error but by a research
**design**: potential outcomes and randomization (Week 3), then instrumental variables,
difference-in-differences, and regression discontinuity (Week 4). Maya's fair-lending question returns in
Week 4 with the tools to hold creditworthiness genuinely fixed.*
