# PS 6.1 — Building the KPSS Patent-Value Measure: Construction, Validation, and Critique

**Course:** 8-Week Empirical Finance Camp · Week 6 · Problem Set 6.1
**Covers:** Ch 6.1 (Reader's Guide: *Technological Innovation, Resource Allocation, and Growth*, Kogan, Papanikolaou, Seru & Stoffman 2017), read through the fixed **Reader's-Guide anatomy** — the seven sections *Research question · Identification strategy · Data · Table-by-table reading order · What's clever · What's vulnerable · Three replication exercises*. You will be asked which section a question lives in, so keep the anatomy at your elbow. The sheet also reaches back to **Week 4** (the event-study market model and the abnormal return) and **Week 1** (the construct-versus-measure gap, measurement validity, and selection / external validity).

**Methods allowed:** only what this week's reading and the prior weeks have given you — the **market model** $R_{it} = a_i + b_i R_{mt} + \varepsilon_{it}$ fit on a pre-event **estimation window**, with the day-by-day **abnormal return** $AR_{it} = R_{it} - (\hat a_i + \hat b_i R_{mt})$ as the firm-specific surprise; the **cumulative abnormal return** $\text{CAR} = \sum_{k} AR_{it_k}$ over a short **event (grant) window**; the conversion of a percentage return into dollars by multiplying by **market capitalization**; the KPSS construction logic of §2 (filter out the market → scale by market cap → inflate for grant-anticipation probability $\pi$); the §1 critique of **patent counts** and **forward citations** as value proxies; the Week-1 vocabulary of **construct vs. measure**, **convergent / predictive validity**, **selection**, and **external validity**; and the variance-of-an-average fact that averaging $n$ roughly-independent noisy pieces shrinks the noise variance by about $1/n$. You do **not** need any structural model of patent value, any asset-pricing factor model beyond the single market regression, or the back-half growth/reallocation econometrics — those are read *about*, not *estimated*, here.

**Total: 100 points.** Point values are stated per problem. Show your reasoning — a correct final number with no derivation earns roughly half credit, because the reasoning *is* the skill we are grading. Solutions are in Appendix E (`E-w6-ps6.1-solutions.md`); attempt every part before you look.

**A note on the numbers.** Kogan, Papanikolaou, Seru & Stoffman's (2017) actual table values are **not** reproduced here. Every figure in this sheet is **illustrative and constructed** — built to behave like the paper's so you can practice the moves, never quoted as the paper's own. When the problem set says "Leah computes," the numbers are Leah's synthetic panel (the seeded fallback in `nb6.1`), not real USPTO/CRSP data. Cite the paper by name: **Kogan, Papanikolaou, Seru & Stoffman (2017)**, abbreviated **KPSS** as in Ch 6.1.

**The difficulty curve.** Problem 1 is the conceptual warm-up — *why* counting patents and even counting citations is the wrong unit, and why a market price fixes it. Problem 2 is the heart of the sheet: a by-hand grant-window event study that rebuilds one patent's dollar value from returns, wiring Week 4 straight into Week 6. Problem 3 asks what evidence would *convince* you the measure is valid (the validation logic of §4). Problem 4 is the referee's attack — three named vulnerabilities from §6, each tied to a prior week. Problem 5 is the aggregation problem: why summing noisy per-patent values into a firm-year panel makes the signal *clearer*, not muddier. Problem 6 asks you to design the replication pipeline that becomes `nb6.1`, in words. We stay with **Leah**, who has wanted a dollar figure for an invention since Week 1; this sheet hands her the number and then teaches her exactly how much to trust it.

---

## Problem 1 — Why a dollar measure? Counts, citations, and the construct–measure gap (14 points)

Before any arithmetic, the genre of the problem. Leah's recurring question — "how much is this invention actually *worth*?" — is a **measurement** question (Ch 6.1 §1), and KPSS's contribution is mostly a measurement strategy, not a causal estimate. Begin by saying clearly what is being measured and why the two standard proxies fail.

**(a) (4 pts)** Name the **construct** Leah ultimately cares about (the unobservable thing) in one phrase, and then state, in one sentence each, the distinct way **patent counts** and **forward citations** each fail as a *measure* of that construct. Your two sentences must name the specific defect for each: what counts weight wrongly, and the *two* defects of citations that §1 insists you be able to recite (one about *timing*, one about what happens to *recent* patents).

**(b) (4 pts)** Explain the core idea — §5's first "clever" move — that lets a stock price stand in for the value of an idea. In two or three sentences, say (i) why a patent *grant* is "news" that the market can react to, (ii) what a large positive reaction versus a near-zero reaction is telling you about the patent, and (iii) why this "outsources the valuation" to the market rather than requiring KPSS to build a structural model of demand, competition, and discount rates.

**(c) (3 pts)** The new measure is denominated in **dollars** and is available the **moment the patent issues**. State the one §5 advantage of dollars over citations that is about *units* (what citations are not denominated in), and the one §5 advantage that is about *speed/timing* (contrast "three days" with "a decade"). In one sentence, connect the speed advantage to *why* it is the thing that makes a long firm-year panel — and hence the growth analysis — possible at all.

**(d) (3 pts)** Frame the whole measure in Week-1 language. State the **construct** and the **measure** as two separate objects, then write the one-sentence honest description of what the KPSS number actually is (the words "market's," "expected," and "at grant" must all appear). Explain in one sentence why dropping any of those three words turns a careful claim into an overclaim — i.e., why the measure is *not* "the value the patent realized."

---

## Problem 2 — Rebuild one patent's value from a grant-window event study (24 points)

This is the core construction, and it is the Week-4 event-study machine pointed at a new event. Leah takes a single patent $j$ granted to firm $f$ (one of her synthetic firms in `nb6.1`). She has already fit the **market model** on a pre-event **estimation window** and obtained
$$
\hat a_f = 0.0000, \qquad \hat b_f = 1.10,
$$
so the firm's *predicted* (normal) return on any day is $\hat R_{ft} = \hat a_f + \hat b_f R_{mt}$. The **grant window** is the three trading days $k\in\{-1,0,+1\}$ centered on the grant date. The realized daily firm returns $R_{ft}$ and the matching market returns $R_{mt}$ over that window are (all in decimal, **illustrative constructed numbers**):

| Event day $k$ | $-1$ | $0$ | $+1$ |
|:---:|:---:|:---:|:---:|
| Firm return $R_{ft}$ | $0.0120$ | $0.0180$ | $0.0070$ |
| Market return $R_{mt}$ | $0.0040$ | $0.0050$ | $0.0030$ |

Firm $f$'s market capitalization at the grant date is $\$8{,}000{,}000{,}000$ (\$8B).

**(a) (6 pts)** For each of the three window days, compute the **abnormal return** $AR_{ft_k} = R_{ft} - (\hat a_f + \hat b_f R_{mt})$. Show the predicted-return piece $\hat b_f R_{mt}$ explicitly for each day. State in one sentence *why* you subtract $\hat b_f R_{mt}$ at all — i.e., which §2 refinement this step is ("filter out the market"), and what would contaminate the raw window return if you skipped it.

**(b) (5 pts)** Sum the three daily abnormal returns into the **cumulative abnormal return** $\text{CAR} = \sum_{k=-1}^{+1} AR_{ft_k}$, and report it as a percentage. Then convert the percentage into a **gross dollar reaction** by multiplying by market cap, $\text{CAR}\times\text{MktCap}_f$. State in one sentence which §2 refinement the market-cap multiplication is ("scale by market cap") and *why* a raw percentage cannot be compared across firms of different sizes.

**(c) (5 pts)** Now apply the **third** refinement. A patent grant is only *partly* a surprise — markets anticipate some grants — so the raw window reaction *understates* the patent's full value. KPSS scale up by $1/\pi$, where $\pi$ is (illustratively) the probability that the observed reaction reflects the genuine patent surprise rather than noise; take $\pi = 0.5$. Compute the final per-patent value $\xi_j = (\text{CAR}\times\text{MktCap}_f)/\pi$. State in one sentence why the adjustment *raises* rather than lowers the estimate, and write the one-sentence interpretation of $\xi_j$ — the careful sentence from Problem 1(d), now attached to a number.

**(d) (5 pts) Stress the construction on purpose.** Leah re-runs the calculation with two other window choices, holding the market model fixed:

- **One-day window** ($k=0$ only): the abnormal return is just $AR_{f,0}$.
- **Five-day window** ($k\in\{-2,\dots,+2\}$): the two extra days have abnormal returns $AR_{f,-2}=+0.005\%$ and $AR_{f,+2}=-0.15\%$ (in percent), which you add to your three-day CAR.

Compute the *gross* dollar reaction (before the $\pi$ inflation) under each of the three windows — one-day, three-day, five-day — and lay the three dollar figures side by side. Then explain in two or three sentences what this spread of answers demonstrates about the measure: which §6 vulnerability it makes concrete ("the measure depends on modeling choices"), why the *short* window is nonetheless the principled default (what a *longer* window lets in), and why "the patent is worth exactly \$X" is therefore the wrong way to talk about any single $\xi_j$.

---

## Problem 3 — What would convince you the measure is valid? (18 points)

A constructed measure is not credible because its author says so; it earns trust by **predicting things it should predict if it really captures patent value** (Ch 6.1 §4, Step 1). This problem is about designing and reading that evidence — the validation logic, not the construction.

**(a) (5 pts) Convergent validity.** Forward citations are the literature's established (if slow) proxy for patent importance. Leah regresses the (log) number of forward citations a patent eventually receives on its KPSS dollar value at grant, across her synthetic patents, and gets a slope of $+0.31$ with a $t$-statistic of $5.8$ (**illustrative**). State which §4 sanity test this is and what *sign and significance* you wanted to see. Then explain in two sentences the precise logic of why agreeing with citations is *reassuring but not sufficient* — i.e., what it would mean if the new measure agreed with the old one only where the old one is trustworthy, and why a measure that merely *reproduced* citations would add nothing.

**(b) (5 pts) Predictive validity.** Ch 6.1 §4 calls one validation "the strongest." Leah regresses firm $f$'s **next-year** profitability on this year's total KPSS innovation value and finds a positive, significant slope (in `nb6.1`, the measure predicts a planted next-year outcome with $t\approx 3.6$, **illustrative**). State why a three-day stock reaction forecasting a *real outcome years out* is stronger evidence of validity than the citation correlation in (a). Your answer must distinguish *what the citation test shows* (agreement with another proxy) from *what the profitability test shows* (agreement with the construct itself), in Week-1 construct-vs-measure language.

**(c) (4 pts) The discriminant check.** A skeptic says the grant-window return might just be reflecting *generic* good-news announcement returns, not the patent. State, in one sentence, the §4 validation aimed at this worry ("does it survive the obvious confound?"), and describe in two sentences one concrete check Leah could run on her synthetic data to show the patent-grant signal is *distinct* from a generic announcement return — for instance, what she would compare grant-window returns *against*.

**(d) (4 pts) Falsifiability.** State the §4 rule for *how* to read these validation tables — for **signs and significance**, not magnitudes you memorize — and explain in two sentences what pattern across the citation, profitability, and confound tests would *break* the measure (cause "the paper to collapse here"). Name which Reader's-Guide anatomy section this entire validation exercise lives in.

---

## Problem 4 — Read like a referee: three named vulnerabilities (24 points)

A referee attacks the paper at its weakest joints (Ch 6.1 §6), and for a measurement paper the joints are mostly *in the measure*. Each part below is one named vulnerability tied to a prior week. Leah must say *what could be wrong* and *what she would check* — not merely admire the result.

**(a) (8 pts) Expectations, not realized value (Week 1 — measurement validity).** §6 calls this "the single most important caveat."
&nbsp;&nbsp;(i) State precisely what the grant-window return *is* a forecast *of*, and what it is *not* (the gap between the **construct** — true realized economic value — and the **measure** — a three-day price reaction). (2 pts)
&nbsp;&nbsp;(ii) Give a concrete example in Leah's terms of a patent that would carry a *high* KPSS value yet turn out to be worth little, and explain in one sentence which direction the measure's error goes for "flashy" patents the market over-loves at grant. (3 pts)
&nbsp;&nbsp;(iii) Design — in words — the check from the "Read like a referee" box: using *later* outcomes (realized profits, eventual citations, litigation), how would Leah test whether the market's grant-window forecasts are, on average, **unbiased** or **systematically too high** for some kinds of patents? Then state the deep reason the measure can **never, by itself**, distinguish "the market was right" from "the market was wrong but *consistently* wrong." (3 pts)

**(b) (8 pts) Confounding news in the window (Week 4 — event-study identification).**
&nbsp;&nbsp;(i) State the identifying assumption the whole grant-window design rests on (the §2 one-sentence assumption: what is the *only* value-relevant news allowed in the window?). (2 pts)
&nbsp;&nbsp;(ii) Name two concrete kinds of *other* news that could land in or near the grant window and contaminate the abnormal return, and explain in one sentence how that contamination corrupts $\xi_j$. (3 pts)
&nbsp;&nbsp;(iii) §6 says the short window and aggregation are the two *defenses*, but warns one kind of contamination "would not wash out." Distinguish **idiosyncratic** confounds (which averaging over many patents removes) from **systematic** confounds (which it does not), and state which one is the genuinely dangerous case — connecting to the `nb6.1` "break it" exercise where contamination *correlated with* true value is the one that survives aggregation. (3 pts)

**(c) (8 pts) Selection and efficient markets (Week 1 — external validity; and circularity).**
&nbsp;&nbsp;(i) §6 lists **three** stacked selection screens that decide which patents even *get* a value. Name all three, and write one sentence stating the population the firm-year value panel actually represents (it is not "all innovation"). (3 pts)
&nbsp;&nbsp;(ii) State one growth/reallocation conclusion you would *not* be willing to extend to the whole economy on this panel, and why — tying it to the screens in (i). (2 pts)
&nbsp;&nbsp;(iii) The measure *assumes* the market prices the patent correctly and promptly at grant. Explain in two sentences the **circularity** this creates: why can the KPSS measure never be used to *test* market efficiency, and what does "efficient markets cuts both ways" mean for the measure when markets are instead *slow* (attenuation) versus *over-reacting* (inflation)? (3 pts)

---

## Problem 5 — Aggregation: why summing noise sharpens the signal (10 points)

The measure is built at the **patent level**, but every economic result is at the **firm-year level** (Ch 6.1 §3): you sum each patent's $\xi_j$ over the patents a firm is granted in a year. This problem is about *why* that aggregation is not just bookkeeping — it is the second defense against the noise of §6, and it is why the firm-year panel is the central data object.

Leah's `nb6.1` reports that her per-patent reconstruction recovers the *true* planted value with a correlation of only about $0.4$, but her **firm-year** totals recover the true firm-year value with a correlation of about $0.72$ (**illustrative**, from the notebook). The construction did not change — only the unit of aggregation did.

**(a) (5 pts)** Model the per-patent value as $\hat\xi_j = \xi_j^{\text{true}} + e_j$, where $e_j$ is measurement noise (window confounds, model error) with standard deviation $\sigma$, roughly independent across patents. Using the variance-of-an-average fact, explain why the **average** per-patent noise across the $n$ patents a firm is granted in a year has standard deviation $\sigma/\sqrt{n}$, and fill in the table for the *factor* by which averaging shrinks the noise standard deviation:

| Patents in firm-year, $n$ | $1$ | $4$ | $25$ | $100$ |
|:---:|:---:|:---:|:---:|:---:|
| Noise-SD shrink factor $1/\sqrt{n}$ | ? | ? | ? | ? |

**(b) (3 pts)** State in one sentence the assumption about the noise $e_j$ that makes the $1/\sqrt{n}$ shrinkage work, and then connect it back to Problem 4(b): which *kind* of confound (idiosyncratic vs. systematic) does aggregation defeat, and which does it leave untouched? Explain in one sentence why this is the same distinction that decides whether the firm-year panel can be trusted.

**(c) (2 pts)** Use part (a) to explain, in one or two sentences, *why* Leah's firm-year correlation ($\approx 0.72$) is so much higher than her per-patent correlation ($\approx 0.4$) even though "the construction did not change." Then state the one-sentence design lesson for her capstone: when a per-unit measure is noisy but unbiased, what does aggregating to a coarser unit buy you, and what does it cost you (what question can the firm-year panel *no longer* answer)?

---

## Problem 6 — Design the replication pipeline for `nb6.1` (10 points)

You are about to build (or have just read) `nb6.1` (`notebooks/week-06/nb6.1-patent-value-panel.ipynb`), the notebook that turns Ch 6.1 §7's exercises into your own numbers. Write the **design in words** — the pipeline, the choices, the checks. **No full code**; a few variable names or one-line pseudocode steps are fine, but the deliverable is a clear specification a teammate could implement, mapped onto the three §7 exercises.

**(a) (4 pts) Inspect and aggregate (§7 Exercise 1).** In ordered steps, describe how to go from a patent-level value file to the firm-year value panel. Your steps must (i) say what to plot *first* and what you expect that plot to show (recall §7: the distribution of per-patent values is "wildly right-skewed" — state why that skew is the whole motivation for not counting patents equally), (ii) state the aggregation operation (sum $\xi_j$ within firm and year), and (iii) name the two sanity checks §7 demands — the top-ten firm-years "do the names make sense?" check, and the note on *which* patents **lack** a value and **why** (the selection of §6).

**(b) (4 pts) Rebuild and stress one patent's value (§7 Exercise 2).** Describe the event-study reconstruction you implemented by hand in Problem 2, as a pipeline: which window the market model is fit on, the gap before the event, the grant window, the CAR, the market-cap multiplication, and the comparison of your hand-built $\xi_j$ to the published KPSS value. Then name the two construction choices §7 tells you to *vary on purpose* to watch the estimate move (the lesson of Problem 2(d)).

**(c) (2 pts) Validate, then break it; and data discipline (§7 Exercise 3 + Conventions §5).** State the validation regression (a future outcome on this year's value) and the "break it" manipulation (inject simulated earnings-announcement returns into a subset of grant windows and watch the validation degrade — Problem 4(b)). Then state the two things the notebook must do so it (i) runs end-to-end on a student laptop with no licensed data, and (ii) is honest about not fabricating real numbers — recalling that real CRSP daily returns stay read-only on GMU infrastructure (Conventions §5) and the public KPSS dataset is a Path-A pull.

---

*End of PS 6.1. When you have attempted everything, check yourself against `book/appendices/E-solutions-manual/E-w6-ps6.1-solutions.md`. The arithmetic in Problem 2 (and the shrink factors in Problem 5) can be confirmed on paper or in a few lines of Python; the construction, validation, and "break it" steps come alive in `nb6.1` (`notebooks/week-06/nb6.1-patent-value-panel.ipynb`), where you simulate patent grants with a known "true" value baked in, rebuild each patent's value from a grant-window market-model event study, aggregate to the firm-year panel, confirm the measure predicts a planted future outcome, and then contaminate a slice of the grant windows on purpose to watch the validation degrade — the moment Kogan, Papanikolaou, Seru & Stoffman (2017) stops being a paper you read and becomes a measure you built.*
