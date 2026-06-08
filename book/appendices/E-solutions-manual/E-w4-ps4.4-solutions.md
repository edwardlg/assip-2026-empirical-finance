# Solutions — PS 4.4 (Synthetic Control Weights & Placebo Inference)

**Problem set:** `book/weeks/week-04/ps4.4.md` (PS 4.4, Week 4).
**Chapter:** Ch 4.4 — Synthetic Control & Synthetic DiD.

These are full worked solutions, not just answers. Notation follows `CONVENTIONS.md` and locks to Ch 4.4: $J+1$ units with treated unit $i=1$ and donor pool $i=2,\dots,J+1$; pre-period $t=1,\dots,T_0$, post-period $t=T_0+1,\dots,T$; potential outcomes $Y_{it}^{N}$ (no treatment) and $Y_{it}^{I}$ (intervention), with $\tau_{1t}=Y_{1t}^{I}-Y_{1t}^{N}$; the synthetic counterfactual $\hat{Y}_{1t}^{N}=\sum_{j=2}^{J+1} w_j Y_{jt}$ and estimate $\hat{\tau}_{1t}=Y_{1t}-\hat{Y}_{1t}^{N}$; the convex-weight program with $w_j\ge 0$ and $\sum_j w_j=1$ minimizing the pre-period mismatch $(\mathbf{X}_1-\mathbf{X}_0\mathbf{w})'\mathbf{V}(\mathbf{X}_1-\mathbf{X}_0\mathbf{w})$; root-mean-squared prediction errors $\text{RMSPE}_{\text{pre}}$, $\text{RMSPE}_{\text{post}}$; the post/pre ratio $r_i=\text{RMSPE}_{\text{post},i}/\text{RMSPE}_{\text{pre},i}$; the placebo permutation $p$-value $p=\#\{i:r_i\ge r_1\}/(J+1)$ and its $1/(J+1)$ floor; and synthetic DiD (Arkhangelsky, Athey, Hirshberg, Imbens and Wager 2021). All premiums are in **hundreds of dollars**. Every numerical result here was confirmed in Python (NumPy arithmetic and a `scipy.optimize` SLSQP solve over the simplex for Problem 2); verifying notes appear where useful.

---

## Problem 1 — When synthetic control beats DiD (14 points)

**(a) (4 pts)** *The parallel-trends assumption.* A DiD of the treated state against the equal-weighted average of all other states assumes: **absent the mandate, the treated state's average homeowner premium and the average premium of the (equal-weighted) rest-of-the-states control group would have changed by the same amount from the pre- to the post-period** — i.e., their premium trends would have stayed parallel. The post-minus-pre *difference* in the control's premium is then a valid estimate of what the treated state's premium *change* would have been with no mandate.

Why this is especially hard to defend with one treated unit: there is no naturally occurring "twin" for a single specific state. If Priya **picks one similar state** as the control, her entire estimate hinges on that one arbitrary choice — a critic can always nominate a *different* "similar" state with a different trend that flips the sign of the answer, and Priya has no principled way to adjudicate. If she instead **averages all the other states equally**, she is silently imposing weights $w_j=1/J$ on every donor, and there is no reason an equal-weighted blend should happen to share *her* treated state's trend. In both cases the pre-trends almost never line up, so parallel trends becomes a hope rather than something she can show the reader.

**(b) (5 pts)** *DiD as frozen-equal-weight synthetic control.* The 2×2 DiD counterfactual for the treated state's post-period level is the treated state's own pre-period level plus the *common* change estimated from the control group, and that control group is the simple average of the $J$ donors. Writing only the donor-average piece as a weighted average,
$$
\hat{Y}_{1t}^{N,\,\text{DiD-style}} \;=\; \sum_{j=2}^{J+1} w_j\, Y_{jt}, \qquad w_j=\frac{1}{J}\ \text{for every } j,
$$
so DiD is the synthetic-control estimator with the weight vector **frozen at equality**, $\mathbf{w}=(1/J,\dots,1/J)$, rather than chosen. (DiD additionally removes a constant level via the unit fixed effect; the point here is the *control-construction* step, where the weights live.)

What synthetic control does differently: instead of fixing $w_j=1/J$ and *hoping* the equal-weighted blend tracks the treated state's pre-period, it **chooses** $\mathbf{w}$ — subject to $w_j\ge 0$ and $\sum_j w_j=1$ — to minimize the pre-period mismatch $(\mathbf{X}_1-\mathbf{X}_0\mathbf{w})'\mathbf{V}(\mathbf{X}_1-\mathbf{X}_0\mathbf{w})$. That is exactly "earning the parallel-trends comparison rather than assuming it": where DiD *asserts* parallel pre-trends and (at best) checks them afterward, synthetic control makes parallel pre-trends the *objective function* it optimizes and then *displays* the achieved match so the reader can judge whether it worked. The leap of faith shrinks from "these two groups would have moved together" to "this carefully matched composite would have kept moving together for a few more years."

**(c) (5 pts)** Two features pushing toward synthetic control:

1. **One (or very few) treated units.** When $N_{\text{treated}}=1$ there is no cross-sectional treatment variation to power a DiD with a credible control group, and the "pick a twin" problem above bites hardest. Synthetic control is purpose-built for this case — it constructs a comparison unit instead of borrowing one. (Mechanism: a tailored convex blend can match a single unit's pre-period that no off-the-shelf group matches.)
2. **A long, matchable pre-period where equal weights visibly fail.** If the donors' equal-weighted trend diverges from the treated state before treatment, the parallel-trends assumption is *already* falsified for DiD, but a data-chosen convex blend may still track the treated state closely. Synthetic control *targets* that match. (Mechanism: optimizing the weights over the simplex finds the sparse blend that closes the pre-period gap.)

One feature pushing back toward DiD / synthetic DiD:

- **The treated unit sits at the edge of the donor distribution (no convex blend matches its level), but its trend is matchable.** Convexity forbids extrapolating past the most extreme donor, so classic synthetic control will underfit and produce a contaminated gap; DiD (and especially synthetic DiD) differences out a constant level gap and needs only a matched *trend*, which is achievable here. (Mechanism: the unit fixed effect / first-difference absorbs the persistent level mismatch that convexity cannot close — this is exactly Problem 6.)

---

## Problem 2 — Donor weights by hand: matching the pre-period (22 points)

Setup: $\mathbf{X}_1=(12,13,14)'$; donors $A=(10,10,10)'$, $B=(14,16,18)'$, $C=(20,21,24)'$; $\mathbf{V}=\mathbf{I}$; convex weights $\mathbf{w}=(w_A,w_B,w_C)$ with $w_j\ge0$, $\sum w_j=1$.

**(a) (4 pts)** *Equal weights $\tfrac13$ each.* The synthetic premium in each pre-year is the simple average of the three donors:
$$
\hat{Y}_{1}^{N} = \tfrac13(A+B+C) = \tfrac13\big((10{+}14{+}20),\,(10{+}16{+}21),\,(10{+}18{+}24)\big) = \tfrac13(44,47,52) = (14.67,\,15.67,\,17.33).
$$
The mismatch vector is $\mathbf{X}_1-\hat{Y}_1^{N}=(12-14.67,\,13-15.67,\,14-17.33)=(-2.67,\,-2.67,\,-3.33)$, so
$$
\text{SSR} = (-2.67)^2+(-2.67)^2+(-3.33)^2 = 7.11+7.11+11.11 = 25.33.
$$
The equal-weighted "control" is a **poor** match: it sits 2.67–3.33 units (hundreds of dollars) *above* the treated state every pre-year, because the expensive donor $C$ drags the simple average up. This is exactly the DiD failure from Problem 1 — equal weights have no reason to track the treated unit. *(Verified in Python: SSR $=25.33$.)*

**(b) (8 pts)** *The real optimization.*

*Step 1 — argue $w_C^{*}=0$.* Donor $C=(20,21,24)$ lies far **above** the treated state $(12,13,14)$ in every period — even further above than $B$. Donors $A=(10,10,10)$ and $B=(14,16,18)$ already **bracket** the treated path (the treated values lie between $A$ and $B$ each year), so a convex blend of $A$ and $B$ alone can reach the treated state. Adding any positive weight on $C$ pulls the synthetic average *up and away* from the treated state (and to keep the weights summing to one, it must steal weight from the donors that were closing the gap). Because $C$ is dominated this way — it can only push the synthetic premium in the wrong direction — the optimizer drives $w_C^{*}=0$. (This is the chapter's sparsity-from-convexity point: the dominated donor gets exactly zero.)

*Step 2 — solve the two-donor convex match.* With $w_C=0$ and $w_B=1-w_A$, require $w_A A + (1-w_A)B = \mathbf{X}_1$. Use the 2015 equation:
$$
10\,w_A + 14\,(1-w_A) = 12 \;\Longrightarrow\; 14 - 4\,w_A = 12 \;\Longrightarrow\; w_A = \tfrac{2}{4} = 0.5.
$$

*Step 3 — verify all three years* with $w_A=0.5,\ w_B=0.5$:
$$
\begin{aligned}
2015:&\ 0.5(10)+0.5(14)=5+7=12 \ \checkmark\\
2016:&\ 0.5(10)+0.5(16)=5+8=13 \ \checkmark\\
2017:&\ 0.5(10)+0.5(18)=5+9=14 \ \checkmark
\end{aligned}
$$
The synthetic path is exactly $(12,13,14)=\mathbf{X}_1$, so the mismatch is the zero vector and $\text{SSR}=0$. The match is **exact**.

**(c) (4 pts)** The full optimal weight vector is
$$
\mathbf{w}^{*}=(w_A^{*},w_B^{*},w_C^{*})=(0.5,\ 0.5,\ 0),
$$
with synthetic pre-period path $(12,13,14)$. Both constraints hold: all weights are $\ge 0$, and $0.5+0.5+0=1$. *(Verified: the SLSQP solver over the simplex returns $\mathbf{w}^{*}=(0.5,0.5,0)$ with objective $0$.)* The paper-ready sentence: **"the treated state's pre-period premium path is reproduced exactly by an equal blend of two donors — half donor $A$, half donor $B$ — and zero weight on the high-premium donor $C$."** That is a sparse, defensible, one-line description, the thing the chapter contrasts with a regression carrying many nonzero coefficients of both signs.

**(d) (6 pts)** *The unconstrained-regression temptation.* With **three** pre-years and **three** donors, an unconstrained regression of $\mathbf{X}_1$ on the donors has as many free coefficients as equations, so it can hit a **perfect** in-sample fit (SSR $=0$) — generically a unique solution to the $3\times3$ linear system, allowing any signs and any magnitudes for the coefficients (they need not sum to one). A perfect in-sample fit is **not** reassuring, for three linked reasons. First, with $T_0$ data points and $J=T_0$ donors, perfect fit is *guaranteed by counting*, not by genuine similarity — the regression is interpolating the pre-period, including its noise, by exploiting accidental correlations. Second, convexity is exactly what the unconstrained fit throws away: a convex synthetic control **cannot extrapolate** ($\hat{Y}_{1t}^{N}$ is boxed inside the range of donor premiums), so when it fits well that fit is *informative*, whereas the unconstrained fit can manufacture a fit with wild offsetting positive and negative coefficients that mean nothing. Third, what the unconstrained fit is likely to do in the **post-period**: those coefficients, tuned to interpolate pre-period noise, have no reason to hold out of sample and typically **explode** — predicting a counterfactual far outside the donor range and producing a spurious "effect." The convexity handcuffs buy stability and honesty at the cost of in-sample fit, which is the whole personality of the method.

---

## Problem 3 — From weights to counterfactual: reading the effect (16 points)

Carry $\mathbf{w}^{*}=(0.5,0.5,0)$ into the post-period. Post-year donor premiums: $A=(10,11,11)$, $B=(20,21,23)$, $C=(26,27,29)$; treated actuals $Y_1=(18,20,21)$.

**(a) (6 pts)** Synthetic counterfactual $\hat{Y}_{1t}^{N}=0.5\,A_t + 0.5\,B_t + 0\cdot C_t$:
$$
\begin{aligned}
2018:&\ 0.5(10)+0.5(20)=5+10=15\\
2019:&\ 0.5(11)+0.5(21)=5.5+10.5=16\\
2020:&\ 0.5(11)+0.5(23)=5.5+11.5=17
\end{aligned}
$$
So $\hat{Y}_{1}^{N}=(15,16,17)$. Donor $C$ contributes nothing because $w_C^{*}=0$. *(Verified: $(15,16,17)$.)*

**(b) (5 pts)** Estimated effects $\hat{\tau}_{1t}=Y_{1t}-\hat{Y}_{1t}^{N}$:
$$
\hat{\tau}_{1,2018}=18-15=3,\quad \hat{\tau}_{1,2019}=20-16=4,\quad \hat{\tau}_{1,2020}=21-17=4.
$$
Average post-treatment gap $=\dfrac{3+4+4}{3}=\dfrac{11}{3}=3.67$ (hundreds of dollars). **Headline estimate:** the mandate raised the average homeowner premium in the treated state by about **\$367 per home** over the three post-years (in premium-dollar terms, $+3.67\times\$100$). *(Verified: mean gap $=3.667$.)*

**(c) (5 pts)** This *is* the synthetic-control estimate because $\hat{\tau}_{1t}=Y_{1t}-\hat{Y}_{1t}^{N}$ plugs the synthetic counterfactual into the definition of the causal effect $\tau_{1t}=Y_{1t}^{I}-Y_{1t}^{N}$. In $\hat{\tau}_{1t}=Y_{1t}-\hat{Y}_{1t}^{N}$: the first term $Y_{1t}=Y_{1t}^{I}$ is **observed** (the treated state's actual post-mandate premium); the second term $\hat{Y}_{1t}^{N}=\sum_j w_j^{*}Y_{jt}$ is the **estimate of the unobservable counterfactual** $Y_{1t}^{N}$ — what the treated state's premium *would have been* with no mandate, built from the donors' observed untreated premiums. Because the Problem-2 match was *exact*, the **pre-period gap was zero** in every year — the synthetic twin walked in lockstep with the real state before treatment. That flat-at-zero pre-period gap is the credential: a comparison that demonstrably reproduced the treated state when there was no effect to obscure it is one we can plausibly trust to keep reproducing it for a few more years, so the post-period divergence is read as the causal effect of the mandate (under no-anticipation and no-interference).

---

## Problem 4 — Placebo permutation inference (24 points)

**(a) (6 pts)** Ratios $r_i=\text{RMSPE}_{\text{post},i}/\text{RMSPE}_{\text{pre},i}$:

| Unit | pre | post | $r_i$ |
|:---|:---:|:---:|:---:|
| **Treated** | $0.40$ | $3.20$ | $\mathbf{8.00}$ |
| Donor 1 | $0.50$ | $0.90$ | $1.80$ |
| Donor 2 | $2.00$ | $5.00$ | $2.50$ |
| Donor 3 | $0.30$ | $0.60$ | $2.00$ |
| Donor 4 | $1.20$ | $1.10$ | $0.92$ |
| Donor 5 | $0.45$ | $0.70$ | $1.56$ |
| Donor 6 | $3.00$ | $4.50$ | $1.50$ |
| Donor 7 | $0.60$ | $0.50$ | $0.83$ |
| Donor 8 | $0.80$ | $1.40$ | $1.75$ |
| Donor 9 | $0.55$ | $0.66$ | $1.20$ |

*(Verified: e.g. $3.20/0.40=8.00$, $5.00/2.00=2.50$, $4.50/3.00=1.50$, $0.66/0.55=1.20$.)*

**(b) (5 pts)** Ranked largest to smallest:
$$
\underbrace{8.00}_{\text{Treated}} > 2.50_{\text{D2}} > 2.00_{\text{D3}} > 1.80_{\text{D1}} > 1.75_{\text{D8}} > 1.56_{\text{D5}} > 1.50_{\text{D6}} > 1.20_{\text{D9}} > 0.92_{\text{D4}} > 0.83_{\text{D7}}.
$$
The treated state has the **single largest** ratio ($8.00$, more than triple the runner-up). So $\#\{i:r_i\ge r_1\}=1$ (only the treated unit itself), and with $J+1=10$,
$$
p=\frac{1}{J+1}=\frac{1}{10}=0.10.
$$

**(c) (5 pts)** Re-ranking by **raw $\text{RMSPE}_{\text{post}}$** alone:
$$
5.00_{\text{D2}} > 4.50_{\text{D6}} > \underbrace{3.20}_{\text{Treated}} > 1.40_{\text{D8}} > 1.10_{\text{D4}} > 0.90_{\text{D1}} > \dots
$$
On the raw-gap ranking the treated state falls to **3rd**, leapfrogged by **Donor 2** (post $5.00$) and **Donor 6** (post $4.50$). What is special about those two: both have **terrible pre-period fit** ($\text{RMSPE}_{\text{pre}}=2.00$ and $3.00$ respectively) — they were never matched well to begin with, so their large post-period "gaps" are just continuations of a comparison that was already off-track, not evidence of an effect. The ratio neutralizes them by dividing by that large pre-RMSPE ($5.00/2.00=2.50$ and $4.50/3.00=1.50$ — both modest). If Priya ranked on **raw** post-gaps she would wrongly conclude the treated state is *not* exceptional (it's only 3rd, $p$ would look like $3/10=0.30$) and might abandon a real finding. Scaling by each unit's own pre-fit is exactly what rescues it.

**(d) (8 pts)**

&nbsp;&nbsp;**(i)** With $J=9$ donors the reference set has $J+1=10$ units, so the smallest achievable $p$-value is $1/(J+1)=1/10=0.10$ — attained when the unit has the single largest ratio. The treated state **is** at that floor here ($p=0.10$). It is as extreme as the data can possibly register, and yet $p=0.10$ is the best it can do — the floor, not the t-test, is the binding constraint.

&nbsp;&nbsp;**(ii)** Solve $\dfrac{1}{J+1}<0.05$: this requires $J+1>20$, i.e. $J+1\ge 21$, so $J\ge 20$. **Priya needs at least 20 donors** for the floor to dip below $0.05$ (with $J=20$, the floor is $1/21\approx0.048$). Note the boundary: $J=19$ gives a floor of exactly $1/20=0.05$, which does *not* clear a strict $<0.05$ threshold — hence $J\ge 20$, not $J\ge 19$.

&nbsp;&nbsp;**(iii)** With only $J=8$ donors the reference set has $9$ units, so the *smallest possible* permutation $p$-value is $1/9\approx0.111$. A reported "$p<0.01$" is **mathematically impossible** for a single-treated-unit placebo test with $8$ donors — the classmate cannot have obtained it from a legitimate permutation, regardless of how clean the gap looks; they have almost certainly mis-applied a t-statistic or an asymptotic standard error that does not exist when $N_{\text{treated}}=1$.

&nbsp;&nbsp;**(iv)** The permutation $p$-value is a **small-sample, exact, randomization-style** statement: it reports the fraction of units (treated plus placebos) whose scaled gap is at least as extreme as the treated unit's, under the sharp null that the policy had no effect on any unit. It does **not** assume normal errors, large-$N$ asymptotics, or a cross-section of treated units — the very ingredients the t-statistic (Ch 2.4) needs and that are absent when there is one treated unit. Its **resolution is bounded by how many placebos you have** because the only $p$-values it can ever produce are the discrete values $1/(J+1), 2/(J+1), \dots, 1$; with few donors the grid is coarse and the smallest nonzero value ($1/(J+1)$) is large, so you literally cannot express more precision than your placebo count allows.

---

## Problem 5 — No extrapolation: the convexity constraint as conscience (8 points)

**(a) (4 pts)** With convex weights ($w_j\ge0$, $\sum_j w_j=1$), the synthetic premium $\hat{Y}_{1t}^{N}=\sum_j w_j Y_{jt}$ is a genuine weighted average of the donor premiums, so for every year it is **trapped inside the range of the donors**: it can be no higher than the most expensive donor and no lower than the cheapest. If the treated state has the highest premium of *any* state, then in every pre-year its value lies *above* the top of that range, and no convex blend can climb up to meet it — the synthetic path is pinned below the treated path with a persistent gap. As a result the **pre-period RMSPE is large and roughly constant** (it cannot be driven to zero no matter how the weights are chosen). The chapter's point that "the convexity constraint will not let it lie about that" is a **feature**: a large pre-RMSPE is the method *confessing* that no honest convex combination of these donors resembles the treated unit, which is true and which Priya needs to know — rather than papering over the mismatch with a slick but meaningless fit.

**(b) (4 pts)** The unconstrained regression of Problem 2(d) *can* reach above all donors because it allows coefficients greater than one and **negative** coefficients on other donors — "two parts the second-most-expensive donor minus one part a cheap one." That is **extrapolation**: the fitted counterfactual leaves the convex hull of the data, supported only by the linear functional form, not by any actual donor resembling the treated unit. It is untrustworthy out of sample precisely because those offsetting coefficients are tuned to in-sample noise and have no reason to hold in the post-period, where they typically swing wildly. This is why convexity makes synthetic control "read less like a regression and more like matching": instead of estimating a coefficient for every donor, it *selects and weights a small comparison set drawn from real units*, and it refuses to invent a comparison unit that does not exist. The one diagnostic Priya must report so a reader can judge the edge-unit problem: the **pre-period fit — the pre-period RMSPE and a plot of the treated unit against its synthetic twin through the whole pre-period.** A visibly large, persistent pre-period gap is the signal that the convex hull could not reach the edge unit and the counterfactual should not be trusted (and that she should consider synthetic DiD instead — Problem 6).

---

## Problem 6 — Synthetic DiD vs synthetic control on an edge unit (16 points)

Treated $Y_1=(22,23,24,28,29)$; synthetic blend $\hat{Y}_1^{N}=(20,21,22,23,24)$; pre-years 2015–2017, post-years 2018–2019.

**(a) (5 pts)** Classic synthetic-control gap $\hat{\tau}_{1t}=Y_{1t}-\hat{Y}_{1t}^{N}$:
$$
\begin{aligned}
2015:&\ 22-20=2 & 2016:&\ 23-21=2 & 2017:&\ 24-22=2\\
2018:&\ 28-23=5 & 2019:&\ 29-24=5.
\end{aligned}
$$
Average **pre-period** gap $=\frac{2+2+2}{3}=2$; average **post-period** gap $=\frac{5+5}{2}=5$. Naive synthetic-control "effect" $=5$ (the average post gap). It is **contaminated** because the convex blend never matched the treated state's *level* — there is a persistent $+2$ gap *before* any treatment (the edge-unit pathology of Problem 5). That $+2$ is pure level mismatch, not effect, yet it sits inside the post-period gap, inflating the estimate. *(Verified: pre-mean $=2.0$, post-mean $=5.0$.)*

**(b) (6 pts)** Synthetic DiD keeps the same unit-weighted blend but **differences out the constant level gap**. The baseline level difference is the average pre-period gap, $=2$. Subtract it from each post-period gap:
$$
\hat{\tau}^{\text{sdid}}_{2018}=5-2=3,\qquad \hat{\tau}^{\text{sdid}}_{2019}=5-2=3,
$$
average SDID estimate $=\frac{3+3}{2}=3$. *(Verified: SDID effect $=(3,3)$, mean $3.0$.)* This is exactly what the SDID objective
$$
\min_{\tau,\mu,\alpha,\beta}\ \sum_{i}\sum_{t}\big(Y_{it}-\mu-\alpha_i-\beta_t-\tau D_{it}\big)^2\,\hat w_i\,\hat\lambda_t
$$
does in miniature: the **unit fixed effect $\alpha_i$ absorbs the constant $+2$ level gap** between the treated unit and its weighted donors, so $\tau$ picks up only the *post-period change relative to that absorbed baseline* — the $+3$ break.

**(c) (5 pts)** The true injected effect is $+3$ per post-year. **Synthetic DiD recovered it exactly** ($\hat\tau^{\text{sdid}}=3$); **classic synthetic control was off by $+2$** ($\hat\tau^{\text{SC}}=5$ versus true $3$ — overstated by the full level mismatch). SDID succeeds because it requires only a matched **trend**, not a matched **level**: the donor blend has the same slope as the treated unit, so once the unit **fixed effect** differences away the constant level gap, what remains is the genuine post-period divergence; classic synthetic control fails because convexity could not lift the synthetic path up to the treated state's level, and that un-removed level gap leaks straight into the post-period estimate. The one situation where you would still prefer **classic** synthetic control: when you have **one treated unit with an excellent pre-period level fit** (the synthetic twin tracks the treated unit in *level*, not just trend) — there classic synthetic control is clean, fully transparent, gives you a sparse weight vector you can name in a sentence, and comes with the placebo permutation test, so the extra machinery of SDID buys you nothing.

---

*End of solutions for PS 4.4. The full pipeline — convex weight estimation, the placebo loop with RMSPE ratios, the gray-spaghetti placebo plot, and a real synthetic-DiD estimator — appears in `nb4.4`, where these hand-checked patterns reappear on Priya's simulated premium panel. Citations: the synthetic-control method is due to Abadie and Gardeazabal (2003) and Abadie, Diamond and Hainmueller (2010); the placebo/RMSPE-ratio inference and the $1/(J+1)$ floor are from Abadie, Diamond and Hainmueller (2010); synthetic difference-in-differences is from Arkhangelsky, Athey, Hirshberg, Imbens and Wager (2021).*
