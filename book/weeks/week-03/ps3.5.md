# Problem Set 3.5 — Anderson–Rubin Inference and the Instrument-Validity Critique

**Covers Chapter 3.5 (Reading IV in the Wild + the Weak-IV Pathology).** Methods through Ch 3.5 only:
the referee's five-question checklist for reading an IV paper (the $z$–$x$–$y$ triple, relevance via the
first-stage $F$, exclusion as an untestable argument, the complier/LATE population, just- vs.
over-identification); the weak-instrument pathology — 2SLS biased *toward OLS* with a falsely narrow
standard error, summarized by the $1/(F+1)$ heuristic; the Bound–Jaeger–Baker (1995) quarter-of-birth
cautionary tale; Anderson–Rubin (1949) test inversion and the meaning of unbounded and empty AR
confidence intervals; the Sargan/Hansen-$J$ overidentification test and its limits; many-instruments
bias; and the Olea–Pflueger (2013) effective $F$. Notation follows the Conventions. The single-instrument
IV estimator is the ratio
$$\hat\beta_{\text{IV}} = \frac{\widehat{\operatorname{Cov}}(z,y)}{\widehat{\operatorname{Cov}}(z,x)},$$
with instrument $z$, endogenous regressor $x$, outcome $y$. The Anderson–Rubin test of $H_0:\beta=\beta_0$
regresses the *adjusted outcome* $y-\beta_0 x$ on $z$ (plus controls) and tests the coefficient on $z$ for
zero.

Six problems, escalating, **100 points total**. Each is self-contained; where a number is asked for, the
inputs are supplied so you can work by hand. **The grading rule of this set:** this is a chapter about
*reading and judgment*, so a verdict stated without naming *why* — which assumption is at risk, which
diagnostic settles it, which back-door channel threatens exclusion, who the compliers are — earns half
credit at most. Throughout, when you name a threat, name the diagnostic or design that addresses it (spec
discipline, Conventions §4). No statistic substitutes for an argument about exclusion.

---

## Problem 1 — Read an IV paper like a referee (20 points)

Leah is refereeing a working paper, *"Does Patenting Raise Firm Value? Evidence from Examiner Leniency."*
The design: when a US patent application arrives, it is assigned to a patent examiner through a process the
authors argue is **as-good-as-random within an art unit** (the technology group that handles a given
application). Examiners differ in how often they grant patents — some are lenient, some strict. The authors
build, for each firm-application, the **leniency of the assigned examiner** (the examiner's historical grant
rate on *other* applications) and use it to instrument whether the firm's application is **granted**. The
outcome is the firm's **market value** in the three years after the decision. They report a first-stage
$F$-statistic of $42$, a 2SLS estimate that a granted patent raises firm value by $8.1\%$
($\text{SE}=2.4\%$, two stars), and they note that examiner-leniency designs are "standard in the
literature." There is one instrument (leniency) for one endogenous regressor (grant), within art-unit and
application-year fixed effects.

**(a)** [4 pts] Write down the IV triple — instrument $z$, endogenous regressor $x$, outcome $y$ — in one
sentence each, exactly as the chapter's question 1 demands. Then state whether the design is just-identified
or over-identified, and say what that implies about whether an overidentification test is available here.

**(b)** [4 pts] Assess **relevance**. Given the reported first-stage $F$ of $42$, is weak-instrument bias a
live concern in this design? Reference the rule of thumb from the chapter and say in one sentence what the
$1/(F+1)$ heuristic implies about how much of any OLS bias 2SLS still carries here.

**(c)** [6 pts] Assess **exclusion** — the question the data cannot answer. Examiner leniency must affect
firm value *only* through whether the patent is granted. Identify **two** distinct back-door channels by
which the assigned examiner could touch firm value *without* going through the grant decision, and for each
say in one sentence how a careful author could argue it away or control for it. (Hint: examiners do more
than grant or reject — think about *timing*, *scope/claims*, and *who gets assigned to whom*.)

**(d)** [4 pts] Identify the **complier population**. In an examiner-leniency design, whose grant outcome
does the instrument actually move? Describe the compliers concretely (in terms of application quality), name
the always-takers and never-takers, and state in one sentence the narrow LATE the $8.1\%$ actually estimates
— and whether the title *"Does Patenting Raise Firm Value?"* overclaims.

**(e)** [2 pts] The authors defend the design only by writing that examiner-leniency instruments are
"standard in the literature." State in one sentence why "it's standard" is not, by itself, an exclusion
argument, using the chapter's principle that exclusion is defended by argument, not by precedent or a
statistic.

---

## Problem 2 — Why Anderson–Rubin stays valid, and how to read its shapes (18 points)

This problem is about the *cure*. Answer in prose and one short derivation; no numbers are needed except in
part (d).

**(a)** [5 pts] Explain, from the structure of the estimator, **why** the conventional 2SLS confidence
interval becomes unreliable when the instrument is weak, and **why** the Anderson–Rubin interval does not.
Your answer must (i) identify the specific quantity 2SLS divides by that causes the trouble, and (ii) state
the one structural feature of the AR test that immunizes it — *"no first stage appears anywhere."*

**(b)** [4 pts] Write down the AR test of $H_0:\beta=\beta_0$ as an explicit recipe a classmate could run:
what variable do you construct, what do you regress it on, what coefficient do you test, and why must that
coefficient be zero under the null if exclusion holds? Then state in one sentence how you turn a *test* into
a *confidence interval* by inversion over a grid.

**(c)** [5 pts] Leah's coauthor computes an AR 95% interval and gets back the **entire real line**,
$(-\infty,+\infty)$. (i) What does an unbounded AR interval tell Leah about her instrument? (ii) The coauthor
says, "Since AR can't rule anything out, let's just report the 2SLS point estimate as our best guess." Is
that sound? Explain in two sentences why or why not, referencing what the *conventional* 2SLS interval would
have falsely reported on the same data.

**(d)** [4 pts] On a *different* over-identified dataset (two instruments, one regressor), Leah's AR 95%
interval comes back **empty** — no value of $\beta_0$ survives the test. (i) Explain why an empty interval
can only arise under over-identification. (ii) State precisely what an empty interval diagnoses, and why it
does **not** mean "the effect is zero." Connect it to the disagreement principle behind the overidentification
test of Problem 4.

---

## Problem 3 — The Bound–Jaeger–Baker lesson and the $1/(F+1)$ heuristic (16 points)

A published IV paper reports a 2SLS coefficient of $0.42$ ($\text{SE}=0.11$, three stars), an OLS
coefficient of $0.55$, and a first-stage $F$ of $3.8$. Treat OLS as biased *upward* by endogeneity (the
usual same-shock story) and the true effect as unknown.

**(a)** [5 pts] Use the $1/(F+1)$ heuristic from Section 3.5.2 to compute the *approximate fraction* of
OLS's bias that 2SLS still carries at $F=3.8$. Is the 2SLS estimate's closeness to OLS ($0.42$ vs. $0.55$) a
coincidence, or exactly what a weak instrument predicts? State the direction of the residual bias relative to
the truth.

**(b)** [4 pts] Should you trust the tight standard error of $0.11$? Explain in two sentences what is wrong
with it — name the assumption underlying the conventional 2SLS SE that fails at this first-stage strength,
and say which way the error points (too wide or too narrow).

**(c)** [4 pts] State the Bound–Jaeger–Baker (1995) lesson in your own words, and explain why a first-stage
that is "statistically significant" can still be far too weak to trust. Reference their most famous
demonstration — what happened when they replaced the real quarter-of-birth instrument with a *randomly
generated* one — and what that proves about reading a small 2SLS standard error as reassurance.

**(d)** [3 pts] What single additional result would you demand from the authors before believing the
coefficient, and what would it look like if the instrument were in fact too weak to identify the effect?
Name the result and describe the specific shape it would take.

---

## Problem 4 — The overidentification test: what a passed J really certifies (14 points)

Priya studies whether a firm's **green-bond issuance** lowers its **cost of capital**, instrumenting issuance
with **two** instruments: (1) the firm's distance to the nearest green-bond underwriter's regional office,
and (2) an index of state-level green-subsidy generosity. This is over-identified: two instruments, one
endogenous regressor.

**(a)** [4 pts] State the logic of the Sargan (1958) / Hansen-$J$ (1982) overidentification test in two or
three sentences: what object is regressed against the IV residuals $\hat u = y - x\hat\beta_{\text{IV}}$,
what the null hypothesis is, and what a **large** $J$ (small $p$-value) tells you. Then give the degrees of
freedom of the test in this two-instrument, one-regressor case, and explain the count.

**(b)** [4 pts] Priya runs the test and gets a *large* $p$-value (the $J$ test "passes"). She writes: "The
overidentification test confirms that my instruments satisfy the exclusion restriction." Identify the **two**
distinct errors in that sentence — one about what the test detects ("disagreement," not validity), and one
about the scenario in which *both* instruments are invalid.

**(c)** [3 pts] Suppose both of Priya's instruments are in fact invalid *in the same direction* — both
correlated with an omitted regional economic-vitality factor that also lowers cost of capital. Explain in two
sentences why the $J$ test will happily *pass* in this case, and what that proves about the claim "a clean $J$
certifies exclusion."

**(d)** [3 pts] State the limit that connects this problem to Problem 1(a): for a **just-identified** design
(one instrument, one regressor), how many over-identifying restrictions are there, and what does that mean
for whether the $J$ test is available? In one sentence, say what the empirical analyst is left with for
defending exclusion when no $J$ test exists.

---

## Problem 5 — Weak-IV diagnosis: first-stage F, effective F, and what to do (16 points)

Sam is running an IV regression of a stock's **next-month return** on its **realized turnover** (trading
volume scaled by shares outstanding), instrumenting turnover with a measure of **retail-attention shocks**.
He reports a non-robust first-stage $F$ of $11.6$ — "above 10, so we're fine" — but his standard errors are
heteroskedastic, and when he computes the **Olea–Pflueger (2013) effective $F$**, it comes back at $5.2$,
below its relevant critical value.

**(a)** [5 pts] Sam concludes from his first-stage $F$ of $11.6$ that weak instruments are not a problem.
Explain why the *effective* $F$ of $5.2$ overrides that conclusion. State in two sentences (i) what the
Olea–Pflueger effective $F$ corrects for that the conventional first-stage $F$ does not, and (ii) why, when
the two disagree, the effective $F$ is the one to believe here.

**(b)** [4 pts] Given an effective $F$ of $5.2$, diagnose the situation using the chapter's vocabulary: is
identification weak? What does the $1/(F+1)$ intuition say about the direction his 2SLS estimate is likely
pulled, and what would you predict about the width and honesty of his conventional 2SLS confidence interval
versus an Anderson–Rubin interval on the same data?

**(c)** [4 pts] Sam proposes to "fix" the weakness by interacting his one instrument with twenty
market-state dummies, creating twenty-one instruments — which pushes the conventional first-stage $F$ above
$20$. (i) Name the specific bias this strategy invites, and explain its mechanism in terms of the first-stage
fitted value $\hat x$ and what happens as the number of instruments grows. (ii) Will the *effective* $F$ be
fooled the way the conventional $F$ was? Say why the chapter calls this the right diagnostic.

**(d)** [3 pts] State concretely what Sam should *do* instead. Give the chapter's prescription in one
sentence — what kind of fix actually addresses weak identification — and name the one inference procedure he
should report regardless of first-stage strength so a reader can judge the result honestly.

---

## Problem 6 — Design-critique essay: apply the referee checklist to a finance scenario (16 points)

Maya is reviewing a fair-lending study, *"Does Access to Credit Reduce Default? An Instrumental-Variables
Analysis."* The author wants the causal effect of **receiving a loan** ($x$, the endogenous regressor) on the
borrower's later **default** ($y$). Loan approval is endogenous — unobserved borrower quality drives both
approval and repayment. As an instrument the author uses the fact that applications are routed to loan
officers who differ in **approval strictness**, and instruments approval with **the assigned officer's
historical approval rate** on other applicants. The author reports a first-stage $F$ of $7.5$, a 2SLS
estimate that receiving a loan *lowers* default probability by 6 points ($\text{SE}=2.9$ pts, two stars),
no Anderson–Rubin interval, and a single sentence on exclusion: "loan-officer assignment is plausibly
exogenous."

Write a referee report of roughly **250–400 words** that runs the chapter's five-question checklist (the
§3.5.9 ledger) on this design. A full-credit report must, explicitly and in order:

- **[3 pts] Relevance.** Judge the first-stage $F$ of $7.5$ against the rule of thumb; say what the $1/(F+1)$
  heuristic implies about residual bias toward OLS; and demand the diagnostic the author should have computed
  given likely heteroskedasticity in default data.
- **[4 pts] Exclusion.** Name at least two concrete back-door channels by which the assigned loan officer
  could affect *default* other than through *approval* (think: loan terms the officer sets — rate, amount,
  collateral; coaching or monitoring; which applicants the officer is assigned). State why "plausibly
  exogenous" is an assertion, not an argument.
- **[3 pts] Compliers / LATE.** Describe whose approval the officer-strictness instrument moves (the marginal
  applicants near the approval threshold), name the always-takers and never-takers, and say whether the
  abstract's universal-sounding claim overreaches the complier-specific estimate.
- **[2 pts] Identification count.** State whether the design is just- or over-identified and what check is or
  is not available as a result.
- **[2 pts] Honest inference.** Note the absence of an Anderson–Rubin interval, and say — given the low
  first-stage $F$ — what shape the AR interval might plausibly take and what that would mean for the headline
  6-point result.
- **[2 pts] Verdict and connection to Maya's own question.** Render a one-paragraph verdict (publish / revise
  / reject-as-uninformative, with reasons), and close by connecting this to Maya's recurring fair-lending
  question: what does this design teach about earning a credible causal number where unobserved borrower
  quality confounds everything?

You may invent neither numbers nor results beyond those given; argue from the design and the diagnostics the
chapter provides.

---

*End of Problem Set 3.5. Solutions: Appendix E, `E-w3-ps3.5-solutions.md`. This closes Week 3 and the first
half of the camp's causal-inference arc. Every threat rehearsed here — weak instruments, exclusion
violations, many-instrument bias — is a reason the single-cross-section, single-assumption designs of Week 3
need a sturdier successor. Week 4 supplies it: difference-in-differences (each unit its own control through
panel structure), regression discontinuity (an arbitrary cutoff as a local experiment), and synthetic control
(a bespoke counterfactual). Maya's fair-lending question and Leah's patent question return there with designs
whose credibility comes from the shape of the natural experiment, not from the validity of an instrument.*
