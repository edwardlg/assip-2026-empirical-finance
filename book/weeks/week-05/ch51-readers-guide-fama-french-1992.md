# Chapter 5.1 — Reader's Guide: *The Cross-Section of Expected Stock Returns* (Fama & French 1992)

For four weeks you have been a *producer* of empirical work: you built OLS from the design matrix up, learned which standard errors lie and which tell the truth, drew the line between a correlation and a cause, and assembled the modern toolkit — DiD, instruments, regression discontinuity — for prying causal effects out of observational data. Week 5 flips the verb. Now you become a *consumer*. The skill that separates a student who has "taken econometrics" from one who can actually do research is the ability to pick up a frontier paper, read it the way a referee reads it, and decide for yourself whether to believe it. That is a different muscle, and it is trainable.

We train it on a great text, slowly, with someone pointing at the moves. Our great text is Fama and French's 1992 paper: one of the most cited articles in all of finance, it killed a theory that had ruled the field for two decades, and — crucially for us — it uses *exactly the machine you built in Lab 2*. You already own the tools. This chapter teaches you to watch a master use them.

> **Sam's stake in this.** Sam trades on momentum and has a working belief that "riskier stocks pay more." In Lab 2 he built the Fama–MacBeth machine to test the cleanest version of that belief — the CAPM claim that a stock's reward is proportional to its market beta. This paper is the moment the field told Sam his belief was, at best, badly incomplete. Read it as the autopsy on the theory Sam started with.

The paper is:

> **Fama, E. F., & French, K. R. (1992). The Cross-Section of Expected Stock Returns. *Journal of Finance*, 47(2), 427–465.**

We read it through the **Reader's-Guide anatomy** — seven fixed sections we will use for every paper this week. Learn the anatomy here; from now on it is the lens.

---

## 1. Research question

Strip the paper to one sentence and it asks: **what explains why some stocks have higher average returns than others?**

To feel the force of that question, you need the theory it was attacking. The Capital Asset Pricing Model (CAPM), the framework Sam met in Lab 2, gives a sharp and beautiful answer. The *only* thing that should earn a stock a higher average return is its **market beta** $\beta_i$ — its sensitivity to swings in the overall market. Diversifiable, stock-specific risk earns you nothing, because you can diversify it away for free; only the undiversifiable, move-with-the-market part deserves compensation. Written as the relationship Lab 2 estimated,

$$
\mathbb{E}[r_{it}] = \gamma_0 + \gamma_1\,\beta_i,
$$

CAPM predicts $\gamma_1 > 0$ (higher beta, higher reward) and, in strict form, that beta is the *whole story* — add any other firm characteristic to that regression and its slope should be zero. For roughly twenty years this was the organizing fact of asset pricing. It is taught in every finance course. It is the null hypothesis Sam walked in with.

Fama and French ask whether it is *true* in the data, and they ask it with a twist that makes the paper land. By the late 1980s a scattering of studies had noticed two awkward patterns: small firms (low **market capitalization** — share price times shares outstanding, "size" for short) seemed to earn higher average returns than big firms, and "value" firms — those with a high **book-to-market ratio**, the accountant's book value of equity divided by the stock market's valuation of that equity (BE/ME) — seemed to beat "growth" firms. These were treated as anomalies, footnotes to the CAPM. Fama and French's question is whether these "anomalies" are actually the *main event*: once you account for **size** and **book-to-market**, does market beta have anything left to explain at all?

The answer, telegraphed by the paper's own results, is the one that made it famous: **size and book-to-market capture the cross-sectional variation in average returns, and market beta adds essentially nothing once they are controlled for.** Beta, the field's crown jewel, comes out flat. That is why the paper matters. It did not just add a variable; it dethroned one.

---

## 2. Identification strategy

Here is the first habit of a good referee: before you ask "do I believe the result?" ask "what *kind* of claim is this, and what would it take to make it credible?" Weeks 3 and 4 drilled you to hunt for a *causal* design — a treatment, a counterfactual, an as-good-as-random source of variation. **You will not find one here, and you should not expect to.** This is not a flaw in the paper; it is the paper's genre. Fama–French (1992) is a **descriptive / predictive asset-pricing study**. It documents which *firm characteristics* line up with *average returns* in the cross-section. It is the empirical-finance cousin of the regressions in Week 1, not the natural experiments of Week 4. Read it asking "is this relationship real and robust?" — not "is this the causal effect of size on returns?" Keeping that straight is half of reading the paper well.

So what is the empirical machinery? Two pieces, both of which you have already built.

**Piece one: portfolio sorts.** Rather than trust a single regression line, Fama and French first *sort* stocks into buckets and look at average returns bucket by bucket. Rank every stock by size, cut into deciles, and compute each decile's average return — that is a univariate sort on size. The power move, which §5 will dwell on, is the **double sort**: form a grid by sorting on size *and* on pre-formation beta (or on size *and* BE/ME) at the same time, so each cell holds firms that are similar on one dimension and spread out on the other. Sorts are nonparametric — they impose no linear functional form — so they let the data show its shape before any model is forced on it.

**Piece two: Fama–MacBeth cross-sectional regressions.** This is Lab 2, verbatim. Recall the two-pass machine. *Pass 1* estimates each stock's beta from a time-series regression of its returns on the market. *Pass 2* runs, **separately in each month**, a cross-sectional regression of that month's stock returns on the characteristics (beta, log size, log BE/ME, and others), producing a time series of monthly slope estimates $\hat\gamma_{j,t}$. You then average each slope over the months to get the Fama–MacBeth point estimate, and you get its standard error *for free* from the month-to-month scatter:

$$
\hat\gamma_j = \frac{1}{T}\sum_{t=1}^{T}\hat\gamma_{j,t},
\qquad
\widehat{\operatorname{se}}(\hat\gamma_j) = \frac{\operatorname{sd}_t(\hat\gamma_{j,t})}{\sqrt{T}}.
$$

Remember *why* this standard error is the honest one. In any single month every stock is shoved by the same market-wide shock, so the within-month cross-sectional errors are violently correlated — the "time effect" of Ch 2.4. Pooling all stock-months into one giant OLS would treat correlated observations as independent and report a standard error far too small. Fama–MacBeth dissolves that by never comparing *across* months inside a regression: it collapses each month to one slope, then treats the slopes as a little time series. When you read the paper's t-statistics, you are reading **Fama–MacBeth standard errors** — the same object you computed in Lab 2.

One subtlety the paper handles carefully and you should watch for: **pre-formation beta estimation.** A stock's beta is itself an *estimate* from Pass 1, not a known number, and individual-stock betas are noisy. Fama and French assign betas using *portfolios* (a stock inherits the beta of the size–beta portfolio it belongs to, estimated on the portfolio's longer, less noisy return series) and estimate those betas on data from *before* the return month being explained, so the explanatory variable does not peek at the outcome. Hold onto the phrase "beta is an estimate" — it returns with teeth in §6.

The one-line empirical spec, in our Week-1 discipline: **outcome** = a stock's monthly return; **key regressors** = market beta, log size, log BE/ME (plus leverage and E/P in some specs); **controls** = the other characteristics in the same regression; **fixed effects** = none in the FM sense; **standard errors** = Fama–MacBeth (month-to-month scatter of slopes); **sample** = below; **identifying claim** = *none, in the causal sense* — these are predictive associations in the cross-section of returns.

---

## 3. Data

Two databases, stitched together — the workhorse pairing of empirical finance, and the same one your camp uses.

**Returns come from CRSP** (the Center for Research in Security Prices), which has monthly returns and prices for essentially every stock on the major U.S. exchanges. **Book equity comes from Compustat**, the accounting database, which carries each firm's balance-sheet book value of common equity from its annual financial statements. Size (market equity) needs only price and shares, so it comes from CRSP; book-to-market needs both — book equity from Compustat in the numerator, market equity from CRSP in the denominator.

The sample is **nonfinancial firms on the NYSE, AMEX, and NASDAQ**. Financial firms (banks, insurers) are dropped because high leverage means something mechanically different for them than for an industrial firm, so their book-to-market is not comparable. The return tests run on the period from roughly **1963 to 1990** (Fama & French 1992, *Journal of Finance*, 47(2), 427–465), with the start chosen partly because Compustat's coverage of book equity becomes reliable around the early 1960s — a data-availability boundary that, as §6 warns, is not innocent.

The sorting logic is the heart of the data construction. Each year, firms are ranked and binned by **size** and, separately, by **BE/ME**, and there is a deliberate **timing gap**: returns from (roughly) July of year $t$ through June of year $t+1$ are matched to accounting data from the fiscal year ending in calendar year $t-1$. That gap is not bookkeeping fussiness — it is the paper protecting itself against **look-ahead bias**. A firm's annual report for, say, December is not actually public until months later; if you matched December book equity to that same December's return, you would be using information no investor could have had yet, and you would manufacture predictability that does not exist in real time. The lag forces every explanatory variable to be genuinely *knowable* before the returns it is asked to explain. File that move away; you will reuse it any time you merge accounting data to returns.

---

## 4. Table-by-table reading order

New readers read a paper front to back and drown in the introduction. Experienced readers read **tables first**. The prose is the author's argument; the tables are the evidence, and a good paper's tables tell the whole story if you know the order to take them in. Here is the order for this one.

**Start with the sort tables (the size–beta and size–BE/ME portfolios), not the regressions.** These are nearly the first exhibits, and they are the most honest thing in the paper because they assume almost nothing. Read the **size–beta double sort** first, and read it for one specific purpose: *to watch beta die.* Within a row of (roughly) constant size, slide across the beta columns — from low-beta portfolios to high-beta portfolios — and look at whether average return climbs. CAPM says it must climb steeply. What you see is close to **flat**: holding size fixed, sorting on beta buys you little or no spread in average return. That flat row is the headline of the entire paper, and you found it in a table that contains not a single regression coefficient.

Now read the **size–BE/ME sort**. Slide across BE/ME and watch average return *rise* — value (high BE/ME) beats growth (low BE/ME) — and slide down size and watch average return rise as you move toward small firms. Two live patterns, one dead one. You now know the result before reading a word of regression output.

**Then go to the Fama–MacBeth regression tables.** These quantify what the sorts showed and let the characteristics fight each other in one specification. Read the columns as a *sequence of horse races*, not as one table:

- A column with **beta alone** as the regressor. Its slope $\hat\gamma_\beta$ is the formal CAPM test. The reveal: the slope is small and statistically indistinguishable from zero — frequently the wrong sign — once betas are measured carefully. Beta, run by itself, does not earn its keep.
- A column with **log size alone**, and one with **log BE/ME alone**. Both slopes are large and strongly significant (size negative — smaller firms, higher returns; BE/ME positive — higher book-to-market, higher returns). Big, healthy t-statistics here.
- The **kitchen-sink column**: beta, size, and BE/ME together (often with leverage and E/P). This is the decisive cell of the whole paper. Size and BE/ME *keep* their large, significant slopes; beta's slope stays near zero and insignificant. **When beta competes against size and book-to-market, beta loses, and the other two survive together.**

How to spot the headline in a table you have never seen: find the row for the market-beta coefficient, then scan its t-statistic across columns. If it is large alone but collapses toward zero the moment size and BE/ME enter, you have found the paper's thesis with your fingertip. The number that *should* be big under the reigning theory is the number that isn't — that absence is the finding.

---

## 5. What's clever

Three moves separate this paper from the dozen "anomaly" papers that preceded it.

**The double sort to disentangle size from beta.** In the raw data, size and beta are correlated — small firms tend to be high-beta — so a simple sort on beta is partly a disguised sort on size, and vice versa. If you sort on beta alone and see a return spread, you cannot tell whether you are being paid for beta or for smallness. The double sort breaks the tangle: by forming size–beta portfolios, Fama and French create cells that vary in beta while holding size roughly fixed. *Now* the within-size beta comparison is clean — and it is flat. This is the same logic as "controlling for a confounder," done nonparametrically with buckets instead of a regression slope, and it is what lets them say beta's apparent premium was size in disguise.

**Putting book-to-market on the marquee.** BE/ME is a single ratio, computable from two numbers any firm reports, and it turns out to do enormous work — arguably more than size. Elevating it from a curiosity to a headline variable, and showing it survives alongside size when beta does not, gave the field a durable, replicable, *cheap-to-compute* predictor. The 1993 sequel built the famous three-factor model directly on these two variables; this 1992 paper is where they earned their seats.

**The framing — "beta is dead."** Plenty of papers find that variable X predicts returns. Few have the nerve and the evidence to say the *reigning* variable does not. Fama and French stage the result as a direct execution of CAPM's central prediction, and they do it with the field's own preferred weapon — the Fama–MacBeth regression that asset pricers trusted. That is rhetorically devastating: you cannot dismiss the method as some outsider's gimmick when it is the discipline's house technique. The cleverness is as much in the *framing of the contest* as in any single estimate.

---

## 6. What's vulnerable

A referee's job is not to admire; it is to attack the paper at its weakest joints and see if it holds. Four lines of attack, each connecting to something you already know.

**Data-snooping and multiple testing (Week 1).** Size and BE/ME were not the *first* characteristics anyone tried; they are the survivors of a field-wide search across many candidate predictors. When the whole profession ransacks the same dataset for variables that correlate with returns, some will clear a $t > 2$ bar **by chance alone** — the multiple-comparisons problem from Week 1, scaled into a collective, decades-long fishing expedition. A single Fama–MacBeth t-statistic does not adjust for the hundreds of tests the literature ran to find it. The worry is not idle: later work (Harvey, Liu & Zhu 2016[^hlz]) argued the hurdle for "discovering" a return factor should sit well above the conventional $t>2$ precisely because of how much snooping the field has done. The right skeptical question is: *would size and BE/ME survive in data the authors had never seen?* (Largely yes — out-of-sample and international evidence has been kinder to BE/ME than to most factors — but the burden is real.)

**Survivorship and look-ahead in Compustat book equity.** Compustat's historical coverage was backfilled, and backfilling tends to add firms that *survived* long enough to be worth adding — a **survivorship bias** that can distort early-sample book equity. And the whole construction lives or dies on the timing lag from §3: get the gap wrong and you smuggle in **look-ahead bias**, crediting investors with accounting numbers they could not yet have seen. The paper is careful here, but "careful" is a claim to be checked, not assumed, and it is exactly what your replication in §7 will stress-test.

**Risk versus mispricing — the interpretation debate.** Suppose you fully believe the *facts*: value and small stocks earn higher average returns. *Why?* Two camps, never reconciled. **Risk story (the authors' lean):** size and BE/ME proxy for exposures to systematic risks the single market beta misses — distress risk, say — so the extra return is fair compensation for bearing real risk, and CAPM was simply too crude a risk model. **Mispricing story:** investors irrationally over-love glamorous growth firms and under-price beaten-down value firms, so the value premium is a behavioral *mistake* the market slowly corrects, not a risk premium at all. The 1992 paper *documents the pattern but cannot settle which story generates it* — and this is precisely where §2 pays off. Because the design is descriptive, not causal, it has no leverage to adjudicate *mechanism*. A referee should accept the cross-sectional fact and refuse to accept either interpretation as established by this paper alone.

**Errors-in-variables in beta (Week 2 / Week 3).** Here is the subtle one, and it cuts in the paper's favor while still deserving scrutiny. Beta is not observed; it is *estimated* in Pass 1, with noise. From the measurement-error discussion you have met, a regressor measured with random error suffers **attenuation bias** — its estimated slope is pulled toward zero. So a skeptic could object: maybe beta's flat slope is just attenuation, and beta really does matter, the noise is hiding it. Fama and French anticipate this — it is the *reason* they assign betas via portfolios rather than individual stocks, since portfolio betas are far less noisy. A careful referee asks whether that fix is enough, and whether the residual measurement error in beta is large enough to explain away a premium that should have been large. (The honest reading: portfolio grouping shrinks the problem a lot, and the beta premium is so close to zero that attenuation alone is a strained rescue — but you should *see why the objection is the right one to raise* before you decide it fails.)

---

## 7. Three replication exercises

You do not understand a paper until you have tried to rebuild a piece of it. These escalate, and all three live in **`nb5.1`** (`notebooks/week-05/nb5.1-ff92-portfolio-sorts.ipynb`). As always, real CRSP/Compustat stays read-only on GMU infrastructure (Conventions §5); the notebook ships a seeded synthetic fallback with the same schema so every step runs on your laptop, with a Path-A pull for Hopper.

**Exercise 1 — Reproduce a univariate size sort.** Rank firms into size deciles each year, form the ten portfolios, and compute each decile's average monthly return over the sample. Plot average return against the size decile. You should see the line slope *down* — small firms, higher returns. This is the gentlest possible replication: one sort, one picture, and you have recreated the paper's simplest live fact. Then break it on purpose: re-sort using *contemporaneous* market equity instead of lagged, and watch how look-ahead contamination changes the picture.

**Exercise 2 — Build the size–BE/ME double sort.** Construct the $5\times5$ (or decile $\times$ decile) grid sorted on size and book-to-market, honoring the July-to-June timing gap of §3. Print the table of average returns. Read it the way §4 taught: returns rising across BE/ME within each size row, rising down size within each BE/ME column. The deliverable is the headline table, in miniature, built by your own hands — and a one-paragraph note on exactly where you applied the timing lag and why.

**Exercise 3 — Run the Fama–MacBeth horse race.** Reuse your Lab-2 machine. Pass 1: estimate (portfolio-level) pre-formation betas. Pass 2: each month, regress returns on beta, log size, and log BE/ME; collect the monthly slopes; average them; compute the Fama–MacBeth standard errors from the slope scatter. Run three specifications — beta alone, size and BE/ME alone, all three together — and assemble the columns of §4 yourself. Confirm with your own t-statistics that beta's slope collapses while size and BE/ME survive. This is the moment the abstract sentence "beta adds little once you control for size and book-to-market" becomes a number on your own screen.

---

### Read like a referee

Before you leave this paper, sit with three questions — the kind a referee writes in the margin:

1. **Snooping.** If size and BE/ME are the survivors of a field-wide search across many candidate predictors, what evidence in or outside this paper would convince you they are *real* and not two lucky winners of a multiple-testing lottery (Week 1)? What would falsify them?
2. **Mechanism.** The paper shows value and small stocks earn more but cannot say *why*. Design — in words — an additional test that would push you toward the **risk** story over the **mispricing** story, or vice versa. Why can a descriptive cross-sectional design (§2) never fully settle this on its own?
3. **The dog that didn't bark.** Beta's premium is the number that *should* be large under CAPM and isn't. List every reason it could be near zero — true (beta doesn't matter), measurement error attenuating it (Week 2 EIV), or the sort/sample masking it — and say what you would check to tell those apart.

Next stop: **`nb5.1`**, where you stop reading about the sorts and build them.

[^hlz]: Harvey, C. R., Liu, Y., & Zhu, H. (2016). …and the Cross-Section of Expected Returns. *Review of Financial Studies*, 29(1), 5–68.
