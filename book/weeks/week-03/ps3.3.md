# PS 3.3 — Entropy-Balancing Weights & AIPW by Hand

**Course:** 8-Week Empirical Finance Camp · Week 3 · Problem Set 3.3
**Covers:** Ch 3.3 (inverse-probability weighting — Horvitz–Thompson vs. Hájek/stabilized; the extreme-weight explosion and the trimming/stabilizing defenses; effective sample size; entropy balancing as a max-entropy optimization with moment constraints and its exponential-form solution; augmented IPW / doubly-robust estimation and the double-robustness property; choosing among PSM, entropy balancing, and AIPW). Leans on Ch 3.1 (potential outcomes, ATT/ATE, the missing-counterfactual framing) and Ch 3.2 (propensity score $e(\mathbf{X})$, CIA, overlap, balance) for vocabulary.
**Total:** 100 points across 6 problems. Problems escalate; each is self-contained, but Problems 1–3 share one dataset and you will reuse its weights.

**Ground rules.** Use only tools through Chapter 3.3. You may take estimated propensity scores $\hat e(\mathbf{X}_i)$ as *given* — do not re-estimate a logit (that was Ch 3.2). The estimators you may use are: the Horvitz–Thompson IPW estimator, the Hájek (self-normalizing) IPW estimator, stabilized weights $\hat p/\hat e$ and $(1-\hat p)/(1-\hat e)$, the effective-sample-size formula $\big(\sum_i w_i\big)^2/\sum_i w_i^2$, the entropy-balancing optimization $\min_{\{w_i\}} \sum_i w_i \log(w_i/q_i)$ subject to moment and normalization constraints (with its closed-form solution $w_i \propto q_i \exp(-\sum_k \lambda_k X_{ik})$), and the AIPW / doubly-robust estimator. No standard-error or asymptotic-variance machinery beyond the effective-sample-size diagnostic. No instruments (that is Ch 3.4). Show every step; a bare number earns little. Work in exact fractions where you can, then give a decimal to three places.

Throughout, follow CONVENTIONS §3 notation: $D_i \in \{0,1\}$ is treatment, $Y_i$ the observed outcome, $\mathbf{X}_i$ the covariates, $e(\mathbf{X}_i)=\Pr(D_i=1\mid\mathbf{X}_i)$ the propensity score, $w_i$ a unit's weight, $\hat\tau_{\text{ATT}}$ and $\hat\tau_{\text{ATE}}$ the target effects, and $\hat\mu_d(\mathbf{X})=\hat{\mathbb{E}}[Y\mid\mathbf{X},D=d]$ the outcome-model predictions. Cite Hainmueller (2012) by name where the problem asks for the source of entropy balancing.

---

## The shared dataset (Problems 1–3)

Maya extends her financial-literacy study from the chapter. Six students: three enrolled in the program ($D=1$) and three did not ($D=0$). The outcome $Y$ is the interest rate (in percentage points) on each student's first installment loan, and $\hat e$ is the estimated propensity score (probability of enrolling) carried over from her Ch 3.2 logit. Lower $Y$ is better.

| student $i$ | $D_i$ | $\hat e(\mathbf{X}_i)$ | $Y_i$ (rate) |
|---|---|---|---|
| A | 1 | $0.50$ | $7.0$ |
| B | 1 | $0.25$ | $8.0$ |
| C | 1 | $0.20$ | $9.0$ |
| D | 0 | $0.80$ | $10.0$ |
| E | 0 | $0.50$ | $9.0$ |
| F | 0 | $0.75$ | $8.5$ |

The overall enrollment share is $\hat p = \Pr(D=1) = 3/6 = 1/2$.

---

## Problem 1 — IPW, stated and read (12 points)

This problem checks that you can say what the two IPW estimators are and why one of them is the one you actually run.

**(a) [3 pts]** State, in one careful sentence each, the **Horvitz–Thompson** IPW estimator and the **Hájek** IPW estimator for the average treatment effect, writing both formulas. Your sentences must make explicit the *one structural difference* between them: what sits in the denominator of each arm.

**(b) [4 pts]** Explain why the Horvitz–Thompson estimator can return a "treated mean" that lies *outside* the range of the observed treated outcomes, while the Hájek estimator never can. Frame your answer around the fact that the inverse-probability weights $1/\hat e(\mathbf{X}_i)$ do not, in a finite sample, sum to $N$. (One short paragraph.)

**(c) [3 pts]** A classmate says: "The two estimators are both unbiased for the same thing, so it doesn't matter which I use." State whether this is true, and explain in one or two sentences the sense in which it is right *and* the practical sense in which it is badly wrong — connect your answer to the Ch 1 lesson that an estimator can be unbiased in expectation yet a poor choice in finite samples.

**(d) [2 pts]** Compute the *unweighted* (naive) difference in mean rates, treated minus control, from the shared dataset. State in one sentence why this number is not a credible causal estimate here, naming the assumption from Ch 3.2 that the IPW reweighting is meant to exploit.

---

## Problem 2 — IPW weights and the ATT, by hand (22 points)

Work entirely from the shared dataset. Maya wants the effect of enrolling. We will build the weights, compute both IPW estimators, and then watch one weight explode.

**(a) [5 pts]** **Build the weights.** For each student, compute the unstabilized inverse-probability weight: $1/\hat e_i$ for the treated, $1/(1-\hat e_i)$ for the controls. Tabulate all six. Then report the sum of the treated weights and the sum of the control weights, and note in one sentence why neither sum equals $N=6$ (nor equals $3$).

**(b) [5 pts]** **Horvitz–Thompson.** Compute $\hat\tau_{\text{HT}} = \frac{1}{N}\sum_i \frac{D_i Y_i}{\hat e_i} - \frac{1}{N}\sum_i \frac{(1-D_i)Y_i}{1-\hat e_i}$ for the shared dataset, showing the two arm-terms separately. Report to three decimals.

**(c) [6 pts]** **Hájek.** Compute the Hájek estimate by forming the self-normalizing weighted mean in each arm (weighted sum of outcomes divided by the sum of weights *in that arm*). Report the treated weighted mean, the control weighted mean, and their difference as exact fractions and decimals. State which of the two estimators — your part (b) or part (c) answer — you would report, and why.

**(d) [3 pts]** **The weights tell a story.** Identify which single treated student carries the largest weight and which single control student carries the largest weight, and explain in one or two sentences *why those particular units* get up-weighted — what role does a low-propensity enrollee (or a high-propensity non-enrollee) play in recovering the missing counterfactual?

**(e) [3 pts]** **Stabilize.** Recompute all six weights as *stabilized* weights — treated get $\hat p/\hat e_i$, controls get $(1-\hat p)/(1-\hat e_i)$, with $\hat p = 1/2$. Tabulate them, and then state what the Hájek ATT becomes when you use the stabilized weights instead of the raw ones. Explain in one sentence why the Hájek point estimate is *unchanged* even though every weight shrank.

---

## Problem 3 — When IPW explodes, and the effective sample size (14 points)

Still the shared dataset, now stress-tested.

**(a) [4 pts]** **The explosion.** Suppose Maya re-runs her propensity logit with one extra interaction term, and student C's estimated score drops from $\hat e_C = 0.20$ to $\hat e_C = 0.02$ (the other five scores are unchanged). Compute C's new unstabilized weight. Then explain in two or three sentences why this single re-estimated probability should make Maya nervous about her IPW point estimate — name the assumption from Ch 3.2 that a near-zero propensity score signals is in trouble.

**(b) [5 pts]** **Effective sample size.** The effective sample size of a weighted arm is $N_{\text{eff}} = \big(\sum_i w_i\big)^2 / \sum_i w_i^2$. Using the *unstabilized treated weights* from Problem 2(a) (the original $\hat e_C = 0.20$ case), compute $N_{\text{eff}}$ for the three treated students. Then recompute $N_{\text{eff}}$ for the treated arm *after* C's weight explodes to the part-(a) value (B and A unchanged). Report both as decimals to two places, and say in one sentence what the drop means in plain English.

**(c) [3 pts]** Show that if every weight in an arm is *equal*, then $N_{\text{eff}}$ equals the actual number of units in that arm. (A short algebraic argument with the formula; you may illustrate with the four equal weights $w=(3,3,3,3)$.) State in one sentence what this tells you about the *best case* for the effective sample size.

**(d) [2 pts]** Maya's full study has 600 students but an effective sample size of 40 in the control arm because three units carry half the weight. Trimming the most extreme score barely changes this. State, in one or two sentences, the honest conclusion she should draw and report — and connect it to the chapter's warning that the IPW failure mode is "quiet."

---

## Problem 4 — Entropy balancing: solve and verify (20 points)

Now leave IPW behind and solve directly for balancing weights, the way Hainmueller (2012) proposed. We target the **ATT**, so we reweight the **control** units to match the treated group's covariate moments, then keep every treated unit at weight one.

Throughout this problem, write the entropy-balancing program for control weights $\{w_i\}$ as
$$
\min_{\{w_i\}} \; \sum_{i \in \text{control}} w_i \log\frac{w_i}{q_i}
\quad\text{s.t.}\quad
\sum_{i} w_i = 1,\quad w_i \ge 0,\quad \sum_{i} w_i X_{ik} = \bar X_k^{\text{treated}}\ \ (\text{each balanced moment } k),
$$
with uniform base weights $q_i = 1/N_c$, and recall the closed-form solution $w_i \propto q_i \exp\!\big(-\sum_k \lambda_k X_{ik}\big)$.

**(a) [3 pts]** Explain, in two or three sentences, the role of the objective $\sum_i w_i \log(w_i/q_i)$ versus the role of the constraints. Why does the problem *need* an objective at all — i.e., why isn't the balance constraint enough to pin down the weights on its own? Use the phrase "closest to uniform."

**(b) [6 pts]** **Solve the two-control case.** A miniature version: Maya's treated group has mean income $\bar X^{\text{treated}} = 6$ (in \$10{,}000s). She has just *two* control students, with incomes $X_1 = 4$ and $X_2 = 9$. Set up the two equations the weights $w_1, w_2$ must satisfy (the income-balance constraint and normalization), solve them, and report $w_1, w_2$ as exact fractions. Then explain in one sentence why, in this particular case, the *entropy objective never enters the calculation* — what is special about having two units and two constraints?

**(c) [7 pts]** **Verify a three-control solution.** Now Maya has *three* control students with incomes $X = (2, 2, 8)$, and the treated mean income is again $\bar X^{\text{treated}} = 5$. A classmate claims the entropy-balancing weights are $w = \left(\tfrac14, \tfrac14, \tfrac12\right)$.
  - (i) Verify these weights satisfy normalization and *exactly* balance the income mean to $5$.
  - (ii) Confirm they have the required exponential form $w_i \propto \exp(-\lambda X_i)$ by finding a single $\lambda$ consistent with all three weights. (Hint: take logs; two students share an income, so they must share a weight — check that they do, then solve for $\lambda$ from the two *distinct* $(X_i, w_i)$ pairs. You may leave $\lambda$ in terms of $\log 2$.)
  - (iii) State in one sentence what the fact that the two students with the same income receive the same weight tells you about how max-entropy weighting treats identical units.

**(d) [4 pts]** **The entropy-balanced ATT.** Using the three control students from part (c) with the verified weights $w=(\tfrac14,\tfrac14,\tfrac12)$, suppose their loan rates are $Y = (8.0, 8.0, 11.0)$ and the two treated students have rates $(7.0, 8.0)$. Compute the entropy-balanced ATT: the (unweighted) treated mean rate minus the weighted control mean rate. Then compute the *naive* ATT that uses the unweighted control mean, and explain in one or two sentences why the two differ — which control unit got up-weighted, and why balancing income changed the answer.

---

## Problem 5 — AIPW by hand and the double-robustness property (22 points)

This is the centerpiece. You will compute the augmented-IPW (doubly-robust) estimator by hand, then deliberately break one model at a time and watch it survive.

The data: six students, one binary covariate $X \in \{0,1\}$ (say, $X=1$ flags "household income above median"). Three students have $X=0$, three have $X=1$.

| student $i$ | $X_i$ | $D_i$ | $Y_i$ |
|---|---|---|---|
| 1 | 0 | 1 | $5.0$ |
| 2 | 0 | 0 | $3.0$ |
| 3 | 0 | 0 | $1.0$ |
| 4 | 1 | 1 | $10.0$ |
| 5 | 1 | 1 | $8.0$ |
| 6 | 1 | 0 | $6.0$ |

The AIPW estimator for each arm is
$$
\hat\mu_1^{\text{DR}} = \frac1N \sum_i \Big[\hat\mu_1(X_i) + \frac{D_i\,(Y_i-\hat\mu_1(X_i))}{\hat e(X_i)}\Big],\qquad
\hat\mu_0^{\text{DR}} = \frac1N \sum_i \Big[\hat\mu_0(X_i) + \frac{(1-D_i)\,(Y_i-\hat\mu_0(X_i))}{1-\hat e(X_i)}\Big],
$$
with $\hat\tau_{\text{DR}} = \hat\mu_1^{\text{DR}} - \hat\mu_0^{\text{DR}}$ and $N=6$.

**(a) [4 pts]** **Build the "correct" models from the strata.** Because $X$ is binary, the *saturated* outcome model just predicts each stratum's by-arm mean, and the *saturated* propensity model just predicts each stratum's treated fraction. Compute, showing your work:
  - $\hat\mu_1(0), \hat\mu_1(1)$ — the mean outcome among treated, in each stratum;
  - $\hat\mu_0(0), \hat\mu_0(1)$ — the mean outcome among controls, in each stratum;
  - $\hat e(0), \hat e(1)$ — the fraction treated, in each stratum (as fractions).

**(b) [7 pts]** **Compute the doubly-robust ATE with both models correct.** Using the models from part (a), evaluate the six-term bracket for $\hat\mu_1^{\text{DR}}$ and the six-term bracket for $\hat\mu_0^{\text{DR}}$, showing each unit's contribution. Report $\hat\mu_1^{\text{DR}}$, $\hat\mu_0^{\text{DR}}$, and $\hat\tau_{\text{DR}}$. (You should get a clean integer ATE.)

**(c) [5 pts]** **Break the propensity model; keep the outcome model.** Replace the propensity scores with the *wrong* flat value $\hat e(0)=\hat e(1)=\tfrac12$, but keep the correct outcome model from (a). Recompute $\hat\tau_{\text{DR}}$. Then explain — using the within-stratum residuals $Y_i - \hat\mu_1(X_i)$ for the treated and $Y_i - \hat\mu_0(X_i)$ for the controls — *why* the answer did not move. (Hint: compute the sum of the treated residuals within each stratum.)

**(d) [4 pts]** **Break the outcome model; keep the propensity model.** Now use a deliberately wrong, flat outcome model $\hat\mu_1(X)=\hat\mu_0(X)=5$ for all $X$, but restore the correct propensity scores from (a). Recompute $\hat\tau_{\text{DR}}$. Verify it still equals your part-(b) answer, and explain in one or two sentences which estimator the AIPW formula collapses to in this case, and why that estimator was already consistent.

**(e) [2 pts]** **Break both.** Finally, use both wrong models at once — flat $\hat\mu = 5$ everywhere *and* flat $\hat e = \tfrac12$ everywhere — and compute $\hat\tau_{\text{DR}}$. State what familiar (biased) estimator it collapses to, and write the one-sentence moral of parts (b)–(e) about what "doubly robust" does and does not promise.

---

## Problem 6 — Which method when? (10 points)

A short decision problem. For each scenario below, name the *single* method you would lead with — **propensity-score matching (Ch 3.2)**, **entropy balancing**, or **AIPW / doubly-robust** — and defend the choice in two or three sentences that a referee would accept. Tie each answer to the specific strength or weakness of the method at issue (balance guarantee, weight stability, unit retention, specification angst, double-robustness, efficiency, ML extensibility). There is a defensible best answer in each case.

**(a) [3 pts]** Devon studies whether adopting a particular DeFi lending protocol changed a crypto wallet's borrowing cost. He has 40 covariates (on-chain activity metrics), suspects the selection mechanism is highly non-linear, wants the strongest possible consistency guarantee for a *headline* number he intends to publish, and is comfortable fitting two models. Which method, and why?

**(b) [3 pts]** Priya has a clean four-covariate climate-insurance study, a modest sample, and a referee who is famously suspicious of "researcher degrees of freedom" — she has been burned before by reviewers accusing her of fishing across caliper choices. She wants *exact* balance on the means (and maybe variances) of her four covariates, wants to keep all her uninsured farms, and wants a method whose balance targets she can write down explicitly in the paper. Which method, and why?

**(c) [2 pts]** Sam is writing the *exposition* section of a paper for a non-technical audience and wants to first convey the idea of "comparing each treated unit to a nearly identical untreated one," before reporting his more careful final estimate. For this *pedagogical first pass*, which method, and why — and what is the one cost he must disclose when he uses it?

**(d) [2 pts]** State the chapter's meta-advice in one sentence: what should all three of these researchers ultimately do with *more than one* method, and what does it mean for their finding if the methods disagree?

---

*Solutions: see `book/appendices/E-solutions-manual/E-w3-ps3.3-solutions.md`.*
