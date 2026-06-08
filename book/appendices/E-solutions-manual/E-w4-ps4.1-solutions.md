# Solutions — PS 4.1 (The 2×2 Difference-in-Differences and Event-Study Construction)

**Problem set:** `book/weeks/week-04/ps4.1.md` (PS 4.1, Week 4).
**Chapter:** Ch 4.1 — Difference-in-Differences and Event Studies.

These are full worked solutions, not just answers. Notation follows `CONVENTIONS.md` and locks to Ch 4.1: the four cell means $\bar Y_T^{\,\text{pre}}, \bar Y_T^{\,\text{post}}, \bar Y_C^{\,\text{pre}}, \bar Y_C^{\,\text{post}}$; the double difference $\widehat{\text{DiD}}$; panel potential outcomes $Y_{it}(1), Y_{it}(0)$ with the observation rule $Y_{it}=D_{it}Y_{it}(1)+(1-D_{it})Y_{it}(0)$; the estimand $\text{ATT}=\mathbb{E}[Y_{it}(1)-Y_{it}(0)\mid\text{treated, post}]$; parallel trends; the TWFE regression $Y_{it}=\alpha_i+\lambda_t+\beta D_{it}+\varepsilon_{it}$ and its dummy-interaction equivalent; the event-study specification with the $k=-1$ normalization; pre-trend reading and its logical/statistical limits; and cluster-robust inference. Every numerical result here was confirmed in Python (NumPy four-cell arithmetic and a TWFE-equivalence check on a constructed two-period panel); verifying notes appear where useful. All premiums are annual dollars.

---

## Problem 1 — Compute and interpret a 2×2 DiD (14 points)

The four cells: $\bar Y_T^{\,\text{pre}}=1{,}620$, $\bar Y_T^{\,\text{post}}=1{,}845$, $\bar Y_C^{\,\text{pre}}=1{,}280$, $\bar Y_C^{\,\text{post}}=1{,}410$.

**(a) (4 pts)** The two contaminated one-way comparisons:

*Treated before-and-after change:* $\bar Y_T^{\,\text{post}}-\bar Y_T^{\,\text{pre}} = 1{,}845-1{,}620 = \$225.$ This confounds the regulation with **the passage of time** — everything else that moved premiums that year (worsening wildfires, costlier reinsurance, inflation in rebuilding costs) and would have happened regardless of the rule.

*Cross-sectional after-gap:* $\bar Y_T^{\,\text{post}}-\bar Y_C^{\,\text{post}} = 1{,}845-1{,}410 = \$435.$ This confounds the regulation with **the fixed difference between the states** — the treated state's own fire geography, building stock, and baseline price level, which made it more expensive than the control to begin with (a $\bar Y_T^{\,\text{pre}}-\bar Y_C^{\,\text{pre}}=1{,}620-1{,}280=\$340$ head start) for reasons having nothing to do with the rule.

**(b) (4 pts)** *Route 1 — (treated change) minus (control change), differencing over time first:*
$$
\widehat{\text{DiD}} = \big(\bar Y_T^{\,\text{post}}-\bar Y_T^{\,\text{pre}}\big) - \big(\bar Y_C^{\,\text{post}}-\bar Y_C^{\,\text{pre}}\big) = (1{,}845-1{,}620) - (1{,}410-1{,}280) = 225 - 130 = \$95.
$$

*Route 2 — (after-gap) minus (before-gap), differencing across groups first:*
$$
\widehat{\text{DiD}} = \big(\bar Y_T^{\,\text{post}}-\bar Y_C^{\,\text{post}}\big) - \big(\bar Y_T^{\,\text{pre}}-\bar Y_C^{\,\text{pre}}\big) = (1{,}845-1{,}410) - (1{,}620-1{,}280) = 435 - 340 = \$95. \quad\checkmark
$$

Both land on **\$95**, as they must — the double difference is symmetric. What each operation cancels: **differencing over time** (within a state) kills anything *fixed across the two periods* — the treated state's permanently higher price level and fire geography subtract out because they sit in both its "before" and its "after." **Differencing across groups** (within a period) kills anything that *hits both states equally* in that period — the nationwide reinsurance shock and common inflation subtract out because they sit in both rows.

**(c) (3 pts)** Of the \$225 rise in the treated state's premiums, DiD attributes **\$95 to the regulation** and **\$130 to "everything else"** — the latter being precisely the control state's change $\bar Y_C^{\,\text{post}}-\bar Y_C^{\,\text{pre}}=130$, our estimate of the common trend the treated state would have ridden anyway. The "everything else" \$130 is picking up forces such as **worsening wildfire frequency/severity nationwide** and **rising reinsurance costs** (also acceptable: economy-wide inflation in rebuilding/construction costs) — broad shocks that lifted premiums everywhere, treated and control alike.

**(d) (3 pts)** **Card and Krueger (1994)** studied fast-food employment around a minimum-wage change. The **treated jurisdiction was New Jersey** (which raised its minimum wage in 1992); the **control was Pennsylvania** (which did not); the **treatment was the minimum-wage increase**; and the cells held **average fast-food employment** (they surveyed fast-food restaurants in both states before and after). The result — that employment did *not* fall, contrary to the textbook competitive prediction — was argued over on the *assumption* rather than the arithmetic because the $2\times 2$ design was clean and the double difference was transparent; the only place left to push back was whether New Jersey's employment *would have* tracked Pennsylvania's absent the hike, i.e., whether parallel trends held. (Arguing with the assumption rather than the arithmetic is exactly the right thing to do, which is why the study became canonical.)

---

## Problem 2 — The double difference in potential outcomes, and parallel trends (20 points)

**(a) (5 pts)** The ATT is the effect of the regulation on the state that actually got it, in the period it had it:
$$
\text{ATT} = \mathbb{E}\big[\,Y_{it}(1)-Y_{it}(0)\;\big|\;\text{treated, post}\,\big].
$$
The first term, $\mathbb{E}[Y_{it}(1)\mid\text{treated, post}]$, is **observed**: by the observation rule the treated state's post cell *is* its treated potential outcome, $\bar Y_T^{\,\text{post}}=\$1{,}845$. The second term, $\mathbb{E}[Y_{it}(0)\mid\text{treated, post}]$, is the **missing counterfactual** — what the treated state's premium would have been in the post period *had the regulation never passed*. It is unobservable because it lives in a world that did not happen: the regulation *did* pass, so the treated state's untreated post-period outcome was never realized. This is the Fundamental Problem of Causal Inference carried into the panel.

**(b) (5 pts)** DiD imputes the missing counterfactual by taking the treated state's own pre level and letting it grow by the *control group's* observed change:
$$
\widehat{\mathbb{E}[Y_{it}(0)\mid\text{treated, post}]} = \bar Y_T^{\,\text{pre}} + \big(\bar Y_C^{\,\text{post}}-\bar Y_C^{\,\text{pre}}\big) = 1{,}620 + 130 = \$1{,}750.
$$
Then the ATT is the actual post outcome minus this imputed counterfactual:
$$
\widehat{\text{ATT}} = \bar Y_T^{\,\text{post}} - 1{,}750 = 1{,}845 - 1{,}750 = \$95,
$$
which reproduces the Problem 1 double difference. $\checkmark$ Contrast with the two *wrong* imputations: the **naive before-after** comparison uses $\bar Y_T^{\,\text{pre}}=\$1{,}620$ as the counterfactual (assuming the treated state's premium would have been *flat* — false, premiums were rising everywhere), and the **cross-sectional** comparison uses $\bar Y_C^{\,\text{post}}=\$1{,}410$ (assuming the two states would have had the *same level* — false, the treated state was \$340 higher to begin with). DiD's imputation is smarter than both: it keeps the treated state's level *and* lets it ride the common trend.

**(c) (6 pts)** **Parallel-trends assumption, formal:** in the absence of treatment, the treated group's average untreated potential outcome would have changed over time by the same amount as the control group's,
$$
\underbrace{\mathbb{E}[Y_{it}(0)\mid\text{treated, post}] - \mathbb{E}[Y_{it}(0)\mid\text{treated, pre}]}_{\text{treated group's counterfactual change}}
=
\underbrace{\mathbb{E}[Y_{it}(0)\mid\text{control, post}] - \mathbb{E}[Y_{it}(0)\mid\text{control, pre}]}_{\text{control group's change}}.
$$
**In English:** had the regulation never happened, the treated state's premiums would have moved in lockstep with the control state's — same trend (same before-to-after change), not necessarily the same level.

**Why it is untestable for the post period:** look at the left-hand side. The term $\mathbb{E}[Y_{it}(0)\mid\text{treated, post}]$ — the treated group's untreated potential outcome *in the post period* — is the very missing counterfactual from part (a). It is the world in which the regulation never passed, which did not occur. No data, no diagnostic, no sample size can reveal it, because "would have" never happened. So the equation that defines parallel trends contains a term we can never measure, and any "test" of it for the post period is impossible in principle. (The control-side terms and the treated *pre* term are all observable; it is the single treated-post $Y(0)$ term that sinks testability.) The honest empirical-spec sentence: identification rests on parallel trends, which is *assumed, not tested*.

**(d) (4 pts)** Selection-on-observables forbade any fixed unobserved difference in $Y(0)$ *levels* between treated and control (after conditioning on $X$). Parallel trends **allows exactly that**: the treated state may be permanently \$340 more expensive — for unobserved reasons we never name — and it does no harm, because differencing over time subtracts the fixed difference away. What parallel trends **still forbids** is a *differential trend*: the groups may start apart, but absent treatment they must *move together* (same change over time). So DiD relaxes "no unobserved difference in levels" down to the weaker "no unobserved difference in trends," and *that* weaker demand is why a natural experiment with a control group can beat a single-cross-section regression — the cross-section must defend the much stronger level assumption, which a permanently-higher-risk treated state flatly violates, whereas DiD only needs the two states' premiums to have been drifting in parallel.

---

## Problem 3 — Build the TWFE regression and say what the fixed effects absorb (16 points)

**(a) (5 pts)** The two-way fixed-effects regression:
$$
Y_{it} = \alpha_i + \lambda_t + \beta\, D_{it} + \varepsilon_{it}.
$$
In Priya's terms: $Y_{it}$ is **state $i$'s average homeowner premium in year $t$**; $\alpha_i$ is the **state fixed effect** (one intercept per state, capturing that state's permanent price level); $\lambda_t$ is the **year fixed effect** (one intercept per year, common to all states, capturing nationwide conditions that year); $D_{it}$ is the **treatment indicator** ($1$ when state $i$ is under the wildfire-pricing rule in year $t$); and $\beta$ is the DiD estimate — the regulation's effect. In the $2\times 2$, $D_{it}=1$ in **exactly one cell: the treated state in the post period**, and $0$ in the other three.

**(b) (5 pts)** The **state fixed effects $\alpha_i$** absorb everything about a state that is *constant over time* — its permanently higher price level, fixed fire geography, building stock. This is the regression performing the **"difference across groups"** that removed the *fixed group difference*. The **year fixed effects $\lambda_t$** absorb everything that *hits every state equally* in a given year — the nationwide reinsurance shock, common inflation. This is the regression performing the **"difference across time"** that removed the *common time shock*. Once both are in, the **only variation left** for $D_{it}$ to explain is the part that varies across *both* state and year together — which, in the $2\times 2$, is precisely the treated state being treated in the post period. That leftover is the regulation's effect because every other source of movement (fixed state differences, common year shocks) has already been soaked up by the two sets of dummies.

**(c) (3 pts)** The **interaction coefficient $\beta_3$** is the DiD estimate (identical to $\beta$ above, identical to the \$95). The interaction $\text{Treat}_i\times\text{Post}_t$ *is* the same regressor as $D_{it}$ here because it equals $1$ only when both $\text{Treat}_i=1$ and $\text{Post}_t=1$ — i.e., only for the treated state in the post period, which is exactly the one cell where $D_{it}=1$. We carry the **fixed-effects form** forward (not the dummy form) because with many states and many years you cannot write a single $\text{Treat}\times\text{Post}$ interaction, but you *can* still write one intercept per state and one per year — the FE notation scales, the single-interaction notation does not.

**(d) (3 pts)** Calling $\alpha_i$ and $\lambda_t$ "controls" in the Week-2 sense is misleading because Week-2 controls are *covariates* you add to hold a confounding variable fixed; the fixed effects are not variables Priya measured at all. They are the algebraic machinery that **demeans the data** — $\alpha_i$ subtracts each state's own time-average, $\lambda_t$ subtracts each year's cross-state average (the within transformation from Ch 2.3) — so that by the time $\beta$ is estimated, the regression is working on data from which the fixed state level and the common year level have *already been swept out*. They *are* the two differencing operations of the $2\times 2$, written as a regression; $\beta$ is simply what survives both sweeps.

---

## Problem 4 — Construct and read an event study (18 points)

**(a) (5 pts)** With event time $k=t-t_i^*$ ($t_i^*$ = first treated year for unit $i$), the event-study / leads-and-lags specification is
$$
Y_{it} = \alpha_i + \lambda_t + \sum_{k\neq -1} \beta_k\,\mathbb{1}\{\,t - t_i^* = k\,\} + \varepsilon_{it}.
$$
The dummies for $k<0$ are **leads** (periods *before* treatment); the dummies for $k\ge 0$ are **lags** (the treatment year and after). The two regions serve distinct purposes: the **lags trace the dynamic treatment effect** (how the regulation's effect evolves once it switches on), while the **leads serve as the pre-trend check** (under parallel trends the groups should not have been diverging before any treatment existed, so the leads should hug zero).

**(b) (4 pts)** By convention we omit **$k=-1$**, the period immediately before treatment. We *must* omit one event-time dummy because a full set of them, alongside the unit and time fixed effects, is **perfectly collinear** — the dummies would span the same space the fixed effects already occupy (the dummy-variable trap: you cannot include every category and an intercept structure simultaneously). Dropping $k=-1$ sets $\beta_{-1}=0$ *by construction*, so every remaining $\hat\beta_k$ reads as the treated-versus-control gap in event-period $k$ **relative to the last pre-treatment period** ($k=-1$) — "how far has the gap moved from where it stood the instant before treatment." This pins the period-before to zero and makes the plot easy to read.

**(c) (5 pts)** Reading $\{\hat\beta_{-3},\dots,\hat\beta_2\} = \{4,-3,0,60,120,180\}$:

(i) **Lags ($k\ge 0$):** $\hat\beta_0=\$60$, $\hat\beta_1=\$120$, $\hat\beta_2=\$180$ — the effect is **building**, not immediate. The regulation bites gradually (plausibly as policies renew at the new pricing rules), accumulating from \$60 in the first treated year toward \$180 two years out. It is neither an immediate-and-permanent jump (which would show as a flat post-period) nor a transitory spike that decays.

(ii) **Leads ($k<0$):** $\hat\beta_{-3}=\$4$, $\hat\beta_{-2}=-\$3$ (and $\hat\beta_{-1}=0$ by construction) — these are tiny, scattered around zero with no slope. They are **consistent with parallel trends**: the treated and control states moved together in the pre-period, with no divergence before the rule existed. (Consistent with, not proof of — see Problem 5.)

(iii) The static $2\times 2$ would have collapsed the three lags into a single $\beta$ — roughly their average, a blurry \$120-ish number. The event study **un-blurs the dynamics**: it shows the effect is *growing* over time rather than constant, information the single coefficient destroys by averaging.

**(d) (4 pts)** The new leads $\{\hat\beta_{-3},\hat\beta_{-2}\} = \{-90,-55\}$ are not scattered around zero — they slope **steadily upward toward $k=0$** (from $-90$ to $-55$ to $0$, a rise of roughly \$45 per period). That is a **pre-trend**: the two states were *already pulling apart* before the regulation existed, so something other than the treatment was driving their relative premiums up. This poisons the post-period coefficients because if you extend the pre-trend line forward — the gap was rising about \$45–55 per period before treatment — a good chunk of the post-period $\hat\beta_0=40,\hat\beta_1=60,\hat\beta_2=85$ is just that pre-existing divergence *continuing*, mislabeled as a treatment effect. The parallel-trends story is in serious trouble, and the honest reading is that the "effect" here is confounded with a differential trend that was coming anyway.

---

## Problem 5 — Why flat leads do not *prove* parallel trends (16 points)

**(a) (5 pts) The logical problem.** (i) The leads are about the **pre-period** — a world that *did* happen and that Priya can therefore measure. The parallel-trends assumption that matters for identification is about the treated group's **post-period** counterfactual $Y_{it}(0)$ — a world that *never happened*. These are different statements about different periods, so confirming the first does not establish the second. (ii) A concrete scenario: suppose at the exact moment of the regulation, a *separate* shock hit only the treated state — say a large insurer exited that state's market, or a coincident state tax on policies took effect — bundled in time with the rule but distinct from it. The pre-period leads would look pristine (no divergence before $t^*$), yet the treated state's post-period premiums would have risen *even absent the regulation* because of the coincident shock, so parallel trends fails in the post period despite flat leads. **Slogan:** *pre-trends can refute parallel trends, but they can never confirm it* — a clean pre-period is evidence, not proof.

**(b) (5 pts) The statistical problem (low power).** **Power** is the probability of *detecting* a pre-trend violation when one genuinely exists. On a small, noisy, few-period state panel, the lead coefficients have wide standard errors, so their confidence intervals are wide — wide enough to contain both zero and an economically meaningful differential trend. "I failed to reject zero pre-trend" then has two utterly different meanings: "there is no pre-trend" *or* "there is one, but my data is too noisy to see it," and a wide interval cannot tell them apart. The asymmetry is **exactly backwards from what you want**: the *worst* datasets — small, noisy, few periods — are the ones *most* likely to produce a falsely reassuring flat pre-trend, precisely because they cannot detect anything at all. A well-powered test that finds flat leads is genuine evidence; an underpowered one that finds flat leads is mostly evidence that the test was weak.

**(c) (6 pts) Making it concrete.** $\hat\beta_{-2}=\$40$, clustered $\text{SE}=\$35$.

(i) Approximate 95% CI:
$$
40 \pm 1.96(35) = 40 \pm 68.6 = [\,-28.6,\ 108.6\,].
$$
It **does contain zero** (since $-28.6 < 0 < 108.6$), so Priya "fails to reject" a zero pre-trend at 5%.

(ii) The same interval *also* contains **\$100** (since $-28.6 < 100 < 108.6$). That one confidence interval contains **both zero and a \$100 violation** means the data is consistent both with "no pre-trend at all" and with "a worrying, economically meaningful pre-trend" — the test simply cannot distinguish them. Priya **cannot rule out** the second story ("there is a pre-trend, but the data is too noisy to see it"); failing to reject zero here is *uninformative*, not reassuring. The estimate is too imprecise to license any conclusion.

(iii) Before treating the flat lead as genuinely reassuring, Priya would need the confidence band to be **tight enough to exclude an economically meaningful differential trend** — e.g., an interval that ruled out the \$100 violation (and ideally hugged zero), so that "flat" means "demonstrably small" rather than "could be anything." Beyond the eyeball test, the chapter recommends she add **formal sensitivity analysis** — asking *how large* a parallel-trends violation would have to be to overturn her result, rather than pretending the violation is exactly zero.

---

## Problem 6 — Inference: cluster by unit, and the BDM warning (16 points)

**(a) (4 pts)** With $\widehat\beta=\$225$ fixed and $t=\widehat\beta/\text{SE}$:

| SE flavor | Std. error | $t$ |
|-----------|:---------:|:---:|
| Classical (OLS) | \$22 | $225/22 \approx 10.23$ |
| Robust (HC1) | \$26 | $225/26 \approx 8.65$ |
| Clustered by state | \$95 | $225/95 \approx 2.37$ |

The point estimate is identical across all three rows. The general principle (from Ch 2.4): **the choice of standard-error flavor changes the *standard error* — and hence the $t$-stat, the $p$-value, and the confidence interval — but never the point estimate $\widehat\beta$ itself.** Here $\widehat\beta=\$225$ regardless; what moves is how *certain* we are about it, and the honest $t$ drops from a triumphant $10.23$ to a sobering $2.37$ once we let each state's residuals correlate across years.

**(b) (5 pts)** **Bertrand, Duflo & Mullainathan (2004)** took real panel data, **assigned *placebo* treatments at random** (fake interventions with *no true effect whatsoever*), and ran the standard DiD regression thousands of times. With honest standard errors, such pure-noise "effects" should be flagged significant at the 5% level **about 5% of the time** — that is what 5% significance means. Instead, conventional standard errors flagged the fake effects as significant **up to ~45% of the time** — nearly half of pure-noise treatments looked "significant," so the SEs were catastrophically too small. The culprit is **serial correlation within units**: a state's premium (and hence its *residual*) this year is highly correlated with last year's, because slow-moving local conditions persist. By the **Moulton intuition**, when observations within a group are positively correlated, each carries *less fresh information* than an independent draw would, so the *effective* sample size is far below the nominal count; a "1,000-observation" panel (50 states × 20 years) holds far less independent information than 1,000. Classical/robust formulas assume the within-state residuals are independent across years and so divide by the inflated nominal $N$, producing a standard error that is too small and a $t$-stat that lies.

**(c) (4 pts)** The fix is the **cluster-robust standard error, clustered by the unit of treatment — here, by state** (each state's errors allowed to be arbitrarily correlated across all its years; a block-diagonal $\boldsymbol\Omega$ with one block per state). This is *especially* acute in DiD because the treatment indicator $D_{it}$ is itself **highly persistent within a unit** — it is $0$ for years and then $1$ for years — i.e., high within-cluster regressor correlation $\rho_x$. The Moulton factor $1+(n-1)\rho_x\rho_\varepsilon$ shows that when *both* the regressor ($\rho_x$, high here because $D_{it}$ barely varies within a state) *and* the residuals ($\rho_\varepsilon$, high because premiums persist) are strongly within-cluster-correlated, the naive standard error is understated by a large multiplicative factor. So DiD combines exactly the two ingredients that make naive SEs explode, which is why clustering by the treatment unit is the non-negotiable default.

**(d) (3 pts)** With exactly **one treated state**, clustering by state cannot rescue inference because the cluster-robust formula needs *many* clusters — and, more pointedly, *many treated* clusters — to pin down the treatment's sampling distribution from the data. There simply is not enough independent variation in the treatment (one switch, in one unit) for the standard cluster-robust formula, the few-clusters $t$ correction, or even the wild cluster bootstrap (Cameron, Gelbach & Miller, 2008) to estimate its variability reliably. This is a *genuine limitation of the two-state design*, not a software setting to flip. One alternative: **placebo / permutation (randomization) inference** — assign the fake treatment to each control state in turn, compute the placebo estimate each time, and ask how unusual Priya's real \$225 looks against that distribution of placebo effects. (This is also why researchers reach for *many* treated units, the staggered-adoption setting of Ch 4.2.)

---

*All numerical answers verified in Python. Key results: P1 $\widehat{\text{DiD}}=(1845-1620)-(1410-1280)=225-130=\$95$, identical via after-gap minus before-gap $(1845-1410)-(1620-1280)=435-340=\$95$; treated before-after \$225, cross-sectional after-gap \$435; \$95 to the rule, \$130 to common trend. P2 imputed counterfactual $\bar Y_T^{\,\text{pre}}+130=\$1{,}750$, ATT $=1845-1750=\$95$. P4 lags $\{60,120,180\}$ build; alt-state leads $\{-90,-55\}$ slope up = pre-trend. P5(c) 95% CI $40\pm1.96(35)=[-28.6,\,108.6]$, contains both 0 and 100. P6(a) $t$-stats $225/22\approx10.23$, $225/26\approx8.65$, $225/95\approx2.37$. Citations by name only, per chapter: Card–Krueger (1994), Bertrand–Duflo–Mullainathan (2004), Cameron–Gelbach–Miller (2008). All premiums illustrative/constructed; no fabricated empirical estimates.*
