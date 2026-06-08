# D.1 — Table Craft

In Week 5 you learned to read an empirical-finance table the way a professional does: tables first, prose last, the standard-error note before anything else. This appendix is the same skill pointed the other way. Now *you* are the author, and a stranger — a referee, a capstone mentor, Prof. Gao at the conference — is about to read your table the way you learned to read Fama–French, looking for the seam where the trick falls apart. The whole craft of an empirical table is to leave no such seam. This section is the binding standard for how you build one. Chapter 8.3 told you *why* tables must stand alone and lead the results; this is the *how*, down to the typography. When `nb8.3` renders your `pyfixest` results to LaTeX, this is the spec it is rendering to, and this is what the grader checks your output against.

Here is the reveal that organizes everything below, stated once so you carry it through the details. **A table is not a place to store numbers; it is an argument compressed into a grid.** The reader who looks only at your headline table — and many will look at nothing else — must be able to reconstruct the entire claim from it: what you regressed on what, in what sample, with what assumed about the errors, and how confident to be. Every convention in this section exists to make that reconstruction possible *without the prose.* A table that needs the surrounding paragraphs to be intelligible has failed its first and most demanding reader, and that reader decides your fate.

---

## 1. Layout: booktabs, and the war on vertical rules

Open any top finance journal — the *Journal of Finance*, the *Review of Financial Studies*, the *Journal of Financial Economics* — and look at the *lines* in the tables. You will find exactly three kinds of horizontal rule and zero vertical rules. This is not an aesthetic accident; it is the `booktabs` convention, and it is the single most visible signal of whether a table was made by someone who knows the genre.

The rule is this. A table has a **top rule** (a thick line above the column headers), a **midrule** (a thinner line separating the headers from the body), and a **bottom rule** (a thick line closing the table). Inside the body, you use the occasional thin partial rule (`\cmidrule`) to group columns under a shared heading, and nothing else. **You never draw a vertical line, and you never box a cell.** The reason is perceptual: vertical rules chop a table into cells and force the eye to stop at every boundary, which is exactly what you do *not* want when a reader is trying to scan a coefficient leftward across specifications. Whitespace separates columns better than a line does, because the eye reads a gap as "different group" without having to brake. The horizontal rules, by contrast, do real work — they mark the three structural seams of the table (header / body / end) and the occasional sub-group. Lines that carry information, kept; lines that merely decorate, gone.

In LaTeX this means loading the `booktabs` package and using `\toprule`, `\midrule`, `\cmidrule`, and `\bottomrule` instead of the default `\hline`. Never use `\hline` and never use the `|` column-separator in the `tabular` preamble; the moment a `|` appears in your preamble you have left the convention. The body of the table is plain `&`-separated cells with `\\` line breaks. The estimator package you use (`stargazer`, `pyfixest`'s `etable`, `texreg`) emits `booktabs` rules by default, so the easy path and the correct path are the same one — which is the whole point of generating tables rather than hand-typing them.

Two layout habits beyond the rules. First, **columns are specifications, not variables** — this is the convention from the Week-5 glossary, and you obey it as an author: each numbered column is a separate regression of the same outcome, and you build them up left-to-right from parsimonious to saturated (the discipline D.2 makes precise). Second, **right-align the numeric columns on the decimal point** so that $0.042$ sits directly above $-1.4$ and the eye can compare magnitudes by reading down a clean column. The `dcolumn` package or a `siunitx` `S` column does this automatically; an unaligned numeric column is a table that looks amateur even when the numbers are right.

---

## 2. The cell: a coefficient with its standard error stacked beneath

The atomic unit of an empirical table is the **estimate stacked over its uncertainty.** The point estimate $\hat\beta$ sits on top; directly beneath it, in parentheses, sits one number describing how precisely it was estimated. That second number is almost always the **standard error**, but it is *sometimes* the *t*-statistic, and a few journals print *t*-stats in brackets to distinguish them from SE parentheses. The reader cannot tell which you mean by looking at the number — $(0.011)$ could be a tiny SE or a tiny *t* — so the iron rule is:

> **Pick one convention — standard errors *or* t-statistics in parentheses — use it in every table in the paper, and state which one in the note.**

The overwhelming default in empirical finance is **standard errors in parentheses**, and unless you have a specific reason, use that. The reason it is the better default is that the SE is the *primitive*: given $\hat\beta$ and its SE the reader can compute the *t*-statistic, the confidence interval, and the *p*-value themselves, whereas given only the *t* they cannot recover the SE. Reporting the SE gives the reader the most information and the most freedom to check your stars against their own threshold. If you do report *t*-stats instead (some asset-pricing tables do, because the *t* is the object of interest in a portfolio sort), say so in the note in those exact words — "*t*-statistics in parentheses" — and never mix the two in one paper.

Whatever you stack beneath the coefficient, **name its flavor.** CONVENTIONS §3 is explicit: standard errors are always labeled with their type — classical, HC1/HC2/HC3, HAC (Newey–West), or clustered, and if clustered, *clustered on what.* "Robust standard errors in parentheses" is incomplete; "heteroskedasticity-robust (HC1) standard errors in parentheses" or "standard errors clustered by state in parentheses" is the standard. The clustering phrase is the most load-bearing sentence in the entire note, for the reason Week 5 hammered: on persistent panel data, un-clustered SEs are the Bertrand–Duflo–Mullainathan disease — too small, *t*-stats inflated, false significance. A reader who cannot find your clustering level assumes the worst.

---

## 3. Significance stars: define them, because the thresholds vary

Stars are the table's shorthand for statistical significance: a coefficient gets asterisks according to how small its *p*-value is against fixed thresholds. The near-universal convention in finance is

$$
{}^{*}\ p<0.10, \qquad {}^{**}\ p<0.05, \qquad {}^{***}\ p<0.01,
$$

three stars for the strongest. But — and this is the trap you learned to watch for as a reader and must now disarm as an author — **the mapping is not universal.** Some journals and some fields reserve one star for $p<0.05$ and drop the 10% tier entirely; some experimental and medical venues use ${}^{*}\,p<0.05,\,{}^{**}\,p<0.01,\,{}^{***}\,p<0.001$. The same three asterisks therefore mean different things in different tables. The rule that follows is absolute:

> **Always print the star legend in the table note. Never assume the reader knows your thresholds, and never leave them to guess.**

A second discipline about stars, carried straight from Week 2 and repeated everywhere in this book because it is the most common abuse: **stars measure statistical significance, not economic importance.** A three-star coefficient of $0.0002$ is precisely estimated and may be economically trivial; a one-star coefficient of $0.3$ may be the most important number on the page. The table reports the stars honestly; your *prose* (D.5, and Ch 8.3 §5) carries the economic interpretation that the stars cannot. Do not let a row of asterisks substitute for telling the reader whether the effect is *big enough to matter.* And resist the related temptation to decorate: stars on a constant term, stars on control coefficients you do not interpret, stars everywhere, train the reader's eye to ignore them. Stars are loudest when they are rare.

---

## 4. Significant digits: precision discipline

A coefficient is not more trustworthy for carrying six decimal places. Spurious precision — `0.0418273` where `0.042` was all the data could support — is a tell that the author does not understand their own standard errors, because the digits past the second significant figure of the SE are pure noise. The discipline:

> **Report enough significant digits that the last printed digit of the coefficient is roughly the first uncertain digit implied by its standard error — and use the *same* number of decimals for a coefficient and the SE beneath it.**

Concretely: if $\hat\beta = 0.0418$ with $\text{SE} = 0.011$, the SE tells you the second decimal is already uncertain, so you report $0.042$ over $(0.011)$ — three decimals, matched. Reporting $0.0418273\ (0.0109841)$ is not more precise; it is less honest, because it implies a confidence the data do not warrant. A workable default for most finance coefficients is **two or three significant figures**, with the decimal count chosen so the coefficient and its SE align. Keep the decimal count *consistent down a column* so the numbers stack cleanly on the decimal point. The exceptions are quantities with a natural scale: report $N$ as a whole number with thousands separators ($18{,}402$, not $18402.0$), report $R^2$ to two decimals ($0.19$), report a *t*-statistic, if you show one, to one or two decimals. When coefficients are tiny because of units (a daily return in raw decimals), do not paper over it with ten decimals — **rescale the variable** (returns in percent, dollars in thousands or millions) and say so in the note, so the table shows $1.4$ rather than $0.000014$. Readable magnitudes are part of the craft.

---

## 5. The bottom rows: N, R², within-R², and the FE switches

Beneath the coefficient block, separated by a partial rule, sit the rows that let a reader audit the specification at a glance. These are not optional garnish; they are the reality check.

**Fixed-effects rows are "Yes/No" switches, never coefficients.** You would never print four hundred lender intercepts, so the table reports *whether* a set of fixed effects was included, with "Yes" or "No" in each column. A row labeled "State fixed effects" with "Yes" in column (3) tells the reader the regression absorbed one intercept per state — and, crucially, tells them *what variation identifies the coefficient*: with state FE on, the effect is identified *within* state, off variation across that state's own observations over time. The FE rows are how a table discloses its identifying variation in two words. D.2 treats the full disclosure discipline; here the layout point is simply that fixed effects belong in switch rows at the bottom, never as estimated coefficients in the body.

**$N$ is the observation count, and you watch it across columns.** Report it as a whole number with thousands separators, on its own row. The reason to put it on every column and not just once is the silent-sample-change trap from Week 5: if $N$ *drops* when a control is added, that control is missing for some observations and the estimation sample quietly changed, so any movement in the coefficient confounds "the control mattered" with "the sample changed." A reader who can see $N$ holding constant across columns trusts the build-up; a reader who sees it lurch is right to be suspicious. Make $N$ visible so they can check.

**$R^2$ versus within-$R^2$ is the row students get wrong, and D.2 §2 treats it in full.** The short version for layout: for a model *without* fixed effects, report the ordinary $R^2$. For a model *with* fixed effects, the headline number is the **within-$R^2$** — the share of variance explained by your covariates *after* the fixed effects have absorbed the between-group variation — because the ordinary $R^2$ of a fixed-effects model is inflated by the hundreds of absorbed intercepts and says almost nothing about your regressors. Label the row for exactly what it is ("Within $R^2$"), never an unlabeled "$R^2$" that the reader cannot interpret. In cross-sectional finance a small $R^2$ ($0.04$) is normal and not damning. In an IV first stage the relevant bottom-row statistic is instead the first-stage $F$; show it there.

---

## 6. The table note: where the table earns its independence

The **note** is what makes a table stand alone, and it is the part beginners neglect because it feels like fine print. It is not fine print; it is the table's instruction manual, and a referee reads it first. A complete empirical-finance note carries six things, and you can remember them as a checklist:

1. **What the dependent variable is** — and its units. ("The dependent variable is the county-year minority–white mortgage-denial gap, in percentage points.") The reader must not have to guess what the column tops are explaining.
2. **The sample** — source, period, unit of observation, and the filters. ("HMDA LAR, all U.S. counties, 2010–2019; financial-only applications excluded.") Every filter is a potential selection threat, so disclose it (D.2 §4).
3. **The standard-error flavor and clustering level** — the load-bearing sentence. ("Standard errors clustered by state in parentheses.")
4. **The star legend** — your exact thresholds. ("\*\*\* $p<0.01$, \*\* $p<0.05$, \* $p<0.10$.")
5. **What the parentheses contain** — SE or *t*-stat, stated once. ("Standard errors in parentheses.")
6. **Anything non-obvious** — the estimator if it is not plain OLS (Callaway–Sant'Anna, 2SLS, logit), any rescaling ("returns in percent"), and what the Yes/No FE rows mean if it is not self-evident.

The note belongs *below* the table, in smaller type, and it should be readable on its own. The test of a good note is the one from Ch 8.3's third reflection prompt: cover the prose, show a stranger only the table and its note, and ask whether they can determine the sample, the estimator, the meaning of the coefficient, the meaning of the stars, and the fixed effects and clustering. Everything they cannot determine is a hole in your note, fixed *in the note*, never in the paragraph.

---

## 7. A fully worked, annotated example

Here is a complete headline table for Maya's project — the staggered difference-in-differences asking whether state fair-lending examination programs reduced the county-year minority–white mortgage-denial gap (the design of Ch 4.2, the memo of Ch 7.5, the robustness of Ch 8.2). It is shown three ways: the LaTeX source you would actually ship, the same table rendered as Markdown for reading, and a line-by-line annotation of every choice.

### The LaTeX source

```latex
\begin{table}[t]
\centering
\caption{Fair-lending examination programs and the minority--white denial gap}
\label{tab:main}
\begin{tabular}{l S[table-format=-1.3] S[table-format=-1.3] S[table-format=-1.3]}
\toprule
 & {(1)} & {(2)} & {(3)} \\
 & {Bivariate} & {+ Controls} & {+ County \& Year FE} \\
\midrule
Examination program          & -2.18  & -1.71  & -1.42  \\
                             & (0.42) & (0.39) & (0.55) \\
Applicant income (\$000s)     &        & -0.031 & -0.024 \\
                             &        & (0.009)& (0.008)\\
Loan-to-value ratio          &        &  0.044 &  0.029 \\
                             &        & (0.014)& (0.013)\\
Constant                     &  1.95  &  0.88  &        \\
                             & (0.18) & (0.27) &        \\
\midrule
County fixed effects         & {No}   & {No}   & {Yes}  \\
Year fixed effects           & {No}   & {No}   & {Yes}  \\
Within $R^2$                 & {0.06} & {0.14} & {0.21} \\
$N$ (county-years)           & {28{,}640} & {28{,}640} & {28{,}640} \\
\bottomrule
\end{tabular}

\vspace{0.5em}
\footnotesize
\textit{Notes.} The dependent variable is the county-year minority--white
mortgage-denial gap (minority denial rate minus white denial rate), in
percentage points. Sample: HMDA LAR, all U.S. counties, 2010--2019; the
treatment is an indicator for an active state fair-lending examination program
(staggered adoption). Columns build from bivariate (1) to the fully saturated
two-way fixed-effects specification (3). Standard errors clustered by state
(50 clusters) in parentheses. \textsuperscript{***}$p<0.01$,
\textsuperscript{**}$p<0.05$, \textsuperscript{*}$p<0.10$.
\end{table}
```

### Rendered as Markdown

**Table D.1 — Fair-lending examination programs and the minority–white denial gap**

| | (1) Bivariate | (2) + Controls | (3) + County & Year FE |
|---|---:|---:|---:|
| **Examination program** | −2.18\*\*\* | −1.71\*\*\* | −1.42\*\* |
| | (0.42) | (0.39) | (0.55) |
| **Applicant income (\$000s)** | | −0.031\*\*\* | −0.024\*\*\* |
| | | (0.009) | (0.008) |
| **Loan-to-value ratio** | | 0.044\*\*\* | 0.029\*\* |
| | | (0.014) | (0.013) |
| **Constant** | 1.95\*\*\* | 0.88\*\*\* | |
| | (0.18) | (0.27) | |
| County fixed effects | No | No | Yes |
| Year fixed effects | No | No | Yes |
| Within $R^2$ | 0.06 | 0.14 | 0.21 |
| $N$ (county-years) | 28,640 | 28,640 | 28,640 |

*Notes.* The dependent variable is the county-year minority–white mortgage-denial gap (minority denial rate minus white denial rate), in percentage points. Sample: HMDA LAR, all U.S. counties, 2010–2019; the treatment is an indicator for an active state fair-lending examination program (staggered adoption). Columns build from bivariate (1) to the fully saturated two-way fixed-effects specification (3). Standard errors clustered by state (50 clusters) in parentheses. \*\*\* $p<0.01$, \*\* $p<0.05$, \* $p<0.10$.

### The annotation, choice by choice

Read the table the way you would attack it, and notice that every convention above is doing a job.

**The caption is a sentence, not a label.** "Fair-lending examination programs and the minority–white denial gap" tells a reader scanning the list of tables what this one is about. "Table 1: Regression results" tells them nothing and wastes the most-read line in the exhibit.

**Columns build from parsimonious to saturated.** Column (1) is the raw bivariate relationship; (2) adds the applicant-composition controls; (3) adds county and year fixed effects, the most demanding specification. Reading the treatment coefficient leftward — $-2.18 \to -1.71 \to -1.42$ — tells the honest story that about a third of the raw association was confounding, and the effect that *survives* the march across columns is the credible one (D.2 §1). The column subheads ("Bivariate", "+ Controls", "+ County & Year FE") name what each specification adds, so the build-up is legible without the prose.

**Each cell is an estimate over its clustered SE.** The treatment estimate in column (3) is $-1.42$ with $(0.55)$ beneath it. The note says those parentheses are standard errors clustered by state, so the reader computes $t = -1.42/0.55 \approx -2.6$ themselves and confirms the two stars. Two decimals on both the coefficient and the SE, matched, aligned on the decimal point.

**Stars are defined, and the legend is in the note.** The reader does not have to assume that \*\* means 5%; the note says so. Notice the treatment loses a star moving to column (3) — from \*\*\* to \*\* — because the conservative state-clustered SE in the fully-saturated spec is wider. That is honest, and the table shows it rather than hiding the most demanding column.

**The constant has no FE column.** In column (3) the constant cell is blank because the two-way fixed effects have absorbed the intercept; printing a "constant" for a demeaned model would mislead. Blank, correctly, rather than a meaningless number.

**The FE rows are switches.** "County fixed effects: No, No, Yes" and the year row tell the reader that column (3)'s coefficient is identified *within* county and net of common year shocks — the identifying variation, disclosed in two words, exactly as Week 5 taught you to read it.

**The bottom block is the reality check.** $N = 28{,}640$ is *constant* across all three columns — the controls and FE are never missing for some observations, so the sample never silently changed, and the leftward shrinkage of the coefficient is about confounding, not about a moving sample. The reported fit is **within-$R^2$**, labeled as such, because columns (3) carries fixed effects and the ordinary $R^2$ would be inflated by the absorbed county and year intercepts; D.2 §2 explains why this is the only honest fit statistic to headline for an FE model.

**The note carries all six required elements.** Dependent variable and its units; sample source, period, unit, and the build-up; SE flavor and clustering level with the cluster count; the star legend; and the estimator context. Cover the prose and this table still answers every question a referee would ask of it. That is the standard. That is what "the table stands alone" means, and it is the bar your `nb8.3`-generated tables must clear before a single one of them goes into the paper.

---

## 8. The checklist

Before any table enters your manuscript, run it against this list — the same audit a grader and a referee will run:

- `booktabs` rules only (top / mid / bottom, plus `\cmidrule` for groups); **no vertical rules, no `\hline`, no boxed cells.**
- Columns are specifications, built left-to-right from parsimonious to saturated; numeric columns right-aligned on the decimal.
- Each coefficient has its SE (or *t*-stat) stacked beneath in parentheses; one convention, stated in the note.
- SE flavor named (classical / HC1–HC3 / HAC / clustered) and, if clustered, the level *and* the cluster count.
- Star thresholds defined in the note; stars not sprayed on controls and constants you do not interpret.
- Significant digits matched between coefficient and SE, consistent down each column; variables rescaled to readable magnitudes.
- FE shown as Yes/No switch rows, never as coefficients.
- $N$ on every column (watch for silent sample changes); fit reported as **within-$R^2$** for FE models, labeled as such; first-stage $F$ for an IV first stage.
- A complete note: dependent variable and units, sample and filters, SE/clustering, star legend, what the parentheses hold, and the estimator if not plain OLS.
- The cover-the-prose test passes: a stranger can reconstruct the entire claim from the table and its note alone.

The companion sections take this further: **D.2** governs *which* coefficients to show and how to disclose the fixed-effects set, clustering, and sample; **D.3** governs the robustness section that turns your threats table into persuasion; **D.4** is the replication-packet standard that makes every number here reproducible; and **D.5** is the prose style — hedging, causal-language discipline, and citing primary sources — that surrounds these tables. A table built to this section and a paragraph written to D.5 are the same act of honesty, performed in two media.
