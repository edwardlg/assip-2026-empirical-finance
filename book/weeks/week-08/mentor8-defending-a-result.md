# Mentor Session 8 — "Defending a result: what a referee actually asks."

*Week 8 live session · 60 minutes · led by Prof. Lei Gao · ASSIP's final mentor session before the
Aug 12 symposium*

Eight weeks ago you computed an average return and thought you had an answer. Today you have a
*result* — a number you can defend sentence by sentence, with a design behind it and an
uncertainty attached. So today we close the arc by teaching the last skill ASSIP owes you: what
happens after the result exists. Yesterday's chapter (8.4) put you on both sides of the referee's
desk — writing a report, then answering one in writing. But the place a result is *actually*
judged is not on paper; it is live, in a room, when someone who wants to disbelieve you starts
asking questions and you have six seconds to answer. That room is the **ASSIP Research Symposium
on Wednesday, August 12, 2026** — the in-person poster session for on-campus interns, the virtual
breakout track for our remote group — where Mason faculty, your peer mentors, your families, the
College of Science leadership, and a roving photographer from Mason News will walk up to your
poster and ask you the things they would ask any researcher whose work they doubt for the right
reasons. That room is Assessment 8, the capstone defense. And that room is every research seminar
I have sat in for twenty years, where the same handful of questions get asked of every paper, mine
included. **The single biggest predictor of whether a result survives is not how clever it is —
it is whether the person who found it knows, before anyone asks, exactly where it is weakest, and
can say so out loud without flinching.** Bring the pre-read, your written warm-ups, and — this is
the one that matters — your own capstone's threats-and-responses table from Chapter 7.5. By the
end of the hour you will have stress-tested your own result against a live referee, which is to
say, against me.

---

## (a) Pre-read packet — "The referee is looking for the reason *not* to believe you."

*Read this once before the session. It is one page; read it slowly, because this is the mindset I
want in the room.*

Here is the thing nobody tells you until you have published a few papers, so I will tell you now: a
referee is not trying to understand your result. A referee is trying to find the *reason not to
believe it.* That sounds adversarial, and in a sense it is — but it is the most useful service in all
of science, and once you stop taking it personally it becomes the thing you cannot work without. The
referee's whole job is to stand between your claim and the permanent record and ask, on behalf of
every future reader who will cite you without checking: *is there a more boring explanation for this
number than the one the author is selling?* Almost always there is at least a candidate. Your job in
the defense is not to pretend there isn't — it is to show you found that candidate first, looked it in
the eye, and either ruled it out or honestly bounded how much it could matter.

So what does a referee actually ask? After refereeing and presenting for two decades, I can tell you
that the hard questions in empirical finance collapse into three families, and they come in this order
of danger.

The first and deadliest is **identification.** This is the question of whether your comparison is
*fair* — whether the difference you measured between treated and untreated, before and after, high and
low, is caused by the thing you claim or by something tangled up with it. "Isn't this just picking up
[some confounder]?" is the identification question wearing its everyday clothes, and it is the
question that kills papers, because if the comparison was never clean, no amount of careful estimation
rescues it. A precise standard error on a confounded coefficient is a precise estimate of nothing.
This is the row at the top of your Chapter 7.5 table, and it is the question I will ask first.

The second is **robustness** — the question of whether your result is *fragile.* Granting the design,
does the number survive the arbitrary choices you made along the way? A different sample filter, a
different control set, a different cutoff, a different flavor of standard error, a different window?
"Does this hold if you [change that one choice]?" The referee asking this suspects you searched, even
quietly, for the specification that gave the prettiest answer — the garden of forking paths from
Chapter 7.3 — and wants to see the result is not balanced on a single knife-edge decision. This is
survivable in a way identification is not: a robustness attack moves a number; an identification attack
removes a comparison.

The third is **alternative explanations** — the question of whether a *different mechanism* produces
the same data. Your story is one of several stories consistent with the pattern, and the referee wants
to know why yours. "Couldn't [this other channel] generate exactly what you see?" The defense here is
rarely to deny the alternative; it is to find the place where your story and theirs make *different*
predictions, and show the data sides with yours.

Internalize the ranking, because it tells you where to spend your scarce composure: identification is
fatal, robustness and alternatives are usually survivable. And hold one reflex sharp as you read
today's questions — *for my own result, what is the one reason a hostile, intelligent reader would
have not to believe it, and have I already written down my answer?* If you have, the defense is just
reading your own script back. If you haven't, that gap is the most important finding of the session.

---

## (b) Three Socratic warm-up questions

*Come with a written sentence or two for each. These have honest answers and evasive ones, not right
and wrong ones.*

1. **The referee's real question, decoded.** A referee writes: *"I worry the effect is driven by
   pre-existing differences between your treated and control groups."* Translate that single sentence
   into plain English — what are they actually accusing your design of? — and then name which of the
   three families it belongs to (identification, robustness, alternative explanation). Now the harder
   half: in one sentence, what is the *single* piece of evidence you could put on a slide that would do
   the most to answer it, and why does producing that evidence beat arguing with the referee in words?

2. **Survivable or fatal — tell them apart in six seconds.** Here are two questions you might get in
   your defense: (i) *"Did you cluster your standard errors at the right level?"* and (ii) *"Couldn't
   the same event that you call your treatment also have changed who is in your sample?"* One you can
   answer with "we checked; it doesn't move," and one, if the questioner is right, sinks the paper. Say
   which is which, and state the general test — in one sentence — that lets you classify *any* incoming
   question as survivable or fatal while it is still being asked. (Hint from Ch 8.5: does it attack a
   number, or the comparison?)

3. **The honest "I don't know."** You will get a question you cannot answer; everyone does. Write the
   *bad* version of your answer (the bluff — a number or a claim invented on the spot) and then the
   *good* version (the located "I don't know"). What three things does the good version contain that
   the bluff doesn't — and why does a room full of people who do this for a living trust your other
   answers *more* after you admit this one limit, not less?

---

## (c) Five-slide deck (speak-from scaffold)

**Slide 1 — "The referee wants a reason not to believe you."**
- After the result exists, the game changes: the room is not trying to *understand* your number, it is trying to find the more boring explanation for it. That is the job, and it is the most useful service in science.
- The defense is not pretending no such explanation exists. It is showing you found it first, looked at it, and either ruled it out or honestly bounded it.
- Three families of question, in order of danger: **identification** (is the comparison fair?), **robustness** (is the number fragile?), **alternative explanations** (does a different mechanism fit the same data?).
- You already did the work — in your Chapter 7.5 threats table. The defense is reading your own script back to a room. Today we rehearse that, on your real result.

**Slide 2 — Identification: the fatal family.**
- "Isn't this just picking up [confounder]?" is the identification question in everyday clothes — and it is the one that *kills*, because a confounded comparison was never clean and no estimation rescues it.
- A precise standard error on a confounded coefficient is a precise estimate of nothing. This is why identification sits above robustness, always.
- The pattern of a strong answer: name the threat (so you don't look surprised) → say what we'd *see* if it were true → show what we actually see → state the residual you still can't rule out. That order makes you look like you saw it coming, because you did.
- The selection version, which you will all face: my subjects didn't get the treatment *randomly* — so why isn't the result just selection? Hold that; it's the spine of today's stretch questions.

**Slide 3 — Robustness & alternatives: usually survivable.**
- **Robustness** = "does it hold if you change that one choice?" The referee suspects you searched for the prettiest spec. Answer with the specification curve from Ch 8.1 — a tight cluster, not one number — and one sentence: "stable across the three choices I worried about most."
- **Alternative explanation** = "couldn't [other channel] produce the same data?" Don't deny it; find where your story and theirs make *different* predictions, and show the data sides with you.
- The tell that separates these from identification: they attack a *number*, not the *comparison*. A moved number is a wound; a removed comparison is a death.
- Pre-empt them on the slide so they're answered before they're asked. The robustness slide is a pre-emptive strike, not an appendix.

**Slide 4 — When the critique is fatal and the attacker is right.**
- It happens. The instinct is to argue harder. That is exactly wrong — defending a broken design in front of a room that can see it is broken turns a damaged paper into a damaged reputation.
- The move: concede at the level the point was made, and retreat to what survives. "You're right I can't rule that out with this design — so the honest reading is a strong *association* consistent with the mechanism, not the clean causal estimate I'd hoped for."
- Almost always there is a retreat position: fatal *to the causal claim* is rarely fatal *to the descriptive one.* "A robust pattern future work with [the better design] should test causally" is real, honest, publishable.
- Know your retreat position before you walk in. That is what the residual-concern column of your threats table was *for.* A conceded fatal critique is a wounded paper but an intact scientist.

**Slide 5 — Now defend your own.**
- You walk in with your capstone result and your Chapter 7.5 threats table. You walk out having defended it against a live referee — me — and having found the one question you could *not* answer cleanly.
- Your capstone is graded on the *defense*, not the cleverness (Assessment 8). In the 8-minute talk, the eight minutes are the easy part; the question period is where the result is judged. The questions are your own threats-table rows, fired back at you.
- The strongest sentence you can say to a hostile question about a number: *"the exact code that produces it is in the packet — clone it and you get the same figure, seed and all."* You invite verification instead of asking for trust. That is the posture of someone with nothing to hide.
- The reflection prompt makes you write the three hardest questions you'll face — and your drafted answers — *before* the conference, when you're calm. Bring it to your defense.

---

## (d) Three "stretch" questions — defending a disclosure result against a referee

These tie today's theme to a paper of mine, offered as a live worked case in exactly the spot where a
referee presses hardest: a result about CEO *behavior* where the CEOs plainly did not get their
characteristics assigned at random. The citation, used verbatim:

> Elnahas, A., Gao, L., Hossain, M. N., & Kim, J-B. (2024). CEO Political Ideology and Voluntary
> Forward-Looking Disclosure. *Journal of Financial and Quantitative Analysis*, 59(8), 3671–3707.

The paper asks whether a CEO's **political orientation** — broadly, whether the executive leans
conservative or liberal — relates to how the firm they run **discloses information**: how much, how
forthcoming, how transparent the firm's communications to the market are. The reason this is the
*perfect* case for today is that it sits squarely in the crosshairs of all three referee families at
once. A skeptic's first reaction is immediate and correct: **CEOs are not handed their politics at
random.** The kind of person who becomes a conservative-leaning CEO may differ from a liberal-leaning
one in a hundred ways — the industry they rose through, the firm that hired them, their age, their risk
appetite — and any of those could drive disclosure directly. That is *selection*, and it is the single
hardest thing this paper had to defend.

**Reason about measurement, identification, selection, and how a defense is *built* — not about what
the paper specifically found. Do NOT invent or recite any specific reported magnitudes, coefficients,
sample sizes, t-statistics, or named control variables from the paper. Frame every answer as "how a
disclosure outcome could be measured," "what a referee would demand," or "how I would defend it." Mark
anything you would need to confirm against the actual paper as [CHECK].**

1. **Measuring the outcome — what number goes in the $y$ column?** Before a referee can attack
   identification, they attack *measurement*, because if "information disclosure" isn't a real number,
   there is nothing to defend. (a) "Information disclosure" is a concept, not a series. Propose two
   *distinct, defensible* ways a researcher could turn "how forthcoming is this firm's communication"
   into a measurable variable on a firm-year — and for each, name one thing a referee would worry the
   measure is *secretly* capturing instead of disclosure (a mechanical confound: firm size, industry
   reporting norms, litigation exposure). (b) A referee's classic measurement challenge is: *"Your
   disclosure measure and your politics measure could both just be proxying for something else — how do
   I know you're measuring what you say?"* In the language of today, which family does that belong to,
   and what is the *cheapest* convincing response — a better measure, or showing the result holds across
   *several* different disclosure measures that share no common mechanical flaw? (c) [CHECK] the paper's
   *actual* disclosure measure(s) and its proxy for CEO political orientation before describing either
   as fact — reason about what a *good* measure must do, not which one the paper uses.

2. **The selection problem, stated and attacked.** Here is the referee's deadliest question, and it is
   the one every one of you will face in some form: *"CEOs don't get their politics randomly assigned.
   Isn't your 'effect' just selection — conservative-leaning CEOs end up at a different kind of firm,
   and it's the firm, not the CEO's politics, doing the disclosing?"* (a) State, in one plain sentence,
   the **identifying assumption** this kind of design needs to survive that question — what would have
   to be true about *how CEOs sort into firms* for the comparison to be fair? (b) Name two concrete
   robustness/identification moves a referee would *demand* to make the selection story less plausible —
   think about what we covered in Weeks 3–4: controlling richly for firm and CEO characteristics (and
   why "we control for it" is a *claim*, not a spell — the omitted-variable ghost from Week 2), firm
   *fixed effects* so the comparison is within-firm, or — the strongest move — finding variation in CEO
   politics that arrives for reasons *plausibly unrelated* to the firm's disclosure tendencies (a CEO
   turnover event, a shock to the executive's environment). For *each* move, say in one sentence what
   threat it kills and what it leaves standing. (c) Now the honest part: selection can rarely be killed
   *completely* with observational data. Following Ch 8.5's retreat logic, what is the most a defensible
   version of this paper should claim — a clean *causal* effect of CEO politics on disclosure, or a
   *robust association* that survives the obvious selection stories — and why is claiming the second,
   honestly, stronger than overclaiming the first? ([CHECK] the paper's actual identification strategy
   before asserting which of these moves it used.)

3. **Building the defense the way the authors had to.** Step into the authors' shoes at the revise-and-
   resubmit stage — exactly the R&R memo of Ch 8.4, now imagined for a real journal. A referee has
   raised the selection concern from Q2 and an *alternative explanation*: *"This isn't about politics at
   all — it's about risk tolerance. Conservative-leaning executives are simply more risk-averse, and
   risk-averse managers disclose differently. You've relabeled risk aversion as politics."* (a) Why is
   that alternative-explanation attack *more* dangerous than a pure robustness complaint, even though
   it doesn't attack the design directly? (Hint: it grants your number and steals your *interpretation*.)
   (b) Describe the *shape* of a convincing answer — not the paper's actual one, which you should
   [CHECK] — using today's rule: find a place where "it's politics" and "it's just risk aversion" make
   *different* predictions, and let the data choose. What kind of test would split those two stories?
   (c) Tie it back to honesty: a referee will *never* be fully satisfied that politics, risk aversion,
   and a dozen correlated CEO traits are perfectly disentangled. Where, exactly, does that residual
   concern belong in the final paper — buried, or stated plainly in the limitations — and why does the
   author who writes "here is the trait I still can't fully separate out" get believed *more* than the
   one who claims a clean sweep? (Frame everything as "how I would defend it"; borrow no magnitudes.)

---

## (e) Post-session reflection prompt

*Write ~250–350 words after the session. This is the one that goes with you into Assessment 8 and the
conference — write it as if your defense depended on it, because it does.*

Write your **defense brief** for your own capstone. Open your Chapter 7.5 threats-and-responses table,
your robustness results from Chapter 8.2, and your one-click packet from Chapter 8.5, and then do the
thing this whole session was pointed at: **anticipate the three hardest questions a referee will ask
about *your* result, and draft your answer to each in full.** For every one of the three, write four
lines. First, the **question itself**, phrased the way a hostile, intelligent reader would actually say
it — not a softball; the real one, the one you hope nobody asks. Second, classify it: is this
**identification** (fatal if lost), **robustness** (a number that might move), or an **alternative
explanation** (someone stealing your interpretation)? Be honest, because the classification decides how
hard you fight. Third, write the **drafted answer in the four-beat shape from Slide 2**: name the
threat so you don't look surprised, say what you'd *see* in the data if it were true, show what you
*actually* see (point to the table, figure, or robustness column — the real number), and state the
**residual concern** you cannot fully rule out. Fourth, and only for whichever of the three is
genuinely *fatal* if the attacker is right: write your **retreat position** — the claim that survives
even if you lose the point, almost always the honest descriptive version ("a robust association future
work should test causally with [the better design]"), so that a conceded critique leaves you a wounded
paper and an intact scientist rather than nothing at all.

Then close with the two sentences that are the whole point of eight weeks. The first is the question I
will actually ask you in your defense, so have the answer ready: *"What is the single best reason,
right now, not to believe your result — and what did you do about it?"* The second is the sentence this
camp existed to let you say truthfully, the one that turns a claim into a result and ends the arc that
started with an eight-percent average: *"Here is what I found, here is exactly why you should believe
it, and here is the one command that lets you check me."* If you can write both sentences honestly, you
are not a student who took a finance course. You are a researcher who can defend a result. Go defend it.
