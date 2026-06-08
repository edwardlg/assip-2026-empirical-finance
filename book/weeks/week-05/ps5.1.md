# PS 5.1 — Sorting, Double-Sorting, and the Fama–MacBeth Horse Race in Fama & French (1992)

**Course:** ASSIP 2026 · 8-Week Empirical Finance Track · Week 5 · Problem Set 5.1
**Covers:** Ch 5.1 (Reader's Guide: *The Cross-Section of Expected Stock Returns*, Fama & French 1992), read through the fixed **Reader's-Guide anatomy** — the seven sections *Research question · Identification strategy · Data · Table-by-table reading order · What's clever · What's vulnerable · Three replication exercises*. You will be asked to name which section a question lives in, so keep the anatomy at your elbow.

**Methods allowed:** only what Week 5's reading and the labs behind it have given you — **portfolio sorts** (univariate decile sorts; the $5\times5$ or $3\times3$ double sort to disentangle two characteristics nonparametrically); reading a **return spread** off a sort table (high bucket minus low bucket) and calling it a *premium*; the **Fama–MacBeth two-pass machine of Lab 2** (Pass 1: time-series betas; Pass 2: a cross-sectional regression *each month* of returns on characteristics, giving a time series of slopes $\hat\gamma_{j,t}$) with the FM point estimate $\hat\gamma_j=\frac1T\sum_t\hat\gamma_{j,t}$ and the honest FM standard error $\widehat{\operatorname{se}}(\hat\gamma_j)=\operatorname{sd}_t(\hat\gamma_{j,t})/\sqrt T$; the descriptive/predictive (not causal) reading of an asset-pricing study from §2; the Week-1 **multiple-testing / data-snooping** problem $P(\text{at least one false ``discovery''})=1-(1-\alpha)^m$; the Week-2/3 **errors-in-variables → attenuation** result (a regressor measured with random noise has its slope biased toward zero); and **look-ahead** / **survivorship** bias in merged accounting–return data. You do **not** need the 1993 three-factor model (that is Ch 5.2), nor any matrix-algebra derivation of the FM estimator.

**Total: 100 points.** Point values are stated per problem. Show your reasoning — a correct final number with no derivation earns roughly half credit, because reading the logic *is* the skill we are grading. Solutions are in Appendix E (`E-w5-ps5.1-solutions.md`); attempt every part before you look.

**A note on the numbers.** Fama and French's actual table values are *not* reproduced here. Every figure in this sheet is **illustrative and constructed** — built to behave like the paper's so you can practice the moves, never quoted as the paper's own. When the problem set says "Sam computes," the numbers are Sam's synthetic panel (the seeded fallback in `nb5.1`), not CRSP/Compustat. Cite the paper by name: **Fama & French (1992)**.

**The difficulty curve.** Problem 1 is a conceptual warm-up — why sort at all? Problem 2 puts the decile-sort arithmetic in your fingers. Problem 3 is the disentangling problem, the cleverest move in the paper and the one most students misread. Problem 4 hands you Fama–MacBeth output and asks you to read it the way §4 taught. Problem 5 is the referee's attack — three named vulnerabilities, each tied to a prior week. Problem 6 asks you to *design* the replication pipeline that becomes `nb5.1`, in words, no code. We stay with **Sam**, who walked into Week 2 believing "riskier stocks pay more" and built the Fama–MacBeth machine to test it; this sheet is the autopsy on that belief.

---

## Problem 1 — Why sort? Portfolios versus individual stocks (12 points)

Before any number, the genre. Sam's first instinct is to skip the sorts entirely and regress every individual stock's monthly return on its own characteristics in one giant pooled regression. Ch 5.1 §2 ("Identification strategy") says the paper does something else first: it forms **portfolios** and looks at average returns bucket by bucket.

**(a) (4 pts)** A single small stock's monthly return is wildly volatile — month to month it can swing by tens of percent for reasons specific to that one firm (a lawsuit, a product recall, a single earnings surprise). Explain, in terms of the **variance of an average**, why sorting a few hundred stocks into a portfolio and tracking the *portfolio's* mean return produces a far less noisy object than tracking any one stock — and why that noise reduction is what lets a real premium of, say, under one percent per month become *visible* against the churn. (You may invoke the fact that averaging $n$ roughly-independent pieces shrinks the idiosyncratic variance by about $1/n$.)

**(b) (4 pts)** Sorts are described in §2 as **nonparametric** — "they impose no linear functional form." State precisely what a univariate decile sort assumes about the shape of the return–characteristic relationship versus what the single pooled regression $\mathbb{E}[r_{it}]=\gamma_0+\gamma_1\,x_i$ assumes. Then give one concrete way the sort can *reveal a shape the linear regression would hide* — for instance, what the decile means could look like if the premium lived almost entirely in the extreme bucket.

**(c) (4 pts)** Name the Reader's-Guide anatomy section that tells you to read the **sort tables before the regression tables**, and restate, in one sentence, the §4 reason that ordering is the experienced reader's habit. Then connect this to Sam's plan: why is it a mistake for Sam to lead with the kitchen-sink regression and treat the sorts as an afterthought?

---

## Problem 2 — Read a univariate decile sort and lift the premium off it (16 points)

Sam runs the gentlest replication (Exercise 1 of §7) on his synthetic panel. He ranks firms into **size deciles** each year — D1 the smallest firms, D10 the largest — forms the ten portfolios, and computes each decile's average monthly return over the sample. Separately he does the same on **book-to-market (BE/ME) deciles** — B1 the lowest BE/ME ("growth"), B10 the highest ("value"). His two tables of average monthly returns (in percent per month, **illustrative constructed numbers**):

**Size sort**

| Decile | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 |
|:------:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| Mean ret (%/mo) | 1.62 | 1.48 | 1.39 | 1.31 | 1.24 | 1.18 | 1.10 | 1.02 | 0.93 | 0.78 |

**BE/ME sort**

| Decile | B1 | B2 | B3 | B4 | B5 | B6 | B7 | B8 | B9 | B10 |
|:------:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| Mean ret (%/mo) | 0.72 | 0.86 | 0.97 | 1.08 | 1.17 | 1.25 | 1.36 | 1.49 | 1.67 | 1.95 |

**(a) (5 pts)** Compute the **size premium** as the spread between the extreme deciles — be explicit about which decile you subtract from which, and *why that sign convention* (which is the "small" end?). Report it in %/mo and then as a rough annualized figure (multiply by 12). Do the same for the **value premium** from the BE/ME table. State in one sentence each which §4 pattern these reproduce ("two live patterns").

**(b) (4 pts)** Look at the *monotonicity* of each column, not just the endpoints. State whether each sort is monotone (returns moving the same direction at every step) and explain why a referee finds a **smooth monotone** sort more convincing than one where only the extreme bucket is unusual. Which of the two characteristics shows the steeper *and* cleaner gradient in Sam's numbers?

**(c) (4 pts)** Sam now does the §7 "break it on purpose" exercise: he re-sorts on size using **contemporaneous** market equity (this month's price $\times$ shares) instead of the properly **lagged** value, and the size spread *widens* dramatically. Explain the mechanism: why does sorting on a within-month price that is *part of* the return being measured manufacture a spread that is not a real premium? Name the bias (it is one of the four §6 vulnerabilities), and connect it to the July-to-June timing gap §3 builds in to prevent exactly this.

**(d) (3 pts)** Sam reports the size spread as a single number, "0.84 %/mo," with no standard error. State in one sentence why a spread between two portfolio means is not yet evidence until you attach a measure of its sampling variability, and name the object from Lab 2 / §2 that supplies the honest standard error when this premium is re-estimated as a regression slope. (You are *not* asked to compute it.)

---

## Problem 3 — The double sort: was beta's premium just size in disguise? (20 points)

This is the cleverest move in the paper (§5, "What's clever") and the one most students misread. In the raw data, **size and beta are correlated** — small firms tend to be high-beta — so a one-way sort on beta is partly a *disguised* sort on size. Sam will see why that wrecks a naive beta test, and how the double sort fixes it.

First, Sam's naive one-way **beta** sort on his synthetic panel. He ranks firms into three beta groups — Low, Mid, High pre-formation beta — and reports each group's average monthly return (%/mo, **illustrative**), together with the size mix of each beta bucket:

| Beta group | Mean ret (%/mo) | % of bucket that is *small* firms | % that is *big* firms |
|:----------:|:---------------:|:--------------------------------:|:---------------------:|
| Low beta   | 1.01 | 10% | 60% |
| Mid beta   | 1.19 | 27% | 27% |
| High beta  | 1.33 | 60% | 10% |

**(a) (5 pts)** Read off the **naive High-minus-Low beta spread** (%/mo). Taken at face value, what would CAPM-believing Sam conclude — does this support his "riskier pays more" prior? Then look at the size-mix columns and state the worry in one precise sentence: what *else*, besides beta, is changing as you move from the Low-beta to the High-beta bucket?

**(b) (7 pts)** Now Sam runs the **double sort**: a $3\times3$ grid sorted on size (rows) *and* pre-formation beta (columns) at once, so each cell holds firms similar in size and spread in beta. Average monthly returns (%/mo, **illustrative**):

|              | Low beta | Mid beta | High beta |
|:------------:|:--------:|:--------:|:---------:|
| **Small**    | 1.50     | 1.53     | 1.49      |
| **Mid**      | 1.18     | 1.21     | 1.17      |
| **Big**      | 0.84     | 0.81     | 0.86      |

(i) For each size *row*, compute the within-size High-minus-Low beta spread. What do these three numbers say about whether beta earns a return premium *once size is held roughly fixed*? Quote the §4 phrase for what you are watching happen.
(ii) For each beta *column*, compute the within-beta Small-minus-Big size spread. What do these say about the size premium *once beta is held roughly fixed*?
(iii) In two sentences, reconcile (a) and (b): how can a one-way beta sort show a $+0.32$ %/mo "premium" while every within-size beta spread is essentially flat? (Your answer must use the size-mix columns from part (a).)

**(c) (5 pts)** Ch 5.1 §5 says the double sort "is the same logic as *controlling for a confounder*, done nonparametrically with buckets instead of a regression slope." Make that mapping explicit: name the confounder, the treatment-like variable, and the outcome, and explain in two or three sentences why forming size–beta cells achieves with buckets what adding a control to a regression achieves with a slope. Then state the one thing the bucket version buys you that the linear control does *not* (hint: §2's word "nonparametric").

**(d) (3 pts)** A classmate objects: "You only used *three* beta groups. With finer beta bins maybe a premium would appear." State the legitimate kernel of this objection (what *can* coarse bins hide?) and the §5 reason the double-sort conclusion is nonetheless robust here — i.e., what about the *flatness across the whole row* makes "finer bins would rescue beta" a strained hope rather than a likely fix.

---

## Problem 4 — Read the Fama–MacBeth horse race (22 points)

Sam reuses his Lab-2 machine (§7 Exercise 3) and runs three Fama–MacBeth specifications on $T=330$ monthly cross-sections. He reports, for each regressor, the FM point estimate $\hat\gamma_j$ (the average of the monthly slopes) and the **FM standard error** $\widehat{\operatorname{se}}(\hat\gamma_j)=\operatorname{sd}_t(\hat\gamma_{j,t})/\sqrt T$. All numbers are **illustrative constructed** monthly-return units (returns in %, characteristics in logs):

| Spec | Regressor | $\hat\gamma_j$ | FM SE | $t=\hat\gamma_j/\widehat{\operatorname{se}}$ |
|:----:|:---------:|:--------------:|:-----:|:--:|
| **A** beta alone        | $\beta$         | $+0.18$ | $0.14$ | ? |
| **B** size & BE/ME      | $\log\text{size}$ | $-0.15$ | $0.035$ | ? |
|                         | $\log\text{BE/ME}$ | $+0.42$ | $0.085$ | ? |
| **C** kitchen sink      | $\beta$         | $-0.02$ | $0.13$ | ? |
|                         | $\log\text{size}$ | $-0.14$ | $0.036$ | ? |
|                         | $\log\text{BE/ME}$ | $+0.40$ | $0.090$ | ? |

**(a) (5 pts)** Fill in all six $t$-statistics (one decimal). State which slopes clear a conventional $|t|>2$ bar and which do not, *in each spec*.

**(b) (5 pts)** Read the **beta row across specs A and C** the way §4's last paragraph instructs ("find the row for the market-beta coefficient, then scan its t-statistic across columns"). Describe in words what happens to beta's slope and $t$ when $\log\text{size}$ and $\log\text{BE/ME}$ enter the regression alongside it. State the headline of the entire paper in one sentence, and explain why "the number that *should* be big under CAPM is the number that isn't" is the finding — i.e., why an *absence* is the result.

**(c) (4 pts)** Read the **size and BE/ME rows**: do they keep their large, significant slopes when beta joins them in the kitchen sink (compare spec B to spec C)? Interpret the *signs* in plain English — what does $\hat\gamma_{\log\text{size}}<0$ say about small versus big firms, and what does $\hat\gamma_{\log\text{BE/ME}}>0$ say about value versus growth? Tie each back to the matching live pattern you found in the Problem 2 sorts.

**(d) (5 pts)** Now the inference machinery, connecting to Lab 2 / Ch 2.4. (i) Explain in two or three sentences *why* the Fama–MacBeth standard error — built from the month-to-month scatter of the slopes, $\operatorname{sd}_t(\hat\gamma_{j,t})/\sqrt T$ — is the honest one here, where a single pooled OLS over all stock-months would report a standard error far too small. (Name the within-month correlation problem from Ch 2.4.) (ii) Sam's $\log\text{BE/ME}$ slope in spec C is $\hat\gamma=0.40$ with FM SE $0.090$; recover the implied **standard deviation of the monthly slopes** $\operatorname{sd}_t(\hat\gamma_{\log\text{BE/ME},t})$ using $T=330$. (Invert the SE formula; one line of arithmetic.)

**(e) (3 pts)** Name the Reader's-Guide section that frames these columns as "a sequence of horse races, not one table," and state in one sentence why staging beta-alone → size-and-BE/ME-alone → all-three-together is more persuasive than reporting only the kitchen-sink column.

---

## Problem 5 — Read like a referee: three named vulnerabilities (20 points)

A referee's job is to attack the paper at its weakest joints (§6, "What's vulnerable"). Each part below is one named vulnerability tied to a prior week. Sam must say *what could be wrong* and *what he would check* — not merely admire the result.

**(a) (7 pts) Data-snooping / multiple testing (Week 1).** Size and BE/ME are the *survivors* of a field-wide search across many candidate return predictors. Suppose the profession quietly tested $m=20$ truly worthless characteristics, each at the $\alpha=0.05$ level on the same data.
&nbsp;&nbsp;(i) Compute the probability that *at least one* of the 20 clears significance by chance alone, using $P=1-(1-\alpha)^m$, and the *expected number* of false "discoveries," $\alpha m$.
&nbsp;&nbsp;(ii) Explain in two sentences why a single reported Fama–MacBeth $t>2$ on BE/ME does *not* by itself rule out that BE/ME is one such lucky winner, and state the §6 skeptical question that would actually settle it ("would size and BE/ME survive in data the authors had never seen?").
&nbsp;&nbsp;(iii) Name the kind of out-of-sample evidence that, per §6, has been *kinder* to BE/ME than to most factors, and say in one sentence why surviving there is the right falsification test.

**(b) (7 pts) Errors-in-variables in beta (Week 2 / Week 3).** Beta is not observed; it is *estimated* in Pass 1, with noise.
&nbsp;&nbsp;(i) State the Week-2 measurement-error result that a skeptic would invoke here, and explain precisely how it could make beta's flat slope a *statistical artifact* rather than a real "beta doesn't matter" — i.e., spell out the direction of the bias and why it points where it does.
&nbsp;&nbsp;(ii) Explain the *fix* Fama and French use to blunt this — assigning betas via **portfolios** rather than individual stocks — and why a portfolio beta is less noisy than an individual-stock beta (one sentence of reasoning about averaging out estimation error).
&nbsp;&nbsp;(iii) Give the §6 "honest reading": why is attenuation a *strained* rescue of beta here, given how close to zero the estimated beta slope is? (Two sentences. The point is not that the objection is wrong to raise — it is the *right* objection — but that the data do not let it carry the day.)

**(c) (6 pts) Look-ahead and survivorship in the book-equity data.** The whole construction rests on merging Compustat book equity to CRSP returns.
&nbsp;&nbsp;(i) Define **survivorship bias** in one sentence and explain how Compustat's *backfilled* historical coverage could distort early-sample book equity in a way that flatters the value premium.
&nbsp;&nbsp;(ii) Define **look-ahead bias** in one sentence and explain why getting the §3 timing gap wrong (matching, say, December book equity to that same December's return) would manufacture predictability that no real-time investor could have exploited.
&nbsp;&nbsp;(iii) Ch 5.1 §6 says the paper is "careful here, but *careful* is a claim to be checked, not assumed." State the one concrete thing in `nb5.1` that *checks* the timing claim rather than trusting it.

---

## Problem 6 — Design the replication pipeline for `nb5.1` (10 points)

You are about to build `nb5.1` (`notebooks/week-05/nb5.1-ff92-portfolio-sorts.ipynb`), the notebook that turns §7's three exercises into your own numbers. Write the **design in words** — the pipeline, the choices, the checks. **No full code**; a few variable names or one-line pseudocode steps are fine, but the deliverable is a clear specification a teammate could implement.

**(a) (4 pts) The sort pipeline.** In ordered steps, describe how to go from a firm-month panel (returns, market equity, book equity) to (i) the univariate size and BE/ME decile sorts of Problem 2 and (ii) the size×BE/ME double sort of §7 Exercise 2. Your steps must say **explicitly** where the **July-to-June timing lag** is applied and *why* — i.e., which variable is lagged relative to which return window, and which §6 bias the lag defends against. (Recall §3: returns from July of year $t$ through June of $t+1$ are matched to accounting data from the fiscal year ending in $t-1$.)

**(b) (4 pts) The Fama–MacBeth pipeline.** Describe the two passes of the §7 Exercise 3 horse race as you would implement them: Pass 1 (what regression, estimated on what window, producing **portfolio-level** pre-formation betas — and why portfolio-level, tying to Problem 5b); Pass 2 (the month-by-month cross-sectional regression, what is collected each month, how the point estimate and the FM standard error are then formed from the collected slopes). Name the three specifications you would run to stage the §4 horse race.

**(c) (2 pts) Reproducibility and data discipline.** Per Conventions §5, real CRSP/Compustat stays read-only on GMU infrastructure. State the two things the notebook must do so it (i) runs end-to-end on a student laptop with no licensed data and (ii) is honest about not fabricating real CRSP/Compustat numbers. (Hint: a seeded synthetic fallback with the same schema; a pinned snapshot date on the Path-A pull.)

---

*End of PS 5.1. When you have attempted everything, check yourself against `book/appendices/E-solutions-manual/E-w5-ps5.1-solutions.md`. The arithmetic in Problems 2, 3, 4, and 5(a) can be confirmed on paper or in a few lines of Python; the sorts, the double sort, and the full Fama–MacBeth horse race come alive in `nb5.1` (`notebooks/week-05/nb5.1-ff92-portfolio-sorts.ipynb`), where you rank firms into deciles, build the size×BE/ME grid honoring the July-to-June timing gap, break the sort on purpose with contemporaneous market equity to watch look-ahead inflate the spread, and run the Lab-2 Fama–MacBeth machine to watch beta's slope collapse while size and BE/ME survive — the moment Fama & French (1992) becomes a number on your own screen.*
