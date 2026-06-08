# Chapter 3.3 — Selection on Observables II: Entropy Balancing & Doubly-Robust Estimation

Maya has a propensity score and a problem with it.

In Ch 3.2 she did everything right. She is studying a free financial-literacy program — a
six-week course on budgeting and credit that some students at her old high school enrolled in
and some did not — and she wants to know whether enrolling later *lowered* a student's interest
rate on their first installment loan. Enrollment was not random: the students who signed up were
already a little more financially engaged, came from households with slightly higher income, had
marginally better starting credit, and skewed older. That is **selection** — exactly the bias
Ch 3.1 decomposed and Ch 3.2 set out to defeat. Following Ch 3.2, Maya estimated a **propensity
score** $e(\mathbf{X}) = \Pr(D=1 \mid \mathbf{X})$ — each student's probability of enrolling
given their observed covariates $\mathbf{X}$ (income, starting credit score, age, prior
account history) — and matched each enrollee to the non-enrollee with the nearest score.

It worked, sort of. But matching threw away a third of her control group (no good match within
the caliper), the balance table still showed her income covariate off by a noticeable margin,
and when she nudged the propensity-model specification — added an interaction here, a quadratic
there — her estimated effect wobbled by half a percentage point. She has a result. She does not
yet have a result she trusts.

This chapter is about three tools that all start from the same place Ch 3.2 left us — the
propensity score and the conditional-independence assumption — and push past the limitations of
matching. The first, **inverse-probability weighting (IPW)**, uses the propensity score not to
*pair* units but to *reweight* them, manufacturing a pseudo-population in which treatment looks
random. The second, **entropy balancing**, skips the propensity model's middleman entirely and
solves directly for weights that force the covariates into balance. The third,
**doubly-robust / augmented IPW (AIPW)**, combines a propensity model and an outcome model so
that you are protected if *either one* is right — a genuinely surprising and useful guarantee.

> **The one-sentence result of this chapter:** Under the same conditional-independence and
> overlap assumptions as Ch 3.2, you can recover the causal effect either by reweighting units
> by the inverse of their propensity score (IPW), by solving directly for weights that balance
> the covariates (entropy balancing), or — best of all — by combining a weighting model and an
> outcome model so the answer is right if *either* model is correct (doubly robust).

We are not going to re-derive the **conditional-independence assumption (CIA)** — that
$\{Y_i(0), Y_i(1)\} \perp D_i \mid \mathbf{X}_i$, the assumption that once you condition on the
observed covariates $\mathbf{X}$, who got treated is as good as random — nor the **overlap**
(or **common-support**) requirement that $0 < e(\mathbf{X}) < 1$ for everyone. Ch 3.2 earned
those. This chapter takes them as given and asks: given that they hold, what is the *smartest*
way to use them? And the recurring theme — the thread to keep your eye on — is **stability**.
All three methods are consistent in theory. They differ enormously in how badly they misbehave
when the propensity model is even slightly wrong, which in real data it always is.

A reminder of the target, in the notation from Ch 3.1. We want a causal contrast — usually the
**average treatment effect on the treated (ATT)**,

$$
\tau_{\text{ATT}} = \mathbb{E}[\,Y_i(1) - Y_i(0) \mid D_i = 1\,],
$$

the average effect *for the kind of student who actually enrolled* — or the **average treatment
effect (ATE)**, $\tau_{\text{ATE}} = \mathbb{E}[Y_i(1) - Y_i(0)]$, over everyone. The
**fundamental problem of causal inference** from Ch 3.1 is that for each student we see only one
of the two potential outcomes $Y_i(1)$ (rate if enrolled) or $Y_i(0)$ (rate if not); the other
is a missing counterfactual. Every method in this chapter is, at heart, a different clever way to
*fill in the missing column* using the units we do observe.

---

## 1. Inverse-probability weighting: building a pseudo-population

### 1.1 The trick, stated plainly

Here is the whole idea of IPW in one image. Maya's enrollees are over-represented among
high-income, high-credit students and under-represented among low-income ones — that is what
selection *means*. Suppose a particular high-income student had a propensity score of
$e(\mathbf{X}) = 0.8$: students like her enrolled 80% of the time. Then among the treated group,
students like her are *over*-counted relative to the population, because most of them ended up
treated. To undo that, we should count each treated student not as one person but as
$1/e(\mathbf{X}) = 1/0.8 = 1.25$ people — slightly *up*-weighting her, because she stands in for
the few students like her who happen *not* to have enrolled. Symmetrically, a low-income student
with $e(\mathbf{X}) = 0.1$ who *did* enroll is rare and precious: she represents the many
students like her who did not enroll, so we count her as $1/0.1 = 10$ people.

Do the mirror image for the controls. A control student with $e(\mathbf{X}) = 0.8$ (the kind who
usually enrolls but didn't) is rare among controls and gets up-weighted by
$1/(1 - e(\mathbf{X})) = 1/0.2 = 5$; a control with $e(\mathbf{X}) = 0.1$ is common and gets a
weight of $1/0.9 \approx 1.11$.

> **IPW in one sentence:** weight each treated unit by $1/e(\mathbf{X}_i)$ and each control unit
> by $1/(1 - e(\mathbf{X}_i))$, and the reweighted treated and control groups have the *same*
> covariate distribution — so comparing their average outcomes is no longer apples-to-oranges.

The reweighted dataset is called a **pseudo-population**. In it, by construction, the covariates
$\mathbf{X}$ are independent of treatment $D$: treatment is *as good as randomly assigned*, which
is exactly the world a randomized experiment lives in. And in that world the naive
difference-in-means is an unbiased causal estimate. We have not run an experiment; we have
*reweighted our way into a fake one.*

### 1.2 Why it works — the algebra behind the magic

Why does dividing by the propensity score recover the right average? The key is one line of
expectation algebra. Take the treated arm. We want $\mathbb{E}[Y_i(1)]$, the average outcome if
*everyone* were treated. We only observe $Y_i$ for the units with $D_i = 1$. Consider the
weighted quantity

$$
\mathbb{E}\!\left[\frac{D_i\, Y_i}{e(\mathbf{X}_i)}\right].
$$

The factor $D_i$ zeroes out every control (they contribute nothing), so the expectation only
runs over treated units, where $Y_i = Y_i(1)$. Now use the law of iterated expectations,
conditioning on $\mathbf{X}_i$ first:

$$
\mathbb{E}\!\left[\frac{D_i\,Y_i(1)}{e(\mathbf{X}_i)}\right]
= \mathbb{E}\!\left[\, \mathbb{E}\!\left[\frac{D_i\,Y_i(1)}{e(\mathbf{X}_i)} \,\Big|\, \mathbf{X}_i\right]\right].
$$

Inside the inner expectation, $e(\mathbf{X}_i)$ is a constant (we have fixed $\mathbf{X}_i$), so
it comes out front. And under CIA, $D_i$ is independent of $Y_i(1)$ given $\mathbf{X}_i$, so the
expectation of their product factors:

$$
\mathbb{E}\!\left[\frac{D_i\,Y_i(1)}{e(\mathbf{X}_i)} \,\Big|\, \mathbf{X}_i\right]
= \frac{1}{e(\mathbf{X}_i)}\, \mathbb{E}[D_i \mid \mathbf{X}_i]\, \mathbb{E}[Y_i(1) \mid \mathbf{X}_i]
= \frac{1}{e(\mathbf{X}_i)}\, e(\mathbf{X}_i)\, \mathbb{E}[Y_i(1) \mid \mathbf{X}_i].
$$

The propensity scores cancel — that is the whole trick — leaving
$\mathbb{E}[Y_i(1) \mid \mathbf{X}_i]$, whose outer expectation over $\mathbf{X}$ is exactly
$\mathbb{E}[Y_i(1)]$. The same argument with $(1 - D_i)/(1 - e(\mathbf{X}_i))$ recovers
$\mathbb{E}[Y_i(0)]$. Subtract, and you have the ATE. The cancellation of $e(\mathbf{X}_i)$ in
that middle step is the entire reason inverse-*probability* weighting works: dividing by the
probability of selection exactly undoes the over- or under-sampling that selection created.

### 1.3 Two estimators: Horvitz–Thompson and Hájek

Turning that expectation into a formula you can run on data gives the **Horvitz–Thompson
estimator** (the name comes from 1950s survey sampling, where the same inverse-probability idea
was invented to handle unequal sampling rates):

$$
\hat\tau_{\text{HT}}
= \frac{1}{N}\sum_{i=1}^{N} \frac{D_i\,Y_i}{\hat e(\mathbf{X}_i)}
- \frac{1}{N}\sum_{i=1}^{N} \frac{(1-D_i)\,Y_i}{1 - \hat e(\mathbf{X}_i)},
$$

where $\hat e(\mathbf{X}_i)$ is the estimated propensity score from Ch 3.2 (typically a logit).
This is a direct translation of the two expectations above, with sample averages standing in for
$\mathbb{E}[\cdot]$.

There is a subtle defect, though. The weights $1/\hat e(\mathbf{X}_i)$ do not, in any given
sample, add up to $N$ — they add up to whatever they happen to add up to. So the Horvitz–Thompson
"average" is dividing the weighted sum of outcomes by $N$ rather than by the actual total weight,
which can make it numerically wild and even push an estimated mean outside the range of the data.
The fix is to **normalize the weights so they sum to one within each arm**, giving the **Hájek
estimator**:

$$
\hat\tau_{\text{H\'ajek}}
= \frac{\sum_i \dfrac{D_i\,Y_i}{\hat e(\mathbf{X}_i)}}{\sum_i \dfrac{D_i}{\hat e(\mathbf{X}_i)}}
- \frac{\sum_i \dfrac{(1-D_i)\,Y_i}{1 - \hat e(\mathbf{X}_i)}}{\sum_i \dfrac{1-D_i}{1 - \hat e(\mathbf{X}_i)}}.
$$

The numerators are the same; the denominators are now the *sum of the weights* in each arm
rather than $N$. This is a self-normalizing weighted mean, it is far more stable in practice, and
it is what essentially every software package means when it says "IPW." Use Hájek, not raw
Horvitz–Thompson. The distinction is the IPW version of the lesson from Ch 1: an estimator can be
unbiased in expectation (Horvitz–Thompson) and still be a bad idea in finite samples because its
variance is enormous.

### 1.4 A worked number

Make it concrete with a tiny pseudo-population. Maya has six students; three enrolled ($D=1$),
three did not. The outcome $Y$ is the interest rate (in percentage points); $\hat e$ is the
estimated propensity score.

| Student | $D$ | $\hat e$ | $Y$ (rate) | weight |
|---|---|---|---|---|
| A | 1 | 0.8 | 7.0 | $1/0.8 = 1.25$ |
| B | 1 | 0.5 | 8.0 | $1/0.5 = 2.00$ |
| C | 1 | 0.2 | 9.0 | $1/0.2 = 5.00$ |
| D | 0 | 0.8 | 9.5 | $1/0.2 = 5.00$ |
| E | 0 | 0.5 | 9.0 | $1/0.5 = 2.00$ |
| F | 0 | 0.2 | 8.5 | $1/0.8 = 1.25$ |

The Hájek treated mean is the weighted average of A, B, C:
$\frac{1.25(7) + 2(8) + 5(9)}{1.25 + 2 + 5} = \frac{8.75 + 16 + 45}{8.25} = \frac{69.75}{8.25}
\approx 8.45$. The Hájek control mean is the weighted average of D, E, F:
$\frac{5(9.5) + 2(9) + 1.25(8.5)}{5 + 2 + 1.25} = \frac{47.5 + 18 + 10.625}{8.25} =
\frac{76.125}{8.25} \approx 9.23$. The IPW estimate is $8.45 - 9.23 = -0.78$ percentage points —
enrolling lowered the rate by about three-quarters of a point.

Notice what the weights did. Student C (a low-propensity enrollee — the rare student "like a
control" who enrolled anyway) got a weight of 5 and dominates the treated mean, pulling it toward
the higher rate she carries. Student D (a high-propensity control — the rare student "like a
treated" who didn't enroll) likewise got weight 5 and dominates the control mean. The estimator
leans hardest on exactly the units that look like the *other* group, because those are the units
that tell us about the missing counterfactual. The simple unweighted difference, by contrast,
would have been $8.0 - 9.0 = -1.0$ — a different answer, because the unweighted version lets
selection contaminate the comparison.

### 1.5 When IPW explodes — and what to do about it

Now the failure mode, because reveal-the-trick demands we say what breaks. Look at student C's
weight of 5, and imagine her propensity score had been estimated at $\hat e = 0.02$ instead of
$0.2$. Her weight becomes $1/0.02 = 50$. One student would carry the weight of fifty, and the
entire treated mean would be hostage to that single observation's outcome and to the accuracy of
that one tiny estimated probability. This is the **IPW explosion problem**, and it is the central
practical hazard of the method: as $\hat e(\mathbf{X}_i) \to 0$ for a treated unit (or
$\to 1$ for a control), the weight $\to \infty$, and the estimator's variance blows up.

This is not a rare edge case; it is the *typical* situation whenever overlap is thin. Recall from
Ch 3.2 that overlap requires $0 < e(\mathbf{X}) < 1$ for everyone. IPW is exquisitely sensitive
to near-violations of overlap: a unit whose covariates make treatment nearly certain or nearly
impossible gets an astronomically large weight, and a handful of such units can swamp everything.
A single mis-estimated propensity score near zero can move your headline number by a percentage
point. Worse, the symptom is quiet — you get an estimate and a standard error; nothing throws an
error — so you have to *look* for it.

Three standard defenses, in increasing order of how much you should reach for them:

**Trimming.** Drop (or set aside) units with extreme estimated propensity scores — a common rule
is to discard observations with $\hat e < 0.01$ or $\hat e > 0.99$, or to restrict to the region
of common support where treated and control scores overlap. Trimming changes the estimand
slightly (you are now estimating the effect on the trimmable subpopulation), so you must report
how many units you dropped and re-run without trimming as a robustness check.

**Stabilized weights.** Instead of $1/\hat e(\mathbf{X}_i)$, use
$\hat p \,/\, \hat e(\mathbf{X}_i)$ for the treated and
$(1-\hat p)\,/\,(1 - \hat e(\mathbf{X}_i))$ for controls, where $\hat p = \Pr(D=1)$ is the
overall (marginal) treatment share. Multiplying by the marginal probability shrinks the variance
of the weights without changing what they estimate — the giant weights get tamed by a constant
factor — and it is essentially free. Most modern IPW uses stabilized weights by default.

**Just diagnose the weights.** Always print the distribution of your weights: the max, the 99th
percentile, and the **effective sample size** $\big(\sum_i w_i\big)^2 / \sum_i w_i^2$, which tells
you how many "real" observations your weighted sample is worth. If your 600-student sample has an
effective sample size of 40 because three units carry half the weight, no amount of trimming will
save you — your data simply do not contain a credible counterfactual, and you should say so.

The honest summary: IPW is beautiful in theory and treacherous in practice, and the treachery is
entirely about extreme weights born of thin overlap. That treachery is precisely what the next
method was invented to avoid.

---

## 2. Entropy balancing: solve for the weights directly

### 2.1 The complaint that motivates it

Step back and notice something odd about the whole propensity-score pipeline, IPW and matching
alike. We do not actually *care* about the propensity score. It is a means to an end: a
*correctly specified* propensity model would, if we reweight by it, balance the covariates. But
balancing the covariates is the *goal*; the propensity model is just an indirect route to it. We
fit a logit, hope it is the right functional form, convert its predictions into weights, and then
— this is the embarrassing part — *check afterward* whether the covariates actually came out
balanced (the balance diagnostics of Ch 3.2). If they did not, we go back and add interactions
and polynomials to the propensity model and try again, fishing for a specification that produces
balance.

Jens Hainmueller's **entropy balancing** (2012) asks the obvious question: if balance is what we
want, why not just *solve for it directly*?[^hainmueller] Skip the propensity model. State the
balance conditions you want — "the reweighted control group must have the same mean income, mean
credit score, and mean age as the treated group" — as exact mathematical constraints, and find
weights on the controls that satisfy them. There will be many such weight vectors (the
constraints are far fewer than the number of control units), so among all weight vectors that
achieve exact balance, pick the one that is **closest to uniform** — that disturbs the data the
least. "Closest to uniform" is made precise by maximizing **entropy**, which is where the name
comes from.

[^hainmueller]: Hainmueller, J. (2012). Entropy Balancing for Causal Effects: A Multivariate
Reweighting Method to Produce Balanced Samples in Observational Studies. *Political Analysis*,
20(1), 25–46.

### 2.2 The optimization, in plain terms

Set up to estimate the ATT (the most common use). We will reweight the **control** units to look
like the treated group, then compare. Let $w_i$ be the weight on control unit $i$. The problem is

$$
\min_{\{w_i\}} \; \sum_{i \in \text{control}} w_i \log\!\frac{w_i}{q_i}
\quad\text{subject to balance and normalization constraints,}
$$

where $q_i$ is a *base weight* (uniform, $q_i = 1/N_c$, unless you have a reason otherwise). That
objective $\sum w_i \log(w_i / q_i)$ is the **Kullback–Leibler divergence** of the weights from
uniform — a standard measure of how far one distribution is from another. Minimizing it is the
same as *maximizing entropy*: it keeps the weights as flat and as close to the base weights as
possible. Flat weights are good weights — they mean no single unit dominates, which is exactly the
explosion problem IPW could not control.

The constraints are where you say what balance means. For each covariate $X_k$ you want to match,
you impose

$$
\sum_{i \in \text{control}} w_i\, X_{ik} \;=\; \bar X_{k}^{\text{treated}},
$$

i.e. the *weighted mean* of covariate $k$ among controls must **exactly equal** the treated-group
mean of that covariate. You can add a second moment to match variances —
$\sum_i w_i (X_{ik} - \bar X_k^{\text{treated}})^2 = $ treated variance — or cross-moments to
match covariances. Plus the normalization $\sum_i w_i = 1$ and non-negativity $w_i \ge 0$.

Two things make this both powerful and unusual. First, balance is **exact, not approximate**: the
income means do not come out "close," they come out *equal*, by construction, to as many decimals
as you like. There is no post-hoc balance check that can fail, because balance is the constraint,
not the hope. Second, you choose *which moments* to balance — means only, or means and variances,
or higher moments — making it transparent and tunable in a way the black-box logit is not. You
are stating your balance requirements as an explicit, inspectable list.

The solution has a tidy closed form. Because of the entropy objective, the optimal weights turn
out to be exponential in the covariates,
$w_i \propto q_i \exp\!\big(-\sum_k \lambda_k X_{ik}\big)$, where the $\lambda_k$ are
Lagrange multipliers chosen to satisfy the constraints — found quickly by a low-dimensional
convex optimization (one $\lambda$ per balance condition, not one per unit). You do not need to
implement this by hand; the point is that it is a small, well-behaved problem with a unique
answer, not a fishing expedition.

### 2.3 Why it is usually more stable than PSM and IPW

Here is the punchline, and the reason entropy balancing has become a workhorse in empirical
finance. Plain IPW gets balance *only if the propensity model is correctly specified*, and even
then only *approximately* in any finite sample — and it pays for misspecification with exploding
weights. Entropy balancing **guarantees exact balance on the moments you chose, in every sample,
by construction**, while *simultaneously* keeping the weights as close to uniform as the
constraints allow. It gives you the thing IPW only promises (balance) without the thing IPW
inflicts (wild weights).

There is even a deep connection: entropy balancing is *equivalent* to a particular logistic
propensity model — but one fit by a loss function that targets covariate balance directly rather
than predictive likelihood. So it is not magic from nowhere; it is what you get when you stop
asking the propensity model to predict treatment well and start asking it to balance covariates
well, which is what you actually needed all along.

The practical contrast with matching (Ch 3.2) is just as sharp. Matching *discards* units (the
unmatched controls, the ones outside the caliper) — Maya lost a third of her control group.
Entropy balancing *keeps every unit* and simply gives some of them small weights; nothing is
thrown away, so you retain more information and more precision. And it sidesteps the
specification-search problem: there is no "which matching algorithm, which caliper, with or
without replacement" menu to agonize over and to invite reviewer suspicion that you picked the
spec that gave the prettiest answer.

### 2.4 Maya, reweighted

Back to Maya. She wants the ATT: the effect of enrolling, for the kind of student who enrolled.
She reweights her **non-enrollees** so that their weighted means of income, starting credit
score, age, and prior-account count *exactly* match the enrollees' means, while keeping the
weights as flat as possible. After solving, her balance table is perfect — every covariate
difference is mechanically zero — and her effective sample size among controls is, say, 410 out
of 600, a mild and honest cost. The reweighted control mean rate is $9.1$; the (unweighted, since
this is ATT) enrollee mean is $8.4$; her entropy-balanced ATT is $8.4 - 9.1 = -0.7$ percentage
points. Crucially, when she re-runs adding *variance* matching, the number barely moves — a
reassurance the IPW wobble never gave her, because the estimate no longer rides on a fragile
functional form. This is the kind of robustness that turns "I have a result" into "I have a result
I trust."

A Priya variant to show it generalizes beyond Maya's loans. Priya studies **climate insurance**:
she wants to know whether buying parametric drought insurance changed a smallholder farm's
investment in irrigation. Insured and uninsured farms differ on rainfall variability, farm size,
distance to a bank branch, and prior losses — classic selection. Rather than match or fit a logit,
Priya entropy-balances the uninsured farms to share the insured farms' means (and variances) of
those four covariates, then compares irrigation spending. The weights stay tame even though a few
insured farms sit in unusual rainfall zones (the units that would have blown up an IPW estimator),
precisely because the entropy objective refuses to let any one farm's weight run away. Same
estimand, same assumptions as IPW — far steadier in hand.

---

## 3. Doubly-robust / Augmented IPW: two shots at the truth

### 3.1 The setup: two models, two ways to be right

So far we have leaned entirely on a *model of treatment* — the propensity score, or the balancing
weights, which is the same job in different clothes. There is a completely different route to the
counterfactual that we have so far only mentioned: a **model of the outcome**. Fit a regression of
$Y$ on $\mathbf{X}$ separately in the treated and control groups, getting predicted outcomes
$\hat\mu_1(\mathbf{X}) = \hat{\mathbb{E}}[Y \mid \mathbf{X}, D=1]$ and
$\hat\mu_0(\mathbf{X}) = \hat{\mathbb{E}}[Y \mid \mathbf{X}, D=0]$. Then impute each unit's missing
counterfactual with the model's prediction and average the difference:
$\hat\tau_{\text{reg}} = \frac{1}{N}\sum_i [\hat\mu_1(\mathbf{X}_i) - \hat\mu_0(\mathbf{X}_i)]$.
This is **regression imputation** (sometimes "g-computation"), and under CIA it is also
consistent — *if the outcome model is correctly specified*.

So we have two strategies, each consistent under CIA but each leaning on a *different* modeling
assumption:

- **IPW / weighting** is consistent if the **propensity model** $\hat e(\mathbf{X})$ is correct.
  It does not care whether the outcome is linear in $\mathbf{X}$.
- **Regression imputation** is consistent if the **outcome model** $\hat\mu_d(\mathbf{X})$ is
  correct. It does not care whether you got the propensity score right.

In real data you are never *sure* either model is correct. Wouldn't it be nice to hedge — to use
both, in a way that is forgiving if one of them is wrong?

### 3.2 The estimator, and why "doubly"

That hedge exists. It is the **augmented inverse-probability-weighted (AIPW)** estimator, also
called **doubly robust**, developed by Robins, Rotnitzky, and Zhao (1994).[^rrz] For the ATE it
is, per arm,

$$
\hat\mu_1^{\text{DR}}
= \frac{1}{N}\sum_{i=1}^N \left[ \hat\mu_1(\mathbf{X}_i)
+ \frac{D_i\,\big(Y_i - \hat\mu_1(\mathbf{X}_i)\big)}{\hat e(\mathbf{X}_i)} \right],
$$

with the symmetric formula for $\hat\mu_0^{\text{DR}}$ (replace $D_i$ with $1-D_i$,
$\hat\mu_1$ with $\hat\mu_0$, and $\hat e$ with $1-\hat e$), and
$\hat\tau_{\text{DR}} = \hat\mu_1^{\text{DR}} - \hat\mu_0^{\text{DR}}$.

[^rrz]: Robins, J. M., Rotnitzky, A., & Zhao, L. P. (1994). Estimation of Regression Coefficients
When Some Regressors Are Not Always Observed. *Journal of the American Statistical Association*,
89(427), 846–866. The doubly-robust / AIPW form is developed and extended across this line of
work by Robins and Rotnitzky and coauthors through the 1990s.

Read the bracket as a sum of two pieces. The first piece, $\hat\mu_1(\mathbf{X}_i)$, is the
**outcome-regression prediction** — the regression-imputation estimate. The second piece is an
**IPW correction applied to the regression's residuals**: it takes the part the outcome model got
*wrong* on the treated units, $Y_i - \hat\mu_1(\mathbf{X}_i)$, and reweights it by
$1/\hat e(\mathbf{X}_i)$. So AIPW starts from the outcome model's best guess and then patches it
using inverse-probability-weighted residuals. The word **augmented** is literal: it is IPW
*augmented* with an outcome model, or equivalently the outcome model *augmented* with an IPW
correction.

Now the "doubly" — the surprising part that earns the method its fame. **The estimator is
consistent if EITHER the propensity model OR the outcome model is correct; you do not need both.**
You get two independent shots at the truth, and you only have to hit with one. Here is why,
informally, by checking the two cases:

*Case 1 — the outcome model is right, the propensity model is wrong.* Then
$\hat\mu_1(\mathbf{X}_i)$ already estimates $\mathbb{E}[Y(1) \mid \mathbf{X}_i]$ correctly. The
correction term has expectation zero because, with a correct outcome model, the residual
$Y_i - \hat\mu_1(\mathbf{X}_i)$ averages to zero *within each value of* $\mathbf{X}$ — so no matter
what (possibly wrong) weights $1/\hat e$ you multiply those residuals by, they still average out
to zero. The wrong propensity score is multiplied into something that vanishes. The first term
carries the day.

*Case 2 — the propensity model is right, the outcome model is wrong.* Then $\hat\mu_1$ is some
incorrect prediction. But the second term, with the *correct* $e(\mathbf{X})$, is exactly the IPW
estimator applied to $Y_i$ — which we proved in §1.2 is consistent — *minus* an IPW-weighted term
in $\hat\mu_1$ that, with correct propensity scores, precisely cancels the wrong $\hat\mu_1$ sitting
in the first piece. The bad outcome model gets added in by the first term and *subtracted back out*
by the second, leaving the consistent IPW estimate standing. The IPW machinery carries the day.

Either way, one correct model is enough; the other model's errors get neutralized. That is the
doubly-robust property, and it is genuinely remarkable: a kind of statistical insurance policy where
you only need one of two claims to be valid.

### 3.3 Why this matters beyond the safety net

Doubly robust is not just defensive. It also tends to be *more efficient* — lower variance — than
plain IPW when both models are even roughly right, because the outcome model soaks up much of the
variation in $Y$ before the noisy inverse-probability weights ever touch it. The weights now act on
*residuals* (small, after a decent regression) rather than on the raw outcomes (large), so the
weight-explosion damage is muffled even when some $\hat e$ are small. AIPW does not fully cure the
extreme-weight problem — a $\hat e$ near zero still hurts — but it leans on those weights far less.

There is a deeper modern reason AIPW is everywhere now. Because the estimator has a special
"insensitivity" to small errors in *each* model (a property called **Neyman orthogonality**), you
can plug **machine-learning estimators** — random forests, gradient boosting, neural nets — into
both the propensity model and the outcome model, use sample-splitting (fit the models on one half,
evaluate on the other) to avoid overfitting, and still get valid standard errors and confidence
intervals for the treatment effect. This is the engine behind **double/debiased machine learning**
(Chernozhukov et al., 2018),[^dml] the dominant framework for high-dimensional causal estimation
in current empirical economics and finance. You will not implement that this week, but it is worth
knowing that the humble bracket above is the seed of the field's most active methodology. AIPW is
where selection-on-observables grows up.

[^dml]: Chernozhukov, V., Chetverikov, D., Demirer, M., Duflo, E., Hansen, C., Newey, W., & Robins,
J. (2018). Double/Debiased Machine Learning for Treatment and Structural Parameters.
*The Econometrics Journal*, 21(1), C1–C68.

---

## 4. The code

One runnable script ties the three methods together on a simulated dataset where we *know* the
true effect, so you can watch which estimators land near it and which wander. We build Maya's
financial-literacy setup: enrollment depends on income and credit (so there is selection), and
the true effect of enrolling is a $-0.8$ percentage-point reduction in the rate.

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

rng = np.random.default_rng(33)
N = 4000

# --- covariates ---
income = rng.normal(0, 1, N)          # standardized household income
credit = rng.normal(0, 1, N)          # standardized starting credit score

# --- selection into treatment (the propensity TRUTH) ---
lin = 0.9 * income + 0.7 * credit
p_true = 1 / (1 + np.exp(-lin))       # true propensity score
D = (rng.uniform(size=N) < p_true).astype(int)

# --- outcomes: TRUE treatment effect is -0.8; outcome depends on X too ---
tau_true = -0.8
y0 = 9.0 - 0.6 * income - 0.5 * credit + rng.normal(0, 1, N)   # rate if NOT enrolled
y1 = y0 + tau_true                                             # rate if enrolled
Y = np.where(D == 1, y1, y0)          # we observe only one potential outcome each

df = pd.DataFrame({"Y": Y, "D": D, "income": income, "credit": credit})

# --- (0) naive difference in means: biased by selection ---
naive = df.loc[df.D == 1, "Y"].mean() - df.loc[df.D == 0, "Y"].mean()

# --- estimate the propensity score (a logit), then build stabilized IPW weights ---
ps = smf.logit("D ~ income + credit", data=df).fit(disp=0)
ehat = ps.predict(df).clip(0.01, 0.99)        # clip = trimming extreme scores
p_marg = df.D.mean()
w = np.where(df.D == 1,
             p_marg / ehat,                    # stabilized treated weight
             (1 - p_marg) / (1 - ehat))        # stabilized control weight

# --- (1) IPW (Hajek): self-normalizing weighted means per arm ---
def hajek_mean(mask):
    ww = w[mask]
    return np.sum(ww * df.Y[mask]) / np.sum(ww)
ipw = hajek_mean(df.D == 1) - hajek_mean(df.D == 0)

# --- (2) Augmented IPW / doubly robust ---
m1 = smf.ols("Y ~ income + credit", data=df[df.D == 1]).fit()   # outcome model, treated
m0 = smf.ols("Y ~ income + credit", data=df[df.D == 0]).fit()   # outcome model, control
mu1 = m1.predict(df); mu0 = m0.predict(df)
dr1 = np.mean(mu1 + df.D * (df.Y - mu1) / ehat)
dr0 = np.mean(mu0 + (1 - df.D) * (df.Y - mu0) / (1 - ehat))
aipw = dr1 - dr0

print(f"true effect      : {tau_true:+.3f}")
print(f"naive diff       : {naive:+.3f}   (biased by selection)")
print(f"IPW (Hajek)      : {ipw:+.3f}")
print(f"AIPW (doubly rob): {aipw:+.3f}")
print(f"weights: max={w.max():.1f}  eff. N={w.sum()**2/np.sum(w**2):.0f} of {N}")
```

Run it and the naive difference comes out badly biased toward zero (selection makes enrollees and
non-enrollees differ in the outcome for reasons that have nothing to do with the program), while
both IPW and AIPW land close to the true $-0.8$. The printed weight diagnostics — the max weight
and the effective sample size — are the habit to internalize: *always look at your weights.* For
the entropy-balancing comparison, the `EBweights`/`ebal` route (or a short convex solve) is the
subject of nb3.3, where you will see entropy weights deliver exact balance with a smaller max
weight than IPW on the very same data.

To *feel* the double-robustness property, change the outcome models `m1`/`m0` to deliberately
wrong specifications (drop `credit`, or add a spurious term) and watch AIPW stay near $-0.8$
because the propensity model is still right; then instead corrupt the propensity formula (drop
`credit` from the logit) while keeping the outcome models correct, and watch AIPW *still* stay
near $-0.8$. Break *both* at once and it finally drifts. That experiment — one model wrong at a
time is survivable, both wrong is not — is the whole "doubly" in one screen.

---

## 5. A practical decision guide: PSM vs. entropy balancing vs. AIPW

You now have, across Ch 3.2 and Ch 3.3, four ways to exploit selection-on-observables. Here is how
to choose, stated as the kind of judgment you should be able to defend to a referee.

**Reach for propensity-score matching (Ch 3.2) when** you want a transparent, intuitive design and
your treated and control groups overlap well. Matching's appeal is that it *mimics an experiment*
unit by unit and is easy to explain to a non-technical audience ("we compared each enrollee to a
nearly identical non-enrollee"). Its costs are the ones Maya hit: it discards unmatched units, it
forces a menu of arbitrary choices (caliper, with/without replacement, number of neighbors), and
it only achieves *approximate* balance that you must check after the fact. Good for exposition and
for a first look; rarely your final, most efficient estimator.

**Reach for entropy balancing when** you want guaranteed exact balance on chosen moments, maximum
stability, and minimal specification angst — which in practice is *most of the time* in empirical
finance. It keeps every unit, produces tame weights by construction, makes your balance targets
explicit and inspectable, and is hard for a referee to accuse of cherry-picking because there is no
algorithm-and-caliper menu to fish through. Its limitation is that you must *choose* which moments
to balance, and it balances only those — if the true selection depends on a high-order interaction
you did not include, you have not balanced it. State your moments and defend them.

**Reach for AIPW / doubly-robust when** you want the strongest consistency guarantee and the best
efficiency, and especially when you are willing to bring an outcome model and a treatment model and
let them cover for each other. This is the right default for a *headline* causal estimate you intend
to publish: it is consistent if either model is right, it is more efficient than plain IPW, and it
is the on-ramp to machine-learning-based estimation if your covariate set is large. Its cost is
conceptual overhead (two models, not one) and that it still suffers — though less — from extreme
weights.

The honest meta-advice: **report more than one.** If PSM, entropy balancing, and AIPW all point to
roughly $-0.8$, your finding is robust to method choice and you can write it up with confidence. If
they disagree, that disagreement is *information* — almost always a sign of thin overlap or a
fragile specification — and the disagreement itself belongs in your paper, not swept under the rug
of whichever method gave the prettiest number. This is the empirical-spec discipline from the
Conventions applied to method choice: name the estimand (ATE or ATT), name the covariates you
balanced on, name the overlap region you restricted to, and name the assumption — CIA — that the
whole exercise rides on.

---

## 6. The ceiling on everything in this chapter — and the door out

Stand back and see the boundary of what Week 3 has built so far. IPW, entropy balancing, AIPW,
and the matching of Ch 3.2 are *four different engines bolted to the same chassis*, and that
chassis is the **conditional-independence assumption**: that once we condition on (or balance, or
reweight on) the *observed* covariates $\mathbf{X}$, treatment is as good as random. Every method
in this chapter is a way to use $\mathbf{X}$ more cleverly, more stably, more efficiently. Not one
of them can rescue you if CIA is false.

And CIA is false exactly when there is an **unobserved confounder** — a variable that drives both
selection into treatment *and* the outcome, that you did not measure and therefore cannot put in
$\mathbf{X}$. Suppose the students who enrolled in Maya's program were also, on average, more
*conscientious* in a way no dataset captures, and conscientiousness independently lowers interest
rates. Then enrollees would have gotten lower rates even without the program, no amount of
balancing on income and credit removes it, and *every estimator in this chapter is biased* —
silently, with a clean-looking balance table and a confident standard error. Balancing the
observables you have does nothing about the confounder you don't. This is the unbreakable ceiling
of selection-on-observables, and it is why a careful researcher always asks, "what's the
unobserved thing that could be driving both?"

That question is the doorway to Ch 3.4. When you cannot defend CIA — when you fear an unobserved
confounder you cannot measure — you need a fundamentally different source of identifying variation:
not a richer set of controls, but an **instrument**, a variable that shoves units into treatment
for reasons unrelated to the outcome. Ch 3.4 introduces **instrumental variables** as the escape
hatch for precisely the situation this chapter cannot handle. Everything in Week 3 up to now has
assumed selection-on-observables; the rest of the week is about what to do when that assumption
finally breaks.

---

## Your Turn

Open **nb3.3 — entropy balancing vs. IPW vs. AIPW.** You will take a single simulated dataset with
a known treatment effect and selection on observables, and run all three estimators side by side:
build stabilized IPW (Hájek) weights and inspect their distribution and effective sample size;
solve for entropy-balancing weights that exactly match covariate means (then means *and*
variances) and confirm the balance table comes out mechanically perfect; and compute the AIPW
estimate, then deliberately break the propensity model, then instead break the outcome model, and
watch the doubly-robust estimator survive each single failure but not their conjunction. The goal
is to *see*, with your own data, why entropy weights stay tame where IPW weights explode, and why
"doubly robust" is more than a slogan.

**Check questions.**

1. A treated unit in Maya's data has an estimated propensity score of $\hat e = 0.04$. What is its
   (unstabilized) IPW weight, and why should this single number make you nervous about the IPW
   estimate? Name two distinct things you could do about it.

2. Priya runs AIPW on her climate-insurance data. A colleague says, "your outcome regression is
   surely misspecified — irrigation spending isn't linear in rainfall — so your estimate is
   garbage." Explain why this objection is *not necessarily* fatal, and state precisely the
   condition under which Priya's AIPW estimate is still consistent despite the wrong outcome model.

3. Maya's entropy-balanced ATT and her IPW ATT agree (both about $-0.7$), but her colleague Sam
   warns that *both* could still be badly biased. Describe the one kind of variable whose existence
   would make that warning correct, explain why no method in this chapter can fix it, and name the
   chapter (and tool) that addresses it.
