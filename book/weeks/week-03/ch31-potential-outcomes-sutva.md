# Chapter 3.1 — Potential Outcomes, SUTVA, and the Fundamental Problem of Causal Inference

Maya has a number she does not trust, and this time the problem is not her regression.

She has been volunteering at a community credit union that runs a free financial-literacy program — six evening sessions on budgeting, credit scores, and how to read a loan offer. Enrollment is voluntary: anyone can sign up. Maya pulls the records and asks the obvious question. Among people who came through the program, **62%** had their next loan application approved. Among people who did not enroll, only **41%** were approved. That is a 21-percentage-point gap, and it is wildly statistically significant — thousands of applicants, a t-statistic that would make any beginner reach for the champagne. The program, it seems, *causes* a 21-point jump in approval. Maya is ready to write it up and recommend the credit union expand the program nationwide.

And she is about to make a mistake that is subtler, and far more dangerous, than anything in Week 2 — because there is no omitted control she can add to fix it, no standard error she can robustify, no diagnostic test that will warn her. The mistake is buried in the word *causes*.

Here is the thing she has not asked. *Who signs up for a free six-week evening course on personal finance?* People who are already organized enough to commit six weeknights. People already worried about their credit, already saving, already the type to read the fine print. The kind of person who voluntarily enrolls in a financial-literacy program is, on average, **already more likely to get a loan approved** — program or no program. So when Maya compares enrollees to non-enrollees, she is not comparing the same people with and without the program. She is comparing two *different kinds of people*. The 21-point gap is some unknown blend of two things: whatever the program actually does, plus the head start the enrollees already had. Her number cannot tell her how much is which.

This chapter builds the machinery to say that sentence *precisely* — precisely enough to write down an equation, decompose Maya's 21 points into its honest pieces, and see exactly which piece is the causal effect she wants and which piece is the contamination. The framework is called the **potential-outcomes model** (also the Rubin causal model, after the statistician Donald Rubin who formalized it in the 1970s, building on much earlier work by Jerzy Neyman on agricultural experiments). It is the language the entire rest of the camp speaks. Every method in Week 3 and Week 4 — matching, weighting, instrumental variables, difference-in-differences, regression discontinuity — is, at bottom, a different strategy for solving the one problem this chapter is going to pose. So we go slowly and get the definitions exactly right. By the end you will be able to look at any "X causes Y" claim, in finance or anywhere, and locate the precise assumption it is leaning on.

We follow the usual reveal-the-trick structure. First, the clean idea: what a causal effect *is*, defined so carefully that the definition itself exposes why causation is hard. Then the worked numbers on Maya's case. Then the algebra that decomposes her naive comparison into a causal piece and a bias piece. Then the assumption (SUTVA) that the whole framework quietly rests on, and where it breaks in finance. And finally the one design — randomization — that makes the bias provably vanish, which is why it is the gold standard everything else is measured against.

---

## 3.1.1 Two outcomes that cannot both happen

Start with one person. Forget samples and averages for a moment; we will build everything from a single unit, because the whole framework is clearest there.

Take one applicant — call her unit $i$. There is a treatment she might or might not receive: enrollment in the financial-literacy program. And there is an outcome we care about: whether her next loan is approved. The central move of the potential-outcomes framework — the move that makes everything else possible — is to imagine, for this one person, **two parallel worlds**:

- In one world, she **enrolls** in the program. Her loan outcome in that world is a number we write $Y_i(1)$ — read "$Y$-sub-$i$-of-one," the outcome for unit $i$ *if treated*. (For a yes/no outcome like approval, code it $1$ for approved, $0$ for denied, so $Y_i(1)$ is either $1$ or $0$; for a continuous outcome like a credit score, it is a real number.)
- In the other world, the very same person **does not enroll**. Her outcome there is $Y_i(0)$ — "$Y$-sub-$i$-of-zero," the outcome *if untreated*.

These two numbers, $Y_i(1)$ and $Y_i(0)$, are called unit $i$'s **potential outcomes**. They are properties of the person, fixed in advance, that exist *before* anyone decides whether she enrolls. $Y_i(1)$ is what *would* happen to her under treatment; $Y_i(0)$ is what *would* happen to her under no treatment. The word "potential" is doing real work: both numbers are real features of the world — what *would* occur in each scenario — but at most one of them will ever be realized.

Now define the **treatment indicator**

$$D_i = \begin{cases} 1 & \text{if unit } i \text{ receives the treatment (enrolls)},\\ 0 & \text{if not.}\end{cases}$$

The treatment $D_i$ acts like a switch that selects *which* of the two parallel worlds actually happens. The outcome we get to *observe* — the one that lands in Maya's dataset — is whichever potential outcome the switch points to:

$$\boxed{\ Y_i = D_i\, Y_i(1) + (1 - D_i)\, Y_i(0)\ }$$

Stare at this for a second, because it is the hinge of the whole framework, and it is just careful bookkeeping. If $D_i = 1$, the formula collapses to $Y_i = Y_i(1)$: we see her treated outcome. If $D_i = 0$, it collapses to $Y_i = Y_i(0)$: we see her untreated outcome. The equation is sometimes called the **observation rule** or the **consistency** link — it says the observed outcome equals the potential outcome corresponding to the treatment actually taken. It is not an assumption about the world; it is the *definition* of how the world we observe relates to the two worlds we imagine.

With this in hand, the **individual treatment effect** for unit $i$ writes itself. The causal effect of the program *on this one person* is the difference between her two parallel-world outcomes:

$$\tau_i = Y_i(1) - Y_i(0).$$

That is what "the program's effect on Maya's applicant" *means*, stated with full precision: the gap between what happens to her with the program and what happens to her without it, holding the person and everything else fixed. If $\tau_i = 0.3$ for a continuous outcome, the program raises *her* credit score by $0.3$; if her outcome is binary and $\tau_i = 1$, the program flips her from denied to approved; if $\tau_i = 0$, the program does nothing for her. This is a clean, assumption-free definition of a causal effect. There is no regression here, no error term, no statistics at all yet — just two numbers and their difference.

And now the trap springs.

---

## 3.1.2 The Fundamental Problem of Causal Inference

Look again at the individual treatment effect $\tau_i = Y_i(1) - Y_i(0)$, and look at the observation rule $Y_i = D_i Y_i(1) + (1-D_i)Y_i(0)$. Put them side by side and a brutal fact emerges.

For any single person, the treatment switch $D_i$ takes exactly one value. If she enrolled ($D_i = 1$), we observe $Y_i(1)$ — and $Y_i(0)$, the world where she *didn't* enroll, never happens. We do not get to see it. If she did not enroll ($D_i = 0$), we observe $Y_i(0)$, and $Y_i(1)$ — the world where she *did* — is the one that never happens. **We can never observe both potential outcomes for the same unit.** One of them is always realized; the other is forever a hypothetical, a road not taken.

This is the **Fundamental Problem of Causal Inference** (the name is due to the statistician Paul Holland, 1986), and it deserves a box because the rest of the camp is a hundred different attempts to wriggle around it:

> **The Fundamental Problem of Causal Inference.** For each unit $i$ we observe at most *one* of the two potential outcomes $Y_i(1)$, $Y_i(0)$ — whichever one the treatment $D_i$ selected. The other is the **missing counterfactual**. Therefore the individual treatment effect $\tau_i = Y_i(1) - Y_i(0)$ can *never* be computed from data for any single unit. Causal inference is, irreducibly, a **missing-data problem.**

It is worth sitting with how strange this is. The individual effect $\tau_i$ is a perfectly well-defined number — it is the difference of two real features of unit $i$. There is nothing fuzzy or probabilistic about it. And yet it is *unobservable in principle*, not because our instruments are crude or our sample is small, but because reality only runs one of the two worlds. No amount of data on person $i$ — not a billion observations, not a perfect measurement — will ever reveal $\tau_i$, because the data can only ever come from the world that actually happened. The counterfactual leaves no trace.

Lay it out as a table to make the missingness vivid. Suppose we could somehow peek at both columns for five of Maya's applicants (we cannot — this is a thought experiment, the "science table" we will never fully see):

| Unit $i$ | $Y_i(0)$ (if no program) | $Y_i(1)$ (if program) | $\tau_i = Y_i(1)-Y_i(0)$ | $D_i$ | Observed $Y_i$ |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | 0 | 1 | $+1$ | 1 | $Y_1(1)=1$ |
| 2 | 1 | 1 | $0$ | 0 | $Y_2(0)=1$ |
| 3 | 0 | 0 | $0$ | 1 | $Y_3(1)=0$ |
| 4 | 0 | 1 | $+1$ | 0 | $Y_4(0)=0$ |
| 5 | 1 | 1 | $0$ | 1 | $Y_5(1)=1$ |

The first three columns are the truth — the *full* science table, with both potential outcomes for everyone. The middle column, $\tau_i$, is what we wish we knew. But in real life we only get the last two columns: the treatment each person took, and the *one* potential outcome it selected. Everything to the left of $D_i$ is, for any given person, half-hidden — for unit 1 we see $Y_1(1)=1$ but $Y_1(0)$ is missing; for unit 2 we see $Y_2(0)=1$ but $Y_2(1)$ is missing. The blanks are not noise. They are structural, permanent, and they are the entire reason causal inference is hard.

So we are stuck — at the *individual* level. The escape, which the rest of this chapter develops, is to stop asking about individuals and start asking about **averages over a population.** We cannot recover any single $\tau_i$, but with the right design we *can* recover the average of the $\tau_i$'s across many people. The Fundamental Problem says individual effects are gone forever. It does *not* say average effects are. That distinction is the whole ballgame.

---

## 3.1.3 The estimands: ATE, ATT, and a first look at LATE

When you cannot recover individual effects, you ask about averages, and you have to be careful about *which* average. An average causal effect, defined as a feature of the population we want to learn, is called an **estimand** — the target we are trying to estimate, named before we ever touch data. (Contrast with an *estimator*, the formula we apply to data, and an *estimate*, the number it spits out — the trio you met in Chapter 1.3. The estimand is the thing in the world; the estimator is the recipe; the estimate is the dish.) Three estimands carry the entire week, so we name them now and use this notation for the rest of camp.

**The Average Treatment Effect (ATE)** is the mean of the individual treatment effects over the *whole* population:

$$\text{ATE} = \mathbb{E}[\tau_i] = \mathbb{E}\big[Y_i(1) - Y_i(0)\big] = \mathbb{E}[Y_i(1)] - \mathbb{E}[Y_i(0)].$$

In words: if we could enroll *everyone* in the program versus enroll *no one*, the ATE is the average change in the outcome. It answers the policy question "what if we made this universal?" In Maya's five-unit table the individual effects are $+1, 0, 0, +1, 0$, so the ATE is $2/5 = 0.4$ — on average across these five, the program flips $40\%$ of applicants from denied to approved. (Of course we computed that from the hidden columns; the point of the week is to recover it *without* them.)

**The Average Treatment effect on the Treated (ATT)** restricts the average to the units who *actually received* the treatment:

$$\text{ATT} = \mathbb{E}[\tau_i \mid D_i = 1] = \mathbb{E}\big[Y_i(1) - Y_i(0)\,\big|\, D_i = 1\big].$$

This conditions on $D_i = 1$ — it averages the effect only over the enrollees. It answers a *different* question: "for the people who chose to enroll, how much did the program help *them*?" That is often the policy-relevant quantity — the credit union cares what its program does for the people who use it, not for hypothetical universal enrollees who might respond differently. The ATE and the ATT are equal only when the treated are, in their responsiveness, a representative slice of the population. When the people who select into treatment are exactly the people the treatment helps most (or least), ATT and ATE diverge — and that gap is itself an important fact about the world. Note the subtle thing inside the ATT: it involves $\mathbb{E}[Y_i(0)\mid D_i=1]$, the average *untreated* outcome **among the treated** — the counterfactual "how would the enrollees have done if they hadn't enrolled?" That term is missing data of the worst kind, and you will see in a moment that it is exactly where Maya's trouble lives.

**The Local Average Treatment Effect (LATE)** is the third, and we only *name* it here — its full treatment waits for Chapter 3.4 on instrumental variables. The teaser: sometimes you can neither randomize nor convincingly control, but you have a lever — an *instrument* — that nudges *some* people into treatment without directly touching their outcomes. The catch is that the lever moves only a *subset* of the population (the people who comply with the nudge), and so it identifies the average effect only *for that subset* — the "compliers." That subset-specific average is the LATE. It is "local" because it is local to the compliers, not the whole population: a fourth estimand, narrower than the ATE, that you can sometimes recover when the first two are out of reach. File the name away; we will earn it properly in 3.4.

Three estimands, three questions: *everyone* (ATE), *the treated* (ATT), *the compliers* (LATE). They are different numbers answering different questions, and a recurring source of confusion — and bad policy advice — is reporting one while claiming another. The discipline the rest of the week enforces is to *say which estimand you are after before you estimate anything.*

---

## 3.1.4 The naive estimator, and why Maya should not trust it

Back to Maya's 21 points. What did she actually compute? She took the average observed outcome among enrollees and subtracted the average observed outcome among non-enrollees:

$$\widehat{\Delta} = \underbrace{\overline{Y}_{D=1}}_{0.62} - \underbrace{\overline{Y}_{D=0}}_{0.41} = 0.21.$$

In population terms, her estimator is targeting the **naive difference in means**,

$$\Delta = \mathbb{E}[Y_i \mid D_i = 1] - \mathbb{E}[Y_i \mid D_i = 0],$$

the difference in *observed* average outcomes between the treated and untreated groups. This is the quantity every spreadsheet, every dashboard, every "users who did X had higher Y" headline reports. The question that decides whether it means anything is: **when is $\Delta$ equal to a causal effect?** To answer it, we translate $\Delta$ from the language of observed outcomes into the language of potential outcomes — and the answer falls out as an exact decomposition. This derivation is the heart of the chapter; do it once carefully and the rest of causal inference clicks into place.

Begin with the two terms. Among the treated, the observation rule says the observed $Y_i$ equals $Y_i(1)$, so

$$\mathbb{E}[Y_i \mid D_i = 1] = \mathbb{E}[Y_i(1) \mid D_i = 1].$$

Among the untreated, the observed $Y_i$ equals $Y_i(0)$, so

$$\mathbb{E}[Y_i \mid D_i = 0] = \mathbb{E}[Y_i(0) \mid D_i = 0].$$

Therefore the naive difference is

$$\Delta = \mathbb{E}[Y_i(1) \mid D_i = 1] - \mathbb{E}[Y_i(0) \mid D_i = 0].$$

So far this is exact and assumption-free — just the observation rule applied twice. Now comes the one trick of the derivation, the same "add and subtract zero" move you have seen before. We want the ATT, $\mathbb{E}[Y_i(1)-Y_i(0)\mid D_i=1]$, to appear. The ATT needs $\mathbb{E}[Y_i(0)\mid D_i = 1]$ — the treated group's *untreated* potential outcome, that missing counterfactual from §3.1.3. It is nowhere in $\Delta$. So we conjure it by adding and subtracting it:

$$\Delta = \mathbb{E}[Y_i(1) \mid D_i = 1] \; \underbrace{-\; \mathbb{E}[Y_i(0)\mid D_i=1] \;+\; \mathbb{E}[Y_i(0)\mid D_i=1]}_{\text{added and subtracted: equals } 0} \; -\; \mathbb{E}[Y_i(0)\mid D_i=0].$$

Now group the four terms into two pairs. The first pair is the ATT; the second pair is something new:

$$\Delta = \underbrace{\Big(\mathbb{E}[Y_i(1)\mid D_i=1] - \mathbb{E}[Y_i(0)\mid D_i=1]\Big)}_{\textstyle \text{ATT}} + \underbrace{\Big(\mathbb{E}[Y_i(0)\mid D_i=1] - \mathbb{E}[Y_i(0)\mid D_i=0]\Big)}_{\textstyle \text{selection bias}}.$$

There it is — the decomposition the whole week pivots on:

$$\boxed{\ \underbrace{\mathbb{E}[Y_i\mid D_i=1] - \mathbb{E}[Y_i\mid D_i=0]}_{\text{naive difference } \Delta} \;=\; \underbrace{\text{ATT}}_{\text{what we want}} \;+\; \underbrace{\mathbb{E}[Y_i(0)\mid D_i=1] - \mathbb{E}[Y_i(0)\mid D_i=0]}_{\text{selection bias}}\ }$$

The naive difference in means equals the causal effect on the treated (ATT) **plus a selection-bias term**. And read what that bias term *is*:

$$\text{selection bias} = \mathbb{E}[Y_i(0)\mid D_i=1] - \mathbb{E}[Y_i(0)\mid D_i=0].$$

It is the difference in the **untreated potential outcome** $Y_i(0)$ between the two groups. In plain English: *how would the enrollees have done without the program* ($\mathbb{E}[Y_i(0)\mid D_i=1]$) versus *how the non-enrollees actually did without the program* ($\mathbb{E}[Y_i(0)\mid D_i=0]$). It compares the two groups in a world where *neither* gets treated — it measures how different the groups already were, on the outcome scale, *before the program touched anyone.* If the people who enroll would have had higher approval rates anyway — which is exactly Maya's worry — then $\mathbb{E}[Y_i(0)\mid D_i=1] > \mathbb{E}[Y_i(0)\mid D_i=0]$, the selection bias is positive, and Maya's 21 points *overstate* the program's true effect on the treated.

This is the clean, exact statement of what Week 2's omitted-variable bias was groping toward. There it was "a relevant correlated variable leaks into the error term." Here it is sharper and more general: **the comparison group's outcome is a bad stand-in for the treated group's missing counterfactual, by exactly the amount the two groups differ in $Y(0)$.** No regression assumption, no functional form — just the definitions. The naive difference *always* decomposes this way. The only question is whether the selection-bias term is zero.

---

## 3.1.5 Maya's puzzle, decomposed on real numbers

Let us put numbers to it so the decomposition stops being algebra and starts being a story. Suppose — and we can only *suppose*, because the counterfactuals are unobserved — the truth about Maya's two groups is this:

- **Enrollees** ($D=1$): their average approval *with* the program is $\mathbb{E}[Y(1)\mid D=1] = 0.62$ (this we observe). Had they *not* enrolled, their average would have been $\mathbb{E}[Y(0)\mid D=1] = 0.55$ (this we do *not* observe — it is the counterfactual). So the program's true effect on the enrollees is $\text{ATT} = 0.62 - 0.55 = 0.07$.
- **Non-enrollees** ($D=0$): their average approval *without* the program is $\mathbb{E}[Y(0)\mid D=0] = 0.41$ (this we observe).

Now run the decomposition:

$$\Delta = \text{ATT} + \text{selection bias} = \underbrace{(0.62 - 0.55)}_{0.07} + \underbrace{(0.55 - 0.41)}_{0.14} = 0.07 + 0.14 = 0.21.\ \checkmark$$

Maya's headline 21 points splits cleanly into **7 points of real program effect** and **14 points of selection bias.** Two-thirds of her "effect" is not the program at all — it is the simple fact that enrollees were already $14$ percentage points more approvable than non-enrollees, *before the program did anything*, because of who they are. The program helped (the ATT is a genuine $+0.07$), but Maya's naive number overstates that help by a factor of three. If she recommends a nationwide rollout promising "+21 points," she will badly disappoint, because the +14 was never the program's to give.

And here is the cruelty that connects back to Week 2: **nothing in Maya's data reveals the split.** She observes $0.62$ and $0.41$. The numbers $0.55$ — the enrollees' counterfactual — is missing, structurally, by the Fundamental Problem. She cannot compute the selection bias, so she cannot subtract it off. A bigger sample makes $0.62$ and $0.41$ more precise; it does nothing to recover the hidden $0.55$. A robust standard error tightens the confidence interval around a *biased* number. This is the wall Week 2 ended on, now stated in its sharpest form: the problem is not estimation, it is *identification* — whether the quantity we can compute even equals the quantity we want.

So the entire enterprise of causal inference reduces to one mission: **make the selection-bias term go to zero, or estimate it, or design around it.** Everything in Weeks 3 and 4 is a tactic for that mission. Before we meet the cleanest tactic, we have to make explicit one assumption the framework has been quietly leaning on the whole time.

---

## 3.1.6 SUTVA: the assumption hiding in the notation

Go back to the very first move, where we wrote down $Y_i(1)$ and $Y_i(0)$ for unit $i$. That notation smuggled in an assumption so basic it is easy to miss, and it is load-bearing for everything above. We wrote unit $i$'s potential outcome as depending only on *unit $i$'s own* treatment — a single number $Y_i(1)$ for "treated" and a single number $Y_i(0)$ for "untreated." That is **SUTVA**, the **Stable Unit Treatment Value Assumption**, and it has two distinct parts that you must check separately:

**Part 1 — No interference.** One unit's treatment does not affect another unit's potential outcomes. Maya's applicant 7's loan outcome depends on whether *she* took the program, not on whether applicant 8 did. Formally, this is what lets us write $Y_i(d)$ as a function of $i$'s own treatment $d$ alone, rather than a function of the *entire vector* of everyone's treatments. Without it, "the potential outcome under treatment" is not even well-defined for a single unit, because it would depend on what everybody else did.

**Part 2 — No hidden versions of treatment.** There is only one "treatment" and one "control," consistently defined. "Enrolling in the program" means the same thing for everyone — not a watered-down version for some and an intensive version for others. If "treatment" is secretly several different treatments, then $Y_i(1)$ is ambiguous: *which* version of $1$? SUTVA insists treatment is a single, well-defined condition so that $Y_i(1)$ is a single, well-defined number.

When both parts hold, the potential-outcomes notation we have used is legitimate and the decomposition of §3.1.4 stands. When either fails, the framework does not just lose precision — it loses *meaning*, because the objects $Y_i(1)$, $Y_i(0)$ are no longer well-defined. SUTVA is not a minor technical footnote; it is the foundation under the foundation.

Finance is unusually good at breaking it, because financial actors are connected — through markets, prices, networks, and competition — in exactly the ways SUTVA forbids. Three examples, one for each kind of failure:

- **Spillovers (interference), Maya's own program.** Suppose enrollees teach their roommates and siblings what they learned — how to dispute a credit-report error, how to time an application. Then a *non*-enrollee living with an enrollee gets some of the treatment second-hand. Her $Y_i(0)$ — supposedly "outcome with no program" — is contaminated by her neighbor's treatment. Interference. The control group is no longer a clean "no-treatment" world, and the naive comparison understates the program's reach because the "untreated" were partly treated.

- **General equilibrium (interference at market scale), Devon's case.** Devon studies a tax credit that subsidizes first-time crypto-asset purchases, and wants its effect on adoption. If a *few* people get the credit, no problem — but if it scales nationwide, the surge in demand moves the *price*. Now everyone — credit recipients and non-recipients alike — faces a different market. The non-recipients' $Y_i(0)$ shifts because of *other people's* treatment, operating through the price. This is the classic **general-equilibrium** failure of SUTVA: a treatment that is harmless to study at small scale because it leaves prices alone can have completely different (and harder to study) effects at large scale, where it moves the equilibrium everyone trades at. The partial-equilibrium estimate does not extrapolate to the policy.

- **Hidden versions of treatment, Priya's case.** Priya evaluates whether "adopting an ESG disclosure standard" lowers a firm's cost of capital. But "adopting the standard" is not one thing: one firm publishes an audited, detailed report; another files a vague two-paragraph statement to check the box. Coding both as $D_i = 1$ violates SUTVA's second part — there is no single $Y_i(1)$, because "treated" hides a spectrum of intensities. Priya's estimate is an uninterpretable blend of effects from genuinely different treatments masquerading as one.

The practical upshot: every causal claim you make or read sits on a SUTVA assumption, and you should be able to state it out loud. "I am assuming no spillovers between units, and that the treatment is the same well-defined thing for everyone." Often it is fine — a small pilot program with unconnected participants rarely moves markets or leaks across people. Sometimes it is fatally wrong. Either way, *name it*, the way the empirical-spec discipline of CONVENTIONS demands. SUTVA failures cannot be fixed by randomization (the tool we turn to next); randomizing *who* gets treated does nothing about treatments *spilling* across units or *meaning different things*. SUTVA has to hold (or be designed for, via cluster-level treatment or scale limits) before randomization can do its job.

---

## 3.1.7 Randomization: the design that zeroes selection bias

Now the payoff. We have a villain with a name — the selection-bias term $\mathbb{E}[Y_i(0)\mid D_i=1] - \mathbb{E}[Y_i(0)\mid D_i=0]$ — and we want it to be zero. The cleanest way to make it vanish is to take the decision of *who gets treated* out of human hands and hand it to a coin.

Suppose that instead of letting people choose, the credit union **randomly assigns** the program: flip a fair coin (or, more realistically, a computer's random-number generator) for each applicant, enroll the heads, leave the tails as controls. The applicant has no say. What does randomization buy us? It makes the treatment indicator $D_i$ **statistically independent of the potential outcomes**:

$$\big(Y_i(0),\, Y_i(1)\big) \perp\!\!\!\perp D_i.$$

That symbol $\perp\!\!\!\perp$ means "is independent of." The claim is that *which group you land in* ($D_i$) carries no information about *what your outcomes would be* ($Y_i(0), Y_i(1)$), because the coin does not know or care who you are. The organized, credit-savvy, already-approvable applicants are split evenly across treatment and control by chance; so are the disorganized ones. The two groups become, in expectation, *the same kind of people* — identical in their distribution of potential outcomes, differing only in the coin flip.

Watch what independence does to the selection-bias term. Independence means conditioning on $D_i$ does not change the expectation of a potential outcome:

$$\mathbb{E}[Y_i(0)\mid D_i=1] = \mathbb{E}[Y_i(0)\mid D_i=0] = \mathbb{E}[Y_i(0)].$$

The untreated potential outcome has the *same* average in both groups — because the groups are interchangeable by construction. So the selection bias is

$$\mathbb{E}[Y_i(0)\mid D_i=1] - \mathbb{E}[Y_i(0)\mid D_i=0] = 0.$$

It is gone. Identically, randomization equates the *treated* potential outcome across groups, $\mathbb{E}[Y_i(1)\mid D_i=1] = \mathbb{E}[Y_i(1)\mid D_i=0] = \mathbb{E}[Y_i(1)]$, which collapses the distinction between ATT and ATE — when the treated are a random slice, "the effect on the treated" equals "the effect on everyone." Feed the zero back into the master decomposition:

$$\Delta = \text{ATT} + 0 = \text{ATE}.$$

The naive difference in means — the *simplest possible estimator*, two averages subtracted — now equals the causal effect, full stop. In Maya's numbers: had the program been randomized, the enrollees' counterfactual $\mathbb{E}[Y(0)\mid D=1]$ would have equaled the controls' observed $0.41$, not the inflated $0.55$ that her self-selected enrollees brought to the table. The difference in means would have read off the true effect directly, no contamination to subtract.

This is why a **randomized controlled trial** (RCT) is called the **gold standard** of causal inference. It does not *measure* the selection bias and subtract it; it *prevents it from existing*, by design, before any data is collected. The credibility comes not from a clever estimator but from the *coin* — from the physical act of randomizing assignment, which severs the link between who-gets-treated and who-they-are. You will see RCTs everywhere serious money cares about causation: clinical trials, A/B tests at every tech and fintech company, field experiments in development economics, the lending experiments that test whether a disclosure or a nudge actually changes borrower behavior. When you can randomize, randomize. The math could not be simpler, and that simplicity is the point — the work was done by the design, not the statistics.

Two honest caveats, both of which motivate the rest of the camp. First, randomization zeroes selection bias *in expectation*, over the randomness of assignment; in any one finite sample the coin might, by bad luck, deal a few more savvy applicants to the treatment group. That residual imbalance is *sampling variation* — it shrinks with sample size and is exactly what the standard errors and confidence intervals of Week 1 quantify. It is a precision issue, not a bias issue, and it is the *good* kind of problem: it goes away with more data. Second, and far more important: **most of the time you cannot randomize.** You cannot randomly assign families to take on student debt, firms to adopt ESG standards, neighborhoods to receive bank branches, or countries to suffer financial crises — for reasons of ethics, cost, law, or because the event already happened in the historical record you are stuck with. The data you get is *observational*: people and firms selected their own treatments, and the selection-bias term is alive and nonzero. That is the world empirical finance actually lives in, and it is why the next four chapters exist.

---

## 3.1.8 The bridge to "controlling for X" — and what the next chapters do

So what do you do when you cannot randomize? Week 2 already offered an answer, and it is worth seeing precisely where it fits — and where it falls short — in this new language.

When you "control for $X$" in a regression — add credit score, income, age, employment to Maya's approval regression — you are trying to *manufacture* the comparability that randomization gives for free. The hope is that *within* groups of applicants who match on all the $X$'s, treatment is "as good as randomly assigned": among two applicants with identical credit, income, and employment, whether one enrolled in the program is plausibly just noise, unrelated to their potential outcomes. If that hope holds, the selection bias vanishes *conditional on $X$*, and a regression that controls for $X$ recovers the causal effect. This assumption has a name we will use all week — **conditional independence**, also called **unconfoundedness** or **selection on observables**:

$$\big(Y_i(0), Y_i(1)\big) \perp\!\!\!\perp D_i \;\big|\; X_i.$$

Read it as "randomization holds *within each value of $X$*." It is randomization's poorer cousin: instead of a coin guaranteeing independence unconditionally, you *assume* independence holds once you have conditioned on enough observed characteristics.

And there is the rub, the exact rub Week 2 ended on. **Conditional independence is an assumption, not a fact — and the data cannot verify it.** It holds only if the $X$'s you controlled for capture *every* characteristic that drives both selection into treatment and the outcome. If there is one unobserved confounder left — applicant motivation, soft information the loan officer saw, a hustle the dataset never recorded — that you could not measure and so could not condition on, then conditional independence fails, selection bias survives, and your "controlled" estimate is biased exactly as in Week 2's OVB ledger. Randomization needs *no* such assumption: the coin balances the unobservables too, the ones you could never name. That is the deep reason randomization is the gold standard and "controlling for X" is a bet — the same bet, now stated in the language of potential outcomes.

This is the cliff the chapter leaves you on, and the next four chapters are the climbing equipment, each a different strategy for the one mission of zeroing or sidestepping selection bias:

- **Chapter 3.2 (matching and propensity scores)** takes conditional independence seriously and asks: given that we are betting on selection-on-observables, what is the *best* way to construct comparable treated-and-control groups from the $X$'s — by matching like with like, or by collapsing the $X$'s into a single propensity-to-treat score?
- **Chapter 3.3 (inverse-probability weighting, AIPW)** attacks the same conditional-independence world from the angle of *reweighting* — up-weighting under-represented combinations so the treated and control samples look alike, and doubly-robust methods that hedge the bet.
- **Chapter 3.4 (instrumental variables, 2SLS)** abandons conditional independence entirely for the cases where unobserved confounders are unavoidable, and instead finds an external lever — the instrument — that shifts treatment without touching the outcome directly. This is where **LATE**, named in §3.1.3, finally gets its full derivation, because an instrument identifies the effect only for the compliers it moves.
- **Chapter 3.5** ties the week together and stress-tests every assumption.

Every one of these is, underneath, a machine for dealing with the selection-bias term $\mathbb{E}[Y_i(0)\mid D_i=1] - \mathbb{E}[Y_i(0)\mid D_i=0]$ — assuming it away conditional on $X$ (3.2, 3.3), or designing around it with an instrument (3.4). Keep that one term in your mind's eye as the thing every method is chasing, and the week will hang together as a single argument rather than a bag of tricks. The notation you learned here — $Y_i(1), Y_i(0), D_i, \tau_i$, ATE/ATT/LATE, selection bias, SUTVA — is the spine of all of it.

You now know exactly what a causal effect *is*, why you can never see one directly, what contaminates the easy comparison, and the one design that cleans it. The next four chapters teach you what to do when the easy design is off the table — which, in finance, is almost always.

---

## Your Turn

Open **`nb3.1`** (`notebooks/week-03/nb3.1-potential-outcomes-selection-bias.ipynb`), the potential-outcomes simulation lab. Because this is a simulation, you get to play God: you will *generate the full science table* — both $Y_i(0)$ and $Y_i(1)$ for every unit — which means you can compute the true ATE and ATT that real data hides from you, and then check whether each estimator recovers them. You will (1) **build Maya's world**: simulate applicants whose untreated approval $Y_i(0)$ depends on a "savviness" trait, let savvier people self-select into the program ($D_i$ correlated with savviness), set a known true effect, and verify the master decomposition $\Delta = \text{ATT} + \text{selection bias}$ holds *on the dollar* using the hidden counterfactual column. (2) **Watch the naive estimator lie**: confirm the difference in means overstates the truth, and dial the strength of self-selection up and down to see the selection-bias term grow and shrink. (3) **Turn on the coin**: re-assign $D_i$ by a fair random draw instead of by savviness, re-run the difference in means, and confirm the selection-bias term collapses to (sampling noise around) zero and the naive estimator now nails the ATE. (4) **Optional SUTVA-breaker**: add a spillover so that controls near treated units get partial treatment, and watch a "clean" randomized estimate go wrong anyway — interference without a fix.

**Check questions.**

1. A fintech reports that users who enabled its automatic-savings feature have average balances \$1,800 higher than users who did not. Write this claim in potential-outcomes notation as a naive difference $\mathbb{E}[Y_i\mid D_i=1]-\mathbb{E}[Y_i\mid D_i=0]$, decompose it into ATT plus selection bias, and explain in one sentence the most plausible reason the selection-bias term is *positive* here. Would a bigger user base shrink the bias? Why or why not?

2. The Fundamental Problem says $\tau_i = Y_i(1)-Y_i(0)$ is never observable for any individual $i$. (a) Explain why this is true even with a perfect measurement instrument and infinite data on person $i$. (b) Given that individual effects are unrecoverable, what *exactly* does randomization let us recover, and through which term in the master decomposition does it work? (c) In one sentence, what is the difference between the ATE and the ATT, and name a situation where a credit union would care more about the ATT.

3. Priya wants to estimate the effect of a city-wide green-building mandate on commercial property values, and proposes comparing values in mandated buildings to non-mandated ones. (a) State the SUTVA assumption her comparison requires, in both of its parts. (b) Give one concrete reason *no interference* might fail here. (c) She switches plans and finds a clean randomized pilot that assigned the mandate to a few scattered buildings — but then wants to use the result to predict the effect of a full city-wide rollout. Which SUTVA-related problem from §3.1.6 makes that extrapolation dangerous, and why?
