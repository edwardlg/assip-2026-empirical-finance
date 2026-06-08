# PS 8.2 — The Full Robustness Battery + Write-Up

**Course:** 8-Week Empirical Finance Camp · Week 8 · Problem Set 8.2
**Covers:** Ch 8.2 (Robustness & Inference Stress-Tests) and the companion notebook **nb8.2** (the robustness-battery harness), building directly on the pre-registered estimate you produced in PS 8.1 / Ch 8.1, the threats-and-responses table you filed in PS 7.5 / Ch 7.5, and the inference toolkit of Ch 2.4 (sandwich SEs, clustering, HAC, the wild cluster bootstrap), the placebo logic of Ch 4.1 and Ch 4.4, and the multiple-testing discipline of Ch 1.5.
**Type:** Project deliverable, not a numeric problem set. You are running the robustness battery on *your own* result — the single headline estimate from PS 8.1 — and writing the **robustness section** that will become the backbone of your Week-8 paper (its presentation craft is Ch 8.3; its place in the replication packet is Ch 8.5). What is graded is not whether your result *survives* — a result that fails honestly is worth full marks — but whether every promise in column 3 of your Ch 7.5 threats table is **operationalized into a real test**, read by the pass/fail rules of Ch 8.2, and reported with the honesty discipline that treats a failed test as a finding rather than a setback to bury.

**Total: 100 points.** Point values are stated per part. A model deliverable — a full A-grade robustness section for one cast project (Maya's HMDA fair-lending DiD), with a battery-vs-threats-table mapping, a worked Oster (2019) δ, and the honesty discipline annotated — is in Appendix E (`E-w8-ps8.2-solutions.md`). Read it *after* you draft your own, to calibrate, not to copy.

**The standing rule on numbers.** This sheet and its solutions use Maya's HMDA staggered DiD as the running example, and every magnitude that appears — the −1.4pp ATT, the SE-flavor table, the BH family of eight p-values, the Oster δ — is **illustrative**: clearly labeled, internally self-consistent, and **consistent with nb8.2**'s seeded synthetic output, *not* a real figure off HMDA. Your real battery will produce different numbers on your own data; report *yours*, and label any worked example you borrow as illustrative. Where this sheet quotes a number that matches the Ch 8.2 worked tables (the eight-outcome BH family, in particular), it is reproducing the chapter's stylized example exactly so you can check your harness against a known answer.

**Pick your project once, and stay with it.** Every part below says "your result." Use the same project and the same headline estimate throughout — the one you pre-registered in Ch 7.3, built the panel for in Ch 7.4, defended in the Ch 7.5 memo, and ran in PS 8.1:

- **Maya** — staggered DiD on HMDA: do state fair-lending examination programs shrink the county-level minority–white mortgage-denial gap? Callaway–Sant'Anna overall ATT against never-/not-yet-treated controls, clustered by state. (The chapter's and the solution's running example.)
- **Devon** — on-chain / FinTech event study or panel: the headline is a treatment or event coefficient on a fat-tailed crypto outcome. Your battery leans hard on the *winsorize/sample* knob and the *fat-tail* sensitivity.
- **Priya** — climate-insurance DiD: a billion-dollar FEMA disaster on county homeowner-premium costs. Your battery leans on the *spillover/SUTVA* placebo (fake-unit) and *two-way clustering*.
- **Sam** — value/momentum panel: a long-short portfolio alpha or a cross-sectional return predictor. Your battery leans on *subsample/crisis-window* sensitivity and the *multiple-outcome family* (many predictors tested at once).
- **Leah** — patents/innovation panel: a text-or-patent-count treatment coefficient. Your battery leans on the *placebo outcome* (a count the treatment cannot mechanically move) and *clustering by firm vs. industry*.

If your real PS-8.1 estimate is not yet runnable, build on the **seeded synthetic fallback from nb8.2** so the whole battery runs end to end; say so in your header and treat every magnitude as illustrative.

---

## What you submit

Two artifacts, committed to your project repository in the same tagged commit as your final `nb8.2` run:

1. **`robustness.md`** — the robustness section of your paper, the graded deliverable. It has exactly five subsections, in the order of Ch 8.2: (1) alternative standard errors, (2) placebo tests, (3) sensitivity, (4) multiple-testing correction, (5) Oster (2019) δ — closed by (6) a **battery-vs-threats-table mapping** and a short **honesty audit**. One to three pages of prose plus the tables named below.
2. **`nb8.2` (your run)** — the notebook executed end to end on *your* estimate, with the tables and figures `robustness.md` references (the SE panel, the placebo distribution plot, the BH table, the Oster δ with its $R_{\max}$ sweep). The prose cites the notebook cells; the notebook is the evidence.

The non-negotiable framing, stated once: **your robustness section is the answer to column 3 of your Ch 7.5 threats table.** Keep that table open beside you. Every test below is the operationalization of one row's promised defense, and every row of your table must show up somewhere in your battery. A robustness section that runs tests with no map back to the threats they answer reads as a grab-bag; one that says "row 1 of my threats table promised an in-time placebo against the pre-trend threat; here it is, and here is what it found" reads as a design being honestly defended.

---

## Part 1 — Alternative standard errors (18 points)

Your headline estimate from PS 8.1 has *one* point estimate $\hat\beta$ and *one* reported standard error. Part 1 asks: is that standard error telling the truth? Recall the central lesson of Ch 2.4 — **misbehaving errors do not corrupt $\hat\beta$; they corrupt its variance**, hence the t-stat, hence the p-value. None of the tests below touches your point estimate. They re-ask "how uncertain is this number?" under less convenient, more honest assumptions about how the errors are correlated.

**(a) The clustering-level panel (8 pts).** Re-run your headline estimate under *every defensible* error-covariance assumption and build the table from Ch 8.2 §1 — same $\hat\beta$ in every row, only the SE (and hence t and CI) moving:

| Clustering | SE | t | 95% CI |
|---|---|---|---|
| Classical | … | … | … |
| Heteroskedasticity-robust (HC1/HC2/HC3) | … | … | … |
| Unit-level (your observation level) | … | … | … |
| **Your primary level** | … | … | … |
| Two-way (e.g., unit × time) | … | … | … |

State, in one sentence per row, what error correlation that flavor assumes (classical: none; clustered: correlated blocks at that level; two-way: Cameron–Gelbach–Miller 2011). Then read the table top to bottom the way Ch 8.2 §1 read Maya's: the classical SE is a fantasy that treats every observation as independent; as you move to coarser, more honest clustering, the SE inflates. **The verdict you must state:** does the CI exclude zero under the *most conservative* defensible clustering? If yes, the result passes this attack. If the most conservative row crosses zero, the honest report is "significant under [primary] clustering but not under [two-way]" — and the result is *fragile* on this axis, and you say so in those words.

**(b) Serial correlation (4 pts).** State, for *your* design, whether within-unit serial correlation is a live threat (it is for any multi-period panel: outcomes are sticky over time) and how your primary inference handles it. The Ch 2.4 rule: **clustering by the unit already absorbs arbitrary within-unit serial correlation** (the block-diagonal $\boldsymbol\Omega$), so a panel clustered by unit is serial-correlation-robust without a separate HAC step; HAC (Newey–West) is the tool when you have *one* long time series and cannot cluster. Name which case you are in, cite the Bertrand–Duflo–Mullainathan (2004) result that ignoring serial correlation drives a DiD's false-positive rate toward ~45%, and state in one sentence why your clustering choice defuses it (or, for a single-series design, report the HAC SE and its bandwidth).

**(c) The few-clusters check — wild cluster bootstrap (6 pts).** The table in (a) silently hides one danger: cluster-robust SEs need *many* clusters (the Ch 2.4 rule of thumb, 30–50), and the relevant count is the number of *treated* clusters, which is often far smaller than your total cluster count. With few treated clusters the cluster-robust SE is **downward-biased and noisy**, your t-stat does not follow the t-distribution you compare it to, and you **over-reject** — you find significance that is not there.

Run the **wild cluster bootstrap** (Cameron, Gelbach & Miller 2008) from nb8.2: impose the null, flip each cluster's residual signs with Rademacher ($\pm 1$) weights, re-estimate $B \ge 999$ times, and read your real t-stat's position in the bootstrapped null distribution to get a p-value. Report (i) your number of total and *treated* clusters, (ii) the conventional clustered p-value, and (iii) the wild-cluster-bootstrap p-value. **Pass:** the bootstrap p is small and roughly agrees with the conventional p — your significance was not a few-clusters artifact. **Fail:** the bootstrap p is much larger (e.g., conventional $p=0.01$, bootstrap $p=0.18$); then the conventional stars are fake, and the honest report is short and brutal: "with few treated clusters, inference is too imprecise to reject zero; we report the result as suggestive, not significant." **If the two disagree, believe the bootstrap** — that is the whole reason it is in your battery. If your design genuinely has many treated clusters (say, > 40), say so and state that the bootstrap is a confirmatory formality rather than the load-bearing inference; do not skip it, *demonstrate* it.

---

## Part 2 — Placebo tests (24 points)

A placebo runs your exact analysis where, by construction, *there can be no treatment effect*, and checks that you correctly find nothing. If your method finds an "effect" where none can exist, the effect it found in the real analysis is suspect, because your method is manufacturing patterns out of whatever structure is in the data. Run **all three** flavors that apply to your design; for each, state the threat it probes, the pass/fail rule, and the honest report on a fail.

**(a) In-time placebo — fake treatment date (8 pts).** Pick a period *well before* any real treatment — Ch 8.2 §2 used three years before the earliest real adoption — pretend treatment switched on then, and leave the true post-period out so the fake effect cannot be contaminated by the real one. Re-run your full estimator on the fictional timing. **What it probes:** whether your estimator detects an "effect" purely from the trend structure — the differential-pre-trend threat (row 1 of most DiD threats tables). **Pass:** placebo effect small and statistically indistinguishable from zero (asymmetric but real support for parallel trends, the same evidence as a flat event-study lead in one number). **Fail:** the placebo effect is itself large/significant — close to fatal, because your method finds effects in years when nothing happened. There is no spin that survives a failed in-time placebo; the honest move is to conclude the design cannot separate the treatment from a pre-existing trend, and either redesign (cleaner control, shorter window) or report the result as uninterpretable. (RD project: substitute a *placebo cutoff* — a threshold where no treatment changes hands — for the fake date.)

**(b) In-space placebo — permutation across units (8 pts).** Assign fake "treatment" to units that never actually got it, re-estimate, and repeat across **many** random reassignments (nb8.2 uses ~500) to build a *distribution* of placebo effects; then locate your *real* effect in it. **What it probes:** whether an effect of your magnitude shows up routinely when treatment is assigned at random — the synthetic-control-style inference of Ch 4.4, and the *right* inference when clusters are too few for the t-approximation (so this and Part 1c are two answers to the same "few clusters" row). Report a **permutation p-value** and a histogram of the placebo distribution with your real effect marked. **Pass:** the real effect sits in the extreme tail (more extreme than ~95% of placebos, permutation $p < 0.05$). **Fail:** the real effect is buried in the placebo cloud — not distinguishable from noise. The placebo distribution *is* the honest summary of uncertainty here; if your number is unremarkable within it, say so plainly.

**(c) Placebo outcome — fake outcome (8 pts).** Pick an outcome the treatment has *no plausible mechanical channel* to move, but that shares your data structure (Maya: a denial gap for a loan category exempt from fair-lending examination; Leah: a patent count the program cannot touch; Priya: a premium series outside the disaster's reach). Re-run. **What it probes:** a broad confounder — a general economic shock to treated units that would have moved *everything*. **Pass:** no effect on the placebo outcome (rules out the broad confounder). **Fail:** the program "moves" an outcome it cannot mechanically affect — a tell that something other than your treatment is driving treated units, and your effect is riding on it. State which placebo outcome you chose and *why the treatment cannot mechanically reach it* — a placebo outcome the treatment *could* plausibly move is not a placebo.

The unifying honesty point (Ch 8.2 §2): a placebo is a prediction your theory makes about *where you should find nothing*, and reporting a failed one is **not optional**. A paper that omits the obvious placebo reads as evasive; one that reports a failed placebo and grapples with it reads as honest. You ran the placebo to learn the truth, not to collect a pass.

---

## Part 3 — Sensitivity analysis (16 points)

Every analysis has knobs — defensible individually, but jointly giving you the freedom to land on a number you like. Sensitivity analysis wiggles each knob across its defensible range and reports how much the estimate moves. The sharper-than-Ch-8.1 question: not "is my result stable across all forks?" but "is my result hostage to *this particular* arbitrary choice?" Run the knobs that apply to *your* design; you must run at least **(b) controls** and **(c) sample/winsorizing** (every project has these), plus **(a) bandwidth** if you are an RD.

**(a) Bandwidth — RD only (4 pts; redistribute to (b)/(c) if not an RD).** Plot the RD coefficient and its CI as a function of the bandwidth $h$, from half the optimal bandwidth to twice it (the Calonico–Cattaneo–Titiunik procedure automates the optimal choice, but you must *show* the estimate is not a one-bandwidth artifact). **Pass:** flat and significant across the range. **Fail:** swings wildly, or is significant only in a narrow window of $h$ around your chosen value — a result tuned into existence.

**(b) Controls — coefficient stability (6 pts; 8 if not an RD).** Report your estimate with **no controls**, with your **primary controls**, and with an **aggressive battery** of extra controls — three columns. **Pass-with-a-caveat:** the coefficient barely moves; *suggestive* of robustness — but read Part 5 before celebrating, because stability alone can be a trap (Oster makes the subtlety precise). **Fail:** the coefficient halves or flips sign when a control is added; then the result depends on a modeling choice and you must justify *which* control set is correct on substantive grounds, never by picking the one that keeps the stars. Flag explicitly that you did **not** add any *bad control* — a post-treatment variable that is itself an outcome of the treatment — because that bleeds the effect away and its instability is an artifact, not evidence.

**(c) Sample and winsorizing — the data knob (6 pts; 8 if not an RD).** Re-run at **0% (raw), 1%, and 5% winsorizing**, and drop **defensible subsamples**: exclude the crisis years (2008–2009), exclude your largest/most-influential unit, exclude the earliest cohort. **Pass:** stable across these. **Fail:** the result lives or dies on a handful of outliers, on one influential unit, or on the crisis window. Then the honest claim is *narrower* than the one you wanted ("the effect holds outside the financial crisis but is not separately identified within it") — and narrowing the claim to what the data support is the job, not a defeat. (Fat-tailed-outcome projects — Devon especially — note where winsorizing would *erase the signal* rather than tame noise, per Ch 7.4: winsorize the noise in your controls, not your subject.)

---

## Part 4 — Multiple-testing correction (16 points)

You almost certainly do not have one outcome — you have a *family* (the primary outcome plus secondary outcomes, subgroups, alternative measures). Recall the hard lesson of Ch 1.5: **the false-positive rate of a single test does not protect a search across many tests.** If you tested eight truly-null outcomes at 5%, the chance at least one clears the bar is $1-(1-0.05)^8 \approx 0.34$ — a one-in-three false "discovery" from pure noise. You owe the reader an adjustment for the size of your family.

**(a) Declare your family (4 pts).** Write down **every outcome you looked at** — not just the ones you plan to report — and state $m$, the family size. State, honestly, whether this family was **pre-specified** in your Ch 7.3 PAP. The cardinal sin (the garden of forking paths, Ch 1.5) is to run twenty outcomes, find one significant, and report it alone as if it were the only test you ran; declaring the family in advance is what disarms it. If your family grew beyond the PAP, say so and treat the extras as exploratory.

**(b) Apply both corrections (8 pts).** Run **Bonferroni** (FWER — test each of $m$ at $\alpha/m$; the probability of *even one* false positive across the family) and **Benjamini–Hochberg (1995)** (FDR — the expected *fraction* of declared discoveries that are false). Report the BH table in the Ch 8.2 §4 form — outcomes ordered by p-value, rank $k$, the sliding bar $\frac{k}{m}\alpha$, and the $\le$-bar check — and state the surviving set under each. Recall the worked family (this is the chapter's stylized $m=8$ example, reproduced exactly so you can check your routine):

| Outcome | $p$ | rank $k$ | BH bar $\frac{k}{8}(0.05)$ | $\le$ bar? |
|---|---|---|---|---|
| Primary | 0.004 | 1 | 0.00625 | yes |
| Secondary A | 0.011 | 2 | 0.01250 | yes |
| Secondary B | 0.030 | 3 | 0.01875 | no |
| … | … | … | … | … |

The largest $k$ with $p_{(k)} \le \frac{k}{8}(0.05)$ is $k=2$, so BH declares the two smallest significant; the $p=0.030$ outcome, which cleared the *naive* 5% bar, does **not** survive. Bonferroni here (bar $0.05/8 = 0.00625$) keeps only the primary. That gap *is* the FWER-vs-FDR trade-off made concrete: Bonferroni buys near-certainty against any false positive at the cost of power; BH tolerates a small false-discovery fraction to keep more real effects. State which target is right for *your* setting — FWER when a single false positive is costly (a drug-approval mindset), FDR when you are screening many candidate signals (the natural posture in finance).

**(c) The honest contribution sentence (4 pts).** State the surviving set in the Ch 8.2 form: "Of the $m$ pre-specified outcomes, [k] survive Benjamini–Hochberg FDR control at 5%." **If your headline result is the one that fails to survive correction, you say so**, and your contribution narrows to "suggestive on the secondary outcomes, robust only on the primary" (or whatever the truth is). A reader trusts a corrected family far more than an uncorrected lone star.

---

## Part 5 — Oster (2019) δ (18 points)

The deepest attack: the omitted variable you never measured. No balance table can reach it — the confounder you fear is by definition the one not in the table. Oster (2019) reframes the unanswerable "is there an unobserved confounder?" into the answerable: **how strong would selection on unobservables have to be, relative to the selection on observables you can see, to explain away your entire result?**

**(a) The two regressions and the three ingredients (5 pts).** Report, from *your* data: the **uncontrolled** regression coefficient $\hat\beta_0$ and its $R^2$ ($\tilde R_0$); the **controlled** (full-covariate) coefficient $\hat\beta_1$ and its $R^2$ ($\tilde R_1$); and your chosen **$R_{\max}$** — the $R^2$ a regression on treatment plus all observables *and* unobservables would attain. State Oster's evidence-based default, $R_{\max} = \min(1.3\,\tilde R_1,\, 1.0)$, and that you use it. State the core logic in your own words: coefficient stability is **only half the story**, and the missing half is $R^2$ — a coefficient that stays put while $R^2$ jumps a lot (powerful controls, shrugged off) is far more reassuring than one that stays put while $R^2$ barely rises (toothless controls, proving nothing).

**(b) Compute δ both ways (8 pts).** Using the nb8.2 calculator:

- **The bounding set.** Fix $\delta = 1$ (the benchmark: unobservables exactly as confounding as observables) and solve for the bias-adjusted coefficient $\beta^*$. Report the identified set $[\hat\beta_1, \beta^*]$. **Pass:** it excludes zero. **Fail:** it contains zero.
- **The δ that kills it.** Set $\beta^* = 0$ and solve for the required $\hat\delta$. **Pass:** $\hat\delta \ge 1$ (Oster's heuristic) — an unobservable would have to be *at least as confounding as everything you observed* to nullify the result, usually implausible because you already control for the obvious confounders. The larger $\hat\delta$, the more robust. **Fail:** $\hat\delta < 1$ — a confounder *weaker* than your observables could erase the effect.

Show the calculator inputs and the result. For calibration, the chapter's illustrative Maya numbers (an uncontrolled ATT of −2.2 moving only modestly to −1.4 while $R^2$ climbs from 0.08 to 0.42, $R_{\max}=1.3\tilde R_1$) give $\hat\delta \approx 4.7$ — robust; nb8.2's seeded synthetic version produces a comparably-large δ on its own DGP. Report *your* δ.

**(c) The three Oster honesty rules (5 pts).** State and obey all three from Ch 8.2 §5:
1. **Report $R_{\max}$ and defend it** — $\hat\delta$ is mechanically sensitive to it. Run the **$R_{\max}$ sweep** from nb8.2 (from $\tilde R_1$, where the test is vacuous, to $1.0$, where it is harshest) and report how $\hat\delta$ moves; a δ without its $R_{\max}$ is uninterpretable.
2. **δ is not a p-value** — it measures robustness to a specific, *untestable* threat, not significance. A result can be wildly significant with $\hat\delta = 0.3$ (fragile to confounding), or have a modest t with $\hat\delta = 5$ (hard to confound). Report both kinds of evidence.
3. **A failing δ is information, not an embarrassment** — if $\hat\delta = 0.4$, state it plainly in your limitations: "an omitted variable only 0.4 times as important as our controls would suffice to explain the result." This is the §5 honesty of the identification memo made quantitative.

---

## Part 6 — The battery-vs-threats-table mapping + honesty audit (8 points)

**(a) The mapping table (5 pts).** Close `robustness.md` with the table that makes the whole section legible — every row of *your* Ch 7.5 threats table, the stress-test that answers it, what a pass looks like, and your actual result. This is the structure of Ch 8.2 §6:

| Threat (from your Ch 7.5 table) | The stress-test (this PS) | Pass looks like | Your result (pass / fail / fragile) |
|---|---|---|---|
| Differential pre-trend | In-time placebo | Placebo effect ≈ 0 | … |
| Few treated clusters | Wild cluster bootstrap; in-space placebo | Bootstrap p agrees / real effect in tail | … |
| Errors correlated across units/time | Alternative clustering; HAC | CI excludes zero under conservative clustering | … |
| Result tuned to a knob | Sensitivity (bandwidth/controls/winsorizing) | Estimate flat across defensible range | … |
| Cherry-picked from a family | Bonferroni / Benjamini–Hochberg | Survives the pre-specified correction | … |
| Unobserved confounder | Oster (2019) δ | $\hat\delta \ge 1$; bounding set excludes zero | … |

Every row of your threats table must appear. A threat with no matching test is an unkept promise from Ch 7.5, and you must either run the test or state in the cell why it is not runnable.

**(b) The honesty audit (3 pts).** In a few sentences each, the three Ch 8.2 "Your Turn" reflections: (i) **Your scariest placebo** — the one answering the threat you ranked most dangerous in Ch 7.5; if it *failed*, write the honest sentence that narrows or kills the claim and state your decision (redesign vs. report-as-limitation). (ii) **Coefficient stability through Oster's eyes** — did the coefficient stay stable because the controls were powerful (large $\hat\delta$, reassuring) or toothless (small $\hat\delta$, proves nothing)? (iii) **The family audit** — is your headline robust to your *true* family size, and is the honest contribution sentence the one you were hoping to write? **A robustness section that contains only passes is *less* credible, not more** — a reader assumes you did not try hard enough to fail. If everything passed, say what the *most* fragile result was and where it nearly broke.

---

## Submission checklist (graded as part of the parts above)

Tick every box; an unticked box is points off on the part it belongs to.

- [ ] `robustness.md` has all six subsections in Ch 8.2 order, plus the battery-vs-threats-table mapping and the honesty audit.
- [ ] The SE panel (Part 1a) shows the **same $\hat\beta$** in every row, only SE/t/CI moving, with the conservative-clustering verdict stated.
- [ ] The **wild cluster bootstrap** (Part 1c) is run; total *and treated* cluster counts reported; conventional vs. bootstrap p compared; the "believe the bootstrap if they disagree" rule honored.
- [ ] **All applicable placebos** run (in-time, in-space permutation with a distribution plot and permutation p, placebo outcome) with pass/fail stated by the Ch 8.2 rules — and any *failed* placebo reported, not buried.
- [ ] Sensitivity run on controls (no/primary/aggressive) and sample/winsorizing (0/1/5%, defensible subsamples); **no bad control** added; fat-tail "do not winsorize the subject" case named where it applies.
- [ ] The **family** is declared with its size $m$ and pre-specification status; **both** Bonferroni and Benjamini–Hochberg applied; surviving set and honest contribution sentence stated.
- [ ] **Oster δ** computed *both ways* (bounding set at $\delta=1$; the $\hat\delta$ that drives $\beta^*$ to 0), with $R_{\max}$ defended and an $R_{\max}$ **sweep** reported; δ-is-not-a-p-value and failing-δ-is-information rules obeyed.
- [ ] Every threat row of the Ch 7.5 table maps to a test in the battery (or a stated reason it is not runnable).
- [ ] The honesty audit answers all three reflections; **no all-passes section without naming its most fragile result.**
- [ ] Every magnitude labeled **real** (your data, snapshot pinned) or **illustrative** (synthetic / consistent-with-nb8.2 / borrowed from the solutions).
- [ ] `robustness.md` and the executed `nb8.2` are in the **same tagged commit**; the prose cites the notebook cells that produced each number.

**Point recap.** P1 (18) + P2 (24) + P3 (16) + P4 (16) + P5 (18) + P6 (8) = **100**. Placebos (P2) and the SE/bootstrap (P1) are the two heaviest blocks on purpose: a failed in-time placebo or a few-clusters illusion exposed by the bootstrap can *invalidate the headline*, no matter how clean the rest of the battery is.

---

## How this is graded

Assessment 8 grades the Week-8 paper and this robustness section *together*, on the empirical-rigor rubric. The allocation maps onto it: P1 → inference honesty (SE flavors, the few-clusters bootstrap); P2 → placebo discipline (the most-weighted block, because a failed placebo is the most damning and the most informative); P3 → sensitivity (hostage-to-a-knob detection); P4 → multiple-testing honesty (declared family, FWER vs. FDR, corrected contribution); P5 → the Oster (2019) selection-on-unobservables test, computed and read correctly; P6 → the structural honesty that maps every test to the threat it answers and treats failures as findings. The single highest-signal question a grader asks: **for every promise in column 3 of your Ch 7.5 table, is there a real test here, read by the Ch 8.2 pass/fail rules, and reported honestly whether or not it passed?** The model deliverable in Appendix E shows the A-grade standard for Maya's HMDA DiD, annotated with the rubric levels each subsection hits.

---

*End of PS 8.2. The model deliverable is in `book/appendices/E-solutions-manual/E-w8-ps8.2-solutions.md` — a full A-grade robustness section for Maya's HMDA fair-lending DiD, with the battery-vs-threats mapping, a worked Oster δ (δ ≥ 1), and the honesty discipline annotated by an instructor. Run your own battery first; read the exemplar to calibrate, not to copy. The harness lives in `notebooks/week-08/nb8.2-robustness-battery.ipynb` (`nb8.2`): a placebo engine (fake dates, permuted units, fake outcomes), an SE panel that re-clusters at every defensible level and runs the wild cluster bootstrap, a Benjamini–Hochberg routine, and an Oster δ calculator with an $R_{\max}$ sweep. The author who runs these tests hoping they pass and the author who runs them hoping to learn the truth get the same code and the same output — but only the second one is doing science, and this assignment exists to make you the second kind of author on purpose, before a referee makes you one by force.*
