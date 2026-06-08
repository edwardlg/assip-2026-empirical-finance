# Mentor Session 2 — "Why your standard error is the whole ballgame."

*Week 2 live session · 60 minutes · led by Prof. Lei Gao*

Last week we asked when a number is a finding. This week you learned the machinery that
turns a regression into a claim — OLS in matrix form, the Gauss–Markov guarantees, the
Frisch–Waugh–Lovell trick, and the chapter that this session lives inside: what happens to
your standard error when the errors misbehave. Today we put the two weeks together and stare
at one uncomfortable fact. In empirical finance, computing the point estimate $\hat\beta$ is
usually the easy part. Your laptop will hand you $\hat\beta$ in milliseconds, and under
Gauss–Markov it is unbiased no matter how the errors are correlated. The *credibility* of your
work — whether a referee believes you, whether the finding survives — lives almost entirely in
the standard error. Bring the pre-read and your written answers to the three warm-ups. We will
argue, not lecture.

---

## (a) Pre-read packet — "The same β̂, two different verdicts."

*Read once before the session. One page; read it slowly.*

Here is a fact that should unsettle you a little. You can run one regression, on one dataset,
get one point estimate $\hat\beta = 0.42$, and walk away with *either* a triumphant
"significant at 1%" or a deflating "can't reject zero" — and the thing that decides which, the
entire difference between publish and not-yet, is a modeling choice you make about a matrix you
never see. That matrix is $\boldsymbol\Omega$, the variance–covariance matrix of the errors,
and the choice is how you estimate the middle of the variance sandwich
$(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\boldsymbol\Omega\mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}$.
Same $\hat\beta$. Same data. Different story about $\boldsymbol\Omega$, different t-statistic,
different conclusion. That is what we mean by "the standard error is the whole ballgame."

Recall Maya's fair-lending result from Chapter 2.4. She regressed loan interest rates on a
ZIP-code-tier indicator, controlling for credit score, loan size, and income, across
$N = 9{,}000$ loans. The coefficient came back $\hat\beta_1 = 0.42$ percentage points with a
classical standard error of $0.07$, for a t-statistic of $6.0$ — a number screaming through a
megaphone. Then her mentor asked the only question that mattered: *are those 9,000 loans really
9,000 independent pieces of evidence?* They are not. Loans cluster by lender (shared pricing
models), and by state (shared regulation and local economies). Once Maya let the errors inside
a lender be correlated — clustering — the *same* $\hat\beta_1 = 0.42$ came back with a standard
error of $0.19$ and a t-statistic of $2.2$. The estimate never moved a hair. The $0.07$ was the
lie; the $0.42$ was right the whole time.

Why does this happen, mechanically? Because the classical formula assumes
$\boldsymbol\Omega = \sigma^2\mathbf{I}$ — every error has the same variance and no two errors
are correlated. In finance that assumption is essentially always false. Errors are
heteroskedastic (bigger loans, bigger surprises), correlated within groups (firms, lenders,
states), and correlated across time (this month echoes last month). Each of those is a
different shape for $\boldsymbol\Omega$, and each makes the naive standard error wrong — almost
always too *small*, because positive within-group correlation means your observations carry less
independent information than the count $N$ suggests. The Moulton-style arithmetic from Ch 2.4 is
brutal: with clusters of size $n$ and even mild within-cluster correlation, the true variance can
be many times the naive one. A t-stat of $6.0$ can honestly be a $1.8$.

So here is the mental shift for today. Stop thinking of the standard error as a small technical
afterthought you append to a result. The standard error *is* the result, in the sense that it is
the only thing standing between "I computed a number" and "I am entitled to believe it." A
referee will spend thirty seconds on your point estimate and thirty minutes on how you computed
its uncertainty — what level you clustered at, whether you had enough clusters, whether you
confused fixed effects with clustering. Today we learn to think the way that referee thinks, by
making the same $\hat\beta$ tell two different stories and deciding which one is honest.

---

## (b) Three Socratic warm-up questions

*Come with a written sentence or two for each. No trick answers — only honest and dishonest ones.*

1. **Maya's t-statistic fell from 6.0 to 2.2 when she clustered by lender, and her coefficient
   stayed at 0.42.** A classmate concludes: "the clustering weakened her result, so the original
   result was better." In one or two sentences, say what is actually true here — what got
   *corrected* versus what got *weakened* — and why "better" is the wrong word.

2. **A friend reports: "I used robust (White / HC1) standard errors, so I'm protected against
   correlated errors."** Is that true? Name the specific kind of correlation robust SEs *do*
   handle and the specific kind they are completely blind to — and give a one-line finance
   example of the kind they miss.

3. **You have a panel of 8,000 firm-year observations but only 11 industries, and you're tempted
   to cluster by industry.** Clustering is supposed to make you more honest. Explain why, with
   only 11 clusters, clustering could actually make you *overconfident again* — i.e., why the cure
   can reintroduce the disease — and name one thing you could do about it.

---

## (c) Five-slide deck (speak-from scaffold)

**Slide 1 — "The point estimate is the easy part."**
- Under Gauss–Markov, $\hat\beta = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$ is unbiased no matter how the errors are correlated — your laptop hands it to you for free.
- What is *not* free, and not automatic, is knowing how much to trust it: that is the standard error.
- Today's claim: in empirical finance, credibility lives in the SE, not the coefficient.
- We will make one $\hat\beta$ say "significant" and "not significant" without changing a single data point.

**Slide 2 — One sandwich, many fillings (Chapter 2.4 in one breath).**
- The honest variance is always the sandwich $(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\boldsymbol\Omega\mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}$ — bread fixed, filling $\boldsymbol\Omega$ unknown.
- Classical SE is the sandwich for the fantasy diet $\boldsymbol\Omega = \sigma^2\mathbf{I}$ — equal variances, zero correlation.
- We never fix $\hat\beta$; the whole game is estimating the *middle* without pretending $\boldsymbol\Omega = \sigma^2\mathbf{I}$.
- Three real shapes for $\boldsymbol\Omega$: heteroskedastic (robust/HC), block-correlated (clustered), time-banded (HAC).

**Slide 3 — Why naive SEs lie, and which way.**
- Positive within-group correlation → each observation carries *less* independent information than the count $N$ pretends.
- Moulton arithmetic: true Var $\approx$ naive Var $\times\,[\,1 + (n-1)\rho_x\rho_\varepsilon\,]$ — the damage scales with *cluster size*.
- So the naive SE is almost always too *small*, the t-stat too *big* — overconfidence is the default failure mode.
- More observations inside existing clusters do not buy evidence; more *clusters* do.

**Slide 4 — The panel case: Petersen's taxonomy.**
- A panel (firms × years) can have a *firm effect* (errors correlated over time within a firm) and a *time effect* (common shocks across firms) at once.
- Firm effect → cluster by firm; time effect → time fixed effects or cluster by time; both → two-way cluster.
- Diagnostic you can run: cluster by firm, then by time; whichever moves the SE more off the White number points at the bigger problem.
- Fixed effects and clustering are *not* substitutes — one removes a mean, the other honors leftover co-movement. You often need both.

**Slide 5 — Thinking like the referee.**
- The empirical-spec discipline made concrete: naming your clustering level is an economic claim about where $\boldsymbol\Omega$'s off-diagonals live.
- Report the estimate, the SE flavor, the clustering level, and the cluster count — every time, no exceptions.
- "Significant" with the wrong SE is how real papers get retracted; the coefficient was never the problem.
- Your summer goal: produce standard errors you would defend to someone actively trying to break them.

---

## (d) Three "stretch" questions — connecting Week-2 SEs to real panel work

These tie the clustering and panel-dependence content from Chapter 2.4 to two real references.
The first is the paper that turned "which standard error?" from folklore into a discipline:

> Petersen, M. A. (2009), "Estimating Standard Errors in Finance Panel Data Sets," *Review of
> Financial Studies*, 22(1), 435–480.

The second is one of my own panel studies, offered as a setting where the panel-dependence and
clustering choices genuinely matter:

> Gao, Han, Kim & Pan (2024), "Overlapping institutional ownership along the supply chain and
> earnings management of supplier firms," *Journal of Corporate Finance*, 84, 102520.

For all three questions, **reason about method and inference only.** Do not invent or recite
specific reported magnitudes from either paper — the point is to practice the judgment, not to
quote results.

1. **Petersen's central diagnostic, on your own terms.** Petersen (2009) showed that finance
   papers using different standard-error methods on the *same* panel were getting standard
   errors that differed by factors of two or more, and that the dominant, most-often-ignored
   problem in corporate-finance panels is a persistent *firm effect*. (a) Explain, using the
   block-diagonal $\boldsymbol\Omega$ picture from Section 2.4.4, why clustering by firm is the
   right tool for a firm effect and why White (HC) standard errors leave you overconfident in
   its presence. (b) Petersen offers a practical way to *detect* which effect dominates without
   guessing: cluster by firm and read the SE, then cluster by time and read it again. Describe
   what you would conclude in two cases — (i) firm-clustering roughly doubles the SE but
   time-clustering barely moves it, and (ii) both move it substantially — and which estimator you
   would report in each.

2. **Common ownership along a supply chain — where do the errors hold hands?** Consider a panel
   study like Gao, Han, Kim & Pan (2024), which relates a supplier firm's *earnings management*
   (the discretionary-accruals slack with which managers shape the reported earnings number) to
   *overlapping institutional ownership along its supply chain* (shared institutional owners
   linking a supplier firm to its customers). Think carefully about the dependence structure before any number is
   computed. (a) Name at least two distinct dimensions along which the residuals could plausibly be
   correlated here — and for each, say what economic story makes the errors hold hands (think:
   the same firm observed over many years; firms tied together through a shared owner or a shared
   supply-chain linkage; a common macro or industry shock in a given year). (b) For each dimension
   you named, state the clustering or fixed-effect choice it implies, and explain in one sentence
   why *ignoring* that dimension would push the standard error in the dangerous (too-small)
   direction. (c) Why is this a setting where two-way clustering is a natural thing to at least
   consider, rather than a single clustering dimension?

3. **The few-clusters trap meets a real design.** Suppose a researcher in the supply-chain
   common-ownership setting wants to cluster at a *coarse* level — say by industry, or by
   supply-chain "block" — to capture correlation among economically linked firms, but that level
   yields only a couple dozen clusters. (a) Using the "asymptotics live in $G$, not $N$" point
   from Section 2.4.4, explain why this coarse clustering could make the cluster-robust t-test
   *anti-conservative* (overconfident) even though the intent was to be more honest. (b) Petersen
   (2009) and the few-clusters literature suggest remedies; name one (e.g., the small-sample
   $t$-distribution with $G-1$ degrees of freedom, or the wild cluster bootstrap) and say what it
   is correcting for. (c) Tie it back to the empirical-spec discipline: how would you *report* this
   tension honestly in a paper, rather than quietly picking whichever clustering level gives the
   smallest SE?

---

## (e) Post-session reflection prompt

*Write ~150–250 words after the session; we will read a few aloud next week.*

Take any regression you have run — in nb2.4, in a Week-1 notebook, or in something you find in
the wild (a working paper, a finance blog, a result a friend cites). Write the spec out in full,
the way the empirical-spec discipline demands: outcome · key regressor · controls · fixed
effects · clustering · sample · the identifying assumption in one sentence. Then interrogate the
standard error specifically. Ask: what shape is $\boldsymbol\Omega$ likely to have in this data —
heteroskedastic, clustered, time-correlated, or a panel with both a firm and a time effect? What
SE flavor was actually used, and is it the right one for that shape? If clustering was used, at
what level, how many clusters were there, and is that enough? Finish with the question that is
the whole point of today: *if I recomputed this standard error the honest way, would the
conclusion survive — and how confident am I in my answer?* You do not need to be certain. You
need to have looked at the standard error as hard as you looked at the coefficient, because that
is the half of the work where credibility is actually won or lost.
