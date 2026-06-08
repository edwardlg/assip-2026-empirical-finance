# A.3 Asymptotics

Almost every standard error you have computed, or will compute, in this book rests on a single move: pretend the sample is large, and ask what the estimator's distribution settles into as the sample grows without bound. That is what "asymptotics" means — the behavior of estimators in the limit as $N \to \infty$. It sounds like an abstraction with no business near real data, since no dataset is infinite. The trick this section reveals is that the limit is not the point; the limit is a *good approximation* for the finite $N$ you actually have, and it is a far more honest one than pretending you know the exact small-sample distribution (which you almost never do). When Week 2 hands you a robust standard error, or Week 5 hands you a GRS $F$-statistic, the justification is asymptotic. This section assembles the small toolkit of theorems that turn "the sample is big" into "here is the distribution I can do inference with."

We lean on two companion sections. **A.1 Matrix Algebra** gives the matrix objects — $\mathbf{X}'\mathbf{X}$, its inverse, transposes — that appear in the sandwich formula at the end. We will use them as named pieces; if any feel unfamiliar, read A.1 first. We do not re-derive the Law of Large Numbers or the Central Limit Theorem here either: those were shown, not asserted, in **Week 1, Chapter 1.4**, and we recall them only as tools.

---

## 1. Two kinds of convergence

A regular sequence of numbers like $1, \tfrac12, \tfrac13, \dots$ converges to $0$ in the ordinary calculus sense: eventually it gets and stays arbitrarily close to its limit. Estimators are not numbers, though — they are *random variables*, because they depend on the random sample. The sample mean $\bar{x}$ from one draw of 252 days is a different number than from another draw. So "$\bar{x}$ converges to $\mu$" needs a definition that respects the randomness. There are two definitions we care about, and keeping them straight is the whole game.

### Convergence in probability

The first, weaker idea is **convergence in probability**, written $\hat\theta_N \xrightarrow{p} \theta$. Read it as: as the sample grows, the probability that the estimator misses the target by any fixed amount shrinks to zero. Concretely, pick any tolerance $\epsilon > 0$ — a hundredth of a cent, a thousandth of a percent, whatever you like — and look at the probability $\Pr(|\hat\theta_N - \theta| > \epsilon)$ that the estimate is more than $\epsilon$ away from the truth. Convergence in probability says that probability goes to $0$ as $N \to \infty$:

$$
\Pr\!\big(|\hat\theta_N - \theta| > \epsilon\big) \to 0 \quad \text{for every } \epsilon > 0.
$$

The picture to hold in your head is a histogram of $\hat\theta_N$ over many hypothetical samples: as $N$ grows, that histogram squeezes tighter and tighter around the single point $\theta$, until essentially all its mass sits in a sliver around the truth. An estimator with this property is called **consistent**. The Law of Large Numbers from Ch 1.4 is exactly the statement that the sample mean is consistent for the population mean: $\bar{x} \xrightarrow{p} \mu$. Consistency is the baseline demand we make of any estimator — collect enough honest data and you home in on the right answer. An estimator that is *not* consistent (one whose histogram refuses to collapse onto the truth no matter how much data you feed it) is broken, and a large chunk of Weeks 2 through 8 is about diagnosing exactly when our estimators stop being consistent (omitted variables, measurement error, bad instruments).

### Convergence in distribution

The second, subtler idea is **convergence in distribution**, written $Z_N \xrightarrow{d} Z$. This is not about a quantity homing in on a point — it is about the *entire shape* of a distribution settling down. We say $Z_N \xrightarrow{d} Z$ when the cumulative distribution function of $Z_N$ approaches that of $Z$ at every point where the limit is continuous. In plain terms: histogram $Z_N$ for larger and larger $N$, and the silhouette of that histogram morphs into the silhouette of $Z$'s distribution. The Central Limit Theorem is the headline example. Standardize the sample mean and its shape converges to the standard normal, no matter what messy distribution the raw data came from:

$$
\frac{\bar{x} - \mu}{\sigma/\sqrt{N}} \xrightarrow{d} N(0,1).
$$

Here is the distinction that trips everyone up, so we state it bluntly. Convergence *in probability* is about a target collapsing to a point: the thing stops being random. Convergence *in distribution* is about a shape stabilizing: the thing stays random forever, but its randomness takes on a known, fixed form. The two answer different questions. The LLN ($\xrightarrow{p}$) tells you *where* $\bar{x}$ ends up — on $\mu$. The CLT ($\xrightarrow{d}$) tells you the *shape of the cloud* of misses around that destination, once you have magnified it by $\sqrt{N}$. Chapter 1.4 made exactly this point with the microscope image, and it is worth re-reading if the difference still feels slippery.

One technical relationship is worth knowing because we use it implicitly. Convergence in probability is *stronger*: if $Z_N \xrightarrow{p} c$ to a constant $c$, then automatically $Z_N \xrightarrow{d} c$ (the limiting "distribution" is just a spike at $c$). The reverse is false in general — converging in distribution to a genuinely random $Z$ says nothing about any particular $Z_N$ landing near a fixed point. The one exception is the special case just named: convergence in distribution to a *constant* is the same as convergence in probability to it. That equivalence is the hinge that makes Slutsky's theorem, next, do its work.

---

## 2. Slutsky's theorem: mixing the two convergences

Real estimators are built from several moving parts, and those parts converge in different ways. In the $t$-statistic from Ch 1.5,

$$
t = \frac{\bar{x} - \mu_0}{s/\sqrt{N}},
$$

the numerator (suitably scaled) converges *in distribution* to a normal by the CLT, while the denominator's ingredient $s$ converges *in probability* to the true $\sigma$ by the LLN. To say anything about the ratio, we need a rule for combining a "$\xrightarrow{d}$" piece with a "$\xrightarrow{p}$" piece. That rule is **Slutsky's theorem**.

State it plainly: if $Z_N \xrightarrow{d} Z$ and $A_N \xrightarrow{p} a$ (where $a$ is a constant), then sums, products, and ratios behave the way you would naively hope —

$$
Z_N + A_N \xrightarrow{d} Z + a, \qquad A_N Z_N \xrightarrow{d} a Z, \qquad \frac{Z_N}{A_N} \xrightarrow{d} \frac{Z}{a} \;\;(a \neq 0).
$$

The intuition is that a quantity converging in probability to a constant is, for large $N$, *effectively that constant* — it has stopped wobbling — so you can treat it as a fixed number that scales or shifts the still-random $Z_N$. The slogan is: **once something has converged to a constant, you may substitute the constant.** The fine print, which earns its keep in counterexamples, is that $a$ must be a constant; if $A_N$ converged in distribution to a genuinely random thing, you could *not* just multiply the limits, because $Z_N$ and $A_N$ might be correlated in ways the limits hide.

A number makes the substitution rule tangible. Suppose at $N=500$ your CLT-standardized numerator has realized a value near $1.8$, and your sample standard deviation $s$ has come in at $0.97$ when the truth is $\sigma=1.00$, so the correction factor $\sigma/s = 1/0.97 \approx 1.031$. The $t$-statistic is $1.8 \times 1.031 \approx 1.856$ — barely nudged from the $1.8$ you would get if you knew $\sigma$ exactly. At $N=20$, $s$ might instead land at $0.85$, giving a correction of $1.176$ and a $t$ of $2.12$ — a meaningful distortion. The whole content of Slutsky here is that as $N$ grows, $s$ presses against $\sigma$, the correction factor presses against $1$, and the distortion vanishes. Watch it close out the $t$-statistic algebraically. Write

$$
t = \frac{\bar{x} - \mu_0}{s/\sqrt{N}} = \underbrace{\frac{\bar{x} - \mu_0}{\sigma/\sqrt{N}}}_{\xrightarrow{d}\,N(0,1)} \cdot \underbrace{\frac{\sigma}{s}}_{\xrightarrow{p}\,1}.
$$

The first factor is the CLT-standardized mean, heading to $N(0,1)$ in distribution. The second factor is $\sigma/s$; since $s \xrightarrow{p} \sigma$, this ratio $\xrightarrow{p} 1$. Slutsky says the product converges in distribution to $N(0,1) \times 1 = N(0,1)$. That is the precise reason the $t$-statistic is approximately standard normal in large samples even though we had to *estimate* the standard deviation — the estimation error in $s$ washes out asymptotically, and the small-sample penalty (the fatter tails of the $t_{N-1}$ distribution) vanishes as $N \to \infty$, exactly as Ch 1.5 claimed. Every "$t$ is approximately $z$ for large $N$" sentence in this book is Slutsky's theorem wearing plain clothes.

---

## 3. The continuous-mapping theorem: convergence survives smooth transformations

The next tool answers a question you will ask constantly: if my estimator converges, does a *function* of it also converge? You estimate a variance and want a standard deviation (a square root). You estimate a slope and a mean and want their ratio. You estimate log-odds and want a probability. Does feeding a convergent estimator through a transformation preserve the convergence?

The **continuous-mapping theorem** says yes, as long as the transformation is continuous at the limit. Precisely: if $g$ is a continuous function, then

$$
Z_N \xrightarrow{p} c \;\;\Longrightarrow\;\; g(Z_N) \xrightarrow{p} g(c), \qquad\text{and}\qquad Z_N \xrightarrow{d} Z \;\;\Longrightarrow\;\; g(Z_N) \xrightarrow{d} g(Z).
$$

Convergence passes through continuous functions untouched. The intuition is almost too simple to state: continuity means "small input changes produce small output changes," so if the input is settling down, the output cannot be doing anything wild. If $\bar{x}$ is collapsing onto $\mu$, then $\bar{x}^2$ is collapsing onto $\mu^2$, $\sqrt{\bar{x}}$ (for positive values) onto $\sqrt{\mu}$, and so on. The sample standard deviation is consistent for the population standard deviation precisely because $s = \sqrt{s^2}$ and the square root is continuous on positive numbers: $s^2 \xrightarrow{p} \sigma^2$ implies $s \xrightarrow{p} \sigma$, which is the fact Slutsky just consumed.

The "continuous at the limit" caveat is the failure mode, and it bites at exactly the points where the function does something abrupt. The ratio $g(u,v) = u/v$ is continuous everywhere *except* where the denominator is zero. So a statistic like $\hat\beta_1 / \hat\beta_2$ converges nicely as long as the true $\beta_2 \neq 0$ — but if $\beta_2$ is truly zero (or so small the estimate routinely flips sign), you are evaluating the transformation right at its discontinuity, and the theorem offers no comfort. This is not a textbook curiosity: it is the deep reason "weak instruments" misbehave (the relevant ratio has a near-zero denominator) and the reason ratio estimators built on a denominator that might vanish are treacherous. Whenever you transform an estimate, the reflex is to ask: *is my function smooth at the value I'm actually near?*

---

## 4. The delta method: standard errors for transformed estimates

The continuous-mapping theorem tells you the *center* a transformed estimator converges to. It does not, by itself, tell you the transformed estimator's *standard error* — and you need that to put a confidence interval on the transformed quantity. Supplying that standard error is the job of the **delta method**, and it is the most practically useful single tool in this entire section.

The result in one sentence: **to find the standard error of $g(\hat\theta)$, multiply the standard error of $\hat\theta$ by the absolute slope $|g'(\theta)|$ of the transformation at the estimate.** That is the whole idea. The machinery behind it is the first-order Taylor expansion — exactly the linear approximation from AP Calculus. Near the true value $\theta$, a smooth function looks like its tangent line:

$$
g(\hat\theta) \approx g(\theta) + g'(\theta)\,(\hat\theta - \theta).
$$

Read that as: the deviation of $g(\hat\theta)$ from $g(\theta)$ is roughly the deviation of $\hat\theta$ from $\theta$, *stretched by the slope* $g'(\theta)$. If the slope is steep, small wiggles in $\hat\theta$ become big wiggles in $g(\hat\theta)$; if the slope is shallow, wiggles get damped. Variance scales with the square of a multiplicative factor, so the variance of the transformed estimate is the variance of the original, multiplied by $[g'(\theta)]^2$:

$$
\operatorname{Var}\big(g(\hat\theta)\big) \approx [g'(\theta)]^2 \cdot \operatorname{Var}(\hat\theta),
\qquad\text{hence}\qquad
\operatorname{se}\big(g(\hat\theta)\big) \approx |g'(\theta)| \cdot \operatorname{se}(\hat\theta).
$$

Stated as a distributional result, if $\sqrt{N}(\hat\theta - \theta) \xrightarrow{d} N(0,\,\sigma^2)$, then $\sqrt{N}\big(g(\hat\theta) - g(\theta)\big) \xrightarrow{d} N\!\big(0,\,[g'(\theta)]^2\sigma^2\big)$. In practice you do not know $\theta$, so you evaluate the derivative at the estimate $\hat\theta$ — which is fine, because by continuous mapping $g'(\hat\theta) \xrightarrow{p} g'(\theta)$ and Slutsky lets you swap it in.

### A worked finance example: the standard error of a Sharpe ratio

Sam, who runs trading simulations, has 252 daily returns from a strategy. The strategy's **Sharpe ratio** — a workhorse of finance — is the mean return divided by its standard deviation, $\text{SR} = \mu / \sigma$, measuring reward per unit of risk. Sam can estimate it directly as $\widehat{\text{SR}} = \bar{x} / s$. But Sam needs a *standard error* on that number, because a Sharpe ratio of $0.10$ daily means nothing without knowing whether it is $0.10 \pm 0.02$ or $0.10 \pm 0.15$. The Sharpe ratio is a nonlinear function of estimated quantities, so the delta method is exactly the tool.

To keep the algebra clean, hold $\sigma$ fixed and treat the Sharpe ratio as a function of the mean alone: $g(\mu) = \mu/\sigma$, so the estimate is $g(\bar{x}) = \bar{x}/\sigma$. The derivative is $g'(\mu) = 1/\sigma$, a constant here. The sample mean has $\operatorname{se}(\bar{x}) = \sigma/\sqrt{N}$. The delta method then gives

$$
\operatorname{se}\big(\widehat{\text{SR}}\big) \approx |g'(\mu)| \cdot \operatorname{se}(\bar{x}) = \frac{1}{\sigma}\cdot\frac{\sigma}{\sqrt{N}} = \frac{1}{\sqrt{N}}.
$$

Put a number on it. With $N = 252$, $\operatorname{se}(\widehat{\text{SR}}) \approx 1/\sqrt{252} = 1/15.87 \approx 0.063$. So if Sam's estimated daily Sharpe is $0.10$, the rough $95\%$ confidence interval is $0.10 \pm 1.96 \times 0.063 = [-0.023,\,0.223]$ — which *includes zero*. A single year of data simply cannot distinguish Sam's strategy from a coin flip at the daily horizon, and the delta method made that uncomfortable fact computable in two lines. (The full delta-method standard error that also accounts for the sampling noise in $s$, and for fat tails in returns, adds a correction term; the version here, treating $\sigma$ as known, captures the dominant piece and the right $1/\sqrt{N}$ scaling. The honest practitioner reports the fuller formula or bootstraps — but the logic is identical.)

A second, even more common case shows how lightweight the rule is. Suppose Priya estimates an insurance-loss model and reports a coefficient $\hat\beta$ whose interpretation is cleanest after exponentiating — she wants $g(\hat\beta) = e^{\hat\beta}$, a multiplicative risk factor rather than a log-scale slope. The derivative is $g'(\beta) = e^{\beta}$, so the delta method gives $\operatorname{se}(e^{\hat\beta}) \approx e^{\hat\beta}\cdot\operatorname{se}(\hat\beta)$. If $\hat\beta = 0.40$ with $\operatorname{se}(\hat\beta) = 0.10$, then $e^{0.40}\approx 1.49$ and its standard error is $\approx 1.49\times 0.10 = 0.149$. Notice the standard error of the transformed quantity is *not* symmetric in spirit with the original — it has been stretched by the local slope $e^{0.40}$ — which is exactly the delta method's job: report uncertainty in the units you actually care about. (For a quantity that must stay positive, like $e^{\hat\beta}$, many analysts prefer to build the interval on the log scale and exponentiate the endpoints, sidestepping the symmetric-interval awkwardness; the delta-method standard error is the quick version when a symmetric band is good enough.)

The delta method also reveals *when it fails*, and the failure is the same one as continuous mapping. The approximation is a tangent-line approximation, so it is trustworthy only when $g$ is roughly linear over the region where $\hat\theta$ realistically lands, and only when the derivative $g'(\theta)$ is not zero. If $g'(\theta) = 0$ — the function is flat at the true value — the first-order term vanishes and the leading variance term is zero, which is the method's way of telling you the simple formula has broken and you need a second-order (curvature) expansion. And for the Sharpe ratio specifically, if the true mean is near zero relative to its noise, the *full* version (varying both $\bar{x}$ and $s$) has a denominator that can get small, dragging in the same near-zero-denominator pathology continuous mapping warned about. The reflex, again: check that your transformation is smooth and non-flat near where the estimate actually lives.

---

## 5. The sandwich variance estimator: where robust standard errors come from

We close with the tool that ties this section to the regression engine, and the one whose formula looks most intimidating before you see where it comes from. In **Week 2, Chapter 2.4**, you met the **robust** (heteroskedasticity-consistent) standard error, whose variance matrix is

$$
\widehat{\operatorname{Var}}(\hat{\boldsymbol\beta}) = (\mathbf{X}'\mathbf{X})^{-1}\,\mathbf{X}'\hat{\boldsymbol\Omega}\,\mathbf{X}\,(\mathbf{X}'\mathbf{X})^{-1}.
$$

It is called a **sandwich** because it has the shape of one: two identical "bread" pieces $(\mathbf{X}'\mathbf{X})^{-1}$ on the outside, and a "meat" piece $\mathbf{X}'\hat{\boldsymbol\Omega}\mathbf{X}$ in the middle. The asymptotic ideas of this section are precisely what justify it, and you can read the whole formula off the OLS estimator with no new machinery.

Start from the estimator itself (matrix details in A.1; here we just track the pieces). Writing $\mathbf{y} = \mathbf{X}\boldsymbol\beta + \boldsymbol\varepsilon$ and substituting,

$$
\hat{\boldsymbol\beta} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}
= \boldsymbol\beta + (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\boldsymbol\varepsilon.
$$

The estimation error is the second term: $\hat{\boldsymbol\beta} - \boldsymbol\beta = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\boldsymbol\varepsilon$. Take the variance of this random quantity. The factor $(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'$ is (conditional on $\mathbf{X}$) a fixed matrix multiplying the random vector $\boldsymbol\varepsilon$, and the rule for the variance of a matrix-times-random-vector $\mathbf{A}\boldsymbol\varepsilon$ is $\mathbf{A}\,\operatorname{Var}(\boldsymbol\varepsilon)\,\mathbf{A}'$. Let $\boldsymbol\Omega = \operatorname{Var}(\boldsymbol\varepsilon\mid\mathbf{X})$ be the error variance matrix. With $\mathbf{A} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'$ and its transpose $\mathbf{A}' = \mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}$ (using that $(\mathbf{X}'\mathbf{X})^{-1}$ is symmetric),

$$
\operatorname{Var}(\hat{\boldsymbol\beta}\mid\mathbf{X})
= \mathbf{A}\,\boldsymbol\Omega\,\mathbf{A}'
= (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\,\boldsymbol\Omega\,\mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}.
$$

There is the sandwich, derived in one line — it is nothing more exotic than the variance-of-a-linear-combination rule applied to the OLS error. The bread $(\mathbf{X}'\mathbf{X})^{-1}$ comes from how $\hat{\boldsymbol\beta}$ weights the data; the meat carries $\boldsymbol\Omega$, the structure of the errors.

Now the punchline that explains the whole Week 2 saga. If you *assume* the classical condition — errors all share one variance and are uncorrelated, $\boldsymbol\Omega = \sigma^2\mathbf{I}$ — the meat collapses: $\mathbf{X}'(\sigma^2\mathbf{I})\mathbf{X} = \sigma^2\mathbf{X}'\mathbf{X}$, and the sandwich telescopes into the familiar classical formula $\sigma^2(\mathbf{X}'\mathbf{X})^{-1}$. So the classical standard error is just the sandwich under a strong assumption about the meat. The robust standard error refuses that assumption. It does not need to know the true $\boldsymbol\Omega$; it only needs the *meat* $\mathbf{X}'\boldsymbol\Omega\mathbf{X}$, and that middle quantity can be estimated consistently from the data without ever pinning down the full $\boldsymbol\Omega$. White's (1980) insight, which Ch 2.4 develops, is to estimate the meat with the squared OLS residuals, $\hat{\boldsymbol\Omega} = \operatorname{diag}(\hat\varepsilon_1^2,\dots,\hat\varepsilon_N^2)$, so that

$$
\mathbf{X}'\hat{\boldsymbol\Omega}\mathbf{X} = \sum_{i=1}^N \hat\varepsilon_i^2\,\mathbf{x}_i\mathbf{x}_i'.
$$

This is where asymptotics is load-bearing, and it is worth pausing on the apparent paradox because it is the single most counterintuitive thing in the chapter. Each individual residual $\hat\varepsilon_i^2$ is a terrible estimate of its own error variance — it is a single squared number, and a single draw squared tells you almost nothing about the variance that generated it. You cannot estimate $N$ separate variances from $N$ data points; there is one observation per quantity. So how can a sum of $N$ hopeless estimates produce a good one? The answer is that we never needed the $N$ individual variances — we only ever needed their *weighted aggregate* $\mathbf{X}'\boldsymbol\Omega\mathbf{X}$. The sum $\sum_i \hat\varepsilon_i^2\,\mathbf{x}_i\mathbf{x}_i'$ is an average of $N$ terms, and by a Law-of-Large-Numbers argument that average converges in probability to the true population meat $\mathbb{E}[\varepsilon_i^2\,\mathbf{x}_i\mathbf{x}_i']$ — even though no single term is reliable. The unreliable pieces cancel in exactly the way Ch 1.4 described: each $\hat\varepsilon_i^2$ overshoots or undershoots its own true variance, but when you add up many of them the overshoots and undershoots offset, and the aggregate homes in on the right number. Consistency comes from the aggregation, not from any single term being trustworthy.

A one-line numerical sanity check makes the point concrete. Suppose the true error variances along the diagonal of $\boldsymbol\Omega$ are $1, 4, 1, 4, \dots$ (heteroskedastic — alternating between two regimes). Any one squared residual might land at, say, $0.1$ when its true variance is $4$, a wild miss. But average a thousand of them and the sample mean of the squared residuals settles toward the true average variance $2.5$, with the misses washing out. The robust meat is just this same averaging done with the $\mathbf{x}_i\mathbf{x}_i'$ weights attached. Then continuous mapping (the inverse and the matrix products are smooth functions) carries that convergence through to the assembled sandwich, and a CLT-plus-Slutsky argument delivers the asymptotic normality that lets you read $t$-statistics off $\hat{\boldsymbol\beta}$ divided by the square roots of the sandwich's diagonal. The robust standard error is *not* exact in any finite sample — and Ch 2.4's HC1/HC2/HC3 corrections exist precisely to patch up its small-sample behavior — but it is *consistent*, meaning it gets the variance right as $N$ grows, which is the strongest honest guarantee available when you refuse to assume you know the error structure.

The same skeleton extends to the messier worlds of Week 2 and beyond. Cluster-robust standard errors keep the bread and replace the meat with a *block-diagonal* $\hat{\boldsymbol\Omega}$ that allows errors within a firm or a year to correlate; HAC (Newey–West) standard errors fill in off-diagonal bands to allow serial correlation over time. In every case the architecture is identical — outer bread $(\mathbf{X}'\mathbf{X})^{-1}$ from the estimator, inner meat carrying whatever error structure you are willing to allow, and an asymptotic argument certifying that the estimated meat converges to the truth. Once you see the sandwich as "the variance-of-a-linear-combination rule, with the meat estimated by averaging," the alphabet soup of HC0/HC1/HC2/HC3, clustered, and HAC stops being a list to memorize and becomes a single idea with different fillings.

---

## 6. The toolkit, assembled

Step back and see how the five tools chain together to do one job: turn "I have an estimator and a big sample" into "here is the distribution I can test with." The **LLN** ($\xrightarrow{p}$, from Ch 1.4) makes your estimators consistent — they land on the truth. The **CLT** ($\xrightarrow{d}$, from Ch 1.4) makes their rescaled errors normal, so you have a known shape to compute tail probabilities from. **Slutsky** lets you plug consistent estimates (like $s$ for $\sigma$, or the estimated meat for the true meat) into a converging-in-distribution expression without spoiling the normal limit. The **continuous-mapping theorem** lets convergence ride through any smooth transformation. The **delta method** is continuous mapping plus a Taylor expansion, delivering standard errors for nonlinear functions of estimates. And the **sandwich estimator** is the variance-of-a-linear-combination rule whose middle piece these theorems certify you can estimate by averaging. Every standard error, $t$-statistic, confidence interval, and joint $F$-test you compute for the rest of the camp is some combination of these five moves. They are the reason the word "approximately" in "$\hat\beta$ is approximately normal" is a promise you can take to the bank, not a hope.
