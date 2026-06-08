# PS 8.4 — A Referee Report + Your R&R Memo

**Course:** 8-Week Empirical Finance Camp · Week 8 · Problem Set 8.4
**Covers:** Ch 8.4 (Peer Review & Revision), standing on the reading discipline of Weeks 5–6 (read tables-first, ask the identifying question first) and the threats-and-responses table of Ch 7.5 / PS 7.5.
**Type:** Project deliverable, not a numeric problem set. This assignment has two halves, and you will play both sides of the desk. First you **referee** an assigned classmate's capstone draft and write a full report on it. Then, on the report another classmate writes about *your* paper, you write a **revise-and-resubmit memo** responding point by point. There is no answer key with "the right number," because what is graded is not a finding but a *judgment* — whether your report names the real threat and says what would change your mind, and whether your memo concedes, defends, and bounds on the evidence rather than the ego.

**Total: 100 points** — 60 for the referee report you write, 40 for the R&R memo you write in response to the report you receive. Point values are stated per part. A model deliverable — an A-grade exemplar referee report (Devon on Maya's fair-lending paper) and an R&R memo excerpt (Maya answering), with instructor grading notes — is in Appendix E (`E-w8-ps8.4-solutions.md`). Read it *after* you draft your own, the way Ch 8.4 §5–§8 walked through the same pair: not to copy, but to calibrate.

A note on what this assignment is for. Ch 8.4 revealed the trick once, and it is the whole of the assignment: **refereeing and writing are the same skill aimed in opposite directions, and you already learned the skill in Weeks 5 and 6.** Reading a paper tables-first and asking "what is the identifying assumption and what threatens it" was rehearsal for exactly this. The only thing new is that the paper on your desk was written by a peer who will read what you say — which is why the governing norm is **tough on the work, kind to the person**, and the governing constraint on your memo is **do exactly what you say you did.** Those two norms are not decoration. They are graded directly, and a submission that violates either fails the part it touches no matter how polished the prose.

---

## What you submit

**Two Markdown files**, both committed to the workshop repository under your handle:

1. `referee-report.md` — your report on the draft you were assigned. One to two pages.
2. `rr-memo.md` — your point-by-point response to the report you received on *your own* paper. One to two pages.

You will receive your assignment (whose paper you referee) and your incoming report (who refereed yours) from the workshop matching at the start of the session. The draft you referee is a classmate's 8.1–8.3 capstone; the report you answer is one a classmate wrote on yours. If the logistics give you the incoming report before you have finished writing the outgoing one, write the outgoing report first anyway — you cannot fairly respond to a referee until you have stood in a referee's shoes.

---

## Part A — The referee report (60 points)

Write `referee-report.md` in the fixed skeleton of Ch 8.4 §2, in order. The order is load-bearing in exactly the way the Week-5 reading order was: you read tables-first, and you *write* the report concern-first. Open the file with a single line stating your verdict (Part A6), then the body in the skeleton below.

### A1 — Summary in your own words (10 points)

Open with one paragraph — three to six sentences — stating what the paper does: the question, the data, the design, and the headline finding *with its magnitude as the author reports it*. Write it the way you would summarize Fama–French from the tables, ideally without leaning on the author's abstract. This is not filler and not flattery; it is *proof you understood the paper*, and it is the single most reassuring thing an anxious author can read.

- Full marks: a faithful, specific summary that names the design and the headline number, that the author would recognize as their paper.
- Where points are lost: a vague restatement of the title ("this paper is about fair lending"); a summary that silently corrects or editorializes instead of describing; a summary that describes a paper the author did not write *without flagging the mismatch*. That last case is subtle — if your honest summary does not match the paper's intent, **that mismatch is itself a finding** (the paper failed to communicate its claim) and belongs at the top of your major points, not buried.

### A2 — The single biggest concern, stated first (15 points)

After the summary, lead with the one issue that most threatens the paper — the thing that, if the author cannot answer it, sinks the result. Do not bury it behind smaller points; do not soften it; do not build to it. In almost every empirical paper this biggest concern is an **identification threat** — the alternative explanation for the headline result that the design did not rule out. Name it *specifically*, the way PS 7.5 demanded of your own memo: "anticipation contaminating the pre-period," not "endogeneity."

- This is the highest-value single judgment in the report and it is weighted accordingly. Full marks require (i) that the concern you lead with is genuinely the most dangerous one on the paper — not the most *findable* one — and (ii) that you say **what evidence would change your mind**, stating, where you can, both what would *reassure* you and what would be *fatal*.
- Where points are lost: leading with a typo or an exposition nit while a broken design waits on page two (mis-ranked concerns — the report has failed its core job); naming a vague threat ("there might be confounders") with no falsifying evidence attached; stating a complaint instead of a contract (see A4).

### A3 — Identification threats, in descending order of danger (12 points)

Having led with the biggest one, work through the remaining threats to the credible interpretation. This is pure Week-5 reading: for the design the author *chose*, pull the standard menu from Ch 7.5 §2 and go threat by threat. For a difference-in-differences that menu is pre-trends, anticipation, and — in staggered designs — the forbidden comparison of already-treated units (Ch 4.2). For IV it is relevance and exclusion; for RD, continuity and manipulation. For each: did the author address it, did they address it *convincingly*, and if not, what specific evidence would settle it?

- Respect the asymmetry of Ch 8.4 §1: **it is the author's paper, not yours.** You may, in one sentence, note that an alternative design exists; you may not spend three paragraphs rewriting the paper into the one you would have done. A report that hijacks the project loses points here even if every individual point is correct.
- Full marks: the standard menu for *this* design is covered, ordered by danger, each threat paired with the evidence that would settle it.

### A4 — Specification and robustness (10 points)

Below identification sit the questions of whether, *granting* the design, the estimate is fragile. Are the standard errors the right flavor — clustered at the level the treatment varies, per Petersen (2009) and Bertrand, Duflo & Mullainathan (2004) from Week 5? Does the headline survive the march across columns as controls are added (the 8.1 specification curve), or collapse? Are the obvious placebo and falsification tests run (8.2)? Is multiple testing handled if many outcomes are reported? These matter, but they are *downstream* of identification: a perfectly clustered standard error on a coefficient with no credible design is a precise estimate of nothing — so do not let a robustness nit crowd out a design threat.

### A5 — Exposition (5 points)

Last come the writing issues: an introduction that overclaims relative to the tables, a contribution sentence you cannot find, a results section that narrates coefficients instead of interpreting them, tables that violate the Appendix D conventions, a figure with no axis labels. Exposition matters — a paper a reader cannot follow is a paper a reader will not believe — but it goes last so the author reads it last, after absorbing what actually matters. Fixing prose on a paper with a fatal design is rearranging deck chairs.

### A6 — Major/minor labeling, the change-my-mind rule, and the verdict (8 points)

Three disciplines, graded together:

- **(a) Major vs. minor (3 pts).** Sort every point into a numbered **major** list (resolution could change the paper's conclusion or your belief in it) and a **minor** list (improves the paper without touching the verdict). The label is a courtesy to the author — where to spend limited revision energy — and a discipline on you, forcing you to decide, per comment, whether it could really change the result.
- **(b) The change-my-mind contract (3 pts).** For **every** major point, state what evidence would change your mind. Not "I am not convinced parallel trends holds" (a complaint) but "an event-study plot with at least four pre-period leads would let me judge; flat, insignificant leads would substantially reassure me" (a contract the author can act on). A major point with no falsifying-or-reassuring evidence attached is incomplete and is scored as such.
- **(c) The verdict (2 pts).** State, on the top line of the file, your honest and *calibrated* verdict: **reject**, **major revision**, **minor revision**, or near-ready. A clean design on real data with a found, stress-tested result is a major or minor revision even with ten things to fix — the bones are sound. A headline resting on a design that cannot identify the claimed effect is a *reject as currently identified*, however clean the prose; saying so plainly is kinder than a vague "promising but needs work" that wastes the author's next month.

### The tone gate (applies across Part A)

The norm of Ch 8.4 §4 is enforced on the whole report: **criticize the paper as hard as the evidence demands; never criticize the author.** Write "the identification section does not rule out anticipation," not "you didn't think about anticipation." Attribute claims to the text, not to a supposed failing of mind. Assume competence and good faith. A report whose *content* is excellent but whose *tone* attacks the person is marked down across Part A — not as etiquette policing, but because a hard point delivered carelessly gets rejected for its tone instead of accepted for its content, which means the criticism fails to do its one job. The flip side is equally penalized: **false reassurance is the true cruelty.** A report that waves through a broken design to spare feelings has guaranteed a harsher audience breaks it later, when it costs more. Tough on the work *is* the kindness.

---

## Part B — The R&R memo (40 points)

Now flip the desk. You have received a report on your paper. Write `rr-memo.md` responding to it point by point, in the rigid and merciful shape of Ch 8.4 §6. You need not address every minor comment in full prose, but you must respond to **every major point**.

### B1 — The quote-change-evidence shape, for every major point (16 points)

For each comment, do three things, **in this order**: **quote** the comment verbatim (blockquote or italics, so your reader need not hold two documents side by side); state **what you changed** in plain, specific language ("we have added an event study as new Figure 2 and discuss it in Section 4.2"); then point to the **evidence** — the new table or figure number, the section, and the actual number the new analysis produced.

- Full marks: every major point answered in this exact shape, with a *specific location* and a *specific result* for each.
- Where points are lost, hard: "we have addressed this concern" with no *where* and no *number*. The editor cannot verify it and will assume you did nothing — and so will the grader. A response with no number attached scores near zero for that point.

### B2 — Concede, defend, and bound — at least one of each, consciously chosen (15 points)

A memo that caves to every comment is as weak as one that fights every comment. The skill is knowing which is which, and your memo must demonstrate all three moves of Ch 8.4 §7. Across your responses you must show, and you should label for the grader which is which:

- **One concession (5 pts).** Where the referee was right, fix it, say so plainly, and report the consequence *even if it weakens your result*. "The referee is correct; we had clustered at the wrong level. We now cluster by state, and the t-statistic falls from 4.1 to 2.6, which we report." Conceding a weaker number honestly is the *strongest* evidence you can offer that the surviving result is real — a referee believes a 2.6 they forced far more than a 4.1 they doubted. Honest concession is not surrender.
- **One evidence-backed defense (5 pts).** Where the referee was wrong, disagree respectfully — but with **evidence, not attitude**. The cleanest defenses *do the requested work first* and then explain why the worry does not bite: "We respectfully disagree that small-cell volatility drives the result; as the referee suggests, we checked directly — weighting by volume (new column 4) leaves the estimate at 1.3 pp, dropping small counties (column 5) gives 1.5 pp." A defense that is pure assertion with no test run scores as a non-defense.
- **One bounded untestable threat (5 pts).** For the comment you can neither fully fix nor fully rebut — the exclusion restriction, the parallel-trends counterfactual itself — neither concede the paper is broken nor pretend the concern is gone. **Bound** it: acknowledge it is real and untestable, present every piece of indirect evidence, and state the residual honestly in the paper's limitations. This is the fourth column of your Ch 7.5 threats table, promoted into a public defense. A memo that claims every threat is vanquished reads as naïve; a referee trusts the author who says "here is what still worries me."

### B3 — The do-what-you-said-you-did gate (9 points)

The deepest norm of the whole exercise, and the one graded hardest: **every change your memo claims must be a change your revised paper actually contains.** If your memo says you added an event study, the event study must be in the paper, it must be the one you describe, and its leads must say what your memo says they say. Referees check; the grader checks; the whole institution of peer review runs on the assumption that the memo is honest, and a single caught discrepancy poisons every other claim in the document.

- Full marks: a spot-check of any claim in your memo against your revised paper confirms it.
- Where points are lost, terminally: a memo claim the paper does not back up. This is not a deduction proportional to the error — a caught fabrication zeroes B3 and casts doubt on the rest, exactly as it would end a referee's trust in your career. Honesty here is the load-bearing wall, not optional ethics.

---

## Submission checklist

Before you commit, confirm:

**Referee report (`referee-report.md`):**
- [ ] Verdict on the top line; one of reject / major revision / minor revision / near-ready, and *calibrated* to the design's actual health.
- [ ] Summary in your own words first, naming the design and the headline magnitude — and any author/summary mismatch flagged as a major point.
- [ ] The **single biggest concern stated first**, named specifically (not "endogeneity"), with the evidence that would change your mind.
- [ ] Identification threats next (the standard menu for *this* design), then specification/robustness, then exposition — in that order.
- [ ] Every point sorted into **major** or **minor** and labeled; for **every major point**, the falsifying-or-reassuring evidence is stated.
- [ ] Tough on the work, kind to the person: every sentence about the paper, none about the author; no false reassurance on a real flaw.
- [ ] You did **not** hijack the paper into the one you would have written.

**R&R memo (`rr-memo.md`):**
- [ ] Every **major** point answered in the quote → what-changed → evidence shape, with a specific location *and* a specific number.
- [ ] At least **one concession, one evidence-backed defense, and one bounded untestable threat**, each labeled.
- [ ] Where a concession weakened a result, the weaker number is reported, not hidden.
- [ ] Every change the memo claims is actually in the revised paper (spot-check it yourself before you submit).
- [ ] No claim of a "clean sweep"; the residual limitation is stated honestly.

---

## How this is graded

This problem set is the engine of the **Week-8 peer-review workshop** and feeds **Assessment 8**, which grades the report and the memo together on the peer-review rubric. The allocation above maps onto it: Part A1–A3 → the reading discipline of Weeks 5–6 turned outward (summary as comprehension proof; biggest-concern-first; the design's threat menu); A4–A5 → the downstream-of-identification ordering; A6 → calibrated judgment (major/minor, the change-my-mind contract, an honest verdict); the tone gate → the tough-on-work-kind-to-person norm. Part B1–B2 → the quote-change-evidence discipline and the conscious concede/defend/bound decision; B3 → the do-what-you-said-you-did norm, the single most heavily protected line in the rubric. The model deliverable in Appendix E shows the A-grade standard for both documents, annotated with the rubric levels each section hits and the moves that separate a *constructive* report from a *destructive* one.

---

## The bridge to Ch 8.5

The report you wrote and the memo you wrote do not end here. In Ch 8.5 you defend the revised paper and ship the replication packet — and the revised paper **must already reflect the changes your R&R memo promised**. That is the do-what-you-said-you-did norm with a deadline: the new Figure 2 your memo described is the figure that must appear in the packet, producing the number your memo quoted. Mentor Session 8, *"Defending a result: what a referee actually asks,"* rehearses the live version of this exchange — the questions a referee fires across a seminar table — tied to Prof. Gao's disclosure work (Elnahas, Gao, Hossain & Kim, 2024, *JFQA*). Come to the workshop ready to be both referee and author in the same hour.

---

*End of PS 8.4. The model deliverable is in `book/appendices/E-solutions-manual/E-w8-ps8.4-solutions.md`: Devon's A-grade report on Maya's HMDA fair-lending paper and Maya's R&R reply, with instructor notes on constructive vs. destructive refereeing. Draft both of your own documents first; read the exemplar to calibrate, not to copy. The skeptic who reads a stranger's tables and the author who answers a stranger's report are the same person — this assignment is you, in one session, doing for a classmate what Week 5 trained you to do, and letting a classmate do it for you so you both fix the flaw before the grader finds it.*
