# Solutions — Problem Set 4.3 (Regression Discontinuity: Local-Polynomial Fitting and Bandwidth Experiments)

*Full worked solutions to `book/weeks/week-04/ps4.3.md`. Notation follows CONVENTIONS §3 and Ch 4.3. Core objects: the running variable $X$ and known cutoff $c$; the sharp treatment $D_i=\mathbf 1\{X_i\ge c\}$; the **sharp-RD estimand** $\tau_{\text{SRD}}=\lim_{x\downarrow c}\mathbb{E}[Y\mid X=x]-\lim_{x\uparrow c}\mathbb{E}[Y\mid X=x]$ identified under **continuity** of the potential-outcome means $\mathbb{E}[Y_i(1)\mid X=x]$, $\mathbb{E}[Y_i(0)\mid X=x]$ at $c$; **local linear** estimation on a window $|X_i-c|\le h$ with a **triangular kernel**; the bias–variance trade-off in $h$; the **fuzzy-RD** Wald ratio $\tau_{\text{FRD}}=(\text{jump in }Y)/(\text{jump in }D)$ with instrument $Z_i=\mathbf 1\{X_i\ge c\}$; and the §9 validity-threat checklist. Citations used by name: Gelman, A. & Imbens, G. (2019), "Why High-Order Polynomials Should Not Be Used in Regression Discontinuity Designs," Journal of Business & Economic Statistics 37(3), 447–456; Imbens, G. & Kalyanaraman, K. (2012), "Optimal Bandwidth Choice for the Regression Discontinuity Estimator," Review of Economic Studies 79(3), 933–959; Calonico, S., Cattaneo, M. D. & Titiunik, R. (2014), "Robust Nonparametric Confidence Intervals for Regression-Discontinuity Designs," Econometrica 82(6), 2295–2326; McCrary, J. (2008), "Manipulation of the Running Variable in the Regression Discontinuity Design: A Density Test," Journal of Econometrics 142(2), 698–714. All arithmetic verified numerically.*

---

## Problem 1 — State the estimand and the identifying assumption (14 pts)

**(a) (3 pts)** With cutoff $c=660$, the sharp-RD estimand is the jump in the conditional-mean function of $Y$ at the cutoff:
$$
\tau_{\text{SRD}}=\lim_{x\downarrow 660}\mathbb{E}[Y\mid X=x]-\lim_{x\uparrow 660}\mathbb{E}[Y\mid X=x].
$$
The first term is the limiting average distress as you approach $660$ from **above** (the approved side); the second is the limiting average as you approach from **below** (the rejected side). Their difference is a treatment effect, not just a slope, because the running variable $X$ is *continuous through* $660$ and enters the outcome smoothly — the smooth influence of "having a slightly higher score" is the *same* on both sides as $x\to 660$ and cancels in the difference, so the only thing that can open a gap between the two one-sided limits is approval switching from $0$ to $1$ at exactly $660$.

**(b) (4 pts)** **Continuity:** the average potential outcomes are continuous functions of $X$ at the cutoff,
$$
\mathbb{E}[Y_i(1)\mid X=x]\quad\text{and}\quad \mathbb{E}[Y_i(0)\mid X=x]\quad\text{are continuous in }x\text{ at }x=660.
$$
In plain words: *had the cutoff sat slightly higher* (so a barely-approved applicant had instead been rejected), that applicant's distress would have evolved **smoothly** through $660$ with no jump — the world does not put a cliff in the outcome at $660$ except through approval itself. The function we never directly observe on the treated side is the **untreated** potential outcome $\mathbb{E}[Y_i(0)\mid X=x]$ for the approved applicants (we cannot see how an approved person would have done *unapproved*); continuity says the just-**below**-cutoff (rejected) applicants supply that missing counterfactual in the limit.

**(c) (4 pts)** CIA (Week 3) demands that treated and untreated units be comparable **after conditioning on a complete set of observed covariates** — an untestable claim that *no* unobserved confounder is left, holding *everywhere* across the covariate space. Continuity demands far less: comparability only **in the limit, exactly at the cutoff**, secured by a smoothness condition on the potential-outcome means at one point. That is easier to defend because it does not require you to have measured and controlled for every confounder; it only requires that nothing *jumps discontinuously* at $c$ except treatment — and, as Problems 5–6 show, that requirement leaves observable fingerprints (a smooth density, balanced covariates) that you can actually go and check, unlike CIA's blanket no-unobservables claim.

**(d) (3 pts)** $\tau_{\text{SRD}}$ is the average effect of approval **for applicants right at $X=660$** — the *marginal* borrowers at the cutoff, not all approved borrowers and not deep-subprime or deep-prime applicants far from the line. This local estimand is exactly the right number for a regulator deciding whether to move the cutoff to $650$, because the people who would be newly affected by relocating the threshold are precisely the marginal applicants near it, and $\tau_{\text{SRD}}$ is their effect.

---

## Problem 2 — A by-hand local-linear RD (20 pts)

**(a) (6 pts)** Control-side line through $(-3,5.2)$ and $(-1,5.4)$. Two-point slope:
$$
b_-=\frac{5.4-5.2}{-1-(-3)}=\frac{0.2}{2}=\boxed{0.10}\ \text{(% per rank)}.
$$
Solve for the intercept using $(-1,5.4)$: $5.4=a_-+0.10\,(-1)\Rightarrow a_-=5.4+0.10=\boxed{5.5}$. (Check with $(-3)$: $5.5+0.10(-3)=5.2$ ✓.) The extrapolated control-side height at the cutoff is the intercept,
$$
\lim_{x\uparrow 0}\widehat{\mathbb{E}}[Y\mid X=x]=a_-=\boxed{5.5}.
$$

**(b) (6 pts)** Treated-side line through $(+1,5.9)$ and $(+3,6.1)$. Slope:
$$
b_+=\frac{6.1-5.9}{3-1}=\frac{0.2}{2}=\boxed{0.10}\ \text{(% per rank)}.
$$
Intercept using $(+1,5.9)$: $5.9=a_++0.10(1)\Rightarrow a_+=5.9-0.10=\boxed{5.8}$. (Check with $(+3)$: $5.8+0.10(3)=6.1$ ✓.) The extrapolated treated-side height at the cutoff is
$$
\lim_{x\downarrow 0}\widehat{\mathbb{E}}[Y\mid X=x]=a_+=\boxed{5.8}.
$$

**(c) (4 pts)** The estimated jump is
$$
\hat\tau_{\text{SRD}}=a_+-a_-=5.8-5.5=\boxed{0.30}\ \text{percentage points}.
$$
This is *not* the difference of the two nearest bins ($5.9-5.4=0.5$) because those two bins sit at $x=+1$ and $x=-1$, not at the cutoff $x=0$. The local-linear fit corrects for the fact that the outcome is **trending** on each side: it extrapolates each side's line *to the boundary* $x=0$ before differencing, removing the part of the nearest-bin gap that is just the smooth slope of $Y$ in $X$ carrying you from $-1$ to $+1$, rather than the treatment.

**(d) (4 pts)** The nearest-bin difference ($0.5$) is **bigger** than the local-linear jump ($0.30$). Both side-trends slope **upward** (each slope is $+0.10$ per rank), so as you move from the control bin at $x=-1$ rightward to the treated bin at $x=+1$, the outcome rises for *two* reasons mixed together: the genuine treatment jump *and* two ranks' worth of the rising smooth trend ($2\times 0.10=0.20$). The nearest-bin shortcut attributes all of that $0.5$ to treatment, so it is **biased upward** by exactly the $0.20$ of trend it failed to subtract; the local-linear fit, by extrapolating to the common point $x=0$, nets out the trend and leaves the clean $0.30$. (The triangular kernel would not change anything here: a kernel reweights observations, but two points already determine a unique straight line, so any positive weights produce the same line through them.)

---

## Problem 3 — Bandwidth, bias, variance, and the global-polynomial trap (18 pts)

**(a) (5 pts)** As $h$ goes from $4$ to $32$:
- **Standard error falls** ($0.18\to 0.07$). A wider window admits many more observations, and each fitted side-line is then estimated from far more points, so its sampling variability — and the variability of the boundary heights you difference — shrinks. More data, less noise: *lower variance*.
- **Bias rises** ($\hat\tau$ drifts from $0.56$ away from the truth $0.60$, down to $0.41$). The smooth part of $\mathbb{E}[Y\mid X]$ is **convex on the treated side**. A straight line fit over a wide treated window cannot follow that upward curve; it under-reads the treated-side curve's *height at the boundary*, pulling $a_+$ — and hence the jump — too low. The wider the window, the more curvature the line must ignore, so *higher bias*. This is the bias–variance trade-off made numerical: too narrow is honest-but-noisy, too wide is precise-but-wrong.

**(b) (3 pts)** Naive $95\%$ intervals $\hat\tau\pm 1.96\,\widehat{\text{se}}$:
$$
h=4:\quad 0.56\pm 1.96(0.18)=0.56\pm 0.353=[\,0.21,\ 0.91\,]\quad(\text{width }0.71),
$$
$$
h=32:\quad 0.41\pm 1.96(0.07)=0.41\pm 0.137=[\,0.27,\ 0.55\,]\quad(\text{width }0.27).
$$
An honest analyst prefers the **$h=4$ window**: its interval is wide but it is *centered near the truth* and actually contains $0.60$, whereas the tight $h=32$ interval is mis-centered and **excludes** the true $0.60$ entirely. "Narrow" measures only *precision* (how reproducible the estimate is); it says nothing about *accuracy* (whether the estimate is aimed at the right number) — a confidently-stated wrong answer is still wrong.

**(c) (5 pts)** The global quartic returns the same biased point ($\approx 0.41$) with a *tight* standard error — precise *and* wrong. **Gelman–Imbens (2019)** give three reasons a high-order global polynomial mis-estimates a boundary value: (i) polynomials behave **erratically near the edges** of the data, and the cutoff is exactly where two one-sided extrapolations meet; (ii) it lets data **far from the cutoff** (huge R1000 firms, tiny deep-R2000 firms) dictate the curvature right at $c$, manufacturing spurious wiggles or erasing real jumps at the boundary; (iii) the estimate is **hostage to the arbitrary polynomial order**, swinging between a cubic and a quartic with no principled way to choose, and the implicit weights on individual observations can even go negative. The "deceptively tight standard error around a wrong number" is the lesson in miniature: the global fit uses all $6{,}000$ points so its *variance* is small, but it is estimating the *wrong object* (a boundary height corrupted by distant data), so small se buys you nothing — precision around a biased target is just confident inaccuracy.

**(d) (5 pts)**
(i) **Imbens–Kalyanaraman (2012)** choose the bandwidth that **minimizes the asymptotic mean squared error (MSE)** of the RD estimator — they estimate the two ingredients of MSE (the curvature of the outcome function at $c$, which drives bias, and the noise variance, which drives variance) and plug them into the optimal-$h$ formula. Because MSE = (bias)$^2$ + variance, *minimizing* it deliberately accepts **some non-zero bias** to buy a large variance reduction; the MSE-optimal $h$ is, by construction, large enough that the leading bias term is **not negligible**.
(ii) That leftover bias breaks the naive interval, because $\hat\tau\pm 1.96\,\widehat{\text{se}}$ assumes the estimator is centered on the truth — at the MSE-optimal $h$ it is not, so the interval is mis-located and **undercovers** (contains the true effect less than $95\%$ of the time). **Calonico–Cattaneo–Titiunik (2014)** robust bias-correction does two things: (1) it **estimates the leading bias term explicitly and subtracts it** from the point estimate (bias correction), and (2) it **inflates the standard error** to account for the extra noise that the bias-correction step itself introduces (the "robust" standard error). The repaired interval then achieves its nominal $95\%$ coverage even at the MSE-optimal bandwidth — fixing the undercoverage of the naive interval.

---

## Problem 4 — Fuzzy RD as the Wald ratio (18 pts)

**(a) (4 pts)** Jump in treatment (first stage) and jump in outcome (reduced form) at $c=0$:
$$
\text{jump in }D=\lim_{x\downarrow 0}\mathbb{E}[D\mid X]-\lim_{x\uparrow 0}\mathbb{E}[D\mid X]=0.70-0.30=\boxed{0.40},
$$
$$
\text{jump in }Y=\lim_{x\downarrow 0}\mathbb{E}[Y\mid X]-\lim_{x\uparrow 0}\mathbb{E}[Y\mid X]=61.0-57.4=\boxed{3.6}.
$$
The treatment jump is the empirical content of **relevance** — the fuzzy-RD analog of the first stage. A jump of $0.40$ (treatment probability rising from $30\%$ to $70\%$ at the cutoff) is **reassuring**: it is a substantial, visible discontinuity, far from the near-zero denominator that would invite the weak-instrument pathology.

**(b) (4 pts)** The fuzzy-RD estimand is the ratio of the two jumps:
$$
\hat\tau_{\text{FRD}}=\frac{\text{jump in }Y}{\text{jump in }D}=\frac{61.0-57.4}{0.70-0.30}=\frac{3.6}{0.40}=\boxed{9.0}\ \text{governance-index points}.
$$
Interpretation: crossing the cutoff raised the governance index by $3.6$ points but only moved an extra $40\%$ of firms into heavy passive ownership; scaling the reduced form up by the dose of treatment delivered, heavy passive ownership raises the governance index by about **$9$ points** — for the **firms the cutoff actually moved into treatment** (the compliers at the cutoff), under monotonicity, not for all firms.

**(c) (4 pts)** The instrument is $Z_i=\mathbf 1\{X_i\ge 0\}$, the indicator for landing on the **Russell-2000 (above-cutoff) side**. The mapping to Week 3:
- the **jump in $D$** ($0.40$) is the **first stage** — the effect of the instrument (crossing the cutoff) on the treatment;
- the **jump in $Y$** ($3.6$) is the **reduced form** — the effect of the instrument on the outcome, ignoring $D$.
$\hat\tau_{\text{FRD}}$ is *literally* the Wald estimator of Ch 3.4, $\hat\beta_1^{\text{Wald}}=(\text{reduced form})/(\text{first stage})$, with the above-cutoff indicator playing the role of the randomized instrument: fuzzy RD is instrumental variables where the instrument is "which side of $c$ you landed on."

**(d) (3 pts)** **Exclusion** here means: crossing the rank cutoff must affect the governance index **only through** the treatment (heavy passive ownership), and nothing else may jump at $c$. A concrete violation: if crossing into the Russell 2000 *also* triggers, at the same rank, a change in **analyst-coverage or index-reconstitution disclosure rules** that independently affects governance, then $Z$ reaches $Y$ by a second road that bypasses $D$, and the Wald ratio is contaminated. This is an instance of the **compound-treatment** threat (§9, Threat 3) — for a fuzzy design, exclusion *is* the no-other-channel requirement.

**(e) (3 pts)** With the treatment jump collapsing to $0.05$ while the outcome jump stays near $3.6$, the point estimate balloons to $3.6/0.05=72$ — the ratio becomes enormous and unstable because you are **dividing by a near-zero first stage**. Far worse, the *precision* collapses: the standard error of a ratio explodes as its denominator approaches zero, so the confidence interval blows up and the estimate becomes untrustworthy. This is the **weak-instrument pathology** of Ch 3.5, in RD clothing — a weak first stage (tiny treatment jump) makes the IV/Wald estimate both wildly imprecise and maximally vulnerable to any small exclusion violation.

---

## Problem 5 — The McCrary density test and manipulation (16 pts)

**(a) (4 pts)** The **McCrary (2008) density test** estimates the **density of the running variable $X$** (here, credit scores) separately on each side of the cutoff — a local-linear density estimator on the left and on the right — and tests whether the two estimated densities **agree at $c$**. The **null hypothesis** is that the density of $X$ is *continuous at $660$* (no sorting). **Rejecting** the null means there is a jump in the density at the cutoff — evidence of **manipulation**. You *hope* to **fail to reject**: a smooth density is consistent with the clean, no-manipulation story in which applicants cannot finely control which side of $660$ they land on.

**(b) (4 pts)** If capable applicants sort from just-below to just-above $660$, the histogram develops a characteristic two-sided distortion at the cutoff: **too few** observations pile up in the bins **immediately below** $660$ (those people moved out) and **too many** in the bins **immediately above** $660$ (that is where they moved to). The result is a visible **cliff in the histogram of $X$ exactly at $660$** — a downward step on the left, an upward step on the right. That is the link from "sorting": units relocating across the line deplete one side and overfill the other, which *is* a discontinuity in the density at $c$, precisely what McCrary's test is built to detect. Under the no-manipulation story the density should pass through $660$ smoothly (people don't bunch at a threshold they can't control).

**(c) (4 pts)** Sorting breaks the design even though approval still flips cleanly at $660$, because RD's credibility rests on **local randomization / continuity**, not on the sharpness of the treatment rule. The just-**above** group becomes **enriched** with strategic, more financially-capable applicants — the ones who knew to pay down a balance to cross the line — precisely the kind of **unobserved characteristic** (sophistication, resources) that continuity assumes is *balanced* across the cutoff. Once the just-above group is systematically more capable than the just-below group, the two are **no longer exchangeable**: they differ in a confounder, not just in treatment. The resulting $\hat\tau_{\text{SRD}}$ then **mixes the causal effect of approval with a selection effect** — the capability gap between movers and stayers — so the jump no longer cleanly identifies the treatment.

**(d) (4 pts)** (i) A passed density test is **necessary but not sufficient** because it rules out only the *crudest* fingerprint of sorting — a discontinuity in the *density* — but cannot by itself prove the design is clean: sorting that happens to preserve the density (contrived but logically possible), or any threat that does not move the density, slips right past it. A smooth density is a hurdle the design must clear, not a certificate that it is valid. (ii) One §9 threat a passed density test cannot rule out at all is the **compound-treatment** threat (Threat 3): if some *other* policy changes at the same cutoff, the density of $X$ stays perfectly smooth (nobody is sorting), yet the design is broken — exactly the case Problem 6 develops. (Covariate imbalance, Threat 2, is likewise invisible to the density test.)

---

## Problem 6 — Validity threats: the compound-treatment critique (14 pts)

**(a) (4 pts)** This is the **compound-treatment** threat (§9, Threat 3): the *same* threshold $c=660$ triggers *more than one thing at once* — approval **and** the rate switch **and** securitization eligibility. The one-sentence identification condition it violates is the through-line of §9: **RD is identified by the assumption that crossing the cutoff changes one thing and only one thing, smoothly in everything else.** Here three things change at $660$, so that assumption fails.

**(b) (4 pts)** No statistical test can detect a compound treatment because every test in the kit checks for *some discontinuity*, and here **all the discontinuities are real and all happen at the same point** — there is nothing anomalous to flag. McCrary sees a smooth density (nobody is sorting). Covariate balance sees no jump (pre-determined characteristics really are balanced). A donut RD still finds the jump (it isn't driven by exactly-at-the-line cases). A bandwidth sweep finds the jump stable (it is a genuine effect of crossing $660$). The contrast with the **manipulation** threat of Problem 5 is exactly this: manipulation leaves a *statistical fingerprint* (a density discontinuity) that a test can catch, whereas a compound treatment leaves **none** — the jump is real, it is simply the effect of the *bundle*. Maya must therefore use **institutional evidence**: documentation of how the underwriting rule actually works, to establish what does and does not change at $660$ — exactly as the exclusion restriction is argued, not tested, in Week 3.

**(c) (3 pts)** Maya's RD still identifies a real causal effect — the effect of **crossing the $660$ threshold**, i.e. the effect of the *bundle* (approval + the switch to a lower variable rate + securitization eligibility) taken together, for applicants at the cutoff:
$$
\hat\tau=\text{effect on default of the entire }660\text{-cutoff package, at the margin.}
$$
It is **not** the "effect of approval" she wanted, because approval is only one of three things that flip at $660$; she cannot attribute the default jump to approval alone when the rate change and securitization moved in lockstep with it.

**(d) (3 pts)** In a fuzzy design with $Z=\mathbf 1\{X\ge 660\}$ as the instrument for approval, the compound treatment breaks **exclusion**. Exclusion requires that crossing $660$ affect default *only through* approval; but the rate switch and securitization give crossing $660$ **additional channels to default that bypass approval**, so $\operatorname{Cov}(Z,\varepsilon)\ne 0$ and the Wald ratio is contaminated — it scales up a reduced form that already includes the rate and securitization effects, mis-crediting all of them to approval.

---

*End of solutions for PS 4.3. Cross-references: Ch 4.3 (sharp-RD estimand & continuity §2–§3, fuzzy RD/Wald ratio §4, local linear vs. global polynomial / Gelman–Imbens §5, bandwidth bias–variance & IK/CCT §6, reading the RD plot §7, McCrary density test §8, validity threats §9, Russell sharp-vs-fuzzy wrinkle §10, code §11); Ch 3.1 (potential outcomes); Ch 3.4 (Wald estimator, relevance/exclusion, LATE/compliers, monotonicity); Ch 3.5 (weak-instrument pathology, here the collapsing first-stage jump of P4(e)). Numeric keys: P2 control line $b_-=0.10$, $a_-=5.5$; treated line $b_+=0.10$, $a_+=5.8$; jump $\hat\tau_{\text{SRD}}=0.30$ (vs. nearest-bin $0.5$, biased up by $0.20$ of trend). P3 naive CIs $h{=}4$:$[0.21,0.91]$ (brackets truth $0.60$), $h{=}32$:$[0.27,0.55]$ (excludes $0.60$). P4 jump in $D=0.40$, jump in $Y=3.6$, $\hat\tau_{\text{FRD}}=9.0$; weak case $3.6/0.05=72$. Companion: nb4.3 (rdrobust, CCT bandwidth, rdplot, density test, fuzzy IV/Wald).*
