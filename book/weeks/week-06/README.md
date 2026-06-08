# Week 6 — Reading the Frontier II: Text, Modern Empirics, and the AI Co-Pilot

Text-as-data and machine-learning-flavored empirical finance, plus a full module on using LLMs
*responsibly* as a research co-pilot. See [`../../TOC.md`](../../TOC.md) for the full plan.

## Meta-pack
- [Reading Guide Pack 6 + AI Lab Manual](reading-guide-pack-6-ai-lab-manual.md) — reading measurement papers, a RAG architecture, a prompt-pattern catalog, an LLM-label evaluation harness, and a responsible-use/disclosure checklist.

## Reader's Guides + the AI chapter
1. [Ch 6.1 — Kogan, Papanikolaou, Seru & Stoffman (2017)](ch61-readers-guide-kpss-2017.md), *QJE* 132(2):665–712 (market-based patent value)
2. [Ch 6.2 — Hoberg & Phillips (2016)](ch62-readers-guide-hoberg-phillips-2016.md), *JPE* 124(5):1423–1465 (TNIC; 10-K cosine similarity)
3. [Ch 6.3 — Loughran & McDonald (2011)](ch63-readers-guide-loughran-mcdonald-2011.md), *JF* 66(1):35–65 (finance sentiment dictionaries)
4. [Ch 6.4 — Bartlett et al. (2022) + Bhutta–Hizmo–Ringo (paired)](ch64-readers-guide-bartlett-bhutta-fair-lending.md) (fair lending in the algorithmic era; ties to Gao & Sun 2019)
5. [Ch 6.5 — The AI Co-Pilot for Research (LLM-in-the-Loop)](ch65-ai-copilot-for-research.md) — prompt patterns, RAG over 10-Ks, OOS-validated classification, critical limits, the Anthropic + GMU Azure APIs (env-var keys only)

## Notebooks (`../../../notebooks/week-06/`)
- nb6.1 Patent-value panel (event-study) · nb6.2 10-K text vectorization & cosine similarity (sklearn) · nb6.3 Loughran–McDonald sentiment pipeline · nb6.4 Mortgage-disparity decomposition (Blinder–Oaxaca; over-controlling trap) · **nb6.5 AI co-pilot lab** (RAG + OOS-validated classification; runs offline with a local fallback, env-gated live Anthropic/Azure cells, no hard-coded secrets)
- All verified to run headless.

## Problem sets (solutions in [Appendix E](../../appendices/E-solutions-manual/))
- [PS 6.1](ps6.1.md) Patent-value · [PS 6.2](ps6.2.md) Cosine/TNIC · [PS 6.3](ps6.3.md) LM vs. naive dictionary · [PS 6.4](ps6.4.md) Fair-lending decomposition · [PS 6.5](ps6.5.md) LLM classification + held-out validation + leakage audit

## Mentor, assessment
- [Mentor Session 6 — "Text as data, and AI without fooling yourself"](mentor6-text-as-data-ai-without-fooling-yourself.md) (Gao et al. 2024 *JCF*; Gao et al. forthcoming *J. Financial Education*)
- [Week 6 Assessment + Rubric](assessment6.md) — build and **validate** a text classifier with an out-of-sample report (completable with no API key)
