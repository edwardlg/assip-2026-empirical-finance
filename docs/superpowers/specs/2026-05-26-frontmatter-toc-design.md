# Design Spec — NextGen Empirical Finance Research Camp Textbook

**Date:** 2026-05-26
**Author:** Drafting orchestration (PlannerAgent et al.) for Prof. Lei Gao
**Scope of THIS spec:** the project-wide conventions ("the constitution") + the first build slice
(front matter + full annotated table of contents). Later weeks/appendices/capstones each get
their own plan and reference this document.

---

## 1. Problem & Goal

Produce a publication-quality textbook + lab manual + problem-set bank for an 8-week summer
intensive empirical-finance research camp for top U.S. high-school students (USAMO/ISEF/Regeneron
caliber; AP Calc BC + AP Stats complete; some Python). The camp is hosted by Prof. Lei Gao
(Associate Professor of Finance, Costello College of Business, George Mason University) and feeds
GMU Schar's **NextGen FinTech Scholars / Data Science Young Scholars Research Program**.

By Week 8 each student produces an original 12–20 page empirical paper on real public data,
in LaTeX, with a replicable GitHub repo.

Target total length across all artifacts: **300,000–500,000 words**. This is far too large for one
pass, so the work is decomposed into independent slices, each built to completion.

## 2. Why This Is Decomposed (scope decision)

The full deliverable (§8 of the master prompt) is at least: 8 weekly modules + 5 appendices +
5 full capstone papers + an instructor's manual + ~40 notebooks + ~40 problem sets + ~12 reading
guides + ~16 data cards. That is a dozen-plus independent sub-projects. Each gets its own
spec → plan → build cycle. **Build order:**

1. **Front matter + full annotated TOC** *(this slice)* — establishes voice, notation, structure
   that everything else inherits. Lowest-risk anchor.
2. Weeks 1–2 (OLS foundations) — first full vertical slice (prose + problems + notebooks + assessment).
3. Weeks 3–4 (causal inference) → 5–6 (reading the frontier) → 7–8 (research project).
4. Appendices A–E.
5. Capstone gallery (5 papers).
6. Instructor's manual + top-level README.

## 3. Output Mode & Architecture (decided with user)

- **Files, not chat.** All content is written as repo files (`.md`, later `.ipynb`, `.tex`). The repo
  is the source of truth, not conversation scrollback.
- **Four agents as real dispatched subagents:** PlannerAgent → WriterAgent → CoderAgent →
  ReviewerAgent. Handoffs logged to `agents/handoffs/` so orchestration is auditable (mirrors the
  master prompt's `[Agent →]` tags). For the front-matter slice, PlannerAgent owns the TOC,
  WriterAgent drafts prose, ReviewerAgent gives the closing verdict; CoderAgent idles until a week
  with notebooks is built.

### Repo layout

```
8weeks/
├── README.md                      # repo map + how-to-deploy (built in a later slice)
├── CONVENTIONS.md                 # the constitution — every agent reads first
├── book/
│   ├── 00-front-matter/
│   │   ├── 00-preface.md           # drafted for Prof. Gao's approval
│   │   ├── 01-articulation-matrix.md
│   │   ├── 02-how-to-use.md
│   │   └── 03-prerequisite-self-test.md   # 20 Q + full solutions
│   ├── TOC.md                      # PlannerAgent's full annotated table of contents
│   ├── weeks/week-01 … week-08/    # stub dirs now (one-line README each)
│   ├── appendices/A … E/           # stub dirs now
│   ├── capstones/                  # stub dirs now
│   └── instructor-manual/          # stub dir now
├── notebooks/                      # mirrors weeks/ (stub now)
├── data-cards/                     # §4 data cards (stub now)
└── agents/handoffs/                # logged agent handoffs
```

## 4. Conventions (locked; later slices MUST honor)

**Notation.** Bold lowercase = vectors ($\mathbf{x}$); bold uppercase = matrices ($\mathbf{X}$);
hats = estimates ($\hat\beta$); $\mathbb{E}[\cdot]$ expectation; $N$ = observations, $K$ = regressors;
$i$ indexes units, $t$ time, $j$ regressors. Full table lives in `CONVENTIONS.md`.

**Recurring student cast** (continuity + inclusivity per master prompt §9): a small diverse set of
fictional students used across worked examples — **Maya, Devon, Priya, Sam, Leah**. Consistent
personalities/interests so examples build on each other.

**Voice.** Reveal-the-trick pedagogy: (1) state the result in one sentence, (2) show why it works,
(3) show when it fails, (4) show the code. Full paragraphs, not bullet soup. Define every term on
first use. No emojis, no marketing voice, no "in today's fast-paced world."

**Reproducibility pin.** `python=3.11`; `pandas>=2.2`, `numpy`, `statsmodels`, `linearmodels`,
`pyfixest`, `wrds`, `yfinance`, `pandas-datareader`, `requests`, `pyarrow`. No `pd.append`; no chained
indexing without `.copy()`. Every notebook pins its CRSP/Compustat snapshot date.

**Citation policy.** Every empirical claim cites a primary source with full bib. Prof. Gao's own
papers are cited exactly from his CV (see §5). Anything else unverifiable gets a `[CHECK]` tag rather
than fabrication.

**Regression-spec discipline.** Every specification states: outcome, treatment, controls, fixed
effects, clustering, sample, and the identifying assumption in one sentence.

## 5. Anchor papers (exact citations from Prof. Gao's CV)

Used in the Preface, the reading guides (Weeks 5–6), and the mentor sessions (§6 of master prompt):

- **Fair lending / discrimination detection:** Gao, L., & Sun, H. (2019). Lending practices to
  same-sex borrowers. *PNAS*, 116(19), 9293–9302. (Congressional testimony; HUD; Federal Reserve.)
- **Supply-chain common ownership:** Gao, L., Han, J., Kim, J-B., & Pan, T. (2024). Overlapping
  institutional ownership along the supply chain and earnings management of supplier firms.
  *Journal of Corporate Finance*, 84, 102520.
- **Municipal borrowing (working):** Gao, L., Liu, S., & Wang, Y. The Rainbow of Credits: Evidence
  from Municipal Borrowing. (AEA 2025; target *Journal of Finance*).
- **Return predictability:** Gao, L., Han, Y., Li, S., & Zhou, G. (2018). Market Intraday Momentum.
  *Journal of Financial Economics*, 129, 394–414.
- **Natural experiment / crash risk:** Deng, X., Gao, L., & Kim, J-B. (2020). Short-sale Constraints
  and Stock Price Crash Risk: Causal Evidence from a Natural Experiment. *Journal of Corporate
  Finance*, 60, 101498.
- **Disclosure / CEO politics:** Elnahas, A., Gao, L., Hossain, N., & Kim, J-B. (2024). CEO Political
  Orientation and Information Disclosure. *Journal of Financial and Quantitative Analysis*.
- **AI in finance education:** Gao, L., Gopalakrishnan, S., Ehrlich, M., & Wang, C. (forthcoming).
  Derivatives Trading Simulation Supported by AI. *Journal of Financial Education*.
- **CSR / price pressure:** Gao, L., He, J., & Wu, J. (2023). Standing Out from the Crowd via CSR
  Engagement. *Journal of Financial and Quantitative Analysis*.

The POM supply-chain-risk/bank-loan-cost manuscript (ms POM-Nov-25-OA-1924) named in the master
prompt is not in the CV's selected list; it is tagged `[CHECK]` until confirmed.

## 6. What This Slice Produces

1. `CONVENTIONS.md` — the constitution above, expanded with the full notation table.
2. `book/00-front-matter/00-preface.md` — Preface drafted for Prof. Gao's voice/approval, grounded in
   verified CV facts; ~1,200–1,800 words.
3. `book/00-front-matter/01-articulation-matrix.md` — 2-page matrix mapping the 8-week camp against
   the real NextGen program (12 wks, Fri 12–2pm EST, Jun 26–Sep 11 2026; CRSP/Compustat/EDGAR/
   Bloomberg; Claude/ChatGPT; Schar Young Scholars Journal + GMU MARS; awards to $2,000). Shows where
   the camp **deepens** vs. where NextGen **leads**.
4. `book/00-front-matter/02-how-to-use.md` — pedagogy, daily rhythm, how problems/notebooks/labs
   interlock; ~1,500 words.
5. `book/00-front-matter/03-prerequisite-self-test.md` — 20 questions (calculus, probability/stats,
   light Python) + full solutions + a routing table ("missed these? read Appendix A first").
6. `book/TOC.md` — full annotated TOC: 8 weeks × 5 chapters + daily problem sets + per-chapter
   notebooks + appendices + 5 capstones + instructor manual, each with a word-count estimate summing
   toward the 300–500k target.
7. Stub dirs + one-line READMEs for everything not yet built, so the shape is visible.

## 7. Success Criteria

- Front matter reads in Prof. Gao's professional voice and contains zero fabricated facts.
- Articulation Matrix references the actual NextGen program structure and dates.
- TOC is complete (every deliverable in master prompt §3/§8 appears) with credible word-count
  estimates and no `[CHECK]`/TODO placeholders.
- `CONVENTIONS.md` is specific enough that a later slice (or subagent) can match voice, notation,
  cast, and environment without re-deriving them.

## 8. Out of Scope (this slice)

Any week chapter prose, any notebook code, any problem-set content beyond the 20-question
prerequisite self-test, any capstone paper, the instructor's manual, the deploy README.
Those are later slices.

## 9. Open Items

- `[CHECK]` POM ms POM-Nov-25-OA-1924 (supply-chain risk → bank loan cost) — confirm bib.
- Git is not initialized in this directory; committing the spec is deferred until the user wants a repo.
