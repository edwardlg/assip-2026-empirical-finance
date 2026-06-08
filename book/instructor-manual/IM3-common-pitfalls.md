# IM-3 — Common Student Pitfalls, by Week

> **Companion documents.** This guide catalogs the errors the camp's strongest students still make,
> week by week, and gives each a **diagnostic question** (the one prompt that surfaces the
> misconception fast) and a **fix** (how to correct it without re-teaching the whole chapter). It is
> the field guide to the rubric in **IM-2** — every pitfall here maps to a row that loses points —
> and to the clock in **IM-1**: pitfalls compound across weeks, so catching the Week-1 ones early is
> what keeps the Week-8 capstone defensible. For worked answer keys that show the *correct* version
> of each, see **IM-5 (Answer Keys & Anchor Work)**; for how to surface these in a mentor session,
> **IM-4 (Mentor-Session Facilitation)**.

A note on how to use this. These are not exotic errors — they are the *predictable* ones, the
misconceptions a smart, well-prepared 16-year-old arrives with or develops precisely *because* the
intuition is reasonable. The job is not to shame them but to surface them early, because each one has
a downstream cost: a Week-1 p-value misreading becomes a Week-8 overclaim; a Week-3 "controlling for
X" reflex becomes a capstone with a blank residual-concerns column. The diagnostic questions below
are designed to be asked in a problem-set review or a mentor session and to produce, in the wrong
answer, an unmistakable signature. When you hear the signature, apply the fix.

---

## Week 1 — Probability, Sampling, and the Logic of Inference

**Pitfall 1.1 — The p-value as a posterior probability.** The single most common error in the camp,
and the one the W1 assessment (A7) is built to catch. A student gets $p = 0.03$ and writes "there is
a 3% chance the rule has no real edge" or "a 97% chance it works." This swaps the conditional bar:
$p$ is $\Pr(\text{a statistic this extreme} \mid H_0 \text{ true})$, not $\Pr(H_0 \text{ true} \mid
\text{data})$. The second requires a prior and Bayes' rule and is simply unsupported by the test.

- *Diagnostic question:* "Write the p-value as a conditional probability. What is on the left of the
  bar, and what is on the right?" A student who writes $\Pr(H_0 \mid \text{data})$ has the error.
- *Fix:* Force the verbal translation every time: "*if* the rule truly had zero edge, a t-statistic
  at least this large would occur about 3% of the time by chance." Make them say "if the null were
  true" out loud before any p-value claim. This phrasing is the antidote and it carries all the way
  to the capstone's "no overclaiming" row.

**Pitfall 1.2 — "Finite mean" mistaken for the CLT's load-bearing assumption.** A student invokes the
CLT because the distribution "has a mean" (W1 A6). The real requirement is **finite variance** (plus
enough observations relative to tail weight). A distribution can have a perfectly good mean and
infinite variance (Student's $t$ with $\nu=2$), in which case there is no $\sigma$ to standardize by
and the CLT does not apply at all; and with finite-but-heavy tails the CLT arrives *slowly*, so 200
crypto-return observations need not be nearly enough.

- *Diagnostic question:* "Your population is $t(\nu=2)$. It has a mean. Does the CLT give you a
  trustworthy 95% interval from $N=200$? Name the specific assumption doing the work."
- *Fix:* Have them run the W1 Part-B simulation on a heavy-tailed population and *watch* the
  empirical size drift from 0.05. Seeing the size break is more durable than the theorem. Tie it to
  the Ch 1.4 statement that the CLT arrives slowly under skew/heavy tails.

**Pitfall 1.3 — Treating a simulated number as exact truth.** A student reports an empirical size of
0.058 and either calls it "basically 0.05" or treats it as a fact, with no standard error. The
mindset the whole camp rests on is that *every estimate, including a Monte Carlo one, has a standard
error.* Here each repetition is Bernoulli, so the SE of a size near 0.05 from $R=20{,}000$ reps is
$\sqrt{0.05 \cdot 0.95 / 20{,}000} \approx 0.0015$; a 0.05-vs-0.058 gap is about five SEs — real
signal, not noise.

- *Diagnostic question:* "Your simulated size is 0.058. Put a standard error on it. Is the gap from
  0.05 real or noise?"
- *Fix:* Require a Monte Carlo SE on every simulated quantity, and reward the calibrated phrasing in
  the honesty rubric row (IM-2 §2). "0.058 with an SE of 0.0015, so a real gap" must outscore "0.058,
  basically 0.05."

---

## Week 2 — The OLS Engine

**Pitfall 2.1 — Conflating a bias problem with a standard-error problem.** The defining Week-2
confusion. Students lump heteroskedasticity, clustering, and omitted-variable bias into one bucket of
"things that make the regression wrong." But the first two leave $\hat\beta$ *unbiased and consistent*
and only corrupt the *standard error* (so the point estimate is fine, the t-stat lies); OVB and
measurement error corrupt $\hat\beta$ *itself*. Robust/clustered SEs fix the inference; they do
nothing for a biased coefficient.

- *Diagnostic question:* "You cluster your standard errors and the coefficient barely moves but the
  t-stat halves. Did clustering fix a bias problem or a precision problem? What did *not* change, and
  why?"
- *Fix:* Make them keep the **bias–consistency ledger** from Ch 2.5 on every problem: one column for
  "is $\hat\beta$ right?" and one for "is the SE right?". Heteroskedasticity/clustering live only in
  the second column; OVB/measurement error live in the first. A student who can place each problem in
  the right column has the Week-2 distinction.

**Pitfall 2.2 — Picking the SE flavor by reflex instead of by the data's structure.** Students reach
for HC1 (or worse, classical) everywhere, or cluster on whatever variable is handy. The choice is
dictated by where the correlation in the errors actually lives: cluster at the level at which
treatment is assigned and shocks are correlated (Petersen 2009's taxonomy), use HAC (Newey–West) for
time-series autocorrelation, and remember that with *few* clusters even cluster-robust SEs are
unreliable (the few-clusters problem that returns in Week 4 and the capstone).

- *Diagnostic question:* "At what level are your observations correlated, and does your SE choice
  match that level? How many clusters do you have?"
- *Fix:* Require the SE choice to be *justified in one sentence naming the correlation structure*,
  exactly as the capstone's spec-discipline demands (CONVENTIONS §4). Defer the few-clusters wild
  bootstrap to Week 4/8 but plant the flag now.

**Pitfall 2.3 — Reading a multivariate coefficient without FWL.** Students interpret $\hat\beta_j$ as
"the effect of $x_j$" without grasping that it is the effect of the *part of $x_j$ orthogonal to all
other regressors* (Frisch–Waugh–Lovell). This is why "controlling for" works the way it does, and why
controlling for a variable on the causal pathway is a trap.

- *Diagnostic question:* "Residualize $x_j$ on the other regressors and regress $y$ on the residual.
  Why do you get exactly $\hat\beta_j$ back?"
- *Fix:* Run the nb2.3 residualization demo by hand once. FWL is the bridge to fixed effects (Week 4)
  and the over-control trap (Week 3/7), so the investment pays off three times.

---

## Week 3 — Causal Inference I

**Pitfall 3.1 — "Controlling for X" treated as a causal license.** The central Week-3 error and the
one Maya's loan-approval narrative exists to puncture. Students believe that throwing controls into a
regression "handles confounding" and earns a causal interpretation. It does not: selection-on-
observables requires conditional independence on the *right* variables, and you can never test that
the variables are right. Worse, controlling for a variable on the causal pathway (a mediator) or a
collider actively *introduces* bias.

- *Diagnostic question:* "Name one unobserved variable that would make your 'controlled' estimate
  wrong. Now: is there any control you could *add* that would make it worse, not better?"
- *Fix:* Insist on the language discipline from CONVENTIONS §4 — no "controls for endogeneity," ever;
  name the *specific* threat and the design that addresses it. Have them write the identifying-
  assumption sentence (the Week-7 template) even for a Week-3 problem, so "controlling for X" must be
  defended as an assumption, not assumed as a fact.

**Pitfall 3.2 — Trusting a weak instrument because the second stage looks fine.** Students run 2SLS,
see a plausible coefficient and a significant t-stat, and declare victory without checking the first
stage. A weak instrument biases 2SLS *toward OLS* (bias fraction $\approx 1/F$), inflates and
invalidates the variance, and amplifies any exclusion violation — and a weak-IV second stage can look
perfectly reasonable while being badly wrong.

- *Diagnostic question:* "What is your first-stage F? With that F, what fraction of the OLS bias does
  your 2SLS estimate still carry?" (If they cannot answer, they did not check.)
- *Fix:* Require the first-stage F (and the Olea–Pflueger effective F) reported *before* the second
  stage is interpreted, and teach that "F > 10" is a floor, not a guarantee — for valid inference the
  bar can be far higher. For weak first stages, switch to Anderson–Rubin confidence sets (Ch 3.5),
  which stay valid regardless of instrument strength. Lab 3 (the weak-IV pathology) is the durable
  cure: make them *build* the disaster.

**Pitfall 3.3 — Confusing exclusion (untestable) with relevance (testable).** Students try to
"verify" the exclusion restriction with a statistical test, or treat a strong first stage as evidence
the instrument is valid. Relevance ($\operatorname{Cov}(Z,D) \neq 0$) is testable in the first stage;
exclusion ($\operatorname{Cov}(Z,\varepsilon) = 0$) leaves no fingerprint and must be *argued*
institutionally.

- *Diagnostic question:* "Which of your two IV assumptions can you test, and which can you only
  argue? What evidence goes with each?"
- *Fix:* This is the testable-vs-arguable discipline that the Week-7 threats table grades hard
  (IM-2 §4a). Plant it here: a statistic for relevance, an institutional argument for exclusion, and
  never the two confused.

---

## Week 4 — Causal Inference II

**Pitfall 4.1 — Trusting two-way fixed effects under staggered adoption.** The headline Week-4
pitfall. Students run the canonical TWFE event-study regression on staggered treatment timing and
read $\hat\beta$ as "the effect," not knowing that under heterogeneous and dynamic effects TWFE uses
**already-treated units as controls for newly-treated units** — the *forbidden comparison* — which
can attenuate, and in the extreme **flip the sign**: a policy that helps every unit can produce a
positive TWFE coefficient. A subtle teaching point the book makes honestly: the dramatic sign flip
requires *no never-treated group* (a never-treated unit always preserves the TWFE sign), and that
same condition is what makes the forbidden comparison the only game in town.

- *Diagnostic question:* "In your TWFE regression, which units serve as the control group for your
  last-treated cohort? Are any of them already treated? What does that do to the weight on their
  ATT?"
- *Fix:* Run the Ch 4.2 / nb4.2 World-A demo where TWFE gives $+0.40$ while the truth is $-3.455$ —
  watching the sign flip is the cure. Then show Callaway–Sant'Anna recovering the truth to the
  decimal by forming only *clean* comparisons (against never- and not-yet-treated). Require a
  Goodman–Bacon decomposition to expose the forbidden-comparison weight, and teach the two conditions
  that rescue TWFE (common timing *or* homogeneous effects) so students know exactly when the simple
  estimator is safe.

**Pitfall 4.2 — Reading a flat pre-trend as *confirmation* of parallel trends.** Students see
insignificant event-study leads and conclude "parallel trends holds, so my DiD is valid." A flat
pre-trend can only *fail to refute* parallel trends; it can never confirm the *post-period*
counterfactual, which is fundamentally untestable. It is also easy to mis-specify the leads (using a
naive TWFE event study that contaminates the pre-trends, the problem Sun–Abraham fixes).

- *Diagnostic question:* "Your leads are flat. State precisely what that does and does not establish
  about the years *after* treatment."
- *Fix:* Make them write the residual-concern explicitly — "a flat pre-trend fails to refute, does
  not confirm" — which is exactly the kind of non-empty residual cell the threats table grades. For
  the specification, use Sun–Abraham or Callaway–Sant'Anna leads, not naive TWFE leads.

**Pitfall 4.3 — RD bandwidth as a free dial.** In regression discontinuity, students try several
bandwidths and report the one that gives the cleanest result, not realizing this is a fork in the
garden. The bandwidth must be chosen by a principled rule (Imbens–Kalyanaraman, or
Calonico–Cattaneo–Titiunik robust bias-corrected), and the McCrary density test must be run to check
for manipulation of the running variable.

- *Diagnostic question:* "How did you choose your bandwidth, and did you choose it before or after
  seeing the estimate? Did you run a density test at the cutoff?"
- *Fix:* Require a CCT data-driven bandwidth and a sensitivity sweep *reported whichever way it comes
  out* — the same pre-commitment that protects the capstone. The bandwidth sweep is a planned
  robustness check, not a search.

---

## Week 5 — Reading the Frontier I

**Pitfall 5.1 — Fabricating or mis-transcribing table numbers in a replication.** Reading weeks shift
from running code to reading papers, and the new failure mode is *manufacturing* the numbers the
paper or a replication should produce — reporting a Fama–French sort or a momentum spread from memory
or expectation rather than from the actual computed output, or hand-copying a coefficient into prose
where it drifts from the table.

- *Diagnostic question:* "Show me the line of code that produced this number, and the cell it came
  from. Re-run it in front of me."
- *Fix:* Establish, in Week 5, the rule that becomes the capstone's reproducibility row: *every
  number in prose is generated by code, never pasted by hand.* If a student cannot regenerate a
  number on demand, it does not go in the write-up. This habit is the entire point of the eventual
  `make clean && make all` standard.

**Pitfall 5.2 — Reading a paper front-to-back instead of tables-first.** Students slog through the
introduction and literature review and arrive at the tables exhausted, having absorbed the authors'
framing without independently judging the evidence. The professional move (the W5 opening narrative)
is tables-first: find the headline table, find the identification, *then* read the prose to see if it
earns its claims.

- *Diagnostic question:* "Before you read the introduction — which table is the headline result, and
  what comparison does it rest on?"
- *Fix:* Drill the fixed Reader's-Guide anatomy (research question · identification · data ·
  table-by-table reading order · what's clever · what's vulnerable · replication). The W5 assessment
  is exactly this skill on an unseen paper; make students apply the template before forming an
  opinion.

**Pitfall 5.3 — Mistaking serial correlation for a non-issue in DiD (the BDM lesson).** Students
replicate a DiD and trust the conventional standard errors, not internalizing Bertrand–Duflo–
Mullainathan (2004): serial correlation in the outcome inflates significance dramatically, and a
placebo-law test will manufacture false positives at alarming rates if the SEs are naive.

- *Diagnostic question:* "Run a placebo law — assign a fake treatment date to untreated units. How
  often do you get a 'significant' effect? What does that tell you about your real SEs?"
- *Fix:* Have them reproduce the BDM placebo-DiD false-positive (PS 5.5 / nb5.5). The false-positive
  rate they generate themselves is the unforgettable lesson, and it sets up the few-clusters and
  wild-bootstrap concerns in the capstone.

---

## Week 6 — Reading the Frontier II + the AI Co-Pilot

**Pitfall 6.1 — Trusting LLM labels without out-of-sample validation.** The defining Week-6 pitfall
and the one the assessment weights most heavily. Students use an LLM to classify text (8-K events,
sentiment, fair-lending categories) and treat the labels as ground truth, when an LLM label is a
*measurement* like any other and must be validated against a hand-labeled gold set: a held-out
test split, a confusion matrix, precision/recall/F1 — and *not* accuracy alone when classes are
imbalanced.

- *Diagnostic question:* "Where is your hand-labeled gold set, and what are precision and recall on
  the *held-out* split? Why not just report accuracy?"
- *Fix:* Require the full OOS validation protocol from Ch 6.5: gold set, dev/test split, confusion
  matrix, precision/recall/F1, with the *test* split touched once. The W6 rubric rewards the
  validation table over the headline accuracy, and an AI-produced variable in the capstone requires
  exactly this validation table (IM-2 §4b, honesty/disclosure).

**Pitfall 6.2 — Look-ahead and training-data leakage.** Students build an LLM or ML classifier that
secretly uses information unavailable at the prediction date — a model whose training data postdates
the event it "predicts," or features that encode the future. This is the text-as-data analogue of the
survivorship/look-ahead bias from Week 7's data-build chapter, and it silently inflates every
performance metric.

- *Diagnostic question:* "Could your model have known the outcome at the time it makes its prediction?
  When was the model trained relative to your sample period?"
- *Fix:* Make them write a one-paragraph **leakage audit** (PS 6.5) naming, for every feature and the
  model itself, what was knowable when. Tie it to the capstone's responsible-AI disclosure: AI-produced
  data needs a validation table *and* a leakage statement.

**Pitfall 6.3 — Prompt-induced p-hacking and treating stochastic output as reproducible.** Students
re-prompt an LLM until it returns the answer they wanted (a form of the garden-of-forking-paths), or
report a result from a stochastic model without fixing what can be fixed and disclosing what cannot.
LLM outputs are not deterministic the way a seeded simulation is.

- *Diagnostic question:* "How many prompts did you try before this one, and would you have kept a
  different answer? If I re-run your pipeline, do I get the same labels?"
- *Fix:* Require a logged, fixed prompt and a disclosed protocol; treat re-prompting-to-taste as the
  same offense as spec-searching. Disclose stochasticity honestly rather than pretending to a
  reproducibility the tool does not offer. This is the Week-6 root of the capstone's honesty row.

---

## Week 7 — Research Project I: Question to Pre-Analysis Plan

**Pitfall 7.1 — Peeking before the PAP is filed (breaking the freeze).** The cardinal Week-7 sin.
Students run "just a quick first regression" on their data before filing the pre-analysis plan, or
they file a PAP whose primary spec they have already seen the result of. The whole apparatus —
hypotheses, one primary spec, multiple-testing plan — only constrains anything if it is fixed
*before* the data can flatter them. A starred coefficient that postdates no `pap-filed` tag means the
p-value no longer means what Chapter 1.5 says.

- *Diagnostic question:* "Show me the Git history. Does the `pap-filed` tag predate every confirmatory
  commit? Have you looked at your primary spec's result yet?"
- *Fix:* Enforce the tagged-commit mechanic mechanically — `git tag pap-filed` before any
  confirmatory regression exists (Lab 7). Freeze nb7.5 (first-look regressions) until the PAP is filed.
  This is a hard cap on the capstone's execution row (IM-2 §4c), so establishing the discipline now is
  non-negotiable.

**Pitfall 7.2 — A PAP so vague it constrains nothing.** Students write "I will study X using
appropriate controls and standard errors" — a "shaped object" that looks like a plan but pins no
single specification, leaving every fork open. Vagueness is p-hacking with extra steps.

- *Diagnostic question:* "Read me your primary specification. Can more than one regression be read as
  'the test'? Name the outcome variable — the variable, not the concept."
- *Fix:* Require all seven slots of CONVENTIONS §4 named explicitly: outcome (to a variable name),
  key regressor, named controls (with a deliberately-excluded over-control flagged), fixed effects,
  clustering justified *in advance*, exact sample with expected $N$, and the identifying-assumption
  sentence. If more than one spec could be "the test," the row caps at Developing.

**Pitfall 7.3 — Confusing a good design with an honest one (PAP vs. memo).** Students believe a
tagged PAP makes their identification sound, conflating the two instruments: the PAP governs
*honesty* (did you test or search?), the identification memo governs *validity* (is this the right
test of the right effect?). A bulletproof PAP on an OLS-on-observables study does nothing to close the
omitted-variable gap.

- *Diagnostic question:* "Your PAP is perfect. Name the unobserved confounder that still wounds your
  estimate. Which document is supposed to confront it?"
- *Fix:* Drill the division of labor: PAP = honesty, memo = validity. Make the memo's threats table
  match a statistic to every testable threat and an argument to every arguable one, with no empty
  residual cell — the discipline that started in Weeks 3–4 and now becomes gradable.

---

## Week 8 — Research Project II: Execution, Robustness, Writing, Defense

**Pitfall 8.1 — Overclaiming: causal language the design does not earn.** The terminal pitfall the
whole camp exists to prevent. Students hedge in the abstract ("is associated with") and then drift to
"causes" or "proves" in the conclusion, attaching a verb to the main result that the weakest
assumption cannot support. A clean OLS-on-observables association written up as a causal effect is the
classic overclaim.

- *Diagnostic question:* "Read me only the verbs attached to your main result, abstract through
  conclusion. Do they all match your weakest assumption? Where does the verb drift?"
- *Fix:* The verb audit (IM-2 §6): force every verb attached to the main result to the *weakest*
  assumption, with no drift across sections. Reward the honest hedge — a paper that writes "my Oster
  $\hat\delta$ is 0.4, so I report a robust *association*, not a causal effect" outscores one claiming
  a clean causal effect from the same data.

**Pitfall 8.2 — The robustness section that only passes.** Students show only the checks that
confirmed their result and quietly drop the scary placebo or the sensitivity sweep that narrowed the
claim. A battery with no failed check reads as *less* credible, because the grader assumes the student
did not try hard enough to fail. Related failures: asserting Oster $\delta$ without a defended
$R_{\max}$ and a sweep to 1; keeping conventional stars on a treatment with few treated clusters after
a wild cluster bootstrap disagreed.

- *Diagnostic question:* "Which check *failed* or narrowed your claim? Show me the scary placebo for
  your top-ranked threat. What is your $R_{\max}$ and did you sweep $\delta$ to 1?"
- *Fix:* Teach that a failed check is a *finding* that narrows the claim, not a defeat to hide. The
  scary placebo for the top threat must appear whether or not it passed; Oster $\delta$ is
  uninterpretable without its $R_{\max}$; few treated clusters demand the wild bootstrap and, if it
  disagrees, the stars come off. This is the A/B line (IM-2 §4d).

**Pitfall 8.3 — The pasted number that breaks the rebuild.** Students hand-copy a coefficient or
paste a figure into the paper, so `make clean && make all` no longer reproduces it — the single most
common reproducibility failure. Related: a SEED set but not threaded through every stochastic step, or
a hard-coded secret (which caps the row at Missing on its own).

- *Diagnostic question:* "I just ran `make clean && make all` on a fresh clone. This table number
  drifted. Where did it come from?"
- *Fix:* Run the rebuild yourself — it is the most objective row in the rubric and it *is* the GMU
  JSSR submission standard (IM-2 §4c). Every table and figure generated by code, never pasted; one named
  SEED threaded through every bootstrap/permutation/split; environment pinned (`.yml` + `.lock.yml`);
  no secret anywhere, env vars only (CONVENTIONS §5).

**Pitfall 8.4 — Bluffing the fatal critique in the defense.** Under questioning, students argue
harder when they should concede — defending a critique that attacks their *comparison* (fatal) as if
it attacked merely a *number* (survivable). This is the B-not-A behavior, and it inverts what the camp
rewards.

- *Diagnostic question:* "That critique — does it attack one of your numbers, or the comparison your
  whole design rests on? If the comparison, can your design answer it at all?"
- *Fix:* Teach the survivable-vs-fatal distinction and *reward the concession*: "you're right, that
  attacks my comparison, and my design cannot answer it" demonstrates the exact judgment the camp
  teaches and should outscore a successful bluff. Rehearse with the Tue Aug 11 dry-run defense (IM-1 §6);
  use the mentor-session question protocol in IM-4.

---

## ASSIP 2026 — remote-cohort pitfalls

The eight weekly pitfalls above are about *methods*: they will appear in any cohort that meets this
curriculum, residential or remote. The pitfalls below are specific to the **ASSIP 2026 remote-only
format** — they describe the failure modes the room's design itself produces, and they are the ones a
sub-leader running the daily standup or an instructor watching the cohort sync should be alert for
*independent of the chapter*. They are not signs of weakness in any individual student; they are the
predictable physics of running a 14-person full-time cohort over Zoom for eight weeks.

**ASSIP-R.1 — The silent dropout.** The defining remote-cohort failure. A student is "in the Zoom"
all day but their camera has been off for three days, their pod standup contributions are
single-sentence reports of "still working on it," and their problem sets shift from late to missing.
By the time it is visible to the cohort it is usually two weeks past the point of intervention. The
underlying cause is rarely the curriculum — it is isolation, a quiet personal crisis, an unreliable
home setup, or the unconscious math that "no one will notice if I disappear from a 14-person Zoom for
a day," which compounds.

- *Diagnostic question (for the sub-leader, not the student):* "Has this student turned a camera on
  in the last 48 hours? Has their pod sub-leader had a one-on-one with them this week? Did their
  Friday show-and-tell happen?" If any answer is no, the student is at risk regardless of grades.
- *Fix:* Hard rule for sub-leaders: a one-on-one (ten minutes, camera-on if accommodations allow, by
  phone if not) with every student in your pod **at least once every five weekdays**, scheduled.
  Escalate to Prof. Gao on the *first* missed problem set, not the third — early intervention is
  cheap, late intervention is sometimes impossible. The cohort sync 4:00 pm slot is the public
  heartbeat; absences from it for two consecutive days trigger the one-on-one automatically.

**ASSIP-R.2 — Pod fragmentation: the room of four small rooms.** A natural consequence of the pod
structure is that students start to identify with their pod and stop talking to the other ten
students. Tuesday/Thursday peer-review pairs work for a week, then quietly stop happening because the
pair feels less efficient than working within the pod. By Week 4 the cohort is functionally four
parallel cohorts of three or four, and the cross-pollination that produces the strongest capstone
ideas evaporates.

- *Diagnostic question:* "How many of the other ten students outside your pod can you name and
  describe their capstone project in one sentence?" Run this in Week 3 and Week 5. A student who
  cannot name six is in a fragmented cohort.
- *Fix:* The W4 pod reshuffle (IM-1 §3) is the structural defense — *every student gets new podmates
  exactly once*, which forces a second round of cross-pod friendships. Reinforce with mandatory
  cross-pod peer-review pairs Tuesday and Thursday (rotate the pairing matrix weekly), and use the
  Friday show-and-tell to make every student answer one question from a student in a different pod.

**ASSIP-R.3 — The wiki ghost town.** The cohort wiki (IM-1 §6) is supposed to be the cohort's shared
brain — every student's daily notebook, every replication walk-through, every "I got stuck here and
this is how I unstuck myself" written up so the next student does not have to reinvent it. The
predictable failure: the wiki gets seeded on Day 1 with the per-student and per-pod page skeletons,
and then nothing flows into it. By Week 3 it is a graveyard and students are answering the same
question for the seventh time on Zoom because no one wrote the answer down.

- *Diagnostic question (for the instructor, weekly):* "How many edits to the wiki happened this week
  from students who are *not* the four sub-leaders? Are last week's three most-asked Zoom questions
  documented anywhere a future student can find them?"
- *Fix:* Build wiki-writing into the workflow, not as an aspiration. Two structural moves work.
  First, **rotate a "wiki scribe" role across the cohort each week** — one student per week is
  responsible for documenting the week's three highest-signal Zoom questions and their answers,
  graded as cohort-participation; the scribe rotates so every student does it once across the eight
  weeks. Second, the **end-of-day standup includes a "what did I add to the wiki today" line**, and
  it is fine for the answer to be "nothing" twice in a row but not three times — the visibility of
  the count is the pressure. The wiki is the only thing that survives the cohort; treat it as the
  cohort's deliverable to the *next* cohort, not as scratch paper.

**ASSIP-R.4 — Zoom-fatigue grading drift.** The instructor or sub-leader who has been on Zoom for
seven hours grades the next student's problem set differently than the first. The drift is downward
(stricter at the end of the day) or upward (charitable because the grader is tired) depending on the
person; either way it is a fairness problem because the order in which papers happen to be graded is
not a property of the student's work.

- *Diagnostic question:* "Look at your last 20 graded problem sets in order. Is there a visible
  trend in the row-by-row scores over the sequence?"
- *Fix:* Apply the by-row pass discipline (IM-5 Part A) ruthlessly under remote conditions — grade
  Problem 1 across all 14 students, then Problem 2 — and *take the break between rows*. A grader's
  attention is a Tuesday-morning resource; do not spend it after the cohort sync. The double-grade
  random sample (IM-5 Part E) catches drift before it changes a letter grade.

**ASSIP-R.5 — The async/sync confusion.** Because Prof. Gao's slot is remote and recorded, students
who miss a synchronous block tell themselves they'll catch the recording. Often they do not; the
recording sits unwatched, and the student arrives at the next chapter without the foundation it
assumes. Recordings are an *equity* tool (IM-6, for the student with bandwidth issues or an
accommodation) but they are not a *substitute* for synchronous attendance, and the line between
those two uses is the failure point.

- *Diagnostic question:* "Did the student attend the last three days' chapter blocks synchronously,
  or have they been 'catching up on recording'? When did they last submit a problem set on time?"
- *Fix:* Treat synchronous attendance as the default and the recording as the documented exception.
  A pod sub-leader's one-on-one (ASSIP-R.1's mechanism) is the right place to surface a slipping
  attendance pattern — the recording-catch-up student is one phone call away from the silent
  dropout.

The five remote-cohort pitfalls share a structure: each one is invisible until it is a crisis. The
defenses are all small, daily, structural acts — the one-on-one, the standup, the wiki scribe, the
cross-pod pair, the by-row grading pass with a break. Build them into the rhythm in Week 1 and they
cost almost nothing in Weeks 2–8. Skip them in Week 1 and you spend Weeks 4–8 retroactively rescuing
students whose drift was preventable.

---

## Using this guide across the camp

The pitfalls are not independent; they are a chain. The student who learns in Week 1 that a p-value
is not a posterior, and that every simulated number has a standard error, is the student who in Week 8
does not overclaim and does not present a battery that only passes. The student who in Week 3 stops
saying "controlling for X" and starts naming the specific threat is the student whose Week-7 threats
table has no empty residual cell. Catch the early ones early — the diagnostic questions are cheap to
ask in a problem-set review or a mentor session, and an hour spent surfacing a Week-1 misconception
saves a capped rubric row in Week 8. That compounding is exactly why the dependency order in IM-1 is
not negotiable, and why the rubric in IM-2 weights the late, honest craft over the early, easy
arithmetic.
