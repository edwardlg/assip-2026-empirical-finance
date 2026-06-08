# PS 4.4 — Synthetic Control Weights & Placebo Inference

**Course:** ASSIP 2026 · 8-Week Empirical Finance Track · Week 4 · Problem Set 4.4
**Covers:** Ch 4.4 (Synthetic Control & Synthetic DiD).
**Methods allowed:** only what is built through Ch 4.4 — the single-treated-unit setup with $J+1$ units (treated unit $i=1$, donor pool $i=2,\dots,J+1$); pre-period $t=1,\dots,T_0$ and post-period $t=T_0+1,\dots,T$; the potential outcomes $Y_{it}^{N}$ (no treatment) and $Y_{it}^{I}$ (intervention) with effect $\tau_{1t}=Y_{1t}^{I}-Y_{1t}^{N}$; the synthetic counterfactual $\hat{Y}_{1t}^{N}=\sum_{j=2}^{J+1} w_j Y_{jt}$ and estimate $\hat{\tau}_{1t}=Y_{1t}-\hat{Y}_{1t}^{N}$; the convex-weight program ($w_j\ge 0$, $\sum_j w_j=1$) minimizing pre-period mismatch; the root-mean-squared prediction error $\text{RMSPE}_{\text{pre}}$ and $\text{RMSPE}_{\text{post}}$; the post/pre RMSPE ratio $r_i$; the placebo permutation $p$-value $p=\#\{i:r_i\ge r_1\}/(J+1)$ and its $1/(J+1)$ floor; and the synthetic-DiD idea of unit *and* time weights with DiD-style differencing. You do **not** need anything from later chapters. DiD and parallel trends from Ch 4.1 are fair game as the comparison baseline.

**Total: 100 points.** Point values are stated per problem. Show your reasoning — a correct final number with no derivation earns roughly half credit, because the reasoning *is* the skill we are grading. Solutions are in Appendix E (`E-w4-ps4.4-solutions.md`); try every part before you look.

A note on the difficulty curve: Problem 1 is a conceptual warm-up on *when* synthetic control beats DiD. Problem 2 is the mechanical heart — finding convex donor weights by hand on a small, exactly-solvable case. Problem 3 turns those weights into a post-period counterfactual and reads off the effect. Problem 4 is the inferential core: post/pre RMSPE ratios, the permutation rank, and the $1/(J+1)$ floor. Problem 5 is a short conceptual essay on convexity and no-extrapolation. Problem 6 stress-tests an edge case where synthetic DiD beats classic synthetic control. Throughout, the running setting is Priya's single-treated-state climate study from Ch 4.4: one state passed a first-in-the-nation **climate-risk disclosure mandate** forcing home insurers to publish wildfire- and flood-exposure pricing, and the outcome $Y_{it}$ is the average homeowner premium (in **hundreds of dollars**) in state $i$, year $t$. Premiums are reported in hundreds of dollars throughout, so a value of $12$ means \$1,200.

---

## Problem 1 — When synthetic control beats DiD (14 points)

Priya has exactly **one** treated state and a pool of untreated states. She is deciding between a 2×2 difference-in-differences against "the rest of the states" (Ch 4.1) and a synthetic control (Ch 4.4).

**(a) (4 pts)** State the **parallel-trends assumption** that a DiD against the equal-weighted rest-of-the-states control would require, in one sentence, using Priya's premium outcome. Then explain in two or three sentences why this assumption is *especially* hard to defend when there is a single treated unit — what goes wrong with "pick one similar state" and with "average all the others equally"?

**(b) (5 pts)** The chapter claims "**DiD is synthetic control with the weights frozen at equality.**" Make that precise. Write the DiD counterfactual for the treated state as a weighted average $\hat{Y}_{1t}^{N}=\sum_{j=2}^{J+1} w_j Y_{jt}$ of the donors and state the implied weight $w_j$ for each of the $J$ donors. Then explain, in terms of the pre-period, what synthetic control does *differently* with those weights and why that is properly described as "*earning* the parallel-trends comparison rather than *assuming* it."

**(c) (5 pts)** Give two concrete features of a research setting that should push Priya toward synthetic control over DiD, and one feature that should push her *back* toward DiD (or synthetic DiD). For each, name the assumption or mechanism involved — do not just say "it's better." (Hint: think about the number of treated units, the quality of the pre-period match, and what a critic could do to your one arbitrary control choice.)

---

## Problem 2 — Donor weights by hand: matching the pre-period (22 points)

Strip Priya's study to a toy you can solve with a pencil. There are **three pre-treatment years** (2015, 2016, 2017, so $T_0$ is 2017) and **three donor states** in the pool, which we will call $A$, $B$, and $C$ ($J=3$). All premiums are in hundreds of dollars. The treated state's pre-period premiums are

$$
\mathbf{X}_1 = (12,\ 13,\ 14)',
$$

and the three donors' pre-period premium vectors (each column is one donor's three years) are

$$
\mathbf{X}_0 = \begin{pmatrix} 10 & 14 & 20 \\ 10 & 16 & 21 \\ 10 & 18 & 24 \end{pmatrix},
\qquad
\text{i.e.}\quad
A=(10,10,10)',\ \ B=(14,16,18)',\ \ C=(20,21,24)'.
$$

We use $\mathbf{V}=\mathbf{I}$ (all three years weighted equally), so the objective is the plain pre-period sum of squared mismatch
$$
\text{SSR}(\mathbf{w}) \;=\; \big(\mathbf{X}_1-\mathbf{X}_0\mathbf{w}\big)'\big(\mathbf{X}_1-\mathbf{X}_0\mathbf{w}\big)
\;=\;\sum_{t=1}^{3}\Big(X_{1t}-\textstyle\sum_j w_j X_{0,tj}\Big)^2,
$$
minimized over convex weights $\mathbf{w}=(w_A,w_B,w_C)$ with $w_j\ge 0$ and $w_A+w_B+w_C=1$.

**(a) (4 pts)** Warm up with the naive DiD choice: equal weights $w_A=w_B=w_C=\tfrac13$. Compute the synthetic premium path $\hat{Y}_{1t}^{N}$ for the three pre-years and the resulting $\text{SSR}$. Is the equal-weighted "control" a good match to the treated state?

**(b) (8 pts)** Now do the real optimization, but use the structure to avoid calculus. First argue, by comparing donor $C$ to donors $A$ and $B$, that the optimal weight on $C$ should be **zero** — i.e., that loading any weight on $C$ can only hurt. Then, *restricting to $A$ and $B$ only* (so $w_B = 1-w_A$), set up the convex match $w_A A + (1-w_A) B = \mathbf{X}_1$ and solve for $w_A$ using any one of the three pre-years. Verify your $w_A$ reproduces the treated path in **all three** years (so the match is exact and $\text{SSR}=0$).

**(c) (4 pts)** Write down the full optimal weight vector $\mathbf{w}^{*}=(w_A^{*},w_B^{*},w_C^{*})$ and the synthetic pre-period path. Confirm it satisfies both constraints (non-negativity and sum-to-one). In one sentence, interpret the weights as a "sentence Priya could put in a paper" the way the chapter describes (e.g., "the treated state is X parts $A$, Y parts $B$").

**(d) (6 pts)** A classmate proposes dropping the convexity constraints and instead running an **unconstrained** regression of $\mathbf{X}_1$ on the three donors (allowing negative coefficients and coefficients that need not sum to one). With three pre-years and three donors, what will the in-sample fit look like, and roughly why? Explain in two or three sentences why a *perfect* in-sample fit from such a regression would not reassure Priya — name what the convexity constraints buy her that the unconstrained fit throws away, and what the unconstrained fit is likely to do in the post-period.

---

## Problem 3 — From weights to counterfactual: reading the effect (16 points)

Carry the optimal weights $\mathbf{w}^{*}$ from Problem 2 into the **post-period**. The mandate takes effect in 2018, so the post-years are 2018, 2019, 2020. The donors' **observed (untreated)** premiums in those years are

| Year | Donor $A$ | Donor $B$ | Donor $C$ |
|:---:|:---:|:---:|:---:|
| 2018 | $10$ | $20$ | $26$ |
| 2019 | $11$ | $21$ | $27$ |
| 2020 | $11$ | $23$ | $29$ |

and the treated state's **actual** premiums (with the mandate in force) are $Y_{1,2018}=18$, $Y_{1,2019}=20$, $Y_{1,2020}=21$.

**(a) (6 pts)** Using $\mathbf{w}^{*}$ from Problem 2, build the synthetic counterfactual $\hat{Y}_{1t}^{N}=\sum_j w_j^{*} Y_{jt}$ for each post-year. Show the arithmetic.

**(b) (5 pts)** Compute the estimated effect $\hat{\tau}_{1t}=Y_{1t}-\hat{Y}_{1t}^{N}$ in each post-year, and report the **average post-treatment gap** as Priya's headline point estimate. State it in Priya's units (premium dollars per home).

**(c) (5 pts)** Explain, in two or three sentences, why this construction *is* the synthetic-control estimate and how it relates to the counterfactual $Y_{1t}^{N}$. In particular: which quantity in $\hat{\tau}_{1t}=Y_{1t}-\hat{Y}_{1t}^{N}$ is observed, which is the estimate of the unobservable counterfactual, and what would the gap have looked like in the pre-period if the match in Problem 2 was good? Why does that pre-period behavior license reading the post-period gap as causal?

---

## Problem 4 — Placebo permutation inference (24 points)

Priya now needs an honest $p$-value, and with one treated unit she cannot use a t-statistic. She runs the placebo procedure of Abadie, Diamond and Hainmueller (2010): treat each donor as if it were the treated unit, build a synthetic control for it from the *other* donors, and compute its pre- and post-period fit. Here are the results for the real treated state plus **nine** donor states ($J=9$, so $J+1=10$ units). RMSPE values are in premium units (hundreds of dollars).

| Unit | $\text{RMSPE}_{\text{pre}}$ | $\text{RMSPE}_{\text{post}}$ |
|:---|:---:|:---:|
| **Treated state** | $0.40$ | $3.20$ |
| Donor 1 | $0.50$ | $0.90$ |
| Donor 2 | $2.00$ | $5.00$ |
| Donor 3 | $0.30$ | $0.60$ |
| Donor 4 | $1.20$ | $1.10$ |
| Donor 5 | $0.45$ | $0.70$ |
| Donor 6 | $3.00$ | $4.50$ |
| Donor 7 | $0.60$ | $0.50$ |
| Donor 8 | $0.80$ | $1.40$ |
| Donor 9 | $0.55$ | $0.66$ |

**(a) (6 pts)** For every unit, compute the **post/pre RMSPE ratio** $r_i = \text{RMSPE}_{\text{post},i}/\text{RMSPE}_{\text{pre},i}$. Report the ten ratios (two decimals are fine).

**(b) (5 pts)** Rank the units by $r_i$ from largest to smallest. Where does the treated state fall? Compute the **permutation $p$-value** $p=\#\{i:r_i\ge r_1\}/(J+1)$ and state it as a fraction and a decimal.

**(c) (5 pts)** Now show *why the ratio is the right yardstick and the raw post-period gap is not.* Re-rank the units by $\text{RMSPE}_{\text{post}}$ alone. Where would the treated state fall on that (wrong) ranking, and which two donors would leapfrog it? Explain in two sentences what is special about those two donors that the ratio correctly *neutralizes* — and what mistaken conclusion Priya would draw if she ranked on raw post-gaps.

**(d) (8 pts)** The $1/(J+1)$ **floor**, four sub-points.
&nbsp;&nbsp;(i) With $J=9$ donors, what is the *smallest possible* permutation $p$-value any unit could achieve, and is the treated state at that floor here?
&nbsp;&nbsp;(ii) Priya wants to be able to report $p<0.05$ if the effect is genuinely the most extreme. What is the minimum number of donors $J$ she needs in her pool for the floor $1/(J+1)$ to dip below $0.05$? (Solve $1/(J+1)<0.05$ for $J$.)
&nbsp;&nbsp;(iii) A classmate has a single-treated-unit synthetic control with only $J=8$ donors and reports "$p<0.01$." Explain, in one sentence, why that number is not credible regardless of how clean the gap looks.
&nbsp;&nbsp;(iv) In one or two sentences, explain what *kind* of inferential statement the permutation $p$-value is — what it does and does **not** assume relative to the t-statistic the chapter warns against — and why its resolution is "bounded by how many placebos you have."

---

## Problem 5 — No extrapolation: the convexity constraint as conscience (8 points)

This problem is a short conceptual essay (no arithmetic required). Priya discovers that her treated state has the **highest** pre-period premium of *any* state in her data — it sits at the very edge of the donor distribution.

**(a) (4 pts)** Explain why a **convex** synthetic control (weights $\ge 0$, summing to one) must *systematically underfit* a treated unit that lies above every donor. Refer explicitly to the fact that $\hat{Y}_{1t}^{N}=\sum_j w_j Y_{jt}$ with convex weights is boxed inside the range of the donor premiums — it "can never be higher than the most expensive donor or lower than the cheapest." What will the pre-period RMSPE look like as a result, and why is the chapter's claim that "the convexity constraint will not let it lie about that" a *feature*, not a bug?

**(b) (4 pts)** Contrast this with the unconstrained regression of Problem 2(d): such a regression *can* reach above the donors by using coefficients greater than one and negative coefficients on other donors. Explain in two or three sentences why that ability to **extrapolate** is precisely what makes the unconstrained fit untrustworthy out of sample, and connect it to the chapter's point that convexity makes synthetic control "read less like a regression and more like matching." Name the one diagnostic Priya should report so a reader can judge whether the edge-unit problem has corrupted her counterfactual.

---

## Problem 6 — Synthetic DiD vs synthetic control on an edge unit (16 points)

Priya's treated state is the edge unit from Problem 5: no convex combination of donors can match its *level*, but a convex blend *can* match its *trend*. Here is a clean numerical version. There are three pre-years (2015–2017) and two post-years (2018–2019). The treated state's premiums and the premiums of its best convex donor blend (the "synthetic" path that classic synthetic control produces) are:

| Year | Treated $Y_{1t}$ | Synthetic $\hat{Y}_{1t}^{N}$ (best convex blend) |
|:---:|:---:|:---:|
| 2015 (pre) | $22$ | $20$ |
| 2016 (pre) | $23$ | $21$ |
| 2017 (pre) | $24$ | $22$ |
| 2018 (post) | $28$ | $23$ |
| 2019 (post) | $29$ | $24$ |

Notice the donor blend tracks the treated state's *slope* (both rise by $1$ per year in the pre-period) but sits a constant **2 units below** it in level — the convex hull cannot reach up to the edge unit, exactly the Problem-5 pathology.

**(a) (5 pts)** Compute the **classic synthetic-control gap** $\hat{\tau}_{1t}=Y_{1t}-\hat{Y}_{1t}^{N}$ for all five years. Report the average pre-period gap and the average post-period gap. What would Priya report as her naive synthetic-control "effect," and why is that number contaminated?

**(b) (6 pts)** Synthetic DiD (Arkhangelsky et al. 2021) keeps the same unit-weighted donor blend but *differences out the constant level gap* DiD-style, because it only requires a matched **trend**, not a matched **level**. Implement this by hand: take the average pre-period gap as the baseline level difference, subtract it from each post-period gap, and report the resulting SDID estimate for each post-year and on average. (You are doing, in miniature, what the SDID objective $\sum_{i,t}(Y_{it}-\mu-\alpha_i-\beta_t-\tau D_{it})^2\,\hat w_i\hat\lambda_t$ does when the unit fixed effect $\alpha_i$ absorbs the constant level gap.)

**(c) (5 pts)** The true injected effect in this scenario is a $+3$ (hundred-dollar) premium jump in each post-year. Which method recovered it — classic synthetic control or synthetic DiD — and by how much was the other one off? Explain in two or three sentences *why* SDID succeeds here where classic synthetic control fails, using the words "level," "trend," and "fixed effect." Then state the one situation from the chapter in which you would still prefer **classic** synthetic control over SDID.

---

*End of PS 4.4. When you have attempted everything, check yourself against `book/appendices/E-solutions-manual/E-w4-ps4.4-solutions.md`. Every numerical part (the donor-weight match in Problem 2, the counterfactual in Problem 3, the RMSPE ratios and floor in Problem 4, and the SDID differencing in Problem 6) can be confirmed in a few lines of NumPy/`scipy.optimize` — you are encouraged to do so after working them by hand. In `nb4.4` you will run the full synthetic-control pipeline, the placebo loop, and a real synthetic-DiD estimator on Priya's simulated panel and watch these same patterns appear at scale.*
