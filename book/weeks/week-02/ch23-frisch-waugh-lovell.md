# Ch 2.3 — The Frisch–Waugh–Lovell Theorem

Every time you read a multiple regression in a finance paper, you read it the same way. The coefficient on R&D spending is reported "controlling for firm size." The coefficient on a treatment dummy is reported "controlling for industry and year." The word *controlling* does so much work that it has almost stopped meaning anything — it sounds like a magic spray that removes contamination. This chapter is about what that word *actually* does, mechanically, to the arithmetic. And the answer is precise and a little surprising: controlling for the other variables means **subtracting them out of everything first**, and then running a plain simple regression on what is left over.

That statement is the Frisch–Waugh–Lovell theorem (everyone calls it **FWL**). It is the single most useful interpretive fact in this whole book. It tells you exactly what a multiple-regression coefficient *is*: not a coefficient in some irreducible $K$-dimensional object, but a humble two-variable slope — once both variables have been cleaned of the other regressors. Once you have FWL in your hands, you can read any control coefficient correctly, you understand what "holding constant" really buys you, and — as a bonus that pays off all of Weeks 3 and 4 — you understand why subtracting group means is the same thing as throwing in a dummy for every group. That last equivalence *is* fixed effects, sneaking up on you a month early.

We built the machinery for the proof in Ch 2.1. There we wrote OLS in matrix form, $\mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\varepsilon}$ with $\hat{\boldsymbol{\beta}} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$, and we met two matrices that do all the geometric work: the **hat matrix** $\mathbf{H} = \mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'$, which projects any vector onto the column space of $\mathbf{X}$ (it turns $\mathbf{y}$ into the fitted values $\hat{\mathbf{y}} = \mathbf{H}\mathbf{y}$), and the **residual-maker matrix** $\mathbf{M} = \mathbf{I} - \mathbf{H}$, which sweeps out everything explainable by $\mathbf{X}$ and leaves the residuals, $\hat{\boldsymbol{\varepsilon}} = \mathbf{M}\mathbf{y}$. We will use $\mathbf{M}$ as a finished tool. If you need to refresh why $\mathbf{M}$ is symmetric ($\mathbf{M}' = \mathbf{M}$) and idempotent ($\mathbf{M}\mathbf{M} = \mathbf{M}$), and why $\mathbf{M}\mathbf{X} = \mathbf{0}$, flip back to Ch 2.1 §4 — those three facts are the entire engine of this chapter's proof.

---

## 1. The result in one plain sentence

> **FWL, stated plainly.** A coefficient in a multiple regression is exactly the slope you would get from a *simple* regression — of the outcome, after removing the other regressors from it, on the key regressor, after removing the other regressors from *it* too.

"Removing the other regressors" means: regress the thing on those other regressors and keep the residual. The residual is the part that the other regressors *cannot* explain — the part that is left over, orthogonal to them. FWL says a multiple-regression coefficient lives entirely in the leftover parts. The bulk of the regressors are not in the room when the key slope is decided; they have already done their job by being subtracted out.

That is the whole idea. The rest of the chapter earns it — first with a number, then with the algebra, then with the two payoffs (reading controls, and the within-transformation preview of fixed effects).

Why should you believe a multivariate problem can collapse to a bivariate one? Here is the intuition before any algebra. A multiple regression is doing two jobs at once for each regressor: it is using $x$ to explain $y$, *and* it is making sure $x$ does not get credit for anything the other regressors could have explained. Those two jobs interfere — that is precisely why the coefficient on $x$ in a multiple regression is generally not the same as the simple-regression slope of $y$ on $x$. The genius of partialling-out is to *separate* the two jobs. First, settle the bookkeeping: figure out how much of $x$ the other regressors can account for, and set it aside (that is $\hat{x}$); keep only the part they cannot, $\tilde{x}$. Do the same to $y$. Now the bookkeeping is done — the other regressors have been paid in full — and what remains is a clean, uncontaminated question: of the variation in $y$ that the controls did not claim, how much lines up with the variation in $x$ that the controls did not claim? No interference is left, because everything the controls could touch has already been removed. So a simple slope of the leftovers answers the partial question exactly. The word **partialling-out** names this maneuver: you partial the other regressors out of both variables, then regress.

---

## 2. Reveal the trick: Leah's R&D and patents

Leah studies innovation. She has firm-level data and a hunch she has heard stated a hundred ways: firms that spend more on research and development produce more patents. But she also knows the obvious objection — *big firms do everything more*. Big firms spend more on R&D and they file more patents, simply because they are big. So a raw correlation between R&D and patents might be measuring nothing but size. The honest question is the **partial** one: does R&D predict patents *after netting out firm size*?

The textbook move is a multiple regression. Let $y_i$ be patents (per year), $x_i$ be R&D spending (in \$millions), and $z_i$ be firm size (log assets, say). Leah runs

$$
y_i = \beta_0 + \beta_1 x_i + \beta_2 z_i + \varepsilon_i,
$$

and reports $\hat{\beta}_1$ as "the effect of R&D, controlling for size." FWL claims she can get *exactly the same number* $\hat{\beta}_1$ a completely different way — without ever running the three-variable regression. Let us watch it happen on a tiny dataset of six firms, small enough to do by hand.

| firm $i$ | patents $y_i$ | R&D $x_i$ | size $z_i$ |
|---|---|---|---|
| 1 | 10 | 2 | 1 |
| 2 | 14 | 3 | 2 |
| 3 | 22 | 5 | 3 |
| 4 | 24 | 4 | 4 |
| 5 | 33 | 7 | 5 |
| 6 | 39 | 8 | 6 |

Notice that R&D and size are positively related across these firms (bigger firms tend to spend more on R&D), which is exactly the entanglement Leah worries about. Here are the means we will need:

$$
\bar{y} = 23.667,\qquad \bar{x} = 4.833,\qquad \bar{z} = 3.5.
$$

### Step 0: the answer we are trying to match

First, so we have a target, the full multiple regression of $y$ on $x$ and $z$ (with intercept) gives

$$
\hat{\beta}_1 = 1.838,\qquad \hat{\beta}_2 = 3.676,\qquad \hat{\beta}_0 = 1.919.
$$

(You will reproduce these in nb2.3; for now take them as the destination.) Keep $\hat{\beta}_1 = 1.838$ in mind. FWL says we can hit it with two simple regressions and no matrix inversion bigger than a scalar.

### Step 1: residualize the key regressor $x$ against everything else

"Everything else" here is firm size $z$ plus the intercept. So regress R&D on size:

$$
x_i = a_0 + a_1 z_i + (\text{residual}),\qquad \tilde{x}_i \equiv x_i - \hat{x}_i.
$$

The slope of $x$ on $z$ is $a_1 = \operatorname{Cov}(x,z)/\operatorname{Var}(z)$. Working it out on the six firms, $a_1 = 1.171$ and $a_0 = 0.733$, so the fitted values and residuals $\tilde{x}_i = x_i - (0.733 + 1.171 z_i)$ come out to

| $i$ | $\hat{x}_i$ | $\tilde{x}_i$ |
|---|---|---|
| 1 | 1.905 | $+0.095$ |
| 2 | 3.076 | $-0.076$ |
| 3 | 4.248 | $+0.752$ |
| 4 | 5.419 | $-1.419$ |
| 5 | 6.590 | $+0.410$ |
| 6 | 7.762 | $+0.238$ |

These residuals $\tilde{x}_i$ are **the part of R&D that size cannot explain** — the firm-specific R&D intensity that has nothing to do with mere bigness. They sum to zero (up to rounding), as residuals from a regression with an intercept always must.

### Step 2: residualize the outcome $y$ against everything else

Do the same to patents — regress $y$ on size $z$ (and intercept), keep the residual $\tilde{y}_i = y_i - \hat{y}_i$:

$$
y_i = c_0 + c_1 z_i + (\text{residual}).
$$

Here $c_1 = 5.829$ and $c_0 = 3.267$, giving

| $i$ | $\hat{y}_i$ | $\tilde{y}_i$ |
|---|---|---|
| 1 | 9.095 | $+0.905$ |
| 2 | 14.924 | $-0.924$ |
| 3 | 20.752 | $+1.248$ |
| 4 | 26.581 | $-2.581$ |
| 5 | 32.410 | $+0.590$ |
| 6 | 38.238 | $+0.762$ |

The $\tilde{y}_i$ are **the part of patenting that size cannot explain** — patenting beyond what the firm's size alone would predict.

### Step 3: regress leftover on leftover

Now the punchline. Run a *simple* regression of the residualized outcome on the residualized regressor — no intercept needed, since both residual vectors already average to zero:

$$
\tilde{y}_i = \beta_1 \,\tilde{x}_i + (\text{error}).
$$

The slope of a simple no-intercept regression is just $\sum_i \tilde{x}_i \tilde{y}_i \big/ \sum_i \tilde{x}_i^2$. Plugging in the two residual columns:

$$
\hat{\beta}_1 = \frac{\sum_i \tilde{x}_i \tilde{y}_i}{\sum_i \tilde{x}_i^2} = \frac{(0.095)(0.905) + (-0.076)(-0.924) + \cdots + (0.238)(0.762)}{(0.095)^2 + (-0.076)^2 + \cdots + (0.238)^2} = \frac{5.181}{2.819} = 1.838.
$$

There it is: **1.838**, the exact same number as the multiple-regression coefficient from Step 0. We never put $x$ and $z$ in the same regression. We cleaned $z$ out of both $x$ and $y$, then ran a two-variable regression on the cleaned versions, and the slope landed precisely on $\hat{\beta}_1$. That is not a coincidence of these six numbers; it is a theorem, and it is exactly true for every dataset. Let us prove it.

> **One detail worth pausing on.** You must residualize *both* $y$ and $x$ against $z$. A common mistake is to clean $z$ out of $x$ only, then regress the *raw* $y$ on $\tilde{x}$. As it happens, that also gives the right slope here — because $\tilde{x}$ is orthogonal to $z$, the part of $y$ that $z$ explains is orthogonal to $\tilde{x}$ and contributes nothing to the slope. So you can get away with residualizing only the regressor *for the point estimate*. But you must residualize both to get the right *residuals*, the right standard error, and the right $R^2$ from the short regression. The clean, symmetric statement — clean both sides — is the one to memorize, and the one the proof below delivers.

---

## 3. The formal statement and a clean proof

Now we say it in matrix language, the way you will see it in a real econometrics text, and prove it with the residual-maker matrix from Ch 2.1.

**Setup.** Partition the regressor matrix into two blocks of columns:

$$
\mathbf{y} = \mathbf{X}_1\boldsymbol{\beta}_1 + \mathbf{X}_2\boldsymbol{\beta}_2 + \boldsymbol{\varepsilon}.
$$

Here $\mathbf{X}_1$ is the block of regressors you care about (in Leah's case, the single column of R&D values $x$), with coefficient vector $\boldsymbol{\beta}_1$, and $\mathbf{X}_2$ is the block of everything else you are controlling for — the intercept, firm size, industry dummies, whatever (in Leah's case, the intercept column and the size column $z$), with coefficient $\boldsymbol{\beta}_2$. The full OLS fit produces $\hat{\boldsymbol{\beta}}_1$ and $\hat{\boldsymbol{\beta}}_2$ jointly.

**The residual-maker for $\mathbf{X}_2$.** Define the matrix that sweeps out everything in the column space of $\mathbf{X}_2$:

$$
\mathbf{M}_2 = \mathbf{I} - \mathbf{X}_2(\mathbf{X}_2'\mathbf{X}_2)^{-1}\mathbf{X}_2'.
$$

This is exactly the residual maker from Ch 2.1, just built from the $\mathbf{X}_2$ block instead of the full $\mathbf{X}$. Multiplying any vector by $\mathbf{M}_2$ returns the residual from regressing that vector on $\mathbf{X}_2$. So define the **residualized** quantities

$$
\tilde{\mathbf{y}} = \mathbf{M}_2\,\mathbf{y}, \qquad \tilde{\mathbf{X}}_1 = \mathbf{M}_2\,\mathbf{X}_1.
$$

These are precisely Leah's $\tilde{y}$ and $\tilde{x}$ columns from §2 — $y$ and $x$ with size (and the intercept) netted out.

> **Frisch–Waugh–Lovell.** The OLS coefficient $\hat{\boldsymbol{\beta}}_1$ from the full regression of $\mathbf{y}$ on $[\mathbf{X}_1,\ \mathbf{X}_2]$ is identical to the OLS coefficient from the simple regression of $\tilde{\mathbf{y}}$ on $\tilde{\mathbf{X}}_1$:
> $$\hat{\boldsymbol{\beta}}_1 = (\tilde{\mathbf{X}}_1'\tilde{\mathbf{X}}_1)^{-1}\tilde{\mathbf{X}}_1'\tilde{\mathbf{y}}.$$
> Moreover, the residuals from that short regression equal the residuals from the full regression.

**Proof.** Recall the three properties of any residual maker $\mathbf{M}_2$, established in Ch 2.1: it is **symmetric** ($\mathbf{M}_2' = \mathbf{M}_2$), **idempotent** ($\mathbf{M}_2\mathbf{M}_2 = \mathbf{M}_2$ — sweeping out $\mathbf{X}_2$ twice does nothing more than sweeping it once), and it **annihilates** its own block ($\mathbf{M}_2\mathbf{X}_2 = \mathbf{0}$ — there is no residual left when you regress $\mathbf{X}_2$ on itself). Those three facts are all we need.

Start from the full normal equations. The fitted model is $\mathbf{y} = \mathbf{X}_1\hat{\boldsymbol{\beta}}_1 + \mathbf{X}_2\hat{\boldsymbol{\beta}}_2 + \hat{\boldsymbol{\varepsilon}}$, where the OLS residual $\hat{\boldsymbol{\varepsilon}}$ is orthogonal to *every* regressor, hence to both blocks: $\mathbf{X}_1'\hat{\boldsymbol{\varepsilon}} = \mathbf{0}$ and $\mathbf{X}_2'\hat{\boldsymbol{\varepsilon}} = \mathbf{0}$.

Now hit the whole equation on the left with $\mathbf{M}_2$:

$$
\mathbf{M}_2\mathbf{y} = \mathbf{M}_2\mathbf{X}_1\hat{\boldsymbol{\beta}}_1 + \mathbf{M}_2\mathbf{X}_2\hat{\boldsymbol{\beta}}_2 + \mathbf{M}_2\hat{\boldsymbol{\varepsilon}}.
$$

Take the three terms on the right one at a time. The middle term dies: $\mathbf{M}_2\mathbf{X}_2 = \mathbf{0}$, so $\mathbf{M}_2\mathbf{X}_2\hat{\boldsymbol{\beta}}_2 = \mathbf{0}$. That is the heart of the trick — sweeping out $\mathbf{X}_2$ erases the entire $\hat{\boldsymbol{\beta}}_2$ contribution, controls and all. The last term is unchanged: $\hat{\boldsymbol{\varepsilon}}$ is already orthogonal to $\mathbf{X}_2$, so it survives untouched, $\mathbf{M}_2\hat{\boldsymbol{\varepsilon}} = \hat{\boldsymbol{\varepsilon}}$. (Concretely, $\mathbf{M}_2\hat{\boldsymbol{\varepsilon}} = \hat{\boldsymbol{\varepsilon}} - \mathbf{X}_2(\mathbf{X}_2'\mathbf{X}_2)^{-1}\mathbf{X}_2'\hat{\boldsymbol{\varepsilon}}$, and the second piece vanishes because $\mathbf{X}_2'\hat{\boldsymbol{\varepsilon}} = \mathbf{0}$.) What remains is

$$
\tilde{\mathbf{y}} = \tilde{\mathbf{X}}_1\hat{\boldsymbol{\beta}}_1 + \hat{\boldsymbol{\varepsilon}},
$$

using $\tilde{\mathbf{y}} = \mathbf{M}_2\mathbf{y}$ and $\tilde{\mathbf{X}}_1 = \mathbf{M}_2\mathbf{X}_1$. This already says something beautiful: the *same* $\hat{\boldsymbol{\beta}}_1$ and the *same* residual $\hat{\boldsymbol{\varepsilon}}$ from the full regression also describe the residualized outcome as a linear function of the residualized regressor.

To pin $\hat{\boldsymbol{\beta}}_1$ down as an OLS slope, left-multiply by $\tilde{\mathbf{X}}_1'$:

$$
\tilde{\mathbf{X}}_1'\tilde{\mathbf{y}} = \tilde{\mathbf{X}}_1'\tilde{\mathbf{X}}_1\,\hat{\boldsymbol{\beta}}_1 + \tilde{\mathbf{X}}_1'\hat{\boldsymbol{\varepsilon}}.
$$

The cross term $\tilde{\mathbf{X}}_1'\hat{\boldsymbol{\varepsilon}}$ is zero. Why? $\tilde{\mathbf{X}}_1' = (\mathbf{M}_2\mathbf{X}_1)' = \mathbf{X}_1'\mathbf{M}_2$ (symmetry), so $\tilde{\mathbf{X}}_1'\hat{\boldsymbol{\varepsilon}} = \mathbf{X}_1'\mathbf{M}_2\hat{\boldsymbol{\varepsilon}} = \mathbf{X}_1'\hat{\boldsymbol{\varepsilon}} = \mathbf{0}$, where we used $\mathbf{M}_2\hat{\boldsymbol{\varepsilon}} = \hat{\boldsymbol{\varepsilon}}$ again and then the full-model orthogonality $\mathbf{X}_1'\hat{\boldsymbol{\varepsilon}} = \mathbf{0}$. So the cross term drops, leaving the normal equation of a simple regression:

$$
\tilde{\mathbf{X}}_1'\tilde{\mathbf{X}}_1\,\hat{\boldsymbol{\beta}}_1 = \tilde{\mathbf{X}}_1'\tilde{\mathbf{y}} \quad\Longrightarrow\quad \hat{\boldsymbol{\beta}}_1 = (\tilde{\mathbf{X}}_1'\tilde{\mathbf{X}}_1)^{-1}\tilde{\mathbf{X}}_1'\tilde{\mathbf{y}}. \qquad\blacksquare
$$

There is one cosmetic simplification worth noting. Because $\mathbf{M}_2$ is symmetric and idempotent, $\tilde{\mathbf{X}}_1'\tilde{\mathbf{X}}_1 = \mathbf{X}_1'\mathbf{M}_2'\mathbf{M}_2\mathbf{X}_1 = \mathbf{X}_1'\mathbf{M}_2\mathbf{X}_1 = \mathbf{X}_1'\tilde{\mathbf{X}}_1$, and likewise $\tilde{\mathbf{X}}_1'\tilde{\mathbf{y}} = \mathbf{X}_1'\mathbf{M}_2\mathbf{y} = \mathbf{X}_1'\tilde{\mathbf{y}}$. So you only strictly need to residualize *one* side to recover the point estimate — exactly the observation flagged in the box at the end of §2. The symmetric "residualize both" version is the safe default because it also delivers the correct short-regression residuals, which you need for everything downstream.

The proof used nothing but the three properties of $\mathbf{M}_2$ and the orthogonality of the full-model residual. That is the payoff of having built $\mathbf{M}$ carefully in Ch 2.1: a result that looks like deep magic falls out in four lines.

### The geometry, in one picture

If the algebra felt like symbol-pushing, here is the picture underneath it, using the projection geometry from Ch 2.1. Think of every variable as a vector in $\mathbb{R}^N$ — one coordinate per firm. The outcome $\mathbf{y}$ is a point in that space; the regressors span a subspace; OLS drops a perpendicular from $\mathbf{y}$ onto that subspace and calls the foot of the perpendicular $\hat{\mathbf{y}}$.

Now picture the controls $\mathbf{X}_2$ as carving out their own little subspace — a plane, say, if $\mathbf{X}_2$ is the intercept and size. The residual maker $\mathbf{M}_2$ is the operation "project everything onto the directions *perpendicular* to that plane." So $\tilde{\mathbf{X}}_1 = \mathbf{M}_2\mathbf{X}_1$ is the shadow of your regressor cast onto the perpendicular space, and $\tilde{\mathbf{y}} = \mathbf{M}_2\mathbf{y}$ is the shadow of the outcome. FWL says: to find how much $\mathbf{y}$ leans in the $\mathbf{X}_1$ direction *after accounting for the plane*, you should project both vectors off the plane first and then measure how the shadows line up. The controls are not deleted; they define the plane you are standing perpendicular to. Every multiple-regression coefficient is, geometrically, a simple slope measured in the subspace orthogonal to the controls. That single sentence is worth more than the four lines of matrix algebra — it is the mental model to keep.

---

## 4. Controls as residualization: what "holding constant" really means

This is the conceptual heart of the whole chapter, and it is worth slowing down for, because it changes how you read every empirical table for the rest of your life.

When a paper says "$\hat{\beta}_1 = 1.838$, controlling for firm size," beginners picture something physical: hold size fixed at some value, wiggle R&D, watch patents respond. That picture is fine intuition but it is *not* what the regression did. The regression has no way to hold size fixed; the firms in the data are whatever sizes they are. What it actually did, FWL tells us exactly, is **remove the linear influence of size from both R&D and patents, and then look at how the leftovers move together.**

So "controlling for $z$" is not a filter and not an experiment. It is a *subtraction*. The coefficient $\hat{\beta}_1$ answers the question: among firms that have *more R&D than their size would predict*, do we also see *more patents than their size would predict*? It is a statement entirely about the residual variation — the wobble in R&D and patents that size leaves unexplained. The slope is built only from the parts of the variables that size cannot account for.

This reframing immediately settles several things that otherwise feel mysterious:

**Why adding an irrelevant control barely moves a coefficient, and a relevant one moves it a lot.** If a control $z$ is unrelated to your regressor $x$, then residualizing $x$ on $z$ changes $x$ hardly at all ($\tilde{x} \approx x$), so $\hat{\beta}_1$ barely budges. But if $z$ is strongly related to $x$ — as size is to R&D — residualizing strips out a big chunk of $x$, and the coefficient can change a lot. FWL makes this mechanical, not mystical: the control only matters to the extent that it overlaps with the regressor you care about.

**Why a control with almost no independent variation is dangerous.** Suppose two controls in $\mathbf{X}_2$ together can predict $x$ almost perfectly. Then $\tilde{x} = \mathbf{M}_2 x$ is nearly the zero vector — there is almost no leftover R&D variation once the controls have had their say. The denominator $\tilde{\mathbf{X}}_1'\tilde{\mathbf{X}}_1$ is then tiny, and a tiny denominator makes the slope wildly sensitive to noise. This is **multicollinearity**, and FWL shows you precisely where it bites: it is the case where you have residualized away nearly all of your own regressor. There is simply not much "own variation" left for $x$ to use to explain $y$. You will see the inflated standard error this produces when we do variances in Ch 2.4; FWL tells you *why* it happens.

**What omitting a control does.** If Leah had run the *short* regression — patents on R&D alone, leaving size out — she would have gotten a different (larger) slope, because the raw R&D variable still carries the size signal inside it. On her six firms the short slope is about $4.65$, more than double the $1.838$ she gets once size is partialled out. The reason is exactly the FWL picture run in reverse: in the short regression nothing is residualized, so $x$ enters with the size-driven part of its variation intact, and patents respond to *both* the genuine R&D effect and the size effect that travels with R&D. The gap, $4.65 - 1.838$, is the bias from omitting size; FWL is the clean lens for seeing it, because it shows that controlling means subtracting size out, and *not* controlling means leaving it in. Ch 2.5 will turn this gap into the **omitted-variable-bias formula** — bias equals the coefficient of the omitted variable times the slope of the omitted variable on the included one — and you will recognize both pieces as residualization quantities. For now, hold the picture: leaving out a control means *failing to residualize*, so the leftover variation still has the control's fingerprints on it, and the coefficient absorbs whatever the omitted variable would have explained.

A subtler point hides here, and it is the one professional readers train themselves to ask. "Holding size constant" only cleans out the part of the relationship that runs *through size as we measured it* — log assets. It does nothing about variables we never put in $\mathbf{X}_2$ at all. If older firms both patent more and spend more on R&D for reasons unrelated to size, then firm age is still sitting inside $\tilde{x}$ and $\tilde{y}$, uncontrolled, and Leah's $1.838$ is "controlling for size" but not for age. FWL is brutally honest about this: it tells you the coefficient is a clean simple slope in the space orthogonal to *exactly the columns you included* — no more. The theorem cannot residualize out something that is not in the regression. That is why CONVENTIONS §4 insists you name the controls and the identifying assumption: the list of what you residualized *is* the boundary of what "holding constant" covers, and everything outside that list is a potential threat you have not addressed.

The discipline this enforces is the one in CONVENTIONS §4: when you report a coefficient, you must be able to name what was residualized out — the controls and fixed effects — because that list *defines* what the coefficient means. "Controlling for size" is not a disclaimer you tack on; it is a description of the exact subtraction that produced the number.

---

## 5. Demeaning is the within transformation — a preview of fixed effects

Here is the most consequential special case of FWL, and the bridge to the next two weeks of the camp.

Take the simplest possible control: a single intercept. The $\mathbf{X}_2$ block is just a column of ones, $\boldsymbol{\iota} = (1,1,\dots,1)'$. What does residualizing on a column of ones do? Regressing any variable on a constant gives the mean as the fitted value, so the residual maker $\mathbf{M}_2 = \mathbf{I} - \boldsymbol{\iota}(\boldsymbol{\iota}'\boldsymbol{\iota})^{-1}\boldsymbol{\iota}'$ simply **subtracts the overall mean**:

$$
(\mathbf{M}_2\mathbf{y})_i = y_i - \bar{y}.
$$

So FWL contains, as its tiniest case, a fact you already half-knew: a slope in a regression *with an intercept* equals the slope from a regression on the **demeaned** variables. The intercept is a "control," and controlling for it means centering everything. That is why in §2 the residual columns averaged to zero and we could drop the intercept in Step 3.

Now make the control richer. Instead of one overall mean, suppose your data come in **groups** — firms grouped by industry, students grouped by school, observations grouped by year — and you control for a full set of **group dummy variables**, one indicator column per group (dropping one to avoid perfect collinearity with the intercept, or dropping the intercept). What does residualizing on the group dummies do?

Regressing any variable on a complete set of group dummies fits, for each observation, *its own group's mean*. So the residual maker subtracts the **group-specific mean**:

$$
(\mathbf{M}_2\mathbf{y})_i = y_i - \bar{y}_{g(i)},
$$

where $g(i)$ is the group that observation $i$ belongs to and $\bar{y}_{g(i)}$ is the mean of $y$ within that group. This operation — subtracting each group's own mean from each observation — is called the **within transformation** (because it keeps only the variation *within* each group and discards all variation *between* groups).

Putting FWL together with this fact gives a clean and important equivalence:

> **Dummies ⇔ demeaning.** Running a regression of $y$ on $x$ *plus a full set of group dummies* produces exactly the same slope on $x$ as running a regression of the **within-group-demeaned** $y$ on the **within-group-demeaned** $x$.

You can get the coefficient either way and the number is identical — FWL guarantees it, because the dummies *are* the $\mathbf{X}_2$ block and demeaning *is* multiplication by their residual maker. Leah could control for industry by literally adding a hundred industry dummy columns, or by subtracting each industry's mean R&D and mean patents and running a tiny two-variable regression on what is left. Same slope.

Let us watch it on Leah's six firms one more time, now grouped by industry: firms 1–3 are "biotech," firms 4–6 are "hardware." The within transformation says: from each firm, subtract *its own industry's* mean of each variable. The biotech mean R&D is $(2+3+5)/3 = 3.333$ and the hardware mean is $(4+7+8)/3 = 6.333$; the biotech mean patents is $(10+14+22)/3 = 15.333$ and the hardware mean is $(24+33+39)/3 = 32.0$. Subtracting gives the demeaned columns:

| $i$ | industry | $\ddot{x}_i = x_i - \bar{x}_{g}$ | $\ddot{y}_i = y_i - \bar{y}_{g}$ |
|---|---|---|---|
| 1 | biotech | $-1.333$ | $-5.333$ |
| 2 | biotech | $-0.333$ | $-1.333$ |
| 3 | biotech | $+1.667$ | $+6.667$ |
| 4 | hardware | $-2.333$ | $-8.000$ |
| 5 | hardware | $+0.667$ | $+1.000$ |
| 6 | hardware | $+1.667$ | $+7.000$ |

A no-intercept simple regression of $\ddot{y}$ on $\ddot{x}$ gives $\sum \ddot{x}\ddot{y} / \sum \ddot{x}^2 = 49.67 / 13.33 = 3.725$. And if instead you regress $y$ on R&D *plus a biotech/hardware dummy*, the R&D coefficient comes out to exactly $3.725$ as well. The two-line demeaning and the dummy regression agree to the last digit — that is FWL, with the industry dummies playing the role of $\mathbf{X}_2$. Notice the slope differs from §2's $1.838$: controlling for *industry* asks a different question than controlling for *size*, and FWL makes the difference visible as a different residualization.

This is not a side curiosity. It is the entire idea of **fixed effects**, which run Weeks 3 and 4. A panel of firms observed over many years has a natural grouping — by firm. Controlling for a firm dummy for every firm absorbs everything about a firm that does not change over time: its industry, its founding culture, its headquarters state, its baseline managerial quality. The within transformation subtracts each firm's own time-average from each of its observations, leaving only how the firm deviates from *itself* over time. FWL is the reason the "subtract the firm mean" estimator and the "throw in a firm dummy for every firm" estimator give the identical slope — and it is the reason you do not have to actually build and invert a matrix with thousands of dummy columns. You demean instead, which is cheap. When we write $y_{it} = \alpha_i + \beta x_{it} + \varepsilon_{it}$ in Week 3 and estimate $\beta$ by within-demeaning, you should hear FWL humming underneath. We are getting that machinery for free, four weeks early, just by reading the intercept case of this theorem and then turning the dial up from one mean to many group means.

---

## 6. Why FWL also matters for fast computation

FWL is mostly an *interpretive* theorem, but it has a practical computational edge that real software leans on hard.

The first edge is the one we just used: instead of inverting a giant $(\mathbf{X}'\mathbf{X})$ that includes thousands of dummy columns, you can **partial out** the dummies by demeaning — an operation that costs almost nothing, just subtracting group means — and then solve a small regression on the residualized variables. This is exactly how modern fixed-effects packages such as `pyfixest` and the algorithm behind them work: they never form the dummy matrix at all. For two-way or higher fixed effects (firm *and* year, say), they iterate the demeaning step until it converges (the method of alternating projections — repeatedly applying residual makers $\mathbf{M}_2$), which is the multi-group generalization of the single $\mathbf{M}_2$ in our proof. Decades of "absorbing" fixed effects rest on FWL.

To feel the size of this saving, imagine a panel with 5,000 firms and 20 years. Controlling for a firm dummy and a year dummy the brute-force way means a design matrix with over 5,000 columns, and inverting $\mathbf{X}'\mathbf{X}$ — a 5,000-plus square matrix — for a single regression. That is enormous and numerically delicate. FWL says you never have to: subtract each firm's mean and each year's mean (iterating until both are swept out, since the two demeanings interfere), then run a regression on a handful of real variables. The cost drops from "invert a huge matrix" to "compute some group averages," which is linear in the data. This is not a minor optimization; it is the difference between a regression that runs in milliseconds and one that does not run at all. Every "high-dimensional fixed effects" result you will read in modern empirical finance — papers with firm × year, or manager × firm, or borrower × lender effects — exists because FWL lets the dummies be absorbed instead of inverted.

The second edge shows up whenever you want one coefficient but have many controls: you can residualize once and reuse the cleaned variables. And the third, quieter edge is diagnostic — because FWL collapses any multivariate coefficient down to a *bivariate* slope of $\tilde{y}$ on $\tilde{x}$, you can **plot** it. The scatter of $\tilde{y}$ against $\tilde{x}$, with the FWL slope drawn through it, is the honest two-dimensional picture of a coefficient that otherwise lives in $K$ dimensions. That plot — called a **partial-regression** or **added-variable plot** — is the single best way to *see* whether a control coefficient is driven by the bulk of the data or by one or two influential firms hiding in a high-dimensional regression. It is exactly what nb2.3 builds.

---

## 7. When the trick needs care

FWL is an algebraic identity, so unlike the modeling assumptions of Ch 2.2 (Gauss–Markov) it does not "fail" in the sense of becoming false — it is exactly true whenever the OLS estimator exists. But there are two places where naïve use of it bites.

**The $\mathbf{X}_2$ block must not perfectly explain $\mathbf{X}_1$.** If the controls can reproduce your regressor exactly, then $\tilde{\mathbf{X}}_1 = \mathbf{M}_2\mathbf{X}_1 = \mathbf{0}$, the denominator $\tilde{\mathbf{X}}_1'\tilde{\mathbf{X}}_1$ is singular, and there is no slope to compute. This is just perfect collinearity wearing FWL clothes: there is no leftover variation in your regressor to use. (A classic trap: controlling for a full set of group dummies *and* a variable that is constant within each group — the dummies already absorb it, leaving nothing.)

**Degrees of freedom must be counted on the long regression, not the short one.** The two-variable FWL regression in Step 3 *looks* like it used only one or two parameters, so a software routine that does not know better will report a standard error using $N - 1$ or $N - 2$ degrees of freedom. But the residualizing step silently spent the degrees of freedom in $\mathbf{X}_2$. The correct denominator is $N - K$, counting *all* the regressors including the partialled-out ones. The point estimate is identical either way; only the standard error needs this correction. When you build the partial-regression plot in nb2.3, the slope is honest, but trust the full regression's standard error, computed the way Ch 2.4 will spell out — not the one the short regression naively prints. This is a real bug that people ship: residualize, run a small regression, and quote its too-small standard error, overstating precision. The good fixed-effects packages handle the degrees-of-freedom accounting for you; if you roll your own partialling-out, you must do it by hand.

**Do not residualize the key regressor against a version of itself.** A surprisingly common slip is to include in $\mathbf{X}_2$ a variable that is a transformation of $\mathbf{X}_1$ — for instance, partialling out "log R&D" while studying "R&D." Then $\mathbf{M}_2$ removes most of the signal you care about, and the leftover $\tilde{\mathbf{X}}_1$ is mostly noise; the coefficient on it is no longer answering the question you posed. FWL will faithfully compute *a* slope, but it will be the slope of the wrong question. The fix is conceptual, not numerical: keep $\mathbf{X}_2$ to genuine *controls* — things you want to hold constant — and keep your regressor of interest out of it.

A word on the name, since you will meet it constantly. Ragnar Frisch and Frederick Waugh proved the demeaning-as-partialling case in 1933, working on detrending economic time series;[^fw1933] Michael Lovell generalized it in 1963, in the context of seasonal adjustment.[^lovell1963] The whole tradition of "absorbing" trends, seasonals, and fixed effects by partialling-out descends from that 1933 paper. When a modern paper writes "we absorb firm and year fixed effects," it is invoking Frisch–Waugh–Lovell, ninety years on.

[^fw1933]: Frisch, R., & Waugh, F. V. (1933). Partial Time Regressions as Compared with Individual Trends. *Econometrica*, 1(4), 387–401.

[^lovell1963]: Lovell, M. C. (1963). Seasonal Adjustment of Economic Time Series and Multiple Regression Analysis. *Journal of the American Statistical Association*, 58(304), 993–1010.

---

## 8. The code

Here is the whole chapter in fifteen lines: build Leah's six firms, run the full multiple regression, then reproduce $\hat{\beta}_1$ by the two-step residualize-and-regress recipe. The two numbers must match to machine precision.

```python
import numpy as np
import statsmodels.api as sm

# Leah's six firms: patents (y), R&D (x), size (z)
y = np.array([10, 14, 22, 24, 33, 39], dtype=float)
x = np.array([ 2,  3,  5,  4,  7,  8], dtype=float)
z = np.array([ 1,  2,  3,  4,  5,  6], dtype=float)

# --- Full multiple regression: y on [const, x, z] ---
X_full = sm.add_constant(np.column_stack([x, z]))
beta_full = sm.OLS(y, X_full).fit().params      # [const, b_x, b_z]
print("multiple-regression coef on x:", round(beta_full[1], 4))

# --- FWL: residualize y and x against [const, z], then regress ---
Z = sm.add_constant(z)                            # the X2 block (intercept + size)
x_tilde = x - sm.OLS(x, Z).fit().fittedvalues     # R&D, size netted out
y_tilde = y - sm.OLS(y, Z).fit().fittedvalues     # patents, size netted out
beta_fwl = (x_tilde @ y_tilde) / (x_tilde @ x_tilde)   # no-intercept simple slope
print("FWL two-step coef on x:      ", round(beta_fwl, 4))

assert np.isclose(beta_full[1], beta_fwl)         # identical, by the theorem
```

Running it prints `1.838` twice and the assertion passes. The multiple-regression coefficient and the residualize-then-regress slope are the same number, exactly as the proof in §3 guarantees — on these six firms and on any dataset you feed it.

---

## What to carry forward

Three things from this chapter will do real work for the rest of the book.

First, the *reading rule*. Whenever you meet a multiple-regression coefficient, translate "controlling for the other variables" into "I residualized those variables out of both the outcome and this regressor, then took a simple slope of the leftovers." That translation tells you what the number means, what it does *not* mean (it only nets out the columns you actually included), and which firms or observations are driving it (the ones with large residualized values). A coefficient is always a two-variable slope in disguise; FWL is the disguise-remover.

Second, the *equivalence* that powers panels: regressing on a full set of group dummies is identical to subtracting group means and regressing on the leftovers. Demeaning is residualizing on dummies. When Week 3 introduces $y_{it} = \alpha_i + \beta x_{it} + \varepsilon_{it}$ and estimates $\beta$ by subtracting each firm's time-average, you will already know why that "within estimator" gives the same $\beta$ as a regression with one dummy per firm — and why it is computationally cheap. The fixed-effects chapters are, in a real sense, FWL applied at scale.

Third, the *threat-naming discipline*. FWL draws a hard line around what a coefficient controls for: exactly the columns in $\mathbf{X}_2$, nothing else. Everything outside that block is still inside your residuals, uncontrolled. That is why every spec in this book must name its controls and its identifying assumption — and it is the on-ramp to Ch 2.5's omitted-variable bias, where the gap between the short and long regressions becomes a formula you can compute.

---

## Your Turn

Open **nb2.3 — "FWL residualization, visualized."** You will reproduce Leah's two-step calculation on the six firms, then scale it up to a real Compustat extract of R&D and patents controlling for firm size *and* industry dummies, and draw the **partial-regression (added-variable) plot**: the scatter of residualized patents against residualized R&D with the FWL slope drawn through it. You will watch a multivariate coefficient become a picture you can point at — and you will see which firms are pulling the slope around.

Before you start, make sure you can answer these:

1. **Does residualizing only one side change the point estimate?** In the code above, replace `y_tilde` with the *raw* `y` and recompute the slope as `(x_tilde @ y) / (x_tilde @ x_tilde)`. Do you get the same `1.838`? Explain, using the symmetry-and-idempotence argument at the end of §3, why cleaning only the regressor still nails the point estimate — and state one quantity (besides the point estimate) that would come out *wrong* if you residualized only one side.

2. **From demeaning to fixed effects.** Suppose Leah's six firms came from two industries — firms 1–3 in "biotech," firms 4–6 in "hardware" — and she controls for industry with a dummy instead of for size. Describe, in words and then as a formula, what the within transformation does to each $y_i$ and $x_i$. Why does this give the same R&D slope as adding an industry dummy column to the regression? Which theorem are you invoking?

3. **Multicollinearity through the FWL lens.** Imagine a second control $w$ that, together with size $z$, can predict R&D $x$ almost perfectly. Using FWL, explain what happens to the residualized regressor $\tilde{x}$ and therefore to the denominator $\tilde{\mathbf{X}}_1'\tilde{\mathbf{X}}_1$. Why does this make the slope estimate fragile, even though FWL itself never "fails"?
