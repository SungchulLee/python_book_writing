# Root Finding: Finding Zeros of Functions

Root finding is the problem of determining where a function equals zero: find $x$ such that $f(x) = 0$. This is one of the most fundamental problems in numerical computing with applications in solving equations, finding equilibrium points, and many other areas.

!!! tip "Mental Model"
    Root finding is like searching for sea level on a function's landscape -- the exact point where the curve crosses the horizontal axis. Bracketing methods (Brent, bisection) work like a binary search: they trap the crossing between two points of opposite sign and squeeze inward. Open methods (Newton, secant) are faster but riskier -- they extrapolate where the crossing should be and jump there, which can overshoot if the function is poorly behaved.

---

## Scalar Root Finding: scipy.optimize.root_scalar()

For single-variable functions, `root_scalar()` provides a streamlined interface with several algorithms optimized for reliability and speed.

### Basic Usage

```python
from scipy.optimize import root_scalar
import numpy as np

# Simple quadratic: x^2 - 4 = 0
def f(x):
    return x**2 - 4

# Find the positive root
result = root_scalar(f, bracket=[0, 5])

print(f"Root found: x = {result.root:.6f}")
print(f"Function value at root: f(x) = {result.fun:.2e}")
print(f"Converged: {result.converged}")
print(f"Iterations: {result.iterations}")
print(f"Function evaluations: {result.function_calls}")
```

### Finding All Roots

```python
from scipy.optimize import root_scalar
import numpy as np
import matplotlib.pyplot as plt

# Cubic: x^3 - 2x^2 - 5x + 6 = 0
# Has roots at x = -2, 1, 3
def f(x):
    return x**3 - 2*x**2 - 5*x + 6

# Plot to visualize roots
x = np.linspace(-3, 4, 1000)
y = f(x)

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, y, 'b-', linewidth=2, label='f(x)')
ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
ax.grid(True, alpha=0.3)

# Find roots in different brackets
brackets = [[-3, 0], [0, 2], [2, 4]]
roots = []

for bracket in brackets:
    result = root_scalar(f, bracket=bracket)
    roots.append(result.root)
    ax.plot(result.root, 0, 'ro', markersize=10)

ax.set_xlabel('x')
ax.set_ylabel('f(x)')
ax.set_title('Finding Multiple Roots')
ax.legend()
plt.tight_layout()
plt.show()

print(f"Roots found: {roots}")
```

---

## Root-Finding Methods

Different algorithms have different strengths. `root_scalar()` supports several:

### Bracketing Methods (Guaranteed Convergence)

These methods require the function to have opposite signs at the bracket endpoints: $f(a) \cdot f(b) < 0$.

#### Brent's Method

The best general-purpose method: combines bisection, secant, and inverse quadratic interpolation.

**Characteristics:**
- Guaranteed convergence (if bracket brackets a root)
- Very fast in practice
- Doesn't require derivatives
- Default method for `root_scalar()`

```python
from scipy.optimize import root_scalar
import numpy as np

def f(x):
    return x**3 - 2*x + 1

# Brent's method (default for bracketing)
result = root_scalar(f, bracket=[-2, 1], method='brentq')

print(f"Brent's method:")
print(f"  Root: {result.root:.10f}")
print(f"  Iterations: {result.iterations}")
print(f"  Function evals: {result.function_calls}")
```

#### Bisection

Simple and bulletproof: repeatedly halves the bracket containing the root.

**Characteristics:**
- Very reliable
- Slower than Brent
- Predictable convergence rate
- Good for ill-behaved functions

```python
from scipy.optimize import root_scalar

def f(x):
    return x**3 - 2*x + 1

# Bisection
result = root_scalar(f, bracket=[-2, 1], method='bisect')

print(f"Bisection:")
print(f"  Root: {result.root:.10f}")
print(f"  Iterations: {result.iterations}")
print(f"  Function evals: {result.function_calls}")
```

### Open Methods (Faster but May Diverge)

These methods don't require a bracket but may fail to converge:

#### Newton-Raphson

Uses both function and derivative. Very fast when derivative is available.

**Characteristics:**
- Requires derivative (or numerical gradient)
- Quadratic convergence (very fast)
- May diverge for poor starting points
- Best when derivative is cheap to compute

```python
from scipy.optimize import root_scalar
import numpy as np

def f(x):
    return x**3 - 2*x + 1

def df(x):
    """Derivative."""
    return 3*x**2 - 2

# Newton's method
result = root_scalar(f, x0=0, fprime=df, method='newton')

print(f"Newton's method:")
print(f"  Root: {result.root:.10f}")
print(f"  Iterations: {result.iterations}")
print(f"  Function evals: {result.function_calls}")
```

#### Secant Method

Uses finite differences to approximate the derivative. Good balance of speed and simplicity.

**Characteristics:**
- No derivative required
- Good convergence rate (super-linear)
- Faster than bisection, slower than Newton
- Requires two initial points or guess + step

```python
from scipy.optimize import root_scalar

def f(x):
    return x**3 - 2*x + 1

# Secant method
result = root_scalar(f, x0=0, x1=1, method='secant')

print(f"Secant method:")
print(f"  Root: {result.root:.10f}")
print(f"  Iterations: {result.iterations}")
print(f"  Function evals: {result.function_calls}")
```

### Comparison of Methods

```python
from scipy.optimize import root_scalar
import numpy as np

def f(x):
    return x**3 - 2*x + 1

def df(x):
    return 3*x**2 - 2

methods = {
    'brentq': {'bracket': [-2, 1]},
    'bisect': {'bracket': [-2, 1]},
    'newton': {'x0': 0, 'fprime': df},
    'secant': {'x0': 0, 'x1': 1},
}

print("Method Comparison:")
print("-" * 70)
print(f"{'Method':<15} {'Root':<15} {'Iterations':<15} {'F-evals':<15}")
print("-" * 70)

for method, kwargs in methods.items():
    result = root_scalar(f, method=method, **kwargs)
    print(f"{method:<15} {result.root:<15.8f} {result.iterations:<15} {result.function_calls:<15}")
```

---

## Systems of Equations: scipy.optimize.root()

For multiple equations in multiple unknowns, use `root()`:

$$\begin{cases}
f_1(x, y) = 0 \\
f_2(x, y) = 0
\end{cases}$$

### Basic Example

```python
from scipy.optimize import root
import numpy as np

def system(vars):
    """System of equations to solve."""
    x, y = vars
    eq1 = x**2 + y**2 - 1      # Circle: x^2 + y^2 = 1
    eq2 = x - y                  # Line: x = y
    return [eq1, eq2]

# Solve the system
result = root(system, x0=[0.5, 0.5])

x_sol, y_sol = result.x

print(f"Solution: x = {x_sol:.6f}, y = {y_sol:.6f}")
print(f"Verification:")
print(f"  x^2 + y^2 = {x_sol**2 + y_sol**2:.6f} (should be 1)")
print(f"  x - y = {x_sol - y_sol:.2e} (should be ~0)")
```

### Methods for Root Finding of Systems

```python
from scipy.optimize import root

def system(vars):
    x, y = vars
    return [x**2 + y**2 - 1, x - y]

# Different methods
methods = ['hybr', 'lm', 'broyden1', 'broyden2']

print("System Root Finding Methods:")
print("-" * 60)
print(f"{'Method':<15} {'Solution':<30} {'Success':<10}")
print("-" * 60)

for method in methods:
    try:
        result = root(system, x0=[0.5, 0.5], method=method)
        print(f"{method:<15} ({result.x[0]:.4f}, {result.x[1]:.4f})       {result.success}")
    except Exception as e:
        print(f"{method:<15} Failed: {str(e)[:25]}")
```

**Available Methods:**
- `hybr`: Hybrid Powell method (default, most robust)
- `lm`: Levenberg-Marquardt (good for least-squares)
- `broyden1`, `broyden2`: Broyden's method variants
- `linearmixing`, `diagbroyden`, `excitingmixing`: Variants

### Jacobian (Derivative Matrix)

For large systems, provide the Jacobian matrix for better performance:

```python
from scipy.optimize import root
import numpy as np

def system(vars):
    x, y = vars
    return [
        x**2 + y**2 - 1,
        x - y
    ]

def jacobian(vars):
    """Jacobian matrix: [[∂f1/∂x, ∂f1/∂y], [∂f2/∂x, ∂f2/∂y]]."""
    x, y = vars
    return [
        [2*x, 2*y],
        [1, -1]
    ]

# With Jacobian
result = root(system, x0=[0.5, 0.5], jac=jacobian)

print(f"Solution with Jacobian: {result.x}")
print(f"Function evaluations: {result.nfev}")
```

---

## Practical Applications

### Finding Equilibrium Points

An equilibrium occurs where forces or flows balance:

```python
from scipy.optimize import root_scalar
import numpy as np

# Predator-prey equilibrium: dN/dt = 0
# Prey: dN/dt = r*N - a*N*P = 0
# With P (predators) constant, find N where dN/dt = 0

r = 0.5      # Prey growth rate
a = 0.01     # Predation rate
P = 20       # Predator population

def equilibrium(N):
    return r * N - a * N * P

# Find prey equilibrium
result = root_scalar(equilibrium, bracket=[0, 100])
N_eq = result.root

print(f"Equilibrium prey population: {N_eq:.1f}")
print(f"Check: dN/dt = {equilibrium(N_eq):.2e} ≈ 0")
```

### Solving Transcendental Equations

Equations that mix polynomial, exponential, and trigonometric terms:

```python
from scipy.optimize import root_scalar
import numpy as np
import matplotlib.pyplot as plt

# Transcendental equation: tan(x) = x
# Plotting shows roots exist
def f(x):
    return np.tan(x) - x

# Plot to understand the function
x = np.linspace(-2*np.pi, 2*np.pi, 2000)
# Avoid discontinuities of tan
x = x[(x % np.pi) > 0.1]
y = np.tan(x) - x

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(x, y, 'b-', linewidth=1.5)
ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
ax.set_ylim([-10, 10])
ax.set_xlabel('x')
ax.set_ylabel('tan(x) - x')
ax.set_title('Transcendental Equation: tan(x) = x')
ax.grid(True, alpha=0.3)

# Find roots in different regions
roots = []
for x0 in [0.5, 4, 7, 10]:
    try:
        result = root_scalar(f, bracket=[x0, x0+0.9], method='brentq')
        roots.append(result.root)
        ax.plot(result.root, 0, 'ro', markersize=8)
    except:
        pass

plt.tight_layout()
plt.show()

print(f"Roots found: {roots}")
```

### Implicit Equation Solving

When you can't solve for y explicitly:

```python
from scipy.optimize import root_scalar
import numpy as np

# Implicit equation: x*exp(y) + y = 1
# Want to find y for a given x
def implicit_eq(y, x):
    return x * np.exp(y) + y - 1

# For x = 0.5, find y
x_val = 0.5

# Need to find bracket where function changes sign
y_test = np.linspace(-2, 1, 100)
f_test = [implicit_eq(y, x_val) for y in y_test]

# Find where function changes sign
for i in range(len(f_test)-1):
    if f_test[i] * f_test[i+1] < 0:
        result = root_scalar(lambda y: implicit_eq(y, x_val),
                            bracket=[y_test[i], y_test[i+1]])
        print(f"For x = {x_val}: y = {result.root:.6f}")
        break
```

---

## Error Handling

Root finding can fail if initial guesses are poor or the problem is ill-posed:

```python
from scipy.optimize import root_scalar
import numpy as np

def f(x):
    return x**2 + 1  # No real roots!

try:
    result = root_scalar(f, bracket=[-2, 2])
    print(f"Root: {result.root}")
except ValueError as e:
    print(f"Error: {e}")
    print("The function doesn't change sign in the bracket.")
    print("Check that f(a) and f(b) have opposite signs.")

# For systems of equations:
from scipy.optimize import root

def system(vars):
    x, y = vars
    return [x**2 + 1, y**2 + 1]  # No solution

result = root(system, x0=[0, 0])
print(f"\nSystem result:")
print(f"  Converged: {result.success}")
print(f"  Message: {result.message}")
```

---

## Comparison: minimize() vs root_scalar()

Sometimes the same problem can be formulated as either optimization or root-finding:

```python
from scipy.optimize import root_scalar, minimize
import numpy as np

# Problem: Find where f(x) = 0
def f(x):
    return x**3 - 2*x + 1

# Method 1: Direct root finding
result_root = root_scalar(f, bracket=[-2, 1])

# Method 2: Minimize |f(x)|
def abs_f(x):
    return np.abs(f(x))

result_opt = minimize(abs_f, x0=0)

print(f"Root-finding: x = {result_root.root:.10f}")
print(f"Optimization:  x = {result_opt.x[0]:.10f}")
print(f"\nRoot-finding is faster and more reliable for this problem.")
```

---

## Summary

**Key Points:**

1. **root_scalar()** for single equations: Use Brent's method (default) for reliability
2. **Bracketing methods** (bisect, brentq): Guaranteed to work, needs function sign change
3. **Newton's method**: Very fast but needs derivative
4. **Secant method**: Good balance, no derivative needed
5. **root()** for systems: Use 'hybr' method (default) for robustness
6. **Provide Jacobian** for large systems to improve performance
7. **Always verify** the solution by plugging back into the equation

**Choose Based On:**
- Single equation? → root_scalar()
- Multiple equations? → root()
- Have derivative? → Newton's method
- No derivative, single eq? → Brent or Secant
- Guaranteed convergence needed? → Bisection or Brent

---

## Exercises

**Exercise 1.**
Use `root_scalar` with Newton's method to find the root of $f(x) = e^x - 3x$ near $x = 1$. Provide both the function and its derivative $f'(x) = e^x - 3$. Print the root, number of iterations, and verify by evaluating $f$ at the root.

??? success "Solution to Exercise 1"
        ```python
        import numpy as np
        from scipy.optimize import root_scalar

        def f(x):
            return np.exp(x) - 3 * x

        def df(x):
            return np.exp(x) - 3

        result = root_scalar(f, x0=1, fprime=df, method='newton')

        print(f"Root: {result.root:.10f}")
        print(f"f(root) = {f(result.root):.2e}")
        print(f"Iterations: {result.iterations}")
        print(f"Converged: {result.converged}")
        ```

---

**Exercise 2.**
Use `scipy.optimize.root` to solve the nonlinear system $x^2 + y^2 = 4$ and $xy = 1$ starting from `x0 = [1.5, 0.5]`. Provide the Jacobian matrix. Print both solutions (there are multiple; try different starting points) and verify each.

??? success "Solution to Exercise 2"
        ```python
        import numpy as np
        from scipy.optimize import root

        def system(vars):
            x, y = vars
            return [x**2 + y**2 - 4, x * y - 1]

        def jacobian(vars):
            x, y = vars
            return [[2*x, 2*y], [y, x]]

        # First solution
        result1 = root(system, x0=[1.5, 0.5], jac=jacobian)
        print(f"Solution 1: x={result1.x[0]:.6f}, y={result1.x[1]:.6f}")
        print(f"  Verify: x^2+y^2={result1.x[0]**2+result1.x[1]**2:.6f}, xy={result1.x[0]*result1.x[1]:.6f}")

        # Second solution (different starting point)
        result2 = root(system, x0=[0.5, 1.5], jac=jacobian)
        print(f"Solution 2: x={result2.x[0]:.6f}, y={result2.x[1]:.6f}")
        print(f"  Verify: x^2+y^2={result2.x[0]**2+result2.x[1]**2:.6f}, xy={result2.x[0]*result2.x[1]:.6f}")
        ```

---

**Exercise 3.**
The equation $x = \cos(x)$ has a fixed point near $x \approx 0.739$. Rewrite this as $f(x) = x - \cos(x) = 0$ and find the root using three methods: bisection on $[0, 1]$, Brent on $[0, 1]$, and secant with `x0=0, x1=1`. Compare the number of function evaluations for each method.

??? success "Solution to Exercise 3"
        ```python
        from scipy.optimize import root_scalar
        import numpy as np

        def f(x):
            return x - np.cos(x)

        # Bisection
        res_bisect = root_scalar(f, bracket=[0, 1], method='bisect')
        print(f"Bisection: root={res_bisect.root:.10f}, f_evals={res_bisect.function_calls}")

        # Brent
        res_brent = root_scalar(f, bracket=[0, 1], method='brentq')
        print(f"Brent:     root={res_brent.root:.10f}, f_evals={res_brent.function_calls}")

        # Secant
        res_secant = root_scalar(f, x0=0, x1=1, method='secant')
        print(f"Secant:    root={res_secant.root:.10f}, f_evals={res_secant.function_calls}")
        ```
