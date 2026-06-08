# Model Deliverable — PS 8.1 (Specification Curve for Your Main Result)

**Problem set:** `book/weeks/week-08/ps8.1.md` (PS 8.1, Week 8).
**Chapter:** Ch 8.1 — Execution & the Specification Curve.
**Notebook:** `notebooks/week-08/nb8.1-specification-curve.ipynb`.

PS 8.1 has no numeric answer key: it is a project deliverable, and what is graded is the *honesty of the execution and the read*, not a single finding. So this appendix entry is not a worked solution but a **model deliverable** — a complete, A-grade specification-curve write-up for one cast project, written exactly as a strong student would submit it, followed by **instructor grading notes** that key each section to the empirical-execution rubric and call out the moves that earn (and lose) points. Read the exemplar the way Ch 8.1 §8.1.3 walked through Maya's curve: not to copy, but to see the standard.

The exemplar is **Maya's staggered fair-lending DiD** — the HMDA project carried from Ch 7.3 (her PAP) through Ch 7.5 (her identification memo) and executed in Ch 8.1. We use Maya here, rather than a second cast member, on purpose: this is the deliverable the chapter and the notebook both work end to end, so the numbers can be stated concretely and a student can check their own `nb8.1` run against a known target. **Every magnitude below is illustrative and consistent with `nb8.1`'s synthetic HMDA DiD** — the notebook reuses the Ch 7.5 first-look data-generating process so the pre-registered primary recovers an ATT near $-1.89$ pp; the planted truth is $-1.80$ pp. These are teaching numbers from a synthetic panel, *not* an empirical claim about U.S. mortgage markets.

---

## THE MODEL DELIVERABLE — `spec-curve.md`

### 1. The confirmatory result

**Specification (CONVENTIONS §4 form), identical to the `pap-filed` commit.**

- **Outcome:** the county-year minority–white denial gap — `gap_it`, the minority-applicant denial rate minus the white-applicant denial rate in county $i$, year $t$, in percentage points (denial = `action_taken` $\in \{3,7\}$).
- **Treatment / key regressor:** `treat_it` $= \mathbf{1}\{t \ge G_s\}$, an indicator that county $i$'s state $s$ has an active fair-lending examination program in year $t$, where $G_s$ is the state's adoption year (never-adopters are clean controls, $G_s = \infty$). The overall ATT against never- and not-yet-treated states (Callaway–Sant'Anna, Ch 4.2) is the one number I read off to answer H1.
- **Controls:** none in the primary specification beyond the fixed effects (composition controls are a *fork*, varied in the multiverse — see §2).
- **Fixed effects:** county and year FE — the comparison is within-county, net of common-year shocks.
- **Clustering:** by state, the level at which treatment turns on (Petersen rule, Ch 2.4).
- **Sample:** all counties with continuous coverage over the pinned HMDA vintage window; never-adopters and not-yet-treated counties as controls; ~county-year panel as recorded in the data card.
- **Identifying assumption:** absent the examination program, treated and never-/not-yet-treated counties' denial gaps would have followed parallel per-cohort trends.

**The number.**

$$\widehat{\text{ATT}} = -1.89 \text{ pp}, \qquad \text{SE}_{\text{clustered by state}} = 0.065, \qquad 95\%\ \text{CI} = [-2.02,\ -1.75].$$

*(Illustrative, consistent with `nb8.1`: the run returned $-1.8857$ pp; planted truth $-1.80$ pp.)*

**The reading.** The examination programs are associated with a roughly 1.9-percentage-point *narrowing* of the minority–white denial gap — the sign I hypothesized in H1 — with a confidence interval comfortably away from zero. Per my PAP's falsification clause, a CI this tight and this far from zero is a **confirmation**, not a power-limited inconclusive. This is the number my paper defends. It is necessary but not sufficient for a credible finding: I ran exactly one branch of a tree I could defensibly have climbed differently, so §2–§4 ask whether the $-1.89$ survives the choices I could have made otherwise.

### 2. The multiverse enumeration

I list, for each slot, only forks I would defend out loud in a seminar. (One slot — fixed effects — I held *partly* fixed: county and year FE are in every specification, because dropping either would not be a defensible DiD; what I vary is the *addition* of state-specific linear trends.)

- **Controls** — which county-year applicant-composition covariates enter. A doubly-robust DiD can defensibly include the income distribution, the loan-to-value distribution, and the loan-amount distribution, or any nested subset. **4 options:** none / income only / income+LTV / all three.
- **Fixed effects** — county+year FE always; *additionally*, state-specific linear time trends, a standard parallel-trends hedge. **2 options:** with / without trends.
- **Sample window** — full period / drop 2020 (the COVID-disrupted year behaved anomalously) / drop the first and last adoption cohorts (thinly identified). **3 options.**
- **Clustering / inference** — cluster by state (pre-registered, the treatment level) / cluster by county (the unit of observation) / HC1 heteroskedasticity-robust (a defensible floor when the cluster count is questioned). **3 options.**
- **Outcome definition** — the denial *gap* (minority rate minus white rate) / an alternative gap operationalization (`gap_alt`, the same construct measured on a transformed scale). **2 options.**

**Count.** $4 \times 2 \times 3 \times 3 \times 2 = \mathbf{144}$ specifications. One of these 144 *is* my pre-registered primary: {controls = none, FE = no trends, sample = full, clustering = state, outcome = gap}. It is a labeled, privileged point inside the multiverse, not outside it.

**Why 144 matters.** From Ch 1.5: with $k$ specifications, even if the true effect were exactly zero, the probability that at least one lands at $p<0.05$ by luck is $1-(1-0.05)^{k}$ — for $k=144$ that is essentially 1. I ran only *one* regression for the confirmatory result, but the 144 measure how many I *could defensibly have run*, which is the real size of my multiple-testing problem. The spec curve does not erase that problem; it shows the whole distribution of what luck and choice together produce, so my one starred coefficient can never masquerade as the only specification I ever considered.

### 3. The specification curve

![Specification curve for Maya's fair-lending DiD: top panel, 144 ATT estimates sorted by magnitude with 95% CIs (all filled/significant, all below zero); bottom panel, the aligned choice grid (controls, state trends, sample window, clustering, outcome).](spec-curve.png)

*Figure read against the committed `spec-curve.png` from `nb8.1`. Top panel: the 144 point estimates, sorted most-negative (left) to least-negative (right), each with its 95% CI; every marker is filled (significant at 5%); the curve sits entirely below the zero line. The pre-registered primary is marked with a red diamond. Bottom panel: one row per analytic choice, one column per specification, aligned to the top sort order, with a tick where a specification uses a choice.*

### 4. The read

**The four-point checklist applied to my curve.**

1. **Where does the sign live?** Entirely negative. All 144 estimates are below zero, ranging from about $-2.4$ pp on the left to about $-1.3$ pp on the right; the median is about $-1.85$ pp. The *direction* of the effect is robust to every defensible analytic choice I could have made. *(Illustrative, consistent with `nb8.1`: 100% of the 144 specifications are negative.)*
2. **Where does the pre-registered specification sit?** Near the center. The confirmatory $-1.89$ pp lands around the 46th percentile of the sorted distribution — neither the most nor the least favorable corner. My headline is *representative* of the multiverse, not a cherry-picked extreme, which is exactly what I want a referee to see and what my PAP's commit-first discipline was designed to deliver.
3. **What fraction is significant, and where do the exceptions cluster?** All of them. 144 of 144 specifications are significant at the 5% level (every CI excludes zero) — there are no hollow markers to read downward. *(Illustrative, consistent with `nb8.1`: 100% significant.)* The honest implication is that significance is *not* a fragile feature here; even the least-favorable corner of the multiverse (the most aggressive sample trim combined with the most conservative inference) keeps the interval below zero.
4. **Which rows of the bottom panel drive the spread?** The spread is narrow — about 1.1 pp from the most to the least negative estimate — so no single fork dominates it. Reading the bottom panel, the choice that most moves the magnitude is the **sample window**: the "drop first and last cohorts" specifications cluster toward the less-negative (right) end, because trimming the early and late cohorts discards identifying variation and pulls the estimate modestly toward zero. But this is a magnitude effect within a single sign, not a sign flip or a significance flip, so it is a benign sensitivity, not a fragility. I name it because PS 8.2's robustness section will revisit cohort composition, and because saying "no single fork flips my result" *is* the stronger claim — I report it as such.

**The one honest paragraph (for the Week-8 paper).**

> Across all 144 defensible specifications, the estimated effect of fair-lending examinations on the minority–white denial gap is negative, with a median of about $-1.85$ pp and a range of roughly $[-2.4, -1.3]$ pp. The pre-registered primary specification ($-1.89$ pp) sits near the center of this distribution, at about the 46th percentile. The effect is statistically significant at the 5% level in all 144 specifications: the sign never changes, the magnitude is stable around the pre-registered estimate, and even the least-favorable corner of the multiverse — the most aggressive sample trim under the most conservative inference — leaves the confidence interval entirely below zero. The widest magnitude variation is driven by the sample-window choice (trimming the first and last adoption cohorts pulls the estimate modestly toward zero by discarding identifying variation), but no single analytic choice flips the sign or the significance of the result. **The result is robust to analytic-choice multiplicity.** What this curve does *not* establish is that the underlying design is valid — every one of the 144 specifications assumes parallel trends, and if that assumption fails, the curve reports a stable artifact; that assumption is stress-tested separately in the robustness analysis (PS 8.2), not here.

### 5. The honest deviations log

I made **one** deviation from the PAP on the confirmation data; it was mechanical, not outcome-driven.

- **2026-05-27 — collinear state trend mechanically dropped `[mechanical, not outcome-driven]`.** PAP §2 fixed the primary specification with county and year FE. In the multiverse, the "add state-specific linear trends" fork (`i(state, year_c)`) produces one redundant trend term that is collinear with the county and year FE for a single state, which `pyfixest` mechanically drops with a collinearity warning. This affects only the *state-trend* arm of the multiverse, never the pre-registered primary (which has no trends). I confirmed the dropped term is the expected mechanical redundancy — not a substantive variable — and silenced the warning inside the spec loop with an explanatory comment. The primary ATT is untouched at $-1.89$ pp. **Not outcome-driven; nothing about the result steered the change.**

No other departures. The confirmatory run executed exactly as filed, behind the `PAP_FILED=True` gate, and returned $-1.89$ pp on the first and only run.

**Deviations-to-multiverse audit.** Every alternative I was tempted to consider while staring at the confirmatory number is *already a numbered fork in the multiverse*, so I never had to silently switch the primary:

- "Should I have clustered by county instead of state?" → that is the county-clustering arm; those specifications sit among the 144 and remain significant. The headline does not depend on the clustering choice.
- "Should I have added composition controls to tighten the estimate?" → that is the controls slot (income / income+LTV / all three); those specifications sit near the primary. The headline does not depend on the control set.
- "Should I have dropped 2020?" → that is the sample-window fork; the drop-2020 specifications are negative and significant. The headline does not depend on the 2020 handling.

Because each temptation maps to an existing specification, I can point at the curve rather than re-choose the headline — which is the entire ethic of Ch 8.1 §8.1.5: the spec curve is the honest home for every fork I was tempted to walk, and this log is the record of the one I actually had to.

---

## INSTRUCTOR GRADING NOTES (keyed to the empirical-execution rubric)

These notes show *why* this deliverable earns an A and where a weaker submission would lose points. The criteria mirror the PS 8.1 part allocation and Assessment 8.

### Part 1 — Confirmatory result (15 pts) → **Excellent**

All seven CONVENTIONS §4 slots are named to the variable level and stated as *identical to the PAP*; the number is reported with the **labeled** SE flavor (clustered by state) and the 95% CI; and the reading invokes the PAP's falsification clause explicitly ("a CI this tight and this far from zero is a confirmation"). The decisive A-grade move is the last sentence: the student states that a clean execution is necessary but **not sufficient**, refusing to let the starred coefficient stand in for a robust result. That sentence is the §8.1.1 lesson internalized.
*Where points are lost on a typical submission:* reporting the coefficient with no SE flavor named (which flavor? a referee cannot tell); or — the serious failure — a specification that has *silently drifted* from the PAP, which is a commit-first contract violation and is flagged regardless of polish; or reading a starred coefficient as "this proves the effect," skipping the multiverse entirely.

### Part 2 — Multiverse enumeration (25 pts) → **Excellent**

The five slots are enumerated with a one-clause defense per option, and the student demonstrates judgment in *both* directions of the "defensible" test: nothing absurd is padded in to inflate the count, and the standard clustering debate (state vs. county vs. HC1) is included rather than collapsed to one option. The count is stated as an explicit cross-product ($4\times2\times3\times3\times2=144$), the pre-registered primary is identified *as one of the 144*, and the multiple-testing arithmetic ($1-(1-0.05)^{144}\approx 1$) is connected to *why the count matters*. A subtle A-grade touch: the student names a dimension held *fixed* (county+year FE always present) and says why varying it would be indefensible — exactly the §8.1.4 meta-honesty about what you chose not to vary.
*Where points are lost:* omitting an obvious fork for the design (a DiD multiverse with no clustering-level variation, say) caps this part; padding with a fork the student would never defend ("I added a 6-month window to get to 200 specs") is penalized *harder* than omission, because it is the §8.1.4 "p-hacking with extra steps"; forgetting that the primary lives inside the multiverse loses the (b) sub-points; stating the count without the $1-(1-0.05)^k$ logic loses (c).

### Part 3 — The specification curve (20 pts) → **Excellent**

The figure is the canonical two-panel object: estimates sorted by magnitude on top with significance-coded CI markers, the aligned choice grid underneath, a zero line, labeled units (pp), a legend, and — the non-negotiable element — the **pre-registered primary marked** (the red diamond). The grid rows correspond one-to-one to the §2 forks, so a reader can read downward from any region of the curve to the choices that produced it.
*Where points are lost:* a top panel that is *not sorted* (so the "curve" has no monotone shape and the read collapses); a bottom panel *not aligned* to the top sort order (so reading downward is meaningless); no zero line or unlabeled axis; and the common, costly omission — *failing to mark the pre-registered point*, which is what lets a fishing-license reading sneak in (§8.1.4).

### Part 4 — The read (25 pts, the heaviest part) → **Excellent**

The four-point checklist is applied concretely to *this* curve, not recited abstractly: sign (all negative), pre-registered position (46th percentile, "representative"), significance fraction (144/144), and the spread-driving fork (sample window, named and correctly characterized as a magnitude effect within one sign, not a fragility). The one honest paragraph *earns* the word **robust** by the §8.1.3 standard — sign never flips, magnitude stable, loss of significance confined to (here, entirely absent from) the low-power corner — and, crucially, the paragraph **closes with the boundary**: it states plainly that robustness across the multiverse is *not* design validity, and points to PS 8.2 for the parallel-trends stress test. That closing sentence is the difference between a student who understands what a spec curve does and one who thinks it proves the result.
*Where points are lost:* the cardinal sin is asserting "robust" because the author *wants* it — declaring robustness while the curve actually sweeps across zero, or while the significant specifications all share one fork. A fragile curve mislabeled robust fails this part regardless of prose quality. The mirror failure is hedging a genuinely robust curve into mush ("results are somewhat mixed") when the sign never flips. The exemplar also models the correct handling of a curve with *no* dominant fork: saying so explicitly and noting that "no single fork flips my result" is the *stronger* claim, per the §8.1.3 / Your-Turn prompt 1.

### Part 5 — The honest deviations log (15 pts) → **Excellent**

The student logs the one real deviation, dates it, and correctly classifies it as **mechanical** (a collinear state-trend term dropped by the estimator — a coding/data reality, not an outcome-driven choice), confirming the primary ATT was untouched. Then — the part weak students skip — the **deviations-to-multiverse audit** walks through each *temptation* (cluster by county? add controls? drop 2020?) and locates it as an existing numbered fork, so the student points at the curve instead of re-choosing the headline. That is the §8.1.5 system working as designed: the deviations log and the spec curve are one instrument, and between them no fork is left in the dark.
*Where points are lost:* an empty or absent log when deviations plainly occurred (the worst failure — it reads as concealment); a deviation logged but *not* classified mechanical vs. outcome-driven; an outcome-driven deviation reported *as the headline* instead of as labeled-exploratory; or — the audit failure — a temptation the student cannot locate anywhere in the multiverse, which means the Part-2 enumeration was incomplete and should have been patched. A student who genuinely made zero deviations earns full marks by saying so explicitly, as the exemplar's closing line models.

### One-line grading heuristic

The two highest-signal questions for any PS 8.1 submission: **(1)** Does the verdict word (**robust** / **fragile**) match what the curve *actually shows* — sign stability, the significance pattern, and where the exceptions cluster (Part 4)? **(2)** Is the pre-registered point *marked* on the curve and reported *around* the multiverse rather than *chosen by* it, with every tempted fork located as an existing specification (Parts 3, 5)? A student who clears both has the Week-8 mindset — they keep "not an artifact of my analytic choices" cleanly apart from "proven causal," and they show the whole orchard before a referee can accuse them of picking one tree. This exemplar clears both cleanly, which is what an A looks like.

---

*End of model deliverable for PS 8.1. The exemplar is Maya's HMDA fair-lending DiD — the same project carried through Ch 7.3 (PAP), Ch 7.5 (identification memo), and executed in Ch 8.1, so a student can check their own `nb8.1` run against a known target. All magnitudes are illustrative and consistent with `nb8.1`'s synthetic data-generating process (primary ATT $\approx -1.89$ pp; planted truth $-1.80$ pp; 144 specifications, 100% negative, 100% significant, primary near the 46th percentile); they are teaching numbers from a synthetic panel, not empirical claims about U.S. mortgage markets. The intellectual frame is Simonsohn, Simmons & Nelson (2020), Specification Curve Analysis, Nature Human Behaviour 4, 1208–1214. The cautionary fragile contrast — Sam's momentum multiverse, whose sign flips with the weighting/universe choice — is built in `nb8.1` and discussed in Ch 8.1 §8.1.3. Design validity (parallel trends), as distinct from the analytic-choice robustness shown here, is the job of PS 8.2.*
