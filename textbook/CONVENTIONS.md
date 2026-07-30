# CONVENTIONS — The Constitution

Every agent (human or AI) working on this textbook reads this file first. It locks the decisions
that keep 300,000+ words coherent across many sessions. If you need to deviate, change this file in
the same commit and say why.

---

## 1. Audience & Voice

**Reader:** a mathematically gifted 16–18-year-old (AP Calc BC + AP Stats done, some Python).
Has seen limits/derivatives/integrals, basic probability, mean/variance/correlation, t-tests, and
simple regression as a black box. Has *not* seen matrix algebra beyond basics, MLE, asymptotics,
panel data, causal inference, finance datasets, or LaTeX.

**Reveal-the-trick pedagogy (mandatory structure for any technical idea):**
1. State the result in one plain sentence.
2. Show *why* it works (intuition, then a worked numerical example, then the algebra).
3. Show *when it fails* (the assumption that breaks, and what you see when it does).
4. Show the code (a runnable snippet).

**Style rules.**
- Full paragraphs that walk a smart kid through an argument. Avoid bullet-point soup.
- Define every term the first time it appears, in-line.
- Concrete before abstract: a number before a Greek letter.
- No emojis. No marketing voice. No "in today's fast-paced world" openings.
- Never dumbed-down: a real Wooldridge-level problem, just better motivated.
- Inclusive, 17-year-old-relevant examples: student debt, gig-economy income volatility, climate risk
  in insurance, BNPL, crypto adoption, fair lending. Avoid culturally narrow references.

## 2. Recurring Student Cast

Use these five fictional students across worked examples for continuity. Keep their interests stable
so examples can build on each other. Diverse by design.

| Name  | Interest hook (use to motivate examples) |
|-------|------------------------------------------|
| Maya  | Student debt, household finance, fair lending |
| Devon | Crypto, on-chain data, FinTech |
| Priya | Climate risk, insurance, ESG |
| Sam   | Sports/markets, momentum, trading simulations |
| Leah  | Patents, innovation, text analysis |

## 3. Mathematical Notation

| Symbol | Meaning |
|--------|---------|
| $x$, $\beta$ | scalars (italic) |
| $\mathbf{x}$, $\mathbf{\beta}$ | vectors (bold lowercase) |
| $\mathbf{X}$, $\mathbf{\Sigma}$ | matrices (bold uppercase) |
| $\hat{\beta}$, $\hat{y}$ | estimates / fitted values (hat) |
| $\mathbb{E}[\cdot]$, $\operatorname{Var}(\cdot)$, $\operatorname{Cov}(\cdot,\cdot)$ | expectation, variance, covariance |
| $\varepsilon$, $u$ | error / disturbance terms |
| $N$ | number of observations; $K$ number of regressors |
| $i$ | indexes units (firms, people); $t$ time; $j$ regressors |
| $\beta_0$ | intercept; $\beta_1\dots\beta_K$ slopes |
| $\xrightarrow{p}$, $\xrightarrow{d}$ | convergence in probability / distribution |
| $\sim$ | "is distributed as" |

Write OLS in matrix form as $\mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\varepsilon}$,
$\hat{\boldsymbol{\beta}} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$.
Standard errors always labeled with their flavor: classical, HC1/HC2/HC3, HAC (Newey–West), clustered.

## 4. Empirical-Spec Discipline

Every regression specification stated in the book must name, explicitly:
**outcome · treatment/key regressor · controls · fixed effects · clustering · sample · the
identifying assumption in one sentence.** No hand-wavy "this controls for endogeneity" — name the
threat and the design that addresses it.

## 5. Code & Reproducibility

- Environment: `python=3.11`; `pandas>=2.2`, `numpy`, `scipy`, `statsmodels`, `linearmodels`,
  `pyfixest`, `matplotlib`, `wrds`, `yfinance`, `pandas-datareader`, `requests`, `pyarrow`.
- Every code block must run end-to-end on a fresh conda env.
- No deprecated `pd.append`. No chained indexing without `.copy()`. No `iloc`/`loc` confusion.
- Every notebook that touches licensed data pins its CRSP/Compustat (etc.) snapshot date and notes
  that licensed data stays on GMU infrastructure (read-only on Hopper/WRDS Cloud).
- Secrets via env vars only (e.g., `${AZURE_OPENAI_KEY}`); never hard-coded.
- Each chapter ships a Jupyter notebook with sample output and a "Your Turn" extension.

## 6. Citations

- Every empirical claim cites at least one primary source with full bibliographic info.
- Prof. Gao's papers are cited exactly per his CV (see the anchor list in
  `docs/superpowers/specs/2026-05-26-frontmatter-toc-design.md` §5).
- If a citation can't be verified, tag it `[CHECK]` rather than fabricate.

## 7. File & Naming Conventions

- Prose: GitHub-flavored Markdown with LaTeX math (`$...$`, `$$...$$`).
- Weeks under `book/weeks/week-0N/`; chapters `chNN-slug.md`; problem sets `psNN.md`;
  solutions in `book/appendices/E-solutions-manual/`.
- Notebooks under `notebooks/week-0N/` mirroring chapters.
- Data cards under `data-cards/<source-slug>.md`.
- Agent handoffs logged under `agents/handoffs/`.

## 8. Program Facts (for the Articulation Matrix & Preface — verified)

- **Host:** Prof. Lei Gao, Associate Professor of Finance, Costello College of Business, GMU.
- **Feeds:** ASSIP 2026 (Aspiring Scientists Summer Internship Program) (GMU College of Science).
  Real program: 8 weeks full-time (Mon-Fri 9-5), Jun 22 - Aug 12, 2026; Phase 1 = 8 weeks of full-time research (M-F 9:00 am - 5:00 pm ET);
  Phase 2 = conference presentation (Wed Aug 12, 2026); Phase 3 = 4 weeks paper refinement. Datasets: CRSP,
  Compustat, SEC EDGAR, Bloomberg. AI tools: Claude, ChatGPT. Outputs published in the Journal of
  Student-Scientists' Research (JSSR), GMU Mason Publishing. 3 GMU College of Science credits + \$1,299 tuition (full waivers for Pell-eligible / reduced-lunch students). Directed by Dr. Lei Gao.
