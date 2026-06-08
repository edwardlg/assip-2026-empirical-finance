# Chapter 2.4 — When the Errors Misbehave: Heteroskedasticity, Clustering, HC/HAC

Maya has a clean-looking result and a problem she cannot name yet.

She is studying fair lending. She has pulled a dataset of $N = 9{,}000$ consumer loans — the
kind of mid-prime installment loans a lot of her own friends' families actually use — and she
wants to know whether borrowers in a particular ZIP-code tier get charged higher interest
rates after controlling for credit score, loan size, and income. She runs the regression her
laptop makes easy. Out comes a coefficient on her tier variable of $\hat\beta_1 = 0.42$
percentage points, with a standard error of $0.07$. The t-statistic is $0.42 / 0.07 = 6.0$.
Six. That is not "marginally significant"; that is a coefficient screaming through a megaphone.
She writes it up.

Then her mentor asks one question: *"Are those 9,000 loans really 9,000 independent pieces of
evidence?"*

They are not. The loans cluster by lender, and lenders set rates in correlated ways. They
cluster by state, and states have correlated regulation and correlated local economies. Once
Maya accounts for that, the *same* coefficient $\hat\beta_1 = 0.42$ comes back with a standard
error of $0.19$, and the t-statistic collapses from $6.0$ to $2.2$. Still significant — but
the megaphone is now a normal speaking voice, and a referee could reasonably push back.

Here is the unsettling part, and it is the whole chapter in one line: **her point estimate
never moved.** The $0.42$ was right the whole time. What was wrong was the $0.07$ — the number
that tells you how much to *trust* the $0.42$. In Ch 2.2 we proved that OLS is unbiased and,
under the Gauss–Markov assumptions, the best linear unbiased estimator. None of that breaks
here. What breaks is the *standard error*, and therefore every t-statistic, every p-value,
every confidence interval you build on top of it.

> **The one-sentence result of this chapter:** When the errors are heteroskedastic or
> correlated, $\hat{\boldsymbol\beta}$ is still fine — but the classical standard-error formula
> lies, and you must replace it with a robust, clustered, or HAC formula that tells the truth.

We are going to take this apart carefully, because "your point estimate is fine, your t-stat
lies" is one of the most important and most misunderstood facts in all of applied
econometrics. We will start exactly where Ch 2.2 left us — with the classical variance formula
— watch it break, and build the replacement.

---

## 1. Where we start: the classical variance and the assumption holding it up

Recall the setup from Ch 2.1. We write the model in matrix form,

$$
\mathbf{y} = \mathbf{X}\boldsymbol\beta + \boldsymbol\varepsilon ,
$$

where $\mathbf{y}$ is the $N\times 1$ vector of outcomes (Maya's interest rates), $\mathbf{X}$
is the $N\times K$ matrix of regressors (a column of ones for the intercept, plus tier, credit
score, loan size, income), $\boldsymbol\beta$ is the $K\times 1$ vector of coefficients we
want, and $\boldsymbol\varepsilon$ is the $N\times 1$ vector of errors — everything about each
loan's rate that our regressors do not explain. The OLS estimator is

$$
\hat{\boldsymbol\beta} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y} .
$$

Now substitute $\mathbf{y} = \mathbf{X}\boldsymbol\beta + \boldsymbol\varepsilon$ into that and
simplify (the $\mathbf{X}\boldsymbol\beta$ part collapses to $\boldsymbol\beta$, which is the
algebra behind unbiasedness):

$$
\hat{\boldsymbol\beta} = \boldsymbol\beta + (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\boldsymbol\varepsilon .
$$

This little equation is the engine room of the whole chapter. Read it slowly. The estimator
equals the truth, $\boldsymbol\beta$, plus a *sampling-error term*
$(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\boldsymbol\varepsilon$ that depends on which particular
errors $\boldsymbol\varepsilon$ the universe happened to deal this sample — exactly the
"what if the draw had been different" question from Ch 1.3, now in matrix clothing. The whole
variance of $\hat{\boldsymbol\beta}$ comes from that second term.

Take its variance, treating $\mathbf{X}$ as fixed (conditioning on $\mathbf{X}$, as in Ch 2.2):

$$
\operatorname{Var}(\hat{\boldsymbol\beta}\mid \mathbf{X})
= (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\,
\underbrace{\operatorname{Var}(\boldsymbol\varepsilon \mid \mathbf{X})}_{=\;\boldsymbol\Omega}\,
\mathbf{X}(\mathbf{X}'\mathbf{X})^{-1} .
$$

I have given the middle object a name: $\boldsymbol\Omega = \operatorname{Var}(\boldsymbol\varepsilon\mid\mathbf{X})$,
the $N\times N$ **variance–covariance matrix of the errors.** Its diagonal entries are the
variances of each error, $\operatorname{Var}(\varepsilon_i)$; its off-diagonal entries are the
covariances between errors of different observations, $\operatorname{Cov}(\varepsilon_i,\varepsilon_j)$.
*Everything* in this chapter is a story about what $\boldsymbol\Omega$ really looks like.

In Ch 2.2 we made the **homoskedasticity-and-no-correlation** assumption:

$$
\operatorname{Var}(\boldsymbol\varepsilon \mid \mathbf{X}) = \boldsymbol\Omega = \sigma^2 \mathbf{I}.
$$

In plain language, that single equation makes two claims at once. First, **homoskedasticity**
("same scatter"): every error has the *same* variance $\sigma^2$, regardless of the regressors
— a \$2,000 loan and a \$40,000 loan have rates that are equally hard to predict, in squared
dollars. That puts the same $\sigma^2$ all down the diagonal. Second, **no correlation across
observations**: the errors of any two different loans are uncorrelated, so every off-diagonal
entry is zero. Together they make $\boldsymbol\Omega$ a scalar times the identity matrix — a
matrix with $\sigma^2$ on the diagonal and zeros everywhere else.

Plug $\boldsymbol\Omega = \sigma^2\mathbf{I}$ into the sandwich and watch it collapse. The
middle $\sigma^2$ is a scalar and slides out front; the $\mathbf{I}$ vanishes; one
$\mathbf{X}'\mathbf{X}$ cancels against an inverse:

$$
\operatorname{Var}(\hat{\boldsymbol\beta}\mid\mathbf{X})
= \sigma^2 (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}
= \sigma^2 (\mathbf{X}'\mathbf{X})^{-1} .
$$

That is the **classical variance formula** from Ch 2.2. The standard error of any single
coefficient $\hat\beta_j$ is the square root of the $j$-th diagonal entry of
$\hat\sigma^2(\mathbf{X}'\mathbf{X})^{-1}$, where $\hat\sigma^2 = \frac{1}{N-K}\sum_i \hat\varepsilon_i^2$
is the usual estimate of the error variance built from the residuals $\hat\varepsilon_i$. It is
clean, it is fast, and it is what your software prints by default.

It is also only as true as the assumption $\boldsymbol\Omega = \sigma^2\mathbf{I}$. The rest of
this chapter is what happens when that assumption is false — which, in finance data, is
basically always.

---

## 2. Reveal the trick: the sandwich never went away

Here is the key idea, and it is liberating once you see it. We did **not** need
$\boldsymbol\Omega = \sigma^2\mathbf{I}$ to write down the variance. The honest formula is the
full **sandwich**:

$$
\boxed{\;\operatorname{Var}(\hat{\boldsymbol\beta}\mid\mathbf{X})
= (\mathbf{X}'\mathbf{X})^{-1}\,\mathbf{X}'\boldsymbol\Omega\,\mathbf{X}\,(\mathbf{X}'\mathbf{X})^{-1}\;}
$$

The name is literal. The two $(\mathbf{X}'\mathbf{X})^{-1}$ factors are the slices of bread; the
$\mathbf{X}'\boldsymbol\Omega\mathbf{X}$ in the middle is the filling. The classical formula is
just the sandwich for the special diet $\boldsymbol\Omega = \sigma^2\mathbf{I}$. If the real
$\boldsymbol\Omega$ has *different* variances on the diagonal (heteroskedasticity) or *nonzero*
off-diagonals (correlation), the bread is unchanged but the filling is different — and so the
final standard errors are different.

This reframes the entire problem. We are never going to "fix" $\hat{\boldsymbol\beta}$; there is
nothing wrong with it. The whole game is **estimating the middle of the sandwich,
$\mathbf{X}'\boldsymbol\Omega\mathbf{X}$, without pretending $\boldsymbol\Omega = \sigma^2\mathbf{I}$.**

That sounds impossible at first. $\boldsymbol\Omega$ is an $N\times N$ matrix — with $N = 9{,}000$
loans that is 81 million entries, and we have only 9,000 data points. We cannot estimate
81 million numbers from 9,000 observations. This is the genuine difficulty, and the next three
sections are three different clever answers to it:

- **White / HC (Section 3):** We don't need $\boldsymbol\Omega$ itself, only the sandwiched
  combination $\mathbf{X}'\boldsymbol\Omega\mathbf{X}$, which is a small $K\times K$ matrix. If
  errors are *uncorrelated* (diagonal $\boldsymbol\Omega$), we can estimate that small thing
  directly using each observation's own squared residual.
- **Clustered (Section 4):** If errors are correlated *within groups but not across them*,
  $\boldsymbol\Omega$ is block-diagonal, and we estimate the middle using whole blocks.
- **HAC / Newey–West (Section 5):** If errors are correlated *across time* in a way that fades
  with distance, we estimate the middle using nearby observations with decaying weights.

Same sandwich every time. Only the recipe for the filling changes.

### 2.1 A two-observation sandwich you can do by hand

Abstract matrices hide what is going on, so let us collapse the sandwich to the smallest case
that still shows the mechanism: a *single* regressor (no intercept), so $\mathbf{X}$ is just a
column of numbers and the whole sandwich becomes ordinary arithmetic. Suppose we have only the
simplest model $y_i = \beta x_i + \varepsilon_i$. Then $\mathbf{X}'\mathbf{X} = \sum_i x_i^2$ is
a single number, and the sandwich for a diagonal $\boldsymbol\Omega$ reads

$$
\operatorname{Var}(\hat\beta) = \frac{\sum_i x_i^2\,\sigma_i^2}{\left(\sum_i x_i^2\right)^2}.
$$

Now compare two worlds with the same regressors $x = (1, 2, 3, 4)$, so $\sum_i x_i^2 = 30$.

*World A (homoskedastic):* every $\sigma_i^2 = 1$. The numerator is
$\sum_i x_i^2 \cdot 1 = 30$, so $\operatorname{Var}(\hat\beta) = 30 / 30^2 = 1/30 \approx 0.033$.
This is exactly the classical answer $\sigma^2/\sum x_i^2 = 1/30$.

*World B (heteroskedastic):* the scatter grows with $x$, say $\sigma_i^2 = x_i^2$, so the
variances are $(1, 4, 9, 16)$. The numerator is now
$\sum_i x_i^2 \cdot x_i^2 = 1 + 16 + 81 + 256 = 354$, so
$\operatorname{Var}(\hat\beta) = 354 / 900 \approx 0.393$ — almost **twelve times larger.** The
classical formula, which would still report $1/30 \approx 0.033$ here (it averages the variances
and forgets that the big-variance points are also the high-$x$, high-leverage points), would
understate the true standard error by a factor of $\sqrt{0.393/0.033} \approx 3.5$. A t-stat of
$3.5$ would *really* be a t-stat of $1$. That is the entire heteroskedasticity problem in four
data points, and notice it required no calculus and no asymptotics — just plugging the right
$\sigma_i^2$ into the middle of the sandwich instead of pretending they are all equal. The rest
of Section 3 is only about how to *estimate* those $\sigma_i^2$ when, unlike here, nobody hands
them to you.

---

## 3. Heteroskedasticity: White / HC standard errors

### 3.1 What heteroskedasticity is, in a picture

Priya, working her insurance-claims data, has the cleanest possible example. She regresses the
size of a wildfire claim on the insured value of the property. A \$200,000 cabin can produce a
claim anywhere from \$0 (false alarm) to \$200,000 (total loss) — a spread of \$200,000. A
\$5 million estate can produce a claim anywhere from \$0 to \$5 million — a spread twenty-five
times wider. The *scatter of the errors grows with the regressor.* That is
**heteroskedasticity** ("different scatter"): $\operatorname{Var}(\varepsilon_i)$ depends on
$i$, so the diagonal of $\boldsymbol\Omega$ is not a single repeated $\sigma^2$ but a list of
different $\sigma_i^2$:

$$
\boldsymbol\Omega = \operatorname{diag}(\sigma_1^2, \sigma_2^2, \dots, \sigma_N^2).
$$

The off-diagonals are still zero — Priya's claims are independent across unrelated properties —
so this is a *purely* heteroskedastic, still-uncorrelated case. The classical formula
$\sigma^2(\mathbf{X}'\mathbf{X})^{-1}$ uses one average $\hat\sigma^2$ everywhere, which means
it systematically misprices the uncertainty: too small where the true scatter is large, too
large where it is small. There is no general rule for which way the *overall* t-stat goes — but
it is wrong, and in finance it is usually wrong in the direction of overconfidence.

### 3.2 White's idea (1980)

Halbert White's insight was to stop chasing the impossible $N\times N$ object and look at what
we actually need. Write the middle of the sandwich for a diagonal $\boldsymbol\Omega$. Because
the off-diagonals are zero, the matrix product $\mathbf{X}'\boldsymbol\Omega\mathbf{X}$ becomes
a simple sum over observations:

$$
\mathbf{X}'\boldsymbol\Omega\mathbf{X} = \sum_{i=1}^{N} \sigma_i^2\,\mathbf{x}_i \mathbf{x}_i' ,
$$

where $\mathbf{x}_i$ is the $K\times 1$ row of regressors for observation $i$ (written as a
column). This is a $K\times K$ matrix — for Maya, $5\times 5$ — no matter how big $N$ is. We do
*not* need each $\sigma_i^2$ on its own; we need this weighted sum. And White's trick is that
each unknown $\sigma_i^2$ can be replaced by the single thing we observe for that point: its
**squared residual** $\hat\varepsilon_i^2$. Any one $\hat\varepsilon_i^2$ is a terrible
estimate of $\sigma_i^2$ — it's based on one data point. But summed up across all $N$
observations, the errors in those guesses average out, and the *sum* converges to the right
thing. That gives the **heteroskedasticity-consistent (HC) estimator**:

$$
\widehat{\operatorname{Var}}(\hat{\boldsymbol\beta})_{\text{HC0}}
= (\mathbf{X}'\mathbf{X})^{-1}\left(\sum_{i=1}^{N}\hat\varepsilon_i^2\,\mathbf{x}_i\mathbf{x}_i'\right)(\mathbf{X}'\mathbf{X})^{-1}.
$$

These are **White standard errors**, also called **heteroskedasticity-robust** or just
**robust** standard errors. The "0" in HC0 is a clue that there are corrected versions
HC1–HC3, which we get to next. Crucially, robust SEs are valid whether or not there is
heteroskedasticity: if the errors *happen* to be homoskedastic, the robust estimator converges
to the classical answer as $N$ grows. In fact the small-sample correspondence is sharpest for
**HC1**, which carries the same $N/(N-K)$ degrees-of-freedom factor as the classical
$\hat\sigma^2$: under homoskedasticity HC1 reproduces the classical SE almost exactly, while raw
HC0 (lacking that factor) runs a touch *smaller*. Either way, robust SEs cost you almost nothing
and protect you from a real failure — which is why "always report robust" is close to a default
in modern finance work.

### 3.3 HC0, HC1, HC2, HC3 — the finite-sample corrections

White's HC0 is *consistent*, meaning it gets the right answer as $N\to\infty$. But in finite
samples it has a known flaw: OLS residuals are systematically **too small.** The fitting
procedure bends the line toward each point, so $\hat\varepsilon_i$ understates the true
$\varepsilon_i$, which makes HC0 standard errors too *small* — overconfident again, in small
samples. The fix is to inflate the squared residuals. The four common flavors differ only in
*how* they inflate:

| Flavor | Each $\hat\varepsilon_i^2$ is replaced by | What it corrects | Use when |
|--------|-------------------------------------------|------------------|----------|
| **HC0** | $\hat\varepsilon_i^2$ | nothing (raw White) | large $N$, you don't care about small-sample bias |
| **HC1** | $\dfrac{N}{N-K}\,\hat\varepsilon_i^2$ | a flat degrees-of-freedom inflation | the default in Stata; fine for moderate $N$ |
| **HC2** | $\dfrac{\hat\varepsilon_i^2}{1-h_{ii}}$ | leverage, observation by observation | small samples; principled choice |
| **HC3** | $\dfrac{\hat\varepsilon_i^2}{(1-h_{ii})^2}$ | leverage, more aggressively | small $N$ or high-leverage points; safest |

The $h_{ii}$ here are the diagonal entries of the **hat matrix** $\mathbf{H} = \mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'$
from Ch 2.1 — the **leverage** of observation $i$, a number between 0 and 1 measuring how much
that point pulls the fitted line toward itself. A high-leverage point (an outlier in
$\mathbf{X}$, like Priya's one \$5 million estate among cabins) has its residual shrunk the
most by fitting, so HC2 and HC3 inflate it the most to compensate. HC1 ignores leverage and
applies the same $N/(N-K)$ factor to everyone.

The practical guidance is simple and worth memorizing. With a few hundred observations or more
and no extreme leverage, HC1 (Stata's default) is fine and HC0–HC3 barely differ. When $N$ is
small — say under 50 — or a handful of points have high leverage, the flavors diverge and HC3
is the conservative, recommended default (it is the most likely to keep you honest). HC3 is
never badly anti-conservative, so if you are unsure, HC3 is the safe pick.

### 3.4 A number to make it concrete

Priya simulates 60 claims where the true error standard deviation grows linearly with insured
value (textbook heteroskedasticity), with one \$5M estate among \$200K cabins to create
leverage. On her coefficient of interest the four standard errors come out roughly:

| Classical | HC0 | HC1 | HC2 | HC3 |
|-----------|-----|-----|-----|-----|
| 0.085 | 0.121 | 0.127 | 0.140 | 0.169 |

The classical SE of $0.085$ understates the true uncertainty by about half relative to HC3's
$0.169$. If her coefficient were $0.30$, the classical t-stat would read $0.30/0.085 = 3.5$
(comfortably significant) while the HC3 t-stat reads $0.30/0.169 = 1.8$ (not significant at the
5% level). Same coefficient. Same data. The only thing that changed is whether we told the
truth about $\boldsymbol\Omega$ — and it flipped the conclusion. Notice also how the four robust
flavors fan out: HC0 at $0.121$ and HC3 at $0.169$ differ by a real margin precisely *because*
that one \$5M estate is a high-leverage point, and HC3's $(1-h_{ii})^2$ denominator inflates its
residual the hardest. In a sample with no leverage and a few hundred points, those four numbers
would have agreed to the third decimal.

### 3.5 When it fails, what you actually see

Reveal-the-trick demands we say what the *symptom* looks like, so you can catch it in your own
work rather than only in a textbook. Three tells, in increasing order of formality:

First, **the residual plot.** Plot the residuals $\hat\varepsilon_i$ against a fitted value or
against a regressor. Under homoskedasticity you see a structureless horizontal band of constant
thickness. Under heteroskedasticity you see a *fan* or *funnel* — the band widens (or narrows)
as you move along the axis. Priya's wildfire residuals fan open toward expensive properties;
Maya's loan residuals often fan with loan size. This single plot catches most real cases and
costs you one line of code.

Second, **a formal test.** The Breusch–Pagan test regresses the squared residuals on the
regressors and asks whether they explain any of the variance (if scatter is constant, they
should not); the White test does the same with squares and cross-products to catch more general
patterns. A small p-value says "reject homoskedasticity." But here is the modern attitude, and
it is worth internalizing: **you usually should not bother testing.** Because robust SEs are
valid whether or not heteroskedasticity is present, the cost of "just always using robust" is
near zero, while the cost of testing, failing to reject by bad luck, and then trusting classical
SEs is a published overconfident result. Test if a referee asks; otherwise default to robust.

Third, **the SEs themselves disagree.** If classical and robust standard errors are nearly
identical, your errors are roughly homoskedastic and nothing was at stake. If they differ
materially — as in Priya's table — heteroskedasticity is real and the robust number is the one
to report. The disagreement *is* the diagnostic.

---

## 4. Clustering: when errors hold hands within groups

### 4.1 The failure that White SEs do not fix

Robust SEs assume the off-diagonals of $\boldsymbol\Omega$ are zero — errors uncorrelated across
observations. In finance that assumption is heroic and usually false. Maya's loans within the
same lender share the lender's pricing model, risk appetite, and quirks; their errors move
together. Priya's wildfire claims within the same state share that state's fire season,
building codes, and reinsurance market; their errors move together. Devon's daily token returns
within the same week share whatever sentiment shock hit crypto that week. These are
**within-cluster correlations**, and robust SEs are blind to them because they only ever look
at one observation at a time.

The stakes here are not academic. Go back to Maya's fair-lending result from the opening. Her
claim — that one borrower tier pays measurably more after controlling for credit — is the kind
of finding that can support or sink a discrimination complaint, inform a regulator, or appear in
a policy brief. If she reports a t-stat of $6.0$ when the honest, clustered t-stat is $2.2$, she
has not just made a technical slip; she has overstated the strength of evidence on a question
where overstating it has real consequences in both directions (a false alarm wastes enforcement
attention; underpowered honesty lets real discrimination slide). The reason the naive number is
*so* much too big is not that her 9,000 loans are fake data — they are real — but that they are
not 9,000 *independent* pieces of evidence. Loans from the same lender largely repeat the same
story. Counting them as independent is like polling one household nine times and reporting a
sample of nine. The clustered standard error is the correction that stops you from doing that.

Here is *why ignoring clustering is so dangerous* — and it is the single most expensive mistake
in empirical finance, so it earns its own derivation. Suppose Maya has $N$ loans split into $G$
lenders ("clusters") of equal size $n = N/G$, and within a lender the errors all share a common
shock with within-cluster correlation $\rho$. There is a classic result (a special case of the
Moulton factor) for how badly the naive standard error understates the truth. The variance of
your estimate is inflated, relative to what the naive formula reports, by approximately

$$
\text{true Var} \approx \text{naive Var} \times \big[\,1 + (n-1)\,\rho_x\,\rho_\varepsilon\,\big],
$$

where $n$ is the cluster size, $\rho_\varepsilon$ is the within-cluster error correlation, and
$\rho_x$ is the within-cluster correlation of your regressor. Stare at the bracket. The damage
scales with **cluster size $n$**: bigger clusters, worse understatement. With $n = 200$ loans
per lender and even a mild $\rho_x\rho_\varepsilon = 0.05$, the bracket is
$1 + 199\times0.05 \approx 11$. Your true variance is *eleven times* the naive one — so your
true standard error is $\sqrt{11}\approx 3.3$ times bigger, and your reported t-stat of $6.0$
should really be about $6.0/3.3 \approx 1.8$. That is *exactly* what happened to Maya in the
opening, and now you can see it was not bad luck; it was arithmetic. Pouring in more
observations *within existing clusters* does not buy you the independent evidence the naive
formula thinks it does. What buys evidence is more **clusters.**

### 4.2 The cluster-robust sandwich

The fix is the same sandwich, with a middle built from whole clusters instead of single points.
If errors are correlated *within* cluster $g$ but uncorrelated *across* clusters, then
$\boldsymbol\Omega$ is **block-diagonal** — a big matrix with dense blocks down the diagonal
(one block per cluster, capturing all the within-cluster covariances) and zeros everywhere
else. The middle of the sandwich then becomes a sum over the $G$ clusters:

$$
\widehat{\operatorname{Var}}(\hat{\boldsymbol\beta})_{\text{cluster}}
= (\mathbf{X}'\mathbf{X})^{-1}\left(\sum_{g=1}^{G}\mathbf{X}_g'\hat{\boldsymbol\varepsilon}_g\,\hat{\boldsymbol\varepsilon}_g'\mathbf{X}_g\right)(\mathbf{X}'\mathbf{X})^{-1},
$$

where $\mathbf{X}_g$ is the block of regressor rows for cluster $g$ and
$\hat{\boldsymbol\varepsilon}_g$ is its vector of residuals. Compare this to White's HC0 in
§3.2. There the middle summed $\hat\varepsilon_i^2\,\mathbf{x}_i\mathbf{x}_i'$ over single
*observations*; here it sums $\mathbf{X}_g'\hat{\boldsymbol\varepsilon}_g\hat{\boldsymbol\varepsilon}_g'\mathbf{X}_g$
over whole *clusters*, and the outer product $\hat{\boldsymbol\varepsilon}_g\hat{\boldsymbol\varepsilon}_g'$
deliberately keeps the within-cluster covariances (the products $\hat\varepsilon_{i}\hat\varepsilon_{j}$
for two loans $i,j$ in the same lender) that White's version threw away. White SEs are just
cluster SEs where every cluster has size one. It is the *same machine*, zoomed out from points
to groups.

The empirical-spec discipline from the Conventions now has teeth: when you write a spec you must
**name the clustering level**, and that choice is an economic claim about where
$\boldsymbol\Omega$'s off-diagonal blocks live. "Clustered by lender" asserts that two loans
from the same lender have correlated errors and two loans from different lenders do not. If you
believe the correlation actually lives at the state level (shared regulation, shared economy),
you cluster by state, and the blocks get bigger.

### 4.3 The few-clusters caveat

There is a catch, and it bites hard in finance. The cluster-robust estimator is consistent as
the **number of clusters $G \to \infty$**, not as $N\to\infty$. The asymptotics live in $G$, not
in $N$. If Maya clusters by state, she has at most $G = 50$ clusters; if she clusters by some
broad industry, maybe $G = 12$. With few clusters the cluster-robust SE is itself noisy and
*biased downward* — overconfident again, the very disease we are treating.

The rough rule of thumb is that you want **at least 30–50 clusters** before you trust the
cluster-robust normal-approximation t-test at face value. Below that, you reach for fixes: the
small-sample $t$-distribution with $G-1$ degrees of freedom rather than the normal; or the
**wild cluster bootstrap** (Cameron, Gelbach & Miller, 2008),[^cgm2008] which resamples
whole clusters and is the current standard remedy for the few-clusters problem.

[^cgm2008]: Cameron, A. C., Gelbach, J. B., & Miller, D. L. (2008). Bootstrap-Based Improvements for Inference with Clustered Errors. *Review of Economics and Statistics*, 90(3), 414–427. The lab in
nb2.4 has you watch a cluster-robust SE get unreliable as you shrink $G$, which is the kind of
thing you only really believe once you have made it happen on your own screen.

[^cgm2011]: Cameron, A. C., Gelbach, J. B., & Miller, D. L. (2011). Robust Inference With Multiway Clustering. *Journal of Business & Economic Statistics*, 29(2), 238–249.

---

## 5. HAC / Newey–West: correlation across time

### 5.1 The time-series version of the same disease

Sam trades. He regresses a strategy's monthly return on a market-timing signal and gets a
beautiful t-stat. But returns and residuals in financial time series are **serially correlated**
(also called **autocorrelated**): this month's error is correlated with last month's, because
slow-moving forces — a drifting risk premium, a multi-month liquidity squeeze, momentum itself —
persist across periods. Now $\boldsymbol\Omega$ has nonzero off-diagonals, but in a special
pattern: the correlation is strongest between *adjacent* periods and **fades as the time gap
grows.** $\operatorname{Cov}(\varepsilon_t,\varepsilon_{t-1})$ is large,
$\operatorname{Cov}(\varepsilon_t,\varepsilon_{t-12})$ is near zero.

This is not clustering — there are no clean groups — and it is not pure heteroskedasticity. It
is a third shape for $\boldsymbol\Omega$: a band of decaying correlations around the diagonal.
Ignoring it, just like ignoring clustering, makes standard errors too small when the
autocorrelation is positive (the usual case in finance), inflating t-stats.

### 5.2 Newey and West's idea (1987)

Whitney Newey and Kenneth West built the **heteroskedasticity-and-autocorrelation-consistent
(HAC)** estimator for exactly this. Same sandwich. The middle now includes not just each
period's own squared-residual term but **cross-products of residuals from nearby periods**,
$\hat\varepsilon_t\hat\varepsilon_{t-\ell}\,\mathbf{x}_t\mathbf{x}_{t-\ell}'$, for time gaps
("lags") $\ell = 1, 2, \dots, L$. Because correlation fades with distance, Newey–West applies
**declining weights** $w_\ell = 1 - \tfrac{\ell}{L+1}$ (the Bartlett kernel): the lag-1
cross-products count almost fully, distant lags count for less, and beyond the chosen
**bandwidth** $L$ they count for nothing. The two declining-weight pieces are there both to
honor the fading-correlation structure and, mathematically, to guarantee the resulting variance
matrix is positive (a variance can't be negative — without the weights this sum could
misbehave).

The one knob you must set is the bandwidth $L$ — how many lags to include. Too small and you
miss real persistence; too large and you add noise. A common automatic choice is
$L \approx 4(T/100)^{2/9}$ (the Newey–West rule of thumb), where $T$ is the number of time
periods, and most software offers an automatic-bandwidth option. For Sam's monthly data,
setting $L$ to a small multiple of 12 (a year or two of lags) is a sensible manual starting
point. HAC SEs are the default for pure time-series regressions: predictive return
regressions, factor-model time-series tests, anything indexed by $t$ with one observation per
period.

### 5.3 Why positive autocorrelation inflates t-stats, in one intuition

It is worth pinning down *why* serial correlation, like clustering, makes naive standard errors
too small — because the mechanism is the same one, wearing a time-series costume. Recall the
Moulton-style intuition from §4.1: when errors are positively correlated, each new observation
carries *less* fresh information than the naive formula assumes, because part of it just echoes
what you already saw. A time series with positive autocorrelation is exactly a chain of
observations that echo their neighbors. If Sam has $T = 120$ monthly returns but each month's
residual is, say, 0.4-correlated with the previous month's, his *effective* sample size — the
number of genuinely independent monthly draws — is well below 120. The naive formula divides by
the wrong (too large) effective $T$, so it reports a standard error that is too small and a
t-stat that is too big. HAC repairs this by counting the lagged cross-products, which is
arithmetically how it discovers that the 120 months are worth fewer than 120 independent
observations.

The same logic explains the sign. *Positive* autocorrelation (the usual case in finance, where
shocks persist) shrinks the effective sample and inflates t-stats — the dangerous direction.
*Negative* autocorrelation (rarer, e.g. bid–ask bounce in high-frequency prices) would do the
reverse, making naive t-stats too conservative. Either way, HAC gets it right because it
estimates the actual band of off-diagonal covariances rather than assuming the band is empty.

---

## 6. Putting it together: the Petersen (2009) panel taxonomy

Now the hard case, and the one Maya and Priya actually live in: a **panel**, where you observe
many firms ($i$) over many time periods ($t$) at once. A panel can have *both* diseases at
once — errors correlated within a firm across time (a **firm effect**: a firm that is
mispriced this year tends to be mispriced next year) *and* errors correlated across firms within
the same period (a **time effect**: when the whole market drops, every firm's residual drops
together). Which standard error do you use?

This is the precise question Mitchell Petersen took up in a now-canonical 2009 paper, after
noticing that finance papers were using a chaos of incompatible methods and getting standard
errors that differed by factors of two or more *on the same data*. His contribution was not a
new estimator so much as a clear **taxonomy and a set of simulations** showing which approach is
right in which situation. The headline findings, which you should treat as practical defaults:

- **A persistent firm effect** (the firm's residuals correlated over time) is, in Petersen's
  data, the dominant problem in corporate-finance panels, and it is the one most often ignored.
  The right tool is **clustering by firm**, which lets each firm's errors be arbitrarily
  correlated across all its years — exactly the block-diagonal $\boldsymbol\Omega$ of Section 4,
  with one block per firm spanning all its time periods. White SEs and Fama–MacBeth do *not*
  fix a firm effect and will leave you badly overconfident.

- **A time effect** (a common shock hitting all firms in a period, like a market-wide crash) is
  better handled by **clustering by time** — one block per period, spanning all firms in it.
  Petersen notes that in many corporate panels a time effect is well absorbed by including
  **time fixed effects** (a dummy for each period, previewed by the demeaning idea in Ch 2.3);
  but if a *residual* common shock remains, clustering by time catches it.

- **Both effects present?** Use **two-way clustering** (Cameron, Gelbach & Miller,
  2011,[^cgm2011] building on Petersen and Thompson), which clusters by firm *and* by time
  simultaneously, allowing both kinds of correlation in $\boldsymbol\Omega$ at once. The
  mechanical recipe is elegant: compute the firm-clustered sandwich, add the time-clustered
  sandwich, and subtract the plain White (heteroskedasticity-only) sandwich so the overlap
  isn't double-counted.

The decision rule Petersen leaves you with is the empirical-spec discipline made concrete:
**figure out where your residuals are correlated — across time within a firm, across firms
within a period, or both — and cluster on that dimension (or those dimensions).** It is an
economic judgment about $\boldsymbol\Omega$, not a software default, and the same dataset can
demand different clustering depending on what you put on the left-hand side. (Ch 5.4 is a full
reader's guide to this paper; here we want the operational rule.)

How do you tell *which* effect dominates without guessing? Petersen offers a practical
diagnostic that you can run yourself. Cluster by firm and look at the standard error; then
cluster by time and look again. Whichever clustering moves the standard error *more* away from
the naive White number is pointing at the bigger source of correlation. If clustering by firm
roughly doubles your SE but clustering by time barely changes it, you have a firm effect and
little else — firm-clustering is enough. If both move it a lot, you have both effects and want
two-way clustering. This is exactly the experiment nb2.4 walks you through, and it turns the
"which cluster?" question from a matter of taste into something you can read off your own output.

A subtlety worth flagging now and developing in Weeks 3–4: **fixed effects and clustering are
not substitutes — they do different jobs.** A firm fixed effect (a dummy for each firm, Ch 2.3's
demeaning) removes the firm's *average* level from both sides; it handles a firm-specific mean
that never changes. Clustering by firm handles *correlation in the leftover residuals* over time
— the part a fixed effect cannot touch because it is about co-movement, not means. You often
want both at once: firm fixed effects to absorb permanent firm differences *and* clustering by
firm to honor the within-firm residual correlation that remains. Conflating the two ("I have
firm fixed effects, so I don't need to cluster by firm") is a common and costly error, and it is
the kind of thing the empirical-spec line in your write-up forces you to get explicit about.

A worked taste of the stakes, in the spirit of Petersen's own tables. Maya assembles a panel of
default outcomes for many firms over many years and regresses default on a leverage measure. The
coefficient is the same in every column; only the SE flavor changes. The illustrative numbers
below show the *shape* of what happens — the SE inflates as you allow more correlation into
$\boldsymbol\Omega$, dragging the t-stat across the significance line. (For real, reproducible
magnitudes built from a simulated panel, see nb2.4: on its 120-firm $\times$ 20-year panel the
identical $\hat\beta=0.30$ carries a classical t of $5.70$ that collapses to a firm-clustered t
of $2.19$ — the same story, with numbers you can re-run. The smaller §7 toy panel just below
shows the same collapse at its own scale.)

| SE flavor | Std. error (illustrative) | t-stat | Honest? |
|-----------|-----------|--------|---------|
| Classical (OLS) | 0.018 | 5.0 | No — assumes $\sigma^2\mathbf{I}$ |
| White (HC1) | 0.021 | 4.3 | No — ignores within-firm correlation |
| Clustered by firm | 0.044 | 2.0 | Yes, if the firm effect dominates |
| Two-way (firm + year) | 0.052 | 1.7 | Yes, if both effects are present |

These figures are illustrative, not the output of a committed script; the live numbers are in
nb2.4. The qualitative point is exact, though: a classical t-stat around $5$ and a
two-way-clustered t-stat around $1.7$ are computed from *identical* point estimates on
*identical* data. One says "publish"; the other says "not yet." The difference is entirely a
story about $\boldsymbol\Omega$, and choosing the wrong one is how real papers get retracted.

---

## 7. The code

Every flavor in this chapter is one argument in `statsmodels`. The point of seeing them
side by side is to feel how much the t-stat moves while $\hat\beta$ sits perfectly still.

```python
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# --- A toy clustered panel: firms over years, with a firm-level error component ---
rng = np.random.default_rng(8)
n_firms, n_years = 40, 15
firm = np.repeat(np.arange(n_firms), n_years)
year = np.tile(np.arange(n_years), n_firms)

# the regressor itself has a persistent firm-level piece (correlated within firm) --
# this is what makes ignoring clustering so costly (the Moulton logic of Section 4.1):
x_firm = np.repeat(rng.normal(size=n_firms), n_years)
x = x_firm + 0.5 * rng.normal(size=n_firms * n_years)      # the key regressor
firm_shock = np.repeat(rng.normal(size=n_firms), n_years)  # persistent firm effect
year_shock = np.tile(rng.normal(size=n_years), n_firms)    # common time shock
eps = 1.5 * firm_shock + year_shock + rng.normal(size=n_firms * n_years)
y = 0.30 * x + eps                                         # TRUE slope is 0.30

df = pd.DataFrame({"y": y, "x": x, "firm": firm, "year": year})
fit = smf.ols("y ~ x", data=df).fit()                  # one OLS fit, reused below
xi = list(fit.params.index).index("x")                 # column position of the x coef

def se(res, label):
    # robust results return plain numpy arrays, so index by position, not name
    b = np.asarray(res.params)[xi]
    s = np.asarray(res.bse)[xi]
    print(f"{label:<22} beta={b:.3f}  se={s:.3f}  t={b/s:.2f}")

se(fit,                                          "classical")
se(fit.get_robustcov_results("HC1"),             "robust HC1")
se(fit.get_robustcov_results("HC3"),             "robust HC3")
se(fit.get_robustcov_results("cluster", groups=df["firm"]),  "cluster by firm")
se(fit.get_robustcov_results("cluster",
       groups=df[["firm", "year"]]),             "two-way (firm+year)")
# HAC / Newey-West (for a pure time series; shown for completeness):
se(fit.get_robustcov_results("HAC", maxlags=4),  "Newey-West HAC(4)")
```

Run it and you will see the coefficient on `x` glued near $0.27$ in every line (close to the
true $0.30$) while the standard error roughly *doubles* from classical (about $0.073$) to
firm-clustered (about $0.144$), because we deliberately built a strong, persistent firm effect
into both the regressor and the error. That doubling is the chapter in one screen of output:
**the estimate is fine; the t-stat was lying** — it falls from about $3.7$ to about $1.9$,
crossing the significance line without the point estimate budging. Change `firm_shock` to zero
(and drop the firm piece of `x`) and the
gap closes — robust and classical agree when the errors really are well behaved, which is the
reassurance that you lose nothing by defaulting to the honest formula.

---

## 8. The mental checklist

When you sit down with a regression and ask "which standard error?", walk the decision in this
order — it is just "what does $\boldsymbol\Omega$ look like?" in plain questions:

1. **Could the error variance differ across observations?** In finance, essentially always yes.
   So never use classical SEs as your final answer — use at least **robust (HC1, or HC3 if $N$
   is small or leverage is high)**.
2. **Are observations grouped, with correlated errors inside a group** (firms, lenders, states,
   schools)? Then **cluster** on that group — and check you have enough clusters (aim for
   $\gtrsim 30$–$50$; otherwise use the wild cluster bootstrap).
3. **Is it a pure time series with serial correlation?** Use **HAC / Newey–West**, and set the
   bandwidth to cover the persistence you expect.
4. **Is it a panel (many units × many periods)?** Diagnose the correlation structure à la
   **Petersen (2009)**: firm effect → cluster by firm; time effect → time FEs or cluster by
   time; both → two-way cluster.

The recurring lesson, and the reason this chapter sits between the Gauss–Markov guarantees of
Ch 2.2 and the bias problems of Ch 2.5: **getting $\hat\beta$ right and getting its uncertainty
right are two separate jobs.** Ch 2.5 is about when $\hat\beta$ itself is biased — a different
and in some ways more dangerous failure. This chapter was entirely about the second job. A
biased estimator points at the wrong answer; a wrong standard error makes you wrongly *confident*
about whatever answer you have. Both will get a finding rejected. Only one of them will get it
rejected *after* it's been published.

---

## Your Turn

Open **nb2.4 — SE flavors on a clustered panel.** You will build a panel with a tunable firm
effect and a tunable time effect, then watch the five standard-error flavors (classical, HC1,
HC3, firm-clustered, two-way) move as you turn the knobs — including the unsettling experiment
of shrinking the number of clusters until the cluster-robust SE stops being trustworthy. The
goal is to *see*, with your own simulated data, the gap between the t-stat that lies and the
t-stat that tells the truth.

**Check questions.**

1. Maya runs a regression and gets $\hat\beta_1 = 0.50$ with a classical SE of $0.10$ (t = 5.0).
   After clustering by lender the SE rises to $0.25$ (t = 2.0). A classmate says "so the
   clustering shrank your coefficient." In one or two sentences, explain exactly what is wrong
   with that statement and what actually changed.

2. Priya has a panel of 8,000 insurance-claim records but only **9 states**. She clusters her
   standard errors by state. Why should she be nervous about the resulting t-statistics, and
   name one thing she could do about it.

3. Sam regresses monthly strategy returns on a signal and reports classical standard errors. His
   residuals are positively autocorrelated from month to month. Is his reported t-statistic
   likely too big or too small, and which standard-error flavor should he switch to? Explain
   why in terms of what the off-diagonal entries of $\boldsymbol\Omega$ look like in his case.
