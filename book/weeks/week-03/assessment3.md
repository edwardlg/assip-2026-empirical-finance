# Week 3 Assessment — Causal Inference I

This is the end-of-week assessment for Week 3. It has three parts. **Part A** is a conceptual derive-and-
judge section on the spine of the week — the potential-outcomes framework and the selection-bias
decomposition, the conditional-independence assumption with matching and propensity scores, inverse-
probability weighting and entropy balancing and the doubly-robust idea, instrumental variables and the
relevance/exclusion split, LATE and compliers, and weak instruments with the first-stage $F$ and Anderson–
Rubin inference. **Part B** is a small simulation you build, estimate, and report on: you play God, generate
the science table, and watch a weak instrument lie before Anderson–Rubin tells the truth. **Part C** is the
rubric, with explicit point totals. An instructor answer key follows Part C.

The whole thing is one focused sitting plus the coding task. Methods are limited to Week 3: potential
outcomes and SUTVA, the ATT/ATE/LATE estimands, CIA/overlap with matching, propensity scores, IPW (Horvitz–
Thompson and Hájek), entropy balancing, AIPW/doubly-robust, IV/2SLS, LATE and the complier taxonomy, the
first-stage and Olea–Pflueger effective $F$, and Anderson–Rubin inference. No difference-in-differences, no
regression discontinuity, no synthetic control — those are Week 4. Show your reasoning. A correct number with
no argument earns little; an honest "this assumption is untestable, and here is what I'd need to defend it"
earns a great deal.

**Total: 100 points.** Part A = 48, Part B = 42, Presentation/honesty woven through both = 10.

Throughout, write potential outcomes as $Y_i(1), Y_i(0)$, the treatment indicator $D_i$, the instrument
$Z_i$, and name every estimand (ATE, ATT, or LATE) before you estimate it. Name the identifying assumption
of any design in one sentence, in the spec-discipline format from CONVENTIONS §4.

---

## Part A — Derive, interpret, and judge (48 points)

Answer in a few lines of algebra plus two to four sentences of interpretation. Where a derivation is asked
for, the steps must be visible; a boxed final formula with no path earns half credit at most.

**A1. (The selection-bias decomposition, from the definitions. 8 pts.)** Sam reports that hedge-fund clients
who enrolled in his firm's "risk-coaching" program had average annual returns 4.0 percentage points higher
than clients who did not enroll. Let $D_i=1$ for enrollees, $Y_i$ the return. (i) Write the naive difference
$\Delta = \mathbb{E}[Y_i\mid D_i=1]-\mathbb{E}[Y_i\mid D_i=0]$ and, using only the observation rule
$Y_i = D_iY_i(1)+(1-D_i)Y_i(0)$ and an add-and-subtract step, derive the exact decomposition
$\Delta = \text{ATT} + \big(\mathbb{E}[Y_i(0)\mid D_i=1]-\mathbb{E}[Y_i(0)\mid D_i=0]\big)$. (ii) State in
words what the selection-bias term *is* (in terms of $Y(0)$), and give the most plausible reason it is
*positive* here. (iii) Would a larger client base shrink the bias? Answer in one sentence and say why.

**A2. (CIA, overlap, and why matching is still selection-on-observables. 8 pts.)** Maya matches enrollees in
a financial-literacy course to non-enrollees on credit score, income, and age, and her post-matching balance
table shows every standardized mean difference below $0.03$. (i) State the conditional independence
assumption (CIA) and the overlap condition formally, and explain in one sentence what beautiful balance on
$\mathbf{X}$ *has* established. (ii) Name the one thing the balance table can *never* establish, and explain
*why* no balance table ever could — tie your answer to the fundamental problem of causal inference. (iii)
**Is selection-on-observables credible here?** Suppose applicant *motivation* drives both enrolling and
approval and is not in $\mathbf{X}$. Connect the resulting bias to the Week-2 omitted-variable-bias product
$\beta_2\delta_1$, give its sign, and state whether matching over- or understates the course's effect.

**A3. (Why inverse-probability weighting works, and when it explodes. 8 pts.)** (i) For the treated arm,
show the one line of expectation algebra that makes IPW work: using the law of iterated expectations and CIA,
prove $\mathbb{E}\!\left[\dfrac{D_iY_i}{e(\mathbf{X}_i)}\right]=\mathbb{E}[Y_i(1)]$, where
$e(\mathbf{X}_i)=\Pr(D_i=1\mid\mathbf{X}_i)$. Point to the exact step where the propensity score cancels.
(ii) A treated unit has an estimated score $\hat e=0.04$. Compute its (unstabilized) IPW weight and explain
in one sentence why this single number should make you nervous. (iii) Name two distinct defenses against
exploding weights and say, for one of them, what it costs you (does it change the estimand?).

**A4. (Entropy balancing and the doubly-robust property. 8 pts.)** (i) In one or two sentences, contrast how
*IPW* achieves covariate balance with how *entropy balancing* achieves it — which one balances *exactly, by
construction* and which one balances *only if a model is right*, and why entropy balancing's weights tend to
stay tame where IPW's explode. (ii) Write the AIPW (doubly-robust) estimator for the treated mean,
$\hat\mu_1^{\text{DR}}=\frac1N\sum_i\big[\hat\mu_1(\mathbf{X}_i)+\tfrac{D_i(Y_i-\hat\mu_1(\mathbf{X}_i))}{\hat
e(\mathbf{X}_i)}\big]$, and explain precisely what "doubly robust" *means* — which two models are involved and
how many of them you need to get right. (iii) Priya's colleague says her AIPW estimate is "garbage because
irrigation spending surely isn't linear in rainfall," so her outcome model is wrong. State the exact
condition under which her estimate is *still* consistent despite the misspecified outcome model.

**A5. (IV: relevance vs. exclusion, the Wald ratio, and LATE/compliers. 8 pts.)** Maya's nonprofit randomly
mailed a course-promotion flyer to some households ($Z_i=1$) and not others. Among the mailed, $40\%$
completed the course and the mean change in credit-card balance was $-\$120$; among the unmailed, $10\%$
completed and the mean change was $-\$30$ (lower is better). (i) Compute the first stage, the reduced form,
and the Wald estimate $\hat\beta_1^{\text{Wald}}$. (ii) State the relevance condition and the exclusion
restriction for the mailer, and say which one the data can confirm and which one is *untestable* and must be
argued — give one concrete way exclusion could fail here. (iii) Define the four complier types via the
treatment potential outcomes $D_i(0),D_i(1)$; state which assumption rules out defiers; name *whose* effect
the Wald number estimates and what share of the population they are; and name two groups whose effect IV is
*blind* to and why.

**A6. (Weak instruments: the pathology, the diagnostics, and honest inference. 8 pts.)** A classmate reports
a 2SLS coefficient of $0.42$ (classical SE $=0.11$, three stars) for the effect of patenting on firm value,
an OLS coefficient of $0.55$, and a first-stage $F$ of $3.8$, computed with classical errors on data that are
clustered by industry. (i) Using the $\dfrac{1}{F+1}$ heuristic for the 2SLS-relative-to-OLS bias, is the
2SLS estimate's proximity to OLS a coincidence or exactly what a weak instrument predicts? In which direction
is the weak-IV bias pointed, and why is that direction the cruel one? (ii) Explain in one sentence why the
tight SE of $0.11$ is *not* reassuring. (iii) **Name the identification threat and the design/diagnostic that
addresses it**: which strength statistic should the classmate report instead of the classical first-stage $F$
given the clustering, and which inference procedure stays valid *no matter how weak* the instrument is — and
what does an *unbounded* confidence interval from that procedure mean?

---

## Part B — Simulate a weak instrument; compare conventional vs. Anderson–Rubin coverage (42 points)

You will build a world where you control the truth, plant an instrument whose strength you can dial, and watch
2SLS slide toward the biased OLS number while its conventional confidence interval lies about its own
precision — then watch Anderson–Rubin inference stay honest. This ties Ch 3.4 (2SLS, first-stage $F$) and
Ch 3.5 (the weak-IV pathology, AR inference) into one script. You are reproducing, in miniature, the lesson
Bound–Jaeger–Baker burned into the profession.

### The data-generating process

For $i=1,\dots,N$, with a tunable first-stage strength $\pi$ and a **true effect of exactly zero** so that
any nonzero estimate is pure bias:

$$
z_i\sim\mathcal{N}(0,1),\quad u_i\sim\mathcal{N}(0,1),\quad v_i\sim\mathcal{N}(0,1),
$$
$$
x_i = \pi\, z_i + 0.8\,u_i + v_i, \qquad y_i = \beta\, x_i + u_i,\quad \beta = 0 .
$$

The shared shock $0.8\,u_i$ sitting in both $x_i$ and $y_i$ makes $x$ **endogenous**, so OLS is biased *up*.
The instrument $z_i$ is **valid** by construction (it never enters $y$ except through $x$, so exclusion
holds) and its **strength is $\pi$**: large $\pi$ is a strong instrument, $\pi$ near zero is a weak one. Use
$N=2{,}000$. Pin your random seed and state it.

### Tasks

**B1. Build the disaster and quantify the pull (10 pts).** With $\pi=0.05$ (weak), simulate one dataset.
Report (a) the OLS estimate of $\beta$, (b) the 2SLS estimate using $z$ as the instrument for $x$ (use
`linearmodels`' `IV2SLS` so the standard errors are correct), and (c) the first-stage $F$ (for a single
instrument, $F=t_z^2$ from the regression of $x$ on $z$). Confirm that 2SLS sits *between* OLS and the truth
($0$), and compare the realized $\dfrac{\hat\beta_{\text{2SLS}}}{\hat\beta_{\text{OLS}}}$ ratio to the
$\dfrac{1}{F+1}$ prediction. State, in one sentence, why a weak instrument hands you back the very bias you
used IV to escape.

**B2. Conventional coverage: watch the CI lie (12 pts).** Wrap B1 in a loop over many simulated datasets
(at least $1{,}000$ replications, new draws each time, same $\pi=0.05$). For each, form the conventional 2SLS
95% interval $\hat\beta_{\text{2SLS}}\pm1.96\,\widehat{\text{SE}}$ and record whether it *contains* the true
$\beta=0$. Report the empirical coverage (the fraction of intervals that cover $0$). It should fall well
*below* the nominal $95\%$ — the conventional interval is too narrow and miscentered, so it falsely excludes
the truth far more than $5\%$ of the time.

**B3. The cure: Anderson–Rubin coverage (14 pts).** For each simulated dataset, also build the **Anderson–
Rubin** 95% interval by test inversion: over a grid of candidate values $\beta_0$, form the adjusted outcome
$y-\beta_0 x$, regress it on $z$ (and a constant), and *keep* every $\beta_0$ for which the $F$-test that the
coefficient on $z$ equals zero *fails to reject* at $5\%$ (compare $t_z^2$ to the $0.95$ quantile of
$F_{1,\,N-2}$). The AR interval is the min-to-max of the surviving grid (note if it runs to a grid edge —
that is an *unbounded* interval). Report the empirical AR coverage of $\beta=0$ across replications and
confirm it is near $95\%$. Then push $\pi\to0.01$ on a single draw and report what happens to the *width* of
the AR interval.

**B4. Confirm the machinery works when it should (6 pts).** Set $\pi=0.8$ (strong instrument) and re-run
B1 on a single draw. Report the first-stage $F$, the 2SLS estimate, and both the conventional and AR
intervals; confirm that the $F$ is large, 2SLS lands near the true $0$, and the two intervals nearly
coincide and are tight. State the one-sentence verdict: the IV machinery is not broken in general — it is
broken *by weakness*, and the diagnostics catch the difference.

### Deliverables

A single notebook or script that runs end-to-end on a fresh environment with the stated seed, the two
coverage numbers (B2 conventional, B3 AR), the strong-instrument table (B4), and the short verdict
paragraphs. State your software versions. Same seed must reproduce the numbers.

**Optional extension (no extra points):** add a *second*, equally weak instrument and watch the many-
instruments bias nudge 2SLS even closer to OLS while the Olea–Pflueger effective $F$ (reported by
`linearmodels`) flags the weakness — a few strong instruments beat many weak ones, always.

---

## Part C — Analytic rubric (point allocations explicit)

Each row is scored at one of four levels. Part-A rows describe how the 48 Part-A points are awarded across the
six conceptual items; Part B is graded by the task allocation above, refined by the criteria here. The
Presentation/honesty row spans both parts.

| Criterion | Excellent | Proficient | Developing | Missing | Points |
|---|---|---|---|---|---|
| **Conceptual correctness — potential outcomes & weighting (A1, A3, A4)** | Selection-bias decomposition derived from the observation rule with the add-and-subtract step explicit; IPW algebra shown with the propensity-cancellation step named; entropy-vs-IPW balance contrast correct; AIPW written correctly and "doubly robust" defined as *either model right suffices*. | One derivation has a gap (e.g. IPW cancellation asserted not shown) or one slip in the entropy/AIPW contrast; rest correct. | Final formulas stated but derivations missing; "doubly robust" garbled (e.g. "need both models"). | Not attempted or fundamentally wrong. | 18 |
| **Identification reasoning — CIA, IV conditions, LATE (A2, A5)** | CIA and overlap stated correctly; relevance/exclusion split stated with the *testable vs. arguable* asymmetry; Wald ratio computed; four complier types defined via $D_i(0),D_i(1)$; monotonicity named as ruling out defiers; the estimate correctly labeled a complier LATE with the blind groups identified. | Conditions right; one of {asymmetry, monotonicity, complier identification} thin or missing. | States conditions but conflates relevance with exclusion, or calls the IV estimate the ATE. | Absent or wrong on the core conditions. | 16 |
| **Weak-IV reasoning & honest inference (A6)** | $1/(F+1)$ pull-toward-OLS identified as predicted (not coincidence) with the correct (toward-OLS) direction and why it is cruel; tight SE correctly dismissed; effective $F$ (Olea–Pflueger) named for clustered errors; Anderson–Rubin named as weak-robust; unbounded AR interval correctly read as "instrument cannot identify the effect." | Most correct; one of {effective $F$, AR, unbounded reading} missing or thin. | Recognizes weakness but trusts the SE or names no robust procedure. | Not attempted. | 14 |
| **Code correctness & reproducibility (Part B)** | One DGP simulated; OLS/2SLS via `linearmodels` with correct SEs; first-stage $F=t^2$; AR interval built by genuine test inversion over a grid; seed pinned; runs end-to-end and reproduces; never hand-rolls 2SLS SEs. | Runs and is essentially correct; minor non-reproducibility or a small AR-grid detail off. | Logic flaw (e.g. AR interval built from $\pm1.96\,$SE, or 2SLS SEs hand-computed from two OLS stages); partial output. | Does not run or wrong estimator. | 24 |
| **Coverage interpretation (B1–B4)** | Conventional coverage reported and correctly read as *below* 95% (the CI lies); AR coverage near 95% (it is honest); AR width balloons toward unbounded as $\pi\to0$; strong-$\pi$ case shows everything agreeing; states 2SLS sits between OLS and truth as $1/(F+1)$ predicts. | Coverage numbers right; one interpretive link (unbounded behavior, or the strong-$\pi$ reconciliation) missing. | Reports coverage without reading which procedure is honest or why. | Absent, or claims the conventional CI is fine. | 18 |
| **Presentation, untestable assumptions, honest threats** | Clean prose; estimand (ATE/ATT/LATE) named before estimation; designs stated in spec-discipline format; explicitly flags CIA and exclusion as *untestable* and says what would be needed to defend them; never says "proves causation," "the data confirm exclusion," or "balance proves unconfoundedness." | One stylistic or labeling lapse. | Several lapses; estimand unnamed; untestable assumptions treated as verified. | Unreadable or rife with banned claims. | 10 |

**Total: 100 points.** (The first three Part-A criteria sum to 48; the Part-B criteria sum to 42; the
Presentation row adds 10, and the rubric is normalized so the maximum awarded is 100.)

A note on the spirit of the honesty row: this week rewards students who can say, out loud and unprompted,
*which assumptions the data can never check*. CIA (selection-on-observables) and the exclusion restriction
are the two great untestable bets of Week 3. An answer that balances covariates beautifully and then writes
"this is credible *only if* there is no unmeasured confounder like motivation, which I defend by [argument
from institutions], and which no balance table can verify" outscores a flawless balance table presented as
proof. Knowing *what kind* of claim you are making — an identified estimate under a defended assumption
versus a number dressed up as a fact — is the entire point of Week 3.

---

## Instructor answer key / model-answer sketch

**A1.** (i) By the observation rule, $\mathbb{E}[Y_i\mid D_i=1]=\mathbb{E}[Y_i(1)\mid D_i=1]$ and
$\mathbb{E}[Y_i\mid D_i=0]=\mathbb{E}[Y_i(0)\mid D_i=0]$, so
$\Delta=\mathbb{E}[Y_i(1)\mid D_i=1]-\mathbb{E}[Y_i(0)\mid D_i=0]$. Add and subtract
$\mathbb{E}[Y_i(0)\mid D_i=1]$:
$\Delta=\underbrace{(\mathbb{E}[Y_i(1)\mid D_i=1]-\mathbb{E}[Y_i(0)\mid D_i=1])}_{\text{ATT}}
+\underbrace{(\mathbb{E}[Y_i(0)\mid D_i=1]-\mathbb{E}[Y_i(0)\mid D_i=0])}_{\text{selection bias}}$.
(ii) The selection-bias term is the gap in the *untreated potential outcome* $Y(0)$ between enrollees and
non-enrollees — how the enrollees *would have* done without the program versus how the non-enrollees actually
did. It is positive here because the kind of client who signs up for risk-coaching is plausibly more
disciplined/sophisticated and would have earned higher returns *anyway*; so $\Delta$ overstates the ATT.
(iii) No — a larger client base makes $\mathbb{E}[Y\mid D=1]$ and $\mathbb{E}[Y\mid D=0]$ more *precise* but
does nothing to recover the missing counterfactual $\mathbb{E}[Y(0)\mid D=1]$; selection bias is an
identification problem, not a sampling-noise problem. *(Full credit needs the add-and-subtract step and the
"more data doesn't help" point.)*

**A2.** (i) CIA: $\{Y_i(1),Y_i(0)\}\perp\!\!\!\perp D_i\mid\mathbf{X}_i$; overlap:
$0<\Pr(D_i=1\mid\mathbf{X}_i=\mathbf{x})<1$ for all $\mathbf{x}$. Beautiful balance establishes that the
matched treated and control groups have the *same distribution of the observed $\mathbf{X}$* — the comparison
is apples-to-apples on what was measured. (ii) It can never establish that the groups have the same
distribution of $Y(0)$ given $\mathbf{X}$, i.e. that there is no *unobserved* confounder — because $Y_i(0)$
for a treated unit is exactly the counterfactual the fundamental problem says we never observe, so there is
no statistic that can confirm CIA, and balance on measured $\mathbf{X}$ says nothing about unmeasured drivers.
(iii) Not credible if motivation is omitted: motivation raises approval ($\beta_2>0$) and raises enrolling
($\delta_1>0$), so the OVB product $\beta_2\delta_1>0$ — the bias is *positive*, and matching on observables
alone **overstates** the course's effect. **CIA is the potential-outcomes name for "no omitted confounder,"
and it is untestable; defending it requires an argument from institutions that the measured $\mathbf{X}$
captures everything driving selection.** *(Credit the untestability tied to the missing counterfactual and
the correct positive OVB sign.)*

**A3.** (i) Condition on $\mathbf{X}_i$ first (law of iterated expectations). $D_i$ kills the controls, so on
treated units $Y_i=Y_i(1)$:
$\mathbb{E}\!\big[\tfrac{D_iY_i(1)}{e(\mathbf{X}_i)}\big]
=\mathbb{E}\!\big[\tfrac{1}{e(\mathbf{X}_i)}\,\mathbb{E}[D_i\mid\mathbf{X}_i]\,\mathbb{E}[Y_i(1)\mid\mathbf{X}_i]\big]$,
where the product factors *because CIA makes $D_i\perp Y_i(1)\mid\mathbf{X}_i$*. Then
$\mathbb{E}[D_i\mid\mathbf{X}_i]=e(\mathbf{X}_i)$, **the propensity score cancels**, leaving
$\mathbb{E}\big[\mathbb{E}[Y_i(1)\mid\mathbf{X}_i]\big]=\mathbb{E}[Y_i(1)]$. (ii) Weight $=1/0.04=25$: a
single observation counts as 25 people, so the treated mean is hostage to one unit's outcome and to the
accuracy of one tiny estimated probability — variance explosion from thin overlap. (iii) Two of: *trimming*
(drop $\hat e<0.01$ or $>0.99$ — but this changes the estimand to the trimmable subpopulation, so you must
report how many you dropped); *stabilized weights* (multiply by the marginal $\hat p=\Pr(D=1)$ — shrinks
weight variance without changing the estimand); *diagnose the weights* (report max weight and effective
sample size $(\sum w_i)^2/\sum w_i^2$). *(Credit the cancellation step named, weight $=25$, and one defense
with its cost.)*

**A4.** (i) IPW balances covariates *only if the propensity model is correctly specified*, and even then only
approximately in finite samples, paying for misspecification with exploding weights; entropy balancing
**solves directly for weights that make chosen covariate moments exactly equal across groups, by
construction, in every sample**, while keeping the weights as close to uniform as the constraints allow (the
max-entropy / min-KL objective), so no single unit's weight runs away. (ii) Doubly robust: the AIPW estimator
combines a *propensity model* $\hat e(\mathbf{X})$ and an *outcome model* $\hat\mu_d(\mathbf{X})$, and it is
consistent if **either one** is correctly specified — you need only one of the two right, not both. (Case
check: if the outcome model is right, the residual $Y-\hat\mu_1$ averages to zero within each $\mathbf{X}$ so
the IPW correction vanishes regardless of the wrong weights; if the propensity model is right, the correction
*is* a consistent IPW term that cancels the wrong $\hat\mu_1$.) (iii) Priya's AIPW is still consistent if her
*propensity model is correctly specified* — a wrong outcome model is survivable precisely because of the
doubly-robust property; both must be wrong for AIPW to fail. *(Credit "exact by construction vs. model-
dependent," correct AIPW reading, and the propensity-model condition.)*

**A5.** (i) First stage $=0.40-0.10=0.30$; reduced form $=-120-(-30)=-\$90$; Wald
$=\dfrac{-90}{0.30}=-\$300$. (ii) Relevance: $\operatorname{Cov}(Z,D)\neq0$ — the mailer raised completion;
*testable* via the first stage (here clearly nonzero, $0.30$). Exclusion: the mailer affects credit-card
balances *only through* course completion and is unrelated to confounders; the random mailing buys
independence from confounders for free, but the *no-direct-path* half is **untestable** and must be argued —
it could fail if recipients read budgeting tips off the flyer and improve *without* enrolling, or if the
flyer's arrival primes money-mindfulness directly. (iii) Types by $(D_i(0),D_i(1))$: never-taker $(0,0)$,
always-taker $(1,1)$, complier $(0,1)$, defier $(1,0)$. **Monotonicity** ($D_i(1)\ge D_i(0)$) rules out
defiers. The Wald number is the **LATE — the effect on compliers** (fence-sitters the mailer tipped in),
who are $30\%$ of the population (the first stage *is* the complier share). IV is blind to always-takers
(highly motivated, would enroll regardless — mailer moves them not at all) and never-takers (never enroll —
likewise unmoved), because the instrument never changes their treatment status. *(Credit Wald $=-300$, the
testable/arguable split, monotonicity, and the complier LATE with both blind groups.)*

**A6.** (i) Not a coincidence — exactly predicted. With $F=3.8$, the 2SLS bias is about
$\tfrac{1}{F+1}=\tfrac{1}{4.8}\approx0.21$ of the OLS bias, so 2SLS should sit *partway between OLS and the
truth, pulled toward OLS*: $0.42$ between $0.55$ (OLS) and the smaller true value is precisely the toward-OLS
drift. The direction is cruel because IV was supposed to *escape* the OLS bias, and a weak instrument hands
it right back — the disease dressed as the cure. (ii) The tight SE of $0.11$ is not reassuring because the
normal approximation underlying the conventional 2SLS SE breaks down at this first-stage strength; the
sampling distribution of the ratio is fat-tailed and skewed, so the reported SE is *too small* — a confident,
falsely narrow interval around a contaminated point. (iii) **Threat: weak instrument.** Because the data are
clustered, report the **Olea–Pflueger effective $F$** (cluster-robust) rather than the classical first-stage
$F$, comparing it to its critical value; and for inference use the **Anderson–Rubin** confidence interval,
which never divides by the first stage and stays valid no matter how weak the instrument is. An **unbounded**
AR interval means the instrument is too weak to identify the effect at all — the honest conclusion is "this
design cannot answer the question," not a point estimate. *(Credit the $1/(F+1)$ recognition with toward-OLS
direction, the SE dismissal, and effective-$F$ + AR + unbounded reading.)*

**Part B expected results (for grading).**

- *B1:* With $\pi=0.05$ and seed-dependent draws, OLS lands well above $0$ (around $+0.3$–$0.4$, biased up by
  the shared shock); 2SLS lands *between* OLS and $0$ (often $\approx0.2$–$0.3$); the first-stage $F$ is low
  (single digits, typically $\approx3$–$6$). The realized ratio $\hat\beta_{\text{2SLS}}/\hat\beta_{\text{OLS}}$
  should be roughly $1/(F+1)$ in order of magnitude (exact match not expected — it is a finite-sample
  approximation). Required sentence: a weak instrument makes $\hat D$ mostly first-stage noise, which is
  correlated with the structural error in finite samples, so the endogeneity leaks back in and 2SLS drifts
  toward OLS.
- *B2:* Conventional coverage of the true $0$ should be **well below 95%** — commonly $70$–$90\%$ depending on
  $\pi$ and replications — because the interval is too narrow and miscentered. Students who report coverage
  near or above $95\%$ likely built the interval wrong or used too strong a $\pi$; the *direction* (below
  nominal) is the gradeable claim.
- *B3:* AR coverage should be **near 95%** (it is honest by construction). Pushing $\pi\to0.01$ makes the AR
  interval *very wide*, running to the grid edges — i.e. effectively **unbounded**, the signature that the
  data cannot pin down $\beta$. Full credit requires a genuine *test-inversion* AR interval (regress
  $y-\beta_0x$ on $z$ for each grid $\beta_0$), **not** $\hat\beta\pm1.96\,$SE relabeled.
- *B4:* With $\pi=0.8$, the first-stage $F$ is large (well into the dozens or more), 2SLS lands near $0$
  (bias purged), and the conventional and AR intervals nearly coincide and are tight. The verdict:
  IV works when the instrument is strong; weakness — not IV itself — is what broke everything in B1–B3, and
  the first-stage $F$ / effective $F$ / AR interval are the diagnostics that tell the two cases apart.

**Quick grading heuristic.** The two highest-signal items are A2/A5 (do they correctly flag CIA and exclusion
as *untestable* — not "verified by balance" or "confirmed by the $J$ test" — and do they call the IV estimate
a *complier LATE*, not the ATE?) and B2/B3 (did the conventional coverage come out *below* nominal while the
AR coverage stayed near $95\%$, and did they build AR by real test inversion?). A student who keeps "identified
under a defended-but-untestable assumption" cleanly separate from "proven causal" — and who never trusts a
tight SE behind a single-digit $F$ — has the Week-3 mindset; the rest is execution.
