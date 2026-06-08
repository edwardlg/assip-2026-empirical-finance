# Problem Set 1.5 — Power, Size, and Confidence Intervals

**Covers Chapter 1.5 (Hypothesis Testing Done Right).** Methods through Ch 1.5 only: the
one-sample $t$-statistic, size and power, one- vs. two-sided tests, the p-value defined correctly,
confidence intervals as inverted tests, and the multiple-testing preview. Use the notation from the
Conventions: $\bar{x}$ is the sample mean, $s$ the sample standard deviation, $\mu$ the population
mean, $\mu_0$ the null value, and $\widehat{\operatorname{se}}(\bar{x}) = s/\sqrt{N}$ the estimated
standard error.

Six problems, escalating, **100 points total**. Each is self-contained. Where a normal or $t$
tail probability is needed, the relevant values are supplied in the problem so you can work by hand;
with $N$ in the hundreds the $t_{N-1}$ distribution is indistinguishable from the standard normal, so
you may use the normal cutoffs $1.645$ (one-sided $5\%$), $1.96$ (two-sided $5\%$), and $2.326$
(one-sided $1\%$) freely. Show every step: a correct number with a wrong interpretation earns half
credit at most, because in this chapter the interpretation *is* the skill.

Useful standard-normal tail areas, $\Pr(Z > z)$:

| $z$ | 0.30 | 0.50 | 0.59 | 0.84 | 1.00 | 1.28 | 1.645 | 1.96 | 2.00 | 2.326 |
|-----|------|------|------|------|------|------|-------|------|------|-------|
| $\Pr(Z>z)$ | 0.382 | 0.309 | 0.278 | 0.200 | 0.159 | 0.100 | 0.050 | 0.025 | 0.023 | 0.010 |

---

## Problem 1 — The t-statistic and the p-value, by hand (16 points)

Sam runs the one-day reversal rule for a full year and records $N = 252$ daily returns with sample
mean $\bar{x} = 0.08\%$ and sample standard deviation $s = 0.75\%$. The hypotheses, fixed in advance
from the directional reversal story, are $H_0: \mu = 0$ versus $H_1: \mu > 0$.

**(a)** [4 pts] Compute the estimated standard error $\widehat{\operatorname{se}}(\bar{x}) = s/\sqrt{N}$
and the t-statistic $t = (\bar{x} - \mu_0)/\widehat{\operatorname{se}}(\bar{x})$. Keep three
significant figures.

**(b)** [3 pts] The one-sided p-value works out to $p \approx 0.046$. Using $\alpha = 0.05$, state
the decision (reject or fail to reject $H_0$) and explain in one sentence why the p-value verdict and
the critical-value verdict must always agree.

**(c)** [6 pts] Sam writes in the backtest log: *"$p = 0.046$, so there is only a $4.6\%$ chance the
rule truly has no edge."* This sentence is wrong. (i) Identify the error by name. (ii) Write the
correct one-sentence interpretation of $p = 0.046$ for this specific test. (iii) Explain, using the
language of conditional probability, exactly which two quantities Sam has swapped.

**(d)** [3 pts] Sam reruns the identical rule on a *different* year of data and gets $p = 0.055$.
Sam concludes the rule "stopped working between the two years." Give the one-sentence reason this
conclusion is unwarranted, citing the relevant property of the p-value as a random variable.

---

## Problem 2 — Size: what $\alpha$ does and does not promise (15 points)

Devon builds an automated screener that, every morning, runs a one-sided $t$-test at $\alpha = 0.05$
on a *single* crypto-momentum signal, asking $H_0: \mu = 0$ versus $H_1: \mu > 0$. Assume that for
this signal the null is in fact true — the signal is genuinely worthless — and that each day's test
is independent of the others.

**(a)** [4 pts] On any one day, what is the probability the screener fires a "buy" alert (rejects
$H_0$)? State the precise meaning of the number $\alpha = 0.05$ in this context, being careful to
say whether it is a property of a dataset or of the testing rule.

**(b)** [5 pts] Over a $20$-trading-day month, what is the expected number of false "buy" alerts, and
what is the probability of *at least one* false alert? (Use $1 - 0.95^{20} \approx 0.642$.)

**(c)** [3 pts] Devon lowers the bar to $\alpha = 0.01$ to cut down on false alerts. Name the cost
of this change in terms of the *other* error type, and explain the mechanism in one sentence.

**(d)** [3 pts] True or false, with a one-sentence justification: *"Because the screener uses
$\alpha = 0.05$, at most $5\%$ of the buy alerts it has ever issued were mistakes."* (Careful — this
is a statement about a different conditional probability than $\alpha$.)

---

## Problem 3 — Power and the sample size for 80% (20 points)

Priya is studying whether a new climate-risk disclosure rule changes the average daily abnormal
return of exposed insurers. She will run a **two-sided** test, $H_0: \mu = 0$ versus
$H_1: \mu \neq 0$, at $\alpha = 0.05$ (critical value $\pm 1.96$). Suppose the *true* mean effect is
$\mu = 0.05\%$ per day and the standard deviation of daily abnormal returns is $\sigma = 0.75\%$.
(Treat $\sigma$ as known and use the normal approximation throughout, so the standard error is
$\sigma/\sqrt{N}$.)

**(a)** [4 pts] With $N = 252$ days, compute the standard error and the **noncentrality** — the
number of standard errors the true mean sits above $\mu_0 = 0$, i.e. $\mu/(\sigma/\sqrt{N})$.

**(b)** [6 pts] Power for a two-sided test is the probability the statistic clears $+1.96$ *or* falls
below $-1.96$ when the truth is $\mu = 0.05\%$. The lower-tail piece is negligible here; approximate
power by the upper piece, $\Pr(Z > 1.96 - \text{noncentrality})$. Compute the approximate power at
$N = 252$ and state in plain English what it means about Priya's chance of detecting a real effect of
this size.

**(c)** [7 pts] Priya wants $80\%$ power. For $80\%$ power in a two-sided $5\%$ test, the required
noncentrality is $1.96 + 0.84 = 2.80$ (the $0.84$ comes from $\Pr(Z > 0.84) = 0.20$). Set
$\mu/(\sigma/\sqrt{N}) = 2.80$ and solve for the required $N$. Round up to a whole number of days and
convert it to *years* (252 trading days per year).

**(d)** [3 pts] Priya's actual study has only $N = 252$ days and returns $p = 0.21$ (not
significant). A co-author writes: *"The disclosure rule has no effect on returns."* Explain why this
conclusion is unjustified, and state the correct conclusion in the vocabulary of Section 1.5.9.

---

## Problem 4 — Confidence interval as an inverted test (18 points)

Use Sam's year again: $\bar{x} = 0.08\%$, $\widehat{\operatorname{se}}(\bar{x}) = 0.0473\%$,
$N = 252$. Use the two-sided $5\%$ critical value $1.96$.

**(a)** [5 pts] Construct the $95\%$ confidence interval for $\mu$,
$\bar{x} \pm 1.96\,\widehat{\operatorname{se}}(\bar{x})$. Report the endpoints in percent to three
decimals.

**(b)** [4 pts] Is $\mu_0 = 0$ inside the interval? State the decision of the *two-sided* test at
$\alpha = 0.05$ that you can read off directly from this fact, and explain the general principle —
why the CI *is* the test, inverted.

**(c)** [3 pts] Reconcile this with Problem 1: Sam's *one-sided* test rejected $H_0$ at
$\alpha = 0.05$, yet the *two-sided* $95\%$ CI contains $0$. Explain in two sentences why there is no
contradiction.

**(d)** [6 pts] A classmate reads Sam's interval and says: *"There is a $95\%$ probability that the
true edge $\mu$ lies between $-0.013\%$ and $0.173\%$."* (i) State precisely why this is the wrong
interpretation of a confidence interval. (ii) Give the correct frequentist interpretation in one
sentence. (iii) Beyond the verdict, name one thing the *width* of this interval tells Sam that a bare
"reject / fail to reject" would hide.

---

## Problem 5 — Sam's trading rule: one- vs. two-sided, and the temptation (12 points)

Sam is designing the *next* backtest and must commit to the test's sidedness in advance.

**(a)** [4 pts] Sam's reversal hypothesis is directional — losers are *supposed* to bounce back, so
only $\mu > 0$ would count as success. Sam therefore plans a one-sided test at $\alpha = 0.05$
(critical value $1.645$). Leah is instead testing whether a *new* patent-disclosure event moves
returns at all, with no directional prior. State the appropriate sidedness for Leah, write her $H_0$
and $H_1$, and give her critical value.

**(b)** [5 pts] After collecting data, Sam computes $t = 1.80$. Sam first ran a *two-sided* test
(critical value $1.96$), saw the failure to reject, noticed the estimate was positive, and then
re-labeled the test as one-sided (critical value $1.645$) to reject. Explain exactly why this is
cheating, and state what it does to the *true* size of Sam's test. (A number or a clear directional
statement is required.)

**(c)** [3 pts] State the one-sentence rule from Section 1.5.5 that prevents this abuse, and explain
why "when in genuine doubt, use two-sided" is the honest default.

---

## Problem 6 — Multiple testing and a Bonferroni fix (19 points)

Sam, chastened, admits the year's "winning" reversal rule was actually the best of **$k = 20$** rules
tested — reversal, momentum, day-of-week, moon phase, and sixteen others — each tested once at
$\alpha = 0.05$, with only the winner reported. Assume for this problem that *all twenty rules are
truly worthless* and that the twenty tests are independent.

**(a)** [5 pts] Compute the probability that *at least one* of the twenty worthless rules crosses
$p < 0.05$ by pure luck, using the formula $1 - (1-\alpha)^k$. (You may use $0.95^{20} \approx 0.358$.)
Interpret the number in one sentence: what does it say about Sam's "discovery"?

**(b)** [3 pts] Define **p-hacking** in one or two sentences as it applies to what Sam did, and
explain why the reported $p < 0.05$ on the winning rule is, in your words, "a lie."

**(c)** [6 pts] To hold the **family-wise** false-positive rate (the chance of *any* false positive
across all twenty tests) at about $5\%$, apply the **Bonferroni** rule: test each rule at
$\alpha/k$ instead of $\alpha$. (i) Compute the Bonferroni per-test level for $k = 20$. (ii) The
corresponding two-sided critical value rises from $1.96$ to about $2.576$; does a rule now need a
*larger* or *smaller* t-statistic to be declared significant? (iii) Verify the fix roughly works by
computing $1 - (1 - 0.0025)^{20}$ and comparing it to $0.05$. (Use $0.9975^{20} \approx 0.951$.)

**(d)** [5 pts] Sam asks: *"How many worthless rules would I need to test before I'm more likely than
not — over $50\%$ — to get at least one false 'winner' at $\alpha = 0.05$?"* Set up the inequality
$1 - 0.95^k > 0.5$ and solve for the smallest integer $k$. (You may use that $0.95^{13} \approx 0.513$
and $0.95^{14} \approx 0.488$.) State the practical lesson in one sentence: what is the first question
you should ask of any reported trading-rule p-value?

---

*End of Problem Set 1.5. Solutions: Appendix E, `E-w1-ps1.5-solutions.md`. The companion notebook
`nb1.5` lets you check Problems 1, 3, and 6 by simulation.*
