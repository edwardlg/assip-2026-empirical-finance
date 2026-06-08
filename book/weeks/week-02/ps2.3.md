# PS 2.3 — Frisch–Waugh–Lovell: Partialling-Out by Hand

**Course:** 8-Week Empirical Finance Camp · Week 2 · Problem Set 2.3
**Covers:** Ch 2.3 (the FWL theorem; partialling-out / residualization; the residual-maker matrix $\mathbf{M}_2$ and its symmetric–idempotent–annihilating properties; "holding constant" as subtraction; demeaning as the within transformation; the dummies $\Leftrightarrow$ demeaning equivalence; the short-vs-long regression gap as a preview of omitted-variable bias). Leans on Ch 2.1 (OLS in matrix form, the hat and residual-maker matrices) for the proof problem.
**Total:** 100 points across 6 problems. Problems escalate; each is self-contained, but Problems 2 and 6 share a dataset.

**Ground rules.** Use only tools through Chapter 2.3: the OLS estimator $\hat{\boldsymbol{\beta}} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$, the residual-maker matrix $\mathbf{M} = \mathbf{I} - \mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'$ and its three properties (symmetric, idempotent, $\mathbf{M}\mathbf{X}=\mathbf{0}$), the simple-regression slope formulas $\hat{a}_1 = \operatorname{Cov}(x,z)/\operatorname{Var}(z)$ and the no-intercept slope $\sum \tilde{x}_i\tilde{y}_i / \sum \tilde{x}_i^2$, and the FWL theorem itself. No standard-error machinery (that is Ch 2.4) except where a problem explicitly asks you to *count* degrees of freedom. No omitted-variable-bias *formula* (that is Ch 2.5) — Problem 6 asks you to anticipate it, not quote it. Show every step; a bare number earns little. Work in exact fractions where you can, then give a decimal to three places.

Throughout, follow CONVENTIONS §3 notation: $\tilde{\mathbf{y}} = \mathbf{M}_2\mathbf{y}$ and $\tilde{\mathbf{X}}_1 = \mathbf{M}_2\mathbf{X}_1$ denote variables residualized on the control block $\mathbf{X}_2$; a double-dot $\ddot{x}_i = x_i - \bar{x}_{g(i)}$ denotes within-group demeaning.

---

## Problem 1 — State it, then read it (12 points)

This problem checks that you can say the theorem precisely and translate it into the language a paper actually uses.

**(a) [4 pts]** State the Frisch–Waugh–Lovell theorem in one careful sentence, for the partition $\mathbf{y} = \mathbf{X}_1\boldsymbol{\beta}_1 + \mathbf{X}_2\boldsymbol{\beta}_2 + \boldsymbol{\varepsilon}$ where $\mathbf{X}_1$ is the regressor of interest and $\mathbf{X}_2$ is the block of controls. Your sentence must name *what gets residualized on what* and *which two coefficients are being claimed equal*.

**(b) [4 pts]** Maya reads a fair-lending paper reporting: "the coefficient on applicant income is $\hat{\beta}_1 = 0.0042$, controlling for credit score and loan-to-value ratio." Rewrite the phrase "controlling for credit score and loan-to-value ratio" as an explicit *two-step residualization recipe* that would reproduce $0.0042$ without ever running the three-regressor regression. Be concrete about what you regress on what, and what you do with the leftovers.

**(c) [4 pts]** A classmate claims FWL is "just an approximation that works when the controls are weak." State whether this is true or false, and justify in one sentence by appealing to the *kind of statement* FWL is (identity vs. modeling assumption). Contrast it with one result from Ch 2.2 (Gauss–Markov) that genuinely *is* an assumption that can fail.

---

## Problem 2 — Partialling-out by hand: Maya's five borrowers (24 points)

Maya studies whether a borrower's **financial-literacy score** $x$ predicts their **on-time repayment rate** $y$ (in percentage points above some baseline), worried that both are entangled with **household income** $z$ (in \$10{,}000s): higher-income households both score higher and repay more, so a raw correlation could be measuring income, not literacy. She has five borrowers:

| borrower $i$ | repayment $y_i$ | literacy $x_i$ | income $z_i$ |
|---|---|---|---|
| 1 | 6 | 2 | 1 |
| 2 | 5 | 2 | 2 |
| 3 | 6 | 3 | 3 |
| 4 | 9 | 5 | 4 |
| 5 | 14 | 8 | 5 |

The means are $\bar{y} = 8$, $\bar{x} = 4$, $\bar{z} = 3$. Maya wants $\hat{\beta}_1$, the coefficient on literacy in the multiple regression $y_i = \beta_0 + \beta_1 x_i + \beta_2 z_i + \varepsilon_i$, but she will get it the FWL way, by hand.

**(a) [7 pts]** **Residualize the regressor.** Regress literacy on income (with an intercept): $x_i = a_0 + a_1 z_i + \tilde{x}_i$. Compute $a_1 = \operatorname{Cov}(x,z)/\operatorname{Var}(z)$ and $a_0 = \bar{x} - a_1\bar{z}$, then tabulate the five residuals $\tilde{x}_i = x_i - (a_0 + a_1 z_i)$. Verify they sum to zero, and explain in one sentence what these residuals *mean* (what part of literacy is left).

**(b) [7 pts]** **Residualize the outcome.** Do the same to repayment: regress $y$ on income (with intercept), $y_i = c_0 + c_1 z_i + \tilde{y}_i$. Compute $c_1, c_0$, and tabulate $\tilde{y}_i$. Again confirm they sum to zero.

**(c) [6 pts]** **Regress leftover on leftover.** Run the no-intercept simple regression $\tilde{y}_i = \beta_1 \tilde{x}_i + (\text{error})$ using $\hat{\beta}_1 = \sum_i \tilde{x}_i\tilde{y}_i / \sum_i \tilde{x}_i^2$. Report the slope as an exact fraction and a decimal. Explain in one sentence why no intercept is needed in this last step.

**(d) [4 pts]** State what FWL guarantees about the number you just computed relative to the three-regressor multiple regression, and how you would check it in one line of code (you may sketch the `statsmodels` call). Then interpret $\hat{\beta}_1$ in plain English for Maya, using the phrase "more than their income would predict."

---

## Problem 3 — The residual-maker proof (20 points)

Now prove the theorem you stated in Problem 1, using the residual-maker matrix from Ch 2.1. Let $\mathbf{M}_2 = \mathbf{I} - \mathbf{X}_2(\mathbf{X}_2'\mathbf{X}_2)^{-1}\mathbf{X}_2'$, and write $\tilde{\mathbf{y}} = \mathbf{M}_2\mathbf{y}$, $\tilde{\mathbf{X}}_1 = \mathbf{M}_2\mathbf{X}_1$. The full-model fit is $\mathbf{y} = \mathbf{X}_1\hat{\boldsymbol{\beta}}_1 + \mathbf{X}_2\hat{\boldsymbol{\beta}}_2 + \hat{\boldsymbol{\varepsilon}}$, where OLS orthogonality gives $\mathbf{X}_1'\hat{\boldsymbol{\varepsilon}} = \mathbf{0}$ and $\mathbf{X}_2'\hat{\boldsymbol{\varepsilon}} = \mathbf{0}$.

**(a) [4 pts]** State the three properties of $\mathbf{M}_2$ you will use, and for each give the one-line reason it holds. (Symmetry, idempotence, annihilation of its own block.)

**(b) [8 pts]** Left-multiply the full-model fit by $\mathbf{M}_2$ and simplify each of the three terms on the right, justifying each simplification by one of the properties in (a) or by the orthogonality of $\hat{\boldsymbol{\varepsilon}}$. Show that you arrive at
$$
\tilde{\mathbf{y}} = \tilde{\mathbf{X}}_1\hat{\boldsymbol{\beta}}_1 + \hat{\boldsymbol{\varepsilon}}.
$$

**(c) [6 pts]** Left-multiply *that* equation by $\tilde{\mathbf{X}}_1'$ and show the cross term $\tilde{\mathbf{X}}_1'\hat{\boldsymbol{\varepsilon}}$ vanishes — you must use symmetry of $\mathbf{M}_2$ and $\mathbf{M}_2\hat{\boldsymbol{\varepsilon}} = \hat{\boldsymbol{\varepsilon}}$ explicitly — to conclude
$$
\hat{\boldsymbol{\beta}}_1 = (\tilde{\mathbf{X}}_1'\tilde{\mathbf{X}}_1)^{-1}\tilde{\mathbf{X}}_1'\tilde{\mathbf{y}}.
$$

**(d) [2 pts]** The proof also shows the *residual* from the short regression equals $\hat{\boldsymbol{\varepsilon}}$, the full-model residual. Point to the exact line in your work that establishes this, and say in one sentence why it matters for getting standard errors right later (Ch 2.4).

---

## Problem 4 — What "holding constant" really means (14 points)

This problem is conceptual; answer in prose, tying every claim back to residualization.

**(a) [5 pts]** A beginner pictures "controlling for income" as: physically hold income fixed, wiggle literacy, watch repayment respond. Explain why the regression did *not* do that, and what it did instead. Your answer must use the word "subtract" (or "residualize") and must describe the coefficient as a statement about *leftover* variation.

**(b) [5 pts]** Explain, through the FWL lens, why adding a control that is essentially *unrelated* to the regressor of interest barely moves the coefficient, while adding a control *strongly related* to it can move the coefficient a lot. Refer to what residualizing does to $\tilde{x}$ in each case.

**(c) [4 pts]** Priya controls for "log assets" when studying climate-disclosure quality across insurers, and reports her coefficient as "holding firm size constant." A referee notes that firm *age* also drives both disclosure and size, and was not included. Using FWL's honesty about *which columns* get residualized, explain precisely what Priya's coefficient does and does not account for, and connect this to why CONVENTIONS §4 demands she name her controls and identifying assumption.

---

## Problem 5 — Demeaning is the within transformation (18 points)

Sam groups six trading desks into two strategy types — three "momentum" desks and three "value" desks — and asks whether a desk's **signal strength** $x$ predicts its **risk-adjusted return** $y$, *controlling for strategy type* (a two-level group dummy). The data, with desks 1–3 in group A (momentum) and 4–6 in group B (value):

| desk $i$ | group | return $y_i$ | signal $x_i$ |
|---|---|---|---|
| 1 | A | 3 | 2 |
| 2 | A | 6 | 4 |
| 3 | A | 9 | 6 |
| 4 | B | 8 | 3 |
| 5 | B | 11 | 5 |
| 6 | B | 14 | 7 |

**(a) [4 pts]** Compute the group means $\bar{x}_A, \bar{x}_B, \bar{y}_A, \bar{y}_B$. Then form the within-group-demeaned columns $\ddot{x}_i = x_i - \bar{x}_{g(i)}$ and $\ddot{y}_i = y_i - \bar{y}_{g(i)}$ and tabulate them. (They should be clean integers.)

**(b) [5 pts]** Run the no-intercept simple regression of $\ddot{y}$ on $\ddot{x}$: $\hat{\beta}_1 = \sum_i \ddot{x}_i\ddot{y}_i / \sum_i \ddot{x}_i^2$. Report the slope as a fraction and a decimal.

**(c) [5 pts]** Argue, citing FWL, that this within-demeaning slope equals the coefficient on $x$ in the regression of $y$ on $x$ *plus a group dummy* $D_i = \mathbf{1}\{\text{desk } i \in \text{group B}\}$ (and an intercept). Identify exactly what plays the role of the control block $\mathbf{X}_2$, and explain in one sentence *why* regressing on a full set of group dummies subtracts each group's own mean. (You do not need to run the dummy regression; you must explain why the two give the same slope.)

**(d) [4 pts]** For contrast, the *pooled* slope — regressing $y$ on $x$ alone, ignoring the groups — comes out to $1.8$, different from your within answer. Explain in one or two sentences what question the pooled slope answers versus what the within slope answers, and connect this to the sentence in Ch 2.3 that "controlling for industry asks a different question than controlling for size." Then state, in one sentence, why this within machinery is exactly the **fixed-effects** estimator you will meet in Week 3, and why packages demean instead of building a dummy per group.

---

## Problem 6 — Short vs. long: FWL as the lens on omitted-variable bias (12 points)

Return to Maya's five borrowers from Problem 2 ($y$ repayment, $x$ literacy, $z$ income; $\bar{y}=8$, $\bar{x}=4$, $\bar{z}=3$). In Problem 2 you found the **long** regression coefficient on literacy, $\hat{\beta}_1^{\text{long}} = 2$ (controlling for income), and you can take the long coefficient on income to be $\hat{\beta}_2^{\text{long}} = -1$.

**(a) [5 pts]** Compute the **short** regression slope — regress repayment on literacy *alone* (with intercept), $\hat{\beta}_1^{\text{short}} = \operatorname{Cov}(x,y)/\operatorname{Var}(x)$. Report it as an exact fraction and a decimal. Is it larger or smaller than the long coefficient $2$?

**(b) [4 pts]** Using the FWL picture *run in reverse*, explain in words why the short slope differs from the long slope: what variation is still riding inside the raw literacy variable in the short regression that was residualized out in the long one? Name which omitted variable's signal the short coefficient is absorbing.

**(c) [3 pts]** Without deriving the general formula (that is Ch 2.5), verify numerically that the gap decomposes as
$$
\hat{\beta}_1^{\text{short}} = \hat{\beta}_1^{\text{long}} + \hat{\beta}_2^{\text{long}}\cdot \hat{\delta},
$$
where $\hat{\delta} = \operatorname{Cov}(x,z)/\operatorname{Var}(x)$ is the slope from regressing the *omitted* control $z$ on the *included* regressor $x$. Compute $\hat{\delta}$, plug in, and confirm you recover your part-(a) number. State in one sentence which two quantities Ch 2.5 will name as the two factors of omitted-variable bias.

---

*Solutions: see `book/appendices/E-solutions-manual/E-w2-ps2.3-solutions.md`.*
