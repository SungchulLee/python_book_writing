# Singular Value Decomposition

SVD factorizes any matrix into orthogonal components.

!!! tip "Mental Model"
    SVD decomposes any matrix $A$ into $U \Sigma V^T$, where $U$ and $V$ are rotations and $\Sigma$ is a diagonal of scaling factors (singular values). The singular values tell you how much "signal" each component carries. Truncating to the top $k$ singular values gives the best rank-$k$ approximation -- the basis of PCA, image compression, and noise reduction.

!!! note "SVD in Machine Learning and Data Science"
    SVD is the computational backbone behind many ML techniques:

    - **PCA**: projecting data onto the top singular vectors
    - **Linear regression**: `lstsq` uses SVD internally for numerical stability
    - **Recommender systems**: low-rank matrix factorization of user-item matrices
    - **Natural language processing**: latent semantic analysis (LSA)
    - **Neural networks**: weight initialization and analyzing layer Jacobians

    If you learn one decomposition deeply, make it SVD — it is the most general
    factorization and the one you will encounter most often in practice.

## np.linalg.svd

### 1. Basic Usage

```python
import numpy as np

def main():
    A = np.array([[1, 2],
                  [3, 4],
                  [5, 6]])
    
    U, s, Vt = np.linalg.svd(A)
    
    print(f"A shape: {A.shape}")
    print(f"U shape: {U.shape}")
    print(f"s shape: {s.shape}")
    print(f"Vt shape: {Vt.shape}")
    print()
    print(f"Singular values: {s}")

if __name__ == "__main__":
    main()
```

### 2. Mathematical Form

$$A = U \Sigma V^T$$

- $U$: Left singular vectors (orthogonal)
- $\Sigma$: Diagonal matrix of singular values
- $V^T$: Right singular vectors (orthogonal)

### 3. Reconstruct Matrix

```python
import numpy as np

def main():
    A = np.array([[1, 2],
                  [3, 4],
                  [5, 6]])
    
    U, s, Vt = np.linalg.svd(A)
    
    # Reconstruct: A = U @ Sigma @ Vt
    Sigma = np.zeros((U.shape[0], Vt.shape[0]))
    np.fill_diagonal(Sigma, s)
    
    A_reconstructed = U @ Sigma @ Vt
    
    print("Original A:")
    print(A)
    print()
    print("Reconstructed:")
    print(A_reconstructed.round(10))

if __name__ == "__main__":
    main()
```

## Reduced SVD

### 1. full_matrices=False

```python
import numpy as np

def main():
    A = np.array([[1, 2],
                  [3, 4],
                  [5, 6]])
    
    # Full SVD
    U_full, s, Vt_full = np.linalg.svd(A, full_matrices=True)
    print("Full SVD:")
    print(f"  U: {U_full.shape}, Vt: {Vt_full.shape}")
    
    # Reduced SVD
    U_red, s, Vt_red = np.linalg.svd(A, full_matrices=False)
    print("Reduced SVD:")
    print(f"  U: {U_red.shape}, Vt: {Vt_red.shape}")

if __name__ == "__main__":
    main()
```

### 2. Memory Efficiency

Reduced SVD is more memory efficient for tall/wide matrices.

### 3. Simpler Reconstruction

```python
import numpy as np

def main():
    A = np.array([[1, 2],
                  [3, 4],
                  [5, 6]])
    
    U, s, Vt = np.linalg.svd(A, full_matrices=False)
    
    # Simpler reconstruction with reduced SVD
    A_reconstructed = U @ np.diag(s) @ Vt
    
    print("Reconstructed:")
    print(A_reconstructed.round(10))

if __name__ == "__main__":
    main()
```

## Low-Rank Approximation

### 1. Truncated SVD

Keep only top k singular values.

```python
import numpy as np

def main():
    np.random.seed(42)
    A = np.random.randn(5, 4)
    
    U, s, Vt = np.linalg.svd(A, full_matrices=False)
    
    print(f"Singular values: {s.round(3)}")
    
    # Rank-2 approximation
    k = 2
    A_approx = U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :]
    
    error = np.linalg.norm(A - A_approx, 'fro')
    print(f"Approximation error: {error:.4f}")

if __name__ == "__main__":
    main()
```

### 2. Optimal Approximation

SVD gives the best rank-k approximation (Eckart-Young theorem).

```python
import numpy as np

def main():
    np.random.seed(42)
    A = np.random.randn(10, 8)
    
    U, s, Vt = np.linalg.svd(A, full_matrices=False)
    
    print("Rank | Error")
    print("-" * 20)
    
    for k in range(1, len(s) + 1):
        A_k = U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :]
        error = np.linalg.norm(A - A_k, 'fro')
        print(f"  {k}  | {error:.4f}")

if __name__ == "__main__":
    main()
```

### 3. Compression Ratio

```python
import numpy as np

def main():
    m, n = 100, 80
    A = np.random.randn(m, n)
    
    U, s, Vt = np.linalg.svd(A, full_matrices=False)
    
    original_size = m * n
    
    print("Rank | Compressed Size | Ratio | Error")
    print("-" * 50)
    
    for k in [5, 10, 20, 40]:
        compressed_size = k * (m + n + 1)
        ratio = compressed_size / original_size
        A_k = U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :]
        error = np.linalg.norm(A - A_k, 'fro') / np.linalg.norm(A, 'fro')
        print(f" {k:3} | {compressed_size:15} | {ratio:.2%} | {error:.4f}")

if __name__ == "__main__":
    main()
```

## Properties

### 1. Singular Values

Always non-negative and sorted descending.

```python
import numpy as np

def main():
    A = np.array([[1, 2, 3],
                  [4, 5, 6]])
    
    U, s, Vt = np.linalg.svd(A)
    
    print(f"Singular values: {s}")
    print(f"All non-negative: {np.all(s >= 0)}")
    print(f"Sorted descending: {np.all(np.diff(s) <= 0)}")

if __name__ == "__main__":
    main()
```

### 2. Matrix Rank

Count non-zero singular values.

```python
import numpy as np

def main():
    # Rank-deficient matrix
    A = np.array([[1, 2, 3],
                  [2, 4, 6],
                  [1, 2, 3]])
    
    U, s, Vt = np.linalg.svd(A)
    
    print(f"Singular values: {s}")
    
    rank = np.sum(s > 1e-10)
    print(f"Numerical rank: {rank}")
    print(f"np.linalg.matrix_rank: {np.linalg.matrix_rank(A)}")

if __name__ == "__main__":
    main()
```

### 3. Condition Number

Ratio of largest to smallest singular value.

```python
import numpy as np

def main():
    A = np.array([[1, 2],
                  [3, 4]])
    
    U, s, Vt = np.linalg.svd(A)
    
    cond_svd = s[0] / s[-1]
    cond_numpy = np.linalg.cond(A)
    
    print(f"Singular values: {s}")
    print(f"Condition (σ_max/σ_min): {cond_svd:.4f}")
    print(f"np.linalg.cond: {cond_numpy:.4f}")

if __name__ == "__main__":
    main()
```

## Applications

### 1. Image Compression

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    np.random.seed(42)
    
    # Simulated grayscale image
    img = np.random.randn(100, 100)
    img = np.cumsum(np.cumsum(img, axis=0), axis=1)
    img = (img - img.min()) / (img.max() - img.min())
    
    U, s, Vt = np.linalg.svd(img, full_matrices=False)
    
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    
    axes[0].imshow(img, cmap='gray')
    axes[0].set_title('Original')
    
    for ax, k in zip(axes[1:], [5, 20, 50]):
        img_k = U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :]
        ax.imshow(img_k, cmap='gray')
        ax.set_title(f'Rank {k}')
    
    for ax in axes:
        ax.axis('off')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Pseudoinverse

```python
import numpy as np

def main():
    A = np.array([[1, 2],
                  [3, 4],
                  [5, 6]])
    
    U, s, Vt = np.linalg.svd(A, full_matrices=False)
    
    # Pseudoinverse: V @ S^(-1) @ U^T
    s_inv = 1 / s
    A_pinv_svd = Vt.T @ np.diag(s_inv) @ U.T
    
    A_pinv_numpy = np.linalg.pinv(A)
    
    print("Pseudoinverse via SVD:")
    print(A_pinv_svd.round(4))
    print()
    print("np.linalg.pinv:")
    print(A_pinv_numpy.round(4))

if __name__ == "__main__":
    main()
```

### 3. Latent Semantic Analysis

```python
import numpy as np

def main():
    # Term-document matrix (simplified)
    # Rows: terms, Columns: documents
    A = np.array([[1, 0, 1, 0],
                  [0, 1, 0, 1],
                  [1, 1, 0, 0],
                  [0, 0, 1, 1],
                  [1, 0, 0, 1]])
    
    U, s, Vt = np.linalg.svd(A, full_matrices=False)
    
    print("Singular values:", s.round(3))
    print()
    
    # Reduce to 2 dimensions
    k = 2
    term_vectors = U[:, :k] @ np.diag(s[:k])
    doc_vectors = Vt[:k, :].T @ np.diag(s[:k])
    
    print("Term vectors (2D):")
    print(term_vectors.round(3))
    print()
    print("Document vectors (2D):")
    print(doc_vectors.round(3))

if __name__ == "__main__":
    main()
```

## scipy Alternative

### 1. Truncated SVD

More efficient for large sparse matrices.

```python
import numpy as np
from scipy.sparse.linalg import svds

def main():
    np.random.seed(42)
    A = np.random.randn(100, 80)
    
    # Compute only top 5 singular values
    U, s, Vt = svds(A, k=5)
    
    print(f"U shape: {U.shape}")
    print(f"s: {s}")
    print(f"Vt shape: {Vt.shape}")

if __name__ == "__main__":
    main()
```

### 2. Randomized SVD

```python
import numpy as np
from sklearn.decomposition import TruncatedSVD

def main():
    np.random.seed(42)
    A = np.random.randn(1000, 500)
    
    svd = TruncatedSVD(n_components=10)
    A_transformed = svd.fit_transform(A)
    
    print(f"Singular values: {svd.singular_values_}")
    print(f"Explained variance ratio: {svd.explained_variance_ratio_.sum():.4f}")

if __name__ == "__main__":
    main()
```

### 3. When to Use Each

- `np.linalg.svd`: Full SVD, small/medium matrices
- `scipy.sparse.linalg.svds`: Truncated SVD, sparse matrices
- `sklearn.decomposition.TruncatedSVD`: Randomized, very large matrices

---

## Exercises

**Exercise 1.**
Compute the SVD of `A = np.array([[1, 2], [3, 4], [5, 6]])`. Reconstruct `A` from `U`, `s`, and `Vt` by forming `U[:, :2] @ np.diag(s) @ Vt`. Verify the reconstruction matches `A`.

??? success "Solution to Exercise 1"

        import numpy as np

        A = np.array([[1, 2], [3, 4], [5, 6]], dtype=float)
        U, s, Vt = np.linalg.svd(A)
        A_reconstructed = U[:, :2] @ np.diag(s) @ Vt
        print(f"Match: {np.allclose(A, A_reconstructed)}")

---

**Exercise 2.**
Use SVD to compute a rank-1 approximation of `A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])`. Keep only the first singular value and its corresponding vectors. Compute the approximation error as the Frobenius norm of the difference.

??? success "Solution to Exercise 2"

        import numpy as np

        A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=float)
        U, s, Vt = np.linalg.svd(A)

        # Rank-1 approximation
        A_rank1 = s[0] * np.outer(U[:, 0], Vt[0, :])
        error = np.linalg.norm(A - A_rank1, 'fro')
        print(f"Rank-1 approximation error: {error:.4f}")
        print(f"Second singular value (expected error): {s[1]:.4f}")

---

**Exercise 3.**
Compute the condition number of `A = np.array([[1, 2], [3, 4]])` using SVD (ratio of largest to smallest singular value). Verify it matches `np.linalg.cond(A)`.

??? success "Solution to Exercise 3"

        import numpy as np

        A = np.array([[1, 2], [3, 4]], dtype=float)
        _, s, _ = np.linalg.svd(A)
        cond_svd = s[0] / s[-1]
        cond_np = np.linalg.cond(A)
        print(f"SVD condition number: {cond_svd:.4f}")
        print(f"np.linalg.cond:      {cond_np:.4f}")
        print(f"Match: {np.allclose(cond_svd, cond_np)}")
