# PS 2.2 — Gauss–Markov: Breaking the Contract on Purpose

**Course:** 8-Week Empirical Finance Camp · Week 2 · Problem Set 2.2
**Covers:** Ch 2.2 (the five classical assumptions as testable claims; the unbiasedness proof off the contamination identity $\hat{\boldsymbol{\beta}} = \boldsymbol{\beta} + (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\boldsymbol{\varepsilon}$; the variance formula $\sigma^2(\mathbf{X}'\mathbf{X})^{-1}$ and its scalar shadow $\sigma^2 / \sum(x_i-\bar x)^2$; BLUE / efficiency; the unbiased-versus-consistent distinction).
**Total:** 110 points across 6 problems, escalating in difficulty. Each problem is self-contained.

**Ground rules.** Use only tools through Chapter 2.2. You may *cite* — but need not re-derive — results flagged for later chapters: omitted-variable bias is quantified in Ch 2.5, robust/clustered standard errors in Ch 2.4, and functional-form fixes (logs, polynomials, multicollinearity) in Ch 2.3. Take expectations conditional on $\mathbf{X}$ unless told otherwise, and treat $(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'$ as a constant matrix once $\mathbf{X}$ is fixed. Notation follows CONVENTIONS §3: scalars italic, vectors bold lowercase, matrices bold uppercase, $\hat{\,\cdot\,}$ for estimates. Show every step; a correct conclusion with no reasoning earns little. Throughout, rates are in percentage points and income in thousands of dollars unless stated.

---

## Problem 1 — Read the contract back to me (12 points)

The Gauss–Markov theorem is a contract with five clauses. For each of the **five assumptions** of Chapter 2.2, do all three of the following in a sentence or two each. Be precise; this is the vocabulary the rest of the week is built on.

**(a) [6 pts]** Name the assumption and state it as a *claim about a data-generating process* (not as a ritual). For Assumptions 3 and 4, write the defining equation in expectation/variance notation.

**(b) [4 pts]** For each assumption, state in one phrase *what you would see go wrong* if it failed — and crucially, classify the damage as either a **bias problem** (the estimate $\hat{\boldsymbol{\beta}}$ no longer aims at $\boldsymbol{\beta}$) or a **precision/standard-error problem** (the estimate is still aimed true but your reported uncertainty is wrong or no longer minimal). One of the five is neither — it is a *mechanical* failure that makes the estimator undefined rather than merely biased; flag which one and why.

**(c) [2 pts]** State the three-tier summary from the chapter: which assumptions buy unbiasedness, which additional one buys BLUE, and which additional one buys exact small-sample inference. Note explicitly which single assumption is *not* needed for Gauss–Markov at all.

---

## Problem 2 — Prove OLS is unbiased, and find the exact line that breaks (16 points)

Maya runs $\mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\varepsilon}$ on her loan data and computes $\hat{\boldsymbol{\beta}} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$.

**(a) [7 pts]** Starting from the OLS formula and substituting the true model, derive the **contamination identity**
$$
\hat{\boldsymbol{\beta}} = \boldsymbol{\beta} + (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\boldsymbol{\varepsilon}.
$$
Justify each algebraic move, and say in one sentence which two assumptions you used *silently* just to write down this line (i.e., before taking any expectation).

**(b) [5 pts]** Take the conditional expectation $\mathbb{E}[\hat{\boldsymbol{\beta}}\mid\mathbf{X}]$ and show it equals $\boldsymbol{\beta}$. State exactly where Assumption 3 enters, and explain why conditioning on $\mathbf{X}$ is what lets you pull the matrix $(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'$ outside the expectation. Then extend to the *unconditional* result $\mathbb{E}[\hat{\boldsymbol{\beta}}] = \boldsymbol{\beta}$ using the law of total expectation.

**(c) [4 pts]** Two stress tests of the proof. (i) Maya's errors turn out to be wildly heteroskedastic — the spread of $\varepsilon$ is huge for low-income borrowers and tiny for high earners. Does your part-(b) conclusion still hold? Point to the precise step that does or does not use the variance of $\boldsymbol{\varepsilon}$. (ii) Maya instead discovers that income is correlated with an omitted creditworthiness variable, so $\mathbb{E}[\boldsymbol{\varepsilon}\mid\mathbf{X}] \neq \mathbf{0}$. Write the resulting expression for $\mathbb{E}[\hat{\boldsymbol{\beta}}\mid\mathbf{X}]$, identify the leftover term as the thing Ch 2.5 will name, and explain in one sentence why "the math didn't break, the assumption did."

---

## Problem 3 — The variance formula, by hand, and why spread is precision (20 points)

Specialize to simple regression: $\mathbf{X}$ is an intercept plus one regressor (income), so $\hat{\beta}_1$ is the slope. The chapter states that the bottom-right entry of $\sigma^2(\mathbf{X}'\mathbf{X})^{-1}$ is
$$
\operatorname{Var}(\hat{\beta}_1\mid\mathbf{X}) = \frac{\sigma^2}{\sum_{i=1}^N (x_i - \bar{x})^2} = \frac{\sigma^2}{(N-1)\,s_x^2}.
$$

**(a) [6 pts]** Derive this scalar formula from $\operatorname{Var}(\hat{\boldsymbol{\beta}}\mid\mathbf{X}) = \sigma^2(\mathbf{X}'\mathbf{X})^{-1}$. Write out the $2\times 2$ matrix $\mathbf{X}'\mathbf{X}$ in terms of $N$, $\sum x_i$, and $\sum x_i^2$; invert it using the $2\times2$ inverse rule (one over the determinant times the adjugate); take the bottom-right entry; and show the determinant simplifies to $N\sum(x_i-\bar x)^2$, so that the entry collapses to the boxed result. (Hint: $\sum x_i^2 - N\bar x^2 = \sum(x_i-\bar x)^2$.)

**(b) [6 pts]** Maya has $N = 250$ loans, residual standard deviation $\sigma = 1.2$ percentage points, and a sample income standard deviation $s_x = 20$. Compute $\operatorname{Var}(\hat{\beta}_1)$ and the standard error $\operatorname{se}(\hat{\beta}_1) = \sqrt{\operatorname{Var}(\hat{\beta}_1)}$. Report the standard error to four significant figures.

**(c) [4 pts]** Suppose Maya could instead draw a sample in which incomes were *twice as spread out* ($s_x = 40$), holding $N$ and $\sigma$ fixed. What happens to $\operatorname{Var}(\hat{\beta}_1)$ and to $\operatorname{se}(\hat{\beta}_1)$? State the exact multiplicative factors. Then explain in one sentence why the chapter calls regressor spread "the multivariate version of sample size" — i.e., what change in $N$ alone would have bought the same shrinkage in the standard error?

**(d) [4 pts]** A rival researcher brags that he has $N = 2{,}500$ loans — ten times Maya's sample — but he drew them all from a single narrow income band, with $s_x = 4$. Using the formula, compute his $\operatorname{se}(\hat{\beta}_1)$ and compare it to Maya's from part (b). Who estimates the income–rate slope more precisely, despite the smaller sample? State the one-sentence moral about *what kind of data* buys precision for a slope.

---

## Problem 4 — Why "Best" means minimum variance among a club (16 points)

A classmate, Sam, reads the four letters **BLUE** and concludes: "OLS is the Best Linear Unbiased Estimator, so it's simply the best estimator there is — nothing can beat it." Your job is to dismantle this cleanly using only Chapter 2.2.

**(a) [4 pts]** Unpack the word **Best** precisely. In the Gauss–Markov theorem, "best" is a claim about *which* numerical property of an estimator, compared against *which* set of rival estimators? State the comparison class in full (the two adjectives that define club membership), and explain why "best" is "a technical word, not a compliment."

**(b) [5 pts]** Give **two distinct reasons** Sam's claim overstates the theorem. The first must be about the *class*: name a kind of estimator that lives *outside* the linear-unbiased club and can sometimes beat OLS, and say what you must give up to use it. The second must be about an *assumption*: name the assumption whose failure revokes the "**B**" (efficiency) while *leaving $\hat{\boldsymbol{\beta}}$ unbiased*, name the better-than-OLS recipe that then exists, and name the later chapter that handles the fallout.

**(c) [5 pts]** Here is the load-bearing intuition. The chapter sketches that any rival linear unbiased estimator has variance
$$
\operatorname{Var}(\tilde{\boldsymbol{\beta}}\mid\mathbf{X}) = \underbrace{\sigma^2(\mathbf{X}'\mathbf{X})^{-1}}_{\text{OLS variance}} + \underbrace{\sigma^2\mathbf{D}\mathbf{D}'}_{\text{extra}}.
$$
Explain (i) why the extra term $\sigma^2\mathbf{D}\mathbf{D}'$ can **never be negative**, and what the *only* way to make it exactly zero is; (ii) why this argument has the **same shape** as the bias–variance decomposition from Chapter 1.3 (a target term plus a non-negative penalty, minimized by killing the penalty); and (iii) which assumption let us write $\operatorname{Var}(\boldsymbol{\varepsilon}\mid\mathbf{X}) = \sigma^2\mathbf{I}$ so the cross-terms cancelled — i.e., the one assumption doing the real work in the proof.

**(d) [2 pts]** True or false, with one sentence of justification: "Because OLS is BLUE, a researcher with a correctly specified model can never improve on OLS's precision by accepting a little bias." (Think about what "U" excludes.)

---

## Problem 5 — Unbiased vs. consistent: build one of each (18 points)

These two virtues are independent, and confusing them is, per the chapter, "the most expensive conceptual error in all of applied work." Make the distinction concrete by *constructing* estimators.

**(a) [7 pts]** **Unbiased but inconsistent.** Define the estimator $\hat{\beta}_1^{\text{(5)}}$ that throws away all but the first 5 loans and runs OLS on just those (assume those 5 have income spread, so the slope is defined). (i) Argue that it is **unbiased** for $\beta_1$ — point to which step of the Problem-2 proof still applies to a sample of size 5. (ii) Argue that it is **inconsistent** — write its variance using the Problem-3 formula restricted to the 5 retained observations, and explain why that variance does *not* shrink to zero as the full sample $N \to \infty$. (iii) State in one sentence what its sampling distribution looks like as $N \to \infty$: where is it centered, and does it collapse to a point?

**(b) [7 pts]** **Biased but consistent.** Consider the deliberately damaged estimator $\check{\beta}_1 = \big(1 + \tfrac{10}{N}\big)\,\hat{\beta}_1$, where $\hat{\beta}_1$ is the usual full-sample OLS slope (unbiased, consistent). (i) Compute $\mathbb{E}[\check{\beta}_1\mid\mathbf{X}]$ and show it is **biased** at every finite $N$; give the bias as a formula in $N$ and $\beta_1$, and evaluate it at $N = 50$. (ii) Argue it is nonetheless **consistent**: explain what happens to the multiplier $1 + 10/N$ as $N \to \infty$ and why that, combined with $\hat{\beta}_1 \xrightarrow{p} \beta_1$, delivers $\check{\beta}_1 \xrightarrow{p} \beta_1$. (iii) Evaluate the multiplier at $N = 50$ and at $N = 100{,}000$ to show the bias melting away.

**(c) [4 pts]** A researcher has $100{,}000$ loans and must choose between $\hat{\beta}_1^{\text{(5)}}$ (part a) and $\check{\beta}_1$ (part b). Which should she pick, and why? Frame your answer in terms of where each estimator's sampling distribution sits *at that sample size* — center and spread — and connect it to the chapter's slogan that "a biased-but-consistent estimator beats an unbiased-but-inconsistent one in any large dataset, every time."

---

## Problem 6 — Diagnose the patient: bias or standard errors? (28 points)

For each of the four scenarios below, a junior analyst has run a regression and is worried. Your task in **each case**: (1) name the *single* classical assumption most directly at stake; (2) classify the problem as a **bias problem** (the point estimate is aimed at the wrong target) or a **standard-error / efficiency problem** (the point estimate is fine but the reported uncertainty or efficiency is compromised); (3) say in one sentence whether **collecting more data fixes it**; and (4) name the later chapter that addresses it. Then answer the extra computation where asked.

**(a) [8 pts] — The omitted variable (Devon).** Devon regresses a crypto token's daily return on a single "social-media buzz" score, getting a strongly significant coefficient. But buzz is highly correlated with overall market sentiment, which he left out, and market sentiment independently drives returns. Diagnose using (1)–(4). Then the computation: in the spirit of the chapter's "number that should frighten you," suppose the *true direct* effect of buzz on returns, holding sentiment fixed, is **zero** ($\beta_{\text{buzz}} = 0$). The omitted sentiment variable has a direct effect of $-0.6$ on returns per unit, and the slope from regressing sentiment on buzz (the "$\delta$" linking the omitted to the included regressor) is $0.7$. Using the heuristic that the short-regression slope tends toward $\beta_{\text{buzz}} + (\text{effect of sentiment}) \times \delta$, compute the value Devon's coefficient settles on. Is it zero? What does running the regression on $10\times$ more days do to this number and to its standard error? (You may *use* the OVB direction result; Ch 2.5 derives it.)

**(b) [8 pts] — The fan-shaped residuals (Maya).** Maya plots her loan-rate residuals against income and sees a clear fan: wide scatter at low incomes, tight scatter at high incomes. Diagnose using (1)–(4). Then explain, in two or three sentences and pointing to the relevant step of the Problem-2 unbiasedness proof, **why this does not bias $\hat{\beta}_1$** — i.e., why $\hat{\beta}_1$ still aims at the truth — even though it makes the classical standard-error formula $\sigma^2(\mathbf{X}'\mathbf{X})^{-1}$ untrustworthy. Name the specific flavor of standard error (from CONVENTIONS §3 / Ch 2.4) that repairs the reported uncertainty.

**(c) [6 pts] — The duplicated column (Sam).** Sam builds a design matrix that includes income measured in dollars *and* income measured in thousands of dollars as two separate columns, then is baffled when the software errors out or silently drops a regressor. Diagnose using (1)–(4) — but note this case is special: classify it not as bias-vs-SE but as the *third category* from Problem 1. Explain precisely why $(\mathbf{X}'\mathbf{X})^{-1}$ fails to exist here (connect to full column rank), and why this is "undefined, like dividing by zero" rather than "biased." State whether more data fixes it and why not.

**(d) [6 pts] — The clustered loans (Priya).** Priya's insurance-claim sample contains many policies from the *same* few regions; claims within a region move together (a regional flood hits them all at once), so the errors are correlated across observations within a cluster. Diagnose using (1)–(4). Identify *which half* of Assumption 4 is violated — the equal-variance (homoskedasticity) half or the off-diagonal-zeros (uncorrelated-errors) half — and explain in one sentence why ordinary standard errors will be *too small* (overstating precision) if she ignores the clustering. Name the standard-error flavor that fixes it.

---

*Solutions: see `book/appendices/E-solutions-manual/E-w2-ps2.2-solutions.md`.*
