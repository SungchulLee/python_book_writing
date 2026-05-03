# Optimization Methods

SciPy's `minimize()` function supports numerous optimization algorithms. Each has different strengths, weaknesses, and computational costs. Understanding these differences is crucial for solving optimization problems efficiently.

!!! tip "Mental Model"
    Optimization methods sit on a spectrum: at one end, gradient-free methods (Nelder-Mead, Powell) treat the function as a black box and poke around to find lower values. At the other end, Newton-type methods use first and second derivatives to take precise, large steps. More information about the function means fewer steps to the answer, but each step costs more to compute. Pick your method based on what you know about your function and how expensive it is to evaluate.

---

## Gradient-Free Methods

These methods do not require gradient information and often work well on noisy or non-smooth functions.

### Nelder-Mead Simplex Method

The Nelder-Mead method maintains a simplex (a geometric shape in $n$-dimensional space) and iteratively moves away from the worst point.

**Characteristics:**
- No gradient required
- Works reasonably well in low dimensions (< 10)
- Slower convergence than gradient-based methods
- Robust to noise and non-smoothness
- Default method in older SciPy versions

```python
from scipy import optimize
import numpy as np

def noisy_function(x):
    """Function with some noise."""
    return (x[0] - 2)**2 + (x[1] - 3)**2 + 0.01 * np.random.randn()

# Nelder-Mead
result = optimize.minimize(
    noisy_function,
    x0=[0, 0],
    method='Nelder-Mead',
    options={'maxiter': 5000}
)

print(f"Nelder-Mead result: {result.x}")
print(f"Iterations: {result.nit}")
print(f"Function evaluations: {result.nfev}")
```

**When to use:**
- Noisy objective functions
- Non-smooth functions
- Low-dimensional problems
- When you have no gradient information

### Powell's Method

Powell's method uses conjugate direction methods and performs line searches along successive dimensions.

**Characteristics:**
- No gradient required
- Good for smooth functions
- Often faster than Nelder-Mead
- Works well for dimension < 100
- Can be sensitive to poor starting points

```python
from scipy import optimize

def rosenbrock(x):
    return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2

# Powell's method
result = optimize.minimize(
    rosenbrock,
    x0=[0, 0],
    method='Powell'
)

print(f"Powell result: {result.x}")
print(f"Function value: {result.fun:.2e}")
print(f"Iterations: {result.nit}")
print(f"Function evaluations: {result.nfev}")
```

**When to use:**
- Smooth but gradient-free optimization
- Medium dimensions
- Image registration and alignment
- When you need good speed without gradient computation

---

## Gradient-Based Methods

These methods use the gradient (first derivative) to guide the search. They're usually faster but require either analytical gradients or numerical gradient estimation.

### Gradient Descent (Steepest Descent)

The simplest gradient-based method: move in the direction opposite to the gradient.

**Characteristics:**
- Slow convergence
- Requires gradient
- Simple to understand
- Not typically recommended (BFGS is usually better)

```python
from scipy.optimize import minimize
import numpy as np

def quadratic(x):
    return (x[0] - 2)**2 + (x[1] - 3)**2

def quadratic_grad(x):
    return np.array([2*(x[0] - 2), 2*(x[1] - 3)])

# Gradient descent
result = minimize(
    quadratic,
    x0=[0, 0],
    method='BFGS',  # Default is BFGS, not pure gradient descent
    jac=quadratic_grad
)

print(f"Result: {result.x}")
```

### BFGS (Broyden-Fletcher-Goldfarb-Shanno)

BFGS is a quasi-Newton method that approximates the inverse Hessian (second derivatives).

**Characteristics:**
- Uses first-order derivatives (gradients)
- Excellent convergence for smooth problems
- Efficient: requires only gradients, not Hessians
- Default method for unconstrained optimization
- Robust and widely used
- Requires storing an $n \times n$ matrix (memory for large $n$)

```python
from scipy import optimize
import numpy as np

def quadratic(x):
    return (x[0] - 2)**2 + 3*(x[1] - 3)**2

def quadratic_grad(x):
    return np.array([2*(x[0] - 2), 6*(x[1] - 3)])

# With gradient
result = optimize.minimize(
    quadratic,
    x0=[0, 0],
    method='BFGS',
    jac=quadratic_grad
)

print(f"BFGS with gradient: {result.x}")
print(f"Iterations: {result.nit}")
print(f"Function evaluations: {result.nfev}")

# Without gradient (finite differences)
result2 = optimize.minimize(
    quadratic,
    x0=[0, 0],
    method='BFGS'
)

print(f"BFGS with finite differences: {result2.x}")
print(f"Function evaluations: {result2.nfev}")
```

**When to use:**
- Smooth, continuous objective functions
- When gradient is available or easily computed
- Medium to large-scale problems
- Generally the first choice for unconstrained optimization

### L-BFGS-B (Limited Memory BFGS with Bounds)

L-BFGS-B is BFGS with limited memory (useful for large problems) and built-in bounds support.

**Characteristics:**
- Limited memory version of BFGS (uses $\mathcal{O}(m \times n)$ memory instead of $\mathcal{O}(n^2)$)
- Handles bounds naturally
- Good for large-scale problems
- Can handle inequality constraints via bounds
- Typically requires about 5-10 previous iterations to approximate Hessian

```python
from scipy import optimize
import numpy as np

def f(x):
    return np.sum((x - np.arange(1, len(x) + 1))**2)

def grad_f(x):
    return 2 * (x - np.arange(1, len(x) + 1))

# Large problem
x0 = np.zeros(1000)

# L-BFGS-B is much more efficient than BFGS for this
result = optimize.minimize(
    f,
    x0,
    method='L-BFGS-B',
    jac=grad_f,
    bounds=[(0, None)] * 1000  # All parameters >= 0
)

print(f"Optimal value: {result.fun:.2e}")
print(f"Iterations: {result.nit}")
```

**When to use:**
- Large-scale problems (thousands of variables)
- When you need to constrain parameters to ranges
- Limited memory available
- Problems where BFGS runs out of memory

### Conjugate Gradient (CG)

CG uses conjugate directions to achieve faster convergence than steepest descent.

**Characteristics:**
- Requires gradient
- Good for large sparse problems
- Converges in $n$ iterations for quadratic functions
- Sensitive to numerical accuracy
- Memory efficient

```python
from scipy import optimize
import numpy as np

def quadratic(x):
    A = np.array([[10, 1], [1, 10]])
    return 0.5 * x @ A @ x

def quadratic_grad(x):
    A = np.array([[10, 1], [1, 10]])
    return A @ x

result = optimize.minimize(
    quadratic,
    x0=[1, 1],
    method='CG',
    jac=quadratic_grad
)

print(f"CG result: {result.x}")
print(f"Iterations: {result.nit}")
```

**When to use:**
- Very large-scale smooth problems
- When memory is limited
- Problems with sparse structure
- Quadratic or nearly quadratic functions

---

## Comparison of Methods

### Performance on Rosenbrock Function

```python
import numpy as np
from scipy import optimize
import time

def rosenbrock(x):
    return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2

def rosenbrock_grad(x):
    dfdx0 = 2*(x[0] - 1) + 100*2*(x[1] - x[0]**2)*(-2*x[0])
    dfdx1 = 100*2*(x[1] - x[0]**2)
    return np.array([dfdx0, dfdx1])

methods = ['Nelder-Mead', 'Powell', 'BFGS', 'L-BFGS-B', 'CG']
results_dict = {}

for method in methods:
    if method in ['BFGS', 'CG']:
        result = optimize.minimize(
            rosenbrock,
            [0, 0],
            method=method,
            jac=rosenbrock_grad
        )
    else:
        result = optimize.minimize(
            rosenbrock,
            [0, 0],
            method=method
        )

    results_dict[method] = {
        'x': result.x,
        'fun': result.fun,
        'nit': result.nit,
        'nfev': result.nfev
    }

print("Method Comparison on Rosenbrock Function")
print("=" * 70)
print(f"{'Method':<15} {'Function Value':<20} {'Iterations':<15} {'F-evals':<10}")
print("-" * 70)
for method, res in results_dict.items():
    print(f"{method:<15} {res['fun']:.2e}           {res['nit']:<15} {res['nfev']:<10}")
```

### Summary Table

| Method | Gradient | Bounds | Memory | Speed | Robustness |
|:-------|:--------:|:------:|:------:|:-----:|:----------:|
| Nelder-Mead | No | No | Low | Slow | High |
| Powell | No | No | Low | Medium | High |
| BFGS | Yes | No | $O(n^2)$ | Fast | High |
| L-BFGS-B | Yes | Yes | $O(mn)$ | Fast | High |
| CG | Yes | No | Low | Fast | Medium |

---

## Choosing a Method

### Decision Tree

```
Do you have gradient information?
├─ NO
│  ├─ Low dimensional (< 10)?
│  │  └─ Use: Nelder-Mead or Powell
│  └─ Higher dimensional?
│     └─ Use: Powell or differential_evolution
│
├─ YES
│  ├─ Need bounds?
│  │  └─ Use: L-BFGS-B
│  │
│  ├─ Very large problem (n > 10,000)?
│  │  └─ Use: CG or L-BFGS-B
│  │
│  └─ Medium problem, want best speed?
│     └─ Use: BFGS or L-BFGS-B
```

### Practical Recommendations

```python
from scipy import optimize
import numpy as np

# Example: Your optimization problem
def objective(x):
    return (x[0] - 2)**2 + (x[1] - 3)**2

# Decision 1: Do you have a gradient function?
has_gradient = False

# Decision 2: Do you need bounds on parameters?
needs_bounds = True
bounds = [(0, 5), (0, 5)]

# Decision 3: Dimension and problem size?
dimension = 2
large_scale = False

# Choice of method
if needs_bounds:
    method = 'L-BFGS-B'
elif large_scale:
    method = 'CG'
elif has_gradient:
    method = 'BFGS'
else:
    method = 'Powell'

result = optimize.minimize(
    objective,
    x0=[0, 0],
    method=method,
    bounds=bounds if needs_bounds else None
)

print(f"Using method: {method}")
print(f"Result: {result.x}")
```

---

## Providing Gradients

Providing analytical gradients can significantly speed up optimization:

```python
from scipy import optimize
import numpy as np
import time

def f(x):
    return np.sum(np.sin(x) * np.exp(-x**2))

def grad_f(x):
    return (np.cos(x) * np.exp(-x**2) -
            2*x * np.sin(x) * np.exp(-x**2))

x0 = np.array([1.0, 2.0, 3.0])

# With gradient
t1 = time.time()
result1 = optimize.minimize(f, x0, method='BFGS', jac=grad_f)
time1 = time.time() - t1

# Without gradient (finite differences)
t2 = time.time()
result2 = optimize.minimize(f, x0, method='BFGS')
time2 = time.time() - t2

print(f"With analytical gradient:")
print(f"  Time: {time1:.4f}s")
print(f"  Function evals: {result1.nfev}")
print(f"\nWith finite differences:")
print(f"  Time: {time2:.4f}s")
print(f"  Function evals: {result2.nfev}")
print(f"\nSpeedup: {time2/time1:.1f}x")
```

---

## Advanced: Hessian Information

Some methods can use second-order derivatives (Hessian matrix):

```python
from scipy import optimize
import numpy as np

def f(x):
    return x[0]**2 + 2*x[1]**2

def grad_f(x):
    return np.array([2*x[0], 4*x[1]])

def hess_f(x):
    """Hessian matrix."""
    return np.array([[2, 0],
                     [0, 4]])

# Newton-CG method uses Hessian
result = optimize.minimize(
    f,
    x0=[1, 1],
    method='Newton-CG',
    jac=grad_f,
    hess=hess_f
)

print(f"Result: {result.x}")
print(f"Iterations: {result.nit}")
```

---

## Summary

**Key Points:**

1. **Gradient-free methods** (Nelder-Mead, Powell) work on any function but are slower
2. **Gradient-based methods** (BFGS, L-BFGS-B) are faster but require smooth functions
3. **L-BFGS-B** is usually the best choice for constrained problems
4. **CG** is memory-efficient for very large problems
5. Providing analytical gradients can significantly improve speed
6. Choose based on: gradient availability, problem scale, constraints, and desired accuracy

The next section addresses the critical issue of local minima and strategies to find global optima.

---

## Runnable Example: `optimization_comparison.py`

```python
"""
Comparing SciPy Optimization Methods - A Comprehensive Tutorial
Exploring scipy.optimize.minimize with multiple algorithms, callback functions,
Jacobians, Hessians, and convergence analysis. See optimization in action!
Run this file to compare different optimization strategies!
"""

import numpy as np
from scipy import optimize
import sys

if __name__ == "__main__":

    print("=" * 70)
    print("COMPARING SCIPY OPTIMIZATION METHODS")
    print("=" * 70)

    # ============================================================================
    # EXAMPLE 1: The Rosenbrock Function - A Classic Optimization Benchmark
    # ============================================================================
    print("\n1. THE ROSENBROCK FUNCTION: A CHALLENGING TEST CASE")
    print("-" * 70)

    def rosenbrock_f(a, b):
        """
        Return the Rosenbrock function, Jacobian, and Hessian.

        The Rosenbrock function is a classic test case for optimization:
        f(x, y) = (a - x)^2 + b*(y - x^2)^2

        It has a minimum value of 0 at (a, a^2).
        The function is easy to evaluate but has a narrow curved valley,
        making it challenging for gradient-free methods.

        Parameters
        ----------
        a, b : float
            Parameters defining the surface. Typical values are a=1, b=100.
            Higher b makes the valley narrower and harder to navigate.
        """
        def f(x, y):
            return (a - x)**2 + b * (y - x**2) ** 2

        def J(x, y):
            # Jacobian (gradient) of the Rosenbrock function
            # df/dx = -2(a - x) - 4*b*x*(y - x^2)
            # df/dy = 2*b*(y - x^2)
            return np.array([
                -2 * (a - x) - 4 * b * x * (y - x**2),
                2 * b * (y - x ** 2)
            ])

        def H(x, y):
            # Hessian (matrix of second derivatives)
            # Used by Newton-CG and trust region methods
            # [d²f/dx²  d²f/dxdy]
            # [d²f/dydx d²f/dy²]
            return np.array([
                [2 + 8*b*x**2 - 4*b*(y - x**2), -4*b*x],
                [-4*b*x, 2*b]
            ])

        return f, J, H

    # Set up Rosenbrock with typical parameters
    a, b = 1.0, 100.0
    rosenbrock, rosenbrock_J, rosenbrock_H = rosenbrock_f(a=a, b=b)

    # Test evaluation
    x0_test, y0_test = -0.5, 2.5
    f_val = rosenbrock(x0_test, y0_test)
    print(f"Rosenbrock function at ({x0_test}, {y0_test}): {f_val:.4f}")
    print(f"True minimum is at ({a}, {a**2}) with value 0.0")
    print(f"Starting point is {f_val:.0f} units away from optimum")

    # Evaluate gradient and Hessian
    grad = rosenbrock_J(x0_test, y0_test)
    hess = rosenbrock_H(x0_test, y0_test)
    print(f"\nGradient at start: {grad}")
    print(f"Hessian at start:\n{hess}")

    # ============================================================================
    # EXAMPLE 2: Nelder-Mead Method - Gradient-Free Optimization
    # ============================================================================
    print("\n2. NELDER-MEAD METHOD: NO GRADIENTS NEEDED")
    print("-" * 70)

    print("Nelder-Mead is a simplex-based method requiring only function values.")
    print("Advantages: robust, no gradients needed, handles non-smooth functions")
    print("Disadvantages: slower convergence, more function evaluations\n")

    x0 = np.array([-0.5, 2.5])
    result_nm = optimize.minimize(
        lambda p: rosenbrock(*p),
        x0=x0,
        method='Nelder-Mead',
        options={'disp': False}
    )

    print("Nelder-Mead Results:")
    print(f"  Optimal point: ({result_nm.x[0]:.6f}, {result_nm.x[1]:.6f})")
    print(f"  Function value: {result_nm.fun:.2e}")
    print(f"  Iterations: {result_nm.nit}")
    print(f"  Function evaluations: {result_nm.nfev}")
    print(f"  Success: {result_nm.success}")

    # ============================================================================
    # EXAMPLE 3: BFGS Method - Quasi-Newton with Gradient
    # ============================================================================
    print("\n3. BFGS METHOD: QUASI-NEWTON WITH GRADIENT")
    print("-" * 70)

    print("BFGS is a quasi-Newton method that approximates the Hessian.")
    print("Advantages: faster than gradient-free, uses only gradients (no Hessian)")
    print("Disadvantages: needs accurate gradients, may fail on non-smooth functions\n")

    result_bfgs = optimize.minimize(
        lambda p: rosenbrock(*p),
        x0=x0,
        jac=lambda p: rosenbrock_J(*p),
        method='BFGS',
        options={'disp': False}
    )

    print("BFGS Results:")
    print(f"  Optimal point: ({result_bfgs.x[0]:.6f}, {result_bfgs.x[1]:.6f})")
    print(f"  Function value: {result_bfgs.fun:.2e}")
    print(f"  Iterations: {result_bfgs.nit}")
    print(f"  Function evaluations: {result_bfgs.nfev}")
    print(f"  Gradient evaluations: {result_bfgs.njev}")

    # ============================================================================
    # EXAMPLE 4: Newton-CG Method - Using Exact Hessian
    # ============================================================================
    print("\n4. NEWTON-CG METHOD: USING EXACT HESSIAN")
    print("-" * 70)

    print("Newton-CG uses exact Hessian information for rapid convergence.")
    print("Advantages: fewest iterations, most accurate near minimum")
    print("Disadvantages: must compute and provide Hessian matrix\n")

    result_ncg = optimize.minimize(
        lambda p: rosenbrock(*p),
        x0=x0,
        jac=lambda p: rosenbrock_J(*p),
        hess=lambda p: rosenbrock_H(*p),
        method='Newton-CG',
        options={'disp': False}
    )

    print("Newton-CG Results:")
    print(f"  Optimal point: ({result_ncg.x[0]:.6f}, {result_ncg.x[1]:.6f})")
    print(f"  Function value: {result_ncg.fun:.2e}")
    print(f"  Iterations: {result_ncg.nit}")
    print(f"  Function evaluations: {result_ncg.nfev}")

    # ============================================================================
    # EXAMPLE 5: L-BFGS-B Method - Bounded Optimization
    # ============================================================================
    print("\n5. L-BFGS-B METHOD: HANDLE BOUNDS ON VARIABLES")
    print("-" * 70)

    print("L-BFGS-B handles box constraints (lower and upper bounds per variable).")
    print("Advantages: efficient for bounded problems, limited memory use")
    print("Disadvantages: requires bounds, doesn't use Hessian\n")

    # Add box constraints: -0.8 <= x <= 0.8, 0 <= y <= 3.0
    bounds = [(-0.8, 0.8), (0, 3.0)]
    result_lbfgs = optimize.minimize(
        lambda p: rosenbrock(*p),
        x0=x0,
        jac=lambda p: rosenbrock_J(*p),
        method='L-BFGS-B',
        bounds=bounds,
        options={'disp': False}
    )

    print("L-BFGS-B Results (with bounds: x in [-0.8, 0.8], y in [0, 3]):")
    print(f"  Optimal point: ({result_lbfgs.x[0]:.6f}, {result_lbfgs.x[1]:.6f})")
    print(f"  Function value: {result_lbfgs.fun:.2e}")
    print(f"  Iterations: {result_lbfgs.nit}")
    print(f"  Note: optimum would be (1, 1) but y=1 is outside x-bound")

    # ============================================================================
    # EXAMPLE 6: Callback Functions - Tracking Optimization Path
    # ============================================================================
    print("\n6. TRACKING OPTIMIZATION PROGRESS WITH CALLBACKS")
    print("-" * 70)

    print("Callback functions execute during optimization to monitor progress.")
    print("Track iteration count, function values, or record the optimization path.\n")

    path = [x0.copy()]  # Record starting point
    iteration_count = [0]  # Use list to modify in nested function

    def callback_function(xk):
        """
        Called after each iteration.
        xk: current parameter values
        """
        iteration_count[0] += 1
        path.append(xk.copy())

    result_with_callback = optimize.minimize(
        lambda p: rosenbrock(*p),
        x0=x0,
        jac=lambda p: rosenbrock_J(*p),
        method='BFGS',
        callback=callback_function,
        options={'disp': False}
    )

    path = np.array(path)
    print("Optimization path (first 5 steps):")
    for i in range(min(5, len(path))):
        f_val = rosenbrock(path[i, 0], path[i, 1])
        print(f"  Step {i}: x={path[i, 0]:7.4f}, y={path[i, 1]:7.4f}, f={f_val:10.4f}")

    print(f"\n  ... (total {len(path)-1} steps)")
    print(f"  Final: x={path[-1, 0]:7.4f}, y={path[-1, 1]:7.4f}, f={result_with_callback.fun:.2e}")

    # ============================================================================
    # EXAMPLE 7: Convergence Comparison - Method Efficiency
    # ============================================================================
    print("\n7. COMPARING CONVERGENCE RATES AND EFFICIENCY")
    print("-" * 70)

    # Compare different methods
    methods_to_compare = [
        ('Nelder-Mead', {'method': 'Nelder-Mead', 'options': {'disp': False}}),
        ('BFGS', {'method': 'BFGS',
                  'jac': lambda p: rosenbrock_J(*p), 'options': {'disp': False}}),
        ('Newton-CG', {'method': 'Newton-CG',
                       'jac': lambda p: rosenbrock_J(*p),
                       'hess': lambda p: rosenbrock_H(*p),
                       'options': {'disp': False}}),
        ('L-BFGS-B', {'method': 'L-BFGS-B',
                      'jac': lambda p: rosenbrock_J(*p),
                      'options': {'disp': False}}),
        ('CG', {'method': 'CG',
                'jac': lambda p: rosenbrock_J(*p),
                'options': {'disp': False}}),
    ]

    print("\nMethod Comparison (starting from [-0.5, 2.5]):")
    print("-" * 70)
    print(f"{'Method':<15} {'Iterations':<12} {'Func Evals':<12} {'Final Value':<15} {'Success':<10}")
    print("-" * 70)

    results_comparison = {}
    for method_name, options in methods_to_compare:
        result = optimize.minimize(lambda p: rosenbrock(*p), x0=x0, **options)
        results_comparison[method_name] = result
        print(f"{method_name:<15} {result.nit:<12} {result.nfev:<12} {result.fun:<15.2e} {str(result.success):<10}")

    print("\nInterpretation:")
    print("  Iterations: fewer iterations = faster algorithm")
    print("  Func Evals: evaluations of objective function")
    print("  Final Value: lower is better (should be ~0)")
    print("  Success: did optimization converge?")

    # ============================================================================
    # EXAMPLE 8: Effect of Starting Point on Convergence
    # ============================================================================
    print("\n8. STARTING POINT SENSITIVITY")
    print("-" * 70)

    print("Optimization can be sensitive to initial conditions.\n")

    starting_points = [
        (-0.5, 2.5),
        (0.0, 0.0),
        (2.0, 2.0),
        (-1.0, 3.0),
    ]

    print(f"{'Starting Point':<20} {'BFGS Iters':<15} {'Newton-CG Iters':<15}")
    print("-" * 50)

    for x0_point in starting_points:
        x0_array = np.array(x0_point)

        result_bfgs_var = optimize.minimize(
            lambda p: rosenbrock(*p),
            x0=x0_array,
            jac=lambda p: rosenbrock_J(*p),
            method='BFGS',
            options={'disp': False}
        )

        result_ncg_var = optimize.minimize(
            lambda p: rosenbrock(*p),
            x0=x0_array,
            jac=lambda p: rosenbrock_J(*p),
            hess=lambda p: rosenbrock_H(*p),
            method='Newton-CG',
            options={'disp': False}
        )

        print(f"{str(x0_point):<20} {result_bfgs_var.nit:<15} {result_ncg_var.nit:<15}")

    # ============================================================================
    # EXAMPLE 9: Visualization of Convergence Patterns
    # ============================================================================
    print("\n9. DETAILED CONVERGENCE ANALYSIS")
    print("-" * 70)

    print("Track function values throughout optimization process:\n")

    # Track function values with BFGS
    function_values = [rosenbrock(*x0)]
    iteration_num = [0]

    def callback_tracking(xk):
        function_values.append(rosenbrock(*xk))
        iteration_num.append(iteration_num[-1] + 1)

    result_track = optimize.minimize(
        lambda p: rosenbrock(*p),
        x0=x0,
        jac=lambda p: rosenbrock_J(*p),
        method='BFGS',
        callback=callback_tracking,
        options={'disp': False}
    )

    print("Function value reduction in BFGS method:")
    print(f"{'Iteration':<12} {'Function Value':<20} {'Reduction':<20}")
    print("-" * 52)
    for i in range(min(10, len(function_values))):
        fval = function_values[i]
        if i == 0:
            reduction = "-"
        else:
            reduction = f"{function_values[i-1] - fval:.4e}"
        print(f"{i:<12} {fval:<20.6e} {str(reduction):<20}")

    if len(function_values) > 10:
        print(f"... ({len(function_values)-10} more steps)")
        print(f"{len(function_values)-1:<12} {function_values[-1]:<20.6e}")

    # ============================================================================
    # EXAMPLE 10: Gradient Accuracy and Optimization Quality
    # ============================================================================
    print("\n10. IMPORTANCE OF ACCURATE GRADIENTS")
    print("-" * 70)

    # Compare with numerical gradient approximation
    def numerical_gradient(func, x, eps=1e-8):
        """Approximate gradient using finite differences"""
        grad = np.zeros_like(x)
        for i in range(len(x)):
            x_plus = x.copy()
            x_minus = x.copy()
            x_plus[i] += eps
            x_minus[i] -= eps
            grad[i] = (func(x_plus) - func(x_minus)) / (2 * eps)
        return grad

    print("Comparing analytical vs numerical gradients:\n")
    x_test = np.array([0.5, 0.5])
    analytical_grad = rosenbrock_J(*x_test)
    numerical_grad = numerical_gradient(lambda p: rosenbrock(*p), x_test)

    print(f"Analytical gradient: {analytical_grad}")
    print(f"Numerical gradient:  {numerical_grad}")
    print(f"Difference: {np.linalg.norm(analytical_grad - numerical_grad):.2e}")

    # Optimize with analytical gradient
    result_analytical = optimize.minimize(
        lambda p: rosenbrock(*p),
        x0=x0,
        jac=lambda p: rosenbrock_J(*p),
        method='BFGS',
        options={'disp': False}
    )

    print(f"\nWith analytical gradient: {result_analytical.nit} iterations")
    print(f"Final value: {result_analytical.fun:.2e}")

    print("\n" + "=" * 70)
    print("Key takeaways:")
    print("- Nelder-Mead: robust, no gradients, but slower")
    print("- BFGS: good balance, needs gradient, no Hessian")
    print("- Newton-CG: fastest, needs exact Hessian")
    print("- L-BFGS-B: for bounded optimization problems")
    print("- Callbacks: track optimization progress in real-time")
    print("- Accurate gradients/Hessians = faster convergence")
    print("- Starting point can affect convergence speed")
    print("=" * 70)
```

---

## Exercises

**Exercise 1.**
Define a 3D objective function $f(x, y, z) = (x-1)^2 + 2(y-2)^2 + 3(z-3)^2$. Write its analytical gradient. Minimize using BFGS with and without the analytical gradient. Compare the number of function evaluations in each case.

??? success "Solution to Exercise 1"
        ```python
        import numpy as np
        from scipy import optimize

        def f(x):
            return (x[0]-1)**2 + 2*(x[1]-2)**2 + 3*(x[2]-3)**2

        def grad_f(x):
            return np.array([2*(x[0]-1), 4*(x[1]-2), 6*(x[2]-3)])

        x0 = np.array([0.0, 0.0, 0.0])

        # Without gradient
        res_no_grad = optimize.minimize(f, x0, method='BFGS')
        print(f"Without gradient: nfev={res_no_grad.nfev}, x={res_no_grad.x}")

        # With gradient
        res_with_grad = optimize.minimize(f, x0, method='BFGS', jac=grad_f)
        print(f"With gradient: nfev={res_with_grad.nfev}, x={res_with_grad.x}")
        print(f"Function eval savings: {res_no_grad.nfev - res_with_grad.nfev}")
        ```

---

**Exercise 2.**
Implement a timing benchmark that minimizes the Rosenbrock function from the starting point $(-1, -1)$ using Nelder-Mead, Powell, BFGS, and L-BFGS-B. Use `time.perf_counter()` to measure wall-clock time for each. Print a table of method, final value, iterations, and elapsed time.

??? success "Solution to Exercise 2"
        ```python
        import numpy as np
        from scipy import optimize
        import time

        def rosenbrock(x):
            return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2

        x0 = np.array([-1.0, -1.0])
        methods = ['Nelder-Mead', 'Powell', 'BFGS', 'L-BFGS-B']

        print(f"{'Method':<15} {'Value':<15} {'Iters':<10} {'Time (ms)':<12}")
        print("-" * 52)

        for method in methods:
            start = time.perf_counter()
            result = optimize.minimize(rosenbrock, x0, method=method)
            elapsed = (time.perf_counter() - start) * 1000

            print(f"{method:<15} {result.fun:<15.2e} {result.nit:<10} {elapsed:<12.2f}")
        ```

---

**Exercise 3.**
Use L-BFGS-B to minimize $f(\mathbf{x}) = \sum_{i=1}^{n} (x_i - i)^2$ for $n = 500$ with the constraint that all $x_i \geq 0$. Provide the analytical gradient. Print the optimal value and the number of iterations. Verify that all solution components are non-negative.

??? success "Solution to Exercise 3"
        ```python
        import numpy as np
        from scipy import optimize

        n = 500

        def f(x):
            return np.sum((x - np.arange(1, n+1))**2)

        def grad_f(x):
            return 2 * (x - np.arange(1, n+1))

        x0 = np.zeros(n)
        bounds = [(0, None)] * n

        result = optimize.minimize(f, x0, method='L-BFGS-B', jac=grad_f, bounds=bounds)

        print(f"Optimal value: {result.fun:.2e}")
        print(f"Iterations: {result.nit}")
        print(f"All x >= 0: {np.all(result.x >= -1e-10)}")
        print(f"x[:5] = {result.x[:5]}")
        ```
