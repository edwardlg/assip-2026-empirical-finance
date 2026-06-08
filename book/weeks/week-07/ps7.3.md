# PS 7.3 — Write and Register a Complete Pre-Analysis Plan for *Your* Project

**Course:** 8-Week Empirical Finance Camp · Week 7 · Problem Set 7.3
**Covers:** Ch 7.3 (The Pre-Analysis Plan, short form, Olken 2015), with the empirical-spec discipline of CONVENTIONS §4, the multiple-testing arithmetic of Week 1 (§1.5.10), and the freeze-the-rubric discipline of Week 6 (§6.5). Feeds Lab 7 ("Your Data, Reproducibly") and the Week 7 assessment.
**Paper:** Olken, B. A. (2015). *Promises and Perils of Pre-Analysis Plans.* Journal of Economic Perspectives, 29(3), 61–80.
**What you turn in:** a single Markdown file, `PAP.md`, committed to your project repository and **time-stamped with a `pap-filed` Git tag**, plus a short reflection. This is not a problem-solving sheet with one right answer — it is a **scaffolding assignment** that produces a real deliverable for your own project. Every camper's PAP is different because every camper's project is different.

**Total: 100 points.** Point values are stated per component and map one-to-one onto the research-design rubric Appendix E grades against. A vague PAP loses points the same way a vague specification loses a referee: not because it is *wrong* but because it *commits to nothing*, and a plan that commits to nothing protects no one (Ch 7.3 §7.3.5, "Olken's perils").

**The one rule that makes this assignment mean anything.** You must write and **tag** your PAP *before* you run a single confirmatory regression on your confirmation data. The entire value of the exercise — the entire value of a PAP — collapses the instant you peek at your outcomes first and then back-fill a plan to match. If your data already exist (HMDA, CRSP, EDGAR, on-chain — most camp projects), you do this with a **hold-out split**: you may explore freely on a small exploration set, but the confirmation set stays untouched until after the tag. If your study is genuinely prospective (a sample window that has not happened yet), the future is your hold-out and no split is needed. Either way: **register before you peek.** A PAP filed after the peek is, in Olken's phrase, a peril wearing the costume of a promise.

**A note on the difficulty curve.** Component 1 is the warm-up that is secretly the hardest: stating *directional* hypotheses you are willing to be wrong about. Components 2–3 are the technical heart — one primary specification in full seven-slot CONVENTIONS §4 form, and a multiple-testing plan that quarantines the garden of forking paths with a primary/secondary split and Benjamini–Hochberg FDR for your families. Component 4 (falsification) is the one beginners skip and Olken would not let you skip. Component 5 (planned robustness) converts the forks you might have fished in into checks you promise to report either way. Component 6 is the registration mechanism itself — the tag, the hold-out, the deviation log — which is *when* and *how* you commit, and is what separates a plan from a wish.

Throughout, the **model deliverable** in `book/appendices/E-solutions-manual/E-w7-ps7.3-solutions.md` shows the A-grade standard on **Maya's** HMDA fair-lending project (the worked example from Ch 7.3 §7.3.4 and the planted design in nb7.5). Read it *after* you draft your own — not before — so it calibrates your standard without dictating your project. Your PAP should be *as precise as Maya's about your own question*, not a paraphrase of hers.

**Tools you already have.** `nb7.3` (`notebooks/week-07/nb7.3-pap-companion-power-calc.ipynb`) walks the five components and, crucially, runs the **power calculation for your design** and a **Benjamini–Hochberg** routine, then emits a filled-in PAP template you tag as `pap-filed`. Use it. The power calc is not optional ornament: it tells you, *before* you waste a confirmation run, whether your data are even capable of detecting the smallest effect you care about (Reflection prompt 3 of Ch 7.3).

---

## Component 1 — Directional hypotheses (15 points)

State your project's hypotheses as **numbered, falsifiable, directional sentences**. Not "X is related to Y" — that is a coin that lands heads on any nonzero coefficient — but "X *raises* Y" or "the gap is *smaller* for the treated group," with the sign written down.

**(a) (6 pts)** Write **H1**, your *primary* hypothesis — the single claim the whole project lives or dies on — as one directional sentence, and state the sign of the coefficient it predicts (e.g., $\beta_1 > 0$). Then write one sentence justifying *why* you have a directional prior: name the literature, the theory, or the institutional fact that told you the direction *before* you saw your data. (Recall from Ch 7.3 §7.3.2 / Week 1: you may only claim a one-sided test if the direction came from the science, and the PAP is your evidence that it did. If you genuinely have no prior, say so and commit to a two-sided test — honest, but it costs you $1.96$ instead of $1.65$.)

**(b) (5 pts)** Write **H2** and (optionally) **H3** as your *secondary* hypotheses — claims that would enrich the story but whose failure would not sink the paper. State each directionally where you have a prior; where you genuinely do not (e.g., a subgroup-heterogeneity question with no sign expectation), say "no directional prior; two-sided" explicitly. Number them, because the numbers reappear in Component 3.

**(c) (4 pts)** In two or three sentences, explain *why deciding which hypothesis is primary, in advance, is itself a multiplicity control* — i.e., why promoting one test to "primary" shrinks the multiple-testing problem for your headline from "however many things I tried" to one (Ch 7.3 §7.3.3, the cheapest and most honest defense). This sentence is your insurance against the temptation, six hours from now, to crown whichever coefficient came out starred.

---

## Component 2 — The primary specification, in CONVENTIONS §4 seven-slot form (30 points)

This is the heart of the PAP. Write out the **single regression that tests H1** — the one number that, if it broke, sinks the paper — naming explicitly **all seven slots** of the empirical-spec discipline (CONVENTIONS §4). Write the model equation in the notation of CONVENTIONS §3. Vagueness in *any* slot is the peril of §7.3.5 ("a plan that does not name the outcome to a variable name, the clustering level, and the exact sample is not a plan"), and is graded as such.

**(a) (4 pts) The equation.** Write your primary specification as a linear model in CONVENTIONS §3 notation — e.g.
$$y_{i} = \beta_0 + \beta_1\,D_{i} + \mathbf{x}_i'\boldsymbol{\gamma} + (\text{fixed effects}) + \varepsilon_i,$$
naming which symbol is the **single coefficient** that answers H1. Writing the equation is not ornament: it pins down, unambiguously, which number is the test.

**(b) (18 pts, 3 each) The seven slots.** State each of the following to the level of a *variable name and a decision*, not a hand-wave:
1. **Outcome** — the exact dependent variable, defined to a variable name (e.g., "`denied` = 1 if HMDA `action_taken` ∈ {3, 7}, else 0"), not the concept ("denial").
2. **Treatment / key regressor** — the one coefficient you will read off the table to answer H1.
3. **Controls** — the legitimate covariates you hold fixed, *named*, with one phrase each on *why it belongs*. **Crucially**, name at least one variable you are *deliberately NOT controlling for because it sits on the causal pathway* (the Mentor 4 over-controlling trap) and say why conditioning on it would regress away your effect. (If your design genuinely has no pathway-variable to exclude, say so and explain why.)
4. **Fixed effects** — which absorbing dummies, and what comparison each one forces (e.g., "lender FE → within-lender comparison; tract FE → within-neighborhood comparison").
5. **Clustering** — the level the standard errors are clustered at, *chosen now and justified*. Name the mechanism that makes errors correlated at that level. (This is a notorious fork: choosing the clustering level *after* seeing which one gives significance is p-hacking on the standard error.)
6. **Sample** — the exact universe of rows: which years, units, geographies, purposes, and exclusions, with the row count you *expect* (you may state $N \approx$ [from exploration set] if you have estimated it there).
7. **Identifying assumption, in one sentence** — the single CONVENTIONS §4 sentence that, if true, makes your key coefficient the thing you claim it is. Name the threat it addresses; if your design only bounds the effect rather than identifying it cleanly, *say it is a bound* (e.g., Maya's missing credit score). You cannot write this sentence vaguely.

**(c) (8 pts) Self-audit of your spec.** In a short paragraph, identify the **two or three most dangerous forks** in your specification — the slots where, if you peeked at the result first, you would be most tempted to flip the choice toward your hypothesis (an outcome definition, a sample exclusion, a clustering level, a control, a prompt rubric if you are using an LLM label per Week 6). For each, state the one sentence in your PAP that nails it down. This is Reflection prompt 1 of Ch 7.3 made into a deliverable.

---

## Component 3 — The multiple-testing plan (20 points)

You will compute more than one number. The multiple-testing plan decides, *in advance*, how the army of tests is governed so your headline is not a lucky draw from a crowd (Ch 7.3 §7.3.3; Week 1 §1.5.10's $1 - 0.95^{20} \approx 0.64$).

**(a) (6 pts) Primary vs. secondary.** Declare, explicitly, that your H1 coefficient is *the* primary test, held to the strict $\alpha = 0.05$ and reported as the result. List every other quantity you will compute (interactions, subgroups, alternate outcomes, alternate years) and mark each **secondary** — reported, interesting, but explicitly *not* the confirmatory claim. Explain in one sentence why this single move retires most of the multiplicity problem for your headline.

**(b) (10 pts) Families and FDR.** Group your secondary tests into **pre-committed families** and state the correction for each. For any family of related tests (e.g., a gap measured across five income bands, or three applicant subgroups, or several event windows), commit to **Benjamini–Hochberg FDR control at 0.05 within that family**. Write the families out as a list, e.g.:
> Family A (primary): H1 alone, $\alpha = 0.05$, no correction (single primary test).
> Family B: {your secondary interaction(s)}, $\alpha = 0.05$.
> Family C (exploratory): {your subgroup/heterogeneity tests}, Benjamini–Hochberg FDR at 0.05 *within this family*; labeled exploratory regardless of outcome.

Then **demonstrate you can run BH by hand** on your own (or a stand-in) family: take $m$ p-values, sort them ascending $p_{(1)} \le \dots \le p_{(m)}$, find the largest rank $k$ with $p_{(k)} \le \frac{k}{m}\alpha$, and reject ranks $\le k$. Show the comparison table and state how many discoveries BH admits — and, in one sentence, why this is less brutal than Bonferroni's $\alpha/m$ on every test when the family has several genuine effects. (If you have not run any regressions yet — and you should not have, on the confirmation set — use a small illustrative set of p-values for the by-hand demonstration, clearly labeled illustrative, exactly as `nb7.3` does.)

**(c) (4 pts) The pre-commitment clause.** State, in one sentence, *why the families must be a pre-committed list* — i.e., why deciding after seeing the p-values which tests count as a "family" lets you shrink or grow the family until your favorite effect survives correction. This is the part the PAP exists to enforce.

---

## Component 4 — What would falsify you (15 points)

For each hypothesis, write the result that would make you **abandon** it — not "fail to confirm," *falsify*. Olken would not let you skip this; Popper's point dragged into finance is that a hypothesis no possible result could contradict is not a claim, it is a mood.

**(a) (8 pts) The falsification sentence for H1.** Write the exact **coefficient-and-confidence-interval pattern** that would force you to say "I was wrong." Phrase it, as in Ch 7.3 §7.3.2 (drawing on §1.5.8), to **distinguish a genuine refutation from a mere power failure**: a 95% CI that is *tight and brackets zero while excluding economically meaningful values* is informative absence (a refutation); a *wide* CI that merely includes zero is a power failure (inconclusive, not a refutation). State the *economically meaningful* threshold for your outcome in its own units (for Maya, a denial gap of, say, ≥ 2 percentage points; for you, the smallest effect a real person/firm/market would care about).

**(b) (4 pts) Falsification for your secondary hypotheses.** Briefly state the result that would falsify H2 (and H3 if you have it) — including, where relevant, a *wrong-signed* result (e.g., for Maya, an interaction that is positive rather than negative).

**(c) (3 pts) Would you actually report it?** In two or three sentences, answer honestly: if your H1 null came out as the tight-zero refutation you just described, *would you report it as your headline*, or would you keep looking? If your honest answer is "I'd keep looking," your PAP is not yet protecting you — name the fork you are still leaving open and close it. (This is Reflection prompt 2 of Ch 7.3; the single biggest cause of p-hacking is that researchers cannot stomach a null they did not pre-commit to believing.)

---

## Component 5 — Planned robustness (10 points)

**(a) (7 pts) The planned list.** List the robustness checks you *plan* to run, labeled **planned** to distinguish them from any post-hoc check you might add later. Aim for three to five concrete checks drawn from your own design's forks — e.g., an alternate clustering level, dropping an anomalous year/period, an alternate (continuous vs. binary) outcome, a sample restriction to the largest units, re-estimating on the full sample as a precision check. For each, name the fork it stress-tests in one phrase.

**(b) (3 pts) The report-either-way clause.** State the discipline explicitly: a planned robustness check is one whose result you commit to **reporting whichever way it comes out**. Write the sentence that obligates you — e.g., "If H1 holds in the main spec but evaporates under [alternate clustering / dropping year X], the PAP obligates me to say so." Robustness is a stress test you promised to report honestly, not a search for confirmation.

---

## Component 6 — Registration mechanism: hold-out, tagged commit, deviation log (10 points)

The five components are *what* you write; this component is *when* and *how* you commit — the mechanics that make the plan binding (Ch 7.3 §7.3.3).

**(a) (4 pts) The hold-out (or prospective) design.** State how you separate exploratory from confirmatory data *mechanically*. If your data already exist: declare your **hold-out split** — e.g., 30% exploration / 70% confirmation, split on a *stable, pinned key* (a hash of a unit identifier, reproducible per CONVENTIONS §5), with the exact rule (e.g., `hash(loan_id) mod 10 < 3` → exploration). State that the primary specification runs **once** on the untouched confirmation set after the tag. If your study is prospective, state that the future window is your hold-out and explain why no split is needed.

**(b) (3 pts) The tagged commit.** State that you will register `PAP.md` as a **`pap-filed` Git tag** in your project repo — your time stamp — and explain in one sentence *why a tagged commit is a credible registration*: anyone can verify the PAP existed, in exactly this form, before the commits that contain your confirmatory results (the camp's analogue of OSF / AsPredicted / the AEA RCT Registry). Confirm that nb7.5 ("first-look regressions") stays **frozen until the PAP is filed**.

**(c) (3 pts) The deviation log.** State that you will keep a `DEVIATIONS.md` — a dated record of every departure from the plan, *what* changed, *why*, and **whether the change was prompted by seeing the outcome**. In two sentences, explain the crux (Olken's *perils*): a deviation forced by a mechanical reality (collinearity, a bug, a data-availability surprise) is innocent and noted; a deviation that happened *because you saw the coefficient and didn't like it* is exactly the p-hacking the PAP exists to prevent — and reclassifies that result as exploratory. The deviation log is the instrument that draws the confirmatory/exploratory line; it makes the PAP a baseline, not a prison.

---

## Submission checklist

Turn in **one file**, `PAP.md`, in your project repo, plus the reflection below. Before you tag, confirm:

- [ ] **H1 is directional and primary**, with a one-sentence justification of the prior; secondary hypotheses numbered (Component 1).
- [ ] **Primary specification names all seven CONVENTIONS §4 slots** — outcome (to a variable name), key regressor, controls (with one deliberately-excluded pathway variable named), fixed effects, clustering (justified), sample (with expected $N$), identifying assumption (one sentence, bound flagged if not clean) — plus the model equation (Component 2).
- [ ] **Self-audit names your 2–3 most dangerous forks** and the sentence that nails each down (Component 2c).
- [ ] **Multiple-testing plan** declares primary-vs-secondary, lists pre-committed families, assigns BH-FDR to each family, includes a by-hand BH demonstration, and states the pre-commitment clause (Component 3).
- [ ] **Falsification sentence for H1** distinguishes refutation from power failure and states the economically-meaningful threshold in the outcome's own units; secondary falsifications stated; the "would I actually report it?" honesty check answered (Component 4).
- [ ] **Planned robustness list** (3–5 checks) with the report-either-way clause (Component 5).
- [ ] **Registration mechanism**: hold-out split (pinned key) or prospective design; `pap-filed` tag plan; `DEVIATIONS.md` plan (Component 6).
- [ ] **`nb7.3` power calculation run for your design** — you know the $N$ your design needs to detect your smallest meaningful effect at 80% power, $\alpha = 0.05$, and whether your data clear that bar *before* you spend the confirmation run.
- [ ] **Voice and citation**: precise, no marketing voice, no emojis; Olken (2015) cited by name where you invoke the confirmatory/exploratory frame.
- [ ] **You have NOT looked at a single confirmatory coefficient.** If you have, say so in the deviation log and label the affected result exploratory — do not hide it.

**Reflection (ungraded but required, ~150 words).** Answer Ch 7.3 Reflection prompt 3 for *your* project: suppose `nb7.3`'s power calculation reveals that detecting the smallest effect you care about, at 80% power, would need substantially more sample than you have. What are your options *before* you run the confirmation regression — narrow the question, change the outcome, pool more data, or report a pre-registered bound — and why is "run it anyway and hope" the one option a pre-registered researcher has already foreclosed?

---

## How this is graded

Appendix E grades against the **research-design rubric**, with points mapped to the six components above. Two cross-cutting principles dominate the grade, both straight from Olken (2015):

1. **Precision beats hedging.** A slot named to a variable name and a decision earns full marks; a slot that says "appropriate controls and standard errors" earns near zero, because it is a PAP-shaped object that licenses every fork in the garden (§7.3.5). The skill we grade is the *commitment*, not the prose.
2. **Honesty beats confidence.** A PAP that pre-registers an imperfect design and *admits* the residual (the bound, the threat, the power shortfall) scores *higher* than one that pretends the design is clean. Pre-registration governs the **honesty** of your inference (did you test or did you search?), not its **validity** (is the test the right one?) — validity is the job of the identification memo you write next in Ch 7.5. A PAP and an ID memo are complementary: one promises you did not fish, the other argues the pond is the right pond. You need both.

---

*End of PS 7.3. When your `PAP.md` is drafted, check your standard against the model deliverable in `book/appendices/E-solutions-manual/E-w7-ps7.3-solutions.md` — a complete A-grade short-PAP for Maya's HMDA fair-lending study, with instructor grading notes keyed to the rubric. Then run `nb7.3` end-to-end, paste its emitted template and power summary into `PAP.md`, commit, and `git tag pap-filed`. The tag is the moment your project stops being a hope and becomes a falsifiable, registered design — and the only person it is really protecting you from is yourself, eight hours and thirty-two specifications from now (Ch 7.3 §7.3.4). This PAP, filed alongside the identification memo of Ch 7.5 as your Lab 7 deliverable, is the spine of a project that could survive a hostile referee.*
