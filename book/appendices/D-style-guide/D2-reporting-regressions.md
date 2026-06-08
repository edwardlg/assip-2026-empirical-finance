# D.2 — Reporting Regressions

D.1 taught you how to *build* a table — the rules, the cells, the note. This section is about a harder and more consequential set of decisions: *what to put in it.* A regression produces dozens of numbers — a coefficient and standard error for every regressor, an intercept, hundreds of fixed-effect intercepts, two or three fit statistics, the sample size. You cannot and must not show all of them. Reporting a regression well is an act of *selection*, and the selection is itself an argument: what you choose to display tells the reader what the paper is about and what variation identifies the result. This appendix is the binding standard for that selection, and it is the one Chapters 8.3 and 8.5 point your manuscript at when they say "follow Appendix D."

The reveal that organizes the whole section: **a regression table is a claim about identification, and most of identification lives in the rows you do *not* fill with coefficients.** The fixed-effects switches, the clustering line, the sample row — the things that look like boilerplate at the bottom of the table — are where a reader learns whether your number means what you say it means. Beginners lavish attention on the coefficient block and treat the bottom rows as an afterthought; professionals do the opposite, because they know the coefficient is only as credible as the disclosure beneath it. CONVENTIONS §4 demands that every specification name its outcome, treatment, controls, fixed effects, clustering, sample, and identifying assumption; the table is where the middle five of those seven become visible in a glance.

---

## 1. Which coefficients to show

A regression with a treatment variable, eight controls, county and year fixed effects, and a constant produces a long list of estimates. Show almost none of them. The rule:

> **Report the coefficient on the variable you care about, and on the handful of controls a reader needs to interpret it. Everything else — the rest of the controls, the fixed effects, the constant — is summarized, not printed.**

The **key coefficient** — your treatment, your sort variable, the right-hand-side object the paper is about — goes at the top of the body, on its own line, with its standard error beneath, in every column. This is the number the paper lives or dies on, and it should be the first thing a reader's eye lands on after the column heads. For Maya it is the examination-program indicator; for Sam, the momentum signal; for Devon, the on-chain adoption measure.

The **key controls** — the two or three covariates whose coefficients a reader would want to *interpret* or *sanity-check* — also get printed lines. If you control for applicant income and the income coefficient is positive when economics says it should be negative, that is a sign something is wrong, and a reader checking your work wants to see it. Show controls that are themselves of interest, or that serve as a sanity check, and *interpret* the ones you show in the prose.

Everything else gets **collapsed into a switch row or a summary.** The fifteen industry-classification dummies, the polynomial-in-age terms, the battery of nuisance covariates that are in the regression purely to absorb confounding and that you have no intention of interpreting — these are not printed as individual coefficients. Instead you add a row, "Controls", with "Yes" in the columns that include them, and you list *what* the control set is in the note or text. Printing forty coefficients you never mention is not rigor; it is clutter that buries the one number that matters and signals you do not know which number that is.

The **constant** is a judgment call. Many finance tables show it; many suppress it because in a demeaned fixed-effects model the intercept is not interpretable. The safe default: show the constant in specifications without fixed effects (where it has a meaning), and leave it blank or omit it once fixed effects absorb it. Never put stars on a constant you do not interpret, and never let a significant constant be mistaken for a finding.

---

## 2. R² versus within-R²: the most common reporting error

This is the single most frequent mistake in student fixed-effects tables, and it has a clean fix once you see why it happens. Recall what fixed effects *do*: a county fixed effect is a separate intercept for every county, and with a few thousand counties that is a few thousand parameters, each soaking up everything time-invariant about its county. Those intercepts explain an enormous share of the variance in the outcome — counties differ a lot, persistently — so the **ordinary $R^2$ of a fixed-effects regression is mechanically huge and almost entirely uninformative about your regressors.** Report an $R^2$ of $0.92$ from a model with county and year fixed effects and you have told the reader almost nothing, because $0.90$ of it might be the fixed effects and $0.02$ your covariates. Worse, you have *misled* them, because the naive reader reads $0.92$ as "this model is great" when it means "counties are persistent."

The fix is the **within-$R^2$**: the share of variance your covariates explain *after the fixed effects have absorbed the between-group variation.* Mechanically, it is the $R^2$ of the regression run on the demeaned data — outcome and regressors with their group means subtracted — which is exactly the variation your coefficients are estimated from. The within-$R^2$ answers the question a reader actually has: *given the fixed effects, how much do your regressors add?* That is the honest fit statistic for an FE model, and it is usually small and *should* be — a within-$R^2$ of $0.21$ on a clean panel is a perfectly respectable, honest number, far more credible than a flattering-but-meaningless $0.92$.

The reporting rule, then:

> **For a model without fixed effects, report the ordinary $R^2$. For a model with fixed effects, report and label the *within*-$R^2$. Never print an unlabeled "$R^2$" for an FE model, and never headline the inflated total $R^2$.**

`pyfixest` and `linearmodels` both compute the within-$R^2$ directly and label it; use their output rather than the total $R^2$ that some packages report by default. If you want to show both — total and within — label each unambiguously ("$R^2$" and "Within $R^2$") so the reader is never left guessing which one carries the information. And in the special case of an IV first stage, the fit statistic the reader needs is not $R^2$ at all but the **first-stage $F$** on the excluded instruments — that is what speaks to relevance and the weak-instrument concern (Ch 8.2 §1; Week 3), so that is the bottom-row statistic you show there.

---

## 3. Disclosing the fixed-effects set, the clustering, and the sample

Here is where the table does its identification work, and where CONVENTIONS §4 becomes visible. Three disclosures, each in its own row or line, none optional.

**The fixed-effects set, as switch rows.** Every set of fixed effects in the model gets a "Yes/No" row, labeled by *what* it absorbs: "County fixed effects", "Year fixed effects", "Firm fixed effects", "Industry × Year fixed effects". You report whether each set is included in each column, never the intercepts themselves. The reason this matters beyond bookkeeping is that **the fixed-effects rows disclose the identifying variation.** "County FE: Yes" tells the reader the coefficient is identified *within* county — off how a county's own outcome moves over time, not off differences between counties — which is precisely the demeaning of Ch 2.3 and the two-way fixed effects of Ch 4.1. A reader who knows the FE set knows what comparison your coefficient represents. Be specific about *interactions*: "State × Year fixed effects" is a very different (and much more demanding) object than "State fixed effects" plus "Year fixed effects", and conflating them in the disclosure misrepresents the design. If the FE structure is non-obvious, spell it out in the note.

**The clustering, named explicitly.** The clustering level is disclosed in the note (D.1 §6) and, for a multi-panel paper, often echoed in a table row ("SE clustering: State"). This is the load-bearing disclosure, because — as Week 5 and Ch 8.2 §1 drilled — the clustering level decides whether the *t*-statistics are honest. The standard from CONVENTIONS §3 is to name the flavor (clustered, and on what; or HC1/HC2/HC3; or HAC) every time. The cardinal failure here is **undisclosed clustering**: a panel table whose note says only "robust standard errors" or, worse, is silent. On persistent panel data that is the BDM disease, and a reader who cannot find the clustering level rightly assumes the SEs are too small and the stars are inflated. State the level, and state it at the level the *treatment* varies — if the program switches on at the state level, you cluster by state, and the table says so.

**The sample, disclosed and watched.** The sample is named in the note — source, period, unit of observation, and filters (D.1 §6) — and the *size* of it appears as an $N$ row on every column. The discipline beyond mere disclosure is to **watch $N$ across columns**, because a changing $N$ is a silent sample change that confounds your coefficient comparisons (D.1 §5, Week 5). If adding a control drops $N$ from $28{,}640$ to $19{,}220$ because that control is missing for a third of your observations, then the coefficient movement across those columns mixes "the control mattered" with "the sample shrank to a different population", and the honest fix is to hold the sample fixed across columns (restrict every column to the observations where all variables are present) so the build-up is clean. Report $N$ on every column precisely so this is visible to you and to the reader.

Every filter you applied is a *decision*, and decisions can be levers (Week 5, box 3). "We drop financial firms", "we require two years of prior data", "we winsorize at 1/99" — each is disclosed, because each is a place where a skeptic might suspect the sample was chosen to produce the result. Disclosing filters is not confession; it is the move that lets a reader rebuild your sample and confirm you did not gerrymander it.

---

## 4. Building up columns: parsimonious to saturated

The left-to-right architecture of an empirical table is itself an argument, and you build it deliberately. The convention:

> **Column (1) is the most parsimonious defensible specification — often the bivariate or treatment-only regression. Each column to the right adds controls or fixed effects, ending in the fully saturated specification you most believe.**

Reading the key coefficient *across* the columns is how the reader judges robustness to confounding. If the treatment coefficient barely moves as you pile on controls and fixed effects — $-1.5, -1.5, -1.4$ — that is a strong result: the raw association was not an artifact of the obvious omitted variables. If it collapses — $-1.5, -0.9, -0.1$ — the table has honestly told the reader that most of the raw relationship was confounding, and the saturated column is the truth. **Either way, the build-up is honest reporting, not salesmanship**, because it shows the reader the *path* from raw correlation to your preferred estimate and lets them see how much of the effect is fragile to controls.

Two disciplines keep the build-up clean. First, **hold the sample fixed across columns** (§3) so that movement in the coefficient reflects the added controls, not a changing population. Second, beware the **bad control**: never add, in a later column, a variable that is itself an *outcome* of the treatment (a post-treatment mediator), because conditioning on it bleeds away the very effect you are estimating, and the resulting "stability" or "instability" is an artifact, not evidence (Ch 8.2 §3). The build-up should add *pre-determined* confounders and absorbing fixed effects, never post-treatment channels.

The saturated column — the rightmost, with your full controls and fixed effects — is the one you defend as your **primary specification**, and it should be the one your pre-analysis plan committed you to (Ch 7.3). The earlier columns are context: they show what the world looked like before you imposed the design. The story the table tells, read left to right, is the story of your identification strategy doing its work.

---

## 5. The "table stands alone" principle

Carry this from Ch 8.3 §8, because it is the standard everything in D.1 and D.2 serves. **Referees read tables before they read prose, and sometimes read only the tables.** A reader who arrives at your headline table without having read a word of the surrounding paragraphs must be able to determine, from the table and its note alone:

- what the dependent variable is and its units;
- what the key coefficient measures and in what direction;
- what the stars mean (the legend, in the note);
- what the parentheses hold (SE or *t*, named);
- what the standard-error flavor and clustering level are;
- which fixed effects are included, hence what variation identifies the estimate;
- the sample and its size.

If any of those cannot be read off the table, the table has failed, and the fix goes *in the table* — in a row or in the note — never in the paragraph. The operational test, from Ch 8.3's reflection prompt: cover the prose, hand the bare table to a classmate who has not seen your project, and list everything they cannot determine. That list is your repair list. A table that needs the prose to be intelligible is a table that loses points on the rubric (the E-solutions manual is explicit: a table that violates Appendix D loses points "no matter how good the surrounding prose"), and, worse, it is a table a real referee will distrust.

The deep reason the principle holds is the one from Week 5: the table is the part of the paper the author cannot fudge. Prose can spin a *t* of $1.3$ as "suggestive"; the table just shows the $1.3$ and lets the reader judge. By making your table self-contained, you are inviting exactly the scrutiny that a credible result welcomes. A table that hides behind its prose is signaling, to a trained reader, that it has something to hide.

---

## 6. Common mistakes, and how to not make them

A short catalog of the failures a grader sees most often, each with the fix. These are the exact errors your Week-5 training taught you to *catch* in others; now you avoid them in yourself.

**Bare standard errors.** A number in parentheses with no statement of what it is. The reader cannot tell SE from *t*-stat, cannot tell classical from clustered, cannot judge the inference. *Fix:* state the convention and the flavor in the note, every table (D.1 §2, §6).

**Undisclosed clustering.** A panel table whose note says "robust SEs" or nothing at all. On persistent data this is the BDM disease and the *t*-stats are likely too big. *Fix:* name the clustering level and the cluster count, and cluster at the level the treatment varies (§3; Ch 8.2 §1).

**The kitchen-sink table.** Forty coefficients shown, the treatment buried among nuisance controls and fixed-effect intercepts, no signal about which number is the point. This is the opposite of selection, and it reads as an author who does not know what their paper is about. *Fix:* show the key coefficient and key controls; collapse the rest into a "Controls: Yes" switch row (§1).

**The inflated $R^2$.** An FE model headlining a total $R^2$ of $0.9$ that is mostly absorbed intercepts. *Fix:* report and label the within-$R^2$ (§2).

**The silently shifting sample.** $N$ changing across columns because a control is missing, so coefficient comparisons are confounded with population changes. *Fix:* hold the sample fixed; report $N$ on every column so the constancy is visible (§3).

**Conflating FE structures in the disclosure.** Reporting "State FE" and "Year FE" as two switches when the model actually has "State × Year" interactions, or vice versa — a misrepresentation of the identifying variation. *Fix:* disclose the exact FE structure, interactions included, in the rows and the note (§3).

**Spurious precision.** Six decimal places on a coefficient whose SE is uncertain in the second. *Fix:* match digits to the SE, two or three significant figures, consistent down the column (D.1 §4).

**Star-spraying and significance-as-importance.** Stars on every control and the constant, and prose that treats three stars as "important" rather than "precisely estimated". *Fix:* stars only where they carry information; let the *prose* (D.5) carry the economic magnitude, in human units, separate from the significance (Week 2; D.1 §3).

**The retyped table.** A table hand-typed into the manuscript rather than generated from the analysis, which inevitably drifts from the numbers it claims to report. *Fix:* generate every table from the frozen results in `nb8.3`, export to LaTeX, never retype — the entire point of the reproducible pipeline (Ch 8.3 *Your Turn*; D.4).

---

## 7. The reporting checklist

Run every regression table against this before it enters the manuscript:

- The **key coefficient** is on top, in every column; only **interpretable controls** are shown as coefficients; nuisance controls are a "Controls: Yes" switch row.
- The **constant** is shown only where interpretable, never starred if uninterpreted, blank under fixed effects.
- Fit is the **within-$R^2$** for FE models (labeled), the ordinary $R^2$ otherwise, the **first-stage $F$** for an IV first stage.
- **Fixed-effects sets** are Yes/No switch rows, labeled precisely (interactions disclosed as interactions), so the identifying variation is legible.
- The **clustering level** is named, at the level the treatment varies, with the cluster count; the SE flavor follows CONVENTIONS §3.
- The **sample** is named with its filters in the note; **$N$ is on every column** and held constant across columns (no silent sample change).
- Columns **build parsimonious → saturated**, sample fixed, no **bad (post-treatment) controls** introduced along the way; the saturated column is the pre-registered primary spec.
- The **table stands alone**: cover the prose and a stranger can reconstruct outcome, key effect, stars, SE flavor, FE, and sample.
- The table is **generated, not retyped**, from the frozen analysis.

With the table built (D.1) and reported (D.2), the next section — **D.3** — governs how you *defend* it: the robustness section that turns your Ch 7.5 threats-and-responses table into persuasion. **D.4** is the replication-packet standard that makes every number reproducible, and **D.5** is the prose style and causal-language discipline that surrounds the whole thing. The selection you perform in this section — showing the coefficient that matters, disclosing the fixed effects and clustering, holding the sample honest — is the same discipline as the identification memo, now made visible in a grid.
