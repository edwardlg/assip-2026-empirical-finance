# Ch 3.4 — Instrumental Variables

For three chapters now we have been living inside a single, generous assumption. Chapters 3.2 and 3.3 took the **conditional independence assumption** — CIA, the idea that once you condition on enough observed covariates, treatment is as good as randomly assigned — and squeezed everything they could out of it: matching, propensity scores, entropy balancing, doubly-robust estimation. Every one of those tools is a different clever way of comparing treated and untreated units who look identical *on the variables you measured*. And every one of them dies the same death the moment a confounder you did **not** measure is in the room. Chapter 2.5 named that death precisely: when a relevant, correlated variable sits in the error term, $\mathbb{E}[\varepsilon \mid D] \neq 0$, the regressor $D$ is **endogenous**, and no amount of conditioning on the *observed* covariates can save you, because the thing doing the damage is by definition not among them.

This chapter is the escape hatch. Instrumental variables — IV — is the first design in this book that does not require you to observe and condition on the confounder. It requires something else entirely: a *third* variable, an **instrument** $Z$, that wiggles the treatment $D$ around for reasons that have nothing to do with the confounder, and then reads the causal effect off how the outcome $Y$ responds to *that* exogenous wiggle. If you can find such a $Z$ — and that "if" is the whole game — you can identify a causal effect even with an unobserved confounder, even with reverse causality, even with the classical measurement error that attenuated your coefficient in Chapter 2.5. IV is the Swiss Army knife of the endogeneity problems we cataloged in the bias–consistency ledger.

The price of admission is steep and it is intellectual, not computational. The arithmetic of IV is a two-line matrix formula and one function call. The *argument* — that your instrument is valid — is unfalsifiable in part, and a career's worth of empirical fights have been about exactly that argument. So this chapter splits cleanly. First, the trick: what IV solves, the two conditions an instrument must satisfy, the Wald estimator, and two-stage least squares (2SLS) seen through the Frisch–Waugh–Lovell lens you built in Chapter 2.3. Then, the fine print: *whose* effect IV actually estimates — the **LATE**, the local average treatment effect, which is the single most important and most misunderstood fact about modern IV — and what goes wrong when the instrument is **weak**. We will set up the weak-instrument problem carefully and hand the full pathology, and the inference that survives it, to Chapter 3.5.

Throughout, Maya is our guide. She still wants to know whether financial-literacy training actually helps people manage debt, and she still cannot run the clean regression, because the people who sign up for a free financial-literacy class are not like the people who do not — they are more motivated, more organized, more worried about money, in ways no dataset fully records. That unobserved motivation is the confounder. CIA fails. We need an instrument.

---

## 1. The result in one plain sentence

> **IV, stated plainly.** If you can find a variable $Z$ that shoves the treatment $D$ around but has no other path to the outcome $Y$, then the causal effect of $D$ on $Y$ is the ratio of two things you *can* measure: how much $Y$ moves with $Z$, divided by how much $D$ moves with $Z$.

That ratio is the whole idea. Read it as a kind of leverage. You cannot move $D$ yourself in a clean way — every natural shove on $D$ in the data drags the confounder along with it. But $Z$ can shove $D$ cleanly, and the only way that shove can reach $Y$ is *through* $D$. So whatever response you see in $Y$ when $Z$ changes must have traveled the one open road, $Z \to D \to Y$. Divide the $Y$-response by the $D$-response and the units of $Z$ cancel, leaving the effect of $D$ on $Y$ per unit of $D$. The instrument is a lever; the denominator tells you how hard the lever pushed the treatment; the numerator tells you how far the outcome moved; the ratio is the mechanical advantage.

Everything technical in this chapter is an elaboration of that ratio. The Wald estimator *is* that ratio for a binary instrument. 2SLS is that ratio generalized to many regressors and controls. The LATE theorem is the discovery that "the effect of $D$" in that sentence is sneakier than it sounds — it is the effect for the particular people whom $Z$ actually managed to shove. And weak instruments are what happens when the denominator — how much $D$ moves with $Z$ — is close to zero, so that dividing by it amplifies every imperfection into nonsense.

---

## 2. The problem IV solves: a regressor you cannot trust

Let us be exact about what is broken, in the notation of Week 3. Maya posits a causal model for a person $i$:

$$
Y_i = \beta_0 + \beta_1 D_i + \varepsilon_i,
$$

where $Y_i$ is a debt-health outcome (say, the change in credit-card balance over the next year, coded so that *lower* is better), $D_i \in \{0,1\}$ indicates whether person $i$ completed the financial-literacy course, and $\beta_1$ is the causal effect she is after — what completing the course *does* to debt, holding the person fixed. In the potential-outcomes language of Chapter 3.1, $\beta_1$ is the average of the unit-level effects $Y_i(1) - Y_i(0)$ (we will refine *which* average in §6). For OLS to recover $\beta_1$, Chapter 2.2's zero-conditional-mean assumption must hold: $\mathbb{E}[\varepsilon_i \mid D_i] = 0$.

It does not. The error $\varepsilon_i$ contains everything about person $i$ that affects their debt and is not the course — and the dominant such thing is **financial motivation**, the unmeasured tendency to budget, save, and avoid revolving debt. Motivated people both (a) sign up for the course ($D_i = 1$) and (b) have better debt outcomes anyway ($\varepsilon_i$ low). So $D_i$ and $\varepsilon_i$ move together: $\operatorname{Cov}(D_i, \varepsilon_i) < 0$, and $\mathbb{E}[\varepsilon_i \mid D_i = 1] < \mathbb{E}[\varepsilon_i \mid D_i = 0]$. The regressor $D_i$ is **endogenous**. Run OLS and $\hat{\beta}_1$ converges to $\beta_1$ plus a bias term:

$$
\hat{\beta}_1^{\text{OLS}} \xrightarrow{p} \beta_1 + \frac{\operatorname{Cov}(D, \varepsilon)}{\operatorname{Var}(D)}.
$$

This is the same disease as the omitted-variable bias of Chapter 2.5 — motivation is a relevant variable, correlated with $D$, banished into the error — and Maya cannot cure it by conditioning, because she has no column for motivation. CIA, the engine of Chapters 3.2–3.3, is exactly the assumption that no such unobserved confounder exists, and here it fails by construction.

Endogeneity has three classic faces, all of which IV addresses, and you have met all three:

- **Unobserved confounding** (this case): a variable in $\varepsilon$ drives both $D$ and $Y$. Motivation drives course-taking and debt.
- **Simultaneity / reverse causality**: $Y$ also causes $D$. A firm's stock-price crash risk might *itself* change how much investors want to short it, so short interest and crash risk are jointly determined — you cannot tell which way the arrow points by regression alone.
- **Measurement error**: from Chapter 2.5, classical noise in a regressor, $x = x^* + m$, mechanically correlates the regressor with the error and attenuates the slope toward zero. A valid instrument for $x^*$ undoes the attenuation, because the instrument is correlated with the true $x^*$ but not with the noise $m$.

In all three, the fix is the same: find variation in $D$ that is *not* contaminated. That variation is what an instrument supplies.

---

## 3. The two conditions for a valid instrument

An instrument $Z$ earns its name by satisfying two conditions. They are not symmetric in how you defend them, and learning the asymmetry is half of becoming a competent empiricist.

**Condition 1 — Relevance.** The instrument must actually move the treatment:

$$
\operatorname{Cov}(Z, D) \neq 0.
$$

The instrument has to be connected to $D$, or there is no lever at all — the denominator of our magic ratio is zero and the whole thing is undefined. The good news: relevance is a statement about two variables you both observe, $Z$ and $D$, so it is **testable**. You estimate the **first stage** — the regression of $D$ on $Z$ — and look at whether the coefficient is real. We will spend §8–§9 on *how strong* that connection must be, because "nonzero" turns out to be a dangerously low bar.

**Condition 2 — Exclusion (exogeneity).** The instrument must affect the outcome *only through* the treatment, and must be unrelated to the confounder. Formally, $Z$ is uncorrelated with the structural error: $\operatorname{Cov}(Z, \varepsilon) = 0$. Pictorially, the only arrow leaving $Z$ goes into $D$:

$$
Z \longrightarrow D \longrightarrow Y, \qquad \text{and \emph{no} arrow } Z \longrightarrow Y \text{ that bypasses } D, \qquad \text{and no } Z \longleftrightarrow \varepsilon.
$$

This bundles two ideas that are worth separating in your head. First, **as-good-as-random assignment of $Z$**: the instrument itself must not be tangled up with the confounder (motivation must not predict $Z$). Second, the **exclusion restriction proper**: even granting that $Z$ is randomly assigned, it must not have its *own* direct channel to $Y$. Both must hold, and here is the brutal part — **the exclusion restriction is fundamentally untestable.** You cannot check $\operatorname{Cov}(Z, \varepsilon) = 0$ because $\varepsilon$ is unobserved; that is the very reason you are doing IV. There is no test, no diagnostic, no $p$-value. The exclusion restriction must be **argued**, from institutional knowledge and economic logic, and defended against every clever critic who proposes an alternative path $Z \to Y$. This is why IV papers spend pages, not paragraphs, justifying their instrument: the credibility of the entire result rests on a claim that the data can never confirm.

Hold the asymmetry firmly: **relevance is testable, exclusion is arguable.** A weak instrument is a statistical problem you can measure and partly fix. An invalid instrument — one that violates exclusion — is a logical problem that no amount of data will reveal, and it poisons your estimate without leaving a fingerprint.

### Maya's instrument

Maya's nonprofit ran a recruitment campaign for its financial-literacy course. Limited budget meant they could not mail everyone, so — and this is the design that makes IV possible — they **randomly** selected which households received a glossy promotional mailer with a sign-up link and a small completion incentive. Let $Z_i = 1$ if household $i$ was mailed, $Z_i = 0$ otherwise. Mailing is the instrument.

Check the two conditions, naming each explicitly as CONVENTIONS §4 demands:

- **Relevance.** Did the mailer raise course completion? Almost certainly: people who get a nudge and an incentive are more likely to enroll. This is the first stage, $D_i = \pi_0 + \pi_1 Z_i + \nu_i$, and Maya can *test* it — she expects $\pi_1 > 0$ and will check that it is large enough (§8). Plausible and verifiable.
- **Exclusion.** Does receiving the mailer affect debt outcomes *only* by getting people into the course, and is it unrelated to motivation? The randomization buys the second half directly: because mailing was assigned by a coin flip, $Z_i$ is statistically independent of motivation and every other confounder — $Z \not\leftrightarrow \varepsilon$ by design. The first half — *no direct path* — is the part Maya must argue. Could the mailer improve debt outcomes *without* the course? Perhaps a person reads the glossy brochure's budgeting tips and improves on their own, never enrolling. Perhaps the mailer's mere arrival makes people think about money. If so, $Z$ reaches $Y$ around $D$, exclusion fails, and Maya's estimate is contaminated. She defends exclusion by arguing the mailer was content-light (a sign-up link, not a budgeting lesson) and that any priming effect is negligible relative to a full course. Notice she cannot *prove* this; she can only make it credible.

Random assignment of the instrument is the gold standard precisely because it secures the hardest half of exclusion — independence from the confounder — for free. The classic "natural experiment" instruments work the same way by borrowing randomness from the world: **rainfall** as an instrument for crop income (rain is as-good-as-random and plausibly affects the local economy only through agriculture), or **quarter of birth** as an instrument for years of schooling (compulsory-schooling laws tied to birthdates create exogenous variation in how long students stay enrolled). Each lives or dies on the same untestable exclusion claim: rainfall must not affect the outcome except through income; birth-quarter must not affect earnings except through schooling. When you read these designs in Chapter 3.5 and beyond, train yourself to ask, every single time: *what is the relevance evidence, and what is the exclusion argument?*

---

## 4. The Wald estimator: IV for a binary instrument

Start with the simplest possible case, because the formula is transparent and the intuition is total: a binary instrument $Z \in \{0,1\}$, a binary treatment $D \in \{0,1\}$, no controls. This is exactly Maya's setup — mailed or not, completed or not.

Recall the magic ratio from §1: the effect is "how $Y$ moves with $Z$" over "how $D$ moves with $Z$." With a binary instrument, "moves with $Z$" is just a difference in means between the $Z=1$ and $Z=0$ groups. So define:

$$
\hat{\beta}_1^{\text{Wald}} = \frac{\overline{Y}_{Z=1} - \overline{Y}_{Z=0}}{\overline{D}_{Z=1} - \overline{D}_{Z=0}}.
$$

This is the **Wald estimator**. The numerator is the **reduced form** — the raw effect of the mailer on debt, ignoring the course entirely (it is exactly the difference-in-means you would compute in a randomized experiment where the "treatment" is the *offer*, the mailer). The denominator is the first stage — the effect of the mailer on completion, i.e., the share of mailed people who took the course minus the share of unmailed people who did. The Wald estimator scales up the reduced form by the first stage.

### A number

Suppose Maya's data look like this:

| Group | Share completing course ($\overline{D}$) | Mean balance change ($\overline{Y}$, \$) |
|---|---|---|
| Mailed ($Z=1$) | $0.40$ | $-120$ |
| Not mailed ($Z=0$) | $0.10$ | $-30$ |

The mailer raised completion from $10\%$ to $40\%$, a first stage of $\overline{D}_{Z=1} - \overline{D}_{Z=0} = 0.30$. The mailer lowered the average balance change from $-\$30$ to $-\$120$, a reduced form of $\overline{Y}_{Z=1} - \overline{Y}_{Z=0} = -\$90$. The Wald estimate is

$$
\hat{\beta}_1^{\text{Wald}} = \frac{-90}{0.30} = -300.
$$

Read it carefully. The mailer, on average, improved balances by \$90. But the mailer only got an extra $30\%$ of people into the course. If we believe the *only* way the mailer helped was by getting people into the course, then that \$90 improvement was produced entirely by the $30\%$ who enrolled because of it. So the per-completer effect must be $90 / 0.30 = \$300$ of improvement. The Wald estimator is dividing the diluted, intention-to-treat-style reduced form by the dose of treatment the instrument actually delivered, to recover the effect on the people who responded.

Why does this beat OLS? OLS would compare *all* completers to *all* non-completers — including the highly-motivated people who would have completed the course no matter what, and whose great debt outcomes have nothing to do with the course. The Wald estimator never makes that contaminated comparison. It only ever compares the mailed group to the unmailed group, and since mailing was random, those two groups are identical in motivation. The contrast is clean. The price — and it is the central subtlety of all IV — is that "$\$300$" is the effect for a *specific subpopulation*, the people the mailer moved. We unpack exactly who they are in §6.

One more reading of the same formula, to lock it in. By the law of total probability, the reduced form decomposes as the first stage times the effect-per-complier; dividing recovers the effect-per-complier. The instrument's job is to *deliver a dose of treatment*; the Wald ratio strips the offer back down to the effect of the dose.

---

## 5. 2SLS as Frisch–Waugh–Lovell with an instrument

The Wald estimator handles one binary instrument and no controls. Real problems have continuous treatments, multiple controls, and sometimes multiple instruments. The general workhorse is **two-stage least squares (2SLS)**, and the cleanest way to understand it — for you specifically, having done Chapter 2.3 — is as Frisch–Waugh–Lovell with an instrument in place of the raw regressor.

### The two stages, mechanically

Write the structural equation with controls $\mathbf{X}$ (exogenous covariates — age, income, things you *do* trust) and the endogenous treatment $D$:

$$
Y_i = \beta_0 + \beta_1 D_i + \mathbf{X}_i\boldsymbol{\gamma} + \varepsilon_i.
$$

The problem is the single column $D_i$, which correlates with $\varepsilon_i$. 2SLS replaces it with a cleaned-up version in two steps.

**First stage.** Regress the endogenous treatment on the instrument *and the controls*:

$$
D_i = \pi_0 + \pi_1 Z_i + \mathbf{X}_i\boldsymbol{\delta} + \nu_i, \qquad \hat{D}_i = \hat{\pi}_0 + \hat{\pi}_1 Z_i + \mathbf{X}_i\hat{\boldsymbol{\delta}}.
$$

The fitted value $\hat{D}_i$ is the part of the treatment that is *explained by* the instrument and the controls. This is the magic: $\hat{D}_i$ is built only from $Z$ and $\mathbf{X}$, both of which are uncorrelated with $\varepsilon$. So $\hat{D}_i$ inherits their cleanliness — it is the slice of $D$ that has been laundered of the confounder. Whatever motivation was hiding inside $D$ lived in the residual $\nu_i$, which we throw away.

**Second stage.** Regress the outcome on the fitted treatment (and the same controls):

$$
Y_i = \beta_0 + \beta_1 \hat{D}_i + \mathbf{X}_i\boldsymbol{\gamma} + \text{error}.
$$

The coefficient $\hat{\beta}_1^{\text{2SLS}}$ from this second regression is the IV estimate. Because $\hat{D}_i$ is uncorrelated with $\varepsilon$ (it is a function of exogenous things), the zero-conditional-mean assumption is restored *for the regressor we actually use*, and the slope is consistent for $\beta_1$.

A non-negotiable warning that students learn the hard way: **never run the two stages by hand and trust the standard errors.** The second-stage regression on $\hat{D}_i$ produces the correct point estimate, but its reported standard errors are *wrong*, because the software thinks $\hat{D}_i$ is data when really it is an estimate carrying its own sampling noise. The right standard errors account for the first-stage uncertainty. Always use a dedicated 2SLS routine (`linearmodels`' `IV2SLS`), which gets the point estimate and the standard errors right in one call. Hand-rolling the two stages is for *understanding*, never for *reporting*.

### Why this is FWL with an instrument

Here is the connection to Chapter 2.3 that makes 2SLS click. Recall FWL: a multiple-regression coefficient on $D$ equals the simple slope of residualized-$Y$ on residualized-$D$, where "residualized" means *partial out the controls $\mathbf{X}$ from both sides*. OLS partials the controls out of $D$ and then uses what is left of $D$ — including its endogenous part — to explain $Y$. That is precisely the problem: the leftover $\tilde{D}$ still has the confounder in it.

2SLS makes one surgical change. Partial the controls out of everything, exactly as FWL prescribes — call the residualized versions $\tilde{Y}$, $\tilde{D}$, $\tilde{Z}$. But now, instead of regressing $\tilde{Y}$ on $\tilde{D}$ (which is contaminated), use the instrument to extract only the trustworthy part of $\tilde{D}$. The IV slope is

$$
\hat{\beta}_1^{\text{2SLS}} = \frac{\operatorname{Cov}(\tilde{Z}, \tilde{Y})}{\operatorname{Cov}(\tilde{Z}, \tilde{D})}.
$$

Stare at this and you will recognize the Wald ratio from §4 — numerator is how residualized $Y$ moves with the residualized instrument, denominator is how residualized $D$ moves with it — now generalized to live in the FWL world where the controls have already been swept out. OLS is the special case where you put $D$ in the role of its own instrument ($Z = D$), which is exactly the move that fails when $D$ is endogenous. **2SLS is FWL where you replace the contaminated regressor with its instrument.** The first stage *is* the residualize-and-project step; the second stage *is* the simple slope on the cleaned regressor. Everything you proved about partialling-out in Chapter 2.3 carries over — same geometry, same projection logic — with the single twist that the projection is now onto the instrument rather than onto $D$ itself.

This view also tells you instantly what "controls in IV" means and why they go in *both* stages. The controls $\mathbf{X}$ are partialled out of $Y$, $D$, *and* $Z$ alike — they belong in the first stage and the second stage identically, because FWL residualizes every variable in the system against them. Forgetting the controls in the first stage is a classic bug that quietly invalidates the cleaning.

### The matrix form, for completeness

In the matrix notation of Chapter 2.1, collect the instrument(s) and exogenous controls into a matrix $\mathbf{Z}$ (the full set of *exogenous* variables, including $\mathbf{X}$ and the constant) and the regressors into $\mathbf{X}_{\text{all}}$ (the controls plus the endogenous $D$). When the number of instruments equals the number of endogenous regressors (the **just-identified** case), the IV estimator is

$$
\hat{\boldsymbol{\beta}}^{\text{IV}} = (\mathbf{Z}'\mathbf{X}_{\text{all}})^{-1}\mathbf{Z}'\mathbf{y}.
$$

Compare it to OLS, $\hat{\boldsymbol{\beta}}^{\text{OLS}} = (\mathbf{X}_{\text{all}}'\mathbf{X}_{\text{all}})^{-1}\mathbf{X}_{\text{all}}'\mathbf{y}$: the IV estimator swaps the *first* $\mathbf{X}_{\text{all}}$ for $\mathbf{Z}$, replacing the regressor with the instrument in exactly the two places where the troublesome $\operatorname{Cov}(D, \varepsilon)$ would otherwise sneak in. With more instruments than endogenous regressors (**over-identified**), 2SLS uses the projection $\hat{\mathbf{X}}_{\text{all}} = \mathbf{Z}(\mathbf{Z}'\mathbf{Z})^{-1}\mathbf{Z}'\mathbf{X}_{\text{all}}$ (the fitted values from the first stage) and the formula becomes $\hat{\boldsymbol{\beta}}^{\text{2SLS}} = (\hat{\mathbf{X}}_{\text{all}}'\mathbf{X}_{\text{all}})^{-1}\hat{\mathbf{X}}_{\text{all}}'\mathbf{y}$. You will not invert these by hand; you should recognize that the projection matrix $\mathbf{Z}(\mathbf{Z}'\mathbf{Z})^{-1}\mathbf{Z}'$ is the hat matrix of Chapter 2.1, applied to manufacture $\hat{D}$.

---

## 6. LATE: whose effect did you just estimate?

We now arrive at the deepest idea in the chapter, and the one that separates people who *use* IV from people who *understand* it. Go back to the Wald estimate of \$300. It is tempting to call it "the effect of the financial-literacy course." It is not. It is the effect for a specific, invisible subgroup — and Imbens and Angrist (1994) proved exactly which one.[^imbensangrist] The result is the **local average treatment effect (LATE)**, and it reorganizes how you read every IV paper ever written.

[^imbensangrist]: Imbens, G. W., & Angrist, J. D. (1994). Identification and Estimation of Local Average Treatment Effects. *Econometrica*, 62(2), 467–475.

### A taxonomy of four types

The key move is to think about how each person's *treatment status* would respond to the instrument, using the potential-outcomes notation from Chapter 3.1 — but now applied to the treatment itself. Define $D_i(1)$ as the treatment person $i$ *would* take if mailed ($Z_i=1$), and $D_i(0)$ as the treatment they *would* take if not mailed ($Z_i=0$). Just as we never see both potential *outcomes* $Y_i(1), Y_i(0)$, we never see both potential *treatment statuses* — we see $D_i(1)$ for mailed people and $D_i(0)$ for unmailed people, never both for the same person. Every individual falls into one of four types:

| Type | $D_i(0)$ | $D_i(1)$ | Behavior |
|---|:---:|:---:|---|
| **Never-taker** | $0$ | $0$ | Never takes the course, mailed or not. |
| **Always-taker** | $1$ | $1$ | Always takes the course, mailed or not. |
| **Complier** | $0$ | $1$ | Takes the course *if and only if* mailed — the instrument moves them. |
| **Defier** | $1$ | $0$ | Takes the course only if *not* mailed — perversely repelled by the nudge. |

These four types are the heart of LATE, so attach Maya's people to them. The **always-takers** are the highly motivated who would have hunted down the course with or without a mailer — the very people whose self-selection ruined OLS. The **never-takers** are those who, mailer or not, will never enroll. The **compliers** are the swing group: they sit on the fence and the mailer tips them in. The **defiers** are the contrarians who would have enrolled but, annoyed by junk mail, now refuse — a strange type we will assume away in a moment.

Now watch what the instrument can and cannot learn. For an always-taker, $D$ is $1$ whether or not they are mailed, so the mailer changes nothing about their treatment — they contribute *zero* to the first stage and the instrument is blind to their treatment effect. Same for never-takers: $D$ is always $0$, the mailer moves nothing, invisible. The *only* people whose treatment status responds to the instrument are the compliers (and defiers). So when the Wald ratio reads the outcome response off the instrument's wiggle, the only treatment effects in that response belong to **compliers**. IV literally cannot see the effect for always-takers and never-takers, because the instrument never changed their treatment.

### The monotonicity assumption and the theorem

There is one loose end: defiers. If some people are pushed *into* treatment by the instrument while others are pushed *out*, their effects enter the numerator with opposite signs and can cancel or even reverse the estimate. To rule this out, Imbens and Angrist impose **monotonicity**: the instrument moves everyone in the same direction (or not at all). Formally, $D_i(1) \geq D_i(0)$ for all $i$ — the mailer can only *increase* (or leave unchanged) the chance of taking the course, never decrease it. Monotonicity says: **no defiers.** It is usually a mild and defensible assumption — it is hard to imagine many people who would take a course *only* when *not* invited — but like exclusion, it is an assumption about behavior, not a fact you can fully check.

With relevance, exclusion, and monotonicity in hand, the Imbens–Angrist (1994) theorem delivers the punchline:

> **LATE theorem.** Under a valid instrument and monotonicity, the IV (Wald / 2SLS) estimand equals the average treatment effect *among compliers*:
> $$\hat{\beta}_1^{\text{IV}} \xrightarrow{p} \mathbb{E}\!\left[\,Y_i(1) - Y_i(0) \;\middle|\; \text{$i$ is a complier}\,\right] \equiv \text{LATE}.$$

Maya's \$300 is therefore the effect of the course *on the kind of person who takes it because they were mailed* — the fence-sitters. It is **not** the effect on the always-takers (the highly motivated), nor on the never-takers (the unreachable). And that is often exactly the policy-relevant number: if Maya is deciding whether to scale up the *mailer*, the compliers are precisely the people a bigger mailing campaign would reach. But if she wants the effect of the course on the unreachable never-takers — perhaps to argue for *mandatory* financial education — LATE is silent, because no voluntary-uptake instrument can speak to people who never take the course.

This is why "LATE, not ATE" is a mantra in modern applied work. The **ATE** (average treatment effect, the average over *everyone*) and the **ATT** (average over the *treated*, which here is dominated by always-takers) are generally different numbers from the LATE, and they will differ whenever the treatment effect varies across the four types — which it almost always does. Two valid instruments for the same treatment can yield two different LATEs, not because either is wrong, but because they move different sets of compliers. When you read an IV result, the honest question is never just "is the instrument valid?" but also "**who are the compliers, and do I care about them?**" An estimate can be perfectly identified and still answer a question you did not ask.

A small reassurance about external relevance: under the same assumptions, the *size* of the complier group is recoverable — the first stage $\overline{D}_{Z=1} - \overline{D}_{Z=0}$ is exactly the share of compliers (here, $0.30$, so $30\%$ of Maya's population are compliers). You can also characterize compliers' observable traits (average age, income) even though you cannot tag any single person as one. Knowing that compliers are, say, lower-income fence-sitters makes the LATE far more interpretable than a nameless "local" effect.

---

## 7. Reduced form, first stage, and the anatomy of an IV table

Before weak instruments, install a habit. Every honest IV analysis reports three regressions, and you should read them as a set:

1. **First stage**: $D$ on $Z$ (and controls). Establishes *relevance*. You want a large, precisely-estimated coefficient on $Z$. This is where the strength diagnostics of §8 live.
2. **Reduced form**: $Y$ on $Z$ (and controls). The instrument's total effect on the outcome. Crucially, **if the reduced form is a flat zero, your IV estimate is built on nothing** — there is no instrument-driven outcome variation to scale up, and a "significant" 2SLS number coming out of a null reduced form is a red flag that something (usually a weak first stage) has gone wrong.
3. **2SLS**: the ratio, $\hat{\beta}_1^{\text{IV}} = (\text{reduced form}) / (\text{first stage})$ in the just-identified binary case.

A useful sanity identity, true in the just-identified case: the 2SLS coefficient is *exactly* the reduced-form coefficient divided by the first-stage coefficient. If a colleague shows you a 2SLS table without the first stage and reduced form, ask for them — they are where the design lives, and the 2SLS number alone hides the two things that can break it.

This is also where simultaneity and measurement-error applications connect. For Maya's reverse-causality cousin — a researcher worried that crash risk and short interest are jointly determined — an instrument that shifts the *cost or feasibility* of short-selling (a regulatory pilot that randomly relaxes short-sale constraints for some stocks) gives a first stage (does the rule change short interest?) and a reduced form (does the rule change crash risk?), and the ratio identifies the causal effect of short-selling on crash risk for the *complier* stocks — those whose short interest actually responded to the rule. This is the logic behind the Deng, Gao & Kim (2020) natural-experiment design you will meet in Mentor Session 3;[^denggaokim] the regulatory change borrows randomness from the regulator the way Maya's mailer borrows it from the coin flip.

[^denggaokim]: Deng, X., Gao, L., & Kim, J-B. (2020). Short-sale Constraints and Stock Price Crash Risk: Causal Evidence from a Natural Experiment. *Journal of Corporate Finance*, 60, 101498.

---

## 8. Weak instruments: when the lever barely moves

Return to the magic ratio one final time, because its denominator is about to cause all our trouble:

$$
\hat{\beta}_1^{\text{IV}} = \frac{\text{how } Y \text{ moves with } Z}{\text{how } D \text{ moves with } Z}.
$$

What happens as the denominator — the first stage, $\operatorname{Cov}(Z,D)$ — shrinks toward zero? Relevance technically still holds (the covariance is *nonzero*), so the estimator is still defined, still consistent in the limit. But dividing by a number close to zero is numerically violent: tiny errors in the numerator get amplified into enormous errors in the ratio. An instrument with a near-zero first stage is a **weak instrument**, and weak instruments produce three pathologies that, together, can make IV *worse* than the OLS it was supposed to fix.

**Pathology 1 — Bias toward OLS.** This is the counterintuitive killer. You turned to IV to escape OLS's bias; a weak instrument drags you right back to it. Here is why. The fitted treatment $\hat{D}_i$ from the first stage is supposed to be the clean, instrument-driven part of $D$. But when the instrument is weak, $Z$ explains almost none of $D$, so the first-stage fit $\hat{D}_i$ is mostly *not* coming from $Z$ — it is mostly first-stage sampling noise, and that noise is correlated with $\varepsilon$ in finite samples (the first-stage residual $\nu$ and the structural error $\varepsilon$ share the confounder). So $\hat{D}_i$ is contaminated by exactly the endogeneity you were fleeing, and the second-stage slope drifts toward the OLS slope. The approximation is stark: the finite-sample bias of 2SLS, as a fraction of the OLS bias, is roughly

$$
\frac{\mathbb{E}[\hat{\beta}^{\text{2SLS}}] - \beta_1}{\mathbb{E}[\hat{\beta}^{\text{OLS}}] - \beta_1} \approx \frac{1}{F},
$$

where $F$ is the population first-stage F-statistic (defined below). When the first stage is strong ($F$ large), the bias fraction is small and 2SLS is nearly unbiased. When $F$ is near $1$, 2SLS is nearly as biased as OLS — and you paid a large variance penalty for the privilege. This is the result Chapter 3.5 will reproduce in a guided "disaster," where a deliberately weak instrument makes 2SLS hug the OLS bias while its confidence interval lies about its own precision.

**Pathology 2 — Inflated, unreliable variance.** Dividing by a near-zero denominator inflates the sampling variance of the ratio enormously. Weak-IV estimates wobble violently from sample to sample; the standard error balloons, and — worse — the usual asymptotic approximation that justifies the reported standard error and t-statistic breaks down. The textbook confidence interval becomes badly miscalibrated, often far too narrow, so you get overconfident inference around a biased point. (The fix for *inference* under weak instruments — Anderson–Rubin confidence intervals, which stay valid no matter how weak the instrument — is the subject of Chapter 3.5.)

**Pathology 3 — Tiny exclusion violations get amplified.** Suppose the instrument has a small forbidden direct effect on $Y$ — a minor exclusion violation, $\operatorname{Cov}(Z,\varepsilon) = c$ for small $c$. That bias enters the IV estimate as $c / \operatorname{Cov}(Z,D)$. When the first stage is strong, a small numerator violation divided by a large denominator is negligible. When the first stage is weak, that same small violation, divided by a near-zero denominator, blows up. **Weak instruments make you maximally vulnerable to exactly the exclusion violations you cannot test for.** A strong first stage is not just about precision; it is your buffer against the untestable assumption.

### Measuring strength: the first-stage F

Since relevance is testable, weak-instrument *strength* is too — that is the one piece of good news. The standard measure is the **first-stage F-statistic**: the F-statistic for the joint significance of the *excluded instruments* (the $Z$'s, not the controls) in the first-stage regression. With a single instrument it is just the squared t-statistic on $Z$ in the first stage. A large F says $Z$ explains a lot of $D$ beyond the controls — a strong lever. A small F says the lever is loose.

How large is large enough? The famous rule of thumb is **$F > 10$**, and it comes from real theory, not folklore — but the theory has limits you must know.

### Stock–Yogo critical values and the "F > 10" rule

Stock and Yogo (2005) made the question precise.[^stockyogo] They asked: how strong must the first stage be to guarantee that the 2SLS bias is no more than, say, $10\%$ of the OLS bias — or that a nominal $5\%$ hypothesis test rejects no more than $15\%$ of the time under the null? They tabulated **critical values** for the first-stage F that deliver such guarantees, as a function of the number of instruments and the tolerance you choose.

[^stockyogo]: Stock, J. H., & Yogo, M. (2005). Testing for Weak Instruments in Linear IV Regression. In D. W. K. Andrews & J. H. Stock (Eds.), *Identification and Inference for Econometric Models: Essays in Honor of Thomas Rothenberg* (pp. 80–108). Cambridge University Press. For one endogenous regressor and one instrument, the critical value for the "bias $\leq 10\%$ of OLS" guarantee is right around $F \approx 10$ — which is where the rule of thumb comes from. Clear the Stock–Yogo bar and you have a *formal* assurance that the weak-IV bias is bounded small.

But treat "$F > 10$" as a smoke alarm, not a certificate. Its limits matter:

- It was derived under **homoskedastic, non-clustered** errors. With heteroskedasticity or clustering — i.e., almost every finance dataset, as Chapter 2.4 taught you — the standard (non-robust) first-stage F does not correspond to the Stock–Yogo guarantee, and $F > 10$ can badly understate weakness.
- The critical value **rises with the number of instruments**; with many instruments, $10$ is far too lenient.
- More recent work (Lee, McCrary, Moreira, Porter, and others) argues that to keep the *t-test* honest, you may need first-stage F values much larger than $10$ — sometimes above $100$ — once you account for the distortion weak instruments inflict on inference. "$F > 10$" was a guarantee about *bias*, not a license to trust your t-statistic.

So $F > 10$ is necessary hygiene and nowhere near sufficient. Report the first-stage F always; clear $10$ comfortably; and when your errors are non-classical (they are), reach for the robust version below.

### The Olea–Pflueger effective F

Olea and Pflueger (2013), writing in the *Journal of Business & Economic Statistics*, fixed the homoskedasticity hole.[^oleapflueger] They derived an **effective F-statistic** — built from heteroskedasticity- and autocorrelation-robust (and cluster-robust) variance estimates — that measures first-stage strength *under the messy error structures real data have*, and they provide the matching critical values for a chosen bias tolerance. When your errors are heteroskedastic or clustered (the default assumption in finance), the **Olea–Pflueger effective F is the statistic to report and compare against its critical value**, not the classical first-stage F. `linearmodels` computes it for you, and Chapter 3.5's pathology lab will show a case where the classical F looks reassuring while the effective F correctly flags the instrument as dangerously weak. The lesson generalizes the spirit of Chapter 2.4: once you admit your errors are not classical, every diagnostic built on classical errors needs a robust replacement, and the first-stage F is no exception.

[^oleapflueger]: Montiel Olea, J. L., & Pflueger, C. (2013). A Robust Test for Weak Instruments. *Journal of Business & Economic Statistics*, 31(3), 358–369.

> **The weak-IV checklist.** Always report the first stage. Compute the effective F (Olea–Pflueger) with the same robust/clustered errors you use for the second stage. Compare it to the Stock–Yogo / Olea–Pflueger critical value for your tolerance and instrument count — do not just eyeball "$F > 10$." If the instrument is weak, do not paper over it with a t-statistic; switch to weak-IV-robust inference (Anderson–Rubin), which Chapter 3.5 delivers.

---

## 9. The code

Here is the whole chapter in one runnable block: simulate a world with an unobserved confounder where OLS is biased, then recover the truth with 2SLS via `linearmodels`, and read off the first stage and its strength. We build the data so the true effect is $\beta_1 = -2$ (the treatment lowers the balance change by 2 units), motivation confounds both treatment and outcome, and a random instrument shifts treatment.

```python
import numpy as np
import pandas as pd
from linearmodels.iv import IV2SLS

rng = np.random.default_rng(20260528)
N = 5_000
beta1_true = -2.0

# Unobserved confounder: financial motivation (lowers balance change, raises take-up)
motivation = rng.normal(0.0, 1.0, size=N)

# Instrument: random mailer (a coin flip -> independent of motivation, satisfies exclusion by design)
Z = rng.integers(0, 2, size=N).astype(float)

# Treatment: driven by the mailer (relevance) AND by motivation (the endogeneity)
#   compliers are those the mailer pushes over the enrollment threshold
latent = 0.8 * Z + 1.0 * motivation + rng.normal(0.0, 1.0, size=N)
D = (latent > 0.7).astype(float)

# Outcome: true causal effect of D is beta1_true; motivation also lowers the balance change
eps = rng.normal(0.0, 1.0, size=N)
Y = 1.0 + beta1_true * D - 1.5 * motivation + eps   # motivation in the error => endogeneity

df = pd.DataFrame({"Y": Y, "D": D, "Z": Z, "const": 1.0})

# --- Naive OLS: biased, because motivation is in the error and correlates with D ---
# With no endogenous regressors, IV2SLS just runs OLS of Y on [const, D].
ols = IV2SLS(df["Y"], df[["const", "D"]], None, None).fit()
print("OLS  beta_hat:", round(ols.params["D"], 3))

# --- 2SLS: instrument the endogenous D with Z. linearmodels gives correct standard errors. ---
# IV2SLS(dependent, exog=[const + any controls], endog=[D], instruments=[Z])
iv = IV2SLS(df["Y"], df[["const"]], df[["D"]], df[["Z"]]).fit(cov_type="robust")
print("2SLS beta_hat:", round(iv.params["D"], 3))

# --- First-stage strength: the built-in diagnostics report the partial F on the instrument ---
print("First-stage diagnostics:\n", iv.first_stage.diagnostics[["f.stat", "f.pval"]])
```

Running it prints an OLS coefficient biased relative to the truth (motivation makes treated people look better than the course alone explains), a 2SLS coefficient close to the true $-2$, and a first-stage diagnostics table reporting the partial F on the instrument — comfortably above $10$ here because we built a strong first stage (`0.8 * Z`). The `iv.first_stage` accessor in `linearmodels` gives you the first-stage regression, its F-statistic, and the robust effective-F machinery in one place; nb3.4 walks through reading every cell of that table.

Two things to notice in the output. First, OLS and 2SLS disagree, and the gap is the endogeneity bias made visible — the entire reason for the exercise. Second, if you go back and shrink the first stage (change `0.8 * Z` to `0.05 * Z`) and re-run, you will watch 2SLS slide *back toward the biased OLS number* and its standard error explode — the weak-instrument pathology of §8, which you will reproduce in full and learn to inoculate against in Chapter 3.5.

---

## What to carry forward

Four things from this chapter will do real work for the rest of the camp.

First, **the escape from CIA**. When an unobserved confounder makes the treatment endogenous — when CIA fails and matching/balancing cannot help because the confounder is unmeasured — an instrument lets you identify a causal effect anyway, by importing exogenous variation from outside the system. IV is the design-based answer to the bottom rows of Chapter 2.5's bias–consistency ledger: unobserved confounding, simultaneity, and measurement error all yield to a valid instrument.

Second, **the two conditions and their asymmetry**. Relevance ($\operatorname{Cov}(Z,D)\neq 0$) is testable — check and report the first stage. Exclusion (no path $Z\to Y$ except through $D$, and $Z$ unrelated to the confounder) is *un*testable and must be argued from institutions and logic. Random assignment of the instrument, as in Maya's mailer, buys you the hardest half of exclusion for free; the direct-path half you must still defend in prose. Every IV result you read should be interrogated on both fronts, separately.

Third, **LATE, not ATE**. IV identifies the effect for *compliers* — the units the instrument actually moved — not for always-takers, never-takers, or the population at large. Under monotonicity (no defiers), the Imbens–Angrist theorem makes this exact. When you read or write an IV result, the question is not only "is the instrument valid?" but "who are the compliers, and is their effect the one I care about?" The same treatment with two different instruments can give two different, both-correct LATEs.

Fourth, **strength is everything**. A weak first stage drags 2SLS back toward the OLS bias you were fleeing, inflates and corrupts your standard errors, and amplifies any small exclusion violation. Report the first-stage F; clear Stock–Yogo's bar (the origin of "$F>10$") but do not trust it blindly — it assumes classical errors and bounds bias, not inference. With the heteroskedastic, clustered errors real finance data have, report the **Olea–Pflueger effective F** instead. We have set up the weak-IV problem here; Chapter 3.5 reproduces the full pathology and arms you with Anderson–Rubin inference that stays valid even when the instrument is weak.

---

## Your Turn

Open **nb3.4 — "2SLS with `linearmodels`; first-stage F."** You will (1) reproduce Maya's mailer experiment as a Wald estimator by hand from a 2×2 means table and confirm it equals the just-identified 2SLS coefficient; (2) scale up to a continuous-treatment, multiple-control 2SLS run on a simulated debt panel, verifying that 2SLS recovers the true $\beta_1$ while OLS does not, and that running the two stages by hand reproduces the *point* estimate but the *wrong* standard error; (3) read the full first-stage diagnostics — the partial F and the Olea–Pflueger effective F — and then deliberately weaken the instrument and watch 2SLS slide back toward OLS while the effective F drops below its critical value, previewing Chapter 3.5's pathology.

Before you start, make sure you can answer these:

1. **Relevance vs. exclusion.** Maya proposes using *distance from the household to the nearest class location* as an instrument for course completion, instead of the random mailer. (a) State the relevance condition for this instrument and how you would test it. (b) State the exclusion restriction in words, and give one concrete reason distance might violate it (hint: think about what else neighborhood location correlates with). (c) Which of the two conditions can the data confirm, and which can it never confirm?

2. **The Wald ratio and LATE.** In a mailer experiment, $40\%$ of mailed households and $25\%$ of unmailed households completed the course; mean balance change was $-\$80$ for mailed and $-\$20$ for unmailed. (a) Compute the first stage, the reduced form, and the Wald estimate. (b) What share of the population are compliers? (c) Whose treatment effect is your Wald estimate — name the type — and name two groups whose effect it does *not* capture and why the instrument is blind to them.

3. **Weak instruments.** A classmate reports a 2SLS estimate with a first-stage F of $3.2$, computed with classical (non-robust) standard errors, and a tight 95% confidence interval that excludes zero. (a) Why is the tight confidence interval *not* reassuring here? (b) In which direction is the 2SLS point estimate likely biased, and toward what? (c) Their data are clustered by ZIP code. Which statistic should they report instead of the classical first-stage F, and who derived it?
