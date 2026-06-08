# Problem Set 2.5 — OVB Sign Predictions and the Measurement-Error Simulation

**Covers Chapter 2.5 (Misspecification: OVB, Measurement Error, Functional Form).** Methods through
Ch 2.5 only: the omitted variable bias formula and the two-sign rule, the difference between bias and
sampling noise (a biased coefficient does not improve with $N$), classical errors-in-variables and
the attenuation factor, the mismeasured-$y$ versus mismeasured-$x$ asymmetry, functional-form
misspecification and the RESET diagnostic, and the bias–consistency ledger. Notation follows the
Conventions. The true (long) model is written
$$y = \beta_0 + \beta_1 x + \beta_2 z + \varepsilon, \qquad \mathbb{E}[\varepsilon \mid x, z] = 0,$$
the short (misspecified) model is $y = \tilde\beta_0 + \tilde\beta_1 x + u$, and the auxiliary slope of
the omitted $z$ on the included $x$ is $\delta_1 = \operatorname{Cov}(x,z)/\operatorname{Var}(x)$. For
the measurement-error problems the true regressor is $x^\*$, the observed one is $x = x^\* + m$, and
$\lambda = \sigma_{x^\*}^2/(\sigma_{x^\*}^2 + \sigma_m^2)$ is the reliability ratio.

Six problems, escalating, **100 points total**. Each is self-contained. Where a numerical answer is
asked for, the inputs are supplied so you can work by hand. **The grading rule of this set:** a
direction or a fix stated without naming *why* — which assumption broke, which term entered the error,
which design restores exogeneity — earns half credit at most. In this chapter the *reasoning* is the
skill, exactly as the interpretation was the skill in Chapter 1.5. Throughout, when you name a threat,
also name the design that would address it (spec discipline, Conventions §4).

---

## Problem 1 — Derive the OVB formula, then read the bias term (14 points)

The whole chapter rests on one line of algebra. You will rebuild it from the definition so it is yours,
not memorized.

**(a)** [6 pts] Start from the simple-regression slope of the short model,
$\hat{\tilde\beta}_1 = \widehat{\operatorname{Cov}}(x,y)/\widehat{\operatorname{Var}}(x)$. Substitute the
*true* long model $y = \beta_0 + \beta_1 x + \beta_2 z + \varepsilon$ into the covariance, use linearity
of covariance, and use $\operatorname{Cov}(x,\varepsilon)=0$ (the long model is well-specified). Show
each step and arrive at
$$\hat{\tilde\beta}_1 \xrightarrow{p} \beta_1 + \beta_2\,\delta_1, \qquad
\delta_1 = \frac{\operatorname{Cov}(x,z)}{\operatorname{Var}(x)}.$$
State clearly *which* limit theorem lets you replace sample covariances with population ones.

**(b)** [4 pts] The bias term is the product $\beta_2\,\delta_1$. Explain, in two sentences, why *both*
factors must be nonzero for OVB to exist, and give a one-line example of an omitted variable that is
relevant to $y$ but causes **no** bias on $\hat{\tilde\beta}_1$ — and say what such a variable *does*
cost you instead.

**(c)** [4 pts] The short-model error is $u = \beta_2 z + \varepsilon$. Show that
$\mathbb{E}[u \mid x] \neq 0$ whenever $\delta_1 \neq 0$, and state in one sentence the connection to the
Chapter 2.2 zero-conditional-mean assumption: OVB is not a separate disease from endogeneity but its
canonical case.

---

## Problem 2 — The two-sign rule in three finance scenarios (20 points)

For each scenario, (i) name the omitted variable, (ii) give the sign of $\beta_2$ (its effect on the
outcome) with a one-clause reason, (iii) give the sign of $\delta_1$ (its slope on the included
regressor) with a one-clause reason, (iv) multiply to get the sign of the bias and state whether the
short coefficient is too large or too small *as an estimate of the included regressor's own effect*, and
(v) write the honest one-sentence conclusion a careful analyst would put in the paper.

**(a)** [7 pts] **Maya's fair-lending regression.** Maya regresses an approval indicator (1 = approved)
on a demographic indicator $D$ (coded $D=1$ for the historically disadvantaged group), with controls for
loan amount and age only. The decisive omitted variable is **creditworthiness** $C$ (a composite of
credit score, debt-to-income, payment history). In her sample the $D=1$ group has, for reasons of
unequal access to credit and wealth, *lower* average measured creditworthiness.

**(b)** [7 pts] **Sam's momentum regression.** Sam regresses a stock's next-month return on a momentum
signal and omits firm **size**. Take as given for this part that, in Sam's sample, smaller firms earn
higher average returns and momentum scores are *higher* for smaller firms (so the omitted size variable,
measured as "smallness," is positively related to both return and momentum). Work the rule with these
stated signs. Then add a one-sentence caveat about why the empirical sign of the size–momentum
relationship should be checked in the actual sample before this is asserted in print.

**(c)** [6 pts] **Priya's ESG-premium regression.** Priya regresses a firm's insurance premium on an ESG
score and omits the firm's **physical climate exposure** (coastal/wildfire risk). Higher exposure raises
premiums; and in her sample, firms with high ESG scores also tend to have *higher* physical exposure
(green-branding firms cluster in exposed industries like energy and real estate). Predict the direction
of bias on the ESG coefficient and state what it does to a naive "ESG lowers premiums" claim.

---

## Problem 3 — OVB does not shrink with N (the precisely-wrong number) (16 points)

Maya, told her $D$ coefficient may be biased, replies: "Then I will just collect ten times the data and
the problem will wash out." This problem shows why she is wrong, and pins down exactly what *does* and
does *not* improve with sample size.

Use the chapter's worked numbers: the true demographic effect is $\beta_1 = 0$ (no discrimination at
all), creditworthiness has effect $\beta_2 = 0.30$ on approval probability, and the auxiliary slope is
$\delta_1 = -0.50$ (group $D=1$ averages half a standard deviation lower in $C$).

**(a)** [4 pts] Compute the probability limit of Maya's short-regression coefficient
$\hat{\tilde\beta}_1$. State the number she will read off and what it appears to say.

**(b)** [5 pts] Maya runs the short regression at $N = 5{,}000$ and again at $N = 5{,}000{,}000$.
Describe what happens to (i) the *point estimate* $\hat{\tilde\beta}_1$ and (ii) its *standard error* as
$N$ grows by a factor of 1000. Be quantitative about the standard error: by roughly what factor does it
shrink? Then state the punchline in one sentence — what the larger sample buys her and what it does not.

**(c)** [4 pts] At $N = 5{,}000{,}000$ Maya's t-statistic on $D$ is enormous (in the hundreds). Connect
this to the Chapter 2.5 opening line about Maya's "$t = 4.1$." Explain, in two sentences, why a giant
t-statistic is *evidence of precision, not of correctness*, and which column of the bias–consistency
ledger this problem lives in.

**(d)** [3 pts] Contrast: suppose instead the omitted variable had been relevant to approval but
*uncorrelated* with $D$ ($\delta_1 = 0$). Would more data help in that case? Say precisely what the extra
data would and would not fix, and which ledger column that scenario belongs to.

---

## Problem 4 — Classical measurement error: derive $\lambda$, predict the attenuated slope (18 points)

Devon scrapes "on-chain wallet activity" with an imperfect scraper and uses it as a regressor for
next-week token return. The true model is $y = \beta_0 + \beta_1 x^\* + \varepsilon$ with
$\mathbb{E}[\varepsilon \mid x^\*] = 0$; Devon observes $x = x^\* + m$. Assume the classical
errors-in-variables (CEV) conditions: $m$ has mean zero and is uncorrelated with both $x^\*$ and
$\varepsilon$.

**(a)** [8 pts] Derive the probability limit of the OLS slope of $y$ on the observed $x$. Compute
$\operatorname{Cov}(x,y)$ and $\operatorname{Var}(x)$ separately under CEV, showing which cross terms die
and *why*, and conclude
$$\hat\beta_1 \xrightarrow{p} \beta_1 \cdot \lambda, \qquad
\lambda = \frac{\sigma_{x^\*}^2}{\sigma_{x^\*}^2 + \sigma_m^2}.$$
State why $0 < \lambda \le 1$ and therefore in which direction the estimate is biased, *for any sign of*
$\beta_1$.

**(b)** [4 pts] Suppose the true effect is $\beta_1 = 1.0$ and the reliability ratio is $\lambda = 0.6$
(40% of the variance in Devon's measure is scraper noise). What value does Devon's OLS coefficient
converge to? If Devon instead halved the noise variance so that $\sigma_m^2$ fell to one-quarter of
$\sigma_{x^\*}^2$, recompute $\lambda$ and the new probability limit.

**(c)** [3 pts] Explain why no amount of additional data moves the answer in (b): contrast "bias in the
probability limit" with "sampling noise that averages out." Which one is attenuation?

**(d)** [3 pts] Name the threat in spec-discipline language ("classical measurement error in the activity
regressor, biasing its coefficient toward zero") and name the *two* fixes — one measurement-based, one
design-based — pointing to the Week 4 tool. For the design fix, state in one clause what a valid
instrument for $x^\*$ would have to be.

---

## Problem 5 — Mismeasured $y$ versus mismeasured $x$: bias versus standard error (16 points)

This problem isolates the chapter's crucial asymmetry. Use the same true model as Problem 4,
$y = \beta_0 + \beta_1 x^\* + \varepsilon$.

**(a)** [6 pts] Now suppose the *regressor is clean* ($x = x^\*$) but the **outcome** is measured with
classical noise: Devon observes $y = y^\* + v$, with $v$ mean-zero and uncorrelated with $x^\*$. Write the
estimated equation in terms of the observed $y$ and show that the composite error becomes
$\varepsilon + v$. Argue that the zero-conditional-mean assumption *survives*, so $\hat\beta_1$ stays
**consistent**. What is the only cost, and to which quantity?

**(b)** [4 pts] Fill in this contrast table in your answer and add a one-sentence rule that captures it:

| Mismeasured quantity (classical) | Biases $\hat\beta_1$? | Direction | Bias or SE problem? |
|---|---|---|---|
| regressor $x$ | ? | ? | ? |
| outcome $y$ | ? | ? | ? |

**(c)** [3 pts] Devon's *control* variable — not the key regressor, but a confounder he is trying to
absorb — is noisily measured. Explain why this is worse than the $y$ case: what does a noisily-measured
control do to the coefficient on the key regressor, and what name from Section 2.5.7 does this carry?
("A noisily-measured control is a partially-omitted control.")

**(d)** [3 pts] State the catch on the word *classical* in part (a): give one concrete way the
outcome's measurement error could be **non-classical** in Devon's crypto setting, and say why
$\hat\beta_1$ would then no longer be safe.

---

## Problem 6 — Functional form, RESET, and a Monte Carlo design (16 points)

This problem closes the chapter: a conceptual functional-form/RESET part, then a simulation-design part
that you will execute in **`nb2.5`** (`notebooks/week-02/nb2.5-biased-estimator-lab.ipynb`).

**(a)** [5 pts] Priya fits insurance premium on emissions intensity with a straight line, but the truth
is convex: $y = \beta_0 + \beta_1 x + \beta_2 x^2 + \varepsilon$ with $\beta_2 > 0$. (i) Show that
fitting only $y = \tilde\beta_0 + \tilde\beta_1 x + u$ pushes the curvature into the error,
$u = \beta_2 x^2 + \varepsilon$, and explain in one sentence why this is "the same disease as OVB" with
the omitted variable being a transformation of a variable she already has. (ii) State what the single
slope $\hat{\tilde\beta}_1$ over- and under-states, and why it describes the relationship at *neither*
low nor high emissions.

**(b)** [4 pts] Priya runs RESET on the linear fit and gets $p = 0.001$; she adds an $x^2$ term and
re-runs RESET, getting $p = 0.42$. (i) State precisely what each result tells her. (ii) Name one threat
to her premium–emissions coefficient that the clean $p = 0.42$ does **not** rule out, and explain in one
sentence why RESET is structurally blind to it.

**(c)** [7 pts] **Design a Monte Carlo** (to be implemented in `nb2.5`) that demonstrates *either* OVB
*or* attenuation — your choice. Your written design must specify, in enough detail that a classmate
could code it without further guidance:
- the **data-generating process**: every parameter (true $\beta$s, the correlation/noise structure that
  creates the bias, $N$), and which random draws produce $x$, $z$ (or $m$), $\varepsilon$, and $y$;
- the **two regressions** you will run and compare (e.g. long vs. short, or clean vs. mismeasured);
- the **theoretical prediction** the simulation should match ($\beta_1 + \beta_2\delta_1$ for OVB, or
  $\beta_1\lambda$ for attenuation), written as a formula in your chosen parameters;
- one **sweep** that makes the mechanism visible — e.g. flip the sign of $\delta_1$ and predict (via the
  two-sign rule) that the bias flips, or raise $\sigma_m$ across a grid and predict the estimate slides
  toward zero — stating the *expected pattern* before you run it;
- a one-sentence statement of what a **single, fixed-$N$** run does versus what averaging over **many
  Monte Carlo replications** does, so the reader sees that the bias is in the center of the sampling
  distribution, not in its spread.

---

*End of Problem Set 2.5. Solutions: Appendix E, `E-w2-ps2.5-solutions.md`. The companion notebook
`nb2.5-biased-estimator-lab.ipynb` lets you check Problems 3, 4, and 6 by simulation. This is the last
problem set of Week 2; every "Bias" row in the §2.5.11 ledger is answered by a research **design** in
Weeks 3 (potential outcomes, randomization) and 4 (IV, difference-in-differences, RDD) — Maya's
fair-lending question returns there with the tools to hold creditworthiness genuinely fixed.*
