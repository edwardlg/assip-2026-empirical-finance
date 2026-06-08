# PS 8.5 — Your 8-Minute Poster Talk + the One-Click Replication Packet

**Course:** ASSIP 8-Week Empirical Finance Camp · Week 8 · Problem Set 8.5
**Covers:** Ch 8.5 (The 8-Minute Poster Talk & the Replication Packet), standing on Lab 7 (the
repository that *is* the packet), Lab 8 (the final poster compile and dry-run), Ch 7.5 (the
threats table you defend under questions), Ch 8.2 (the robustness that fills your robustness
panel), and Appendix D (the packet and style standard).
**Type:** Project deliverable, not a numeric problem set. This is the last thing you build in
ASSIP, and it is the same project you have carried since Week 7 — your question, your data, your
pre-registered design — seen from its two public surfaces at the **Aug 12, 2026 ASSIP Research
Symposium**: the **8-minute talk you give standing beside your poster** (or on the symposium's
virtual-breakout track if you are one of Prof. Gao's remote interns) and the **folder a visitor
clones from the QR code on the poster**. There is no answer key with "the right number," because
what is graded is not a finding but two *crafts*: whether your eight minutes make one argument
land in front of a symposium audience, and whether a stranger can rebuild every number you claimed
by typing one command after scanning your QR code.

**Total: 100 points.** Point values are stated per part. A model deliverable — an A-grade
panel-by-panel poster outline and a completed replication-packet checklist for one cast project
(Maya's HMDA fair-lending DiD), with instructor grading notes — is in Appendix E
(`E-w8-ps8.5-solutions.md`). Read it *after* you draft your own, the way Ch 8.5 walked through the
cast talks: not to copy, but to calibrate.

A note on what this assignment is for. Ch 8.5 stated the thesis as bluntly as it deserves, and this problem set is where you earn it: **reproducibility is not a virtue you bolt on at the end — it is the form your credibility takes once you stop talking and the skeptic is alone with your folder.** A correct result nobody can follow on a slide, or nobody can rebuild on their own machine, is — to the person in the room — indistinguishable from a guess. So the single most valuable outcome of this problem set is *not* a pretty deck. It is the moment, during the `make clean && make all` honesty test, when the rebuilt PDF comes back with a number that does not match the one on your slide — and you find the hand-edit *before* a reviewer does. If that happens, the assignment did its most important job.

---

## What you submit

Three artifacts, all living inside the capstone repository you stood up in Lab 7 — there is no
separate upload, because (Lab 7, Step 2) the repository *is* the submission:

1. **The poster** — `paper/poster.pdf` (48"×36" landscape, built with `beamerposter` or PowerPoint
   per Lab 8 §1.2), committed to your repo. Six content panels in the reading order of the
   six-beat arc (Ch 8.5 §1), with the JSSR-ready abstract `\input`ed into the title block (Lab 8
   §1.1) and a scannable QR code resolving to your **public** repo in the contribution panel.
2. **The talk notes** — `paper/talk-notes.md`: your speaker notes, one short block per poster
   panel, including your **pre-decided cut line** (which panel you skim if you reach minute six
   still on the headline) and your **prepared answers** to the three hardest questions you expect.
   If you also use companion slides on the virtual-breakout track, ship `paper/slides.pdf` (≤ 7
   slides) too — the same six-beat arc, same titles, just a screen-optimized layout.
3. **The replication packet** — your finished Lab 7 repository, with the **six load-bearing parts**
   assembled (Ch 8.5 §5) and a single `make all` / `run_all.py` entry point that regenerates every
   table, figure, the JSSR abstract, **and the poster PDF** from raw inputs. Plus
   `REPLICATION-CHECKLIST.md` at the repo root: the completed packet checklist (Part 4 below),
   each box checked with the command output or file that proves it.

The poster is the visual artifact and the talk notes are short by design; the packet is where
most of the work already lives, finished. All three are graded together, because they are the
same project: the poster + talk *claim* the numbers, the packet (reached via the QR code)
*proves* them.

---

## Part 1 — The 8-minute deck: the six-beat arc (35 points)

Build a deck that hits the six beats of Ch 8.5 §1, in order, **one beat per slide**, with a title slide making seven in total. Eight minutes has room for exactly one idea defended cleanly; the slides exist to keep you and the room on that one idea. Budget roughly one minute per slide and target a talk that fits in **seven** minutes in rehearsal, not eight (§3) — the eighth minute is insurance, not content.

Each beat below is one slide, and each is graded on whether it does *its* one job and no other:

- **(a) The question slide (5 pts).** One sentence a smart sixteen-year-old could repeat back. Not the literature, not the motivation — the question. (Devon's: *"Does the launch of a spot Bitcoin ETF reduce the volatility of the underlying token?"*) The title *is* the question. No three-paragraph history; the room cannot hold context it has not yet been given a reason to want.
- **(b) The why-it-matters slide (5 pts).** One concrete stake a stranger feels in thirty seconds — *concrete before abstract, a number before a Greek letter* (CONVENTIONS §1). Priya's opens not with the IPCC but with: *"if wildfire risk is mispriced, insurers either go insolvent or abandon whole counties."* This comes *after* the question, never before.
- **(c) The design / identification slide (8 pts — the spine).** Your identifying-assumption sentence from Ch 7.5, on the screen, in the contract form: *"Our estimate is credible as long as [the assumption], which we defend by [the design]."* This is **not** your regression equation — nobody reads a regression equation in sixty seconds. It is a slide about *why the comparison is fair*, ideally with one small picture. If the room leaves understanding only one slide, it must be this one; this is where every hard question lands.
- **(d) The headline-result slide (6 pts).** **One** number, with its uncertainty, shown as a *picture*, not a table — and one sentence of interpretation in human units ("1.8 percentage points, about a fifth of the baseline gap," not "$\hat\beta = 0.018$, $t = 3.2$"). A confidence interval is part of the result, not an afterthought; a point estimate with no interval reads as naïve or evasive.
- **(e) The robustness slide (6 pts).** The visual answer to "is your result fragile?" — a specification curve or a small grid of alternative specs, all clustering near the headline (this is where Ch 8.2 pays off). You do not narrate every check; you show they exist and agree, in one sentence: *"the result is stable across [the three choices I worried about most]."* This pre-empts the §3 questions before anyone asks.
- **(f) The contribution slide (5 pts).** One sentence naming what the room now knows that it did not eight minutes ago — *and* one clause naming what you are **not** claiming ("we show X, under assumption Y; we do not show Z"). That last clause is not weakness; it is the single most credibility-building sentence in the talk. Then stop.

**Grading note on slide discipline.** Every slide is also scored on the **one-idea-per-slide** rule (Part 2). A slide with two ideas, or a noun-phrase title ("Results") instead of a full-sentence claim, loses points even if its content is correct — because in a live talk a crowded slide costs you the room.

---

## Part 2 — One idea per slide, and the table-to-figure translation (20 points)

Two rules govern what goes *on* each slide; both respect the fact that a live audience reads with their ears, not their eyes.

**(a) One idea per slide — and the title test (8 pts).** A slide is a single claim with a single piece of evidence for it. The test is brutal and useful: if you cannot write the slide's one idea as its *title* — a full sentence, not a noun phrase — the slide is doing too much. "Results" is not a title; *"The denial gap falls 1.8 points after the regulation, and the fall is concentrated in algorithmic lenders"* is a title, because it *is* the idea. A reader who reads only your titles should get the whole argument. For full marks, every one of your eight titles must pass this test; submit them as a list at the top of `slides-notes.md` so a grader can read the argument from titles alone.

**(b) The table-to-figure translation (12 pts).** This is the highest-leverage skill in the chapter. Your paper's results live in a precise regression table (the four-decimal, standard-errors-in-parentheses object Appendix D specifies). That table is *correct* and *unreadable from row eight of a lecture hall in four seconds.* So you do not show it — you **translate it into a figure** for the talk, and leave the table in the paper and on a backup slide. The translation is mechanical (Ch 8.5 §2); pick the one your design demands and state, in `slides-notes.md`, *which* translation your headline and robustness slides use and *why*:

| Your result is… | The talk figure is… | The eye reads… |
|---|---|---|
| a single coefficient + CI | a **point with an error bar** | "different from zero?" and "how precise?" |
| a coefficient across specs | a **coefficient plot** (dot-and-whisker per spec, reference line) | stability as a *shape* — a tight cluster |
| a difference-in-differences / event study | an **event-study plot** (effects by period: flat before, jump after) | the parallel-trends defense, made visible |
| a regression discontinuity | a **binned scatter with the fitted jump at the cutoff** | the discontinuity you can *see* |
| a subgroup pattern | a **small-multiples bar chart** | the gap is bigger here than there |

The principle under all of them: *a table is for a reader who can stop and study; a figure is for a listener who cannot.* Same number, two encodings, chosen for the medium — this is not dumbing down; the error-bar slide is exactly as precise as the table. One mercy rule for the figures themselves, also graded: a slide figure needs axis labels readable from the back of the room and *no more than is load-bearing* — strip the gridlines, the dead legend, the third decimal on the ticks. **Non-negotiable, and tied to Part 4:** the figure on your slide must be the *same file your code generated* into `paper/figures/`, never a hand-drawn or hand-pasted picture. If your slide figure and your packet figure can drift apart, the chain is already broken.

---

## Part 3 — Defending identification under questions (15 points)

The talk is eight minutes; the questions are where the talk is judged. A polished eight minutes followed by a flailing answer to the first question undoes the polish. The good news: you already did the work — **the questions you will get are the rows of your Ch 7.5 threats-and-responses table.** You are not improvising; you are reading from a script you authored when you were calm. In `slides-notes.md`, write out three prepared answers:

**(a) Two prepared "what about [confound]?" answers (6 pts).** Every hard empirical question has the shape *"isn't your estimate just picking up [some confounder]?"* — which is your identifying assumption attacked at a named weak point you wrote yourself (column 1 of the threats table). For your **two most likely** such questions, write the four-part answer in order: the threat (their question), why it's plausible (so you don't dismiss it), what you did about it (column 3 — the test or design choice), and the residual concern (column 4 — what honestly remains). The template: *"Yes, that's the central worry — if [confounder] were driving this we'd see [signature]; we checked, and we see [reassuring result]; what I still can't fully rule out is [residual], though [bound on how bad it could be]."*

**(b) One located "I don't know" (5 pts).** You will get a question you cannot answer; everyone does. Bluffing costs you more credibility than the gap ever would — a room of professionals smells it instantly. Write one honest, *located* "I don't know": not a bare shrug but *"I don't know — that's outside what my design can speak to, because [reason]; my guess is [direction], but I'd want to [the specific check] before claiming it."* (Maya, asked whether her fair-lending effect generalizes to auto loans, does not invent a number; she names the mechanism — examiner attention — and says auto lending has a different supervisor, so she would re-run it there before extending the estimate.)

**(c) Fatal vs. survivable, and your retreat position (4 pts).** State, in one sentence, which single critique would be **fatal** to your causal claim — *a fatal critique attacks the comparison; a survivable one attacks a number* (Ch 8.5 §4, mapping to Ch 7.5 §4's testable-vs-arguable). Re-clustering or winsorizing differently is survivable: "we checked; it doesn't move." A pre-existing divergence between treated and control, or an instrument that affects the outcome directly, is fatal: no re-clustering saves you. Then write your **retreat position** in advance: if the fatal critique lands and the attacker is right, you concede at the level it was made and retreat to what survives — almost always *"this is a robust pattern that future work with [the better design] should test causally,"* which is a real, honest, publishable contribution. Know this before you walk in; it is what the residual-concern column was *for*.

---

## Part 4 — The one-click replication packet (30 points)

Now the second surface, the one the skeptic touches alone. The bar from Appendix D and Lab 7 is exact and unforgiving: **a stranger, on a machine that has never seen your project, runs one command and watches every table and figure in your paper regenerate from raw data to final PDF.** Not "mostly." Not "after I email a fix." One command, everything. Assemble the **six load-bearing parts** on top of your Lab 7 repo and verify each:

- **(a) The data — or a data-access script (5 pts).** Public data ships *in* the packet, cached, with its vintage pinned. Licensed data (CRSP, Compustat, anything from WRDS) does *not* ship — the license forbids redistribution (CONVENTIONS §5) — so what ships instead is the **data-access script** in `src/` (the bounded, pinned query that reconstructs it for anyone with the same access) plus the `logs/pulls.jsonl` log with content hashes. This is Lab 7's *asymmetry of reproducibility*: public data fully re-runnable, licensed data recipe-reproducible. Your README states honestly which is which. *(Maya's HMDA is public, so it ships — many capstones' licensed sources do not.)*
- **(b) Code in run-order (5 pts).** Scripts in `src/` and notebooks in `notebooks/`, named or numbered so the order is unambiguous (`01_pull.py`, `02_build.py`, `03_analysis.py`). Lab 7's rule holds: *logic in `src/`, story in `notebooks/`.* A reviewer should never have to guess which script runs first.
- **(c) A README (4 pts).** The *what / why / how-to-run* document from Lab 7, but the "how to run" section has now collapsed to almost nothing, because the answer is one command. It still names the data sources, the secrets a user must `export`, and the licensed-vs-public split.
- **(d) A pinned environment file (4 pts).** Both files from Lab 7: human-readable `environment.yml` (Python 3.11 + the CONVENTIONS §5 stack) and machine-exact `environment.lock.yml`. The sentence you must be able to say: *"my results were produced under `environment.lock.yml`; rebuild that and you rebuild my numbers."*
- **(e) A fixed, named SEED (5 pts).** Anywhere your code uses randomness — a bootstrap, a train/test split, a permutation or placebo test, a simulation — it must be seeded from a *single named constant* set once at the top of the run, not scattered ad-hoc. Without it, your bootstrap CI is *different every run* and your headline interval is, strictly, irreproducible. Use the modern generator, not the legacy global:

  ```python
  # config.py — one seed, imported everywhere randomness happens
  SEED = 20260815  # the conference date; any fixed int, just FIXED and named

  # at the top of every script/notebook that uses randomness:
  import numpy as np
  from config import SEED
  rng = np.random.default_rng(SEED)   # a seeded Generator, not legacy np.random.seed
  ```

  Record the seed in the README so a reviewer knows it was fixed *before* results, not tuned after. (A seed you *searched over* for a prettier interval is p-hacking with extra steps, Ch 7.3's garden of forking paths in disguise; the `pap-filed` tag is what proves you didn't.)
- **(f) A single `make all` / `run_all.sh` entry point (7 pts).** The one-click. A single command that runs the whole pipeline *in order* — pull (or load cached), build the dataset, run every estimation, regenerate every figure and table, compile the paper to PDF — so a fresh clone goes from raw inputs to finished document with no human in the loop. The non-negotiable property: **the figures and tables in your paper are *generated by the code*, never pasted by hand.** `03_analysis.py` writes `paper/figures/event_study.pdf` and `paper/tables/main_results.tex`, and the LaTeX `\includegraphics`/`\input`s them. The instant a human copies a number from a notebook into the manuscript, the chain breaks and the packet is no longer one-click.

  The honesty test, which you must run and record the result of: **`make clean && make all`.** Delete every derived file and rebuild from nothing. If the paper comes back byte-identical, the packet is real. If a number drifts, you just found a hand-edit — find it now.

---

## Submission checklist — `REPLICATION-CHECKLIST.md`

Paste this into `REPLICATION-CHECKLIST.md` at your repo root and check a box only when you can point to the command output or file that proves it — this is exactly the audit a referee (or Prof. Gao, at the conference) would run.

**The deck**
- [ ] Exactly 7 slides (1 title + 6 beats) hitting the beats in order (title · question · why · design · headline · robustness · contribution), one beat per slide.
- [ ] Every slide title is a *full-sentence claim*, not a noun phrase; the argument is legible from the titles alone (list pasted atop `slides-notes.md`).
- [ ] The design/identification slide shows the *identifying-assumption sentence* (Ch 7.5), not the regression equation.
- [ ] The headline slide shows *one* number with its *confidence interval*, as a **figure**, with a human-units interpretation sentence.
- [ ] The robustness slide is a specification curve or coefficient grid clustering near the headline (Ch 8.2), with a one-sentence stability claim.
- [ ] The contribution slide names what is now known *and* what you are *not* claiming.
- [ ] Every slide figure is the *same file your code generated* into `paper/figures/` — none hand-drawn or hand-pasted.

**The talk**
- [ ] Rehearsed timed at least three times; fits in **seven** minutes, not eight.
- [ ] A **cut line** is pre-decided and written in `slides-notes.md` (which slide you skip if you are behind — never the design or headline slide).
- [ ] Two prepared "what about [confound]?" answers (threat → plausible → what you did → residual) and one located "I don't know," written out.
- [ ] Your one **fatal** critique is named, and your **retreat position** is written before you walk in.

**The packet**
- [ ] All six parts present: data/access-script · code in run-order · README · pinned env (`environment.yml` + `environment.lock.yml`) · fixed named SEED · single `make all`/`run_all.sh`.
- [ ] README states the public-vs-licensed split honestly; **no licensed data and no secrets** anywhere in the repo or its history (`git ls-files` is clean — Lab 7, Step 5).
- [ ] The SEED is a single named constant, threaded through every stochastic step via `np.random.default_rng(SEED)`, and recorded in the README.
- [ ] Every table and figure in `paper/` is *generated by code* and `\input`/`\includegraphics`'d — none pasted by hand.
- [ ] **`make clean && make all`** rebuilds the paper from nothing and the PDF is *identical* to the committed one. (If not: you found a hand-edit — fix it, then re-run.)
- [ ] Verified on a **fresh clone**, not just your working copy — the true "stranger's machine" test (Lab 8).

---

## How this is graded

This problem set is graded on the two crafts, weighted as the parts show: the deck (Parts 1–2, 55 pts) on whether one argument lands cleanly under slide discipline; question-handling (Part 3, 15 pts) on whether you defend identification honestly rather than bluff; and the packet (Part 4, 30 pts) on whether `make clean && make all` actually rebuilds your claims. The highest-signal single check is the honesty test: a packet whose rebuild does not reproduce the slide's headline number fails the part regardless of how polished the deck is, because — Ch 8.5 §6 — *a result a stranger cannot reconstruct is not yet a result; it is a claim about a result.* The model deliverable in Appendix E shows the A-grade standard for one cast project, annotated with the rubric levels each piece hits.

---

## The bridge — and the close of the camp

This is the last deliverable, and it closes the arc the whole camp walked. Look back at Week 1: the first thing you did was compute an average return of about eight percent, and it felt like an answer. It was the *first question*. You learned the eight percent had a standard error, that the standard error rested on assumptions you could not see, that a "significant" sign could be an artifact of how many specifications you quietly tried. Week 2 turned correlation into regression and the ghost of omitted-variable bias; Weeks 3–4 turned "we control for X" into *designs* — IV, RD, DiD, synthetic control — each a specific argument for why a comparison is fair; Week 5 taught you to read a paper as a skeptic; Week 6 sharpened the inference; Week 7 made it *yours* — an idea, data pulled reproducibly, a pre-analysis plan tagged before you could fool yourself, an identification memo that named every threat. Week 8 made it *communicable and checkable*: written up with calibrated verbs (Ch 8.3), stress-tested for robustness (Ch 8.2), peer-reviewed (Ch 8.4), and now — today — defended in eight minutes and packaged so a stranger can rebuild every claim with one command.

The single sentence this whole camp existed to let you say truthfully: *"Here is what I found, here is exactly why you should believe it, and here is the command that lets you check me."* When you build this deck and this packet, you can say it. The eight percent was the toe in the water. This is the swim.

*End of PS 8.5. The model deliverable is in `book/appendices/E-solutions-manual/E-w8-ps8.5-solutions.md`. Build your own deck and finish your own packet first; read the exemplar to calibrate, not to copy. The skeptic who clones a stranger's repo and types `make all`, and the author who makes their own rebuild honestly, are the same person — this assignment is you doing to your own work, on purpose, what a referee will do to it next.*
