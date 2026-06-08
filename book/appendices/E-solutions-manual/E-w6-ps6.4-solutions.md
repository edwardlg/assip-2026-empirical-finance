# Solutions — Problem Set 6.4 (Fair-Lending Decomposition and the Disparate-Impact Critique)

*Full worked solutions to `book/weeks/week-06/ps6.4.md`. Notation follows CONVENTIONS §3, Ch 2.5 (OVB), and Ch 6.4. The decomposition object is a raw group gap $\Delta = \overline{y}_{D=1}-\overline{y}_{D=0}$ split into an **explained** part $\hat\beta_X(\overline{X}_{D=1}-\overline{X}_{D=0})$ (Blinder–Oaxaca, common-coefficient version) and an **unexplained residual** $\Delta-\text{explained}$. The OVB machinery is $\hat{\tilde\beta}_D\xrightarrow{p}\beta_D+\beta_{\text{score}}\delta$ with $\delta=\operatorname{Cov}(D,\text{score})/\operatorname{Var}(D)$ (Ch 2.5). Citations by name: Bartlett, Morse, Stanton & Wallace (2022); Bhutta, Hizmo & Ringo; Gao & Sun (2019); also Blinder (1973) and Oaxaca (1973) for the decomposition. **Every numerical figure is the labeled illustrative value from the problem set**, chosen to reproduce the qualitative pattern of the two papers (large raw gap, much explained by legitimate risk, a contested residual surviving, algorithms shrinking but not closing the gap) — not transcribed from any published table. All decomposition arithmetic is verified at the foot of Task 2.*

---

## Task 1 — Two definitions of discrimination (12 pts)

**(a) (4 pts)**

**Disparate treatment** is *intentionally* (or at least overtly) applying a **different rule to applicants who are identical on the legitimate inputs**, on the basis of a protected trait — comparing two applicants matched on everything a lender may lawfully price (score, LTV, income, …) and finding that the protected one is charged more or denied more. The violation is the different treatment of like-for-like applicants.

**Disparate impact** is a **facially neutral rule — applied identically to everyone — that nonetheless produces systematically worse outcomes for a protected group**, and that is not justified by business necessity. The comparison is between *group outcomes* under one common rule; the violation is the unjustified adverse effect, regardless of intent or of whether the protected trait is an input.

The crisp contrast the hint wants: disparate treatment = *a different rule applied to the same inputs*; disparate impact = *the same (neutral) rule producing different outcomes*.

**(b) (4 pts)** The **first clipping** ("8 bps more than *identical* white borrowers") is a **disparate-treatment** claim: it asserts that like-for-like applicants — identical on the legitimate inputs — are priced differently by race, which is the different-rule-to-same-inputs story.

The **second clipping** ("model approves a smaller share of minority applicants, even though no input is race") is a **disparate-impact** claim: one neutral rule (the scoring model), applied to everyone, yields worse group outcomes for the protected group.

"No input is race" does **not** clear the lender, because disparate impact is about the *effect* of a neutral rule, not its intent or its literal inputs. A model can use variables — zip code, the credit score itself, account history — that are correlated with race and that carry the imprint of historical inequities, so the rule lands harder on the protected group even with race formally excluded. Disparate-impact law asks whether that adverse effect is justified by business necessity, not whether race was typed into the model. (Bartlett et al.'s own worry — that an algorithm prices on *geography that proxies for race* — is exactly a disparate-impact channel that survives the removal of race as an input.)

**(c) (4 pts)** BHR's race-blind AUS is, by construction, a rule that *cannot see race*, so comparing actual decisions to what the AUS recommended isolates whether a human applied a *different* rule to like applicants — that is a **disparate-treatment** test, and a small residual after conditioning on the score says the human did *not* deviate much from the neutral rule. But that says almost nothing about disparate *impact*, because the neutral rule itself — the credit score and the AUS built on it — may produce worse outcomes for the protected group *and still pass the treatment test*. The seam is precisely the credit score: if the score is shaped by historical inequities (unequal access to credit-building, thin files, redlining's long tail), then conditioning on it *removes* a disparate-treatment concern while *being itself* the channel of disparate impact. Reassuring about treatment, nearly silent about impact — and a single number cannot answer both legal questions at once, which is why Ch 6.4 says to state *which definition a result speaks to* before quoting it.

---

## Task 2 — A Blinder–Oaxaca decomposition by hand (22 pts)

Set-up values (illustrative): $\overline{\text{rate}}_{D=1}=168$, $\overline{\text{rate}}_{D=0}=150$ bps; $\overline{\text{LTV}}_{D=1}=88$, $\overline{\text{LTV}}_{D=0}=82$ %; common slope $\hat\beta_{\text{LTV}}=2.0$ bps per LTV-point.

**(a) (3 pts)** Raw rate gap:
$$
\Delta = \overline{\text{rate}}_{D=1}-\overline{\text{rate}}_{D=0} = 168 - 150 = \boxed{18\ \text{bps}}.
$$
This is the alarming "before" number — the disparity, not yet a finding. By itself it confounds "minority borrowers happen to take riskier (higher-LTV) loans" with "minority borrowers are charged more for the same loan."

**(b) (6 pts)** Explained part (the two groups differ in LTV, priced at the common slope):
$$
\text{explained} = \hat\beta_{\text{LTV}}\big(\overline{\text{LTV}}_{D=1}-\overline{\text{LTV}}_{D=0}\big) = 2.0\times(88-82) = 2.0\times 6 = \boxed{12\ \text{bps}}.
$$
Plain English: the minority group holds, on average, 6 LTV-points-riskier loans, and a fair lender who prices LTV identically for everyone (2 bps per point) would charge *anyone* with those loans 12 bps more. So even a perfectly even-handed lender, applying one common pricing rule, would generate 12 bps of the observed 18-bp gap purely because the two groups bring different (legitimate) risk to the table. That is the "same rule applied to groups that differ in legitimate factors" half of the confound — not discrimination.

**(c) (4 pts)** Unexplained residual:
$$
\text{unexplained} = \Delta - \text{explained} = 18 - 12 = \boxed{6\ \text{bps}}.
$$
This is the Blinder–Oaxaca residual — the part of the gap that the legitimate factor (LTV) does *not* account for, the by-hand analogue of the surviving minority coefficient in a conditional regression. It is the number a fair-lending case turns on, because it is the candidate for "a different rule applied to the same factors": after netting out the legitimately-priced risk difference, two groups bringing the *same* LTV still differ by 6 bps. (Whether those 6 bps are *truly* differential treatment depends on whether LTV is the *only* legitimate factor that differs — see Task 3: the credit score is the missing one.)

**(d) (4 pts)** Re-derive via risk-adjusted rates. Subtract each group's legitimately-priced LTV component $\hat\beta_{\text{LTV}}\cdot\overline{\text{LTV}}_{\text{group}}$ from its mean rate:
$$
\text{risk-adj}_{D=1} = 168 - 2.0(88) = 168 - 176 = -8\ \text{bps},
$$
$$
\text{risk-adj}_{D=0} = 150 - 2.0(82) = 150 - 164 = -14\ \text{bps}.
$$
Difference: $-8 - (-14) = \boxed{6\ \text{bps}}$, which equals the answer to (c). The two routes agree because they are algebraically identical: $(\overline r_1 - \beta\overline X_1) - (\overline r_0 - \beta\overline X_0) = (\overline r_1 - \overline r_0) - \beta(\overline X_1 - \overline X_0) = \Delta - \text{explained}$. This is the by-hand version of "add the control and read the coefficient": pricing out the legitimate factor first, then comparing what is left.

**(e) (5 pts)** (i) Different LTV *slopes* would mean the price *per unit of risk* differs by group — e.g., the minority group is charged 2.5 bps per LTV-point while the reference group is charged 2.0, so the same incremental risk costs more for one group. (ii) That third "coefficients" term is itself a candidate piece of discrimination, not a nuisance to net out, because charging a different price for *identical* risk is the very definition of disparate treatment on the pricing margin — folding it into "explained" would *hide* discrimination by relabeling a discriminatory slope as a legitimate one. (iii) For this two-task purpose, collapsing everything beyond the common-coefficient explained part into a single "unexplained" residual is **conservative**: it refuses to credit any group-specific slope as "legitimate," so it cannot accidentally launder a discriminatory price difference into the explained bucket. The risk runs the other way only if you wrongly attribute a benign slope difference to discrimination — but for a *fair-lending* reading, erring toward a larger unexplained residual is the cautious direction, and it keeps the decomposition honest with a single legitimate factor measured.

**Arithmetic verification (foot of task):** raw $=168-150=18$; explained $=2.0\cdot(88-82)=12$; residual $=18-12=6$; risk-adjusted means $-8$ and $-14$, difference $6$. All three numbers consistent.

---

## Task 3 — Omitted creditworthiness: the residual inflates (18 pts)

**(a) (5 pts)** Two-sign rule on $\text{bias}=\beta_{\text{score}}\cdot\delta$:

- **Sign of $\beta_{\text{score}}$:** negative. A higher credit score means lower risk, and the GSE/lender prices lower risk with a *lower* rate, so score pushes the (higher = expensive) rate down. $\beta_{\text{score}}<0$.
- **Sign of $\delta$:** negative. $\delta$ is the slope of score on $D$; the minority group $D=1$ averages a *lower* credit score (the legacy of unequal credit access, Ch 2.5), so regressing score on $D$ gives a negative slope. $\delta<0$.
- **Product:** $(-)\times(-) = \boxed{+}$. The bias term is **positive**.

Plain English: omitting the credit score pushes the measured minority rate premium **up** — the score-omitted residual **overstates** the true differential-treatment effect $\beta_D$. Intuitively, the regression cannot see that the minority group really does carry lower scores (genuine, legitimately-priced risk), so it mistakenly loads that price difference onto the only group variable it *can* see, the minority indicator. The "premium" absorbs real risk the data hid.

**(b) (5 pts)** With $\beta_D=4$, $\beta_{\text{score}}=-0.5$ bps per score-point, $\delta=-20$ score-points per unit of $D$:
$$
\text{bias} = \beta_{\text{score}}\,\delta = (-0.5)(-20) = +10\ \text{bps},
$$
$$
\hat{\tilde\beta}_D \xrightarrow{p} \beta_D + \text{bias} = 4 + 10 = \boxed{14\ \text{bps}}.
$$
Dropping the score inflates the apparent premium by **10 bps** (from a true 4 to an apparent 14). The HMDA-only researcher — who *cannot* see the score — is estimating the contaminated $\hat{\tilde\beta}_D=14$, **not** the clean $\beta_D=4$. So her "unexplained residual" (the Task-2 object, now in a score-blind world) is more than triple the true differential-treatment effect: most of what looks like discrimination is the omitted score in disguise.

**(c) (4 pts)** Prediction: when the score is **added**, the estimated minority coefficient **shrinks toward zero** (from $\approx 14$ down toward $\approx 4$ in this illustration). This follows directly from the sign in (a): the bias was *positive*, so removing it by including the score takes the coefficient *down*. This is exactly BHR's claim — that "much of what earlier studies called unexplained was omitted-variable bias all along": once the creditworthiness variables underwriters actually saw are in the regression, the race coefficient collapses, revealing that the earlier residual was largely the missing score. It is the OVB of Week 2 *measured* rather than feared: the HMDA literature could only *reason about the sign* of the bias (two-sign rule) because the score was unobserved; BHR got the score, so they could *watch* the coefficient march down as it entered — turning Mentor 4's "you can never see the score" into "here is what happens to the coefficient when you finally can."

**(d) (4 pts)** The remaining omitted variable is the **soft information** a human underwriter gleans that no dataset records — the explanatory letter about a one-time hardship, local knowledge of the applicant's employer or neighborhood, a judgment about the stability of the income (the "pre-read" of Mentor 4, the residual list at the end of Ch 2.5: unobserved motivation, soft information, local shocks). Its presence means BHR's surviving residual is a **lower bound** on true differential treatment in the following sense: *if* that soft information is itself correlated with race in the disfavored direction — i.e., minority applicants on average carry soft signals that legitimately *worsen* the file beyond what the hard data show — then including it would *raise* the residual, so the residual we can measure (without it) is conservatively small. Equivalently, a near-complete file still omits one relevant, possibly-correlated variable, so by the same OVB logic the measured coefficient is biased, and under that correlation it understates the true effect — hence a bound, not a clean causal estimate.

*(Note: the direction of this bound is conditional. If the unrecorded soft information instead flattered the minority group's files, the sign would flip; the defensible claim is the one Ch 6.4 makes — that even a near-complete file leaves a residual that is a bound rather than a point estimate, because some relevant, plausibly-correlated thing is still in the error term.)*

---

## Task 4 — The over-controlling trap: discrimination that wrongly vanishes (18 pts)

**(a) (5 pts)** The offered rate is a **mediator** — a variable *on* the causal path $D\to\text{offered rate}\to\text{final rate}$ — not a pre-existing confounder. Conditioning on a mediator **blocks the very path the effect travels down**: it asks "holding the offered rate fixed, does $D$ still move the final rate?" But the whole mechanism of this discrimination *is* that $D$ moves the offered rate, which then moves the final rate. Holding the offered rate fixed removes exactly that channel, so the coefficient on $D$ collapses to the (near-zero) *direct* effect that bypasses the offered rate — here +0.3 bps. The total effect of $D$ on the final rate was +6 bps; controlling for the mediator throws away the 5.7 bps that flowed *through* the offered rate. The +0.3 is therefore a gross **understatement** of discrimination, because it has conditioned away the discrimination itself — it answers a different question ("the direct effect net of the offered-rate channel") than the one Maya asked ("the total effect of being minority on what you pay"). You cannot "be thorough" by adding a variable that is downstream of your treatment.

**(b) (4 pts)** The one-sentence test (Ch 6.4 §6): **add a control if it is a pre-existing *confounder* you should hold fixed (a legitimate factor that affects the outcome and is *not caused by* the treatment); do *not* add it if it is a *channel/mediator* on the causal path from the protected trait to the outcome.** Applied:

- **(i) Credit score** — *legitimate confounder*. It is determined before and independently of the lending decision, reflects genuine repayment risk a lender may price, and is not *caused by* the applicant's group membership in the lending interaction. **Add it.**
- **(ii) Loan-to-value ratio** — *legitimate confounder*. A pre-set, formula-priced risk input (the down-payment / loan structure), part of "all the legitimate risk." **Add it.**
- **(iii) Internal "risk grade" assigned partly via loan-officer discretion** — *pathway variable*. Because it is assigned *during* the process and *encodes the officer's discretion*, it can itself carry the discrimination; conditioning on it would absorb the bias and shrink the race coefficient for the wrong reason. **Do not add it** (or treat it as an outcome, not a control).

**(c) (5 pts)** Conditioning on the **published GSE risk inputs** (credit score, LTV, etc.) is safe because those inputs are *exogenous to the lending interaction* and *legitimate by institutional construction*: for conforming loans sold to Fannie Mae / Freddie Mac, default risk is priced by a *published formula* (the loan-level price adjustments), so two loans with the same score and LTV carry the same credit risk to the investor *by construction*. They are pre-existing confounders — the "all the legitimate risk and nothing on the discrimination pathway" set — so any rate gap surviving them cannot be attributed to risk the lender legitimately priced. A **steered product type** or a **discretionary internal grade**, by contrast, is *produced inside the process*: if minority applicants are steered into a costlier product, the product type is a mediator of the discrimination, and conditioning on it regresses away the effect (Task 4a). The over-controlling danger *grows* with every "richer" control added in the name of precision because each new variable is one more chance to accidentally include a pathway variable: the richer and more endogenous the control (lender-assigned grades, realized terms, post-application variables), the more likely it sits downstream of the treatment and silently launders the discrimination out of the coefficient. This is why Ch 6.4 says the formula inputs keep Bartlett et al. "on safe ground" precisely *because* they are not richer than the published risk formula.

**(d) (4 pts)** Identifying-assumption sentence (CONVENTIONS §4 format), clean spec:

> *The conditional minority rate gap equals differential treatment as long as **the conditioning set captures all the legitimate risk a fair lender is allowed to price (the GSE formula inputs — credit score, LTV, and the like — so no genuine risk leaks into the residual)** and **no control sits on the steering/discrimination pathway (no mediator such as the offered/quoted rate, a steered product type, or a discretion-laden internal grade is held fixed)**.*

First blank = the OVB threat (omitted legitimate risk → residual too big, Task 3); second blank = the over-controlling threat (a held-fixed mediator → residual too small, Task 4). Both must hold: the residual is a credible measure of differential treatment only when the controls are *all the legitimate risk and nothing on the pathway*.

---

## Task 5 — Human versus algorithmic: does the machine cure it? (16 pts)

Illustrative conditional gaps: traditional 8.0 bps, FinTech 5.0 bps.

**(a) (5 pts)** The hoped-for answer the chapter names: **"a machine has no face to read, no neighborhood prejudice, no discretion to abuse — algorithms are blind, so they do not discriminate; the algorithm is the cure."** It is a **hypothesis to test, not an assumption**, because an algorithm can still discriminate without ever seeing race — by pricing on variables that proxy for race (geography), or by competing less hard in some markets — and the only way to know is to *measure* the gap under algorithmic pricing rather than to assume it away. Reading the table: removing the human **shrinks** the gap (8.0 → 5.0) but does **not eliminate** it. The robust one-sentence finding (Ch 6.4 §4): **algorithmic lending reduces the disparity but does not eliminate it** — discretion-based discrimination falls, yet a residual survives even with no human in the loop.

**(b) (4 pts)** Mechanism decomposition:

- The **3.0-bp difference** (8.0 − 5.0) is plausibly the **human-discretion** channel: the face-to-face mechanism — a loan officer's discretion, in-person judgment, or prejudice — that algorithmic pricing removes. Take the human out and that 3.0 bps disappears.
- The **5.0-bp residual** survives even with **no human in the loop**, so it cannot be face-to-face discretion. Ch 6.4's two mechanisms for how a race-blind algorithm still produces a gap: (1) the algorithm **prices on variables that proxy for race** — e.g., geography that correlates with race — so a "neutral" input reintroduces the disparity (a disparate-impact channel, Task 1); and (2) **weaker competition in some markets** lets the algorithm extract a higher price from borrowers in less-competitive (often minority) segments. Neither needs a human or a race input.

**(c) (4 pts)** The race-blind **AUS** provides what a regression cannot: a *real, deployed decision rule that by design cannot use race*, producing an approve/refer recommendation purely from risk inputs. That makes it a **mechanical counterfactual** for "what a rule that cannot discriminate would decide" — the literal "same-quality applicant, vary only the protected trait" comparison that Ch 3.1 says you can never directly observe, because here the comparison is built into the system rather than assumed in a regression: the AUS *is* the like-for-like, race-blind decision for each application. Comparing **actual** denials to the **AUS-recommended** decisions isolates what the *risk rule says* from what the *human did on top of it* — i.e., it separates the neutral-rule outcome from the human's deviation, which is precisely the disparate-treatment test of Task 1c.

**(d) (3 pts)** Bartlett et al. live on the **pricing** margin (conditional on getting a loan, what do you pay?); BHR primarily on the **acceptance** margin (do you get the loan at all?). A complete verdict needs both because a lender can **launder** discrimination from one margin to the other: *approve everyone but price the disfavored group higher* (clean acceptance, dirty pricing), or *price uniformly but deny more* (clean pricing, dirty acceptance). A paper that examines only the acceptance margin could declare approvals even-handed while the disparity has simply moved into price (and vice versa) — so the disparity is not gone, just relocated to the margin no one measured.

---

## Task 6 — Critique and spec discipline: name the threat, name the design (14 pts)

**(a) (5 pts)** Maya's claim rewritten in CONVENTIONS §4 format (illustrative values supplied for the fields she left blank, and flagged as such):

- **Outcome:** the loan's rate spread (HMDA post-2018 pricing field), in basis points.
- **Key regressor:** a minority indicator $D$ (Black/Hispanic = 1, non-Hispanic white = 0).
- **Controls:** loan amount, applicant income (the legitimate factors HMDA carries) — *note: the credit score is **not** available in HMDA.*
- **Fixed effects:** census-tract and lender fixed effects.
- **Clustering:** standard errors clustered by lender *(illustrative — Maya had not stated this; she must)*.
- **Sample:** conforming first-lien purchase mortgages, HMDA, a stated set of recent post-2018 years *(illustrative — must be named)*.
- **Identifying assumption (one sentence):** *the conditional rate-spread gap equals differential treatment as long as the controls capture all the legitimate risk a fair lender prices and none sits on the discrimination pathway* — which, with the credit score unavailable, is **not** satisfied (see (b)).

**(b) (4 pts)** Two threats:

1. **Omitted credit score (required).** HMDA cannot see the score; from Task 3, $\beta_{\text{score}}<0$ and $\delta<0$ (minority group averages a lower score), so the bias $\beta_{\text{score}}\delta>0$ is **positive** — the 5-bp estimate is biased **upward**, i.e. **too big** as an estimate of differential treatment. The true score-adjusted gap is almost certainly smaller (recall BHR: the coefficient shrinks when the score enters). So 5 bps is an *upper* bound on differential treatment, not the effect itself.
2. *(Choose one — here, disparate-treatment vs. disparate-impact, Task 1.)* Calling 5 bps "the causal effect of race on price" elides which legal question it answers. Even a clean score-adjusted residual would be a **disparate-treatment** estimate and would say nothing about **disparate impact** — and the score Maya wishes she had may itself be a channel of disparate impact (a score shaped by historical inequities). *Fix/hedge:* state which definition the number speaks to, and note that conditioning on a score (were it available) could control away a disparate-impact channel even as it sharpens the disparate-treatment estimate. *(Alternatively, the over-controlling trap from Task 4: do not add a mediator such as the offered rate or a steered-product flag in pursuit of a "cleaner" number, or the gap will vanish for the wrong reason and **understate** discrimination.)*

Corrected one-sentence claim Maya should write:

> *"On a HMDA extract, the conditional rate-spread gap for minority borrowers is about 5 bps after controlling for loan amount, income, and tract and lender fixed effects; because HMDA omits the credit score and the gap therefore likely overstates true differential treatment, this is best read as an **upper bound** on a disparate-**treatment** rate premium — not a clean causal effect of race, and not evidence on disparate impact."*

**(c) (5 pts)** Connection to **Gao & Sun (2019)** and **Capstone 1**:

*(i) The design move.* When more controls cannot fix the problem because the decisive variable (the credit score) is *fundamentally unobserved in HMDA*, you substitute a **design** for the missing control: a **matched comparison** (pair each minority application to a non-minority application identical on income band, loan amount, LTV, and tract, and compare within pairs) and/or a **policy-change difference-in-differences** (a state that changes fair-lending enforcement at a known date gives a before/after, treated/control contrast). This is exactly the move Gao & Sun (2019) made in the same-sex-borrower work: HMDA's missing score forced a *design* — matched comparison and policy variation — rather than a kitchen-sink regression to carry the argument.

*(ii) Why a design can succeed where controls fail.* Adding controls can only adjust for variables *in the data*; it is powerless against a variable that is *not recorded at all*, like the HMDA-missing score — no regression can hold fixed what it cannot see. A clean matched comparison or a policy DiD instead **makes the unobserved factor irrelevant by construction**: matching pairs applications that are alike on the observables (and, the bet goes, comparable on the unobservables), while a DiD differences out any *time-invariant* group difference (including a stable unobserved score gap) and asks only whether the *change* at the policy date differs by group. The identifying work is done by the comparison or the institutional variation, not by a longer control list — which is why Ch 6.4 says a design beats more controls here.

*(iii) The confound a matched HMDA comparison still cannot fix.* The **unobserved credit score** (and, relatedly, **selection into who applies**): matching on income, loan amount, LTV, and tract still leaves two "identical" applicants potentially differing in the one thing HMDA never records — the score — so a within-pair gap could still reflect a genuine, unpriced risk difference rather than differential treatment. Carrying that *named, unclosed* threat into Capstone 1 is the whole point of spec discipline: a design that survives a hostile referee, a regulator, and a court is one that states precisely the threat it has *not* closed (the missing score; applicant self-selection) rather than pretending controls have closed it.

---

*End of solutions for PS 6.4. Cross-references: Ch 6.4 (Reader's Guide to Bartlett, Morse, Stanton & Wallace (2022) and Bhutta, Hizmo & Ringo — pricing vs. acceptance margins, the FinTech-vs-human contrast, the race-blind AUS counterfactual, the over-controlling knife's edge, disparate treatment vs. disparate impact, the [CHECK]-tagged magnitudes); Ch 2.5 §§2.5.3–2.5.5 (OVB formula and the two-sign rule, with the identical creditworthiness example — relevant $\beta_{\text{score}}\neq 0$ and correlated $\delta\neq 0$); Week 3 (selection-on-observables); Week 4 (clean comparisons / design over controls); Mentor 4 (a disparity is not a finding; warm-up 3 = the over-controlling trap); Gao & Sun (2019), same-sex-borrower work, the camp's anchor for design-over-controls under a missing score. Key verdicts: T1 treatment = different rule / same inputs, impact = neutral rule / different outcomes, AUS tests treatment not impact; T2 raw 18 = explained 12 + unexplained 6 (verified two ways); T3 omitting the score biases the premium **up** (+), apparent 14 vs. true 4, adding the score shrinks it (BHR), remaining soft-info residual is a bound; T4 the offered rate is a mediator — conditioning on it makes discrimination wrongly vanish (understate), GSE formula inputs are safe confounders, danger grows with richer controls; T5 algorithms reduce but do not eliminate the gap (8→5), 3 bps human discretion + 5 bps proxy/competition, AUS = mechanical counterfactual, both margins needed against laundering; T6 spec-discipline rewrite + named threats (omitted score → upper bound; treatment-vs-impact) + Gao & Sun design (matching / policy DiD) with the still-unclosed missing-score confound carried into Capstone 1. All magnitudes are labeled illustrative values, not transcribed from the papers' tables. nb6.4 (mortgage-disparity decomposition) is where the student regenerates every illustrative number on public HMDA data.*
