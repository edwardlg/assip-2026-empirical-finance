# Problem Set 3.4 — Instrumental Variables: 2SLS Derivation and Weak-IV Diagnostics

*Covers Ch 3.4. Methods allowed: everything through Ch 3.4 — the two validity conditions (relevance $\operatorname{Cov}(Z,D)\neq 0$ and exclusion $\operatorname{Cov}(Z,\varepsilon)=0$); the Wald estimator $\hat\beta_1^{\text{Wald}}=(\overline Y_{Z=1}-\overline Y_{Z=0})/(\overline D_{Z=1}-\overline D_{Z=0})$; the first stage, reduced form, and 2SLS triple; the FWL-with-an-instrument slope $\hat\beta_1^{\text{2SLS}}=\operatorname{Cov}(\tilde Z,\tilde Y)/\operatorname{Cov}(\tilde Z,\tilde D)$; the LATE theorem and the four compliance types under monotonicity; the first-stage F and the weak-IV bias approximation $(\mathbb{E}[\hat\beta^{\text{2SLS}}]-\beta_1)/(\mathbb{E}[\hat\beta^{\text{OLS}}]-\beta_1)\approx 1/F$. You may treat OLS, FWL/residualization (Ch 2.3), and the bias–consistency ledger (Ch 2.5) as known. Show your reasoning; a boxed number with no argument earns no credit, and any time you invoke a condition you must **name it** — "relevance" or "exclusion" — never just "the assumption."*

**Total: 100 points.** Six problems, escalating. Problem 1 is conceptual (state relevance and exclusion, classify which is testable); Problem 2 computes a Wald estimator from a $2\times 2$ table; Problem 3 derives the 2SLS slope as a covariance ratio in the FWL-with-an-instrument world; Problem 4 is a first-stage-F / Stock–Yogo strength diagnostic; Problem 5 is a LATE/compliers taxonomy problem; Problem 6 is the weak-instrument bias-toward-OLS calculation built on $1/F$.

One idea runs through every problem, so hold it from the start. IV reads a causal effect off a ratio — *how the outcome moves with the instrument* divided by *how the treatment moves with the instrument*. Relevance is the promise that the denominator is not zero, and it is **testable** because both $Z$ and $D$ are observed. Exclusion is the promise that the only road from $Z$ to $Y$ runs through $D$, and it is **untestable** because it is a statement about the unobserved error $\varepsilon$. Every problem below is, at bottom, about that asymmetry: what you can verify in data versus what you must argue from the design.

---

## Problem 1 — State the two conditions; classify which is testable (12 points)

Priya studies whether buying *parametric flood insurance* (a policy that pays out automatically when rainfall crosses a threshold, $D_i=1$) lowers a household's financial distress after a storm ($Y_i$, a distress index, lower is better). Take-up is endogenous: households who buy are systematically more risk-aware and better-resourced, and risk-awareness sits unmeasured in the error $\varepsilon_i$. She proposes as an instrument $Z_i=$ whether the household was **randomly assigned to a door-to-door insurance-education visit** during a pilot program.

**(a) (3 pts)** Write Priya's structural equation in the notation of Ch 3.4, identify which regressor is endogenous, and say in one sentence why $\operatorname{Cov}(D_i,\varepsilon_i)\neq 0$ here (name the confounder).

**(b) (3 pts)** State the **relevance** condition for $Z_i$ both as a covariance statement and in plain words, and describe exactly the regression Priya runs to test it and what coefficient she hopes to see.

**(c) (3 pts)** State the **exclusion** condition for $Z_i$ both as a covariance statement and in plain words. Then give one concrete, specific channel through which the education visit might violate exclusion — a path from $Z_i$ to $Y_i$ that does *not* pass through buying the policy.

**(d) (3 pts)** One of your two conditions can be confirmed in the data and one can never be. Name which is which, and explain in two sentences *why* the untestable one is untestable — what object would you need to observe, and why don't you have it?

---

## Problem 2 — The Wald estimator from a $2\times 2$ table (15 points)

Devon's brokerage ran a randomized promotion: a subset of new users was randomly offered a one-time fee rebate for opening a diversified index position ($Z_i=1$ if offered the rebate, $0$ otherwise). Let $D_i=1$ if the user actually opened a diversified position, and let $Y_i$ be the change in the annualized volatility of the user's portfolio over the next year, in volatility points (lower is better — diversification should *reduce* volatility). The randomized offer is the instrument. The data:

| Group | $N$ | Share opening position ($\overline D$) | Mean volatility change ($\overline Y$, vol pts) |
|---|---:|---:|---:|
| Offered rebate ($Z=1$) | $500$ | $0.50$ | $-4.5$ |
| Not offered ($Z=0$) | $500$ | $0.20$ | $-1.5$ |

**(a) (3 pts)** Compute the **first stage** $\overline D_{Z=1}-\overline D_{Z=0}$ and the **reduced form** $\overline Y_{Z=1}-\overline Y_{Z=0}$. Say in one sentence what each one measures, naming the relevance condition where it applies.

**(b) (4 pts)** Compute the **Wald estimate** $\hat\beta_1^{\text{Wald}}$. Interpret the number in Devon's units: what does it claim the diversified position does to portfolio volatility, and *for whom*?

**(c) (3 pts)** Devon's friend says, "Just compare the volatility change of users who opened a position to those who didn't — that's the effect." Compute *nothing*; instead explain in two or three sentences why that naive comparison is biased and why the Wald estimator avoids the bias. Name the condition (relevance or exclusion) that makes the offered-vs-not comparison clean.

**(d) (3 pts)** From the table, how many users in each group actually opened a position (give the counts)? Then state what fraction of the *whole* population are compliers, and justify why the first stage equals the complier share here.

**(e) (2 pts)** Suppose a regulator later reveals that the rebate email also contained a paragraph of generic "diversify your holdings" advice that some recipients followed *without* opening a position through Devon. Which validity condition is now in doubt, and which direction does it likely push $\hat\beta_1^{\text{Wald}}$ (toward zero or away)? One sentence of reasoning.

---

## Problem 3 — 2SLS as FWL-with-an-instrument: the covariance ratio (20 points)

This problem derives and then evaluates the central 2SLS formula from §5 of the chapter,
$$
\hat\beta_1^{\text{2SLS}}=\frac{\operatorname{Cov}(\tilde Z,\tilde Y)}{\operatorname{Cov}(\tilde Z,\tilde D)},
$$
where $\tilde Y,\tilde D,\tilde Z$ are the FWL-residualized versions of outcome, treatment, and instrument — each one with the exogenous controls $\mathbf X$ partialled out, exactly as in Ch 2.3.

**(a) (5 pts)** Derive the formula. Start from the just-identified structural equation $\tilde Y_i=\beta_1\tilde D_i+\tilde\varepsilon_i$ (controls already swept out, so no intercept). Multiply through by $\tilde Z_i$, take expectations, and impose the **exclusion** condition $\operatorname{Cov}(\tilde Z,\tilde\varepsilon)=0$ to solve for $\beta_1$. At which step does exclusion do its work, and at which step would the derivation collapse if **relevance** failed?

**(b) (6 pts)** Maya has a small panel where the controls have already been partialled out, leaving these residualized values for $N=5$ regions:

| $i$ | $\tilde Z_i$ | $\tilde D_i$ | $\tilde Y_i$ |
|---|---:|---:|---:|
| 1 | $-2$ | $-1$ | $+2$ |
| 2 | $-1$ | $0$ | $+2$ |
| 3 | $0$ | $0$ | $0$ |
| 4 | $1$ | $0$ | $-2$ |
| 5 | $2$ | $1$ | $-2$ |

(Each column has mean zero, as residualized variables must.) Compute $\sum_i \tilde Z_i\tilde D_i$ and $\sum_i \tilde Z_i\tilde Y_i$, then the 2SLS slope. (Because the covariance is each sum divided by the same $N$, the $N$'s cancel and you may use the raw sums.)

**(c) (4 pts)** Now compute what OLS of $\tilde Y$ on $\tilde D$ would give: the slope $\sum_i \tilde D_i\tilde Y_i/\sum_i \tilde D_i^2$. Report both slopes. They differ — state which one is attenuated toward zero, and explain in one sentence why a gap between the OLS and 2SLS slopes is the *signature* of endogeneity (connect to the OLS bias term from §2 of the chapter).

**(d) (3 pts)** Explain why the controls $\mathbf X$ must be partialled out of **all three** of $Y$, $D$, and $Z$ — not just $Y$ and $D$ — for this formula to be valid. What goes wrong (which condition is silently broken) if you forget to residualize $Z$?

**(e) (2 pts)** State the OLS special case in one line: which choice of instrument $Z$ turns the 2SLS covariance ratio into the ordinary OLS slope, and why is that choice exactly the move that fails under endogeneity?

---

## Problem 4 — First-stage F and the Stock–Yogo bar (16 points)

Leah instruments a firm's R&D intensity ($D$) with a plausibly-exogenous shifter $Z$ (a quasi-random change in a federal R&D tax credit that hit some states and not others). With a single instrument, the first-stage F-statistic is just the squared t-statistic on $Z$ in the first-stage regression of $D$ on $Z$ and controls.

**(a) (3 pts)** Leah's first stage gives $\hat\pi_1=0.30$ with standard error $0.05$. Compute the t-statistic on $Z$ and the first-stage F. State the relevance condition and say whether this instrument clears the famous "$F>10$" bar.

**(b) (4 pts)** Explain precisely what question Stock and Yogo (2005) answered to *produce* the number $10$. What guarantee does clearing their critical value buy you — about bias, and relative to what benchmark? (One or two sentences; name the benchmark explicitly.)

**(c) (4 pts)** A second analyst on the team reports a first stage with $\hat\pi_1=0.08$, standard error $0.05$. Compute that t-statistic and F. Is this instrument strong? In one sentence, state the consequence for the 2SLS estimate that you will quantify in Problem 6.

**(d) (5 pts)** Leah's data are clustered by state, and her first-stage errors are heteroskedastic. Give **three** reasons from the chapter why "$F>10$" is, in her setting, "a smoke alarm, not a certificate." For one of the three, name the statistic she should report instead and the authors who derived it.

---

## Problem 5 — LATE and the four compliance types (18 points)

Return to Devon's randomized rebate offer from Problem 2 ($Z=$ offered, $D=$ opened a diversified position). This problem is about *whose* effect the Wald/2SLS estimate captures.

**(a) (6 pts)** Define the four compliance types using the potential-treatment notation $D_i(0),D_i(1)$ from the chapter (the treatment a user would take if not offered / if offered). Fill in a table giving, for each of **never-taker, always-taker, complier, defier**, the values of $D_i(0)$ and $D_i(1)$, and attach a one-line Devon-context description to each (who they are among brokerage users).

**(b) (3 pts)** State the **monotonicity** assumption formally (in terms of $D_i(1)$ and $D_i(0)$) and in words. Which one of the four types does it assume out of existence, and why is that assumption needed for the LATE theorem to hold?

**(c) (4 pts)** Explain why the instrument is *blind* to the treatment effect of always-takers and never-takers. Tie this directly to the first stage: how much does each of those two types contribute to $\overline D_{Z=1}-\overline D_{Z=0}$, and what does that imply about whether their effect can appear in the Wald numerator?

**(d) (3 pts)** State the Imbens–Angrist (1994) LATE theorem in one line (what the IV estimand equals, and under which named assumptions). Then say in one sentence why two *different* valid instruments for the same treatment $D$ can produce two *different* LATEs, with neither being wrong.

**(e) (2 pts)** Devon's compliance fraction (first stage) was $0.30$. A policymaker wants the effect of diversification on the users who will *never* diversify regardless of any nudge, to justify a *mandate*. Can Devon's IV answer that question? Name the type the policymaker cares about and explain in one sentence why no voluntary-uptake instrument can speak to them.

---

## Problem 6 — Weak instruments: the bias-toward-OLS calculation (19 points)

This problem makes the central weak-IV pathology of §8 quantitative using the approximation
$$
\frac{\mathbb{E}[\hat\beta^{\text{2SLS}}]-\beta_1}{\mathbb{E}[\hat\beta^{\text{OLS}}]-\beta_1}\approx \frac{1}{F},
$$
where $F$ is the population first-stage F-statistic and $\beta_1$ is the true effect.

Setup: in Leah's R&D study the true effect is $\beta_1=2.0$. Because more-innovative firms both do more R&D and have unobserved quality in the error, OLS is biased *upward* by $+1.5$ — that is, $\mathbb{E}[\hat\beta^{\text{OLS}}]=3.5$.

**(a) (4 pts)** Using the strong instrument from Problem 4(a) (so $F=36$), estimate the 2SLS bias as a fraction of the OLS bias, then the 2SLS bias in levels, then the expected 2SLS estimate $\mathbb{E}[\hat\beta^{\text{2SLS}}]$. Is 2SLS doing its job here?

**(b) (5 pts)** Now use the *weak* instrument from Problem 4(c) (so $F\approx 2.56$; use $F=2.56$). Recompute the 2SLS bias fraction, the bias in levels, and $\mathbb{E}[\hat\beta^{\text{2SLS}}]$. Compare the weak-IV 2SLS estimate to the OLS estimate of $3.5$ and to the truth of $2.0$ — which is it closer to?

**(c) (4 pts)** Explain the *mechanism* behind "bias toward OLS" in two or three sentences, using the chapter's account of the fitted treatment $\hat D_i$. Why, when $Z$ explains almost none of $D$, does $\hat D_i$ become contaminated by the very confounder you were fleeing — and what does the second-stage slope therefore drift toward?

**(d) (3 pts)** A weak instrument also has a small *exclusion* problem you cannot test: a forbidden direct effect $\operatorname{Cov}(Z,\varepsilon)=c$ for small $c>0$. The chapter says this contaminates IV as $c/\operatorname{Cov}(Z,D)$. Explain, using that ratio, why weak instruments make you *maximally* vulnerable to exactly the exclusion violations you can never detect — and why a strong first stage is therefore a buffer against an untestable assumption, not just a precision win.

**(e) (3 pts)** Synthesize Problems 4 and 6 into the chapter's "weak-IV checklist," in your own words: name the diagnostic you always report, the robust version you switch to under clustered/heteroskedastic errors and who derived it, and what you do for *inference* if the instrument turns out weak (name the method and the chapter that delivers it).

---

*End of PS 3.4. Solutions in `book/appendices/E-solutions-manual/E-w3-ps3.4-solutions.md`. This set feeds directly into Ch 3.5, which reproduces the weak-IV pathology of Problem 6 in a guided "disaster" lab and arms you with Anderson–Rubin inference that stays valid no matter how weak the instrument.*
