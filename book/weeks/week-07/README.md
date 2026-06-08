# Week 7 — Independent Research Project I: From Question to Pre-Analysis Plan

Turn a hunch into a falsifiable, pre-registered empirical design with data in hand. See
[`../../TOC.md`](../../TOC.md) for the full plan.

## Chapters
1. [Ch 7.1 — Idea-Generation Workshop](ch71-idea-generation-workshop.md) (so-what filter; cast → dataset map; feasibility/novelty rubric)
2. [Ch 7.2 — Data Acquisition in Practice](ch72-data-acquisition-in-practice.md) (WRDS, EDGAR, FRED, HMDA, 13F, PatentsView, yfinance; reproducible pulls)
3. [Ch 7.3 — The Pre-Analysis Plan (Olken 2015 short form)](ch73-pre-analysis-plan.md) (hypotheses, primary spec, FDR, falsification, register before peeking)
4. [Ch 7.4 — Building the Analysis Dataset](ch74-building-the-analysis-dataset.md) (PERMNO/GVKEY/CIK crosswalks, survivorship/look-ahead, winsorizing, missing data)
5. [Ch 7.5 — The Identification Memo](ch75-identification-memo.md) (identifying-assumption sentence + threats-and-responses table)

## Notebooks (`../../../notebooks/week-07/`)
- nb7.1 Idea-to-spec template (runnable scoring rubric) · nb7.2 Multi-source data-pull harness (cache-or-fetch + audit log; env-gated real pulls, offline-safe) · nb7.3 PAP companion (power calc + BH-FDR + PAP emitter) · nb7.4 Dataset-build & validation (validate= merges, merge_asof look-ahead guard) · nb7.5 First-look regressions (frozen until PAP filed)
- All verified to run headless; no hard-coded secrets.

## Problem sets (project deliverables; model exemplars in [Appendix E](../../appendices/E-solutions-manual/))
- [PS 7.1](ps7.1.md) Candidate questions + rubric · [PS 7.2](ps7.2.md) Pull script + data card · [PS 7.3](ps7.3.md) Pre-analysis plan · [PS 7.4](ps7.4.md) Merged analysis dataset + diagnostics · [PS 7.5](ps7.5.md) Identification memo + threats table

## Lab, mentor, assessment
- [Lab 7 — Your Data, Reproducibly](lab7-your-data-reproducibly.md) (repo template, pinned env, .gitignore discipline, PAP as a tagged commit)
- [Mentor Session 7 — "How I pick a project — and kill one"](mentor7-how-i-pick-and-kill-a-project.md) (Gao, He & Wu 2023 *JFQA*; *Rainbow of Credits*)
- [Week 7 Assessment + Rubric](assessment7.md) — submit the PAP + identification memo (the design half of the capstone)
