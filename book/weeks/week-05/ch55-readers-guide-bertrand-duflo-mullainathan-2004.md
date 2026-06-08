# Chapter 5.5 — Reader's Guide: Bertrand, Duflo & Mullainathan (2004)

> **Bertrand, M., Duflo, E., & Mullainathan, S. (2004). How Much Should We Trust Differences-in-Differences Estimates? *Quarterly Journal of Economics*, 119(1), 249–275.**

You already met this paper. In Week 4, when Priya clustered her wildfire-regulation standard errors by state and watched the t-stat fall from a triumphant 5.0 to a sobering 1.8, the footnote said: *this is the lesson of Bertrand, Duflo & Mullainathan*. Back then it was a footnote — a rule you obeyed. This week we read it the way a professional reads a paper: not as a rule handed down, but as an argument someone had to *win*. And the argument BDM won is one of the most unsettling in all of empirical economics, because it is not about any particular study being wrong. It is about a whole *method* of computing standard errors being wrong, in a way that made hundreds of published difference-in-differences results look far more certain than the data ever justified.

Here is the whole paper in one sentence, and we will spend the chapter unpacking it: **when you run a standard DiD regression on a long panel and report the usual standard errors, those standard errors are too small — often dramatically — because the outcome is serially correlated over time within each unit, and the conventional formula pretends it is not.** Too-small standard errors mean too-large t-statistics, which mean you reject the null too often, which means you "discover" effects that are not there. BDM did not just assert this. They *measured* it, with a trick — the placebo-law experiment — that is so clean you will be able to run it yourself by the end of the week.

This is a methods paper, also called a *credibility* paper: it studies not the world but the way economists study the world. Read it as the empirical equivalent of an auditor showing up at a firm that has been reporting suspiciously smooth profits.

---

## 1. The research question

The question is narrow, technical, and enormous in consequence: **do the conventional standard errors reported in difference-in-differences studies dramatically overstate statistical significance?**

To see why anyone would worry, recall the anatomy of a DiD study from Week 4. A researcher has a state-year panel — say, women's wages in each of the 50 states observed annually for 20-some years. At some point a state passes a law (a minimum-wage change, a benefit reform, an insurance regulation), and the researcher estimates the two-way fixed-effects regression you carried all of last week,

$$
Y_{ist} = \alpha_s + \lambda_t + \beta\, D_{st} + \varepsilon_{ist},
$$

where $s$ indexes states, $t$ indexes years, $i$ indexes individuals, $\alpha_s$ are state fixed effects, $\lambda_t$ are year fixed effects, and $D_{st}$ turns on when state $s$ has the law in year $t$. The coefficient $\beta$ is the policy effect; the researcher reports $\hat\beta$ and a standard error, computes $t = \hat\beta / \mathrm{SE}(\hat\beta)$, and declares significance if $|t| > 1.96$.

Everything hinges on that standard error being honest. And BDM's suspicion — the seed of the whole paper — is that the standard DiD standard error is built on an assumption that the data flatly violate. The assumption is that the residuals $\varepsilon_{ist}$ are independent across time within a state. The reality, for the slow-moving outcomes economists actually study, is that they are not: a state with high women's wages this year almost certainly had high women's wages last year. This is **serial correlation**, the within-unit autocorrelation you first met as a disease in Chapter 2.4, and BDM's thesis is that it quietly poisons DiD inference.

Notice what kind of question this is. It is a **size** question, in the exact sense of Week 1. The *size* of a test is the probability it rejects a true null — the Type I error rate, the $\alpha$ you set to 0.05 and promised yourself you would honor. BDM are asking: when DiD researchers say "significant at 5%," is the true size really 5%, or is it something far worse? If the machinery is broken, the test that advertises a 5% false-positive rate might actually fire 30% or 40% of the time on pure noise. That is the question, and it is answerable — which is the beautiful part.

---

## 2. The identification strategy: the placebo-law experiment

How do you *test* whether a standard error is honest? You cannot just stare at one. A standard error is a claim about a sampling distribution — about how much $\hat\beta$ would bounce around if you could rerun history. BDM's move is to **rerun history on purpose, under a null they control**, and count how often the test misbehaves. This is the placebo-law experiment, and it is the heart of the paper.

The recipe is almost mischievous in its simplicity. Take a real panel — actual state-year data on some outcome like women's wages, with all its real serial correlation baked in. Now invent a **fake law.** Pick a random subset of states and declare they were "treated" starting in some random year. There was no real law; nothing actually happened to those states. So the *true* effect of this placebo intervention is, by construction, exactly **zero.** Then run the standard DiD regression with the conventional standard error, compute the t-statistic on the placebo treatment, and ask the Week-1 question: did it cross 1.96?

Now repeat. Draw a new random set of placebo states and a new random year, run it again, check significance again. Do this hundreds or thousands of times. Each run is a draw from a world where the null — "no effect" — is *known* to be true, because you made it true. So the fraction of runs that come back "significant" is a direct, brute-force estimate of the **true size** of the test. This is exactly the simulation logic from the Week 1 coin-flip lab, where you built a universe with a genuinely fair coin and counted how often your test wrongly called it biased. BDM build a universe with a genuinely null law and count how often DiD wrongly calls it real.

And here is the whole experiment's punchline waiting to be sprung. *If the standard errors were honest, the placebo rejection rate would come back at about 5% — that is what 5% means.* Reject 5% of the time on data you know is null, and the machinery is working as advertised. Reject far more than 5%, and you have caught the standard error red-handed: it is too small, the t-stats are inflated, and the test is crying wolf. The placebo design converts an abstract worry about serial correlation into a single number you can read off a table — the empirical size of the test. That conversion, from "I suspect the SEs are wrong" to "here is the false-positive rate, measured," is the identification strategy. Note the kinship with Week 4's permutation/placebo inference for Priya's one-treated-state design: there, you assigned the fake treatment to each control state to build a null distribution for *one* study. BDM industrialize the same idea into a referendum on the *method*.

---

## 3. The data

The paper runs on the kind of panel that DiD studies actually use, and that is the point — BDM want their indictment to land on real research practice, not a strawman. The workhorse dataset is **CPS-style microdata aggregated to state-year cells**: the Current Population Survey, the U.S. government's monthly labor-market survey, from which one can build, for each state and each year, an average outcome such as women's log wages or an employment rate. [CHECK: exact CPS years and the specific wage variable used in the lead experiment.]

Two features of this data make it the perfect crime scene. First, it is a **long panel** — many years per state — and serial correlation only does real damage when there are enough time periods for the within-state persistence to accumulate. With two periods there is little room for an autocorrelation problem to grow; with twenty, a slow-moving outcome's residuals form long, gently drifting runs that the independence assumption badly misreads. The longer the panel, BDM show, the worse the over-rejection. Second, the outcomes are **economically persistent in exactly the way that matters**: wages, employment, and similar variables move slowly: this year looks a lot like last year, so a state's residuals are positively autocorrelated. That persistence is not a data-cleaning artifact you can scrub away; it is the genuine time-series structure of the economy, and it is precisely what the conventional DiD standard error ignores. BDM also note that the treatment dummy $D_{st}$ is itself extremely persistent within a state — off for years, then on for years — and Week 4 taught you (via the Moulton intuition) that a highly persistent regressor combined with serially correlated errors is the worst case for naive standard errors.

---

## 4. Table-by-table reading order

A professional does not read this paper front to back. Read it tables-first, in the order that tells the story.

**Start with the placebo rejection-rate table — the headline.** This is the table that made the paper famous, and it is the first thing to find. It reports, for the conventional DiD specification, the fraction of placebo laws (true effect zero) that came back statistically significant at the 5% level. Read down the column for the standard, serial-correlation-ignoring standard error and look for a number that should be near 0.05 and is not — it is far higher. *Do not memorize a precise figure;* what matters, and what is robustly true, is that the over-rejection is **severe — many times the nominal 5%**, large enough that a substantial fraction of pure-noise "laws" look significant. [CHECK: the exact headline rejection rate for the OLS/conventional row — the often-quoted figure is roughly 0.45, but confirm against Table I before quoting a number.] Once you have seen this one number, you understand the whole paper: the advertised 5% test is, in truth, a coin-flip-ish test. Everything else is diagnosis and cure.

**Then read the table that varies the panel length.** Having established that over-rejection happens, BDM show *when it gets worse*, and the answer — longer panels, more serial correlation — confirms the mechanism. This is the table that rules out "maybe it's just noise" and pins the blame on autocorrelation. Read it as the paper's argument that it has found the *right* culprit, not just *a* symptom.

**Then read the fixes table(s) — the cures.** Having diagnosed the disease, BDM test remedies and report the rejection rate each one delivers. Read this table asking a single question of every row: *did this fix bring the rejection rate back down to roughly 5%?* The remedies, in rough order of how the paper treats them:

- **Block bootstrap.** Resample whole *states* (entire time series, kept intact) rather than individual observations, so the bootstrap preserves each state's serial-correlation structure instead of shattering it. This respects the within-unit dependence and brings the size back toward 5%, especially when the number of states is not tiny.
- **Clustering at the state level.** This is the cluster-robust standard error of Chapter 2.4, with the cluster set to the unit at which treatment is assigned — the state. It lets each state's residuals be *arbitrarily* correlated across all its years (the block-diagonal $\boldsymbol\Omega$, one block per state), which is exactly the serial-correlation pattern the disease consists of. With enough states, clustering restores honest size. This is the fix that became the field's default, and the reason Priya clustered by state last week.
- **Collapsing to pre/post.** Throw away the time dimension's internal structure entirely: average each state's data into one "before" number and one "after" number, reducing the panel to effectively two periods per state. With only two periods there is no within-period serial correlation left to misread, so a simple comparison delivers honest size. The cost — and BDM are upfront about it — is power: you have discarded information, so true effects are harder to detect. We return to this trade-off below.

Reading in this order — symptom, mechanism, cure — is how the paper actually argues, and it is the reading-order heuristic this whole week is teaching you.

---

## 5. What's clever

Three things, and they compound.

The first and deepest is **the placebo design as a way to test inference itself.** Most papers test a hypothesis about the world. BDM test a hypothesis about a *procedure* — about whether the standard-error formula tells the truth — and they do it by manufacturing a setting where the right answer is known. Because the placebo law has a true effect of exactly zero by construction, *any* rejection is a false positive, full stop, with no ambiguity about what "should" have happened. This sidesteps the entire problem of never observing the counterfactual that haunts ordinary causal work: here the researcher *is* the counterfactual's author. It is the same intellectual move as building a simulator where you play God (Week 1's coin universe, Week 4's tunable pre-trend), elevated into a critique of an entire literature.

The second is **quantifying the over-rejection rather than merely warning about it.** Economists had long known, in the abstract, that serial correlation could bias standard errors. What BDM did was put a *number* on the danger — turning a vague methodological caveat into a measured 5%-should-be-but-isn't fact. A number changes behavior in a way a caveat never does; "your standard errors might be a little off" is ignorable, but "your test that claims 5% actually fires on noise a third of the time or more" is not.

The third is that **they did not just break things; they offered fixes that work and that practitioners could actually adopt.** Block bootstrap, cluster-by-state, collapse-to-two-periods — all are implementable with the tools of the day, and they each demonstrably pull the rejection rate back toward 5%. A critique with a remedy attached is one people will use, and they did: clustering by the unit of treatment is now so standard that omitting it is treated as an error, which is precisely why it was non-negotiable for Priya.

---

## 6. What's vulnerable

A good reader pushes back, and there are real soft spots — most of which are about the cures, not the diagnosis.

The first is the **few-clusters problem**, which BDM themselves flag and which Week 4 hammered home. The clustering fix and the block bootstrap both rely on having *many* clusters — the rule of thumb is 30 to 50 — because the cluster-robust formula estimates the within-cluster correlation from variation *across* clusters, and with few clusters there simply is not enough of it. With the 50 U.S. states you are roughly in the safe zone, but a great many real DiD designs have far fewer treated units (recall Priya's *single* treated state, and Card–Krueger's essentially one). In the small-number-of-clusters regime, the very fix BDM recommend can itself over-reject, and you need further corrections (the wild cluster bootstrap of Cameron, Gelbach & Miller, 2008, or few-cluster $t$ adjustments). So the cure is not universal; it is a large-number-of-clusters cure.

The second is the **power cost of collapsing to two periods.** Averaging the panel down to pre/post buys honest *size* — but Week 1 reminds you that size and power trade off, and you cannot drive both errors to zero with fixed data. By discarding the within-period time variation you weaken the test's ability to detect a *true* effect when one exists (Type II error rises). Collapsing is the safest fix for false positives and one of the weakest for finding real signals; which matters more depends on whether your study is more endangered by crying wolf or by missing a real wolf.

The third is **dependence on the panel's length and structure.** BDM's headline numbers are tied to the specific autocorrelation and the specific length of the CPS panels they used. A different outcome with weaker serial correlation, a shorter panel, or a different treatment-timing structure would over-reject by a different amount — so the precise 5%-should-be-but-isn't figure is not a universal constant but a property of *this* data-generating process. The qualitative lesson (ignoring serial correlation inflates significance, and the longer/more-persistent the panel the worse it gets) is robust; the exact magnitude travels less well, and a careful reader should treat any single number as illustrative of a mechanism rather than a law of nature.

---

## 7. Three replication exercises

These are scaffolded toward **nb5.5**, the BDM placebo-law simulation. You are reproducing the *spirit* of the paper — a clean simulated panel, not the proprietary CPS extract — but the mechanism, and the punchline, are identical.

1. **Reproduce a placebo-DiD false-positive rate.** Simulate a state-year panel with serially correlated within-state errors (e.g., an AR(1) process so this year's shock partly carries over to next year) and *no* true treatment effect. In each of 1,000 replications, assign a random placebo law to a random subset of states starting in a random year, run the TWFE regression with the **conventional** standard error, and record whether $|t| > 1.96$. Report the empirical rejection rate. You should see it land *far above* 0.05 — this is BDM's headline table, rebuilt on your laptop, and the moment the abstract worry becomes a number you measured.

2. **Turn the dial on serial correlation and on panel length.** Rerun Exercise 1 sweeping the AR(1) persistence parameter from 0 (independent errors) up toward 1 (highly persistent), and separately sweeping the number of years $T$ from small to large. Plot the placebo rejection rate against each. At zero persistence the rate should sit near the honest 5%; as persistence and panel length grow, it should climb — reproducing BDM's mechanism evidence and proving to yourself that serial correlation, not chance, is the culprit.

3. **Test the cures.** Hold the data-generating process fixed at a strongly serially correlated setting and rerun the placebo experiment three more times, swapping in each fix: (a) **cluster the standard errors by state**, (b) **block-bootstrap by resampling whole states**, and (c) **collapse each state to a single pre and post average** and run the two-period comparison. Tabulate the four rejection rates side by side (conventional + three fixes). Confirm that each fix drags the rate back toward 5%, then, as a stretch, shrink the number of states to a handful and watch the clustering fix start to over-reject again — rediscovering the few-clusters caveat from §6 with your own simulation.

---

### Where this goes next

Open **`nb5.5`** (`notebooks/week-05/nb5.5-bdm-placebo-law.ipynb`), the BDM placebo-law simulation, where you build the serially correlated panel, run the placebo experiment across standard-error flavors, and read the false-positive rate off your own output rather than off a table in a 2004 journal. The three exercises above are its backbone; the "Your Turn" extension pushes the few-clusters regime until clustering itself breaks.

**Referee questions to carry into the lab and the discussion:**

1. The headline placebo rejection rate is a property of the CPS panel's specific serial-correlation structure and length. How sensitive is the indictment to those choices — would an outcome with weaker autocorrelation, or a much shorter panel, still embarrass the conventional standard error, and by how much?

2. BDM rehabilitate inference partly through clustering and the block bootstrap, both of which lean on having many clusters. Given that an enormous share of influential DiD studies have *few* treated units, does the paper's recommended cure actually reach the designs that need it most, or does it quietly assume the easy case (many states)?

3. Collapsing to pre/post restores honest size at a cost in power. For a policy evaluation where missing a real effect is itself costly (a public-health or fair-lending intervention, say), is the collapse the right default — or does buying size with power trade one error for a more dangerous one, and how should a researcher decide which error to fear more?
