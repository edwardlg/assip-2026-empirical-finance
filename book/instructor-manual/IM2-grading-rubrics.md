# IM-2 — Grading Rubrics (Consolidated)

> **Companion documents.** This document consolidates the *grading* of every deliverable in the
> camp. The per-week assessment files (`book/weeks/week-0N/assessmentN.md`) remain the **detailed,
> authoritative source** for each week's rubric; this manual pulls them into one place, states the
> weighting that ties them together, and gives the consolidated tables an instructor needs at a
> glance. For the daily clock those deliverables sit in, see **IM-1 (Pacing Guide)**; for the errors
> the rubric is built to catch, see **IM-3 (Common Pitfalls)**; for worked answer keys and anchor
> papers calibrated to these levels, see **IM-5 (Answer Keys & Anchor Work)**; for accommodations
> that affect how the rubric is applied, **IM-6 (Equity/Access)**.

The camp grades four kinds of deliverable: **daily problem sets**, **weekly assessments**, the
**capstone paper** (the 200-point terminal rubric), and the **presentation/defense**. They are not
four unrelated scoring systems — they are one standard applied at four scales. The standard, pressed
since Chapter 1.5 and stated verbatim in the Week-8 assessment, is this: *a modest result you have
stress-tested honestly outscores an ambitious one you cannot defend.* Every rubric below is built to
reward calibrated honesty over confident error, and to make the design craft — identification,
robustness, reproducibility — weigh more than the eventual coefficient. An instructor who internalizes
that one sentence can grade the whole camp consistently; the tables exist to make the application
even-handed across students and graders.

A second cross-cutting principle: **every assessment is scored with an analytic, four-level rubric**
(Excellent / Proficient / Developing / Missing), one row per criterion, scored independently and
summed. Do not let a brilliant talk inflate a packet that does not rebuild; do not let one missing
placebo sink an otherwise honest battery. The four-level structure exists precisely to keep criteria
separable. Grade each row against its descriptor, then add.

---

## 1. The weighting that ties it all together

The deliverables compound: daily problem sets feed weekly assessments, weekly assessments rehearse
the design rubric, and the design rubric *is* the terminal capstone rubric. The program-level weight
should reflect that the capstone — for ASSIP 2026, the **Symposium poster + JSSR abstract + 8-minute
talk + reproducible repo** — is the only thing the camp was building toward. A defensible overall
weighting for the ASSIP 8-week full-time run:

| Component | Weight (of final grade) | Rubric source |
|---|---:|---|
| Daily problem sets (8 weeks × 5) | 15% | Per-PS; consolidated PS rubric in §2 |
| Weekly assessments (Weeks 1–6) | 25% | `assessment1`–`assessment6.md`; §3 |
| Week-7 design deliverable (PAP + memo, tagged commit) | 15% | `assessment7.md` (research-design rubric); §4 |
| Week-8 capstone (Symposium poster + JSSR abstract + 8-min talk + repo) | 35% | `assessment8.md` (200-pt rubric, re-allocated for ASSIP); §4 |
| Symposium defense & cohort participation | 10% | §5 + Friday show-and-tell |

Two shifts from the residential default deserve naming. First, the **Week-8 capstone bundle expands
from a paper-only deliverable to a four-part deliverable** (poster, abstract, talk, repo), and the
200-point terminal rubric re-allocates inside that bundle (§4b). Second, the **Symposium defense
absorbs the standalone presentation grade**: on Wed Aug 12, 2026, the 8-minute talk + poster Q&A *is*
the graded defense, scored live against §5. The principle is invariant: **identification,
execution/robustness, and reproducibility together should always exceed half the capstone grade**,
because those — not the coefficient — are what make a finding defensible. The terminal rubric
enforces this by construction (its three craft rows sum to 108 of 200, unchanged).

---

## 2. Daily problem sets — consolidated rubric

Problem sets are formative-leaning graded practice, ~6 problems each, with full worked solutions in
Appendix E (students attempt before consulting). They are not graded to the decimal; they are graded
to *whether the reasoning is right and honestly shown.* A correct number with no argument earns
little; an honest "I am not sure, here is why" earns more than a confident error. Use a compact
four-level rubric applied per problem and then to the set:

| Criterion | Excellent | Proficient | Developing | Missing |
|---|---|---|---|---|
| **Method / derivation** | Right tool named, steps shown, derivation correct | One slip, method sound | Method partly right, several errors | Wrong tool or not attempted |
| **Numerics / code** | Correct result; code runs, seed pinned where stochastic | Minor arithmetic/reproducibility slip | Logic flaw or partial output | Does not run / wrong target |
| **Interpretation** | Reads the result in context; units; no overclaiming | Mostly right, one link missing | Describes without interpreting | Absent or wrong |
| **Honesty / calibration** | Puts a number on uncertainty; flags "looks close" claims | Judgment sound, light quantification | Acknowledges noise, no number | Treats estimates as exact truth |

Two grading conventions keep PS scoring fast and fair. First, **the honesty row is not optional
politeness — it is the Week-1 mindset made gradable** (put a standard error on a simulated number;
do not call 0.058 "basically 0.05" without checking the Monte Carlo SE). Second, identify the
**two highest-signal problems** in each set and weight them; IM-5 flags which problems separate
strong from weak work (e.g., in PS 1.x the size/SE-of-a-simulated-number problems; in PS 4.x the
Goodman–Bacon negative-weights demo). Under compression you keep exactly those.

A practical scale: score each problem 0–4 against the dominant criterion, sum, and convert to a
percentage of the set. Reserve full marks for work that would earn "Excellent" on the honesty row,
not merely the numeric one — that is the differentiator the camp cares about.

---

## 3. Weekly assessments (Weeks 1–6) — consolidated view

Each weekly assessment is **100 points** and shares a common spine: a conceptual/derivation part, a
build-or-simulate part, and a presentation/honesty thread woven through both worth 10 points. The
exact split shifts as the camp turns from running estimators (Weeks 1–4) to reading/building them
(Weeks 5–6). The detailed rubrics live in each `assessmentN.md`; the consolidated weighting:

| Week | Total | Conceptual / derivation (Part A) | Build / simulate / produce (Part B) | Presentation & honesty | Signature graded skill |
|---|---:|---:|---:|---:|---|
| **W1** — Probability & Inference | 100 | 42 | 48 | 10 (woven) | Size of a t-test by simulation; SE *of* a simulated number |
| **W2** — OLS Engine | 100 | 48 | 42 | 10 (woven) | Choosing the right SE flavor on a clustered panel |
| **W3** — Causal I (PO/IV) | 100 | 48 | 42 | 10 (woven) | Weak-IV diagnosis; Anderson–Rubin coverage |
| **W4** — Causal II (DiD/RD/SC) | 100 | 48 | 42 | 10 (woven) | TWFE breaks under staggering; Callaway–Sant'Anna repairs |
| **W5** — Reading the Frontier I | 100 | 70 (write a Reader's Guide) | 20 (reading drills) | 10 (woven) | A 4-page Reader's Guide on an *unseen* paper |
| **W6** — Reading the Frontier II + AI | 100 | 70 (build + validate a classifier) | 20 (conceptual) | 10 (woven) | OOS-validated LLM classifier + leakage audit |

Three patterns to grade consistently across the six:

- **Weeks 1–4 are roughly half conceptual, half build**, with the build graded on
  *code-correctness-and-reproducibility* (does it run on a fresh env from the stated seed?) and the
  conceptual graded on *naming the right result and the right assumption* — the recurring high-signal
  items are the "spot the error" questions (W1 A6/A7 on finite-variance and the p-value-as-posterior
  error; W2 on which SE; W4 on the forbidden comparison). These are where strong and weak work
  separate; weight them when triaging.
- **Weeks 5–6 flip to 70/20** because the deliverable *is* a produced artifact — a Reader's Guide
  (W5) or a validated classifier (W6). The W6 rubric in particular weights **validation rigor and
  honesty** over the model's headline accuracy: a classifier with a precision/recall table against
  hand labels and a leakage audit outscores a higher-accuracy one with no validation. This is
  deliberate preparation for the capstone's reproducibility and disclosure rows.
- **The 10-point presentation/honesty row is identical in spirit everywhere**: clean prose, units on
  every number, no banned language ("proves," "accepts the null," significance-equals-importance).
  It is the same row that becomes the capstone's "Honesty & disclosure" row. Score it the same way at
  every scale.

The W1 assessment carries the canonical worked rubric and answer key (its A1–A7 sketches and Part-B
expected results); use it as the template for how to grade a weekly assessment, and see IM-5 for the
answer keys to the rest.

---

## 4. The capstone — the terminal 200-point rubric

Weeks 7 and 8 are one assessment in two halves. **Week 7 grades the design half** (PAP +
identification memo + reproducible repo, 100 points) against the *research-design rubric*; that same
rubric is then *extended* to the whole project in **Week 8, the 200-point terminal rubric**. Grade
the W7 deliverable on its own rubric at the end of W7 (Fri Aug 7), then grade the full capstone on
the 200-point rubric at the **ASSIP Symposium (Wed Aug 12)** for students completing the standard
deliverable bundle, and at the end of the four-week paper-refinement window for students who elect
the optional full JSSR paper. The two are continuous by design: the first two rows of the terminal
rubric carry forward the Week-7 design weights, and the new weight goes to *honest execution*.

### 4a. The Week-7 research-design rubric (100 pts)

The detailed version is in `assessment7.md`; the consolidated rows:

| Row | Pts | What "Excellent" requires |
|---|---:|---|
| **Identifying assumption + threats table** | 26 | Assumption names the *effect* and the *specific threat* (never "endogeneity"), verb (*causal/credible*) calibrated; threats table matches a *statistic to every testable threat and an argument to every arguable one*, every residual cell non-empty, ordered by descending danger |
| **Primary-specification discipline** | 18 | One primary spec in full seven-slot CONVENTIONS §4 form (outcome to a variable name · key regressor · named controls + a flagged over-control · FE · clustering justified in advance · exact sample with expected $N$ · identifying-assumption sentence) |
| **Multiple-testing plan** | 14 | Primary vs. secondary declared; secondary tests in pre-committed families with a named correction (BH-FDR or justified Bonferroni) at a stated level; family fixed in advance |
| **Reproducibility — tagged PAP + pinned env** | 12 | PAP/memo filed as a `pap-filed` tagged commit *before* any confirmatory result; env pinned; licensed-data snapshot pinned and on GMU infra; exploratory/confirmatory split reproducible; `DEVIATIONS.md` present; **no secret anywhere** |
| **Presentation & honest write-up** | 10 | PAP–memo division (honesty vs. validity) explicit; intrinsic vs. fixable limitations distinguished; admits where the design is weakest |

The four design-craft rows sum to **70 of 100** — more than two-thirds — by design. The two
highest-signal things to grade: (1) is there *exactly one* primary specification, named in full and
tagged before any result; (2) does the threats table match a statistic to every testable threat and
an argument to every arguable one, with no empty residual cell. A hard-coded secret caps the
reproducibility row at Missing on its own.

### 4b. The Week-8 terminal capstone rubric (200 pts) — ASSIP deliverable bundle

This is the program's terminal assessment, on the **four ASSIP deliverables that are one finding seen
from four sides**: the **poster** (the public face), the **JSSR abstract** (the published argument),
the **8-minute talk + defense** (the live defense at the Wed Aug 12 Symposium), and the **reproducible
repo** (the proof). The seven rows below are the residential-program rubric **re-allocated** to
reflect the ASSIP deliverable bundle — same structure, weights shifted so that the poster, abstract,
and talk get their proper share of the grade.

| Row | Pts | The bright line for "Excellent" — graded across poster + abstract + talk + repo |
|---|---:|---|
| **Research question & contribution** (in JSSR abstract + poster headline + talk opener) | 28 | One-sentence contribution naming a recognizable job (first/overturn/reconcile/mechanism/new-data) with a calibrated verb, consistent across abstract, poster headline, and the talk's first beat; lit review on poster *constructs* the gap by contrast; every citation in the JSSR abstract load-bearing and **verified** |
| **Identification & threats** (poster design panel + talk design beat + repo memo) | 34 | Assumption sentence names the *effect* and the *specific threat* (never "endogeneity"); threats table appears on the poster (compressed) and in full in the repo; matches statistic-to-testable and argument-to-arguable, no empty residual, ordered by danger |
| **Execution & robustness** (repo confirmatory results + poster robustness panel) | 40 | Pre-registered spec run *once* and reported whichever way it fell; spec curve with the pre-registered point marked; correct SE flavor + wild cluster bootstrap if few treated clusters; placebos; sensitivity sweeps; **Oster δ with $R_{\max}$ defended and swept to 1**; a *failed* check reported as a finding that narrows the claim — and shown on the poster, not buried in an appendix |
| **Communication craft — poster + abstract + writing** | 26 | Poster legible at 4 feet (headline, design, result, robustness — four panels not seventeen); JSSR abstract hits the journal's word count and structure; argument not transcript; headline-first; verbs match the weakest assumption with no causal drift; tables stand alone per Appendix D |
| **Reproducibility — one-click packet** | 34 | `make clean && make all` rebuilds every table/figure (and the poster's plots) to PDF from raw on a fresh clone; code-generated never pasted; env pinned (`.yml` + `.lock.yml`); SEED fixed/named/threaded; licensed data recipe-reproducible on GMU infra; **no secret anywhere** |
| **8-minute talk & Symposium defense** | 28 | Six-beat arc in 8 minutes (question → why it matters → design → headline result → robustness → contribution), one idea per slide, results as figures; defense at the Symposium poster session answers as threats-table rows, gives a *located* "I don't know," concedes a fatal critique rather than bluffing |
| **Honesty & disclosure** (repo `DEVIATIONS.md` + AI-use statement on poster + abstract) | 10 | Confirmatory/exploratory line drawn in public (`DEVIATIONS.md`); limitations as intrinsic vs. fixable; AI-use disclosure complete and category-correct (validation table for AI-produced data, citations verified), reproduced on the poster and in the JSSR abstract per JSSR policy |

The rows sum to 28 + 34 + 40 + 26 + 34 + 28 + 10 = **200**. The three craft rows — *identification &
threats* (34), *execution & robustness* (40), and the *one-click packet* (34) — still sum to **108**,
more than half the grade, by design. The two heaviest single rows are still the two questions a
Symposium audience and a JSSR referee both ask first: execution & robustness (40), and identification
& threats (34). The talk + Symposium defense row (28) now carries the live-presentation weight that
was 22 in the paper-only rubric — appropriate to the fact that the talk is in front of Mason faculty,
mentors, families, and Mason News press, and is the version of the result the world sees first.

A note on the four deliverables as **one finding seen from four sides**. A strong capstone tells the
same story consistently across the four artifacts: the JSSR abstract's headline, the poster's top
panel, the talk's first beat, and the repo's README all say the same one-sentence contribution with
the same calibrated verb. Inconsistency across artifacts — abstract says "associated," poster says
"causes," talk says "proves" — is a verb-drift failure that the Communication-craft row penalizes
heavily, because the public artifacts each get judged in isolation and a verb that drifts in any of
them is the one the reader will remember.

### 4c. Two non-negotiable caps

Two rules override the row-by-row sum and an instructor must apply them mechanically:

1. **The freeze.** Check the Git history. If the starred headline coefficient postdates no
   `pap-filed` tag, or the primary spec mutated after the first look, the contract is broken and the
   p-value no longer means what Chapter 1.5 says. This **caps Execution & robustness at Developing**,
   regardless of how clean the battery looks.
2. **The rebuild.** Run `make clean && make all` on a fresh clone. If it does not reproduce the
   paper's numbers, **caps Reproducibility at Developing**. If a hard-coded key or secret appears
   anywhere, **caps Reproducibility at Missing on its own**, no exceptions (CONVENTIONS §5).

These two checks are the most objective things in the entire camp. Run them first; they are not
formalities, they *are* the rows.

### 4d. The A/B line, stated once

Use this to calibrate. Both an A and a B capstone run a real design on real data and write it up
cleanly. The difference is **honest stress-testing under pressure**. The A capstone marks its
pre-registered point on the spec curve and it sits near the center; reports the check that *failed*
and narrows the claim; its Oster δ comes with a defended, swept $R_{\max}$; `make clean && make all`
rebuilds byte-for-byte; and in the defense the student concedes the one fatal critique rather than
bluffing. The B capstone runs the battery but shows only the passes, asserts $R_{\max}$ without the
sweep, leaves the spec-curve point unmarked, rebuilds "after one fix," and argues when it should
concede. The B is not dishonest — it has not yet internalized that a failed check is a finding and a
conceded critique is a strength. That internalization is the A. The capstone gallery
(`book/capstones/`) gives five worked anchors at the A/A− line; IM-5 supplies the annotated graded
versions.

---

## 5. The Symposium talk & defense — how to grade it

At the **ASSIP Research Symposium on Wed Aug 12, 2026**, every student delivers an **8-minute talk
plus a poster-session defense**, graded live against the W8 row in §4b (28 points). Score the **talk**
on the six-beat arc (question → why it matters → design / identification → headline result →
robustness → contribution), one idea per slide, every spoken result translated from a table into a
*figure*, and timing (rehearsed to fit in 8 minutes with a pre-decided cut line — the Symposium
schedule is fixed and the 8-minute cap is hard). Score the **poster-session defense** on whether the
student answers questions from the visiting audience (Mason faculty, mentors, families, College of
Science leadership, Mason News press) *as the rows of their own threats table* — threat →
why-plausible → what-they-did → residual-concern — gives a *located* "I don't know" when they cannot
answer, and can tell a survivable critique (it attacks a number) from a fatal one (it attacks the
comparison), conceding the fatal one honestly. The remote-cohort version of the defense runs in
**virtual breakouts** running concurrently with the in-person poster session; grade both formats
against the same grid.

Practical scoring grid for the defense, since it is the row instructors find hardest to grade live:

| Behavior | Excellent | Proficient | Developing | Missing |
|---|---|---|---|---|
| **Answers from the threats table** | Every answer routes to a row; structured threat→response→residual | Mostly structured, one rambling answer | Answers ad hoc, ignores own table | Cannot connect questions to design |
| **Located "I don't know"** | Says exactly which assumption is unprovable and why | Admits uncertainty, vaguely located | Deflects or guesses | Bluffs |
| **Survivable vs. fatal** | Concedes the fatal critique, defends the survivable | Concedes, but argues a bit long | Over-defends a critique it should concede | Bluffs the fatal critique |

The single most common defense failure is **arguing harder when one should concede** — that is the
B-not-A behavior. Reward the concession. A student who says "you're right, that critique attacks my
comparison, not just a number, and my design cannot answer it" demonstrates the exact judgment the
camp exists to teach, and should score above one who successfully bluffs.

For the **Symposium** (Wed Aug 12, 2026), grade the talk + defense live against this grid; bank the
score row-by-row and fold it into the §4b "8-minute talk & Symposium defense" row (28 pts) and into
the 10% Symposium-defense weight at final grading. The mentor-session question protocol in IM-4 is
the right rehearsal instrument for the **Tue Aug 11 dry-run defense** that IM-1 schedules — sub-leaders
run a mock poster-session round with their pod, with Prof. Gao floating between pods.

---

## 6. Grading fairly — the cross-cutting rules

Five rules that apply to every deliverable above:

1. **Grade the project the student chose to write**, not the one you would have written (the
   refereeing asymmetry of Ch 8.4). Ambition is not an axis; honesty under stress is.
2. **Reward calibrated honesty over confident error.** "My size was 0.058, but with a Monte Carlo
   SE near 0.0015 that is a real gap, not noise" outscores "the size was 0.058, basically 0.05" —
   even though both report the same number. This is the spirit of the honesty row at every scale.
3. **The robustness section that only passes is *less* credible.** A battery with no failed check
   reads as a student who did not try hard enough to fail. The scary placebo for the top-ranked
   threat must be present whether or not it passed.
4. **Read only the verbs attached to the main result, across sections**, and force them to the
   weakest assumption. Causal-language drift (hedged in the abstract, "proves" in the conclusion) is
   the most common writing failure; the verb audit catches it.
5. **Score each rubric row independently, then sum.** Do not let one strength mask one failure. The
   two mechanical caps (the freeze, the rebuild) are the only exceptions, and they exist because
   those two failures invalidate the whole inference rather than weakening one part of it.

Applied consistently, these rules make the rubric do what it is for: produce, across many students
and many graders, the same judgment a referee at the Journal of Student-Scientists' Research (JSSR), GMU Mason Publishing would reach — which
is exactly where the strongest of these papers are headed.
