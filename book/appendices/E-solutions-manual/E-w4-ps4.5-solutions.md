# Solutions — Problem Set 4.5 (Shift-Share Exposure Weights and the Identification Critique)

*Full worked solutions to `book/weeks/week-04/ps4.5.md`. Notation follows CONVENTIONS §3 and Ch 4.5. Core objects: the shift-share / Bartik instrument $B_r=\sum_k s_{rk}\,g_k$ built from baseline local exposure shares $s_{rk}$ (rows sum to one, $\sum_k s_{rk}=1$) and national shifts $g_k$ (leave-one-region-out industry/bank growth rates); the canonical design that uses $B_r$ to instrument the realized endogenous local shock; the **relevance** ($\operatorname{Cov}(B_r,\Delta C_r)\neq0$, testable) and **exclusion** ($\operatorname{Cov}(B_r,\varepsilon_r)=0$, untestable) conditions inherited from Ch 3.4; the **GPSS (2020)** "identification from the shares" view with its Rotemberg decomposition $\hat\beta_1^{\text{Bartik}}=\sum_k\hat\alpha_k\,\hat\beta_{1,k}$, $\sum_k\hat\alpha_k=1$; the **BHJ (2022)** "identification from the shifts" view with the effective-number-of-shocks count $K_{\text{eff}}=1/\sum_k\omega_k^2$; and the **AKM (2019)** cross-regional-correlation inference correction. Citations used by name: Bartik, T. J. (1991), *Who Benefits from State and Local Economic Development Policies?*, W.E. Upjohn Institute; Goldsmith-Pinkham, P., Sorkin, I., & Swift, H. (2020), "Bartik Instruments: What, When, Why, and How," American Economic Review 110(8), 2586–2624; Borusyak, K., Hull, P., & Jaravel, X. (2022), "Quasi-Experimental Shift-Share Research Designs," Review of Economic Studies 89(1), 181–213; Adão, R., Kolesár, M., & Morales, E. (2019), "Shift-Share Designs: Theory and Inference," Quarterly Journal of Economics 134(4), 1949–2010. All arithmetic verified numerically.*

---

## Problem 1 — Construct the Bartik instrument by hand (16 pts)

**(a) (3 pts)** Exposure shares must form a valid weighting: for each region the bank shares are nonnegative and sum to one across banks, $\sum_b s_{rb}=1$. Check both:
$$
\text{Lakeside: } 0.20+0.50+0.30=\boxed{1.00},\qquad \text{Mill Hollow: } 0.70+0.10+0.20=\boxed{1.00}.
$$
Both are valid exposure-weight vectors — each region's deposits are fully allocated across the three banks. (This is the $\sum_k s_{rk}=1$ requirement from Ch 4.5 §2; it guarantees $B_r$ is a genuine *weighted average* of the shifts, so a region whose banks all grew at rate $g$ gets predicted growth $g$.)

**(b) (5 pts)** Apply $B_r=\sum_b s_{rb}\,g_b$ with shifts $g=(+4\%,-10\%,+1\%)$.

Lakeside:
$$
B_{\text{Lake}}=(0.20)(+4\%)+(0.50)(-10\%)+(0.30)(+1\%)=+0.8\%-5.0\%+0.3\%=\boxed{-3.9\%}.
$$
Mill Hollow:
$$
B_{\text{Mill}}=(0.70)(+4\%)+(0.10)(-10\%)+(0.20)(+1\%)=+2.8\%-1.0\%+0.2\%=\boxed{+2.0\%}.
$$

**(c) (3 pts)** Lakeside is *predicted to suffer a credit-supply contraction* ($-3.9\%$): it banked heavily ($50\%$) with Heartland Savings, which shed $10\%$ of its lending nationally, so its bank mix dragged it down. Mill Hollow is *predicted to get easier credit* ($+2.0\%$): it banked heavily ($70\%$) with the nationally-expanding BigCommerce. The two regions differ even though they face the *identical* three national shifts because **the shares do all the work** of turning one common set of shocks into two region-specific predictions — the only thing distinguishing $B_{\text{Lake}}$ from $B_{\text{Mill}}$ is the exposure-weight vectors (the seed of the GPSS "it's the shares" view).

**(d) (3 pts)** With common shares $(0.40,0.30,0.30)$:
$$
B_r=(0.40)(+4\%)+(0.30)(-10\%)+(0.30)(+1\%)=+1.6\%-3.0\%+0.3\%=\boxed{-1.1\%},
$$
the *same number for every region*. A constant instrument has no cross-regional variation, so it has zero covariance with the realized local shock and instruments **nothing** — relevance ($\operatorname{Cov}(B_r,\Delta C_r)\neq0$) fails by construction. The variation destroyed here is **share dispersion**: with identical shares, regions are indistinguishable as bundles of bank bets.

**(e) (2 pts)** With a common shift $g_b=+2\%$ for all banks and Lakeside's shares:
$$
B_{\text{Lake}}=(0.20+0.50+0.30)(+2\%)=(1.00)(+2\%)=\boxed{+2.0\%}.
$$
Because the shares sum to one, $B_r=\sum_b s_{rb}\,g=g\sum_b s_{rb}=g$ for *every* region — again a constant. The variation destroyed now is **shift dispersion**: if all shocks are equal, reweighting them by any shares returns the common shock. $B_r$ varies across regions only from the *interaction* of share dispersion and shift dispersion; kill either and the instrument dies (Ch 4.5 §2).

---

## Problem 2 — Relevance / the first stage (14 pts)

**(a) (4 pts)** The **first stage** regresses the realized endogenous regressor on the instrument and controls:
$$
\Delta C_r=\pi_0+\pi_1 B_r+\mathbf X_r\boldsymbol\gamma+\nu_r,
$$
i.e. regress realized local credit growth $\Delta C_r$ on the bank-mix prediction $B_r$. **Relevance** is $\operatorname{Cov}(B_r,\Delta C_r)\neq0$ (after partialling out controls): in plain words, regions the bank-mix prediction says should have ridden contracting banks must *actually* have experienced slower realized credit growth. We expect it to hold because the prediction $B_r$ is assembled from the genuine credit-supply behavior of the banks that *operate in the region* — if your dominant lender is pulling back nationally, it tends to pull back on you too, so the predicted crunch shows up in realized local credit. Relevance is the empirical content of "the lever actually moves the treatment."

**(b) (4 pts)** With a single instrument the first-stage F is the squared t on $B_r$:
$$
t=\frac{\hat\pi_1}{\text{se}}=\frac{0.85}{0.10}=8.5,\qquad F=t^2=8.5^2=\boxed{72.25}.
$$
This clears the "$F>10$" rule of thumb comfortably ($72.25\gg10$). The F-statistic speaks *only* to **relevance** — it measures how strongly $B_r$ moves $\Delta C_r$, the testable validity condition.

**(c) (3 pts)** The colleague conflates relevance with validity. The first-stage F confirms **relevance** ($B_r$ is a strong lever on $\Delta C_r$) and *nothing else*; it is silent on **exclusion** ($\operatorname{Cov}(B_r,\varepsilon_r)=0$), because exclusion is a statement about the *unobserved* region error $\varepsilon_r$ — you cannot put a standard error on a covariance with a column you do not have. This is exactly the Ch 3.4 testable/untestable asymmetry: relevance lives in observed $(B_r,\Delta C_r)$ and is testable; exclusion lives in $\varepsilon_r$ and can only be *argued*. A strong first stage plus a broken exclusion restriction is a precisely-estimated wrong answer.

**(d) (3 pts)** Under clustering and heteroskedasticity, the classical F no longer matches its nominal guarantee; Maya should report the **Olea–Pflueger effective F-statistic** (Ch 3.5), computed with the same robust/clustered variance as the second stage. A *weak* shift-share first stage is dangerous because, exactly as in Ch 3.4–3.5, the fitted treatment $\widehat{\Delta C_r}$ becomes mostly first-stage noise correlated with the confounder, and 2SLS **drifts back toward the biased OLS estimate** — the bias you used the instrument to escape. Significance is not strength: a $B_r$ that is statistically significant but weak still drags 2SLS toward OLS.

---

## Problem 3 — Identification from the shares: GPSS and Rotemberg weights (20 pts)

**(a) (4 pts)** In a single cross-section, the national shifts $g_b$ are *fixed numbers* — the same auto/bank shock applied to every region. So in $B_r=\sum_b s_{rb}\,g_b$, the only thing that changes as you move from region to region is the **vector of shares** $(s_{r1},s_{r2},\dots)$; the shifts are constants serving as *weights* in a recipe. Cross-sectionally, then, the Bartik instrument *is* the shares (weighted by the shifts), and any cross-regional variation in $B_r$ is variation in shares. Therefore whatever delivers the cross-regional exogenous variation $B_r$ needs to be a valid instrument — the variation uncorrelated with $\varepsilon_r$ — must be a statement about the **shares**. (Goldsmith-Pinkham–Sorkin–Swift 2020: 2SLS with the single $B_r$ is numerically the over-identified GMM estimator using each share $s_{rk}$ as a separate instrument.)

**(b) (4 pts)** **GPSS identifying assumption (exogenous shares):** each baseline share is uncorrelated with the region error, conditional on controls,
$$
\mathbb{E}[\varepsilon_r\mid s_{r1},\dots,s_{rB},\mathbf X_r]=0,
$$
equivalently $\operatorname{Cov}(s_{rk},\varepsilon_r)=0$ for every bank $k$. In plain words, a region's *initial bank mix* is as-good-as-randomly assigned with respect to whatever else drives delinquency. Under this view the **shifts are let off the exogeneity hook entirely** — they are allowed to be endogenous to all sorts of macro forces (the national credit cycle can be driven by anything), because they enter only as fixed weights. The shifts must still be *relevant* (the first stage must hold), but the *exclusion* burden falls wholly on the shares.

**(c) (4 pts)** A concrete back-door story. Suppose regions whose 2006 deposits were concentrated in **aggressive, fast-growing lenders** (say, banks that pushed subprime products) were *also* regions with looser household lending standards and more fragile household balance sheets — latent fragility that would have driven up delinquency *regardless of the bank-supply shock*. Then the baseline share $s_{r,\text{aggressive-bank}}$ is correlated with the fragility sitting in $\varepsilon_r$: the share predicts delinquency through a back door (the region was full of overextended borrowers) rather than only through the credit-supply channel. Exclusion fails on the share side and the Bartik estimate is contaminated. (This is the household-credit cousin of the trade-literature worry that manufacturing-heavy regions were on a secular decline predating the China shock.)

**(d) (5 pts)** First, the weights sum to one: $0.70+0.22+0.05+0.03=\boxed{1.00}$. Now reassemble the headline:
$$
\sum_k\hat\alpha_k\hat\beta_{1,k}=(0.70)(0.80)+(0.22)(0.20)+(0.05)(0.10)+(0.03)(-0.30).
$$
Term by term: $0.560+0.044+0.005-0.009=\boxed{+0.60}$, which exactly reassembles the headline $\hat\beta_1^{\text{Bartik}}=+0.6$. The estimate is **dominated by BigCommerce Bank**, whose share-instrument carries a Rotemberg weight of $\hat\alpha=0.70$ — fully **70%** of the weight, and contributing $0.56$ of the $0.60$ headline. The whole causal claim is essentially a story about one bank's exposure.

**(e) (3 pts)** Maya should aim her **share-exogeneity skepticism at BigCommerce first**, because $70\%$ of the estimate rides on the exogeneity of *that* bank's deposit share — if regions banking heavily with BigCommerce differ systematically in latent fragility (the Problem 3(c) back door), the headline is contaminated. The single most informative robustness check: **drop BigCommerce's share-instrument and re-estimate** (and run a balance / pre-trend test of the BigCommerce share against pre-period covariates), to see whether the result survives without its dominant driver. This is the shift-share analogue of the Ch 4.2 Rotemberg/negative-weights lesson: a headline is a weighted average of building blocks, so look at the weights before believing the average. As for Pinebluff Mutual — its per-instrument estimate $\hat\beta_{1,\text{Pine}}=-0.30$ has the *wrong sign*, but its weight is only $0.03$, so it barely perturbs the headline (it removes just $0.009$). Its low weight does make it *largely* harmless to the point estimate, but it is a yellow flag worth noting: a wrong-signed building block hints the share-exogeneity story is not uniform across banks, and you would not want it to be carrying serious weight.

---

## Problem 4 — Identification from the shifts: BHJ and the effective number of shocks (18 pts)

**(a) (4 pts)** **BHJ identifying assumption (quasi-random shifts):** the random object is the vector of **national shocks** $g_k$. They must be as-good-as-randomly assigned across industries/banks — mean-independent of the industry-level unobservables, conditional on shock-level controls — and crucially there must be **many** of them, with exposure sufficiently dispersed. The BHJ view **lets the shares be endogenous**: a region's bank mix can be as historically loaded as you like, because identification is now a *shock-level* quasi-experiment in which shares are demoted to mere exposure weights (how much of each random shock each region absorbs). This is exactly the *opposite license* from GPSS: GPSS makes the shares carry exogeneity and frees the shifts; BHJ makes the shifts carry exogeneity and frees the shares. A product is exogenous if either factor is — so the two views are two routes to the same untestable exclusion restriction.

**(b) (4 pts)** With *many* dispersed shocks, $B_r=\sum_k s_{rk}\,g_k$ is an exposure-weighted average of many independent random draws, and a law-of-large-numbers logic kicks in: any single endogenous or idiosyncratic shock contributes only a tiny exposure-weighted slice, so it *washes out* and $B_r$ behaves like a clean region-level draw from the shock lottery. With only a *handful* of shocks there is no "many" to average over — a single big shock (e.g., one dominant bank's idiosyncratic move) carries a large fraction of every region's exposure, the LLN fails, and you cannot honestly claim $B_r$ is as-good-as-random. This is why "how many shocks" decides whether the BHJ story is available.

**(c) (5 pts)** Compute $K_{\text{eff}}=1/\sum_k\omega_k^2$.

*Sample A (dispersed),* $\omega=(0.20,0.20,0.20,0.20,0.20)$:
$$
\sum_k\omega_k^2=5\times(0.20)^2=5\times0.04=0.20,\qquad K_{\text{eff}}=\frac{1}{0.20}=\boxed{5.0}.
$$

*Sample B (concentrated),* $\omega=(0.80,0.10,0.05,0.03,0.02)$:
$$
\sum_k\omega_k^2=0.64+0.01+0.0025+0.0009+0.0004=0.6538,\qquad K_{\text{eff}}=\frac{1}{0.6538}\approx\boxed{1.53}.
$$
Both samples have *five* banks nominally, but $K_{\text{eff}}$ reveals that Sample A behaves like five effective shocks while Sample B behaves like fewer than *two* — essentially one big shock plus noise. Only **Sample A** can honestly invoke the BHJ "many shocks" story; in Sample B the "many" is an illusion (one $80\%$-weight bank dominates), the LLN has nothing to lean on, and the BHJ defense collapses. This is BHJ's warning that the effective sample size, not the nominal count, governs the quasi-experiment.

**(d) (3 pts)** Maya can honestly invoke only **GPSS (exogenous shares)** in her bank setting. With just six banks, two of which hold most deposits region-by-region, her $K_{\text{eff}}$ is small (Sample-B-like): there are too few effective shocks for the BHJ law-of-large-numbers logic, so the **BHJ "quasi-random many shifts" view fails** — a single dominant bank's idiosyncratic shock would drive the whole instrument, with no "many" to average it away. The labor-demand design she read about, with several hundred industries, is the reverse regime where BHJ is natural. Few concentrated shares $\Rightarrow$ GPSS; many dispersed shocks $\Rightarrow$ BHJ (Ch 4.5 §6).

**(e) (2 pts)** To defend the shift side beyond $K_{\text{eff}}$, Maya reports a **balance / pre-trend test of the shifts against shock-level (industry/bank-level) confounders** — checking that the national shocks are not systematically aligned with pre-existing industry trends (often after *residualizing the shocks against shock-level controls*, e.g. removing broad sector trends). It is the **shock-level analogue of the share-balance / pre-trend tests** on the GPSS side (Problem 5(d), and the parallel-trends interrogation reused from Ch 4.1): same balance logic, but the unit of defense is the *industry/bank* rather than the *region*.

---

## Problem 5 — Critique a described design (16 pts)

**(a) (4 pts)** This is a textbook shift-share design with roughly **30 shocks** (the 30 largest bank holding companies). Thirty is more than a handful but far from the hundreds in the labor-demand case, and during a banking crisis exposure is likely **concentrated**, not dispersed — a few giant holding companies (the ones at the center of 2008–09) probably dominate deposits across many commuting zones, so the *effective* number of shocks is well below 30. Given moderate-but-concentrated shocks, **BHJ (quasi-random shifts)** is the more natural *primary* defense (there are enough banks to talk about a shock-level quasi-experiment), but it is shaky enough that **GPSS (exogenous shares)** should be carried as a serious *backup* — and the honest move is to report both and let the diagnostics (a low $K_{\text{eff}}$ would force a retreat to GPSS) decide.

**(b) (4 pts)** **Shift-side argument:** the 2007–09 national lending changes of these 30 holding companies are as-good-as-random with respect to *which regions* were exposed to them — banks contracted for reasons (their own capital and securitization positions) unrelated to the latent trajectories of the specific regions where they happened to hold deposits. **Concrete threat:** during 2007–09 the banks that contracted lending most were precisely those most loaded with subprime mortgage exposure — and their *pre-crisis branch footprints were not random*. They had expanded aggressively into exactly the frothy housing markets (Sun Belt sand states) that were about to crater on their own. So the "shock" (a bank's national contraction) is correlated with the latent regional trajectory through the bank's non-random footprint — the shift is not quasi-random with respect to exposure. This is a genuine threat to the BHJ defense.

**(c) (4 pts)** **Share-side argument:** 2006 deposit shares are unrelated to a region's *other* determinants of small-business closure — initial bank mix is a historical accident with respect to the latent business-fragility trajectory in $\varepsilon_r$. **Concrete back-door story:** regions banking heavily with the most crisis-exposed institutions in 2006 were *also* the regions with the frothiest housing markets and the weakest pre-crisis small-business balance sheets (those markets attracted the aggressive lenders in the first place). Then the deposit share predicts business closures through a back door — the region was economically overheated and due for a fall — rather than only through the credit-supply channel. Exogenous shares fails. (Note this is *the same underlying fact* as the shift-side threat in (b), seen from the share side: when the danger is the bank–region footprint correlation, it can break *both* views at once, which is the worst case.)

**(d) (4 pts)** Two concrete diagnostics:

1. *Share defense:* run a **balance / pre-trend test of the 2006 deposit shares against pre-period regional covariates and pre-trends** (e.g. 2002–06 house-price growth, prior closure trends), plus a **Rotemberg-weight ranking** to see which banks drive the estimate. A *failing* result: the high-weight banks' shares are strongly correlated with pre-crisis house-price froth, or the estimate is riding on two or three banks whose shares fail balance — meaning the result is a story about those few exposures, not a clean credit-supply effect.
2. *Shift defense:* compute the **effective number of shocks** $K_{\text{eff}}=1/\sum_k\omega_k^2$ over the 30 holding companies, plus a **shock-balance check** of the national lending changes against bank-level pre-crisis characteristics (e.g. subprime exposure). A *failing* result: $K_{\text{eff}}$ is far below 30 (a few giant banks carry all the exposure weight, so "30 shocks" is an illusion), and/or the contraction shocks correlate with banks' pre-crisis subprime loadings — meaning the shocks were not quasi-randomly assigned across exposure.

---

## Problem 6 — Connecting back to IV: relevance, exclusion, and honest inference (16 pts)

**(a) (4 pts)** Translating the two IV conditions for $B_r$:

- **Relevance:** $\operatorname{Cov}(B_r,\Delta C_r)\neq0$. The bank-mix prediction must actually move realized local credit growth — regions predicted to ride contracting banks must really have slower credit growth (the first stage). **Testable.**
- **Exclusion:** $\operatorname{Cov}(B_r,\varepsilon_r)=0$, i.e. $B_r$ affects delinquency *only through* realized credit growth $\Delta C_r$ and is uncorrelated with everything else in $\varepsilon_r$. **Must be argued.**

This is **exactly** the Ch 3.4 split: relevance lives in observed variables and gets a first-stage F; exclusion lives in the unobserved error and can only be defended from the design. A shift-share instrument earns no exemption — it is still an instrument.

**(b) (4 pts)** The product structure gives "two shots" because of a simple algebraic fact: **a product $B_r=\sum_k s_{rk}g_k$ is uncorrelated with the error if *either* factor's variation is uncorrelated with the error.** If the *shares* are exogenous (GPSS), then any shifts may serve as weights and $\operatorname{Cov}(B_r,\varepsilon_r)=0$ follows from the share side. If instead the *shifts* are as-good-as-random across many industries (BHJ), then any shares may serve as exposure and $\operatorname{Cov}(B_r,\varepsilon_r)=0$ follows from the shift side. So exclusion — the single hardest, untestable IV assumption — can be sourced from whichever ingredient you can most credibly call exogenous; it is a legitimate *either/or*, not a *both-required*. The honest empiricist names which shot they are taking, given the data regime (few concentrated shares $\to$ shares; many dispersed shocks $\to$ shifts).

**(c) (4 pts)** Two commuting zones on opposite coasts that are both heavily exposed to the *same* bank receive a *common* shock through that shared exposure: when that bank contracts, both regions' credit (and outcomes) move together, so their regression errors are **correlated through the shared shifter** even though the regions share no geographic cluster. Ordinary by-state clustering (Problem 5) only allows correlation *within* a state and assumes regions in different states are independent — so it **completely misses** this cross-regional, cross-state correlation induced by shared exposure, making the reported standard errors **too small** and the tests over-reject. **Adão–Kolesár–Morales (2019)** derived standard errors valid under this exposure-induced cross-regional correlation; those are the honest choice. One alternative that gets correct inference "for free": the **BHJ shock-level regression**, which by construction clusters at the *shock (bank/industry) level* and therefore accounts for the shared-shock dependence automatically.

**(d) (4 pts)** A referee's four-line checklist:

1. **Relevance:** always report the first stage and its strength — the **Olea–Pflueger effective F** under clustered/heteroskedastic errors, not the eyeballed "$F>10$" (significance is not strength; a weak first stage drags 2SLS toward OLS).
2. **Name your exclusion defense for your data regime, with its diagnostic:** with few, concentrated shares, claim **GPSS exogenous shares** and back it with a **share balance/pre-trend test plus a Rotemberg-weight ranking** showing which shares drive the estimate (and survive dropping them).
3. **The other-regime diagnostic if your data favor it:** with many, dispersed shocks, claim **BHJ quasi-random shifts** and back it with the **effective number of shocks $K_{\text{eff}}=1/\sum_k\omega_k^2$ plus a shock-balance check** against industry-level confounders.
4. **Inference fix:** report **AKM-robust standard errors (Adão–Kolesár–Morales 2019)** — or run the **BHJ shock-level regression** — so that the cross-regional correlation from shared exposure does not lie to you about precision; never settle for vanilla region- or state-clustered standard errors.

---

*End of solutions for PS 4.5. Cross-references: Ch 4.5 (shift-share construction $B_r=\sum_k s_{rk}g_k$; shares-vs-shifts variation; GPSS exogenous-shares view and Rotemberg decomposition; BHJ quasi-random-shifts view and effective number of shocks; the "product exogenous if either factor is" unification; AKM cross-regional inference), Ch 3.4 (relevance/exclusion asymmetry, testable vs argued, LATE-style weighted-average estimands), Ch 3.5 (significance≠strength, Olea–Pflueger effective F, weak-IV drift toward OLS), Ch 4.1 (parallel-trends/pre-trend tests reused for share and shock balance), Ch 4.2 (Rotemberg/negative-weights spirit — headline as weighted average of building blocks), Ch 2.4 (clustering and the structure of dependence). Numeric keys: P1 $B_{\text{Lake}}=-3.9\%$, $B_{\text{Mill}}=+2.0\%$, identical-shares $=-1.1\%$ (kills share dispersion), common-shift $=+2.0\%$ (kills shift dispersion); P2 $t=8.5\Rightarrow F=72.25$ (clears 10, relevance only); P3 weights sum to 1.00, reassembled $\hat\beta_1^{\text{Bartik}}=+0.60$, BigCommerce dominates at $70\%$ of weight (contributes $0.56$), Pinebluff wrong-signed but only $0.03$ weight; P4 $K_{\text{eff}}=5.0$ (dispersed) vs $\approx1.53$ (concentrated, $\sum\omega^2=0.6538$); Maya's 6-bank case $\Rightarrow$ GPSS only. Closes the Weeks 3–4 causal-inference arc; bridges to Weeks 5–6 reading-the-frontier (defend shares or shifts, show Rotemberg weights, count effective shocks, AKM-robust SEs).*
