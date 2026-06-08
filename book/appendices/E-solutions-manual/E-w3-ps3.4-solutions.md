# Solutions — Problem Set 3.4 (Instrumental Variables: 2SLS Derivation and Weak-IV Diagnostics)

*Full worked solutions to `book/weeks/week-03/ps3.4.md`. Notation follows CONVENTIONS §3 and Ch 3.4. Core objects: the structural equation $Y_i=\beta_0+\beta_1 D_i+\mathbf X_i\boldsymbol\gamma+\varepsilon_i$ with endogenous treatment $D$; the two validity conditions, **relevance** $\operatorname{Cov}(Z,D)\neq 0$ and **exclusion** $\operatorname{Cov}(Z,\varepsilon)=0$; the Wald estimator $\hat\beta_1^{\text{Wald}}=(\overline Y_{Z=1}-\overline Y_{Z=0})/(\overline D_{Z=1}-\overline D_{Z=0})$; the FWL-with-an-instrument slope $\hat\beta_1^{\text{2SLS}}=\operatorname{Cov}(\tilde Z,\tilde Y)/\operatorname{Cov}(\tilde Z,\tilde D)$ where $\tilde{(\cdot)}$ denotes a variable residualized on the controls $\mathbf X$ (Ch 2.3 FWL); potential-treatment notation $D_i(0),D_i(1)$ (Ch 3.1); and the weak-IV bias approximation $(\mathbb{E}[\hat\beta^{\text{2SLS}}]-\beta_1)/(\mathbb{E}[\hat\beta^{\text{OLS}}]-\beta_1)\approx 1/F$. Citations used by name: Imbens, G. W. & Angrist, J. D. (1994), "Identification and Estimation of Local Average Treatment Effects," Econometrica 62(2), 467–475; Stock, J. H. & Yogo, M. (2005), "Testing for Weak Instruments in Linear IV Regression," in Identification and Inference for Econometric Models, Cambridge Univ. Press; Olea, J. L. M. & Pflueger, C. (2013), "A Robust Test for Weak Instruments," Journal of Business & Economic Statistics 31(3), 358–369. All arithmetic verified numerically.*

---

## Problem 1 — State the two conditions; classify which is testable (12 pts)

**(a) (3 pts)** Priya's structural equation, in the notation of Ch 3.4, is
$$
Y_i=\beta_0+\beta_1 D_i+\varepsilon_i,
$$
with $Y_i$ the post-storm financial-distress index, $D_i\in\{0,1\}$ the indicator for holding parametric flood insurance, and $\beta_1$ the causal effect she wants. The endogenous regressor is **$D_i$**. It is endogenous because the unmeasured confounder — **household risk-awareness / resources** — sits in $\varepsilon_i$ and drives both sides: risk-aware households are more likely to buy the policy ($D_i=1$) *and* tend to have lower distress anyway (low $\varepsilon_i$), so $\operatorname{Cov}(D_i,\varepsilon_i)\neq 0$ (in fact $<0$). This is the omitted-variable disease of Ch 2.5: a relevant variable correlated with the regressor, banished to the error.

**(b) (3 pts)** **Relevance:** $\operatorname{Cov}(Z_i,D_i)\neq 0$. In plain words, the randomized education visit must actually change whether households buy the policy — the instrument has to be a real lever on the treatment. Priya tests it by estimating the **first stage**, the regression $D_i=\pi_0+\pi_1 Z_i+\nu_i$ (with any controls), and checking that the coefficient $\hat\pi_1$ is large and precisely estimated; she hopes to see $\hat\pi_1>0$ (visited households buy more) clearing a strength bar (Problem 4).

**(c) (3 pts)** **Exclusion:** $\operatorname{Cov}(Z_i,\varepsilon_i)=0$. In plain words, the education visit must affect post-storm distress *only* by changing whether the household buys the policy, and must itself be unrelated to risk-awareness. Random assignment of the visit secures the "unrelated to the confounder" half for free (a coin flip cannot correlate with risk-awareness). The fragile half is *no direct path*. A concrete violation: the visit might teach households **general emergency-savings or evacuation-planning habits** that lower post-storm distress on their own, even for households that never buy the policy. That is a road $Z_i\to Y_i$ that bypasses $D_i$, and it breaks exclusion.

**(d) (3 pts)** **Relevance is testable; exclusion is not.** Relevance is a statement about $\operatorname{Cov}(Z,D)$, and Priya observes both $Z$ and $D$, so she can estimate it and put a standard error on it. Exclusion is the statement $\operatorname{Cov}(Z,\varepsilon)=0$, and it is untestable because it involves the **structural error $\varepsilon$, which is never observed** — $\varepsilon$ contains exactly the unmeasured confounder (risk-awareness) that motivated IV in the first place. With no data column for $\varepsilon$, there is no covariance to compute and no $p$-value to report; exclusion can only be *argued* from the design and institutional knowledge.

---

## Problem 2 — The Wald estimator from a $2\times 2$ table (15 pts)

Data: $\overline D_{Z=1}=0.50$, $\overline D_{Z=0}=0.20$; $\overline Y_{Z=1}=-4.5$, $\overline Y_{Z=0}=-1.5$; each group $N=500$.

**(a) (3 pts)**
$$
\text{first stage}=\overline D_{Z=1}-\overline D_{Z=0}=0.50-0.20=\boxed{0.30},\qquad
\text{reduced form}=\overline Y_{Z=1}-\overline Y_{Z=0}=-4.5-(-1.5)=\boxed{-3.0}.
$$
The first stage is the effect of the *offer* on opening a position — it is the empirical content of the **relevance** condition (nonzero, here a healthy $0.30$). The reduced form is the effect of the *offer* on the volatility outcome, ignoring $D$ entirely — the raw "intention-to-treat" response of $Y$ to the instrument.

**(b) (4 pts)**
$$
\hat\beta_1^{\text{Wald}}=\frac{\text{reduced form}}{\text{first stage}}=\frac{-3.0}{0.30}=\boxed{-10\ \text{vol pts}}.
$$
The offer lowered average volatility by $3.0$ points but only moved an extra $30\%$ of users into a diversified position; if the offer helped *only* through that position (exclusion), the entire $3.0$-point improvement was produced by those $30\%$, so the per-opener effect is $3.0/0.30=10$ points of volatility *reduction*. The estimate says: opening a diversified position lowers annualized volatility by about $10$ points — **for the users the offer actually moved** (the compliers), not for all users.

**(c) (3 pts)** The naive comparison — volatility change of openers minus non-openers — is biased because opening is **self-selected**: users who open a diversified position on their own tend to be more financially sophisticated, and their portfolios would have been calmer regardless of this one position, so the comparison mixes the position's effect with the sophistication gap (the confounder in $\varepsilon$). The Wald estimator never compares openers to non-openers; it only ever compares the **offered group to the not-offered group**, and because the offer was randomized, those two groups are identical in sophistication. The condition that makes the offered-vs-not contrast clean is **exclusion** (specifically its as-good-as-random half, delivered by the randomization), so the difference reflects the offer alone.

**(d) (3 pts)** Counts of users who opened a position: offered group $0.50\times 500=\boxed{250}$; not-offered group $0.20\times 500=\boxed{100}$. The complier share of the *whole* population is the first stage, $\boxed{0.30}$ (i.e. $30\%$). It equals the first stage because, under **monotonicity** (no defiers), the only people whose opening status responds to the offer are compliers: always-takers open in both arms and never-takers open in neither, so they cancel in $\overline D_{Z=1}-\overline D_{Z=0}$, leaving exactly the fraction who open *because* they were offered — the compliers.

**(e) (2 pts)** The **exclusion** condition is now in doubt: the advice paragraph gives the offer a direct path to $Y$ (lower volatility through diversifying *elsewhere*) that bypasses $D$. Because that channel also *lowers* volatility, it inflates the magnitude of the (negative) reduced form without raising the first stage, pushing $\hat\beta_1^{\text{Wald}}$ **away from zero** (more negative) — it over-credits the position with improvement that the advice actually caused.

---

## Problem 3 — 2SLS as FWL-with-an-instrument: the covariance ratio (20 pts)

**(a) (5 pts)** Start from the residualized just-identified equation $\tilde Y_i=\beta_1\tilde D_i+\tilde\varepsilon_i$. Multiply through by $\tilde Z_i$ and take expectations (all variables mean-zero after residualizing, so expectations of products are covariances):
$$
\operatorname{Cov}(\tilde Z,\tilde Y)=\beta_1\operatorname{Cov}(\tilde Z,\tilde D)+\operatorname{Cov}(\tilde Z,\tilde\varepsilon).
$$
Impose **exclusion**, $\operatorname{Cov}(\tilde Z,\tilde\varepsilon)=0$ — *this is the step where exclusion does its work*, killing the last term. Solving,
$$
\beta_1=\frac{\operatorname{Cov}(\tilde Z,\tilde Y)}{\operatorname{Cov}(\tilde Z,\tilde D)}.
$$
The derivation would **collapse if relevance failed**: if $\operatorname{Cov}(\tilde Z,\tilde D)=0$ the final division is by zero and $\beta_1$ is not identified — there is no lever to read the effect off of.

**(b) (6 pts)** Build the two sums term by term.

| $i$ | $\tilde Z_i$ | $\tilde D_i$ | $\tilde Y_i$ | $\tilde Z_i\tilde D_i$ | $\tilde Z_i\tilde Y_i$ |
|---|---:|---:|---:|---:|---:|
| 1 | $-2$ | $-1$ | $+2$ | $+2$ | $-4$ |
| 2 | $-1$ | $0$ | $+2$ | $0$ | $-2$ |
| 3 | $0$ | $0$ | $0$ | $0$ | $0$ |
| 4 | $1$ | $0$ | $-2$ | $0$ | $-2$ |
| 5 | $2$ | $1$ | $-2$ | $+2$ | $-4$ |
| **Σ** | | | | **$+4$** | **$-12$** |

So $\sum_i\tilde Z_i\tilde D_i=4$ and $\sum_i\tilde Z_i\tilde Y_i=-12$, and
$$
\hat\beta_1^{\text{2SLS}}=\frac{\sum_i\tilde Z_i\tilde Y_i}{\sum_i\tilde Z_i\tilde D_i}=\frac{-12}{4}=\boxed{-3}.
$$

**(c) (4 pts)** OLS of $\tilde Y$ on $\tilde D$: build $\sum_i\tilde D_i\tilde Y_i$ and $\sum_i\tilde D_i^2$. Only observations $1$ and $5$ have $\tilde D_i\neq 0$: $\tilde D_1\tilde Y_1=(-1)(2)=-2$, $\tilde D_5\tilde Y_5=(1)(-2)=-2$, so $\sum=-4$; and $\sum\tilde D_i^2=(-1)^2+1^2=2$. Thus
$$
\hat\beta_1^{\text{OLS}}=\frac{-4}{2}=\boxed{-2}.
$$
The two slopes: $\hat\beta_1^{\text{2SLS}}=-3$, $\hat\beta_1^{\text{OLS}}=-2$. The **OLS slope is attenuated toward zero** (smaller in magnitude). A gap between OLS and 2SLS is the *signature of endogeneity* because OLS carries the bias term $\operatorname{Cov}(D,\varepsilon)/\operatorname{Var}(D)$ from §2 of the chapter — when that covariance is nonzero (here positive, pulling the negative slope up toward zero), OLS and the consistent 2SLS estimate diverge by exactly the bias.

**(d) (3 pts)** FWL prescribes residualizing *every* variable in the system against the controls $\mathbf X$, so $Y$, $D$, **and** $Z$ must all be partialled out for the covariance ratio to equal the controlled 2SLS coefficient. If you forget to residualize $Z$, the leftover $Z$ still carries the part of itself that is *explained by* the controls; that piece can correlate with the residualized error, silently breaking **exclusion** in the residualized system ($\operatorname{Cov}(\tilde Z,\tilde\varepsilon)\neq 0$), and the ratio no longer recovers $\beta_1$. Equivalently, omitting the controls from the first stage is the classic bug from §5 of the chapter that invalidates the cleaning.

**(e) (2 pts)** Setting $Z=D$ (the treatment is its own instrument) turns the ratio into $\operatorname{Cov}(\tilde D,\tilde Y)/\operatorname{Cov}(\tilde D,\tilde D)=\operatorname{Cov}(\tilde D,\tilde Y)/\operatorname{Var}(\tilde D)$, the ordinary OLS slope. That is exactly the move that fails under endogeneity, because it requires $\operatorname{Cov}(D,\varepsilon)=0$ — the very assumption that is false.

---

## Problem 4 — First-stage F and the Stock–Yogo bar (16 pts)

**(a) (3 pts)** $t=\hat\pi_1/\text{se}=0.30/0.05=6.0$, and with a single instrument the first-stage F is the squared t:
$$
F=t^2=6.0^2=\boxed{36}.
$$
The **relevance** condition $\operatorname{Cov}(Z,D)\neq 0$ is comfortably satisfied and *strongly* so: $F=36\gg 10$, clearing the rule-of-thumb bar with room to spare.

**(b) (4 pts)** Stock and Yogo (2005) made "how strong is strong enough" precise. They asked: how large must the first-stage F be to **guarantee that the 2SLS bias is no more than a chosen fraction (e.g. $10\%$) of the bias of OLS** (or, in a second version, that a nominal $5\%$ test rejects no more than some bounded fraction of the time under the null)? They tabulated critical values delivering those guarantees as a function of the number of instruments and the chosen tolerance; for one endogenous regressor and one instrument, the "bias $\le 10\%$ of OLS" critical value lands near $F\approx 10$ — the origin of the rule of thumb. Clearing it buys a *formal* bound on weak-IV bias **relative to the OLS bias** (the named benchmark), not an absolute guarantee.

**(c) (4 pts)** $t=0.08/0.05=1.6$, so $F=t^2=1.6^2=\boxed{2.56}$. This instrument is **weak** — far below $10$, and the t is not even conventionally significant. The consequence, quantified in Problem 6: the 2SLS estimate will be dragged back toward the biased OLS estimate (its weak-IV bias is a large fraction $\approx 1/F$ of the OLS bias), and its standard error will be inflated and unreliable.

**(d) (5 pts)** Three reasons "$F>10$" is a smoke alarm, not a certificate:
1. **It assumes classical errors.** The Stock–Yogo critical values were derived under **homoskedastic, non-clustered** errors. Leah's errors are heteroskedastic and clustered by state, so the ordinary (non-robust) first-stage F no longer corresponds to the Stock–Yogo guarantee and can badly *understate* weakness.
2. **The bar rises with the number of instruments.** The critical value grows as you add instruments; with many instruments, $10$ is far too lenient.
3. **"$F>10$" bounded *bias*, not *inference*.** More recent work argues that to keep the *t-test* honest you may need F values far above $10$ — sometimes above $100$ — once you account for the distortion weak instruments inflict on the sampling distribution; clearing $10$ does not license trusting your t-statistic.

For reason (1), the statistic Leah should report instead is the **Olea–Pflueger (2013) effective F-statistic**, which is built from heteroskedasticity- and cluster-robust variance estimates and comes with matching critical values for a chosen bias tolerance — the right strength diagnostic when errors are non-classical.

---

## Problem 5 — LATE and the four compliance types (18 pts)

**(a) (6 pts)** Using $D_i(0),D_i(1)$ = the position-opening choice if not offered / if offered:

| Type | $D_i(0)$ | $D_i(1)$ | Devon-context description |
|---|:---:|:---:|---|
| **Never-taker** | $0$ | $0$ | Never opens a diversified position, offer or not (uninterested or distrustful users). |
| **Always-taker** | $1$ | $1$ | Opens a diversified position regardless — the already-sophisticated users who'd diversify anyway. |
| **Complier** | $0$ | $1$ | Opens *iff* offered the rebate — the fence-sitters the promotion tips over. |
| **Defier** | $1$ | $0$ | Opens *only if not* offered — perversely repelled by the rebate (assumed away). |

**(b) (3 pts)** **Monotonicity:** $D_i(1)\ge D_i(0)$ for every $i$ — the offer can only weakly *increase* the chance of opening, never decrease it. In words, the instrument pushes everyone in the same direction (or not at all). It assumes the **defiers** out of existence. It is needed because, without it, defiers' treatment responses enter the Wald numerator with the *opposite sign* to compliers' and can cancel or even reverse the estimate; ruling them out is what lets the IV estimand be a clean (positively-weighted) complier average — the LATE.

**(c) (4 pts)** The instrument is blind to always-takers and never-takers because **their treatment status does not respond to the offer**: an always-taker has $D_i=1$ in both arms and a never-taker has $D_i=0$ in both arms, so each contributes $D_i(1)-D_i(0)=0$ to the first stage $\overline D_{Z=1}-\overline D_{Z=0}$. Since the Wald estimator reads the outcome response off the *instrument-induced* change in treatment, and these two types produce *no* change in treatment, none of their treatment effect can enter the Wald numerator — the only effects that survive belong to the compliers, whose treatment the offer actually flipped.

**(d) (3 pts)** **Imbens–Angrist (1994) LATE theorem:** under a valid instrument (relevance + exclusion) and monotonicity, the IV (Wald/2SLS) estimand equals the average treatment effect among compliers, $\hat\beta_1^{\text{IV}}\xrightarrow{p}\mathbb{E}[Y_i(1)-Y_i(0)\mid i\text{ is a complier}]\equiv\text{LATE}$. Two different valid instruments can give two different LATEs because they **move different sets of compliers** — a rebate offer and, say, a different nudge tip different fence-sitters into treatment, and if the effect varies across users, the two complier averages differ; neither is wrong, they simply answer about different subpopulations.

**(e) (2 pts)** No, Devon's IV **cannot** answer it. The policymaker cares about the **never-takers** (those who will not diversify under any nudge). No voluntary-uptake instrument can identify their effect, because by definition the instrument never moves their treatment status — they never open a position in any arm, so their $Y_i(1)-Y_i(0)$ never appears in the instrument-driven variation that IV exploits.

---

## Problem 6 — Weak instruments: the bias-toward-OLS calculation (19 pts)

Setup: true $\beta_1=2.0$; OLS bias $=+1.5$, so $\mathbb{E}[\hat\beta^{\text{OLS}}]=3.5$. Bias approximation: $\dfrac{\mathbb{E}[\hat\beta^{\text{2SLS}}]-\beta_1}{\mathbb{E}[\hat\beta^{\text{OLS}}]-\beta_1}\approx\dfrac{1}{F}$, so the 2SLS bias in levels is $\approx(\text{OLS bias})\times\frac1F=1.5/F$.

**(a) (4 pts)** Strong instrument, $F=36$:
$$
\text{bias fraction}\approx\frac{1}{36}=0.0278,\qquad
\text{bias in levels}\approx 1.5\times0.0278=\boxed{0.042},
$$
$$
\mathbb{E}[\hat\beta^{\text{2SLS}}]\approx 2.0+0.042=\boxed{2.04}.
$$
2SLS is doing its job: the estimate sits essentially on the truth $2.0$, having shed all but about $2.8\%$ of the OLS bias.

**(b) (5 pts)** Weak instrument, $F=2.56$:
$$
\text{bias fraction}\approx\frac{1}{2.56}=0.391,\qquad
\text{bias in levels}\approx 1.5\times0.391=\boxed{0.586},
$$
$$
\mathbb{E}[\hat\beta^{\text{2SLS}}]\approx 2.0+0.586=\boxed{2.59}.
$$
Compare: truth $=2.0$, OLS $=3.5$, weak-IV 2SLS $\approx 2.59$. The 2SLS estimate is still closer to the truth than OLS is, but it has been dragged a substantial $39\%$ of the way back toward the OLS bias — and this point estimate comes with an inflated, unreliable standard error, so even this partial improvement is not trustworthy. The weak instrument has surrendered most of the bias-fighting benefit it was supposed to deliver.

**(c) (4 pts)** The first stage produces a fitted treatment $\hat D_i$ that is *supposed* to be the clean, instrument-driven slice of $D$. But when $Z$ explains almost none of $D$ (weak first stage), $\hat D_i$ is built mostly from **first-stage sampling noise** rather than from $Z$, and that noise is correlated with the structural error $\varepsilon$ in finite samples (the first-stage residual $\nu$ and $\varepsilon$ share the confounder). So $\hat D_i$ is recontaminated by exactly the endogeneity IV was meant to remove, and the second-stage slope therefore **drifts toward the OLS slope** — back to the bias you were fleeing.

**(d) (3 pts)** A forbidden direct effect contaminates IV as $c/\operatorname{Cov}(Z,D)$. When the first stage is **strong** (large $\operatorname{Cov}(Z,D)$), a small numerator $c$ divided by a large denominator is negligible — the violation barely registers. When the first stage is **weak** ($\operatorname{Cov}(Z,D)$ near zero), that *same* small $c$ is divided by a near-zero denominator and blows up into a large bias. So weak instruments make you **maximally vulnerable to exactly the exclusion violations you can never test for** (you cannot measure $c$ because $\varepsilon$ is unobserved). A strong first stage shrinks the denominator-driven amplification, making it a *buffer* against the untestable exclusion assumption — not merely a gain in precision.

**(e) (3 pts)** The weak-IV checklist:
- **Always report the first stage** and its strength statistic — the first-stage F — as the testable face of relevance.
- Under **heteroskedastic or clustered errors** (the finance default), do not trust the classical F; switch to the **Olea–Pflueger (2013) effective F-statistic**, computed with the same robust/clustered errors as the second stage, and compare it to the matching critical value rather than eyeballing "$F>10$."
- If the instrument turns out **weak**, do not paper over it with a t-statistic; switch to weak-IV-**robust inference**, namely **Anderson–Rubin confidence intervals**, which stay valid no matter how weak the instrument — the method delivered in **Chapter 3.5**.

---

*End of solutions for PS 3.4. Cross-references: Ch 3.4 (relevance/exclusion asymmetry, Wald estimator, 2SLS as FWL-with-an-instrument, LATE/compliers, weak-IV pathologies, first-stage F, Stock–Yogo, Olea–Pflueger effective F), Ch 2.3 (FWL/residualization), Ch 2.5 (OLS bias term and the bias–consistency ledger), Ch 3.1 (potential-outcomes notation, here applied to potential treatments), Ch 3.5 (weak-IV disaster lab and Anderson–Rubin inference). Numeric keys: P2 first stage 0.30, reduced form −3.0, Wald −10, openers 250/100, complier share 0.30; P3 ΣZ̃D̃=4, ΣZ̃Ỹ=−12, 2SLS slope −3, OLS slope −2 (attenuated); P4 strong t=6 → F=36 (clears 10), weak t=1.6 → F=2.56; P6 F=36 → bias 0.042, E[2SLS]≈2.04; F=2.56 → bias 0.586, E[2SLS]≈2.59 (39% of the way back to OLS=3.5). Feeds Ch 3.5.*
