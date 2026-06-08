# D.3 — Robustness Sections That Persuade

D.1 and D.2 governed the tables. This section governs the part of the paper that surrounds your robustness *tables* with the argument that makes them land: the **robustness section.** You have already done the analytic work — in Chapter 8.2 you ran the placebos, re-clustered the standard errors, swept the bandwidths and the winsorizing thresholds, computed the Oster (2019) $\delta$ for the confounder you could not measure. What you have is a folder of checks. What you do *not* yet have is a section of a paper, and the gap between those two is the subject of this appendix. A robustness section is not a dump of every extra regression you happened to run; it is an *argument*, organized around a skeptic's doubts, that earns belief.

The reveal that organizes everything below, stated once. **A robustness check that no one asked for persuades no one; a check that answers a threat a referee was about to raise disarms the attack before it lands.** This is the sentence from Ch 8.3 §6, and it is the whole craft. The difference between a persuasive robustness section and an unpersuasive one is not the *number* of checks — it is whether each check is visibly an *answer to a specific, named doubt.* The doubts are not yours to invent on the spot; you wrote them down in Chapter 7.5, in the threats-and-responses table. The robustness section is that table, cashed out. This is why the whole arc of the capstone hangs together: the memo names the threats, Chapter 8.2 runs the responses, and this section presents them as the answers they always were.

---

## 1. Organize around the threats table, not the regression list

The structural decision that makes or breaks a robustness section is the *ordering principle*. There are two, and only one is right.

The wrong one is to organize by *what you ran*: "Section 6.1 reports alternative clustering. Section 6.2 reports a placebo test. Section 6.3 reports the Oster bound." This is a regression list. It puts the burden on the reader to figure out, for each check, *which doubt it is supposed to settle* — and a reader who has to do that work is a reader losing patience.

The right one is to organize by *the reader's doubts* — which is to say, by your Chapter 7.5 threats table. Each subsection takes **one named threat** and shows the check that addresses it, in the order a skeptic would raise them. The threats table already put your rows in descending order of danger (Ch 7.5 §3), so the robustness section inherits that order: lead with the check that answers your *most dangerous* threat, the one a seminar audience asks about in the first ninety seconds. The section then reads as a conversation in which you anticipate every objection and meet it before it is spoken.

The mechanical move that signals this organization is a sentence template, used once per threat, that does three things in the reader's order:

> "A reader might worry that **[named threat]**; we **[the check]**, and **[the reassuring result]** (Table N)."

For Maya: *"A reader might worry that adopting states were already on a differential denial-gap trajectory; we estimate the event study and find pre-treatment leads that are flat and statistically indistinguishable from zero (Figure 3)."* That sentence names the threat, reports the check, and states the result — in the order the reader would *attack*, so the attack is answered before it forms. Robustness sections that persuade are built of these sentences, one per row of the threats table.

---

## 2. The threats-and-responses table format, as it appears in the paper

The threats-and-responses table you built for the identification memo (Ch 7.5 §3) reappears in the paper, sometimes as an actual table and always as the *skeleton* of the prose. Its four columns are unchanged, because their rigid shape is what forces honesty:

| Column | What goes in it |
|---|---|
| **Threat** | The named failure of the identifying assumption — from the design's standard menu (Ch 7.5 §2), in one phrase. **Never "endogeneity."** |
| **Why it's plausible** | One sentence on the concrete story under which the threat is *real in your setting.* A threat with no plausible story is a strawman and does not belong. |
| **What we do about it** | The specific test, design choice, or robustness check — the Chapter 8.2 result that answers this row. |
| **Residual concern** | What still worries you after column 3. The honest leftover. **A blank here is a tell, not a triumph.** |

In the *paper*, the table's third column is no longer a promise ("we will run a placebo") but a *result* ("the placebo ATT is 0.1pp, indistinguishable from zero, Table 5"). That is the entire transformation from memo to paper: column 3 comes due. And the fourth column survives into the paper intact, because the residual concern is the part a good mentor reads first. A robustness section whose every residual is "none" is *less* credible, not more — every real observational design has residual concerns, and a reader who sees none assumes you did not look hard enough (Ch 7.5 §3, §5). The point of the section is not to claim the threats are vanquished; it is to show you *saw* them, *engaged* them, and *bounded* what remains.

---

## 3. Reporting the actual checks, honestly

Each kind of robustness check from Chapter 8.2 has an honest way to report it. The discipline is the same throughout: state the threat, state what a *pass* would look like *before* you report the result, then report the result whether or not it passed.

**Alternative standard errors.** Report the small SE table from Ch 8.2 §1 — the same point estimate under classical, unit-clustered, treatment-level-clustered, and two-way-clustered SEs — and read it top to bottom. The honest reading is that the conservative, defensible clustering is the truth and the classical SE is a fantasy. *Pass:* the confidence interval excludes zero even under the most conservative defensible clustering. *Honest fail:* "significant under state clustering but not under two-way clustering" — and then you say the result is *fragile* on inference, plainly. For a design with few treated clusters, the wild cluster bootstrap (Ch 8.2 §1) is the honest inference, not the default clustered SE; if they disagree, you report the bootstrap and you do not keep the stars the conventional SE gave you.

**Placebos.** Report the in-time placebo (fake treatment date in the pre-period), the in-space placebo (permute treatment across never-treated units), and the placebo outcome (an outcome the mechanism cannot move). State the prediction your design makes — *you should find nothing* — and then report what you found. *Pass:* the placebo effect is small and indistinguishable from zero, real (if asymmetric) support for your assumption. *Honest fail:* a placebo lights up, and there is no spin that survives it — "the design cannot separate the treatment from a pre-existing trend", stated plainly, and either a redesign or a result reported as uninterpretable. A robustness section that omits the obvious placebo reads as evasive, because the referee runs it in their head whether or not you ran it on paper (Ch 8.2 §2).

**Sensitivity / specification.** Report how the estimate moves as you wiggle the defensible knobs — the RD bandwidth, the control set, the winsorizing threshold, the subsample (Ch 8.2 §3). The standard display is a sensitivity plot or a short table across the range. *Pass:* the estimate is flat and stays significant across the defensible range. *Honest fail:* the estimate swings, or lives only in a narrow window of the knob you happened to pick — then the honest claim is *narrower* than the one you wanted ("the effect holds outside the crisis window but is not separately identified within it"), and narrowing the claim to what the data support is the entire job, not a defeat.

**Oster $\delta$ (selection on unobservables).** This is the deepest check, because it confronts the one threat that *cannot* be tested directly — a confounder you never measured (Ch 8.2 §5). Report it honestly, which means reporting three things, not one. First, the $\hat\delta$ — *"an omitted confounder would have to be 4.7 times as correlated with treatment as our rich observables to nullify the estimate ($\hat\delta = 4.7 \gg 1$)."* Second, the $R_{\max}$ you assumed and a sensitivity sweep, because $\hat\delta$ is mechanically sensitive to $R_{\max}$ and a $\delta$ reported without its $R_{\max}$ is uninterpretable — state that you used Oster's default $R_{\max} = 1.3\,\tilde R_1$ and show how $\hat\delta$ moves when you push $R_{\max}$ to 1. Third, the honest framing: $\delta$ is *not* a p-value; it measures robustness to a specific untestable threat, not statistical significance, and a result can be wildly significant yet fragile to confounding ($\hat\delta = 0.3$) or modestly significant yet hard to confound ($\hat\delta = 5$). *Pass:* $\hat\delta \ge 1$ and the bounding set excludes zero. *Honest fail:* $\hat\delta = 0.4$ means a confounder *weaker* than your observables could erase the result, and that belongs in your limitations, stated plainly — the test found the vulnerability before a referee did, and you say so (Ch 8.2 §5).

Throughout, the non-negotiable reporting rule is the one from Ch 8.2: **state what a pass looks like before you report the result.** Writing the pass criterion first removes your freedom to redefine "pass" after seeing the number — the same garden-of-forking-paths discipline (Ch 1.5, Ch 7.3) that the pre-analysis plan enforces, applied to your own robustness battery.

---

## 4. When a result does not fully survive

This is the part of the craft that most distinguishes an honest empiricist from a salesperson, and the rule is blunt: **a result that does not survive a check is reported as not surviving.** A failed robustness test is a *finding*, not a setback to be buried (Ch 8.2 §6). The author who runs a check hoping it passes and the author who runs it hoping to learn the truth get the same code and the same output — but only the second is doing science.

There is a spectrum of "not fully surviving", and each point on it has an honest sentence:

- **The point estimate holds but precision collapses.** "The point estimate is −1.4pp, but with few treated clusters the wild cluster bootstrap cannot reject zero; we report the result as suggestive, not significant." You do not keep the three stars the conventional SE gave you.
- **The effect holds in part of the sample.** "The effect is robust outside the 2008–2009 crisis window but is not separately identified within it." The claim narrows to the subsample the data support.
- **The effect survives the number but not the design.** This is the distinction §5 is about, and it is the one a sophisticated reader cares most about — a result can be perfectly *stable* across every robustness check and still rest on an *invalid identifying assumption.* Robustness is not identification.
- **The effect does not survive at all.** A placebo lights up; the design cannot separate the treatment from a pre-trend. There is no honest spin. You report the failure, and you redesign or report the result as uninterpretable.

The reason candor wins is verifiable and not sentimental. A referee will think of the residual concern whether or not you write it; *writing it first robs the attack of its force* (Ch 7.5 §5). A reader trusts a paper that flags its own fragility far more than one that pretends to none, because the flagged fragility is evidence that the author looked hard, and the unflagged one is evidence only that they did not — or did, and hid it. The verbs follow the evidence here too (D.5): a check that half-survives downgrades your claim from "we show" to "we find suggestive evidence", and the prose must move with it.

---

## 5. Robustness is not identification

Hold this distinction at the center of the section, because conflating the two is the most sophisticated mistake a strong student makes. **Robustness asks: does the number move when I change the analysis? Identification asks: is the research design valid in the first place?** They are different questions, and passing one does not answer the other.

A coefficient can be magnificently robust — stable across every control set, every clustering, every bandwidth, every winsorizing threshold, with an Oster $\hat\delta$ of 6 — and still be *biased*, because the identifying assumption is false. If treated and control states were never on parallel trends, then no amount of re-clustering or re-winsorizing fixes the DiD; the bias is baked into the design, and robustness checks only confirm that the *biased* number is stable. Robustness tells you the number is not an artifact of arbitrary analytic choices. It says nothing about whether the number is the *causal effect you claim*, because that is a property of the design, defended by the identifying assumption (Ch 7.5), not of the analysis.

The practical upshot for the section: do not let a thick robustness section substitute for the identification argument. The empirical-design section (Ch 8.3 §5) carries the identification — it names the assumption and the threat in the CONVENTIONS §4 form. The robustness section carries the *defense of that argument against specific named threats* — and crucially, some of those threats are about identification (a differential pre-trend attacks parallel trends itself) and some are only about inference or analytic choice (the clustering level, the winsorizing threshold). A persuasive section keeps the two visible: it shows which checks defend the *design* (placebos against pre-trends, the Goodman–Bacon decomposition against forbidden comparisons, the Oster bound against unobserved confounding) and which merely show the *number is stable* (clustering, winsorizing, bandwidth). A reader who can see that you understand the difference trusts the section; one who sees a thick pile of stability checks offered as if they proved the design valid is being sold something, and a Week-5-trained reader knows it.

---

## 6. The robustness-section checklist

Run your robustness section against this before it enters the manuscript:

- The section is **organized around the threats table** (Ch 7.5), one subsection per named threat, in **descending order of danger** — not organized as a list of regressions.
- Each threat is introduced with the **"a reader might worry… we… and…"** move: named threat, check, reassuring result, table reference.
- Every threat is **named specifically** (pre-trend, weak instrument, manipulation, unobserved confounder), **never "endogeneity."**
- For each check, the **pass criterion is stated before the result** is reported.
- **Standard-error alternatives** report the multi-clustering table; the **wild cluster bootstrap** is the honest inference where treated clusters are few.
- **Placebos** state the no-effect prediction and report it whether it passed; the obvious placebo is not omitted.
- **Sensitivity** sweeps the defensible range of each knob; a result that lives in a narrow window is reported as such.
- **Oster $\delta$** reports $\hat\delta$, the assumed $R_{\max}$ with a sensitivity sweep, and the framing that $\delta$ is robustness-to-confounding, not a p-value.
- **Results that do not fully survive are reported as not surviving**, with the claim narrowed and the verbs (D.5) downgraded to match.
- **Every residual concern is stated** — no "none"; the residual-concern column is substantive.
- The section keeps **robustness and identification distinct**: stability checks are not offered as proof the design is valid.

The thread that ties D.3 back to the rest of Appendix D, and back to Week 5: *the skeptic who reads a stranger's table and the author who builds an honest one are the same person.* You spent Weeks 5–6 learning to find a published author's softest assumption and to ask which robustness check they ran that most reassured you — and which they *should* have run but did not (the Week-5 self-check rubric). The robustness section is you doing that to yourself, on purpose, on the page, before a referee gets the chance. The companion sections close the loop: **D.1** and **D.2** built and reported the tables this section defends; **D.4** is the replication-packet standard that lets a skeptic re-run every check here on their own machine; and **D.5** is the prose style — hedging, calibrated causal verbs, citing primary sources — in which the whole defense is written. A robustness check, run honestly, and a hedge, written honestly, are the same act of intellectual honesty, performed in two registers.
