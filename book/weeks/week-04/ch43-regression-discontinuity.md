# Ch 4.3 — Regression Discontinuity

Every design in this book so far has been a fight to make treated and untreated units comparable. Week 3 fought it with conditioning (matching, balancing) and then, when that failed, with an instrument that imported clean variation from outside. The two difference-in-differences chapters that opened this week fought it across time, leaning on a parallel-trends assumption about how the untreated *would have* moved. Each design buys comparability at the price of an assumption you mostly cannot test — CIA, exclusion, parallel trends. This chapter introduces a design where comparability is almost handed to you by the world, and where the central assumption is, for once, *partly checkable*.

The idea is **regression discontinuity** — RD — and it lives wherever a treatment is switched on by a sharp rule. Some bureaucratic, mechanical threshold decides who gets treated: a credit score at or above 660 flips a loan from rejected to approved; a test score at or above the cutoff wins the scholarship; a firm's market-cap rank at the annual reconstitution lands it in one stock index rather than another. The rule creates a knife-edge. A unit that lands at $659$ and a unit at $661$ are, for all practical purposes, the same kind of unit — same creditworthiness, same everything that matters — yet one is treated and one is not, purely because a number crossed a line. Compare the outcomes of units *just* on either side of that line and you have something that looks remarkably like a randomized experiment, run for free by the institution that drew the cutoff.

Our guide this chapter is Sam, who trades on momentum and index effects and has fixated on one of the cleanest natural experiments in all of finance: the annual reconstitution of the Russell stock indexes. Once a year, FTSE Russell ranks U.S. stocks by market capitalization and slices the list. The largest roughly $1{,}000$ go into the **Russell 1000** (large-cap); the next roughly $2{,}000$ go into the **Russell 2000** (small-cap). The boundary between the two — somewhere around rank $1{,}000$ — is a cutoff. A stock ranked $998$ and a stock ranked $1{,}002$ are nearly identical companies of nearly identical size, but one is a small fish in the large-cap pond and the other is a big fish in the small-cap pond. Crucially, *vastly* more passive money tracks the Russell 2000 than the bottom of the Russell 1000, so crossing into the 2000 can mean a large jump in passive-fund ownership — and through that, in governance, liquidity, and price. Sam wants the causal effect of index membership on these outcomes, and the cutoff is going to give it to him.

This chapter follows the usual reveal-the-trick arc. First the idea and the **sharp RD** estimand — a jump in a conditional mean. Then **fuzzy RD**, where the cutoff only *nudges* the treatment probability, which turns RD into an instrumental-variables problem and connects us straight back to Week 3. Then the machinery that makes RD honest: **local polynomial estimation** (and why you must resist high-order global polynomials), **bandwidth selection** and its bias–variance trade-off, the **McCrary density test** for cheating at the cutoff, and finally how to *read* an RD plot. We close on the validity threats that turn a beautiful design into a mirage.

---

## 1. The result in one plain sentence

> **RD, stated plainly.** When a treatment switches on at a known cutoff $c$ in some running variable $X$, the causal effect of the treatment — for units right at the cutoff — is the size of the *jump* in the outcome as $X$ crosses $c$.

That is the entire design. There is a variable $X$ — the **running variable** (also called the *forcing variable* or *score*) — and a known threshold $c$. The treatment is assigned by which side of $c$ you fall on. If the outcome $Y$ varies smoothly with $X$ everywhere *except* for a clean break exactly at $c$, then that break cannot be the smooth influence of $X$ itself (which is continuous through $c$); the only thing that changes discontinuously at $c$ is the treatment. So the vertical gap in $\mathbb{E}[Y \mid X]$ at $c$ *is* the treatment effect.

Everything technical in this chapter is an elaboration of "measure the jump." Sharp RD measures the jump in the outcome directly. Fuzzy RD measures the jump in the outcome and divides by the jump in treatment probability — the same magic ratio you met in Week 3. Local polynomials are how you estimate the height of the curve on each side of $c$ without contaminating it with far-away data. Bandwidth choice is how wide a window around $c$ you trust. And the validity tests all ask one question: *is the jump really the treatment, or is something else also jumping at $c$?*

---

## 2. Why units near the cutoff are comparable: local randomization

The deepest justification for RD is an analogy to a randomized experiment, and it is worth building slowly because it is what makes the design credible.

Think about what determines a stock's exact reconstitution rank. It is its market capitalization on the ranking date, measured to the dollar. Now, a company's *fundamental* size — its true economic footprint — is something it controls over years. But its rank *to the precise dollar* on one particular day in late spring is buffeted by a thousand tiny, essentially random forces: a rival's earnings surprise that nudged sector sentiment that morning, a block trade by some unrelated pension fund, microstructure noise in the closing auction, the exact path of the past month's returns. Two companies of genuinely identical fundamental size can end up on opposite sides of rank $1{,}000$ because of this fine-grained noise, and which side they land on is, in the immediate neighborhood of the cutoff, *as good as a coin flip*.

This is the **local randomization** intuition, and it is the heart of RD. Far from the cutoff, treated and untreated units differ systematically — the Russell 1000 is full of genuinely enormous firms, the bottom of the 2000 full of genuinely tiny ones, and you would never compare Apple to a micro-cap. But *in a small window around $c$*, the assignment to one side or the other is dominated by noise that no firm can finely control, so the units just above and just below $c$ are balanced on everything — observed and unobserved — exactly as randomization would make them balanced. The cutoff manufactures a tiny local experiment. The treated group is the units that happened to land at $X = c + \epsilon$; the control group is the units at $X = c - \epsilon$; and because the landing was noise-driven, the two groups are exchangeable.

The formal version of this intuition is a **continuity** assumption, and we state it in potential-outcomes language from Chapter 3.1. Let $Y_i(1)$ and $Y_i(0)$ be unit $i$'s potential outcomes under treatment and control. The identifying assumption of RD is that the *average* potential outcomes are **continuous functions of $X$ at the cutoff**:

$$
\mathbb{E}[Y_i(1) \mid X = x] \quad \text{and} \quad \mathbb{E}[Y_i(0) \mid X = x] \quad \text{are continuous in } x \text{ at } x = c.
$$

Read this carefully, because it is the whole game. It says: *if no treatment had switched on at $c$, the outcome would have evolved smoothly through $c$ with no jump.* The untreated potential outcome $\mathbb{E}[Y_i(0)\mid X]$ — what would have happened to a just-barely-Russell-2000 stock had it instead stayed just-barely-Russell-1000 — is the same, in the limit, as what we actually observe for the just-barely-Russell-1000 stocks sitting on the other side. They are the missing counterfactual, and continuity says the stocks on the control side supply it. Any jump we then see *must* be the treatment.

Note the elegant difference from CIA. CIA (Week 3) demanded that treated and untreated units be comparable *after conditioning on a big pile of covariates you hope is complete* — a strong, untestable claim about the absence of unobserved confounders everywhere. RD demands comparability only *in the limit, exactly at the cutoff*, and gets it from a smoothness condition that is far weaker and, as we will see in §8–§9, leaves observable fingerprints when it fails. The price for this gift is in §3's fine print: RD only identifies the effect *at the cutoff*, for the local population sitting near $c$. It is the ultimate "LATE" — local in the most literal sense.

---

## 3. Sharp RD: the jump is the effect

**Sharp RD** is the case where treatment is a *deterministic* step function of the running variable: everyone on one side is treated, everyone on the other side is not, with no exceptions. Formally,

$$
D_i = \mathbf{1}\{X_i \geq c\},
$$

where $\mathbf{1}\{\cdot\}$ is the indicator that equals $1$ when its condition holds. Treatment is a perfect, gapless function of $X$. Maya's world is the cleanest example: a lender's automated underwriting system approves every applicant with a credit score $X_i \geq 660$ and rejects every applicant below, mechanically, with the loan officer having no discretion. Cross $660$ and approval flips from $0$ to $1$ with certainty.

Under continuity, the sharp-RD estimand is the jump in the conditional-mean function of the outcome at $c$:

$$
\tau_{\text{SRD}} \;=\; \lim_{x \downarrow c} \mathbb{E}[Y \mid X = x] \;-\; \lim_{x \uparrow c} \mathbb{E}[Y \mid X = x].
$$

In words: take the limit of the outcome's average as you approach $c$ *from above* (the treated side), subtract the limit as you approach *from below* (the control side), and the difference is the treatment effect. The $\lim_{x \downarrow c}$ and $\lim_{x \uparrow c}$ are one-sided limits — you are reading the *height of each fitted curve right at the boundary*, extrapolated to the cutoff from its own side. Because the running variable $X$ is continuous through $c$ and enters $\mathbb{E}[Y(0)\mid X]$ smoothly, the only thing that can produce a gap between those two limits is the treatment switching on. The gap is $\tau_{\text{SRD}}$.

There is one subtlety in the interpretation, and it is the RD analog of LATE. The estimand $\tau_{\text{SRD}}$ is the average treatment effect **for units with $X = c$** — the firms right at rank $1{,}000$, the borrowers right at score $660$. It is *not* the average effect for all borrowers, nor for the treated, nor for anyone whose score is far from the cutoff. If the effect of a loan is large for marginal borrowers but small for deep-subprime applicants far below the line, RD will report only the marginal number, because the marginal units are the only ones whose treatment status the cutoff actually pins down. As in Week 3, you must always ask: *is the effect at the cutoff the effect I care about?* For policy questions about where to *set* the cutoff — should the score threshold be $660$ or $640$? — the effect at the margin is exactly the right number, which is part of why RD is beloved by regulators.

### A number, to make it concrete

Suppose Sam bins stocks by their reconstitution rank distance from the cutoff and computes average next-year passive-fund ownership in each bin:

| Rank distance from cutoff | Side | Mean passive ownership (%) |
|---|---|---|
| $-6$ to $-4$ (just inside R1000) | control | $5.1$ |
| $-3$ to $-1$ (just inside R1000) | control | $5.3$ |
| $+1$ to $+3$ (just inside R2000) | treated | $5.9$ |
| $+4$ to $+6$ (just inside R2000) | treated | $6.0$ |

The control-side numbers ($5.1, 5.3$) are climbing gently toward the cutoff; extrapolated to $c$, the control curve sits around $5.4$. The treated-side numbers ($5.9, 6.0$), extrapolated back to $c$, sit around $5.8$. The jump is roughly $\hat\tau_{\text{SRD}} \approx 5.8 - 5.4 = 0.4$ percentage points of passive ownership, caused by landing in the Russell 2000 rather than the bottom of the Russell 1000. Notice we did not just difference the two nearest bins blindly; we read off the *limit of each side's trend at the boundary*. Getting that extrapolation right is what local polynomial estimation in §5 is for.

---

## 4. Fuzzy RD: when the cutoff only nudges treatment

Sharp RD assumes the cutoff flips treatment with certainty. The real world is messier, and the Russell example is the textbook illustration of *why*. The reconstitution rule does not mechanically force a fixed quantity of passive money into every stock that crosses into the Russell 2000. What crossing changes is the *probability and intensity* of passive ownership — index funds tracking the 2000 will tend to buy a newly added stock, but not every fund rebalances identically, the float-adjusted index weights vary, "banding" rules introduce slack, and some institutions track custom benchmarks. So treatment (here, "high passive ownership" or "index-fund inclusion") does not jump from $0$ to $1$ at the cutoff; its *probability* jumps — from, say, a $30\%$ chance of heavy passive uptake just inside the 1000 to a $70\%$ chance just inside the 2000.

This is **fuzzy RD**: the cutoff shifts the *probability* of treatment discontinuously, but does not determine it. Formally, instead of $D_i = \mathbf{1}\{X_i \geq c\}$ holding exactly, we only have a jump in the treatment probability:

$$
\lim_{x \downarrow c} \mathbb{E}[D \mid X = x] \;\neq\; \lim_{x \uparrow c} \mathbb{E}[D \mid X = x].
$$

The left side is the share treated just above the cutoff; the right side is the share treated just below; in sharp RD this difference is exactly $1$, and in fuzzy RD it is some fraction strictly between $0$ and $1$.

Here is where Week 3 comes roaring back. In a fuzzy design you have a discontinuity that affects the *outcome* (the numerator) and a discontinuity that affects the *treatment* (the denominator), and the causal effect is their ratio:

$$
\tau_{\text{FRD}} \;=\;
\frac{\displaystyle \lim_{x \downarrow c}\mathbb{E}[Y\mid X=x] - \lim_{x \uparrow c}\mathbb{E}[Y\mid X=x]}
     {\displaystyle \lim_{x \downarrow c}\mathbb{E}[D\mid X=x] - \lim_{x \uparrow c}\mathbb{E}[D\mid X=x]}
\;=\;
\frac{\text{jump in outcome at } c}{\text{jump in treatment at } c}.
$$

Stare at that fraction and you will recognize the **Wald estimator** from Chapter 3.4 exactly. The numerator is a reduced form: the effect of *crossing the cutoff* on the outcome, ignoring treatment. The denominator is a first stage: the effect of crossing the cutoff on the treatment. Divide and you scale the reduced form up by the dose of treatment the cutoff actually delivered. **Fuzzy RD is instrumental variables, where the instrument is the indicator $Z_i = \mathbf{1}\{X_i \geq c\}$ for being above the cutoff.** Everything you learned in Week 3 transfers:

- **Relevance** is the jump in the treatment probability — the denominator. It is testable (you can see the first-stage jump in $\mathbb{E}[D\mid X]$), and it had better be a real jump, not a sliver, or you are dividing by something near zero and inviting the weak-instrument pathology of Chapter 3.5.
- **Exclusion** is the RD continuity assumption applied to the instrument: crossing the cutoff must affect the outcome *only through* the treatment, and nothing else can jump at $c$. If passive ownership were the *only* thing that changes when a stock crosses into the Russell 2000, exclusion holds. If crossing *also* triggers, say, a change in analyst coverage rules at the same rank, exclusion fails and the ratio is contaminated. (This is precisely the "compound treatment" threat of §10.)
- **LATE, not ATE.** Just as IV identifies the effect for *compliers*, fuzzy RD identifies the effect for units who take treatment *because* they crossed the cutoff — the **compliers at the cutoff**. Stocks that would have heavy passive ownership regardless (always-takers) and those that never attract it (never-takers) contribute nothing to the ratio. Under a monotonicity assumption (crossing the cutoff can only raise, never lower, the chance of treatment — no defiers), the fuzzy-RD estimand is the LATE for cutoff compliers.

So you do not need new machinery for fuzzy RD; you need to estimate two jumps instead of one and take their ratio, with standard errors that respect the ratio (the same warning as Week 3: never hand-divide two regressions and trust the naive standard error — let the software propagate the uncertainty). In practice `rdrobust` does both jumps and the ratio in one call, which is exactly what nb4.3 will use.

---

## 5. Local polynomial estimation: why local linear, not a global curve

We have an estimand — a jump in a conditional mean at $c$. Now: how do you actually estimate the height of $\mathbb{E}[Y\mid X]$ on each side of the cutoff? This is where a generation of empiricists made a mistake that you should learn to avoid on sight.

The tempting move is to fit one **global polynomial** to all the data — say, regress $Y$ on a treatment dummy $D$ plus $X, X^2, X^3, X^4$ over the entire sample, letting the slopes differ on each side of $c$, and read the coefficient on $D$ as the jump. It seems principled: a high-order polynomial is flexible, it uses all the data efficiently, and it gives you a tidy single regression. For years, RD papers did exactly this.

It is a trap, and Gelman and Imbens (2019) named the trap precisely.[^gelmanimbens] High-order global polynomials produce **noisy, misleading estimates of the value at a boundary point**, for three concrete reasons. First, polynomials are notoriously erratic near the *edges* of the data — and the cutoff, by construction, is an interior-but-pivotal point where you are reading two one-sided extrapolations that meet. Second, a global polynomial lets data *far* from the cutoff — Apple, on the Russell 1000 side; a tiny micro-cap deep in the 2000 — dictate the curvature right at $c$. Those distant points have nothing to do with the marginal stocks you care about, yet a fourth-order polynomial fit to the whole range will twist itself to accommodate them and, in doing so, can manufacture a spurious wiggle (or erase a real jump) exactly at the boundary. Third, the estimate is disturbingly sensitive to the *arbitrary choice of polynomial order*: the jump you report can swing wildly between a cubic and a quartic, with no principled way to pick. Gelman and Imbens showed that the implicit weights a high-order polynomial places on individual observations to estimate the boundary value can be bizarre and even negative — a sign the estimator is doing something you would never endorse if you saw it spelled out.

[^gelmanimbens]: Gelman, A., & Imbens, G. (2019). Why High-Order Polynomials Should Not Be Used in Regression Discontinuity Designs. *Journal of Business & Economic Statistics*, 37(3), 447–456.

The fix is **local polynomial estimation**, and the recommended workhorse is **local linear regression**. The idea is to throw away the data far from the cutoff and fit a simple, low-order — usually linear — model only *within a window* of width $h$ (the **bandwidth**) on each side of $c$:

1. Keep only observations with $|X_i - c| \leq h$.
2. Fit a separate straight line to the outcome on each side of the cutoff (equivalently, one regression of $Y$ on $D$, $(X-c)$, and their interaction).
3. Weight observations by a **kernel** that gives points near $c$ more weight than points near the edge of the window — a **triangular kernel**, which declines linearly from weight $1$ at $c$ to weight $0$ at the window edge, is standard and theoretically near-optimal for boundary estimation.
4. The estimated jump is the gap between the two fitted lines *at $c$* — the coefficient on $D$.

A line is a good local approximation to almost any smooth curve over a short enough interval (it is just the first-order Taylor expansion you know from calculus), so within a narrow window the linear fit captures the trend faithfully without the wild extrapolation a high-order polynomial commits. You can go to local *quadratic* if you have a lot of data and want to reduce bias from curvature, but the field's consensus, following Gelman–Imbens, is: **stay local, stay low-order.** Local linear with a good bandwidth and a triangular kernel is the default for a reason.

---

## 6. Bandwidth selection: the bias–variance trade-off

The bandwidth $h$ is the single most consequential choice in an RD analysis, and it is governed by a tension you have met before in disguise: the **bias–variance trade-off**.

Make $h$ **large** and you include lots of data far from the cutoff. Your two fitted lines are estimated precisely (many points, small standard errors — *low variance*), but you are now using stocks ranked $950$ and $1{,}050$ to infer what is happening at $1{,}000$, and if the true outcome curve bends over that range, your straight line will systematically mis-read its height at the boundary — *high bias*. Make $h$ **small** and you use only the handful of stocks hugging the cutoff. Now there is almost no curvature to worry about, so the linear approximation is nearly exact (*low bias*), but with so few points your fitted lines jitter from sample to sample and your standard errors balloon (*high variance*). Too wide and you are biased; too narrow and you are noisy. The optimal bandwidth balances the squared bias against the variance to minimize the mean squared error of the jump estimate.

You can watch this trade-off in the verified code of §11. With a true jump of $0.6$, the local-linear estimate at bandwidth $h=4$ comes in around $0.56$ (close to the truth, but with a wide standard error of $\sim 0.18$), while at $h=32$ it drifts to $\sim 0.41$ (a much tighter standard error of $\sim 0.07$, but now badly biased because the wide window let the curvature on the treated side bend the fit). The narrow window is honest but noisy; the wide window is precise but wrong. That is the trade-off made numerical.

Two named procedures choose $h$ for you in a principled, data-driven way, so you are not eyeballing it (and not, crucially, *p*-hacking by trying bandwidths until the result you want appears).

**Imbens–Kalyanaraman (2012).** Imbens and Kalyanaraman derived the bandwidth that minimizes the asymptotic mean squared error of the RD estimator.[^ik] Their formula estimates the two ingredients of the MSE — the curvature of the outcome function at the cutoff (which drives bias) and the noise variance (which drives variance) — from the data, then plugs them into the optimal-$h$ expression. The "IK bandwidth" was the first widely adopted automatic choice and made RD analyses far less arbitrary.

[^ik]: Imbens, G., & Kalyanaraman, K. (2012). Optimal Bandwidth Choice for the Regression Discontinuity Estimator. *Review of Economic Studies*, 79(3), 933–959.

**Calonico–Cattaneo–Titiunik (2014).** Here is the subtlety IK leaves dangling, and CCT fixed it. The MSE-optimal bandwidth is, by design, *large enough that the bias is not negligible* — that is what minimizing MSE means, you accept some bias to buy variance reduction. But the conventional confidence interval, $\hat\tau \pm 1.96\,\widehat{\text{se}}$, is built assuming the estimator is centered on the truth. At the MSE-optimal bandwidth it is *not* centered — there is a leftover bias — so the conventional interval is mis-located and undercovers: it will contain the true effect less than $95\%$ of the time. Calonico, Cattaneo, and Titiunik (2014) gave the now-standard fix, **robust bias-corrected inference**.[^cct] They (i) estimate the leading bias term explicitly and subtract it from the point estimate (*bias correction*), and (ii) inflate the standard error to account for the extra noise that the bias-correction step itself introduces (*robust* standard errors). The result is a confidence interval that achieves its nominal coverage even at the MSE-optimal bandwidth. This is the method implemented in the `rdrobust` package, and it is what nb4.3 uses. When you report an RD estimate today, the expectation is: a data-driven (CCT/IK-style) bandwidth, local linear with a triangular kernel, and CCT robust bias-corrected confidence intervals.

[^cct]: Calonico, S., Cattaneo, M. D., & Titiunik, R. (2014). Robust Nonparametric Confidence Intervals for Regression-Discontinuity Designs. *Econometrica*, 82(6), 2295–2326.

A discipline note in the spirit of CONVENTIONS §4: pick your bandwidth procedure *before* you look at the estimate, report it, and show that the result survives reasonable alternatives (a standard robustness check is to halve and double the chosen $h$ and confirm the jump does not vanish or explode). Bandwidth-shopping until the stars appear is one of the easiest ways to fool yourself and your reader with RD.

---

## 7. How to read an RD plot

RD is the most *visual* design in this book, and a good RD plot is half the argument. Before any regression, plot the data, because the human eye is an excellent jump-detector and an even better fraud-detector. A canonical RD plot has three elements layered together.

**The binned scatter.** Chop the running variable into bins (say, every two ranks), compute the *mean* outcome within each bin, and plot one dot per bin against the bin's center. Raw scatterplots of individual observations are too noisy to read; binning averages away the idiosyncratic noise and reveals the shape of $\mathbb{E}[Y\mid X]$. Each dot is a local average, and the dots should trace out a smooth trend on each side of the cutoff. (The number of bins is itself a choice; too few hides the shape, too many re-introduces noise — `rdrobust`'s companion `rdplot` picks a sensible default.)

**The fitted curves.** Overlay the local polynomial fit — two separate curves, one on each side of $c$, each extrapolated *to* the cutoff but not across it. These are the lines whose boundary heights you are differencing. Show them only over the bandwidth you actually used, so the reader sees the window your estimate rests on.

**The jump.** At $c$, the two fitted curves meet the cutoff at two different heights, and the vertical gap between them is $\hat\tau$. A convincing sharp-RD plot shows a clear, visible step at $c$ with smoothly-trending dots approaching from both sides; the jump should be obvious to the naked eye, not something only a regression can find. If you cannot *see* the discontinuity in a well-binned plot, be deeply skeptical of a regression that claims one.

How to read it like a referee: First, **is there a visible jump at the cutoff, and only at the cutoff?** A jump somewhere *other* than $c$ is a warning that your "effect" might be an artifact of functional form. Second, **are the trends on each side smooth and gentle, or is a high-order wiggle being fit?** Gentle near-linear trends are reassuring; a curve doing gymnastics to hit the boundary is the Gelman–Imbens pathology made visible. Third, for a fuzzy design, **plot the treatment too** — make a second RD plot with $D$ (the treatment probability) on the vertical axis and confirm there is a real jump in treatment at $c$, which is your first stage. Fourth, **plot pre-determined covariates** the same way (more on this in §9): they should *not* jump. A good RD paper is a wall of these plots, and learning to read them is learning to audit the design.

---

## 8. The McCrary density test: did people game the cutoff?

The local-randomization story has one fatal enemy: **manipulation**. If units can precisely control which side of the cutoff they land on, the coin-flip story collapses, and the units just above $c$ are no longer comparable to the units just below.

Picture Maya's lending cutoff at a credit score of $660$. Suppose a savvy applicant, or a loan officer helping them, can nudge a $658$ into a $661$ by paying down one small balance right before the pull — but *only* the more sophisticated, more financially-capable applicants know to do this. Then the people who "should" have been at $658$ but appear at $661$ are systematically more capable than the people who remain at $658$. The just-above and just-below groups are no longer exchangeable; the just-above group is now enriched with strategic, higher-type borrowers. Manipulation has **sorted** units across the cutoff on exactly the kind of unobserved characteristic RD assumes is balanced, and your jump now mixes the treatment effect with a selection effect. Sam's Russell example is comparatively safe here — a firm cannot finely control its market-cap rank to the dollar on the ranking day, which is much of *why* the Russell cutoff is such a clean instrument — but you must check, not assume.

The fingerprint of manipulation is a **discontinuity in the density of the running variable at the cutoff.** If borrowers are sneaking from just-below to just-above $660$, then you will see *too few* observations piled up just below the cutoff and *too many* just above — a cliff in the histogram of $X$ exactly at $c$. Under the clean, no-manipulation story, the density of $X$ should be *smooth* through $c$ (people don't bunch at a threshold they can't see or control). Under manipulation, it bunches.

This is what the **McCrary density test** checks.[^mccrary] McCrary (2008) proposed estimating the density of the running variable separately on each side of the cutoff and testing whether the two densities agree at $c$:

- **Null hypothesis:** the density of $X$ is continuous at $c$ (no sorting). This is what you *hope* to see.
- **Reject the null** $\Rightarrow$ there is a jump in the density — evidence of manipulation, and a serious threat to the design.

Mechanically, it is a local-linear density estimator on each side, with the test statistic being the log difference in the estimated densities at the boundary. A modern, more robust implementation (Cattaneo–Jansson–Ma) is what most packages ship, but the logic is McCrary's.[^cjm] Run it, plot the density, and report the test. A *failed* density test (a visible jump in the histogram at $c$) is often fatal: it says the cutoff is being gamed and your comparison is broken. A *passed* test is necessary but not sufficient reassurance — it rules out the crudest form of sorting but cannot by itself prove the design is clean (sorting that happens to preserve the density, though contrived, is logically possible).

[^mccrary]: McCrary, J. (2008). Manipulation of the Running Variable in the Regression Discontinuity Design: A Density Test. *Journal of Econometrics*, 142(2), 698–714.

[^cjm]: Cattaneo, M. D., Jansson, M., & Ma, X. (2020). Simple Local Polynomial Density Estimators. *Journal of the American Statistical Association*, 115(531), 1449–1455. This is the implementation shipped in the `rddensity` package and called from `rdrobust`'s diagnostics.

---

## 9. Validity threats and how to interrogate them

The McCrary test polices one threat — manipulation — but a careful RD analyst runs through a whole checklist, because RD's credibility rests entirely on the claim that *the cutoff is the only thing that changes at $c$.* Lee and Lemieux (2010) is the survey that systematized this discipline, and it is the single best thing to read after this chapter.[^leelemieux] Here are the threats, and the test for each.

[^leelemieux]: Lee, D. S., & Lemieux, T. (2010). Regression Discontinuity Designs in Economics. *Journal of Economic Literature*, 48(2), 281–355.

**Threat 1 — Manipulation / sorting (§8).** *Test:* the McCrary density test plus an eyeball of the histogram. If the density jumps at $c$, the design is in trouble.

**Threat 2 — Covariate imbalance at the cutoff.** Local randomization implies that *pre-determined* characteristics — things fixed before treatment, which the treatment cannot have caused — should be **balanced** across the cutoff, just as in a real experiment. *Test:* run the *same RD* with each pre-determined covariate as the outcome, and confirm there is **no jump**. If a stock's pre-reconstitution book-to-market ratio, or prior-year return, jumps discontinuously at the rank cutoff, something other than index membership is sorting at $c$ and your continuity assumption is suspect. This is the RD analog of a balance table, and it is one of the most persuasive checks you can run: the treatment should jump, and *nothing predetermined* should.

**Threat 3 — Other policies changing at the same cutoff (compound treatments).** This is the most insidious threat, because it passes the density test and the covariate-balance test and *still* breaks the design. The danger is that the *same* threshold $c$ triggers *more than one* thing at once. Cutoffs are administratively convenient, so institutions love to reuse them: a credit score of $660$ might flip *not only* loan approval *but also* the interest rate tier, the required down payment, and whether the loan is eligible for securitization — all at $660$. Then your RD jump in default rates is the combined effect of *all* of those changes bundled together, and you cannot attribute it to "loan approval" alone. The estimand is a real causal effect of *crossing the threshold*, but it is the effect of a **compound treatment**, not the clean single treatment you wanted. *Defense:* this one cannot be tested statistically — it must be *argued* from institutional knowledge, exactly like the exclusion restriction in Week 3. You must establish, from how the rule actually works, that the cutoff you study governs *only* the treatment you claim. (For fuzzy RD this is literally the exclusion restriction: if crossing $c$ affects $Y$ through any channel besides the treatment $D$, the Wald ratio is contaminated.)

**Threat 4 — A discontinuity in $X$ itself, or a "donut" problem.** Sometimes observations *at* the cutoff are weird — exact-threshold cases, rounding artifacts, or units that were re-scored. A common robustness check is the **donut RD**, which drops observations in a tiny window right at $c$ and re-estimates, to confirm the jump is not driven by anomalous exactly-at-the-line cases.

**Threat 5 — Bandwidth and specification sensitivity.** As §6 warned, an estimate that appears at one bandwidth and vanishes at half that bandwidth is not a finding. *Test:* report the estimate across a range of bandwidths and polynomial orders, and show stability. With CCT, report the robust bias-corrected interval, not the naive one.

The through-line of all five: **RD is identified by the assumption that crossing the cutoff changes one thing and only one thing, smoothly in everything else.** Threats 1, 2, and 4 leave statistical fingerprints you can hunt for; threat 3 does not, and must be defended in prose with institutional evidence. A polished RD study walks through every one of these, which is why RD sections in good finance papers run long.

---

## 10. Sharp vs. fuzzy in Sam's hands: the Russell wrinkle

It is worth being honest with Sam about a real subtlety in the Russell design, because it teaches the sharp-vs-fuzzy distinction better than any toy could. Naively, the Russell 1000/2000 boundary looks *sharp*: your end-of-May market-cap rank deterministically decides your index. But the *outcome* economists usually care about — actual passive-fund ownership, or index weight — does not jump deterministically with index membership, because index weights are based on *float-adjusted* market cap (not raw rank), and FTSE Russell added **banding** rules in 2007 that introduce a buffer zone to reduce churn. So in modern data the design is genuinely *fuzzy*: crossing the rank cutoff sharply raises the *probability* and *intensity* of Russell-2000-tracking ownership, but does not force a fixed amount. The right tool is the fuzzy-RD/IV ratio of §4 — the jump in the outcome (governance, liquidity, price) over the jump in passive ownership — with the above-cutoff indicator as the instrument.

This is also where a famous methodological fight lives, and you should know it exists: some influential Russell-RD studies used the *raw end-of-May rank* as the running variable, but the actual index assignment depends on a *float-adjusted* rank that researchers reconstruct imperfectly, and the choice of running variable and bandwidth has been shown to swing the headline results. Sam's takeaway is not "the Russell design is bad" — it is one of the best in finance — but "the running variable and the first stage must be defined *exactly* as the institution defines them," which is a special case of threat 3. When you read a Russell-RD paper, the first questions are: *what is the running variable, is the design sharp or fuzzy, and is the first stage (the jump in passive ownership) real and well-measured?* `[CHECK]` the specific methodological-debate citations (e.g., Appel–Gormley–Keim vs. Wei–Young vs. Glossner critiques) before relying on any one of them in a literature review.

---

## 11. The code

Here is the whole sharp-RD idea in one runnable block: simulate a world where landing in the Russell 2000 (treatment $D = \mathbf{1}\{X \geq c\}$) jumps next-year passive ownership by a true $\tau = 0.6$ points on top of a smooth trend, then estimate the jump with a triangular-kernel local-linear regression at several bandwidths — and, for contrast, with the global high-order polynomial Gelman–Imbens warns against. This uses only `numpy`/`pandas`/`statsmodels` so you can run it anywhere; nb4.3 redoes it the production way with `rdrobust` and CCT bandwidths.

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm

rng = np.random.default_rng(20260528)
N = 6_000
tau_true = 0.6                       # the true jump at the cutoff

# Running variable X: a stock's rank distance from the Russell 1000/2000 cutoff,
# recentered so the cutoff is c = 0. X >= 0 lands in the Russell 2000 (treatment D=1).
X = rng.uniform(-50, 50, size=N)
c = 0.0
D = (X >= c).astype(float)           # SHARP RD: treatment is a deterministic step at c

# Outcome Y: next-year passive-fund ownership (%). A smooth function of rank, plus the jump.
mu = 5.0 + 0.02 * X + 0.0020 * np.where(X > 0, X**2, 0.0)   # smooth & continuous through c
Y = mu + tau_true * D + rng.normal(0, 1.0, size=N)
df = pd.DataFrame({"Y": Y, "X": X, "D": D})

def local_linear_rd(df, c=0.0, h=8.0):
    """Triangular-kernel local-linear RD: one WLS with a cutoff dummy and separate slopes."""
    d = df.copy()
    d["Xc"] = d["X"] - c
    d = d[d["Xc"].abs() <= h].copy()                  # keep only the window |X - c| <= h
    w = (1.0 - (d["Xc"].abs() / h)).clip(lower=0)     # triangular kernel: 1 at c, 0 at edge
    M = pd.DataFrame({"const": 1.0, "D": d["D"], "Xc": d["Xc"], "Xc_D": d["Xc"] * d["D"]})
    res = sm.WLS(d["Y"], M, weights=w).fit(cov_type="HC1")
    return res                                         # coef on D is the estimated jump tau

for h in (4, 8, 16, 32):
    r = local_linear_rd(df, c=0.0, h=h)
    print(f"h={h:>2}  tau_hat={r.params['D']:.3f}  se={r.bse['D']:.3f}  n={int(r.nobs)}")

# Gelman-Imbens cautionary contrast: a GLOBAL quartic fit on ALL the data.
d = df.copy(); d["Xc"] = d["X"] - c
G = pd.DataFrame({"const": 1.0, "D": d["D"],
                  "X1": d["Xc"], "X2": d["Xc"]**2, "X3": d["Xc"]**3, "X4": d["Xc"]**4})
rg = sm.OLS(d["Y"], G).fit(cov_type="HC1")
print(f"global quartic  tau_hat={rg.params['D']:.3f}  se={rg.bse['D']:.3f}")
```

Running it prints the bias–variance trade-off of §6 in numbers. At the narrow bandwidth $h=4$ the estimate is close to the true $0.6$ (around $0.56$) but with a wide standard error (about $0.18$); as $h$ grows to $32$ the standard error shrinks (to about $0.07$) but the estimate drifts down toward $0.41$, because the wide window lets the curvature on the treated side bend the linear fit and bias the boundary height. The global quartic, fit to all $6{,}000$ points, reports a tight-looking standard error around a *biased* estimate near $0.41$ — the Gelman–Imbens pathology made concrete: a deceptively precise number that is simply in the wrong place, because data far from the cutoff are dictating the curvature at the boundary. The lesson is the chapter in miniature: stay local, choose the bandwidth honestly (which is what IK and CCT automate), and trust the robust interval over the naive one.

Two things to try in nb4.3. First, swap the hand-rolled local-linear function for `rdrobust(y=df.Y, x=df.X, c=0)` and confirm it reports a data-driven (CCT) bandwidth and a robust bias-corrected confidence interval that brackets the true $0.6$. Second, make the design *fuzzy* — let $D$ be random with probability $0.3$ below $c$ and $0.7$ above instead of a deterministic step — and use `rdrobust(..., fuzzy=df.D)` to recover the jump via the IV/Wald ratio of §4, watching how the estimate's precision degrades as you shrink the first-stage jump (the weak-instrument lesson of Chapter 3.5, in RD clothing).

---

## What to carry forward

Five things from this chapter will do real work later.

First, **the RD idea**: when a treatment switches at a known cutoff $c$ in a running variable $X$, units just above and just below $c$ are as-good-as-randomly assigned by the fine-grained noise in $X$, so the *jump* in $\mathbb{E}[Y\mid X]$ at $c$ is the causal effect — for the local population at the cutoff. The identifying assumption is *continuity* of the potential-outcome means at $c$, which is weaker than CIA and, unlike CIA, leaves checkable fingerprints when it fails.

Second, **sharp vs. fuzzy**. Sharp RD ($D = \mathbf{1}\{X\geq c\}$) reads the effect straight off the outcome jump. Fuzzy RD, where the cutoff only shifts the treatment *probability*, is instrumental variables with the above-cutoff indicator as the instrument: the effect is the jump in $Y$ divided by the jump in $D$ — the Week 3 Wald ratio — identifying a LATE for compliers at the cutoff under monotonicity. Everything you learned about relevance, exclusion, and weak instruments transfers directly.

Third, **stay local, stay low-order**. Estimate the boundary heights with local linear regression on a window around $c$ and a triangular kernel — *not* a global high-order polynomial, which (Gelman–Imbens) lets distant data corrupt the boundary estimate and makes the answer hostage to the arbitrary polynomial order.

Fourth, **bandwidth is a bias–variance trade-off, and you should automate it**. Narrow $h$: low bias, high variance. Wide $h$: low variance, high bias. Use a data-driven choice (Imbens–Kalyanaraman's MSE-optimal bandwidth) and report **CCT robust bias-corrected** confidence intervals, because the MSE-optimal bandwidth deliberately leaves a bias that the naive interval ignores. This is exactly what `rdrobust` delivers.

Fifth, **audit the design**. Run the McCrary density test for manipulation/sorting; check that pre-determined covariates do *not* jump at $c$; argue from institutions that *no other policy* changes at the same cutoff (the compound-treatment threat, untestable and the most dangerous); and show the estimate survives reasonable bandwidth and donut perturbations. Plot everything — a clean RD plot with a visible jump and smooth side-trends is half the argument, and a referee will look at it first.

---

## Your Turn

Open **nb4.3 — "RD with `rdrobust`; CCT bandwidths."** You will (1) reproduce Sam's sharp Russell-style design with `rdrobust`, comparing your hand-rolled triangular-kernel local-linear estimate to the package's data-driven CCT bandwidth and robust bias-corrected interval, and confirming both bracket the true jump; (2) build the RD plot — binned scatter plus the two fitted local-linear curves — with `rdplot`, and learn to *see* the discontinuity; (3) run the McCrary/Cattaneo–Jansson–Ma density test and a covariate-balance RD to audit the design; and (4) switch to a *fuzzy* design and recover the effect via the IV/Wald ratio, watching precision collapse as you weaken the first-stage jump.

Before you start, make sure you can answer these:

1. **Sharp or fuzzy?** For each design, say whether it is sharp or fuzzy RD and name the running variable, the cutoff, and the treatment: (a) a lender that *automatically* approves every applicant with a credit score $\geq 660$ and rejects all others; (b) a means-tested subsidy that families *become eligible to apply for* when household income drops below a threshold, but only $60\%$ of eligible families actually enroll; (c) crossing into the Russell 2000 at the reconstitution rank cutoff, where the outcome of interest is actual passive-fund ownership. For the fuzzy cases, write the estimand as a ratio of two jumps and state what plays the role of the instrument.

2. **Bandwidth and bias.** A classmate runs Sam's RD at a hand-picked bandwidth of $h = 40$ and reports a tight confidence interval that excludes zero. (a) Why might the *tightness* of that interval be misleading about the *accuracy* of the estimate? (b) In which direction would you expect the estimate to be biased if the true outcome curve is convex on the treated side, as in the §11 simulation? (c) Name the two procedures that would choose $h$ for them automatically, and explain what CCT's "robust bias correction" fixes that a naive $\hat\tau \pm 1.96\,\widehat{\text{se}}$ interval at the optimal bandwidth gets wrong.

3. **Auditing the cutoff.** Maya studies a loan-approval RD at a credit-score cutoff of $660$ and finds a large jump in two-year default rates. (a) Describe the McCrary density test in words and say what a *failed* test (a jump in the density at $660$) would imply about her design. (b) She runs the same RD with applicants' *pre-application* debt-to-income ratio as the outcome and finds it also jumps at $660$. What does this tell her, and is it good or bad news? (c) She later learns that at exactly $660$ the lender *also* switches the loan from a fixed to a lower variable interest rate. Which validity threat is this, why can no statistical test detect it, and what does it do to the interpretation of her default-rate jump?
