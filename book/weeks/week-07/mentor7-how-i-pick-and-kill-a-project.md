# Mentor Session 7 — "How I pick a project — and kill one."

*Week 7 live session · 60 minutes · led by Prof. Lei Gao*

Yesterday's chapter handed you a machine for turning a mood into a sentence — the puzzle, the
"so what / who cares / what's new" filter, the four-slot hypothesis grammar, the scoring rubric. I
use a version of it every week. But it leaves out the part of the job no rubric can do for you,
because it is emotional rather than technical: the killing. By the time a paper of mine reaches a
journal, I have abandoned somewhere between ten and thirty ideas — most of them ideas I liked,
several I had already half-built. The biggest difference between people who finish good research and
people who don't is not cleverness at generating ideas; almost everyone can generate ideas. It is
the willingness to kill the ones they've already fallen in love with, early, before the love becomes
sunk cost and the sunk cost becomes a year you can't get back. So today is the unglamorous half of
the funnel. **A researcher's real skill is not having one brilliant idea; it is generating many,
killing most on purpose and without grief, committing hard to one — and knowing the difference
between a project that is merely hard and one that is dead.** Bring the pre-read, your written
warm-ups, and the three or four candidate questions you scored in PS 7.1 — by the end of the hour
you will apply the kill-criteria to your own work, out loud.

---

## (a) Pre-read packet — "The funnel is mostly a furnace."

*Read this once before the session. It is one page; read it slowly.*

Picture the research process as a funnel: wide at the top where ideas go in, narrow at the bottom
where one project comes out. Beginners imagine the funnel's job is to *select* — to recognize the
one good idea among the noise. That is half right. Its real job is to *destroy*: it is a furnace
that burns ten ideas for every one it lets through, and the heat is the point. An idea that has not
survived a serious attempt to kill it is not a good idea, it is an *untested* one, and untested ideas
are where months go to die. So the discipline I want you to learn today is not how to fall in love —
you already know how — it is how to fall *out* of love quickly and cheaply, on paper, before the data
and the deadline make the breakup expensive.

The first enemy of cheap killing is a bias you will recognize from any decision you have ever
regretted: **sunk cost.** Once you have spent a week scraping a dataset, the dataset starts arguing
for its own survival — *I can't quit now, I've already cleaned 40,000 rows.* But the rows you have
already cleaned are gone whether you continue or not; they are not a reason to continue, they are a
reason you *wish* you had a reason. The only honest question at every checkpoint is forward-looking:
*given what I know now, and ignoring everything I've already spent, is this still the best use of the
weeks I have left?* I make myself answer that question on purpose, because my instincts will not ask
it — my instincts will defend the work I've done. Write the cost off. Decide from here.

The second tool is the one I lean on hardest, and it is brutally simple. It is the **"so what" test**,
the same one from Chapter 7.1, but turned into a weapon you point at your *own* project weekly, not
just at the idea once. Force yourself to write the sentence: *"If I find [either result], then
[someone] should [believe or do something different]."* If you cannot fill that in — if the honest
answer is "then I would know a thing, but no one would change their mind or their behavior" — the
project is inert, and inert is a form of dead. The cruelty of the test is that it does not care how
hard you worked or how clean your code is. A flawlessly executed answer to a question nobody asked is
still an answer nobody asked for.

The third tool is a checklist of **fatal flaws** — failure modes that do not weaken a project but end
it, the way a cracked engine block ends a car. Unlike weaknesses you can patch, a fatal flaw means
*stop now.* Learn to spot these in your own work the way you'd spot them in someone else's:

- **No variation in the treatment.** If your key regressor barely moves across your units — every
  firm got the same shock on the same day, every county is "treated" — there is nothing to compare,
  and no design rescues a comparison that doesn't exist.
- **The outcome can't be measured.** If you cannot say what number goes in the $y$ column, you have a
  mood, not a study. "Investor confidence" is not an outcome until you have named the series.
- **Unbreakable confounding (the identification is hopeless).** If your treatment varies for reasons
  hopelessly tangled with the outcome and there is no cutoff, no dated policy, no clean event, and no
  defensible instrument, then the causal version is dead. (The *descriptive* version may live — but
  only if you say so honestly, per CONVENTIONS §4.)
- **The data does not exist, or you can't get it in time.** The most common killer of all. A question
  whose data lives behind a paywall, an IRB you can't clear, or an approval longer than the camp is
  not your question this summer.
- **Reverse causality you cannot break, or a sample so small the standard errors will swallow any
  effect.** Both are diagnoses you can make *before* running anything.

Here is the liberating part, the thing it took me years to believe: **killing an idea is a win, not a
loss.** Every idea you kill on paper in an afternoon is a month you did not waste in the data. The
researchers who look productive are not the ones who never have bad ideas — we all have mostly bad
ideas — they are the ones whose furnace runs hot enough that only the survivors ever see daylight. As
you read today's stretch questions, hold one reflex sharp: *for each of my own candidate questions,
where is the variation, who is the audience, and what is the single fatal flaw most likely to kill it
— and can I kill it this week, on paper, for free?*

---

## (b) Three Socratic warm-up questions

*Come with a written sentence or two for each. These have honest answers and dishonest ones, not right and wrong ones.*

1. **The sunk-cost trap, made personal.** You have spent ten days building a dataset for a project,
   and you now suspect a cleaner, more answerable version of the question would require a *different*
   dataset you don't yet have. In one or two sentences, write the question you should ask yourself at
   that checkpoint — and explain why the ten days you already spent must *not* appear anywhere in that
   question. What is the smallest signal that would tell you to kill it anyway?

2. **"So what" for both answers.** Take your favorite of the candidate questions you scored in PS 7.1.
   Write the sentence "If I find [result A], then someone should ___; if I find [result B, the
   opposite], then someone should ___." Now be honest: did *both* halves fill in, or did only the
   result you're hoping for have consequences? If only one side matters, what does that tell you about
   whether you have a research question or a wish?

3. **Fatal flaw vs. fixable weakness.** Here are two project troubles: (i) "my sample has only 40
   observations" and (ii) "I haven't decided whether to cluster my standard errors by firm or by
   industry." One is potentially fatal and one is a Tuesday-afternoon fix. Say which is which and why
   — and then name the test that, in general, distinguishes a flaw that ends a project from a weakness
   that merely slows it down. (Hint: can you patch it with more work, or is the patch impossible
   *given the world your data comes from*?)

---

## (c) Five-slide deck (speak-from scaffold)

**Slide 1 — "The funnel is mostly a furnace."**
- The research process is a funnel: wide at the top (many ideas), one project out the bottom. Its real job isn't to *select* — it's to *destroy*, burning ~10 ideas per survivor.
- The skill that separates finishers from non-finishers isn't generating ideas — everyone can. It's killing the ones you already love, early and without grief.
- I abandon 10–30 ideas to get one paper to a journal. That's not failure; that's the process working.
- Today is the unglamorous half of yesterday's chapter: not how to pick, but how to *kill* — cheaply, on paper, before the data and the deadline make it expensive.

**Slide 2 — Three enemies of cheap killing.**
- **Sunk cost:** the week you already spent cleaning data argues for its own survival. It shouldn't. The only honest question ignores what's spent: *from here, is this still the best use of the weeks I have left?*
- **The inert project:** flawlessly answering a question nobody asked. The "so what" test, pointed at your *own* project weekly — "if I find either answer, who changes their mind?"
- **The fatal flaw:** not a weakness you patch, but a crack that means *stop now.*
- The discipline isn't pessimism — it's running the furnace hot so only survivors see daylight.

**Slide 3 — The fatal-flaw checklist.**
- **No variation** in the treatment — nothing to compare, no design saves it.
- **Unmeasurable outcome** — no number for the $y$ column means a mood, not a study.
- **Hopeless confounding** — no cutoff, no policy date, no clean event, no instrument → the *causal* claim is dead (the honest *descriptive* version may live, per CONVENTIONS §4).
- **Data you can't get in time** — the most common killer of all.
- Each of these is diagnosable *before* you run a single regression. That's the gift: most fatal flaws are visible on paper.

**Slide 4 — Two of my own funnels.**
- **A clean shock makes a project viable** — *Standing Out from the Crowd via CSR* (JFQA 2023): the question only became answerable when we found a source of price pressure that moves a firm's stock for reasons *unrelated to its fundamentals*. That's what turned a correlation into a design.
- **An idea becomes a paper over years** — *The Rainbow of Credits* (municipal borrowing, AEA 2025, headed for the JF): I'll trace how the question narrowed, which versions I killed, and what survived contact with the data.
- The thread: both lived or died on the same two questions — *where's the clean variation?* and *can I actually measure and get this?*

**Slide 5 — Now kill your own.**
- You walk in with 3–4 candidate questions from PS 7.1. You walk out having killed at least one *on purpose* and committed hard to one, with a runner-up in reserve.
- Commitment is the other half of killing: once the furnace has run, you stop shopping for a better idea and start building. A good question you finish beats a brilliant one you don't.
- Your capstone is graded on the *defense*, not the cleverness — and the first thing I'll ask in Phase 2 is "what did you consider and reject, and why?"
- The reflection prompt makes you write your own kill-or-commit memo. Bring it next week.

---

## (d) Three "stretch" questions — picking and killing, in two of my own projects

These tie today's theme to two of my own projects, offered as live worked cases — one where finding a
*clean source of variation* is what made the project viable at all, and one that shows how a project
*evolves* from a vague idea to a submission over years. The exact citations:

> Gao, L., He, J., & Wu, J. (2023). Standing Out from the Crowd via CSR Engagement: Evidence from
> Non-Fundamental-Driven Price Pressure. *Journal of Financial and Quantitative Analysis*.
>
> Gao, L., Liu, S., & Wang, Y. The Rainbow of Credits: Evidence from Municipal Borrowing. (AEA 2025;
> target *Journal of Finance*).

The first paper asks whether a firm's exposure to **price pressure that is *not* driven by its
fundamentals** — a swing in its stock price caused by something mechanical, like flows into and out of
an index or a fund, rather than by news about the business — changes how the firm engages in
**corporate social responsibility (CSR)**. The whole project hinges on one move you should study
closely: isolating a piece of price movement that is plausibly *unrelated to the firm's underlying
quality*, so that the relationship you measure isn't just "good firms do good things." The second is a
working paper on **why some municipalities borrow at higher cost than others** — and it is the better
case for watching an idea travel the whole funnel, from a puzzle to an AEA presentation to a target at
the top journal in the field.

**Reason about idea-selection, identification, and feasibility only. Do *not* invent or recite specific
reported magnitudes, coefficients, sample sizes, or t-statistics from either project — frame every
answer as "how a clean source of variation makes this viable" or "how I would decide whether to keep
or kill this version." Mark anything you would need to confirm against the actual paper as [CHECK].**

1. **Why the clean shock is what makes the project viable.** Start with the CSR paper's central design
   problem. The naive version of the question — "do firms whose stock price moves a lot engage in more
   CSR?" — is *fatally confounded*, and you should be able to say exactly how: name one confounder that
   would make CSR and price movement move together even if neither caused the other. (a) Now explain, in
   the language of today's session, why a source of price pressure that is *non-fundamental* — that
   moves the price for reasons unrelated to the firm's business prospects — is what *rescues* the
   project from that fatal flaw, turning a hopeless correlation into something with a defensible design.
   What is the identifying assumption, in one sentence, that the non-fundamental variation has to
   satisfy? (b) Apply the funnel backwards, the way Chapter 7.1 taught: if you were a student who had
   the puzzle "maybe stock prices affect firm behavior" but could *not* find any clean, non-fundamental
   source of price variation, would you kill the causal project or redesign it as descriptive — and what
   exactly would the honest descriptive version be allowed to claim? (c) [CHECK] the paper's *actual*
   source of non-fundamental price pressure before describing it as fact — reason about what *kind* of
   variation the design *needs*, not which specific instrument the paper uses.

2. **Watching an idea travel the whole funnel.** Use *The Rainbow of Credits* as the worked case for a
   project's life cycle. (a) The puzzle is something like "municipalities seem to pay very different
   borrowing costs, and not only because some are riskier." Run that puzzle through yesterday's three
   filters out loud — *so what* (who acts differently if either answer is true — a city treasurer, a
   regulator, a bond investor?), *who cares* (whose conversation does municipal-borrowing-cost sit
   inside?), and *what's new* (which flavor of novelty — new data, new period, new outcome, new
   identification — would a project like this most plausibly offer?). (b) Now the funnel's destructive
   half: a question this broad has *many* possible versions, and most must be killed to get to one.
   Name two narrower questions a researcher might carve out of "why do munis borrow at different
   costs," and for *each*, say in one sentence what would most likely kill it — a missing data source, a
   confounder you can't break, or an audience that doesn't exist. (c) Feasibility and the long road:
   this project went from idea to an AEA presentation to a *Journal of Finance* target over a span of
   years, not a summer. Name two concrete things that a multi-year academic project can afford to do
   that *your five-week capstone cannot* — and then state the one principle from today that lets a
   five-week project still be real research despite that gap. ([CHECK] anything about the actual data
   sources, sample, or design of the working paper before asserting it; reason about the *life cycle*,
   not the contents.)

3. **Your own kill decision, under my two questions.** Step back from my projects to yours. Across both
   of my cases, the same two questions decided whether a version lived or died: *where is the clean
   variation?* and *can I actually measure and get this, in the time I have?* (a) Take the candidate
   question from PS 7.1 you are *most* attached to — the one you'd least like to kill — and answer both
   questions about it honestly, in one sentence each. (b) Now do the harder thing: take the candidate
   you scored *lowest*, and instead of discarding it, try to find the one move — a cutoff, a dated
   policy, a clean event, a non-fundamental shock in the spirit of the CSR paper — that would *rescue*
   it. If no such move exists, say so plainly; an idea you can confidently kill is more useful than one
   you keep out of politeness. (c) Tie it to commitment: once you've run your own furnace, what is the
   evidence that would make you *stop shopping* for a better idea and commit — and why is the inability
   to ever commit just as fatal to a five-week project as a bad question? (Frame everything as "how I
   would decide," and do not borrow magnitudes from my papers.)

---

## (e) Post-session reflection prompt

*Write ~200–300 words after the session; we will read a few aloud next week.*

Write your **kill-or-commit memo** for your own capstone. Lay the three or four candidate questions you
scored in PS 7.1 on the table and run each through today's furnace, in writing. For *every* candidate,
do four things. **So what, both ways:** write the sentence "if I find either result, then [someone]
should [believe or do something different]" — and if you can't fill it in for both answers, mark the
candidate inert. **Fatal-flaw scan:** run the checklist from the pre-read (no variation · unmeasurable
outcome · hopeless confounding · data you can't get in time · reverse causality or a sample too small)
and name the single flaw most likely to kill this candidate — then say whether it is *fatal* (stop now)
or a *fixable weakness* (and what the fix is). **Clean variation:** for each surviving candidate, name
where the identifying variation comes from — a cutoff, a dated policy, a clean event, or a
non-fundamental shock like the one that rescued the CSR project — or admit honestly that the project is
descriptive, not causal. Then make the decision the memo exists for: **kill at least one candidate on
purpose**, writing one sentence on *why* and one sentence on what you'd have had to find for it to
survive — and **commit to one**, writing the single defensible sentence-spec in the CONVENTIONS §4
format (outcome · treatment · controls · fixed effects · clustering · sample · identifying assumption),
plus a one-line runner-up you'd fall back to if the data doesn't materialize in Ch 7.2. Be ruthless
about sunk cost: if the candidate you've already invested in is not the best use of the weeks you have
*left*, kill it anyway and say so. Finish with the question that is the whole point of today: *when I
present in Phase 2 and someone asks "what did you consider and reject, and why?" — do I have an answer
that shows I ran the furnace, or did I just keep the first idea I happened to like?*
