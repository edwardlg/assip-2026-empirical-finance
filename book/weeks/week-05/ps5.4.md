# Problem Set 5.4 — Re-running Petersen's Clustering Comparison on a Panel

*Covers Ch 5.4 (Reader's Guide to Petersen 2009) and builds directly on Week 2, Ch 2.4 (the sandwich estimator, White/HC, the cluster-robust sandwich, the Moulton inflation factor, the few-clusters caveat, and the firm-effect / time-effect / two-way taxonomy). Methods allowed: everything through Ch 2.4 and Ch 5.4. As in PS 2.4, **the point estimate $\hat\beta$ is never the question** — Petersen's whole paper is about which **standard error** to trust. You may treat every $\hat\beta$ as already computed; your job is to reason about $\boldsymbol\Omega=\operatorname{Var}(\boldsymbol\varepsilon\mid\mathbf{X})$, about coverage, and about which method's assumed shape for $\boldsymbol\Omega$ matches the truth. Show your reasoning; a boxed verdict with no argument earns no credit.*

**Total: 100 points.** Six tasks, escalating. Task 1 is the conceptual taxonomy (firm effect vs. time effect, and which clustering each demands). Task 2 reads a simulated coverage table (method × correlation structure) and names which SE is right. Task 3 is Petersen's own self-diagnostic — cluster by firm, cluster by time, see which moves the SE. Task 4 is the few-clusters caution (consistency in the number of clusters $G$, not the number of observations $N$). Task 5 compares Fama–MacBeth against cluster-by-time. Task 6 is a replication-design task: describe the Monte Carlo coverage experiment you will run in **nb5.4**.

A reminder on the one idea that runs through the whole set, because it *is* Petersen's paper. A standard-error method is a **bet about the shape of $\boldsymbol\Omega$** — the matrix of error variances and covariances. Classical OLS bets $\boldsymbol\Omega=\sigma^2\mathbf{I}$ (constant diagonal, zero off-diagonal). White/HC bets the off-diagonals are zero but lets the diagonal vary. Cluster-by-firm bets the off-diagonals live in dense **firm blocks** (a firm's errors correlated with themselves across years). Cluster-by-time bets they live in **time blocks** (all firms' errors correlated within a year). The estimate $\hat\beta$ never moves as you change the bet; only your claimed uncertainty does. Petersen's contribution was to make the bet *decidable*: build worlds where you know the true $\boldsymbol\Omega$, and watch which method's reported SE matches the true sampling variability of $\hat\beta$. A method "works" precisely when its assumed shape for $\boldsymbol\Omega$ matches the real one. Carry that sentence into every task below.

A note on numbers. The coverage figures in this set are **labeled illustrative values** — round, pedagogically clean numbers chosen to reproduce the *qualitative* pattern Petersen established (OLS and White undercover under a firm or time effect; clustering on the right dimension restores near-nominal coverage; the wrong clustering does not). They are **not** transcribed from Petersen's tables, and you should not cite them as his. When you run nb5.4 in Task 6 you will generate your own.

---

## Task 1 — The firm-effect / time-effect taxonomy (14 points)

This is the lens you classify a panel through *before* you choose a standard error. Two students set up pooled panel regressions $y_{it}=\beta_0+\beta_1 x_{it}+\varepsilon_{it}$.

- **Maya** regresses each firm-year's loan-default rate on the firm's leverage, on a panel of $N_{\text{firms}}=1{,}200$ lenders over $T=15$ years. She argues: "A lender that runs hot on defaults this year — sloppy underwriting, a bad regional book — tends to run hot next year too. That habit is the firm's, and it persists."
- **Priya** regresses each firm-year's insurance-loss ratio on the firm's climate-exposure score, on a panel of property insurers over the same 15 years. She argues: "When a megastorm hits in a given year, *every* insurer's loss ratio jumps together that year. The shock is the calendar's, not the firm's."

**(a) (4 pts)** Name the dependence each student is describing — a **firm effect** or a **time effect** — and, for each, write down *where the nonzero off-diagonal entries of $\boldsymbol\Omega$ live* (which pairs $(\varepsilon_{it},\varepsilon_{js})$ are correlated, and which are zero). Use the indices $i,j$ for firms and $t,s$ for years.

**(b) (4 pts)** State the clustering choice each student should make, and explain in one sentence *why that clustering is the matching bet* — i.e., what block structure of $\boldsymbol\Omega$ each clustering choice allows.

**(c) (3 pts)** Petersen models these effects as **additive variance components**: $\varepsilon_{it}=\gamma_i+\delta_t+\nu_{it}$, with $\gamma_i$ the firm component, $\delta_t$ the time component, and $\nu_{it}$ idiosyncratic noise, all independent. Show that Maya's "pure firm effect" world is the special case $\operatorname{Var}(\delta_t)=0$, and write the resulting $\operatorname{Cov}(\varepsilon_{it},\varepsilon_{is})$ for $t\neq s$ (same firm) in terms of the component variances.

**(d) (3 pts)** Recall the Moulton logic from Ch 2.4 §4.1: the damage that an ignored firm effect does to the OLS standard error scales with the product of the within-firm correlation of the **errors** *and* of the **regressor**. Devon objects: "Both Maya and Priya have a real firm/time effect in their *errors*, so both must have badly broken OLS SEs." Give the one condition on the **regressor** $x_{it}$ under which the broken-error structure barely hurts the OLS SE, and name which of Maya's or Priya's regressors (leverage; climate-exposure score) is more likely to be persistent within firm and therefore more dangerous.

---

## Task 2 — Read the simulated coverage table; name the right SE (20 points)

Petersen's identification strategy was to build worlds with a known true $\beta$ and a known $\boldsymbol\Omega$, then check, across many simulated panels, what fraction of each method's nominal **95% confidence intervals actually contain the true $\beta$** (its *coverage*). A correct method covers $\approx 0.95$; an overconfident method — one whose reported SE sits below the true sampling SD of $\hat\beta$ — covers far less.

Below are **illustrative coverage rates** (not Petersen's own numbers — see the header note) from a coverage experiment of the kind nb5.4 runs. Each cell is the fraction of 95% intervals that trapped the true $\beta=0.30$, across many simulated panels. The columns are the *true* correlation structure of the world; the rows are the SE method.

| Method | World: **firm effect** | World: **time effect** | World: **both** |
|---|---|---|---|
| Classical OLS | 0.71 | 0.70 | 0.58 |
| White / HC1 | 0.73 | 0.72 | 0.60 |
| Cluster by firm | **0.94** | 0.72 | 0.78 |
| Cluster by time | 0.73 | **0.94** | 0.79 |
| Two-way (firm + time) | 0.93 | 0.93 | **0.94** |

**(a) (4 pts)** Read down the **firm-effect** column. Classical OLS covers only 0.71 against a nominal 0.95. State plainly what that 0.71 *means* for someone publishing a result with OLS SEs in this world — in particular, translate "coverage 0.71" into a statement about how often their "95% confident" claim is actually wrong, and in which direction the SE errs.

**(b) (5 pts)** The single most important "gotcha" in Petersen: in the firm-effect column, **White/HC1 covers 0.73 — essentially no better than OLS.** Explain why. Be precise about what White SEs *do* fix (which part of $\boldsymbol\Omega$) and what they are *blind to* (which part), and why that blindness is exactly fatal here. End with the one-sentence warning about the marketing word "robust."

**(c) (4 pts)** In the firm-effect column, **cluster-by-firm recovers 0.94** while cluster-by-time stays at 0.73. State the general principle this illustrates ("a method works when ___"), and explain why cluster-by-*time* fails to help even though it is "a clustering method."

**(d) (4 pts)** Read across the **time-effect** column and confirm the *symmetry*: which single method now does the job, and which clustering choice fails? In one sentence, what does this symmetry tell you about whether "cluster by firm" is a universally safe default.

**(e) (3 pts)** Look at the **both** column. Cluster-by-firm covers 0.78 and cluster-by-time covers 0.79 — each better than OLS but still short of 0.95 — while two-way covers 0.94. Explain why a *single* one-way clustering is no longer enough when both effects are present, and what two-way clustering catches that neither one-way version does.

---

## Task 3 — Diagnose the dependence: Petersen's self-diagnostic (16 points)

In a *simulation* you know the true $\boldsymbol\Omega$. In your *own* data you do not — so Petersen gives you a diagnostic you can run on real output: **cluster by firm and look; cluster by time and look; whichever clustering moves the SE more away from the White number is pointing at the bigger source of correlation.** Sam runs a single pooled panel regression of a momentum strategy's firm-level monthly alpha on a signal, and reports the same $\hat\beta_1=0.30$ under five SE flavors. (Illustrative numbers; the estimate is identical in every row by construction.)

| SE flavor | Std. error | t-stat |
|---|---|---|
| Classical (OLS) | 0.040 | 7.5 |
| White (HC1) | 0.042 | 7.1 |
| Clustered by **firm** | 0.045 | 6.7 |
| Clustered by **time** | 0.120 | 2.5 |
| Two-way (firm + time) | 0.122 | 2.5 |

**(a) (5 pts)** Apply the diagnostic. Compute (qualitatively is fine, but say the ratios) how much firm-clustering moves the SE relative to White, and how much time-clustering moves it. Which effect dominates Sam's panel — a persistent firm effect, a common time effect, or both? What is the correct clustering choice here?

**(b) (4 pts)** Sam's mentor says, "This is a momentum/return panel — of course it's a time effect; the whole market moves together each month." Sam protests that he *expected* a firm effect because he had drilled the corporate-finance examples where the firm effect dominates. Explain why the *diagnostic on the output*, not the prior expectation, is the right tiebreaker — and connect this to the Ch 5.4 point that **the right clustering depends on the left-hand-side variable, not just on the dataset.** (Monthly returns are dominated by common market shocks; firm leverage panels are dominated by persistent firm differences. Same kinds of firms; different $\boldsymbol\Omega$.)

**(c) (4 pts)** Notice that the **two-way** SE (0.122) is barely above the **time-clustered** SE (0.120). Explain what that near-equality tells you about the relative size of the firm and time components in Sam's residuals, and why two-way clustering, when one dimension is essentially inert, costs almost nothing but also adds almost nothing here.

**(d) (3 pts)** A subtle trap: suppose Sam had reported only the **OLS and White** rows (0.040 and 0.042) and stopped — they agree, so he concludes "the errors are well-behaved, no clustering needed." Using the table, explain why the close agreement of OLS and White is **not** evidence that clustering is unnecessary. What does the OLS-vs-White comparison actually test, and what does it miss?

---

## Task 4 — The few-clusters caution: consistency in $G$, not $N$ (16 points)

The cluster-robust sandwich (Ch 2.4 §4.2) is consistent as the **number of clusters $G\to\infty$**, *not* as the number of observations $N\to\infty$. Petersen flags this as his own main caveat (Ch 5.4 §6): when $G$ is small, the cluster-robust SE is itself noisy and **biased downward**, reintroducing the very overconfidence it was meant to cure.

Priya clusters by **time** in a climate-loss panel that, by construction, has a genuine time effect, so cluster-by-time is the *correct* method. But she has only a handful of years. Below are **illustrative coverage rates** for the *correct* method (cluster-by-time) as the number of time clusters $G$ shrinks — the kind of sweep nb5.4 produces.

| Number of time clusters $G$ (years) | Cluster-by-time coverage |
|---|---|
| 30 | 0.94 |
| 20 | 0.92 |
| 12 | 0.88 |
| 8 | 0.82 |
| 5 | 0.74 |

**(a) (4 pts)** Describe the pattern and state the paradox in one sentence: Priya is using the *correct* clustering for her world, yet her coverage falls from 0.94 to 0.74 as $G$ shrinks. Why does being "right about the dimension" not save her when $G=5$?

**(b) (4 pts)** Explain *why* small $G$ biases the cluster-robust SE **downward** (not upward). What is the estimator using the $G$ cluster sums to approximate, and why is an average built from only 5 noisy pieces a poor — and specifically *too small* — estimate of the true sampling variability of $\hat\beta$? It is the same "too few independent pieces of evidence" disease as the Moulton story, one level up: the **clusters** themselves are now the scarce independent units.

**(c) (4 pts)** Devon says, "Easy fix — Priya should add 200 more *firms* per year. That's thousands more observations; surely that fixes the few-clusters problem." Explain precisely why pouring more *observations into the existing 5 years* does **not** help the few-clusters problem, and what the only thing that does help is. Tie this to the Task-1(d) / Ch 2.4 lesson that precision in clustered inference lives in $G$, not $N$.

**(d) (4 pts)** Give two concrete fixes from Ch 2.4 / Ch 5.4 §6 for the small-$G$ case, and say what each does. (Hint: one swaps the critical value; one resamples whole clusters.) State the rough rule-of-thumb threshold below which you should worry, and why "robust to within-cluster correlation" stops being a free lunch below it.

---

## Task 5 — Fama–MacBeth vs. cluster-by-time (18 points)

Fama–MacBeth (FM), which you built in Lab 2, estimates $\beta$ **period by period**: for each year $t$ it runs a *cross-sectional* regression of $y$ on $x$ across all firms in that year, getting a slope $\hat\beta_t$; the reported estimate is the average $\bar\beta=\frac1T\sum_t\hat\beta_t$ and the reported SE is the standard deviation of the $\hat\beta_t$'s divided by $\sqrt{T}$, i.e. $\operatorname{se}_{\text{FM}}=\operatorname{sd}(\hat\beta_t)/\sqrt{T}$ (compared against a $t$-distribution with $T-1$ degrees of freedom). Below are **illustrative coverage rates** of the kind nb5.4's FM-vs-cluster comparison produces.

| World | Fama–MacBeth coverage | Cluster-by-time coverage |
|---|---|---|
| Pure **time** effect | 0.94 | 0.94 |
| Pure **firm** effect | 0.79 | 0.73 |

**(a) (5 pts)** Explain *why* Fama–MacBeth correctly handles a **time effect**. Walk through what averaging period-by-period cross-sectional slopes does to a common shock $\delta_t$ that hits every firm in year $t$ together: how does building the SE from the *spread of the yearly slopes* automatically account for that within-year correlation? Why is this morally the same bet about $\boldsymbol\Omega$ as cluster-by-time — hence the matching 0.94 in the top row?

**(b) (5 pts)** Explain *why* Fama–MacBeth **fails under a firm effect** (it undercovers at 0.79). The key is that a persistent firm component $\gamma_i$ makes a firm's residual in year $t$ correlated with its residual in year $t+1$ — i.e., the yearly cross-sectional slopes $\hat\beta_t$ and $\hat\beta_{t+1}$ are **not independent draws**. Why does that correlation make $\operatorname{sd}(\hat\beta_t)/\sqrt{T}$ understate the true sampling variability of $\bar\beta$? State the slogan: FM corrects for a ___ effect but is blind to a ___ effect.

**(c) (4 pts)** Petersen's claim is that the **firm effect dominates the typical corporate-finance panel**, which is why he warns against the then-common reflex of reaching for Fama–MacBeth. Given Task 5(b), state when Fama–MacBeth *is* the right tool and when it is the wrong one, and name the modern method you would prefer over FM if you suspected the firm effect dominated. (You do not need both effects yet — just the one-way fix.)

**(d) (4 pts)** A classmate notes that cluster-by-time *also* covers only 0.73 in the firm-effect world (from Task 2). "So FM and cluster-by-time are equally wrong under a firm effect — they're interchangeable." Is that right? Explain what the two methods share that makes them *both* fail there, and therefore why "switch from FM to cluster-by-time" would **not** fix a firm-effect problem — what dimension must you cluster on instead?

---

## Task 6 — Replication design: the Monte Carlo coverage experiment (16 points)

You will run this in **nb5.4 (Petersen clustering replication)**, which hands you a panel-simulation harness. Before you touch code, *design the experiment on paper* — Petersen's identification strategy is the whole point, and you should be able to state it without the notebook.

The harness exposes: a `simulate_panel(structure, ...)` function that builds one balanced panel of `n_firms` $\times$ `n_years` firm-years from a *known* process with true slope $\beta=0.30$ and an error $\varepsilon_{it}=\texttt{firm\_sd}\cdot\gamma_i+\texttt{time\_sd}\cdot\delta_t+\texttt{idio\_sd}\cdot\nu_{it}$ (the variance components are knobs), where `structure` switches the firm and/or time component on or off; a `fit_ses(df)` function that fits one pooled OLS and returns the SE of $x$ under five methods (`OLS`, `White`/HC1, `Cluster firm`, `Cluster time`, `Two-way`); and a `monte_carlo(structure, reps, ...)` driver that repeats this over many simulated panels.

**(a) (5 pts)** **Write the design in Petersen's own terms.** In a short paragraph, state (i) what plays the role of the "known truth" here and why a simulation — not real data — is the only way to get it; (ii) the two numbers you compare for each method to judge it (define the **true SE** as the standard deviation of $\hat\beta_1$ *across the simulated panels*, and the **mean estimated SE** as the average of that method's reported SE); and (iii) the third diagnostic, **coverage**, and exactly how you compute it from the $S$ panels (for each panel form the 95% interval $\hat\beta_1\pm1.96\,\widehat{\operatorname{se}}$ and count the fraction containing $\beta=0.30$). State what "method M is correct" looks like in all three numbers at once.

**(b) (4 pts)** **Specify Experiment 1 (firm effect).** Name the exact knob settings you would pass to reproduce Petersen's headline firm-effect result: which `structure`, which variance components on or off, and — crucially, invoking the Moulton logic — why the regressor $x$ must itself carry a **persistent firm component** for the OLS SE to break. Predict the qualitative shape of the resulting table: which methods undercover, and which one recovers $\approx 0.95$ coverage.

**(c) (4 pts)** **Specify Experiment 2 (flip to a time effect) and the time-FE aside.** Say what one change flips the world from a firm effect to a time effect, and predict which method now matches the truth. Then describe the *additional* run where you add a **time fixed effect** (a dummy per year) to the regression, and state what you expect it to do to the time effect — connecting to the Ch 2.4 point that **fixed effects and clustering do different jobs** (one removes a mean, the other handles a covariance; recall Task 3 of PS 2.4).

**(d) (3 pts)** **Specify Experiment 3 (break the few-clusters case on purpose).** Starting from a world where the *correct* clustering covers $\approx 0.95$, name the single knob you would shrink to *make the correct method fail*, and predict the direction coverage moves as you shrink it (tie to Task 4). State in one sentence why "watching the correct method undercover on data whose truth you set yourself" is more convincing than reading the caveat in prose.

---

*End of PS 5.4. Solutions in `book/appendices/E-solutions-manual/E-w5-ps5.4-solutions.md`. This set is the active-replication companion to Ch 5.4 (Reader's Guide to Petersen 2009) and the direct sequel to **Week 2, Ch 2.4 §6** and **PS 2.4 Problem 6**, where you first met the firm-effect / time-effect / two-way taxonomy as a recipe. There you used the result; here you re-run the experiment that proved it. Tomorrow's paper, Bertrand–Duflo–Mullainathan (2004), is the same disease — ignored within-group serial correlation — in a difference-in-differences costume. Go run nb5.4 (Petersen clustering replication) and generate your own version of every illustrative table above.*
