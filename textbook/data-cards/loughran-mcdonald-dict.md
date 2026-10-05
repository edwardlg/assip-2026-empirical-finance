# Data Card — Loughran–McDonald Master Dictionary (Finance Sentiment Word Lists)

**Provider & what it is.** A set of finance-specific sentiment word lists, maintained by **Bill McDonald** at the University of Notre Dame's Software Repository for Accounting and Finance (SRAF), and built on the research of Loughran and McDonald (2011). The reveal of the underlying paper is the reveal of the whole resource: a *general-English* sentiment dictionary (the Harvard General Inquirer / Harvard-IV-4) systematically *misclassifies* financial text, because words like *liability*, *tax*, *cost*, *depreciation*, *capital*, and *crude* are "negative" in everyday English but neutral, descriptive accounting terms in a 10-K. The Loughran–McDonald (LM) **Master Dictionary** fixes this by hand-tagging words for finance, sorting them into categories — **Negative, Positive, Uncertainty, Litigious, Strong-Modal, Weak-Modal, Constraining** — that are shaped to how finance language actually behaves. The deliverable is the *word lists themselves*: the public infrastructure that lets you turn a filing into a tone score by counting list words, transparently and reproducibly. It is the field-standard dictionary for bag-of-words sentiment in finance.

**Coverage.** A single master CSV listing tens of thousands of unique words (the dictionary's vocabulary), each flagged for which sentiment categories it belongs to, plus auxiliary statistics (document frequency, syllables, a sequence number). It is *not* a panel of observations — it is a fixed lexicon you *apply to* a text corpus (e.g., SEC EDGAR 10-Ks/8-Ks). McDonald periodically revises and re-versions the lists; the master file is dated by year. Pin the version you used.

**Key identifiers.** The unit is the **word** (uppercase token). The columns that matter are the per-category flags — `Negative`, `Positive`, `Uncertainty`, `Litigious`, `Strong_Modal`, `Weak_Modal`, `Constraining` — where a nonzero value typically encodes the year the word was added to that list (so `0` means "not in this list"). There is no firm/date key here; you *join the dictionary to your corpus by matching tokens*, then key the resulting scores by whatever identifies your documents (CIK + filing date for EDGAR).

**Access path.** Free public download from the SRAF site; no key, no account. You read the CSV once and build category word sets in memory:

```python
import pandas as pd

# Public download from the Notre Dame SRAF site (pin the version/year you use).
LM_URL = "https://sraf.nd.edu/loughranmcdonald-master-dictionary/"  # [CHECK] exact CSV file URL/version
lm = pd.read_csv("Loughran-McDonald_MasterDictionary_2023.csv")     # cached local copy

neg_words = set(lm.loc[lm["Negative"] > 0, "Word"].str.upper())
unc_words = set(lm.loc[lm["Uncertainty"] > 0, "Word"].str.upper())

def neg_score(tokens):
    # Bag-of-words: fraction of a document's words that are on the negative list.
    return sum(t.upper() in neg_words for t in tokens) / max(len(tokens), 1)
```

No secrets are involved — there is nothing to put in an environment variable here — but the same reproducibility discipline applies: cache the dictionary file locally and pin its version, because a future LM release will have different words and your scores will move.

**License & note.** The LM lists are made **freely available for research use** by Notre Dame SRAF, with the request that you **cite Loughran & McDonald (2011)** when you use them. Treat them as citeable academic infrastructure: cache and redistribute within the bounds the SRAF site states, attribute properly, and pin the version `[CHECK exact license wording and citation form on the SRAF page]`. Full citation per the TOC: Loughran, T., & McDonald, B. (2011). *When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks.* Journal of Finance, 66(1), 35–65 `[CHECK pages/venue]`.

**Gotchas.**
- **Bag-of-words ignores context.** Counting list words cannot see negation, sarcasm, or conditionals: *"this was not a bad quarter"* fires on `bad` and scores negative. The dictionary is a *transparent* instrument, not an *accurate* one — its virtue is reproducibility, not comprehension (the bridge to embeddings and LLMs, Ch 6.2 / 6.5).
- **Tokenize the same way you built the lists.** The words are uppercase; your scorer must uppercase and tokenize consistently, or matches silently fail. Match the regex you use to score to the one the lists assume.
- **Version drift.** The lists change across releases. Two papers using "the LM dictionary" from different years are not using the same instrument — pin the year.
- **Look-ahead by tuning.** If you *modify* the word list using the very sample you test on, you have snooped (the Week-1 lesson). Build/tune on one split, test out of sample.
- **Denominator and weighting choices.** Raw counts vs. document-length normalization vs. tf–idf weighting all change the score; tf–idf muffles boilerplate but cannot rescue a bad dictionary. State your choice.
- **Sentiment ≠ disclosure style.** A "negative" 10-K may reflect a genuinely bad year *or* a cautious legal writing style — a confound to address, not assume away.

**First 10 rows — schema sketch (illustrative; values invented, real LM columns).**

| Word | Sequence | Negative | Positive | Uncertainty | Litigious | Strong_Modal | Weak_Modal | Constraining |
|---|---|---|---|---|---|---|---|---|
| ABANDON | 1 | 2009 | 0 | 0 | 0 | 0 | 0 | 0 |
| ACHIEVE | 2 | 0 | 2009 | 0 | 0 | 0 | 0 | 0 |
| ADVERSE | 3 | 2009 | 0 | 0 | 0 | 0 | 0 | 0 |
| APPROXIMATELY | 4 | 0 | 0 | 2009 | 0 | 0 | 0 | 0 |
| BENEFICIAL | 5 | 0 | 2009 | 0 | 0 | 0 | 0 | 0 |
| CONTINGENT | 6 | 0 | 0 | 2009 | 0 | 0 | 0 | 0 |
| DEFENDANT | 7 | 0 | 0 | 0 | 2009 | 0 | 0 | 0 |
| LIABILITY | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LITIGATION | 9 | 0 | 0 | 0 | 2009 | 0 | 0 | 0 |
| MUST | 10 | 0 | 0 | 0 | 0 | 2009 | 0 | 0 |

(Note `LIABILITY` is flagged in *no* category — the paper's headline: the accounting word general-English dictionaries wrongly score as negative.)

**Which chapter/lab/capstone uses it.** This is the data behind **Ch 6.3** ("Reader's Guide: Loughran & McDonald 2011") and its notebook **nb6.3** (the Loughran–McDonald sentiment pipeline, ~26–30 cells), Leah's text-as-data thread. nb6.3 loads the real master CSV, builds the category sets, scores a corpus of 10-K/8-K text, and demonstrates the misclassification result — then seeds **PS 6.3**. It returns in **Ch 6.5** as the *transparent cousin* of an LLM label (PS 6.5 §c contrasts the auditable dictionary against the opaque LLM), and underpins any text-sentiment **capstone** (e.g., SEC 8-K tone in the spirit of Capstone 4). Apply it to EDGAR text (see the `sec-edgar` data card); acquire and document both through the **Ch 7.2 / Lab 7** reproducible-pull discipline, pinning the dictionary version.
