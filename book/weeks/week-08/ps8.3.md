# PS 8.3 — Draft Your JSSR Abstract and Poster Results Narrative Against the Style Guide

**Course:** ASSIP 8-Week Empirical Finance Camp · Week 8 · Problem Set 8.3
**Covers:** Ch 8.3 (Writing the Empirical Paper) — the four-move introduction (§2) compressed to
the **JSSR abstract**, the one-sentence contribution (§3), the positioning literature review (§4),
the headline-first results section (§5) compressed to your **poster's results panel**, and the
causal-language discipline (§7) — held to the binding table-and-prose standard of **Appendix D**
(`book/appendices/D-style-guide/`; D.1 table layout and notes, D.2 coefficient/FE/cluster/sample
disclosure, D.5 prose-style and causal-language rules). Builds on the frozen estimates from Ch 8.1
(specification curve) and Ch 8.2 (robustness), and the identification memo of Ch 7.5.
**Tool:** `nb8.3` (`notebooks/week-08/nb8.3-publication-tables-figures.ipynb`) — generates your
headline regression table, the event-study figure, **and the 200–300-word JSSR abstract** to the
Appendix D / JSSR standard, exported to LaTeX. **You do not hand-format a single table or hand-type
the abstract.**
**What you turn in:** a single Markdown (or LaTeX) file, `abstract-and-results.md`, containing two
artifacts of *your own* ASSIP project — the **JSSR-ready 200–300-word abstract** (the one the
poster's title block and the JSSR submission both carry) and your **poster results-panel narrative
plus headline-table backing** — plus a short reflection. This is a **scaffolding assignment that
produces a real deliverable for your own project.** Every camper's draft is different because every
camper's project is different. *Students writing the optional companion full paper should still
complete this PS; the abstract drafted here is the same abstract the companion paper carries — they
cannot diverge.*

**Total: 100 points.** Point values are stated per component and map onto the writing rubric Appendix E grades against. The two cross-cutting principles dominate the grade, both straight from Ch 8.3: **front-load every verdict** (the contribution leads the intro, the headline table leads the results, the topic sentence leads each paragraph — §1's "say the important thing first, at every scale"), and **match every verb to your weakest assumption** (§7's causal-language discipline). A draft that buries its contribution in paragraph four, or that lets "is associated with" drift into "causes" by the results section, loses points the same way a real manuscript loses a referee.

**The one rule that makes this assignment mean anything.** Your introduction must be **readable by someone who will never read the rest of the paper** (Ch 8.3 §2). A program officer skimming fifty abstracts, a professor deciding whether to assign your paper, a journalist hunting a number to quote — all of them stop at your introduction. If a reader who stops there cannot walk away with your *question*, your *answer*, and the *appropriate degree of confidence* in that answer, the introduction has failed its one job, and no polish on the body will rescue it. Write the front for the reader who never reaches the back.

**A note on numbers.** Unlike PS 7.3 (the pre-analysis plan, which is *pre-results* and therefore contains no estimates), this assignment is *post-results*: you have your frozen point estimate from Ch 8.1 and your robustness battery from Ch 8.2, and the whole point is to *report* them well. Report your real, frozen numbers — never numbers you wish you had, never numbers tuned after the fact. If you are drafting before your own analysis is final, you may use **clearly-labeled illustrative** numbers from `nb8.3`'s synthetic example (as the model deliverable does), but label them illustrative every time, exactly as the exemplar does. The cardinal sin is a table that has silently drifted from the analysis it claims to report — which is why `nb8.3` *generates* your table from the frozen results rather than letting you retype them.

**The model deliverable** in `book/appendices/E-solutions-manual/E-w8-ps8.3-solutions.md` shows the A-grade standard on **Maya's** HMDA fair-lending difference-in-differences (the project carried since Week 1, the identification memo of Ch 7.5, the robustness battery of Ch 8.2). Read it *after* you draft your own — not before — so it calibrates your standard without dictating your project. Your introduction should be *as disciplined as Maya's about your own question*, not a paraphrase of hers.

---

## Component 1 — The one-sentence contribution (15 points)

Before you write a paragraph, build the single sentence the whole introduction serves (Ch 8.3 §3). If you cannot write it, you do not yet have a paper — you have a regression and a hope.

**(a) (8 pts) Write it, and name its job.** Write your **one-sentence contribution**: the answer to *what is true now that was not established before you did this work?* Not what you did ("we run a difference-in-differences on HMDA") but what is now *known* ("we provide the first quasi-experimental estimate of how state fair-lending examination programs affect the minority–white denial gap"). Then name which of the recognizable **jobs** from §3 it claims — *first* to credibly estimate, *overturn/qualify* an established finding, *reconcile* two literatures, *measure a mechanism*, or *bring new data* — and justify in one sentence that your literature review will *support* that claim rather than expose it (if you claim "first" and three papers did it already, you have just handed a referee a ten-second kill).

**(b) (4 pts) Calibrate the verb to the design.** State, in one sentence, why your contribution sentence uses the verb it uses, *bounded by your weakest identifying assumption* (§7). A clean staggered DiD with flat pre-trends earns "credibly estimate"; an OLS-on-observables with a plausible omitted variable you could not rule out earns only "document a robust association" or "provide suggestive evidence." Quote your own contribution sentence's main verb and name the assumption that licenses it.

**(c) (3 pts) The stress test.** Apply the §3 practical test: hand your contribution sentence to a classmate who has not seen your project and ask them to tell you, from that sentence alone, *what you did and why it matters.* Report what they said. If they asked "wait, what's the question?" or "is that causal?", revise the sentence and report the revision — those questions mean the sentence is doing the introduction's whole job badly.

---

## Component 2 — The four-move introduction (35 points)

Write your full introduction as the four moves of Ch 8.3 §2, **in order**: hook, one-sentence contribution (from Component 1, landing in the first or second paragraph), the "we find" preview, and the roadmap — with one bridge sentence of positioning into the literature. Roughly four to six paragraphs. Label each paragraph with the move it makes (you may delete the labels in a final version, but keep them for grading).

**(a) (8 pts) The hook.** Open with a real-world fact or tension — a number, a puzzle, a policy debate — that names the question and makes the reader care, in that order, fast. **Do not open with "the literature has long studied."** The hook earns attention with *consequence*, not with a literature recitation. Two or three sentences. (Maya's hook leads with the denial-gap number and the regulatory stakes, not with a citation.)

**(b) (8 pts) The "we find" preview.** Write the paragraph — usually beginning literally "We find that..." or "Our main result is..." — that previews **the headline number, its sign, its rough magnitude in units a human can feel, and the key robustness fact**, then names the assumption the interpretation rests on. Magnitude in human units means "about 1.8 percentage points, roughly a fifth of the pre-period gap," *not* a bare coefficient. Students resist this paragraph because it feels like spoiling the ending; reread §1, there is no ending to spoil. Give the number up front; you spend the rest of the paper earning the right to have stated it.

**(c) (6 pts) The positioning bridge.** Write the one or two sentences that locate your contribution between the strands of literature, *by contrast, not by listing* — "our work sits at the intersection of two literatures that have not met: [strand A, which establishes X but cannot do Y] and [strand B, which does Y but cannot speak to Z]." This is a preview of Component 4; here it is the single bridge sentence that takes the introduction into the literature section.

**(d) (5 pts) The roadmap.** Write the short, functional last paragraph: "Section 2 positions our work in the literature; Section 3 describes the data; Section 4 lays out the design and our identifying assumption; Section 5 presents the main results; Section 6 reports robustness; Section 7 concludes." A few sentences, no drama.

**(e) (8 pts) Verb audit (the §7 discipline, made into a deliverable).** After drafting, do the deliberate pass of §7: read *only the verbs attached to your main result*, across the hook, the preview, and the contribution sentence, and force every one down to the level your weakest identifying assumption permits. In a short paragraph, report the verbs you found and any you changed — e.g., "the preview originally said 'the program reduces the gap'; my design is a DiD whose parallel-trends assumption is untestable beyond the pre-period, so I changed it to 'the program reduced the gap, an estimate credible under parallel trends,' with the assumption attached." Catch *drift* (the abstract hedges, the results forget themselves) and catch *over-hedging into mush* ("may possibly perhaps tentatively suggest" has hedged itself out of any claim). Calibration cuts both ways: claim *exactly* as much as your design supports.

---

## Component 3 — The positioning literature review (15 points)

Write the literature-review section of your paper — the part that draws the map so your gap is **visible as a gap** (Ch 8.3 §4). The failure mode this component grades against has a name: the **annotated bibliography** ("Smith finds A. Jones finds B. We contribute."). That is a list, and a list does the reader no work.

**(a) (9 pts) Group and contrast.** Cluster the prior work into **two or three strands** — by question, by method, or by finding — and characterize each strand by what it *established* **and what it could not**, so the empty space on the map (your contribution) is *constructed brick by brick out of the literature itself*, not merely asserted. Cite primary sources with full bibliographic information per CONVENTIONS §6; if you cannot verify a citation, tag it `[CHECK]` rather than fabricate it (a hallucinated reference is the one error a referee catches in ten seconds and never forgives). Maya's fair-lending positioning cites **Gao & Sun (2019)** on the same-sex-borrower margin as part of the strand that documents differential treatment.

**(b) (3 pts) Every citation load-bearing.** Confirm in one sentence that every paper you cite either *builds part of the map's wall or marks the edge of the hole* — if a citation could be deleted without changing where the gap appears, delete it. A padded review signals you are counting references, not building an argument.

**(c) (3 pts) Generous and precise, never dismissive.** Confirm that you position prior work as "established X under conditions Y; we extend to where Y fails," not "prior work was wrong." The dismissive voice is the voice of someone about to be refereed by the author they just insulted.

---

## Component 4 — The headline-first results section (25 points)

Write a results-section **excerpt** that **leads with your headline table** (Ch 8.3 §5). The cardinal sin here is the *data dump*: eight tables of equal weight, leaving the reader to find the important one. You found it for them in the introduction; do it again here.

**(a) (12 pts) The headline table, generated by `nb8.3`, Appendix-D-compliant.** Place your single main table — generated by `nb8.3`, **not hand-typed** — as the first object in the section. It must **stand alone** (Ch 8.3 §8): a reader seeing *only* the table can determine the sample, the estimator, the meaning of the coefficient, what the stars mean, and what fixed effects and clustering were used. Per **Appendix D** the table carries:
1. an **informative title** and **complete notes** defining the sample, units, estimator, and every symbol (D.1);
2. **standard errors or t-statistics in parentheses** directly beneath each coefficient, with the **flavor of SE named and clustered *on what*** (D.2) — "standard errors clustered by state in parentheses," not a bare "(0.07)";
3. **significance stars defined in the notes** (e.g., `*** p<0.01, ** p<0.05, * p<0.10`), never left to the reader's guess;
4. a **consistent, sensible number of significant digits** (a coefficient is not more precise for six decimals);
5. dedicated rows disclosing **fixed effects, controls, sample size $N$, and (within-)$R^2$** (D.2) so the specification is legible at a glance.

If you have a building-up table (column 1 raw, then adding controls and fixed effects, with your preferred specification flagged), so much the better — that is the standard nb8.3 produces.

**(b) (9 pts) Walk the reader through it, in human units.** In prose, point at the coefficient, state its **sign**, its **magnitude in units a human can feel** ("1.8 percentage points, about a fifth of the pre-period gap" — not just a number), and its **statistical precision**. Then interpret it **economically**: is the effect big enough to *matter*, not just big enough to be *significant*? Significance is not importance — a coefficient can be three-starred and economically trivial — and your prose must carry the economic interpretation the stars cannot. Lead with the headline; mention secondary results only *after*, and explicitly subordinate them.

**(c) (4 pts) Causal language held to the design (the §7 audit, again).** Confirm in one or two sentences that the verbs in your results prose match your weakest assumption — the place §7 warns drift bites hardest ("the results section forgets itself"). If your design is a DiD, the results say "the program reduced the gap" *with the parallel-trends conditional somewhere in the section*, never an unconditional "causes." If your design is observational, the results say "is associated with" and stay there. Name the strongest verb you used and the assumption that earns it.

---

## Submission checklist

Turn in **one file**, `intro-and-results.md`, plus the reflection below. Before you submit, confirm:

- [ ] **One-sentence contribution** written, its §3 *job* named, its verb calibrated to the weakest assumption, and stress-tested on a classmate (Component 1).
- [ ] **Introduction makes the four moves in order** — hook (fact/tension, not "the literature"), contribution sentence (in para 1–2), "we find" preview (number + human-unit magnitude + key robustness fact + assumption named), positioning bridge, roadmap (Component 2).
- [ ] **A reader who stops at the introduction** walks away with the question, the answer, and the right degree of confidence (Ch 8.3 §2's one rule).
- [ ] **Verb audit done** — only the verbs attached to the main result, forced to the weakest-assumption level; drift caught, over-hedging caught (Component 2e, §7).
- [ ] **Literature review groups-and-contrasts** into 2–3 strands, constructs the gap, every citation load-bearing, generous-and-precise tone, Gao & Sun (2019) cited where the fair-lending differential-treatment margin is positioned; full bibliographic info per CONVENTIONS §6, `[CHECK]` on anything unverified (Component 3).
- [ ] **Results section leads with the headline table**, generated by `nb8.3` (not hand-typed), **Appendix-D-compliant** — title, complete notes, named-and-clustered SEs in parentheses, defined stars, sensible significant digits, FE/controls/$N$/$R^2$ disclosure rows — and the table **stands alone** (Component 4a, Ch 8.3 §8, Appendix D.1–D.2).
- [ ] **Headline walked in human units** with an explicit **economic** interpretation (big enough to matter, not just to be significant), headline before secondary results (Component 4b).
- [ ] **Causal language matches the design** everywhere — no "causes" without the identifying-assumption conditional; no observational study dressed in causal clothing (Component 4c, §7).
- [ ] **Numbers are real and frozen** (from Ch 8.1/8.2) or, if drafting early, **clearly labeled illustrative** every time; the table is *generated*, never retyped, so it cannot silently drift (assignment's note on numbers).
- [ ] **Voice and citation**: full paragraphs, concrete-before-abstract, no marketing voice, no emojis (CONVENTIONS §1).

**Reflection (ungraded but required, ~150 words).** Answer Ch 8.3's "Your Turn" prompt 3 for *your* project: take the headline table `nb8.3` generated, cover up the surrounding prose, and list **every thing a reader cannot determine from the table alone** — the sample, the estimator, what the stars mean, the fixed effects, the clustering. Then say which of those you fixed in the **table notes** (following Appendix D) rather than in the paragraph, and why a table that needs its surrounding prose to be intelligible has failed its first and most important reader (the referee who goes to the tables first).

---

## How this is graded

Appendix E grades against the **writing rubric**, with points mapped to the four components above. Two cross-cutting principles dominate, both straight from Ch 8.3:

1. **Front-load every verdict.** The contribution leads the introduction, the headline table leads the results, the topic sentence leads each paragraph (§1). A draft that builds suspense toward a reveal at the end — the high-school mystery-essay habit — loses points, because in a paper suspense is a bug: the reader is your judge, not your entertainment, and you make their job easy by stating the verdict first. Full marks require that a reader who quits after the first sentence of any unit has still learned the most important thing in that unit.

2. **Match every verb to your weakest assumption.** Your strongest verb is bounded by your weakest assumption (§7). A clean DiD with flat pre-trends earns "the program reduced the gap" *with the assumption named*; an OLS-on-observables earns only "is associated with." The most-punished failure is *drift* — the abstract hedges correctly, the results section forgets itself, the conclusion claims "we have shown that X causes Y." We run the same audit you ran on published authors in Week 5: underline every causal verb attached to the main result and ask "did the design earn this?" Run it on yourself before the grader does.

A note on the division of labor with Appendix D: this problem set tells you *which moves to make and in what order*; **Appendix D is the binding spec for the table craft and prose style** — exact table layout and notes (D.1), which coefficients and FE/cluster/sample lines to disclose (D.2), the prose-style and causal-language rules (D.5). Do not reinvent the standard here; point your draft at D and follow it. And do not hand-format your tables in a text editor — `nb8.3` does it for you, reproducibly, from the frozen results, which is the entire point.

---

*End of PS 8.3. When your `intro-and-results.md` is drafted, check your standard against the model deliverable in `book/appendices/E-solutions-manual/E-w8-ps8.3-solutions.md` — an A-grade introduction and a headline-first results excerpt for Maya's HMDA fair-lending DiD, with a fully Appendix-D-compliant headline table and instructor grading notes on overclaiming, table craft, and the one-sentence contribution. Read it after you draft your own. The introduction you write here is the promise your whole paper defends; the results section is where, leading with the table, you begin to redeem it. Both live or die on the same two disciplines — say the important thing first, and claim exactly as much as your design supports, no more and no less.*
