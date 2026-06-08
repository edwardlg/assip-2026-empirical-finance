# PS 7.5 — Your Identification Memo + Threats Table

**Course:** 8-Week Empirical Finance Camp · Week 7 · Problem Set 7.5
**Covers:** Ch 7.5 (The Identification Memo), building on Chs 7.1–7.4 (idea → data → PAP → analysis dataset) and the design toolkit of Weeks 3–4.
**Type:** Project deliverable, not a numeric problem set. You are writing the one page your Week-8 paper will defend, for *your own* project — the question you committed to in your pre-analysis plan (Ch 7.3) on the dataset you built in Ch 7.4. There is no answer key with "the right number," because there is no number yet: the memo is about *design*, not findings. What is graded is whether your design is stated honestly enough that a skeptic can attack it cleanly and find nothing you did not already see.

**Total: 100 points.** Point values are stated per part. A model deliverable — a full A-grade memo for one cast project, with instructor grading notes keyed to the research-design rubric — is in Appendix E (`E-w7-ps7.5-solutions.md`). Read it *after* you draft your own, the way Ch 7.5 §6 walked through Maya's: not to copy, but to calibrate.

A note on what this assignment is for. Ch 7.5 said it once and it is worth repeating: the identification memo is not a defensive document you write to survive review. It is a thinking tool you write to find out whether your project is real. The single most valuable outcome of this problem set is *not* a polished page — it is the moment, while filling the table, when you discover a threat whose third column is empty and whose fourth column is "this could be the entire effect." If that happens, the memo has done its most important job: it found the project-killer in Week 7 instead of Week 8. The right response is to redesign or to state the limitation plainly, never to soften the language until the threat disappears.

---

## What you submit

A single Markdown file, `memo.md`, committed to your project repository as part of your Lab 7 tagged commit (the same tag that freezes your PAP and `nb7.5`). It has exactly three sections, in this order:

1. **The specification, in CONVENTIONS §4 form** (Part 1 below).
2. **The identifying-assumption paragraph** (Part 2).
3. **The threats-and-responses table** (Part 3).

Plus a short **honesty audit** (Part 4) you write *for yourself* and paste at the bottom. The whole thing is one to two pages. The identifying-assumption sentence is allowed to be the longest sentence in the document; everything else is terse.

---

## Part 1 — The specification, in spec-discipline form (15 points)

Before you can name an identifying assumption, you must name the regression it attaches to. Write your **primary specification** — the single estimate that tests your primary hypothesis H1 from the PAP — listing all seven slots of CONVENTIONS §4 explicitly, each defined to the level of a variable name (not "denial" but "the binary indicator `denied` = 1 if `action_taken` ∈ {3,7}").

- **Outcome** — the exact dependent variable. (3 pts)
- **Treatment / key regressor** — the one coefficient you read off the table to answer H1. (2 pts)
- **Controls** — the covariates you hold fixed, *named*, with one clause on why each belongs; flag any variable you deliberately do *not* control for because it sits on the causal pathway (the over-controlling trap from Mentor 4 / Ch 7.3). (3 pts)
- **Fixed effects** — which absorbing dummies, and what comparison they force (within-lender? within-county-year?). (2 pts)
- **Clustering** — the level, chosen in advance and justified by where the errors plausibly correlate. (2 pts)
- **Sample** — the exact universe of rows: years, geographies, loan/firm types, exclusions, with the expected row count. (2 pts)
- **Identifying assumption, in one sentence** — the placeholder for Part 2; you will expand it there. (1 pt)

This section must be *identical* to the specification you registered in your PAP. If it has drifted, you have broken the commit-first contract of Ch 7.3 §5, and you must either revert to the registered spec or flag the deviation explicitly and explain why (a legitimate move only if forced by something you learned building the dataset in Ch 7.4 — e.g., a variable that did not exist, a sample that was empty — and never because a different spec gave a prettier coefficient *you have not yet seen*).

---

## Part 2 — The identifying-assumption paragraph (25 points)

Write one paragraph whose spine is a single sentence in the fixed template of Ch 7.5 §1:

> Our estimate of **[the effect]** is **causal / credible** as long as **[the assumption]**, which we defend by **[the design feature or evidence]**.

Three blanks, three jobs, and the grading follows them.

**(a) Name the effect, not the regression (4 pts).** The first blank names *what you are estimating* — "the effect of state fair-lending examinations on the county-level minority–white mortgage-denial gap," not "the coefficient on the treatment dummy."

**(b) Name the specific threat, not "endogeneity" (10 pts).** The second blank states the exact condition under which your estimate equals that effect — the named counterfactual that has to hold and the exact way it could fail. This is CONVENTIONS §4 applied to your own paper: "as long as there is no endogeneity" earns **zero** for this part, because it names no threat. "As long as treated and control states would have followed parallel denial-gap trends absent the regulation" earns full marks, because a referee knows precisely what to attack. Pull the assumption from the standard menu of your design (Ch 7.5 §2: selection-on-observables for OLS; relevance + exclusion for IV; parallel trends + no-anticipation for DiD; continuity for RD; donor-pool match for synthetic control).

**(c) Defend it — make the third blank do real work (7 pts).** Name the design feature or evidence that makes the assumption believable: the fixed effects that absorb the obvious confounder, the placebo that would have caught the obvious failure, the institutional fact that rules out the obvious alternative story. "Defended by parallel trends" is *not* a defense (it just restates the assumption); "defended by a flat pre-trend in the event-study leads, a clean-control comparison against never- and not-yet-treated units only, and the institutional fact that adoption timing was set by legislative calendars unrelated to local lending conditions" *is*.

**(d) Match the verb to the evidence (4 pts).** Choose `causal` or `credible` deliberately. `causal` is earned only by a design with a testable fingerprint that an honest reader accepts as near-proof (a clean RD at an ungameable cutoff, a randomized instrument). Most observational designs earn `credible`: the assumption is untestable, you have argued it as hard as you can, and the reader grants a conditional belief, not a proof. Overclaiming here is the tell of an amateur, and it is graded as such. If you wrote `causal`, your paragraph must name the testable fingerprint that earns it; if you cannot, downgrade to `credible` and adjust every claim to match.

The rest of the paragraph (two to four more sentences) lists, in compressed form, the defenses you will deliver and the inference you will report (the standard-error flavor, any placebo). This paragraph becomes your Week-8 *empirical strategy* section nearly verbatim, so write it as prose a referee will read, not as notes.

---

## Part 3 — The threats-and-responses table (45 points)

Build the four-column table of Ch 7.5 §3 as a literal Markdown table. Its rigid shape is what forces honesty: every threat gets a response, every response ends in a residual concern.

| Column | What goes in it |
|---|---|
| **Threat** | The named failure of the identifying assumption — from the menu of your design — in one phrase. *Not* "endogeneity." |
| **Why it's plausible** | One sentence on the concrete story under which this threat is *real in your setting*. A threat with no plausible story is a strawman; cut it. |
| **What we do about it** | The specific test, design choice, or robustness check — with the expected result that would *reassure* a reader. |
| **Residual concern** | What still worries you after column 3. The honest leftover. A blank here costs you. |

**(a) Coverage: the standard menu plus your own data (12 pts).** Your table must include **every** threat on your design's standard menu from Ch 7.5 §2 — the ones a referee reaches for first — and **at least one** threat specific to *your* data (a survivorship filter, a look-ahead leak from Ch 7.4, a measurement-error problem from Week 1, a composite-outcome issue). A table that omits the obvious menu threat for your design — e.g., a DiD table with no parallel-trends row, an IV table with no exclusion row — cannot score above half on this part, however polished the rest is. Expect **four to six rows**.

**(b) Plausibility, not strawmen (6 pts).** Each "Why it's plausible" cell tells a concrete, setting-specific story. "States might differ" is not a story; "states that chose to adopt examinations may already have been on an improving denial-gap trajectory, because reform-minded legislatures both legislate and improve" is.

**(c) The right *kind* of response — testable vs. arguable (15 pts).** This is the conceptual heart of the assignment and the most heavily weighted single criterion. For *every* row, decide first whether the threat is **testable** (leaves a fingerprint in the data) or **arguable** (the data are logically incapable of revealing it), and put the right kind of thing in column 3 (Ch 7.5 §4):

- **Testable threats** → column 3 is a *statistic or diagnostic* (event-study leads for pre-trends; first-stage $F$ for IV relevance; a balance table for OLS/RD; the McCrary density for RD manipulation) and column 4 is "what the test can and cannot rule out."
- **Arguable threats** → column 3 is an *institutional fact or economic argument* (the exclusion restriction; compound treatment at a cutoff; the parallel-trends counterfactual *beyond* the observed pre-period; silent anticipation) and column 4 is "this rests on a claim the data cannot confirm."

Two errors are penalized hard here because each advertises that the author does not understand their own design: (i) running a clever test against an untestable threat — most notoriously, claiming a balance table "shows the exclusion restriction holds," which it cannot; and (ii) arguing your way past a threat you could simply have checked. Mark each row `[testable]` or `[arguable]` so the grader can see you made the call deliberately.

**(d) No empty residual-concern cells (8 pts).** Column 4 is mandatory and must be substantive for every row. A table whose residual column is all "none" is *less* credible, not more — every real design has residual concerns, and a reader who sees none assumes you did not look hard enough. "We cannot rule out a contemporaneous policy shock that hit treated states the same year" is worth more than a triumphant "no concerns remain." If you genuinely believe a residual is negligible, say *why* in the cell; do not leave it blank.

**(e) Order by danger (4 pts).** Put your rows in *descending order of danger*. Row 1 is the threat that, if true, would most cleanly kill the paper — the one a seminar asks about in the first ninety seconds. Burying your most serious threat in row five reads as evasion; leading with it reads as confidence.

---

## Part 4 — Honesty audit (15 points)

Paste a short audit at the bottom of `memo.md` answering the three reflection prompts from Ch 7.5's "Your Turn," in a few sentences each. This is where you grade yourself before the instructor does.

**(a) Your most dangerous threat (6 pts).** Which row, if true, would most cleanly kill your paper? Is it testable or only arguable? If arguable, write the two strongest sentences of institutional or economic argument you have — and state honestly whether they are enough. If they are not, say what you would change.

**(b) Audit your verb (4 pts).** Did you write `causal` or `credible` in Part 2? Defend the choice against the actual strength of your evidence. If `causal`, name the testable fingerprint that earns it.

**(c) The empty-cell test (5 pts).** Is any residual-concern cell blank or "none"? If so, you have either a genuinely bulletproof threat (rare — defend it) or one you have not looked at hard enough (likely — go look). Conversely, is any residual concern "this could be the entire effect"? If so, the memo just did its job: decide *now* whether to redesign or to proceed with the limitation stated plainly, and write which.

---

## Submission checklist

Before you commit, confirm:

- [ ] `memo.md` has all three sections (spec · paragraph · table) plus the Part-4 audit, in order.
- [ ] The Part-1 specification names all seven CONVENTIONS §4 slots and is **identical to the PAP** (or the deviation is flagged and justified).
- [ ] The identifying-assumption sentence fills all three blanks of the template and names a **specific threat**, never the word "endogeneity."
- [ ] The verb (`causal` / `credible`) matches the strength of the evidence, and the prose uses "consistent with" / "we cannot reject" rather than "proves" / "establishes" wherever the assumption is untestable.
- [ ] The table covers **every** standard-menu threat for your design **plus** at least one data-specific threat (4–6 rows).
- [ ] Every row is marked `[testable]` or `[arguable]`, and column 3 contains the *matching* kind of response (statistic vs. argument).
- [ ] **No** residual-concern cell is blank or "none."
- [ ] Rows are ordered by descending danger; row 1 is your hardest question.
- [ ] `memo.md` is committed in the **same tagged commit** as the PAP and `nb7.5` — the freeze of Ch 7.5's "Your Turn." You do not run the first-look regression until this memo is filed.

---

## How this is graded

Assessment 7 grades the PAP (Ch 7.3) and this identification memo *together*, on the research-design rubric. The point allocation above maps onto that rubric: Part 1 → spec-discipline; Part 2 → identification reasoning (the named, defended, correctly-verbed assumption); Part 3(c) → the testable-vs-arguable distinction that is the signature skill of the design half of the course; Parts 3(d), 4 → intellectual honesty (stated residuals, calibrated verbs, the hardest question led not buried). The model deliverable in Appendix E shows the A-grade standard for one cast project, annotated with the rubric levels each section hits.

---

## The bridge to Week 8

This memo is the **spine of your Week-8 paper**, exactly as Ch 7.5 §7 promised. The identifying-assumption paragraph becomes your *empirical strategy* section. The threats table becomes the skeleton of your *robustness* section: Ch 8.2 is almost literally the instruction "go run column 3 for every testable row of your table" — the placebos, the alternative standard errors, the bandwidth and sample perturbations that turn each promised defense into a real result. Ch 8.3 turns the memo's prose into an introduction that promises exactly what the design can deliver and no more. And Ch 8.4 hands your memo to another student, who will read it the way you learned to read Fama–French in Week 5 — tables first, identifying assumption second, prose last and skeptically — and who will attack the row you hoped to bury. Write the memo so there is no such row.

*End of PS 7.5. The model deliverable is in `book/appendices/E-solutions-manual/E-w7-ps7.5-solutions.md`. Draft your own memo first; read the exemplar to calibrate, not to copy. The skeptic who reads a stranger's table and the author who builds an honest one are the same person — this assignment is you doing to yourself, on purpose, what you will spend Week 8 doing to a classmate's paper.*
