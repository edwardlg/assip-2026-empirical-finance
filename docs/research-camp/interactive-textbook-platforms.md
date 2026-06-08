# Interactive Online Textbook Platforms — A 2026 Comparison for the 8-Week Empirical-Finance Camp

**Author:** Research analyst (commissioned by Prof. Lei Gao, GMU)
**Date:** 2026-05-30
**Scope:** Pick the publishing platform best fitted to `/mnt/e/ccli/8weeks` — ~670k words across 189 Markdown chapter/lab/problem files, 40 executable Jupyter notebooks, 34 data cards, math-heavy probability/stats/regression chapters using `$…$` / `$$…$$`, five LaTeX appendices, and an AI-co-pilot module sprinkled with fenced Python code.

The book today is *plain Markdown + .ipynb*, with no platform config files (no `_quarto.yml`, no `_config.yml`, no `mkdocs.yml`, no `myst.yml`). That means every option below is a green-field decision — but it also means the cost of choosing badly is mostly *retro-fitting front-matter and link syntax*, not rewriting prose.

---

## 1. One-sentence summaries

- **Jupyter Book 2** — Full rewrite of Jupyter Book on top of the [MyST Document Engine](https://mystmd.org/guide); JS/TypeScript build pipeline (formerly Sphinx); reached `2.1.1` in Jan 2026 and now powers The Turing Way, NumPy tutorials, QuantEcon, Project Pythia, QIIME 2 ([2i2c release post](https://2i2c.org/blog/jupyter-book-release-jan-2026/), [Turing Way blog](https://blog.jupyterbook.org/posts/2025-02-27-the-turing-way-upgrades-to-jb2/), [NumPy migration](https://blog.jupyterbook.org/posts/2025-11-13-numpy-tutorials-jb2/)).
- **Quarto** — Posit's polyglot scientific publishing system; renders `.qmd`, `.md`, and `.ipynb` *directly* with a single CLI, builds HTML books, PDFs, Word, EPUB, and slides from the same source ([Quarto books](https://quarto.org/docs/books/), [Quarto ipynb reference](https://quarto.org/docs/reference/formats/ipynb.html)).
- **MyST Markdown / MyST-Sphinx** — Two products under one name: the *new* Node-based `mystmd` CLI (same engine Jupyter Book 2 wraps), and the *old* `myst-parser` Sphinx extension that still backs Jupyter Book 1 ([MyST guide](https://mystmd.org/guide), [myst-parser docs](https://myst-parser.readthedocs.io/en/latest/syntax/cross-referencing.html)).
- **MkDocs Material** — Documentation-site theme on top of MkDocs (Python), with first-class search, dark mode, and a community `mkdocs-jupyter` plugin for embedding notebooks ([Material](https://squidfunk.github.io/mkdocs-material/), [mkdocs-jupyter](https://github.com/danielfrg/mkdocs-jupyter)).
- **Docusaurus** — React/MDX site generator from Meta; great for product docs and blogs, but math and notebooks are bolt-ons via remark-math/rehype-katex + custom MDX loaders ([Docusaurus math](https://docusaurus.io/docs/markdown-features/math-equations)).
- **GitBook** — Hosted, paid SaaS focused on team product documentation; not a notebook-first or math-first platform.
- **Bookdown** — R-Markdown-centric book engine from Yihui Xie; battle-tested for stats/econ books in R; Python support is via `reticulate` and feels second-class ([bookdown.org](https://bookdown.org/home/tags/forecasting/)).
- **mdBook** — Rust-based, lightweight book builder used by *The Rust Programming Language*; KaTeX/MathJax via preprocessors but no native Jupyter integration ([mdBook MathJax](https://rust-lang.github.io/mdBook/format/mathjax.html), [mdbook-katex](https://github.com/lzanini/mdbook-katex)).

---

## 2. Feature matrix

Legend: ✅ first-class · 🟡 works via plugin/config · ❌ unsupported or impractical · n/a not applicable.

| Capability                                                  | Jupyter Book 2 | Quarto | MyST (`mystmd`) | MyST-Sphinx (JB1) | MkDocs Material | Docusaurus | GitBook | Bookdown | mdBook |
|---|---|---|---|---|---|---|---|---|---|
| Renders `.ipynb` directly (no rewrite)                      | ✅ | ✅ | ✅ | ✅ | 🟡 `mkdocs-jupyter` | 🟡 (custom loader) | ❌ | 🟡 via reticulate | ❌ |
| Executes notebook cells at build time                       | ✅ | ✅ (`--execute`, freeze, cache) | ✅ | ✅ (`jupyter-execute`) | 🟡 `execute: true` flag | ❌ | ❌ | ✅ (knitr) | ❌ |
| LaTeX math (`$…$`, `$$…$$`) without source rewrite          | ✅ | ✅ | ✅ | ✅ | 🟡 (extension) | 🟡 (remark-math + KaTeX) | 🟡 | ✅ | 🟡 |
| Numbered equations + `{eq}` / `\eqref` cross-refs            | ✅ | ✅ | ✅ | ✅ | ❌ | 🟡 | ❌ | ✅ | ❌ |
| Cross-references across chapters by label                   | ✅ | ✅ | ✅ | ✅ | 🟡 (autorefs) | 🟡 | 🟡 | ✅ | ❌ |
| Citations from BibTeX / CSL                                 | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |
| Full-text search out of the box                             | ✅ (client-side) | ✅ | ✅ | ✅ | ✅ (best-in-class) | ✅ | ✅ | 🟡 | ✅ |
| Dark mode                                                   | ✅ | ✅ | ✅ | 🟡 (theme) | ✅ | ✅ | ✅ | 🟡 | 🟡 |
| GitHub Pages deploy (single Action)                         | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | n/a (hosted) | ✅ | ✅ |
| Multi-format output (PDF/EPUB/Word from same source)        | 🟡 (PDF improving) | ✅ (50+ formats) | 🟡 | ✅ (mature LaTeX) | ❌ (HTML only) | ❌ | ❌ | ✅ | 🟡 |
| Interactive widgets (ipywidgets, Plotly, Observable, Thebe) | ✅ | ✅ | ✅ | ✅ | 🟡 | 🟡 | ❌ | 🟡 | ❌ |
| Plugin ecosystem maturity                                   | 🟡 (younger, growing) | ✅ | 🟡 | ✅ (Sphinx ext.) | ✅ (huge) | ✅ (huge) | n/a | 🟡 | 🟡 |
| Active maintenance signal (2025–26)                         | ✅ very active | ✅ very active | ✅ very active | 🟡 (JB1 in maintenance) | ✅ very active | ✅ very active | ✅ (commercial) | 🟡 | 🟡 |
| Single binary / fewest moving parts                         | 🟡 (Python + Node) | ✅ (single CLI) | ✅ (single Node CLI) | ❌ (Sphinx stack) | 🟡 (Python) | 🟡 (Node) | n/a | 🟡 (R+pandoc+LaTeX) | ✅ (Rust binary) |
| Realistic build time at our size (~190 md + 40 nb)          | minutes (incremental) | minutes (cached freeze) | minutes | 5–15 min (cold Sphinx) | < 1 min | < 1 min (no exec) | n/a | minutes | seconds |
| Keep current `.md` + `.ipynb` tree unchanged                | mostly ✅ (add `myst.yml`, light front-matter) | mostly ✅ (add `_quarto.yml`, light front-matter) | mostly ✅ | ✅ (with directives) | 🟡 (front-matter, mkdocs.yml, plugin) | ❌ (rename to `.mdx`, fix syntax) | ❌ (import) | ❌ (rewrite as `.Rmd`) | 🟡 (SUMMARY.md) |

Sources for the cells above: [Jupyter Book 2 / MyST features](https://mystmd.org/guide), [Quarto books](https://quarto.org/docs/books/), [Quarto ipynb](https://quarto.org/docs/reference/formats/ipynb.html), [Quarto bibliography options](https://quarto.org/docs/authoring/citations.html), [Material search](https://squidfunk.github.io/mkdocs-material/), [mkdocs-jupyter README](https://github.com/danielfrg/mkdocs-jupyter), [Docusaurus math](https://docusaurus.io/docs/markdown-features/math-equations), [mdBook math](https://rust-lang.github.io/mdBook/format/mathjax.html), [Pangeo discussion: when to use which](https://discourse.pangeo.io/t/when-to-use-quarto-v-jupyterbook/3136), [JB vs Quarto migration write-ups (2025)](https://blog.ouseful.info/2025/01/20/migrating-to-quarto/).

---

## 3. Real comparable books actually using each platform (2025–26)

- **Jupyter Book 2 / MyST.** [The Turing Way](https://book.the-turing-way.org/) migrated in Feb 2025 ([blog](https://blog.jupyterbook.org/posts/2025-02-27-the-turing-way-upgrades-to-jb2/)); [NumPy Tutorials](https://numpy.org/numpy-tutorials/) cut over in Nov 2025 ([blog](https://blog.jupyterbook.org/posts/2025-11-13-numpy-tutorials-jb2/)); [QuantEcon "Intermediate Quantitative Economics with Python"](https://python.quantecon.org/intro.html) and ["A First Course"](https://intro.quantecon.org/) are MyST-source and built with the JB toolchain; Project Pythia and QIIME 2 docs run on JB2 ([SciPy 2025 proceedings](https://proceedings.scipy.org/articles/hwcj9957)).
- **Quarto.** A growing wave of CRC/Chapman & Hall stats and ML books are now Quarto-native (template at [bgreenwell/quarto-crc](https://github.com/bgreenwell/quarto-crc)); the [Quarto gallery](https://quarto.org/docs/gallery/) lists data-science books, Tufte-style books, and finance/economics texts. Posit's own tutorials and many R-package "vignettes-as-books" have moved off bookdown to Quarto.
- **MyST-Sphinx (Jupyter Book 1).** Still alive in the wild: thousands of legacy books in the [JB1 gallery](https://jupyterbook.org/stable/gallery/) and the 14,000+ instances cited by the executable-books project. New books shouldn't start here.
- **MkDocs Material.** Used by FastAPI, Pydantic, Material itself, and a long tail of Python-library docs; very common for *documentation*, far less common for *textbooks with math*. The reference math+notebook example is Christina Hedges' [astronomy workflow site](https://christinahedges.github.io/astronomy_workflow/).
- **Docusaurus.** React Native, Babel, Jest, Algolia — i.e., software product docs. No flagship math/notebook textbook uses it.
- **GitBook.** Corporate handbooks and product manuals; no major open textbook.
- **Bookdown.** Rob Hyndman & George Athanasopoulos, [*Forecasting: Principles and Practice* (fpp3)](https://otexts.com/fpp3/), last updated 3 May 2026 — the textbook of record for bookdown's reach. Scott Cunningham's [*Causal Inference: The Mixtape*](https://mixtape.scunning.com/) is also bookdown-built. Hyndman's new Python version, [fpppy](https://otexts.com/fpppy/), keeps the OTexts/bookdown stack.
- **mdBook.** *The Rust Programming Language*, Rust by Example, Cargo Book — software documentation, no math-heavy textbooks of note.

Notable counter-example: Jake VanderPlas's [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/) is just raw Jupyter notebooks rendered to GitHub Pages — no platform per se. That is *roughly* the state our repo is in today, and is the lowest-effort baseline we are comparing each platform against.

---

## 4. Migration cost from our current Markdown + `.ipynb` tree

Our tree has 189 `.md` files using Pandoc-style `$…$` math and standard fenced code blocks, plus 40 `.ipynb` files with the same math conventions, plus 34 data-card `.md` files. No bibliography is in use yet (grep finds no `.bib` references); no `{cite}` / `{ref}` / `{numref}` MyST roles in the prose. That makes migration cost almost entirely about *front-matter + a TOC file*, not rewriting body text.

| Platform | What you must add | What you may need to rewrite | Rough effort |
|---|---|---|---|
| **Quarto** | One `_quarto.yml`, optional YAML header per file, one `.bib` if/when you add citations. `.ipynb` rendered as-is. ([book setup](https://quarto.org/docs/books/)) | Almost nothing in the body. Pandoc math is native. Some `[link](path.md)` may need extension adjustments. | **Low** — 1–3 person-days for 230 files. |
| **Jupyter Book 2 / mystmd** | `myst.yml`, per-folder TOC. `.md` and `.ipynb` parsed natively. ([myst.yml](https://mystmd.org/guide)) | Body math (`$…$`/`$$…$$`) works. Custom cross-refs to chapters/equations need labels added incrementally. PDF is still maturing. | **Low–Medium** — 2–5 person-days. |
| **MyST-Sphinx (JB1)** | `_config.yml` + `_toc.yml`, Sphinx ext list. ([JB1 docs](https://jupyterbook.org/stable/)) | Same as JB2 plus you're adopting a stack the upstream is actively migrating off — expect a forced re-migration to JB2 within 1–2 years. | **Medium**, plus future re-work. |
| **MkDocs Material** | `mkdocs.yml`, navigation manually, `pymdownx.arithmatex` for math, `mkdocs-jupyter` plugin, `mkdocs-bibtex` for citations. ([material](https://squidfunk.github.io/mkdocs-material/), [mkdocs-jupyter](https://github.com/danielfrg/mkdocs-jupyter)) | Math mostly fine via arithmatex; cross-references between chapters require `autorefs` plugin and manual anchor work; no native numbered equation refs. | **Medium-High** — 5–10 person-days, fragile around equation numbering. |
| **Docusaurus** | `docusaurus.config.js`, sidebars, remark-math + rehype-katex, custom notebook loader (e.g., `nbconvert` → MDX). ([math](https://docusaurus.io/docs/markdown-features/math-equations)) | Rename `.md` to `.mdx`, escape characters that conflict with JSX (`{`, `<`, etc.), build a notebook pipeline because notebooks are not first-class. No native citations. | **High** — 2–4 person-weeks. |
| **GitBook** | Import via GitHub sync; configure in SaaS UI. | Lose execution and reproducibility; LaTeX support is OK but limited; paid for any non-trivial team use. | **Medium** import, **High** ongoing lock-in cost. |
| **Bookdown** | `_bookdown.yml`, `index.Rmd`, knit pipeline. ([bookdown.org](https://bookdown.org/)) | Convert `.md` → `.Rmd`; convert `.ipynb` code to chunks (probably via `reticulate`); install R + LaTeX toolchain. | **High** — 3–6 person-weeks; against the Python grain of the camp. |
| **mdBook** | `book.toml`, `SUMMARY.md`, `mdbook-katex` preprocessor. ([mdbook-katex](https://github.com/lzanini/mdbook-katex)) | Notebooks must be exported to static HTML/Markdown externally — *no execution at build*. Citations and cross-chapter refs are DIY. | **High** for our content shape; mdBook is the wrong tool for math + notebooks. |

The Quarto and Jupyter Book 2 paths share a key property: **no body-text rewrite**. Every other path imposes either format conversion (Bookdown, Docusaurus, mdBook) or a heavy plugin stack with capability gaps (MkDocs, GitBook).

---

## 5. Recommendation

**Pick Quarto.**

Reasoning, prioritised against the brief:

1. **It renders our existing files unchanged.** `.qmd`, `.md`, and `.ipynb` are all first-class inputs to a Quarto book project; Pandoc-flavored `$…$` math is the native syntax we already use; fenced Python blocks and notebook cells execute via Jupyter kernels with `--execute`, `freeze`, and `cache` knobs we control per-chapter ([ipynb reference](https://quarto.org/docs/reference/formats/ipynb.html), [book setup](https://quarto.org/docs/books/)).
2. **Math, citations, cross-refs are first-class, not bolted on.** Numbered equations, `@key` citations from `references.bib`, `@fig-`, `@tbl-`, and `@eq-` cross-references, callouts, and figure captions all work without plugins ([citations](https://quarto.org/docs/authoring/citations.html)) — which matters for the five math-heavy appendices and the regression chapters in Weeks 2–6.
3. **One CLI, one config, deterministic builds.** `quarto render` produces the HTML book; the same source also yields PDF, EPUB, Word, and Reveal.js slides — useful when you eventually need a printable instructor manual or lecture slides from the same prose ([gallery](https://quarto.org/docs/gallery/)). MkDocs and Docusaurus cannot do this; Jupyter Book 2's PDF is still maturing.
4. **GitHub Pages deployment is a documented one-pager.** `quarto publish gh-pages` or the GitHub Action template gets us there in minutes ([GitHub Pages guide](https://quarto.org/docs/publishing/github-pages.html)).
5. **Maintenance burden is low.** Quarto ships as a single binary; the upstream (Posit) is commercially backed and shipping steadily; the next major release is planned for late 2026 with backward compatibility for Quarto 1 files ([Wikipedia](https://en.wikipedia.org/wiki/Quarto_(software))). Author write-ups in 2025 are unanimous: "we should have moved earlier" ([ouseful.info Jan 2025](https://blog.ouseful.info/2025/01/20/migrating-to-quarto/), [ouseful.info Sep 2025](https://blog.ouseful.info/2025/09/23/moving-to-quarto-and-latex/)).
6. **Plugin ecosystem we'd actually want is already in core.** Tabsets, callouts, panel layouts, dark mode, Algolia / built-in search, Thebe-style interactive runtimes, and Observable widgets are out-of-the-box ([Quarto features](https://quarto.org/)).
7. **Risk profile is benign for a Python-first finance camp.** Quarto is language-agnostic; the camp's Python notebooks remain the source of truth. R and Stata code in any future "Mixtape-style" sections (Week 5/Week 7) would also be welcome.

Concrete next steps if you adopt Quarto: (a) add a `_quarto.yml` at the repo root listing chapters and appendices; (b) add three lines of YAML front-matter to each top-level chapter (`title`, `format`, optional `execute: freeze: auto`); (c) add an empty `references.bib` we backfill as citations get added; (d) wire up `.github/workflows/quarto-publish.yml` from the published template ([deployment template](https://thecoatlessprofessor.com/programming/quarto/template-for-auto-deploying-quarto-book-on-github-with-github-pages/)).

---

## 6. Runner-up and when it would win

**Jupyter Book 2** (`mystmd`-based) is the runner-up. We would pick it instead of Quarto if any of these become true:

- We want **richer scientific cross-references and interactive Jupyter-native widgets** (Thebe, JupyterLite live execution in the browser, embedded MyST plugins) — JB2 leans further into this than Quarto today ([MyST guide](https://mystmd.org/guide), [SciPy 2025 paper](https://proceedings.scipy.org/articles/hwcj9957)).
- We want **deeper alignment with the QuantEcon / Project Pythia / Turing Way community** — JB2 is now the de-facto standard there, and contribution patterns (PRs, plugins) match.
- We want **a structured document model with semantic metadata** (cross-project references, content reuse across books) — JB2's MyST AST exposes that; Quarto does not at the same depth.

Jupyter Book 2 is genuinely close to Quarto on capability and *better* on a couple of niche dimensions. Two pragmatic reasons we still rank it second:

1. **Maturity timing.** JB2 only just shipped `2.1.1` in January 2026; the upstream itself describes recent work as "fixing bugs and generally improving stability, reliability, and UX papercuts" ([2i2c Jan 2026](https://2i2c.org/blog/jupyter-book-release-jan-2026/)). Quarto has been past that phase for two release cycles.
2. **Multi-format output.** Quarto's PDF, Word, and slide pipelines are markedly more polished — important for distributing printable problem sets, instructor manuals, and reveal.js lecture decks from the same source.

**Honorable mentions and when to use them:**

- **MkDocs Material** — if the project ever splits the *book* from a *companion documentation site* (e.g., the AI-co-pilot module's API reference, the data-cards as a searchable catalog). Material's search is genuinely best-in-class and complements either Quarto or JB2 nicely as a *second* site.
- **Bookdown** — only if the camp pivots to an R-first curriculum (e.g., to mirror Hyndman/Cunningham). It is not the right tool for our Python-first book.
- **mdBook, Docusaurus, GitBook** — out of scope for a math-and-notebook textbook of this shape.

---

## Sources

- [Jupyter Book / MyST stack release (Jan 2026) — 2i2c](https://2i2c.org/blog/jupyter-book-release-jan-2026/)
- [The Turing Way upgrades to Jupyter Book 2 — JB Blog](https://blog.jupyterbook.org/posts/2025-02-27-the-turing-way-upgrades-to-jb2/)
- [NumPy tutorials now built with Jupyter Book 2 — JB Blog](https://blog.jupyterbook.org/posts/2025-11-13-numpy-tutorials-jb2/)
- [Jupyter Book 2 and the MyST Document Stack — SciPy 2025 Proceedings](https://proceedings.scipy.org/articles/hwcj9957)
- [Towards Jupyter Book 2 with MyST-MD — Executable Books](https://executablebooks.org/en/latest/blog/2024-05-20-jupyter-book-myst/)
- [Jupyter Book 2.0 planning issue #2281](https://github.com/jupyter-book/jupyter-book/issues/2281)
- [MyST Markdown Guide](https://mystmd.org/guide)
- [MyST cross-references](https://mystmd.org/guide/cross-references)
- [myst-parser cross-referencing (Sphinx)](https://myst-parser.readthedocs.io/en/latest/syntax/cross-referencing.html)
- [Quarto](https://quarto.org/)
- [Quarto — Creating a Book](https://quarto.org/docs/books/)
- [Quarto — Jupyter Notebook (ipynb) Options](https://quarto.org/docs/reference/formats/ipynb.html)
- [Quarto — Citations](https://quarto.org/docs/authoring/citations.html)
- [Quarto — GitHub Pages publishing](https://quarto.org/docs/publishing/github-pages.html)
- [Quarto — Book Options reference](https://quarto.org/docs/reference/projects/books.html)
- [Quarto Gallery](https://quarto.org/docs/gallery/)
- [Quarto-CRC template (Chapman & Hall) — bgreenwell](https://github.com/bgreenwell/quarto-crc)
- [Template for auto-deploying Quarto book to GitHub Pages — Coatless Professor](https://thecoatlessprofessor.com/programming/quarto/template-for-auto-deploying-quarto-book-on-github-with-github-pages/)
- [Quarto (software) — Wikipedia](https://en.wikipedia.org/wiki/Quarto_(software))
- [When to use Quarto vs Jupyter Book — Pangeo discourse](https://discourse.pangeo.io/t/when-to-use-quarto-v-jupyterbook/3136)
- [Migrating to Quarto (Jan 2025) — ouseful.info](https://blog.ouseful.info/2025/01/20/migrating-to-quarto/)
- [Moving to Quarto and LaTeX (Sep 2025) — ouseful.info](https://blog.ouseful.info/2025/09/23/moving-to-quarto-and-latex/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [mkdocs-jupyter plugin (GitHub)](https://github.com/danielfrg/mkdocs-jupyter)
- [Docusaurus — Math Equations](https://docusaurus.io/docs/markdown-features/math-equations)
- [mdBook — MathJax support](https://rust-lang.github.io/mdBook/format/mathjax.html)
- [mdbook-katex preprocessor](https://github.com/lzanini/mdbook-katex)
- [Forecasting: Principles and Practice (3rd ed., fpp3) — Hyndman & Athanasopoulos](https://otexts.com/fpp3/)
- [Forecasting: Principles and Practice, the Pythonic Way (2026)](https://otexts.com/fpppy/)
- [Causal Inference: The Mixtape — Cunningham](https://mixtape.scunning.com/)
- [Python Data Science Handbook — VanderPlas](https://jakevdp.github.io/PythonDataScienceHandbook/)
- [Intermediate Quantitative Economics with Python — QuantEcon](https://python.quantecon.org/intro.html)
- [A First Course in Quantitative Economics with Python — QuantEcon](https://intro.quantecon.org/)
- [QuantEcon/lecture-python.myst (GitHub)](https://github.com/QuantEcon/lecture-python.myst)
- [Probabilistic Machine Learning — Murphy (probml.github.io)](https://probml.github.io/pml-book/book1.html)
- [Gallery of Jupyter Books](https://jupyterbook.org/stable/gallery/)
