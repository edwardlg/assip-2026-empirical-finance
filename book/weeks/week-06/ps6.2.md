# Problem Set 6.2 — 10-K Cosine Similarity & TNIC Mini-Build

**Covers Chapter 6.2 (Reader's Guide: Hoberg & Phillips (2016)).** This set is a *replication-flavored*
walk through the measurement machinery of Hoberg and Phillips (2016), "Text-Based Network Industries and
Endogenous Product Differentiation." Methods through Ch 6.2 only: turning a firm's 10-K **product
description** (Item 1) into a **bag-of-words vector**; comparing two firm vectors with **cosine
similarity** — the *same* cosine you met in Chapter 1.2 when we said correlation *is* a cosine, now
pointed at word counts instead of returns; the **TF–IDF** reweighting that down-weights ubiquitous words;
and the construction of **TNIC** (Text-based Network Industry Classifications) from a similarity matrix
and a threshold $\tau$, with its three signature properties — **firm-specific, time-varying,
intransitive** — that a fixed SIC code cannot represent. Notation follows the Conventions: firm $i$'s
description is a vector $\mathbf{w}_i$ with one entry per dictionary word $j$; $w_{ij}$ is the weight of
word $j$ in firm $i$; the cosine similarity between firms $i$ and $k$ is
$$
\text{sim}(i,k) \;=\; \cos\theta \;=\; \frac{\mathbf{w}_i \cdot \mathbf{w}_k}{\lVert\mathbf{w}_i\rVert\,\lVert\mathbf{w}_k\rVert}
\;=\;
\frac{\sum_j w_{ij}\,w_{kj}}{\sqrt{\sum_j w_{ij}^2}\;\sqrt{\sum_j w_{kj}^2}}.
$$

Six problems, escalating, **100 points total**. Every numerical input is supplied so you can work the
arithmetic by hand — no computer needed for Problems 1–4. The companion notebook **nb6.2**
(`notebooks/week-06/nb6.2-10k-text-similarity.ipynb`) lets you scale the same operations to a 16-firm
corpus with `scikit-learn`'s `CountVectorizer`, `TfidfVectorizer`, and `cosine_similarity`, and watch the
industry blocks light up on a heatmap — but the *understanding* is built here, by hand, on three short
descriptions.

**The grading rule of this set:** a number reported *without saying what it means* — a cosine without the
words "shared vocabulary," a TNIC neighbor list without naming the property it demonstrates (firm-specific,
intransitive) — earns half credit at most. As everywhere in this book, this is a **measurement** paper, so
the skill is *reading the measure*: where it comes from, what choice each number depends on, and where it
is a noisy or biased signal of what the firm actually does. Whenever you name a vulnerability, name the
construction choice that mitigates it.

> **A standing warning on numbers and text.** Every word count, cosine, IDF weight, similarity matrix, and
> product description in this problem set is **illustrative** — invented to make the arithmetic clean and
> the reasoning visible. **None of it is from Hoberg and Phillips's tables or the TNIC data library.** Do
> not quote any figure here as if it were theirs. The *qualitative* facts (two same-industry firms score
> high; cosine normalizes away length; common words must be down-weighted; TNIC is firm-specific,
> time-varying, and intransitive where SIC is not) are well established and safe to state; any precise
> number belongs in your own replication in nb6.2, not in memory. Citation by name: Hoberg & Phillips
> (2016).

Problems 1–3 share one small world, defined once here so you can carry the vectors between them.

> **The illustrative three-firm corpus (the working world).** After a firm files its 10-K, we extract
> Item 1 (the product description), lowercase it, and **drop stop-words** (ultra-common function words like
> *we, and, to, into, the* that carry no product information). What survives is a short list of **content
> words**. Here are three deliberately tiny descriptions, already tokenized and stop-word-stripped, with
> each content word's count:

> | Firm | What it is | Content words (with counts) |
> |:---|:---|:---|
> | **A** | an oil firm | `oil`×2, `crude`×1, `refine`×1, `fuel`×1 |
> | **B** | an oil firm | `oil`×2, `refine`×1, `fuel`×1, `barrels`×1 |
> | **C** | an airline | `flights`×1, `airline`×1, `tickets`×1, `travel`×1 |

> The **union dictionary** across the three firms is the set of all content words that appear in any of
> them: `{airline, barrels, crude, flights, fuel, oil, refine, tickets, travel}` — nine words. Firm $i$'s
> bag-of-words vector $\mathbf{w}_i$ has one entry per dictionary word, equal to that word's count in firm
> $i$ (zero if absent). You will build all three vectors in Problem 1.

---

## Problem 1 — Vectorize three product descriptions and compute cosine similarity by hand (24 points)

This is the factory floor of the whole paper: prose in, geometry out. You will turn three product
descriptions into vectors and measure who is near whom — *without ever telling the arithmetic what an
industry is.*

**(a)** [6 pts] Write out the three bag-of-words vectors $\mathbf{w}_A, \mathbf{w}_B, \mathbf{w}_C$ over
the nine-word union dictionary, in the fixed alphabetical order
`[airline, barrels, crude, flights, fuel, oil, refine, tickets, travel]`. (Each vector is nine numbers.)

**(b)** [8 pts] Compute the cosine similarity $\text{sim}(A,B)$ between the two oil firms. Show the three
pieces explicitly: the **dot product** $\mathbf{w}_A\cdot\mathbf{w}_B = \sum_j w_{Aj}w_{Bj}$, and the two
**norms** $\lVert\mathbf{w}_A\rVert = \sqrt{\sum_j w_{Aj}^2}$ and $\lVert\mathbf{w}_B\rVert$. Then assemble
the cosine. Report it as an exact fraction and as a decimal to three places.

**(c)** [4 pts] Compute $\text{sim}(A,C)$ and $\text{sim}(B,C)$ (oil firm vs. airline). You should find
both are exactly $0$ — explain in one sentence *why* the cosine is exactly zero here, in terms of the
words A and C share (or do not share), and what angle $\theta$ a cosine of $0$ corresponds to.

**(d)** [4 pts] You just produced a $3\times3$ similarity matrix purely from word counts, and the two oil
firms came out near-twins while each oil firm and the airline came out strangers — *with no industry
labels supplied anywhere.* State in two sentences what this demonstrates about the central idea of Hoberg
and Phillips (2016): that an industry can be **discovered from text** rather than assigned by a code.

**(e)** [2 pts] **The Chapter 1.2 connection.** In Chapter 1.2 you learned that the correlation between two
mean-centered data vectors *is* the cosine of the angle between them. State in one sentence what is the
*same* and what is *different* between that correlation-as-cosine and the similarity you just computed
(Hint: same formula; what plays the role of the "data vector," and is the word-count vector mean-centered?).

---

## Problem 2 — TF–IDF: why down-weight common words (16 points)

The raw bag-of-words count treats every word as equally informative. It is not. This problem shows *why*
the standard fix — **TF–IDF**, term frequency times inverse document frequency — is necessary, and makes
the down-weighting concrete.

Recall the inverse-document-frequency weight for word $j$, with $D$ the number of documents (firms) and
$d_j$ the number of documents containing word $j$:
$$
\text{idf}_j = \log\!\frac{D}{d_j}.
$$
The TF–IDF entry for word $j$ in firm $i$ is then $w_{ij} = \text{tf}_{ij}\cdot\text{idf}_j$, where
$\text{tf}_{ij}$ is the count of word $j$ in firm $i$.

Consider a corpus of $D = 4$ firms with these document frequencies:

| Word | $d_j$ (docs containing it) |
|:---|:---:|
| `company` | 4 |
| `products` | 3 |
| `oil` | 2 |
| `lithium` | 1 |

**(a)** [6 pts] Compute $\text{idf}_j$ (using natural log) for each of the four words. Report all four
values. Which word is **completely silenced** (its IDF weight is exactly zero), and what is the one-sentence
intuition for *why* that word deserves to be silenced in an industry-similarity measure?

**(b)** [6 pts] **The spurious-similarity demonstration.** Suppose you *forgot* to strip stop-words, so a
boilerplate word — say `company` — survives in both an oil firm's vector and an airline's vector. Concretely,
take the oil firm `oil`×2, `crude`×1, `refine`×1, `fuel`×1, `company`×1 and the airline `flights`×1,
`airline`×1, `tickets`×1, `travel`×1, `company`×2. Their *only* shared word is `company`. Compute their raw
**count** cosine similarity. (You should get a strictly positive number even though they share no product
vocabulary.) Then explain in one or two sentences how giving `company` its IDF weight — which, if `company`
appears in *every* document, is $\log(D/D) = 0$ — repairs this: what does the spurious similarity become?

**(c)** [4 pts] State the general principle in two sentences: TF–IDF up-weights words that are *distinctive*
(rare across firms, like `lithium`) and down-weights words that are *ubiquitous* (common across firms, like
`company`). Connect this to a vulnerability the Chapter 6.2 guide flags — **boilerplate and legal language**
— and say in one clause why down-weighting common words is a partial, not a complete, defense against it.

---

## Problem 3 — Build a TNIC from a similarity matrix (20 points)

Now scale up from a pair to a network. You are given the full pairwise cosine-similarity matrix for **five**
firms (illustrative, symmetric, rounded to two decimals — built the same way as Problem 1, just at larger
scale). The firms are two cloud-software firms (**SoftA**, **SoftB**), a retailer (**RetA**), a bank
(**Bank1**), and a cross-over firm **OmniMart** that sells retail goods *and* runs a cloud platform (an
Amazon-like straddler — the same role OmniMart plays in nb6.2).

> | $\text{sim}(i,k)$ | SoftA | SoftB | OmniMart | RetA | Bank1 |
> |:---|:---:|:---:|:---:|:---:|:---:|
> | **SoftA** | 1.00 | 0.62 | 0.34 | 0.05 | 0.08 |
> | **SoftB** | 0.62 | 1.00 | 0.22 | 0.04 | 0.07 |
> | **OmniMart** | 0.34 | 0.22 | 1.00 | 0.41 | 0.06 |
> | **RetA** | 0.05 | 0.04 | 0.41 | 1.00 | 0.05 |
> | **Bank1** | 0.08 | 0.07 | 0.06 | 0.05 | 1.00 |

The TNIC rule (Ch 6.2 §2, step four): firm $i$'s **text-based industry** is the set of *other* firms whose
similarity to $i$ clears a chosen threshold $\tau$. Use $\tau = 0.20$ throughout this problem.

**(a)** [6 pts] For each of the five firms, list its TNIC industry — the set of other firms with
$\text{sim} \ge 0.20$. (Read off each firm's row; ignore the diagonal $1.00$, a firm is not its own
competitor.) Write out all five neighbor sets.

**(b)** [6 pts] **Firm-specific, not a partition.** Compare SoftA's industry to OmniMart's industry from
part (a). Show they are **different sets** — and note the asymmetry of *membership in a set* vs. *having the
same set*: SoftA appears in OmniMart's industry, yet OmniMart's industry is not identical to SoftA's. Explain
in two sentences why this is impossible under a SIC code (which assigns each firm one box and declares
everyone in that box mutual competitors) and what HP mean by calling TNIC **firm-specific**: each firm
centers its *own* neighborhood.

**(c)** [6 pts] **Intransitivity.** Find a triple of firms $X, Y, Z$ in this matrix such that
$\text{sim}(X,Y) \ge \tau$ and $\text{sim}(Y,Z) \ge \tau$ but $\text{sim}(X,Z) < \tau$ — i.e., $X$ and $Z$
are *both* neighbors of $Y$ but are *not* neighbors of each other. State the triple and the three similarity
values. Then explain in two sentences why this **intransitivity** is exactly the Amazon-style fact SIC cannot
represent (Hint: $Y$ is the cross-over firm; tie it to "neighbor to both Microsoft on cloud and Walmart on
groceries, though those two are not neighbors").

**(d)** [2 pts] **The threshold is a knob.** Recompute OmniMart's neighbor *count* (number of firms in its
industry) at four thresholds: $\tau = 0.10,\ 0.30,\ 0.40,\ 0.50$. State in one sentence what happens to a
firm's competitor count as $\tau$ rises, and why this makes $\tau$ a **lever**, not a fact — a measurement
choice that must be disclosed and defended (Ch 6.2 §3, "knobs are levers").

---

## Problem 4 — TNIC vs. SIC on a cross-over firm (12 points)

This problem makes the horse race personal: take the one firm that breaks the official taxonomy and show how
each system handles it. Use the same five-firm matrix and $\tau = 0.20$ from Problem 3.

OmniMart sells retail goods *and* operates a cloud platform. A government classifier must assign it **one**
four-digit SIC code; suppose — because retail is its larger revenue segment — it lands in a **retail** SIC
box, the same box as RetA. (This mirrors nb6.2, where the SIC-like foil forces each cross-over firm into a
single box and it "loses half its identity.")

**(a)** [4 pts] **What SIC sees.** Under the retail SIC box, who are OmniMart's competitors, and who is
*invisible* to it? State which of {SoftA, SoftB, RetA, Bank1} the SIC box counts as OmniMart's industry, and
which real competitor(s) — visible in the similarity matrix — the box *misses entirely*.

**(b)** [5 pts] **What TNIC sees.** From OmniMart's TNIC industry (Problem 3a), state how many *distinct*
SIC-style businesses OmniMart neighbors — i.e., does its text-based industry span retail *and* software? Name
the neighbors and the business each represents. Then state in one sentence the precise sense in which TNIC
*recovers the half of OmniMart's identity* that the single SIC box threw away.

**(c)** [3 pts] **The horse-race framing.** The Chapter 6.2 guide insists this is a **measurement** paper:
its central claim is validated by a *horse race*, not a causal identifying assumption. State in two sentences
what the horse race is — what outcome would TNIC and SIC compete to explain on the *same* firms in the *same*
years — and why "TNIC neighbors OmniMart with both a software firm and a retailer" is suggestive but **not
yet** the validation (Hint: what would still have to be shown about *outcomes* like co-movement or margins?).

---

## Problem 5 — What's vulnerable: boilerplate, self-description, bag-of-words (16 points)

A measurement paper has measurement vulnerabilities — different from the causal threats of Week 5. The right
skeptical question is not "what confounds the treatment?" but **"what makes the text a noisy or biased signal
of what the firm actually does?"** This problem is pure reasoning; it tests whether you can push on the
measure the way a referee would.

**(a)** [5 pts] **Boilerplate and legal language.** A 10-K is written by lawyers as much as managers; large
stretches are formulaic and shared across firms (risk-factor language, disclaimers, accounting boilerplate).
Explain in two or three sentences how shared boilerplate could make two firms in *different* businesses score
"similar," and name the *two* construction choices from Problems 2 and the working-world setup that limit
this. Then state in one clause why the problem is *worse* for the time-varying comparisons TNIC is built to
make (Hint: disclosure norms — and therefore the boilerplate baseline — drift over time).

**(b)** [5 pts] **Firms' incentives in self-description.** This is the sharpest critique, specific to
*self-reported* text. Firms *choose* how to describe themselves — vaguely to avoid tipping off rivals,
grandly to flatter investors ("we are an AI company now"), conservatively to manage legal exposure. Explain
in two or three sentences the **reflexivity** problem this creates *specifically because differentiation is
itself one of the paper's outcomes*: if a firm that merely *talks* differently is coded as differentiated,
what exactly is the measure measuring? Pose the referee's one-sentence question in the form "are we measuring
___, or ___?"

**(c)** [4 pts] **Bag-of-words ignores meaning.** The representation throws away word order, synonymy, and
context. Give the two canonical failures: (i) a negation example — write two short sentences that mean
*opposite* things about competing in a market but produce nearly *identical* bags-of-words; and (ii) a
synonym example — two words a human reads as the same product that the bag treats as unrelated. Then state in
one sentence which later tool (Ch 6.5) is built precisely to close this gap, and what kind of vector it uses.

**(d)** [2 pts] **Threat → guard, one per vulnerability.** For each of (a), (b), (c), name in a phrase the
discipline or check a careful replicator uses to address it (one per vulnerability). This is spec discipline
(Conventions §4) pointed at a text-based measure: name the threat, then name the guard.

---

## Problem 6 — Replication design: from this problem set to nb6.2 (12 points)

You will run this for real in nb6.2. This problem makes you design the replication *before* you touch the
keyboard — stating the corpus, the pipeline, and the checks you would commit to in advance.

**(a)** [4 pts] **The pipeline, in order.** Name the four steps that turn a folder of product descriptions
into a similarity matrix, in the order nb6.2 runs them (Ch 6.2 §2): (1) get/clean the text, (2) build
vectors, (3) measure similarity, (4) build the network. For step (2), name the *two* vectorizers nb6.2
compares (`CountVectorizer` for plain counts vs. `TfidfVectorizer` for TF–IDF) and state in one sentence what
swapping one for the other lets you *see* about the role of IDF (Hint: Problem 2b).

**(b)** [4 pts] **The headline check.** nb6.2 hands you a 16-firm corpus across three latent industries
(software/cloud, banking/lending, retail/apparel) plus two deliberate cross-over firms. State the **one
quantitative comparison** you would compute to confirm the measure "works" *before* trusting any TNIC
neighbor list (Hint: compare the *average* similarity of firms in the *same* latent industry to the average
across *different* industries — what ordering must hold, and what is the name for that ratio?). Then name the
one *picture* that makes the same point visually (Hint: what lights up on the diagonal of a cluster-ordered
heatmap?).

**(c)** [4 pts] **Two network properties to reproduce, and the real-data pointer.** Name the two network
properties — beyond same-industry blocks — that nb6.2 asks you to demonstrate on the cross-over firm and (if
two years of filings are supplied) on a firm that changed its business; tie each to the matching property of
TNIC (**intransitivity** and **time-variation**). Finally, state where a real replication would get the text
and the ready-made industries instead of re-parsing tens of thousands of filings yourself: name the **source
of the raw text** (the public SEC filing system) and the **public data library** Hoberg and Phillips
maintain so researchers can download the computed TNIC industries directly. [The exact library URL is left as
a verify-before-printing item, consistent with the Ch 6.2 guide.]

---

*End of Problem Set 6.2. Solutions: Appendix E, `E-w6-ps6.2-solutions.md`. The companion notebook **nb6.2**
(`notebooks/week-06/nb6.2-10k-text-similarity.ipynb`) lets you scale every operation here to a 16-firm
corpus — tokenize and TF–IDF-vectorize the product descriptions, compute the full pairwise cosine matrix,
print it as a cluster-ordered heatmap and watch the industry blocks light up on the diagonal, then build a
TNIC at a threshold $\tau$ and verify its firm-specific and intransitive structure on a cross-over firm —
checking your hand arithmetic from Problems 1–4 against `scikit-learn`, with a "Your Turn" extension that
adds a firm, sweeps the threshold, or switches to bigrams. The single discipline to carry forward: this is a
**measurement** paper, so read every cosine as a *choice-dependent estimate* of product overlap — clean
enough to redraw the map of American industry from text alone, but only as good as the words a firm chooses,
the stop-words you strip, and the threshold you pick. Citation by name: Hoberg & Phillips (2016).*
