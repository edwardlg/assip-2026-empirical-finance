# Problem Set 4.5 — Shift-Share Exposure Weights and the Identification Critique

*Covers Ch 4.5, and leans on Week 3 IV. Methods allowed: everything through Ch 4.5 — the shift-share / Bartik construction $B_r=\sum_k s_{rk}\,g_k$ from baseline local exposure shares $s_{rk}$ (with $\sum_k s_{rk}=1$) and national shifts $g_k$; the canonical local-shock design (instrument the realized local shock with $B_r$); the two identification views — **Goldsmith-Pinkham–Sorkin–Swift (2020)** "identification from the shares" (exogenous initial shares; Rotemberg-weight decomposition $\hat\beta_1^{\text{Bartik}}=\sum_k\hat\alpha_k\,\hat\beta_{1,k}$, $\sum_k\hat\alpha_k=1$) and **Borusyak–Hull–Jaravel (2022)** "identification from the shifts" (quasi-random shocks across many dispersed industries; effective number of shocks); the **Adão–Kolesár–Morales (2019)** inference problem (cross-regional error correlation from shared exposure); and all of Ch 3.4 IV (relevance $\operatorname{Cov}(Z,D)\neq0$ testable; exclusion $\operatorname{Cov}(Z,\varepsilon)=0$ untestable; first-stage F; LATE-style weighted-average estimands). You may treat OLS, FWL (Ch 2.3), clustering (Ch 2.4), and the IV machinery (Ch 3.4–3.5) as known. Show your reasoning; a boxed number with no argument earns no credit, and any time you invoke a condition you must **name it** — "relevance," "exclusion," "exogenous shares," or "quasi-random shifts" — never just "the assumption."*

**Total: 100 points.** Six problems, escalating. Problem 1 constructs Bartik instruments by hand from shares and shifts (arithmetic). Problem 2 is the relevance / first-stage problem (why $B_r$ predicts the realized local shock). Problem 3 is the GPSS "identification from the shares" view (what must be exogenous; which industries drive the estimate, via Rotemberg weights). Problem 4 is the BHJ "identification from the shifts" view (as-good-as-random shocks; the effective number of shocks). Problem 5 is a design-critique problem (argue which assumption is credible in a described design and how you'd diagnose it). Problem 6 is the connection-to-IV problem (relevance and exclusion translated into shift-share terms, plus AKM inference).

One idea runs through every problem, so hold it from the start. A shift-share instrument $B_r=\sum_k s_{rk}\,g_k$ is a *product* of two ingredients — local shares and national shifts — and a product is exogenous to the error if *either* factor is. So the single hardest, untestable assumption in all of IV (exclusion) gets *two* independent shots in a shift-share design: defend the **shares** (GPSS) or defend the **shifts** (BHJ). Which shot is honest depends on your data — few concentrated shares push you toward the share story, many dispersed shocks toward the shift story. Every problem below is, at bottom, about that fork: which factor can you credibly call exogenous, and what diagnostic backs it up.

Throughout, Maya anchors the finance setting: regional **bank-lending** exposure and its effect on **household credit / delinquency**. Outcome $Y_r$ is the change in region $r$'s household-debt delinquency rate; the endogenous regressor is the realized local credit-supply growth $\Delta C_r$; the instrument is the bank-mix prediction $B_r$.

---

## Problem 1 — Construct the Bartik instrument by hand (16 points)

Maya builds a **bank-lending** shift-share instrument. There are three banks. The **shifts** $g_b$ are each bank's national lending growth over the year (computed *leaving out region $r$*, so the region cannot have caused them). The **shares** $s_{rb}$ are the fraction of each region's baseline deposits held by each bank (rows sum to one). Two of her regions:

| Bank $b$ | National shift $g_b$ | Lakeside share $s_{rb}$ | Mill Hollow share $s_{rb}$ |
|---|:---:|:---:|:---:|
| BigCommerce Bank | $+4\%$ | $0.20$ | $0.70$ |
| Heartland Savings | $-10\%$ | $0.50$ | $0.10$ |
| Coastal Credit Union | $+1\%$ | $0.30$ | $0.20$ |

**(a) (3 pts)** Confirm both regions' shares are valid exposure weights (state the condition the rows must satisfy and check it).

**(b) (5 pts)** Compute the Bartik instrument $B_r=\sum_b s_{rb}\,g_b$ for **Lakeside** and for **Mill Hollow**. Show each product term. Report each $B_r$ as a percentage.

**(c) (3 pts)** In one or two sentences, interpret the two numbers in Maya's setting: what predicted credit-supply shock does each region get, and *why* do the two regions differ even though they face the *identical* three national shifts?

**(d) (3 pts)** Suppose every region in Maya's sample held *exactly* the same deposit shares $(0.40, 0.30, 0.30)$. Compute $B_r$ for such a region, and explain in one sentence why a shift-share instrument built this way would instrument *nothing* — tie your answer to which kind of variation (share dispersion or shift dispersion) has been destroyed.

**(e) (2 pts)** Separately, suppose instead that all three banks had the *same* national shift, $g_b=+2\%$ for every $b$, but regions kept their different shares. Compute $B_r$ for Lakeside under this scenario and explain in one sentence why $B_r$ is again a constant across regions — naming the other kind of variation that has now been destroyed.

---

## Problem 2 — Relevance / the first stage (14 points)

Maya now treats $B_r$ as an instrument for the realized local credit-supply growth $\Delta C_r$, in the spec (state it in the CONVENTIONS §4 discipline): **outcome** = change in regional delinquency rate $Y_r$; **key regressor** = realized regional credit growth $\Delta C_r$; **controls** = baseline region demographics; **fixed effects** = region and period; **clustering** = (to be revisited in Problem 6); **sample** = U.S. commuting zones over the period; **identifying assumption** = $B_r$ is as-good-as-randomly assigned, defended in Problems 3–4.

**(a) (4 pts)** Write the **first-stage** regression Maya runs (regress what on what?), and state the **relevance** condition both as a covariance statement involving $B_r$ and $\Delta C_r$ and in plain words. Why should we *expect* relevance to hold here — i.e., why would a region predicted to ride contracting banks actually experience slower realized credit growth?

**(b) (4 pts)** Maya's first stage gives a coefficient on $B_r$ of $\hat\pi_1=0.85$ with standard error $0.10$. Compute the t-statistic and, since there is a single instrument, the first-stage F. Does this clear the "$F>10$" rule of thumb? State explicitly which of the two IV conditions this F-statistic speaks to.

**(c) (3 pts)** A colleague says, "The first stage is significant, so relevance is settled — and that means my instrument is *valid*." Correct him in two sentences: distinguish which condition the first-stage F can confirm and which it can say *nothing* about, and connect this to the testable/untestable asymmetry from Ch 3.4.

**(d) (3 pts)** Recall from Ch 3.5 that "significance is not strength." Maya's data are clustered and heteroskedastic. Name the kind of first-stage statistic she should report instead of the classical F, and in one sentence say why a *weak* shift-share first stage is dangerous — what does 2SLS drift back toward as the first stage weakens?

---

## Problem 3 — Identification from the shares: GPSS and Rotemberg weights (20 points)

Goldsmith-Pinkham, Sorkin and Swift (2020) showed that running 2SLS with the single instrument $B_r$ is numerically equivalent to using each baseline share $s_{rk}$ as a *separate* instrument, with the shifts $g_k$ supplying the weights.

**(a) (4 pts)** In the cross-section of regions in a given period, the national shifts $g_b$ are *fixed numbers* — the same for every region. Using that fact, explain in two or three sentences why GPSS conclude that "whatever makes $B_r$ valid must be a statement about the **shares**." What is the *only* thing varying across regions in $B_r=\sum_b s_{rb}\,g_b$?

**(b) (4 pts)** State the **GPSS identifying assumption** ("exogenous shares") both as a conditional-expectation statement involving the region error $\varepsilon_r$ and the shares, and in plain words. What does this assumption let the *shifts* off the hook from — i.e., what are the shifts allowed to be, under the GPSS view?

**(c) (4 pts)** Give one concrete, specific back-door story by which a baseline **bank share** could violate exogenous-shares for Maya's *delinquency* outcome. (Construct a story in which the region's initial bank mix is correlated with latent household fragility sitting in $\varepsilon_r$, so the share predicts delinquency through a channel *other than* the credit-supply shock.)

**(d) (5 pts)** GPSS show the Bartik estimate decomposes as a weighted average of per-instrument estimates,
$$
\hat\beta_1^{\text{Bartik}}=\sum_k \hat\alpha_k\,\hat\beta_{1,k},\qquad \sum_k \hat\alpha_k=1,
$$
where $\hat\beta_{1,k}$ is the IV estimate using only share $k$ as the instrument and $\hat\alpha_k$ is its **Rotemberg weight**. Maya's headline estimate is $\hat\beta_1^{\text{Bartik}}=+0.6$ (a predicted credit contraction raises delinquency). Her Rotemberg decomposition over four bank-instruments reads:

| Bank $k$ | Rotemberg weight $\hat\alpha_k$ | Per-instrument estimate $\hat\beta_{1,k}$ |
|---|:---:|:---:|
| BigCommerce Bank | $0.70$ | $+0.80$ |
| Heartland Savings | $0.22$ | $+0.20$ |
| Coastal Credit Union | $0.05$ | $+0.10$ |
| Pinebluff Mutual | $0.03$ | $-0.30$ |

First verify the weights sum to one. Then compute $\sum_k\hat\alpha_k\,\hat\beta_{1,k}$ and confirm it reassembles the headline $+0.6$. Finally, state which single bank's share-instrument *dominates* the estimate, and what fraction of the weight it carries.

**(e) (3 pts)** Given the table, where should Maya aim her share-exogeneity skepticism *first*, and what is the single most informative robustness check she should run? (Connect to the spirit of the Rotemberg-weight / negative-weights idea from Ch 4.2: a headline estimate is a weighted average of building blocks, so look at the weights.) Note also the one bank whose per-instrument estimate has the *wrong sign* — does its low weight make it harmless, and why or why not in one sentence?

---

## Problem 4 — Identification from the shifts: BHJ and the effective number of shocks (18 points)

Borusyak, Hull and Jaravel (2022) locate identification not in the shares but in the **shifts**, viewed as a quasi-experiment over industries (or, here, banks).

**(a) (4 pts)** State the **BHJ identifying assumption** ("quasi-random shifts") in words: what is treated as the random object, what must be true of it, and how many of them do you need? Critically, what does the BHJ view let the *shares* be — and why is this exactly the opposite license from the GPSS view?

**(b) (4 pts)** Explain the law-of-large-numbers logic in two or three sentences: why does having *many* dispersed shocks make the exposure-weighted average $B_r=\sum_k s_{rk}\,g_k$ behave like a clean region-level experiment, and what goes wrong with that logic when there are only a *handful* of shocks?

**(c) (5 pts)** BHJ warn that the *nominal* number of shocks can overstate the *effective* number when a few shocks carry most of the exposure weight. A simple Herfindahl-style effective count is
$$
K_{\text{eff}}=\frac{1}{\sum_k \omega_k^2},
$$
where $\omega_k\ge0$ are the (normalized, $\sum_k\omega_k=1$) aggregate exposure weights on each shock. Consider two of Maya's sub-samples, each with **five** banks:

- *Sample A (dispersed):* weights $\omega=(0.20,\,0.20,\,0.20,\,0.20,\,0.20)$.
- *Sample B (concentrated):* weights $\omega=(0.80,\,0.10,\,0.05,\,0.03,\,0.02)$.

Compute $K_{\text{eff}}$ for each sample. (Show the sum of squares.) Even though both have five banks nominally, what does $K_{\text{eff}}$ tell you about which sample can honestly invoke the BHJ "many shocks" story?

**(d) (3 pts)** Maya's full bank sample has only six banks, two of which hold most deposits region-by-region, while the labor-demand version of the design she read about had several hundred industries. State which identification view — GPSS or BHJ — she can honestly invoke in her *bank* setting, and why the *other* view fails in her data. (One or two sentences; tie it to $K_{\text{eff}}$ and to "how many shocks.")

**(e) (2 pts)** Name the natural BHJ-style diagnostic Maya would report to defend the shift side (other than $K_{\text{eff}}$), and say in one sentence what it is the shock-level analogue *of* on the share side.

---

## Problem 5 — Critique a described design (16 points)

A team studying the **2008–09 financial crisis** writes: *"We estimate the effect of local credit-supply contraction on small-business closures across 700 U.S. commuting zones. We instrument realized local credit growth with a shift-share instrument: baseline 2006 deposit shares of each of the 30 largest U.S. bank holding companies, times each holding company's national (leave-one-region-out) change in lending from 2007 to 2009. We report a strong first stage (effective F = 48) and cluster our standard errors by state."*

**(a) (4 pts)** Classify this design. Roughly how many shocks does it have, and how dispersed is exposure likely to be? Based on that, which identification view (GPSS or BHJ) is the *more* natural primary defense here, and which is the *backup*? Justify in two or three sentences.

**(b) (4 pts)** State the **shift-side** credibility argument and one concrete threat to it. Specifically: for the *quasi-random shifts* assumption to hold, the national lending changes of these 30 holding companies must be as-good-as-random with respect to which regions are exposed to them. Give one concrete reason this could *fail* during 2007–09 (think about what was systematically true of the banks that contracted lending most, and whether their pre-crisis footprints were random across regions).

**(c) (4 pts)** State the **share-side** credibility argument and one concrete threat to it. Specifically: for the *exogenous shares* assumption, 2006 deposit shares must be unrelated to the regions' *other* determinants of small-business closure. Give one concrete back-door story (think: were regions banking heavily with the most crisis-exposed institutions *also* regions with, e.g., the frothiest housing markets or weakest pre-crisis business balance sheets?).

**(d) (4 pts)** Propose **two** concrete diagnostics the team should run — one suited to the share defense and one suited to the shift defense — and say in one sentence each what a *failing* result would look like. (Hint: one is a balance/pre-trend test on the shares plus a Rotemberg-weight ranking; the other is an effective-number-of-shocks count plus a shock-balance check.)

---

## Problem 6 — Connecting back to IV: relevance, exclusion, and honest inference (16 points)

Map the whole shift-share machine onto the Ch 3.4 IV vocabulary.

**(a) (4 pts)** Translate **relevance** and **exclusion** into shift-share terms for Maya's bank design. For each: write the condition involving $B_r$, and say in one sentence what it requires of the bank-mix prediction. Which one is *testable* and which must be *argued* — and is that the same testable/untestable split you learned for a generic instrument in Ch 3.4?

**(b) (4 pts)** Explain the chapter's central unification in two or three sentences: *why* does the product structure $B_r=\sum_k s_{rk}\,g_k$ give you "two shots" at the single untestable exclusion restriction? State the algebraic fact about products and errors that makes "defend the shares OR defend the shifts" a legitimate either/or rather than a both-required.

**(c) (4 pts)** Adão, Kolesár and Morales (2019) showed that standard shift-share standard errors are too small. Explain the mechanism in two or three sentences: *why* are the regression errors of two commuting zones on opposite coasts correlated when both are heavily exposed to the same bank, even though they share no geographic cluster — and what does that do to the team's by-state clustering from Problem 5? Then name what kind of standard errors fix this, and one alternative route (from BHJ) that gets honest inference "for free."

**(d) (4 pts)** Synthesize the chapter's verdict in your own words as a four-line checklist a referee would demand of *any* shift-share paper: (i) the relevance check you always report; (ii) which exclusion defense you *name* given your data regime, and the diagnostic that backs it; (iii) the other diagnostic you'd add if your data instead favored the *other* regime; (iv) the inference fix that keeps your standard errors honest, with the authors who derived it. Be specific and name names.

---

*End of PS 4.5. Solutions in `book/appendices/E-solutions-manual/E-w4-ps4.5-solutions.md`. This set closes Week 4 and the full Weeks 3–4 causal-inference arc. The reflex it drills — name the threat, name which exogeneity assumption your data lets you defend, separate what you can test from what you must argue, and bring the matching diagnostic — is exactly the lens Weeks 5–6 hand you for reading frontier empirical papers tables-first, including ones that say "we instrument local exposure with a Bartik shift-share design." When you meet that sentence in a published paper, you will not nod along; you will ask whether they defended the shares or the shifts, whether they showed Rotemberg weights, how many effective shocks they had, and whether their standard errors are AKM-robust.*
