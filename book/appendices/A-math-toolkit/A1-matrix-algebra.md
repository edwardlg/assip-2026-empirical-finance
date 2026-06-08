# A.1 — Matrix Algebra (just enough)

You have already met matrices in this book, whether or not anyone called them that. When Maya stacked two assets' variances and their covariance into the grid $\mathbf{\Sigma}$ in Chapter 1.2, that was a matrix. When Sam wrote his whole regression on one line as $\mathbf{y} = \mathbf{X}\boldsymbol\beta + \boldsymbol\varepsilon$ in Chapter 2.1, every bold symbol there was a vector or a matrix. This appendix is the reference desk for that machinery: it collects, in one place and from the ground up, the linear algebra you need to read Weeks 1 through 8 without ever feeling that a symbol got smuggled past you. It is deliberately *not* a linear algebra course. There is no determinant theory beyond the one $2\times 2$ formula you will actually use, no Gram–Schmidt, no Jordan forms. There is exactly the kit that earns its keep in empirical finance, and every tool is introduced next to the place in the book where it does its job.

The promise of matrix algebra is the same promise Chapter 2.1 cashed out: write the operation once, in a notation that does not grow when the data grow. A regression with two regressors and a regression with twenty look identical on the page — $\hat{\boldsymbol\beta} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$ — and that invariance is not a convenience, it is the whole reason the subject is tractable. To get there we need vectors, the product that combines them, the transpose that flips them, the inverse that "divides" by them, and two structural ideas — rank and positive-definiteness — that tell you *when the machine works* and *when it jams*. We close with the one piece of higher structure you should carry as intuition rather than algebra: eigenvalues as stretch directions, and why $\mathbf{X}'\mathbf{X}$ being symmetric and positive semidefinite is the quiet guarantee behind everything.

## 1. Vectors and matrices: stacking numbers on purpose

**The result, in one sentence.** A vector is an ordered column of numbers and a matrix is a rectangular grid of numbers; their entire point is to let one symbol stand for a whole dataset so that one equation can describe every observation at once.

Start concrete. Sam pulls four trading days of his stock's returns: $-1$, $0$, $3$, $2$ (in percent). Written as a **column vector**, that is

$$
\mathbf{y} = \begin{pmatrix} -1 \\ 0 \\ 3 \\ 2 \end{pmatrix}.
$$

The boldface lowercase letter signals "vector" (the book's convention from CONVENTIONS.md §3), and by default a vector is a *column* — a single stack. A vector with $N$ entries is said to live in $\mathbb{R}^N$, the space of all lists of $N$ real numbers; Sam's $\mathbf{y}$ lives in $\mathbb{R}^4$. We index entries with a subscript, so $y_3 = 3$ is the third day's return. There is nothing mysterious here: a vector is just a column of a spreadsheet given a name so we can talk about all of it at once.

A **matrix** is the next step up: a full rectangular block of numbers, written with a boldface uppercase letter. Sam's design matrix from Chapter 2.1, with a column of ones for the intercept and a column of market returns, was

$$
\mathbf{X} = \begin{pmatrix} 1 & -2 \\ 1 & 0 \\ 1 & 1 \\ 1 & 1 \end{pmatrix}.
$$

We describe a matrix by its **shape**, rows-by-columns, and the order is not negotiable: rows first, columns second. Sam's $\mathbf{X}$ is $4 \times 2$ — four rows, two columns. In the book's standard notation, the design matrix is $N \times K$, where $N$ is the number of observations (rows, one per firm-day-person) and $K$ is the number of regressors (columns, one per variable, counting the intercept's column of ones). We name an individual entry by its row then its column: $X_{32} = 1$ is the entry in row 3, column 2. Reading a matrix's shape correctly is half the battle in everything that follows, because — as the next section makes painfully precise — shapes have to line up or the operation is simply undefined.

It helps to hold two readings of $\mathbf{X}$ in your head at the same time. **By rows**, $\mathbf{X}$ is a stack of observations: row $i$ is everything we know about day $i$, the pair $(1, x_i)$. **By columns**, $\mathbf{X}$ is a collection of variables: the first column is the constant, the second is the market return across all four days. Both readings are correct and both get used. Regression-as-stacked-equations is the row reading; regression-as-projection-onto-the-column-space (Chapter 2.1 §5) is the column reading. A square matrix, where the number of rows equals the number of columns, is special enough to deserve its own word — Maya's $\mathbf{\Sigma}$ and the $\mathbf{X}'\mathbf{X}$ that sits inside the OLS formula are both square ($K \times K$) — because only square matrices can have inverses, which is where Section 4 is headed.

## 2. Matrix multiplication: the row-meets-column rule

**The result, in one sentence.** To multiply two matrices, you slide each row of the first across each column of the second, taking a dot product every time — which is defined only when the inner shapes match, and which produces a new matrix whose shape is the two outer dimensions.

Everything starts with the **dot product** of two vectors, the single operation the whole subject is built from. Given two columns of the same length, you multiply them entry by entry and add up the results. For $\mathbf{u} = (u_1, \dots, u_n)'$ and $\mathbf{v} = (v_1, \dots, v_n)'$,

$$
\mathbf{u} \cdot \mathbf{v} = \sum_{i=1}^{n} u_i v_i = u_1 v_1 + u_2 v_2 + \cdots + u_n v_n,
$$

a single number. You have seen this exact operation already wearing a different hat: in Chapter 1.2, the covariance of two mean-centered return series *was* a dot product, which is why "uncorrelated" turned out to mean "perpendicular." The dot product is the atom; matrix multiplication is just many dot products arranged in a grid.

Here is the rule. To form the product $\mathbf{A}\mathbf{B}$, the entry in row $i$, column $j$ of the result is the dot product of **row $i$ of $\mathbf{A}$** with **column $j$ of $\mathbf{B}$**. For that dot product to make sense, row $i$ of $\mathbf{A}$ and column $j$ of $\mathbf{B}$ must have the same length — which means the number of columns of $\mathbf{A}$ must equal the number of rows of $\mathbf{B}$. State the shapes as $\mathbf{A}$ is $(m \times n)$ and $\mathbf{B}$ is $(n \times p)$: the two inner $n$'s must agree (the product is otherwise undefined), and they cancel, leaving a result of shape $(m \times p)$:

$$
\underbrace{(m \times n)}_{\mathbf{A}} \cdot \underbrace{(n \times p)}_{\mathbf{B}} = \underbrace{(m \times p)}_{\mathbf{A}\mathbf{B}}.
$$

This "inner dimensions match, outer dimensions survive" bookkeeping is the single most useful habit in the whole appendix. Before you ever compute a matrix product, write down the shapes and check that the inner numbers agree. If they do not, you have made a modeling error, not an arithmetic one.

**A number first.** Take a tiny case. Let

$$
\mathbf{A} = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix} \ (2\times 2), \qquad \mathbf{b} = \begin{pmatrix} 5 \\ 6 \end{pmatrix} \ (2 \times 1).
$$

The inner dimensions ($2$ and $2$) match, so $\mathbf{A}\mathbf{b}$ exists and is $2 \times 1$. The first entry is row 1 of $\mathbf{A}$ dotted with $\mathbf{b}$: $(1)(5) + (2)(6) = 5 + 12 = 17$. The second is row 2 dotted with $\mathbf{b}$: $(3)(5) + (4)(6) = 15 + 24 = 39$. So $\mathbf{A}\mathbf{b} = (17, 39)'$. Notice that a matrix times a vector returns a vector — and that each entry of that vector is one dot product, one weighted combination of the inputs. That is exactly what a fitted value is: $\hat y_i = \mathbf{x}_i' \boldsymbol\beta$ is the $i$-th row of $\mathbf{X}$ dotted with the coefficient vector, the prediction for observation $i$.

**Where the OLS shapes come from.** Now watch the regression formula type-check itself. With $\mathbf{X}$ being $N \times K$, $\boldsymbol\beta$ being $K \times 1$, and $\mathbf{y}$ being $N \times 1$:

- $\mathbf{X}\boldsymbol\beta$ has shapes $(N\times K)(K \times 1)$ — inner $K$'s match — yielding $N \times 1$, the right shape to compare with $\mathbf{y}$. Good: the model equation $\mathbf{y} = \mathbf{X}\boldsymbol\beta + \boldsymbol\varepsilon$ adds vectors of matching length.
- $\mathbf{X}'$ (the transpose, Section 3) is $K \times N$, so $\mathbf{X}'\mathbf{X}$ is $(K \times N)(N \times K) = K \times K$, a square matrix — the one we will invert.
- $\mathbf{X}'\mathbf{y}$ is $(K \times N)(N \times 1) = K \times 1$, a vector.
- $(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$ is $(K \times K)(K \times 1) = K \times 1$, exactly the shape $\hat{\boldsymbol\beta}$ must have, one number per regressor.

Every product in $\hat{\boldsymbol\beta} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$ is legal and the final shape is right. That is not a coincidence; it is the shapes confirming the formula could not have meant anything else.

**Three warnings you will trip over if you skip them.** First, **order matters**: in general $\mathbf{A}\mathbf{B} \ne \mathbf{B}\mathbf{A}$, and frequently one of the two does not even exist because the shapes only line up one way. Matrix multiplication is *not* commutative; this is the single most common beginner mistake, and it is why we are always careful to say "multiply both sides *on the left*" or "*on the right*." Second, multiplication *is* associative, $(\mathbf{A}\mathbf{B})\mathbf{C} = \mathbf{A}(\mathbf{B}\mathbf{C})$, and distributive over addition, so you may regroup and expand freely as long as you never reorder. Third, a row vector times a column vector ($1 \times n$ times $n \times 1$) gives a single number — that is the dot product again — whereas a column times a row ($n \times 1$ times $1 \times n$) gives a full $n \times n$ matrix, the **outer product**. Maya's covariance matrix was secretly built from an averaged outer product, $\mathbf{\Sigma} = \mathbb{E}[(\mathbf{R} - \mathbb{E}[\mathbf{R}])(\mathbf{R} - \mathbb{E}[\mathbf{R}])']$ (Chapter 1.2 §5); the order of the two vectors there is what turns a list of returns into a square grid of covariances.

```python
import numpy as np
A = np.array([[1, 2], [3, 4]])
b = np.array([5, 6])
print(A @ b)          # [17 39]  -- the @ operator is matrix multiply
print(A.shape, b.shape)   # (2, 2) (2,)
# Try A @ A.T vs A.T @ A to feel how order changes the result.
```

## 3. The transpose: flipping rows and columns

**The result, in one sentence.** The transpose $\mathbf{A}'$ reflects a matrix across its diagonal, turning rows into columns, and it is the operation that lets a dot product, a sum of squares, and a covariance all be written as one matrix multiply.

The transpose is the simplest operation here and one of the most used. To transpose a matrix, you turn its rows into columns: the entry that was in row $i$, column $j$ moves to row $j$, column $i$. A $4 \times 2$ matrix becomes $2 \times 4$. For Sam's design matrix,

$$
\mathbf{X} = \begin{pmatrix} 1 & -2 \\ 1 & 0 \\ 1 & 1 \\ 1 & 1 \end{pmatrix}
\qquad\Longrightarrow\qquad
\mathbf{X}' = \begin{pmatrix} 1 & 1 & 1 & 1 \\ -2 & 0 & 1 & 1 \end{pmatrix}.
$$

The book writes the transpose with a prime, $\mathbf{X}'$ (you will also see $\mathbf{X}^\top$ in other texts; they mean the same thing). A column vector transposed becomes a row vector, which is why the dot product $\mathbf{u} \cdot \mathbf{v}$ is written $\mathbf{u}'\mathbf{v}$: laying $\mathbf{u}$ flat as a row ($1 \times n$) and multiplying by the column $\mathbf{v}$ ($n \times 1$) gives the single number $(1 \times 1)$ that is the dot product. This is the notation Chapter 2.1 used the moment it wrote the sum of squared residuals as $\mathbf{e}'\mathbf{e}$ — a vector laid flat and multiplied by itself, which sums its squared entries, giving the squared length.

Two facts about the transpose carry real weight. The first is the **reversal rule** for products:

$$
(\mathbf{A}\mathbf{B})' = \mathbf{B}'\mathbf{A}'.
$$

Transposing a product reverses the order and transposes each factor. This is not a curiosity; it is the workhorse that lets you simplify the algebra of OLS. Chapter 2.1 used it twice in one breath — to expand $(\mathbf{y} - \mathbf{X}\mathbf{b})'(\mathbf{y} - \mathbf{X}\mathbf{b})$ and to prove the hat matrix is symmetric. The second fact is the definition of a **symmetric matrix**: one that equals its own transpose, $\mathbf{A}' = \mathbf{A}$. Only square matrices can be symmetric, and symmetry means the grid is a mirror image across its main diagonal — the $(i,j)$ entry equals the $(j,i)$ entry. Maya's covariance matrix is symmetric because $\operatorname{Cov}(R_j, R_k) = \operatorname{Cov}(R_k, R_j)$, and $\mathbf{X}'\mathbf{X}$ is symmetric because of the reversal rule: $(\mathbf{X}'\mathbf{X})' = \mathbf{X}'(\mathbf{X}')' = \mathbf{X}'\mathbf{X}$, since transposing twice returns the original. Symmetry is the precondition for the spectral picture in Section 7, so it is worth recognizing on sight: any matrix of the form $\mathbf{A}'\mathbf{A}$ is automatically square and symmetric, and both $\mathbf{X}'\mathbf{X}$ and $\mathbf{\Sigma}$ are of exactly this build.

## 4. The identity and the inverse: how to "divide" by a matrix

**The result, in one sentence.** The identity matrix $\mathbf{I}$ is the matrix that does nothing when you multiply by it, and the inverse $\mathbf{A}^{-1}$ is the matrix that undoes $\mathbf{A}$ — the closest thing to division that matrices have — but only square, non-degenerate matrices possess one.

The number $1$ has a defining property: multiply anything by it and nothing changes. Among matrices, the **identity matrix** $\mathbf{I}$ plays that role. It is square, with $1$'s down the main diagonal and $0$'s everywhere else, and for any compatible matrix $\mathbf{A}\mathbf{I} = \mathbf{I}\mathbf{A} = \mathbf{A}$. The $2 \times 2$ and $3 \times 3$ identities are

$$
\mathbf{I}_2 = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}, \qquad
\mathbf{I}_3 = \begin{pmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix}.
$$

The residual-maker derivation in Chapter 2.1 §6, $\mathbf{M} = \mathbf{I} - \mathbf{H}$, leans on exactly this "$\mathbf{I}$ leaves vectors untouched" property: $\mathbf{M}\mathbf{y} = (\mathbf{I} - \mathbf{H})\mathbf{y} = \mathbf{y} - \mathbf{H}\mathbf{y}$, the original outcome minus its fitted shadow.

Now, division. You cannot divide by a matrix the way you divide by a number, but you can do the next best thing: multiply by its **inverse**. The inverse of a square matrix $\mathbf{A}$, written $\mathbf{A}^{-1}$, is the unique matrix that satisfies

$$
\mathbf{A}^{-1}\mathbf{A} = \mathbf{A}\mathbf{A}^{-1} = \mathbf{I}.
$$

It is the matrix that undoes $\mathbf{A}$, exactly as $\tfrac{1}{a}$ undoes multiplication by $a$. This is the engine of the whole OLS formula. The normal equations from Chapter 2.1 read $\mathbf{X}'\mathbf{X}\,\hat{\boldsymbol\beta} = \mathbf{X}'\mathbf{y}$; to solve for $\hat{\boldsymbol\beta}$ you multiply both sides *on the left* by $(\mathbf{X}'\mathbf{X})^{-1}$, the left side collapses because $(\mathbf{X}'\mathbf{X})^{-1}(\mathbf{X}'\mathbf{X}) = \mathbf{I}$, and out drops $\hat{\boldsymbol\beta} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$. "Solving a linear system" and "inverting the coefficient matrix" are the same act.

But here is the catch that governs half of econometrics: **not every square matrix has an inverse.** A matrix with no inverse is called **singular**; one that has an inverse is **non-singular** or **invertible**. The number analogy is exact — $0$ is the one number you cannot divide by, and a singular matrix is the matrix version of zero, a matrix that has "collapsed" some directions to nothing. Section 5 tells you precisely when this collapse happens (it is a rank condition), and Section 6 tells you why it matters that it never *quite* happens in real data.

**Inverting a $2\times 2$ by hand.** For the smallest interesting case there is a formula worth memorizing. For

$$
\mathbf{A} = \begin{pmatrix} a & b \\ c & d \end{pmatrix}, \qquad
\mathbf{A}^{-1} = \frac{1}{ad - bc}\begin{pmatrix} d & -b \\ -c & a \end{pmatrix}.
$$

You swap the two diagonal entries, negate the two off-diagonal entries, and divide everything by the number $ad - bc$, which is called the **determinant** of $\mathbf{A}$. Look at what happens when the determinant is zero: you would be dividing by zero, and the inverse does not exist. **A $2\times 2$ matrix is singular exactly when $ad - bc = 0$**, and that condition, $ad = bc$, means the two columns are proportional — one is a scalar multiple of the other — which is the smallest example of the linear dependence Section 5 is about.

Let us invert a real one. Take

$$
\mathbf{A} = \begin{pmatrix} 4 & 2 \\ 2 & 3 \end{pmatrix}.
$$

The determinant is $ad - bc = (4)(3) - (2)(2) = 12 - 4 = 8$, which is nonzero, so the inverse exists. Apply the formula — swap the $4$ and $3$, negate the two $2$'s, divide by $8$:

$$
\mathbf{A}^{-1} = \frac{1}{8}\begin{pmatrix} 3 & -2 \\ -2 & 4 \end{pmatrix} = \begin{pmatrix} 3/8 & -1/4 \\ -1/4 & 1/2 \end{pmatrix}.
$$

Always check by multiplying back to the identity. Row 1 of $\mathbf{A}$ dotted with column 1 of $\mathbf{A}^{-1}$: $(4)(3/8) + (2)(-1/4) = 12/8 - 2/4 = 1.5 - 0.5 = 1$. Off-diagonal, row 1 with column 2: $(4)(-1/4) + (2)(1/2) = -1 + 1 = 0$. Continuing gives $\mathbf{A}\mathbf{A}^{-1} = \mathbf{I}_2$ exactly, as it must. (This is the same $2\times 2$ inversion you would do to find the minimum-variance portfolio weights for two assets, where $\mathbf{A}$ is the covariance matrix $\mathbf{\Sigma}$ — the Lagrange solution in Appendix A.2 §4 needs precisely $\mathbf{\Sigma}^{-1}$.) For Sam's regression in Chapter 2.1, the matrix to invert came out diagonal, $\mathbf{X}'\mathbf{X} = \operatorname{diag}(4, 6)$, and a diagonal matrix is inverted by reciprocating each diagonal entry: $(\mathbf{X}'\mathbf{X})^{-1} = \operatorname{diag}(1/4, 1/6)$ — the determinant there is $4 \times 6 = 24 \ne 0$, so the inverse exists, and Sam's beta of $7/6$ followed in one multiply. Beyond $2 \times 2$ the hand formula gets ugly fast, and in practice you never invert by hand: you call `np.linalg.inv`, or better `np.linalg.solve`, which solves the system without ever forming the inverse and is more numerically stable.

```python
import numpy as np
A = np.array([[4.0, 2.0], [2.0, 3.0]])
Ainv = np.linalg.inv(A)
print(Ainv)               # [[ 0.375 -0.25 ] [-0.25   0.5  ]]
print(A @ Ainv)           # ~ identity (tiny floating-point dust off-diagonal)
print(np.linalg.det(A))   # 8.0  -- nonzero, so invertible
```

## 5. Rank and full column rank: when the machine has enough information

**The result, in one sentence.** The rank of a matrix counts how many genuinely independent directions its columns carry; a regression's $\mathbf{X}'\mathbf{X}$ is invertible exactly when $\mathbf{X}$ has *full column rank*, meaning no regressor is a perfect linear combination of the others.

We need a precise word for "the columns carry redundant information," because that redundancy is exactly what makes a matrix singular. Two vectors are **linearly dependent** if one is a scalar multiple of the other; a whole set of columns is linearly dependent if some column can be written as a weighted sum of the others. If no such relationship exists — if the only way to combine the columns and land on the zero vector is to weight them all by zero — the columns are **linearly independent**. The **rank** of a matrix is the number of linearly independent columns it has, which is the true dimension of the space those columns can reach (the column space from Chapter 2.1 §5).

For a design matrix $\mathbf{X}$ that is $N \times K$, the most columns could possibly be independent is $K$ (you cannot have more independent directions than you have columns). When the rank hits that ceiling, $\operatorname{rank}(\mathbf{X}) = K$, we say $\mathbf{X}$ has **full column rank**, and this is precisely the condition under which OLS works. The chain of equivalences is worth stating once, cleanly, because Week 2 leans on every link:

$$
\mathbf{X} \text{ has full column rank } K
\;\Longleftrightarrow\;
\mathbf{X}'\mathbf{X} \text{ is invertible}
\;\Longleftrightarrow\;
\hat{\boldsymbol\beta} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y} \text{ exists and is unique.}
$$

Read it left to right: if the regressors are non-redundant, the system can be solved and the answer is pinned down. Read it right to left and you have the diagnosis of every "matrix is singular" error a stats package will ever throw at you. The failure case has the grim name **perfect multicollinearity**: some regressor is an exact linear combination of the others.

The intuition is the same one Chapter 2.1 §7 gave with Sam's example. Suppose Sam accidentally includes the market return measured in percent *and* the same return measured in basis points — exactly $100$ times the first column. Those two columns are proportional, so the rank does not actually rise when you add the second: the column space still has the dimension it had before, and there is no unique way to split a coefficient between two columns that carry identical information. Should beta load on the percent column or the basis-point column? Any split that adds up to the same fitted values is equally good, so the data cannot choose, and $\hat{\boldsymbol\beta}$ is not determined. The algebra mirrors this exactly: if column redundancy lets you build a nonzero vector $\mathbf{v}$ with $\mathbf{X}\mathbf{v} = \mathbf{0}$, then $\mathbf{v}'\mathbf{X}'\mathbf{X}\mathbf{v} = \lVert\mathbf{X}\mathbf{v}\rVert^2 = 0$ for that nonzero $\mathbf{v}$ — the matrix $\mathbf{X}'\mathbf{X}$ has a direction it crushes to zero length, which is the geometric signature of singularity.

This is the *same* wall Maya hit in Chapter 1.2 §5 from the portfolio side. If one asset is a linear combination of others — a fund that is exactly 60% asset 1 plus 40% asset 2 — then the columns of the covariance matrix $\mathbf{\Sigma}$ become linearly dependent, $\mathbf{\Sigma}$ drops rank, goes singular, and cannot be inverted, so the minimum-variance portfolio is not uniquely defined. Singular $\mathbf{\Sigma}$ in Week 1 and singular $\mathbf{X}'\mathbf{X}$ in Week 2 are the same mathematical event with the same cure: do not feed the machine a column that some other columns already contain. Two practical consequences follow immediately. First, full column rank requires at least as many observations as regressors, $N \ge K$ — you cannot fit more coefficients than you have data points, or the columns are forced into dependence (a fact that haunts high-dimensional and panel settings in Weeks 6–8). Second, perfect collinearity in real data almost always signals a coding bug, classically the **dummy-variable trap**: including a separate 0/1 indicator for *every* category *plus* an intercept, so the category dummies sum to the all-ones column and reproduce the intercept exactly. The fix is to drop one category (the omitted baseline) or the intercept.

## 6. Positive (semi)definiteness: the matrix version of "non-negative"

**The result, in one sentence.** A symmetric matrix is positive semidefinite if the quadratic form $\mathbf{v}'\mathbf{A}\mathbf{v}$ is never negative, and positive definite if it is strictly positive for every nonzero $\mathbf{v}$ — the matrix generalization of "this number is $\ge 0$" and "this number is $> 0$," and the property that distinguishes a singular jam from a clean, invertible fit.

A single number can be positive, negative, or zero. The matrix analogue of "non-negative" is not about the entries of the matrix — they can be any sign — but about a *quantity the matrix produces*. Given a symmetric matrix $\mathbf{A}$ and any vector $\mathbf{v}$, the expression

$$
\mathbf{v}'\mathbf{A}\mathbf{v}
$$

is a single number, called a **quadratic form**. (Check the shapes: $(1\times n)(n \times n)(n \times 1) = 1 \times 1$, a scalar.) We classify $\mathbf{A}$ by the sign this number takes as $\mathbf{v}$ ranges over all nonzero vectors. If $\mathbf{v}'\mathbf{A}\mathbf{v} > 0$ for every $\mathbf{v} \ne \mathbf{0}$, the matrix is **positive definite (PD)**. If $\mathbf{v}'\mathbf{A}\mathbf{v} \ge 0$ for every $\mathbf{v}$, allowing equality, it is **positive semidefinite (PSD)**. The difference between $>$ and $\ge$ is the whole story: a PSD matrix that is *not* PD has some nonzero direction it sends to zero, and that direction is exactly the linear-dependence direction of Section 5 — so PSD-but-not-PD means *singular*, and PD means *invertible*.

You have already proven the two facts that matter, in two different chapters, without the vocabulary. In Chapter 1.2, Maya's covariance matrix satisfied $\mathbf{w}'\mathbf{\Sigma}\mathbf{w} = \operatorname{Var}(\mathbf{w}'\mathbf{R}) \ge 0$ — a portfolio's variance can never be negative — which is *precisely* the statement that $\mathbf{\Sigma}$ is PSD. In Chapter 2.1, the same argument settled that $\mathbf{X}'\mathbf{X}$ is PSD: for any $\mathbf{v}$,

$$
\mathbf{v}'\mathbf{X}'\mathbf{X}\mathbf{v} = (\mathbf{X}\mathbf{v})'(\mathbf{X}\mathbf{v}) = \lVert\mathbf{X}\mathbf{v}\rVert^2 \ge 0,
$$

because a squared length is never negative. And it pins down the boundary: this quantity is *zero* only if $\mathbf{X}\mathbf{v} = \mathbf{0}$, which (Section 5) happens for some nonzero $\mathbf{v}$ exactly when the columns are dependent. So $\mathbf{X}'\mathbf{X}$ is positive *definite* (strictly, every direction positive) when $\mathbf{X}$ has full column rank, and merely positive *semidefinite* (some direction flat) when it does not. Full rank, PD, invertible, unique $\hat{\boldsymbol\beta}$ — these are four names for the same healthy state.

Two payoffs make this worth the vocabulary. The first is in Appendix A.2 on optimization: a function is at a genuine *minimum* when its matrix of second derivatives (the Hessian) is positive definite, the multivariable echo of "the second derivative is positive at the bottom of a parabola." The SSR objective that OLS minimizes has Hessian $2\mathbf{X}'\mathbf{X}$, and its positive semidefiniteness is exactly why the normal-equations solution is a minimum rather than a maximum or a saddle (Chapter 2.1 §3) — when it is positive *definite*, that minimum is the *unique* bottom of a strictly convex bowl. The second payoff is variance matrices everywhere downstream: the estimated variance of $\hat{\boldsymbol\beta}$, the sandwich/robust covariance matrices of Chapter 2.4, and the cluster and HAC variants all must come out PSD to be believable, because a variance that went negative in some direction would be reporting a portfolio of coefficients with negative uncertainty, which is nonsense. PSD-ness is the sanity check that a thing claiming to be a variance actually could be one.

## 7. The spectral idea: eigenvalues as stretch directions

**The result, in one sentence.** Every symmetric matrix acts on space by stretching it along a set of perpendicular axes, and the stretch factors are the **eigenvalues** — positive ones for a positive-definite matrix, a zero one exactly where the matrix is singular — which makes "eigenvalues" the precise dial for how close $\mathbf{X}'\mathbf{X}$ is to collapsing.

This last idea is the one to carry as a mental picture rather than a computation; you will not invert anything by hand here, and you do not need the characteristic-polynomial machinery. Think of a matrix as a *transformation*: feed it a vector, it returns a vector, generally pointing somewhere new and scaled to a new length. For most input directions the matrix both rotates and stretches. But a symmetric matrix has special directions it does *not* rotate — directions it only stretches or shrinks, leaving them pointing the same way. Those special directions are the **eigenvectors**, and the factor by which each is stretched is its **eigenvalue** $\lambda$. The defining relationship is

$$
\mathbf{A}\mathbf{v} = \lambda \mathbf{v},
$$

read as "$\mathbf{A}$ applied to the direction $\mathbf{v}$ just scales $\mathbf{v}$ by the number $\lambda$." The deep fact about *symmetric* matrices — the **spectral theorem**, which both $\mathbf{\Sigma}$ and $\mathbf{X}'\mathbf{X}$ obey because they are symmetric — is that these stretch directions are mutually perpendicular and there are exactly enough of them to describe the matrix completely. A symmetric matrix is therefore nothing but a set of perpendicular axes, each with a stretch factor: it takes a sphere and squashes or stretches it into an ellipse whose axes are the eigenvectors and whose radii are the eigenvalues.

This picture instantly re-explains everything above, which is why it is worth holding. **Positive definiteness becomes "all eigenvalues are positive"**: every direction gets stretched by a positive factor, nothing is flattened, so $\mathbf{v}'\mathbf{A}\mathbf{v} > 0$ always. **Positive semidefiniteness allows a zero eigenvalue**: one axis gets stretched by $0$, flattening that direction to a point — and a flattened direction is exactly a direction the matrix crushes, which is singularity. So *a symmetric matrix is singular precisely when one of its eigenvalues is zero*, and this is the cleanest single statement of when OLS jams. The determinant, it turns out, is just the product of the eigenvalues, which is why "determinant $= 0$" and "some eigenvalue $= 0$" say the same thing.

Now the part that matters most in practice, and the reason this appendix bothered with eigenvalues at all: **near-collinearity is a near-zero eigenvalue.** In real data you almost never see *perfect* collinearity (Section 5), so $\mathbf{X}'\mathbf{X}$ is technically invertible — none of its eigenvalues is exactly zero. But two regressors that are *almost* redundant (a firm's total assets and its total liabilities, say, which track each other closely) drive one eigenvalue of $\mathbf{X}'\mathbf{X}$ *close* to zero, so the matrix is invertible but barely. Inverting it then divides by that tiny eigenvalue, blowing up the corresponding direction of $(\mathbf{X}'\mathbf{X})^{-1}$ — and since the variance of $\hat{\boldsymbol\beta}$ is proportional to $(\mathbf{X}'\mathbf{X})^{-1}$ (Chapter 2.4), the coefficients on the near-collinear regressors get enormous standard errors. The estimate becomes wildly sensitive to tiny changes in the data, exactly the instability Chapter 2.1 §7 flagged. The ratio of the largest to the smallest eigenvalue even has a name, the **condition number**, and software warns you when it gets large. So the eigenvalue picture is not decoration: it is the dial that reads how close your regression is to falling apart, and it connects the abstract "rank" of Section 5 to the concrete, quantifiable "imprecise estimates" you will diagnose in Week 2.

The same eigenvalue lens reappears whenever this book reduces dimensions or summarizes covariance: principal-component-style thinking (the directions of largest variance are the top eigenvectors of $\mathbf{\Sigma}$, with the eigenvalues measuring how much variance each captures) underlies the factor models and dimension-reduction tools you meet in the later weeks. You do not need to compute an eigendecomposition by hand anywhere in this book — `np.linalg.eigvalsh` does it for symmetric matrices in one call — but you should be able to look at "this matrix is symmetric PSD with a near-zero eigenvalue" and immediately translate it to "this is a covariance-like object whose nearly-collinear direction will make some estimate imprecise." That translation is the entire working intuition.

```python
import numpy as np
# Sam's X'X from Ch 2.1 -- diagonal, well-conditioned
XtX = np.array([[4.0, 0.0], [0.0, 6.0]])
print(np.linalg.eigvalsh(XtX))     # [4. 6.]  -- both positive => positive definite

# Near-collinear design: second column almost equals the first
X = np.array([[1.0, 1.001], [1.0, 0.999], [1.0, 1.000], [1.0, 1.002]])
vals = np.linalg.eigvalsh(X.T @ X)
print(vals)                         # one eigenvalue tiny => near-singular
print(np.linalg.cond(X.T @ X))      # large condition number => unstable beta-hat
```

## Summary

A vector is a named column of numbers and a matrix is a named grid, shaped rows-by-columns; the design matrix $\mathbf{X}$ is $N \times K$, with rows reading as observations and columns reading as variables. Matrix multiplication is the row-meets-column dot-product rule — inner dimensions must match, outer dimensions survive — and checking those shapes is what makes the OLS formula $\hat{\boldsymbol\beta} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$ type-check, with $\mathbf{X}'\mathbf{X}$ landing at $K\times K$ and $\hat{\boldsymbol\beta}$ at $K \times 1$. The transpose flips rows and columns, reverses across products as $(\mathbf{A}\mathbf{B})' = \mathbf{B}'\mathbf{A}'$, and makes any $\mathbf{A}'\mathbf{A}$ symmetric — so both $\mathbf{X}'\mathbf{X}$ and Maya's $\mathbf{\Sigma}$ are symmetric. The identity $\mathbf{I}$ does nothing; the inverse $\mathbf{A}^{-1}$ undoes $\mathbf{A}$ and exists only when $\mathbf{A}$ is non-singular, with the $2\times 2$ inverse hinging on the determinant $ad - bc$ being nonzero. A matrix is invertible exactly when its columns are linearly independent — full column rank — which is the same singular-matrix wall that perfect multicollinearity in $\mathbf{X}'\mathbf{X}$ (Week 2) and a redundant asset in $\mathbf{\Sigma}$ (Week 1) both run into. Positive (semi)definiteness is the matrix "$\ge 0$": $\mathbf{X}'\mathbf{X}$ and $\mathbf{\Sigma}$ are always PSD because their quadratic forms are squared lengths and variances, and they are positive *definite* — strictly invertible — exactly when there is full rank, which is also why the SSR Hessian $2\mathbf{X}'\mathbf{X}$ certifies a minimum (Appendix A.2). Finally, the spectral picture: a symmetric matrix stretches space along perpendicular eigenvector axes by its eigenvalue factors, positive definiteness means all eigenvalues are positive, singularity means a zero eigenvalue, and near-collinearity means a near-zero eigenvalue — the large condition number that makes $\hat{\boldsymbol\beta}$ imprecise. From here, Appendix A.2 puts these objects to work in optimization, and Appendix A.3 (Asymptotics) and A.4 (Distributions reference) build the inference machinery on top.
