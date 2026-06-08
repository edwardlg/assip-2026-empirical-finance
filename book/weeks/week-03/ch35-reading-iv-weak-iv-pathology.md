# Chapter 3.5 — Reading IV in the Wild + The Weak-IV Pathology

Devon is reading his first real instrumental-variables paper. It is a study of whether holding crypto in your portfolio changes how much you trade other assets, and the authors instrument crypto-holding with the distance from a person's home to the nearest crypto ATM. The abstract is confident. The IV estimate is three times the OLS estimate, the standard error is tight, the stars are dense, and the conclusion is bold. Devon's instinct, trained by Chapters 2.5 and 3.4, is to be impressed: they found an instrument, they ran two-stage least squares, they reported a number with a small standard error. Surely a small standard error means a reliable answer.

This is the chapter where that instinct gets dismantled.

Chapter 3.4 built instrumental variables from the ground up: the two requirements an instrument $z$ must satisfy — **relevance** (it actually shifts the endogenous regressor $x$) and **exclusion** (it affects the outcome $y$ *only* through $x$, never directly); two-stage least squares as Frisch–Waugh–Lovell run with an instrument; the **LATE** interpretation, where IV recovers the effect *only for the compliers* — the units whose treatment status the instrument actually moved — under a monotonicity assumption; and the first diagnostic for trouble, the **first-stage $F$-statistic**, with its Stock–Yogo critical values and the more honest **Olea–Pflueger effective $F$** when errors are not homoskedastic. That chapter taught you how to *build* and *run* an IV estimator.

This chapter is its companion. It teaches you two things the first chapter only gestured at. First, **how to read an IV paper critically** — the questions a sharp referee asks in the first ten minutes, the ones that separate a credible design from a confident-sounding fraud. Second, and more deeply, **how IV breaks**, even when you did everything by the book. The headline failure is the **weak-instrument pathology**: when relevance is *barely* satisfied — when the first stage is faint — 2SLS does not merely get noisy. It gets *biased*, in a predictable and treacherous direction, and its conventional confidence interval gets *too narrow*, lying to you with false confidence. We will see exactly why, watch it happen in a simulation where we know the truth, and then meet the cure: **Anderson–Rubin inference**, a way to test the causal parameter that stays honest no matter how weak the first stage is. Along the way we will confront the surprise that **adding more instruments can make the bias worse, not better**, and the famous cautionary tale — the quarter-of-birth instrument and the Bound–Jaeger–Baker critique — that taught the profession to fear weak instruments. The reveal-the-trick structure holds throughout: state it, see why, see when it fails, watch it in code.

---

## 3.5.1 How to read an IV paper: the referee's checklist

Before any algebra, learn to read. An IV paper is a magic trick, and like any magic trick it depends on misdirection: the authors want you looking at the impressive IV coefficient, not at the instrument doing the work. Your job as a critical reader is to ignore the coefficient at first entirely and interrogate the instrument. There are five questions, and they go in order.

**1. What is the instrument, exactly?** Find it. This sounds trivial; it is not. Papers bury the instrument in a sentence in the data section, or behind a euphemism ("we exploit plausibly exogenous variation in..."). Name it concretely. In Devon's paper the instrument is *distance to the nearest crypto ATM*. The endogenous regressor is *crypto-holding*. The outcome is *trading volume in other assets*. Write these three down as a triple — instrument $z$, treatment $x$, outcome $y$ — before reading another word. If you cannot state the triple in one sentence, the paper has not earned your trust.

**2. Is it relevant?** Does $z$ actually move $x$? This is the one question the data can answer cleanly, and the paper *must* report the answer: the **first-stage regression** of $x$ on $z$ (plus controls), and its strength. The single number to hunt for is the **first-stage $F$-statistic** on the excluded instrument(s). From Chapter 3.4 you know the rough rule of thumb — $F$ comfortably above 10 (the old Staiger–Stock benchmark), or above the relevant Stock–Yogo / Olea–Pflueger critical value — and you know that an $F$ in the single digits is a klaxon. If a paper does not report a first-stage $F$, or reports the first-stage $R^2$ instead (which is not the right object) and hopes you will not notice, be very suspicious. The first-stage strength is the load-bearing diagnostic of the entire enterprise, and this whole chapter is about what happens when it is weak.

**3. Is exclusion plausible?** Does $z$ affect $y$ *only* through $x$? This is the question the data *cannot* answer — exclusion is fundamentally untestable in the just-identified case, an assumption you defend with argument, not with a statistic. So the referee reads the authors' defense and looks for the back door: a channel by which the instrument touches the outcome *without* going through the treatment. For Devon's ATM-distance instrument, ask: does living near a crypto ATM correlate with anything *else* that affects your trading behavior? Crypto ATMs cluster in dense, young, tech-forward, financially-active neighborhoods. People in those neighborhoods trade more of *everything* for reasons that have nothing to do with whether they personally hold crypto — income, financial literacy, smartphone penetration, peer effects. If so, ATM-distance violates exclusion: it is correlated with trading through a back door (neighborhood affluence), not only through crypto-holding. A good paper anticipates this and controls for it or argues it away; a bad paper pretends the back door does not exist. **Exclusion is where most IV papers actually live or die**, and it is an argument, not a test.

**4. Who are the compliers?** Recall from Chapter 3.4 that IV does not estimate the average treatment effect for everybody. It estimates the **Local Average Treatment Effect** — the effect for **compliers**, the subpopulation whose treatment status the instrument actually flips. For ATM-distance, the compliers are people who would hold crypto *if* an ATM were nearby but *would not* if it were far — marginal, convenience-driven adopters. They are not the crypto whales, who hold regardless of ATMs (always-takers), nor the crypto-averse, who never hold (never-takers). So even if the design is perfect, the number answers a narrow question: the trading effect of crypto-holding *for convenience-driven marginal adopters*. Ask of every IV paper: who are the compliers, are they an interesting population, and does the abstract overclaim by describing a complier-specific effect as if it were universal? Most do.

**5. Just-identified or over-identified?** Count the instruments and the endogenous regressors. If there is **one instrument per endogenous regressor**, the model is **just-identified** — exactly enough information to pin down the parameter, no more. If there are **more instruments than endogenous regressors**, it is **over-identified** — and you get something extra: a *testable implication*. With surplus instruments, each one implies its own IV estimate, and if they all point to the same place, that is reassuring; if they disagree wildly, at least one of them is violating exclusion. That is the **overidentification test** (Section 3.5.6). It is also where the *many-instruments bias* lurks (Section 3.5.7) — over-identification is a double-edged sword. Just-identified IV is cleaner to reason about but offers no internal check on exclusion; over-identified IV offers a check but introduces new ways to go wrong.

Run these five questions on every IV paper and you will read them better than most graduate students. Now we turn to the deepest failure mode, the one hiding inside question 2.

---

## 3.5.2 The weak-instrument pathology: the result and the intuition

**The result, in one sentence:** when the first stage is weak — the instrument barely moves the endogenous regressor — 2SLS is *biased toward the OLS estimate it was supposed to rescue you from*, and its conventional standard error is *too small*, so you get a confidence interval that is both centered on the wrong place and falsely narrow about it.

Read that twice, because it inverts every intuition you have. You reached for IV precisely *because* OLS was biased by endogeneity. A weak instrument quietly drags your IV estimate *back toward* the biased OLS number — it gives you the disease you were treating, while handing you a certificate of health. And it does the damage not by being noisy in an obvious way (a huge standard error you would respect), but by being *confidently wrong*: a tight interval around a contaminated point.

Here is the intuition, and it comes straight from the structure of 2SLS. Recall the IV estimator in the simplest one-instrument, one-regressor case. The IV slope is a *ratio*:

$$\hat\beta_{\text{IV}} = \frac{\widehat{\operatorname{Cov}}(z, y)}{\widehat{\operatorname{Cov}}(z, x)}.$$

The numerator is the **reduced form** — how the instrument moves the outcome. The denominator is the **first stage** — how the instrument moves the treatment. IV is "the effect of $z$ on $y$, scaled up by how much $z$ moves $x$." If a tiny nudge in $z$ produces a tiny shift in $y$ but only a *very* tiny shift in $x$, the ratio blows the small reduced-form signal up by the small first-stage denominator.

Now watch what a small denominator does. **You are dividing by a number that is close to zero and itself estimated with error.** Two catastrophes follow. First, the sampling distribution of a ratio whose denominator hugs zero is wild — fat-tailed, skewed, nothing like the tidy normal the conventional standard-error formula assumes. The standard formula linearizes around the denominator and badly underestimates the true spread, which is why the reported standard error is too small. Second — and this is the subtle, deadly part — the denominator $\widehat{\operatorname{Cov}}(z,x)$ and the numerator's error are *correlated in finite samples* through the endogeneity itself. When $x$ is endogenous, the same chance fluctuations that make $\widehat{\operatorname{Cov}}(z,x)$ land high or low also push the numerator the same way, and the ratio inherits a systematic tilt. That tilt points, provably, *toward the OLS probability limit*. The weaker the instrument, the stronger the pull.

There is an exact, memorable way to summarize the bias. In an over-identified model with $L$ instruments and a first-stage strength measured by the population analog of the $F$-statistic, the approximate bias of 2SLS relative to the bias of OLS is

$$\frac{\mathbb{E}[\hat\beta_{\text{2SLS}}] - \beta}{\mathbb{E}[\hat\beta_{\text{OLS}}] - \beta} \approx \frac{1}{F + 1},$$

a relationship that is the engine behind the famous "$F > 10$" rule (with $L$ instruments the story is a little richer, but this captures it). When the first-stage $F$ is enormous, $1/(F+1) \approx 0$ and 2SLS has shed essentially all of OLS's bias — the instrument is strong, IV works. When $F$ is small — say $F = 1$ — the ratio is about $1/2$: **2SLS carries half of OLS's bias.** And critically, the sign is *toward* OLS. The very bias you fled is the bias a weak instrument hands back to you. This is why a weak instrument is worse than no instrument at all: no instrument leaves you with honest OLS and an honest worry; a weak instrument gives you contaminated OLS dressed up as a clean causal estimate.

---

## 3.5.3 The cautionary tale: quarter of birth and Bound–Jaeger–Baker

The profession learned this the hard way, and the lesson has a name. In a celebrated 1991 study, Angrist and Krueger wanted the causal effect of an extra year of schooling on earnings. Schooling is endlessly endogenous — ability, family background, ambition all drive both schooling and wages and live in the error term. Their instrument was beautiful: **quarter of birth.** Compulsory-schooling laws let you drop out at age 16, but you start school in the year you turn six. So children born early in the year hit 16 with *less* accumulated schooling than children born late in the year — quarter of birth nudges years of education for the marginal dropout, and quarter of birth is, surely, as-good-as-random with respect to earnings. Relevance plausible, exclusion plausible. A textbook instrument.

Then, in a 1995 paper in the *Journal of the American Statistical Association*, Bound, Jaeger, and Baker delivered the critique that reshaped how empiricists think.[^bjb] Their argument had two prongs, and both are pure weak-instrument pathology. **First, the instrument is weak**: quarter of birth explains a minuscule fraction of the variation in schooling — the first stage, though "statistically significant" in their enormous sample of hundreds of thousands, is faint in the sense that matters, the $F$ in many specifications hovering low. **Second, and devastatingly, they showed that this weakness made the IV estimate vulnerable to even tiny exclusion violations and to finite-sample bias toward OLS.** Their most quoted demonstration: they re-ran the analysis after replacing the real quarter-of-birth instrument with *randomly generated* quarter-of-birth — pure noise, correlated with nothing — and 2SLS still produced a "significant," plausible-looking schooling coefficient with a respectable standard error. A *random number* posing as an instrument manufactured a causal estimate. That is the weak-instrument disaster made visible: when the first stage is feeble, 2SLS will conjure a confident answer out of essentially nothing, and the conventional standard error will not warn you.

[^bjb]: Bound, J., Jaeger, D. A., & Baker, R. M. (1995). Problems with Instrumental Variables Estimation When the Correlation Between the Instruments and the Endogenous Explanatory Variable Is Weak. *Journal of the American Statistical Association*, 90(430), 443–450. The 1991 schooling study they critique is Angrist, J. D., & Krueger, A. B. (1991). Does Compulsory School Attendance Affect Schooling and Earnings? *Quarterly Journal of Economics*, 106(4), 979–1014.

The lesson Bound–Jaeger–Baker burned into the field is the one this chapter is built around: **statistical significance of the first stage is not the same as strength.** With a big enough sample, a useless instrument clears the significance bar while remaining far too weak to support credible inference. You must check the first-stage $F$ against the weak-instrument critical values, not against a $t$-stat of 2. And you must use inference methods that do not fall apart when the instrument is weak — which is exactly where Anderson–Rubin comes in.

---

## 3.5.4 The cure: Anderson–Rubin inference

The weak-instrument pathology came from one place: **dividing by a weak, error-ridden first stage.** So the cure is to design an inference procedure that *never divides by the first stage at all.* That is the whole idea of the **Anderson–Rubin** test, which, remarkably, was published in 1949 — decades before anyone understood how badly weak instruments could bite.[^ar] It sat as a curiosity for fifty years and was rediscovered in the late 1990s as the gold standard for weak-instrument-robust inference.

[^ar]: Anderson, T. W., & Rubin, H. (1949). Estimation of the Parameters of a Single Equation in a Complete System of Stochastic Equations. *Annals of Mathematical Statistics*, 20(1), 46–63.

**The result, in one sentence:** instead of estimating $\beta$ and dividing by a shaky first stage, the Anderson–Rubin approach tests each *candidate value* of $\beta$ directly through the reduced form, building a confidence interval out of all the candidate values it cannot reject — and because it never divides by the first stage, it stays valid no matter how weak the instrument is.

Here is the mechanism, and it is genuinely clever. Suppose you want to test the hypothesis that the true effect equals some specific number, $H_0: \beta = \beta_0$. If that hypothesis were *true*, then the quantity $y - \beta_0 x$ — the outcome with the hypothesized treatment effect subtracted out — would be free of the causal effect of $x$, leaving only the structural error and whatever is unrelated to the treatment. Under exclusion, the instrument $z$ should have **no relationship** with this adjusted outcome, because $z$ only ever touched $y$ *through* $x$, and we have just removed $x$'s effect. So the test is:

> Form $y - \beta_0 x$. Regress it on the instrument $z$ (and controls). If $\beta_0$ is the true effect, the coefficient on $z$ must be zero. Test that with an ordinary $F$-test.

That is it. **No first stage appears anywhere.** You are testing a coefficient in a plain reduced-form regression of an observed, constructed variable on the instrument. There is no ratio, no denominator hugging zero, no division by a weak quantity. The $F$-test on $z$ in that regression is exactly valid in finite samples under the usual regression assumptions, *regardless of whether the instrument is strong or weak.* Whatever the first-stage strength, the Anderson–Rubin test keeps its promised size — a 5% test rejects a true null exactly 5% of the time.

To build a **confidence interval**, you invert the test: sweep $\beta_0$ across a grid of candidate values, run the Anderson–Rubin $F$-test at each one, and collect every $\beta_0$ the test *fails to reject* at the 5% level. That set is the 95% **Anderson–Rubin confidence interval** — by construction it contains the true $\beta$ in 95% of samples, weak instrument or not. Compare this to the conventional 2SLS interval, which is "estimate $\pm$ 1.96 standard errors" and inherits all the pathology of the ratio. The AR interval sidesteps the ratio entirely.

The price you pay for this honesty is that the AR interval can take *strange shapes* the conventional interval never does, and those shapes are not bugs — they are the procedure telling you the truth about how little the data know.

---

## 3.5.5 Reading the weird shapes: unbounded and empty AR intervals

Because the Anderson–Rubin interval is "the set of $\beta_0$ values we cannot reject," it is not forced to be a tidy symmetric segment around a point estimate. It can be **unbounded** (stretching to $\pm\infty$, or a finite interval plus two infinite rays), and it can even be **empty**. Both shapes carry a precise, useful message, and learning to read them is a skill.

**The unbounded interval: "the data cannot rule out a near-zero first stage."** Suppose the instrument is very weak. Then for almost any candidate $\beta_0$ you try, the adjusted outcome $y - \beta_0 x$ shows no significant relationship with $z$ — not because every $\beta_0$ is plausible, but because $z$ is so weakly related to *anything* that the test has no power to reject. The AR test fails to reject a huge range of $\beta_0$ values, and the confidence interval balloons, possibly to the whole real line. An **unbounded AR interval is the honest face of a weak instrument.** It says, in effect: "given how little this instrument moves the treatment, the data are consistent with almost any effect size, including enormous ones." The conventional 2SLS interval, faced with the identical weak instrument, would have reported something tight and specific — and would have been lying. The unbounded AR interval is what the conventional interval *should* have looked like. When you see an unbounded AR interval, the design has failed to identify the parameter, full stop; the appropriate conclusion is "this instrument cannot answer the question," not a number.

**The empty interval: "something is wrong with the model itself."** Stranger still, the AR interval can come back empty — *no* value of $\beta_0$ survives the test. This can only happen when the model is **over-identified** (more instruments than regressors), and it means the instruments *disagree* about $\beta$ so severely that no single value of $\beta$ can simultaneously make all of them uncorrelated with the adjusted outcome. An empty AR interval is a flashing red light on the **exclusion restriction or model specification**: it is the AR procedure detecting, through the same machinery, an overidentification failure. The instruments are not all valid, or the model is misspecified. An empty interval does not mean "no effect"; it means "your instruments cannot all be telling the truth."

Devon, reading his crypto paper, should now demand: *what does the Anderson–Rubin interval look like?* If the authors only report a 2SLS standard error and the first-stage $F$ is in the single digits, an honest AR interval might well be unbounded — in which case the paper's confident headline number is an artifact of dividing by a weak first stage, and the real answer is "we don't know."

---

## 3.5.6 The overidentification test: when surplus instruments check each other

Step back to over-identification, where you have more instruments than you strictly need. The bonus is a *testable implication of exclusion*, and the classical tool is the **overidentification test** — the **Sargan** test (Sargan, 1958)[^sargan] under homoskedasticity, generalized to the heteroskedasticity-robust **Hansen $J$** test (Hansen, 1982)[^hansen] inside the GMM framework that subsumes IV.

[^sargan]: Sargan, J. D. (1958). The Estimation of Economic Relationships Using Instrumental Variables. *Econometrica*, 26(3), 393–415.

[^hansen]: Hansen, L. P. (1982). Large Sample Properties of Generalized Method of Moments Estimators. *Econometrica*, 50(4), 1029–1054.

The logic is the same disagreement principle behind the empty AR interval, made into a single statistic. Each valid instrument, regressed against the IV residuals $\hat u = y - x\hat\beta_{\text{IV}}$, should show no relationship — a valid instrument is uncorrelated with the structural error by the exclusion restriction. With several instruments, you can ask jointly: *are all of them uncorrelated with the IV residual?* The Sargan/Hansen $J$ statistic measures the total correlation between the instruments and the residual; under the null that **all** instruments are valid, it follows a chi-squared distribution with degrees of freedom equal to the **number of over-identifying restrictions** — the number of surplus instruments, $L - 1$ when you have $L$ instruments for one regressor. A large $J$ (small $p$-value) **rejects** the joint null: at least one instrument is correlated with the error, i.e., at least one violates exclusion.

```python
import numpy as np
import pandas as pd
from linearmodels.iv import IV2SLS

# Over-identified IV with two instruments z1, z2 for one regressor x
# (df has columns: y, x, z1, z2, and a constant)
res = IV2SLS(df["y"], df[["const"]], df[["x"]], df[["z1", "z2"]]).fit()
print(res.summary)               # 2SLS point estimate and (conventional) SE
print(res.sargan)                # Sargan overidentification test
print(res.wooldridge_overid)     # robust (Hansen J-style) version
```

But read the test's limits, because they are severe and routinely ignored. **First, it tests only over-identifying restrictions, never the whole exclusion assumption.** If you have one instrument (just-identified), there are *zero* over-identifying restrictions and the test is empty — there is nothing to check. Even with several instruments, the test assumes that *enough* of them are valid to estimate $\beta$ in the first place; it can only detect *relative* disagreement. **If all your instruments are invalid in the same direction — all sharing the same back door — they will agree perfectly and the $J$ test will happily pass.** A clean $J$ is not a certificate of validity; it is the absence of evidence of *disagreement*. Second, the test has low power when instruments are weak (it inherits the weakness problem). Third, a rejection tells you *that* something is wrong, not *which* instrument. Like RESET in Chapter 2.5, the $J$ test is a flag, not a diagnosis — and a passed $J$ test is one of the most over-interpreted results in applied work. Exclusion remains, at bottom, an argument you must make, not a box a statistic can check.

---

## 3.5.7 Many-instruments bias: when more is worse

Here is the surprise that catches everyone. You have a weak instrument and you think: *more instruments means a stronger first stage, so let me add a dozen more.* Angrist and Krueger, in fact, did something like this — they interacted quarter of birth with year and state of birth to manufacture *hundreds* of instruments, hoping to strengthen identification. **It made things worse.** This is **many-instruments bias**, and it is one of the genuinely counterintuitive results in econometrics.

The intuition runs straight through the first-stage fitting. Recall that 2SLS replaces the endogenous $x$ with its first-stage fitted value $\hat x$ — the projection of $x$ onto the instruments. The trouble: with many instruments, that projection **overfits.** Each additional instrument, even a near-useless one, lets the first-stage regression chase a little more of the *idiosyncratic noise* in $x$ — and the noise in $x$ is exactly the endogenous part, the part correlated with the structural error. So the fitted $\hat x$ starts to recover the very endogeneity you used IV to purge, and in the extreme — as the number of instruments approaches the sample size — $\hat x$ approaches $x$ itself and **2SLS collapses back to OLS**, the worst case of the toward-OLS bias from Section 3.5.2. More instruments inflate the bias precisely by reintroducing the contamination.

This sharpens the rule of thumb. A "strong first stage" is not about piling up instruments until the $F$-test is significant; a high $F$ achieved by stuffing in many weak instruments is exactly the trap. **A few strong instruments beat many weak ones, always.** The right diagnostic is the **Olea–Pflueger effective $F$** from Chapter 3.4, which is built to flag weak identification honestly under heteroskedasticity and many-instrument settings — it does not reward you for adding junk.[^oleapflueger35]

[^oleapflueger35]: Montiel Olea, J. L., & Pflueger, C. (2013). A Robust Test for Weak Instruments. *Journal of Business & Economic Statistics*, 31(3), 358–369. If your effective $F$ is low, the fix is a *better* instrument, not *more* of them. Devon, if his paper has interacted ATM-distance with a dozen demographics to "boost the first stage," should treat the resulting estimate with *more* suspicion, not less.

---

## 3.5.8 Reproducing the disaster: a guided simulation

Now we do what Bound–Jaeger–Baker did in spirit: build a world where we *know* the true causal effect, plant a weak instrument, and watch 2SLS lie to us — then watch Anderson–Rubin and the effective $F$ catch the lie. This is the pathology of Lab 3 and notebook **nb3.5**, walked through here so you understand every line before you run it.

We construct a data-generating process with three features: $x$ is **endogenous** (correlated with the structural error $u$, so OLS is biased), the instrument $z$ is **valid** (uncorrelated with $u$, so exclusion holds — we are testing weakness, not invalidity), and crucially $z$ is **weak** (a small first-stage coefficient $\pi$, tunable). We set the true effect to $\beta = 0$ so that any nonzero estimate is pure bias — the cleanest possible demonstration, in the spirit of Maya's zero-discrimination world from Chapter 2.5.

```python
import numpy as np
import pandas as pd
from linearmodels.iv import IV2SLS
import statsmodels.api as sm

rng = np.random.default_rng(20260528)
N = 2_000
beta_true = 0.0          # TRUE effect is exactly zero
pi = 0.05                # first-stage strength: tiny -> weak instrument

# Shared shock makes x endogenous: corr(x, u) > 0, so OLS is biased UP.
z = rng.normal(size=N)                      # valid instrument
u = rng.normal(size=N)                      # structural error
v = rng.normal(size=N)
x = pi * z + 0.8 * u + v                     # weak first stage (pi) + endogeneity (0.8*u)
y = beta_true * x + u                        # exclusion holds: z absent from y given x

df = pd.DataFrame({"y": y, "x": x, "z": z})
df["const"] = 1.0

# OLS: biased toward the endogeneity (upward), as expected
ols = sm.OLS(df["y"], df[["const", "x"]]).fit()

# 2SLS with the weak instrument
iv = IV2SLS(df["y"], df[["const"]], df[["x"]], df[["z"]]).fit()

# First-stage strength
fs = sm.OLS(df["x"], df[["const", "z"]]).fit()
first_stage_F = fs.tvalues["z"] ** 2        # single instrument: F = t^2

print(f"OLS  beta_hat = {ols.params['x']:.3f}  (true 0.000)")
print(f"2SLS beta_hat = {iv.params['x']:.3f}  SE = {iv.std_errors['x']:.3f}")
print(f"first-stage F = {first_stage_F:.2f}")
```

Running it produces, up to simulation noise, something like:

```
OLS  beta_hat = 0.388   (true 0.000)
2SLS beta_hat = 0.281   SE = 0.214
first-stage F = 4.91
```

Read every number. OLS is badly biased upward — about $0.39$ against a truth of $0$ — exactly because $x$ shares the shock $u$ with the outcome. We turned to IV to fix this. But 2SLS reports about $0.28$: it has *not* purged the bias, it has merely *shrunk it partway toward OLS*, landing between OLS ($0.39$) and the truth ($0$), precisely as the $1/(F+1)$ story predicts with a low $F$. The first-stage $F$ of about $5$ is below 10 — the klaxon is sounding. And look at the standard error: $0.214$ gives a conventional 95% interval of roughly $0.28 \pm 1.96(0.214) \approx [-0.14,\ 0.70]$ — which happens to *contain* zero here, but is centered well away from it and far too narrow to be trusted, since the normal approximation underlying that SE is invalid at this first-stage strength. In many draws of this DGP the conventional interval *excludes* zero entirely: a confident, significant, completely false discovery of a positive effect.

Now the cure. We compute the Anderson–Rubin interval by inverting the test over a grid, and the Olea–Pflueger effective $F$.

```python
from scipy import stats

# Anderson-Rubin: for each candidate b0, regress (y - b0*x) on z; test coef on z = 0.
grid = np.linspace(-3, 3, 1201)
ar_not_rejected = []
for b0 in grid:
    adj = df["y"] - b0 * df["x"]                       # y - b0*x : remove hypothesized effect
    ar_fit = sm.OLS(adj, df[["const", "z"]]).fit()
    F_ar = ar_fit.tvalues["z"] ** 2                    # F-test that z has no effect
    if F_ar < stats.f.ppf(0.95, 1, N - 2):             # fail to reject at 5%
        ar_not_rejected.append(b0)

ar_lo, ar_hi = min(ar_not_rejected), max(ar_not_rejected)
print(f"AR 95% CI = [{ar_lo:.2f}, {ar_hi:.2f}]   (contains true 0? "
      f"{ar_lo <= 0 <= ar_hi})")

# Olea-Pflueger effective F (linearmodels reports it directly)
iv_robust = IV2SLS(df["y"], df[["const"]], df[["x"]], df[["z"]]).fit(cov_type="robust")
print(iv_robust.first_stage)        # effective F appears here; compare to OP critical values
```

The Anderson–Rubin interval comes back **wide** — something like $[-0.9,\ 1.4]$ — and it *contains the true value of zero*, honestly reflecting that this weak instrument simply cannot pin down the effect. If you crank $\pi$ down further (say $0.01$), the AR interval grows toward **unbounded**, the signature of Section 3.5.5: the data confess they cannot answer the question. Meanwhile the Olea–Pflueger effective $F$ sits below its critical value, formally flagging weak identification — the diagnostic doing its job. The contrast is the entire lesson in one screen: the conventional 2SLS interval is narrow and can falsely exclude the truth; the AR interval is wide, sometimes unbounded, and always honest.

Then flip the experiment to see the system working when it *should*. Set `pi = 0.8` — a strong instrument — and re-run. Now the first-stage $F$ is large (well above any critical value), 2SLS lands near the true zero (having genuinely purged OLS's bias), the conventional and AR intervals nearly coincide and are both tight, and the effective $F$ clears its threshold. **The machinery is not broken in general; it is broken by weakness.** With a strong instrument, every method agrees and IV delivers on its promise. The discipline is to *check* — first-stage $F$, effective $F$, and AR interval — before believing any 2SLS number, your own or a published paper's.

---

## 3.5.9 The IV reader's ledger

Collect the chapter into a checklist, the IV analog of Chapter 2.5's bias ledger. Confronting any IV result — in a paper or in your own output — run down this table. The right-hand column is the point: most entries are answered by *design and argument*, and only a few by a statistic.

| What to check | How to check it | What a bad answer looks like |
|---|---|---|
| **Relevance** | First-stage $F$ vs. Stock–Yogo / Olea–Pflueger critical value; effective $F$ | Single-digit $F$; "significant" first stage in a huge sample (BJB trap); $R^2$ reported instead of $F$ |
| **Exclusion** | Argument about back-door channels; overid ($J$) test *only if* over-identified | No discussion of alternative channels; reliance on $J$ test as "proof" of validity |
| **Compliers / LATE** | Who does the instrument move? Is that population interesting? | Abstract claims a universal effect from a complier-specific estimate |
| **Just- vs. over-identified** | Count instruments vs. endogenous regressors | Hundreds of weak interacted instruments (many-instruments bias) |
| **Weak-instrument bias** | $1/(F+1)$ pull toward OLS; effective $F$ | 2SLS estimate sitting suspiciously close to OLS with a low $F$ |
| **Honest inference** | Anderson–Rubin CI (valid even when weak) | Only a conventional 2SLS SE; no AR interval reported |
| **AR interval shape** | Bounded / unbounded / empty | Unbounded (unidentified) or empty (overid failure) hidden behind a tidy point estimate |
| **Overid test limits** | Sargan / Hansen $J$ | Passed $J$ read as "exclusion confirmed" (it isn't); empty for just-identified |

The deep moral connects back to where Week 2 left off. In Chapter 2.5 the lesson was that a regression cannot tell you whether its own coefficient is biased — the diagnostics live outside the regression, in the research design. IV is a *design* that, when it works, manufactures the exogenous variation OLS lacked. But IV has its own failure modes, and this chapter's lesson is the exact parallel: **a 2SLS standard error cannot tell you whether the instrument is strong enough to trust it.** The first-stage $F$, the effective $F$, and the Anderson–Rubin interval are the diagnostics that live *outside* the 2SLS point estimate. Devon's confident crypto paper, with its tight standard error and its three-stars coefficient, told him nothing about whether its instrument was strong. Only the first-stage $F$ and an AR interval could.

---

## 3.5.10 Where this goes next: from instruments to designs

This chapter closes Week 3, and with it the first half of the camp's causal-inference arc. Step back and see the shape of what you have learned. Week 3 took the regression machine of Week 2 — which Chapter 2.5 showed could be confidently, precisely wrong — and rebuilt causal inference on a sturdier foundation: the **potential-outcomes** framework (Ch 3.1), then three strategies for earning a causal number. Selection-on-observables (Ch 3.2–3.3) bets that you have measured the confounders and adjusts for them with matching, weighting, and doubly-robust estimators. Instrumental variables (Ch 3.4–3.5) gives up on measuring confounders and instead finds a source of *exogenous variation* — an instrument — to identify the effect for compliers, *if* relevance and exclusion hold and the first stage is strong. Each strategy trades one heroic assumption for another, and the art is knowing which assumption your setting can actually support.

But notice what every Week 3 method has in common: each leans on a *single cross-section* and a strong, often untestable assumption — conditional independence for matching, exclusion for IV. Week 4 changes the game by exploiting *structure in the data itself* — repetition over time and sharp thresholds in assignment — to weaken those assumptions. **Difference-in-differences** uses panels (the same units observed before and after a treatment) so that each unit serves as its own control, differencing away every fixed confounder you never measured. **Regression discontinuity** exploits an arbitrary cutoff — a credit score of exactly 620, a test score of exactly 70 — where units just above and just below are as-good-as-randomly assigned, manufacturing a local experiment at the threshold. **Synthetic control** builds a bespoke counterfactual for a single treated unit out of a weighted blend of untreated ones. These are **design-based** methods: the credibility comes from the *shape of the natural experiment*, not from a list of controls or the validity of an instrument. They are, in a sense, what Maya's fair-lending question and Devon's crypto question were waiting for.

You now know the three classic ways IV breaks — weak instruments, exclusion violations, many-instrument bias — and the three tools that catch them — the first-stage and effective $F$, the Anderson–Rubin interval, and the overidentification test. You can read an IV paper like a referee. Week 4 hands you a sharper set of designs that need fewer leaps of faith, and asks you to read those critically too.

---

## Your Turn

Open **`nb3.5`** (`notebooks/week-03/nb3.5-weak-iv-pathology.ipynb`), the weak-instrument pathology reproduction. You will (1) **build the disaster:** generate the endogenous-$x$, valid-but-weak-$z$, true-effect-zero DGP from Section 3.5.8, and confirm that 2SLS sits *between* OLS and the truth — quantify the pull and compare it to the $1/(F+1)$ prediction as you vary the first-stage strength $\pi$. (2) **Watch the conventional CI lie:** run the DGP across many simulated samples and record how often the conventional 2SLS 95% interval *excludes* the true zero — the empirical false-rejection rate, which should badly exceed 5% when the instrument is weak. (3) **Apply the cure:** compute the Anderson–Rubin interval by test inversion over a grid, verify its coverage *is* near 95% across the same simulations, and push $\pi$ toward zero until the AR interval goes **unbounded** — then add a second, equally-weak instrument and watch the *many-instruments bias* nudge 2SLS even closer to OLS while the Olea–Pflueger effective $F$ flags the weakness. (4) Finally, set $\pi = 0.8$ and confirm every method agrees when the instrument is strong.

**Check questions.**

1. A published IV paper reports a 2SLS coefficient of $0.42$ ($\text{SE} = 0.11$, three stars), an OLS coefficient of $0.55$, and a first-stage $F$ of $3.8$. (a) Using the $1/(F+1)$ heuristic, is the 2SLS estimate's proximity to OLS a coincidence or exactly what a weak instrument predicts? (b) Should you trust the tight standard error of $0.11$? Explain in one sentence what is wrong with it. (c) What single additional result would you demand from the authors before believing the coefficient, and what would it look like if the instrument were in fact too weak to identify the effect?

2. Leah instruments a firm's patenting with a policy change, computes the Anderson–Rubin 95% confidence interval, and gets back the *entire real line*, $(-\infty, +\infty)$. A coauthor says "great, that means the effect could be anything — let's report the 2SLS point estimate as our best guess." (a) What does an unbounded AR interval actually tell Leah about her instrument? (b) Is the coauthor's plan sound? Why or why not? (c) How could the AR interval instead come back *empty*, and what entirely different problem would that diagnose?

3. Sam has one weak instrument for a momentum-trading regression and decides to "fix" the weakness by interacting it with twenty market-state dummies to create twenty-one instruments, which raises the first-stage $F$-statistic above 10. (a) Has Sam actually strengthened his identification? Name the specific bias his strategy invites and explain the mechanism in terms of the first-stage fitted value $\hat x$. (b) Why is a single first-stage $F$ above 10 misleading here, and which diagnostic from Chapter 3.4 is designed to not be fooled? (c) If Sam now runs a Hansen $J$ overidentification test and it *passes* (large $p$-value), is he entitled to conclude his instruments satisfy exclusion? Explain.
