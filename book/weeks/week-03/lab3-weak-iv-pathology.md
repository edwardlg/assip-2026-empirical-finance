# Lab 3 — Reproduce a Weak-IV Pathology

This is the capstone of Week 3. Chapter 3.4 built instrumental variables from the ground up — relevance, exclusion, the Wald ratio, 2SLS as Frisch–Waugh–Lovell with an instrument, the LATE interpretation, and the first-stage $F$. Chapter 3.5 then turned on the lights and showed you the dark room IV can become: when the first stage is *weak*, 2SLS does not merely get noisy, it gets **biased toward the very OLS estimate you reached for IV to escape**, and its conventional confidence interval gets *too narrow* — confidently, precisely wrong. Bound, Jaeger, and Baker taught the profession this the hard way, by feeding a *random* instrument into a famous design and watching 2SLS manufacture a plausible, significant, completely fake causal effect.

In this lab you do not read about that disaster. You **build** it. You will construct a data-generating process where you set the true effect to exactly zero, plant an endogeneity that biases OLS, and then dial a single knob — the instrument's first-stage strength — from weak to strong. You will watch 2SLS slide between OLS and the truth; measure, by averaging over many simulated worlds, how badly the conventional 95% confidence interval *under-covers*; confirm that **Anderson–Rubin** intervals recover honest ≈95% coverage; compute the **Olea–Pflueger effective $F$** and watch it flag the weak instrument; and finally flip the strength knob to strong and see every method snap back into agreement.

The single most important habit this lab drills is the one Chapter 3.5's notebook insisted on: **a single draw is an anecdote, not evidence.** One simulated dataset might, by luck, hand you a 2SLS estimate near the truth and an interval that covers it. The pathology is a statement about the *sampling distribution* of these estimators, and you cannot see a distribution from one point. So almost everything here is a Monte Carlo: redraw the universe more than a thousand times, and read *averages*, *coverage rates*, and *distributions* — never one lucky sample. A close cousin of that habit is a fat-tail subtlety you will meet head-on: because 2SLS is a *ratio* with a near-zero denominator, its sampling distribution has heavy tails, so its *mean* is thrown around by a handful of wild draws. The honest summary of "where the estimate typically lands" is the **median**, and you will see exactly why.

This lab is pure simulation. No licensed data, no credentials, no WRDS — it runs anywhere, on your laptop or the camp container, because you are the one building the universe. That is the point: when you are unsure whether a tool does what it claims, build a world where you know the truth and check.

---

## Learning goals

By the end of this lab you will be able to:

1. **Build** an endogenous-regressor data-generating process with a *tunable* instrument strength, and explain which line creates the endogeneity (so OLS is biased) and which creates the relevance (so IV is even possible).
2. Demonstrate, in numbers, that **OLS is biased** by a confounder shared between regressor and outcome.
3. Run **just-identified 2SLS by hand** (the projection formula), cross-check it against `linearmodels`, and watch it sit *between* OLS and the truth as the instrument weakens — the $1/(F+1)$ pull made visible.
4. Run a **Monte Carlo** over many draws and *measure* that the conventional 2SLS 95% confidence interval **under-covers** badly, while the **Anderson–Rubin** interval recovers ≈95% coverage.
5. Compute and interpret the **first-stage $F$** and the **Olea–Pflueger effective $F$**, and explain why a *significant* first stage is not a *strong* one.
6. **Contrast** weak vs. strong instruments and show that the IV machinery is not broken in general — it is broken by weakness.

The discipline this lab enforces is the IV reader's ledger from Chapter 3.5: before believing any 2SLS number — your own or a published paper's — you check the first-stage $F$, the effective $F$, and the AR interval, because *a 2SLS standard error cannot tell you whether the instrument is strong enough to trust it.*

---

## Setup

Per the Conventions (§5), every code block must run end-to-end on a fresh environment. Create and activate a conda environment, then install what this lab needs.

```bash
conda create -n week03-lab python=3.11 -y
conda activate week03-lab
pip install numpy "pandas>=2.2" scipy statsmodels linearmodels matplotlib
```

Open `notebooks/week-03/lab3-weak-iv-pathology.ipynb` or a script, and start every run with the same header. Two reproducibility rules you will follow without exception, exactly as in Labs 1 and 2:

- **Pin the seed.** Use `numpy`'s modern generator, `rng = np.random.default_rng(SEED)`, not the legacy global `np.random.seed`. A pinned seed means anyone re-running your code gets your exact figures.
- **Draw all randomness from that one `rng`.** A single source of randomness is what makes a Monte Carlo replayable bit-for-bit.

```python
import matplotlib
matplotlib.use("Agg")          # headless: render figures to buffers, not a screen

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from linearmodels.iv import IV2SLS

SEED = 20260528                # any fixed integer; write it down
rng = np.random.default_rng(SEED)
```

One honest caveat before you start, because it will save you confusion later. Monte Carlo estimates are *themselves* random. When you "measure" a coverage rate and get $0.801$ instead of some clean round number, that is the sampling error in your *measurement of a procedure*, not a bug. Reruns with the *same* seed are bit-for-bit identical; reruns with a *different* seed wobble by a Monte Carlo standard error. Everything below uses `SEED = 20260528` and the numbers quoted are what that seed produces — yours will match if you draw all randomness from the one `rng`, in order.

---

## Step 1 — Build an endogenous-regressor DGP with a tunable instrument

**What to do.** Build the world from Chapter 3.5.8, rigged so that everything that can go wrong is something *you* chose and can *measure*. The structural equation is the cleanest possible:

$$y = \beta\, x + u, \qquad \beta = 0.$$

The true effect is *exactly zero*. That is a deliberate choice: with $\beta = 0$, any nonzero estimate you ever see is **pure bias**, with no real signal to confuse it. Now make $x$ **endogenous** and the instrument $z$ **valid but tunably weak**:

$$x = \pi\, z + c\, u + v, \qquad y = \beta\, x + u.$$

Read every term. The instrument $z$, the structural error $u$, and the idiosyncratic noise $v$ are independent standard normals. The coefficient $\pi$ is the **first-stage strength** — the knob you will turn. The coefficient $c$ is the **endogeneity strength**: because the same $u$ appears in both $x$ (through $c\,u$) and $y$ (as the error), $x$ is correlated with the structural error, so OLS will be biased. And notice what is *not* in $y$: the instrument $z$ never enters the outcome equation. Since $\beta = 0$, the outcome is literally $y = u$, so $z$ touches $y$ *only* through $x$ — **exclusion holds by construction.** We are testing weakness, not invalidity. You isolate one disease at a time.

**Code skeleton.**

```python
def simulate(N, pi, beta_true=0.0, endog=2.0, rng=None):
    """One dataset: endogenous x, valid-but-(maybe)-weak instrument z, true effect beta_true."""
    z = rng.normal(size=N)                 # valid instrument
    u = rng.normal(size=N)                 # structural error (the source of endogeneity)
    v = rng.normal(size=N)                 # idiosyncratic first-stage noise
    x = pi * z + endog * u + v             # weak first stage (pi) + endogeneity (endog * u)
    y = beta_true * x + u                  # exclusion holds: z is absent from y given x
    return z, x, y

# Settings for the whole lab — change PI to retune instrument strength.
N         = 400        # sample size
PI_WEAK   = 0.07       # weak first stage   <- the pathology lives here
PI_STRONG = 0.8        # strong first stage <- the contrast in Step 6
ENDOG     = 2.0        # endogeneity strength -> OLS badly biased upward
BETA_TRUE = 0.0        # the truth; any nonzero estimate is pure bias

z, x, y = simulate(N, PI_WEAK, rng=rng)
print(f"Drew one weak-IV dataset: N={N}, pi={PI_WEAK}, true beta={BETA_TRUE}")
```

**What to expect.** Nothing prints but a confirmation line — this step only builds the machine. The thing to internalize is the *anatomy*: `endog * u` is the endogeneity (the same $u$ is in $y$), and `pi * z` is the relevance (how hard the instrument shoves $x$). Turning `pi` down toward zero is turning the instrument from strong to weak *while leaving everything else fixed*, which is exactly the controlled experiment Chapter 3.5 wanted and a real dataset would never grant you.

**Reflection.** Point to the single term that makes OLS biased, and the single term that makes IV possible at all. If you set `endog = 0`, what happens to the OLS bias — and would you still need an instrument? If you set `pi = 0` exactly, which of the two conditions for a valid instrument (relevance, exclusion) fails, and what does that do to the magic ratio $\widehat{\operatorname{Cov}}(z,y)/\widehat{\operatorname{Cov}}(z,x)$?

---

## Step 2 — Show the OLS bias

**What to do.** Before touching IV, confirm the disease. Regress $y$ on $x$ by ordinary least squares. Because $x$ shares the shock $u$ with $y$, the OLS slope will not recover the true zero — it will land well above it, biased *upward* by the endogeneity. This is the bias-and-consistency ledger of Chapter 2.5 made concrete: a relevant, correlated variable ($u$) sits in the error, so $\mathbb{E}[\varepsilon \mid x] \neq 0$, and OLS is inconsistent.

**Code skeleton.**

```python
def ols_slope(x, y):
    """Plain OLS slope of y on [1, x]."""
    n = len(y)
    X = np.column_stack([np.ones(n), x])
    return np.linalg.solve(X.T @ X, X.T @ y)[1]

print(f"OLS beta_hat = {ols_slope(x, y):+.3f}   (true value is {BETA_TRUE:+.3f})")
```

**What to expect.** On this seed the single-draw OLS slope is about $+0.40$ against a truth of $0$. Do not over-read one draw (Step 5 will average it properly), but the sign and rough size are no accident: with $c = 2.0$ the endogeneity is strong and positive, so OLS is dragged up. This is precisely the number IV is *supposed* to fix — keep $+0.4$ in your head as "the bias we are trying to escape," because the punchline of the lab is that a weak instrument hands a big chunk of it right back.

**Reflection.** The OLS bias here is *upward*. Trace it to the DGP: $x$ and $u$ are positively related (through `endog * u`), and $u$ *is* the error in $y$, so the regression mistakes "high $u$" for "high $x$ causes high $y$." Write the omitted-variable-bias formula from Chapter 2.5 for this case and predict the *sign* of the bias from the signs of the two covariances — then check it against your number.

---

## Step 3 — Run 2SLS by hand and watch it sit between OLS and the truth

**What to do.** Now instrument. With one instrument, one endogenous regressor, and a constant, just-identified 2SLS is the projection estimator

$$\hat{\boldsymbol\beta}_{\text{2SLS}} = (\mathbf{X}'\mathbf{P}_Z\mathbf{X})^{-1}\mathbf{X}'\mathbf{P}_Z\,\mathbf{y},
\qquad \mathbf{P}_Z = \mathbf{Z}(\mathbf{Z}'\mathbf{Z})^{-1}\mathbf{Z}',$$

with $\mathbf{X} = [\mathbf{1}, x]$ and $\mathbf{Z} = [\mathbf{1}, z]$. You will write this by hand so nothing is hidden — and crucially, you will also compute the **conventional standard error**, $\hat\sigma^2(\mathbf{X}'\mathbf{P}_Z\mathbf{X})^{-1}$, the one the textbook formula reports and the one that is about to lie to you. The structural residual uses the *real* $x$, not the fitted $\hat x$ — a subtlety students get wrong constantly, which is one more reason to hand-roll it once and then **never trust your hand-rolled SE for reporting** (Chapter 3.4's warning). You confirm your code is right by matching `linearmodels.IV2SLS` to machine precision. While you are here, grab the **first-stage $F$**: with one instrument it is simply $t^2$ from regressing $x$ on $z$.

**Code skeleton.**

```python
def fit_2sls(z, x, y):
    """Hand-rolled just-identified 2SLS: returns (beta_hat, conventional SE)."""
    n = len(y)
    Z = np.column_stack([np.ones(n), z])
    X = np.column_stack([np.ones(n), x])
    ZtZ_inv = np.linalg.inv(Z.T @ Z)
    Pz_X = Z @ (ZtZ_inv @ (Z.T @ X))           # P_Z X
    XtPzX = X.T @ Pz_X
    beta  = np.linalg.solve(XtPzX, Pz_X.T @ y) # (X'PzX)^-1 X'Pz y
    resid = y - X @ beta                        # structural residual: uses x, NOT x-hat
    sigma2 = (resid @ resid) / (n - X.shape[1])
    cov = sigma2 * np.linalg.inv(XtPzX)
    return beta[1], np.sqrt(cov[1, 1])

def first_stage_F(z, x):
    """One-instrument first-stage F = t^2 from regressing x on [1, z]."""
    n = len(x)
    Z = np.column_stack([np.ones(n), z])
    ZtZ_inv = np.linalg.inv(Z.T @ Z)
    b = ZtZ_inv @ (Z.T @ x)
    resid = x - Z @ b
    sigma2 = (resid @ resid) / (n - 2)
    se1 = np.sqrt(sigma2 * ZtZ_inv[1, 1])
    return (b[1] / se1) ** 2

# Hand-rolled estimate, and a cross-check against linearmodels on the same draw:
b_hand, se_hand = fit_2sls(z, x, y)
df = pd.DataFrame({"y": y, "x": x, "z": z, "const": 1.0})
lm = IV2SLS(df["y"], df[["const"]], df[["x"]], df[["z"]]).fit(cov_type="unadjusted")

print(f"hand-rolled 2SLS  beta = {b_hand:+.6f}")
print(f"linearmodels 2SLS beta = {lm.params['x']:+.6f}")
print(f"max abs difference     = {abs(b_hand - lm.params['x']):.2e}")
print()
print(f"OLS  beta = {ols_slope(x, y):+.3f}   (true 0.000, biased UP)")
print(f"2SLS beta = {b_hand:+.3f}   SE = {se_hand:.3f}   first-stage F = {first_stage_F(z, x):.2f}")
```

**What to expect.** Three things. First, your hand-rolled coefficient matches `linearmodels` to about $10^{-16}$ — floating-point dust — so you know the machine is correct. Second, on this seed the single-draw 2SLS estimate lands around $+0.42$ with a first-stage $F$ near $1.5$ — *above* the OLS number, not below it, which is your first taste of how violently a single weak-IV draw can swing. (A weak instrument's estimate is a fat-tailed ratio; one draw can land almost anywhere.) Third, the reported SE of about $0.18$ looks reassuringly tight — and that tightness is exactly the lie Chapter 3.5 warned about. **Do not draw any conclusion from this one number.** The whole point of Steps 4–5 is that you cannot read the pathology off a single draw; you have to average.

If you now go back to Step 1 and re-run with `PI_STRONG = 0.8`, the same single-draw 2SLS will land near the true zero with a large $F$. That contrast is the experiment — but to make it rigorous, you must repeat it thousands of times.

**Reflection.** Your single-draw 2SLS came out *above* OLS this time, even though Chapter 3.5 says weak 2SLS is biased *toward* OLS (which is below it would be… no — OLS is at $0.4$, the truth at $0$, so "toward OLS" means staying high). Why is "where this one draw landed" not in tension with "the pathology pulls the *typical* estimate toward OLS"? Name the statistical object the chapter's claim is actually about. (Hint: it is a property of the distribution, not of a point.)

---

## Step 4 — Monte Carlo: conventional CIs under-cover, AR CIs ≈ 95%

This is the heart of the lab, and it has two parts: build the Anderson–Rubin interval, then run the Monte Carlo that exposes the coverage failure.

### 4a — Anderson–Rubin by hand

**What to do.** The pathology came from one place: *dividing by a weak, error-ridden first stage.* So the cure (Chapter 3.5.4) is an inference procedure that **never divides by the first stage**. To test $H_0:\beta = \beta_0$, form the adjusted outcome $y - \beta_0 x$ and regress it on $z$. If $\beta_0$ is the true effect, then $z$ — which only ever touched $y$ through $x$ — should have *no* relationship with the adjusted outcome, so the coefficient on $z$ must be zero; test it with an $F$-test. To get a confidence interval, **invert the test**: sweep $\beta_0$ over a grid and keep every value the test fails to reject at 5%.

A small algebra trick makes the grid sweep cheap: regressing $(y - \beta_0 x)$ on $\mathbf{Z}$, the coefficient on $z$ and the residual are both *linear* in $\beta_0$, so you compute the four pieces once and evaluate the AR statistic at every grid point. An accepted set that touches a grid edge is flagged **unbounded** — the honest signature of a weak instrument (Chapter 3.5.5).

```python
def ar_interval(z, x, y, grid):
    """Anderson-Rubin 95% CI by grid inversion. Returns (lo, hi, empty, unbounded)."""
    n = len(y)
    Z = np.column_stack([np.ones(n), z])
    ZtZ_inv = np.linalg.inv(Z.T @ Z)
    crit = stats.f.ppf(0.95, 1, n - 2)         # 1 instrument -> F(1, n-2)
    by = ZtZ_inv @ (Z.T @ y)                    # coef of y on [1, z]
    bx = ZtZ_inv @ (Z.T @ x)                    # coef of x on [1, z]
    ry = y - Z @ by                             # residual pieces, both linear in b0
    rx = x - Z @ bx
    var_coef1 = ZtZ_inv[1, 1]
    accept = np.zeros(len(grid), dtype=bool)
    for i, b0 in enumerate(grid):
        coef1  = by[1] - b0 * bx[1]             # coef on z for this candidate b0
        resid  = ry - b0 * rx
        sigma2 = (resid @ resid) / (n - 2)
        F_ar   = coef1 ** 2 / (sigma2 * var_coef1)
        accept[i] = F_ar < crit                 # fail to reject -> keep b0
    if not accept.any():
        return np.nan, np.nan, True, False      # empty (over-id only; won't happen here)
    idx = np.where(accept)[0]
    lo, hi = grid[idx[0]], grid[idx[-1]]
    unbounded = bool(accept[0] or accept[-1])   # touches an edge
    return lo, hi, False, unbounded

GRID = np.linspace(-10, 10, 1001)               # candidate beta values for inversion
```

### 4b — The Monte Carlo engine

**What to do.** Now wrap one experiment: at a fixed `pi`, redraw the world `reps` times and, on every draw, record the OLS estimate, the 2SLS estimate, the first-stage $F$, whether the conventional 95% interval ($\hat\beta \pm 1.96\,\text{SE}$) covered the truth, and whether the AR interval covered it. **Coverage** is the fraction of draws whose interval contained the true zero; a 95% interval that earns its name covers about 95% of the time.

```python
def run_mc(N, pi, reps, grid, rng, beta_true=0.0, endog=2.0):
    """One Monte Carlo experiment at fixed pi. Returns arrays + coverage rates."""
    ols_e = np.empty(reps); iv_e = np.empty(reps); Fs = np.empty(reps)
    conv_cov = ar_cov = ar_unb = 0
    for r in range(reps):
        z, x, y = simulate(N, pi, beta_true=beta_true, endog=endog, rng=rng)
        b_iv, se_iv = fit_2sls(z, x, y)
        iv_e[r]  = b_iv
        ols_e[r] = ols_slope(x, y)
        Fs[r]    = first_stage_F(z, x)
        if b_iv - 1.96 * se_iv <= beta_true <= b_iv + 1.96 * se_iv:   # conventional CI
            conv_cov += 1
        lo, hi, empty, unb = ar_interval(z, x, y, grid)               # AR CI
        if not empty:
            ar_unb += unb
            if lo <= beta_true <= hi:
                ar_cov += 1
    return {"ols": ols_e, "iv": iv_e, "F": Fs,
            "conv_coverage": conv_cov / reps,
            "ar_coverage":  ar_cov / reps,
            "ar_unbounded": ar_unb / reps}

REPS = 1200
weak = run_mc(N, PI_WEAK, REPS, GRID, rng, beta_true=BETA_TRUE, endog=ENDOG)

print(f"WEAK instrument (pi={PI_WEAK}), {REPS} draws, true beta = {BETA_TRUE}\n")
print(f"  median OLS  estimate      = {np.median(weak['ols']):+.3f}   (biased up by endogeneity)")
print(f"  median 2SLS estimate      = {np.median(weak['iv']):+.3f}   (sits BETWEEN OLS and 0)")
print(f"  mean   2SLS estimate      = {np.mean(weak['iv']):+.3f}   (fat-tailed; mean is unstable!)")
print()
print(f"  conventional 95% coverage = {weak['conv_coverage']:.3f}   <-- should be 0.95, badly UNDER")
print(f"  Anderson-Rubin coverage   = {weak['ar_coverage']:.3f}   <-- back near 0.95, HONEST")
print(f"  fraction AR CIs unbounded = {weak['ar_unbounded']:.3f}")

pull = np.median(weak['iv']) / np.median(weak['ols'])
print(f"\n  2SLS retains ~{pull:.0%} of OLS's bias (a strong instrument would retain ~0%).")
```

**What to expect.** On `SEED = 20260528` with 1,200 draws you will see, up to Monte Carlo noise, something close to:

```
  median OLS  estimate      = +0.400   (biased up by endogeneity)
  median 2SLS estimate      = +0.258   (sits BETWEEN OLS and 0)
  mean   2SLS estimate      = -0.561   (fat-tailed; mean is unstable!)

  conventional 95% coverage = 0.801   <-- should be 0.95, badly UNDER
  Anderson-Rubin coverage   = 0.973   <-- back near 0.95, HONEST
  fraction AR CIs unbounded = 0.911

  2SLS retains ~65% of OLS's bias (a strong instrument would retain ~0%).
```

Read every number, because this output *is* Chapter 3.5. The **median OLS** sits at $+0.40$ — endogeneity, exactly as Step 2 warned. The **median 2SLS** sits at $+0.258$ — strictly *between* the biased OLS ($0.40$) and the truth ($0$). It did **not** purge the bias; it shrank it partway back toward OLS and stopped, retaining roughly $65\%$ of it. That is the $1/(F+1)$ pull made visible: with a tiny first-stage $F$, 2SLS keeps most of OLS's bias. The **conventional 95% coverage is $0.801$** — a researcher reporting "$\hat\beta \pm 1.96\,\text{SE}$" from a single weak-IV dataset is wrong about their own uncertainty about *one time in five*, not one in twenty. The **AR coverage is $0.973$**, back near the promised 95%, because AR never divided by the weak first stage — at the price of being **unbounded on 91% of draws**, which is not a failure but AR honestly refusing to pretend it can pin down an effect this instrument cannot identify.

Notice the **mean 2SLS is $-0.561$** — on the *wrong side* of zero and nowhere near the median. That is the fat-tail subtlety: 2SLS is a ratio with a near-zero denominator, so a few draws where the first stage nearly vanishes throw enormous values into the average and yank the mean around. The mean is *not* the honest summary of "where the estimate typically lands." The **median** is. Lean on the median for every central-tendency claim in this lab, and you have learned something most first-time IV users never internalize.

**Reflection.** The conventional interval covers only $80\%$ of the time, yet on any single draw it *looks* like a perfectly normal 95% interval — tight, symmetric, often excluding zero. Explain, in terms of the *shape* of the 2SLS sampling distribution versus the normal the SE formula assumes, why "estimate ± 1.96 SE" systematically promises more precision than it delivers here. Then connect it to the deeper moral of Chapter 3.5: which diagnostics live *outside* the 2SLS point estimate and could have warned you, and why can the SE itself never be one of them?

---

## Step 5 — Compute and interpret the effective F

**What to do.** You have two ways to measure first-stage strength. The first, the classical first-stage $F$, you already coded in Step 3. But Chapter 3.4 was emphatic: the classical $F$ assumes homoskedastic, non-clustered errors, and the right statistic under realistic error structures is the **Olea–Pflueger effective $F$**, which `linearmodels` reports directly in its first-stage diagnostics. Pull it on a handful of fresh draws in each world and compare. While you are at it, look at the *distribution* of the classical $F$ across the weak draws — it carries the Bound–Jaeger–Baker lesson directly.

```python
def effective_F(z, x, y):
    """Olea-Pflueger effective F from linearmodels' robust first-stage diagnostics."""
    d = pd.DataFrame({"y": y, "x": x, "z": z, "const": 1.0})
    res = IV2SLS(d["y"], d[["const"]], d[["x"]], d[["z"]]).fit(cov_type="robust")
    return float(res.first_stage.diagnostics.loc["x", "f.stat"])

rng_F = np.random.default_rng(7)
eff_weak   = np.array([effective_F(*simulate(N, PI_WEAK,   endog=ENDOG, rng=rng_F)) for _ in range(100)])
eff_strong = np.array([effective_F(*simulate(N, PI_STRONG, endog=ENDOG, rng=rng_F)) for _ in range(100)])

print("Olea-Pflueger effective F (mean over 100 fresh draws each):")
print(f"  weak   instrument: {eff_weak.mean():6.2f}   (below ~10 -> FLAGGED weak)")
print(f"  strong instrument: {eff_strong.mean():6.1f}   (far above -> strong)")
print()
print("Classical first-stage F across the 1,200 weak draws (significance != strength):")
print(f"  mean F             = {np.mean(weak['F']):.2f}")
print(f"  fraction F < 10    = {np.mean(weak['F'] < 10):.3f}   (klaxon almost always sounding)")
print(f"  MAX F              = {np.max(weak['F']):.1f}   <-- sometimes spuriously LARGE")
```

**What to expect.** The effective $F$ comes in around $1.2$ for the weak instrument and around $54$ for the strong one — it correctly **flags the weak case** (far below the ~10 threshold) and **clears the strong case** by a mile. The classical-$F$ distribution carries the deeper lesson: the mean weak $F$ is about $1.4$ and **over 99% of weak draws have $F < 10$** — the klaxon is almost always sounding — *but the maximum across 1,200 draws is around 14*, comfortably above 10. A researcher unlucky enough to draw that one sample would declare the instrument "strong" and march straight into the pathology. This is Bound–Jaeger–Baker in one line: **a statistically significant first stage is not a strong one.** With a big enough sample, or enough draws, a useless instrument occasionally clears the $F > 10$ bar by pure chance. The $F > 10$ rule guards the *typical* draw, never *your* draw — which is why you report the effective $F$ and never lean on a single significant first stage.

**Reflection.** The effective $F$ ($\approx 1.2$) and the mean classical $F$ ($\approx 1.4$) are close here, because the DGP's errors happen to be homoskedastic. Construct (in words) a version of this DGP where the classical $F$ would look *reassuring* while the effective $F$ correctly flags weakness — what would you have to do to the error term? Which statistic would Chapter 3.4 tell you to trust in a real finance dataset, and why?

---

## Step 6 — Contrast: a strong instrument, where everything works

**What to do.** The machinery is not broken in general — it is broken by *weakness*. Re-run the identical Monte Carlo with the strength knob set to `PI_STRONG = 0.8`, changing nothing else, and watch every pathology evaporate. This is the controlled half of the experiment: same code, same endogeneity, same sample size, one knob turned.

```python
strong = run_mc(N, PI_STRONG, REPS, GRID, rng, beta_true=BETA_TRUE, endog=ENDOG)

print(f"STRONG instrument (pi={PI_STRONG}), {REPS} draws, true beta = {BETA_TRUE}\n")
print(f"  median OLS  estimate      = {np.median(strong['ols']):+.3f}   (OLS is never fixed)")
print(f"  median 2SLS estimate      = {np.median(strong['iv']):+.3f}   (on the truth -> bias purged)")
print(f"  conventional 95% coverage = {strong['conv_coverage']:.3f}   (recovered)")
print(f"  Anderson-Rubin coverage   = {strong['ar_coverage']:.3f}   (agrees)")
print(f"  fraction AR unbounded     = {strong['ar_unbounded']:.3f}   (never)")
print(f"  mean first-stage F        = {np.mean(strong['F']):.0f}   (off the charts)")

# Optional: one bar chart makes the contrast unmissable (Agg backend -> save, don't show).
fig, ax = plt.subplots(figsize=(8, 5))
labels = ["Weak\nconventional", "Weak\nAR", "Strong\nconventional", "Strong\nAR"]
vals   = [weak["conv_coverage"], weak["ar_coverage"],
          strong["conv_coverage"], strong["ar_coverage"]]
bars = ax.bar(labels, vals, color=["#c0392b", "#27ae60", "#e67e22", "#16a085"],
              edgecolor="black", alpha=0.85)
ax.axhline(0.95, color="black", linestyle="--", linewidth=2, label="nominal 95%")
ax.set_ylabel("empirical coverage of the truth"); ax.set_ylim(0, 1.05)
ax.set_title("Conventional 2SLS CIs under-cover only when the instrument is weak")
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width()/2, v + 0.02, f"{v:.2f}", ha="center", fontweight="bold")
ax.legend(loc="lower right"); fig.tight_layout()
fig.savefig("coverage_weak_vs_strong.png", dpi=120)
print("\nSaved coverage_weak_vs_strong.png")
```

**What to expect.** With the strong instrument the world is well-behaved: the **median 2SLS lands on the truth** (about $0.00$ — the bias is genuinely purged, OLS's $+0.40$ notwithstanding, since OLS is *never* fixed and stays biased), **conventional coverage recovers to $\approx 0.95$** (about $0.948$), **AR coverage agrees** ($\approx 0.95$, here $0.953$) and is **never unbounded**, and the **mean first-stage $F$ is around 52** — off the charts. The bar chart makes it unmissable: the weak-conventional bar sits far below the 95% line while the other three clear it. The conventional method is not "approximately right" under a weak instrument; it is *systematically overconfident* — and it snaps back to honest the instant the instrument is strong. Every method agrees when the first stage is strong, which is the reassuring half of the lesson: **IV delivers on its promise when, and only when, you have a strong instrument — so the discipline is to check.**

**Reflection.** With the strong instrument, the conventional and AR intervals nearly coincide. Why should they? Argue from the AR mechanism: when the first stage is strong, the accepted set of $\beta_0$ values is a tight bounded interval centered near the truth, and the $1/(F+1)$ pull is essentially zero. Then state the rule you would put on a referee's checklist: under what single observed condition is it safe to *skip* the AR interval and just report the conventional 2SLS SE — and why is "the SE is small" never that condition?

---

## You're done when…

Use this checklist. A box is checked only when you can point to the number or figure that proves it.

- [ ] **Step 1.** Your `simulate` builds $x$ with both an endogeneity term (`endog * u`, shared with $y$) and a relevance term (`pi * z`), and you can name which is which and why exclusion holds by construction.
- [ ] **Step 2.** OLS recovers a slope around $+0.4$ against a truth of $0$, and you can predict the *sign* of the bias from the DGP.
- [ ] **Step 3.** Your hand-rolled 2SLS matches `linearmodels` to ~$10^{-16}$, and you can explain why *no* conclusion should be drawn from the single-draw estimate or its tight SE.
- [ ] **Step 4.** Over 1,200 draws, the **median 2SLS sits strictly between the truth (0) and the median OLS** (retaining ~65% of OLS's bias); **conventional coverage is well below 0.95** (~0.80) while **AR coverage is ~0.95** (~0.97); and you can explain why the *mean* 2SLS ($\approx -0.56$) is the wrong summary and the **median** is the right one.
- [ ] **Step 5.** The **effective $F$ is ~1.2 for the weak instrument and ~54 for the strong one**; you can show that >99% of weak draws have classical $F < 10$ yet the *max* exceeds 10, and state the Bound–Jaeger–Baker lesson it illustrates.
- [ ] **Step 6.** With `PI_STRONG`, **2SLS lands on the truth, conventional coverage recovers to ~0.95, AR agrees and is never unbounded, and mean $F$ ~52**; your coverage bar chart shows only the weak-conventional bar below the 95% line.
- [ ] **Reproducibility.** Every number regenerates identically from `SEED = 20260528` and one `rng`; rerunning top-to-bottom reproduces the quoted values, and you can name your seed.

---

## Reflection questions — tied to the Ch 3.5 referee's checklist

Chapter 3.5 left you a ledger of questions to run on any IV result. You have now *built* the world those questions police. Answer each by pointing back to a number you produced.

1. **Relevance / weak-instrument bias.** A classmate shows you a 2SLS coefficient of $0.26$ with a tight SE, an OLS coefficient of $0.40$, and a first-stage $F$ of $4$. Using the $1/(F+1)$ heuristic, is the 2SLS estimate's proximity to OLS a coincidence or exactly what a weak instrument predicts? Map their three numbers onto your Step 4 output and say which simulated quantity each corresponds to.

2. **Honest inference.** Your conventional 95% interval covered the truth only $80\%$ of the time, while AR covered $97\%$. The classmate above reports only the conventional SE and no AR interval. Write the one-sentence demand you would make as a referee, and describe what the AR interval would most likely look like for their weak instrument (recall that yours was unbounded on 91% of draws) and what that shape *means*.

3. **Significance is not strength (BJB).** Across your 1,200 weak draws, over 99% had $F < 10$ but the maximum exceeded 10. Explain to the classmate, who happened to draw an $F$ of $12$ and declared victory, why their single significant/strong-looking first stage is not reassuring — and name the diagnostic from Chapter 3.4 that does not get fooled by a lucky draw, with the value it took in your weak world.

4. **The fat-tail subtlety.** You reported the *median* 2SLS as the central-tendency summary, not the mean. A coauthor insists the mean is "more standard." Using your two numbers (median $\approx +0.26$, mean $\approx -0.56$), explain why the mean is meaningless for a weak-IV ratio estimator and what feature of its sampling distribution makes the median the honest choice.

5. **Establish it by averaging.** Your Step 3 single draw came out *above* OLS; your Step 4 median came out *between* OLS and the truth. Write the methodological rule this contrast teaches — the same rule Lab 1 drilled with sizes and powers — and explain why a referee should distrust any weak-IV claim built on a single estimate, however significant.

---

## Where this connects

You have now reproduced, with your own hands, the disaster Bound–Jaeger–Baker made famous: a valid but weak instrument that drags 2SLS back toward the OLS bias it was meant to cure, reports a confidence interval far too narrow to be honest, and clears the $F > 10$ bar by luck just often enough to fool someone. And you watched the two cures work — the **Olea–Pflueger effective $F$** that flags the weakness and the **Anderson–Rubin interval** that stays honest no matter how weak the first stage is, even when honesty means confessing, via an unbounded interval, that the data simply cannot answer the question.

The habit underneath all of it is the one that runs through every lab in this camp: *when you are unsure whether a tool does what it claims, build a universe where you know the truth and check — and establish the answer by averaging over many draws, never one.* You used it in Lab 1 to audit the size and power of a test; you used it in Lab 2 to confirm Fama–MacBeth recovers a planted premium; you used it here to catch IV lying. Week 4 hands you design-based methods — difference-in-differences, regression discontinuity, synthetic control — that lean on different assumptions, and you will stress-test those the same way: plant a truth, simulate the world, and see whether the estimator and its standard error tell you the truth or a confident fiction. Keep this notebook; the Monte Carlo skeleton and the AR-by-inversion trick will return.
