# Toeplitz and Circulant

Toeplitz and circulant matrices appear throughout signal processing, time series analysis, and numerical methods for differential equations. A Toeplitz matrix has constant values along each diagonal, which means the entire matrix is determined by its first row and first column. A circulant matrix is a special case where each row is a cyclic shift of the previous one, enabling fast $O(n \log n)$ matrix-vector multiplication via the FFT. SciPy provides dedicated constructors for both.

!!! tip "Mental Model"
    A Toeplitz matrix is constant along every diagonal -- it is fully determined by just $2n - 1$ values instead of $n^2$. A circulant matrix goes one step further: it wraps around cyclically, which means it is diagonalized by the DFT matrix. This connection to the Fourier transform is why convolution (a circulant operation) can be computed in $O(n \log n)$ time via the FFT.

```python
import numpy as np
from scipy import linalg
```

---

## Toeplitz Matrix

A Toeplitz matrix $T$ has the property that each descending diagonal from left to right is constant. Formally, $T_{ij} = t_{i-j}$ for some sequence $\{t_k\}$. The general form is

$$
T = \begin{pmatrix} t_0 & t_{-1} & t_{-2} & \cdots & t_{-(n-1)} \\ t_1 & t_0 & t_{-1} & \cdots & t_{-(n-2)} \\ t_2 & t_1 & t_0 & \cdots & t_{-(n-3)} \\ \vdots & \vdots & \vdots & \ddots & \vdots \\ t_{n-1} & t_{n-2} & t_{n-3} & \cdots & t_0 \end{pmatrix}
$$

The matrix is fully determined by $2n - 1$ values (the first column and first row) rather than $n^2$.

### scipy.linalg.toeplitz

`linalg.toeplitz(c, r)` constructs a Toeplitz matrix from its first column `c` and first row `r`. The first element of `c` and `r` must agree (both define the top-left corner).

```python
def main():
    c = [1, 2, 3, 4]  # First column
    r = [1, 5, 6, 7]  # First row (first element matches c[0])

    T = linalg.toeplitz(c, r)
    print(T)

if __name__ == "__main__":
    main()
```

```
[[1 5 6 7]
 [2 1 5 6]
 [3 2 1 5]
 [4 3 2 1]]
```

Each diagonal running from top-left to bottom-right contains a constant value: the main diagonal is all 1's, the first sub-diagonal is all 2's, and so on.

### Symmetric Toeplitz

If only the first column is provided (no `r`), the result is a symmetric Toeplitz matrix where the first row equals the first column.

```python
T_sym = linalg.toeplitz([1, 2, 3, 4])
print(T_sym)
```

```
[[1 2 3 4]
 [2 1 2 3]
 [3 2 1 2]
 [4 3 2 1]]
```

!!! note "Autocovariance Matrices"
    The autocovariance matrix of a stationary time series is a symmetric Toeplitz matrix, since $\text{Cov}(X_t, X_s) = \gamma(|t - s|)$ depends only on the time lag.

---

## Circulant Matrix

A circulant matrix is a Toeplitz matrix where each row is a cyclic (circular) shift of the row above it. Given a vector $c = (c_0, c_1, \ldots, c_{n-1})$, the circulant matrix is

$$
C = \begin{pmatrix} c_0 & c_{n-1} & c_{n-2} & \cdots & c_1 \\ c_1 & c_0 & c_{n-1} & \cdots & c_2 \\ c_2 & c_1 & c_0 & \cdots & c_3 \\ \vdots & \vdots & \vdots & \ddots & \vdots \\ c_{n-1} & c_{n-2} & c_{n-3} & \cdots & c_0 \end{pmatrix}
$$

### scipy.linalg.circulant

```python
def main():
    c = [1, 2, 3, 4]
    C = linalg.circulant(c)
    print(C)

if __name__ == "__main__":
    main()
```

```
[[1 4 3 2]
 [2 1 4 3]
 [3 2 1 4]
 [4 3 2 1]]
```

Each row is the previous row shifted one position to the right (with wraparound).

---

## FFT Diagonalization of Circulant Matrices

The key computational property of circulant matrices is that they are diagonalized by the discrete Fourier transform (DFT) matrix $F$:

$$
C = F^{-1} \Lambda F
$$

where $\Lambda = \mathrm{diag}(\hat{c})$ and $\hat{c} = \mathrm{FFT}(c)$ is the DFT of the first column. This means matrix-vector multiplication $Cx$ can be computed as

$$
Cx = F^{-1}(\hat{c} \odot Fx)
$$

where $\odot$ denotes element-wise multiplication. Since the FFT runs in $O(n \log n)$, this is much faster than the standard $O(n^2)$ matrix-vector multiply.

```python
c = np.array([1, 2, 3, 4], dtype=float)
x = np.array([1, 0, 0, 1], dtype=float)

# Direct multiplication
C = linalg.circulant(c)
y_direct = C @ x

# FFT-based multiplication
c_hat = np.fft.fft(c)
x_hat = np.fft.fft(x)
y_fft = np.fft.ifft(c_hat * x_hat).real

print(f"Direct: {y_direct}")   # [3. 6. 6. 8.]
print(f"FFT:    {y_fft}")      # [3. 6. 6. 8.]
```

!!! tip "When to Use FFT Multiplication"
    For small matrices, direct multiplication is faster due to FFT overhead. The FFT approach becomes worthwhile for $n \gtrsim 64$, and the speedup grows with matrix size — at $n = 10{,}000$, the FFT is roughly 1000 times faster.

---

## Summary

| Function | Purpose | Key Property |
|----------|---------|-------------|
| `scipy.linalg.toeplitz(c, r)` | Construct Toeplitz matrix | Constant diagonals; $2n-1$ parameters |
| `scipy.linalg.circulant(c)` | Construct circulant matrix | Cyclic row shifts; diagonalized by FFT |

**Key Takeaways**:

- A Toeplitz matrix is defined by its first column and first row (constant diagonals)
- A circulant matrix is a special Toeplitz matrix where rows are cyclic shifts of one another
- Circulant matrices are diagonalized by the DFT matrix, enabling $O(n \log n)$ multiplication via FFT
- Symmetric Toeplitz matrices arise naturally as autocovariance matrices of stationary time series
- Use `linalg.toeplitz(c)` (one argument) for symmetric Toeplitz, `linalg.toeplitz(c, r)` for general

---

## Exercises

**Exercise 1.**
Construct a $5 \times 5$ symmetric Toeplitz matrix with first column $[4, -1, 0, 0, 0]$ (a tridiagonal matrix). Compute its eigenvalues using `linalg.eigvalsh` and verify that all eigenvalues are positive (the matrix is positive definite). Solve $Tx = b$ where $b = (1, 2, 3, 4, 5)^T$.

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import linalg

        c = [4, -1, 0, 0, 0]
        T = linalg.toeplitz(c)
        print("Toeplitz matrix:")
        print(T)

        eigenvalues = linalg.eigvalsh(T)
        print(f"\nEigenvalues: {eigenvalues}")
        print(f"All positive: {np.all(eigenvalues > 0)}")

        b = np.array([1, 2, 3, 4, 5], dtype=float)
        x = linalg.solve(T, b)
        print(f"\nSolution x: {x}")

---

**Exercise 2.**
Build a $6 \times 6$ circulant matrix from the vector $c = [3, -1, 0, 0, 0, -1]$. Verify the FFT diagonalization property: compute $\hat{c} = \text{FFT}(c)$ and check that for a test vector $x$, the circulant-vector product $Cx$ equals $\text{IFFT}(\hat{c} \odot \text{FFT}(x))$.

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import linalg

        c = np.array([3, -1, 0, 0, 0, -1], dtype=float)
        C = linalg.circulant(c)
        print("Circulant matrix:")
        print(C)

        # FFT diagonalization check
        x = np.array([1, 0, 1, 0, 1, 0], dtype=float)
        y_direct = C @ x

        c_hat = np.fft.fft(c)
        x_hat = np.fft.fft(x)
        y_fft = np.fft.ifft(c_hat * x_hat).real

        print(f"\nDirect: {y_direct}")
        print(f"FFT:    {y_fft}")
        print(f"Match: {np.allclose(y_direct, y_fft)}")

---

**Exercise 3.**
Create a $100 \times 100$ Toeplitz matrix representing a discrete convolution with kernel $[0.1, 0.2, 0.4, 0.2, 0.1]$ (first column has these values at the top, first row has them at the left). Apply this operator to a random signal of length 100 using both direct matrix-vector multiplication and, for the circulant approximation, using FFT-based multiplication. Compare the results.

??? success "Solution to Exercise 3"
        import numpy as np
        from scipy import linalg

        np.random.seed(0)
        n = 100
        kernel = [0.1, 0.2, 0.4, 0.2, 0.1]

        # Toeplitz matrix
        col = np.zeros(n)
        col[:3] = [0.4, 0.2, 0.1]
        row = np.zeros(n)
        row[:3] = [0.4, 0.2, 0.1]
        T = linalg.toeplitz(col, row)

        # Random signal
        signal = np.random.randn(n)

        # Direct multiplication
        y_direct = T @ signal

        # Circulant (FFT) approximation
        c_circ = np.zeros(n)
        c_circ[0] = 0.4
        c_circ[1] = 0.2
        c_circ[2] = 0.1
        c_circ[-2] = 0.1
        c_circ[-1] = 0.2
        c_hat = np.fft.fft(c_circ)
        y_fft = np.fft.ifft(c_hat * np.fft.fft(signal)).real

        error = np.linalg.norm(y_direct - y_fft)
        print(f"Direct vs FFT difference norm: {error:.6f}")
        print(f"First 5 values (direct): {y_direct[:5].round(4)}")
        print(f"First 5 values (FFT):    {y_fft[:5].round(4)}")
