# PS 7.1 — Three Candidate Questions, Scored: A Feasibility-and-Novelty Deliverable

**Course:** 8-Week Empirical Finance Camp · Week 7 · Problem Set 7.1
**Covers:** Ch 7.1 (Idea-Generation Workshop) — the puzzle→falsifiable-hypothesis transformation (the four-slot grammar: *outcome · treatment · direction · unit-and-window*, §7.1.1), the **so what / who cares / what's new** filter run in that order (§7.1.2), the design catalog run *backwards* to find identifying variation (§7.1.3, reaching back to Weeks 3–4: RD/DiD/event-study/IV), the four feasibility constraints (§7.1.4: data access · scope · time-and-reproducibility · your own skills), the leashed AI literature scan (§7.1.5, building on Ch 6.5), and above all the **five-dimension feasibility/novelty rubric** (§7.1.7, 0–2 per dimension, /10, with a hard **veto** on *Identifiable?* or *Feasible?*). It reaches back to **CONVENTIONS §4** for the seven-field spec line and **§5** for data discipline.

**This is a research deliverable, not a numeric drill.** There is no back-of-the-book number to recover and no autograder for prose. You are producing the document that every other chapter of Week 7 consumes: a short, honest portfolio of three candidate research questions, each sharpened, scored, and either kept or killed, ending with one locked choice you can defend in front of a room. The skill being graded is *judgment* — can you tell a researchable question from a mood, a real design from a correlation dressed up as one, and a five-week project from a five-year one — so your reasoning is the answer, not your conclusion.

**Tools you will reuse.** The notebook `nb7.1` (`notebooks/week-07/nb7.1-idea-to-spec-template.ipynb`) already gives you the exact machinery: the four-slot hypothesis grammar, the `spec_line(...)` formatter that refuses a blank CONVENTIONS §4 field, and the `Idea` dataclass with `rank_ideas(...)` that encodes the rubric and its veto. You may write your three candidates *as* three `Idea(...)` rows and run `rank_ideas` to produce your ranking table — that is the intended workflow, and the conceptual contract this problem set is built on. You do not need any data, any regression, or any new code beyond filling that template.

**Total: 100 points.** Point values are stated per problem. The single most common way to lose points here is to flatter a weak idea instead of killing it — the rubric is "a checklist with veto power, not a sum to maximize" (§7.1.7), and a submission that keeps an unidentifiable or infeasible idea because its *total* looked high has missed the entire lesson. The model deliverable is in Appendix E (`E-w7-ps7.1-solutions.md`); attempt your own three candidates before you read it.

**A note on the numbers.** Your candidate questions are **proposals, not results.** Do not invent an effect size, a coefficient, a t-statistic, or a "the 2022 depeg wiped out \$40B"-style magnitude — you have not run anything yet, and a fabricated number in a proposal is exactly the §6.5 / CONVENTIONS §6 failure the chapter warned you about. A directional *hypothesis* ("volume **rises**") is required; a *quantified prediction* ("volume rises 312%") is forbidden until you have the data. Datasets you name must be ones that genuinely exist and that you could actually obtain (the §7.1.6 map is your menu of safe choices); if you reference a paper to argue novelty, it must be a real, verifiable citation, tagged `[CHECK]` if you could not confirm it rather than fabricated.

**How the pieces fit.** Problem 1 builds the three candidates — for each, the refined question, the signed hypothesis with $H_0$, the identifying variation, and the CONVENTIONS §4 spec line. Problem 2 scores all three on the rubric and ranks them, with the veto explicit. Problem 3 is the selection: you pick one, justify it against the rubric *and* the four feasibility constraints, and name the runner-up you hold in reserve. Problem 4 is the honesty check — the single most dangerous confounder your chosen design does *not* handle, and the descriptive-vs-causal line. Problem 5 is the short reproducibility-and-citation discipline pass. Pick a real interest of your own (or adopt a cast member's lane if you are still searching); whatever you choose in Problem 1 you carry through all five problems.

---

## Problem 1 — Three candidate questions, fully specified (40 points)

Produce **three distinct candidate research questions.** They may live in one topic area (three different angles on crypto, say) or span three — but they must be genuinely different questions, not three rephrasings of one. At least one should be an idea you are tempted by *and* suspect may be weak, because the rubric only earns its keep when it has something to kill. For **each** of the three candidates, deliver all four components below. Lay each candidate out under its own subheading (Candidate A / B / C) so the grader can read them in parallel.

**(a) (12 pts — 4 per candidate) The refined question.** Pass your puzzle through the four-slot grammar of §7.1.1 and write **one sentence** that names: the **outcome $y$** (the number that would go in the $y$ column, for many units — not a mood), the **treatment or key variation $D$** (the thing whose effect you want, which must *vary* across units), the **unit** (whose outcome — firm, person, county, token, patent), and the **window** (over what period). A sentence missing any of the four is not yet a refined question. Below the sentence, list the four slots explicitly as a short labeled list so the grader can see you filled each one.

**(b) (12 pts — 4 per candidate) The directional hypothesis with $H_0$.** Commit to a **sign**. Write the alternative $H_1$ as a signed prediction (up / down / larger-for-group-A) and the null $H_0$ as the boring "no effect / no difference" it is tested against. This is the move that makes the question falsifiable — "the moment Devon can be wrong" (§7.1.1). Do **not** attach a magnitude; a direction is required, a number is forbidden (you have no data). One sentence per hypothesis.

**(c) (12 pts — 4 per candidate) The identifying variation.** Run the Weeks 3–4 catalog *backwards* (§7.1.3): name *where in the world that generates your data* there is variation in $D$ plausibly unrelated to the confounders you fear, and name the resulting **design** — a sharp rule/cutoff (RD, Ch 4.3), a dated policy/shock hitting some units (DiD, Ch 4.1), a timestamped natural event (event study, Ch 4.2), or — only if you can defend it in one sentence — a found/built instrument (IV/shift-share, Ch 3.4–3.5). If your treatment varies for reasons hopelessly tangled with the outcome and you have no cutoff, date, event, or clean instrument, say so honestly and label the candidate **descriptive** — that is allowed and for a first project often wise (§7.1.3); what is forbidden is a correlation dressed in causal language. State the design in one sentence and the source of variation in one more.

**(d) (4 pts — total, not per candidate) The CONVENTIONS §4 spec line, for your strongest candidate only.** For whichever of the three you currently like best, write the full seven-field spec sentence: **outcome · treatment/key regressor · controls · fixed effects · clustering · sample · identifying assumption (one sentence).** Every field must be filled — a blank field is the gap an audience finds in Phase 2, which is exactly why `spec_line(...)` in `nb7.1` raises a `ValueError` on any empty field. (You may, and are encouraged to, generate this by calling `spec_line(...)`; paste its output.)

---

## Problem 2 — Score and rank all three on the rubric (25 points)

Now the §7.1.7 rubric earns its keep. Score each of your three candidates on the five dimensions, **0–2 points each**, and assemble the ranking. The dimensions and anchors, reproduced so you grade against them and not from memory:

| Dimension | 0 — fatal | 1 — workable | 2 — strong |
|---|---|---|---|
| **Falsifiable?** | A mood; no direction. | A direction, vaguely stated. | A sharp signed hypothesis with $H_0$. |
| **So what / who cares?** | No one acts on either answer. | A niche audience cares. | A real conversation cares; both answers matter. |
| **Novel?** | Re-run of a known result, same data. | New setting or period for a known idea. | New data, outcome, or identification. |
| **Identifiable?** | Pure correlation dressed as causal. | Descriptive, honestly labeled. | A real design (RD/DiD/event/IV) from Weeks 3–4. |
| **Feasible in 5 weeks?** | Data unavailable or out of scope. | Data obtainable; scope tight but real. | Data in hand by Ch 7.2; one clean question. |

**(a) (15 pts — 5 per candidate) The scored table.** For each candidate, give the five sub-scores **with a one-clause justification per dimension** — not just the number, the *reason* for the number ("Novel = 1: new period, but the disaster→insurance link itself is studied"). A bare number with no justification earns roughly half credit on that dimension, because the justification is the judgment we are grading. Present the three candidates as a single table (rows = candidates, columns = the five dimensions + total), the same shape `rank_ideas(...)` produces.

**(b) (6 pts) The verdict and the veto.** State each candidate's **total /10** and its **verdict**, applying the rule exactly as `nb7.1` encodes it: a solid project is **≥ 7 with no zeros**; **4–6** is "salvage by narrowing"; and — non-negotiable — **any 0 on *Identifiable?* or *Feasible?* is a veto**, sending the idea to the bottom *regardless of its total*. If one of your candidates scores, say, an 8 but earns `feasible = 0`, it must rank below a clean 5. State explicitly whether any veto fired and on which dimension. (If none of your three triggers a veto, you have not stress-tested hard enough — see Problem 3(c).)

**(c) (4 pts) Read the ranking like the chapter does.** In two or three sentences, say what the ranking *tells* you: which idea is the model project and why, which is the runner-up and what single point it lost, and — if a veto fired — why "the rubric is doing its job killing an infeasible idea early" beats letting a tall-but-dead idea waste a week of data work. If your top total and your top *rank* disagree because of the veto, name that explicitly; that disagreement is the whole point of the veto.

---

## Problem 3 — Select one, justify it, and name the reserve (20 points)

A ranking is not a decision until you commit. This problem is the commit.

**(a) (10 pts) The selection justification.** Pick **one** candidate to carry into the rest of Week 7. Justify the choice in a short paragraph that does two things at once: (i) cites the **rubric** — why this idea's scores beat the alternatives', and specifically that it survives both vetoes (real identification, obtainable data); and (ii) walks the **four feasibility constraints of §7.1.4** for the winner — *data access* (can you have it in hand by the end of Ch 7.2, per the §7.1.6 map?), *scope* (is it the *smallest* version of the question that is still interesting — one outcome, one treatment, one sample?), *time and reproducibility* (does the five-week backward-from-Phase-2 arithmetic close?), and *your own skills* (can you defend this design line by line when the audience asks, or is it a fragile method you half-understand?). A justification that names only the total score and skips the four constraints earns at most half credit.

**(b) (6 pts) The runner-up in reserve.** Name which candidate you hold as the runner-up and state, in two sentences, the *condition* under which you would switch to it — typically "if the data for my top choice turns out not to be obtainable in Ch 7.2." A good researcher leaves the workshop "with one project locked and a runner-up in reserve" (§7.1, Your Turn); the reserve is your insurance against the data-access surprise that kills the most first projects.

**(c) (4 pts) Honest scoping of the winner.** State, in one or two sentences, the *one* "and" you are deliberately **cutting** from your winning question to keep scope tight — the heterogeneity split, the extra decade, the second outcome, the cross-country comparison you are *tempted* to add and are choosing not to (yet). The professional instinct is to "find the smallest version of the question that is still interesting, answer that cleanly, and only then add" (§7.1.4); show you are exercising it.

---

## Problem 4 — The dangerous confounder and the causal/descriptive line (10 points)

This is the honesty problem, and it is the one a sharp audience member will push on first.

**(a) (6 pts) The most dangerous confounder.** For your **selected** question, name the single most dangerous confounder your chosen design does **not** fully handle — the threat that, if real, would make your estimate something other than the effect you claim. Then state, in one or two sentences, *how your design addresses it as far as it can* (the tight event window and pre-trend check for an event study; the difference-in-differences sweeping out fixed unit characteristics plus a parallel-trends check for DiD; the local randomization at the threshold for RD) **and** what residual worry survives. Name the *threat* and the *design that addresses it*, exactly as CONVENTIONS §4 demands — no hand-wavy "this controls for endogeneity."

**(b) (4 pts) Causal or descriptive — and why that is allowed.** State plainly whether your selected project is making a **causal** claim or an honestly-labeled **descriptive** one. If causal, name the one identifying assumption that, if it fails, collapses the causal interpretation into a mere correlation. If descriptive, state the careful sentence you will use so you never overclaim ("here is how X behaves around Y, with no causal claim"), and note why a clean description of a new phenomenon is a real, survivable Phase 2 contribution. The forbidden move — the only one that loses full credit here — is a descriptive correlation dressed up in causal language (§7.1.3).

---

## Problem 5 — Data discipline and the leashed literature scan (5 points)

A short discipline pass, because the proposal is only as good as the data and the citations behind it.

**(a) (3 pts) Data access and reproducibility.** For your selected question, name the **specific dataset(s)** you will pull and which access path each one is: *open/free and downloadable now* (HMDA, NOAA storm events, FEMA declarations, FRED, USPTO PatentsView, on-chain APIs, `yfinance`) versus *licensed and read-only on GMU infrastructure* (CRSP, Compustat, Bloomberg — which per CONVENTIONS §5 you may use read-only on Hopper/WRDS, with a pinned snapshot date, never copied off). In one sentence, confirm your top choice rests on data you can actually have in hand by the end of Ch 7.2 — and if it secretly does not, that is a Problem 3 veto you missed.

**(b) (2 pts) The AI co-pilot on a leash.** State the one non-negotiable rule from §7.1.5 / Ch 6.5 you will follow when you use an LLM to scan the literature for "what's new": you treat it as a *suggestion engine for what to go verify*, and you **verify every single citation against a real index** (Google Scholar, the journal site, a DOI lookup) before it enters your proposal — because an LLM will hand you flawless-looking citations that do not exist, and you cannot tell which from the page. Name what you do with a claim you genuinely cannot verify (tag it `[CHECK]`, per CONVENTIONS §6, rather than let a fabrication stand).

---

## Submission checklist

Before you submit, confirm every box. A submission missing any of these is incomplete regardless of how good the kept idea is.

- [ ] **Three** genuinely distinct candidate questions, each with: a four-slot refined question, a signed $H_1$ + $H_0$, and a named identifying variation (or an honest "descriptive" label). *(Problem 1a–c)*
- [ ] A full **CONVENTIONS §4 spec line** — all seven fields filled — for your strongest candidate. *(Problem 1d)*
- [ ] A **scored table**: five dimensions × 0–2 for all three candidates, each sub-score with a one-clause justification. *(Problem 2a)*
- [ ] Each candidate's **total /10 and verdict**, with the **veto** rule applied and stated. *(Problem 2b)*
- [ ] One **selected** question, justified against the rubric **and** the four §7.1.4 feasibility constraints, plus a named **runner-up** and the switch condition. *(Problem 3a–b)*
- [ ] The one "**and**" you are cutting to keep scope tight. *(Problem 3c)*
- [ ] The **most dangerous confounder** named, with the design's response and the residual worry; and a clear **causal-vs-descriptive** declaration. *(Problem 4)*
- [ ] **Data access** path for each dataset (open vs. licensed-read-only) and the **AI-leash citation-verification** rule. *(Problem 5)*
- [ ] **No fabricated empirical magnitudes** anywhere — directions yes, numbers no. Every cited paper is real (or tagged `[CHECK]`). *(throughout)*

---

*End of PS 7.1. When you have your three candidates scored, ranked, and one selected, check yourself against the model deliverable in `book/appendices/E-solutions-manual/E-w7-ps7.1-solutions.md` — it works three sibling candidates for one cast member end to end, shows the veto sending a tall idea to the bottom, and justifies the selection against both the rubric and the four feasibility constraints. The single locked spec you produce here is the input to everything that follows: Ch 7.2 turns it into acquired data and a data card, Ch 7.3 freezes it into a pre-analysis plan, Ch 7.4 builds the dataset, and Ch 7.5 makes you defend the identification in a memo. Get this sentence right and the project almost runs itself.*
