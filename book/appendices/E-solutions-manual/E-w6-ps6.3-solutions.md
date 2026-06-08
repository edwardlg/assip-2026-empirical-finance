# Solutions — PS 6.3 (The LM Dictionary vs. a Naive Dictionary: When a Liability Is Not a Liability)

**Problem set:** `book/weeks/week-06/ps6.3.md` (PS 6.3, Week 6).
**Chapter:** Ch 6.3 — Reader's Guide: Loughran & McDonald (2011), with a forward pointer to Ch 6.5 (embeddings / LLMs) and a look-ahead callback to Week 1 (data-snooping).
**Paper:** Loughran, T., & McDonald, B. (2011). *When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks.* Journal of Finance, 66(1), 35–65.

These are full worked solutions, not just answers. Notation follows `CONVENTIONS.md` and locks to Ch 6.3: the **bag-of-words** model (tokenize, lowercase, drop order, keep a multiset of counts); the **dictionary NegScore** $\text{NegScore}_d = (\#\text{negative-list words in } d)/(\#\text{total words in } d)$; the flag rule (flag negative if $\text{NegScore}_d \geq \theta$, with $\theta = 0.05$); the **false-flag rate** on documents a human reads as neutral; **tf–idf** weighting $w_{t,d}=\text{tf}_{t,d}\,\text{idf}_t$ with $\text{idf}_t=\ln(N/\text{df}_t)$; the bag-of-words **negation/context failure**; and the **out-of-sample** discipline. **Every word list, sentence, and number in this sheet is illustrative** — the two dictionaries are teaching subsets, not the real Harvard General Inquirer list or the full Loughran–McDonald Master Dictionary, and the counts are chosen for clean arithmetic. The single claim about the real paper is the qualitative Ch 6.3 one: a *large share* of the "negative" word occurrences a general-English dictionary finds in 10-Ks are benign accounting terms, and the LM finance dictionary is the field standard that fixed it. Do not present any toy percentage here as the paper's measured number — Ch 6.3 tags that figure `[CHECK]`. **All by-hand counts and scores below were confirmed in Python** with the exact tokenizer from `nb6.3` (`re.findall(r"[a-z]+", text.lower())`); verifying notes appear where useful.

Recall the two dictionaries used throughout (teaching subsets):

- $D_{\text{naive}}$ (general-English, Harvard-GI-style): liability, liabilities, tax, taxes, cost, costs, depreciation, crude, vice, capital, expense, expenses, loss, losses, lose, bad, decline, declined, weak, doubt, adverse, fraud, default, severe, fail, failed, risk.
- $D_{\text{LM}}$ (finance-specific, LM-style): loss, losses, litigation, adverse, deficiency, restated, termination, terminated, bankruptcy, default, doubt, impairment, fraud, weakness, decline, declined, weak, severe, restructuring, alleging.

---

## Problem 1 — Score finance prose with a general-English list, by hand (16 points)

**(a) (4 pts)** Tokenize S1 — *"The deferred tax liability increased as depreciation expense rose."* Lowercase, alphabetic runs only:

$$
[\text{the},\ \text{deferred},\ \text{tax},\ \text{liability},\ \text{increased},\ \text{as},\ \text{depreciation},\ \text{expense},\ \text{rose}].
$$

So $\#\{\text{total words}\} = \mathbf{9}$. The tokens on $D_{\text{naive}}$ are **tax, liability, depreciation, expense** — four hits. Therefore
$$
\text{NegScore}^{\text{naive}}_{\text{S1}} = \frac{4}{9} \approx 0.4444 = \mathbf{44.44\%}.
$$
Almost half of this neutral bookkeeping sentence is "negative" to the naive list. (*Verified in Python: tokens as listed, 4 naive hits, $4/9$.*)

**(b) (4 pts)** S2 — *"Our Vice President reviewed the cost of capital and the crude oil reserve."* Tokens:
$$
[\text{our},\ \text{vice},\ \text{president},\ \text{reviewed},\ \text{the},\ \text{cost},\ \text{of},\ \text{capital},\ \text{and},\ \text{the},\ \text{crude},\ \text{oil},\ \text{reserve}],
$$
so $\#\{\text{total words}\} = \mathbf{13}$. The naive-list hits are **vice, cost, capital, crude** — four again. (Note "vice" is flagged because "vice" is a sin in general English; here it is the *Vice* President's title.) Thus
$$
\text{NegScore}^{\text{naive}}_{\text{S2}} = \frac{4}{13} \approx 0.3077 = \mathbf{30.77\%}.
$$

**(c) (4 pts)** S3 — *"The company incurred a substantial net loss and an impairment charge."* — has 11 tokens; the only naive-list hit is **loss** (note "impairment" is *not* on the naive general-English list — it is a finance word):
$$
\text{NegScore}^{\text{naive}}_{\text{S3}} = \frac{1}{11} \approx 0.0909 = \mathbf{9.09\%}.
$$
S4 — *"Revenue grew and the board approved a higher dividend on solid demand."* — has 12 tokens and **zero** naive-list hits:
$$
\text{NegScore}^{\text{naive}}_{\text{S4}} = \frac{0}{12} = \mathbf{0\%}.
$$

Applying the flag rule $\theta = 0.05$ to all four:

| Doc | Truth | $\text{NegScore}^{\text{naive}}$ | Naive flag ($\geq 5\%$)? |
|-----|-------|:---:|:---:|
| S1 | benign | $44.44\%$ | **NEGATIVE** |
| S2 | benign | $30.77\%$ | **NEGATIVE** |
| S3 | negative | $9.09\%$ | NEGATIVE |
| S4 | positive | $0\%$ | not negative |

The naive list gets S3 right and S4 right — but flags **both benign accounting sentences as negative**, the two errors that are the whole point of the paper.

**(d) (4 pts)** The words doing the flagging on the benign sentences are **tax, liability, depreciation, expense** (S1) and **vice, cost, capital, crude** (S2). Every one is dark in general English — a *liability* is a burden, a *cost* is a loss, a *vice* is a sin, *crude* is rude — but in a financial disclosure each is a neutral, technical term: a deferred tax *liability* is a balance-sheet line, *cost* of capital is a discount rate, the *Vice* President is a job title, *crude* oil is a commodity. On these two sentences the naive NegScore is therefore *not measuring sentiment at all*; it is measuring the **density of ordinary accounting vocabulary** — a sentence stuffed with bookkeeping nouns scores as "gloomy" purely because the balance-sheet lexicon happens to overlap the general-English negative lexicon. This is exactly Loughran & McDonald's (2011) one-line diagnosis, and the title's riddle: *when is a liability not a liability?* — when a company writes it in a 10-K, where "liability" is Tuesday, not bad news. A general dictionary pointed at financial text mostly measures accounting density wearing a sentiment costume.

---

## Problem 2 — Recompute with the LM finance list and quantify the misclassification reduction (16 points)

**(a) (5 pts)** Re-score with $D_{\text{LM}}$, reusing the Problem 1 tokenizations:

- **S1** (9 tokens): none of {the, deferred, tax, liability, increased, as, depreciation, expense, rose} is on $D_{\text{LM}}$ — the benign accounting words were deliberately excluded. $\text{NegScore}^{\text{LM}}_{\text{S1}} = 0/9 = \mathbf{0\%}$.
- **S2** (13 tokens): no LM hits (vice, cost, capital, crude are all off the finance list). $\text{NegScore}^{\text{LM}}_{\text{S2}} = 0/13 = \mathbf{0\%}$.
- **S3** (11 tokens): LM hits are **loss** *and* **impairment** (the finance list *does* contain "impairment"). $\text{NegScore}^{\text{LM}}_{\text{S3}} = 2/11 \approx 0.1818 = \mathbf{18.18\%}$.
- **S4** (12 tokens): no LM hits. $\text{NegScore}^{\text{LM}}_{\text{S4}} = 0/12 = \mathbf{0\%}$.

Flags ($\theta = 0.05$):

| Doc | Truth | $\text{NegScore}^{\text{LM}}$ | LM flag? |
|-----|-------|:---:|:---:|
| S1 | benign | $0\%$ | not negative |
| S2 | benign | $0\%$ | not negative |
| S3 | negative | $18.18\%$ | **NEGATIVE** |
| S4 | positive | $0\%$ | not negative |

The LM list flags the *one* genuinely negative sentence and nothing else — perfect on this toy. (*Verified in Python.*) Note it also scores S3 *higher* than the naive list did ($18.18\%$ vs $9.09\%$), because it catches "impairment" that the naive list missed: a finance dictionary is not just *fewer* words, it is the *right* words.

**(b) (5 pts)** Restricting to the two benign sentences (the neutral accounting prose, $\#\{\text{benign}\} = 2$), the false-flag rate is the share of them wrongly flagged negative:

$$
\text{false-flag rate}^{\text{naive}} = \frac{\#\{\text{benign flagged}\}}{2} = \frac{2}{2} = \mathbf{100\%},
\qquad
\text{false-flag rate}^{\text{LM}} = \frac{0}{2} = \mathbf{0\%}.
$$

The naive list flags **both** benign sentences (S1, S2); the LM list flags **neither**. The **reduction** is $100\% - 0\% = \mathbf{100\ \text{percentage points}}$ — on this corpus the finance list eliminates the false flags entirely. In plain words: every false alarm the general-English list raised on neutral accounting prose was a word the finance list knew to ignore. (This mirrors `nb6.3`'s headline diagnostic, which prints `naive false-flag rate > LM false-flag rate` and reports `PASS`.)

**(c) (3 pts)** Counting word *occurrences* across the two benign sentences combined, the naive-list hits are **tax, liability, depreciation, expense** (S1) and **vice, cost, capital, crude** (S2) — $\mathbf{8}$ total occurrences. Every single one is a **benign accounting term** carrying no negative meaning in finance, so the benign share is
$$
\frac{8}{8} = \mathbf{100\%}.
$$
This is the *shape* of Loughran & McDonald's headline exhibit: the most frequent "negative" words a general dictionary finds in 10-Ks are benign vocabulary like tax / cost / capital / liability, so a large share of the dictionary's flagged "negativity" is misclassified accounting language. **Caution, per the standing rule:** $100\%$ here is an artifact of a hand-built two-sentence toy; it is *not* the paper's measured figure. Ch 6.3 reports the real share qualitatively ("a large share, on the order of three-quarters") and tags the exact percentage `[CHECK]` — do not quote our toy number as theirs.

**(d) (3 pts)** Mechanically, $D_{\text{LM}}$ does better because it **deleted from the negative list precisely the words that were benign in finance but dark in English** — tax, liability, depreciation, expense, cost, capital, vice, crude — and those deleted words were the *entire* source of the false flags (they contributed every one of the 8 spurious hits in part (c)). Remove them and the benign sentences' NegScore drops from $44.44\%$/$30.77\%$ to $0\%$, falling below the threshold; the genuinely negative sentence is untouched (indeed it gains a hit, "impairment"). The law this demonstrates, from Ch 6.3 §5: **the sentiment of a word is not a property of the word — it is a property of the word in its domain.** "Liability" is negative in English and neutral in accounting; an instrument calibrated on one domain mismeasures the other. Leah's portable rule: never reuse a measurement instrument across domains without re-checking that the words still mean what the instrument assumes.

---

## Problem 3 — tf–idf weighting: *how* you count, not just *what* you count (18 points)

**(a) (5 pts)** With $N = 4$ and $\text{idf}_t = \ln(N/\text{df}_t)$:

| Term | $\text{df}_t$ | $\text{idf}_t = \ln(4/\text{df}_t)$ | decimal |
|------|:---:|:---:|:---:|
| risk | 4 | $\ln(4/4)=\ln 1$ | $\mathbf{0.0000}$ |
| litigation | 2 | $\ln(4/2)=\ln 2$ | $\mathbf{0.6931}$ |
| bankruptcy | 1 | $\ln(4/1)=\ln 4$ | $\mathbf{1.3863}$ |
| impairment | 1 | $\ln(4/1)=\ln 4$ | $\mathbf{1.3863}$ |

The value that is exactly $0$ is $\text{idf}_{\text{risk}}$. A word appearing in **every** document in the corpus has $\text{df}_t = N$, so $\ln(N/\text{df}_t) = \ln 1 = 0$, and its tf–idf weight is zero *no matter how many times it occurs*. For a word like "risk" — boilerplate that shows up in every filing's risk-factor section — this is exactly the right behavior: a word that is everywhere distinguishes no document from any other, so it should carry no weight in scoring how negative *this particular* filing is. (*Verified in Python: $\ln 1 = 0$, $\ln 2 = 0.6931$, $\ln 4 = 1.3863$.*)

**(b) (6 pts)** Each filing is 10 tokens.

*Raw-count NegScore* (negative-list words / total tokens):
$$
\text{NegScore}^{\text{raw}}_{P} = \frac{4 + 1}{10} = \frac{5}{10} = \mathbf{0.50}, \qquad
\text{NegScore}^{\text{raw}}_{Q} = \frac{1 + 1 + 1}{10} = \frac{3}{10} = \mathbf{0.30}.
$$
Raw counts rank **P more negative than Q** ($0.50 > 0.30$): P simply contains more negative-list tokens.

*tf–idf-weighted negative mass* ($\sum_t \text{tf}_{t,d}\,\text{idf}_t$ over the negative-list words present):
$$
\text{mass}_{P} = \underbrace{4 \times \text{idf}_{\text{risk}}}_{4 \times 0} + \underbrace{1 \times \text{idf}_{\text{litigation}}}_{1 \times 0.6931} = 0 + 0.6931 = \mathbf{0.6931},
$$
$$
\text{mass}_{Q} = \underbrace{1 \times \text{idf}_{\text{risk}}}_{0} + \underbrace{1 \times \text{idf}_{\text{bankruptcy}}}_{1.3863} + \underbrace{1 \times \text{idf}_{\text{impairment}}}_{1.3863} = 0 + 1.3863 + 1.3863 = \mathbf{2.7726}.
$$
tf–idf ranks **Q more negative than P** ($2.7726 > 0.6931$). (*Verified in Python.*)

**(c) (4 pts)** The ranking **flips**. Filing P is mostly the word **"risk" repeated four times** — pure boilerplate that, being in every filing ($\text{idf} = 0$), contributes *nothing* under tf–idf; its only genuine signal is one "litigation." Filing Q's three negative words are all **distinctive** — "bankruptcy" and "impairment" are rare across filings and carry the full $\ln 4$ weight. A human analyst would agree with tf–idf: a filing warning of *bankruptcy* and *impairment* is more genuinely alarming than one that just says "risk" four times in a standard risk-factor paragraph. This is exactly the boilerplate trap Ch 6.3 warns about — a long, legally cautious filing scoring as "negative" on raw counts simply because it repeats common cautionary vocabulary. tf–idf strips that artifact out by asking not "how many negative words?" but "how many *distinctive* negative words?"

**(d) (3 pts)** *Principle:* tf–idf **down-weights ubiquitous words (low idf, toward zero) and up-weights rare-but-present words (high idf)**, which helps a sentiment score by stopping common boilerplate from inflating negativity and letting genuinely distinctive bad-news words drive the measure. *Caveat:* on a *tiny* corpus, almost every word appears in only one document, so $\text{df}_t = 1$ for nearly all words and their idf values are all $\ln(N/1) = \ln N$ — essentially **identical** — so tf–idf rescales every word by the same constant and barely re-ranks anything. (This is exactly what `nb6.3` observes on its 15-sentence toy corpus: the re-ranking is "mild" because idf has almost no variation to work with.) tf–idf only earns its keep when the corpus is large enough that words *differ* in how widely they appear.

---

## Problem 4 — Breaking the bag: negation and context (failure task) (18 points)

Score with the combined vocabulary $D_{\text{bow}} = D_{\text{naive}} \cup D_{\text{LM}}$, $\theta = 0.05$. The whole point: every sentence below is one a human reads as *fine* (positive or neutral), yet the word counter flags it negative — and the failure is intrinsic to word-counting, not to either list.

**(a) (6 pts)** Per sentence (token counts and hits verified in Python):

| Doc | Human | Tokens | $D_{\text{bow}}$ words that fire | NegScore | BOW says ($\geq 5\%$)? |
|-----|-------|:---:|---|:---:|:---:|
| T1 | positive | 12 | **bad** | $1/12 = 8.33\%$ | **NEGATIVE** |
| T2 | positive | 11 | **litigation, adverse** | $2/11 = 18.18\%$ | **NEGATIVE** |
| T3 | neutral | 13 | **severe, losses, default** | $3/13 = 23.08\%$ | **NEGATIVE** |
| T4 | positive | 11 | **failed, lose** | $2/11 = 18.18\%$ | **NEGATIVE** |

All four clear the threshold and are flagged **NEGATIVE**. The scorer disagrees with the human on **4/4** — three positives and one neutral-conditional, all mislabeled negative.

**(b) (4 pts)** The meaning-carrying device differs in each, and *none* of these words is itself on a sentiment list — that is why the bag misses them:

- **T1** — the negator **"not"** (in *"not a bad quarter"*): a single short word flips "bad" to its opposite. The bag sees "bad," never the "not."
- **T2** — again **"not"** (*"not exposed to … litigation or adverse judgment"*): the firm is *denying* exposure, the strongest possible good news on legal risk, yet "litigation" and "adverse" both fire.
- **T3** — the **conditional "only if … the unlikely … were to occur"**: the severe losses are hypothetical and explicitly improbable, not a realized outcome; the bag counts "severe," "losses," "default" as if they had happened.
- **T4** — the **negated verb phrase "failed to lose"** (*"failed to lose money … exceeding every target"*): a double construction where "failed" + "lose" together mean *the company made money*; the bag scores both words as negative and doubles down on the error.

**(c) (4 pts)** The general reason is structural: a bag-of-words representation **discards word order, syntax, and scope**, keeping only *which* content words appeared and how often. But negation, conditionality, and sarcasm live entirely in the *arrangement* of words — "not bad" and "bad" share the identical content word and differ only in a function word and its position, which the bag throws away. This is *not* fixable by enlarging the list: even if you add "not" as a "positive" word, the model still cannot represent that "not" *attaches to* and *inverts* the nearby "bad" rather than to some other word — it has no notion of *attachment* at all. The deepest statement: **the same word means opposite things in two sentences** ("bad" in "a bad quarter" vs. "not a bad quarter"), and a representation that assigns each word a single fixed score *cannot* encode that two-faced behavior. Word-counting is a proxy for meaning that works on average over a 50,000-word document but breaks sentence by sentence.

**(d) (4 pts)** This is the bridge to Ch 6.5. A **word embedding** (word2vec / GloVe) replaces the flat list — where every word is either on it or off it — with a *dense vector* for each word, learned from the company it keeps, so that "good" and "great" land near each other and "loss" sits far from "profit"; you gain a notion of *similarity* and degree (the cosine-similarity geometry of Ch 6.2), rather than a binary in-list/out-of-list membership. But a plain embedding still gives "bad" *one* fixed vector regardless of context, so it still cannot tell "a bad quarter" from "not a bad quarter." A **contextual model / LLM** (the transformers of Ch 6.5) goes further: it computes each word's representation *as a function of the entire surrounding sentence*, so the token "bad" in "not a bad quarter" gets a genuinely different vector than "bad" in "a bad quarter" — the negation, the conditional, the sarcasm become at least partly *learnable* rather than structurally invisible. The one discipline Ch 6.3 §6 insists carries forward *unchanged* to these fancier models: **out-of-sample validation** (Problem 5). A smarter instrument is still only an instrument; it earns trust the same way the dictionary does — by working on data it never saw.

---

## Problem 5 — Validity and look-ahead: don't tune the dictionary on the test sample (16 points)

**(a) (5 pts)** The error is **data-snooping / data-mining** (the multiple-testing and overfitting hazard from Week 1). The labmate's validation is circular because the return data is used *twice*: first to **build** the list (keep only words that correlate with low returns in the 5,000 filings), then to **test** the list (show its NegScore predicts low returns in the *same* 5,000 filings). A list selected to correlate with returns in a sample is, by construction, *guaranteed* to correlate with returns in that sample — the high correlation is mechanical, not evidence of genuine content. The dictionary is **grading itself with the answer key**: it was handed the test answers (the returns) while being built, so a strong in-sample fit tells you nothing about whether it would predict returns in filings it had never seen. Even a list of words with no true relationship to firm fundamentals would pass this "test," because chance correlations in the build sample are exactly what the selection step harvested.

**(b) (4 pts)** Loughran & McDonald's construction defends against this in two ways. (i) The word selection was based on **linguistic and financial judgment about what words mean** in a disclosure — does a human reading a 10-K take this word as negative? — *not* on the words' correlation with returns. The return data never entered the choice of which words go on the list. (ii) The categories (negative, positive, uncertainty, litigious, modal) were **pre-specified** — defined by what concept they capture *before* any validation regression was run — rather than mined from the data for return-predictability. Each feature breaks the circularity for the same reason: if the answer key (returns) played no role in building the instrument, then a later finding that the instrument correlates with returns is *real* information, not a tautology — the instrument and the test are independent.

**(c) (4 pts)** The clean fix is an **out-of-sample design**: split the matched filings into a **build set** and a **held-out test set**. On the **build set** you may do everything that involves looking — fix the word list, choose the threshold, tune any decision. On the **held-out test set** you do exactly one thing: apply the *frozen* instrument and measure whether its score relates to market outcomes — and the inviolable rule is that **the test set must never inform the construction**: you do not peek at it, refit on it, or adjust the list after seeing it (no second tries). The result that would convince you of *genuine* signal: the frozen dictionary, built without ever touching the test filings, still shows more-negative tone associated with lower abnormal returns / higher volume / higher volatility *on the held-out filings* — a relationship it could not have memorized, because that data did not exist for it during construction.

**(d) (3 pts)** A large language model has **millions of parameters** and is fit to enormous text; that vast flexibility means it can fit not just signal but noise and idiosyncrasies of whatever sample it was trained or tuned on — it has far more capacity to *memorize* and thus to look good in-sample than a fixed 2,000-word dictionary, whose handful of hand-chosen words simply cannot overfit the same way. So the claim "**our LLM works**" deserves the *more* skeptical out-of-sample audit: the fancier and more flexible the model, the easier it is to mistake an in-sample fit for genuine predictive content, and the more essential a clean held-out test (on data the model never saw, ideally from a later period) becomes before believing it. The tool got smarter; the discipline did not change.

---

## Problem 6 — Replication design (pointing at nb6.3) (16 points)

**(a) (5 pts) Scoring recipe.**
1. **Tokenize:** lowercase each filing's text and split into alphabetic word tokens (`re.findall(r"[a-z]+", text.lower())`); punctuation dropped; every token counts toward the denominator.
2. **Two dictionaries:** the naive general-English negative list $D_{\text{naive}}$ (Harvard-GI-style) and the finance-specific LM-style list $D_{\text{LM}}$.
3. **NegScore:** for each filing and each dictionary, $\text{NegScore}_d = (\#\text{list words in } d)/(\#\text{total tokens in } d)$.
4. **Flag:** flag a filing negative if its NegScore $\geq \theta$ ($\theta = 0.05$ as in `nb6.3`).
5. **The diagnostic that *is* the paper:** among the words the **naive** list flags as negative in the **benign** filings, tabulate the most frequent ones. Expect them to be dominated by **benign accounting terms** — tax, cost, capital, liability, depreciation, expense — words no human would call negative in a financial sentence. Reproducing that this benign vocabulary makes up a large share of the naive list's "negativity" is the qualitative headline (Ch 6.3 §4's first exhibit, `nb6.3` Exercise 1).

**Data:** the raw 10-Ks come from **SEC EDGAR**, the SEC's free electronic filing archive. What makes this source unusual relative to CRSP/Compustat: it is **public and enormous, with no licensing wall** — the cost is not access but the engineering of parsing ~50,000 words of messy HTML/SGML into a clean bag of words. **CONVENTIONS §5 rule:** any matched *return / volume / volatility* data used for validation is licensed (CRSP-style) and must stay **read-only on GMU infrastructure (Hopper / WRDS Cloud)**; you must **pin the snapshot date** of that licensed return data in the notebook. (Per the reader's guide, `nb6.3` also ships a seeded synthetic fallback so the notebook runs offline.)

**(b) (4 pts)** The **two numbers reported side by side** to quantify the repair are the **naive false-flag rate** and the **LM false-flag rate** on the benign filings (Problems 1c, 2b) — naive high, LM near zero, the gap being the misclassification you removed. The figure `nb6.3` plots to make the over-flagging visible is the **mean NegScore by truth-label** (negative / benign / positive), with the two dictionaries as side-by-side bars: the naive bar towers over the benign-finance group while the LM bar stays low, exactly where the two should agree (the negative group) and disagree (the benign group). The one thing you must **not** claim: a **precise misclassification percentage presented as the paper's measured number** — Ch 6.3 tags the real share `[CHECK]` (qualitatively "a large share, on the order of three-quarters"), and our toy figures are illustrative props, so the honest write-up reports the *direction and order of magnitude*, not a transcribed decimal.

**(c) (4 pts)** **Out-of-sample deliverable** (Problem 5): split the matched filings into a build set and a held-out test set; build/freeze the dictionary and any threshold on the **build** set only, then confirm the tone–outcome association *on the held-out test set*; the inviolable rule is that **the test set never informs the construction** (no peeking, no refitting). **Failure-demonstration deliverable** (Problem 4): hand-construct a dozen sentences carrying **negation, sarcasm, and conditionals** ("not a bad quarter," "not exposed to litigation," "we would face severe losses only if…"), run them through the bag-of-words scorer, and the output must support the verdict that **word-counting misclassifies sentences whose meaning lives in word order — the §6 vulnerability made concrete — which is precisely the gap the embedding/LLM methods of Ch 6.5 set out to fill.**

**(d) (3 pts) Two validity threats to pre-register.**
1. *Look-ahead in the word list (Problem 5):* the threat that the dictionary was selected to correlate with returns in the same sample used to test it. **Check:** build the list on linguistic judgment (or on a build set) and validate only on a **held-out test set the construction never touched** — report the out-of-sample association explicitly.
2. *Sentiment-vs-disclosure-style confound (reader's guide §6 / referee Q2):* a filing's tone score also reflects its **length, boilerplate density, legal-template choices, and parsing rules**, not just genuine bad news. **Control:** include controls for document length / boilerplate density (and firm characteristics), or use **firm/industry fixed effects**, so the score's relation to outcomes is not just "this firm's lawyers write longer, more hedged filings"; report whether the tone effect survives those controls.

---

*End of solutions for PS 6.3. The by-hand pieces were each confirmed in Python with the exact `nb6.3` tokenizer: S1 naive $=4/9=44.4\%$ (LM $0\%$), S2 naive $=4/13=30.8\%$ (LM $0\%$), S3 naive $=1/11=9.1\%$ / LM $=2/11=18.2\%$, S4 $=0\%$ both; naive false-flag rate on benign $=2/2=100\%$ vs LM $=0/2=0\%$; the tf–idf masses $\text{mass}_P=0.6931$ vs $\text{mass}_Q=2.7726$ flip the raw ranking ($0.50$ vs $0.30$); all four trick sentences T1–T4 are wrongly flagged NEGATIVE. The full pipeline — both dictionaries, the false-flag diagnostic, the mean-NegScore-by-label bar chart, the tf–idf re-ranking, the negation-failure block, and the out-of-sample split — is built in `notebooks/week-06/nb6.3-loughran-mcdonald-sentiment.ipynb`, where you watch "tax" and "liability" light up a benign sentence and "not a bad quarter" get called negative. That is the moment Loughran & McDonald's title stops being a riddle and Ch 6.5's reason for existing comes into view.*
