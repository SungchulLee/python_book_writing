# Least Squares Connection

When `np.polyfit` fits a polynomial to data, it solves a least squares problem under the hood. Understanding this connection reveals why polynomial fitting works, when it fails, and how to control the numerical behavior. The same least squares machinery underlies linear regression, spline fitting, and many other approximation techniques.

!!! tip "Mental Model"
    Polynomial fitting is really matrix algebra in disguise. You build a Vandermonde matrix from your x-values, then solve an overdetermined system in the least-squares sense. The coefficients that minimize the sum of squared residuals are the same ones that `np.polyfit` returns -- understanding this connection lets you diagnose ill-conditioning and choose the right degree.

---

!!! info "Big Picture"
    All polynomial fitting reduces to one equation: $V \mathbf{c} \approx \mathbf{y}$, where $V$ is the Vandermonde matrix built from x-values and $\mathbf{c}$ are the unknown coefficients. Everything else — normal equations, QR, SVD, scaling — is about *how* we solve that system stably.

!!! note "Unified Approximation Map"
    Every topic in this section connects through a single pipeline:

    ```text
    Data (x, y)
        │
        ▼
    Vandermonde Matrix V
        │
        ▼
    Least Squares: V c ≈ y
        │
        ├──→ polyfit / poly1d       (legacy API, power basis)
        │
        ├──→ Polynomial.fit         (modern API, domain scaling)
        │         │
        │         ▼
        │    Polynomial class       (coefficients + domain + window)
        │
        └──→ Problems
              │
              ├── Ill-conditioning  → fix with domain mapping (Polynomial.fit)
              └── Oscillation       → fix with splines (scipy.interpolate)
    ```

    At the deepest level, this is the same $A\mathbf{x} \approx \mathbf{b}$
    that appears in linear regression, signal processing (FFT is a linear
    transform), and every other least-squares problem in the book.

## The Fitting Problem

Given data points $(x_i, y_i)$ for $i = 1, \ldots, m$, find the polynomial of degree $n$ that best fits the data.

### 1. Polynomial Model

A polynomial of degree $n$ has $n + 1$ coefficients:

$$
p(x) = c_0 + c_1 x + c_2 x^2 + \cdots + c_n x^n
$$

### 2. Residuals

The residual at each data point measures the fitting error:

$$
r_i = y_i - p(x_i)
$$

### 3. Least Squares Objective

Find coefficients $c_0, c_1, \ldots, c_n$ that minimize the sum of squared residuals:

$$
\min_{c_0, \ldots, c_n} \sum_{i=1}^{m} \left( y_i - \sum_{j=0}^{n} c_j x_i^j \right)^2
$$


## The Vandermonde Matrix

The fitting problem becomes a linear system through the Vandermonde matrix.

### 1. Matrix Formulation

Stacking all data points into a matrix equation:

$$
\underbrace{\begin{pmatrix} 1 & x_1 & x_1^2 & \cdots & x_1^n \\ 1 & x_2 & x_2^2 & \cdots & x_2^n \\ \vdots & \vdots & \vdots & \ddots & \vdots \\ 1 & x_m & x_m^2 & \cdots & x_m^n \end{pmatrix}}_{V} \underbrace{\begin{pmatrix} c_0 \\ c_1 \\ \vdots \\ c_n \end{pmatrix}}_{\mathbf{c}} = \underbrace{\begin{pmatrix} y_1 \\ y_2 \\ \vdots \\ y_m \end{pmatrix}}_{\mathbf{y}}
$$

### 2. Building the Vandermonde in NumPy

```python
import numpy as np

def main():
    x = np.array([0, 1, 2, 3, 4], dtype=float)
    deg = 2

    # np.vander builds the Vandermonde matrix
    V = np.vander(x, N=deg + 1, increasing=True)
    print("Vandermonde matrix:")
    print(V)

if __name__ == "__main__":
    main()
```

Output:

```
Vandermonde matrix:
[[ 1.  0.  0.]
 [ 1.  1.  1.]
 [ 1.  2.  4.]
 [ 1.  3.  9.]
 [ 1.  4. 16.]]
```

### 3. Overdetermined System

When $m > n + 1$ (more data points than coefficients), the system $V \mathbf{c} = \mathbf{y}$ has no exact solution. The least squares solution minimizes $\|V \mathbf{c} - \mathbf{y}\|_2^2$.


## Normal Equations

The classical approach to solving least squares.

### 1. Derivation

Setting the gradient to zero yields the normal equations:

$$
V^T V \, \mathbf{c} = V^T \mathbf{y}
$$

### 2. Direct Solution

```python
import numpy as np

def main():
    x = np.array([0, 1, 2, 3, 4], dtype=float)
    y = np.array([1, 3, 7, 13, 21], dtype=float)
    deg = 2

    V = np.vander(x, N=deg + 1, increasing=True)
    # Normal equations: (V^T V) c = V^T y
    c = np.linalg.solve(V.T @ V, V.T @ y)
    print("Coefficients (ascending):", c)

if __name__ == "__main__":
    main()
```

Output:

```
Coefficients (ascending): [1. 1. 1.]
```

### 3. Numerical Issues

The normal equations square the condition number of $V$. If $V$ has condition number $\kappa$, then $V^T V$ has condition number $\kappa^2$, amplifying numerical errors. For this reason, `np.polyfit` does not use normal equations directly.


## QR Decomposition Approach

The method `np.polyfit` actually uses for better numerical stability.

### 1. QR Factorization

Decompose $V = QR$ where $Q$ is orthogonal and $R$ is upper triangular:

$$
V \mathbf{c} = \mathbf{y} \implies QR \mathbf{c} = \mathbf{y} \implies R \mathbf{c} = Q^T \mathbf{y}
$$

### 2. Implementation

```python
import numpy as np

def main():
    x = np.array([0, 1, 2, 3, 4], dtype=float)
    y = np.array([1, 3, 7, 13, 21], dtype=float)
    deg = 2

    V = np.vander(x, N=deg + 1, increasing=True)
    Q, R = np.linalg.qr(V)
    c = np.linalg.solve(R, Q.T @ y)
    print("Coefficients (QR):", c)

if __name__ == "__main__":
    main()
```

### 3. Why QR is Better

The condition number of $R$ equals the condition number of $V$ (not its square), providing much better numerical stability for high-degree polynomials or poorly spaced data points.


## np.lstsq — Direct Least Squares

NumPy provides `np.linalg.lstsq` for solving least squares problems directly.

### 1. Basic Usage

```python
import numpy as np

def main():
    x = np.array([0, 1, 2, 3, 4], dtype=float)
    y = np.array([1, 3, 7, 13, 21], dtype=float)
    deg = 2

    V = np.vander(x, N=deg + 1, increasing=True)
    c, residuals, rank, sv = np.linalg.lstsq(V, y, rcond=None)
    print("Coefficients:", c)
    print("Residuals:", residuals)
    print("Rank:", rank)
    print("Singular values:", sv)

if __name__ == "__main__":
    main()
```

Output:

```
Coefficients: [1. 1. 1.]
Residuals: []
Rank: 3
Singular values: [18.76166304  2.07972297  0.26600784]
```

### 2. Residuals Interpretation

The `residuals` array contains $\|V \mathbf{c} - \mathbf{y}\|_2^2$. When the fit is exact (as with degree = number of points - 1), the residuals array is empty.

### 3. Comparison with polyfit

```python
import numpy as np

def main():
    x = np.array([1, 2, 3, 4, 5], dtype=float)
    y = np.array([2.1, 3.9, 6.2, 7.8, 10.1], dtype=float)

    # polyfit (descending order)
    coeffs_polyfit = np.polyfit(x, y, 2)

    # lstsq (ascending order with Vandermonde)
    V = np.vander(x, N=3, increasing=True)
    coeffs_lstsq, _, _, _ = np.linalg.lstsq(V, y, rcond=None)

    print("polyfit (descending):", coeffs_polyfit)
    print("lstsq   (ascending):", coeffs_lstsq)
    print("Match:", np.allclose(coeffs_polyfit, coeffs_lstsq[::-1]))

if __name__ == "__main__":
    main()
```


## Conditioning and Stability

When polynomial fitting fails numerically.

### 1. Ill-Conditioned Vandermonde

```python
import numpy as np

def main():
    # Wide-range x values create ill-conditioned Vandermonde
    x = np.array([1, 10, 100, 1000, 10000], dtype=float)
    y = np.array([1, 2, 3, 4, 5], dtype=float)

    V = np.vander(x, N=3, increasing=True)
    cond = np.linalg.cond(V)
    print(f"Condition number: {cond:.2e}")

if __name__ == "__main__":
    main()
```

### 2. Centering and Scaling

Improve conditioning by normalizing the x values:

```python
import numpy as np

def main():
    x = np.array([1, 10, 100, 1000, 10000], dtype=float)
    y = np.array([1, 2, 3, 4, 5], dtype=float)

    # Center and scale
    x_mean = x.mean()
    x_std = x.std()
    x_norm = (x - x_mean) / x_std

    V_raw = np.vander(x, N=3, increasing=True)
    V_norm = np.vander(x_norm, N=3, increasing=True)

    print(f"Raw condition:        {np.linalg.cond(V_raw):.2e}")
    print(f"Normalized condition: {np.linalg.cond(V_norm):.2e}")

if __name__ == "__main__":
    main()
```

### 3. np.polynomial Uses This Automatically

The modern `np.polynomial.Polynomial.fit` method automatically centers and scales internally, which is one reason it is numerically superior to `np.polyfit`.


## Weighted Least Squares

Assign different importance to different data points.

### 1. Weight Parameter in polyfit

```python
import numpy as np

def main():
    x = np.array([0, 1, 2, 3, 4], dtype=float)
    y = np.array([1.0, 2.8, 5.1, 7.0, 20.0])  # last point is outlier

    # Unweighted fit
    c_unweighted = np.polyfit(x, y, 1)

    # Downweight the outlier
    w = np.array([1, 1, 1, 1, 0.1])
    c_weighted = np.polyfit(x, y, 1, w=w)

    print(f"Unweighted: y = {c_unweighted[0]:.2f}x + {c_unweighted[1]:.2f}")
    print(f"Weighted:   y = {c_weighted[0]:.2f}x + {c_weighted[1]:.2f}")

if __name__ == "__main__":
    main()
```

### 2. Mathematical Formulation

Weighted least squares minimizes:

$$
\sum_{i=1}^{m} w_i \left( y_i - p(x_i) \right)^2
$$

This is equivalent to solving $W V \mathbf{c} = W \mathbf{y}$ where $W = \text{diag}(\sqrt{w_1}, \ldots, \sqrt{w_m})$.

### 3. Use Cases

Weights are useful when data points have different measurement uncertainties. Set $w_i = 1/\sigma_i^2$ where $\sigma_i$ is the standard deviation of the measurement at $x_i$.


## Summary

| Method | Function | Stability | Notes |
|---|---|---|---|
| Normal equations | `np.linalg.solve(V.T @ V, V.T @ y)` | Poor | Condition number squared |
| QR decomposition | `np.linalg.qr` + solve | Good | Used by `np.polyfit` |
| SVD-based lstsq | `np.linalg.lstsq` | Best | Returns rank and singular values |
| Modern API | `Polynomial.fit` | Best | Auto-centering and scaling |

The least squares framework unifies all polynomial fitting: `np.polyfit` builds a Vandermonde matrix and solves via QR, `np.linalg.lstsq` uses SVD for maximum stability, and `np.polynomial.Polynomial.fit` adds automatic conditioning improvements.

---

## Exercises

**Exercise 1.**
Build the Vandermonde matrix for `x = [0, 1, 2, 3, 4]` with degree 3 using `np.vander(x, N=4, increasing=True)`. Solve the least-squares problem `V @ c = y` for `y = [1, 2, 9, 28, 65]` using both the normal equations and `np.linalg.lstsq`. Verify both methods produce the same coefficients.

??? success "Solution to Exercise 1"

        import numpy as np

        x = np.array([0, 1, 2, 3, 4], dtype=float)
        y = np.array([1, 2, 9, 28, 65], dtype=float)
        V = np.vander(x, N=4, increasing=True)

        # Normal equations
        c_normal = np.linalg.solve(V.T @ V, V.T @ y)

        # lstsq
        c_lstsq, _, _, _ = np.linalg.lstsq(V, y, rcond=None)

        print(f"Normal equations: {c_normal}")
        print(f"lstsq:           {c_lstsq}")
        print(f"Match: {np.allclose(c_normal, c_lstsq)}")

---

**Exercise 2.**
Fit a degree-1 polynomial (line) to `x = [0, 1, 2, 3, 4]`, `y = [1.0, 2.8, 5.1, 7.0, 20.0]` with and without weights. Use `w = [1, 1, 1, 1, 0.1]` to downweight the outlier at `x=4`. Print the slope and intercept for both fits and confirm the weighted fit is closer to the true underlying line `y = 2x + 1`.

??? success "Solution to Exercise 2"

        import numpy as np

        x = np.array([0, 1, 2, 3, 4], dtype=float)
        y = np.array([1.0, 2.8, 5.1, 7.0, 20.0])

        # Unweighted
        m, b = np.polyfit(x, y, 1)
        print(f"Unweighted: y = {m:.2f}x + {b:.2f}")

        # Weighted
        w = np.array([1, 1, 1, 1, 0.1])
        m_w, b_w = np.polyfit(x, y, 1, w=w)
        print(f"Weighted:   y = {m_w:.2f}x + {b_w:.2f}")

        # True line is y = 2x + 1
        print(f"Weighted slope closer to 2: {abs(m_w - 2) < abs(m - 2)}")

---

**Exercise 3.**
Compute the condition number of the Vandermonde matrix for `x = np.linspace(0, 100, 20)` at degrees 5, 10, and 15. Then center and scale `x` to `x_norm = (x - x.mean()) / x.std()` and recompute the condition numbers. Print the improvement factor at each degree.

??? success "Solution to Exercise 3"

        import numpy as np

        x = np.linspace(0, 100, 20)
        x_norm = (x - x.mean()) / x.std()

        for deg in [5, 10, 15]:
            V_raw = np.vander(x, N=deg+1, increasing=True)
            V_norm = np.vander(x_norm, N=deg+1, increasing=True)
            cond_raw = np.linalg.cond(V_raw)
            cond_norm = np.linalg.cond(V_norm)
            print(f"Degree {deg:2d}: raw cond={cond_raw:.2e}, "
                  f"norm cond={cond_norm:.2e}, "
                  f"improvement={cond_raw/cond_norm:.0f}x")
