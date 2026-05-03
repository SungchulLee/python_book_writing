# Sparse Eigenvalues

`scipy.sparse.linalg` provides eigensolvers for large sparse matrices.

!!! tip "Mental Model"
    When your matrix has millions of rows but you only need a handful of eigenvalues, sparse eigensolvers like `eigs` and `eigsh` use iterative methods (Arnoldi/Lanczos) that never form the full matrix. You trade the ability to find all eigenvalues for the ability to find a few eigenvalues of matrices far too large for dense solvers.

## eigs - General Sparse

### 1. Basic Usage

```python
import numpy as np
from scipy import sparse
from scipy.sparse import linalg as splinalg

def main():
    # Large sparse matrix
    n = 1000
    A = sparse.diags([-1, 2, -1], [-1, 0, 1], shape=(n, n), format='csr')
    
    # Find 6 largest eigenvalues
    eigenvalues, eigenvectors = splinalg.eigs(A, k=6)
    
    print("6 largest eigenvalues:")
    print(eigenvalues)

if __name__ == "__main__":
    main()
```

### 2. Which Eigenvalues

```python
import numpy as np
from scipy import sparse
from scipy.sparse import linalg as splinalg

def main():
    n = 100
    A = sparse.diags([-1, 2, -1], [-1, 0, 1], shape=(n, n), format='csr')
    
    # 'LM' - largest magnitude (default)
    vals_LM, _ = splinalg.eigs(A, k=3, which='LM')
    
    # 'SM' - smallest magnitude
    vals_SM, _ = splinalg.eigs(A, k=3, which='SM')
    
    # 'LR' - largest real part
    vals_LR, _ = splinalg.eigs(A, k=3, which='LR')
    
    print("Largest magnitude:", vals_LM)
    print("Smallest magnitude:", vals_SM)
    print("Largest real:", vals_LR)

if __name__ == "__main__":
    main()
```

## eigsh - Symmetric Sparse

### 1. Basic Usage

```python
import numpy as np
from scipy import sparse
from scipy.sparse import linalg as splinalg

def main():
    n = 1000
    A = sparse.diags([-1, 2, -1], [-1, 0, 1], shape=(n, n), format='csr')
    
    # For symmetric matrices - faster
    eigenvalues, eigenvectors = splinalg.eigsh(A, k=6)
    
    print("6 eigenvalues (real, sorted):")
    print(eigenvalues)

if __name__ == "__main__":
    main()
```

### 2. Smallest Eigenvalues

```python
import numpy as np
from scipy import sparse
from scipy.sparse import linalg as splinalg

def main():
    n = 100
    A = sparse.diags([-1, 2, -1], [-1, 0, 1], shape=(n, n), format='csr')
    
    # Smallest algebraic eigenvalues
    vals_SA, _ = splinalg.eigsh(A, k=3, which='SA')
    
    # Largest algebraic eigenvalues
    vals_LA, _ = splinalg.eigsh(A, k=3, which='LA')
    
    print("Smallest:", vals_SA)
    print("Largest:", vals_LA)

if __name__ == "__main__":
    main()
```

## Applications

### 1. Graph Laplacian Spectrum

```python
import numpy as np
from scipy import sparse
from scipy.sparse import linalg as splinalg

def main():
    # Random sparse graph
    np.random.seed(42)
    n = 500
    A = sparse.random(n, n, density=0.02, format='csr')
    A = (A + A.T) / 2  # Symmetric
    A.data[:] = 1  # Binary
    
    # Laplacian
    D = sparse.diags(np.array(A.sum(axis=1)).flatten())
    L = D - A
    
    # Find smallest eigenvalues
    vals, vecs = splinalg.eigsh(L, k=10, which='SM')
    
    print("Smallest Laplacian eigenvalues:")
    print(vals)

if __name__ == "__main__":
    main()
```

### 2. Spectral Clustering

```python
import numpy as np
from scipy import sparse
from scipy.sparse import linalg as splinalg

def main():
    n = 200
    A = sparse.random(n, n, density=0.1, format='csr')
    A = (A + A.T) / 2
    
    D = sparse.diags(np.array(A.sum(axis=1)).flatten())
    L = D - A
    
    # Second smallest eigenvector for 2-way partition
    vals, vecs = splinalg.eigsh(L, k=2, which='SM')
    fiedler = vecs[:, 1]
    
    partition = fiedler > 0
    print(f"Partition sizes: {partition.sum()}, {(~partition).sum()}")

if __name__ == "__main__":
    main()
```

## Summary

| Function | Description |
|:---------|:------------|
| `splinalg.eigs(A, k)` | k eigenvalues of sparse A |
| `splinalg.eigsh(A, k)` | k eigenvalues of symmetric sparse A |
| `which='LM'` | Largest magnitude |
| `which='SM'` | Smallest magnitude |
| `which='SA'` | Smallest algebraic (eigsh) |

---

## Runnable Example: `spectral_methods_example.py`

```python
"""
Spectral Methods with Sparse Eigenvalue Problems - Linear Algebra Foundations
Exploring Laplacian matrices, sparse eigenvalue decomposition, and spectral
analysis techniques using scipy.sparse.linalg.eigsh() and eigendecomposition.
Run this file to see spectral methods in action!
"""

import numpy as np
from scipy import sparse
from scipy import linalg

if __name__ == "__main__":

    print("=" * 70)
    print("SPECTRAL METHODS WITH SPARSE EIGENVALUE PROBLEMS")
    print("=" * 70)

    # ============================================================================
    # EXAMPLE 1: Building Laplacian Matrix from Adjacency Matrix
    # ============================================================================
    print("\n1. CONSTRUCTING LAPLACIAN MATRIX FROM ADJACENCY MATRIX")
    print("-" * 70)

    # Adjacency matrix represents connections in a graph
    # Element A[i,j] = 1 if node i connects to node j, 0 otherwise
    A = np.array([
        [0, 1, 1, 0],
        [1, 0, 1, 1],
        [1, 1, 0, 1],
        [0, 1, 1, 0]
    ], dtype=float)

    print("Adjacency matrix A (4 nodes):")
    print(A)

    # Degree matrix D: diagonal matrix with degrees on diagonal
    # degree[i] = sum of connections from node i
    degrees = np.sum(A, axis=0)
    print("\nDegree of each node:", degrees)

    # Laplacian L = D - A (undirected case)
    D = np.diag(degrees)
    L = D - A

    print("\nDegree matrix D:")
    print(D)
    print("\nLaplacian matrix L = D - A:")
    print(L)

    # ============================================================================
    # EXAMPLE 2: Making Graph Undirected and Symmetric
    # ============================================================================
    print("\n2. SYMMETRIZING ADJACENCY MATRIX FOR UNDIRECTED GRAPHS")
    print("-" * 70)

    # If the graph is undirected but stored asymmetrically, symmetrize it
    A_asymmetric = np.array([
        [0, 1, 0, 0],
        [0, 0, 1, 1],
        [1, 1, 0, 1],
        [0, 0, 0, 0]
    ], dtype=float)

    print("Asymmetric adjacency matrix:")
    print(A_asymmetric)

    # Make symmetric by averaging: C = (A + A^T) / 2
    C = (A_asymmetric + A_asymmetric.T) / 2
    print("\nSymmetrized: C = (A + A^T) / 2:")
    print(C)

    # ============================================================================
    # EXAMPLE 3: Constructing Normalized Laplacian
    # ============================================================================
    print("\n3. NORMALIZED LAPLACIAN MATRIX")
    print("-" * 70)

    # Normalized Laplacian: Q = D^(-1/2) L D^(-1/2)
    # This normalization is useful for spectral clustering
    n = C.shape[0]
    degrees_C = np.sum(C, axis=0)
    D_C = np.diag(degrees_C)

    # D^(-1/2) is the inverse square root of the degree matrix
    D_inv_sqrt = np.diag(1.0 / np.sqrt(degrees_C + 1e-10))  # add epsilon to avoid division by zero

    # Normalized Laplacian
    L_C = D_C - C
    Q = D_inv_sqrt @ L_C @ D_inv_sqrt

    print("Degrees:", degrees_C)
    print("\nNormalized Laplacian Q = D^(-1/2) L D^(-1/2):")
    print(Q)

    # ============================================================================
    # EXAMPLE 4: Computing Eigenvalues with Sparse Matrices
    # ============================================================================
    print("\n4. EIGENDECOMPOSITION: SPARSE MATRIX VERSION")
    print("-" * 70)

    # Convert to sparse format for efficiency (especially important for large matrices)
    L_sparse = sparse.csr_matrix(L_C)
    Q_sparse = sparse.csr_matrix(Q)

    print("Dense Laplacian shape:", L_C.shape)
    print("Sparse Laplacian non-zero elements:", L_sparse.nnz)

    # For small matrices, use dense eigsh; for large use sparse.linalg.eigsh
    # Dense eigendecomposition (good for comparison and understanding)
    eigvals_dense, eigvecs_dense = linalg.eigh(Q)
    print("\nEigenvalues (full, sorted ascending):")
    print(eigvals_dense)

    # Get eigenvectors sorted by eigenvalue
    idx_sorted = np.argsort(eigvals_dense)
    eigvals_sorted = eigvals_dense[idx_sorted]
    eigvecs_sorted = eigvecs_dense[:, idx_sorted]

    print("\nSmallest 2 eigenvalues:", eigvals_sorted[:2])
    print("Corresponding eigenvectors (first 2):")
    print(eigvecs_sorted[:, :2])

    # ============================================================================
    # EXAMPLE 5: Sparse Eigenvalue Solver - eigsh()
    # ============================================================================
    print("\n5. SPARSE EIGENVALUE SOLVER: scipy.sparse.linalg.eigsh()")
    print("-" * 70)

    # eigsh() finds k smallest (or largest) eigenvalues of sparse symmetric matrix
    # k: number of eigenvalues to compute
    # which='SM' means smallest magnitude
    try:
        # Request k=2 smallest eigenvalues
        eigvals_sparse, eigvecs_sparse = sparse.linalg.eigsh(
            Q_sparse, k=2, which='SM', tol=1e-5
        )
        print("Using sparse.linalg.eigsh() for k=2 smallest eigenvalues:")
        print("Eigenvalues:", eigvals_sparse)
        print("Eigenvector shape:", eigvecs_sparse.shape)
        print("First eigenvector (constant - shows overall structure):")
        print(eigvecs_sparse[:, 0])
        print("\nSecond eigenvector (spectral ordering):")
        print(eigvecs_sparse[:, 1])
    except Exception as e:
        print("Note: eigsh() for very small matrices may raise exception")
        print("Using dense eigendecomposition instead for demonstration")

    # ============================================================================
    # EXAMPLE 6: Spectral Ordering Using Second Eigenvector
    # ============================================================================
    print("\n6. SPECTRAL ORDERING - EMBEDDING NODES IN 1D")
    print("-" * 70)

    # The second eigenvector (Fiedler vector) provides optimal 1D ordering of nodes
    # Nodes are ordered by their coordinate in this eigenvector space
    x_coords = eigvecs_sorted[:, 1]  # second eigenvector
    print("Spectral coordinates (second eigenvector):")
    for i, coord in enumerate(x_coords):
        print(f"  Node {i}: position {coord:.4f}")

    # Sort nodes by this coordinate
    node_order = np.argsort(x_coords)
    print("\nNodes sorted by spectral position:")
    print("  Order:", node_order)
    print("  This ordering can reveal graph structure and community organization")

    # ============================================================================
    # EXAMPLE 7: Pseudoinverse for Solving Linear Systems
    # ============================================================================
    print("\n7. PSEUDOINVERSE: SOLVING ILL-CONDITIONED SYSTEMS")
    print("-" * 70)

    # The Laplacian is singular (rank = n-1 for connected graphs)
    # Its pseudoinverse can solve related problems
    print("Laplacian rank:", np.linalg.matrix_rank(L_C))
    print("Expected rank (n-1):", n - 1)

    # Compute pseudoinverse using linalg.pinv
    L_pinv = linalg.pinv(L_C)
    print("\nPseudoinverse shape:", L_pinv.shape)
    print("L @ L_pinv @ L ≈ L (pseudoinverse property):")
    reconstruction = L_C @ L_pinv @ L_C
    error = np.max(np.abs(reconstruction - L_C))
    print(f"Max reconstruction error: {error:.2e}")

    # ============================================================================
    # EXAMPLE 8: 2D Spectral Embedding Using Multiple Eigenvectors
    # ============================================================================
    print("\n8. SPECTRAL EMBEDDING: EMBEDDING IN 2D SPACE")
    print("-" * 70)

    # Use the 2nd and 3rd eigenvectors for 2D embedding
    x_2d = D_inv_sqrt @ eigvecs_sorted[:, 1]
    y_2d = D_inv_sqrt @ eigvecs_sorted[:, 2]

    print("2D spectral coordinates for each node:")
    for i in range(n):
        print(f"  Node {i}: ({x_2d[i]:7.4f}, {y_2d[i]:7.4f})")

    print("\nThese coordinates reflect graph topology:")
    print("- Similar graph positions map to similar coordinates")
    print("- Can be visualized as a 2D plot")
    print("- Useful for spectral clustering and visualization")

    # ============================================================================
    # EXAMPLE 9: Spectral Properties Analysis
    # ============================================================================
    print("\n9. INTERPRETING SPECTRAL PROPERTIES")
    print("-" * 70)

    # Eigenvalue properties tell us about graph structure
    print("Graph spectral analysis:")
    print(f"  Smallest eigenvalue (λ₁): {eigvals_sorted[0]:.6f}")
    print(f"  Second eigenvalue (λ₂): {eigvals_sorted[1]:.6f}")
    print(f"  Spectral gap (λ₂ - λ₁): {eigvals_sorted[1] - eigvals_sorted[0]:.6f}")

    print("\nInterpretation:")
    print("  λ₁ = 0: Always true for normalized Laplacian")
    print("  λ₂ > 0: Graph is connected")
    print("  Larger λ₂: Graph is more 'well-mixed' (faster mixing)")
    print("  Smaller λ₂: Graph may have community structure")

    # ============================================================================
    # EXAMPLE 10: Large Sparse Graph Example
    # ============================================================================
    print("\n10. PRACTICAL EXAMPLE: LARGER SPARSE GRAPH")
    print("-" * 70)

    # Create a larger sparse graph: ring network
    n_large = 100
    # Ring topology: each node connects to neighbors
    A_ring = np.zeros((n_large, n_large))
    for i in range(n_large):
        A_ring[i, (i-1) % n_large] = 1
        A_ring[i, (i+1) % n_large] = 1

    print(f"Ring graph with {n_large} nodes")
    print(f"Adjacency matrix density: {np.count_nonzero(A_ring) / (n_large**2):.4%}")

    # Convert to sparse
    A_ring_sparse = sparse.csr_matrix(A_ring)

    # Compute Laplacian
    D_ring = sparse.diags(np.array(A_ring_sparse.sum(axis=1)).ravel())
    L_ring = D_ring - A_ring_sparse

    # Compute normalized Laplacian
    D_inv_sqrt_ring = sparse.diags(1.0 / np.sqrt(np.array(D_ring.diagonal())))
    Q_ring = D_inv_sqrt_ring @ L_ring @ D_inv_sqrt_ring

    print(f"Sparse Laplacian non-zeros: {L_ring.nnz}")

    # Use sparse eigsh for efficiency
    try:
        eigvals_ring, eigvecs_ring = sparse.linalg.eigsh(Q_ring, k=3, which='SM')
        print(f"\nSmallest 3 eigenvalues of ring graph: {eigvals_ring}")
        print("Ring graphs have predictable spectral structure (cosine-like)")
    except Exception:
        # Fallback to dense for very small
        eigvals_ring = np.linalg.eigvalsh(Q_ring.todense())
        print(f"Eigenvalues: {eigvals_ring[:3]}")

    print("\n" + "=" * 70)
    print("Key takeaways:")
    print("- Laplacian L = D - A captures graph structure in matrix form")
    print("- Normalized Laplacian: Q = D^(-1/2) L D^(-1/2)")
    print("- Eigenvalues and eigenvectors reveal graph properties")
    print("- eigsh() efficiently solves sparse eigenvalue problems")
    print("- Fiedler vector (2nd eigenvector) provides optimal 1D ordering")
    print("- Spectral methods bridge linear algebra and graph structure")
    print("=" * 70)
```

---

## Exercises

**Exercise 1.**
Create a $2000 \times 2000$ sparse symmetric tridiagonal matrix with 2 on the diagonal and -1 on the sub/super-diagonals. Use `eigsh` to find the 5 largest and 5 smallest eigenvalues. Print them and verify the smallest eigenvalue is positive (the matrix is positive definite).

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import sparse
        from scipy.sparse import linalg as splinalg

        n = 2000
        A = sparse.diags([-1, 2, -1], [-1, 0, 1], shape=(n, n), format='csr')

        vals_large, _ = splinalg.eigsh(A, k=5, which='LA')
        vals_small, _ = splinalg.eigsh(A, k=5, which='SA')

        print("5 largest eigenvalues:", np.sort(vals_large)[::-1])
        print("5 smallest eigenvalues:", np.sort(vals_small))
        print(f"Smallest eigenvalue positive: {np.min(vals_small) > 0}")

---

**Exercise 2.**
Build a sparse adjacency matrix for a ring graph with 500 nodes (each node connected to its two neighbors). Construct the graph Laplacian and use `eigsh` to compute the 4 smallest eigenvalues. Verify that the smallest eigenvalue is approximately 0 (the graph is connected) and compare the second smallest with the analytical value $2(1 - \cos(2\pi/500))$.

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import sparse
        from scipy.sparse import linalg as splinalg

        n = 500
        row = list(range(n)) + list(range(n))
        col = [(i + 1) % n for i in range(n)] + [(i - 1) % n for i in range(n)]
        data = np.ones(2 * n)
        A = sparse.csr_matrix((data, (row, col)), shape=(n, n))

        D = sparse.diags(np.array(A.sum(axis=1)).flatten())
        L = D - A

        vals, _ = splinalg.eigsh(L.astype(float), k=4, which='SM')
        vals = np.sort(vals)
        print(f"4 smallest eigenvalues: {vals}")
        print(f"Smallest ~ 0: {np.isclose(vals[0], 0, atol=1e-10)}")

        analytical_2nd = 2 * (1 - np.cos(2 * np.pi / n))
        print(f"2nd smallest: {vals[1]:.8f}")
        print(f"Analytical:   {analytical_2nd:.8f}")

---

**Exercise 3.**
Generate a $1000 \times 1000$ sparse random matrix with density 0.01 using `sparse.random` and `np.random.seed(7)`. Make it symmetric by computing $(A + A^T)/2$, then add $2I$ to ensure positive definiteness. Use `eigs` (not `eigsh`) with `which='LM'` to find the 3 eigenvalues of largest magnitude. Print their values and magnitudes.

??? success "Solution to Exercise 3"
        import numpy as np
        from scipy import sparse
        from scipy.sparse import linalg as splinalg

        np.random.seed(7)
        A = sparse.random(1000, 1000, density=0.01, format='csr')
        A = (A + A.T) / 2
        A = A + 2 * sparse.eye(1000)

        vals, vecs = splinalg.eigs(A, k=3, which='LM')
        for v in vals:
            print(f"Eigenvalue: {v:.6f}, magnitude: {abs(v):.6f}")
