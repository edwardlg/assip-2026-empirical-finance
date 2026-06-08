# Chapter 6.1 — Reader's Guide: *Technological Innovation, Resource Allocation, and Growth* (Kogan, Papanikolaou, Seru & Stoffman 2017)

Week 5 handed you a lens — the seven-part Reader's-Guide anatomy — and four classic papers to practice it on. Week 6 keeps the lens but turns it on a harder, more modern problem: **measurement**. Every paper you read last week took its key variable as given. Returns came from CRSP, book equity from Compustat; nobody had to *invent* the number. This week's papers are different. Their central act is to **build a variable that did not exist before**, out of data that was never meant to measure the thing they want. That is the frontier skill, and it is the skill your Week-7 capstone will live or die on. So we open Week 6 with the paper that, more than any other in the last decade, taught empirical finance how to *measure an idea*.

> **Leah's stake in this.** Leah cares about patents and innovation, and in Week 1 she ran headfirst into the oldest problem in the field: how do you count innovation? The obvious answer — *count patents* — treats a throwaway design tweak and the transistor as one unit each. The second answer — *count forward citations* — is better but slow (citations accrue over a decade) and still measures attention, not dollars. Leah's question all along has been, "How much is this invention actually *worth*?" This paper gives her a number, and the trick behind that number is one she already met in Week 4: an event study.

The paper is:

> **Kogan, L., Papanikolaou, D., Seru, A., & Stoffman, N. (2017). Technological Innovation, Resource Allocation, and Growth. *Quarterly Journal of Economics*, 132(2), 665–712.**

We will call it **KPSS** throughout. Read it through the same anatomy as last week — the order is the order in which a claim must survive scrutiny.

---

## 1. Research question

Strip the paper to one sentence and it asks: **how do you measure the economic *value* of a single patent — not whether it exists, not how often it is cited, but how many dollars it is worth — and once you can, what does the flow of valuable innovation tell us about growth and the reallocation of resources across firms?**

There are really two questions stacked on top of each other, and you should keep them separate while you read, because the paper's contribution is mostly in the first.

The **measurement question** comes first, and it is the one Leah has been circling since Week 1. Innovation is the engine of long-run growth, but it is maddeningly hard to quantify. The two standard proxies both fail in instructive ways. **Patent counts** weight every patent equally — a firm with a hundred trivial patents looks more innovative than a firm with the one patent that defined a decade. **Citation counts** (how many later patents cite this one) are a real improvement, the workhorse of the innovation literature, and they do track importance. But they have two defects you should be able to name: they are *slow* — a patent's citations accumulate over ten or more years, so you cannot value a recent patent in real time — and they are *truncated* — recent patents look artificially uncited simply because the future has not happened yet. Neither proxy is denominated in the unit anyone actually cares about, which is **money**. So the first question is sharp: *can we put a dollar value on each patent, in real time, the moment it is granted?*

The **economics question** comes second and rides on the answer to the first. *Once* you have a firm-by-firm, year-by-year flow of innovation measured in dollars, you can ask the things macro-finance has always wanted to ask but lacked the data to: Does a surge of valuable innovation at a firm predict that the firm grows, that its competitors shrink, that resources (labor, capital) flow toward the innovator? Is innovation **creative destruction** — one firm's gain coming partly at rivals' expense — visible in the data? The outcome here is firm growth and reallocation; the key right-hand-side variable is the new patent-value measure. But notice the dependence: the second question is only as credible as the variable built to answer the first. **That is why a referee spends most of her energy on the measure, and so will we.**

---

## 2. Identification strategy

Here is the first habit Week 5 drilled: before asking "do I believe it?", ask "what *kind* of claim is this?" The headline contribution of KPSS is **not** a causal estimate in the Week-3/Week-4 sense. It is a **measurement strategy** — a recipe for turning observable data into a number that proxies an unobservable (the economic value of an invention). So the thing that plays the role of an "identifying assumption" here is the assumption that *makes the recipe valid*. Pin that down and you have understood the paper.

**The clever move: let the stock market value the patent for you.** When the U.S. Patent and Trademark Office grants a patent to a publicly traded firm, that grant is *news*. The market did not know for certain the patent would issue, or on exactly what claims; the grant resolves some of that uncertainty. If the patent is valuable, the firm's stock should jump when the grant becomes public; if it is worthless, the stock should not move. So KPSS reads the **stock-market reaction in a short window around the patent-grant date** as the market's real-time, dollar-denominated estimate of what that patent is worth. This is exactly the **event-study logic from Week 4**: pick an event date, define a narrow window around it, and measure the *abnormal* return — the part of the return that is not explained by the market's normal movement on those days. The intuition is the same one Leah met for corporate events; here the "event" is a patent grant, and the abnormal return *is* the valuation.

Two refinements turn that intuition into a usable number, and you should be able to recite both.

**Refinement one: filter out the market.** A stock can move during the grant window for reasons that have nothing to do with the patent — the whole market rallied, or the firm's sector moved. The raw window return is therefore contaminated. KPSS strips out the market's contribution, leaving the **idiosyncratic** (firm-specific) component of the window return — the abnormal return $R^{e}$ in the language of Week 4. This is the same discipline as the market model: $R_{it} = a_i + b_i R_{mt} + \varepsilon_{it}$, where the residual $\varepsilon_{it}$ is the firm-specific surprise. The patent's value lives in the residual, not the raw return.

**Refinement two: scale and adjust for surprise.** A 1% jump means very different dollar amounts for a \$10B firm and a \$200M firm, so the window return is multiplied by **market capitalization** to convert a percentage into dollars. And because a patent grant is only *partly* a surprise — markets anticipate some grants — the raw reaction understates the patent's full value; KPSS scales up by an estimate of the probability that the reaction reflects the patent rather than noise, recovering an expected dollar value. The end product, per patent $j$ of firm $f$, is a dollar figure $\xi_j$ [CHECK exact symbol] interpretable as *the market's estimate of the private value of patent $j$ to firm $f$*. Sum these over all patents a firm is granted in a year and you have a **firm-level, year-level panel of innovation value** — the central data object the rest of the paper, and `nb6.1`, are built on.

State the assumption that makes this valid, in one sentence, Week-5 style: **the abnormal stock return in the grant window equals the market's unbiased estimate of the patent's economic value — *as long as* markets are efficient enough to impound the patent's value at grant, and no other value-relevant news contaminates the window.** That single sentence is where §6 will aim its fire. Note what it is *not*: it is not a claim that the patent *caused* the firm to grow. The growth and reallocation results in the back half of the paper are correlational associations built on top of the measure, and KPSS is appropriately careful about how strongly to read them.

The one-line spec, in our Week-1 discipline. For the **measure**: outcome (constructed) = dollar value per patent; raw input = idiosyncratic stock return in a short window around the grant date; adjustments = market-filtered, scaled by market cap, inflated for grant-anticipation probability; sample = patents granted to CRSP-listed firms; validating assumption = market efficiency over the short window with no confounding news. For the **growth results**: outcome = firm output/growth and reallocation measures; key regressor = the new patent-value flow; these are predictive associations, *not* identified causal effects.

---

## 3. Data

Three sources, stitched together — and the stitching is itself a contribution.

**Patents come from the USPTO.** KPSS use the universe of U.S. patents over a long span (roughly the mid-1920s onward for the grant-based measure, with the citation-rich modern era from the 1970s [CHECK exact coverage years]). Each patent carries a **grant date** — the day the USPTO officially issued it — and this date is the linchpin of the whole design, because it is the "event date" the event study fires on. A patent also carries an application date, an assignee (the owner), and the technology class; the grant date is what makes the market reaction datable.

**Stock returns come from CRSP** — the same daily-return database Sam and Leah have used since Week 1. KPSS need *daily* returns (not the monthly returns of Fama–French) because the event window is only a few trading days wide; you cannot read a three-day reaction off monthly data. The merge requires matching each patent's assignee to its CRSP-listed firm, a non-trivial name-matching job (firms change names, merge, spin off), and it mechanically restricts the value measure to patents owned by **publicly traded** firms — a selection issue §6 will return to.

**The public KPSS patent-value dataset.** This is the part that made the paper infrastructure rather than just a result. Having built the firm-by-year value panel, the authors **released it publicly** — the patent-level dollar-value estimates, downloadable, regularly extended. Dozens of later papers in finance, economics, and management use "the KPSS measure" off the shelf. When a paper hands the profession a *dataset* and not just a finding, its citation count and its influence decouple from any single table: people cite it because they *use* it. Keep this in mind in §5; the dataset is half the contribution.

The unit of observation depends on which part of the paper you are reading. The measure is built at the **patent level** (one row per granted patent, with its dollar value); the economic analysis is at the **firm-year level** (aggregating patents to firms) and, for growth, at the **aggregate/economy level**. Watch which unit a given table is using — it changes what the standard errors should be clustered on.

A filter worth flagging now, because filters are levers: the value measure exists *only for patents granted to public firms with usable CRSP returns around the grant date*. Private firms, universities, and foreign assignees without a U.S. listing drop out. That is not a bug the authors hid — it is intrinsic to a market-based measure — but it bounds the population the panel describes, and you must say so out loud when you use it.

---

## 4. Table-by-table reading order

New readers start at the introduction and drown. You start at the exhibits, and for this paper there is a *specific* order dictated by the two-questions structure of §1: **read the measure-validation evidence first, the economics second.** If the measure is not credible, nothing downstream matters, so that is where a referee looks first.

**Step 1 — Find the validation exhibits: does the dollar value behave like a value should?** This is the make-or-break evidence and it usually comes early. A constructed measure earns trust by predicting things it *should* predict if it really captures patent value. Read these as a checklist of sanity tests:

- **Does the market-based value correlate with forward citations?** Citations are the literature's established (if slow) proxy for patent importance. If KPSS's dollar value rises with the number of future citations a patent receives, the new measure agrees with the old one *where the old one is trustworthy* — convergent validity. Look for the positive, significant relationship between value and citations.
- **Does it predict future profitability and growth?** A patent the market valued highly at grant should be followed by higher future profits, R&D productivity, or output for the owning firm. This is the strongest validation: the measure, built from a three-day stock reaction, forecasts real outcomes years out.
- **Does it survive the obvious confound?** The window return could just be reflecting *other* contemporaneous news. Watch for the authors' attempts to show the patent-grant signal is distinct from generic announcement returns.

Read these tables for *signs and significance*, not for magnitudes you will memorize. The pattern that matters is: value-measure positively and significantly predicts citations, profits, and growth. If that pattern holds, the measure has earned its place; if it were flat, the paper would collapse here.

**Step 2 — The asset-pricing exhibits.** Having validated the measure, KPSS show it carries information for *returns*: firms doing more (high-value) innovation, or firms exposed to *others'* innovation, have different return profiles. This connects the innovation measure to the cross-section of expected returns you met in Week 5 (Fama–French). Read for whether an innovation-based sort produces a return spread.

**Step 3 — The growth and reallocation exhibits (the economics payoff).** These are the tables that justify the title. Look for: a firm's innovation predicting its *own* future growth (the innovator expands), and — the creative-destruction signature — a firm's innovation predicting that *competitors* lose ground, and that resources reallocate toward innovators. At the aggregate level, look for the link between the economy-wide flow of patent value and **measured productivity/output growth**. These are the most interpretively loaded tables, so read them most skeptically (see §6): they are associations consistent with creative destruction, not an experiment that isolates it.

**How to spot the headline in a table you have never seen.** For this paper the "headline" is split. The *measurement* headline is the validation table where the market-based value predicts forward citations and future profits — point to the value coefficient and read its sign and t-stat. The *economics* headline is the reallocation table where one firm's innovation predicts rivals' decline. If the first broke, the paper is a non-starter; if the second broke, the paper would still stand as a measurement contribution. Knowing which table carries which claim is most of reading KPSS well.

---

## 5. What's clever

Three moves separate KPSS from the long line of innovation papers that counted patents and citations.

**Using market prices as a real-time valuation of innovation.** The deep idea is that a competitive stock market is a forecasting machine that has *already done the hard work* of valuing a patent — you just have to read the price. Instead of building a structural model of how much a patent is worth (which would require assumptions about demand, competition, and discount rates that nobody can defend), KPSS outsource the valuation to the thousands of investors who collectively set the price, and they extract that valuation with the cleanest possible tool: the abnormal return in a tight window, where confounds have the least time to creep in. This is the same philosophy as an event study, applied to a variable — *innovation value* — that the field had despaired of measuring. It converts an unobservable into an observable by finding the moment the market reveals its estimate.

**Turning a slow, truncated proxy into a fast, real-time one.** Citations take a decade to accrue and are truncated for recent patents; a stock reaction happens in three days and is available the moment the patent issues. By anchoring on the grant date, KPSS get a value for *every* patent *immediately*, including last year's. That is what makes a long, dense panel possible — and a panel is what you need to study growth and reallocation, which play out year by year. The measure is not just *better* than citations; it is available on a timescale citations can never match.

**Releasing the dataset as public infrastructure.** This is the move with the longest half-life. By publishing the patent-level value estimates and keeping them updated, the authors made their measure a *common good* the whole profession builds on. The cleverness here is strategic as much as technical: a public dataset compounds. Every paper that uses "the KPSS measure" validates it again by using it, and the measure becomes a standard the way CRSP returns are a standard. When you reach your capstone, notice the lesson — a well-constructed, well-documented, openly shared variable can be a larger contribution than any single regression.

---

## 6. What's vulnerable

A referee's job is to attack the paper at its weakest joint and see if it holds. The joints here are mostly in the measure — which is exactly where you'd expect the soft spots in a measurement paper — and each connects to something you already know.

**The window captures *expectations*, not realized value (Week 1 — measurement validity).** The single most important caveat, and the authors are explicit about it: the grant-window return is the market's *forecast* of the patent's value, formed in three days with the information available then. It is not the value the patent *ultimately* realized. If the market is systematically too optimistic about flashy patents and too pessimistic about quiet ones, the measure inherits that bias. A patent that the market loved at grant and that later flopped still gets a high KPSS value. The measure is therefore best read as "the market's expected private value at grant," and any sentence that drops the words "expected" and "market's" is overclaiming. This is the gap between the *construct* (true economic value) and the *measure* (a three-day price reaction), and naming that gap is straight out of Week 1.

**Confounding news in the window (Week 4 — event-study identification).** The whole design assumes the only value-relevant news in the short window is the patent grant. But firms release earnings, announce deals, and get analyst revisions on ordinary days too. If such news clusters near grant dates — or just lands in the window by chance — the abnormal return mixes the patent's value with the other news, and the measure is contaminated. The short window helps (less time for confounds), and aggregating over many patents averages out *idiosyncratic* confounds, but *systematic* contamination would not wash out. The right skeptical question is: *what evidence rules out that grant-window returns are driven by something other than the patent?* — and you should check how hard the paper works to answer it.

**Selection: only granted patents of public firms (Week 1 / external validity).** Three selection screens stack up. First, only *granted* patents get a value — applications that were rejected or abandoned (and the strategic decision to even apply) are invisible. Second, only patents of *publicly traded* firms with CRSP returns can be valued — private firms, startups pre-IPO, universities, and foreign assignees are excluded, and these are not a random slice of innovation. Third, the firm has to *survive* and stay listed around the grant date. So the panel describes the innovation of large, public, surviving U.S. firms, and generalizing its growth/reallocation conclusions to the whole economy requires an argument the data alone cannot supply. This bounds external validity in a way every downstream user inherits.

**Efficient markets is baked in (and cuts both ways).** The measure *assumes* the market prices the patent correctly and promptly at grant. If markets are slow or noisy, the window misses value that leaks in later, and the measure is attenuated; if markets over-react, it is inflated. You cannot use the measure to *test* market efficiency, because efficiency is the assumption that built it — a circularity worth stating plainly. And remember Week 4: the abnormal return is itself estimated relative to a market model whose parameters are estimated with noise, so a careful reader asks how sensitive the measure is to the choice of normal-return model and window length.

**The growth results are associations, not experiments (Weeks 3–4).** Even granting a perfect measure, the reallocation and growth findings are *predictive* — innovating firms grow and rivals shrink *on average* — not identified causal effects. There is no random assignment of patents, no instrument for innovation, no discontinuity. The creative-destruction reading is *consistent with* the correlations but not pinned down by them; reverse causality (growing firms innovate more) and common drivers (a demand shock lifts both innovation and growth) are live alternatives. KPSS are measured about this, and you should be too: accept the measure, accept the correlations, and reserve judgment on the precise causal story.

---

## 7. Three replication exercises

You do not understand a constructed measure until you have tried to build a piece of it yourself. These three escalate, and all live in **`nb6.1`** (`notebooks/week-06/nb6.1-patent-value-panel.ipynb`). As always, real CRSP daily returns stay read-only on GMU infrastructure (Conventions §5); the notebook ships a seeded synthetic fallback with the same schema — simulated patent grants, grant dates, and daily returns with a known "true" patent value baked in — so every step runs on your laptop, with a Path-A pull for the public KPSS dataset and Hopper CRSP.

**Exercise 1 — Inspect and aggregate the public patent-value panel.** Download (or load the synthetic stand-in for) the patent-level KPSS values, and *look at them before you trust them*. Plot the distribution of per-patent dollar values — you should find it wildly right-skewed, a few blockbuster patents dwarfing thousands of small ones, which is the whole motivation for not counting patents equally. Then **aggregate to a firm-year panel**: sum patent values within firm and year to build the central data object. Print the top-ten firm-years by total innovation value and ask whether the names make sense (do the famous innovators show up?). The deliverable is the firm-year value panel plus a one-paragraph sanity check on its skew and its top entries — and a note on which patents *lack* a value, and why (the selection of §6).

**Exercise 2 — Rebuild a single patent's value from a grant-window event study.** Reuse your Week-4 event-study machine. For one patent (real or synthetic), pull the firm's *daily* returns around the grant date, fit a market model on a pre-event estimation window, compute the **abnormal return** over the short grant window, multiply by market cap to convert to dollars, and compare your hand-built number to the published KPSS value. Then **stress the construction on purpose**: vary the window length (one day, three days, five days) and the normal-return model, and watch the estimate move. The lesson — that the measure depends on modeling choices §6 flagged — becomes a number on your own screen, not a caveat you read past.

**Exercise 3 — Validate the measure, then break a validation.** Reproduce the *spirit* of the paper's headline validation: in the firm-year panel, regress a future outcome (next year's profitability or growth, in the synthetic data the known "true" value) on this year's KPSS innovation value, and confirm the positive, significant association that earns the measure its credibility. Then **inject a confound**: contaminate a subset of grant windows with simulated earnings-announcement returns, rebuild the value measure on the contaminated windows, and watch the validation degrade. You will see, directly, how confounding news in the window (§6) eats into the measure's predictive power — and why the short window and aggregation are the defenses.

---

### Read like a referee

Before you leave KPSS, sit with three questions — the kind a referee writes in the margin:

1. **Expected vs. realized value.** The measure is the market's *forecast* of a patent's value at grant, not what the patent ultimately earned. Design — in words — a check using *later* outcomes (realized profits, eventual citations, litigation) that would tell you whether the market's grant-window forecasts are, on average, unbiased or systematically too high for some kinds of patents. Why can the measure never, by itself, distinguish "the market was right" from "the market was wrong but consistent"?

2. **Confounds in the window.** A skeptic says the grant-window return is really just earnings and analyst news that happens to land near grant dates. Name the *one* piece of evidence in the paper that most reassures you on this, and the *one* test you would run that the paper did not — and say which direction the bias would go if grant dates and good-news days were positively correlated.

3. **Whose innovation does this panel describe?** Given the three selection screens of §6 (granted patents · public firms · survivors), write one sentence stating the population the firm-year value panel actually represents, and one sentence on a growth/reallocation conclusion you would *not* be willing to extend to the whole economy on this evidence — and why.

Next stop: **`nb6.1`**, where you stop reading about the patent-value panel and build it — first inspecting the public KPSS dataset, then reconstructing a single patent's value from a grant-window event study of your own.
