# Chapter 2.2 — Gauss–Markov and the Meaning of "Best"

Maya has a question that her credit union actually pays people to answer: **does a borrower's
income predict the interest rate they get on a personal loan?** She pulls a sample of $N$
approved loans, and for each borrower $i$ she records the annual percentage rate $y_i$ they were
charged and their reported annual income $x_i$. She runs the regression you built in Chapter 2.1,

$$
y_i = \beta_0 + \beta_1 x_i + \varepsilon_i ,
$$

or in the matrix form we will use for the rest of the week, $\mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\varepsilon}$,
and out pops the familiar formula

$$
\hat{\boldsymbol{\beta}} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y} .
$$

Her software prints $\hat{\beta}_1 = -0.42$: each extra \$10,000 of income is associated with a
rate about 0.42 percentage points lower. She writes it down. And then — because Chapter 1.3
trained her to — she asks the only honest follow-up question there is: **why should anyone trust
this number?**

Notice she is not asking "is $-0.42$ the right answer?" She will never know the true $\beta_1$,
the same way Priya could never see the true mean claim. She is asking the two questions Chapter
1.3 taught us to separate. Is the *recipe* $\hat{\boldsymbol{\beta}} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$
**aimed at the truth** — is it unbiased? And of all the recipes she *could* have used, is this one
the **steadiest** — does it have the smallest variance? Chapter 1.3 answered both questions for
the sample mean. This chapter answers them for OLS.

Here is the punchline, stated once in plain English and then earned over the next six sections.
There is a famous theorem — the **Gauss–Markov theorem** — that says OLS is **BLUE**: the *Best
Linear Unbiased Estimator*. "Best" is a precise technical word, not a compliment, and it comes
with a price tag: a list of assumptions you have to be willing to sign. The theorem is really a
contract. *If* you accept five conditions about how your data were generated, *then* OLS is
guaranteed to be the lowest-variance estimator in a specific club. The entire art of applied
econometrics is reading that contract carefully — knowing which clause is most likely to be
violated in your particular dataset, what you'll see when it breaks, and which later chapter
fixes it. So we will spend most of this chapter not celebrating the theorem but interrogating its
fine print.

---

## 1. The contract: five assumptions, stated as testable claims

Textbooks usually list the classical assumptions as abstract Greek. We will instead state each
one as a *claim about Maya's loan data* that could, at least in principle, be true or false — and
flag, for each, what you'd see if it failed and where in the book we repair it. Keep the spec
discipline from the Conventions in mind: an assumption is not a ritual incantation, it is a
falsifiable statement about a data-generating process.

**Assumption 1 — Linearity in parameters.** The true relationship is
$\mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\varepsilon}$, meaning $y$ is a sum of the
columns of $\mathbf{X}$ each multiplied by a constant coefficient, plus an error. The crucial and
often-misread word is *parameters*. The model must be linear in the $\beta$'s, **not** in the
$x$'s. Maya is completely free to put $x^2$, $\log(\text{income})$, or an interaction term in as a
column of $\mathbf{X}$; the curve can bend however the world bends. What she may *not* write is
something like $y = \beta_0 + x^{\beta_1} + \varepsilon$, where a coefficient sits in an exponent.
*What goes wrong if it fails:* if the true rate-income relationship is, say, $y = \beta_0 +
\beta_1\log x + \varepsilon$ and she fits a straight line in $x$, she is fitting the wrong
functional form, and her residuals will show a tell-tale U- or arc-shaped pattern when plotted
against income. The fix lives in this same week: Chapter 2.3 shows how to add polynomial, log, and
interaction terms so a "linear" model captures curved relationships.

**Assumption 2 — Random sampling and no perfect collinearity (full-rank $\mathbf{X}$).** Two ideas
travel together here. First, the $N$ loans are a representative draw from the population Maya cares
about — the analogue of Priya's "the 200 claims come from the population whose mean I want."
Second, and this is the part that is genuinely *mechanical* rather than statistical: the matrix
$\mathbf{X}$ has **full column rank**, which we met in Chapter 2.1. No column is a constant
multiple of another, and no column is an exact linear combination of the others. This is what lets
$(\mathbf{X}'\mathbf{X})^{-1}$ exist in the first place — without it the OLS formula is not biased,
it is *undefined*, like dividing by zero. *What goes wrong if it fails:* if Maya accidentally
includes income in both dollars and thousands of dollars as two columns, one is exactly $1000\times$
the other, $\mathbf{X}'\mathbf{X}$ is singular, and the software either errors out or silently
drops a column. *Near* failure — two highly (but not perfectly) correlated regressors — is
**multicollinearity**, which doesn't bias anything but inflates variances; we'll diagnose it in
Chapter 2.3.

**Assumption 3 — Zero conditional mean: $\mathbb{E}[\boldsymbol{\varepsilon}\mid\mathbf{X}] = \mathbf{0}$.**
This is the one that matters. Everything causal in the entire book turns on it, so read it slowly.
It says: *whatever Maya did not put in her regression — call it the error $\varepsilon$ — has
average value zero for every possible configuration of the things she did put in.* Pick any income
level, high or low; among borrowers at that income, the stuff the model leaves out (credit
history, existing debt, the loan officer's mood) must average out to zero. The error is allowed to
be large for any individual borrower; it just can't be *systematically related to the regressors*.
*What goes wrong if it fails:* this is the master fault. If borrowers with higher income also
happen to have better credit scores (which Maya didn't include) and credit scores independently
lower rates, then her income coefficient is silently absorbing the credit-score effect — the
left-out variable lives in $\varepsilon$ and is correlated with $x$, so $\mathbb{E}[\varepsilon\mid
x] \neq 0$. This is **omitted-variable bias**; together with **measurement error** in the
regressors it is the subject of Chapter 2.5. We motivate it here and prove its damage there.

**Assumption 4 — Homoskedasticity: $\operatorname{Var}(\boldsymbol{\varepsilon}\mid\mathbf{X}) = \sigma^2\mathbf{I}$.**
Two claims again. The errors all have the *same* variance $\sigma^2$ regardless of $\mathbf{X}$
(that's the constant $\sigma^2$ on the diagonal — the word *homoskedastic* is Greek for "same
scatter"), and they are *uncorrelated across observations* (that's the zeros off the diagonal,
making the matrix $\sigma^2\mathbf{I}$). *What goes wrong if it fails:* in Maya's data, the scatter
of rates around the line is almost surely **larger for low-income borrowers** — lenders have more
discretion, more risk-based pricing, more spread — and tighter for high earners. That is
**heteroskedasticity**: the diagonal of the variance matrix is not constant. It does *not* bias
$\hat{\boldsymbol{\beta}}$, but it wrecks the *standard errors*, so every t-statistic and
confidence interval from Chapter 1.5 becomes untrustworthy. This is exactly Chapter 2.4, where
robust (HC1/HC2/HC3) standard errors come to the rescue. The off-diagonal zeros — uncorrelated
errors — are the same independence assumption that gave Priya her clean $\sigma^2/N$; when loans
cluster (same branch, same month) those zeros become positive and we'll need clustered standard
errors, also Chapter 2.4.

**Assumption 5 (the add-on) — Normality: $\boldsymbol{\varepsilon}\mid\mathbf{X} \sim \mathcal{N}(\mathbf{0},\,\sigma^2\mathbf{I})$.**
This one is *not* part of Gauss–Markov, and it is important to know that. The first four
assumptions are all the theorem needs. Normality is an *extra* assumption we bolt on later when we
want **exact** finite-sample inference — the exact $t$ and $F$ distributions of Chapter 1.5,
valid even at small $N$. *What goes wrong if it fails:* surprisingly little, for large samples.
Even without normality, the Central Limit Theorem from Chapter 1.4 makes $\hat{\boldsymbol{\beta}}$
approximately normal as $N$ grows, so our t-tests are *approximately* valid anyway. Normality is a
convenience for small samples, not a pillar. We will lean on it lightly and flag it whenever we do.

The cleanest way to hold this in your head: **Assumptions 1–3 buy you unbiasedness. Adding 4 buys
you BLUE. Adding 5 buys you exact small-sample inference.** Three tiers, increasingly demanding,
each delivering more. The next two sections cash in the first two tiers.

---

## 2. Unbiasedness: the recipe aims at the truth

Recall the standard we set in Chapter 1.3. An estimator is **unbiased** if its expected value —
its center across all possible samples — equals the truth: $\mathbb{E}[\hat{\boldsymbol{\beta}}] =
\boldsymbol{\beta}$. For the sample mean we proved this in three lines using only that expectation
is linear and that $\mathbb{E}[x_i] = \mu$. We will now do the exact same move for OLS, and the
star ingredient will be Assumption 3.

Start from the OLS formula and substitute in the *true* model $\mathbf{y} = \mathbf{X}\boldsymbol{\beta}
+ \boldsymbol{\varepsilon}$ — this is the step that connects the estimate to the truth it is chasing:

$$
\hat{\boldsymbol{\beta}}
= (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}
= (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'(\mathbf{X}\boldsymbol{\beta} + \boldsymbol{\varepsilon}) .
$$

Distribute the multiplication across the sum. The first piece collapses beautifully, because
$(\mathbf{X}'\mathbf{X})^{-1}(\mathbf{X}'\mathbf{X}) = \mathbf{I}$, the identity matrix — a matrix
times its own inverse is the "do-nothing" matrix:

$$
\hat{\boldsymbol{\beta}}
= \underbrace{(\mathbf{X}'\mathbf{X})^{-1}(\mathbf{X}'\mathbf{X})}_{=\ \mathbf{I}}\,\boldsymbol{\beta}
\;+\; (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\boldsymbol{\varepsilon}
\;=\; \boldsymbol{\beta} + (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\boldsymbol{\varepsilon} .
$$

Pause on this line, because it is the most revealing equation in the chapter. It says the estimate
equals the **truth plus a contamination term**: $\hat{\boldsymbol{\beta}} = \boldsymbol{\beta} +
(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\boldsymbol{\varepsilon}$. The whole question of whether OLS
aims true reduces to whether that second term averages to zero. The estimation error is a known
matrix, $(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'$, multiplying the unknowable error vector
$\boldsymbol{\varepsilon}$.

Now take the conditional expectation given $\mathbf{X}$. Conditioning on $\mathbf{X}$ lets us treat
the matrix $(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'$ as a *constant* — once we fix the regressors,
the only thing still random is the error — and pull it outside the expectation, exactly the way we
pulled $\tfrac1N$ out of $\mathbb{E}[\bar{x}]$:

$$
\mathbb{E}[\hat{\boldsymbol{\beta}}\mid\mathbf{X}]
= \boldsymbol{\beta} + (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\,\underbrace{\mathbb{E}[\boldsymbol{\varepsilon}\mid\mathbf{X}]}_{=\ \mathbf{0}\ \text{(Assumption 3)}}
= \boldsymbol{\beta} .
$$

There it is. The contamination term vanishes **precisely because** $\mathbb{E}[\boldsymbol{\varepsilon}\mid\mathbf{X}] = \mathbf{0}$.
And by the law of total expectation, the unconditional center is the same: $\mathbb{E}[\hat{\boldsymbol{\beta}}]
= \mathbb{E}\big[\mathbb{E}[\hat{\boldsymbol{\beta}}\mid\mathbf{X}]\big] = \boldsymbol{\beta}$. OLS is
unbiased. Maya's recipe aims at the true $\beta_1$.

Three things to notice, each a direct echo of Chapter 1.3:

1. **The proof used exactly one assumption — number 3.** Linearity (Assumption 1) was used
   silently when we wrote the true model, and full rank (Assumption 2) was used so the inverse
   exists. But homoskedasticity and normality played *no role whatsoever*. Unbiasedness is cheap:
   it doesn't care whether the errors are heteroskedastic, non-normal, or wildly different in
   spread. This is why heteroskedasticity (Chapter 2.4) leaves $\hat{\boldsymbol{\beta}}$ unbiased
   and only damages the standard errors.

2. **Unbiasedness has nothing to do with sample size.** Just as Priya's 3-claim average was as
   unbiased as her 3-million-claim average, OLS is unbiased at $N = 5$ and at $N = 5{,}000{,}000$,
   provided Assumption 3 holds. What changes with $N$ is the variance, next section.

3. **When Assumption 3 fails, the proof collapses at a visible spot.** If income is correlated
   with omitted creditworthiness, then $\mathbb{E}[\boldsymbol{\varepsilon}\mid\mathbf{X}] \neq
   \mathbf{0}$, the contamination term does *not* average away, and $\mathbb{E}[\hat{\boldsymbol{\beta}}\mid\mathbf{X}]
   = \boldsymbol{\beta} + (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\,\mathbb{E}[\boldsymbol{\varepsilon}\mid\mathbf{X}]
   \neq \boldsymbol{\beta}$. That leftover term *is* the omitted-variable bias formula, and reading
   it off this line is how Chapter 2.5 will quantify exactly how wrong Maya's $-0.42$ becomes. The
   math didn't break; the assumption did. Same lesson as Priya's miscounted county.

---

## 3. The variance of OLS, and what "best" will mean

Unbiasedness is the archer centering on the bullseye. Now we ask the second Chapter-1.3 question:
*how tightly clustered are the arrows?* We need the variance of $\hat{\boldsymbol{\beta}}$, and this
is where Assumption 4 finally does some work.

Start from the contamination line, $\hat{\boldsymbol{\beta}} - \boldsymbol{\beta} =
(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\boldsymbol{\varepsilon}$. The variance of an estimator
measures how much this deviation bounces around. Writing $\mathbf{A} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'$
for the constant matrix (constant once we condition on $\mathbf{X}$), the rule for the variance of
$\mathbf{A}\boldsymbol{\varepsilon}$ is $\mathbf{A}\operatorname{Var}(\boldsymbol{\varepsilon}\mid\mathbf{X})\mathbf{A}'$
— the matrix generalization of "pulling a constant out of a variance squares it," which Priya used
to get $\sigma^2/N$. Plugging in Assumption 4, $\operatorname{Var}(\boldsymbol{\varepsilon}\mid\mathbf{X})
= \sigma^2\mathbf{I}$:

$$
\operatorname{Var}(\hat{\boldsymbol{\beta}}\mid\mathbf{X})
= \mathbf{A}\,(\sigma^2\mathbf{I})\,\mathbf{A}'
= \sigma^2\,(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\,\mathbf{X}\,(\mathbf{X}'\mathbf{X})^{-1}
= \boxed{\;\sigma^2(\mathbf{X}'\mathbf{X})^{-1}\;}
$$

where the middle collapsed because $\mathbf{X}'\mathbf{X}$ sandwiched between two copies of its own
inverse leaves one inverse standing. This $\sigma^2(\mathbf{X}'\mathbf{X})^{-1}$ is the single most
important variance formula in this book — it is the matrix that, square-rooted along its diagonal,
becomes the standard errors on Maya's regression printout. Notice the family resemblance to
$\sigma^2/N$: more error variance $\sigma^2$ makes estimates jumpier, and "more/better-spread
$\mathbf{X}$" (a bigger $\mathbf{X}'\mathbf{X}$, hence a smaller inverse) makes them tighter. Spread
in your regressor is the multivariate version of sample size.

**A number, to make the formula concrete.** Abstract matrix algebra hides what
$\sigma^2(\mathbf{X}'\mathbf{X})^{-1}$ is really telling you, so let's compute it by hand for the
slope in a simple regression. When $\mathbf{X}$ is just an intercept plus one regressor (income),
the bottom-right entry of $\sigma^2(\mathbf{X}'\mathbf{X})^{-1}$ — the variance of the *slope*
$\hat{\beta}_1$ — works out to the tidy expression

$$
\operatorname{Var}(\hat{\beta}_1\mid\mathbf{X})
= \frac{\sigma^2}{\sum_{i=1}^N (x_i - \bar{x})^2}
= \frac{\sigma^2}{(N-1)\,s_x^2} ,
$$

where $s_x^2$ is the sample variance of income. Read that fraction like a story. The numerator
$\sigma^2$ is the noise in the rate that income can't explain — more scatter around the line, jumpier
slope. The denominator is the *spread of income in your sample*. Suppose Maya's errors have standard
deviation $\sigma = 1.5$ percentage points, she has $N = 400$ loans, and incomes have a standard
deviation of $s_x = 30$ (thousands of dollars). Then

$$
\operatorname{Var}(\hat{\beta}_1) = \frac{1.5^2}{399 \times 30^2} = \frac{2.25}{359{,}100} \approx 6.27\times 10^{-6},
$$

so the standard error of the slope is $\sqrt{6.27\times10^{-6}} \approx 0.0025$ percentage points
per thousand dollars. Now notice the lever the denominator hands you. If Maya could draw a sample
where incomes were *twice* as spread out ($s_x = 60$), the denominator quadruples and the standard
error *halves* — the same $\sqrt{\cdot}$ payoff that quadrupling $N$ would buy. **Spread in your
regressor is precision.** A study that only sampled borrowers in a narrow income band would estimate
the income–rate slope terribly, no matter how many loans it had, because there'd be no $x$-variation
to pin the line's tilt. This is the scalar shadow of the matrix fact that a bigger $\mathbf{X}'\mathbf{X}$
means a smaller inverse means tighter estimates.

But here is the thing to sit with. This formula gives *the variance of OLS specifically*. It does
not yet tell us whether OLS is the *best* anyone can do. Maya could have used a different linear
recipe. To know whether her arrows are the tightest possible, we need a theorem that compares OLS
against the entire field of competitors. That theorem is Gauss–Markov, and we need to define its
playing field first.

---

## 4. The Gauss–Markov theorem: OLS is BLUE

Read the four letters of **BLUE** backward, because that is the order in which they constrain the
competition.

- **E — Estimator** of $\boldsymbol{\beta}$. Some recipe that turns the data into a guess.
- **U — Unbiased.** We only let estimators into the contest if they aim true: $\mathbb{E}[\tilde{\boldsymbol{\beta}}]
  = \boldsymbol{\beta}$. This is a real restriction — it bars the dart-throwers and the
  "always-report-7.5%" cheats from Chapter 1.3, and, importantly, it bars *biased* estimators that
  might actually have lower MSE (more on that tension in §6).
- **L — Linear.** We further restrict the contest to estimators that are *linear in $\mathbf{y}$*:
  recipes of the form $\tilde{\boldsymbol{\beta}} = \mathbf{C}\mathbf{y}$ for some matrix
  $\mathbf{C}$ that may depend on $\mathbf{X}$ but not on $\mathbf{y}$. OLS qualifies, with
  $\mathbf{C} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'$. This club is large but not universal — it
  excludes, for example, estimators that do something nonlinear like medians or maximum-likelihood
  with a weird error distribution.
- **B — Best**, meaning **minimum variance**. Among everyone left standing — every linear unbiased
  estimator — OLS has the smallest variance. More precisely, for *any* linear combination
  $\mathbf{c}'\boldsymbol{\beta}$ of the coefficients you might care about (a single slope, a sum, a
  difference), the OLS-based estimate has the smallest variance of any linear unbiased competitor.

Put together:

> **Gauss–Markov Theorem.** Under Assumptions 1–4 (linearity, full-rank random sampling, zero
> conditional mean, and homoskedasticity), the OLS estimator $\hat{\boldsymbol{\beta}}$ is the
> **Best Linear Unbiased Estimator** of $\boldsymbol{\beta}$: among all estimators that are both
> linear in $\mathbf{y}$ and unbiased, it has the smallest variance.

Notice the contract precisely: normality (Assumption 5) is *absent*. Gauss–Markov is a statement
about variances, not about distributional shape, so it does not need the errors to be bell-shaped.
That is why we filed normality as a separate add-on.

**The intuition for what "best" buys you.** Every linear unbiased estimator is unbiased — they all
center on $\boldsymbol{\beta}$, like a roomful of archers all aiming true. Gauss–Markov says OLS is
the archer with the tightest cluster. In Chapter-1.3 language: since all the contestants have zero
bias, MSE equals variance for every one of them, so "minimum variance" *is* "minimum MSE within the
club." OLS gives you the most precise estimate, the narrowest confidence intervals, and the most
powerful t-tests available *without leaving the world of linear, unbiased recipes*. You cannot do
better on precision without either accepting bias or going nonlinear.

**A sketch of why it's true** (the full proof is an appendix exercise, but the shape of the
argument is worth seeing). Take any rival linear unbiased estimator and write it as OLS plus a
detour: $\tilde{\boldsymbol{\beta}} = \hat{\boldsymbol{\beta}} + \mathbf{D}\mathbf{y}$ for some
matrix $\mathbf{D}$ capturing how the rival differs. Demanding that $\tilde{\boldsymbol{\beta}}$ be
*unbiased for every possible $\boldsymbol{\beta}$* forces an algebraic condition on $\mathbf{D}$ —
specifically $\mathbf{D}\mathbf{X} = \mathbf{0}$, the detour must be "orthogonal" to the
regressors. When you then compute the rival's variance, that orthogonality makes the cross-terms
vanish and you are left with

$$
\operatorname{Var}(\tilde{\boldsymbol{\beta}}\mid\mathbf{X})
= \underbrace{\sigma^2(\mathbf{X}'\mathbf{X})^{-1}}_{\text{OLS variance}}
\;+\; \underbrace{\sigma^2\mathbf{D}\mathbf{D}'}_{\text{extra, never negative}} .
$$

The rival's variance is the OLS variance *plus a non-negative extra piece* ($\mathbf{D}\mathbf{D}'$
is a sum of squares; it can be zero but never negative). The only way to tie OLS is to set
$\mathbf{D} = \mathbf{0}$ — which makes you OLS. Any genuine deviation strictly *adds* variance.
This is the same shape of argument as the bias–variance decomposition: a target term plus a
non-negative penalty, minimized by killing the penalty. **The homoskedasticity assumption is doing
the load-bearing work** — it's what let us write $\operatorname{Var}(\boldsymbol{\varepsilon}\mid\mathbf{X})
= \sigma^2\mathbf{I}$ so the cross-terms cleanly cancel. Break it, and OLS is no longer guaranteed
best (a weighted estimator can beat it), which is the deeper reason Chapter 2.4 cares about
heteroskedasticity.

---

**Seeing unbiasedness and the variance formula in code.** Before we name the efficiency property,
let's confirm the two §2–§3 facts by faking Maya's universe. We *set* the true $\boldsymbol{\beta}$,
draw many samples that obey all four assumptions, and check that the OLS estimates center on the
truth and that their spread matches $\sigma^2(\mathbf{X}'\mathbf{X})^{-1}$.

```python
import numpy as np

rng = np.random.default_rng(420)

# --- the "true" world: rate = 12 - 0.42 * income(in $10k) + noise ---
beta_true = np.array([12.0, -0.42])     # [intercept, slope]
sigma = 1.5                             # error std, in percentage points
N = 400

# fix the regressors once (we condition on X), incomes spread around 6 (=$60k)
income = rng.normal(6.0, 3.0, size=N)
X = np.column_stack([np.ones(N), income])   # N x 2 design matrix, full rank

def one_ols_fit():
    eps = rng.normal(0.0, sigma, size=N)               # homoskedastic, mean-zero
    y = X @ beta_true + eps                            # the true model
    return np.linalg.solve(X.T @ X, X.T @ y)           # (X'X)^{-1} X'y

# draw 20,000 alternate universes, collect 20,000 beta-hats
betas = np.array([one_ols_fit() for _ in range(20_000)])

print("True beta ............", beta_true)
print("Mean of beta-hats ....", betas.mean(axis=0), "  (should ~ true: unbiased)")
print("Empirical Var(slope) .", betas[:, 1].var())

# theory: bottom-right of sigma^2 (X'X)^{-1}
theory_cov = sigma**2 * np.linalg.inv(X.T @ X)
print("Theory  Var(slope) ...", theory_cov[1, 1])
```

The mean of the twenty thousand slope estimates lands on $-0.42$ — unbiasedness, *seen* rather than
just proven — and the empirical variance of the slopes matches the bottom-right entry of
$\sigma^2(\mathbf{X}'\mathbf{X})^{-1}$ to two or three decimals. The formula and the histogram are
two views of the same object, exactly as they were for Priya's sample mean. The notebook `nb2.2`
takes this skeleton and adds a *rival* estimator to it, which is where "best" earns its keep.

## 5. Efficiency: the word for "smallest variance"

The property at the heart of "best" has a name we will use constantly: **efficiency**.

> Among a specified class of estimators, the **efficient** one is the member with the smallest
> variance. Gauss–Markov says OLS is efficient *within the class of linear unbiased estimators* —
> a property econometricians abbreviate as OLS being **the efficient estimator in its class**, or
> simply BLUE.

Three cautions keep "efficient" from being oversold, and each maps onto an assumption we can break.

First, efficiency is **relative to a class**. OLS is the most efficient *linear unbiased*
estimator. It is emphatically *not* claimed to be the most efficient estimator overall. If you are
willing to leave the linear club — for instance, by using maximum likelihood with a correctly
specified non-normal error distribution — you can sometimes beat OLS. Gauss–Markov is a champion of
a league, not of all leagues. (When the errors *are* normal, a bonus result we won't prove says OLS
also becomes efficient among *all* unbiased estimators, linear or not — normality promotes OLS from
league champion to world champion. That is one more thing Assumption 5 buys.)

Second, efficiency **dies with homoskedasticity**. When Assumption 4 fails — Maya's
heteroskedastic spread, wide for low earners and tight for high earners — OLS stays unbiased but is
no longer BLUE. A smarter recipe called **weighted least squares**, which down-weights the noisy
low-income observations, achieves lower variance. OLS becomes "linear unbiased but no longer best."
We mostly don't switch to weighted least squares in practice (it requires knowing the variance
pattern), but the loss of the efficiency *guarantee* is precisely why we patch the standard errors
in Chapter 2.4 instead of trusting the $\sigma^2(\mathbf{X}'\mathbf{X})^{-1}$ formula blindly.

Third, **efficiency presumes unbiasedness, and that presumption can be a trap** — which is the
bridge to the chapter's last and subtlest idea.

---

## 6. Unbiased versus consistent: a distinction that decides everything

Gauss–Markov is a *finite-sample* theorem. Every word of it — unbiased, minimum variance — is a
statement about a fixed $N$, exactly like the bias and variance of Chapter 1.3 §2–3. But Chapter
1.3 §5 introduced a second, large-sample virtue that lives in a different world: **consistency**,
the property that an estimator converges in probability to the truth as the sample grows,
$\hat{\boldsymbol{\beta}}_N \xrightarrow{p} \boldsymbol{\beta}$. These two virtues are *not the same
thing*, and confusing them is the most expensive conceptual error in all of applied work. So we'll
nail the distinction, then show why it reshapes how a modern econometrician reads Gauss–Markov.

Recall the two warnings from Chapter 1.3, now in regression dress:

- **Unbiased but inconsistent.** Imagine Maya, instead of using all $N$ loans, builds an estimator
  that uses only the first 5 loans and ignores the rest forever. By the §2 proof it is *unbiased* —
  five observations satisfy $\mathbb{E}[\boldsymbol{\varepsilon}\mid\mathbf{X}] = \mathbf{0}$ just
  fine — but its variance $\sigma^2(\mathbf{X}_5'\mathbf{X}_5)^{-1}$ never shrinks, no matter how
  many millions of loans she later collects, because the recipe throws them away. It never settles
  onto $\boldsymbol{\beta}$. Unbiased, inconsistent, useless.
- **Biased but consistent.** Conversely, many of the most important estimators in this book are
  *biased at every finite $N$ yet consistent* — their bias melts to zero as $N \to \infty$. The
  instrumental-variables estimator you'll meet later, and even some everyday adjustments, work
  exactly this way: a little finite-sample bias you tolerate because the estimator homes in on the
  truth with enough data. A biased-but-consistent estimator beats an unbiased-but-inconsistent one
  in any large dataset, every time.

So the two properties are logically independent: an estimator can have either, both, or neither.
**Unbiasedness is about the center of the sampling distribution at a fixed $N$; consistency is
about where that distribution collapses as $N\to\infty$.** OLS, gratifyingly, has *both* — it is
unbiased under Assumptions 1–3 *and* consistent under those same assumptions (its variance
$\sigma^2(\mathbf{X}'\mathbf{X})^{-1}$ shrinks toward zero as $N$ grows, because $\mathbf{X}'\mathbf{X}$
accumulates, so the centered-and-shrinking argument from Chapter 1.3 §5 applies). That double
virtue is part of why OLS is the workhorse.

But here is the practical reason a modern econometrician often cares *more* about consistency than
about unbiasedness or BLUE. In a serious empirical project Maya rarely has 50 observations where
exact unbiasedness and minimum-variance bragging rights matter; she has tens of thousands of loans.
With that much data, the Central Limit Theorem (Chapter 1.4) makes $\hat{\boldsymbol{\beta}}$
approximately normal whether or not the errors were normal, so the normality add-on barely matters;
and the finite-sample efficiency edge of BLUE over a near-rival is microscopic. What she cannot
escape, at *any* sample size, is a violation of Assumption 3. If income is correlated with omitted
creditworthiness, then — just as a consistent estimator of the wrong thing is still wrong (Priya's
miscounted county) — OLS converges *confidently to the biased number*. More data makes the wrong
answer *more precise*, not more correct. The standard error shrinks, the confidence interval
tightens triumphantly around a value that is not $\beta_1$.

**A number that should frighten you.** Suppose the *true* world is that rates depend on income only
through creditworthiness: high earners have better credit, and it's credit, not income per se, that
earns the lower rate. Say the genuine, direct effect of income on rate, holding credit fixed, is
*zero* — $\beta_1 = 0$. But Maya omits credit. Her income coefficient then picks up the full
indirect channel: it inherits (correlation of income with credit) $\times$ (effect of credit on
rate). If income and credit score correlate at $0.7$, and a one-unit credit improvement lowers rates
by enough, Maya's $\hat{\beta}_1$ might settle confidently at $-0.42$ — a strong, "significant,"
beautifully-precise estimate of an effect that *does not exist*. With 400 loans her standard error
is wide enough that she might hedge; with 400,000 loans the standard error shrinks to nothing and she
reports $-0.42$ with three stars and a tiny confidence interval. The data did not make her *more*
right. It made her *more sure of something false*. That is what "consistent estimator of the wrong
target" means in dollars and stars, and it is the entire motivation for Chapter 2.5.

That is the deepest lesson of the chapter, and it reorders the assumptions by how much they should
keep you up at night. A failure of homoskedasticity (Assumption 4) costs you efficiency and honest
standard errors — fixable in Chapter 2.4 with robust SEs, and survivable. A failure of normality
(Assumption 5) costs you exact small-sample inference — and the CLT mostly bails you out anyway. But
a failure of zero-conditional-mean (Assumption 3) costs you the *truth itself*, and **no amount of
data fixes it** — which is why Chapter 2.5, and the entire causal-inference machinery of Weeks 5
and 6, exists. Gauss–Markov hands you a beautiful guarantee, but it is a guarantee about *precision*
(variance), conditional on having already won the harder battle for *accuracy* (Assumption 3).
"Best" is a promise about the tightness of your arrows. It says nothing about whether you are aiming
at the right target.

---

## 7. Where this is heading

Step back and see the architecture. We signed a five-clause contract and watched it pay out in
three tiers. Assumptions 1–3 gave us **unbiasedness** — OLS aims at the true $\boldsymbol{\beta}$,
proven in three lines off the contamination identity $\hat{\boldsymbol{\beta}} = \boldsymbol{\beta}
+ (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\boldsymbol{\varepsilon}$. Adding Assumption 4 gave us the
variance formula $\sigma^2(\mathbf{X}'\mathbf{X})^{-1}$ and the **Gauss–Markov** guarantee that OLS
is **BLUE** — the most **efficient** estimator in the linear-unbiased club. Adding Assumption 5
will give us exact inference in small samples. And cutting across all of it, the
unbiased-versus-consistent distinction told us which violations are merely annoying (4 and 5) and
which are existential (3).

The rest of Week 2 is a guided tour of the broken clauses. Chapter 2.3 relaxes the *functional
form* side of linearity, adding logs, polynomials, and interactions, and diagnoses
multicollinearity. Chapter 2.4 confronts **heteroskedasticity** head-on — the failure of Assumption
4 — and builds the robust standard errors (HC1/HC2/HC3, and clustered) that let Maya report honest
uncertainty even when OLS is no longer BLUE. Chapter 2.5 stares down the assumption that matters
most, **zero conditional mean**, deriving the omitted-variable-bias formula straight off the line
where our §2 proof would collapse, and showing what measurement error does to it. By the end of the
week, Maya's $-0.42$ will either be a number she can defend or a number she knows to distrust — and
she'll be able to say *which assumption* makes the difference.

---

## Your Turn

Open **`nb2.2` — the Gauss–Markov Monte Carlo efficiency demo**. The notebook fakes a universe
where you *know* the true $\boldsymbol{\beta}$, then draws thousands of samples and computes, on
each, both the OLS estimate and a rival linear unbiased estimator (a deliberately clumsy weighted
estimator). You will watch both sampling distributions center on the truth — confirming both are
unbiased — while the OLS one is visibly *narrower*, letting you *see* BLUE: minimum variance among
linear unbiased competitors. Then you'll flip on heteroskedasticity and watch OLS lose its
efficiency crown to weighted least squares, and flip on an omitted variable and watch OLS converge,
with shrinking standard errors, onto the *wrong* number — consistency aimed at the wrong target.

**Check questions.**

1. In Maya's loan regression, suppose higher-income borrowers also tend to have longer credit
   histories (which she did not include), and longer histories independently lower rates. Which
   classical assumption is violated, is $\hat{\beta}_1$ still unbiased, and will collecting 10× more
   loans fix the problem? Point to the exact line in the §2 proof that breaks.

2. A classmate says: "OLS is BLUE, so it's always the best possible estimator." Give two distinct
   reasons this overstates the theorem — one about the *class* the word "best" is restricted to, and
   one about an assumption whose failure revokes the "B" while leaving $\hat{\boldsymbol{\beta}}$
   unbiased. Name the later chapter that handles the second case.

3. Construct, in words, an estimator of $\beta_1$ that is **unbiased but inconsistent**, and one
   that is **biased but consistent**. For each, state what happens to its sampling distribution as
   $N \to \infty$, and explain why a researcher with 100,000 loans would prefer the second.
