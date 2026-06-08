# D.5 — Prose Style

The other sections of Appendix D govern objects you can see: D.1 a table's layout and notes, D.2 which coefficients you report and how you disclose fixed effects and clustering, D.3 a robustness section built around a threats-and-responses table, D.4 the replication packet. This section governs the sentences that hold those objects together — the prose. It is the easiest part of the style guide to wave away ("I'll just write how I write") and the one a referee judges fastest, because a single overclaiming verb in your abstract tells a trained reader, in four seconds, that you do not yet know what your design can support.

Here is the reveal that organizes everything below, stated before the rules so you carry it through them. **In an empirical paper, your prose is a promise about your evidence, and every verb is a clause of that promise.** When you write "the program *reduces* the gap," you are promising a causal design strong enough to license the word *reduces*. When you write "is *associated with*," you are promising less, honestly. The reader does not take your word for the result; they read your *verbs* as a confession of how strong your design is, and they check the confession against the design section. Calibrated prose is therefore not a matter of taste or politeness — it is the same discipline as a correct standard error, applied to language. Get the verb wrong and you have misreported your result as surely as if you had printed the wrong number.

---

## D.5.1 The weakest-assumption rule: matching verbs to the design

The rule from Chapter 8.3 §7 is the spine of this entire section, so state it plainly and then never forget it: **your strongest verb is bounded by your weakest assumption.** The strength of your causal language is capped not by your best robustness check or your most careful control, but by the single weakest link in your identification — because that is the link a skeptic attacks, and your verb is a claim that the link holds.

The mapping from design to permissible verb is not a matter of opinion; it is close to a lookup table, and a reader who knows designs reads it as one:

| Design | Earns | Forbidden |
|--------|-------|-----------|
| Randomized experiment | "causes," "increases," "the effect of," "raises by" | — |
| Quasi-experiment, identifying assumption *testable and passed* (DiD with flat pre-trends; RD with smooth density) | "causally estimate," "the program reduced," *with the assumption named* | unconditional "causes" |
| Observational regression on observables (OLS with a plausible omitted variable you could not rule out) | "is associated with," "predicts," "is consistent with," "suggestive of" | "causes," "the effect of," "leads to" |
| Descriptive / predictive (a momentum sort, a factor model) | "documents," "captures variation in," "describes" | any causal verb at all |

Notice the three verbs students most often confuse, because the distinctions are exactly the ones referees punish. **"Is associated with"** is a statement about a joint distribution — two things move together in your sample — and it commits you to nothing about *why*. It is the honest verb for an observational regression, and it is never wrong, only sometimes weaker than you earned. **"Causes"** is a statement about a counterfactual: had the treatment been different, the outcome would have been different. It requires a design that defends that counterfactual, and on observational data you almost never have it. **"Leads to"** is the sneaky one: it *sounds* like a hedge, softer than "causes," but it is a fully causal verb dressed in a cardigan — "X leads to Y" asserts that X produces Y just as firmly as "causes" does. Do not reach for "leads to" thinking you have hedged; you have made the same causal claim in a quieter voice, and a trained reader hears it at full volume.

The discipline has a concrete enforcement step, the one Week 5 trained you to run on published authors: **after a draft is done, read *only* the verbs attached to your main result, in every section, and force each one down to the level your weakest assumption permits.** Underline every verb that touches the headline coefficient. For each, ask: did the design earn this word? If your design is a clean staggered difference-in-differences with flat pre-trends, you earned "the program reduced the gap, under parallel trends" — say it, with the assumption attached. If your design is OLS on observables with an omitted variable you named but could not eliminate, you earned "is associated with," and nothing stronger, anywhere.

---

## D.5.2 Hedging versus overclaiming — and the mush in between

There are two opposite failures, and calibration means avoiding *both*, not fleeing one into the arms of the other.

**Overclaiming** is the loud failure: claiming more than the design supports. It is the OLS regression whose author writes "we show that financial literacy *causes* higher savings," when all they have is a correlation between a literacy survey score and a savings rate, with a dozen plausible confounders (income, parental wealth, patience) sitting in the error term. The verb writes a check the design cannot cash, and the referee bounces it.

**Mush** is the quiet failure, and beginners flee into it the moment they are warned about overclaiming: hedging so heavily that no claim survives. "Our results *may possibly* suggest that, *under certain conditions*, there *could perhaps* be a *tentative* relationship that *might* indicate..." — by the end of that sentence the reader cannot tell what you are actually asserting, and a claim nobody can locate is a claim nobody can believe or check. Over-hedging is not modesty; it is a refusal to commit, and it reads as a writer who does not understand their own evidence well enough to say what it shows.

The target between them is **precise calibration**: claim *exactly* as much as your design supports, no more and no less. If you ran a clean DiD with flat pre-trends and a battery of passed robustness checks, you have *earned* a confident, plainly stated claim — "the program reduced the gap by 1.8 percentage points, and this estimate is credible under parallel trends" — and you should make it, in those words, with the assumption attached and no apologetic fog around it. The hedge belongs on the *assumption*, not smeared across the whole sentence. One well-placed conditional ("under parallel trends," "absent the confound we discuss in §6") does the entire job of honesty; a dozen scattered modal verbs do nothing but blur.

Watch especially for **drift**, the most common way calibration fails in practice. The abstract hedges correctly ("we document a robust association"); the introduction is a touch bolder ("our results suggest the program reduces the gap"); the results section forgets itself ("the program reduces the gap by 1.8 points"); and by the conclusion the verbs have climbed all the way to "we have shown that fair-lending exams *cause* a decline in discrimination." Each step up is small; the cumulative drift is a paper that ends by claiming far more than it began by promising. The verb-audit of §1 is the cure: run it across *all* sections at once, so the abstract and the conclusion are held to the same ceiling.

---

## D.5.3 The one-sentence contribution

Every paper needs one sentence that answers the question a skeptical reader is entitled to ask: *what is true now that was not established before you did this work?* Chapter 8.3 §3 treats this as the load-bearing sentence of the introduction; here the style point is narrower and sharper. **The contribution sentence states what is now *known*, not what you *did*** — and its verb obeys §1 exactly, because the contribution sentence is where overclaiming bites first and is caught first.

"We run a difference-in-differences on HMDA data" describes an activity; it is a sentence about your afternoon. "We provide the first quasi-experimental estimate of how state fair-lending examination programs affect the minority–white mortgage-denial gap" describes a *contribution to knowledge*; it is a sentence about the world. The second is what belongs in the paper, and notice its verb — "estimate," with "quasi-experimental" naming the design that licenses it — is calibrated to the staggered-DiD design and not one notch stronger. A practical test: hand the sentence to a classmate who has not seen your project. If they can tell you what you did and why it matters, it works; if they ask "wait, is that causal?", the verb is miscalibrated and the sentence is doing the introduction's job badly.

---

## D.5.4 Citing primary sources — and the [CHECK]-don't-fabricate rule

Two rules govern citation, and the second is non-negotiable in a way the first is not.

First, **every empirical claim cites at least one primary source with full bibliographic information** (CONVENTIONS §6) — authors, year, title, venue, volume/pages. Cite the paper that *did* the thing, not a textbook that mentions it or a blog that summarizes it; "Petersen (2009)" for clustered standard errors in panel finance, not "a paper I read about clustering." And cite to *position*, not to pad: a citation that does not mark a wall of the map or the edge of your gap (D.3 and Ch 8.3 §4) is a citation that should be deleted, because a padded reference list signals counting rather than arguing.

Second, and this is the rule that has no exceptions: **if you cannot verify a citation, tag it `[CHECK]` rather than fabricate it** (CONVENTIONS §6). A hallucinated reference — a plausible-sounding author, year, and title for a paper that does not exist, or real authors attached to a journal they never published in — is the single error a referee can catch in ten seconds and never forgive, because it tells them your *other* facts may be invented too. When you are unsure of a volume number, a page range, or whether the result you remember is really in the paper you remember, write the claim and append `[CHECK]` so a later pass (or a reviewer) resolves it against the real source. A visible `[CHECK]` is a flag of honesty; a confidently fabricated citation is the opposite, and the asymmetry in how a referee receives them could not be larger. Never invent a reference to fill a hole. Tag the hole.

---

## D.5.5 Active voice, and the honest-limitations paragraph

**Prefer the active voice.** "We estimate a staggered difference-in-differences" is clearer, shorter, and more honest about agency than "a staggered difference-in-differences was estimated" — the passive hides *who did what*, and in a methods section that agency matters, because the reader wants to know what *you* chose. The passive has legitimate uses (when the actor is genuinely irrelevant — "the data were collected by the Census Bureau"), but the default is active, and a draft drowning in "it was found that" and "it can be argued that" is a draft hiding behind grammar. Write "we find," "we control for," "we cluster by state."

**The honest-limitations paragraph** is the place students most want to skip and most need to write. It belongs in the conclusion (Ch 8.3 §6) and it is where the residual-concern column of your threats table finally appears in the paper's prose: the confounds you could not rule out, the populations your sample does not cover, the mechanism you measured an effect on but could not fully open. Stating limits plainly is not weakness — it is the candor that makes a referee trust everything else you wrote, the prose analogue of the conceded-fatal-critique move from Chapter 8.5. The paragraph that admits "our design cannot rule out X, so the honest reading is a strong association consistent with the mechanism rather than the clean causal estimate we hoped for" reads as the work of someone who sees their project clearly; the conclusion that declares the question permanently settled reads as someone who has not yet been refereed. And guard the verbs here especially — the conclusion is the most-quoted part of the paper after the abstract, and it is exactly where drifted verbs ("this paper *proves*") undo eleven pages of calibrated honesty in one sentence.

---

## D.5.6 Banned phrases

A short list of phrases that should never appear in your paper, each because it signals a specific failure a reader will pounce on.

- **"controls for endogeneity."** Endogeneity is not a thing you spray on a regression; it is a *named* problem (omitted variables, simultaneity, measurement error) addressed by a *named* design. The phrase is hand-waving that hides the absence of an argument, and CONVENTIONS §4 forbids it outright: name the threat and name the design that addresses it. Write "to address the concern that bank size is correlated with both adoption and the gap, we include county fixed effects and show the result survives in §6," not "we control for endogeneity."
- **"in today's fast-paced world"** (and its cousins: "in an increasingly globalized economy," "now more than ever," "since the dawn of finance"). These are content-free throat-clearing that open a paper with marketing instead of a fact (CONVENTIONS §1). Open with a concrete number or tension — a denial gap, a volatility spike, a policy date — not with a platitude about the times.
- **"proves" / "definitively shows"** (for any empirical result). Empirical work *provides evidence*; it does not *prove*, which is a word for mathematics. Even a clean experiment estimates an effect with uncertainty.
- **"the data speak for themselves."** They do not; you are interpreting them, and this phrase ducks the interpretive work that is your job.
- **"obviously" / "clearly" / "it is well known that."** If it were obvious you would not be writing it, and these words pressure the reader to agree rather than showing them why. Cut them and let the evidence carry the claim.

---

## D.5.7 Worked rewrites: good versus bad

The rules above are abstract until you see them applied. Here are sentence-level rewrites, each tagged with the rule it enforces. Read the bad version, see why it fails, and study how little has to change to fix it.

**Causal language on observational data (§1).**
> Bad: *Financial literacy leads to higher retirement savings, increasing balances by 12%.*
> Good: *Higher financial-literacy scores are associated with retirement balances about 12% larger, a gap that persists after controlling for income and education but that we cannot interpret causally, since more patient households may both learn more and save more.*

The bad sentence uses "leads to" (a causal verb, §1) and "increasing" on a design — a literacy survey correlated with savings — that cannot support either. The good sentence reports the same number with "associated with," names the residual confound (patience), and tells the reader exactly how far to trust it.

**The endogeneity dodge (§6, CONVENTIONS §4).**
> Bad: *We control for endogeneity using fixed effects.*
> Good: *Adopting states might differ from non-adopting states in ways correlated with the denial gap; county and year fixed effects absorb time-invariant county differences and common shocks, and our identifying assumption is that, absent the program, adopters' and non-adopters' gaps would have trended in parallel.*

The bad sentence is the banned phrase; it names no threat and no design. The good sentence names the threat (selection into adoption), names what the fixed effects do, and states the identifying assumption in one sentence — the CONVENTIONS §4 form.

**Drift into the conclusion (§2).**
> Bad: *In sum, we have proven that fair-lending examinations eliminate discriminatory lending.*
> Good: *In sum, we estimate that fair-lending examinations reduced the county-level denial gap by about 1.8 percentage points under the parallel-trends assumption we defend in §4; we cannot speak to discrimination in lending channels our HMDA sample does not observe.*

"Proven" and "eliminate" are overclaims (§6, §1); the good version keeps the calibrated verb from the results section, re-attaches the assumption, and states a limit in the same breath.

**Over-hedging into mush (§2).**
> Bad: *Our results may possibly suggest that, under some conditions, there could perhaps be a tentative association that might indicate an effect.*
> Good: *We find a robust association — stable across the alternative specifications in §6 — though our observational design cannot rule out selection on unobservables, so we read it as suggestive rather than causal.*

The bad sentence has hedged itself into asserting nothing. The good sentence makes a definite claim ("a robust association"), then places *one* honest caveat on it (selection on unobservables), which is calibration, not mush.

**The empty opener (§6, CONVENTIONS §1).**
> Bad: *In today's fast-paced financial world, volatility is more important than ever.*
> Good: *When the first U.S. spot Bitcoin ETF launched in January 2024, the underlying token's daily volatility fell by a third within a month — a drop large enough to matter for anyone pricing options on it.*

The bad sentence is throat-clearing; the good sentence is a concrete fact with a stake, the hook of Chapter 8.3 §2.

**Activity versus contribution, in the active voice (§3, §5).**
> Bad: *A difference-in-differences was run on the data, and some interesting results were found.*
> Good: *We provide the first quasi-experimental estimate of how state fair-lending examination programs affect the minority–white denial gap, exploiting the staggered timing of adoption.*

The bad sentence is passive, describes an activity, and previews nothing; the good sentence is active, states a contribution to knowledge, and carries a verb ("estimate," qualified "quasi-experimental") calibrated to its design.

---

The thread through all of this is the reveal from the top: your prose is a promise about your evidence, and the reader audits the promise against the design. Match every verb to your weakest assumption, hedge the assumption rather than the whole sentence, cite real sources and flag the unverified ones with `[CHECK]`, write in the active voice, admit your limits plainly, and never reach for the banned phrases that hide an absent argument. Do that and a referee reading your prose arrives at the same confidence your design actually warrants — which is the entire goal, because a paper that earns *exactly* the belief it deserves is the one that survives. See D.1–D.3 for the tables, figures, and robustness sections this prose surrounds, and D.4 for the packet that lets a skeptic check that the numbers in those calibrated sentences are real.
