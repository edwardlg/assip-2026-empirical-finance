---
title: "Poster Template — August 12 Symposium"
description: >-
  Format, structure, and typography for the 48"x36" landscape research
  poster you will defend at the ASSIP Research Symposium on August 12, 2026.
---

# Poster Template — August 12 Symposium

Your **required deliverable** for ASSIP 2026 is a research poster, defended in person (and via virtual breakout for remote interns) at the **ASSIP Research Symposium on Wednesday, August 12, 2026**. This page tells you exactly what the poster needs to look like and how to build it. The substantive guidance — what counts as a finding worth posting, how to talk to a stranger about your work in three minutes — lives in **Chapter 8.5** of the [textbook](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/).

---

## Physical format

| Spec | Value |
|------|-------|
| **Dimensions** | 48 inches wide × 36 inches tall (landscape, horizontal orientation) |
| **File format** | PDF, with all fonts embedded |
| **Color space** | CMYK preferred (some printers will accept sRGB; CMYK avoids surprises) |
| **Resolution** | All raster figures at ≥ 300 DPI at final print size |
| **Template** | GMU College of Science official poster template *([URL TBD — to confirm with Dr. Haymond Still](mailto:cosassip@gmu.edu))* |
| **Bleed** | None (the GMU template includes a built-in border) |
| **File naming** | `poster_<lastname>_<projectN>_v<NN>.pdf`, e.g., `poster_doe_p07_v03.pdf` |

!!! warning "Template URL not yet finalized"
    The GMU College of Science poster template URL for ASSIP 2026 will be circulated by the program office before Week 6. Email <cosassip@gmu.edu> to confirm. Until that link lands, you can prototype against the generic Mason template at <https://branding.gmu.edu>.

---

## Sections (in order, left → right, top → bottom)

A reader walking past your poster spends an average of **eight seconds** before deciding whether to stop. The structure below is the one Prof. Gao uses with his own coauthors; it works because every section answers the next question a skeptical reader is going to ask.

### 1. Title and authorship (top banner)
- **Title:** ≤ 15 words. Active voice. Names the headline finding or question.
- **Author line:** Your name · ASSIP 2026 · George Mason University, College of Science.
- **Mentor line:** *Mentor: Prof. Lei Gao, Costello College of Business.*
- **Track tag:** small badge in the corner — *Fair Lending* / *Common Ownership* / *Innovation* / *FinTech* / *Macro Events*.

### 2. Question (top-left, ~10% of the poster)
One sentence. Why does anyone care?

### 3. Data (top-middle, ~10%)
Two or three lines. Source, time window, unit of observation, N. One figure if you can — a map, a time-series count of observations, or a small balance table.

### 4. Design (top-right, ~15%)
The empirical specification, written out as an equation, with every variable defined. The PAP link (`pap/pap-v1.md`) and the file-date timestamp. The decision rule — what does the headline coefficient sign and significance buy you?

### 5. Results (center, ~30%, the largest single block)
**One** headline figure or table — the one a reader would walk away remembering. Then one supporting table or figure. Captions must be self-contained: a reader who reads only the caption should understand what the picture is saying.

### 6. Robustness (bottom-center, ~15%)
Three to five robustness checks, each a one-line label plus a small coefficient plot or table. The point is to show the reader that you tried to break your result and it survived.

### 7. Contribution (bottom-right, ~10%)
Two or three bullets. *What did we know before? What do we know now? Why is the difference worth your reader's time?*

### 8. Footer (bottom band)
- QR code → GitHub repo (mandatory).
- QR code → PAP (mandatory).
- Funding / acknowledgments (ASSIP, College of Science, RA sub-leader).
- A reproducibility statement: *"All figures and tables in this poster reproduce from a single `make all` command on commit `<sha>`."*

---

## Typography

| Element | Font | Size at final print | Notes |
|---------|------|---------------------|-------|
| Title | Sans, bold | 80 – 100 pt | Readable from 10 feet away |
| Section headers | Sans, bold | 36 – 44 pt | Same color for all sections |
| Body text | Sans, regular | 24 – 28 pt | This is the minimum readable size at a poster session |
| Figure captions | Sans, italic | 20 – 22 pt | One short paragraph; never two |
| Equations | Serif (LaTeX-style) or Computer Modern | 24 – 30 pt | Render at vector resolution |
| URLs / footer | Mono | 18 – 20 pt | OK to use the smaller size in the footer only |

The Mason brand fonts (Source Sans 3 for body, Roboto Slab for display) are the defaults in the GMU template. Do not change them.

---

## Figure standards

Every figure on your poster must conform to the **Appendix D — Figure Standards** in the [textbook](https://edwardlg.github.io/assip-2026-empirical-finance/textbook/). The short version:

- **One** message per figure. If you find yourself writing "and also" in the caption, split it into two figures.
- **Axes labeled** with units (`Coefficient (pp)`, not `coef`).
- **Confidence intervals** shown explicitly — error bars, shaded ribbons, or whiskers. Never report point estimates without a measure of uncertainty.
- **Color-blind safe** palette. The textbook ships with a Mason-green-anchored palette in `code/fig_style.py` / `code/fig_style.R` — use it.
- **Source line** in the bottom-right of every figure: `Source: <data> · Sample: <window> · N = <n>`.
- **Reproducible** — the figure must be produced from a script in your repo, not from a hand-edited Illustrator file. The script's filename goes in the figure's metadata so we can find it months later.

---

## Synthetic-results notice (only if applicable)

Some projects will run their final specification on real data; others may, for reasons of data availability or licensing, finish the summer with results on a **synthetic** or **placebo** sample. That is not a failure — Chapter 7 explains why a synthetic-data pipeline is itself a research contribution — but it must be **disclosed prominently** on the poster.

If any figure or table on your poster uses synthetic, simulated, or placebo data:

!!! danger "Required notice — place a visible badge in the figure title block"
    **Results based on synthetic data — interpretation is illustrative, not inferential.**

The badge should be at least 22 pt, red or Mason-gold background, and placed inside the **Results** section header. The same notice must appear at the top of your JSSR abstract.

If only a subset of figures uses synthetic data, label *those figures* individually and leave the rest unmarked. Your PAP must already note which variables would be synthesized; the disclosure on the poster mirrors that.

---

## Build pipeline

The recommended workflow:

1. Draft the poster in a `.qmd` or `.tex` file inside `poster/` in your repo.
2. Compile to PDF with `make poster`.
3. Open a draft PR titled `Poster v1 — [Project N] — [Your Name]` by **Friday August 7, 2026**.
4. Address PR comments by **Monday August 10, 2026** (dress rehearsal).
5. Submit the final PDF to the College of Science poster-printing queue per the deadline that the program office circulates (typically Mon Aug 10 of symposium week).

The dress rehearsal on Aug 10 is the last point at which mentors and pod RA sub-leaders can flag a layout problem before the print run goes out.

---

## What graders look for

When Prof. Gao and the visiting faculty walk the symposium floor on August 12, they are scoring on four axes:

1. **Clarity of the question.** Can a stranger read the top-left corner and immediately know what you were trying to answer?
2. **Honesty of the result.** Is the PAP linked? Are the robustness checks visible? Is the uncertainty quantified?
3. **Quality of the visualization.** Does the headline figure stand on its own? Are the colors and labels legible at three feet?
4. **The three-minute pitch.** Can you defend your numbers to a skeptical reader in 180 seconds without notes? See Ch 8.5 for the pitch structure.

A great poster is one that — even with the author missing for ten minutes during the symposium — still teaches a stranger something true about the world.
