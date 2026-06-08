# A.4 Probability Distributions Reference

Six distributions do almost all the work in this book. You do not need to derive them, and you certainly do not need to memorize their density formulas — `scipy.stats` knows those. What you need is a working acquaintance: what shape each one has, what its mean and variance are, *where it shows up* in the camp, and how the six are secretly related to one another. That last part is the payoff. These are not six unrelated facts to file away; they are a small family tree, and once you see the relationships — the $t$ becomes the Normal, the $F$ is a ratio of chi-squareds, a pile of Bernoullis is a Binomial — the whole set collapses into something you can reconstruct from memory.

This section is a reference: skim it now, return to it whenever a distribution surfaces in a chapter. Notation follows the rest of Appendix A. We write a density (for continuous variables) as a *pdf* and a probability (for discrete variables) as a *pmf*.

---

## The reference table

| Distribution | pdf / pmf | Mean | Variance | First appears |
|---|---|---|---|---|
| Normal $N(\mu,\sigma^2)$ | $\dfrac{1}{\sigma\sqrt{2\pi}}\exp\!\Big(-\dfrac{(x-\mu)^2}{2\sigma^2}\Big)$ | $\mu$ | $\sigma^2$ | Week 1, Ch 1.4 (CLT) |
| Student's $t_\nu$ | $\dfrac{\Gamma\!\big(\frac{\nu+1}{2}\big)}{\sqrt{\nu\pi}\,\Gamma\!\big(\frac{\nu}{2}\big)}\Big(1+\dfrac{x^2}{\nu}\Big)^{-\frac{\nu+1}{2}}$ | $0$ (for $\nu>1$) | $\dfrac{\nu}{\nu-2}$ (for $\nu>2$) | Week 1, Ch 1.5 ($t$-test) |
| Chi-squared $\chi^2_k$ | $\dfrac{1}{2^{k/2}\Gamma(k/2)}\,x^{k/2-1}e^{-x/2}$, $x>0$ | $k$ | $2k$ | Weeks 2 / 5 (joint tests) |
| $F_{d_1,d_2}$ | ratio form (see below) | $\dfrac{d_2}{d_2-2}$ (for $d_2>2$) | involved; see prose | Weeks 2 / 5 (GRS) |
| Bernoulli$(p)$ | $p^x(1-p)^{1-x}$, $x\in\{0,1\}$ | $p$ | $p(1-p)$ | Week 1 (coin-flip lab) |
| Binomial$(n,p)$ | $\binom{n}{x}p^x(1-p)^{n-x}$ | $np$ | $np(1-p)$ | Week 1 (denial counts) |
| Poisson$(\lambda)$ | $\dfrac{\lambda^x e^{-\lambda}}{x!}$, $x=0,1,2,\dots$ | $\lambda$ | $\lambda$ | counts (e.g. patents) |

Here $\Gamma(\cdot)$ is the gamma function, a continuous generalization of the factorial; you will never evaluate it by hand. Now the prose for each.

---

## Normal

The **Normal** (or Gaussian) is the bell curve, the centerpiece of the whole edifice. Its two parameters say everything: the mean $\mu$ sets where the peak sits, and the variance $\sigma^2$ sets how wide the bell is. The **standard normal** $N(0,1)$ has $\mu=0$, $\sigma=1$, and is the version you standardize *to*. Roughly $68\%$ of the mass lies within one standard deviation of the mean, $95\%$ within $1.96$ standard deviations (the source of the famous "1.96"), and $99.7\%$ within three — numbers worth knowing cold, because they are the mental ruler you use to judge whether a $t$-statistic is surprising.

The Normal is everywhere in this book for one reason, and it is not that financial data are normal — they emphatically are not. It is the **Central Limit Theorem** of Week 1, Ch 1.4: averages and sums of many independent pieces converge in distribution to the Normal regardless of the shape of the raw data. So the Normal shows up not as a model of returns themselves but as the model of *estimators* — sample means, regression coefficients, anything built by aggregating. Every $z$-statistic, the large-sample form of every $t$-statistic, and the asymptotic normality of $\hat{\boldsymbol\beta}$ in Week 2 are Normal in their bones. When you read "$\hat\beta$ is approximately normal," that is the CLT plus the asymptotic toolkit of A.3 talking.

Two computational facts about the Normal earn their keep constantly. First, *any* normal becomes the standard normal by standardizing: if $X \sim N(\mu,\sigma^2)$ then $(X-\mu)/\sigma \sim N(0,1)$, which is why one table (or one `scipy.stats.norm` object) covers every normal you will ever meet. Second, a *linear combination* of independent normals is again normal — sum two normals and you get a normal whose mean and variance are the sums of the pieces. That closure property is quietly behind portfolio mathematics (a weighted sum of normal asset returns is normal) and is the deeper reason the CLT's limit is the Normal specifically: the bell is the one finite-variance shape stable under the summing-and-rescaling that averaging performs.

---

## Student's t

The **Student's $t$** is the Normal's cautious cousin: same symmetric, centered-at-zero bell shape, but with *heavier tails*. Extreme values are more likely under the $t$ than under the Normal of matching width. The single parameter $\nu$ (the **degrees of freedom**) controls how heavy those tails are — small $\nu$ means fat tails, large $\nu$ means nearly Normal. Its variance, $\nu/(\nu-2)$, is larger than the standard normal's $1$ and only exists when $\nu>2$; for $\nu\le 2$ the tails are so heavy the variance is infinite, the cautionary tale Devon met in Ch 1.4.

The $t$ enters in Week 1, Ch 1.5, for an exact and necessary reason: when you estimate the standard deviation $\sigma$ with the sample $s$ rather than knowing it, the test statistic $(\bar{x}-\mu_0)/(s/\sqrt{N})$ no longer follows the Normal but the $t$ with $N-1$ degrees of freedom. The fatter tails are precisely the penalty for not knowing $\sigma$ — you are a little more likely to see extreme statistics, so the critical values sit a little farther out. This is the distribution behind every regression coefficient's $t$-statistic and reported $p$-value.

**The key relationship: $t_\nu \to N(0,1)$ as $\nu\to\infty$.** As the degrees of freedom grow, the estimation noise in $s$ vanishes (Slutsky's theorem, A.3), the tails thin out, and the $t$ becomes indistinguishable from the standard Normal. By $\nu \approx 30$ they are already nearly identical, which is why with the $N=252$ samples typical in this book, practitioners use $t$ and $z$ critical values interchangeably. The $t$ earns its keep in *small* samples — a study of 12 firms — where the tail correction genuinely changes the verdict.

---

## Chi-squared

The **chi-squared** distribution, $\chi^2_k$, is the distribution of a *sum of squares of independent standard normals*: if $Z_1,\dots,Z_k$ are independent $N(0,1)$, then $Z_1^2+\cdots+Z_k^2 \sim \chi^2_k$. Because it is a sum of squares it lives only on the positive numbers, and it is right-skewed (a long tail to the right), though it grows more symmetric as the degrees of freedom $k$ rise. Its mean is exactly $k$ and its variance $2k$ — both easy to remember once you know it is built from $k$ squared standard normals, each contributing mean $1$ and variance $2$.

Chi-squared shows up wherever we measure *total squared deviation* and wherever we run **joint tests** — asking whether several parameters are zero *all at once* rather than one at a time. The sample variance is, up to scaling, chi-squared distributed: when the data are normal, $(N-1)s^2/\sigma^2 \sim \chi^2_{N-1}$, the precise statement behind the "$N-1$ degrees of freedom" you spend estimating the mean. This is exactly why it pairs with the Normal to build the $t$: a standard normal divided by the square root of an independent chi-squared-over-its-degrees-of-freedom *is* a Student's $t$, $t_\nu = Z/\sqrt{\chi^2_\nu/\nu}$. So the three continuous distributions you have met so far are one construction seen from different angles — the Normal on top, the chi-squared underneath, the $t$ their ratio. More importantly for Weeks 2 and 5, a **Wald statistic** that tests several regression restrictions simultaneously is asymptotically chi-squared, with degrees of freedom equal to the number of restrictions (the asymptotics of A.3 are what deliver that limit). When Week 1's multiple-testing problem warns you not to eyeball 25 separate $t$-statistics, the chi-squared — and its finite-sample sibling, the $F$ — is the honest single-number alternative that accounts for testing everything together, because it folds all the restrictions into one statistic with one critical value rather than 25 separate chances to be fooled by noise.

---

## F

The **$F$ distribution**, $F_{d_1,d_2}$, is a **ratio of two independent chi-squared variables, each divided by its own degrees of freedom**:

$$
F = \frac{\chi^2_{d_1}/d_1}{\chi^2_{d_2}/d_2} \sim F_{d_1,d_2}.
$$

Like the chi-squared it is positive and right-skewed, with two degrees-of-freedom parameters: $d_1$ for the numerator, $d_2$ for the denominator. Its mean is $d_2/(d_2-2)$ for $d_2>2$ (close to $1$ when $d_2$ is large, since a ratio of two things each averaging near $1$ should hover near $1$). The variance formula is messier and not worth memorizing.

The $F$ is the finite-sample workhorse for **joint hypothesis tests**. Whenever you ask "are these several coefficients *jointly* zero?" — the comparison of a restricted to an unrestricted regression — the test statistic follows an $F$. Its headline appearance in this book is the **GRS test** of Week 5 (Gibbons, Ross & Shanken 1989), which asks whether the intercepts ($\alpha$'s) of many asset-pricing regressions are simultaneously zero. The GRS statistic is a single $F$, and an asset-pricing model "passes" when GRS *fails to reject* — the rare case where the researcher is rooting for the null. The intuition is the joint-test logic from Week 2: instead of 25 separate intercept questions, ask one question about all of them at once, accounting for the fact that the residuals are correlated.

**Two relationships tie the $F$ to its neighbors.** First, the $F$ is by construction a ratio of (scaled) chi-squareds, so it inherits its skew and positivity from them. Second, $d_1 \cdot F_{d_1,d_2} \to \chi^2_{d_1}$ as $d_2\to\infty$: when the denominator degrees of freedom grow, the denominator chi-squared (divided by $d_2$) converges to $1$ by the LLN, and the $F$ collapses to a scaled chi-squared. This is the finite-sample-($F$)-versus-asymptotic-(chi-squared) pairing that mirrors the $t$-versus-Normal pairing exactly. And the simplest tie of all: $F_{1,d_2} = t_{d_2}^2$ — a one-restriction $F$ test is just the square of the corresponding $t$ test, so the two never disagree.

---

## Bernoulli and Binomial

The **Bernoulli$(p)$** is the simplest distribution there is: a single trial with two outcomes, $1$ ("success") with probability $p$ and $0$ ("failure") with probability $1-p$. Its mean is $p$ and its variance $p(1-p)$ — note the variance is largest at $p=0.5$ (maximum uncertainty) and shrinks to zero as $p$ approaches $0$ or $1$ (near-certainty). This is the mathematical atom of a coin flip, and it anchors **Week 1's coin-flip lab**, where you build a sampling-distribution universe from scratch out of nothing but Bernoulli draws. It is also the natural model for any single yes/no outcome: a loan **denial** in Maya's fair-lending work, a default, a click, a fraud flag.

The **Binomial$(n,p)$** is what you get when you **add up $n$ independent Bernoulli$(p)$ trials and count the successes**. That is the key relationship, stated plainly: *a sum of $n$ Bernoullis is a Binomial.* If each of $n$ loan applications is denied independently with probability $p$, the total number of denials is Binomial$(n,p)$. Its mean $np$ and variance $np(1-p)$ are just $n$ copies of the Bernoulli's, exactly as you would expect from summing $n$ independent pieces. The pmf carries a binomial coefficient $\binom{n}{x}$ because there are many distinct orderings of $x$ successes among $n$ trials.

There is one more relationship worth holding: by the **CLT**, a Binomial with large $n$ is approximately Normal, $N(np,\,np(1-p))$ — because it is, after all, a sum of many independent pieces. This is why a count of denials, or the empirical size of a test you measure by simulation in the coin-flip lab, can be given a Normal-based confidence interval once $n$ is large enough. The Bernoulli is the atom, the Binomial is the sum, and the Normal is the large-sample limit of the sum — three links in one short chain.

---

## Poisson

The **Poisson$(\lambda)$** models **counts of rare events over a fixed window** — events that happen at some average rate $\lambda$ but whose exact number is random. Its defining quirk is that its **mean and variance are both equal to $\lambda$**. The classic empirical-finance application, and the one this book points to, is **counts of patents** in Leah's innovation work: how many patents a firm files in a year is a non-negative integer with no natural upper bound, clustering around a firm-specific average, which is exactly the Poisson's territory. The same shape fits counts of trades in an interval, defaults in a portfolio per quarter, or fraud events per month.

Two relationships locate the Poisson in the family. First, it is the **limit of the Binomial** when $n$ is large and $p$ is small with $np = \lambda$ held fixed — many trials, each rarely a success, so you stop tracking the (huge) number of trials and track only the (modest) average count. That is why "rare events among many opportunities" is Poisson's home. Second, the mean-equals-variance property is also its sharpest *failure mode*: real count data, especially patents, are usually **over-dispersed** — their variance exceeds their mean, because firms differ systematically in ways a single $\lambda$ cannot capture. When you see variance far above the mean in count data, that is the Poisson assumption breaking, and it is the signal to reach for a richer count model (negative binomial), a topic the later weeks flag rather than fully develop.

---

## The family tree, in one breath

Hold the whole reference as a set of links rather than seven separate facts. Sum or average *anything* with finite variance and the **CLT** delivers the **Normal** (Ch 1.4). Take a **Normal** statistic but estimate its scale and you get the **Student's $t$**, which relaxes back to the Normal as degrees of freedom grow. Square and add independent standard **Normals** and you get the **chi-squared**; take a ratio of two scaled **chi-squareds** and you get the **$F$**, which collapses to a chi-squared as its denominator degrees of freedom grow and equals $t^2$ when the numerator has one degree of freedom. On the discrete side, a single yes/no is **Bernoulli**, a sum of $n$ of them is **Binomial**, the Binomial goes **Normal** for large $n$ (CLT again) and goes **Poisson** in the rare-event limit. Five continuous distributions and two discrete ones, all reachable from one another by summing, squaring, taking ratios, or taking limits — which is exactly why you can stop memorizing densities and start reconstructing the whole family from the relationships.
