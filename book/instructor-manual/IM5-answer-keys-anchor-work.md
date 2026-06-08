# IM-5 — Answer Keys & Anchor Work

This is the operational heart of grading the camp. IM-2 (the consolidated rubrics) tells you *what*
each deliverable is worth and what each level means; this section tells you *how* to grade against
those rubrics quickly, consistently, and — when more than one person is grading — in agreement.
Three tools do the work: **Appendix E**, the solutions manual that fully works every problem-set
problem; the **per-week assessment answer keys** that ship inside each `assessment*.md`; and **anchor
papers** — sample graded work pinned at the A/B/C boundaries that calibrate everyone's eye to the
same standard. The back half of this section is a worked walk-through of "what an A versus a B
capstone looks like" against the 200-point rubric, followed by a concrete norming protocol for when
multiple graders must converge.

The standard that governs all of it is the one the book has pressed since Chapter 1.5 and that the
capstone rubric restates: **a modest result honestly stress-tested outscores an ambitious one the
student cannot defend.** Grading the camp is, more than anything, the discipline of rewarding honesty
and craft over ambition and polish. Hold that line and the rest is mechanics.

---

## Part A — Using Appendix E for fast, consistent problem-set grading

Appendix E (`book/appendices/E-solutions-manual/`) is the canonical home of every worked solution:
40 files, one per problem set, eight weeks by five sets, each problem fully derived with code where
relevant and interpretation throughout. The solutions are written *to the student* — they explain not
just the answer but which assumption each step leans on (see `E-w1-ps1.3-solutions.md`, where the
unbiasedness proof pauses to note that "independence was *not* needed for unbiasedness"). That
explain-the-step quality is exactly what makes the manual a grading instrument and not merely an
answer sheet: when a student loses points, the solution tells you *which idea* they missed, which is
what your margin comment should name.

**How to grade a problem set in one pass.** Problem sets are formative — they are the daily reps, not
the high-stakes assessment — so grade them for *evidence of the right reasoning*, fast, and do not
agonize over partial credit to the half-point. The efficient pass:

1. **Read the Appendix E solution for that set first, once, before you open any student work.** Each
   solution carries per-problem and per-part point weights in its headers (e.g., "Problem 1 —
   Unbiasedness of the sample mean (12 pts)", "(a) [4 pts]"). Those weights are your rubric for the
   set; do not invent your own.
2. **Grade by the load-bearing step, not the final number.** The Weeks 1–6 sets are numeric drills,
   and a correct final number with a wrong derivation is worth less than a correct derivation with an
   arithmetic slip — because the camp is teaching the derivation. The Appendix E solution flags the
   step that *is* the point (the linearity-of-expectation move, the FWL partialling, the
   first-stage-F check); award most of the credit there.
3. **Use the solution's interpretation paragraph as the standard for the "interpret" parts.** Many
   problems end by asking what a result *means*. Appendix E models the expected answer in prose;
   grade the student's interpretation against it for *correctness and honesty*, not word count.
4. **Comment by naming the missed idea, then cite the solution.** "You computed Var(x̄) correctly but
   treated bias and variance as the same failure — see E-w1-ps1.3 Problem 1(b)" teaches more in one
   line than a number does, and it routes the student to the worked fix.

**Weeks 7–8 are different and Appendix E says so.** The solutions for the last two weeks are *model
deliverables*, not numeric keys — a sample pre-analysis plan, an identification memo, a threats
table, a robustness write-up — because those problem sets are scaffolding for the capstone, not
drills with a single right answer. Grade them against the *shape* of the model deliverable (does the
PAP name a single primary spec? does the identification memo name a specific threat, never
"endogeneity"?) rather than for an exact match. This is the same standard the Week 7 and Week 8
assessments use, and it is intentional: by Week 7 the camp has stopped asking for the right answer and
started asking for a defensible one.

**Speed and consistency come from order.** Grade *across students by problem*, not *across problems by
student* — do all of Problem 1 for the whole class, then all of Problem 2 — so the standard for a
given problem stays fixed in your head and the solution stays open to one page. This single habit is
the largest consistency gain available on problem sets and costs nothing.

---

## Part B — The per-week assessment answer keys

Each end-of-week assessment (`book/weeks/week-0N/assessment*.md`) ships its own answer key and
analytic rubric inline; you do not assemble these yourself. The structure is uniform: a short-answer
and/or derive-and-interpret component plus a small applied task (a mini-simulation in Week 1, a
replication in Week 2, a written design in Week 7), each scored on a four-level analytic rubric with
explicit point allocations. The keys are written in the same explain-the-step register as Appendix E,
so they double as feedback you can quote.

**Grade assessments more carefully than problem sets** — they are summative, they feed the gradebook
IM-2 lays out, and they are where a misgrade actually costs a student. Two practices keep them
consistent. First, **grade each rubric row independently across the whole cohort** before moving to
the next row — the same by-row discipline as the problem sets, scaled up — so "Proficient on
identification" means the same thing for the first and last paper you read. Second, **decide the
bright lines before you start**, not mid-stack: the assessment keys name the line between Excellent and
Proficient for each row (a single slip versus a pattern of them), and you should fix in your mind what
the one allowable slip is before reading, so you are not silently raising the bar as you tire.

A note on the assessments that prefigure the capstone. The Week 6 assessment weights *validation and
honesty* — it asks students to build and OOS-validate one LLM text classifier and report it
truthfully — and the Week 7 assessment's research-design rubric is, in the assessment's own words,
"the rubric your capstone meets." Grade those two with the capstone standard already in mind, because
a student who learns in Week 6 that the validation table is where the points are, and in Week 7 that a
named threat beats a longer control list, arrives at the capstone already calibrated. Use the margin
to say so: "this is exactly what Capstone row 'Identification & threats' will demand."

---

## Part C — Anchor papers: what they are and how to build them

An **anchor paper** is a real (or realistic) piece of student work, graded once, carefully, with its
score and the *reasoning* for that score attached, kept as the fixed reference point for a level. You
want, for the capstone and for each major assessment, a small set of anchors — minimally one at the
**A/A− line**, one at the **B line**, and one at the **C line** — so that every grader, and every
grading session, calibrates against the same physical examples rather than a private memory of "what
an A feels like." Anchors are how a rubric stops being words and becomes a shared eye.

The camp gives you a head start the rubric explicitly relies on: **the five capstones in the
gallery (`book/capstones/`) are worked anchors at the A/A− line.** The Week 8 assessment says
outright, "Calibrate against the gallery: each of the five capstones is a worked anchor at the
A/A− line." Fair Lending on HMDA, Common Ownership from 13F, Innovation from USPTO, SEC 8-K Text
Classification, and the FRED macro event study are five *different* designs all clearing the same
bar, which is precisely what you want — it shows graders that the A standard is about *craft*, not
about a particular method. Read one for its seams, as the assessment instructs: find its
identification slide, find the residual concern its threats table admits, and run its `make all`.
For ASSIP 2026 specifically, also ask the cross-artifact question — *does the gallery's repo
README, its compressed-to-poster design panel, and its 8-minute talk outline say the same
contribution sentence with the same calibrated verb?* That is the A anchor in hand for the ASSIP
deliverable bundle.

**You must build the B and C anchors yourself, from the first cohort.** The gallery gives you the
ceiling; it does not give you the boundary. The practical path:

1. **During the first cohort, flag candidate anchors as you grade** — a paper that sits cleanly at the
   B line, one that is honestly a C, one borderline case you want to remember how you resolved.
2. **Anonymize and get permission.** Strip names; keep the work. Camp materials are CC-BY-NC, but a
   student's own paper is theirs — ask before you archive it as a teaching anchor.
3. **Attach the score *and the reasoning*, row by row.** An anchor without its rationale is just an
   old paper. Write, for each rubric row, why it scored where it did, in the rubric's own language.
   The reasoning is the part that transfers to next year's grader.
4. **Pick anchors that are *typical* of their level, not extreme.** The most useful B anchor is a
   solidly representative B, not a paper that barely missed an A — boundary-illustrating extremes have
   their place, but your primary anchors should be the center of mass of each grade.

Anchors compound: by the second or third cohort you have a small, well-reasoned library at every
level for every major deliverable, and norming (Part E) becomes fast because everyone is pointing at
the same examples.

---

## Part D — A worked "A versus B capstone" against the 200-point rubric (ASSIP deliverable bundle)

The ASSIP capstone is graded on the 200-point analytic rubric in IM-2 §4b: seven rows summing to 200
across the four ASSIP deliverables — **Symposium poster, JSSR abstract, 8-minute talk + defense, and
reproducible repo** — weighted by design toward identification (34), execution and robustness (40),
and the one-click reproducibility packet (34). Those three sum to 108, more than half the grade,
because what makes a capstone defensible is the craft, not the coefficient. Here is what the
difference between an A and a B looks like *concretely*, walked row by row, so graders can see where
the points actually move. The principle in one line — *both run a real design on real data, find a
result, and write it up cleanly; the difference is honest stress-testing under pressure* — is what
the walk-through expands.

Take two capstones on the same kind of question — say, both estimate whether a state policy change
moved a lending outcome, both using a difference-in-differences on a public panel. The bones are
sound for both: a real design, real data, a clean four-panel poster, an abstract submitted to JSSR
on time, an 8-minute talk delivered at the Symposium. They diverge exactly where honesty meets
pressure.

**Research question & contribution (28 pts).** The A states a one-sentence contribution with a verb
calibrated to the design — "we provide the first credible estimate of…" with *credible*, not
*causal*, because the design supports an association under a defended assumption — and the same
contribution sentence appears, word-for-word, in the JSSR abstract, on the poster's top panel, and as
the talk's opening beat. The B has a contribution sentence too, but the verb over-reaches by one
notch ("we show that X *causes* Y"), or — the ASSIP-specific tell — the poster's headline does not
match the abstract's verb. **A scores Excellent (~28); B scores high-Proficient (~22–24).** Small
points; this row is not where the grade is decided.

**Identification & threats (34 pts).** This is where it starts to separate. The A's
identifying-assumption sentence names the *effect* and the *specific threat* — never the word
"endogeneity" — and its threats table leads with the most dangerous row, matches a *statistic* to
every testable threat and an *argument* to every arguable one, and leaves no residual cell empty.
The compressed-for-poster version of that table (the design panel of the poster) survives the
compression honestly. The B's table is present and pulls the right design menu, but it has a thin
spot: one residual cell reads "none," or a testable threat got an argument where it needed a number,
or the poster's compression dropped the most-dangerous row to make room for a prettier chart.
**A: Excellent (34). B: Proficient (~26).** Eight points, and they are honest points — the B
genuinely left a threat un-quantified.

**Execution & robustness (40 pts) — the row where the grade is won or lost.** The A ran the
pre-registered spec *once* and reported it whichever way it fell (check the Git history: the
`pap-filed` tag predates the confirmatory commit); marked its pre-registered point on the
specification curve, where it sits near the center; ran the *scary* placebo for the top-ranked
threat and reported the one check that *failed*, narrowing the claim accordingly; and reported an
Oster δ with its R_max defended and swept to 1. The robustness panel of the poster shows the failed
check, not buried in an appendix. The B ran the battery but shows only the passes, asserts R_max
without the sweep, leaves the spec-curve point unmarked, and — the tell — keeps three conventional
stars on a treatment with few treated clusters where a wild cluster bootstrap, if run, would have
disagreed. **A: Excellent (40). B: Proficient (~28).** Twelve points, the single largest swing in
the rubric, and every one of them is the difference between *showing your result might be fragile*
and *hiding that it might be*.

**Communication craft — poster + abstract + writing (26 pts).** This row replaces the
paper-only "writing & table craft" of the residential rubric and explicitly grades the **poster**
and the **JSSR abstract** as artifacts. The A's poster is legible at four feet — four panels
(headline, design, result, robustness), not seventeen; the abstract hits the JSSR word count and
structure; and the verbs match the weakest assumption with no causal-language *drift* across
poster, abstract, talk, and repo. The B drifts once — the talk says "proves" where the abstract
hedged — or the poster has the seventeen-panel chart-graveyard problem, or one table on the poster
is missing its SE-flavor note. **A: Excellent (~26). B: Proficient (~20).**

**Reproducibility — the one-click packet (34 pts).** The most objective row in the rubric, and you
grade it by *running it*: `make clean && make all` on a fresh clone. For the A it rebuilds every
table, figure, *and the poster's plots* byte-for-byte from raw data through seeded code. For the B
it rebuilds "after one fix" — a path that needed editing, a step that errored once — which is the
Proficient descriptor exactly. **A: Excellent (34). B: Proficient (~26).** (Note the two hard caps
that override the level descriptors: a packet that does not rebuild at all caps this row at
Developing, and a hard-coded secret caps it at Missing on its own, per CONVENTIONS §5 — check for
both before you score the row.)

**8-minute talk & Symposium defense (28 pts).** The A delivers the six-beat arc in figures-not-tables
inside the hard 8-minute cap, and — the part graded as hard as the talk — in the poster-session
question period *concedes the one fatal critique rather than bluffing* and can state precisely where
its own design is weakest. The B gives a solid talk but, in defense, argues harder when it should
concede; or runs over 8 minutes and is cut off by the Symposium chair before the robustness beat.
**A: Excellent (~28). B: Proficient (~22).**

**Honesty & disclosure (10 pts).** The A draws the confirmatory/exploratory line in public
(`DEVIATIONS.md`, labeled exploratory analyses), ships a complete category-correct AI-use disclosure,
and reproduces the disclosure on the poster and in the JSSR abstract per JSSR's submission policy.
The B logs a deviation without its outcome-driven verdict, or its disclosure is slightly vague, or
the poster omits the AI-use disclosure altogether. **A: Excellent (10). B: Proficient (~8).**

**The arithmetic.** The A lands near **200**; the B lands near **154** (≈24+26+28+20+26+22+8 across
the seven rows) — a high-B that is *not dishonest*, that simply, in the rubric's words, "has not
yet internalized that a failed check is a finding and a conceded critique is a strength." The gap
is ~46 points, and roughly half of it is concentrated in two rows — execution/robustness and
identification/threats — which is the rubric working as designed: it puts the weight where the
defensibility lives. Show this walk-through to every grader before they touch a capstone, because
the lesson is not the numbers, it is *where to look* — at the spec-curve mark, the failed check,
the conceded critique at the poster session, the byte-for-byte rebuild including the poster's
plots, and the verb consistency across poster, abstract, and talk.

---

## Part E — Running norming so multiple graders agree

When more than one person grades — co-instructors, mentor-TAs, or you across a stack large enough that
*you* drift between the first paper and the fortieth — you run **norming**, a short calibration ritual
before the real grading starts. The goal is inter-rater agreement: two graders reading the same paper
land within a level on every row. Norming is cheap insurance against the single worst grading failure,
which is a student's grade depending on *which* grader they drew.

**The protocol, before any real grading:**

1. **Everyone reads the rubric and the anchors first** — the gallery A-anchors and your B/C anchors
   from Part C — so the level descriptors are loaded against concrete examples, not abstractly.
2. **All graders independently score the same one or two calibration papers**, row by row, without
   conferring. Use a real paper from the current stack (then it is graded for real) or a held-aside
   anchor.
3. **Compare scores row by row and surface every disagreement of more than one level.** A one-level
   spread (Excellent vs. Proficient) is normal and fine; a two-level spread (Excellent vs. Developing)
   means the graders are reading the descriptor differently, and that is the conversation to have.
4. **Resolve each gap by returning to the rubric language and the anchor, not by averaging.** The
   point is to converge on a *shared reading* of the descriptor — "we agree this counts as one slip,
   so it is Proficient, not Excellent" — so the agreement holds for the rest of the stack. Write the
   resolution down; it becomes a grading note for next year.
5. **Re-norm mid-stack if the stack is large.** Drift is real over forty papers. A five-minute
   re-check on one paper halfway through catches a grader (or you) who has unconsciously gotten
   stricter or softer.

**Divide the work to minimize disagreement, not just to go fast.** If you split a stack across
graders, split it *by row* where feasible — one grader does the reproducibility row (running
`make clean && make all`) for every paper, another does identification for every paper — so each
grader holds one standard fixed across the cohort rather than every standard across a few papers. This
both speeds grading and tightens consistency, for the same reason the by-row pass works for a single
grader. Where you must split *by paper*, double-grade a random sample (say one in five) blind and
check that the two scores agree within a level; a sample that disagrees is a signal to stop and
re-norm.

**The two highest-signal checks override everything else, so verify them first and identically.** The
Week 8 assessment names them: (1) was there exactly *one* pre-registered primary spec, run once, with
`pap-filed` predating the confirmatory commit — check the Git history; and (2) does
`make clean && make all` actually rebuild the paper's numbers on a fresh clone — run it. These are the
most objective things in the rubric and the two most consequential for the grade (they gate the
execution and reproducibility rows). Agree as a grading team *exactly* how you check both — same
clone procedure, same reading of "predates" — before anyone scores a paper, because a split on these
two is the split most likely to change a letter grade.

Norm once well and the rest of the grading is mechanical in the best sense: graders disagree rarely,
disagree small when they do, and every student's grade reflects the rubric rather than the luck of the
draw. That is the whole purpose of answer keys, anchors, and norming together — to make the standard
the camp spent eight weeks teaching the *same* standard it is finally graded against.
