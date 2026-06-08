# PS 1.1 — Conditional Probability & LIE/LTV Drills

**Course:** ASSIP 2026 · 8-Week Empirical Finance Track · Week 1 · Problem Set 1.1
**Covers:** Ch 1.1 (Joint, Conditional, and the Two Laws That Run Everything).
**Methods allowed:** only what is built through Ch 1.1 — joint/marginal/conditional distributions, the multiplication rule, independence, conditional expectation as a random variable, the Law of Iterated Expectations (LIE), and the Law of Total Variance (LTV). You will *not* need covariance algebra (Ch 1.2), sampling theory (Ch 1.3), or anything later. Where a problem says "explain," a clear sentence or two beats a wall of symbols.

**Total: 100 points.** Point values are stated per problem. Show your reasoning — a correct final number with no work earns roughly half credit, because the reasoning *is* the skill we are grading. Solutions are in Appendix E (`E-w1-ps1.1-solutions.md`); try every part before you look.

A note on the difficulty curve: Problem 1 is a warm-up you should finish in five minutes; Problems 4 and 5 are genuinely hard and are where the learning lives. Budget your time accordingly.

---

## Problem 1 — Reading a joint table (14 points)

Priya is studying flood-insurance claims. For each insured home in a coastal county she records two things in a single year:

- $Y$ = the home's flood-zone rating, coded $H$ for "high risk" and $L$ for "low risk."
- $X$ = whether the home filed a claim that year, coded $1$ for "filed a claim" and $0$ for "no claim."

Her data give the following joint distribution — each cell is the joint probability $\Pr(X = x,\, Y = y)$ that a randomly drawn insured home falls in that combination:

| | $X = 0$ (no claim) | $X = 1$ (claim) |
|---|---|---|
| **$Y = L$ (low risk)** | $0.55$ | $0.05$ |
| **$Y = H$ (high risk)** | $0.25$ | $0.15$ |

**(a) (3 pts)** Verify this is a valid joint distribution, and compute the two marginal distributions $p_Y(y)$ and $p_X(x)$.

**(b) (4 pts)** Compute the conditional distribution of $X$ given $Y = H$ — that is, $\Pr(X = 0 \mid Y = H)$ and $\Pr(X = 1 \mid Y = H)$. Confirm the two numbers sum to $1$, and state in one sentence what the claim rate is among high-risk homes.

**(c) (4 pts)** Compute $\Pr(X = 1 \mid Y = L)$, the claim rate among low-risk homes. By what factor is a high-risk home more likely to file a claim than a low-risk home? (This ratio is exactly the kind of number an insurer uses to set a premium differential.)

**(d) (3 pts)** Are $X$ and $Y$ independent? Show the single check that settles it, and say in one sentence why the answer is what an insurer would *expect*. (Reveal-the-trick reminder: independence is an *all-cells* claim, but *dis*proving it takes only one cell — you do not have to check the whole table. Find the cheapest cell that breaks the product rule and stop there.)

---

## Problem 2 — Maya, reverse conditioning, and a fair-lending audit (18 points)

Maya is auditing a bank's small-business loan model for fair lending. The model assigns each applicant a binary flag $F$: $F = 1$ means "flagged as high default risk" (loan likely denied), $F = 0$ means "not flagged." Separately, each applicant truly either defaults or does not over the loan term; let $D = 1$ if the applicant *would* default and $D = 0$ if they would repay. From a large validation sample the bank reports:

- The true default rate in the applicant pool is $\Pr(D = 1) = 0.10$.
- Among applicants who *would* default, the model flags $\Pr(F = 1 \mid D = 1) = 0.80$ (it catches $80\%$ of true defaulters).
- Among applicants who *would* repay, the model still flags $\Pr(F = 1 \mid D = 0) = 0.15$ (a $15\%$ false-flag rate on good borrowers).

**(a) (4 pts)** Find the overall fraction of applicants the model flags, $\Pr(F = 1)$. (Hint: a flagged applicant is *either* a true defaulter who got caught *or* a good borrower who got falsely flagged. Use the multiplication rule on each piece, then add — this is the marginalization-by-conditioning move from §1–§2 of the chapter.)

**(b) (6 pts)** Maya's real question is the *reverse* of what the bank reported. The bank told her $\Pr(F = 1 \mid D = 1)$ — flag given default. Maya wants $\Pr(D = 1 \mid F = 1)$ — given that an applicant was flagged, what is the probability they truly would have defaulted? Compute it. Show the reverse-conditioning step explicitly (joint over the relevant marginal).

**(c) (4 pts)** Interpret the gap. The model "catches $80\%$ of defaulters," yet the number you found in (b) is much smaller than $80\%$. Explain in two or three sentences *why* these two numbers are so different, and which one a denied applicant should care about.

**(d) (4 pts)** Now compute $\Pr(D = 1 \mid F = 0)$ — the true default rate among applicants the model did *not* flag. In one sentence, what does comparing this to the pool's base rate of $0.10$ tell Maya about whether the flag carries real information?

---

## Problem 3 — The Law of Iterated Expectations, proved then applied (16 points)

**(a) (8 pts)** Prove the Law of Iterated Expectations for discrete random variables: for any $X$ with a finite mean and any discrete $Y$,
$$
\mathbb{E}\big[\mathbb{E}[X \mid Y]\big] = \mathbb{E}[X].
$$
Write the proof in your own steps. You may use, without re-deriving them, the definition of conditional expectation $\mathbb{E}[X \mid Y = y] = \sum_x x\, p_{X\mid Y}(x \mid y)$, the multiplication rule $p(x,y) = p_{X\mid Y}(x\mid y)\, p_Y(y)$, and marginalization $\sum_y p(x,y) = p_X(x)$. State clearly at each step which of these you are invoking. The whole proof is three or four honest lines; the grading is on whether each line *names* the rule that justifies it, not on length. Finally, state in one sentence where the assumption "$X$ has a finite mean" actually gets used — there is exactly one step that silently relies on it.

**(b) (8 pts)** Now *apply* it. Devon tracks the daily return $X$ (in percent) on a crypto token. The return depends on whether the day sees a major exchange-listing announcement, a rare event. Let $Y = 1$ if there is an announcement that day and $Y = 0$ otherwise, with $\Pr(Y = 1) = 0.04$. Devon estimates the conditional means
$$
\mathbb{E}[X \mid Y = 1] = 12.0\%, \qquad \mathbb{E}[X \mid Y = 0] = -0.25\%.
$$
Use LIE to find the unconditional expected daily return $\mathbb{E}[X]$. Then explain in one sentence why the unconditional mean is so close to the boring non-announcement number despite the huge announcement-day return — i.e., name the mechanism in the LIE formula that produces this.

---

## Problem 4 — Sam's regimes and the Law of Total Variance (22 points)

Sam refines the momentum strategy from the chapter and re-estimates the joint distribution of the daily portfolio return $X$ (in percent) and the market regime $Y$. The new table has **three** return values and **two** regimes:

| | $X = -3\%$ | $X = 0\%$ | $X = +3\%$ | row total |
|---|---|---|---|---|
| **$Y = 1$ (calm)** | $0.04$ | $0.16$ | $0.40$ | $0.60$ |
| **$Y = 2$ (stormy)** | $0.24$ | $0.10$ | $0.06$ | $0.40$ |

**(a) (4 pts)** Compute the conditional mean return in each regime, $\mathbb{E}[X \mid Y = 1]$ and $\mathbb{E}[X \mid Y = 2]$. Then write out the conditional-expectation random variable $\mathbb{E}[X \mid Y]$ explicitly (which value it takes, with what probability).

**(b) (5 pts)** Compute the within-regime variances $\operatorname{Var}(X \mid Y = 1)$ and $\operatorname{Var}(X \mid Y = 2)$, and from them the within-regime piece $\mathbb{E}\big[\operatorname{Var}(X \mid Y)\big]$.

**(c) (4 pts)** Compute the across-regime piece $\operatorname{Var}\big(\mathbb{E}[X \mid Y]\big)$.

**(d) (4 pts)** Add the two pieces, then verify your answer by computing $\operatorname{Var}(X)$ directly from the marginal distribution of $X$. The two routes must agree exactly; if they do not, find your arithmetic error before reading on.

**(e) (5 pts)** Report the fraction of total variance that is *across-regime*. Compare it to the chapter's strategy, where the across-regime share was about $19\%$. In two or three sentences, tell Sam what this new number means for whether **regime forecasting** (predicting calm vs. stormy in advance) is worth the effort for *this* strategy versus the chapter's.

---

## Problem 5 — Uncorrelated but dependent (18 points)

The chapter warns (§3) that "uncorrelated" is strictly weaker than "independent": zero covariance only rules out *linear* association, not all association. This problem makes you build the counterexample yourself and see the trap from both directions. You may use the fact that $\operatorname{Cov}(X, Y) = \mathbb{E}[XY] - \mathbb{E}[X]\,\mathbb{E}[Y]$; everything else uses only Ch 1.1 tools.

Devon models a "volatility-harvesting" position whose daily P&L $X$ depends on the size of the market move but not its direction. Let $Y$ be the signed market move, taking the three values $-1$, $0$, $+1$ each with probability $\tfrac{1}{3}$, and let the position's payoff be $X = Y^2$ (so $X = 1$ on a big move either way, $X = 0$ on a flat day).

**(a) (3 pts)** Write down the conditional distribution of $X$ given each value of $Y$. Use it to argue in one sentence that $X$ and $Y$ are **dependent** — i.e., that knowing $Y$ changes what you know about $X$. (You should not need any arithmetic beyond reading off values.)

**(b) (6 pts)** Now show they are **uncorrelated**: compute $\mathbb{E}[Y]$, $\mathbb{E}[XY]$, and hence $\operatorname{Cov}(X, Y)$, and confirm it is zero. (Hint: $XY = Y^3$. Use LIE or a direct sum — your choice — but show the expectation calculation.)

**(c) (5 pts)** This is the part most students get wrong, so think before writing. Reconsider the claim "$X$ and $Y$ are uncorrelated." Compute $\mathbb{E}[X \mid Y = y]$ for each $y$ and write out the random variable $\mathbb{E}[X \mid Y]$. Is $\mathbb{E}[X \mid Y]$ equal to the constant $\mathbb{E}[X]$? What does your answer say about whether "$\operatorname{Cov}(X,Y) = 0$" and "$\mathbb{E}[X \mid Y] = \mathbb{E}[X]$" are the same condition? (They are not — explain the difference in plain words.)

**(d) (4 pts)** Tie it to Sam. In the chapter's regime example, $\operatorname{Cov}(\text{return}, \text{regime})$ happened to be nonzero. Suppose a *different* strategy had $\operatorname{Cov}(X, Y) = 0$ between return and a regime indicator. Using what you just learned, is Sam safe to conclude "the regime is useless for forecasting my return"? Answer yes/no and give the one-sentence reason, referencing the difference between parts (b) and (c).

---

## Problem 6 — Simulation design (pointing to nb1.1) (12 points)

You will *not* write working code here — you will *design* the experiment that `notebooks/week-01/nb1.1` carries out, in enough detail that a classmate could implement it. Use Sam's three-value table from Problem 4 as the universe. The point of this problem is that a simulation is only trustworthy if you can state, in advance, exactly what it should produce; here you have an analytic answer (Problem 4) to check the code against, which is the gold standard for debugging a sampler.

**(a) (5 pts)** Describe, step by step in plain English (pseudocode is fine), how to draw $N$ independent samples of the pair $(X, Y)$ from Problem 4's joint distribution using only a uniform random-number generator. Be explicit about how you turn the six joint probabilities into a sampling rule. (Hint: flatten the table into six outcomes with probabilities summing to $1$, take the cumulative sums, draw a uniform $u \in [0,1)$, and pick the first outcome whose cumulative probability exceeds $u$.)

**(b) (4 pts)** Given a simulated sample of $N$ pairs, describe how you would *estimate* the within-regime piece $\mathbb{E}[\operatorname{Var}(X\mid Y)]$ and the across-regime piece $\operatorname{Var}(\mathbb{E}[X\mid Y])$ from the data alone (i.e., grouping by the realized regime), and what single equation you would check to confirm the Law of Total Variance held in your sample.

**(c) (3 pts)** As $N$ grows from $10^2$ to $10^6$, what do you expect to happen to the gap between (i) your simulated within-plus-across sum and (ii) the exact $\operatorname{Var}(X)$ you computed in Problem 4(d)? Will it ever be *exactly* zero at finite $N$? Answer in two sentences, and name the qualitative reason (you do not yet have the formal tool — that is Ch 1.3 — but state the intuition).
