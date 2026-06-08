# Solutions — PS 3.1 (Potential-Outcomes Algebra & the Selection-Bias Decomposition)

**Problem set:** `book/weeks/week-03/ps3.1.md` (PS 3.1, Week 3).
**Chapter:** Ch 3.1 — Potential Outcomes, SUTVA, and the Fundamental Problem of Causal Inference.

These are full worked solutions, not just answers. Notation follows `CONVENTIONS.md` and locks to Ch 3.1: potential outcomes $Y_i(1), Y_i(0)$; treatment indicator $D_i\in\{0,1\}$; observation rule $Y_i = D_i Y_i(1) + (1-D_i)Y_i(0)$; individual effect $\tau_i = Y_i(1)-Y_i(0)$; estimands $\text{ATE}=\mathbb{E}[\tau_i]$ and $\text{ATT}=\mathbb{E}[\tau_i\mid D_i=1]$; naive difference $\Delta = \mathbb{E}[Y_i\mid D_i=1]-\mathbb{E}[Y_i\mid D_i=0]$; the master decomposition and its selection-bias term; SUTVA; and independence under randomization. Conditional means $\mathbb{E}[\cdot\mid D_i=1]$ are taken over the treated group only. Every numerical result here was confirmed in Python (NumPy boolean-mask group means and, for Problem 5, an exhaustive enumeration of assignments); verifying notes appear where useful.

---

## Problem 1 — The observation rule and individual effects (12 points)

**(a) (4 pts)** The observation rule $Y_i = D_i Y_i(1) + (1-D_i)Y_i(0)$ selects, for each unit, the potential outcome matching the treatment actually taken: if $D_i=1$ we see $Y_i(1)$ (and $Y_i(0)$ is missing); if $D_i=0$ we see $Y_i(0)$ (and $Y_i(1)$ is missing). Reading the table:

| Unit $i$ | $D_i$ | Observed $Y_i$ | Missing counterfactual |
|:---:|:---:|:---:|:---:|
| 1 | $1$ | $Y_1(1)=45$ | $Y_1(0)=35$ |
| 2 | $0$ | $Y_2(0)=20$ | $Y_2(1)=44$ |
| 3 | $1$ | $Y_3(1)=52$ | $Y_3(0)=40$ |
| 4 | $0$ | $Y_4(0)=25$ | $Y_4(1)=49$ |
| 5 | $1$ | $Y_5(1)=53$ | $Y_5(0)=45$ |
| 6 | $0$ | $Y_6(0)=30$ | $Y_6(1)=48$ |

So Maya's observed outcome vector is $Y = (45,\,20,\,52,\,25,\,53,\,30)$. Everything in the "missing counterfactual" column is structurally invisible to her — it is the road not taken for each unit.

**(b) (4 pts)** The individual effects $\tau_i = Y_i(1)-Y_i(0)$:

$$
\begin{aligned}
\tau_1 &= 45-35 = 10, & \tau_2 &= 44-20 = 24, & \tau_3 &= 52-40 = 12,\\
\tau_4 &= 49-25 = 24, & \tau_5 &= 53-45 = 8, & \tau_6 &= 48-30 = 18.
\end{aligned}
$$

The program helps **units 2 and 4 the most** (a $+24$-point gain each) and **unit 5 the least** (a $+8$-point gain). Notice this is already a teaser for Problem 2: the units who benefit most (2 and 4) are *control* units, while the unit who benefits least (5) is *treated*.

**(c) (4 pts)** Maya sees only $D_i$ and the single observed $Y_i$ — one number per person, the potential outcome the treatment switch selected. To compute *any* $\tau_i = Y_i(1)-Y_i(0)$ she would need *both* potential outcomes for the same person, but only one is ever realized; the other never happens and leaves no trace in the data. This is the **Fundamental Problem of Causal Inference** (Holland 1986): it is a missing-data problem, not a sample-size problem, so a larger $N$ — even infinite data on person $1$ — cannot conjure the missing value. For **unit 1 specifically**, Maya observes $Y_1 = Y_1(1) = 45$; the entry she can never see is the counterfactual $Y_1(0) = 35$, what unit 1's credit gain *would have been* had she skipped the program.

---

## Problem 2 — ATE versus ATT from the science table (16 points)

We reuse the individual effects $\tau = (10, 24, 12, 24, 8, 18)$ from Problem 1(b). Treated units are $\{1,3,5\}$ ($D_i=1$); untreated are $\{2,4,6\}$ ($D_i=0$).

**(a) (4 pts)** Average over all six:

$$
\text{ATE} = \mathbb{E}[\tau_i] = \frac{10+24+12+24+8+18}{6} = \frac{96}{6} = 16.
$$

If the program were given to everyone in this population versus no one, the average credit-score gain attributable to it is **$16$ points**.

**(b) (4 pts)** Average over the treated only, then over the untreated only:

$$
\text{ATT} = \mathbb{E}[\tau_i\mid D_i=1] = \frac{\tau_1+\tau_3+\tau_5}{3} = \frac{10+12+8}{3} = \frac{30}{3} = 10,
$$
$$
\text{ATC} = \mathbb{E}[\tau_i\mid D_i=0] = \frac{\tau_2+\tau_4+\tau_6}{3} = \frac{24+24+18}{3} = \frac{66}{3} = 22.
$$

(Consistency check: the ATE is the size-weighted average of these two, $\tfrac{1}{2}(10) + \tfrac{1}{2}(22) = 16$, since the two groups are equal-sized. $\checkmark$)

**(c) (4 pts)** $\text{ATT}=10 \neq 16 = \text{ATE}$ — indeed $\text{ATT} < \text{ATE} < \text{ATC}$. The pattern in the table is that the treated units ($1,3,5$) have *high* untreated outcomes $Y_i(0) = 35, 40, 45$ but *small* treatment effects $\tau_i = 10, 12, 8$, while the untreated units ($2,4,6$) have *low* $Y_i(0) = 20,25,30$ but *large* effects $\tau_i = 24,24,18$. In words: the people who selected into the program are the already-high-credit, "savvy" types who had the least room to gain (a ceiling effect), and the program actually helps the *non*-enrollees more. Selection here is on a *high baseline* paired with *low responsiveness* — exactly the kind of self-selection that makes ATT and ATE diverge.

**(d) (4 pts)** "How much does our program help the people who actually use it?" is answered by the **ATT $=10$ points** — it conditions on $D_i=1$, the actual users. The *different* question "should we make this program universal?" is answered by the **ATE $=16$ points**, because making it universal would extend it to the currently-untreated, who (in this table) respond much more strongly; their large effects pull the all-population average above the treated-only average. Reporting one while claiming the other — e.g., touting the $16$-point ATE as what current users get, or the $10$-point ATT as the universal-rollout effect — is exactly the estimand confusion the chapter warns against.

---

## Problem 3 — Derive and apply the selection-bias decomposition (20 points)

**(a) (10 pts)** We want to rewrite the naive difference $\Delta = \mathbb{E}[Y_i\mid D_i=1] - \mathbb{E}[Y_i\mid D_i=0]$ in potential-outcomes terms.

*Step 1 — apply the observation rule (definition, not assumption).* Among the treated ($D_i=1$) the observation rule gives $Y_i = Y_i(1)$, so the observed mean *is* the treated-group mean of the treated potential outcome:
$$
\mathbb{E}[Y_i\mid D_i=1] = \mathbb{E}[Y_i(1)\mid D_i=1].
$$
Among the untreated ($D_i=0$), $Y_i = Y_i(0)$, so
$$
\mathbb{E}[Y_i\mid D_i=0] = \mathbb{E}[Y_i(0)\mid D_i=0].
$$
Subtract:
$$
\Delta = \mathbb{E}[Y_i(1)\mid D_i=1] - \mathbb{E}[Y_i(0)\mid D_i=0]. \tag{$\ast$}
$$
This is exact and assumption-free — just the observation rule applied twice.

*Step 2 — add and subtract the right counterfactual.* We are aiming at the ATT, $\mathbb{E}[Y_i(1)-Y_i(0)\mid D_i=1]$, which requires the term $\mathbb{E}[Y_i(0)\mid D_i=1]$ — *the treated group's untreated potential outcome*, the missing counterfactual "how would the enrollees have done with no program?" That term is nowhere in $(\ast)$. *That particular term* is the one to conjure, because it is exactly what the ATT needs and exactly what is absent. So add and subtract it (a net of zero):
$$
\Delta = \mathbb{E}[Y_i(1)\mid D_i=1]
\;-\; \mathbb{E}[Y_i(0)\mid D_i=1]
\;+\; \mathbb{E}[Y_i(0)\mid D_i=1]
\;-\; \mathbb{E}[Y_i(0)\mid D_i=0].
$$

*Step 3 — regroup into two named pairs.*
$$
\Delta = \underbrace{\Big(\mathbb{E}[Y_i(1)\mid D_i=1] - \mathbb{E}[Y_i(0)\mid D_i=1]\Big)}_{=\,\mathbb{E}[\tau_i\mid D_i=1]\,=\,\text{ATT}}
\;+\;
\underbrace{\Big(\mathbb{E}[Y_i(0)\mid D_i=1] - \mathbb{E}[Y_i(0)\mid D_i=0]\Big)}_{\text{selection bias}}.
$$
The first pair is the difference of two conditional means *over the same group* $D_i=1$, which by linearity of expectation is $\mathbb{E}[Y_i(1)-Y_i(0)\mid D_i=1] = \text{ATT}$. The second pair is the selection-bias term. This is the master decomposition:
$$
\boxed{\ \Delta \;=\; \text{ATT} \;+\; \big(\mathbb{E}[Y_i(0)\mid D_i=1] - \mathbb{E}[Y_i(0)\mid D_i=0]\big).\ } \qquad\checkmark
$$

*Which step is an assumption?* **None of them.** Every line is the observation rule (a definition) or the linearity of expectation (pure algebra). The decomposition is an *identity* that holds for any data whatsoever — randomized or hopelessly confounded. That is precisely why it is so powerful: it does not let you off the hook anywhere. The only question the rest of the week asks is whether the *selection-bias term equals zero*, which is where assumptions (randomization, or conditional independence) finally enter — not in the decomposition itself.

**(b) (6 pts)** Maya's round-up feature. Given $\mathbb{E}[Y_i\mid D_i=1]=0.70$, $\mathbb{E}[Y_i\mid D_i=0]=0.46$, and the (unobservable) truth $\text{ATT}=0.09$.

(i) Naive difference:
$$
\Delta = 0.70 - 0.46 = 0.24.
$$

(ii) The enrollees' missing counterfactual. By the observation rule the treated observed mean *is* their treated potential-outcome mean, $\mathbb{E}[Y_i(1)\mid D_i=1] = 0.70$. Since $\text{ATT} = \mathbb{E}[Y_i(1)\mid D_i=1] - \mathbb{E}[Y_i(0)\mid D_i=1]$, solve for the counterfactual:
$$
\mathbb{E}[Y_i(0)\mid D_i=1] = \mathbb{E}[Y_i(1)\mid D_i=1] - \text{ATT} = 0.70 - 0.09 = 0.61.
$$

(iii) Selection-bias term:
$$
\text{selection bias} = \mathbb{E}[Y_i(0)\mid D_i=1] - \mathbb{E}[Y_i(0)\mid D_i=0] = 0.61 - 0.46 = 0.15.
$$
(Here $\mathbb{E}[Y_i(0)\mid D_i=0] = \mathbb{E}[Y_i\mid D_i=0] = 0.46$ by the observation rule.)

*Verify the decomposition:* $\text{ATT} + \text{selection bias} = 0.09 + 0.15 = 0.24 = \Delta$. $\checkmark$

**(c) (4 pts)** Maya's headline $24$-percentage-point gap splits into **$9$ points of genuine program effect on the treated** and **$15$ points of selection bias**. Her naive number overstates the true effect on the treated by a factor of $0.24/0.09 \approx 2.7$ — nearly three times too big. The reason more data cannot fix it is that the broken quantity is $\mathbb{E}[Y_i(0)\mid D_i=1] = 0.61$, the enrollees' counterfactual: it is *missing*, not *noisy*. Ten times the sample sharpens the estimates of $0.70$ and $0.46$, but those two numbers were never the problem; the $0.61$ that would let her subtract off the bias is structurally absent by the Fundamental Problem, so a precise estimate of a biased difference is just a precise wrong answer.

---

## Problem 4 — Spot the SUTVA violation (16 points)

**(a) (5 pts) Devon's crypto tax credit — nationwide extrapolation.**
(i) **SUTVA is violated — Part 1 (no interference), in its general-equilibrium form.** (ii) In the scattered pilot, one person's receipt of the credit does not move the market price, so each individual's $Y_i(\cdot)$ depends only on her own treatment and the pilot estimate is fine. At nationwide scale, the surge of subsidized demand *moves the price of the crypto asset*; now a non-recipient's untreated potential outcome $Y_i(0)$ — her adoption decision absent the credit — shifts because of *everyone else's* treatment, transmitted through the equilibrium price. The single number $Y_i(d)$ is no longer well-defined as a function of $i$'s own treatment alone; it depends on the whole vector of who got the credit. (iii) Randomizing *who* receives the credit does nothing, because the problem is not unbalanced groups — it is that scaling the treatment up changes the price everyone faces, so the small-scale (partial-equilibrium) effect simply does not extrapolate to the large-scale (general-equilibrium) policy regardless of how cleanly assignment was randomized.

**(b) (5 pts) Priya's ESG disclosure standard.**
(i) **SUTVA is violated — Part 2 (no hidden versions of treatment).** (ii) "Adopting the standard," coded $D_i=1$, is secretly a spectrum: an audited line-by-line report and a vague two-paragraph box-check are genuinely different treatments lumped under one label. So there is no single well-defined $Y_i(1)$ for a firm — "the potential outcome under treatment" is ambiguous because it depends on *which version* of treatment, and Priya's estimate is an uninterpretable blend of the effects of several distinct treatments masquerading as one. (iii) Randomizing which firms adopt would balance the groups, but it cannot make a smeared-together treatment well-defined: the comparison would still average over hidden intensities, so "the effect of adoption" remains meaningless until Priya defines a single, consistent treatment (e.g., audited reports only).

**(c) (6 pts) Sam's roommate workshop.**
(i) **SUTVA is violated — Part 1 (no interference), via spillovers.** (ii) Attendees and their roommate controls cook, shop, and split bills together, so an attendee passes budgeting habits to her control roommate. The control's $Y_i(0)$ — supposedly her quiz score in a "no-workshop" world — is contaminated by her *roommate's* treatment, second-hand. The potential outcome $Y_i(0)$ is no longer a property of unit $i$ alone; it depends on whether $i$'s roommate was treated, which the notation forbids. The control group is no longer a clean no-treatment baseline (it is partly treated), so the attendee-vs-control gap *understates* the workshop's true effect. (iii) Randomization does not help — and this is the trap, because the assignment here genuinely *was* randomized. The coin balances *who* gets treated, but it does nothing to stop the treatment from *leaking across roommates*; interference is a property of how units are connected, not of how assignment was decided. The fix is design, not randomization: assign treatment at the *dorm* (cluster) level so that both roommates are in the same arm, removing the within-dorm contamination.

---

## Problem 5 — Randomization zeroes the selection bias (20 points)

The population: eight applicants, with $Y_i(0)=1$ for four "savvy" types and $Y_i(0)=0$ for four others, so $\mathbb{E}[Y_i(0)] = \tfrac{4(1)+4(0)}{8} = 0.5$.

**(a) (4 pts) Self-selection world.** The four savvy ($Y(0)=1$) enroll, the four others ($Y(0)=0$) stay out:
$$
\mathbb{E}[Y_i(0)\mid D_i=1] = \frac{1+1+1+1}{4} = 1, \qquad
\mathbb{E}[Y_i(0)\mid D_i=0] = \frac{0+0+0+0}{4} = 0,
$$
$$
\text{selection bias} = 1 - 0 = 1.
$$
This is the worst possible case: the entire untreated-outcome gap between the groups is selection. The two groups are *not* the same kind of people at all — the treated would have had perfect approval even with no program, the controls zero — so the naive comparison is pure contamination on the $Y(0)$ scale, with no claim to causality.

**(b) (5 pts) Balanced-coin world.** Now each arm holds exactly two savvy ($Y(0)=1$) and two non-savvy ($Y(0)=0$):
$$
\mathbb{E}[Y_i(0)\mid D_i=1] = \frac{1+1+0+0}{4} = 0.5, \qquad
\mathbb{E}[Y_i(0)\mid D_i=0] = \frac{1+1+0+0}{4} = 0.5,
$$
$$
\text{selection bias} = 0.5 - 0.5 = 0.
$$
Both group means now equal the population $\mathbb{E}[Y_i(0)] = 0.5$, because balanced assignment makes the two arms interchangeable slices of the same population.

**(c) (5 pts)** Randomization makes $(Y_i(0), Y_i(1)) \perp\!\!\!\perp D_i$. Independence means that conditioning on $D_i$ carries no information about the potential outcomes, so the conditional expectation of $Y_i(0)$ does not depend on which value $D_i$ takes:
$$
\mathbb{E}[Y_i(0)\mid D_i=1] = \mathbb{E}[Y_i(0)] = \mathbb{E}[Y_i(0)\mid D_i=0].
$$
(The middle equality is the definition of independence: the conditional mean collapses to the unconditional mean.) Substituting into the selection-bias term,
$$
\text{selection bias} = \mathbb{E}[Y_i(0)\mid D_i=1] - \mathbb{E}[Y_i(0)\mid D_i=0] = \mathbb{E}[Y_i(0)] - \mathbb{E}[Y_i(0)] = 0.
$$
Feeding the zero back into the master decomposition leaves
$$
\Delta = \text{ATT} + 0 = \text{ATT}.
$$
And since independence equally forces $\mathbb{E}[Y_i(1)\mid D_i=1] = \mathbb{E}[Y_i(1)\mid D_i=0] = \mathbb{E}[Y_i(1)]$, the treated are a representative slice, $\text{ATT}=\text{ATE}$, and so $\Delta = \text{ATE}$: the simple difference in means recovers the causal effect outright.

**(d) (6 pts)**
(i) An *unlucky* four-treated/four-control split. Put three savvy ($Y(0)=1$) and one non-savvy ($Y(0)=0$) in the treatment arm; then the control arm gets one savvy and three non-savvy:
$$
\mathbb{E}[Y_i(0)\mid D_i=1] = \frac{1+1+1+0}{4} = 0.75, \qquad
\mathbb{E}[Y_i(0)\mid D_i=0] = \frac{1+0+0+0}{4} = 0.25,
$$
$$
\text{selection bias (realized)} = 0.75 - 0.25 = 0.50 \neq 0.
$$
(The most extreme unlucky draw — all four savvy into one arm — would reproduce the $+1$ of part (a); the value here is just one illustrative imbalance.)

(ii) This leftover gap is *sampling variation*, not bias, because it averages to zero *across the randomness of assignment*: over all $\binom{8}{4}=70$ equally likely four-treated assignments, the mean selection-bias term is exactly $0$ (confirmed by exhaustive enumeration). Any single draw can deal a few extra savvy applicants to one arm, but there is no *systematic* tilt — the expected bias is zero, and as the population grows the realized imbalance shrinks toward zero (it is a precision issue, governed by standard errors, the *good* kind of problem that more data fixes). Contrast part (a): there the selection bias is $+1$ *in expectation*, baked in by the selection mechanism, so it does **not** shrink with sample size — a million self-selecting applicants reproduce the same $+1$, because the treated are systematically the savvy ones every time.

---

## Problem 6 — Why not "just control for $X$"? (16 points)

**(a) (5 pts)** Maya's hope is the **conditional independence assumption** (unconfoundedness / selection on observables):
$$
\big(Y_i(0), Y_i(1)\big) \perp\!\!\!\perp D_i \;\big|\; X_i,
$$
where $X_i = (\text{credit score, income, employment status})$. In plain English: *within each combination of credit score, income, and employment, whether a member enrolled in the round-up feature is as good as randomly assigned — unrelated to what her approval outcome would be either way.* If that holds, the selection-bias term vanishes once we compare like-with-like on $X$, and a comparison (or regression) that conditions on $X$ recovers the causal effect. It is randomization's poorer cousin: instead of a coin *guaranteeing* independence unconditionally, Maya *assumes* it holds after conditioning on the variables she happened to measure.

**(b) (6 pts)** The catch is that conditional independence is an *assumption about the unobserved*, and the data cannot verify it: it holds only if the $X$'s Maya controlled for capture *every* characteristic that drives both selection into the feature and the loan outcome. The single kind of variable that breaks it is an **unobserved confounder** — something correlated with both $D_i$ and the potential outcomes that is *not* in $X_i$ and so cannot be conditioned on. A concrete example in the round-up setting: a member's **financial conscientiousness / planning habit** (or "soft information" a loan officer perceives in person) — the disposition to budget, save, and not miss payments. Conscientious members are more likely to *opt into* an automatic-savings feature ($D_i=1$) *and* more likely to be approved regardless of the feature, yet conscientiousness appears in no column of Maya's dataset. Its presence means that *even within* fixed credit score, income, and employment, the enrollees still have a higher untreated outcome than the non-enrollees — so the conditional selection-bias term $\mathbb{E}[Y_i(0)\mid D_i=1, X_i] - \mathbb{E}[Y_i(0)\mid D_i=0, X_i]$ is *not* zero, and the "controlled" estimate stays biased, exactly as Week 2's omitted-variable bias predicted.

**(c) (5 pts)** Randomization handles the very variable that defeats controlling for $X$: the coin balances the *unobservables* too — conscientiousness, soft information, motivations Maya could never name or measure — because it severs the link between *who gets treated* and *who they are* by physical construction, requiring no assumption about which variables matter. Controlling for $X$ can only balance the variables you *thought to measure and could observe*; it is therefore a *bet* that you measured all the confounders, a bet the data cannot settle, whereas the RCT needs no such bet and so is the **gold standard**. For a researcher *forced* to make that bet because she cannot randomize, **Ch 3.2 (matching and propensity scores)** takes conditional independence as given and asks the best way to construct comparable treated-and-control groups from the observed $X$'s — matching like with like, or collapsing the $X$'s into a single propensity-to-treat score.

---

*All numerical answers verified in Python. Key results: P1 observed $Y=(45,20,52,25,53,30)$, $\tau=(10,24,12,24,8,18)$; P2 $\text{ATE}=16$, $\text{ATT}=10$, $\text{ATC}=22$; P3 $\Delta=0.24 = \text{ATT}\,0.09 + \text{selection bias}\,0.15$ with enrollees' counterfactual $\mathbb{E}[Y_i(0)\mid D_i=1]=0.61$, overstatement factor $\approx 2.7$; P5 self-selection bias $=1$, balanced-coin bias $=0$, mean bias over all $\binom{8}{4}=70$ assignments $=0$, illustrative unlucky split bias $=0.5$. P4 and P6 are conceptual (no arithmetic).*
