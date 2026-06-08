# Mentor Session 6 — "Text as data, and AI without fooling yourself."

*Week 6 live session · 60 minutes · led by Prof. Lei Gao*

All week the raw material changed under your feet. For five weeks "data" meant numbers that arrived
already numeric — a return, a leverage ratio, a yield. This week the data was *prose*: a 10-K running
to fifty thousand words, a product description a firm wrote about itself, a risk-factor section a
lawyer drafted to be read by no one. Hoberg and Phillips turned product descriptions into a map of
who competes with whom. Loughran and McDonald showed that the most popular tool for scoring financial
tone was counting "liability" and "tax" as gloom. And in Chapter 6.5 you met the newest, most powerful,
most dangerous instrument of all — a large language model that will read forty thousand filings for you
overnight and hand back a confident column of labels, some of which are quietly invented. Today we put
those three things together into one discipline. The discipline is this: **a number you extracted from
text is a measurement — a noisy proxy for something you cannot see directly — and an LLM is just a very
fluent measuring instrument that has not been calibrated until you calibrate it.** Everything else today
is the consequence of taking that sentence seriously. Bring the pre-read and your written warm-ups.

---

## (a) Pre-read packet — "A text-derived variable is a measurement, not a fact."

*Read this once before the session. It is one page; read it slowly.*

There is a seductive illusion in text-as-data, and it gets stronger the better your tools get. You point
an instrument — a dictionary, a similarity score, an LLM classifier — at a document, and out comes a
number: tone = −0.04, similarity = 0.31, label = "negative." It *looks* like a fact about the document,
the way the document's filing date is a fact. It is not. It is the output of an instrument, and like every
instrument it has error. Recall the idea from Week 1: when you write down `tone`, you are not observing the
filing's true latent sentiment — you are observing a *noisy proxy* for it, the true thing plus a systematic
bias (maybe your instrument over-calls "negative" on legal boilerplate) plus random noise (re-run the LLM
and the same filing might flip). The instant that proxy enters a regression as a variable, it is a
mismeasured variable, and you already know what mismeasurement does: at best it attenuates your coefficient
toward zero and inflates your standard errors; at worst, if the measurement error is correlated with
something else in the model, it biases the estimate in a direction you cannot even sign. So the right
question is never "is the LLM accurate?" in the abstract. It is: *how accurate is this instrument, on my
data, against truth — and is my downstream result robust to the error I know is there?*

This reframing has a liberating consequence: text-as-data is not a new kind of magic, it is the *same*
measurement discipline you have practiced all camp, applied to a new sensor. The Loughran–McDonald
dictionary is transparent — its "rubric" is a published word list anyone can inspect, so you can see
exactly why a filing scored as it did. An LLM may be *more* accurate than a word list, but it is far *less*
transparent: its rubric is your prompt plus an opaque model whose reasoning you cannot read. Less
transparency raises the bar on validation; it does not lower it. And validation has one non-negotiable
shape. You build a **gold set** — a random sample of documents you label by hand, the closest thing you
have to ground truth. You *split* it, holding out a test set you do not look at while you tune your prompt,
because tuning against the numbers you then report is how you lie to yourself. You compute **precision and
recall on the held-out set**, never bare accuracy — because financial text is almost always imbalanced, and
under imbalance a lazy classifier that labels everything "not-negative" can score 95% accuracy while
catching zero of the cases you actually care about. Only after the instrument clears that bar, *out of
sample*, do you earn the right to run it across the forty thousand documents you never hand-labeled.

Three more disciplines keep the instrument honest, and all three are about not fooling yourself.
**Out-of-sample is the whole game.** A measure tuned on the same data it is tested on is grading itself with
the answer key; report only what survives on data the instrument never saw during development.
**Look-ahead and leakage are the finance-specific trap.** An LLM trained on text through some cutoff date
may "know" the future relative to your sample — it has read what happened to those 2021 stocks. Labeling a
2019 filing's *tone* is comparatively safe (the tone is in the text); *predicting* 2020's returns from that
filing is exactly where hindsight leaks in and manufactures fake performance that evaporates when you trade
it forward. When you retrieve passages, enforce the date filter mechanically: a query dated $t$ never sees a
document dated after $t$. **Disclosure is what makes it science.** The prompt that produced your labels is a
variable definition; freeze it *before* you look at the regression result (or you will, consciously or not,
shop prompts until the coefficient turns significant — p-hacking in a new costume), report it verbatim in an
appendix, pin the exact model version, log every call, and save the labels to disk and treat that file as
your data. As you read today's stretch questions, hold one reflex sharp: *for every text-derived number,
what is it a proxy for, how was it validated, and what would I have to disclose so a referee can judge the
error I could not remove?*

---

## (b) Three Socratic warm-up questions

*Come with a written sentence or two for each. These have honest answers and dishonest ones, not right and wrong ones.*

1. **What is it a proxy for?** Take a text-derived variable from this week — Loughran–McDonald negative
   tone, Hoberg–Phillips product similarity, or an LLM tone label like Leah's. In one sentence, name the
   *true latent quantity* the number is trying to measure (not the formula — the thing in the world). Then
   name one *systematic* way the instrument could be biased (it consistently over- or under-reads the true
   quantity) and one *random* way it could be noisy. Which of the two is more dangerous to a regression, and
   why?

2. **The 95%-accuracy trap.** A classmate reports that their LLM filing-classifier is "94% accurate" and
   wants to put its labels straight into a regression. Only about 6% of the filings in the corpus are truly
   "negative." In two or three sentences, explain why that 94% might be nearly worthless, what *two* numbers
   you would ask to see instead, and on *which* documents those numbers must be computed for you to believe
   them.

3. **The same filing, twice.** You run the same LLM on the same 10-K on Monday and again on Friday and get
   two different labels. A deterministic regression never does this. (a) Name the property of the model that
   causes it, and (b) describe the single change to your *pipeline* — not to the model — that makes the
   labels in your paper reproducible by someone who has only your repository. (Hint: the labels are data;
   what do you do with data?)

---

## (c) Five-slide deck (speak-from scaffold)

**Slide 1 — "A text number is a measurement, not a fact."**
- For five weeks "data" arrived numeric. This week it arrived as prose — and prose has to be *measured* into numbers before it can enter a regression.
- Every text instrument — dictionary, similarity score, LLM label — outputs a *noisy proxy* for a true latent quantity you cannot see directly (Week 1 measurement error, new sensor).
- So a text-derived variable is a *mismeasured regressor*: at best attenuated toward zero with inflated SEs; at worst biased in a direction you can't sign.
- The question is never "is the LLM accurate?" — it's "how accurate, on *my* data, against *truth*, and does my result survive the error I know is there?"

**Slide 2 — The instruments, from transparent to opaque.**
- Loughran–McDonald (Ch 6.3): the rubric *is* a published word list. Fully transparent — you can see exactly why a filing scored as it did. "Liability" counted as gloom is a *visible* bug.
- Hoberg–Phillips (Ch 6.2): prose becomes geometry; similarity is a cosine you can recompute. A measurement paper — judged on "better than what we had, at what?", not on causal identification.
- LLM classifier (Ch 6.5): possibly *more* accurate, definitely *less* transparent — rubric = your prompt + an opaque model. Less transparency *raises* the validation bar, it does not lower it.
- Same discipline across all three; only the opacity — and therefore the burden of proof — changes.

**Slide 3 — Validation, or it didn't happen.**
- Build a **gold set**: a *random* sample you hand-label — the closest thing you have to ground truth (cherry-picked easy cases flatter the instrument).
- **Split it.** Tune the prompt/rubric on a development set; *hold out* a test set you touch exactly once. Tuning against the numbers you report is lying to yourself.
- Report **precision and recall** on the held-out set, never bare accuracy — under imbalance, "94% accurate" can mean "caught zero of the 6% I care about."
- Clear the bar out-of-sample → *then* you've earned the right to run the instrument on the 40,000 documents you never labeled. Not before.

**Slide 4 — Three ways AI fools you, and the guardrail for each.**
- **Look-ahead / leakage:** the model may "know the future" of your sample. Labeling 2019 *tone* is safe; *predicting* 2020 returns from it is contaminated. Guardrail: post-cutoff out-of-sample tests; enforce a date filter in retrieval ($t$ never sees $>t$).
- **Prompt p-hacking:** rewording the rubric until the coefficient turns significant. Guardrail: freeze the prompt against the *gold set* before you look at the regression; report it verbatim.
- **Irreproducibility:** stochastic outputs, silently-updated model versions. Guardrail: pin the version string, log every call, save labels to disk and treat that file as the data.
- The thread: AI is a *co-pilot* — it accelerates work you can verify; it is a hazard the moment you let it replace judgment you don't check.

**Slide 5 — Why this is your capstone's integrity section.**
- I'll walk two of my own papers: one where the outcome — *earnings management of supplier firms* — is itself a **measured construct** (discretionary accruals as a noisy proxy for the unobserved thing the manager is actually doing), and the panel structure dictates the SEs (*Overlapping Institutional Ownership Along the Supply Chain and Earnings Management of Supplier Firms*); and one about using *AI responsibly in finance research and teaching* (*Derivatives Trading Simulation Supported by AI*). The first paper is not text-as-data — but the measurement discipline we built today applies wherever a regression's outcome is a proxy, not a fact.
- Your capstone must *disclose and defend* every way you used AI: writing aid (you own the words) vs. data generation (labels that enter a regression — these demand a validation table).
- The responsible-AI-use disclosure is graded: prompt verbatim, gold-set + held-out sizes, OOS precision/recall, model version pinned, calls logged, citations and figures verified against a primary source.
- The seminar question you'll face in Weeks 7–8: *which text variable would a referee attack first — and can I show its error is small enough not to be driving my result?*

---

## (d) Three "stretch" questions — measurement and responsible AI in two of my own papers

These tie today's ideas to two of my own papers, offered as live worked cases — one of *measuring and
validating a behavioral construct (earnings management) inside a panel*, and one of *using AI responsibly
in research and teaching*:

> Gao, L., Han, J., Kim, J-B., & Pan, T. (2024). Overlapping institutional ownership along the supply
> chain and earnings management of supplier firms. *Journal of Corporate Finance*, 84, 102520.
>
> Gao, L., Gopalakrishnan, S., Ehrlich, M., & Wang, C. (forthcoming). Derivatives Trading Simulation
> Supported by AI. *Journal of Financial Education*.

The first paper asks whether **overlapping institutional ownership along a supply chain** — the situation
where the *same* institutional investors hold large stakes in both a supplier firm and its customer firm —
changes how aggressively the *supplier* firm's managers engage in **earnings management** (the discretionary
slack in accruals with which managers shape the reported earnings number away from the underlying cash
reality). The natural unit of observation is a supplier firm in a given year, embedded in supplier–customer
links, and the key outcome — *earnings management* — is **not directly observable**: it has to be backed out
of accounting data as a residual from a model of "normal" accruals (Jones / modified-Jones discretionary
accruals). That makes it a measurement problem of exactly the same shape as today's text problem — a noisy
proxy for an unseen latent quantity — even though the sensor is an accruals model, not an LLM.

**Reason about measurement, validation, and method only. Do *not* invent or recite specific reported
magnitudes, coefficients, sample sizes, or t-statistics from either paper — frame every answer as "how I
would measure / validate / cluster this." Mark anything you would need to confirm as [CHECK].**

1. **Earnings management as a measured proxy — and how I would validate it.** (a) "Earnings management" is
   not a number that arrives ready-made; it has to be *constructed* from accounting data as the residual of a
   model that predicts a firm's "normal" accruals from its sales growth and fixed assets — what is left over
   is labeled *discretionary* accruals and treated as a proxy for managerial intervention. Pick one concrete
   sensor — the Jones model, the modified-Jones model, or a Dechow–Dichev-style accruals-quality residual —
   and state, in one sentence, the *true latent quantity* the proxy is meant to capture (the thing in the
   world, not the formula). Then name one *systematic* error the proxy could carry (e.g., the model's
   "normal" component is itself misspecified for fast-growing firms, so growth gets relabeled as
   manipulation) and one *random* error (a single year's noisy accrual blip moves the residual). (b)
   Validation looks different from text-as-data here because the outcome is continuous, not a binary label —
   there is no gold set of hand-labeled "yes/no earnings managers." Describe how you would *substitute* for
   that: simulate a panel in which you *plant* a known amount of discretionary accruals in a known subset of
   firm-years and check whether your sensor recovers the planted truth (Lab 4's slogan: when you cannot
   ground-truth in the real world, build a universe where you can); then re-run the sensor under an
   alternative accruals model and report whether the headline correlation moves materially. Which *two*
   numbers would you report on the simulation, and why is "the headline regression coefficient is similar
   across Jones / modified-Jones" the continuous analogue of the precision/recall move you would make on
   labels? (c) Why does the *transparency* of the measure matter to a referee — what can a skeptic check
   about an accruals model whose every coefficient is published, that they *cannot* check about an opaque
   alternative (say, an LLM ranking firms on "earnings-management-y" language), and what would you have to
   disclose to close that gap if you used the opaque sensor instead? Mark as [CHECK] anything about the
   paper's *actual* earnings-management measure you would need to confirm against the published version
   before quoting it.

2. **Panel dependence and clustering — the SE choice the design forces.** This is a panel — the *same* firms
   observed over *many* years, linked into supplier–customer pairs — so the standard-error question from
   Pack 5 (Petersen) is not optional. (a) Using the CONVENTIONS §4 format — *outcome · key regressor ·
   controls · fixed effects · clustering · sample · identifying assumption in one sentence* — sketch what an
   earnings-management-on-supply-chain-common-ownership specification would look like, *leaving the
   clustering slot deliberately open*. (b) Now fill that slot and defend it. Residuals for the *same supplier
   firm* across years are correlated (a firm that runs high discretionary accruals this year tends to next
   year too); residuals may *also* be correlated *across* the linked supplier and customer. Name at least two plausible clustering choices (e.g., by firm, by
   supplier–customer pair, by industry, or two-way) and say, in one sentence each, *what dependence each one
   is meant to absorb* — and why getting this wrong tends to make t-statistics look *more* significant than
   they deserve (recall: clustered SEs are usually *larger* than classical ones). (c) Connect it to today's
   theme: your key regressor, common ownership, is *itself* a measured network variable. In one sentence, say
   why measurement error in a *right-hand-side* variable, combined with an overly optimistic SE, is a
   double-barreled way to fool yourself — and which of the two problems clustering does *not* fix.
   ([CHECK] the paper's actual fixed-effects and clustering choices before asserting them; reason about what
   the design *demands*, not what you recall.)

3. **Using AI without fooling yourself — and without fooling your students.** Now the second paper, on an
   AI-supported derivatives-trading simulation used to *teach*. The responsible-use questions are the same
   ones your capstone will be graded on, in a teaching dress. (a) Draw the bright line from Ch 6.5's
   disclosure checklist: where in such a project is AI a *writing/teaching aid* (you own and verify every
   word — a low bar of "is it true and is it mine?") versus a *generator of data or decisions* (outputs that
   feed an analysis or a grade — a high bar that demands validation)? Give one example of each from a trading
   simulation, and say what disclosure each demands. (b) An AI tutor or simulation that "predicts" market
   moves for students to trade against is a **leakage** minefield. Name the one place training-data
   look-ahead could make the simulation secretly unfair or unrealistic — the model "knowing" how a historical
   episode actually resolved — and describe the cleanest defense (a date-fenced information set; testing on
   post-cutoff episodes the model could not have read). (c) Step back to *reproducibility and honesty*: name
   two concrete things you would have to log or pin so that another instructor — or a referee of the
   education paper — could re-run the simulation and get the *same* experience, given that the AI's outputs
   are stochastic and the model version can silently change. Tie your answer to one line of your own
   capstone's responsible-AI-use disclosure. (Frame everything as "how I would design and disclose this";
   [CHECK] any specific feature of the published simulation before describing it as fact.)

---

## (e) Post-session reflection prompt

*Write ~150–250 words after the session; we will read a few aloud next week.*

Take a text-derived variable you might actually use in your capstone — Maya's fair-lending language in loan
disclosures, Devon's sentiment in on-chain governance forums, Priya's climate-risk wording in 10-K risk
factors, Sam's tone in earnings calls, or Leah's patent-text innovation labels — and write its **honest
measurement card**, the way we read disclosure today. **Proxy:** in one sentence, name the *true latent
quantity* the variable is supposed to measure, and the instrument you would use (a published dictionary, a
similarity score, or an LLM classifier). State one systematic bias and one source of random noise the
instrument carries. **Validation:** describe the gold set you would build, the held-out split, and the *two*
numbers (not accuracy) you would report out-of-sample — and be honest about whether your instrument would
plausibly clear a bar high enough to put its output in a regression. **Without fooling yourself:** name the
one place look-ahead or leakage could contaminate your variable, the one place you might be tempted to shop
prompts until the coefficient cooperated, and the one thing in your pipeline that is irreproducible right
now — and for each, write the single concrete fix (post-cutoff test; freeze-and-disclose the prompt; pin the
version and save the labels to disk). Finish by drafting the two or three sentences of **responsible-AI-use
disclosure** you would put in your capstone's methods section, distinguishing where AI was a writing aid you
own from where it *generated data* you had to validate. Then ask the question that is the whole point of
today: *if a referee could see every prompt I tried and every label I kept, would my result still stand — or
am I trusting an instrument I never calibrated?*
