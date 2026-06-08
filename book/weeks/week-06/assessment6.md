# Week 6 Assessment — Reading the Frontier II: Build and Validate a Text Classifier

Weeks 1 through 4 taught you to *run* an estimator; Week 5 taught you to *read* one in
someone else's hands. Week 6 added a third skill that sits underneath both: when the data is
*words*, someone has to turn those words into a number, and that someone is now often a large
language model (LLM). Chapter 6.5 stated the sentence the whole week turns on — **an LLM-produced
label is a measurement, not the truth, so before any LLM label enters a regression you must validate
it against a hand-labeled gold standard and report its error rate on held-out data.** This assessment
makes you do exactly that, once, alone, end to end.

You will define a small text-classification problem, hand-label a gold set, split it into a
development set and a held-out test set, build a classifier, and produce an out-of-sample (OOS)
validation report: a confusion matrix, per-class and macro precision/recall/F1, and Cohen's kappa
against your human labels. Then — and this is what the rubric weights hardest — you will write a
**leakage/look-ahead audit** and a **reproducibility/disclosure statement** that an honest referee
would accept. The grading does *not* reward a high F1. It rewards an F1 you have *earned the right to
report*: built on a held-out test, scored with the right metrics, and disclosed with its limitations
named out loud. A classifier with a mediocre but honestly validated F1 outscores a classifier with a
shiny but contaminated one. That asymmetry is the entire point of the week.

**Total: 100 points.** Part A (the build-and-validate task) = 70, Part B (four conceptual items) = 20,
presentation and intellectual honesty woven through both = 10. This is take-home: budget one sitting
to define the task and hand-label your gold set, and a second to build, validate, and write up. You do
**not** need an API key — the local fallback classifier from nb6.5 (a bag-of-words logistic regression
with a keyword backstop) is fully acceptable, and a dictionary baseline is acceptable too. If you *do*
use an LLM through the provider switch, the disclosure bar simply rises; it does not change the task.

Throughout, hold yourself to the discipline of CONVENTIONS §5: code runs end to end on a fresh
environment, **secrets live in environment variables only — never hard-coded**, and LLM-generated
labels are saved to disk and treated as data, never re-queried inside the analysis.

---

## Part A — Build and validate one text classifier (70 points)

### A.0 Define the classification problem (5 pts)

Pick **one** text-classification problem on public text the camp can actually reach (EDGAR 8-K and
10-K filings are public and free; a 10-K from EDGAR is fine, the CRSP return you might join to it is
not — strip to public text). State, in the CONVENTIONS-style measurement form:

> **concept being measured · text unit · label set (with the rubric) · corpus and source · why this
> label would matter for a downstream finance question.**

Three candidate problems, each tied to a member of the cast — pick one or clear your own with your
mentor:

1. **8-K event-type label** (Leah / Sam). Each 8-K snippet → one of `{LAYOFF, M&A, EXEC_CHANGE,
   OTHER}`, or a binary `{LAYOFF, NOT_LAYOFF}`. Downstream use: does the market react differently to
   layoff 8-Ks than to other material events?
2. **10-K Risk-Factor tone** (Maya / Priya). Each Item 1A snippet → `{NEGATIVE, NEUTRAL, POSITIVE}`
   using the rubric from §6.5.2 (worsening threat / boilerplate / resolved risk). Downstream use: does
   risk-factor tone predict next-quarter volatility?
3. **Disclosure-topic label** (Devon / Priya). Each snippet → `{LIQUIDITY_RISK, CLIMATE_RISK,
   REGULATORY_RISK, OTHER}`. Downstream use: do firms that newly disclose climate risk see a change in
   insurance-related costs?

Whatever you pick, **write the rubric in full** — the explicit decision rule, with a default for the
ambiguous case (e.g., "if genuinely ambiguous, choose NEUTRAL"). The rubric is a measurement protocol,
not a hint; it must be precise enough that another grader, or the model on a re-run, applies the same
definition to item 5,000 as to item 5.

### A.1 Hand-label a gold set and split it (12 pts)

Build a **gold standard** — the closest thing you have to ground truth.

- Draw a **random** sample of at least **60 snippets** from your corpus (200 is the floor in real
  research; 60 is the floor for this assessment, given your time). It must be random, not cherry-picked
  easy cases — a gold set of easy cases flatters every classifier. State your sampling procedure.
- Label each snippet **yourself**, against your A.0 rubric. If you can, have a **second person** label
  the same snippets independently and reconcile disagreements; if you do, you will compute human–human
  Cohen's kappa in A.4, which tells you how hard the task is *before* you blame any model.
- **Split the gold set** into a **development set** (you may look at it freely while tuning) and a
  **held-out test set** of at least **20 snippets** that you do **not** look at while building. Use a
  stratified split so each label appears in both halves. Write the split to disk with a fixed random
  seed and **report the seed**. The test set is touched exactly **once**, at the end.

Submit your labeled gold set as a CSV (`id, text_or_text_hash, gold_label, split`) — you may store a
hash of the text instead of the raw text if the snippet is long, but for public EDGAR text the raw
snippet is fine and more checkable.

### A.2 Build the classifier (18 pts)

Build a classifier that maps a snippet to a label. **Any one** of three routes earns full marks if
done correctly; pick the one that fits your access:

- **Local ML/dictionary baseline (no API key needed).** A bag-of-words or TF-IDF logistic regression
  trained on the *development* set, or a dictionary classifier (e.g., a Loughran–McDonald-style word
  count for tone, or a keyword rule for event type). This is the nb6.5 fallback path and is fully
  acceptable. If you train an ML model, it trains on the **dev** set only — the test set is never seen
  during fitting.
- **LLM via the provider switch (nb6.5).** Send each snippet to a model with your rubric as the
  *stable* system prompt (the volatile snippet last, so prompt caching works), and parse the one-word
  label. Read your key from the environment — `Anthropic()` reads `ANTHROPIC_API_KEY` automatically;
  the GMU Azure client reads `os.environ["AZURE_OPENAI_KEY"]`. **No key appears in your code.**
- **LLM, local fallback for licensed text.** If your text were licensed (it should not be for this
  assessment — use public EDGAR), you would run a local model via Ollama so the data never leaves the
  machine. Note this path even if you do not need it.

Whichever route you take, the build must include the rubric/prompt or the feature/word list **verbatim**
as an artifact, and the classifier must be **frozen** before you touch the test set. A correct build
also handles the ambiguous/unsure case explicitly (an `UNCLEAR`/`null`/default class) rather than
forcing a guess.

Skeleton of the env-only call pattern (no secrets in code):

```python
import os
from anthropic import Anthropic          # reads ANTHROPIC_API_KEY from the environment

client = Anthropic()                      # NO key passed in code — env var only

RUBRIC = """You are classifying 8-K snippets. Assign exactly one label:
LAYOFF / M&A / EXEC_CHANGE / OTHER, following these rules: [... full rubric ...].
If genuinely ambiguous, return OTHER. Return only the label word."""

def classify(snippet: str) -> str:
    resp = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=16,                                  # one word out
        system=[{"type": "text", "text": RUBRIC,
                 "cache_control": {"type": "ephemeral"}}],   # cache the stable rubric
        messages=[{"role": "user", "content": snippet}],     # volatile input last
    )
    return resp.content[0].text.strip()
```

If you use the local fallback instead, `classify()` is your trained model's `.predict()` plus the
keyword backstop — same interface, no network, no key. **Run the classifier once over the gold set and
save the predicted labels to disk**; treat that file as your data and do not re-query inside the
scoring code.

### A.3 The out-of-sample validation report (25 pts)

This is the centerpiece. Report, **on the held-out test set only** (with the classifier frozen):

**(a) Confusion matrix (5 pts).** Rows = predicted, columns = gold (or state your convention). For a
binary task it is the 2×2 of TP/FP/FN/TN; for a multi-class task it is the full $C\times C$ matrix.
Label the axes. This is the raw material every later number comes from, so show it.

**(b) Per-class precision, recall, F1 (8 pts).** For each class $c$, using one-vs-rest counts:

$$\text{Precision}_c=\frac{TP_c}{TP_c+FP_c},\qquad
\text{Recall}_c=\frac{TP_c}{TP_c+FN_c},\qquad
F_{1,c}=2\cdot\frac{\text{Precision}_c\cdot\text{Recall}_c}{\text{Precision}_c+\text{Recall}_c}.$$

Report all three for **every** class, not just the one you like. Precision answers "when the model
says class $c$, how often is it right?"; recall answers "of the true class-$c$ items, how many did it
catch?" Report the precision/recall on the **rare class you care about** prominently, because that is
where accuracy lies.

**(c) Macro-averaged precision, recall, F1 (4 pts).** The macro average is the unweighted mean across
classes, e.g. $\text{macro-}F_1=\frac{1}{C}\sum_c F_{1,c}$. Report it, and say in one line why you
report *macro* (which weights every class equally) rather than only *micro*/accuracy (which lets the
majority class dominate). This is the class-imbalance defense made concrete.

**(d) Cohen's kappa vs. human labels (5 pts).** Compute

$$\kappa=\frac{p_o-p_e}{1-p_e},$$

where $p_o$ is the observed fraction the classifier and the human gold label agree on, and $p_e$ is
the agreement expected by chance given each side's label frequencies. Report classifier–human kappa.
If you had a second human annotator, also report human–human kappa, and compare: if the model's kappa
approaches the human–human kappa, the model is a credible annotator; if human–human kappa is itself
low, the *task* is ambiguous and the rubric needs fixing before you blame the model.

**(e) Uncertainty (3 pts).** Report a confidence interval (a bootstrap CI over the test items, or a
normal-approximation interval) on at least your headline metric — macro-F1 or the rare-class recall.
A precision of 0.80 measured on 10 predicted-positives is nearly uninformative; show that you know it.
State your test-set size $n$ next to every metric.

> **You must not report bare accuracy as the headline number.** You may report it, but only alongside
> the base rate, and you must say in one sentence why it would mislead here. A classifier that labels
> everything with the majority class is the trap.

### A.4 Leakage / look-ahead audit (5 pts)

Write a short audit (a few sentences, with the specific checks you ran) covering both kinds of leakage
from §6.5.5:

- **Pipeline leakage** — did any information from the *test* set touch the *build*? (Was the ML model
  fit on dev only? Did you tune any threshold or prompt wording against the test labels? Did vocabulary
  or IDF get computed including test text?) State explicitly that the test set was scored exactly once
  with the classifier frozen.
- **Training-data / look-ahead leakage** (the LLM-specific, finance-specific trap) — could the model
  "know" your labels for the wrong reason? For a *contemporaneous attribute* (the tone of *this* text,
  the event type of *this* 8-K) leakage is mild — labeling a 2019 filing's tone does not require knowing
  2020 returns. For a *forward-looking* target (predict next year's return from this filing), it is
  fatal, because the model's training cutoff may postdate your sample. State your model's training
  cutoff (or "n/a — local model trained only on my dev set"), classify your task as contemporaneous or
  predictive, and name the one defense you applied (e.g., a date filter on retrieval, or the fact that
  your label is contemporaneous, or OOS testing on post-cutoff text).

### A.5 Reproducibility & disclosure statement (5 pts)

A short statement that would let a stranger with only your repository re-run the work:

- **What the AI did (if anything).** Distinguish AI used as a *writing aid* (you own every word) from
  AI used to *generate data* (labels that enter the analysis); only the second demands the validation
  above. If you used no LLM, say so.
- **Pinning.** Name the exact model *version string* and provider (or "local: scikit-learn x.y, fixed
  seed 42"), the API version if applicable, and any temperature/seed. **Note honestly where determinism
  is not guaranteed** — e.g., that Opus 4.7 does not expose a `temperature` knob, so you made the
  *pipeline* reproducible by saving the labels to disk rather than relying on the model being
  deterministic.
- **Logging.** If you called an API, commit a JSONL audit log (one record per call: timestamp, model
  version, a SHA-256 hash of the prompt if the input is sensitive, token counts). If local, commit the
  training script and seed.
- **Frozen labels.** Confirm the predicted labels were saved to disk and the analysis reads that file
  rather than re-querying the model — "the labels are data; freeze them like data."
- **No secrets.** Confirm no key appears anywhere in the code or notebook.

---

## Part B — Conceptual items (20 points)

Answer each in two to five sentences. These test the Week-6 reflexes in isolation.

**B1. Text-as-data is measurement, not causality (5 pts).** Your classifier labels each 8-K as
`LAYOFF` or not, and you find layoff-8-K firms have lower next-quarter returns. A reader says "so
layoffs cause the price drop." In two to four sentences, explain (i) why a *valid* classifier is a
claim about *measurement* (does the `LAYOFF` label capture actual layoff announcements?) and *not*
about causality, and (ii) what kind of evidence — distinct from your validation report — a causal
claim would additionally require. Connect the validity idea to one Week-6 paper (KPSS patent value,
Hoberg–Phillips similarity, or Loughran–McDonald tone).

**B2. Why raw accuracy misleads under imbalance (5 pts).** In your corpus, 8% of 8-Ks are layoffs. A
classifier that labels *every* filing `NOT_LAYOFF` is asked to report its quality. Give its accuracy,
its recall on the `LAYOFF` class, and its `LAYOFF` precision (note the precision is undefined — explain
why). Then state, in one sentence, which single metric most cleanly exposes that this classifier is
useless, and why macro-F1 would also flag it while accuracy hides it.

**B3. Detect and prevent look-ahead leakage (5 pts).** Sam proposes: "ask the LLM to read each firm's
January 2021 10-K and predict whether the stock rose during 2021." Explain in two to four sentences
(i) precisely why this can show fake, spectacular performance even with a perfect prompt, naming the
mechanism (training cutoff vs. sample period), and (ii) the one change that would make the test honest
(genuine OOS testing on post-cutoff data, or recasting the task as *contemporaneous* extraction rather
than *prediction*). Contrast it with a task on the same filing that is *not* contaminated.

**B4. What to disclose about AI use (5 pts).** You used Opus 4.7 to (a) generate the `LAYOFF` labels
that go into your regression, (b) rewrite your methods paragraph, and (c) suggest three papers to cite.
For each of the three uses, state what you must disclose and what you must independently verify before
it enters the paper — and explain why use (a) demands a validation table while use (b) does not, and
why use (c) is the most dangerous if left unchecked.

---

## Part C — Analytic rubric (point allocations explicit)

Each row is scored at one of four levels. The rubric is weighted, by design, toward **validation
rigor**, **honesty about leakage and limitations**, and **reproducibility** — because those, not a high
F1, are what separate a defensible measurement from a confident guess.

| Criterion | Excellent | Proficient | Developing | Missing | Pts |
|---|---|---|---|---|---|
| **Validation rigor — held-out test, right metrics** (A.1 split + A.3). The reported numbers are computed on a genuinely held-out, stratified test set with the classifier frozen; confusion matrix shown with labeled axes; per-class precision/recall/F1 reported for *every* class; macro-average reported with a one-line justification over accuracy; Cohen's kappa vs. human computed correctly; a CI/uncertainty and test-set $n$ accompany the headline metric; bare accuracy is never the headline. | Held-out test used and most metrics correct, but one slip: macro-average missing or unjustified, no uncertainty/CI, kappa omitted, or one per-class metric not reported. | Metrics computed but on the dev set or the whole gold set (no real held-out), or only accuracy/one global F1 reported, or the confusion matrix is unlabeled/wrong. | No held-out test, or only accuracy reported, or metrics not traceable to a confusion matrix. | **24** |
| **Honesty about leakage & limitations** (A.4 + B1, B3 + the honesty thread). Leakage audit covers *both* pipeline leakage (test never touched the build; scored once; IDF/vocab/threshold not fit on test) *and* training-data/look-ahead leakage (model cutoff stated, task classified contemporaneous vs. predictive, defense named); the write-up states plainly what the classifier *cannot* support (measurement ≠ causality) and what a low recall or small $n$ does to a downstream regression; B1 and B3 correct and specific. | Both leakage types addressed and limitations named, but one is thin — e.g., cutoff stated but defense vague, or the measurement-vs-causality point asserted without tying it to the downstream consequence. | Only one kind of leakage discussed, or limitations are generic ("the model isn't perfect") without the concrete downstream consequence; B1/B3 partially correct. | No leakage audit, or overclaims (treats labels as truth / claims causality from a classifier). | **20** |
| **Reproducibility & disclosure** (A.5 + B4 + CONVENTIONS §5). Exact model version/provider (or local lib + seed) pinned; API version if used; determinism caveat stated honestly (e.g., Opus 4.7 has no temperature knob → labels saved to disk instead); audit log committed (or training script + seed for local); predicted labels saved and analysis reads the file, not the live model; gold set + split + seed committed; **no secret anywhere — env vars only**; B4 correct on the three AI uses. | Reproducible and disclosed, but one element thin: seed unstated, log present but missing a field, or the determinism caveat omitted. | Some disclosure but a re-run would not reproduce the labels (no saved labels, no pinned version, or no seed); B4 superficial. | No disclosure, OR a hard-coded key/secret appears anywhere (this alone caps the row at Missing). | **18** |
| **Correctness of the classifier build** (A.0 + A.2). Problem defined in the measurement form with a full, explicit rubric incl. an ambiguous-case default; classifier built correctly via one of the three routes; ML model fit on dev only; rubric/prompt or feature/word list included verbatim; classifier frozen before the test set; env-only call pattern if an API is used. | Build correct and frozen, but the rubric lacks an explicit ambiguous-case rule, or the verbatim artifact is paraphrased, or a minor build detail is off. | Classifier runs but the rubric is vague/one-line, or the ML model's fit may have seen test data, or the unsure case forces a guess. | No working classifier, or the build is not reproducible from what is submitted. | **8** |
| **Presentation & honest write-up** (whole assessment). Clean prose in the book's voice; the measurement-instrument framing is explicit; reports the validation *before* any downstream interpretation; states which limitations are intrinsic vs. fixable; admits where the student is unsure rather than overclaiming. | One stylistic/labeling lapse; honesty present but a touch thin. | Several lapses; presents an unvalidated label as a finding; overclaims. | Unreadable, or asserts the classifier "works" with no validation shown. | **10** |

**Total: 100 points.** (Validation rigor 24 + leakage/limitations honesty 20 + reproducibility/disclosure
18 + classifier-build correctness 8 + presentation/honesty 10 = 80 from Part A and the honesty thread;
Part B's 20 points are folded in — B1, B3 into the leakage/limitations row [10] and B2 into validation
rigor, B4 into reproducibility. The rubric is normalized so the maximum awarded is 100.) The three
heaviest rows — validation rigor, leakage honesty, reproducibility — sum to **62**, more than three
times the weight on the build itself. Build a mediocre-but-honest classifier well-validated over a
brilliant one you cannot defend.

A note on the spirit of the honesty thread. Week 6 rewards the student who writes, unprompted, "my
held-out test is only 20 items, so my macro-F1 of 0.78 has a 95% CI of roughly [0.6, 0.9] and I would
not stake a headline regression on it without a label-error correction" — and who refuses to launder
"the model sounded confident" into "the labels are correct." A report that *admits* low recall on the
rare class and explains what that does to a downstream coefficient outscores one that reports a single
glossy accuracy number and stops. Knowing *what kind of claim* your classifier supports — a measurement
under a stated error rate, never the truth — is the entire point of the week.

---

## Instructor guidance and answer key

This is partly an open-ended build, so the key is a set of *standards* plus worked metric computations.
The two highest-signal things to grade: (1) **Did the student report metrics on a genuinely held-out
test, with per-class + macro P/R/F1 and kappa, and never lean on bare accuracy?** and (2) **Is the
leakage audit real** — both pipeline (test never touched the build, scored once) and training-data
(cutoff stated, task classified contemporaneous vs. predictive)? A student who does these two things
honestly has the Week-6 mindset regardless of how fancy the classifier is. Watch for the two classic
failures: (a) tuning the prompt or threshold against the test labels and reporting the result as OOS
(silent leakage — caps the validation row), and (b) any hard-coded key, which caps the reproducibility
row at Missing on its own per CONVENTIONS §5.

### Worked metric computations (so graders can check student arithmetic)

**Binary worked example** (the §6.5.4 / pack numbers). Suppose the held-out test gives, for the
`LAYOFF` class: $TP=80,\ FP=20,\ FN=40,\ TN=60$ ($n=200$).

- Precision $=80/(80+20)=0.80$. Recall $=80/(80+40)=0.667$.
- $F_1=2\cdot(0.80\cdot0.667)/(0.80+0.667)=2\cdot0.533/1.467=0.727$.
- Accuracy $=(TP+TN)/n=(80+60)/200=0.70$.
- This is a "screening, not headline" classifier: good enough to flag candidates, not to drop a label
  column straight into a regression without an error-rate correction. A student who says exactly this
  earns the interpretation marks.

**Why accuracy lies under imbalance (B2 key).** Base rate 8% layoffs, classifier predicts
`NOT_LAYOFF` for all $n$. Then $TP=0,\ FP=0,\ FN=0.08n,\ TN=0.92n$.

- Accuracy $=0.92$ — looks great.
- `LAYOFF` recall $=0/(0+0.08n)=0$ — catches none of the class you care about.
- `LAYOFF` precision $=0/(0+0)$ is **undefined** (no positive predictions); by convention report it as
  0 or "n/a" and flag the degenerate case. The cleanest single exposer is **recall on the rare class
  (0)**. Macro-F1 also flags it: the `LAYOFF` $F_1=0$, so even if `NOT_LAYOFF` $F_1\approx0.96$, macro-F1
  $\approx0.48$ — far from the 0.92 accuracy. Accuracy hides the failure because it is dominated by the
  92% majority class.

**Cohen's kappa worked example (A.3d key).** Two raters (or model vs. human) on $n=50$ binary items.
Observed agreement on 40 → $p_o=0.80$. Suppose the human called `LAYOFF` 20% of the time and the model
called `LAYOFF` 30% of the time. Chance agreement
$p_e=(0.20\cdot0.30)+(0.80\cdot0.70)=0.06+0.56=0.62$. Then
$\kappa=(0.80-0.62)/(1-0.62)=0.18/0.38=0.474$ — "moderate" agreement, and notably *lower* than the
raw 80% agreement suggests, because much of that 80% was expected by chance. Reward students who note
that raw agreement overstates reliability and that kappa is the honest number; penalize those who
report 80% agreement as if it were kappa.

**Macro vs. micro (A.3c key).** Macro-F1 averages the per-class F1s equally; micro-F1 pools all
TP/FP/FN and reduces to accuracy in the single-label case. Under imbalance, micro/accuracy is dominated
by the majority class, so a classifier can post high micro-F1 while failing the rare class. Macro-F1
gives the rare class equal vote, which is why it is the right headline for an imbalanced finance corpus.

### Model-answer sketches for Part B

**B1 (measurement, not causality).** A strong answer says: validation establishes *construct/criterion
validity* — that the `LAYOFF` label reliably captures actual layoff announcements (low measurement
error vs. the gold set) — which is a statement about the *instrument*, not about what layoffs *do* to
prices. A causal claim additionally needs an identification strategy (an event study with a clean
window, or exogenous variation in layoffs), exactly the Week-5 machinery; the classifier only supplies
a *measured regressor*, and if that regressor is mismeasured it attenuates or biases the coefficient
(Week 1). Good answers tie this to a Week-6 paper: KPSS *validate* their patent-value measure against
citations and future growth before using it — the validation table, not the measure's name, is what
earns trust; an LLM label needs the same.

**B2 (accuracy under imbalance).** See the worked numbers above: accuracy $0.92$, `LAYOFF` recall $0$,
`LAYOFF` precision undefined. Cleanest exposer = rare-class recall (0). Macro-F1 ($\approx0.48$) flags
it because it weights the failed minority class equally; accuracy ($0.92$) hides it because the 92%
majority dominates. Full credit names the undefined precision and explains *why* it is undefined (zero
positive predictions).

**B3 (look-ahead leakage).** The mechanism: the model's training cutoff postdates Jan-2021, so it has
likely *read* what 2021 stocks did; its "prediction" is recall of memorized outcomes, not inference,
producing fake spectacular backtest performance that evaporates on truly unseen forward data. The honest
fix: test out-of-sample on text *after* the model's cutoff where it cannot have peeked, or recast the
task as *contemporaneous* (e.g., "what risk does this 2021 filing disclose?") rather than *predicting*
2021 returns. The uncontaminated contrast: labeling the *tone* of the same Jan-2021 filing is
contemporaneous — it needs no knowledge of 2021 returns — so it is comparatively safe; predicting the
return is exactly where leakage bites.

**B4 (disclosure).** (a) Label generation is *data generation* → disclose the exact model version,
provider, date range, and the verbatim rubric, and include the OOS precision/recall/F1/kappa validation
table; without validation the labels are unfalsifiable. (b) Prose rewriting is a *writing aid* → disclose
that AI edited the prose, but it needs no validation table; the only obligation is that every word is
true and yours. (c) Suggested citations are the *most dangerous* — LLMs fabricate perfectly-formatted
references to papers that do not exist — so every suggested citation must be verified against a real
index (Google Scholar / DOI / the journal) *before* it enters the paper, and anything unverifiable is
tagged `[CHECK]` per CONVENTIONS §6, never cited on the model's say-so. The principle: AI as a writing
aid demands only truthful, owned words; AI as a data generator demands validation; AI as a fact/citation
source demands independent verification.

### What a top report looks like, in one paragraph

It defines the task in the measurement form with a full rubric; hand-labels ≥60 random snippets and
holds out ≥20 in a seeded, stratified split; builds (say) a TF-IDF logistic regression fit on dev only,
or an LLM classifier with the rubric cached and keys read from the environment; scores the *frozen*
classifier on the test set *once*; reports a labeled confusion matrix, per-class and macro
precision/recall/F1, classifier–human kappa, and a bootstrap CI on macro-F1 with $n$ stated, refusing to
headline accuracy and explaining why; audits both leakage types and states the task is contemporaneous;
commits the gold set, the split seed, the saved label file, and (if an API was used) the JSONL log with
no secret anywhere; and closes by stating plainly what the labels can and cannot support — a measurement
under a reported error rate, not the truth, and certainly not causality. That report would survive a
referee, which is the only standard Week 6 cares about.
