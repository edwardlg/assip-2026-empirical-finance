# Solutions — PS 3.3 (Entropy-Balancing Weights & AIPW by Hand)

**Linked problem set:** `book/weeks/week-03/ps3.3.md` · Week 3, Chapter 3.3.
These solutions use only Ch 3.3 tools: Horvitz–Thompson and Hájek IPW estimators, stabilized weights, the effective-sample-size diagnostic $N_{\text{eff}} = (\sum_i w_i)^2 / \sum_i w_i^2$, the entropy-balancing optimization $\min_{\{w_i\}}\sum_i w_i\log(w_i/q_i)$ with moment/normalization constraints and its closed-form $w_i\propto q_i\exp(-\sum_k\lambda_k X_{ik})$, and the AIPW / doubly-robust estimator — plus the Ch 3.1 potential-outcomes/ATT vocabulary and the Ch 3.2 propensity score $\hat e(\mathbf{X})$, CIA, and overlap. Notation follows CONVENTIONS §3. Entropy balancing is attributed to Hainmueller (2012) per the chapter. All arithmetic was verified in Python (`fractions` for exact values).

**Shared dataset (Problems 1–3):** $D=(1,1,1,0,0,0)$ for students A–F; $\hat e = (0.50,0.25,0.20,0.80,0.50,0.75)$; $Y=(7.0,8.0,9.0,10.0,9.0,8.5)$; $\hat p = 1/2$.

---

## Problem 1 — IPW, stated and read (12 pts)

**(a) [3 pts]** **Horvitz–Thompson** weights each treated outcome by $1/\hat e_i$ and each control outcome by $1/(1-\hat e_i)$ and divides each arm's weighted sum by the *fixed* sample size $N$:
$$
\hat\tau_{\text{HT}} = \frac1N\sum_i \frac{D_i Y_i}{\hat e_i} - \frac1N\sum_i \frac{(1-D_i)Y_i}{1-\hat e_i}.
$$
**Hájek** uses the *same* numerators but divides each arm by the *sum of that arm's weights* rather than by $N$ — it is self-normalizing:
$$
\hat\tau_{\text{H\'ajek}} = \frac{\sum_i D_i Y_i/\hat e_i}{\sum_i D_i/\hat e_i} - \frac{\sum_i (1-D_i)Y_i/(1-\hat e_i)}{\sum_i (1-D_i)/(1-\hat e_i)}.
$$
The one structural difference: **the denominator** — $N$ for Horvitz–Thompson, the realized total weight $\sum_i w_i$ for Hájek.

**(b) [4 pts]** The Horvitz–Thompson "treated mean," $\frac1N\sum_i D_iY_i/\hat e_i$, is a weighted sum of treated outcomes with weights $1/(N\hat e_i)$ that do *not* add up to one — in any finite sample $\frac1N\sum_i D_i/\hat e_i$ is whatever it happens to be, sometimes well above or below $1$. Multiplying outcomes by weights that sum to, say, $1.3$ inflates the average past the largest observed outcome; weights summing to $0.7$ deflate it below the smallest. So the HT mean is not a genuine weighted *average* (a convex combination) and can land outside the data range. The Hájek mean divides by exactly $\sum_i D_i/\hat e_i$, forcing the effective weights to sum to one, so it is always a convex combination of the observed treated outcomes and therefore always lies within their range.

**(c) [3 pts]** It is **true** that both are consistent (asymptotically unbiased) for the same estimand under CIA and overlap — but it is badly wrong in practice. The Horvitz–Thompson estimator has a much larger finite-sample variance because its un-normalized weights let a single small $\hat e_i$ swing the answer, and it can produce nonsensical out-of-range estimates. This is the Ch 1 lesson exactly: unbiasedness in expectation does not protect you in the one finite sample you actually have, where a high-variance estimator can be wildly off. Report Hájek.

**(d) [2 pts]** Naive difference: treated mean $\frac{7+8+9}{3} = 8.0$, control mean $\frac{10+9+8.5}{3} = 9.1\overline{6}$, difference $8.0 - 9.1\overline{6} = -1.1\overline{6} \approx -1.167$. It is not credible because enrollment was not random: enrollees and non-enrollees differ in the covariates $\mathbf{X}$ that also drive the rate, so this comparison is apples-to-oranges. The reweighting is meant to exploit the **conditional-independence assumption (CIA)** from Ch 3.2 — that once we condition on $\mathbf{X}$, treatment is as good as random — by manufacturing a pseudo-population in which $\mathbf{X}$ is balanced across arms.

---

## Problem 2 — IPW weights and the ATT, by hand (22 pts)

**(a) [5 pts]** Treated weight $1/\hat e_i$; control weight $1/(1-\hat e_i)$:

| student | $D$ | $\hat e$ | weight |
|---|---|---|---|
| A | 1 | $0.50$ | $1/0.50 = 2$ |
| B | 1 | $0.25$ | $1/0.25 = 4$ |
| C | 1 | $0.20$ | $1/0.20 = 5$ |
| D | 0 | $0.80$ | $1/0.20 = 5$ |
| E | 0 | $0.50$ | $1/0.50 = 2$ |
| F | 0 | $0.75$ | $1/0.25 = 4$ |

Treated weights sum to $2+4+5 = 11$; control weights sum to $5+2+4 = 11$. Neither sum equals $N=6$ or the arm count $3$: the inverse-probability weights add up to "however much they add up to," because nothing in the formula constrains them to a target total. This is precisely the defect that motivates Hájek's self-normalization.

**(b) [5 pts]** **Horvitz–Thompson.**
$$
\text{treated arm} = \frac1N\sum_i \frac{D_iY_i}{\hat e_i} = \frac16\big[2(7)+4(8)+5(9)\big] = \frac16(14+32+45) = \frac{91}{6} \approx 15.167,
$$
$$
\text{control arm} = \frac1N\sum_i \frac{(1-D_i)Y_i}{1-\hat e_i} = \frac16\big[5(10)+2(9)+4(8.5)\big] = \frac16(50+18+34) = \frac{102}{6} = 17.000,
$$
$$
\boxed{\hat\tau_{\text{HT}} = \tfrac{91}{6} - 17 = \tfrac{91}{6}-\tfrac{102}{6} = -\tfrac{11}{6} \approx -1.833.}
$$
Note how far off the arm "means" are from the data ($15.2$ and $17.0$ versus rates that run $7$–$10$) — the un-normalized division by $N$ has thrown both outside the observed range, exactly the pathology of Problem 1(b).

**(c) [6 pts]** **Hájek.** Same numerators, divide by the arm's weight total ($11$ each):
$$
\text{treated mean} = \frac{2(7)+4(8)+5(9)}{11} = \frac{91}{11} \approx 8.273,\qquad
\text{control mean} = \frac{5(10)+2(9)+4(8.5)}{11} = \frac{102}{11} \approx 9.273,
$$
$$
\boxed{\hat\tau_{\text{H\'ajek}} = \frac{91}{11} - \frac{102}{11} = -\frac{11}{11} = -1.000.}
$$
Both arm means now sit sensibly inside the data range. **Report the Hájek estimate, $-1.000$.** It is the self-normalizing weighted mean, far more stable, and it is what software calls "IPW"; the Horvitz–Thompson $-1.833$ is corrupted by the weights' failure to sum to a sensible total.

**(d) [3 pts]** Largest treated weight: **student C** (weight $5$, propensity $0.20$). Largest control weight: **student D** (weight $5$, propensity $0.80$). C is a *low-propensity enrollee* — the rare student who looks like a control (unlikely to enroll) but enrolled anyway; D is a *high-propensity non-enrollee* — the rare student who looks like a treated unit but didn't enroll. Each stands in for the many students like them in the *other* arm, so the estimator leans hardest on exactly these units, because they carry the information about the missing counterfactual.

**(e) [3 pts]** **Stabilized** weights: treated $\hat p/\hat e_i = 0.5/\hat e_i$, control $(1-\hat p)/(1-\hat e_i) = 0.5/(1-\hat e_i)$:

| student | $D$ | stabilized weight |
|---|---|---|
| A | 1 | $0.5/0.50 = 1.0$ |
| B | 1 | $0.5/0.25 = 2.0$ |
| C | 1 | $0.5/0.20 = 2.5$ |
| D | 0 | $0.5/0.20 = 2.5$ |
| E | 0 | $0.5/0.50 = 1.0$ |
| F | 0 | $0.5/0.25 = 2.0$ |

The Hájek ATT with stabilized weights is **still $-1.000$.** Stabilizing multiplied every treated weight by the same constant $\hat p = 1/2$ and every control weight by the same constant $1-\hat p = 1/2$; a constant common factor cancels in the self-normalizing ratio (it appears in both numerator and denominator of each arm), so the Hájek point estimate is unchanged. Stabilizing shrinks the *variance* of the weights, not the Hájek point estimate.

---

## Problem 3 — When IPW explodes, and the effective sample size (14 pts)

**(a) [4 pts]** With $\hat e_C = 0.02$, student C's weight becomes $1/0.02 = \boxed{50}$. One student would carry the weight of fifty, so the entire treated mean would be hostage to C's single outcome and to the accuracy of that one tiny estimated probability. A score of $0.02$ is a near-violation of the **overlap (common-support) assumption** from Ch 3.2, which requires $0 < e(\mathbf{X}) < 1$ for everyone: a unit whose covariates make treatment nearly impossible gets an astronomically large weight, and the estimator's variance blows up. A move from $0.20$ to $0.02$ — a plausible consequence of a small specification tweak — multiplies C's influence tenfold.

**(b) [5 pts]** Treated weights originally $(2,4,5)$, sum $11$:
$$
N_{\text{eff}} = \frac{(\sum_i w_i)^2}{\sum_i w_i^2} = \frac{11^2}{2^2+4^2+5^2} = \frac{121}{4+16+25} = \frac{121}{45} \approx 2.69 \text{ of } 3.
$$
After C explodes to $50$, weights $(2,4,50)$, sum $56$:
$$
N_{\text{eff}} = \frac{56^2}{2^2+4^2+50^2} = \frac{3136}{4+16+2500} = \frac{3136}{2520} \approx 1.24 \text{ of } 3.
$$
The effective sample size collapses from about $2.7$ to about $1.2$: the three-student treated arm is now worth barely more than a *single* observation, because one unit dominates. Most of the apparent data has been thrown away by the weighting.

**(c) [3 pts]** If all $n$ weights in an arm equal a common value $c$, then $\sum_i w_i = nc$ and $\sum_i w_i^2 = nc^2$, so
$$
N_{\text{eff}} = \frac{(nc)^2}{nc^2} = \frac{n^2 c^2}{n c^2} = n.
$$
For $w=(3,3,3,3)$: $N_{\text{eff}} = 12^2/(4\cdot 9) = 144/36 = 4$, the actual count. This is the **best case**: equal weights waste nothing, so $N_{\text{eff}}$ can never exceed the actual number of units and attains that ceiling only when every unit contributes equally. Any inequality in the weights strictly lowers $N_{\text{eff}}$.

**(d) [2 pts]** The honest conclusion: her data simply do not contain a credible counterfactual for the control arm — three units carrying half the weight means the estimate rides on a handful of observations, and no trimming fixes that. She should report the effective sample size and say so plainly, rather than present a confident-looking point estimate and standard error. This is the chapter's "quiet failure" warning: IPW throws no error and prints a clean number, so you must *look* at the weight distribution and $N_{\text{eff}}$ to catch it.

---

## Problem 4 — Entropy balancing: solve and verify (20 pts)

**(a) [3 pts]** The constraints state *what balance means* — exactly which covariate moments the reweighted controls must match — but there are far more control units than constraints, so infinitely many weight vectors satisfy them. The objective $\sum_i w_i\log(w_i/q_i)$ (the Kullback–Leibler divergence from the base weights, equivalently the negative entropy) breaks the tie by selecting, among all weight vectors that achieve exact balance, the one **closest to uniform** — the one that disturbs the data least and lets no single unit dominate. Without an objective the problem would be underdetermined; the entropy objective is what makes the solution unique and keeps the weights tame.

**(b) [6 pts]** Two controls, incomes $X_1=4$, $X_2=9$, target treated mean $\bar X^{\text{treated}}=6$. The constraints are normalization and income balance:
$$
w_1 + w_2 = 1,\qquad 4w_1 + 9w_2 = 6.
$$
Substitute $w_1 = 1-w_2$: $4(1-w_2)+9w_2 = 6 \Rightarrow 4 + 5w_2 = 6 \Rightarrow w_2 = \frac{2}{5}$, hence $w_1 = \frac35$.
$$
\boxed{w_1 = \tfrac35 = 0.600,\qquad w_2 = \tfrac25 = 0.400.}
$$
Check: $4(\tfrac35)+9(\tfrac25) = \tfrac{12}{5}+\tfrac{18}{5} = \tfrac{30}{5} = 6$. ✓ The entropy objective never enters because with **two units and two constraints** the linear system already pins the weights down uniquely — there is no remaining freedom for an objective to choose among. (Equivalently: the feasible set is a single point, so "closest to uniform" is moot.) The entropy objective only does work when units outnumber constraints.

**(c) [7 pts]** Three controls, incomes $X=(2,2,8)$, target $\bar X^{\text{treated}}=5$, claimed weights $w=(\tfrac14,\tfrac14,\tfrac12)$.

**(i)** Normalization: $\tfrac14+\tfrac14+\tfrac12 = 1$. ✓ Income balance:
$$
\sum_i w_i X_i = \tfrac14(2) + \tfrac14(2) + \tfrac12(8) = \tfrac12 + \tfrac12 + 4 = 5 = \bar X^{\text{treated}}. \checkmark
$$
Exact, to as many decimals as you like — that is the entropy-balancing guarantee.

**(ii)** The exponential form requires $w_i = \exp(-\lambda X_i)/Z$ for a single $\lambda$ and normalizer $Z$. The two students with $X=2$ both receive $\tfrac14$ — consistent, since identical $X$ must give identical $\exp(-\lambda X)$. Take logs of the two *distinct* pairs $(X,w) = (2,\tfrac14)$ and $(8,\tfrac12)$:
$$
\log\tfrac14 = -2\lambda - \log Z,\qquad \log\tfrac12 = -8\lambda - \log Z.
$$
Subtract the first from the second: $\log\tfrac12 - \log\tfrac14 = -6\lambda$, i.e. $\log 2 = -6\lambda$, so
$$
\boxed{\lambda = -\frac{\log 2}{6} \approx -0.1155.}
$$
A single $\lambda$ reproduces all three weights, so the claimed weights *do* have the required max-entropy exponential form. (Sanity check: $\lambda<0$ means weight *increases* with income, which is right — the lone high-income control at $X=8$ must be up-weighted to drag the control mean up to the treated target of $5$.)

**(iii)** Two units with identical covariates receive identical weights: max-entropy weighting treats observationally identical units symmetrically — it has no reason to favor one over the other, so it spreads weight evenly across them. (This is a direct consequence of the weights depending on the data only through $\exp(-\lambda X_i)$.)

**(d) [4 pts]** Control rates $Y=(8.0,8.0,11.0)$, weights $(\tfrac14,\tfrac14,\tfrac12)$; treated rates $(7.0,8.0)$.
$$
\text{weighted control mean} = \tfrac14(8) + \tfrac14(8) + \tfrac12(11) = 2 + 2 + 5.5 = 9.5,\qquad
\text{treated mean} = \tfrac{7+8}{2} = 7.5.
$$
$$
\boxed{\hat\tau_{\text{ATT}}^{\text{EB}} = 7.5 - 9.5 = -2.000.}
$$
The naive ATT uses the unweighted control mean $\frac{8+8+11}{3} = 9.0$, giving $7.5 - 9.0 = -1.500$. The two differ because entropy balancing **up-weights the high-income control** (the $X=8$ unit, weight $\tfrac12$ instead of $\tfrac13$) to match the treated group's higher mean income. Since that high-income control also has the highest rate ($11$), pulling it up raises the comparison mean from $9.0$ to $9.5$, widening the estimated effect from $-1.5$ to $-2.0$. Balancing income is exactly what removes the selection contamination from the contrast.

---

## Problem 5 — AIPW by hand and the double-robustness property (22 pts)

Strata $X=0$: students 1 (D=1, Y=5), 2 (D=0, Y=3), 3 (D=0, Y=1). Stratum $X=1$: students 4 (D=1, Y=10), 5 (D=1, Y=8), 6 (D=0, Y=6). $N=6$.

**(a) [4 pts]** Saturated models are stratum-by-arm means and treated fractions:
$$
\hat\mu_1(0) = 5 \ (\text{only unit 1}),\qquad \hat\mu_1(1) = \tfrac{10+8}{2} = 9,
$$
$$
\hat\mu_0(0) = \tfrac{3+1}{2} = 2,\qquad \hat\mu_0(1) = 6 \ (\text{only unit 6}),
$$
$$
\hat e(0) = \tfrac{1}{3}\ (1 \text{ of } 3 \text{ treated}),\qquad \hat e(1) = \tfrac{2}{3}\ (2 \text{ of } 3 \text{ treated}).
$$

**(b) [7 pts]** **Both models correct.** The $\hat\mu_1^{\text{DR}}$ bracket, unit by unit, with $\big[\hat\mu_1(X_i) + D_i(Y_i-\hat\mu_1(X_i))/\hat e(X_i)\big]$:

| unit | $X$ | $D$ | $\hat\mu_1(X)$ | $\hat e(X)$ | term |
|---|---|---|---|---|---|
| 1 | 0 | 1 | 5 | $1/3$ | $5 + 1\cdot(5-5)/\tfrac13 = 5$ |
| 2 | 0 | 0 | 5 | $1/3$ | $5 + 0 = 5$ |
| 3 | 0 | 0 | 5 | $1/3$ | $5 + 0 = 5$ |
| 4 | 1 | 1 | 9 | $2/3$ | $9 + 1\cdot(10-9)/\tfrac23 = 9 + 1.5 = 10.5$ |
| 5 | 1 | 1 | 9 | $2/3$ | $9 + 1\cdot(8-9)/\tfrac23 = 9 - 1.5 = 7.5$ |
| 6 | 1 | 0 | 9 | $2/3$ | $9 + 0 = 9$ |

$\hat\mu_1^{\text{DR}} = \frac16(5+5+5+10.5+7.5+9) = \frac{42}{6} = 7.0$.

The $\hat\mu_0^{\text{DR}}$ bracket, $\big[\hat\mu_0(X_i) + (1-D_i)(Y_i-\hat\mu_0(X_i))/(1-\hat e(X_i))\big]$:

| unit | $X$ | $D$ | $\hat\mu_0(X)$ | $1-\hat e(X)$ | term |
|---|---|---|---|---|---|
| 1 | 0 | 1 | 2 | $2/3$ | $2 + 0 = 2$ |
| 2 | 0 | 0 | 2 | $2/3$ | $2 + (3-2)/\tfrac23 = 2 + 1.5 = 3.5$ |
| 3 | 0 | 0 | 2 | $2/3$ | $2 + (1-2)/\tfrac23 = 2 - 1.5 = 0.5$ |
| 4 | 1 | 1 | 6 | $1/3$ | $6 + 0 = 6$ |
| 5 | 1 | 1 | 6 | $1/3$ | $6 + 0 = 6$ |
| 6 | 1 | 0 | 6 | $1/3$ | $6 + (6-6)/\tfrac13 = 6$ |

$\hat\mu_0^{\text{DR}} = \frac16(2+3.5+0.5+6+6+6) = \frac{24}{6} = 4.0$.
$$
\boxed{\hat\tau_{\text{DR}} = 7.0 - 4.0 = 3.000.}
$$

**(c) [5 pts]** **Propensity wrong ($\hat e\equiv\tfrac12$), outcome correct.** The $\hat\mu_1^{\text{DR}}$ bracket becomes $\hat\mu_1(X_i) + D_i(Y_i-\hat\mu_1(X_i))/\tfrac12$. The first parts still average to $\frac16(5+5+5+9+9+9) = 7.0$. The correction terms are $2D_i(Y_i-\hat\mu_1(X_i))$, nonzero only for treated units. Stratum $X=0$: just unit 1 with residual $5-5 = 0$. Stratum $X=1$: units 4 and 5 with residuals $10-9 = +1$ and $8-9 = -1$, which **sum to zero**. So the total treated correction is $\frac16\cdot 2\cdot(0 + 1 - 1) = 0$, leaving $\hat\mu_1^{\text{DR}} = 7.0$. The symmetric calculation gives $\hat\mu_0^{\text{DR}} = 4.0$ (control residuals within each stratum likewise sum to zero: stratum $X=0$ has $3-2=+1$ and $1-2=-1$; stratum $X=1$ has $6-6=0$). Hence
$$
\boxed{\hat\tau_{\text{DR}} = 3.000 \text{ (unchanged).}}
$$
**Why it didn't move:** with a *correct* outcome model, the residual $Y_i-\hat\mu_d(X_i)$ averages to zero *within each stratum of* $X$. So no matter what (even wrong) weights $1/\hat e(X_i)$ multiply those residuals by — as long as the weight is constant within a stratum — the weighted residuals still cancel within the stratum. The wrong propensity score is multiplied into something that vanishes, and the correct outcome model carries the estimate.

**(d) [4 pts]** **Outcome wrong ($\hat\mu_1=\hat\mu_0=5$ everywhere), propensity correct.** Now the first parts contribute a flat $5$ to each arm, and the corrections do the work. For example $\hat\mu_1^{\text{DR}} = \frac16\sum_i\big[5 + D_i(Y_i-5)/\hat e(X_i)\big]$. Computing: stratum $X=0$ treated correction from unit 1 is $(5-5)/\tfrac13 = 0$; stratum $X=1$ from units 4,5 is $(10-5)/\tfrac23 + (8-5)/\tfrac23 = 7.5 + 4.5 = 12$. So $\hat\mu_1^{\text{DR}} = \frac16(6\cdot 5 + 0 + 12) = \frac{42}{6} = 7.0$; symmetrically $\hat\mu_0^{\text{DR}} = 4.0$, giving
$$
\boxed{\hat\tau_{\text{DR}} = 3.000 \text{ (still unchanged).}}
$$
With the outcome model constant, the AIPW formula collapses (after the flat $\hat\mu$ pieces cancel between the added-in term and the correction's $-\hat\mu/\hat e$ piece) to the plain **IPW estimator** with the *correct* propensity scores — which we proved in §1.2 of the chapter is consistent. The IPW machinery carries the estimate.

**(e) [2 pts]** **Both wrong ($\hat\mu\equiv 5$, $\hat e\equiv\tfrac12$).** Then $\hat\mu_1^{\text{DR}} = \frac16\sum_i[5 + 2D_i(Y_i-5)] $. Treated outcomes are $5,10,8$, so corrections $2(0)+2(5)+2(3) = 16$, giving $\hat\mu_1^{\text{DR}} = \frac16(30+16) = \frac{46}{6} = 7.\overline{6}$; controls $3,1,6$ give $\hat\mu_0^{\text{DR}} = \frac16(30 + 2[(3-5)+(1-5)+(6-5)]) = \frac16(30 - 10) = \frac{20}{6} = 3.\overline{3}$. So $\hat\tau_{\text{DR}} = 7.\overline{6} - 3.\overline{3} = \frac{13}{3} \approx 4.333$ — which is exactly the **naive difference in means** ($\frac{5+10+8}{3} - \frac{3+1+6}{3} = \frac{23}{3} - \frac{10}{3} = \frac{13}{3}$), the biased estimator AIPW was supposed to beat. **Moral:** doubly robust means consistent if *either* model is right (parts c, d), but it guarantees nothing when *both* are wrong (part e) — one correct model is the insurance policy; zero is not.

---

## Problem 6 — Which method when? (10 pts)

**(a) [3 pts]** **AIPW / doubly-robust.** Devon wants the strongest consistency guarantee for a headline number (AIPW is consistent if *either* his propensity or his outcome model is right — two shots at the truth), he is comfortable bringing both models, and with 40 covariates and suspected non-linearity he benefits from AIPW's Neyman-orthogonality property, which lets him plug machine-learning estimators into both models with sample-splitting and still get valid inference (the double/debiased ML route, Chernozhukov et al. 2018). It is also more efficient than plain IPW when both models are even roughly right. PSM would discard units and force arbitrary caliper choices; entropy balancing would balance only the moments he names, risky when selection is high-order and non-linear.

**(b) [3 pts]** **Entropy balancing.** Priya wants *exact* balance on the means (and variances) of four covariates — entropy balancing delivers that by construction in every sample, with no post-hoc balance check that can fail (Hainmueller 2012). It keeps every uninsured farm (no discarding, unlike matching), produces tame weights, and makes her balance targets an explicit, inspectable list she can write in the paper. Crucially, it sidesteps exactly the "researcher-degrees-of-freedom" attack she fears: there is no caliper-and-algorithm menu to fish through, so a suspicious referee has far less to object to. Her one obligation is to state and defend which moments she balanced.

**(c) [2 pts]** **Propensity-score matching.** Its whole appeal for exposition is that it mimics an experiment unit by unit and is easy to explain to a non-technical audience as "we compared each treated unit to a nearly identical untreated one." For a pedagogical first pass that is ideal. The one cost he must disclose: matching **discards units** (the unmatched controls outside the caliper) and achieves only *approximate* balance that must be checked after the fact — so the matched-sample estimate rests on a subsample and a balance table, which he should report before moving to his more careful final estimator.

**(d) [2 pts]** **Report more than one method.** If PSM, entropy balancing, and AIPW all point to roughly the same effect, the finding is robust to method choice and can be written up with confidence; if they disagree, that disagreement is itself information — almost always a sign of thin overlap or a fragile specification — and belongs in the paper rather than being hidden by reporting only whichever method gave the prettiest number.

---

*End of solutions for PS 3.3.*
