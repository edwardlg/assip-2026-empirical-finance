# Problem Set 2.4 — Robust, Clustered, and HAC Standard Errors

*Covers Ch 2.4. Methods allowed: everything through Ch 2.4 — the classical variance formula $\hat\sigma^2(\mathbf{X}'\mathbf{X})^{-1}$, the full sandwich $(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\boldsymbol\Omega\mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}$, the White/HC estimator and its HC0–HC3 flavors, the cluster-robust sandwich and the Moulton-style inflation factor $1+(n-1)\rho_x\rho_\varepsilon$, the few-clusters caveat, HAC / Newey–West, and the Petersen (2009) panel taxonomy. You may treat $\hat\beta$ as already computed — every problem here is about its standard error, never about the estimate itself. Show your reasoning; a boxed number with no argument earns no credit.*

**Total: 100 points.** Six problems, escalating. Problem 1 is conceptual (why heteroskedasticity hits the SE but not the unbiasedness of $\hat\beta$); Problems 2–3 are pencil-and-paper sandwich arithmetic (classical vs robust; HC0–HC3); Problem 4 is the clustering / Moulton calculation; Problem 5 is HAC / serial correlation; Problem 6 is a Petersen-style "which clustering dimension?" decision problem on a panel.

A reminder on the one idea that runs through every problem, because it is the whole chapter. OLS hands you two separate things: a point estimate $\hat\beta$ and a claim about how much to trust it (its standard error). The first comes from $\hat{\boldsymbol\beta}=\boldsymbol\beta+(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\boldsymbol\varepsilon$ and is unbiased whenever $\mathbb{E}[\boldsymbol\varepsilon\mid\mathbf{X}]=\mathbf{0}$, regardless of what the errors' variances and covariances look like. The second comes from $\operatorname{Var}(\hat{\boldsymbol\beta}\mid\mathbf{X})=(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\boldsymbol\Omega\mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}$ and depends entirely on the shape of $\boldsymbol\Omega=\operatorname{Var}(\boldsymbol\varepsilon\mid\mathbf{X})$. When a problem asks "which standard error?", it is asking you to describe $\boldsymbol\Omega$ — diagonal-and-constant, diagonal-but-varying, block-diagonal, or banded — and then read the right filling for the sandwich off that description. The estimate never moves; only the filling changes.

---

## Problem 1 — Why $\boldsymbol\Omega$ breaks the SE but not $\hat\beta$ (12 points)

Maya regresses the interest rate on a pool of installment loans on a ZIP-code-tier indicator plus controls, and gets $\hat\beta_1=0.42$ with a classical standard error of $0.07$ (t = 6.0). Her mentor warns that the errors are almost certainly heteroskedastic — bigger loans have far less predictable rates than tiny ones — and possibly correlated within lender. Maya panics that her whole result, the $0.42$, is now suspect.

**(a) (4 pts)** Start from the identity $\hat{\boldsymbol\beta}=\boldsymbol\beta+(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\boldsymbol\varepsilon$ from the chapter. Take the conditional expectation of both sides given $\mathbf{X}$, and use it to argue that $\hat{\boldsymbol\beta}$ is unbiased. Which assumption did you need — and, crucially, did you anywhere have to assume anything about $\operatorname{Var}(\boldsymbol\varepsilon\mid\mathbf{X})=\boldsymbol\Omega$?

**(b) (4 pts)** Now write down the general sandwich formula for $\operatorname{Var}(\hat{\boldsymbol\beta}\mid\mathbf{X})$ and circle (in words) the one piece of it that changes when $\boldsymbol\Omega$ stops being $\sigma^2\mathbf{I}$. Explain in one or two sentences why this means heteroskedasticity contaminates the standard error while leaving the estimate alone.

**(c) (2 pts)** Reassure Maya in one sentence: is her $\hat\beta_1=0.42$ biased by the heteroskedasticity? What exactly is the thing that is wrong?

**(d) (2 pts)** Maya's classmate says, "If $\hat\beta$ is still unbiased, then who cares about the standard error — the estimate is right." Give the one-sentence rebuttal that names the practical thing she loses if she trusts the $0.07$.

---

## Problem 2 — The sandwich by hand: classical vs robust (18 points)

Work the smallest case that still shows the mechanism: a single regressor through the origin, $y_i=\beta x_i+\varepsilon_i$, so that $\mathbf{X}'\mathbf{X}=\sum_i x_i^2$ is just a number and the heteroskedasticity-robust variance reduces to the scalar formula from §2.1 of the chapter,
$$
\widehat{\operatorname{Var}}(\hat\beta)_{\text{HC0}}=\frac{\sum_i x_i^2\,\hat\varepsilon_i^2}{\left(\sum_i x_i^2\right)^2},
\qquad
\widehat{\operatorname{Var}}(\hat\beta)_{\text{classical}}=\frac{\hat\sigma^2}{\sum_i x_i^2},
\quad \hat\sigma^2=\frac{1}{N-K}\sum_i\hat\varepsilon_i^2 .
$$
Priya has $N=5$ wildfire claims with regressor (insured value, in \$M) and residuals already computed for you ($K=1$):

| $i$ | $x_i$ | $\hat\varepsilon_i$ |
|-----|-------|---------------------|
| 1 | 1 | $+1$ |
| 2 | 2 | $-2$ |
| 3 | 3 | $+1$ |
| 4 | 4 | $-4$ |
| 5 | 5 | $+5$ |

**(a) (3 pts)** Compute $\sum_i x_i^2$ and $\sum_i \hat\varepsilon_i^2$.

**(b) (4 pts)** Compute the **classical** variance and standard error of $\hat\beta$. (Use $\hat\sigma^2=\frac{1}{N-K}\sum_i\hat\varepsilon_i^2$ with $N-K=4$.)

**(c) (5 pts)** Compute the **HC0 robust** variance and standard error of $\hat\beta$ by evaluating $\sum_i x_i^2\,\hat\varepsilon_i^2$ in the numerator. Show the per-observation terms.

**(d) (3 pts)** Report the ratio robust-SE / classical-SE. Which is larger, and what feature of the data (look at how $\hat\varepsilon_i^2$ lines up with $x_i$) makes it so?

**(e) (3 pts)** In one or two sentences: if the residuals had instead been *constant in magnitude* across all $x_i$ (say all $\hat\varepsilon_i^2=9$), what would the ratio in (d) become, and why? You do not need to redo the full arithmetic — argue it.

---

## Problem 3 — HC0, HC1, HC2, HC3: which correction, and when (16 points)

The four robust flavors differ only in how each squared residual is inflated before it goes into the middle of the sandwich:
$$
\text{HC0: } \hat\varepsilon_i^2,\quad
\text{HC1: } \tfrac{N}{N-K}\hat\varepsilon_i^2,\quad
\text{HC2: } \tfrac{\hat\varepsilon_i^2}{1-h_{ii}},\quad
\text{HC3: } \tfrac{\hat\varepsilon_i^2}{(1-h_{ii})^2},
$$
where $h_{ii}$ is the leverage (the $i$-th diagonal of the hat matrix).

**(a) (3 pts)** Priya has $N=60$ observations and $K=4$ regressors. Compute the HC1 inflation factor $N/(N-K)$ and state what kind of error it corrects (and what it ignores).

**(b) (5 pts)** A single high-leverage point — Priya's one \$5M estate among \$200K cabins — has leverage $h_{ii}=0.5$. For *that observation*, compute the multiplier that HC0, HC2, and HC3 apply to its $\hat\varepsilon_i^2$. (HC0's multiplier is 1 by definition.) Rank the three by how aggressively they inflate this point's contribution.

**(c) (4 pts)** Explain *why* OLS residuals are systematically too small, and why that makes raw HC0 standard errors too small in finite samples. Then explain why the leverage correction in HC2/HC3 targets exactly the points that are shrunk the most by fitting.

**(d) (4 pts)** Give the practical decision rule: for $N=9{,}000$ loans with no extreme leverage, do the four flavors matter? For $N=25$ observations with one big outlier in $\mathbf{X}$, which flavor should you default to, and why is it the "safe" pick?

---

## Problem 4 — Clustering and the Moulton factor (20 points)

Maya's pool of $N=9{,}000$ loans is split into $G=45$ lenders ("clusters") of equal size $n=N/G=200$. Within a lender, errors share a common pricing shock, and her key regressor (the tier indicator) is also correlated within lender. The chapter's special-case Moulton result says the *true* variance of $\hat\beta_1$ exceeds the naive (non-clustered) variance by approximately
$$
\text{true Var} \approx \text{naive Var}\times\big[\,1+(n-1)\,\rho_x\,\rho_\varepsilon\,\big].
$$

**(a) (3 pts)** Explain in two or three sentences *why* ignoring within-cluster correlation makes the naive standard error too small — i.e., why $9{,}000$ correlated loans are not $9{,}000$ independent pieces of evidence. Use the "polling one household nine times" framing or your own.

**(b) (5 pts)** Take $\rho_x=\rho_\varepsilon=0.20$ and $n=200$. Compute the bracketed inflation factor. By what factor does the *true standard error* exceed the naive one? If Maya's naive t-stat is 6.0, what is her honest (clustered) t-stat, approximately?

**(c) (4 pts)** Maya wants to halve the gap between her naive and honest standard errors. Her advisor offers two options: (i) collect 9,000 *more* loans from the *same* 45 lenders, or (ii) add 45 *new* lenders. Using the structure of the inflation factor, explain which one actually buys her statistical evidence and why the other essentially does not.

**(d) (4 pts)** Write the cluster-robust sandwich estimator (the middle summed over clusters $g=1,\dots,G$) and explain, by comparing it to White's HC0 middle $\sum_i\hat\varepsilon_i^2\,\mathbf{x}_i\mathbf{x}_i'$, what term the cluster version keeps that White's throws away. One sentence on the slogan "White SEs are cluster SEs with clusters of size one."

**(e) (4 pts)** Now suppose Maya instead clusters by **state**, and she operates in only $G=9$ states. Why should she be nervous about the resulting t-statistics even though clustering "more broadly" sounds safer? Name one concrete fix from the chapter.

---

## Problem 5 — HAC / Newey–West and serial correlation (16 points)

Sam regresses his strategy's monthly return on a market-timing signal over $T=120$ months and reports classical standard errors. His residuals are positively autocorrelated: each month's residual is about $0.4$-correlated with the previous month's, fading with the gap.

**(a) (4 pts)** Describe what $\boldsymbol\Omega$ looks like in Sam's case — diagonal, block-diagonal, or banded? Where are the nonzero entries, and what happens to them as the time gap $\ell$ grows? Contrast this with the clustering case in Problem 4.

**(b) (4 pts)** Is Sam's reported classical t-statistic likely too big or too small? Argue it through the "effective sample size" intuition: with positive autocorrelation, how does the number of genuinely independent monthly draws compare to 120, and how does that bias the standard error?

**(c) (4 pts)** Which standard-error flavor should Sam switch to, and what is the one knob (and its name) he must set? Using the Newey–West rule of thumb $L\approx 4(T/100)^{2/9}$ with $T=120$, compute a starting bandwidth (round to the nearest integer). Briefly: what goes wrong if he sets $L$ too small? Too large?

**(d) (4 pts)** Sam's colleague trades a high-frequency strategy whose residuals show *negative* autocorrelation (bid–ask bounce). For that colleague, are naive t-stats too big or too small, and why? State the general principle linking the *sign* of the autocorrelation to the direction of the naive SE's error.

---

## Problem 6 — Petersen (2009): which clustering dimension? (18 points)

Maya assembles a **panel**: many firms $i$ observed over many years $t$, and regresses a default outcome on a leverage measure. The coefficient is identical in every column below; only the SE flavor changes. She runs Petersen's own diagnostic — cluster one way, then the other, and watch which moves the SE more.

| SE flavor | Std. error | t-stat |
|-----------|-----------|--------|
| Classical (OLS) | 0.018 | 5.0 |
| White (HC1) | 0.021 | 4.3 |
| Clustered by **firm** | 0.044 | 2.0 |
| Clustered by **time** | 0.024 | 3.8 |
| Two-way (firm + time) | 0.046 | 1.96 |

**(a) (4 pts)** Reading the table with Petersen's diagnostic: clustering by firm roughly *doubles* the White SE while clustering by time barely moves it. Which effect dominates Maya's panel — a persistent firm effect, a common time effect, or both? What is the correct clustering choice, and what does that choice assert about where the off-diagonal blocks of $\boldsymbol\Omega$ live?

**(b) (3 pts)** Why do White (HC1) standard errors fail to fix Maya's problem here? Be specific about what White SEs assume about the off-diagonals of $\boldsymbol\Omega$.

**(c) (4 pts)** Suppose a different outcome on the *same* dataset produced firm-clustered SE $\approx$ White SE but time-clustered SE roughly double the White SE. What would that pattern imply, and which clustering would you choose? This is the point that "the right clustering depends on the left-hand-side variable, not just the dataset" — restate it in your own words.

**(d) (4 pts)** A classmate says: "I already put **firm fixed effects** in the regression, so I don't need to cluster by firm — the fixed effects took care of the firm." Explain why this is wrong by distinguishing the two jobs (what a firm fixed effect removes vs. what clustering by firm handles). Can you want both at once?

**(e) (3 pts)** Sketch the mechanical recipe for the **two-way** (firm + time) clustered variance in terms of three sandwiches you already know how to build. Why is one of them *subtracted*?

---

*End of PS 2.4. Solutions in `book/appendices/E-solutions-manual/E-w2-ps2.4-solutions.md`. This set looks ahead to Weeks 3–4, where fixed effects and panel methods are developed in full, and to Ch 5.4, the complete reader's guide to Petersen (2009).*
