# Week 8 — Independent Research Project II: Execution, Robustness, Poster, and Defense

Run it, break it on purpose, distill it onto a 48"×36" research poster, write a 200–300-word JSSR
abstract, and defend the work in eight minutes at the ASSIP Research Symposium on **Wednesday,
August 12, 2026**. See [`../../TOC.md`](../../TOC.md) for the full plan.

This is the final active week of ASSIP. The week-7 design (PAP, identification memo) and the
week-8 execution (confirmatory run, multiverse, robustness battery) all funnel into three
artifacts the symposium audience and the Journal of Student-Scientists' Research (JSSR) will
actually see: a **research poster (PDF, GMU College of Science template, ~48"×36" landscape)**, a
**JSSR abstract (200–300 words)**, and an **8-minute poster talk** during the in-person poster
session (with virtual breakouts for remote interns — Prof. Gao's 2026 ASSIP slot is officially
remote). An optional full paper is available for students who want to push the work further; the
graded ASSIP deliverable is the poster + abstract + talk + replication packet.

## Chapters
1. [Ch 8.1 — Execution & Specification Curve](ch81-execution-specification-curve.md) (confirmatory run; multiverse analysis; deviations log)
2. [Ch 8.2 — Robustness & Inference Stress-Tests](ch82-robustness-inference-stress-tests.md) (alt SEs, placebos, sensitivity, BH-FDR, Oster δ)
3. [Ch 8.3 — Writing the Empirical Paper](ch83-writing-the-empirical-paper.md) (the prose discipline — argument-not-transcript, the one-sentence contribution, causal-language discipline — that the abstract and the poster narrative inherit)
4. [Ch 8.4 — Peer Review & Revision](ch84-peer-review-and-revision.md) (the referee report; the revise-and-resubmit memo — adapted for poster-draft critique at ASSIP)
5. [Ch 8.5 — The 8-Minute Poster Talk & the Replication Packet](ch85-presentation-and-replication-packet.md) (slide / poster-panel discipline; defending identification; one-click reproducibility)

## Notebooks (`../../../notebooks/week-08/`)
- nb8.1 Specification-curve generator (144-spec multiverse) · nb8.2 Robustness battery (placebos, wild cluster bootstrap, Oster δ) · nb8.3 Publication tables/figures → LaTeX (pyfixest `etable`) · nb8.4 Reproducibility check (seeded, bit-identical reruns + manifest) · nb8.5 Final poster build (LaTeX/PowerPoint → PDF, engine-gated; the abstract block is `\input{}`ed from a generated file so the 250-word JSSR abstract cannot drift from the analysis)
- All verified to run headless.

## Problem sets (project deliverables; model exemplars in [Appendix E](../../appendices/E-solutions-manual/))
- [PS 8.1](ps8.1.md) Specification curve · [PS 8.2](ps8.2.md) Robustness battery · [PS 8.3](ps8.3.md) JSSR abstract + poster results narrative vs. style guide · [PS 8.4](ps8.4.md) Referee report + R&R memo on a peer poster draft · [PS 8.5](ps8.5.md) 8-min poster talk + replication-packet checklist

## Lab, mentor, assessment
- [Lab 8 — Final Poster + Repo + Symposium Defense](lab8-final-manuscript-repo-defense.md) (poster compile on the GMU College of Science template, Makefile/run_all one-click packet, timed talk dry-run for the Aug 12 symposium)
- [Mentor Session 8 — "Defending a result: what a referee actually asks"](mentor8-defending-a-result.md) (Elnahas, Gao, Hossain & Kim 2024, *JFQA* — the live-defense case study; the same skill the symposium poster-session judges will exercise)
- [Week 8 Assessment + Rubric — the Capstone](assessment8.md) — the program's **terminal assessment** (200 pts): JSSR abstract + research poster + 8-minute poster talk + replication packet + AI-use disclosure
