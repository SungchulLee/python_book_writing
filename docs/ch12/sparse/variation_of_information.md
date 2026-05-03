# Variation of Information

!!! tip "Mental Model"
    Variation of information measures the distance between two clusterings using information theory: how many bits you lose going from one clustering to another, plus how many you gain. It is a true metric (unlike mutual information), and computing it efficiently on large datasets requires sparse matrices because the joint distribution over cluster pairs is almost always sparse.

## Background

The **variation of information** (VI) is a metric on the space of clusterings,
introduced by Marina Meila. It measures how much information is lost and gained
when moving from one clustering to another. Unlike many clustering comparison
measures, VI is a true metric: it satisfies non-negativity, symmetry, and the
triangle inequality.

VI is defined in terms of conditional entropies:

$$
\mathrm{VI}(X; Y) = H(X \mid Y) + H(Y \mid X)
$$

where $H(X \mid Y)$ is the conditional entropy of clustering $X$ given
clustering $Y$. When two clusterings are identical, $\mathrm{VI} = 0$.

Computing VI efficiently for large datasets requires sparse matrix operations
because the joint probability matrix between cluster labels is typically very
sparse.

## Objective

This example demonstrates how to:

- build sparse matrices from cluster assignment data using COO format
- convert between sparse formats (COO to CSR)
- compute marginal and conditional probabilities from sparse joint distributions
- use `sparse.diags` for efficient diagonal matrix operations
- implement the variation of information metric using sparse matrix arithmetic

## Setup

Given two clusterings $X$ and $Y$ of $n$ data points, each point receives a
cluster label. The joint distribution $p(x, y)$ counts how many points have
label $x$ in the first clustering and label $y$ in the second, then normalizes
by $n$. This joint distribution is naturally sparse because most cluster pairs
have no shared points.

The marginal distributions are:

$$
p(x) = \sum_y p(x, y), \qquad p(y) = \sum_x p(x, y)
$$

The conditional entropy $H(Y \mid X)$ is:

$$
H(Y \mid X) = -\sum_x p(x) \sum_y p(y \mid x) \log p(y \mid x)
$$

where $p(y \mid x) = p(x, y) / p(x)$.

## Code

### Building Sparse Matrices from Coordinate Data

The COO (Coordinate) format stores entries as `(row, col, data)` triples,
making it the natural choice for constructing a joint distribution from
paired cluster labels.

```python
import numpy as np
from scipy import sparse

x = np.array([1, 0, 2, 1, 1, 2])  # cluster labels from first clustering
y = np.array([0, 1, 1, 2, 0, 2])  # cluster labels from second clustering
data = np.ones(len(x))             # count 1 for each data point

coo = sparse.coo_matrix((data, (x, y)), shape=(3, 3))
print(coo)
```

```
  (1, 0)	1.0
  (0, 1)	1.0
  (2, 1)	1.0
  (1, 2)	1.0
  (1, 0)	1.0
  (2, 2)	1.0
```

### Converting to CSR and Normalizing

CSR (Compressed Sparse Row) format supports efficient arithmetic operations.
Converting and normalizing produces the joint probability distribution.

```python
csr = coo.tocsr()
pxy = csr.copy()
pxy.data /= np.sum(pxy.data)
print("Sum:", pxy.sum())  # 1.0
```

### Computing Marginal Probabilities

Row sums give $p(x)$ and column sums give $p(y)$.

```python
px = np.array(pxy.sum(axis=1)).ravel()  # p(x): sum over y
py = np.array(pxy.sum(axis=0)).ravel()  # p(y): sum over x
print("p(x):", px)  # [0.1667, 0.5, 0.3333]
print("p(y):", py)  # [0.3333, 0.3333, 0.3333]
```

### Diagonal Matrices and Safe Operations

The `sparse.diags` function creates diagonal matrices efficiently. Two helper
functions handle the numerical edge cases where $0 \cdot \log 0 = 0$ by
convention and division by zero must be avoided.

```python
def safe_inverse(arr):
    """Invert array elements, leaving zeros as zeros."""
    result = arr.copy()
    nz = np.nonzero(arr)
    result[nz] = 1 / arr[nz]
    return result

def xlogx(arr):
    """Compute x * log2(x), treating 0 * log(0) = 0."""
    result = arr.copy()
    nz = np.nonzero(arr)
    result[nz] = arr[nz] * np.log2(arr[nz])
    return result

px_inv = sparse.diags([safe_inverse(px)], [0])
py_inv = sparse.diags([safe_inverse(py)], [0])
```

### Variation of Information

Combining all the pieces, the VI computation uses sparse matrix products
to compute conditional probabilities and entropies.

```python
def variation_of_information(x, y):
    """
    Compute Variation of Information between two clusterings.

    VI(X;Y) = H(X|Y) + H(Y|X)

    Parameters
    ----------
    x, y : array-like
        Cluster assignment arrays of the same length.

    Returns
    -------
    float
        VI score. Lower is better; 0 means identical clusterings.
    """
    pxy = sparse.coo_matrix(
        (np.ones(x.size), (x.ravel(), y.ravel())), dtype=float
    ).tocsr()
    pxy.data /= np.sum(pxy.data)

    px = np.array(pxy.sum(axis=1)).ravel()
    py = np.array(pxy.sum(axis=0)).ravel()

    px_inv = sparse.diags([safe_inverse(px)], [0])
    py_inv = sparse.diags([safe_inverse(py)], [0])

    # H(Y|X) via p(y|x) = diag(1/p(y)) @ p(x,y)
    hygx = -(px * xlogx(py_inv.dot(pxy)).sum(axis=1)).sum()
    # H(X|Y) via p(x|y) = p(x,y) @ diag(1/p(x))
    hxgy = -(py * xlogx(pxy.dot(px_inv)).sum(axis=1)).sum()

    return hygx + hxgy

c1 = np.array([0, 0, 1, 1, 2, 2])
c2 = np.array([0, 0, 1, 1, 2, 2])
c3 = np.array([0, 1, 0, 1, 0, 1])

print("VI(identical):", variation_of_information(c1, c2))  # ~0
print("VI(different):", variation_of_information(c1, c3))   # > 0
```

```
VI(identical): 0.0
VI(different): 1.459
```

## Interpretation

The variation of information captures two complementary types of mismatch
between clusterings:

- $H(X \mid Y)$ measures the information about $X$ that is **not** explained
  by $Y$. If $Y$ perfectly predicts $X$, this term is zero.
- $H(Y \mid X)$ measures the information about $Y$ that is **not** explained
  by $X$.

When both conditional entropies are zero, the clusterings are identical and
$\mathrm{VI} = 0$. A larger VI indicates more disagreement.

!!! note "Key Insight"
    Unlike the Rand index or mutual information, VI is a true metric on the
    space of clusterings. This means you can use it to define distances between
    clusterings in algorithms that require metric properties, such as computing
    medians or building clustering dendrograms.

## Statistical Insight

The sparse matrix approach is essential for scalability. If there are $k_1$
clusters in $X$ and $k_2$ clusters in $Y$, the joint distribution matrix has
shape $k_1 \times k_2$. For fine-grained clusterings of large datasets, most
entries are zero because most cluster pairs share no points. Sparse storage
reduces memory from $O(k_1 k_2)$ to $O(\min(n, k_1 k_2))$ and sparse
arithmetic avoids wasted computation on zero entries.

!!! warning "Common Mistake"
    Do not use `np.log` on sparse matrix data without handling zeros. The
    convention $0 \log 0 = 0$ must be enforced explicitly, otherwise `NaN`
    values propagate through the computation.

The key sparse patterns used here generalize to many information-theoretic
computations:

| Pattern | Sparse operation |
|---|---|
| Normalize to probabilities | Divide `.data` by total sum |
| Compute marginals | `sum(axis=0)` or `sum(axis=1)` |
| Conditional probabilities | Multiply by `sparse.diags(1/marginal)` |
| Element-wise $x \log x$ | Apply only to `.data` (non-zero entries) |

## Extensions

- Compute the **normalized variation of information** $\mathrm{NVI} = \mathrm{VI} / \log n$
  to obtain a value between 0 and 1
- Implement **mutual information** $I(X; Y) = H(X) + H(Y) - H(X, Y)$ using
  the same sparse framework
- Compare VI against the adjusted Rand index on synthetic clustering benchmarks
- Scale the implementation to clusterings with millions of points and observe
  the memory advantage of sparse formats

## Exercises

**Exercise 1.**
Given the joint probability matrix below in dense form, compute $H(X \mid Y)$
by hand using base-2 logarithms.

| | $y=0$ | $y=1$ |
|---|---|---|
| $x=0$ | 0.25 | 0.25 |
| $x=1$ | 0.125 | 0.375 |

??? success "Solution to Exercise 1"
    First compute $p(y)$: $p(y=0) = 0.375$, $p(y=1) = 0.625$.

    Conditional distribution $p(x \mid y=0)$: $p(x=0 \mid y=0) = 0.25/0.375 = 2/3$,
    $p(x=1 \mid y=0) = 0.125/0.375 = 1/3$.

    Conditional distribution $p(x \mid y=1)$: $p(x=0 \mid y=1) = 0.25/0.625 = 2/5$,
    $p(x=1 \mid y=1) = 0.375/0.625 = 3/5$.

    $$
    H(X \mid Y) = -p(y=0)\bigl[\tfrac{2}{3}\log_2\tfrac{2}{3} + \tfrac{1}{3}\log_2\tfrac{1}{3}\bigr] - p(y=1)\bigl[\tfrac{2}{5}\log_2\tfrac{2}{5} + \tfrac{3}{5}\log_2\tfrac{3}{5}\bigr]
    $$

    $$
    = -0.375 \times (-0.9183) - 0.625 \times (-0.9710) \approx 0.3444 + 0.6069 = 0.9513 \text{ bits}
    $$

---

**Exercise 2.**
Prove that $\mathrm{VI}(X; Y) = 0$ if and only if $X = Y$ (i.e., the two
clusterings assign the same label to every point, up to relabeling).

??? success "Solution to Exercise 2"
    $\mathrm{VI}(X; Y) = H(X \mid Y) + H(Y \mid X)$. Since conditional
    entropy is non-negative, $\mathrm{VI} = 0$ requires both $H(X \mid Y) = 0$
    and $H(Y \mid X) = 0$.

    $H(X \mid Y) = 0$ means that $X$ is a deterministic function of $Y$: knowing
    the $Y$-label of a point completely determines its $X$-label. Similarly,
    $H(Y \mid X) = 0$ means $Y$ is a deterministic function of $X$.

    If $X$ is a function of $Y$ and $Y$ is a function of $X$, then the two
    clusterings define the same partition of the data (they may use different
    label names, but the grouping is identical). Conversely, if $X = Y$ up to
    relabeling, then both conditional entropies are zero. $\square$

---

**Exercise 3.**
Write a function that computes the **mutual information** $I(X; Y)$ using the
same sparse matrix framework. Verify that $I(X; Y) = H(X) - H(X \mid Y)$.

??? success "Solution to Exercise 3"
    ```python
    def mutual_information(x, y):
        pxy = sparse.coo_matrix(
            (np.ones(x.size), (x.ravel(), y.ravel())), dtype=float
        ).tocsr()
        pxy.data /= np.sum(pxy.data)

        px = np.array(pxy.sum(axis=1)).ravel()
        py = np.array(pxy.sum(axis=0)).ravel()

        # H(X)
        hx = -np.sum(xlogx(px))
        # H(Y)
        hy = -np.sum(xlogx(py))
        # H(X, Y) from joint distribution
        hxy = -np.sum(xlogx(pxy.data))

        return hx + hy - hxy

    c1 = np.array([0, 0, 1, 1, 2, 2])
    c2 = np.array([0, 0, 1, 1, 2, 2])
    print(mutual_information(c1, c2))  # H(X), since X = Y
    ```

    To verify $I(X; Y) = H(X) - H(X \mid Y)$: from the definitions,

    $$
    I(X; Y) = H(X) + H(Y) - H(X, Y)
    $$

    and $H(X \mid Y) = H(X, Y) - H(Y)$, so $H(X) - H(X \mid Y) = H(X) - H(X, Y) + H(Y) = I(X; Y)$.

---

**Exercise 4.**
Explain why COO format is preferred for constructing the joint distribution
matrix, while CSR format is preferred for the subsequent arithmetic. Under what
conditions would CSC format be more efficient than CSR for the VI computation?

??? success "Solution to Exercise 4"
    **COO for construction**: COO stores each entry as an independent
    `(row, col, value)` triple, so duplicate entries (multiple data points with
    the same cluster pair) are simply appended. The conversion to CSR then
    sums duplicates automatically. Building directly in CSR would require
    pre-sorting or incremental insertion, both of which are slower.

    **CSR for arithmetic**: CSR stores rows contiguously, making row-based
    operations (row slicing, row sums via `sum(axis=1)`, and left-multiplication
    by diagonal matrices) efficient. The VI computation relies heavily on these
    row operations.

    **When CSC would be better**: if the computation were restructured to
    primarily use column operations (column sums via `sum(axis=0)`, right-multiplication
    by diagonal matrices), CSC would be faster. In the current VI implementation,
    column sums are computed once for $p(y)$, but the dominant cost is in the
    matrix products, which favor CSR when the left factor is the sparse joint
    distribution.
