# Capstone 4 — Reading the Tape: An Out-of-Sample-Validated Text Classifier for SEC 8-K Events and the Short-Window Return Reaction

> **ASSIP framing — read first.** *The ASSIP 2026 terminal deliverable is a research poster
> (~48"×36") + a JSSR abstract (200–300 words) + an 8-minute poster talk + a replication packet
> — not a full paper.* This exemplar is the **full research narrative the poster summarizes**: a
> complete AI/text-as-data paper written one level above the ASSIP graded artifact, so you can
> see what the full validation-discipline argument looks like before you compress it onto six
> poster panels (question · why · design+validation · headline · robustness · contribution-
> and-limits) and a 10-sentence JSSR abstract. The full validation table (precision/recall/F1 by
> class, Cohen's κ) belongs on the poster's design panel; the full prompt-disclosure belongs in
> the replication packet the QR code points to.
>
> **Exemplar capstone paper.** *Author voice:* Leah Okonkwo (student). Modeled on the empirical-paper structure of Chapter 8.3 and built to the Appendix-D table and prose standards. Read it as a template you can adapt, then read the annotated "How this paper was built" commentary at the end, which narrates every design choice and every place the discipline of Chapter 6.5 bit.

---

> **ILLUSTRATIVE / SYNTHETIC RESULTS — READ FIRST.** Every number in this paper is synthetic. The 8-K text snippets and the returns are *constructed for instruction* in the Week 6 AI co-pilot lab (`nb6.5`), not pulled from live EDGAR filings or CRSP, and the classifier was validated against a 45-document hand-labeled teaching set, not a research-scale corpus. The validation figures (macro-F1 ≈ 0.86, Cohen's κ ≈ 0.80) and the return-reaction figures are **not empirical findings** and must not be cited as facts about real markets. The paper exists to show *the form of a correct argument* — how to validate a text classifier out-of-sample, address training-data leakage, and study a return reaction honestly — not to report a result. Where a real submission would carry a verified citation, an unverifiable one is tagged `[CHECK]`.

---

## Abstract

The SEC's 8-K is the market's "something just happened" signal: firms disclose material events — an earnings release, an executive departure, a completed acquisition — usually within four business days, on a sharply timestamped public filing. We ask whether the *type* of event an 8-K reports can be recovered from its text by a validated classifier, and whether the short-window return reaction differs across recovered event types. Treating the classifier as a *measurement instrument* rather than an oracle, we hand-label a random gold set, freeze a four-class rubric against a held-out test split *before* looking at any returns, and report out-of-sample precision, recall, and F1 by class plus Cohen's κ. On the synthetic teaching corpus the classifier reaches a macro-F1 of 0.86 and κ of 0.80 — accurate enough to use, imperfect enough to matter. On a market-model event study, earnings 8-Ks carry the largest average absolute three-day cumulative abnormal return and executive-departure 8-Ks a negative average reaction, while "other" (Item 8.01) filings move prices least. Our marquee threat is training-data leakage: because the task is *contemporaneous* (what event does this text describe?) not *predictive* (will this stock rise?), leakage is contained but not eliminated, and we address it explicitly. We read the patterns as associations consistent with information content, not causal effects, and disclose every prompt, model version, and validation number so the measurement can be audited. **(All results synthetic; see `nb6.5`.)**

---

## 1. Introduction

On October 18, 2023, a firm filed an 8-K at 4:05 p.m. Eastern whose Item 2.02 pointed to Exhibit 99.1, a quarterly earnings release; within minutes the stock moved several percent. Two days later the same firm filed an Item 5.02 8-K — a single paragraph announcing its CFO would step down — and the market reacted again, in the opposite direction. Both filings are public, free, and machine-readable the instant they post, both timestamped to the minute. What separates them — the *kind* of news each carries — lives in the text. This paper asks whether a machine can read that text reliably enough to study how prices respond to different kinds of corporate news, without fooling the researcher into mistaking a fluent guess for a measurement.

That is harder than it looks, for the reason Chapter 6.5 hammers: a label a model assigns is *not* the truth, it is a noisy proxy, and a proxy never calibrated against hand-coded ground truth is a confident guess in the costume of data. The temptation — type "classify these filings by event type," paste the output into a spreadsheet, run a regression — is exactly the failure. If the classifier mislabels even ten percent of filings and the error correlates with anything (it reads ambiguous restructurings as "earnings," say), every downstream return comparison is contaminated by measurement error of unknown sign; and because the labels depend on the *prompt*, a researcher can rewrite the rubric until the reaction comes out "significant" — p-hacking through a door that did not exist before language models.

**This paper's contribution is methodological as much as empirical: we provide a worked, fully-disclosed protocol for using a text classifier as a validated measurement instrument in an event study — hand-labeling a random gold set, freezing the rubric against a held-out test split before any returns are examined, reporting out-of-sample precision/recall/F1 and Cohen's κ, and auditing the marquee threat of training-data leakage — and we apply it to recover SEC 8-K event types and study their short-window return reactions.** The contribution is the *discipline*, demonstrated end to end; the return patterns illustrate what that discipline lets you claim — and, on this synthetic corpus, only what it lets you claim.

We find three things. First, the classifier is usable but not perfect: on the held-out test set it reaches a macro-F1 of 0.86 and Cohen's κ of 0.80 against hand labels, with the weakest class — executive changes — at recall 0.78, a gap large enough that we report what that miss does downstream rather than bury it. Second, on a market-model event study the average absolute three-day cumulative abnormal return (CAR) is largest for earnings 8-Ks (about 3.1 points), signed-negative for executive-departure 8-Ks (mean CAR ≈ −1.4 points), and smallest for "other" (Item 8.01) filings (near zero) — consistent with the market pricing the *information content* an event type carries. Third, these are associations, not causal effects: even our weaker-than-causal assumption is threatened by confounding contemporaneous news, which we cannot rule out and do not pretend to. **All figures are synthetic teaching values; see `nb6.5`.**

The rest of the paper proceeds as Chapter 8.3 prescribes. Section 2 positions the work between the Loughran–McDonald dictionary tradition and the LLM/text-as-data thread; Section 3 describes the data; Section 4 lays out the classifier *and its validation*, then the event-study design and identifying assumption; Section 5 leads with the two headline tables; Section 6 reports robustness; Section 7 concludes with honest limits and the responsible-AI-use disclosure.

---

## 2. Positioning in the literature

Two strands of work meet in this paper, and the gap we occupy is the seam between them.

The first strand is the **finance text-as-data tradition that begins with dictionaries**. Loughran and McDonald (2011) is the foundational reference and the cautionary tale at once: the general-purpose Harvard psychosocial dictionary, applied to 10-Ks, miscounts ordinary accounting vocabulary ("liability," "tax," "cost," "capital") as negative sentiment, while a finance-specific word list both fits the language better and relates more cleanly to market reactions around filings. The durable lesson is not the word list but the *epistemology*: a text measurement is valid only to the extent it has been checked against an external criterion, and an instrument calibrated for one domain does not transfer to another without re-validation. We inherit that validation discipline while moving past the bag-of-words blindness to context that counts "not a good quarter" as positive because it sees "good" and never the negation.

The second strand is the **modern text-as-data and LLM thread** that puts context back in. Word embeddings (the cosine-similarity geometry of Hoberg and Phillips (2016) and the word2vec/GloVe line) represent a word by the company it keeps; transformer models and LLMs represent a word as a function of the whole sentence, so negation and long-range dependence become at least partly learnable. The promise for event classification is obvious — an LLM can read "our chief financial officer has informed the Board of her intention to retire" and assign "executive change" without the literal Item number — and so is the peril Chapter 6.5 catalogues: fluent fabrication, prompt-induced p-hacking, irreproducible stochastic outputs, and the marquee finance threat, training-data leakage, in which a model trained through some cutoff "knows" the future relative to a backtest sample.

The hole we fill is the seam between the strands. The dictionary literature has the validation discipline but not the contextual power; the LLM literature has the power but, in much applied practice, *not the validation discipline* — labels flow into regressions un-audited. We do not claim to be first to classify 8-Ks (the SEC's Item-numbering is itself a coarse label, and 8-K event studies are long established; for the event-study machinery we follow the standard market-model framework of MacKinlay (1997)). What we contribute is the *intersection*: a contextual classifier whose labels are treated as a measurement to be validated out-of-sample, with the leakage audit and full prompt disclosure an LLM-era event study requires and applied work too often skips.

---

## 3. Data

**The filings.** Our unit of observation is a single 8-K, identified by its accession number (a firm files many 8-Ks a year, so "the 2023 8-K" is never a valid reference). The 8-K is organized by numbered Items: Item 2.02 (earnings release), Item 5.02 (departure/appointment of directors and officers), Item 1.01 (material agreement), Item 2.01 (completed acquisition), Item 8.01 (other events). We collapse the event space into four analysis classes — **earnings**, **executive change**, **material agreement / acquisition**, and **other** — because finer distinctions blur in the text and the four-way split is where the return reaction plausibly differs. Two construction facts from the data card drive the pipeline. First, **earnings releases hide in Exhibit 99.1**: the body of an Item 2.02 8-K is often a one-line pointer to the exhibit, so we classify on the exhibit text where present. Second, **boilerplate dominates a naive reading**: the "furnished, not filed" disclaimer and forward-looking safe harbor repeat across firms and would swamp a bag-of-words model, so we strip them first.

> **Synthetic-data note.** The corpus is the 45-document hand-labeled teaching set built in `nb6.5`: short, realistic 8-K *snippets* spanning the four classes with deliberate boundary cases (a restructuring that mentions earnings; an Item 8.01 filing announcing a buyback). A real Capstone 4 would pull live EDGAR filings under the fair-access rule (a `User-Agent` naming the researcher, under 10 requests/second) and would face the multi-label problem — one 8-K can carry Items 2.02 *and* 9.01 — which we sidestep here by labeling each snippet's dominant event. The smallness of the gold set is the binding constraint on every confidence interval below.

**The returns.** The event study needs a return series around each filing date. In a real submission these come from CRSP daily returns (a pinned snapshot per CONVENTIONS §5, licensed data staying on GMU infrastructure) with a value-weighted market index. Here the returns are synthetic series constructed in `nb6.5` so the four event types carry *different* information content by design — which is precisely why the return-reaction table is not evidence about real markets. It demonstrates that the *pipeline* produces a coherent answer, not a finding.

A subtlety the data card flags: **filing-time versus event-time.** The 8-K must be filed within four business days of the event, so the filing date can lag the event. Centering the window on the filing date — the sharp machine-readable timestamp — risks missing a reaction that already happened on the event date. We treat this look-ahead-adjacent issue in the threats table (§4) and robustness (§6).

---

## 4. Methods

The methods come in two halves. The first builds the *measurement instrument* — the classifier — and validates it out-of-sample, because an uncalibrated label is not data. The second is the *event study* using the validated labels. We present them in that order deliberately: the classifier is frozen against the gold set *before* any return is examined, so the downstream result cannot have shopped for the prompt.

### 4.1 The classifier

We classify each filing into one of four event types using the provider-switch design of `nb6.5`: the same rubric runs through a local model (TF-IDF/logistic-regression, or a small local LLM via Ollama for licensed text that may not leave GMU infrastructure), the Anthropic Messages API, or a GMU Azure OpenAI deployment, with the model identity logged on every call. The classification logic is a **rubric** — an explicit decision rule with boundary cases named, as Chapter 6.5 Pattern 4 prescribes — because consistency across documents *is* the measurement: a classifier using a different definition of "earnings" on document 40 than document 4 has injected noise. The full rubric is in Appendix A; its skeleton:

```text
You are classifying the PRIMARY event type reported in an SEC 8-K
filing (or its Exhibit 99.1). Assign exactly one label:

  EARNINGS   — reports results of operations / a quarterly or annual
               earnings release (typically Item 2.02 / Exhibit 99.1).
  EXEC_CHANGE— reports the departure, appointment, or retirement of a
               director or principal officer (typically Item 5.02).
  AGREEMENT  — reports entry into a material agreement or the
               completion of an acquisition (typically Item 1.01/2.01).
  OTHER      — any other event, including Item 8.01 "other events."

Rules:
- Judge only the text provided. Do not use outside knowledge about
  the company or what happened to its stock.
- Boilerplate ("furnished, not filed"; forward-looking safe harbor)
  carries no event information; ignore it.
- If a filing reports multiple events, label the one given the most
  textual emphasis. If genuinely ambiguous, choose OTHER.

Return only the label word.
```

Three design choices follow Chapter 6.5 directly. The stable rubric goes first and the volatile filing text last, so the rubric can be prompt-cached and — more importantly — so *every* document is judged by identical instructions. The "do not use outside knowledge about what happened to its stock" clause is a leakage guard written into the prompt (§4.4). And the ambiguous-case default ("choose OTHER") stops the model coin-flipping on boundary cases, which would inject exactly the random measurement error we are trying to bound.

### 4.2 The validation protocol — the measurement, not the truth

This is the heart of the paper: we treat the classifier's output as a measurement and validate it against a hand-labeled gold standard, out-of-sample, before it goes near a return.

**Step 1 — Build a gold set by hand.** We draw a *random* sample and label each document by hand against the rubric. In `nb6.5` this is the full 45-document teaching set; a real study would use ≥200, with two coders labeling independently and reconciling disagreements (the disagreement rate itself estimates how hard the task is for humans). The draw must be random — a gold set of easy cases flatters the classifier and lies about field performance.

**Step 2 — Split the gold set.** We stratify-split into a **development set** (used to write and tune the rubric) and a **held-out test set** *not examined* during rubric development — the same train/test discipline as any predictive task, for the same reason: a rubric tuned until it nails the examples it is measured on reports optimistic garbage. The test set is touched once, after the rubric is frozen.

**Step 3 — Confusion matrix and per-class metrics.** Cross-tabulating the frozen classifier's predictions against hand labels (a 4×4 confusion matrix), we compute, *per class*,

$$
\text{Precision} = \frac{TP}{TP+FP}, \qquad \text{Recall} = \frac{TP}{TP+FN}, \qquad F_1 = 2\cdot\frac{\text{Precision}\cdot\text{Recall}}{\text{Precision}+\text{Recall}},
$$

then the **macro-average** of F1. We report precision and recall by class, never bare accuracy, because event corpora are imbalanced — earnings 8-Ks common, completed acquisitions rare — and accuracy lies under imbalance: a classifier labeling everything "earnings" posts high accuracy and is useless on the rare classes we most need.

**Step 4 — Cohen's κ.** Accuracy and F1 ignore the agreement you would get *by chance*. **Cohen's κ** corrects for it: with $p_o$ the observed agreement and $p_e$ the agreement expected if both labeled at random with the same marginals,

$$
\kappa = \frac{p_o - p_e}{1 - p_e}.
$$

κ = 1 is perfect, κ = 0 is chance-level, and κ above roughly 0.8 is conventionally "almost perfect" — the Landis & Koch (1977) bands are 0.81–1.00 "almost perfect," 0.61–0.80 "substantial," 0.41–0.60 "moderate," 0.21–0.40 "fair," and below 0.20 "slight" (*Biometrics* 33(1), 159–174). It is the honest summary of whether the classifier agrees with a human for real reasons or by lucky base rates.

**Step 5 — Freeze, then report with uncertainty.** The reported numbers are computed on the held-out test set *once*, after the prompt is frozen against the development set. Because the gold set is small, every metric carries a wide interval, which we obtain by a stratified bootstrap (resample the test set, recompute each metric) and report alongside the point estimate. A precision of 0.83 on a handful of predicted-positives is not the evidence that 0.83 on a thousand is, and the interval says so.

### 4.3 The event study

With labels frozen and validated, we run a textbook market-model event study (MacKinlay 1997). For filing $i$ on filing date $\tau=0$, we estimate the market model on a pre-event **estimation window** ($\tau \in [-120, -11]$),

$$
R_{i\tau} = \alpha_i + \beta_i R_{m\tau} + \varepsilon_{i\tau},
$$

with $R_{i\tau}$ firm $i$'s return and $R_{m\tau}$ the market return. The **abnormal return** is realized minus model-predicted, $AR_{i\tau} = R_{i\tau} - (\hat\alpha_i + \hat\beta_i R_{m\tau})$, and the **cumulative abnormal return** over the short window is $CAR_i = \sum_{\tau=-1}^{+1} AR_{i\tau}$. Our outcome is $CAR_i$ (and its absolute value $|CAR_i|$, the reaction magnitude regardless of direction); the key regressor is the *classified event type* from §4.1. We compare mean $CAR$ and mean $|CAR|$ across the four classes, clustering standard errors by firm (a firm filing several 8-Ks contributes correlated reactions) — the CONVENTIONS §3 discipline of naming the SE flavor every time.

### 4.4 The identifying assumption and threats

**Specification, in CONVENTIONS §4 form.** *Outcome:* the three-day filing-window CAR (and $|CAR|$). *Key regressor:* the validated event-type label. *Controls:* none in the headline (a controlled version in robustness). *Fixed effects:* none in baseline; firm and calendar-month FE in robustness. *Clustering:* by firm. *Sample:* the classified 8-K corpus. *Identifying assumption (one sentence):* **conditional on the classifier being a valid measurement of event type, the average reaction within each class reflects that event type's information content and is not systematically driven by another event in the same three-day window or by label error correlated with returns.** This is deliberately *not* causal — we randomize nothing — it is the weaker claim that the cross-class differences are about the events, not contamination. Even that has threats, named below rather than waved at.

The marquee threat is **training-data leakage**, the fatal finance-specific trap of Chapter 6.5. An LLM is trained through a cutoff date; if our sample predates it, the model may have *read* what happened to these stocks. The distinction that contains the threat: our task is **contemporaneous, not predictive** — "what event does this text describe?" is answerable from the filing alone, unlike "will this stock rise?", which requires knowing the future. Labeling a 2019 filing's *event type* needs no knowledge of 2019's returns, so leakage into the *label* is far less dangerous than into a *prediction*. But "far less" is not "none," and three residual channels remain: (1) the model could lean on memorized outside knowledge rather than the text — suppressed by the rubric's "judge only the text, no outside knowledge" clause and probed in §6 by masking identifying details; (2) the *returns* could leak if the model saw them — it does not, and the audit log proves it saw only filing text; (3) if memorized outcomes shifted the label on ambiguous cases (calling a restructuring "earnings" because the firm beat estimates), label error would correlate with returns — the one channel that could bias the CAR comparison, which §6's leakage-masked re-label measures. The cleanest defense, which a real study should add, is validation on filings created *after* the model's cutoff.

The second threat is **confounding contemporaneous news**: the three-day window can catch a reaction to something *other* than the 8-K — a same-day downgrade, a sector shock, a different filing. The market model strips out market-wide co-movement but not firm-specific contemporaneous news. We cannot rule this out; it is the leading reason the comparison is an association, not a causal effect, and our verbs say so throughout.

| Threat | Why it could break the claim | Design feature / response | Residual concern |
|---|---|---|---|
| **Training-data leakage** | Model "knows" the future of the sample; could shift labels on ambiguous cases, correlating label error with returns | Task is *contemporaneous* (event type), not *predictive*; rubric forbids outside knowledge; audit log proves model saw only filing text; leakage-masked re-label in §6 | Cannot fully exclude memorized outcomes biasing ambiguous labels; ideal fix is post-cutoff validation |
| **Label measurement error** | A misclassified event puts its return in the wrong class, blurring or biasing the comparison | OOS precision/recall/F1 + κ reported; classes with weak recall flagged; bootstrap CIs | At κ ≈ 0.80, ~1-in-7 labels disputable; attenuates and could bias cross-class gaps |
| **Confounding contemporaneous news** | A same-window event (downgrade, sector shock) drives the CAR, not the 8-K | Market model removes market-wide co-movement; firm clustering; tight 3-day window | Firm-specific same-day news not removed; the reason this is association, not causation |
| **Filing-time vs. event-time** | Reaction already occurred on the (earlier) event date, missed by a filing-date window | Window centered on the sharp filing-date timestamp; robustness widens to $[-1,+5]$ and reads body event dates | Some pre-filing reaction unobserved for lagged filings |
| **Prompt-induced p-hacking** | Researcher rewrites rubric until the return comparison turns "significant" | Rubric frozen against the gold set *before* returns examined; gold-set F1, not the regression, decides the prompt; rubric disclosed verbatim (App. A) | Honesty rests on the freeze being real; pre-registration would harden it |
| **Stochastic irreproducibility** | Re-running the LLM yields different labels, so results do not replicate | Labels run once and saved to disk as data; model version string pinned and logged; provider/version in App. A | Frontier models are not bit-for-bit deterministic even at fixed settings |

---

## 5. Results

We lead with the two headline tables, as Chapter 8.3 §5 requires: first the **validation table** (is the instrument good enough to use?), then the **return-reaction table** (what does it show?). The order is not cosmetic — a return table read before the validation table is a number with no error bar on its key regressor.

### 5.1 The validation table

Table 1 reports the out-of-sample performance of the frozen classifier on the held-out test set, by class and macro-averaged.

**Table 1 — Out-of-sample classifier validation against the hand-labeled gold standard**

| | Precision | Recall | F1 | Support (test) |
|---|---:|---:|---:|---:|
| Earnings | 0.92 | 0.94 | 0.93 | 6 |
| Executive change | 0.84 | 0.78 | 0.81 | 4 |
| Agreement / acquisition | 0.86 | 0.85 | 0.85 | 4 |
| Other (Item 8.01) | 0.83 | 0.86 | 0.84 | 4 |
| **Macro average** | **0.86** | **0.86** | **0.86** | **18** |
| Cohen's κ | | | **0.80** | |

*Notes.* All values **synthetic**, from the `nb6.5` teaching corpus; **not empirical findings.** The reported quantity is the agreement between the frozen four-class classifier and hand labels on the **held-out test split** (18 documents) of the 45-document gold set, drawn at random and not examined during rubric development. Precision, recall, and F1 are defined per class in §4.2; the macro average is the unweighted mean of per-class F1. Cohen's κ adjusts observed agreement for chance. "Support" is the number of test documents with that gold label; the tiny support drives wide bootstrap intervals (95% CI on macro-F1 ≈ [0.74, 0.93]; on κ ≈ [0.64, 0.90] — illustrative). Reported once, after the rubric was frozen. Model version, provider, and full rubric in Appendix A.

Read Table 1 as a referee would. The macro-F1 of 0.86 and κ of 0.80 say the classifier agrees with a human reader for real, chance-adjusted reasons — a *usable* instrument. But it is not flawless, and the table refuses to hide its weakest point: **executive change** has the lowest recall, 0.78, so roughly one departure filing in five is *missed*, read as something else (usually "other") when buried in a longer filing. This matters downstream: if executive-change filings are systematically missed, their reaction is diluted by the milder "other" reactions absorbing them, *attenuating* that class's CAR toward zero — so the return-table number below is a conservative estimate, and the reader should carry that caveat. The wide bootstrap intervals are the other honest signal: with only four executive-change test documents, the 0.78 recall could plausibly run from the high 0.4s to the low 0.9s, and a ≥200-document gold set would tighten this enormously. The table earns its independence — a stranger reading only it knows the instrument's accuracy, its weakest class, and how uncertain both are.

### 5.2 The return-reaction table

With the labels established as a defensible measurement, Table 2 reports the short-window return reaction by classified event type.

**Table 2 — Three-day filing-window return reaction by classified 8-K event type**

| | (1) Mean CAR[−1,+1] | (2) Mean \|CAR\|[−1,+1] | (3) Mean CAR, + controls |
|---|---:|---:|---:|
| Earnings | 0.41 | 3.08\*\*\* | 0.38 |
| | (0.55) | (0.39) | (0.57) |
| Executive change | −1.42\*\* | 1.96\*\*\* | −1.31\* |
| | (0.61) | (0.44) | (0.68) |
| Agreement / acquisition | 1.18\*\* | 2.21\*\*\* | 1.05\* |
| | (0.52) | (0.41) | (0.55) |
| Other (Item 8.01) | −0.07 | 0.74\* | −0.05 |
| | (0.33) | (0.30) | (0.34) |
| Firm & month controls | No | No | Yes |
| SE clustering | Firm | Firm | Firm |
| $N$ (filings) | 45 | 45 | 45 |

*Notes.* All values **synthetic**, from the `nb6.5` teaching corpus; **not empirical findings.** The dependent variable is the three-day cumulative abnormal return $CAR_{[-1,+1]}$ in **percentage points**, from a market model estimated over $[-120,-11]$ (§4.3); column (2) uses its absolute value $|CAR|$, the reaction magnitude regardless of sign. The "key regressor" is the validated event-type label from Table 1; cells report the class mean (a regression of CAR on event-class indicators with no constant), with standard errors clustered by firm in parentheses. Column (3) adds firm size and calendar-month fixed effects. Returns rescaled to percentage points for legibility. \*\*\* $p<0.01$, \*\* $p<0.05$, \* $p<0.10$. Because event labels carry measurement error (Table 1: macro-F1 0.86, κ 0.80), every coefficient is a *mismeasured-regressor* estimate, attenuated toward the cross-class mean; the executive-change row in particular is biased toward zero by that class's 0.78 recall.

The economic reading, in associational verbs because that is all the design earns. The **magnitude** column (2) is the cleanest: the average absolute reaction is largest for **earnings** (3.08 points), where the market digests a quantitative surprise, and smallest for **other** (0.74 points), where the median Item 8.01 event carries little price-relevant information — the ordering one expects if the classifier is recovering real information content, and the synthetic corpus's intended signal. The **signed** column (1) adds that executive-change filings carry a *negative* average CAR (−1.42), consistent with unplanned departures reading as bad news, while agreement/acquisition filings are *positive* (+1.18). Both survive the firm-and-month controls in column (3) with only slight attenuation (−1.31, +1.05), mild reassurance they are not driven by firm-size composition or calendar clustering. But — and here the validation table does its work on the return table — the executive-change coefficient is the *least* trustworthy precisely because that class is identified worst (recall 0.78), so its true magnitude is plausibly *larger* in absolute value than −1.42, the miss having diluted it. We do not claim these events *cause* the returns; we document that, *through a validated-but-imperfect classifier and net of market co-movement*, the short-window reaction differs across recovered event types in the direction information content predicts — an association we cannot cleanly separate from confounding same-window news (§4.4).

---

## 6. Robustness

Following Appendix D.3, we organize robustness around the threats of §4.4, each subsection answering one named doubt.

**Cross-provider re-labeling (model-quirk threat).** A result holding only under one model's idiosyncrasies is an artifact. We re-label the whole corpus with a *different* vendor's model (the GMU Azure OpenAI deployment in place of the Anthropic model), identical frozen rubric, and recompute Table 2. The two label columns agree on 41 of 45 documents (cross-model κ ≈ 0.85), and the reaction ordering is unchanged: earnings largest in magnitude, other smallest, executive change negative. Stability across vendors is real evidence — on these synthetic data — that the result is about the documents and rubric, not one model's quirks. The four disagreements are all boundary cases (a restructuring; a buyback in an Item 8.01), exactly the documents the "if ambiguous, choose OTHER" rule governs.

**Leakage-masked re-label (leakage threat).** To probe the one leakage channel that could bias the CAR comparison — the model leaning on memorized outcomes — we re-run the classifier with firm names, tickers, and dates masked, so it has only anonymized event language. If labels barely move, the model read the text, not its memory. The masked labels agree with the original on 43 of 45 documents and Table 2's ordering is unchanged, consistent with the contemporaneous task being leakage-resistant. This is a *probe*, not a proof: the airtight version validates on post-cutoff filings.

**Window width (filing-time-vs-event-time threat).** Because the filing can lag the event by up to four business days, a reaction may begin before $\tau=0$. Widening the window to $[-1,+5]$, and separately re-centering on body event dates where present, leaves the cross-class *ranking* — the object of the claim — unchanged; absolute CARs rise modestly with the wider window as more noise accumulates.

**Alternative inference.** Clustering by firm rather than treating filings as independent widens the standard errors, as the table reflects; the earnings and acquisition magnitude effects survive, while the executive-change signed effect drops from two stars to one under the most conservative clustering, which we report rather than suppress. Significance is not importance: the −1.4-point executive-change reaction is economically meaningful whichever side of the 5% line its t-statistic lands on, and the prose carries that, not the stars.

What does *not* survive scrutiny, plainly: we have no defense against firm-specific contemporaneous news in the window, and on a 45-document synthetic corpus every interval is too wide for a confident magnitude claim. Real limits, not rhetorical modesty.

---

## 7. Conclusion

We set out to show, end to end, how to use a text classifier as a *validated measurement instrument* in a finance event study. The contribution is the protocol: hand-label a random gold set, freeze a rubric against a held-out test set *before* any return is examined, report out-of-sample precision/recall/F1 and κ by class, audit training-data leakage explicitly, and disclose every prompt and model version. On the synthetic corpus the classifier reached a macro-F1 of 0.86 and κ of 0.80 — accurate enough to use, imperfect enough that we reported what its weakest class (executive change, recall 0.78) does downstream rather than hiding it — and the validated labels recovered a reaction ordering (earnings largest in magnitude, "other" smallest, executive change negative, acquisitions positive) consistent with information content.

**Honest limits.** First and most important, *all results here are synthetic teaching values and must not be read as findings about real markets.* Second, even taking the pipeline at face value, the claim is associational, not causal: we cannot rule out firm-specific contemporaneous news driving the three-day reaction. Third, label error at κ ≈ 0.80 leaves roughly one label in seven disputable, attenuating the comparisons and biasing the worst-identified class (executive change) toward zero. Fourth, the leakage audit is a probe, not a proof — the airtight defense is validation on post-cutoff filings, which we did not do. Fifth, the 45-document gold set is far too small for confident magnitudes; a real study needs ≥200 hand labels with two coders.

**What comes next.** The natural extension is the multi-label problem the data card flags — one 8-K can carry Items 2.02 *and* 9.01 — which our single-label collapse sidesteps and a richer study should model directly; the cleanest leakage defense is a sample drawn entirely after the model's cutoff. The obvious next question, which this paper opens but does not close, is whether the *text content within* an event type (a more- versus less-negative earnings release, scored by the Loughran–McDonald dictionary) predicts the *sign and size* of the reaction beyond the event type alone — where the dictionary and LLM traditions would finally be compared head to head.

### Responsible-AI-use disclosure (per Chapter 6.5 §6.5.7)

**Where AI was used.** An LLM was used as a *data-generating* instrument — assigning the four-class event label to each filing — the subject of the validation in §4.2 and Table 1. An LLM was *also* a *writing and code aid* (drafting prose, reviewing event-study code); the author owns every word kept and line run, that use generated no data. The two uses are kept distinct, as the checklist demands: the first is validated, the second merely owned.

**Models and versions.** The labels in this exemplar are synthetic, produced by the `nb6.5` local pipeline (TF-IDF + logistic regression with a keyword backstop) standing in for an LLM; the real-API paths (Anthropic Messages API, model `claude-opus-4-7`; GMU Azure OpenAI deployment) are present but gated and not executed for these numbers. A real submission states the exact model *version string(s)*, provider(s), and date range of calls, and pins the API version (the GMU Azure `api_version` and deployment name are `[CHECK]` in `nb6.5` pending confirmation against the N1 AI portal).

**Validation.** The out-of-sample precision/recall/F1 and κ against the hand-labeled gold set are in Table 1, with gold-set size (45) and held-out test size (18) stated, per-class metrics reported (never bare accuracy), and the labeling procedure described (§4.2).

**Reproducibility.** Labels were generated *once* and saved to disk as data — the analysis never re-queries the model — so the pipeline is reproducible even though frontier LLMs are not bit-for-bit deterministic (some, including Opus 4.7, do not expose a `temperature` parameter; §6.5.5). Every API call is logged one-JSON-line-per-call (model version, prompt hash, token counts); the full rubric is in Appendix A.

**Integrity.** The rubric was frozen against the gold set *before* the returns were examined, foreclosing prompt-induced p-hacking; that freeze is the load-bearing honesty of the paper, and a real study would harden it with a dated pre-registration. Every citation that could not be verified is tagged `[CHECK]` rather than fabricated, per CONVENTIONS §6.

---

### Appendix A — Classification rubric (verbatim) and model log

*The full four-class rubric run on every document is reproduced in §4.1; the production version adds three labeled boundary examples per class. The provider-switch configuration, the JSONL audit-log schema (timestamp, model version string, SHA-256 prompt hash, input/output token counts, `cache_read_input_tokens`), and the frozen label file live in `nb6.5`. Model IDs, the GMU Azure `api_version`, and the deployment name are tagged `[CHECK]` in the notebook pending confirmation against GMU's N1 AI portal.*

### References

- Loughran, T., & McDonald, B. (2011). When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks. *Journal of Finance*, 66(1), 35–65.
- Hoberg, G., & Phillips, G. (2016). Text-Based Network Industries and Endogenous Product Differentiation. *Journal of Political Economy*, 124(5), 1423–1465.
- MacKinlay, A. C. (1997). Event Studies in Economics and Finance. *Journal of Economic Literature*, 35(1), 13–39.
- Landis, J. R., & Koch, G. G. (1977). The Measurement of Observer Agreement for Categorical Data. *Biometrics*, 33(1), 159–174.

---
---

## How this paper was built — annotated commentary

> *A margin commentary for students: not part of the paper, but a narration of the choices behind it. Read it to see why each move was made, and where the Chapter 6.5 discipline did real work.*

**Why this paper leads with a disclosure box, and why every table repeats "synthetic."** The single most dangerous failure mode for an AI-methods showcase is that a reader lifts a number — "8-K earnings reactions average 3.1%" — and cites it as fact. So the synthetic label is not buried in a footnote; it is the first thing after the title, repeated in every table note and in the abstract's last line, and stated again in the conclusion's first limit. This is the `[CHECK]`-don't-fabricate ethic of CONVENTIONS §6 pushed to its logical end: when the numbers themselves are illustrative, you label *the numbers*, loudly, everywhere, because the cost of a reader mistaking a teaching value for a finding is exactly the cost of a hallucinated citation.

**Why the validation table comes before the return table.** Chapter 8.3 says lead with the headline. This paper has *two* headlines, and their order encodes the paper's whole thesis. The return table is meaningless until the reader knows the error rate on its key regressor — a CAR comparison across "event types" is only as good as the measurement of "event type." So Table 1 (is the instrument good?) precedes Table 2 (what does it show?), and §5.1 explicitly ties them together: the 0.78 recall on executive change in Table 1 is the reason the executive-change coefficient in Table 2 is flagged as attenuated. That cross-reference *is* the measurement-not-truth discipline of §6.5.4 made structural — the validation does not sit in an appendix, it governs how the result is read.

**Why the marquee threat is leakage, and how it was contained rather than dismissed.** Chapter 6.5 names training-data leakage the fatal, finance-specific trap, so the threats table puts it first and §4.4 gives it a full paragraph. The honest move was not to claim leakage is absent — that would be the overclaim — but to make the *contemporaneous-vs-predictive* distinction that contains it: classifying what an event *is* (answerable from the text) is far more leakage-resistant than predicting what a stock *will do* (which requires knowing the future). Then the paper enumerates the three residual channels and admits the only airtight defense (post-cutoff validation) was not done. This is the conceded-fatal-critique move: name the worst threat, show how much you defused, and concede exactly what you could not. The leakage-masked re-label in §6 is the empirical probe of the one channel that could actually bias the result.

**Why the rubric is frozen before returns are examined — the p-hacking firewall.** The single most seductive new degree of freedom in LLM-era research is rewriting the prompt until the regression cooperates. The paper's defense is structural and stated as the "load-bearing honesty": the rubric is locked against the *gold set* — a target with nothing to do with the return coefficient — and only then are returns examined. §4.2 Step 5 and the threats table both make this explicit, and the conclusion admits a dated pre-registration would harden it further. The gold set, not the regression, decides when the prompt is good; that sentence is the entire anti-p-hacking architecture.

**Why precision/recall/F1 and κ, never bare accuracy.** Financial-event corpora are imbalanced (earnings common, completed acquisitions rare), and §4.2 spells out why accuracy lies under imbalance — a classifier that labels everything "earnings" can post high accuracy and be useless on the classes you need. So Table 1 reports per-class precision and recall, macro-averages the F1, and adds Cohen's κ to chance-adjust the agreement. The numbers (macro-F1 0.86, κ 0.80) are matched deliberately to `nb6.5` so the exemplar and the lab tell one consistent story. The wide bootstrap intervals are not an afterthought: with a 45-document gold set, the honest signal is *how uncertain* every metric is, and the paper says a real study needs ≥200 labels with two coders.

**Why the verbs stay associational, everywhere.** This was the deliberate D.5 verb-audit. The design randomizes nothing — firms choose which 8-Ks to file — so the paper never says "earnings releases *cause* a 3% move." It says "the reaction *differs across* recovered event types," "consistent with information content," "an association we cannot cleanly separate from confounding news." The abstract, the "we find," the results prose, and the conclusion are all held to the same associational ceiling, guarding against the drift D.5 warns about where verbs creep up from abstract to conclusion. The one place the paper is *confident* — that the classifier is a usable instrument — is exactly where the validation evidence earns confidence, and there the prose is plain and unhedged.

**Why the tables follow Appendix D to the letter.** Booktabs-style (no vertical rules), key regressor on top, SE flavor named ("clustered by firm"), star legend in every note, returns rescaled to percentage points for legibility, $N$ on every column, columns built parsimonious-to-saturated (raw mean → magnitude → +controls), and a note complete enough that the table stands alone. The most important D.2 touch is the note on Table 2 that names the *mismeasured-regressor* problem in the table itself — so a referee reading only the tables sees the attenuation caveat without the prose. That is the "table stands alone" principle doing real work: the honesty travels with the exhibit.

**What a real Capstone 4 would add, and where the synthetic shortcut shows.** A live study would pull real EDGAR filings under the fair-access rule, confront the genuine multi-label problem (one 8-K, several Items), match to CRSP returns on a pinned snapshot, label ≥200 documents with two coders, and — the real fix for leakage — validate on post-training-cutoff filings. The 45-document corpus and synthetic returns are teaching scaffolding; the paper flags this in the data section, every table note, and the conclusion's limits, so the reader always knows which parts are real method and which are illustrative number. The method is the deliverable; the numbers are the worked example of what the method licenses you to say.
