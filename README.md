# Empirical Finance from the Ground Up — ASSIP 2026 Cohort

### A Textbook, Lab Manual, Problem-Set Bank, Capstone Gallery, and Instructor's Manual for the GMU ASSIP 2026 Empirical Finance Group

**Host (faculty mentor):** Prof. Lei Gao, Associate Professor of Finance, Costello College of Business, George Mason University — **2026 ASSIP slot: REMOTE only.**
**Program:** Aspiring Scientists Summer Internship Program (ASSIP), GMU College of Science. Director: Dr. Amanda Haymond Still. Contact: `cosassip@gmu.edu`.
**Cohort:** 14 advanced high-school and pre-graduation undergraduate researchers (typical ASSIP group size is 2–15; 14 is the high end and warrants layered mentorship via PhD/RA sub-leaders).
**Calendar:** Orientation Thu **Jun 18, 2026**; first working day Mon **Jun 22**; symposium **Wed Aug 12**. ~8 net active weeks, Mon–Fri 9:00 am – 5:00 pm. Holidays off: Fri **Jun 19** (Juneteenth) and Fri **Jul 3** (Independence Day observance).
**Deliverable:** A research poster at the **ASSIP Research Symposium on Aug 12, 2026**, an abstract submitted to the *Journal of Student-Scientists' Research* (JSSR, GMU Mason Publishing), an optional full paper, and 3 GMU College of Science credits.
**Audience prerequisites:** AP Calc BC + AP Stats (or equivalents); some prior Python; no GPA floor; HS 15+ (16+ for in-person wet-lab tracks — not applicable here, as our slot is remote).
**License intent:** CC BY-NC-SA 4.0 (see front-matter title page).

---

## 0. Live sites

Once the repository is pushed and GitHub Pages is enabled, this project is published as **two interlinked sites** on the same Pages domain:

| Site | URL | Source | Purpose |
|---|---|---|---|
| **Cohort wiki** | `https://<owner>.github.io/<repo>/` | [`wiki/`](wiki/) (MkDocs Material) | Operational dashboard — week-by-week dates, project templates, mentor roster, FAQ, symposium logistics, resources. |
| **Textbook** | `https://<owner>.github.io/<repo>/textbook/` | this repo's root (Quarto) | The 8-week textbook, problem sets, notebooks, capstones, appendices, instructor's manual. |

The two sites cross-link: the wiki points students at the textbook chapter for each day, and the textbook's "Cohort & Mentorship" pages point back at the wiki for the live operational details. The dual deploy is built by a single GitHub Actions workflow at [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) — see [`SITE.md`](SITE.md) for the full local-build + deploy walkthrough.

---

## 1. What this is

This repository is a publication-quality, self-contained curriculum built for the **ASSIP 2026 Empirical Finance research group**. It is simultaneously:

- a **textbook** that rebuilds probability, OLS, and modern causal inference from first principles, using the "reveal-the-trick" pedagogy (state the result, show why it works, show when it fails, show the code);
- a **lab manual** of hands-on, dataset-driven exercises;
- a **problem-set bank** with a fully worked solutions manual;
- a **capstone gallery** of five publication-style example papers students can model their own work on; and
- an **instructor's manual** for pacing, mentoring, grading, and equity/access — calibrated specifically to the ASSIP 8-week full-time format.

The book deepens the methodological core; the live ASSIP 2026 program supplies the cohort, the symposium, the scientific-writing forum, and the institutional scaffolding (see the [Articulation Matrix](book/00-front-matter/01-articulation-matrix.md) and the [Cohort & Mentorship Model](book/00-front-matter/04-cohort-and-mentorship.md)).

**Quick stats**

| | |
|---|---:|
| Weeks of instruction | 8 |
| Chapters / reading guides + appendix sections | ~40 |
| Verified Jupyter notebooks | 40 |
| Data cards (Appendix C / `data-cards/`) | 34 |
| Capstone example papers | 5 |
| Instructor's-manual sections | 6 |
| Target length | ~672,000 words |

---

## 2. Repository map

```
ASSIP8weeks/
├── README.md                         This file — master entry point.
├── CONVENTIONS.md                    "The Constitution": voice, notation, spec discipline, reproducibility, citations.
├── SITE.md                           How the Quarto book is built and deployed (dual-site: textbook + wiki).
├── _quarto.yml                       Quarto book config. Output goes to _site/textbook/ (book lives at /textbook/).
├── index.qmd, about.qmd, 404.qmd     Landing, about, and 404 pages of the textbook site.
├── styles.scss                       Custom SCSS for the textbook theme.
├── install-tools.sh                  One-shot installer for CLI tooling (jq, fd, gh, ...).
├── environment.yml                   Pinned conda environment (python=3.11 + scientific stack).
├── .gitignore                        Excludes licensed data and secrets from version control.
│
├── book/                             All prose.
│   ├── TOC.md                        The full plan: every chapter, problem set, notebook, lab, mentor session, word budget.
│   ├── 00-front-matter/              Preface, articulation matrix, how-to-use, prerequisite self-test, cohort & mentorship model.
│   ├── weeks/                        The 8-week arc.
│   │   ├── week-01/ ... week-08/     Each: README, 5 chapters, 5 problem sets, lab/reading pack, mentor session, assessment.
│   ├── appendices/
│   │   ├── A-math-toolkit/           Matrix algebra, optimization, asymptotics, distributions reference.
│   │   ├── B-python-latex-setup/     Conda env, GitHub Classroom, WRDS Cloud, Hopper SLURM, Overleaf/LaTeX.
│   │   ├── C-data-dictionary/        Pointer/index for the data cards.
│   │   ├── D-style-guide/            Empirical-finance writing: tables, regressions, robustness, replication packet.
│   │   └── E-solutions-manual/       Every problem set fully worked, organized by week.
│   ├── capstones/                    5 publication-style example papers + annotated "how it was built" notes.
│   └── instructor-manual/            Pacing, rubrics, pitfalls, mentor notes, answer keys, equity/access.
│
├── notebooks/                        Runnable companions, one per chapter.
│   └── week-01/ ... week-08/         40 verified notebooks mirroring the chapters.
│
├── data-cards/                       34 data-source cards (provider, coverage, identifiers, access, license, gotchas).
│
├── docs/
│   └── superpowers/specs/            Design specs (front-matter & TOC design, citation anchor list).
│
└── agents/
    └── handoffs/                     Per-slice agent handoff logs and the running [CHECK] ledger.
```

---

## 3. The 8-week arc (ASSIP 2026 calendar)

Each week contains a week-opening narrative, five chapters, five daily problem sets (solutions in Appendix E), a notebook per chapter with a "Your Turn" extension, a lab manual (Weeks 1–4, 7–8) or paper-reading guides (Weeks 5–6), a 60-minute Lei Gao mentor session, and an end-of-week assessment with rubric. The full-time M–F format means roughly one chapter per morning + a problem-set / notebook block in the afternoon; mentor sessions anchor mid-week.

| Week | ASSIP dates (M–F) | Theme | Link |
|---|---|---|---|
| 1 | Jun 22 – Jun 26 | **Foundations & inference** — probability, sampling, the logic of inference, with simulation as the microscope. | [week-01](book/weeks/week-01/README.md) |
| 2 | Jun 29 – Jul 2 *(Jul 3 off)* | **The OLS engine** — OLS in matrix form, Gauss–Markov, FWL, and the three ways the story breaks (heteroskedasticity, clustering, misspecification). | [week-02](book/weeks/week-02/README.md) |
| 3 | Jul 6 – Jul 10 | **Causal inference I** — potential outcomes, selection-on-observables (matching, entropy balancing, AIPW), and instrumental variables. | [week-03](book/weeks/week-03/README.md) |
| 4 | Jul 13 – Jul 17 | **Causal inference II** — DiD/event studies, the staggered-adoption crisis, regression discontinuity, synthetic control, and shift-share designs. | [week-04](book/weeks/week-04/README.md) |
| 5 | Jul 20 – Jul 24 | **Reading the frontier I** — one classic empirical paper per day, decoded with a fixed Reader's-Guide anatomy. | [week-05](book/weeks/week-05/README.md) |
| 6 | Jul 27 – Jul 31 | **Reading the frontier II + AI** — text-as-data and modern empirics, plus a module on using LLMs responsibly as a research co-pilot. | [week-06](book/weeks/week-06/README.md) |
| 7 | Aug 3 – Aug 7 | **Research project I** — from question to a falsifiable, pre-registered design with data in hand. | [week-07](book/weeks/week-07/README.md) |
| 8 | Aug 10 – Aug 12 *(symposium Wed)* | **Research project II** — execution, robustness, poster build, defense at the ASSIP Symposium. | [week-08](book/weeks/week-08/README.md) |

Orientation is Thursday **Jun 18, 2026**; Friday **Jun 19** is Juneteenth (off). See [`book/TOC.md`](book/TOC.md) for the line-by-line plan and word budget, and [`book/instructor-manual/IM1-pacing-guide.md`](book/instructor-manual/IM1-pacing-guide.md) for the day-by-day ASSIP pacing.

---

## 4. How to use the book (student path)

1. **Start in the front matter.** Read the [Preface](book/00-front-matter/00-preface.md), then the [Articulation Matrix](book/00-front-matter/01-articulation-matrix.md) to see how the curriculum maps onto ASSIP's symposium deliverable, and the [Cohort & Mentorship](book/00-front-matter/04-cohort-and-mentorship.md) page for how the 14-student group is organized.
2. **Read [How to Use This Book](book/00-front-matter/02-how-to-use.md).** It explains the daily rhythm and how chapters, problem sets, notebooks, labs, and mentor sessions interlock, and introduces the recurring student cast (Maya, Devon, Priya, Sam, Leah).
3. **Take the [Prerequisite Self-Test](book/00-front-matter/03-prerequisite-self-test.md).** It routes you: if you miss the calculus/probability/Python items, read **Appendix A** ([Math Toolkit](book/appendices/A-math-toolkit/README.md)) and **Appendix B** ([Python + LaTeX Setup](book/appendices/B-python-latex-setup/README.md)) first. Doing this **before Jun 22** is the single highest-leverage thing you can do.
4. **Work the weeks in order.** For each chapter, read the prose, run the matching notebook in [`notebooks/`](notebooks/README.md), then do that day's problem set; check yourself against [Appendix E](book/appendices/E-solutions-manual/README.md).
5. **Aim at the symposium.** Weeks 7–8 turn the toolkit into your own poster + abstract for the **ASSIP Research Symposium on Aug 12, 2026**; the [Capstone Gallery](book/capstones/README.md) shows five finished exemplars to model from.

---

## 5. How to deploy the camp (instructor path)

1. **Set up the environment.** Follow **Appendix B** ([B.1 Toolchain](book/appendices/B-python-latex-setup/B1-toolchain.md)): install Miniconda/Miniforge and create the camp environment from the root `environment.yml` (`conda env create -f environment.yml`). The stack is pinned: `python=3.11`, `pandas>=2.2`, `numpy`, `scipy`, `statsmodels`, `linearmodels`, `pyfixest`, `matplotlib`, `wrds`, `yfinance`, `pandas-datareader`, `requests`, `pyarrow`.
2. **Wire GitHub Classroom.** See [B.2](book/appendices/B-python-latex-setup/B2-github-classroom.md) for the assignment-repo and submission workflow.
3. **Provision licensed data on GMU infrastructure.** WRDS Cloud access and querying are covered in [B.3](book/appendices/B-python-latex-setup/B3-wrds-cloud.md); GMU Hopper SLURM templates (batch jobs, A100 GPU for the AI module) in [B.4](book/appendices/B-python-latex-setup/B4-hopper-slurm.md). **Per CONVENTIONS §5, licensed data (CRSP, Compustat, etc.) stays read-only on GMU infrastructure (Hopper / WRDS Cloud) and is never committed to this repo.**
4. **Configure the AI module keys (Week 6).** Provide credentials via **environment variables only** — `ANTHROPIC_API_KEY` for the Anthropic Messages API and the GMU Azure APIM gateway credentials (`AZURE_APIM_KEY`, base URL) for GPT-5.4 / 4.1 / 4o / Maverick. A **no-key local fallback** runs the same exercises against Ollama / a Hopper A100, so students without keys are never blocked.
5. **Run the cohort.** The [Instructor's Manual](book/instructor-manual/README.md) provides the [ASSIP-specific pacing guide](book/instructor-manual/IM1-pacing-guide.md) (M–F 9–5, Jun 22 – Aug 12, with Jun 19 and Jul 3 off), [grading rubrics](book/instructor-manual/IM2-grading-rubrics.md), [common pitfalls](book/instructor-manual/IM3-common-pitfalls.md), [guest-lecture/mentor notes](book/instructor-manual/IM4-guest-lectures-mentor-notes.md), [answer keys + anchor work](book/instructor-manual/IM5-answer-keys-anchor-work.md), and [equity/access notes](book/instructor-manual/IM6-equity-access.md) — including how to run the all-remote 2026 slot and how the layered mentorship (faculty mentor + PhD/RA sub-leaders) is organized across the 14 students.

### Deploying the site

The book ships as a Quarto site that lives at the **`/textbook/`** subpath of the deployed GitHub Pages domain, so a project wiki can live at the root. Target repo:

> `https://github.com/edwardlg/assip-2026-empirical-finance` *(placeholder until the public repo is created)*

Once that repo exists, push to `main` and the included [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) GitHub Action will, in a single Ubuntu job:

1. Run `quarto render` (the book builds into `_site/textbook/`).
2. Run `mkdocs build --site-dir ../_site/` from `wiki/` (the wiki builds into `_site/` at root).
3. Publish the combined `_site/` to the `gh-pages` branch via `peaceiris/actions-gh-pages@v4`.
4. The **wiki** is served from `https://edwardlg.github.io/assip-2026-empirical-finance/`.
5. The **textbook** is served from `https://edwardlg.github.io/assip-2026-empirical-finance/textbook/`.

See [`SITE.md`](SITE.md) for the full local-render + deploy walkthrough, including the dual-site directory layout.

---

## 6. Reproducibility & conventions

This project enforces a strict reproducibility discipline, set out in [`CONVENTIONS.md`](CONVENTIONS.md):

- **Pinned environment.** `python=3.11` plus the pinned scientific stack above; every code block must run end-to-end on a fresh conda env.
- **Notebooks verified headless.** All 40 notebooks are designed to execute non-interactively, with sample output and a "Your Turn" extension.
- **Secrets via environment variables only.** No keys are hard-coded; `.env` and `*.key` are git-ignored.
- **Licensed data never committed.** Data files (`data/`, `*.parquet`, `*.csv`) are git-ignored except the documentation in `data-cards/`; licensed snapshots stay on GMU infrastructure with their snapshot date pinned in the notebook that uses them.
- **The `[CHECK]` policy.** Unverified citations and live API/endpoint specifics are tagged `[CHECK]` rather than fabricated, so a human can confirm them before publication.

See [`CONVENTIONS.md`](CONVENTIONS.md) for the full constitution: audience and voice, the recurring student cast, notation, empirical-spec discipline, code rules, citation rules, and file/naming conventions.

---

## 7. Credits & status

- **Faculty mentor / author:** Prof. Lei Gao, Costello College of Business, George Mason University. 2026 ASSIP slot: REMOTE only.
- **Host program:** ASSIP (Aspiring Scientists Summer Internship Program), GMU College of Science. Director: Dr. Amanda Haymond Still. Program contact: `cosassip@gmu.edu`.
- **Build process:** drafted via a multi-agent workflow (Planner → Writer → Coder → Reviewer), with every slice logged under [`agents/handoffs/`](agents/handoffs/README.md).
- **Open items:** outstanding `[CHECK]` items — chiefly exact page ranges/venues for the Week 5–6 cited papers — are tracked in [`agents/handoffs/`](agents/handoffs/README.md) and consolidated at the foot of [`book/TOC.md`](book/TOC.md). All Prof. Gao citations follow `CONVENTIONS.md §6` verbatim.
