# Chapter 4.1 — Difference-in-Differences and Event Studies

Priya has a natural experiment, and for once it is not the kind she has to apologize for.

She studies climate risk in insurance markets, and a clean thing just happened. On January 1 of a particular year, one state — call it the **treated state** — changed a regulation governing how home insurers may price wildfire risk. The other states left their rules alone. Priya has annual data on the average homeowner's premium in every state for several years before and after the change. Her question is the one a regulator would actually ask: *did the regulation change premiums, and by how much?*

Her first instinct is the one Week 3 taught her to distrust. She could compare the treated state's premium *after* the rule to its premium *before* — a before-and-after difference. Premiums in the treated state rose \$180 on average from the year before to the year after. Is that the effect of the regulation? Almost certainly not all of it. Those were years when wildfires got worse everywhere, reinsurance costs climbed nationwide, and inflation pushed up rebuilding costs across the country. Some of Priya's \$180 is the regulation; some of it is everything else that was happening to insurance that year and would have happened *regardless* of the rule. A pure before-and-after comparison confounds the treatment with the passage of time.

Her second instinct is the one Week 3 taught her to distrust *even more*. She could compare the treated state to the other states *in the year after* the change — a treated-versus-control difference at a single point in time. But that runs straight into the selection-bias term from Chapter 3.1: the treated state is not a random state. It has its own fire geography, its own building stock, its own pre-existing premium level. Maybe it always had premiums \$300 higher than the average state, regulation or no regulation. A cross-sectional comparison confounds the treatment with whatever made that state different in the first place — the very $\mathbb{E}[Y_i(0)\mid D_i=1]\neq\mathbb{E}[Y_i(0)\mid D_i=0]$ problem we spent all of Week 3 fighting.

Each comparison alone is contaminated. The trick of this chapter — and it is one of the most useful tricks in all of applied economics — is that the two *bad* comparisons, combined the right way, cancel each other's contamination and leave something clean. Take the difference *across time* (which removes the fixed state difference) and the difference *across states* (which removes the common time shock), and **difference the two differences**. What survives is the regulation's effect, under one assumption we will state with great care because it is the whole ballgame. This is **difference-in-differences** (DiD), and by the end of the chapter you will be able to write it three ways — as a table of four cell means, as a potential-outcomes estimand, and as a regression you can run on a laptop — and, more importantly, to name the single assumption every version of it leans on and to say exactly what you would see when that assumption fails.

We follow the usual reveal-the-trick structure. The clean idea first: the $2\times 2$ table and the double difference. Then the potential-outcomes meaning, and the assumption that makes the double difference equal a causal effect. Then the regression form that we will carry for the rest of the week. Then the dynamic version — event studies — that lets the effect grow over time and lets us *look* at whether the assumption was plausible. Then how to get the standard errors right, which is subtler here than anywhere you have seen. And finally a warning: everything in this chapter assumes the treatment switched on at *one* moment for *one* group, and the moment that assumption breaks — when different units adopt at different times — much of the clean story breaks with it. That is Chapter 4.2.

---

## 4.1.1 The 2×2: four numbers and a double difference

Strip Priya's problem to its skeleton. Two groups: the **treated** state and a **control** group (one comparison state, or the average of several — for now imagine one, to keep the arithmetic visible). Two time periods: **before** the regulation and **after**. That gives four cells, and in each cell we have an average outcome — here, the average premium. Lay them in a table.

|                | Before          | After           |
|----------------|-----------------|-----------------|
| **Treated**    | $\bar Y_T^{\,\text{pre}}$ | $\bar Y_T^{\,\text{post}}$ |
| **Control**    | $\bar Y_C^{\,\text{pre}}$ | $\bar Y_C^{\,\text{post}}$ |

Put Priya's numbers in, in dollars of annual premium:

|                | Before  | After   |
|----------------|---------|---------|
| **Treated**    | \$1{,}500 | \$1{,}680 |
| **Control**    | \$1{,}200 | \$1{,}310 |

Now the two contaminated comparisons, written out. The treated state's **before-and-after** change is $\bar Y_T^{\,\text{post}} - \bar Y_T^{\,\text{pre}} = 1{,}680 - 1{,}500 = \$180$. That is the \$180 from the opening, and we agreed it mixes the regulation with everything else that moved that year. The control state's before-and-after change is $\bar Y_C^{\,\text{post}} - \bar Y_C^{\,\text{pre}} = 1{,}310 - 1{,}200 = \$110$. The control got *no* regulation, so its \$110 is *pure* "everything else" — the common upward drift in premiums from worsening fires, costlier reinsurance, and inflation, with no treatment in it at all.

Here is the move. The treated state experienced "everything else" *plus* the regulation; the control state experienced "everything else" *alone*. So subtract the control's change from the treated's change, and "everything else" cancels:

$$
\widehat{\text{DiD}}
= \underbrace{(\bar Y_T^{\,\text{post}} - \bar Y_T^{\,\text{pre}})}_{\text{treated change} = \$180}
\;-\;
\underbrace{(\bar Y_C^{\,\text{post}} - \bar Y_C^{\,\text{pre}})}_{\text{control change} = \$110}
= 180 - 110 = \$70.
$$

The difference-in-differences estimate is **\$70**. The honest reading: of the \$180 the treated state's premiums rose, \$110 was the tide lifting all boats — the trend the control state also rode — and only the remaining **\$70** is attributable to the regulation. That is the number Priya wants, and the two contaminated differences produced it by cancellation.

It is worth seeing that the "double difference" can be taken in the other order and gives the identical answer, which is a good sanity check and also tells you something. Instead of (treated change) minus (control change), take (after-gap) minus (before-gap): the treated-minus-control gap *after* is $1{,}680 - 1{,}310 = \$370$, the same gap *before* is $1{,}500 - 1{,}200 = \$300$, and the difference of those gaps is $370 - 300 = \$70$ again. Same number. The first order says "remove the time trend by differencing over time, then compare groups." The second says "remove the fixed group difference by differencing across groups, then compare over time." Both land on \$70 because the double difference is symmetric:

$$
\widehat{\text{DiD}}
= \big(\bar Y_T^{\,\text{post}} - \bar Y_T^{\,\text{pre}}\big) - \big(\bar Y_C^{\,\text{post}} - \bar Y_C^{\,\text{pre}}\big)
= \big(\bar Y_T^{\,\text{post}} - \bar Y_C^{\,\text{post}}\big) - \big(\bar Y_T^{\,\text{pre}} - \bar Y_C^{\,\text{pre}}\big).
$$

Notice what each differencing operation kills. Differencing **over time** within a group removes anything about that group that is *fixed across the two periods* — the treated state's permanently higher fire risk, its building stock, its baseline price level. Those subtract out because they are in both the "before" and the "after." Differencing **across groups** within a period removes anything that hits *both groups equally* in that period — the nationwide reinsurance shock, the common inflation. Those subtract out because they are in both the treated row and the control row. DiD is a machine for removing two kinds of confounding at once: a *fixed group difference* and a *common time shock*. What it cannot remove — and this is the crack we will return to — is anything that varies across *both* group and time together.

This is the most famous application in the canon, so meet it now: **Card and Krueger (1994)** studied what happened to fast-food employment when New Jersey raised its minimum wage in 1992 while neighboring Pennsylvania did not. They surveyed fast-food restaurants in both states before and after the increase, built exactly this $2\times 2$ table with employment in the cells, and computed the double difference. New Jersey is the treated state, Pennsylvania the control, the wage hike the regulation. Their finding — that employment did not fall, contrary to the textbook prediction — was controversial precisely *because* the design was clean enough that people had to argue with the assumption rather than the arithmetic. Which is the right thing to argue with, and is where we go next.

---

## 4.1.2 What the double difference means in potential outcomes

The \$70 is suggestive, but Week 3 trained you not to trust a number until you have written it in potential outcomes and found the assumption that makes it a causal effect. Let us do that. We are now in a **panel**: each unit $i$ (a state) is observed at each time $t$, so outcomes, treatment, and potential outcomes all carry two subscripts. Keep the Chapter 3.1 machinery, just add time.

For unit $i$ in period $t$, define two potential outcomes exactly as before, now indexed by time:

- $Y_{it}(1)$ — the outcome unit $i$ *would* have in period $t$ **if it were treated** in $t$.
- $Y_{it}(0)$ — the outcome unit $i$ *would* have in period $t$ **if it were untreated** in $t$.

Let $D_{it}=1$ if unit $i$ is under treatment in period $t$ and $0$ otherwise. In our $2\times 2$ world the treated state has $D_{it}=1$ only in the *post* period; every control-state cell and the treated state's *pre* cell have $D_{it}=0$. The observation rule from Chapter 3.1 carries over unchanged: $Y_{it} = D_{it}\,Y_{it}(1) + (1-D_{it})\,Y_{it}(0)$.

The estimand DiD targets is the **average treatment effect on the treated, in the post period** — the effect of the regulation on the state that actually got it, at the time it had it:

$$
\text{ATT} = \mathbb{E}\big[\,Y_{it}(1) - Y_{it}(0)\;\big|\;\text{treated},\ \text{post}\,\big].
$$

The first term, $\mathbb{E}[Y_{it}(1)\mid \text{treated, post}]$, is the treated state's *observed* post-period premium, $\bar Y_T^{\,\text{post}} = \$1{,}680$. No problem there — that world happened. The villain, as always, is the second term, $\mathbb{E}[Y_{it}(0)\mid \text{treated, post}]$: **what the treated state's premium would have been in the post period had the regulation never passed.** That world did not happen. It is the missing counterfactual, and DiD's entire job is to supply a credible value for it.

Now watch how the four cells try to reconstruct that counterfactual. The naive before-after comparison uses the treated state's own *pre* level, $\bar Y_T^{\,\text{pre}}=\$1{,}500$, as the stand-in for its untreated post outcome — which assumes the treated state's premium would have been *flat* from pre to post absent treatment. That is wrong: premiums were rising everywhere. The cross-sectional comparison uses the control state's *post* level, $\bar Y_C^{\,\text{post}}=\$1{,}310$, as the stand-in — which assumes the two states would have had the *same level* absent treatment. Also wrong: the treated state was \$300 higher to begin with.

DiD's counterfactual is smarter than either. It says: take the treated state's own pre-period level, and let it *grow by the same amount the control state grew*. The control's growth, $\bar Y_C^{\,\text{post}} - \bar Y_C^{\,\text{pre}} = \$110$, is our estimate of the common trend. So the imputed counterfactual is

$$
\widehat{\mathbb{E}[Y_{it}(0)\mid \text{treated, post}]}
= \underbrace{\bar Y_T^{\,\text{pre}}}_{1{,}500} + \underbrace{(\bar Y_C^{\,\text{post}} - \bar Y_C^{\,\text{pre}})}_{110}
= \$1{,}610.
$$

The treated state, absent the regulation, *would have* reached \$1,610 — its own starting point lifted by the common trend. Its *actual* post premium was \$1,680. The gap between what happened and this counterfactual is the ATT:

$$
\widehat{\text{ATT}} = 1{,}680 - 1{,}610 = \$70,
$$

which is precisely the double difference. The $2\times 2$ arithmetic and the potential-outcomes story are the same calculation wearing two costumes: DiD imputes the treated unit's missing $Y(0)$ by **starting from its own pre level and adding the control group's change.** Everything now rides on whether that imputation is right — on whether the control's change is the right number to add. That is one assumption, and it has a name.

---

## 4.1.3 The parallel-trends assumption — stated carefully, and untestable

Here is the identifying assumption of difference-in-differences, the load-bearing wall. It is called **parallel trends** (or the *common-trends* assumption), and because it is the most important sentence in the chapter we state it in potential outcomes and then in English.

> **Parallel-trends assumption.** In the absence of treatment, the average *untreated* potential outcome of the treated group would have changed over time by the *same amount* as the control group's:
> $$
> \mathbb{E}\big[Y_{it}(0)\mid \text{treated, post}\big] - \mathbb{E}\big[Y_{it}(0)\mid \text{treated, pre}\big]
> \;=\;
> \mathbb{E}\big[Y_{it}(0)\mid \text{control, post}\big] - \mathbb{E}\big[Y_{it}(0)\mid \text{control, pre}\big].
> $$

In English: *had the regulation never happened, the treated state's premiums would have moved in lockstep with the control state's* — not at the same level, but with the same *trend*, the same change from before to after. The two lines on a premium-versus-time plot would have stayed parallel. This is exactly the assumption that lets us add the control's \$110 change to the treated state's pre level and call the result the treated state's counterfactual: it asserts the treated group's $Y(0)$ trend equals the control group's $Y(0)$ trend, so the control's observed change is a valid estimate of the treated's *unobserved* change.

Connect this to Week 3, because the comparison is illuminating and is the reason DiD is more credible than a plain regression with controls. Selection-on-observables (Chapter 3.1, 3.2) required that, after conditioning on $X$, the treated and control groups have the *same level* of untreated potential outcome — no unobserved confounder shifting one group's $Y(0)$ above the other's. That is a strong demand: it forbids any fixed unobserved difference between the groups. **Parallel trends asks for much less.** It *allows* the treated and control groups to differ in $Y(0)$ by a fixed amount — the treated state can be permanently \$300 more expensive for reasons we never observe — and that fixed difference does no harm, because differencing over time subtracts it away. What parallel trends forbids is a *differential trend*: the groups may start apart, but absent treatment they must *move together*. DiD relaxes "no unobserved difference in levels" down to "no unobserved difference in trends." That weaker demand is exactly why a natural experiment with a control group buys you something a kitchen-sink regression on a single cross-section cannot.

But — and this is the sentence to underline three times — **parallel trends is an assumption about a counterfactual, and the counterfactual is unobservable.** Look again at the boxed equation: every term on the left-hand side is $Y_{it}(0)$ for the *treated* group, including in the *post* period. The treated group's post-period $Y(0)$ is the world where the regulation never passed — the world that did not happen. We can never see it. So **the parallel-trends assumption can never be tested for the post-period.** No statistical test, no diagnostic, no amount of data will confirm that the treated state *would have* tracked the control after treatment, because "would have" never occurred. This is the same flavor of un-testability we met with conditional independence in Week 3: the identifying assumption lives in a counterfactual world, and data only reports the actual one. DiD does not escape the Fundamental Problem of Causal Inference; it makes a specific, often-plausible, but ultimately *unverifiable* bet about the missing counterfactual. The honest empirical-spec sentence is therefore: *"Identification rests on parallel trends — that absent the regulation, treated-state premiums would have moved like control-state premiums — which is assumed, not tested."*

When the assumption fails, you can see the wreckage in the logic even though you cannot see it in a test. Suppose the treated state was *already* on a steeper premium trajectory than the control — its fire risk was worsening faster — for reasons having nothing to do with the regulation. Then absent treatment its premiums would have risen by *more* than the control's \$110, say \$160. The true counterfactual is \$1,660, the true ATT is $1{,}680-1{,}660=\$20$, and our DiD estimate of \$70 is too big by \$50: we credited the regulation with \$50 of a divergence that was coming anyway. A differential pre-existing trend masquerades as a treatment effect. This is DiD's characteristic failure, and the next section is about the main tool for making it *less* likely — while being honest that the tool can never make it *impossible*.

---

## 4.1.4 The TWFE regression: DiD as one coefficient

The $2\times 2$ table is transparent but it does not scale, and it gives no standard error. Both problems are solved by writing DiD as a regression, which also gives us the object the rest of Week 4 builds on. For the canonical case — two groups, two periods — the difference-in-differences estimate is *exactly* the coefficient $\beta$ in the **two-way fixed-effects (TWFE)** regression:

$$
\boxed{\;Y_{it} = \alpha_i + \lambda_t + \beta\, D_{it} + \varepsilon_{it}\;}
$$

Read each piece against the cancellations from §4.1.1. The term $\alpha_i$ is a **unit fixed effect** — one intercept per unit (here, one per state). It absorbs everything about unit $i$ that is *constant over time*: the treated state's permanently higher price level, its fixed fire geography, its building stock. This is the regression doing, automatically, the "difference across groups" that removed the fixed group difference. (You met fixed effects as demeaning in Chapter 2.3; a unit dummy subtracts each unit's own time-average.) The term $\lambda_t$ is a **time fixed effect** — one intercept per period, *common to all units*. It absorbs everything that hits every unit equally in period $t$: the nationwide reinsurance shock, the common inflation. This is the regression doing the "difference across time" that removed the common time shock. With $\alpha_i$ soaking up fixed unit differences and $\lambda_t$ soaking up common time shocks, the *only* variation left for $D_{it}$ to explain is the thing that varies across both unit and time together — which, in the $2\times 2$ design, is exactly the treated state being treated in the post period.

The treatment indicator $D_{it}$ is $1$ in precisely one cell — treated unit, post period — and $0$ in the other three. Its coefficient $\beta$ is therefore the DiD estimate. You can verify the equivalence by plugging the four cell means into the model and solving; the algebra returns $\hat\beta = (\bar Y_T^{\,\text{post}} - \bar Y_T^{\,\text{pre}}) - (\bar Y_C^{\,\text{post}} - \bar Y_C^{\,\text{pre}})$, the same \$70. The fixed effects are not "controls" we threw in for good measure; they are the regression encoding of the two differencing operations, and $\beta$ is what survives both.

A point of vocabulary that matters for next chapter: the older way to write this same regression used explicit dummies rather than fixed effects. Let $\text{Treat}_i = 1$ for the treated unit, $\text{Post}_t = 1$ for the post period, and interact them:

$$
Y_{it} = \beta_0 + \beta_1 \text{Treat}_i + \beta_2 \text{Post}_t + \beta_3\,(\text{Treat}_i \times \text{Post}_t) + \varepsilon_{it}.
$$

Here $\beta_1$ is the fixed treated-versus-control gap (what $\alpha_i$ generalizes), $\beta_2$ is the common before-after change (what $\lambda_t$ generalizes), and **the interaction coefficient $\beta_3$ is the DiD estimate** — identical to $\beta$ above, identical to the \$70. The interaction term *is* $D_{it}$ in this two-group/two-period case: it equals $1$ only for the treated unit in the post period. The two specifications are the same model; the fixed-effects form $Y_{it}=\alpha_i+\lambda_t+\beta D_{it}+\varepsilon_{it}$ is just the one that keeps working when you have many units and many periods, because then you cannot write a single $\text{Treat}\times\text{Post}$ interaction but you *can* still write one intercept per unit and one per period. **Carry the boxed TWFE form forward**: it is the equation Chapter 4.2 will interrogate, because the clean interpretation we just gave it — "$\beta$ is the DiD / the ATT" — turns out to depend on the $2\times 2$ structure in a way that quietly fails when units adopt treatment at different times.

Stated in the empirical-spec discipline from the Conventions, Priya's design is: **outcome** = state-year average homeowner premium; **treatment** = the wildfire-pricing regulation, $D_{it}=1$ for the treated state in post years; **controls** = none needed beyond the fixed effects; **fixed effects** = state ($\alpha_i$) and year ($\lambda_t$); **clustering** = by state (see §4.1.6); **sample** = all states, all years in the window; **identifying assumption** = parallel trends, that absent the regulation the treated state's premiums would have moved like the controls'. Every DiD paper you read can — and should — be reduced to a spec exactly this explicit.

---

## 4.1.5 Event studies: letting the effect breathe, and looking at the trends

The $2\times 2$ collapses all of "before" into one number and all of "after" into one number. Real data usually has *several* periods on each side, and that extra structure is a gift: it lets us ask two questions the single $\beta$ cannot. First, *does the effect grow, fade, or jump?* — a regulation might bite slowly as contracts renew. Second, and more importantly, *were the treated and control groups already drifting apart before the treatment, in a way that should make us nervous about parallel trends?* The specification that answers both is the **event study**, also called the **dynamic** or **leads-and-lags** specification.

The idea is to replace the single treatment dummy with a *set* of dummies, one for each period relative to the moment treatment switched on. Define **event time** $k = t - t^*$, where $t^*$ is the period treatment begins; $k=0$ is the first treated period, $k=-1$ is the period just before, $k=+2$ is two periods after, and so on. Then estimate

$$
Y_{it} = \alpha_i + \lambda_t + \sum_{k \neq -1} \beta_k \, \mathbb{1}\{\,t - t_i^* = k\,\} + \varepsilon_{it},
$$

one coefficient $\beta_k$ for each event-time period. The dummies for $k<0$ are **leads** (periods *before* treatment); the dummies for $k\geq 0$ are **lags** (the treatment period and after). Each $\beta_k$ measures the treated-versus-control gap in event-period $k$, relative to a chosen baseline.

That baseline is the crucial normalization, and you must get it right: **we omit $k=-1$**, the period immediately before treatment, and interpret every $\beta_k$ as the gap *relative to that last pre-treatment period*. We have to drop one event-time dummy or the model is collinear with the fixed effects (the same reason you drop one category dummy to avoid the dummy trap). By convention we drop $k=-1$ so that $\beta_{-1}=0$ by construction, and every other coefficient reads as "how far has the treated-control gap moved away from where it stood the instant before treatment." This makes the plot easy to read: the period before treatment is pinned to zero, and everything is measured against it.

Now plot the $\hat\beta_k$ against event time $k$, with their confidence intervals — this is *the* canonical DiD figure, and reading it is a skill. Two regions, two purposes:

- **The lags ($k\geq 0$): the dynamic treatment effect.** These trace out how the regulation's effect evolves after it switches on. If $\hat\beta_0=\$30$, $\hat\beta_1=\$55$, $\hat\beta_2=\$70$, the effect builds over three years — perhaps as policies renew at the new rules — toward the \$70 the static $2\times 2$ would have averaged into a single blurry number. The event study un-blurs it. A flat post-period says the effect is immediate and permanent; a rising one says it accumulates; a spike that decays says it was transitory.

- **The leads ($k<0$): the pre-trend test.** This is the half of the plot that earns the event study its keep. Under parallel trends, the treated and control groups should *not* have been diverging *before* the treatment — there was no treatment yet to cause divergence. So the lead coefficients $\hat\beta_{-2}, \hat\beta_{-3}, \dots$ should all be statistically indistinguishable from zero, hugging the horizontal axis. If they do, the treated and control groups moved together in the pre-period — a *visible* parallel trend, at least before treatment. If instead the leads slope steadily upward toward $k=0$, that is a **pre-trend**: the groups were already pulling apart before anything happened, and the parallel-trends story is in serious trouble.

---

## 4.1.6 Pre-trends do not prove parallel trends

Now the caution, and it is a deep one that separates a sophisticated DiD reader from a naive one. It is tempting to look at flat lead coefficients and conclude "parallel trends holds — I tested it." **You did not, and it does not.** Two distinct problems sit underneath that overconfidence.

The first is logical, and it is the point §4.1.3 already insisted on: parallel trends is an assumption about the treated group's *post-period* counterfactual $Y(0)$ — a world that never happened. The pre-period leads are about the *pre-period*, a world that *did* happen and that you can therefore measure. Flat leads tell you the groups moved together *before* treatment. They are *consistent with* parallel trends continuing to hold afterward, and they are reassuring, but they are not the same statement. Something could have changed the treated group's trajectory at exactly the moment of treatment for reasons *other* than the treatment — a coincident shock, a policy bundled with the regulation — and the pre-trends would look pristine while the post-period assumption is false. **Pre-trends are a necessary-looking symptom, not the disease itself.** A clean pre-period is evidence, not proof, and you should present it as the former: "the leads are flat, which is consistent with parallel trends, but parallel trends in the post-period remains an untestable assumption."

The second problem is statistical, and it is more insidious because it can make a *bad* design look *good*: **pre-trend tests have low power.** Power is the probability of detecting a violation when one truly exists. With only a few pre-periods and noisy state-level data, the confidence intervals on the lead coefficients are wide — wide enough to contain both zero and an economically meaningful differential trend. So "I failed to reject zero pre-trend" can mean either "there is no pre-trend" or "there is a pre-trend, but my data is too noisy to see it." Those are very different worlds, and a wide, zero-spanning lead coefficient cannot tell them apart. The danger is asymmetric and exactly backwards from what you want: the *worst* datasets — small, noisy, few periods — are the ones *most* likely to hand you a falsely reassuring flat pre-trend, because they cannot detect anything. A well-powered test that finds flat leads is genuine evidence; an underpowered one that finds flat leads is mostly evidence that the test was weak. This is why modern practice does not stop at "the pre-trends look fine." It reports the confidence bands honestly (are they tight enough to rule out a worrying slope?), and increasingly supplements the eyeball test with formal **sensitivity analysis** — asking how large a violation of parallel trends would have to be to overturn the result, rather than pretending the violation is exactly zero. The slogan to carry: *pre-trends can refute parallel trends, but they can never confirm it.*

---

## 4.1.7 Inference: cluster by unit, and the lesson of Bertrand–Duflo–Mullainathan

We have an estimate, \$70, and a coefficient $\beta$ that delivers it from a regression. Now the question that sank Maya in Chapter 2.4 returns in a new guise: **what is its standard error?** Getting this wrong is, if anything, *easier* in DiD than anywhere else, and the canonical warning is one of the most cited methods papers in empirical economics.

**Bertrand, Duflo, and Mullainathan (2004)** asked a deceptively simple question: when researchers run DiD regressions on long panels — many units observed over many years — and report classical (or even heteroskedasticity-robust) standard errors, are those standard errors honest? They ran a brutal test. They took real data, invented *placebo* treatments that were assigned at random and therefore had *no true effect whatsoever*, and ran the standard DiD regression thousands of times. With honest standard errors, a placebo "effect" should be flagged as statistically significant at the 5% level about 5% of the time — that is what 5% significance *means*. Instead, the conventional standard errors flagged the fake effects as significant **up to 45% of the time.** Nearly half of pure-noise treatments looked "significant." The standard errors were catastrophically too small, and a generation of DiD results was, in consequence, far less certain than it claimed.

The culprit is exactly the disease of Chapter 2.4, §4–5: **serial correlation within units.** A state's premium this year is highly correlated with its premium last year — slow-moving local conditions persist. So a state's *residuals* are correlated across time. Recall the Moulton logic: when observations within a group are positively correlated, each one carries less fresh information than an independent observation would, so the *effective* number of observations is far below the nominal count. A DiD panel with 50 states over 20 years looks like 1,000 observations but, because of within-state persistence, contains far less independent information than 1,000. The treatment dummy $D_{it}$ is itself *highly persistent within a unit* — it is $0$ for years and then $1$ for years — which is precisely the regressor pattern (high within-cluster correlation $\rho_x$) that the Moulton factor $1+(n-1)\rho_x\rho_\varepsilon$ shows makes naive standard errors explode. Classical and even White/HC standard errors assume the within-state residuals are independent across years; they are not; the standard errors are too small; the t-stats lie.

The fix BDM landed on, and the default for DiD ever since, is the cluster-robust standard error from Chapter 2.4, **clustered by the unit of treatment** — here, by state:

$$
\text{cluster on the unit (state), allowing each unit's errors to be arbitrarily correlated across all its time periods.}
$$

This lets each state's residuals hold hands across all its years — the block-diagonal $\boldsymbol\Omega$ with one block per state spanning every period — which is exactly the serial-correlation structure BDM identified. In their placebo experiment, clustering by unit brought the rejection rate back down near the honest 5%. So the inference rule for DiD is short and non-negotiable: **cluster your standard errors by the unit at which treatment is assigned.** If the regulation is assigned at the state level, cluster by state; if treatment varies at the firm level, cluster by firm.

To feel the magnitude, take Priya's full panel (the many-state, many-year version she would use once we leave the toy $2\times 2$). Her estimated effect is \$70, and the three standard-error flavors come out, illustratively, like this:

| SE flavor | Std. error | t-stat | Honest? |
|-----------|-----------|--------|---------|
| Classical (OLS) | 14 | 5.0 | No — assumes $\sigma^2\mathbf{I}$, ignores within-state persistence |
| Robust (HC1) | 16 | 4.4 | No — fixes unequal variance but still ignores serial correlation |
| Clustered by state | 38 | 1.8 | Yes, if there are enough treated clusters |

The point estimate never moves off \$70 — Chapter 2.4's lesson exactly. What moves is the standard error, which more than doubles once we let each state's residuals correlate across years, dragging the t-stat from a triumphant $5.0$ to a sobering $1.8$. Classical and robust SEs both miss the serial correlation that BDM warned about; only the clustered SE tells the truth. (These magnitudes are illustrative; the live numbers are in nb4.1, where you reproduce the placebo experiment yourself.)

And now the same catch that haunted Chapter 2.4 returns with a vengeance, because it is *especially* acute in DiD. Cluster-robust standard errors are trustworthy only when you have *many* clusters — the rule of thumb was 30–50. But a great many DiD designs have *few* treated units. Priya's canonical case has exactly **one treated state.** Card and Krueger had essentially **one** treated jurisdiction (New Jersey) and one control (Pennsylvania). You cannot cluster your way out of having one treated cluster — there is simply not enough independent variation in the treatment to pin down its sampling distribution from the data, and the standard cluster-robust formula, the few-clusters $t$ correction, and even the wild cluster bootstrap (Cameron, Gelbach & Miller, 2008) all strain when the *treated* clusters are few. This is a genuine limitation of the clean two-state design, not a software setting you can flip: with one treated unit, the honest position is that your uncertainty is large and hard to quantify precisely, and you lean on placebo/permutation inference (assign the fake treatment to each control state in turn and ask how unusual your real estimate looks against that distribution) rather than a textbook t-test. The two-state natural experiment is wonderfully transparent and genuinely hard to do inference on — a tension worth sitting with, and one of several reasons researchers reach for *many* treated units, which is exactly the staggered-adoption setting of the next chapter.

---

## 4.1.8 The crack in the 2×2: where this chapter ends and 4.2 begins

Everything in this chapter has assumed a very particular world: **one treated group, one control group, one moment when treatment switches on.** Two groups, two (or a few) periods, a single clean before-and-after for a single clean treated unit. In that world, DiD is beautiful: the double difference equals the ATT under parallel trends, the TWFE coefficient $\beta$ in $Y_{it}=\alpha_i+\lambda_t+\beta D_{it}+\varepsilon_{it}$ recovers it exactly, the event study lets the effect breathe and lets us inspect the pre-trends, and clustering by unit (with enough units) gets the standard errors right.

But step into the world empirical finance usually hands you, and the clean story develops a crack. Suppose the wildfire regulation does not arrive in one state in one year. Suppose it rolls out across *many* states at *different* times — California in 2018, Colorado in 2020, Oregon in 2022 — a pattern called **staggered adoption**. Your instinct, and for two decades the entire profession's instinct, is to run the *same* TWFE regression $Y_{it}=\alpha_i+\lambda_t+\beta D_{it}+\varepsilon_{it}$, now with $D_{it}$ switching on at each state's own adoption date, and read $\beta$ as "the" average treatment effect. It seems like the obvious generalization: same equation, more switches.

It is a trap. When treatment timing varies across units, that single $\beta$ is no longer a clean average of treatment effects. The reason — which we develop carefully in Chapter 4.2 — is that the TWFE machine, in its hunt for "units that change treatment status," ends up using **already-treated units as controls for newly-treated units.** A state treated in 2018 becomes part of the implicit comparison group for a state treated in 2022, and if the 2018 state's effect is still evolving, that comparison is contaminated. Under some patterns of timing and dynamic effects, $\beta$ can be a strange, even *negatively* weighted average of the underlying effects — it can come out the wrong sign while every individual treatment effect is positive. The exact same equation that is *exactly right* in the $2\times 2$ becomes *misleading* the moment timing varies.

So hold onto the TWFE form $Y_{it}=\alpha_i+\lambda_t+\beta D_{it}+\varepsilon_{it}$ — but hold onto it the way you hold a tool whose limits you now know. In the canonical $2\times 2$ of this chapter it is exactly the difference-in-differences estimator, and $\beta$ is the ATT under parallel trends. The next chapter shows precisely how and why that interpretation breaks under staggered adoption, and what the modern estimators (which is to say, the last decade of econometrics) do instead. The double difference was the foundation; the staggered critique is what gets built on it.

---

## Your Turn

Open **`nb4.1`** (`notebooks/week-04/nb4.1-event-studies-parallel-trends.ipynb`), the difference-in-differences and event-study lab built on Priya's climate-insurance shock. Because it is a simulation, you again get to play God: you will generate state-year premiums with a known true treatment effect *and* a tunable pre-existing differential trend, so you can compare what DiD recovers to the truth it is chasing. You will (1) **build the $2\times 2$** — simulate one treated state and several controls with a fixed level difference and a common time shock, compute the four cell means and the double difference by hand, and confirm it matches the TWFE coefficient $\beta$ from `Y ~ C(state) + C(year) + treated_post`; (2) **run the event study** — replace the single dummy with leads-and-lags, normalize to $k=-1$, and plot $\hat\beta_k$ with confidence bands, reading the lags as the dynamic effect and the leads as the pre-trend check; (3) **break parallel trends on purpose** — dial up a differential pre-trend in the treated state and watch the lead coefficients tilt away from zero *and* the estimated treatment effect inflate, seeing exactly how a pre-existing divergence gets mislabeled as a treatment effect; (4) **stress the inference** — compare classical, HC1, and state-clustered standard errors on the panel and reproduce the spirit of Bertrand–Duflo–Mullainathan by running placebo (random) treatments and watching how often each standard-error flavor falsely declares significance.

**Check questions.**

1. Priya's $2\times 2$ has treated premiums of \$1,500 (before) and \$1,680 (after), control premiums of \$1,200 (before) and \$1,310 (after). (a) Compute the difference-in-differences estimate two ways — as (treated change) minus (control change), and as (after gap) minus (before gap) — and confirm they agree. (b) Write the counterfactual $\mathbb{E}[Y_{it}(0)\mid\text{treated, post}]$ that DiD imputes, and explain in one sentence which assumption justifies it. (c) Suppose the treated state was secretly on a steeper premium trend than the control even before the regulation. State whether the \$70 over- or under-states the true ATT, and why.

2. In the event-study specification $Y_{it}=\alpha_i+\lambda_t+\sum_{k\neq -1}\beta_k\mathbb{1}\{t-t_i^*=k\}+\varepsilon_{it}$: (a) why must we omit one event-time dummy, and why is $k=-1$ the conventional choice? (b) A classmate plots the leads, sees them all statistically indistinguishable from zero, and writes "this proves parallel trends holds." Give the *two* separate reasons (one logical, one statistical) this conclusion is unwarranted. (c) What would you need to see in the lead coefficients' confidence bands before you'd treat flat leads as genuinely reassuring rather than merely uninformative?

3. Bertrand, Duflo & Mullainathan (2004) found conventional DiD standard errors rejected *placebo* (no-effect) treatments far more than 5% of the time. (a) Name the property of the residuals that causes this, and explain via the Moulton intuition why it makes naive standard errors too small. (b) What standard-error flavor and clustering level fixes it, and why does the persistence of $D_{it}$ within a unit make this *especially* important in DiD? (c) Priya's design has exactly one treated state. Explain why clustering by state does not fully rescue her inference, and name one alternative she could use instead.
