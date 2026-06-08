# Capstone 5 — FRED Macro Event Study

> **ASSIP framing — read first.** *The ASSIP 2026 terminal deliverable is a research poster
> (~48"×36") + a JSSR abstract (200–300 words) + an 8-minute poster talk + a replication packet
> — not a full paper.* This exemplar is the **full research narrative the poster summarizes**: a
> complete macro-announcement event-study paper written one level above the ASSIP graded artifact,
> so that you can see what the full event-study scaffolding (surprise extraction, HAC standard
> errors, placebo dates, split-sample checks) looks like end to end before you compress it onto
> six poster panels and a 10-sentence JSSR abstract. The poster's design panel shows the
> identifying-assumption sentence ("the surprise component is orthogonal to the announcement-day
> equity return absent the news"); the robustness panel shows the placebo distribution; the
> contribution panel says "an announcement-day association, not a clean causal effect."
>
> **EXEMPLAR PAPER — READ THIS FIRST.** This is a *worked example* of the Capstone 5 deliverable, written in the voice of the cast member **Sam** so you can see what a finished macro-announcement event study looks like end to end. **Every number in it is synthetic: announcement dates, surprise components, and returns were constructed for instruction and are not empirical findings.** Do not cite any figure here as a fact about the world; cite it only as a demonstration of *form*. Where a real submission would carry a verified citation, unverified references are tagged `[CHECK]` exactly as CONVENTIONS §6 and Appendix D.5.4 require. Your own capstone replaces the synthetic block with a real reproducible pull (Lab 7 discipline) and re-runs the pipeline.

---

## Do FOMC Surprises Move the Market? An Event Study of the S&P 500 Reaction to Monetary-Policy Announcements

**Sam [Student Author], ASSIP 2026 (Aspiring Scientists Summer Internship Program)** · Mentor: Prof. Lei Gao · Conference draft

### Abstract

When the Federal Open Market Committee (FOMC) announces a rate decision, the stock market reacts within minutes — but to *what*, exactly? The level of the new rate is largely known in advance, so any clean reaction should load on the **surprise**: the gap between the decision and what markets had already priced. This paper estimates the daily return reaction of a broad U.S. equity index to scheduled FOMC announcements over **2010–2024**, separating the expected component of each decision from its surprise using a market-implied policy-rate measure. On a sample of **120 scheduled meetings** (synthetic; see the data note), a regression of the announcement-day index return on the monetary surprise yields a slope of **−4.8** (index return in percent per percentage-point surprise), precisely estimated under heteroskedasticity-and-autocorrelation-consistent (HAC, Newey–West) standard errors and statistically distinguishable from zero, while the *level* of the new rate carries no separately identified reaction. A one-day event window, placebo dates drawn from non-announcement days, and split-sample checks across the 2010–2019 and 2020–2024 sub-periods all leave the surprise coefficient stable in sign and order of magnitude. We read the estimate as the *announcement-day association* between monetary surprises and equity returns under a tightly defended timing assumption — consistent with, but not a clean causal measurement of, the price impact of monetary news, because same-day macro releases and the endogeneity of the surprise itself remain live threats we cannot fully close.

---

### 1. Introduction

On the afternoon of a scheduled FOMC meeting, trading desks do not wait for the Chair to finish speaking. The decision is released at 2:00 p.m. Eastern, and within the first minute the S&P 500 can move more than it does on a typical full day. Yet the *number* in the release — the new target range for the federal funds rate — is rarely a surprise: by the morning of the meeting, futures markets have usually assigned better than even odds to the outcome that actually arrives. If the level were what moved prices, the market would have moved days earlier, when the expectation formed. What is left to react to on the day is the **surprise**: the piece of the decision the market had *not* already priced. This is the central insight of the monetary-announcement literature, and it is the one this paper is built to exploit.

**Contribution.** This paper provides a transparent, properly-inferred estimate of the announcement-day relationship between the *surprise component* of FOMC rate decisions and the daily return on a broad U.S. equity index, decomposing each decision into an expected part and a surprise part and showing that the market reaction loads on the surprise and not on the rate level. The contribution is not a new fact about monetary policy — the sign and rough magnitude here echo decades of work — but a clean, reproducible *worked demonstration* of how to run such an event study with honest standard errors and a stated identifying assumption, at a level a strong high-school empiricist can execute end to end.

**What we find.** On the synthetic sample, the announcement-day index return falls by about **4.8 percentage points per one-percentage-point hawkish (higher-than-expected) surprise**, an estimate that is stable across event-window lengths, survives placebo dates that carry no announcement, and holds in both halves of the sample. The *level* of the new rate, entered alongside the surprise, carries no separately identified reaction — exactly the pattern the "markets price the expected, react to the surprise" view predicts.

**Roadmap.** Section 2 positions the paper in the monetary-surprise and event-study literatures. Section 3 describes the FRED series, the announcement dates, the surprise construction, and the return data. Section 4 lays out the event-study design, states the identifying assumption in one sentence, and tables the threats to it. Section 5 leads with the headline regression and reads it. Section 6 is the robustness section, organized around the threats. Section 7 concludes with the honest limits.

---

### 2. Positioning in the literature

The methodological backbone is the **event-study** framework, the standard tool for measuring how a discrete, dated piece of information moves asset prices. Its canonical statements are MacKinlay (1997), "Event Studies in Economics and Finance," *Journal of Economic Literature* 35(1):13–39, and the textbook treatment in Campbell, Lo & MacKinlay (1997), *The Econometrics of Financial Markets* (Princeton University Press), which formalize the abnormal-return calculation and the inference around an event window. The event-study logic is older than finance's use of it — Fama, Fisher, Jensen & Roll (1969), "The Adjustment of Stock Prices to New Information," *International Economic Review* 10(1):1–21, is the founding application — but MacKinlay is the reference a referee expects to see for the design.

The substantive literature is the study of **monetary-policy surprises**. The pivotal move — measuring the surprise from the change in fed funds *futures* prices in a tight window around the announcement, rather than from the rate decision itself — is Kuttner (2001), "Monetary Policy Surprises and Interest Rates: Evidence from the Fed Funds Futures Market," *Journal of Monetary Economics* 47(3):523–544. Kuttner's insight is the one this paper rests on: the market reacts to the surprise, and the surprise is identified from the price of an instrument that was already pricing the expectation. Bernanke & Kuttner (2005), "What Explains the Stock Market's Reaction to Federal Reserve Policy?", *Journal of Finance* 60(3):1221–1257, applied exactly this decomposition to equity returns and found that an unexpected 25-basis-point easing is associated with a roughly one-percent rise in broad indices — the direct ancestor of the regression in this paper. The high-frequency identification literature that followed — Gürkaynak, Sack & Swanson (2005), "Do Actions Speak Louder Than Words? The Response of Asset Prices to Monetary Policy Actions and Statements," *International Journal of Central Banking* 1(1):55–93, and Nakamura & Steinsson (2018), "High-Frequency Identification of Monetary Non-Neutrality: The Information Effect," *Quarterly Journal of Economics* 133(3):1283–1330 — tightened the window to thirty minutes around the release and surfaced the *information effect* (a surprise can move the economy's outlook, not just its discount rate), which is the deepest threat to the clean reading and one Section 7 returns to.

This paper sits at the intersection: it borrows MacKinlay's event-study scaffolding and Kuttner's surprise decomposition, applies them to a daily equity index at a level a beginner can reproduce from free data, and — following the inference discipline of Week 2 — reports HAC standard errors of the kind Newey & West (1987), "A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix," *Econometrica* 55(3):703–708, made standard. It does not claim the daily window of Nakamura–Steinsson precision; it claims the daily window of a free-data classroom replication, and it is honest about the gap.

---

### 3. Data

> **Synthetic-data note.** The announcement dates, surprise values, and returns below were *constructed for instruction* to reproduce the qualitative shape of the literature (a negative surprise–return slope of plausible magnitude, with realistic noise). They are **not** real market or policy data. A real submission would replace this section with a reproducible pull per the Lab 7 / Chapter 7.2 discipline — pinned, cached to `data/raw/`, logged in `logs/pulls.jsonl` with a content hash — and would cite the underlying agencies, not "FRED."

The study joins three pieces on a common spine, the **announcement date**.

**The policy series (FRED).** The realized policy stance comes from the effective federal funds rate, FRED series `DFF` (daily) and `FEDFUNDS` (monthly average), produced by the **Board of Governors of the Federal Reserve System** and redistributed through FRED. For the *expected* rate we use a market-implied measure — in the synthetic build, a constructed analogue of the fed funds futures-implied rate the morning of each meeting; a real build would use the CME fed funds futures or the 30-day futures-implied path, and would pull a point-in-time value so the expectation is the one that *existed before* the announcement, not a revised series (the look-ahead trap the FRED data card flags). Following the FRED card's discipline, any revisable macro series used as a control (e.g. the most recent CPI print, `CPIAUCSL`, from the **Bureau of Labor Statistics**) is taken as an **ALFRED vintage** — its value *as reported on the event date* — never the latest revised number, because a revised CPI is data that did not exist when the market traded.

**The announcement dates (FOMC).** The event dates are the **scheduled FOMC decision days**, of which there are eight per year, published by the Federal Reserve Board (the FOMC-text data card). We use the *decision date* — the day the statement is released, when the market actually learns the outcome — and deliberately exclude the *minutes-release* date three weeks later, which is new information on its own day and would be a separate event with its own timing. Confusing the two is the look-ahead bug the data card warns about; pinning the decision date is the fix. The synthetic sample covers **120 scheduled meetings, 2010-01-01 through 2024-12-31**; unscheduled intermeeting actions (e.g. emergency cuts) are excluded because their timing is itself endogenous to market stress, which would contaminate the design.

**The surprise.** For each meeting $t$ we define the **monetary surprise** as the realized policy change minus the expected change implied by the futures price the morning of the meeting:

$$
\text{Surprise}_t \;=\; \Delta r_t^{\text{realized}} \;-\; \mathbb{E}_{t^-}\!\left[\Delta r_t\right],
$$

where $\Delta r_t^{\text{realized}}$ is the change in the target rate announced at $t$ and $\mathbb{E}_{t^-}[\Delta r_t]$ is the market-implied expected change just *before* the release. A positive surprise is *hawkish* (the Fed was tighter than expected); a negative surprise is *dovish*. This is the Kuttner (2001) decomposition. The expected component, by construction, is the part of the decision the market already knew, so a clean reaction should load on the surprise and not on the level.

**The returns (free market data).** The outcome is the daily close-to-close return on a broad U.S. equity index proxy (in the synthetic build, a constructed series mimicking the S&P 500 total-return index; a real build would pull a free index ETF such as `SPY` via `yfinance`, or an index level, and compute the simple daily return). Returns are in **percent** so the table shows readable magnitudes (per Appendix D.1 §4). The announcement-day return is aligned to the decision date; because the 2:00 p.m. release falls inside the trading day, the close-to-close return on the decision date captures the post-announcement move plus a few hours of pre-announcement drift — a measurement issue we address with the event-window robustness in Section 6.

**Table 1 — Variable definitions and sources (synthetic sample).**

| Variable | Definition | Frequency | Source (cite the factory, not FRED) |
|---|---|---|---|
| $r^{\text{mkt}}_t$ | Daily close-to-close index return, percent | Daily | Free index/ETF (synthetic proxy) |
| $\text{Surprise}_t$ | Realized minus expected rate change, pp | Per meeting | Fed (`DFF`) + futures-implied expectation |
| $\Delta r_t^{\text{realized}}$ | Announced change in target rate, pp | Per meeting | Board of Governors (FRED `DFF`) |
| Level$_t$ | New target rate after the decision, pp | Per meeting | Board of Governors (FRED `DFF`) |
| CPI surprise$_t$ | Same-day CPI print minus consensus (control) | Monthly (ALFRED vintage) | Bureau of Labor Statistics (`CPIAUCSL`) |

*Notes.* Sample: 120 scheduled FOMC meetings, 2010–2024 (synthetic). The decision date is the event date; minutes-release dates and unscheduled actions are excluded. Revisable macro controls are taken as ALFRED point-in-time vintages to avoid look-ahead.

---

### 4. Empirical design

**The estimating equation.** The headline specification regresses the announcement-day index return on the monetary surprise, with the rate *level* entered alongside it to test the literature's prediction that the level carries no separately identified reaction:

$$
r^{\text{mkt}}_t \;=\; \beta_0 \;+\; \beta_1\,\text{Surprise}_t \;+\; \beta_2\,\text{Level}_t \;+\; \varepsilon_t,
\qquad t \in \{\text{scheduled FOMC days}\}.
$$

The coefficient of interest is $\beta_1$, the index return per percentage-point surprise; the "markets price the expected, react to the surprise" view predicts $\beta_1 \neq 0$ (negative: a hawkish surprise depresses equities) and $\beta_2 \approx 0$. In CONVENTIONS §4 form: the **outcome** is the announcement-day index return; the **key regressor** is the monetary surprise; the **controls** are the rate level and (in robustness) the same-day CPI surprise; there are **no fixed effects** (the sample is a single time series of events, not a panel); inference uses **HAC (Newey–West) standard errors**; the **sample** is the 120 scheduled meetings, 2010–2024.

**The identifying assumption, in one sentence.** *The timing of a scheduled FOMC announcement is fixed years in advance and exogenous to that day's idiosyncratic equity shock, so the announcement-day return — net of the expected component already priced — reflects the market's reaction to the monetary surprise rather than to whatever else would have moved the market that day.* The two clauses each do work. The *fixed-in-advance timing* is what makes the event date exogenous: the FOMC does not schedule its meeting for a day it expects the market to be calm or turbulent, so the date itself is "as good as random" with respect to the day's other news. The *expected-vs-surprise decomposition* is what isolates the news: by subtracting the priced-in expectation, $\text{Surprise}_t$ strips out the part of the decision the market already knew, leaving the component that can actually move prices on the day.

**Why HAC, and why it recalls Week 2.** The events are spaced about six weeks apart, but the residuals are not guaranteed independent: clustered macro regimes (a tightening cycle, a crisis) can induce serial correlation in announcement-day returns, and announcement-day volatility is itself heteroskedastic. Classical OLS standard errors assume neither problem exists and, as Week 2 (Ch 2.4) drilled, deliver *t*-statistics that are too large when they do — the same disease as un-clustered panel SEs, in a time-series guise. The fix is the **heteroskedasticity-and-autocorrelation-consistent** estimator of Newey & West (1987): it widens the standard errors to absorb both, at a lag length chosen to span the plausible window of dependence. We report Newey–West SEs at a lag of 3 (meetings) as the headline and sweep the lag in robustness. Reporting classical SEs here would be the time-series analogue of the Bertrand–Duflo–Mullainathan mistake, and a referee would catch it in one line of the note.

**Threats to identification.** The design is clean only if the announcement-day move is the surprise's doing. Three threats stand between the regression and that reading; we name each, give the concrete story under which it bites, state what we do about it, and keep the honest residual.

**Table 2 — Threats and responses.**

| Threat | Why it's plausible here | What we do about it | Residual concern |
|---|---|---|---|
| **Confounding same-day news** | The morning of an FOMC day often carries other macro releases (a CPI or jobs print) that move the index independently of the policy surprise. | Control for the same-day CPI surprise (§6); restrict to meetings with no major same-day release as a subsample. | A control cannot absorb *every* same-day shock; the tightest fix (intraday windows) is beyond free daily data. |
| **Expected-vs-surprise mismeasurement** | If the futures-implied expectation is measured with error, $\text{Surprise}_t$ contains part of the *expected* change, biasing $\beta_1$ toward zero (classical measurement-error attenuation, Ch 2.5). | Use the morning-of futures-implied rate, point-in-time; show the level coefficient $\beta_2$ is near zero, evidence the decomposition is doing its job. | Attenuation means our $|\beta_1|$ is a *lower bound*; the true reaction may be larger. |
| **Overlapping / mis-timed windows & serial dependence** | A longer event window can overlap the next event or a regime shift; announcement-day residuals may be serially correlated and heteroskedastic. | One-day window as primary; HAC (Newey–West) SEs; sweep the window length and the HAC lag (§6). | HAC corrects inference, not bias; a genuinely overlapping window still mixes two events. |
| **Endogeneity of the surprise (information effect)** | A "surprise" may reveal the Fed's private read of the economy, so the equity move reflects revised growth expectations, not the policy shock alone (Nakamura–Steinsson 2018). | Acknowledged; decomposition isolates *a* surprise but cannot separate the policy-rate channel from the information channel with daily data. | This is the deepest residual and caps the causal language (§7). |

The fourth threat is the reason the abstract and conclusion stop at *association under a timing assumption* rather than *causal effect*: the daily window cannot separate the two channels, and honesty about the verb (Appendix D.5.1) requires saying so.

---

### 5. Results

The table leads; read it before the prose. It builds left to right from the parsimonious surprise-only regression to the specification that adds the rate level and the same-day CPI control, exactly the parsimonious-to-saturated discipline of Appendix D.2 §4.

**Table 3 — Announcement-day index return and the monetary surprise (synthetic).**

| | (1) Surprise only | (2) + Rate level | (3) + CPI surprise |
|---|---:|---:|---:|
| **Monetary surprise (pp)** | −4.82\*\*\* | −4.79\*\*\* | −4.71\*\*\* |
| | (0.91) | (0.93) | (0.95) |
| **Rate level (pp)** | | −0.04 | −0.05 |
| | | (0.08) | (0.08) |
| **CPI surprise (pp)** | | | −1.12\* |
| | | | (0.61) |
| **Constant** | 0.06 | 0.11 | 0.10 |
| | (0.07) | (0.14) | (0.14) |
| HAC (Newey–West, 3 lags) | Yes | Yes | Yes |
| $R^2$ | 0.21 | 0.21 | 0.23 |
| $N$ (meetings) | 120 | 120 | 120 |

*Notes.* **Synthetic data — illustrative, not empirical findings.** The dependent variable is the announcement-day close-to-close return on a broad U.S. equity index proxy, in percent. The monetary surprise is the realized minus market-expected rate change, in percentage points (Kuttner 2001 decomposition); positive = hawkish. Sample: 120 scheduled FOMC meetings, 2010–2024; decision dates only. No fixed effects (single time series of events). Standard errors are heteroskedasticity-and-autocorrelation-consistent (Newey–West, 3 lags) in parentheses. \*\*\* $p<0.01$, \*\* $p<0.05$, \* $p<0.10$.

The headline is column (1): a one-percentage-point *hawkish* surprise is associated with a **4.8-percentage-point lower** announcement-day index return, with a HAC standard error of 0.91, so $t \approx -5.3$ and the estimate is comfortably distinguishable from zero. The sign is the one the literature predicts — tighter-than-expected money depresses equities — and the magnitude is in the neighborhood of Bernanke & Kuttner (2005) once you account for the synthetic scaling (their roughly one-percent index move per 25-basis-point surprise implies a per-percentage-point slope of order four, the same ballpark). A word on economic size, kept separate from the stars (Appendix D.1 §3): a *typical* FOMC surprise is small — a few basis points, or a few hundredths of a percentage point — so the *typical* announcement-day move attributable to the surprise is a fraction of a percent, not five percent. The 4.8 is the *slope*, the reaction to a hypothetical full-point surprise; the realized surprises are tiny, which is exactly why the market is usually quiet on FOMC days and occasionally violent on the rare day the Fed blindsides it.

Column (2) adds the rate level, and it is the decomposition's test: the level coefficient is **−0.04 with a standard error of 0.08** — indistinguishable from zero — while the surprise coefficient is essentially unchanged at −4.79. This is the predicted pattern. The market does not react to *where the rate is*; it reacts to *how the decision differed from what was priced*. A reader worried that the surprise is just proxying for the level can see from this column that it is not: hold the surprise fixed and the level moves the market not at all. Column (3) adds the same-day CPI surprise; it enters negative and marginally significant (a hot inflation print depresses equities, plausibly), the surprise coefficient barely moves (−4.71), and $N$ holds at 120 across all three columns, so the build-up is clean and no silent sample change is doing the work (Appendix D.2 §3).

---

### 6. Robustness

The robustness section is organized around the threats table (§4), one check per named threat, in descending order of danger, following Appendix D.3. For each check we state what a *pass* looks like before reporting the result.

**Confounding same-day news (Threat 1).** A reader might worry that the announcement-day return reflects a same-day macro release rather than the policy surprise. We already control for the same-day CPI surprise in Table 3 column (3); we additionally re-estimate column (1) on the subsample of meetings with *no* major same-day release. A pass is a surprise coefficient stable in sign and magnitude. The subsample slope is **−4.6 (HAC SE 1.1)** on the reduced sample — slightly attenuated, well within sampling noise of the full-sample −4.8, and still firmly negative. The residual stands: daily data cannot rule out *every* same-day shock, only the ones we can name and measure.

**Event-window length (Threat 3).** A reader might worry that the one-day window mistimes the reaction — too short if the move bleeds into the next day, too long if it overlaps the next event. We sweep the cumulative-return window from the announcement day alone to a symmetric three-day window around it. A pass is a slope that is stable and does not balloon as the window widens (ballooning would signal contamination from adjacent days).

**Table 4 — Surprise coefficient across event windows (synthetic).**

| Event window | $\hat\beta_1$ | HAC SE | $N$ |
|---|---:|---:|---:|
| Day 0 only (primary) | −4.82\*\*\* | 0.91 | 120 |
| Days [0, +1] | −5.05\*\*\* | 1.02 | 120 |
| Days [−1, +1] | −4.93\*\*\* | 1.14 | 120 |
| Days [0, +2] | −5.21\*\*\* | 1.27 | 120 |

*Notes.* **Synthetic.** Dependent variable is the cumulative index return over the stated window, in percent. Newey–West (3 lags) SEs. \*\*\* $p<0.01$. The slope is stable; the modest growth from −4.82 to −5.21 as the window widens is consistent with a small amount of next-day drift, not contamination, and the standard error grows as the window admits more unrelated variance.

The slope is stable across windows, drifting only modestly upward as the window lengthens — consistent with a little post-announcement continuation, not with a window picking up an adjacent event. We additionally sweep the **HAC lag** from 1 to 6 meetings; the point estimate is invariant (HAC changes only the SE, not $\hat\beta$, by construction) and the standard error rises gently from 0.84 (1 lag) to 0.98 (6 lags), leaving the estimate significant throughout. Pass.

**Placebo dates (Threat 1/3, inference validity).** A reader might worry that the surprise–return relationship is an artifact of the regression rather than the announcement. The sharpest test assigns *fake* announcement dates: we draw 120 random non-FOMC trading days, assign each the surprise value from a randomly matched real meeting, and re-estimate. The design's prediction is unambiguous — **on placebo dates, the surprise should carry no information, so $\hat\beta_1$ should be indistinguishable from zero.** Across 1,000 such placebo permutations the mean placebo slope is **−0.07 with 95% of draws falling in [−1.8, +1.7]**, a distribution centered on zero that comfortably contains it, while the true announcement-day slope of −4.82 sits far in the left tail (a permutation *p*-value below 0.001). This is the asymmetric-but-real support the design needs: the relationship appears on announcement days and vanishes on days carrying no announcement, which is what makes the timing assumption credible rather than decorative.

**Sub-period stability (general robustness).** A reader might worry the estimate is driven by one regime — say, the zero-lower-bound 2010s or the 2022 tightening cycle. We split the sample at 2020 and re-estimate. A pass is the same sign and order of magnitude in both halves.

**Table 5 — Sub-period split (synthetic).**

| Sub-period | $\hat\beta_1$ | HAC SE | $N$ |
|---|---:|---:|---:|
| 2010–2019 | −4.51\*\*\* | 1.18 | 80 |
| 2020–2024 | −5.34\*\*\* | 1.39 | 40 |

*Notes.* **Synthetic.** Surprise-only specification (Table 3 col. 1) on each sub-period. Newey–West (3 lags). \*\*\* $p<0.01$. The slope is somewhat steeper in the later, higher-volatility period, but the two confidence intervals overlap substantially, so we do not read the difference as a regime change in the reaction.

Both halves deliver a negative, significant slope; the later period is steeper, plausibly because announcement-day volatility was higher after 2020, but the intervals overlap and we do not over-interpret the gap.

**Robustness is not identification.** Every check above tells us the *number* is not an artifact of an arbitrary window, lag, sub-sample, or the regression itself — the placebo in particular is real support for the *timing* assumption. None of them closes the **information-effect** threat (Threat 4): a stable, placebo-passing slope is still consistent with the surprise moving equities partly through revised growth expectations rather than the policy rate alone. Robustness asks whether the number moves when we change the analysis; identification asks whether the design measures what we claim. The checks pass the first question; the second is settled by the design, not the robustness battery, and our design leaves the information channel open — which is exactly why the verbs in this paper stop at "associated with."

---

### 7. Conclusion

This paper asked a narrow, answerable question: when the FOMC announces a rate decision, does the equity market react to the *surprise* — the part it had not already priced — rather than to the level of the new rate? On a synthetic sample built to the shape of the literature, the answer is a clean yes: a one-percentage-point hawkish surprise is associated with a roughly 4.8-percentage-point lower announcement-day index return, the rate level carries no separately identified reaction, and the estimate is stable across event windows, HAC lags, sub-periods, and a placebo that correctly finds nothing on non-announcement days. The pattern is the one Kuttner (2001) and Bernanke & Kuttner (2005) documented and the inference is the HAC inference Week 2 demanded.

**Honest limits.** The estimate is an *announcement-day association under a timing assumption*, not a clean causal measurement, and three limits keep it there. First, the **information effect**: a surprise can reveal the Fed's private outlook, so part of the equity reaction may be revised growth expectations rather than the monetary shock, and daily data cannot separate the two channels — the deepest residual concern, and the one that caps the causal language (Nakamura–Steinsson 2018). Second, **measurement error in the surprise**: if the market-expected rate is measured imperfectly, classical attenuation pushes $|\hat\beta_1|$ toward zero, so the true reaction may be *larger* than 4.8, not smaller. Third, **the daily window**: the high-frequency literature isolates the reaction in a thirty-minute window precisely because the trading day admits other news, and a free-data daily study cannot match that precision; our same-day CPI control and no-release subsample bound the contamination but do not eliminate it. A real version of this study would tighten the window with intraday prices, instrument the surprise with the futures change in a narrow band, and test the information channel directly — and would replace every synthetic number here with a reproducible pull. What the exemplar shows is the *form*: a dated event, an expected-vs-surprise decomposition, a stated identifying assumption, HAC inference, a placebo, and verbs that promise exactly what the design can pay.

---

### References

- Bernanke, B. S., & Kuttner, K. N. (2005). What explains the stock market's reaction to Federal Reserve policy? *Journal of Finance*, 60(3), 1221–1257.
- Campbell, J. Y., Lo, A. W., & MacKinlay, A. C. (1997). *The Econometrics of Financial Markets*. Princeton University Press.
- Fama, E. F., Fisher, L., Jensen, M. C., & Roll, R. (1969). The adjustment of stock prices to new information. *International Economic Review*, 10(1), 1–21.
- Gürkaynak, R. S., Sack, B., & Swanson, E. T. (2005). Do actions speak louder than words? The response of asset prices to monetary policy actions and statements. *International Journal of Central Banking*, 1(1), 55–93.
- Kuttner, K. N. (2001). Monetary policy surprises and interest rates: Evidence from the Fed funds futures market. *Journal of Monetary Economics*, 47(3), 523–544.
- MacKinlay, A. C. (1997). Event studies in economics and finance. *Journal of Economic Literature*, 35(1), 13–39.
- Nakamura, E., & Steinsson, J. (2018). High-frequency identification of monetary non-neutrality: The information effect. *Quarterly Journal of Economics*, 133(3), 1283–1330.
- Newey, W. K., & West, K. D. (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. *Econometrica*, 55(3), 703–708.

*Citation status: all eight references above have been verified against the journal listings (Bernanke–Kuttner *JF* 60(3) 1221–1257; Kuttner *JME* 47(3) 523–544; Nakamura–Steinsson *QJE* 133(3) 1283–1330; MacKinlay *JEL* 35(1) 13–39; Gürkaynak–Sack–Swanson *IJCB* 1(1) 55–93; Newey–West *Econometrica* 55(3) 703–708; Fama–Fisher–Jensen–Roll *IER* 10(1) 1–21; Campbell–Lo–MacKinlay 1997 Princeton UP). Any future change to a citation should be re-verified before submission, per CONVENTIONS §6.*

---
---

## Margin commentary — "How this paper was built"

*An annotated walkthrough for the student, written outside the paper. The paper above is the deliverable; this is the scaffolding behind it — the design choices, the order they were made in, and the places where the standard could have slipped. Read it as a checklist you can run on your own capstone.*

**Why start from the question, not the data.** The paper exists to answer one sentence: *does the market react to the surprise, not the level?* That question was fixed before any number was generated, which is what kept the analysis honest. The temptation in an event study is to pull the data first, notice a pattern, and write the question to fit it — the garden of forking paths (Week 1 §1.5, Week 7 §7.3). Writing the question first means the headline regression in Table 3 is the *confirmatory* spec, and everything in Section 6 is a check *around* it, not a fishing expedition that produced it.

**The contribution sentence is calibrated, on purpose.** Section 1's contribution sentence says the paper "provides a transparent, properly-inferred estimate of the announcement-day relationship" — not "shows that surprises cause market moves." The verb is "estimate the relationship," not "measure the effect," because the design is an event study on observational data with a live information-effect threat, and Appendix D.5.1's lookup table caps an observational design at "is associated with." Every verb attached to the headline number, from the abstract to the conclusion, was audited against that ceiling (D.5.1's verb-audit). The single place the paper allows itself confidence — "the level carries no separately identified reaction" — is a *null* result about a control, where confidence is cheap and earned.

**Why the surprise decomposition is the whole game.** The single most important design choice is subtracting the expected rate change. Without it, $\text{Surprise}_t$ would be the raw decision, which is mostly anticipated, and the regression would mostly measure noise — the market having already moved when the expectation formed. Kuttner's (2001) insight, borrowed wholesale, is that the futures market hands you the expectation for free, so the surprise is identifiable. The level coefficient in Table 3 column (2) is there precisely to *show the decomposition worked*: a near-zero level coefficient is the evidence that the surprise is not just proxying for where rates are. This is the "show, don't assert" move — the reader sees the decomposition validated in the table rather than taking the author's word.

**The identifying assumption was written before the results.** Section 4 states the timing assumption in one sentence and unpacks its two clauses (fixed-in-advance timing → exogenous date; expected-vs-surprise → isolated news). This is the CONVENTIONS §4 requirement, and stating it *before* Section 5 is deliberate: the assumption is the promise the results section must not exceed. When the conclusion stops at "association under a timing assumption," it is honoring the promise made here, not retreating from a stronger claim made earlier.

**Why HAC, and the Week 2 callback.** The standard-error choice is not cosmetic. Announcement-day returns can be serially correlated (regimes) and heteroskedastic (some FOMC days are wild), and classical SEs assume neither — the time-series cousin of the un-clustered-panel disease Week 2 (Ch 2.4) and Petersen (2009) made infamous. Newey–West HAC widens the SEs to absorb both. The note on every table names the flavor and the lag ("Newey–West, 3 lags"), which is the load-bearing disclosure of Appendix D.1 §6; a table that said only "robust SEs" would lose points no matter how good the prose.

**The threats table did double duty.** The four-row Table 2 was written during design (Section 4) and then *cashed out* row by row in Section 6, in the same order, descending by danger (Appendix D.3 §1). Each robustness subsection opens with the "a reader might worry… we… and…" move, names the threat specifically (never "endogeneity"), and states the pass criterion before the result. The residual-concern column is never blank — every row keeps an honest leftover, because a threats table with no residuals reads as an author who did not look hard (D.3 §2).

**The placebo is the paper's spine.** Of all the checks, the placebo on fake announcement dates is the one that most defends the *timing* assumption: if the surprise–return relationship showed up on random non-FOMC days, the whole event-study premise would collapse. Stating the no-effect prediction *first* ("on placebo dates $\hat\beta_1$ should be indistinguishable from zero") removes the freedom to reinterpret a bad result after the fact (D.3 §3). Reporting the permutation *p*-value puts a number on "far in the tail."

**Table craft, concretely.** Every table follows Appendix D: the key coefficient (surprise) on top in every column; the level shown because it is *interpretable* (it tests the decomposition), not sprayed; the constant shown but unstarred; $N = 120$ on every column so the reader sees the sample never silently changed; columns built parsimonious → saturated; and a complete note carrying dependent variable, units, sample, SE flavor and lag, and the star legend. There are no fixed-effect rows because the design is a single time series of events, not a panel — and the note says so, rather than leaving the reader to wonder why the usual FE switches are absent.

**The synthetic label is everywhere it needs to be.** Per the brief and CONVENTIONS, the data are flagged synthetic at the top, in the data note, and in every table's note. This is not throat-clearing: a reader who lifted the −4.8 as a real estimate would be misled, so the label rides along with every number. In your real capstone, this block is replaced by a reproducible-pull paragraph — pinned ALFRED vintages for revisable series, decision dates pinned (not minutes dates), cached and logged — and the synthetic warnings come out.

**The honest-limits paragraph is the most important paragraph.** Section 7's limits are not a ritual apology; they are where the residual-concern column finally speaks in prose (D.5.5). The information effect caps the causal verb; measurement-error attenuation tells the reader the estimate is a *lower bound* on the magnitude; the daily window names what a better study would do. A conclusion that declared the question settled would undo the calibrated honesty of the eleven sections above it in one sentence — the drift D.5.2 warns about. The paper ends one notch below where a careless author would, which is exactly where the design can pay.
