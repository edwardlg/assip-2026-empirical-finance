# Problem Set 3.2 — Hand-Matching, Propensity Scores, and the Limits of Selection-on-Observables

**Covers Chapter 3.2 (Selection on Observables I: Matching & Propensity Scores).** Methods through
Ch 3.2 only: the Conditional Independence Assumption (CIA / unconfoundedness) and overlap (common
support), exact matching on discrete covariates, the average treatment effect on the treated (ATT) as
a treated-weighted average of within-cell effects, the propensity score $e(\mathbf{X}) = \Pr(D=1\mid\mathbf{X})$
and the Rosenbaum–Rubin balancing-score reduction, nearest-neighbor and caliper matching with the
bias–variance knobs, standardized mean differences (SMD) as the balance diagnostic, and the firewall
between design and outcome. Notation follows the Conventions. Potential outcomes are $Y_i(1), Y_i(0)$;
the treatment indicator is $D_i$; observed outcome $Y_i = D_i Y_i(1) + (1-D_i) Y_i(0)$; covariates
$\mathbf{X}_i$. The estimand is

$$\tau_{\text{ATT}} = \mathbb{E}[\,Y_i(1) - Y_i(0)\mid D_i = 1\,].$$

Six problems, escalating, **100 points total**. Each is self-contained, and every numerical input is
supplied so you can work by hand — no computer needed (the companion notebook `nb3.2` lets you check
Problems 2–4 by simulation). **The grading rule of this set:** a number, a match, or a "looks
balanced" stated *without naming which assumption it relies on and what it does and does not buy* earns
half credit at most. In this chapter the *reasoning about identification* is the skill, exactly as the
bias direction was the skill in Chapter 2.5. Whenever you name a threat, also name the design that
would address it (spec discipline, Conventions §4).

---

## Problem 1 — State CIA and overlap, and say what each buys (14 points)

Maya wants the causal effect of a free financial-literacy course ($D_i = 1$ if applicant $i$ enrolled)
on loan approval ($Y_i$). She plans to estimate it by selection-on-observables, conditioning on
covariates $\mathbf{X}_i$ (credit score, income, age).

**(a)** [4 pts] Write the **Conditional Independence Assumption** in potential-outcomes notation, and
translate it into one plain English sentence about what conditioning on $\mathbf{X}$ accomplishes. Then
state precisely *which term* in the naive-difference decomposition

$$\mathbb{E}[Y_i\mid D_i=1] - \mathbb{E}[Y_i\mid D_i=0] = \tau_{\text{ATT}} + \big(\mathbb{E}[Y_i(0)\mid D_i=1] - \mathbb{E}[Y_i(0)\mid D_i=0]\big)$$

CIA is designed to kill, and explain in one sentence *why* CIA kills it (work within a cell
$\mathbf{X}_i = \mathbf{x}$).

**(b)** [4 pts] Write the **overlap** (common-support) condition as an inequality on
$e(\mathbf{x}) = \Pr(D_i=1\mid \mathbf{X}_i=\mathbf{x})$, valid for every $\mathbf{x}$ in the population of
interest. Explain what *concretely* goes wrong in the estimation if overlap fails at some profile
$\mathbf{x}^\dagger$ where every applicant enrolled — i.e., what quantity becomes uncomputable, and why.

**(c)** [4 pts] CIA and overlap buy *different* things. In one sentence each, say what each one
separately guarantees: which assumption makes the within-cell treated-vs-untreated comparison *equal
to a causal effect*, and which assumption makes that comparison *exist at all*. Then name the joint
condition (CIA + overlap) and the paper that coined the term.

**(d)** [2 pts] One of these two assumptions is *partly checkable from the data alone* and the other is
*fundamentally untestable*. Say which is which, and give the one-line reason the untestable one cannot
be checked.

---

## Problem 2 — Exact matching by hand on a discrete covariate (20 points)

Forget propensity scores for now: when the only confounder is discrete with a few values, you can match
*exactly* and compute the ATT with arithmetic. Maya's lender ran a **budgeting module** ($D=1$ if the
applicant completed it) and now measures on-time repayment one year later ($Y=1$ if repaid on time).
The single confounder is the applicant's **number of prior products** with the bank (0, 1, or 2) —
more-engaged customers complete the module *and* repay more reliably regardless. The data, sorted into
exact cells, are:

| Cell ($X$ = prior products) | $n$ treated ($D=1$) | repay rate, treated | $n$ control ($D=0$) | repay rate, control |
|---|---:|---:|---:|---:|
| 0 products | 50  | $0.40$ | 150 | $0.30$ |
| 1 product  | 100 | $0.62$ | 200 | $0.50$ |
| 2 products | 150 | $0.84$ | 100 | $0.78$ |

**(a)** [4 pts] Compute the **naive** difference in repayment rates — the overall treated mean minus the
overall control mean, ignoring the cells. Show the weighted averages explicitly.

**(b)** [6 pts] Compute the three **within-cell effects** (treated rate minus control rate in each
cell). Then form the **exact-matching ATT estimate** by averaging the within-cell effects *weighted by
the treated counts*, $\widehat\tau_{\text{ATT}} = \sum_x \frac{n^{(1)}_x}{N_1}\big(\bar Y^{(1)}_x - \bar Y^{(0)}_x\big)$.
State in one sentence *why the weights are the treated counts and not the total counts* — i.e., why ATT
averages over the covariate distribution of the treated.

**(c)** [4 pts] Compute the **ATE** estimate instead — the same within-cell effects, now weighted by
each cell's *total* count $(n^{(1)}_x + n^{(0)}_x)/N$. It differs from the ATT. Explain in one sentence
which feature of the data makes ATE $\neq$ ATT here (point to where the treated are over- or
under-represented).

**(d)** [4 pts] The naive difference and the ATT differ. Compute the **selection bias** as their gap,
and identify it with the bias term from Problem 1(a): is
$\mathbb{E}[Y_i(0)\mid D_i=1]$ larger or smaller than $\mathbb{E}[Y_i(0)\mid D_i=0]$ here, and which
feature of the table tells you so?

**(e)** [2 pts] Suppose a fourth cell existed — "3 products" — with 30 treated applicants and **zero**
control applicants. What does exact matching do with those 30 treated units, which assumption from
Problem 1 is the reason, and how does dropping them change the *interpretation* of the ATT you report?

---

## Problem 3 — Propensity score from a logit, then match with a caliper (22 points)

Now the discrete confounder becomes three continuous-ish ones and exact matching is hopeless, so Maya
estimates a propensity score and matches on the single number. The lender's fitted logit for enrollment
is

$$\hat e(\mathbf{X}_i) = \frac{1}{1 + \exp\!\big(-\hat z_i\big)}, \qquad
\hat z_i = -0.4 + 0.8\,(\text{credit}_i) + 0.6\,(\text{income}_i) + 0.5\,(\text{account}_i),$$

where $\text{credit}$ and $\text{income}$ are *standardized* (mean 0, SD 1) and $\text{account}\in\{0,1\}$
indicates a prior checking account. Here are four treated applicants and five untreated controls, with
their covariates and observed repayment outcome $Y$:

| Treated | credit | income | account | $Y$ |
|---|---:|---:|---:|---:|
| T1 | $1.0$ | $1.0$ | $1$ | $1$ |
| T2 | $0.5$ | $0.0$ | $0$ | $1$ |
| T3 | $2.5$ | $2.0$ | $1$ | $1$ |
| T4 | $0.0$ | $0.5$ | $1$ | $0$ |

| Control | credit | income | account | $Y$ |
|---|---:|---:|---:|---:|
| C1 | $1.0$ | $0.5$ | $1$ | $1$ |
| C2 | $0.0$ | $0.0$ | $0$ | $0$ |
| C3 | $-0.5$ | $-0.5$ | $0$ | $0$ |
| C4 | $0.0$ | $0.8$ | $1$ | $0$ |
| C5 | $-1.0$ | $-1.0$ | $0$ | $0$ |

**(a)** [8 pts] Compute the linear index $\hat z_i$ and the propensity score $\hat e_i$ for **all nine
units**. (You may use $e^{-x}$ to two or three decimals;
$\tfrac{1}{1+e^{-1.5}} \approx 0.818$, $\tfrac{1}{1+e^{0}} = 0.5$, $\tfrac{1}{1+e^{-3.3}}\approx 0.964$
are given as anchors.) Present a small table of $(\hat z_i, \hat e_i)$.

**(b)** [6 pts] Perform **1:1 nearest-neighbor matching on the score, with replacement**: for each
treated unit, find the control with the closest $\hat e$, and record the absolute score distance. List
the four proposed pairs and their distances. State explicitly which control (if any) is reused, and why
*with replacement* is what allows that.

**(c)** [4 pts] Apply a **caliper of $0.10$ on the score**: any treated unit whose nearest control lies
more than $0.10$ away in $\hat e$ is **dropped** rather than matched. State which treated units survive
and which are dropped. Then compute the matched ATT estimate as the mean within-pair outcome difference
$\frac{1}{m}\sum (Y^{(1)} - Y^{(0)})$ over the surviving pairs.

**(d)** [4 pts] The dropped unit is the near-certain enrollee with $\hat e \approx 0.96$. (i) Explain
in causal-inference terms *why* its nearest control being far away is a problem — name the assumption
the caliper is enforcing unit-by-unit. (ii) Compute what the ATT estimate *would have been* had you
forced that unit into its nearest control (kept all four pairs), and say in one sentence why the
forced-match number is *less* trustworthy even though it uses more data.

---

## Problem 4 — Balance diagnostics: standardized mean differences before and after (16 points)

Maya has run her full match on 4,000 applicants and now must *audit* it before believing any number.
The standard tool is the **standardized mean difference** for each covariate $X_j$,

$$\text{SMD}_j = \frac{\bar X_{j,1} - \bar X_{j,0}}{s_j},$$

where $\bar X_{j,1}, \bar X_{j,0}$ are the treated and control means and $s_j$ is the pooled standard
deviation. Here are the group means before and after matching, with the (fixed) pooled SD for each
covariate:

| Covariate $X_j$ | pooled SD $s_j$ | treated mean, before | control mean, before | treated mean, after | control mean, after |
|---|---:|---:|---:|---:|---:|
| credit score (pts) | $75$ | $720$ | $660$ | $702$ | $699$ |
| income (\$000) | $30$ | $70$ | $58$ | $64$ | $62.5$ |
| debt-to-income | $0.12$ | $0.28$ | $0.34$ | $0.32$ | $0.318$ |
| employment tenure (yr) | $4$ | $8$ | $5$ | $7.6$ | $6.8$ |

**(a)** [8 pts] Compute the SMD for **each covariate, before and after matching** (eight numbers).
Present them as a table. (Keep signs.)

**(b)** [3 pts] The convention (Austin 2011; Stuart 2010) is that $|\text{SMD}_j| < 0.1$ is acceptable
balance. State which covariates clear the threshold *after* matching and which do **not**. Interpret the
"before" column in one sentence: what does the pattern of pre-matching SMDs *tell you about the
selection* — who enrolled?

**(c)** [3 pts] One covariate is still imbalanced after matching. State which, and what Maya should do
about it — and be specific that the fix is on the *design* (the propensity-score specification or
caliper), **not** a fix she finds by looking at the treatment-effect estimate. Name the chapter's term
for the firewall she must keep.

**(d)** [2 pts] Maya's teammate proposes settling the balance question with a **two-sample t-test** on
each covariate instead of the SMD. Give the one-sentence reason this is the *wrong* diagnostic for
balance, referencing how matching changes the sample size.

---

## Problem 5 — Off-support units and whose effect you are estimating (12 points)

This problem isolates common support. In Maya's data, enrollment in the literacy course rises sharply
with credit score. At the extremes: **every** applicant with a credit score above 800 enrolled (the
savviest all take the free course), and **no** applicant below 560 ever enrolled.

**(a)** [4 pts] Translate both extremes into statements about the propensity score $e(\mathbf{x})$, and
say precisely which side of the overlap inequality $0 < e(\mathbf{x}) < 1$ each one violates. For each
region, say whether the problem is "no usable control" or "no treated unit at all."

**(b)** [4 pts] State the **region of common support** in words for this example, and explain what a
caliper-matching procedure *does* with the above-800 treated applicants in practice (it does not crash —
say what happens to them). Then state the consequence: after dropping the off-support treated units,
*whose* average treatment effect on the treated is Maya actually estimating? Be precise that the
estimand has quietly changed.

**(c)** [2 pts] Maya's teammate suggests "just extrapolate" — fit a model and predict the missing
counterfactual outcomes for the above-800 treated units from the controls she does have. Name the one
honest advantage matching-with-a-caliper has over a regression that would silently do this
extrapolation (point to the relevant Chapter 3.2 argument).

**(d)** [2 pts] Suppose Maya reports her ATT *without* mentioning that 14% of treated units were
dropped for lack of support. State, in one sentence, what is misleading about the unqualified number
and the one line she should add to the paper.

---

## Problem 6 — Matching is still selection-on-observables: CIA failure as OVB (16 points)

The honest spine of the chapter. Maya's covariates are credit, income, and age. Her matching is
flawless: after caliper matching, **every** SMD is below $0.04$, including the propensity score itself.
She is about to write "the course causally raises approval by 31 percentage points."

But there is a variable she never measured: applicant **motivation** — the drive to fix one's finances
that makes someone both *seek out the free course* and *clean up their application in other ways the
lender rewards*. Motivation raises approval and raises enrollment, and it is **not in $\mathbf{X}$**.

**(a)** [4 pts] State precisely why Maya's beautiful balance table is **silent** about motivation —
i.e., why $|\text{SMD}| < 0.04$ on credit, income, and age says *nothing* about whether the matched
groups are balanced on motivation. Connect this to the claim that "CIA is untestable": which
unobservable potential outcome is the missing half of the test (cite the fundamental problem of causal
inference)?

**(b)** [5 pts] Make the equivalence to Week 2 **exact**. A confounder omitted from $\mathbf{X}$ is
precisely an omitted variable, and the bias it creates is the omitted-variable bias of Chapter 2.5,
$\beta_2\,\delta_1$. For motivation: (i) give the sign of $\beta_2$ (its effect on approval) with a
one-clause reason; (ii) give the sign of $\delta_1$ (its association with enrollment) with a one-clause
reason; (iii) apply the two-sign rule to state whether Maya's matched estimate is biased **upward or
downward**, and therefore whether she *overstates* or *understates* the course's true effect.

**(c)** [4 pts] State the chapter's bottom line: "matching does not buy you anything that
controlling-for-$\mathbf{X}$-in-a-regression does not also buy" — because *both* rest on CIA. Then list
**two** of the three honest, non-magical advantages matching *does* have over regression-with-controls
(from Section 3.2.8), and for each, say in one clause why it does **not** weaken the CIA requirement.

**(d)** [3 pts] Name the escape. Since the threat is an *unobserved* confounder, neither a fancier
matching estimator nor a richer propensity model can save Maya. Name the *kind* of research design that
*can* identify the effect with an unobserved confounder present, name the specific chapter that
develops it, and state in one clause what such a design must supply that selection-on-observables
assumes away.

---

*End of Problem Set 3.2. Solutions: Appendix E, `E-w3-ps3.2-solutions.md`. The companion notebook
`nb3.2` (`notebooks/week-03/nb3.2-psm-balance-diagnostics.ipynb`) lets you check Problems 2–4 by
simulation — build the cells, fit the logit, match with a caliper, and produce the SMD Love plot.
Problem 6's escape — identifying a causal effect when the confounder is **unobserved** — is the entire
subject of Chapter 3.4 (instrumental variables); Maya's motivation problem returns there with a design
that manufactures the exogenous variation selection-on-observables can only assume.*
