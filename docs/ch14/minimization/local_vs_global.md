# Local vs Global Optimization

One of the fundamental challenges in optimization is that local minimization methods can get trapped in local minima — points that are lower than nearby points but not the global minimum. Understanding this problem and how to avoid it is crucial for real-world optimization.

!!! tip "Mental Model"
    Picture a hilly landscape with many valleys. A local optimizer is a hiker who always walks downhill and stops at the bottom of whichever valley they start in. A global optimizer is a helicopter that surveys the entire terrain before dropping the hiker into the deepest valley. The trade-off is simple: the helicopter costs more fuel (computation), but it finds the true lowest point.

---

## The Local Minima Problem

A cost function landscape can be visualized as a terrain with multiple valleys. Local minimization methods are like hiking downhill: they follow the slope and stop at the bottom of whichever valley they start in, without knowing if there's a deeper valley elsewhere.

### Understanding Local Minima

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

# Function with multiple local minima
def multi_minima(x):
    """Function with several local and one global minimum."""
    return np.sin(x) + 0.1 * x

# Plot the function
x = np.linspace(-2*np.pi, 2*np.pi, 1000)
y = multi_minima(x)

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(x, y, 'b-', linewidth=2, label='Objective function')
ax.set_xlabel('x')
ax.set_ylabel('f(x)')
ax.set_title('Function with Multiple Local Minima')
ax.grid(True, alpha=0.3)

# Find local minima from different starting points
starting_points = [-4*np.pi, -2*np.pi, 0, 2*np.pi, 4*np.pi]
colors = ['red', 'orange', 'green', 'purple', 'brown']

for start, color in zip(starting_points, colors):
    result = optimize.minimize(multi_minima, start, method='BFGS')
    ax.plot(result.x, result.fun, 'o', color=color, markersize=10,
            label=f'Start: {start:.1f}')
    ax.plot(start, multi_minima(start), 'x', color=color, markersize=8)

ax.legend()
plt.tight_layout()
plt.show()
```

### The Rosenbrock Challenge

The Rosenbrock function perfectly illustrates why local methods fail:

$$f(x, y) = (1-x)^2 + 100(y-x^2)^2$$

The global minimum is at $(1, 1)$, but the function has narrow, curved valley that gradient-based methods struggle to follow.

```python
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt

def rosenbrock(x):
    return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2

# Local minimization
starting_points = [
    np.array([-1, -1]),
    np.array([0, 0]),
    np.array([2, 2])
]

fig = plt.figure(figsize=(14, 5))

# 3D visualization
ax1 = fig.add_subplot(131, projection='3d')
x = np.linspace(-2, 3, 100)
y = np.linspace(-1, 4, 100)
X, Y = np.meshgrid(x, y)
Z = (1 - X)**2 + 100 * (Y - X**2)**2
ax1.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_zlabel('f(x, y)')

# Contour plot with optimization paths
ax2 = fig.add_subplot(132)
contour = ax2.contourf(X, Y, Z, levels=30, cmap='viridis')
ax2.plot(1, 1, 'r*', markersize=20, label='Global minimum')

for i, start in enumerate(starting_points):
    result = optimize.minimize(rosenbrock, start, method='BFGS')
    ax2.plot(start[0], start[1], 'go', markersize=8)
    ax2.plot(result.x[0], result.x[1], 'rs', markersize=8)
    ax2.annotate(f'Start {i+1}', xy=start, xytext=(start[0]+0.1, start[1]+0.1))

ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.set_title('Local Optimization Paths')
ax2.legend()

# Cost function value from different starting points
ax3 = fig.add_subplot(133)
costs = []
for start in starting_points:
    result = optimize.minimize(rosenbrock, start, method='BFGS')
    costs.append(result.fun)

ax3.bar(range(len(starting_points)), costs)
ax3.set_xlabel('Starting Point')
ax3.set_ylabel('Final Cost')
ax3.set_title('Local Minima Different Values')
ax3.set_yscale('log')

plt.tight_layout()
plt.show()
```

---

## Global Optimization Methods

When local minima are a concern, global optimization methods search more broadly across the parameter space.

### Differential Evolution

Differential evolution uses a population-based approach: multiple candidate solutions evolve over iterations by mutating and recombining.

**Characteristics:**
- Population-based (maintains many candidate solutions)
- No gradient required
- Very robust, rarely gets stuck in local minima
- Slower than local methods (more function evaluations)
- Works on non-smooth and discontinuous functions
- Good for black-box optimization

```python
from scipy import optimize
import numpy as np

def multi_peak(x):
    """Function with many local minima."""
    return np.sum(np.sin(x) * np.exp(-0.1 * np.sum(x**2)))

# Local method gets stuck
result_local = optimize.minimize(
    multi_peak,
    x0=[0, 0],
    method='BFGS'
)

# Global method finds true minimum
result_global = optimize.differential_evolution(
    multi_peak,
    bounds=[(-5, 5), (-5, 5)],
    seed=42
)

print(f"Local minimization:")
print(f"  Value: {result_local.fun:.6f}")
print(f"  x: {result_local.x}")
print(f"\nGlobal (differential_evolution):")
print(f"  Value: {result_global.fun:.6f}")
print(f"  x: {result_global.x}")
print(f"\nFunction evaluations - Local: {result_local.nfev}, Global: {result_global.nfev}")
```

**When to use:**
- Black-box optimization (no gradient available)
- Function has many local minima
- Non-smooth or discontinuous functions
- Can afford extra function evaluations

### Basin-Hopping

Basin-hopping combines local minimization with random jumps in parameter space. It minimizes locally, then makes a random step and minimizes again from the new location.

**Characteristics:**
- Local minimization with randomization
- Escapes local minima by jumping to new regions
- Faster than population-based methods
- Good balance between speed and global search
- Can use any local minimization method

```python
from scipy import optimize
import numpy as np

def f(x):
    """Challenging optimization problem."""
    return (x[0] - 2)**2 * (1 + np.sin(5*x[1])) + x[1]**2

# Local method
result_local = optimize.minimize(f, x0=[0, 0], method='L-BFGS-B')

# Basin hopping
minimizer_kwargs = {"method": "L-BFGS-B"}
result_basin = optimize.basinhopping(
    f,
    x0=[0, 0],
    minimizer_kwargs=minimizer_kwargs,
    niter=100,
    seed=42
)

print(f"Local optimization:")
print(f"  Value: {result_local.fun:.6f}")
print(f"  x: {result_local.x}")
print(f"\nBasin-hopping:")
print(f"  Value: {result_basin.fun:.6f}")
print(f"  x: {result_basin.x}")
```

**When to use:**
- Need faster global optimization than differential_evolution
- Problem has distinct basins
- Can provide good local minimizer
- Function evaluations are expensive

### Dual Annealing

Dual annealing is a variant of simulated annealing that combines global and local search strategies.

**Characteristics:**
- Simulated annealing variant
- Probabilistically accepts uphill moves to escape local minima
- Temperature gradually decreases
- Combines with local optimization
- Good for continuous optimization

```python
from scipy import optimize
import numpy as np

def nonconvex(x):
    """Highly non-convex function."""
    return (x[0]**2 + x[1]**2 - 5)**2 + (x[0] - x[1])**2

# Local minimization
result_local = optimize.minimize(nonconvex, [0, 0], method='L-BFGS-B')

# Dual annealing
result_annealing = optimize.dual_annealing(
    nonconvex,
    bounds=[(-3, 3), (-3, 3)],
    seed=42
)

print(f"Local: f = {result_local.fun:.6f}")
print(f"Dual annealing: f = {result_annealing.fun:.6f}")
```

**When to use:**
- Moderate-sized global optimization
- Bounds are naturally defined
- Don't want to tune population size (like in differential_evolution)

---

## Practical Strategies for Global Optimization

### Strategy 1: Multi-Start Local Optimization

Run local optimization from many random starting points and keep the best:

```python
from scipy import optimize
import numpy as np

def objective(x):
    return np.sin(x[0]) * np.cos(x[1]) + 0.1 * x[0]**2

best_result = None
best_value = float('inf')

# Try from 20 random starting points
np.random.seed(42)
for i in range(20):
    x0 = np.random.uniform(-2*np.pi, 2*np.pi, 2)
    result = optimize.minimize(objective, x0, method='L-BFGS-B')

    if result.fun < best_value:
        best_value = result.fun
        best_result = result

print(f"Best found: f = {best_result.fun:.6f}")
print(f"At: {best_result.x}")
```

### Strategy 2: Coarse Grid Search + Local Refinement

First scan the space coarsely, then refine promising regions:

```python
from scipy import optimize
import numpy as np
import matplotlib.pyplot as plt

def objective(x):
    return (x[0] - 2.5)**2 * np.sin(x[1]) + (x[1] - 3)**2

# Coarse grid search
x = np.linspace(-1, 6, 10)
y = np.linspace(-1, 6, 10)
X, Y = np.meshgrid(x, y)
Z = np.zeros_like(X)
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        Z[i, j] = objective([X[i, j], Y[i, j]])

# Find best grid point
best_idx = np.unravel_index(np.argmin(Z), Z.shape)
x0 = np.array([X[best_idx], Y[best_idx]])

print(f"Coarse grid best: f = {Z[best_idx]:.6f} at {x0}")

# Refine locally
result = optimize.minimize(objective, x0, method='L-BFGS-B')
print(f"Refined: f = {result.fun:.6f} at {result.x}")

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Grid search
ax = axes[0]
contour = ax.contourf(X, Y, Z, levels=20, cmap='viridis')
ax.plot(x0[0], x0[1], 'r*', markersize=20, label='Grid best')
ax.set_title('Coarse Grid Search')
plt.colorbar(contour, ax=ax)

# After refinement
Z_fine = np.zeros_like(X)
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        Z_fine[i, j] = objective([X[i, j], Y[i, j]])

ax = axes[1]
contour = ax.contourf(X, Y, Z_fine, levels=20, cmap='viridis')
ax.plot(result.x[0], result.x[1], 'r*', markersize=20, label='Refined')
ax.set_title('After Local Refinement')
plt.colorbar(contour, ax=ax)

plt.tight_layout()
plt.show()
```

### Strategy 3: Combining Multiple Approaches

Use different methods and compare results:

```python
from scipy import optimize
import numpy as np

def objective(x):
    return (x[0] - 2)**2 + 100*(x[1] - x[0]**2)**2

x0 = [0, 0]
bounds = [(-5, 5), (-5, 5)]

# Try multiple methods
results = {}

# Differential evolution
results['DE'] = optimize.differential_evolution(objective, bounds)

# Basin hopping
results['BH'] = optimize.basinhopping(objective, x0,
                                      minimizer_kwargs={'method': 'L-BFGS-B'},
                                      niter=100)

# Dual annealing
results['DA'] = optimize.dual_annealing(objective, bounds)

# Local L-BFGS-B
results['LBFGS'] = optimize.minimize(objective, x0, method='L-BFGS-B', bounds=bounds)

# Compare results
print("Method Comparison:")
print("-" * 50)
for method, result in results.items():
    value = result.fun if hasattr(result, 'fun') else result.get('fun', None)
    print(f"{method:<10}: f = {value:.2e}")

# Find and report best
best_method = min(results.items(), key=lambda x: x[1].fun if hasattr(x[1], 'fun') else float('inf'))
print(f"\nBest method: {best_method[0]}")
print(f"Optimal value: {best_method[1].fun:.2e}")
```

---

## Multimodal Optimization: Image Registration Example

The problem of aligning images demonstrates local minima challenges and solutions:

```python
from scipy import optimize
import numpy as np
import matplotlib.pyplot as plt

# Simulate an error surface with multiple local minima
# (similar to image alignment MSE landscape)
def alignment_error(shift):
    """
    Simulated image alignment error function.
    Has multiple local minima due to image periodicity.
    """
    main_error = (shift - 5)**2
    periodic_ripples = 2 * np.cos(shift)
    return main_error + periodic_ripples

# Plot the error surface
shifts = np.linspace(-5, 15, 1000)
errors = np.array([alignment_error(s) for s in shifts])

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(shifts, errors, 'b-', linewidth=2, label='Alignment error')
ax.set_xlabel('Image shift (pixels)')
ax.set_ylabel('MSE')
ax.set_title('Image Alignment Error Surface')
ax.grid(True, alpha=0.3)

# Local method from poor starting point
result_local = optimize.minimize(alignment_error, x0=-2, method='BFGS')
ax.plot(result_local.x, result_local.fun, 'rs', markersize=10,
        label='Local opt (x0=-2)')

# Global method
result_global = optimize.differential_evolution(alignment_error, bounds=[(-5, 15)])
ax.plot(result_global.x, result_global.fun, 'g*', markersize=15,
        label='Global opt')

ax.legend()
plt.tight_layout()
plt.show()

print(f"Local from x0=-2: shift = {result_local.x[0]:.2f}, error = {result_local.fun:.4f}")
print(f"Global: shift = {result_global.x[0]:.2f}, error = {result_global.fun:.4f}")
```

---

## Summary

**Key Insights:**

1. **Local methods** are fast but can get stuck in poor local minima
2. **Global methods** explore more thoroughly but cost more function evaluations
3. **Differential evolution** is robust and works on non-smooth functions
4. **Basin-hopping** balances speed and global search capability
5. **Multi-start** local optimization is simple and often effective
6. **Combine strategies**: Use coarse grid search → local refinement → verify globally

Choose based on:
- Problem complexity and number of local minima
- Computational budget (function evaluation cost)
- Need for accuracy vs speed
- Whether you can provide bounds or initial guesses

---

## Exercises

**Exercise 1.**
Define the Rastrigin function $f(\mathbf{x}) = 10n + \sum_{i=1}^{n}[x_i^2 - 10\cos(2\pi x_i)]$ for $n = 2$. Use `differential_evolution` with bounds $[-5.12, 5.12]$ for each variable to find its global minimum (which is 0 at the origin). Compare the result to a local `minimize` call from `x0 = [3, 3]`.

??? success "Solution to Exercise 1"
        ```python
        import numpy as np
        from scipy import optimize

        def rastrigin(x):
            n = len(x)
            return 10 * n + np.sum(x**2 - 10 * np.cos(2 * np.pi * x))

        # Global optimization
        result_global = optimize.differential_evolution(
            rastrigin, bounds=[(-5.12, 5.12)] * 2, seed=42
        )
        print(f"Global (DE): f = {result_global.fun:.6f}, x = {result_global.x}")

        # Local optimization from a poor starting point
        result_local = optimize.minimize(rastrigin, x0=[3, 3], method='BFGS')
        print(f"Local (BFGS from [3,3]): f = {result_local.fun:.6f}, x = {result_local.x}")
        ```

---

**Exercise 2.**
Use `basinhopping` with 200 iterations to minimize $f(x) = \sin(5x) \cdot (1 - \tanh(x^2))$ over the real line, starting from `x0 = 2`. Use L-BFGS-B as the local minimizer. Print the found minimum and compare it against 50 random multi-start local optimizations.

??? success "Solution to Exercise 2"
        ```python
        import numpy as np
        from scipy import optimize

        def f(x):
            return np.sin(5 * x) * (1 - np.tanh(x**2))

        # Basin-hopping
        result_bh = optimize.basinhopping(
            f, x0=2, niter=200,
            minimizer_kwargs={"method": "L-BFGS-B"}, seed=42
        )
        print(f"Basin-hopping: f = {result_bh.fun:.6f}, x = {result_bh.x[0]:.6f}")

        # Multi-start comparison
        np.random.seed(42)
        best_val = float('inf')
        best_x = None
        for _ in range(50):
            x0 = np.random.uniform(-5, 5)
            res = optimize.minimize(f, x0=x0, method='L-BFGS-B')
            if res.fun < best_val:
                best_val = res.fun
                best_x = res.x[0]

        print(f"Multi-start (50 trials): f = {best_val:.6f}, x = {best_x:.6f}")
        ```

---

**Exercise 3.**
Implement the "coarse grid + local refinement" strategy for the 2D function $f(x, y) = \cos(x)\sin(y) + 0.05(x^2 + y^2)$ on the domain $[-5, 5] \times [-5, 5]$. Evaluate on a 20x20 grid, pick the best grid point, then refine with `minimize`. Print the grid-best value and the refined value.

??? success "Solution to Exercise 3"
        ```python
        import numpy as np
        from scipy import optimize

        def f(x):
            return np.cos(x[0]) * np.sin(x[1]) + 0.05 * (x[0]**2 + x[1]**2)

        # Coarse grid search
        grid_x = np.linspace(-5, 5, 20)
        grid_y = np.linspace(-5, 5, 20)
        best_val = float('inf')
        best_point = None

        for xi in grid_x:
            for yi in grid_y:
                val = f([xi, yi])
                if val < best_val:
                    best_val = val
                    best_point = [xi, yi]

        print(f"Grid best: f = {best_val:.6f} at {best_point}")

        # Local refinement
        result = optimize.minimize(f, x0=best_point, method='L-BFGS-B')
        print(f"Refined: f = {result.fun:.6f} at {result.x}")
        ```
