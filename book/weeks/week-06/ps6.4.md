# Problem Set 6.4 — Fair-Lending Decomposition and the Disparate-Impact Critique

*Covers Ch 6.4 (Reader's Guide to Bartlett, Morse, Stanton & Wallace (2022) and Bhutta, Hizmo & Ringo) and builds directly on Week 2, Ch 2.5 (omitted-variable bias and the two-sign rule $\text{bias}=\beta_2\delta_1$), Week 3 (selection-on-observables), Week 4 (clean comparisons / design over controls), Mentor Session 4 (a disparity is not a finding; the over-controlling trap), and Gao & Sun (2019). Methods allowed: everything through Ch 6.4. As in the readings, **the point estimate is rarely the question** — the whole intellectual content of fair lending lives in deciding which controls are legitimate risk and which sit on the discrimination pathway, and in knowing which direction the omitted score moves your residual. You may treat every regression coefficient as already estimated; your job is to reason about what it means, decompose it by hand, and name the threat to each interpretation. Show your work; a boxed verdict with no argument earns no credit.*

**Total: 100 points.** Six tasks, escalating. Task 1 fixes the two legal definitions (disparate treatment vs. disparate impact) that the rest of the set turns on. Task 2 is a Blinder–Oaxaca-style decomposition **by hand**: split a raw rate gap into an "explained" piece and an "unexplained" residual from group means and a coefficient. Task 3 is an omitted-creditworthiness OVB task — drop the credit score and watch the residual inflate, read off the direction with the Week-2 two-sign rule. Task 4 is the **over-controlling trap**: control for a variable that lies *on* the discrimination pathway (the offered rate) and watch the measured discrimination wrongly vanish. Task 5 is the human-versus-algorithmic comparison (the Bartlett move and the BHR race-blind AUS benchmark). Task 6 is a critique / spec-discipline task: name the threat and the design, tie to Gao & Sun (2019) and Capstone 1.

A reminder on the one idea that runs through the whole set, because it *is* the lesson of both papers. A raw gap confounds *the same rule applied to groups that differ in legitimate factors* with *a different rule applied to the same factors*; only the second is discrimination. Every control you add is a bet about which of those two stories you are removing. Hold fixed a genuine **confounder** (legitimate risk a fair lender is allowed to price) and the residual gets *closer* to differential treatment. Hold fixed a variable **on the pathway** (a channel through which the discrimination itself operates) and you regress away the very thing you are hunting. The arithmetic of a decomposition is easy; deciding which bucket each variable belongs in is the entire job. Carry that sentence into every task below.

A note on numbers. Every figure in this set — rate gaps in basis points, group means, coefficients, approval-rate gaps — is a **labeled illustrative value**, chosen to be round and pedagogically clean and to reproduce the *qualitative* pattern the two papers established (a large raw gap; legitimate risk explains much of it; a contested residual survives; algorithms shrink the human-discretion channel without eliminating the gap). They are **not** transcribed from Bartlett et al.'s or BHR's tables, and you must not cite them as such. When you run **nb6.4** you will generate your own on public HMDA data.

---

## Task 1 — Two definitions of discrimination (12 points)

Maya keeps two news clippings on her desk. The first: *"Lender charges minority borrowers 8 basis points more than identical white borrowers."* The second: *"Lender's automated credit-scoring model approves a smaller share of minority applicants, even though no input to the model is race."* She suspects these are not the same accusation, and the law agrees.

**(a) (4 pts)** Define **disparate treatment** and **disparate impact** in one careful sentence each, in the fair-lending context. For each, state what is being compared and what would count as a violation. (Hint: one is about a *different rule applied to the same inputs*; the other is about a *facially neutral rule that produces worse outcomes for a protected group*.)

**(b) (4 pts)** Classify each clipping. Which accusation is a disparate-*treatment* claim and which is a disparate-*impact* claim? For the second clipping in particular, explain why "no input is race" does **not** by itself clear the lender of a disparate-impact problem.

**(c) (4 pts)** Ch 6.4 says BHR's race-blind automated-underwriting-system (AUS) benchmark "measures *disparate treatment* and says little about disparate *impact*." Explain in two or three sentences why a small residual *after* conditioning on the credit score is reassuring about disparate treatment yet nearly silent about disparate impact — and why "a credit score shaped by historical inequities" is exactly the seam between the two definitions.

---

## Task 2 — A Blinder–Oaxaca decomposition by hand (22 points)

This is the workhorse the BHR reading calls "watch the race coefficient march across columns," made fully explicit. We will split a raw group gap into an **explained** part (the two groups differ in a legitimate factor, and that factor is priced the same for everyone) and an **unexplained** residual (what is left after the legitimate factor is accounted for). All numbers are illustrative.

Maya studies the offered mortgage rate (in **basis points above a benchmark**, so larger = more expensive) for two groups, $D=1$ (a protected minority group) and $D=0$ (the reference group). She has the **group mean rates** and the **group mean of one legitimate risk factor**, the loan-to-value ratio (**LTV**, in percent), which a fair lender is allowed to price. Suppose both groups face the *same* pricing slope on LTV, an estimated $\hat\beta_{\text{LTV}} = 2.0$ basis points of rate per 1 percentage point of LTV (riskier, higher-LTV loans cost more — legitimately).

| Group | Mean rate (bps over benchmark) | Mean LTV (%) |
|---|---|---|
| $D=1$ (minority) | 168 | 88 |
| $D=0$ (reference) | 150 | 82 |

**(a) (3 pts)** Compute the **raw rate gap**, $\overline{\text{rate}}_{D=1} - \overline{\text{rate}}_{D=0}$, in basis points. This is the alarming "before" number — the disparity, not yet a finding.

**(b) (6 pts)** Compute the **explained** part of the gap: the portion attributable to the two groups differing in LTV, priced at the common slope. The formula is
$$
\text{explained} = \hat\beta_{\text{LTV}} \cdot \big(\overline{\text{LTV}}_{D=1} - \overline{\text{LTV}}_{D=0}\big).
$$
Show the subtraction and the multiplication. In one sentence, say in plain English what this number represents — i.e., why a fair lender pricing LTV identically for both groups would *still* produce part of the observed gap.

**(c) (4 pts)** Compute the **unexplained** residual as $\text{raw gap} - \text{explained}$. This is the Blinder–Oaxaca residual — the analogue of the surviving race coefficient in a conditional regression. State what it represents and why it is the number a fair-lending case actually turns on.

**(d) (4 pts)** Re-derive the same residual a second way to check the arithmetic: it must equal the gap in **risk-adjusted** rates, i.e. the difference in each group's mean rate *after* subtracting the legitimately-priced LTV component $\hat\beta_{\text{LTV}}\cdot\overline{\text{LTV}}_{\text{group}}$. Compute each group's risk-adjusted mean rate and confirm their difference equals your answer to (c). (This is the by-hand version of "add the control and read the coefficient.")

**(e) (5 pts)** Suppose a referee says: "Your explained part assumes the LTV slope is the *same* for both groups; a full Blinder–Oaxaca decomposition also allows the two groups to face *different* slopes, which adds a third, 'coefficients' term." In two or three sentences, explain (i) what it would *mean*, substantively, for the two groups to face different LTV slopes, (ii) why that third term is itself a candidate piece of discrimination rather than a nuisance to be netted out, and (iii) why, for this simple two-task purpose, folding everything beyond the explained part into a single "unexplained" residual is a conservative and defensible reading.

---

## Task 3 — Omitted creditworthiness: the residual inflates (18 points)

Now connect the residual of Task 2 to the Week-2 machinery directly. HMDA — the public data the camp can actually touch — is *blind to the credit score*. So the realistic decomposition omits a legitimate risk factor that both drives the rate **and** differs across groups. Use the OVB formula from Ch 2.5: the short (score-omitted) regression's coefficient on the minority indicator $D$ converges to
$$
\hat{\tilde\beta}_D \xrightarrow{p} \beta_D + \beta_{\text{score}}\,\delta,
\qquad \delta = \frac{\operatorname{Cov}(D,\ \text{score})}{\operatorname{Var}(D)},
$$
where $\beta_D$ is the *true* differential-treatment effect we want, $\beta_{\text{score}}$ is the effect of the omitted credit score on the rate, and $\delta$ is the slope of score on $D$ (the "auxiliary regression").

Throughout, "rate" is coded so that **higher = more expensive**, and a higher **credit score means lower risk and thus a lower rate**, so $\beta_{\text{score}} < 0$. In Maya's sample the minority group $D=1$ has, on average, a **lower** credit score than the reference group (the legacy of unequal credit access discussed in Ch 2.5), so regressing score on $D$ gives a negative slope, $\delta < 0$.

**(a) (5 pts)** Apply the **two-sign rule**. State the sign of $\beta_{\text{score}}$ and the sign of $\delta$ with the one-sentence reason for each, multiply, and report the sign of the bias term $\beta_{\text{score}}\,\delta$. Then state, in plain English, which direction omitting the credit score pushes the measured minority rate premium: does the score-omitted residual **overstate** or **understate** the true differential-treatment effect $\beta_D$?

**(b) (5 pts)** Put numbers on it (illustrative). Suppose the true differential-treatment effect is $\beta_D = 4$ bps, the score effect is $\beta_{\text{score}} = -0.5$ bps per credit-score point, and the auxiliary slope is $\delta = -20$ score points per unit of $D$ (the minority group averages 20 points lower). Compute the probability limit of the score-omitted coefficient $\hat{\tilde\beta}_D$. By how many basis points does dropping the score inflate the apparent premium? Relate this back to the Task-2 "unexplained residual": which of these two numbers ($\beta_D$ vs. $\hat{\tilde\beta}_D$) is the HMDA-only researcher actually estimating?

**(c) (4 pts)** This is the BHR move stated as a prediction. BHR *get* the score (and a near-complete underwriting file) where the HMDA literature could not. Using your sign from (a), predict what happens to the estimated minority coefficient when the score is **added** to the regression — does it shrink toward zero or grow? Explain why BHR can therefore claim that "much of what earlier studies called unexplained was omitted-variable bias all along," and why this is the OVB of Week 2 *measured* rather than feared.

**(d) (4 pts)** A subtle limit, straight from Ch 6.4 §6. Even after adding the score and the full file, BHR's residual is "still a bound, not a clean causal effect." Name the *remaining* omitted variable that a near-complete file still cannot capture (the thing a human underwriter sees that no dataset records), and state in one sentence why its presence means the surviving residual is a **lower** bound on the true differential treatment if that soft information is itself correlated with race in the disfavored direction. (Connect to the residual list at the end of Ch 2.5.)

---

## Task 4 — The over-controlling trap: discrimination that wrongly vanishes (18 points)

The mirror-image danger. Task 3 was about *too few* controls (omit the score, residual inflates). This task is about the *wrong* control — one that sits **on the discrimination pathway** rather than off it. This is Mentor 4's warm-up 3, and it is the trap Bartlett et al. walk a knife's edge to avoid.

Maya wants the total effect of being in group $D=1$ on the final **interest rate**. Consider this causal sketch of how a discriminatory lender might operate:
$$
D \ (\text{minority}) \;\longrightarrow\; \text{higher offered/quoted rate} \;\longrightarrow\; \text{higher final interest rate}.
$$
That is, suppose part of how discrimination *operates* is that minority applicants are quoted worse rates, which then mechanically determine the final rate they pay. The **offered rate** is therefore a **mediator** — a variable on the causal path from $D$ to the outcome — not a pre-existing confounder.

Suppose (illustrative) that without the offered rate as a control, the estimated minority coefficient on the final rate is **+6 bps** and strongly significant. Maya, wanting to "be thorough," adds the offered rate as a control. The minority coefficient collapses to **+0.3 bps**, statistically indistinguishable from zero.

**(a) (5 pts)** Explain precisely why adding the offered rate makes the measured discrimination *wrongly vanish*. Use the language of mediators and the path diagram: what does conditioning on a variable that lies *on* the $D \to \text{outcome}$ path do to the coefficient on $D$? Why is the resulting +0.3 bps an **understatement** of discrimination rather than a more careful measurement of it?

**(b) (4 pts)** Contrast this explicitly with Task 2/Task 3, where adding a control (LTV; the credit score) was the *right* thing to do. State the one-sentence test that separates a control you **should** add from one you **must not** add — the "confounder I should hold fixed, or channel I should not?" question from Ch 6.4 §6. Apply it to three candidate controls: (i) the credit score, (ii) the loan-to-value ratio, (iii) the lender's internal "risk grade" that is itself assigned partly on the basis of the loan officer's discretion. For each, say whether it is a legitimate confounder or a pathway variable, and why.

**(c) (5 pts)** This is why Ch 6.4 calls Bartlett et al.'s use of the **GSE pricing formula** so clever, and why it keeps them "on safe ground." Explain how conditioning on the *published GSE risk inputs* (credit score, LTV, etc.) differs from conditioning on a *steered product type* or a *discretionary internal grade*. Why are the GSE inputs legitimate confounders — "all the legitimate risk and nothing on the discrimination pathway" — whereas a steered product is a pathway variable? Why does the danger of the over-controlling trap *grow* with every "richer" control added in the name of precision?

**(d) (4 pts)** Write the Ch 6.4 §4 identifying-assumption sentence for the *clean* specification (the one that does **not** over-control), in the CONVENTIONS §4 format. That is, complete: "The conditional minority rate gap equals differential treatment as long as ____ and ____." Name the threat in the first blank (what the conditioning set must capture) and the over-controlling danger in the second (what must *not* be in the controls).

---

## Task 5 — Human versus algorithmic: does the machine cure it? (16 points)

This is the question that makes Ch 6.4 a Week-6 chapter and not a re-run of Week 4: *if a computer makes the lending decision instead of a loan officer, does the discrimination go away?* Both papers put the algorithm on trial. Below are **illustrative** conditional minority rate gaps (in basis points, after the legitimate risk controls), split by lender technology — the public-data analogue of Bartlett et al.'s headline FinTech-versus-traditional contrast.

| Lender type | Conditional minority rate gap (bps) |
|---|---|
| Traditional (face-to-face, loan-officer discretion) | 8.0 |
| FinTech (algorithmic pricing, no human in the loop) | 5.0 |

**(a) (5 pts)** State the *hoped-for* answer the chapter names — "algorithms are blind, so they do not discriminate" — and explain why it is a **hypothesis to test, not an assumption to make**. Then read the table: does removing the human eliminate the gap, shrink it, or leave it unchanged? Write the one-sentence robust finding from Ch 6.4 §4 that this pattern illustrates.

**(b) (4 pts)** Decompose the mechanism. The traditional gap (8.0) exceeds the FinTech gap (5.0). Attribute the **3.0-bp difference** to one channel and the **5.0-bp residual** to another. Name each channel: which part is plausibly *human-discretion* discrimination (the face-to-face mechanism that algorithmic pricing removes), and which part survives even with no human in the loop? For the surviving 5.0 bps, give the two mechanisms Ch 6.4 offers for how an algorithm with no race input can *still* produce a gap.

**(c) (4 pts)** Now the BHR companion idea, on the *acceptance* margin. Explain what the **race-blind AUS** (automated underwriting system) provides that a regression cannot: why is "what the race-blind algorithm *would* have decided" a *mechanical counterfactual* for the "same-quality applicant, vary only the protected trait" comparison that Ch 3.1 says you can never directly observe? In one sentence, say what comparing *actual* denials to *AUS-recommended* decisions isolates (what the rule says vs. what the human did on top of it).

**(d) (3 pts)** Tie the two papers together as the chapter does: Bartlett et al. live on the **pricing** margin, BHR primarily on the **acceptance** margin. Explain in two sentences why a complete fair-lending verdict needs **both** margins — specifically, how a lender could "launder" discrimination from one margin to the other, so that a paper examining only one margin could declare the market clean while the disparity simply moved.

---

## Task 6 — Critique and spec discipline: name the threat, name the design (14 points)

This is the referee's task, and the bridge to **Capstone 1**. You will produce the full spec-discipline statement and the honest critique that Ch 6.4 demands.

Maya drafts the following claim for her capstone: *"On a HMDA extract, the conditional rate-spread gap for minority borrowers is 5 bps after controlling for loan amount, applicant income, and tract and lender fixed effects; this is the causal effect of race on price."*

**(a) (5 pts)** Rewrite Maya's specification in the **CONVENTIONS §4 format**, naming explicitly: **outcome · key regressor · controls · fixed effects · clustering · sample · the identifying assumption in one sentence.** (You may choose reasonable illustrative values for any field Maya left unstated, e.g. clustering and sample, but you must state them — that is the point of the discipline.)

**(b) (4 pts)** Attack the claim the way a referee will, naming **two** distinct threats from Ch 6.4 §6 and saying which direction each biases the 5-bp estimate. At minimum, one must be the **omitted credit score** (Task 3 — HMDA cannot see it; which way does it move the coefficient, and is 5 bps therefore too big or too small as an estimate of differential treatment?). For the second, choose either the over-controlling trap (Task 4) or the disparate-treatment-vs-disparate-impact ambiguity (Task 1), and state precisely what is wrong and how to fix or hedge it. Conclude with the corrected one-sentence claim Maya *should* write (replace "this is the causal effect of race on price" with an honest, bounded statement).

**(c) (5 pts)** Connect to **Gao & Sun (2019)** and **Capstone 1**, as Ch 6.4's closing does. Gao & Sun's same-sex-borrower work faced *exactly* HMDA's missing-credit-score problem and let a **design** — not a longer list of controls — carry the argument. (i) Name the design move that substitutes for the unavailable score when more controls cannot fix the problem (Ch 6.4 §7 Exercise 2 and the chapter's closing): matching, and/or a policy-change difference-in-differences. (ii) Explain in two sentences why a *design* can succeed where adding controls fails — i.e., what a clean comparison or a policy DiD buys you that a kitchen-sink regression on HMDA cannot, given that the score is *fundamentally unobserved* in the data. (iii) State the one confound a within-pair matched comparison on HMDA *still* cannot fix (Ch 6.4 §7 Exercise 2), so that you carry into Capstone 1 a design that names the threat it has *not* closed.

---

*End of PS 6.4. Solutions in `book/appendices/E-solutions-manual/E-w6-ps6.4-solutions.md`. This set is the active-replication companion to Ch 6.4 (Reader's Guide to Bartlett, Morse, Stanton & Wallace (2022) and Bhutta, Hizmo & Ringo) and the direct sequel to **Week 2, Ch 2.5** (the OVB two-sign rule, with the very same creditworthiness example) and **Mentor Session 4** (a disparity is not a finding; the over-controlling trap). The Blinder–Oaxaca decomposition you did by hand in Task 2 is what `nb6.4` automates on public HMDA data; the over-control of Task 4 and the matched comparison of Task 6 are two of its three exercises. The whole set points at **Capstone 1**: take exactly this question — are two otherwise-identical applicants treated differently? — from a HMDA extract to a design that could survive a hostile referee, a regulator, and a court, precisely *because* the credit score is missing, exactly as Gao & Sun (2019) did. Go run nb6.4 (mortgage-disparity decomposition) and generate your own version of every illustrative table above.*
