# Solutions — Problem Set 2.4 (Robust, Clustered, and HAC Standard Errors)

*Full worked solutions to `book/weeks/week-02/ps2.4.md`. Notation follows CONVENTIONS §3 and Ch 2.4: the OLS estimator is $\hat{\boldsymbol\beta}=(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$ with sampling-error identity $\hat{\boldsymbol\beta}=\boldsymbol\beta+(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\boldsymbol\varepsilon$; the error variance–covariance matrix is $\boldsymbol\Omega=\operatorname{Var}(\boldsymbol\varepsilon\mid\mathbf{X})$; the general variance is the sandwich $(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\boldsymbol\Omega\mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}$; $h_{ii}$ is the leverage (diagonal of the hat matrix $\mathbf{H}=\mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'$). Citations: Petersen, M. A. (2009). Estimating Standard Errors in Finance Panel Data Sets: Comparing Approaches. Review of Financial Studies, 22(1), 435–480. White (1980) and Newey & West (1987) referenced by name.*

---

## Problem 1 — Why $\boldsymbol\Omega$ breaks the SE but not $\hat\beta$ (12 pts)

**(a) (4 pts)** Take conditional expectations of the identity given $\mathbf{X}$:
$$
\mathbb{E}[\hat{\boldsymbol\beta}\mid\mathbf{X}]
=\boldsymbol\beta+(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\,\mathbb{E}[\boldsymbol\varepsilon\mid\mathbf{X}].
$$
If $\mathbb{E}[\boldsymbol\varepsilon\mid\mathbf{X}]=\mathbf{0}$ (exogeneity — the errors have mean zero given the regressors), the entire second term vanishes and $\mathbb{E}[\hat{\boldsymbol\beta}\mid\mathbf{X}]=\boldsymbol\beta$: unbiased. The only assumption used was **mean independence of the errors**, $\mathbb{E}[\boldsymbol\varepsilon\mid\mathbf{X}]=\mathbf{0}$. **Nowhere** did we touch $\operatorname{Var}(\boldsymbol\varepsilon\mid\mathbf{X})=\boldsymbol\Omega$ — unbiasedness is a statement about the *mean* of the errors, and $\boldsymbol\Omega$ is a statement about their *spread and co-movement*, a completely separate object.

**(b) (4 pts)** The general sandwich is
$$
\operatorname{Var}(\hat{\boldsymbol\beta}\mid\mathbf{X})
=(\mathbf{X}'\mathbf{X})^{-1}\,\mathbf{X}'\boldsymbol\Omega\mathbf{X}\,(\mathbf{X}'\mathbf{X})^{-1}.
$$
The piece that changes is the **filling, $\mathbf{X}'\boldsymbol\Omega\mathbf{X}$** (the "meat" of the sandwich); the two bread factors $(\mathbf{X}'\mathbf{X})^{-1}$ depend only on the regressors and are untouched. Heteroskedasticity replaces the constant-$\sigma^2$ diagonal of $\boldsymbol\Omega$ with varying $\sigma_i^2$, which changes the filling and hence the variance — but the variance is a property of the *distribution* of $\hat{\boldsymbol\beta}$, not of its center, so the center ($\boldsymbol\beta$) is left exactly where part (a) put it.

**(c) (2 pts)** No — $\hat\beta_1=0.42$ is **not biased** by the heteroskedasticity; it is still centered on the true effect. The thing that is wrong is the reported **standard error** $0.07$, which was computed from the classical formula $\hat\sigma^2(\mathbf{X}'\mathbf{X})^{-1}$ that silently assumed $\boldsymbol\Omega=\sigma^2\mathbf{I}$.

**(d) (2 pts)** If she trusts the $0.07$ she loses the ability to say *how confident* to be: every t-statistic, p-value, and confidence interval she builds on top of it is wrong, so she may declare "significant" a result that an honest SE would call a coin-flip — being right about the point but wrong about the uncertainty is exactly how overconfident findings get published and then retracted.

---

## Problem 2 — The sandwich by hand: classical vs robust (18 pts)

Data: $x=(1,2,3,4,5)$, $\hat\varepsilon=(+1,-2,+1,-4,+5)$, $N=5$, $K=1$.

**(a) (3 pts)**
$$
\sum_i x_i^2 = 1+4+9+16+25 = 55,\qquad
\sum_i \hat\varepsilon_i^2 = 1+4+1+16+25 = 47.
$$

**(b) (4 pts)** $\hat\sigma^2=\frac{1}{N-K}\sum_i\hat\varepsilon_i^2=\frac{47}{4}=11.75$. Then
$$
\widehat{\operatorname{Var}}(\hat\beta)_{\text{classical}}=\frac{\hat\sigma^2}{\sum_i x_i^2}=\frac{11.75}{55}=0.2136,
\qquad
\text{SE}_{\text{classical}}=\sqrt{0.2136}=\boxed{0.462}.
$$

**(c) (5 pts)** Build the numerator $\sum_i x_i^2\,\hat\varepsilon_i^2$ term by term:

| $i$ | $x_i^2$ | $\hat\varepsilon_i^2$ | $x_i^2\hat\varepsilon_i^2$ |
|-----|---------|-----------------------|----------------------------|
| 1 | 1 | 1 | 1 |
| 2 | 4 | 4 | 16 |
| 3 | 9 | 1 | 9 |
| 4 | 16 | 16 | 256 |
| 5 | 25 | 25 | 625 |
| **Σ** | | | **907** |

So
$$
\widehat{\operatorname{Var}}(\hat\beta)_{\text{HC0}}=\frac{907}{55^2}=\frac{907}{3025}=0.2998,
\qquad
\text{SE}_{\text{HC0}}=\sqrt{0.2998}=\boxed{0.548}.
$$

**(d) (3 pts)** Ratio $=0.548/0.462=\boxed{1.18}$. The **robust SE is larger.** Look at the table in (c): the biggest squared residuals ($\hat\varepsilon_4^2=16$, $\hat\varepsilon_5^2=25$) sit at the **high-$x$, high-leverage** observations, and the robust numerator multiplies each $\hat\varepsilon_i^2$ by $x_i^2$, so those points dominate. The classical formula instead spreads one average $\hat\sigma^2$ evenly and so undercounts the uncertainty contributed by exactly the points that matter most. Robust SEs catch the positive alignment of $\hat\varepsilon_i^2$ with $x_i^2$ (textbook heteroskedasticity) that classical SEs ignore.

**(e) (3 pts)** If every $\hat\varepsilon_i^2$ were the same constant $c$ (here $c=9$), the robust numerator becomes $\sum_i x_i^2\cdot c=c\sum_i x_i^2$, so $\text{Var}_{\text{HC0}}=c\sum x_i^2/(\sum x_i^2)^2=c/\sum x_i^2$, while $\text{Var}_{\text{classical}}=\frac{Nc}{N-K}\big/\sum x_i^2$. The two now differ *only* by the degrees-of-freedom factor $N/(N-K)=5/4$: the HC0 SE is a touch **smaller** (ratio $\sqrt{(N-K)/N}=\sqrt{4/5}\approx 0.89$), and **HC1** — which multiplies HC0 by exactly $N/(N-K)$ — would match the classical SE on the nose. The point: under genuine homoskedasticity the robust and classical answers converge, so robust SEs cost essentially nothing; the gap in (d) appeared *only* because the residuals were not constant.

---

## Problem 3 — HC0, HC1, HC2, HC3: which correction, and when (16 pts)

**(a) (3 pts)** $N=60$, $K=4$: $\dfrac{N}{N-K}=\dfrac{60}{56}=\boxed{1.071}$. It is a **flat degrees-of-freedom inflation** applied equally to every observation, correcting (crudely) for the fact that residuals are too small after fitting. It **ignores leverage** — it does not know that high-leverage points have their residuals shrunk more than others, so it under-inflates exactly those points.

**(b) (5 pts)** With $h_{ii}=0.5$, the multipliers on that observation's $\hat\varepsilon_i^2$ are:
$$
\text{HC0: } 1,\qquad
\text{HC2: } \frac{1}{1-h_{ii}}=\frac{1}{0.5}=2,\qquad
\text{HC3: } \frac{1}{(1-h_{ii})^2}=\frac{1}{0.25}=4.
$$
Ranking by aggressiveness: $\text{HC3 }(4)>\text{HC2 }(2)>\text{HC0 }(1)$. HC3 inflates this leveraged point's contribution four-fold; HC0 not at all.

**(c) (4 pts)** OLS chooses $\hat{\boldsymbol\beta}$ to *minimize* $\sum_i\hat\varepsilon_i^2$, which bends the fitted line toward each data point; the line is partly chasing the very noise it is supposed to leave in the residual, so $\hat\varepsilon_i$ is on average **smaller in magnitude than the true $\varepsilon_i$.** Feeding too-small squared residuals into the sandwich makes HC0 standard errors too small — overconfident — in finite samples. The shrinkage is *worst* at high-leverage points (a point that pulls the line hardest toward itself has the most-shrunk residual), and the leverage factor $1-h_{ii}$ is precisely the amount of that shrinkage: dividing by $1-h_{ii}$ (HC2) or $(1-h_{ii})^2$ (HC3) undoes it observation-by-observation, restoring most weight to exactly the points the fitting deflated most.

**(d) (4 pts)** For $N=9{,}000$ loans with no extreme leverage, the four flavors are **practically identical** (they agree to several decimals — the corrections all $\to 1$ as $N$ grows and leverage stays low), so it does not matter; report HC1. For $N=25$ with one big $\mathbf{X}$-outlier, the flavors **diverge**, and you should default to **HC3**: it inflates the high-leverage point's residual the most via the $(1-h_{ii})^2$ denominator, it is **never badly anti-conservative**, and so it is the safe pick that keeps you honest when a single point could otherwise drive a spuriously tight SE.

---

## Problem 4 — Clustering and the Moulton factor (20 pts)

**(a) (3 pts)** Within a lender, the loans share a common pricing shock, so their errors are *positively correlated*: once you know one loan's error you can partly predict its neighbors'. That means each additional loan from the same lender carries **less than one observation's worth of fresh information** — it largely repeats the lender's story. The naive formula treats all $9{,}000$ as independent and so divides the error variance by too large an effective $N$, reporting a standard error that is too small. It is exactly like polling one household nine times and claiming a sample of nine: the nominal count overstates the real evidence.

**(b) (5 pts)** With $\rho_x=\rho_\varepsilon=0.20$ and $n=200$:
$$
1+(n-1)\rho_x\rho_\varepsilon = 1+199\times(0.20)(0.20)=1+199\times 0.04 = 1+7.96 = \boxed{8.96}.
$$
The true variance is $\approx 8.96\times$ the naive variance, so the true SE is $\sqrt{8.96}\approx \boxed{2.99}$ times the naive one. A naive t-stat of $6.0$ becomes an honest t-stat of $\approx 6.0/2.99\approx\boxed{2.0}$ — still significant, but the megaphone has become a speaking voice.

**(c) (4 pts)** The inflation factor is $1+(n-1)\rho_x\rho_\varepsilon$, driven by **cluster size $n$**, not by the total $N$. Option (i) — 9,000 more loans from the *same* 45 lenders — *increases $n$* (each lender now has $\sim 400$ loans), which makes the bracket **larger**, not smaller: more within-cluster repetition, no new independent evidence. Option (ii) — 45 new lenders — *increases the number of clusters $G$* while holding $n$ fixed; the cluster-robust estimator's precision lives in $G$, so new clusters are what actually buy evidence. Choose **(ii)**. The slogan: pouring observations into existing clusters does not deliver the independence the naive formula assumes; more clusters does.

**(d) (4 pts)** The cluster-robust sandwich keeps the bread and rebuilds the filling cluster-by-cluster:
$$
\widehat{\operatorname{Var}}(\hat{\boldsymbol\beta})_{\text{cluster}}
=(\mathbf{X}'\mathbf{X})^{-1}\left(\sum_{g=1}^{G}\mathbf{X}_g'\hat{\boldsymbol\varepsilon}_g\,\hat{\boldsymbol\varepsilon}_g'\mathbf{X}_g\right)(\mathbf{X}'\mathbf{X})^{-1}.
$$
White's HC0 middle is $\sum_i \hat\varepsilon_i^2\,\mathbf{x}_i\mathbf{x}_i'$ — a sum over single observations that keeps only the *diagonal* products $\hat\varepsilon_i^2$. The cluster version's outer product $\hat{\boldsymbol\varepsilon}_g\hat{\boldsymbol\varepsilon}_g'$ keeps the **within-cluster cross-products $\hat\varepsilon_i\hat\varepsilon_j$** for loans $i,j$ in the same lender — exactly the off-diagonal covariances White's version discards. Hence "White SEs are cluster SEs with clusters of size one": when each cluster is a single observation there are no cross-products and the two formulas coincide.

**(e) (4 pts)** Clustering by state gives only $G=9$ clusters, and the cluster-robust estimator is consistent as $G\to\infty$, **not** as $N\to\infty$. With so few clusters the estimator is itself noisy and **biased downward** — overconfident, the very disease being treated — so the normal-approximation t-test is untrustworthy. The rule of thumb is to want $\gtrsim 30$–$50$ clusters. One concrete fix: use the **wild cluster bootstrap** (Cameron, Gelbach & Miller 2008, *Review of Economics and Statistics*, 90(3), 414–427) which resamples whole clusters; alternatively, use a $t$-distribution with $G-1=8$ degrees of freedom rather than the normal.

---

## Problem 5 — HAC / Newey–West and serial correlation (16 pts)

**(a) (4 pts)** $\boldsymbol\Omega$ is **banded**: nonzero entries along and *near* the diagonal, fading to zero away from it. The diagonal holds each period's variance; the first off-diagonals hold the large $\operatorname{Cov}(\varepsilon_t,\varepsilon_{t-1})$, and as the lag $\ell$ grows the covariance $\operatorname{Cov}(\varepsilon_t,\varepsilon_{t-\ell})$ shrinks toward zero (e.g. $\operatorname{Cov}(\varepsilon_t,\varepsilon_{t-12})\approx 0$). This differs from clustering: clustering gives **block-diagonal** $\boldsymbol\Omega$ with dense blocks and clean group boundaries (correlation is all-or-nothing — full within a lender, zero across), whereas serial correlation gives a *smear* around the diagonal with no groups, the correlation decaying continuously with distance.

**(b) (4 pts)** **Too big.** Positive autocorrelation means each month's residual partly echoes the previous month's, so the $120$ months contain fewer than $120$ genuinely independent draws — the *effective* sample size is well below $120$. The naive classical formula divides by the wrong (too large) effective $T$, producing a standard error that is too small and therefore a t-statistic that is too big.

**(c) (4 pts)** Switch to **HAC / Newey–West** standard errors. The one knob is the **bandwidth** $L$ — the number of lags whose residual cross-products enter the middle of the sandwich (with declining Bartlett weights $w_\ell=1-\ell/(L+1)$). The rule of thumb:
$$
L\approx 4\left(\frac{T}{100}\right)^{2/9}=4\left(\frac{120}{100}\right)^{2/9}=4(1.2)^{0.2222}\approx 4.17 \;\Rightarrow\; \boxed{L=4}.
$$
Too small a bandwidth misses real persistence (it stops counting lagged correlation that is genuinely there, so the SE stays too small); too large adds noisy, near-zero lag terms that inflate the variance of the variance estimate, making the SE itself unstable.

**(d) (4 pts)** For the high-frequency colleague with *negative* autocorrelation, naive t-stats are **too small** (too conservative). The general principle: the sign of the autocorrelation determines the direction of the naive SE's error. **Positive** autocorrelation (the usual finance case — shocks persist) shrinks the effective sample and makes naive SEs too small / t-stats too big; **negative** autocorrelation (e.g. bid–ask bounce, where an up-tick tends to be followed by a down-tick) does the reverse, making naive SEs too large / t-stats too small. HAC gets either case right because it *estimates* the actual band of off-diagonal covariances rather than assuming the band is empty.

---

## Problem 6 — Petersen (2009): which clustering dimension? (18 pts)

**(a) (4 pts)** A **persistent firm effect dominates.** Petersen's diagnostic: whichever clustering moves the SE *more* away from the White number points at the bigger source of correlation. Here firm-clustering moves the SE from $0.021$ to $0.044$ (roughly doubling) while time-clustering barely moves it ($0.021\to 0.024$) — so the residuals are correlated **across time within a firm** (a firm mispriced this year tends to be mispriced next year) far more than across firms within a year. The correct choice is **clustering by firm**, which asserts that $\boldsymbol\Omega$'s off-diagonal blocks are organized **by firm**: one dense block per firm spanning all its years, zeros across firms.

**(b) (3 pts)** White (HC1) SEs assume the **off-diagonals of $\boldsymbol\Omega$ are zero** — errors uncorrelated across observations — and only ever look at one observation's own squared residual. They correct for heteroskedasticity (the *diagonal*) but are completely blind to the within-firm correlation across years (the *off-diagonal blocks*). That is why White's $0.021$ is barely above classical's $0.018$ and far below the honest firm-clustered $0.044$.

**(c) (4 pts)** That opposite pattern — firm-clustered $\approx$ White but time-clustered roughly double — would imply a **common time effect dominates**: a market-wide shock in each period hits all firms' residuals together (correlation *across firms within a period*), with little persistence within a firm. You would **cluster by time** (or absorb it with time fixed effects and cluster on any residual common shock). The lesson restated: the correlation structure of the *residuals* — hence the right clustering — depends on what you put on the **left-hand side**, because different outcomes carry different shocks; the same panel of firms and years can demand firm-clustering for one regression and time-clustering for another. Clustering is an economic judgment about $\boldsymbol\Omega$, not a software default.

**(d) (4 pts)** They do **different jobs**. A firm **fixed effect** (a dummy per firm, the demeaning of Ch 2.3) removes the firm's *average level* — the permanent, time-invariant part of the firm's outcome. **Clustering by firm** handles *correlation in the leftover residuals over time* — the co-movement that remains after the mean is removed, which a fixed effect cannot touch because it is about the mean, not the covariance. So "I have firm FEs, so I don't need to cluster by firm" conflates a mean with a covariance and leaves you overconfident. **Yes — you typically want both at once:** firm fixed effects to absorb permanent firm differences *and* clustering by firm to honor the within-firm residual correlation that survives the demeaning.

**(e) (3 pts)** Two-way (firm + time) clustered variance is built from three sandwiches you already know:
$$
\widehat{\operatorname{Var}}_{\text{two-way}}
=\widehat{\operatorname{Var}}_{\text{cluster by firm}}
+\widehat{\operatorname{Var}}_{\text{cluster by time}}
-\widehat{\operatorname{Var}}_{\text{White (heterosk.-only)}}.
$$
The White (single-observation) sandwich is **subtracted** because each observation's own variance is counted *twice* — once inside its firm block and once inside its time block — so the overlap (the pure diagonal, captured by White) must be removed once to avoid **double-counting** (Cameron, Gelbach & Miller 2011, *Journal of Business & Economic Statistics*, 29(2), 238–249).

---

*End of solutions for PS 2.4. Cross-references: Ch 2.4 (sandwich, White/HC, HC0–HC3, clustering, Moulton factor, HAC/Newey–West, Petersen taxonomy), Ch 2.1 (hat matrix and leverage $h_{ii}$), Ch 2.2 (classical variance and Gauss–Markov), Ch 2.3 (demeaning = fixed effects). Numeric keys: P2 classical SE 0.462, HC0 SE 0.548, ratio 1.18; P3 HC1 factor 1.071, HC2/HC3 multipliers 2 and 4 at $h=0.5$; P4 bracket 8.96, SE factor 2.99, honest t ≈ 2.0; P5 NW bandwidth $L=4$; P6 firm effect dominates → cluster by firm, two-way = firm + time − White. Looks ahead to Weeks 3–4 (panel/fixed-effects methods) and Ch 5.4 (full Petersen 2009 reader's guide).*
