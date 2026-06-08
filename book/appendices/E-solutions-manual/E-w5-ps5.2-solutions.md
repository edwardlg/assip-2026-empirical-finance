# Solutions — Problem Set 5.2 (FF93 Factor Construction & Time-Series Regressions)

Full worked solutions to `book/weeks/week-05/ps5.2.md`, covering Chapter 5.2 (Reader's Guide: Fama &
French (1993)). Notation follows the Conventions: $R_{it}$ is portfolio $i$'s return in month $t$,
$R_{ft}$ the risk-free rate, $R_{Mt} - R_{ft}$ the market excess return; the three factors are the
market excess return, **SMB** ("small minus big," the size factor), and **HML** ("high minus low," the
value factor). The estimated time-series regression for a test portfolio $i$ is
$$
R_{it} - R_{ft} = \alpha_i + b_i\,(R_{Mt} - R_{ft}) + s_i\,\text{SMB}_t + h_i\,\text{HML}_t + \varepsilon_{it},
$$
with loadings $\hat b_i, \hat s_i, \hat h_i$ and pricing error $\hat\alpha_i$. The recurring theme of the
key: **a factor model is read two ways — the $R^2$ for *common variation* (how much of the portfolio's
month-to-month wiggle the factors share) and the intercept $\alpha$ for *pricing* (how much average
return is left unexplained) — and FF93's real test is whether all the intercepts are *jointly* zero
(GRS), not whether any single one is.**

**The working world (carried across Problems 1–3):** six value-weighted corner portfolios from a 2×3
size × BE/ME sort, illustrative excess returns (%/month):

| | Low BE/ME | Medium BE/ME | High BE/ME |
|:---|:---:|:---:|:---:|
| **Small** | S-Low $= 0.30$ | S-Med $= 0.95$ | S-High $= 1.50$ |
| **Big**   | B-Low $= 0.45$ | B-Med $= 0.70$ | B-High $= 0.85$ |

**Every number in this set is illustrative**, invented for clean arithmetic — *not* a Fama–French table
value. All arithmetic below was verified in `python3`.

---

## Problem 1 — Construct SMB and HML by hand (18 pts)

**(a)** [6 pts] **SMB.** Average the three small portfolios, average the three big portfolios, difference.

$$
\overline{\text{Small}} = \tfrac{1}{3}(0.30 + 0.95 + 1.50) = \tfrac{2.75}{3} = 0.91\overline{6},
$$
$$
\overline{\text{Big}} = \tfrac{1}{3}(0.45 + 0.70 + 0.85) = \tfrac{2.00}{3} = 0.66\overline{6},
$$
$$
\boxed{\text{SMB} = 0.91\overline{6} - 0.66\overline{6} = 0.25.}
$$

**What SMB is, in words:** the return on a portfolio that is **long the average small-cap stock and
short the average big-cap stock**, holding the value tilt fixed. An investor "holding SMB" is making a
pure bet that *small stocks out-earn big stocks this month*; here that bet paid $+0.25\%$.

**(b)** [6 pts] **HML.** Average the two high-BE/ME (value) portfolios, average the two low-BE/ME
(growth) portfolios, difference.

$$
\overline{\text{High}} = \tfrac{1}{2}(\text{S-High} + \text{B-High}) = \tfrac{1}{2}(1.50 + 0.85) = \tfrac{2.35}{2} = 1.175,
$$
$$
\overline{\text{Low}} = \tfrac{1}{2}(\text{S-Low} + \text{B-Low}) = \tfrac{1}{2}(0.30 + 0.45) = \tfrac{0.75}{2} = 0.375,
$$
$$
\boxed{\text{HML} = 1.175 - 0.375 = 0.80.}
$$

**What HML is, in words:** the return on a portfolio **long the average high-book-to-market (value)
stock and short the average low-book-to-market (growth) stock**, holding the size tilt fixed. An
investor "holding HML" bets that *value out-earns growth this month*; here that bet paid $+0.80\%$.

**(c)** [4 pts] **Why average across the other characteristic.** The averaging makes each factor a
*clean, neutral* bet on one characteristic. SMB averages over all three value buckets before
differencing small minus big, so its value tilt roughly cancels — it is a size bet **neutral** to value.
HML averages over both size buckets before differencing value minus growth, so its size tilt roughly
cancels — a value bet **neutral** to size. If instead you built a "size factor" as just S-High $-$
B-High (small-value minus big-value), that single difference would **contaminate** the size bet with a
value bet: you'd be comparing small *value* stocks to big *value* stocks, and any difference in how
value-tilted the two are would leak in. The instinct is exactly Frisch–Waugh–Lovell (Ch 2.3): to isolate
the effect of one variable, partial the other one out — here, average over the value dimension to strip
its influence out of the size factor (and vice versa), so the two factors don't step on each other and
their loadings in the §2 regression stay interpretable.

**(d)** [2 pts] **The naive size bets disagree:**
$$
\text{S-High} - \text{B-High} = 1.50 - 0.85 = 0.65, \qquad \text{S-Low} - \text{B-Low} = 0.30 - 0.45 = -0.15.
$$
A "size effect" measured only in the value column ($+0.65$) and one measured only in the growth column
($-0.15$) point in *opposite directions* and differ by $0.80$. Picking either single column would give a
size factor badly contaminated by *where in the value spectrum you happened to look*; averaging over all
three value buckets (which gives $\text{SMB} = 0.25$, between the extremes) is precisely how FF avoid
letting an arbitrary column choice masquerade as the size premium.

---

## Problem 2 — Read a single time-series factor regression (20 pts)

Given fit: $\hat\alpha_i = 0.04$, $\hat b_i = 1.00$, $\hat s_i = 0.80$, $\hat h_i = 0.40$, $R^2 = 0.94$,
$t(\hat\alpha_i) = 0.6$.

**(a)** [4 pts] **The specification (Conventions §4 form).**
- **Outcome:** the small-value test portfolio's monthly **excess return**, $R_{it} - R_{ft}$.
- **Regressors (key, no controls):** the three factor returns — market excess return $R_{Mt} - R_{ft}$,
  $\text{SMB}_t$, $\text{HML}_t$.
- **No fixed effects, no clustering:** this is plain time-series OLS (Ch 2.1) on one portfolio's stream
  of $T$ monthly observations.
- **Sample:** the monthly time series over the full study window (FF93: July 1963 – December 1991,
  ~342 months).
- **The question it answers:** *when this portfolio's excess return moves month to month, how much of
  that movement is shared with the three factors (the loadings and $R^2$), and is there any average
  return left over once the factor exposures are accounted for (the intercept)?*

**(b)** [5 pts] **The $R^2$ reading — common variation.** $R^2 = 0.94$ says the three factors explain
**94% of the month-to-month variance of this portfolio's excess return**; only 6% is idiosyncratic
residual $\varepsilon_{it}$. The right phrase is **"common variation,"** not merely "fit," because the
factors are themselves portfolios that *many* stocks move with — so a high $R^2$ certifies that the bulk
of this portfolio's wiggle is the *shared, non-diversifiable* part of returns that the factors capture,
exactly the "common risk factors" of the paper's title. A *low* $R^2$ here would have been damning: it
would say that whatever moves this portfolio month to month is mostly *not* the market, size, or value —
i.e., SMB and HML would have failed to be genuine common sources of co-movement, and the model would
have missed the very variation it claims to describe.

**(c)** [6 pts] **The loadings reading.**
- $\hat b_i = 1.00$ tracks the **market factor**: the portfolio moves roughly one-for-one with the
  market excess return. Sensible — equity portfolios have market betas near one.
- $\hat s_i = 0.80$ tracks the **size factor (SMB)**: a strong *positive* loading. This portfolio is a
  *small*-cap portfolio, so it should co-move strongly and positively with "small stocks did well this
  month" — a big-cap portfolio would load near zero or negative. The positive sign **makes sense** and
  is exactly the orderliness FF93 look for: loadings that march with the sort.
- $\hat h_i = 0.40$ tracks the **value factor (HML)**: a positive loading. This is a *value* portfolio
  (high BE/ME), so it should load positively on "value did well this month"; a growth portfolio would
  load negative. Sign and direction **make sense**.

All three signs are what you'd predict from the portfolio's place in the sort — the model is
"recognizing" the characteristics the portfolio was sorted on. That is what people mean when they say the
loadings "make sense."

**(d)** [5 pts] **The intercept reading — pricing error.** The intercept $\hat\alpha_i = 0.04\%$/month is
the **average excess return left over after the three factors have done their work** — the part of the
portfolio's mean return that its factor *exposures* do not account for. It is called the **pricing
error** because if the three factors are the complete description of priced risk, a portfolio's average
return should be fully earned through its loadings, leaving nothing over; $\hat\alpha_i = 0$ would assert
exactly that — *the model prices this portfolio with no leftover*. Here $\hat\alpha_i = 0.04$ is
**economically tiny** (four hundredths of a percent per month) and, with $t(\hat\alpha_i) = 0.6 < 2$,
**statistically indistinguishable from zero** — we cannot reject that the true pricing error is zero. The
**two-column rule (Ch 5.2 §4):** *high $R^2$ (near 1) plus $\alpha$ near 0 together certify a working
factor model* — the factors capture both the **common variation** (the $R^2$) and the **average level**
(the zero $\alpha$). This portfolio passes both.

---

## Problem 3 — CAPM vs FF3 on the same portfolio (16 pts)

Inputs: $\mathbb{E}[R_M - R_f] = 0.50$, $\mathbb{E}[\text{SMB}] = 0.25$, $\mathbb{E}[\text{HML}] = 0.40$
(%/month); average excess return $\overline{R_i - R_f} = 0.90$; FF3 loadings $\hat b_i = 1.00,
\hat s_i = 0.80, \hat h_i = 0.40$; CAPM loading $\hat b_i^{\text{CAPM}} = 1.10$.

**(a)** [5 pts] **CAPM pricing error.**
$$
\text{predicted}^{\text{CAPM}} = \hat b_i^{\text{CAPM}}\cdot\mathbb{E}[R_M - R_f] = 1.10 \times 0.50 = 0.55,
$$
$$
\boxed{\alpha_i^{\text{CAPM}} = \overline{R_i - R_f} - 0.55 = 0.90 - 0.55 = 0.35.}
$$
CAPM explains only $0.55$ of the $0.90$ average excess return; a large $\alpha_i^{\text{CAPM}} = 0.35\%$/
month is left on the table as a pricing error — money CAPM cannot explain.

**(b)** [5 pts] **FF3 pricing error.** Predicted, term by term:
$$
\hat b_i\,\mathbb{E}[R_M - R_f] = 1.00 \times 0.50 = 0.50,
$$
$$
\hat s_i\,\mathbb{E}[\text{SMB}] = 0.80 \times 0.25 = 0.20,
$$
$$
\hat h_i\,\mathbb{E}[\text{HML}] = 0.40 \times 0.40 = 0.16,
$$
$$
\text{predicted}^{\text{FF3}} = 0.50 + 0.20 + 0.16 = 0.86,
$$
$$
\boxed{\alpha_i^{\text{FF3}} = 0.90 - 0.86 = 0.04.}
$$
This **matches the $\hat\alpha_i = 0.04$ given in Problem 2** — the intercept of the time-series
regression *is* the average return minus the loading-weighted factor premia. ✓

**(c)** [4 pts] **Side by side:** $\alpha_i^{\text{CAPM}} = 0.35$ vs. $\alpha_i^{\text{FF3}} = 0.04$.
CAPM leaves a large unexplained chunk; FF3 leaves almost nothing. The two pieces FF3 added to the
predicted return are the **size premium contribution** $\hat s_i\,\mathbb{E}[\text{SMB}] = 0.20$ and the
**value premium contribution** $\hat h_i\,\mathbb{E}[\text{HML}] = 0.16$ — together $0.36$, which is
almost exactly the $0.35$ that CAPM had left unexplained. A small-value portfolio is *precisely* the
asset CAPM mis-prices: it earns a high average return that its market beta alone cannot justify (the
FF92/FF93 finding), and that "excess" is exactly what its strong *positive* loadings on the size and
value factors capture — so FF3 converts CAPM's pricing error into earned factor premia.

**(d)** [2 pts] The $R^2$ increase from CAPM to FF3 speaks to **common variation**, not pricing — it
says the two new factors explain more of the portfolio's month-to-month *variance*. That is logically
**separate** from the shrinkage in $\alpha$ (which is about the *average level*): a factor could lift
$R^2$ (co-move with the portfolio) while carrying no premium and so not shrink $\alpha$ at all, or carry
a premium that shrinks $\alpha$ while explaining little co-movement. FF3 happens to do **both** here,
which is why it is a genuinely better model and not just a better fit.

---

## Problem 4 — The GRS joint test (16 pts)

**(a)** [5 pts] **The null hypothesis.** GRS tests
$$
H_0: \ \alpha_1 = \alpha_2 = \cdots = \alpha_{25} = 0,
$$
i.e., **all 25 test-portfolio intercepts are simultaneously zero**. In words: *the three-factor model
prices every one of the 25 portfolios with no leftover — there is no portfolio whose average return the
factor loadings fail to explain.* This is the formal version of the two-column rule's second column: GRS
is the precise statement of "**the entire $\alpha$ column is zero**," asked as one question about all 25
intercepts at once.

**(b)** [5 pts] **Why joint, not 25 separate $t$-tests.** Two reasons.

*Multiple testing (Ch 1.5, the Week 1 problem).* If you run 25 separate $t$-tests at the 5% level and
ask whether *any* rejects, the chance that **at least one** crosses the bar by pure luck — even if the
true model is perfect and every $\alpha_i = 0$ — is far above 5%. With 25 independent tests it is about
$1 - 0.95^{25} \approx 0.72$: you'd expect to see a "significant" pricing error roughly 72% of the time
even when the model is exactly right. Scanning $t$-stats and declaring victory (or defeat) on the loudest
one inflates the **family-wise error rate** and is exactly the data-snooping mistake the joint test
avoids.

*Correlated residuals.* The 25 portfolios hold **overlapping stocks**, so their regression residuals are
**correlated** and the $\hat\alpha_i$ are *not* independent. A naive procedure that treated the 25
intercepts as independent would mis-state the joint significance — it would mis-count how much
*independent* evidence the 25 numbers really carry. The GRS $F$-statistic builds in the full residual
covariance matrix, so it asks the right joint question with the right standard error.

**(c)** [4 pts] **The decision rule.** GRS yields one $F$-statistic; **a model "passes" the asset-pricing
bar when GRS *fails to reject* $H_0$** — i.e., when the pricing errors are jointly indistinguishable from
zero. This is the **opposite** of the usual treatment-effect mindset, where you *hope to reject* a null
of "no effect." Here the model *is* the null (zero pricing errors), so the researcher is rooting **for**
the null — a non-rejection is the win. A **rejection** of the GRS null would say the intercepts are
jointly nonzero: the model leaves systematic, statistically real pricing errors somewhere in the 25
portfolios — it is *not* a complete description of priced risk.

**(d)** [2 pts] The stubborn corner is **small-growth** (the small-cap, low-BE/ME cell). Its
persistently nonzero (typically negative) intercept is the three-factor model's most resistant pricing
error: it signals either a *tolerable blemish* on an otherwise excellent model, or a symptom that a
**fourth factor** (profitability, investment, or momentum) is missing — the tension FF93 honest readers
flag without fully resolving.

---

## Problem 5 — What's vulnerable (18 pts)

**(a)** [6 pts] **Risk or mispricing.** The time-series machinery measures only **co-movement** ($R^2$)
and **leftover average return** ($\alpha$); it is silent on *why* the premium exists. A high $R^2$ and a
zero $\alpha$ are **equally consistent** with "HML is compensation for bearing a genuine risk (distress,
say) that pays off in bad states" and with "HML captures a systematic *behavioral mistake* — investors
over-extrapolate glamour growth and under-price beaten-down value, and the premium is the correction."
Both stories predict the same regression output: value stocks co-move (a real factor exists) and earn a
premium (a nonzero loading times a positive factor mean). The regression cannot peer inside the premium
to see whether it is a risk price or a mistake. **One piece of evidence pushing toward risk:** show that
HML pays off *badly in bad states* — that value stocks crash precisely in recessions or distress, when an
investor's marginal utility is high — which is what makes them genuinely risky and would justify
compensation; alternatively, an **out-of-sample / out-of-country replication** (the premium recurs in
markets and periods the original search never saw) is harder to square with a one-time behavioral
artifact.

**(b)** [6 pts] **The factor zoo and multiple testing.** Each candidate characteristic is one hypothesis
test (is its long-short alpha nonzero?). Under the multiple-testing logic of Ch 1.5, if you test $m$
characteristics at the 5% level and the truth is that *none* is a real factor, you still expect about
$0.05\,m$ of them to clear the bar by **pure chance** — test 200, expect ~10 spurious "factors." Reporting
only the winners of a large search is therefore a **data-snooping** trap: the significance you see is
manufactured by the number of tries, not by the data. **Retrospective worry about FF93 itself:** were
size and value *found by searching* over many candidate sorts, and would they survive a multiple-testing
correction applied to the *whole* search that produced them? **The honest counter-argument:** SMB and HML
have held up far better **out-of-sample and across countries and decades** than the typical zoo entry —
durable replication in data the original search never touched is real evidence they are not pure flukes,
even though the *method* is a data-snooping machine if used undisciplined.

**(c)** [4 pts] **Look-ahead in factor construction.** The lag — fiscal year-end accounting from year
$y{-}1$ matched to returns from July of year $y$ — guards against **look-ahead bias**: without it you
would be sorting June-of-$y$ portfolios on a book-equity number that was *not yet public*, implicitly
assuming the investor knew the firm's accounts before they were filed, which no real-time investor could.
The specific Compustat feature that can sneak the bias back in is **backfilling**: historically Compustat
added data for firms only *after* they had become established and successful, so the early sample is
tilted toward survivors and their good outcomes are "known" in a way they were not in real time. A sloppy
lag would manufacture a value premium **no real-time investor could ever have earned** — an artifact of
hindsight, not a tradeable return.

**(d)** [2 pts] **Threat → guard, one per vulnerability:**
1. *Risk vs. mispricing* → seek **identifying evidence on the economics** (recession-state pattern in
   HML; link to firm fundamentals; out-of-sample/out-of-country replication) rather than reading cause
   off the regression.
2. *Factor zoo / multiple testing* → apply a **multiple-testing correction** (e.g., a higher $t$-stat
   hurdle) and demand **out-of-sample replication** before believing a new factor.
3. *Look-ahead / backfill* → impose the **correct reporting lag** and use a **point-in-time** data
   snapshot, and check robustness by varying the lag.

---

## Problem 6 — Replication design for nb5.2 (12 pts)

**(a)** [4 pts] **Data and access.** FF93's stock side uses **CRSP** (Center for Research in Security
Prices) for returns and market caps, and **Compustat** annual files for book equity — both
**licensed** (they stay on GMU infrastructure, read-only on Hopper/WRDS Cloud). The fact that makes this
replication unusually accessible: **Ken French hosts the official monthly factor returns (market, SMB,
HML) and the 25 size × BE/ME portfolios free and public** on his data library — no license needed. You
would use those free series as a **check** by **correlating your hand-built monthly SMB and HML against
French's official SMB and HML, month by month**, expecting correlations **comfortably above 0.9** (not a
perfect 1.0, because data vintages and exact construction details differ); a badly diverging month is a
flag to diagnose.

**(b)** [4 pts] **The two-column table.** One row per test portfolio, columns:
**$\hat b$ · $\hat s$ · $\hat h$** (the loadings), **$\hat\alpha$ with its $t$-statistic** (the pricing
error), and **$R^2$**. The three qualitative facts to verify:
1. **$R^2$ column:** high across the board (factors capture the **common variation** of every
   portfolio).
2. **Loadings:** they **march monotonically with the sort** — $\hat s$ rises as you go from big to small
   portfolios; $\hat h$ rises as you go from growth to value.
3. **Intercepts:** **economically small and mostly insignificant** — with **small-growth** the cell to
   watch as the visible exception (its $\hat\alpha$ is the stubborn one).

**(c)** [4 pts] **A robustness check.** Change **one** construction choice — e.g., swap **NYSE
breakpoints for all-stock breakpoints** (which loads the small portfolios with thousands of micro-caps),
or **value-weighting for equal-weighting** (which lets tiny stocks drive the result). Re-form the six
corner portfolios, **re-compute SMB and HML, re-run the 25 regressions for the loadings, and recompute
the GRS statistic.** A **robust** finding barely moves — the premia and the GRS verdict survive a cut at
30% vs. 33% or NYSE vs. all-stock; a **fragile** one swings materially, telling you "the" size and value
premia are really "the premia *under these specific rules*" (the §6 critique turned into a measured
number). This is the kind of sensitivity check a referee will demand of your own capstone.

---

*End of solutions for Problem Set 5.2. The arithmetic spine, verified: from the illustrative 2×3 grid,
$\text{SMB} = 0.91\overline{6} - 0.66\overline{6} = 0.25$ and $\text{HML} = 1.175 - 0.375 = 0.80$
(Problem 1); the small-value test portfolio's CAPM alpha is $0.90 - 1.10(0.50) = 0.35$ but its FF3 alpha
collapses to $0.90 - (0.50 + 0.20 + 0.16) = 0.04$ (Problem 3), the size and value contributions ($0.20 +
0.16 = 0.36$) absorbing almost exactly CAPM's $0.35$ pricing error. The conceptual spine: read every
factor regression two ways — $R^2$ for common variation, $\alpha$ for pricing — test the intercepts
**jointly** with GRS (not 25 separate $t$-tests), and hold the humility that the machinery describes
co-movement beautifully while staying silent on whether the premia are risk or mistake. Citation by name:
Fama & French (1993); Gibbons, Ross & Shanken (1989).*
