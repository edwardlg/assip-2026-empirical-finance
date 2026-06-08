# Problem Set 5.2 — FF93 Factor Construction & Time-Series Regressions

**Covers Chapter 5.2 (Reader's Guide: Fama & French (1993)).** This set is a *replication-flavored*
walk through the machinery of Fama and French (1993), "Common Risk Factors in the Returns on Stocks and
Bonds." Methods through Ch 5.2 only: the **2×3 size × book-to-market sort** and the six value-weighted
corner portfolios; the construction of the size factor **SMB ("small minus big")** and the value factor
**HML ("high minus low")** from those six portfolios; the **time-series factor regression** of a test
portfolio's excess return on the three factors,
$$
R_{it} - R_{ft} = \alpha_i + b_i\,(R_{Mt} - R_{ft}) + s_i\,\text{SMB}_t + h_i\,\text{HML}_t + \varepsilon_{it},
$$
read **two ways** — the $R^2$ for *common variation* and the intercept $\alpha_i$ for *pricing error*;
the **CAPM-vs-FF3 comparison**; and the **GRS joint test** (Gibbons, Ross & Shanken 1989) of the null
that all test-portfolio intercepts are simultaneously zero. Notation follows the Conventions: $R_{it}$
is portfolio $i$'s gross return in month $t$, $R_{ft}$ the risk-free rate, $R_{Mt} - R_{ft}$ the market
excess return; $b_i, s_i, h_i$ are factor **loadings** and $\hat\alpha_i$ the **pricing error**.

Six problems, escalating, **100 points total**. Every numerical input is supplied so you can work the
arithmetic by hand — no computer needed. The companion notebook **nb5.2** (`notebooks/week-05/
nb5.2-ff93-factor-regressions.ipynb`) lets you check the construction and the regressions on data, and
the official Fama–French factors used there are **free and public** — Ken French has hosted them for
decades, so this is one replication you can do with no licensed CRSP/Compustat access at all.

**The grading rule of this set:** a number reported *without saying what it means* — an $R^2$ without
the words "common variation," an $\alpha$ without the words "pricing error," a loading without naming
which characteristic it tracks — earns half credit at most. As everywhere in this book, the *reading*
of the regression is the skill, not the arithmetic. Whenever you name a vulnerability, name the design
choice or test that addresses it (spec discipline, Conventions §4).

> **A standing warning on numbers.** Every figure in this problem set is **illustrative** — invented to
> make the arithmetic clean and the reasoning visible. **They are not the numbers in Fama and French's
> tables.** Do not quote them as if they were. The *qualitative* facts (positive SMB/HML premia, high
> $R^2$s on the test portfolios, small intercepts, small-growth as the weak spot) are well established
> and safe to state; any precise coefficient belongs in your own replication in nb5.2, not in
> memory.

Several problems share one small world, defined once here so you can carry the numbers between them.

> **The illustrative six-portfolio month (the working world).** At the end of June, all stocks are
> split into **two size groups** (Small / Big, at the NYSE-median market-cap breakpoint) and
> independently into **three book-to-market groups** (Low / Medium / High BE/ME, at the NYSE 30th and
> 70th percentiles). Intersecting gives **six value-weighted portfolios**. Here are their **excess
> returns in one illustrative month** (percent per month — invented, clean):

| | Low BE/ME (growth) | Medium BE/ME | High BE/ME (value) |
|:---|:---:|:---:|:---:|
| **Small** | S-Low $= 0.30$ | S-Med $= 0.95$ | S-High $= 1.50$ |
| **Big**   | B-Low $= 0.45$ | B-Med $= 0.70$ | B-High $= 0.85$ |

> Read the grid the FF way before you compute anything: down each column (Small to Big) the size effect
> says small should out-earn big; across each row (Low to High BE/ME) the value effect says value
> should out-earn growth. Both patterns are visible in this single illustrative month. The factor
> formulas (Ch 5.2 §2) are
> $$
> \text{SMB} = \tfrac{1}{3}\big(\text{S-Low}+\text{S-Med}+\text{S-High}\big) - \tfrac{1}{3}\big(\text{B-Low}+\text{B-Med}+\text{B-High}\big),
> $$
> $$
> \text{HML} = \tfrac{1}{2}\big(\text{S-High}+\text{B-High}\big) - \tfrac{1}{2}\big(\text{S-Low}+\text{B-Low}\big).
> $$

---

## Problem 1 — Construct SMB and HML by hand from the 2×3 sort (18 points)

This is the factory floor. Build the two factors from the six corner portfolios and see *why* the
construction is shaped the way it is.

**(a)** [6 pts] Using the working-world grid, compute **SMB** for this month. Show the average of the
three small portfolios, the average of the three big portfolios, and the difference. Then state in one
sentence what SMB *is*, in plain words — what bet does an investor holding SMB hold?

**(b)** [6 pts] Compute **HML** for this month. Show the average of the two high-BE/ME portfolios, the
average of the two low-BE/ME portfolios, and the difference. State in one sentence what HML *is* as a
bet.

**(c)** [4 pts] The construction averages *across* the other characteristic before differencing — SMB
averages over the three value buckets before differencing small minus big; HML averages over the two
size buckets before differencing value minus growth. Explain in two or three sentences why this
averaging is deliberate: what would go wrong if, instead, you built a "size factor" as just S-High
minus B-High (small-value minus big-value)? Use the words "neutral" and "contaminate," and connect the
idea to Frisch–Waugh–Lovell (Ch 2.3) — partialling one effect out to isolate the other.

**(d)** [2 pts] Compute the *naive* size bet S-High $-$ B-High and the *naive* size bet S-Low $-$ B-Low
from the grid. Note that they disagree (one is much bigger than the other). State in one sentence what
this disagreement illustrates about why FF average over the value dimension rather than picking a single
column.

---

## Problem 2 — Set up and read a single time-series factor regression (20 points)

Now move from constructing factors to *using* them. One test portfolio, one regression, read three ways.

A researcher forms a **small-value** test portfolio (it is *not* one of the six factor-ingredient
portfolios — keep that distinction sharp; the six build the factors, the test portfolios are the
patients the model must cure) and runs, over $T$ months,
$$
R_{it} - R_{ft} = \alpha_i + b_i\,(R_{Mt} - R_{ft}) + s_i\,\text{SMB}_t + h_i\,\text{HML}_t + \varepsilon_{it}.
$$
The fitted results are (illustrative):
$$
\hat\alpha_i = 0.04,\quad \hat b_i = 1.00,\quad \hat s_i = 0.80,\quad \hat h_i = 0.40,\quad R^2 = 0.94,
$$
with the intercept's $t$-statistic $t(\hat\alpha_i) = 0.6$.

**(a)** [4 pts] Write down the full empirical specification in the Conventions §4 form: name the
**outcome**, the **regressors**, the **sample**, and state in one sentence the question the regression
answers. (No fixed effects or clustering here — this is plain time-series OLS, Ch 2.1, on one
portfolio's monthly stream.)

**(b)** [5 pts] **The $R^2$ reading — common variation.** Interpret $R^2 = 0.94$ in the specific
language of this paper. What fraction of *what* does it describe, and why is the phrase "common
variation" — as opposed to just "fit" — the right one? In one sentence, say what a *low* $R^2$ here
would have told you about whether SMB and HML are genuine common factors.

**(c)** [6 pts] **The loadings reading.** Interpret $\hat b_i, \hat s_i, \hat h_i$. For each, say which
characteristic it tracks and whether its sign and magnitude *make sense* for a small-value portfolio.
(Hint: think about how $\hat s_i$ should look for a *small* portfolio versus a big one, and how
$\hat h_i$ should look for a *value* portfolio versus a growth one — the loadings should march with the
sort.)

**(d)** [5 pts] **The intercept reading — pricing error.** Interpret $\hat\alpha_i = 0.04$ with
$t(\hat\alpha_i) = 0.6$. What does the intercept *mean* in an asset-pricing time-series regression — why
is it called the pricing error, and what would $\hat\alpha_i = 0$ assert about the model? Is this
portfolio's pricing error economically and statistically distinguishable from zero? State the
**two-column rule** from Ch 5.2 (§4) in one sentence: what does high $R^2$ *plus* zero $\alpha$ together
certify?

---

## Problem 3 — CAPM vs FF3 on the same portfolio (16 points)

The whole point of FF93 is that adding SMB and HML *prices* portfolios that CAPM cannot. Make that
concrete with the same small-value portfolio.

Take the long-run average premia (illustrative, percent per month):
$$
\mathbb{E}[R_M - R_f] = 0.50,\qquad \mathbb{E}[\text{SMB}] = 0.25,\qquad \mathbb{E}[\text{HML}] = 0.40,
$$
and suppose the portfolio's **average excess return** over the sample is $\overline{R_i - R_f} = 0.90$.
The FF3 loadings are the Problem-2 values $\hat b_i = 1.00, \hat s_i = 0.80, \hat h_i = 0.40$. A
**CAPM-only** regression of the same portfolio gives a market loading $\hat b_i^{\text{CAPM}} = 1.10$.

**(a)** [5 pts] **CAPM pricing error.** Under CAPM, the model-predicted average excess return is
$\hat b_i^{\text{CAPM}}\cdot\mathbb{E}[R_M - R_f]$. Compute it, then compute the CAPM alpha
$\alpha_i^{\text{CAPM}} = \overline{R_i - R_f} - \hat b_i^{\text{CAPM}}\cdot\mathbb{E}[R_M - R_f]$.
Report the number.

**(b)** [5 pts] **FF3 pricing error.** Under FF3, the predicted average excess return is
$\hat b_i\,\mathbb{E}[R_M - R_f] + \hat s_i\,\mathbb{E}[\text{SMB}] + \hat h_i\,\mathbb{E}[\text{HML}]$.
Compute it term by term, then compute the FF3 alpha
$\alpha_i^{\text{FF3}} = \overline{R_i - R_f} - (\text{predicted})$. Report the number, and confirm it
matches the $\hat\alpha_i = 0.04$ given in Problem 2.

**(c)** [4 pts] Lay $\alpha_i^{\text{CAPM}}$ and $\alpha_i^{\text{FF3}}$ side by side. CAPM leaves a
large unexplained chunk of the average return; FF3 leaves almost nothing. State, in two sentences,
*which two pieces* SMB and HML added to the predicted return, and why a small-value portfolio in
particular is exactly the kind of asset CAPM mis-prices and FF3 rescues.

**(d)** [2 pts] In a replication you would also see the $R^2$ rise from the CAPM regression to the FF3
regression on this portfolio. Say in one sentence which of the two readings — common variation or
pricing — that $R^2$ increase speaks to, and why a rise in $R^2$ is logically *separate* from the
shrinkage in $\alpha$ (you can have one without the other).

---

## Problem 4 — The GRS joint test: what it tests and why joint (16 points)

A single portfolio's intercept is one number with one $t$-statistic. FF93's real test asks about *all*
the test portfolios at once. This problem pins down the GRS test (Gibbons, Ross & Shanken 1989) — we use
it, we do not derive it.

A researcher runs the three-factor regression on each of the **25** size × BE/ME test portfolios (a 5×5
sort), obtaining 25 intercepts $\hat\alpha_1, \dots, \hat\alpha_{25}$ and their $t$-statistics.

**(a)** [5 pts] State the **null hypothesis** the GRS test evaluates, symbolically and in words. What
single English sentence about the model is true if and only if this null holds? (Tie it back to the
two-column rule: GRS is the formal version of "the $\alpha$ column is zero.")

**(b)** [5 pts] **Why joint, not 25 separate $t$-tests?** Explain in three or four sentences why you
**cannot** simply scan the 25 individual $t$-statistics and declare victory if most are insignificant.
Name the Week 1 problem this is (Ch 1.5), and state what would go wrong with the family-wise error rate
if you ran 25 tests at the 5% level and asked whether *any* rejected. Then add the second reason the
test must be joint: the 25 portfolios' residuals are **correlated** (they hold overlapping stocks), so
the intercepts are *not* independent — and say in one sentence why a procedure that ignored that
correlation would mis-state the joint significance.

**(c)** [4 pts] The GRS statistic is a single $F$-statistic. State the decision rule in asset-pricing
terms: **a model "passes" when GRS *fails to reject*** the joint null. Explain why that is the opposite
of the usual "we hope to reject the null" mindset from a treatment-effect regression — i.e., here the
researcher is rooting *for* the null. In one sentence, say what a *rejection* of the GRS null would tell
you about the model.

**(d)** [2 pts] FF93's three-factor model dramatically out-performs CAPM on the GRS test, but the joint
test is not always a clean pass — one corner of the 5×5 grid is the stubborn culprit. Name that corner
portfolio and state in one sentence what its persistently nonzero intercept signals (a tolerable blemish
vs. a missing factor — you need not resolve the debate, just name the cell and the tension).

---

## Problem 5 — What's vulnerable: risk vs. mispricing, the factor zoo, look-ahead (18 points)

A model this influential invites hard questions. This problem is pure reasoning — it tests whether you
can push on FF93 the way a referee would, using the vocabulary of Weeks 1 and 2.

**(a)** [6 pts] **Risk or mispricing?** FF93 frames SMB and HML as compensation for *risk*; a rival camp
reads the premia as the correction of *mispricing* (investors over-pay for glamour growth firms,
under-pay beaten-down value firms). Explain in three or four sentences why the time-series regression
machinery — high $R^2$, zero $\alpha$ — **cannot distinguish** these two stories. Then name *one* piece
of additional evidence that would push you toward the risk reading (Hint: think about when HML pays off —
is it in good states or bad states of the world? — or about an out-of-sample / out-of-country
replication).

**(b)** [6 pts] **The factor zoo and multiple testing.** The FF93 recipe — sort on a characteristic,
build a long-short portfolio, check the alpha — has since been run on *hundreds* of candidate
characteristics, producing the "factor zoo." Explain, using the Week 1 multiple-testing problem
(Ch 1.5), why reporting only the characteristics with significant alphas out of a large search is a
**data-snooping** trap: what happens to the number of "significant" factors you expect to find by pure
chance as the number of characteristics tested grows? Then state the retrospective worry this raises
about FF93 *itself*, and give the one honest counter-argument in its favor (Hint: out-of-sample and
out-of-country behavior).

**(c)** [4 pts] **Look-ahead in factor construction.** FF93 matches accounting data from fiscal year-end
in calendar year $y{-}1$ to returns from July of year $y$ onward — a deliberate **lag**. Explain in two
or three sentences what bias this lag is guarding against (what would you be assuming the investor knew,
and when, if you skipped it?), and name the specific Compustat feature — historical **backfilling** of
data for firms only after they became established — that can sneak the bias back in even when you think
you have lagged correctly. State in one clause what a sloppy lag would manufacture: a premium *no
real-time investor could have earned*.

**(d)** [2 pts] For *each* of the three vulnerabilities above, name in a phrase the discipline or check
that a careful replicator uses to address it (one per vulnerability). This is spec discipline
(Conventions §4) pointed at a factor model: name the threat, then name the guard.

---

## Problem 6 — Replication design: from this problem set to nb5.2 (12 points)

You will run this for real in nb5.2. This problem makes you design the replication *before* you touch
the keyboard — stating the spec, the data, and the checks you would commit to in advance.

**(a)** [4 pts] **Data and access.** Name the two data sources FF93 uses for the stock side (one for
returns and market caps, one for book equity), and state which is licensed and which is free. Then state
the key fact that makes this replication unusually accessible for a high-school camp: Ken French hosts
the official monthly factor returns and the 25 portfolios **free and public**. Explain in one sentence
how you would use those free series as a *check* on factors you built yourself (what would you correlate
with what, and roughly how high should the correlation be?).

**(b)** [4 pts] **The two-column table.** Sketch the table you would produce from the 25 time-series
regressions: name the columns (loadings $\hat b, \hat s, \hat h$; intercept $\hat\alpha$ with its $t$;
and $R^2$) and state the **three qualitative facts** you would verify reading it — one about the $R^2$
column, one about how the loadings should move across the sort, and one about the intercepts (including
which cell to watch). This is the §4 reading order turned into a deliverable.

**(c)** [4 pts] **A sensitivity / robustness check.** FF93's factors depend on *construction choices* —
the 2×3 cut, NYSE breakpoints, value-weighting, the 30/70 cutoffs, the June rebalance. Design one
concrete robustness check: name *one* construction choice you would change (e.g., NYSE breakpoints →
all-stock breakpoints, or value-weighting → equal-weighting), state what you would re-compute after the
change (SMB, HML, the loadings, the GRS statistic), and state in one sentence what a *robust* finding
would look like versus a *fragile* one. Tie this to the §6 critique: "the" size and value premia are
really "the premia *under these specific rules*."

---

*End of Problem Set 5.2. Solutions: Appendix E, `E-w5-ps5.2-solutions.md`. The companion notebook
**nb5.2** (`notebooks/week-05/nb5.2-ff93-factor-regressions.ipynb`) lets you build the six 2×3
portfolios and the factors, run the 25 time-series regressions and assemble the two-column $R^2$/$\alpha$
table, contrast CAPM with FF3, and compute the GRS statistic for both — checking your hand arithmetic
from Problems 1–4 against real, free Ken French data, with a "Your Turn" extension that bolts a momentum
factor onto the model. The single discipline to carry forward: a working factor model is **high $R^2$
(common variation) plus zero $\alpha$ (no pricing error), tested jointly** — and even the best one,
FF93, leaves the small-growth corner unhealed.*
