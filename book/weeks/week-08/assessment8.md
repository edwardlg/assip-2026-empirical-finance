# Week 8 Assessment — The Capstone (Terminal Assessment of ASSIP)

This is the last thing you will be graded on, and it is the only thing the eight weeks of ASSIP
were ever building toward. Weeks 1 through 4 handed you a toolkit; Weeks 5 and 6 taught you to read
an estimator in a stranger's hands and to build a measurement honestly; Week 7 made you design a
falsifiable question of your own and file the pre-analysis plan and identification memo that froze
it before the data could flatter you. Week 8 is where that frozen plan becomes the **ASSIP terminal
deliverable**: a research poster a roomful of GMU faculty, mentors, families, and visiting College
of Science leadership cannot ambush at the Aug 12 symposium; a JSSR abstract that survives the peer
review of GMU Mason Publishing's *Journal of Student-Scientists' Research*; and a replication
packet a stranger can rebuild with one command. The Week-7 assessment graded the design half and
told you, in plain words, that its rubric *is* the rubric your capstone meets. This assessment is
that promise come due. It extends the Week-7 research-design rubric to the full project: not just
"is the plan one a referee could not ambush?" but "did you execute it honestly, stress-test it
until it nearly died, distill it onto a poster so a stranger walking the floor believes it in
ninety seconds, write a 200–300-word abstract a JSSR editor would accept, and ship a packet a
stranger can check?"

**Total: 200 points** across four deliverables and seven rubric rows. The standard is the one this
whole book has pressed since Chapter 1.5: *a modest result you have stress-tested honestly outscores
an ambitious one you cannot defend.* A capstone that writes, unprompted, "my Oster $\hat\delta$ is
0.4, so an unobservable weaker than my controls could explain the result, and I report it as a robust
association, not a causal effect" earns more than one that claims a clean causal effect from the same
data. Hold yourself to CONVENTIONS §4 (every spec named in seven-slot form) and §5 (the repo runs on
a fresh env, the environment is pinned, licensed data stays on GMU infrastructure, no secret ever
appears in code) throughout — those are not extra credit, they are the floor.

**The ASSIP deliverable model, in one paragraph.** ASSIP 2026 (Aspiring Scientists Summer
Internship Program; George Mason University, College of Science; director Dr. Amanda Haymond Still;
contact `cosassip@gmu.edu`) asks for a **research poster** at the in-person/virtual Aug 12
symposium, an **abstract published in JSSR** (Journal of Student-Scientists' Research, GMU Mason
Publishing), an *optional* full paper for students who want to push the work further, and
participation in the program's scientific-writing and career-forum sessions. The rubric below
weights the four graded artifacts — the JSSR abstract, the poster, the 8-minute poster talk, and
the replication packet — so that a clean, honest poster on a stress-tested result outscores an
ambitious paper-style overclaim. The graded deliverable is the **poster + abstract + talk +
packet**, not a full manuscript; the full-paper option is mentioned in Lab 8 for students who
choose to write one.

Before you start, read one finished example in the **capstone gallery** (`book/capstones/`): five
complete exemplar papers, each paired with the talk it underpins and the one-click packet that
proves it — Fair Lending on HMDA, Common Ownership from 13F, Innovation from USPTO, SEC 8-K Text
Classification, and a FRED macro event study. Each exemplar paper carries a top-of-document note
that explains the framing: *the ASSIP terminal deliverable is a poster + JSSR abstract, not a full
paper, and the exemplar is the **full research narrative** the poster's six panels and the
abstract's 250 words distill from.* Read one not for its result but for its *seams*: find its
identification section, find the residual concern its threats table admits, and run its `make all`.
That is the bar you are distilling onto your poster.

---

## How you submit

The four deliverables below are *one* thing seen from four sides: the **abstract** is the
single-paragraph argument JSSR will publish; the **poster** is the visual argument the symposium
audience walks up to; the **talk** is the eight-minute defense you give standing beside it; and the
**packet + disclosure** is the proof a stranger can rebuild every number. You submit them together
as the single Git repository you have been committing into since Lab 7 — the `pap-filed` tag still
in its history, the confirmatory commit dated after it, `DEVIATIONS.md` filled in, the compiled
`paper/poster.pdf` and the slide deck both regenerable by the same `run_all` that produces your
results, and the JSSR-ready `paper/abstract.tex` generated from a single Python call so its 250
words cannot drift from the analysis they summarize. There is no separate "final upload": the
repository *is* the submission, and the first thing a grader does is clone it and type one command.
Everything else — the rubric below, the question period at the Aug 12 symposium — is downstream of
whether that command works. Treat the week as the assembly job it is, not as four new things to
build: every piece already exists from Weeks 7 and 8; the capstone is the act of making them hold
together under a stranger's hands and on a 48"×36" board.

## The four deliverables

### D1 — The JSSR abstract (200–300 words, GMU Mason Publishing format)

The single most-read paragraph of your entire ASSIP, and the one that lives permanently in the
*Journal of Student-Scientists' Research* index whether or not you submit a full paper. Written in
the fixed shape Ch 8.3 §2 trains for an introduction, compressed: **(a)** one sentence of motivation
naming a concrete stake (the hook), **(b)** one sentence stating the question, **(c)** one sentence
naming the data and design — including the identifying assumption verb (causal vs. associated) —
**(d)** the headline number with its uncertainty in human units (e.g., "1.8 percentage points,
about a fifth of the pre-period gap, 95% CI $[-2.5, -1.1]$"), **(e)** one sentence on the strongest
robustness result, and **(f)** one sentence on what you are *not* claiming. 200–300 words inclusive.
Generated by code, never typed — `nb8.5` writes `paper/abstract.tex` from the frozen analysis
variables (the same source as the poster's headline panel), so the abstract and the poster cannot
silently disagree. The verb is calibrated to your weakest assumption per Ch 8.3 §7; overclaiming
here is the most expensive sentence you write in ASSIP, because JSSR's audience sees this paragraph
forever and almost no one will read past it.

### D2 — The research poster (PDF, ~48"×36" landscape, GMU College of Science template)

The visual argument a stranger walks up to at the Aug 12 symposium and decides — in the eight
seconds before they decide whether to stay — whether to ask you a question. Built on the **GMU
College of Science academic-poster template** if one is distributed (search the ASSIP and College of
Science sites; if no template is available the camp distributes a defensible landscape default;
`[CHECK]` — confirm the current template URL with `cosassip@gmu.edu`), and arranged in the
**six-panel reading order that mirrors Ch 8.5's six-beat talk arc**:

1. **Title block** — your name, ASSIP 2026, Prof. Lei Gao (mentor), the **JSSR-ready 200–300-word
   abstract** as a left-column block (the same `\input{abstract.tex}` the JSSR submission carries).
2. **Question + why it matters** — one sentence each, large, top-left; concrete stake before any
   abstraction (CONVENTIONS §1).
3. **Data + design / identification** — the seven-slot specification (CONVENTIONS §4) in compact
   form, and the identifying-assumption sentence on screen as the *contract* form: *"our estimate
   is credible as long as [the assumption], which we defend by [the design]."* This is the spine
   panel; if a passerby reads only this panel, they should still understand why the comparison is
   fair.
4. **Headline result** — *one* number with its confidence interval, shown as a **figure** (point
   with error bar, coefficient plot, event-study plot, or RD scatter — the Ch 8.5 §2
   table-to-figure translation), with one sentence of interpretation in human units. Never a table
   here; this panel must read in three seconds.
5. **Robustness** — the specification curve from Ch 8.1 or a small coefficient grid from Ch 8.2,
   clustering near the headline, with one sentence: *"stable across [the three choices I worried
   about most]."*
6. **Contribution + limits + the rebuild command** — one sentence on what is now known that was not,
   one clause on what you are *not* claiming, and the **one-line `make all` command + the repo URL +
   a scannable QR code** to the replication packet. The QR code is the load-bearing detail: a
   skeptic on the symposium floor scans it and clones the repo before they ask the first question.

Every figure on the poster is the *same file* `nb8.3`/`nb8.5` wrote into `paper/figures/` — never
hand-drawn, never copy-pasted from a notebook screenshot. The poster `.pdf` is regenerated by
`make poster` from the same source as the abstract and the talk slides, so the three artifacts
cannot drift. Typography legible from six feet away (title ≥ 72 pt, body ≥ 24 pt); GMU branding per
the template; no emojis; figures legible in grayscale (Appendix D).

### D3 — The replication packet (verified by `make clean && make all`)

The six-part packet of Chapter 8.5, finishing the Lab-7 repository. (Originally this was labeled
"D2"; under the ASSIP deliverable model it is **D3**, third in order behind the abstract and the
poster, but the packet's six load-bearing parts are unchanged from the original specification:)

1. **Data or a data-access script.** Public data ships cached with its vintage pinned; licensed data
   (CRSP, Compustat, Bloomberg, WRDS) does *not* ship — it stays read-only on GMU infrastructure, and
   the packet carries the pinned access script in `src/` plus a `logs/pulls.jsonl` with content
   hashes so a reviewer with access re-pulls identical bytes. The README states which is which.
2. **Code in run-order** — `01_pull.py`, `02_build.py`, `03_analysis.py`, … — logic in `src/`, story
   in `notebooks/`, the order unambiguous.
3. **A README** — what / why / how-to-run — whose run section has collapsed to *one line*.
4. **A pinned environment** — human-readable `environment.yml` (`python=3.11` + the §5 stack) and the
   machine-exact `environment.lock.yml`.
5. **A fixed, named SEED** set once and threaded through every stochastic step (bootstrap,
   permutation, split), recorded in the README so a reviewer knows it was fixed *before* results, not
   tuned after.
6. **A single `make` / `run_all` entry point.** `make all` regenerates every table and figure from
   raw bytes to compiled PDF, with tables and figures *generated by code, never pasted by hand.* The
   honesty test, and the standard this row is graded against, is literally `make clean && make all`:
   delete every derived file and rebuild from nothing. If the PDF comes back identical, the packet is
   real; if a number drifts, you have a hand-edit, and you found it before a reviewer did.

### D4 — The 8-minute poster talk + defense at the Aug 12 symposium

The six-beat arc of Chapter 8.5 §1 — **question → why it matters → design/identification → headline
result → robustness → contribution** — delivered standing beside the poster you designed in D2.
ASSIP's poster session is in-person for on-campus interns and on virtual breakouts for remote
interns (Prof. Gao's 2026 ASSIP slot is officially remote, so the symposium's virtual track is the
primary defense venue), and the poster *is* your visual aid: each beat maps directly to a poster
panel, and you point at the panel as you speak. Optional companion slides (≤ 7) may be used for the
virtual track or for backup; if used, every result you say out loud is translated from a table into
a *figure* (point-with-error-bar, coefficient plot, event-study plot, RD binned scatter) — the Ch
8.5 §2 table-to-figure translation. Rehearse timed to fit in **seven** minutes with a pre-decided
cut line. The defense is graded as hard as the talk: the questions are the rows of your Chapter 7.5
threats table, so you answer in threat → why-plausible → what-you-did → residual-concern order, you
give a *located* "I don't know" when you cannot answer, and you can tell a survivable critique (it
attacks a number) from a fatal one (it attacks the comparison) and concede the fatal one honestly
rather than bluff.

### D5 — The responsible-AI-use disclosure (from Week 6)

A short disclosure (Ch 6.5 / Assessment 6 B4) stating, by category, where AI tools touched the work:
**label generation or any AI-produced data needs a validation table; prose editing is disclosed but
needs no validation; AI-suggested citations are the most dangerous and must be independently verified
or tagged `[CHECK]`.** This is the camp's honesty norm made explicit, and per CONVENTIONS §5 no key
or secret appears anywhere — environment variables only.

---

## The analytic rubric (200 points, allocations explicit)

Each row is scored at one of four levels. The rubric extends the Week-7 research-design rubric to the
whole project and is weighted, by design, toward **identification and threats**, **execution and
robustness**, and **reproducibility** — because those, not the eventual coefficient, are what make a
capstone defensible. The first two rows carry forward the Week-7 weights (they are the design half you
already filed); the new weight goes to *honest execution* and to the two ASSIP-specific
distillation crafts (the JSSR abstract and the poster).

| Criterion | Excellent | Proficient | Developing | Missing | Pts |
|---|---|---|---|---|---|
| **Research question & contribution** (Ch 8.3 §2–§4). One-sentence contribution naming a recognizable job (first / overturn / reconcile / mechanism / new data) with a verb calibrated to the design; the **JSSR abstract**'s six required moves all present (motivation, question, data+design, headline-with-CI, robustness, what-you-do-not-claim) inside the **200–300 word limit**; literature framed by contrast; every citation load-bearing and verified. | Contribution clear and calibrated, but one slip: a slightly over-claimed verb in the abstract, one missing move, or the abstract over/under the word count. | Contribution present but vague or a transcript-style "we run a regression on X"; abstract is a chronology instead of an argument. | No findable contribution sentence, abstract above 300 or below 200 words, or a fabricated/unverifiable citation, or "first" claimed where prior work did the same. | **30** |
| **Identification & threats** (Ch 7.5 → poster panel 3). Assumption sentence names the *effect* and the *specific threat* (never "endogeneity"), with the verb (*causal* vs. *credible*) calibrated to the evidence; threats table pulls the right design menu, adds data-specific threats, **matches a statistic to every testable threat and an argument to every arguable one**, leaves no residual cell empty, ordered by descending danger; **the assumption sentence is on the poster in the contract form** ("credible as long as [assumption], defended by [design]"). | Strong, but one slip: verb slightly overclaimed, one response mismatched to threat-nature, one thin/"none" residual cell, or the poster shows the regression equation where the contract sentence belonged. | Assumption vague ("controlling for confounders") or table missing the menu threats, several blank residuals, or testable/arguable confused. | No named assumption (or it says "endogeneity"), or no threats table, or every residual is "none." | **34** |
| **Execution & robustness** (Ch 8.1, 8.2). Pre-registered spec run *once* and reported whichever way it fell; specification curve with the pre-registered point marked and read by the §8.1.3 checklist; robustness battery operationalizes column 3 — correct SE flavor (clustered where treatment varies) **and** wild cluster bootstrap if treated clusters are few; placebos; sensitivity sweeps; **Oster $\delta$ with $R_{\max}$ defended and swept to 1**; a *failed* check reported as a finding that narrows the claim. | Battery present and mostly correct, but one gap: spec curve unmarked, $R_{\max}$ asserted without the sweep, or one obvious placebo missing. | Some robustness but key checks absent or misread (few-cluster ignored, $\delta$ with no $R_{\max}$, failed check buried), or a starred number kept after the bootstrap killed it. | No spec curve / no battery, or the confirmatory result was tuned post-hoc (freeze broken), or only-passing checks shown with the scary one omitted. | **40** |
| **Poster design & table-to-figure translation** (Ch 8.5 §2 + Appendix D). Six panels in reading order (title+abstract / question+stakes / design+identification / headline figure / robustness figure / contribution+limits+QR); every result on the poster is a **figure**, not a table (point-with-error-bar, coefficient plot, event-study plot, RD binned scatter); typography legible at six feet (title ≥ 72 pt, body ≥ 24 pt); axes labeled, CIs shown, units in human terms; figures grayscale-legible; GMU College of Science template (or the camp default if no template is available — `[CHECK]`); every figure is the same file `nb8.3`/`nb8.5` generated, never hand-pasted. | Clean and self-contained, but one lapse: a small table where a figure belonged, one panel out of order, a CI missing, or a noun-phrase title where a sentence-claim title belonged. | Several lapses: dense-text "data dump" panel, a hand-drawn figure, missing QR/repo link, or causal-language drift across panels. | No identifying-assumption panel, or only tables shown, or numbers retyped onto the poster so the abstract and the poster disagree. | **30** |
| **Reproducibility — the one-click packet** (Ch 8.5 + CONVENTIONS §5). `make clean && make all` rebuilds every table, figure, the abstract, **and the poster PDF** from raw on a fresh clone; abstract is generated from analysis variables (cannot drift from poster headline); env pinned (`.yml` + `.lock.yml`); SEED fixed, named, threaded; licensed data recipe-reproducible and kept on GMU infrastructure; **no secret anywhere**; the **QR code on the poster resolves to a working public repo**. | Rebuilds and is pinned, but one element thin: SEED set but not threaded everywhere, or one figure pasted, or the QR code broken / pointing to a private repo, or the licensed-data split undocumented. | A re-run would fail: `make all` errors or skips a step, no pinned lock file, abstract typed and disagrees with poster, or some numbers hand-copied so the chain breaks. | `make clean && make all` does not reproduce the poster, OR a hard-coded key/secret appears anywhere (this alone caps the row at Missing). | **34** |
| **Poster talk & symposium defense** (Ch 8.5 §1–§4). The six-beat arc delivered standing beside the poster (or on the virtual-breakout track for remote interns) in **≤ 8 min**, each beat tied to its panel, results in figures not tables; the defense answers questions as threats-table rows, gives a *located* "I don't know," and concedes a fatal critique rather than bluffing. | Solid talk and defense, but one slip: ran slightly long, one panel narrated as a table, or one bluffed answer. | Talk delivers the result but the design panel is weak or skipped; the defense dodges or over-defends a critique it should have conceded. | No coherent arc, or the defense bluffs a fatal critique / cannot state the design's weakness. | **22** |
| **Honesty & disclosure** (whole project + Ch 6.5 / D5). The confirmatory/exploratory line is drawn in public (DEVIATIONS.md, labeled exploratory analyses); limitations stated as intrinsic vs. fixable on the poster *and* in the abstract; the AI-use disclosure is complete and category-correct (validation table for AI-produced data, citations verified). | Honesty present, but one thin spot: a deviation logged without the outcome-driven verdict, or a disclosure category slightly vague. | Several lapses: overclaims the design, an outcome-driven deviation passed off as confirmatory, or an incomplete AI disclosure. | Hides a deviation, presents a searched result as a test, or omits/falsifies the AI-use disclosure. | **10** |

**Total: 200 points.** The rows sum to 30 + 34 + 40 + 30 + 34 + 22 + 10 = **200**. The three
design-and-execution-craft rows — identification & threats (34), execution & robustness (40), and the
one-click packet (34) — sum to **108**, more than half the grade, by design: what makes an ASSIP
capstone defensible is the craft, not the coefficient. The two heaviest single rows, *execution &
robustness* (40) and *identification & threats* (34), are the two questions a symposium judge or a
JSSR reviewer asks first and the two ASSIP's eight weeks taught you to answer about your own work
before anyone else can. Note that the **writing & table craft** row of the original course rubric
has been re-pointed at **poster design & table-to-figure translation** here, because the ASSIP
deliverable's load-bearing prose is the 250-word abstract (graded under row 1) and the load-bearing
visual is the poster (row 4). A full paper, when written, is governed by the writing rubric in the
optional-companion-paper supplement to this assessment.

---

## Instructor guidance and grading key

This is an open-ended terminal deliverable on each student's own project, so the key is a set of
*standards*, anchor papers, and the bright lines that separate the levels — not an answer sheet.

**The two highest-signal things to grade**, the same two from Week 7 now joined by execution: (1)
**Was there exactly one pre-registered primary specification, run once on the confirmation data and
reported whichever way it fell**, with the `pap-filed` tag predating any confirmatory commit? Check
the Git history; a starred headline that postdates no tag, or a primary spec that mutated after the
first look, breaks the contract and caps *execution & robustness* at Developing. (2) **Does
`make clean && make all` actually rebuild the paper's numbers on a fresh clone?** Run it. This is not
a formality — it is the row, and it is the single most objective thing in the rubric. A packet that
does not rebuild caps reproducibility at Developing; a hard-coded secret caps it at Missing on its own
per CONVENTIONS §5.

**How to grade fairly.** Grade the project the student *chose to write*, not the one you would have
written (the refereeing asymmetry of Ch 8.4 §1). Ambition is not the axis — a clean OLS-on-observables
study that honestly reports its Oster $\delta$ and labels its claim "robust association" is an A
project; an ambitious DiD that overclaims "causes" with a blank residual column is not. Calibrate
against the gallery: each of the five capstones is a worked anchor at the A/A− line. Grade each row
independently against the level descriptors, then sum; do not let a brilliant talk inflate a packet
that does not rebuild, and do not let one missing placebo sink an otherwise honest battery — that is
what the four-level structure is for.

**The line between an A and a B capstone.** Both run a real design on real data, find a result, and
write it up cleanly; the bones are sound for both. The difference is *honest stress-testing under
pressure*. The A capstone marks its pre-registered point on the spec curve and it sits near the
center; it reports the check that *failed* and narrows the claim accordingly; its Oster $\delta$ comes
with a defended $R_{\max}$ and a sweep to 1; `make clean && make all` rebuilds byte-for-byte; and in
the defense the student concedes the one fatal critique rather than bluffing and can state precisely
where their own design is weakest. The B capstone runs the battery but only shows the passes, asserts
$R_{\max}$ without the sweep, leaves the spec-curve point unmarked, has a packet that rebuilds "after
one fix," and in the defense argues harder when it should concede. The B is not dishonest — it simply
has not yet internalized that a failed check is a finding and a conceded critique is a strength. That
internalization is the whole point of the camp, and it is the A.

**Common failure modes**, the classic capstone ways to lose points:
(a) *Transcript, not argument* — a chronological "first I downloaded, then I cleaned, then I tried
three specs" with no headline-first structure; cap *writing & table craft* (Ch 8.3 §1).
(b) *Causal-language drift* — abstract hedges, conclusion claims "proves"; read only the verbs
attached to the main result across sections and force them to the weakest assumption (Ch 8.3 §7).
(c) *The robustness section that only passes* — a battery with no failed check reads as *less*
credible, because the grader assumes the student did not try hard enough to fail (Ch 8.2 §6); the
scary placebo for the top-ranked threat must be present whether or not it passed.
(d) *The few-clusters illusion* — three conventional stars on a treatment with eight treated clusters
and no wild cluster bootstrap; if the bootstrap was run and disagreed, the stars must be dropped, and
keeping them caps *execution & robustness* (Ch 8.2 §1).
(e) *Oster $\delta$ without $R_{\max}$* — uninterpretable; a $\delta$ reported without its $R_{\max}$
and a sweep to 1 is a non-answer (Ch 8.2 §5).
(f) *The pasted number* — a table or figure copied by hand so the chain breaks and `make clean &&
make all` does not reproduce it; this is the most common reproducibility failure and it caps the
packet row (Ch 8.5 §5).
(g) *The freeze broken* — a confirmatory coefficient that postdates no tag or mutated after peeking;
the p-value no longer means what Chapter 1.5 says, and the result is a search dressed as a test.
(h) *A hard-coded secret* — caps reproducibility at Missing on its own, no exceptions, per §5.

**How the rubric maps to the publication standard.** This capstone is calibrated to the
real-program bar: ASSIP's required deliverable is an **abstract published in the Journal of
Student-Scientists' Research (JSSR), GMU Mason Publishing** plus a **poster presented at the
Aug 12, 2026 symposium**, with an optional full paper. An *Excellent* across the contribution
(abstract), identification, execution, poster, and reproducibility rows is, concretely, a poster +
abstract pair that would clear a first-round JSSR review and that a symposium judge would not be
able to ambush: a credible (not overclaimed) identifying assumption with a threats table that
disarms the obvious attacks, a robustness battery that a reviewer would otherwise demand in round
two, figures legible from six feet and built to the Appendix-D craft standard, and a one-click
packet that satisfies the JSSR data-availability expectation. The JSSR submission standard *is* the
reproducibility row: a stranger scans the poster's QR code, clones the repo, types one command, and
the abstract and headline number rebuild from the deposited data and code. Grade to that standard,
because that is where the strongest ASSIP outputs are actually headed.

### What a top ASSIP capstone looks like, in one paragraph

It opens — both on the poster's top-left panel and in the JSSR abstract's first sentence — with a
hook that leads with a fact and a stake, and a one-sentence contribution whose verb is calibrated
to a design the audience can see filling a real, *constructed* gap; the design panel of the poster
shows the identifying-assumption sentence (effect named, specific threat named, verb honest) in
contract form, backed by a threats table that leads with the most dangerous row, matches a
statistic to every testable threat and an argument to every arguable one, and leaves no residual
cell empty; the headline panel reports the pre-registered spec — run once and reported whichever
way it fell — as a figure with its confidence interval and a single human-units sentence, with the
specification curve from Ch 8.1 in the robustness panel showing the marked pre-registered point
near the center of the distribution and an Oster $\delta$ with a defended, swept $R_{\max}$ noted
honestly, including the one check that narrowed the claim; the abstract carries the same number
because the abstract is *generated* from the same analysis variables — they cannot disagree; it
ships as a repo where `make clean && make all` rebuilds the **poster PDF** and the **abstract**
from raw data through seeded code with no secret anywhere, and the **QR code in the poster's
bottom-right panel** resolves to that repo on a visiting reviewer's phone; it is defended in eight
minutes of figures-not-tables standing beside the poster (or on the symposium's virtual breakout
track, since Prof. Gao's 2026 slot is remote), with the design panel as the spine, and in the
question period the student answers from their own threats table, gives a located "I don't know,"
and concedes the one fatal critique rather than bluffing; and it discloses, by category, exactly
where AI touched the work. That capstone can say the sentence the whole eight weeks existed to let
a student say truthfully, standing beside the poster on Aug 12: *"Here is what I found, here is
exactly why you should believe it, and here is the QR code that lets you check me."* That is an
original ASSIP capstone. That is the A.
