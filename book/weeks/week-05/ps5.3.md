# PS 5.3 — Momentum Portfolio Replication and the Transaction-Cost Critique

**Course:** ASSIP 2026 · 8-Week Empirical Finance Track · Week 5 · Problem Set 5.3
**Covers:** Ch 5.3 (Reader's Guide: Jegadeesh & Titman 1993), with an inference callback to Ch 2.4 (HAC / Newey–West).
**Paper:** Jegadeesh, N., & Titman, S. (1993). *Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency.* Journal of Finance, 48(1), 65–91.
**Methods allowed:** only what is built through Ch 5.3 and the Week-2 inference toolkit — the $J/K$ formation/holding sort; decile ranking on past cumulative return; the equal-weighted, zero-cost **winner-minus-loser** (WML) portfolio with return $r^{W}-r^{L}$; the overlapping monthly-reformation (calendar-time) construction and the serial correlation it induces; testing a mean return by regressing the series on a constant; the distinction between an i.i.d. / classical standard error and a **HAC (Newey–West)** standard error with lag $L$; the Moulton-style "effective sample size" intuition for why positive autocorrelation deflates standard errors; portfolio **turnover** and a per-round-trip transaction-cost charge in basis points; a **break-even cost**; and the qualitative robustness checks from the reader's guide (risk adjustment, sub-periods, the January/seasonality decomposition, data-snooping across the grid, the risk-vs-behavioral debate). You do **not** need factor regressions (Ch 5.2), the full Newey–West sandwich algebra, or any matrix manipulation beyond what Ch 2.4 already showed.

**Total: 100 points.** Point values are stated per problem. Show your reasoning — a correct final number with no derivation earns roughly half credit, because the reasoning *is* the skill we are grading. Solutions are in Appendix E (`E-w5-ps5.3-solutions.md`); try every part before you look.

A note on the difficulty curve. Problem 1 is a by-hand warm-up: rank a small universe and build the WML portfolio so the mechanics are in your fingers. Problem 2 makes you read a $J\times K$ grid the way a referee reads it — as a surface, not a number. Problem 3 is the conceptual core and the reason Week 2 came before Week 5: *why* the overlapping construction manufactures serial correlation, *why* the naive $t$-statistic is therefore a lie, and *what* HAC/Newey–West does about it. Problem 4 is the transaction-cost / break-even computation that turns "anomaly" into "tradable or not" — the heart of the sheet. Problem 5 is the "what's vulnerable" task: data-snooping, the January effect, and the unresolved risk-vs-behavioral question. Problem 6 is a replication-design task that hands off to `nb5.3`. Throughout we stay with **Sam**, our markets-and-momentum student, who has wanted to build this strategy all week.

**A standing rule on numbers.** Every return figure in this sheet is **illustrative** — clearly labeled, internally consistent, and chosen to make the arithmetic clean. They are *not* transcribed from Jegadeesh & Titman's tables; do not memorize them as the paper's results. The only claim we make about the real paper is the order-of-magnitude one from Ch 5.3: the classic six-month-formation / six-month-holding (6/6) winner-minus-loser spread is **positive and on the order of roughly 1% per month** over a sample near the original. Treat any specific decimal below as a teaching prop.

---

## Problem 1 — Build a winner-minus-loser portfolio by hand (14 points)

Sam pulls a tiny universe of ten stocks and their cumulative returns over the past six months (the formation period, $J=6$). To keep the arithmetic by hand, we will use **quintiles of two** rather than the paper's deciles: the **two** highest-ranked stocks form the winner portfolio $W$, the **two** lowest form the loser portfolio $L$. Each leg is **equal-weighted** within itself.

| Stock | A | B | C | D | E | F | G | H | I | J |
|-------|---|---|---|---|---|---|---|---|---|---|
| Past-6-month return (%) | $+38$ | $-12$ | $+9$ | $+61$ | $+2$ | $-27$ | $+24$ | $-4$ | $+15$ | $+47$ |

After ranking on the **past** return, Sam holds the portfolio for the **next** month ($K=1$ for this warm-up). The realized **next-month** returns of the same ten stocks turn out to be:

| Stock | A | B | C | D | E | F | G | H | I | J |
|-------|---|---|---|---|---|---|---|---|---|---|
| Next-month return (%) | $+3.0$ | $+1.0$ | $+0.5$ | $+2.0$ | $-0.5$ | $+4.0$ | $+1.5$ | $-1.0$ | $+0.0$ | $+2.5$ |

**(a) (4 pts)** Rank the ten stocks by their *past-six-month* return and name the two members of the winner portfolio $W$ and the two members of the loser portfolio $L$. State explicitly which column you sorted on, and note that the realized next-month returns play *no role* in the ranking.

**(b) (4 pts)** Compute the equal-weighted realized next-month return of the winner leg $r^{W}$ and of the loser leg $r^{L}$, using the next-month-return table. Then compute the zero-cost winner-minus-loser spread $r^{\text{WML}}=r^{W}-r^{L}$. Show the averaging.

**(c) (3 pts)** Explain in two sentences why this is called a **zero-cost** portfolio, and why the number you just computed is the right object to test for an efficiency violation rather than $r^{W}$ alone. (Hint: what does going long \$1 of winners *and short \$1 of losers* do to your net cash outlay, and what common movement does the subtraction cancel?)

**(d) (3 pts)** Stock F was the *worst* past performer (a loser) yet had the *best* next-month return ($+4.0\%$). In one or two sentences, explain why a single stock bouncing like this does **not** by itself refute momentum — i.e., what momentum is a claim about (the *average* of the spread across many months and many stocks) versus what F is (one realization of one name in one month). Connect this to why the paper re-forms the portfolio every month over decades rather than betting on one sort.

---

## Problem 2 — Read the $J\times K$ returns grid like a referee (16 points)

Jegadeesh & Titman's headline object is a grid: formation period $J$ down the rows, holding period $K$ across the columns, each cell the **average monthly WML spread** for that strategy. Below is an **illustrative** $4\times 4$ grid in percent per month (clearly fictional, chosen to show the shape the reader's guide describes — positive in the medium-horizon region, decaying as both $J$ and $K$ grow long, with the 6/6 cell near $1\%/$month). Read it as a *surface*.

| $J \backslash K$ | $K=3$ | $K=6$ | $K=9$ | $K=12$ |
|:---:|:---:|:---:|:---:|:---:|
| **$J=3$** | $0.72$ | $0.68$ | $0.55$ | $0.41$ |
| **$J=6$** | $1.08$ | $0.99$ | $0.80$ | $0.52$ |
| **$J=9$** | $1.12$ | $0.95$ | $0.71$ | $0.33$ |
| **$J=12$** | $0.94$ | $0.74$ | $0.40$ | $-0.06$ |

**(a) (4 pts)** Locate the **6/6** cell and state its value. In one sentence, say how it compares to the Ch 5.3 order-of-magnitude claim, and annualize it *roughly* (a simple $\times 12$ is fine for the order of magnitude — state that you are ignoring compounding).

**(b) (5 pts)** Describe the **shape** of the surface in two or three sentences. Specifically: (i) holding $J$ fixed at $6$, what happens to the spread as the holding period $K$ lengthens from $3$ to $12$? (ii) Reading down toward the bottom-right ($J=12$, $K=12$), what happens, and what later-horizon phenomenon from the reader's guide (the De Bondt–Thaler one) does that decaying / sign-flipping corner *foreshadow*? Name it.

**(c) (4 pts)** A classmate scans the grid, points at the single largest cell ($J=9$, $K=3$, at $1.12$), and says "that's the strategy — it's the most profitable, so that's the one to trade and report." Give two distinct reasons this is the wrong way to read the grid. (Hint: one reason is statistical and you will sharpen it in Problem 5; the other is about what a *region* of positive cells tells you that a single hand-picked cell does not.)

**(d) (3 pts)** The grid above shows only the **point estimates**. State the one column of information the reader's guide insists must sit *next to* every cell before you are allowed to believe any of it, and name the specific failure mode that omitting it produces. (You will compute exactly this object in Problem 3.)

---

## Problem 3 — Overlapping holding periods, induced serial correlation, and why HAC (18 points)

This is the inference core, and it is the reason the syllabus puts Week 2 before Week 5. Recall from Ch 5.3 the **overlapping monthly-reformation** construction: rather than rebalance once every $K$ months, Jegadeesh & Titman form a *fresh* WML portfolio every single month and hold each one for $K$ months. So the return you record in calendar month $t$ is the **equal-weighted average across the $K$ cohorts currently live** — the one formed this month, last month, …, back to $K-1$ months ago.

Take the 6/6 strategy, so $K=6$.

**(a) (5 pts)** Explain, in your own words and with explicit reference to *shared cohorts*, why the reported monthly return in month $t$ and the reported monthly return in month $t+1$ are **mechanically correlated even if the underlying momentum signal were i.i.d. across cohorts**. Your answer must state: how many of the $K=6$ cohorts that determine month $t$'s return are *also* among the cohorts determining month $t+1$'s return, and therefore over how many lags ($\ell = 1, 2, \dots$) you expect the induced autocorrelation to persist before it dies out. (This is the exact overlapping-observations mechanism from Week 2.)

**(b) (5 pts)** Now connect it to the standard error. Sam regresses the 6/6 spread series on a constant to test whether its mean differs from zero (a one-regressor OLS where $\hat\beta_0$ *is* the mean spread). Using the **effective-sample-size** intuition from Ch 2.4 §5.3: explain why **positive** serial correlation makes the *classical / i.i.d.* standard error on that mean **too small**, and therefore the $t$-statistic **too large**. State precisely which quantity the naive formula gets wrong (Hint: it divides by an effective $T$ that is too ____), and state which direction the error goes — does it make Sam *over*- or *under*-confident that momentum is real?

**(c) (4 pts)** State the fix from Ch 2.4 by name, and give the **lag length** $L$ you would set for the 6/6 strategy and a one-sentence justification tied to your answer in part (a). Then explain in one sentence what the HAC estimator does *arithmetically* that the classical formula does not (what extra terms enter the "middle of the sandwich"), and confirm that the **point estimate** — the mean spread itself — is *unchanged* by switching to HAC; only the standard error moves.

**(d) (4 pts)** Sam computes, for the 6/6 series, a mean spread of $1.00\%$/month with a **classical** standard error of $0.083\%$ and a **Newey–West (HAC, $L=5$)** standard error of $0.122\%$. (Illustrative numbers, consistent with the reader's guide's claim that the HAC SE is roughly half-again larger.)
&nbsp;&nbsp;(i) Compute both $t$-statistics ($t=\text{mean}/\text{SE}$), to two decimals.
&nbsp;&nbsp;(ii) At the conventional $|t|>1.96$ bar, does the conclusion ("momentum is significant") survive the switch from classical to HAC here?
&nbsp;&nbsp;(iii) In one sentence, describe the situation — a *marginal* original $t$-statistic — in which the same switch would **flip** a "significant" result to "not significant," and say why that is exactly the case the reader's guide warns a referee to check first.

---

## Problem 4 — The transaction-cost critique and the break-even cost (22 points)

This is the heart of the sheet: the exercise that decides whether a gross anomaly is a *tradable* anomaly. Momentum is a **high-turnover** strategy — every month you re-rank and trade a fresh slice of the book — and the losers you short are disproportionately small, illiquid, low-priced names with wide bid-ask spreads, the most expensive stocks to trade. Ch 5.3 insists: *any claim of momentum profits must be quoted net of a credible cost model.*

Here is the cost model, the same one `nb5.3` builds. The strategy holds a long leg (winners) and a short leg (losers). Each month, **turnover** on a leg is the fraction of that leg's dollar book that actually changes hands on re-ranking — the round-trip notional traded as a share of the leg. We charge a per-round-trip cost $c$, in **basis points** (1 bp $= 0.01\% = 0.0001$), on the traded notional of *each* leg, plus an **extra premium** $\text{sp}$ on the short leg to proxy the borrow fee / wider spreads on illiquid losers. With $\bar g$ the gross mean spread (per month), $\bar\tau_L$ the average long-leg turnover, and $\bar\tau_S$ the average short-leg turnover, the **net** mean spread is

$$
\text{net}(c) \;=\; \bar g \;-\; c\,\bar\tau_L \;-\; (c+\text{sp})\,\bar\tau_S .
$$

Use these **illustrative** inputs throughout (consistent with `nb5.3`'s order of magnitude):

- Gross 6/6 mean spread $\bar g = 1.00\%/\text{month} = 100$ bps.
- Average long-leg turnover $\bar\tau_L = 0.30$ (30% of the winner book trades each month).
- Average short-leg turnover $\bar\tau_S = 0.30$ (30% of the loser book trades each month).
- Short-leg premium $\text{sp} = 40$ bps.

**(a) (4 pts)** First, intuition before arithmetic. In one or two sentences, explain *why* turnover is the right thing to multiply the cost by (rather than, say, the total book value), and *why* the short leg gets an extra premium — i.e., what is physically different about shorting beaten-down small-cap losers versus holding large-cap winners.

**(b) (6 pts)** Compute the **net** mean spread at a round-trip cost of $c=50$ bps and again at $c=100$ bps, in bps per month, using the formula above. Show the two cost components (long-leg cost $c\,\bar\tau_L$ and short-leg cost $(c+\text{sp})\,\bar\tau_S$) separately at each $c$. At which of these two cost levels, if either, is the strategy still net-profitable?

**(c) (6 pts)** Derive the **break-even** round-trip cost $c^\star$ — the value of $c$ at which $\text{net}(c)=0$ — *algebraically* from the formula, then plug in the numbers. (Set $\text{net}(c)=0$ and solve for $c$; note the $+\text{sp}\,\bar\tau_S$ term moves to the gross side.) Report $c^\star$ in bps to one decimal. Then, as a check on *which leg does the damage*, compute the break-even **as if there were no short premium** ($\text{sp}=0$) and state in one sentence how much the borrow-cost premium on the short leg lowers the break-even.

**(d) (3 pts)** A realistic round-trip institutional cost for the *liquid* large-cap winners might be on the order of $20$–$30$ bps, but the *illiquid* small-cap losers on the short leg can run several times that. Given your $c^\star$ from part (c), write the **one-paragraph verdict** the reader's guide asks for: at realistic costs, does this illustrative 6/6 strategy survive, *which leg* is doing the killing, and what does this imply for whether momentum is a genuine efficiency violation versus a paper profit that disappears at the trading desk?

**(e) (3 pts)** Now combine Problem 3 and Problem 4. The *gross* series had a HAC $t$-statistic comfortably above 2 (Problem 3d). Explain in two or three sentences why subtracting the monthly cost can drag the **net** series' $t$-statistic below 2 *even when the net mean is still positive* — i.e., why a strategy can be "profitable on average but no longer statistically distinguishable from zero" once costs are charged. (Hint: think about what the cost subtraction does to the *mean* of the net series relative to its *standard deviation*, which costs barely change.)

---

## Problem 5 — What's vulnerable: data-snooping, January, and risk vs. behavioral (16 points)

A referee's job. Even granting the gross numbers, Ch 5.3 lists live threats to the momentum result. This problem makes you reason about three of them.

**(a) (6 pts) Data-snooping (Week 1's multiple testing).** The $J\times K$ grid in Problem 2 is **sixteen** strategies, hence sixteen significance tests on heavily *correlated* data.
&nbsp;&nbsp;(i) Explain in two sentences why crowning the single most-significant cell and reporting its $t$-statistic overstates the evidence — name the Week-1 problem this is (the one revisited under FDR later) and what a "$t=2.5$ that is the maximum over sixteen tries" is really worth.
&nbsp;&nbsp;(ii) Then give the **two** mitigating facts from the reader's guide that make momentum *more* defensible against a snooping charge than a typical lone-cell anomaly — one about the *shape* of the grid (Problem 2b), and one about what happened *after* 1989. State why out-of-sample survival is the strongest available answer to "you just snooped."

**(b) (5 pts) The January / seasonality effect.** The size and value anomalies of the era were famously concentrated in January. Momentum has the *opposite* relationship with January.
&nbsp;&nbsp;(i) State what momentum tends to do in January versus the other eleven months, and give the one-sentence mechanism the reader's guide offers (what kind of stocks sit in the loser leg, and what happens to them at year-end).
&nbsp;&nbsp;(ii) Explain why this *anti*-January pattern makes the result **harder** to dismiss as a seasonality artifact than if the profits had been concentrated *in* January — yet why the reader's guide still files seasonality under "vulnerable" rather than "robustness check passed." (Hint: it is a clue to *mechanism*, and a strategy whose annual profit is eleven months minus a January loss is exposed to anything that shifts that seasonal pattern.)

**(c) (5 pts) Risk-based vs. behavioral — the unresolved question.** Suppose every prior problem has gone momentum's way: the spread is positive, HAC-significant, survives realistic costs, and replicates out of sample. State the *two* competing explanations for *why* momentum exists — the **behavioral** story (name the two-stage under/over-reaction mechanism) and the **risk-based** story (name the specific tail event the reader's guide cites as evidence that momentum carries a priced crash risk). Then state, in one sentence, why Jegadeesh & Titman (1993) itself cannot adjudicate between them, and what the intellectually honest write-up therefore does.

---

## Problem 6 — Replication design (pointing at nb5.3) (14 points)

Sam is about to open `nb5.3` and rebuild the strategy on modern CRSP. Before touching the keyboard, he must write down the design so the result is honest and reproducible. Answer each in the empirical-spec spirit of CONVENTIONS §4 — name the object, not a hand-wave.

**(a) (5 pts)** Write the **construction recipe** for one cell of the grid (say 6/6) as a numbered procedure a classmate could follow: what you compute at the end of each month $t$ (the ranking variable), how you split the universe, how you form the equal-weighted long and short legs, the overlapping-reformation step, and what single number you record each month. State the **data**: which return file, which exchange filter and sample window the reader's guide flags as the original's order of magnitude, and the one CONVENTIONS rule about licensed data you must honor (where it lives, and what you must pin).

**(b) (4 pts)** State the **two standard errors you will report side by side** for every cell and why (tie to Problem 3), the **lag length** you will set for the 6/6 cell, and the one sentence of expected result the reader's guide licenses you to predict for 6/6 over a window near the original sample. Flag explicitly the one thing you must *not* do: claim to match a specific decimal from the paper's table.

**(c) (3 pts)** State the **transaction-cost deliverable**: what you plot (net profit as a function of what), the one number you must locate on that plot (from Problem 4), and the one-paragraph verdict the figure must support. Name which leg you expect to dominate the cost.

**(d) (2 pts)** Name **two** robustness checks from Problem 5 you will add to the replication so the write-up survives a referee — one addressing data-snooping and one addressing seasonality — and in each case state the single figure or split that demonstrates it.

---

*End of PS 5.3. When you have attempted everything, check yourself against `book/appendices/E-solutions-manual/E-w5-ps5.3-solutions.md`. The by-hand pieces (Problems 1, 3d, 4b–c) can be confirmed on paper or in three lines of Python; the grid reading (Problem 2), the inference machinery (Problem 3), and the cost critique (Problem 4) come alive in `nb5.3` (`notebooks/week-05/nb5.3-momentum-backtest.ipynb`), where you build the $J\times K$ grid on real (or, offline, synthetic) data, print the Newey–West $t$-statistic next to the naive one and watch it shrink, measure turnover from the actual portfolio weights, and sweep the round-trip cost until the net profit crosses zero. The moment that break-even line appears, you will understand why Ch 5.3 calls the cost critique "the exercise that turns 'anomaly' into 'tradable or not.'"*
