# Model Deliverable — PS 7.3 (A Complete Pre-Analysis Plan Draft)

**Problem set:** `book/weeks/week-07/ps7.3.md` (PS 7.3, Week 7).
**Chapter:** Ch 7.3 — The Pre-Analysis Plan (short form, Olken 2015), with the empirical-spec discipline of CONVENTIONS §4 and the multiple-testing arithmetic of Week 1 (§1.5.10).
**Paper:** Olken, B. A. (2015). *Promises and Perils of Pre-Analysis Plans.* Journal of Economic Perspectives, 29(3), 61–80.

PS 7.3 has no single right answer — every camper's PAP is different because every camper's project is different. What this manual provides instead is a **model deliverable**: one complete, A-grade short-form pre-analysis plan, written for **Maya's** HMDA fair-lending project (the worked example of Ch 7.3 §7.3.4 and the planted synthetic design students estimate in nb7.5). It shows the standard a PAP must reach — *precision in every slot, honesty about every residual* — without dictating any camper's question. Below the PAP itself are **instructor grading notes keyed to the research-design rubric**, component by component, so a grader can see exactly where the points are and what the common failure modes look like.

**A standing rule on numbers.** A pre-analysis plan is, by definition, **pre-results**: it is filed *before* any confirmatory regression is run. Therefore this exemplar contains **no estimated coefficients, standard errors, or p-values** as findings — to invent them would defeat the entire purpose of the document and violate CONVENTIONS §6. The only numbers that legitimately appear are (i) *design parameters Maya commits to in advance* (the threshold $\theta$, the hold-out split fraction, the $\alpha$ level, the economically-meaningful effect size she cares about), (ii) *exploration-set quantities* she is allowed to look at because that set is her laboratory (an expected $N$, a residual SD feeding the power calc), and (iii) the *illustrative* p-values in the by-hand Benjamini–Hochberg demonstration, which are clearly labeled illustrative and reuse the worked family from Ch 7.3 §7.3.3 — not results from Maya's data. The nb7.5 planted ATT of $-1.80$ pp is named only as the *truth the synthetic generator was built around*, never as an estimate Maya has seen. Maya's HMDA snapshot is pinned in `data-cards/hmda.md` and any matched licensed data stays read-only on GMU infrastructure per CONVENTIONS §5.

---

## The model deliverable: Maya's filed `PAP.md`

> **PRE-ANALYSIS PLAN**
> **Conditional Racial Disparity in Mortgage Denial, and the FinTech Margin**
>
> *Author: Maya · Project repo: `maya-hmda-fairlending` · Filed as tagged commit `pap-filed`, before any confirmatory regression · Data: HMDA 2019–2021 extract, snapshot pinned in `data-cards/hmda.md`; FFIEC HMDA Loan/Application Register, public · Power calc: `nb7.3`, run on the exploration set only (summary in §7 below)*
>
> ---
>
> ### §1. Hypotheses (directional)
>
> **H1 (primary).** Conditional on observable risk factors, the lender, and the neighborhood, minority applicants face a *higher* mortgage-denial rate than otherwise-similar non-minority applicants: $\beta_1 > 0$. **One-sided.** The direction is the long-standing prior in the fair-lending literature — a conditional denial disparity is documented in Bartlett, Morse, Stanton & Wallace (2022) and in Bhutta, Hizmo & Ringo, and the structural mechanism is consistent with Gao & Sun (2019). I held this prior *before* pulling the data; this PAP is the dated evidence of that, which is what entitles me to the one-sided $1.65$ critical value rather than $1.96$.
>
> **H2 (secondary).** The conditional gap is *smaller* for algorithmic (FinTech) lenders than for face-to-face lenders: the interaction coefficient on `minority × fintech` is $< 0$. **One-sided.** Prior from Bartlett et al. (2022): algorithmic underwriting narrows but does not eliminate the face-to-face gap.
>
> **H3 (secondary, exploratory family).** The conditional gap *differs* across applicant subgroups (Black / Hispanic / Asian) and across five income bands. **No directional prior; two-sided.** This is a heterogeneity scan, not a confirmatory test — I expect to *generate* hypotheses here, not confirm one.
>
> *Primary-as-multiplicity-control:* By naming H1 the single primary test in advance, the multiplicity problem for my headline shrinks from "however many forks I might walk" to **one** — the cheapest and most honest multiplicity defense there is (Olken 2015).
>
> ---
>
> ### §2. Primary specification (CONVENTIONS §4 seven-slot form)
>
> $$\texttt{denied}_{i} = \beta_0 + \beta_1\,\texttt{minority}_{i} + \mathbf{x}_i'\boldsymbol{\gamma} + \alpha_{\ell(i)} + \delta_{t(i)} + \varepsilon_i$$
>
> where $\beta_1$ is the **single coefficient H1 is about**, $\mathbf{x}_i$ the named control vector, $\alpha_{\ell(i)}$ a lender fixed effect, and $\delta_{t(i)}$ a census-tract fixed effect.
>
> 1. **Outcome.** `denied` = 1 if HMDA `action_taken` ∈ {3, 7} (application denied; preapproval request denied), else 0. A linear probability model on the application sample defined in slot 6.
> 2. **Treatment / key regressor.** `minority` = 1 if applicant race/ethnicity is Black or Hispanic, else 0. The coefficient $\beta_1$ is the one number I read off the table to answer H1. For H2, `minority` is interacted with `fintech` (lender flagged as an algorithmic/online originator).
> 3. **Controls $\mathbf{x}_i$** (named, with why each belongs). `log_loan_amount` (loan size legitimately prices risk), `log_income` (capacity to repay), `ltv` loan-to-value (collateral cushion), `loan_term` (amortization risk). **Deliberately excluded — on the causal pathway:** loan-*product type* and the high-cost / rate-spread flag. Steering a minority applicant into a worse product is *itself* a channel of discrimination; conditioning on it would absorb the very effect H1 is hunting (the Mentor 4 over-controlling trap). I therefore do *not* put product type in $\mathbf{x}_i$; I examine it separately as an outcome in robustness.
> 4. **Fixed effects.** Lender FE $\alpha_\ell$ → the comparison is *within a single lender* (nets out a lender's overall strictness and clientele), not across lenders with different applicant pools. Census-tract FE $\delta_t$ → the comparison is *between applicants in the same neighborhood* (nets out local housing-market and demographic conditions).
> 5. **Clustering.** Standard errors clustered **by lender**, chosen now and justified: a lender's idiosyncratic underwriting style induces correlation in the errors of all its loans, so the lender is the level at which observations are not independent. Choosing this level *after* seeing which gives significance would be p-hacking on the standard error; I commit to lender clustering before any confirmatory run.
> 6. **Sample.** First-lien, owner-occupied, one-to-four-family, conventional conforming **purchase** mortgage applications, **2019–2021**. Exclusions: drop applications withdrawn by applicant, closed for incompleteness, and preapproval-request-only rows that never became applications. Expected $N \approx$ **[estimated on exploration set; see §7]** confirmation-set rows after exclusions.
> 7. **Identifying assumption (one sentence).** *Conditional on the named controls and the lender and tract fixed effects, `minority` is uncorrelated with the unobserved creditworthiness — chiefly the credit score that HMDA omits — that lenders legitimately price; this assumption is known to be imperfect, so $\hat{\beta}_1$ is reported as an **upper bound** on differential treatment, not a clean causal effect.* The named threat is omitted-variable bias from the missing score; I address it by bounding rather than claiming clean identification, and I defend the bound in the Ch 7.5 identification memo filed alongside this PAP.
>
> *Self-audit — my three most dangerous forks (and the sentence nailing each down):*
> - **Clustering level.** Tempting to switch lender → county if it tightens the SE. *Nailed:* "Clustered by lender; county clustering appears only as a pre-listed robustness check, reported either way" (§5).
> - **Sample purpose.** Tempting to drop refinances/keep them depending on the coefficient. *Nailed:* "Purchase loans only, 2019–2021, exclusions as listed; refinances are out of sample, decided now" (slot 6).
> - **Income winsorization.** Tempting to winsorize 1%/99% only if the raw fit looks bad. *Nailed:* "Income entered as `log_income` after winsorizing at 1%/99%, fixed in `nb7.4` dataset build before the confirmation run."
>
> ---
>
> ### §3. Multiple-testing plan
>
> **Primary vs. secondary.** H1's coefficient $\beta_1$ on `minority` is *the* primary test, held to the strict $\alpha = 0.05$ (one-sided) and reported as the result. Everything else — the H2 interaction, the H3 subgroup and income-band gaps, the product-type and rate-spread margins, year-by-year splits — is **secondary**: reported, but explicitly *not* the confirmatory claim. This single declaration retires most of the multiplicity problem for the headline.
>
> **Pre-committed families and their corrections.**
> - **Family A (primary):** H1 alone, $\alpha = 0.05$, one-sided. No correction — single primary test.
> - **Family B:** H2 FinTech interaction, $\alpha = 0.05$, one-sided. Single test, no within-family correction.
> - **Family C (exploratory):** the {Black, Hispanic, Asian} × {5 income-band} subgroup gaps from H3. **Benjamini–Hochberg FDR control at 0.05 *within this family*.** Results labeled exploratory regardless of outcome.
>
> **By-hand BH demonstration** (illustrative p-values, *not* results from my data — reused from Ch 7.3 §7.3.3 to show the procedure I will apply). Suppose Family C's five income-band p-values come in as $\{0.008,\ 0.012,\ 0.039,\ 0.041,\ 0.330\}$. Sort ascending; compare each $p_{(k)}$ to the BH threshold $\frac{k}{m}\alpha$ with $m = 5$, $\alpha = 0.05$:
>
> | rank $k$ | $p_{(k)}$ | threshold $\frac{k}{5}(0.05)$ | $p_{(k)} \le$ threshold? |
> |:---:|:---:|:---:|:---:|
> | 5 | 0.330 | 0.050 | no |
> | 4 | 0.041 | 0.040 | no |
> | 3 | 0.039 | 0.030 | no |
> | 2 | 0.012 | 0.020 | **yes** |
> | 1 | 0.008 | 0.010 | yes |
>
> The largest rank satisfying the inequality is $k = 2$, so I reject ranks $\le 2$: **two discoveries** (the 0.008 and 0.012 bands). Bonferroni would hold *every* band to $0.05/5 = 0.01$ and admit only the 0.008 band — discarding the 0.012 effect that BH keeps. BH is less brutal precisely because the $k$-th smallest p-value is allowed up to $\frac{k}{m}\alpha$ rather than $\frac{1}{m}\alpha$, so a family with several genuine effects lets the later ones in at a friendlier bar.
>
> **Pre-commitment clause.** Families A–C are fixed *now*, before I have any p-value. If I were to decide *after* seeing the numbers which tests count as a "family," I could shrink or grow the family until my favorite effect survived correction — so the family list is frozen in this tagged PAP and is unspoofable.
>
> ---
>
> ### §4. Falsification
>
> **H1 is falsified** if, in the primary specification on the confirmation set, the 95% CI for $\beta_1$ is **tight and brackets zero while excluding economically meaningful values** — concretely, if the CI lies within $\pm 2$ percentage points of zero (my economically-meaningful threshold: a conditional denial gap smaller than **2 pp** is below what would change a real borrower's outcome or a regulator's attention). That is informative *absence*: the data place a tight bound near zero, and I will conclude this dataset does not support a conditional denial gap and say so. A **wide** CI that merely includes zero is *not* a refutation — it is a **power failure** (the noisy-but-large case of §1.5.8), reported as *inconclusive*, never as evidence of no gap. (My `nb7.3` power calc, §7, is designed to keep me out of that case.)
>
> **H2 is falsified** if the `minority × fintech` interaction is statistically indistinguishable from zero (FinTech and face-to-face gaps equal) *or* **positive** (FinTech *worse*, the wrong sign).
>
> **H3** generates rather than tests; it has no falsification condition, which is exactly why it lives in an explicitly exploratory family with FDR control.
>
> *Would I actually report an H1 null?* Yes. I am writing this sentence in a dated, tagged file precisely so that a tight-zero refutation obligates me: a clean, pre-registered null about fair lending is a genuine contribution, not a failure. I have inoculated myself against the eight-hours-from-now temptation to keep fishing for a star. I can find no fork I am still leaving open in the primary spec.
>
> ---
>
> ### §5. Planned robustness (reported whichever way they come out)
>
> 1. **Re-cluster by county** instead of lender — stress-tests the clustering fork.
> 2. **Drop 2020** — stress-tests sensitivity to COVID-era denial anomalies in the sample-window fork.
> 3. **Continuous rate-spread outcome** alongside binary `denied` — stress-tests the outcome-definition fork (and probes the pricing margin).
> 4. **Restrict to the 50 largest lenders** — checks the result is not driven by thin-data small lenders.
> 5. **Re-estimate on the full sample** (exploration + confirmation) as a precision check, clearly labeled as combining the two sets.
>
> *Report-either-way clause:* Each check is a fork I am choosing to walk *deliberately and in advance*. If H1 holds in the main spec but evaporates under county clustering or after dropping 2020, this PAP obligates me to report that — robustness is a stress test I promised to report honestly, not a search for confirmation.
>
> ---
>
> ### §6. Registration mechanism
>
> **Hold-out.** The HMDA extract already exists, so I cannot rely on a future hold-out. I split the extract **30% exploration / 70% confirmation** on a stable, pinned key: `hash(loan_id) mod 10 < 3` → exploration (reproducible per CONVENTIONS §5). I design and tune the specification *only* on the 30% exploration set; the primary regression runs **once** on the untouched 70% confirmation set *after* this PAP is tagged.
>
> **Tagged commit.** I register `PAP.md` as a **`pap-filed` Git tag** in `maya-hmda-fairlending`. The tag is my time stamp and a cryptographic promise: anyone can verify the PAP existed in exactly this form *before* the commits containing my confirmatory results — the camp's analogue of OSF / AsPredicted / the AEA RCT Registry. `nb7.5` ("first-look regressions") is **frozen until this tag exists**; its `PAP_FILED` gate refuses to run the confirmatory cell until the plan is filed.
>
> **Deviation log.** I keep `DEVIATIONS.md`, a dated record of every departure: *what* changed, *why*, and **whether it was prompted by seeing the outcome**. A deviation forced by a mechanical reality (a control that turns out collinear, a corrupted lender id, a data-availability surprise) is innocent and noted; a deviation made *because I saw the coefficient and disliked it* is the p-hacking this PAP exists to prevent, and reclassifies that result as exploratory. The log makes the PAP a baseline, not a prison — and lets a referee see exactly where my analysis was confirmatory and where it became exploratory (Olken 2015).
>
> ---
>
> ### §7. Power summary (from `nb7.3`, exploration set only)
>
> Using the exploration set's base denial rate and `minority` share to fix the residual standard deviation of $\hat\beta_1$, and the nb1.5 power machinery (ncp = effect / SE; power = mass beyond the one-sided critical value), I computed the sample size needed to detect my **2 pp** economically-meaningful gap at $\alpha = 0.05$, 80% power. The confirmation set's expected $N$ **clears that bar** (the minimum detectable effect at my $N$ is below 2 pp). I am therefore not running an underpowered confirmation. Had it *not* cleared the bar, my pre-registered options were to widen the question, pool more years, or report a bound — never to "run it anyway and hope," which a pre-registered design has already foreclosed.
>
> *— End of Maya's `PAP.md`. Tag: `pap-filed`. Companion: the Ch 7.5 identification memo, filed in the same commit.*

---

## Instructor grading notes (keyed to the research-design rubric)

The PAP is graded on **precision** (each commitment named to a variable-name-and-decision) and **honesty** (residuals, bounds, and power shortfalls admitted, not hidden) — the two cross-cutting principles of PS 7.3's grading section, both straight from Olken (2015). Below, the points per component, what the A-grade exemplar does, and the common failure modes that cost points.

**Component 1 — Directional hypotheses (15 pts).** *A-grade markers:* H1 stated with an explicit sign ($\beta_1 > 0$) and a one-sentence prior citing the literature *by name* (Bartlett et al. 2022; Bhutta–Hizmo–Ringo; Gao & Sun 2019) — this is what earns the one-sided test. H2/H3 numbered, with H3 honestly flagged "no directional prior; two-sided." The primary-as-multiplicity-control sentence is present. *Deduct:* "race is related to denial" (non-directional, −4); claiming one-sided with no stated prior (the prior is the entitlement to $1.65$, −3); no primary/secondary distinction (−4). *Common failure:* students state a direction but cannot say where it came from — a directional claim with no pre-data justification is a two-sided test in disguise.

**Component 2 — Primary specification, seven slots (30 pts; equation 4 + slots 18 + self-audit 8).** This is the heart and the largest weight. *A-grade markers:* the equation names $\beta_1$ as the single coefficient; **every slot is to a variable name and a decision**, not a concept; the **deliberately-excluded pathway variable** (product type / rate-spread flag) is named *with the over-controlling reason* — this is the slot most students miss and the clearest A/B discriminator; clustering is justified by a *named mechanism* (within-lender error correlation), not asserted; the identifying-assumption sentence names the threat (missing credit score) and *flags the estimate as a bound* rather than overclaiming causality. *Deduct heavily for vagueness:* "appropriate controls and standard errors" earns near-zero on the relevant slot — it is a PAP-shaped object that licenses every fork (§7.3.5); outcome stated as "denial" rather than the `action_taken ∈ {3,7}` rule (−2); no excluded pathway variable named (−3); identifying assumption that says "this controls for endogeneity" with no named threat (−3, CONVENTIONS §4 violation). *Self-audit (8 pts):* full marks require *specific* forks with the *exact sentence* that closes each; generic "I'll be careful with my controls" earns half.

**Component 3 — Multiple-testing plan (20 pts; primary/secondary 6 + families+BH 10 + pre-commitment 4).** *A-grade markers:* H1 explicitly promoted to the single $\alpha=0.05$ primary; families written as a *frozen list* (A/B/C); BH assigned to the genuine family (C); the **by-hand BH demonstration is correct** — finds $k=2$, admits the two smallest, and correctly contrasts with Bonferroni admitting only one; the pre-commitment clause explains *why* late family definition is gameable. *Deduct:* applying BH/Bonferroni to *every* test including the primary (the primary needs no correction — it is one test, −2); BH arithmetic errors, e.g. rejecting the largest p below threshold without taking the *largest* qualifying rank (−3); no pre-commitment clause (−4) — this is the clause the plan exists to enforce. *Common failure:* declaring "I'll correct for multiple testing" without naming the families or the procedure — the multiplicity control that is not pre-specified is not a control.

**Component 4 — Falsification (15 pts; H1 sentence 8 + secondary 4 + honesty check 3).** *A-grade markers:* the H1 falsification sentence **distinguishes a tight-CI refutation from a wide-CI power failure** (the §1.5.8 move) and states the economically-meaningful threshold (2 pp) *in the outcome's own units*; H2 falsification includes the *wrong-signed* case; the "would I actually report it?" answer is a candid "yes" with the reason (a pre-registered null is a contribution). *Deduct:* "if it's insignificant I'm wrong" (conflates a noisy null with a refutation — the exact §1.5.8 error, −4); no economically-meaningful threshold in units (−3); honesty check answered "yes" with no reasoning or, worse, "I'd keep looking" with no fork named to close (−3). *Common failure:* students treat falsification as a formality and write a sentence that no result could actually trigger — a hypothesis nothing could refute is a mood, not a claim (Olken / Popper).

**Component 5 — Planned robustness (10 pts; list 7 + report-either-way 3).** *A-grade markers:* 3–5 *concrete* checks, each tagged to the *fork it stress-tests* (county clustering ↔ clustering fork; drop 2020 ↔ sample-window fork; rate-spread ↔ outcome fork); the report-either-way clause written as a *self-obligation* with a concrete "if it evaporates I say so." *Deduct:* vague "various robustness checks" (−4); robustness framed as confirmation-seeking ("checks that confirm H1") rather than stress tests reported either way (−3) — that is fishing with a planned-sounding label.

**Component 6 — Registration mechanism (10 pts; hold-out 4 + tag 3 + deviation log 3).** *A-grade markers:* hold-out split on a **pinned, reproducible key** (`hash(loan_id) mod 10`), with the "primary runs once on the untouched 70%" commitment; the `pap-filed` tag explained as a *credible time stamp* (verifiable that the PAP predates the results), tied to nb7.5's frozen gate; the deviation log's **outcome-driven-vs-mechanical** distinction stated as the crux. *Deduct:* "I won't peek" with no mechanical hold-out (willpower is not a registration mechanism, −3); tag mentioned but not explained as a time stamp (−1); deviation log without the outcome-driven distinction (−2) — that distinction is the entire point.

**Cross-cutting (folded into the above, not separately scored).** *Power calc:* an A-grade PAP *uses nb7.3* and reports whether the design clears the 80%-power bar for its smallest meaningful effect — a PAP that pre-registers an underpowered design without noticing has wasted its confirmation run before firing it. *No fabricated results:* a PAP that reports coefficients/SEs/p-values as findings is *automatically capped* — it is logically impossible to have confirmatory results in a document filed before the confirmatory run; such a paper has either peeked (a fatal honesty violation, log it or fail) or fabricated (CONVENTIONS §6). *Validity vs. honesty:* the exemplar scores high partly *because* it admits its design is imperfect (the bound, the missing score). Remind students: pre-registration buys honesty (did you test or search?), not validity (is the test right?) — validity is the Ch 7.5 identification memo's job, and the two are filed together as the Lab 7 deliverable.

---

*End of model deliverable and grading notes for PS 7.3. This exemplar PAP is consistent with the worked plan in Ch 7.3 §7.3.4 and with the planted synthetic design students estimate in `notebooks/week-07/nb7.5-first-look-regressions.ipynb` — where the same primary specification, frozen behind a `PAP_FILED` gate, recovers a pre-planted denial-gap effect on data the student designed the spec without ever seeing. The PAP promises Maya did not fish; the identification memo of Ch 7.5 argues the pond is the right pond. Filed together as a tagged commit, they are the spine of a project that could survive a hostile referee — which is the entire point of Week 7.*
