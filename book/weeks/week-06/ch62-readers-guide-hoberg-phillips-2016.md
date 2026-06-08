# Chapter 6.2 — Reader's Guide: Hoberg & Phillips (2016), "Text-Based Network Industries and Endogenous Product Differentiation"

> **Full citation.** Hoberg, G., & Phillips, G. (2016). Text-Based Network Industries and Endogenous Product Differentiation. *Journal of Political Economy*, 124(5), 1423–1465.

Here is a question you have never had to ask, because someone answered it for you decades ago and you never noticed: *what industry is a company in?* You think you know — Apple is "technology," Coca-Cola is "beverages." But ask a precise version, *who exactly competes with Amazon?*, and the easy answer falls apart. A bookseller? A grocery chain? A cloud provider? Amazon is all of those, and the firm it fights hardest on cloud (Microsoft) is not the one it fights on groceries (Walmart). The official answer — a four-digit **SIC code** or six-digit **NAICS code**, a number slotting each firm into one box of a fixed, government-maintained tree — forces Amazon into a *single* box and declares everyone sharing that box a competitor and everyone outside it not. That is the convention this paper overthrows.

This is the paper Leah, our text-analysis student, should read first, because it is the cleanest example in finance of one idea: **the words a firm uses to describe itself are data** — in the same hard sense a stock price is data. Hoberg and Phillips take the product-description section every U.S. public firm is legally required to write in its annual report, turn each into a vector of numbers, and use those vectors to draw a map of who-competes-with-whom built from what firms *say they do* rather than from a code assigned decades ago. Reveal the trick early: the paper rests on turning prose into geometry, and the geometry is the cosine you met in Chapter 1.2 when we said correlation *is* a cosine. Hold that thought; we are about to cash it in.

One warning before the anatomy. The Week-5 papers were **causal** — they claimed *X causes Y* and lived or died on an identifying assumption. This paper is mostly **not** causal. Its central contribution is a *measurement*: a new way to define an industry. A measurement paper is judged differently — not "is the identifying assumption true?" but "is the measure better than what we had, and better *at what*?" Keep that distinction live; it is the thing most first-time readers get wrong about this paper.

---

## 1. Research question

In one plain sentence: **can we define industries from what firms *say* they do — the product descriptions in their 10-K filings — rather than from fixed SIC/NAICS codes, and does the resulting firm-specific network of competitors describe the world better?**

Two questions are stacked here; hold them apart. The first is a *measurement* question: is there a better way to draw industry boundaries than the official classification? The second is an *economics* question the better measure makes answerable for the first time: when a firm differentiates its product away from its rivals, what happens, and what drives it? The title names both halves — "Text-Based Network Industries" is the measure, "Endogenous Product Differentiation" the economics it unlocks.

Name the **outcome** and the **key variable**, as the Week-5 pack drilled you. In the measurement half the "outcome" is a definition: for each firm, a list of who its competitors are. In the economics half the key variable is **product similarity** — how close a firm's product description sits to its rivals' — and the outcomes are things competition should move: profit margins, the decision to differentiate, how firms respond when a rival or a merger crowds their product space. The unifying claim is that an industry is not a fixed box you are born into but a *neighborhood* you occupy — firm-specific (yours is not identical to your neighbor's), changing year to year as products evolve, and explaining real outcomes (return co-movement, profitability, competitive responses) better than the static government code.

Why care that economists dislike SIC codes? Because the system has a defect you can feel: it is **transitive and time-invariant**. Transitive means if A shares a box with B and B with C, then A, B, and C are all declared mutual competitors — clean partitions, no overlaps. Time-invariant means a firm's code rarely changes even as the firm reinvents itself. Both are false about real competition. Netflix fought Blockbuster, then HBO, then Disney — a moving neighborhood, not a fixed box — and its rival set overlaps but does not coincide with Disney's. Hoberg and Phillips ask: what if we let the data draw the neighborhoods, and let them overlap, and let them move?

---

## 2. Identification strategy

Keep the measurement-versus-causal distinction sharp, because "identification" behaves differently here than in Week 5. **This paper does not identify a causal effect with an instrument or a discontinuity. It *constructs a measure*, then *validates* it.** The strategy is construction plus validation. The construction is what you rebuild in nb6.2, so we do it the slow way.

**Step one: get the text.** Every U.S. public firm files a 10-K, and Item 1 is a mandated **business / product description**: a few hundred to a few thousand words saying what the firm makes and sells. Hoberg and Phillips extract that section from tens of thousands of SEC EDGAR filings. (How *cleanly* you can extract it is a vulnerability — section 6.)

**Step two: turn each description into a vector.** This is the "text-as-data" heart of the enterprise. Build a giant dictionary of every non-trivial word appearing across all descriptions — tens of thousands of distinct words. Represent firm $i$'s description as a vector $\mathbf{w}_i$ with one entry per dictionary word: entry $j$ measures how much firm $i$ uses word $j$. In the simplest **bag-of-words** scheme that entry is just a count or a presence indicator. A firm heavy on "wireless," "spectrum," "subscribers" lands far from one full of "crude," "refining," "barrels." Word order is thrown away — hence "bag," a real limitation we flag later — but it buys enormous simplicity.

A refinement nb6.2 and the AI module both lean on is **TF–IDF** — *term frequency–inverse document frequency*. Not all words are equally informative: "company" appears in every description and tells you nothing about *which* firm; "lithium" appears in few and tells you a lot. TF–IDF multiplies a word's within-document frequency (TF) by a factor that grows when the word appears in *fewer* documents (IDF), downweighting ubiquitous words and amplifying distinctive ones. The inverse-document-frequency weight for word $j$ is
$$
\text{idf}_j = \log\!\frac{D}{d_j},
$$
with $D$ the number of documents and $d_j$ the number containing word $j$. A word in every document has $d_j=D$, so $\text{idf}_j=\log 1=0$ — silenced. A word in one document out of ten thousand gets a large weight. The firm vector then has entries $\text{tf}_{ij}\cdot\text{idf}_j$. [CHECK: confirm the exact vector construction Hoberg–Phillips use — raw indicators, counts, or a TF–IDF-style weighting, and any stop-word/proper-noun filtering — before attributing TF–IDF specifically to them; TF–IDF is the standard idea we teach for nb6.2 regardless.]

**Step three: measure similarity with the cosine.** The payoff, and the moment Chapter 1.2 cashes in. For two firm vectors $\mathbf{w}_i$ and $\mathbf{w}_k$, the **cosine similarity** is
$$
\text{sim}(i,k) \;=\; \cos\theta \;=\; \frac{\mathbf{w}_i \cdot \mathbf{w}_k}{\lVert \mathbf{w}_i\rVert\,\lVert \mathbf{w}_k\rVert}
\;=\;
\frac{\sum_j w_{ij}\,w_{kj}}{\sqrt{\sum_j w_{ij}^2}\,\sqrt{\sum_j w_{kj}^2}}.
$$
This is exactly the correlation-as-a-cosine formula from Chapter 1.2, applied to word vectors instead of return vectors. The numerator is large when two firms emphasize the *same* words; the denominators normalize away description *length*, so a wordy firm and a terse one describing the same product still score similar. The result runs from $0$ (no shared vocabulary — orthogonal, $\theta=90°$) to $1$ (identical direction, $\theta=0°$). Two oil firms score near $1$; an oil firm and a streamer near $0$. "Are these two firms in the same business?" is now a number computable from text.

**Step four: build the network.** Compute that cosine for *every pair* in a year and you have a full similarity matrix. From it, Hoberg and Phillips define **TNIC — Text-based Network Industry Classifications**: firm $i$'s industry is the set of firms whose similarity to $i$ clears a chosen threshold. The property that earns the word "network" is that this is **firm-specific, time-varying, and *intransitive*.** Firm-specific: each firm centers its *own* neighborhood — no global partition. Time-varying: recomputed yearly from that year's filings, so neighborhoods drift. Intransitive: A can be similar to B and B to C without A similar to C — the Amazon case, neighbor to both Microsoft (cloud) and Walmart (groceries) though those two are not neighbors. SIC cannot represent any of this; TNIC is built to.

So the "identifying" logic of a measurement paper is its validation logic: **a text-based definition beats SIC/NAICS if it explains outcomes competition should drive — return co-movement, profit margins, competitive responses — that SIC/NAICS explains less well, on the same firms in the same years.** That is a *horse race*, not a causal claim: TNIC versus SIC, judged by fit on outcomes competition ought to move. Reading the tables, you are watching that race.

---

## 3. Data

**Unit of observation.** A firm in a year (in the network results, often a firm-*pair* in a year — every pair gets a similarity score). The text is one 10-K per firm-year.

**Source — the text.** SEC **EDGAR**, the public filing system, supplies the 10-Ks; the input is the Item 1 business/product-description section parsed out of each filing. The sample is the universe of U.S. public firms that file 10-Ks and match to financial data, over a multi-decade window beginning in the mid-1990s when EDGAR's electronic coverage becomes comprehensive. [CHECK: exact sample period and firm/observation counts — the library begins around 1996–1997 given EDGAR's electronic start; verify precise start year, end year, and N from the paper.]

**Source — the financials.** To match filings to firms and run the economic outcomes (margins, profitability, market values), the text links to **Compustat** (fundamentals) and **CRSP** (returns, market values), the workhorses you have used since Week 1, via SEC identifiers (CIK) bridged to PERMNO/GVKEY.

**Filters are decisions, and decisions are levers.** The salient ones: a firm must have a usable, extractable product description (filings where the parser fails or the section is missing/boilerplate-only drop out — a selection to keep in mind); the vocabulary is pruned (common words and likely proper nouns — company names, geography — are filtered so two firms are not "similar" merely for sharing "the" or both naming "California"); and the similarity threshold that turns the continuous matrix into discrete industries is a chosen knob. [CHECK: the specific stop-word/proper-noun filtering and threshold-calibration rule — describe qualitatively unless verified.]

**The part that outlives the paper: the public TNIC data library.** Hoberg and Phillips published the computed TNIC industries — and related similarity measures — as a **free, public data library** any researcher can download and merge into their own work. [CHECK: canonical name/host — commonly the "Hoberg–Phillips Data Library" at a university page; verify the current URL before printing it.] You do not re-parse EDGAR to use text-based industries; you pull theirs. Turning a measure into infrastructure others build on is much of why this paper is cited so heavily — and the deeper capstone lesson: a *reusable measure* can outweigh any single regression you run with it.

---

## 4. Table-by-table reading order

Read this paper in two passes mirroring its two halves. Do not start at the front; start where the measure proves itself.

**Pass one — does the measure work? (validation tables, first).** Before you care what the measure *finds*, you must believe it is *real*.

1. **The TNIC illustration.** Find the table or example showing what a firm's text-based neighborhood looks like — how many competitors a typical firm has, how the network differs from the SIC box (overlaps, intransitivity). Read it to internalize that TNIC is a different *shape* of data, not just a relabeling.
2. **The horse-race tables: does TNIC explain things SIC misses?** The heart of the validation. The canonical demonstration: firms grouped by text similarity show **stronger co-movement in outcomes** — returns, sales growth, profitability — than firms grouped by SIC, and text similarity explains cross-firm **profit-margin** differences better than the official code. Read each Week-5-style: dependent variable across the top, the TNIC-based regressor in the rows, and — critically — a *competing* SIC-based measure in the same regression so you watch TNIC win the incremental-explanatory-power contest. The number carrying this half is the one showing TNIC stays strong (often dominant) *with SIC included.* [CHECK: the specific validation outcomes and the magnitude of TNIC's advantage — describe qualitatively (TNIC beats SIC on co-movement and margins) and read exact coefficients/$R^2$ off the tables rather than quoting from memory.]

**Pass two — what does the measure find? (the product-differentiation economics).** Only after the measure earns trust do you read what it teaches.

3. **Product similarity and differentiation.** Tables linking how *crowded* a firm's product space is (high average similarity to rivals) to its margins and its incentive to differentiate. The economics: dense neighborhoods mean tougher competition; differentiation — moving your description *away* from rivals — is the strategic response.
4. **Dynamic / competitive-response tables.** Because TNIC is time-varying, the authors watch firms *move* in product space — how they respond when rivals enter or mergers reshape a neighborhood. This is what a yearly-updating *network* buys that a fixed code cannot. Read last: most novel, least essential to believing the core claim.

The Week-5 rule holds: the headline that would sink the paper if it broke is the **pass-one horse race** — TNIC must out-explain SIC, or there is no reason to prefer it. Pass two is the reward, interesting only *because* the measure passed pass one.

---

## 5. What's clever

Four moves, named because they are transferable to your own capstone.

**Letting firms define their own industry.** The deepest idea is a refusal. Rather than accept the government's top-down taxonomy, Hoberg and Phillips let *firms* say who they are, in their own words, and let the *data* draw the boundaries. The pattern generalizes: when an official classification is convenient but wrong, build your own from a primary source the classifiers ignored. The 10-K product description sat in plain sight — legally mandated, machine-readable — for decades. They were the ones who read it as data.

**Firm-specific, time-varying, intransitive networks.** SIC's three defects — one box per firm, frozen in time, no overlaps — are exactly what TNIC fixes, and it fixes them *because* it is built from pairwise similarity rather than a partition. This is a different mathematical object (a weighted network) replacing a cruder one (disjoint sets), and it is the right object for competition, which really is a web of overlapping, shifting rivalries. Recognizing when your phenomenon needs a *network* and not a *partition* is a modeling instinct worth stealing.

**Cosine similarity as the bridge from words to numbers.** The whole apparatus reduces to one operation you already knew: the cosine between two vectors. Chapter 1.2 said correlation is a cosine; this paper shows the cosine does not care whether the vectors hold returns or word counts. That generality is why this paper launches the AI module (Ch 6.5): modern language models represent text as vectors and compare them with cosine similarity, so the "embedding" you will meet there is the grown-up cousin of the bag-of-words vector you build in nb6.2.

**A reusable public dataset.** The most *consequential* cleverness is sociological. By publishing the TNIC library, the authors made their measure a public good — hundreds of later papers use TNIC industries without re-deriving them, the way you use Fama–French factors without re-sorting portfolios. Infrastructure compounds: every paper built on it is, indirectly, evidence for it. Designing a capstone, ask not only "what do I find?" but "could what I *build* be useful to the next person?"

---

## 6. What's vulnerable

A measurement paper has measurement vulnerabilities, different from Week 5's causal threats. The right skeptical question is not "what confounds the treatment?" but **"what makes the text a noisy or biased signal of what the firm actually does?"** Four soft spots a referee will press.

**Boilerplate and legal language.** A 10-K is written by lawyers as much as managers; large stretches are formulaic and shared across firms — risk-factor language, disclaimers, accounting boilerplate. If that leaks into the vectors, two firms score "similar" because they share a law firm's templates, not because they make similar products. Restricting to the product-description section and downweighting ubiquitous words limits this, but does not erase it — and as disclosure norms drift over time, the boilerplate baseline drifts too, contaminating the *time-varying* comparisons. The skeptic asks: *how much measured similarity is product, and how much is shared legalese?*

**Firms' incentives in self-description.** The sharpest critique, and the one specific to *self-reported* text. Firms choose how to describe themselves, with motives: vaguely to avoid tipping off rivals, grandly to flatter investors ("we are an AI company now"), conservatively to manage legal exposure. If description and reality diverge *systematically* with something that also drives the outcomes, the measure inherits that bias. Worse, since differentiation is itself an outcome, there is reflexivity: a firm that *talks* differently is coded differentiated, but talking different is not always *being* different. The skeptic asks: *are we measuring product differentiation, or differentiation in marketing prose?*

**Bag-of-words ignores meaning.** The representation throws away word order and, basically, synonymy and context. "We do not compete in semiconductors" and "we compete in semiconductors" give nearly identical bags; "automobile" and "car" are treated as unrelated. The measure sees *vocabulary overlap*, which correlates with shared business but is not the same thing. This is exactly the gap the embedding models of Ch 6.5 close — meaning, not word identity — which is why this paper sits one chapter before the AI module: it is the bag-of-words *ceiling* that motivates moving past it. The skeptic asks: *would a measure that understood meaning redraw these neighborhoods?*

**Parsing and section-extraction noise.** Everything upstream depends on correctly pulling Item 1 from a messy, inconsistently formatted, decades-spanning EDGAR corpus. Formats change; HTML and plain-text eras differ; some firms bury or merge the description. Every parsing error injects noise — or worse, *selection*, if cleanly-parsing filings differ systematically from the rest (larger, better-resourced firms file cleaner documents). The measure is only as good as a long, unglamorous extraction pipeline. The skeptic asks: *how were extraction failures handled, and could the dropped filings be a non-random slice of the economy?*

None of these sinks the paper — the pass-one validation is the defense, showing the measure out-predicts SIC *despite* the noise. They locate it: a genuinely better industry measure, built from a signal that is informative but self-reported, vocabulary-based, and parser-dependent, with limits the next generation of text methods is built to push against.

---

## 7. Three replication exercises

These run in **nb6.2 (10-K text vectorization & similarity)**, which hands you a small corpus of product descriptions and the tooling to vectorize them. The goal is not the full TNIC library — that is a months-long pipeline — but a *mini* version on a handful of firms, so the magic becomes mechanical in your own hands.

**Exercise 1 — Build a mini cosine-similarity measure and rediscover an industry.** Take product descriptions for 15–20 well-known firms across a few obvious industries (two oil majors, two airlines, two banks, two streamers, two automakers). Tokenize, drop stop-words, build a TF–IDF matrix, compute the full pairwise cosine matrix. **You should reproduce the core intuition with your own code:** the two oil firms score near each other, the two airlines near each other, an oil firm and an airline low — *without ever telling the code what an industry is.* Sam will recognize the same trick that builds a return-correlation matrix; print the similarity matrix as a heatmap and watch the industry blocks light up on the diagonal.

**Exercise 2 — Stress the construction: show the measure depends on your choices.** Re-run Exercise 1 changing one knob at a time. (a) Swap TF–IDF for plain counts and watch "company" and "products" pull *everyone* toward similarity — showing *why* IDF reweighting matters. (b) Change the stop-word list, or fail to strip proper nouns, and show two firms scoring "similar" merely for both naming the same state. (c) Move the similarity *threshold* and watch a firm's competitor count balloon or collapse. The section-3 lesson made tactile: **knobs are levers**, and a measurement paper's claims are only as stable as the choices behind them.

**Exercise 3 — Extend to the network properties SIC cannot represent.** Pick a firm straddling two businesses (an Amazon-like or a conglomerate) and show with your scores that it neighbors firms in *two* blocks that are *not* neighbors of each other — **intransitivity** on your own data: $\text{sim}(A,B)$ and $\text{sim}(B,C)$ both high, $\text{sim}(A,C)$ low. Then, if the notebook supplies two years of filings for a firm that changed its business, recompute its neighborhood each year and show it *moved* — **time-variation**. Together these reproduce, in miniature, the overlapping-and-shifting neighborhoods that are the whole reason TNIC beats SIC.

---

### Where this connects, and what to ask next

This guide is the empirical-finance face of a tool you first met as pure geometry. **Chapter 1.2** said correlation is the cosine of an angle between two vectors; here the same cosine, pointed at word vectors, redraws the map of American industry. It sets up the rest of Week 6: **Ch 6.3 (Loughran–McDonald)** stays in the bag-of-words world but asks a different question of the same text — *tone*, via finance-specific word lists — and **Ch 6.5 (the AI Co-Pilot)** is where bag-of-words gives way to learned *embeddings* that capture meaning, answering this paper's "bag-of-words ignores meaning" vulnerability. Read in order, Week 6 is one long argument about turning words into numbers responsibly.

**Go now to nb6.2 (10-K text vectorization & similarity)** and do Exercise 1 before the next chapter. The instant your own code scores two oil firms as near-twins and an oil firm and an airline as strangers — with you having defined no industries at all — the abstraction collapses into something you *know*, and you never again read a 10-K as merely a legal document.

**Three referee questions to carry into the notebook.**

1. *Product, or prose?* The measure scores firms on the words they choose to describe themselves. What evidence in the paper convinces you the similarity tracks real product overlap rather than shared marketing language or shared legal boilerplate — and what test would you run to separate the two?
2. *Is the validation a fair race?* TNIC is shown to out-explain SIC on co-movement and margins. Is the comparison apples-to-apples — same firms, same years, SIC entered with comparable flexibility — or could TNIC win partly because it is a *finer* partition (more, smaller groups) that mechanically fits better? What would you demand to rule that out?
3. *What does meaning add?* If you replaced bag-of-words vectors with modern embedding vectors (Ch 6.5) that understand synonyms and negation, which of this paper's neighborhoods do you expect to change most — and is there any result here that would *flip* if the measure understood that "we do not compete in X" is the opposite of "we compete in X"?
