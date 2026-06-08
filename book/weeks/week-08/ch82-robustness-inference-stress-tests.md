# Ch 8.2 — Robustness & Inference Stress-Tests

In the last chapter you ran your pre-registered specification and then surrounded it with a specification curve — every defensible analytic choice, plotted, so a reader can see that your headline number is not an artifact of one lucky fork in the garden. That chapter was about *analytic-choice multiplicity*: the many regressions you *could* have run. This chapter is about something different and, frankly, more adversarial. Here you stop varying your choices and start attacking your *inference itself*. The question is no longer "is my estimate stable across reasonable specifications?" It is "is my estimate even real, or have I been fooled — by correlated errors that make my t-statistic lie, by a pattern that would show up even where no treatment happened, by a knob I tuned until the stars appeared, by a family of outcomes I tested all at once, or by a confounder I never measured?"

The discipline this chapter teaches has an ugly name and a beautiful purpose: you are going to try to **kill your own result**. Not soften it, not hedge it — kill it. You will design the tests a hostile referee would design, run them on yourself first, and report what they find whether or not you like the answer. This is the single most important professional habit in empirical work, and it is the one that separates a paper a reader *trusts* from one they merely *read*. The reveal-the-trick promise of this whole book gets turned, one last time, on you: the trick you are now revealing is the one you might be playing on yourself.

Here is the spine of the chapter, so you have it before the machinery. In Chapter 7.5 you wrote an identification memo with a threats-and-responses table — four columns, the third of which was *"what we do about it."* **Column 3 was a set of promises.** This chapter is where those promises come due. Each robustness test below is the operationalization of one row's column 3: a placebo for the "this pattern is spurious" threat, a wild cluster bootstrap for the "few clusters break my standard errors" threat, an Oster δ for the "unobserved confounder" threat. So as you read, keep your own threats table open. Every test here is an answer you owe to a row you already wrote.

We will continue with Maya's project from Week 7: the staggered difference-in-differences on HMDA, asking whether state **fair-lending examination** programs reduced the county-level minority–white gap in mortgage-denial rates.[^gaosun] Her identifying assumption is per-cohort parallel trends; her primary estimate is a Callaway–Sant'Anna overall ATT against never- and not-yet-treated controls (Chapter 4.2), clustered by state. Suppose she ran it and got an ATT of roughly **−1.4 percentage points** — the examination programs appear to *shrink* the denial gap by 1.4pp — with a state-clustered standard error of about 0.55, so a t of about 2.5 and three stars on the table. A good day. Now we spend the chapter trying to make that number die.

---

## 1. Alternative standard errors: is the t-statistic telling the truth?

Start with the cheapest attack, because it is also the most common cause of a result that evaporates: the standard error is too small, so the t-statistic is too big, and the significance is an illusion. Recall the central lesson of Chapter 2.4: **OLS gives you the right point estimate even when the errors misbehave; what misbehaving errors corrupt is the *variance* of that estimate — the standard error, hence the t-stat, hence the p-value.** A robustness check on standard errors does not touch your $\hat{\beta}$ at all. It re-asks the question "how uncertain is this number?" under a less convenient — and often more honest — set of assumptions about how the errors are correlated.

The sandwich estimator from Chapter 2.4 was the unifying object: $\widehat{\operatorname{Var}}(\hat{\boldsymbol\beta}) = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\hat{\boldsymbol\Omega}\mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}$, where the only thing that changes between SE flavors is what you assume about the error variance-covariance matrix $\boldsymbol\Omega$. Classical SEs assume $\boldsymbol\Omega = \sigma^2\mathbf{I}$ — errors all the same size and uncorrelated. Heteroskedasticity-robust SEs (HC1/HC2/HC3) let the diagonal of $\boldsymbol\Omega$ vary. Cluster-robust SEs let $\boldsymbol\Omega$ have correlated blocks. HAC (Newey–West) lets errors be correlated across time within a unit, with the correlation fading over a bandwidth. The robustness exercise is to **re-run your headline estimate under each plausible flavor and watch the standard error move.**

### What it probes

Three distinct threats, all of which inflate your significance if you ignore them.

**The clustering level.** This is the one that bites Maya hardest, and the question is deceptively simple: *at what level are the errors correlated?* In Chapter 2.4 you learned the Petersen (2009) rule — cluster at the level of the correlation, and if treatment varies at the state level you must cluster at the state level, because the Moulton-style inflation factor $1+(n-1)\rho_x\rho_\varepsilon$ shows that within-state error correlation, combined with a treatment that is constant within state, can multiply the true variance many times over. The robustness check is to try the *defensible alternatives* and see if the verdict survives. Maya clusters by state in her primary spec. A referee might ask: what about clustering by county (her unit of observation)? Or two-way, by state *and* by year, since a national shock to mortgage markets in 2008 correlates errors across all states in that year (Cameron, Gelbach & Miller 2011)?[^cgm2011] The honest move is to report a small table:

| Clustering | SE | t | 95% CI |
|---|---|---|---|
| Classical | 0.18 | 7.8 | [−1.75, −1.05] |
| County (unit) | 0.31 | 4.5 | [−2.01, −0.79] |
| **State (primary)** | **0.55** | **2.5** | **[−2.48, −0.32]** |
| State + Year (two-way) | 0.61 | 2.3 | [−2.60, −0.20] |

Read this top to bottom and you see the whole drama of Chapter 2.4 in one column. The classical SE is a fantasy — it treats every county-year as independent information and reports a t of 7.8 that no one should believe. As you move to coarser, more honest clustering, the SE roughly triples and the t falls from absurd to merely solid. The right reading: Maya's result *passes*, because even under the most conservative defensible clustering (two-way) the interval still excludes zero. Had the two-way row crossed zero, the honest report would be "significant under state clustering but not under two-way clustering" — and then the result is *fragile*, and you say so.

**Serial correlation over time.** Maya's panel runs over many years, and denial gaps are sticky — a county high this year tends to be high next year. That is exactly the within-unit serial correlation that the HAC / Newey–West estimator (Chapter 2.4) was built for, and that Bertrand, Duflo & Mullainathan (2004) showed will, if ignored, give a DiD a false-positive rate near 45% instead of 5%. We will treat their specific placebo construction in §2; for the SE flavor itself, the rule is that cluster-robust SEs that cluster by the unit *already* absorb arbitrary within-unit serial correlation (that is the whole point of the block-diagonal $\boldsymbol\Omega$), so a panel clustered by state is generally serially-correlation-robust without a separate HAC step. HAC is the tool when you have *one* long time series and cannot cluster.

### The hard case: few clusters, and the wild cluster bootstrap

Now the threat that the table above silently hides, and the one Maya wrote into her threats table as "few-treated-cluster inference." Cluster-robust standard errors lean on an asymptotic argument that needs the *number of clusters* to be large — the rule of thumb from Chapter 2.4 was 30 to 50. The danger is subtle: with few clusters, the cluster-robust SE is itself **downward-biased and noisy**, so the t-statistic does not follow the t-distribution you compare it against, and you over-reject — you find significance that is not there. Maya has 50 states, which sounds fine, but the relevant count for a treatment effect is closer to the number of *treated* clusters, and if only, say, eight states ever adopted an examination program, her effective cluster count is dangerously small. This is the same fragility that made Card & Krueger's single-treated-state design (Chapter 4.1) demand permutation inference.

The fix is the **wild cluster bootstrap** (Cameron, Gelbach & Miller 2008),[^cgm2008] which you met by name in Chapter 2.4. The intuition is the trick worth revealing. An ordinary bootstrap resamples *observations*; that breaks the within-cluster correlation you are trying to respect. A *cluster* bootstrap resamples whole clusters; with few clusters that does not give you enough distinct resamples. The wild cluster bootstrap does something cleverer: it keeps the clusters and the regressors exactly as they are, and instead **flips the sign of each cluster's residuals at random** — multiplying every residual in a cluster by $+1$ or $-1$ with equal probability (the Rademacher weights) — to manufacture a distribution of the test statistic *under the null*. You re-impose the null hypothesis ($\beta = 0$) when computing the residuals, perturb, re-estimate thousands of times, and read your real t-statistic's position in that bootstrapped distribution to get a p-value. It is, in spirit, the same permutation logic as a placebo test: build the distribution of "what this statistic looks like when nothing is going on," then locate your real number in it.

```python
# Wild cluster bootstrap for the treatment coefficient, restricted (null-imposed) residuals.
# Pedagogical implementation; in practice use a vetted package (e.g., wildboottest / fwildclusterboot).
import numpy as np
import statsmodels.formula.api as smf

def wild_cluster_bootstrap(df, formula, param, cluster_col, B=1999, seed=8):
    rng = np.random.default_rng(seed)
    # 1) Unrestricted fit -> the t-stat we actually observed.
    fit = smf.ols(formula, data=df).fit(
        cov_type="cluster", cov_kwds={"groups": df[cluster_col]}
    )
    t_obs = fit.params[param] / fit.bse[param]

    # 2) Restricted fit: impose H0 by dropping the tested regressor, keep its residuals.
    restricted_formula = formula.replace(f" + {param}", "").replace(f"{param} + ", "")
    r_fit = smf.ols(restricted_formula, data=df).fit()
    resid_hat = r_fit.resid.to_numpy()
    fitted_0  = r_fit.fittedvalues.to_numpy()
    yname = formula.split("~")[0].strip()

    clusters = df[cluster_col].to_numpy()
    uniq = np.unique(clusters)
    t_boot = np.empty(B)
    for b in range(B):
        # 3) One Rademacher (+/-1) draw PER CLUSTER, broadcast to its rows.
        signs = rng.choice([-1.0, 1.0], size=uniq.size)
        w = np.empty_like(resid_hat)
        for s, c in zip(signs, uniq):
            w[clusters == c] = s
        df_b = df.copy()
        df_b[yname] = fitted_0 + w * resid_hat        # bootstrap outcome under H0
        fb = smf.ols(formula, data=df_b).fit(
            cov_type="cluster", cov_kwds={"groups": df_b[cluster_col]}
        )
        t_boot[b] = fb.params[param] / fb.bse[param]

    # 4) Two-sided bootstrap p-value: how often |t_boot| >= |t_obs|.
    p = (np.sum(np.abs(t_boot) >= np.abs(t_obs)) + 1) / (B + 1)
    return t_obs, p
```

### How to read pass/fail, and honesty

**Pass:** the wild-cluster p-value is small (and roughly agrees with your conventional clustered p-value). Your significance was not an artifact of too few clusters. **Fail:** the wild-cluster p-value is much larger — say your conventional table said $p = 0.01$ but the bootstrap says $p = 0.18$. That is the few-clusters illusion exposed, and the honest report is brutal and short: *"The point estimate is −1.4pp, but with few treated clusters, inference is too imprecise to reject zero; we report the result as suggestive, not significant."* You do not get to keep the three stars from the conventional SE once the bootstrap has told you they are fake. The whole reason the wild cluster bootstrap is in your threats table is that, for designs with few treated clusters, **it, not the default clustered SE, is the honest inference.** If they disagree, believe the bootstrap.

---

## 2. Placebo tests: would this pattern appear where it can't be real?

The second attack is the most intuitive and, when it fails, the most damning. A **placebo test** runs your exact analysis on a setting where, by construction, *there can be no treatment effect* — a fake treatment date, a fake treatment unit, a fake outcome — and checks that you correctly find nothing. The logic is the logic of a control group raised one level: if your method finds an "effect" where none can exist, then the "effect" it found in your real analysis is suspect too, because your method is manufacturing patterns out of whatever structure is in the data. Recall the placebo permutation inference of Chapter 4.1 (assign Card & Krueger's treatment to every other state in turn) and the Bertrand–Duflo–Mullainathan placebo of Week 5: this is the same idea, now a standard weapon in your battery.

### Fake treatment dates (the in-time placebo)

Maya picks a year *well before* any state actually adopted an examination program — say, three years before the earliest real adoption — and pretends the programs switched on then, leaving the true post-period out entirely so the fake effect cannot be contaminated by the real one. She re-runs the entire Callaway–Sant'Anna estimator on this fictional timing. **What it probes:** whether her estimator detects a "treatment effect" purely from the trend structure of the data — exactly the differential-pre-trend threat that sits in row one of her table. If adopting states were already on a different denial-gap trajectory, a fake treatment placed in the pre-period will *catch* that trajectory and report a spurious effect.

**Pass:** the placebo ATT is small and statistically indistinguishable from zero. This is real, if asymmetric, support for parallel trends — it is the same evidence as a flat event-study lead, dressed as a single number. **Fail:** the placebo ATT is itself large and significant, perhaps even similar in size to the real estimate. That is close to fatal: it means your method finds "1.4pp effects" in years when nothing happened, so the 1.4pp it found in the real years carries no special weight. There is no spin that survives a failed in-time placebo; the honest move is to conclude the design cannot separate the treatment from a pre-existing trend, and either redesign (a cleaner control group, a shorter window) or report the result as uninterpretable.

### Fake treatment units (the in-space placebo / permutation)

Now permute *units* instead of time. Assign fake "adoption" to states that never actually adopted, re-estimate, and repeat across many random reassignments to build a distribution of placebo effects. Locate the *real* effect in that distribution. **What it probes:** whether an effect of Maya's magnitude shows up routinely when treatment is assigned at random — the synthetic-control-style inference of Chapter 4.4, and the right inference when clusters are too few for the t-approximation. **Pass:** the real effect sits in the extreme tail of the placebo distribution (say, more extreme than 95% of placebos), so a permutation p-value below 0.05. **Fail:** the real effect is buried in the middle of the placebo cloud — plenty of randomly-assigned "treatments" produce effects as big — so it is not distinguishable from noise. The placebo distribution *is* the honest summary of uncertainty here; if your real number is unremarkable within it, say so plainly.

### Fake outcomes (the placebo outcome)

Pick an outcome the treatment should have *no* plausible channel to move, but that shares the same data structure — Maya might use the denial gap for a loan category exempt from fair-lending examination, or a gap that the program's mechanism cannot touch. **Pass:** no effect on the placebo outcome, which rules out a broad confounder (a general economic shock to adopting states) that would have moved *everything*. **Fail:** the program "moves" an outcome it cannot mechanically affect — a tell that something other than the program is driving adopting states, and your effect is riding on it.

The unifying intellectual-honesty point: a placebo test is a *prediction your theory makes about where you should find nothing*, and reporting a failed placebo is not optional. Referees run placebos in their heads as they read; a paper that omits the obvious one reads as evasive, and a paper that reports a failed one and grapples with it reads as honest. You ran the placebo to find out the truth, not to collect a pass.

---

## 3. Sensitivity analysis: which knobs is my result hostage to?

Every analysis has knobs — tuning parameters and judgment calls that are individually defensible but, taken together, give you enormous freedom to land on a number you like. **Sensitivity analysis** wiggles each knob across its defensible range and reports how much the estimate moves. It overlaps with the specification curve of Chapter 8.1, but with a sharper question: not "is my result stable across *all* forks?" but "is my result hostage to *this particular* arbitrary choice?" Three knobs matter most.

### Bandwidth (the RD knob)

This one is for the regression-discontinuity crowd (Chapter 4.3). An RD estimate is a comparison of units just above and just below a cutoff, and "just" is set by a **bandwidth** $h$: include units within $h$ of the threshold. Too wide and you import units far from the cutoff whose comparison is contaminated by the very confounding RD was meant to avoid; too narrow and you have almost no data and a wild, imprecise estimate. The bias–variance trade-off is exactly the one the Calonico–Cattaneo–Titiunik robust bias-corrected procedure automates, but you must still *show* the estimate is not an artifact of one bandwidth. The standard display is a **sensitivity plot**: the RD coefficient and its confidence band as a function of $h$, from half the optimal bandwidth to twice it. **Pass:** the estimate is flat and stays significant across the range — the result is not a bandwidth artifact. **Fail:** the estimate swings wildly, or is significant only in a narrow window of $h$ around the value you happened to pick. That is a result tuned into existence, and a referee who sees a single bandwidth with no sensitivity plot assumes the worst.

### Controls (the specification knob)

How does the estimate move as you add or drop control variables? This is more subtle than "more controls is more rigorous," and §4's Oster logic will make the subtlety precise. For now the diagnostic is **coefficient stability**: report your estimate with no controls, with your primary controls, and with an aggressive battery of extra controls. **Pass with a caveat:** the coefficient barely moves as controls are added. That is *suggestive* of robustness — but read §4 before you celebrate, because stability alone can be a trap. **Fail:** the coefficient halves, or flips sign, when you add a control. Then the result depends entirely on a modeling choice, and you must justify *which* control set is correct on substantive grounds, not pick the one that keeps the stars. A special trap: never "control for" a variable that is itself an *outcome* of the treatment (a post-treatment variable / bad control), because that bleeds the effect away and the resulting instability is an artifact of the bad control, not evidence against your result.

### Sample and winsorizing (the data knob)

Finally, the choices buried in data construction (Week 7's Chapter 7.4). Does the result survive dropping the most extreme observations? Financial data is fat-tailed, and a single county or firm-year can move a coefficient; the conventional defense is **winsorizing** — capping each variable at, say, its 1st and 99th percentiles so extreme values are pulled to the cap rather than deleted. Sensitivity here means re-running at 0% (raw), 1%, and 5% winsorizing, and also dropping defensible subsamples (excluding the crisis years 2008–2009, excluding the largest state, excluding the earliest adoption cohort). **Pass:** the estimate is stable across these. **Fail:** the result lives or dies on a handful of outliers, or on including one influential state, or on the crisis window. Then the honest claim is narrower than the one you wanted: "the effect holds outside the financial crisis but is not separately identified within it," for instance. Narrowing the claim to what the data actually support is not a defeat; it is the entire job.

---

## 4. Multiple-testing corrections, done right

Maya does not have one outcome. Like most real projects she has a *family*: the denial gap overall, but also the gap in approval *rates*, in interest-rate spreads, in loan amounts, broken out by minority subgroup. Suppose she tests eight outcomes and two come back significant at the 5% level. How impressed should you be? Recall the hard lesson of Chapter 1.5: **the false-positive rate of a single test does not protect a search across many tests.** If all eight outcomes were truly null, the chance that *at least one* clears the 5% bar is $1 - (1-0.05)^8 \approx 0.34$ — a one-in-three chance of a false "discovery" from pure noise. Run enough outcomes and a significant result is *expected*, not impressive. Maya owes the reader an adjustment for the size of her family.

The two corrections you must know — both named in Chapter 1.5 — answer two different questions, and using the wrong one is a common and consequential error.

**Bonferroni** controls the **family-wise error rate (FWER)**: the probability of *even one* false positive across the whole family. The rule is brutal and simple — test each of $m$ hypotheses at $\alpha/m$ instead of $\alpha$ (equivalently, multiply each p-value by $m$ and cap at 1). For Maya's eight outcomes, the per-test bar becomes $0.05/8 = 0.00625$. **When to use it:** when a single false positive is costly and you must be able to say "*every* starred result here is almost surely real" — a drug-approval mindset. **The cost:** Bonferroni is conservative to the point of bluntness; with a large family it kills statistical power, and you will fail to flag real effects (Type II errors) to buy near-certainty against any false one.

**Benjamini–Hochberg (1995)** controls the **false discovery rate (FDR)**: the *expected fraction* of your declared discoveries that are false. This is usually the more sensible target when you are screening many candidate signals and can tolerate that, say, 5% of your "finds" are flukes — the natural posture in finance and in genomics, where BH was born. The procedure is a ranked one and worth seeing in full:

1. Order your $m$ p-values from smallest to largest: $p_{(1)} \le p_{(2)} \le \dots \le p_{(m)}$.
2. Find the largest rank $k$ such that $p_{(k)} \le \frac{k}{m}\,\alpha$.
3. Reject (declare significant) all hypotheses with rank $\le k$.

The genius is the *sliding* bar: the smallest p-value is held to the strict Bonferroni-like threshold $\frac{1}{m}\alpha$, but each successive p-value gets a more lenient bar, so a cluster of moderately-small p-values can reinforce each other into significance in a way Bonferroni would never allow. Here is Maya's family worked, with $m=8$, $\alpha=0.05$:

| Outcome | $p$ | rank $k$ | BH bar $\frac{k}{8}(0.05)$ | $\le$ bar? |
|---|---|---|---|---|
| Denial gap (primary) | 0.004 | 1 | 0.00625 | yes |
| Approval-rate gap | 0.011 | 2 | 0.01250 | yes |
| Rate-spread gap | 0.030 | 3 | 0.01875 | no |
| Loan-amount gap | 0.041 | 4 | 0.02500 | no |
| Subgroup A gap | 0.20 | 5 | 0.03125 | no |
| Subgroup B gap | 0.33 | 6 | 0.03750 | no |
| Subgroup C gap | 0.51 | 7 | 0.04375 | no |
| Subgroup D gap | 0.78 | 8 | 0.05000 | no |

Find the largest $k$ with $p_{(k)} \le \frac{k}{8}(0.05)$: that is $k=2$ (0.011 ≤ 0.0125). BH then declares the *two* smallest — denial gap and approval-rate gap — significant, and the rest not. Note the rate-spread gap at $p=0.030$, which cleared the naive 5% bar, does *not* survive: once you account for having looked at eight outcomes, it is no longer distinguishable from the noise you would expect from eight draws. Bonferroni here would have required $p \le 0.00625$ and kept *only* the primary denial gap; BH keeps two. That gap between them is the FWER-vs-FDR trade-off made concrete.

**How to read pass/fail and stay honest.** The non-negotiable rule: **declare your family in advance** — ideally in the pre-analysis plan of Chapter 7.3 — so you cannot gerrymander it after the fact. The cardinal sin is to run twenty outcomes, find one significant, and report it *alone* as if it were the only test you ran; that is the garden of forking paths from Chapter 1.5, and the correction exists precisely to disarm it. The honest report names $m$, names the correction, and states the surviving set: *"Of the eight pre-specified outcomes, two survive Benjamini–Hochberg FDR control at 5%."* If your headline result is the one that *fails* to survive correction, you say so, and your contribution becomes "suggestive on the secondary outcomes, robust only on the primary." A reader trusts a corrected family far more than an uncorrected lone star.

---

## 5. Oster (2019) δ: how much would the unobservable confounder have to matter?

Now the deepest attack, and the one with the most beautiful logic, because it confronts the threat that *cannot be tested directly*: an omitted variable you never measured. Maya's weakest design assumption — the one in her threats table with the residual concern "unobserved creditworthiness differences could still shift the gap" — is selection on unobservables. No balance table can reach it, because the confounder you fear is by definition the one not in the table. So the question can never be "is there an unobserved confounder?" (there always could be). Oster (2019) reframes it into a question you *can* answer: **how strong would selection on unobservables have to be, relative to the selection on observables you can see, to explain away your entire result?** If the answer is "implausibly strong — stronger than the observables, which you already control for," your result is robust to the threat you cannot test. If the answer is "barely as strong as the observables," it is fragile.

### The coefficient-stability-plus-R² logic

The argument builds on the coefficient-stability intuition from §3, but fixes its fatal flaw. The naive idea is: *if my coefficient barely moves when I add controls, it must be robust to omitted variables too.* Oster shows this is **only half the story, and the missing half is the $R^2$.** Adding a control can leave the coefficient stable for two opposite reasons: either the control truly does not matter (genuinely reassuring), or the control matters but is nearly uncorrelated with treatment (the coefficient is stable but the controls explain a lot of *outcome* variance — and an unobservable as predictive as those controls could still move the coefficient a lot). Coefficient movement is only meaningful *relative to how much explanatory power the controls added.* A coefficient that stays put while $R^2$ jumps from 0.10 to 0.55 is far more reassuring than one that stays put while $R^2$ barely rises — because in the first case the controls were powerful and the coefficient shrugged them off, while in the second the controls were toothless and proved nothing.

Oster formalizes this with three ingredients you read off two regressions:

- The **uncontrolled** regression: coefficient $\hat\beta_0$ and $R^2$ value $\tilde R_0$ (Maya: treatment with no covariates).
- The **controlled** regression: coefficient $\hat\beta_1$ and $R^2$ value $\tilde R_1$ (Maya: her full covariate-conditional spec).
- A **maximum $R^2$**, $R_{\max}$: the $R^2$ a hypothetical regression on treatment *plus all observables and all unobservables* would attain. You cannot observe it, so you assume it — Oster's evidence-based default is $R_{\max} = 1.3\,\tilde R_1$, capped at 1.0.

The key parameter is $\delta$ (delta): the **ratio of selection on unobservables to selection on observables.** $\delta = 1$ means the unobservables are *exactly as related* to treatment as the observables you control for — the natural benchmark, because it says "the stuff I couldn't measure is no more confounding than the stuff I could." $\delta = 2$ means twice as confounding; $\delta = 0.5$ means half. There are two ways to use it, and you should report both.

**Use 1 — the bounding set.** Fix $\delta$ at the benchmark $\delta = 1$ and solve for the **bias-adjusted coefficient** $\beta^*$: where your estimate would land if unobservable selection were exactly as strong as observable selection. This gives an identified set, conventionally the interval $[\hat\beta_1, \beta^*]$. **Pass:** the set excludes zero — even with confounding as strong as your observables, the effect stays the same sign and away from zero. **Fail:** the set contains zero — plausible unobserved confounding could fully explain your result.

**Use 2 — the δ that kills it.** Set $\beta^* = 0$ and solve for the $\delta$ that would be required to drive your effect to zero. Call it $\hat\delta$. **Pass:** $\hat\delta \ge 1$ (Oster's heuristic threshold), meaning an unobservable would have to be *at least as confounding as everything you observed* to explain away the result — usually an implausible thing to assert, since researchers typically control for the most obvious confounders, so the leftovers should be *weaker*, not stronger. The larger $\hat\delta$ is, the more robust. **Fail:** $\hat\delta < 1$ — a confounder weaker than your observables could erase the effect, so the result is fragile.

```python
# Oster (2019) delta: how much stronger must unobservable selection be than
# observable selection to drive the treatment coefficient to zero?
def oster_delta(beta0, R0, beta1, R1, Rmax=None, beta_target=0.0):
    """beta0,R0 = uncontrolled coef & R^2; beta1,R1 = controlled coef & R^2."""
    if Rmax is None:
        Rmax = min(1.3 * R1, 1.0)          # Oster's evidence-based default
    num = (beta1 - beta_target) * (R1 - R0)
    den = (beta0 - beta1) * (Rmax - R1)
    return num / den                        # delta to reach beta_target (default 0)

# Maya: coef moves only modestly (-2.2 -> -1.4) while R^2 climbs a lot (0.08 -> 0.42) => robust.
delta = oster_delta(beta0=-2.2, R0=0.08, beta1=-1.4, R1=0.42)
print(f"delta to explain away the effect: {delta:.2f}")   # ~ 4.72  (>> 1 : robust)
```

### Reading Maya's δ, and the honesty rule

Plug in Maya's numbers: an uncontrolled ATT of −2.2 that moves only modestly to −1.4 when controls are added, while $R^2$ climbs a lot, from 0.08 to 0.42. The coefficient moved a little *but* the controls explained a great deal — and it is that contrast that matters — so $\hat\delta \approx 4.7$. An unobservable would have to be roughly **four to five times** as correlated with examination adoption as Maya's full set of applicant-composition controls to explain away the effect. Since she already controls for the obvious confounders, an unobservable that potent is hard to argue for, and she can write: *"The result is robust to selection on unobservables under the Oster (2019) test: an omitted confounder would have to be 4.7 times as important as the rich observables to nullify the estimate ($\hat\delta = 4.7 \gg 1$, with $R_{\max} = 1.3\tilde R_1$)."*

Three honesty rules specific to Oster, because the test is easy to abuse:

1. **Report $R_{\max}$ and defend it.** $\hat\delta$ is mechanically sensitive to $R_{\max}$: assume the controls explain everything ($R_{\max} = \tilde R_1$) and the test is vacuous; assume $R_{\max} = 1$ and it is harshest. State which you used (default $1.3\tilde R_1$) and show how $\hat\delta$ moves if you push $R_{\max}$ to 1. A δ reported without its $R_{\max}$ is uninterpretable.
2. **δ is not a p-value.** It does not measure statistical significance; it measures robustness to a *specific, untestable* threat. A result can be wildly significant and have $\hat\delta = 0.3$ (fragile to confounding); another can have a modest t and $\hat\delta = 5$ (precise enough, hard to confound). Report both kinds of evidence — they answer different questions.
3. **A failing δ is information, not an embarrassment.** If $\hat\delta = 0.4$, the test has told you, honestly, that a confounder weaker than your observables could be the whole story. That belongs in your limitations, stated plainly: *"We cannot rule out that unobserved selection drives the result; an omitted variable only 0.4 times as important as our controls would suffice."* This is the §5 honesty of the identification memo, made quantitative — you found the project's vulnerability before a referee did, and you said so.

---

## 6. Assembling the battery, and what a survivor looks like

Step back and see the structure. Each test in this chapter answered a row of the threats table you wrote in Chapter 7.5:

| Threat (from your Ch 7.5 table) | The stress-test (this chapter) | Pass looks like |
|---|---|---|
| Differential pre-trend | In-time placebo (fake date in pre-period) | Placebo ATT ≈ 0 |
| Few treated clusters | Wild cluster bootstrap; in-space placebo | Bootstrap p agrees / real effect in tail |
| Errors correlated across units or time | Alternative clustering levels; HAC | CI excludes zero under conservative clustering |
| Result tuned to a knob | Sensitivity to bandwidth / controls / winsorizing | Estimate flat across defensible range |
| Cherry-picked from a family of outcomes | Bonferroni / Benjamini–Hochberg | Result survives the correction you pre-specified |
| Unobserved confounder | Oster (2019) δ | $\hat\delta \ge 1$; bounding set excludes zero |

A result that survives this battery is not *proven* — nothing observational ever is, as Chapter 7.5 hammered — but it is *credible* in the precise sense the identification memo demanded: you tried every attack a referee would try, you tried them on yourself first, and the number held. That is the strongest claim empirical work can honestly make.

And the converse is the real lesson of this chapter, so let it land. **A result that does not survive should be reported as not surviving.** The single most important professional habit you can build is to treat a failed robustness test as a *finding*, not a setback to be buried. If Maya's wild cluster bootstrap had returned $p = 0.2$, the honest paper says the effect is suggestive but imprecisely estimated. If her in-time placebo had lit up, the honest paper says the design cannot separate the program from a pre-trend. If her Oster δ had come in at 0.4, the honest paper states that unobserved selection could explain the result. None of these is a failure of *you*; each is a success of the *method*, which is built to stop you from telling the world something that is not true. The author who runs these tests hoping they pass and the author who runs them hoping to learn the truth get the same code and the same output — but only the second one is doing science. The whole apparatus of this chapter exists to make you the second kind of author, on purpose, before anyone else gets the chance to make you one by force.

---

## Your Turn

Open **nb8.2 — the robustness-battery harness.** It is built to run column 3 of *your* threats table, end to end, on your pre-registered estimate from Chapter 8.1: a placebo engine (fake dates, fake units via permutation, fake outcomes), a standard-error panel that re-clusters at every defensible level and runs the wild cluster bootstrap, a Benjamini–Hochberg routine for your pre-specified family of outcomes, and an Oster δ calculator with an $R_{\max}$ sensitivity sweep. Run each cell, read each pass/fail by the rules above, and assemble the results into the robustness table that becomes the backbone of your paper's robustness section (the craft of presenting it lives in Chapter 8.3 and Appendix D.3).

Three reflection prompts to write up alongside the notebook:

1. **Run your scariest placebo first.** Take the threat you ranked most dangerous in your Chapter 7.5 table and build the placebo that would expose it — the fake date if you fear a pre-trend, the permutation if you fear few clusters, the fake outcome if you fear a broad confounder. Run it. If it *fails*, do not move on: write the honest sentence that narrows or kills your claim, and decide whether to redesign or to report the limitation plainly. A robustness section that only contains passes is not more credible — it is less, because a reader assumes you did not try hard enough to fail.

2. **Read your coefficient stability with Oster's eyes.** Report your treatment coefficient with no controls and with your full controls, and *also* report the two $R^2$ values. Compute $\hat\delta$. Now answer the question §5 was built around: did your coefficient stay stable because the controls were powerful and it shrugged them off (large $\hat\delta$, reassuring), or because the controls were toothless (small $\hat\delta$, proves nothing)? Defend your $R_{\max}$ choice, then re-run with $R_{\max} = 1$ and report how much $\hat\delta$ moves.

3. **Audit your family.** Write down every outcome you have looked at — not just the ones you plan to report. How many is $m$? Apply both Bonferroni and Benjamini–Hochberg. Which results survive each? If your headline result survives only the uncorrected single test and not the correction for your true family size, what is the honest contribution sentence you can write — and is it the one you were hoping to write?

[^gaosun]: Gao, L., & Sun, H. (2019). Lending practices to same-sex borrowers. *Proceedings of the National Academy of Sciences*, 116(19), 9293–9302.

[^oster]: Oster, E. (2019). Unobservable Selection and Coefficient Stability: Theory and Evidence. *Journal of Business & Economic Statistics*, 37(2), 187–204.

[^bh]: Benjamini, Y., & Hochberg, Y. (1995). Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing. *Journal of the Royal Statistical Society: Series B*, 57(1), 289–300.

[^cgm2008]: Cameron, A. C., Gelbach, J. B., & Miller, D. L. (2008). Bootstrap-Based Improvements for Inference with Clustered Errors. *Review of Economics and Statistics*, 90(3), 414–427.

[^cgm2011]: Cameron, A. C., Gelbach, J. B., & Miller, D. L. (2011). Robust Inference with Multiway Clustering. *Journal of Business & Economic Statistics*, 29(2), 238–249.
