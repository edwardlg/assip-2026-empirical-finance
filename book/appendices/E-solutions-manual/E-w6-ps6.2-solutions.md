# Solutions — Problem Set 6.2 (10-K Cosine Similarity & TNIC Mini-Build)

Full worked solutions to `book/weeks/week-06/ps6.2.md`, covering Chapter 6.2 (Reader's Guide: Hoberg &
Phillips (2016), "Text-Based Network Industries and Endogenous Product Differentiation"). Notation follows
the Conventions: firm $i$'s product description is a vector $\mathbf{w}_i$ with one entry per dictionary
word $j$; $w_{ij}$ is the weight (count, or TF–IDF weight) of word $j$ in firm $i$; the cosine similarity
between firms $i$ and $k$ is
$$
\text{sim}(i,k) \;=\; \cos\theta \;=\; \frac{\mathbf{w}_i \cdot \mathbf{w}_k}{\lVert\mathbf{w}_i\rVert\,\lVert\mathbf{w}_k\rVert}
\;=\;
\frac{\sum_j w_{ij}\,w_{kj}}{\sqrt{\sum_j w_{ij}^2}\;\sqrt{\sum_j w_{kj}^2}}.
$$
The recurring theme of the key: **this is a *measurement* paper, so every number is a choice-dependent
estimate of product overlap** — the cosine turns prose into geometry (the same cosine as Chapter 1.2's
correlation), TF–IDF decides which words count, and a threshold $\tau$ decides who is a competitor. Read
each number for *what it measures and what choice it depends on*, never as a fact handed down by a code.

**Every number, cosine, IDF weight, similarity matrix, and product description in this set is
illustrative** — invented for clean arithmetic and clear reasoning, *not* a Hoberg–Phillips table value or
a TNIC-library number. All arithmetic below was verified in `python3`. Citation by name: Hoberg & Phillips
(2016).

**The working world (carried across Problems 1–4).** Three tiny product descriptions, already tokenized
and stop-word-stripped, over the nine-word union dictionary
`[airline, barrels, crude, flights, fuel, oil, refine, tickets, travel]`:

| Firm | What it is | Content words (with counts) |
|:---|:---|:---|
| **A** | oil firm | `oil`×2, `crude`×1, `refine`×1, `fuel`×1 |
| **B** | oil firm | `oil`×2, `refine`×1, `fuel`×1, `barrels`×1 |
| **C** | airline | `flights`×1, `airline`×1, `tickets`×1, `travel`×1 |

---

## Problem 1 — Vectorize three descriptions and compute cosine similarity by hand (24 pts)

**(a)** [6 pts] **The three bag-of-words vectors** over the fixed alphabetical dictionary
`[airline, barrels, crude, flights, fuel, oil, refine, tickets, travel]`:

$$
\mathbf{w}_A = (\,0,\ 0,\ 1,\ 0,\ 1,\ 2,\ 1,\ 0,\ 0\,),
$$
$$
\mathbf{w}_B = (\,0,\ 1,\ 0,\ 0,\ 1,\ 2,\ 1,\ 0,\ 0\,),
$$
$$
\mathbf{w}_C = (\,1,\ 0,\ 0,\ 1,\ 0,\ 0,\ 0,\ 1,\ 1\,).
$$
Reading $\mathbf{w}_A$: it has a $1$ in the `crude`, `fuel`, `refine` slots, a $2$ in the `oil` slot, and
zeros everywhere else — exactly the counts in the table. Each firm's prose is now a point in
nine-dimensional "word space."

**(b)** [8 pts] **Cosine between the two oil firms, $\text{sim}(A,B)$.** The two oil vectors overlap on
`oil` (2 and 2), `fuel` (1 and 1), and `refine` (1 and 1); they disagree only on `crude` (A only) and
`barrels` (B only).

*Dot product* (multiply matching slots, sum):
$$
\mathbf{w}_A\cdot\mathbf{w}_B = (2)(2)_{\text{oil}} + (1)(1)_{\text{fuel}} + (1)(1)_{\text{refine}} = 4 + 1 + 1 = 6.
$$
(`crude` contributes $1\times0=0$ and `barrels` $0\times1=0$ — a word only one firm uses adds nothing.)

*Norms* (square the entries, sum, square-root):
$$
\lVert\mathbf{w}_A\rVert = \sqrt{2^2 + 1^2 + 1^2 + 1^2} = \sqrt{4+1+1+1} = \sqrt{7},
$$
$$
\lVert\mathbf{w}_B\rVert = \sqrt{2^2 + 1^2 + 1^2 + 1^2} = \sqrt{4+1+1+1} = \sqrt{7}.
$$
(Both have squared length $7$ — same four nonzero counts $\{2,1,1,1\}$.)

*Assemble the cosine:*
$$
\boxed{\text{sim}(A,B) = \frac{6}{\sqrt{7}\,\sqrt{7}} = \frac{6}{7} \approx 0.857.}
$$
Two firms emphasizing the *same* words (`oil`, `fuel`, `refine`) score near $1$: the small gap from $1$ is
the single word each uses that the other does not (`crude` vs. `barrels`). In words: A and B share most of
their product vocabulary, so the angle between their word vectors is small and the cosine is high — the
machine has just announced "these two are in the same business."

**(c)** [4 pts] **Oil firm vs. airline.** A and C share *no* dictionary words: A uses
$\{$`oil, crude, refine, fuel`$\}$, C uses $\{$`flights, airline, tickets, travel`$\}$, and these sets are
disjoint, so every product $w_{Aj}w_{Cj}$ is $0$ and the dot product is $0$. Hence
$$
\text{sim}(A,C) = \frac{0}{\sqrt{7}\cdot 2} = 0, \qquad \text{sim}(B,C) = \frac{0}{\sqrt{7}\cdot 2} = 0
$$
(using $\lVert\mathbf{w}_C\rVert = \sqrt{1^2+1^2+1^2+1^2} = \sqrt{4} = 2$). A cosine of exactly $0$ means
the two vectors are **orthogonal** — the angle $\theta = 90°$ — because they have **no shared vocabulary**.
The geometry is literal: zero overlap in words is zero overlap in direction.

**(d)** [4 pts] **What the $3\times3$ matrix demonstrates.** From three product descriptions and nothing
else — no SIC code, no human label, no "this is an oil company" tag — the cosine alone placed the two oil
firms near each other ($0.857$) and each oil firm far from the airline ($0$). This is the central idea of
Hoberg and Phillips (2016) in miniature: an **industry can be discovered from the words a firm uses to
describe itself**, treating text as data in the same hard sense a stock price is data, rather than read off
a government code assigned decades ago. The blocks emerged because firms in the same business *talk* alike;
the measure simply listened.

**(e)** [2 pts] **The Chapter 1.2 connection.** *Same:* the formula is identical — the cosine of the angle
between two vectors, $\langle\mathbf{x},\mathbf{y}\rangle / (\lVert\mathbf{x}\rVert\lVert\mathbf{y}\rVert)$;
in Ch 1.2 the vectors held (mean-centered) returns and the cosine *was* the correlation, here they hold
word counts. *Different:* the word-count vectors are **not mean-centered** (counts are nonnegative, so they
live in the positive orthant and similarities run $0$ to $1$, never negative), whereas the Ch 1.2 vectors
were centered, letting correlation run $-1$ to $1$. Same trick, different vectors — which is exactly why
Ch 6.5's learned embeddings, also compared by cosine, are "the grown-up cousin" of this bag-of-words vector.

---

## Problem 2 — TF–IDF: why down-weight common words (16 pts)

**(a)** [6 pts] **IDF weights** with $D = 4$ and $\text{idf}_j = \log(D/d_j)$ (natural log):

| Word | $d_j$ | $\text{idf}_j = \log(4/d_j)$ |
|:---|:---:|:---|
| `company` | 4 | $\log(4/4) = \log 1 = \mathbf{0}$ |
| `products` | 3 | $\log(4/3) \approx 0.288$ |
| `oil` | 2 | $\log(4/2) = \log 2 \approx 0.693$ |
| `lithium` | 1 | $\log(4/1) = \log 4 \approx 1.386$ |

The **completely silenced** word is `company`: it appears in *all four* firms, so $d_j = D$ and
$\text{idf} = \log 1 = 0$, which zeros out its TF–IDF entry no matter how many times a firm says it.
**Intuition:** a word every firm uses cannot help tell firms *apart* — it carries no information about
*which* industry a firm is in — so an industry-similarity measure should give it zero weight. Notice the
weights climb monotonically as the word gets rarer ($0 \to 0.288 \to 0.693 \to 1.386$): `lithium`, in one
firm out of four, is the most distinctive and gets the largest weight.

**(b)** [6 pts] **The spurious-similarity demonstration.** The oil firm vector
(`oil`×2, `crude`×1, `refine`×1, `fuel`×1, `company`×1) and the airline vector
(`flights`×1, `airline`×1, `tickets`×1, `travel`×1, `company`×2) share *only* the boilerplate word
`company`. The raw **count** cosine:
$$
\text{dot} = (1)(2)_{\text{company}} = 2 \quad(\text{the only matching slot}),
$$
$$
\lVert\text{oil}\rVert = \sqrt{2^2+1^2+1^2+1^2+1^2} = \sqrt{8}, \qquad
\lVert\text{air}\rVert = \sqrt{1^2+1^2+1^2+1^2+2^2} = \sqrt{8},
$$
$$
\boxed{\text{sim}_{\text{count}} = \frac{2}{\sqrt{8}\,\sqrt{8}} = \frac{2}{8} = 0.25.}
$$
An oil firm and an airline — which share *no product vocabulary at all* — now score a strictly positive
$0.25$, purely because both said the empty word `company`. **The IDF repair:** since `company` appears in
*every* document, its weight is $\text{idf} = \log(D/D) = \log 1 = 0$. The only shared slot is multiplied
by zero, so the TF–IDF dot product is $0$ and the spurious similarity **collapses back to $0$** — the
honest answer for two firms in unrelated businesses. This is precisely why nb6.2 contrasts
`CountVectorizer` against `TfidfVectorizer`: plain counts let common words pull *everyone* toward fake
similarity; IDF strips that pull out.

**(c)** [4 pts] **The general principle.** TF–IDF multiplies each word's within-firm count (TF) by a factor
(IDF) that *grows when the word appears in fewer firms*, so it **up-weights distinctive words** (rare across
firms, like `lithium`, $\text{idf} \approx 1.386$) and **down-weights ubiquitous words** (common across
firms, like `company`, $\text{idf} = 0$). This is a partial defense against the Chapter 6.2
**boilerplate-and-legal-language** vulnerability: formulaic disclaimer and accounting language is shared
across many firms, so IDF naturally shrinks its weight. But it is only *partial* — boilerplate that is
common but *not in literally every* filing keeps a nonzero IDF weight and still leaks some shared-legalese
"similarity" into the vectors, and restricting to Item 1 (the product section) rather than the whole 10-K
is the complementary guard. Down-weighting helps; it does not erase the problem.

---

## Problem 3 — Build a TNIC from a similarity matrix (20 pts)

The five-firm matrix (illustrative, symmetric), with $\tau = 0.20$:

| | SoftA | SoftB | OmniMart | RetA | Bank1 |
|:---|:---:|:---:|:---:|:---:|:---:|
| **SoftA** | 1.00 | 0.62 | 0.34 | 0.05 | 0.08 |
| **SoftB** | 0.62 | 1.00 | 0.22 | 0.04 | 0.07 |
| **OmniMart** | 0.34 | 0.22 | 1.00 | 0.41 | 0.06 |
| **RetA** | 0.05 | 0.04 | 0.41 | 1.00 | 0.05 |
| **Bank1** | 0.08 | 0.07 | 0.06 | 0.05 | 1.00 |

**(a)** [6 pts] **Each firm's TNIC industry** = the other firms in its row with $\text{sim} \ge 0.20$
(skip the diagonal):

| Firm | Row entries $\ge 0.20$ | **TNIC industry** |
|:---|:---|:---|
| **SoftA** | SoftB $0.62$, OmniMart $0.34$ | $\{\text{SoftB, OmniMart}\}$ |
| **SoftB** | SoftA $0.62$, OmniMart $0.22$ | $\{\text{SoftA, OmniMart}\}$ |
| **OmniMart** | SoftA $0.34$, SoftB $0.22$, RetA $0.41$ | $\{\text{SoftA, SoftB, RetA}\}$ |
| **RetA** | OmniMart $0.41$ | $\{\text{OmniMart}\}$ |
| **Bank1** | (none $\ge 0.20$) | $\varnothing$ |

Bank1 is a *singleton*: at this threshold its text matches no one — a lone firm in its own neighborhood,
which TNIC permits and SIC (which always co-files it with other "banks") cannot.

**(b)** [6 pts] **Firm-specific, not a partition.** Compare:
$$
\text{TNIC}(\text{SoftA}) = \{\text{SoftB, OmniMart}\}, \qquad
\text{TNIC}(\text{OmniMart}) = \{\text{SoftA, SoftB, RetA}\}.
$$
These are **different sets**. Note the asymmetry the problem flags: SoftA *is a member of* OmniMart's
industry (OmniMart lists SoftA), yet OmniMart's industry is *not the same set as* SoftA's — OmniMart
neighbors RetA, but SoftA does not. Under a **SIC code** this is impossible: SIC assigns each firm one box
and declares everyone sharing that box mutual competitors, so industry membership is an equivalence
relation — if SoftA and OmniMart are in the same box, they have *identical* competitor sets (everyone else
in the box), full stop. TNIC breaks that because it is built from *pairwise* similarity, not a partition:
**each firm centers its own neighborhood**, and two firms can have overlapping-but-distinct neighborhoods.
That is what Hoberg and Phillips mean by **firm-specific** — there is no global map of disjoint industries,
only one personalized list of rivals per firm.

**(c)** [6 pts] **Intransitivity.** Take the triple $X = \text{SoftA}$, $Y = \text{OmniMart}$,
$Z = \text{RetA}$:
$$
\text{sim}(\text{SoftA},\text{OmniMart}) = 0.34 \ge \tau, \qquad
\text{sim}(\text{OmniMart},\text{RetA}) = 0.41 \ge \tau, \qquad
\text{sim}(\text{SoftA},\text{RetA}) = 0.05 < \tau.
$$
So SoftA and RetA are **both** neighbors of OmniMart, but are **not** neighbors of each other. This is
**intransitivity**: "neighbor of" does not chain. It is exactly the Amazon-style fact SIC cannot represent
— OmniMart, the cross-over firm $Y$, straddles two businesses (cloud, where it is close to the software
firm SoftA, and retail, where it is close to RetA), and is therefore a neighbor to both, even though
SoftA (pure software) and RetA (pure retail) describe themselves so differently they are strangers to each
other. SIC must put OmniMart in *one* box and would force a false transitivity (everyone in OmniMart's box
declared mutual competitors); TNIC is built from overlapping pairwise links precisely so it *can* hold "A
near B and B near C but A far from C," which is what real competition looks like.

**(d)** [2 pts] **The threshold is a knob.** OmniMart's neighbor *count* as $\tau$ rises:

| $\tau$ | OmniMart's neighbors ($\ge\tau$) | count |
|:---:|:---|:---:|
| $0.10$ | SoftA, SoftB, RetA | **3** |
| $0.20$ | SoftA, SoftB, RetA | 3 |
| $0.30$ | SoftA, RetA | **2** |
| $0.40$ | RetA | **1** |
| $0.50$ | (none) | **0** |

As $\tau$ rises, a firm's competitor count can only **shrink** (more firms fall below the bar): OmniMart
balloons to 3 rivals at a loose $\tau=0.10$ and collapses to $0$ at a strict $\tau=0.50$. This makes $\tau$
a **lever, not a fact** — the very *number* of competitors a firm has is something the researcher chooses by
setting the threshold, so it must be disclosed and defended (and its sensitivity checked, as nb6.2's
$\tau$-sweep does), exactly the Ch 6.2 §3 lesson that "knobs are levers."

---

## Problem 4 — TNIC vs. SIC on a cross-over firm (12 pts)

**(a)** [4 pts] **What SIC sees.** Forced into a single **retail** SIC box (its larger segment), OmniMart's
SIC "industry" is just **RetA** — the only other retailer. Everyone outside the retail box is declared a
non-competitor. So the SIC box **misses OmniMart's software/cloud rivals entirely**: SoftA ($\text{sim} =
0.34$) and SoftB ($\text{sim} = 0.22$), both *above* the TNIC threshold and visibly close in the matrix,
are invisible to the box. (Bank1, genuinely unrelated at $0.06$, is correctly excluded by both systems.)
The single box captured the retail half of OmniMart and threw the cloud half away.

**(b)** [5 pts] **What TNIC sees.** OmniMart's TNIC industry from Problem 3(a) is
$\{\text{SoftA, SoftB, RetA}\}$ — neighbors spanning **two** distinct SIC-style businesses:
- **SoftA, SoftB** → the *software/cloud* business (OmniMart's cloud-platform side);
- **RetA** → the *retail* business (OmniMart's store side).

So TNIC places OmniMart in a neighborhood that crosses retail *and* software, whereas SIC saw only retail.
This is the precise sense in which TNIC **recovers the half of OmniMart's identity the single box threw
away**: because TNIC lets a firm belong to overlapping neighborhoods rather than one exclusive box, it can
register that OmniMart competes on cloud (with SoftA/SoftB) *and* on retail (with RetA) at once — the
firm-specific, overlapping structure SIC's one-box-per-firm rule structurally forbids.

**(c)** [3 pts] **The horse-race framing.** The horse race is the paper's **validation**: TNIC and SIC are
each entered — ideally in the *same* regression, on the *same* firms in the *same* years — to explain an
**outcome that competition ought to move**, such as cross-firm co-movement in returns or sales growth, or
differences in profit margins. The measure that explains more of that outcome wins; HP's headline is that
TNIC stays strong (often dominant) even with a SIC-based measure included. The OmniMart result here is
**suggestive but not yet the validation**: showing TNIC neighbors OmniMart with a software firm *and* a
retailer demonstrates the measure has the *right shape* (firm-specific, overlapping) — but it does not yet
show those text-based neighbors **co-move in returns or margins better** than the SIC box's neighbors do.
A measurement paper is judged by fit on outcomes, not by anecdote; the cross-over example earns its keep
only once the horse race confirms the text-based neighborhood predicts real economic co-movement that the
official code misses.

---

## Problem 5 — What's vulnerable: boilerplate, self-description, bag-of-words (16 pts)

**(a)** [5 pts] **Boilerplate and legal language.** A 10-K is drafted by lawyers as much as managers, so
large stretches are formulaic and shared across firms — risk-factor disclaimers, accounting and
governance boilerplate. If that language leaks into the vectors, two firms in *different* businesses can
share many words (the law firm's templates) and so score "similar" for reasons that have nothing to do
with products. The two construction choices that limit this are: **(i)** restricting the text to **Item 1,
the product description**, rather than vectorizing the whole filing (keeps most legal boilerplate out), and
**(ii) TF–IDF / stop-word removal**, which down-weights or drops ubiquitous words (Problem 2). The problem
is *worse for TNIC's time-varying comparisons* because **disclosure norms drift over time** — the
boilerplate baseline in 1997 differs from 2015 — so two filings can look more or less "similar" across
years partly because the shared legalese changed, contaminating the very year-to-year movement TNIC is
built to detect.

**(b)** [5 pts] **Firms' incentives in self-description.** Because firms *choose* their own words — vaguely
to avoid tipping off rivals, grandly to flatter investors, conservatively to manage legal exposure — the
text is a *self-report*, not an audit of what the firm actually makes. The **reflexivity** problem is
sharp *because differentiation is itself one of the paper's outcomes*: the measure codes a firm as
"differentiated" when its product description moves *away* from rivals' words, but a firm can move its
*words* (rebrand as "an AI company," adopt fresh jargon) without changing its actual products. If talking
different gets scored as *being* different, the measure may be tracking marketing prose rather than
economic reality — and worse, that gap can correlate with the very outcomes (margins, valuations) the paper
studies, biasing the result. The referee's question:
**"Are we measuring product differentiation, or differentiation in marketing language?"**

**(c)** [4 pts] **Bag-of-words ignores meaning.**
- **(i) Negation.** "We compete in semiconductors" and "We do not compete in semiconductors" mean
  *opposite* things, yet their bags-of-words differ by a single token (`not`) and are nearly identical — so
  the cosine reads them as almost the same firm. (Worse, `not` is often a stripped stop-word, erasing the
  one difference entirely.)
- **(ii) Synonyms.** "We manufacture automobiles" and "We build cars" describe the *same* product, but
  `automobile`/`car` and `manufacture`/`build` are distinct tokens, so the bag treats the two firms as
  unrelated where they share no surface words.

The later tool built precisely to close this gap is **Ch 6.5's embeddings** (learned language-model
vectors): instead of one slot per literal word, an embedding represents text as a dense vector where words
with similar *meaning* sit near each other, so `car` and `automobile` get nearby vectors and negation can
shift the representation — capturing meaning, not word identity. This is why Ch 6.2 sits one chapter before
the AI module: bag-of-words is the *ceiling* embeddings are built to push past.

**(d)** [2 pts] **Threat → guard:**
1. *Boilerplate / legal language* → **restrict to Item 1 and apply TF–IDF / stop-word and proper-noun
   filtering** so ubiquitous and templated words are down-weighted or dropped.
2. *Self-description incentives* → **validate against an external, non-self-reported outcome** (return
   co-movement, margins) — i.e., insist on the horse race rather than trusting the words at face value;
   and probe whether the "similarity" predicts real economic behavior.
3. *Bag-of-words ignores meaning* → **move to embedding vectors (Ch 6.5)** that capture synonymy and
   negation, and check which neighborhoods change when meaning is understood.

---

## Problem 6 — Replication design: from this problem set to nb6.2 (12 pts)

**(a)** [4 pts] **The pipeline, in order** (Ch 6.2 §2):
1. **Get and clean the text** — pull Item 1 (the product description), lowercase, tokenize, drop stop-words.
2. **Build vectors** — turn each cleaned description into a numeric vector over the union dictionary.
3. **Measure similarity** — compute the cosine for every pair, giving the full similarity matrix.
4. **Build the network** — apply a threshold $\tau$ to turn the continuous matrix into each firm's TNIC
   industry.

For step (2), nb6.2 compares **`CountVectorizer`** (plain bag-of-words counts) against **`TfidfVectorizer`**
(TF–IDF weighting). Swapping one for the other lets you *see* the role of IDF directly: under plain counts,
ubiquitous words like `company`/`products` inflate everyone's pairwise similarity (the spurious $0.25$ of
Problem 2b), while TF–IDF down-weights them and the cross-industry similarities fall back toward zero —
making the industry blocks separate more cleanly.

**(b)** [4 pts] **The headline check.** Before trusting any single TNIC neighbor list, compute the **average
within-industry similarity vs. the average cross-industry similarity**: the mean cosine among firms in the
*same* latent industry (e.g., software firm vs. software firm) must come out **substantially higher** than
the mean cosine among firms in *different* latent industries. The summary statistic is their **separation
ratio** (within-average ÷ cross-average); a ratio comfortably above $1$ — ideally several-fold — certifies
the measure is recovering real industry structure and not noise. (nb6.2 reports exactly this, asserting the
ratio rather than the raw difference, since plain counts inflate all magnitudes.) The matching **picture** is
a **cluster-ordered heatmap** of the similarity matrix: when it works, **bright blocks light up on the
diagonal** — one per latent industry — with dark off-diagonal regions between them.

**(c)** [4 pts] **Two network properties and the real-data pointer.** Beyond same-industry blocks, nb6.2
asks you to reproduce:
1. **Intransitivity** — on the cross-over firm, show it neighbors firms in *two* blocks that are *not*
   neighbors of each other ($\text{sim}(A,B)$ and $\text{sim}(B,C)$ high, $\text{sim}(A,C)$ low — Problem 3c).
   This is TNIC's **firm-specific, overlapping** structure.
2. **Time-variation** — if two years of filings are supplied for a firm that changed its business, recompute
   its neighborhood each year and show it *moved*. This is TNIC being **recomputed yearly** so neighborhoods
   drift, the property a frozen SIC code cannot have.

For a real replication, the **raw text** comes from **SEC EDGAR**, the public electronic-filing system that
hosts every U.S. firm's 10-K (Item 1 parsed out of each filing). And rather than re-parse tens of thousands
of filings, you would download the ready-made computed industries from the **public data library Hoberg and
Phillips maintain** (commonly cited as the Hoberg–Phillips Data Library) — the infrastructure that lets
hundreds of later papers use TNIC industries without re-deriving them, the way researchers use Fama–French
factors without re-sorting portfolios. *[The exact library URL is a verify-before-printing item, consistent
with the Ch 6.2 guide's open [CHECK]; do not print a URL from memory.]*

---

*End of solutions for Problem Set 6.2. The arithmetic spine, verified in `python3`: from the three-firm
corpus, the two oil firms score $\text{sim}(A,B) = 6/(\sqrt{7}\sqrt{7}) = 6/7 \approx 0.857$ while each oil
firm and the airline score exactly $0$ (orthogonal, no shared words) — an industry discovered from text with
no labels supplied (Problem 1); the boilerplate word `company` inflates an oil-vs-airline count cosine to
$2/8 = 0.25$, which IDF $= \log(4/4) = 0$ collapses back to $0$ (Problem 2); the five-firm matrix at
$\tau = 0.20$ yields firm-specific neighborhoods ($\text{TNIC}(\text{SoftA}) = \{\text{SoftB, OmniMart}\}
\neq \{\text{SoftA, SoftB, RetA}\} = \text{TNIC}(\text{OmniMart})$) and the intransitive triple
SoftA–OmniMart–RetA with similarities $0.34,\ 0.41,\ 0.05$ (Problems 3–4). The conceptual spine: this is a
**measurement** paper — the cosine turns prose into the Chapter 1.2 geometry, TF–IDF decides which words
count, the threshold $\tau$ decides who is a competitor, and the measure earns its keep only by winning a
horse race against SIC on outcomes competition ought to move — built from a signal (self-reported,
vocabulary-based, parser-dependent text) whose limits the embeddings of Ch 6.5 are built to push against.
Citation by name: Hoberg & Phillips (2016).*
