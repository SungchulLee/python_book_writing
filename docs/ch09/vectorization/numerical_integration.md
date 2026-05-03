# Numerical Integration

Vectorization enables efficient numerical integration via Riemann sums.

!!! tip "Mental Model"
    Numerical integration approximates the area under a curve by summing thin rectangles (Riemann) or trapezoids. With NumPy, you evaluate the function at all grid points in one vectorized call, then `np.sum` the areas. The finer the grid, the better the approximation -- and vectorization makes even millions of rectangles fast.

## Riemann Sum

### 1. Mathematical Form

$$\int_a^b f(x) \, dx \approx \sum_{i=0}^{n-1} f(x_i) \cdot \Delta x$$

### 2. Discretization

Divide $[a, b]$ into $n$ subintervals of width $\Delta x = \frac{b-a}{n}$.

### 3. Left Endpoint Rule

Use left endpoint of each subinterval for evaluation.

## Basic Example

### 1. Target Integral

$$\int_0^1 x^3 \, dx = \frac{1}{4} = 0.25$$

### 2. Implementation

```python
import numpy as np

def f(x):
    return x ** 3

def main():
    n = 1000
    
    x = np.linspace(0, 1, n + 1)[:-1]  # Left endpoints
    dx = x[1] - x[0]
    y = f(x)
    
    integral = np.sum(y * dx)
    
    print(f"Numerical: {integral:.6f}")
    print(f"Exact:     0.250000")
    print(f"Error:     {abs(integral - 0.25):.6f}")

if __name__ == "__main__":
    main()
```

### 3. Vectorized Computation

The entire sum is computed in one NumPy call.

## Convergence

### 1. Visualization Code

```python
import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return x ** 3

def main():
    n_values = []
    integral_values = []
    
    for n in range(10, 1000, 10):
        x = np.linspace(0, 1, n + 1)[:-1]
        dx = x[1] - x[0]
        y = f(x)
        numerical = np.sum(y * dx)
        
        n_values.append(n)
        integral_values.append(numerical)
    
    fig, ax = plt.subplots(figsize=(6.5, 4))
    
    ax.set_title(r'Numerical Integration of $\int_0^1 x^3 dx$', fontsize=15)
    ax.plot(n_values, integral_values, '-*', markersize=3)
    ax.axhline(0.25, color='r', linestyle='--', label='Exact = 0.25')
    ax.set_xlabel('Number of Subintervals')
    ax.set_ylabel('Numerical Value')
    ax.legend()
    
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Convergence Rate

Error decreases as $O(1/n)$ for left Riemann sum.

### 3. Accuracy vs Cost

More subintervals improve accuracy but increase computation.

## Vectorized vs Loop

### 1. Loop Version

```python
import numpy as np
import time

def f(x):
    return x ** 3

def main():
    n = 100000
    a, b = 0, 1
    dx = (b - a) / n
    
    tic = time.time()
    total = 0
    for i in range(n):
        x_i = a + i * dx
        total += f(x_i) * dx
    loop_time = time.time() - tic
    
    print(f"Loop result: {total:.6f}")
    print(f"Loop time:   {loop_time:.4f} sec")

if __name__ == "__main__":
    main()
```

### 2. Vectorized Version

```python
import numpy as np
import time

def f(x):
    return x ** 3

def main():
    n = 100000
    
    tic = time.time()
    x = np.linspace(0, 1, n + 1)[:-1]
    dx = x[1] - x[0]
    result = np.sum(f(x) * dx)
    vec_time = time.time() - tic
    
    print(f"Vec result:  {result:.6f}")
    print(f"Vec time:    {vec_time:.6f} sec")

if __name__ == "__main__":
    main()
```

### 3. Speedup

Vectorized version is typically 50-100× faster.

## Other Functions

### 1. Gaussian Integral

```python
import numpy as np

def main():
    n = 10000
    a, b = -5, 5
    
    x = np.linspace(a, b, n + 1)[:-1]
    dx = x[1] - x[0]
    
    # Standard normal PDF (unnormalized)
    y = np.exp(-x ** 2 / 2)
    integral = np.sum(y * dx)
    
    exact = np.sqrt(2 * np.pi)
    print(f"Numerical: {integral:.6f}")
    print(f"Exact:     {exact:.6f}")

if __name__ == "__main__":
    main()
```

### 2. Trigonometric

```python
import numpy as np

def main():
    n = 10000
    
    x = np.linspace(0, np.pi, n + 1)[:-1]
    dx = x[1] - x[0]
    
    integral = np.sum(np.sin(x) * dx)
    
    print(f"∫sin(x)dx from 0 to π")
    print(f"Numerical: {integral:.6f}")
    print(f"Exact:     2.000000")

if __name__ == "__main__":
    main()
```

### 3. Custom Functions

Any vectorized function works with this pattern.

## scipy.integrate

For production-quality numerical integration, `scipy.integrate` provides adaptive quadrature methods that are far more accurate and robust than simple Riemann sums.

### Basic Usage: quad

The `quad` function integrates a callable over a finite or infinite interval and returns both the result and an error estimate:

```python
import numpy as np
from scipy.integrate import quad

def f(x):
    return np.exp(-x**2 / 2) / np.sqrt(2 * np.pi)

result, error = quad(f, -3, 3)
print(f"Result: {result:.10f}")   # ≈ 0.9973002040
print(f"Error:  {error:.2e}")
```

### Infinite Integration Domains

Replace finite bounds with `np.inf` or `-np.inf` for improper integrals:

```python
result, error = quad(f, -np.inf, np.inf)
print(f"Result: {result:.10f}")   # ≈ 1.0 (standard normal integrates to 1)
```

### Functions with Extra Parameters

Pass additional arguments via the `args` tuple:

```python
def f(x, mu, sigma):
    return np.exp(-(x - mu)**2 / (2 * sigma**2)) / np.sqrt(2 * np.pi * sigma**2)

mu, sigma = 3, 2
result, error = quad(f, -np.inf, np.inf, args=(mu, sigma))
print(f"Result: {result:.10f}")   # ≈ 1.0
```

### Controlling Precision

The `epsabs` parameter trades accuracy for speed. Reducing precision can halve computation time when integrating repeatedly:

```python
import time

n = 10_000
t1 = time.perf_counter()
[quad(f, -np.inf, np.inf, args=(mu, sigma)) for _ in range(n)]
t2 = time.perf_counter()
print(f"Default precision: {t2 - t1:.2f} sec")

t1 = time.perf_counter()
[quad(f, -np.inf, np.inf, args=(mu, sigma), epsabs=1e-4) for _ in range(n)]
t2 = time.perf_counter()
print(f"Reduced precision: {t2 - t1:.2f} sec")
```

### Difficult Integrands: the points Parameter

When a function has sharp peaks far from the origin, `quad` may miss them. The `points` parameter directs the adaptive algorithm to examine specific locations:

```python
def f(x):
    return np.exp(-(x - 700)**2) + np.exp(-(x + 700)**2)

# Without guidance — may return 0 (misses the peaks)
result, _ = quad(f, -np.inf, np.inf)

# With guidance — finds both peaks (cannot use infinite bounds with points)
result, _ = quad(f, -800, 800, points=[-700, 700])
print(f"Result: {result:.10f}")   # ≈ 2√π ≈ 3.5449077
```

### Vectorized Integration: quad_vec

When you need to evaluate the same integral for many parameter values, `quad_vec` is dramatically faster than looping over `quad`:

```python
from scipy.integrate import quad_vec

def f(x, alpha):
    return np.exp(-alpha * x**2)

alphas = np.linspace(1, 2, 10_000)

# quad_vec: single call, vectorized over alpha (100x+ faster)
result, error = quad_vec(f, -1, 3, args=(alphas,))
print(f"Mean result: {result.mean():.10f}")
```

The speedup comes from evaluating the integrand at all parameter values simultaneously for each quadrature point, rather than running separate adaptive integrations.

### quad_vec with Multiple Parameters

For parameter grids, use `np.meshgrid` to create broadcast-compatible arrays:

```python
import matplotlib.pyplot as plt
from scipy.integrate import quad_vec

def f(x, a, b):
    return np.exp(-a * (x - b)**2)

a = np.arange(1, 20, 1)
b = np.linspace(0, 5, 100)
av, bv = np.meshgrid(a, b)

integral = quad_vec(f, -1, 3, args=(av, bv))[0]

plt.pcolormesh(av, bv, integral, shading='auto')
plt.xlabel('$a$')
plt.ylabel('$b$')
plt.colorbar(label='Integral value')
plt.show()
```

### Combining Interpolation with Integration

A powerful pattern is to interpolate discrete data with `scipy.interpolate.interp1d` and then integrate the smooth interpolant:

```python
from scipy.interpolate import interp1d
from scipy.integrate import quad

x = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.55, 0.662, 0.8, 1., 1.25,
              1.5, 2., 3., 4., 5., 6., 8., 10.])
y = np.array([0., 0.032, 0.06, 0.086, 0.109, 0.131, 0.151, 0.185,
              0.212, 0.238, 0.257, 0.274, 0.256, 0.205, 0.147, 0.096, 0.029, 0.002])

f = interp1d(x, y, 'cubic')
numerator = quad(lambda t: t * f(t), x.min(), x.max())[0]
denominator = quad(f, x.min(), x.max())[0]
mean = numerator / denominator   # Weighted mean ≈ 3.38
```

This technique is directly applicable to computing expected values from empirical probability distributions — a common task in financial mathematics.

### When to Use Each

- **Riemann sums** (earlier sections): Educational, quick vectorized estimates, full control over grid
- **quad**: Single integrals requiring high accuracy, supports infinite bounds and singularities
- **quad_vec**: Batch evaluation of parameterized integrals, orders of magnitude faster than looping `quad`

---

## Runnable Example: `scipy_integrate_tutorial.py`

```python
"""
scipy.integrate Tutorial: quad and quad_vec
============================================
Level: Beginner-Intermediate
Topics: Numerical integration, adaptive quadrature, infinite domains,
        parameterized integrals, vectorized batch integration

This module provides a comprehensive tutorial on scipy.integrate.quad
and scipy.integrate.quad_vec for numerical integration in Python.
"""

import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.integrate import quad, quad_vec

# =============================================================================
# SECTION 1: Basic quad Usage
# =============================================================================

if __name__ == "__main__":
    """
    scipy.integrate.quad computes a definite integral using adaptive
    Gauss-Kronrod quadrature. It returns (result, error_estimate).
    """

    print("=" * 70)
    print("SECTION 1: Basic quad Usage")
    print("=" * 70)


    def f(x):
        """Standard normal PDF (unnormalized by convention here)."""
        return np.exp(-x**2 / 2) / np.sqrt(2 * np.pi)


    # Integrate the standard normal PDF from -3 to 3
    result, error = quad(f, -3, 3)
    print(f"∫ N(0,1) from -3 to 3:")
    print(f"  Result: {result:.10f}")
    print(f"  Error:  {error:.2e}")
    print()

    # =============================================================================
    # SECTION 2: Infinite Integration Domains
    # =============================================================================

    print("=" * 70)
    print("SECTION 2: Infinite Integration Domains")
    print("=" * 70)

    result, error = quad(f, -np.inf, np.inf)
    print(f"∫ N(0,1) from -∞ to ∞:")
    print(f"  Result: {result:.10f}")
    print(f"  Error:  {error:.2e}")
    print()

    # =============================================================================
    # SECTION 3: Functions with Extra Parameters
    # =============================================================================

    print("=" * 70)
    print("SECTION 3: Extra Parameters via args")
    print("=" * 70)


    def f_params(x, mu, sigma):
        """General normal PDF with parameters."""
        return np.exp(-(x - mu)**2 / (2 * sigma**2)) / np.sqrt(2 * np.pi * sigma**2)


    mu, sigma = 3, 2
    result, error = quad(f_params, -np.inf, np.inf, args=(mu, sigma))
    print(f"∫ N({mu},{sigma}) from -∞ to ∞:")
    print(f"  Result: {result:.10f}")
    print(f"  Error:  {error:.2e}")
    print()

    # =============================================================================
    # SECTION 4: Controlling Precision for Speed
    # =============================================================================

    print("=" * 70)
    print("SECTION 4: Precision vs Speed Trade-off")
    print("=" * 70)

    n = 10_000

    t1 = time.perf_counter()
    [quad(f_params, -np.inf, np.inf, args=(mu, sigma)) for _ in range(n)]
    t2 = time.perf_counter()
    print(f"Default precision ({n} integrals): {t2 - t1:.2f} sec")

    t1 = time.perf_counter()
    [quad(f_params, -np.inf, np.inf, args=(mu, sigma), epsabs=1e-4) for _ in range(n)]
    t2 = time.perf_counter()
    print(f"Reduced precision ({n} integrals): {t2 - t1:.2f} sec")
    print()

    # =============================================================================
    # SECTION 5: Difficult Integrands — points Parameter
    # =============================================================================

    print("=" * 70)
    print("SECTION 5: Guiding quad with points")
    print("=" * 70)


    def f_peaks(x):
        """Function with two sharp peaks far from the origin."""
        return np.exp(-(x - 700)**2) + np.exp(-(x + 700)**2)


    # Without guidance — quad may miss the peaks entirely
    result_naive, _ = quad(f_peaks, -np.inf, np.inf)
    print(f"Without points: {result_naive:.10f}")

    # With guidance — cannot use infinite bounds with points
    result_guided, _ = quad(f_peaks, -800, 800, points=[-700, 700])
    print(f"With points:    {result_guided:.10f}")
    print(f"Exact (2√π):    {2 * np.sqrt(np.pi):.10f}")
    print()

    # =============================================================================
    # SECTION 6: quad_vec — Vectorized Batch Integration
    # =============================================================================

    print("=" * 70)
    print("SECTION 6: quad_vec — Massive Speedup")
    print("=" * 70)


    def f_alpha(x, alpha):
        """Gaussian with variable width parameter."""
        return np.exp(-alpha * x**2)


    n_params = 10_000
    alphas = np.linspace(1, 2, n_params)

    # Method 1: Loop with quad (slow)
    t1 = time.perf_counter()
    results_loop = [quad(f_alpha, -1, 3, args=(a,)) for a in alphas]
    t2 = time.perf_counter()
    time_loop = t2 - t1
    mean_loop = np.array([v for v, e in results_loop]).mean()
    print(f"quad loop ({n_params} integrals):     {time_loop:.3f} sec, mean={mean_loop:.10f}")

    # Method 2: quad_vec (fast)
    t1 = time.perf_counter()
    result_vec, error_vec = quad_vec(f_alpha, -1, 3, args=(alphas,))
    t2 = time.perf_counter()
    time_vec = t2 - t1
    mean_vec = result_vec.mean()
    print(f"quad_vec ({n_params} integrals):      {time_vec:.3f} sec, mean={mean_vec:.10f}")
    print(f"Speedup: {time_loop / time_vec:.0f}x")
    print()

    # =============================================================================
    # SECTION 7: quad_vec with Two Parameters
    # =============================================================================

    print("=" * 70)
    print("SECTION 7: quad_vec with Parameter Grid")
    print("=" * 70)


    def f_ab(x, a, b):
        """Gaussian with variable width and center."""
        return np.exp(-a * (x - b)**2)


    a = np.arange(1, 20, 1)
    b = np.linspace(0, 5, 100)
    av, bv = np.meshgrid(a, b)

    integral_grid = quad_vec(f_ab, -1, 3, args=(av, bv))[0]
    print(f"Computed {integral_grid.size} integrals in a single call")
    print(f"Result shape: {integral_grid.shape}")

    plt.figure(figsize=(8, 4))
    plt.pcolormesh(av, bv, integral_grid, shading='auto')
    plt.xlabel('$a$ (width parameter)')
    plt.ylabel('$b$ (center parameter)')
    plt.colorbar(label='Integral value')
    plt.title(r'$\int_{-1}^{3} e^{-a(x-b)^2} dx$ over parameter grid')
    plt.tight_layout()
    plt.show()

    # =============================================================================
    # SECTION 8: quad_vec with Variable Integration Domains
    # =============================================================================

    print("=" * 70)
    print("SECTION 8: Variable Domains via Indicator Functions")
    print("=" * 70)


    def f_variable_domain(x, a):
        """Use indicator function to implement variable bounds [-a, a]."""
        return (x >= -a) * (x <= a) * np.exp(-a * x**2)


    a_vals = np.arange(1, 20, 1)
    integral_variable = quad_vec(f_variable_domain, -np.inf, np.inf, args=(a_vals,))[0]

    plt.figure(figsize=(8, 4))
    plt.plot(a_vals, integral_variable, '--*')
    plt.xlabel('$a$')
    plt.ylabel('Integral value')
    plt.title(r'$\int_{-a}^{a} e^{-ax^2} dx$ for various $a$')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    print()
    print("=" * 70)
    print("Tutorial Complete!")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("1. quad: single integrals with adaptive quadrature")
    print("2. Use args=(...) for parameterized integrands")
    print("3. Use epsabs to trade accuracy for speed")
    print("4. Use points=[...] for difficult integrands with sharp peaks")
    print("5. quad_vec: batch integrals 100x+ faster than looping quad")
    print("6. Use meshgrid for multi-parameter grids with quad_vec")
```

---

## Exercises

**Exercise 1.** Write a vectorized NumPy solution and a pure Python loop solution for the same computation. Measure and compare their performance using `time.perf_counter()`.

??? success "Solution to Exercise 1"
    ```python
    import numpy as np
    import time

    n = 1_000_000
    data = np.random.default_rng(42).random(n)

    # Python loop
    start = time.perf_counter()
    result_py = [x ** 2 for x in data]
    py_time = time.perf_counter() - start

    # NumPy vectorized
    start = time.perf_counter()
    result_np = data ** 2
    np_time = time.perf_counter() - start

    print(f"Python: {py_time:.4f}s, NumPy: {np_time:.6f}s")
    print(f"Speedup: {py_time / np_time:.0f}x")
    ```

---

**Exercise 2.** Identify a potential performance pitfall in the following code and rewrite it using NumPy vectorization:

```python
result = []
for i in range(len(data)):
    result.append(data[i] ** 2 + 2 * data[i] + 1)
```

??? success "Solution to Exercise 2"
    ```python
    import numpy as np

    data = np.random.default_rng(42).random(100000)

    # Vectorized (fast)
    result = data ** 2 + 2 * data + 1
    ```

    The loop version creates Python objects for each element and calls `append` repeatedly. The vectorized version computes everything in compiled C code on contiguous memory.

---

**Exercise 3.** Explain why NumPy vectorized operations are faster than Python loops. Reference memory layout, type checking overhead, and SIMD instructions in your answer.

??? success "Solution to Exercise 3"
    NumPy vectorized operations are faster because:

    1. **Contiguous memory**: NumPy arrays store elements in a contiguous block, enabling efficient CPU cache usage.
    2. **No type checking**: Python loops check types at each iteration; NumPy knows the dtype in advance.
    3. **Compiled C loops**: The actual computation runs in compiled C/Fortran code, not interpreted Python.
    4. **SIMD instructions**: Modern CPUs can process multiple array elements simultaneously using SIMD (Single Instruction, Multiple Data).

---

**Exercise 4.** Apply the concepts from this page to a practical problem: given a large array of temperatures in Celsius, convert them all to Fahrenheit and find the maximum. Compare vectorized and loop approaches.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    import time

    rng = np.random.default_rng(42)
    celsius = rng.uniform(-40, 50, 1_000_000)

    # Vectorized
    start = time.perf_counter()
    fahrenheit = celsius * 9/5 + 32
    max_f = fahrenheit.max()
    vec_time = time.perf_counter() - start

    # Loop
    start = time.perf_counter()
    max_f_loop = max(c * 9/5 + 32 for c in celsius)
    loop_time = time.perf_counter() - start

    print(f"Vectorized: {vec_time:.6f}s, max={max_f:.1f}F")
    print(f"Loop: {loop_time:.4f}s, max={max_f_loop:.1f}F")
    ```
