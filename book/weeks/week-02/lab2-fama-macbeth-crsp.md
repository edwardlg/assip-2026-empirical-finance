# Lab 2 — Replicate a Textbook Fama–MacBeth on CRSP

This is the capstone of Week 2. Across Chapters 2.1–2.4 you rebuilt OLS from the floor up: the design matrix, the normal equations $\hat{\boldsymbol\beta} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$, the Gauss–Markov guarantees, and — the part that will earn its keep today — the honest sandwich variance and the idea that **correlated errors make naive standard errors lie.** Now you put all of it to work on the single most famous estimation procedure in empirical asset pricing.

The question is Sam's, scaled up. In Ch 2.1 Sam ran one regression of one stock's return on the market and got one beta — a number for how much his stock moves when the market moves 1%. The natural next question is the one that launched a thousand papers: **across all stocks, do the high-beta ones actually earn higher average returns?** The Capital Asset Pricing Model (CAPM) says yes, and it says exactly how much: the extra expected return per unit of beta should equal the **market risk premium**, $\lambda$. Testing that claim means relating a *cross-section* of average returns to a *cross-section* of betas — and doing it in a way whose standard errors survive the fact that, in any given month, every stock's return is shoved around by the same market-wide shock.

Eugene Fama and James MacBeth solved this in 1973 with a procedure so clean it is still the default fifty years later (Fama & MacBeth 1973, *Journal of Political Economy* 81(3), 607–636). Their trick — and it *is* a trick, in the reveal-the-trick sense — is to run the cross-sectional regression **separately in each time period** and then treat the resulting sequence of slope estimates as a little time series whose mean is your answer and whose scatter gives you a standard error for free. That standard error automatically handles the within-month cross-sectional correlation that would otherwise wreck you. By the end of this lab you will have built the whole two-pass machine, run it, and — because you will plant a known premium in synthetic data — *checked* that it recovers the truth.

A note on data, before anything else, because it governs how this lab is structured. The canonical Fama–MacBeth test runs on **CRSP** monthly stock returns, and CRSP is licensed. Per the Conventions (§5), licensed data stays on GMU infrastructure: you may only touch it read-only on Hopper or the WRDS Cloud, and no CRSP numbers ever get copied into these notes. So this lab has **two paths**:

- **Path A (real CRSP via WRDS):** the connection pattern, the exact query, and a pinned snapshot date. Run this *only* on GMU infrastructure. We do not print any CRSP output here.
- **Path B (synthetic fallback):** a fully self-contained, seeded simulation with the *same schema* (`permno`, `month`, `ret`, plus a market column) and a *known* planted risk premium. It runs anywhere — your laptop, Colab, the camp container — with no credentials. Every student completes the full two-pass estimation on Path B; Path A is the "do it for real on Hopper" extension.

---

## Learning goals

By the end of this lab you will be able to:

1. State the two-pass Fama–MacBeth procedure precisely and explain *why* it is two passes, not one big panel regression.
2. **Pass 1:** estimate a time-series beta for every stock by regressing its returns on a market factor (full-sample first, then a rolling window).
3. **Pass 2:** run a cross-sectional regression of returns on betas *separately in each period*, producing a time series of slope estimates $\hat\gamma_{1,t}$.
4. Aggregate the period-by-period slopes into a single **Fama–MacBeth point estimate** (their mean) and a **Fama–MacBeth standard error** (their scatter over $\sqrt{T}$), and read off the FM t-statistic.
5. Explain in plain terms *how* the FM standard error neutralizes cross-sectional correlation, and connect that mechanism to the clustering ideas from Ch 2.4.
6. Connect to a real WRDS/CRSP pull (Path A) without ever copying licensed data off GMU infrastructure.
7. Verify your machine against ground truth by recovering a *planted* premium from synthetic data, with a sensible t-stat.

The discipline this lab enforces is the empirical-spec discipline from the Conventions: by the end you will be able to write the one-line spec for this regression — outcome, key regressor, sample, and *clustering/standard-error choice* — and defend the last item, which is the whole point of Fama–MacBeth.

---

## Setup

Every code block must run end-to-end on a fresh environment (Conventions §5). Create and activate a conda environment, then install what this lab needs. The `wrds` package is only used on Path A; install it now so the import does not surprise you later.

```bash
conda create -n week02-lab python=3.11 -y
conda activate week02-lab
pip install numpy "pandas>=2.2" scipy statsmodels matplotlib wrds pyarrow
```

Open `notebooks/week-02/lab2-fama-macbeth-crsp.ipynb` or a script, and start every run with the same header. Two reproducibility rules you will follow without exception:

- **Pin the seed.** Use `numpy`'s modern generator, `rng = np.random.default_rng(SEED)`, not the legacy global `np.random.seed`. A pinned seed means anyone re-running your code gets your exact figures.
- **Draw all randomness from that one `rng`.** A single source of randomness is what makes a run replayable bit-for-bit.

```python
import numpy as np
import pandas as pd

SEED = 20260527            # any fixed integer; write it down
rng = np.random.default_rng(SEED)
```

One honest caveat to carry through the whole lab: the Fama–MacBeth premium estimate converges to the *average realized factor return over your sample*, not to its theoretical mean. Your recovered number will sit near the planted truth but will wobble around it by sampling error, and the FM standard error is precisely the size of that wobble. That is not a bug; it is the thing you are measuring.

---

## The two-pass method, with the math

Before you write any code, get the procedure straight on paper. We have a panel: many stocks $i = 1,\dots,N$ observed over many months $t = 1,\dots,T$. We observe each stock's monthly **excess return** $r_{it}$ (return minus the risk-free rate) and a **market excess return** $r_{m,t}$ (the market's return over the risk-free rate). The CAPM claim, written as a relationship we can estimate, is that a stock's expected excess return is proportional to its market beta:

$$
\mathbb{E}[r_{it}] = \gamma_0 + \gamma_1\,\beta_i,
$$

where $\beta_i$ is stock $i$'s sensitivity to the market and $\gamma_1$ is the **risk premium** per unit of beta — the number we want. Strict CAPM predicts $\gamma_0 = 0$ (no reward for bearing only diversifiable risk) and $\gamma_1 = \mathbb{E}[r_{m,t}]$ (the price of one unit of market risk is the market's own average excess return). Testing CAPM means estimating $\gamma_0$ and $\gamma_1$ and asking whether they match those predictions.

The naive thing — pool every stock-month into one giant OLS of $r_{it}$ on $\beta_i$ — is exactly the mistake Ch 2.4 warned you about. In any single month, *every* stock's return is jolted by the same market move; the errors of all $N$ stocks in month $t$ are violently correlated (a **time effect**, in Petersen's language). Pooled OLS would treat your $N \times T$ stock-months as $N \times T$ independent observations when, on the cross-sectional dimension, a single month's data is really closer to *one* draw. The standard error would be wildly too small. Fama and MacBeth's design dissolves this problem instead of patching it.

**Pass 1 — time-series betas.** For each stock $i$, run a time-series regression of its excess return on the market excess return:

$$
r_{it} = \alpha_i + \beta_i\, r_{m,t} + u_{it}, \qquad t = 1,\dots,T.
$$

The slope $\hat\beta_i$ is stock $i$'s estimated beta — exactly Sam's beta from Ch 2.1, one per stock. In practice you estimate this on a **rolling window** (say the trailing 60 months) so beta is allowed to drift and, crucially, so the beta used to explain month $t$'s return is estimated from data *before* month $t$ (no peeking into the future). For your first pass through this lab, estimate beta on the full sample to keep the moving parts down; the rolling version is the extension.

**Pass 2 — period-by-period cross-sectional regressions.** Now flip the regression sideways. In *each* month $t$, treating the betas from Pass 1 as known regressors, run a single cross-sectional OLS across all stocks:

$$
r_{it} = \gamma_{0,t} + \gamma_{1,t}\,\hat\beta_i + \varepsilon_{it}, \qquad i = 1,\dots,N.
$$

This is one tiny regression per month — $N$ data points, one slope. Run it $T$ times and you get a *time series* of intercepts $\hat\gamma_{0,t}$ and slopes $\hat\gamma_{1,t}$, one pair per month. The slope $\hat\gamma_{1,t}$ answers, "in month $t$, how much extra return did each unit of beta buy?" Some months it is positive (high-beta stocks won), some months negative (they lost), and that month-to-month swing is enormous — it is dominated by whether the market happened to go up or down that month.

**Aggregate — the Fama–MacBeth estimator.** Collapse each time series to its mean. The Fama–MacBeth point estimates are simply the averages of the period-by-period coefficients:

$$
\hat\gamma_1^{\text{FM}} = \frac{1}{T}\sum_{t=1}^{T}\hat\gamma_{1,t}, \qquad
\hat\gamma_0^{\text{FM}} = \frac{1}{T}\sum_{t=1}^{T}\hat\gamma_{0,t}.
$$

And here is the move that makes the whole thing work — the **Fama–MacBeth standard error**. Because $\hat\gamma_1^{\text{FM}}$ is just the sample mean of the $T$ numbers $\hat\gamma_{1,t}$, its standard error is the ordinary standard error of a mean: the sample standard deviation of those numbers divided by $\sqrt{T}$.

$$
\widehat{\operatorname{se}}\big(\hat\gamma_1^{\text{FM}}\big)
= \frac{1}{\sqrt{T}}\sqrt{\frac{1}{T-1}\sum_{t=1}^{T}\big(\hat\gamma_{1,t} - \hat\gamma_1^{\text{FM}}\big)^2}.
$$

The Fama–MacBeth t-statistic is then $\hat\gamma_1^{\text{FM}} / \widehat{\operatorname{se}}(\hat\gamma_1^{\text{FM}})$, compared against a $t$-distribution with $T-1$ degrees of freedom.

### Why this fixes the cross-sectional correlation problem

Stare at what just happened, because it is genuinely clever. The disease was correlation *across stocks within a month*. The cure is to let each month produce a *single number*, $\hat\gamma_{1,t}$, that already digests all the within-month cross-sectional structure — including the common shock that correlated everyone's errors. Whatever correlation lived *inside* month $t$ is sealed up inside that one estimate. The only thing left to do is average those $T$ monthly numbers and quantify *their* scatter.

So the standard error is built from variation **across months**, not across stocks. The FM SE asks: "how much does the price of beta bounce around from month to month?" — and if the months are roughly independent of each other (a reasonable first approximation for monthly returns), that is a perfectly honest variance for the average. The within-month cross-sectional correlation that would have destroyed a pooled regression simply never enters the variance calculation, because we never treat two stocks in the same month as separate pieces of evidence about $\gamma_1$. One month, one vote.

**Connect this to Ch 2.4.** This is *exactly* the clustering idea, viewed from a different angle. Fama–MacBeth is, in effect, **clustering by time period.** Recall Petersen's (2009) taxonomy from Ch 2.4 §6: when the dominant correlation is a *time effect* — a common shock hitting all firms in a period — the right tool is to cluster by time, treating each period's block of correlated errors as one unit. Fama–MacBeth does precisely that, by the most literal route imaginable: it physically runs one regression per period and then aggregates, so each period contributes exactly one independent observation to the final variance. In fact, for a balanced panel the Fama–MacBeth standard error is known to be very close to the time-clustered standard error of a pooled regression (Petersen 2009). They are two implementations of the same economic judgment about where $\boldsymbol\Omega$'s off-diagonal blocks live.

The flip side is also straight from Ch 2.4, and you must internalize it: **Fama–MacBeth does *not* fix a firm effect.** If a stock's residuals are correlated *over time* (this year's mispricing predicts next year's), the FM standard error — which assumes the monthly slopes $\hat\gamma_{1,t}$ are roughly independent across $t$ — is too small, just as White SEs were too small in the presence of clustering. Petersen flagged this exactly. The honest fix is a Newey–West (HAC) correction applied to the time series of $\hat\gamma_{1,t}$, which you will add as an extension. For now, hold the headline: FM clusters by *time*, not by *firm*.

---

## Path A — the real thing on CRSP (run only on GMU infrastructure)

This is how you would pull the actual data on the WRDS Cloud or Hopper. **Do not run this off GMU infrastructure, and never copy CRSP rows into your notes or this repo** — licensed data stays read-only on Hopper/WRDS Cloud per Conventions §5. We show the pattern; we do *not* show any CRSP output, and we invent no CRSP numbers.

The `wrds` package opens an authenticated connection (your WRDS credentials live in a `~/.pgpass` file on the GMU machine, never in code). You query the **CRSP Monthly Stock File** (`crsp.msf`) for the permanent security identifier `permno`, the month-end `date`, and the holding-period return `ret`; you join the **CRSP/Ziman or Fama–French risk-free + market** series for the market proxy. Pin the snapshot.

```python
# === PATH A: real CRSP via WRDS — RUN ONLY ON GMU INFRASTRUCTURE ===
# Licensed data; read-only on Hopper/WRDS Cloud. Do not export rows.
import wrds

CRSP_SNAPSHOT = "2025-12-31"   # PINNED snapshot date — record this in your write-up

db = wrds.Connection(wrds_username="your_gmu_wrds_user")   # creds via ~/.pgpass, NOT in code

# Monthly stock returns: permno, date, ret. Restrict to common stocks (shrcd 10,11)
# on NYSE/AMEX/Nasdaq (exchcd 1,2,3) and a sane sample window.
crsp = db.raw_sql(
    """
    select a.permno, a.date, a.ret
    from crsp.msf as a
    left join crsp.msenames as b
        on a.permno = b.permno
       and b.namedt <= a.date
       and a.date <= b.nameendt
    where b.shrcd in (10, 11)
      and b.exchcd in (1, 2, 3)
      and a.date between '1965-01-01' and '2024-12-31'
    """,
    date_cols=["date"],
)

# Market & risk-free from Fama-French (also on WRDS): build excess returns.
ff = db.raw_sql(
    """
    select date, mktrf, rf
    from ff.factors_monthly
    where date between '1965-01-01' and '2024-12-31'
    """,
    date_cols=["date"],
)
db.close()

# Align month keys, drop missing returns, compute excess returns.
crsp = crsp.dropna(subset=["ret"]).copy()
crsp["month"] = crsp["date"].dt.to_period("M")
ff["month"] = ff["date"].dt.to_period("M")
panel = crsp.merge(ff[["month", "mktrf", "rf"]], on="month", how="inner")
panel["ret_excess"] = panel["ret"] - panel["rf"]      # stock excess return
panel = panel.rename(columns={"mktrf": "mkt_excess"})  # market excess return
# panel now has: permno, month, ret_excess, mkt_excess  -> feed into Pass 1 below.
```

From here, Path A and Path B share the *same* two-pass code, because we deliberately gave the synthetic panel the same column names. The only differences on real data: returns have missing values (handled by `dropna`), stocks enter and exit (the panel is unbalanced — require a minimum number of months per stock in Pass 1), and you must use a **rolling** beta to avoid look-ahead. Record `CRSP_SNAPSHOT` in your write-up; a CRSP pull is not reproducible without it, because CRSP revises historical data.

---

## Path B — the synthetic fallback (runs anywhere)

Now the version every student runs. We build a one-factor universe with a **known** risk premium, generate a CRSP-shaped panel, and then recover the planted premium with the exact two-pass machine. Because you set the truth, you can grade the procedure — this is the same "build the universe so you can check the tools" move as Lab 1.

The data-generating process is the CAPM itself: each stock $i$ has a fixed true beta $\beta_i$, the market delivers an excess return $r_{m,t}$ each month whose *long-run mean is the premium* $\lambda$, and a stock's return is $r_{it} = \gamma_0 + \beta_i\, r_{m,t} + e_{it}$ with idiosyncratic noise $e_{it}$.

```python
# === PATH B: synthetic CRSP-shaped panel with a KNOWN planted premium ===
N_STOCKS = 300
N_MONTHS = 360            # 30 years of monthly data
LAMBDA_TRUE = 0.006       # TRUE monthly market risk premium = 0.6%/month
GAMMA0_TRUE = 0.001       # TRUE zero-beta rate              = 0.1%/month

# Each stock's TRUE beta, drawn once and fixed forever.
true_beta = np.clip(rng.normal(1.0, 0.35, N_STOCKS), 0.1, 2.5)

# Realized market excess return each month; its sample MEAN is the premium.
mkt_excess = rng.normal(LAMBDA_TRUE, 0.025, N_MONTHS)

# CAPM data-generating process:  r_it = gamma0 + beta_i * mkt_t + e_it
idio = rng.normal(0.0, 0.06, size=(N_MONTHS, N_STOCKS))
ret = GAMMA0_TRUE + true_beta[None, :] * mkt_excess[:, None] + idio

# Reshape into a tidy panel with the SAME schema as Path A.
panel = pd.DataFrame({
    "permno":     np.tile(np.arange(N_STOCKS), N_MONTHS),
    "month":      np.repeat(np.arange(N_MONTHS), N_STOCKS),
    "ret":        ret.reshape(-1),
    "mkt_excess": np.repeat(mkt_excess, N_STOCKS),
})
panel.head()
```

You now hold a panel with columns `permno`, `month`, `ret`, `mkt_excess` and 300 × 360 = 108,000 stock-months — and, off to the side, the secret truth `true_beta` and `LAMBDA_TRUE` that the procedure is not allowed to see. Time to estimate.

---

## Step 1 — Pass 1: a time-series beta for every stock

**What to do.** For each `permno`, regress its `ret` on `mkt_excess` and keep the slope. That slope is $\hat\beta_i$. Merge the estimated betas back onto the panel so every stock-month row carries its stock's beta.

The cleanest way is a small function applied per group. You write the design matrix `[1, mkt_excess]` and solve the normal equations — use `np.linalg.lstsq`, which is the numerically stable way to compute $\hat{\boldsymbol\beta} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$ without forming the inverse by hand.

```python
def ts_beta(g):
    X = np.column_stack([np.ones(len(g)), g["mkt_excess"].values])
    b, *_ = np.linalg.lstsq(X, g["ret"].values, rcond=None)
    return b[1]                       # the slope = estimated beta

betas = panel.groupby("permno").apply(ts_beta, include_groups=False)
betas.name = "beta_hat"
panel = panel.merge(betas, left_on="permno", right_index=True)
```

**Check it against the planted truth.** Because this is synthetic data, you can do something you could *never* do on CRSP: compare your estimated betas to the real ones. They will not match exactly (idiosyncratic noise means each beta is estimated with error), but the correlation should be high.

```python
corr = np.corrcoef(betas.values, true_beta)[0, 1]
print(f"corr(estimated beta, true beta) = {corr:.3f}")   # expect ~0.93
```

**Think about it.** Why is the correlation not exactly 1.0? What single number in the data-generating process — if you cranked it up — would push that correlation toward 0.5, and what would that do to your final premium estimate downstream? (This is the *errors-in-variables* problem from Ch 2.5: betas estimated with noise are noisy regressors in Pass 2, which biases $\hat\gamma_1$ toward zero. Fama and MacBeth mitigated it by forming portfolios; you will meet that fix in the reflection questions.)

---

## Step 2 — Pass 2: a cross-sectional regression every month

**What to do.** For each `month`, run one OLS of `ret` on `beta_hat` across all stocks in that month. Keep both coefficients — the intercept $\hat\gamma_{0,t}$ and the slope $\hat\gamma_{1,t}$. The output is a $T \times 2$ table: one row per month.

```python
def xsec(g):
    X = np.column_stack([np.ones(len(g)), g["beta_hat"].values])
    b, *_ = np.linalg.lstsq(X, g["ret"].values, rcond=None)
    return pd.Series({"gamma0": b[0], "gamma1": b[1]})

gammas = panel.groupby("month").apply(xsec, include_groups=False)
print(gammas.describe())     # look at the spread of gamma1 across months
```

**Look at what you got.** Plot the time series of `gammas["gamma1"]`. You will see it swing wildly between positive and negative — in some months high-beta stocks crushed it, in others they got crushed. That month-to-month volatility is *not* noise to be embarrassed about; it is the realized market return showing through, and it is exactly the scatter that the Fama–MacBeth standard error is about to turn into honest uncertainty. The *average* of this jagged series is your premium; its *roughness* is your standard error.

---

## Step 3 — Aggregate into the Fama–MacBeth estimate and SE

**What to do.** Collapse each column of `gammas` to its mean (the FM point estimate), its standard error (sample std over $\sqrt{T}$), and form the t-stat. This is just "the standard error of a sample mean," applied to a series of regression coefficients.

```python
T = len(gammas)
fm_mean = gammas.mean()
fm_se   = gammas.std(ddof=1) / np.sqrt(T)     # FM standard error = sd(slopes)/sqrt(T)
fm_t    = fm_mean / fm_se

summary = pd.DataFrame({"FM estimate": fm_mean, "FM SE": fm_se, "FM t": fm_t})
print(summary.round(5))
print(f"\nplanted lambda = {LAMBDA_TRUE};  recovered gamma1 = {fm_mean['gamma1']:.5f}")
```

**What you should see.** With the seed and parameters above, the recovered `gamma1` lands near the planted `0.006` (you will get roughly `0.0055`), with an FM t-statistic comfortably above 3. The intercept `gamma0` is small. That is the whole replication in one table: a known premium, recovered from data, with a defensible standard error. Note that the recovered number is the *average realized* market excess return over your 360 months, which differs from the theoretical `0.006` by sampling error — and the FM SE is the size of that very gap. Re-run with a *different* seed and the point estimate wobbles by about one FM standard error, which is the best confirmation that the SE is calibrated.

---

## Step 4 — How to read the Fama–MacBeth standard error

You now have a number; make sure you can defend it. Three questions to ask of any FM standard error, all of them straight from Ch 2.4's "what does $\boldsymbol\Omega$ look like?" checklist.

First, **what variation is it built from?** The FM SE is the scatter of the *monthly slopes* over $\sqrt{T}$. So it is driven entirely by how many months you have and how much the price of beta bounces between them. Doubling the number of *stocks* per month barely tightens it (it just makes each $\hat\gamma_{1,t}$ a bit more precise); doubling the number of *months* tightens it like $1/\sqrt{T}$. This is the cluster-asymptotics lesson from Ch 2.4 §4.3 wearing a new hat: the FM SE's precision lives in $T$ (the number of time clusters), not in $N$ (the cross-section). If you have only 30 months, be as nervous as Priya was with 9 states — use the $t_{T-1}$ distribution, not the normal, and do not over-trust a borderline t-stat.

Second, **what correlation does it handle, and what does it miss?** It handles, automatically and exactly, the within-month cross-sectional correlation — the common market shock that moves all stocks together. It *misses* serial correlation in the slopes across months. If $\hat\gamma_{1,t}$ this month predicts $\hat\gamma_{1,t+1}$ next month (a firm-effect-style persistence), the plain FM SE is too small. The fix is Newey–West on the slope series; see the extension.

Third, **does it disagree with the naive number?** Run a pooled OLS of `ret` on `beta_hat` across the *entire* stacked panel and compare its (classical or even White) standard error on `beta_hat` to your FM SE. The pooled SE will be dramatically smaller — because it pretends your 108,000 stock-months are 108,000 independent observations, when on the dimension that matters they are closer to 360. That disagreement *is* the diagnostic, exactly as in Ch 2.4 §3.5: the gap between the lying t-stat and the honest one.

```python
# The naive comparison: pooled OLS treats every stock-month as independent.
import statsmodels.formula.api as smf
pooled = smf.ols("ret ~ beta_hat", data=panel).fit()
print("pooled OLS SE on beta_hat:", round(pooled.bse['beta_hat'], 6))
print("Fama-MacBeth SE on gamma1:", round(fm_se['gamma1'], 6))
# Expect the pooled SE to be far too small -> a wildly inflated t-stat.
```

---

## You're done when…

Tick every box before you call this lab finished:

- [ ] Your conda env builds and the Path B block runs top-to-bottom with no errors on a fresh kernel.
- [ ] Pass 1 produces one `beta_hat` per `permno`, and `corr(beta_hat, true_beta)` is around 0.9.
- [ ] Pass 2 produces a $T \times 2$ table of monthly `gamma0`, `gamma1`, and you have *plotted* the `gamma1` series and seen it swing.
- [ ] The aggregated FM `gamma1` lands near the planted `LAMBDA_TRUE = 0.006`, with FM t-stat above ~3.
- [ ] You computed the naive pooled-OLS SE and can state, in one sentence, why it is far too small.
- [ ] You can explain out loud why Fama–MacBeth is "clustering by time" and why it does *not* fix a firm effect.
- [ ] (Path A, on GMU infra only) You can describe the CRSP query, the pinned snapshot date, and the licensed-data rule — without any CRSP numbers leaving Hopper.

---

## Reflection questions

1. **One vote per month.** Explain, in two or three sentences, why running one cross-sectional regression per month and then averaging the slopes neutralizes the within-month correlation that would sink a single pooled regression. What assumption about the *months* does the FM standard error rely on instead?

2. **Clustering connection.** In Ch 2.4 §6, Petersen's taxonomy says: time effect → cluster by time; firm effect → cluster by firm; both → two-way. Where does Fama–MacBeth sit in that taxonomy, and what kind of correlation would make you *distrust* a plain FM standard error? Name the specific fix.

3. **Errors-in-variables.** Your Pass-1 betas are estimated with noise, then used as a regressor in Pass 2. From Ch 2.5, what does measurement error in a regressor do to its coefficient, and in which direction does it push $\hat\gamma_1$? Fama and MacBeth grouped stocks into 20 beta-sorted **portfolios** and used portfolio betas instead of individual ones. Why does forming portfolios reduce the measurement-error problem? (Hint: what happens to idiosyncratic noise when you average 15 stocks?)

4. **Look-ahead bias.** The Path B code estimates each stock's beta on the *full* sample, then uses it to explain returns from that same sample. Why is this cheating on real data, and how does a *rolling trailing-window* beta fix it? Sketch the change to the Pass-1 code.

5. **Reading the premium.** Suppose your recovered $\hat\gamma_1^{\text{FM}}$ comes out at $0.005$ with an FM SE of $0.0015$ over $T = 360$ months. Write the FM t-statistic, state the degrees of freedom you would use, and translate the estimate into a plain-English annualized risk premium. Is it consistent with the planted $0.006$?

---

## Extensions (pick one)

- **Rolling betas (the honest version).** Replace full-sample Pass 1 with a trailing 60-month rolling regression, so the beta used in month $t$ is estimated from months $t-60$ to $t-1$. Re-run and confirm the premium survives. This is mandatory before you would ever report a Path A (CRSP) result.

- **Newey–West on the slopes.** The plain FM SE assumes the monthly slopes are serially uncorrelated. Apply a Newey–West (HAC) correction to the time series `gammas["gamma1"]` (regress it on a constant with `cov_type="HAC", cov_kwds={"maxlags": 6}` in `statsmodels`). Compare to the plain FM SE. If they barely differ, your slopes were roughly independent and FM was fine; if HAC is larger, you had persistence FM missed — exactly the firm-effect blind spot from Ch 2.4.

- **Add a second factor.** Generate a size factor with its own planted premium, give each stock a loading on it, and run a *two-regressor* Pass 2 (`ret ~ beta_hat + size_loading`). Recover both premia. This is the multi-factor Fama–MacBeth that underlies every modern asset-pricing test.

---

## A short note on Fama–MacBeth and Petersen (2009) clustering

It is worth ending where Ch 2.4 ended, because Fama–MacBeth is the historical ancestor of the entire clustering literature. Fama and MacBeth invented their procedure in 1973 — a decade before White's robust SEs (1980) and three decades before Petersen's panel taxonomy (2009) — precisely to handle the cross-sectional correlation in stock returns without any of the sandwich machinery, which did not yet exist. Their solution was operational genius: don't estimate the $N \times N$ error covariance, just *side-step* it by letting each period speak once.

Petersen (2009) later placed Fama–MacBeth inside the unified framework you learned in Ch 2.4. His verdict is the practical bottom line, and you should carry it out of this lab: **Fama–MacBeth is essentially clustering by time period, and it is the right tool when a common time shock is the dominant source of correlated errors — the canonical situation for cross-sectional return regressions.** It produces standard errors very close to time-clustered standard errors on the same panel. But Petersen's warning is just as important: when the data also has a *firm effect* — residuals correlated within a stock across time — Fama–MacBeth understates the standard error, just as White SEs understate it under any clustering. There, you need clustering by firm, or two-way clustering, or the Newey–West correction on the slope series you tried in the extension.

The deeper lesson is the one the whole of Week 2 has been driving at, from the Gauss–Markov theorem through the sandwich and now to this lab: **getting the point estimate is the easy half; getting its uncertainty right is the half that decides whether your finding is real.** Fama and MacBeth understood that in 1973, built a procedure around it, and handed you a tool you will use unchanged on real CRSP data the first time you sit at a Hopper terminal.
