# ASSIP 2026 — Empirical Finance Research Wiki

This directory builds the **cohort dashboard** for the Aspiring Scientists
Summer Internship Program (ASSIP) Empirical Finance Research group at George
Mason University, Summer 2026 (Prof. Lei Gao, Director: Dr. Amanda Haymond
Still, `cosassip@gmu.edu`).

It is intentionally **separate** from the Quarto textbook that lives in the
parent directory (`/mnt/e/ccli/ASSIP8weeks/`):

| Site             | Tool             | Audience                      | Source            |
| ---------------- | ---------------- | ----------------------------- | ----------------- |
| Textbook + labs  | Quarto           | Self-study readers, alumni    | `../book/`, `../*.qmd` |
| Cohort dashboard | MkDocs Material  | This summer's 14 interns      | `./docs/`         |

The two sites cross-link to each other.

---

## Quick start

### 1. Install build deps

```bash
# from /mnt/e/ccli/ASSIP8weeks/wiki/
python -m venv .venv
source .venv/bin/activate          # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Preview locally

```bash
mkdocs serve
```

Open <http://127.0.0.1:8000>. The dev server hot-reloads on any change to
`mkdocs.yml`, `docs/`, `overrides/`, `docs/stylesheets/`, or
`docs/javascripts/`.

### 3. Build static HTML

```bash
mkdocs build --strict
```

Output is written to `./site/`. The `--strict` flag fails the build on any
broken nav link or unresolved cross-reference — keep it green before
merging.

### 4. Deploy

Deployment is wired through GitHub Actions (see
`/mnt/e/ccli/ASSIP8weeks/.github/workflows/` for the workflow files). On
push to `main`, the action runs `mkdocs build` and publishes `./site/` to
the configured GitHub Pages target (root path `/`).

For a one-off manual deploy from a maintainer's machine:

```bash
mkdocs gh-deploy --force
```

---

## Layout

```
wiki/
├── mkdocs.yml                 # site config (theme, nav, plugins, palette)
├── requirements.txt           # pinned Python build deps
├── README.md                  # this file
├── overrides/                 # (reserved) custom HTML template overrides
└── docs/
    ├── index.md               # Home dashboard (grid cards) — TODO: content
    ├── stylesheets/
    │   └── extra.css          # GMU green + gold palette, card grid, badges
    ├── javascripts/
    │   └── mathjax.js         # MathJax 3 config + instant-nav rebinder
    ├── home/                  # "Home" tab content
    ├── weeks/                 # "Week-by-Week" tab content (Week 0–8)
    ├── projects/              # "Projects" tab content (capstone groups)
    ├── cohort/                # "Cohort" tab content (roster, mentors)
    └── resources/             # "Resources" tab content (data, tools)
```

The five top-level tabs in the rendered nav correspond to the five
subdirectories under `docs/` (plus `index.md` for Home). Content pages
referenced in `mkdocs.yml`'s `nav:` block are populated by separate authoring
passes — this commit ships only the scaffold.

---

## Design notes

* **Direction A** from the wiki research scoping doc:
  *course dashboard with grid cards, top tabs for program phases,
  GMU green + gold palette.*
* **Light mode**: Mason Green (`#006633`) primary, Mason Gold (`#FFCC33`)
  accent.
* **Dark mode**: inverse — Mason Gold primary on near-black, green as
  secondary surface.
* **Type**: Inter (text), JetBrains Mono (code).
* **Math**: MathJax 3 via `pymdownx.arithmatex` in `generic: true` mode,
  so authors can write `$x$`, `\(x\)`, `$$ ... $$`, or `\[ ... \]`.
* **Diagrams**: Mermaid via `pymdownx.superfences` custom fences
  (` ```mermaid `).
* **Grid cards** on the Home and phase landing pages use Material's
  `.grid.cards` component, restyled in `stylesheets/extra.css` with Mason
  hover states.

---

## Program facts cached for content authors

These are the canonical 2026 facts. Cite them verbatim:

| Item              | Value                                                            |
| ----------------- | ---------------------------------------------------------------- |
| Program           | Aspiring Scientists Summer Internship Program (ASSIP)            |
| Host              | George Mason University, College of Science                      |
| Director          | Dr. Amanda Haymond Still (`cosassip@gmu.edu`)                    |
| Mentor / cohort   | Prof. Lei Gao — Empirical Finance Research Group (remote-only)   |
| Orientation       | Thursday **June 18, 2026**                                       |
| First day         | Monday **June 22, 2026**                                         |
| Holidays off      | Jun 19 (Juneteenth), Jul 3 (Independence Day observance)         |
| Symposium         | Wednesday **August 12, 2026** (in-person + virtual breakouts)    |
| Schedule          | Mon–Fri, 9:00 am – 5:00 pm (full-time)                           |
| Modality (2026)   | **Remote only** for this group                                   |
| Eligibility       | HS students 15+ (16+ for in-person wet lab); undergrads ≤ senior |
| Cost              | \$25 application fee + \$1,299 tuition; Pell / reduced-lunch waivers |
| Deliverables      | Poster (required), JSSR abstract, optional full paper, 3 GMU credits |
| Credit            | 3 GMU College of Science credits                                 |

If any fact above changes, update both this README *and*
`mkdocs.yml → extra.program` so the macros plugin can surface the new value
across every page.
