# SciPy Optimize Overview

Function optimization is fundamental to scientific computing. Whether fitting a model to data, finding equilibrium points, or tuning parameters to minimize error, optimization algorithms are indispensable tools. The `scipy.optimize` module provides a comprehensive set of methods for solving these problems across a wide range of complexity levels.

!!! tip "Mental Model"
    The `scipy.optimize` module answers one core question in several forms: "What input makes this function's output as small (or zero) as possible?" Minimization finds the lowest valley, root finding locates where the function crosses zero, and curve fitting minimizes the gap between a model and data. Every tool in the module is a variation on this theme, differing only in what constraints you impose and how the search is conducted.

---

## What is Optimization?

Optimization is the process of finding parameter values that either minimize or maximize an objective function. In most cases, we focus on **minimization** — finding parameters $\mathbf{x}$ that minimize some cost function $f(\mathbf{x})$.

### Why Optimization Matters

Consider a practical scenario: you have experimental measurements and want to fit a mathematical model to them. The quality of fit can be quantified using a cost function, such as the sum of squared errors:

$$\text{Cost} = \sum_{i=1}^{n} (y_i - \hat{y}_i(\mathbf{x}))^2$$

where $y_i$ are observations and $\hat{y}_i(\mathbf{x})$ are predictions from your model with parameters $\mathbf{x}$. Optimization finds the parameters that minimize this cost.

### Real-World Applications

- **Machine Learning**: Training neural networks by minimizing loss functions
- **Engineering**: Designing structures to minimize weight or stress
- **Finance**: Portfolio optimization to maximize returns for given risk
- **Scientific Computing**: Finding equilibrium states or solving nonlinear equations
- **Image Processing**: Image registration by aligning multiple images

---

## Module Organization

The `scipy.optimize` module is organized around several key problems:

### 1. Unconstrained Minimization

Find $\mathbf{x}$ that minimizes $f(\mathbf{x})$ with no restrictions on $\mathbf{x}$.

```python
from scipy import optimize

def f(x):
    return (x - 3)**2

result = optimize.minimize(f, x0=0)
print(result.x)  # Near 3
```

**Key Functions:**

- `minimize()`: General-purpose minimizer supporting multiple algorithms
- `minimize_scalar()`: Specialized for single-variable functions

### 2. Constrained Minimization

Find $\mathbf{x}$ that minimizes $f(\mathbf{x})$ subject to constraints like $\mathbf{x} \geq 0$ or $g(\mathbf{x}) = 0$.

```python
from scipy import optimize

constraints = {'type': 'ineq', 'fun': lambda x: x[0]}  # x >= 0
result = optimize.minimize(f, x0=0, constraints=constraints)
```

**Key Functions:**

- `minimize()` with `constraints` and `bounds` arguments
- `LinearConstraint()`, `NonlinearConstraint()`: For structured constraints

### 3. Curve Fitting

Fit model parameters to observed data by minimizing the difference between predictions and observations.

```python
from scipy import optimize
import numpy as np

xdata = np.array([1, 2, 3, 4, 5])
ydata = np.array([2, 4, 6, 8, 10])

def model(x, a, b):
    return a * x + b

params, _ = optimize.curve_fit(model, xdata, ydata)
```

**Key Functions:**

- `curve_fit()`: Nonlinear least squares curve fitting
- `least_squares()`: General least squares with bounds and regularization

### 4. Root Finding

Find values of $\mathbf{x}$ where $f(\mathbf{x}) = 0$.

```python
from scipy import optimize

def f(x):
    return x**2 - 4

root = optimize.brentq(f, 0, 3)  # Finds x = 2
```

**Key Functions:**

- `root_scalar()`: For scalar functions
- `root()`: For systems of equations
- `brentq()`, `newton()`: Specialized scalar root finders

### 5. Linear Programming

Minimize $\mathbf{c}^T \mathbf{x}$ subject to linear constraints.

```python
from scipy import optimize

c = [1, 2]  # Coefficients to minimize
A_ub = [[1, 1], [1, -1]]  # Inequality constraint coefficients
b_ub = [3, 1]

result = optimize.linprog(c, A_ub=A_ub, b_ub=b_ub)
```

**Key Functions:**

- `linprog()`: Linear programming solver

### 6. Global Optimization

Find global minima, not just local ones, often at higher computational cost.

```python
from scipy import optimize

# Differential evolution
result = optimize.differential_evolution(f, bounds=[(0, 10)])
```

**Key Functions:**

- `differential_evolution()`: Stochastic population-based method
- `basinhopping()`: Local minimization with random jumps
- `dual_annealing()`: Simulated annealing variant

---

## When to Use Each Method

### Local vs Global Optimization

| Scenario | Method | When to Use |
|:---------|:-------|:-----------|
| Small, smooth problems | `minimize()` | Fast convergence, simple setup |
| Many local minima | `basinhopping()` | Want to escape local traps |
| High-dimensional global | `differential_evolution()` | Black-box optimization, no gradients |
| Simpler global search | `dual_annealing()` | Larger search ranges, moderate computation |

### Gradient Information

| Scenario | Methods |
|:---------|:---------|
| Have gradient/derivative | BFGS, L-BFGS-B, CG (faster, more accurate) |
| No gradient available | Nelder-Mead, Powell, differential_evolution |
| Can use finite differences | Most methods can auto-estimate gradients |

---

## Module Structure

```
scipy.optimize
├── minimize()              # General minimization
├── minimize_scalar()       # 1D minimization
├── curve_fit()             # Nonlinear least squares
├── least_squares()         # Advanced least squares
├── root_scalar()           # Scalar root finding
├── root()                  # System root finding
├── linprog()               # Linear programming
├── basinhopping()          # Global optimization with local search
├── differential_evolution()# Population-based global optimization
├── dual_annealing()        # Simulated annealing variant
├── LinearConstraint()      # Constraint object
├── NonlinearConstraint()   # Constraint object
└── Bounds()                # Bounds object
```

---

## Typical Workflow

### Step 1: Define Your Cost Function

```python
import numpy as np

def cost_function(params, data, predictions):
    """Compute difference between data and predictions."""
    residuals = data - predictions(params)
    return np.sum(residuals**2)
```

### Step 2: Choose Initial Parameters

```python
x0 = np.array([1.0, 1.0])  # Initial guess
```

### Step 3: Set Up Constraints/Bounds (if needed)

```python
bounds = [(0, 10), (0, 10)]  # Each param: lower, upper bound
```

### Step 4: Call Optimizer

```python
result = optimize.minimize(cost_function, x0,
                          args=(data, predictions),
                          bounds=bounds,
                          method='L-BFGS-B')
```

### Step 5: Inspect Results

```python
print(f"Success: {result.success}")
print(f"Optimal parameters: {result.x}")
print(f"Final cost: {result.fun}")
print(f"Iterations: {result.nit}")
```

---

## Key Concepts

### Objective Function (Cost Function)

The function you're trying to minimize. Good cost functions are:

- Smooth and continuous (helps most algorithms)
- Computable at any point in parameter space
- Meaningful for your problem

### Local vs Global Minima

A **local minimum** is lower than nearby points but not globally lowest. Gradient-based methods easily get trapped in local minima.

```python
# This function has multiple local minima
def f(x):
    return np.sin(x) + 0.1 * x

# Different starting points find different minima
optimize.minimize(f, x0=0)    # Finds one local minimum
optimize.minimize(f, x0=10)   # Finds a different one
optimize.differential_evolution(f, bounds=[(-10, 10)])  # Finds global
```

### Convergence Criteria

Algorithms stop when:

- Changes in parameters become very small
- Changes in cost become very small
- Maximum iterations reached
- Cost gradient approaches zero (for gradient-based methods)

---

## Next Steps

The remaining sections of this chapter cover:

1. **Minimization Basics**: Introduction to `minimize()` with simple examples
2. **Optimization Methods**: Detailed comparison of different algorithms
3. **Local vs Global**: Strategies for avoiding local minima
4. **Constrained Optimization**: Adding restrictions to parameter values
5. **Curve Fitting**: Specialized optimization for fitting models to data
6. **Root Finding**: Finding zeros of functions

Each section builds intuition with practical examples and guidance on method selection.

---

## Exercises

**Exercise 1.**
Write a function `find_best_method` that takes a 1D objective function and a search range, then runs `minimize_scalar` (bounded), `minimize` (Nelder-Mead), and `differential_evolution` on it. Return a dictionary mapping each method name to its result object. Print which method found the lowest function value.

??? success "Solution to Exercise 1"
        ```python
        import numpy as np
        from scipy import optimize

        def find_best_method(func, search_range):
            results = {}

            # minimize_scalar with bounded method
            res_scalar = optimize.minimize_scalar(
                func, bounds=search_range, method='bounded'
            )
            results['minimize_scalar'] = res_scalar

            # minimize with Nelder-Mead
            x0 = (search_range[0] + search_range[1]) / 2
            res_nm = optimize.minimize(func, x0=x0, method='Nelder-Mead')
            results['Nelder-Mead'] = res_nm

            # differential_evolution
            res_de = optimize.differential_evolution(func, bounds=[search_range])
            results['differential_evolution'] = res_de

            # Find best
            best_name = min(results, key=lambda k: results[k].fun)
            print(f"Best method: {best_name} with f = {results[best_name].fun:.6e}")

            return results

        # Test
        def objective(x):
            return np.sin(x) + 0.1 * x**2

        results = find_best_method(objective, (-5, 5))
        for name, res in results.items():
            print(f"{name}: f = {res.fun:.6f}")
        ```

---

**Exercise 2.**
Using `scipy.optimize.curve_fit`, fit both a linear model and a quadratic model to the data `x = [0, 1, 2, 3, 4, 5]`, `y = [0.1, 2.3, 4.1, 6.5, 8.2, 10.8]`. Compute the residual sum of squares for each model and print which model fits better.

??? success "Solution to Exercise 2"
        ```python
        import numpy as np
        from scipy.optimize import curve_fit

        x = np.array([0, 1, 2, 3, 4, 5])
        y = np.array([0.1, 2.3, 4.1, 6.5, 8.2, 10.8])

        def linear(x, a, b):
            return a * x + b

        def quadratic(x, a, b, c):
            return a * x**2 + b * x + c

        params_lin, _ = curve_fit(linear, x, y)
        params_quad, _ = curve_fit(quadratic, x, y)

        rss_lin = np.sum((y - linear(x, *params_lin))**2)
        rss_quad = np.sum((y - quadratic(x, *params_quad))**2)

        print(f"Linear fit: a={params_lin[0]:.4f}, b={params_lin[1]:.4f}, RSS={rss_lin:.4f}")
        print(f"Quadratic fit: a={params_quad[0]:.4f}, b={params_quad[1]:.4f}, c={params_quad[2]:.4f}, RSS={rss_quad:.4f}")

        if rss_quad < rss_lin:
            print("Quadratic model fits better (lower RSS).")
        else:
            print("Linear model fits better (lower RSS).")
        ```

---

**Exercise 3.**
Use `scipy.optimize.root_scalar` with Brent's method to find all three roots of the polynomial $f(x) = x^3 - 6x^2 + 11x - 6$ by supplying three different bracket intervals. Verify each root by evaluating $f$ at the found value.

??? success "Solution to Exercise 3"
        ```python
        import numpy as np
        from scipy.optimize import root_scalar

        def f(x):
            return x**3 - 6*x**2 + 11*x - 6

        # The roots are 1, 2, 3. Use brackets around each.
        brackets = [(0.5, 1.5), (1.5, 2.5), (2.5, 3.5)]

        for bracket in brackets:
            result = root_scalar(f, bracket=bracket, method='brentq')
            print(f"Bracket {bracket}: root = {result.root:.10f}, f(root) = {f(result.root):.2e}")
        ```
