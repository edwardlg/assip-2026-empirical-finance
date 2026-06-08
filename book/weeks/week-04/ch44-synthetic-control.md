# Ch 4.4 — Synthetic Control & Synthetic DiD

Chapter 4.1 gave you difference-in-differences, and it gave you a warning. DiD compares the *change* in some treated group to the *change* in a control group, and it works — it actually identifies the causal effect of a policy — only if the two groups would have moved in parallel had the policy never happened. That **parallel-trends assumption** is the entire engine. When you have dozens of treated units and dozens of controls, and when their pre-treatment trends lie convincingly on top of one another, parallel trends is a bet you can defend: you point at the pre-period, show the lines tracking, and argue that absent the policy they would have kept tracking. The event-study plot from §4.1 is exactly that argument made visible.

But sometimes the world hands you *one* treated unit. A single state passes a first-in-the-nation law. A single firm gets hit by a scandal. A single country adopts the euro, or builds a wall, or unifies after a partition. And now the comfortable machinery of DiD starts to creak. Which control do you use? If you pick one similar state, your estimate lives or dies on that one arbitrary choice, and a critic will always find a different "similar" state that gives the opposite answer. If you average all the other states into a single control group, you are implicitly weighting them equally, and there is no reason equal weights should reproduce *your* treated unit's trajectory. The pre-trends almost never line up, because no naturally occurring group is a good twin for one specific unit. Parallel trends becomes a wish rather than a defensible claim.

This chapter is about what to do when one treated unit is all you have. The central idea, due to **Abadie and Gardeazabal (2003)** and developed in full by **Abadie, Diamond and Hainmueller (2010)**, is disarmingly simple to state and surprisingly deep once you push on it: instead of *picking* a control or *averaging* controls equally, you *build* one.[^ag][^adh] You take a pool of untreated units — the **donor pool** — and find the weighted average of them that best reproduces your treated unit's behavior *before* the treatment. That weighted average is the **synthetic control**: a synthetic version of the treated unit, assembled from real untreated units, that walks in lockstep with the real thing through the entire pre-period. Then you let the policy hit, and you watch the real unit and its synthetic twin diverge. The gap between them, after treatment, is your estimated effect.

[^ag]: Abadie, A., & Gardeazabal, J. (2003). The Economic Costs of Conflict: A Case Study of the Basque Country. *American Economic Review*, 93(1), 113–132.

[^adh]: Abadie, A., Diamond, A., & Hainmueller, J. (2010). Synthetic Control Methods for Comparative Case Studies: Estimating the Effect of California's Tobacco Control Program. *Journal of the American Statistical Association*, 105(490), 493–505.

Then we will reveal the trick's limits — convexity, the donor pool, anticipation, interference — and the honest way to do inference when your effective sample size is *one*: not a t-statistic, but a **placebo permutation test**. Finally, **synthetic DiD (Arkhangelsky, Athey, Hirshberg, Imbens and Wager, 2021)** stitches synthetic control and DiD together, keeping the best of both.[^sdid]

[^sdid]: Arkhangelsky, D., Athey, S., Hirshberg, D. A., Imbens, G. W., & Wager, S. (2021). Synthetic Difference-in-Differences. *American Economic Review*, 111(12), 4088–4118. Throughout, Priya is our guide. From the Week 4 opening narrative, she is chasing one event: a single state — call it the treated state — that, in 2018, passed a first-in-the-nation **climate-risk disclosure mandate** forcing home insurers to publish wildfire- and flood-exposure pricing. Did the mandate change average homeowner premiums? One treated state. No clean twin. This is the problem synthetic control was built for.

---

## 1. The result in one plain sentence

> **Synthetic control, stated plainly.** When you have one treated unit, build a fake "control" unit as a weighted average of the units that were *not* treated, choosing the weights so the fake unit matches the treated unit's pre-treatment outcomes; then read the treatment effect off how far the real unit drifts from its fake twin after treatment.

The whole method is in the phrase *weighted average chosen to match the pre-period*. You are not assuming a control group is comparable; you are *constructing* one that demonstrably tracks the treated unit before anything happened, and then arguing — exactly as in DiD, but with a far better-matched comparison — that it would have kept tracking absent the policy. Parallel trends does not disappear. It is *engineered*: the weights are picked precisely so that the pre-trends are parallel, indeed nearly identical, by construction. The leap of faith shrinks from "these two groups would have moved together" to "this carefully matched composite would have kept moving together for a few more years."

Everything technical below is an elaboration of that sentence. The weights are the heart of it: how they are chosen, why they are constrained to be non-negative and sum to one, and what that constraint buys you. The donor pool is the raw material. The placebo test is how you decide whether the post-treatment gap you see is real or just the kind of gap you would see for *any* unit by chance. And synthetic DiD is what you reach for when even the engineered match is not quite good enough.

---

## 2. The setup, in Week 4 notation

Index units (states) by $i$ and time (years) by $t$, exactly as in the DiD chapter. There are $J+1$ units in total. Unit $i=1$ is the treated state — the one that passed the disclosure mandate. The other $J$ units, $i = 2, \dots, J+1$, are the **donor pool**: untreated states that never adopted such a mandate over the sample. Treatment turns on at time $T_0+1$: the pre-treatment period is $t = 1, \dots, T_0$ and the post-treatment period is $t = T_0+1, \dots, T$. For Priya, the outcome $Y_{it}$ is the average homeowner insurance premium in state $i$, year $t$; $T_0$ is 2017 (the last pre-mandate year); the mandate takes effect in 2018.

We work in potential outcomes, the language of Chapter 3.1. Let $Y_{it}^{N}$ be the premium state $i$ *would* show in year $t$ with **no** treatment, and $Y_{it}^{I}$ the premium *with* the intervention. We observe $Y_{1t}^{I}$ for the treated state after $T_0$ and $Y_{it}^{N}$ for everyone else throughout. The causal effect on the treated state in a post-period year $t$ is

$$
\tau_{1t} = Y_{1t}^{I} - Y_{1t}^{N}, \qquad t > T_0.
$$

The first term is observed — it is just the treated state's actual premium. The second term, $Y_{1t}^{N}$, is the **counterfactual**: what the treated state's premium *would have been* in 2019, 2020, 2021 had the mandate never passed. It is unobservable, the missing half of the comparison. Every causal method is a strategy for filling in a counterfactual; DiD fills it in by assuming parallel trends with a control group, and synthetic control fills it in with a tailor-made composite. The estimate is

$$
\hat{\tau}_{1t} = Y_{1t} - \hat{Y}_{1t}^{N}, \qquad \hat{Y}_{1t}^{N} = \sum_{j=2}^{J+1} w_j\, Y_{jt},
$$

where the $w_j$ are the synthetic-control weights on the donor states. The synthetic counterfactual $\hat{Y}_{1t}^{N}$ is a weighted average of the donors' *observed, untreated* premiums. Pick the weights well in the pre-period and you have a credible stand-in for the treated state in the post-period. That is the whole estimator. The art is entirely in choosing $\mathbf{w} = (w_2, \dots, w_{J+1})$.

---

## 3. Choosing the weights: matching the pre-period

Here is the mechanical core. We want the synthetic control to reproduce the treated state before treatment — not just its average premium, but the whole pre-period path, and ideally a set of **predictors** that drive premiums (population density in fire zones, median home value, reinsurance costs, the share of coastal property). Collect for the treated state a column vector $\mathbf{X}_1$ of $k$ such pre-treatment characteristics — these can include the premium in each pre-period year and the predictor averages — and collect the same characteristics for each donor into the columns of a matrix $\mathbf{X}_0$ (size $k \times J$). We choose weights $\mathbf{w}$ to make the synthetic state's characteristics, $\mathbf{X}_0 \mathbf{w}$, as close as possible to the treated state's, $\mathbf{X}_1$:

$$
\mathbf{w}^{*} = \arg\min_{\mathbf{w}} \; (\mathbf{X}_1 - \mathbf{X}_0 \mathbf{w})' \, \mathbf{V} \, (\mathbf{X}_1 - \mathbf{X}_0 \mathbf{w})
\quad\text{subject to}\quad
w_j \ge 0 \;\; \text{for all } j, \;\; \sum_{j=2}^{J+1} w_j = 1.
$$

Read this slowly. The thing in parentheses, $\mathbf{X}_1 - \mathbf{X}_0\mathbf{w}$, is the vector of *mismatches*: for each characteristic, how far the synthetic state falls from the real treated state. We square those mismatches and add them up — that is what the quadratic form $(\cdot)'\mathbf{V}(\cdot)$ does — and we choose $\mathbf{w}$ to make the total as small as possible. The diagonal matrix $\mathbf{V}$ holds weights *on the characteristics*: it lets predictors that matter more for the outcome count more in the matching. (Choosing $\mathbf{V}$ well is its own small problem; in practice it is picked to minimize pre-treatment prediction error of the *outcome*, often by cross-validation, and the software does it for you. Do not let it distract you — the heart of the method is the $\mathbf{w}$.)

### The two constraints are the whole personality of the method

Notice the two restrictions hanging off the minimization. They look like fine print. They are the entire point.

**Non-negativity, $w_j \ge 0$.** No donor can enter with a negative weight. You cannot say "two parts California minus one part Florida." Every weight is zero or positive.

**Sum to one, $\sum_j w_j = 1$.** The weights are shares of a whole. Together with non-negativity, this means the synthetic control is a **convex combination** of the donors — a genuine weighted average, where the weights are like proportions of a portfolio that must add to 100%.

Why constrain things this way? Because a convex combination cannot **extrapolate**. The synthetic premium $\hat{Y}_{1t}^{N} = \sum_j w_j Y_{jt}$ is always boxed inside the range of the donor premiums: it can never be higher than the most expensive donor or lower than the cheapest. Contrast this with ordinary regression, which is exactly an *un*constrained linear combination — coefficients can be any sign, any size — and which routinely predicts outside the range of the data when you push it. If you regressed the treated state's pre-period premium on the donors' premiums with no constraints, you could fit the pre-period *perfectly* (with $J$ donors and $T_0$ periods, you have plenty of freedom) by using wild positive and negative coefficients that exploit accidental correlations. That perfect fit would be a fantasy: it interpolates the noise and then explodes out-of-sample in the post-period. The convexity constraint is a deliberate handcuff that says: *the synthetic control may only live inside the convex hull of the real donors.* You buy stability and honesty at the cost of fit. Sometimes you cannot match the treated unit well, and that is the constraint telling you the truth — that no combination of donors resembles your treated unit, and you should not pretend otherwise.

A second gift of convexity: **interpretability and sparsity.** The optimal weights are typically *sparse* — most donors get weight exactly zero, and a handful carry the synthetic control. Priya might find her synthetic state is 0.46 Oregon, 0.31 Colorado, 0.18 Arizona, 0.05 New Mexico, and zero on the other thirty donors. That is a sentence she can write in a paper and defend: "the treated state's premium path before the mandate is best reproduced by a blend of four western states with similar wildfire exposure." Try writing that sentence about a regression with forty nonzero coefficients of both signs.

Where does the sparsity come from? It is a feature of optimizing a convex objective over the **simplex** — the set of non-negative weights summing to one, whose corners are the individual donors and whose interior is every possible blend. Minimizing a sum of squares over that geometry tends to push the solution toward a low-dimensional face: you load up on the few donors that genuinely help close the mismatch and zero out the rest, the same way a constrained portfolio optimizer often concentrates in a few assets rather than spreading thinly across all of them. This is the deep reason synthetic control reads less like a regression and more like **matching** (Chapter 3.2): instead of estimating a coefficient for every donor, it *selects and weights a small comparison set*, and the selection is data-driven rather than imposed. The price, again, is honesty under duress — if no small blend can reproduce the treated unit, the optimizer cannot hide it behind a dense vector of offsetting weights.

### A worked number

Strip it to three pre-periods and three donors so you can see the gears. Suppose the treated state's pre-period premiums (in hundreds of dollars) are $\mathbf{X}_1 = (12, 13, 14)'$ for 2015, 2016, 2017. Three donors have pre-period premium vectors

$$
\mathbf{X}_0 = \begin{pmatrix} 10 & 16 & 11 \\ 11 & 17 & 12 \\ 12 & 18 & 13 \end{pmatrix},
$$

where column $j$ is donor $j$'s three premiums. With $\mathbf{V} = \mathbf{I}$ (treat all three years equally) and weights $\mathbf{w} = (w_2, w_3, w_4)$ summing to one and non-negative, try $\mathbf{w} = (0.5,\, 0.0,\, 0.5)$: the synthetic premiums are $0.5\cdot(10,11,12) + 0.5\cdot(11,12,13) = (10.5, 11.5, 12.5)$. The mismatch vector is $(12,13,14) - (10.5,11.5,12.5) = (1.5, 1.5, 1.5)$, sum of squares $= 6.75$. Now try $\mathbf{w}=(0,0,1)$: synthetic $=(11,12,13)$, mismatch $(1,1,1)$, sum of squares $3$. Better. The middle donor, with premiums $(16,17,18)$, is far above the treated state and gets driven to weight zero — including it would only push the synthetic average up and *away*. The optimizer keeps searching the simplex of valid weights for the lowest sum of squares; the convexity constraint keeps it from doing something absurd like $w=(−5, 0.1, 5.9)$ that might fit even better in-sample by exploiting the third donor's slope. That refusal is the feature.

### How this relates to DiD

Tie it back to §4.1 explicitly. **DiD is synthetic control with the weights frozen at equality.** When you run a 2×2 DiD against "the rest of the states," you are implicitly using $w_j = 1/J$ for every donor — an equal-weighted average control — and *hoping* that equal-weighted average happens to share the treated unit's trend. Synthetic control says: don't hope, *optimize*. Let the data choose the weights so the pre-trends actually coincide, and report the match so the reader can see it worked. Where DiD asserts parallel trends and tests it after the fact, synthetic control *targets* parallel pre-trends as the objective function. That is the sense in which this chapter relaxes Chapter 4.1: it earns the parallel-trends comparison instead of assuming it.

---

## 4. The donor pool, and the assumptions that protect it

The synthetic control is only as good as the units you let it draw from. Choosing the **donor pool** — which untreated units are eligible to receive weight — is a research-design decision as consequential as choosing an instrument in Chapter 3.4, and like that choice it must be defended, not made by reflex.

Three rules govern the pool, and each maps to an assumption that, if violated, quietly poisons the estimate.

**Donors must be untreated, and stay untreated, through the whole sample.** Obvious but easy to botch. If a "donor" state passed its own disclosure law in 2020, then after 2020 its premium path is contaminated by *its* treatment, and any weight on it corrupts your counterfactual. Drop it, or truncate the sample before its adoption. This is the synthetic-control version of the staggered-timing problem you will meet head-on in Chapter 4.2: contaminated controls are poison wherever they appear.

**Donors must be plausibly driven by the same forces as the treated unit — but not be the treated unit in disguise.** You want a pool of states whose premiums respond to the same national reinsurance market, the same climate trends, the same regulatory backdrop, so that a blend of them can mimic the treated state. But you must exclude units affected by *idiosyncratic shocks* the treated unit did not face. If one donor state had a once-in-a-century hurricane in 2019, its premium spiked for reasons unrelated to anything the treated state experienced, and letting it into the synthetic counterfactual injects that hurricane into your "what would have happened" line. Curate the pool the way you would curate a control group: similar enough to be relevant, clean enough to be valid.

**No-interference (SUTVA across units).** This is the subtle one. The synthetic counterfactual is the donors' *untreated* potential outcomes. That is only legitimate if the treatment of unit 1 did **not spill over** onto the donors. Suppose the treated state's disclosure mandate spooked the national reinsurance market and nudged premiums up *everywhere*, including in the donor states. Then the donors are no longer showing you $Y_{jt}^{N}$ (their no-treatment path); they are showing a path partly bent by the treated state's policy. Your synthetic control inherits that bend, the gap between real and synthetic shrinks, and you *understate* the true effect. This is the **no-interference** requirement — the same SUTVA stable-unit assumption from Chapter 3.1, now demanding that the donor pool be insulated from the treated unit's treatment. Priya defends it by arguing one state's disclosure rule is too small to move the national reinsurance market, and by checking that geographically distant donors (which should be most insulated) behave like the nearby ones.

**No-anticipation.** One more, shared with DiD. The pre-treatment fit assumes the treated unit's pre-period outcomes are genuinely untreated. If insurers, *anticipating* the 2018 mandate, started repricing in 2017 — the last "pre" year — then $Y_{1,2017}$ is already partly treated, the synthetic control is matched to a contaminated target, and the estimated effect is biased toward zero (because some of the effect has leaked backward into the matching window). The fix is the same as in event studies: define $T_0$ at the moment expectations could first have moved (often the announcement date, not the effective date), and inspect the last pre-periods for a suspicious early divergence. A clean synthetic-control study, like a clean event study, shows a flat gap right up to $T_0$ and a break only after.

State all of this in the CONVENTIONS §4 form. **Outcome:** average homeowner premium $Y_{it}$. **Treatment:** the 2018 climate-risk disclosure mandate, on for the treated state from 2018. **"Controls"/matching variables:** pre-period premiums plus predictors (fire-zone density, median home value, reinsurance cost index, coastal share), entered through $\mathbf{X}$. **Donor pool:** US states never adopting such a mandate in-sample, excluding any hit by idiosyncratic catastrophes. **Comparison unit:** the convex-weighted synthetic state. **Identifying assumption, one sentence:** absent the mandate, the treated state's premium would have continued to track its pre-period-matched synthetic control, which requires no anticipation, no interference from the policy onto donors, and a donor pool of clean, comparable, untreated states.

---

## 5. When it fails: reading the pre-period fit

The reveal-the-trick discipline demands we ask what failure *looks like*, and synthetic control is unusually honest here, because its central diagnostic is staring at you the whole time: the **pre-treatment fit**.

A good study shows the real unit and its synthetic twin lying on top of each other through the entire pre-period, then diverging after $T_0$. The pre-period fit is the credential. If the synthetic control cannot reproduce the treated unit *before* treatment — when there is no treatment effect to obscure the comparison — then it has no business claiming to reproduce it *after*. A large pre-period gap is the method confessing that no convex combination of your donors resembles your treated unit, and the convexity constraint will not let it lie about that. This is exactly why convexity matters: an unconstrained regression would paper over the failure with a slick in-sample fit; the constrained optimizer leaves the gap visible.

Quantify the fit with the **root mean squared prediction error** over the pre-period:

$$
\text{RMSPE}_{\text{pre}} = \sqrt{ \frac{1}{T_0} \sum_{t=1}^{T_0} \big( Y_{1t} - \hat{Y}_{1t}^{N} \big)^2 }.
$$

A small pre-period RMSPE relative to the scale of the outcome means the synthetic control tracks well; a large one is a red flag that no honest comparison exists. Three failure modes to watch for. First, **bad fit**: large pre-RMSPE, no credible counterfactual — the honest move is to report it and abandon the design, not to crank the predictors until something fits. Second, **interpolation bias**: a treated unit at the *edge* of the donor distribution (the highest-premium state, say) cannot be matched by a convex average of donors all below it — the constraint forbids reaching past the most extreme donor, so the synthetic systematically falls short. Third, **the short pre-period trap**: with only a few pre-periods, you can match them by luck, the way an unconstrained regression overfits; a convincing study has a *long* pre-period so that tracking through it is genuinely hard to fake. The longer the pre-period the synthetic control survives, the more the post-period divergence deserves to be read as causal.

---

## 6. Inference when your sample size is one: placebo tests

Now the hardest and most distinctive part. You have a treated unit, a synthetic twin, and a post-treatment gap of, say, $+\$140$ in average premium. Is that gap *real* — a genuine effect of the mandate — or is it the kind of gap any unit might show against its synthetic control just from noise and imperfect fit? In standard regression you would compute a standard error and a t-statistic. But here the effective number of treated units is **one**. There is no cross-sectional variation in treatment to power a conventional standard error; the asymptotics that justify t-tests (Chapter 2.4) simply do not apply when $N_{\text{treated}} = 1$. Reporting a t-statistic here would be false precision dressed up as rigor.

Abadie, Diamond and Hainmueller (2010) supply the honest alternative, and it is a beautiful piece of reasoning: a **placebo permutation test**, in the spirit of the randomization inference you have met before. The logic is this. If the mandate truly did nothing, then the treated state is not special — its post-treatment gap should look like the gap you would get by running the *exact same procedure* on a state that was *not* treated. So run the procedure on every donor as if it were the treated one.

Concretely: for each donor state $j$, pretend $j$ is the treated unit, build a synthetic control for $j$ from the *other* donors (and the real treated unit is dropped or, more cleanly, also excluded), and compute $j$'s post-treatment gap path. This gives you $J$ **placebo gaps**, one per donor — a distribution of "effects" for units we know were never treated. That distribution is your null: it is what gaps look like when nothing happened, including all the noise and fit imperfection the method generates. The real treated state's effect is **credible only if its gap is an outlier** relative to this placebo distribution — only if it lies out past where almost all the fake-treated donors landed.

### RMSPE ratios, the right yardstick

There is a wrinkle, and fixing it gives the workhorse statistic. Some donors fit their synthetic controls badly *in the pre-period* — for them, a big post-period gap means nothing, because they were already off-track before any pretend-treatment. Comparing raw post-period gaps would let those badly-fit donors masquerade as large "effects." The fix is to scale each unit's post-period gap by its *own* pre-period fit. Define the **post/pre RMSPE ratio**:

$$
r_i = \frac{\text{RMSPE}_{\text{post},\,i}}{\text{RMSPE}_{\text{pre},\,i}}
= \frac{\sqrt{\tfrac{1}{T-T_0}\sum_{t>T_0}(Y_{it}-\hat{Y}_{it}^{N})^2}}{\sqrt{\tfrac{1}{T_0}\sum_{t\le T_0}(Y_{it}-\hat{Y}_{it}^{N})^2}}.
$$

A large $r_i$ means the unit fit *well* before treatment (small denominator) and diverged *sharply* after (large numerator) — exactly the signature of a real effect, and not contaminated by units that were never matched well to begin with. Compute $r_1$ for the real treated state and $r_j$ for every placebo donor. The **permutation $p$-value** is the fraction of all $J+1$ units whose ratio is at least as large as the treated unit's:

$$
p = \frac{\#\{\, i : r_i \ge r_1 \,\}}{J+1}.
$$

If the treated state has the single largest ratio out of, say, 35 units, then $p = 1/35 \approx 0.029$: a gap this extreme, properly scaled, would arise for a randomly chosen unit only about 3% of the time. That is your inferential statement, and notice exactly what kind of statement it is. It is **small-sample and permutation-based**: there is no appeal to large-$N$ asymptotics, no assumption of normal errors, no clustered standard error. It is the honest probability that the treated unit's ratio is special given the reference set of placebos. With only 20 donors the *smallest possible* $p$-value is $1/21 \approx 0.048$ — you literally cannot get below 5% — which is why a respectable synthetic-control study wants a reasonably large donor pool, and why claims of $p < 0.01$ from a handful of donors should make you suspicious. Be honest about this ceiling: the inference is exact for the permutation it performs, but its resolution is bounded by how many placebos you have.

There is a visual companion you will produce in the notebook: overlay all the placebo gap paths in gray and the treated unit's gap in black. If the black line wanders out beyond the gray cloud after $T_0$ while sitting inside it before, the effect is real and you can *see* it. If the black line is just one more strand in the spaghetti, there is no effect, no matter what point estimate you computed. (Some studies trim placebo units with terrible pre-fit — say, pre-RMSPE more than 2–5× the treated unit's — before drawing the cloud, since those units can never produce an interpretable gap; do it transparently and report the rule.)

One honest caveat about what this $p$-value *is* and is not. It is a test of the **sharp null** that the policy had *no effect on any unit at any time* — the same flavor of null you met in Fisher-style randomization inference — re-imagined for a setting where "treatment" is reassigned across units rather than across coin flips. It does not assume the donors were *randomly* chosen to be untreated; the reference distribution is simply "what the procedure does to units we know were not treated," which is why it is sometimes called a *permutation* or *placebo* test rather than a true randomization test. That distinction matters when you write it up: you are claiming the treated unit's gap is implausibly large *relative to the donors you assembled*, not that treatment was randomly assigned across states. The strength of the claim therefore rests, once more, on the quality and comparability of the donor pool — bad donors make both the point estimate and the inference untrustworthy at the same time.

---

## 7. Synthetic DiD: the best of both worlds

Synthetic control has a quiet weakness, and DiD has a different one, and **Arkhangelsky, Athey, Hirshberg, Imbens and Wager (2021)** noticed that each method's strength patches the other's hole. Their **synthetic difference-in-differences** (SDID) is the synthesis.

Recall the two estimators side by side. **DiD** uses *all* units with equal weight and removes a common time effect by differencing — but it relies on the parallel-trends assumption holding for the raw, unweighted control group, which we have spent the whole chapter doubting. **Synthetic control** reweights *units* to match the pre-period beautifully — but it uses no time differencing and forces the pre-period fit to be near-perfect, which can make it fragile and which throws away the level information DiD exploits. SDID does *both kinds of reweighting at once* and keeps the DiD differencing.

The recipe, in words. SDID computes two sets of weights. **Unit weights** $\hat{w}_j$ on the donors, like synthetic control, chosen so the weighted donors' pre-period trend runs *parallel* to the treated unit's — note "parallel," not "identical": SDID allows a constant level gap between the treated unit and its weighted donors, because it is going to *difference that gap away* DiD-style, so it does not need a perfect level match, only a matched *trend*. **Time weights** $\hat{\lambda}_t$ on the pre-periods, chosen so that the pre-periods which best predict the post-period get more say — down-weighting distant, less-relevant history and emphasizing the pre-years that actually resemble the post-period. Then it runs a *weighted* two-way fixed-effects DiD using both sets of weights:

$$
(\hat{\tau}^{\text{sdid}}, \dots) = \arg\min_{\tau,\mu,\alpha,\beta} \; \sum_{i=1}^{J+1}\sum_{t=1}^{T} \big( Y_{it} - \mu - \alpha_i - \beta_t - \tau\, D_{it} \big)^2 \, \hat{w}_i\, \hat{\lambda}_t,
$$

where $D_{it}=1$ for the treated unit in the post-period, $\alpha_i$ and $\beta_t$ are unit and time fixed effects (Chapter 4.1's two-way FE), and $\tau$ is the treatment effect. Strip the weights ($\hat w_i \equiv 1$, $\hat\lambda_t \equiv 1$) and this *is* ordinary two-way-FE DiD. Drop the time fixed effects and the differencing and push the unit weights to match levels exactly and you are back near pure synthetic control. SDID sits between them, and it does something neither parent does: because it differences out a level gap, it needs only a *parallel* weighted-donor trend (a much weaker, more achievable target than synthetic control's exact match), and because it reweights units and times, it needs a far more defensible parallel-trends claim than vanilla DiD.

The practical payoffs. SDID is more **robust** — it does not crash when no convex combination matches the treated unit's *level*, because it only asks for a matched trend. It is more **precise** — Arkhangelsky et al. show it typically has smaller variance than either parent. And crucially it comes with a **principled inference** procedure (placebo-based or jackknife variance estimators they derive), so you are not stuck with synthetic control's single-unit permutation ceiling when you have a handful of treated units. When you have *one* treated unit and an excellent pre-period fit, classic synthetic control with placebo inference is clean and transparent — use it. When the level match is poor but the *trend* match is good, or when you have a few treated units and want a variance estimate with coverage guarantees, reach for SDID. They are not rivals; SDID is the more general tool, and Abadie's synthetic control is the special, maximally-interpretable case you should still prefer when its assumptions hold and you want a weight vector you can name in a sentence.

---

## 8. The code

Here is a self-contained synthetic control on a simulated premium panel, followed by the placebo loop. It uses only `numpy`, `pandas`, `scipy`, and `matplotlib` so it runs on a fresh env per CONVENTIONS §5; the notebook layers on the `pysyncon`/`SparseSC` libraries and a real SDID implementation.

```python
import numpy as np
import pandas as pd
from scipy.optimize import minimize

rng = np.random.default_rng(20260528)

# --- Simulate a premium panel: 1 treated state + 30 donors, 2010-2022 (T0 = 2017) ---
years = np.arange(2010, 2023)
T0_year = 2017
J = 30                                  # donors
# Two latent factors drive premiums (national trend + a cyclical climate factor);
# each state loads on them differently. A convex donor blend can span this structure.
f1 = np.linspace(8, 12, len(years))                       # national premium trend
f2 = np.sin(np.linspace(0, 3, len(years))) * 1.5          # cyclical climate factor
L1 = rng.uniform(0.7, 1.3, J + 1)                         # loadings on factor 1
L2 = rng.uniform(0.3, 1.0, J + 1)                         # loadings on factor 2
L1[0], L2[0] = 1.0, 0.65                                  # treated state INSIDE donor range
Y = np.outer(L1, f1) + np.outer(L2, f2) + rng.normal(0, 0.12, (J + 1, len(years)))

# Treated state (row 0): a +1.4 (hundred-$) premium jump from 2018 onward.
post = years > T0_year
Y[0, post] += 1.4

panel = pd.DataFrame(Y, columns=years)
pre = years <= T0_year

def synth_weights(treated_pre, donors_pre):
    """Convex weights minimizing pre-period sum of squared mismatch (V = I)."""
    Jn = donors_pre.shape[0]
    def loss(w):
        return np.sum((treated_pre - w @ donors_pre) ** 2)
    cons = ({"type": "eq", "fun": lambda w: w.sum() - 1.0},)   # weights sum to 1
    bnds = [(0.0, 1.0)] * Jn                                   # weights >= 0  (convexity)
    w0 = np.full(Jn, 1.0 / Jn)
    res = minimize(loss, w0, method="SLSQP", bounds=bnds, constraints=cons,
                   options={"ftol": 1e-12, "maxiter": 500})
    return res.x

def sc_gap(unit_idx, pool_idx):
    """Build synthetic control for unit_idx from pool_idx; return gap path + pre/post RMSPE."""
    treated_pre = Y[unit_idx, pre]
    donors_pre = Y[np.ix_(pool_idx, pre)]
    w = synth_weights(treated_pre, donors_pre)
    synth = w @ Y[np.ix_(pool_idx, np.arange(len(years)))]
    gap = Y[unit_idx] - synth
    rmspe_pre = np.sqrt(np.mean(gap[pre] ** 2))
    rmspe_post = np.sqrt(np.mean(gap[~pre] ** 2))
    return gap, rmspe_pre, rmspe_post, w

# --- Real treated unit (row 0) vs synthetic built from all 30 donors ---
donor_ids = np.arange(1, J + 1)
gap0, pre0, post0, w0 = sc_gap(0, donor_ids)
print("Top donor weights:", np.round(np.sort(w0)[::-1][:5], 3))
print(f"Treated pre-RMSPE = {pre0:.3f}, post-RMSPE = {post0:.3f}, ratio = {post0/pre0:.2f}")
print(f"Mean post-treatment gap (est. effect) = {gap0[~pre].mean():.3f}  (true = 1.4)")

# --- Placebo permutation: treat each donor as fake-treated, build SC from the others ---
ratios = {0: post0 / pre0}
for j in donor_ids:
    others = donor_ids[donor_ids != j]          # exclude self; real treated already excluded from pools
    _, prej, postj, _ = sc_gap(j, others)
    ratios[j] = postj / max(prej, 1e-8)

r1 = ratios[0]
all_r = np.array(list(ratios.values()))
p_val = np.mean(all_r >= r1)                     # permutation p-value via RMSPE ratio
rank = (all_r >= r1).sum()
print(f"Treated RMSPE ratio = {r1:.2f}; rank = {rank} of {len(all_r)}; placebo p = {p_val:.3f}")
```

Running it prints a sparse weight vector (a handful of donors carry the synthetic control, most get $\approx 0$), a tiny pre-RMSPE (about $0.035$) against a much larger post-RMSPE (about $1.5$) for a ratio near $44$, a mean post-treatment gap of about $1.5$ — close to the true $+1.4$ we injected — and a permutation $p$-value of $1/31 \approx 0.032$ because the genuinely-treated unit lands as the *single largest* RMSPE ratio among the 31 units. Two things to internalize from the output. First, the *estimate* is a gap, not a coefficient with a textbook standard error; its credibility comes from the placebo rank, not a t-statistic. Second, if you delete the line `Y[0, post] += 1.4` so there is no real effect and re-run, the treated unit's ratio falls back into the placebo crowd (rank $\approx 5$ of $31$, $p \approx 0.16$ — no longer an outlier, no longer significant), and the estimated gap collapses toward zero. The method correctly finds nothing when there is nothing. That is the test working.

---

## What to carry forward

Four things from this chapter will do real work for the rest of the camp and beyond.

First, **build the counterfactual, don't assume it.** When you have one treated unit, DiD's parallel-trends assumption is a wish: no naturally occurring control group is a twin for one specific unit. Synthetic control replaces the wish with a construction — a convex-weighted average of donors, with weights chosen to match the treated unit's pre-period — and then makes the match *visible* so the reader can judge it. Parallel trends is not abandoned; it is engineered and displayed.

Second, **the convexity constraint is the method's conscience.** Non-negative weights summing to one mean the synthetic control cannot extrapolate beyond the donors and cannot fake a fit with wild offsetting coefficients the way unconstrained regression can. You pay in fit — sometimes you simply *cannot* match a treated unit at the edge of the donor distribution — and that refusal to lie is the feature. The resulting sparse weights also give you a sentence you can defend: "the treated unit is 0.46 Oregon, 0.31 Colorado, 0.18 Arizona."

Third, **inference is permutation, not asymptotics.** With one treated unit there is no honest standard error. The placebo test runs the whole procedure on each donor as fake-treated, scales every unit's post-period gap by its own pre-period fit (the RMSPE ratio), and asks whether the real unit is an outlier in that reference distribution. The $p$-value is small-sample, exact for its permutation, and floored at $1/(J+1)$ — so curate a real donor pool and never report more precision than the number of placebos can support.

Fourth, **synthetic DiD generalizes the toolkit.** Arkhangelsky et al. (2021) combine unit weights *and* time weights with a DiD-style differencing, so they need only a matched pre-period *trend* (not an exact level match), inherit DiD's robustness and synthetic control's tailored comparison, and arrive with principled variance estimators. Reach for classic synthetic control when you have one unit, an excellent pre-fit, and want maximal interpretability; reach for SDID when the level match is poor but the trend match is good, or when a few treated units let you exploit its inference. Next chapter (4.5) leaves the single-treated-unit world entirely for shift-share designs, where the identifying variation hides in exposure weights — a different way of asking "where does the variation really come from?"

---

## Your Turn

Open **nb4.4 — "Synthetic control & synthetic DiD."** You will (1) reproduce Priya's climate-disclosure study end to end: build the donor pool, estimate convex weights with `pysyncon` (or the `SparseSC` library), and plot the treated state against its synthetic twin to *see* the pre-period match and the post-period divergence; (2) run the full placebo loop, compute the post/pre RMSPE ratio for every donor, draw the gray-spaghetti placebo plot with the treated unit in black, and report the permutation $p$-value — then delete the injected effect and confirm the method finds nothing; (3) estimate the same effect with **synthetic DiD**, compare its point estimate and its variance-based confidence interval to the classic synthetic-control gap, and write one paragraph on which design you would defend in a referee report and why.

Before you start, make sure you can answer these:

1. **Convexity.** Priya's treated state has the *highest* pre-period premium of any state in her data. (a) Explain why a convex (non-negative, sum-to-one) synthetic control will systematically *underfit* it, and what the pre-period RMSPE will look like as a result. (b) An unconstrained regression of the treated premium on the donors fits the pre-period almost perfectly. Why is that fit *not* reassuring, and what is it likely to do in the post-period? (c) Which method, classic synthetic control or synthetic DiD, is better suited to an edge unit, and why?

2. **Placebo inference.** Priya has 18 donor states. Her treated state's post/pre RMSPE ratio is the second-largest of the 19 units. (a) Compute the permutation $p$-value. (b) What is the *smallest* $p$-value she could possibly report with 18 donors, and what does that tell her about how many donors a credible study needs? (c) A classmate reports a t-statistic of 4.1 and $p<0.001$ for a single-treated-unit synthetic control. What is wrong with that, and what should they report instead?

3. **The assumptions.** The treated state's disclosure mandate was *announced* in mid-2016 but took *effect* in 2018, and insurers visibly began repricing in 2017. (a) Which assumption does the 2017 repricing threaten, and in which direction does it bias the estimated effect? (b) How should Priya set $T_0$ to handle it? (c) Separately, suppose the mandate pushed up reinsurance costs nationally, nudging *donor* premiums upward too. Name the assumption this violates and state whether it makes Priya over- or under-state the true effect.
