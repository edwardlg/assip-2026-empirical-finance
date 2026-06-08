# Chapter 6.3 — Reader's Guide: Loughran & McDonald (2011), "When Is a Liability Not a Liability?"

> **Full citation.** Loughran, T., & McDonald, B. (2011). When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks. *Journal of Finance*, 66(1), 35–65.

You have spent five weeks turning numbers into evidence. This week the *raw material itself* changes. A firm's annual report, the SEC 10-K, is roughly fifty thousand words of prose, and somewhere in there is information the income statement does not contain: how worried management is, how much litigation looms, how uncertain the future looks to the people who know the firm best. Text-as-data is the project of turning that prose into a column of numbers you can put in a regression. The question is how — and the paper you read today taught the field how *not* to do it with the most popular tool of its era.

Here is the trick it reveals, in one breath: **the standard way of scoring text for "negativity" in 2011 was a dictionary built for novels, newspapers, and psychology experiments — and when you point it at a 10-K, most of the words it flags as "negative" are not negative at all. They are the ordinary vocabulary of accounting.** "Liability," "tax," "cost," "depreciation," "capital," "crude" — to a general-English sentiment dictionary these are dark words; to a balance sheet they are Tuesday. Loughran and McDonald showed this is not a quibble. It is a measurement error large enough to change what you conclude about whether the *tone* of a filing predicts anything. Then they did the constructive thing: built a finance-specific dictionary, put it in the public domain, and watched it become the field standard.

This is a **measurement paper**, like Petersen last week was a methods paper. Its "finding" is not a fact about markets; it is a fact about a *tool*. Read it that way. The villain is a dictionary, the evidence is a word count, and the moral — that the meaning of a word depends on the room it is spoken in — reaches all the way to the large language models you meet in Ch 6.5.

---

## 1. Research question

The plain-English question is: **does scoring financial text with a general-English sentiment dictionary misclassify the tone of that text — and can a finance-specific dictionary do better at relating to outcomes investors care about, like returns and volatility?**

Name the two pieces. The **outcome** here is not a stock return in the usual sense; it is a *measurement*: the "sentiment" or "tone" score we assign to a document. The **key right-hand-side variable** — the thing whose effect we are really testing — is the *choice of dictionary itself*. Two analysts read the same 10-K. One scores it with the Harvard General Inquirer (the "Harvard-IV-4" / "GI" word lists, the standard general-purpose psychosocial dictionary of the era). The other scores it with a list of words chosen because they are negative *in a financial context*. Loughran and McDonald ask: do these two scores disagree, do they disagree *systematically*, and which one is actually picking up signal in market data?

The motivating observation is almost embarrassingly concrete — it is the title. *When is a liability not a liability?* In general English, "liability" is a burden, a bad thing ("he was a liability to the team"), so the Harvard dictionary files it under negative words. But in a 10-K, "liability" appears thousands of times as a neutral accounting term: deferred tax liability, current liabilities, liability insurance. Every one of those mentions gets counted as a dose of negative sentiment, even though no human reader would call the sentence gloomy. The same is true of "tax," "cost," "capital," "board," "vice," "crude," "depreciation," and a long tail of others. The general dictionary is not a little bit off: Loughran and McDonald document that a *large share* of the words the Harvard list counts as negative in 10-Ks carry no negative meaning in finance at all [CHECK: the paper reports a specific fraction — on the order of three-quarters of Harvard-negative word *occurrences* in 10-Ks being words like "tax/cost/capital/liability" that are not negative in a financial sense; verify the exact percentage and whether by word-type or occurrence before quoting].

So the research question has the same two-part shape as a good measurement paper always does. **(a) Diagnosis:** how badly does the off-the-shelf tool mismeasure financial tone? **(b) Repair and validation:** if we build a domain-specific tool, does it carry more genuine signal — does finance-specific negativity line up with lower returns around the filing, higher trading volume, higher volatility — than the general tool does? The answer to (a) is "badly," and the answer to (b) is "yes, and it has been the standard ever since."

---

## 2. Identification strategy

There is no instrument here, no difference-in-differences, no randomized anything. The strategy is **construction plus validation**, and it belongs to a whole tradition of empirical work — the **bag-of-words** era of textual analysis — that you should understand as a method in its own right.

**The bag-of-words model, stated plainly.** Take a document; throw away word order, grammar, and sentence structure. What remains is a *multiset* — a bag — of the words that appeared and how many times each appeared. "The company expects continued losses" and "Continued losses the company expects" are, to a bag-of-words model, the same object. You score the document by counting how many of its words fall into a pre-specified list. If you have a list of "negative" words, the document's negativity is (roughly)
$$
\text{NegScore}_d \;=\; \frac{\#\{\text{negative-list words in document } d\}}{\#\{\text{total words in document } d\}},
$$
the share of the document made of negative-list words. Every sentiment measure in this paper, both the Harvard one and the finance one, is a count of this form. The *only* thing that differs between two competing measures is **which words are on the list** — which is why the choice of dictionary *is* the treatment.

**The construction step.** Loughran and McDonald build word lists tailored to financial disclosure. The most important is the **negative** list — words that are negative when a company uses them about itself ("loss," "litigation," "deficiency," "adverse," "restated," "termination," "going concern"). But they do not stop there. They release a family of categories, because finance cares about more than good-versus-bad mood:

- **Negative** and **Positive** tone.
- **Uncertainty** — words like "approximate," "contingency," "may," "risk," "could" — capturing how much the firm hedges about its own future.
- **Litigious** — "plaintiff," "tort," "settlement," "court" — legal exposure.
- **Strong-modal** and **weak-modal** — words signaling how firmly management commits ("will," "must," "always" versus "may," "might," "possibly").

A subtle and underrated choice: they build these lists *from the actual word frequencies in 10-Ks*, keeping a word only if it is both plausibly negative in a financial setting and common enough in filings to matter, and they handle the awkward fact that the same word can be positive or negative depending on **negation** ("not profitable") — though, as we will see in §6, bag-of-words handles negation only crudely.

**The validation step — this is the identification.** A new word list is just an opinion until it earns its keep against data. Loughran and McDonald validate by asking whether their finance-negative score *relates to market outcomes the way real negative news should*. If a 10-K's tone genuinely carries bad information, filings scored more negative should be followed by **lower abnormal returns** around the filing date, **higher trading volume**, and **higher return volatility**. The test is comparative: run these associations using the Harvard-GI negative count, then the finance-specific count, and see which shows the cleaner, more sensible relationship — and whether the Harvard measure's apparent signal *survives* once you strip out the misclassified accounting words. The identifying claim, in the spirit of CONVENTIONS §4: *a dictionary measures financial tone validly to the extent that its score moves with market reactions to the filing in the direction real bad news would move them, and not because it is mechanically counting neutral accounting vocabulary.* The headline result: the finance dictionary passes this test better than the general one, and a meaningful part of the general dictionary's apparent "negativity" was noise from misclassified words.

---

## 3. Data

The unit of observation is a **10-K filing** — one firm's annual report for one fiscal year — and, downstream, the firm-filing's market reaction.

**The filings: SEC EDGAR.** Every U.S. public company files its 10-K with the Securities and Exchange Commission, and since the mid-1990s those filings live in the SEC's **EDGAR** electronic archive, free to anyone. Loughran and McDonald assemble a large sample of 10-Ks over roughly a decade-plus window around the 1994–2008 period [CHECK: confirm the exact filing-year range and the count of 10-Ks — the paper analyzes on the order of tens of thousands of filings; verify the precise N and years]. This is a defining feature of text-as-data finance: the raw material is *public and enormous*. There is no licensing wall, as there is with CRSP or Compustat. The cost is not access; it is the engineering of parsing fifty thousand words of messy HTML/SGML into a clean bag of words (stripping tables, exhibits, HTML tags, and boilerplate — decisions that are themselves levers, see §6).

**The market data.** To validate, the filings are matched to standard return, volume, and volatility data (CRSP-style) around the filing date, plus firm characteristics (size, book-to-market, etc.) as controls. The text score is the key regressor; the market reaction is the outcome.

**The public resource — the real deliverable.** The most-used output of this paper is not a number in a table; it is a *file*. Loughran and McDonald released the **Master Dictionary** and the associated word lists (negative, positive, uncertainty, litigious, modal, and more), maintained and updated publicly ever since. When a paper today says "we measure tone using the Loughran–McDonald dictionary," it means: it downloaded these lists and counted. That a 2011 *Journal of Finance* paper's most durable contribution is a freely downloadable word list tells you something true about modern empirical finance — sometimes the most valuable thing you can publish is a clean, reusable measurement instrument.

**Filters and traps to note.** Watch the same things you watched in any sample: which filings are dropped (very small firms, financials, filings that fail to parse), and whether the parsing rules quietly change the sample. And flag a look-ahead worry up front — see §6 — because a dictionary *tuned to relate to returns in the same sample it is tested on* would be using the answer to grade itself.

---

## 4. Table-by-table reading order

Do not read this paper front to back. Read the *misclassification evidence first* — it is the whole point — then the validation horse race. Here is the order.

**First, the word-misclassification exhibit.** Find the table/list that shows *which* Harvard-negative words actually appear in 10-Ks and how often. This is the headline of the diagnosis. You are looking for the result that the most *frequent* "negative" words in filings, by the Harvard list, are words like **tax, cost, capital, liability, board, vice, crude, depreciation** — words no one would call negative in a financial sentence. The number that carries the paper is the *share* of Harvard-flagged negativity that comes from such benign words: a large fraction [CHECK: verify the exact percentage and whether reported by occurrence or by unique word]. Read this first and the rest of the paper is just consequences. If three-quarters of your "negative" signal is the word "tax," your sentiment measure is mostly an accounting-density measure wearing a costume.

**Second, the construction summary.** Skim the table that describes the finance-specific lists — how many words are in the negative list, the positive list, the uncertainty/litigious/modal lists. You do not need to memorize counts; you need to see that the categories are *finance-shaped* (uncertainty and litigious are not standard psychology categories — they exist because finance has lawsuits and forward-looking statements).

**Third, the validation regressions — the horse race.** Now the comparative tests: regressions of filing-period **abnormal returns**, **trading volume**, and **return volatility** on the tone score, run once with the Harvard-GI negative measure and once with the finance-negative measure, with the usual firm controls. Read these the way Week 5 taught you to read a table — sign, magnitude, t-stat, and *what is being held fixed across columns*. The pattern to look for: the finance-negative measure shows a cleaner, more robust association with market reactions (more negative tone → worse returns / higher volume / higher volatility), and the apparent power of the Harvard measure *weakens* once you account for the misclassified words. The specific coefficients and t-stats matter less than the *direction of the comparison*; do not quote magnitudes from memory [CHECK: read the exact coefficients and t-stats off the paper's validation tables before citing any].

**Last, the robustness and weighting tables.** The paper also explores **term weighting** — instead of counting raw word frequencies, weighting words by how *distinctive* they are using a scheme called **tf–idf** (term frequency × inverse document frequency, which down-weights words that appear in almost every filing and up-weights words that are rare across filings but frequent in this one). Read this last, as a refinement of the core message: *how* you count, not just *what* you count, affects the signal. This is also the seam that connects to Ch 6.2's text-similarity work and, eventually, to the dense vector representations of Ch 6.5.

---

## 5. What's clever

Several moves here are worth naming because you will reuse them.

**Domain-specificity as the whole idea.** The intellectual core is a single, portable insight: **the sentiment of a word is not a property of the word — it is a property of the word in its domain.** "Liability," "vice," "crude," "tax" mean different things in finance than in general English, and a tool calibrated on one domain mismeasures the other. This sounds obvious once stated, which is exactly the mark of a good measurement paper: it makes an error everyone was making feel obvious *in retrospect*. The same logic generalizes — a sentiment tool for medical notes, legal briefs, or central-bank statements needs its own dictionary. Leah, who cares about patents and text, should carry this as a law: *never reuse a measurement instrument across domains without checking that the words still mean what the instrument assumes.*

**Falsifying a widely-used tool.** It takes nerve and care to show that a standard, widely-cited tool is *wrong for your setting*. The Harvard-GI dictionary was respectable and ubiquitous; many published finance papers had used it. Loughran and McDonald did not argue abstractly that it *might* be miscalibrated — they *counted*, and showed precisely which words were doing the damage and how much. Diagnosis by enumeration is more convincing than diagnosis by assertion.

**A reusable public good.** The deepest cleverness is strategic, not statistical. By releasing the Master Dictionary publicly and maintaining it, they turned a one-paper result into *infrastructure*. The marginal researcher no longer has to build a finance dictionary; she downloads theirs. This is why the paper's citation count dwarfs that of cleverer-but-private contributions: a tool everyone can use beats a result only the authors can reproduce. When you build your capstone measurement, ask whether the most useful thing you could ship is the *instrument*, not just the finding.

**Categories beyond good/bad.** Splitting tone into negative, positive, uncertainty, litigious, and modal was a real conceptual contribution. "Uncertainty" in particular — counting hedging words — turned out to predict volatility better than raw negativity in much later work, because *how sure* a firm is about its future is different information from *how bad* the future is. Good measurement is often good taxonomy, the same lesson Petersen taught with standard errors.

---

## 6. What's vulnerable

A good reader admires the paper and then finds its edges. The edges here are mostly the edges of bag-of-words *itself*, which is why this section doubles as the on-ramp to Ch 6.5.

**Bag-of-words throws away context, and context is meaning.** This is the central limitation, and the authors would be the first to grant it. Counting words ignores **order, syntax, and scope**. "This is not a good year" contains the positive word "good," and a naive count scores it positive; the negation flips the meaning, and the bag never sees the "not." Loughran and McDonald handle simple negation with crude rules (e.g., flagging a positive word as negated if a negator appears within a few words), but the patch is partial. **Sarcasm, irony, conditionals** ("we would face severe losses *if* the unlikely event occurred"), and long-range dependencies ("the risks described in last year's filing no longer apply") are invisible to a word counter. The model literally cannot represent the idea that the same word means opposite things in two sentences. Word-counting is not meaning; it is a proxy for meaning that works *on average, over long documents*, and breaks sentence by sentence.

**Dictionaries are static; language and disclosure drift.** A fixed word list is frozen at the moment it was built. New financial vocabulary ("crypto," "SPAC," "going-concern" usage patterns, pandemic-era boilerplate) arrives; old words shift connotation; firms learn which words the algorithms flag and *adjust their writing to game the score*. A dictionary built on 1994–2008 filings may misread 2026 filings, and a measure everyone uses is a measure firms have an incentive to manage. The public list is updated over time, which helps, but the underlying fragility — *the meaning of the instrument can decay* — is structural to dictionary methods.

**Look-ahead in tuning the dictionary.** Here is the methodological worry to keep your eye on, the same family of error you met with data-snooping in Week 1. If the word list were *selected* to maximize its correlation with returns *in the very sample used to validate it*, the validation would be circular — the dictionary would be using the answer key to grade itself, and its apparent out-of-sample power would be illusory. The defense is that the lists are built on *linguistic/financial judgment about what words mean*, not fit to the return data, and that the categories are pre-specified rather than mined for return-predictability. A skeptical referee still asks: *how much of the word selection was informed, even indirectly, by what worked on the test data?* The honest standard — which Ch 6.5 will hammer — is **out-of-sample validation**: build the instrument on one set of filings, test it on filings it never saw.

**Parsing decisions are researcher degrees of freedom.** Stripping tables, exhibits, HTML, and boilerplate from a 10-K is not mechanical; different rules yield different word bags and can move the measured tone. Two labs counting "the Loughran–McDonald negative score" can disagree if they parse differently. The paper specifies its choices, but the broader lesson is that *the pipeline before the count is itself a set of decisions that should be reported and stress-tested.*

**The bridge to embeddings and LLMs (Ch 6.5).** Every one of these vulnerabilities is, at root, the same complaint: *a word is not an atom of meaning; meaning lives in context.* The next decade of text-as-data is the story of putting context back in. **Word embeddings** (word2vec, GloVe) represent each word as a dense vector learned from the company it keeps, so "good" and "great" land near each other in space — the cosine-similarity geometry you meet in Ch 6.2. **Contextual models and large language models** (the transformers behind Ch 6.5) go further: they represent each word *as a function of the whole sentence around it*, so "not a good year" and "a good year" get genuinely different representations, and negation, sarcasm, and long-range dependence become at least partly learnable rather than invisible. Loughran–McDonald is the high-water mark of the era *before* this — the most careful possible version of counting words — so reading it teaches you exactly what counting words cannot do, which is precisely the gap the embedding/LLM era set out to fill. It also carries the hardest lesson forward: a fancier model is *also* just an instrument, only as trustworthy as its out-of-sample validation. The tool got smarter; the discipline did not change.

None of this sinks the paper. It locates it: a careful, honest, enormously useful diagnosis of one tool and a clean replacement for it — with limitations the authors largely named themselves, and a frontier the field crossed in the fifteen years since.

---

## 7. Three replication exercises

These run in **nb6.3 (Loughran–McDonald sentiment pipeline)**, which hands you a 10-K parser, the LM word lists, and a small sample of filings matched to returns. They also seed **PS 6.3** (LM dictionary vs. a naive dictionary). Each escalates.

**Exercise 1 — Reproduce the misclassification (recreate the headline).** Take a handful of real 10-Ks from EDGAR (or the notebook's bundled sample). Score each for negativity *twice*: once with the Harvard-GI negative list, once with the LM finance-negative list. Then do the diagnostic that *is* the paper: among the words the Harvard list counts as negative in these filings, tabulate the most frequent ones and tag which are genuinely negative in finance versus benign accounting terms ("tax," "cost," "capital," "liability," "depreciation"). **You should reproduce the qualitative headline** — a large share of Harvard-flagged "negativity" comes from neutral accounting vocabulary, and the two negativity scores for the same filing differ substantially. This is §4's first table, built with your own hands.

**Exercise 2 — Stress the measure: build a naive dictionary and a tf–idf weighting.** Construct a deliberately *naive* negative dictionary (say, a generic web list of "negative words" with no finance filtering) and score the same filings with it. Compare its scores to the LM finance-negative scores: where do they most disagree, and on which words? Then re-score the filings using **tf–idf weighting** instead of raw counts, and see whether down-weighting ubiquitous boilerplate words changes the ranking of filings by negativity. This exercise makes you *feel* both levers from §4 — *which* words and *how* you weight them — and is the heart of PS 6.3.

**Exercise 3 — Validate out-of-sample, then break it with negation.** Split your matched filings into a build set and a held-out test set. Using only the build set, confirm the direction of the validation result — more LM-negative tone associated with lower abnormal returns / higher volume / higher volatility around the filing — then *re-estimate on the held-out filings* to check the association is not an artifact of the build sample (the out-of-sample discipline from §6). Finally, hand-construct a dozen sentences with negation, sarcasm, and conditionals ("we are *not* exposed to material litigation"), run them through the bag-of-words scorer, and watch it misclassify them. This last step is the §6 vulnerability made concrete on your own screen, and it is the exact failure that motivates the embedding/LLM methods of Ch 6.5 — the best possible setup for that chapter.

---

### Where this connects, and what to ask next

This guide sits between **Ch 6.2** (Hoberg–Phillips: cosine similarity of 10-K text — the same EDGAR raw material, vectorized for *similarity* rather than *sentiment*) and **Ch 6.5** (the AI co-pilot — embeddings and LLMs that finally put context back into text). Loughran–McDonald is the careful endpoint of the bag-of-words era: it shows both how far you can get by counting the right words and exactly where counting words stops being meaning. Carry forward two laws: *measurement instruments do not transfer across domains without re-validation*, and *every text model, dictionary or transformer, is only as honest as its out-of-sample test.*

**Go now to nb6.3 (Loughran–McDonald sentiment pipeline)** and run Exercise 1 before the next chapter. Seeing "tax" and "liability" dominate a 10-K's "negative" word count — when you know they are not negative — is the moment the paper's title stops being a riddle and becomes a method.

**Three referee questions to carry into the notebook.**

1. *Is the dictionary's apparent power out-of-sample, or did the test set help build it?* If any part of the word selection was informed by what correlated with returns, the validation is partly circular. What would a clean out-of-sample design look like, and what would you ask the authors to report to rule out look-ahead in the word list?

2. *How much of the result is sentiment versus disclosure style?* A filing's tone score also reflects its length, boilerplate density, legal-template choices, and parsing rules. How would you separate "this firm has genuinely bad news" from "this firm's lawyers write longer, more hedged filings" — and which controls or fixed effects would you demand?

3. *Where does bag-of-words break, and does it matter at the document level?* Negation, sarcasm, and conditionals are invisible to a word counter. Over a 50,000-word 10-K do these errors average out, or do they bias the score systematically (e.g., risk-factor sections that are *all* conditionals)? What evidence would tell you whether the move to context-aware models in Ch 6.5 actually buys you validity, not just complexity?
