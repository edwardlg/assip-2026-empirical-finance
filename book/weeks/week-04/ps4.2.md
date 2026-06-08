# Problem Set 4.2 — Goodman-Bacon by Hand, and the Negative-Weights Crisis

**Covers Chapter 4.2 (The Staggered-Adoption Crisis).** Methods through Ch 4.2 only: the two-way
fixed-effects (TWFE) regression $Y_{it} = \alpha_i + \lambda_t + \beta D_{it} + \varepsilon_{it}$ with
an absorbing, staggered treatment $D_{it} = \mathbf{1}\{t \ge G_i\}$ (cohort $G_i$ = the period unit $i$
first switches on, $G_i = \infty$ for never-treated); the **forbidden comparison** (an
already-treated unit used as a control); the **Goodman-Bacon decomposition** of $\hat\beta^{\text{TWFE}}$
into a timing-variance-weighted average of 2×2 DiDs; the **de Chaisemartin–D'Haultfœuille** cell-weight
view (the same $\hat\beta$ as a weighted average of cell-level effects, with weights that can be
negative); the **Callaway–Sant'Anna** group-time average treatment effect $\text{ATT}(g,t)$ estimated
against clean (never- or not-yet-treated) controls and aggregated by event time $e = t - g$; and the
**Sun–Abraham** and **Borusyak–Jaravel–Spiess** routes to the same clean-control fix. Notation follows
the Conventions. The genuine cell-level effect is $\text{ATT}_{it}$; the true overall effect averages it
over treated cells.

Six problems, escalating, **100 points total**. Every numerical input is supplied so you can work the
whole thing by hand — no computer needed (the companion notebook `nb4.2` lets you check Problems 2–4 by
simulation). **The grading rule of this set:** a TWFE coefficient, a 2×2 DiD, or a weight reported
*without naming which comparison it comes from and whether that comparison is clean or forbidden* earns
half credit at most. As in Chapter 4.1, the *reasoning about which comparison identifies what* is the
skill, not the arithmetic. Whenever you name a threat, name the design that addresses it (spec
discipline, Conventions §4 — extended in Ch 4.2 to require naming the **control group** and the
**aggregation weights**).

Several problems share one small world, defined once here so you can carry the numbers between them.

> **Priya's stylized disclosure panel (the working world).** Priya studies a climate-risk-disclosure
> rule for property insurers; her outcome $Y_{it}$ is the non-renewal rate (lower is better) in state
> $i$, year $t$. Three states, six possible years $t = 1, \dots, 5$ (we use five to keep the
> arithmetic by-hand). State **E** ("early") adopts in year $G_E = 2$; state **L** ("late") adopts in
> year $G_L = 4$; state **U** never adopts ($G_U = \infty$). Disclosure *helps* and helps *more the
> longer it has been in force*: the per-period treatment effect at event time $e = t - G_i$ is
> $\text{ATT}_{it} = -(e+1)$, i.e. $-1$ in the first treated year, $-2$ in the second, $-3$ in the
> third, and so on (negative and **building** — the dynamic effect that is the whole crux of the
> crisis). Untreated potential outcome is $10$ in every state-year, so **parallel trends holds
> perfectly**. The realized outcomes are:

| Year $t$ | State E ($G=2$) | State L ($G=4$) | State U (never) |
|:---:|:---:|:---:|:---:|
| 1 | $10$ | $10$ | $10$ |
| 2 | $10-1=9$ | $10$ | $10$ |
| 3 | $10-2=8$ | $10$ | $10$ |
| 4 | $10-3=7$ | $10-1=9$ | $10$ |
| 5 | $10-4=6$ | $10-2=8$ | $10$ |

> Treat each state as one unit, so all three cohorts have equal size — this makes the Goodman-Bacon
> weights pure functions of *timing*, exactly the point. The TWFE regression run on these 15
> observations returns $\hat\beta^{\text{TWFE}} = -1.25$ (you will not be asked to two-way-demean all
> 15 cells by hand; that number is given, and Problem 3 reconstructs it from the 2×2 pieces).

---

## Problem 1 — Why TWFE is biased: name the forbidden comparison (14 points)

This problem is pure reasoning — no arithmetic. It pins down *why* the pooled $\hat\beta$ misbehaves
before you compute anything.

**(a)** [4 pts] In the working world, the TWFE regression must find a control group for State L when L
switches on in year 4. Using only the data in the table, name the years that form a **clean** 2×2
comparison between States E and L (one in which the unit playing "control" is genuinely untreated
throughout the window), and say which state is the control there. Then name the years that form the
**forbidden** comparison for L's effect, and say which state is wrongly pressed into service as the
control and *why* that makes it contaminated.

**(b)** [4 pts] Explain in two or three sentences the mechanism by which the forbidden comparison
biases $\hat\beta$ — i.e., what quantity the forbidden 2×2 actually estimates instead of L's treatment
effect. Use the phrase "change in the already-treated unit's effect over the window," and connect it to
the fact that E's per-period effect is *still deepening* (from $-2$ toward $-4$) across years 4–5.

**(c)** [4 pts] State the **two distinct conditions**, *either* of which would rescue the pooled TWFE
coefficient under staggered timing. For each, explain in one sentence why the forbidden comparison stops
doing damage. (Hint: one condition removes already-treated controls from the data entirely; the other
makes the contamination they inject equal to zero.)

**(d)** [2 pts] The crisis was hidden for thirty years partly because textbook examples had at least one
of those two conditions quietly switched on. State which of the two conditions Priya's *real* problem
violates, and confirm in one clause that the working world above violates *both* of the rescues from
(c) at once (so it is the genuine danger case).

---

## Problem 2 — The four kinds of 2×2 and their values (18 points)

Goodman-Bacon (2021) proves $\hat\beta^{\text{TWFE}}$ is *identically* a weighted average of every simple
2×2 DiD the staggered data can form. First you must build those 2×2s and see which are clean and which
are poison. Use the working world.

A 2×2 difference-in-differences with treated unit $A$, control unit $B$, pre-period set $\mathcal P$, and
post-period set $\mathcal Q$ is
$$\widehat{\text{DiD}} = \big(\bar Y_{A,\mathcal Q} - \bar Y_{A,\mathcal P}\big) - \big(\bar Y_{B,\mathcal Q} - \bar Y_{B,\mathcal P}\big).$$

**(a)** [6 pts] Compute the two **treated-vs-never-treated** 2×2s (Goodman-Bacon's clean "Type 1"):
- **(A)** State E vs State U. Pre = $\{1\}$ (before E adopts), post = $\{2,3,4,5\}$.
- **(B)** State L vs State U. Pre = $\{1,2,3\}$ (before L adopts), post = $\{4,5\}$.

Show the four cell means in each and the resulting DiD.

**(b)** [4 pts] Compute the **early-vs-late, before the late group adopts** 2×2 (Goodman-Bacon's clean
"Type 2"):
- **(C)** State E (treated) vs State L (control), pre = $\{1\}$, post = $\{2,3\}$.

Here L is the control. Explain in one sentence why L is a *legitimate* control in this specific window,
even though L is itself an eventual adopter.

**(c)** [4 pts] Compute the **late-vs-early, after the early group has adopted** 2×2 (Goodman-Bacon's
"Type 3" — the **forbidden** one):
- **(D)** State L (treated) vs State E (control), pre = $\{2,3\}$, post = $\{4,5\}$.

Report the number. It should make you uncomfortable: the policy helped both states in every treated
year, yet this 2×2 comes out *positive*. In one sentence, say what about State E across years 2–5 drives
the wrong sign.

**(d)** [4 pts] Lay the four DiDs side by side ($\text{A}, \text{B}, \text{C}, \text{D}$) and label each
**clean** or **forbidden**, identifying which unit serves as the control and whether that unit is
untreated-in-window or already-treated. State which single comparison is the entire source of the bias,
and what its sign would have to be (relative to the others) for it to drag $\hat\beta$ toward zero or
past it.

---

## Problem 3 — The Goodman-Bacon weights, and TWFE as a weighted average (22 points)

Now assemble the decomposition: show that the one number $\hat\beta^{\text{TWFE}} = -1.25$ *is* a
particular weighted average of the four 2×2 DiDs from Problem 2, with weights driven entirely by
treatment-timing variance.

For a balanced panel with equal-size cohorts, write $\bar D_k$ for the **share of periods cohort $k$
spends treated**. Over $t = 1, \dots, 5$: cohort E is treated in years $2$–$5$, so $\bar D_E = 4/5$;
cohort L is treated in years $4$–$5$, so $\bar D_L = 2/5$; cohort U is never treated. The (unnormalized)
Goodman-Bacon weight attached to each 2×2 building block, for equal cohort shares, is proportional to:

$$
\begin{aligned}
\text{(A) E vs never:} && s_A &\propto \bar D_E\,(1 - \bar D_E),\\
\text{(B) L vs never:} && s_B &\propto \bar D_L\,(1 - \bar D_L),\\
\text{(C) E vs L, pre-L (clean):} && s_C &\propto (1-\bar D_L)^2\cdot\frac{(\bar D_E - \bar D_L)}{(1-\bar D_L)}\cdot\frac{(1-\bar D_E)}{(1-\bar D_L)},\\
\text{(D) L vs E, post-E (forbidden):} && s_D &\propto \bar D_E^{\,2}\cdot\frac{\bar D_L}{\bar D_E}\cdot\frac{(\bar D_E - \bar D_L)}{\bar D_E}.
\end{aligned}
$$

(These are Goodman-Bacon's variance weights specialized to three equal cohorts with a never-treated
group; the common factor that cancels on normalization has been dropped. You do **not** need to derive
them — you need to plug in and see what they say.)

**(a)** [8 pts] Plug $\bar D_E = 4/5$ and $\bar D_L = 2/5$ into the four expressions and simplify each to
a single fraction. Then **normalize** so the four weights sum to one: $w_k = s_k / (s_A + s_B + s_C +
s_D)$. Present the four normalized weights $w_A, w_B, w_C, w_D$ as clean fractions or decimals, and
confirm they sum to $1$.

**(b)** [6 pts] Form the weighted average $\sum_k w_k \,\widehat{\text{DiD}}_k$ using your Problem-2
DiD values and your Problem-3(a) weights, and verify it equals $\hat\beta^{\text{TWFE}} = -1.25$ to the
decimal. Write the arithmetic out term by term. (This is Goodman-Bacon's exact identity — not an
approximation, an equality.)

**(c)** [4 pts] Read the weights as a *diagnostic*. (i) Which single comparison carries the largest
weight, and is it clean or forbidden? (ii) What total weight sits on the forbidden comparison, and what
*signed contribution* ($w_D \cdot \widehat{\text{DiD}}_D$) does it add to $\hat\beta$? State in one
sentence how the true overall ATT ($-13/6 \approx -2.17$, the average of all six cells' true effects)
compares to $\hat\beta = -1.25$, and attribute the gap to the forbidden term.

**(d)** [4 pts] Now the punchline that the *chapter* used: **delete State U** so that no never-treated
unit exists. With only States E and L, only the single pair $(E, L)$ survives, contributing just the two
sub-comparisons C and D; their weights renormalize to $w_C = 1/3$, $w_D = 2/3$. Recompute
$\hat\beta = w_C\,\widehat{\text{DiD}}_C + w_D\,\widehat{\text{DiD}}_D$ for this two-state world, and
state in one sentence *why* removing the clean never-treated control makes the situation strictly worse —
i.e., what happens to the forbidden comparison's weight, and why losing U is exactly the condition that
let the chapter's eight-year version flip the sign all the way to $+0.40$.

---

## Problem 4 — The negative-weights view: de Chaisemartin–D'Haultfœuille (16 points)

Goodman-Bacon decomposes $\hat\beta$ by *pairs of cohorts*. de Chaisemartin and D'Haultfœuille (2020)
decompose the *same* $\hat\beta$ a different way — as a weighted average over individual **treated
cells** $(i,t)$:
$$\hat\beta^{\text{TWFE}} \;\xrightarrow{p}\; \sum_{(i,t):\,D_{it}=1} w_{it}\,\text{ATT}_{it}, \qquad \sum_{(i,t):\,D_{it}=1} w_{it} = 1,$$
where $\text{ATT}_{it}$ is the genuine effect in that cell and the weights $w_{it}$ **sum to one but need
not be positive.** The weights come from residualizing $D_{it}$ on the two-way fixed effects (the
Frisch–Waugh–Lovell step from Chapter 2.3): the weight on a treated cell is its FWL-residualized
treatment, normalized to sum to one over treated cells. For the working world (E, L, U; $t=1,\dots,5$),
those residualized weights work out to:

| Treated cell | State | $t$ | event time $e$ | $w_{it}$ | $\text{ATT}_{it}$ (true) |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | E | 2 | $0$ | $+0.2500$ | $-1$ |
| 2 | E | 3 | $1$ | $+0.2500$ | $-2$ |
| 3 | E | 4 | $2$ | $-0.0625$ | $-3$ |
| 4 | E | 5 | $3$ | $-0.0625$ | $-4$ |
| 5 | L | 4 | $0$ | $+0.3125$ | $-1$ |
| 6 | L | 5 | $1$ | $+0.3125$ | $-2$ |

**(a)** [4 pts] Confirm the weights sum to $1$, and verify $\sum w_{it}\,\text{ATT}_{it} = -1.25$, the
same $\hat\beta^{\text{TWFE}}$ you reconstructed two ways already. Write out the six-term sum.

**(b)** [5 pts] Identify the **negative weights**: which two cells carry them, which cohort do they
belong to, and what is special about those cells in event-time terms? Connect this directly to Problem 2:
explain in two sentences why the cells getting negative weight are *exactly* the early cohort's
late-period cells (E in years 4–5) that served as the contaminated control in the forbidden Type-3
comparison. (This is the bridge between the two decompositions — same disease, two diagnostics.)

**(c)** [4 pts] State the de Chaisemartin–D'Haultfœuille warning precisely: because every
$\text{ATT}_{it}$ here is strictly negative but some $w_{it}$ are negative, what could in principle
happen to the *sign* of $\hat\beta$? Use the working world's neighbor — the chapter's eight-year,
no-never-treated world where $\hat\beta = +0.40$ — to make the point concrete in one sentence: all true
effects negative, estimate positive.

**(d)** [3 pts] de Chaisemartin and D'Haultfœuille stress that the weights $w_{it}$ depend **only on the
design** (who is treated when), not on the treatment effects. State the practical diagnostic this hands
the researcher, and say *what she can compute before estimating a single treatment effect* — and why
that ordering (weights first, effects second) is what makes it a genuine pre-commitment check rather
than a post-hoc rationalization.

---

## Problem 5 — Callaway–Sant'Anna: clean ATT(g,t) and event-time aggregation (18 points)

The cure. Callaway and Sant'Anna (2021) build the **group-time average treatment effect**
$\text{ATT}(g,t)$ — the effect at calendar time $t$ on the cohort that first adopted in year $g$ —
directly from clean 2×2s, and aggregate them with weights chosen on purpose. For cohort $g$ and a
post-period $t \ge g$, comparing to the period just before $g$ adopted:
$$
\widehat{\text{ATT}}(g,t) = \big(\bar Y_{g,t} - \bar Y_{g,\,g-1}\big) - \big(\bar Y_{C,t} - \bar Y_{C,\,g-1}\big),
$$
where the control group $C$ is **never-treated or not-yet-treated** units — *never* an already-treated
unit. Use the working world (E, L, U; $t = 1,\dots,5$).

**(a)** [4 pts] Define, in your own words and then symbolically, what the two arguments of
$\text{ATT}(g,t)$ mean, and what **event time** $e$ is in terms of $g$ and $t$. Then state precisely
which units are *eligible* to be the clean control for cohort $g$ at time $t$, and which are *forbidden*.

**(b)** [8 pts] Compute the full grid of clean $\widehat{\text{ATT}}(g,t)$ for the working world. For
cohort E ($g=2$), use State U as the never-treated control (you may also note that State L is a valid
*not-yet-treated* control in years $t < 4$, and gives the same answer here). For cohort L ($g=4$), use
State U — *never* the already-treated State E. Compute the six values:
$\widehat{\text{ATT}}(2,2),\ \widehat{\text{ATT}}(2,3),\ \widehat{\text{ATT}}(2,4),\ \widehat{\text{ATT}}(2,5),\ \widehat{\text{ATT}}(4,4),\ \widehat{\text{ATT}}(4,5).$
Show the cell means. Confirm each recovers the *true* effect $-(e+1)$ exactly — i.e., the clean
estimator is unbiased here where TWFE was not.

**(c)** [4 pts] Aggregate the grid **by event time** $e = t - g$, averaging across cohorts that share
the same $e$ (equal cohort sizes here, so simple averages). Report $\widehat{\text{ATT}}^{\text{es}}(e)$
for $e = 0, 1, 2, 3$. Then collapse to a single **overall ATT** as the simple average of all six
group-time effects, and confirm it equals the true $-13/6 \approx -2.17$. Contrast this in one sentence
with the pooled $\hat\beta^{\text{TWFE}} = -1.25$: which is right, and what did TWFE do to the magnitude?

**(d)** [2 pts] The chapter warns that clean estimators *refuse to fabricate an answer when no clean
control exists*. In the two-state world of Problem 3(d) (States E and L only, no U), what does
Callaway–Sant'Anna report for $\widehat{\text{ATT}}(4, t)$ — State L's effect — and why? State in one
sentence why this "refusal" is a *feature*, not a bug, contrasting it with what TWFE did with the same
two states.

---

## Problem 6 — Which estimator, and diagnosing a contaminated event study (12 points)

The chapter gives three heterogeneity-robust estimators that all implement the same idea — clean
controls, then transparent aggregation — by different routes: Callaway–Sant'Anna (explicit group-time
2×2s), Sun–Abraham (a saturated event-study regression with cohort×relative-time interactions, the
interaction-weighted estimator), and Borusyak–Jaravel–Spiess (imputation of the untreated counterfactual
from untreated cells only). This problem tests that you can *choose among them* and *read the diagnostic
they fix*.

**(a)** [3 pts] A classmate has already run a naive TWFE **event study** — the Chapter 4.1 regression
with a full set of relative-time dummies — and wants to fix it while changing as little of her code as
possible, staying inside a single `feols`-style regression call. Which of the three estimators is the
natural choice, and what *specifically* does it do to the event-study regression (name the
"interaction-weighted" mechanism) so that one cohort's dynamics can no longer leak into another's
coefficient?

**(b)** [3 pts] A second classmate wants the most *efficient* estimator and a pre-trend test that is
built from genuinely clean (uncontaminated) residuals. Which estimator fits, and describe its three-step
recipe in one sentence each (fit on untreated cells only → impute → difference). State the one-line
reason its fixed-effect estimates $\hat\alpha_i, \hat\lambda_t$ are not contaminated by treatment
effects, unlike pooled TWFE's.

**(c)** [4 pts] **Diagnosis.** Priya runs a naive TWFE event study on her real staggered data and the
plot shows non-zero, *trending* coefficients in the pre-periods ($e = -3, -2, -1$ are not flat near
zero) — even though she is certain parallel trends actually holds in her setting. She panics that her
design is broken. Explain what is most likely happening, using the Sun–Abraham result: why can a naive
TWFE event study show *funny pre-trends from contamination* even when the true pre-trends are flat? Name
the mechanism (cohort bleed through forbidden comparisons), and state what she should run instead to get
a pre-trend test she can trust, and what that corrected plot's pre-period coefficients should look like
if parallel trends really holds.

**(d)** [2 pts] In one or two sentences, give the Chapter 4.2 spec-discipline upgrade for staggered
designs (Conventions §4, extended): name the **two** specification choices a staggered-DiD write-up must
state explicitly that a plain 2×2 did not need, and state the identifying assumption in its
*per-cohort* form.

---

*End of Problem Set 4.2. Solutions: Appendix E, `E-w4-ps4.2-solutions.md`. The companion notebook
`nb4.2` (`notebooks/week-04/nb4.2-staggered-did-twfe-vs-cs.ipynb`) lets you check Problems 2–5 by
simulation — build Priya's staggered panel, confirm the pooled TWFE coefficient, run the Goodman-Bacon
decomposition and read the negative weight off the forbidden comparison, then fit Callaway–Sant'Anna
group-time $\text{ATT}(g,t)$ with never-treated controls and aggregate to a heterogeneity-robust event
study. The single discipline to carry forward: under staggered timing with heterogeneous or dynamic
effects, never trust a pooled $\hat\beta$ before you have seen how much of it rests on forbidden
comparisons.*
