# PS 4.1 — The 2×2 Difference-in-Differences and Event-Study Construction

**Course:** ASSIP 2026 · 8-Week Empirical Finance Track · Week 4 · Problem Set 4.1
**Covers:** Ch 4.1 (Difference-in-Differences and Event Studies).
**Methods allowed:** only what is built through Ch 4.1 — the $2\times 2$ table of four cell means $\bar Y_T^{\,\text{pre}}, \bar Y_T^{\,\text{post}}, \bar Y_C^{\,\text{pre}}, \bar Y_C^{\,\text{post}}$; the double difference $\widehat{\text{DiD}} = (\bar Y_T^{\,\text{post}}-\bar Y_T^{\,\text{pre}}) - (\bar Y_C^{\,\text{post}}-\bar Y_C^{\,\text{pre}})$ and its symmetric (after-gap minus before-gap) form; panel potential outcomes $Y_{it}(1), Y_{it}(0)$ with the observation rule $Y_{it}=D_{it}Y_{it}(1)+(1-D_{it})Y_{it}(0)$; the estimand $\text{ATT}=\mathbb{E}[Y_{it}(1)-Y_{it}(0)\mid \text{treated, post}]$; the **parallel-trends** assumption and the fact that it is untestable for the post period; the two-way fixed-effects (TWFE) regression $Y_{it}=\alpha_i+\lambda_t+\beta D_{it}+\varepsilon_{it}$ and the equivalent $\beta_0+\beta_1\text{Treat}_i+\beta_2\text{Post}_t+\beta_3(\text{Treat}_i\times\text{Post}_t)$ form; the event-study / leads-and-lags specification $Y_{it}=\alpha_i+\lambda_t+\sum_{k\neq-1}\beta_k\mathbb{1}\{t-t_i^*=k\}+\varepsilon_{it}$ with the $k=-1$ normalization; pre-trend reading and its two limits (logical: leads are pre-period; statistical: low power); and cluster-robust inference (cluster by the unit of treatment), with the Bertrand–Duflo–Mullainathan (2004) serial-correlation warning and the few-treated-clusters problem. You do **not** need staggered adoption, the TWFE decomposition weights, or the modern heterogeneity-robust estimators — those are Ch 4.2.

**Total: 100 points.** Point values are stated per problem. Show your reasoning — a correct final number with no derivation earns roughly half credit, because the reasoning *is* the skill we are grading. Solutions are in Appendix E (`E-w4-ps4.1-solutions.md`); try every part before you look.

A note on the difficulty curve: Problem 1 is a five-minute warm-up that gets the four-cell arithmetic into your fingers. Problem 2 is the conceptual core — translating the double difference into potential outcomes and pinning down the one assumption that turns it into a causal effect. Problem 3 makes you *build* the TWFE regression and say what each fixed effect erases. Problem 4 asks you to construct an event study from scratch and read it. Problems 5 and 6 are the hardest and most important: 5 is the pre-trend reasoning problem that separates a sophisticated DiD reader from a naive one, and 6 is the inference problem where getting the standard error wrong is easier than anywhere else you have been. Throughout, we stay with **Priya's climate-insurance shock**: a state changes how home insurers may price wildfire risk on January 1 of a particular year, and Priya has state-year average homeowner premiums for several years on each side. All dollar figures are annual premiums.

---

## Problem 1 — Compute and interpret a 2×2 DiD (14 points)

Priya pulls a clean four-cell table. One **treated** state changed its wildfire-pricing rule; one **control** state left its rules alone. The cells are average annual homeowner premiums, in dollars, collapsed into one "before" number and one "after" number per state.

|                | Before  | After   |
|----------------|---------|---------|
| **Treated**    | \$1{,}620 | \$1{,}845 |
| **Control**    | \$1{,}280 | \$1{,}410 |

**(a) (4 pts)** Write out the two *contaminated* one-way comparisons in numbers: the treated state's **before-and-after** change, and the treated-versus-control **cross-sectional** gap *in the after period*. State in one sentence each what confound is baked into each of these two comparisons (i.e., what besides the regulation each one is secretly measuring).

**(b) (4 pts)** Compute the difference-in-differences estimate **two ways** — first as (treated change) minus (control change), then as (after-gap) minus (before-gap) — and confirm the two routes land on the same number. State, in one sentence each, what gets *cancelled* by each of the two differencing operations.

**(c) (3 pts)** Of the \$225 by which the treated state's premiums rose, how many dollars does DiD attribute to the regulation, and how many to "everything else"? Name two concrete forces that the "everything else" component is picking up in Priya's setting.

**(d) (3 pts)** This is the canonical empirical application. **Card and Krueger (1994)** ran exactly this $2\times 2$, but with a different outcome in the cells and a different treatment. Name their treated jurisdiction, their control jurisdiction, the treatment, and the outcome they put in the four cells — and in one sentence say why their result was argued over on the grounds of the *assumption* rather than the *arithmetic*.

---

## Problem 2 — The double difference in potential outcomes, and parallel trends (20 points)

Stay with the exact table from Problem 1.

**(a) (5 pts)** Write the estimand DiD targets, the ATT, in panel potential-outcomes notation, being explicit about the conditioning ("treated, post"). Identify which of the two terms in the ATT is *observed* (and equal to which cell mean) and which is the *missing counterfactual*. Explain in one sentence why that second term is, in principle, unobservable — i.e., which world it lives in.

**(b) (5 pts)** Show how DiD *imputes* the missing counterfactual $\mathbb{E}[Y_{it}(0)\mid\text{treated, post}]$ from the four cells: write the imputation formula in symbols, plug in Priya's numbers to get a dollar value, and then confirm that $\bar Y_T^{\,\text{post}}$ minus this imputed counterfactual reproduces your DiD estimate from Problem 1. In one sentence, contrast this imputation with the *two wrong* imputations — the one the naive before-after comparison uses, and the one the cross-sectional comparison uses.

**(c) (6 pts)** State the **parallel-trends assumption** twice: once in potential-outcomes notation (the formal statement about $Y_{it}(0)$ for the treated and control groups), and once in one plain-English sentence about Priya's premiums. Then explain — referencing your formal statement — **why the assumption can never be tested for the post period**. Your explanation must name *which specific term* in the formal statement is the unobservable one and *why* (which counterfactual world it sits in).

**(d) (4 pts)** Connect parallel trends to Week 3. Selection-on-observables (Ch 3.1–3.2) demanded that treated and control groups have the same untreated-outcome *level* (after conditioning on $X$). Parallel trends demands less. State precisely what parallel trends *allows* that selection-on-observables forbids, and what it *still* forbids — and explain in one sentence why this is the reason a DiD design with a control group can be more credible than a kitchen-sink regression on a single cross-section.

---

## Problem 3 — Build the TWFE regression and say what the fixed effects absorb (16 points)

**(a) (5 pts)** Write down the two-way fixed-effects regression for Priya's $2\times 2$ design, $Y_{it}=\alpha_i+\lambda_t+\beta D_{it}+\varepsilon_{it}$, and define each of the four symbols ($\alpha_i$, $\lambda_t$, $\beta$, $D_{it}$) in one phrase, *in Priya's terms* (states, years, premiums). State exactly which of the four cells of the table has $D_{it}=1$.

**(b) (5 pts)** Explain what the unit fixed effects $\alpha_i$ absorb and what the time fixed effects $\lambda_t$ absorb, mapping each onto the corresponding *differencing operation* from the $2\times 2$ (which one removes the "fixed group difference," which one removes the "common time shock"). Then state, in one sentence, what variation is *left over* for $D_{it}$ to explain once both sets of fixed effects have done their work — and why that leftover variation is exactly the regulation's effect.

**(c) (3 pts)** A classmate prefers the dummy-interaction form $Y_{it}=\beta_0+\beta_1\text{Treat}_i+\beta_2\text{Post}_t+\beta_3(\text{Treat}_i\times\text{Post}_t)+\varepsilon_{it}$. State which coefficient is the DiD estimate, and explain in one sentence why $\text{Treat}_i\times\text{Post}_t$ is the *same regressor* as $D_{it}$ in this two-group/two-period world. Then say in one sentence why the fixed-effects form, not the dummy form, is the one to carry forward to settings with many states and many years.

**(d) (3 pts)** The chapter calls the fixed effects "the regression encoding of the two differencing operations," **not** "controls we threw in for good measure." Explain the distinction in two or three sentences: why is it misleading to describe $\alpha_i$ and $\lambda_t$ as control variables in the Week-2 sense, and what do they actually *do* to the data before $\beta$ is estimated?

---

## Problem 4 — Construct and read an event study (18 points)

The $2\times 2$ blurs all of "before" into one number and all of "after" into one. Priya now has *six* years of data: three before the regulation and three after. She wants to (i) let the effect evolve year by year and (ii) inspect whether the two groups were already drifting apart before the rule. Let $t^*$ be the first treated year, and define **event time** $k=t-t^*$.

**(a) (5 pts)** Write down the event-study (leads-and-lags) specification for Priya's panel, in the chapter's notation. State which event-time periods are **leads** and which are **lags**, and explain in one sentence the distinct purpose each region of the plot serves.

**(b) (4 pts)** The specification omits one event-time dummy. State **which** $k$ is omitted by convention, give the technical reason we *must* omit one (what goes wrong if we keep them all alongside the fixed effects), and explain what each remaining $\hat\beta_k$ then measures — "the gap relative to *what*?"

**(c) (5 pts)** Priya estimates the following coefficients (dollars; $\hat\beta_{-1}=0$ by construction):

| $k$ | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| $\hat\beta_k$ | $4$ | $-3$ | $0$ | $60$ | $120$ | $180$ |

Read this plot in words. (i) Describe what the **lags** ($k\ge 0$) say about the dynamics of the regulation's effect — is it immediate, building, or fading? (ii) Describe what the **leads** ($k<0$) say, and state whether they are *consistent with* parallel trends. (iii) The static $2\times 2$ would have averaged the lags into a single $\beta$. In one sentence, say what information the event study recovers that the single $\beta$ destroys.

**(d) (4 pts)** Now Priya is handed a *different* set of estimates from a *different* treated state, where the leads slope steadily upward: $\hat\beta_{-3}=-90,\ \hat\beta_{-2}=-55,\ \hat\beta_{-1}=0,\ \hat\beta_0=40,\ \hat\beta_1=60,\ \hat\beta_2=85$. Explain in two or three sentences what this lead pattern signals about parallel trends, and why it should make you distrust the post-period coefficients $\hat\beta_0,\hat\beta_1,\hat\beta_2$ as estimates of the regulation's effect. (Hint: extend the pre-trend line forward.)

---

## Problem 5 — Why flat leads do not *prove* parallel trends (16 points)

This is the conceptual heart of the sheet, and it has no arithmetic in parts (a) and (b). A classmate, looking at the flat leads of Problem 4(c), writes: *"The lead coefficients are all statistically indistinguishable from zero, so I have tested parallel trends and it holds."* Both halves of that sentence are wrong, for two distinct reasons.

**(a) (5 pts) The logical problem.** Explain why flat leads, even if measured perfectly, are *not the same statement* as parallel trends holding in the post period. Your answer must (i) say which period the leads are about and which period the parallel-trends assumption is about, and (ii) give one concrete scenario in Priya's setting in which the leads would look pristine yet the post-period assumption is nonetheless false. Conclude with the chapter's slogan about what pre-trends can and cannot do.

**(b) (5 pts) The statistical problem (low power).** Define statistical power in this context in one sentence. Then explain why a pre-trend test on a small, noisy, few-period state panel tends to have *low* power, and why this makes a "flat" pre-trend dangerously *reassuring* in exactly the wrong cases. State the asymmetry precisely: which datasets are *most* likely to hand you a falsely comforting flat pre-trend, and why that is "exactly backwards from what you want."

**(c) (6 pts) Making it concrete.** Priya's lead coefficient at $k=-2$ comes back as $\hat\beta_{-2}=\$40$ with a clustered standard error of \$35.
&nbsp;&nbsp;(i) Construct the approximate 95% confidence interval ($\hat\beta_{-2}\pm 1.96\,\text{SE}$) and state whether it contains zero.
&nbsp;&nbsp;(ii) A worrying differential pre-trend in this setting would be on the order of \$100. State whether the same confidence interval *also* contains \$100, and explain in two sentences what it means that one interval contains *both* zero and an economically meaningful violation. Which of "there is no pre-trend" versus "there is a pre-trend, but the data is too noisy to see it" can Priya rule out here?
&nbsp;&nbsp;(iii) In one sentence, state what Priya would need to see in this confidence band before she could treat the flat lead as genuinely reassuring rather than merely uninformative, and name the modern practice (beyond the eyeball test) the chapter recommends she add.

---

## Problem 6 — Inference: cluster by unit, and the BDM warning (16 points)

Now the standard error, where DiD makes it *easier* than anywhere to fool yourself. Priya scales up to her full panel — 50 states observed over 20 years — and estimates the regulation's effect at $\widehat\beta=\$225$. Her software reports three flavors of standard error:

| SE flavor | Std. error | $t = \widehat\beta/\text{SE}$ | |
|-----------|:---------:|:---:|---|
| Classical (OLS) | \$22 | ? | |
| Robust (HC1) | \$26 | ? | |
| Clustered by state | \$95 | ? | |

**(a) (4 pts)** Fill in the three $t$-statistics. Note that the point estimate \$225 is *identical* across all three rows — only the SE moves. State in one sentence the general principle (carried from Ch 2.4) about *what* the choice of standard-error flavor does and does not change.

**(b) (5 pts)** **Bertrand, Duflo, and Mullainathan (2004)** ran a placebo experiment that exposed why the classical and robust columns above are dishonest. Describe their experiment: what did they assign at random, what *should* the rejection rate of such placebo "effects" have been at the 5% level, and what did they actually find it to be with conventional standard errors? Then name the property of the residuals that causes the conventional SEs to be too small, and explain via the Moulton intuition (effective sample size) *why* that property shrinks the reported SE below the truth.

**(c) (4 pts)** State the fix BDM landed on — which standard-error flavor, and clustered at which level for Priya's design. Then explain why the *persistence of the treatment indicator $D_{it}$ within a state* (it is $0$ for years, then $1$ for years) makes this problem *especially* acute in DiD, referencing what high within-unit regressor correlation does to the naive standard error.

**(d) (3 pts)** Priya's clean toy design (Problems 1–4) had exactly **one treated state**. Explain why clustering by state does *not* fully rescue inference when there is only one treated cluster — i.e., why this is a genuine limitation of the two-state design rather than a software setting she can flip — and name one alternative inference approach she could use instead.

---

*End of PS 4.1. When you have attempted everything, check yourself against `book/appendices/E-solutions-manual/E-w4-ps4.1-solutions.md`. The numerical parts of Problems 1, 2, 5(c), and 6(a) can be confirmed in a few lines of Python or even on paper; the event study of Problem 4 and the inference of Problem 6 come alive in `nb4.1` (`notebooks/week-04/nb4.1-event-studies-parallel-trends.ipynb`), where you build the $2\times 2$, run the leads-and-lags, dial up a pre-trend on purpose to watch the leads tilt and the estimate inflate, and reproduce the spirit of Bertrand–Duflo–Mullainathan by running placebo treatments and watching each standard-error flavor's false-positive rate.*
