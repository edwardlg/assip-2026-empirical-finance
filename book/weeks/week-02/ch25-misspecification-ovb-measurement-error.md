# Chapter 2.5 — Misspecification: OVB, Measurement Error, Functional Form

Maya has a clean dataset and a clean question. She is studying mortgage approvals at a regional lender, and she wants to know whether applicants from one demographic group are approved at lower rates than otherwise-similar applicants — a fair-lending question with real legal teeth. She runs the regression every beginner would run: approval (1 for approved, 0 for denied) on a demographic indicator, plus a handful of obvious controls she happens to have — loan amount, applicant age. The coefficient on the demographic indicator comes back negative and statistically significant. The t-statistic is a comfortable $4.1$. By the machinery of Chapter 1.5 — estimate divided by standard error, compared to a critical value — she has "found" a gap.

And she is about to make the most expensive mistake in all of empirical work, which is to believe it.

Here is the problem, stated as bluntly as it deserves. Everything you learned in Chapters 2.1 through 2.4 was about computing $\hat{\boldsymbol{\beta}}$ correctly and quantifying how much it wobbles. Chapter 2.1 gave you the model and the OLS estimator. Chapter 2.2 gave you the one assumption that makes that estimator *mean the right thing* — the zero-conditional-mean assumption $\mathbb{E}[\varepsilon \mid \mathbf{X}] = 0$. Chapter 2.3 gave you partialling-out (Frisch–Waugh–Lovell) as the language for what a single coefficient really represents. Chapter 2.4 fixed your *standard errors* — the wobble. But a standard error tells you how much your estimate would bounce around if you redrew the sample. It says *nothing whatsoever* about whether the number you are bouncing around is the right number. You can have a razor-sharp standard error on a completely wrong coefficient. Maya's $t = 4.1$ is precisely that danger: a precise estimate of a biased quantity.

This chapter is about the three classic ways your coefficient can be *biased* — pointed at the wrong target — no matter how much data you collect or how carefully you cluster your standard errors. We will take them one at a time: **omitted variable bias** (you left out something that mattered), **measurement error** (the variables you have are noisy copies of the ones you want), and **functional-form misspecification** (you forced a straight line through a curved world). For each, we follow the reveal-the-trick structure: state the result, see why it happens on real numbers, derive the algebra, see exactly when it strikes and which direction it pushes, and write the code to watch it happen. Then we collect everything into a single **bias–consistency ledger** — a table that, for every threat, answers three questions: does it bias $\hat{\beta}$? Is the problem about bias or about standard errors? And what fix or research design addresses it?

That last column is the point of the whole week. By the end of this chapter you will understand, in your bones, why "add more controls and cluster your standard errors" is *not* a research strategy, and why Weeks 3 and 4 exist at all. This chapter is the bridge from mechanics to causal inference.

---

## 2.5.1 The setup: bias is the failure of $\mathbb{E}[\varepsilon \mid \mathbf{X}] = 0$

Let us be precise about what "bias" means, because the word gets thrown around loosely. We have a true model — the data-generating process — and we have a regression we actually run. Bias is the gap between what our regression's coefficient *converges to* and the true causal parameter we wanted.

Recall from Chapter 2.2 the assumption that makes OLS estimate the truth. Write the true model for an outcome $y$ as

$$y = \beta_0 + \beta_1 x + \varepsilon,$$

where we *want* $\beta_1$ to be the causal effect of $x$ on $y$ — the amount $y$ would change if we reached in and nudged $x$ by one unit, holding everything else fixed. OLS recovers this $\beta_1$ on average only if the **zero-conditional-mean assumption** holds:

$$\mathbb{E}[\varepsilon \mid x] = 0.$$

In words: the part of $y$ that your model does not explain — the error $\varepsilon$ — has nothing systematic to do with $x$. Whatever is hiding in $\varepsilon$ is, on average, the same across all values of $x$. When this holds, $x$ is called **exogenous**, and $\hat{\beta}_1 \xrightarrow{p} \beta_1$: the estimator is **consistent**, homing in on the truth as the sample grows. When it fails — when $\varepsilon$ and $x$ move together — $x$ is **endogenous**, and $\hat{\beta}_1$ converges to something *other* than $\beta_1$. That gap is the bias, and it does not shrink with more data. A biased estimator with a million observations is a precisely-wrong number.

Every threat in this chapter is, at bottom, a story about *how* $\mathbb{E}[\varepsilon \mid x] = 0$ breaks. Omitted variable bias breaks it by stuffing a relevant variable into $\varepsilon$ that is correlated with $x$. Measurement error breaks it by making the $x$ you regress on differ from the $x$ in the true model, in a way that mechanically correlates the mismeasured regressor with the error. Functional-form error breaks it by dumping the curvature you failed to model into $\varepsilon$, where it again correlates with $x$. Same disease, three vectors. Keep the assumption in view as we go; it is the thread.

---

## 2.5.2 Omitted variable bias: the result and the intuition

**The result, in one sentence:** when you leave out a variable that belongs in the model and is correlated with a variable you kept, the coefficient on the variable you kept absorbs part of the omitted variable's effect — and the contamination equals *the omitted variable's true effect times the slope from regressing the omitted variable on the included one.*

Start with the intuition before the algebra. Maya regresses approval on the demographic indicator $D$, but leaves out **creditworthiness** $C$ — a composite of credit score, debt-to-income ratio, and payment history. Creditworthiness obviously affects approval: lenders approve creditworthy applicants. And — this is the load-bearing fact — for reasons rooted in decades of unequal access to wealth, credit, and stable employment, creditworthiness is *not* evenly distributed across demographic groups in her sample. So when Maya's regression sees that group $D$ is approved less often, it cannot tell whether that is because of $D$ *itself* (discrimination) or because $D$ is correlated with lower measured creditworthiness $C$ (which the lender is, legally, allowed to price on). Her coefficient on $D$ blends the two. It is not the discrimination effect; it is the discrimination effect *plus a smear of the creditworthiness effect*, channeled through the correlation between $D$ and $C$.

That sentence — "the true effect of the omitted thing, channeled through its correlation with the thing you kept" — is the entire content of omitted variable bias. Now we make it exact.

A quick numerical preview to fix ideas before the algebra. Imagine the *true* effect of being in group $D=1$ on approval is exactly zero — no discrimination at all. But suppose creditworthiness raises the approval probability by $0.30$ per standard-deviation of credit ($\beta_2 = 0.30$), and group $D=1$ has, on average, creditworthiness $0.50$ standard deviations lower than group $D=0$ (so the slope of credit on $D$ is $\delta_1 = -0.50$). Then the short regression's coefficient on $D$ converges to $\beta_1 + \beta_2\delta_1 = 0 + (0.30)(-0.50) = -0.15$. Maya would read a $15$-percentage-point approval penalty against group $D=1$ — a damning-looking, highly significant number — *in a world with literally zero discrimination*. The entire "effect" is borrowed from creditworthiness through the correlation. That is OVB in a single line, and it is why we now derive the formula carefully.

---

## 2.5.3 Deriving the OVB formula

Suppose the **true** (long) model is

$$y = \beta_0 + \beta_1 x + \beta_2 z + \varepsilon, \qquad \mathbb{E}[\varepsilon \mid x, z] = 0,$$

where $x$ is the regressor you care about, $z$ is a second variable that genuinely affects $y$ (so $\beta_2 \neq 0$), and the assumption holds *in the long model* — meaning if you could run the long regression, $\hat{\beta}_1$ would be consistent for the true $\beta_1$. But you do not have $z$, or you forget it. You run the **short** regression

$$y = \tilde{\beta}_0 + \tilde{\beta}_1 x + u,$$

and obtain the short-regression slope $\hat{\tilde{\beta}}_1$. The tilde marks "this came from the misspecified short model." What does $\hat{\tilde{\beta}}_1$ converge to?

Here is the cleanest derivation, and it uses the partialling-out logic from Chapter 2.3 directly. The simple-regression slope of $y$ on $x$ is, by definition,

$$\hat{\tilde{\beta}}_1 = \frac{\widehat{\operatorname{Cov}}(x, y)}{\widehat{\operatorname{Var}}(x)}.$$

Substitute the *true* model for $y$ into that covariance. Because covariance is linear in its arguments and the constant $\beta_0$ contributes nothing,

$$\operatorname{Cov}(x, y) = \operatorname{Cov}(x,\ \beta_0 + \beta_1 x + \beta_2 z + \varepsilon) = \beta_1 \operatorname{Var}(x) + \beta_2 \operatorname{Cov}(x, z) + \operatorname{Cov}(x, \varepsilon).$$

The last term is zero because the long model is well-specified ($\varepsilon$ is uncorrelated with $x$). Divide through by $\operatorname{Var}(x)$:

$$\frac{\operatorname{Cov}(x,y)}{\operatorname{Var}(x)} = \beta_1 + \beta_2 \cdot \frac{\operatorname{Cov}(x,z)}{\operatorname{Var}(x)}.$$

Now recognize the last fraction. The quantity $\operatorname{Cov}(x,z)/\operatorname{Var}(x)$ is exactly the slope you would get from regressing the *omitted* variable $z$ on the *included* variable $x$. Call that slope $\delta_1$ — the "auxiliary regression" coefficient, from $z = \delta_0 + \delta_1 x + \text{noise}$. Taking probability limits (sample covariances converge to population ones by the Law of Large Numbers from Chapter 1.4), we have arrived at the **omitted variable bias formula**:

$$\boxed{\ \hat{\tilde{\beta}}_1 \xrightarrow{p} \beta_1 + \beta_2 \,\delta_1\ } \qquad \text{where } \delta_1 = \frac{\operatorname{Cov}(x,z)}{\operatorname{Var}(x)}.$$

The short regression does not estimate $\beta_1$. It estimates $\beta_1$ *plus a bias term* $\beta_2 \delta_1$. Read that bias term in plain English and memorize it, because it is one of the half-dozen most useful sentences in all of econometrics:

$$\text{bias} = \underbrace{\beta_2}_{\substack{\text{effect of the omitted}\\\text{variable on } y}} \times \underbrace{\delta_1}_{\substack{\text{slope of omitted}\\\text{on included}}}.$$

**The bias is a product of two slopes.** For it to be nonzero — for there to be a problem at all — *both* factors must be nonzero. The omitted variable must actually matter for $y$ ($\beta_2 \neq 0$), *and* it must be correlated with your regressor ($\delta_1 \neq 0$). If either is zero, the short regression is fine. This immediately tells you which omitted variables to lose sleep over: only those that both drive the outcome and travel with your key regressor. A variable that affects $y$ but is uncorrelated with $x$ costs you precision (it inflates the error variance) but does *not* bias $\hat{\beta}_1$. A variable correlated with $x$ but irrelevant to $y$ ($\beta_2 = 0$) also does no harm. It is the *intersection* — relevant *and* correlated — that is poison.

There is a second, equivalent way to see this that uses the partialling-out language of Chapter 2.3 (Frisch–Waugh–Lovell), and it is worth holding both pictures in your head. FWL told you that the *long-model* coefficient $\hat\beta_1$ on $x$ equals the slope from regressing $y$ on the part of $x$ that is *orthogonal to* $z$ — the residual $\tilde{x}$ after partialling $z$ out of $x$. The short regression skips that partialling entirely: it regresses $y$ on the *whole* of $x$, including the slice of $x$ that overlaps with $z$. So the short slope picks up $y$'s response to $x$ *through* that overlapping slice — and $y$ responds to it because $z$ affects $y$ with coefficient $\beta_2$. The bias term $\beta_2\delta_1$ is precisely the contribution of the un-partialled, $z$-overlapping piece of $x$. OVB is what you get when you *fail to partial out* a relevant variable; the long regression partials it out and is clean, the short regression leaves it in and is contaminated.

Connect this back to Chapter 2.2. The short-model error is $u = \beta_2 z + \varepsilon$ — it has swallowed the omitted $\beta_2 z$ term. Since $z$ is correlated with $x$ (that is $\delta_1 \neq 0$), the short-model error $u$ is now correlated with $x$, and $\mathbb{E}[u \mid x] \neq 0$. The zero-conditional-mean assumption fails *exactly because* a relevant, correlated variable got banished into the error term. OVB is not a separate phenomenon from endogeneity; it is the canonical example of it.

---

## 2.5.4 The two-sign rule: which way does the bias push?

You will rarely know the *magnitude* of the bias — that would require knowing $\beta_2$ and $\delta_1$, and if you knew them you would just include $z$. But you can almost always reason about its **sign**, and that is often enough to know whether your estimate is too big or too small. The sign of the bias $\beta_2 \delta_1$ is the product of two signs:

| Sign of $\beta_2$ (omitted $\to y$) | Sign of $\delta_1$ (omitted $\leftrightarrow$ included) | Sign of bias $\beta_2\delta_1$ | What it does to $\hat{\tilde\beta}_1$ |
|:---:|:---:|:---:|:---|
| $+$ | $+$ | $+$ | biased **up** (too positive) |
| $+$ | $-$ | $-$ | biased **down** (too negative) |
| $-$ | $+$ | $-$ | biased **down** |
| $-$ | $-$ | $+$ | biased **up** |

This is the **two-sign rule**: figure out the sign of the omitted variable's effect on the outcome, figure out the sign of its correlation with your included regressor, multiply, and you have the direction the bias drags your estimate. "Same signs push up, opposite signs push down."

**Maya's case, worked.** Maya's regressor is the demographic indicator $D$; suppose she has coded it so that the disadvantaged group is $D = 1$. Her outcome is approval. The omitted variable is creditworthiness $C$. Two signs:

- **$\beta_2$, effect of $C$ on approval:** positive. More creditworthy applicants are approved more often. $\beta_2 > 0$.
- **$\delta_1$, slope of $C$ on $D$:** in her sample, the $D = 1$ group has *lower* average measured creditworthiness (the legacy of unequal access described above), so regressing $C$ on $D$ gives a negative slope. $\delta_1 < 0$.

Product: $(+)(-) = -$. The bias is **negative**. Maya's short-regression coefficient on $D$ is biased *downward* — pushed in the negative direction — meaning her estimate *overstates* the approval penalty against group $D = 1$. Part of what looks like discrimination is really the lender responding to lower measured creditworthiness, which her regression mistakenly loads onto $D$. The honest statement is not "there is no discrimination" — we have not shown that — but "the raw $D$ coefficient is an upper bound on the disadvantage attributable to $D$ itself, contaminated by omitted creditworthiness; I cannot separate the two without controlling for $C$."

That last clause is the fair-lending threat named in the language of CONVENTIONS spec discipline. Let us write Maya's specification out fully, because naming the threat *is* the deliverable:

- **Outcome:** approval indicator (1 = approved).
- **Key regressor:** demographic indicator $D$.
- **Controls (current):** loan amount, age. **Missing and decisive:** creditworthiness $C$.
- **Sample:** applicants to one regional lender, one year.
- **Threat:** omitted variable bias from $C$ — relevant ($\beta_2 > 0$) and correlated with $D$ ($\delta_1 < 0$) — biasing the $D$ coefficient downward.
- **What would fix it:** include a credit-risk control; or, better, a design that compares applicants who are *identical on creditworthiness* (Week 4). Adding the control attacks the bias *if* $C$ is the only omitted confounder, which is itself an assumption.

**A second example, opposite direction.** Sam regresses a stock's next-month return on a "momentum" signal but omits a firm-**size** variable. The point here is the *mechanics*, so let us reason from supposed signs rather than assert what the data show. Suppose, in Sam's sample, the omitted size variable raises returns in the direction his coding implies ($\beta_2 > 0$), and suppose momentum is positively correlated with that size variable ($\delta_1 > 0$). Then $(+)(+) = +$: Sam's momentum coefficient would be biased *up*, and he would overstate momentum's profitability — exactly the kind of mirage that the multiple-testing discussion of Chapter 1.5 warned about, now with a structural cause. Flip either supposed sign and the two-sign rule flips the bias with it. The lesson is the rule, not the particular signs: Sam must establish the actual signs of $\beta_2$ and $\delta_1$ in his own sample (and ideally just include size) before claiming any direction in print.

---

## 2.5.5 Adding controls is a bet, not a cure

Here is the seductive trap. "Fine," you say, "OVB comes from omitting variables, so I will *include* everything." Maya adds creditworthiness, employment, neighborhood, ten more controls. Does that fix it?

It fixes the bias from *those particular* variables — and only if they are measured well (Section 2.5.6) and enter in the right functional form (Section 2.5.9). It does nothing about variables you *still* omit, including ones you cannot even name or measure. And there is always a residual list: unobserved applicant motivation, soft information the loan officer saw that the dataset did not record, local economic shocks. The bias formula does not care whether the omitted variable is omitted because you forgot it or because it is fundamentally unmeasurable. As long as some relevant, correlated thing sits in the error term, $\hat\beta_1$ is biased.

So "control for it" is a *bet* — a bet that the variables you added were the important confounders and that nothing comparably important remains. Sometimes it is a good bet; often it is not; and crucially, **the regression itself cannot tell you whether you won the bet.** No diagnostic, no $R^2$, no standard error reveals the bias from a variable that is not in your data. This is the wall that pure regression hits, and it is why Weeks 3 and 4 turn to research *designs* — randomization, natural experiments, instruments — that make the zero-conditional-mean assumption *credible by construction* rather than by hopeful enumeration of controls.

---

## 2.5.6 Measurement error: classical errors-in-variables and attenuation

Now the second threat. Even with no omitted variable, your coefficient can be biased simply because you measured your regressor *imprecisely*.

**The result, in one sentence:** when your key regressor is a noisy version of the true variable, with noise that is just random static unrelated to anything, the OLS coefficient is biased *toward zero* — a phenomenon called **attenuation bias** — and the shrinkage factor is the share of the regressor's variance that is real signal rather than noise.

Set it up. The true model uses the true regressor $x^\*$:

$$y = \beta_0 + \beta_1 x^\* + \varepsilon, \qquad \mathbb{E}[\varepsilon \mid x^\*] = 0.$$

But you do not observe $x^\*$. You observe a mismeasured version

$$x = x^\* + m,$$

where $m$ is **measurement error**. The **classical errors-in-variables** (CEV) assumptions are that the error is pure random static: $m$ has mean zero, is uncorrelated with the true value $x^\*$, and is uncorrelated with the equation error $\varepsilon$. (Think of $m$ as a thermometer that reads the true temperature plus an independent jiggle.) You regress $y$ on the observed $x$. What happens?

Substitute $x^\* = x - m$ into the true model:

$$y = \beta_0 + \beta_1 (x - m) + \varepsilon = \beta_0 + \beta_1 x + \underbrace{(\varepsilon - \beta_1 m)}_{\text{new error } u}.$$

Look at the new composite error $u = \varepsilon - \beta_1 m$. It contains $-\beta_1 m$. And the regressor $x = x^\* + m$ also contains $m$. So the regressor and the error share the term $m$ — they are *mechanically correlated*. The zero-conditional-mean assumption fails again, this time not because we omitted a variable but because the noise in our regressor leaks into the error term. Let us compute the consequence. The probability limit of the OLS slope is

$$\hat{\beta}_1 \xrightarrow{p} \frac{\operatorname{Cov}(x, y)}{\operatorname{Var}(x)}.$$

Compute the pieces under the CEV assumptions. The numerator:

$$\operatorname{Cov}(x, y) = \operatorname{Cov}(x^\* + m,\ \beta_0 + \beta_1 x^\* + \varepsilon) = \beta_1 \operatorname{Var}(x^\*),$$

because $m$ is uncorrelated with $x^\*$ and with $\varepsilon$, killing every cross term. The denominator, because $x^\*$ and $m$ are uncorrelated, splits cleanly:

$$\operatorname{Var}(x) = \operatorname{Var}(x^\*) + \operatorname{Var}(m) = \sigma_{x^\*}^2 + \sigma_m^2.$$

Divide:

$$\boxed{\ \hat{\beta}_1 \xrightarrow{p} \beta_1 \cdot \underbrace{\frac{\sigma_{x^\*}^2}{\sigma_{x^\*}^2 + \sigma_m^2}}_{\text{attenuation factor } \lambda}\ }$$

The OLS slope converges not to $\beta_1$ but to $\beta_1$ multiplied by a number $\lambda = \sigma_{x^\*}^2 / (\sigma_{x^\*}^2 + \sigma_m^2)$. Because variances are non-negative, $\lambda$ lies strictly between 0 and 1 (whenever there is any noise, $\sigma_m^2 > 0$). So the estimate is *pulled toward zero* — smaller in magnitude than the truth, regardless of sign. This is **attenuation bias**.

The factor $\lambda$ has a beautiful interpretation: it is the **reliability ratio**, the fraction of the observed regressor's variance that is genuine signal. If half the variance in your measured $x$ is noise ($\sigma_m^2 = \sigma_{x^\*}^2$), then $\lambda = 1/2$ and your coefficient is exactly *half* its true size — a 100% measurement-error variance halves your estimate. If the measurement is nearly perfect ($\sigma_m^2 \approx 0$), $\lambda \approx 1$ and there is no problem. Unlike OVB, the *direction* of classical measurement-error bias is always known: toward zero. A real effect looks weaker than it is; you under-reject; you may miss a relationship that genuinely exists.

**Maya's self-reported income.** Maya's dataset records applicant income from a self-reported field on the application — and self-reported income is famously noisy (people round, misremember, conflate gross and net, occasionally exaggerate). Treat self-reported income as $x = x^\* + m$ where $x^\*$ is true income. Then the coefficient on income in her approval model is attenuated: it will *understate* how much true income matters for approval. The threat, named per spec discipline: **classical measurement error in income, biasing its coefficient toward zero**; the fix is a better-measured income (verified tax records, pay stubs) or, formally, an instrument for true income (Week 4) — for example, a second independent measurement, which under CEV provides exactly the leverage needed to undo $\lambda$.

---

## 2.5.7 Three subtleties that trip people up

The clean attenuation result is for one specific case. Three variations matter, and confusing them is a common error.

**(1) Mismeasured $y$ is harmless to the slope (mostly).** Suppose the *outcome* is measured with classical error: you observe $y = y^\* + v$ with $v$ random static uncorrelated with the regressors. Then the mismeasurement just folds into the equation error: $y = \beta_0 + \beta_1 x + (\varepsilon + v)$. Since $v$ is uncorrelated with $x$, the zero-conditional-mean assumption *survives*, and $\hat\beta_1$ remains **consistent**. The only cost is a larger error variance, which inflates standard errors — a *precision* problem, not a *bias* problem. This is the crucial asymmetry: **classical noise in $x$ biases the slope; classical noise in $y$ does not.** (The catch is "classical": if the outcome's error is *correlated* with a regressor — say, people with higher $x$ systematically over-report $y$ — all bets are off.)

**(2) Mismeasured controls re-open OVB.** Suppose your *control* variable is mismeasured. Maya includes creditworthiness, but her credit proxy is noisy. Then the control only *partially* removes the confounding it was meant to absorb — the regression "controls for" the noisy proxy, not the true confounder, so residual confounding leaks back into the coefficient on $D$. A noisily-measured control is a partially-omitted control. This is why "I controlled for it" and "I controlled for it *well*" are different claims, and why the OVB bet of Section 2.5.5 is even riskier than it first looked.

**(3) Non-classical error can bias *away* from zero.** The toward-zero guarantee depends on the error being uncorrelated with the true value. When the error is correlated with the truth — for instance, top-coded incomes, or self-reports where high earners under-state more — the bias can go in either direction, including *away* from zero. "Measurement error always attenuates" is a half-truth; it attenuates *under the classical assumptions*. State the assumptions, then claim the direction.

---

## 2.5.8 Watching attenuation happen in code

The fastest way to trust the formula is to simulate it. We build data where we *know* the true $\beta_1 = 2$, then corrupt the regressor with increasing amounts of noise and watch the estimate slide toward zero exactly as $\lambda$ predicts.

```python
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

rng = np.random.default_rng(20260527)
N = 50_000
beta1_true = 2.0

# True regressor and outcome (well-specified, no omission)
x_star = rng.normal(0.0, 1.0, size=N)          # Var(x*) = 1
eps     = rng.normal(0.0, 1.0, size=N)
y       = 1.0 + beta1_true * x_star + eps

rows = []
for sigma_m in [0.0, 0.5, 1.0, 2.0]:            # rising measurement-error SD
    m  = rng.normal(0.0, sigma_m, size=N)
    x  = x_star + m                             # classical EIV: x = x* + m
    fit = smf.ols("y ~ x", data=pd.DataFrame({"y": y, "x": x})).fit()
    lam = 1.0 / (1.0 + sigma_m**2)              # lambda = Var(x*)/(Var(x*)+Var(m))
    rows.append({
        "sigma_m": sigma_m,
        "lambda_predicted": lam,
        "beta_hat": fit.params["x"],
        "predicted_plim": beta1_true * lam,
    })

print(pd.DataFrame(rows).round(3).to_string(index=False))
```

Running it produces, up to simulation noise:

```
 sigma_m  lambda_predicted  beta_hat  predicted_plim
     0.0             1.000     1.998           2.000
     0.5             0.800     1.602           1.600
     1.0             0.500     1.001           1.000
     2.0             0.200     0.402           0.400
```

The estimate marches from $2.0$ toward $0$ exactly as $\beta_1 \lambda$ predicts. With noise variance equal to signal variance ($\sigma_m = 1$), the coefficient is halved. No amount of additional data changes this — try $N = 5{,}000{,}000$ and the numbers barely move, because attenuation is a bias in the probability *limit*, not sampling noise. That is the difference between a bias problem and a standard-error problem in one experiment.

---

## 2.5.9 Functional form: when the straight line is the wrong shape

The third threat is different in flavor. OVB and measurement error are about *which* variables and *how well measured*; functional-form misspecification is about the *shape* of the relationship. OLS fits the best *straight line* (or flat plane). If the true relationship between $x$ and $y$ is curved, a straight line is not just imprecise — it can be systematically wrong, and the error it makes is, once again, correlated with $x$.

**The result, in one sentence:** if you fit a linear model to a nonlinear relationship, the omitted curvature lands in the error term, correlates with $x$, and the coefficient you report is a slope that does not exist anywhere — neither the slope at low $x$ nor at high $x$, but a misleading average that can mislead about both.

Consider Priya, who studies how a firm's carbon-emissions intensity relates to its insurance premium. Suppose the true relationship is *convex*: premiums rise slowly with emissions at low levels, then steeply at high levels (insurers price catastrophic tail risk). The true model has a quadratic term, $y = \beta_0 + \beta_1 x + \beta_2 x^2 + \varepsilon$ with $\beta_2 > 0$. If Priya fits only $y = \tilde\beta_0 + \tilde\beta_1 x + u$, the $x^2$ curvature is swept into $u = \beta_2 x^2 + \varepsilon$, which is correlated with $x$ — the same disease as OVB, with the "omitted variable" being a *transformation of a variable she already has.* The fitted line will understate the premium's sensitivity at high emissions and overstate it at low emissions, and the single number $\hat{\tilde\beta}_1$ describes neither.

The fixes are a toolkit, and the good news is you already own the variables — you just need to add the right transformations:

- **Polynomials.** Add $x^2$ (and maybe $x^3$) as regressors: $y = \beta_0 + \beta_1 x + \beta_2 x^2 + \varepsilon$. This stays *linear in the parameters* — it is still OLS, still least squares — even though the relationship in $x$ is curved. The marginal effect is now $\partial y/\partial x = \beta_1 + 2\beta_2 x$, which varies with $x$, capturing the convexity.
- **Logs.** Replacing levels with logs reshapes the relationship and changes the *interpretation* to elasticities and semi-elasticities. In $\ln y = \beta_0 + \beta_1 x + \varepsilon$, $\beta_1$ is the approximate *proportional* change in $y$ per unit of $x$ (a semi-elasticity); in $\ln y = \beta_0 + \beta_1 \ln x + \varepsilon$, $\beta_1$ is an *elasticity* — the percent change in $y$ per percent change in $x$. Logs also tame skewed, multiplicative financial variables (firm size, income, market cap) and stabilize variance.
- **Interactions.** If the effect of $x$ on $y$ *depends on* another variable $w$, include the product: $y = \beta_0 + \beta_1 x + \beta_2 w + \beta_3 (x \cdot w) + \varepsilon$. Now the slope on $x$ is $\beta_1 + \beta_3 w$, different for different $w$. Maya might interact loan size with income if the income effect on approval is stronger for large loans.

These are not exotic. They are ordinary OLS with cleverly-constructed regressors, and they dissolve most functional-form problems — *if you know the right shape*. The harder question is diagnosing that you have a problem at all.

---

## 2.5.10 The RESET test: a diagnostic for "is my line the wrong shape?"

Ramsey's **Regression Equation Specification Error Test** (RESET) is a simple, clever check for neglected nonlinearity. The idea: if your linear model has captured the true shape, then *powers of the fitted values* should have no additional explanatory power — there is no leftover curvature for them to pick up. If they *do* help, your functional form is missing something.

The procedure is mechanical:

1. Fit your model $y = \beta_0 + \beta_1 x + \dots + u$ and save the fitted values $\hat{y}$.
2. Re-fit, adding powers of the fitted values as extra regressors: $y = \beta_0 + \beta_1 x + \dots + \gamma_1 \hat{y}^2 + \gamma_2 \hat{y}^3 + e$.
3. Test the joint null $H_0: \gamma_1 = \gamma_2 = 0$ with an $F$-test (the joint-significance machinery from Chapter 2.4 / 1.5).

Why $\hat{y}^2$ and $\hat{y}^3$? Because the fitted value is a combination of all your regressors, its powers are a cheap, low-dimensional stand-in for *all* the squared and cross terms you might have omitted, without having to guess which specific variable needs a polynomial. A rejection ($p < 0.05$) says "there is curvature your linear model is not capturing" — a flag, not a diagnosis. RESET tells you *that* something is wrong with the shape, not *what*. You then go hunting: which variable needs a square, which pair needs an interaction, whether logs are called for.

```python
import statsmodels.formula.api as smf
from statsmodels.stats.diagnostic import linear_reset

# Priya's convex truth, fit with a (wrong) straight line
rng = np.random.default_rng(7)
x   = rng.uniform(0, 5, 4000)
y   = 1 + 0.5*x + 0.4*x**2 + rng.normal(0, 1, 4000)   # true beta2 = 0.4 > 0
df  = pd.DataFrame({"y": y, "x": x})

linear_fit = smf.ols("y ~ x", data=df).fit()
reset = linear_reset(linear_fit, power=3, use_f=True)   # adds yhat^2, yhat^3
print(f"RESET F = {reset.fvalue:.1f},  p = {reset.pvalue:.2e}")   # tiny p: reject linearity

quad_fit = smf.ols("y ~ x + I(x**2)", data=df).fit()
reset2 = linear_reset(quad_fit, power=3, use_f=True)
print(f"RESET F = {reset2.fvalue:.2f},  p = {reset2.pvalue:.2f}")  # large p: shape now OK
```

The linear fit fails RESET with a microscopic p-value; add the quadratic term and RESET no longer rejects. The diagnostic flagged the problem, the polynomial fixed it, and the test confirmed the fix — the full reveal-the-trick loop in four lines.

One caution worth stating: RESET is a test for *functional form*, not for OVB or measurement error. A model can sail through RESET and still be hopelessly confounded by an omitted variable, because RESET only looks at curvature among the variables you *have*. Passing RESET means "the shape looks right," not "the coefficient is causal." Do not let a clean RESET lull you into trusting a number that OVB has quietly poisoned.

---

## 2.5.11 The bias–consistency ledger

Now we collect everything. The single most useful habit this chapter can give you is to look at any regression and silently run down a checklist: *for each thing that could be wrong, does it bias my coefficient, or merely inflate my standard error? And what would fix it?* Bias and precision are different diseases with different cures, and conflating them is the signature error of the beginner. The table below is that checklist. The last two columns are the heart of it: notice how often the honest fix is not a regression tweak but a *research design* — which is the door into Weeks 3 and 4.

| Problem | Biases $\hat\beta$? | Direction (if known) | Bias or SE issue? | Fix / design that addresses it |
|---|---|---|---|---|
| **Omitted variable** (relevant + correlated with $x$) | Yes | sign of $\beta_2\,\delta_1$ (two-sign rule) | **Bias** | Include the control (a *bet*); better: randomization or natural experiment that removes the confounder by design → **Weeks 3–4** |
| Irrelevant variable omitted ($\beta_2=0$) | No | — | Neither | Nothing needed |
| Relevant variable, *uncorrelated* with $x$ ($\delta_1=0$) | No | — | **SE** (larger error variance) | Include it to gain precision |
| **Classical measurement error in $x$** | Yes | toward zero (attenuation, factor $\lambda$) | **Bias** | Better measurement; instrument for $x^\*$ → **Week 4** |
| Measurement error in $y$ (classical) | No | — | **SE** (wider intervals) | Live with it / more data |
| Mismeasured *control* | Yes (re-opens OVB) | partial, in OVB direction | **Bias** | Measure the control well; instrument; better design |
| Non-classical measurement error | Yes | either direction | **Bias** | Model the error process; validation data |
| **Wrong functional form** (neglected curvature) | Yes | depends on shape | **Bias** | Polynomials, logs, interactions; diagnose with **RESET** |
| Heteroskedasticity (from Ch 2.4) | No | — | **SE** | Robust HC1/HC2/HC3 standard errors |
| Clustering / serial correlation (Ch 2.4) | No | — | **SE** | Clustered / HAC (Newey–West) standard errors |
| Simultaneity / reverse causality ($y$ also causes $x$) | Yes | either direction | **Bias** | Instrument; design that isolates exogenous variation → **Week 4** |

Read the table top to bottom and a pattern jumps out. The Chapter 2.4 problems — heteroskedasticity, clustering — live entirely in the **SE** column: they change how much your estimate wobbles, never where it is centered. Robust and clustered standard errors are the right and complete fix for them. The problems of *this* chapter live in the **bias** column: they move the center, and no standard-error adjustment can touch them. Bigger samples, fancier standard errors, more decimal places — none of it helps a biased coefficient. That is the line this chapter draws, and it is the line that organizes the rest of the camp.

---

## 2.5.12 Where this goes next: the bridge to causal inference

Step back and see what just happened to the regression you trusted. In Chapter 2.1 OLS looked like a finished machine: feed in data, turn the crank, read off $\hat\beta$. Chapters 2.2–2.4 sharpened it — the assumption that makes it mean something, the partialling-out that interprets it, the standard errors that quantify its wobble. And now Chapter 2.5 has shown that the machine's *central output* can be pointed at the wrong target by any of three everyday problems, that "add controls and cluster" cannot rescue it, and that the regression cannot even *tell you* it has been fooled. Maya's $t = 4.1$ was real; the number it certified was not the number she wanted.

This is not a counsel of despair — it is the motivation for everything that follows. The deep lesson is that **whether $\hat\beta$ is causal is a question about where the variation in $x$ comes from, and that is a question regression alone cannot answer.** If $x$ varies because of confounders ($z$), or because of noise ($m$), or because $y$ feeds back into $x$, then OLS faithfully estimates a contaminated quantity. To get a causal number, you need $x$ to vary for reasons unrelated to the error term — and arranging that is the job of *research design*, not estimation.

Week 3 starts over from a different foundation: the **potential-outcomes** framework, where we define a causal effect precisely as the difference between what *would* happen to a unit under treatment versus under no treatment, and confront the "fundamental problem of causal inference" — that we never see both. From there, randomization (Week 3) and quasi-experimental designs — instrumental variables, difference-in-differences, regression discontinuity (Week 4) — are revealed as machines for manufacturing the exogenous variation that OVB, measurement error, and simultaneity destroy. Every threat in this chapter's ledger gets a design-based answer there. Maya's fair-lending question, in particular, returns in Week 4 with the tools to actually identify the effect of $D$ holding creditworthiness genuinely fixed — and with Prof. Gao's own fair-lending research as the worked example.

You now know the diseases. The next two weeks are the cure.

---

## Your Turn

Open **`nb2.5`** (`notebooks/week-02/nb2.5-biased-estimator-lab.ipynb`), the biased-estimator lab. You will (1) **simulate OVB** end to end: generate data from a known long model $y = \beta_0 + \beta_1 x + \beta_2 z + \varepsilon$ with $z$ correlated with $x$, run both the long and short regressions, and verify that the short-regression slope lands on $\beta_1 + \beta_2\delta_1$ — then flip the sign of $\delta_1$ and watch the bias flip with the two-sign rule. (2) **Simulate attenuation:** corrupt a regressor with rising measurement-error variance and confirm $\hat\beta_1 \to \beta_1\lambda$, plotting the estimate against the reliability ratio. (3) Build Maya's case: simulate approvals where the *true* demographic effect is zero but creditworthiness confounds, show the short regression "finds" a spurious gap, and show that controlling for (well-measured) creditworthiness removes it — then re-run with a *noisily-measured* creditworthiness control and watch the bias partially return.

**Check questions.**

1. A researcher regresses startup valuation on founder age and finds a strong positive coefficient. A skeptic says years of industry experience is omitted: experience raises valuation ($\beta_2 > 0$) and is positively correlated with age ($\delta_1 > 0$). (a) Using the two-sign rule, which direction is the age coefficient biased? (b) Is the reported coefficient too large or too small as an estimate of age's *own* effect? (c) Would clustering the standard errors fix this? Explain in one sentence why or why not.

2. Devon measures on-chain wallet activity with a noisy scraper, then regresses token return on this activity measure. The true effect of activity on return is $\beta_1 = 1.0$; the activity measure has reliability ratio $\lambda = 0.6$. (a) What value will Devon's OLS coefficient converge to, and in which direction is it biased? (b) Devon's *outcome* (return) is also measured with classical noise. Does that bias the slope, widen the standard error, or both? (c) Devon doubles his sample size. Which of the two problems in (a) and (b) does that help?

3. Priya fits insurance premium on emissions linearly, runs RESET, and gets $p = 0.001$. (a) What does this tell her, and what does it *not* tell her? (b) She adds an $x^2$ term and re-runs RESET, now getting $p = 0.42$. Name one threat to her premium–emissions coefficient that this clean RESET result does *not* rule out, and explain why RESET is blind to it.
