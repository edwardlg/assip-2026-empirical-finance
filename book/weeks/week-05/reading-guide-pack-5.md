# Reading Guide Pack 5 — How to Read an Empirical Paper

This week the textbook stops teaching you *methods* and starts teaching you *judgment*. Weeks 1–4 built the toolkit: OLS and its assumptions, robust and clustered standard errors, omitted-variable bias, instrumental variables, difference-in-differences, regression discontinuity. You can run all of it. What you cannot yet do — and what separates someone who *uses* econometrics from someone who *reads* it — is pick up a paper you have never seen, in a journal you have never opened, and in twenty minutes know what it claims, whether to believe it, and where it is soft. That is the skill of Week 5, and this pack is the connective tissue. The five chapters this week each apply the same fixed procedure to one famous paper — Fama–French (1992) and (1993), Jegadeesh–Titman (1993), Petersen (2009), Bertrand–Duflo–Mullainathan (2004). This pack is the procedure itself, stated once, so you can carry it to *any* paper, including the unseen one you will dissect on the Week-5 assessment.

A warning before the trick: papers are not written to be *read*, they are written to be *cited*. The intro oversells, the literature review flatters, the prose hides the one assumption everything hangs on inside a subordinate clause on page 14. The professional reader is not impressed and not fooled. She has a checklist, she reads in a deliberate order that is *not* front-to-back, and she knows that the real paper lives in the tables. Let us hand you her checklist.

---

## 1. The Reader's-Guide template — the seven-part anatomy

Every Reader's Guide this week has the same seven parts, in the same order. The order is not decoration; it is the order in which a claim has to survive scrutiny. A result that has a sharp question but no credible identification is a guess; one with great identification but thin data is a curiosity. You will fill in these seven boxes for Fama–French on Monday and for an unseen paper on Friday. Apply this template to *any* empirical paper you ever read — class, capstone, or the rest of your life.

**(1) Research question.** One sentence, in plain English, ending in a question mark. Not "this paper studies the cross-section of returns" but "does a stock's *size* predict its average return after you account for market risk?" If you cannot state the question as a question, you do not yet understand the paper. Force yourself to name the **outcome** (what is being explained) and the **key right-hand-side variable** (the thing whose effect we care about) right here.

**(2) Identification strategy.** *How* does the paper claim to isolate the effect of the key variable from everything else? Name the design — a portfolio sort, a panel regression with fixed effects, an instrument, a DiD, an RD — and then, in one sentence, **the identifying assumption**: the condition under which the estimate equals the thing we want. This is the single most important box. Most of the rest of the guide is in service of deciding whether this sentence is true.

**(3) Data.** What is the unit of observation (a firm-month? a person? a state-year?), the sample period, the source (CRSP, Compustat, SEC EDGAR, a survey), and the number of observations? Note any sample filters — "we drop financial firms," "we require two years of prior data" — because filters are decisions, and decisions can be levers. Note look-ahead and survivorship traps you suspect, even if the paper does not.

**(4) Table-by-table reading order.** Which table is the **headline** — the one that, if it broke, would sink the paper? Which tables are setup (summary statistics, the first stage of an IV), and which are defense (robustness, placebo, alternative specifications)? Write the order in which a reader should look at the tables to absorb the argument fastest, and say in one line what each table is *for*.

**(5) What's clever.** Every paper that survives has one genuinely good idea — a construction, a comparison, a piece of data nobody had assembled, a way of turning an awkward problem into a clean one. Name it. (Fama–French's cleverness is sorting stocks into portfolios so that the noise in individual-stock betas averages out; Bertrand–Duflo–Mullainathan's is inventing *placebo* laws to measure how often the standard errors lie.) Naming the cleverness is how you learn to be clever yourself.

**(6) What's vulnerable.** Every paper also has a soft spot — the assumption most likely to be false, the alternative explanation it did not rule out, the sample that may not generalize, the standard errors that may be too small. State the *single most threatening* alternative explanation and what evidence would settle it. This is not nitpicking; it is the question a referee, a seminar audience, or a skeptical capstone mentor will ask first. Reveal the trick *and* reveal where the trick can fail.

**(7) Three replication exercises.** Three concrete things a student could *do* — on real data, on a laptop — to test or extend the paper. One should re-create a number from the headline table; one should stress an assumption (re-run with different controls, a different sample window, a different standard-error flavor); one should extend the idea to a new setting (a new asset class, a more recent decade, a different country). These become your problem-set and notebook tasks; they are also the seed of a capstone.

---

## 2. The reading-order heuristic — tables first, prose last

Here is the move that most surprises beginners, and the single most useful habit in this pack. **A professional does not read a paper front-to-back.** She reads it in this order:

1. **Abstract** — once, for the claim and the magnitude. What did they find, and how big?
2. **Tables and figures — *before any of the body prose*.** Go straight to the exhibits. Find the headline table. Read the main result *off the table itself* — the sign, the size, the t-statistic, the sample size — before you read a single sentence of the authors' description of it.
3. **The identification section** — usually "Data" and "Methodology" / "Empirical Strategy." Now that you know the result, go learn how they claim to have earned it. Pin down the identifying assumption from box (2).
4. **Robustness section** — what did they do to convince a skeptic? Which alternative explanations did they pre-empt, and which did they conspicuously *not* mention?
5. **Introduction and literature review — *last*.** Only now read the framing. By this point you already know the answer and the design, so you can read the intro for what it is — salesmanship — without being sold.

**Why tables first?** Because the table is the part of the paper the authors cannot fudge. Prose can spin a $1.3$ t-statistic as "suggestive evidence"; the table just shows you the $1.3$, and you decide for yourself. Reading the result off the table *before* the prose inoculates you against the authors' framing: you form your own one-sentence summary of what the numbers say, then check whether the prose agrees. When the prose claims more than the table delivers — and it often does — you will catch it, because you read the table while your mind was still your own. A second reason: the table tells you instantly whether the paper is even *about* what you think. The dependent variable at the top of the columns, the key regressor in the rows, the sample size at the bottom — that is the paper's skeleton, visible in thirty seconds, before you have spent an hour on an introduction that may have promised something the data could not deliver.

This is exactly how Devon should attack a new crypto-adoption paper, how Priya should attack a climate-insurance study, how Sam should read the latest momentum paper: skeleton first, framing last.

---

## 3. A glossary of table conventions — how to read an empirical-finance table

Empirical-finance tables look forbidding the first time and identical to each other ever after, because they obey strict, unwritten conventions. Learn them once. Here is an annotated mock table — invent it for Maya, who is asking whether a borrower's **debt-to-income ratio** predicts loan **default**, controlling for credit score, with the data organized as loans within lenders.

| | (1) | (2) | (3) |
|---|---|---|---|
| **Debt-to-income** | 0.042*** | 0.038*** | 0.021** |
| | (0.011) | (0.010) | (0.009) |
| **Credit score** | | −0.015*** | −0.012*** |
| | | (0.004) | (0.004) |
| **Constant** | 0.118*** | 0.640*** | |
| | (0.022) | (0.071) | |
| Lender fixed effects | No | No | Yes |
| Year fixed effects | No | No | Yes |
| $R^2$ | 0.04 | 0.11 | 0.19 |
| $N$ | 18,402 | 18,402 | 18,402 |

*Dependent variable: default (1 = defaulted within 24 months). Standard errors clustered by lender in parentheses. \*\*\* p<0.01, \*\* p<0.05, \* p<0.10.*

Now read it the way a professional does, top to bottom and corner to corner.

**Columns are specifications, not variables.** Each numbered column, (1)–(3), is a *separate regression* of the same outcome, adding controls or fixed effects as you move right. Column (1) is the raw bivariate relationship; (3) is the most demanding specification. Reading left to right tells you how *robust* the key coefficient is as you pile on controls — here, debt-to-income's coefficient shrinks from $0.042$ to $0.021$ as we add credit score and fixed effects, which honestly says "about half of the raw association was confounding." A coefficient that survives the march across columns is a strong result; one that collapses to insignificance in column (3) was mostly an artifact of what was left out.

**Each cell is a coefficient with its standard error stacked underneath in parentheses.** The top number, $0.042$, is the estimate $\hat\beta$. The number in parentheses below it, $(0.011)$, is its **standard error** — almost never the t-statistic, though a few journals do report t-stats in brackets, so always read the table's note to see which. Given $\hat\beta$ and its SE you compute the t-statistic yourself: $t = \hat\beta / \text{SE} = 0.042/0.011 \approx 3.8$. Anything past about $|t|=1.96$ is significant at the 5% level; past $2.58$, at 1%.

**Stars are significance shorthand.** The asterisks encode the p-value against the threshold given in the note: here \*\*\* is p<0.01, \*\* is p<0.05, \* is p<0.10. The exact mapping *varies by journal* — sometimes one star means 10%, sometimes 5% — so the rule is iron: **read the note, never assume the stars.** And remember Week 2's discipline: stars measure statistical significance, not economic importance. A three-star coefficient of $0.0002$ may be precisely estimated and economically trivial.

**The fixed-effects rows are "Yes/No" switches.** The rows "Lender fixed effects" and "Year fixed effects" do not report numbers (you would never print 400 lender intercepts); they report whether that set of absorbed effects was *included*. "Yes" in column (3) means the regression contains one intercept per lender and one per year, soaking up everything fixed about each lender and everything common to each year — the demeaning you met in Chapter 2.3 and the two-way fixed effects of Chapter 4.1. The Yes/No rows are how a table tells you what variation actually identifies the coefficient: with lender fixed effects "Yes," debt-to-income's effect is identified *within* lender, off variation across that lender's own borrowers.

**The bottom rows are the reality check.** $N$ is the number of observations — watch it across columns, because if $N$ *drops* when a control is added, that control is missing for some observations and the sample silently changed, which can move coefficients for reasons that have nothing to do with the control. $R^2$ is the share of variance explained; in cross-sectional finance it is often small ($0.04$ here) and that is normal and not damning. In a first-stage IV table the relevant bottom-row statistic is instead the first-stage $F$.

**The standard-error note is load-bearing — read it first, not last.** "Standard errors clustered by lender" tells you the authors let each lender's residuals correlate (Chapter 2.4 and the Petersen paper you read this week). That single phrase decides whether the t-stats are honest. If the data are a panel and the note says "robust" or is silent, be suspicious: un-clustered SEs on persistent panel data are exactly the Bertrand–Duflo–Mullainathan disease, too small, t-stats inflated. Always locate the SE note and ask: *clustered by what, and is that the level at which the key variable varies?*

---

## 4. The self-check rubric — apply to every paper

After you have run the seven-part template on a paper, grade your own understanding against this rubric. If you cannot answer all of these without re-opening the paper, you have not finished reading it. These are the exact questions your mentor — and a seminar audience — will fire at you.

- **The question.** Can I state the research question in one sentence, naming the outcome and the key regressor?
- **The identifying assumption.** Can I state the identifying assumption in **one sentence**, in the form "this estimate equals the true effect *as long as* ___"? (If the answer has the word "endogeneity" in it but names no specific threat, I have failed — see CONVENTIONS §4.)
- **The threat.** Can I name the single most plausible *alternative* explanation for the headline result — the thing that, if true, would make the estimate biased — and say which way it would bias it?
- **The headline.** Which table is the headline, and what is the one number in it that carries the paper? Could I point to it and read its sign, magnitude, and t-stat aloud?
- **The spec.** Can I write the headline specification in the CONVENTIONS §4 format: outcome · key regressor · controls · fixed effects · clustering · sample · identifying assumption?
- **The standard errors.** Are the standard errors clustered, and at the level the treatment/key variable varies? If not, do I expect the reported t-stats are too big or too small?
- **The robustness.** What is the one robustness check the authors ran that most reassured me — and the one they *should* have run but did not?
- **The replication.** Can I name one number in the paper I could reproduce on a laptop with the data we have, and one thing I would change to stress-test it?

A paper you can answer all eight on is a paper you have genuinely read. A paper you can answer only the first two on is a paper you have skimmed and an abstract you have memorized.

---

## 5. A note on spec-discipline, and the road to your capstone

You may have noticed that this pack and the CONVENTIONS file are saying the same thing from two directions. CONVENTIONS §4 — the *empirical-spec discipline* — demands that **every** specification this book writes name, explicitly, its **outcome · treatment/key regressor · controls · fixed effects · clustering · sample · and the identifying assumption in one sentence**, with no hand-wavy appeals to "controlling for endogeneity." That rule was written so that *we*, the authors, cannot fool you. The seven-part Reader's-Guide template is the same rule pointed *outward*: it is how you hold *other* authors to the standard we hold ourselves to. Box (1) is the outcome and key regressor; box (2) is the identifying assumption in one sentence; box (3) is the sample; the fixed-effects and clustering rows of any table are what §4 forces every author to state. Reading a paper well and writing a defensible spec are the same act, performed in opposite directions. The skeptic who reads a stranger's table and the author who builds an honest one are the same person.

This is also why Week 5 sits where it does. In Weeks 7 and 8 you write a **capstone** — your own empirical paper, with a real question, a real dataset (CRSP, Compustat, EDGAR), an identification strategy you can defend, and tables you build yourself. Chapter 7.5 will ask you for an *identification memo* — the one-paragraph statement of your identifying assumption and the threats-and-responses table the whole project defends — and Chapter 8.2 will stress-test it with placebos and alternative standard errors. Every box of the template you practice this week becomes a section of that paper. When a capstone mentor reads your draft, she will read it exactly as you are learning to read Fama–French this week: tables first, identifying assumption second, the prose last and skeptically. The most useful thing you can do, starting now, is to read every paper as though you will one day have to *defend* its tables in a seminar — because in eight weeks, with your own tables, you will.

So: pick up Monday's paper. Go straight to the tables. Find the headline. Then come back and tell us, in one sentence, what it would take to be wrong.
