# PS 3.1 — Potential-Outcomes Algebra & the Selection-Bias Decomposition

**Course:** 8-Week Empirical Finance Camp · Week 3 · Problem Set 3.1
**Covers:** Ch 3.1 (Potential Outcomes, SUTVA, and the Fundamental Problem of Causal Inference).
**Methods allowed:** only what is built through Ch 3.1 — the potential outcomes $Y_i(1)$ and $Y_i(0)$; the treatment indicator $D_i\in\{0,1\}$; the observation (consistency) rule $Y_i = D_i Y_i(1) + (1-D_i)Y_i(0)$; the individual treatment effect $\tau_i = Y_i(1) - Y_i(0)$; the Fundamental Problem of Causal Inference; the estimands $\text{ATE}=\mathbb{E}[\tau_i]$ and $\text{ATT}=\mathbb{E}[\tau_i\mid D_i=1]$; the naive difference in means $\Delta = \mathbb{E}[Y_i\mid D_i=1]-\mathbb{E}[Y_i\mid D_i=0]$; the master decomposition $\Delta = \text{ATT} + \big(\mathbb{E}[Y_i(0)\mid D_i=1]-\mathbb{E}[Y_i(0)\mid D_i=0]\big)$; SUTVA (no interference / no hidden versions); and the independence $(Y_i(0),Y_i(1))\perp\!\!\!\perp D_i$ that randomization buys. You do **not** need matching, weighting, instruments, or any regression machinery — those are Ch 3.2 onward. This sheet is the *algebra of counterfactuals*, nothing more.

**Total: 100 points.** Point values are stated per problem. Show your reasoning — a correct final number with no derivation earns roughly half credit, because the reasoning *is* the skill we are grading. Solutions are in Appendix E (`E-w3-ps3.1-solutions.md`); try every part before you look.

A note on the difficulty curve: Problem 1 is a five-minute warm-up on the observation rule. Problems 2 and 3 are the conceptual core — Problem 3 in particular asks you to *re-derive* the master decomposition from scratch, which is the single most important algebraic move of the week; do it until it is automatic. Problems 4 and 5 are the harder ones, where SUTVA and randomization get stress-tested. Problem 6 is a short conceptual essay that builds the bridge to Ch 3.2. Throughout, code outcomes as the chapter does (for a binary outcome, $1$ = the good event, $0$ = not), and remember that $\mathbb{E}[\,\cdot\mid D_i=1]$ means "average over the treated group only."

---

## Problem 1 — The observation rule and individual effects (12 points)

You have been handed a **science table** — a thing you can never have in real life, because it lists *both* potential outcomes for every unit. It comes from a (fictional) full-information audit of six of Maya's credit-counseling clients. The outcome $Y_i$ is the **gain in credit score** (in points) over the six months following the counseling window. $Y_i(1)$ is the gain if the client *attends* the counseling program; $Y_i(0)$ is the gain if she *does not*. The treatment actually taken is $D_i$.

| Unit $i$ | $Y_i(0)$ | $Y_i(1)$ | $D_i$ |
|:---:|:---:|:---:|:---:|
| 1 | $35$ | $45$ | $1$ |
| 2 | $20$ | $44$ | $0$ |
| 3 | $40$ | $52$ | $1$ |
| 4 | $25$ | $49$ | $0$ |
| 5 | $45$ | $53$ | $1$ |
| 6 | $30$ | $48$ | $0$ |

**(a) (4 pts)** Using the observation rule $Y_i = D_i Y_i(1) + (1-D_i)Y_i(0)$, write down the *observed* outcome $Y_i$ for each of the six units — the single number that would actually land in Maya's dataset. State clearly, for each unit, which potential outcome is *observed* and which is the *missing counterfactual*.

**(b) (4 pts)** Compute the individual treatment effect $\tau_i = Y_i(1) - Y_i(0)$ for all six units. Which client does the program help the most, and which the least?

**(c) (4 pts)** Here is the part that makes the Fundamental Problem concrete. Pretend you are Maya, who sees *only* the columns $D_i$ and $Y_i$ (not the two potential-outcome columns). Explain in two or three sentences why she cannot compute *any single* $\tau_i$ from her data, no matter how large her sample grows — and name precisely which entry of the table is, for unit 1 specifically, the one she can never see.

---

## Problem 2 — ATE versus ATT from the science table (16 points)

Stay with the exact same six-unit science table from Problem 1. Now we compute the population estimands — which we *can* do here only because we are playing God with both columns visible.

**(a) (4 pts)** Compute the **ATE** $=\mathbb{E}[\tau_i]$, averaging the individual effects over all six units. Interpret the number in one sentence in Maya's units (credit-score points).

**(b) (4 pts)** Compute the **ATT** $=\mathbb{E}[\tau_i\mid D_i=1]$, averaging $\tau_i$ over only the *treated* units (those with $D_i=1$). Then, for contrast, compute the average effect on the *untreated*, $\mathbb{E}[\tau_i\mid D_i=0]$ (sometimes called the ATC, the average treatment effect on the controls).

**(c) (4 pts)** You should find $\text{ATT} \neq \text{ATE}$. Explain in two or three sentences *what about this table* makes them differ — i.e., describe the pattern relating who got treated ($D_i$) to how much the program helps them ($\tau_i$), and say in words what kind of person seems to have selected into the program here.

**(d) (4 pts)** A credit union running this exact program wants to know "how much does our program help the people who actually use it?" Which estimand answers that question — ATE or ATT — and what is its value? In one further sentence, explain why a *different* number (the ATE) would be the right answer to the *different* question "should we make this program universal?"

---

## Problem 3 — Derive and apply the selection-bias decomposition (20 points)

This is the heart of the whole week. You will rebuild the master decomposition from the definitions, then turn it on a real-looking number.

**(a) (10 pts)** Starting from the naive difference in means, *derive* the master decomposition

$$
\underbrace{\mathbb{E}[Y_i\mid D_i=1] - \mathbb{E}[Y_i\mid D_i=0]}_{\Delta}
\;=\;
\text{ATT}
\;+\;
\underbrace{\big(\mathbb{E}[Y_i(0)\mid D_i=1]-\mathbb{E}[Y_i(0)\mid D_i=0]\big)}_{\text{selection bias}} .
$$

Do it in full, justifying each step. Your derivation must (i) use the observation rule to replace each observed conditional mean with the corresponding potential-outcome conditional mean; (ii) perform the "add and subtract $\mathbb{E}[Y_i(0)\mid D_i=1]$" move and say in one sentence *why that particular term*; and (iii) regroup into the ATT and the selection-bias term, identifying each by name. State clearly which step (if any) is an *assumption* and which steps are pure *definition/algebra*. (Hint: none of part (a) requires SUTVA-beyond-notation or randomization — it is an identity that *always* holds. That is the point.)

**(b) (6 pts)** Now apply it. Maya studies a credit union's auto-savings "round-up" feature (every card purchase rounds up to the nearest dollar and sweeps the difference into savings; enrollment is voluntary). Her outcome $Y_i$ is whether the member's next small-dollar loan is approved ($1$/$0$). She observes:

$$
\mathbb{E}[Y_i\mid D_i=1] = 0.70 \ \text{(approval rate among enrollees)}, \qquad
\mathbb{E}[Y_i\mid D_i=0] = 0.46 \ \text{(among non-enrollees)}.
$$

Suppose the *true* effect of the feature on the people who enrolled is $\text{ATT}=0.09$ (a fact Maya cannot observe, but which we hand you). Compute (i) the naive difference $\Delta$; (ii) the enrollees' missing counterfactual $\mathbb{E}[Y_i(0)\mid D_i=1]$; and (iii) the selection-bias term. Verify your three numbers satisfy the decomposition.

**(c) (4 pts)** Interpret the split for Maya in plain English. By what factor does her naive headline overstate the true effect on the treated? And explain, in one sentence, why collecting ten times more data would *not* fix her problem — naming which quantity in the decomposition is missing rather than merely imprecise.

---

## Problem 4 — Spot the SUTVA violation (16 points)

The potential-outcomes notation $Y_i(1), Y_i(0)$ quietly assumes SUTVA: (Part 1) *no interference* — one unit's treatment does not change another unit's potential outcomes; and (Part 2) *no hidden versions* — "treated" means one well-defined thing. For each scenario below, the researcher writes down a naive comparison as if SUTVA holds. State (i) whether SUTVA is violated and, if so, *which part*; (ii) the specific mechanism, named in potential-outcomes language (i.e., *whose* treatment is contaminating *whose* $Y_i(0)$ or $Y_i(1)$, or *why* the treatment is not a single well-defined condition); and (iii) one sentence on why randomizing $D_i$ would **not** rescue the study.

**(a) (5 pts)** Devon studies a one-time tax credit that subsidizes first-time crypto-asset purchases, to estimate its effect on adoption. The pilot covers a few hundred scattered individuals and prices do not budge. The legislature then scales the credit nationwide, and Devon wants to use his pilot estimate to predict the nationwide adoption effect. *(Focus your answer on the nationwide extrapolation.)*

**(b) (5 pts)** Priya evaluates whether "adopting an ESG disclosure standard" lowers a firm's cost of capital, coding $D_i=1$ for any firm that adopts. In her sample, some adopters publish audited, line-by-line emissions reports; others file a vague two-paragraph statement to check a box. She compares the average cost of capital of all $D_i=1$ firms to all $D_i=0$ firms.

**(c) (6 pts)** Sam runs a campus financial-literacy workshop and randomly assigns *which roommate in each two-person dorm* attends; the other is the control. He then compares the budgeting-quiz scores of attendees ($D_i=1$) to non-attendees ($D_i=0$). Attendees and their roommates cook, shop, and split bills together. *(Note: the assignment here genuinely is randomized — make sure your part (iii) explains why randomization still doesn't save it.)*

---

## Problem 5 — Randomization zeroes the selection bias (20 points)

Here you prove, on a tiny visible population, the central promise of the gold standard: that randomizing $D_i$ drives the selection-bias term to zero. Consider eight applicants. Four are "savvy" with untreated approval $Y_i(0)=1$, and four are "not" with $Y_i(0)=0$, so the population mean is $\mathbb{E}[Y_i(0)] = 0.5$. (We work with the $Y(0)$ column only, since that is the column the selection-bias term lives in.)

**(a) (4 pts)** *Self-selection world.* Suppose the four savvy applicants ($Y_i(0)=1$) all enroll and the four others ($Y_i(0)=0$) all stay out, so $D_i$ is perfectly determined by savviness. Compute $\mathbb{E}[Y_i(0)\mid D_i=1]$, $\mathbb{E}[Y_i(0)\mid D_i=0]$, and the selection-bias term. This is the worst case — comment in one sentence on what the value you get says about the comparison.

**(b) (5 pts)** *Balanced-coin world.* Now imagine assignment by a mechanism that places exactly two savvy and two non-savvy applicants in each arm (the "expected" outcome of a fair coin over this population). Recompute $\mathbb{E}[Y_i(0)\mid D_i=1]$, $\mathbb{E}[Y_i(0)\mid D_i=0]$, and the selection-bias term. Note that both group means now equal the population $\mathbb{E}[Y_i(0)]$.

**(c) (5 pts)** Connect the picture to the algebra. Randomization makes $(Y_i(0),Y_i(1))\perp\!\!\!\perp D_i$. Starting from that independence statement, show in two or three lines *why* it forces $\mathbb{E}[Y_i(0)\mid D_i=1] = \mathbb{E}[Y_i(0)\mid D_i=0] = \mathbb{E}[Y_i(0)]$, and therefore why the selection-bias term in the master decomposition is exactly zero. Conclude what $\Delta$ then equals.

**(d) (6 pts)** Two precise points about *expectation versus any one sample*.
&nbsp;&nbsp;(i) The chapter says randomization zeroes the bias "in expectation." Using the eight applicants of this problem, give a concrete *unlucky* split of four-treated/four-control in which the realized selection-bias term is **not** zero, and report its value.
&nbsp;&nbsp;(ii) In one or two sentences, explain why the leftover imbalance in (i) is a *precision* problem (sampling variation) and not a *bias* problem — and what happens to it as the population grows large. Contrast this with the self-selection bias of part (a), which more data does *not* shrink.

---

## Problem 6 — Why not "just control for $X$"? (16 points)

This problem is a short conceptual essay (no arithmetic) that builds the bridge from Ch 3.1 to Ch 3.2. Maya, having absorbed the selection-bias lesson, proposes a fix: "I'll run a regression of approval on the round-up feature and *control for* credit score, income, and employment status. Controlling for those makes the groups comparable, so the leftover difference is the causal effect."

**(a) (5 pts)** Restate Maya's hope in the language of this chapter. Write down the **conditional independence assumption** (also called unconfoundedness / selection on observables) in potential-outcomes notation, and translate it into one plain-English sentence about what must be true "within each value of $X$" for her plan to recover the causal effect.

**(b) (6 pts)** Explain the central catch in two or three sentences: *why is conditional independence an assumption the data cannot verify, and what single kind of variable, if it exists, breaks it?* Give one concrete example of such a variable in Maya's round-up setting that plausibly drives *both* who enrolls *and* whether the loan is approved, yet is absent from her dataset. Then say precisely what its presence does to the selection-bias term *conditional on $X$*.

**(c) (5 pts)** Contrast this with randomization in exactly one respect: explain why the coin handles the very variable that defeats "controlling for $X$," and why that difference is the deep reason an RCT is called the gold standard while a controlled regression is "a bet." End with one sentence naming what Ch 3.2 will do for a researcher who is *forced* to make that bet because randomization is off the table.

---

*End of PS 3.1. When you have attempted everything, check yourself against `book/appendices/E-solutions-manual/E-w3-ps3.1-solutions.md`. The numerical parts of Problems 1–3 and 5 can be confirmed in a few lines of Python (build the science-table arrays, take group means with boolean masks); you are encouraged to do so after working them by hand — and the simulation in `nb3.1` lets you watch the selection-bias term grow, shrink, and collapse to zero exactly as Problem 5 predicts.*
