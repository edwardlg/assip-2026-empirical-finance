# Ch 4.5 — Bartik / Shift-Share Designs

Week 3 handed you the instrumental-variables machine and one hard truth: a valid instrument is something you *find*, and finding one is rare. You need a variable $Z$ that shoves the treatment $D$ around, has no other path to the outcome $Y$, and is unrelated to the confounder — and most of the time the world simply does not hand you a clean coin flip the way Maya's nonprofit handed her a randomized mailer. This chapter is about a different way to get an instrument: not by finding one ready-made, but by *building* one out of pieces you already have.

The construction is called a **shift-share instrument**, or a **Bartik instrument** after Timothy Bartik, who put it to work in 1991.[^bartik] It is everywhere in empirical economics and finance — local labor markets, immigration, trade exposure, bank lending, household credit. And for thirty years it had a peculiar status: everyone used it, it clearly *worked* in the sense of producing sensible-looking results, and almost nobody could say cleanly *why* it was a valid instrument. The "why" got sorted out only recently, in two landmark papers that gave two different — and at first glance contradictory — answers. Goldsmith-Pinkham, Sorkin and Swift (2020) said the identification comes from the **shares**.[^gpss] Borusyak, Hull and Jaravel (2022) said it comes from the **shifts**.[^bhj] Both are right; they are two lenses on the same object, and which lens you should look through depends on your data. Learning to hold both in your head at once is exactly the kind of methodological maturity Weeks 3 and 4 have been building toward.

[^bartik]: Bartik, T. J. (1991). *Who Benefits from State and Local Economic Development Policies?* W.E. Upjohn Institute for Employment Research.

[^gpss]: Goldsmith-Pinkham, P., Sorkin, I., & Swift, H. (2020). Bartik Instruments: What, When, Why, and How. *American Economic Review*, 110(8), 2586–2624.

[^bhj]: Borusyak, K., Hull, P., & Jaravel, X. (2022). Quasi-Experimental Shift-Share Research Designs. *Review of Economic Studies*, 89(1), 181–213.

This chapter does not re-teach IV. Relevance, exclusion, the first stage, LATE — all of that is Week 3, and you should keep it loaded, because a shift-share instrument is *still an instrument* and every condition from Chapter 3.4 still applies to it. What is new is the *structure*: this instrument is assembled from a national part and a local part, and that structure is what lets us argue exogeneity in two distinct ways. We follow the usual reveal-the-trick order. First the plain statement and the construction. Then the two identification views, each with the assumption it leans on, when that assumption is credible, and how to diagnose it. Then the code, and a closing bridge that ends the causal-inference arc of the whole camp.

Our anchor is Maya. She wants to know whether a negative shock to *local labor demand* — a downturn in the industries that happen to employ a region's workers — causes households in that region to fall behind on their debt. Does a place getting economically hammered push its residents into credit-card delinquency and mortgage default? The trouble is the same endogeneity disease as always, and we will name it precisely in a moment.

---

## 1. The result in one plain sentence

> **Shift-share, stated plainly.** To get an instrument for how hard a *local* economy was hit, take the *national* growth rate of each industry — a shock that no single town can have caused — and reweight those national shocks by *how much each town depended on each industry to begin with*. A town that was heavily invested in industries that happened to boom nationally gets a high predicted shock; a town tied to nationally-declining industries gets a low one. That predicted shock is your instrument.

The whole idea lives in two words. **Shifts** are the national industry growth rates — how fast nationwide employment in, say, auto manufacturing, or finance, or retail, grew this year. **Shares** are the local exposure weights — what fraction of region $r$'s jobs were in autos, in finance, in retail, *at the start of the period*, before any of this year's shocks landed. The instrument is the **share-weighted sum of the shifts**: you sprinkle each region with the national shocks, but in the proportions that region was already exposed to.

Why would that be a good instrument for a region's *actual* economic shock? Because a region's realized fortunes mix two things: the national tide lifting or sinking its industries (exogenous to the region — Toledo did not cause the national auto cycle) and purely local stuff (a local scandal, a local boom, the very confounders we fear). The shift-share construction keeps only the first ingredient. It predicts what *should* have happened to region $r$ if it had simply ridden the national industry waves at its initial exposure, throwing away everything local. That predicted-from-national-tides shock is the clean lever; the realized local shock is the contaminated treatment it instruments for.

Everything technical below is an elaboration of that sentence, plus the long-delayed answer to *why the lever is clean* — which, it turns out, you can defend from the share side or the shift side, and the two defenses are the two halves of this chapter.

---

## 2. The construction, with numbers

Let me build the instrument concretely before writing any general formula, because the formula is opaque and the arithmetic is transparent.

Index regions (commuting zones, counties, MSAs — pick your geography) by $r$, and industries by $j$. There are two ingredients, measured at two different times.

**The shares** are local and measured at a *baseline* period, before the shocks we study. Let $s_{rj}$ be the fraction of region $r$'s employment that was in industry $j$ in the baseline year. For each region these fractions sum to one across industries: $\sum_j s_{rj} = 1$. These are the **exposure weights** — they say how much region $r$ "rode on" each industry.

**The shifts** are national and measured *over the period of interest*. Let $g_j$ be the national growth rate of industry $j$'s employment over the period — computed *leaving out* region $r$, or from the whole country (we will worry about that nuance later). These are the industry **shocks**: the auto industry shed $8\%$ of its jobs nationally, finance grew $3\%$, and so on. Crucially, $g_j$ is a *national* number; it is the same shock that every region feels, scaled by how exposed each region is.

The **Bartik / shift-share instrument** for region $r$ is the share-weighted sum of the shifts:

$$
B_r \;=\; \sum_{j} s_{rj}\, g_j .
$$

That is the entire object. Read it as a forecast: "given how region $r$ was distributed across industries at baseline, and given how each industry did nationally, here is the employment growth we'd *predict* for region $r$ from national forces alone."

Take a stripped-down example with three industries. Two of Maya's regions, Rustville and Finchester, started the period with very different industrial DNA:

| Industry $j$ | National shift $g_j$ | Rustville share $s_{rj}$ | Finchester share $s_{rj}$ |
|---|:---:|:---:|:---:|
| Auto manufacturing | $-8\%$ | $0.60$ | $0.05$ |
| Finance | $+3\%$ | $0.10$ | $0.55$ |
| Retail | $-1\%$ | $0.30$ | $0.40$ |

Rustville's predicted shock:

$$
B_{\text{Rust}} = (0.60)(-8\%) + (0.10)(3\%) + (0.30)(-1\%) = -4.8\% + 0.3\% - 0.3\% = -4.8\%.
$$

Finchester's predicted shock:

$$
B_{\text{Finch}} = (0.05)(-8\%) + (0.55)(3\%) + (0.40)(-1\%) = -0.4\% + 1.65\% - 0.4\% = +0.85\%.
$$

The instrument says: Rustville, leaning on autos in an auto downturn, should have been hit hard ($-4.8\%$); Finchester, leaning on a growing financial sector, should have done fine ($+0.85\%$). Notice that *the only thing distinguishing these two numbers is the shares* — both regions saw the identical national shifts $(-8\%, 3\%, -1\%)$. The shares did all the work of turning one set of national shocks into two different regional predictions. Hold that observation; it is the seed of the Goldsmith-Pinkham–Sorkin–Swift view in §5.

Equivalently, *the only thing that makes the same industry contribute differently across regions is the share*, and *the only thing that makes the predicted shock move at all is the shifts being nonzero and varied*. The instrument needs both to vary: if every region had identical shares, $B_r$ would be a constant and instrument nothing; if every industry grew at the same national rate, $B_r$ would just be that common rate times one, again a constant. Variation in $B_r$ across regions is born from the *interaction* of share dispersion and shift dispersion. That is the seed of the Borusyak–Hull–Jaravel view.

---

## 3. The canonical use: local labor-demand shocks

Why was this construction invented, and why is it the workhorse of regional economics? Bartik's original problem was the textbook simultaneity disease of Chapter 3.4, in regional form.

Suppose Maya runs the naive regression of a region-level outcome on the region's realized employment growth:

$$
Y_r = \beta_0 + \beta_1\, \Delta L_r + \varepsilon_r,
$$

where $Y_r$ is, say, the change in the household debt-delinquency rate in region $r$ and $\Delta L_r$ is the realized growth in local employment — her proxy for "how the local economy did." She wants $\beta_1$: the causal effect of a labor-demand shock on household financial distress. (State the spec in the CONVENTIONS §4 discipline: **outcome** = change in regional delinquency rate; **key regressor** = realized regional employment growth; **controls** = baseline region demographics; **fixed effects** = region and period if panel; **clustering** = by region; **sample** = U.S. commuting zones over the period; **identifying assumption** = the instrument below is as-good-as-randomly assigned, defended two ways in §5–6.)

The problem: realized local employment growth $\Delta L_r$ is *jointly determined* with the outcome and tangled with local confounders. A wave of local optimism could raise both employment and household borrowing (reverse-causality-style simultaneity). A local housing bubble could inflate employment *and* set up the later delinquency spike (an unobserved local confounder living in $\varepsilon_r$). Worst of all, $\Delta L_r$ blends *labor demand* (firms wanting to hire) with *labor supply* (workers moving in or out) — and Maya only wants the demand piece. So $\operatorname{Cov}(\Delta L_r, \varepsilon_r) \neq 0$: the regressor is endogenous, OLS is biased, and CIA is hopeless because the confounders are local and unmeasured.

Bartik's instrument isolates the demand piece by importing it from outside the region. The national industry shifts $g_j$ are demand-side shocks to each industry that an individual commuting zone is too small to have caused — Toledo's local conditions did not move the *national* auto cycle. Reweighting those national shocks by region $r$'s baseline industry mix predicts the labor-*demand* shock region $r$ should have received purely from riding national industry tides, stripped of local supply responses and local confounders. That predicted demand shock, $B_r$, is then used as an instrument for realized local growth $\Delta L_r$. First stage: do regions with worse predicted shocks actually have worse realized growth? (Yes — that is relevance, and it is testable.) Second stage: read the effect of growth on delinquency off the part of growth that the *national tides* explain.

This template — predict a local shock from national-industry-mix exposure, instrument the realized local shock with the prediction — is the canonical Bartik design. The same skeleton, with the nouns swapped, drives a huge applied literature: immigration's effect on wages (predict immigrant inflows to a city from national inflows by country-of-origin times the city's baseline settlement shares); the China trade shock (predict a region's import exposure from national Chinese import growth by industry times the region's baseline industry shares); and the finance examples we turn to next.

---

## 4. The finance version: regional bank-lending shocks and household credit

Maya's debt question fits the Bartik mold cleanly, and there is a second finance flavor worth seeing because it makes the share/shift logic vivid: **bank-lending shocks**.

Banks are not evenly spread. A region's credit supply depends on *which banks operate there*, and different banks expand or contract their lending at different national rates in a given year for reasons internal to each bank — a merger, a capital shock, a national strategy shift. So we can build a shift-share instrument for a region's credit-supply shock by combining:

- **Shares**: the fraction of region $r$'s baseline deposits (or loans) held by each bank $b$, call it $s_{rb}$ — the local exposure to each bank.
- **Shifts**: the national growth rate of each bank's lending, $g_b$, computed from the bank's lending *outside* region $r$ — a bank-level shock the region did not cause.

The instrument $B_r = \sum_b s_{rb}\, g_b$ predicts region $r$'s credit-supply shock from "which banks happened to be here, and how those banks did elsewhere." A town that banked heavily with an institution that contracted nationally gets a predicted credit crunch; a town tied to a nationally-expanding lender gets predicted easy credit. Maya can then ask whether a predicted credit-supply contraction raises household delinquency — instrumenting realized local credit growth with the bank-mix prediction, because realized local credit is endogenous (a town with deteriorating households both borrows differently and gets lent to differently). This is exactly the kind of design behind a strand of work on how bank health transmits to local real outcomes, and it is the household-credit cousin of the labor-demand story in §3.

Keep both finance examples in view, because they sharpen the two identification views. In the **labor** version there are a few hundred industries; in the **bank** version there might be only a handful of banks that dominate a region's deposits. As you will see in §6, "how many shocks, and how concentrated the shares" is precisely what decides which identification story you are allowed to tell.

---

## 5. Identification view I — it's the shares (Goldsmith-Pinkham, Sorkin & Swift 2020)

Now the long-delayed question: *why is $B_r$ a valid instrument?* The first modern answer comes from Goldsmith-Pinkham, Sorkin and Swift (2020), and it is the one that connects most directly to Chapter 3.4.

### The trick: a Bartik instrument is a recipe for combining many share-instruments

Look again at the construction $B_r = \sum_j s_{rj} g_j$ and ask: as we move from region to region, what is actually varying? In a given period the national shifts $g_j$ are *fixed numbers* — the same auto shock, the same finance shock, applied everywhere. The only thing that differs across regions is the vector of shares $(s_{r1}, s_{r2}, \dots)$. So from a cross-sectional standpoint, **the Bartik instrument is the shares, weighted by the shifts.** The shifts are not the source of cross-regional variation; they are the *weights* in a recipe that mixes many share-based instruments into one.

That reframing is the heart of GPSS. They show, with a little algebra, that running 2SLS with the single Bartik instrument $B_r$ is *numerically identical* to running an over-identified GMM/2SLS using **each industry's baseline share $s_{rj}$ as a separate instrument**, where the national shifts $g_j$ supply the particular weights GMM places on each share-instrument. In other words:

> **GPSS reframing.** The Bartik instrument is one specific linear combination of $J$ underlying instruments — the local industry shares. Using $B_r$ is equivalent to using all the shares $\{s_{rj}\}$ as instruments and combining them with the shifts as weights. So whatever makes $B_r$ valid must be a statement about the *shares*.

And here is the payoff. By Chapter 3.4, an instrument is valid only if it satisfies the exclusion restriction — uncorrelated with the structural error. If the operative instruments are the *shares*, then the identifying assumption is:

> **GPSS identifying assumption — exogenous shares.** Each baseline industry share $s_{rj}$ is uncorrelated with the region-level error $\varepsilon_r$: a region's *initial industrial composition* is as-good-as-randomly assigned with respect to whatever else drives the outcome. Formally, $\mathbb{E}[\varepsilon_r \mid s_{r1}, \dots, s_{rJ}] = 0$ (conditional on controls).

The shifts get a much lighter job. They need to be relevant (industries that grew nationally must actually move regional employment — the first stage) and they should be *consistent* in the sense of capturing genuine demand variation, but the *exogeneity* burden falls entirely on the shares. The national auto cycle is allowed to be endogenous to all sorts of macro forces; what must be exogenous is *that Rustville started out 60% auto*.

### When is "exogenous shares" credible — and when not?

This is a strong, very checkable-feeling assumption, and stating it this way immediately surfaces the threats. A region's baseline industry mix is *not* a coin flip; it is the product of history, geography, and policy. The exogeneity-of-shares assumption fails whenever a region's *initial specialization* is correlated with its *later outcome trajectory* for reasons other than the shock channel.

Maya's danger is concrete. Suppose regions that were heavily specialized in auto manufacturing at baseline were *also* regions with historically loose lending standards, weak financial literacy, or fragile household balance sheets — features that would have driven up delinquency *regardless* of the auto cycle. Then the auto share $s_{r,\text{auto}}$ is correlated with $\varepsilon_r$ (the latent fragility sitting in the error), exclusion fails on the share side, and the Bartik estimate is contaminated. The famous version of this worry in the trade literature: manufacturing-heavy regions were on a long secular decline for reasons predating the China shock, so their high manufacturing shares predict bad outcomes through a back door, not just through the import channel.

So "exogenous shares" is credible when **baseline industrial composition is plausibly unrelated to the outcome's other determinants**, and you defend it the way you defend any exclusion restriction (Chapter 3.4): with institutional argument, and — this is the GPSS contribution — with diagnostics. You can, and must, control for region characteristics that correlate with both shares and outcomes, run balance tests of shares against pre-period covariates and pre-trends (exactly the parallel-trends interrogation you learned for DiD in Chapter 4.1), and check robustness to dropping the most suspect industries. The assumption lives at the level of *each share*, which is what makes those checks possible.

### Diagnosing which shares drive the estimate: Rotemberg weights

Here is the GPSS diagnostic you must remember. If the Bartik instrument is secretly a weighted combination of $J$ share-instruments, then some industries get more weight than others — and the whole estimate could be riding on just a few. GPSS show how to compute **Rotemberg weights** $\hat{\alpha}_j$, one per industry, that decompose the Bartik 2SLS estimate as a weighted average of the $J$ "just-identified" estimates you'd get from each industry-share instrument alone:

$$
\hat{\beta}_1^{\text{Bartik}} = \sum_j \hat{\alpha}_j\, \hat{\beta}_{1,j}, \qquad \sum_j \hat{\alpha}_j = 1,
$$

where $\hat{\beta}_{1,j}$ is the IV estimate using only industry $j$'s share as the instrument. The weight $\hat{\alpha}_j$ measures how much industry $j$'s share-instrument contributes to (and can move) the headline number; a few high-$|\hat{\alpha}_j|$ industries typically dominate.

This is the shift-share analogue of the Rotemberg-weight idea you should file next to the *Rotemberg weights of DiD* (the negative-weights story of Chapter 4.2) — same spirit, different design: a headline estimate is a weighted average of building-block estimates, and you had better look at the weights. The practical recipe: rank industries by $|\hat{\alpha}_j|$; for the top few, sanity-check that *that* industry's share is plausibly exogenous (no back-door story), that the estimate $\hat{\beta}_{1,j}$ is not an outlier driving everything, and that the result survives dropping it. If your entire causal claim about household debt rests on the auto industry's share, and you cannot defend auto-share exogeneity, you do not have a result — you have a story about Rustville. Rotemberg weights tell you *where to aim your skepticism*, and computing them is the spine of nb4.5.

---

## 6. Identification view II — it's the shifts (Borusyak, Hull & Jaravel 2022)

Now the second lens, which at first sounds like a flat contradiction of the first. Borusyak, Hull and Jaravel (2022) locate identification not in the shares but in the **shifts** — and they are also right. The resolution of the apparent paradox is that the two papers make exogeneity assumptions about *different ingredients*, and they become credible in *different data regimes*.

### The trick: the shocks are a quasi-experiment

BHJ ask you to think about the national shifts $g_j$ themselves as the random thing. Imagine the universe drew the industry growth rates — auto down 8%, finance up 3%, retail down 1% — from some distribution, as-good-as-randomly across the many industries, *independent of how exposed any region was to them*. If the shifts are essentially a lottery over industries, then a region's predicted shock $B_r = \sum_j s_{rj} g_j$ is a region-specific *exposure-weighted average of random draws* — and the more industries there are, the more this average behaves like a clean experiment at the region level. The shares are now demoted to *exposure weights* (hence the title "exposure-weights view"): they are not required to be exogenous; they just determine how much of each random shock each region absorbs.

> **BHJ identifying assumption — quasi-randomly assigned shifts.** The national industry shocks $g_j$ are as-good-as-randomly assigned across industries (mean-independent of the industry-level unobservables, conditional on shock-level controls), and there are *many* shocks whose exposure is sufficiently dispersed. Identification is then a *shock-level* quasi-experiment: it is as if nature ran a randomized experiment on industries, and regions are bundles of industry bets.

The formal engine is a clever change of perspective: BHJ show the shift-share IV moment condition can be rewritten as a regression *at the level of the shocks (industries)*, exposure-weighted. Exogeneity of the shocks at that level is what you need, and — critically — **the shares are allowed to be endogenous.** A region's manufacturing specialization can be as historically-loaded as you like; as long as the *national manufacturing shock itself* was not systematically picked to coincide with manufacturing regions' latent trends, the design holds.

### When is "quasi-random shifts" credible — and how many shocks do you need?

This assumption is credible precisely when the GPSS one is shaky, and vice versa — which is the beautiful complementarity. It is most defensible when:

- **There are many industries (many shocks),** so the exposure-weighted average has a law-of-large-numbers logic to lean on. With $J$ in the hundreds (the labor-demand case), a single endogenous shock washes out. With $J$ a handful (Maya's *bank* version, where two banks hold most deposits), there is no "many" to invoke — a single big bank's idiosyncratic shock dominates, the LLN fails, and you should *not* lean on the BHJ story. This is why §4's "how many shocks" question decides your strategy: many industries → BHJ is natural; few concentrated shares → GPSS is your only honest defense.
- **Exposure is dispersed,** not concentrated in a few regions — so no single region drives the shock-level regression.
- **The shocks are plausibly as-good-as-random:** national auto demand swings for reasons (global oil prices, technology, foreign competition) that are not handpicked to hurt the specific regions that happen to be auto-heavy. You defend this with the same care as any exclusion argument, but now the unit of defense is the *industry*, not the region. A standard move is to *residualize the shocks against shock-level controls* (e.g., remove broad sector trends) so what remains is plausibly idiosyncratic.

The natural diagnostic here is also shock-level: report how many *effective* shocks you have (BHJ give an effective-sample-size measure — if a few industries carry all the exposure weight, your "many shocks" is an illusion), and check balance of the shifts against industry-level confounders, the shock-side analogue of the share-balance tests in §5.

### Adão–Kolesár–Morales: the standard errors are the sneaky problem

There is a third paper you must know, because it concerns *inference*, not identification, and it bites under *both* views. Adão, Kolesár and Morales (2019) pointed out that regions sharing similar industry shares are effectively exposed to the *same* shocks, which induces a correlation in their regression errors that ordinary clustering — say, clustering by region or by state — completely misses.[^akm] Two commuting zones on opposite coasts that are both auto-heavy will have correlated outcomes through the common auto shock, even though they share no geographic cluster. Standard shift-share standard errors are therefore too small, sometimes wildly, and the over-rejection can be severe. AKM derive standard errors valid under this **cross-regional correlation induced by shared exposure**; BHJ's shock-level regression delivers correct inference by construction (clustering at the shock level). The Chapter 2.4 lesson returns in a new guise: *the structure of your design dictates the structure of your dependence, and the wrong clustering lies to you about precision.* When you report a shift-share result, AKM-robust (or BHJ shock-level) standard errors are the honest choice, not vanilla region-clustered ones.

[^akm]: Adão, R., Kolesár, M., & Morales, E. (2019). Shift-Share Designs: Theory and Inference. *Quarterly Journal of Economics*, 134(4), 1949–2010.

---

## 7. Connecting back to Week 3 IV: relevance and exclusion, shift-share edition

Step back and map this whole chapter onto the IV vocabulary of Chapter 3.4, because a shift-share instrument earns no exemptions — it is an instrument, and the two conditions still rule.

**Relevance** is exactly as before, and exactly as testable. The first stage regresses the realized local shock (employment growth, or credit growth) on the constructed instrument $B_r$ and the controls; you want a large, precisely-estimated coefficient and a healthy first-stage F. Regions predicted to be hit hard by national tides should *actually* have been hit hard. This is checkable and you check it — though heed Chapter 3.5's warning that significance is not strength, and use robust/effective-F diagnostics. A weak shift-share first stage drags 2SLS back toward OLS just as surely as any weak instrument.

**Exclusion** is where the structure earns its keep, and where the two views are really two *strategies for arguing the same untestable restriction*. The shift-share exclusion restriction is that $B_r$ affects the outcome *only through* the realized local shock and is uncorrelated with $\varepsilon_r$. Since $B_r = \sum_j s_{rj} g_j$ is built from shares times shifts, that covariance can be made to vanish by making *either ingredient* exogenous:

- **GPSS route:** assume the *shares* are exogenous (initial industry mix unrelated to $\varepsilon_r$). Then any old shifts will do as weights. Defend it region-by-region; diagnose with Rotemberg weights; best when shares are plausibly random and shocks are few.
- **BHJ route:** assume the *shifts* are exogenous (national shocks as-good-as-random across many industries). Then any old shares will do as exposure. Defend it industry-by-industry; diagnose with effective number of shocks; best when shocks are many and dispersed.

This is the deep lesson and the reason the chapter holds two views without contradiction: **exclusion for a constructed instrument can be sourced from whichever ingredient you can most credibly call exogenous.** A product is exogenous to the error if either factor is — so the shift-share design gives you two independent shots at the single hardest, untestable assumption in all of IV. The honest empiricist names *which* shot they are taking, given their data, and brings the matching diagnostic. And just as in Chapter 3.4, what you identify is a *LATE-like* weighted average — here a weighted average across regions/shocks (the Rotemberg-weight decomposition makes the weights explicit), not a clean population average. "Whose effect did I estimate?" becomes "*which industries' shocks, with what weights, are driving this?*" — and Rotemberg weights are how you answer it.

---

## 8. The code

Here is the chapter in one runnable block: build a shift-share instrument from synthetic shares and national shifts in a world with an unobserved regional confounder, show OLS is biased, recover the truth with 2SLS, and decompose the estimate into Rotemberg-style industry weights so you can see which shares drive it. We set the true effect to $\beta_1 = -1.5$ (a worse local shock raises delinquency, coded so a negative employment shock maps to a positive delinquency change via the negative sign).

```python
import numpy as np
import pandas as pd
from linearmodels.iv import IV2SLS

rng = np.random.default_rng(20260528)
R, J = 400, 20          # 400 regions, 20 industries
beta1_true = -1.5

confounder = rng.normal(size=R)                      # latent regional fragility (in the error)

# Baseline LOCAL shares s_rj: a Dirichlet-style draw per region, rows sum to 1.
# Clean baseline: shares are independent of the confounder (we STRESS this in nb4.5).
alpha0 = rng.gamma(shape=0.5, size=(R, J))           # sparse-ish industry mix per region
S = alpha0 / alpha0.sum(axis=1, keepdims=True)       # (R x J), rows sum to 1

# NATIONAL shifts g_j: as-good-as-random across the 20 industries (the BHJ ideal).
g = rng.normal(0.0, 0.05, size=J)

# Shift-share (Bartik) instrument: B_r = sum_j s_rj * g_j  (standardized for clean scaling)
B = S @ g
B = (B - B.mean()) / B.std()                         # (R,)

# Realized local shock = clean part (driven by B) + endogenous local part (confounder)
local_shock = 1.0 * B + 0.8 * confounder + rng.normal(0, 0.3, size=R)

# Outcome: delinquency change. True effect beta1_true; confounder ALSO raises delinquency.
eps = 1.0 * confounder + rng.normal(0, 0.3, size=R)    # confounder lives in the error
Y = 0.0 + beta1_true * local_shock + eps

df = pd.DataFrame({"Y": Y, "shock": local_shock, "B": B, "const": 1.0})

# --- OLS: biased, because the confounder is in the error and correlates with the shock ---
ols = IV2SLS(df["Y"], df[["const", "shock"]], None, None).fit()
print("OLS  beta_hat:", round(ols.params["shock"], 3))

# --- 2SLS: instrument the endogenous local shock with the Bartik instrument B ---
iv = IV2SLS(df["Y"], df[["const"]], df[["shock"]], df[["B"]]).fit(cov_type="robust")
print("2SLS beta_hat:", round(iv.params["shock"], 3))
print("First-stage F:\n", iv.first_stage.diagnostics[["f.stat", "f.pval"]])

# --- Rotemberg-style decomposition: each industry-share as its own instrument ---
# beta_hat_j = IV estimate using ONLY industry j's share s_rj as the instrument.
betas_j = []
for j in range(J):
    zj = pd.DataFrame({"sj": S[:, j]})
    fit_j = IV2SLS(df["Y"], df[["const"]], df[["shock"]], zj).fit(cov_type="robust")
    betas_j.append(fit_j.params["shock"])
betas_j = np.array(betas_j)

# Rotemberg weights alpha_j proxy: each industry's contribution to the first stage,
# alpha_j ∝ g_j * Cov(s_rj, shock); normalize to sum to 1. (nb4.5 uses the exact GPSS formula.)
cov_sj_shock = np.array([np.cov(S[:, j], local_shock)[0, 1] for j in range(J)])
alpha = g * cov_sj_shock
alpha = alpha / alpha.sum()
order = np.argsort(-np.abs(alpha))
print("\nTop-5 industries by |Rotemberg weight|:")
print(pd.DataFrame({"industry": order[:5],
                    "rotemberg_w": np.round(alpha[order[:5]], 3),
                    "beta_j": np.round(betas_j[order[:5]], 3)}))
print("Reassembled beta (sum alpha_j * beta_j):", round(float((alpha * betas_j).sum()), 3))
```

Running it prints a biased OLS coefficient — about $-1.06$, because the confounder makes hard-hit regions look worse than the shock alone explains — a 2SLS coefficient that lands right on the true $-1.5$, a first-stage F in the hundreds (we built a real first stage with `1.0 * B`), and a table of the top industries by Rotemberg weight together with the industry-specific IV estimates $\hat{\beta}_{1,j}$ that, weighted by $\hat{\alpha}_j$, reassemble the headline 2SLS number to $-1.5$. Two things to watch. First, OLS and 2SLS disagree, and the gap ($-1.06$ versus $-1.5$) *is* the regional endogeneity made visible — exactly the reason for the exercise. Second — and this is the GPSS lesson in code — the decomposition shows the estimate is not spread evenly: a handful of industries carry most of the Rotemberg weight, and those are the shares whose exogeneity you must defend hardest. In this clean baseline the shares were drawn *independently* of the confounder, so every $\hat{\beta}_{1,j}$ hovers near $-1.5$ and the design is sound; nb4.5 then *stresses* it by tying the shares to the confounder, so that the high-weight industries become exactly the ones whose share-exogeneity is violated — and you watch the headline number drift away from the truth even while the F-statistic still looks reassuring. nb4.5 also replaces the proxy weights with the exact GPSS formula, adds AKM-robust standard errors, and walks the full decomposition table cell by cell.

---

## What to carry forward

Four things from this chapter will do real work in the weeks ahead.

First, **a shift-share instrument is *built*, not found**. When the world refuses to hand you a clean coin flip, you can manufacture an instrument from a national part (industry **shifts** — growth rates no single region caused) and a local part (baseline **shares** — exposure weights), combined as $B_r = \sum_j s_{rj} g_j$. The canonical use is local labor-demand shocks; the finance uses — regional bank-lending shocks, local industry exposure driving household credit and default — are the same skeleton with the nouns swapped.

Second, **identification has two faces, and you choose your defense by your data**. Goldsmith-Pinkham–Sorkin–Swift: the Bartik is a GMM combination of share-instruments, so exogeneity of the *initial shares* is the key assumption — credible when baseline industry mix is plausibly unrelated to the outcome's other drivers, best when shocks are few. Borusyak–Hull–Jaravel: identification is a quasi-experiment in the *shifts*, as-good-as-randomly assigned across *many* industries — credible when there are many dispersed shocks, and it lets the shares be endogenous. A product is exogenous if *either* factor is, so the design gives you two shots at the one untestable assumption. Name your shot.

Third, **diagnose, don't assert**. Rotemberg weights tell you which industries' shares actually drive the estimate — aim your share-exogeneity skepticism there, and check robustness to dropping them. The effective number of shocks tells you whether "many shocks" is real or an illusion. And Adão–Kolesár–Morales tell you the standard errors are the sneaky failure: regions with similar shares share shocks, ordinary clustering misses it, and unadjusted shift-share standard errors are too small.

Fourth, **it is still IV**. Relevance is testable (check the first-stage F, robustly, per Chapter 3.5); exclusion is arguable (now sourceable from shares *or* shifts); and what you identify is a Rotemberg-weighted average of effects, the shift-share cousin of LATE. Every habit from Chapter 3.4 transfers.

### The arc closes — and the next one opens

Step all the way back. Weeks 3 and 4 built you a causal-inference toolkit from the ground up: potential outcomes and SUTVA (3.1); the CIA family — matching, propensity scores, balancing, doubly-robust (3.2–3.3); the escape from CIA via instruments (3.4–3.5); and then the design-based methods that exploit *structure* in the world to defend identification — difference-in-differences and the staggered-adoption crisis (4.1–4.2), regression discontinuity (4.3), synthetic control (4.4), and now shift-share (4.5). You now own the modern empiricist's full kit and, more importantly, the *reflex* that matters more than any single estimator: for every design, name the threat, name the assumption that addresses it, separate what the data can test from what you must argue, and bring the diagnostic that shows where the result is fragile.

That reflex is the whole point, because Weeks 5 and 6 turn from *building* tools to *reading* the frontier work that uses them. You will stop deriving estimators and start decoding published empirical papers — tables-first, the way professionals read — using this exact toolkit as your lens, including papers by Prof. Gao. The questions you have been trained to ask in these two weeks — *what's the design, what's the identifying assumption, where are the weights, is the inference honest?* — are precisely the questions a Reader's Guide is built around. You spent four chapters learning shift-share so that when a paper says "we instrument local exposure with a Bartik shift-share design," you do not nod along; you ask whether they defended the shares or the shifts, whether they showed Rotemberg weights, and whether their standard errors are AKM-robust. That is what it means to read the frontier. Turn the page.

---

## Your Turn

Open **nb4.5 — "Bartik instrument decomposition."** You will (1) construct a shift-share instrument from a synthetic panel of regional shares and national shifts and confirm the first stage is strong; (2) show OLS is biased while 2SLS recovers the true effect, and verify the headline 2SLS number equals the Rotemberg-weighted average of the per-industry IV estimates $\hat\beta_{1,j}$; (3) compute the exact GPSS Rotemberg weights, rank the industries that drive the estimate, and stress the design by tying shares to a confounder — watching the most-suspect shares earn the biggest weights — then re-run inference with AKM-robust standard errors and compare them to vanilla region-clustered ones.

Before you start, make sure you can answer these:

1. **Shares vs. shifts.** Maya builds a bank-lending shift-share instrument for two regions; one region holds $70\%$ of its deposits in a single bank that contracted lending $12\%$ nationally. (a) Write out $B_r = \sum_b s_{rb} g_b$ in words for that region. (b) She has only six banks with concentrated shares. Which identification view — GPSS (exogenous shares) or BHJ (quasi-random many shifts) — can she honestly invoke, and why does the *other* one fail in her data? (c) Which condition (relevance or exclusion) can she test, and which must she argue?

2. **Rotemberg weights.** A classmate's Bartik estimate of the effect of local labor-demand shocks on delinquency is $\hat\beta_1 = -1.4$, and the Rotemberg decomposition shows $80\%$ of the weight sits on a single industry, oil-and-gas, whose own instrument gives $\hat\beta_{1,\text{oil}} = -3.0$. (a) What does this tell you about where the result comes from? (b) Name one concrete back-door story by which oil-and-gas *share* could violate the GPSS exogenous-shares assumption for a delinquency outcome. (c) What single robustness check would you demand first?

3. **Inference.** Two commuting zones on opposite coasts are both heavily exposed to the auto industry. (a) Why are their regression errors correlated even though they share no geographic cluster, and what does that do to ordinary region-clustered standard errors? (b) Who derived the standard errors that fix this, and what feature of the design do they account for? (c) How does the BHJ shock-level regression get honest inference "for free"?
