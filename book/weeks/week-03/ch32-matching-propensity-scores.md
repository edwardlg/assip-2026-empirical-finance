# Chapter 3.2 — Selection on Observables I: Matching & Propensity Scores

Maya is back, and this time she has a different lender and a different question. The lender runs a free **financial-literacy program** — a short course on budgeting, credit scores, and how loan terms work — that some applicants take before applying for a loan and most do not. Maya wants to know the program's causal effect on getting approved. Does sitting through the course actually raise your odds of approval, or do the people who *choose* to enroll just look better to begin with?

That parenthetical — *choose* — is the whole problem, and Chapter 3.1 gave you the language for it. Let $D_i = 1$ if applicant $i$ enrolled in the program and $D_i = 0$ if not. Each applicant has two **potential outcomes**: $Y_i(1)$, whether they would be approved *if* they took the course, and $Y_i(0)$, whether they would be approved *if* they did not. We only ever observe one of them — the **fundamental problem of causal inference** — and the one we see is $Y_i = D_i Y_i(1) + (1 - D_i) Y_i(0)$. The causal effect we want here is the **average treatment effect on the treated**, the ATT:

$$\tau_{\text{ATT}} = \mathbb{E}[\,Y_i(1) - Y_i(0) \mid D_i = 1\,],$$

the average benefit of the program *for the kind of person who actually enrolls*. (We will say a word later about why ATT, not ATE, is the natural target for matching.)

And Chapter 3.1 showed you the trap. The obvious thing — compare the approval rate of enrollees to non-enrollees — does not estimate $\tau_{\text{ATT}}$. Decompose the naive difference exactly as we did last chapter:

$$\underbrace{\mathbb{E}[Y_i \mid D_i = 1] - \mathbb{E}[Y_i \mid D_i = 0]}_{\text{naive difference}} = \underbrace{\tau_{\text{ATT}}}_{\text{what we want}} + \underbrace{\big(\mathbb{E}[Y_i(0) \mid D_i = 1] - \mathbb{E}[Y_i(0) \mid D_i = 0]\big)}_{\text{selection bias}}.$$

That second term is the **selection bias**: the gap in the *untreated potential outcome* $Y_i(0)$ between the people who enrolled and the people who did not. If the enrollees are the financially-savvier, higher-income applicants who would have been approved at higher rates *even without the course*, then $\mathbb{E}[Y_i(0)\mid D_i=1] > \mathbb{E}[Y_i(0)\mid D_i=0]$, the selection bias is positive, and the naive comparison overstates the program. Maya's job is to kill that term.

This chapter is the first of two on how to kill selection bias *when the thing driving it is observable*. The strategy has a name — **selection on observables** — and a tool: **matching**, refined into **propensity-score matching**. The reveal-the-trick promise: state the assumption that makes it work, show on real numbers why comparing look-alikes recovers $\tau_{\text{ATT}}$, watch it break, and write the code. But hold one warning in your head from the first page, because it is the honest spine of the whole chapter: **matching is not a different beast from regression with controls.** It is the same bet — the bet that you have measured the confounders — dressed in better clothes. The omitted-variable bias of Week 2 is waiting for you here under a new name. We will earn that warning, not just assert it.

---

## 3.2.1 The Conditional Independence Assumption

Start with the result in one sentence: **if treatment is "as good as randomly assigned" once you hold a set of observed characteristics $\mathbf{X}_i$ fixed, then within any group of applicants who share the same $\mathbf{X}_i$, the difference in average outcomes between the treated and untreated *is* the causal effect.**

Written formally, the assumption is the **Conditional Independence Assumption** (CIA), also called **unconfoundedness** or **selection on observables**:

$$\{Y_i(1),\, Y_i(0)\} \perp\!\!\!\perp D_i \mid \mathbf{X}_i.$$

Read the $\perp\!\!\!\perp$ as "is independent of." In words: *once you condition on the observed covariates $\mathbf{X}_i$, whether or not someone got treated carries no further information about what their potential outcomes would have been.* Treatment may be wildly correlated with potential outcomes *overall* — savvier people both enroll and get approved — but the assumption says that correlation runs *entirely through* $\mathbf{X}_i$. Fix $\mathbf{X}_i$, and the leftover variation in $D_i$ is as good as a coin flip.

It helps to compare CIA to what a randomized experiment buys you. In a randomized controlled trial, the coin flip guarantees $\{Y_i(1), Y_i(0)\} \perp\!\!\!\perp D_i$ *unconditionally* — no $\mathbf{X}$ needed, because randomization makes treated and control groups identical in expectation on *everything*, observed and unobserved. CIA asks for less and more at once: less, because it only needs independence *within* cells of $\mathbf{X}$; more, because it demands you have *measured the right $\mathbf{X}$*. CIA is "randomization, conditional on the covariates" — the claim that nature ran a stratified experiment and stratified on variables you happen to observe.

Why does CIA deliver the ATT? Here is the argument, and it is short enough to hold in your hand. Pick a value $\mathbf{x}$ of the covariates and look only at applicants with $\mathbf{X}_i = \mathbf{x}$. Among them, the average untreated outcome of the *treated* equals the average untreated outcome of the *untreated*:

$$\mathbb{E}[Y_i(0) \mid D_i = 1, \mathbf{X}_i = \mathbf{x}] = \mathbb{E}[Y_i(0) \mid D_i = 0, \mathbf{X}_i = \mathbf{x}] = \mathbb{E}[Y_i(0)\mid \mathbf{X}_i = \mathbf{x}].$$

The first equality is *exactly* CIA: conditional on $\mathbf{x}$, the treated and untreated have the same distribution of $Y(0)$, so the same mean. And the right-hand side is something we can *measure*, because for the untreated we actually observe $Y_i = Y_i(0)$. So inside the cell $\mathbf{X}_i = \mathbf{x}$, the untreated group's average outcome is a valid stand-in — a valid **counterfactual** — for what the treated would have looked like had they not been treated. The within-cell treated-minus-untreated difference is therefore

$$\mathbb{E}[Y_i \mid D_i=1, \mathbf{X}_i = \mathbf{x}] - \mathbb{E}[Y_i \mid D_i=0, \mathbf{X}_i = \mathbf{x}] = \mathbb{E}[Y_i(1) - Y_i(0)\mid \mathbf{X}_i = \mathbf{x}],$$

a clean causal effect *for that cell*. The selection-bias term from the chapter opening — the gap in $Y(0)$ between the groups — has been zeroed out *within the cell*, because CIA says there is no such gap once $\mathbf{x}$ is fixed. To get the ATT, average these within-cell effects over the distribution of $\mathbf{X}$ *among the treated*:

$$\tau_{\text{ATT}} = \mathbb{E}_{\mathbf{X} \mid D=1}\big[\,\mathbb{E}[Y_i \mid D_i=1,\mathbf{X}] - \mathbb{E}[Y_i \mid D_i=0,\mathbf{X}]\,\big].$$

That is the entire engine of selection-on-observables. **Compare like with like, then average.** Everything else in this chapter — matching, calipers, propensity scores — is machinery for doing that comparison well when $\mathbf{X}$ is high-dimensional. The idea never changes.

A number before the Greek letters, to make this concrete. Suppose Maya's only confounder is a single binary variable: whether the applicant already had a checking account, $\mathbf{X}_i \in \{\text{account}, \text{no account}\}$. The existing-account applicants are savvier and would be approved more often regardless. Here are the cells:

| Cell | # enrolled ($D=1$) | approval rate, enrolled | # not enrolled ($D=0$) | approval rate, not enrolled | within-cell effect |
|---|---:|---:|---:|---:|---:|
| account | 600 | $0.80$ | 400 | $0.65$ | $+0.15$ |
| no account | 200 | $0.50$ | 800 | $0.40$ | $+0.10$ |

The **naive** comparison ignores the cells: enrollee approval is $(600\cdot0.80 + 200\cdot0.50)/800 = 0.725$, non-enrollee approval is $(400\cdot0.65 + 800\cdot0.40)/1200 = 0.483$, a gap of $0.242$. But that gap is inflated, because enrollees are disproportionately account-holders (the higher-baseline cell). The **exact-matching** estimate instead takes each within-cell effect and averages it *with weights equal to the treated counts*, since ATT averages over the covariate distribution of the *treated*: $\tau_{\text{ATT}} = (600\cdot0.15 + 200\cdot0.10)/800 = 0.1375$. Comparing like with like and averaging over the enrollees' own mix of accounts gives $13.75$ percentage points — barely half the naive $24.2$. The difference, $0.242 - 0.1375 \approx 0.10$, is the selection bias, removed by conditioning on the one confounder. This is the whole method on two cells; the rest of the chapter is what to do when there are 12,000.

---

## 3.2.2 Overlap: you can only compare where both kinds exist

There is a second assumption hiding in that argument, and it is easy to miss because it is so obvious once stated. To compute the within-cell difference at $\mathbf{X}_i = \mathbf{x}$, you need *both* a treated unit and an untreated unit at $\mathbf{x}$. If every applicant with a given profile enrolled — no untreated comparison exists — you have no counterfactual and the cell is useless. This is the **overlap** or **common support** condition:

$$0 < \Pr(D_i = 1 \mid \mathbf{X}_i = \mathbf{x}) < 1 \quad \text{for all } \mathbf{x} \text{ in the population of interest.}$$

In words: at *every* covariate profile, there is a positive chance of being treated and a positive chance of not being treated. No profile is a guaranteed enrollee, none a guaranteed non-enrollee. If some profile is always treated, the strict inequality fails on the right; if always untreated, on the left. Either way that region of covariate space has no usable comparison and must be excluded — which silently changes *whose* effect you are estimating.

Overlap is the assumption that does the real work in practice, and unlike CIA it is *partly checkable*: you can look at the data and see whether treated and untreated units actually occupy the same regions of $\mathbf{X}$. For Maya, suppose every applicant with a credit score above 780 enrolled in the program (the very savviest all take the free course), and no applicant below 580 ever did. Then there are no untreated high-score units to serve as counterfactuals for treated high-score units, and no treated low-score units at all. Those tails violate overlap. Maya can only learn the program's effect in the **region of common support** — the band of credit scores where both enrollees and non-enrollees exist. CIA plus overlap together are called **strong ignorability** (the Rosenbaum–Rubin 1983 term); they are the joint license to compare like with like.

---

## 3.2.3 Exact matching and the curse of dimensionality

So the recipe is clear: for each treated applicant, find untreated applicants with the *same* $\mathbf{X}$, use their outcomes as the counterfactual, and average. When $\mathbf{X}$ is a single binary variable — say, "has a prior account, yes/no" — this is trivial. You have two cells. Match treated to untreated within each, take the difference, average over the two treated subgroups. This is **exact matching**, and within each cell it is unimpeachable.

Now add realism. Maya's confounders are credit score, income, age, debt-to-income ratio, employment status, prior banking relationship, ZIP-code median income. Suppose, generously, you coarsen each into just a handful of bins: credit into 5 buckets, income into 5, age into 4, debt-to-income into 4, employment into 3, prior-relationship into 2, ZIP into 5. The number of distinct cells is

$$5 \times 5 \times 4 \times 4 \times 3 \times 2 \times 5 = 12{,}000.$$

With, say, 4,000 applicants spread across 12,000 cells, the *average* cell holds well under one person. Most cells are empty; most of the occupied ones contain a lone treated applicant with no untreated twin, or vice versa. Exact matching breaks down completely — not because the idea is wrong, but because in high dimensions, *nobody has an exact twin.* This is the **curse of dimensionality**: the number of cells grows multiplicatively in the number of covariates, so the data thin out exponentially fast and the "find someone with the same $\mathbf{X}$" step finds no one.

You might try to rescue it by coarsening more — fewer, wider bins — but then "the same $\mathbf{X}$" means "vaguely similar $\mathbf{X}$," CIA is only approximately satisfied within each fat cell, and a different bias (from comparing not-quite-alike units) creeps back in. You are trapped between *empty cells* (too fine) and *unlike comparisons* (too coarse). This tension is exactly what the propensity score was invented to escape.

---

## 3.2.4 The propensity score and the Rosenbaum–Rubin reduction

Here is the trick, and it is genuinely surprising the first time you see it. Define the **propensity score** as the probability of treatment given covariates:

$$e(\mathbf{X}_i) = \Pr(D_i = 1 \mid \mathbf{X}_i).$$

It is a single number between 0 and 1 — for Maya, "given everything I know about this applicant, how likely were they to enroll?" Rosenbaum and Rubin (1983) proved a remarkable fact: **if CIA holds given the full vector $\mathbf{X}$, then it also holds given the single scalar $e(\mathbf{X})$**:

$$\{Y_i(1), Y_i(0)\} \perp\!\!\!\perp D_i \mid \mathbf{X}_i \quad \Longrightarrow \quad \{Y_i(1), Y_i(0)\} \perp\!\!\!\perp D_i \mid e(\mathbf{X}_i).$$

You do not need to match on all seven covariates. You only need to match on the *one number* that summarizes them for the purpose of predicting treatment. A 7-dimensional matching problem collapses to a 1-dimensional one. The curse of dimensionality is lifted.

Why does this work? The intuition is that the propensity score is a **balancing score**: among units with the *same* propensity score, the distribution of covariates is the *same* for treated and untreated. Formally, Rosenbaum and Rubin first showed $\mathbf{X}_i \perp\!\!\!\perp D_i \mid e(\mathbf{X}_i)$ — that conditioning on the score balances the covariates. Here is the one-line argument. We want to show that, given $e(\mathbf{X}) = e$, knowing $D$ tells you nothing about $\mathbf{X}$. It suffices to show the treatment probability does not depend on $\mathbf{X}$ once we fix the score:

$$\Pr(D_i = 1 \mid \mathbf{X}_i, e(\mathbf{X}_i)) = \Pr(D_i = 1 \mid \mathbf{X}_i) = e(\mathbf{X}_i),$$

since $e(\mathbf{X}_i)$ is a function of $\mathbf{X}_i$ and adds nothing; while

$$\Pr(D_i = 1 \mid e(\mathbf{X}_i)) = \mathbb{E}[\,\Pr(D_i=1\mid \mathbf{X}_i) \mid e(\mathbf{X}_i)\,] = \mathbb{E}[\,e(\mathbf{X}_i) \mid e(\mathbf{X}_i)\,] = e(\mathbf{X}_i).$$

The two are equal — both are $e(\mathbf{X}_i)$ — which means that conditional on the score, the probability of treatment does *not* further depend on $\mathbf{X}$. So $\mathbf{X}$ and $D$ are independent given $e(\mathbf{X})$: the covariates are balanced at each value of the score. And once the covariates are balanced, the part of CIA that says "potential outcomes don't differ by treatment status given the covariates" transfers automatically to the score, because potential outcomes only relate to $D$ *through* $\mathbf{X}$ in the first place. Two treated and untreated applicants with the same enrollment probability $e$ look the same on $\mathbf{X}$ on average — so comparing them is, under CIA, comparing like with like.

How do you get $e(\mathbf{X})$ in practice? You estimate it. The treatment indicator $D_i$ is binary, so the natural model is a **logistic regression** of $D$ on the covariates,

$$\hat e(\mathbf{X}_i) = \frac{1}{1 + \exp\!\big(-(\hat\gamma_0 + \hat\gamma_1 X_{i1} + \dots + \hat\gamma_K X_{iK})\big)},$$

fit by maximum likelihood (any classifier that outputs calibrated probabilities works — logit is the convention because it is simple, transparent, and its coefficients are interpretable as log-odds of enrolling). Two disciplines govern this fit, and they are different from everything you learned about fitting models in Week 2. First, **the propensity model is judged by the balance it produces, not by how well it predicts $D$.** You are not trying to forecast enrollment accurately; a model that predicts $D$ near-perfectly is actually a *disaster*, because perfect prediction means $\hat e$ is near 0 or 1 for everyone — an overlap catastrophe with no comparable units left. You want a model just rich enough to soak up the covariate imbalance, and you confirm it did so with the balance table of Section 3.2.7, iterating on the *specification* (adding squares, interactions) until balance is achieved — not until pseudo-$R^2$ is high. Second, **the outcome $Y$ never appears in this regression.** The score is a function of $D$ and $\mathbf{X}$ alone. That is what makes the whole procedure honest, and we return to it forcefully in Section 3.2.7.

A subtlety worth flagging now, because Chapter 3.3 will exploit it: in real data you do not *know* $e(\mathbf{X})$; you estimate it, $\hat e(\mathbf{X})$, usually with the logistic regression just described. Two things follow. First, the balancing property is a property of the *true* score, so after matching on $\hat e$ you must *check* that covariates actually balanced — the estimated score is only useful insofar as it produced balance (Section 3.2.7). Second, the score is the central object Chapter 3.3 will *reweight* by, rather than match on, to build entropy-balancing, IPW, and doubly-robust estimators. Matching is the most intuitive use of the score; it is not the only one. Estimate it well here and you have built the foundation for both.

---

## 3.2.5 Nearest-neighbor and caliper matching

Even on a single score, two treated and untreated applicants almost never have *identically* equal $\hat e$ — it is a continuous number. So "exact match on the score" becomes "**nearest-neighbor match**": for each treated unit, find the untreated unit whose estimated propensity score is *closest*, and use its outcome as the counterfactual. This is the workhorse, and it comes with a handful of design choices that each trade **bias against variance**.

**How many neighbors?** The simplest is **1:1 matching** — one nearest control per treated unit. Using more neighbors (1:$k$) averages several controls per treated unit. More neighbors means *lower variance* (you are averaging over more control outcomes, so noise cancels) but potentially *higher bias* (the 2nd, 3rd, … nearest neighbors are by definition worse matches, with more dissimilar scores). This is the bias–variance trade-off in its purest form: tighter matches are less biased but noisier; looser, more-numerous matches are smoother but more contaminated.

**With or without replacement?** **Without replacement**, each control can be used as a match only once; once "spent," it is removed from the pool. **With replacement**, a single excellent control can serve as the counterfactual for many treated units. With replacement gives *better matches* (you always get the genuinely closest control, never a forced second-best because the best was taken) — lower bias — but *higher variance* and a subtlety in inference: because the same control's outcome is reused, the matched observations are not independent, and naive standard errors are wrong. Without replacement is simpler but its quality degrades as the control pool gets used up, and the result can even depend on the *order* in which you process treated units.

**The caliper.** What if a treated applicant's *nearest* neighbor is still far away on the score — say a treated unit with $\hat e = 0.95$ whose closest control sits at $\hat e = 0.60$? Forcing that match manufactures a bad comparison and reintroduces bias; it is a quiet overlap violation at the level of a single unit. The fix is a **caliper**: a maximum allowed distance. If the nearest neighbor lies outside the caliper, the treated unit is *dropped* rather than badly matched. A common rule of thumb (Austin 2011) sets the caliper at $0.2$ times the standard deviation of the estimated score (or of its logit). The caliper enforces common support *unit by unit*: it is overlap as a runtime check.

Every one of these knobs is a point on the same trade-off curve. There is no universally correct setting. The discipline is to (a) make a defensible choice, (b) check that it produced **balance** (next), and (c) show your estimate is not fragile to flipping the knobs — the robustness habit from the Week 2 style guide. Matching is honest only when you report how much the answer moves as you change the recipe.

---

## 3.2.6 The PSM workflow on Maya's program — with numbers

Let us run the whole thing on a concrete (simulated, so we know the truth) version of Maya's question, then generalize the steps. We build 4,000 applicants. Three observed confounders drive *both* enrollment and approval: a standardized **creditworthiness** index, **income**, and **age**. Savvier (higher-credit, higher-income) applicants are more likely to enroll *and* more likely to be approved regardless — that is the selection. We *engineer* a true program effect so we can grade ourselves. The full data-generating process and matching code is the seed for `nb3.2`; here is the part that matters.

```python
import numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from scipy.spatial import cKDTree

rng = np.random.default_rng(20260528)
N = 4000
credit = rng.normal(0, 1, N)        # standardized creditworthiness
income = rng.normal(0, 1, N)
age    = rng.normal(0, 1, N)

# Selection: savvier applicants enroll more (this is what creates the bias).
idx = -0.2 + 0.9*credit + 0.6*income + 0.3*age
D   = (rng.uniform(size=N) < 1/(1 + np.exp(-idx))).astype(int)

# Potential outcomes on an approval index; treatment shifts the index by tau.
tau    = 0.8
y0_idx = -0.1 + 0.3*credit + 0.5*income + 0.2*age + rng.normal(0, 0.3, N)
appr0  = (y0_idx > 0).astype(int)            # Y(0): approved if untreated
appr1  = (y0_idx + tau > 0).astype(int)      # Y(1): approved if treated
Y      = np.where(D == 1, appr1, appr0)      # we observe only one per person

att_true = (appr1[D == 1] - appr0[D == 1]).mean()   # truth, known by construction
naive    = Y[D == 1].mean() - Y[D == 0].mean()       # the contaminated comparison
```

Running it, the **true ATT** is $0.322$: the program raises the approval rate of enrollees by about 32 percentage points. The **naive difference** in approval rates between enrollees and non-enrollees is $0.629$ — nearly *double* the truth. The gap, $0.629 - 0.322 = 0.307$, is the selection bias from the chapter opening, made of flesh: enrollees would have been approved at much higher rates *even without the course*, because they are the higher-credit, higher-income applicants. The naive number is a textbook lie.

Now the **PSM workflow**, four steps:

```python
# Step 1: estimate the propensity score e(X) = P(D=1 | X) by logistic regression.
X  = np.column_stack([credit, income, age])
ps = LogisticRegression().fit(X, D).predict_proba(X)[:, 1]
df = pd.DataFrame({"D": D, "Y": Y, "credit": credit, "income": income,
                   "age": age, "ps": ps})
treated, control = df[df.D == 1].copy(), df[df.D == 0].copy()

# Step 2: 1:1 nearest-neighbor match on the score, WITH replacement, with a caliper.
caliper = 0.2 * ps.std()
tree = cKDTree(control[["ps"]].values)
dist, j = tree.query(treated[["ps"]].values, k=1)   # nearest control per treated
keep = dist <= caliper                               # drop unmatchable treated units
mt = treated[keep]
mc = control.iloc[j[keep]]

# Step 3: the ATT estimate is the mean within-pair outcome difference.
att_psm = (mt["Y"].values - mc["Y"].values).mean()
```

This recovers an ATT estimate of about $0.31$ — essentially the true $0.322$, and a world away from the naive $0.629$. Matching on the single number $\hat e(\mathbf{X})$ stripped out the selection bias, because it compared each enrollee to a non-enrollee who was *just as likely to have enrolled* — same credit, same income, same age, on average — and so just as likely to have been approved anyway. The leftover difference is the program. **Step 4 is not optional and is the subject of the next section: check that the matching actually balanced the covariates.** Notice what we did *not* do: at no point did the outcome $Y$ enter the matching. The score was built from $\mathbf{X}$ and $D$ only. That separation is deliberate, and it is the heart of the next section.

The reason ATT is the natural target should now be visible in the code: we matched *every treated unit to a control*, reusing controls freely with replacement. We never had to find a treated twin for each control. ATT only asks "what would the *enrollees* have looked like without the program," so it only needs counterfactuals for the treated — and there are usually plenty of untreated units to draw from. Estimating the full ATE would additionally require imputing $Y(1)$ for the *untreated*, demanding overlap in the other direction too. Matching's asymmetry makes ATT the path of least resistance.

---

## 3.2.7 Balance diagnostics — and why you never look at the outcome

You have a propensity-score model and a set of matches. Before you believe the $0.31$, you must answer one question: **did the matching make the treated and control groups actually comparable on $\mathbf{X}$?** That is what the whole exercise was for. A propensity-score model can be badly specified, the caliper too loose, the overlap too thin — and any of these leaves residual imbalance that re-confounds the estimate. So you *audit the balance*.

The standard tool is the **standardized mean difference** (SMD), computed for each covariate, before and after matching. For covariate $X_j$, with treated and control means $\bar X_{j,1}, \bar X_{j,0}$ and (pooled) standard deviation $s_j$,

$$\text{SMD}_j = \frac{\bar X_{j,1} - \bar X_{j,0}}{s_j}.$$

It is the gap in means measured in standard-deviation units — scale-free, so a credit score and an income in dollars are on the same footing. The convention (Austin 2011, Stuart 2010) is that $|\text{SMD}_j| < 0.1$ is acceptable balance; larger means the groups still differ on $X_j$ and the comparison is suspect. Crucially, you do *not* use a t-test for balance: a t-test conflates the size of the imbalance with the sample size, and matching changes the sample size, so a "significant" imbalance can shrink to "insignificant" just by dropping units, with no real improvement. The SMD measures the imbalance itself, not whether it clears a noise threshold.

Here are Maya's SMDs, before and after matching, from the same run:

| Covariate | SMD before | SMD after |
|---|---:|---:|
| creditworthiness | $+0.79$ | $-0.03$ |
| income | $+0.45$ | $+0.02$ |
| age | $+0.27$ | $+0.04$ |
| propensity score $\hat e$ | $+1.02$ | $\approx 0.00$ |

Before matching, the groups are wildly different — enrollees are $0.79$ SDs more creditworthy, and a full $1.02$ SDs higher on the propensity score. That imbalance *is* the selection bias in covariate form. After 1:1 caliper matching, every SMD drops below the $0.1$ threshold: the matched enrollees and non-enrollees are now genuine look-alikes on all three confounders. *This table is the evidence that the $0.31$ deserves to be believed.* A balance table like this — not the regression output — is what a referee reads first in a matching paper.

Now the rule that trips up everyone the first time: **you check balance, never the outcome.** You tune your propensity model, your caliper, your number of neighbors, looking *only* at how well $\mathbf{X}$ balances — and you keep the outcome $Y$ hidden from yourself until the design is locked. Why? Because the entire credibility of selection-on-observables rests on the design being chosen *independently of the answer it produces*. If you fiddle with the matching recipe while watching the treatment-effect estimate, you are — consciously or not — selecting the specification that gives the effect you like. That is the multiple-testing / specification-search pathology from Chapter 1.5, now aimed straight at your causal conclusion. Matching's great procedural virtue is precisely that it *forces* this separation: the matching stage uses $D$ and $\mathbf{X}$ only, the outcome enters *after* the design is frozen. Treat that firewall as sacred. Balance is the thing you optimize; the effect is the thing you report once, at the end.

---

## 3.2.8 When it fails: CIA is untestable, and matching is still selection-on-observables

Now the part the brochures leave out. Everything above is conditional on CIA holding — on $\mathbf{X}$ containing *all* the confounders. And here is the brutal fact: **CIA is fundamentally untestable.** You cannot check it in the data, ever. The reason is the fundamental problem of causal inference itself. CIA is a statement about the unobserved potential outcome $Y_i(0)$ of the *treated* — that it matches the untreated within cells of $\mathbf{X}$. But $Y_i(0)$ for a treated unit is exactly the thing we never see. There is no statistic you can compute that confirms two groups have the same $Y(0)$ distribution conditional on $\mathbf{X}$, because half of that distribution is missing by construction. Beautiful balance on $\mathbf{X}$ does *not* imply balance on the *unobserved* confounders, and unobserved confounders are, by definition, not in your balance table.

This is where the warning from page one comes due. Suppose Maya's data lack a key driver: applicant **motivation** — the same drive to improve one's finances that makes someone both *seek out the free course* and *clean up their application in other ways the lender rewards*. Motivation affects approval ($Y$) and affects enrollment ($D$), and it is **not in $\mathbf{X}$**. Then CIA fails. Run the propensity score on credit, income, and age; match beautifully; produce a balance table with every SMD under $0.05$ — and your estimate is *still biased*, because the matched enrollees are more motivated than their matched non-enrollee twins, and motivation independently raises approval. Your gorgeous balance table is silent about it. Matching balanced what you measured and is helpless about what you didn't.

Map this onto Week 2 and the equivalence becomes exact. **A confounder omitted from $\mathbf{X}$ is precisely an omitted variable**, and the bias it creates is the omitted-variable bias of Chapter 2.5 — the product of the omitted variable's effect on the outcome ($\beta_2$) and its association with treatment ($\delta_1$). Motivation has $\beta_2 > 0$ (raises approval) and is positively associated with enrolling ($\delta_1 > 0$), so by the two-sign rule the program effect is biased *upward*: matching on observables alone would *overstate* the course. CIA is just the potential-outcomes name for "no omitted confounders," i.e., for the zero-conditional-mean condition $\mathbb{E}[\varepsilon \mid D, \mathbf{X}] = 0$ that Chapter 2.2 demanded. **Matching does not buy you anything that controlling-for-$\mathbf{X}$-in-a-regression does not also buy.** Both are selection-on-observables; both die the same death from the same omitted confounder.

So what *does* matching give you over regression with controls, if the identifying assumption is identical? Three honest, non-magical advantages. **(1) It is nonparametric in the outcome.** Regression assumes a functional form linking $\mathbf{X}$ to $Y$ (usually linear); matching makes no such assumption — it never models the outcome at all, so it cannot be fooled by getting that shape wrong (recall the functional-form misspecification of Chapter 2.5). **(2) It enforces overlap explicitly.** A regression will happily extrapolate a fitted line into regions of $\mathbf{X}$ where there are no controls at all, silently inventing counterfactuals; matching with a caliper *refuses* to compare units that have no real neighbor, making the common-support problem visible instead of papering over it. **(3) It separates design from outcome.** As Section 3.2.7 stressed, the matching stage never touches $Y$, which structurally prevents specification-searching on the answer. These are real and valuable. But notice that not one of them weakens the CIA requirement. Matching is a *better-disciplined* way to do selection-on-observables, not an *escape* from it.

When *should* you reach for it, then? When you have a credible argument — from institutional knowledge, not hope — that the variables driving selection are observed and measured. Maya's case is honest only if she can argue that credit, income, age, and a handful of other recorded fields really do capture why people enroll, with no large unmeasured driver like motivation. Often she cannot make that argument cleanly, and then the right move is not a fancier matching estimator but a *different research design* — an instrument for enrollment, a natural experiment, a discontinuity in eligibility — the design-based tools of Chapter 3.4 and Week 4 that manufacture exogenous variation rather than assuming it away. The most sophisticated thing you can say about matching is knowing when *not* to trust it. And the most useful sensitivity question to carry forward (Rosenbaum's: *how strong would an unobserved confounder have to be to overturn my result?*) is the subject of more advanced reading; for now, internalize that the answer to "is CIA true?" comes from outside the dataset, never from inside it.

---

## 3.2.9 What you can carry forward

Strip the chapter to its load-bearing sentences. Under the **Conditional Independence Assumption** $\{Y_i(1),Y_i(0)\}\perp\!\!\!\perp D_i \mid \mathbf{X}_i$ and **overlap** $0 < e(\mathbf{X}_i) < 1$, comparing treated and untreated units with the same $\mathbf{X}$ recovers a causal effect, because the selection-bias term in $Y(0)$ vanishes within each covariate cell. Exact matching does this directly but dies of the **curse of dimensionality**. The **propensity score** $e(\mathbf{X}) = \Pr(D=1\mid\mathbf{X})$ rescues it: Rosenbaum–Rubin proved that conditioning on the scalar $e(\mathbf{X})$ suffices, because the score is a balancing score. **Nearest-neighbor and caliper matching** implement the comparison, with choices (neighbors, replacement, caliper) that all trade bias against variance. You validate the result with **balance diagnostics** — standardized mean differences before and after, never t-tests — and you check *balance, not the outcome*, keeping a firewall between design and answer. And you remember, always, that **CIA is untestable and matching is still selection-on-observables**: an omitted confounder is the omitted-variable bias of Week 2 wearing a potential-outcomes costume, and no balance table can see it.

Chapter 3.3 keeps the propensity score you just learned to estimate but stops *matching* on it. Instead it *reweights* by it — **inverse-probability weighting**, **entropy balancing**, and the **doubly-robust / AIPW** estimators that combine a propensity model with an outcome model so that getting *either one* right saves you. The score you built here is the raw material; next chapter turns it into a weight.

---

## Your Turn

Open **`nb3.2`** (`notebooks/week-03/nb3.2-psm-balance-diagnostics.ipynb`), the propensity-score-matching lab. You will (1) build Maya's program-enrollment data from a known DGP, compute the true ATT and the contaminated naive difference, and confirm the selection bias equals their gap; (2) estimate the propensity score by logistic regression, then implement **1:1 nearest-neighbor caliper matching** (with replacement) and recover the ATT; (3) produce a **balance table and a Love plot** of standardized mean differences before vs. after matching, and verify every covariate lands under $0.1$; (4) stress the design — tighten and loosen the caliper, switch matching *without* replacement, add a *useless* covariate and a *mismeasured* confounder — and watch how the estimate and the balance respond; and (5) inject an **unobserved confounder** (motivation) the score cannot see, re-run the whole pipeline, and watch the perfectly-balanced matching deliver a confidently *wrong* answer — CIA failing in front of you.

**Check questions.**

1. Maya matches enrollees to non-enrollees on credit, income, and age, and her post-matching balance table shows every standardized mean difference below $0.04$. Her teammate says, "Balance this good proves the matching removed the selection bias — the estimate is causal." (a) What exactly *has* the balance table established? (b) Name the one thing it has *not* established, and explain why no balance table ever could. (c) Connect your answer to the omitted-variable-bias formula $\beta_2\delta_1$ from Chapter 2.5.

2. A treated applicant has estimated propensity score $\hat e = 0.97$ (they were nearly certain to enroll). The closest available control sits at $\hat e = 0.71$. (a) What does a *caliper* of $0.2$ score-SDs do with this treated unit, assuming the score SD is about $0.25$? (b) Which assumption from this chapter is the caliper protecting, and what bias would you risk by forcing the match instead? (c) If many treated units look like this one, what does that tell you about the design, and what should you report?

3. Explain in two or three sentences why you tune the propensity-score model and matching recipe by looking at *covariate balance* rather than at the estimated treatment effect — and what specific Chapter 1.5 pathology you would be courting if you optimized the recipe while watching the effect.
