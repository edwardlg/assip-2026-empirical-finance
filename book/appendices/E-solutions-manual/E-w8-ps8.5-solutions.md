# Model Deliverable — PS 8.5 (8-Minute Deck + One-Click Replication Packet)

**Problem set:** `book/weeks/week-08/ps8.5.md` (PS 8.5, Week 8).
**Chapter:** Ch 8.5 — The 8-Minute Presentation & the Replication Packet.

PS 8.5 has no numeric answer key: it is the camp's final project deliverable, and what is graded is not a finding but two *crafts* — whether eight minutes make one argument land, and whether a stranger can rebuild every claimed number with one command. So this appendix entry is not a worked solution but a **model deliverable**: a complete, A-grade slide-by-slide deck outline (seven slides — one title plus the six beats of Ch 8.5 §1 — with speaker notes) plus a completed replication-packet checklist — repo layout and `make`/`run_all` entry point included — for one cast project, followed by **instructor grading notes** that key each piece to the rubric and call out the moves that earn (and lose) points.

The project is **Maya's HMDA fair-lending difference-in-differences** — the staggered DiD she carried from Lab 4 through her Week-7 pre-analysis plan and identification memo into the Week-8 paper: *do state fair-lending examination programs reduce the county-level minority–white gap in mortgage-denial rates?* Her primary estimate is a Callaway–Sant'Anna overall ATT against never- and not-yet-treated controls (Ch 4.2), clustered by state. Every magnitude below is **illustrative** — the figures (an ATT near −1.8 percentage points, a confidence interval, a baseline gap) are presented as a worked *talk* example to show what an A-grade slide says, not as a claimed empirical result; the real number comes out of `make all` on the real pinned HMDA vintage.

---

## PART A — THE DECK (`paper/slides.pdf`, 7 slides: 1 title + 6 beats)

Below: each slide's full-sentence title (the one-idea-per-slide title test, PS 8.5 Part 2a), what sits *on* the slide, and the speaker notes that would live in `paper/slides-notes.md`. Read the **titles alone, top to bottom** — they should tell the whole argument:

> 0. *(title)* Do Fair-Lending Exams Shrink the Mortgage Denial Gap? — Maya R., Capstone
> 1. **Does adopting a state fair-lending examination program reduce the minority–white gap in mortgage-denial rates?**
> 2. **A mispriced or discriminatory denial gap locks families out of homeownership — and we don't know if examinations actually move it.**
> 3. **Our estimate is credible if, absent the exams, treated and never-treated states' denial gaps would have moved in parallel — which we defend with flat pre-trend leads and clean (never-/not-yet-treated) controls.**
> 4. **Adopting an exam program shrinks the denial gap by about 1.8 percentage points — roughly a fifth of the baseline gap.**
> 5. **The −1.8-point result is stable across clustering, control-group, and bandwidth choices, and survives a placebo on never-treated states.**
> 6. **Exams reduce the denial gap where the supervisor's attention reaches; we do not show they change loan *terms*, only the approve/deny margin.**

That is the argument in seven sentences. A reader who skims only the titles already knows the question, the stake, the design, the number, that it is robust, and where it stops. That is what one-idea-per-slide buys you.

---

### Slide 0 — Title

**On the slide:** Title (*Do Fair-Lending Exams Shrink the Mortgage Denial Gap?*), name, the camp/conference, one line: "all results regenerate from raw data via `make all` — repo on the last slide."

**Speaker notes (~15 sec):** "I'm Maya; I study whether a specific fair-lending policy actually changes who gets a mortgage. Everything you'll see is reproducible — there's a command at the end that rebuilds every number." *Get off this slide fast; the clock starts on slide 1.*

---

### Slide 1 — The question (beat 1)

**Title:** *Does adopting a state fair-lending examination program reduce the minority–white gap in mortgage-denial rates?*

**On the slide:** the question, large, and nothing else. Maybe one small map thumbnail of which states adopted, no labels.

**Speaker notes (~40 sec):** "Here's the one question. Some states run examination programs that audit lenders for fair-lending compliance; others don't, and they turned these on in different years. I ask whether turning one on shrinks the gap between how often minority and white applicants get denied — holding the applicant pool fixed as best I can." *Do not open with the history of the Fair Housing Act. The room cannot hold context it has no reason to want yet; the reason comes on slide 2.*

---

### Slide 2 — Why it matters (beat 2)

**Title:** *A mispriced or discriminatory denial gap locks families out of homeownership — and we don't know if examinations actually move it.*

**On the slide:** one concrete stake, one number for scale (illustrative): "the raw minority–white denial gap runs near 9 points; exams cost states real money — do they work?"

**Speaker notes (~25 sec):** "Homeownership is how most American families build wealth, so a denial gap isn't abstract — it compounds across a generation. States spend real money standing up these exam regimes on the *theory* that supervision shrinks the gap. Nobody has cleanly tested whether it does. That's the gap I fill." *Concrete before abstract, a number before a Greek letter (CONVENTIONS §1). This is where you spend the motivation — after the question, not before.*

---

### Slide 3 — Design / identification (beat 3 — the spine)

**Title:** *Our estimate is credible if, absent the exams, treated and never-treated states' denial gaps would have moved in parallel — which we defend with flat pre-trend leads and clean (never-/not-yet-treated) controls.*

**On the slide:** the **identifying-assumption sentence** in the Ch 7.5 contract form, plus one small picture — the cohort-mean denial-gap lines (treated cohorts tracking the never-treated line *before* adoption, peeling off *after*). **No regression equation.** A one-line spec strip at the bottom in plain words: "within-state-and-year comparison; clustered by state; Callaway–Sant'Anna against clean controls (Ch 4.2)."

**Speaker notes (~90 sec — slow down here):** "This is the slide that matters. My claim is causal *only if* one thing holds: that absent the exams, the states that adopted would have moved like the states that never did. I can't prove that — it's a statement about a counterfactual that never happened. But I defend it two ways. First, the picture: before each cohort adopts, its denial-gap line tracks the never-adopters — that's the flat pre-trend you can see. Second, I never use an already-treated state as a control for a later one, because its own effect is still building and would contaminate the comparison — that's the staggered-DiD trap from the literature, and the clean-control estimator avoids it. If you only remember one slide, remember this one." *This is where every hard question lands; if this slide is weak, the talk does not survive questions.*

---

### Slide 4 — Headline result (beat 4)

**Title:** *Adopting an exam program shrinks the denial gap by about 1.8 percentage points — roughly a fifth of the baseline gap.*

**On the slide:** **one figure** — the event-study plot: estimated effect by event-time, flat and hugging zero before adoption, dropping to about −1.8 after, with a shaded confidence band. One annotation: "overall ATT ≈ −1.8 pp [−2.8, −0.8]." *(All illustrative.)* **No table.**

**Speaker notes (~80 sec):** "Here's the answer. Each dot is the effect on the denial gap in a year relative to when the exam turned on. Before — flat, sitting on zero; that's the parallel-trends defense from the last slide, now as data. After — it drops and stays down, around 1.8 points. In human terms: the baseline gap is about nine points, so the exams close roughly a fifth of it. And the confidence interval — about minus-2.8 to minus-0.8 — doesn't include zero, but notice I'm *showing* you the interval, not hiding behind a point estimate. The effect is real but not enormous." *The CI is part of the result, not an afterthought. The event-study plot is the table-to-figure translation (PS 8.5 Part 2b): a DiD result becomes an event-study plot, and the flat pre-period argues identification for free.*

---

### Slide 5 — Robustness (beat 5)

**Title:** *The −1.8-point result is stable across clustering, control-group, and bandwidth choices, and survives a placebo on never-treated states.*

**On the slide:** a **specification curve / coefficient plot** — one dot-and-whisker per alternative spec (state-clustered vs. wild-cluster-bootstrap SEs; never-treated vs. not-yet-treated controls; with/without the population floor; ±1 year of the adoption window), all clustering near −1.8, with a vertical reference line at the headline. A second small panel: the placebo distribution (random fake-adoption years) centered on zero with the real estimate far in the tail.

**Speaker notes (~55 sec):** "I tried to kill this number. Cluster by state, bootstrap the standard errors, swap the control group, raise the sample floor, shift the adoption window — it sits near minus-1.8 every time; that's the tight vertical cluster. And the placebo: when I assign fake exam dates to states that never adopted, the effect vanishes to zero — so I'm not picking up some mechanical artifact of the estimator. The result didn't depend on one lucky choice." *You don't narrate all twelve specs; you show they exist and agree, in one sentence. This pre-empts the survivable critiques before anyone asks (Ch 8.5 §3).*

---

### Slide 6 — Contribution (beat 6)

**Title:** *Exams reduce the denial gap where the supervisor's attention reaches; we do not show they change loan terms, only the approve/deny margin.*

**On the slide:** one sentence of what's new, one clause of what's *not* claimed. A pointer: "repo + one-click rebuild → `make all` · github.com/CAMP-ORG/capstone-2026-maya".

**Speaker notes (~40 sec):** "So: a cleanly-identified estimate that fair-lending examinations actually shrink the denial gap, by about a fifth — under a parallel-trends assumption I've defended but can't prove. What I'm *not* claiming: I look only at approve-versus-deny, not at the rate or terms applicants got, and only at mortgages, not other credit. And the exact code that produces every number is one command away — clone it and you'll get my figure, seed and all. Thank you." *The "what we do not claim" clause is the single most credibility-building sentence in the talk — it signals you know exactly where your claim stops. Then stop; do not summarize the summary.*

---

### Backup slides (shown only if asked)

The precise regression **table** (Appendix D format, four decimals, SEs in parentheses — the object the slide-4 figure was *translated from*); the Goodman–Bacon decomposition; the full pre-trend leads with confidence bands; the imputation count by treatment status. These exist for the questioner who wants the fourth decimal — *a table is for a reader who can stop and study; a figure is for a listener who cannot.*

---

### Speaker-notes appendix: timing, cut line, and prepared answers

**Time budget (target 7:00, not 8:00).** Title 0:15 · Q+why 1:05 · **design 1:30 (slow)** · **headline 1:20 (let it land)** · robustness 0:55 · contribution 0:40 = ~5:45 of content, ~1:15 of slack for the things that go wrong. Rehearsed timed ×4; longest run 7:10.

**Cut line (pre-decided).** If I'm at minute six and still on the headline, I **drop the placebo panel of slide 5** and say one sentence ("it also survives a placebo — happy to show it"). I never cut the design slide or the headline. Deciding this in advance means I cut cleanly instead of panicking.

**Prepared answer 1 — "Aren't adopting states just on a better trajectory anyway?" (the fatal one).** *Threat:* differential pre-trend — reform-minded legislatures might both pass exams *and* already be improving. *Plausible:* yes, entirely; this is the central worry. *What I did:* the event-study leads are flat and tight enough to rule out an economically meaningful pre-slope, and adoption timing tracks legislative calendars, not local lending conditions. *Residual:* a flat pre-trend fails to *refute* parallel trends but can't *confirm* the post-period counterfactual, and with few treated states the leads have limited power. "So I'd say: consistent with parallel trends, not proof of it."

**Prepared answer 2 — "Why cluster by state, not county?" (survivable).** *This attacks a number, not the comparison.* "Treatment turns on at the state level, so the errors correlate within state — that's the right level (BDM). I also report a wild-cluster bootstrap because there are few treated states; the result holds. It's on the robustness slide and in the backup table." *A survivable critique: the number might wiggle, it doesn't vanish.*

**Prepared answer 3 — the located "I don't know": "Would this generalize to auto loans?"** "My data is mortgages, so I genuinely don't know. The mechanism I identify is *examiner attention*, and I'd expect it to matter wherever there's a comparable exam regime — but auto lending has a different supervisor, so I wouldn't extend the estimate without re-running it there." *Located, not a shrug: it admits the limit, explains why it's a limit, and names what would resolve it — a better answer than a confident yes.*

**Fatal vs. survivable, and my retreat position.** The *fatal* critique is a real pre-existing divergence in the denial gap (it attacks the comparison; no re-clustering saves me). The *survivable* ones attack numbers (clustering, winsorizing, controls) — "we checked; it doesn't move." **Retreat position, written before I walk in:** if someone shows the pre-trends genuinely tilt, I concede at that level — "you're right I can't rule that out with this design; the honest reading is a strong association consistent with the examiner-attention mechanism, which future work with [an RD on an exam-eligibility threshold] should test causally." A conceded fatal critique is a wounded paper but an intact scientist.

---

## PART B — THE REPLICATION PACKET (completed checklist)

### Repo layout (the Lab 7 repository, finished)

```
capstone-2026-maya/
├── README.md                  # what / why / how-to-run (one command) + public-vs-licensed split
├── Makefile                   # `make all` rebuilds EVERYTHING raw -> paper.pdf
├── run_all.sh                 # same pipeline, no make required
├── environment.yml            # human-readable: python=3.11 + CONVENTIONS §5 stack
├── environment.lock.yml       # machine-exact: every package at the solved version
├── config.py                  # the single fixed SEED, imported everywhere randomness happens
├── .gitignore                 # blocks data/, .env, *.parquet, keys (Lab 7 Step 5)
├── PRE-ANALYSIS-PLAN.md        # tagged `pap-filed` before any confirmatory regression
├── DEVIATIONS.md               # dated departures from the PAP, all after the tag
├── memo.md                     # the Ch 7.5 identification memo (the talk's design slide)
├── REPLICATION-CHECKLIST.md    # this checklist, each box proven
├── data/
│   ├── raw/                    # GIT-IGNORED; cached public HMDA pulls land here
│   │   └── .gitkeep
│   └── processed/              # GIT-IGNORED; built county-year panel
│       └── .gitkeep
├── src/
│   ├── 01_pull_data.py         # CFPB HMDA Data Browser pull (public) + FRED controls; logs hashes
│   ├── 02_build_dataset.py     # aggregate LAR -> county-year denial-gap panel; survivorship/look-ahead checks
│   └── 03_analysis.py          # CS estimator + robustness; WRITES tables/ and figures/ (seeded)
├── notebooks/
│   └── nb8.5_manuscript_build.ipynb   # story/narration; calls src/ logic, no analysis buried in cells
├── logs/
│   └── pulls.jsonl             # one line per pull: what, when, vintage, content hash
├── data-cards/
│   ├── hmda.md                 # public; CFPB vintage pinned
│   └── fred.md                 # public; controls
└── paper/
    ├── main.tex                # \input{tables/...} and \includegraphics{figures/...} — never pasted
    ├── slides.pdf              # the 8-slide deck (Part A)
    ├── slides-notes.md         # speaker notes, cut line, prepared answers
    ├── figures/                # event_study.pdf, spec_curve.pdf — GENERATED by 03_analysis.py
    └── tables/                 # main_results.tex — GENERATED by 03_analysis.py
```

The rule from Lab 7 holds visibly: *logic in `src/`, story in `notebooks/`*, the `data/` tree git-ignored, the licensed-data wall enforced by `.gitignore`. Here HMDA is **public**, so it ships cached in `data/raw/` with its vintage pinned — but the same layout would keep a CRSP-based capstone's licensed bytes on GMU infrastructure and ship only the `src/01_pull_data.py` access script plus the hash log (Ch 8.5 §5, the asymmetry of reproducibility).

### The single entry point — `Makefile`

```makefile
# Makefile — `make all` regenerates EVERYTHING from raw to paper/main.pdf.
.PHONY: all data analysis paper clean

all: paper

data:                       ## pull (public HMDA + FRED) or load cache, then build the panel
	python src/01_pull_data.py
	python src/02_build_dataset.py

analysis: data              ## estimate CS ATT + robustness; write tables/ and figures/ (deterministic via SEED)
	python src/03_analysis.py

paper: analysis             ## compile the write-up, pulling in the just-built tables/figures
	cd paper && latexmk -pdf main.tex

clean:                      ## delete ALL derived outputs so a rebuild is honest
	rm -rf data/processed/* paper/tables/* paper/figures/* paper/main.pdf
```

The equivalent shell entry point, for a reviewer without `make`:

```bash
# run_all.sh — same pipeline: `bash run_all.sh`
set -euo pipefail                 # stop on the first error; never silently half-build
python src/01_pull_data.py
python src/02_build_dataset.py
python src/03_analysis.py         # tables/figures written here, deterministically (one SEED)
( cd paper && latexmk -pdf main.tex )
echo "Rebuilt paper/main.pdf from raw. Compare to the committed PDF."
```

### The fixed, named SEED — `config.py`

```python
# config.py — one seed, imported everywhere randomness happens
SEED = 20260815  # the conference date; any fixed int, just FIXED and named

# in 03_analysis.py, at the top, before any draw:
import numpy as np
from config import SEED
rng = np.random.default_rng(SEED)   # modern Generator, NOT legacy np.random.seed
# the placebo reassignment and the wild-cluster bootstrap both draw from this rng,
# passed in explicitly so a reader sees exactly what randomness each step consumes.
```

Maya's analysis has two stochastic steps — the wild-cluster bootstrap on slide 5's standard errors and the placebo that reassigns fake adoption years — and **both** draw from this one `rng`. That is why her headline interval `[−2.8, −0.8]` comes out identical on a reviewer's machine; without the fixed seed it would drift run to run and the packet would, strictly, be irreproducible. The seed is recorded in the README and was fixed in the `pap-filed` commit (Ch 7.3), so it provably was not searched over for a prettier interval.

### Completed `REPLICATION-CHECKLIST.md`

**The deck**
- [x] 7 slides (1 title + 6 beats) in order (title · question · why · design · headline · robustness · contribution). → `paper/slides.pdf`
- [x] Every title is a full-sentence claim; argument legible from titles alone. → list atop `paper/slides-notes.md`
- [x] Design slide shows the identifying-assumption sentence (from `memo.md`), not the regression equation.
- [x] Headline slide: one number + CI, as the event-study **figure**, human-units sentence ("about a fifth of the baseline gap").
- [x] Robustness slide: spec curve + placebo panel clustering near −1.8, one stability sentence.
- [x] Contribution slide names what's new *and* the "we do not show loan terms / non-mortgage credit" non-claim.
- [x] Every slide figure is the file `03_analysis.py` wrote into `paper/figures/` — none hand-pasted. *(verified: `slides.pdf` `\includegraphics`es `figures/event_study.pdf`)*

**The talk**
- [x] Rehearsed timed ×4; longest run 7:10, fits in seven.
- [x] Cut line pre-decided (drop slide-5 placebo panel) — in `slides-notes.md`.
- [x] Two "what about [confound]?" answers + one located "I don't know" written out (above).
- [x] Fatal critique named (pre-existing denial-gap divergence); retreat position written (concede → descriptive association → RD as future work).

**The packet**
- [x] Six parts present: HMDA access script (public, ships cached) · `src/01–03` in run-order · README · `environment.yml`+`environment.lock.yml` · `config.py` SEED · `Makefile`+`run_all.sh`.
- [x] README states public HMDA / public FRED; **no licensed data, no secrets** in repo or history. → `git ls-files | grep -E '\.env|\.parquet|crsp' ` returns nothing.
- [x] SEED is one named constant via `np.random.default_rng(SEED)`, threaded through bootstrap + placebo, recorded in README.
- [x] Every `paper/` table and figure is code-generated and `\input`/`\includegraphics`'d — none pasted.
- [x] **`make clean && make all`** rebuilt `paper/main.pdf`; `git diff --stat` on the PDF and on `tables/`/`figures/` shows **no change** → no hand-edits. *(the honesty test, passed)*
- [x] Verified on a **fresh clone** in a scratch dir, not the working copy: `git clone … && conda env create -f environment.yml && conda activate capstone && make all` → identical PDF.

---

## INSTRUCTOR GRADING NOTES (keyed to the PS 8.5 rubric)

These notes show *why* this deliverable earns an A and where a weaker submission would lose points.

### Part 1 — The six-beat arc (35 pts) → **Excellent**

All six beats are present, in order, one per slide, and — the A-grade move — each slide does *its* one job and refuses the others. **(a) Question (5):** one sentence, no literature dump; the title *is* the question. **(b) Why (5):** a concrete stake with a scale number, placed *after* the question, not before — the single most common ordering error (opening abstract loses the room in thirty seconds) is avoided. **(c) Design (8 — the spine):** the slide shows the *identifying-assumption sentence* and a cohort-mean picture, **not the regression equation** — exactly right, because nobody reads a regression in sixty seconds; the spec is reduced to one plain-words strip. This is where weak decks collapse: a design slide that is a wall of $\beta$'s and fixed-effect notation cannot be read live, and the talk dies at the first hard question. **(d) Headline (6):** one number, *with its confidence interval*, as a figure, interpreted in human units ("a fifth of the baseline gap"). **(e) Robustness (6):** a spec curve that shows stability as a *shape*, plus a placebo — not a narrated list of twelve checks. **(f) Contribution (5):** the "what we do *not* claim" clause is present and load-bearing.
*Where points are lost on a typical submission:* a "Results" slide that is the paper's regression table screenshotted (unreadable from row eight — auto-deduction on Part 2b); a headline with a point estimate and no interval (reads as evasive); a design slide showing the equation instead of the assumption; motivation before the question. Each is scored down on the specific beat.

### Part 2 — One idea per slide + table-to-figure (20 pts) → **Excellent**

**(a) Title test (8):** every title is a full-sentence claim, and the argument is legible from the titles alone — the deliverable even prints the seven-title list so a grader can verify it in ten seconds. A deck with noun-phrase titles ("Background," "Results," "Robustness") loses this part wholesale, because the titles carry no argument. **(b) Translation (12):** the student names *which* translation each slide uses and *why* — the DiD result becomes an **event-study plot** (flat-then-jump, which argues parallel trends for free), the robustness becomes a **coefficient/spec plot** (stability as a tight cluster), and the precise table is demoted to a backup slide for the fourth-decimal questioner. The figures are stripped to load-bearing elements. Critically, the deliverable verifies the slide figure *is the file the code generated* — closing the loop with Part 4 so the slide and the packet cannot drift apart.
*Where points are lost:* showing the table on the main slide instead of translating it; a figure with unreadable ticks, dead legends, and gridlines; or — the silent failure that surfaces in Part 4 — a slide figure that was exported by hand and no longer matches what `make all` produces.

### Part 3 — Defending identification (15 pts) → **Excellent**

**(a) Two prepared confound answers (6):** the four-part structure (threat → plausible → what-I-did → residual) is followed exactly, drawn straight from the Ch 7.5 threats table — the student is reading from a script authored when calm, not improvising. The pre-trend answer concedes the worry is *central and plausible* before answering, which reads as more credible than a confident dismissal. **(b) Located "I don't know" (5):** the auto-loan answer is the chapter's gold standard — it admits the limit, explains *why* (different supervisor), and names what would resolve it (re-run there), rather than bluffing a number. **(c) Fatal vs. survivable + retreat (4):** the student correctly identifies that *attacks on the comparison are fatal* (a real pre-trend) while *attacks on a number are survivable* (clustering), maps this to Ch 7.5 §4's testable-vs-arguable, and — the mature move — writes the retreat to a descriptive claim *before* walking in.
*Where points are lost:* answering a confound question by dismissing it ("we control for that"); bluffing the "I don't know"; or misclassifying a fatal critique as survivable and trying to re-cluster their way out of a broken comparison in front of a room that can see it is broken.

### Part 4 — The one-click packet (30 pts) → **Excellent**

All six parts present and each *verified*, not merely asserted. **(a) Data (5):** correctly ships public HMDA cached with a pinned vintage and states the public/licensed split honestly. **(b) Run-order (5):** `01→02→03` numbering makes the order unambiguous; logic in `src/`, story in `notebooks/`. **(c) README (4):** the how-to-run has collapsed to one command. **(d) Env (4):** both `environment.yml` and `environment.lock.yml` committed; the student can say the "rebuild that and you rebuild my numbers" sentence. **(e) SEED (5):** a single named `SEED` in `config.py`, threaded through *both* stochastic steps (bootstrap and placebo) via `np.random.default_rng`, recorded in the README, fixed in the `pap-filed` commit so it provably was not searched over. **(f) Entry point (7):** a `Makefile` *and* a `run_all.sh`, with the figures/tables **generated by `03_analysis.py`** and `\input`/`\includegraphics`'d — never pasted.
The decisive A-grade evidence is the **honesty test, run and recorded**: `make clean && make all` rebuilt the PDF byte-identical, *and* the student re-verified on a **fresh clone** in a scratch directory — the true stranger's-machine test, not the working copy where stale derived files hide hand-edits.
*Where points are lost:* the single most common — and most penalized — failure is a number on a slide that the rebuild does not reproduce, because it was hand-copied from a notebook into the manuscript and has since drifted from the code. That breaks the one-click chain and fails the part regardless of how polished the deck is. Also penalized: a seed scattered ad-hoc (or the legacy `np.random.seed`), a missing lock file ("it worked on my machine"), or licensed data / a `.env` committed to history (a Lab 7 Step-5 violation that is serious independent of the grade).

### One-line grading heuristic

The two highest-signal questions for any PS 8.5 submission: **(1)** Can a reader reconstruct the entire argument from the slide *titles* alone, with the design slide showing the *assumption* (not the equation) and the headline showing a number *with its interval as a figure*? **(2)** Does **`make clean && make all`, on a fresh clone**, regenerate the exact number the headline slide claims? A student who clears both has internalized the camp's thesis — *reproducibility is the form credibility takes* — because the talk *invites* verification ("here's the command that checks me") instead of asking to be believed, and the packet makes good on the invitation. This exemplar clears both cleanly, which is what an A looks like.

---

*End of model deliverable for PS 8.5. The exemplar is Maya's HMDA fair-lending DiD — the project she carried from Lab 4 through the Week-7 PAP, identification memo (Ch 7.5), and robustness battery (Ch 8.2) into this final talk and packet. All magnitudes (the ≈ −1.8 pp ATT, the [−2.8, −0.8] interval, the ~9-point baseline gap, the "fifth of the gap") are **illustrative**, presented as a worked talk example, not a claimed estimate; the real numbers come out of `make all` on the pinned, public CFPB HMDA vintage recorded in `data-cards/hmda.md`. The packet standard is Appendix D + Lab 7; the staggered-DiD machinery is Callaway & Sant'Anna (2021) and Goodman-Bacon (2021), as built in Ch 4.2 and Lab 4; the SEED/`make`/one-command discipline is Ch 8.5 §5 and Gentzkow & Shapiro (2014). No secrets or keys appear; the `SEED = 20260815` constant and `config.py` pattern are illustrative.*
