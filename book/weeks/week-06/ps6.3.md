# PS 6.3 — The LM Dictionary vs. a Naive Dictionary: When a Liability Is Not a Liability

**Course:** 8-Week Empirical Finance Camp · Week 6 · Problem Set 6.3
**Covers:** Ch 6.3 (Reader's Guide: Loughran & McDonald 2011), with a forward pointer to Ch 6.5 (embeddings / LLMs) and a look-ahead callback to Week 1 (data-snooping).
**Paper:** Loughran, T., & McDonald, B. (2011). *When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks.* Journal of Finance, 66(1), 35–65.
**Methods allowed:** only what is built through Ch 6.3 and the companion notebook nb6.3 — the **bag-of-words** model (tokenize, lowercase, drop order/grammar, keep a multiset of word counts); the **dictionary NegScore** $\text{NegScore}_d = (\#\text{negative-list words in } d)/(\#\text{total words in } d)$; a flag rule (flag a document "negative" if its NegScore clears a threshold); a **false-flag rate** on documents a human reads as neutral; **tf–idf** weighting $w_{t,d}=\text{tf}_{t,d}\times \text{idf}_t$ with $\text{idf}_t=\ln(N/\text{df}_t)$; the bag-of-words **negation/context failure**; and the **out-of-sample** discipline from Ch 6.3 §6. You do **not** need any regression, the validation horse race's actual coefficients, embeddings, or any code beyond what nb6.3 already gives you.

**Total: 100 points.** Point values are stated per problem. Show your reasoning — a correct final number with no derivation earns roughly half credit, because the reasoning *is* the skill we are grading. Solutions are in Appendix E (`E-w6-ps6.3-solutions.md`); try every part before you look.

A note on the difficulty curve. Problem 1 is the by-hand warm-up that *is* the paper's title: score four short finance sentences with a general-English negative list and watch ordinary accounting words ("liability," "tax," "cost," "depreciation") get flagged as gloom. Problem 2 swaps in a finance-specific (LM-style) list and makes you **quantify** how much misclassification you just removed. Problem 3 adds the second lever from Ch 6.3 §4 — *how* you count, not just *what* you count — with a tf–idf weighting that can flip which filing looks more negative. Problem 4 is the conceptual heart and the on-ramp to Ch 6.5: hand the bag-of-words scorer a sentence with **negation** ("not a bad quarter") and watch it fail, because a word counter cannot see the word order that carries the meaning. Problem 5 is the referee's validity task: a dictionary tuned on the same sample it is tested on is grading itself with the answer key — the look-ahead worry, straight out of Week 1. Problem 6 is the replication-design task that hands off to `nb6.3`. Throughout we stay with **Leah**, our text-and-patents student, who has wanted to turn prose into a column of numbers all week.

**A standing rule on numbers.** Every word list, sentence, and count in this sheet is **illustrative** — clearly labeled, hand-written, internally consistent, and chosen to make the arithmetic clean. The two dictionaries below are *teaching subsets*, not the real Harvard General Inquirer list or the full Loughran–McDonald Master Dictionary; do **not** memorize their membership as the paper's. The only claim we make about the real paper is the qualitative Ch 6.3 one: a *large share* of the "negative" word occurrences a general-English dictionary finds in 10-Ks are benign accounting terms, and the finance-specific LM dictionary is the field standard that fixed this. Do not quote a precise misclassification percentage as the paper's number — Ch 6.3 flags that figure `[CHECK]`.

**The two dictionaries (illustrative teaching subsets).** Use these exact lists for every by-hand computation. They are the same two contestants you will meet in `nb6.3`.

- **Naive general-English negative list** $D_{\text{naive}}$ (a Harvard-GI-style stand-in). Note it contains words that are negative in ordinary English but *neutral in a balance sheet* — that is the trap:
  > liability, liabilities, tax, taxes, cost, costs, depreciation, crude, vice, capital, expense, expenses, loss, losses, lose, bad, decline, declined, weak, doubt, adverse, fraud, default, severe, fail, failed, risk

- **Finance-specific (LM-style) negative list** $D_{\text{LM}}$ — built on what words *mean in a financial disclosure*, with the benign accounting terms deliberately excluded:
  > loss, losses, litigation, adverse, deficiency, restated, termination, terminated, bankruptcy, default, doubt, impairment, fraud, weakness, decline, declined, weak, severe, restructuring, alleging

**Tokenizer (use this exactly).** Lowercase the text; a *token* is a maximal run of alphabetic characters (regex `[a-z]+`); punctuation is dropped; every token counts toward the denominator $\#\{\text{total words}\}$. So "tax," and "tax" are the same token, and a possessive "board's" tokenizes to two tokens, `board` and `s`. This is the tokenizer in `nb6.3`; matching it lets you check your by-hand answers against the notebook to the digit.

**Flag rule (use this exactly).** A document is **flagged negative** by a dictionary if its NegScore is at least the threshold $\theta = 0.05$ (i.e., $\geq 5\%$ of its tokens are on that dictionary's list).

---

## Problem 1 — Score finance prose with a general-English list, by hand (16 points)

Leah lifts four one-sentence excerpts from a sample of filings. A careful human reader labels them as shown in the **truth** column (this label is what a person who *understands finance* would assign; it is the ground truth we are grading the dictionaries against).

| Doc | Truth | Sentence |
|-----|-------|----------|
| **S1** | benign | *The deferred tax liability increased as depreciation expense rose.* |
| **S2** | benign | *Our Vice President reviewed the cost of capital and the crude oil reserve.* |
| **S3** | negative | *The company incurred a substantial net loss and an impairment charge.* |
| **S4** | positive | *Revenue grew and the board approved a higher dividend on solid demand.* |

"Benign" means *neutral accounting prose* — a human reads it as ordinary bookkeeping, neither good news nor bad. Score each sentence with the **naive general-English list** $D_{\text{naive}}$.

**(a) (4 pts)** Tokenize **S1** with the rule above and write out its tokens in order. State $\#\{\text{total words}\}$ (the denominator). Then list which of those tokens are on $D_{\text{naive}}$ and compute $\text{NegScore}^{\text{naive}}_{\text{S1}}$ as an exact fraction and a percent.

**(b) (4 pts)** Do the same for **S2**: total tokens, the naive-list hits, and $\text{NegScore}^{\text{naive}}_{\text{S2}}$.

**(c) (4 pts)** Now S3 and S4. Compute $\text{NegScore}^{\text{naive}}_{\text{S3}}$ and $\text{NegScore}^{\text{naive}}_{\text{S4}}$ (you may state the token counts more briefly here). Then apply the flag rule ($\theta = 0.05$) to **all four** sentences and report, for each, whether the naive list flags it negative.

**(d) (4 pts)** Here is the paper's title made concrete. Look at *which* words fired on the two benign sentences S1 and S2. In two or three sentences: name the specific words doing the flagging, explain why a human calls every one of them neutral *in a financial context* even though they are dark words in general English, and state what kind of document property the naive NegScore is *actually* measuring on these two sentences (hint: it is not sentiment — it is the density of a particular vocabulary). Connect this to Loughran & McDonald's (2011) one-line diagnosis.

---

## Problem 2 — Recompute with the LM finance list and quantify the misclassification reduction (16 points)

Now run the second contestant. Re-score the same four sentences with the **finance-specific list** $D_{\text{LM}}$, which was built precisely to *exclude* the benign accounting words that tripped up the naive list.

**(a) (5 pts)** Compute $\text{NegScore}^{\text{LM}}$ for all four sentences (S1–S4), as fractions and percents, using the same tokenizations from Problem 1. For each sentence list which LM-list words (if any) fired. Apply the flag rule ($\theta = 0.05$) and report the LM flag for each.

**(b) (5 pts)** Build the comparison table the paper is really about. The relevant error here is a **false flag**: flagging as "negative" a sentence a human calls *not negative* (the benign and positive ones). Restrict to the two **benign** sentences (S1, S2) — the neutral accounting prose — and compute the **false-flag rate** of each dictionary on that block:
$$
\text{false-flag rate} \;=\; \frac{\#\{\text{benign sentences a dictionary flags negative}\}}{\#\{\text{benign sentences}\}}.
$$
Report the naive false-flag rate and the LM false-flag rate. State the **reduction** (naive rate minus LM rate) in plain words.

**(c) (3 pts)** Count word *occurrences*, not just sentences, to mirror the paper's headline exhibit. Across the two benign sentences combined, how many total naive-negative word *occurrences* are there, and what fraction of those occurrences are **benign accounting terms** (the ones that carry no negative meaning in finance)? State the fraction and connect it to the Ch 6.3 claim about what share of a general dictionary's flagged "negativity" in 10-Ks is benign vocabulary — being careful, per the standing rule, *not* to present your toy fraction as the paper's measured number.

**(d) (3 pts)** State precisely *why* $D_{\text{LM}}$ does better here — not "it is finance-specific" as a slogan, but the mechanical reason in terms of *which words were removed from the list and what those words were doing to the score*. Then name the one law from Ch 6.3 §5 ("what's clever") this exercise demonstrates — the portable insight about the sentiment of a word and the domain it lives in.

---

## Problem 3 — tf–idf weighting: *how* you count, not just *what* you count (18 points)

So far every word on the list counted the same — one hit, one unit of negativity. But Ch 6.3 §4's last refinement is that **how** you weight a word matters. A word like "risk" appears in *every* 10-K's risk-factor section; it is boilerplate, and counting it heavily makes a filing look negative just for being long and legally cautious. **tf–idf** down-weights such ubiquitous words and up-weights words that are *distinctive* — rare across filings but present in this one.

Recall the definition. With $N$ documents in the corpus, for a term $t$ let $\text{df}_t$ be the **document frequency** (the number of documents containing $t$ at least once) and $\text{tf}_{t,d}$ the **term frequency** (the count of $t$ in document $d$). The **inverse document frequency** and the tf–idf weight are
$$
\text{idf}_t \;=\; \ln\!\Big(\frac{N}{\text{df}_t}\Big), \qquad w_{t,d} \;=\; \text{tf}_{t,d}\times\text{idf}_t .
$$
(This is the textbook unsmoothed idf; `nb6.3` uses scikit-learn's smoothed variant $\ln\!\big((1+N)/(1+\text{df}_t)\big)+1$, which never hits exactly zero — note the difference but use the textbook form for the by-hand arithmetic.)

Leah has a corpus of **$N = 4$** one-line risk-factor excerpts. Across the whole corpus, the four negative-list terms she cares about have these document frequencies:

| Term $t$ | $\text{df}_t$ (out of $N=4$) |
|----------|:---:|
| risk | 4 |
| litigation | 2 |
| bankruptcy | 1 |
| impairment | 1 |

**(a) (5 pts)** Compute $\text{idf}_t$ for each of the four terms, leaving answers in terms of $\ln(\cdot)$ and as a decimal to four places. One value is exactly $0$ — identify it and explain in one sentence *why* a word that appears in every document in the corpus gets zero tf–idf weight, and what that means for a word like "risk."

**(b) (6 pts)** Leah ranks two filings head-to-head by negativity. Each filing is 10 tokens long; here are the negative-list words each contains (all other tokens are off-list, neutral words):

- **Filing P:** the word *risk* appears **4 times** and *litigation* **once**.
- **Filing Q:** *risk* once, *bankruptcy* once, *impairment* once.

First compute each filing's **raw-count** NegScore (negative-list words / total tokens) and state which filing the raw count ranks as more negative. Then compute each filing's **tf–idf-weighted negative mass**, $\sum_{t} \text{tf}_{t,d}\,\text{idf}_t$ summed over the negative-list words it contains, and state which filing tf–idf ranks as more negative. Show the two sums.

**(c) (4 pts)** The ranking **flips** between the two schemes. Explain in two or three sentences *why*: what is filing P mostly made of, what is filing Q made of, and which scheme is closer to what a human analyst would call "more genuinely negative"? Tie this to the boilerplate problem the chapter warns about — a long, legally cautious filing scoring as "negative" on raw counts.

**(d) (3 pts)** State the general principle and one honest caveat. The principle: in one sentence, what does tf–idf systematically do to ubiquitous words versus rare ones, and why does that help a sentiment score? The caveat (from the `nb6.3` discussion): on a *tiny* corpus where almost every word appears in only one document, tf–idf barely re-ranks anything — explain in one sentence why, in terms of what $\text{df}_t$ looks like when the corpus is small.

---

## Problem 4 — Breaking the bag: negation and context (failure task) (18 points)

This is the conceptual heart of the sheet and the exact failure that motivates Ch 6.5. The bag-of-words model **throws away word order**. That is fine on average over a 50,000-word document, but sentence by sentence it can inverts meaning, because the words that *flip* a sentence's sentiment — "not," "far from," "failed to" — are themselves invisible to a list of content words.

Leah hand-constructs four sentences engineered so that word order carries the meaning. The **human** column is the reading a person would give. Score each with a combined bag-of-words negative vocabulary $D_{\text{bow}} = D_{\text{naive}} \cup D_{\text{LM}}$ (the union of both lists from the header) and the same threshold $\theta = 0.05$. The point is that the failure is intrinsic to *word-counting itself*, not to one particular list.

| Doc | Human reading | Sentence |
|-----|---------------|----------|
| **T1** | positive | *This was not a bad quarter; demand held up better than feared.* |
| **T2** | positive | *We are not exposed to any material litigation or adverse judgment.* |
| **T3** | neutral (conditional) | *We would face severe losses only if the unlikely default were to occur.* |
| **T4** | positive | *The company failed to lose money this year, exceeding every target.* |

**(a) (6 pts)** For each of T1–T4, list which $D_{\text{bow}}$ words fire, give the NegScore (you may approximate the denominator by counting tokens), and state whether the bag-of-words scorer flags the sentence **NEGATIVE** under $\theta = 0.05$. (For each sentence at least one negative-list word fires; you do not need exact decimals if you correctly identify that the score clears the threshold.)

**(b) (4 pts)** For each sentence, name the **specific word or phrase** that carries the true meaning and that the bag-of-words model cannot see. (E.g., T1's meaning hinges on a single short word.) Be specific to each sentence: the device in T1, T2, T3, and T4 are *not* all the same.

**(c) (4 pts)** State, in two or three sentences, the *general* reason a word counter must get these wrong — phrased as a property the bag-of-words representation *structurally lacks*. Your answer should make clear that this is not a fixable bug in the word list (adding "not" to a list does not solve it) but a limit of the representation itself. Use the idea that "the same word means opposite things in two sentences."

**(d) (4 pts)** This is the bridge to Ch 6.5. The chapter says the next decade of text-as-data is the story of *putting context back in*. In three or four sentences: explain what a **word embedding** (word2vec / GloVe, the cosine-similarity geometry from Ch 6.2) buys you over a flat word list, and then what a **contextual model / LLM** (the transformers of Ch 6.5) buys you *beyond* embeddings — specifically, why a contextual model can represent "not a bad quarter" and "a bad quarter" differently while a fixed embedding for "bad" cannot. Close with the one discipline Ch 6.3 §6 insists carries forward to those fancier models unchanged (hint: it is the subject of Problem 5).

---

## Problem 5 — Validity and look-ahead: don't tune the dictionary on the test sample (16 points)

A referee's job. A new word list is just an opinion until it earns its keep against data — but *how* it earns its keep decides whether the validation means anything. This problem is the Ch 6.3 §6 worry, which is the same data-snooping error you met in Week 1, wearing text-analysis clothes.

Leah's overeager labmate proposes a procedure. *"Forget linguistic judgment. I have 5,000 filings, each matched to its filing-window abnormal return. I'll start with a big candidate vocabulary, and **keep on my 'negative' list only the words whose presence correlates with low returns in these 5,000 filings**. Then I'll show that my new dictionary's NegScore predicts low returns in — the same 5,000 filings. Look how high the correlation is! My dictionary works."*

**(a) (5 pts)** Name the error precisely (it has a name from Week 1) and explain in two or three sentences *why* the labmate's validation is circular. Your answer must use the phrase "grading itself with the answer key" or an equivalent, and must say what role the return data played twice (once in *building* the list, once in *testing* it) — and why that double use guarantees a high in-sample correlation even if the dictionary has no genuine predictive content.

**(b) (4 pts)** Contrast this with how Loughran & McDonald actually built their lists, per Ch 6.3. State the two features of their construction that defend against the look-ahead charge: (i) what the word selection was based on *instead of* the return data, and (ii) what was true about the categories (negative, positive, uncertainty, litigious, modal) *before* any validation regression was run. Explain why each feature breaks the circularity.

**(c) (4 pts)** State the clean fix — the **out-of-sample** design — as a concrete two-set procedure a referee would accept: what you do on the **build set**, what you do on the **held-out test set**, and the one rule about the test set that must never be violated. Then state in one sentence what result on the held-out set would convince you the dictionary carries *genuine* signal rather than a fit to one historical window.

**(d) (3 pts)** Ch 6.3 §6 warns this same discipline must survive the move to fancier models. In two sentences: why is a large language model with millions of parameters *more* exposed to the look-ahead / overfitting worry than a 2,000-word dictionary, not less — and what does that imply about which claim ("our dictionary works" vs. "our LLM works") deserves the *more* skeptical out-of-sample audit?

---

## Problem 6 — Replication design (pointing at nb6.3) (16 points)

Leah is about to open `nb6.3` and rebuild Loughran & McDonald's headline on a real (or, offline, synthetic) sample of filings. Before touching the keyboard, she writes down the design so the result is honest and reproducible. Answer each in the empirical-spec spirit of CONVENTIONS §4 — name the object, not a hand-wave.

**(a) (5 pts)** Write the **scoring recipe** as a numbered procedure a classmate could follow to reproduce the misclassification headline (Ch 6.3 §4's *first* exhibit, and `nb6.3`'s Exercise 1): the tokenization step; what the two competing dictionaries are; how NegScore is computed; how a document is flagged; and the **one diagnostic** that *is* the paper — among the words the naive list flags as negative in the benign filings, what you tabulate and what you expect to find (which words dominate, and that they are benign accounting terms). State the **data**: where the raw 10-Ks come from (and the one thing that makes that source unusual relative to CRSP/Compustat), and — per CONVENTIONS §5 — the one rule you must honor about any matched *return* data and the snapshot you must pin.

**(b) (4 pts)** State the **two numbers you will report side by side** to quantify the repair (tie to Problems 1–2), and the one figure `nb6.3` plots to make the over-flagging visible (hint: mean NegScore by truth-label, both dictionaries). Then flag explicitly the one thing you must **not** claim: a precise misclassification percentage presented as the paper's measured number — state why (tie to the Ch 6.3 `[CHECK]` and the standing rule on numbers).

**(c) (4 pts)** State the **out-of-sample deliverable** (tie to Problem 5): what you split, what you estimate on each piece, and the one rule about the test set. Then state the **failure-demonstration deliverable** (tie to Problem 4): the kind of sentences you hand-construct, what you run them through, and the one sentence of verdict the output must support about where bag-of-words breaks — and which later chapter that failure sets up.

**(d) (3 pts)** Name **two** validity threats from this sheet you will pre-register in the write-up so it survives a referee — one about *look-ahead in the word list* (Problem 5) and one about a *confound* the reader's guide raises (a filing's tone score also reflects its length, boilerplate density, and parsing rules, not just genuine bad news). For each, state the single check, split, or control that addresses it.

---

*End of PS 6.3. When you have attempted everything, check yourself against `book/appendices/E-solutions-manual/E-w6-ps6.3-solutions.md`. The by-hand pieces (Problems 1–3) can be confirmed on paper or in a few lines of Python; the misclassification headline (Problems 1–2), the tf–idf re-ranking (Problem 3), the negation failures (Problem 4), and the out-of-sample split (Problem 5) all come alive in `nb6.3` (`notebooks/week-06/nb6.3-loughran-mcdonald-sentiment.ipynb`), where you score a small corpus with both dictionaries, watch "tax" and "liability" light up a benign sentence, flip a ranking with tf–idf, and hand the scorer "not a bad quarter" and watch it call it negative. The moment that last sentence is flagged — when you know it is good news and the counter does not — is the moment the paper's title stops being a riddle and becomes the reason Ch 6.5 exists.*
