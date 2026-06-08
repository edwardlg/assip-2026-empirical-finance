# Week 4 Assessment — Causal Inference II

This is the end-of-week assessment for Week 4. It has three parts. **Part A** is a conceptual derive-and-
judge section on the spine of the week — the $2\times 2$ difference-in-differences and parallel trends, the
staggered-adoption crisis (the forbidden comparison, Goodman-Bacon, negative weights, Callaway–Sant'Anna),
regression discontinuity (sharp and fuzzy, the bandwidth bias–variance trade-off, the McCrary density test),
synthetic control with placebo inference, and shift-share identification with its two faces. **Part B** is a
small simulation you build, estimate, and report on: you play God, generate a staggered-adoption panel where
you know every true effect, and watch the pooled two-way fixed-effects coefficient mangle it while a
clean-control estimator recovers the truth. **Part C** is the rubric, with explicit point totals. An
instructor answer key follows Part C.

The whole thing is one focused sitting plus the coding task. Methods are limited to Week 4: the $2\times 2$ DiD
and the TWFE regression $Y_{it}=\alpha_i+\lambda_t+\beta D_{it}+\varepsilon_{it}$, parallel trends and event
studies, the staggered-adoption critique (Goodman-Bacon, de Chaisemartin–D'Haultfœuille negative weights,
Callaway–Sant'Anna / Sun–Abraham / Borusyak–Jaravel–Spiess), sharp and fuzzy regression discontinuity, local
linear estimation and bandwidth choice, the McCrary density test, synthetic control and synthetic DiD with
placebo permutation inference, and shift-share / Bartik designs with the GPSS and BHJ views, Rotemberg weights,
and AKM standard errors. You may lean on Week 3 vocabulary — potential outcomes, LATE, compliers, the Wald
ratio, exclusion — where a Week-4 design reduces to it, and you should, but no new Week-3-only machinery is
required. Show your reasoning. A correct number with no argument earns little; an honest "this assumption is
untestable, and here is what I'd need to defend it" earns a great deal.

**Total: 100 points.** Part A = 48, Part B = 42, Presentation/honesty woven through both = 10.

Throughout, write panel potential outcomes as $Y_{it}(1), Y_{it}(0)$ (or $Y_{it}^{I}, Y_{it}^{N}$ for the
synthetic-control intervention/no-intervention split), the treatment indicator $D_{it}$, the running variable
$X$ with cutoff $c$, the adoption cohort $G_i$, and event time $e=t-G_i$. Name every estimand (ATT, the
group-time $\text{ATT}(g,t)$, the RD effect at the cutoff, a LATE for compliers) before you estimate it, and
name the identifying assumption of any design in one sentence, in the spec-discipline format from CONVENTIONS
§4.

---

## Part A — Derive, interpret, and judge (48 points)

Answer in a few lines of algebra plus two to four sentences of interpretation. Where a derivation is asked
for, the steps must be visible; a boxed final formula with no path earns half credit at most.

**A1. (The $2\times 2$, the imputed counterfactual, and parallel trends. 8 pts.)** Priya studies a wildfire-
pricing regulation that one state ("treated") adopted while others did not. Her four cell means, in dollars of
annual homeowner premium, are: treated before \$1{,}500, treated after \$1{,}680; control before \$1{,}200,
control after \$1{,}310. (i) Compute the difference-in-differences estimate two ways — as (treated change)
minus (control change), and as (after gap) minus (before gap) — and confirm they agree. (ii) Write the
counterfactual $\mathbb{E}[Y_{it}(0)\mid\text{treated, post}]$ that DiD *imputes*, as a number, and state in
one sentence which assumption justifies that imputation. (iii) Suppose the treated state was secretly already
on a *steeper* premium trajectory than the control before the regulation, for reasons unrelated to it. State
whether the \$70 over- or understates the true ATT, and explain via the parallel-trends equation why.

**A2. (Pre-trends do not prove parallel trends — name the assumption and how you'd interrogate it. 8 pts.)**
Priya estimates an event study $Y_{it}=\alpha_i+\lambda_t+\sum_{k\neq -1}\beta_k\mathbb{1}\{t-t_i^*=k\}+
\varepsilon_{it}$, omitting $k=-1$, and her lead coefficients $\hat\beta_{-4},\dots,\hat\beta_{-2}$ are all
statistically indistinguishable from zero. (i) **Name the identifying assumption of DiD and explain why it is
untestable** — point to the exact term in the parallel-trends equation that lives in a counterfactual world.
(ii) Give the *two distinct reasons* (one logical, one statistical) that flat leads do not establish parallel
trends, and explain why the statistical reason makes the *worst* datasets the *most* falsely reassuring. (iii)
State precisely what you would need to see in the lead coefficients' confidence bands before treating flat
leads as genuine evidence rather than mere noise, and name one thing beyond eyeballing the leads that a
careful analyst reports.

**A3. (The staggered-adoption crisis: the forbidden comparison and the sign flip. 8 pts.)** Priya now has a
disclosure rule adopted by State E in year 2 and State L in year 5, no never-treated state, eight years, and a
treatment effect that *helps* (lowers non-renewals) and *builds* over event time. Every true treatment effect
in the panel is negative, yet the pooled TWFE coefficient $\hat\beta$ comes out *positive*. (i) Name the
**forbidden comparison** that drives the flip: which years, which state is wrongly used as the control, and why
is that control "contaminated"? (ii) Explain in one or two sentences the *mechanism* — why does subtracting an
already-treated unit's change flip the sign here, and why does it require the effect to be *dynamic*? (iii)
State the **two distinct conditions, either of which rescues** the pooled TWFE coefficient under staggered
timing, and for each explain in a sentence why the forbidden comparisons stop causing trouble.

**A4. (Goodman-Bacon, negative weights, and the clean cure. 8 pts.)** (i) State the Goodman-Bacon identity in
words — $\hat\beta^{\text{TWFE}}$ equals what kind of weighted average, and what determines the weights (not
the effects)? Name the three types of $2\times 2$ comparison and say which one is forbidden. (ii) de
Chaisemartin and D'Haultfœuille write $\hat\beta^{\text{TWFE}}\xrightarrow{p}\sum_{(i,t):D_{it}=1}w_{it}\,
\text{ATT}_{it}$ with weights summing to one. State the one property of these $w_{it}$ that makes the estimator
dangerous, and the one practical fact about them — what can you compute, and *before* doing what? (iii) Write
the Callaway–Sant'Anna group-time estimator $\widehat{\text{ATT}}(g,t)$ as a clean $2\times 2$, define its
control group precisely (which units are *eligible* and which are *forbidden*), and say in one sentence why its
event-study pre-trends are more trustworthy than the naive TWFE event study's.

**A5. (Which design fits this scenario, and why — plus sharp-vs-fuzzy RD. 8 pts.)** For each of the following,
name the single Week-4 design you would use and justify the choice in one or two sentences; where the design is
RD, also say whether it is **sharp or fuzzy** and, if fuzzy, write the estimand as a ratio of two jumps and
name what plays the role of the instrument. (i) A lender's automated system *approves every* applicant with a
credit score $\geq 660$ and rejects all others; Maya wants the effect of approval on two-year default at the
margin. (ii) A means-tested subsidy that families *become eligible to apply for* when income drops below a
threshold, but only $60\%$ of eligible families enroll; the outcome is household savings. (iii) A single state
passes a first-in-the-nation climate-disclosure mandate and Priya wants the effect on its average premium, with
no naturally comparable twin state. (iv) Maya wants the effect of a *local labor-demand shock* on regional
delinquency, but realized local employment growth is endogenous (local confounders, supply responses) and she
has no randomized lever — only national industry growth rates and each region's baseline industry mix.

**A6. (RD machinery: bandwidth, the global-polynomial trap, and the McCrary test. 8 pts.)** Sam runs a sharp
Russell-1000/2000 RD with rank-distance as the running variable and a true jump he does not know. (i) A
classmate fits a *global quartic* in $X$ to all the data and reports a tight confidence interval; at a narrow
*local-linear* bandwidth the estimate is close to the truth but imprecise, and at a wide bandwidth it is
precise but drifts away from the truth. Explain the **bias–variance trade-off** this exhibits, why the global
quartic is a trap (cite the mechanism, not just the name), and which two procedures choose the bandwidth
honestly. (ii) State what **CCT robust bias correction** fixes that the naive $\hat\tau\pm1.96\,\widehat{\text{se}}$
interval gets wrong *at the MSE-optimal bandwidth*. (iii) Describe the **McCrary density test** in words — its
null, what rejecting it implies, and what threat it polices — and then name one threat to an RD design that the
McCrary test, the covariate-balance test, and the donut check would *all* miss, and say how you would defend
against it instead.

**A7. (Synthetic control inference, and the shift-share two-faces problem. 8 pts.)** (i) Priya builds a
synthetic control for her single treated state from a donor pool. Explain why she cannot report a t-statistic,
and describe the **placebo permutation test** that replaces it — what gets reassigned, why the **post/pre
RMSPE ratio** $r_i$ (not the raw post gap) is the right yardstick, and how the $p$-value is computed. With 18
donors and a treated unit whose ratio is the *second-largest* of the 19 units, compute the $p$-value and state
the smallest $p$-value she could ever report with that pool. (ii) A shift-share (Bartik) instrument is
$B_r=\sum_j s_{rj}g_j$. State the **two identification views** — whose exogeneity GPSS leans on versus BHJ —
and explain why "a product is exogenous if *either* factor is" means a single design gives you two shots at one
untestable restriction. (iii) Maya's *bank-lending* shift-share has only six banks, with one bank holding
$70\%$ of a region's deposits. Which view can she honestly invoke and which fails, and why? Name the diagnostic
that tells her *which shares drive her estimate*, and the standard-error fix she needs because two distant
auto-heavy regions share the same shock.

---

## Part B — Simulate staggered adoption; show TWFE breaks and Callaway–Sant'Anna repairs it (42 points)

You will build a panel where you control every treatment effect, plant staggered adoption and a *building*
dynamic effect, and watch the pooled TWFE coefficient become a biased — and in one configuration *wrong-signed*
— weighted average while a clean-control group-time estimator recovers the truth. This ties Ch 4.1 (the TWFE
form, parallel trends, the event study) to Ch 4.2 (the forbidden comparison, Goodman-Bacon, Callaway–Sant'Anna)
in one script. You are reproducing, in miniature, the lesson the staggered-DiD literature burned into the
profession around 2018–2021.

### The data-generating process

Index states $i$ and years $t$. Each state has an adoption cohort $G_i$ (the year it first switches on, or
$\infty$ for never-treated); $D_{it}=\mathbf{1}\{t\geq G_i\}$ is the absorbing treatment. Build the outcome so
**parallel trends holds exactly** and the **true effect is known, negative, and building**:

$$
Y_{it} = \alpha_i + \lambda_t + \tau_{it}\,D_{it} + \varepsilon_{it},
\qquad
\tau_{it} = -(e+1)\ \text{ at event time } e = t - G_i \ (\text{so } -1, -2, -3, \dots),
$$

with unit effects $\alpha_i$, common year effects $\lambda_t$, and small noise $\varepsilon_{it}$. The
per-period effect $-(e+1)$ means the policy helps in every treated cell and helps *more* the longer it has been
in force — staggered timing *and* dynamic heterogeneity, the exact recipe for the crisis. Pin your random seed
and state it. Use enough states (say 40) and years (say 12) to estimate the modern estimator with real standard
errors; you may also build the deliberately tiny two-state worlds below by hand.

### Tasks

**B1. Build the sign-flip world and the contained world (10 pts).** First, the sharp pocket example: **World A**
has exactly two states — E adopting in year 2, L adopting in year 5 — *no never-treated state*, eight years,
noise off, baselines equal. Compute the pooled TWFE coefficient $\hat\beta$ from
`Y ~ C(state) + C(year) + D` and confirm it is **positive** even though every true $\tau_{it}$ is negative —
the sign flip. Then **World B** adds a genuine never-treated state N; recompute $\hat\beta$ and confirm it is
now the *right sign but attenuated* (not the truth). State, in one sentence, why adding one never-treated unit
rescues the *sign* but not the *magnitude*, and name the forbidden comparison that was the only game in town in
World A.

**B2. The full panel: TWFE vs. the truth (10 pts).** Build the 40-state, 12-year panel above with several
adoption cohorts and a block of never-treated states, noise on. (a) Report the pooled TWFE
$\hat\beta$ (use `pyfixest`'s `feols` with state and year fixed effects, clustered by state). (b) Compute the
*true* overall ATT by averaging the $\tau_{it}$ over all actually-treated cells. (c) Report the gap between
$\hat\beta$ and the truth and state its sign and rough size. The TWFE number should be biased toward zero
(attenuated) relative to the true, more-negative average.

**B3. Callaway–Sant'Anna: clean controls and a heterogeneity-robust event study (16 pts).** Estimate the
group-time $\widehat{\text{ATT}}(g,t)$ with a clean-control estimator (the `differences` package's
`ATTgt`, or a hand-rolled clean $2\times 2$ loop in the spirit of Ch 4.2 §7 using never- and not-yet-treated
units as controls — state which you used). (a) Aggregate to an **event-study** profile
$\widehat{\text{ATT}}^{\text{es}}(e)$ and confirm the post-period coefficients ($e\geq 0$) trace the true
building profile $-1,-2,-3,\dots$ within sampling noise, while the pre-period coefficients ($e<0$) are flat
near zero. (b) Collapse to a single overall ATT and confirm it lands near the true value from B2(b) and far
from the broken TWFE from B2(a). (c) In one sentence, explain why this estimator *refuses* to estimate a
cohort's effect when no clean control exists, and why that refusal is a feature, not a bug — tie it to World A.

**B4. Diagnose the weights (6 pts).** Make the forbidden comparisons visible. Either (i) run a Goodman-Bacon
decomposition (e.g. via a `bacon`-style routine or by hand on a small version) and report how much weight sits
on the forbidden "later-vs-already-treated" comparisons, *or* (ii) compute the de Chaisemartin–D'Haultfœuille
cell weights $w_{it}$ from the design alone and report how many are negative and how much total negative weight
there is. State the one-sentence verdict: the pooled $\hat\beta$ is broken not by a coding bug or a violated
parallel-trends assumption — parallel trends holds *perfectly* by construction — but by the design letting
already-treated units serve as controls, and the diagnostics show exactly where.

### Deliverables

A single notebook or script that runs end-to-end on a fresh environment with the stated seed, the World A
sign-flipped $\hat\beta$ (B1), the full-panel TWFE-vs-truth gap (B2), the Callaway–Sant'Anna event-study plot
and overall ATT (B3), the weight diagnostic (B4), and the short verdict paragraphs. State your software
versions. Same seed must reproduce the numbers.

**Optional extension (no extra points):** add a never-treated control to World A and search adoption
patterns to confirm that *any* never-treated unit keeps the TWFE sign correct (it only ever attenuates) — the
full flip requires the forbidden comparison to be the *only* available comparison. Or swap in Sun–Abraham
(saturated cohort × event-time interactions) or Borusyak–Jaravel–Spiess imputation and confirm all three
clean estimators land within sampling noise of one another.

*Alternative Part B (instructor's option, same point allocation):* an **RD bandwidth sweep**. Simulate a sharp
RD with a known jump on a smooth-but-curved outcome; (B1) estimate the jump by triangular-kernel local-linear
regression across a grid of bandwidths and tabulate $\hat\tau$, its SE, and $n$ at each; (B2) overlay a global
quartic and show it is precisely-but-wrongly placed; (B3) call `rdrobust` and confirm its data-driven CCT
bandwidth and robust bias-corrected interval bracket the truth where the naive interval at the MSE-optimal
bandwidth undercovers; (B4) run the McCrary/Cattaneo–Jansson–Ma density test and a covariate-balance RD to
audit the design. Grade against the same rubric, reading "TWFE-vs-clean" as "wide-bandwidth-bias-vs-CCT" and
"weight diagnostic" as "density/covariate audit."

---

## Part C — Analytic rubric (point allocations explicit)

Each row is scored at one of four levels. Part-A rows describe how the 48 Part-A points are awarded across the
seven conceptual items; Part B is graded by the task allocation above, refined by the criteria here. The
Presentation/honesty row spans both parts.

| Criterion | Excellent | Proficient | Developing | Missing | Points |
|---|---|---|---|---|---|
| **Conceptual correctness — DiD, RD, synthetic control mechanics (A1, A6, A7i)** | $2\times 2$ DiD computed both ways and agreeing; imputed counterfactual written as a number with parallel trends named; bias–variance trade-off explained with the *direction* of wide-bandwidth bias and the global-polynomial mechanism (distant data dictate boundary curvature); CCT correctly described as fixing undercoverage from leftover bias at the MSE-optimal $h$; McCrary null/reject/threat correct; synthetic-control placebo logic and RMSPE ratio correct with the $p$-value and $1/(J{+}1)$ floor. | One mechanic has a gap (e.g. CCT asserted not explained, or the RMSPE-ratio rationale thin); rest correct. | Final formulas/numbers stated but reasoning missing; McCrary garbled; t-stat reported for synthetic control without flagging it. | Not attempted or fundamentally wrong. | 16 |
| **Identification reasoning — assumptions named and interrogated (A2, A3, A4, A5)** | Parallel trends named and its *post-period counterfactual* term correctly flagged as untestable; the two reasons flat leads ≠ parallel trends (logical + low-power) given, with the "worst data most reassuring" point; forbidden comparison identified by years/state with the dynamic-effects mechanism; the two TWFE-rescue conditions stated; Goodman-Bacon and negative-weights identities stated correctly (weights from design, computable before estimating, can be negative); Callaway–Sant'Anna clean control defined (never-/not-yet-treated eligible, already-treated forbidden); A5 design choices all correct with sharp/fuzzy split and the fuzzy ratio/instrument named. | Conditions right; one of {the two-reasons split, the rescue conditions, the CS control definition, one A5 design} thin or missing. | States assumptions but conflates pre-trends with parallel trends, calls the RD effect a population ATE, or picks a wrong design for one scenario. | Absent or wrong on the core assumptions. | 18 |
| **Code correctness & reproducibility (Part B)** | Staggered DGP with parallel trends holding by construction and known building $\tau_{it}$; World A sign flip reproduced; full-panel TWFE via `pyfixest` clustered by state; Callaway–Sant'Anna via `differences` (or a correct hand-rolled clean $2\times 2$ using never-/not-yet-treated controls only); event study and overall ATT recovered; seed pinned; runs end-to-end and reproduces; never forms a forbidden comparison in the "clean" estimator. | Runs and is essentially correct; minor non-reproducibility or a small aggregation-weight detail off. | Logic flaw (e.g. clean estimator silently uses already-treated controls, or TWFE SEs not clustered, or no never-treated block so nothing is identified); partial output. | Does not run or wrong estimator. | 18 |
| **Results & diagnostic interpretation (B1–B4)** | World A $\hat\beta$ read correctly as the *wrong sign* with the forbidden comparison named; full-panel TWFE read as attenuated toward zero versus the more-negative truth; CS event study read as flat pre / building post matching the known $\tau$; overall CS ATT near truth and far from TWFE; weight diagnostic (Goodman-Bacon forbidden share *or* dCDH negative-weight count) reported and read as "the design, not a bug, broke TWFE while parallel trends held." | Numbers right; one interpretive link (the World-A-vs-B sign/magnitude distinction, or the weight diagnostic reading) missing. | Reports numbers without reading which estimator is honest or why; treats the TWFE bias as a parallel-trends violation. | Absent, or claims the pooled TWFE is fine. | 14 |
| **Presentation, untestable assumptions, honest threats** | Clean prose; estimand ($\text{ATT}$, $\text{ATT}(g,t)$, RD-at-cutoff, complier LATE) named before estimation; designs stated in spec-discipline format; explicitly flags parallel trends, RD continuity / compound-treatment, no-interference / no-anticipation, and shift-share exclusion as *untestable* and says what would be needed to defend each; never says "the pre-trends prove parallel trends," "the jump proves the effect," or reports a t-stat for a single-treated-unit synthetic control. | One stylistic or labeling lapse. | Several lapses; estimand unnamed; untestable assumptions treated as verified by a diagnostic. | Unreadable or rife with banned claims. | 10 |

**Total: 100 points.** (Conceptual correctness 16 + identification reasoning 18 sum to the 34 of the
"derive/judge" Part-A weight, with the remaining 14 of Part A folded into how the code and results rows reward
the Part-B reasoning; Part-B criteria sum to 32; the Presentation row adds 10. The rubric is normalized so the
maximum awarded is 100.)

A note on the spirit of the honesty row: this week rewards students who can say, out loud and unprompted,
*which assumptions the data can never check*, and who keep "identified under a defended-but-untestable
assumption" cleanly separate from "proven causal." Parallel trends (in the *post-period*), RD continuity and
the compound-treatment threat, synthetic control's no-interference and no-anticipation, and shift-share's
exclusion (sourced from shares *or* shifts) are the great untestable bets of Week 4. An answer that shows flat
pre-trends and then writes "this is consistent with parallel trends, but the post-period assumption remains
untestable, and here is the sensitivity analysis I would run" outscores a flat-leads plot presented as proof.
Equally, an answer that *refuses* to estimate a quantity the data cannot identify — the late cohort with no
clean control — and says so plainly outscores one that fabricates a number. Knowing *what kind* of claim you
are making is the entire point of Week 4.

---

## Instructor answer key / model-answer sketch

**A1.** (i) Treated change $=1{,}680-1{,}500=\$180$; control change $=1{,}310-1{,}200=\$110$; DiD
$=180-110=\$70$. The other order: after gap $=1{,}680-1{,}310=\$370$, before gap $=1{,}500-1{,}200=\$300$;
$370-300=\$70$. Agree. (ii) DiD imputes
$\widehat{\mathbb{E}[Y_{it}(0)\mid\text{treated, post}]}=\bar Y_T^{\text{pre}}+(\bar Y_C^{\text{post}}-
\bar Y_C^{\text{pre}})=1{,}500+110=\$1{,}610$ — the treated state's own pre level lifted by the control's
trend; the ATT is $1{,}680-1{,}610=\$70$. The justifying assumption is **parallel trends**: absent the
regulation, the treated state's untreated potential outcome would have changed by the same amount as the
control's. (iii) If the treated state was on a steeper $Y(0)$ trend, its true counterfactual change exceeds the
control's \$110 (say it would have risen \$160 to \$1{,}660), so the true ATT is $1{,}680-1{,}660=\$20<\$70$:
the \$70 **overstates** the ATT, because the parallel-trends equation's left-hand side
($\mathbb{E}[Y_{it}(0)\mid\text{treated, post}]-\mathbb{E}[Y_{it}(0)\mid\text{treated, pre}]$) is larger than
the right-hand side we substituted in, and the unmodeled differential trend is mislabeled as treatment effect.
*(Credit both DiD computations, the \$1{,}610 imputation with parallel trends named, and "overstates" with the
trend-divergence reason.)*

**A2.** (i) The identifying assumption is **parallel trends**:
$\mathbb{E}[Y_{it}(0)\mid\text{treated, post}]-\mathbb{E}[Y_{it}(0)\mid\text{treated, pre}]=
\mathbb{E}[Y_{it}(0)\mid\text{control, post}]-\mathbb{E}[Y_{it}(0)\mid\text{control, pre}]$. It is untestable
because the term $\mathbb{E}[Y_{it}(0)\mid\text{treated, post}]$ is the treated group's *post-period untreated*
potential outcome — the world where the regulation never passed — which never happened and can never be
observed; no test on realized data can confirm it. (ii) *Logical:* flat leads concern the *pre-period* (a world
that did happen and is measurable); parallel trends is a claim about the *post-period* counterfactual.
Something could shift the treated group's trajectory exactly at treatment for reasons other than the treatment
(a coincident shock, a bundled policy) and leave pre-trends pristine while the post-period assumption is false
— pre-trends are a necessary-looking symptom, not the disease. *Statistical:* pre-trend tests have **low
power**; with few noisy pre-periods the lead confidence intervals are wide enough to contain both zero and a
meaningful differential trend, so "failed to reject zero pre-trend" can mean "no pre-trend" or "a pre-trend my
data can't see." The worst datasets — small, noisy, few periods — are *most* likely to hand you a falsely
reassuring flat pre-trend, because they can detect nothing; reassurance and statistical weakness look
identical. (iii) You need the lead bands to be *tight* — narrow enough to rule out an economically meaningful
differential slope, not merely centered on zero. Beyond eyeballing leads, a careful analyst reports a formal
**sensitivity analysis**: how large a parallel-trends violation would have to be to overturn the result, rather
than pretending the violation is exactly zero. *(Credit untestability tied to the post-period counterfactual
term, both reasons with the asymmetric-danger point, and "tight bands + sensitivity analysis.")*

**A3.** (i) The **forbidden comparison** is years 5–8, where State E is used as the control for newly-treated
State L. E is *contaminated* because it is already treated throughout that window — it is not a clean untreated
counterfactual but a unit carrying its own (still-moving) treatment effect. (ii) Across years 5–8, E's effect
is still deepening (from $-4$ toward $-7$), so E's outcome is sliding *downward faster* than freshly-treated L's;
when TWFE differences L's change against E's change, L looks like it is *rising relative to E*, and the
forbidden comparison subtracts E's still-growing effect from L's, flipping the differenced quantity positive.
With no never-treated state to dilute it, this forbidden comparison dominates and $\hat\beta$ comes out
positive. It requires a **dynamic** effect: if E's effect were constant, its *change* over the window would be
zero and nothing would be subtracted. (iii) **(1) Common timing** — if all treated units adopt at the same
date there are no already-treated units to misuse as controls, so no forbidden comparison exists. **(2)
Homogeneous (constant) effects** — even when an already-treated unit is used as a control, the contamination it
injects is just the constant $\beta$, which cancels cleanly. The disease needs *both* staggered timing *and*
dynamic/heterogeneous effects. *(Credit the years-5–8 forbidden comparison with E named, the
faster-sliding-control mechanism, the dynamic requirement, and both rescue conditions.)*

**A4.** (i) Goodman-Bacon: $\hat\beta^{\text{TWFE}}$ is *exactly* (an algebraic identity, not an approximation)
a weighted average of all the simple $2\times 2$ DiDs in the data, with weights determined entirely by
treatment-timing variance (largest for mid-sample adopters) — *not* by how trustworthy each comparison is. The
three types are: treated-vs-never-treated (clean), earlier-vs-later *before* the later adopts (clean), and
later-vs-earlier *after* the earlier has adopted (**forbidden** — an already-treated unit as control). (ii) The
dangerous property: the weights $w_{it}$ **can be negative** (they sum to one but are not all positive), so the
"average" can lie outside the range of every true effect — if all $\text{ATT}_{it}<0$ but some weights are
negative, the sum can be positive. The practical fact: the weights depend only on the *design* (who is treated
when), not on the effects, so you can **compute them from your data alone, before estimating a single
treatment effect**, and count the negative ones. (iii)
$\widehat{\text{ATT}}(g,t)=(\bar Y_{g,t}-\bar Y_{g,g-1})-(\bar Y_{C,t}-\bar Y_{C,g-1})$: cohort $g$'s change
from its last pre-period $g-1$ to $t$, minus the clean control's change over the same window. The control group
$C$ is **never-treated units or not-yet-treated units** (adoption year strictly after $t$, hence still
untreated through the window); **already-treated units are forbidden**. Its pre-trends are more trustworthy
because each cohort's dynamics are estimated against clean controls *in isolation*, so no cohort's lead/lag can
bleed into another's the way the naive TWFE event study's do (Sun–Abraham). *(Credit the exact-identity
weighted-average statement, the three types with the forbidden one flagged, the negative-weights danger plus
"computable from design before estimating," and the clean-control definition with the no-bleed pre-trend
point.)*

**A5.** (i) **Sharp RD.** Approval is a deterministic step at $c=660$ in the running variable (credit score),
so the effect at the margin is the jump in $\mathbb{E}[Y\mid X]$ at $660$; the marginal effect is exactly the
right number for a question about where to set the cutoff. (ii) **Fuzzy RD.** Eligibility jumps at the
threshold but only $60\%$ enroll, so the cutoff shifts the *probability* of treatment, not treatment itself.
Estimand $=\dfrac{\lim_{x\downarrow c}\mathbb{E}[Y\mid X]-\lim_{x\uparrow c}\mathbb{E}[Y\mid X]}
{\lim_{x\downarrow c}\mathbb{E}[D\mid X]-\lim_{x\uparrow c}\mathbb{E}[D\mid X]}$ = (jump in outcome)/(jump in
treatment), a Wald ratio; the **instrument** is $Z=\mathbf{1}\{X\geq c\}$, the above-cutoff indicator, and the
effect is a LATE for compliers at the cutoff under monotonicity. (iii) **Synthetic control** (or synthetic
DiD): one treated unit, no clean twin, so *build* a convex-weighted donor blend that matches the pre-period and
read the effect off the post-period divergence. (iv) **Shift-share / Bartik instrument**: manufacture an
instrument $B_r=\sum_j s_{rj}g_j$ from national industry shifts (which no single region caused) times the
region's baseline industry shares, and use it to instrument the endogenous realized local shock — it isolates
the demand piece riding national tides from local supply responses and confounders. *(Credit all four designs;
require sharp/fuzzy for (i)–(ii) and the fuzzy ratio + instrument for (ii).)*

**A6.** (i) **Bias–variance trade-off:** a wide bandwidth uses many points far from $c$ — low variance (tight
SE) but high bias, because the straight line is forced to fit data over a range where the true curve bends, so
it mis-reads the boundary height; a narrow bandwidth uses only points hugging $c$ — low bias (a line is a good
local approximation) but high variance (few points, jittery fit). The **global quartic is a trap** because
high-order polynomials are erratic near the boundary, let data *far* from $c$ dictate the curvature *at* $c$
(Apple's data bending the fit at rank 1{,}000), and place bizarre, even negative, implicit weights on
observations — Gelman–Imbens — so it returns a *precise* number in the *wrong place*. Honest bandwidth choice:
**Imbens–Kalyanaraman** (MSE-optimal) and **Calonico–Cattaneo–Titiunik (CCT)**. (ii) At the MSE-optimal
bandwidth the estimator is deliberately *not* centered on the truth — minimizing MSE accepts some leftover bias
to buy variance reduction — so the naive interval $\hat\tau\pm1.96\,\widehat{\text{se}}$, built assuming
centering, is mis-located and *undercovers*. **CCT robust bias correction** estimates and subtracts the leading
bias term and inflates the SE to account for the noise the correction itself adds, restoring nominal coverage.
(iii) **McCrary density test:** estimate the density of the running variable on each side of $c$ and test
whether they agree at the cutoff; *null* = density continuous at $c$ (no sorting), *reject* = a jump in the
density, evidence of **manipulation/sorting** (units gaming which side of $c$ they land on). The threat all
three checks miss is a **compound treatment** — the *same* cutoff triggering more than one thing at once (a
credit score of $660$ flipping approval *and* the rate tier *and* securitization eligibility). It leaves no
statistical fingerprint (density smooth, covariates balanced, donut stable) and must be defended from
**institutional knowledge** that the cutoff governs only the treatment you claim — for fuzzy RD this is literally
the exclusion restriction. *(Credit the trade-off with wide-bandwidth bias direction, the Gelman–Imbens
mechanism, IK + CCT, the undercoverage fix, McCrary null/reject/threat, and compound treatment as the
untestable miss.)*

**A7.** (i) No t-statistic because the effective number of treated units is **one** — there is no
cross-sectional treatment variation to power a conventional standard error, and the large-$N$ asymptotics
behind t-tests do not apply; a t-stat here is false precision. The **placebo permutation test** reassigns the
*treatment label* to each donor in turn: build a synthetic control for each donor (from the other donors),
compute its gap path, and form a reference distribution of "effects" for units known to be untreated. The
yardstick is the **post/pre RMSPE ratio** $r_i=\text{RMSPE}_{\text{post},i}/\text{RMSPE}_{\text{pre},i}$, not
the raw post gap, because a donor that fit *badly* in the pre-period would show a big post gap for reasons
unrelated to any effect; scaling by pre-fit isolates units that matched well then diverged sharply. The
$p$-value is the fraction of all $J+1$ units with $r_i\geq r_1$. With 18 donors (19 units) and the treated
unit's ratio *second-largest*, $p=2/19\approx0.105$; the smallest possible $p$-value with this pool is
$1/19\approx0.053$ — so even a perfect outlier cannot clear 5%, which is why a credible study needs a larger
donor pool. (ii) **GPSS** leans on **exogenous shares** (the Bartik is a GMM combination of the industry-share
instruments, so the initial industry mix must be uncorrelated with the error); **BHJ** leans on
**quasi-randomly assigned shifts** (the national shocks are as-good-as-random across *many* industries, and the
shares may be endogenous). Because $B_r$ is a *product* shares $\times$ shifts, the covariance with the error
vanishes if *either* factor is exogenous — so a single design gives two independent shots at the one
untestable exclusion restriction, and the honest empiricist names which shot they are taking. (iii) With only
six banks and one holding $70\%$ of deposits, there is no "many shocks" law-of-large-numbers to invoke — a
single big bank's idiosyncratic shock dominates — so **BHJ fails** and she must defend **GPSS exogenous
shares** (argue the region's initial bank mix is unrelated to its latent fragility). The diagnostic for *which
shares drive the estimate* is **Rotemberg weights** $\hat\alpha_j$ (the headline 2SLS is
$\sum_j\hat\alpha_j\hat\beta_{1,j}$); aim share-exogeneity skepticism at the high-weight banks. The SE fix is
**Adão–Kolesár–Morales (AKM)** standard errors (or the BHJ shock-level regression), because regions with
similar exposure share the same shocks, inducing cross-regional error correlation that ordinary region
clustering misses and that makes vanilla SEs too small. *(Credit the one-treated-unit reason, the placebo
reassignment + RMSPE-ratio rationale, $p=2/19$ and the $1/19$ floor, the GPSS/BHJ split with the
"either-factor" logic, the six-banks → GPSS-only judgment, and Rotemberg weights + AKM SEs.)*

**Part B expected results (for grading).**

- *B1:* **World A** (E adopts yr 2, L adopts yr 5, no never-treated, 8 yrs, noise off) gives a pooled TWFE
  $\hat\beta\approx+0.40$ — the **sign flip**, positive on data where every true $\tau_{it}$ is negative,
  driven by the forbidden "L-vs-already-treated-E" comparison in years 5–8 that is the only comparison
  available. **World B** (add never-treated N, 6 yrs) gives $\hat\beta\approx-1.23$ — the right sign but
  attenuated (the true overall ATT is $\approx-2.57$). The required sentence: a never-treated unit supplies a
  *clean* comparison that keeps the sign correct, but pooled TWFE still mixes in forbidden comparisons that
  drag the magnitude toward zero, so the sign is rescued and the magnitude is not.
- *B2:* On the 40-state, 12-year panel the pooled TWFE $\hat\beta$ is biased **toward zero** relative to the
  true overall ATT (which is the average of the $-(e+1)$ effects over treated cells, a clearly negative number
  whose magnitude exceeds $|\hat\beta^{\text{TWFE}}|$). The gradeable claim is the *direction and rough size* of
  the gap (TWFE attenuated, true more negative), not exact decimals — those are seed- and cohort-mix-dependent.
- *B3:* The Callaway–Sant'Anna event study has **flat pre-period coefficients** ($e<0$, near zero — the genuine
  placebo/pre-trend check) and **post-period coefficients tracing the building profile** $\approx-1,-2,-3,\dots$
  within noise; the **overall clean ATT lands near the B2(b) truth** and far from the broken TWFE. Full credit
  requires a genuine clean-control estimator (never-/not-yet-treated controls only) — *not* a relabeled TWFE.
  The sentence for (c): the estimator refuses to form a forbidden comparison, so when a cohort has no clean
  control (World A's late cohort L) it returns no estimate rather than fabricating one — honesty under duress,
  the same refusal that exposed the crisis.
- *B4:* Either the Goodman-Bacon decomposition shows a meaningful share of weight on the forbidden
  "later-vs-already-treated" comparisons (with negative weight visible on the worst), *or* the dCDH cell-weight
  count shows some negative $w_{it}$ with nonzero total negative weight. Verdict: parallel trends holds
  *perfectly* by construction, so the bias is *not* a violated assumption or a bug — it is the design letting
  already-treated units do control duty, and the weight diagnostic localizes it.

**Quick grading heuristic.** The two highest-signal items are A2/A3 (do they correctly flag parallel trends —
specifically the *post-period* counterfactual — as untestable, give *both* reasons flat leads are not proof,
and name the *forbidden comparison* with the dynamic-effects mechanism rather than blaming a parallel-trends
violation?) and B1/B3 (did World A actually flip sign while the clean Callaway–Sant'Anna estimator recovered
the building profile and the right-signed overall ATT — and did they build the clean estimator with *clean
controls only*, never an already-treated unit?). A student who keeps "identified under a defended-but-untestable
assumption" cleanly separate from "proven causal," who reads the TWFE failure as a *design/weighting* problem
rather than an assumption violation, and who refuses to fabricate an estimate the data cannot identify, has the
Week-4 mindset; the rest is execution.
