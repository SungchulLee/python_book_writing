# Constrained Optimization

Real-world problems often come with constraints. You might need to minimize cost while keeping all parameters within valid ranges, or ensure that parameters satisfy certain physical laws or business requirements. Constrained optimization handles these scenarios.

!!! tip "Mental Model"
    Think of unconstrained optimization as rolling a ball downhill on open terrain, while constrained optimization is rolling that ball inside a fenced area. The fence (constraints) may prevent you from reaching the absolute lowest point, so the optimizer finds the best spot you can actually stand on. The tighter the fence, the more the solution is shaped by the constraints rather than the objective.

---

## Types of Constraints

### Bound Constraints

The simplest constraint type: each parameter must fall within a specified range.

$$\mathbf{x}^{\text{lower}} \leq \mathbf{x} \leq \mathbf{x}^{\text{upper}}$$

```python
from scipy import optimize
import numpy as np

# Cost function
def objective(x):
    return (x[0] - 3)**2 + (x[1] - 2)**2

# Unconstrained: minimum at (3, 2)
result_unconstrained = optimize.minimize(objective, x0=[0, 0])
print(f"Unconstrained: {result_unconstrained.x}")

# With bounds: each parameter constrained to [0, 2.5]
bounds = [(0, 2.5), (0, 2.5)]
result_bounded = optimize.minimize(objective, x0=[0, 0], bounds=bounds,
                                  method='L-BFGS-B')
print(f"Bounded: {result_bounded.x}")

# The solution is constrained to the feasible region
print(f"Unconstrained value: {objective(result_unconstrained.x):.4f}")
print(f"Bounded value: {objective(result_bounded.x):.4f}")
```

**Key Methods Supporting Bounds:**
- `L-BFGS-B`: Limited memory BFGS with bounds (recommended)
- `TNC`: Truncated Newton method
- `SLSQP`: Sequential least squares programming
- `differential_evolution`: Population-based (global)
- `dual_annealing`: Simulated annealing variant

### Inequality Constraints

Constraints of the form $g(\mathbf{x}) \geq 0$. When the constraint function is non-negative, the constraint is satisfied.

```python
from scipy import optimize
import numpy as np

def objective(x):
    """Minimize x[0]^2 + x[1]^2."""
    return x[0]**2 + x[1]**2

# Constraint: x[0] + x[1] >= 2 (equivalently, 2 - x[0] - x[1] <= 0)
# Express as: x[0] + x[1] - 2 >= 0
constraints = {'type': 'ineq', 'fun': lambda x: x[0] + x[1] - 2}

result = optimize.minimize(
    objective,
    x0=[1, 1],
    constraints=constraints,
    method='SLSQP'
)

print(f"Optimal x: {result.x}")
print(f"Objective value: {result.fun:.6f}")
print(f"Constraint value (should be >= 0): {x[0] + x[1] - 2:.6f}")

# Verify the solution lies on the constraint boundary
x_opt = result.x
print(f"x[0] + x[1] = {x_opt[0] + x_opt[1]:.6f} (should be ~2)")
```

### Equality Constraints

Constraints of the form $h(\mathbf{x}) = 0$. The constraint must be exactly satisfied.

```python
from scipy import optimize
import numpy as np

def objective(x):
    """Minimize (x[0] - 3)^2 + (x[1] - 2)^2."""
    return (x[0] - 3)**2 + (x[1] - 2)**2

# Constraint: x[0]^2 + x[1]^2 = 10 (point lies on circle of radius sqrt(10))
constraints = {'type': 'eq', 'fun': lambda x: x[0]**2 + x[1]**2 - 10}

result = optimize.minimize(
    objective,
    x0=[2, 2],
    constraints=constraints,
    method='SLSQP'
)

print(f"Optimal x: {result.x}")
print(f"Objective value: {result.fun:.6f}")

# Verify constraint
x_opt = result.x
constraint_value = x_opt[0]**2 + x_opt[1]**2
print(f"Constraint x[0]^2 + x[1]^2 = {constraint_value:.6f} (should be ~10)")
```

---

## Constraint Objects: LinearConstraint and NonlinearConstraint

For more complex constraint specifications, scipy provides constraint objects that offer better organization and allow multiple constraints:

### LinearConstraint

Linear constraints of the form $\mathbf{lb} \leq A\mathbf{x} \leq \mathbf{ub}$.

```python
from scipy import optimize
import numpy as np

def objective(x):
    """Minimize x[0]^2 + x[1]^2."""
    return x[0]**2 + x[1]**2

# Linear constraint: 2*x[0] + x[1] <= 4
# Form: A @ x <= b, so A @ x - b <= 0
# Using LinearConstraint: -inf <= A @ x <= 4

A = np.array([[2, 1]])  # Constraint coefficients
lb = -np.inf
ub = 4

constraint = optimize.LinearConstraint(A, lb, ub)

result = optimize.minimize(
    objective,
    x0=[0, 0],
    constraints=constraint,
    method='SLSQP'
)

print(f"Optimal x: {result.x}")
print(f"Constraint A @ x = {A @ result.x:.6f} (should be <= 4)")
```

### NonlinearConstraint

Nonlinear constraints of the form $\mathbf{lb} \leq g(\mathbf{x}) \leq \mathbf{ub}$.

```python
from scipy import optimize
import numpy as np

def objective(x):
    """Minimize x[0]^2 + x[1]^2."""
    return x[0]**2 + x[1]**2

def constraint_func(x):
    """Nonlinear constraint: x[0]^2 + 2*x[1]^2."""
    return np.array([x[0]**2 + 2*x[1]**2])

# Constraint: 0.5 <= x[0]^2 + 2*x[1]^2 <= 4
constraint = optimize.NonlinearConstraint(constraint_func, 0.5, 4)

result = optimize.minimize(
    objective,
    x0=[1, 1],
    constraints=constraint,
    method='SLSQP'
)

print(f"Optimal x: {result.x}")
print(f"Constraint value: {constraint_func(result.x)[0]:.6f}")
print(f"(should be in [0.5, 4])")
```

---

## Practical Example: Portfolio Optimization

A classic constrained optimization problem: allocate capital among assets to minimize risk while achieving target return.

```python
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt

# Expected returns and covariance matrix for 4 assets
expected_returns = np.array([0.05, 0.08, 0.12, 0.10])
cov_matrix = np.array([
    [0.01,   0.002,  0.005,  0.003],
    [0.002,  0.015,  0.008,  0.006],
    [0.005,  0.008,  0.040,  0.010],
    [0.003,  0.006,  0.010,  0.025]
])

def portfolio_variance(weights):
    """Calculate portfolio variance (risk)."""
    return weights @ cov_matrix @ weights

def portfolio_return(weights):
    """Calculate portfolio return."""
    return weights @ expected_returns

# Constraints
def return_constraint(weights):
    """Constraint: return >= 0.08."""
    return portfolio_return(weights) - 0.08

constraints = [
    {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},  # Sum to 1
    {'type': 'ineq', 'fun': return_constraint}        # Return >= 0.08
]

# Bounds: each weight in [0, 1]
bounds = [(0, 1)] * 4

# Initial guess: equal weight
w0 = np.array([0.25, 0.25, 0.25, 0.25])

# Optimize
result = optimize.minimize(
    portfolio_variance,
    w0,
    constraints=constraints,
    bounds=bounds,
    method='SLSQP'
)

print("Optimal Portfolio:")
print(f"Weights: {result.x}")
print(f"Return: {portfolio_return(result.x):.4f}")
print(f"Risk (std): {np.sqrt(portfolio_variance(result.x)):.4f}")

# Explore efficient frontier
target_returns = np.linspace(0.05, 0.12, 20)
variances = []

for target_return in target_returns:
    constraints = [
        {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
        {'type': 'eq', 'fun': lambda w: portfolio_return(w) - target_return}
    ]

    result = optimize.minimize(
        portfolio_variance,
        w0,
        constraints=constraints,
        bounds=bounds,
        method='SLSQP'
    )

    if result.success:
        variances.append(portfolio_variance(result.x))

# Plot efficient frontier
fig, ax = plt.subplots(figsize=(10, 6))
risks = np.sqrt(variances)
ax.plot(risks, target_returns[:len(risks)], 'b-', linewidth=2)
ax.scatter(risks, target_returns[:len(risks)], c=target_returns[:len(risks)],
          cmap='viridis')
ax.set_xlabel('Risk (Standard Deviation)')
ax.set_ylabel('Return')
ax.set_title('Efficient Frontier')
ax.grid(True, alpha=0.3)
plt.colorbar(ax.collections[0], ax=ax, label='Target Return')
plt.tight_layout()
plt.show()
```

---

## Handling Multiple Constraints

When you have many constraints, using a list or proper constraint objects is clearer:

```python
from scipy import optimize
import numpy as np

def objective(x):
    return (x[0] - 3)**2 + (x[1] - 1)**2 + (x[2] - 2)**2

# Multiple constraints
constraints = [
    # Equality constraint: x[0] + x[1] = 2
    {'type': 'eq', 'fun': lambda x: x[0] + x[1] - 2},

    # Inequality constraint: x[2] >= 1
    {'type': 'ineq', 'fun': lambda x: x[2] - 1},

    # Inequality constraint: x[0] + x[1] + x[2] <= 5
    {'type': 'ineq', 'fun': lambda x: 5 - (x[0] + x[1] + x[2])}
]

bounds = [(None, None)] * 3  # No direct bounds

result = optimize.minimize(
    objective,
    x0=[0, 0, 0],
    constraints=constraints,
    bounds=bounds,
    method='SLSQP'
)

print(f"Optimal x: {result.x}")
print(f"Objective: {objective(result.x):.6f}")

# Verify constraints
x = result.x
print(f"x[0] + x[1] = {x[0] + x[1]:.6f} (should be 2)")
print(f"x[2] = {x[2]:.6f} (should be >= 1)")
print(f"x[0] + x[1] + x[2] = {np.sum(x):.6f} (should be <= 5)")
```

---

## Understanding Infeasible Constraints

Sometimes constraints cannot all be satisfied simultaneously. The optimizer will do its best:

```python
from scipy import optimize
import numpy as np

def objective(x):
    return x[0]**2 + x[1]**2

# Infeasible constraints: x[0] + x[1] >= 2 AND x[0] + x[1] <= 1
constraints = [
    {'type': 'ineq', 'fun': lambda x: x[0] + x[1] - 2},   # >= 2
    {'type': 'ineq', 'fun': lambda x: 1 - (x[0] + x[1])}  # <= 1
]

result = optimize.minimize(
    objective,
    x0=[0, 0],
    constraints=constraints,
    method='SLSQP'
)

print(f"Success: {result.success}")
print(f"Optimal x: {result.x}")
print(f"x[0] + x[1] = {result.x[0] + result.x[1]:.6f}")
print(f"Message: {result.message}")
```

---

## Constraint Jacobians

For better performance, you can provide gradients of the constraint functions:

```python
from scipy import optimize
import numpy as np

def objective(x):
    return (x[0] - 2)**2 + (x[1] - 3)**2

def constraint_func(x):
    """x[0]^2 + x[1]^2 = 10."""
    return x[0]**2 + x[1]**2 - 10

def constraint_jac(x):
    """Gradient of constraint."""
    return np.array([2*x[0], 2*x[1]])

# Define constraint with Jacobian
constraints = {
    'type': 'eq',
    'fun': constraint_func,
    'jac': constraint_jac
}

result = optimize.minimize(
    objective,
    x0=[2, 2],
    constraints=constraints,
    method='SLSQP'
)

print(f"Optimal x: {result.x}")
print(f"Objective: {objective(result.x):.6f}")
```

---

## Choosing Methods for Constrained Optimization

| Method | Bounds | Equality | Inequality | Notes |
|:-------|:------:|:--------:|:----------:|:------|
| L-BFGS-B | Yes | No | No | Fast, good for bounds only |
| SLSQP | Yes | Yes | Yes | General-purpose, reliable |
| TNC | Yes | No | No | Good for large problems |
| COBYLA | No | Yes | Yes | Robust, no derivatives |
| trust-constr | Yes | Yes | Yes | Modern, good for large-scale |

```python
from scipy import optimize
import numpy as np

def objective(x):
    return (x[0] - 3)**2 + (x[1] - 2)**2

def constraint(x):
    return x[0] + x[1] - 2  # x[0] + x[1] >= 2

# Choose method based on your constraints
constraints = {'type': 'ineq', 'fun': constraint}
bounds = [(0, 10), (0, 10)]

# SLSQP is most general
result = optimize.minimize(
    objective,
    x0=[0, 0],
    constraints=constraints,
    bounds=bounds,
    method='SLSQP'
)

print(f"Result: {result.x}")
```

---

## Summary

**Key Points:**

1. **Bounds** are easiest to implement and handled efficiently by L-BFGS-B
2. **Inequality constraints** ($g(\mathbf{x}) \geq 0$) expand what's possible
3. **Equality constraints** ($h(\mathbf{x}) = 0$) further restrict the solution space
4. **SLSQP** is the most general-purpose constrained method
5. **LinearConstraint/NonlinearConstraint** provide cleaner syntax for complex problems
6. Always **verify constraints are satisfied** in the final solution
7. **Check feasibility** before optimizing (infeasible constraints = no solution)

Next sections cover specialized optimization for fitting curves to data and finding roots of functions.

---

## Exercises

**Exercise 1.**
Minimize $f(x, y) = x^2 + y^2$ subject to the equality constraint $x + y = 4$ using SLSQP. Print the optimal point and verify that the constraint is satisfied. Also solve analytically (using Lagrange multipliers, the answer is $(2, 2)$) and compare.

??? success "Solution to Exercise 1"
        ```python
        import numpy as np
        from scipy import optimize

        def objective(x):
            return x[0]**2 + x[1]**2

        constraints = {'type': 'eq', 'fun': lambda x: x[0] + x[1] - 4}

        result = optimize.minimize(objective, x0=[0, 0],
                                   constraints=constraints, method='SLSQP')

        print(f"Optimal point: ({result.x[0]:.4f}, {result.x[1]:.4f})")
        print(f"Objective value: {result.fun:.4f}")
        print(f"Constraint x+y = {result.x[0] + result.x[1]:.4f} (should be 4)")
        print(f"Close to (2, 2): {np.allclose(result.x, [2, 2], atol=1e-4)}")
        ```

---

**Exercise 2.**
Solve a simple resource allocation problem: minimize $f(x_1, x_2, x_3) = x_1^2 + 2x_2^2 + 3x_3^2$ subject to $x_1 + x_2 + x_3 = 10$ (equality) and $x_i \geq 0$ for all $i$ (bounds). Use SLSQP and print the optimal allocation and objective value.

??? success "Solution to Exercise 2"
        ```python
        import numpy as np
        from scipy import optimize

        def objective(x):
            return x[0]**2 + 2*x[1]**2 + 3*x[2]**2

        constraints = {'type': 'eq', 'fun': lambda x: x[0] + x[1] + x[2] - 10}
        bounds = [(0, None), (0, None), (0, None)]

        result = optimize.minimize(objective, x0=[3, 3, 4],
                                   constraints=constraints,
                                   bounds=bounds, method='SLSQP')

        print(f"Allocation: x1={result.x[0]:.4f}, x2={result.x[1]:.4f}, x3={result.x[2]:.4f}")
        print(f"Objective: {result.fun:.4f}")
        print(f"Sum: {np.sum(result.x):.4f} (should be 10)")
        ```

---

**Exercise 3.**
Use `NonlinearConstraint` to minimize $f(x, y) = (x - 3)^2 + (y - 3)^2$ subject to $1 \leq x^2 + y^2 \leq 10$. Start from `x0 = [1, 1]`. Print the optimal point and verify the constraint is within bounds.

??? success "Solution to Exercise 3"
        ```python
        import numpy as np
        from scipy import optimize

        def objective(x):
            return (x[0] - 3)**2 + (x[1] - 3)**2

        def constraint_func(x):
            return x[0]**2 + x[1]**2

        constraint = optimize.NonlinearConstraint(constraint_func, 1, 10)

        result = optimize.minimize(objective, x0=[1, 1],
                                   constraints=constraint, method='SLSQP')

        c_val = constraint_func(result.x)
        print(f"Optimal point: ({result.x[0]:.4f}, {result.x[1]:.4f})")
        print(f"Objective: {result.fun:.4f}")
        print(f"Constraint value: {c_val:.4f} (should be in [1, 10])")
        print(f"Constraint satisfied: {1 <= c_val <= 10}")
        ```
