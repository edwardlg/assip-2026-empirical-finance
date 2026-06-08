# Chapter 1.5 — Hypothesis Testing Done Right

Sam has a trading rule. It is nothing fancy: each morning, buy a basket of stocks that went *down* the most yesterday, hold for one day, sell at the close. The idea is that yesterday's losers "bounce back" — a bet on short-term reversal. Sam backtests it on 252 trading days of last year's data and finds an average daily return of $0.08\%$. Eight basis points a day. Annualized, that is more than $20\%$. Sam is, briefly, very excited.

Then the doubt arrives, which is the right instinct and the subject of this chapter. Eight basis points is a *positive* average. But the daily returns bounced all over the place — some days up $1.5\%$, some days down $1.2\%$. With that much noise, could a rule that is *truly worthless* — a rule whose real edge is exactly zero — still produce a sample average of $+0.08\%$ over 252 days, just by luck? If the answer is "easily," then Sam has discovered nothing. If the answer is "almost never," then Sam may have discovered something.

That single question — *could pure luck have produced what I'm seeing?* — is the engine of hypothesis testing. Notice what kind of question it is. It is not "is the rule good?" or "what is the true edge?"; it is the narrower, sharper "*is what I observed too far from nothing to be nothing?*" Hypothesis testing answers that one question well and refuses to answer the others, and most of the mistakes in this chapter come from forgetting which question was asked. This chapter builds the machine that answers it carefully, names the ways it can lie to you, and corrects the three mistakes nearly every beginner makes. We close Week 1 here; everything we build will return in Week 2, when the thing being tested is a regression coefficient instead of an average.

We will follow the reveal-the-trick structure: state the result, see why it works on Sam's numbers, see when it fails, and run the code.

---

## 1.5.1 The two hypotheses

A hypothesis test starts by writing down two competing claims about the world — not about your *sample*, but about the *population* or process that generated it.

The **null hypothesis**, written $H_0$, is the claim of "nothing going on." It is the skeptic's position: the boring default that you will believe until the data force you off it. For Sam, the population quantity of interest is the *true* expected daily return of the rule, $\mu$ — the average return the rule would earn over an infinite number of days under the same conditions. The skeptic says the rule has no edge:

$$H_0: \mu = 0.$$

The **alternative hypothesis**, written $H_1$ (or $H_A$), is what you suspect might be true instead. Sam suspects the rule makes money:

$$H_1: \mu > 0.$$

Why $\mu = 0$ as the null, rather than, say, $\mu = 0.05\%$? Because zero is the value that means "the rule is worthless" — it is the dividing line between an edge and an anti-edge, and it is the thing a skeptic would assert costs nothing to believe. The null is generally chosen to be the *uninteresting* or *status-quo* value, the one whose rejection would constitute a discovery. Choosing it well is a scientific judgment, not a statistical one: it should encode what "no finding" means for your specific question. For Maya comparing two neighborhoods, "no finding" is *equal* approval rates, so her null is a difference of zero. For a study testing whether a new fee changes default rates, the null is "no change."

Three things deserve emphasis right away, because they are where the logic lives.

First, the hypotheses are statements about $\mu$, the unobservable population mean — *not* about $\bar{x}$, the sample average Sam actually computed. We know $\bar{x} = 0.08\%$ with certainty; there is nothing to test about a number we already hold. The whole exercise is about what $\bar{x}$ lets us *infer* about $\mu$.

Second, the test is deliberately asymmetric. We do not treat $H_0$ and $H_1$ as two equally-matched contestants. We grant $H_0$ the benefit of the doubt and ask whether the data can overturn it — the way a courtroom presumes innocence and asks the prosecution to overcome that presumption. This asymmetry is a *choice*, and it is the reason the conclusions of a test are phrased so carefully (Section 1.5.9).

Third, the null is almost always a *point* — a single value like $\mu = 0$ — precisely because a point gives us something concrete to compute with. If we assume $\mu = 0$ is exactly true, we can ask exactly how surprising Sam's $\bar{x} = 0.08\%$ would be. We cannot do that with a vague "the rule is bad."

---

## 1.5.2 The test statistic: turning data into a single ruler

The result, in one sentence: **a test statistic rescales your estimate into units of its own noise, so that "how far is the data from the null?" becomes a number you can look up in a known distribution.**

Here is the reasoning. Sam's $\bar{x} = 0.08\%$ looks small or large only relative to how much $\bar{x}$ *wobbles* from sample to sample. If daily returns barely vary, then $+0.08\%$ averaged over 252 days is a mountain. If they swing wildly, it is a pebble. So a raw distance from the null — here, $\bar{x} - 0 = 0.08\%$ — is uninterpretable on its own. We must divide it by a measure of its own variability.

Recall the central result from Chapter 1.4. If $x_1, \dots, x_N$ are independent draws with mean $\mu$ and finite variance $\sigma^2$, the Central Limit Theorem says the standardized sample mean converges in distribution to a standard normal:

$$\frac{\bar{x} - \mu}{\sigma / \sqrt{N}} \xrightarrow{d} N(0,1).$$

The denominator $\sigma/\sqrt{N}$ is the **standard error** of the mean — the standard deviation of $\bar{x}$ across hypothetical repeated samples. (Note the $\sqrt{N}$: collect four times as much data and the wobble halves. This is why sample size will matter so much below.)

Now do the one move that defines a test. *Assume the null is true* and substitute $\mu = 0$ into the CLT expression. Under $H_0$,

$$\frac{\bar{x} - 0}{\sigma/\sqrt{N}} \xrightarrow{d} N(0,1).$$

This is the **test statistic** in its idealized form: take your estimate, subtract the null value, divide by the standard error. The result is a pure number — Sam's eight basis points expressed in "standard errors above zero." A test statistic of $0.3$ means the data sit less than a third of a standard error from the null: utterly unremarkable. A test statistic of $4$ means four standard errors out: a place the null almost never visits.

There is one honest problem left, and fixing it gives us the $t$.

---

## 1.5.3 Deriving the t-test: what to do when you don't know $\sigma$

The expression above contains $\sigma$, the *true* population standard deviation of daily returns. Sam does not know it. Nobody ever does. We can only *estimate* it from the same sample, using the sample standard deviation

$$s = \sqrt{\frac{1}{N-1}\sum_{i=1}^{N}(x_i - \bar{x})^2}.$$

(The divisor is $N-1$, not $N$ — the Bessel correction from Chapter 1.3, which makes $s^2$ an unbiased estimator of $\sigma^2$. We "spent" one degree of freedom estimating $\bar{x}$, so only $N-1$ pieces of independent information about spread remain.)

Replacing the unknown $\sigma$ with the estimated $s$ gives the statistic we actually compute, the **t-statistic**:

$$t = \frac{\bar{x} - \mu_0}{s/\sqrt{N}},$$

where $\mu_0$ is the value of $\mu$ under the null (here $\mu_0 = 0$). The quantity $s/\sqrt{N}$ is the **estimated standard error**, written $\widehat{\operatorname{se}}(\bar{x})$.

Swapping $s$ for $\sigma$ is not free. We have replaced a fixed constant with a *random* quantity — $s$ jiggles from sample to sample just as $\bar{x}$ does — and dividing by something random adds extra uncertainty, fattening the tails. William Gosset worked out the exact consequence in 1908, publishing under the pen name "Student" because his employer (the Guinness brewery) forbade staff publications. The result: when the underlying data are normal, the statistic $t$ does *not* follow a standard normal. It follows **Student's t-distribution** with $N-1$ degrees of freedom, written $t \sim t_{N-1}$.

The $t$-distribution is shaped like the normal — symmetric, bell-like, centered at zero — but with heavier tails that account for the extra uncertainty in $s$. Extreme values are a little more likely under the $t$ than under the normal, which is exactly the penalty you should pay for not knowing $\sigma$. The fewer the degrees of freedom, the fatter the tails: with $N-1 = 4$, the tails are noticeably heavy; with $N-1 = 30$, the $t$ is already almost indistinguishable from the normal.

And here is the clean bridge back to Chapter 1.4. As $N \to \infty$, $s \xrightarrow{p} \sigma$ — the sample standard deviation converges to the truth — so the random denominator stops being random, and the $t$-distribution converges to the $N(0,1)$ the CLT promised:

$$t_{N-1} \xrightarrow{d} N(0,1) \quad \text{as } N \to \infty.$$

This is why you will hear practitioners use the words "t-statistic," "z-statistic," and "the rule of 2" almost interchangeably for large samples. With $N=252$, Sam's $t$-distribution has 251 degrees of freedom and is normal for all practical purposes. The distinction between $t$ and $z$ earns its keep in *small* samples — a study of 12 firms, a clinical trial of 20 patients — where the tail correction genuinely changes the answer. Use the $t$ by default; it costs nothing and is correct in finite samples (when the data are roughly normal), and it gracefully becomes the normal when $N$ is large.

One more point of rigor, because it is the assumption that will break first. The exact $t_{N-1}$ result requires the *underlying data* to be normally distributed — daily returns drawn from a normal. Real returns are not normal: they are fat-tailed (extreme days happen far more often than a normal predicts) and often skewed. So why do we still use the $t$? Because of the CLT itself. Even when the $x_i$ are non-normal, the *numerator* $\bar{x}$ is approximately normal for large $N$, and the whole statistic is approximately $t$ (hence approximately normal). The exact small-sample $t$ distribution is a luxury that requires normal data; the large-sample approximation is robust and requires only finite variance and enough observations. With $N = 252$ this approximation is excellent. With $N = 8$ and fat-tailed returns, neither the exact nor the approximate result is trustworthy — a failure mode we flag now and confront repeatedly later.

**Sam's numbers.** Say the 252 daily returns have $\bar{x} = 0.08\%$ and sample standard deviation $s = 0.75\%$. Then

$$\widehat{\operatorname{se}}(\bar{x}) = \frac{0.75\%}{\sqrt{252}} = \frac{0.75\%}{15.87} = 0.0473\%, \qquad t = \frac{0.08\%}{0.0473\%} \approx 1.69.$$

Sam's average sits about $1.69$ estimated standard errors above zero. Notice the role of $N$ in that denominator: had Sam run the rule for only one quarter — $N = 63$ days — the same $\bar{x}$ and $s$ would give $\widehat{\operatorname{se}} = 0.75\%/\sqrt{63} = 0.0945\%$ and $t \approx 0.85$, less than half as large and nowhere near significant. *Identical average return, opposite conclusion*, purely because of how much data backed it. This is the single most important practical lesson of the standard error: a result is only as convincing as the sample size beneath it. Is $t = 1.69$ far enough to overturn the skeptic? To answer, we need to decide *in advance* how surprised we must be before we act — which is the language of size and power.

---

## 1.5.4 Size (Type I error) and power (Type II error)

Any decision rule based on noisy data can be wrong in two distinct ways. Laying them out in a table is the single most clarifying thing you can do.

| | $H_0$ is true (no edge) | $H_1$ is true (real edge) |
|---|---|---|
| **We reject $H_0$** | Type I error (false positive) | Correct (a "hit") |
| **We fail to reject $H_0$** | Correct | Type II error (false negative) |

A **Type I error** is rejecting a null that is actually true: declaring Sam's worthless rule a winner. We *choose* a ceiling on how often we are willing to make this mistake, called the **significance level** or **size** of the test, written $\alpha$. The convention $\alpha = 0.05$ means: "I will tolerate wrongly crying victory on a truly dead rule at most $5\%$ of the time." Crucially, $\alpha$ is set *before* seeing the data, and it is a property of the *rule*, not of any one dataset.

The rule itself: reject $H_0$ when the test statistic lands in the **rejection region** — the set of statistic values so extreme that they would occur with probability only $\alpha$ if $H_0$ were true. For Sam's one-sided alternative $H_1: \mu > 0$ at $\alpha = 0.05$ with 251 degrees of freedom, the **critical value** is the point cutting off the top $5\%$ of the $t_{251}$ distribution, which is about $1.65$. The rule is: reject if $t > 1.65$.

A **Type II error** is failing to reject a null that is actually false: missing a rule that genuinely works. Its probability is written $\beta$. The quantity we usually care about is its complement,

$$\text{power} = 1 - \beta = \Pr(\text{reject } H_0 \mid H_1 \text{ is true}),$$

the probability of *catching* a real effect when one exists. A test with low power is a metal detector that stays silent over buried treasure — it protects you from false alarms (small $\alpha$) by almost never alarming at all, which is useless.

The two error rates trade off against each other, and four levers move them:

- **Lower $\alpha$** (demand more evidence) shrinks the rejection region, cutting false positives but also lowering power. You cannot drive both errors to zero at once with fixed data.
- **A bigger true effect** is easier to detect, so power rises as the real $\mu$ moves farther from $\mu_0$.
- **Less noise** ($s$ smaller) sharpens the test, raising power.
- **More data** ($N$ larger) shrinks the standard error $s/\sqrt{N}$, which is the lever you usually control. This is why **power analysis** — computing, before collecting data, the $N$ needed to detect an effect of a given size with, say, $80\%$ power — is standard practice in serious empirical work and a part of every well-designed study.

It is worth making power concrete with one calculation, because "power" stays abstract until you compute it. Suppose the reversal rule's *true* edge is $\mu = 0.05\%$ per day, with $\sigma = 0.75\%$. Over $N = 252$ days the standard error is $0.0473\%$, so the true mean sits $0.05\%/0.0473\% \approx 1.06$ standard errors above zero. The rejection rule (one-sided, $\alpha = 0.05$) fires when $t > 1.65$. The probability of that, *given the true mean*, is the chance a normal centered at $1.06$ exceeds $1.65$ — that is, $\Pr(Z > 1.65 - 1.06) = \Pr(Z > 0.59) \approx 0.28$. So a rule with a genuine $0.05\%$ daily edge would be detected only about $28\%$ of the time in a single year of data. That is *low power*: nearly three times in four, a real edge this size would slip past Sam's test unnoticed. To reach $80\%$ power for the same effect with this one-sided test, Sam would need the true mean to sit $z_{0.05} + z_{0.20} = 1.645 + 0.84 = 2.485$ standard errors above zero, i.e. $\sqrt{N} = 2.485\,\sigma/\mu = 2.485 \times 0.75\%/0.05\% = 37.3$, so $N \approx 1{,}390$ days — about five and a half years. (Demand a *two-sided* test instead and the bar rises to $1.96 + 0.84 = 2.80$ standard errors, pushing the requirement to $N \approx 1{,}760$ days, about seven years — the power cost of two-sidedness you will quantify in the problem set.) This is exactly the kind of arithmetic a power analysis produces before you commit to a study, and it explains why a non-rejection from a short backtest proves so little.

Sam's actual $t = 1.69$ exceeds the one-sided critical value $1.65$, so the rule clears the $\alpha = 0.05$ bar — barely. Before celebrating, notice how marginal "barely" is, and ask the question we have been deferring: exactly how surprising is $t = 1.69$?

---

## 1.5.5 One-sided vs. two-sided tests

The shape of $H_1$ decides where the rejection region sits, and you must commit to it *before* looking at the data.

Sam had a directional prior — the reversal rule was *supposed* to make money — so $H_1: \mu > 0$ is a **one-sided (one-tailed) test**, with the entire $\alpha = 0.05$ rejection region in the upper tail (critical value $\approx 1.65$).

Contrast Maya, who is comparing loan-approval rates between two neighborhoods and testing whether they differ. She has no prior about *which* is higher; either direction would be a finding. Her null and alternative are

$$H_0: \mu_A - \mu_B = 0, \qquad H_1: \mu_A - \mu_B \neq 0,$$

a **two-sided (two-tailed) test**. Now the $5\%$ must be split across both tails — $2.5\%$ in each — so the critical value moves out to about $\pm 1.96$ (the famous "1.96" of large-sample testing). A two-sided test is more conservative: you need a larger statistic in absolute value to reject, because you reserved part of your error budget for surprises in the other direction.

This creates an obvious temptation and an absolute rule. The temptation: run a two-sided test, see the effect is positive, then *retroactively* claim you "always meant" the one-sided test to get the easier $1.65$ cutoff. That is cheating — it secretly doubles your true Type I rate from $5\%$ to effectively $10\%$, because you gave yourself two bites. **Choose the sidedness from the science before you see the data.** When in genuine doubt, use two-sided; it is the honest default, and most published finance results are reported two-sided for exactly this reason. Sam can justify one-sided only because the reversal hypothesis was directional from the start — and even then, reporting both is the cautious move.

---

## 1.5.6 The p-value, defined correctly

Critical values give a yes/no verdict at a fixed $\alpha$. The **p-value** reports something richer: *how* extreme the data are, on a continuous scale. Here is the definition, and it must be memorized in exactly this form:

> The **p-value** is the probability, *computed assuming the null hypothesis is true*, of observing a test statistic at least as extreme as the one you actually got.

Read it slowly. Everything is conditioned on $H_0$ being true. We live inside the skeptic's world — $\mu = 0$ — and ask: in that world, how often would noise alone hand me a result this striking or more so? A small p-value means "this data would be a real surprise if the null were true," which is evidence *against* the null.

For Sam's one-sided test, the p-value is the area in the upper tail of the $t_{251}$ distribution beyond $1.69$:

$$p = \Pr(T \geq 1.69 \mid H_0),\qquad T \sim t_{251},$$

which works out to about $0.046$. Since $0.046 < 0.05$, Sam rejects $H_0$ at the $5\%$ level — the same verdict the critical value gave, which is no accident: **the p-value is below $\alpha$ exactly when the statistic is past the critical value.** They are two views of one comparison. For a two-sided test you double the one-tail area: a statistic of $1.96$ gives a two-sided $p \approx 0.05$.

Now the correction that matters more than almost anything else in this book.

> **The p-value is NOT the probability that the null hypothesis is true.** Sam's $p = 0.046$ does **not** mean "there is a $4.6\%$ chance the rule has no edge."

The p-value is $\Pr(\text{data this extreme} \mid H_0 \text{ true})$. The thing students *want* it to be is $\Pr(H_0 \text{ true} \mid \text{data})$. These are different conditional probabilities, and swapping the two sides of a conditional bar is a basic probabilistic error — the same error as confusing $\Pr(\text{wet} \mid \text{rain})$ with $\Pr(\text{rain} \mid \text{wet})$. To even *speak* of "the probability the null is true" you would need a prior probability that the null is true and Bayes' rule to update it; a p-value contains no prior and makes no such statement. It assumes $H_0$ outright and never questions it. The hypothesis is treated as fixed; the *data* are the random thing whose extremeness we measure.

A second, related caution: a p-value is itself a random variable. Run Sam's backtest on a fresh year and you would get a different $\bar{x}$, a different $t$, and a different p-value. A $p$ of $0.046$ and a $p$ of $0.055$ are practically the same evidence; the $0.05$ line is a useful convention, not a law of nature, and treating it as a cliff edge is a habit worth distrusting. In fact there is a clean and underappreciated theorem here: *when the null is true, the p-value is uniformly distributed on $[0,1]$.* Every value is equally likely — which is exactly why a true null still produces $p < 0.05$ a full $5\%$ of the time, and is the seed of the multiple-testing problem in Section 1.5.10. A small p-value from a single test is *mild* surprise; only when it would be surprising across everything you tried does it carry weight.

---

## 1.5.7 Confidence intervals as inverted tests

A p-value answers one question — "can I reject *this particular* null?" A **confidence interval (CI)** answers all of them at once, and is often the more honest object to report.

Start from the test. We *fail* to reject a candidate null value $\mu_0$ at level $\alpha$ exactly when the statistic is not extreme — when $|t| \le t^*$, where $t^*$ is the two-sided critical value. Writing that out,

$$\left| \frac{\bar{x} - \mu_0}{s/\sqrt{N}} \right| \le t^* \quad\Longleftrightarrow\quad \bar{x} - t^*\,\frac{s}{\sqrt{N}} \;\le\; \mu_0 \;\le\; \bar{x} + t^*\,\frac{s}{\sqrt{N}}.$$

The set of *all* null values $\mu_0$ that survive the test is precisely the interval

$$\left[\, \bar{x} - t^*\,\widehat{\operatorname{se}}(\bar{x}), \;\; \bar{x} + t^*\,\widehat{\operatorname{se}}(\bar{x}) \,\right].$$

That is the $100(1-\alpha)\%$ confidence interval. **A confidence interval is simply the collection of null hypotheses you cannot reject** — a test, inverted. For Sam, with $t^* \approx 1.97$ at $251$ degrees of freedom, the $95\%$ CI for $\mu$ is

$$0.08\% \pm 1.97 \times 0.0473\% = [\,-0.013\%,\; 0.173\%\,].$$

Two things to read off it. First, $0$ *is* inside this two-sided $95\%$ interval — consistent with the fact that Sam's *one-sided* test only barely cleared its bar and a two-sided test at $5\%$ would not reject. Second, the interval shows the full range of edges compatible with the data: from a tiny loss to a sizable $0.17\%$ daily gain. That range is wide, and its width is the standard error scaled up — the honest measure of how little 252 days really pin down.

The interpretation of "confidence" deserves the same care as the p-value. The correct statement is about the *procedure*: if we repeated the whole experiment many times, $95\%$ of the intervals so constructed would contain the true $\mu$. It is **not** correct to say "there is a $95\%$ probability that $\mu$ lies in *this* particular interval." Once computed, the interval either contains $\mu$ or it does not; the $95\%$ describes the long-run hit rate of the *method*, not the realized interval. Same logic as before: $\mu$ is fixed, the interval is the random thing.

---

## 1.5.8 Effect size vs. statistical significance

Here is a scenario that should bother you. Suppose Sam scales up the backtest to $N = 100{,}000$ days of simulated data (a long high-frequency study), and finds the same $\bar{x} = 0.0008\%$ — eight *ten-thousandths* of a percent — with the standard error now tiny because $\sqrt{N}$ is huge. The t-statistic could be $5$, the p-value microscopic, the result "wildly significant." And it would be worthless. Eight ten-thousandths of a percent per day does not survive a single basis point of trading costs. It is a real, detectable, *economically meaningless* effect.

This is the distinction every empirical scientist must keep straight:

- **Statistical significance** asks: *can I distinguish this effect from zero?* It is a statement about precision, and it is largely controlled by sample size. With enough data, almost any effect — however trivial — becomes statistically significant, because the standard error shrinks toward zero.
- **Effect size** (also "economic significance" or "practical significance") asks: *is the effect large enough to matter?* For Sam: is the edge big enough, after costs, to be worth trading? For Maya: is a 3-percentage-point gap in approval rates large enough to harm real borrowers? This is a question about the *magnitude* of $\bar{x}$ or $\hat{\beta}$, in the units of the problem — and no p-value can answer it.

> **Statistical significance is not economic significance.** A significant result can be trivially small; an insignificant result can be economically huge but measured too noisily to confirm.

The two questions can disagree in *both* directions, and it helps to hold all four cases in mind. (1) Significant *and* large: the dream — a real, big effect, well measured. (2) Significant but tiny: Sam's $100{,}000$-day example, where huge $N$ makes a trivial effect "detectable." (3) Insignificant but large: a $0.3\%$ daily edge measured over just 10 days, where the point estimate is enormous but the standard error is enormous too — the most dangerous case, because a beginner reads "not significant" as "no effect" and discards a possibly real signal. (4) Insignificant and small: genuinely nothing to see. Only the verdict plus the magnitude plus the interval lets you tell these apart; the p-value alone collapses all four into "star" or "no star."

The discipline this demands: **always report the estimate and its confidence interval, not just a verdict.** Sam's "$\bar{x}=0.08\%$, 95% CI $[-0.01\%, 0.17\%]$" tells you both the best guess *and* the range of plausible truths — including, here, the uncomfortable fact that "no edge at all" is barely inside the interval. A bare "p < 0.05" hides all of that. This is also why this book's empirical-spec discipline (from the Conventions) insists you state magnitudes and units, never just stars on a coefficient. Asterisks are not findings.

---

## 1.5.9 Three mistakes to never make

Three errors are so common, and so corrosive, that we name them explicitly.

**1. "The p-value is the probability the null is true."** Covered in 1.5.6, repeated here because it is the most frequent error in all of applied statistics. The p-value assumes the null and measures the data's extremeness *given* that assumption. It says nothing about the probability of the hypothesis. Reciting the correct definition until it is automatic is time well spent.

**2. "We accept the null."** When a test fails to reject $H_0$, we say exactly that — **fail to reject** — and never "accept" or "prove" the null. Absence of evidence is not evidence of absence. If Sam's $t$ had come out at $0.4$, the right conclusion is "this sample cannot distinguish the rule's edge from zero," *not* "the rule has zero edge." Maybe the edge is real but small, and 252 days is too few to detect it — a power problem, not a proof of nullity. A null that survives a *low-powered* test has survived nothing; it was never seriously challenged. The confidence interval makes this concrete: failing to reject means $0$ is *inside* the interval, but so are many non-zero values you also cannot rule out.

**3. "Statistical significance settles the matter."** Covered in 1.5.8. A small p-value tells you an effect is probably not exactly zero. It does not tell you the effect is large, important, robust, causal, or real outside your sample. Those are separate questions, and the rest of this book is largely about them.

---

## 1.5.10 An honest preview: multiple testing and p-hacking

We end Week 1 with a warning that Week 1 only *previews* — the full treatment of multiple-testing corrections comes later in the program.

Return to Sam, but change one detail. Suppose Sam did not test *one* rule. Sam tested *twenty* — reversal, momentum, day-of-week, moon phase, the lot — kept the one with $p < 0.05$, and reported only that winner. Has Sam found something? Almost certainly not, and here is the arithmetic.

If the null is true for a single rule, the probability of a false positive at $\alpha = 0.05$ is, by construction, $5\%$. Now suppose *all twenty* rules are truly worthless, and (for the illustration) their tests are independent. The probability that *at least one* of them crosses $p < 0.05$ by pure luck is

$$1 - (1 - 0.05)^{20} = 1 - 0.95^{20} \approx 1 - 0.358 = 0.64.$$

There is a $64\%$ chance — better than a coin flip — that at least one dead rule looks "significant," simply because Sam gave luck twenty tries. Test enough worthless ideas and you are *guaranteed* a spurious winner. The per-test error rate $\alpha$ was never designed to survive being applied dozens of times and then cherry-picked.

This is the heart of **p-hacking** (also "data dredging"): running many analyses — many rules, many variable definitions, many subsamples, many control sets — and reporting only the ones that crossed the significance line, as though that single test had stood alone. The reported p-value is then a lie, because it ignores the nineteen silent attempts behind it. The problem is general and is sometimes called the "garden of forking paths": even a single analysis involves dozens of small choices, each a hidden test.

Two honest defenses, which we will build properly later:

- **Pre-registration** — committing to your hypotheses and analysis *before* seeing the data — removes the ability to fish, because the forking paths are nailed down in advance.
- **Multiple-testing corrections** adjust the bar when you run many tests. The crude **Bonferroni** rule, for instance, tests each of $m$ hypotheses at $\alpha/m$ instead of $\alpha$, so the chance of *any* false positive stays near $\alpha$. More refined approaches control the **false discovery rate (FDR)** — the expected *fraction* of your "discoveries" that are false — which is usually the more sensible target when you are screening many candidate signals at once, as in finance and genomics.

For now, take away only the intuition: **the false-positive rate of a single test does not protect a search across many tests.** When you read a paper claiming a trading rule, a risk factor, or a treatment effect, the first question is always "how many things did they try before they found this one?" We treat FDR and the formal corrections in full later in the program; here we only want you to never again be impressed by a lone p-value pulled from an unnamed crowd.

---

## 1.5.11 Where this goes next

Step back and see what you built. A test statistic is an estimate divided by its standard error. The t-statistic is that idea made operational when the variance must itself be estimated — leaning on the CLT from Chapter 1.4, finite-sample-honest through the $t$-distribution, and normal again in the limit. Size and power are the two ways to be wrong and the levers that trade between them. The p-value, defined correctly, measures the data's extremeness under the null and *nothing else*. A confidence interval is the whole family of un-rejectable nulls. And effect size — not significance — is what tells you whether any of it matters.

Now look at the t-statistic one more time: estimate, minus null value, divided by standard error. In Week 2 we build the **OLS regression engine**, and its core output is a coefficient $\hat{\beta}$ that estimates how one variable moves with another. To ask "does $X$ actually move with $Y$, or is this noise?" you will compute $t = (\hat{\beta} - 0)\,/\,\widehat{\operatorname{se}}(\hat{\beta})$ — the *exact same machine* you just built, pointed at a slope instead of a mean. Every idea in this chapter reappears there, which is why we spent so long getting it right.

---

## Your Turn

Open **`nb1.5`** (`notebooks/week-01/nb1.5-power-and-the-t-test.ipynb`). You will build the t-test from scratch on Sam's reversal-rule returns — computing $\bar{x}$, $s$, the standard error, the t-statistic, and the p-value by hand and then checking them against `scipy.stats.ttest_1samp`. You will then simulate **power curves**: fix $\alpha = 0.05$, vary the true effect $\mu$ and the sample size $N$, and plot $1-\beta$ to *see* how power climbs with effect size and with $\sqrt{N}$. The capstone exercise reproduces the multiple-testing simulation from 1.5.10: test 20 worthless rules a thousand times over and watch the false-positive rate balloon toward $64\%$.

**Check questions.**

1. Sam reports "$p = 0.03$, so there's a $3\%$ chance the rule has no real edge." State precisely what is wrong with this sentence, and give the correct interpretation of $p = 0.03$ for the one-sided test $H_0: \mu = 0$ vs. $H_1: \mu > 0$.

2. Maya runs a two-sided test of whether two neighborhoods' approval rates differ and gets a $95\%$ confidence interval for the difference of $[-1.2\%, +6.8\%]$. (a) Will she reject $H_0$ at $\alpha = 0.05$? How do you know from the interval alone? (b) A colleague says "the gap is not statistically significant, so the neighborhoods are treated equally." What two distinct errors is the colleague making?

3. A fund tests 40 independent signals, all in truth worthless, each at $\alpha = 0.05$. (a) What is the approximate probability that at least one signal comes out "significant"? (b) If the fund wants the chance of *any* false positive held to about $5\%$ using the Bonferroni rule, what per-test significance level should it use, and what is the corresponding two-sided critical value's rough direction of change (larger or smaller in absolute value)?
