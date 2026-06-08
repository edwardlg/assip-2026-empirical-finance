# Mentor Session 3 — "Natural experiments: finding the lever nature pulled."

*Week 3 live session · 60 minutes · led by Prof. Lei Gao*

This week you learned the framework that organizes all of causal inference: potential
outcomes, the selection-bias term that contaminates the easy comparison, and the four designs
that chase it down — matching, weighting, and, the one we live inside today, instrumental
variables. Chapter 3.4 taught you that an instrument is a lever that shoves the treatment
around for reasons unrelated to the confounder, and Chapter 3.5 taught you how that lever can
betray you when it is weak. Today we ask where these levers actually come from. You almost
never get to flip the coin yourself — you cannot randomly assign firms to face short-sale
constraints, families to take on debt, or countries to suffer a crisis. So the empiricist's
real craft is *finding* the coin someone else already flipped: a rule change, an accident of
geography, a regulatory experiment, a quirk of timing that splits the world into treated and
control as-if at random. That is a **natural experiment**. Bring the pre-read and your written
answers to the three warm-ups. We will argue, not lecture — and at the end I will show you one
my coauthors and I actually used.

---

## (a) Pre-read packet — "What makes a natural experiment credible?"

*Read this once before the session. It is one page; read it slowly.*

A natural experiment is a piece of the real world that *behaves like* a randomized trial even
though no researcher ran one. Some force outside the system — a legislature, a regulator, a
weather pattern, a calendar rule — assigned a treatment to some units and not to others in a
way that, you will argue, is unrelated to the things that would otherwise confound your
comparison. The entire value of the design rests on that "as-if random" claim, and a credible
natural experiment is one where you can defend three things in plain language.

**First, as-good-as-random assignment.** Recall the master decomposition from Chapter 3.1:
the naive difference in means equals the causal effect plus a selection-bias term,
$\mathbb{E}[Y_i(0)\mid D_i=1] - \mathbb{E}[Y_i(0)\mid D_i=0]$ — how different the two groups
already were before treatment touched anyone. Randomization zeroes that term because the coin
does not know who you are. A natural experiment makes the same bet without a coin: it claims
that *whatever* assigned the treatment did so independently of the units' potential outcomes.
When a regulator picks treated firms by drawing every other name off a list sorted by an
irrelevant key, treated and control firms are, in expectation, the same kind of firm — exactly
the property a coin would have bought. Your first job is to argue that the assigning force was
blind to the outcome, and to *check the balance*: treated and control units should look alike
on observables before treatment, because if the lottery were real they would.

**Second, the exclusion-restriction argument.** This is the harder half, and it is the same
untestable claim that haunted IV in Chapter 3.4. As-if-random assignment gets you a clean
*offer* of treatment, but for the design to identify the effect of the *treatment itself*, the
assignment must reach the outcome **only through** the treatment — no side door. If the rule
that relaxed a constraint also, say, drew analyst attention or changed disclosure rules at the
same moment, then the rule touches the outcome through a channel that is not your treatment,
and the estimate is contaminated. There is no statistic that confirms exclusion; you defend it
with institutional knowledge — what *exactly* did the rule do, and did it do anything else? —
and you stress-test it against every alternative channel a skeptic can name.

**Third, the complier population.** Even a perfect natural experiment does not measure the
effect on everyone. From the LATE theorem (Chapter 3.4), an instrument identifies the effect
only for **compliers** — the units the lever actually moved. A rule that relaxes short-sale
constraints does not change behavior for stocks no one wanted to short anyway (never-takers)
or for stocks already shorted to the hilt (always-takers); it bites only on the marginal
stocks whose short-selling the rule actually unlocked. Your estimate is *their* effect. Before
you generalize, ask: who are the compliers here, and is their effect the one the policy
question cares about?

So as you read today's stretch questions, train the reflex from Chapter 3.5's referee
checklist: name the assignment mechanism, ask whether it was blind, ask what *else* it might
have done, and ask whose effect you are actually estimating. A natural experiment is credible
exactly to the degree that you can answer all three out loud.

---

## (b) Three Socratic warm-up questions

*Come with a written sentence or two for each. There are honest answers and dishonest ones, not right and wrong ones.*

1. **"It's basically a randomized trial, so I don't need to defend anything."** A classmate
   finds a regulatory rule that assigned a treatment to some firms and not others and says the
   as-if-random assignment means the result is automatically causal. In a sentence or two,
   name the *one* assumption that as-if-random assignment does **not** buy you, and give a
   concrete example of a side channel that could break it even if the assignment really was a
   lottery.

2. **As-if random vs. truly random.** A coin flip and a "natural experiment" both promise that
   treated and control groups are comparable. What can you *check in the data* to make the
   as-if-random claim credible, and — being honest — what can you never check? Tie your answer
   to the selection-bias term from Chapter 3.1.

3. **Whose effect did you measure?** Suppose a rule relaxes a constraint for a randomly chosen
   set of firms, and you estimate a clean effect on some outcome. Your abstract says "relaxing
   the constraint causes the outcome to change." Rewrite that sentence so it is honest about
   the complier population, and name one group of firms whose effect your design is *blind* to,
   and why.

---

## (c) Five-slide deck (speak-from scaffold)

**Slide 1 — "You rarely flip the coin; you find one already flipped."**
- Most finance questions cannot be randomized — ethics, cost, law, or the event already happened in the historical record.
- A *natural experiment* is a real-world force (a regulator, a law, a weather pattern, a calendar rule) that assigned treatment as-if at random.
- The craft is recognizing that lever and arguing it is clean — the statistics are the easy part.
- Today: the three things that make a natural experiment credible, then a real one from my own work.

**Slide 2 — As-good-as-random assignment (Chapter 3.1, borrowed from the world).**
- The villain is always the selection-bias term: how different treated and control already were before treatment.
- Randomization zeroes it with a coin; a natural experiment zeroes it by claiming the assigning force was blind to potential outcomes.
- You *test* this with balance: do treated and control units look alike on observables before treatment? If the lottery is real, they should.
- Balance is necessary, not sufficient — it checks the observables; the unobservables are still an act of faith in the design.

**Slide 3 — The exclusion-restriction argument (Chapter 3.4, untestable as ever).**
- As-if random buys a clean *offer*; identifying the *treatment* needs the offer to reach the outcome only through the treatment.
- Side doors kill it: if the same rule also moved disclosure, attention, or another policy, the assignment has a second path to the outcome.
- There is no test — you defend exclusion with institutional facts about what the rule did and did *not* do, then attack your own argument.
- A strong first stage is your buffer: a faint lever amplifies any tiny exclusion violation (Chapter 3.5).

**Slide 4 — The complier population (LATE, not ATE).**
- The lever only moves some units; you estimate the effect for *those* — the compliers — not for everyone.
- A constraint-relaxing rule moves the marginal units, not the never-takers (untouched) or always-takers (already at the limit).
- Always ask: who are the compliers, can I describe them, and is their effect the policy-relevant one?
- Two valid natural experiments for the same question can give two different, both-correct numbers, because they move different compliers.

**Slide 5 — How to read (and run) a natural experiment.**
- Name the assignment mechanism in one sentence; then ask: was it blind, what else did it do, whose effect is this?
- Report the balance check, the first stage (did the rule actually move the treatment?), and the reduced form (did it move the outcome?).
- Honest inference still matters — a weak lever needs the weak-IV-robust tools from Chapter 3.5, not a confident-looking t-stat.
- Your summer goal: spot the lever nature pulled, and defend it the way a hostile referee would attack it.

---

## (d) Three "stretch" questions — a natural experiment from my own work

These tie today's identification ideas to a paper my coauthors and I wrote, offered as a
worked case of a regulatory natural experiment:

> Deng, X., Gao, L., & Kim, J-B. (2020), "Short-sale Constraints and Stock Price Crash Risk:
> Causal Evidence from a Natural Experiment," *Journal of Corporate Finance*, 60, 101498.

The setting is the one Chapter 3.4 §7 previewed. There is a long-standing correlation in the
data: stocks that are harder to short tend to have more **crash risk** — a higher chance of a
sudden, large negative price move, the fingerprint of bad news that management hoarded until it
burst out all at once. But the correlation is hopelessly endogenous. Short-sellers *choose*
which stocks to target based on the very bad news that also drives crashes (reverse causality),
and unobserved firm qualities — governance, opacity, the manager's appetite for hiding losses —
drive both how short-sellers behave and how prone the stock is to crash (confounding). You
cannot regress your way out of this. What you need is exogenous variation in short-sale
constraints: some force that relaxed the constraint for some stocks and not others, for reasons
unrelated to those firms' news or governance. A U.S. regulatory pilot supplied exactly that —
the regulator suspended price restrictions on short sales for a set of stocks selected off a
ranked list in a way unrelated to any individual firm's fundamentals, while leaving the rest
constrained. That is the coin the regulator flipped.

**Reason about identification and method only. Do not invent or recite any specific reported
magnitudes from the paper — the point is to practice the judgment, not to quote results.**

1. **Where is the exogenous variation, and why does it help?** (a) Name the source of
   exogenous variation in this design — what did the regulator do, and to whom — and explain in
   the potential-outcomes language of Chapter 3.1 why the naive regression of crash risk on
   short-sale constraints is *not* causal (name both the reverse-causality and the
   unobserved-confounding threat). (b) Explain how the regulatory pilot lets you sidestep both
   threats: which group is the as-if-randomly-treated set, which is the control, and why
   assignment by a ranked list (rather than by firm choice) is what makes the comparison clean.
   (c) Frame the design in the three-regression anatomy from Chapter 3.4 §7: what is the *first
   stage* (did the rule actually change short-selling for treated stocks?), what is the *reduced
   form* (did the rule change crash risk?), and what does their relationship identify?

2. **State and stress-test the exclusion restriction.** (a) Write the exclusion restriction for
   this design in one careful sentence: the regulatory pilot must affect crash risk *only
   through* its effect on short-sale constraints, and must be unrelated to the firms' underlying
   crash-driving qualities. (b) Now play the hostile referee and propose *two* distinct side
   channels by which being a pilot stock could affect crash risk **without** going through
   actual short-selling — for instance, a change in how much attention analysts or the press
   paid to pilot stocks, or managers behaving differently simply because they knew their stock
   was in the experiment. For each, say in one sentence why it would contaminate the estimate.
   (c) For one of your side channels, describe a concrete check or placebo test that would make
   the exclusion argument more (or less) credible — remembering from Chapter 3.4 that you can
   never *prove* exclusion, only defend it.

3. **Compliers, balance, and reading the result.** (a) Who are the *compliers* in this design —
   for which kind of stock did the pilot actually relax a *binding* short-sale constraint? Name
   one type of stock that is a likely *never-taker* (the rule changed nothing about its
   short-selling) and one likely *always-taker*, and explain why the estimated effect is silent
   about both. (b) Before trusting the as-if-random claim, what *balance* evidence would you
   want to see — what should treated and control pilot stocks look like, on what dimensions,
   before the pilot began — and what would a *failure* of balance tell you about the design? (c)
   Suppose the first stage turned out to be only moderately strong. Using Chapter 3.5, explain
   why that would make you more worried about your two side channels from Question 2, and name
   the weak-IV-robust tool you would reach for instead of a conventional t-statistic.

---

## (e) Post-session reflection prompt

*Write ~150–250 words after the session; we will read a few aloud next week.*

Go find a natural experiment — in a paper you are reading for your project, a working paper, a
finance blog post, or a result a friend cites — and put it through the three-part credibility
test we argued today. First, name the assignment mechanism in one sentence: what force in the
world assigned the treatment, to whom, and for what reason? Then work the three questions in
order. *As-good-as-random:* what is the argument that the assigning force was blind to the
units' potential outcomes, and what balance check could you run (or did the authors run) to
support it? *Exclusion:* state, in your own words, the one untestable assumption the design
leans on — that the assignment reaches the outcome only through the treatment — and name the
single most plausible side channel that could break it. *Compliers:* whose effect does this
design actually estimate, and is that the population the paper's headline claim is really about,
or does the abstract quietly overclaim? Finish with the question that is the whole point of
today: *if I were the hostile referee, which of the three would I attack first, and would the
finding survive?* You do not have to land a verdict. You need to have looked at the design as
hard as you looked at the number — because in a natural experiment, the design *is* the
finding, and the coefficient is just what falls out once the lever is shown to be clean.
