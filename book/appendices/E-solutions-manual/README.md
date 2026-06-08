# Appendix E — Solutions Manual

This appendix works every problem set in the camp, all eight weeks of it. A solution here is not an answer key: it is the full path from the problem to the number. Where a result needs proving, you get the derivation — intuition first, then a worked numerical case, then the algebra, in the order CONVENTIONS asks for. Where a result needs computing, you get the runnable code that produces it. And every solution closes the loop with interpretation: what the number means for the question that motivated the problem, and where the method would break if you pushed it.

Weeks 1–6 are **numeric drills**. The questions have right answers, and the solutions reach them by hand and in code so you can check both your arithmetic and your reasoning. Weeks 7–8 are different: those problem sets scaffold your own research project (a question, a data pull, a pre-analysis plan, a robustness battery, a deck), so they have no single right answer. For those, the manual gives **A-grade model deliverables** — one fully worked exemplar per assignment, built on the chapter's running student-cast example, so you can see the shape and discipline of "done well" before you build your own. The numbers in those exemplars are illustrative teaching figures, never real licensed-data output, and they are labeled as such inside each file.

**How to use this.** Try the problem first. Sit with it, get stuck, write down a wrong answer — then read the solution. A worked solution you read before attempting the problem teaches you almost nothing; the same solution read after a genuine attempt is where the learning happens. If your number disagrees with ours, find out why before you move on: the disagreement is usually the most instructive thing on the page.

**Honesty norm.** These solutions exist so you can learn from them, not copy from them. Submitting a solution from this manual as your own work is the one thing that defeats the entire point of the camp — the camp exists to build *your* judgment, and the only person you cheat is yourself. Cite the manual if you lean on it. When you are unsure whether something crosses the line, ask your mentor.

All solutions follow the notation in [`CONVENTIONS.md`](../../../CONVENTIONS.md) §3 — $\mathbb{E}[\cdot]$, $\operatorname{Var}(\cdot)$, $\operatorname{Cov}(\cdot,\cdot)$; bold for vectors and matrices; hats for estimates; standard errors always labeled by flavor (classical, HC1/2/3, HAC, clustered). Every empirical spec names its outcome, key regressor, controls, fixed effects, clustering, sample, and identifying assumption, per §4. All arithmetic in this manual was verified numerically.

---

## Index

### Week 1 — Probability, estimators, and inference *(numeric drills)*

- [PS 1.1](E-w1-ps1.1-solutions.md) — Conditional probability, the law of iterated expectations, and the law of total variance.
- [PS 1.2](E-w1-ps1.2-solutions.md) — Expectation/variance algebra and the geometry of correlation.
- [PS 1.3](E-w1-ps1.3-solutions.md) — Bias, variance, and the MSE decomposition of estimators.
- [PS 1.4](E-w1-ps1.4-solutions.md) — The Law of Large Numbers and the Central Limit Theorem.
- [PS 1.5](E-w1-ps1.5-solutions.md) — Power, size, and confidence intervals.

### Week 2 — The OLS engine *(numeric drills)*

- [PS 2.1](E-w2-ps2.1-solutions.md) — Matrix-OLS derivations and numerical inversion.
- [PS 2.2](E-w2-ps2.2-solutions.md) — Gauss–Markov: breaking the contract on purpose.
- [PS 2.3](E-w2-ps2.3-solutions.md) — Frisch–Waugh–Lovell: partialling-out by hand.
- [PS 2.4](E-w2-ps2.4-solutions.md) — Robust, clustered, and HAC standard errors.
- [PS 2.5](E-w2-ps2.5-solutions.md) — Omitted-variable-bias sign predictions and the measurement-error simulation.

### Week 3 — Causal inference: selection, matching, and IV *(numeric drills)*

- [PS 3.1](E-w3-ps3.1-solutions.md) — Potential-outcomes algebra and the selection-bias decomposition.
- [PS 3.2](E-w3-ps3.2-solutions.md) — Hand-matching, propensity scores, and the limits of selection-on-observables.
- [PS 3.3](E-w3-ps3.3-solutions.md) — Entropy-balancing weights and AIPW by hand.
- [PS 3.4](E-w3-ps3.4-solutions.md) — Instrumental variables: the 2SLS derivation and weak-IV diagnostics.
- [PS 3.5](E-w3-ps3.5-solutions.md) — Anderson–Rubin inference and the instrument-validity critique.

### Week 4 — Panel and design-based causal methods *(numeric drills)*

- [PS 4.1](E-w4-ps4.1-solutions.md) — The 2×2 difference-in-differences and event-study construction.
- [PS 4.2](E-w4-ps4.2-solutions.md) — Goodman-Bacon by hand, and the negative-weights crisis.
- [PS 4.3](E-w4-ps4.3-solutions.md) — Regression discontinuity: local-polynomial fitting and bandwidth experiments.
- [PS 4.4](E-w4-ps4.4-solutions.md) — Synthetic-control weights and placebo inference.
- [PS 4.5](E-w4-ps4.5-solutions.md) — Shift-share exposure weights and the identification critique.

### Week 5 — Asset pricing and the empirical-finance toolkit *(numeric drills)*

- [PS 5.1](E-w5-ps5.1-solutions.md) — Sorting, double-sorting, and the Fama–MacBeth horse race in Fama & French (1992).
- [PS 5.2](E-w5-ps5.2-solutions.md) — FF93 factor construction and time-series regressions.
- [PS 5.3](E-w5-ps5.3-solutions.md) — Momentum portfolio replication and the transaction-cost critique.
- [PS 5.4](E-w5-ps5.4-solutions.md) — Re-running Petersen's clustering comparison on a panel.
- [PS 5.5](E-w5-ps5.5-solutions.md) — Reproducing a Bertrand–Duflo–Mullainathan placebo-DiD false positive.

### Week 6 — Measurement from text and machine output *(numeric drills)*

- [PS 6.1](E-w6-ps6.1-solutions.md) — Building the KPSS patent-value measure: construction, validation, and critique.
- [PS 6.2](E-w6-ps6.2-solutions.md) — 10-K cosine similarity and a TNIC mini-build.
- [PS 6.3](E-w6-ps6.3-solutions.md) — The Loughran–McDonald dictionary vs. a naive dictionary.
- [PS 6.4](E-w6-ps6.4-solutions.md) — Fair-lending decomposition and the disparate-impact critique.
- [PS 6.5](E-w6-ps6.5-solutions.md) — An LLM classifier as a measurement instrument: held-out validation and a leakage audit.

### Week 7 — Launching the research project *(project deliverables — model exemplars)*

- [PS 7.1](E-w7-ps7.1-solutions.md) — Three candidate research questions, scored.
- [PS 7.2](E-w7-ps7.2-solutions.md) — A working data-pull script and data card for one project source.
- [PS 7.3](E-w7-ps7.3-solutions.md) — A complete pre-analysis-plan draft.
- [PS 7.4](E-w7-ps7.4-solutions.md) — A reproducible merged analysis dataset, with diagnostics.
- [PS 7.5](E-w7-ps7.5-solutions.md) — An identification memo and threats table.

### Week 8 — Robustness, write-up, and presentation *(project deliverables — model exemplars)*

- [PS 8.1](E-w8-ps8.1-solutions.md) — A specification curve for your main result.
- [PS 8.2](E-w8-ps8.2-solutions.md) — The full robustness battery and write-up.
- [PS 8.3](E-w8-ps8.3-solutions.md) — An A-grade introduction and headline-first results excerpt.
- [PS 8.4](E-w8-ps8.4-solutions.md) — A referee report and revise-and-resubmit memo.
- [PS 8.5](E-w8-ps8.5-solutions.md) — An eight-minute deck and one-click replication packet.
