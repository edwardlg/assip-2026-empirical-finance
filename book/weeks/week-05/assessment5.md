# Week 5 Assessment — Reading the Frontier I

This is the end-of-week assessment for Week 5. Weeks 1–4 handed you a toolkit — OLS and its
assumptions, robust and clustered standard errors, omitted-variable bias, instrumental variables,
difference-in-differences, regression discontinuity — and taught you to *run* it. This week taught
you something harder: to *read* it in someone else's hands. Every chapter applied one fixed
procedure, the seven-part Reader's-Guide anatomy from the reading pack, to one famous paper —
Fama–French (1992) and (1993), Jegadeesh–Titman (1993), Petersen (2009), Bertrand–Duflo–Mullainathan
(2004). The assessment asks you to do it once more, alone, on a paper you have never seen.

The assessment has three parts. **Part A** is the centerpiece: you take an unseen empirical-finance
paper that uses methods from Weeks 1–4 and produce your own four-page Reader's Guide on it, applying
the same seven boxes — research question, identification strategy, data, table-by-table reading
order, what's clever, what's vulnerable, and three replication exercises. **Part B** is a short
conceptual section, four quick items that test the reading reflexes in isolation: spot the headline
table, separate identification from estimation, flag a vulnerable claim, name a robustness check.
**Part C** is the analytic rubric with explicit point totals, followed by an instructor answer key
and a worked example of a strong versus a weak "identifying assumption in one sentence."

**Total: 100 points.** Part A = 70, Part B = 20, presentation and intellectual honesty woven through
both = 10. This is take-home: budget an evening to read the paper the professional way (tables first,
prose last) and a second sitting to write. The Guide is the seed of your Week 7–8 capstone, so treat
it as a rehearsal for defending tables you will one day build yourself.

Throughout, hold every author to CONVENTIONS §4: every specification gets named explicitly —
**outcome · treatment/key regressor · controls · fixed effects · clustering · sample · identifying
assumption in one sentence** — with no hand-wavy appeals to "controlling for endogeneity." The skill
is the same one we hold *ourselves* to, pointed outward.

---

## Part A — Write a four-page Reader's Guide on an unseen paper (70 points)

### A.0 The paper

Your instructor will hand you a paper, or you may choose one from the candidate **types** below and
clear it with your mentor. The paper must (i) be empirical — it estimates something from data, it
does not merely theorize; (ii) use a design you met in Weeks 1–4 — a portfolio sort, a panel
regression with fixed effects and clustered standard errors, an instrumental-variables design, a
difference-in-differences, or a regression discontinuity; and (iii) be one you have **not** read
before this assessment. A short paper (15–35 pages) with a clear headline table is ideal. Do not pick
a pure theory paper, a literature survey, or a structural-estimation paper whose machinery is past
Week 4 — you cannot grade an identification strategy you were never taught.

**Six candidate paper types** (pick a *type*, then find a real paper of that type with your mentor —
we deliberately do not hand you a citation, because finding the paper is part of the exercise):

1. **A difference-in-differences on a financial regulation.** A rule that switched on in some places
   or for some firms and not others — a state-level lending law, a disclosure mandate, a change to
   deposit-insurance limits, a short-sale ban applied to some stocks. Outcome: lending, prices,
   default, risk-taking. The identifying assumption will be parallel trends; the chief threat,
   selection into who got the rule and when.
2. **An instrumental-variables paper in corporate finance or banking.** Something instruments an
   endogenous regressor — leverage instrumented by tax-code variation, credit supply instrumented by
   a bank's pre-existing exposure to a shock, financial development instrumented by legal origin. The
   identifying assumption is the exclusion restriction; the chief threat, that the instrument affects
   the outcome through a second channel.
3. **A regression discontinuity at an index threshold.** The Russell 1000/2000 reconstitution cutoff,
   a credit-score approval line, an S&P 500 addition rule, a covenant trigger, an analyst-coverage
   threshold. Outcome: ownership, voting, returns, financing. Identifying assumption: continuity of
   potential outcomes at the cutoff; chief threat, sorting/manipulation or a compound treatment that
   the same cutoff also triggers.
4. **A factor / cross-sectional asset-pricing paper.** A paper proposing a new return predictor or
   anomaly via portfolio sorts and Fama–MacBeth or time-series factor regressions — a Week 5 paper's
   close cousin. "Identification" lives in the portfolio construction and the risk adjustment; the
   chief threat is that the premium is compensation for an omitted risk factor, or a data-mining
   artifact, or driven by tiny illiquid stocks.
5. **A panel fixed-effects study with clustered standard errors.** Firm-year or state-year panels
   on, say, climate risk and insurance pricing, BNPL adoption and household delinquency, or fair-
   lending outcomes. Identification is "within-unit, after absorbing fixed effects"; the chief threats
   are time-varying confounders the fixed effects do not absorb, and standard errors clustered at the
   wrong level (the Petersen/BDM disease).
6. **An event study around a financial shock or announcement.** Abnormal returns around an
   earnings surprise, a regulatory announcement, an index reconstitution, a crypto-protocol change.
   Identification rests on the event being unanticipated and the estimation window being clean; the
   chief threat is confounding events in the window and cross-sectional correlation in abnormal
   returns.

### A.1 The seven-part Reader's Guide (60 points)

Write roughly four pages — about 1,200–1,800 words — organized into the seven numbered boxes, in
order. Read the paper the professional way before you write a word: abstract once, then straight to
the **tables and figures**, find the headline result and read its sign / magnitude / t-statistic /
sample size *off the table itself*, then the identification and data sections, then robustness, and
only last the introduction. The boxes:

**(1) Research question (5 pts).** One sentence, plain English, ending in a question mark. Name the
**outcome** and the **key right-hand-side variable** explicitly. "Does X predict / cause Y?" — not
"this paper studies Y."

**(2) Identification strategy (12 pts).** Name the design (sort, panel FE, IV, DiD, RD), then — the
single most important sentence in the Guide — **state the identifying assumption in one sentence**, in
the form "this estimate equals the true effect *as long as* ___." Then **name the chief threat to that
assumption**: the single most plausible thing that, if true, makes that sentence false, and say which
way it would bias the estimate. Distinguish, in a line, *identification* (the assumption that lets the
number mean what you want) from *estimation* (the regression machinery that produces the number).

**(3) Data (8 pts).** Unit of observation (firm-month? person? state-year?), sample period, source
(CRSP, Compustat, EDGAR, a survey, an exchange feed), and number of observations. List the sample
filters — "drops financial firms," "requires two years of prior data," "winsorizes at 1%" — because
filters are decisions and decisions are levers. Flag any look-ahead or survivorship trap you suspect,
even if the paper does not mention it.

**(4) Table-by-table reading order (10 pts).** Identify the **headline table** — the one that, if it
broke, would sink the paper — and name the one number in it that carries the result. Then give the
order in which a reader should look at the tables to absorb the argument fastest, labeling each as
*setup* (summary stats, an IV first stage), *headline*, or *defense* (robustness, placebo, alternative
specs), with one line on what each is *for*. Write the headline specification in the CONVENTIONS §4
format: outcome · key regressor · controls · fixed effects · clustering · sample · identifying
assumption.

**(5) What's clever (5 pts).** Name the one genuinely good idea — a construction, a comparison, a
dataset nobody had assembled, a way of turning an awkward problem into a clean one. One paragraph.

**(6) What's vulnerable (8 pts).** State the *single most threatening* alternative explanation for the
headline result, and the specific evidence that would settle it for or against. This must be
consistent with the chief threat you named in box (2), and it must be a real soft spot, not a generic
"correlation isn't causation."

**(7) Three replication exercises (12 pts).** Three concrete things a student could *do* on real data
on a laptop. Exactly one of each kind: (a) **reproduce** a specific number from the headline table —
name the table, the cell, and the data you would pull; (b) **stress** an assumption — re-run with
different controls, a different sample window, a different standard-error flavor (cluster differently,
add HAC), or a placebo; say what result would *break* the paper; (c) **extend** the idea to a new
setting — a new asset class, a more recent decade, a different country or market. Each must be
feasible with data the camp can actually reach (CRSP, Compustat, EDGAR, public APIs); "obtain
proprietary hedge-fund records" is not a feasible exercise.

### A.2 The two load-bearing sentences (10 points, scored inside A but called out separately)

Two sentences in your Guide carry disproportionate weight, and we grade them on their own:

- **The identifying assumption, in one sentence** (box 2). In the exact form "this estimate equals the
  true effect *as long as* ___," naming the specific condition for *this* paper's design — not the
  word "endogeneity," not "no confounders" in the abstract, but the concrete bet this paper is making
  (parallel trends in the *post* period; the instrument affecting Y only through the endogenous
  regressor; potential outcomes continuous at the cutoff; the sort not loading on an omitted priced
  risk). **(5 pts)**
- **The chief threat, named** (box 2 / box 6). The single most plausible violation of that assumption,
  named concretely for this paper, with the *direction* of the resulting bias. **(5 pts)**

A Guide that nails these two sentences and is merely competent elsewhere outscores a polished one that
fudges them. This is the whole point of Week 5.

---

## Part B — Conceptual reading drills (20 points)

Four short items. Answer each in two to five sentences. These test the reflexes from the reading pack
in isolation; you may answer them about the paper you chose for Part A, or your instructor may attach
a one-page table excerpt to answer them against. Cite specific cells, columns, or rows.

**B1. Identify the headline table (5 pts).** Of all the tables in your paper, which is the **headline**
— the one that, if it broke, would sink the paper? Name it, name the single number in it that carries
the result, and say in one sentence how you can tell it apart from a *setup* table (summary statistics,
a first stage) and a *defense* table (robustness, placebo). State the headline number's sign,
magnitude, and t-statistic (compute the t-stat yourself as $\hat\beta/\text{SE}$ if the table reports
the standard error).

**B2. Distinguish identification from estimation (5 pts).** Pick the headline specification and
separate its two halves. What is the **estimation** — the mechanical regression that produces the
number (e.g., "OLS of default on debt-to-income with lender and year fixed effects, SEs clustered by
lender")? What is the **identification** — the assumption under which that number equals the causal
or structural quantity the authors want (e.g., "within a lender and year, debt-to-income is as good as
randomly assigned with respect to unobserved borrower quality")? Explain why a paper can have flawless
estimation and still be wrong, but not the reverse.

**B3. Spot a vulnerable claim (5 pts).** Quote one sentence from your paper's *prose* — the abstract,
intro, or conclusion — that claims **more than the corresponding table delivers**: a causal verb where
the design only supports correlation, a "robust across all specifications" where one column wobbles, an
economic-importance claim resting on a statistically-significant-but-tiny coefficient, or a t-stat that
looks inflated because the standard errors are not clustered at the level the key variable varies. Name
which kind of overreach it is, and what the table actually supports.

**B4. Name a robustness check (5 pts).** Name the **one robustness check the authors ran that most
reassured you**, and say what alternative explanation it was designed to rule out and whether it
succeeds. Then name **one robustness check they should have run but did not** — the one a skeptical
seminar audience would ask for first — and say what it would test. (Examples of the genre: a placebo
on a fake event date, re-clustering standard errors, dropping the largest firms, a McCrary density test
at an RD cutoff, a different formation/holding window for a sort, a pre-trend event study for a DiD.)

---

## Part C — Analytic rubric (point allocations explicit)

Each row is scored at one of four levels. The Part-A rows distribute the 70 Part-A points across the
seven boxes and the two load-bearing sentences; Part B is scored by its four items (5 points each); the
presentation-and-honesty row spans the whole assessment.

| Criterion | Excellent | Proficient | Developing | Missing | Points |
|---|---|---|---|---|---|
| **Identifying assumption + chief threat (boxes 2, 6; the two load-bearing sentences A.2)** | The identifying assumption is stated in one clean sentence in the "equals the true effect *as long as* ___" form, naming the *concrete* condition for this design (parallel trends in the post period / exclusion / continuity at the cutoff / sort not loading on an omitted risk); the chief threat is named specifically and its *bias direction* given; identification is cleanly separated from estimation; box 6's vulnerability is the same threat, with the settling evidence named. | Assumption and threat both correct and specific, but bias direction missing, or box 6 only loosely tied to box 2, or the identification-vs-estimation line is thin. | Assumption stated but generic ("controls for endogeneity," "no confounders") or attached to the wrong design; threat named but vague; bias direction absent or wrong. | Assumption absent, the word "endogeneity" doing all the work, or threat not named. | 22 |
| **Table-reading accuracy (box 4, A1; plus B1, B2)** | Headline table correctly identified and distinguished from setup/defense; the one carrying number read correctly (sign, magnitude, t-stat, $N$) off the table, not the prose; reading order sensible; the §4 spec line complete (outcome · key regressor · controls · FE · clustering · sample · assumption); B1/B2 correct, with identification cleanly split from estimation. | Headline correct and number read correctly, but the §4 spec line drops one element (e.g., clustering or sample), or the setup/defense labeling has one slip. | Headline plausible but the carrying number misread or taken from the prose; spec line mostly missing; confuses a setup or defense table for the headline. | Wrong headline table, or numbers invented / not located in any table. | 18 |
| **Quality & feasibility of the three replications (box 7)** | Three exercises, one of *each* kind (reproduce a named cell / stress an assumption / extend to a new setting); each is concrete, names the data source the camp can actually reach, and the stress exercise says what result would *break* the paper; the reproduce exercise names table, cell, and the data pull. | Three exercises of the right three kinds and feasible, but one is vague on the data or the stress test does not say what would break the paper. | Exercises present but two are the same kind, or one requires data the camp cannot reach, or they restate the paper rather than test it. | Fewer than three, or generic ("run more regressions"), or infeasible. | 14 |
| **The other four boxes (1 research question, 3 data, 5 clever; plus B3, B4)** | Question is one sentence as a question with outcome and key regressor named; data box gives unit / period / source / $N$ and lists filters and flags a look-ahead or survivorship trap; "clever" names the one real good idea; B3 quotes a genuine overreach and classifies it; B4 names a reassuring check *and* a missing one. | All four boxes solid; one item thin (e.g., filters listed but no trap flagged, or B4 names a reassuring check but a weak "missing" one). | Boxes present but the question is a statement not a question, data box missing $N$ or source, "clever" is generic; B3/B4 superficial. | One or more boxes missing or wrong. | 16 |
| **Presentation, spec-discipline, and honest limitations** | Clean prose in the book's voice; specs in §4 format; reads tables before prose and says so; explicitly flags which assumptions are *untestable* and what would be needed to defend them; keeps "identified under a defended-but-untestable assumption" cleanly separate from "proven causal"; admits where the paper — or the student's own reading — is uncertain rather than overclaiming. | One labeling or stylistic lapse; honesty present but a touch thin. | Several lapses; treats a passed diagnostic as proof of an untestable assumption; overclaims causality. | Unreadable, or asserts the paper is "proven" with no caveats. | 10 |

**Total: 100 points.** (Part A = 70: the identifying-assumption/threat row 22 + table-reading 18 +
replications 14 + the-other-four-boxes 16 = 70. Part B's 20 points are folded into the table-reading
row [B1, B2 = 10] and the other-four-boxes row [B3, B4 = 10]. The presentation/honesty row adds 10.
The rubric is normalized so the maximum awarded is 100.)

A note on the spirit of the honesty row. Week 5 rewards the reader who can say, out loud and
unprompted, *which assumption the paper's whole result rests on and why no test in the paper can prove
it*, and who refuses to launder "the authors ran a placebo and it passed" into "the design is proven
valid." A Guide that writes "the parallel-trends assumption is untestable in the post period; the flat
pre-trends are reassuring but not proof, and here is the sensitivity check I would run" outscores a
Guide that presents a clean pre-trend plot as a verdict. Equally, a Guide that *admits* it could not
tell, from the paper alone, whether the standard errors were clustered correctly — and says what it
would need to check — outscores one that confidently asserts a t-stat it never interrogated. Knowing
*what kind of claim* the paper is making, and what kind you are making about it, is the entire point.

---

## Instructor guidance and answer key

This is an open-ended writing task, so the key is a set of *standards* and exemplars rather than a
single correct answer. The two highest-signal things to grade are (1) **the identifying-assumption
sentence and the named threat** — does the student state the concrete bet this paper makes, in the
"as long as" form, and name the specific, direction-signed violation — and (2) **table-reading
fidelity** — did the student find the real headline table and read its carrying number off the table
rather than parroting the abstract? A student who does these two things well has the Week-5 mindset
regardless of polish; the rest is execution.

### Model-answer sketch for Part B

**B1 (headline table).** A strong answer points to a *results* table (the main regression or the
main portfolio-sort spread), not Table 1 (which is almost always summary statistics — a *setup*
table) and not a robustness appendix table (*defense*). The tell: the headline table's dependent
variable is the paper's outcome and its key row is the treatment/key regressor; a setup table has no
coefficient of interest; a defense table re-runs the headline under a perturbation. Strong answers
read the carrying number's sign, size, t-stat (computing $t=\hat\beta/\text{SE}$ where only the SE is
printed, per the reading pack's table glossary), and $N$. Common error: naming the first stage of an
IV as the headline — it is *setup*; the headline is the second-stage (or reduced-form) effect on the
outcome.

**B2 (identification vs. estimation).** Full credit separates the two cleanly. *Estimation* is
mechanical and checkable from the table: which estimator, which controls, which fixed effects, which
clustering — anyone with the data can reproduce it. *Identification* is the untestable bridge from the
estimate to the quantity of interest: the assumption (parallel trends / exclusion / continuity /
correct factor model) under which the coefficient equals the effect. The required insight: a paper can
have *flawless estimation and false identification* (the regression is computed perfectly, but the
assumption that makes the coefficient causal is wrong — and *no amount of estimation care fixes a dead
identifying assumption*), whereas the reverse — true identification undone purely by an estimation
slip — is usually a fixable bug, not a fatal flaw. Reward the student who says estimation errors are
correctable and identification failures are often fatal.

**B3 (vulnerable claim).** Reward a *specific quoted sentence* and a correct classification of the
overreach. The four genres to recognize: (i) a **causal verb on a correlational design** ("X *raises*
Y" when the design is a cross-sectional panel with no exogenous variation); (ii) **"robust across all
specifications"** when the coefficient visibly shrinks or loses significance in the most demanding
column; (iii) **economic-importance inflation** — a three-star coefficient that is economically
trivial (Week 2's "stars are not size"); (iv) **inflated t-stats** from standard errors not clustered
at the level the key variable varies (the Petersen/BDM lesson — un-clustered SEs on persistent panel
data are too small). A weak answer quotes a sentence that is actually well-supported, or calls
something an overreach without saying what the table *does* support.

**B4 (robustness).** A strong answer names a *real* check from the paper and the *specific*
alternative it rules out (a placebo event date rules out "anything that happened at that time"; a
McCrary test rules out sorting at an RD cutoff; re-clustering rules out understated SEs; dropping the
largest firms rules out "one mega-cap drives the result"). Then it names a *missing* check that a
referee would demand first — and it should be the check that bears on the chief threat from box 2. A
weak answer names a cosmetic robustness check (e.g., "added one more control") and a missing check
unrelated to the actual vulnerability.

### Worked example: a strong vs. a weak "identifying assumption in one sentence"

Take a candidate of **type 1**, a difference-in-differences on a state lending regulation — Maya's
territory. Suppose the headline table shows that after some states capped payday-loan APRs, household
delinquency in those states fell relative to non-capping states.

**Weak (do not reward):**
> "The paper uses a difference-in-differences design to control for endogeneity and isolate the causal
> effect of the cap, since fixed effects account for confounding factors."

This fails on every count the reading pack and CONVENTIONS §4 warn about. It names no concrete
condition; "control for endogeneity" is exactly the banned hand-wave; "fixed effects account for
confounding" is false comfort (fixed effects absorb *time-invariant* confounders, not the
*time-varying* ones that threaten parallel trends); and it is not in the "as long as" form, so it
states no falsifiable bet. There is no threat named and no bias direction.

**Strong (full credit):**
> "This DiD estimate equals the true effect of the APR cap on delinquency *as long as* the
> capping and non-capping states would have followed parallel delinquency trends absent the cap — the
> chief threat being that states chose to cap precisely when their own delinquency was already turning
> (reverse causation in the timing), which would bias the estimated effect *away from zero* and make
> the cap look more protective than it was."

This names the design's concrete bet (parallel trends in the *post* period), states it as a
falsifiable "as long as" condition, names a *specific* and plausible threat for *this* setting
(policy timing responding to the outcome's own trajectory — not a generic "omitted variable"), and
gives the *direction* of the bias. A student who then adds, in box 6, "I would check the pre-period
event-study leads and run a sensitivity analysis for how large a differential trend would overturn the
result" has connected the assumption, the threat, and a replication into one coherent reading — the
Week-5 target.

A second quick contrast, for an **IV** paper (type 2): weak — "the instrument is valid because it is
exogenous"; strong — "the 2SLS estimate equals the causal effect of leverage on investment *as long as*
the tax-code change shifts a firm's leverage but has no direct effect on its investment except through
leverage — the chief threat being that the same tax change also altered the after-tax return to
investment directly, violating exclusion and biasing the estimate *upward* if the direct channel and
the leverage channel push the same way." The pattern is identical across designs: name the design's
own assumption concretely, in the "as long as" form, then the specific threat and its direction. That
is the sentence the entire week was built to teach.
