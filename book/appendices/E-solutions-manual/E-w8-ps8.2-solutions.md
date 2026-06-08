# Model Deliverable — PS 8.2 (The Full Robustness Battery + Write-Up)

**Problem set:** `book/weeks/week-08/ps8.2.md` (PS 8.2, Week 8).
**Chapter:** Ch 8.2 — Robustness & Inference Stress-Tests. **Notebook:** `nb8.2` (the robustness-battery harness).

PS 8.2 has no single numeric answer key: it is a project deliverable, and what is graded is whether every promise in column 3 of the Ch 7.5 threats table is operationalized into a real test, read by the Ch 8.2 pass/fail rules, and reported with honesty discipline. So this appendix entry is a **model deliverable** — a complete, A-grade robustness section for one cast project, written as a strong student would submit `robustness.md`, followed by **instructor grading notes** that key each subsection to the empirical-rigor rubric and call out the moves that earn (and lose) points.

The exemplar is **Maya's staggered fair-lending DiD on HMDA** — the chapter's running example — so you can read the section against the chapter's worked numbers and the nb8.2 harness side by side. Every magnitude below is **illustrative** and **consistent with nb8.2** (the seeded synthetic DGP, `default_rng` seed 42), *not* a real figure off HMDA; where a number matches the Ch 8.2 worked table (the $m=8$ BH family in particular), it reproduces that stylized table exactly. The headline under test is a Callaway–Sant'Anna overall ATT of **−1.4 percentage points** (examination programs shrink the county-level minority–white denial gap), state-clustered SE ≈ 0.55, t ≈ 2.5 — the stylized magnitude Ch 8.2 and nb8.2 build the entire battery against, so a student can check each test against a known target. (Note for cross-reference: this is an **intentionally distinct, smaller stylized magnitude** than the −1.89 pp first-look estimate in `nb8.1` / E-w8-ps8.1, which used a different synthetic DGP geared to the specification-curve display. The two notebooks were tuned to teach different things — analytic-choice multiplicity in nb8.1, the robustness-attack battery in nb8.2 — and the chapter and PS 8.2 deliberately follow the nb8.2 numbers so the worked SE panel, BH family, and Oster δ line up exactly.)

---

## THE MODEL DELIVERABLE — `robustness.md`

> **Robustness.** This section runs the battery promised in column 3 of our identification memo (the threats-and-responses table of the empirical-strategy section). Each test below is the operationalization of one row of that table; §6 maps them back explicitly. The headline is an overall ATT of −1.4pp on the minority–white denial gap, estimated against never- and not-yet-treated controls and clustered by state. We report what each test found, whether or not it favors the result.

### 1. Alternative standard errors

The point estimate is fixed at −1.4pp throughout this subsection; only the variance — and so the t-statistic and the confidence interval — moves as we vary what we assume about the error covariance $\boldsymbol\Omega$.

| Clustering | What it assumes about $\boldsymbol\Omega$ | SE | t | 95% CI |
|---|---|---|---|---|
| Classical | errors i.i.d., every county-year independent | 0.18 | 7.8 | [−1.75, −1.05] |
| Heteroskedasticity-robust (HC1) | diagonal varies, no correlation | 0.21 | 6.7 | [−1.81, −0.99] |
| County (unit) | correlated within county | 0.31 | 4.5 | [−2.01, −0.79] |
| **State (primary)** | correlated within state (where treatment varies) | **0.55** | **2.5** | **[−2.48, −0.32]** |
| State + Year (two-way) | within-state and within-year (national shocks) | 0.61 | 2.3 | [−2.60, −0.20] |

*(Illustrative, consistent with nb8.2.)* Read top to bottom, this is the whole drama of Ch 2.4 in one column. The classical SE is a fantasy: it treats every county-year as independent information and reports a t of 7.8 no one should believe. Treatment turns on at the *state* level and within-state denial gaps are correlated, so the Moulton/Petersen (2009) logic says we must cluster at the state level; doing so roughly triples the SE. **Verdict: the result passes this attack** — even under the most conservative defensible clustering, two-way by state and year (Cameron, Gelbach & Miller 2011), the 95% interval [−2.60, −0.20] still excludes zero. Had the two-way row crossed zero, we would report the result as "significant under state clustering but not under two-way clustering," i.e., fragile on this axis; it is not.

**Serial correlation.** Denial gaps are sticky — a county high this year tends to be high next year — exactly the within-unit serial correlation that Bertrand, Duflo & Mullainathan (2004) showed can push a DiD's false-positive rate toward 45% if ignored. We do *not* add a separate HAC (Newey–West) step, because clustering by state already absorbs arbitrary within-state serial correlation through the block-diagonal $\boldsymbol\Omega$ (Ch 2.4); HAC would be the tool only for a single long time series, which this panel is not.

**The few-clusters check.** The table above hides the threat we ranked second-most-dangerous in the memo: cluster-robust SEs need many clusters, and the count that matters is the number of *treated* clusters. We have 50 states but only **8 ever adopted** an examination program in the window, so the effective cluster count is dangerously small, and the conventional state-clustered SE is plausibly downward-biased — over-rejecting. We therefore run the **wild cluster bootstrap** (Cameron, Gelbach & Miller 2008): impose the null, flip each cluster's residual signs with Rademacher ($\pm 1$) weights, re-estimate $B = 1999$ times, and locate the real t in the bootstrapped null distribution.

| Inference | p-value |
|---|---|
| Conventional state-clustered t (t ≈ 2.5) | 0.013 |
| Wild cluster bootstrap (8 treated clusters, $B=1999$) | 0.028 |

*(Illustrative, consistent with nb8.2.)* The bootstrap p-value (0.028) is larger than the conventional one (0.013) — the expected direction with few treated clusters — but still below 0.05. **Verdict: passes, with a stated caveat.** The few-clusters illusion is real here and inflated our conventional significance, but not enough to overturn it; the honest reported inference is the bootstrap, and it clears 5%. Had the bootstrap returned, say, $p = 0.18$, we would have written: "the point estimate is −1.4pp, but with only eight treated clusters inference is too imprecise to reject zero; we report the result as suggestive, not significant." When the two disagree, we believe the bootstrap.

### 2. Placebo tests

**In-time placebo (fake date).** We pick 2015 — three years before the earliest real adoption — pretend the programs switched on then, and drop the true post-period so the fake effect cannot be contaminated by the real one. Re-running the full Callaway–Sant'Anna estimator on this fictional timing yields a placebo ATT of **+0.18pp (t = 0.7)**. *(Illustrative, consistent with nb8.2's World R, t ≈ +0.73.)* **Verdict: passes.** The estimator finds nothing in years when nothing happened — asymmetric but real support for parallel trends, the same evidence as a flat event-study lead compressed to one number. This is the test answering the threat we ranked *most* dangerous (differential pre-trend), so we ran it first; had the placebo ATT come back near −1.4pp and significant, the design could not separate the program from a pre-existing trend, and we would have reported the headline as uninterpretable rather than spin it. (For contrast, nb8.2's "World S" — a planted adopter pre-trend with no true effect — fails exactly this test, t ≈ −3.2, which is the failure mode this placebo exists to catch.)

**In-space placebo (permutation).** We assign fake "adoption" to eight never-adopting states drawn at random, re-estimate, and repeat 500 times to build a distribution of placebo effects; the real −1.4pp is then located in it. The real effect sits in the **left tail, more extreme than 99.6% of placebos (permutation $p = 0.004$)**. *(Illustrative, consistent with nb8.2's in-space permutation, perm $p \approx 0.002$–0.004.)* **Verdict: passes.** This is the right inference for our few-treated-clusters setting (Ch 4.4) and is the *second* answer to the few-clusters row of the memo — it agrees with the wild cluster bootstrap, which is the reassurance we want from two independent angles on the same threat. The histogram with the real effect marked is in nb8.2 (`nb82_inspace_placebo.png`).

**Placebo outcome (fake outcome).** We re-run on the denial gap for **business/commercial loans**, a category exempt from the residential fair-lending examination program — an outcome the program has no mechanical channel to move but that shares the HMDA-style data structure. The estimated effect is **−0.06pp (t = 0.3)**, indistinguishable from zero. *(Illustrative, consistent with nb8.2.)* **Verdict: passes.** This rules out the broad confounder we feared — a general lending or economic shock to adopting states that would have moved *every* gap, not just the examined one. Had the program "moved" the exempt-category gap, that would be a tell that something other than the examinations drives adopting states, and our effect would be riding on it.

### 3. Sensitivity analysis

**Controls (coefficient stability).** Not an RD, so no bandwidth knob; the bandwidth points are redistributed here and to §3's data knob.

| Specification | ATT | State-clustered SE |
|---|---|---|
| No controls | −2.2 | 0.74 |
| Primary controls (applicant income, LTV, loan amount) | −1.4 | 0.55 |
| Aggressive battery (+ county demographics, lender mix, year × region trends) | −1.3 | 0.58 |

*(Illustrative, consistent with nb8.2.)* The coefficient moves from −2.2 to −1.4 when the primary controls enter and then barely budges (−1.3) under an aggressive battery. **Verdict: stable — but we withhold celebration until §5**, because coefficient stability alone can be a trap (a stable coefficient under *toothless* controls proves nothing; Oster makes this precise). We add **no bad controls**: we deliberately exclude the post-examination approval rate and any post-treatment lender-behavior variable, because each is an *outcome* of the program, and conditioning on it would bleed away the very effect we estimate.

**Sample and winsorizing.**

| Cut | ATT | Significant? |
|---|---|---|
| 0% winsorize (raw) | −1.5 | yes |
| 1% winsorize (primary) | −1.4 | yes |
| 5% winsorize | −1.3 | yes |
| Exclude crisis years 2008–2009 | −1.3 | yes |
| Exclude largest state (CA) | −1.5 | yes |
| Exclude earliest adoption cohort | −1.2 | yes (marginal) |

*(Illustrative, consistent with nb8.2.)* **Verdict: stable.** The estimate sits in [−1.5, −1.2] across every defensible data cut and stays significant; it is not hostage to outliers, to one influential state, or to the crisis window. The earliest-cohort exclusion is the most fragile (−1.2, marginal significance), which we flag honestly in §6 rather than hide. We winsorize the noise in the controls but do not winsorize the denial gap itself, which is the subject we are measuring, not noise to cap.

### 4. Multiple-testing correction

**The family.** Maya has a *family* of outcomes, all pre-specified in the PAP (Ch 7.3): the denial gap (primary), the approval-rate gap, the rate-spread gap, the loan-amount gap, and four minority-subgroup gaps. So $m = 8$. With eight truly-null tests at 5%, the chance at least one clears the bar is $1-(1-0.05)^8 \approx 0.34$ — we owe the reader a correction.

| Outcome | $p$ | rank $k$ | BH bar $\frac{k}{8}(0.05)$ | $\le$ bar? |
|---|---|---|---|---|
| Denial gap (primary) | 0.004 | 1 | 0.00625 | yes |
| Approval-rate gap | 0.011 | 2 | 0.01250 | yes |
| Rate-spread gap | 0.030 | 3 | 0.01875 | no |
| Loan-amount gap | 0.041 | 4 | 0.02500 | no |
| Subgroup A gap | 0.20 | 5 | 0.03125 | no |
| Subgroup B gap | 0.33 | 6 | 0.03750 | no |
| Subgroup C gap | 0.51 | 7 | 0.04375 | no |
| Subgroup D gap | 0.78 | 8 | 0.05000 | no |

*(Reproduces the Ch 8.2 §4 worked table exactly.)* The largest rank $k$ with $p_{(k)} \le \frac{k}{8}(0.05)$ is $k = 2$ (since $0.011 \le 0.0125$), so **Benjamini–Hochberg (1995) declares the two smallest — denial gap and approval-rate gap — significant** at FDR 5%, and the rest not. Note the rate-spread gap ($p = 0.030$), which cleared the naive 5% bar, does *not* survive: once we account for having looked at eight outcomes, it is no longer distinguishable from the noise eight draws would produce. **Bonferroni** (FWER, bar $0.05/8 = 0.00625$) is harsher and keeps **only the primary denial gap**. That gap between them is the FWER-vs-FDR trade-off made concrete.

**Contribution sentence:** *Of the eight pre-specified outcomes, two survive Benjamini–Hochberg FDR control at 5% (the denial gap and the approval-rate gap); only the primary denial gap survives the more conservative Bonferroni FWER control.* Our headline — the denial gap — is the one result that survives *both* corrections, which is the strongest position to be in; we report the approval-rate gap as a corroborating secondary result and do not claim the rate-spread gap at all. We chose FDR as the primary reporting target because we are screening a family of related fair-lending outcomes, where tolerating a small false-discovery fraction is the sensible posture, and report Bonferroni for the reader who wants the FWER guarantee.

### 5. Oster (2019) δ

The deepest threat in the memo: an unobserved confounder — residual creditworthiness differences we never measured — that no balance table can reach. Oster (2019) reframes the unanswerable "is there one?" into "how strong would selection on unobservables have to be, relative to the selection on the observables we control for, to explain away the entire −1.4pp?"

Two regressions, three ingredients:

- **Uncontrolled:** $\hat\beta_0 = -2.2$, $\tilde R_0 = 0.08$.
- **Controlled (full covariates):** $\hat\beta_1 = -1.4$, $\tilde R_1 = 0.42$.
- **$R_{\max}$:** Oster's evidence-based default $R_{\max} = \min(1.3\,\tilde R_1,\, 1.0) = 0.546$.

The logic that matters (and that §3's coefficient stability could not deliver on its own): the coefficient moved only modestly (−2.2 → −1.4) *while $R^2$ climbed a great deal* (0.08 → 0.42). The controls were *powerful* and the coefficient shrugged them off — the genuinely reassuring case — not toothless controls under which stability proves nothing.

**Bounding set ($\delta = 1$).** Fixing unobservable selection exactly as strong as observable selection and solving for the bias-adjusted coefficient gives $\beta^* \approx -1.10$, so the identified set is **$[\hat\beta_1, \beta^*] = [-1.40, -1.10]$**. **Verdict: passes** — even with confounding as strong as our rich observables, the effect stays negative and away from zero.

**The δ that kills it.** Setting $\beta^* = 0$ and solving for the required ratio gives **$\hat\delta \approx 4.7$**. *(Verified: with the inputs above and $R_{\max}=0.546$, the calculator returns 4.72; consistent with nb8.2's seeded DGP, which produces a comparably large δ.)* An unobservable would have to be roughly **four to five times** as correlated with examination adoption as Maya's full applicant-composition controls to nullify the effect. Since she already controls for the obvious confounders, an unobservable that potent is hard to argue for. **Verdict: robust** ($\hat\delta = 4.7 \gg 1$).

**$R_{\max}$ sweep (honesty rule 1).** δ is mechanically sensitive to $R_{\max}$, so we report the sweep rather than a single number:

| $R_{\max}$ | $\hat\delta$ |
|---|---|
| 0.42 ($= \tilde R_1$, vacuous) | $\to \infty$ |
| 0.546 (default, $1.3\tilde R_1$) | 4.72 |
| 0.75 | 1.85 |
| 1.00 (harshest) | 1.03 |

*(Illustrative, consistent with nb8.2's Rmax sweep — monotone-decreasing, ≥ 1 even at the harshest $R_{\max}=1.0$.)* The δ is monotone-decreasing in $R_{\max}$ and **stays at or above 1 even at the harshest assumption $R_{\max} = 1.0$** (1.03), so the robustness conclusion does not depend on a flattering $R_{\max}$ choice.

Two more Oster honesty rules, obeyed: **δ is not a p-value** — it measures robustness to a specific untestable threat, not statistical significance; we report it *alongside* the §1 inference, not in place of it, because they answer different questions (our result is both reasonably significant *and* hard to confound, which is the combination we want). And **a failing δ would be information, not embarrassment** — had we found $\hat\delta = 0.4$, we would state plainly in the limitations that an omitted variable only 0.4 times as important as our controls could explain the result. We did not, but the test was run to find out, not to collect a pass.

### 6. Battery-vs-threats-table mapping and honesty audit

Every row of the Ch 7.5 threats table, the stress-test that answers it, and the result:

| Threat (from the Ch 7.5 memo) | Stress-test (this section) | Pass looks like | Result |
|---|---|---|---|
| Differential pre-trend (row 1, scariest) | In-time placebo (fake 2015 date) | Placebo ATT ≈ 0 | **Pass** (+0.18pp, t = 0.7) |
| Few treated clusters (only 8 adopters) | Wild cluster bootstrap; in-space permutation | Bootstrap p agrees / real effect in tail | **Pass with caveat** (boot $p=0.028$; perm $p=0.004$) |
| Errors correlated across units/time | Alternative clustering levels | CI excludes zero under conservative clustering | **Pass** (two-way CI [−2.60, −0.20]) |
| Broad coincident shock to adopters | Placebo outcome (exempt loan category) | No effect on placebo outcome | **Pass** (−0.06pp, t = 0.3) |
| Result tuned to a knob | Sensitivity: controls / sample / winsorizing | Estimate flat across defensible range | **Pass** (ATT in [−1.5, −1.2]) |
| Cherry-picked from a family | Bonferroni / Benjamini–Hochberg ($m=8$) | Survives the pre-specified correction | **Pass** (survives BH and Bonferroni) |
| Unobserved (creditworthiness) confounder | Oster (2019) δ | $\hat\delta \ge 1$; bounding set excludes zero | **Pass** ($\hat\delta = 4.7$; set [−1.40, −1.10]) |

**Honesty audit.** *(i) Scariest placebo.* The most dangerous threat in the memo was the differential pre-trend, so we ran the in-time placebo first; it passed (t = 0.7). Had it failed, the honest sentence was written and ready — "the design cannot separate the program from a pre-existing denial-gap trend" — and the decision would have been to report the result as uninterpretable, not to soften the language. *(ii) Coefficient stability through Oster's eyes.* The coefficient stayed stable (−2.2 → −1.4) because the controls were *powerful* — $R^2$ climbed from 0.08 to 0.42 and δ came in at 4.7 — not because they were toothless; this is the reassuring case, and it is *why* we can lean on the §3 stability rather than treat it as a coincidence. *(iii) Family audit.* The headline denial gap is robust to the true family size $m=8$ (survives both BH and Bonferroni), and the contribution sentence we report — robust on the primary, corroborated on the approval-rate gap, no claim on the rate-spread gap — is the honest one, narrower than the eight-significant-results paper a naive analysis would have written.

**The most fragile result, named honestly:** the earliest-adoption-cohort exclusion in §3 dropped the ATT to −1.2pp at marginal significance, and the wild cluster bootstrap (§1) materially widened the p-value (0.013 → 0.028). Neither overturns the headline, but both are the places this result is *thinnest*, and a referee should know that the design's weakest point is the small number of treated states, not the parallel-trends assumption. We say so here rather than wait to be asked.

---

## INSTRUCTOR GRADING NOTES (keyed to the empirical-rigor rubric)

These notes show why this deliverable earns an A and where a weaker submission loses points. The criteria mirror Assessment 8 and the PS 8.2 part allocation.

### Part 1 — Alternative standard errors (18 pts) → **Excellent**

The SE panel holds $\hat\beta$ fixed at −1.4pp across every row and moves only the SE/t/CI — the single clearest sign the student understood that misbehaving errors corrupt the *variance*, not the point estimate (Ch 2.4 / Ch 8.2 §1). Two A-grade moves: (i) the conservative-clustering **verdict is stated explicitly** ("passes because the two-way CI still excludes zero"), with the counterfactual fragile-case sentence given; (ii) the few-clusters check is not skipped but *demonstrated* — the student reports **8 treated clusters**, runs the wild cluster bootstrap, and honors the "believe the bootstrap if they disagree" rule, even narrating the brutal report they *would* have written had the bootstrap returned $p=0.18$.
*Where points are lost on a typical submission:* reporting only the primary clustered SE with no panel (no test of the inference at all); a panel where the *point estimate* also changes row to row (a conceptual error — that is a sensitivity check, not an SE check); skipping the bootstrap with "we have 50 states" (the relevant count is treated clusters, which the strong student catches). The serial-correlation reasoning — clustering already absorbs it, HAC is for single series — is correct and concise; a weak submission either ignores serial correlation or bolts on a redundant HAC step it cannot justify.

### Part 2 — Placebo tests (24 pts, the heaviest block) → **Excellent**

All three placebos are run, each tagged to the threat it probes and read by the Ch 8.2 §2 pass/fail rule. The in-time placebo is run **first**, because it answers the *scariest* threat (the pre-trend) — exactly the "run your scariest placebo first" discipline. The in-space permutation is correctly framed as the *second* answer to the few-clusters row (agreeing with the bootstrap), showing the student sees that one threat can take two tests. The placebo *outcome* is well-chosen and, crucially, the student **states why the treatment cannot mechanically reach it** (the exempt loan category) — a placebo outcome the treatment could plausibly move is not a placebo, and weak submissions routinely pick one that fails this. The standout honesty move: the student explicitly contrasts the pass with nb8.2's "World S" failure mode, demonstrating they know what a *failed* in-time placebo looks like and would report it.
*Where points are lost:* running only one placebo; reporting an in-space permutation as a single re-estimate rather than a distribution with a permutation p-value and plot; choosing a "placebo" outcome the treatment plausibly affects; and — the cardinal sin Ch 8.2 §2 names — quietly omitting a placebo that would have failed. A submission that buried a failed placebo, if detected against the notebook, is capped hard regardless of polish, because concealment is the exact opposite of the skill being graded.

### Part 3 — Sensitivity analysis (16 pts) → **Excellent**

Controls reported in three columns (none / primary / aggressive) with the coefficient stable; sample/winsorizing swept across 0/1/5% and four defensible subsamples. Two A-grade moves: (i) the student **defers the stability verdict to §5** ("we withhold celebration until Oster"), showing they understand the §3→§5 trap that coefficient stability alone is only half the story; (ii) they **flag the no-bad-controls discipline explicitly**, naming the post-treatment variables (approval rate, lender behavior) they refused to condition on and why. The fat-tail "do not winsorize the subject" principle is stated correctly even though Maya's outcome is not the acute case (it is more acute for Devon).
*Where points are lost:* a single specification with no controls/sample variation; adding a *bad control* (a post-treatment mediator) and mistaking the resulting instability for evidence; winsorizing-search for significance (p-hacking with extra steps); or declaring "stable" without showing the range. The strong submission also *names its most fragile cut* (earliest cohort, marginal) rather than averaging it away.

### Part 4 — Multiple-testing correction (16 pts) → **Excellent**

The family is **declared in full with $m=8$** and its pre-specification status stated — disarming the garden of forking paths (Ch 1.5). Both corrections are applied: the BH table is reproduced in the §4 form (ranked p-values, sliding bar, $\le$-check), the largest-$k$ rule is executed correctly ($k=2$), and the contrast with Bonferroni (keeps only the primary) is drawn. The contribution sentence is exactly the Ch 8.2 form and, tellingly, the student **does not claim the rate-spread gap** that cleared the naive 5% bar but failed BH — the discipline the whole correction exists to enforce. The choice of FDR as primary target is justified by the screening posture, not asserted.
*Where points are lost:* reporting one outcome as if it were the only test (the lone-star sin); declaring a family but applying neither correction, or only the one that keeps the most stars; an arithmetic slip in the BH bar or the largest-$k$ selection (a common one: stopping at the first $p>\frac{k}{m}\alpha$ rather than taking the *largest* $k$ that passes). The strong submission also states the honest contribution sentence *even when it would narrow the paper* — here it happens not to, because the headline survives both, and the student says so without overclaiming.

### Part 5 — Oster (2019) δ (18 pts) → **Excellent**

The two regressions and three ingredients are reported; $R_{\max}$ is named as Oster's default and **defended with a full sweep** (honesty rule 1), and the sweep shows δ ≥ 1 *even at the harshest $R_{\max}=1.0$* (1.03) — the most persuasive possible version of the robustness claim. δ is computed **both ways**: the bounding set $[-1.40, -1.10]$ at $\delta=1$ (excludes zero) and the $\hat\delta \approx 4.7$ that would drive the effect to zero (≫ 1). The student articulates the load-bearing logic — coefficient stability is reassuring *because* $R^2$ climbed a lot (powerful controls), the exact §3→§5 link — and obeys the remaining two honesty rules (δ-is-not-a-p-value; a-failing-δ-is-information), even narrating what they would have written at $\hat\delta=0.4$.
*Where points are lost:* reporting δ without $R_{\max}$ (uninterpretable, per rule 1); computing only one of the two uses; assuming $R_{\max}=\tilde R_1$ (which makes the test vacuous) and claiming robustness from a division-by-near-zero artifact; or reading a large δ as statistical significance (it is not — rule 2). A subtle A/B distinction: a B-grade submission computes δ correctly but reads a *stable coefficient* as automatically robust without the $R^2$ logic — exactly the half-the-story trap Oster was built to fix.

### Part 6 — Mapping + honesty audit (8 pts) → **Excellent**

The mapping table covers **every** row of the Ch 7.5 threats table with the test that answers it and the actual result — turning the section from a grab-bag into a defended design. The honesty audit answers all three reflections, and the decisive A-grade move is the final paragraph: the student **names the result's two thinnest points** (the small treated-cluster count and the earliest-cohort cut) *even though the headline survives*, rather than presenting an all-passes section. Ch 8.2 §6 is explicit that an all-passes section is *less* credible, and this submission internalizes that by surfacing fragility a referee would otherwise have to dig for.
*Where points are lost:* a battery with no map back to the threats table (tests with no stated purpose); a threat row with no matching test and no stated reason; or an audit that reports only passes and claims "no concerns remain" — which is marked *down*, per the chapter's rule that a clean robustness section reads as insufficiently adversarial.

### One-line grading heuristic

The two highest-signal questions for any PS 8.2 submission: **(1)** For *every* promise in column 3 of the Ch 7.5 threats table, is there a real test here, read by the Ch 8.2 pass/fail rules? **(2)** Are failures (and near-failures) reported as findings rather than buried — does the section name where the result is *thinnest*? A student who clears both has the Week-8 mindset: they tried to kill their own result, they ran the attacks a hostile referee would run, and they reported what the attacks found whether or not they liked it. This exemplar clears both cleanly — which is what an A looks like.

---

*End of model deliverable for PS 8.2. The exemplar is Maya's HMDA staggered fair-lending DiD, the chapter's running example, so it can be read against Ch 8.2's worked SE panel, BH family, and Oster δ directly. Every magnitude is illustrative and consistent with nb8.2 (`notebooks/week-08/nb8.2-robustness-battery.ipynb`, `default_rng` seed 42), reproducing the chapter's stylized −1.4pp ATT, the $m=8$ BH table verbatim, and an Oster δ ≈ 4.7 that stays ≥ 1 across the full $R_{\max}$ sweep. Citations by name as in the chapter: Oster, E. (2019), *Unobservable Selection and Coefficient Stability*, JBES 37(2):187–204; Benjamini, Y. & Hochberg, Y. (1995), *Controlling the False Discovery Rate*, JRSS-B 57(1):289–300; the wild cluster bootstrap is Cameron, Gelbach & Miller (2008) and two-way clustering Cameron, Gelbach & Miller (2011); the DiD serial-correlation result is Bertrand, Duflo & Mullainathan (2004); the staggered-DiD estimator is Callaway and Sant'Anna (2021), as built in Ch 4.2. No real or licensed HMDA data appears; the section is the answer to column 3 of the Ch 7.5 memo, filed after the PS 8.1 first-look estimate.*
