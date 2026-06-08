# Ch 4.2 — The Staggered-Adoption Crisis

Chapter 4.1 left you holding a tool that felt almost too clean. You had the two-way fixed-effects regression,

$$
Y_{it} = \alpha_i + \lambda_t + \beta D_{it} + \varepsilon_{it},
$$

where $\alpha_i$ absorbs everything permanent about unit $i$, $\lambda_t$ absorbs everything common to time $t$, $D_{it}$ switches on when unit $i$ is under treatment in period $t$, and $\beta$ — one number, one coefficient — was supposed to be *the* effect of the policy. The machinery was honest: under parallel trends, the within-unit, within-time variation in $D_{it}$ identifies a difference-in-differences, and the canonical 2×2 case — one treated group, one control group, one switch-on date — gave you a $\beta$ you could read off a four-cell table and trust. You even built an event-study version, replacing the single $D_{it}$ with a sequence of lead and lag dummies $\sum_k \beta_k D_{it}^{(k)}$, to *test* parallel trends and trace out the dynamics. It all worked.

This chapter is where it stops working — and the reason is not a coding bug, not a violated parallel-trends assumption, not anything you would have caught with the diagnostics of Chapter 4.1. It is a flaw in the estimator itself, hiding in plain sight for thirty years, exposed only around 2018–2021 by a cluster of papers that set off what people in applied econometrics now simply call the staggered-adoption crisis. The headline result is genuinely unsettling: when units adopt treatment at *different times* (staggered timing) and the treatment effect *differs across units or grows over time* (effect heterogeneity), the single $\beta$ from that exact TWFE regression can be biased, can be a nonsensical weighted average, and — the part that ought to make you sit up — **can come out with the wrong sign.** You can run a regression on a policy that helped everyone, every year, and get back a negative number.

The crisis is not that DiD is wrong. The 2×2 logic of Chapter 4.1 is as sound as ever. The crisis is that the *pooled TWFE regression* you reach for to handle many units adopting at many dates is silently doing something other than what you think. The fix — and there is a clean, now-standard fix — is the heterogeneity-robust estimators of Callaway and Sant'Anna, Sun and Abraham, and Borusyak, Jaravel, and Spiess, all of which share one disarmingly simple idea. This chapter follows the reveal-the-trick pattern: first the plain statement, then *why* TWFE breaks (with a worked example where the sign flips), then the Goodman-Bacon decomposition that names the culprit, then the negative-weights result that generalizes it, and finally the modern estimators that route around the whole problem.

Priya is our guide again, and her question is the one she carried into Chapter 4.1. A wave of states is adopting a climate-risk-disclosure regulation for property insurers — a rule requiring insurers to publish how exposed their books are to wildfire, flood, and storm losses. The hope is that disclosure disciplines underwriting and *lowers* the share of policies that get non-renewed in high-risk ZIP codes (her outcome $Y_{it}$, the non-renewal rate in state $i$, year $t$). In Chapter 4.1 she imagined a single adoption date. Reality is messier and more interesting: California adopts in 2017, a cluster of states in 2019, another wave in 2021, and some states never adopt at all. That is staggered adoption. And the effect of disclosure plausibly *builds* — insurers re-underwrite slowly, so the policy bites harder in year three than in year one. Staggered timing, dynamic effects. That is the exact recipe for the crisis, and Priya is about to run straight into it.

---

## 1. The result in one plain sentence

> **The staggered-DiD crisis, stated plainly.** When different units start treatment in different years *and* the treatment effect is not identical for everyone at every horizon, the single coefficient $\hat{\beta}$ from the two-way fixed-effects regression is a weighted average of many little difference-in-differences comparisons — and some of those comparisons are *forbidden*, because they use already-treated units as the control group, with weights that can be negative.

Everything in this chapter unpacks that sentence. The phrase to burn into memory is **forbidden comparison**: a 2×2 DiD in which the "control" group is a set of units that are *already treated*. In a clean DiD the control group is untreated throughout — its job is to show you what would have happened to the treated group absent the policy. But the pooled TWFE regression, hunting for any variation in $D_{it}$ it can use, will happily treat an early-adopting state as a "control" for a late-adopting state during the years after the early adopter switched on. That early adopter is not a clean counterfactual; it is contaminated by *its own* treatment effect. If that effect is still moving — growing, decaying — it injects a spurious trend into the comparison, and that spurious trend lands inside $\hat{\beta}$ with, it turns out, a weight that can be negative.

The good news, which you should hold onto through the gloom of the next four sections: the disease has a clean cure, and the cure is conceptually trivial. *Only ever compare a newly treated unit to a control group that is genuinely clean — never treated, or not yet treated — never to a unit that has already been treated.* Estimate each clean comparison separately, then average them with transparent, non-negative weights you choose on purpose. That single sentence is the whole research program of Callaway–Sant'Anna, Sun–Abraham, and Borusyak–Jaravel–Spiess. The hard part was seeing that TWFE *fails* to do this; the fix, once seen, is almost obvious.

---

## 2. Why TWFE looks innocent — and where the trap is set

Start by being precise about what the pooled regression is doing, because the trap is set by something that looks like a virtue. Priya has a panel: $N$ states, observed over $T$ years, each state adopting the disclosure rule in some year $G_i$ (its **cohort** or **group**, the year it first switches on) — or never, in which case we say $G_i = \infty$. The treatment indicator is $D_{it} = \mathbf{1}\{t \geq G_i\}$: it turns on in the adoption year and stays on (an **absorbing treatment**, which is the standard staggered setup — once a state has the rule, it keeps it). She runs the same regression as Chapter 4.1:

$$
Y_{it} = \alpha_i + \lambda_t + \beta D_{it} + \varepsilon_{it}.
$$

Why does this *look* like exactly the right thing to do? Because the unit fixed effects $\alpha_i$ soak up every state's permanent differences (California always has more wildfire exposure than Ohio), the time fixed effects $\lambda_t$ soak up every nationwide shock (a bad hurricane season that hits non-renewals everywhere), and $\beta$ is left to be identified by the *within* variation — the moments when a state's $D_{it}$ flips from 0 to 1 against the backdrop of states whose status did not change. With one treated and one control group this is precisely the 2×2 DiD; with many groups it feels like the natural generalization, "pooling all the difference-in-differences together." For decades that is exactly how it was taught and used.

Here is the trap. To identify $\beta$, OLS removes the unit means and the time means from $D_{it}$ and from $Y_{it}$, then regresses the residualized outcome on the residualized treatment — this is the Frisch–Waugh–Lovell logic from Chapter 2.3, the engine under every fixed-effects regression. The residualized treatment $\tilde{D}_{it}$ is what carries all the identifying weight. And $\tilde{D}_{it}$ does something you would never design on purpose: because it is $D_{it}$ with the unit and time averages swept out, a unit that is *already treated* has a residualized treatment that *keeps varying* relative to the changing time average as later cohorts switch on. In the algebra, an already-treated unit gets pressed into service as a comparison group for a not-yet-treated unit. OLS does not know the difference between "untreated and informative" and "already-treated and contaminated." It sees only numbers, and it uses every scrap of variation it can find — including the forbidden kind.

The reason this stayed hidden for thirty years is that the bias *vanishes* in two very common situations, and those situations cover most textbook examples. First, if treatment is **not** staggered — one common adoption date for all treated units — there are no already-treated units to misuse as controls during anyone else's switch-on, and TWFE is fine. Second, if the treatment effect is **homogeneous** — the same constant $\beta$ for every unit at every horizon — then even when an already-treated unit is used as a control, the contamination it injects is itself just $\beta$, which cancels cleanly, and TWFE still recovers $\beta$. The disease requires *both* staggered timing *and* heterogeneous (or dynamic) effects to bite. Chapter 4.1's worked examples had one or the other safely switched off. Priya's real problem has both turned on at once — staggered adoption *and* a treatment effect that grows over time — which is the single most common situation in modern policy data, and exactly the case where the textbook breaks.

---

## 3. The worked example where the sign flips

Abstract warnings persuade no one. Let us build the smallest possible world in which TWFE gets the sign *wrong*, with numbers you can check by hand. This is the example to keep in your pocket for the rest of your career.

Priya has two states and eight years, $t = 1, \dots, 8$. State E (for *early*) adopts the disclosure rule in year 2. State L (for *late*) adopts in year 5. By year 5 every state has the rule — so in this stylized world there is *no never-treated group at all*, which, you will see, is precisely the condition that lets the disaster run to completion. Construct the data so the policy *unambiguously helps* — disclosure *lowers* non-renewal rates, and helps by *more* the longer it has been in force (a dynamic, building effect, which is realistic and is the crucial ingredient).

Write each state's outcome as a baseline level plus a treatment effect that depends on **event time** — years since adoption. Let the per-period treatment effect be $-1$ in the first year of treatment, $-2$ in the second year, $-3$ in the third, and so on: disclosure lowers non-renewals, and the bite deepens. To strip out distractions and see the mechanism nakedly, set all baselines equal and turn off random noise; nothing in the lesson depends on either. The untreated potential outcome of every state is $10$ in every year — so parallel trends holds *perfectly*. The treated outcomes are:

| Year $t$ | State E ($G=2$) | State L ($G=5$) |
|:---:|:---:|:---:|
| 1 | $10$ | $10$ |
| 2 | $10-1=9$ | $10$ |
| 3 | $10-2=8$ | $10$ |
| 4 | $10-3=7$ | $10$ |
| 5 | $10-4=6$ | $10-1=9$ |
| 6 | $10-5=5$ | $10-2=8$ |
| 7 | $10-6=4$ | $10-3=7$ |
| 8 | $10-7=3$ | $10-4=6$ |

Look at what is true by construction. The policy helps both treated states in every treated year — every treatment effect in the table is negative. The *true* average effect of treatment on the treated, averaging the actual effects experienced (E's effects of $-1,\dots,-7$ in years 2–8 and L's effects of $-1,-2,-3,-4$ in years 5–8), is unambiguously and substantially **negative**, $\approx -3.5$. Any honest estimator should return a clearly negative number.

Now run the TWFE regression $Y_{it} = \alpha_i + \lambda_t + \beta D_{it} + \varepsilon_{it}$ on these sixteen observations. You can do this by hand — it is just two-way demeaning — or trust the arithmetic: **the TWFE coefficient comes out positive, $\hat{\beta} = +0.40$.** A policy that lowered non-renewals in every single treated state-year produces a regression coefficient saying it *raised* them. The sign is wrong. Not imprecise — *wrong*.

How can demeaning a table of all-negative effects produce a positive number? The intuition is everything here. Focus on the years 5 through 8, when State L is treated. To estimate L's effect, TWFE wants a control group — units whose status did not change when L switched on. With no never-treated state in the data, the *only* available comparison group is State E — and State E is *already treated* throughout years 5–8, stuck at $D_{it}=1$. So TWFE has no choice but to use **already-treated State E as the control for newly-treated State L.** And what is State E doing across years 5–8? Its treatment effect is *still deepening*, dropping from $-4$ to $-7$. State E's outcome is falling fast for reasons that have nothing to do with State L — it is E's own dynamic treatment effect, still in motion.

When TWFE measures L's treatment by differencing L's change against E's change over years 5–8, E is not a flat baseline — it is *sliding downward* under its own still-growing effect, and sliding *faster* than the freshly-treated L. So L's outcome looks like it is *rising relative to E*, even though L's own non-renewals are falling. The forbidden comparison subtracts E's still-growing treatment effect from L's, and because E's effect is moving in the same direction but faster, the differenced quantity for L flips positive. With no clean never-treated control to dilute it, that forbidden "L-vs-already-treated-E" comparison dominates the pooled average, and $\hat{\beta}$ comes out the wrong sign. (Add even one never-treated state and the catastrophe is contained — TWFE stays negative but badly attenuated, around $-1.2$ instead of the true $-2.6$ on the six-year version; the clean comparisons it provides are enough to keep the *sign* right. The full sign flip needs the forbidden comparisons to be the *only* game in town, which is exactly what "no never-treated unit" delivers.)

That is the entire crisis in one table. Hold the mechanism: **TWFE used an already-treated unit (E), whose own effect was still changing, as a control for a newly-treated unit (L), and the changing effect of the contaminated control got subtracted from the thing you were trying to measure.** Everything that follows is a precise accounting of when and how badly this happens.

---

## 4. The Goodman-Bacon decomposition: TWFE is a weighted average of every possible 2×2

The worked example shows *that* TWFE can break. Goodman-Bacon (2021) shows *exactly* how — by proving that the staggered TWFE coefficient is, identically, a weighted average of all the simple 2×2 DiDs you could form from the data, and by telling you precisely what those 2×2s are and what weight each receives.[^bacon] This is the diagnostic centerpiece of the whole crisis, and it is beautiful because it is an *exact algebraic identity*, not an approximation: the one number $\hat{\beta}$ literally equals a particular weighted sum, no error term.

[^bacon]: Goodman-Bacon, A. (2021). Difference-in-Differences with Variation in Treatment Timing. *Journal of Econometrics*, 225(2), 254–277.

### The four kinds of 2×2

With staggered timing there are several *types* of 2×2 comparison the data can support. Take any two cohorts — say an earlier-adopting group $k$ and a later-adopting group $\ell$ — plus the never-treated group. Goodman-Bacon shows the pooled $\hat{\beta}$ decomposes into these building blocks:

1. **Treated-cohort vs. never-treated.** A timing group compared to states that never adopt. Clean — the control is genuinely untreated throughout. (This is the comparison the §3 table *lacked* a control for, because it had no never-treated state — which is exactly why nothing could rescue the sign there.)
2. **Earlier-treated vs. later-treated, in the window *before* the later group switches on.** The later group is still untreated here, acting as a clean control while the earlier group is treated. Clean — the "control" really is untreated in this window. (In §3: L is the clean control for E during years 2–4, before L adopts.)
3. **Later-treated vs. earlier-treated, in the window *after* the earlier group has switched on.** Here is the poison. The earlier group is *already treated* throughout this window and is being used as the control for the later group. This is the **forbidden comparison**. (In §3: E is the contaminated control for L during years 5–8 — exactly what we traced by hand.)

Types 1 and 2 are honest 2×2 DiDs with clean (untreated-in-window) controls. Type 3 uses an already-treated unit as the control, and it is the entire source of the bias.

### Why the bad comparison is bad — and the weights

In a Type-3 comparison, the change you attribute to the later group's treatment is contaminated by the *change in the earlier group's treatment effect* over the same window. If the earlier group's effect is constant, that change is zero and the comparison is harmless — this is exactly why homogeneous effects save TWFE. But if the effect is **dynamic** (growing or shrinking, as Priya's disclosure effect grows), the earlier group's effect is still moving, and that movement gets *subtracted* from the later group's estimated effect. Goodman-Bacon's identity makes this exact: the Type-3 building block does not estimate the later group's ATT; it estimates the later group's ATT *minus* the change in the earlier group's effect over the window. The forbidden comparison literally has a treatment effect masquerading as a counterfactual trend.

Now the weights. The pooled $\hat{\beta}$ weights each 2×2 by (roughly) the product of the subsample's share of the data and the *variance of treatment* within that pair — and variance of a 0/1 variable is largest when the switch happens in the middle of the window. This has two consequences you must internalize. First, **groups that adopt in the middle of the sample period get the most weight**, regardless of whether their comparisons are clean or forbidden — the weighting has nothing to do with how trustworthy the comparison is, only with treatment timing. Second, and this is the formal punchline that names the crisis:

> **The Goodman-Bacon insight.** $\hat{\beta}^{\text{TWFE}} = \sum_{\text{pairs}} w_{\text{pair}} \cdot \widehat{\text{DiD}}_{\text{pair}}$, an exact weighted average of 2×2 DiDs. The weights $w$ are determined entirely by treatment-timing variance and sum to one, but **the forbidden (Type-3) comparisons enter with weights that can be negative**, and even where weights are positive, the forbidden comparisons estimate the wrong thing. With dynamic effects, the contamination from Type-3 comparisons can dominate, dragging $\hat{\beta}$ away from any sensible average of true effects — even reversing its sign.

This is the practical gift of the decomposition: you can *run* it (the `bacondecomp` routines in Stata and the Python `bacon` implementations) and literally see how much of your $\hat{\beta}$ comes from each type of comparison. If a large share of the weight sits on forbidden "later vs. already-treated" comparisons, your headline TWFE number is built on sand, and the Goodman-Bacon plot — each 2×2 estimate against its weight, colored by type — shows it at a glance. Priya should run this before she trusts any pooled coefficient.

---

## 5. The negative-weights problem, in full generality

Goodman-Bacon's decomposition is exact and intuitive, but it is built for the specific case of a binary, absorbing, staggered treatment. de Chaisemartin and D'Haultfœuille (2020) prove the same disease in a far more general setting and state it in the form that has become the rallying cry of the literature.[^dcdh] Their result strips the problem to its essence.

[^dcdh]: de Chaisemartin, C., & D'Haultfœuille, X. (2020). Two-Way Fixed Effects Estimators with Heterogeneous Treatment Effects. *American Economic Review*, 110(9), 2964–2996.

Their setup: any panel with two-way fixed effects, treatment that can switch on (and even off) at different times for different units. They prove that the TWFE coefficient $\hat{\beta}$ is a weighted average of the treatment effects across all treated unit-time cells $(i,t)$:

$$
\hat{\beta}^{\text{TWFE}} \;\xrightarrow{p}\; \sum_{(i,t)\,:\,D_{it}=1} w_{it}\,\cdot\,\text{ATT}_{it},
$$

where $\text{ATT}_{it}$ is the genuine treatment effect for unit $i$ at time $t$ and the weights $w_{it}$ **sum to one but are not guaranteed to be positive.** That is the whole result, and it is devastating in its simplicity. A weighted average with some negative weights is not a sensible average of anything. If every $\text{ATT}_{it}$ is negative (disclosure helps everyone, always) but some weights are negative, the weighted sum can be positive — which is exactly the sign flip of §3, now derived in complete generality rather than from a hand-built table.

Two consequences make this more alarming than Goodman-Bacon's already-bad news. First, the weights depend only on the *design* — how many units are treated when — and not at all on the treatment effects, so you can **compute the weights from your data alone, before estimating a single effect.** de Chaisemartin and D'Haultfœuille hand you a diagnostic: count how many of your weights are negative and how much total negative weight there is. If a meaningful share of weight is negative, $\hat{\beta}$ is uninterpretable. Second, they show the failure can be so severe that $\hat{\beta}$ and *every individual* $\text{ATT}_{it}$ can have opposite signs — there can exist data-generating processes where all true effects are strictly positive yet the TWFE probability limit is strictly negative. The estimator is not merely noisy or hard to interpret; it can be *qualitatively* wrong about the direction of the effect, which is the one thing a policymaker most needs to get right.

It helps to see Goodman-Bacon and de Chaisemartin–D'Haultfœuille as two views of one object. Goodman-Bacon decomposes $\hat{\beta}$ by *pairs of cohorts* and shows the forbidden later-vs-already-treated pairs are the culprits; de Chaisemartin–D'Haultfœuille decomposes the same $\hat{\beta}$ by *individual treated cells* and shows the culprits manifest as negative cell weights. Same disease, two diagnostics. Both point to the identical cause — already-treated units doing control duty — and both point to the identical cure, which is the subject of the rest of the chapter.

---

## 6. The shared fix: clean controls and transparent aggregation

Step back from the wreckage and ask what went wrong at the root. The pooled regression failed because it let OLS pick the comparisons — and OLS, blind to which units are clean controls, included the forbidden ones with whatever weights the timing-variance arithmetic dictated. Every modern heterogeneity-robust estimator fixes this by *taking the comparison-selection and the weighting out of OLS's hands* and doing both deliberately. They differ in bookkeeping, but they share one idea, and if you remember nothing else, remember this:

> **The shared idea.** Never let an already-treated unit serve as a control. For each newly-treated cohort, estimate its effect by comparing it *only* to clean controls — units that are **never treated**, or **not yet treated** (treated later, but not yet at the moment of comparison). Estimate these clean group-time effects one at a time, then aggregate them into whatever summary you actually want, using weights you choose and can write down.

Two phrases carry the whole load. **"Clean control"** means a unit that is untreated at the moment it is being used as a counterfactual — either never-treated (clean forever) or not-yet-treated (clean *until* its own adoption date, usable as a control only in the window before it switches on). **"Transparent aggregation"** means that instead of one regression spitting out one opaque $\hat{\beta}$, you first estimate a whole panel of *group-time* effects, then explicitly average them — by event time for a dynamics plot, by calendar time, or into a single overall number with sensible non-negative weights (typically each cohort weighted by its size). The opacity that hid the crisis for thirty years is replaced by an audit trail.

The three estimators below are three implementations of that one paragraph. Callaway–Sant'Anna build the group-time effects directly and aggregate them. Sun–Abraham achieve the same thing inside a cleverly-saturated regression. Borusyak–Jaravel–Spiess get there by imputing the missing untreated potential outcomes. They give numerically very similar answers in most applications, because they are solving the same problem the same way; you choose among them mostly by convenience and by which standard errors and pre-trend tests you want.

> **Spec discipline for staggered DiD (CONVENTIONS §4, extended).** When you write up a staggered design, the empirical-spec checklist gains two lines that the 2×2 case did not need. (1) **Name the control group**, explicitly: are your clean comparisons against *never-treated* units, *not-yet-treated* units, or both? This matters because never-treated units may differ systematically from adopters (a state that *never* regulates insurers is a different animal), whereas not-yet-treated units are eventual adopters and often a more credible counterfactual — but using them shrinks your control pool as more cohorts switch on. (2) **Name the aggregation weights**: an event-time average, a calendar-time average, and a single overall ATT can be genuinely different numbers, and the reader must know which one your headline reports and how cohorts were weighted into it. The identifying assumption is still **parallel trends** — but now stated *per cohort*: each adopting cohort's untreated potential outcome would have moved parallel to its clean control group's. Priya's spec, fully named: outcome = state-year non-renewal rate · treatment = climate-disclosure rule (staggered $G_i$) · controls = none (or covariate-conditional parallel trends via doubly-robust DiD) · fixed effects = absorbed inside the group-time estimator · clustering = by state · sample = 50 states, years spanning the adoption waves · identification = per-cohort parallel trends against never- and not-yet-treated states, aggregated to an event-time ATT.

---

## 7. Callaway–Sant'Anna: group-time ATTs with clean controls

Callaway and Sant'Anna (2021) give the cleanest statement of the fix, and it is the estimator paired with TWFE in this chapter's notebook, so we spend the most time here.[^cs] Their central object is the **group-time average treatment effect**, written $\text{ATT}(g,t)$: the average treatment effect, at calendar time $t$, for the cohort of units that first adopted in year $g$. Read the two arguments carefully — $g$ indexes *which cohort* (defined by its adoption year, exactly the $G_i$ from §2), and $t$ indexes *when* you are measuring. $\text{ATT}(2017, 2019)$ is the effect on the states-that-adopted-in-2017, measured in 2019 — i.e., their two-years-after effect.

[^cs]: Callaway, B., & Sant'Anna, P. H. C. (2021). Difference-in-Differences with Multiple Time Periods. *Journal of Econometrics*, 225(2), 200–230.

The estimation of each $\text{ATT}(g,t)$ is a humble, honest 2×2 DiD, built to use only clean controls. For cohort $g$ and a post-adoption period $t \geq g$, compare the change in cohort $g$'s outcome — from the period just before $g$ adopted ($g-1$) to period $t$ — against the change over the *same calendar window* in a clean comparison group:

$$
\widehat{\text{ATT}}(g,t) = \underbrace{\big(\bar{Y}_{g,t} - \bar{Y}_{g,\,g-1}\big)}_{\text{cohort } g\text{'s change}} \;-\; \underbrace{\big(\bar{Y}_{C,t} - \bar{Y}_{C,\,g-1}\big)}_{\text{clean control's change}},
$$

where the control group $C$ is **either the never-treated units, or the not-yet-treated units** (those whose adoption year is strictly after $t$, so they are still untreated throughout the window). That is the only real rule, and it is the rule TWFE broke: the control is never an already-treated unit. Each $\widehat{\text{ATT}}(g,t)$ is a clean Type-1 or Type-2 comparison in Goodman-Bacon's language, and not a single forbidden Type-3 comparison is ever formed. (In practice Callaway–Sant'Anna let you make the comparison *conditional* on covariates, using a doubly-robust DiD that marries the outcome-regression and propensity-score ideas from Chapter 3.3 — so you can relax parallel trends to hold only after conditioning. The clean-control principle is unchanged.)

Now you have a whole grid of $\widehat{\text{ATT}}(g,t)$ values — one for every cohort and every post period. This grid is the honest output, and you aggregate it on purpose. The most useful aggregation is by **event time** $e = t - g$ (years since adoption), averaging $\widehat{\text{ATT}}(g,t)$ across cohorts that share the same $e$:

$$
\widehat{\text{ATT}}^{\text{es}}(e) = \sum_{g} \, \mathbf{1}\{t = g+e\}\; \omega_g \, \widehat{\text{ATT}}(g,\,g+e),
$$

with non-negative weights $\omega_g$ (cohort sizes, summing to one). Plotting $\widehat{\text{ATT}}^{\text{es}}(e)$ against $e$ is the **heterogeneity-robust event study** — the honest replacement for the lead/lag TWFE event study of Chapter 4.1. Its $e < 0$ values are genuine placebo/pre-trend checks (effects should be near zero before adoption), and its $e \geq 0$ values trace the dynamic build-up of the disclosure effect that TWFE mangled. You can also collapse the whole grid to a single overall ATT — a transparent weighted average of every clean group-time effect — which is the one number to report in place of the broken pooled $\hat{\beta}$.

Run this on Priya's world from §3 — but notice the catch that §3 deliberately exposed: with *only* the two eventually-treated states E and L, the late cohort L has *no* clean control in its post-period (E is already treated, and there is no never-treated state), so L's effect is not identified without one. This is the honest flip side of the crisis — clean estimators *refuse* to form the forbidden comparison, which means they refuse to fabricate an answer when no clean control exists. So restore a genuine never-treated state N (Priya's real data has plenty of non-adopters) and watch it work on the six-year version. $\widehat{\text{ATT}}(2, t)$ for State E uses State N (and, before year 5, the not-yet-treated State L) as clean controls and recovers E's true effects $-1, -2, -3, -4, -5$. $\widehat{\text{ATT}}(5, t)$ for State L uses State N as a clean control — *never* the already-treated State E — and recovers L's true effects $-1, -2$. Aggregate by event time and the overall clean ATT comes out at the true $-2.57$, the negative, building dynamic profile that is true by construction — versus the attenuated $-1.23$ that pooled TWFE returns on the very same data. No forbidden comparison, no contamination, no sign flip. The estimator returns the answer the data actually contain.

---

## 8. Sun–Abraham and Borusyak–Jaravel–Spiess: the same idea, two more routes

Callaway–Sant'Anna build the group-time grid from explicit 2×2s. The other two leading estimators reach the same destination by different roads, and seeing them clarifies that the fix is one idea, not three rival theories.

### Sun–Abraham: an honest event-study regression

Sun and Abraham (2021) noticed that the crisis infects the *event-study* version of TWFE just as badly as the static one — and in a way that is especially treacherous because it corrupts the very pre-trend test you rely on.[^sa] Recall the Chapter 4.1 event study: you replace $D_{it}$ with a full set of relative-time dummies $D_{it}^{(e)} = \mathbf{1}\{t - G_i = e\}$ and estimate a coefficient $\beta_e$ for each event time $e$. Sun and Abraham prove that under staggered timing with heterogeneous dynamics, each estimated $\hat{\beta}_e$ is *contaminated by treatment effects from other event times of other cohorts* — the leads and lags bleed into each other through the same forbidden comparisons. A flat-looking pre-trend can hide real bias, and a $\hat{\beta}_e$ for $e=3$ can be polluted by some other cohort's $e=1$ effect. The event-study plot, your trusted diagnostic, can lie.

[^sa]: Sun, L., & Abraham, S. (2021). Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects. *Journal of Econometrics*, 225(2), 175–199.

Their fix, the **interaction-weighted (IW) estimator**, is to *saturate* the regression: interact every relative-time dummy with every cohort indicator, estimating a separate coefficient $\delta_{g,e}$ for each (cohort $g$, event-time $e$) pair, using never-treated (or last-treated) units as the clean control. These $\delta_{g,e}$ are precisely Callaway–Sant'Anna's $\text{ATT}(g,t)$ in regression clothing. Then aggregate to event-time effects with cohort-share weights — the *interaction weighting* in the name. Because each cohort's dynamics are estimated separately before averaging, no cohort's effect can leak into another's. The output is a clean event study you can trust for both pre-trends and dynamics, obtained entirely within the familiar regression framework — attractive if you would rather stay in a single `feols`-style call than learn a new package.

### Borusyak–Jaravel–Spiess: imputation

Borusyak, Jaravel, and Spiess (2024) take the most direct route of all, and it doubles as the most illuminating way to *understand* what every clean estimator is really doing.[^bjs] Their **imputation** estimator reasons as follows. The treatment effect for a treated cell $(i,t)$ is, by definition, the actual outcome minus the untreated potential outcome: $\text{effect}_{it} = Y_{it} - Y_{it}(0)$. You observe $Y_{it}$. The only missing piece is $Y_{it}(0)$ — what the unit *would* have done untreated. So *impute it*.

[^bjs]: Borusyak, K., Jaravel, X., & Spiess, J. (2024). Revisiting Event-Study Designs: Robust and Efficient Estimation. *Review of Economic Studies*, 91(6), 3253–3285.

The recipe is three steps and it is gorgeous in its directness. First, fit the two-way fixed-effects model $Y_{it} = \alpha_i + \lambda_t + \varepsilon_{it}$ **using only the untreated observations** — every cell where $D_{it}=0$ (all never-treated cells, plus the pre-adoption years of every eventual adopter). Crucially, the treated cells are *excluded* from this fit, so no treatment effect contaminates the estimated $\hat{\alpha}_i, \hat{\lambda}_t$. Second, use those estimates to *impute* the missing untreated outcome for each treated cell: $\hat{Y}_{it}(0) = \hat{\alpha}_i + \hat{\lambda}_t$. Third, the estimated effect for each treated cell is the gap $\hat{\tau}_{it} = Y_{it} - \hat{Y}_{it}(0)$, and you average these $\hat{\tau}_{it}$ however you like — by event time, by cohort, overall — with explicit weights.

This makes the shared idea unmissable. The whole disease was that TWFE, fit on *all* the data, let treated cells corrupt the fixed-effect estimates that serve as the counterfactual. Imputation simply *refuses to fit on treated cells*: the counterfactual $\hat{Y}_{it}(0)$ is built only from clean, untreated information, so an already-treated unit's effect can never leak into anyone's control. It is the clean-control principle reduced to its logical minimum, and Borusyak–Jaravel–Spiess show it is also (under their assumptions) the *efficient* estimator — the most precise way to use the clean variation. It comes with a proper pre-trend test built from the untreated residuals, sidestepping the contaminated pre-trends Sun and Abraham warned about.

Three estimators, one principle. Callaway–Sant'Anna assemble clean 2×2s; Sun–Abraham saturate the event-study regression so each cohort's dynamics are estimated in isolation; Borusyak–Jaravel–Spiess impute the counterfactual from untreated cells only. All three (i) form only clean comparisons, (ii) produce a group-time or cohort-event grid of effects, and (iii) aggregate transparently with weights you control. In most real datasets they land within sampling noise of one another — and far, often *qualitatively* far, from the broken pooled TWFE.

---

## 9. The code

Here is the crisis and its cure in one runnable block. We build two worlds. World A is the §3 sign-flip world — two states, *no* never-treated unit — where TWFE comes out the wrong sign. World B adds a genuine never-treated state, which lets the clean group-time estimator identify every cohort and recover the truth. To keep the block self-contained and dependency-light, we implement the Callaway–Sant'Anna clean comparison directly as a handful of clean 2×2 DiDs (the full `differences`/`csdid` packages add inference and covariates; nb4.2 uses them properly).

```python
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

def make_world(adopt, Tmax):
    """Staggered panel; untreated outcome = 10 everywhere (parallel trends holds exactly);
    per-period effect at event time e = -(e+1), i.e. -1,-2,-3,... (negative and BUILDING)."""
    rows = []
    for state, g in adopt.items():
        for t in range(1, Tmax + 1):
            e = t - g
            effect = -(e + 1) if t >= g else 0.0
            rows.append({"state": state, "t": t, "G": g,
                         "D": int(t >= g), "Y": 10.0 + effect})
    return pd.DataFrame(rows)

def twfe(df):
    return smf.ols("Y ~ C(state) + C(t) + D", data=df).fit().params["D"]

def att_gt(df, g, t):
    """ATT for cohort g at time t vs CLEAN controls (never- or not-yet-treated AT t)."""
    base = g - 1                                  # last pre-adoption period for cohort g
    treated = df[df.G == g]
    clean   = df[df.G > t]                        # G>t  =>  untreated through period t  (never E!)
    return ((treated.loc[treated.t == t, "Y"].mean() - treated.loc[treated.t == base, "Y"].mean())
            - (clean.loc[clean.t == t, "Y"].mean() - clean.loc[clean.t == base, "Y"].mean()))

def clean_overall(df, cohorts, Tmax):
    cells = [(g, t) for g in cohorts for t in range(g, Tmax + 1)]
    atts = {(g, t): att_gt(df, g, t) for g, t in cells}
    return atts, np.mean(list(atts.values()))

# --- World A: NO never-treated unit (E adopts yr2, L adopts yr5), 8 years -> TWFE sign FLIPS ---
A = make_world({"E": 2, "L": 5}, Tmax=8)
print("World A  TWFE beta_hat:", round(twfe(A), 3),
      "  <-- WRONG SIGN: every true effect is negative, but TWFE says +")

# --- World B: add a never-treated state N so the clean estimator can identify every cohort ---
B = make_world({"E": 2, "L": 5, "N": np.inf}, Tmax=6)
print("World B  TWFE beta_hat:", round(twfe(B), 3), "  (attenuated toward 0, true is -2.571)")
atts, overall = clean_overall(B, cohorts=[2, 5], Tmax=6)
for (g, t), v in atts.items():
    print(f"   ATT(g={g}, t={t}) = {v:+.2f}   (event time e={t-g})")
print("World B  clean overall ATT:", round(overall, 3),
      "  <-- correct: recovers the true -2.571 exactly")
```

Running it prints a **positive** TWFE coefficient ($+0.40$) in World A, on data where the true effect is negative in every treated cell — the sign flip, live, driven by the forbidden "L vs. already-treated E" comparison that is the *only* comparison available when no never-treated unit exists. In World B, adding a clean never-treated control tames TWFE to a merely *attenuated* $-1.23$ (right sign, wrong magnitude versus the true $-2.571$), and the Callaway–Sant'Anna clean 2×2s recover State E's $-1,-2,-3,-4,-5$ and State L's $-1,-2$ exactly, for an overall clean ATT of $-2.571$ — the truth, to the decimal. The contrast across the three printed numbers *is* the staggered-adoption crisis: same parallel-trends assumption holding perfectly, yet pooled TWFE ranges from sign-flipped to badly attenuated while the clean estimator is exact. nb4.2 takes this further with the real `linearmodels`/`pyfixest` TWFE, a proper Callaway–Sant'Anna fit with valid standard errors and an event-study plot, and a Goodman-Bacon decomposition that shows you the negative weight sitting on the forbidden comparison.

---

## What to carry forward

Four things from this chapter will change how you read every difference-in-differences result for the rest of your life.

First, **the pooled TWFE regression is not a safe default under staggered adoption.** The exact regression from Chapter 4.1, $Y_{it} = \alpha_i + \lambda_t + \beta D_{it} + \varepsilon_{it}$, identifies a sensible effect only when timing is common *or* effects are homogeneous. The moment you have *both* staggered timing *and* heterogeneous or dynamic effects — the normal situation in policy data — the single $\hat{\beta}$ is a contaminated weighted average that can be biased and can carry the wrong sign. Seeing a TWFE DiD on staggered data should now trigger an immediate question, not acceptance.

Second, **the root cause is the forbidden comparison.** OLS, left to itself, uses already-treated units as controls for not-yet-treated units, and if the already-treated unit's effect is still moving, that motion is mis-read as a counterfactual trend and subtracted from the thing you want. Goodman-Bacon (2021) proves $\hat{\beta}$ is exactly a timing-variance-weighted average of all 2×2 DiDs and isolates these "later vs. already-treated" comparisons as the culprits; de Chaisemartin and D'Haultfœuille (2020) prove the same disease in full generality as a weighted average of cell-level effects with *negative weights* — weights you can compute from the design alone, before estimating anything.

Third, **the cure is one idea: clean controls plus transparent aggregation.** Compare each newly-treated cohort only to never-treated or not-yet-treated units, estimate a grid of group-time effects, and average them with weights you choose and can defend. Callaway and Sant'Anna (2021) do this with explicit doubly-robust 2×2s and group-time $\text{ATT}(g,t)$; Sun and Abraham (2021) do it by saturating the event-study regression with cohort×relative-time interactions and weighting them; Borusyak, Jaravel, and Spiess (2024) do it by imputing the untreated counterfactual from untreated cells only. Three routes, one principle, near-identical answers — and all of them honest where TWFE was not.

Fourth, **report the diagnostics, not just the estimate.** Before trusting any staggered DiD, run the Goodman-Bacon decomposition to see how much weight sits on forbidden comparisons, check the de Chaisemartin–D'Haultfœuille negative-weight count, and present a heterogeneity-robust event study whose pre-period coefficients actually test parallel trends without the cohort-bleed that contaminates the naive TWFE event study. The empirical-spec discipline from CONVENTIONS §4 now has a new line for staggered designs: name your *control group* (never- vs. not-yet-treated) and your *aggregation weights* explicitly, because in this setting those choices, not OLS's defaults, determine what your single headline number means.

---

## Your Turn

Open **nb4.2 — "Staggered DiD: TWFE vs. Callaway–Sant'Anna."** You will (1) rebuild Priya's staggered climate-disclosure panel — California in 2017, a 2019 wave, a 2021 wave, and never-adopters — with a treatment effect that *builds* over event time, and confirm the pooled TWFE coefficient is biased (and, in the sharp version, wrong-signed) relative to the true average effect; (2) run the **Goodman-Bacon decomposition** and read off how much of $\hat{\beta}$ comes from clean (treated-vs-never, early-vs-later-before-adoption) comparisons versus the forbidden (later-vs-already-treated) comparisons, and find the negative weight; (3) estimate the **Callaway–Sant'Anna** group-time $\text{ATT}(g,t)$ with never-treated controls, aggregate to a heterogeneity-robust event study, and verify the pre-trends are flat and the post-period dynamics match the truth — then compare its overall ATT to the broken TWFE number side by side.

Before you start, make sure you can answer these:

1. **Name the forbidden comparison.** In Priya's data, California adopts in 2017 and a second state adopts in 2021. (a) Which calendar years form a *clean* 2×2 comparison between these two states, and which state is the control in that window? (b) Which years form the *forbidden* comparison, and which state is wrongly used as the control? (c) Explain in one sentence why the forbidden comparison injects bias *only if* the disclosure effect is dynamic.

2. **When is TWFE actually fine?** State the two distinct conditions, *either* of which rescues the pooled TWFE coefficient under staggered timing, and for each one explain in a sentence why the forbidden comparisons stop causing trouble. (Hint: one condition removes the already-treated controls entirely; the other makes their contamination cancel.)

3. **Read the cure.** A classmate reports a Callaway–Sant'Anna analysis with a grid of $\text{ATT}(g,t)$ estimates and an event-study plot. (a) What does the argument $g$ mean versus the argument $t$, and what is event time $e$ in terms of them? (b) Which units are eligible to serve as the control group for cohort $g$ at time $t$, and which are explicitly forbidden? (c) The plot's coefficients at $e = -2$ and $e = -1$ are near zero — what assumption does that support, and why is this pre-trend test *more* trustworthy here than the one from a naive TWFE event study?
