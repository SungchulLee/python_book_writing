# Numerical Stability

Numerical stability determines whether an algorithm produces reliable results despite unavoidable floating-point errors. A stable algorithm keeps errors bounded; an unstable one amplifies them catastrophically.

!!! tip "Mental Model"
    Conditioning is a property of the problem (how sensitive the answer is to input noise); stability is a property of the algorithm (whether it makes that sensitivity worse). A good algorithm on an ill-conditioned problem still loses digits, but a bad algorithm can turn even a well-conditioned problem into garbage.

## Stability vs Conditioning

Distinguish between problem sensitivity and algorithm reliability.

### 1. Problem Conditioning

A problem's condition number measures inherent sensitivity to input perturbations.

$$\text{Relative output change} \approx \kappa \times \text{Relative input change}$$

```python
import numpy as np

# Well-conditioned matrix (identity-like)
A_good = np.eye(5) + 0.1 * np.random.randn(5, 5)
print(f"Well-conditioned: κ = {np.linalg.cond(A_good):.2f}")

# Ill-conditioned matrix (Hilbert)
def hilbert(n):
    return np.array([[1/(i+j+1) for j in range(n)] for i in range(n)])

A_bad = hilbert(5)
print(f"Ill-conditioned:  κ = {np.linalg.cond(A_bad):.2e}")

# Implication: solving Ax = b loses log10(κ) digits
print(f"\nExpected digit loss:")
print(f"  Good matrix: ~{np.log10(np.linalg.cond(A_good)):.1f} digits")
print(f"  Bad matrix:  ~{np.log10(np.linalg.cond(A_bad)):.1f} digits")
```

### 2. Algorithm Stability

An algorithm is stable if it doesn't amplify errors beyond what the problem's conditioning requires.

```python
import numpy as np

def solve_stable(A, b):
    """Stable: LU decomposition with partial pivoting."""
    return np.linalg.solve(A, b)

def solve_unstable(A, b):
    """Unstable: explicit matrix inversion."""
    return np.linalg.inv(A) @ b

# Test on moderately ill-conditioned system
np.random.seed(42)
n = 50
A = np.random.randn(n, n)
A = A @ A.T + 0.1 * np.eye(n)  # Symmetric positive definite
x_true = np.random.randn(n)
b = A @ x_true

x_stable = solve_stable(A, b)
x_unstable = solve_unstable(A, b)

print(f"Condition number: {np.linalg.cond(A):.2e}")
print(f"Stable error:     {np.linalg.norm(x_stable - x_true):.2e}")
print(f"Unstable error:   {np.linalg.norm(x_unstable - x_true):.2e}")
```

### 3. Backward Stability

A backward stable algorithm computes the exact solution to a nearby problem.

$$\tilde{x} = \text{exact solution of } (A + \Delta A)\tilde{x} = b + \Delta b$$

where $\|\Delta A\| / \|A\|$ and $\|\Delta b\| / \|b\|$ are $O(\epsilon)$.

```python
import numpy as np

def check_backward_stability(A, b, x_computed):
    """
    Check backward error: find residual relative to problem size.
    Small backward error indicates backward stability.
    """
    residual = A @ x_computed - b
    backward_error = np.linalg.norm(residual) / (np.linalg.norm(A) * np.linalg.norm(x_computed) + np.linalg.norm(b))
    return backward_error

# Test
np.random.seed(123)
A = np.random.randn(20, 20)
x_true = np.random.randn(20)
b = A @ x_true

x_solve = np.linalg.solve(A, b)
x_inv = np.linalg.inv(A) @ b

print(f"Machine epsilon: {np.finfo(float).eps:.2e}")
print(f"Backward error (solve): {check_backward_stability(A, b, x_solve):.2e}")
print(f"Backward error (inv):   {check_backward_stability(A, b, x_inv):.2e}")
```

## Stable Algorithms

Examples of numerically stable methods.

### 1. Gaussian Elimination with Pivoting

Partial pivoting prevents division by small numbers.

```python
import numpy as np

def lu_no_pivot(A):
    """LU decomposition without pivoting (unstable)."""
    n = A.shape[0]
    L = np.eye(n)
    U = A.astype(float).copy()
    
    for k in range(n-1):
        for i in range(k+1, n):
            if abs(U[k, k]) < 1e-15:
                raise ValueError("Zero pivot encountered")
            L[i, k] = U[i, k] / U[k, k]
            U[i, k:] -= L[i, k] * U[k, k:]
    
    return L, U

def lu_partial_pivot(A):
    """LU decomposition with partial pivoting (stable)."""
    n = A.shape[0]
    P = np.eye(n)
    L = np.zeros((n, n))
    U = A.astype(float).copy()
    
    for k in range(n-1):
        # Find pivot
        max_idx = k + np.argmax(np.abs(U[k:, k]))
        
        # Swap rows
        U[[k, max_idx]] = U[[max_idx, k]]
        P[[k, max_idx]] = P[[max_idx, k]]
        L[[k, max_idx], :k] = L[[max_idx, k], :k]
        
        # Eliminate
        for i in range(k+1, n):
            L[i, k] = U[i, k] / U[k, k]
            U[i, k:] -= L[i, k] * U[k, k:]
    
    np.fill_diagonal(L, 1)
    return P, L, U

# Test on matrix that needs pivoting
A = np.array([[1e-20, 1.0],
              [1.0, 1.0]])
b = np.array([1.0, 2.0])

# Without pivoting: unstable
try:
    L, U = lu_no_pivot(A)
    x_no_pivot = np.linalg.solve(U, np.linalg.solve(L, b))
    print(f"No pivot solution: {x_no_pivot}")
except Exception as e:
    print(f"No pivot failed: {e}")

# With pivoting: stable
P, L, U = lu_partial_pivot(A)
x_pivot = np.linalg.solve(U, np.linalg.solve(L, P @ b))
print(f"Pivot solution:    {x_pivot}")
print(f"True solution:     {np.linalg.solve(A, b)}")
```

### 2. QR Decomposition

More stable than LU for least squares problems.

```python
import numpy as np

# Least squares: minimize ||Ax - b||²
np.random.seed(42)
m, n = 100, 10
A = np.random.randn(m, n)
b = np.random.randn(m)

# Method 1: Normal equations (less stable)
# Solve A^T A x = A^T b
ATA = A.T @ A
ATb = A.T @ b
x_normal = np.linalg.solve(ATA, ATb)

# Method 2: QR decomposition (more stable)
Q, R = np.linalg.qr(A)
x_qr = np.linalg.solve(R, Q.T @ b)

# Method 3: SVD (most stable)
x_svd = np.linalg.lstsq(A, b, rcond=None)[0]

# Compare residuals
print("Residual norms:")
print(f"  Normal equations: {np.linalg.norm(A @ x_normal - b):.10e}")
print(f"  QR decomposition: {np.linalg.norm(A @ x_qr - b):.10e}")
print(f"  SVD:              {np.linalg.norm(A @ x_svd - b):.10e}")

# Condition numbers
print(f"\nCondition number of A:   {np.linalg.cond(A):.2e}")
print(f"Condition number of A^TA: {np.linalg.cond(ATA):.2e}")  # Squared!
```

### 3. Householder Reflections

Orthogonal transformations preserve norms.

```python
import numpy as np

def householder_qr(A):
    """QR decomposition using Householder reflections."""
    m, n = A.shape
    Q = np.eye(m)
    R = A.astype(float).copy()
    
    for k in range(min(m-1, n)):
        # Construct Householder vector
        x = R[k:, k]
        v = x.copy()
        v[0] += np.sign(x[0]) * np.linalg.norm(x)
        v = v / np.linalg.norm(v)
        
        # Apply reflection
        R[k:, k:] -= 2 * np.outer(v, v @ R[k:, k:])
        
        # Accumulate Q
        Q_k = np.eye(m)
        Q_k[k:, k:] -= 2 * np.outer(v, v)
        Q = Q @ Q_k
    
    return Q, R

# Test orthogonality preservation
A = np.random.randn(10, 5)
Q, R = householder_qr(A)

print(f"Q orthogonality error: {np.linalg.norm(Q.T @ Q - np.eye(10)):.2e}")
print(f"Reconstruction error:  {np.linalg.norm(Q @ R - A):.2e}")
```

## Unstable Algorithms

Examples to avoid and their stable alternatives.

### 1. Gram-Schmidt Orthogonalization

Classical Gram-Schmidt loses orthogonality.

```python
import numpy as np

def gram_schmidt_classical(A):
    """Classical Gram-Schmidt (unstable)."""
    m, n = A.shape
    Q = np.zeros((m, n))
    R = np.zeros((n, n))
    
    for j in range(n):
        v = A[:, j].copy()
        for i in range(j):
            R[i, j] = Q[:, i] @ A[:, j]
            v -= R[i, j] * Q[:, i]
        R[j, j] = np.linalg.norm(v)
        Q[:, j] = v / R[j, j]
    
    return Q, R

def gram_schmidt_modified(A):
    """Modified Gram-Schmidt (more stable)."""
    m, n = A.shape
    Q = A.astype(float).copy()
    R = np.zeros((n, n))
    
    for j in range(n):
        R[j, j] = np.linalg.norm(Q[:, j])
        Q[:, j] /= R[j, j]
        for k in range(j+1, n):
            R[j, k] = Q[:, j] @ Q[:, k]
            Q[:, k] -= R[j, k] * Q[:, j]
    
    return Q, R

# Test on ill-conditioned matrix
np.random.seed(42)
A = np.random.randn(100, 10)
# Make columns nearly parallel
A[:, 1] = A[:, 0] + 1e-8 * np.random.randn(100)

Q_classical, _ = gram_schmidt_classical(A)
Q_modified, _ = gram_schmidt_modified(A)
Q_householder, _ = np.linalg.qr(A)

print("Orthogonality error (||Q^T Q - I||):")
print(f"  Classical GS:  {np.linalg.norm(Q_classical.T @ Q_classical - np.eye(10)):.2e}")
print(f"  Modified GS:   {np.linalg.norm(Q_modified.T @ Q_modified - np.eye(10)):.2e}")
print(f"  Householder:   {np.linalg.norm(Q_householder.T @ Q_householder - np.eye(10)):.2e}")
```

### 2. Polynomial Evaluation

Horner's method vs naive evaluation.

```python
import numpy as np

def poly_naive(coeffs, x):
    """Naive polynomial evaluation (unstable for high degree)."""
    return sum(c * x**i for i, c in enumerate(coeffs))

def poly_horner(coeffs, x):
    """Horner's method (stable)."""
    result = coeffs[-1]
    for c in reversed(coeffs[:-1]):
        result = result * x + c
    return result

# Test with Wilkinson polynomial (notoriously ill-conditioned)
# p(x) = (x-1)(x-2)...(x-20)
from numpy.polynomial import polynomial as P

roots = np.arange(1, 21)
coeffs = np.array([1.0])
for r in roots:
    coeffs = np.convolve(coeffs, [1, -r])

# Evaluate near a root
x = 15.0 + 1e-8

naive_result = poly_naive(coeffs[::-1], x)
horner_result = poly_horner(coeffs[::-1], x)
numpy_result = np.polyval(coeffs, x)

print(f"Naive:  {naive_result:.6e}")
print(f"Horner: {horner_result:.6e}")
print(f"NumPy:  {numpy_result:.6e}")
```

### 3. Recurrence Relations

Some recurrences amplify errors exponentially.

```python
import numpy as np

def fibonacci_recurrence(n):
    """Forward recurrence (unstable for large n with floats)."""
    if n <= 1:
        return float(n)
    a, b = 0.0, 1.0
    for _ in range(n - 1):
        a, b = b, a + b
    return b

def fibonacci_binet(n):
    """Binet formula (direct but loses precision)."""
    phi = (1 + np.sqrt(5)) / 2
    psi = (1 - np.sqrt(5)) / 2
    return (phi**n - psi**n) / np.sqrt(5)

def fibonacci_matrix(n):
    """Matrix exponentiation (more stable)."""
    if n <= 1:
        return float(n)
    
    def matrix_mult(A, B):
        return np.array([[A[0,0]*B[0,0] + A[0,1]*B[1,0], A[0,0]*B[0,1] + A[0,1]*B[1,1]],
                        [A[1,0]*B[0,0] + A[1,1]*B[1,0], A[1,0]*B[0,1] + A[1,1]*B[1,1]]])
    
    def matrix_pow(M, p):
        if p == 1:
            return M
        if p % 2 == 0:
            half = matrix_pow(M, p // 2)
            return matrix_mult(half, half)
        return matrix_mult(M, matrix_pow(M, p - 1))
    
    F = np.array([[1.0, 1.0], [1.0, 0.0]])
    return matrix_pow(F, n)[0, 1]

# Compare for large n
for n in [50, 70, 80]:
    f_rec = fibonacci_recurrence(n)
    f_binet = fibonacci_binet(n)
    f_matrix = fibonacci_matrix(n)
    
    print(f"\nF({n}):")
    print(f"  Recurrence: {f_rec:.0f}")
    print(f"  Binet:      {f_binet:.0f}")
    print(f"  Matrix:     {f_matrix:.0f}")
```

## Preconditioning

Transform ill-conditioned problems to improve stability.

### 1. Diagonal Preconditioning

Scale rows/columns to improve conditioning.

```python
import numpy as np

def diagonal_preconditioner(A):
    """Simple diagonal preconditioner."""
    D = np.diag(1.0 / np.sqrt(np.diag(A @ A.T)))
    return D

# Ill-conditioned system
A = np.array([[1e6, 1],
              [1, 1e-6]])
b = np.array([1e6 + 1, 1 + 1e-6])

print(f"Original condition number: {np.linalg.cond(A):.2e}")

# Precondition
D = diagonal_preconditioner(A)
A_precond = D @ A
b_precond = D @ b

print(f"Preconditioned condition:  {np.linalg.cond(A_precond):.2e}")

# Solve
x_original = np.linalg.solve(A, b)
x_precond = np.linalg.solve(A_precond, b_precond)

print(f"\nSolution (original):      {x_original}")
print(f"Solution (preconditioned): {x_precond}")
```

### 2. Iterative Refinement

Improve solution by correcting residuals.

```python
import numpy as np

def iterative_refinement(A, b, x0, max_iter=5):
    """Improve solution via residual correction."""
    x = x0.copy()
    
    for i in range(max_iter):
        # Compute residual in higher precision (simulated)
        r = b - A @ x
        
        # Solve for correction
        dx = np.linalg.solve(A, r)
        
        # Update solution
        x = x + dx
        
        print(f"  Iter {i+1}: residual norm = {np.linalg.norm(r):.2e}")
    
    return x

# Test
np.random.seed(42)
A = np.random.randn(50, 50)
x_true = np.random.randn(50)
b = A @ x_true

# Initial solve with some error
x_initial = np.linalg.solve(A, b)
# Add artificial error to simulate single precision
x_initial += 1e-8 * np.random.randn(50)

print(f"Initial error: {np.linalg.norm(x_initial - x_true):.2e}")
x_refined = iterative_refinement(A, b, x_initial)
print(f"Refined error: {np.linalg.norm(x_refined - x_true):.2e}")
```

## Stability in Machine Learning

Neural network training requires careful numerical handling.

### 1. Gradient Clipping

Prevent exploding gradients.

```python
import numpy as np

def clip_gradients(grads, max_norm=1.0):
    """Clip gradients to prevent explosion."""
    total_norm = np.sqrt(sum(np.sum(g**2) for g in grads))
    
    if total_norm > max_norm:
        scale = max_norm / total_norm
        return [g * scale for g in grads]
    return grads

# Simulate gradient computation
np.random.seed(42)
grads = [np.random.randn(100, 100) * 10 for _ in range(3)]

original_norm = np.sqrt(sum(np.sum(g**2) for g in grads))
clipped_grads = clip_gradients(grads, max_norm=1.0)
clipped_norm = np.sqrt(sum(np.sum(g**2) for g in clipped_grads))

print(f"Original gradient norm: {original_norm:.2f}")
print(f"Clipped gradient norm:  {clipped_norm:.2f}")
```

### 2. Log-Sum-Exp Trick

Stable softmax computation.

```python
import numpy as np

def softmax_naive(x):
    """Naive softmax (overflow-prone)."""
    exp_x = np.exp(x)
    return exp_x / np.sum(exp_x)

def softmax_stable(x):
    """Numerically stable softmax."""
    x_shifted = x - np.max(x)  # Prevent overflow
    exp_x = np.exp(x_shifted)
    return exp_x / np.sum(exp_x)

# Test with large values
x = np.array([1000, 1001, 1002])

print("Naive softmax:")
try:
    print(f"  {softmax_naive(x)}")
except:
    print("  Overflow!")

print("Stable softmax:")
print(f"  {softmax_stable(x)}")

# Verify: should sum to 1
print(f"  Sum: {np.sum(softmax_stable(x))}")
```

### 3. Batch Normalization

Stabilize training by normalizing activations.

```python
import numpy as np

def batch_norm(x, eps=1e-5):
    """Batch normalization for numerical stability."""
    mean = np.mean(x, axis=0)
    var = np.var(x, axis=0)
    
    # Normalize with epsilon for stability
    x_norm = (x - mean) / np.sqrt(var + eps)
    
    return x_norm, mean, var

# Simulate activations with varying scales
np.random.seed(42)
activations = np.random.randn(32, 100) * np.random.uniform(0.01, 100, 100)

print(f"Before normalization:")
print(f"  Mean range: [{activations.mean(axis=0).min():.2f}, {activations.mean(axis=0).max():.2f}]")
print(f"  Std range:  [{activations.std(axis=0).min():.2f}, {activations.std(axis=0).max():.2f}]")

normalized, _, _ = batch_norm(activations)

print(f"\nAfter normalization:")
print(f"  Mean range: [{normalized.mean(axis=0).min():.4f}, {normalized.mean(axis=0).max():.4f}]")
print(f"  Std range:  [{normalized.std(axis=0).min():.4f}, {normalized.std(axis=0).max():.4f}]")
```

## Testing for Stability

Verify your implementations are numerically sound.

### 1. Perturbation Testing

Check sensitivity to small input changes.

```python
import numpy as np

def test_stability(func, x, n_tests=100, perturbation=1e-10):
    """Test function stability under perturbations."""
    base_result = func(x)
    max_amplification = 0
    
    for _ in range(n_tests):
        # Random perturbation
        delta = perturbation * np.random.randn(*np.atleast_1d(x).shape)
        perturbed_x = x + delta
        
        perturbed_result = func(perturbed_x)
        
        # Measure amplification
        input_change = np.linalg.norm(delta) / np.linalg.norm(x)
        output_change = np.linalg.norm(perturbed_result - base_result) / np.linalg.norm(base_result)
        
        if input_change > 0:
            amplification = output_change / input_change
            max_amplification = max(max_amplification, amplification)
    
    return max_amplification

# Test matrix inversion stability
np.random.seed(42)
A = np.random.randn(10, 10)

amp = test_stability(np.linalg.inv, A)
cond = np.linalg.cond(A)

print(f"Condition number:    {cond:.2f}")
print(f"Max amplification:   {amp:.2f}")
print(f"Ratio:               {amp/cond:.2f}")  # Should be ~1 for stable algorithm
```

### 2. Backward Error Check

Verify computed result solves a nearby problem.

```python
import numpy as np

def backward_error_test(A, b, x_computed):
    """
    Compute backward error for linear solve.
    Small value indicates backward stability.
    """
    residual = A @ x_computed - b
    
    # Relative backward error
    backward_err = np.linalg.norm(residual) / (np.linalg.norm(A) * np.linalg.norm(x_computed) + np.linalg.norm(b))
    
    return backward_err

# Test various solvers
np.random.seed(42)
A = np.random.randn(100, 100)
x_true = np.random.randn(100)
b = A @ x_true

methods = [
    ("np.linalg.solve", lambda A, b: np.linalg.solve(A, b)),
    ("np.linalg.inv @", lambda A, b: np.linalg.inv(A) @ b),
    ("np.linalg.lstsq", lambda A, b: np.linalg.lstsq(A, b, rcond=None)[0]),
]

print(f"Machine epsilon: {np.finfo(float).eps:.2e}\n")
for name, solver in methods:
    x = solver(A, b)
    be = backward_error_test(A, b, x)
    print(f"{name:20s}: backward error = {be:.2e}")
```

---

## Exercises

**Exercise 1.**
Summation order affects numerical accuracy. Predict which method gives a result closer to the true sum:

```python
import random
random.seed(42)

numbers = [random.uniform(-1e10, 1e10) for _ in range(100000)]
numbers.extend([random.uniform(-1e-5, 1e-5) for _ in range(100000)])

sum_naive = sum(numbers)
sum_sorted = sum(sorted(numbers, key=abs))

import math
sum_accurate = math.fsum(numbers)

print(f"Naive - accurate:  {abs(sum_naive - sum_accurate):.2e}")
print(f"Sorted - accurate: {abs(sum_sorted - sum_accurate):.2e}")
```

Why does sorting by magnitude before summing improve accuracy? What does `math.fsum` do differently from both approaches?

??? success "Solution to Exercise 1"
    The sorted sum produces a smaller error than the naive sum (though both may differ from `math.fsum`).

    When adding numbers of vastly different magnitudes, small values get rounded away when added to large partial sums. Sorting by magnitude and adding small values first keeps the partial sum small, preserving more bits of the small values.

    `math.fsum` uses a completely different approach: it maintains a list of partial sums with no rounding error (using Shewchuk's algorithm). It tracks all intermediate rounding errors exactly and compensates for them, producing a correctly-rounded result. This is O(n) in time but uses O(n) auxiliary space in the worst case.

---

**Exercise 2.**
Computing variance can be numerically unstable. Predict which method is more accurate:

```python
import math

data = [1e9 + x for x in [1, 2, 3, 4, 5]]

# Method A: naive formula var = E[x^2] - E[x]^2
mean_sq = sum(x**2 for x in data) / len(data)
sq_mean = (sum(data) / len(data)) ** 2
var_naive = mean_sq - sq_mean

# Method B: two-pass
mean = sum(data) / len(data)
var_twopass = sum((x - mean)**2 for x in data) / len(data)

print(f"Naive variance:    {var_naive}")
print(f"Two-pass variance: {var_twopass}")
print(f"True variance:     {2.0}")
```

Why does the naive formula `E[x^2] - E[x]^2` fail catastrophically here? What is the root cause?

??? success "Solution to Exercise 2"
    Output (approximately):

    ```text
    Naive variance:    0.0
    Two-pass variance: 2.0
    True variance:     2.0
    ```

    The naive formula computes `E[x^2] - E[x]^2`, which requires subtracting two nearly equal enormous numbers: `E[x^2]` is approximately `1e18` and `E[x]^2` is also approximately `1e18`. The true difference is `2.0`, but both terms have only ~15 digits of precision, so the meaningful digits are completely lost to catastrophic cancellation.

    The two-pass method first computes the mean, then computes deviations `(x - mean)`. These deviations are small numbers (1, 2, 3, 4, 5 offset from the mean), so no cancellation occurs. The root cause is always the same: subtracting nearly equal large numbers destroys significant digits.

---

**Exercise 3.**
Comparing floats for equality is unreliable. Predict the output:

```python
import math

a = 0.1 + 0.2
b = 0.3

print(a == b)
print(math.isclose(a, b))
print(math.isclose(a, b, rel_tol=1e-16))
print(math.isclose(1e-300, 0.0))
print(math.isclose(1e-300, 0.0, abs_tol=1e-299))
```

Why does `math.isclose(1e-300, 0.0)` return `False`? When comparing values near zero, why is `rel_tol` insufficient and `abs_tol` necessary?

??? success "Solution to Exercise 3"
    Output:

    ```text
    False
    True
    False
    False
    True
    ```

    `math.isclose` uses the formula: `abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)`. The default is `rel_tol=1e-9` and `abs_tol=0.0`.

    `math.isclose(1e-300, 0.0)` returns `False` because with `abs_tol=0.0`, the only tolerance is relative: `rel_tol * max(1e-300, 0.0) = 1e-9 * 1e-300 = 1e-309`, which is smaller than `1e-300`. Relative tolerance breaks down near zero because any nonzero value is infinitely far from zero in relative terms.

    When comparing values that might be near zero, you must specify `abs_tol` to define what "close to zero" means for your application.
