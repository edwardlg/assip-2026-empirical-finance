# Problem Set 1.4 — The LLN and the CLT, by Hand and by Simulation

*Covers Ch 1.4. Methods allowed: everything through Ch 1.4 — the Weak Law of Large Numbers, Chebyshev's inequality, the Central Limit Theorem, standardization $z_N=(\bar{x}-\mu)/(\sigma/\sqrt{N})$, the standard-normal table, and the fat-tail / Student's-$t$ hierarchy. You may use a normal table or the fact that $\Pr(Z>1.645)\approx 0.05$, $\Pr(|Z|>1.96)\approx 0.05$, $\Pr(Z>2.33)\approx 0.01$. No $t$-tables, no confidence intervals (those are Ch 1.5). Show your reasoning; a boxed number with no argument earns no credit.*

**Total: 100 points.** Six problems, escalating. Problems 1–3 are pencil-and-paper; 4 is conceptual; 5 asks you to design a simulation (you will run it in **nb1.4**); 6 is a finance application that ties the two laws together.

A reminder on the division of labor you should keep straight throughout, because nearly every problem here turns on it. The **Law of Large Numbers** is a statement about a *point*: the sample mean $\bar{x}$ collapses onto the single number $\mu$ as $N$ grows. The **Central Limit Theorem** is a statement about a *shape*: before that collapse is complete, the cloud of possible $\bar{x}$ values around $\mu$, once rescaled by the standard error $\sigma/\sqrt{N}$, looks like the standard normal bell. The LLN says *where* you land; the CLT says *how your misses are distributed* on the way there. Both require independence and a finite mean; the CLT additionally requires a finite variance, and Problems 4 and 6 are precisely about what happens when those requirements bend or break. When a problem asks "which law applies," it is asking you to check those assumptions, not to recite a slogan.

---

## Problem 1 — Chebyshev forces the Weak Law (14 points)

Maya is auditing a large servicer's books and wants to know the *average* monthly interest charge across a pool of student-loan accounts. She cannot afford to pull every account, so she will sample. Treat the charge on a single randomly chosen account as a draw from a population with mean $\mu = \$42$ and standard deviation $\sigma = \$30$. (The standard deviation is comparable to the mean because some accounts are nearly paid off while others carry large balances.) She will draw $N$ independent accounts and compute the sample mean $\bar{x}$. The chapter showed that the Weak Law follows from Chebyshev's inequality once you know one fact about $\operatorname{Var}(\bar{x})$; this problem makes you carry that argument out with numbers.

**(a) (4 pts)** Write down $\mathbb{E}[\bar{x}]$ and $\operatorname{Var}(\bar{x})$ in terms of $\mu$, $\sigma$, and $N$. State in one sentence which fact from Ch 1.3 you are using.

**(b) (5 pts)** Maya wants $\bar{x}$ to land within $\epsilon = \$2$ of the true $\mu$. Using **Chebyshev's inequality applied to $\bar{x}$**, write an upper bound on $\Pr(|\bar{x}-\mu|\ge 2)$ as a function of $N$. Then find the smallest $N$ for which Chebyshev *guarantees* this miss-probability is at most $0.05$.

**(c) (3 pts)** Explain, in one or two sentences, why this argument *proves* the Weak Law of Large Numbers — i.e., why $\bar{x}\xrightarrow{p}\mu$ — even though the bound you used is famously loose.

**(d) (2 pts)** Maya quadruples her sample from $N$ to $4N$. By what factor does the Chebyshev bound on her miss-probability shrink? Connect your answer to the "$\sqrt{N}$" reflex from the chapter — the rule of thumb that to halve your uncertainty you must quadruple your data.

---

## Problem 2 — Standardize a sample mean and read the normal table (16 points)

Priya works on the pricing desk of an auto insurer. She models the monthly cost of a single policy as a draw from a population with mean $\mu = \$120$ and standard deviation $\sigma = \$200$. (The standard deviation dwarfs the mean because most months cost the insurer almost nothing and a few months — accidents — cost a great deal; the population is violently right-skewed, but it has a finite variance.) The insurer holds a portfolio of $N = 400$ independent policies, and Priya cares about the *average* monthly cost across the book, $\bar{x}$, because that is what determines whether premiums cover claims.

**(a) (3 pts)** Compute the mean and the standard deviation (the *standard error*) of $\bar{x}$.

**(b) (4 pts)** Write the standardized quantity $z_N = \dfrac{\bar{x}-\mu}{\sigma/\sqrt{N}}$ and state, citing the CLT, what distribution it is approximately equal to and *why the skew of the raw policy costs does not block this*.

**(c) (6 pts)** Using the normal approximation, find the approximate probability that the portfolio's average monthly cost $\bar{x}$ exceeds $\$130$. Show the standardization step explicitly.

**(d) (3 pts)** Priya's colleague objects: "Each policy cost is wildly skewed, so the average of 400 of them must be skewed too — you can't use a normal table." Reply in two or three sentences, naming the theorem and the one assumption it actually requires, and explaining the difference between the distribution of a *single* policy and the distribution of the *average* of 400 of them.

---

## Problem 3 — How large must $N$ be for a skewed population? (18 points)

Sam runs a small simulated trading desk and is convinced his strategy has a genuine *edge* — a small positive expected profit per trade. The profit on a single trade (in dollars) is drawn from a right-skewed population with mean $\mu = \$5$ and standard deviation $\sigma = \$40$. The catch is that the noise ($\sigma=40$) is eight times the edge ($\mu=5$), so on any single trade the edge is invisible; only by averaging many independent trades can Sam hope to see it. He wants the standard error of $\bar{x}$ small enough that the true edge shows through the noise. This problem is about how many trades that takes — and about a trap that the standard-error formula alone will not warn him about.

**(a) (4 pts)** Write the standard error of $\bar{x}$ as a function of $N$. How large must $N$ be for the standard error to fall to $\$1$? To $\$0.50$?

**(b) (5 pts)** Sam wants the approximate probability that $\bar{x}$ is *negative* (a losing average) to be below $1\%$. Assuming the CLT applies, set up the standardization, use $\Pr(Z<-2.33)\approx 0.01$, and solve for the smallest $N$. Show the algebra.

**(c) (5 pts)** Now suppose the population is much more skewed than Sam assumed — one rare trade in a thousand is a $+\$5{,}000$ jackpot, the rest are small losses that average out to the same $\mu$ and $\sigma$ as before. The *formula* in part (a) still uses $\sigma$ and would return the same numbers, but explain why the answer to (b) might badly understate the $N$ Sam truly needs. Which folk rule is doing unstated work in part (b), and what does it quietly assume about the population's shape?

**(d) (4 pts)** State the general principle in one or two sentences: how does the *shape* of the population — not just its $\sigma$ — govern how large $N$ must be before the standardized mean is trustworthy as normal?

---

## Problem 4 — Devon's heavy-tails hierarchy (18 points)

Devon pulls daily returns for a basket of cryptocurrencies and knows from Section 4 of the chapter that "returns are returns" is a dangerous assumption — the tails matter, and how heavy they are decides whether his statistics mean anything. To build intuition before touching real data, he is comparing three candidate models for fat-tailed daily returns, all Student's $t$ distributions, differing only in degrees of freedom $\nu$ (smaller $\nu$ = heavier tails):

- **Model A:** $t$ with $\nu = 5$
- **Model B:** $t$ with $\nu = 2$
- **Model C:** $t$ with $\nu = 1$ (the Cauchy distribution)

For each model, the random variable is symmetric about $0$. Devon plans to draw $N$ i.i.d. returns, form $\bar{x}$, and standardize.

**(a) (6 pts)** For each of A, B, C, state whether the **mean** exists and whether the **variance** is finite. (You may use the chapter's stated facts: a $t_\nu$ has finite variance iff $\nu>2$ and a defined mean iff $\nu>1$.)

**(b) (6 pts)** For each model, say which of the two laws — **LLN** ($\bar{x}\xrightarrow{p}\mu$) and **CLT** ($z_N\xrightarrow{d} N(0,1)$) — is *guaranteed* to hold, and which fails. Give a one-sentence reason tied to the existence of the mean and the finiteness of the variance.

**(c) (3 pts)** For Model C, Devon averages one million Cauchy draws, expecting the LLN to deliver a stable answer. What is the distribution of that average, and why is it no more informative than a single draw? Name the chapter's "canonical horror story" phrase, and explain in one sentence why this is a failure of the *LLN itself* and not merely slow convergence.

**(d) (3 pts)** Devon's real crypto returns appear to have a finite but very large variance — heavier than $\nu=5$, lighter than $\nu=2$. He plans to standardize and use a normal table after $N=300$ days. Is his sample mean *eventually* consistent and asymptotically normal? Is $N=300$ likely *enough*? Answer both and justify in two sentences.

---

## Problem 5 — Design a Monte Carlo to show CLT convergence (16 points)

You will implement this in notebook **nb1.4**; here you design it on paper. The goal is to demonstrate, by simulation rather than by assertion, that the standardized sample mean of a *skewed* population converges to $N(0,1)$ as $N$ grows — the "shown not asserted" experiment that is the heart of the chapter.

A Monte Carlo experiment is just a controlled, repeatable game of chance run on a computer: you generate random data whose true parameters you *know*, compute a statistic, and repeat thousands of times to see how that statistic behaves. Because you set the population yourself, you can check the statistic against the truth. Write a clear, step-by-step experimental design — in words and pseudocode, not necessarily runnable Python — that does the following. Be precise enough that a classmate could implement it in nb1.4 without asking you a single question.

**(a) (8 pts)** Describe the full Monte Carlo loop:
- which population to draw from and its $\mu$ and $\sigma$ (use the exponential with scale $1$, so $\mu=\sigma=1$, as in the chapter);
- how to draw one sample of size $N$, compute $\bar{x}$, and standardize it to $z_N=(\bar{x}-\mu)/(\sigma/\sqrt{N})$;
- how many repetitions to collect to map the sampling distribution of $z_N$;
- what to plot, and what reference curve to overlay.

**(b) (4 pts)** Specify the sweep over $N$ (give a concrete list of values) and state, for each, what you expect the histogram to look like relative to the overlaid $N(0,1)$ curve. Name the smallest $N$ at which you expect the bell to be indistinguishable by eye, and justify with the chapter's "folk rule."

**(c) (4 pts)** State one diagnostic — a number or a visual check, not just "it looks bell-shaped" — that would let you *quantify* how close $z_N$'s distribution is to standard normal, so the convergence is measured and not merely asserted. (One sentence of justification.)

---

## Problem 6 — Aggregating many small returns (18 points)

This problem is where the two laws meet a real finance question: *why does diversification work, and exactly what does it buy you?* Sam builds an equal-weighted portfolio by combining the daily returns of $N$ assets. Let each asset's daily return $r_i$ be an i.i.d. draw with mean $\mu = 0.0004$ (about $4$ basis points per day) and standard deviation $\sigma = 0.02$ (2% daily). The portfolio's daily return is the average $\bar{r} = \frac{1}{N}\sum_{i=1}^{N} r_i$ — and "averaging many independent pieces" is precisely the setting the LLN and CLT were built for. (We assume independence for now; part (c) is where that assumption gets stress-tested.)

**(a) (4 pts)** Compute $\mathbb{E}[\bar{r}]$ and the standard deviation of $\bar{r}$ for $N = 100$. In one sentence, explain why diversification shrinks the portfolio's volatility but *not* its expected return — and connect this directly to the LLN's claim that averaging cancels noise while leaving the center fixed.

**(b) (6 pts)** Treating $\bar{r}$ as approximately normal by the CLT, find the approximate probability that the $N=100$ portfolio posts a *negative* daily return ($\bar{r}<0$). Show the standardization with $z=(\bar{r}-\mu)/(\sigma/\sqrt{N})$ and read off the normal probability.

**(c) (4 pts)** Sam now points out that real asset returns are (i) **not independent** — they move together, especially in a crash — and (ii) **fat-tailed**, like Devon's crypto. Explain how *each* of these two violations undermines the calculation in (b): one attacks the "$\sigma/\sqrt{N}$" rate, the other attacks the normal-approximation step. Name the mechanism in each case.

**(d) (4 pts)** Tie the two laws together in your own words for this portfolio: what does the **LLN** promise Sam about $\bar{r}$ as $N\to\infty$, what additional thing does the **CLT** promise about the *shape* of $\bar{r}$'s uncertainty, and which promise is the one that lets him eventually make a calibrated probability statement like the one in (b)? (Imagine the LLN alone were the whole story — explain in one sentence why that would leave Sam unable to attach a number like "42%" to anything.)

---

*Solutions: see Appendix E, `E-w1-ps1.4-solutions.md`. The simulations in Problem 5 (and the running-mean experiments referenced throughout) live in notebook **nb1.4 — CLT/LLN convergence animations**.*
