# Solutions — Problem Set 6.5 (An LLM Classifier as a Measurement Instrument: Held-Out Validation and a Leakage Audit)

*Full worked solutions to `book/weeks/week-06/ps6.5.md`. Notation follows CONVENTIONS §3 and Ch 6.5. For a fixed class $c$ in a multiclass confusion matrix, $TP_c$ is the diagonal cell, $FP_c$ the off-diagonal entries of the LLM-predicted-$c$ **row**, $FN_c$ the off-diagonal entries of the truth-is-$c$ **column**; per-class scores use the one-vs-rest convention $\text{Precision}_c=TP_c/(TP_c+FP_c)$, $\text{Recall}_c=TP_c/(TP_c+FN_c)$, $F_{1,c}=2\,\text{Prec}_c\,\text{Rec}_c/(\text{Prec}_c+\text{Rec}_c)$; macro scores are the unweighted means across classes. Cohen's kappa is $\kappa=(p_o-p_e)/(1-p_e)$. All counts are the **labeled illustrative integers from the problem set**. The central thesis (§6.5.4): an LLM label is a measurement, validated against a hand-labeled gold standard out of sample, never trusted as ground truth.*

*Arithmetic note: every fraction, decimal, macro average, accuracy, and kappa below was verified two independent ways in `python3` — by exact-rational `fractions.Fraction` arithmetic and, as a cross-check, by `sklearn.metrics` (`precision_recall_fscore_support`, `accuracy_score`, `cohen_kappa_score`) reconstructing $y_{\text{true}},y_{\text{pred}}$ from the confusion-matrix counts. The two methods agree to all reported digits.*

---

## Task 1 — Why an LLM label is a measurement, not the truth (14 pts)

**(a) (4 pts)** The **latent quantity** is the 8-K's *true* event type — what the filing actually announces (a real M&A deal, real guidance, or other). Leah never observes this latent type directly; she observes it through an **instrument** = the LLM model plus her classification rubric, which returns a *label*. By Ch 1.3, that label is the latent type **plus measurement error**:
$$\text{label}_i = \text{true type}_i + (\text{systematic error}) + (\text{random error}).$$
The **systematic** component is a directional bias of the instrument — e.g., the model consistently over-calls "M&A" whenever a filing contains the word "acquire," tagging routine asset purchases as deals, so it is *biased toward* M&A in a predictable way. The **random** component is run-to-run noise: because the model samples tokens, the *same* borderline filing can come back "M&A" on one run and "OTHER" on the next (the stochasticity of §6.5.5). Systematic error shifts every label the same way; random error scatters them.

**(b) (4 pts)** In the **benign** case — *classical, non-differential* measurement error (the mislabeling is random, unrelated to the true type and to the outcome) — the standard Week-1 result on a mismeasured regressor applies: the coefficient on the "M&A" dummy is **attenuated toward zero** (biased *downward in magnitude*, the classic attenuation/regression-dilution result), and the standard error is **inflated**, so the estimate is both shrunk and noisier. Leah would *understate* the true M&A return effect and might wrongly call it insignificant. In the **non-benign** case the error is *correlated with something* and the bias can point either way: if the model mislabels **small** firms' 8-Ks more often than large firms' (it has less context on obscure tickers), and firm size also drives the abnormal return (small firms move more on news), then the label error is correlated with an omitted determinant of the outcome. The measurement error is now *differential*, the attenuation result no longer holds, and the coefficient is biased in a **direction you cannot sign** without modeling the dependence — exactly the Week-1 warning that correlated measurement error is the dangerous kind.

**(c) (3 pts)** The property LM has and the LLM lacks is **transparency / inspectability**. LM's "rubric" is a fixed, published word list: anyone can open it, see exactly which words count as negative, and reproduce the count deterministically — the instrument is fully auditable, so a reader can judge its construction directly. The LLM's rubric is your prompt *plus an opaque model* whose internal decision rule no one can inspect; the same prompt can even return different labels across runs. A more accurate but opaque instrument is *harder*, not easier, to take on faith, because the referee cannot see *how* a label was produced and so cannot judge whether it measures the named concept or some correlated confound. Greater accuracy does not excuse opacity; it raises the burden of *external* validation (the gold-set precision/recall/F1) precisely because the internal mechanism is hidden. (This is why §6.5.7 demands the verbatim rubric in an appendix — the LLM's nearest available substitute for LM's open word list.)

**(d) (3 pts)** Two distinct reasons:
1. **Wrong data, wrong base rate.** "94% accurate" was measured on *some* task, on *some* dataset, at *some* class balance — none of which is Leah's corpus, her three-label scheme, or her base rates. Accuracy is not portable: a number from another distribution says nothing about how the instrument performs on *her* 8-Ks (and Task 3 shows accuracy is meaningless without the base rate anyway).
2. **In-sample, and self-graded.** A model (or vendor) reporting its own accuracy is grading itself, and the figure is typically in-sample or on a curated benchmark. §6.5.4's protocol requires Leah's *own* **out-of-sample** precision/recall/F1, computed on a *held-out* gold set the prompt was never tuned against, with truth set by *her* hand-labels, not the model's say-so. The verifier must be the gold standard, not the instrument's opinion of itself.

---

## Task 2 — Build the confusion matrix; precision, recall, F1, macro — by hand (22 pts)

Reading the table: rows are LLM predictions, columns are gold truth; diagonal cells (38, 22, 56) are correct.

**(a) (3 pts)** For **GUIDANCE** (top-left class):
- $TP_{\text{G}} = 38$ (LLM said GUIDANCE, truth GUIDANCE — the diagonal).
- $FP_{\text{G}} = 4 + 6 = 10$ (rest of the GUIDANCE *row*: LLM said GUIDANCE but truth was M&A or OTHER).
- $FN_{\text{G}} = 3 + 9 = 12$ (rest of the GUIDANCE *column*: truth was GUIDANCE but LLM said M&A or OTHER).

Plain English: the $FP=10$ are **false alarms** — filings the model *called* guidance announcements that are really something else (4 M&As, 6 other events misfiled as guidance). The $FN=12$ are **misses** — filings that truly *are* guidance announcements but the model labeled M&A (3) or OTHER (9), so they slip out of the guidance bucket.

**(b) (6 pts)** Per-class $TP/FP/FN$ and scores. (M&A: $TP=22$, $FP=3+5=8$, $FN=4+4=8$. OTHER: $TP=56$, $FP=9+4=13$, $FN=6+5=11$.)

**GUIDANCE** ($TP=38, FP=10, FN=12$):
$$\text{Prec}=\tfrac{38}{38+10}=\tfrac{38}{48}=\tfrac{19}{24}=0.792,\quad \text{Rec}=\tfrac{38}{38+12}=\tfrac{38}{50}=\tfrac{19}{25}=0.760,$$
$$F_1=2\cdot\frac{0.7917\cdot0.7600}{0.7917+0.7600}=\frac{38}{49}=0.776.$$

**M&A** ($TP=22, FP=8, FN=8$):
$$\text{Prec}=\tfrac{22}{30}=\tfrac{11}{15}=0.733,\quad \text{Rec}=\tfrac{22}{30}=\tfrac{11}{15}=0.733,\quad F_1=\tfrac{11}{15}=0.733.$$
(Precision = recall here because $FP=FN=8$, so $F_1$ equals them too.)

**OTHER** ($TP=56, FP=13, FN=11$):
$$\text{Prec}=\tfrac{56}{69}=0.812,\quad \text{Rec}=\tfrac{56}{67}=0.836,\quad F_1=2\cdot\frac{0.8116\cdot0.8358}{0.8116+0.8358}=\tfrac{14}{17}=0.824.$$

Summary table:

| Class | $TP$ | $FP$ | $FN$ | Precision | Recall | $F_1$ |
|---|---|---|---|---|---|---|
| GUIDANCE | 38 | 10 | 12 | 0.792 | 0.760 | 0.776 |
| M&A | 22 | 8 | 8 | 0.733 | 0.733 | 0.733 |
| OTHER | 56 | 13 | 11 | 0.812 | 0.836 | 0.824 |

**(c) (4 pts)** Macro = unweighted mean across the three classes:
$$\text{macro-Prec}=\tfrac{0.7917+0.7333+0.8116}{3}=0.779,\qquad \text{macro-Rec}=\tfrac{0.7600+0.7333+0.8358}{3}=0.776,$$
$$\text{macro-}F_1=\tfrac{0.7755+0.7333+0.8235}{3}=0.7775\approx 0.778.$$
(Averaging the *exact* per-class F1s gives $\tfrac{1}{3}\!\left(\tfrac{38}{49}+\tfrac{11}{15}+\tfrac{14}{17}\right)=0.77746$, which rounds to 0.777; averaging the already-3-dp-rounded per-class values gives 0.778. The two agree to within rounding — either is acceptable by hand; we quote 0.778.) Overall **accuracy** = correct over total = $(38+22+56)/147 = 116/147 = 0.789$.
(Note accuracy 0.789 and macro-F1 0.778 are close *here* only because the three classes are not wildly imbalanced; Task 3 is where they diverge violently.)

**(d) (4 pts)** For the M&A class: **precision 0.733** means that when the model stamps "M&A," it is right about **73%** of the time — roughly one in four "M&A" labels is actually a non-deal misfiled into the group. **Recall 0.733** means that of all the *true* M&A 8-Ks, the model **catches about 73%** and misses about a quarter. For Leah's regression — comparing the average return of the *M&A group* to everyone else — the more damaging error is the **false positive** (a non-M&A wrongly tagged M&A). Misses ($FN$) shrink the M&A group but the survivors are still genuine deals, so the group's mean stays roughly *on-concept* (just noisier and lower-powered). False positives ($FP$) inject genuinely non-M&A filings *into* the M&A group, **contaminating the very mean she is measuring** and pulling the M&A-group average toward the overall average — biasing the estimated M&A-vs-rest return difference toward zero (and, if the contaminants are non-random, in an unsignable direction, per Task 1b). Precision is the error that corrupts the treatment group's mean; that is why it is the one to scrutinize for her use.

**(e) (5 pts)** A single macro-F1 of 0.78 is a **point estimate from only 147 filings**, and a point estimate without an interval hides how much it could move on a re-draw of the gold set — the mentor is asking for the sampling uncertainty. The M&A class is the binding worry: the model **predicted M&A on only 30 filings** (the M&A row total), and the M&A *precision* (0.733) is a proportion estimated on those **30 predicted-positives** as its denominator. A proportion near 0.7 estimated from ~30 trials has a wide binomial/Wilson interval — roughly $\pm 0.16$ at 95% — so the true M&A precision could plausibly sit anywhere from the high-0.50s to the high-0.80s. (The recall denominator, the 30 *true* M&As, is equally small, so M&A recall is just as wide.) The general point from §6.5.4: a precision measured on few predicted-positives is fragile, and you must report it **with its confidence interval** so a referee can see the estimate is not as sharp as "0.733" looks. nb6.5 computes these intervals by bootstrapping the gold set; here the takeaway is simply *which* count is small (30) and that small denominators make the M&A scores the least reliable in the table.

---

## Task 3 — Why raw accuracy lies under class imbalance (16 pts)

Setup: $N=500$, true positives (distressed) $=25$ (5%), true negatives $=475$ (95%). Positive class = distressed.

**(a) (3 pts)** Confusion matrices (positive = distressed):

**Classifier A** (labels everything "not-distressed" — predicts negative for all 500):
$$TP=0,\quad FP=0,\quad FN=25,\quad TN=475.$$
(It never predicts positive, so $TP=FP=0$; all 25 true distressed become misses $FN$; all 475 true-negatives are correctly called negative.)

**Classifier B** ($TP=20,\ FP=30,\ FN=5$):
$$TN = N - TP - FP - FN = 500 - 20 - 30 - 5 = 445.$$

| | Pred distressed | Pred not | Total |
|---|---|---|---|
| **A:** true distressed | 0 | 25 | 25 |
| **A:** true not | 0 | 475 | 475 |
| **B:** true distressed | 20 | 5 | 25 |
| **B:** true not | 30 | 445 | 475 |

**(b) (4 pts)** Raw accuracy $=(TP+TN)/N$:
$$\text{Acc}_A=\frac{0+475}{500}=\frac{475}{500}=0.9500,\qquad \text{Acc}_B=\frac{20+445}{500}=\frac{465}{500}=0.9300.$$
The alarming result: the **do-nothing Classifier A (0.9500) has *higher* accuracy than the genuinely useful Classifier B (0.9300)**. By the metric everyone reaches for first, the useless classifier "wins."

**(c) (4 pts)** Distressed-class precision/recall/F1:

**Classifier A:** $\text{Prec}=TP/(TP+FP)=0/0$ — **undefined** (the model never predicts positive, so there is *no* set of "predicted distressed" to be right or wrong about; conventionally reported as 0 or N/A with a zero-division flag). Recall $=0/(0+25)=\mathbf{0.0000}$ — it catches *none* of the distressed firms. $F_1=0$. The classifier is, for Leah's purpose, completely blind.

**Classifier B:** $\text{Prec}=\frac{20}{20+30}=\frac{20}{50}=0.4000$, $\text{Rec}=\frac{20}{20+5}=\frac{20}{25}=0.8000$, $F_1=2\cdot\frac{0.40\cdot0.80}{0.40+0.80}=\frac{0.64}{1.20}=\frac{8}{15}=0.5333$.

Side by side: A has accuracy 0.95 but **recall 0** and **F1 0**; B has accuracy 0.93 but **recall 0.80** and **F1 0.53**. The accuracy ranking (A > B) is **exactly backwards** from what the research question needs, because Leah cares about *finding distressed firms* — the rare positive class — and A finds none of them while B finds 80% of them. Accuracy rewarded A for correctly labeling the 475 easy negatives, which is not the job.

**(d) (3 pts)** Accuracy is wrong as a headline because of the **base rate**: when the positive class is only 5% of the data, a classifier earns **95% accuracy for free** by always predicting the majority ("not-distressed") and doing literally nothing — the no-information baseline. Beating 95% therefore requires essentially **zero skill**; the metric is dominated by the 475 trivial negatives and is nearly blind to performance on the 25 cases that matter. This is the fraud-detector / rare-disease trap: when fraud is 1-in-1000, "always say not-fraud" scores 99.9% accuracy and never catches a fraud. Leah should report **precision and recall on the distressed (positive) class** (and their $F_1$), because those quantities are computed *only* from the positive cases and false alarms — they cannot be inflated by correctly labeling the easy majority, so they expose the recall-0 disaster that accuracy hides.

**(e) (2 pts)** "96% accuracy on distress detection" could be worse than useless because, at a 5% base rate, the **do-nothing baseline is already 95%** — so 96% is barely above free and might still have near-zero recall on actual distress (a classifier could reach 96% while catching almost no distressed firms). The single additional number Leah needs is the **base rate (class balance) of the benchmark** (equivalently, the recall/precision on the positive class): only against the base rate can she tell whether 96% reflects real skill or is one point above a coin that always says "fine."

---

## Task 4 — Cohen's kappa: LLM vs. a human coder (16 pts)

$N=100$. Cells: human-NEG & LLM-NEG $=30$; human-NEG & LLM-NOT $=10$; human-NOT & LLM-NEG $=6$; human-NOT & LLM-NOT $=54$.

**(a) (3 pts)** Observed agreement = diagonal over $N$:
$$p_o=\frac{30+54}{100}=\frac{84}{100}=0.8400.$$
On its own this 84% can mislead because *both* coders call most filings "not-negative" (human 60/100, LLM 64/100), so a large share of that agreement is the cheap kind — two coders who both lean "not-negative" will agree on the easy not-negatives by default. Raw agreement does not subtract off that free, chance-driven concordance.

**(b) (5 pts)** Marginal proportions:
- Human: $\Pr(\text{NEG})=\frac{40}{100}=0.40$, $\Pr(\text{NOT})=\frac{60}{100}=0.60$.
- LLM: $\Pr(\text{NEG})=\frac{36}{100}=0.36$, $\Pr(\text{NOT})=\frac{64}{100}=0.64$.

Chance agreement (independent labeling at those marginals):
$$p_e=\Pr(\text{h=NEG})\Pr(\text{l=NEG})+\Pr(\text{h=NOT})\Pr(\text{l=NOT})=(0.40)(0.36)+(0.60)(0.64).$$
$$p_e=0.1440+0.3840=0.5280.$$

**(c) (3 pts)**
$$\kappa=\frac{p_o-p_e}{1-p_e}=\frac{0.8400-0.5280}{1-0.5280}=\frac{0.3120}{0.4720}=\frac{39}{59}=0.6610.$$
Numerator $p_o-p_e=0.3120$; denominator $1-p_e=0.4720$; ratio $=0.6610$.

**(d) (3 pts)** $\kappa=0.661$ lands in the **0.61–0.80 = "substantial"** band (just over the lower edge). The contrast: the **raw agreement of 0.84 sounds excellent** — "they agree 84% of the time!" — but **$\kappa=0.66$ is merely substantial**, a real but more sober verdict. The gap is what kappa is **charging the coders for**: the **0.528 of agreement they would have reached by chance alone** given how lopsided their marginals are. Kappa rescales the agreement onto a "beyond chance" axis (0 = chance-level, 1 = perfect), and once you remove the free agreement, 84% raw shrinks to 66% chance-corrected.

**(e) (2 pts)** The LLM *is* "a coder" in exactly the Task-1 sense: it is an **instrument that assigns labels**, so its labels can be cross-tabulated against a human's identically to two human coders. A high LLM-vs-human kappa buys you something the precision/recall-against-gold table does not: it measures **agreement with an independent human's judgment beyond chance**, which speaks to whether the *task itself* is well-defined and whether the model's labels track a second, independent interpreter rather than only matching the one gold standard you happened to build. (If even two humans disagree, a modest LLM-human kappa may reflect a hard task, not a bad model — information the gold-set scores alone cannot give you.)

---

## Task 5 — Look-ahead bias / training-data leakage: audit and fix (18 pts)

**(a) (5 pts)** The bias is **look-ahead bias via training-data leakage** (§6.5.5). The model's training cutoff (text through **2024**) is **after** Sam's sample period (**2021**), so the model was very likely trained on text describing *what actually happened* to those stocks over 2021–22 — subsequent news, later filings, analyst write-ups, the realized outcomes themselves. When Sam asks it to "predict" 2021 returns, the model is not forecasting from the 2021 filing; it is **recalling** an outcome it absorbed in training. The information leaking in — knowable to the model, **not** knowable to a trader standing in January 2021 — is the *future realized return* and everything written about the stock after the filing date. This is precisely the Ch 1.5 definition: information from the future entering a decision that is supposed to use only information available *as of* the decision date. The backtest's 31% is hindsight wearing the mask of prediction.

**(b) (4 pts)** Withholding the 2021 returns *at query time* does not help, because the leakage happened **earlier, during training**: the outcome is baked into the model's *weights*, not supplied in the prompt. The model does not need to be *shown* the 2021 return to "know" it — it learned it. So a clean-looking prompt that contains only 2021 filing text still elicits an answer informed by 2022 knowledge. That is why the 31% is a near-certainty to **evaporate** on forward trading: a genuinely live deployment runs on filings about events the model has *never* seen (post-cutoff), where it cannot recall the outcome and must actually predict — and a model that was "predicting" by remembering has no real predictive edge. The fake performance lives entirely in the period the model had already read; remove that overlap and the alpha goes to roughly zero, exactly when real money is on the line.

**(c) (4 pts)** **Task X (tone of a 2021 8-K) is comparatively safe; Task Y (predict 2021–22 return) is exactly where leakage bites.** A filing's *tone* is a **contemporaneous attribute** — it is determined entirely by the text in front of the model, and labeling it correctly never requires knowing any future outcome, so even though the model has "seen" 2021, that does not corrupt a judgment about the document's own contents. A *return* is a **forward outcome** realized after the filing date; "predicting" it is exactly the task the model can short-circuit by recalling what happened. The general rule (§6.5.5): **classifying a contemporaneous attribute of the text is far less leakage-prone than predicting a future outcome from it.** If the correct label is fixed by the text itself, leakage is a minor worry; if the correct label is an event that unfolds *after* the text, and the model's training extends past that event, treat the result as contaminated.

**(d) (5 pts)** The **four-part defense** from §6.5.5:
1. **Know the model's training cutoff** and treat any sample period *before* it as suspected-contaminated for any forward-looking task.
2. **Prefer contemporaneous-attribute tasks over forward-prediction tasks** where the science allows (tone, event type — not "will it go up").
3. **Test genuinely out-of-sample on data created *after* the cutoff**, where the model could not have peeked — the cleanest defense.
4. **In RAG, enforce the time order mechanically** with a date filter on chunk metadata.

The concrete **date-filtered retrieval** (every chunk carries a `date`, per §6.5.3):

```python
def retrieve(query_vec, query_date, index, k=5):
    # INVARIANT: never return a chunk dated AFTER the decision date.
    eligible = [c for c in index if c.metadata["date"] <= query_date]
    eligible.sort(key=lambda c: cosine_sim(query_vec, c.vector), reverse=True)
    return eligible[:k]            # top-k among only as-of-date passages
```

The one-line invariant: **for a query dated $t$, every retrieved chunk satisfies $\text{date}(\text{chunk}) \le t$** — no passage from the future of the decision can ground the answer. (Filter *first*, then rank by cosine similarity, so a more-similar-but-future chunk can never sneak in.) Finally, the *cleanest* defense is point 3: run the strategy on filings created **after** the model's training cutoff, because there the model has no memory of the outcome to leak — any edge it shows there is real prediction, not recall, which is the only kind that survives forward into live trading.

---

## Task 6 — Reproducibility, disclosure, and prompt-induced p-hacking (14 pts)

**(a) (4 pts)** A regression is deterministic (same data + code → same coefficient forever), but an LLM samples its output from a probability distribution over next tokens, so the **same prompt can yield different labels on different runs** — and if the labels move, the downstream regression moves, and "I got $p=0.04$ that one time" is not a replicable result. The single most robust fix (§6.5.5), the one that does **not** rely on the model being deterministic: **run the classification once, save the labels to disk, and treat that saved file as your dataset** — never re-query the model inside an analysis meant to be reproducible. The labels are *data*; freeze them like data. "Set temperature to 0" is **not** a sufficient guarantee on its own because temperature/seed controls differ by provider, are not bit-for-bit guaranteed across model versions or hardware, and **some current frontier models — Anthropic's Opus 4.7 among them — do not expose a `temperature` parameter at all**, so you cannot assume the knob even exists; reproducibility must come from freezing the *pipeline*, not from trusting the model to be deterministic.

**(b) (4 pts)** The four things to log/pin/save (§6.5.6–6.5.7):
1. **The JSONL audit log** — one line per API call recording timestamp, model, token counts, and (a hash of) the prompt and the response. *Omit it →* you cannot prove which request produced which label; "I used an LLM" becomes unfalsifiable.
2. **The exact model *version string*** (e.g., `claude-opus-4-7`, not just "Claude"). *Omit it →* a model silently updated under the same name changes your labels and your results, undetectably — version it like a CRSP snapshot date per CONVENTIONS §5.
3. **The API version, and any seed/temperature** where they exist. *Omit it →* a re-runner uses different defaults and gets a different distribution of outputs.
4. **The saved label file, treated as the dataset.** *Omit it (re-query instead) →* every re-run regenerates labels stochastically and the analysis is no longer replicable.

Why log a **SHA-256 hash** of the prompt rather than the raw prompt when the input contains **licensed text**: the hash **proves exactly what you sent** — any change to the input changes the hash, so it is a tamper-evident fingerprint — *without copying licensed CRSP/Compustat/TRACE text into a log file*, which would breach the data-use agreement (CONVENTIONS §5: licensed data stays on GMU infrastructure). You get auditability and license compliance at once.

**(c) (4 pts)** **Prompt-induced p-hacking** is rewording the classification prompt (consciously or not) until the *labels it produces* yield the regression result you were hoping for, then reporting the lucky prompt. It is **arguably worse** than classic p-hacking because the researcher degree of freedom — the *exact prompt wording* — is enormous, continuous, and so easy to fiddle with that you may not even notice you are searching; there is no discrete list of "specifications tried" to feel guilty about. Leah's bad loop: M&A coefficient insignificant → she broadens the M&A rubric ("merger OR strategic-investment language") → the label column shifts → coefficient now significant → she stops and reports it. The degree of freedom she exploited is **the rubric/prompt wording itself** (which *defines the M&A label* and therefore the regressor). The §6.5.5 structural defense: **freeze the rubric against the *gold set*, before ever looking at the downstream regression coefficient** — lock the prompt when its held-out F1 is acceptable, using a target (gold-set validation) that has *nothing to do with* the regression result, so the prompt cannot be tuned toward significance. (Reinforce with: pre-register the frozen prompt in a dated file, and report it verbatim in an appendix.)

**(d) (2 pts)** Example disclosure paragraph:

> *AI use. We used a large language model in two distinct roles. As a **writing aid**, Claude (model `claude-opus-4-7`) helped edit prose in the introduction and methods; we wrote and verified every claim and own every word retained. As a **data-generating instrument**, the same model classified all 40,000 8-K filings into event types (GUIDANCE / M&A / OTHER) using the frozen rubric reproduced verbatim in Appendix C; these labels enter the regressions. We validated this classifier against a 147-filing hand-labeled gold set, reporting out-of-sample per-class and macro precision, recall, and F1 (Table X), and we release the JSONL call log, the pinned model version, and the saved label file for replication.*

This distinguishes the writing aid (words owned, no validation needed beyond truth) from the data generator (labels that demand the gold-set validation), names what was validated and how, and points to the verbatim rubric in the appendix — the §6.5.7 standard.

---

*End of solutions for PS 6.5. Every numerical answer — the per-class and macro precision/recall/F1 (Task 2), the imbalance accuracy/precision/recall (Task 3), and Cohen's kappa $=0.661$ (Task 4) — was verified in `python3` by exact-rational arithmetic and cross-checked against `sklearn.metrics`. The conceptual spine is Ch 6.5 §6.5.4's thesis welded to Week 1: an LLM label is a measurement (Task 1), graded by precision/recall/F1 not accuracy (Tasks 2–3), agreement-tested beyond chance via kappa (Task 4), audited for look-ahead/training-data leakage (Task 5), and made reproducible and honestly disclosed against prompt-induced p-hacking (Task 6). The runnable companion is nb6.5, which recomputes all of the above on a real hand-labeled 8-K dataset with bootstrap confidence intervals.*
