# Solutions — Problem Set 3.2 (Hand-Matching, Propensity Scores, and the Limits of Selection-on-Observables)

Full worked solutions to `book/weeks/week-03/ps3.2.md`, covering Chapter 3.2. Notation follows the
Conventions: potential outcomes $Y_i(1), Y_i(0)$; treatment $D_i$; observed
$Y_i = D_i Y_i(1) + (1-D_i)Y_i(0)$; covariates $\mathbf{X}_i$; propensity score
$e(\mathbf{X}) = \Pr(D=1\mid\mathbf{X})$; estimand
$\tau_{\text{ATT}} = \mathbb{E}[Y_i(1)-Y_i(0)\mid D_i=1]$. The recurring theme of the key:
**matching is comparing like-with-like and averaging; it works only where CIA and overlap both hold;
and it is the same selection-on-observables bet as regression-with-controls — an omitted confounder
sinks it exactly the way OVB sinks OLS, and only a design (Ch 3.4) escapes.**

---

## Problem 1 — State CIA and overlap, and say what each buys (14 pts)

**(a)** [4 pts] **CIA / unconfoundedness:**
$$\{Y_i(1),\,Y_i(0)\} \perp\!\!\!\perp D_i \mid \mathbf{X}_i.$$
Plain English: *once you hold the observed covariates $\mathbf{X}_i$ fixed, whether or not an applicant
enrolled carries no further information about what their potential outcomes would have been* — within a
group of look-alikes, treatment is "as good as randomly assigned." CIA is designed to kill the
**selection-bias term** $\mathbb{E}[Y_i(0)\mid D_i=1] - \mathbb{E}[Y_i(0)\mid D_i=0]$ — the gap in the
*untreated* potential outcome between enrollees and non-enrollees. *Why it kills it:* inside a cell
$\mathbf{X}_i=\mathbf{x}$, CIA forces
$\mathbb{E}[Y_i(0)\mid D_i=1,\mathbf{x}] = \mathbb{E}[Y_i(0)\mid D_i=0,\mathbf{x}]$, so the within-cell
$Y(0)$ gap is zero and the untreated serve as a valid counterfactual for the treated.

**(b)** [4 pts] **Overlap / common support:**
$$0 < e(\mathbf{x}) = \Pr(D_i=1\mid\mathbf{X}_i=\mathbf{x}) < 1 \quad\text{for all } \mathbf{x}.$$
If at some profile $\mathbf{x}^\dagger$ *every* applicant enrolled, then $e(\mathbf{x}^\dagger)=1$, which
violates the **strict upper** inequality. Concretely, there are **no untreated units at $\mathbf{x}^\dagger$**,
so the cell quantity $\mathbb{E}[Y_i(0)\mid D_i=0,\mathbf{x}^\dagger]$ — the counterfactual for the
treated at that profile — **does not exist** (you cannot average over an empty group). The within-cell
treated-minus-untreated difference is therefore uncomputable; that region of covariate space has no
comparison and must be excluded.

**(c)** [4 pts] They buy different things.
- **CIA** makes the within-cell treated-vs-untreated difference *equal to a causal effect* — it
  guarantees the comparison, *once made*, is unconfounded (no $Y(0)$ gap inside the cell).
- **Overlap** makes that comparison *exist at all* — it guarantees both a treated and an untreated unit
  are present at each profile, so there is something to compare.

Joint condition: **strong ignorability**, the term from **Rosenbaum and Rubin (1983)**.

**(d)** [2 pts] **Overlap is partly checkable**; **CIA is fundamentally untestable.** You *can* look at
the data and see whether treated and untreated units occupy the same regions of $\mathbf{X}$ (overlap).
You *cannot* check CIA, because it is a statement about the unobserved $Y_i(0)$ of the *treated* — and by
the fundamental problem of causal inference, that half of the data is missing by construction, so no
statistic can confirm the two groups share the same $Y(0)$ distribution within cells of $\mathbf{X}$.

---

## Problem 2 — Exact matching by hand on a discrete covariate (20 pts)

Totals: $N_1 = 50+100+150 = 300$ treated, $N_0 = 150+200+100 = 450$ control, $N = 750$.

**(a)** [4 pts] **Naive difference.** Treated mean repayment:
$$\bar Y^{(1)} = \frac{50(0.40)+100(0.62)+150(0.84)}{300} = \frac{20 + 62 + 126}{300} = \frac{208}{300} = 0.6933.$$
Control mean repayment:
$$\bar Y^{(0)} = \frac{150(0.30)+200(0.50)+100(0.78)}{450} = \frac{45 + 100 + 78}{450} = \frac{223}{450} = 0.4956.$$
Naive difference $= 0.6933 - 0.4956 = \mathbf{0.1978}$ (about $19.8$ percentage points).

**(b)** [6 pts] **Within-cell effects:**
$$0.40-0.30 = +0.10,\qquad 0.62-0.50 = +0.12,\qquad 0.84-0.78 = +0.06.$$
**Exact-matching ATT** (treated-count weights):
$$\widehat\tau_{\text{ATT}} = \frac{50(0.10)+100(0.12)+150(0.06)}{300} = \frac{5 + 12 + 9}{300} = \frac{26}{300} = \mathbf{0.0867}.$$
*Why treated counts:* the ATT is the average effect *for the kind of person who actually enrolled*, so
the within-cell effects must be averaged over the covariate distribution **of the treated** —
$\frac{n^{(1)}_x}{N_1}$ is exactly the share of enrollees in cell $x$.

**(c)** [4 pts] **ATE** (total-count weights):
$$\widehat\tau_{\text{ATE}} = \frac{200(0.10)+300(0.12)+250(0.06)}{750} = \frac{20 + 36 + 15}{750} = \frac{71}{750} = \mathbf{0.0947}.$$
ATE $(0.0947) \neq$ ATT $(0.0867)$ because the **treated are concentrated in the high-baseline "2
products" cell** ($150/300 = 50\%$ of enrollees, vs. only $250/750 = 33\%$ of the full sample), and that
cell has the *smallest* within-cell effect ($+0.06$). ATT over-weights the small-effect cell relative to
ATE, so ATT comes out lower. (When the treated mix differs from the population mix *and* effects vary
across cells, ATT and ATE diverge.)

**(d)** [4 pts] **Selection bias** $=$ naive $-$ ATT $= 0.1978 - 0.0867 = \mathbf{0.1111}$. This is the
$Y(0)$ gap from Problem 1(a): here $\mathbb{E}[Y_i(0)\mid D_i=1] > \mathbb{E}[Y_i(0)\mid D_i=0]$ — the
enrollees would repay at *higher* rates even without the module. The table tells you so because
**enrollees are disproportionately in the high-prior-products cells** (where untreated repayment is also
high: $0.78$), while controls are concentrated in the low cells ($0.30$). The positive selection inflates
the naive comparison above the true ATT.

**(e)** [2 pts] The 30 "3 products" treated units have **no control in their cell**, so exact matching
**drops them** — there is no counterfactual. The reason is the **overlap / common-support** assumption:
$e(\text{3 products}) = 1$ violates the strict upper bound. Dropping them changes the *interpretation*:
the reported ATT is now the effect for *treated units who have a control twin* — the estimand has
quietly narrowed from "all enrollees" to "enrollees on common support," and Maya must say so.

---

## Problem 3 — Propensity score from a logit, then match with a caliper (22 pts)

The index is $\hat z_i = -0.4 + 0.8\,\text{credit}_i + 0.6\,\text{income}_i + 0.5\,\text{account}_i$ and
$\hat e_i = 1/(1+e^{-\hat z_i})$.

**(a)** [8 pts] Compute each index, then the score:

| Unit | credit | income | acct | $\hat z_i$ | $\hat e_i$ |
|---|---:|---:|---:|---:|---:|
| T1 | $1.0$ | $1.0$ | $1$ | $-0.4 + 0.8 + 0.6 + 0.5 = 1.50$ | $0.818$ |
| T2 | $0.5$ | $0.0$ | $0$ | $-0.4 + 0.4 = 0.00$ | $0.500$ |
| T3 | $2.5$ | $2.0$ | $1$ | $-0.4 + 2.0 + 1.2 + 0.5 = 3.30$ | $0.964$ |
| T4 | $0.0$ | $0.5$ | $1$ | $-0.4 + 0.30 + 0.5 = 0.40$ | $0.599$ |
| C1 | $1.0$ | $0.5$ | $1$ | $-0.4 + 0.8 + 0.30 + 0.5 = 1.20$ | $0.769$ |
| C2 | $0.0$ | $0.0$ | $0$ | $-0.40$ | $0.401$ |
| C3 | $-0.5$ | $-0.5$ | $0$ | $-0.4 - 0.4 - 0.30 = -1.10$ | $0.250$ |
| C4 | $0.0$ | $0.8$ | $1$ | $-0.4 + 0.48 + 0.5 = 0.58$ | $0.641$ |
| C5 | $-1.0$ | $-1.0$ | $0$ | $-0.4 - 0.8 - 0.60 = -1.80$ | $0.142$ |

(Anchors check: $\hat e(1.5)=1/(1+0.223)=0.818$; $\hat e(0)=0.5$; $\hat e(3.3)=1/(1+0.0369)=0.964$.)

**(b)** [6 pts] **Nearest-neighbor on the score, with replacement.** For each treated unit, the closest
control in $\hat e$:

| Treated ($\hat e$) | nearest control ($\hat e$) | distance $|\Delta\hat e|$ |
|---|---|---:|
| T1 ($0.818$) | C1 ($0.769$) | $0.049$ |
| T2 ($0.500$) | C2 ($0.401$) | $0.099$ |
| T3 ($0.964$) | C1 ($0.769$) | $0.196$ |
| T4 ($0.599$) | C4 ($0.641$) | $0.042$ |

(For T2 the next-closest is C4 at $|0.500-0.641|=0.141$, so C2 wins. For T3 the closest is C1 at
$0.769$; the next, C4 at $0.641$, is farther.) **C1 is reused** — it is the nearest control for *both*
T1 and T3. This is allowed *only* because matching is **with replacement**: a single control is not
"spent" after one use, so the genuinely closest control is always available, never blocked by a prior
match. (The cost — reused outcomes break independence, so naive standard errors are wrong — is flagged in
the chapter but not asked here.)

**(c)** [4 pts] **Caliper $0.10$ on the score.** Compare each distance to $0.10$:
- T1 → C1, dist $0.049 \le 0.10$ → **keep**
- T2 → C2, dist $0.099 \le 0.10$ → **keep** (just inside)
- T3 → C1, dist $0.196 > 0.10$ → **DROP**
- T4 → C4, dist $0.042 \le 0.10$ → **keep**

Surviving pairs: (T1,C1), (T2,C2), (T4,C4); $m=3$. Outcome differences:
$$Y_{T1}-Y_{C1} = 1-1 = 0,\quad Y_{T2}-Y_{C2} = 1-0 = +1,\quad Y_{T4}-Y_{C4} = 0-0 = 0.$$
$$\widehat\tau_{\text{ATT}} = \frac{0 + 1 + 0}{3} = \frac{1}{3} \approx \mathbf{0.333}.$$

**(d)** [4 pts] (i) T3 ($\hat e = 0.964$) is a *near-certain enrollee*; its closest control (C1, $0.769$)
is far away because there is essentially **no untreated unit who looked as likely to enroll** — a quiet
**overlap / common-support** violation *at the level of a single unit*. The caliper is enforcing the
overlap assumption unit-by-unit: rather than manufacture a bad comparison, it refuses the match and drops
T3. (ii) Forcing T3 → C1 ($Y_{T3}-Y_{C1} = 1-1 = 0$) and keeping all four pairs gives
$$\widehat\tau = \frac{0 + 1 + 0 + 0}{4} = \mathbf{0.25}.$$
The forced number is *less* trustworthy even though it uses more data: the T3–C1 "pair" compares a unit
with $\hat e = 0.96$ to one with $\hat e = 0.77$, which are *not* like-with-like, so the comparison
reintroduces selection bias. More data of the wrong kind degrades identification rather than improving it.

---

## Problem 4 — Balance diagnostics: standardized mean differences (16 pts)

$\text{SMD}_j = (\bar X_{j,1} - \bar X_{j,0})/s_j$, computed before and after.

**(a)** [8 pts]

| Covariate | $s_j$ | before: $(\bar X_1-\bar X_0)/s$ | SMD before | after: $(\bar X_1-\bar X_0)/s$ | SMD after |
|---|---:|---|---:|---|---:|
| credit score | $75$ | $(720-660)/75 = 60/75$ | $+0.80$ | $(702-699)/75 = 3/75$ | $+0.04$ |
| income | $30$ | $(70-58)/30 = 12/30$ | $+0.40$ | $(64-62.5)/30 = 1.5/30$ | $+0.05$ |
| debt-to-income | $0.12$ | $(0.28-0.34)/0.12 = -0.06/0.12$ | $-0.50$ | $(0.32-0.318)/0.12 = 0.002/0.12$ | $+0.017$ |
| employment tenure | $4$ | $(8-5)/4 = 3/4$ | $+0.75$ | $(7.6-6.8)/4 = 0.8/4$ | $+0.20$ |

**(b)** [3 pts] After matching, **credit ($0.04$), income ($0.05$), and debt-to-income ($0.017$) clear**
the $|\text{SMD}| < 0.1$ threshold; **employment tenure ($0.20$) does not.** The *before* column shows the
selection: enrollees were $+0.80$ SDs more creditworthy, $+0.40$ SDs higher income, $-0.50$ SDs *lower*
debt-to-income (less indebted), and $+0.75$ SDs longer-tenured — i.e., **the financially stronger, more
established applicants self-selected into the course**, which is exactly the positive selection that would
inflate a naive comparison.

**(c)** [3 pts] **Employment tenure** is still imbalanced ($0.20 > 0.1$). The fix is on the **design**:
re-specify the propensity model (e.g., add tenure with a richer functional form, or interactions), or
tighten the caliper, and re-check balance — iterating on the *specification*, not on the answer. She must
**never** select among matching recipes by watching the treatment-effect estimate; the chapter's term for
the separation she must preserve is the **firewall** between design and outcome (the matching stage uses
$D$ and $\mathbf{X}$ only; $Y$ enters once, after the design is frozen). Tuning the recipe while watching
the effect is the specification-search / multiple-testing pathology of Chapter 1.5 aimed at the causal
conclusion.

**(d)** [2 pts] A t-test is the **wrong** balance diagnostic because it conflates the *size* of the
imbalance with the *sample size*: matching drops units and shrinks $N$, so a "significant" pre-match
imbalance can turn "insignificant" purely from the smaller sample, with no real improvement in
comparability. The SMD measures the imbalance itself (in SD units), not whether it clears a noise
threshold.

---

## Problem 5 — Off-support units and whose effect you are estimating (12 pts)

**(a)** [4 pts] "Every applicant above 800 enrolled" means $e(\mathbf{x}) = 1$ for those profiles —
violating the **strict upper bound** of $0 < e(\mathbf{x}) < 1$; there is **no usable control** in that
region (treated units exist, counterfactuals do not). "No applicant below 560 enrolled" means
$e(\mathbf{x}) = 0$ there — violating the **strict lower bound**; there is **no treated unit at all** in
that region (so nothing to estimate an effect *on*).

**(b)** [4 pts] The **region of common support** is the band of credit scores (roughly 560–800) where
*both* enrollees and non-enrollees exist. A caliper-matching procedure does not crash on the above-800
treated units: their nearest control is far away on the score, the distance exceeds the caliper, and they
are **dropped** (exactly as T3 was in Problem 3). Consequence: after dropping them, Maya estimates the
ATT **only for treated units on common support** — the effect for enrollees with a credit score in the
overlap band. The estimand has quietly changed from "ATT for all enrollees" to "ATT for enrollees who
have a comparable non-enrollee," which excludes the very-highest-score group.

**(c)** [2 pts] **Matching-with-a-caliper enforces overlap explicitly and refuses to extrapolate**, while
a regression would happily extend a fitted line into the above-800 region where there are *no controls
at all*, silently inventing counterfactuals from functional form. Matching makes the common-support
problem *visible* (units get dropped) instead of papering over it (Section 3.2.8, advantage 2).

**(d)** [2 pts] The unqualified ATT is misleading because it implies an effect for *all* enrollees when
it is really the effect for the $86\%$ on common support — the dropped $14\%$ (the highest-score
enrollees) may have a different effect, and the reader cannot tell the estimand changed. The line to add:
*"The estimate is the ATT on the region of common support; $14\%$ of treated units were off-support
(near-certain enrollees with no comparable control) and are excluded, so the effect does not speak to
them."*

---

## Problem 6 — Matching is still selection-on-observables: CIA failure as OVB (16 pts)

**(a)** [4 pts] The balance table reports SMDs **only on the covariates Maya measured** — credit,
income, age. Balance on those three says *nothing* about motivation because motivation is **not in the
table**: a balancing score balances the variables that entered it, and is *helpless* about variables it
never saw. This is exactly why **CIA is untestable**. The test would require comparing the *treated*
units' $Y_i(0)$ — their approval *had they not enrolled* — against the matched controls' outcomes within
cells; but $Y_i(0)$ for a treated unit is unobserved by the **fundamental problem of causal inference**.
Half the distribution the test needs is missing by construction, so no balance table (on observables or
otherwise) can confirm the treated and control share the same $Y(0)$ once you condition on $\mathbf{X}$.

**(b)** [5 pts] Motivation is the omitted variable $z$; bias $= \beta_2\,\delta_1$.
(i) $\beta_2 > 0$ — more motivated applicants clean up their applications and are approved more often, so
motivation raises approval.
(ii) $\delta_1 > 0$ — more motivated applicants are *more* likely to seek out and complete the free
course, so motivation is positively associated with enrollment.
(iii) Two-sign rule: bias $= (+)(+) = +$, **biased upward.** Maya's matched estimate **overstates** the
course's true effect — the matched enrollees are more motivated than their matched non-enrollee twins,
and that extra motivation independently raises approval, loading onto the course coefficient. (Her
"$31$ pp" is too big.)

**(c)** [4 pts] **Bottom line:** matching and regression-with-controls both rest on CIA — "treatment is
as good as random given $\mathbf{X}$" — so a confounder omitted from $\mathbf{X}$ kills *both* identically,
and matching buys no relief from that requirement. Any **two** of the three honest advantages
(Section 3.2.8):
- **Nonparametric in the outcome.** Matching never models $Y$ as a function of $\mathbf{X}$, so it cannot
  be fooled by the wrong functional form. *Does not weaken CIA:* getting the outcome shape right is a
  different issue from having measured all confounders — you still need $\mathbf{X}$ to contain them.
- **Enforces overlap explicitly.** A caliper refuses comparisons with no real neighbor, where regression
  silently extrapolates. *Does not weaken CIA:* refusing off-support comparisons protects the *overlap*
  assumption, not CIA — an unobserved confounder biases the on-support comparisons just the same.
- **Separates design from outcome.** The matching stage touches only $D$ and $\mathbf{X}$, structurally
  preventing specification-search on the answer. *Does not weaken CIA:* a clean firewall guards against
  *p*-hacking, not against an *omitted* confounder that no amount of honest tuning can reveal.

**(d)** [3 pts] The escape is a **design-based / quasi-experimental design that does not require observing
the confounder** — specifically an **instrumental variable** (an instrument for enrollment), developed in
**Chapter 3.4** (also natural experiments / discontinuities in eligibility, Week 4). What such a design
must *supply* that selection-on-observables assumes away: a source of **exogenous variation in treatment**
— a variable that shifts enrollment for reasons unrelated to motivation (and to approval except through
enrollment) — so the effect can be read off that clean variation rather than from a conditional-on-observables
comparison that the unobserved motivation contaminates.

---

*End of solutions for PS 3.2. Every numerical answer above is reproducible by hand from the supplied
inputs, and Problems 2–4 are checkable in `nb3.2-psm-balance-diagnostics.ipynb`. The through-line: CIA +
overlap license "compare like-with-like, then average," but CIA is untestable and is precisely the
no-omitted-confounder condition of Chapter 2.5 in potential-outcomes dress — when it fails, the cure is a
design (Chapter 3.4), not a fancier estimator.*
