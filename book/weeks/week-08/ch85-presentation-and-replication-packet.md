# Ch 8.5 — The 8-Minute Poster Talk & the Replication Packet

This is the last chapter of the camp, and it is about the two things that happen *after* the work
is done: you stand beside your research poster and defend it for eight minutes at the **ASSIP
Research Symposium on Wednesday, August 12, 2026** (in-person at the GMU College of Science venue
for on-campus interns; on the symposium's virtual-breakout track for remote interns, including
Prof. Gao's 2026 group), and you hand someone — via a QR code on the poster — a folder that lets
them rebuild every number you just claimed. Both are acts of credibility, and they fail in the
same way: not because the analysis was wrong, but because you could not make a skeptic believe it.
A correct result that nobody can follow on a poster panel, or that nobody can reproduce on their
own machine, is, to the person walking the symposium floor, indistinguishable from a guess. So
this chapter teaches the two crafts that turn a defensible analysis into a *believed* one: the
discipline of a short talk-beside-a-poster, and the discipline of a one-click replication packet.
They are the same discipline, really — strip away everything that is not load-bearing, and make
what remains impossible to doubt.

The poster is the visual artifact ASSIP grades, and the abstract printed on its title block is the
artifact JSSR (Journal of Student-Scientists' Research, GMU Mason Publishing) publishes. This
chapter uses "slide" and "panel" almost interchangeably, because the six-beat arc below maps one
beat to one slide *and* one beat to one poster panel — you build the six panels of the poster, you
walk a visitor through them in six beats, and any companion slides you use on the virtual-breakout
track follow the same arc. The translation from the longer chapter-8.3 manuscript prose to a
two-line panel happens here.

Here is the move the whole chapter turns on, so you have it before the details. **Reproducibility
is not a virtue you add at the end; it is the form your credibility takes.** When you say "the
effect is 1.8 percentage points," the audience cannot check that from your face. What they *can*
check is your poster's design panel (does the design support that number?), your answer to their
hardest question (do you know where your own design is weak?), and — afterward, alone, on their
phone after scanning your QR code — your packet (does `make all` actually regenerate that 1.8?).
The talk and the packet are the two surfaces a skeptic touches. Everything you built across Weeks
1 through 7 — the estimator, the pre-analysis plan, the identification memo, the pinned repo —
exists so that those two surfaces hold up under pressure. This chapter is where you make them
hold.

---

## 1. Slide / poster-panel discipline: the eight-minute arc

Eight minutes is not a short version of a long talk. It is a different object, with its own
shape, and the most common failure is to treat it as a forty-minute seminar with the boring parts
deleted. It is not. An eight-minute talk has room for exactly one idea, defended cleanly, and the
slides — or, for ASSIP, the six panels of your poster — exist to keep you and the audience on that
one idea. At the Aug 12 symposium, and at every short talk you will give for the rest of your
life, the constraint is the same: you have time to make *one* argument land. The arc below is that
argument, broken into the six beats it has to hit, with **one beat per poster panel** (plus a
title block holding the JSSR-ready abstract).

**Question → why it matters → design/identification → headline result → robustness → contribution.** Memorize that sequence; it is the skeleton of every empirical talk worth listening to. Each beat is one slide. Spend roughly **one minute per slide**, which leaves you two minutes of slack — and you will need every second of it, because talks run long, not short. Let us walk the arc, because the proportions are the lesson.

The **question** slide / panel states, in one sentence a smart sixteen-year-old could repeat back,
what you are asking. Not the literature, not the motivation — the question. Devon's reads: *"Does the launch of a spot Bitcoin ETF reduce the volatility of the underlying token?"* That is a slide. The temptation is to open with three paragraphs of crypto-market history; resist it. The room cannot hold context it has not yet been given a reason to want. State the question; the reason to care comes next.

The **why it matters** slide earns the question its airtime — and this is where you spend it, *after* the question, not before. One concrete stake. Priya's climate-insurance talk does not open with the IPCC; it opens with: *"If wildfire risk is mispriced, insurers either go insolvent or abandon whole counties — and someone has shown neither happens cleanly."* That is a stake a stranger feels. The discipline here is the same one CONVENTIONS §1 drills in the prose: *concrete before abstract, a number before a Greek letter.* A talk that opens abstract loses the room in the first thirty seconds and never gets it back.

The **design/identification** slide is the spine, and it is the one students underweight. This is where you put your identifying-assumption sentence from Chapter 7.5 — the contract — on the screen, in the same form: *"Our estimate is credible as long as [the assumption], which we defend by [the design]."* This is not a slide about your regression equation; nobody can read a regression equation in sixty seconds. It is a slide about *why the comparison is fair*. Sam's momentum talk does not show the Fama–MacBeth machinery; it shows one sentence — *"long past-winners, short past-losers, within each month, so common shocks cancel"* — and one small picture of the sort. If the audience leaves understanding only one thing, it should be this slide. A talk where the design slide is weakest is a talk that will not survive questions, because every hard question lands here.

The **headline result** slide is *one* number with its uncertainty, shown as a picture (we come back to how, in §2). Not a table. One estimate, one interval, one sentence of interpretation in the units a human cares about — "1.8 percentage points, about a fifth of the baseline gap," not "$\hat\beta = 0.018$, $t = 3.2$." If you remember nothing else about result slides: **a confidence interval is part of the result, not an afterthought** — show it, because a point estimate with no interval reads as either naïve or evasive, and a sharp audience clocks the difference instantly.

The **robustness** slide is where Chapter 8.2 pays off, and it has exactly one job: show that the headline did not depend on a single arbitrary choice. This is the visual answer to "is your result fragile?" — typically a **specification curve** or a small grid of alternative specifications, all clustering near the headline. You do not narrate every robustness check; you show that they exist and that they agree, and you say one sentence: *"the result is stable across [the three choices I worried about most]."* This slide is your pre-emptive strike against the questions in §3 — it answers "what about that choice?" before anyone asks.

The **contribution** slide closes by naming what the room now knows that it did not eight minutes ago — *one* sentence — and, crucially, what you are *not* claiming. "We show X, under assumption Y; we do not show Z." That last clause is not weakness; it is the single most credibility-building sentence in the talk, because it signals you know exactly where your own claim stops. Then stop talking. Do not summarize the summary.

---

## 2. One idea per slide, and the table-to-figure translation

Two rules govern what goes *on* each slide, and both are about respecting the fact that a live audience reads with their ears, not their eyes.

**One idea per slide.** A slide is a single claim with a single piece of evidence for it. The instant a slide has two ideas, the audience has to choose which one to follow while you talk, and they will choose wrong, and you will lose them. The test is brutal and useful: if you cannot write the slide's one idea as the *title* — a full sentence, not a noun phrase — the slide is doing too much. "Results" is not a title; "The denial gap falls 1.8 points after the regulation, and the fall is concentrated in algorithmic lenders" is a title, because it *is* the idea, and a reader who only reads your titles should still get the argument. Split anything that resists this. Six clean slides beat four crowded ones every time, because the crowded four cost you the room.

**The table-to-figure translation.** Here is the reveal that separates a paper from a talk. In your paper, your results live in a regression table — the four-decimal, five-column, standard-errors-in-parentheses object that Appendix D specifies down to the typography. That table is *correct* and it is *unreadable from row eight of a lecture hall in four seconds.* A live audience cannot scan a 5×7 grid of numbers while you speak; by the time they have found the coefficient you are talking about, you are three sentences past it. So you do not show the table. **You translate it into a figure.** The translation is mechanical, and learning it is one of the highest-leverage skills in this chapter:

- A **single coefficient with its confidence interval** becomes a **point with an error bar.** One estimate, one whisker. The eye reads "is it different from zero?" and "how precise?" instantly — the two questions the table makes you compute by hand.
- **A coefficient across several specifications** (the columns of your robustness table) becomes a **coefficient plot**: one dot-and-whisker per specification, lined up, with a reference line at zero or at the headline. The audience sees stability as a *shape* — a tight vertical cluster — not as seven numbers they must compare mentally.
- **A difference-in-differences or event study** becomes an **event-study plot**: estimated effects by period, flat before treatment, jumping after. This single picture *is* the parallel-trends defense from Chapter 7.5 — the flat pre-period leads are visible, so the slide argues your identification for you.
- **A regression discontinuity** becomes the **binned scatter with the fitted jump at the cutoff.** The discontinuity is a thing you can *see*; no table conveys it as fast.
- **A subgroup pattern** (the gap is bigger here than there) becomes a **small-multiples bar chart**, not a table with an interaction term the audience has to mentally exponentiate.

The principle under all of these: **a table is for a reader who can stop and study; a figure is for a listener who cannot.** Translate every result you will *say out loud* into a picture, and leave the precise table in the paper and the backup slides for the questioner who wants the fourth decimal. Same number, two encodings, chosen for the medium. This is not dumbing down — Devon's ETF-volatility result is exactly as precise on the error-bar slide as in the table; it is just *legible at the speed of speech.* And one mercy rule for the figures themselves: a slide figure needs axis labels a person can read from the back of the room and no more than is load-bearing — strip the gridlines, the legend nobody reads, the third decimal on the tick marks. The figure has one job, which is to make one comparison obvious.

---

## 3. Time budgeting, and the rehearsal that proves it

A budget you have not tested is a wish. The single most reliable predictor of a talk going over time is that the speaker never once said it out loud against a clock. So the rule is concrete: **rehearse the full talk, timed, at least three times, and cut until it fits in seven minutes, not eight.** You target seven because a live talk runs longer than a rehearsal — you will pause, someone will cough, the clicker will lag — and because the eighth minute is your insurance against disaster, not your content. A talk that *needs* all eight minutes in rehearsal will run to ten on stage, and a talk that runs to ten in an eight-minute slot gets cut off mid-sentence at the result, which is the worst possible place to be cut off.

Where does the time go? Roughly: a minute on question-and-why (combined, fast — get to the substance), a minute and a half on the design slide (slow down here; this is the spine and the room needs it), a minute and a half on the headline (let the number land, then say what it means), a minute on robustness, a minute on contribution, and the rest as the slack you will spend recovering from the things that go wrong. Notice the shape: you go *fast* through motivation and *slow* through identification and result, which is the opposite of what nervous speakers do — they race through the hard middle to get to the safe summary. Resist it. The middle is the talk.

A discipline worth stealing from professional speakers: **know your cut line in advance.** Decide, before you stand up, which slide you will skip if you are at minute six and only on the result. Almost always it is the second robustness detail or the third motivation point — never the design slide, never the headline. When you are over time and improvising, you cut badly; when you have pre-decided the cut, you cut cleanly and nobody notices. The rehearsal is also where you discover the sentences you cannot say smoothly — the ones with three clauses and a parenthetical — and rewrite them, because a sentence you stumble on in rehearsal is a sentence you will fail on stage. nb8.5 and Lab 8 include a dry-run timer for exactly this; use it until the talk fits with room to spare.

---

## 4. Defending identification under questions

The talk is eight minutes; the questions are where the talk is actually judged. A polished eight minutes followed by a flailing answer to the first question undoes the polish entirely, because the question period is where the audience finds out whether *you* believe your result or merely recited it. The good news — and it is genuinely good news — is that you already did the work. **The questions you will get are the rows of your threats-and-responses table from Chapter 7.5.** You wrote them down weeks ago. You are not improvising; you are reading from a script you authored, in private, when you were calm.

**Anticipate the "what about [confound]?" questions.** Every hard question in an empirical seminar has the same shape: *"Isn't your estimate just picking up [some confounder] rather than the effect you claim?"* That is your identifying assumption being attacked at its named weak point — and you named every one of those weak points yourself, in column 1 of the threats table. So before the talk, take your threats table and turn each row into a prepared answer: the threat (their question), why it's plausible (so you don't dismiss it), what you did about it (column 3 — the test or design choice), and the residual concern (column 4 — what honestly remains). When the question comes, you answer in that order: *"Yes, that's the central worry — if [confounder] were driving this, we'd see [signature]; we checked, and we see [reassuring result]; what I still can't fully rule out is [residual], though [bound on how bad it could be]."* That answer makes you look *more* credible than a confident dismissal would, because it shows you saw the problem before they did. The person asking wanted to know if you'd thought about it; you show them you'd thought about it harder than they had.

**How to answer "I don't know" honestly — and well.** You will get a question you cannot answer. Everyone does; a referee's whole job is to find the question you didn't prepare. The amateur move is to bluff — to manufacture an answer on the spot — and a room full of people who do this for a living can smell a bluff instantly, and the bluff costs you far more credibility than the gap ever would. The professional move is to say "I don't know" *with structure*. Not a bare shrug: a located one. "I don't know — that's outside what my design can speak to, because [reason]; my guess is [direction], but I'd want to [the specific thing you'd check] before claiming it." That sentence does three things: it admits the limit, it shows you understand *why* it's a limit, and it names what would resolve it. An honest, located "I don't know" is one of the most credibility-building things you can say, because it proves the rest of your "I know"s are trustworthy — a person who will admit ignorance here is a person whose confidence elsewhere you can believe. Maya, asked whether her fair-lending effect would generalize to auto loans, does not invent a number; she says: "My data is mortgages, so I genuinely don't know — the mechanism I identify is examiner attention, and I'd expect it to matter wherever there's a comparable exam regime, but auto lending has a different supervisor, so I wouldn't extend the estimate without re-running it there." That is a *better* answer than a confident yes.

**The difference between a fatal and a survivable critique — and how to tell, live.** This is the distinction that lets you keep your composure when a question lands hard, so internalize it now. **A survivable critique attacks a number; a fatal critique attacks the comparison.** If someone says "your standard errors should be clustered differently" or "you should winsorize at 1% not 5%" or "did you control for firm size?" — those are survivable, because they ask whether a *choice* changes the answer, and you can say "we checked; it doesn't" (you did, on the robustness slide) or "fair, let me re-run it and report back." The result might move a little; it does not vanish. But if someone says "your treated and control groups were already diverging before treatment" or "your instrument plausibly affects the outcome directly" or "the same cutoff also switches eligibility for a different program" — those attack the *identifying assumption itself*, and if the attacker is right, no amount of re-clustering saves you, because the comparison was never clean. Those are the fatal ones, and you know exactly which they are, because they are the *testable-vs-arguable* threats from Chapter 7.5 §4 — the ones you can only argue, not test, are precisely the ones that are fatal if lost.

Here is what to do when a fatal critique lands and the attacker is *right*: do not defend the indefensible. The instinct under pressure is to argue harder, and it is exactly wrong — defending a broken identification in front of a room that can see it is broken converts a damaged paper into a damaged reputation. The move is to concede the point at the level it was made and retreat to what survives: "You're right that I can't rule that out with this design — so the honest reading is that this is a strong *association* consistent with the mechanism, not the clean causal estimate I'd hoped for, and that's a real limitation." A conceded fatal critique is a wounded paper but an intact scientist; a bluffed one is neither. And often the critique is fatal *to the causal claim* but not to the *descriptive* one — you can almost always retreat to "this is a robust pattern that future work with [the better design] should test causally," which is a real, publishable, honest contribution. Know your retreat position before you walk in. That is what the residual-concern column was *for*.

---

## 5. The one-click replication packet

Now the second surface, the one the skeptic touches alone. After the talk, the most serious members of your audience do not take your word for anything — they ask for the packet and try to rebuild your headline number on their own machine. The packet is the standard from **Appendix D** and **Lab 7**, and the bar is exact and unforgiving: **a stranger, on a machine that has never seen your project, runs one command and watches every table and figure in your paper regenerate from raw data to final PDF.** Not "mostly." Not "after I email them a fix." One command, everything, byte-for-byte. That is the difference between a result and an assertion, and it is the entire reason Lab 7 made you stand up the repository in Week 7: the packet is not a new thing you build now, it is the repository you have been committing into all along, finished.

The packet has six load-bearing parts. You built most of them in Lab 7; here they assemble into the deliverable.

**1. The data — or a data-access script.** Public data ships *in* the packet (cached, with its vintage pinned). Licensed data — CRSP, Compustat, anything from WRDS — does *not* ship, because the license forbids redistribution (Lab 7, Step 5, and CONVENTIONS §5); it stays on GMU infrastructure. What ships instead is the **data-access script** in `src/` — the bounded, pinned query that *reconstructs* the licensed data for anyone with the same WRDS access — plus the `logs/pulls.jsonl` log with content hashes, so a reviewer with access can re-pull and verify they got identical bytes. This is the *asymmetry of reproducibility* from Lab 7: public data is fully re-runnable, licensed data is recipe-reproducible. Your README states honestly which is which.

**2. Code in run-order.** The scripts in `src/` and the notebooks in `notebooks/`, named or numbered so the *order* is unambiguous — `01_pull.py`, `02_build.py`, `03_analysis.py`, or whatever ordering your `run_all` enforces. The rule from Lab 7 holds: *logic in `src/`, story in `notebooks/`*. A reviewer should never have to guess which script runs first.

**3. A README.** The *what / why / how-to-run* document from Lab 7, Step 4 — but now the "how to run" section has collapsed to almost nothing, because the whole point of the packet is that the answer is *one command*. The README still names the data sources, the secrets a user must `export`, and the licensed-vs-public split — but the run instructions are now a single line.

**4. A pinned environment file.** Both files from Lab 7, Step 3: the human-readable `environment.yml` (Python 3.11 + the CONVENTIONS §5 stack) and the machine-exact `environment.lock.yml` (every package at the version the solver chose). This is the answer to "it worked on my machine" — your machine and the reviewer's machine become the *same* machine. The sentence you must be able to say out loud: *"my results were produced under `environment.lock.yml`; rebuild that and you rebuild my numbers."*

**5. A fixed random SEED.** This is the part Lab 7 set up and this chapter makes non-negotiable. Anywhere your code uses randomness — a bootstrap, a train/test split, a permutation test, a synthetic-control placebo, a simulation — it must be seeded from a *single, named constant* set once at the top of the run, not scattered ad-hoc. Without a fixed seed, your bootstrap confidence interval is *different every run*, which means your headline interval is, strictly, irreproducible — a reviewer runs your code and gets `[1.2, 2.4]` where your paper said `[1.3, 2.3]`, and now they doubt everything, fairly. With a fixed seed, the random parts come out *identical*, every time, on every machine:

```python
# config.py — one seed, imported everywhere randomness happens
SEED = 20260815  # the conference date; any fixed int, just FIXED and named

# at the top of every script/notebook that uses randomness:
import numpy as np
from config import SEED
rng = np.random.default_rng(SEED)        # modern NumPy: a seeded Generator, not legacy np.random.seed
# ...every draw goes through rng: rng.choice(...), rng.permutation(...), bootstrap resamples, etc.
```

The discipline is *one* seed, set *once*, threaded through *every* stochastic step — and recorded in the README so a reviewer knows the number was fixed before results, not tuned after. (A seed you *searched over* to get a prettier interval is p-hacking with extra steps, Chapter 7.3's garden of forking paths wearing a disguise; the `pap-filed` tag is what proves you didn't.) Pass `rng` into your functions rather than reaching for the global, so the seeding is explicit and a reader can see exactly what randomness each step consumes.

**6. A single `make` / `run_all` entry point.** This is the one-click. A single command that runs the whole pipeline *in order* — pull (or load cached), build the dataset, run every estimation, regenerate every figure and table, and compile the paper to PDF — so that a fresh clone goes from raw inputs to finished document with no human in the loop. Two equivalent shapes, pick one:

```makefile
# Makefile — `make all` regenerates EVERYTHING from raw to paper.pdf
.PHONY: all data analysis paper clean

all: paper

data:                       ## pull/load + build the analysis dataset
	python src/01_pull_data.py
	python src/02_build_dataset.py

analysis: data              ## estimate; write tables/ and figures/ (deterministic via SEED)
	python src/03_analysis.py

paper: analysis             ## compile the write-up, pulling in the just-built tables/figures
	cd paper && latexmk -pdf main.tex

clean:                      ## delete all derived outputs so a rebuild is honest
	rm -rf data/processed/* paper/tables/* paper/figures/* paper/main.pdf
```

```bash
# run_all.sh — same idea, no make required: `bash run_all.sh`
set -euo pipefail                 # stop on the first error; never silently half-build
python src/01_pull_data.py
python src/02_build_dataset.py
python src/03_analysis.py         # tables/figures are written here, deterministically
( cd paper && latexmk -pdf main.tex )
echo "Rebuilt paper/main.pdf from raw. Compare to the committed PDF."
```

The non-negotiable property: **the figures and tables in your paper are *generated by the code*, never pasted by hand.** `03_analysis.py` writes `paper/figures/event_study.pdf` and `paper/tables/main_results.tex`, and the LaTeX `\includegraphics`/`\input`s them. The instant a human copies a number from a notebook into the manuscript, the chain breaks and the packet is no longer one-click — and worse, the pasted number can silently drift out of sync with the code that supposedly produced it. The whole pipeline must be *machine-traversable* from raw bytes to the PDF on the screen. The honesty test is `make clean && make all`: delete every derived file and rebuild from nothing. If the paper comes back identical, the packet is real. If it doesn't, you just found a hand-edit, and you found it before a reviewer did.

---

## 6. Reproducibility *is* the credibility

It is worth stating the thesis of this whole chapter as bluntly as it deserves, because it is the habit the entire camp was built to install. **A result a stranger cannot reconstruct is not yet a result — it is a claim about a result.** The reviewer who clones your repo, types `make all`, and watches your 1.8-percentage-point estimate emerge from raw HMDA data through your seeded code into a compiled PDF has *checked your work in a way no amount of eloquence on a slide could substitute for.* That is why the packet is not paperwork bolted on at the end; it is the literal form your credibility takes once you stop talking and the skeptic is alone with your folder.

This connects the two halves of the chapter. In the question period (§4), the most powerful thing you can say to a hostile question about a number is: *"the exact code that produces that number is in the packet — clone it and you'll get the same figure, seed and all."* You are not asking to be believed; you are inviting verification, which is the opposite posture, and it is the posture of someone with nothing to hide. A talk that ends with "trust me" and a talk that ends with "here's the one command that checks me" are received completely differently by a serious audience, and the difference is the entire game. The packet lets you be the second kind of speaker. The seam should be visible by design — the same logic as Chapter 7.3's `pap-filed` tag: a referee trusts you *more* when the work is open to inspection, not less, because the openness is itself evidence that you believe what you found.

---

## 7. From "the average return was 8%" to a defensible, reproducible paper

Look back at where Week 1 started. The first thing you did in this camp was compute an average: you pulled a series of returns and found that the mean was about eight percent a year, and that felt like an answer. It was not an answer; it was the *first* question. Because immediately you learned to ask: eight percent compared to *what* — and the arithmetic-versus-geometric distinction taught you that even "the average" hides a choice. You learned that the eight percent had a standard error, that the standard error depended on assumptions you could not see, that the sample was survivorship-filtered, that the sign of a "significant" coefficient could be an artifact of how many specifications you quietly tried.

Trace the arc the eight weeks actually walked. Week 1 turned a number into a number-with-uncertainty. Week 2 turned correlation into the machinery of regression and taught you that "we control for X" is a *claim*, not a spell — the ghost of omitted-variable bias. Weeks 3 and 4 turned that claim into *designs* — IV, RD, difference-in-differences, synthetic control — each one a specific argument for why a particular comparison is fair, each with its own named way of failing. Week 5 taught you to read other people's papers as a skeptic, which is the same skill as reading your own honestly. Week 6 sharpened the inference — the right standard errors, the multiple-testing correction, the bootstrap. And Week 7 made it *yours*: an idea worth pursuing, data pulled reproducibly, a pre-analysis plan tagged before you could fool yourself, an analysis dataset built without look-ahead, and an identification memo that named every threat out loud. Week 8 took that and made it *communicable and checkable* — written up with calibrated verbs, robustness that survived (Ch 8.2), peer-reviewed, and now, today, defended in eight minutes and packaged so a stranger can rebuild every claim.

What you have at the end is not "the average return was 8%." It is a question nobody had cleanly answered, attacked with a design you can defend sentence by sentence, estimated with honest uncertainty, robust to the choices you worried about, written so a referee believes it, and packaged so a skeptic can reproduce it with one command. That is an original empirical paper. That is what a researcher does. The eight percent was the toe in the water; this is the swim. The single sentence that separates the two — and the one this whole camp existed to let you say truthfully — is: *"Here is what I found, here is exactly why you should believe it, and here is the command that lets you check me."* You can say it now. Go say it.

---

## Your Turn

Two deliverables close the camp, and they are the same project seen from its two surfaces.

- **nb8.5 — the final manuscript build.** This is where your Markdown/LaTeX write-up becomes a compiled PDF: tables and figures generated by your code (never pasted), `\input` and `\includegraphics`'d into the manuscript, built by the same `run_all` entry point that produces your results. Run `make clean && make all` and confirm the PDF rebuilds from nothing. If a number drifts, you have a hand-edit to hunt down — find it now.
- **Lab 8 — the final compile, repo, and dry-run.** Assemble the six-part replication packet on top of the Lab 7 repository; verify `make all` regenerates every table and figure from raw to PDF on a *fresh clone*; confirm the SEED is fixed and named; and rehearse the eight-minute talk against the timer until it fits in seven, with your cut line pre-decided and your threats-table answers prepared. The "you're done when…" checklist is the audit a referee — or Prof. Gao, at the conference — would run.

Then look at the **capstone gallery** in `book/capstones/`: five finished student papers, each with its talk and its one-click packet, as exemplars of the bar you are clearing. Read one not for its result but for its *seams* — find its identification slide, find the residual-concern its threats table admits, and run its `make all`. That is how you will read every empirical paper from now on, and how you will want yours read.

### A closing reflection

Pick the single hardest question you expect in your question period — the one that, if the attacker is right, is *fatal* and not merely survivable. Write the prepared answer in full: the threat, why it's plausible, what you did, the residual concern, and — if it is genuinely fatal — your retreat position to the claim that survives. Then ask yourself the question this whole camp was pointed at: *if a stranger clones my repo and types one command, do they get the number I just defended?* If the answer is yes, you are done. If it is "almost," you are not done — and now you know exactly what "done" means.

---

### References

- Christensen, G., & Miguel, E. (2018). Transparency, Reproducibility, and the Credibility of Economics Research. *Journal of Economic Literature*, 56(3), 920–980.
- Wilson, G., Bryan, J., Cranston, K., Kitzes, J., Nederbragt, L., & Teal, T. K. (2017). Good Enough Practices in Scientific Computing. *PLoS Computational Biology*, 13(6), e1005510.
- Gentzkow, M., & Shapiro, J. M. (2014). *Code and Data for the Social Sciences: A Practitioner's Guide.* University of Chicago. (Run-order, `make`, and one-command-rebuild discipline.)
- Olken, B. A. (2015). Promises and Perils of Pre-Analysis Plans. *Journal of Economic Perspectives*, 29(3), 61–80. (Pre-registration; the `pap-filed` tag of Lab 7.)
- See also CONVENTIONS §5 (code & reproducibility stack), Appendix D (style guide & packet standard), and Lab 7 (the repository this packet finishes).
