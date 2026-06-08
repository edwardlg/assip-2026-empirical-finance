# Solutions — PS 6.1 (Building the KPSS Patent-Value Measure: Construction, Validation, and Critique)

**Problem set:** `book/weeks/week-06/ps6.1.md` (PS 6.1, Week 6).
**Chapter:** Ch 6.1 — Reader's Guide: *Technological Innovation, Resource Allocation, and Growth* (Kogan, Papanikolaou, Seru & Stoffman 2017), read through the seven-part Reader's-Guide anatomy.

These are full worked solutions, not just answers. Notation follows `CONVENTIONS.md` and locks to Ch 6.1 and the prior weeks it builds on: the **market model** $R_{it}=a_i+b_iR_{mt}+\varepsilon_{it}$ fit on a pre-event **estimation window**; the day-by-day **abnormal return** $AR_{ft_k}=R_{ft_k}-(\hat a_f+\hat b_f R_{mt_k})$; the **cumulative abnormal return** $\text{CAR}=\sum_k AR_{ft_k}$ over the short grant window; the dollar conversion by **market capitalization**; the §2 three-refinement construction (filter the market → scale by market cap → inflate by $1/\pi$ for grant-anticipation) giving the per-patent value $\xi_j$; the Week-1 **construct-vs-measure** gap, **convergent/predictive validity**, **selection**, and **external validity**; and the variance-of-an-average shrinkage $\sigma\mapsto\sigma/\sqrt n$. Every numerical result here was confirmed in Python (NumPy abnormal-return and CAR arithmetic, the three-window stress, and the $1/\sqrt n$ table); verifying notes appear where useful. All dollar figures and table values are **illustrative and constructed**, never quoted as KPSS's own; the paper is cited by name as **Kogan, Papanikolaou, Seru & Stoffman (2017)** (KPSS).

---

## Problem 1 — Why a dollar measure? Counts, citations, and the construct–measure gap (14 points)

**(a) (4 pts)** The **construct** Leah cares about is **the private economic value of a single invention — how many dollars the patent is worth to the firm that owns it.** The two standard proxies fail in distinct ways:

*Patent counts* weight every patent **equally** — one trivial design tweak counts the same as the patent that defined a decade — so a firm with a hundred throwaway patents looks more innovative than a firm with the one transformative one. Counts measure *quantity*, not *value*.

*Forward citations* are a real improvement (they track importance), but they carry **two** defects §1 insists you recite. First, *timing/speed*: citations accumulate over ten or more years, so you cannot value a recent patent in real time. Second, *truncation*: recent patents look artificially uncited simply because the future that would cite them has not happened yet. And neither proxy is denominated in dollars — the unit anyone actually cares about.

**(b) (4 pts)** The clever move (§5) is to **let the stock market value the patent for you.** (i) A patent grant is *news* because the USPTO's decision and exact claims were uncertain beforehand; the grant resolves some of that uncertainty, and the market updates the firm's price the moment the grant becomes public. (ii) A large positive reaction says the market judged the patent valuable; a near-zero reaction says it judged it worthless — the size of the jump *is* the market's dollar estimate. (iii) This **outsources the valuation** to the thousands of investors who collectively set the price and have already done the hard work, so KPSS need *not* build a structural model of demand, competition, and discount rates (assumptions nobody can defend); they just read the price reaction with the cleanest tool available, the abnormal return in a tight window.

**(c) (3 pts)** The *units* advantage: citations are not denominated in **money** — they count attention, not dollars — whereas the market reaction is a dollar figure directly. The *speed/timing* advantage: a stock reaction happens in **three days** and is available the instant the patent issues, while citations take **a decade** to accrue (and are truncated for recent patents). The speed is what makes a **long firm-year panel possible**: because every patent — including last year's — gets a value *immediately*, KPSS can build a dense year-by-year panel, and a panel is exactly what you need to study growth and reallocation, which play out over time. Citations could never deliver a real-time panel.

**(d) (3 pts)** In Week-1 language, the **construct** is the patent's true economic value (unobservable), and the **measure** is the grant-window abnormal stock return, scaled to dollars (observable). The honest one-sentence description: *the KPSS number is the **market's** **expected** private value of the patent **at grant**.* Dropping any of the three words overclaims: drop "market's" and you pretend it is the true value rather than the market's opinion of it; drop "expected" and you pretend it is realized value rather than a forecast; drop "at grant" and you pretend it incorporates everything learned later. It is **not** the value the patent ultimately realized — a patent the market loved at grant that later flopped still carries a high KPSS value, which is precisely the construct-vs-measure gap.

---

## Problem 2 — Rebuild one patent's value from a grant-window event study (24 points)

Given: $\hat a_f=0.0000$, $\hat b_f=1.10$, $\text{MktCap}_f=\$8{,}000{,}000{,}000$. Predicted normal return each day is $\hat R_{ft}=\hat a_f+\hat b_f R_{mt}=1.10\,R_{mt}$.

**(a) (6 pts)** Abnormal return $AR_{ft_k}=R_{ft_k}-(\hat a_f+\hat b_f R_{mt_k})$, day by day:

| $k$ | $R_{ft}$ | $R_{mt}$ | $\hat b_f R_{mt}$ | $AR_{ft_k}=R_{ft}-\hat b_f R_{mt}$ |
|:---:|:---:|:---:|:---:|:---:|
| $-1$ | $0.0120$ | $0.0040$ | $1.10(0.0040)=0.0044$ | $0.0120-0.0044=0.0076$ ($0.76\%$) |
| $0$ | $0.0180$ | $0.0050$ | $1.10(0.0050)=0.0055$ | $0.0180-0.0055=0.0125$ ($1.25\%$) |
| $+1$ | $0.0070$ | $0.0030$ | $1.10(0.0030)=0.0033$ | $0.0070-0.0033=0.0037$ ($0.37\%$) |

(With $\hat a_f=0$ the intercept drops out.) You subtract $\hat b_f R_{mt}$ because of the §2 first refinement, **"filter out the market"**: a stock can move during the window for reasons that have nothing to do with the patent — the whole market rallied, or the firm's sector moved — and that contribution lives in $\hat b_f R_{mt}$. If you skipped it, the *raw* window return would mix the patent's value with whatever the broad market did those three days; the patent's value lives in the residual (the abnormal return), not the raw return.

**(b) (5 pts)** Cumulative abnormal return over the three window days:
$$
\text{CAR}=\sum_{k=-1}^{+1}AR_{ft_k}=0.0076+0.0125+0.0037=0.0238=2.38\%.
$$
Gross dollar reaction:
$$
\text{CAR}\times\text{MktCap}_f=0.0238\times\$8{,}000{,}000{,}000=\$190{,}400{,}000.
$$
The market-cap multiplication is §2's second refinement, **"scale by market cap."** A raw percentage cannot be compared across firms of different sizes because the *same* 2.38% jump is a very different dollar amount for an \$8B firm than for a \$200M firm; multiplying by market cap converts the firm-specific percentage surprise into the dollars the market added to the firm's value on news of the patent.

**(c) (5 pts)** The third refinement inflates for grant-anticipation. With $\pi=0.5$:
$$
\xi_j=\frac{\text{CAR}\times\text{MktCap}_f}{\pi}=\frac{\$190{,}400{,}000}{0.5}=\$380{,}800{,}000.
$$
The adjustment **raises** the estimate because a grant is only *partly* a surprise — markets anticipate some grants, so the observed window reaction captures only the *unanticipated* fraction of the patent's value; dividing by $\pi<1$ grosses the reaction back up to the full expected value. Interpretation, the careful sentence now attached to a number: **$\xi_j\approx\$381$ million is the market's expected private value, at grant, of patent $j$ to firm $f$** — not what the patent ultimately earned.

**(d) (5 pts) Window stress.** Holding $\hat a_f,\hat b_f$ fixed and converting *gross* (pre-$\pi$) reactions to dollars:

- **One-day** ($k=0$ only): $\text{CAR}_1=AR_{f,0}=1.25\%=0.0125$, so $0.0125\times\$8\text{B}=\$100{,}000{,}000.$
- **Three-day** ($k\in\{-1,0,+1\}$): $\text{CAR}_3=2.38\%$, so $\$190{,}400{,}000$ (from part b).
- **Five-day** ($k\in\{-2,\dots,+2\}$): add $AR_{f,-2}=+0.005\%=0.00005$ and $AR_{f,+2}=-0.15\%=-0.0015$ to the three-day CAR: $\text{CAR}_5=0.0238+0.00005-0.0015=0.02235=2.235\%$, so $0.02235\times\$8\text{B}=\$178{,}800{,}000.$

Side by side: **\$100M (1-day) · \$190.4M (3-day) · \$178.8M (5-day)** — the estimate nearly *doubles* between the one-day and three-day windows and then drifts back down when two more days are added. This makes §6's vulnerability **"the measure depends on modeling choices"** concrete: the same patent's "value" moves by tens of millions of dollars purely because of the window you pick. The **short** window is the principled default because the longer you make the window, the more time you give *other* value-relevant news (earnings, deals, analyst revisions) to land inside it and contaminate the abnormal return — the very confound of §6 / Problem 4(b). So no single $\xi_j$ should be read as "the patent is worth exactly \$X"; it is a noisy, model-dependent point estimate, which is exactly why the firm-year aggregation of Problem 5 is the unit the paper actually trusts.

*(Verification: $AR$ = $\{0.76,1.25,0.37\}\%$; CAR$_3$=2.38%, \$190.4M; CAR$_1$=1.25%, \$100.0M; CAR$_5$=2.235%, \$178.8M; $\xi_j$=\$380.8M at $\pi=0.5$. Confirmed in Python.)*

---

## Problem 3 — What would convince you the measure is valid? (18 points)

**(a) (5 pts) Convergent validity.** This is §4 Step 1's first sanity test — **"does the market-based value correlate with forward citations?"** You wanted a **positive, significant** slope, and Leah's $+0.31$ ($t=5.8$) delivers it. The logic of why it is reassuring but not sufficient: citations are the literature's established proxy for patent importance, trustworthy *where they apply*, so if the dollar value rises with citations the new measure **agrees with the old one where the old one is trustworthy** — that is convergent validity, evidence the new number is tracking something real and not noise. But it is not sufficient because a measure that merely *reproduced* citations would add nothing — citations already exist, and they are slow and unit-less; the point of KPSS is to do *more* than citations (dollars, in real time), so convergent validity is the floor, not the ceiling. (Acceptable also: citations themselves are an imperfect proxy, so agreement with them cannot by itself certify agreement with the *construct*.)

**(b) (5 pts) Predictive validity.** §4 calls the profitability/growth test "the strongest" because it shows the measure — built from a **three-day stock reaction** — forecasts a **real outcome years out**, the owning firm's future profits/output. In Week-1 terms: the citation test in (a) shows the measure **agrees with another proxy** (one imperfect ruler matching another), whereas the profitability test shows the measure **agrees with the construct itself** — economic value should, if real, be followed by higher realized profits, so a positive predictive slope is direct evidence that the number captures value, not just attention. Leah's $t\approx3.6$ (predicting a planted next-year outcome in `nb6.1`) is exactly this stronger evidence: a forecast of reality, not a correlation with a sibling proxy.

**(c) (4 pts) The discriminant check.** The §4 test is **"does it survive the obvious confound?"** — showing the patent-grant signal is *distinct* from a generic announcement return rather than just reflecting *other* contemporaneous news. One concrete check on synthetic data: Leah compares the average grant-window abnormal return to the average abnormal return over **matched non-grant windows** for the same firms (placebo windows on ordinary days with no patent news) — if grant windows show a systematically larger reaction than placebo windows, the signal is attributable to the patent rather than to generic announcement-day churn. (Acceptable also: compare across patents that *do* vs *do not* later prove valuable, or regress out earnings-announcement returns and check the grant effect survives.)

**(d) (4 pts) Falsifiability.** §4's rule for reading these tables is to read them for **signs and significance**, **not** for magnitudes you memorize — the pattern that matters is that the value measure is positively and significantly related to citations, profits, and growth. The measure would **break** ("the paper collapses here") if that pattern *failed*: if the value–citation slope were flat or wrong-signed, if the value–profit forecast were insignificant, or if grant-window returns were indistinguishable from generic announcement returns — any of these would mean the constructed dollar value is not tracking patent value at all. This entire validation exercise lives in Reader's-Guide section **§4, "Table-by-table reading order"** (specifically Step 1, the measure-validation evidence a referee reads *first*).

---

## Problem 4 — Read like a referee: three named vulnerabilities (24 points)

**(a) (8 pts) Expectations, not realized value (Week 1 — measurement validity).**

(i) The grant-window return is a forecast **of the patent's economic value**, formed by the market in three days using only the information available *then*. It is **not** the value the patent *ultimately realized*. The gap is exactly the Week-1 construct-vs-measure gap: the **construct** is true realized economic value; the **measure** is a three-day price reaction, i.e., the market's *expectation* of that value at grant.

(ii) Concrete example, Leah's terms: a glamorous AI-chip patent grant that the market greets with a big positive abnormal return — earning a high $\xi_j$ — but whose technology is leapfrogged within two years and never earns the firm a dollar. For "flashy" patents the market over-loves at grant, the measure's error is **upward**: $\xi_j$ is too high relative to realized value (and symmetrically, quiet patents the market underrates carry a downward-biased $\xi_j$).

(iii) The check (from the "Read like a referee" box): regress a *later realized* outcome — eventual profits attributable to the patent, eventual forward citations, or litigation/renewal outcomes — on the grant-window $\xi_j$, and ask whether the forecast is **unbiased** (slope $\approx1$ on average, errors centered at zero) or **systematically too high for some kinds of patents** (e.g., a negative residual concentrated among the flashiest, most-hyped technology classes). The deep reason the measure can **never, by itself**, separate "the market was right" from "the market was wrong but consistently wrong": the measure *is* the market's forecast, so any test using *only* the measure is circular — you need an *external* realized-outcome benchmark (the later data above) to grade the forecast, and even then a *consistent* bias would just shift the whole calibration without revealing itself within the grant-window number alone.

**(b) (8 pts) Confounding news in the window (Week 4 — event-study identification).**

(i) The identifying assumption (§2, one sentence): **the abnormal return in the grant window equals the market's unbiased estimate of the patent's value — as long as the patent grant is the *only* value-relevant news in that short window** (and markets are efficient enough to impound it).

(ii) Two concrete other-news kinds: an **earnings announcement** (or a guidance update) landing in the window, and a **merger/acquisition or major-deal announcement** (also acceptable: an analyst rating revision, a lawsuit outcome, a regulatory ruling). Either corrupts $\xi_j$ because the window's abnormal return now mixes the patent's value with the *other* news's value — the price moved for two reasons and the construction credits all of it to the patent, biasing $\xi_j$ up or down by the size of the contaminating surprise.

(iii) **Idiosyncratic** confounds are news items that hit individual patents in *random*, *uncorrelated* directions — some windows catch good news, some bad, with no relationship to the patent's true value. Averaging over the many patents in a firm-year (Problem 5) makes these cancel, because their mean tends to zero. **Systematic** confounds are contamination that is *correlated* across patents or *correlated with the true value itself* — e.g., if firms strategically time good-news disclosures near grant dates, or if grant windows for genuinely valuable patents also tend to carry positive earnings surprises. These do **not** wash out under aggregation, because their mean does *not* go to zero — averaging many same-signed errors leaves the bias intact. The systematic case is the genuinely dangerous one, and it is exactly the `nb6.1` "break it" extension where injecting contamination *correlated with* the true value survives aggregation and degrades the validation (whereas purely *random* contamination is averaged away even at high contamination shares).

**(c) (8 pts) Selection and efficient markets (Week 1 — external validity; circularity).**

(i) The three stacked selection screens (§6): **(1) only *granted* patents** get a value — rejected/abandoned applications, and the decision to even apply, are invisible; **(2) only patents of *publicly traded* firms with usable CRSP returns** can be valued — private firms, pre-IPO startups, universities, and foreign assignees drop out; **(3) the firm must *survive* and stay listed** around the grant date. The population the firm-year panel actually represents: **the innovation of large, public, surviving U.S. firms** — *not* "all innovation in the economy."

(ii) A conclusion not extendable to the whole economy: that **a surge of innovation reallocates resources away from rivals across the economy** (the creative-destruction story at the aggregate level). The panel only sees public, surviving firms, so it is silent on innovation by private firms, startups, and universities — exactly the actors who do much of the disruptive innovating — so an economy-wide reallocation claim requires an argument the panel's selected sample cannot supply.

(iii) The **circularity**: the measure is *built* on the assumption that the market prices the patent correctly and promptly at grant — efficiency is the *premise* that turns the abnormal return into "the value." So you cannot turn around and use the measure to *test* market efficiency, because you would be assuming the conclusion. "Efficient markets cuts both ways" for the measure's accuracy: if markets are **slow/noisy**, value leaks in *after* the window and the measure is **attenuated** (too low); if markets **over-react**, the window over-counts and the measure is **inflated** (too high). Either way the measure inherits whatever pricing errors the market makes, and the construction has no internal way to detect them.

---

## Problem 5 — Aggregation: why summing noise sharpens the signal (10 points)

**(a) (5 pts)** Write $\hat\xi_j=\xi_j^{\text{true}}+e_j$ with $e_j$ roughly independent across patents and $\operatorname{Var}(e_j)=\sigma^2$. For the $n$ patents a firm is granted in a year, the **average** noise is $\bar e=\frac1n\sum_{j=1}^n e_j$. By the variance-of-an-average rule, with independent $e_j$,
$$
\operatorname{Var}(\bar e)=\frac{1}{n^2}\sum_{j=1}^n\operatorname{Var}(e_j)=\frac{n\sigma^2}{n^2}=\frac{\sigma^2}{n}
\;\Longrightarrow\;
\operatorname{sd}(\bar e)=\frac{\sigma}{\sqrt n}.
$$
So averaging $n$ roughly-independent noisy values shrinks the noise standard deviation by the factor $1/\sqrt n$:

| Patents in firm-year, $n$ | $1$ | $4$ | $25$ | $100$ |
|:---:|:---:|:---:|:---:|:---:|
| Noise-SD shrink factor $1/\sqrt{n}$ | $1.00$ | $0.50$ | $0.20$ | $0.10$ |

(A firm with 100 granted patents averages its per-patent noise down to one-tenth of a single patent's noise SD. Equivalently, the firm-year *total* has signal-to-noise growing like $\sqrt n$: the true total scales with $n$ while its noise SD scales only with $\sqrt n\,\sigma$, so SNR $\sim n/(\sqrt n\,\sigma)=\sqrt n/\sigma$.)

**(b) (3 pts)** The shrinkage requires the noise $e_j$ to be **roughly independent (uncorrelated) across patents with mean zero** — only then do the cross terms in the variance vanish and the errors cancel rather than reinforce. This is the *same* distinction as Problem 4(b): aggregation defeats **idiosyncratic** confounds (independent, mean-zero window noise — which is what makes $\bar e\to0$), and it leaves **systematic** confounds untouched (correlated or value-dependent contamination, whose mean does *not* go to zero, so $\bar e$ stays biased). It is the same fork because whether the firm-year panel can be trusted comes down to exactly whether the per-patent errors are independent (washed out by summing) or systematic (carried straight through the sum).

**(c) (2 pts)** Leah's firm-year correlation ($\approx0.72$) beats her per-patent correlation ($\approx0.4$) because the construction *is* unchanged but the **unit** changed: at the patent level each $\hat\xi_j$ carries the full per-patent noise SD $\sigma$ (window confounds, model error swamping a small true blip), whereas summing within firm-year averages that noise down by $1/\sqrt n$, so the firm-year totals track the true firm-year value far more tightly. The design lesson for her capstone: when a per-unit measure is **noisy but unbiased**, aggregating to a coarser unit buys you a **much cleaner signal** (noise falls like $1/\sqrt n$ while the true signal accumulates), at the **cost of resolution** — the firm-year panel can no longer answer *patent-level* questions (which *specific* patent was the blockbuster), only firm-year ones.

---

## Problem 6 — Design the replication pipeline for `nb6.1` (10 points)

**(a) (4 pts) Inspect and aggregate (§7 Exercise 1).** Ordered steps:
1. Load the patent-level value file (one row per granted patent: firm id, grant year, $\xi_j$), or the seeded synthetic stand-in with the same schema.
2. **Plot the distribution of per-patent values first**, *before* trusting them — expect it to be **wildly right-skewed**, a few blockbuster patents dwarfing thousands of small ones (in `nb6.1`'s synthetic data the top decile holds the large majority of total value). That skew *is* the whole motivation for not counting patents equally: if value were roughly uniform across patents, counts would suffice; because it is heavy-tailed, one transformative patent outweighs a hundred trivial ones, so you must *weight by dollars*.
3. **Aggregate**: sum $\xi_j$ within (firm, year) to build the firm-year innovation-value panel — the central data object.
4. Sanity checks: (i) print the **top-ten firm-years by total value** and ask whether the names make sense (do the famous innovators show up?); (ii) note **which patents lack a value and why** — patents of private/foreign/non-listed assignees or without usable CRSP returns around the grant date get *no* value, the §6 selection made visible.

**(b) (4 pts) Rebuild and stress one patent's value (§7 Exercise 2).** Pipeline (the Problem 2 calculation, automated):
1. Pick one patent and its owning firm; pull the firm's **daily** returns.
2. Fit the **market model** $R_{ft}=a_f+b_fR_{mt}+\varepsilon$ on a **pre-event estimation window** (e.g., ~120 trading days) ending a short **gap** (e.g., ~10 days) before the grant date, so event-window returns never leak into the estimation of the normal-return model.
3. Form the daily **abnormal returns** over the short **grant window** and sum to the **CAR**.
4. Multiply CAR by **market cap** at grant to get dollars; (optionally) inflate by $1/\pi$ for grant-anticipation; this is your hand-built $\xi_j$.
5. **Compare** your $\xi_j$ to the published KPSS value for that patent.
Then **vary on purpose** the two construction choices §7 flags — the **window length** (1-day / 3-day / 5-day) and the **normal-return model** — and watch the estimate move, the Problem 2(d) lesson that the measure depends on modeling choices.

**(c) (2 pts) Validate, then break it; and data discipline (§7 Exercise 3 + Conventions §5).** The validation regression: regress a **future outcome** (next year's profitability/growth, or the known "true" value in synthetic data) on **this year's** firm-year KPSS value, and confirm the positive, significant slope. The **"break it"** manipulation: inject simulated **earnings-announcement returns** into a subset of grant windows, rebuild the measure on the contaminated windows, and watch the validation degrade (Problem 4(b)). Data discipline: the notebook must (i) ship a **seeded synthetic fallback** with the same schema (simulated grants, dates, daily returns, and a baked-in "true" value) so every step runs end-to-end on a student laptop with **no licensed data**; and (ii) be honest about not fabricating real numbers — real CRSP daily returns stay **read-only on GMU infrastructure** with a **pinned snapshot date** (Conventions §5), the public KPSS dataset is a documented **Path-A pull**, and no real empirical estimates are invented.

---

*All numerical answers verified in Python. Key results: P2 daily $AR=\{0.76,1.25,0.37\}\%$ (predicted piece $\hat b_fR_{mt}=\{0.44,0.55,0.33\}\%$); 3-day CAR $=2.38\%$, gross $=0.0238\times\$8\text{B}=\$190{,}400{,}000$; with $\pi=0.5$, $\xi_j=\$380{,}800{,}000$; window stress gross dollars $\$100.0\text{M}$ (1-day, $1.25\%$) / $\$190.4\text{M}$ (3-day, $2.38\%$) / $\$178.8\text{M}$ (5-day, $2.235\%$). P5 shrink factors $1/\sqrt n=\{1.00,0.50,0.20,0.10\}$ for $n=\{1,4,25,100\}$; firm-year SNR $\sim\sqrt n$. Citations by name only, per chapter: Kogan, Papanikolaou, Seru & Stoffman (2017). All dollar figures and validation t-stats illustrative/constructed; no fabricated KPSS table numbers.*
