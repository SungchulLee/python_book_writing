# Block Matrices

Block matrices arise naturally when a system has multiple components that interact in a structured way — for example, coupled differential equations, multi-asset portfolio models, or finite element discretizations. A block diagonal matrix places smaller matrices along the diagonal with zeros elsewhere, preserving the independence of each block. SciPy provides both dense and sparse constructors for block diagonal matrices.

!!! tip "Mental Model"
    A block diagonal matrix is a collection of independent sub-problems stacked into one matrix. Its determinant, eigenvalues, and inverse all decompose into the corresponding quantities of each block. This structure lets you solve large systems by solving several small ones independently, which is both faster and more memory-efficient.

```python
import numpy as np
from scipy import linalg
```

---

## Block Diagonal Matrix

A block diagonal matrix has the form

$$
D = \begin{pmatrix} A_1 & 0 & \cdots & 0 \\ 0 & A_2 & \cdots & 0 \\ \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \cdots & A_k \end{pmatrix}
$$

where each $A_i$ is a square (or rectangular) matrix and all off-diagonal blocks are zero.

### Key Properties

- **Determinant**: $\det(D) = \det(A_1) \cdot \det(A_2) \cdots \det(A_k)$
- **Eigenvalues**: the eigenvalues of $D$ are the union of eigenvalues of each $A_i$
- **Inverse**: if each $A_i$ is invertible, then $D^{-1} = \mathrm{diag}(A_1^{-1}, A_2^{-1}, \ldots, A_k^{-1})$

### Construction with scipy.linalg.block_diag

`linalg.block_diag` takes any number of arrays and places them along the diagonal of a new matrix, filling the rest with zeros.

```python
def main():
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    C = np.array([[9]])

    D = linalg.block_diag(A, B, C)
    print(D)

if __name__ == "__main__":
    main()
```

```
[[1 2 0 0 0]
 [3 4 0 0 0]
 [0 0 5 6 0]
 [0 0 7 8 0]
 [0 0 0 0 9]]
```

The 2x2 block $A$ occupies the top-left corner, the 2x2 block $B$ is in the center, and the 1x1 block $C$ is in the bottom-right.

---

## Sparse Block Diagonal

For large-scale problems where the blocks are small relative to the total matrix size, the dense representation wastes memory storing zeros. The sparse variant `scipy.sparse.block_diag` returns a sparse matrix that stores only the nonzero entries.

```python
from scipy import sparse

def main():
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]

    D = sparse.block_diag([A, B])
    print(D.toarray())
    print(f"Format: {D.format}")
    print(f"Nonzeros: {D.nnz} out of {D.shape[0] * D.shape[1]} entries")

if __name__ == "__main__":
    main()
```

```
[[1 2 0 0]
 [3 4 0 0]
 [0 0 5 6]
 [0 0 7 8]]
Format: coo
Nonzeros: 8 out of 16 entries
```

!!! tip "When to Use Sparse"
    The sparse variant becomes worthwhile when the total matrix dimension is much larger than the individual block sizes. For a block diagonal with 100 blocks of size 3x3, the dense matrix is 300x300 (90,000 entries) but only 900 are nonzero — a 99% savings in memory.

---

## General Block Matrices with np.block

NumPy's `np.block` constructs arbitrary block matrices (not just block diagonal) from a nested list of arrays.

```python
A = np.ones((2, 2))
B = np.zeros((2, 3))
C = np.zeros((3, 2))
D = np.eye(3)

# 2x2 block structure
M = np.block([
    [A, B],
    [C, D]
])
print(M)
```

```
[[1. 1. 0. 0. 0.]
 [1. 1. 0. 0. 0.]
 [0. 0. 1. 0. 0.]
 [0. 0. 0. 1. 0.]
 [0. 0. 0. 0. 1.]]
```

The nested list structure mirrors the block layout: `[[top-left, top-right], [bottom-left, bottom-right]]`. The inner arrays must have compatible shapes along the concatenation axes.

---

## Summary

| Function | Purpose | Returns |
|----------|---------|---------|
| `scipy.linalg.block_diag(A, B, ...)` | Dense block diagonal matrix | NumPy array |
| `scipy.sparse.block_diag([A, B, ...])` | Sparse block diagonal matrix | Sparse matrix (COO) |
| `np.block([[A, B], [C, D]])` | General block matrix from nested list | NumPy array |

**Key Takeaways**:

- Block diagonal matrices preserve the eigenvalues, determinant, and invertibility structure of the individual blocks
- Use `scipy.linalg.block_diag` for small dense block diagonal matrices
- Use `scipy.sparse.block_diag` when the total size is large and memory matters
- Use `np.block` for general (non-diagonal) block matrix construction from a nested list of arrays

---

## Exercises

**Exercise 1.**
Create a block diagonal matrix from three blocks: $A = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$, $B = \begin{pmatrix} 5 \end{pmatrix}$, and $C = \begin{pmatrix} 6 & 7 & 8 \\ 9 & 10 & 11 \\ 12 & 13 & 14 \end{pmatrix}$. Verify that the determinant of the block diagonal matrix equals the product of determinants of the individual blocks.

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import linalg

        A = np.array([[1, 2], [3, 4]])
        B = np.array([[5]])
        C = np.array([[6, 7, 8], [9, 10, 11], [12, 13, 14]])

        D = linalg.block_diag(A, B, C)
        print("Block diagonal matrix:")
        print(D)

        det_D = np.linalg.det(D)
        det_product = np.linalg.det(A) * np.linalg.det(B) * np.linalg.det(C)
        print(f"\ndet(D) = {det_D:.6f}")
        print(f"det(A)*det(B)*det(C) = {det_product:.6f}")
        print(f"Match: {np.isclose(det_D, det_product)}")

---

**Exercise 2.**
Build a $2 \times 2$ block matrix (not block diagonal) using `np.block`: the top-left block is a $3 \times 3$ identity matrix, the top-right is a $3 \times 2$ matrix of ones, the bottom-left is a $2 \times 3$ matrix of zeros, and the bottom-right is a $2 \times 2$ matrix with 5 on the diagonal. Print the resulting $5 \times 5$ matrix and compute its eigenvalues.

??? success "Solution to Exercise 2"
        import numpy as np

        TL = np.eye(3)
        TR = np.ones((3, 2))
        BL = np.zeros((2, 3))
        BR = 5 * np.eye(2)

        M = np.block([[TL, TR], [BL, BR]])
        print("Block matrix:")
        print(M)

        eigenvalues = np.linalg.eigvals(M)
        print(f"\nEigenvalues: {eigenvalues}")

---

**Exercise 3.**
Create a sparse block diagonal matrix with 50 identical $2 \times 2$ blocks where each block is $\begin{pmatrix} 3 & 1 \\ 1 & 3 \end{pmatrix}$. Print the total matrix shape, number of nonzeros, and density. Then solve $Dx = b$ where $b$ is a vector of ones, and verify the solution is correct.

??? success "Solution to Exercise 3"
        import numpy as np
        from scipy import sparse
        from scipy.sparse import linalg as splinalg

        block = [[3, 1], [1, 3]]
        blocks = [block] * 50
        D = sparse.block_diag(blocks, format='csr')

        print(f"Shape: {D.shape}")
        print(f"Nonzeros: {D.nnz}")
        print(f"Density: {D.nnz / (D.shape[0] * D.shape[1]):.4%}")

        b = np.ones(D.shape[0])
        x = splinalg.spsolve(D, b)
        residual = np.linalg.norm(D @ x - b)
        print(f"Residual: {residual:.2e}")
