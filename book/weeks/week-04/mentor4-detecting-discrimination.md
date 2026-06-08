# Mentor Session 4 — "Detecting discrimination with a clean design."

*Week 4 live session (remote, via the ASSIP 2026 virtual room) · 60 minutes · led by Prof. Lei Gao*

This week you learned a family of designs that manufacture comparability out of the structure
of the world: difference-in-differences leans on parallel trends to subtract off a common shock,
regression discontinuity reads a treatment effect off a jump at a cutoff, and the staggered and
synthetic-control variants handle the messier cases. Today we point all of that machinery at a
question that is harder than it looks and matters more than almost anything else you will study:
**does a lender treat two otherwise-identical applicants differently because of who they are?**
This is the heart of my own fair-lending work, and it is a wonderful teacher, because the naive
approach to it is so tempting and so wrong. Bring the pre-read and your written warm-ups. We will
argue — and at the end I will hand you a paper my coauthor and I wrote that took this question
all the way from a dataset to Congressional testimony.

---

## (a) Pre-read packet — "Isolating discrimination from everything that looks like it."

*Read this once before the session. It is one page; read it slowly.*

You have lending data: who applied, who got approved, on what terms, and a protected
characteristic — race, sex, the composition of a borrowing couple. You see that one group is
approved less often or charged more. Is that discrimination? Not yet, and the gap between "I found
a disparity" and "I found discrimination" is the entire intellectual content of fair-lending
empirics. A raw disparity confounds two stories. In the first, the lender applies the *same* rule
to everyone, but the groups differ in the things that rule legitimately uses — income, credit
score, debt-to-income, loan-to-value. In the second, the lender applies a *different* rule to the
two groups. Only the second is discrimination, and a difference in approval rates, by itself,
cannot tell you which world you are in.

The standard fix is to **control for creditworthiness**: regress the outcome on the protected
characteristic *and* on income, credit score, loan size, and whatever else the underwriter is
supposed to use, and read the coefficient on the protected characteristic as "the disparity that
remains after accounting for legitimate factors." This is real progress over a raw gap, and it is
the workhorse of the field — but be precise about what it can and cannot establish. It can
establish that the disparity is *not explained by the covariates you measured*. It cannot
establish discrimination, for the same reason selection-on-observables failed us in Week 3: there
is almost always something the underwriter sees that you do not — a thin-file applicant's
explanatory letter, a banker's soft assessment, a piece of collateral not in your data. If that
unobserved factor is correlated with both the protected characteristic and the outcome, your
"residual disparity" is part real differential treatment and part **omitted-variable bias**, and
no amount of controls you happen to have can separate them. Worse, you can *over*-control: if you
adjust for a variable that is *itself* a channel of discrimination — say, the loan terms the
lender steered the applicant toward — you regress away the very effect you are hunting. Controlling
is necessary; it is never sufficient; and which way it biases you is rarely obvious.

So the honest target is not "a disparity after controls." It is the **counterfactual** from
Chapter 3.1, written for this problem: take a single application of a given quality and ask what
*would have* happened to it had only the protected characteristic been different — same income,
same score, same collateral, same everything that a fair underwriter is allowed to weigh, varying
*only* the thing the law forbids the lender to weigh. The difference in outcomes between that
applicant and her unchanged self is the causal effect of the characteristic on the lender's
decision. That is discrimination, defined cleanly, and the Fundamental Problem of Causal Inference
applies in full force: you never observe the same application both ways.

This is why **design**, not a longer list of controls, is what rescues you — and it is exactly
the lesson of this whole week. The audit-study tradition (Bertrand and Mullainathan's
résumé-callback experiment is the canonical example) builds the counterfactual: send paired
applications identical except for a name that signals the protected trait, so the trait is
randomized and everything else is held fixed by construction. When you cannot run an experiment —
and in mortgage markets you usually cannot — you reach for the week's natural-experiment designs.
A **difference-in-differences** built on a policy that changed the rules for one group and not
another differences away the fixed, unobserved between-group differences that plague the
cross-section, isolating the *change* in differential treatment the policy caused. A **regression
discontinuity** at an underwriting cutoff compares near-identical applicants on either side of a
mechanical line. The move is the one you have practiced all week: stop asking the data to be honest
after the fact, and instead find a comparison where the protected characteristic varies for reasons
unrelated to creditworthiness. As you read today's stretch questions, keep one reflex sharp: *what
is the same-quality applicant this design is comparing her to, and what makes that comparison
clean?*

---

## (b) Three Socratic warm-up questions

*Come with a written sentence or two for each. There are honest answers and dishonest ones, not right and wrong ones.*

1. **"I controlled for creditworthiness, so the leftover gap is discrimination."** A classmate
   regresses approval on a protected characteristic plus income, credit score, and loan-to-value,
   finds a significant negative coefficient on the characteristic, and calls it discrimination. In
   a sentence or two, name the *one* thing this regression cannot rule out, and give a concrete
   example of an unobserved factor a real underwriter sees that would inflate (or deflate) that
   coefficient even if the lender were perfectly fair.

2. **The counterfactual you can never see.** Write, in plain words, the counterfactual that
   *defines* lending discrimination for a single applicant — what would have to change, and what
   would have to stay fixed. Then say why no dataset, however rich, lets you observe it directly,
   and name one design from this week that tries to reconstruct it without observing it.

3. **When controlling backfires.** Suppose a lender discriminates by *steering* certain applicants
   toward worse loan products, and you "control for" the product type when estimating the approval
   disparity. Explain why adding that control could make the measured disparity *shrink* even
   though discrimination is real, and connect this to the difference between a confounder you should
   control and a channel you should not.

---

## (c) Five-slide deck (speak-from scaffold)

**Slide 1 — "A disparity is not a finding of discrimination."**
- Lending data shows a group is approved less or priced higher — that is a *disparity*, not yet a verdict.
- Two rival stories produce the same disparity: the *same* rule applied to groups that differ in legitimate factors, vs. a *different* rule applied to the same factors.
- Only the second is discrimination; a raw gap cannot tell them apart.
- Today: why "control for creditworthiness" is necessary but never sufficient, and why a *design* is what closes the gap.

**Slide 2 — What controlling for creditworthiness buys you, and what it doesn't.**
- It buys: the disparity is not explained by the covariates you *measured* — real progress over a raw gap.
- It does not buy: a clean causal effect, because the underwriter sees things you don't (omitted-variable bias, Week 3 all over again).
- The trap on the other side: *over*-controlling for a variable that is itself a channel of discrimination regresses away the effect you want.
- The honest target is a counterfactual, not a coefficient: same applicant, vary *only* the protected trait.

**Slide 3 — The counterfactual definition, and why design beats more controls.**
- Discrimination = the causal effect of the protected characteristic on the lender's decision, holding creditworthiness fixed (Chapter 3.1's potential outcomes).
- The Fundamental Problem: you never observe the same application treated as both groups — so you must *construct* the comparison.
- Audit studies construct it by randomizing the trait on identical applications (Bertrand–Mullainathan résumés).
- When you can't experiment, the week's natural-experiment designs reconstruct it from the world.

**Slide 4 — A clean design in mortgage data: DiD and matched comparison.**
- DiD on a policy shock differences away *fixed* unobserved between-group differences, isolating the *change* in differential treatment the policy caused — parallel trends is the load-bearing assumption (Chapter 4.1).
- Matched comparison pairs same-quality applicants who differ only in the protected trait, shrinking the role of observed creditworthiness so the residual is sharper.
- RD at an underwriting cutoff compares near-identical applicants across a mechanical line (Chapter 4.3).
- Each one answers: *what same-quality applicant are we comparing her to, and why is the comparison clean?*

**Slide 5 — Why the design discipline matters beyond the paper.**
- A credible fair-lending estimate has to survive a hostile referee — *and* a regulator, a journalist, and a court.
- Our same-sex-borrower work (next section) moved from HMDA data to Congressional testimony and engagement with HUD and the Fed — the stakes are policy, not just publication.
- The same checklist you run on any design — what's the comparison, what's the threat, what's untestable — is what makes a discrimination finding stand up.
- Your Lab 4 and Capstone 1 are exactly this: a clean DiD/decomposition on HMDA, built to that standard.

---

## (d) Three "stretch" questions — a clean design from my own work

These tie today's identification ideas to a paper my coauthor and I wrote, offered as a worked
case of detecting discrimination in real lending data:

> Gao, L., & Sun, H. (2019), "Lending practices to same-sex borrowers," *Proceedings of the
> National Academy of Sciences*, 116(19), 9293–9302.

The setting is the one this whole session is built around. U.S. mortgage lenders report, under the
**Home Mortgage Disclosure Act (HMDA)**, a near-census of mortgage applications: the loan amount
requested, the applicant and co-applicant characteristics, income, the action taken (approved,
denied, withdrawn), and pricing information — for essentially every application at covered
institutions. Crucially for this design, HMDA records the *sex of each of two co-applicants*, which
lets you identify applications from **same-sex co-borrowers** (two co-applicants of the same
recorded sex) and compare them to **different-sex co-borrowers**, holding the rest of the
application fixed. The question is whether same-sex couples are treated differently — in approval
or pricing — for reasons that cannot be explained by creditworthiness. This paper led to
Congressional testimony and engagement with HUD and the Federal Reserve: a credible finding here
is not an academic curiosity but evidence in a live regulatory debate.

**Reason about identification and method only. Do not invent or recite any specific reported
magnitudes from the paper — the point is to practice the judgment, not to quote results.**

1. **From disparity to differential treatment.** (a) Write the counterfactual that this design
   wants to estimate, in the potential-outcomes language of Chapter 3.1: for an application of a
   given creditworthiness, what is the effect of the co-borrowers being same-sex rather than
   different-sex on the outcome (approval, or price)? Explain why a raw difference in approval
   rates between same-sex and different-sex applicants is *not* that effect. (b) Now suppose you
   run the workhorse regression of the outcome on a same-sex indicator *plus* income, credit
   factors, loan-to-value, and location fixed effects. State precisely what a nonzero coefficient
   on the same-sex indicator does and does not establish — and name the **omitted-variable** threat
   that prevents you from calling it discrimination outright. (c) HMDA does *not* contain the
   applicant's credit score. Explain how that omission cuts both ways: why it makes the
   control-for-creditworthiness argument harder here, and why a *design* that differences out
   fixed unobservables is therefore more valuable than in a setting where you had the score.

2. **Selection into applying, and the confounds you must rule out.** (a) The deepest threat is not
   in the data you have but in who *enters* it: same-sex and different-sex couples may **select into
   applying** differently — different income distributions, different propensity to apply at all,
   different choices of lender or neighborhood. Explain, in one careful sentence each, why
   *selection into applying* and *unobserved creditworthiness* are distinct threats, and why both
   would contaminate the simple regression from Question 1. (b) Propose a **matched comparison**
   that sharpens the design: on what observable dimensions would you match a same-sex application to
   a different-sex application so that the pair differs *as nearly as possible only* in the protected
   characteristic, and what does matching buy you over throwing the same variables into a linear
   regression? (c) Name one confound that matching on observables *cannot* fix, and say which kind
   of variation — a policy change, a cutoff, an as-if-random shock — you would need to go after it.

3. **What a DiD or natural experiment buys you, and reading the result.** (a) Imagine a state or
   federal change that altered fair-lending protections for same-sex couples at a known date in
   some jurisdictions and not others. Set this up as the difference-in-differences of Chapter 4.1:
   what is the outcome, who is treated, what is the comparison group, and what does differencing
   over time *and* across groups remove that the cross-sectional regression of Question 1 cannot?
   (b) State the **parallel-trends** assumption for this fair-lending DiD in one sentence — what
   would have had to be true about same-sex-versus-different-sex outcome gaps *absent* the policy —
   and describe what you would look for in an **event-study** plot (Chapter 4.1 §5) to make it
   credible, remembering that flat pre-trends are reassuring but never a proof. (c) Suppose your
   treatment is assigned at the state level and rolls out at *different dates* across states. Name
   the staggered-adoption pitfall from Chapter 4.2 that a naive two-way fixed-effects regression
   would fall into here, and the estimator your Lab 4 reaches for instead — and say one sentence on
   why getting the *standard errors* right (cluster by state, Chapter 4.1 §7) is non-negotiable when
   a number is headed for Congressional testimony.

---

## (e) Post-session reflection prompt

*Write ~150–250 words after the session; we will read a few aloud next week.*

Take a claim of discrimination — from a news story, a lawsuit, a paper you are reading for your
project, or a result a friend cites — and put it through the discipline we argued today. First,
separate the **disparity** from the **finding**: what raw gap did they observe, and what did they
do to it? Then run the three questions in order. *Controls:* what did they hold fixed, what
plausible determinant of the outcome did they *not* observe, and which direction would that
omission bias the estimate? Ask explicitly whether they *over*-controlled — adjusted for a variable
that is itself a channel of the discrimination — and what that would have hidden. *Counterfactual:*
state the same-quality-applicant comparison the claim is implicitly making — vary only the
protected trait, hold creditworthiness fixed — and judge whether their method actually constructs
that comparison or merely gestures at it. *Design:* is there a natural experiment, a matched
comparison, or a cutoff doing the identifying work, or is the whole weight resting on a regression
with controls? Finish with the question that is the point of today, and of your Capstone: *if I had
to defend this number to a hostile referee — and then to a regulator and a court — which threat
would I be attacked on first, and would the finding survive?* You do not have to reach a verdict.
You have to look as hard at the comparison as you looked at the gap — because in fair lending, as
in every design this week, the credibility *is* the finding, and the coefficient is only what falls
out once the comparison is shown to be clean.
