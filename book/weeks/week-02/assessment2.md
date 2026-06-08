# Week 2 Assessment — The OLS Engine

This is the end-of-week assessment for Week 2. It has three parts. **Part A** is a derive-and-interpret
section on the spine of the week — OLS in matrix form and the normal equations, the hat and residual-maker
matrices, Gauss–Markov and what "BLUE" actually buys you, Frisch–Waugh–Lovell and partialling-out, robust
and clustered standard errors, and omitted-variable bias and attenuation. **Part B** is a small panel you
simulate, estimate, and report on, ending with the single most important habit of the week: choosing the
right standard error and reading what changes. **Part C** is the rubric, with explicit point totals. An
instructor answer key follows Part C.

The whole thing is one focused sitting plus the coding task. Methods are limited to Week 2: matrix OLS,
the four/five classical assumptions, FWL, the sandwich (HC and clustered), HAC by name, and the OVB and
measurement-error formulas. No instrumental variables, no panel fixed-effects estimators beyond the
within-transformation idea, no causal-design machinery — those are Weeks 3–4. Show your reasoning. A
correct number with no argument earns little; an honest "this is an SE problem, not a bias problem, and
here is how I know" earns a great deal.

**Total: 100 points.** Part A = 48, Part B = 42, Presentation/honesty woven through both = 10.

Throughout, write OLS as $\mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\varepsilon}$ with
$\hat{\boldsymbol{\beta}} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$, and label every standard
error with its flavor: classical, HC1/HC2/HC3, HAC (Newey–West), or clustered.

---

## Part A — Derive and interpret (48 points; 8 points each)

Answer in a few lines of algebra plus two to four sentences of interpretation. Where a derivation is
asked for, the steps must be visible; a boxed final formula with no path earns half credit at most.

**A1. (Normal equations from two directions.)** Start from the sum-of-squared-residuals objective
$S(\mathbf{b}) = (\mathbf{y}-\mathbf{X}\mathbf{b})'(\mathbf{y}-\mathbf{X}\mathbf{b})$. (i) Differentiate
with respect to $\mathbf{b}$ and set the gradient to zero to derive the normal equations
$\mathbf{X}'\mathbf{X}\hat{\boldsymbol{\beta}} = \mathbf{X}'\mathbf{y}$, and state the one condition on
$\mathbf{X}$ that lets you write $\hat{\boldsymbol{\beta}} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$.
(ii) Now derive the *same* equations from orthogonality alone — without calculus — using the geometric
fact that the residual vector $\hat{\boldsymbol{\varepsilon}}$ must be orthogonal to the column space of
$\mathbf{X}$. State in one sentence why, when $\mathbf{X}$ contains a column of ones, this forces the
residuals to sum to zero.

**A2. (The hat matrix is a projector.)** Define $\mathbf{H} = \mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'$
and $\mathbf{M} = \mathbf{I} - \mathbf{H}$. (i) Prove $\mathbf{H}$ is symmetric and idempotent
($\mathbf{H}\mathbf{H}=\mathbf{H}$), and show $\mathbf{H}\mathbf{X} = \mathbf{X}$. (ii) Using
$\hat{\boldsymbol{\varepsilon}} = \mathbf{M}\mathbf{y}$ and the Pythagorean split
$\lVert\mathbf{y}\rVert^2 = \lVert\hat{\mathbf{y}}\rVert^2 + \lVert\hat{\boldsymbol{\varepsilon}}\rVert^2$,
explain in words what the diagonal entry $h_{ii}$ measures and why an observation with $h_{ii}$ close to 1
is one a careful analyst worries about. (You do not need to re-derive the Pythagorean split.)

**A3. (Gauss–Markov and the meaning of "best.")** State the classical assumptions under which OLS is BLUE,
decoding what each of the four letters B-L-U-E claims. Then consider a rival linear estimator
$\tilde{\boldsymbol{\beta}} = \mathbf{C}\mathbf{y}$ with $\mathbf{C} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}' + \mathbf{D}$.
Show that requiring $\tilde{\boldsymbol{\beta}}$ to be unbiased for *every* $\boldsymbol{\beta}$ forces
$\mathbf{D}\mathbf{X} = \mathbf{0}$, and state (you need not fully expand the algebra) why this makes
$\operatorname{Var}(\tilde{\boldsymbol{\beta}}) = \operatorname{Var}(\hat{\boldsymbol{\beta}}) + \sigma^2\mathbf{D}\mathbf{D}'$,
a sum of the OLS variance and something positive-semidefinite. Finish with one sentence: which single
classical assumption, when it breaks, is the one that *demotes* OLS from "best" — and does its breaking
make $\hat{\boldsymbol{\beta}}$ biased?

**A4. (FWL / partialling-out — and "is this a bias problem or an SE problem?")** Leah runs the long
regression of patent count $y$ on R&D spending $x$ and firm size $z$ (plus an intercept), and gets
$\hat\beta_1 = 1.84$ on R&D. State the Frisch–Waugh–Lovell theorem precisely enough to describe the
two-step recipe that reproduces $\hat\beta_1$ exactly: which two auxiliary regressions you run, and what
final regression you run on their residuals. Then answer this: Leah notices R&D and firm size are highly
correlated in her sample. A colleague says "high correlation between your regressors *biases* your R&D
coefficient." **Is this a bias problem or a standard-error problem?** Defend your answer in two sentences
using FWL geometry (what near-collinearity does to the residualized regressor $\tilde{x}$).

**A5. (Robust vs. clustered SEs — name the threat and the fix.)** Maya regresses loan APR on a borrower
characteristic across $N = 9{,}000$ loans that come from $G = 9$ lenders, 1,000 loans each. The within-lender
errors are positively correlated because each lender sets rates with a correlated house style. (i) Write
the general sandwich form of $\widehat{\operatorname{Var}}(\hat{\boldsymbol{\beta}})$ and say in one sentence
how the *clustered* version builds its middle differently from the *HC* (heteroskedasticity-robust) version.
(ii) Using the Moulton-style approximation
$\text{true Var} \approx \text{naive Var}\times[\,1+(n-1)\rho_x\rho_\varepsilon\,]$, with cluster size
$n=1{,}000$ and a mild $\rho_x\rho_\varepsilon = 0.05$, compute the factor by which the classical SE
understates the truth (give the variance inflation and the SE inflation). (iii) **Name the threat and the
design/fix in one sentence**, in the spec-discipline format: state what level you cluster at and what
economic claim that choice encodes — and note the one thing about $G = 9$ that should make Maya nervous.

**A6. (OVB and attenuation — two contaminations, two directions.)** (i) Derive the omitted-variable-bias
formula: with true long model $y = \beta_0 + \beta_1 x + \beta_2 z + \varepsilon$ (assumptions holding in
the long model) but a short regression of $y$ on $x$ alone, show
$\hat{\tilde\beta}_1 \xrightarrow{p} \beta_1 + \beta_2\delta_1$ where $\delta_1 = \operatorname{Cov}(x,z)/\operatorname{Var}(x)$.
Then apply the two-sign rule to Maya's case: the omitted variable is creditworthiness $C$, which raises
approval ($\beta_2 > 0$) and is *lower* on average for the disadvantaged group $D=1$ so that the slope of
$C$ on $D$ is negative ($\delta_1 < 0$) — state the sign of the bias on the $D$ coefficient and what it
does to the apparent approval penalty. (ii) Now a *different* contamination: Maya's income variable is
self-reported, $x = x^\* + m$ with classical noise $m$. State the attenuation formula
$\hat\beta_1 \xrightarrow{p} \beta_1\lambda$, define the reliability ratio $\lambda$, and say which way the
income coefficient is pushed. Close with one sentence contrasting OVB and attenuation: which one has a
*known* direction regardless of the data, and why.

---

## Part B — Simulate a clustered panel, estimate β̂ from scratch, and choose the SE (42 points)

You will build a small panel where you control the truth, estimate $\hat\beta$ by hand from the matrix
formula, and then compute classical, HC1, and clustered standard errors for the *same* point estimate.
The headline you are chasing is the one from Ch 2.4: clustering does not move $\hat\beta$ — it moves the
*t*-statistic, sometimes by a lot, and that change is the whole story. This ties Ch 2.1 (the matrix
estimator), Ch 2.2 (unbiasedness under the right assumptions), and Ch 2.4 (the sandwich) together in one
script.

### The data-generating process

Simulate a balanced panel of $G$ lenders, each with $n$ loans, so $N = G n$. For lender $g$ and loan $i$:

$$
y_{ig} = \beta_0 + \beta_1 x_{ig} + \underbrace{a_g + e_{ig}}_{\varepsilon_{ig}},
\qquad a_g \sim \mathcal{N}(0,\sigma_a^2),\quad e_{ig}\sim\mathcal{N}(0,\sigma_e^2).
$$

The term $a_g$ is a **lender-level shock shared by every loan at that lender** — it is what induces
within-cluster error correlation. Make the regressor *also* carry a lender component so that $\rho_x > 0$:
draw $x_{ig} = c_g + v_{ig}$ with $c_g\sim\mathcal{N}(0,1)$ and $v_{ig}\sim\mathcal{N}(0,1)$. Use a true
slope $\beta_1 = 0.30$, $\beta_0 = 1.0$, $\sigma_a = 1.0$, $\sigma_e = 1.0$. Pin your random seed and state it.

### Tasks

**B1. Estimate β̂ from scratch (10 pts).** With $G = 40$ and $n = 50$ ($N = 2{,}000$), build the design
matrix $\mathbf{X}$ (a column of ones and the $x$ column) and compute
$\hat{\boldsymbol{\beta}} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$ using only array operations
(`numpy`), *not* a regression library. Report $\hat\beta_1$ and confirm it is close to $0.30$. Verify two
Ch 2.1 identities numerically: the residuals sum to (essentially) zero, and they are orthogonal to the
$x$ column ($\mathbf{X}'\hat{\boldsymbol{\varepsilon}} \approx \mathbf{0}$).

**B2. Three standard errors for one β̂ (14 pts).** For that same $\hat{\boldsymbol{\beta}}$, compute three
standard errors on $\hat\beta_1$:

- **classical**, $\hat\sigma^2(\mathbf{X}'\mathbf{X})^{-1}$ with $\hat\sigma^2 = \hat{\boldsymbol{\varepsilon}}'\hat{\boldsymbol{\varepsilon}}/(N-K)$;
- **HC1**, the heteroskedasticity-robust sandwich with the usual $N/(N-K)$ correction;
- **clustered by lender**, the block sandwich summing the outer products over the $G$ lenders.

You may write these from the matrix formulas (preferred) or use `statsmodels` for HC1 and the clustered
SE *as a check* — but the clustered computation should match a from-scratch block sum to a few decimals.
Report all three SEs and the three implied *t*-statistics for $H_0:\beta_1 = 0$ in a small table.

**B3. Read the t-stat change (12 pts).** In one short paragraph answer: Which SE is largest, and why is
that the *honest* one here? By roughly what factor does the clustered SE exceed the classical SE, and how
does that compare to what the Moulton approximation
$\sqrt{1+(n-1)\rho_x\rho_\varepsilon}$ would predict for your DGP? State explicitly: did $\hat\beta_1$
itself change across the three SE flavors? Conclude with the one-sentence verdict the week is built
around — **bias problem or SE problem?** — and what that means for whether Maya's result is "real."

**B4. Shrink the clusters (6 pts).** Re-run the clustered SE with $G = 6$ clusters (keep $N$ roughly the
same by raising $n$). Report the clustered SE and note whether you would trust the clustered *t*-test at
face value, invoking the few-clusters rule of thumb from Ch 2.4. (You do not need to implement a wild
cluster bootstrap; naming it as the remedy is enough.)

### Deliverables

A single notebook or script that runs end-to-end on a fresh environment with the stated seed, plus the two
small tables (B2 and B4) and the B3 paragraph. State your software versions. Same seed must reproduce the
numbers.

**Optional extension (no extra points):** set $\sigma_a = 0$ so there is no lender shock, and confirm the
clustered SE collapses back toward the classical SE — clustering only "costs" you when there is genuine
within-cluster correlation to correct for.

---

## Part C — Analytic rubric (point allocations explicit)

Each row is scored at one of four levels. Part-A rows describe how the 48 Part-A points are awarded across
the six derive-and-interpret items; Part B is graded by the task allocation above, refined by the criteria
here. The Presentation/honesty row spans both parts.

| Criterion | Excellent | Proficient | Developing | Missing | Points |
|---|---|---|---|---|---|
| **Derivation correctness (Part A1–A3)** | Normal equations derived both by calculus and by orthogonality with the full-rank condition stated; $\mathbf{H}$ shown symmetric + idempotent and $\mathbf{HX}=\mathbf{X}$; Gauss–Markov rival argument reaches $\mathbf{DX}=\mathbf{0}$ and the PSD variance gap. | One derivation has a gap (e.g. orthogonality route asserted not shown), rest correct. | Final formulas stated but derivations mostly missing or with sign/transpose errors. | Not attempted or fundamentally wrong. | 22 |
| **FWL & identification reasoning (A4)** | States FWL two-step recipe correctly (residualize $y$ on $z$, $x$ on $z$, regress residuals) and correctly classifies near-collinearity as an **SE problem, not bias**, justified by what it does to $\operatorname{Var}(\tilde{x})$. | Recipe right; SE-vs-bias call right but thin justification. | Recipe garbled or calls collinearity a bias problem without seeing the unbiasedness point. | Absent or wrong on both. | 8 |
| **OVB & measurement error (A5–A6)** | Moulton inflation computed correctly; clustered-vs-HC middle distinguished; OVB formula derived with correct $\delta_1$; two-sign rule applied to the right sign; attenuation $\lambda$ defined as reliability ratio with the toward-zero direction; OVB-vs-attenuation direction contrast correct. | One numeric slip or one sign error, logic sound. | Formulas recalled but misapplied (wrong sign, $\lambda$ direction reversed). | Not attempted. | 18 |
| **Code correctness & reproducibility (Part B)** | $\hat\beta$ computed from the matrix formula; residual identities verified; three SEs correct; clustered block sum matches library; seed pinned; runs end-to-end and reproduces. | Runs and is essentially correct; minor non-reproducibility or uses a library where from-scratch was asked. | Logic flaw (e.g. clustered SE smaller than classical, or $\hat\beta$ recomputed per SE flavor); partial output. | Does not run or wrong estimator. | 24 |
| **SE choice & t-stat interpretation (B3–B4)** | Identifies clustered as the honest SE, states $\hat\beta$ did **not** change, lands the bias-vs-SE verdict, compares the inflation to the Moulton prediction, and applies the few-clusters caution at $G=6$ (names wild cluster bootstrap). | Mostly correct; one link (Moulton check or few-clusters) missing. | Reports the SEs without interpreting which to trust or why. | Absent or treats the SE change as a change in the effect. | 18 |
| **Presentation, units, honest threats** | Clean prose; specifications named in spec-discipline format (outcome · regressor · clustering · identifying assumption); never says collinearity or clustering "biases" $\hat\beta$; no "proves"/"accepts the null." | One stylistic or labeling lapse. | Several lapses; SE flavors unlabeled; verdicts without reasoning. | Unreadable or rife with banned claims. | 10 |

**Total: 100 points.** (Part A criteria sum to 48; Part B criteria sum to 42; the Presentation row adds
10, and the rubric is normalized so the maximum awarded is 100.)

A note on the spirit of the SE-choice row: this week rewards students who *keep the point estimate and the
standard error in separate mental boxes*. An answer that says "$\hat\beta_1$ was 0.297 under all three
flavors; only the SE moved, from 0.022 classical to roughly 0.05 clustered, so the *t* fell from ~13 to
~6 — this is an SE problem, the estimate is unchanged" outscores "clustering changed my result" even when
both report the same numbers. Knowing *what kind* of problem you have — a wrong target (bias) versus an
honest target with a lying *t* (SE) — is the entire point of Week 2.

---

## Instructor answer key / model-answer sketch

**A1.** (i) Expand $S(\mathbf{b}) = \mathbf{y}'\mathbf{y} - 2\mathbf{b}'\mathbf{X}'\mathbf{y} + \mathbf{b}'\mathbf{X}'\mathbf{X}\mathbf{b}$;
gradient $\partial S/\partial\mathbf{b} = -2\mathbf{X}'\mathbf{y} + 2\mathbf{X}'\mathbf{X}\mathbf{b}$;
setting it to zero gives $\mathbf{X}'\mathbf{X}\hat{\boldsymbol{\beta}} = \mathbf{X}'\mathbf{y}$. Inverting
requires $\mathbf{X}'\mathbf{X}$ nonsingular, i.e. $\mathbf{X}$ has **full column rank** (no perfect
collinearity). (ii) Geometrically, $\hat{\mathbf{y}}=\mathbf{X}\hat{\boldsymbol{\beta}}$ is the projection
of $\mathbf{y}$ onto $\operatorname{col}(\mathbf{X})$, so the residual
$\hat{\boldsymbol{\varepsilon}} = \mathbf{y}-\mathbf{X}\hat{\boldsymbol{\beta}}$ is orthogonal to every
column of $\mathbf{X}$: $\mathbf{X}'\hat{\boldsymbol{\varepsilon}} = \mathbf{0}$, i.e.
$\mathbf{X}'(\mathbf{y}-\mathbf{X}\hat{\boldsymbol{\beta}})=\mathbf{0}$ — the same normal equations, no
calculus. With a column of ones, $\mathbf{1}'\hat{\boldsymbol{\varepsilon}}=0$, which says the residuals
sum to zero. *(Full credit needs both routes and the full-rank condition.)*

**A2.** (i) Symmetric: $\mathbf{H}' = (\mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}')' = \mathbf{H}$
since $(\mathbf{X}'\mathbf{X})^{-1}$ is symmetric. Idempotent:
$\mathbf{H}\mathbf{H} = \mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}' = \mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}' = \mathbf{H}$
(the inner $\mathbf{X}'\mathbf{X}$ cancels its inverse). And
$\mathbf{H}\mathbf{X} = \mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{X} = \mathbf{X}$ — vectors
already in $\operatorname{col}(\mathbf{X})$ project to themselves. (ii) $h_{ii}$ is the **leverage** of
observation $i$: how much its own $y_i$ pulls its own fitted value $\hat y_i$, i.e. how far its
$x$-row sits from the center of the regressor cloud. Leverage near 1 means that point alone nearly
determines its fit; a single high-leverage point can swing $\hat{\boldsymbol{\beta}}$ and is exactly where
HC2/HC3 corrections (which divide by $1-h_{ii}$) matter most. *(Credit the projection argument and the
"one point controls its fit / influence" reading.)*

**A3.** Classical assumptions: linearity in parameters; no perfect collinearity (full-rank $\mathbf{X}$);
zero conditional mean $\mathbb{E}[\boldsymbol{\varepsilon}\mid\mathbf{X}]=\mathbf{0}$; homoskedasticity and
no autocorrelation $\operatorname{Var}(\boldsymbol{\varepsilon}\mid\mathbf{X})=\sigma^2\mathbf{I}$. **B**est
= smallest variance in its class; **L**inear = a linear function $\mathbf{C}\mathbf{y}$ of the outcome;
**U**nbiased = $\mathbb{E}[\hat{\boldsymbol{\beta}}]=\boldsymbol{\beta}$; **E**stimator. For the rival,
$\mathbb{E}[\tilde{\boldsymbol{\beta}}] = \mathbf{C}\mathbf{X}\boldsymbol{\beta} = [(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'+\mathbf{D}]\mathbf{X}\boldsymbol{\beta} = \boldsymbol{\beta} + \mathbf{D}\mathbf{X}\boldsymbol{\beta}$;
unbiasedness for *every* $\boldsymbol{\beta}$ forces $\mathbf{D}\mathbf{X}=\mathbf{0}$. Then
$\operatorname{Var}(\tilde{\boldsymbol{\beta}}) = \sigma^2\mathbf{C}\mathbf{C}'$; expanding with
$\mathbf{D}\mathbf{X}=\mathbf{0}$ kills the cross terms and leaves
$\sigma^2(\mathbf{X}'\mathbf{X})^{-1} + \sigma^2\mathbf{D}\mathbf{D}'$ — the OLS variance plus a PSD term,
so OLS is best. The assumption whose failure demotes OLS is **homoskedasticity/no-autocorrelation**
($\operatorname{Var}(\boldsymbol{\varepsilon}\mid\mathbf{X})=\sigma^2\mathbf{I}$); its breaking makes OLS
no longer minimum-variance but it stays **unbiased** — so no, it is not a bias problem. *(This is the
A3 hook for the SE-vs-bias theme.)*

**A4.** FWL: the long-model coefficient $\hat\beta_1$ on $x$ equals the slope from (1) regress $y$ on $z$
(and intercept), keep residuals $\tilde y$; (2) regress $x$ on $z$, keep residuals $\tilde x$; (3) regress
$\tilde y$ on $\tilde x$ — the slope is exactly $1.84$, and the residualized SE matches the long-model SE
once the degrees of freedom are corrected. **It is a standard-error problem, not a bias problem.**
Near-collinearity means firm size explains most of R&D's variation, so the residualized $\tilde x$ (the
part of R&D orthogonal to size) has *small variance*; the slope of $\tilde y$ on a low-variance regressor
is still **unbiased** for $\beta_1$, but its variance $\sigma^2/\sum\tilde x^2$ blows up. The estimate is
imprecise, not wrong. *(Full credit requires the unbiasedness point plus the shrinking-$\operatorname{Var}(\tilde x)$
mechanism.)*

**A5.** (i) Sandwich:
$\widehat{\operatorname{Var}}(\hat{\boldsymbol{\beta}}) = (\mathbf{X}'\mathbf{X})^{-1}\big(\mathbf{X}'\hat{\boldsymbol{\Omega}}\mathbf{X}\big)(\mathbf{X}'\mathbf{X})^{-1}$.
HC builds the middle from individual squared residuals (diagonal $\hat{\boldsymbol{\Omega}}$, one entry per
observation); the **clustered** version builds it from a sum of *block* outer products
$\sum_g \mathbf{X}_g'\hat{\boldsymbol{\varepsilon}}_g\hat{\boldsymbol{\varepsilon}}_g'\mathbf{X}_g$, keeping
the within-cluster covariances HC throws away. (ii) Factor $= 1+(n-1)\rho_x\rho_\varepsilon = 1 + 999(0.05)
= 1 + 49.95 = 50.95$. So the true variance is about $51\times$ the naive one, and the SE is understated by
$\sqrt{50.95}\approx 7.1\times$. (A classical $t$ of, say, 14 is really about 2.) (iii) Spec-discipline:
"outcome APR · key regressor borrower characteristic · cluster at the **lender** level — encoding the claim
that errors are correlated within a lender but independent across lenders · sample 9,000 loans." The worry:
$G=9$ clusters is *far* below the 30–50 rule of thumb, so even the clustered SE is unreliable; reach for a
wild cluster bootstrap. *(Credit the $\approx 51\times$ / $\approx 7\times$ split and naming $G=9$ as the
red flag.)*

**A6.** (i) Substitute the long model into the short-slope probability limit:
$\hat{\tilde\beta}_1 \xrightarrow{p} \dfrac{\operatorname{Cov}(x,y)}{\operatorname{Var}(x)} = \dfrac{\operatorname{Cov}(x,\ \beta_1 x + \beta_2 z + \varepsilon)}{\operatorname{Var}(x)} = \beta_1 + \beta_2\dfrac{\operatorname{Cov}(x,z)}{\operatorname{Var}(x)} = \beta_1 + \beta_2\delta_1$,
the last $\operatorname{Cov}(x,\varepsilon)=0$ term vanishing because the long model is well-specified.
Maya: $\beta_2>0$, $\delta_1<0 \Rightarrow$ bias $=\beta_2\delta_1 < 0$, i.e. the $D$ coefficient is biased
**downward** (more negative), so it **overstates** the approval penalty against $D=1$ — part of the
apparent penalty is omitted creditworthiness loaded onto $D$. (ii) $\hat\beta_1 \xrightarrow{p} \beta_1\lambda$
with $\lambda = \sigma_{x^\*}^2/(\sigma_{x^\*}^2+\sigma_m^2)\in(0,1)$, the **reliability ratio** = share of
the measured regressor's variance that is real signal. The income coefficient is pushed **toward zero**
(attenuated) — understated. Contrast: **attenuation has a known direction (always toward zero)** regardless
of the data, because $\lambda$ is a ratio of variances and variances are non-negative; OVB's direction
depends on the unknown signs of $\beta_2$ and $\delta_1$, so it can go either way. *(Credit correct OVB sign
via two-sign rule and the toward-zero attenuation direction.)*

**Part B expected results (for grading).**

- *B1:* $\hat\beta_1$ should land near $0.30$ (typically $0.27$–$0.33$ depending on seed). The two
  identities are near-machine-zero: $\sum\hat\varepsilon_i \approx 0$ and $\mathbf{X}'\hat{\boldsymbol{\varepsilon}}\approx\mathbf{0}$.
  Computing $\hat\beta$ with a library when the task said "from scratch" is a Proficient-level miss, not full
  credit.
- *B2:* The point estimate is **identical** across all three SE flavors — graders should confirm the student
  did not recompute $\hat\beta$ per flavor (a common conceptual error). Ordering: classical < HC1 $\approx$
  classical (heteroskedasticity is mild here) $\ll$ clustered. The clustered SE should be several times the
  classical SE because $a_g$ induces real within-cluster correlation and $x$ also has a cluster component.
- *B3:* Largest = clustered, and it is honest because the DGP has a genuine lender shock $a_g$; the classical
  formula assumes $\operatorname{Var}(\boldsymbol{\varepsilon}\mid\mathbf{X})=\sigma^2\mathbf{I}$, which is
  false here. The inflation factor should be roughly in line with $\sqrt{1+(n-1)\rho_x\rho_\varepsilon}$ for
  the realized $\rho$'s (order-of-magnitude agreement is enough; exact match is not expected because the
  Moulton formula is an equal-cluster approximation). The required verdict: $\hat\beta_1$ did **not** change;
  this is an **SE problem, not a bias problem** — OLS is still unbiased, the classical *t* was lying. "Real"
  means: judged against the honest clustered SE, is the *t* still large? (With $G=40$ it usually still is.)
- *B4:* With $G=6$, the clustered SE is itself noisy and not trustworthy at face value — below the 30–50
  rule of thumb. The remedy to name is the **wild cluster bootstrap** (Cameron, Gelbach & Miller 2008).
  Students should *not* conclude "the result got weaker"; they should conclude "I can no longer trust this
  particular SE."

**Quick grading heuristic.** The two highest-signal items are A4/A3 (do they correctly call collinearity
and heteroskedasticity *SE problems*, with OLS still unbiased?) and B2/B3 (did the point estimate stay
fixed while only the SE moved, and did they read that as an SE problem?). A student who keeps "wrong target"
(bias: OVB, attenuation) cleanly separate from "honest target, lying *t*" (SE: heteroskedasticity,
clustering, collinearity) has the Week-2 mindset; the rest is execution.
