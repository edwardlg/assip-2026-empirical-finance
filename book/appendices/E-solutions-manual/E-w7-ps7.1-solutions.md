# Model Deliverable — PS 7.1 (Three Candidate Questions, Scored)

**Problem set:** `book/weeks/week-07/ps7.1.md` (PS 7.1, Week 7).
**Chapter:** Ch 7.1 — Idea-Generation Workshop (the puzzle→falsifiable-hypothesis grammar §7.1.1, the *so what / who cares / what's new* filter §7.1.2, the design catalog run backwards §7.1.3, the four feasibility constraints §7.1.4, the leashed AI lit scan §7.1.5, and the five-dimension feasibility/novelty rubric with veto §7.1.7).

This is a **model deliverable**, not a key with one right answer. PS 7.1 is a research-scaffolding assignment: there is no number to recover and no single correct question. What follows is one worked submission at the A level — three sibling candidate questions for **Priya** (climate risk / insurance, per the CONVENTIONS §2 cast), each sharpened, scored on the rubric, and either kept or killed, ending with one locked choice justified against both the rubric *and* the four feasibility constraints. It is written to show students the *standard* their own three candidates should meet, in the voice and discipline the chapter built. Instructor grading notes follow the worked answer.

A second model exists implicitly in the chapter and notebook for **Devon** (the stablecoin-depeg event study, scored a clean 10/10 in `nb7.1`); we work Priya here so the model covers a different design family (difference-in-differences and regression discontinuity rather than an event study) and so the three candidates are genuine *siblings* in one topic — which is the harder, more instructive case, because the rubric has to discriminate among three ideas that all sound reasonable.

**On the numbers.** Consistent with the assignment, this deliverable contains **no fabricated empirical magnitudes** — no effect sizes, coefficients, or t-statistics. The candidates are proposals. Directions (hypotheses with a sign) are stated; quantified predictions are not, because Priya has not pulled any data yet. Datasets named are all real and obtainable (NOAA storm events, FEMA disaster declarations, FRED, plus state insurance-department filings); no specific paper magnitude is cited as fact.

---

## The shared puzzle

Priya's recurring interest since Week 1 is **climate risk in insurance**. Her raw puzzle, the mood she starts from: *"Insurers are fleeing wildfire and hurricane country — and the people left behind are paying for it."* That is a feeling that something is interesting; it makes no prediction and nothing could refute it, so it is not yet research (§7.1.1). She generates three different *researchable* angles on it and runs each through the machine.

---

## Problem 1 — Three candidate questions, fully specified (40 points)

### Candidate A — Disaster declarations and the price of homeowner insurance (DiD)

**(a) Refined question (four-slot grammar).** *Do U.S. counties that receive a federally declared major disaster see homeowner-insurance costs rise faster than comparable counties that were not hit, in the years after the declaration?*

- **Outcome $y$:** a county-level homeowner-insurance cost proxy (a FRED/CPI insurance series or a state-filed premium index), measured per county-year.
- **Treatment $D$:** receiving a FEMA major-disaster declaration in a given year — it *varies* because some counties get one in a given year and comparable others do not.
- **Unit:** U.S. county (× year).
- **Window:** annual, 2010–2023.

**(b) Directional hypothesis with $H_0$.**
- $H_1$ (signed): insurance cost grows **faster** in disaster-hit counties in the years *after* the declaration than in comparable un-hit counties.
- $H_0$: cost grows in **parallel** — no post-declaration difference between hit and un-hit counties.

(No magnitude is stated: Priya predicts the *sign* of the post-event gap, not its size, because she has run nothing.)

**(c) Identifying variation.** **Difference-in-differences** (Ch 4.1). The source of variation is the *timing* of a FEMA major-disaster declaration: treated counties get a dated treatment, comparable un-hit counties form the control, and the *difference in differences* sweeps out fixed county characteristics (coastal, fire-prone) that would otherwise confound a raw before/after. The threat — that disaster-prone counties differ systematically from safe ones — is named and addressed by the design (county fixed effects absorb the level difference) plus a parallel-trends check on pre-declaration cost growth.

### Candidate B — A regulatory rate-filing threshold and approval of insurer rate hikes (RD)

**(a) Refined question (four-slot grammar).** *Among insurer rate-increase requests filed with a state insurance department, are requests just above the regulator's "prior-approval review" size threshold less likely to be approved as filed than requests just below it?*

- **Outcome $y$:** whether a filed rate-increase request is approved as filed (0/1), per filing.
- **Treatment $D$:** the requested increase crossing the regulatory review threshold (e.g., a state rule that increases above $X\%$ trigger a stricter prior-approval review) — it *varies* sharply at the cutoff.
- **Unit:** an individual insurer rate filing.
- **Window:** filings over roughly 2015–2023 in states with a sharp, published threshold.

**(b) Directional hypothesis with $H_0$.**
- $H_1$ (signed): filings just **above** the threshold are **less** likely to be approved as filed than otherwise-similar filings just **below** it.
- $H_0$: approval rates are continuous through the threshold — no jump.

**(c) Identifying variation.** **Regression discontinuity** (Ch 4.3). The source of variation is the *sharp rule*: filings landing just above versus just below a published percentage cutoff are plausibly similar in every way except that the larger one triggers the stricter review, so the cutoff "randomizes for you" locally. The threat — that insurers bunch their requests just below the threshold to dodge review (manipulation of the running variable) — is named and addressed by a density check at the cutoff (a McCrary-style test) and by reading only the *local* discontinuity, not a global trend.

### Candidate C — Do people in risky areas "feel" more exposed to climate risk? (descriptive / weak)

**(a) Refined question (four-slot grammar).** *Do homeowners in high-disaster-risk areas report greater concern about climate risk, and does that concern track their insurance behavior?*

- **Outcome $y$:** self-reported climate-risk concern (a survey scale).
- **Treatment $D$:** living in a high-risk area — but this does not *vary* in a way Priya can manipulate or instrument; it is a characteristic of where people already chose to live.
- **Unit:** survey respondent.
- **Window:** whatever a single cross-sectional survey covers.

**(b) Directional hypothesis with $H_0$.**
- $H_1$ (signed): respondents in higher-risk areas report **higher** climate-risk concern.
- $H_0$: concern does not differ by area risk.

**(c) Identifying variation.** **None — this is at best descriptive, and Priya labels it so honestly.** There is no cutoff, no dated policy, no clean event, and no defensible instrument: people select into where they live for reasons (income, family, job) tangled with both risk exposure and climate attitudes, so any "effect of risk on concern" is hopelessly confounded by selection. Worse, the underlying survey microdata Priya would need (linking individual concern to geocoded risk and insurance choices) is not something she can obtain free in five weeks. She writes it down precisely so the rubric can kill it rather than letting it lurk as a tempting-but-fatal option.

**(d) CONVENTIONS §4 spec line — for the strongest candidate (A).** Generated with `spec_line(...)` from `nb7.1`:

> **outcome:** county homeowner insurance-cost proxy (FRED/CPI insurance series or state-filed premium index) · **treatment:** FEMA major-disaster declaration (dated) · **controls:** (swept by fixed effects; add county-year covariates such as population and median income if available) · **fixed effects:** county + year · **clustering:** by county · **sample:** U.S. counties, 2010–2023 (NOAA storm events + FEMA declarations + FRED)
> **identifying assumption:** absent the disaster, hit and un-hit counties' insurance costs would have trended in parallel.

(All seven fields are filled; `spec_line` would raise `ValueError` on any blank one — the discipline device working as intended.)

---

## Problem 2 — Score and rank all three on the rubric (25 points)

### (a) The scored table, with a justification per cell

**Candidate A — Disaster DiD.**
- *Falsifiable? = 2.* A sharp signed hypothesis (faster post-event growth) with an explicit parallel-trends $H_0$ — Priya can be wrong.
- *So what / who cares? = 2.* Both answers matter (rising costs → housing-affordability and insurer-exit regulation; no gap → reassuring null), and a fast-growing climate-finance conversation reads it.
- *Novel? = 2.* The recent surge in billion-dollar disasters is a *new period*, and the county-level NOAA/FEMA/FRED linkage is a *new combination* — the new-data/new-period flavor of novelty.
- *Identifiable? = 2.* A real Weeks 3–4 design (DiD with a dated treatment, county + year fixed effects, parallel-trends check).
- *Feasible? = 2.* All three datasets are open and downloadable now; one outcome, one treatment, one sample — in hand by the end of Ch 7.2.

**Candidate B — Regulatory-threshold RD.**
- *Falsifiable? = 2.* Sharp signed hypothesis (lower approval just above the cutoff) with a continuity $H_0$.
- *So what / who cares? = 2.* Regulators and insurers both act on whether the review threshold actually bites; a live insurance-regulation conversation.
- *Novel? = 2.* A clean RD on regulatory rate-filing approval is a *new identification* angle on insurer pricing, not a re-run.
- *Identifiable? = 2.* A genuine RD design, with a density/manipulation check at the cutoff.
- *Feasible? = 1.* Honest downgrade: state insurance-department rate filings exist but are scattered across state portals (often as PDFs via SERFF-style systems), with no single clean download. The data is *obtainable* but the cleaning is heavy and the sample (filings in states with a sharp, published threshold) may be thin — scope tight but real, not "in hand by Ch 7.2." This is the constraint that separates B from A.

**Candidate C — Risk-perception survey (descriptive).**
- *Falsifiable? = 1.* A direction is stated, but it is a vague cross-sectional correlation, not a sharp design-backed prediction.
- *So what / who cares? = 1.* A niche audience (some risk-communication researchers); neither answer changes a regulator's or insurer's decision much.
- *Novel? = 1.* Risk perception vs. exposure is well-trodden survey territory — at best a new setting for a known idea.
- *Identifiable? = 0.* **Veto.** Pure selection-driven correlation dressed as a relationship — people choose where to live; there is no cutoff, event, policy date, or clean instrument. This is exactly the §7.1.3 forbidden case.
- *Feasible? = 0.* **Veto.** The linked individual-level survey microdata is not obtainable free in five weeks.

| Rank | Candidate | Falsifiable | So-what | Novel | Identifiable | Feasible | Total | Vetoed? | Verdict |
|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| 1 | **A — Disaster DiD** | 2 | 2 | 2 | 2 | 2 | **10** | No | KEEP (≥7, no veto) |
| 2 | **B — Threshold RD** | 2 | 2 | 2 | 2 | 1 | **9** | No | KEEP (≥7, no veto) |
| 3 | **C — Risk survey** | 1 | 1 | 1 | 0 | 0 | **3** | **Yes** | VETOED (0 on identifiable, feasible) |

(This is exactly the table `rank_ideas([Idea("A",2,2,2,2,2), Idea("B",2,2,2,2,1), Idea("C",1,1,1,0,0)])` produces: A and B sort by total above the vetoed C, which sinks regardless. Here C's total of 3 is already low, so the veto and the sum agree — but see the grading note below for the more instructive case where they *disagree*.)

### (b) Verdict and the veto

- **Candidate A: total 10/10, no veto → KEEP.** The model project.
- **Candidate B: total 9/10, no veto → KEEP.** A strong runner-up, docked only on feasibility.
- **Candidate C: total 3/10, vetoed on *both* Identifiable and Feasible → DROP.** Two vetoes fire. Even had Priya scored it more generously on the first three dimensions, the zeros on Identifiable and Feasible would send it to the bottom on their own. The rubric is a checklist with veto power, not a sum to maximize, and C fails the two checks that cannot be waived.

### (c) Reading the ranking

The ranking says the **disaster DiD (A) is the model project**: it is the only candidate that scores a perfect 10, surviving both vetoes on genuinely open data with a design Priya already met in her own Chapter 4.1. The **threshold RD (B) is the runner-up**, and it lost its single point on exactly the right dimension — *feasibility*, not idea quality. B is arguably the *more original* identification, which is a useful lesson: the best *idea* is not always the best *project*, because a five-week deadline weights feasibility heavily. The **survey question (C) is correctly killed** — and this is the rubric doing its job, because C is the kind of plausible-sounding idea that would quietly eat a week of fruitless data hunting and then collapse under the first "but isn't that just selection?" question in Phase 2. Better to kill it on paper today.

---

## Problem 3 — Select one, justify it, and name the reserve (20 points)

### (a) Selection justification — Candidate A (Disaster DiD)

Priya selects the **disaster-declaration DiD**. By the rubric, it is the only perfect 10 and it survives both vetoes, where the survey was vetoed twice and the RD lost a feasibility point. Walking the four §7.1.4 constraints for the winner:

- **Data access.** NOAA storm events, FEMA disaster declarations, and FRED insurance-cost series are all *open, free, and downloadable now* — no license, no portal-scraping, no approval queue. Per the §7.1.6 map she can have all three in hand by the end of Ch 7.2, which is the bar for a `feasible = 2`.
- **Scope.** It is the *smallest interesting version*: one outcome (county insurance cost), one treatment (the FEMA declaration), one sample (U.S. counties, 2010–2023). She resists widening it (see (c)).
- **Time and reproducibility.** The backward-from-Phase-2 arithmetic closes: a county panel built from three open sources is a one-to-two-week cleaning job (Ch 7.4), leaving room for the DiD and a parallel-trends check before the presentation. Everything runs from public files on a laptop — no licensed data to keep read-only on GMU infrastructure, so the §5 reproducibility constraint is trivially satisfied.
- **Own skills.** Priya can defend a difference-in-differences *line by line* — she built one in Chapter 4.1 and knows the parallel-trends assumption, the fixed-effects logic, and the clustered standard errors cold. By contrast, the RD (B) would force her to defend a density/manipulation test and a bandwidth choice she is shakier on, under audience questioning. "A clean difference-in-differences you fully understand beats a fragile structural model you half-understand" (§7.1.4).

### (b) Runner-up in reserve

The **threshold RD (Candidate B)** is the reserve. The switch condition is concrete: *if, in Ch 7.2, the county insurance-cost series turns out to be too coarse or too gappy to support a credible county-year panel* (FRED/CPI insurance coverage is national/regional, and a clean county-level premium index may not exist for free), Priya switches to B and pays the higher data-cleaning cost on state rate filings instead. Holding a scored, specified runner-up is her insurance against the data-access surprise that kills most first projects (§7.1, *Your Turn*).

### (c) Honest scoping — the "and" she is cutting

The one "and" Priya is deliberately **cutting**: she is *not* going to split the effect by **disaster type** (hurricane vs. wildfire vs. flood) in this first pass, however tempting. That heterogeneity split would triple the data work (separate exposure measures per peril) and the ways the analysis can break, and it does not help until the *pooled* effect is nailed first. She locks the single pooled disaster→insurance-cost question, answers it cleanly, and only *then* — if time remains — adds the peril split as an extension. "You can always extend a tight project; you can rarely rescue a sprawling one" (§7.1.4).

---

## Problem 4 — The dangerous confounder and the causal/descriptive line (10 points)

### (a) Most dangerous confounder

For the selected DiD, the single most dangerous confounder is **a contemporaneous, hit-correlated shock that independently moves insurance costs** — concretely, a **state-level regulatory or reinsurance-market change that arrives around the same time as the disasters and disproportionately affects the disaster-hit counties** (e.g., a state allowing larger rate increases statewide just as the disasters cluster). If such a shock exists, the post-event cost jump in hit counties is *partly* the regulation, not the disaster, and Priya's DiD would over-attribute it to the disaster.

The design addresses this as far as it can: county fixed effects sweep out *fixed* differences between hit and safe counties, year fixed effects sweep out *national* shocks common to all counties, and a **parallel-trends check** on pre-declaration cost growth tests whether hit and un-hit counties were already diverging before the disaster (Chapter 4.1's central discipline). What *survives* is precisely a shock that is (i) not fixed, (ii) not national, and (iii) correlated with which counties got hit — a *state-by-time* shock concentrated in disaster-prone areas. Priya names this as the live threat and proposes to partially address it with state-by-year fixed effects (comparing hit vs. un-hit counties *within the same state and year*), while acknowledging that a within-state shock targeting only the hit counties would still leak through. This is the threat named and the design that addresses it, per CONVENTIONS §4 — not a hand-wave.

### (b) Causal or descriptive

The project makes a **causal** claim: that the FEMA declaration (the disaster) *causes* faster insurance-cost growth. The one identifying assumption that, if it fails, collapses the claim into a mere correlation is **parallel trends**: *absent the disaster, hit and un-hit counties' insurance costs would have trended in parallel.* If hit counties were already on a steeper cost trajectory before the disaster (because, say, insurers were repricing climate risk there regardless), then the post-event gap is not the disaster's effect and the causal reading fails. Priya commits to *showing* the pre-trends, not asserting them — and if the pre-trends are not parallel, she will retreat honestly to a *descriptive* framing ("here is how insurance costs co-move with disaster declarations, with no causal claim") rather than dress a failed-assumption correlation in causal language, which is the one forbidden move (§7.1.3).

---

## Problem 5 — Data discipline and the leashed literature scan (5 points)

### (a) Data access and reproducibility

The three datasets and their access paths:
- **NOAA Storm Events Database** — *open / free, downloadable now* (bulk CSV).
- **FEMA major-disaster declarations** — *open / free* (OpenFEMA API and bulk files).
- **FRED insurance-cost series (CPI insurance / premium index)** — *open / free* (FRED API or CSV).

All three are open; *none* is licensed, so there is no CRSP/Compustat/Bloomberg read-only-on-GMU constraint to manage here (CONVENTIONS §5 still applies the moment she touches anything licensed, but this project does not). She confirms her top choice rests on data she can have in hand by the end of Ch 7.2 — the one genuine risk is the *granularity* of the FRED insurance series (it may not exist cleanly at the county level), which is exactly why the RD runner-up is held in reserve and why this risk was surfaced, not buried.

### (b) The AI co-pilot on a leash

When Priya uses an LLM to scan for "what's new" in the climate-finance/insurance literature, the non-negotiable rule (§7.1.5 / Ch 6.5): she treats the model as a **suggestion engine for what to go verify**, never as the citation itself. She **verifies every single citation against a real index** — Google Scholar, the journal's own site, a DOI lookup — before any paper enters her proposal, because an LLM will produce author-list-title-year-journal citations in flawless format, some real and some pure invention, indistinguishable on the page. Any claim she genuinely cannot verify she tags **`[CHECK]`** (CONVENTIONS §6) and does not let stand as fact. She also refuses to cite any LLM-supplied *magnitude* ("disasters raised premiums by 30%") as a fact — that is a hypothesis to check against a primary source, never a citation.

---

## Instructor grading notes

**What an A submission demonstrates.** The point of PS 7.1 is *judgment*, not coverage. An A submission (1) produces three genuinely distinct, fully-specified candidates — each with a real four-slot question, a *signed* hypothesis with $H_0$, and an honest identification label; (2) scores them against the rubric *anchors*, not from gut feel, with a defensible justification per cell; (3) lets the **veto** do its work; and (4) selects on *both* the rubric and the four feasibility constraints, not on the raw total alone. The model above is deliberately built so the best *idea* (arguably the RD) is **not** the best *project* (the DiD), because feasibility binds — students who notice that distinction have understood §7.1.4.

**The veto is the most common grading flashpoint.** Watch for two errors. (i) **Keeping a vetoed idea because its total is high.** The canonical trap, and exactly what `nb7.1`'s self-checks guard: an idea scoring `falsifiable=2, so_what=2, novel=2, identifiable=2, feasible=0` totals **8** but is **VETOED** and must rank *below* a clean total-5 idea. If a student's chosen project carries a 0 on Identifiable or Feasible, that is a failing selection regardless of the rest of the submission — dock heavily. (ii) **Refusing to ever score a 0**, so no idea is ever vetoed. A portfolio of three all-survive ideas usually means the student did not stress-test; the assignment explicitly asks for at least one idea they suspect is weak (Problem 1). Award full credit only when the rubric has been used to *kill*, not just to rank.

**Forbidden moves (lose full credit on the relevant problem).**
- *Fabricated magnitudes.* Any effect size, coefficient, t-stat, or "the disaster raised premiums by X%" in a *proposal* is the §6.5 / CONVENTIONS §6 violation the assignment forbids. Directions are required; numbers are not yet earned. Zero the affected component.
- *Causal language on a descriptive design.* A candidate with no cutoff/event/policy/instrument that nonetheless claims "X *causes* Y" should score `identifiable = 0` and be vetoed; if the student instead scores it 2 and calls it causal, that is the central §7.1.3 error.
- *Fabricated citations.* Any paper cited to support novelty must be real and verifiable; an unverifiable claim must be tagged `[CHECK]`. A confidently-cited paper that does not exist is an automatic fail of Problem 5(b) and a teachable Ch 6.5 moment.

**Acceptable variation.** Students may use *any* cast member or their own genuine interest; any topic area is fine. The three candidates may share a topic (as Priya's do) or span three — both are acceptable as long as they are genuinely distinct questions. Designs other than DiD/RD are fine (an event study like Devon's, a portfolio sort like Sam's descriptive momentum question, an RD/matched comparison like Leah's patent question). What is *not* negotiable is the structure: three specified candidates, a justified scored table with the veto applied, and a selection defended on rubric *and* feasibility. Partial-credit rubric: Problem 1 (40) — 4 per candidate-component for 1a–c, 4 for the 1d spec line; Problem 2 (25) — 5 per scored candidate with justifications, 6 for verdict+veto, 4 for reading the ranking; Problem 3 (20) — 10 selection justification (half if the four constraints are skipped), 6 runner-up + switch condition, 4 the cut "and"; Problem 4 (10) — 6 confounder named with design response and residual worry, 4 causal/descriptive declaration; Problem 5 (5) — 3 data-access paths, 2 the AI-leash citation rule.

**Tie to the contract.** The scored table and verdicts mirror `nb7.1`'s `Idea`/`rank_ideas`/`spec_line` API exactly: five dimensions × 0–2, total /10, veto on Identifiable/Feasible, verdict bands (≥7 KEEP / 4–6 SALVAGE / vetoed → bottom), and the seven-field `spec_line`. A student who built their three candidates *as* `Idea(...)` rows and ran `rank_ideas` has used the intended workflow and should produce a table identical in shape to the one above. No empirical magnitudes are fabricated anywhere in this model; all datasets named (NOAA, FEMA, FRED, state insurance-department filings) are real and access-classified.
