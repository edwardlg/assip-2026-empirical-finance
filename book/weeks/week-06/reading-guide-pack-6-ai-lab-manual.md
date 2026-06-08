# Reading Guide Pack 6 + AI Lab Manual — When the Data Is Words, and the Tool Has Opinions

Week 5 taught you to read a *causal* paper: a study whose whole claim is that some treatment moved some outcome, and whose whole vulnerability is that the comparison might not be clean. You learned to go straight to the headline table, pin down the identifying assumption in one sentence, and name the alternative explanation that would sink the result. That muscle does not retire this week — but it is no longer enough. The five things you read in Week 6 are a different species of paper, and Chapter 6.5 hands you a tool — a large language model (LLM) — that can either make you a faster researcher or quietly fabricate your evidence, depending entirely on how much you trust it.

So this pack does two jobs. The first half retools the Week-5 reading anatomy for **measurement papers**: studies whose central act is not "we identified an effect" but "we built a number out of text, and here is why you should believe the number means what we say." The second half is a **lab manual** for the AI co-pilot module — a RAG architecture you can build, a catalog of prompt patterns that actually work for research, an evaluation harness that treats an LLM's labels the way Week 1 taught you to treat any estimator, and a responsible-use checklist that keeps your capstone reproducible and your licensed data where the law and your university require it to stay. The two halves are the same idea pointed in two directions. A text-as-data paper asks "is this measure valid?" An LLM label *is* a measure. The skepticism you bring to Hoberg and Phillips is the skepticism you must bring to your own prompt output. That is the thread of the whole week.

---

## 1. Reading a measurement paper — the question changes, the anatomy stays

The five Week-6 papers are Kogan, Papanikolaou, Seru & Stoffman (2017), who build a dollar value for each patent out of the *stock-price jump* on the day the patent is granted; Hoberg & Phillips (2016), who measure how similar two firms' products are by the *cosine similarity of their 10-K business descriptions*; Loughran & McDonald (2011), who measure the tone of a financial filing by *counting words from a finance-specific sentiment dictionary*; and the paired fair-lending studies — Bartlett, Morse, Stanton & Wallace (2022) and Bhutta, Hizmo & Ringo — which measure *discrimination* in algorithmic and human lending, building on Gao & Sun (2019). Four of the five turn words or events into a continuous number. None of them is, at its core, a clean natural experiment. So the Week-5 questions, asked verbatim, will mislead you.

Here is the reveal. When you read a causal paper, the load-bearing question is **"is the effect causal?"** — does the comparison isolate the treatment from everything correlated with it? When you read a measurement paper, the load-bearing question becomes **"is the measure valid?"** — does the number the authors constructed actually capture the concept they named it after, and would it behave the way the concept *should* behave? A patent-value measure is valid only if higher values really do flag more valuable inventions; a similarity score is valid only if firms it calls "similar" really do compete. Validity is not assumed by giving the variable a good name. It is *argued for*, with evidence, and your job as a reader is to find that argument and grade it.

The professional way to grade a measure is to ask whether it **predicts something it should predict but was not built to fit** — what psychometricians call *convergent* and *predictive validity*, and what an economist calls a *validation test*. KPSS do not just assert that their stock-return-based patent value is meaningful; they show it correlates with patent citations (a measure built a completely different way) and predicts future firm growth. That external check is the whole ballgame. A measure that only correlates with itself is a tautology dressed as a finding. Reveal the trick: **the validation table, not the headline table, is where a measurement paper lives or dies.**

So apply the same seven-part anatomy from Pack 5, but rotate the lens on three of the boxes:

**(1) Research question → what concept is being measured.** State, in one sentence, the *latent thing* the paper wants a number for: "how economically valuable is this patent?", "how much do these two firms compete?", "is the tone of this 10-K negative?", "does this lender charge minority borrowers more for the same risk?" Name the concept *before* you look at the proxy, because the gap between concept and proxy is where every measurement paper is vulnerable.

**(2) Identification strategy → the construction and its validation.** Do not look for an instrument or a parallel-trends plot. Look for two things. First, the **construction**: precisely how is the raw text or event turned into a number? (KPSS: the three-day abnormal return around the grant date, scaled. Loughran–McDonald: count of negative-dictionary words over total words. Hoberg–Phillips: cosine of two firms' word-frequency vectors.) Second, the **validation**: what *external* quantity does the measure predict, and does it? This second part replaces the identifying assumption as the most important box. The one-sentence test now reads: *"this number measures the concept as long as ___ "* — and the blank is filled by a validation result, not an exogeneity claim.

**(3) Data → and the construction choices that are secretly levers.** Same unit-of-observation and sample-period discipline as before, but add a measurement-specific worry: every step of the construction is a *researcher decision* — which dictionary, how to handle negation, what window around the event, whether to scale by firm size, how to clean the text (drop boilerplate? stem words? lowercase?). Loughran and McDonald exist *because* the off-the-shelf Harvard psychology dictionary mislabels finance words: "liability," "tax," "cost," "capital" are negative in everyday English but neutral accounting terms in a 10-K. A measure built on the wrong dictionary is a measure of the wrong thing. Treat each construction choice the way Pack 5 taught you to treat a sample filter: a lever someone pulled, which you must check could not have been pulled to manufacture the result.

**Boxes (4)–(7) carry over almost unchanged.** The **table-by-table reading order** still has a headline table, but now there is also a *validation table* that you should read second, right after the headline, before any robustness. **What's clever** is usually the construction itself — the insight that a stock-price jump prices an invention, or that two firms' word overlap proxies for product overlap; name it, because clever measurement is the rarest and most teachable skill in the field. **What's vulnerable** is now almost always a *validity threat*: the proxy captures something *other* than the named concept (a confound in measurement clothing — does Loughran–McDonald "negativity" measure pessimism, or just the legal-boilerplate density of a litigation-heavy industry?), or the measure is mechanically correlated with the outcome it later "predicts." And **three replication exercises** still escalate from "rebuild one number" to "stress a construction choice" (swap the dictionary, change the event window) to "extend to a new setting" (apply the measure to crypto-firm filings — Devon — or to climate-risk disclosures — Priya).

One self-check question to add to the Pack-5 rubric, the single most important one for this week: **Can I state, in one sentence, the external quantity this measure predicts that it was not constructed to fit — and did it?** If the answer is "the paper never validates the measure against anything outside itself," you have found the soft spot, and it is usually fatal.

---

## 2. RAG — how to make a language model answer from *your* documents, with citations

The first thing students want to do with an LLM is paste a 10-K into the chat box and ask questions. That works for one short document and fails for everything real: filings are too long for the context window, you have thousands of them, and the model will happily answer from its training data — which may be stale, wrong, or invented — rather than from the document in front of it. **Retrieval-Augmented Generation (RAG)** is the standard fix. The idea in one sentence: instead of trusting the model to *know* the answer, you *retrieve* the relevant passages from your own documents and *paste them into the prompt* as grounded context, then ask the model to answer using only those passages and to cite them.

Here is the pipeline, box by box.

```
                         ┌──────────────────────────────────────────────────┐
                         │  OFFLINE: build the index (do once per corpus)     │
                         └──────────────────────────────────────────────────┘

   ┌───────────┐   chunk    ┌───────────┐   embed    ┌───────────┐
   │ Documents │ ─────────► │  Chunks   │ ─────────► │ Vectors   │ ──┐
   │ (10-Ks,   │  (split    │ (~500-tok │  (text →   │ (one per  │   │
   │  filings) │   into     │  passages │   numeric  │   chunk)  │   │
   └───────────┘   passages)│  + source │   vector)  └───────────┘   │
                            └───────────┘                            ▼
                                                          ┌────────────────────┐
                                                          │   Vector store      │
                                                          │ (chunk vectors +    │
                                                          │  text + source IDs) │
                                                          └────────────────────┘
                         ┌──────────────────────────────────────────────────┐
                         │  ONLINE: answer a question (do once per query)     │
                         └──────────────────────────────────────────────────┘
                                                                    │
   ┌──────────┐  embed   ┌──────────┐   similarity search          │
   │  User    │ ───────► │  Query   │ ──────────────────────────►  │
   │ question │          │  vector  │   (find top-k nearest        ▼
   └──────────┘          └──────────┘    chunk vectors)   ┌────────────────────┐
                                                          │  Retrieve top-k     │
                                                          │  chunks (the most   │
                                                          │  relevant passages) │
                                                          └─────────┬──────────┘
                                                                    │ stuff into prompt
                                                                    ▼
   ┌──────────────────────────────────────────────────────────────────────────┐
   │  PROMPT = system instructions + retrieved chunks (with IDs) + the question │
   └──────────────────────────────────────────┬───────────────────────────────┘
                                               ▼
                                       ┌───────────────┐
                                       │      LLM       │
                                       └───────┬───────┘
                                               ▼
                              Answer, grounded in the chunks,
                              with citations back to source IDs
```

**Chunk.** A 10-K is hundreds of pages; you cannot embed it as one unit and you cannot fit it in a prompt. So you split it into passages of roughly a few hundred tokens (a token is a sub-word piece; ~500 tokens is a few paragraphs), keeping a small overlap between adjacent chunks so a sentence split across a boundary is not lost, and you tag every chunk with its source — *firm, filing, fiscal year, section, character offset* — so an answer can point back to exactly where it came from.

**Embed.** An *embedding model* turns each chunk of text into a vector of numbers — a few hundred to a few thousand dimensions — positioned so that passages about similar topics land near each other in that space. This is the same cosine-similarity geometry Hoberg & Phillips use on 10-Ks in Chapter 6.2; RAG is that idea industrialized. Two passages about supply-chain risk get nearby vectors even if they share no exact words.

**Vector store.** You save all the chunk vectors — alongside their text and source IDs — in a database built for one operation: given a query vector, return the nearest chunk vectors fast. (FAISS or Chroma locally; many hosted options exist.)

**Retrieve top-k.** When a question arrives, you embed *the question* with the same model, then ask the store for the `k` chunks whose vectors are closest (highest cosine similarity) to the question vector. Those `k` passages — typically 3 to 10 — are your evidence.

**Stuff into the prompt.** You build one prompt: a system instruction ("answer only from the context below; if the answer is not there, say so"), the retrieved chunks with their source IDs, and the user's question. The model never sees the whole corpus — only the handful of passages retrieval judged relevant.

**LLM answers with citations.** Because each chunk carries an ID, you instruct the model to cite the chunk it used for each claim. Now an answer is *checkable*: you can open the cited filing and verify the sentence is really there. An answer you cannot trace to a source is an answer you cannot use in a research paper.

**The failure modes — and they are not rare.** *Bad chunking*: cut the text mid-table or mid-sentence and the relevant fact is split across two chunks, so neither alone is retrievable; or chunk so coarsely that one passage mixes five topics and dilutes the signal. *Retrieval miss*: the right passage exists but its vector is not near the question's — the question says "litigation exposure," the filing says "pending legal proceedings," and the embedding model fails to bridge them — so the model answers from an irrelevant chunk or from its own memory. *The model ignores the context*: even with the right passage in the prompt, the model can override it with a confident wrong answer from training, or "answer" a question the context does not support rather than admitting the gap — the hallucination that Chapter 6.5 warns is the cardinal sin of LLM research. The defense against all three is the same discipline as the rest of this book: **validate**. Spot-check that retrieved chunks are actually relevant; confirm cited passages actually say what the answer claims; and never report a RAG answer you have not traced to its source.

---

## 3. A prompt-pattern catalog for research

A prompt is not a wish; it is a *specification*. The patterns below are the reusable ones for empirical work. Each is a template with the variable parts in `{braces}`. The recurring move across all of them is **constrain the output and demand grounding** — tell the model exactly what shape the answer must take, and force it to point at evidence so you can check it.

| Pattern | When to use | What it buys you |
|---|---|---|
| **Extraction** | Pull structured fields from messy text (e.g., the auditor, the going-concern flag, every numeric guidance figure from a filing) | Turns prose into a dataframe column; output is checkable against the source |
| **Classification-with-rubric** | Label each item into categories (sentiment, risk type, "is this 8-K about a layoff?") | Reproducible labels — but only a *measure to be validated* (see §4) |
| **Cite-or-abstain** | Any RAG question over your documents | Kills hallucination: the model must quote a source or say "not in the context" |
| **Code review** | Check your own analysis script before you trust its numbers | A second reader for look-ahead bugs, off-by-one merges, leakage |
| **Summarize-with-quotes** | Digest a long filing or paper without losing traceability | A summary every claim of which is anchored to a verbatim quote |

**Extraction.**
```
You are a careful data-extraction tool. From the TEXT below, extract these fields
as JSON: {field list, with a one-line definition of each}.
Rules: copy values verbatim from the text; do not infer or compute.
If a field is absent, output null — never guess. Output only the JSON.
TEXT: """{document text}"""
```

**Classification-with-rubric.** The rubric is the whole point: it makes the label reproducible by you, by another grader, and by the model on a re-run.
```
Classify the ITEM into exactly one of these labels using the rubric.
Labels & rubric:
- {LABEL_A}: {precise inclusion criteria; one example}
- {LABEL_B}: {precise inclusion criteria; one example}
- UNCLEAR: the text does not give enough information to decide.
Output JSON: {"label": "...", "evidence": "<verbatim phrase that decided it>",
"confidence": 0-1}. Use UNCLEAR rather than guessing.
ITEM: """{text}"""
```

**Cite-or-abstain.** The non-negotiable pattern for RAG.
```
Answer the QUESTION using ONLY the CONTEXT passages below. After each claim, cite
the passage id in [brackets]. If the context does not contain the answer, reply
exactly: "Not supported by the provided context." Do not use outside knowledge.
CONTEXT:
[1] {chunk text}  (source: {firm, filing, year, section})
[2] {chunk text}  (source: ...)
QUESTION: {question}
```

**Code review.** Especially for the look-ahead/leakage bugs §5 warns about.
```
Review this {language} snippet for empirical-research bugs. Check specifically:
(1) look-ahead bias — does any feature at time t use information from t or later?
(2) leakage between train and test; (3) silent sample changes on merge/dropna;
(4) chained indexing or copy-vs-view bugs. List each issue with the line, why it
is wrong, and a fix. If you are unsure, say so rather than inventing a problem.
CODE: """{code}"""
```

**Summarize-with-quotes.**
```
Summarize the DOCUMENT in {n} bullet points. After each bullet, include a verbatim
quote (<=25 words) from the document that supports it, with its location. Do not
state anything the document does not say. If a section is ambiguous, note it.
DOCUMENT: """{text}"""
```

Two cross-cutting rules. First, **give the model an exit**: every classification or extraction template offers `UNCLEAR`/`null`/`"Not supported"`, because a model with no permission to abstain will fabricate to comply, and a forced wrong label is worse than an honest blank. Second, **constrain the output format** (JSON, a fixed label set, a quote) so the result is machine-parseable and checkable — a free-text answer you cannot parse is an answer you cannot validate at scale.

---

## 4. An evaluation harness — an LLM label is a measurement, not ground truth

This is the section that ties the AI module back to the science. When you ask an LLM to classify ten thousand 8-Ks as "layoff / not layoff," you have not *measured* anything yet — you have produced ten thousand *guesses* from an instrument of unknown accuracy. Treating those guesses as ground truth is exactly the error Loughran and McDonald exposed in the off-the-shelf sentiment dictionary, reborn in a fancier tool. The fix is the same one Week 1 taught for any estimator: **validate it against a standard, and report how often it is wrong.**

The standard is a **hand-labeled gold set**: a sample of items that *humans* labeled carefully against the same rubric the model used. Build it right. Draw the sample at random from the real corpus (not the easy cases). Have **at least two humans** label each item independently, then reconcile disagreements, so the gold set itself has a known reliability. And — the discipline that makes the whole thing honest — **split the gold set into a small development set and a held-out test set.** You are allowed to look at the dev set as much as you like while you tune the prompt; you may touch the test set *once*, at the end, to report final numbers. Tuning the prompt until it aces the same examples you report on is the prompt-engineering version of overfitting, and it inflates your accuracy exactly the way in-sample $R^2$ flatters a regression.

Now score the model's labels against the held-out human labels with a **confusion matrix**. For a binary "layoff" classifier:

|  | Human: Layoff | Human: Not |
|---|---|---|
| **LLM: Layoff** | TP (true positive) | FP (false positive) |
| **LLM: Not** | FN (false negative) | TN (true negative) |

From the four counts come the three numbers you report:

$$
\text{Precision} = \frac{TP}{TP+FP}, \qquad
\text{Recall} = \frac{TP}{TP+FN}, \qquad
F_1 = 2\cdot\frac{\text{Precision}\cdot\text{Recall}}{\text{Precision}+\text{Recall}}.
$$

**Precision** answers "when the model says *layoff*, how often is it right?" **Recall** answers "of the real layoffs, how many did it catch?" They trade off — a model that screams "layoff" at everything has perfect recall and terrible precision — and which one matters more depends on your downstream use, so report both. **$F_1$** is their harmonic mean, a single summary that punishes lopsidedness. A worked feel for the numbers: with $TP=80$, $FP=20$, $FN=40$, precision is $80/100 = 0.80$, recall is $80/120 \approx 0.67$, and $F_1 \approx 0.73$ — a classifier you might use for screening but not for a headline regression coefficient without a correction for the error rate.

One number more, and it is the one beginners skip. Accuracy and $F_1$ compare the model to humans *as if the humans were infallible* — but if your two human labelers only agreed 70% of the time, a model that "agrees with the gold set" 75% of the time is barely better than the noise floor. So report **inter-rater agreement** with **Cohen's kappa**, which measures agreement *above what you'd get by chance*:

$$
\kappa = \frac{p_o - p_e}{1 - p_e},
$$

where $p_o$ is the observed fraction of items two raters labeled the same and $p_e$ is the fraction they'd match by chance given each rater's label frequencies. $\kappa = 1$ is perfect agreement, $\kappa = 0$ is chance-level. Compute it **between the two humans** (to know how hard the task is and whether your rubric is even well-defined) *and* **between the LLM and a human** (to know whether the model is as reliable as a second human annotator). If human–human kappa is 0.5, the task is genuinely ambiguous and you should fix the rubric before blaming the model; if LLM–human kappa approaches human–human kappa, the model is a credible annotator for that task.

The whole harness in one sentence, and it is the sentence to carry into your capstone: **an LLM label is a noisy measurement of a latent concept, exactly like a sentiment-dictionary score or a patent-value proxy, and it earns its place in a regression only after you have validated it on a held-out, human-labeled test set and reported its precision, recall, $F_1$, and kappa.** Anything less and you are running KPSS without the validation table.

---

## 5. Responsible-use and disclosure checklist for the capstone

The AI co-pilot is allowed in your Week 7–8 capstone — encouraged, even — but under rules that keep your work honest, reproducible, and legal. This checklist is binding for the capstone and is the standard a mentor will hold your draft to.

**Disclose the assistance.** In a short *AI-use statement* in your capstone, name every place an LLM touched the work: which tasks (brainstorming, code drafting, text classification, prose editing), which model and version, and what *you* did to verify its output. The rule of thumb: a reader should be able to tell what the model did and trust that you checked it. Using AI is not the violation; *hiding* it, or reporting unverified model output as your own verified finding, is.

**Make API-based work reproducible.** An LLM is a *stochastic* instrument — the same prompt can return different text on two runs — so reproducibility takes extra care beyond pinning library versions:
- [ ] **Log every call**: timestamp, the exact prompt, the full response, and the parameters (model, temperature, top-p, max tokens, seed if the API supports one) to a file you keep with the project.
- [ ] **Pin the model version** explicitly (the dated deployment, not a floating alias like "latest"), because providers update models silently and your numbers can move under you. Set `temperature=0` for classification and extraction to make outputs as deterministic as the API allows, and record that you did.
- [ ] **Save the prompts** as files in the repo, versioned, the same way you version code — a result you cannot regenerate from a saved prompt is not reproducible.
- [ ] **Save the gold set and the eval script** so anyone can re-run your precision/recall/kappa from §4.

**Heed the look-ahead and leakage warning.** Two distinct traps, both fatal:
- [ ] *Look-ahead bias* in your own pipeline — never let a feature for time $t$ use information that did not exist until after $t$. The code-review prompt in §3 is built to catch this; run it.
- [ ] *Training-data leakage* unique to LLMs — the model was trained on text up to some cutoff, so if you ask it to "predict" 2019 outcomes, it may simply *remember* them from its training data rather than infer them, and your "out-of-sample" test is contaminated. State your model's training cutoff and make sure your prediction targets fall *after* it, or treat the model as a feature-extractor on text only, never as a forecaster of outcomes it could have memorized.

**Obey the data-governance rule — this one has legal teeth.** Per CONVENTIONS §5, licensed data (CRSP, Compustat, **TRACE**, WRDS-sourced anything) stays read-only on GMU infrastructure and never leaves it. Sending licensed rows to an *external* API — Anthropic's or OpenAI's public endpoints — is a license violation and a data-governance breach, full stop. So:
- [ ] **Never paste licensed or sensitive data into an external LLM API.** Not a CRSP return, not a TRACE bond trade, not a row you are not allowed to redistribute.
- [ ] For sensitive data, run the model **locally**: **Ollama** on your machine or on a **GMU Hopper A100** node (SLURM template in Appendix B.4), where the data and the model both stay inside the licensed perimeter. The GMU Azure APIM gateway is the in-perimeter option for hosted models when GMU's agreement covers it; confirm the data-handling terms before sending anything non-public. `[CHECK]` Confirm with GMU IT / WRDS exactly which data classes the GMU Azure APIM endpoint is contractually cleared to process before routing any licensed data through it.
- [ ] When you *must* use an external API, send only **non-licensed, public text** — a 10-K from EDGAR is public and fine; the CRSP return you joined to it is not. Strip to the public columns first.

The principle underneath all five items is the one this whole book defends: a result is only as good as your ability to *reproduce* it and *defend* it. An LLM does not change that standard; it raises the bar, because it adds a stochastic, opaque, license-sensitive instrument to your toolkit. Log it, pin it, validate it, disclose it, and keep the licensed data home — and the co-pilot makes you faster without making you wrong.

---

So: read the five Week-6 papers asking "is the measure valid?", build your RAG over public 10-Ks, write prompts that constrain and cite, score every LLM label against a held-out gold set, and carry all of it into a capstone you can hand a skeptic and defend line by line. The skeptic who reads a stranger's measurement table and the researcher who validates her own LLM labels are, once again, the same person.
