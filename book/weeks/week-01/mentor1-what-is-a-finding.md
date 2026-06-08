# Mentor Session 1 — "What Is a Finding?"

*Week 1 · Monday AM group session (~75 min) plus mid-week drop-in office hours · led by Prof. Lei Gao (remote)*

This session is the bridge from the Week-1 inference toolkit (Chapters 1.3–1.5) to the
thing you came here to do: research. You now know how to compute a standard error, a
t-statistic, a p-value, a confidence interval, and how to count the ways a test can lie.
The question for today is what those tools are *for*. They exist to answer one deceptively
hard question: **when is a number a finding, and when is it just noise wearing a nice
outfit?** Bring the pre-read packet and your answers to the three warm-up questions. The
Monday block is where we argue as a full group; the mid-week drop-in is where you bring the
question that did not crystallize in front of the whole cohort. Because this is a full-time
M–F program rather than a once-a-week meeting, expect to revisit threads from this session
informally throughout the week — on Slack, in the daily standup, and during PhD/RA-led
sub-group time.

---

## (a) Pre-read packet — "When is a number a finding?"

*Read this over the weekend before our Monday block. It is one page; read it slowly. Come Monday with the three warm-up answers in writing — we will not lecture from these slides, we will argue from your sentences.*

Here is a true thing about empirical research that no textbook chapter quite tells you
head-on: most numbers are not findings. A number becomes a finding only when it survives a
gauntlet, and the gauntlet has three gates. Almost everything we do this summer at ASSIP is
about walking a number through those gates honestly — and the eight weeks we have together,
9 to 5 Monday through Friday, are enough time to do it right exactly once on the poster you
will present at the August 12 symposium.

**Gate one: could noise alone have produced this?** This is the question Chapter 1.5 built a
machine to answer. Sam's reversal rule earned $+0.08\%$ a day over 252 days — eight basis
points, a positive number, briefly exciting. But daily returns swing by a full percent in
either direction, so the honest question was never "is eight basis points positive?" (it
plainly is) but "is eight basis points *too far from zero to be zero*, given how much this
quantity wobbles?" The t-statistic of $1.69$ is the whole answer compressed into one ruler:
the estimate measured in units of its own standard error. A finding has to clear this gate,
but clearing it is the *easiest* of the three, and clearing it alone proves almost nothing.

**Gate two: is the effect big enough to matter?** A result can be statistically significant
and economically trivial. Scale Sam's backtest to 100,000 days and an edge of eight
*ten-thousandths* of a percent becomes "wildly significant" — a t-statistic of 5, a
microscopic p-value — and it is still worthless, because it dies to the first basis point of
trading costs. Statistical significance is a statement about *precision*; effect size is a
statement about *magnitude*. They answer different questions and they can disagree in both
directions. Asterisks are not findings. A finding comes with a number, in the units of the
problem, and an honest range around it.

**Gate three: would the effect survive the search that found it?** This is the gate that
sends most "findings" to the graveyard. If you test twenty worthless rules and report the one
with $p < 0.05$, there is a 64% chance at least one looked significant by pure luck — and you
have reported a coin flip as a discovery. The reported p-value is then a lie, because it
pretends the other nineteen attempts never happened. The first question a serious reader asks
of any result is not "what was the t-statistic?" but "**how many things did you try before you
found this one?**" A finding has to survive not just one test but the whole search that
surfaced it.

There is a fourth thing lurking behind all three gates, and it is worth naming even though we
will not formalize it until later: passing the gates tells you a number is *real and large*,
not that it is *causal*. When Maya finds a gap in loan-approval rates between two
neighborhoods, walking that gap through the three gates establishes that the gap is too big to
be noise, large enough to harm real borrowers, and not an artifact of trying many
neighborhood pairings. It does *not*, by itself, establish *why* the gap exists — that is the
work of identification, which the rest of the program is largely about. Keep the questions
separate. "Is this a finding?" and "what does this finding mean?" are different questions, and
collapsing them is how confident people end up confidently wrong.

So: a number is a finding when it is *too large to be noise* (gate one), *large enough to
care about* (gate two), and *robust to the search that produced it* (gate three) — and even
then it is a *measured* finding, not yet an *explained* one. The toolkit from this week —
standard errors, size, power, p-values, confidence intervals, the multiple-testing warning —
is exactly the set of instruments that test a number at each gate. In our Monday block we
practice using them not on a homework problem with a known answer, but the way a researcher
does: on a number that nobody has yet decided how to feel about. Bring questions you cannot
finish in the group block to the mid-week drop-in office hours — those are for the
follow-up arguments that need ten focused minutes rather than thirty seconds of cohort
airtime.

---

## (b) Three Socratic warm-up questions

Come with a written sentence or two for each. There are no trick answers; there are honest and
dishonest ones.

1. **Sam's reversal rule cleared the $\alpha=0.05$ bar with $t=1.69$ and $p\approx 0.046$.**
   Suppose you are Sam's skeptical friend. Name *one specific reason* you would still not
   trust the result — and say which of the three gates your reason attacks.

2. **A classmate says: "My signal has $p = 0.001$, so it's a thousand-to-one that it's real."**
   What exactly is wrong with that sentence? Rewrite it into a statement that is actually true.

3. **You have one year of data and a true edge so small that your test would catch it only 28%
   of the time.** You run the test and fail to reject. Did you just learn that the edge is
   zero? If not, what *did* you learn — and what would you need to change to learn more?

---

## (c) Five-slide deck (speak-from scaffold)

**Slide 1 — "A number is not a finding."**
- The instinct we are training: between computing a number and believing it lies a gauntlet.
- Three gates: (1) too big to be noise? (2) big enough to matter? (3) survives the search?
- This week's toolkit is the set of instruments for the gates — not an end in itself.
- Today (Monday block): walk one number through all three gates, out loud, together. The
  drop-in office hours later in the week are where you bring the gate that did not click in
  front of the cohort.

**Slide 2 — Gate one: too big to be noise? (Chapter 1.5 in one breath)**
- The t-statistic is just estimate ÷ its own standard error — distance measured in noise units.
- Sam: $\bar{x}=0.08\%$, $s/\sqrt{N}=0.047\%$, so $t\approx 1.69$. Same average over $N=63$
  days gives $t\approx 0.85$ — *identical edge, opposite verdict*, purely from sample size.
- A result is only as convincing as the $N$ beneath it; the $\sqrt{N}$ in the denominator is
  doing the work.
- The p-value answers one narrow question correctly and refuses the others. Respect the refusal.

**Slide 3 — Gate two: big enough to matter? (significance ≠ importance)**
- Statistical significance = "can I tell it apart from zero?" — controlled by precision/$N$.
- Effect size = "is it large enough to act on?" — a question about magnitude and units.
- The four cases: significant+large (the dream); significant+tiny (huge $N$, worthless edge);
  insignificant+large (the dangerous one — real signal, too noisy to confirm); insignificant+small.
- Always report the estimate *and* its confidence interval, never just a verdict. Asterisks
  are not findings.

**Slide 4 — Gate three: survives the search? (the question that kills most findings)**
- A true null still produces $p<0.05$ a full 5% of the time — p-values are uniform under $H_0$.
- Twenty dead rules, one reported winner: $1-0.95^{20}\approx 64\%$ chance of a spurious "hit."
- The garden of forking paths: even one analysis hides dozens of silent choices.
- Defenses we build later: pre-registration, Bonferroni, false discovery rate. For now, always
  ask "how many things did they try?"

**Slide 5 — What separates a finding from noise.**
- A finding clears all three gates and arrives with a magnitude, an interval, and a search history.
- The same machine — estimate, minus null, over standard error — runs on a mean today and on a
  regression slope $\hat\beta$ in Week 2.
- Research is mostly the discipline of *not fooling yourself* (and you are the easiest person to fool).
- Your job this summer: produce numbers you would defend to a skeptic who tried to break them.

---

## (d) Three "stretch" questions — connecting Week-1 inference to a real paper

These connect everything above to a published result of mine, so you can see the gauntlet
applied to an actual finding rather than a textbook example. The paper is:

> Gao, Han, Li & Zhou (2018), "Market Intraday Momentum," *Journal of Financial Economics*,
> 129(2), 394–414.

The paper studies whether the return over part of the trading day predicts the return over a
later part of the *same* day — an "intraday momentum" pattern. For these questions, **reason
about method and inference only**; do not invent specific magnitudes or results from the paper.
The point is to practice the gauntlet, not to recite findings.

1. **Gate one and gate three together.** Intraday momentum is the kind of pattern you could
   "discover" by slicing the trading day many different ways — many windows, many definitions
   of the predictor and the predicted return. Suppose a researcher reports one slicing with a
   strong t-statistic. Using the multiple-testing logic from Section 1.5.10, explain why a
   single impressive t-statistic is *not* enough here, and describe two concrete things a paper
   could do to convince you the pattern is a finding and not data-snooping. (Think: what would
   make the per-test $\alpha$ trustworthy across the search?)

2. **Power and sample design.** Intraday studies use very large samples (many days, many
   intervals), which pushes hard on the significance-vs-effect-size distinction from Section
   1.5.8. (a) With a very large $N$, why is "statistically significant" almost the wrong thing
   to celebrate, and what should you report *instead* to show the pattern matters? (b) Conversely,
   if you wanted to test whether the pattern holds in a single narrow subsample (say one
   turbulent month), how would the power arithmetic from Section 1.5.4 change what a
   non-rejection there is allowed to mean?

3. **Out-of-sample as the honest test.** A pattern that fits the data it was found in has
   cleared, at most, gate one on that data. Explain — using the idea that a p-value is a random
   variable and that the in-sample search inflates the chance of a spurious winner — why
   evaluating the pattern on data *not used to find it* (a later period, a different market) is
   the most credible way to walk it through gate three. What is the inference analogue of a
   confidence interval here: if the out-of-sample effect is weaker but the interval still
   excludes zero, what have you learned, and what have you not?

---

## (e) Post-session reflection prompt

*Write ~150–250 words after the session; we will read a few aloud next week.*

Pick any empirical claim you have encountered — a headline about markets, a stat from a sports
broadcast, a "this stock always rises on Mondays" tip, a result from your own Week-1 notebook.
Walk it through the three gates out loud on paper. For each gate, write one sentence: (1) Could
noise have produced it — and how would I check? (2) Is the effect large enough to matter, and
in what units? (3) How many things were probably tried before this one surfaced, and how would
I find out? End with a single sentence answering the only question that matters: *given all
that, would I call this a finding, and why?* You do not need to be right. You need to be honest
about what you do and don't yet know — which is the entire job.
