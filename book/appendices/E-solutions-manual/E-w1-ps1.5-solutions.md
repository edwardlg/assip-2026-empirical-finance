# Solutions — Problem Set 1.5 (Power, Size, and Confidence Intervals)

Full worked solutions to `book/weeks/week-01/ps1.5.md`, covering Chapter 1.5. Notation follows the
Conventions: $\bar{x}$ sample mean, $s$ sample standard deviation, $\mu$ population mean, $\mu_0$ the
null value, $\widehat{\operatorname{se}}(\bar{x}) = s/\sqrt{N}$ the estimated standard error. With $N$
in the hundreds the $t_{N-1}$ and $N(0,1)$ cutoffs agree to the displayed precision, so we use the
normal cutoffs ($1.645$, $1.96$, $2.326$, $2.576$) throughout. The recurring theme of the answer key:
**every interpretation is conditioned on the null and says nothing about the probability that a
hypothesis is true.**

---

## Problem 1 — The t-statistic and the p-value, by hand (16 pts)

**(a)** [4 pts] The estimated standard error is
$$\widehat{\operatorname{se}}(\bar{x}) = \frac{s}{\sqrt{N}} = \frac{0.75\%}{\sqrt{252}}
= \frac{0.75\%}{15.87} = 0.0473\%.$$
The t-statistic, with $\mu_0 = 0$, is
$$t = \frac{\bar{x} - \mu_0}{\widehat{\operatorname{se}}(\bar{x})} = \frac{0.08\%}{0.0473\%} \approx 1.69.$$
Sam's average sits about $1.69$ estimated standard errors above zero.

**(b)** [3 pts] The one-sided critical value at $\alpha = 0.05$ is $1.645$. Since $t = 1.69 > 1.645$
— equivalently $p = 0.046 < 0.05$ — Sam **rejects $H_0$** at the $5\%$ level (barely). The two
verdicts must agree because the p-value is, by construction, the tail area beyond the observed
statistic, and "$p < \alpha$" is the same inequality as "statistic past the critical value" read from
opposite ends of the same tail: the critical value is exactly the statistic whose tail area equals
$\alpha$.

**(c)** [6 pts]
(i) The error is the **transposed conditional** (the "prosecutor's fallacy"): treating the p-value as
the probability that the null hypothesis is true. This is *the* most common mistake in applied
statistics (Section 1.5.6 / 1.5.9 Mistake 1).
(ii) Correct interpretation: *"If the rule truly had no edge ($\mu = 0$), the probability of observing
a sample mean at least as far above zero as Sam's — a t-statistic of $1.69$ or larger — is about
$4.6\%$."* That is, $p = \Pr(T \ge 1.69 \mid H_0)$ with $T \sim t_{251}$.
(iii) Sam has swapped the two sides of a conditional bar. The p-value is
$\Pr(\text{data this extreme} \mid H_0 \text{ true})$; Sam read it as
$\Pr(H_0 \text{ true} \mid \text{data})$. These are different quantities, just as
$\Pr(\text{wet}\mid\text{rain}) \neq \Pr(\text{rain}\mid\text{wet})$. To obtain
$\Pr(H_0 \mid \text{data})$ one would need a prior probability on $H_0$ and Bayes' rule; a p-value
contains neither, because it *assumes* $H_0$ outright and only measures how surprising the data are
under that assumption.

**(d)** [3 pts] Unwarranted. The p-value is itself a **random variable** — a fresh year of data
yields a different $\bar{x}$, $t$, and $p$ — and when the null is true the p-value is uniformly
distributed on $[0,1]$, so values like $0.046$ and $0.055$ are essentially the same evidence and
straddle the $0.05$ line by chance alone. The $0.05$ threshold is a convention, not a cliff; nothing
about the rule's edge need have changed between the two years.

---

## Problem 2 — Size: what $\alpha$ does and does not promise (15 pts)

**(a)** [4 pts] By definition of size, the probability of rejecting $H_0$ on any single day when
$H_0$ is true is exactly $\alpha = 0.05$. So the screener fires a false "buy" with probability
$5\%$ per day. The meaning of $\alpha = 0.05$: it is the **long-run false-positive rate of the
testing rule** — the ceiling Devon set, in advance, on how often a *truly worthless* signal would be
called significant. It is a property of the **rule**, not of any particular dataset; a single day's
data is either rejected or not, with no "$5\%$" attached to it.

**(b)** [5 pts] With $20$ independent days each rejecting with probability $0.05$, the count of false
alerts is Binomial$(20, 0.05)$.
- Expected number of false alerts: $20 \times 0.05 = 1$ alert per month.
- Probability of at least one false alert:
$$1 - (1 - 0.05)^{20} = 1 - 0.95^{20} = 1 - 0.358 \approx 0.642.$$
So even with a genuinely worthless signal, Devon should *expect* about one false buy a month and has a
$64\%$ chance of at least one in any given month.

**(c)** [3 pts] The cost is **lower power** (a higher Type II / false-negative rate, $\beta$).
Mechanism: lowering $\alpha$ to $0.01$ moves the critical value farther into the tail (from $1.645$ to
$2.326$ one-sided), shrinking the rejection region; that same shrinkage makes it harder to reject when
a *real* signal exists, so genuine edges are missed more often. You cannot reduce both error types at
once with fixed data.

**(d)** [3 pts] **False.** $\alpha$ is $\Pr(\text{reject} \mid H_0 \text{ true})$, not
$\Pr(H_0 \text{ true} \mid \text{reject})$ — the fraction of *issued alerts* that are mistaken is the
latter (the false discovery proportion), a different conditional. That fraction depends on how many of
the signals tested actually had a real edge (the base rate) and on the test's power; if most signals
are worthless, the great majority of alerts can be false even though $\alpha = 0.05$. Same transposed-
conditional trap as Problem 1(c), now applied to size.

---

## Problem 3 — Power and the sample size for 80% (20 pts)

**(a)** [4 pts] Standard error at $N = 252$:
$$\frac{\sigma}{\sqrt{N}} = \frac{0.75\%}{\sqrt{252}} = 0.0473\%.$$
Noncentrality (true mean in standard-error units):
$$\frac{\mu}{\sigma/\sqrt{N}} = \frac{0.05\%}{0.0473\%} \approx 1.06.$$
The true effect sits about $1.06$ standard errors above the null.

**(b)** [6 pts] Approximate power by the upper-tail piece:
$$\text{power} \approx \Pr(Z > 1.96 - 1.06) = \Pr(Z > 0.90) \approx \Pr(Z > 0.84\text{–}1.00).$$
Interpolating the supplied table between $\Pr(Z>0.84)=0.200$ and $\Pr(Z>1.00)=0.159$ gives
$\Pr(Z>0.90) \approx 0.18$. (Accept any answer in the range $0.18$–$0.19$.) **Interpretation:** even
if the disclosure rule genuinely moves returns by $0.05\%$ a day, a two-sided test on a single year of
data would detect it only about $18\%$ of the time — the test is badly **underpowered**, so a
non-rejection here would tell us almost nothing.

*(Note: this is lower than the $\approx 28\%$ power figure in Section 1.5.4 because that worked example
used a* one-sided *test, with cutoff $1.645$ rather than $1.96$. Two-sided testing costs power, which
is exactly the trade-off of Problem 5.)*

**(c)** [7 pts] Set the noncentrality to the value that delivers $80\%$ power in a two-sided $5\%$
test, $1.96 + 0.84 = 2.80$:
$$\frac{\mu}{\sigma/\sqrt{N}} = 2.80 \;\Longrightarrow\; \frac{\mu\sqrt{N}}{\sigma} = 2.80
\;\Longrightarrow\; \sqrt{N} = \frac{2.80\,\sigma}{\mu} = \frac{2.80 \times 0.75\%}{0.05\%} = 42.0.$$
Therefore
$$N = 42.0^2 = 1{,}764 \text{ days}.$$
At $252$ trading days per year, $1{,}764 / 252 = 7.0$ years. Detecting a $0.05\%$ daily effect with
$80\%$ power requires about **seven years** of data — which is why a single-year backtest proves so
little about an effect of this size.

**(d)** [3 pts] Unjustified. With power around $18\%$ (part b), this study was almost designed to miss
a real effect of the plausible size; failing to reject a null in a **low-powered** test means the null
was never seriously challenged, so the result is uninformative, not confirmatory. The correct
conclusion is **"fail to reject $H_0$"** — *"this sample cannot distinguish the disclosure rule's
effect from zero"* — never **"accept $H_0$"** or "the rule has no effect" (Section 1.5.9, Mistake 2:
absence of evidence is not evidence of absence). The $0.05\%$ effect remains entirely compatible with
the data.

---

## Problem 4 — Confidence interval as an inverted test (18 pts)

**(a)** [5 pts]
$$\bar{x} \pm 1.96\,\widehat{\operatorname{se}}(\bar{x}) = 0.08\% \pm 1.96 \times 0.0473\%
= 0.08\% \pm 0.0927\%.$$
So the $95\%$ CI for $\mu$ is
$$[\,-0.013\%,\; 0.173\%\,].$$

**(b)** [4 pts] Yes, $\mu_0 = 0$ lies inside $[-0.013\%, 0.173\%]$. Therefore the **two-sided test at
$\alpha = 0.05$ fails to reject $H_0: \mu = 0$.** General principle: the $100(1-\alpha)\%$ confidence
interval is *exactly the set of null values $\mu_0$ that the two-sided level-$\alpha$ test would fail
to reject* — the test, inverted. A value lies in the interval iff
$|\bar{x} - \mu_0|/\widehat{\operatorname{se}} \le t^*$, which is precisely the non-rejection
condition. Reading "is $0$ in the interval?" is the same act as running the test.

**(c)** [3 pts] No contradiction. The one-sided test puts the *entire* $5\%$ in the upper tail
(cutoff $1.645$), while the two-sided test splits it into $2.5\%$ per tail (cutoff $1.96$); Sam's
$t = 1.69$ clears $1.645$ but not $1.96$. The $95\%$ two-sided CI corresponds to the $\pm 1.96$,
two-sided test, so it being unable to reject $0$ is consistent with the more lenient one-sided test
rejecting. They are different tests with different error budgets, not the same test giving two
answers.

**(d)** [6 pts]
(i) Wrong because, once computed, the interval $[-0.013\%, 0.173\%]$ is a fixed set of numbers and
$\mu$ is a fixed (if unknown) constant: the true mean either is or is not in this interval, so the
probability is $0$ or $1$, not $0.95$. The "$95\%$" is not a probability attached to *this* realized
interval.
(ii) Correct interpretation: *"If we repeated the entire experiment many times and built a CI each
time by this procedure, about $95\%$ of those intervals would contain the true $\mu$."* The $95\%$
describes the long-run hit rate of the **method**, not the realized interval; $\mu$ is fixed, the
interval is the random thing.
(iii) The **width** ($\approx 0.19$ percentage points wide) reports the *precision* of the estimate
and the full range of edges compatible with the data — from a small daily *loss* ($-0.013\%$) up to a
sizable $0.17\%$ daily gain. A bare "fail to reject" would hide that the data are consistent both with
"no edge" and with an economically meaningful edge; the interval shows how little $252$ days actually
pin $\mu$ down. (Accept any one correct reading: precision / range of plausible values / that a
meaningful effect is not ruled out.)

---

## Problem 5 — One- vs. two-sided, and the temptation (12 pts)

**(a)** [4 pts] Leah has no directional prior — an effect in either direction would be a finding — so
she should run a **two-sided** test. Her hypotheses:
$$H_0: \mu = 0, \qquad H_1: \mu \neq 0,$$
(where $\mu$ is the mean abnormal return around the patent-disclosure event). At $\alpha = 0.05$ the
$5\%$ is split into $2.5\%$ per tail, giving critical value $\pm 1.96$.

**(b)** [5 pts] It is cheating because the sidedness of a test must be chosen from the **science,
before seeing the data** — Sam chose it *after* observing the sign of the estimate, specifically to
clear the lower bar. Doing so gives Sam, in effect, two chances to reject (he would have switched to a
one-sided test in whichever direction the estimate landed), which **doubles the true Type I error rate
from the nominal $5\%$ to about $10\%$.** The reported "$\alpha = 0.05$" is then false; the rule no
longer controls size at $5\%$. (With $t = 1.80$: it fails the honest two-sided cutoff $1.96$ but is
made to pass the after-the-fact one-sided cutoff $1.645$ — exactly the manipulation described.)

**(c)** [3 pts] The rule (Section 1.5.5): **"Choose the sidedness from the science before you see the
data."** "When in genuine doubt, use two-sided" is the honest default because it reserves part of the
error budget for a surprise in either direction, cannot be gamed after the fact, and matches how most
published finance results are reported — so it protects you from accidentally (or conveniently)
inflating your false-positive rate.

---

## Problem 6 — Multiple testing and a Bonferroni fix (19 pts)

**(a)** [5 pts] With $k = 20$ independent tests of true nulls, each rejecting with probability
$\alpha = 0.05$:
$$\Pr(\text{at least one false positive}) = 1 - (1 - 0.05)^{20} = 1 - 0.95^{20}
= 1 - 0.358 \approx 0.642.$$
**Interpretation:** there is about a $64\%$ chance — better than a coin flip — that at least one of
the twenty worthless rules looks "significant" at $\alpha = 0.05$ by luck alone. Sam's "winning" rule
is therefore very likely a statistical artifact, not a discovery: testing many dead rules and keeping
the best one practically *manufactures* a spurious $p < 0.05$.

**(b)** [3 pts] **P-hacking** (data dredging) is running many analyses — here, $20$ rules — and
reporting only the one(s) that crossed the significance line as though that single test had stood
alone. The reported $p < 0.05$ on the winner is "a lie" because the $5\%$ false-positive guarantee
attaches to *one pre-specified test*; it silently ignores the nineteen other attempts, so the true
probability that *some* reported rule is a false positive is the $64\%$ of part (a), not $5\%$.

**(c)** [6 pts]
(i) Bonferroni per-test level: $\alpha/k = 0.05/20 = 0.0025$ (i.e. $0.25\%$).
(ii) The critical value rises from $1.96$ to about $2.576$ (two-sided), so a rule now needs a
**larger** t-statistic (in absolute value) to be declared significant — the bar is raised because each
test gets a smaller slice of the error budget.
(iii) Family-wise false-positive rate under the corrected level:
$$1 - (1 - 0.0025)^{20} = 1 - 0.9975^{20} = 1 - 0.951 \approx 0.049 \approx 0.05. \checkmark$$
So testing each of the twenty rules at $0.25\%$ brings the chance of *any* false positive back down to
about $5\%$, as intended. (Bonferroni is slightly conservative — $0.049 \le 0.05$ — which is the
expected, safe direction.)

**(d)** [5 pts] We need the smallest integer $k$ with
$$1 - 0.95^k > 0.5 \quad\Longleftrightarrow\quad 0.95^k < 0.5.$$
Using the supplied values: at $k = 13$, $1 - 0.95^{13} = 1 - 0.513 = 0.487 < 0.5$ (not yet); at
$k = 14$, $1 - 0.95^{14} = 1 - 0.488 = 0.512 > 0.5$. So the smallest such $k$ is
$$\boxed{k = 14}.$$
Test about **fourteen** worthless rules and you are already more likely than not to crown at least one
spurious "winner." **Practical lesson:** the first question to ask of any reported trading-rule
(or factor, or treatment) p-value is *"how many things were tried before this one was found?"* — a
lone p-value pulled from an unnamed crowd of attempts carries almost no evidential weight.

---

*Key takeaway across the set: a p-value and a confidence level are statements conditioned on the null
(or on the procedure), never probabilities that a hypothesis is true; significance is not effect size;
failing to reject is not proof of the null; and the per-test error rate does not survive a search
across many tests.*
