# Problem Set 6.5 — An LLM Classifier as a Measurement Instrument: Held-Out Validation and a Leakage Audit

*Covers Ch 6.5 (The AI Co-Pilot for Research, especially §6.5.4 validation, §6.5.5 critical limits, §6.5.6–6.5.7 reproducibility and disclosure) and builds directly on **Week 1**: measurement error (Ch 1.3), look-ahead bias and p-hacking (Ch 1.5). It also leans on Ch 6.3, the Loughran–McDonald finance sentiment dictionary, as the transparent cousin of an LLM label. Methods allowed: everything through Ch 6.5. **The single idea that runs through the whole set:** an LLM-produced label is a **measurement** — a noisy proxy produced by an instrument (the model + your rubric) — and like any instrument it is worthless until you have calibrated it against ground truth, out of sample, and reported how badly it can be wrong. A confident label is not a true label. Show your reasoning; a boxed number with no argument earns no credit, and "the model is very accurate" is never an answer — it is the question.*

**Total: 100 points.** Six tasks, escalating. Task 1 is the conceptual core (why an LLM label is a measurement, not the truth, in Week-1 language). Task 2 is a full confusion-matrix computation — per-class and macro precision, recall, and F1, **by hand** — for a three-class 8-K event classifier. Task 3 is the class-imbalance trap: why raw accuracy lies, and why a useless classifier can "beat" a useful one on accuracy. Task 4 is a Cohen's-kappa computation (LLM labels vs. a human coder), and why raw agreement flatters. Task 5 is a look-ahead / training-data-leakage **audit**: spot why an LLM backtest is contaminated and write the date-filter fix. Task 6 is reproducibility and disclosure — what to log, pin, and disclose, and how prompt-induced p-hacking sneaks in.

A note on numbers. Every count in this set is a **labeled illustrative value** — small, clean integers chosen so you can do the arithmetic by hand and *see* the mechanism. They are not transcribed from any real study. When you run **nb6.5 (the AI co-pilot lab)** in Task 6 you will compute the same quantities on a real hand-labeled 8-K dataset and get your own numbers, with bootstrap confidence intervals.

The recurring setting. Leah, working on text-as-data, builds an LLM classifier that reads each firm's **8-K filing** (the "current report" a public company files for material events) and assigns the *type* of event it announces. She uses three labels:

- **GUIDANCE** — the 8-K announces or revises forward earnings guidance.
- **M&A** — the 8-K announces a merger, acquisition, or divestiture.
- **OTHER** — anything else (executive changes, routine disclosures, etc.).

She has 40,000 8-Ks she cannot read by hand, and a regression she wants to run (do M&A-type 8-Ks move the stock more than guidance-type 8-Ks?). Before any of those 40,000 LLM labels enters that regression, she must prove the labels are a measurement she can defend. That proof is this problem set.

---

## Task 1 — Why an LLM label is a measurement, not the truth (14 points)

Before any arithmetic, fix the idea that makes the rest of the set matter. In Chapter 1.3 you learned that when you cannot observe a latent quantity directly, you observe it through an *instrument* that returns a **noisy proxy** — the truth plus measurement error — and that a mismeasured regressor has consequences you can sometimes sign and sometimes cannot.

**(a) (4 pts)** State, in Week-1 language, the precise sense in which Leah's LLM label "M&A" is a **measurement** of an 8-K's true event type and not the event type itself. Name the *latent* quantity, name the *instrument*, and identify the **systematic** and the **random** component of the measurement error with one concrete example of each (e.g., what would make the instrument biased in one direction; what would make the same filing get two different labels on two runs).

**(b) (4 pts)** Suppose Leah skips validation, takes the 40,000 LLM labels as if they were ground truth, and runs her regression of the 8-K's three-day abnormal return on a dummy for "M&A-type" (vs. the rest). The "M&A" dummy is mismeasured — sometimes the model tags a true M&A as OTHER and vice-versa. Using the Week-1 result on mismeasured regressors, state what this label error does to her estimated coefficient in the **benign** case (classical, non-differential measurement error) — which direction, and what happens to the standard error — and then describe one **non-benign** case where the error is *correlated with something* and the bias can no longer be signed. (Hint for the non-benign case: what if the model mislabels small firms' 8-Ks differently from large firms', and firm size also drives the return?)

**(c) (3 pts)** In Ch 6.3 you met the Loughran–McDonald (LM) finance sentiment dictionary, which labels a filing's tone by counting words from a fixed, published list. Both LM and the LLM are *instruments* that turn text into a label. Explain why the LLM, even if it is **more accurate** than LM, raises the bar on validation rather than lowering it — i.e., what property does LM have that the LLM lacks, and why does that property matter to a referee?

**(d) (3 pts)** Leah's lab partner says: "We don't need to validate. The model said it's 94% accurate at this kind of task." Give the **two** distinct reasons this sentence is not a substitute for Leah's own validation, drawing on §6.5.4. (One reason is about *whose data and which base rate*; the other is about *in-sample vs. out-of-sample* and who is grading whom.)

---

## Task 2 — Build the confusion matrix; compute precision, recall, F1, and macro — by hand (22 points)

Leah hand-labels a **gold set** of 147 8-Ks (the closest thing she has to ground truth), then runs her frozen LLM classifier on the same 147 filings. The cross-tabulation of LLM label (rows) against gold label (columns) is below. A cell is the count of filings the LLM put in that row whose true label is that column; the diagonal is correct.

| LLM \ Gold | Gold: GUIDANCE | Gold: M&A | Gold: OTHER | **Row total** |
|---|---|---|---|---|
| **LLM: GUIDANCE** | 38 | 4 | 6 | 48 |
| **LLM: M&A** | 3 | 22 | 5 | 30 |
| **LLM: OTHER** | 9 | 4 | 56 | 69 |
| **Column total** | 50 | 30 | 67 | **147** |

This is a *multiclass* problem, so precision, recall, and F1 are computed **per class**, treating each class in turn as "the positive class" and lumping the other two as "negative" (the *one-vs-rest* convention). The formulas, from §6.5.4:

$$\text{Precision}_c = \frac{TP_c}{TP_c + FP_c}, \qquad \text{Recall}_c = \frac{TP_c}{TP_c + FN_c}, \qquad F_{1,c} = 2\cdot\frac{\text{Precision}_c\cdot\text{Recall}_c}{\text{Precision}_c+\text{Recall}_c}.$$

Here, for a fixed class $c$: $TP_c$ is the diagonal cell (LLM said $c$, truth is $c$); $FP_c$ is the rest of the LLM-said-$c$ **row** (LLM said $c$, truth was something else — a false alarm); $FN_c$ is the rest of the truth-is-$c$ **column** (truth was $c$, LLM said something else — a miss).

**(a) (3 pts)** For the **GUIDANCE** class, read off $TP$, $FP$, and $FN$ from the table. State in one sentence each what the $FP$ count and the $FN$ count *mean* in plain English about Leah's classifier (a false alarm of what; a miss of what).

**(b) (6 pts)** Compute precision, recall, and F1 for **each** of the three classes (GUIDANCE, M&A, OTHER). Show the fraction and a decimal to three places for each of the nine numbers. (You will compute $TP$, $FP$, $FN$ for M&A and OTHER the same way you did for GUIDANCE in part (a).)

**(c) (4 pts)** Compute the three **macro-averaged** scores: macro-precision, macro-recall, and macro-F1, each the simple unweighted mean of the three per-class values. Then compute the overall **accuracy** $(TP_{\text{GUIDANCE}}+TP_{\text{M\&A}}+TP_{\text{OTHER}})/N$. Report all four to three decimals.

**(d) (4 pts)** Look at your per-class table. Leah's downstream regression compares **M&A** 8-Ks against the rest, so the **M&A** row is the one that matters most for her result. In one short paragraph, interpret M&A's precision and recall *for her specific use*: when the model tags a filing "M&A," how often is it really an M&A, and of all the true M&As, how many did she catch? Which of the two errors (a non-M&A wrongly tagged M&A, or a true M&A missed) is more damaging to a regression that compares the M&A group's average return to everyone else's, and why?

**(e) (5 pts)** Leah reports the macro-F1 of 0.78 to her mentor, who replies: "A single point estimate from 147 filings is not enough — give me a confidence interval, especially on the M&A class." Explain *why* the macro-F1 alone is insufficient, and be specific about the M&A class: how many filings did the model *predict* as M&A (the denominator of M&A precision), and why does a precision estimated on that few predicted-positives have a **wide** interval? (You do not need to compute the interval by hand — that is nb6.5's job — but state which count is small, and what that smallness does to the reliability of the M&A precision number.)

---

## Task 3 — Why raw accuracy lies under class imbalance (16 points)

Leah's *next* project is rarer and higher-stakes: a binary flag for whether a 10-K shows **material financial distress** (going-concern doubt, covenant breach, liquidity crisis). She hand-labels a gold set of **500** filings; only **25** of them (5%) are truly distressed. "Distressed" is the positive class and the one her fair-lending-adjacent research question actually cares about.

She compares two classifiers on this gold set.

- **Classifier A — the lazy baseline.** It labels **every** filing "not-distressed."
- **Classifier B — the real LLM classifier.** On the 25 truly distressed filings it correctly flags 20 (and misses 5); among the 475 truly-not-distressed filings it wrongly flags 30 as distressed.

**(a) (3 pts)** Write out the 2×2 confusion matrix (positive class = distressed) for **each** classifier. For Classifier A, fill in $TP, FP, FN, TN$; for Classifier B, fill in $TP=20$, $FP=30$, $FN=5$, and compute $TN$.

**(b) (4 pts)** Compute the **raw accuracy** $(TP+TN)/N$ of each classifier. Report both to four decimals. State the result that should alarm you: which classifier has the *higher* accuracy?

**(c) (4 pts)** Now compute **precision, recall, and F1 for the distressed class** for **each** classifier. For Classifier A, explain what goes wrong with the precision formula specifically, and what its recall is. Put the two classifiers side by side and state, in one sentence, why the accuracy ranking from (b) is exactly backwards from what Leah's research question needs.

**(d) (3 pts)** Explain *why* accuracy is the wrong headline number here, in terms of the **base rate**. Connect it to a fraud detector or a rare-disease test: when the positive class is 5% of the data, what accuracy does a classifier earn for free by doing nothing, and why does beating that number require essentially zero skill? Name the quantity Leah should report instead, and why it exposes what accuracy hides.

**(e) (2 pts)** Tie it back to §6.5.4's warning about vendor claims. A model card advertises "96% accuracy on distress detection." Using your numbers, explain why that figure could be *worse than useless* as a guide to whether Leah should trust the labels — i.e., what single additional number would tell her whether 96% is impressive or trivial.

---

## Task 4 — Cohen's kappa: LLM labels vs. a human coder (16 points)

To check how good her gold labels even are — and to compare the LLM against a second human — Leah has a research assistant independently label the same 100 filings as **NEGATIVE** tone or **NOT-NEGATIVE**. She wants a number for how much the LLM and the human agree *beyond what they would agree by chance alone*, because two coders who both call almost everything "not-negative" will agree most of the time for free. That number is **Cohen's kappa**.

The cross-tabulation of the human coder (rows) against the LLM (columns), $N = 100$:

| Human \ LLM | LLM: NEGATIVE | LLM: NOT-NEG | **Row total** |
|---|---|---|---|
| **Human: NEGATIVE** | 30 | 10 | 40 |
| **Human: NOT-NEG** | 6 | 54 | 60 |
| **Column total** | 36 | 64 | **100** |

Cohen's kappa is

$$\kappa = \frac{p_o - p_e}{1 - p_e},$$

where $p_o$ is the **observed** proportion of agreement (the diagonal over $N$) and $p_e$ is the agreement **expected by chance** if the two coders labeled independently with their own observed marginal rates: $p_e = \sum_{\text{labels } \ell} \Pr(\text{human}=\ell)\cdot\Pr(\text{LLM}=\ell)$.

**(a) (3 pts)** Compute $p_o$, the observed (raw) agreement. Show the cells you summed and report a decimal. State why this number, on its own, can be misleadingly high here.

**(b) (5 pts)** Compute $p_e$, the chance agreement. Write the human's and the LLM's marginal proportions for each label, then combine them as the formula requires. Show the arithmetic and report $p_e$ to four decimals.

**(c) (3 pts)** Plug into the formula and compute $\kappa$ to four decimals. Show the numerator $p_o - p_e$ and the denominator $1 - p_e$ explicitly.

**(d) (3 pts)** Interpret the result. By the usual (Landis–Koch) rough guideposts — $\le 0$ none, $0.01$–$0.20$ slight, $0.21$–$0.40$ fair, $0.41$–$0.60$ moderate, $0.61$–$0.80$ substantial, $0.81$–$1.00$ almost perfect — where does your $\kappa$ land? Contrast the *story told by the raw agreement* $p_o$ with the *story told by* $\kappa$, and explain in one sentence what the gap between them is "charging" the coders for.

**(e) (2 pts)** Leah's partner says, "Kappa is for two *humans*. The LLM isn't a coder, so this doesn't apply." Rebut this in two sentences using the Task-1 framing: in what sense *is* the LLM "a coder" here, and what does a high LLM-vs-human kappa buy you that the precision/recall table against the gold set does not?

---

## Task 5 — Look-ahead bias / training-data leakage: audit the backtest, then fix it (18 points)

This is the failure mode §6.5.5 calls "subtle, specific to finance, and fatal." Sam, excited by Leah's classifier, proposes a trading strategy and runs a backtest.

> **Sam's design.** "I take every firm's 8-K filed in **2021**. I feed the filing text to the LLM (training cutoff: text through **2024**) and ask: *'Based on this filing, will this stock outperform the market over the next 12 months? Answer UP or DOWN.'* I buy the UP names, short the DOWN names, hold a year. Backtested over 2021, the strategy earns a spectacular 31% — way above the market. I'm going to pitch it as my capstone."

**(a) (5 pts)** Diagnose the contamination precisely. Name the bias, state the model's training cutoff relative to Sam's sample period, and explain the exact mechanism by which the "prediction" is not a prediction. What information, knowable to the model but **not** knowable to a trader standing in early 2021, is leaking into the answer? Tie it explicitly to the Ch 1.5 definition of look-ahead bias ("information from the future entering a decision that should use only past information").

**(b) (4 pts)** Sam objects: "But I only gave it the 2021 filing text — I never showed it the 2021 returns. So how can it be cheating?" Answer him. Explain why withholding the outcome *at query time* does **not** prevent leakage when the outcome is baked into the model's **training data**, and why this makes the spectacular 31% a near-certainty to **evaporate** the moment the rule is traded forward on filings the model has never seen.

**(c) (4 pts)** Contrast two tasks Sam could run on the *same* 2021 filings, and explain why one is comparatively safe from leakage and the other is exactly where leakage bites:
  - **Task X:** "Classify the *tone* of this 2021 8-K's risk section (NEGATIVE/NEUTRAL/POSITIVE)." — a *contemporaneous attribute*.
  - **Task Y:** "Predict the stock's 2021–22 *return* from this 2021 8-K." — a *forward outcome*.

  Which is comparatively safe and why? State the general rule §6.5.5 gives for telling the two apart.

**(d) (5 pts)** **Write the fix.** Give the four-part defense from §6.5.5, then make the RAG date-filter concrete. Sam's strategy retrieves supporting passages from a vector index of filings to ground each UP/DOWN call. Write pseudocode (or precise prose) for the retrieval step that **mechanically** prevents a query dated time $t$ from ever retrieving a chunk whose metadata date is **after** $t$ — i.e., the date-filter on the metadata that §6.5.3 said every chunk must carry. State the one-line invariant the filter enforces, and explain why the *cleanest* defense of all is to test the strategy out-of-sample on filings created **after** the model's training cutoff.

---

## Task 6 — Reproducibility, disclosure, and prompt-induced p-hacking (14 points)

Leah's classifier is validated (Tasks 2–4) and leakage-audited (Task 5). Now she has to make the AI-assisted pipeline survive a referee and a replicator — the §6.5.6–6.5.7 disclosure-and-reproducibility standard, which is exactly what the Week 6 assessment grades.

**(a) (4 pts)** A regression is deterministic; an LLM is, by default, stochastic. Explain in two-to-three sentences *why* re-running the same classification prompt can return different labels, and why that is a reproducibility problem for a research instrument. Then state the single most robust fix from §6.5.5 — the one that does **not** depend on the model being deterministic — and why "set temperature to 0" is *not* a sufficient guarantee on its own (cite the specific caveat the chapter raises about current frontier models such as Opus 4.7).

**(b) (4 pts)** List the four things Leah must **log, pin, or save** so that someone with only her repository can reconstruct her label column. For each, say in a phrase what breaks if she omits it. (Draw on §6.5.6 audit logging and §6.5.7: the JSONL call log; the exact model *version string*; the API version / seed / temperature where they exist; and the saved label file as data.) Then explain why §6.5.6 logs a **SHA-256 hash** of the prompt rather than the raw prompt when the input contains licensed text.

**(c) (4 pts)** **Prompt-induced p-hacking.** Define it in one sentence, then explain why it is *arguably worse* than the classic Week-1 p-hacking. Walk through the specific bad loop: Leah's M&A coefficient is insignificant; she rewords the M&A rubric ("merger OR strategic-investment language"); now it is significant; she stops and reports the lucky prompt. Name the one researcher degree of freedom she exploited, and state the §6.5.5 defense that **structurally** prevents it — i.e., what target the prompt should be frozen against, and *before* looking at what.

**(d) (2 pts)** Write the two-to-three sentence **AI-use disclosure paragraph** Leah should put in her capstone's methods section, per the §6.5.7 checklist. It must distinguish AI used as a *writing aid* from AI used to *generate data*, name what gets validated, and point to where the verbatim rubric lives. (You are writing the actual paragraph, not describing it.)

---

*End of PS 6.5. Solutions in `book/appendices/E-solutions-manual/E-w6-ps6.5-solutions.md`. This set is the active-validation companion to **Ch 6.5 §6.5.4–6.5.7** and the direct sequel to **Week 1**: every task here is a Week-1 idea (measurement error, look-ahead bias, p-hacking) wearing an LLM costume. The thread of the whole week, from the Reading Guide Pack to Mentor Session 6: a text-as-data paper asks "is this measure valid?", and an LLM label **is** a measure — so the skepticism you brought to Loughran–McDonald and Hoberg–Phillips is exactly the skepticism you must bring to your own prompt's output. Now open **nb6.5 (the AI co-pilot lab)** and compute every number above — confusion matrix, per-class and macro precision/recall/F1, Cohen's kappa, the date-filter, the JSONL audit log — on a real hand-labeled 8-K dataset, with bootstrap confidence intervals on the scores this set asked you to estimate by hand.*
