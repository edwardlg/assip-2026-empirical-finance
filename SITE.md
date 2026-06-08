# Site build & deploy guide

This document explains how the **textbook website** (the Quarto book in
this repo) is built and how it is deployed alongside the **project
wiki** as a dual-site GitHub Pages deployment.

## The dual-site layout

The deployed GitHub Pages site has two co-located surfaces:

| URL path | Content | Source |
|---|---|---|
| `https://edwardlg.github.io/assip-2026-empirical-finance/` | **Project wiki** — ASSIP 2026 cohort wiki (announcements, FAQs, week-by-week logistics, mentor pods, deliverable status) | separate Markdown tree at the **root** of the `gh-pages` branch |
| `https://edwardlg.github.io/assip-2026-empirical-finance/textbook/` | **Textbook** — Quarto book (this repo: chapters, notebooks, data cards, capstones, instructor manual) | built into `_site/textbook/` by `quarto render` and published into the `textbook/` subdirectory of `gh-pages` |

The Quarto config sets `output-dir: _site/textbook` so the entire book
renders into a `textbook/` subdirectory. The GitHub Pages workflow then
publishes the contents of `_site/` to the `gh-pages` branch, which
leaves the wiki at the root and the book at `/textbook/`.

> **Placeholder repo URL:** `https://github.com/edwardlg/assip-2026-empirical-finance`
> — replace once the actual repo is created and update `_quarto.yml`
> (`book.repo-url`, `book.site-url`, navbar GitHub link) and
> `_includes/notebook-buttons.html` (`GH_OWNER`, `GH_REPO`).

## What gets built (this repo)

`_quarto.yml` declares a **Quarto book project** that includes:

- `index.qmd` — landing page (hero, quick-stats, 8-week grid keyed to
  the ASSIP 2026 calendar)
- `about.qmd`, `404.qmd`
- every chapter under `book/00-front-matter/`, `book/weeks/week-XX/`,
  `book/capstones/`, `book/instructor-manual/`
- every appendix under `book/appendices/A-..E-..`
- every notebook under `notebooks/week-XX/*.ipynb`
- every data card under `data-cards/*.md`

Output is **HTML only** (KaTeX math, full-text search, dark/light
themes), rendered into `_site/textbook/`. Notebooks are **not executed**
on CI or during local render (`execute.enabled: false`); their `.ipynb`
output cells are rendered as-is, and students run them in
Colab / Binder / locally via the launcher buttons that the include
script injects.

## Install Quarto (one-time)

macOS:

    brew install --cask quarto

Linux (Ubuntu / WSL):

    # See https://quarto.org/docs/get-started/ for the latest .deb
    curl -fsSL https://quarto.org/download/latest/quarto-linux-amd64.deb -o /tmp/quarto.deb
    sudo dpkg -i /tmp/quarto.deb

Verify:

    quarto --version
    quarto check

## Render locally

From the repo root:

    # Live-reload preview at http://localhost:4200
    quarto preview

    # One-shot full render into ./_site/textbook/
    quarto render

    # Render a single file (faster iteration on the landing page)
    quarto render index.qmd --to html

To preview the dual-site layout locally, serve `_site/` (not
`_site/textbook/`):

    python -m http.server --directory _site 4300
    # Book lives at http://localhost:4300/textbook/
    # Wiki (if you drop a wiki build into _site/ root) lives at http://localhost:4300/

The first full render takes a minute or two because of the 40
notebooks; subsequent renders are cached via the `freeze` directory
(`_quarto.yml` sets `freeze: true`). To force re-render of a file,
delete its entry in `_freeze/` or pass `--cache-refresh`.

## Theme

- Light: **cosmo** + `styles.scss`
- Dark:  **darkly** + `styles.scss`

`styles.scss` overrides typography (serif body, sans nav, JetBrains
Mono code), color palette (restrained academic blue on warm paper),
and adds the landing-page hero/quick-stats/week-grid layout. Edit
`styles.scss` and re-render to see changes.

## Notebook launcher buttons

`_includes/notebook-buttons.html` is included into the `<head>` of
every page (`format.html.include-in-header` in `_quarto.yml`). It is a
small client-side script that detects whether the current page was
rendered from an `.ipynb` source. If so, it injects four buttons under
the page title:

1. **Open in Colab** — `https://colab.research.google.com/github/<owner>/<repo>/blob/<branch>/<path>.ipynb`
2. **Open in Binder** — `https://mybinder.org/v2/gh/<owner>/<repo>/<branch>?filepath=<path>.ipynb`
3. **Download .ipynb** — direct raw.githubusercontent.com link
4. **View on GitHub** — the source `.ipynb` file

The repo owner, repo name, and branch are hard-coded at the top of
`_includes/notebook-buttons.html` (`GH_OWNER`, `GH_REPO`, `GH_BRANCH`).
**When the public repo is created, update those three constants to
match the placeholder `edwardlg/assip-2026-empirical-finance`** (or
whatever the final name is). Binder works because `environment.yml`
lives at the repo root.

## GitHub Actions deploy

`.github/workflows/quarto-publish.yml` runs on every push to `main` and
on manual dispatch from the Actions tab. It:

1. Checks out the repo (full history — required by the publish action).
2. Installs Quarto (`quarto-dev/quarto-actions/setup@v2`).
3. Runs `quarto check` for diagnostics.
4. Runs `quarto render` to build the site into `_site/textbook/`.
5. (Optional) merges the wiki tree into `_site/` at the root, if a
   sibling wiki repo or submodule supplies one.
6. Pushes `_site/` to the **`gh-pages`** branch via
   `quarto-dev/quarto-actions/publish@v2`.

The first successful run will create the `gh-pages` branch.

### Wiki integration

The wiki lives in a separate Markdown tree (e.g. a `wiki/` submodule, a
sibling repo, or a GitHub Wiki export). The expected pattern is:

- Wiki tree is rendered (or copied as static HTML) into `_site/` at the
  root, **before** the publish step.
- The Quarto build already wrote the book into `_site/textbook/`, so the
  two trees coexist without collision.
- `_site/` is published whole to `gh-pages`.

If the wiki ships only as raw Markdown, render it with any static-site
tool (mkdocs, Jekyll, Hugo, or even `pandoc` per file) into HTML before
the publish step. Pick one and document the choice in the wiki repo's
own README; this textbook config does not assume a particular wiki
generator.

### Enable GitHub Pages (one-time)

1. Go to repository **Settings → Pages**.
2. Under **Build and deployment**:
   - Source: **Deploy from a branch**
   - Branch: **`gh-pages`** / **`/ (root)`**
3. Click **Save**.
4. After 30-60 seconds the site appears at
   `https://edwardlg.github.io/assip-2026-empirical-finance/` (wiki)
   and `https://edwardlg.github.io/assip-2026-empirical-finance/textbook/`
   (this textbook).

### Custom domain (optional)

Add a `CNAME` file at the repo root containing your domain (e.g.
`assip.example.edu`) and configure your DNS provider to CNAME that
hostname to `edwardlg.github.io`. GitHub Pages will pick up the CNAME
file on the next deploy. The wiki will then live at
`https://assip.example.edu/` and the book at
`https://assip.example.edu/textbook/`.

## Troubleshooting

**Build fails on a single chapter.** Quarto's error message names the
file and line. Comment that entry out of the `chapters:` list in
`_quarto.yml`, re-render to confirm the rest builds, then fix the file.

**Math doesn't render.** Confirm `html-math-method: katex` is still in
`_quarto.yml` and that the equation uses standard LaTeX syntax. KaTeX
supports most but not all of LaTeX — see
<https://katex.org/docs/supported.html>.

**Notebook output looks stale.** `freeze: true` keeps previously
rendered outputs. Delete the relevant subdirectory under `_freeze/` and
re-render. (Or just delete the whole `_freeze/` folder.)

**Launcher buttons not showing on a notebook page.** Open the page in
the browser and check the console. The script needs the `<meta
name="quarto:source-file">` tag (Quarto 1.4+) or a URL ending in
`notebooks/week-XX/...html`. If neither matches, the script silently
no-ops by design. Also confirm `GH_OWNER` / `GH_REPO` / `GH_BRANCH` in
`_includes/notebook-buttons.html` point at the ASSIP repo.

**Wiki overwrites the textbook (or vice versa).** Make sure the wiki
tree never writes a file named `textbook/index.html` at the root of
`_site/`. The book owns the entire `_site/textbook/` subtree; the wiki
owns everything else in `_site/`.

## Local clean

    rm -rf _site _freeze .quarto

That is safe: the next `quarto render` will rebuild everything.
