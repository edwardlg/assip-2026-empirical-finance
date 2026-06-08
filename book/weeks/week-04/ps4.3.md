# Problem Set 4.3 — Regression Discontinuity: Local-Polynomial Fitting and Bandwidth Experiments

*Covers Ch 4.3. Methods allowed: everything through Ch 4.3 — the **sharp-RD estimand** $\tau_{\text{SRD}}=\lim_{x\downarrow c}\mathbb{E}[Y\mid X=x]-\lim_{x\uparrow c}\mathbb{E}[Y\mid X=x]$ and the **continuity / local-randomization** assumption; **local linear estimation** with a window of half-width $h$ (the bandwidth) and a **triangular kernel**; the **bias–variance trade-off** in $h$ and why local-linear beats a global high-order polynomial (Gelman–Imbens 2019); the data-driven bandwidth choices of **Imbens–Kalyanaraman (2012)** and the robust bias-corrected inference of **Calonico–Cattaneo–Titiunik (2014)**; **fuzzy RD** as the Wald ratio $\tau_{\text{FRD}}=(\text{jump in }Y)/(\text{jump in }D)$ with the above-cutoff indicator $Z_i=\mathbf 1\{X_i\ge c\}$ as the instrument; the **McCrary (2008) density test** for manipulation; and the validity-threat checklist of §9 (manipulation, covariate imbalance, compound treatments, donut, bandwidth sensitivity). You may treat OLS, the Wald estimator and LATE/compliers (Week 3), and weak-instrument logic (Ch 3.5) as known. Show your reasoning; a boxed number with no argument earns no credit, and whenever you invoke an assumption you must **name it** — "continuity," "relevance," "exclusion," "monotonicity" — never just "the assumption."*

**Total: 100 points.** Six problems, escalating. Problem 1 is conceptual (state the sharp-RD estimand and the continuity assumption, and contrast it with CIA). Problem 2 is a by-hand local-linear RD: fit a line on each side of the cutoff and read the jump. Problem 3 is the bandwidth bias–variance problem (what happens as $h$ shrinks and grows; why local linear, not a global quartic — Gelman–Imbens). Problem 4 is a fuzzy-RD problem (jump in treatment probability $\to$ Wald ratio, connected back to Week-3 IV). Problem 5 is a McCrary-density/manipulation problem (what sorting does and how the density test detects it). Problem 6 is a validity-threats critique (compound treatments at the same cutoff).

One idea runs through every problem, so hold it from the start. **RD reads a causal effect off a jump: the vertical gap in $\mathbb{E}[Y\mid X]$ exactly at the cutoff $c$.** Continuity says that, absent the treatment, the outcome would have passed through $c$ smoothly, so the gap can only be the treatment. Local linear regression is just the honest way to read the height of each side's curve *at* $c$; the bandwidth is how wide a window you trust; fuzzy RD divides the outcome jump by the treatment jump exactly as the Week-3 Wald estimator did; and the validity tests all ask the same single question — *is the jump really the treatment, or is something else also jumping at $c$?*

We use the chapter's two running cutoffs: Sam's Russell 1000/2000 reconstitution-rank cutoff (recentered so $c=0$, with $X\ge 0$ landing in the Russell 2000) and Maya's lender credit-score cutoff at $660$.

---

## Problem 1 — State the estimand and the identifying assumption (14 points)

Maya studies an automated lender that approves every applicant with a credit score $X_i\ge 660$ and rejects everyone below, with the loan officer having no discretion. The treatment is loan approval, $D_i=\mathbf 1\{X_i\ge 660\}$, and the outcome $Y_i$ is the applicant's two-year financial-distress index (lower is better). She wants the causal effect of approval.

**(a) (3 pts)** Write the sharp-RD estimand $\tau_{\text{SRD}}$ for Maya's design as a difference of two one-sided limits, in the notation of Ch 4.3. In one sentence, say in plain words what each limit is and why their difference is a treatment effect rather than just "the slope of $Y$ in $X$."

**(b) (4 pts)** State the **continuity** assumption formally, in potential-outcomes language ($Y_i(1),Y_i(0)$), and translate it into one plain-English sentence about what *would have happened* to a barely-approved applicant had the cutoff sat slightly higher. Which of the two potential-outcome functions is the one we never directly observe on the treated side, and which side of the cutoff supplies it?

**(c) (4 pts)** The chapter calls RD's assumption "weaker than CIA, and partly checkable." Explain, in two or three sentences, the precise difference: what does CIA (Week 3) demand, what does continuity demand instead, and *why* does that make continuity easier to defend?

**(d) (3 pts)** Maya's estimate $\tau_{\text{SRD}}$ is the effect of approval **for whom**? Name the population, and say in one sentence why this "local" estimand is nonetheless exactly the right number for a regulator deciding whether to move the cutoff from $660$ to $650$.

---

## Problem 2 — A by-hand local-linear RD (20 points)

Sam bins stocks by reconstitution-rank distance from the cutoff ($c=0$; $X\ge 0$ is the Russell 2000, treated) and computes mean next-year passive-fund ownership (in percentage points) in each bin. Working within a bandwidth of $h=4$, he keeps the four bins inside the window and reads off the bin midpoints:

| Bin midpoint $x$ | Side | Mean passive ownership $\overline Y$ (%) |
|---:|---|---:|
| $-3$ | control (R1000) | $5.2$ |
| $-1$ | control (R1000) | $5.4$ |
| $+1$ | treated (R2000) | $5.9$ |
| $+3$ | treated (R2000) | $6.1$ |

Treat each side as exactly two points, so the local-linear fit on each side is just the straight line through its two points.

**(a) (6 pts)** Fit the **control-side** line $Y=a_- + b_-\,x$ through $(-3,5.2)$ and $(-1,5.4)$. Compute the slope $b_-$ and intercept $a_-$, then the extrapolated control-side height **at the cutoff**, $\lim_{x\uparrow 0}\widehat{\mathbb{E}}[Y\mid X=x]=a_-$. Show the two-point slope calculation.

**(b) (6 pts)** Fit the **treated-side** line $Y=a_+ + b_+\,x$ through $(+1,5.9)$ and $(+3,6.1)$. Compute $b_+$, $a_+$, and the extrapolated treated-side height at the cutoff, $\lim_{x\downarrow 0}\widehat{\mathbb{E}}[Y\mid X=x]=a_+$.

**(c) (4 pts)** Report $\hat\tau_{\text{SRD}}=a_+-a_-$. Explain in one sentence why this is *not* simply the difference of the two nearest bins ($5.9-5.4=0.5$), and what the local-linear fit corrects for.

**(d) (4 pts)** Sam considers replacing the local-linear fit with the crude "nearest-bin difference" $5.9-5.4$. State which estimate is bigger, and explain — using the *direction of the side-trends* you found in (a) and (b) — whether the nearest-bin shortcut is biased up or down relative to the local-linear jump, and why. (No triangular-kernel weighting is needed here because each side has only two equidistant points; state in one line why the kernel would not change a two-point line.)

---

## Problem 3 — Bandwidth, bias, variance, and the global-polynomial trap (18 points)

This problem uses the verified simulation of Ch 4.3 §11. The data-generating process has a **true jump of $\tau=0.6$**; the smooth part of $\mathbb{E}[Y\mid X]$ is *flat-ish* below the cutoff but **convex (curving upward) on the treated side**. The chapter reports these local-linear estimates:

| Bandwidth $h$ | $\hat\tau$ | $\widehat{\text{se}}(\hat\tau)$ |
|---:|---:|---:|
| $4$ | $0.56$ | $0.18$ |
| $32$ | $0.41$ | $0.07$ |

and, for contrast, a **global quartic** fit to all $6{,}000$ points reports $\hat\tau\approx 0.41$ with a *tight-looking* standard error.

**(a) (5 pts)** Explain the bias–variance trade-off across the two bandwidths using the table's own numbers. As $h$ goes from $4$ to $32$: which way does the standard error move, and why (in terms of how many points each fitted line uses)? Which way does the *bias* move, and why (in terms of the curvature on the treated side)?

**(b) (3 pts)** At $h=4$ the estimate is close to the truth ($0.56$ vs $0.60$) but the confidence interval $\hat\tau\pm 1.96\,\widehat{\text{se}}$ is wide; at $h=32$ the interval is narrow but mis-centered. Compute both naive $95\%$ intervals and state, in one sentence, which window an *honest* analyst should prefer and why "narrow" is not the same as "accurate."

**(c) (5 pts)** The global quartic returns essentially the *same biased point estimate* ($0.41$) as the too-wide local-linear fit, but with a deceptively tight standard error. Give the **Gelman–Imbens (2019)** argument in three sentences: name the three reasons a high-order global polynomial mis-estimates a boundary value, and say what the "deceptively tight standard error around a wrong number" reveals about the difference between precision and accuracy.

**(d) (5 pts)** Name the two data-driven bandwidth procedures from the chapter and state precisely what each delivers: (i) what quantity does **Imbens–Kalyanaraman (2012)** minimize, and what does that imply about whether their optimal $h$ leaves any bias behind? (ii) Given that the IK/MSE-optimal bandwidth deliberately leaves a non-negligible bias, what *two* things does **Calonico–Cattaneo–Titiunik (2014)** robust bias-correction do to repair the confidence interval, and what coverage problem does it fix?

---

## Problem 4 — Fuzzy RD as the Wald ratio (18 points)

In modern Russell data the design is *fuzzy*: crossing the rank cutoff does not force a fixed amount of passive ownership; it raises the *probability and intensity* of heavy Russell-2000-tracking ownership. Sam defines the treatment $D_i=1$ as "heavy passive uptake" and estimates four boundary limits (each read off a local-linear fit, $h$ fixed):

| Boundary limit | Value |
|---|---:|
| $\lim_{x\downarrow 0}\mathbb{E}[D\mid X=x]$ (treated-side treatment share) | $0.70$ |
| $\lim_{x\uparrow 0}\mathbb{E}[D\mid X=x]$ (control-side treatment share) | $0.30$ |
| $\lim_{x\downarrow 0}\mathbb{E}[Y\mid X=x]$ (treated-side outcome, governance index) | $61.0$ |
| $\lim_{x\uparrow 0}\mathbb{E}[Y\mid X=x]$ (control-side outcome, governance index) | $57.4$ |

The outcome $Y$ is a firm-governance index (higher = more shareholder-friendly).

**(a) (4 pts)** Compute the **jump in treatment** (the first stage) and the **jump in outcome** (the reduced form) at the cutoff. Name the condition that the treatment jump is the empirical content of, and say whether $0.40$ is reassuring or worrying on that score.

**(b) (4 pts)** Compute the **fuzzy-RD estimand** $\hat\tau_{\text{FRD}}$ as the ratio of the two jumps. Write the ratio explicitly in the form (jump in $Y$)/(jump in $D$), and interpret the number: what does heavy passive ownership do to the governance index, and *for which firms*?

**(c) (4 pts)** Identify the instrument $Z_i$ in this design and map each piece of the ratio to its Week-3 name. Which jump is the "first stage," which is the "reduced form," and why is $\hat\tau_{\text{FRD}}$ literally the Wald estimator from Ch 3.4?

**(d) (3 pts)** State what **exclusion** means *here*, in RD language: what must crossing the rank cutoff do (and not do) to the governance index? Give one concrete channel that, if real, would violate it — and note which §9 threat that channel is an instance of.

**(e) (3 pts)** Suppose FTSE Russell's banding rules weakened, so the treatment jump fell from $0.40$ to $0.05$ while the outcome jump stayed near $3.6$. Without recomputing precisely, say what happens to the fuzzy-RD *point estimate* and, more importantly, to its *precision*, and name the Ch 3.5 pathology this is an instance of.

---

## Problem 5 — The McCrary density test and manipulation (16 points)

Maya worries that applicants (or loan officers helping them) can nudge a credit score from just below $660$ to just above by paying down a small balance right before the pull — but only the more financially-capable applicants know to do this.

**(a) (4 pts)** Describe the **McCrary (2008) density test** in words: what object does it estimate on each side of the cutoff, what is the null hypothesis, and what does *rejecting* the null indicate? State what you *hope* to see (reject or fail to reject) and why.

**(b) (4 pts)** Explain the **fingerprint** of the specific manipulation Maya fears. If capable applicants sort from just-below to just-above $660$, what happens to the *histogram* of credit scores in the bins immediately below and immediately above $660$? Draw the link from "sorting" to "a jump in the density at $c$."

**(c) (4 pts)** Explain *why* this sorting breaks the design even though approval still flips cleanly at $660$. Use the **local-randomization / continuity** language: which group becomes "enriched," on what kind of characteristic, and why are the just-above and just-below applicants no longer exchangeable? What does the resulting $\hat\tau_{\text{SRD}}$ now mix together?

**(d) (4 pts)** Maya runs the test and *fails to reject* the null (the density looks smooth through $660$). Her labmate says, "Great — the density test passed, so the design is clean." Give the two-part correct response: (i) why a passed density test is *necessary but not sufficient*, and (ii) name one validity threat from §9 that a passed density test cannot rule out at all.

---

## Problem 6 — Validity threats: the compound-treatment critique (14 points)

Maya finds a large, clean-looking jump in two-year default rates at the credit-score cutoff of $660$: the density test passes, and a covariate-balance RD on pre-application debt-to-income shows no jump. She is ready to write "approval raises defaults by $\hat\tau$." Then she learns that, at *exactly* $660$, the lender's underwriting system *also* (i) switches the loan from a fixed to a lower variable interest rate, and (ii) makes the loan eligible for securitization (which changes who services it).

**(a) (4 pts)** Name this validity threat from §9 and state, in one sentence, the single sentence that summarizes when RD is identified — the sentence this threat violates.

**(b) (4 pts)** Explain why **no statistical test** — not McCrary, not covariate balance, not a donut, not a bandwidth sweep — can detect this problem. Contrast it explicitly with the manipulation threat of Problem 5, which *does* leave a statistical fingerprint. What kind of evidence must Maya use instead?

**(c) (3 pts)** Reframe the situation honestly: Maya's RD still estimates *a* real causal effect. Of *what*? Write the precise object her $\hat\tau$ identifies, and explain why it is not the "effect of approval" she wanted.

**(d) (3 pts)** Connect this to fuzzy RD's **exclusion** restriction (Problem 4). If Maya's design were fuzzy, with the above-$660$ indicator as the instrument for approval, which IV condition does the compound treatment break, and through what mechanism does it contaminate the Wald ratio? (One or two sentences; name the condition.)

---

*End of PS 4.3. Solutions in `book/appendices/E-solutions-manual/E-w4-ps4.3-solutions.md`. The hands-on companion is **nb4.3 — "RD with `rdrobust`; CCT bandwidths"**: there you re-do Problem 2's hand-rolled local-linear fit against the package's data-driven CCT bandwidth and robust bias-corrected interval, watch Problem 3's bias–variance trade-off and the Gelman–Imbens global-polynomial pathology in live numbers, run the McCrary/Cattaneo–Jansson–Ma density test of Problem 5, and switch to the fuzzy design of Problem 4 to recover the effect via the IV/Wald ratio while precision collapses as the first-stage jump shrinks.*
