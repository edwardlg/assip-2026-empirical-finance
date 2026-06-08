# Prerequisite Self-Test

This self-test tells you where to start. It is twenty questions across calculus, probability and statistics, and light Python — the toolkit the camp assumes on Day 1. Take it closed-book, give yourself about ninety minutes, and write down a real answer for each before checking anything. The questions are fair but not soft; a few will make you think. That is the point. When you finish, grade yourself honestly against the **Solutions** section, then read the **Routing table** at the very end to decide what to do before Week 1.

Do not panic about a wrong answer here. The whole purpose of the test is to route you to the right starting point. The students you will follow through the book — Maya, Devon, Priya, Sam, and Leah — each missed something on a test like this. What mattered was what they did next.

---

## Questions

**Q1 (derivative).** Let $f(x) = 3x^4 - 5x^2 + 7x - 2$. Find $f'(x)$, and evaluate $f'(1)$.

**Q2 (chain rule).** Let $g(x) = e^{-x^2/2}$. Find $g'(x)$. At what value(s) of $x$ is $g'(x) = 0$?

**Q3 (product / quotient rule).** A firm's revenue is $R(p) = p \cdot q(p)$ where $p$ is price and quantity sold is $q(p) = 100 - 4p$. Find $\dfrac{dR}{dp}$ and the price $p$ that maximizes revenue.

**Q4 (partial derivatives).** Let $h(x, y) = x^2 y + 3xy^3$. Find $\dfrac{\partial h}{\partial x}$ and $\dfrac{\partial h}{\partial y}$.

**Q5 (optimization / first-order condition).** Sam fits a line through one number: he wants the constant $c$ that minimizes the sum of squared errors $S(c) = \sum_{i=1}^{n}(y_i - c)^2$ for a fixed dataset $y_1, \dots, y_n$. Set up the first-order condition and solve for the minimizing $c$. What familiar quantity is it?

**Q6 (definite integral).** Evaluate $\displaystyle\int_{0}^{2} (3x^2 + 2x)\, dx$.

**Q7 (limit).** Evaluate $\displaystyle\lim_{x \to 0} \frac{\sin(3x)}{x}$. Briefly say why.

**Q8 (expectation and variance).** A single roll of a fair six-sided die yields $X \in \{1,2,3,4,5,6\}$, each with probability $1/6$. Compute $\mathbb{E}[X]$ and $\operatorname{Var}(X)$.

**Q9 (linearity / scaling of variance).** Priya has a random variable $X$ with $\mathbb{E}[X] = 4$ and $\operatorname{Var}(X) = 9$. Let $Y = 2X - 5$. Find $\mathbb{E}[Y]$ and $\operatorname{Var}(Y)$.

**Q10 (conditional probability / Bayes).** A loan-fraud screen flags 5% of all applications. Among truly fraudulent applications it flags 90%; among legitimate ones it flags 4%. Suppose 2% of applications are truly fraudulent. Given that an application is flagged, what is the probability it is actually fraudulent? (Round to two decimals.)

**Q11 (law of total expectation).** Leah models a startup's payoff. With probability 0.3 it is a "hit" with expected payoff \$10M; with probability 0.7 it is a "miss" with expected payoff \$1M. What is the unconditional expected payoff?

**Q12 (binomial).** Devon flags that a certain coin lands heads with probability 0.6. He flips it 10 times. What is the probability of exactly 7 heads? Give the formula and a numerical value (two decimals).

**Q13 (normal distribution).** Daily returns on a stock are approximately $\mathcal{N}(\mu = 0.0005,\ \sigma = 0.02)$. Roughly what fraction of days have a return below $-0.0395$? (Use the 68–95–99.7 rule; no calculator needed.)

**Q14 (t-test interpretation).** A regression reports a coefficient $\hat{\beta}_1 = 0.42$ with standard error $0.15$. State the approximate $t$-statistic, and explain in one or two sentences what it tells you about the null hypothesis $\beta_1 = 0$ at the usual 5% level.

**Q15 (correlation vs. causation).** Across cities, ice-cream sales and drowning deaths are strongly positively correlated. Does ice cream cause drowning? Name the most likely reason for the correlation and the term for the variable responsible.

**Q16 (reading a confidence interval).** A study reports that a job-training program raised earnings by \$1,200 with a 95% confidence interval of $[-200,\ 2{,}600]$. Maya says "the program had no effect." Is her statement supported? Explain what the interval does and does not let you conclude.

**Q17 (sampling distribution).** You draw a sample of $n = 100$ from a population with mean $\mu$ and standard deviation $\sigma = 20$, and compute the sample mean $\bar{X}$. What is the standard deviation of $\bar{X}$ (the standard error), and what happens to it if you increase $n$ to $400$?

**Q18 (Python output — pandas/numpy).** What does this print?

```python
import numpy as np
a = np.array([1, 2, 3, 4])
print(a[a > 2].sum())
```

**Q19 (vectorized vs. loop).** Two snippets compute the same thing on a NumPy array `x` of length 1,000,000. Which is preferred in this book, and why?

```python
# A
total = 0
for v in x:
    total += v ** 2

# B
total = (x ** 2).sum()
```

**Q20 (groupby interpretation).** Given a DataFrame `df` with columns `sector` and `ret` (a return), what does this produce, in words?

```python
df.groupby("sector")["ret"].mean()
```

---

## Solutions

**Q1.** Differentiate term by term using the power rule $\frac{d}{dx}x^n = nx^{n-1}$:
$$f'(x) = 12x^3 - 10x + 7.$$
At $x = 1$: $f'(1) = 12 - 10 + 7 = \boxed{9}$.

**Q2.** Write $g(x) = e^{u}$ with $u = -x^2/2$, so $u' = -x$. The chain rule gives $g'(x) = e^{u}\cdot u' = -x\,e^{-x^2/2}$. This equals zero only when the factor $x = 0$ (the exponential is never zero), so $g'(x) = 0$ at $\boxed{x = 0}$. (This is the standard normal density up to a constant; its slope is zero at the peak.)

**Q3.** $R(p) = p(100 - 4p) = 100p - 4p^2$, so $\frac{dR}{dp} = 100 - 8p$. Setting this to zero: $p = \boxed{12.5}$. The second derivative is $-8 < 0$, confirming a maximum. (You could also use the product rule on $p\cdot q(p)$ directly: $R' = q(p) + p\,q'(p) = (100 - 4p) + p(-4) = 100 - 8p$, same answer.)

**Q4.** Treat the other variable as a constant.
$$\frac{\partial h}{\partial x} = 2xy + 3y^3, \qquad \frac{\partial h}{\partial y} = x^2 + 9xy^2.$$

**Q5.** Differentiate $S(c) = \sum_i (y_i - c)^2$ with respect to $c$ and set to zero:
$$S'(c) = \sum_i 2(y_i - c)(-1) = -2\sum_i (y_i - c) = 0 \;\Rightarrow\; \sum_i (y_i - c) = 0 \;\Rightarrow\; c = \frac{1}{n}\sum_i y_i.$$
The second derivative $S''(c) = 2n > 0$ confirms a minimum. The minimizing $c$ is the **sample mean** $\bar{y}$ — the first and simplest least-squares estimate you will meet, and the reason the mean shows up everywhere in regression.

**Q6.** Antiderivative of $3x^2 + 2x$ is $x^3 + x^2$. Evaluate from $0$ to $2$:
$$(2^3 + 2^2) - (0 + 0) = 8 + 4 = \boxed{12}.$$

**Q7.** $\displaystyle\lim_{x\to 0}\frac{\sin(3x)}{x} = \boxed{3}$. Reason: $\frac{\sin(3x)}{x} = 3\cdot\frac{\sin(3x)}{3x}$, and $\frac{\sin(u)}{u}\to 1$ as $u\to 0$. (Equivalently, by L'Hôpital, the ratio of derivatives is $\frac{3\cos(3x)}{1}\to 3$.)

**Q8.** $\mathbb{E}[X] = \frac{1}{6}(1+2+3+4+5+6) = \frac{21}{6} = 3.5$. For the variance, $\mathbb{E}[X^2] = \frac{1}{6}(1+4+9+16+25+36) = \frac{91}{6} \approx 15.1667$, so
$$\operatorname{Var}(X) = \mathbb{E}[X^2] - (\mathbb{E}[X])^2 = \frac{91}{6} - 3.5^2 = 15.1667 - 12.25 = \boxed{\tfrac{35}{12} \approx 2.9167}.$$

**Q9.** Expectation is linear: $\mathbb{E}[Y] = 2\mathbb{E}[X] - 5 = 2(4) - 5 = \boxed{3}$. Variance ignores additive constants and scales by the square of the multiplier: $\operatorname{Var}(Y) = 2^2\operatorname{Var}(X) = 4 \cdot 9 = \boxed{36}$. (The $-5$ shifts the whole distribution but does not change its spread.)

**Q10.** Let $F$ = fraudulent, $+$ = flagged. We want $P(F \mid +)$. Bayes:
$$P(F\mid +) = \frac{P(+\mid F)P(F)}{P(+\mid F)P(F) + P(+\mid \text{not }F)P(\text{not }F)} = \frac{0.90 \cdot 0.02}{0.90\cdot 0.02 + 0.04\cdot 0.98} = \frac{0.018}{0.018 + 0.0392} = \frac{0.018}{0.0572} \approx \boxed{0.31}.$$
Note the lesson: even with a screen that catches 90% of fraud, a flagged application is fraudulent only about 31% of the time, because fraud is rare to begin with. (The "flags 5% of all applications" figure in the prompt is a deliberate distractor — and a useful sanity check. The two conditional rates actually imply an overall flag rate of $P(+) = 0.90\cdot0.02 + 0.04\cdot0.98 = 0.0572$, i.e. about 5.7%, not exactly 5%. A careful reader notices the stated marginal is only approximate; either way it is not used in the Bayes calculation, which needs only the conditional rates and the base rate.)

**Q11.** Law of total expectation: $\mathbb{E}[\text{payoff}] = P(\text{hit})\,\mathbb{E}[\text{payoff}\mid\text{hit}] + P(\text{miss})\,\mathbb{E}[\text{payoff}\mid\text{miss}] = 0.3(10) + 0.7(1) = 3 + 0.7 = \boxed{\$3.7\text{M}}.$

**Q12.** Binomial with $n = 10$, $p = 0.6$, $k = 7$:
$$P(X = 7) = \binom{10}{7}(0.6)^7(0.4)^3 = 120 \cdot 0.0279936 \cdot 0.064 \approx \boxed{0.21}.$$

**Q13.** The threshold $-0.0395$ is $\mu - 2\sigma = 0.0005 - 2(0.02) = 0.0005 - 0.04 = -0.0395$, i.e., two standard deviations below the mean. By the 68–95–99.7 rule, about 95% of mass lies within $\pm 2\sigma$, leaving 5% in the two tails, so about $2.5\%$ lies below $-2\sigma$. Answer: **about 2.5% of days.**

**Q14.** The $t$-statistic is $t = \hat\beta_1 / \text{SE} = 0.42 / 0.15 = 2.8$. Since $|t| = 2.8$ exceeds the usual critical value of about $1.96$, we **reject the null** $\beta_1 = 0$ at the 5% level: the estimate is statistically distinguishable from zero. (It says nothing, by itself, about whether the effect is *large* or *causal* — only that it is unlikely to be zero given the data and the model.)

**Q15.** No — ice cream does not cause drowning. Both rise with **hot weather / summer temperature**, which drives more ice-cream buying *and* more swimming (hence more drownings). The temperature variable is a **confounder** (a common cause of both, also called a lurking or omitted variable). This is the central problem the camp's middle weeks are built to solve.

**Q16.** Maya's statement is **not supported as stated.** The point estimate is a \$1,200 *increase*, and the 95% confidence interval $[-200, 2600]$ means the data are consistent with effects ranging from a small negative to a large positive. Because the interval includes zero, we *cannot reject* the hypothesis of no effect at the 5% level — but "cannot reject zero" is not the same as "the effect is zero." The interval is too wide to distinguish "no effect" from "a substantial \$2,000 effect"; the honest conclusion is that the study is **inconclusive / underpowered**, not that the program did nothing.

**Q17.** The standard error of the sample mean is $\sigma/\sqrt{n} = 20/\sqrt{100} = \boxed{2}$. Increasing $n$ to $400$ gives $20/\sqrt{400} = 1$, so the standard error **halves**. Note it falls with the square root of $n$: to cut it in half you need *four times* the data. This is the engine behind why bigger samples give more precise estimates.

**Q18.** The boolean mask `a > 2` selects the elements `3` and `4`; their sum is `3 + 4 = `**`7`**.

**Q19.** **B (the vectorized version) is preferred.** Both compute $\sum x_i^2$, but B pushes the loop into NumPy's compiled C implementation, so it is far faster on a million elements and is more readable. The Python-level `for` loop in A is slow and error-prone. Vectorize whenever you can; we treat explicit elementwise loops over large arrays as a code smell in this book.

**Q20.** It splits the rows of `df` into groups by their `sector` value, then computes the **mean return (`ret`) within each sector**, returning a Series indexed by sector. In words: the average return for each sector.

---

## Routing table

Count your misses by cluster and follow the routing. "Missed" means you got it wrong or had to guess.

| If you missed… | What it signals | Do this before Week 1 |
|----------------|-----------------|-----------------------|
| **Q1–Q7 (any 2 or more)** | Calculus rust — derivatives, chain/product rule, partials, optimization, integrals, limits. Week 2's inference and Week 3's estimators lean on these constantly. | Work through **Appendix A: Math Toolkit** before Week 1. Maya routed here and it paid off. |
| **Q8–Q17 (any 3 or more)** | Probability/statistics gaps — expectation/variance, Bayes, total expectation, binomial/normal, $t$-tests, confidence intervals, sampling distributions, confounding. This is the conceptual spine of the whole camp. | Review the probability and inference sections of **Appendix A**, with special attention to confounding (Q15) and confidence-interval interpretation (Q16) — these recur in every causal-inference week. |
| **Q18–Q20 (any 2 or more)** | Python/`pandas`/NumPy fundamentals — boolean indexing, vectorization, `groupby`. You will write code from Day 1. | Set up your environment and work the fundamentals in **Appendix B: Python & LaTeX Setup** first. Devon skipped this and hit a wall — do not be Devon. |
| **Q15 and Q16 specifically** | Correlation-vs-causation and confidence-interval reading. Even strong students miss these; they are *the* conceptual hinges of empirical work. | You can start Week 1 on schedule, but flag these for your mentor in your first lab session — they are exactly what Weeks 3–6 are about. |
| **Two or more clusters** | Broad gaps across math, stats, and code. | Budget extra time on **Appendices A and B** before Week 1, and tell your mentor where you are starting from. There is no penalty for arriving honest about it; there is real cost to bluffing past it. |
| **0–3 missed total, spread out** | You are ready. | Skim **Appendix A** for the notation conventions and start Week 1. Keep the appendices handy as reference. |
