# Mentor Session 5 — "Anatomy of a JF paper."

*Week 5 live session (remote, via the ASSIP 2026 virtual room) · 60 minutes · led by Prof. Lei Gao*

All week you have been a *reader*. You ran the seven-part template on Fama–French, on Jegadeesh–Titman,
on Petersen, on Bertrand–Duflo–Mullainathan. You learned to go to the tables first and the introduction
last, to find the headline number, to state the identifying assumption in one sentence, and to name the
one threat a referee would fire first. That is the skill of dissecting a finished paper. Today we turn the
camera around. We watch a paper get *built* — from a vague itch of a question, through the search for a
research design that could actually earn the answer, to the tables that carry it. I am going to use one of
my own working papers as the cadaver on the table, because the one thing a published paper hides best is the
two years of false starts that produced it, and I can tell you about those. The seven-part anatomy you have
been applying *outward* to strangers' papers is the same anatomy I apply *inward* when I decide whether a
question of mine is even worth chasing. Reading well and writing well are the same act run in opposite
directions; today you see both directions at once. Bring the pre-read and your written warm-ups.

---

## (a) Pre-read packet — "What makes an empirical finance paper publishable."

*Read this once before the session. It is one page; read it slowly.*

There is a myth that a top-journal paper is one with a *surprising result*. It is not. Journals are full of
surprising results that nobody believes, and the surprise is precisely why nobody believes them. What gets a
paper into the *Journal of Finance* is not the size of the finding but the *credibility of the argument that
produced it*. A publishable empirical paper is a chain, and the chain is only as strong as its weakest link;
referees attack the weakest link, and a paper lives or dies there. Four links matter, and they are exactly the
four things you have been grading all week, now stated as construction advice rather than reading advice.

**First, a sharp question.** Not a topic — a *question*, one sentence ending in a question mark, naming an
outcome and the one right-hand-side variable whose effect you care about. "I study municipal bonds" is a topic
and a referee's eyes glaze. "Does a *state's social and political climate* change the *interest rate a city pays
to borrow*, even when the city's finances are identical?" is a question: it has an outcome (the borrowing cost),
a key regressor (the social/political factor), and an implied counterfactual (the *same* city under a *different*
climate). A sharp question is testable, it is *falsifiable*, and it is narrow enough that data could plausibly
settle it. The narrowness is a feature. The papers you read this week each answer one small question cleanly;
that is why they are cited thirty years later.

**Second, a credible research design.** This is the link referees break papers on, and it is the heart of
everything Weeks 3 and 4 taught you. Having a question is not having an answer; between them sits the problem
that the thing you care about is tangled with everything else. Cities with different social climates also differ
in income, industry, population trend, state tax law — any of which moves borrowing costs. The design is your
argument that you have isolated *your* variable from that thicket. It is a portfolio sort, a panel regression
with the right fixed effects, an instrument, a difference-in-differences off a policy shock, a discontinuity at
a cutoff — and attached to it, in one sentence, the **identifying assumption**: the condition under which your
estimate equals the causal effect and not a confound wearing its coat. If you cannot write that sentence, you do
not have a design; you have a correlation with ambitions.

**Third, transparent tables.** The result lives in the tables, and an honest table hides nothing. It shows the
key coefficient marching across columns as controls and fixed effects pile on, so the reader can watch whether it
survives or collapses. It reports the sample size at the bottom of every column so the reader can catch the
sample silently changing. It states, in a note, the standard-error flavor — and on panel data that note had better
say *clustered*, at the level the key variable varies, or a Petersen-literate referee will not read past it. A
table that reports only the one specification that worked is not transparent; it is a magic trick, and referees
are trained magicians.

**Fourth, honest robustness.** The difference between a working paper and a published one is mostly the robustness
section — the months spent trying to *kill your own result* before a referee does. You re-run with different
controls, a different sample window, a different SE flavor; you run a placebo where the effect *should* be zero
and check that it is; you confront the most threatening alternative explanation head-on and show the data does not
support it. Honest robustness is not decoration. It is you, the author, doing the referee's job to yourself first,
in public, and reporting the checks that *failed* as well as the ones that passed. That honesty is what makes the
headline believable. As you read today's stretch questions, hold one reflex sharp: *for every claim, what is the
comparison, what is the threat, and what check would make a skeptic stop arguing?*

---

## (b) Three Socratic warm-up questions

*Come with a written sentence or two for each. These have honest answers and dishonest ones, not right and wrong ones.*

1. **Topic vs. question.** Take any subject you care about — Devon's crypto adoption, Priya's climate-insurance
   pricing, Maya's student debt. In one sentence ending in a question mark, turn it from a *topic* into a
   *research question* that names an outcome and one key right-hand-side variable. Then write the one-sentence
   counterfactual it implies: the *same* unit, with *only* that one variable changed. If you cannot write the
   counterfactual, your question is still a topic.

2. **The weakest link.** A friend shows you a paper with a dazzling, counterintuitive finding and a t-statistic of
   8. You are unconvinced. Without seeing the paper, name the *three* places the chain could be weak — question,
   design, tables, robustness — and say which one a t-statistic of 8 tells you *nothing* about. (Hint: precision
   and credibility are different animals; recall Petersen.)

3. **Why a working paper isn't done.** A paper has a sharp question, a clean design, and beautiful tables, and it
   has been "almost finished" for two years. In a sentence or two, guess what is missing — and why that missing
   piece, not the headline result, is what stands between the author and the *Journal of Finance*.

---

## (c) Five-slide deck (speak-from scaffold)

**Slide 1 — "A paper is a chain, not a result."**
- What gets into a top journal is not a *surprising finding* — it is a *credible argument*. Surprises without credibility get ignored.
- The chain has four links: a sharp question, a credible design, transparent tables, honest robustness.
- A referee attacks the *weakest* link; the paper lives or dies there, not on the headline.
- Today: I build one of my own working papers in front of you, link by link, including the false starts a finished paper hides.

**Slide 2 — From itch to question.**
- Every project starts as a vague itch — "something is going on with municipal borrowing." That is a topic, not a paper.
- The work is sharpening: name the *outcome* (a city's borrowing cost), the *one* key regressor (a state social/political factor), and the implied *counterfactual* (same city, different climate).
- A good question is narrow, testable, falsifiable — and a referee can restate it in one sentence.
- The papers you read this week each answer one small question cleanly. That is why they last.

**Slide 3 — The design is the paper.**
- Between question and answer sits the thicket: cities differ in income, industry, tax law — all of which move borrowing costs.
- The design is your argument that you isolated *your* variable from the thicket — a panel with fixed effects, a policy shock / DiD, a cross-sectional comparison with the right controls.
- Attached to it: the *identifying assumption*, one sentence, "this estimate is the causal effect *as long as* ___."
- No design, no paper. A correlation with ambitions is not a finding (Weeks 3–4, pointed at my own data).

**Slide 4 — Tables that hide nothing, robustness that tries to kill the result.**
- Honest table: the key coefficient marching across columns; $N$ at the bottom of each; the SE note saying *clustered*, at the level the key variable varies (Petersen, this week).
- A table reporting only the spec that worked is a magic trick; referees are trained magicians.
- Robustness = me doing the referee's job to myself first, in public: alternative controls, windows, SE flavors, a *placebo* where the effect should be zero.
- The honesty *is* the credibility. Report the checks that failed, not just the ones that passed.

**Slide 5 — Why this is your capstone in miniature.**
- *The Rainbow of Credits* (Gao, Liu & Wang, AEA 2025; target *JF*) is a live paper still being built — you are seeing a real one mid-flight, not a museum piece.
- In Weeks 7–8 you write your *own* paper: real question, real data (CRSP / Compustat / EDGAR / municipal data), a design you can defend, tables you build — bound for the **ASSIP Research Symposium on Wednesday, August 12, 2026** (poster + virtual breakout for remote interns) and an abstract in the **Journal of Student-Scientists' Research (JSSR), GMU Mason Publishing**.
- The seven-part template you read *outward* this week is what I run *inward* on every project of mine before I commit two years to it.
- Read every paper — including your own draft — as though you will defend its tables in a seminar. By August 12 you will.

---

## (d) Three "stretch" questions — building a paper from one of my own

These tie today's construction ideas to a working paper my coauthors and I are still building, offered as a live
worked case of how a question becomes a *Journal of Finance* submission:

> Gao, L., Liu, S., & Wang, Y. "The Rainbow of Credits: Evidence from Municipal Borrowing." (AEA 2025; target
> *Journal of Finance*.)

The setting is the U.S. **municipal bond market** — the market through which states, cities, counties, school
districts, and other public bodies borrow money, by issuing bonds, to build roads, schools, and water systems.
The price of that borrowing is the **yield** an issuer must offer investors, and the natural unit of observation
is a *bond issue* (or an issuer in a given year). The broad question is whether a state's **social and political
climate** — the kind of factor that has nothing mechanical to do with a city's balance sheet — moves the interest
rate that local governments pay to borrow, holding the issuer's actual finances fixed. Data of this kind comes
from municipal-bond issuance and secondary-market trade records (the kind of data assembled from the **MSRB**,
Bloomberg, and bond-deal databases [CHECK: confirm the exact data sources and sample window cited in the current
draft before quoting them]). I will not give you our reported magnitudes — partly because the paper is still in
motion, and mostly because the point today is to practice the *judgment*, not to memorize a coefficient.

**Reason about question-formation, identification, and table-reading only. Do *not* invent or recite specific
reported numbers, sample sizes, or design details you cannot verify — frame every answer as "how I would
design / read this." Mark anything you would need to confirm as [CHECK].**

1. **From topic to question to counterfactual.** (a) "Municipal borrowing" is a *topic*. Write the *research
   question* this paper is built on in one sentence ending in a question mark, naming the **outcome** (what is
   being explained) and the **key right-hand-side variable** (the social/political factor whose effect we care
   about). (b) Now write the **counterfactual** in the potential-outcomes language of Chapter 3.1: take a single
   bond issued by a single city of a given financial quality, and state precisely what *would have* to change and
   what *would have* to stay fixed for the comparison to identify the effect of the social/political factor on
   the yield. (c) Explain why a raw correlation — "cities in states with social factor X pay higher yields" — is
   *not* that effect, and name two concrete confounds (think about what *else* differs across these states:
   income, industry, demographics, state tax treatment, default history) that a raw comparison would blame on the
   social factor.

2. **Choosing the identification strategy.** The honest answer to "how do I identify this?" is "it depends on what
   variation I can find," and a real author tries several. (a) **Cross-sectional design.** Suppose I regress the
   yield on the social/political factor *plus* controls for issuer finances (revenue, debt load, credit rating)
   and fixed effects. Using the CONVENTIONS §4 format — *outcome · key regressor · controls · fixed effects ·
   clustering · sample · identifying assumption in one sentence* — write down what this specification would look
   like, and then state the **identifying assumption** in the form "this estimate equals the causal effect *as
   long as* ___." Why is that assumption hard to defend with a pure cross-section? (b) **A policy / shock-based
   design.** Now imagine a state-level **policy change** that altered the relevant social/political factor in some
   states and not others at a known date. Set it up as the difference-in-differences of Chapter 4.1: what is the
   outcome, who is treated, who is the comparison group, and what does differencing across groups *and* over time
   remove that the cross-section in (a) cannot? State the **parallel-trends** assumption for *this* setting in one
   sentence. (Treat this DiD as a teaching device — "how I would *try* to get cleaner variation" — not as a claim
   about what the current draft does. [CHECK] the design the paper actually uses.) (c) If the policy rolls out at
   *different dates* across states, name the staggered-adoption pitfall from Chapter 4.2 that a naive two-way
   fixed-effects regression would fall into, and say why clustering the standard errors **by state** (Petersen,
   this week; Chapter 4.1 §7) is non-negotiable here.

3. **Reading the tables you would expect.** Suppose I hand you the paper's main results table and you have sixty
   seconds. (a) Following Pack 5's *tables-first* discipline, say — *before* reading any prose — what you would
   look at in order: what is in the column headers, what is in the rows, what is the *one* coefficient that
   carries the paper, and where is the sample size. (b) The key coefficient on the social/political factor will
   (one hopes) march across several columns as controls and fixed effects are added. Explain what you would
   conclude if it *stays stable* across columns versus if it *shrinks toward zero* once issuer-finance controls
   and state fixed effects go in — and connect this to the difference between a result and an artifact of what was
   omitted. (c) Now play referee. Name the **single most threatening alternative explanation** for a nonzero
   coefficient that *survives* the controls (what could move both the social/political factor *and* the yield that
   is not in the regression?), and state the **one robustness check or placebo** you would demand to be convinced —
   a check where, if the social factor were really driving yields, the effect should appear, and where, if it is a
   confound, the effect should *vanish*.

---

## (e) Post-session reflection prompt

*Write ~150–250 words after the session; we will read a few aloud next week.*

Take a question you might actually want to answer in your capstone — yours, or one borrowed from Maya, Devon,
Priya, Sam, or Leah — and build the *first three links of the chain* for it, the way we built them for *Rainbow of
Credits* today. **Question:** sharpen your topic into one sentence ending in a question mark, naming the outcome
and the single key right-hand-side variable, and write the counterfactual it implies — the same unit with *only*
that one variable changed. Be honest about whether you can even state it; if you cannot, the topic is not yet a
paper. **Design:** name the thicket — three things that differ across your units and would confound a raw
comparison — and then propose the cleanest design you can imagine *given data that actually exists*: a panel with
fixed effects, a policy shock you could lean on, a cutoff, a matched comparison. Write the identifying assumption
in the "*as long as* ___" form, and say plainly why it might be false. **Tables and robustness:** sketch the one
table whose headline coefficient would carry your paper — what is in the columns, what is in the rows, where the
sample size sits — and name the *one* robustness check or placebo that would most reassure a hostile referee, and
the one that would most embarrass you if it failed. Finish with the question that is the whole point of today, and
of Weeks 7 and 8: *if I had to defend this paper's tables in a seminar, which link of the chain would I be
attacked on first — and is it strong enough yet to survive?* You do not need an answer you believe. You need to
have looked as hard at your own design as you spent all week looking at Fama and French's.
