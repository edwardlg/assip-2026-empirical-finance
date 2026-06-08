# Solutions — PS 5.3 (Momentum Portfolio Replication and the Transaction-Cost Critique)

**Problem set:** `book/weeks/week-05/ps5.3.md` (PS 5.3, Week 5).
**Chapter:** Ch 5.3 — Reader's Guide: Jegadeesh & Titman (1993), with an inference callback to Ch 2.4 (HAC / Newey–West).
**Paper:** Jegadeesh, N., & Titman, S. (1993). *Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency.* Journal of Finance, 48(1), 65–91.

These are full worked solutions, not just answers. Notation follows `CONVENTIONS.md` and locks to Ch 5.3: the $J/K$ formation/holding sort; the equal-weighted zero-cost winner-minus-loser (WML) portfolio with return $r^{\text{WML}} = r^{W} - r^{L}$; the overlapping monthly-reformation (calendar-time) construction; testing a mean by regressing the series on a constant; the classical / i.i.d. versus HAC (Newey–West) standard error with lag $L$; portfolio turnover and a per-round-trip cost in basis points (1 bp $= 0.01\% = 0.0001$); the break-even cost; and the qualitative robustness checks. **Every number in this sheet is illustrative** — chosen for clean arithmetic, not transcribed from the paper. The single claim about the real paper is the Ch 5.3 order-of-magnitude one: the 6/6 WML spread is positive and roughly $\sim 1\%$/month over a sample near the original. All numerical results below were confirmed in Python; verifying notes appear where useful.

---

## Problem 1 — Build a winner-minus-loser portfolio by hand (14 points)

**(a) (4 pts)** Sort on the **past-six-month return** column (the formation signal) — *not* on the next-month column, which is the outcome we are not allowed to peek at when ranking. Descending order:

$$
\underbrace{D\,(+61)}_{\text{rank 1}},\; \underbrace{J\,(+47)}_{2},\; A\,(+38),\; G\,(+24),\; I\,(+15),\; C\,(+9),\; E\,(+2),\; H\,(-4),\; \underbrace{B\,(-12)}_{9},\; \underbrace{F\,(-27)}_{\text{rank 10}}.
$$

The **winner portfolio** is the top two, $W = \{D, J\}$. The **loser portfolio** is the bottom two, $L = \{F, B\}$. The realized next-month returns play no role here: ranking uses *only past prices*, which is exactly the one input weak-form efficiency swears is useless — the whole point of the test.

**(b) (4 pts)** Equal-weight within each leg, using the **next-month** table:

$$
r^{W} = \tfrac{1}{2}\big(r_D + r_J\big) = \tfrac{1}{2}(2.0 + 2.5) = \mathbf{2.25\%},
$$
$$
r^{L} = \tfrac{1}{2}\big(r_F + r_B\big) = \tfrac{1}{2}(4.0 + 1.0) = \mathbf{2.50\%}.
$$

The zero-cost spread is

$$
r^{\text{WML}} = r^{W} - r^{L} = 2.25\% - 2.50\% = \mathbf{-0.25\%}.
$$

(*Verified in Python: ranked, sliced top-2 / bottom-2, averaged — $r^W=2.25$, $r^L=2.50$, WML $=-0.25$.*) Note the spread came out **negative this month** — momentum "lost" — because the loser F bounced hard. That is deliberate; see part (d).

**(c) (3 pts)** It is **zero-cost** because you fund the \$1 long position in winners with the \$1 proceeds from short-selling losers: long and short legs are equal in dollars, so your *net* cash outlay is (notionally) zero and there is no capital base to divide by — the strategy's "return" is a pure spread. The spread $r^{W}-r^{L}$, not $r^{W}$ alone, is the right object to test because the subtraction **cancels whatever common movement hits winners and losers alike** — most importantly the market return. If the whole market rose 2% this month, both legs inherit that 2% and it nets out; what is left is the *differential* between past winners and past losers, which is the only thing an efficiency violation could be hiding in.

**(d) (3 pts)** Momentum is a claim about the **average of the spread across many months and many stocks**, not about any single name in any single month. F bouncing $+4\%$ is *one realization of one stock in one month* — pure idiosyncratic noise that the two-stock loser leg cannot diversify away. With ten stocks and a one-month hold, the spread is dominated by such noise, which is exactly why our toy number came out negative. Jegadeesh & Titman re-form deciles (hundreds of names per leg) and re-do the sort **every month for decades**, so the idiosyncratic bounces average out and what survives is the systematic continuation — the $\sim 1\%$/month *average* spread. One bad month no more refutes momentum than one coin landing tails refutes a fair coin's 50% rate.

---

## Problem 2 — Read the $J\times K$ returns grid like a referee (16 points)

The illustrative grid (percent/month):

| $J \backslash K$ | $K=3$ | $K=6$ | $K=9$ | $K=12$ |
|:---:|:---:|:---:|:---:|:---:|
| **$J=3$** | $0.72$ | $0.68$ | $0.55$ | $0.41$ |
| **$J=6$** | $1.08$ | $0.99$ | $0.80$ | $0.52$ |
| **$J=9$** | $1.12$ | $0.95$ | $0.71$ | $0.33$ |
| **$J=12$** | $0.94$ | $0.74$ | $0.40$ | $-0.06$ |

**(a) (4 pts)** The **6/6 cell** (row $J=6$, column $K=6$) is $\mathbf{0.99\%/\text{month}}$. That sits right on the Ch 5.3 order-of-magnitude claim — positive and $\approx 1\%$/month. Annualizing *roughly*, $0.99\% \times 12 \approx \mathbf{11.9\%/\text{year}}$ (this ignores compounding; it is an order-of-magnitude statement, not a precise annual return — a real annualization would compound and would also have to be quoted net of costs).

**(b) (5 pts)** The surface is a **medium-horizon ridge that decays toward the long-horizon corner**. (i) Holding $J=6$ fixed and lengthening the hold $K$ from 3 to 12, the spread falls monotonically: $1.08 \to 0.99 \to 0.80 \to 0.52$ — the profit is strongest at short holds and *bleeds away* as you hold longer, because the continuation is a medium-horizon phenomenon, not a permanent one. (ii) Reading into the bottom-right corner ($J=12,\,K=12$) the spread decays all the way to $-0.06$ — it goes *negative*. That sign flip foreshadows **long-run reversal** (De Bondt & Thaler, 1985): at long formation-and-holding horizons, past winners start to *under*-perform past losers as prices that overshot eventually correct. Momentum lives in the medium-horizon gap *between* short-run reversal and this long-run reversal.

**(c) (4 pts)** Two reasons the "pick the biggest cell" reading is wrong:

1. *Statistical (data-snooping).* The $1.12$ at $(9,3)$ is the **maximum over sixteen correlated tests**. Crowning the largest cell and reporting its $t$-statistic is the multiple-comparisons trap from Week 1 — the maximum of sixteen tries is upward-biased, so its apparent significance is overstated. You sharpen this in Problem 5(a).
2. *A region beats a cell.* The evidence for momentum is not one starred cell; it is that a **broad contiguous region** of the grid is positive and similar in magnitude (the entire upper-left block is $\approx 0.7$–$1.1\%$). A single hand-picked extreme could be luck; a whole coherent region moving together is a *pattern*, far harder to dismiss and far less sensitive to which exact $(J,K)$ you trade. Reporting the surface, not the peak, is the honest move.

**(d) (3 pts)** The grid shows only point estimates; what must sit *next to* every cell is its **standard error (and the $t$-statistic), and specifically the HAC / Newey–West version, not the naive i.i.d. one**. Omitting it produces the failure mode of **overstated significance**: because the overlapping construction induces positive serial correlation (Problem 3), the naive standard error is too small and the $t$-statistic too large, so cells that look "significant" may not be once the overlap is respected. A grid of bare point estimates is not yet evidence.

---

## Problem 3 — Overlapping holding periods, induced serial correlation, and why HAC (18 points)

**(a) (5 pts)** With $K=6$, the return recorded in calendar month $t$ is the equal-weighted average of the **six cohorts currently live** — those formed in months $t, t-1, \dots, t-5$. The return recorded in month $t+1$ is the average of the cohorts formed in months $t+1, t, t-1, \dots, t-4$. Line them up:

- Month $t$'s cohorts: $\{t,\, t-1,\, t-2,\, t-3,\, t-4,\, t-5\}$.
- Month $t+1$'s cohorts: $\{t+1,\, t,\, t-1,\, t-2,\, t-3,\, t-4\}$.

They **share five of the six cohorts** ($t$ through $t-4$). So even if the momentum payoff to each freshly formed cohort were i.i.d., the two reported monthly returns are averages built from $5/6$ of the *same* underlying ingredients — they are mechanically correlated. The same overlap argument applies at larger gaps: month $t$ and month $t+\ell$ share $6-\ell$ cohorts for $\ell = 1,2,\dots,5$, and share **none** once $\ell \ge 6$. So the induced autocorrelation persists over lags $\ell = 1$ through $\ell = K-1 = \mathbf{5}$ and then dies out. This is precisely the overlapping-observations mechanism from Week 2: overlapping windows manufacture serial correlation out of thin air.

**(b) (5 pts)** Sam regresses the spread series on a constant; the single coefficient $\hat\beta_0$ *is* the mean spread, and its standard error is the standard error of the mean. The classical / i.i.d. formula computes that standard error as (roughly) $s/\sqrt{T}$, which assumes all $T$ monthly observations are **independent draws**. They are not: with positive serial correlation, each new month *echoes* its neighbors, so it carries less fresh information than an independent draw would. The Moulton-style intuition from Ch 2.4 §5.3: the **effective** sample size — the number of genuinely independent observations — is *well below* $T$. The naive formula divides by an effective $T$ that is **too large**, so it reports a standard error that is **too small** and a $t$-statistic that is **too large**. The direction of the error is therefore toward **over-confidence**: Sam will think momentum is more decisively significant than the data actually warrant.

**(c) (4 pts)** The fix is the **HAC (heteroskedasticity-and-autocorrelation-consistent) standard error, a.k.a. Newey–West**. For the 6/6 strategy set the lag length $L = K - 1 = \mathbf{5}$: from part (a) that is exactly how many lags of induced autocorrelation the overlap creates before it vanishes, so $L=5$ absorbs all of it (rounding up further does no harm). Arithmetically, HAC adds to the "middle of the sandwich" the **cross-products of residuals from nearby months**, $\hat\varepsilon_t\hat\varepsilon_{t-\ell}$ for $\ell = 1,\dots,L$, down-weighted by the Bartlett kernel — terms the classical formula assumes are zero. Crucially the **point estimate is unchanged**: the mean spread is still the mean spread regardless of which standard error you compute; only the standard error (hence the $t$-statistic) moves.

**(d) (4 pts)** Mean spread $= 1.00\%$, classical SE $= 0.083\%$, HAC ($L=5$) SE $= 0.122\%$.

(i) The two $t$-statistics:
$$
t_{\text{classical}} = \frac{1.00}{0.083} \approx \mathbf{12.05}, \qquad t_{\text{HAC}} = \frac{1.00}{0.122} \approx \mathbf{8.20}.
$$
(*Verified in Python. The HAC SE is $0.122/0.083 \approx 1.47\times$ the classical — "roughly half-again larger," consistent with the reader's guide.*)

(ii) **Yes, it survives.** Both far exceed $1.96$; momentum is overwhelmingly significant here, and the switch from classical to HAC merely shrinks an enormous $t$ to a still-enormous $t$. A $t$ of 8 does not become insignificant when inflated by a factor of $1.47$.

(iii) The switch would **flip** the conclusion when the original $t$ is **marginal** — say a naive $t \approx 2.5$ that, divided by the same $\approx 1.47$ inflation, lands near $1.7$ and falls below $1.96$. That is exactly the case Ch 5.3 tells a referee to check first: a comfortable $t$ of 6 survives the overlap correction, but a marginal starred result can be entirely an artifact of the too-small naive standard error — so the first question on the referee's notepad is *"are these $t$-statistics overlap-corrected?"*

---

## Problem 4 — The transaction-cost critique and the break-even cost (22 points)

Cost model and illustrative inputs:
$$
\text{net}(c) = \bar g - c\,\bar\tau_L - (c+\text{sp})\,\bar\tau_S, \qquad
\bar g = 100\text{ bps},\;\; \bar\tau_L = 0.30,\;\; \bar\tau_S = 0.30,\;\; \text{sp} = 40\text{ bps}.
$$

**(a) (4 pts)** You multiply the cost by **turnover** — the fraction of each leg that actually *changes hands* on re-ranking — because **you only pay trading costs on the shares you trade**, not on the shares you simply continue to hold. A name that stays in the winner decile from one month to the next costs nothing to "keep"; only the slice that enters or exits the decile incurs the round-trip bid-ask + commission. Charging the cost against the whole book would massively overstate the bill. The short leg gets the extra premium because **shorting beaten-down small-cap losers is physically more expensive**: those names are illiquid and low-priced with wide bid-ask spreads, and you must *borrow the shares to short them*, paying a borrow / stock-loan fee that the long leg of large-cap winners never incurs. The leg the reader's guide warns is the dangerous one is precisely this short leg.

**(b) (6 pts)** At $c = 50$ bps:
$$
\text{long-leg cost} = c\,\bar\tau_L = 50 \times 0.30 = 15\text{ bps}, \qquad
\text{short-leg cost} = (c+\text{sp})\,\bar\tau_S = (50+40)\times 0.30 = 27\text{ bps},
$$
$$
\text{net}(50) = 100 - 15 - 27 = \mathbf{58\text{ bps/month}}.
$$
At $c = 100$ bps:
$$
\text{long-leg cost} = 100 \times 0.30 = 30\text{ bps}, \qquad
\text{short-leg cost} = (100+40)\times 0.30 = 42\text{ bps},
$$
$$
\text{net}(100) = 100 - 30 - 42 = \mathbf{28\text{ bps/month}}.
$$
The strategy is **net-profitable at both** cost levels (58 bps and 28 bps respectively) — unsurprising, since both lie below the break-even computed next. (*Verified in Python.*)

**(c) (6 pts)** Set $\text{net}(c)=0$ and solve for $c$:
$$
\bar g - c\,\bar\tau_L - (c+\text{sp})\,\bar\tau_S = 0
\;\Longrightarrow\;
\bar g - \text{sp}\,\bar\tau_S = c\,(\bar\tau_L + \bar\tau_S)
\;\Longrightarrow\;
c^\star = \frac{\bar g - \text{sp}\,\bar\tau_S}{\bar\tau_L + \bar\tau_S}.
$$
The $+\text{sp}\,\bar\tau_S$ term moves to the gross side because the short premium is a *fixed* charge on the short leg that eats into the gross profit before the per-round-trip cost $c$ even applies. Plugging in:
$$
c^\star = \frac{100 - 40\times 0.30}{0.30 + 0.30} = \frac{100 - 12}{0.60} = \frac{88}{0.60} \approx \mathbf{146.7\text{ bps}}.
$$
(*Verified in Python: $\text{net}(146.7) \approx 0$.*) As a check on which leg does the damage, set $\text{sp}=0$:
$$
c^\star_{\text{no sp}} = \frac{100}{0.60} \approx 166.7\text{ bps}.
$$
So the short-leg borrow premium **lowers the break-even by $166.7 - 146.7 = 20$ bps** — the short leg makes the strategy break even at a $20$-bp-*lower* round-trip cost than it otherwise would, confirming it is the more fragile leg.

**(d) (3 pts) Verdict.** At a break-even of $\approx 147$ bps round-trip, this illustrative 6/6 strategy *does* survive realistic costs **on the liquid long leg alone** — large-cap winners trading at $20$–$30$ bps round-trip leave the gross $\sim 1\%$/month largely intact. The danger is the **short leg**: the beaten-down small-cap losers can cost several times the winners' rate, and once their effective round-trip cost (bid-ask + price impact + borrow) approaches and exceeds the break-even neighborhood, the net profit collapses. So the honest conclusion mirrors the reader's guide's contested verdict: momentum's *gross* profit is real, but a meaningful share of it is trading friction, and **the short leg in small, illiquid losers is what kills it** — which is exactly why a gross-return result is not yet an efficiency violation. Whether momentum is a true anomaly or a paper profit depends on whether you can actually trade the losers at the costs your break-even can tolerate.

**(e) (3 pts)** Subtracting the monthly cost lowers the **mean** of the net series (gross mean $100$ bps $\to$ net mean $58$ bps at $c=50$, etc.) but barely touches its **standard deviation** — the cost is a roughly steady monthly drag, not a new source of volatility, since turnover is fairly stable month to month. The $t$-statistic is mean/SE, so shrinking the numerator while the denominator holds steady **drags the $t$ down even though the net mean stays positive**. A strategy can thus be "profitable on average but no longer statistically distinguishable from zero": the net mean is positive but small relative to the unchanged month-to-month noise, so you can no longer reject the hypothesis that the *true* net spread is zero. This is the bridge between Problems 3 and 4 — the cost critique can sink significance even when it does not sink the average.

---

## Problem 5 — What's vulnerable: data-snooping, January, and risk vs. behavioral (16 points)

**(a) (6 pts) Data-snooping.** (i) The grid is **sixteen correlated significance tests**; crowning the single most-significant cell and reporting its $t$-statistic is the **multiple-comparisons / multiple-testing problem** from Week 1 (Ch 1.5, revisited under the false-discovery rate later). The *maximum* over sixteen tries is upward-biased even under the null — run enough correlated tests and one will star by chance — so a "$t=2.5$ that is the max over sixteen cells" is worth far less than a $t=2.5$ chosen in advance; a reader should mentally Bonferroni-discount it. (ii) Two mitigating facts: first, the result is **a broad region of positive cells, not one isolated lucky cell** (Problem 2b) — a coherent surface is much harder to produce by snooping than a single extreme. Second, momentum **replicated out of sample**: in other countries, other asset classes, and the decades *after* 1989 that the original authors could not have peeked at. Out-of-sample survival is the strongest answer to a snooping charge because you cannot snoop data that did not exist when the hypothesis was formed — post-sample confirmation is evidence the effect is real rather than a fit to one historical window.

**(b) (5 pts) January / seasonality.** (i) Momentum tends to **lose money in January and earn its keep in the other eleven months** — an *anti*-January pattern. Mechanism: the loser leg is full of beaten-down, small, low-priced stocks; these bounce hard in January (tax-loss-selling pressure releases at year-end and the names rebound), so the short leg gets hurt precisely in January. (ii) An anti-January result is **harder** to dismiss than a January-concentrated one because the era's known anomalies (size, value) were *concentrated in* January, so a profit living in January would look like just another seasonal artifact; a profit that *survives despite* a January loss cannot be that artifact. Yet the reader's guide still files it under "vulnerable" because the seasonality is a **clue to mechanism, not a clean robustness pass**: a strategy whose annual profit is "eleven good months minus a January loss" is exposed to anything that shifts that seasonal structure (changes to tax-loss-selling rules, the rise of index investing), so the seasonal dependence is itself a fragility, not a checkbox.

**(c) (5 pts) Risk vs. behavioral.** The **behavioral** story is a two-stage under/over-reaction: investors *underreact* to news so prices drift toward fundamentals only slowly (this is the medium-horizon continuation momentum profits from), and then later *overreact*, pushing prices past fundamentals so they eventually correct (this is the long-run reversal seen in the bottom-right of the grid and in De Bondt–Thaler). The **risk-based** story says momentum loads on some priced, time-varying macro risk and the profit is compensation for bearing it — and the evidence cited is the **2009 momentum crash**, when the beaten-down losers rocketed in the recovery and the short leg blew up, exhibiting the kind of rare, severe crash risk an investor would demand to be paid for. Jegadeesh & Titman (1993) **cannot adjudicate** between these because it *predates the evidence on both sides* — the long-run-reversal and crash-risk data accumulated only later. The honest write-up therefore **reports the anomaly as real and labels the interpretation as open**, taking no premature side.

---

## Problem 6 — Replication design (pointing at nb5.3) (14 points)

**(a) (5 pts) Construction recipe (6/6 cell).** At the end of each month $t$:
1. **Ranking variable:** compute each stock's cumulative return over the past $J=6$ months (months $t-5$ through $t$).
2. **Split:** sort all eligible stocks on that past return into ten deciles.
3. **Form legs (equal-weighted):** long the top decile (winners $W$), short the bottom decile (losers $L$), equal dollars per leg so the position is zero-cost.
4. **Overlapping reformation:** repeat this *every* month; in any calendar month you hold $K=6$ overlapping cohorts at once (formed this month back through five months ago) and average across them.
5. **Record:** one number per month — the cohort-averaged WML spread $r^{W}-r^{L}$.

**Data:** **CRSP monthly returns**, restricted in the original to **NYSE/AMEX common stocks** over **1965–1989** (per Jegadeesh & Titman 1993; for the modern replication expect the magnitudes to shift, so report order-of-magnitude only rather than matching a table decimal). **Licensed-data rule (CONVENTIONS §5):** CRSP stays on GMU infrastructure (read-only on Hopper / WRDS Cloud), and you must **pin the CRSP snapshot date** in the notebook.

**(b) (4 pts)** Report **two standard errors side by side for every cell: the naive i.i.d. (classical) and the Newey–West (HAC)** — because the overlapping construction induces serial correlation that makes the naive SE too small (Problem 3), and showing both makes the $t$-shrinkage visible. For the 6/6 cell set the **lag length $L = K-1 = 5$**. Expected result the reader's guide licenses: **6/6 should be positive and on the order of $\sim 1\%$/month** over a window near the original. The one thing you must *not* do: **claim to match a specific decimal from the paper's table** — magnitudes shift with sample and data vintage; assert order of magnitude only.

**(c) (3 pts) Transaction-cost deliverable.** Plot **net momentum profit as a function of the round-trip cost $c$ (in bps)**, with turnover measured from the *actual* portfolio weights and an extra premium on the short leg. Locate the **break-even cost $c^\star$** (the $c$ where net profit crosses zero — Problem 4c). The figure must support a one-paragraph verdict on whether momentum survives realistic costs and *which leg* kills it; expect the **short leg** (illiquid small-cap losers) to dominate the cost.

**(d) (2 pts) Robustness checks.** (1) *Data-snooping:* an **out-of-sample re-estimation** — split into in-sample (near 1965–1989) versus out-of-sample (1990–present, including the 2009 crash window) and show 6/6 persists; the demonstrating figure is the spread (and worst drawdown) in each era. (2) *Seasonality:* a **January-versus-rest-of-year decomposition** of the 6/6 spread; the demonstrating split is mean spread in January vs. the other eleven months, showing the anti-January pattern.

---

*End of solutions for PS 5.3. The by-hand portfolio (Problem 1), the two $t$-statistics (Problem 3d), and the net-spread and break-even arithmetic (Problem 4b–c) were each confirmed in a few lines of Python: break-even $c^\star = (100 - 40\times0.30)/0.60 = 146.7$ bps, dropping to $166.7$ bps with no short premium; $\text{net}(50)=58$, $\text{net}(100)=28$ bps; $t_{\text{classical}}=12.05$, $t_{\text{HAC}}=8.20$. The grid reading (Problem 2), the HAC machinery (Problem 3), and the cost sweep (Problem 4) are all built in `notebooks/week-05/nb5.3-momentum-backtest.ipynb`, where the Newey–West $t$-statistic prints next to the naive one and the break-even line appears on the net-profit plot.*
