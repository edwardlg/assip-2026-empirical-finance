# Solutions — PS 5.1 (Sorting, Double-Sorting, and the Fama–MacBeth Horse Race in Fama & French 1992)

**Problem set:** `book/weeks/week-05/ps5.1.md` (PS 5.1, Week 5).
**Chapter:** Ch 5.1 — Reader's Guide: *The Cross-Section of Expected Stock Returns* (Fama & French 1992).

These are full worked solutions, not just answers. Notation follows `CONVENTIONS.md` and locks to Ch 5.1: portfolio sorts and return *spreads*; the **Reader's-Guide anatomy** (Research question · Identification strategy · Data · Table-by-table reading order · What's clever · What's vulnerable · Three replication exercises); the Fama–MacBeth two-pass machine of Lab 2 with $\hat\gamma_j=\frac1T\sum_t\hat\gamma_{j,t}$ and FM standard error $\widehat{\operatorname{se}}(\hat\gamma_j)=\operatorname{sd}_t(\hat\gamma_{j,t})/\sqrt T$; the descriptive/predictive (not causal) reading; the Week-1 multiple-testing bound $P=1-(1-\alpha)^m$; the Week-2/3 errors-in-variables → attenuation result; and look-ahead/survivorship bias. **Every number here is illustrative and constructed** — Fama and French's actual table values are not reproduced. All return figures are percent per month unless annualized. Numerical results were confirmed in Python (spread arithmetic, the $t$-statistics, the multiple-testing probabilities, and the inverted FM-SE); verifying notes appear where useful. Cite the paper by name: **Fama & French (1992)**.

---

## Problem 1 — Why sort? Portfolios versus individual stocks (12 points)

**(a) (4 pts)** Write a single small stock's monthly return as a true mean plus idiosyncratic noise, $r_{it}=\mu_i+\varepsilon_{it}$, where $\varepsilon_{it}$ is the firm-specific shock (lawsuit, recall, earnings surprise) with some large variance $\sigma^2$. For one stock the signal $\mu_i$ is buried under $\sigma$. Now average $n$ such stocks into a portfolio. The portfolio return is $\bar r_t=\frac1n\sum_{i=1}^n r_{it}$, and if the idiosyncratic shocks are roughly independent across firms,
$$
\operatorname{Var}(\bar r_t)=\operatorname{Var}\!\Big(\tfrac1n\sum_i \varepsilon_{it}\Big)=\frac{1}{n^2}\sum_i \sigma^2=\frac{\sigma^2}{n}.
$$
Averaging $n$ roughly-independent pieces shrinks the idiosyncratic variance by about $1/n$, so the *standard deviation* of the portfolio's monthly return falls by about $1/\sqrt n$. With a few hundred stocks in a decile, the firm-specific churn that dominates any single name is averaged down by an order of magnitude, while the *common* part of the return — the part the sort is built to isolate — survives. That is exactly what lets a real premium **under one percent per month** poke above the noise: the signal stays put while the noise collapses as $\sigma/\sqrt n$. On a single stock that same sub-1% premium is invisible against monthly swings of tens of percent.

**(b) (4 pts)** The single pooled regression $\mathbb{E}[r_{it}]=\gamma_0+\gamma_1 x_i$ assumes the relationship is **linear** — every one-unit change in $x$ moves expected return by the same $\gamma_1$, everywhere along $x$. The decile sort assumes *almost nothing* about shape: it only assumes you can **rank** firms by $x$ and that the bucket means are informative. It lets the ten decile means trace out whatever curve the data want — flat in the middle and steep at one end, monotone, hump-shaped, anything. Concrete reveal: suppose the size premium lived almost entirely in the smallest decile — D1 at 1.62 %/mo with D2 through D10 nearly flat around 1.0. A linear regression would average that one extreme bucket against nine flat ones and report a modest, possibly insignificant $\hat\gamma_1$, *hiding* the fact that the action is a single corner of the distribution. The sort shows it at a glance: nine flat dots and one that jumps. Sorts let the data show their shape before any model is forced on them.

**(c) (4 pts)** The section is **§4, "Table-by-table reading order."** Its rule: read the **sort tables before the regression tables**, because the sorts "are the most honest thing in the paper — they assume almost nothing," so you can see the result (beta flat within size; value and size live) before a single coefficient or functional-form choice has been imposed. For Sam: leading with the kitchen-sink regression means the *first* thing he sees is filtered through a linear specification and the choice of which regressors to include — if that regression were misspecified or a variable mismeasured, he would have no model-free benchmark to catch it. Reading the sorts first gives him the nonparametric truth to which the regression must then conform; a regression that *disagreed* with a clean monotone sort would be the regression he distrusts, not the sort.

---

## Problem 2 — Read a univariate decile sort and lift the premium off it (16 points)

**(a) (5 pts)** **Size premium.** "Small" is the D1 end (smallest market equity), and small firms earn *more* in Fama & French (1992), so the premium is small minus big:
$$
\widehat{\text{size premium}} = \bar r_{\text{D1}} - \bar r_{\text{D10}} = 1.62 - 0.78 = \mathbf{0.84\ \%/\text{mo}} \approx 0.84\times 12 \approx \mathbf{10.1\ \%/\text{yr}}.
$$
The sign convention is small-minus-big because the live pattern is "smaller firms, higher returns," so we subtract the lower-return big-firm decile to get a positive premium.

**Value premium.** "Value" is the high-BE/ME end, B10, and value beats growth, so the premium is value minus growth:
$$
\widehat{\text{value premium}} = \bar r_{\text{B10}} - \bar r_{\text{B1}} = 1.95 - 0.72 = \mathbf{1.23\ \%/\text{mo}} \approx 1.23\times 12 \approx \mathbf{14.8\ \%/\text{yr}}.
$$
These are §4's **two live patterns**: average return *rises as you move toward small firms* (size), and average return *rises across BE/ME from growth to value* (book-to-market). (Annualizing by $\times 12$ is the crude simple-sum convention; it ignores compounding, but it is the right order-of-magnitude move for reading a sort.)

**(b) (4 pts)** Both columns are **strictly monotone**: the size column falls at every single step (1.62, 1.48, 1.39, …, 0.78 — each entry below the one before), and the BE/ME column rises at every single step (0.72, 0.86, …, 1.95). A referee trusts a smooth monotone gradient more than a sort where only the extreme bucket is unusual, because monotonicity is hard to fake by chance or by one outlier portfolio: it says the characteristic orders returns *all along its range*, not that one weird corner is dragging the spread. A single-bucket jump could be a handful of firms, a data error, or a small-sample fluke in one decile; ten dots marching in order is a pattern. The **BE/ME** sort shows the steeper *and* cleaner gradient: its endpoint spread (1.23) is larger than size's (0.84), and it climbs without hesitation — consistent with §5's remark that book-to-market "does enormous work, arguably more than size."

*Verify:* size steps are all negative; BE/ME steps all positive — confirmed both monotone in Python.

**(c) (4 pts)** The bias is **look-ahead bias**, one of §6's four vulnerabilities. Market equity is price $\times$ shares, and a firm's *contemporaneous* (this-month) market equity is built from this-month's price — but this-month's price is part of what produces this-month's *return*. A stock whose price just dropped is mechanically sorted into a *smaller*-size bucket *and* mechanically has a low return that month; a stock whose price just jumped is sorted larger and has a high return. Sorting on the within-month price thus aligns the bucket assignment with the very return being measured, manufacturing a "small firms earn more" spread that is pure mechanical contamination, not a premium any investor could have traded on (you cannot sort on a price you only learn at month's end). The §3 **July-to-June timing gap** prevents exactly this: it uses *lagged* size (formed before the return window) so the sorting variable is genuinely *knowable* before the returns it is asked to explain — the explanatory variable cannot peek at the outcome. That is why the honest lagged sort gives a modest 0.84 %/mo while the contaminated contemporaneous sort balloons.

**(d) (3 pts)** A spread between two portfolio means is a single realized difference; without a measure of how much it would bounce around in another sample, you cannot tell a real 0.84 %/mo premium from a draw that happened to land at 0.84 by luck. You need a **standard error** to form a $t$-statistic and ask whether the spread is distinguishable from zero. The object from Lab 2 / §2 that supplies the honest one, when the premium is re-estimated as a regression slope, is the **Fama–MacBeth standard error**, $\operatorname{sd}_t(\hat\gamma_{j,t})/\sqrt T$ — built from the month-to-month scatter of the cross-sectional slopes, which correctly accounts for the within-month correlation a naive pooled SE would ignore. (Problem 4 does the computing.)

---

## Problem 3 — The double sort: was beta's premium just size in disguise? (20 points)

**(a) (5 pts)** Naive **High-minus-Low beta spread**:
$$
1.33 - 1.01 = \mathbf{0.32\ \%/\text{mo}}.
$$
Taken at face value this *looks* like support for Sam's "riskier pays more" CAPM prior — higher beta, higher average return, a positive premium of about 0.32 %/mo (~3.9 %/yr). But look at the size-mix columns. As you move from the Low-beta bucket to the High-beta bucket, the bucket goes from **60% big / 10% small** to **10% big / 60% small**. So beta is not the only thing changing across the columns — **firm size is changing in lockstep**: the high-beta bucket is dominated by small firms, the low-beta bucket by big firms. The "beta premium" might be nothing but the size premium wearing a beta costume, because small firms (which earn more, per Problem 2) have piled into the high-beta column.

**(b) (7 pts)**

(i) Within-size **High-minus-Low beta spreads**, row by row:
$$
\text{Small: } 1.49-1.50 = -0.01,\qquad
\text{Mid: } 1.17-1.18 = -0.01,\qquad
\text{Big: } 0.86-0.84 = +0.02.
$$
Holding size roughly fixed, sorting on beta buys essentially **no spread** — the three numbers are within $\pm 0.02$ %/mo of zero, economically nothing and one of them the wrong sign. This is §4's phrase made literal: you **"watch beta die."** The flat within-size beta row is the headline of the entire paper, found in a table with no regression coefficient in it.

(ii) Within-beta **Small-minus-Big size spreads**, column by column:
$$
\text{Low beta: } 1.50-0.84 = +0.66,\qquad
\text{Mid beta: } 1.53-0.81 = +0.72,\qquad
\text{High beta: } 1.49-0.86 = +0.63.
$$
Holding beta roughly fixed, the size premium is **large and positive in every beta column** — about 0.6–0.7 %/mo of extra return for small over big, whichever beta group you look within. Size is a live pattern; beta is a dead one.

(iii) Reconciliation: the one-way beta sort showed $+0.32$ %/mo only because the high-beta bucket is **60% small firms** while the low-beta bucket is **60% big firms** (the size-mix columns). When you average each beta bucket's return, the high-beta average is pulled *up* by the small firms crowding it and the low-beta average is pulled *down* by the big firms crowding it — so the "beta spread" is really the *size* spread leaking in through the correlated size composition. The double sort breaks the tangle by comparing High vs. Low beta *within* a fixed size row, where the size mix is held constant, and there the spread vanishes. Beta's apparent premium was size in disguise.

*Verify (Python):* count-weighted marginal beta returns reproduce 1.01 / 1.19 / 1.33 (spread $+0.32$); within-size beta spreads $-0.01, -0.01, +0.02$; within-beta size spreads $+0.66, +0.72, +0.63$ — confirmed.

**(c) (5 pts)** The mapping to "controlling for a confounder": the **outcome** is average return; the **treatment-like variable** whose effect we want is **beta**; the **confounder** is **size**, which is correlated with beta (small firms are high-beta) and independently moves returns (small firms earn more). Forming size–beta cells achieves with buckets what a control achieves with a slope, because within a single size row every firm has roughly the same size, so size can no longer drive the within-row return differences — any remaining spread across the beta columns must be beta's own doing, exactly as adding `size` to a regression strips size's variation out before reading beta's coefficient. The one thing the bucket version buys that the linear control does not is that it is **nonparametric** (§2's word): it does not assume return is *linear* in beta or in size, nor that size's effect is the same at every beta level. The buckets let the data show their shape — including, here, the fact that beta's row is flat *everywhere*, not just on average — without imposing a functional form that could hide a nonlinearity.

**(d) (3 pts)** The legitimate kernel: coarse bins **average over heterogeneity inside each bin**, so a relationship that is flat across three broad groups could in principle be non-flat across, say, ten finer beta groups if the action lived between the bins. That is a real limit of any coarse sort. But the §5 reason it does not rescue beta here is the **flatness across the *whole* row**, not just the endpoints: every within-size beta spread is within $\pm 0.02$ %/mo of zero, and one is the wrong sign. For finer bins to manufacture a beta premium, the relationship would have to be flat at the coarse level yet strongly sloped at the fine level — a contrived, non-monotone pattern with no economic story. When the coarse spread is essentially *zero with a near-zero gradient*, "finer bins would rescue beta" is a strained hope, whereas if the coarse spread were merely *attenuated* (small but clearly positive) the objection would carry more force.

---

## Problem 4 — Read the Fama–MacBeth horse race (22 points)

**(a) (5 pts)** $t=\hat\gamma_j/\widehat{\operatorname{se}}(\hat\gamma_j)$:

| Spec | Regressor | $\hat\gamma_j$ | FM SE | $t$ |
|:----:|:---------:|:---:|:---:|:---:|
| **A** | $\beta$ | $+0.18$ | $0.14$ | $+0.18/0.14 = \mathbf{+1.3}$ |
| **B** | $\log\text{size}$ | $-0.15$ | $0.035$ | $-0.15/0.035 = \mathbf{-4.3}$ |
|       | $\log\text{BE/ME}$ | $+0.42$ | $0.085$ | $+0.42/0.085 = \mathbf{+4.9}$ |
| **C** | $\beta$ | $-0.02$ | $0.13$ | $-0.02/0.13 = \mathbf{-0.2}$ |
|       | $\log\text{size}$ | $-0.14$ | $0.036$ | $-0.14/0.036 = \mathbf{-3.9}$ |
|       | $\log\text{BE/ME}$ | $+0.40$ | $0.090$ | $+0.40/0.090 = \mathbf{+4.4}$ |

Against a conventional $|t|>2$ bar: in **spec A** beta does **not** clear it ($|t|=1.3$). In **spec B** both $\log\text{size}$ ($|t|=4.3$) and $\log\text{BE/ME}$ ($|t|=4.9$) clear it strongly. In **spec C** beta again **fails** ($|t|=0.2$), while $\log\text{size}$ ($|t|=3.9$) and $\log\text{BE/ME}$ ($|t|=4.4$) both keep clearing it easily.

**(b) (5 pts)** Scanning the **beta row** across A → C the way §4 instructs: beta's slope is a modest, already-insignificant $+0.18$ ($t=+1.3$) when run *alone* in spec A, and the moment $\log\text{size}$ and $\log\text{BE/ME}$ enter alongside it in spec C, the slope **collapses to $-0.02$** ($t=-0.2$) — near zero and even the wrong sign for CAPM. **Headline (one sentence):** size and book-to-market capture the cross-sectional variation in average returns, and market beta adds essentially nothing once they are controlled for — beta, the field's crown jewel, comes out flat. This is the finding precisely because it is an *absence*: under CAPM, beta's slope $\gamma_\beta$ is the number that *must* be large and positive (it is the whole theory), so when the number that should be big is the number that isn't, the missing premium *is* the result. The paper did not just add a variable; it executed the reigning one with the field's own preferred weapon.

**(c) (4 pts)** Yes — size and BE/ME **keep** their large, significant slopes from spec B to spec C: $\log\text{size}$ moves only from $-0.15$ to $-0.14$ ($|t|$ from 4.3 to 3.9) and $\log\text{BE/ME}$ only from $+0.42$ to $+0.40$ ($|t|$ from 4.9 to 4.4) when beta joins them. They survive together; beta does not. Signs in plain English: $\hat\gamma_{\log\text{size}}<0$ means **larger firms earn lower average returns** (equivalently, smaller firms earn more) — the size premium. $\hat\gamma_{\log\text{BE/ME}}>0$ means **higher book-to-market (value) firms earn higher average returns** than low-BE/ME (growth) firms — the value premium. These are the *same* two live patterns from the Problem 2 sorts: the negative size slope is the regression form of the downward-sloping size decile column (small > big), and the positive BE/ME slope is the regression form of the upward-sloping BE/ME decile column (value > growth). The regression quantifies, in one specification with the characteristics fighting each other, what the sorts showed nonparametrically.

**(d) (5 pts)**

(i) The FM standard error is honest because of the **within-month cross-sectional correlation** of Ch 2.4 — the "time effect." In any single month, every stock is shoved by the *same* market-wide shock, so the regression residuals within a month are violently correlated, not independent. A single pooled OLS over all $\sim$stock-months would treat each stock-month as an independent observation and so vastly overcount the effective sample size, reporting a standard error far too small (a falsely huge $t$). Fama–MacBeth never compares *across* months inside a regression: it collapses each month to *one* slope $\hat\gamma_{j,t}$, then treats the $T$ slopes as a small time series and takes their scatter, $\operatorname{sd}_t(\hat\gamma_{j,t})/\sqrt T$. The month-to-month bounce in the slopes *already embeds* the common shocks, so the SE built from that bounce is the honest one.

(ii) Invert the FM-SE formula. With $\widehat{\operatorname{se}}=\operatorname{sd}_t/\sqrt T$,
$$
\operatorname{sd}_t(\hat\gamma_{\log\text{BE/ME},t}) = \widehat{\operatorname{se}}\times\sqrt T = 0.090\times\sqrt{330} = 0.090\times 18.166 \approx \mathbf{1.63}.
$$
So the monthly BE/ME slope swings with a standard deviation of about 1.63 (in the same %/mo-per-log-unit units) month to month, while its *average* is a much tighter 0.40 — the $\sqrt{330}$ in the denominator is what turns a noisy monthly slope into a precisely-estimated average. *Verify:* $0.090\times18.166=1.635$, and a simulated slope series with sd $1.63$ over $T=330$ reproduces FM SE $\approx 0.090$ — confirmed.

**(e) (3 pts)** The section is **§4, "Table-by-table reading order,"** which says to read the regression columns "as a *sequence of horse races*, not as one table." Staging beta-alone → size-and-BE/ME-alone → all-three-together is more persuasive than reporting only the kitchen sink because it shows beta is weak *even when given its best shot alone* (spec A), shows size and BE/ME are strong *on their own* (spec B), and only then lets all three compete (spec C) — so the reader watches beta fail to survive the contest rather than having to trust a single multivariate number. The sequence rules out the rejoinder "beta only looks bad because you buried it among collinear regressors": it was already insignificant by itself.

---

## Problem 5 — Read like a referee: three named vulnerabilities (20 points)

**(a) (7 pts) Data-snooping / multiple testing (Week 1).**

(i) With $m=20$ independent worthless predictors each tested at $\alpha=0.05$:
$$
P(\text{at least one ``significant''}) = 1-(1-0.05)^{20} = 1-(0.95)^{20} = 1-0.3585 \approx \mathbf{0.64},
$$
and the expected number of false discoveries is $\alpha m = 0.05\times 20 = \mathbf{1.0}$. So even with *nothing real*, you have about a **64% chance** of finding at least one "significant" predictor and *expect one* to clear the bar by pure chance. *Verify:* $1-0.95^{20}=0.6415$ — confirmed.

(ii) A single reported Fama–MacBeth $t>2$ on BE/ME does not rule out that BE/ME is one such lucky winner because that $t$-statistic is computed *as if BE/ME were the only hypothesis ever tested* — it makes no adjustment for the hundreds of characteristics the *field* tried before landing on the survivors. A $t$ that would be impressive in isolation is unremarkable as the maximum over many silent tests. The §6 skeptical question that actually settles it: *would size and BE/ME survive in data the authors had never seen?* — because true effects replicate out-of-sample while chance winners of a single-sample lottery do not.

(iii) The out-of-sample evidence §6 names as kinder to BE/ME than to most factors is **international and post-publication / later-sample evidence** (the value premium showing up in other countries' markets and in data drawn after 1992). Surviving there is the right falsification test because that data was *not part of the search* that produced the original finding — a snooped chance correlation has no reason to reappear in a fresh sample, so re-appearance is genuine corroboration rather than the same coincidence re-counted.

**(b) (7 pts) Errors-in-variables in beta (Week 2 / Week 3).**

(i) The Week-2 result: a regressor measured with **random (classical) measurement error** suffers **attenuation bias** — its estimated slope is pulled *toward zero*. Beta is not observed; it is the Pass-1 *estimate* $\hat\beta_i = \beta_i + \text{noise}$, and individual-stock betas are noisy. The skeptic's argument: the noise in $\hat\beta_i$ biases the cross-sectional slope on beta toward zero, so beta's *flat* estimated slope might be a **measurement artifact** — beta could truly matter, with attenuation merely masking a real positive premium. The bias points toward zero because random noise in the regressor inflates its variance without adding any true covariance with returns, diluting the signal-to-noise ratio that the slope estimates (the classic $\hat\gamma \to \gamma\cdot\frac{\sigma^2_\beta}{\sigma^2_\beta+\sigma^2_{\text{noise}}}$ shrinkage).

(ii) The fix: assign betas via **portfolios**, not individual stocks — a stock inherits the beta of the size–beta portfolio it belongs to, estimated on the portfolio's longer, less noisy return series. A portfolio beta is less noisy because it is an *average* of its members' betas, and the independent estimation errors in the individual betas largely **cancel** when averaged (the same $1/n$ variance reduction as Problem 1a, applied to estimation error rather than return noise). So the portfolio beta has a much smaller noise variance $\sigma^2_{\text{noise}}$, which pushes the attenuation factor back toward 1.

(iii) The §6 honest reading: attenuation is a *strained* rescue because the estimated beta slope is so close to zero (and sometimes the wrong sign) that, after the portfolio-grouping fix has already shrunk the noise a great deal, there is essentially no positive signal left for attenuation to be hiding — to "uncover" a real beta premium you would need an implausibly large residual measurement error to scale a near-zero estimate up to a meaningful number. The objection is the *right* one to raise (it is precisely why the authors went to portfolios), but the combination of the portfolio fix and the near-zero estimate means the data do not let attenuation carry the day.

**(c) (6 pts) Look-ahead and survivorship in the book-equity data.**

(i) **Survivorship bias** is the distortion that arises when your sample includes only (or disproportionately) the firms that *survived* long enough to be recorded, dropping those that died. Compustat's historical coverage was **backfilled**, and backfilling tends to add firms that lasted long enough to be worth adding — so early-sample book equity over-represents survivors, which can flatter the value premium if, for example, the distressed high-BE/ME firms that *didn't* survive are missing from the early data, making value's average return look safer and higher than it really was in real time.

(ii) **Look-ahead bias** is using information in the sort or regression that an investor could not actually have known *at the time* the position was formed. Matching December book equity to that same December's return would credit an investor with an accounting number — the firm's annual report — that is not actually public until months later; you would manufacture "predictability" that no real-time investor could have traded on, because the predictor was unknowable when the trade had to be placed.

(iii) The concrete check in `nb5.1`: the **"break it on purpose"** demonstration — re-running the sort with *contemporaneous* market equity (and, by the same logic, mismatched accounting timing) instead of the properly lagged values and showing that the spread *balloons*. By exhibiting how much the look-ahead-contaminated sort inflates the premium relative to the honest lagged sort, the notebook *demonstrates* that the timing lag is doing real protective work rather than merely asserting the construction was careful.

---

## Problem 6 — Design the replication pipeline for `nb5.1` (10 points)

**(a) (4 pts) The sort pipeline.** Ordered steps from a firm-month panel to the sorts:

1. **Assemble characteristics with the right timing.** For each firm, take **market equity** (price $\times$ shares from CRSP) measured at the *portfolio-formation* date and **book equity** (from Compustat) from the **fiscal year ending in calendar year $t-1$**. Form **BE/ME** = (lagged book equity) / (lagged market equity).
2. **Apply the July-to-June timing lag (the load-bearing step).** Match returns from **July of year $t$ through June of year $t+1$** to the accounting data from the fiscal year ending in $t-1$, and to size measured at the end of June $t$. *Why:* the lag forces every sorting variable to be genuinely *knowable before* the return window it explains, so the explanatory variable cannot peek at the outcome. This defends against **look-ahead bias** (§6) — the same reason December book equity must never be matched to December returns.
3. **Univariate decile sorts (Problem 2).** Each year, rank firms into ten **size** deciles by the lagged size; separately rank into ten **BE/ME** deciles. Form the ten portfolios (e.g., equal-weight the firms in each), compute each portfolio's monthly return over the July–June window, and average over the sample. Read the spreads D1$-$D10 and B10$-$B1.
4. **Size×BE/ME double sort (§7 Ex. 2).** Each year, independently rank firms into size buckets and BE/ME buckets, then intersect them into the $5\times5$ (or $3\times3$) grid; form each cell's portfolio, compute and average its monthly return; print the grid. The timing lag of step 2 applies identically — both sort keys are the lagged values.

**(b) (4 pts) The Fama–MacBeth pipeline.**

- **Pass 1 (betas).** For each firm (or, better, each size–beta portfolio), run a **time-series regression of returns on the market return** over a window *ending before* the return month being explained, to get a **pre-formation beta**. Assign each stock the beta of the **portfolio** it belongs to — *portfolio-level* (tying to Problem 5b) because individual-stock betas are too noisy and would attenuate beta's slope toward zero; averaging within a portfolio cancels the independent estimation errors and gives a much less noisy beta.
- **Pass 2 (monthly cross-sections).** For **each month $t$**, run one cross-sectional regression of that month's returns on the characteristics ($\beta$, $\log\text{size}$, $\log\text{BE/ME}$), and **collect that month's slope vector** $\hat\gamma_{j,t}$. After looping over all $T$ months, form the point estimate $\hat\gamma_j=\frac1T\sum_t\hat\gamma_{j,t}$ and the FM standard error $\widehat{\operatorname{se}}(\hat\gamma_j)=\operatorname{sd}_t(\hat\gamma_{j,t})/\sqrt T$ from the scatter of the collected slopes; the $t$-statistic is $\hat\gamma_j/\widehat{\operatorname{se}}(\hat\gamma_j)$.
- **Three specifications** to stage the §4 horse race: **(A) beta alone**, **(B) $\log\text{size}$ and $\log\text{BE/ME}$ alone**, **(C) all three together** (the kitchen sink). Watch beta's $t$ collapse from A to C while size and BE/ME survive.

**(c) (2 pts) Reproducibility and data discipline.** (i) Ship a **seeded synthetic fallback** — a panel with the *same schema* as CRSP/Compustat (firm-month returns, market equity, book equity), generated with a fixed random seed and with the size and value premia *planted* — so the entire notebook runs end-to-end on a student laptop with no licensed data and identical results every run. (ii) Gate the real-data path behind a flag (e.g., `RUN_PATH_A=False`), and on that path **pin the CRSP/Compustat snapshot date** and note that licensed data stays read-only on GMU infrastructure (Conventions §5) — and *do not print or hard-code any real CRSP/Compustat table values*, so no fabricated numbers can leak into the prose. The deliverables (sorts, double sort, FM table) are produced from the synthetic panel, clearly labeled as illustrative.

---

*End of solutions for PS 5.1. The arithmetic checks — size spread 0.84 %/mo, value spread 1.23 %/mo, naive beta spread +0.32 dissolved to $\pm0.02$ within size, the six FM $t$-statistics (1.3 / 4.3 / 4.9 / 0.2 / 3.9 / 4.4), the inverted slope sd $\approx 1.63$, and the multiple-testing $P\approx 0.64$ — were all confirmed in Python and reproduce in `nb5.1` (`notebooks/week-05/nb5.1-ff92-portfolio-sorts.ipynb`). If your numbers match and you can state, in your own words, why beta dies in the double sort and the kitchen sink while size and BE/ME survive, you have read Fama & French (1992) the way a referee reads it.*
