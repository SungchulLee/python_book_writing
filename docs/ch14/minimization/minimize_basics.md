# Minimization Basics

The `scipy.optimize.minimize()` function is the workhorse of optimization in SciPy. It provides a flexible interface to various minimization algorithms, handling everything from simple scalar functions to complex multidimensional optimization problems.

!!! tip "Mental Model"
    Think of `minimize()` as a universal remote for optimization: you hand it a cost function (what to minimize), a starting point (where to begin searching), and optionally a method (which algorithm to use). It returns a result object that tells you the best parameters found, the minimum value achieved, and whether the search actually converged. The cost function is yours to define -- the optimizer just walks downhill.

---

## Understanding Cost Functions

A cost function (also called objective function or loss function) quantifies how well parameters match your goals. The optimizer searches for parameter values that minimize this function.

### Properties of Good Cost Functions

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

# Good cost function: smooth, differentiable
def good_cost(x):
    """Parabola - smooth and convex."""
    return (x - 3)**2

# Challenging cost function: noisy, many local minima
def challenging_cost(x):
    """Multiple local minima."""
    return np.sin(x) + 0.1 * x**2

# Visualize
x = np.linspace(-2, 8, 1000)
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].plot(x, good_cost(x))
axes[0].set_title('Simple Convex Function')
axes[0].set_xlabel('x')
axes[0].set_ylabel('f(x)')

axes[1].plot(x, challenging_cost(x))
axes[1].set_title('Function with Local Minima')
axes[1].set_xlabel('x')
axes[1].set_ylabel('f(x)')

plt.tight_layout()
plt.show()
```

### Formulating Your Problem

The key is expressing your objective as a mathematical function:

```python
import numpy as np
from scipy import optimize

# Example: Fit data to a line
xdata = np.array([1, 2, 3, 4, 5])
ydata = np.array([2.1, 3.9, 6.2, 7.8, 10.1])

# Cost function: sum of squared errors (MSE)
def mse_cost(params):
    """
    Compute mean squared error.

    Parameters
    ----------
    params : array
        [slope, intercept] of line y = slope*x + intercept

    Returns
    -------
    cost : float
        Mean squared error
    """
    slope, intercept = params
    predicted = slope * xdata + intercept
    residuals = ydata - predicted
    return np.mean(residuals**2)

# Alternative: using sum of squared errors
def sse_cost(params):
    """Sum of squared errors."""
    slope, intercept = params
    predicted = slope * xdata + intercept
    residuals = ydata - predicted
    return np.sum(residuals**2)
```

---

## Basic Usage of minimize()

### The Simplest Case: One Parameter

```python
from scipy import optimize

def f(x):
    """Minimize (x - 3)^2."""
    return (x - 3)**2

# Find minimum starting from x=0
result = optimize.minimize(f, x0=0)

print(f"Success: {result.success}")
print(f"Optimal x: {result.x}")
print(f"Minimum value: {result.fun}")
print(f"Iterations: {result.nit}")
print(f"Function evaluations: {result.nfev}")
```

**Output:**
```
Success: True
Optimal x: [3.]
Minimum value: 2.9e-16
Iterations: 3
Function evaluations: 6
```

### Multiple Parameters

```python
import numpy as np
from scipy import optimize

# Fit data to line
xdata = np.array([1, 2, 3, 4, 5])
ydata = np.array([2.1, 3.9, 6.2, 7.8, 10.1])

def mse_cost(params):
    slope, intercept = params
    predicted = slope * xdata + intercept
    residuals = ydata - predicted
    return np.mean(residuals**2)

# Initial guess
x0 = np.array([1.0, 0.0])  # slope=1, intercept=0

# Minimize
result = optimize.minimize(mse_cost, x0)

print(f"Slope: {result.x[0]:.4f}")
print(f"Intercept: {result.x[1]:.4f}")
print(f"MSE: {result.fun:.6f}")

# Verify with numpy's polyfit
coeffs = np.polyfit(xdata, ydata, 1)
print(f"NumPy slope: {coeffs[0]:.4f}")
print(f"NumPy intercept: {coeffs[1]:.4f}")
```

---

## Understanding the Result Object

The `minimize()` function returns an `OptimizeResult` object with detailed information:

```python
from scipy import optimize

def f(x):
    return (x - 3)**2 + 2*x

result = optimize.minimize(f, x0=0)

# Access individual attributes
print(f"x: {result.x}")              # Optimal parameters
print(f"fun: {result.fun}")          # Final function value
print(f"success: {result.success}")  # Did it converge?
print(f"message: {result.message}")  # Details about termination
print(f"nit: {result.nit}")          # Number of iterations
print(f"nfev: {result.nfev}")        # Number of function evaluations
print(f"njev: {result.njev}")        # Number of Jacobian evaluations

# Full result
print(result)
```

---

## The Rosenbrock Function: A Classic Test Case

The Rosenbrock function is a standard benchmark for optimization algorithms because it's notoriously difficult despite looking simple:

$$f(x, y) = (1-x)^2 + 100(y-x^2)^2$$

This function has a global minimum at $(x, y) = (1, 1)$ where $f(1, 1) = 0$.

```python
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def rosenbrock(x):
    """Rosenbrock function."""
    return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2

# Minimize from different starting points
starting_points = [
    np.array([0, 0]),
    np.array([-1, -1]),
    np.array([2, 2])
]

for start in starting_points:
    result = optimize.minimize(rosenbrock, start)
    print(f"Start: {start}")
    print(f"  Optimal: {result.x}")
    print(f"  Value: {result.fun:.2e}")
    print()

# Visualize the function
x = np.linspace(-2, 2, 100)
y = np.linspace(-1, 3, 100)
X, Y = np.meshgrid(x, y)
Z = (1 - X)**2 + 100 * (Y - X**2)**2

fig = plt.figure(figsize=(12, 5))

# 3D surface
ax1 = fig.add_subplot(121, projection='3d')
ax1.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_zlabel('f(x, y)')
ax1.set_title('Rosenbrock Function (3D)')

# Contour plot
ax2 = fig.add_subplot(122)
contour = ax2.contourf(X, Y, Z, levels=20, cmap='viridis')
ax2.plot(1, 1, 'r*', markersize=15, label='Global minimum')
ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.set_title('Rosenbrock Function (Contours)')
plt.colorbar(contour, ax=ax2)

# Show optimization path
result = optimize.minimize(rosenbrock, np.array([0, 0]))
ax2.plot(result.x[0], result.x[1], 'go', markersize=10, label='Found minimum')
ax2.legend()

plt.tight_layout()
plt.show()
```

---

## Passing Additional Arguments

Often your cost function needs additional data or parameters that shouldn't be optimized:

```python
from scipy import optimize
import numpy as np

# Observational data
xdata = np.array([0, 1, 2, 3, 4])
ydata = np.array([0.1, 0.9, 2.1, 3.1, 3.9])

# Cost function that takes additional arguments
def polynomial_cost(coeffs, xdata, ydata, degree):
    """
    Fit polynomial of specified degree.

    Parameters
    ----------
    coeffs : array
        Polynomial coefficients to optimize
    xdata, ydata : array
        Data points (not optimized)
    degree : int
        Polynomial degree (not optimized)
    """
    # Build polynomial
    poly = np.poly1d(coeffs)
    predicted = poly(xdata)
    residuals = ydata - predicted
    return np.sum(residuals**2)

# Initial guess for quadratic (3 coefficients)
x0 = np.array([1.0, 1.0, 0.0])

# Pass fixed data and parameters via args
result = optimize.minimize(
    polynomial_cost,
    x0,
    args=(xdata, ydata, 2),  # Fixed arguments
    method='Nelder-Mead'
)

print(f"Optimal coefficients: {result.x}")
print(f"Final cost: {result.fun}")

# Verify by fitting polynomial
fitted = np.polyfit(xdata, ydata, 2)
print(f"NumPy result: {fitted}")
```

---

## Handling Constraints with Bounds

Simple bound constraints (each parameter has lower and upper limits) can be handled directly:

```python
from scipy import optimize
import numpy as np

def f(x):
    return (x[0] - 5)**2 + (x[1] - 3)**2

# Without bounds
result_unbounded = optimize.minimize(f, x0=[0, 0])
print("Unbounded:")
print(f"  x = {result_unbounded.x}")

# With bounds: 0 <= x0 <= 2, x1 can be anything
bounds = [(0, 2), (None, None)]
result_bounded = optimize.minimize(f, x0=[0, 0], bounds=bounds)
print("\nWith bounds (x0 in [0, 2]):")
print(f"  x = {result_bounded.x}")
```

---

## Checking for Convergence

Successful optimization requires checking that the algorithm actually converged:

```python
from scipy import optimize
import numpy as np

def f(x):
    return x**2

result = optimize.minimize(f, x0=10)

# Check success
if result.success:
    print(f"Converged successfully")
    print(f"Solution: {result.x}")
else:
    print(f"Failed to converge")
    print(f"Reason: {result.message}")
    print(f"Best estimate: {result.x}")

# You might also check the gradient
if hasattr(result, 'jac'):
    gradient = result.jac
    print(f"Gradient magnitude: {np.linalg.norm(gradient)}")
    if np.linalg.norm(gradient) > 1e-4:
        print("  Warning: Gradient not small, may not be at minimum")
```

---

## Common Pitfalls

### 1. Poor Initial Guess

```python
# This function has minimum at x = pi
def f(x):
    return np.cos(x)

# Good initial guess
result1 = optimize.minimize(f, x0=0)
print(f"From x0=0: {result1.x[0]:.4f}")

# Poor initial guess can find wrong local minimum
result2 = optimize.minimize(f, x0=10)
print(f"From x0=10: {result2.x[0]:.4f}")

# Better: use a method that's less sensitive to starting point
result3 = optimize.differential_evolution(f, bounds=[(0, 10)])
print(f"Global: {result3.x[0]:.4f}")
```

### 2. Not Setting Reasonable Bounds

```python
# Without bounds, some methods might search unreasonable areas
def f(x):
    if x[0] < 0 or x[0] > 1:
        return 1e10  # Very large penalty
    return (x[0] - 0.3)**2

# Better: specify bounds instead
bounds = [(0, 1)]
result = optimize.minimize(f, x0=[0.5], bounds=bounds, method='L-BFGS-B')
```

### 3. Ignoring Warnings

```python
# Some methods print warnings if they have issues
result = optimize.minimize(lambda x: x**2, x0=5, maxiter=1)
if result.success is False:
    print(f"Optimization warning: {result.message}")
```

---

## Summary

Key points about `scipy.optimize.minimize()`:

1. **Define a cost function** that takes parameters and returns a scalar cost
2. **Provide initial guess** via `x0` parameter
3. **Choose a method** (default BFGS usually works well)
4. **Add constraints** via `bounds` and `constraints` if needed
5. **Inspect the result** object to verify convergence
6. **Be aware** of local minima and use global methods if needed

The next section explores different algorithms and when to use each one.

---

## Exercises

**Exercise 1.**
Use `scipy.optimize.minimize` to find the minimum of the Booth function $f(x, y) = (x + 2y - 7)^2 + (2x + y - 5)^2$, starting from `x0 = [0, 0]`. Print the optimal point, the function value, and verify that the result is close to the known minimum at $(1, 3)$.

??? success "Solution to Exercise 1"
        ```python
        import numpy as np
        from scipy import optimize

        def booth(x):
            return (x[0] + 2*x[1] - 7)**2 + (2*x[0] + x[1] - 5)**2

        result = optimize.minimize(booth, x0=[0, 0])

        print(f"Optimal point: {result.x}")
        print(f"Function value: {result.fun:.6e}")
        print(f"Success: {result.success}")
        print(f"Close to (1, 3): {np.allclose(result.x, [1, 3], atol=1e-4)}")
        ```

---

**Exercise 2.**
Write a cost function that computes the sum of squared errors between a quadratic model $y = ax^2 + bx + c$ and the data `x = [0, 1, 2, 3, 4]`, `y = [1.0, 2.9, 9.1, 18.8, 33.2]`. Use `minimize` with the `args` parameter to pass the data to the cost function. Print the fitted coefficients.

??? success "Solution to Exercise 2"
        ```python
        import numpy as np
        from scipy import optimize

        def quadratic_sse(params, xdata, ydata):
            a, b, c = params
            predicted = a * xdata**2 + b * xdata + c
            return np.sum((ydata - predicted)**2)

        xdata = np.array([0, 1, 2, 3, 4])
        ydata = np.array([1.0, 2.9, 9.1, 18.8, 33.2])

        result = optimize.minimize(quadratic_sse, x0=[1, 1, 1], args=(xdata, ydata))

        a, b, c = result.x
        print(f"Fitted coefficients: a={a:.4f}, b={b:.4f}, c={c:.4f}")
        print(f"SSE: {result.fun:.6f}")
        print(f"Success: {result.success}")
        ```

---

**Exercise 3.**
Minimize the function $f(x) = e^x + e^{-2x}$ using `minimize` with bounds restricting $x$ to the interval $[-2, 2]$. Compare the result with and without bounds. Check `result.success` in both cases and print the optimal values.

??? success "Solution to Exercise 3"
        ```python
        import numpy as np
        from scipy import optimize

        def f(x):
            return np.exp(x) + np.exp(-2 * x)

        # Without bounds
        result_unbounded = optimize.minimize(f, x0=0)
        print(f"Unbounded: x = {result_unbounded.x[0]:.6f}, f(x) = {result_unbounded.fun:.6f}")
        print(f"  Success: {result_unbounded.success}")

        # With bounds
        bounds = [(-2, 2)]
        result_bounded = optimize.minimize(f, x0=0, bounds=bounds, method='L-BFGS-B')
        print(f"Bounded [-2, 2]: x = {result_bounded.x[0]:.6f}, f(x) = {result_bounded.fun:.6f}")
        print(f"  Success: {result_bounded.success}")
        ```
