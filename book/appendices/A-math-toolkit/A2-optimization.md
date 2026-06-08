# A.2 — Optimization (just enough)

Almost every estimator in this book is the answer to an optimization problem. Ordinary least squares picks the coefficients that make the residuals as short as possible; maximum likelihood (Week 3) picks the parameters that make the data look as probable as possible; Maya's portfolio in Chapter 1.2 picked the weights that make risk as small as possible. "Estimation" and "minimize-or-maximize-something" are, more often than not, the same sentence. This appendix gives you the optimization toolkit those problems need, and no more: how to find the top of a hill or the bottom of a valley when there are several variables at once, how to be sure you have found a minimum rather than a maximum or a saddle, and how to optimize when you are not free to move anywhere — when a constraint, like "the portfolio weights must sum to one," fences you in.

You already own the one-variable version of all of this from AP Calculus. To find where a smooth function $f(x)$ is largest or smallest, you set its derivative to zero, solve for the candidate points, and check the second derivative to see whether each candidate is a peak ($f'' < 0$) or a trough ($f'' > 0$). Everything in this appendix is that same idea, promoted to handle a vector of variables instead of a single $x$. The derivative becomes a *gradient*, the second derivative becomes a *Hessian matrix*, "positive second derivative" becomes "positive definite Hessian" (the property from Appendix A.1 §6), and constraints get handled by a clever bookkeeping device called a Lagrange multiplier. We build each piece on a concrete number, then turn the same crank on the two problems that actually matter for the book: Maya's minimum-variance portfolio and the derivation of the OLS normal equations as an optimization.

## 1. Partial derivatives and the gradient: the slope in every direction at once

**The result, in one sentence.** When a function depends on several variables, its derivative is not one number but a vector — the gradient — whose entries are the partial derivatives, each measuring the slope as you nudge one variable while holding the rest fixed.

Begin with a function of two variables, because two is the smallest number that is genuinely multivariable and you can still picture it. Maya's portfolio risk, as a function of the weight $w$, was a parabola — one variable, one curve. But a function of two variables, say $f(x, y)$, is a *surface*: a landscape of hills and valleys floating above the $xy$-plane, where the height at each point $(x, y)$ is $f(x, y)$. To talk about slopes on a landscape, you have to say *which direction* you are walking, because the ground tilts differently depending on whether you head east or north.

The two most natural directions are along the axes, and the slopes in those directions are the **partial derivatives**. The partial derivative with respect to $x$, written $\partial f / \partial x$, is the ordinary derivative you get by treating $y$ as a frozen constant and differentiating in $x$ alone — the slope you feel walking due east. Likewise $\partial f / \partial y$ freezes $x$ and differentiates in $y$. Take a concrete function we will reuse all section:

$$
f(x, y) = x^2 + xy + y^2 - 3x - 6y.
$$

To get $\partial f / \partial x$, treat $y$ as a constant: $x^2$ differentiates to $2x$, the term $xy$ has $y$ as a constant coefficient so it differentiates to $y$, the $y^2$ term has no $x$ so it dies, $-3x$ gives $-3$, and $-6y$ has no $x$ so it dies. Likewise for $y$, freezing $x$:

$$
\frac{\partial f}{\partial x} = 2x + y - 3, \qquad \frac{\partial f}{\partial y} = x + 2y - 6.
$$

Stack these two slopes into a column vector and you have the **gradient**, written $\nabla f$ (read "grad f") or $\partial f / \partial \mathbf{b}$ when the variables are bundled into a vector $\mathbf{b}$:

$$
\nabla f(x, y) = \begin{pmatrix} \partial f / \partial x \\ \partial f / \partial y \end{pmatrix} = \begin{pmatrix} 2x + y - 3 \\ x + 2y - 6 \end{pmatrix}.
$$

The gradient is the multivariable derivative, and it carries one more piece of meaning than its one-variable cousin: it is a *vector*, and that vector points in the direction of steepest ascent — the compass bearing of the steepest uphill climb from wherever you are standing — with length equal to how steep that climb is. This is exactly the object Chapter 2.1 §3 differentiated when it wrote $\partial\,\text{SSR}/\partial\mathbf{b}$ and set it to the zero vector. The matrix-calculus shortcuts that chapter quoted — $\partial(\mathbf{a}'\mathbf{b})/\partial\mathbf{b} = \mathbf{a}$ and $\partial(\mathbf{b}'\mathbf{A}\mathbf{b})/\partial\mathbf{b} = 2\mathbf{A}\mathbf{b}$ for symmetric $\mathbf{A}$ — are nothing but the gradient computed for the linear and quadratic building blocks, the direct analogues of the scalar rules $\tfrac{d}{db}(ab) = a$ and $\tfrac{d}{db}(ab^2) = 2ab$. When we derive OLS in §5, those two facts are the entire engine.

## 2. First-order conditions: flat ground marks a candidate

**The result, in one sentence.** At any peak or valley of a smooth function the ground is level in every direction, so the gradient is the zero vector — and solving $\nabla f = \mathbf{0}$ is how you find every candidate for a maximum or minimum.

In one variable, an interior maximum or minimum can only occur where $f'(x) = 0$: at the very top of a hill the tangent line is horizontal, and likewise at the very bottom of a valley. The multivariable statement is the same, said in every direction at once. At the bottom of a bowl-shaped surface, no matter which compass bearing you face, the ground is momentarily level — if it tilted any direction you could step downhill and you were not at the bottom after all. "Level in every direction" means every partial derivative is zero, which means the whole gradient vanishes. This is the **first-order condition (FOC)**, sometimes called the stationarity condition:

$$
\nabla f(\mathbf{b}^\star) = \mathbf{0}.
$$

A point where the gradient is zero is called a **critical point** or **stationary point**. Solving the FOC is the first move in every optimization problem in the book.

Run it on our example. Set both partials to zero:

$$
2x + y - 3 = 0, \qquad x + 2y - 6 = 0.
$$

This is a small linear system — two equations, two unknowns — and you can write it in matrix form (Appendix A.1) as $\begin{pmatrix} 2 & 1 \\ 1 & 2\end{pmatrix}\begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} 3 \\ 6 \end{pmatrix}$. From the first equation $y = 3 - 2x$; substitute into the second: $x + 2(3 - 2x) - 6 = 0$, i.e. $x + 6 - 4x - 6 = -3x = 0$, so $x = 0$ and then $y = 3$. The one critical point is $(x, y) = (0, 3)$, where the function takes the value $f(0,3) = 0 + 0 + 9 - 0 - 18 = -9$.

But notice what the FOC has *not* told us. Flat ground also occurs at the top of a hill, and at a **saddle point** — a mountain pass that curves up in one direction and down in another, level at the center but neither a max nor a min. The gradient is zero at all three. Setting the gradient to zero finds candidates; it does not certify what kind of candidate you have. That is the job of the second-order condition, and it is exactly the loose end Chapter 2.1 §3 flagged when it said "we have only verified that the gradient vanishes here, which marks a flat point — is it a minimum?"

## 3. Second-order conditions: the Hessian decides max, min, or saddle

**The result, in one sentence.** Whether a critical point is a minimum, a maximum, or a saddle is decided by the matrix of second partial derivatives — the Hessian — through its definiteness: positive definite means a minimum, the multivariable echo of "$f'' > 0$ at the bottom of a parabola."

In one variable, the second derivative reads the *curvature*: $f'' > 0$ at a critical point means the curve bends upward like a cup (a minimum), $f'' < 0$ means it bends down like a cap (a maximum). With several variables there are several second derivatives — you can differentiate $\partial f/\partial x$ again in $x$ or in $y$, and similarly for $\partial f /\partial y$ — and they get organized into a square, symmetric matrix called the **Hessian**:

$$
\mathbf{H}_f = \begin{pmatrix}
\dfrac{\partial^2 f}{\partial x^2} & \dfrac{\partial^2 f}{\partial x\,\partial y} \\[2ex]
\dfrac{\partial^2 f}{\partial y\,\partial x} & \dfrac{\partial^2 f}{\partial y^2}
\end{pmatrix}.
$$

(It is symmetric because the order of differentiation does not matter for the smooth functions we deal with — $\partial^2 f/\partial x\,\partial y = \partial^2 f/\partial y\,\partial x$ — so the Hessian is exactly the kind of symmetric matrix Appendix A.1 §6 classified by definiteness. Do not confuse this Hessian $\mathbf{H}_f$ with the regression hat matrix $\mathbf{H}$ of Chapter 2.1; same letter, unrelated objects.) For our function, differentiating the gradient entries again: $\partial^2 f/\partial x^2 = 2$, $\partial^2 f/\partial y^2 = 2$, and the cross-partials $\partial^2 f/\partial x\,\partial y = 1$. So everywhere,

$$
\mathbf{H}_f = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}.
$$

The **second-order condition (SOC)** reads the curvature in every direction at once, and "curvature in direction $\mathbf{v}$" is exactly the quadratic form $\mathbf{v}'\mathbf{H}_f\mathbf{v}$ from Appendix A.1. If the Hessian is **positive definite** — $\mathbf{v}'\mathbf{H}_f\mathbf{v} > 0$ for every nonzero $\mathbf{v}$ — the surface curves upward in *every* direction from the critical point, so it is a strict **local minimum**. If the Hessian is **negative definite**, it curves down everywhere, a **local maximum**. If the curvature is positive in some directions and negative in others — an **indefinite** Hessian — the critical point is a **saddle**. The cleanest way to check definiteness is the eigenvalue test from Appendix A.1 §7: all eigenvalues positive means positive definite. For our Hessian $\begin{pmatrix} 2 & 1 \\ 1 & 2\end{pmatrix}$, the eigenvalues are $1$ and $3$, both positive, so the matrix is positive definite and the critical point $(0, 3)$ is a genuine minimum, with $f = -9$ being the lowest value the function attains.

One more property earns the SOC its keep beyond just labeling critical points. When a function's Hessian is positive (semi)definite *everywhere*, not merely at the critical point, the function is **convex** — it is one single bowl with no false bottoms, no separate local minima to get trapped in. For a convex function any critical point is automatically the *global* minimum, and there is only one place to find. This is a big deal: it is the difference between an optimization you can trust a formula to solve in one shot and one where you have to worry about which valley you landed in. The SSR objective of OLS is convex (its Hessian $2\mathbf{X}'\mathbf{X}$ is PSD everywhere), which is exactly why the single solution of the normal equations is *the* answer, full stop — a point we cash out in §5.

```python
import numpy as np
# f(x,y) = x^2 + xy + y^2 - 3x - 6y
# FOC: solve gradient = 0  ->  [[2,1],[1,2]] [x,y] = [3,6]
A = np.array([[2.0, 1.0], [1.0, 2.0]])     # this is also the Hessian here
b = np.array([3.0, 6.0])
crit = np.linalg.solve(A, b)
print("critical point:", crit)             # [0. 3.]
print("Hessian eigenvalues:", np.linalg.eigvalsh(A))  # [1. 3.] -> PD -> minimum
```

## 4. Constrained optimization and Lagrange multipliers

**The result, in one sentence.** To optimize a function while obeying a constraint, you build one combined object — the Lagrangian — that bolts the constraint onto the objective with a new unknown, the Lagrange multiplier, and then apply the ordinary first-order condition to *that*; the trick converts a fenced-in problem into a free one.

So far we have been free to roam the whole landscape. Real problems usually come with a fence. Maya cannot choose portfolio weights that wander anywhere; her weights must sum to one, because she is investing all of her money and no more — $w_1 + w_2 = 1$. The question "what is the lowest-risk portfolio?" is therefore *constrained*: minimize risk, but only over the line of weight vectors that add to one. You cannot just set the gradient of risk to zero, because the unconstrained minimum (hold nothing, risk zero) violates the budget.

Here is the geometric insight that makes the method work, and it is worth seeing before the recipe. Picture the objective's contour lines — the curves of equal risk, like elevation lines on a topographic map — and overlay the constraint as a single line you are forced to stay on. As you slide along the constraint line, you cross contours, moving to lower and lower risk, until you reach the point where the constraint line just *grazes* a contour, touching it tangentially. Push past that point and risk rises again. At that grazing point the constraint line and the contour are tangent, which means their gradients point in the same direction (gradients are always perpendicular to contours). "The objective's gradient is parallel to the constraint's gradient" is the optimality condition, and the proportionality constant between them is the **Lagrange multiplier** $\lambda$:

$$
\nabla f = \lambda \,\nabla g,
$$

where the constraint is written as $g(\mathbf{x}) = c$.

The bookkeeping device that automates this is the **Lagrangian**. To minimize $f(\mathbf{x})$ subject to $g(\mathbf{x}) = c$, form

$$
\mathcal{L}(\mathbf{x}, \lambda) = f(\mathbf{x}) - \lambda\,\big(g(\mathbf{x}) - c\big),
$$

treating $\lambda$ as one more variable, and then take the ordinary first-order condition — set *all* the partial derivatives of $\mathcal{L}$, including the one with respect to $\lambda$, to zero. The partials in $\mathbf{x}$ reproduce $\nabla f = \lambda\nabla g$, and the partial in $\lambda$ reproduces the constraint $g(\mathbf{x}) = c$ itself (which is why the trick "remembers" the fence). A constrained problem in $\mathbf{x}$ becomes an unconstrained problem in $(\mathbf{x}, \lambda)$, solvable by the §2 machinery.

**A first number, kept tiny.** Minimize $f(x, y) = x^2 + y^2$ subject to $x + y = 10$. The Lagrangian is $\mathcal{L} = x^2 + y^2 - \lambda(x + y - 10)$. The three FOCs are $\partial\mathcal{L}/\partial x = 2x - \lambda = 0$, $\partial\mathcal{L}/\partial y = 2y - \lambda = 0$, and $\partial\mathcal{L}/\partial\lambda = -(x + y - 10) = 0$. The first two give $2x = \lambda = 2y$, so $x = y$; the third forces $x + y = 10$; together $x = y = 5$, with $\lambda = 10$ and minimum value $25 + 25 = 50$. By symmetry that is obviously right, which is the point of starting here — the method reproduces the answer you can already see.

**Maya's minimum-variance portfolio.** Now the example the book actually cares about, tying straight back to Chapter 1.2. Maya holds weights $\mathbf{w} = (w_1, w_2)'$ in her two assets, with covariance matrix (Scenario B, uncorrelated)

$$
\mathbf{\Sigma} = \begin{pmatrix} 0.04 & 0 \\ 0 & 0.01 \end{pmatrix}.
$$

Portfolio variance is the quadratic form $\mathbf{w}'\mathbf{\Sigma}\mathbf{w}$ (Chapter 1.2 §5), and the budget constraint is $\mathbf{w}'\mathbf{1} = 1$, where $\mathbf{1} = (1,1)'$. She wants the weights that minimize variance subject to being fully invested:

$$
\min_{\mathbf{w}} \ \mathbf{w}'\mathbf{\Sigma}\mathbf{w} \quad \text{subject to} \quad \mathbf{w}'\mathbf{1} = 1.
$$

Build the Lagrangian, $\mathcal{L} = \mathbf{w}'\mathbf{\Sigma}\mathbf{w} - \lambda(\mathbf{w}'\mathbf{1} - 1)$. The gradient in $\mathbf{w}$ uses the quadratic-form rule from §1 (here $\mathbf{\Sigma}$ is symmetric, so $\partial(\mathbf{w}'\mathbf{\Sigma}\mathbf{w})/\partial\mathbf{w} = 2\mathbf{\Sigma}\mathbf{w}$) and the linear rule ($\partial(\mathbf{w}'\mathbf{1})/\partial\mathbf{w} = \mathbf{1}$):

$$
\frac{\partial\mathcal{L}}{\partial\mathbf{w}} = 2\mathbf{\Sigma}\mathbf{w} - \lambda\mathbf{1} = \mathbf{0}
\quad\Longrightarrow\quad
\mathbf{w} = \frac{\lambda}{2}\,\mathbf{\Sigma}^{-1}\mathbf{1}.
$$

The multiplier $\lambda$ is just a scale knob; the constraint $\mathbf{w}'\mathbf{1} = 1$ sets it. Substituting and solving for the scale gives the clean closed form for the minimum-variance weights,

$$
\mathbf{w}^\star = \frac{\mathbf{\Sigma}^{-1}\mathbf{1}}{\mathbf{1}'\mathbf{\Sigma}^{-1}\mathbf{1}}.
$$

Now the arithmetic, by hand. The inverse of the diagonal $\mathbf{\Sigma}$ reciprocates the diagonal (Appendix A.1 §4): $\mathbf{\Sigma}^{-1} = \operatorname{diag}(25, 100)$, since $1/0.04 = 25$ and $1/0.01 = 100$. Then $\mathbf{\Sigma}^{-1}\mathbf{1} = (25, 100)'$, and the normalizer is $\mathbf{1}'\mathbf{\Sigma}^{-1}\mathbf{1} = 25 + 100 = 125$. So

$$
\mathbf{w}^\star = \frac{1}{125}\begin{pmatrix} 25 \\ 100 \end{pmatrix} = \begin{pmatrix} 0.2 \\ 0.8 \end{pmatrix}.
$$

Maya should put 20% in the riskier asset 1 and 80% in the safer asset 2 — *exactly* the $w^\star = 0.2$ that Chapter 1.2 §3 found by minimizing the one-variable parabola directly. The minimum variance is $\mathbf{w}^{\star\prime}\mathbf{\Sigma}\mathbf{w}^\star = (0.2)^2(0.04) + (0.8)^2(0.01) = 0.0016 + 0.0064 = 0.008$, matching the chapter's $0.008$ on the nose, and the multiplier comes out to $\lambda = 2 \times 0.008 = 0.016$ — twice the minimized variance, a recurring fingerprint that the multiplier measures how hard the constraint is pushing back. The Lagrange machine reproduced Maya's answer and, unlike the one-variable substitution, it scales without change to a hundred assets, where you cannot eliminate variables by hand. That generality is why portfolio optimization, and a great deal of constrained estimation later in the book, is always set up this way.

```python
import numpy as np
Sigma = np.array([[0.04, 0.0], [0.0, 0.01]])
one = np.array([1.0, 1.0])
Sinv = np.linalg.inv(Sigma)
w = (Sinv @ one) / (one @ Sinv @ one)
print("min-variance weights:", w)            # [0.2 0.8]
print("min variance:", w @ Sigma @ w)        # 0.008  (matches Ch 1.2)
```

## 5. The normal equations as an optimization

**The result, in one sentence.** Ordinary least squares is the optimization problem "minimize the sum of squared residuals," and turning the first-order-condition crank on it produces the normal equations $\mathbf{X}'\mathbf{X}\hat{\boldsymbol\beta} = \mathbf{X}'\mathbf{y}$, with the second-order condition certifying that the answer is a genuine, unique minimum.

Now we assemble the whole machine on the problem this book is built around, the derivation Chapter 2.1 §3 walked through — but here we narrate it explicitly as an optimization, naming the gradient, the FOC, and the Hessian SOC as the §1–§3 tools they are. OLS chooses the coefficient vector $\mathbf{b}$ to minimize the sum of squared residuals, the squared length of the gap between the outcomes and the fitted values:

$$
\hat{\boldsymbol\beta} = \arg\min_{\mathbf{b}} \ \text{SSR}(\mathbf{b}), \qquad \text{SSR}(\mathbf{b}) = (\mathbf{y} - \mathbf{X}\mathbf{b})'(\mathbf{y} - \mathbf{X}\mathbf{b}).
$$

This is an unconstrained minimization over the $K$ entries of $\mathbf{b}$, so the recipe is exactly §2 followed by §3: take the gradient, set it to zero, check the Hessian. First expand SSR by multiplying out, using the transpose-reversal rule $(\mathbf{A}\mathbf{B})' = \mathbf{B}'\mathbf{A}'$ from Appendix A.1 §3:

$$
\text{SSR}(\mathbf{b}) = \mathbf{y}'\mathbf{y} - \mathbf{y}'\mathbf{X}\mathbf{b} - \mathbf{b}'\mathbf{X}'\mathbf{y} + \mathbf{b}'\mathbf{X}'\mathbf{X}\mathbf{b}.
$$

The two middle terms are each a single number (shape $1\times 1$), and a number equals its own transpose, so $\mathbf{y}'\mathbf{X}\mathbf{b} = \mathbf{b}'\mathbf{X}'\mathbf{y}$ and they merge into one term of $-2\mathbf{b}'\mathbf{X}'\mathbf{y}$:

$$
\text{SSR}(\mathbf{b}) = \mathbf{y}'\mathbf{y} - 2\,\mathbf{b}'\mathbf{X}'\mathbf{y} + \mathbf{b}'\mathbf{X}'\mathbf{X}\mathbf{b}.
$$

This is precisely the shape of function whose gradient we know cold from §1. The constant $\mathbf{y}'\mathbf{y}$ contributes nothing. The linear term $-2\mathbf{b}'(\mathbf{X}'\mathbf{y})$ has the form $\mathbf{a}'\mathbf{b}$ with $\mathbf{a} = -2\mathbf{X}'\mathbf{y}$, so its gradient is $-2\mathbf{X}'\mathbf{y}$. The quadratic term $\mathbf{b}'(\mathbf{X}'\mathbf{X})\mathbf{b}$ has the form $\mathbf{b}'\mathbf{A}\mathbf{b}$ with $\mathbf{A} = \mathbf{X}'\mathbf{X}$ symmetric (Appendix A.1 §3), so its gradient is $2\mathbf{X}'\mathbf{X}\mathbf{b}$. Adding the pieces, the **gradient** of SSR is

$$
\nabla\,\text{SSR}(\mathbf{b}) = -2\mathbf{X}'\mathbf{y} + 2\mathbf{X}'\mathbf{X}\mathbf{b}.
$$

Now the **first-order condition**: set the gradient to the zero vector and call the solution $\hat{\boldsymbol\beta}$. The $2$'s cancel, and rearranging gives the **normal equations**:

$$
-2\mathbf{X}'\mathbf{y} + 2\mathbf{X}'\mathbf{X}\hat{\boldsymbol\beta} = \mathbf{0}
\quad\Longrightarrow\quad
\boxed{\ \mathbf{X}'\mathbf{X}\,\hat{\boldsymbol\beta} = \mathbf{X}'\mathbf{y}\ }.
$$

These are $K$ linear equations in the $K$ unknown coefficients. When $\mathbf{X}'\mathbf{X}$ is invertible — full column rank, no perfect collinearity (Appendix A.1 §5) — you multiply on the left by its inverse and recover the formula on the cover of every econometrics course, $\hat{\boldsymbol\beta} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$.

The FOC alone, exactly as §2 warned, only certifies flat ground. Is it a minimum? Take the **Hessian** — differentiate the gradient $-2\mathbf{X}'\mathbf{y} + 2\mathbf{X}'\mathbf{X}\mathbf{b}$ once more in $\mathbf{b}$, where only the second term depends on $\mathbf{b}$ and contributes its coefficient matrix:

$$
\mathbf{H}_{\text{SSR}} = \frac{\partial^2\,\text{SSR}}{\partial\mathbf{b}\,\partial\mathbf{b}'} = 2\mathbf{X}'\mathbf{X}.
$$

The **second-order condition** now does its work. We proved in Appendix A.1 §6 that $\mathbf{X}'\mathbf{X}$ is positive semidefinite — for any $\mathbf{v}$, $\mathbf{v}'\mathbf{X}'\mathbf{X}\mathbf{v} = \lVert\mathbf{X}\mathbf{v}\rVert^2 \ge 0$, a squared length — and positive *definite* when $\mathbf{X}$ has full column rank. A positive-definite Hessian means SSR curves upward in every direction: the critical point is a strict minimum, and because the Hessian is positive definite *everywhere* (it does not depend on $\mathbf{b}$ at all), SSR is a convex bowl with a single global bottom and no false minima to fear. The §3 convexity payoff lands exactly here: $\hat{\boldsymbol\beta}$ is not just *a* minimizer of the squared residuals, it is *the* unique global minimizer, which is why we can trust a one-line formula to deliver the answer rather than having to search.

It is worth pausing on how completely this mirrors Maya. Her risk surface was a quadratic in the weights with a positive-definite Hessian (the covariance matrix $\mathbf{\Sigma}$), so portfolio variance was a convex bowl with one bottom; OLS's SSR is a quadratic in the coefficients with positive-definite Hessian $2\mathbf{X}'\mathbf{X}$, so the fit error is a convex bowl with one bottom. Two different problems — picking portfolio weights, picking regression coefficients — are the *same* optimization, a quadratic minimized by setting a gradient to zero and verified by a positive-definite Hessian. That structural sameness is exactly why Chapter 2.1 promised that minimizing SSR would feel like a sequel to Maya's portfolio rather than a new shock.

**A number, to close the loop.** Run the FOC on Sam's four-day data from Chapter 2.1, where $\mathbf{X}'\mathbf{X} = \operatorname{diag}(4, 6)$ and $\mathbf{X}'\mathbf{y} = (4, 7)'$. The normal equations are $\operatorname{diag}(4,6)\,\hat{\boldsymbol\beta} = (4, 7)'$, two uncoupled equations $4\hat\beta_0 = 4$ and $6\hat\beta_1 = 7$, giving $\hat\beta_0 = 1$ and $\hat\beta_1 = 7/6 \approx 1.167$ — Sam's beta. The Hessian $2\mathbf{X}'\mathbf{X} = \operatorname{diag}(8, 12)$ has eigenvalues $8$ and $12$, both positive, so it is positive definite and the solution is a genuine minimum. Every word of the optimization story checks out on a dataset you can verify by hand.

```python
import numpy as np
X = np.array([[1.0, -2.0], [1.0, 0.0], [1.0, 1.0], [1.0, 1.0]])  # Sam, Ch 2.1
y = np.array([-1.0, 0.0, 3.0, 2.0])
XtX, Xty = X.T @ X, X.T @ y
beta_hat = np.linalg.solve(XtX, Xty)             # FOC: solve normal equations
print("beta-hat:", beta_hat)                     # [1.    1.1667]
print("gradient at beta-hat:", -2*Xty + 2*XtX @ beta_hat)   # [0. 0.] -> FOC holds
print("Hessian eigenvalues:", np.linalg.eigvalsh(2*XtX))    # [ 8. 12.] -> PD -> min
```

## Summary

Optimization is the AP-Calculus max/min recipe promoted to many variables. The derivative becomes the **gradient** $\nabla f$, the column of partial derivatives, each measuring the slope along one axis with the others held fixed; the gradient points uphill steepest. The **first-order condition** $\nabla f = \mathbf{0}$ flags critical points — flat ground that could be a min, a max, or a saddle. The **second-order condition** breaks the tie through the **Hessian**, the symmetric matrix of second partials: a positive-definite Hessian means the surface curves up in every direction, a strict minimum, and a Hessian that is positive (semi)definite *everywhere* makes the function convex, so the one critical point is the unique global minimum. Constraints are handled by the **Lagrangian** $\mathcal{L} = f - \lambda(g - c)$, which bolts the constraint onto the objective with a multiplier $\lambda$ and converts a fenced-in problem into an ordinary first-order-condition problem; running it on Maya's "minimize $\mathbf{w}'\mathbf{\Sigma}\mathbf{w}$ subject to $\mathbf{w}'\mathbf{1}=1$" reproduced her $\mathbf{w}^\star = (0.2, 0.8)'$ and minimum variance $0.008$ from Chapter 1.2. Finally, OLS *is* an optimization: minimizing the sum of squared residuals, the FOC delivers the **normal equations** $\mathbf{X}'\mathbf{X}\hat{\boldsymbol\beta} = \mathbf{X}'\mathbf{y}$ and hence $\hat{\boldsymbol\beta} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$ (Chapter 2.1), while the SOC — the positive-definite Hessian $2\mathbf{X}'\mathbf{X}$ from Appendix A.1 §6 — certifies it is the unique global minimum. The same quadratic-bowl structure governs both Maya's portfolio and Sam's regression, which is why the two feel like one idea. From here, Appendix A.3 (Asymptotics) takes the estimators these optimizations produce and asks what happens to them as the sample grows, and Appendix A.4 is the reference for the distributions that answer shows up in.
