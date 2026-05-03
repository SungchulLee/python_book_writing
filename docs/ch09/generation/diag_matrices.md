# Diagonal Matrices

The `np.diag` function provides bidirectional conversion between diagonal components and diagonal matrices.

!!! tip "Mental Model"
    `np.diag` is a two-way street: give it a 1D array and it builds a matrix with those values on the diagonal; give it a 2D matrix and it extracts the diagonal as a 1D array. The `k` parameter lets you shift to super- or sub-diagonals, making it easy to construct tridiagonal and banded matrices.

    Together with [`np.eye` and `np.identity`](full_eye_identity.md), `diag` belongs
    to the **structured matrix** family — creation functions where mathematical
    structure (diagonal, banded, identity) is the point, not just filling values.

!!! note "Where Diagonal Matrices Appear"
    Diagonal and banded matrices are not just textbook constructs — they arise naturally in:

    - **Finite difference methods** — discretizing derivatives produces tridiagonal systems
    - **Eigenvalue decomposition** — diagonalizing a matrix isolates its eigenvalues on the diagonal
    - **Sparse linear algebra** — banded structure enables O(n) solvers instead of O(n^3)
    - **Covariance matrices** — uncorrelated variables produce a diagonal covariance matrix

    The `k` parameter in `np.diag` makes it easy to build these structures directly.


## Core Concept

`np.diag` works in two directions depending on input dimensionality.

$$
\text{diagonal components}
\quad\stackrel{\text{np.diag}}{\longleftrightarrow}\quad
\text{diagonal matrix}
$$


## Components to Matrix

Convert a 1D array of diagonal values into a 2D diagonal matrix.

### 1. Basic Conversion

```python
import numpy as np

def main():
    a = np.diag([1, 2, 3])
    print("np.diag([1, 2, 3])")
    print(a)

if __name__ == "__main__":
    main()
```

Output:

```
np.diag([1, 2, 3])
[[1 0 0]
 [0 2 0]
 [0 0 3]]
```

### 2. Input Requirements

The input must be a 1D array or list of diagonal values.


## Diagonal Offset

The `k` parameter shifts the diagonal position.

### 1. Main Diagonal

```python
import numpy as np

def main():
    a = np.diag([1, 2, 3])
    print("np.diag([1, 2, 3])")
    print(a)

if __name__ == "__main__":
    main()
```

Default `k=0` places values on the main diagonal.

### 2. Upper Diagonals

```python
import numpy as np

def main():
    a = np.diag([1, 2, 3], k=1)
    print("np.diag([1, 2, 3], k=1)")
    print(a)
    
    a = np.diag([1, 2, 3], k=2)
    print("np.diag([1, 2, 3], k=2)")
    print(a)

if __name__ == "__main__":
    main()
```

Output:

```
np.diag([1, 2, 3], k=1)
[[0 1 0 0]
 [0 0 2 0]
 [0 0 0 3]
 [0 0 0 0]]

np.diag([1, 2, 3], k=2)
[[0 0 1 0 0]
 [0 0 0 2 0]
 [0 0 0 0 3]
 [0 0 0 0 0]
 [0 0 0 0 0]]
```

### 3. Lower Diagonals

```python
import numpy as np

def main():
    a = np.diag([1, 2, 3], k=-1)
    print("np.diag([1, 2, 3], k=-1)")
    print(a)
    
    a = np.diag([1, 2, 3], k=-2)
    print("np.diag([1, 2, 3], k=-2)")
    print(a)

if __name__ == "__main__":
    main()
```

Negative `k` shifts the diagonal below the main diagonal.


## Matrix to Components

Extract diagonal values from a 2D matrix.

### 1. Extract Main Diagonal

```python
import numpy as np

def main():
    A = np.array([[1, 4, 0],
                  [0, 2, 5],
                  [0, 0, 3]])
    
    print(f'{np.diag(A) = }')

if __name__ == "__main__":
    main()
```

Output:

```
np.diag(A) = array([1, 2, 3])
```

### 2. Extract Off-Diagonals

```python
import numpy as np

def main():
    A = np.array([[1, 4, 0],
                  [0, 2, 5],
                  [0, 0, 3]])
    
    print(f'{np.diag(A, k=1) = }')
    print(f'{np.diag(A, k=-1) = }')

if __name__ == "__main__":
    main()
```

Output:

```
np.diag(A, k=1) = array([4, 5])
np.diag(A, k=-1) = array([0, 0])
```


## Visual Geometry

Diagonal matrices have a distinctive visual pattern.

### 1. Visualization Code

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    a = np.diag(range(15))
    
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.imshow(a, cmap='Blues')
    ax.axis('off')
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Pattern Recognition

Non-zero values appear only along a single diagonal line.


## Linear Algebra Role

Diagonal matrices have special computational properties.

### 1. Easy Inversion

The inverse of a diagonal matrix is simply the reciprocal of each diagonal element.

### 2. Eigenvalues

The eigenvalues of a diagonal matrix are its diagonal elements.

### 3. Matrix Powers

$D^n$ is computed by raising each diagonal element to the $n$-th power.

---

## Exercises

**Exercise 1.**
Create a 5x5 tridiagonal matrix with `[1, 2, 3, 4, 5]` on the main diagonal, `[10, 20, 30, 40]` on the first upper diagonal (`k=1`), and `[-1, -2, -3, -4]` on the first lower diagonal (`k=-1`). Use `np.diag` three times and add the results.

??? success "Solution to Exercise 1"

        import numpy as np

        main = np.diag([1, 2, 3, 4, 5])
        upper = np.diag([10, 20, 30, 40], k=1)
        lower = np.diag([-1, -2, -3, -4], k=-1)
        tridiag = main + upper + lower
        print(tridiag)

---

**Exercise 2.**
Given a 4x4 matrix `A = np.arange(16).reshape(4, 4)`, extract the main diagonal, the first upper diagonal (`k=1`), and the first lower diagonal (`k=-1`). Print all three and verify that the main diagonal has 4 elements while the off-diagonals have 3 each.

??? success "Solution to Exercise 2"

        import numpy as np

        A = np.arange(16).reshape(4, 4)
        print(f"Main diagonal (k=0): {np.diag(A)}")       # 4 elements
        print(f"Upper diagonal (k=1): {np.diag(A, k=1)}")  # 3 elements
        print(f"Lower diagonal (k=-1): {np.diag(A, k=-1)}")# 3 elements

---

**Exercise 3.**
Create a 6x6 diagonal matrix `D` with diagonal values `[2, 4, 6, 8, 10, 12]`. Compute its inverse by taking the reciprocal of each diagonal element (using `np.diag` to extract and reconstruct). Verify that `D @ D_inv` equals the identity matrix.

??? success "Solution to Exercise 3"

        import numpy as np

        diag_vals = np.array([2, 4, 6, 8, 10, 12], dtype=float)
        D = np.diag(diag_vals)
        D_inv = np.diag(1.0 / diag_vals)
        product = D @ D_inv
        print(f"D @ D_inv is identity: {np.allclose(product, np.eye(6))}")
