# Chapter 6.5 — The AI Co-Pilot for Research (LLM-in-the-Loop)

Leah is three weeks into her capstone on patents and innovation. She has 40,000 firm-year 10-K filings to read, a data dictionary for the USPTO PatentsView tables that runs to ninety pages, a regression that throws an error she does not understand, and a deadline. She opens a chat window with a large language model and types: *"Read these filings and tell me which firms are innovative."* Twenty seconds later she has a confident, fluent, well-organized answer. It is also, in places, completely made up — and the parts that are made up look exactly like the parts that are true.

This chapter is about that last sentence. A large language model (LLM) — a system like Claude or GPT, trained to predict the next token of text and tuned to follow instructions — is the most useful new research tool to arrive in empirical finance in a generation, and also the most dangerous, *for the same reason*: it produces fluent, plausible text on demand, whether or not that text is grounded in anything real. The skill this chapter teaches is not "how to use an LLM." You already know how to type into a box. The skill is how to use one *so that your results survive a referee* — how to extract the genuine help (and it is genuine and large) while building the guardrails that stop a confident-sounding model from quietly corrupting your data, your code, and your conclusions.

We will follow the reveal-the-trick structure the whole book uses: state what the tool actually does, see *why* it helps on a concrete task, see *when and how it fails* (in detail, because the failures are subtle and expensive), and then show the code. By the end you should be able to do four things that separate a researcher from a chatbot user: write prompts that constrain the model instead of inviting it to improvise; build a retrieval pipeline that forces answers to be grounded in source documents; treat every LLM-produced label as a *measurement* that must be validated against hand-coded truth before you trust it; and log every API call so your AI-assisted work is as reproducible and disclosable as a regression table. Everything here connects forward to Mentor Session 6 ("Text as data, and AI without fooling yourself") and to your capstone, where you will have to *disclose and defend* every way you used a model.

---

## 6.5.1 Co-pilot, not autopilot

Here is the framing in one sentence: **an LLM is a co-pilot — it accelerates work you could verify yourself, and it is a hazard exactly when you use it to replace judgment you cannot or do not check.** The aviation metaphor is worth taking literally. A co-pilot reduces the captain's workload, catches routine errors, and handles the tedious legs — but the captain remains responsible for the aircraft, signs the logbook, and is the one the inquiry calls when something goes wrong. An autopilot flown into terrain by a crew that stopped watching the instruments is the cautionary tale. In research, *you* are the captain. The model never signs your paper.

So where does the co-pilot genuinely help? Five places, each of which shares one property: **the output is cheap for you to verify, or the cost of an occasional error is low.**

The first is **literature triage**. You have 200 abstracts returned by a search and two days. An LLM can sort them into "directly relevant / tangential / off-topic," summarize the method of each, and flag the three that seem closest to your design. You then read those three yourself. The model did not decide what matters; it triaged so that your limited reading time landed on the right papers. If it miscategorizes one, you lose little, because you were going to skim the borderline cases anyway.

The second is **parsing data dictionaries and documentation**. The PatentsView schema, the CRSP variable definitions, the WRDS query syntax, the eight ways Compustat encodes a missing value — this is exactly the dense, structured, tedious reference material an LLM reads well. "In the CRSP daily stock file, what is the difference between `RET` and `RETX`, and how is a delisting return encoded?" is a question the model can usually answer, and a question you can *check against the manual in thirty seconds*. The verification is fast, so the speedup is real and safe.

The third is **code review and debugging**. Paste your function and the traceback and ask what is wrong. The model is often right, and when it is wrong you find out immediately because the code either runs or it does not. This is the safest use of all, because the verifier is a Python interpreter, not your own credulity. We will write a code-review prompt pattern in §6.5.2.

The fourth is **drafting and rewriting prose** — turning your rough bullet points into a paragraph, tightening a wordy methods section, suggesting a clearer way to phrase a result. You read every word it produces and you own every word you keep, so the only risk is laziness.

The fifth, and the one this chapter treats most seriously, is **classifying or extracting structured information from text at scale**: reading 40,000 filings and labeling each one's risk-factor tone, or pulling the CEO's name out of every proxy statement, or tagging each 8-K with the type of event it reports. This is where LLMs do something genuinely new and powerful — and it is *also* where they are most dangerous, because the output is a column of numbers that flows straight into a regression, and you cannot eyeball 40,000 labels to check them. The entire methodological core of this chapter (§6.5.4) is about how to make this use safe.

Now the dangerous places, stated just as plainly. An LLM is a hazard whenever **you cannot cheaply verify the output and an error is costly.** Three patterns recur. (1) *Facts you can't check at a glance* — "what is the coefficient in such-and-such paper," "what was the 2008 default rate on subprime ARMs" — where the model will produce a specific, confident number that may be invented. (2) *Anything where the model may "know" your answer for the wrong reason* — most insidiously, knowing the future relative to your sample, which we will see is a fatal bias in backtests (§6.5.5). (3) *Anything you would be tempted to keep only because you like the result* — using the model to generate the framing, the hypothesis, *and* the supporting evidence is a closed loop with no contact with reality. The rest of the chapter is a set of techniques for staying in the safe column and detecting when you have drifted into the dangerous one.

---

## 6.5.2 Prompt patterns for empirical work

A prompt is an instruction, and the difference between a useful answer and a dangerous one is usually written into the instruction itself. The governing principle: **a good empirical prompt constrains the model's degrees of freedom — it tells the model exactly what to produce, what to do when it is unsure, and what format to use — while a bad prompt leaves room for the model to improvise, flatter, or fabricate.** We will build four reusable patterns. For each, contrast a bad version with a good one; the gap between them is the whole lesson.

### Pattern 1 — Precise extraction

You want one fact from each of a thousand documents. The temptation is to ask conversationally.

> **Bad:** "What can you tell me about this company's risk factors?"

This invites a paragraph of free prose that varies in structure from document to document, mixes the fact you want with editorializing, and cannot be parsed into a column. Worse, it does not say what to do when the fact is absent, so the model will often invent something rather than admit a gap.

> **Good:** "From the 10-K text below, extract the company's *primary* stated risk factor in 10 words or fewer. Return only a JSON object of the form `{\"risk\": \"...\"}`. If the filing does not state a clear primary risk, return `{\"risk\": null}`. Do not infer or add risks that are not explicitly stated in the text."

The good prompt fixes the output type (JSON, parseable), bounds the length, defines the *unsure* case explicitly (`null`, not a guess), and forbids inference. Every one of those clauses closes a door the model would otherwise wander through. The phrase "do not infer or add risks that are not explicitly stated" is doing real work: extraction tasks should pull text that *is there*, never synthesize text that *should be* there.

### Pattern 2 — Cite-or-say-you-don't-know

When you ask a model for facts, the single most valuable instruction you can give is permission to admit ignorance. Models fabricate partly because their training rewards helpful-sounding completions; an empty "I don't know" looks unhelpful next to a confident paragraph. You have to explicitly make "I don't know" the *correct* answer.

> **Bad:** "What does the literature say about whether 10-K sentiment predicts returns?"

The model will happily produce a literature review complete with author names, years, journals, and findings — some real, some plausible fiction. You cannot tell which is which from the text.

> **Good:** "Using only the source documents I have provided below, answer the question. Quote the specific sentence that supports each claim, and give the document ID it came from. If the provided documents do not contain the answer, respond exactly: 'Not supported by the provided sources.' Do not use outside knowledge."

This pattern only fully works when you actually provide the sources — which is what retrieval-augmented generation (§6.5.3) is for. But even without retrieval, the instruction "if you are not sure, say so" measurably reduces fabrication. The deeper move is *requiring a quotable, locatable citation for every claim*, because a claim that must point to a specific sentence in a specific document is a claim you can falsify in seconds.

### Pattern 3 — Code review

> **Bad:** "Is this code good?"

"Good" is undefined, so you get vague praise or vague concern, and the model — tuned to be agreeable — tends toward praise. Agreeableness is a real failure mode: a model asked "is this right?" leans toward "yes."

> **Good:** "Review the Python function below for *correctness* bugs only — off-by-one errors, wrong axis in a pandas operation, look-ahead bias in the feature construction, incorrect handling of missing values, or merge keys that don't uniquely identify rows. For each issue, quote the exact line and explain the bug in one sentence. If you find no correctness bugs, say 'No correctness bugs found' — do not invent stylistic suggestions to seem useful."

Naming the *categories* of bug focuses the model on the failure modes that actually matter in empirical code (we will meet look-ahead bias again in §6.5.5, and non-unique merge keys are the silent killer of panel datasets). The final clause — do not invent suggestions to seem useful — counteracts the agreeableness bias directly. Note the symmetry with Pattern 2: in both, you are explicitly making "nothing to report" an acceptable, even rewarded, answer.

### Pattern 4 — Rubric-based classification

This is the pattern your capstone will lean on hardest, so it gets the most care. You want to assign each document to one of a fixed set of categories, *consistently*, across thousands of documents. Consistency is the whole game: a classifier that uses a slightly different definition of "negative" on document 5,000 than on document 5 has injected noise — measurement error — into your data.

> **Bad:** "Is this filing's tone positive or negative?"

"Tone," "positive," and "negative" are undefined, so the model supplies its own definitions, and they may drift across documents or differ from yours. Two researchers running this prompt get different label columns; that is the opposite of a measurement.

> **Good:** A *rubric* — an explicit, written decision rule, ideally with examples for the boundary cases:

```text
You are classifying the tone of the "Risk Factors" section of a 10-K
filing. Assign exactly one label:

  NEGATIVE  — the section emphasizes new or worsening threats to the
              business (litigation, liquidity, going-concern doubt,
              loss of a major customer).
  NEUTRAL   — the section restates standard, boilerplate risks common
              to most firms in the industry, with no emphasis on
              deterioration.
  POSITIVE  — the section explicitly notes that a previously disclosed
              risk has been resolved or materially reduced.

Rules:
- Judge only the text provided. Do not use outside knowledge about
  the company.
- Boilerplate language ("our business is subject to economic
  conditions") is NEUTRAL, not NEGATIVE.
- If genuinely ambiguous, choose NEUTRAL.

Return only the label word.
```

A rubric does three things a one-line prompt cannot. It *pins down* the categories so the model's definitions match yours; it *handles the ambiguous case* with an explicit default rather than letting the model coin-flip; and — critically — it is a written artifact you can put in your paper's appendix so a referee or replicator sees *exactly* how each label was produced. That last point is the bridge to the rest of the chapter: a rubric is to LLM classification what a variable definition is to a regression. It is part of your measurement protocol, and it must be disclosed.

One more discipline applies to all four patterns: **keep the stable instruction separate from the volatile input.** The rubric above is the same for all 40,000 filings; only the filing text changes. Writing the prompt so that the fixed part comes first and the variable part comes last is not just tidy — it is what makes prompt caching work (§6.5.6) and, more importantly, what guarantees every document is judged by *identical* instructions.

---

## 6.5.3 Retrieval-Augmented Generation over 10-K filings

The cite-or-decline pattern of §6.5.2 has an obvious hole: it only works if the model has the right source text in front of it. A model's parametric knowledge — the facts baked into its weights during training — is a blurry, lossy compression of its training data, with no clean way to separate what it "knows" from what it confabulates. So instead of asking the model to recall, we *hand it the relevant source text at query time* and ask it to answer from that. This is **retrieval-augmented generation (RAG)**, and it is the standard architecture for question-answering over a private document collection like a folder of 10-K filings.

The result in one sentence: **RAG grounds the model's answer in retrieved source passages, so the model summarizes documents you control instead of recalling facts it may have invented — which sharply reduces, but does not eliminate, hallucination.** Here is the pipeline, in four stages.

**Stage 1 — Chunk.** A single 10-K can run to 100,000+ words, far more than you want to stuff into one prompt, and most of it is irrelevant to any given question. So you split each filing into *chunks* — passages of, say, 500–1,000 tokens, often broken at section boundaries (Item 1A Risk Factors, Item 7 MD&A) so that each chunk is internally coherent. Each chunk keeps metadata: which filing, which firm, which fiscal year, which section. That metadata is what lets you cite the source later and — we will see in §6.5.5 — what lets you enforce that you never retrieve a chunk from the *future*.

**Stage 2 — Embed.** You convert each chunk into an *embedding* — a vector of a few hundred to a few thousand numbers that represents the chunk's meaning, produced by an embedding model. The key property, which you met in spirit in Chapter 6.2 when you computed cosine similarity between 10-K texts: passages about similar topics land near each other in this vector space, even if they use different words. "We face significant litigation exposure" and "pending lawsuits could materially harm us" sit close together because they *mean* similar things. You embed every chunk once and store the vectors in a *vector index* — a data structure (FAISS, Chroma, or even a NumPy array for a small corpus) built for fast nearest-neighbor search.

**Stage 3 — Retrieve.** When a question arrives — "What liquidity risks did this firm disclose in 2019?" — you embed the *question* with the same embedding model, then find the $k$ chunks whose vectors are nearest to the question's vector (nearest by cosine similarity, exactly the metric from Chapter 6.2). Those $k$ chunks — typically $k$ between 3 and 10 — are the passages most likely to contain the answer. This is the "retrieval" step, and it is plain nearest-neighbor search, not magic.

**Stage 4 — Ground the answer.** You build a prompt that contains the retrieved chunks *and* the question, with an instruction in the spirit of Pattern 2: "Answer using only the passages below. Cite the chunk ID for every claim. If the passages do not contain the answer, say so." The model now has the actual source text in its context window, so its job shifts from *recall* (dangerous, fabrication-prone) to *reading comprehension and summarization* (much more reliable). And because each chunk carries metadata, the answer can cite "Firm X, FY2019 10-K, Item 7" — a citation you can open and verify.

```text
SYSTEM (the grounding instruction — stable across all queries):
  Answer the question using ONLY the numbered passages provided.
  After each sentence, cite the passage number(s) it relies on,
  e.g. [3]. If the passages do not contain enough information to
  answer, respond exactly: "Not answerable from the provided passages."
  Never use information that is not in the passages.

USER (assembled per query):
  Passages:
  [1] (AcmeCorp 10-K FY2019, Item 7) "Our liquidity depends on ..."
  [2] (AcmeCorp 10-K FY2019, Item 1A) "A downgrade of our credit ..."
  [3] (AcmeCorp 10-K FY2019, Item 7) "As of fiscal year end we held ..."

  Question: What liquidity risks did AcmeCorp disclose in 2019?
```

Why does this reduce hallucination rather than eliminate it? Because RAG removes the *recall* failure mode — the model is no longer guessing facts from blurry memory — but it introduces two new ways to go wrong. First, **retrieval can fail**: if the relevant chunk is not in the top-$k$, the model answers from incomplete information, and a model handed the wrong passages can still produce a confident, wrong answer. Second, **the model can still misread or over-extrapolate** from the passages it *was* given — inventing a number that is "close to" one in the text, or stitching two passages into a claim neither supports. So RAG is a large improvement, not a guarantee. The discipline that makes it trustworthy is the same one that runs through this whole chapter: **every claim must cite a retrievable source, and you spot-check those citations.** A claim that cites passage [3] is a claim you can falsify by opening passage [3]. A claim with no citation is a claim you cannot trust, and the prompt should forbid it. (You will build a small RAG pipeline over real 10-Ks in nb6.5.)

---

## 6.5.4 LLM-assisted classification, with out-of-sample validation

This is the heart of the chapter, and it contains the single most important sentence in it: **an LLM-produced label is a measurement, not the truth — so before any LLM label enters a regression, you must validate it against a hand-labeled gold standard and report its error rate on held-out data.** Everything else here is the elaboration of that sentence. If you remember nothing else from Week 6, remember that an LLM classifier is a *measurement instrument*, and a measurement instrument that has not been calibrated against ground truth is just a confident guess.

### Why a label is a measurement

Recall Chapter 1.3 and the idea of measurement error. When you label a filing "negative tone," you are not observing the true latent quantity — the filing's actual tone — directly. You are running it through an instrument (the LLM + your rubric) that produces a *noisy proxy* for it. The instrument has a systematic component (maybe it over-calls "negative" on legal boilerplate) and a random component (the same filing might get a different label on a re-run). If you then regress, say, next-quarter returns on this label, the label is a mismeasured regressor, and you know from Week 1 what mismeasurement does: at best it attenuates your coefficient toward zero and inflates your standard errors; at worst, if the measurement error is *correlated with something*, it biases the coefficient in a direction you cannot sign. You met the benign, transparent version of this instrument in Chapter 6.3: the Loughran–McDonald (LM) finance sentiment dictionary, which labels tone by counting words from a fixed, published list. The LM dictionary's "rubric" is just a word list anyone can inspect; an LLM's rubric is your prompt plus an opaque model. The LLM may be more accurate, but it is far *less transparent*, which raises the bar on validation, not lowers it.

So the question is never "is the LLM accurate?" in the abstract. The question is "how accurate is *this* classifier, on *my* data, measured against *truth* — and is it accurate enough that my downstream result is not an artifact of label error?" You answer it the way you would validate any instrument: against a gold standard, out of sample.

### The validation protocol

Here is the procedure, step by step. It is not optional and it is not hard.

**Step 1 — Build a gold set by hand.** Draw a *random* sample of documents from your corpus — say 200 — and label each one *yourself* (or, better, have two people label independently and reconcile disagreements, which also tells you how hard the task is for humans). This hand-labeled set is your **gold standard**: the closest thing you have to ground truth. It must be a random sample, because a gold set of cherry-picked easy cases will flatter your classifier. Two hundred is a reasonable floor; the smaller the gold set, the wider the confidence intervals on everything that follows.

**Step 2 — Split the gold set.** Set aside a portion — say 50 documents — as a **held-out test set** that you will *not* look at while developing your prompt. The other 150 are your **development set**, used for writing and tuning the rubric. This split is the same discipline as a train/test split in any predictive modeling, and it exists for the same reason: if you tune your prompt until it nails the very examples you are measuring it on, your reported accuracy is optimistic garbage. The test set is touched *once*, at the end.

**Step 3 — Run the LLM on the gold set and build a confusion matrix.** For a binary task (negative vs. not-negative), the LLM's labels versus the gold labels fall into four cells:

| | Gold: Negative | Gold: Not-negative |
|---|---|---|
| **LLM: Negative** | True Positive (TP) | False Positive (FP) |
| **LLM: Not-negative** | False Negative (FN) | True Negative (TN) |

**Step 4 — Compute precision, recall, and F1 — not just accuracy.** From the confusion matrix:

$$\text{Precision} = \frac{TP}{TP + FP}, \qquad \text{Recall} = \frac{TP}{TP + FN}, \qquad F_1 = 2\cdot\frac{\text{Precision}\cdot\text{Recall}}{\text{Precision}+\text{Recall}}.$$

In words: **precision** is "when the LLM says negative, how often is it right?" — it penalizes false alarms. **Recall** (also called sensitivity) is "of all the truly negative filings, how many did the LLM catch?" — it penalizes misses. **F1** is the harmonic mean of the two, a single summary that is high only when *both* are high. Why not just report **accuracy** — the fraction of all labels that are correct, $(TP+TN)/N$? Because accuracy lies under class imbalance, and financial text is almost always imbalanced. Suppose only 5% of filings are truly "negative." A lazy classifier that labels *everything* "not-negative" scores 95% accuracy — and is useless, because its recall on the class you care about is zero. This is the same trap you would fall into reporting the accuracy of a fraud detector when fraud is rare. Precision and recall expose the lie that accuracy hides; report them, with their confidence intervals (a precision of 0.80 measured on 25 predicted-positives has a very wide interval).

**Step 5 — Report performance on the HELD-OUT test set, and report it honestly.** Tune the rubric on the development set as much as you like — try different wordings, add boundary examples, fix systematic errors you see. But the numbers that go in your paper are the precision/recall/F1 computed on the 50 test documents you set aside in Step 2, *evaluated exactly once*, after the prompt is frozen. Those out-of-sample numbers are your honest estimate of how the classifier performs on the 40,000 documents you did *not* hand-label. If precision and recall are high enough on the test set, you have earned the right to apply the classifier to the full corpus and use its labels in a regression. If they are not, you do not have a measurement — you have noise, and no amount of fluent output changes that.

The deepest point: **never trust a raw accuracy claim, including a vendor's or a model's claim about itself.** "This model achieves 94% accuracy on sentiment" is meaningless without knowing the task, the base rate, and whether the number is in-sample. Your job is to produce *your own* out-of-sample precision/recall/F1 on *your own* gold set, and to report it next to your main result so the referee can judge how much label error your conclusion can tolerate. This is exactly what the Week 6 assessment grades, and what Mentor Session 6 means by "AI without fooling yourself." (You will run this full protocol on real 8-K text in PS 6.5 and nb6.5.)

---

## 6.5.5 Critical limits

Even with good prompts, grounding, and validation, four failure modes can wreck an AI-assisted study. Each one has produced retracted or embarrassing results in practice. Learn to recognize and defuse all four.

### Hallucinated citations

An LLM asked for references will produce author lists, titles, years, journals, volume and page numbers — in perfect bibliographic format — for papers *that do not exist*. The format is correct because the model learned what citations look like; the content is fabricated because the model is generating plausible text, not querying a database. This has already embarrassed lawyers who filed briefs citing invented cases and students who submitted bibliographies of phantom papers. The danger in finance research is identical: a fabricated "Smith & Jones (2014) found a 3% effect" sentence is indistinguishable, on the page, from a real one.

How to catch it: **verify every citation against a real index** — Google Scholar, the journal's own site, a DOI lookup — *before* it enters your document. If you cannot find the paper, it is not real, no matter how confident the model was. This is precisely why the book's CONVENTIONS file (§6) demands a verifiable primary source for every empirical claim and tags anything unverifiable as `[CHECK]` rather than letting it stand. Treat an LLM as a *suggestion engine for what to go verify*, never as the citation itself. The same goes for facts and figures: a specific number from an LLM ("the 2008 charge-off rate was 4.7%") is a hypothesis to check against FRED or the original filing, not a datum to cite.

### Look-ahead bias and training-data leakage

This one is subtle, specific to finance, and fatal. A model is trained on text up to some cutoff date. If your study uses a sample that *ends before* that cutoff, then **the model may "know" things about your sample period that were not knowable at the time** — it has read the news articles, the later filings, the eventual outcomes. This is a form of **look-ahead bias**: information from the future leaking into a decision that is supposed to use only past information.

Make it concrete. Sam wants to backtest a trading rule: "ask the LLM to read each firm's January 10-K and predict whether the stock will rise that year." Sam runs it on 2021 filings. But the model was trained on text through, say, 2024 — it has very likely *read* what happened to those stocks in 2021. Its "prediction" is contaminated by hindsight. A backtest built this way can show spectacular, entirely fake performance, because the model is not predicting the future, it is *remembering* it. The result will evaporate the instant you trade it forward on data the model has never seen — which is exactly when real money is at stake. This is the LLM-era version of the look-ahead traps you guarded against in Chapter 1.5 and will guard against again in any event study: the rule must use only information available *as of* the decision date.

How to defend: (1) Know your model's training cutoff and treat any sample period before it as *suspected contaminated* for any forward-looking task. (2) For classification of *contemporaneous* attributes (what tone does this text have?), leakage is far less of a concern than for *prediction* of future outcomes — labeling a 2019 filing's tone does not require knowing 2020's returns, so it is comparatively safe; predicting 2020's returns from the 2019 filing is exactly where leakage bites. (3) The cleanest defense is genuine out-of-sample testing on data created *after* the model's cutoff, where the model cannot have peeked. (4) In RAG, enforce it mechanically: when answering a question dated time $t$, *filter the retrieval to chunks with metadata date $\le t$* — never let a 2019 query retrieve a 2021 filing. This is why §6.5.3 insisted every chunk carry a date.

### Prompt-induced p-hacking

You met p-hacking in Week 1: torturing a dataset — trying specifications until one crosses $p < 0.05$ — until it confesses a result that is really just noise. LLMs open a new and seductive avenue for it. Because the label column *depends on the prompt*, you can — consciously or not — **rewrite the prompt until the labels produce the regression result you were hoping for.** Try "negative" defined one way: coefficient insignificant. Reword the rubric: now it's significant. Stop, declare victory, and report the lucky prompt. This is p-hacking wearing a new costume, and it is arguably worse than the classic kind because the researcher degree of freedom (the exact prompt wording) is so large and so easy to fiddle with that you may not even notice you are doing it.

The defenses are the ones that defeat p-hacking generally, adapted: (1) **Freeze the rubric before you look at the downstream result.** Validate the classifier against the gold set (§6.5.4) — a target that has nothing to do with your regression coefficient — and lock the prompt when its F1 is acceptable. The gold set, not the regression, decides when the prompt is good. (2) **Pre-register**, even informally, the prompt and the specification in a dated file before running the final analysis. (3) **Report the prompt verbatim** in an appendix so a replicator can confirm you did not shop for it. (4) If you genuinely tried several prompts, *say so and show the results under each* — robustness, not concealment. The honest question is the one from Mentor Session 5: would this result survive a referee who can see everything you tried?

### Reproducibility of stochastic outputs

A regression is deterministic: same data, same code, same coefficient, forever. An LLM is, by default, *stochastic* — ask the same question twice and you can get two different answers, because the model samples from a probability distribution over next tokens. For a research instrument, irreproducibility is a serious problem: if your labels change every run, your results are not replicable, and "I got $p = 0.04$ that one time" is not science.

Several controls, and one honest caveat. *Temperature* is the classic knob — it scales how much randomness is injected into sampling; temperature 0 makes the model (close to) greedy and far more repeatable, which is what you usually want for classification. A *seed*, where the API exposes one, pins the random draws so a run is reproducible. **But here is the caveat that is itself a reproducibility lesson:** these controls differ by provider and by model, and they are not guaranteed bit-for-bit. Some current frontier models (Anthropic's Opus 4.7, for instance) do *not* expose a `temperature` parameter at all — the knobs you reach for on one provider may simply not exist on another, and even "temperature 0" is not a hard determinism guarantee across model versions or hardware. The practical consequence: **you cannot rely on the model being deterministic, so you must make your *pipeline* reproducible by other means.** That means three things, and they are the bridge to §6.5.6: pin and record the exact model *version string* (a model silently updated under the same name will change your labels — version it like you version a CRSP snapshot date per CONVENTIONS §5); log every prompt and every response so the actual labels you used are saved, not regenerated; and where determinism matters, run the classification *once*, save the output to disk, and treat that saved file as your data — never re-query the model inside an analysis that is supposed to be reproducible. The labels are data; freeze them like data.

---

## 6.5.6 The APIs: correct, current code

A chat window is fine for exploration, but a research pipeline that labels 40,000 filings runs through an **API** (application programming interface) — you send the model text with a program and get structured responses back, so the whole process is scripted, logged, and reproducible. We show two providers you will actually use in this program: Anthropic's API directly, and OpenAI-family models through GMU's Azure gateway. Then we cover audit logging and a local-model fallback for licensed data.

> **The non-negotiable rule, stated once and meant absolutely:** an API key is a secret, like a password. It is **never** written into code, never pasted into a prompt, never committed to git, never shown in a notebook. It lives in an environment variable and is read at runtime with `os.environ[...]`. Every snippet below obeys this, and CONVENTIONS §5 requires it of every notebook in this book. A key in your code is a key in your GitHub history forever.

### (a) The Anthropic Messages API

The Python `anthropic` SDK reads your key from the `ANTHROPIC_API_KEY` environment variable automatically — you never name it in code. A classification call looks like this:

```python
import os
from anthropic import Anthropic

# The client reads ANTHROPIC_API_KEY from the environment. We do NOT
# pass the key in code. (Set it in your shell: export ANTHROPIC_API_KEY=...)
client = Anthropic()

SYSTEM_PROMPT = """You are classifying the tone of a 10-K Risk Factors
section. Assign exactly one label: NEGATIVE, NEUTRAL, or POSITIVE,
following these rules: [... the full rubric from 6.5.2 ...].
Return only the label word."""

def classify(filing_text: str) -> str:
    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=16,                     # one word out: keep it tiny and cheap
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},   # <- cache the rubric
            }
        ],
        messages=[{"role": "user", "content": filing_text}],
    )
    return response.content[0].text.strip()
```

Three things in that call are worth understanding, because they are the difference between a toy and a production research pipeline.

**Prompt caching.** Notice the structure: the *stable* rubric goes in `system` with a `cache_control` marker; the *volatile* filing text goes in `messages`. The order matters because the API caches a *prefix* of the request. Your rubric might be 1,500 tokens and it is identical for all 40,000 filings; without caching you pay to re-process it 40,000 times. With the `cache_control` breakpoint after the rubric, the API stores the processed rubric after the first call and *reuses* it on every subsequent call — much cheaper and faster. The reason §6.5.2 insisted on "stable instruction first, volatile input last" is exactly this: any change to the cached prefix invalidates the cache, so the filing text must come *after* the breakpoint. **Verify it is working** by reading the usage field:

```python
resp = client.messages.create(...)
print(resp.usage.cache_read_input_tokens)   # >0 means the rubric was cached
```

If `cache_read_input_tokens` stays zero across repeated calls, something is silently invalidating the prefix (a timestamp in the system prompt, a varying rubric) and you are paying full price every time.

**Small `max_tokens` for classification.** The output is one word, so `max_tokens=16` is plenty. You pay per output token, and a tight cap also prevents the model from rambling past the label you asked for. (For tasks that produce real prose — a literature summary — you would set this far higher and stream the response.)

**Adaptive thinking for harder reasoning.** A one-word tone label needs no deliberation, but a harder task — "does this MD&A passage describe a *new* liquidity risk or restate an existing one, and why?" — benefits from letting the model reason before answering. On Opus 4.7 you enable that with `thinking={"type": "adaptive"}`, which lets the model decide how much internal reasoning to spend on each input. Use it for genuinely hard judgment calls; skip it for cheap, high-volume labeling where speed and cost dominate.

Three model IDs are available: `claude-opus-4-7` (the default, most capable), `claude-sonnet-4-6` (faster and cheaper, often plenty for classification), and `claude-haiku-4-5` (cheapest, for the highest-volume, simplest tasks). A sensible workflow: develop and validate your rubric on Opus, then check whether a cheaper model clears your F1 bar on the gold set before running it across all 40,000 documents.

### (b) GMU's Azure OpenAI deployment

GMU provides OpenAI-family models (GPT-5.4, GPT-4.1, GPT-4o) through an Azure API Management gateway. The pattern is the same shape — read the key from the environment, never hard-code it — using the `openai` SDK's `AzureOpenAI` client:

```python
import os
from openai import AzureOpenAI

# Key comes from the environment ONLY. NEVER hard-code it here.
client = AzureOpenAI(
    azure_endpoint="https://apim-n1ai-use-gmun1.azure-api.net/",
    api_key=os.environ["AZURE_OPENAI_KEY"],   # <- read from env, never inline
    api_version="2024-10-21",                 # pin the API version (reproducibility) -- [CHECK] confirm the exact api_version GMU's N1 AI gateway expects
)

def classify_azure(filing_text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",                        # your GMU deployment name -- [CHECK] confirm the exact deployment name in the GMU N1 AI portal
        max_tokens=16,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": filing_text},
        ],
    )
    return response.choices[0].message.content.strip()
```

The endpoint is fixed (`https://apim-n1ai-use-gmun1.azure-api.net/`); the *key* is read from `${AZURE_OPENAI_KEY}` and appears nowhere in the source. The `api_version` and the deployment name (`gpt-4o`) above are illustrative and tagged `[CHECK]` — confirm both against GMU's N1 AI portal before running, since a wrong deployment name or api_version is the most common reason a first Azure call fails. Having two providers is not redundancy for its own sake — it is a robustness check. If your headline result holds up when you re-label your corpus with a *different* model from a different vendor, that is real evidence your finding is about the documents and not an artifact of one model's quirks. If it flips, you have learned something important before a referee does.

### Audit logging

For IRB-style reproducibility — and for your own sanity when a reviewer asks "what exactly did you send the model?" six months from now — **log every API call.** One line of JSON per call (JSONL), appended to a file:

```python
import json, hashlib, datetime

def log_call(logfile, model, prompt, response, usage):
    record = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "model": model,                                   # exact version string
        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),  # not the
        # raw prompt if it contains licensed text — a hash proves what you sent
        "response": response,
        "input_tokens": usage.input_tokens,
        "output_tokens": usage.output_tokens,
        "cache_read_input_tokens": getattr(usage, "cache_read_input_tokens", 0),
    }
    with open(logfile, "a") as f:
        f.write(json.dumps(record) + "\n")
```

This log is the AI-pipeline equivalent of a Stata `.log` file or a lab notebook. It records *which* model version produced *which* label for *which* input, plus the token cost. With it, your AI-assisted results are auditable: anyone can see the exact requests, confirm the model version never silently changed mid-study, and reconstruct your label column. Without it, "I used an LLM to classify the filings" is an unfalsifiable claim. Note the choice to log a SHA-256 *hash* of the prompt rather than the raw prompt when the input contains licensed text — the hash proves exactly what you sent (any change in input changes the hash) without copying licensed data into a log file, which brings us to the last piece.

### Local fallback for licensed data

CONVENTIONS §5 and your WRDS/TRACE license agreements are strict on one point: **licensed data must not leave GMU infrastructure.** Sending raw CRSP, Compustat, or TRACE records to a commercial API over the public internet may violate the data-use agreement, regardless of the vendor's own privacy policy — the data simply is not yours to transmit. When the text you need to classify *is* licensed, you run the model *locally*, inside the secured environment, so the data never crosses the boundary.

Two practical routes. For development and small jobs, run a roughly 8-billion-parameter open model on your own machine with **Ollama** — a tool that downloads and serves models locally on a Mac (or Linux/Windows) and exposes a local HTTP endpoint, so your data never leaves the laptop:

```python
# Ollama serves a model on localhost — data never leaves the machine.
import requests
resp = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "llama3.1:8b",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": filing_text},
        ],
        "stream": False,
    },
)
label = resp.json()["message"]["content"].strip()
```

For production-scale jobs over licensed corpora, run a larger open model on a GPU node — an **A100** on GMU's **Hopper** cluster — where the licensed data already lives and stays. The privacy rationale is the whole point: a local or on-cluster model keeps WRDS/TRACE text inside the walls the license requires. The cost is capability — an 8B local model is weaker than a frontier API model, so its classifier needs the *same* out-of-sample validation from §6.5.4, and you may find you need the larger Hopper model to clear your F1 bar. Validation is what tells you whether the privacy-preserving choice is also an accurate-enough one.

---

## 6.5.7 A responsible-use and disclosure checklist for the capstone

Your capstone must be honest about how AI was used, and reproducible by someone who has only your repository. Treat AI assistance the way you treat any other part of the method: disclose it, validate it, and make it replicable. The following is the checklist your capstone (and the Week 6 assessment) will be held to.

**Disclosure — say what you did.**
- State, in a methods or acknowledgments paragraph, *where and how* you used an LLM: literature triage, code review, prose editing, and/or producing data (labels, extractions). Be specific about which.
- Name the exact model *version string(s)* and provider(s) you used, and the date range over which you ran them.
- Distinguish clearly between AI used as a *writing aid* (you own every word) and AI used to *generate data* (labels that enter a regression) — the second demands validation; the first demands only that the words are true and yours.
- Disclose *every* prompt that produced data, verbatim, in an appendix — especially the classification rubric.

**Validation — prove the measurement.**
- For any LLM-generated label used in analysis, include an out-of-sample precision/recall/F1 table against a hand-labeled gold set, with the gold-set size and the held-out test-set size stated.
- Report performance on the class you care about, never bare accuracy under imbalance.
- State the gold-labeling procedure (one coder or two, how disagreements were resolved).

**Reproducibility — make it re-runnable.**
- Commit the audit log (or a redacted version) so the exact calls are on record.
- Pin the model version, the API version, and any random seed/temperature setting; note where determinism is not guaranteed.
- Save LLM-generated labels to disk and treat that file as your dataset — do not re-query the model inside the analysis pipeline.
- Verify every citation and every specific figure the model suggested against a primary source before it enters the paper; tag anything unverifiable `[CHECK]`.

**Integrity — don't fool yourself, or the referee.**
- Freeze your classification prompt against the gold set *before* looking at the downstream regression result, to avoid prompt-induced p-hacking.
- For forward-looking/prediction tasks, address training-data leakage explicitly: state the model's cutoff and why your sample is not contaminated, or test out-of-sample on post-cutoff data.
- If you tried multiple prompts or models, report the robustness, do not hide it.

The unifying idea, and the one to carry into Mentor Session 6: an LLM is a measurement and drafting instrument that you, the researcher, remain fully responsible for. Used as a co-pilot — accelerating verifiable work, with validation and logging as the guardrails — it makes you faster and lets you tackle text-as-data questions that were out of reach a few years ago. Used as an autopilot — trusted to think, recall, and decide on your behalf — it will, sooner or later, fly your paper into a mountain with total confidence. The difference is entirely in the guardrails, and the guardrails are your job.

---

## Go to the lab

**Now open nb6.5 — the AI co-pilot lab.** There you will run the offline, reproducible versions of everything above: a working RAG pipeline over a small set of real 10-K filings (chunk → embed → retrieve → ground), an OOS-validated 8-K event classifier with a full precision/recall/F1 report against a hand-labeled gold set, calls to both the Anthropic Messages API and the GMU Azure deployment (keys read from the environment, never hard-coded), the JSONL audit logger, and the Ollama local-fallback path for licensed text. The notebook is where the prompt patterns of §6.5.2 stop being advice and become a measurement instrument you have personally calibrated.

**Three questions to carry into the notebook and into Mentor Session 6.**

1. *When is an LLM label a measurement you can defend, and when is it a confident guess?* You have a classifier with test-set precision 0.88 and recall 0.61 for the "negative" class. Your main result depends on identifying negative filings. Would you use these labels? What does the low recall do to your regression, and what would you have to report so a referee can judge the damage?

2. *Where, in your own capstone idea, does training-data leakage threaten you?* Name one task in your design where the model might "know the future" relative to your sample, explain why, and describe the cleanest defense you could implement — including how you would enforce a date filter in retrieval if you use RAG.

3. *What in your AI workflow is irreproducible right now, and how would you fix it?* Walk through your intended pipeline and find every place a re-run could produce different numbers (stochastic outputs, an un-pinned model version, a prompt you tuned against the result). For each, write the one concrete change — freeze the labels, pin the version, validate against the gold set, log the call — that would make your work survive replication.
