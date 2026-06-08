# Solutions — Problem Set 4.2 (Goodman-Bacon by Hand, and the Negative-Weights Crisis)

Full worked solutions to `book/weeks/week-04/ps4.2.md`, covering Chapter 4.2. Notation follows the
Conventions: TWFE regression $Y_{it} = \alpha_i + \lambda_t + \beta D_{it} + \varepsilon_{it}$;
absorbing staggered treatment $D_{it} = \mathbf{1}\{t \ge G_i\}$ with cohort $G_i$ (the period unit $i$
first switches on, $G_i = \infty$ for never-treated); genuine cell-level effect $\text{ATT}_{it}$;
group-time effect $\text{ATT}(g,t)$; event time $e = t - g$. The recurring theme of the key:
**under staggered timing with dynamic effects, the pooled $\hat\beta$ is an exact weighted average of
2×2 DiDs (Goodman-Bacon) or of cell-level effects (de Chaisemartin–D'Haultfœuille), and the forbidden
"later-vs-already-treated" comparison contaminates it; the cure is clean controls + transparent
aggregation, implemented three ways by Callaway–Sant'Anna, Sun–Abraham, and Borusyak–Jaravel–Spiess.**

**The working world (carried across Problems 1–5):** States E ($G_E = 2$), L ($G_L = 4$), U (never);
years $t = 1, \dots, 5$; per-period effect $\text{ATT}_{it} = -(e+1)$ with $e = t - G_i$; untreated
potential outcome $= 10$ throughout (parallel trends holds perfectly). Realized $Y_{it}$:

| $t$ | E | L | U |
|:---:|:---:|:---:|:---:|
| 1 | 10 | 10 | 10 |
| 2 | 9 | 10 | 10 |
| 3 | 8 | 10 | 10 |
| 4 | 7 | 9 | 10 |
| 5 | 6 | 8 | 10 |

The pooled TWFE coefficient on these 15 cells is $\hat\beta^{\text{TWFE}} = -1.25$ (given; reconstructed
exactly in Problems 3 and 4). The true overall ATT — the average of all six treated cells' effects
$(-1,-2,-3,-4,-1,-2)$ — is $-13/6 \approx -2.17$. Every arithmetic result below was verified in
`python3` (statsmodels TWFE; exact-fraction weight algebra).

---

## Problem 1 — Why TWFE is biased: name the forbidden comparison (14 pts)

**(a)** [4 pts] **Clean comparison** between E and L: the window **years 1–3**, before L adopts. In
years 1–3 State L is still untreated ($D_{Lt} = 0$ for $t < 4$), so L is a *legitimate* clean control
for the early adopter E. Here **L is the control** (untreated-in-window) and E is the treated unit. This
is a Goodman-Bacon Type-2 ("earlier-vs-later, before the later switches on") comparison.

**Forbidden comparison** for L's effect: the window **years 4–5**, after E has adopted. When L switches
on in year 4, the TWFE regression needs a unit whose status did not change — and across years 4–5 the
only other state besides the never-treated U is **State E, which is already treated** ($D_{Et} = 1$
since year 2). So E is **wrongly pressed into service as the control for newly-treated L**. E is
contaminated because it is carrying its *own* treatment effect throughout the window — it is not a clean
counterfactual for "what L would have done untreated."

**(b)** [4 pts] **Mechanism.** A 2×2 DiD attributes to the treated unit (L) the *change* in L's outcome
minus the *change* in the control's outcome over the window. When the control is already-treated E, the
"change in E's outcome over years 4–5" is not zero baseline drift — it is the **change in the
already-treated unit's effect over the window**. E's per-period effect is *still deepening*, going from
$-2$ at $t=3$ toward $-3$ at $t=4$ and $-4$ at $t=5$ — its outcome is falling fast for reasons that have
nothing to do with L. The forbidden 2×2 therefore estimates *L's true effect minus the change in E's
still-growing effect*. Because E is sliding downward faster than the freshly-treated L, L looks like it
is *rising relative to E*, and the differenced quantity flips positive — a real treatment effect (E's)
masquerading as a counterfactual trend and getting subtracted from the thing we want.

**(c)** [4 pts] **Two rescues, either one suffices:**

1. **No staggered timing** (one common adoption date for all treated units). Then there are *no
   already-treated units* available to misuse as controls during anyone else's switch-on — the forbidden
   comparison cannot be formed because no unit is treated before another's adoption date. (This rescue
   *removes the contaminated controls entirely.*)
2. **Homogeneous (constant) treatment effects** — the same constant effect for every unit at every
   horizon. Then even when already-treated E is used as a control, the "change in E's effect over the
   window" is **zero** (a constant does not change), so the contamination it injects vanishes and the
   forbidden 2×2 returns the right thing. (This rescue *makes the contamination cancel.*)

**(d)** [2 pts] Priya's real problem has a treatment effect that **builds over time** (re-underwriting is
slow, so disclosure bites harder in year three than year one) — a **dynamic / heterogeneous-across-event-time
effect**, which violates rescue 2. The working world violates **both** rescues at once: timing is
staggered ($G_E = 2 \ne 4 = G_L$, violating rescue 1) *and* the effect builds, $-(e+1)$ growing in $|e|$
(violating rescue 2). So it is the genuine danger case — exactly the recipe for the crisis.

---

## Problem 2 — The four kinds of 2×2 and their values (18 pts)

All cell means read straight from the table.

**(a)** [6 pts] **Treated-vs-never-treated (clean, Type 1).**

**(A) E vs U.** Pre $= \{1\}$, post $= \{2,3,4,5\}$.
$$\bar Y_{E,\text{post}} = \tfrac{9+8+7+6}{4} = 7.5,\quad \bar Y_{E,\text{pre}} = 10,\quad \bar Y_{U,\text{post}} = 10,\quad \bar Y_{U,\text{pre}} = 10.$$
$$\widehat{\text{DiD}}_A = (7.5 - 10) - (10 - 10) = \mathbf{-2.5}.$$

**(B) L vs U.** Pre $= \{1,2,3\}$, post $= \{4,5\}$.
$$\bar Y_{L,\text{post}} = \tfrac{9+8}{2} = 8.5,\quad \bar Y_{L,\text{pre}} = 10,\quad \bar Y_{U,\text{post}} = 10,\quad \bar Y_{U,\text{pre}} = 10.$$
$$\widehat{\text{DiD}}_B = (8.5 - 10) - (10 - 10) = \mathbf{-1.5}.$$

Both are clean: U is genuinely untreated throughout, so each DiD is an honest estimate of the average
treated-period effect for that cohort (E's average effect over $e=0,1,2,3$ is $-2.5$; L's average over
$e=0,1$ is $-1.5$ — exactly the truth).

**(b)** [4 pts] **Early-vs-late, before late adopts (clean, Type 2).**

**(C) E (treated) vs L (control).** Pre $= \{1\}$, post $= \{2,3\}$.
$$\bar Y_{E,\text{post}} = \tfrac{9+8}{2} = 8.5,\quad \bar Y_{E,\text{pre}} = 10,\quad \bar Y_{L,\text{post}} = 10,\quad \bar Y_{L,\text{pre}} = 10.$$
$$\widehat{\text{DiD}}_C = (8.5 - 10) - (10 - 10) = \mathbf{-1.5}.$$
**Why L is a legitimate control here:** in years 1–3 L has not yet adopted ($t < G_L = 4$), so $D_{Lt} =
0$ — L is *not-yet-treated* and therefore untreated *throughout this window*. A not-yet-treated unit is
a clean control as long as the window ends before its own adoption.

**(c)** [4 pts] **Late-vs-early, after early adopts (FORBIDDEN, Type 3).**

**(D) L (treated) vs E (control).** Pre $= \{2,3\}$, post $= \{4,5\}$.
$$\bar Y_{L,\text{post}} = \tfrac{9+8}{2} = 8.5,\quad \bar Y_{L,\text{pre}} = \tfrac{10+10}{2} = 10,$$
$$\bar Y_{E,\text{post}} = \tfrac{7+6}{2} = 6.5,\quad \bar Y_{E,\text{pre}} = \tfrac{9+8}{2} = 8.5.$$
$$\widehat{\text{DiD}}_D = (8.5 - 10) - (6.5 - 8.5) = (-1.5) - (-2.0) = \mathbf{+0.5}.$$
**Positive** — even though disclosure lowered non-renewals in every treated cell. The driver: across the
window State E's outcome drops by $2.0$ ($8.5 \to 6.5$), because **E's own treatment effect is still
deepening** ($-2 \to -4$). L's outcome drops by only $1.5$. So differencing L against the
faster-falling already-treated E makes L look like it *rose*, and the 2×2 flips positive. The forbidden
comparison subtracts E's still-growing effect from L's.

**(d)** [4 pts] **Side by side:**

| 2×2 | treated | control | window | control status | DiD | clean / forbidden |
|:---:|:---:|:---:|:---:|:---|:---:|:---:|
| A | E | U | $\{1\}\!\to\!\{2,3,4,5\}$ | never-treated | $-2.5$ | **clean** |
| B | L | U | $\{1,2,3\}\!\to\!\{4,5\}$ | never-treated | $-1.5$ | **clean** |
| C | E | L | $\{1\}\!\to\!\{2,3\}$ | not-yet-treated (clean in window) | $-1.5$ | **clean** |
| D | L | E | $\{2,3\}\!\to\!\{4,5\}$ | **already-treated** | $+0.5$ | **forbidden** |

The entire source of bias is **comparison D**: it alone uses an already-treated unit (E) as the control.
Its $+0.5$ pulls *against* the three negative clean DiDs. With enough weight on D (positive while the
truth is negative), it drags $\hat\beta$ toward zero, and — given enough weight, as in the chapter's
two-state world — past zero into the wrong sign.

---

## Problem 3 — The Goodman-Bacon weights, and TWFE as a weighted average (22 pts)

**(a)** [8 pts] Plug $\bar D_E = 4/5$, $\bar D_L = 2/5$ into the four (unnormalized) weight expressions.

$$s_A \propto \bar D_E(1-\bar D_E) = \tfrac45\cdot\tfrac15 = \tfrac{4}{25}.$$
$$s_B \propto \bar D_L(1-\bar D_L) = \tfrac25\cdot\tfrac35 = \tfrac{6}{25}.$$
$$s_C \propto (1-\bar D_L)^2\cdot\frac{\bar D_E - \bar D_L}{1-\bar D_L}\cdot\frac{1-\bar D_E}{1-\bar D_L}
= (\bar D_E - \bar D_L)(1-\bar D_E) = \big(\tfrac45-\tfrac25\big)\big(\tfrac15\big) = \tfrac25\cdot\tfrac15 = \tfrac{2}{25}.$$
$$s_D \propto \bar D_E^{\,2}\cdot\frac{\bar D_L}{\bar D_E}\cdot\frac{\bar D_E - \bar D_L}{\bar D_E}
= \bar D_L(\bar D_E - \bar D_L) = \tfrac25\cdot\big(\tfrac45-\tfrac25\big) = \tfrac25\cdot\tfrac25 = \tfrac{4}{25}.$$

Sum: $S = \dfrac{4 + 6 + 2 + 4}{25} = \dfrac{16}{25}$. Normalize ($w_k = s_k/S$):

$$w_A = \frac{4/25}{16/25} = \frac{4}{16} = \tfrac14 = 0.250,\qquad
w_B = \frac{6}{16} = \tfrac38 = 0.375,$$
$$w_C = \frac{2}{16} = \tfrac18 = 0.125,\qquad
w_D = \frac{4}{16} = \tfrac14 = 0.250.$$

Check: $0.250 + 0.375 + 0.125 + 0.250 = 1.000$. ✓

**(b)** [6 pts] **Reconstruct $\hat\beta$** as $\sum_k w_k\,\widehat{\text{DiD}}_k$ using Problem-2 values
$(-2.5, -1.5, -1.5, +0.5)$:
$$
\hat\beta = \underbrace{\tfrac14(-2.5)}_{-0.625} + \underbrace{\tfrac38(-1.5)}_{-0.5625} + \underbrace{\tfrac18(-1.5)}_{-0.1875} + \underbrace{\tfrac14(+0.5)}_{+0.125}.
$$
Sum: $-0.625 - 0.5625 - 0.1875 + 0.125 = \mathbf{-1.25}$. ✓ Exactly the pooled
$\hat\beta^{\text{TWFE}}$ — this is Goodman-Bacon's identity, an exact equality with no error term. (In
fractions: $-\tfrac58 - \tfrac9{16} - \tfrac3{16} + \tfrac18 = -\tfrac{20}{16} = -\tfrac54$.)

**(c)** [4 pts] Reading the weights as a diagnostic.
(i) The **largest** weight is $w_B = 3/8$ on the clean L-vs-never comparison — but note the **forbidden**
comparison D carries a hefty $w_D = 1/4$, *tied for second* and equal to the clean A. The weighting is
driven purely by treatment-timing variance, not by trustworthiness.
(ii) Total weight on the forbidden comparison: $w_D = 0.25$. Its signed contribution is
$w_D \cdot \widehat{\text{DiD}}_D = 0.25 \times (+0.5) = +0.125$. The true overall ATT is $-13/6 \approx
-2.17$, but $\hat\beta = -1.25$ — **attenuated toward zero by about $0.92$** (exactly $-13/6-(-5/4)=-11/12\approx-0.917$). The forbidden term
contributes $+0.125$ directly, and (more importantly) it forces the clean comparisons to be the
*averages over treated periods* $-2.5$ and $-1.5$ rather than the deeper truth; the net effect is that
$\hat\beta$ understates the true effect by a wide margin even though, here, the sign survives.

**(d)** [4 pts] **Delete U.** With only States E and L, the pair $(E, L)$ is the *only* pair, so the
treated-vs-never blocks A and B vanish; only the within-pair sub-comparisons C and D remain. Renormalize
over $\{s_C, s_D\} = \{2/25, 4/25\}$:
$$w_C = \frac{2/25}{6/25} = \tfrac13,\qquad w_D = \frac{4/25}{6/25} = \tfrac23.$$
$$\hat\beta = \tfrac13(-1.5) + \tfrac23(+0.5) = -0.5 + 0.333\overline{3} = \mathbf{-\tfrac16} \approx -0.167.$$
(Verified directly against a TWFE regression on the two-state, five-year panel: $-0.1\overline{6}$.) The
situation is **strictly worse**: removing the clean never-treated control U strips out the two clean
treated-vs-never blocks, so the forbidden comparison's weight *jumps from $1/4$ to $2/3$* — it now
dominates the average. The estimate collapses from $-1.25$ to $-0.167$, almost on top of zero. Lengthen
the horizon (the chapter's eight-year version, $G_E = 2$, $G_L = 5$, $t = 1,\dots,8$) and the forbidden
comparison's positive contamination grows enough to push $\hat\beta$ all the way to **$+0.40$** — a full
sign flip. Losing the never-treated unit is precisely the condition that lets the forbidden comparison
become the *only* game in town for the late cohort, which is what completes the disaster.

---

## Problem 4 — The negative-weights view: de Chaisemartin–D'Haultfœuille (16 pts)

**(a)** [4 pts] **Weights sum to one:**
$$0.25 + 0.25 + (-0.0625) + (-0.0625) + 0.3125 + 0.3125 = 1.0000.\;\checkmark$$
**Weighted average of cell effects:**
$$\sum w_{it}\text{ATT}_{it} = 0.25(-1) + 0.25(-2) + (-0.0625)(-3) + (-0.0625)(-4) + 0.3125(-1) + 0.3125(-2).$$
Term by term: $-0.25 - 0.50 + 0.1875 + 0.25 - 0.3125 - 0.625 = \mathbf{-1.25}$. ✓ The same
$\hat\beta^{\text{TWFE}}$, now reconstructed a *third* way (after the by-hand TWFE and the Goodman-Bacon
2×2 average). One number, three identical decompositions.

**(b)** [5 pts] **The negative weights** are $w = -0.0625$ on **cells 3 and 4**: State **E** in years
**4 and 5**, which are E's event-time $e = 2$ and $e = 3$ cells — i.e., the **early cohort's
late-period cells**, the part of E's treated history that overlaps L's treated window. **Bridge to
Problem 2:** these are *exactly* the cells where already-treated E served as the contaminated control in
the forbidden Type-3 comparison D. In the Goodman-Bacon view, D used E's years 4–5 as L's control; in
the de Chaisemartin–D'Haultfœuille view, those same cells receive *negative* cell weights. The two
decompositions are the same disease seen through two lenses: pairing $\to$ a forbidden 2×2; cell-by-cell
$\to$ a negative weight on the cells doing the forbidden control duty.

**(c)** [4 pts] **The dCDH warning.** Because all six $\text{ATT}_{it}$ are strictly negative but two
weights are negative, the weighted sum is *not* a sensible average of the effects — and in principle the
**sign of $\hat\beta$ can be opposite to the sign of every individual effect.** A weighted average with
negative weights is not bounded between the min and max of the things it averages. Made concrete by the
chapter's neighbor world (eight years, no never-treated state): there *every* true cell effect is
negative (disclosure helps everyone, every year), yet $\hat\beta = +0.40$ — the estimate says the policy
*raised* non-renewals. All true effects negative; estimate positive.

**(d)** [3 pts] **The diagnostic.** Because $w_{it}$ depends only on the **design** — who is treated when
— and not at all on the (unknown) treatment effects, the researcher can **compute every weight from the
treatment-assignment pattern alone, before estimating a single effect.** She counts how many weights are
negative and how much total negative weight there is; if a meaningful share is negative, $\hat\beta$ is
uninterpretable and she should not report it. The ordering matters: computing weights *first* (from
design) and effects *second* makes this a genuine **pre-commitment check** — she cannot be accused of
fishing for a decomposition that excuses a result she already saw, because the weights were fixed by the
adoption calendar before any outcome entered the calculation.

---

## Problem 5 — Callaway–Sant'Anna: clean ATT(g,t) and event-time aggregation (18 pts)

**(a)** [4 pts] **Meaning of the arguments.** $\text{ATT}(g,t)$ is the average treatment effect, at
**calendar time $t$**, on the cohort that **first adopted in year $g$** (i.e., all units with $G_i =
g$). The first argument $g$ says *which group* (defined by its adoption year); the second $t$ says *when
you are measuring*. Symbolically,
$$\text{ATT}(g,t) = \mathbb{E}\big[\,Y_{it}(g) - Y_{it}(\infty)\ \big|\ G_i = g\,\big],$$
the expected gap, for the cohort-$g$ units, between their realized (treated-from-$g$) outcome and their
never-treated potential outcome, at time $t$. **Event time** is $e = t - g$ (years since adoption);
$e = 0$ is the first treated year. **Eligible clean controls** for cohort $g$ at time $t$: units that are
**never-treated** ($G_i = \infty$) or **not-yet-treated** at $t$ (those with $G_i > t$, still untreated
through the whole comparison window). **Forbidden:** any already-treated unit, i.e. any unit with
$g' \le t$ and $g' \ne g$ — in particular an *earlier* cohort.

**(b)** [8 pts] **The clean group-time grid.** Baseline period for cohort $g$ is $g - 1$.

*Cohort E ($g = 2$), control = U (never), baseline $t = 1$:*
$$\widehat{\text{ATT}}(2,2) = (Y_{E,2} - Y_{E,1}) - (Y_{U,2} - Y_{U,1}) = (9-10) - (10-10) = \mathbf{-1}\quad(e=0,\ \text{true } -1)$$
$$\widehat{\text{ATT}}(2,3) = (8-10) - (10-10) = \mathbf{-2}\quad(e=1,\ \text{true } -2)$$
$$\widehat{\text{ATT}}(2,4) = (7-10) - (10-10) = \mathbf{-3}\quad(e=2,\ \text{true } -3)$$
$$\widehat{\text{ATT}}(2,5) = (6-10) - (10-10) = \mathbf{-4}\quad(e=3,\ \text{true } -4)$$
(For $t = 2, 3$ you may instead use the not-yet-treated L as control — $Y_{L,t} = 10$ there — and get
the identical answer, since L is still untreated before year 4.)

*Cohort L ($g = 4$), control = U (never), baseline $t = 3$ — **never** the already-treated E:*
$$\widehat{\text{ATT}}(4,4) = (Y_{L,4} - Y_{L,3}) - (Y_{U,4} - Y_{U,3}) = (9-10) - (10-10) = \mathbf{-1}\quad(e=0,\ \text{true } -1)$$
$$\widehat{\text{ATT}}(4,5) = (8-10) - (10-10) = \mathbf{-2}\quad(e=1,\ \text{true } -2)$$

Every clean group-time estimate hits the true effect **exactly**, because each is a Type-1 (or Type-2)
clean DiD against a genuinely untreated control — no forbidden Type-3 comparison is ever formed, so there
is no contamination to bias the estimate. This is the unbiasedness TWFE lacked.

**(c)** [4 pts] **Event-time aggregation** $e = t - g$ (equal cohort sizes → simple averages across
cohorts sharing an $e$):
$$\widehat{\text{ATT}}^{\text{es}}(0) = \tfrac{(-1) + (-1)}{2} = -1,\quad
\widehat{\text{ATT}}^{\text{es}}(1) = \tfrac{(-2) + (-2)}{2} = -2,$$
$$\widehat{\text{ATT}}^{\text{es}}(2) = -3\ (\text{only E}),\quad
\widehat{\text{ATT}}^{\text{es}}(3) = -4\ (\text{only E}).$$
**Overall ATT** (simple average of all six group-time effects):
$$\frac{(-1) + (-2) + (-3) + (-4) + (-1) + (-2)}{6} = \frac{-13}{6} \approx \mathbf{-2.17}.$$
Exactly the truth. Contrast with the broken pooled $\hat\beta^{\text{TWFE}} = -1.25$: the clean
estimator is **right** ($-2.17$); TWFE got the sign right here but **attenuated the magnitude by about
40%**, understating how much the disclosure rule helped. (And in the no-never-treated world TWFE got the
sign wrong entirely.)

**(d)** [2 pts] In the two-state world (E, L only, no U), Callaway–Sant'Anna reports
$\widehat{\text{ATT}}(4, t)$ for State L as **not identified / undefined** — it *refuses to compute it*,
because L's only available comparison unit is the already-treated E, and the method forbids using an
already-treated unit as a control. This **refusal is a feature**: when no clean counterfactual exists,
the honest answer is "this effect is not identified," not a fabricated number. TWFE, by contrast, *did*
produce a number from the same two states ($-0.167$, nearly flipped) by silently forming the forbidden
comparison — manufacturing an answer where the data contain none.

---

## Problem 6 — Which estimator, and diagnosing a contaminated event study (12 pts)

**(a)** [3 pts] **Sun–Abraham (2021)** — the interaction-weighted (IW) estimator. It stays inside a
single event-study regression, so it changes the least code. The mechanism: instead of one coefficient
$\beta_e$ per relative-time dummy, **saturate** the regression by interacting every relative-time dummy
with every cohort indicator, estimating a separate coefficient $\delta_{g,e}$ for each (cohort $g$,
event-time $e$) pair against never-treated (or last-treated) controls, then aggregate the $\delta_{g,e}$
to event-time effects with **cohort-share weights** (the "interaction weighting"). Because each cohort's
dynamics are estimated *separately* before averaging, no cohort's effect at one event time can leak into
another cohort's coefficient at a different event time — the cohort bleed is shut off.

**(b)** [3 pts] **Borusyak–Jaravel–Spiess (2024)** — the imputation estimator, which they show is
(under their assumptions) the *efficient* one. Three steps: (1) **fit** the two-way FE model
$Y_{it} = \alpha_i + \lambda_t + \varepsilon_{it}$ using **only untreated cells** ($D_{it} = 0$: all
never-treated cells plus every adopter's pre-adoption years); (2) **impute** each treated cell's missing
untreated outcome $\hat Y_{it}(0) = \hat\alpha_i + \hat\lambda_t$; (3) **difference**
$\hat\tau_{it} = Y_{it} - \hat Y_{it}(0)$ and average the $\hat\tau_{it}$ with explicit weights. The
$\hat\alpha_i, \hat\lambda_t$ are uncontaminated **because the treated cells are excluded from the fit** —
no treatment effect ever enters the estimation of the fixed effects that serve as the counterfactual,
which is exactly what pooled TWFE failed to do (it fit on *all* cells, letting treated cells corrupt the
FE that double as everyone's control). Its pre-trend test is built from the untreated residuals, so it
is not contaminated.

**(c)** [4 pts] **Diagnosis.** Priya is *not* seeing a real parallel-trends violation — she is seeing
**Sun–Abraham contamination of the naive event study**. Under staggered timing with heterogeneous/dynamic
effects, each estimated pre-period coefficient $\hat\beta_e$ in a naive TWFE event study is **polluted by
treatment effects from *other* event times of *other* cohorts** — the leads and lags bleed into one
another through the same forbidden later-vs-already-treated comparisons. A coefficient nominally at
$e = -2$ can pick up some other cohort's $e = +1$ effect, manufacturing a slope in the pre-periods even
when the true pre-trends are dead flat. So her "funny pre-trends" are an *artifact of the estimator*, not
evidence her design is broken. **What she should run:** a heterogeneity-robust event study — Sun–Abraham
IW, Callaway–Sant'Anna aggregated by event time, or Borusyak–Jaravel–Spiess — each of which estimates
cohort dynamics in isolation against clean controls. **What the corrected plot should show:** if parallel
trends really holds, the pre-period coefficients ($e < 0$) should sit **near zero** (a genuine
placebo/pre-trend check), and only the post-period coefficients should trace the building disclosure
effect.

**(d)** [2 pts] **Spec-discipline upgrade (Conventions §4, extended).** A staggered-DiD write-up must now
state two choices a plain 2×2 did not need: (1) **name the control group** — are the clean comparisons
against *never-treated* units, *not-yet-treated* units, or both (this matters because never-adopters may
differ systematically, while not-yet-treated adopters are often a more credible counterfactual but shrink
the control pool as cohorts switch on); and (2) **name the aggregation weights** — event-time average,
calendar-time average, or a single overall ATT, and how cohorts were weighted into the headline number.
The identifying assumption is **parallel trends stated per cohort**: each adopting cohort's untreated
potential outcome would have moved parallel to its clean control group's, in every comparison window.

---

*End of solutions for Problem Set 4.2. Three independent decompositions of the same pooled
$\hat\beta = -1.25$ — by-hand TWFE, the Goodman-Bacon 2×2 average (weights $\tfrac14,\tfrac38,\tfrac18,\tfrac14$
on DiDs $-2.5, -1.5, -1.5, +0.5$), and the de Chaisemartin–D'Haultfœuille cell-weight sum (two weights
negative) — all land on the identical number, and all trace the bias to one culprit: the forbidden
later-vs-already-treated comparison ($+0.5$, the only positive piece). The Callaway–Sant'Anna clean grid
recovers the true $-13/6 \approx -2.17$ exactly. Goodman-Bacon (2021), de Chaisemartin and
D'Haultfœuille (2020), Sun and Abraham (2021), Callaway and Sant'Anna (2021), and Borusyak, Jaravel, and
Spiess (2024) are four diagnostics and three cures for one disease.*
