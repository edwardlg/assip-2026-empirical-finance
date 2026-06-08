# Ch 5.2 — Reader's Guide: Fama & French (1993), "Common Risk Factors in the Returns on Stocks and Bonds"

> **Paper.** Fama, E. F., & French, K. R. (1993). Common Risk Factors in the Returns on Stocks and Bonds. *Journal of Financial Economics*, 33(1), 3–56.

Yesterday's guide (Ch 5.1) walked you through Fama and French's 1992 paper, the one that put a knife into CAPM beta and announced that two humble firm characteristics — **size** and **book-to-market** — did the explaining instead. But FF92 left a job unfinished, and it is the kind of unfinished job that should bother you. They showed that *if you sort stocks by size and by book-to-market, the average returns line up with those characteristics*. They ran the cross-section: at each date, regress this month's returns across firms on each firm's size and book-to-market, à la Fama–MacBeth (Lab 2). That tells you the characteristics are *priced* — high book-to-market stocks earn more on average. It does **not** tell you *why*, and it does not give you a *model* you can hand to someone and say "here is the machine that generates expected returns."

That is the gap the 1993 paper fills, and filling it is why this paper, not the 1992 one, became the single most-used regression specification in empirical finance. FF93 takes the two characteristics and manufactures them into **factors** — tradeable portfolios whose returns you put on the right-hand side of an ordinary time-series regression. Where FF92 asked "do these characteristics predict the cross-section of average returns?", FF93 asks the structurally different question: **can a small set of factor returns explain the common month-to-month movement in stock returns, and price them with no leftover?** Same two characters, completely different machinery. Today's job is to see that difference clearly, because students conflate these two papers constantly, and the conflation hides the cleverest move in the literature.

We read it the professional way: tables first, in an order that reveals the argument, not front-to-back. Keep Week 2 loaded — this paper is *nothing but* time-series OLS (Ch 2.1) read for its $R^2$ and its intercepts — and keep Week 1's lesson on multiple testing (Ch 1.5) in your back pocket, because by the "what's vulnerable" section you will need it.

---

## 1. Research question — from the cross-section to a factor model

Here is the cleanest way to hold the two papers apart. Both are about the same empirical fact: small stocks and high book-to-market ("value") stocks have earned higher average returns than CAPM says they should. The difference is the *shape* of the question.

**FF92 is a cross-sectional question.** Freeze a single month. You have a few thousand firms. Each firm has an average-return-this-month and a size and a book-to-market. The cross-sectional regression asks: across firms, on this date, does the return slope on the characteristic? Do it every month and average the slopes. The output is a **risk premium per characteristic** — a number like "a one-unit increase in book-to-market is worth $X$ extra return per month." The unit of variation is *firms within a date*.

**FF93 is a time-series question.** Now freeze a single *portfolio* — say, "small-cap value stocks" — and watch it move through time, month after month. The time-series regression asks: when the small-value portfolio's excess return goes up this month, *what moved with it*? Was it the market? Was it a "small stocks did well this month" factor? A "value stocks did well this month" factor? The unit of variation is *time within a portfolio*. You are decomposing each portfolio's return stream into common pieces plus an idiosyncratic remainder.

Why does going time-series matter so much? Because a time-series regression hands you two things the cross-section cannot. First, the **$R^2$**: the fraction of a portfolio's month-to-month variance that the factors explain. A high $R^2$ means the factors capture the *common variation* — the part of returns that many stocks share, the part that cannot be diversified away. Second, the **intercept** $\alpha$. If your factors are the *complete* description of priced risk, then a portfolio's average excess return should be entirely accounted for by its exposures to those factors, and the intercept — the average return left over *after* the factors have done their work — should be **zero**. A nonzero $\alpha$ is a **pricing error**: money the model cannot explain. The cross-sectional regression of FF92 never produces an $\alpha$ in this sense. The time-series regression does, and that single number is the whole ballgame.

So the FF93 research question, stated as plainly as we can: **Is there a small set of factors — the market, a size factor, and a value factor — such that the time-series regression of any test portfolio's excess return on those three factors has (a) a high $R^2$, meaning the factors capture the common variation, and (b) an intercept indistinguishable from zero, meaning no priced risk is left on the table?** If yes, you have replaced a vague claim ("size and value matter") with an operational model: a three-line regression anyone can run.

---

## 2. Identification strategy — the time-series regression machinery

Everything technical in this paper is built from one idea you already own: ordinary least squares run on a time series. The cleverness is entirely in *what goes on the right-hand side*. Let us build it in the order Fama and French build it.

**Step 1 — Manufacture the factors as portfolios.** A factor here is not an abstract statistical thing; it is a **factor-mimicking portfolio**, a real long-short basket of stocks whose return *is* the factor. There are three.

- **The market factor**, $R_M - R_f$: the return on a broad value-weighted market portfolio minus the risk-free rate. This is the old CAPM factor, unchanged.
- **SMB ("small minus big")**, meant to capture the size effect.
- **HML ("high minus low")**, meant to capture the value effect — "high" and "low" referring to book-to-market equity (BE/ME).

SMB and HML are built from a **2×3 sort**, and the construction matters because half the "what's vulnerable" critique later is about exactly these choices. At the end of June each year, split all stocks into **two size groups** (small / big, by the NYSE median market-cap breakpoint) and independently into **three book-to-market groups** (bottom 30% / middle 40% / top 30%, again on NYSE breakpoints). Intersecting gives **six value-weighted portfolios**: small-low, small-medium, small-high, big-low, big-medium, big-high. Then:

$$
\text{SMB} = \underbrace{\tfrac{1}{3}\big(\text{S-Low} + \text{S-Med} + \text{S-High}\big)}_{\text{average of the three small portfolios}} - \underbrace{\tfrac{1}{3}\big(\text{B-Low} + \text{B-Med} + \text{B-High}\big)}_{\text{average of the three big portfolios}}
$$

$$
\text{HML} = \underbrace{\tfrac{1}{2}\big(\text{S-High} + \text{B-High}\big)}_{\text{average of the two high-BE/ME portfolios}} - \underbrace{\tfrac{1}{2}\big(\text{S-Low} + \text{B-Low}\big)}_{\text{average of the two low-BE/ME portfolios}}
$$

Read those two formulas slowly, because the design is deliberate. SMB averages *across* the three value buckets before differencing small minus big, so it is meant to be a clean size bet roughly *neutral* to value. HML averages *across* the two size buckets before differencing value minus growth, so it is meant to be a clean value bet roughly *neutral* to size. The averaging is how you keep the two factors from contaminating each other. (This is the same instinct as Frisch–Waugh–Lovell from Ch 2.3: to isolate one effect, partial the other one out.)

**Step 2 — Pick the test portfolios.** You need things to *price*. FF93's test assets are the famous **25 portfolios** formed on a 5×5 sort of size and book-to-market: five size quintiles crossed with five BE/ME quintiles. These 25 are *not* the same as the six portfolios used to build SMB and HML — keep that distinction sharp. The six are the *ingredients of the factors*; the 25 are the *patients the model has to cure*.

**Step 3 — Run the time-series regression, one per test portfolio.** For each of the 25 portfolios $i$, regress its monthly excess return on the three factors over the whole sample:

$$
R_{it} - R_{ft} = \alpha_i + b_i\,(R_{Mt} - R_{ft}) + s_i\,\text{SMB}_t + h_i\,\text{HML}_t + \varepsilon_{it}.
$$

This is just multiple OLS (Ch 2.1) with $T$ monthly observations. The estimated slopes $\hat b_i, \hat s_i, \hat h_i$ are the portfolio's **factor loadings** — how strongly it co-moves with market, size, and value. The intercept $\hat\alpha_i$ is the **pricing error**. The $R^2$ is how much of that portfolio's variance the three factors soak up.

**Step 4 — Read the regression two ways.**

*Common variation* is the $R^2$ question. If the three factors are the right common factors, every one of the 25 regressions should have a high $R^2$ — the factors should explain most of each portfolio's month-to-month wiggle. This is the "common risk factors" of the title: the shared movement.

*Pricing* is the $\alpha$ question, and it is more demanding. Even with high $R^2$, the *average* return might not be fully explained — the intercepts could be systematically nonzero. So the real test is **joint**: are all 25 intercepts simultaneously zero? You cannot just eyeball 25 $t$-statistics, because with 25 tests some will look "significant" by chance (Week 1's multiple-testing problem, head on). The right instrument is the **GRS test** — Gibbons, Ross & Shanken (1989) — a single $F$-statistic for the joint null $H_0: \alpha_1 = \alpha_2 = \cdots = \alpha_{25} = 0$.[^grs] We name it and use it; we do not derive it. The intuition is exactly the joint-hypothesis logic from Week 2: instead of 25 separate questions, ask one question about all the intercepts at once, accounting for the fact that the portfolios' residuals are correlated. A model passes the asset-pricing bar when GRS *fails to reject* — i.e., when the pricing errors are jointly indistinguishable from zero.

[^grs]: Gibbons, M. R., Ross, S. A., & Shanken, J. (1989). A Test of the Efficiency of a Given Portfolio. *Econometrica*, 57(5), 1121–1152.

The whole identification strategy is now visible: **build factors as portfolios, regress test portfolios on them in time series, read $R^2$ for common variation and the intercepts (jointly, via GRS) for pricing.** The clean separation between those last two questions — explaining *co-movement* versus explaining *average level* — is the engine of the paper.

---

## 3. Data

The data are the standard pair you have been using all camp. Stock returns and market caps come from **CRSP** (the Center for Research in Security Prices), covering NYSE, AMEX, and NASDAQ common stocks. Book equity comes from the **Compustat** annual files, merged to CRSP by firm. The bond side of the paper (we will keep it brief) adds U.S. government and corporate bond returns.

The stock sample period is **July 1963 through December 1991** — roughly 342 monthly observations.[^period] The start date is not arbitrary: book-equity coverage in Compustat is thin before the early 1960s, so beginning in mid-1963 avoids the worst survivorship and backfill problems. The annual June re-sort with a lag (accounting data from fiscal year-end in calendar year $y{-}1$ matched to returns from July of year $y$ through June of $y{+}1$) is the standard device for making sure that **the book-equity number was actually public before the returns it is used to predict** — a look-ahead guard we will revisit in §6.

[^period]: The stock sample runs July 1963–December 1991 (Fama & French 1993, *Journal of Financial Economics*, 33(1), 3–56), i.e. 342 monthly observations.

For the bonds, briefly: FF93's larger ambition is one model for *both* stocks and bonds, so it adds two bond-market factors — a **term** factor (long-term government minus the short rate, capturing yield-curve slope) and a **default** factor (long-term corporate minus long-term government, capturing credit risk). The headline is that the bond factors do most of the work for bonds while the stock factors do most of the work for stocks; the two markets are largely segmented here. For our purposes — and for nb5.2 — we focus on the three **stock** factors and the **25** stock portfolios, which is where the paper's lasting influence lives.

---

## 4. Table-by-table reading order

A professional does not read this paper top to bottom. Read it in the order the *argument* runs, which is roughly factor-definitions → common-variation → pricing.

**First, the factor-definition / summary table.** Find the table that defines SMB, HML, and the market factor and reports their average returns, standard deviations, and correlations. You are checking three things. (i) Do SMB and HML have *positive* average returns over the sample — i.e., did small and value actually pay? (ii) Are SMB and HML only weakly correlated with each other and with the market? They should be roughly orthogonal *by construction* (that was the point of the 2×3 averaging), and low correlation among regressors is what keeps the loadings in §2's regression interpretable and the standard errors small. (iii) Glance at the magnitudes so you have a feel for what "a unit of HML" means before you read loadings.

**Second, the table of average excess returns on the 25 portfolios.** This is the *pattern to be explained* — the explanandum. Read it as a 5×5 grid. Across BE/ME (left to right, growth to value), average returns should rise: the value effect. Down size (small to big), they should fall: the size effect. The most extreme cell — small-value — is the highest-returning corner, and small-growth is the notorious problem child. Burn this grid into your memory, because every later table is asking "did the model reproduce *this*?"

**Third — the heart of the paper — the time-series regression tables.** These report, for each of the 25 portfolios, the loadings $\hat b_i, \hat s_i, \hat h_i$, the intercept $\hat\alpha_i$ with its $t$-statistic, and the regression $R^2$. Read them in three passes:

1. **$R^2$ pass.** Scan only the $R^2$ column. They should be high across the board — the three factors should explain the large majority of each portfolio's variance. *This is the "common variation" result.* Compare mentally to a market-only (CAPM) regression: adding SMB and HML lifts the $R^2$s substantially, which is the direct evidence that size and value are genuinely *common* sources of co-movement, not just cross-sectional curiosities.

2. **Loadings pass.** Now read $\hat s_i$ (the SMB loading) down the size dimension: small portfolios should load strongly *positive* on SMB, big portfolios near zero or negative. Read $\hat h_i$ (the HML loading) across the BE/ME dimension: value portfolios load strongly positive on HML, growth portfolios negative. The loadings should march monotonically with the sort — that orderliness is the model "recognizing" the very characteristics the portfolios were sorted on. This is what people mean when they say the loadings "make sense."

3. **Intercept pass.** Finally read the $\hat\alpha_i$ column and its $t$-statistics. The claim is that they are **economically small and mostly statistically indistinguishable from zero** — the pricing errors are tiny relative to the average returns from the second table. Then find the **GRS $F$-statistic** for the joint null that all 25 intercepts are zero. The story the paper tells is that the three-factor model gets the intercepts down close enough that it dramatically outperforms CAPM, even if the joint test is not always a clean pass in every corner. Note the one cell that tends to misbehave: **small-growth**, whose intercept is the most stubborn. Honest readers flag it; the model is very good, not perfect.

> **How to *see* "the factors explain most common variation."** Two columns, side by side, tell the whole story. The $R^2$ column near 1 says: *whatever moves these portfolios month to month is mostly these three factors.* The $\alpha$ column near 0 says: *and once you account for the exposures, there is no extra average return to explain.* High $R^2$ + zero $\alpha$ = a working factor model. Memorize that two-column reading; it is the literacy this entire week is teaching.

We are deliberately **not** quoting specific coefficient values. The qualitative findings — positive SMB/HML premia, high $R^2$s on the 25 portfolios, small intercepts, small-growth as the weak spot — are well established and safe to state. Any precise number you want belongs in your own replication, not in a guide written from memory. (Tag any specific figure you carry forward as `[CHECK]`.)

---

## 5. What's clever

Three moves, each of which you can lift into your own work.

**The factor-mimicking portfolio.** This is the master stroke. A "risk factor" sounds like an abstraction you can never observe. FF93's answer: *make it a portfolio.* A long-short basket of real stocks has a return you can compute every month, put on the right-hand side of a regression, and — crucially — that an investor could actually *hold*. That last point is not cosmetic. Because the factor is itself a traded excess return, asset-pricing theory says *the factor must price itself*: a regression of SMB on the three factors should have a zero intercept too. Turning an abstraction into a portfolio is what makes the whole thing testable with nothing fancier than OLS.

**Separating common variation from cross-sectional pricing.** FF92 only had the cross-sectional pricing question. FF93 cleaves the problem into two: *do the factors capture co-movement* ($R^2$) and *do they capture average returns* ($\alpha$). These are genuinely different — you can have one without the other. A factor could co-move with everything (high $R^2$) yet carry no premium (so it does not help price), or carry a premium but explain little co-movement. By insisting on *both*, the time-series test is far more demanding than the cross-section alone, and far more informative about what kind of object size and value are.

**It became the workhorse benchmark.** This is clever in a sociological sense that matters for how you read everything afterward. By packaging size and value as downloadable monthly factor returns (Ken French has hosted them publicly for decades), FF93 gave every subsequent researcher a *common yardstick*. When someone in Week 6 claims a new "anomaly" — a strategy that earns abnormal returns — the first question a referee asks is: "what is its **three-factor alpha**?" That is, regress the strategy's returns on market/SMB/HML and see if the intercept survives. The paper did not just answer a question; it built the ruler everyone now measures with. That is why it is your Week 5 anchor and not FF92.

---

## 6. What's vulnerable

A guide that only praises is useless. Here is where a sharp referee pushes, and where Weeks 1 and 2 give you the vocabulary to push back.

**Are SMB and HML *risk* or *mispricing*?** This is the deepest critique and it is unsettled to this day. FF93 frames size and value as compensation for *risk* — value stocks are riskier in some state-of-the-world sense (distress, say), so they must pay more. But the rival camp says the premia reflect *mispricing*: investors over-extrapolate the glamour of growth firms and under-price beaten-down value firms, and the "premium" is just the correction. The regression machinery **cannot distinguish these.** A high $R^2$ and a zero intercept are equally consistent with "HML is a risk factor" and "HML captures a systematic behavioral mistake." The model is an excellent *description* of co-movement; it is silent on the *economics* of why the premium exists. Hold that humility.

**The factor zoo and data-snooping (Week 1, multiple testing).** Here is the uncomfortable mirror. FF93 found that *two* sorts (size, book-to-market) survive. But the same recipe — sort on a characteristic, build a long-short portfolio, check the alpha — has since been run on *hundreds* of characteristics, yielding the so-called **factor zoo**. When you test hundreds of candidate factors and report the ones with significant alphas, you are running exactly the multiple-comparisons gauntlet from Ch 1.5: with enough tries, some "factors" clear the bar by pure chance. This raises a retrospective worry about FF93 itself — were size and value *found by searching*, and would they survive a multiple-testing correction applied to the whole search that produced them? The honest reading: SMB and HML have held up far better out-of-sample and across countries than most zoo entries, which is real evidence they are not pure flukes — but the critique is exactly right that the *method* is a data-snooping machine if you are not disciplined about it.

**Look-ahead in factor construction.** The June re-sort with the lagged accounting match (§3) is precisely a guard against using book equity before it was public. But the guard depends on getting the timing exactly right, and Compustat's **backfilling** — historically adding data for firms only after they were established and successful — can sneak survivorship and look-ahead bias into the early sample. If your replication is sloppy about the lag, you will manufacture a value premium that *no real-time investor could have earned*. This is a concrete, checkable failure mode, and nb5.2 will make you confront it.

**Sensitivity to portfolio-formation choices.** The 2×3 sort, the NYSE breakpoints, the value-weighting, the bottom-30/top-30 cutoffs, the June rebalance — every one of these is a researcher *choice*, and the factor returns shift if you change them. Value-weighting versus equal-weighting changes how much small stocks drive the result; using all-stock breakpoints instead of NYSE-only loads the small portfolios with thousands of micro-caps. None of these break the paper, but they mean "the" size and value premia are really "the premia *under these specific construction rules*." A robust finding should not hinge on a cutoff at 30% versus 33%; checking that it does not is part of an honest replication.

---

## 7. Three replication exercises

These are scoped for nb5.2; each builds on the FF92 sorting machinery you set up in nb5.1.

1. **Build the factors from scratch and check them against Ken French's data.** Using your CRSP/Compustat merge from nb5.1, form the six 2×3 size×BE/ME portfolios at each June, construct monthly SMB and HML by the formulas in §2, and the value-weighted market excess return. Then download the official Fama–French factors and *correlate your series with theirs month by month*. You will not match perfectly (data vintages differ); aim for correlations comfortably above 0.9 and diagnose any month where you diverge badly. This single exercise teaches more about real-world data plumbing than any lecture.

2. **Run the 25 time-series regressions and make the two-column table.** Form the 5×5 size×BE/ME test portfolios, regress each one's excess return on your three factors (plain OLS, Ch 2.1), and assemble the table from §4: loadings $\hat b,\hat s,\hat h$, the intercept $\hat\alpha$ with its $t$, and $R^2$. Verify the three qualitative facts: high $R^2$s everywhere, loadings that march monotonically with the sorts, and small intercepts — with **small-growth** as the visible exception. Then run a **CAPM-only** regression on the same 25 and show, column by column, how much the $R^2$s rise and the intercepts shrink when SMB and HML are added.

3. **Run the GRS joint test and stress-test the construction.** Compute the GRS $F$-statistic for the joint null that all 25 intercepts are zero, for both the CAPM and the three-factor model, and compare. Then change *one* construction choice — swap NYSE breakpoints for all-stock breakpoints, or value-weighting for equal-weighting — re-form the factors, and re-run. Report how much SMB, HML, the loadings, and the GRS statistic move. This is the §6 "sensitivity" critique turned into a measured number, and it is the kind of robustness check a referee will demand of your own capstone.

---

## Pointers and referee questions

The hands-on companion is **nb5.2 (FF93 factor regressions)**: it walks you from your nb5.1 portfolio sorts through factor construction, the 25 time-series regressions, the two-column $R^2$/$\alpha$ reading, and the GRS test — the exact pipeline behind exercises 1–3 above, with a "Your Turn" extension that re-runs the model with a momentum factor bolted on.

Three questions to interrogate this paper the way a referee would:

1. **Risk or mispricing?** The paper shows HML *prices* the cross-section, but offers no test that pins down *why* value pays. What additional evidence — a recession-state pattern in HML, a link to firm fundamentals, an out-of-sample or out-of-country replication — would move you toward the risk story over the behavioral one, and does FF93 provide any of it?

2. **Survivorship of the factors themselves.** Given the factor-zoo critique, if you applied a multiple-testing correction to the *full set of characteristic-sorts* that the profession searched before settling on size and value, would SMB and HML still clear the bar? What would convince you they are not just the two survivors of a giant fishing expedition?

3. **The small-growth corner.** The three-factor model's most stubborn pricing error sits in small-growth. Is that one rebellious cell a tolerable blemish on an otherwise excellent model, or a symptom that a *fourth* factor (profitability? investment? momentum?) is missing — and how would you decide between those two readings using only the tables in this paper?
