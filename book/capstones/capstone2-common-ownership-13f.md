# Capstone 2 (Exemplar) — Common Ownership from 13F

> **ASSIP framing — read first.** *The ASSIP 2026 terminal deliverable is a research poster
> (~48"×36") + a JSSR abstract (200–300 words) + an 8-minute poster talk + a replication packet
> — not a full paper.* This exemplar is the **full research narrative the poster summarizes**: a
> complete empirical-finance paper written one level above the ASSIP graded artifact, so that you
> can see what the full argument looks like before you compress it onto six poster panels
> (question · why · design · headline · robustness · contribution-and-limits) and a 10-sentence
> abstract. The optional companion full paper, when written, uses this exemplar as its length-and-
> shape template; the required poster pulls panels from its sections.
>
> **Track:** Common Ownership from 13F · **Anchor paper:** Gao, L., Han, J., Kim, J-B., & Pan, T. (2024), "Overlapping institutional ownership along the supply chain and earnings management of supplier firms," *Journal of Corporate Finance*, 84, 102520.
>
> **Student-track variant notice.** *The anchor paper's actual outcome variable is **earnings management of supplier firms** (measured as discretionary accruals from Compustat). This capstone keeps the **same thematic point** — overlapping ownership along a corporate relationship reshapes a firm-level outcome a referee will demand be measured carefully — but substitutes a **voluntary-disclosure index** as the outcome, because (i) the disclosure construct is easier to build, label, and reason about for a high-school capstone, and (ii) it lets the camp practice the measurement-error discipline against a different sensor than the anchor paper's accruals model. **Read this paper as a sibling-outcome variant of the anchor**, not as a replication of it; the design moves, threats table, and inference discipline are the same. Where the anchor paper measures earnings management as a continuous accounting residual, this paper measures voluntary disclosure as a count of guidance items — different sensor, same measurement-error logic.*
>
> **Synthetic-data notice — read before the abstract.** *Every number in this paper — coefficients, standard errors, sample sizes, summary statistics, and the figure — is computed on **synthetic 13F-like holdings data constructed for instruction**, not on real SEC filings or the Thomson/Refinitiv panel. The "results" are **illustrative, not empirical findings**. They exist to show a high-school camp reader what a finished common-ownership paper looks like — the structure, the table craft, the identification discipline, the honest hedging — and they should never be cited as evidence about real markets. Where a real study would report a verified estimate, this exemplar reports a plausibly shaped placeholder, and says so.*

---

## Common Ownership and Voluntary Disclosure: Evidence from a Synthetic 13F Panel

**A capstone exemplar by "Maya R." (ASSIP 2026 (Aspiring Scientists Summer Internship Program), Cohort 2026), advised by Prof. Lei Gao**

### Abstract

When the same large institutional investors hold big stakes in two different firms, those firms are said to be under *common ownership* — and a growing literature argues this shared ownership changes how firms behave toward one another. I build a firm-pair common-ownership measure from quarterly 13F institutional holdings and relate it to a firm's voluntary disclosure, the forward-looking guidance a firm chooses to release. On a **synthetic 13F-like panel** of 600 firms over 24 quarters (2018Q1–2023Q4), built to mimic the structure of the real data, I estimate panel fixed-effects regressions of a disclosure index on a firm's average common ownership with its product-market peers. In the saturated specification — firm and quarter fixed effects, standard errors clustered by firm — a one-standard-deviation increase in common ownership is *associated with* a 0.18-point higher disclosure index (about 11% of a standard deviation), and the association is stable across the build-up of controls. **These magnitudes are illustrative outputs of synthetic data, not estimates of any real-world effect.** I treat the result as observational throughout: common ownership is not randomly assigned, and I devote the design and robustness sections to the threats that follow from that fact. The exercise mirrors, in miniature and on instructional data, the *structural* question Gao, Han, Kim & Pan (2024) ask of real supply-chain overlapping institutional ownership and supplier-firm earnings management — same identifying frame, different sensor on the outcome (see the student-track variant notice above).

---

### 1. Introduction

In a typical recent quarter, the three largest U.S. asset managers together held more than 5% of almost every company in the S&P 500, and often far more — the same handful of institutions sitting on the share registers of firms that compete with one another in the same product market. That fact, a curiosity two decades ago, is now the center of an active debate in finance, antitrust, and corporate governance: when the *same* owners hold *competing* firms, do those firms still behave as rivals? The answer bears on the prices consumers pay, on how aggressively firms innovate, and — the angle this paper takes — on how much firms voluntarily tell the market. The overlap itself is easy to document from public filings; what is hard, and contested, is whether it *changes firm behavior* or merely *reflects* something else about which firms attract the same investors.

This paper constructs a firm-pair common-ownership measure from 13F institutional holdings and relates it to firm-level voluntary disclosure, asking whether firms more commonly owned with their product-market peers disclose differently. The contribution is to *document, on a transparent and reproducible 13F-based measure, a robust panel association between common ownership and voluntary disclosure* — and to be honest about why that association is an association and not yet a causal effect. I deliberately do not claim to estimate a causal effect, because, as Section 4 argues, common ownership is endogenous: investors choose which firms to co-hold, and the same forces that draw them to co-hold two firms may independently drive those firms' disclosure.

I find that a one-standard-deviation increase in a firm's average common ownership with its peers is associated with a 0.18-point increase in its disclosure index — roughly 11% of the index's standard deviation — in the most demanding specification, which absorbs firm and quarter fixed effects and clusters by firm. The association moves only modestly as I add controls and fixed effects (from 0.24 in the bivariate column to 0.18 in the saturated one): about a quarter of the raw correlation is confounding the controls and fixed effects soak up, and the rest survives the most demanding specification I can run on observational data. The association is robust to alternative clustering, an alternative ownership measure, and dropping the largest investors; it does *not* survive as a clean causal claim, and I say so. **All of these numbers are computed on synthetic data and are illustrative only.**

The rest of the paper proceeds as follows. Section 2 positions the exercise in the common-ownership literature. Section 3 describes the synthetic 13F panel and how the common-ownership measure is built from holdings overlap. Section 4 lays out the panel specification, states the identifying assumption in one sentence, and confronts the endogeneity of ownership in a threats table. Section 5 presents the headline results. Section 6 reports robustness organized around the threats. Section 7 concludes with the limits the design cannot escape.

### 2. Positioning in the literature

Three strands of work meet at the question this paper asks, and the gap I occupy is visible only once they are placed side by side rather than listed.

The first strand **measures** common ownership and documents its rise. From the observation that index funds and large active managers hold diversified stakes across whole industries, this literature built the standard tools for quantifying overlap — pairwise co-holding, portfolio-weighted measures of how much two firms' investors coincide — and showed overlap has grown dramatically. It tells us common ownership is large; it does not tell us what it *does*. The second strand asks what overlap does to **product-market competition**, and it is where the controversy lives: one line argues commonly owned firms compete less aggressively and raise prices, while subsequent papers contest both the measurement and the identification, arguing the correlations may reflect which industries attract diversified investors rather than a causal softening of competition. The unresolved core of that debate is *exactly* the endogeneity problem this paper foregrounds — ownership is chosen, not assigned, so a raw correlation between overlap and any outcome is suspect until the design says otherwise.

The third strand — the one this paper sits closest to — connects common ownership to **firm-level reporting and information behavior**. The anchor is Gao, Han, Kim & Pan (2024), who study *overlapping institutional ownership* along the supply chain — the same institutions holding large stakes in both a supplier and its customer — and relate it to the **earnings management** of the supplier firms, measured as discretionary accruals (the slack with which managers shape the reported earnings number away from the underlying cash reality). Their setting is the supplier–customer link with earnings management as the outcome; mine is the product-market peer with **voluntary disclosure** as a sibling outcome — a simpler construct for the camp to build, but driven by the same economic mechanism. The conceptual move is the same: an investor who holds both sides of a relationship internalizes information spillovers between them, which can change how the firm both *reports* its results and *talks about* them. Where Gao, Han, Kim & Pan (2024) bring a careful identification strategy and an accruals-based outcome to the supply-chain case, this exemplar is more modest, runs on a different but related outcome (voluntary disclosure), and is honest about its limits — it documents the panel association on a transparent 13F measure and stops short of the causal claim. The gap I fill is therefore not a gap in the real literature; it is a *pedagogical* one: a fully worked, reproducible, synthetic-data example of how to build the measure, run the panel, and report it to the Appendix-D standard, with the causal language disciplined to what an observational design can bear.

### 3. Data

#### 3.1 The 13F source and what it does and does not tell us

The raw ingredient of any common-ownership measure is Form 13F, the quarterly report that institutional investment managers with over \$100 million in qualifying U.S. equity assets must file with the SEC, disclosing their long equity positions — which stocks, how many shares, what market value — as of each calendar quarter-end. There are two routes to it: the free, public **SEC EDGAR** filings (the exact information-table XML, which you de-duplicate and clean yourself), and the licensed, cleaned **Thomson Reuters / Refinitiv s34 panel on WRDS** (de-duplicated, consistent manager identifiers, but bound by the GMU-infrastructure rule). For a real version of this project the choice between them is the whole methodological point; for this exemplar I use neither, because the data are synthetic — but the synthetic panel mirrors the EDGAR information-table schema (one row per manager-quarter-holding: manager id, CUSIP, period, shares, value) so the measure-building code would run unchanged on a real EDGAR pull.

Three limits of 13F are conceptual constraints the design must respect, because they bound what any common-ownership measure can mean. First, **13F reports long positions only** — no shorts, no most derivatives — so disclosed holdings are not a manager's true net exposure; a "common owner" measured from 13F is a common *long* owner. Second, the **45-day reporting lag** makes holdings stale by the time they are filed, so a 13F-based measure is a lagged snapshot, never real-time positioning. Third, the **"who is one manager" problem** — family-of-funds and sub-advisor structures mean the same assets can appear under several filer identities, so the measure is sensitive to how managers are aggregated, a modeling choice I state rather than a data field I read. (A fourth caveat, **CUSIP licensing**, is a publishing constraint: CUSIPs may be used inside an analysis but a CUSIP master file may not be redistributed; my synthetic data sidesteps this by inventing identifiers.)

#### 3.2 Building the common-ownership measure from holdings overlap

The construct begins with a single intuition stated in one sentence: **two firms are commonly owned to the degree that the same institutions hold large stakes in both.** Turning that sentence into a number takes three steps, and I show the arithmetic on a tiny example before the formula, because a number before a Greek letter is the camp's rule.

*Step one — ownership shares.* For each firm $j$ and quarter $t$, and each institution $m$, compute the fraction of firm $j$'s shares outstanding that manager $m$ holds, call it $w_{mjt}$. If BlackRock holds 7% of Firm A and 5% of Firm B, then $w_{\text{BlackRock},A,t}=0.07$ and $w_{\text{BlackRock},B,t}=0.05$.

*Step two — pairwise overlap.* For a pair of firms $(j,k)$, sum across institutions the product of the two ownership shares:

$$
\text{CO}_{jkt} \;=\; \sum_{m} w_{mjt}\, w_{mkt}.
$$

This is large when the *same* managers hold large stakes in *both* firms, and zero when no institution holds both. In the toy example, if BlackRock is the only common holder the pair's overlap is $0.07 \times 0.05 = 0.0035$; add Vanguard at 6% and 6% and it grows by $0.06\times0.06 = 0.0036$, to $0.0071$. The measure rewards both *how many* institutions co-hold and *how large* their stakes are — the portfolio-weighted spirit of the standard common-ownership measures, simplified to what 13F shares-outstanding ratios support.

*Step three — aggregate to the firm.* A firm's exposure to common ownership is its average overlap with its product-market peers. Let $\mathcal{P}_j$ be the set of firm $j$'s peers (in the synthetic data, firms in the same of 30 simulated industries); then

$$
\text{CommonOwn}_{jt} \;=\; \frac{1}{|\mathcal{P}_j|}\sum_{k \in \mathcal{P}_j} \text{CO}_{jkt}.
$$

This firm-quarter number is the key regressor. I standardize it (mean zero, unit variance within the sample) so that coefficients read in standard-deviation units, which the Appendix-D craft prefers to raw magnitudes that would print as $0.0003$.

#### 3.3 The synthetic panel and the outcome

The panel is 600 firms across 24 quarters (2018Q1–2023Q4), $N = 14{,}400$ firm-quarters, partitioned into 30 industries of 20 firms each. Holdings are simulated for 200 institutions whose choices induce realistic overlap: large "index-like" managers hold broad, correlated baskets (generating high common ownership), while smaller managers hold concentrated, idiosyncratic positions. The outcome, $\text{Disclosure}_{jt}$, is a synthetic voluntary-disclosure index — a standardized count of forward-looking guidance items a firm issued that quarter (a *sibling* outcome to the supplier-firm earnings management Gao, Han, Kim & Pan (2024) study; see the student-track variant notice at the top) — built to carry a modest positive association with common ownership *plus* firm-level persistence, an industry-time component, and substantial noise, so the estimation problem is non-trivial and the fixed effects do real work. Because I built the data-generating process, I *know* the "true" association I planted — exactly why this is a teaching exemplar and not evidence. Controls (log assets, leverage, a profitability proxy) are simulated to correlate with both ownership and disclosure, so omitting them would bias the bivariate estimate and the build-up across columns is informative.

Table 1 reports summary statistics for the estimation sample.

**Table 1 — Summary statistics (synthetic 13F panel, 2018Q1–2023Q4)**

| Variable | Mean | SD | p10 | Median | p90 |
|---|---:|---:|---:|---:|---:|
| Disclosure index | 0.00 | 1.62 | −2.03 | −0.04 | 2.07 |
| Common ownership (CO, standardized) | 0.00 | 1.00 | −1.21 | −0.13 | 1.34 |
| Common ownership (raw, ×10³) | 4.18 | 2.11 | 1.69 | 3.92 | 7.05 |
| Log assets | 7.41 | 1.38 | 5.66 | 7.40 | 9.18 |
| Leverage | 0.31 | 0.18 | 0.07 | 0.30 | 0.55 |
| Profitability | 0.09 | 0.11 | −0.03 | 0.09 | 0.22 |
| No. of common holders per firm | 23.6 | 9.4 | 12 | 23 | 36 |

*Notes.* Synthetic 13F-like panel constructed for instruction; **not real holdings data**. $N = 14{,}400$ firm-quarters (600 firms × 24 quarters). The disclosure index and standardized common ownership are scaled to mean 0; "Common ownership (raw)" is $\text{CommonOwn}_{jt}$ before standardizing, multiplied by $10^3$ for readability. All values are illustrative.

### 4. Empirical design and identification

#### 4.1 Specification

I estimate a two-way fixed-effects panel regression of disclosure on lagged common ownership:

$$
\text{Disclosure}_{jt} \;=\; \beta\,\text{CommonOwn}_{j,t-1} \;+\; \boldsymbol{\delta}'\mathbf{X}_{j,t-1} \;+\; \alpha_j \;+\; \lambda_t \;+\; \varepsilon_{jt},
$$

stated in the CONVENTIONS §4 form so every slot is explicit:

- **Outcome:** $\text{Disclosure}_{jt}$, the firm-quarter voluntary-disclosure index (synthetic).
- **Key regressor:** $\text{CommonOwn}_{j,t-1}$, the firm's standardized average common ownership with its product-market peers, lagged one quarter to respect the 45-day 13F reporting lag and to reduce the most mechanical reverse-causality channel.
- **Controls $\mathbf{X}$:** log assets, leverage, profitability, all lagged.
- **Fixed effects:** firm fixed effects $\alpha_j$ (absorbing everything time-invariant about a firm — its business model, its baseline disclosure culture) and quarter fixed effects $\lambda_t$ (absorbing market-wide shocks to disclosure, such as a regulatory change or a recession quarter).
- **Clustering:** standard errors clustered by firm (600 clusters), the level at which residuals are most obviously correlated.
- **Sample:** the synthetic panel, 600 firms × 24 quarters, $N = 14{,}400$ firm-quarters (the lag costs the first quarter, leaving 13,800 in estimation; reported below).
- **Identifying assumption (one sentence):** *conditional on firm and quarter fixed effects and the controls, within-firm changes in lagged common ownership are uncorrelated with within-firm shocks to disclosure* — that is, the timing of changes in who co-holds a firm is, after the fixed effects, as good as unrelated to the firm's disclosure shocks.

I want to be plain about that assumption: **I do not believe it holds cleanly, and the design does not let me test it directly** — which is why every causal verb is absent from this paper. The firm fixed effects buy that I am not comparing high- to low-common-ownership firms (a comparison hopelessly confounded by what kind of firm attracts diversified investors); I am comparing a firm to *itself* as its common ownership changes. The quarter fixed effects buy that a market-wide swing in disclosure or institutional flows does not masquerade as a common-ownership effect. What neither buys is protection against a *time-varying, firm-specific* confounder — a firm becoming more transparent for its own reasons and, for the same reasons, more attractive to the big diversified funds.

#### 4.2 Why clustering is not optional here (recall Petersen)

This is a panel: the same 600 firms over 24 quarters. The lesson of Petersen (2009) is that on such data, residuals for the *same firm* across quarters are correlated — a firm that discloses a lot this quarter tends to next quarter too — so classical or heteroskedasticity-robust standard errors that ignore this within-firm correlation are too small, inflating $t$-statistics and manufacturing false significance (the Bertrand–Duflo–Mullainathan disease). The defensible default is to **cluster by firm**, the level at which the dependence is strongest and at which the key regressor varies most. I report firm-clustered errors throughout and, in Section 6, show what happens under two-way (firm and quarter) and industry clustering — because the clustering choice, not the point estimate, is where a Week-5-trained referee looks first.

#### 4.3 Threats to identification

Common ownership is endogenous, full stop. The honest way to present that is the threats-and-responses table, in descending order of danger. Column 3 reports what I actually do; column 4 is the residual concern that survives, and it is the column a mentor reads first.

**Table 2 — Threats to identification and responses**

| Threat | Why it's plausible here | What I do about it | Residual concern |
|---|---|---|---|
| **Time-varying firm-level confounder** (selection on a firm trend) | A firm becoming more transparent for its own reasons may simultaneously attract diversified institutions, so within-firm co-movement of ownership and disclosure is not the ownership *causing* disclosure. | Firm FE remove fixed firm traits; I add lagged controls and (§6) a firm-specific linear trend. | A firm trend that is non-linear or coincident with the ownership change is not absorbed; this is the threat the design cannot kill, and it caps my verbs at "associated with." |
| **Reverse causality** (disclosure drives ownership) | Funds may buy firms *because* they disclose more (transparency lowers monitoring cost), so the arrow could run outcome → regressor. | I lag common ownership one quarter (also matching the 45-day 13F lag) and, in §6, lag it two quarters. | Lagging reduces but does not eliminate reverse causality if funds anticipate future disclosure. |
| **Measurement / manager-aggregation error** | The "who is one manager" problem: family-of-funds structures mean the same assets appear under several filers, so CO is mismeasured, biasing $\hat\beta$ (classically, toward zero). | §6 rebuilds CO with an alternative measure (count of common holders above a 1% stake) and drops the five largest managers. | Attenuation from remaining mismeasurement means my estimate is, if anything, a lower bound — but I cannot sign every component of the error. |
| **Industry-time shocks** (a peer-group story) | An industry-wide event could move both peers' ownership and a firm's disclosure together within a quarter, beyond what quarter FE absorb. | §6 adds industry × quarter fixed effects. | Sub-industry shocks finer than my 30-industry partition remain. |

The table makes the paper's stance explicit. There is *no* row whose residual concern is "none," because every observational design on chosen ownership has leftover doubt, and a blank fourth column would be a tell that I had not looked hard enough. The most dangerous row — the time-varying firm-level confounder — is the one the fixed effects *cannot* dispatch, and it is the reason this paper documents an association rather than estimating an effect.

### 5. Results

Table 3 is the headline. Read the key coefficient leftward across the columns and watch what survives.

**Table 3 — Common ownership and voluntary disclosure (synthetic panel)**

| | (1) Bivariate | (2) + Controls | (3) + Firm & Quarter FE |
|---|---:|---:|---:|
| **Common ownership ($t-1$, std.)** | 0.24\*\*\* | 0.21\*\*\* | 0.18\*\* |
| | (0.040) | (0.039) | (0.061) |
| Log assets | | 0.142\*\*\* | 0.097\* |
| | | (0.031) | (0.054) |
| Leverage | | −0.31\*\* | −0.19 |
| | | (0.13) | (0.21) |
| Profitability | | 0.88\*\*\* | 0.52\*\* |
| | | (0.18) | (0.24) |
| Constant | 0.01 | −1.02\*\*\* | |
| | (0.021) | (0.23) | |
| Firm fixed effects | No | No | Yes |
| Quarter fixed effects | No | No | Yes |
| Within $R^2$ | 0.022 | 0.061 | 0.034 |
| $N$ (firm-quarters) | 13,800 | 13,800 | 13,800 |

*Notes.* **Synthetic 13F-like data constructed for instruction; not empirical findings.** The dependent variable is the firm-quarter voluntary-disclosure index (standardized, mean 0, SD 1.62). The key regressor is the firm's average common ownership with its product-market peers, lagged one quarter and standardized to unit variance, so the coefficient is the change in the disclosure index per one-standard-deviation increase in common ownership. Sample: synthetic panel of 600 firms over 2018Q1–2023Q4; the one-quarter lag drops the first quarter, holding $N = 13{,}800$ constant across columns. Columns build from bivariate (1) to the two-way fixed-effects specification (3). Standard errors clustered by firm (600 clusters) in parentheses. Column (1) and (2) report the ordinary $R^2$; column (3) reports the within-$R^2$. \*\*\* $p<0.01$, \*\* $p<0.05$, \* $p<0.10$.

The headline coefficient is **0.18** in the saturated column (3): a one-standard-deviation increase in a firm's lagged common ownership with its peers is *associated with* a 0.18-point higher disclosure index. Since the disclosure index has a standard deviation of 1.62, that is about $0.18/1.62 \approx 11\%$ of a standard deviation — a modest but not trivial association in human terms, the kind of magnitude one would want to weigh against the cost of the disclosure it represents, not just note as statistically distinguishable from zero. The estimate carries two stars: with a firm-clustered standard error of 0.061, the $t$-statistic is $0.18/0.061 \approx 3.0$, which a reader can confirm from the table without trusting my prose.

The story *across* the columns is the one the build-up is designed to tell. The raw bivariate association is 0.24; adding the firm characteristics that correlate with both ownership and disclosure pulls it to 0.21; absorbing firm and quarter fixed effects pulls it to 0.18. The coefficient shrinks by about a quarter from raw to saturated and then *holds* rather than collapsing toward zero. The honest reading: some of the raw correlation was confounding (bigger, more profitable firms both attract diversified owners and disclose more, which the controls and firm FE remove), but a stable association remains within firms once the obvious confounders are absorbed. That stability speaks to the *robustness of the number*; it is silent about whether the number is *causal*, the distinction Section 6 keeps in view.

The bottom block is the reality check. $N$ is constant at 13,800 across all three columns because no control is ever missing, so the leftward shrinkage reflects the added controls and fixed effects, not a quietly changing sample. The fit row reports the ordinary $R^2$ for the no-FE columns and the **within-$R^2$** for column (3), labeled as such: the within-$R^2$ of 0.034 says that *after* the firm and quarter intercepts absorb the large between-firm and between-quarter variation, common ownership and the controls explain about 3.4% of what is left. A small within-$R^2$ is normal and not damning on a noisy panel; headlining the inflated total $R^2$ (large simply because firms differ persistently) would be dishonest. The control coefficients pass an economic sanity check — bigger and more profitable firms disclose more — which is why I print them rather than bury them in a "Controls: Yes" row.

A final reading discipline: the 0.18 is a *within-firm* association. The firm fixed effects mean I am not claiming high-common-ownership firms disclose more than low-common-ownership ones (that between-firm comparison is confounded, and I make no claim about it); I am saying that *as a given firm's common ownership rises, its disclosure tends to rise too*, net of market-wide quarter shocks. That is the comparison the design supports, and the comparison the verb "associated with" describes.

### 6. Robustness

The robustness checks are organized around the threats of Table 2, in the same order, each introduced as an answer to a doubt rather than a context-free extra regression. Before each, I state what a pass would look like, so I cannot redefine "pass" after seeing the number. **All figures remain synthetic and illustrative.**

**Inference: does the result survive conservative clustering?** A reader might worry that firm clustering understates dependence if residuals are also correlated across firms within a quarter (a common flow shock). Pass criterion: the estimate stays distinguishable from zero under the most conservative defensible clustering. Two-way clustering by firm *and* quarter widens the standard error from 0.061 to about 0.072 (the coefficient is unchanged at 0.18), giving $t \approx 2.5$, still significant at 5%; industry clustering (30 clusters) gives SE near 0.078, $t \approx 2.3$. With only 30 clusters the asymptotics are thin, so the honest statement is that the result is *significant under every defensible clustering but with visibly wider intervals as I cluster more coarsely* — not bulletproof, but not fragile on inference either.

**Reverse causality: does lagging further change the story?** A reader might worry that funds buy firms *because* they disclose more, so the arrow runs outcome → regressor. Pass criterion: the association is similar when ownership is lagged two quarters, which a pure reverse-causality story would weaken. The two-quarter lag yields about 0.16 (SE 0.064), close to the one-quarter estimate. This *reduces* but does not eliminate the concern: if funds anticipate disclosure two quarters ahead, even the deeper lag is contaminated.

**Measurement: an artifact of one measure or the largest funds?** A reader might worry that portfolio-weighted CO is sensitive to the giant index managers or to the "who is one manager" aggregation. Pass criterion: a differently constructed measure and a sample without the largest funds give the same sign and similar magnitude. Replacing CO with a *count of common holders above a 1% stake* (re-standardized) gives about 0.15 (SE 0.058); dropping the five largest managers before building CO gives about 0.17 (SE 0.063). Both are a touch smaller, consistent with the attenuation measurement error predicts, and both keep the sign and significance.

**Industry-time shocks: do finer fixed effects kill it?** A reader might worry that an industry-wide event moves peers' ownership and a firm's disclosure together within a quarter. Pass criterion: adding industry × quarter fixed effects, which absorb any shock common to an industry in a quarter, leaves the coefficient distinguishable from zero. This yields about 0.14 (SE 0.066), $t \approx 2.1$ — the most demanding specification in the paper, smaller but surviving at 5%. That some of the association is absorbed here is itself informative: part of the relationship operates at the industry-quarter level, exactly where a peer-group mechanism would live.

**What does not survive — robustness is not identification.** Every check above shows the *number is stable*; none of them shows the *design is valid*. This is the distinction a sophisticated reader cares about most. I can re-cluster, re-measure, and add finer fixed effects all day, and a time-varying firm-specific confounder — a firm getting more transparent for its own reasons and thereby more attractive to diversified funds — would survive every one of these checks intact, because the bias would be baked into the within-firm variation the design relies on. The honest one-line summary: the result is *robust* in the sense that it does not depend on arbitrary analytic choices, and *not identified* in the sense that I cannot rule out the confounder that would make it non-causal. I therefore add a firm-specific linear time trend as the closest I can come to addressing that confounder; it leaves the coefficient near 0.16 (SE 0.067), which bounds — but does not eliminate — a smooth firm trend. A non-linear or coincident trend remains the threat I cannot dispatch.

Figure 1 summarizes the point estimate and its 95% confidence interval across the six specifications, so a reader can see the stability and the widening intervals at a glance.

**Figure 1 — Common-ownership coefficient across specifications (synthetic data; point estimate and 95% CI).**

```
spec                                    coef [95% CI]          0   0.1   0.2   0.3
(3) Firm & Quarter FE (headline)        0.18 [0.06, 0.30]           |---o---|
two-way clustered (firm & quarter)      0.18 [0.04, 0.32]          |----o----|
industry clustered                      0.18 [0.03, 0.33]          |----o-----|
two-quarter lag                         0.16 [0.03, 0.29]          |---o----|
alt. measure (count of common holders)  0.15 [0.04, 0.26]          |---o---|
+ industry × quarter FE                 0.14 [0.01, 0.27]         |----o----|
                                                                  +----+----+----+
```

*Notes.* **Synthetic, illustrative.** Horizontal bars are 95% confidence intervals; "o" marks the point estimate. The vertical reference is zero. Every interval excludes zero, but the intervals widen as clustering coarsens and as finer fixed effects absorb more variation — the visual statement of "robust on the number, with honestly wider uncertainty under the more demanding specifications." A figure like this would be exported to LaTeX from the analysis notebook, not hand-drawn; the ASCII rendering here stands in for the publication figure.

### 7. Conclusion

I built a firm-pair common-ownership measure from the structure of 13F institutional holdings and related it, in a fixed-effects panel, to firms' voluntary disclosure. The finding, stated in its properly hedged form: on a synthetic 13F-like panel, a one-standard-deviation increase in a firm's lagged common ownership with its product-market peers is *associated with* a disclosure index about 0.18 points higher — roughly 11% of a standard deviation — and this association is stable across the build-up of controls and fixed effects and across alternative clustering, ownership measures, and finer fixed effects. **The magnitudes are illustrative outputs of synthetic data and are not evidence about real markets.**

The limitations are the design's, not the data's, and they are the reason I never wrote "causes." Common ownership is chosen, not assigned: investors decide which firms to co-hold, and the same forces that draw them to co-hold two firms may independently drive those firms' disclosure. My firm and quarter fixed effects remove time-invariant firm traits and market-wide shocks, but they cannot remove a *time-varying, firm-specific* confounder — a firm becoming more transparent for its own reasons and thereby more attractive to diversified institutions. That confounder survives every robustness check in Section 6, because robustness is not identification: a stable number can still rest on an invalid assumption. The honest reading of this paper is therefore a *robust within-firm association consistent with the common-ownership-and-disclosure mechanism*, not the clean causal estimate a policy maker would need. Three further limits bound the claim: 13F shows long positions only (a "common owner" is a common *long* owner), the 45-day lag makes the measure a stale snapshot, and the "who is one manager" aggregation choice — which I made one way and tested another — is a modeling decision a different analyst could make differently.

What comes next is what would turn the association into an estimate. The natural extension follows Gao, Han, Kim & Pan (2024) in seeking a source of *plausibly exogenous* variation in common ownership — for example, a financial-institution merger that mechanically combines two managers' portfolios and so raises common ownership for reasons unrelated to either firm's reporting trajectory — and using it as the identifying lever rather than relying on within-firm timing. With real EDGAR or Thomson holdings and such a shock, the verb could climb from "associated with" to "causally estimate, under the assumption that the merger is unrelated to disclosure trends." A complementary extension would *swap the outcome* from voluntary disclosure to discretionary accruals — the supplier-firm earnings-management proxy the anchor paper actually uses — and re-run the same design, an exercise that converts this exemplar from a sibling-outcome variant into a closer methodological replication. This exemplar stops one rung below that, on purpose: its job was to show a camp reader how to build the measure, run the panel, report it to the Appendix-D standard, and keep every verb honest to what an observational design can bear.

---

### References

Bertrand, M., Duflo, E., & Mullainathan, S. (2004). How much should we trust differences-in-differences estimates? *Quarterly Journal of Economics*, 119(1), 249–275.

Gao, L., Han, J., Kim, J.-B., & Pan, T. (2024). Overlapping institutional ownership along the supply chain and earnings management of supplier firms. *Journal of Corporate Finance*, 84, 102520.

Petersen, M. A. (2009). Estimating standard errors in finance panel data sets: Comparing approaches. *Review of Financial Studies*, 22(1), 435–480.

---
---

## Margin commentary — "How this paper was built"

*This ~1,000-word commentary is the part a camp reader studies after the paper: it reverse-engineers the choices, so the exemplar teaches method and not just a model answer. It is written to Maya's advisor's voice.*

**Why the result is labeled synthetic in three places, not one.** The notice sits above the abstract, inside the abstract, in every table note, and in the figure note. That redundancy is deliberate and it is the single most important integrity move in the paper. A reader who lands on Table 3 from a search result, never having seen the front matter, must still learn — *from the table note alone* — that the numbers are instructional. Appendix D.2's "table stands alone" principle is usually about identification; here it is about honesty. A synthetic-data paper that labels itself only once is one screenshot away from being mistaken for evidence.

**Why "associated with" and never "causes."** The verb audit of D.5 is the spine of the whole paper. After drafting, I read only the verbs attached to the 0.18 coefficient — in the abstract, the intro's "we find," the results, and the conclusion — and forced each down to the level the weakest assumption permits. The weakest assumption is that within-firm timing of ownership changes is unrelated to disclosure shocks, and I openly do not believe it holds, so the ceiling is "associated with." The temptation to let the verb drift upward in the conclusion (D.5's "drift") is exactly what the conclusion's hedged restatement guards against. Notice the *contribution sentence* in §1 claims the "document a robust association" job from Ch 8.3 §3, not the "first causal estimate" job — because the design earns the former and not the latter, and claiming the wrong job is the fastest route to a referee's contempt.

**Why the columns build parsimonious → saturated, and why $N$ is constant.** Table 3 is built to D.2 §4: column (1) is the raw bivariate, (2) adds the confounding controls, (3) adds the fixed effects I most believe. Reading the key coefficient leftward (0.24 → 0.21 → 0.18) lets the reader *see* how much of the raw correlation was confounding and how much survives. The constant $N = 13{,}800$ across all three columns is not decoration: it certifies that no control is silently missing for some firms, so the coefficient's movement is about the controls, not a shifting sample (D.1 §5, the silent-sample-change trap). I planted the controls to be correlated with both ownership and disclosure precisely so the build-up would be informative — a bivariate that equals the saturated estimate would have taught nothing.

**Why the within-$R^2$ is labeled and small.** Column (3) reports a within-$R^2$ of 0.034, not an ordinary $R^2$. D.2 §2 calls the unlabeled FE $R^2$ the most common student error: a two-way FE model's total $R^2$ is mechanically huge (firms differ persistently) and says nothing about the regressor. The within-$R^2$ — variance explained *after* the fixed effects absorb the between-group variation — is the honest fit statistic, and a small one on a noisy panel is respectable, not embarrassing. Labeling the row "Within $R^2$" so the reader is never guessing is the whole discipline.

**Why clustering gets its own subsection.** Section 4.2 exists because the paper is panel data and Petersen (2009) is the load-bearing methods cite. The default — cluster by firm, the level where within-unit dependence is strongest — is stated and defended, and the robustness section then *stress-tests inference itself*, reporting how the interval widens under two-way and industry clustering. That move separates the two questions D.3 §5 insists on keeping apart: re-clustering tests *inference*, not the *design*. The honest sentence "significant under every defensible clustering but with visibly wider intervals as I cluster more coarsely" is calibration, not salesmanship — it neither overclaims bulletproof-ness nor hedges into mush.

**Why the threats table has no blank residual column.** D.3 §2 is blunt: a blank "residual concern" is a tell, not a triumph. Every row of Table 2 carries leftover doubt, and the most dangerous one — the time-varying firm-specific confounder — is the one the fixed effects *cannot* kill. The robustness section then says so explicitly under "robustness is not identification," which is the most sophisticated move in the paper: a stable number can rest on an invalid assumption, and pretending otherwise is the error a Week-5-trained reader catches instantly. The firm-trend check is offered as the *closest* approach to that confounder, not a defeat of it.

**Why the data section respects 13F's real limits even on synthetic data.** The long-only, 45-day-lag, and "who is one manager" caveats come straight from the data cards, and they are not ornamental: each one bounds what the measure can mean (a common *long* owner; a stale snapshot; an aggregation choice). Building the synthetic schema to mirror the EDGAR information table means the measure-construction code would run unchanged on a real pull — the recipe is real even though the bytes are not. The CUSIP-licensing caveat is why the synthetic data invents identifiers rather than borrowing real ones.

**Why citations are now fully verified.** Per CONVENTIONS §6 and D.5.4, a citation I cannot verify to the page is flagged, never fabricated. The Gao, Han, Kim & Pan (2024) author list, title, venue, volume, and article number (*JCF*, 84:102520) are taken verbatim from the published version against Prof. Gao's CV anchor list — note that the *published* title is "Overlapping institutional ownership along the supply chain and earnings management of supplier firms," which differs from the working-paper title some earlier internal drafts carried; the published title is the citation of record. The Petersen (2009) page range *RFS* 22(1), 435–480 and the Bertrand–Duflo–Mullainathan (2004) range *QJE* 119(1), 249–275 are likewise verified against the journal listings. A visible `[CHECK]` is a flag of honesty when verification has not yet happened; a confidently fabricated page number is the one error a referee never forgives. The lesson for the camp reader: when you do not know, mark the hole — do not fill it with a plausible guess.
