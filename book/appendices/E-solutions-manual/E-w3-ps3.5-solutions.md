# Solutions — Problem Set 3.5 (Anderson–Rubin Inference and the Instrument-Validity Critique)

Full worked solutions to `book/weeks/week-03/ps3.5.md`, covering Chapter 3.5. Notation follows the
Conventions: instrument $z$, endogenous regressor $x$, outcome $y$; the just-identified IV estimator is the
ratio $\hat\beta_{\text{IV}} = \widehat{\operatorname{Cov}}(z,y)/\widehat{\operatorname{Cov}}(z,x)$; the
Anderson–Rubin (1949) test of $H_0:\beta=\beta_0$ regresses the adjusted outcome $y-\beta_0 x$ on $z$ (plus
controls) and tests the coefficient on $z$. The recurring theme of the key, the IV parallel to Chapter 2.5's
bias-versus-precision lesson: **a 2SLS standard error cannot tell you whether its own instrument is strong
enough to trust. The diagnostics — first-stage $F$, Olea–Pflueger effective $F$, the Anderson–Rubin
interval, the overidentification test — live *outside* the point estimate, in the research design. A tight SE
on a weak instrument is a confident lie.**

---

## Problem 1 — Read an IV paper like a referee (20 pts)

**(a)** [4 pts] The triple:
- Instrument $z$ = **the assigned examiner's historical grant rate** (examiner leniency), measured on the
  examiner's *other* applications so it is not mechanically tied to this firm's outcome.
- Endogenous regressor $x$ = **whether the firm's application is granted** (a 0/1 grant indicator).
- Outcome $y$ = **the firm's market value** in the three years after the decision.

There is one instrument for one endogenous regressor, so the design is **just-identified**. The number of
over-identifying restrictions is $L-1 = 1-1 = 0$, so **no overidentification (Sargan/Hansen-$J$) test is
available** — there is no surplus instrument to disagree with, nothing to check. Exclusion here must be
defended entirely by argument (part c), not by a test.

**(b)** [4 pts] With a first-stage $F$ of $42$, **weak-instrument bias is not a live concern.** $42$ is far
above both the Staiger–Stock benchmark of $10$ and the Stock–Yogo / Olea–Pflueger critical values. By the
$1/(F+1)$ heuristic, 2SLS retains roughly $1/(42+1)\approx 0.023$ — about $2.3\%$ — of OLS's bias, i.e. it
has shed essentially all of it. (Caveat for the careful referee: this $F$ should ideally be the
*heteroskedasticity-robust effective $F$* per Section 3.5.7, not a non-robust first-stage $F$; if the authors
report only the latter, ask for the former. But at a value of $42$ the design is comfortably strong on
relevance.) Relevance is the *one* question the data can answer cleanly, and this paper answers it well — so
the referee's attention must move entirely to exclusion (part c).

**(c)** [6 pts] Exclusion requires that examiner leniency move firm value *only* through the grant decision.
The back door is any channel by which the *assigned examiner* touches firm value without going through
whether the patent is granted. Two distinct channels (any two of these earn full credit):

1. **Timing / pendency.** Lenient examiners may also be *faster* (or slower), so the assigned examiner shifts
   how long the application is pending, not just whether it is granted. A faster decision lets the firm
   commercialize or raise capital sooner, affecting market value through a timing channel independent of the
   grant. *Defense:* control for examiner pendency / decision lag, or show leniency is uncorrelated with
   speed.
2. **Scope of the granted claims.** Examiners differ not only in *whether* they grant but in how broad a set
   of claims they allow. A lenient examiner might grant *narrower* claims; claim breadth affects the patent's
   commercial value directly. So leniency could affect $y$ through claim scope conditional on grant.
   *Defense:* control for granted claim count/breadth, or restrict to the binary grant margin and argue scope
   is orthogonal to leniency.
3. **Non-random assignment within art unit.** If higher-quality applications are routed to particular
   examiners (e.g., specialists), assignment is not as-good-as-random and leniency proxies application
   quality, which drives firm value directly. *Defense:* demonstrate balance of observable application
   characteristics across examiners within art-unit × year cells (a randomization-check table).

The common structure: each is a path from the assigned examiner to firm value that *bypasses* the grant
indicator, which is exactly an exclusion violation. A good paper anticipates and closes these; a bad one
pretends they do not exist.

**(d)** [4 pts] The instrument moves the grant outcome only for **marginal applications** — those whose
*quality is near the grant threshold*, so that a lenient examiner grants them but a strict examiner would
reject them. Those are the **compliers**: borderline applications whose fate is decided by the luck of which
examiner they drew. The **always-takers** are clearly patentable applications granted by every examiner
regardless of leniency; the **never-takers** are clearly unpatentable applications rejected by everyone. IV
estimates the **LATE**: the effect on firm value of a granted patent *for marginal, near-threshold
applications.* So the $8.1\%$ answers the narrow question "what does a granted patent do to value for firms
whose patentability was borderline" — **not** the universal effect of patenting on value. The title *"Does
Patenting Raise Firm Value?"* therefore **overclaims**: it advertises a population-wide effect while the
design identifies only the complier (marginal-application) effect, the precise overreach the chapter's
question 4 warns about.

**(e)** [2 pts] "It's standard in the literature" is an appeal to precedent, not an argument about *this*
setting's back doors. Exclusion is fundamentally **untestable in the just-identified case** (part a) and must
be defended by reasoning through the specific channels — timing, scope, assignment — that could carry the
instrument to the outcome around the treatment. That other papers used examiner leniency tells you nothing
about whether *those* channels are closed in *this* data; a design that is standard can still be wrong, and
"standard" is exactly the kind of misdirection question 3 of the checklist is built to see through. Exclusion
is an argument, not a citation and not a statistic.

---

## Problem 2 — Why Anderson–Rubin stays valid, and how to read its shapes (18 pts)

**(a)** [5 pts]
(i) The 2SLS estimator is a **ratio** whose denominator is the first stage,
$\hat\beta_{\text{IV}} = \widehat{\operatorname{Cov}}(z,y)/\widehat{\operatorname{Cov}}(z,x)$. When the
instrument is weak, the denominator $\widehat{\operatorname{Cov}}(z,x)$ **hugs zero and is itself estimated
with error.** Dividing by a near-zero, noisy quantity makes the sampling distribution of the ratio fat-tailed
and skewed — nothing like the normal the conventional standard-error formula assumes. That formula linearizes
around the denominator and badly *underestimates* the true spread, so the reported SE is too small and the
interval too narrow.
(ii) The Anderson–Rubin test is immunized because **no first stage appears anywhere.** Instead of estimating
$\beta$ and dividing, AR tests each candidate value $\beta_0$ directly in a *plain reduced-form regression* of
the constructed variable $y-\beta_0 x$ on $z$. There is no ratio and no denominator near zero, so the $F$-test
keeps its promised size — a 5% test rejects a true null exactly 5% of the time — **regardless of first-stage
strength.** AR moves the inference off the dangerous division entirely.

**(b)** [4 pts] The recipe for testing $H_0:\beta=\beta_0$:
1. **Construct** the adjusted outcome $\text{adj} = y - \beta_0 x$ — the outcome with the *hypothesized*
   treatment effect subtracted out.
2. **Regress** $\text{adj}$ on the instrument $z$ (and any controls).
3. **Test** the coefficient on $z$ for zero with an ordinary $F$-test.
Under $H_0$, if exclusion holds, $z$ touched $y$ *only through* $x$; subtracting $\beta_0 x$ removes exactly
$x$'s effect, leaving a quantity $z$ has no relationship with — so the coefficient on $z$ must be **zero**.
A significant coefficient means $\beta_0$ is the wrong effect (we have not fully removed $x$'s influence) and
we reject. **Inversion** turns this into a confidence interval: sweep $\beta_0$ over a grid, run the AR
$F$-test at each, and **collect every $\beta_0$ the test fails to reject** at the 5% level. That set is the
95% AR confidence interval; by construction it contains the true $\beta$ in 95% of samples, weak instrument
or not.

**(c)** [5 pts]
(i) An unbounded AR interval is **the honest face of a weak instrument.** It says: given how little this
instrument moves the treatment, the test has no power — for almost any $\beta_0$, the adjusted outcome
$y-\beta_0 x$ shows no significant relationship with $z$ (because $z$ is barely related to *anything*), so
almost nothing gets rejected and the interval balloons to the whole real line. The design has **failed to
identify the parameter**: the data are consistent with essentially any effect size, including enormous ones.
(ii) The coauthor's plan is **not sound.** The 2SLS point estimate is the ratio that divides by the very weak
first stage the AR interval just exposed; reporting it "as a best guess" is reporting an artifact of dividing
by near-zero. On the same data the conventional 2SLS interval would have come back *tight and specific* — and
would have been lying, since its normal approximation is invalid at this first-stage strength. The unbounded
AR interval is what the conventional interval *should* have looked like; the correct conclusion is "this
instrument cannot answer the question," not a number.

**(d)** [4 pts]
(i) An empty AR interval can **only** arise under over-identification (more instruments than regressors)
because emptiness means the instruments *disagree* about $\beta$: no single value of $\beta_0$ can
simultaneously make *all* instruments uncorrelated with the adjusted outcome. With a single instrument
(just-identified) there is always some $\beta_0$ that drives the one coefficient to zero, so the interval can
never be empty — there is nothing for instruments to disagree about.
(ii) An empty interval diagnoses a failure of the **exclusion restriction or model specification**: at least
one instrument is invalid, or the model is misspecified, so the instruments cannot all be telling the truth.
It does **not** mean "the effect is zero" — zero is just one more $\beta_0$ that gets rejected along with
every other value. This is the same **disagreement principle** that drives the overidentification test of
Problem 4: the empty AR interval is AR detecting, through its own machinery, exactly what a rejected Sargan/
Hansen-$J$ test detects — that the surplus instruments point in incompatible directions.

---

## Problem 3 — The Bound–Jaeger–Baker lesson and the $1/(F+1)$ heuristic (16 pts)

**(a)** [5 pts] By the $1/(F+1)$ heuristic at $F=3.8$:
$$\frac{1}{F+1} = \frac{1}{3.8+1} = \frac{1}{4.8} \approx 0.208,$$
so 2SLS carries roughly **$21\%$ of OLS's bias.** This is **not a coincidence:** with a weak first stage,
2SLS is *expected* to sit a fair way toward OLS rather than at the truth. We can see the prediction line up
with the numbers: OLS is $0.55$, 2SLS is $0.42$, so 2SLS has moved only a fraction of the way *down* from OLS
— consistent with retaining about a fifth of the bias. Since OLS is biased *upward* and the residual 2SLS
bias points *toward OLS* (Section 3.5.2), the $0.42$ is still biased **upward relative to the unknown truth**
— the true effect is plausibly *below* $0.42$, not above it. The very bias the authors fled with IV has been
handed back to them in diluted form.

**(b)** [4 pts] **No.** The conventional 2SLS SE relies on the **normal/asymptotic approximation to the
sampling distribution of the ratio estimator**, which assumes the first-stage denominator is comfortably away
from zero. At $F=3.8$ that approximation **fails**: the true sampling distribution is fat-tailed and skewed,
and the linearized formula *underestimates* its spread — so the reported SE of $0.11$ is **too narrow**, the
interval too tight, and the three stars overstate the precision. The danger is precisely that the SE looks
*reassuring* while being invalid; the small SE is not evidence of a reliable estimate, it is a symptom of the
pathology.

**(c)** [4 pts] The Bound–Jaeger–Baker (1995) lesson: **statistical significance of the first stage is not
the same as strength.** In their re-examination of Angrist–Krueger's quarter-of-birth instrument for
schooling, the first stage was *significant* — but only because the sample ran to hundreds of thousands; the
instrument explained a minuscule fraction of the variation in schooling, leaving the design weak in the sense
that matters. Their devastating demonstration: they replaced the real quarter-of-birth instrument with a
**randomly generated** one — pure noise, correlated with nothing — and 2SLS *still* produced a "significant,"
plausible-looking schooling coefficient with a respectable standard error. A random number posing as an
instrument **manufactured a causal estimate.** This proves that a small, significant-looking 2SLS standard
error is no reassurance at all when the first stage is weak: the machinery will conjure a confident answer
out of essentially nothing, and the conventional SE will not warn you. You must check the first-stage $F$
against weak-instrument critical values, not against a $t$-stat of 2.

**(d)** [3 pts] Demand the **Anderson–Rubin 95% confidence interval** (weak-instrument-robust inference). If
the instrument is in fact too weak to identify the effect, the AR interval would come back **very wide,
plausibly unbounded** — stretching to $\pm\infty$ or a finite segment plus two infinite rays — honestly
declaring that the data cannot pin down $\beta$. That shape would reveal the tight conventional interval
around $0.42$ as an artifact of dividing by a feeble first stage, and the right conclusion would become "this
instrument cannot answer the question," not "$0.42$." (Reporting the Olea–Pflueger effective $F$ alongside it
would corroborate the diagnosis.)

---

## Problem 4 — The overidentification test: what a passed J really certifies (14 pts)

**(a)** [4 pts] The Sargan (1958) / Hansen-$J$ (1982) test regresses the **instruments against the IV
residuals** $\hat u = y - x\hat\beta_{\text{IV}}$ and measures their total correlation. A *valid* instrument
is uncorrelated with the structural error by exclusion, so under the **null hypothesis that all instruments
are valid**, each should show no relationship with $\hat u$, and the $J$ statistic follows a chi-squared
distribution. A **large $J$ (small $p$-value) rejects** the joint null: at least one instrument is correlated
with the error — at least one violates exclusion. The **degrees of freedom equal the number of
over-identifying restrictions**, $L - 1$ where $L$ is the number of instruments for one regressor. Here
$L=2$, so $\text{df} = 2 - 1 = 1$: two instruments give one surplus restriction — one independent way for the
instruments to disagree, hence one degree of freedom.

**(b)** [4 pts] Two distinct errors:
1. **What the test detects.** The $J$ test detects *disagreement* among the instruments, not validity. A
   passed $J$ is the **absence of evidence of disagreement**, not evidence of exclusion — it says the two
   instruments point to compatible values of $\beta$, nothing more. "Confirms exclusion" reads absence of a
   flag as a certificate, which it is not.
2. **The all-invalid-together scenario.** The test can only catch *relative* disagreement. If **both**
   instruments are invalid *in the same direction* — sharing the same back door — they will agree perfectly,
   the residual will look uncorrelated with both, and $J$ will pass. So a clean $J$ is fully consistent with
   *both* instruments being invalid; it cannot rule that out (part c).

**(c)** [3 pts] If both instruments are correlated with the same omitted regional economic-vitality factor
that also lowers cost of capital, then **both are biased the same way**, so each implies the *same* (wrong)
$\beta$. The $J$ test only measures whether the instruments *disagree*; since they agree (both shifted by the
identical back door), the test finds no disagreement and **passes**. This proves that **a clean $J$ does not
certify exclusion** — it certifies only that the instruments are not *contradicting each other*. Common
invalidity is invisible to the test, exactly as the chapter warns. Exclusion remains an argument Priya must
make about the regional-vitality channel directly, not a box the $J$ statistic can check.

**(d)** [3 pts] For a **just-identified** design (one instrument, one regressor) there are $L - 1 = 1 - 1 =
\mathbf{0}$ over-identifying restrictions, so **the $J$ test is unavailable** — there is no surplus
instrument, nothing to check, the test is empty (Problem 1a). What the analyst is left with is the same thing
Problem 1(e) insisted on: **a defended argument about back-door channels** — reasoning through every path by
which the instrument could reach the outcome around the treatment — because no statistic can substitute for
that argument when there are no over-identifying restrictions to test.

---

## Problem 5 — Weak-IV diagnosis: first-stage F, effective F, and what to do (16 pts)

**(a)** [5 pts]
(i) The **Olea–Pflueger (2013) effective $F$** corrects for **heteroskedasticity (and the many-instrument
setting)**, which the conventional non-robust first-stage $F$ ignores. The conventional $F$ assumes
homoskedastic first-stage errors; when errors are heteroskedastic — as Sam's are — that assumption is wrong
and the conventional $F$ can *overstate* identification strength. The effective $F$ is built to measure
identification strength honestly under exactly these conditions.
(ii) When the two disagree, **the effective $F$ is the one to believe** because Sam *has* heteroskedasticity,
which is precisely the situation the conventional $F$ mishandles and the effective $F$ was designed for. So
the real diagnosis is the effective $F$ of $5.2$ (below its critical value), not the conventional $11.6$:
identification is **weak**, and the "above 10, so we're fine" reasoning rests on the wrong statistic.

**(b)** [4 pts] With an effective $F$ of $5.2$, below its critical value, **identification is weak.** By the
$1/(F+1)$ intuition, 2SLS retains roughly $1/(5.2+1)\approx 0.16$ — about a sixth — of OLS's bias, so Sam's
2SLS estimate is pulled **toward the OLS estimate** (toward the endogeneity he used IV to escape). On
inference: his **conventional 2SLS interval will be too narrow and possibly centered on the wrong place** —
falsely confident, because the normal approximation to the ratio fails at this strength — while an
**Anderson–Rubin interval on the same data will be wide, possibly unbounded, and honest**, reflecting how
little this instrument actually pins down. The contrast (tight-and-lying vs. wide-and-honest) is the whole
lesson of the chapter.

**(c)** [4 pts]
(i) This invites **many-instruments bias.** Mechanism: 2SLS replaces the endogenous $x$ with its first-stage
fitted value $\hat x$ — the projection of $x$ onto the instruments. With many instruments, that projection
**overfits**, letting the first stage chase the *idiosyncratic noise* in $x$ — and the noise in $x$ is
exactly the endogenous part correlated with the structural error. So $\hat x$ starts to recover the very
endogeneity IV was meant to purge; as the instrument count grows toward the sample size, $\hat x \to x$ and
**2SLS collapses back toward OLS** — the worst case of the toward-OLS bias. The conventional first-stage $F$
of $>20$ is the *trap*, not reassurance: a high $F$ bought by stuffing in weak interacted instruments.
(ii) The **effective $F$ will not be fooled.** Olea–Pflueger is built precisely to flag weak identification
honestly in heteroskedastic *and many-instrument* settings; it does not reward you for piling up junk
instruments. That is why the chapter calls it the right diagnostic — a high conventional $F$ from many weak
instruments is exactly what it is designed to see through.

**(d)** [3 pts] Sam should **find a *better* instrument, not *more* of them** — a few strong instruments beat
many weak ones, always; the fix for low identification strength is stronger relevance from a genuinely
exogenous source, not interactions that manufacture a high conventional $F$. And regardless of first-stage
strength he should **report the Anderson–Rubin confidence interval**, which stays valid whether the
instrument is strong or weak, so a reader can judge the result honestly rather than trusting a conventional
SE that the pathology has corrupted.

---

## Problem 6 — Design-critique essay: apply the referee checklist to a finance scenario (16 pts)

This is graded against the six required components of the §3.5.9 ledger. A model report follows; full credit
requires the substance of each bracketed component, in order, in roughly 250–400 words.

**Model referee report.**

*Relevance* [3 pts]. The reported first-stage $F$ of $7.5$ is **below the Staiger–Stock benchmark of $10$**
and below standard weak-instrument critical values — a single-digit $F$ is a klaxon. By the $1/(F+1)$
heuristic the 2SLS estimate still carries about $1/(7.5+1)\approx 0.12$, roughly $12\%$, of OLS's bias,
pulling it *toward* the endogenous OLS estimate it was meant to escape. Worse, default data are almost
certainly heteroskedastic, so the relevant statistic is the **Olea–Pflueger (2013) effective $F$**, which the
author does not report; given heteroskedasticity the effective $F$ is likely *lower* still than $7.5$. I would
require it before believing the design is identified.

*Exclusion* [4 pts]. Officer assignment must affect default *only* through approval. But loan officers do far
more than approve: they set **loan terms** (interest rate, loan amount, collateral requirements), which
directly affect a borrower's ability to repay regardless of the binary approval; they may **monitor or coach**
borrowers differently, affecting default through effort rather than access; and **assignment may not be
random** if certain applicant types are routed to certain officers, so officer strictness proxies borrower
quality and reaches default directly. Each is a back door from officer to default that bypasses the approval
indicator. "Loan-officer assignment is plausibly exogenous" is an **assertion, not an argument** — it names no
channel and closes none; in a just-identified design exclusion is untestable and must be defended by reasoning
through exactly these paths.

*Compliers / LATE* [3 pts]. The instrument moves approval only for **marginal applicants near the approval
threshold** — those a lenient officer approves but a strict one rejects. These are the **compliers**.
**Always-takers** are clearly creditworthy applicants approved by every officer; **never-takers** are clearly
unqualified applicants rejected by all. The 6-point estimate is therefore the **LATE for marginal
borrowers**, not the universal effect of "access to credit"; the abstract's broad framing **overreaches** the
complier-specific estimate.

*Identification count* [2 pts]. One instrument (officer approval rate), one endogenous regressor (approval):
**just-identified.** Hence $L-1=0$ over-identifying restrictions and **no Sargan/Hansen-$J$ test is
available** — there is no internal check on exclusion, which makes the argument in the *Exclusion* paragraph
the load-bearing defense.

*Honest inference* [2 pts]. The author reports **no Anderson–Rubin interval.** Given the low first-stage $F$,
an honest AR interval could plausibly be **very wide or unbounded**, in which case the headline 6-point
result is an artifact of dividing by a weak first stage and the real answer is "the data cannot say." I would
require the AR interval before trusting the SE of $2.9$ points.

*Verdict and connection to Maya's question* [2 pts]. **Revise-and-resubmit at best, leaning toward
reject-as-uninformative:** the design fails the relevance bar, mounts no real exclusion argument, has no
$J$-test option, and omits weak-IV-robust inference, so the confident 6-point result is not yet credible. For
Maya's own fair-lending work the lesson is exact: a credible causal number where unobserved borrower quality
confounds everything is *earned by the design*, not by a tight standard error — relevance must clear the
weak-IV bar, exclusion must be argued channel by channel, and inference must be reported in a form (Anderson–
Rubin) that does not collapse when the instrument is weak. This is the IV analog of the Chapter 2.5 lesson:
the diagnostics that decide credibility live *outside* the point estimate.

A full-credit report hits all six components in order, argues exclusion with concrete channels (not generic
worry), correctly identifies the complier population and the just-identified status, flags the missing AR
interval, and renders a reasoned verdict — inventing no numbers beyond those given.

---

*End of solutions for Problem Set 3.5. The through-line of Week 3: each causal strategy trades one heroic,
largely untestable assumption for another — conditional independence for matching, exclusion for IV — and the
art is knowing which your setting can support. The diagnostics this set drilled (first-stage and effective
$F$, the Anderson–Rubin interval, the overidentification test) are the tools that keep IV honest, all living
*outside* the 2SLS point estimate. Week 4 changes the game with **design-based** methods that exploit
structure in the data itself — difference-in-differences differences away fixed confounders through panels,
regression discontinuity manufactures a local experiment at an arbitrary cutoff, synthetic control builds a
bespoke counterfactual — needing fewer leaps of faith. Maya's fair-lending question and Leah's patent question
return there with designs whose credibility comes from the shape of the natural experiment.*
