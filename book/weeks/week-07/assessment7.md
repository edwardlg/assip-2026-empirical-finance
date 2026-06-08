# Week 7 Assessment — Independent Research Project I: The Design Half

Weeks 1 through 4 handed you a toolkit and taught you to *run* it. Weeks 5 and 6 taught you to
*read* an estimator in someone else's hands and to *build* a measurement honestly. Week 7 asks for
the thing all of that was rehearsal for: a research **design of your own** — a specific, falsifiable
question, on real data you acquired and cleaned yourself, attacked with a design you choose and must
defend. This assessment grades the *design half* of your capstone. The estimation half — running the
regression, the robustness battery, the write-up — is Week 8. You are not being graded here on what
the data say. You are being graded on whether your plan to interrogate the data is one a hostile
referee could not ambush.

That distinction is the entire point of the week, and it is worth stating plainly before you start.
A pre-registered design is not automatically a *good* design, and a good design is not automatically
*honest* in execution. Chapter 7.3 gave you the instrument that governs **honesty** — the
pre-analysis plan, which pins your hypotheses, your one primary specification, and your
multiple-testing plan *before* the data can flatter you, so a reader can tell which of your results
were tests and which were searches. Chapter 7.5 gave you the instrument that governs **validity** —
the identification memo, whose one identifying-assumption sentence and threats-and-responses table
argue that the number your design produces is the thing you claim it is. The PAP says you did not
fish; the memo says the pond is the right pond. You need both, and this assessment makes you submit
both, filed together as a single tagged commit.

**Total: 100 points.** Part A (the submission — your PAP + identification memo + repo) = 70, Part B
(four conceptual items) = 20, presentation and intellectual honesty woven through both = 10. This is
the design deliverable for your own project, so there is no "right answer" in the back of the book;
there is only the discipline of CONVENTIONS §4 — every specification named explicitly, **outcome ·
treatment/key regressor · controls · fixed effects · clustering · sample · identifying assumption in
one sentence** — held to *yourself*, on *your* data, before you have peeked. The rubric in Part C is
the one your Week-8 capstone will be graded against too, so treat this as the rehearsal it is.

Throughout, hold yourself to CONVENTIONS §5: the repo runs end to end on a fresh environment, the
environment is pinned, licensed data stays on GMU infrastructure, and no secret ever appears in your
code.

---

## Part A — The submission (70 points)

You submit **one repository** containing two documents and the machinery that makes them
reproducible. The two documents are your **short-form pre-analysis plan** (Chapter 7.3, five
components) and your **identification memo** (Chapter 7.5, the assumption sentence + the
threats-and-responses table). The machinery is a pinned environment and a Git history that *proves*
the PAP existed before any confirmatory result. The whole thing must be on *your* project — the
question you have carried since Chapter 7.1 and the dataset you built in Chapter 7.4 — not on Maya's
HMDA study, which is the worked example you imitate, not copy.

### A.0 The project, in one sentence (3 pts)

Open with the one-sentence statement of your project from Chapter 7.1, in the fixed form: **the
effect of [a specific treatment or variation] on [a specific, measurable outcome], identified by [a
specific source of variation], using [a specific dataset I can get].** This sentence is the contract
the rest of the submission keeps. If you cannot write it, you do not yet have a project — you have a
regression and a hope, and no rubric below can rescue that.

### A.1 The short-form pre-analysis plan (25 pts)

File a PAP with all **five components** of CONVENTIONS §4 / Chapter 7.3, *in order*, because the
order is the discipline. Use Maya's worked PAP (§7.3.4) as your template for *form*, not content.

1. **Hypotheses, stated directionally (4 pts).** Numbered, falsifiable sentences. H1 is your
   *primary* hypothesis — the one the project lives or dies on; H2, H3, … are secondary. State each
   *direction* (e.g., "higher," "smaller"), because a directional claim earns a one-sided test only
   if the direction came from the science *before* you saw the data, and writing it here is the
   evidence that it did. If you genuinely have no directional prior, say so and commit to two-sided
   — that is honest too; it just costs you the easier critical value.

2. **The primary specification, in spec-discipline form (8 pts).** The single regression that tests
   H1, written out naming *every* one of the seven slots: **outcome** (to a variable name, not a
   concept), **treatment/key regressor** (the one coefficient you read off the table), **controls**
   (named, with one sentence each on why it belongs — and name any variable you deliberately do
   *not* control for because it sits on the causal pathway, the over-controlling trap of Mentor 4),
   **fixed effects**, **clustering** (chosen and justified in advance — this is a notorious fork),
   **sample** (the exact universe of rows, with expected $N$), and the **identifying assumption in
   one sentence**. Write the linear model in the notation of CONVENTIONS §3; the equation pins,
   unambiguously, which coefficient is the test.

3. **The multiple-testing plan (5 pts).** Three moving parts. (i) *Declare primary vs. secondary
   outcomes* — H1 alone is held to the strict $\alpha=0.05$ and is *the* result; everything else is
   labeled secondary. This is the cheapest and most powerful multiplicity control there is. (ii)
   *Group secondary tests into pre-committed families and state the correction* — Benjamini–Hochberg
   FDR control at 0.05 within each family for screening (or Bonferroni if you want the stricter
   family-wise rate and have few tests), named now, before you have the p-values. (iii) *Fix the
   family membership in advance*, so you cannot grow or shrink a family until your favorite effect
   survives.

4. **What would falsify each hypothesis (4 pts).** For each hypothesis, the coefficient-and-interval
   pattern that would make you *abandon* it — phrased, per §7.3.2 and Chapter 1.5.8, to separate a
   genuine **refutation** (a tight confidence interval near zero that *excludes* economically
   meaningful values) from a mere **power failure** (a wide interval that merely *includes* zero). A
   hypothesis no result could contradict is a mood, not a claim.

5. **Planned robustness (4 pts).** The checks you commit to running *now*, labeled as planned to
   distinguish them from post-hoc robustness discovered later — and each one promised to be
   **reported whichever way it comes out.** A planned robustness check converts a fork from a
   p-hacking liability into a strength precisely because you have pre-committed to reporting it
   honestly.

**Plus the registration mechanic, which is graded in A.3:** state your exploratory/confirmatory
split. If your study is *prospective* (the sample period has not happened yet), the future is your
hold-out and you need no split. If the data already exist and you could peek, partition them — e.g.,
a 30% exploration / 70% confirmation split on a stable hashed key, pinned per CONVENTIONS §5 — and
state that the primary specification runs *once* on the untouched confirmation set after the PAP is
tagged.

### A.2 The identification memo (25 pts)

File a memo with the two parts of Chapter 7.5.

1. **The identifying-assumption sentence (8 pts).** One sentence, in the fixed template:

   > Our estimate of **[the effect]** is **causal / credible** as long as **[the assumption]**, which
   > we defend by **[the design feature or evidence]**.

   The first blank names the *effect*, not the regression. The second names the *specific threat* —
   "parallel trends," "the exclusion restriction," "selection on observables" — **never the word
   "endogeneity,"** which is the phrase CONVENTIONS §4 forbids because it commits to nothing. The
   third names the design or evidence that makes the second believable. Choose the verb — *causal*
   vs. *credible* — to match how strong your assumption really is; a clean RD or randomized
   instrument may earn *causal*, but most observational designs earn the weaker, honest *credible*.
   This sentence is allowed to be the longest in your paper. It is the spine of the whole project.

2. **The threats-and-responses table (17 pts).** A literal four-column Markdown table — **Threat ·
   Why it's plausible · What we do about it · Residual concern** — built by pulling the standard menu
   for *your* design off §7.5.2 (OVB/selection for OLS; weak-instrument/exclusion for IV;
   parallel-trends/anticipation/forbidden-comparison for DiD; manipulation/imbalance/compound-treatment
   for RD; donor-pool/anticipation for synthetic control) and adding the threats specific to *your*
   data (a survivorship filter, a look-ahead leak from Chapter 7.4, a measurement-error problem).
   Three disciplines are graded hard here, because they are what separate a memo a referee trusts
   from one they do not:

   - **Match the response to the nature of the threat.** For every threat, decide first whether it is
     **testable** (it leaves a fingerprint: pre-trends, first-stage $F$, a balance table, a McCrary
     density) or **arguable** (it leaves none: the exclusion restriction, compound treatment, the
     post-period parallel-trends counterfactual, silent anticipation). Put a *statistic* in column 3
     for a testable threat and an *institutional/economic argument* for an arguable one. Claiming a
     balance table "shows the exclusion restriction holds" advertises that you do not understand your
     own design.
   - **Every Residual-concern cell is non-empty and substantive.** A table whose fourth column is all
     "none" is *less* credible, not more — every real design has residual concerns, and a reader who
     sees none assumes you did not look hard enough. The honest leftover is the point.
   - **Order rows by descending danger.** Lead with the threat that, if true, would most cleanly kill
     the paper — the one a seminar audience asks about in the first ninety seconds. Burying it reads
     as evasion; leading with it reads as confidence.

### A.3 The reproducible repository (14 pts)

The PAP and the memo only constrain you if their contents are fixed *before* the analysis, and the
only way to prove that to a skeptic is a credible time stamp plus a reproducible environment. Your
registry is your Git history.

- **Tagged PAP (6 pts).** File the PAP (and the memo) as a **tagged commit** — `git tag pap-filed` —
  before any confirmatory regression exists in the history. The tag is your time stamp: a
  cryptographic promise that the plan existed, in exactly this form, before the commits that contain
  your results. A plan no one can date is a plan that constrains no one. Submit the repository link
  and name the tag.
- **Pinned environment (4 pts).** An `environment.yml` or `requirements.txt` pinning
  `python=3.11` and the package versions of CONVENTIONS §5, so the design (and the eventual analysis)
  runs on a fresh conda env. If your project touches licensed data (CRSP, Compustat, Bloomberg),
  pin the **snapshot/vintage date** in a data card and note that the licensed data stays read-only
  on GMU infrastructure (Hopper/WRDS Cloud) — it does not travel in your repo.
- **Hold-out + deviation log + no secrets (4 pts).** The pinned, reproducible exploratory/confirmatory
  split from A.1; a `DEVIATIONS.md` started (even if empty now) to record every departure from the
  PAP with *what* changed, *why*, and *whether the change was prompted by seeing the outcome*; and
  confirmation that no API key or secret appears anywhere — secrets via environment variables only.
  A hard-coded secret caps this row at Missing on its own, per CONVENTIONS §5.

> The confirmatory regression itself is **not** part of this submission. Chapter 7.5's nb7.5
> ("first-look regressions") is *frozen until the PAP is filed*, and even then the first look is a
> Week-8 activity. Week 7 grades the *design*, not the result. A submission that already contains a
> starred headline coefficient has either broken the freeze or is grading the wrong week.

---

## Part B — Conceptual items (20 points)

Answer each in two to five sentences. These test the Week-7 reflexes in isolation.

**B1. Why pre-register? Confirmatory vs. exploratory (5 pts).** A friend says: "Pre-registration is
bureaucracy. If my analysis is honest, writing it down in advance changes nothing." Using the
arithmetic of Chapter 1.5 — and the garden-of-forking-paths idea of §7.3.1 — explain (i) why an
honest researcher who makes a sequence of reasonable, *outcome-aware* choices can manufacture a
spurious starred result without a single dishonest thought, and (ii) precisely what a dated,
committed PAP changes about the meaning of the p-value on the primary specification. State, in one
sentence, the one thing pre-registration does *not* buy you.

**B2. Identification vs. estimation (5 pts).** Devon files a beautiful PAP — one primary spec,
clustering pre-committed, an FDR plan, a tagged commit — for an OLS-on-observables study of whether
on-chain wallet activity predicts a token's next-month return. He says: "My design is bulletproof; I
pre-registered everything." In two to four sentences, explain why a perfect *PAP* does not make his
*identification* sound, name the specific threat his OLS design faces from §7.5.2, and state which
document (PAP or identification memo) is supposed to confront it and how.

**B3. Sort these threats: testable vs. arguable (5 pts).** For a *staggered difference-in-differences*
design, classify each of the following as a threat you can **test** (name the test and its
fingerprint) or one you can only **argue** (name the kind of argument), and say what belongs in
column 3 of the threats table for each: (a) a differential pre-trend; (b) the exclusion-restriction-style
worry that a *co-timed* policy moved with your treatment; (c) anticipation in the quarters just
before the official treatment date; (d) anticipation that began *before any period you observe*.
Then state the one-sentence rule that governs which kind of response column 3 should contain.

**B4. The multiple-testing / FDR plan rationale (5 pts).** Priya's PAP has a secondary family of five
income-band subgroup p-values, $\{0.008,\ 0.012,\ 0.039,\ 0.041,\ 0.330\}$, with $\alpha=0.05$.
(i) Apply the Benjamini–Hochberg procedure and state how many discoveries it declares and which.
(ii) State what Bonferroni would have declared on the same family, and explain in one sentence why
BH is the more sensible default when *screening* a family of candidate effects. (iii) Explain why
the family must be **pre-committed in the PAP** rather than chosen after the p-values are in hand —
what specific abuse does pre-commitment foreclose?

---

## Part C — Analytic research-design rubric (point allocations explicit)

Each row is scored at one of four levels. The rubric is weighted, by design, toward the **quality of
the identifying assumption and threats table**, the **primary-specification discipline**, the
**multiple-testing plan**, and **reproducibility** — because those, not the eventual coefficient, are
what make a design defensible. *This rubric is reused for the Week-8 capstone*, so the standard it
sets is the standard your paper will meet.

| Criterion | Excellent | Proficient | Developing | Missing | Pts |
|---|---|---|---|---|---|
| **Identifying assumption + threats table** (A.2 + B3 + the testable-vs-arguable thread). The assumption sentence names the *effect* and the *specific threat* (never "endogeneity"), names the defending design/evidence, and the verb (*causal* vs. *credible*) is calibrated to the evidence's real strength. The threats table pulls the right menu for the design, adds data-specific threats, **matches a statistic to every testable threat and an argument to every arguable one**, has a substantive non-empty Residual-concern cell in every row, and is ordered by descending danger. | Sentence and table strong, but one slip: verb slightly overclaimed, one threat's response mismatched to its nature (a test where an argument was needed or vice-versa), or one Residual-concern cell thin/"none." | Assumption stated but vague ("controlling for confounders") or table present but missing the standard menu threats, several residual cells blank, or testable/arguable confused throughout. | No named identifying assumption (or it says "endogeneity"), or no threats table, or every residual concern is "none." | **26** |
| **Primary-specification discipline** (A.1.2 + A.0 + B2). One *primary* spec written in full CONVENTIONS §4 seven-slot form (outcome to a variable name · key regressor · named controls with a deliberately-excluded over-control identified · fixed effects · clustering chosen+justified in advance · exact sample with expected $N$ · identifying-assumption sentence), with the linear model written out so the test coefficient is unambiguous; the one-sentence project statement is specific and falsifiable. | All seven slots present and the spec is unambiguous, but one is thin: clustering asserted without justification, the over-control not flagged, or expected $N$ omitted. | Spec stated but a slot is missing or hand-wavy (outcome a concept not a variable, sample vague, no equation), so more than one specification could be read as "the test." | No single primary spec, or the seven slots are not named, or the project sentence is not researchable. | **18** |
| **Multiple-testing plan** (A.1.3 + B4). Primary vs. secondary outcomes declared (H1 alone held to $\alpha$); secondary tests grouped into **pre-committed** families with a named correction (BH-FDR or justified Bonferroni) at a stated level; family membership fixed *in advance*; the BH/Bonferroni logic applied correctly in B4 and the pre-commitment rationale stated. | Primary/secondary split and a correction present, but one element thin: family boundaries a touch loose, correction named without the level, or B4's arithmetic has a minor slip. | Some multiplicity awareness but no clear primary/secondary hierarchy, or a correction named but not tied to a pre-committed family (so it could be gamed). | No multiple-testing plan, or every test reported at $\alpha=0.05$ with no hierarchy or correction. | **14** |
| **Reproducibility — tagged PAP + pinned env + registration** (A.3 + CONVENTIONS §5). PAP/memo filed as a **tagged commit** (`pap-filed`) before any confirmatory result; environment pinned (`python=3.11` + versions) and licensed-data snapshot/vintage pinned and kept on GMU infra; exploratory/confirmatory split pinned and reproducible; `DEVIATIONS.md` present; **no secret anywhere — env vars only**. | Reproducible and tagged, but one element thin: tag present but env unpinned, or split described but not reproducibly keyed, or deviation log absent. | Some reproducibility but a re-run/verification would fail: no tag (so no time stamp), or no pinned env, or the hold-out is not reproducibly defined. | No tagged PAP (the design is undatable), OR a hard-coded key/secret appears anywhere (this alone caps the row at Missing). | **12** |
| **Presentation & honest write-up** (whole submission). Clean prose in the book's voice; the PAP–memo division of labor (honesty vs. validity) is explicit; states which limitations are intrinsic vs. fixable; admits where the design is weakest rather than overclaiming; falsification conditions are written so the student would actually report a null if it came. | One stylistic/labeling lapse; honesty present but a touch thin. | Several lapses; overclaims the design's strength; falsification conditions absent or unfalsifiable. | Unreadable, or asserts the design is "bulletproof" with no stated residual concern or falsification. | **10** |

**Total: 100 points.** The five rows sum to 26 + 18 + 14 + 12 + 10 = 80 from Part A and the honesty
thread; Part B's 20 points are folded into the rows (B2 into the primary-spec row, B3 into the
identifying-assumption + threats row, B4 into the multiple-testing row, B1 into presentation), and
the rubric is normalized so the maximum awarded is 100. The two heaviest rows — the identifying
assumption + threats table (26) and the primary-specification discipline (18) — sum to **44**, and
together with the multiple-testing plan (14) and reproducibility (12), the four design-craft rows
sum to **70**, more than two-thirds of the grade, by design: the design *craft* is what makes a
project defensible, not the eventual coefficient.

The spirit, stated once: **a modest design you have stress-tested honestly outscores an ambitious one
you cannot defend.** A submission that writes, unprompted, "my identifying assumption rests on
selection-on-observables, which I cannot fully defend because the credit score is unobserved, so my
$\hat\beta_1$ is an upper bound, not a clean causal effect" earns more than one that claims a clean
causal effect from the same data. The whole week is the difference between a number that *tested* a
hypothesis and a number *selected* to look like it did — and the only person the design is really
protecting you from is yourself, eight hours and thirty-two specifications into Week 8.

---

## Instructor guidance and answer key

Because this is an open-ended design deliverable on each student's own project, the key is a set of
*standards* plus model-answer sketches and a strong-vs-weak exemplar graders can calibrate against.
The two highest-signal things to grade: (1) **Is there exactly one primary specification, named in
full seven-slot form and tagged before any result, so the p-value on H1 will mean what Chapter 1.5
says it means?** and (2) **Does the threats table match a statistic to every testable threat and an
argument to every arguable one, with a non-empty residual concern in every row?** A student who does
those two things honestly has the Week-7 mindset regardless of how ambitious the project is.

Watch for the classic failures: (a) a PAP "shaped object" so vague it constrains nothing ("I will
study X using appropriate controls and standard errors") — vagueness is p-hacking with extra steps,
so cap the spec row at Developing; (b) an identifying-assumption sentence that says "controlling for
endogeneity" — the exact phrase CONVENTIONS §4 forbids — cap the threats row; (c) a threats table
with all-"none" residual concerns, which is *less* credible, not more; (d) a memo that drifts to a
*different* design than the registered PAP (the contract is broken); (e) any hard-coded secret, which
caps reproducibility at Missing on its own; (f) a submission that already contains a starred
confirmatory coefficient — the freeze was broken, or the student is doing Week 8's work early.

### Model-answer sketches for Part B

**B1 (why pre-register).** A strong answer: when the null is true the p-value is *uniform* on
$[0,1]$, so a single test crosses $p<0.05$ exactly 5% of the time — but each reasonable "maybe" (drop
small lenders? winsorize? quadratic term? cluster by county or lender?) is a fork, and with five
binary forks there are $2^5=32$ paths; even with a dead hypothesis the chance *some* path stars is
enormous ($1-0.95^{20}\approx0.64$ for twenty true-null tests). The researcher need not be dishonest;
walking the forks *with the outcome in view* pulls them, choice by choice, toward the helping branch
(Gelman's garden of forking paths). A dated, committed PAP collapses the 32 forks to *one*
pre-specified test, so the p-value on H1 again means what Chapter 1.5 says — it is a test, not a
search. The one thing pre-registration does *not* buy: **validity.** It governs the *honesty* of the
inference (did you test or search?), not whether the test is the *right* test — that is the
identification memo's job. Full credit names the uniform-p / forking-paths mechanism *and* the
honesty-not-validity caveat.

**B2 (identification vs. estimation).** A perfect PAP guarantees Devon did not *fish* — it does
nothing to guarantee his OLS estimate is the *effect* he claims. OLS-on-observables rests on
**selection-on-observables / conditional independence**, and its standard threats are
**omitted-variable bias** (some unobserved driver of both wallet activity and returns — market-wide
sentiment, a whale's coordinated moves) and **selection**. A referee needs only name one plausible
omitted variable to wound him, and no amount of pre-registration closes that gap. The document that
must confront it is the **identification memo**: its assumption sentence must name the OVB/selection
threat explicitly (not "endogeneity"), and its threats table must respond — and because OVB is about
*unobservables*, the honest column-3 response is an *argument* plus a balance-on-observables table
whose residual concern admits the table is silent on the very confounder he fears. The deep point:
PAP = honesty, memo = validity; Devon has the first and is missing the second.

**B3 (testable vs. arguable, staggered DiD).** (a) Differential pre-trend — **testable**:
estimate the event study and read the leads (normalized at $k=-1$); fingerprint = non-flat,
significant leads; column 3 = the leads plot/test, with the residual that a flat pre-trend can only
*fail to refute* parallel trends, never confirm it. (b) Co-timed policy / compound shock —
**arguable**: no statistical test detects a *perfectly* co-timed policy; column 3 = an institutional
review of each adopter's contemporaneous policy changes and an argument that none plausibly moves the
outcome. (c) Anticipation just before the date — **(partly) testable**: inspect the leads in the
quarters before $G_i$, optionally drop the year before and re-estimate; column 3 = those leads.
(d) Anticipation *before any observed period* — **arguable**: invisible to every lead coefficient;
column 3 = an institutional argument about whether the treatment was anticipable. The governing rule:
**a threat that leaves a fingerprint in the data gets a statistic in column 3; a threat that leaves
none gets an institutional or economic argument — match the response to the nature of the threat,
every time.**

**B4 (BH / FDR plan).** (i) Sort ascending: $\{0.008, 0.012, 0.039, 0.041, 0.330\}$; BH thresholds
$\frac{k}{5}(0.05) = \{0.01, 0.02, 0.03, 0.04, 0.05\}$. Compare from the top down: rank 5,
$0.330>0.05$, no; rank 4, $0.041>0.04$, no; rank 3, $0.039>0.03$, no; rank 2, $0.012\le0.02$, **yes**
→ $k=2$. BH declares the **two** smallest (0.008 and 0.012) as discoveries. (ii) Bonferroni holds
*every* test to $0.05/5=0.01$ and declares only the 0.008 band — it throws away the 0.012 effect BH
keeps. BH is the sensible default for *screening a family*: it controls the *expected fraction of
declared discoveries that are false* (the false discovery rate) rather than the much harsher
chance-of-*any*-false-positive, so it admits later effects at a friendlier threshold and stays
powered when several candidates are real. (iii) The family must be pre-committed because, if the
family is chosen *after* the p-values are seen, the researcher can shrink or grow it until the
favorite effect survives correction — pre-commitment makes the correction automatic and unspoofable,
foreclosing exactly that abuse.

### Exemplar: strong vs. weak identifying assumption + threats table

Use this calibration pair when grading the A.2 row. The contrast is the single most important thing a
grader can internalize.

**Weak (caps the threats row at Developing/Missing):**

> *"We estimate the causal effect of fair-lending regulation on the minority–white denial gap,
> controlling for endogeneity with appropriate fixed effects and clustered standard errors."*

Why it fails: it says **"causal"** with no testable fingerprint earning it; it uses the forbidden
phrase **"controlling for endogeneity"** and names *no specific threat*; the third blank ("appropriate
fixed effects") does no work — a reader cannot tell which counterfactual must hold or how it could
fail. This sentence could front any paper on any topic, so it can be attacked from every side at once.
A threats table attached to it would have a "Differential pre-trend" row whose column 3 reads
"we control for state and year fixed effects" (a *design choice* offered where a *test* — the
event-study leads — was required) and a Residual-concern column of "none." That table advertises that
the author has not engaged their own hardest question.

**Strong (Excellent):**

> *"Our estimate of the effect of state fair-lending examination programs on the county-level
> minority–white mortgage-denial gap is **credible** as long as, absent the programs, adopting and
> never-adopting states' denial gaps would have moved in parallel — which we defend with flat,
> insignificant event-study leads (normalized at $k=-1$), a Callaway–Sant'Anna estimator that forms
> only clean comparisons against never- and not-yet-treated states (never the already-treated states
> that contaminate pooled TWFE under dynamic effects), and the institutional fact that each state's
> adoption timing was set by its legislative and budget calendar, which we argue is unrelated to
> contemporaneous local-lending shocks."*

Why it works: it names the *effect* (not the regression); it uses **"credible,"** the honest verb for
an untestable counterfactual; it names the *specific* threat (parallel trends) and the *specific*
defenses (a test where one exists — flat leads; a design choice against the staggered-DiD bias; an
institutional argument where no test exists). It is the longest sentence in the paper, and that is
correct. A model threats table built from it leads with the most dangerous row and matches responses
to threat-nature:

| Threat | Why it's plausible | What we do about it | Residual concern |
|---|---|---|---|
| **Differential pre-trend** (parallel trends already failing pre-treatment) | Adopting states may have been on an improving denial-gap trajectory that prompted the legislation. | **Testable.** Event-study leads, normalized at $k=-1$; reassuring if flat and insignificant. | A flat pre-trend cannot *confirm* the post-period counterfactual; it only fails to refute it (Ch 4.1). |
| **Forbidden comparison / negative weights** (staggered TWFE using already-treated as controls) | Adoption is staggered and effects plausibly build, the exact recipe for the bias (Ch 4.2). | **Design choice.** Callaway–Sant'Anna group-time ATTs vs. never-/not-yet-treated only; Goodman–Bacon decomposition to show TWFE's forbidden-comparison weight. | Clean estimator needs a sufficient never-treated pool; thin late cohorts are weakly identified. |
| **Compound policy shock** (a co-timed state policy moves with adoption) | States strengthening exams may also change CRA enforcement or down-payment-assistance rules. | **Arguable.** Document each adopter's contemporaneous lending-policy changes; argue none plausibly moves the *gap*. | No test detects a perfectly co-timed policy; rests on the completeness of the institutional review. |
| **Few-treated-cluster inference** (state-clustered SEs strained with few adopters) | Cluster-robust SEs need many treated clusters (Ch 4.1). | **Inference choice.** State-clustered SEs *and* a placebo permutation (reassign adoption years, locate the real ATT). | With genuinely few adopters the uncertainty is large; the placebo distribution is the honest summary. |

Read it the way a referee would: the hardest question (parallel trends) leads; every column-3
response is the *right kind* (test where testable, argument where not); and no Residual-concern cell
is empty, because none honestly could be. A design built on this spine can be attacked — every design
can — but it cannot be *ambushed*, and that is the only standard Week 7 cares about.

### What a top submission looks like, in one paragraph

It opens with a specific, falsifiable one-sentence project statement; files a five-component PAP with
*one* primary specification in full seven-slot CONVENTIONS §4 form (outcome to a variable name, a
deliberately-excluded over-control flagged, clustering justified in advance, exact sample with
expected $N$, the linear model written out) and directional, falsifiable hypotheses whose
falsification conditions distinguish refutation from power failure; declares a primary-vs-secondary
hierarchy with pre-committed BH-FDR families; files an identification memo whose assumption sentence
names the effect and the specific threat with a calibrated verb, and a threats table that leads with
the most dangerous threat, matches a statistic to every testable threat and an argument to every
arguable one, and leaves no residual-concern cell empty; and commits the whole thing as a `pap-filed`
tagged commit in a repo with a pinned `python=3.11` environment, a pinned licensed-data snapshot kept
on GMU infrastructure, a reproducible exploratory/confirmatory split, a started `DEVIATIONS.md`, and
no secret anywhere. That submission is the spine of a Week-8 paper that could survive a hostile
referee — which is the only thing the design half is for.
