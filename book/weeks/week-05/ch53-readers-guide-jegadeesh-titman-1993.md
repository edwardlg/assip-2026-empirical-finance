# Ch 5.3 — Reader's Guide: Jegadeesh & Titman (1993)

> **Paper.** Jegadeesh, N., & Titman, S. (1993). Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency. *Journal of Finance*, 48(1), 65–91.[^jt93]

[^jt93]: Jegadeesh, N., & Titman, S. (1993). Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency. *Journal of Finance*, 48(1), 65–91.

Yesterday's two Reader's Guides put a price on *risk*. Fama–French (1992) said the cross-section of average returns lines up with size and book-to-market, not with CAPM beta; Fama–French (1993) turned those patterns into tradable factor portfolios. Both papers are, at heart, *efficient-markets* papers: returns differ across stocks because the stocks carry different bundles of priced risk. Today's paper is the one that broke that story open. Jegadeesh and Titman take a strategy a 16-year-old day-trader would invent on a napkin — *buy the stocks that went up, short the ones that went down* — and show it makes money, robustly, for decades, in a way the risk factors of the day could not explain. Sam, our markets-and-momentum student, has been waiting all week for this one.

This is the paper that named **momentum**. It matters not because the strategy is exotic — it is almost insultingly simple — but because of *what its success implies*. If a rule this dumb beats the market after you adjust for known risk, then either there is a risk factor nobody had written down, or prices are not impounding information the way the efficient-markets hypothesis says they do. Thirty years later we still argue about which. That unresolved argument is exactly why this paper is on the syllabus: it is a clean, replicable anomaly that forces you to take a side and defend it with evidence.

We read it the professional way — tables first, in a deliberate order, hunting for where the result could break before we let ourselves believe it. The fixed Reader's-Guide anatomy from the Week 5 reading pack drives the sections below.

---

## 1. Research question

The plain-English question: **do past winners keep winning?** Take a stock's return over the past few months — say the past six. Sort all stocks by that past return. Do the ones near the top (the *winners*) go on to earn higher returns over the *next* few months than the ones near the bottom (the *losers*)? If yes, then past returns predict future returns at intermediate horizons, and a strategy of buying winners and shorting losers should be profitable.

The horizon is the whole game. Jegadeesh and Titman are precise about it: they study **3-to-12-month** formation and holding periods. This is deliberately wedged between two horizons where the *opposite* pattern was already known. At very short horizons (a week, a month) returns tend to *reverse* — last week's losers bounce back — a pattern attributable partly to bid-ask bounce and short-run overreaction. At long horizons (3–5 years) De Bondt and Thaler had documented *long-run reversal*: past long-term losers outperform past long-term winners.[^dbt] Momentum lives in the medium-horizon gap between these two reversals: continuation for a few months to a year, then eventual reversal. Pinning the result to that specific window is part of why the paper is credible — it is not "stocks trend forever," it is "stocks trend for 3–12 months and then unwind."

[^dbt]: De Bondt, W. F. M., & Thaler, R. (1985). Does the Stock Market Overreact? *Journal of Finance*, 40(3), 793–805.

The *implication* is the title's second half: **implications for stock market efficiency.** Recall the weak-form efficient-markets hypothesis (EMH) from Week 1's framing of "what is a finding": prices already reflect all information in *past prices*, so past returns should carry no usable signal about future returns. A profitable rule built only from past returns is a direct strike at weak-form efficiency. So the paper has a methodological burden it cannot dodge: it must show the profits are *not* just compensation for risk. If buying winners is really just loading up on some risk factor, then there is no anomaly — you are being paid for bearing danger, exactly as efficiency predicts. The authors therefore spend much of the paper trying to *kill their own result* with risk adjustment, and reporting that it survives.

---

## 2. Identification strategy

There is no instrument and no natural experiment here. The "identification" is the *portfolio construction*, and reading the paper means understanding that construction cold.

**The J/K sort.** Fix two numbers: a **formation** (or *ranking*) period of $J$ months and a **holding** period of $K$ months. At the end of each month $t$:

1. Compute each stock's cumulative return over the past $J$ months (months $t-J+1$ through $t$).
2. Sort all stocks on that past return and split into ten deciles. The top decile is the **winner** portfolio $W$; the bottom decile is the **loser** portfolio $L$.
3. Hold an equal-weighted position in each decile for the next $K$ months, then re-sort.

The headline trade is the **zero-cost winner-minus-loser portfolio**: go long the winners and short the losers in equal dollar amounts. Long and short legs cancel in cost, so the net investment is (notionally) zero and the return is a pure spread, $r^{W} - r^{L}$. A positive average spread is the momentum profit. The paper reports a grid of these spreads over a $J \times K$ menu — formation periods of 3, 6, 9, 12 months crossed with holding periods of 3, 6, 9, 12 months — sixteen strategies in one table. The classic, the one everyone quotes, is **6/6**: rank on six months, hold six months.

**The overlapping-holding-period trick — and why it complicates inference.** Here is the move that makes the methodology efficient and also makes the statistics subtle. If you held a 6-month portfolio and only re-balanced every six months, you would get one fresh, non-overlapping return observation every half-year — throwing away five-sixths of your months. Instead, Jegadeesh and Titman form a *new* winner-minus-loser portfolio **every month** and hold each for $K$ months. So in any given month you hold $K$ overlapping cohorts at once — the one formed this month, last month, … back $K-1$ months — and your reported monthly return is the *equal-weighted average across those overlapping cohorts*. This is sometimes called the *overlapping-portfolio* or *calendar-time* construction. It uses every month of data and smooths the estimate.

The price you pay is **serial correlation in the return series you then test.** Because consecutive monthly returns share $K-1$ of their $K$ component cohorts, adjacent observations are mechanically correlated even if the true underlying signal were i.i.d. This is *exactly* the overlapping-observations problem we built in Week 2. When you regress an overlapping series on a constant to test whether its mean differs from zero, the usual OLS / i.i.d. standard error is **too small**: it assumes independent observations you do not have, so it overstates your effective sample size and inflates the $t$-statistic. The fix is the one from **Ch 2.4**: a **heteroskedasticity-and-autocorrelation-consistent (HAC)** standard error — **Newey–West** — with the lag truncation set to at least $K-1$ to absorb the induced autocorrelation. When you read this paper's $t$-statistics, the first question a referee asks is: *did they correct the standard errors for the overlap, or are these naive $t$-stats on overlapping data?* (The paper's own returns are computed as averages across cohorts, which dampens but does not eliminate the issue; modern replications report Newey–West $t$-stats as a matter of course.)

A second design choice worth flagging: many momentum implementations **skip the most recent week or month** between formation and holding — rank on months $t-6$ through $t-1$, say, and start holding at $t+1$ — to dodge the short-horizon *reversal* and bid-ask bounce that would otherwise contaminate the winner/loser definitions. [CHECK] the exact skip convention used in JT93's main tables versus later momentum papers; the one-month skip is more strongly associated with later work, so attribute carefully.

---

## 3. Data

The dataset is **CRSP** monthly returns — the Center for Research in Security Prices file, the same return tape Fama–French use, restricted in the paper to **NYSE and AMEX** common stocks. (Nasdaq's broad coverage on CRSP arrives later, which is one reason early momentum work leans on NYSE/AMEX.)

The **sample period is 1965–1989** — twenty-five years of monthly data. That gives roughly 300 monthly formation dates, each spawning a decile sort over hundreds to a couple thousand eligible stocks.

The **J/K grid** is the data object you will spend the most time on: $J \in \{3,6,9,12\}$ formation months crossed with $K \in \{3,6,9,12\}$ holding months. Equal-weighted decile portfolios (each stock counts the same, not value-weighted), with the overlapping monthly re-formation described above. For our notebook we will swap in modern CRSP and extend the sample forward — and you should expect the magnitudes to shift, because the post-1990 period (especially the 2009 "momentum crash") is unkind to the strategy.

---

## 4. Table-by-table reading order

A professional does not read this paper top to bottom. Here is the order that gets you to the truth fastest.

**First: the $J \times K$ returns matrix.** This is the heart of the paper — a single table of average monthly winner-minus-loser spreads across the sixteen formation/holding combinations, with $t$-statistics. Read it as a *surface*. Three things to check before anything else:

- *Sign and significance of the diagonal.* Are the spreads positive and significant across the grid, especially at 6/6, 9/9, 12/3? The qualitative finding is that medium-horizon momentum profits are **positive and on the order of roughly 1% per month** for the classic 6/6 strategy — a big number, annualized. Describe it as *order-of-magnitude ~1%/month*; do **not** quote a specific decimal from memory. [CHECK] the exact 6/6 figure against the table.
- *Where it strengthens and weakens.* Longer formation periods paired with longer holding periods start to show the profit decaying — the seed of the long-run reversal story.
- *Are these $t$-stats overlap-corrected?* Hold this question; it governs how much of the significance you believe (see §2).

**Second: the risk-adjustment table.** Having shown raw spreads are positive, the authors ask whether *risk* explains them. They adjust returns for market exposure (CAPM beta) and report that winners are **not** meaningfully riskier than losers — if anything the beta and size differences run the *wrong way* to rescue efficiency. The momentum alpha survives the risk controls available in 1993. Read this table asking: *what risk model is being used, and what is left unexplained?* (The honest answer, from later work, is that the standard factor models of the era cannot price momentum — which is why a dedicated momentum factor, UMD/WML, eventually gets bolted onto the Fama–French machinery you saw in Ch 5.2.[^carhart])

[^carhart]: Carhart, M. M. (1997). On Persistence in Mutual Fund Performance. *Journal of Finance*, 52(1), 57–82.

**Third: the sub-period and seasonality robustness.** Two checks here. (a) *Sub-periods*: split the sample in half and confirm the profit is not driven by one lucky decade. (b) *Seasonality* — the crucial one: break the profits out **by calendar month**, because the size/value anomalies of the era were famously concentrated in **January**. Momentum has the *opposite* January problem: the strategy tends to **lose money in January** (losers — often beaten-down small caps — bounce hard in January) while earning its keep in the other eleven months. Reading this table tells you the profit is not a January artifact; it is an *anti*-January effect, which is harder to dismiss.

**Last (optional): the longer-horizon / post-holding behavior.** Evidence that the medium-horizon profits eventually *reverse* if you hold long enough — reconciling momentum with De Bondt–Thaler long-run reversal and hinting at the *overreaction* interpretation.

---

## 5. What's clever

**The strategy design is brutally simple and that is the point.** There is no parameter to tune beyond $J$ and $K$, no firm characteristic to construct, no accounting data to clean. You need *only past returns* — the one input the weak-form EMH swears is useless. A simple rule that works is far more damaging to a theory than a complicated one, because there is nowhere to hide a degree of freedom. Sam should sit with this: the *elegance* is the evidence.

**The overlapping-portfolio trick squeezes the data.** Re-forming every month and averaging across $K$ overlapping cohorts turns a data-poor design (one independent 6-month return every six months) into a data-rich monthly series, and the cohort-averaging itself smooths idiosyncratic noise. It is a genuinely good idea — *provided* you then respect the serial dependence it creates when you do inference. The cleverness and the vulnerability are the same coin.

**Framing momentum as an efficiency anomaly, not just a trading tip.** The authors could have stopped at "here is a strategy that makes money." Instead they pre-empt the obvious rebuttal — *you are just being paid for risk* — by running the risk adjustment themselves and showing the profit is not beta in disguise. By doing the skeptic's work first, they shift the burden: now the *defender* of efficiency has to name the missing risk factor. That rhetorical move, doing your critic's job before they can, is the mark of a paper built to survive.

---

## 6. What's vulnerable

This is where a referee earns their keep. Five live threats:

**Transaction costs — does the profit survive trading?** This is the first and biggest. Momentum is a *high-turnover* strategy: every month you re-rank and trade a fresh slice of the portfolio, and the losers you short are disproportionately small, illiquid, low-priced stocks with wide bid-ask spreads — the *most* expensive names to trade. A gross spread of ~1%/month can be eaten alive by round-trip costs, the short-sale costs of borrowing hard-to-borrow losers, and price impact. The paper engages this, but the honest verdict from later work is contested: net profitability shrinks substantially and, by some accounts of the short leg in small caps, can vanish. **Any claim of momentum profits must be quoted net of a credible cost model** — which is precisely the exercise PS 5.3 forces.

**Data-snooping (Week 1's multiple testing).** Sixteen $J \times K$ cells is sixteen strategies. If you stare at a $4 \times 4$ grid and crown the most significant cell, you have run sixteen tests and reported the winner — a textbook multiple-comparisons problem (Ch 1.5; revisited under FDR in Ch 8.2 and the pre-analysis-plan discussion in Ch 7.3). A single $t = 2.5$ means much less when it is the maximum over sixteen correlated tries. The mitigating facts here are real and worth crediting: the result is *not* one isolated cell but a broad region of the grid, it was *predicted ex ante* by the overreaction literature, and it has since replicated **out of sample** — other countries, asset classes, and the decades *after* 1989. Out-of-sample survival is the strongest answer to a snooping charge, and momentum has it. Still, the reader should mentally Bonferroni-discount any single starred cell.

**The January / seasonality effect.** Even though momentum is an *anti*-January phenomenon, the seasonality cuts both ways as a vulnerability: a strategy whose entire annual profit depends on eleven months *minus* a January loss is exposed to anything that shifts that seasonal pattern (tax-loss selling rule changes, the rise of index investing). The seasonal structure is a clue to *mechanism*, not a clean robustness check you can wave away.

**Risk-based vs. behavioral interpretation — genuinely unresolved.** Even granting the profits are real and net-positive, *why* do they exist? The **behavioral** camp says investors *underreact* to news (prices drift toward fundamentals slowly) and later *overreact* (the eventual long-run reversal). The **risk-based** camp says momentum loads on some priced, time-varying macro risk — and the spectacular **2009 momentum crash** (when beaten-down losers rocketed in the recovery and the short leg blew up) is exhibited as evidence that momentum carries crash risk you are compensated for. JT93 cannot adjudicate this; it predates the evidence on both sides. A careful reader reports the anomaly and labels the interpretation as open.

**Overlapping-portfolio inference (Week 2, again).** If the paper's $t$-statistics do not correct for the $K-1$ induced autocorrelation, they are overstated. This does not erase a $t$ of, say, 6, but it can sink a marginal one. The first thing to recompute in replication is Newey–West $t$-stats with lag $\geq K-1$.

---

## 7. Three replication exercises

These point at **nb5.3** (the momentum backtest) and feed **PS 5.3**. Pin your CRSP snapshot date per the conventions and keep licensed data on GMU infrastructure.

**Exercise 1 — Rebuild the $J \times K$ grid and report it honestly.** On CRSP monthly NYSE/AMEX (then optionally add Nasdaq), construct equal-weighted decile winner-minus-loser portfolios for all sixteen $J,K \in \{3,6,9,12\}$ combinations using the overlapping monthly-reformation method. Report the average monthly spread for each cell **with two standard errors side by side**: naive i.i.d. and **Newey–West** with lag $= K-1$. The deliverable is a table that makes the §2 inference point visible — show how much the $t$-statistics shrink once you respect the overlap. Confirm 6/6 is positive and ~1%/month order of magnitude over a window near the original sample; do not expect to match a textbook decimal.

**Exercise 2 — The transaction-cost critique (the PS 5.3 core).** Take your 6/6 gross series and layer on a cost model: a per-side bid-ask + commission charge applied to the *turnover* each month (the fraction of the portfolio that actually trades on re-ranking), plus a separate, larger cost on the short leg to proxy borrow fees, and a sensitivity dial for the small-cap losers. Plot net momentum profit as a function of round-trip cost in basis points, and find the **break-even cost** at which the strategy's net alpha hits zero. Write the one-paragraph verdict: at realistic costs, does momentum survive — and *which leg* kills it? This is the exercise that turns "anomaly" into "tradable or not."

**Exercise 3 — Out-of-sample and the snooping defense.** Re-estimate the 6/6 strategy in **rolling, non-overlapping sub-periods** across the full modern sample (e.g., 1965–1989 *in-sample* versus 1990–present *out-of-sample*), explicitly including the 2009 crash window. Report the spread, the worst drawdown, and the January-versus-rest-of-year decomposition in each era. The point is to let Sam *see* both the multiple-testing rebuttal (does the effect persist outside the original grid and sample?) and the crash-risk story (how brutal is the tail?) in one figure. Tie the write-up back to the risk-vs-behavioral debate of §6.

---

### Referee questions

If this manuscript landed on your desk, you would write back:

1. **Are the reported $t$-statistics corrected for the serial correlation induced by overlapping holding periods?** Please report Newey–West standard errors with lag length at least $K-1$ alongside the originals, and tell us how much the inference changes.
2. **What is the strategy's profit net of realistic transaction and short-sale costs, separately for the long and short legs?** Given that the losers are disproportionately small, illiquid, low-priced stocks, a gross-return result is not yet an efficiency violation.
3. **How do you rule out data-snooping across the sixteen $J \times K$ cells, and can you commit to an out-of-sample test?** A predicted, broad-region effect that survives in post-sample data and other markets is far more convincing than the single most-starred cell of the grid.

> **Next:** open **nb5.3** and rebuild the grid. The moment your Newey–West $t$-stats print next to the naive ones, you will understand why Week 2 came before Week 5.
