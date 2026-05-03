# Numerical Errors

Floating-point arithmetic introduces systematic errors that can accumulate and compromise computational results. Understanding these error sources is essential for writing reliable numerical code.

!!! tip "Mental Model"
    Every floating-point operation can introduce a tiny rounding error up to machine epsilon. One error is negligible, but millions of them can snowball -- especially when you subtract nearly equal numbers (catastrophic cancellation) or accumulate a running sum. Awareness of where errors creep in is the first step toward controlling them.

## Round-Off Error

Every floating-point operation may introduce a small rounding error bounded by machine epsilon.

### 1. Operation Model

IEEE 754 guarantees that basic operations are correctly rounded:

$$x \odot y = (x * y)(1 + \delta), \quad |\delta| \leq \epsilon$$

where $\odot$ is the floating-point operation and $*$ is the exact mathematical operation.

```python
import sys

eps = sys.float_info.epsilon
print(f"Machine epsilon: {eps:.2e}")

# Each operation introduces error up to epsilon
a = 1.0
b = 1e-16

# Exact: a + b = 1.0000000000000001
# Float: loses precision
result = a + b
print(f"1.0 + 1e-16 = {result}")
print(f"Error bound: {eps:.2e}")
```

### 2. Error Accumulation

Errors compound over many operations.

```python
# Repeated operations accumulate error
def sum_naive(n):
    """Sum 1/n, n times. Should equal 1."""
    total = 0.0
    increment = 1.0 / n
    for _ in range(n):
        total += increment
    return total

for n in [10, 100, 1000, 10000, 100000]:
    result = sum_naive(n)
    error = abs(result - 1.0)
    print(f"n={n:>6}: result={result:.15f}, error={error:.2e}")

# Error grows roughly as sqrt(n) * epsilon
```

### 3. Kahan Summation

Compensated summation reduces accumulated error.

```python
def sum_kahan(values):
    """Kahan summation algorithm for reduced error."""
    total = 0.0
    compensation = 0.0
    
    for x in values:
        y = x - compensation      # Compensate for lost low-order bits
        t = total + y             # Add compensated value
        compensation = (t - total) - y  # Recover lost bits
        total = t
    
    return total

# Compare naive vs Kahan
n = 100000
values = [1.0 / n] * n

naive_result = sum(values)
kahan_result = sum_kahan(values)

print(f"Naive sum: {naive_result:.15f}")
print(f"Kahan sum: {kahan_result:.15f}")
print(f"Naive error: {abs(naive_result - 1.0):.2e}")
print(f"Kahan error: {abs(kahan_result - 1.0):.2e}")
```

## Catastrophic Cancellation

Subtracting nearly equal numbers amplifies relative error dramatically.

### 1. Mechanism

When $a \approx b$, the subtraction $a - b$ loses significant digits.

```python
# Two numbers with 15 correct digits each
a = 1.000000000000001
b = 1.000000000000000

# Subtraction loses most significant digits
diff = a - b
print(f"a = {a:.15f}")
print(f"b = {b:.15f}")
print(f"a - b = {diff:.15e}")

# Only ~1 significant digit remains
# Expected: 1e-15, but we get noise
```

### 2. Classic Example: Quadratic Formula

The standard quadratic formula suffers from cancellation.

```python
import math

def quadratic_standard(a, b, c):
    """Standard quadratic formula."""
    disc = math.sqrt(b*b - 4*a*c)
    x1 = (-b + disc) / (2*a)
    x2 = (-b - disc) / (2*a)
    return x1, x2

def quadratic_stable(a, b, c):
    """Numerically stable quadratic formula."""
    disc = math.sqrt(b*b - 4*a*c)
    # Choose the root that avoids cancellation
    if b >= 0:
        q = -0.5 * (b + disc)
    else:
        q = -0.5 * (b - disc)
    x1 = q / a
    x2 = c / q
    return x1, x2

# Test case with cancellation: b² >> 4ac
a, b, c = 1, 1e8, 1
print("Standard formula:")
x1, x2 = quadratic_standard(a, b, c)
print(f"  x1 = {x1:.10e}")
print(f"  x2 = {x2:.10e}")

print("\nStable formula:")
x1, x2 = quadratic_stable(a, b, c)
print(f"  x1 = {x1:.10e}")
print(f"  x2 = {x2:.10e}")

# Verify: x1 * x2 should equal c/a = 1
print(f"\nProduct check (should be 1):")
print(f"  Standard: {quadratic_standard(a, b, c)[0] * quadratic_standard(a, b, c)[1]}")
print(f"  Stable: {quadratic_stable(a, b, c)[0] * quadratic_stable(a, b, c)[1]}")
```

### 3. Variance Calculation

Naive variance formula is unstable.

```python
import math

def variance_naive(data):
    """Naive two-pass variance (unstable for large means)."""
    n = len(data)
    sum_x = sum(data)
    sum_x2 = sum(x*x for x in data)
    return (sum_x2 - sum_x*sum_x/n) / (n-1)

def variance_welford(data):
    """Welford's online algorithm (stable)."""
    n = 0
    mean = 0.0
    M2 = 0.0
    
    for x in data:
        n += 1
        delta = x - mean
        mean += delta / n
        delta2 = x - mean
        M2 += delta * delta2
    
    return M2 / (n - 1) if n > 1 else 0.0

# Test with data having large mean
data = [1e9 + x for x in [1, 2, 3, 4, 5]]

print(f"Naive variance:   {variance_naive(data):.10f}")
print(f"Welford variance: {variance_welford(data):.10f}")
print(f"True variance:    {2.5:.10f}")  # var([1,2,3,4,5])
```

### 4. Detecting Cancellation

Monitor significant digit loss.

```python
import math

def significant_digits(x, y, result):
    """Estimate significant digits lost in x - y = result."""
    if result == 0:
        return float('inf')  # Complete cancellation
    
    # Original digits
    original_digits = 15  # Double precision
    
    # Digits in operands vs result
    magnitude_loss = math.log10(max(abs(x), abs(y)) / abs(result))
    
    return max(0, original_digits - magnitude_loss)

# Examples
pairs = [
    (1.0, 0.5),           # No cancellation
    (1.0, 0.99),          # Mild
    (1.0, 0.999999),      # Moderate
    (1.0, 0.999999999999),  # Severe
]

for x, y in pairs:
    result = x - y
    digits = significant_digits(x, y, result)
    print(f"{x} - {y} = {result:.2e}, ~{digits:.1f} digits remain")
```

## Loss of Associativity

Floating-point addition and multiplication are not associative.

### 1. Addition Non-Associativity

$(a + b) + c \neq a + (b + c)$ in floating-point.

```python
# Dramatic example
a = 1e16
b = -1e16
c = 1.0

left = (a + b) + c   # (1e16 + (-1e16)) + 1 = 0 + 1 = 1
right = a + (b + c)  # 1e16 + (-1e16 + 1) = 1e16 + (-1e16) = 0

print(f"(a + b) + c = {left}")
print(f"a + (b + c) = {right}")
print(f"Difference:  {abs(left - right)}")

# Why? b + c = -1e16 because c is lost
print(f"\nb + c = {b + c}")  # -1e16, not -9999999999999999
```

### 2. Multiplication Non-Associativity

Also affects multiplication with extreme values.

```python
# Near overflow
a = 1e200
b = 1e200
c = 1e-200

left = (a * b) * c   # inf * 1e-200 = inf
right = a * (b * c)  # 1e200 * 1 = 1e200

print(f"(a * b) * c = {left}")
print(f"a * (b * c) = {right}")
```

### 3. Summation Order Effects

Order of summation affects result.

```python
import numpy as np

# Create array with large variance in magnitudes
np.random.seed(42)
small = np.random.randn(1000) * 1e-10
large = np.random.randn(1000) * 1e10
data = np.concatenate([small, large])

# Different orderings
sum_original = sum(data)
sum_sorted_asc = sum(sorted(data))
sum_sorted_desc = sum(sorted(data, reverse=True))
sum_abs_sorted = sum(sorted(data, key=abs))

print(f"Original order:    {sum_original:.10e}")
print(f"Ascending sort:    {sum_sorted_asc:.10e}")
print(f"Descending sort:   {sum_sorted_desc:.10e}")
print(f"By magnitude:      {sum_abs_sorted:.10e}")
print(f"NumPy pairwise:    {np.sum(data):.10e}")
```

### 4. Parallel Reduction Issues

Different reduction trees give different results.

```python
import numpy as np

def reduce_left(arr):
    """Left-to-right reduction."""
    result = arr[0]
    for x in arr[1:]:
        result = result + x
    return result

def reduce_pairwise(arr):
    """Pairwise/tree reduction."""
    if len(arr) == 1:
        return arr[0]
    if len(arr) == 2:
        return arr[0] + arr[1]
    mid = len(arr) // 2
    return reduce_pairwise(arr[:mid]) + reduce_pairwise(arr[mid:])

# Test data
np.random.seed(123)
data = np.random.randn(1024).astype(np.float32)

left_result = reduce_left(data)
pairwise_result = reduce_pairwise(data)

print(f"Left reduction:     {left_result}")
print(f"Pairwise reduction: {pairwise_result}")
print(f"Difference:         {abs(left_result - pairwise_result):.2e}")
```

## Overflow and Underflow

Extreme values exceed representable range.

### 1. Overflow to Infinity

Results exceeding maximum representable value become infinity.

```python
import sys
import math

max_float = sys.float_info.max
print(f"Max float: {max_float:.6e}")

# Overflow
result = max_float * 2
print(f"max * 2 = {result}")  # inf

# Overflow in intermediate calculation
a = 1e200
b = 1e200
c = 1e-200

# Bad: overflow in intermediate
try:
    bad = (a * b) * c
    print(f"(a*b)*c = {bad}")  # inf
except:
    pass

# Good: reorder to avoid overflow
good = a * (b * c)
print(f"a*(b*c) = {good}")  # 1e200
```

### 2. Underflow to Zero

Very small values become zero.

```python
import sys

min_float = sys.float_info.min
print(f"Min positive float: {min_float:.6e}")

# Gradual underflow (subnormal numbers)
tiny = 1e-308
for _ in range(20):
    tiny /= 10
    print(f"{tiny:.6e}", end=" ")
    if tiny == 0:
        print("(underflow)")
        break
print()

# Underflow in intermediate calculation
a = 1e-200
b = 1e-200
c = 1e200

# Bad: underflow
bad = (a * b) * c  # 0 * 1e200 = 0
print(f"(a*b)*c = {bad}")

# Good: reorder
good = a * (b * c)  # 1e-200 * 1 = 1e-200
print(f"a*(b*c) = {good}")
```

### 3. Log-Space Computation

Avoid overflow/underflow using logarithms.

```python
import math
import numpy as np

# Problem: compute product of many small numbers
small_values = [1e-100] * 10

# Direct product underflows
direct_product = 1.0
for v in small_values:
    direct_product *= v
print(f"Direct product: {direct_product}")  # 0.0 (underflow)

# Log-space computation
log_sum = sum(math.log(v) for v in small_values)
print(f"Log of product: {log_sum}")  # -2302.58...
print(f"Exact: 10 * log(1e-100) = {10 * math.log(1e-100)}")

# For probabilities, use log-sum-exp
def logsumexp(log_values):
    """Numerically stable log(sum(exp(x)))."""
    max_val = max(log_values)
    return max_val + math.log(sum(math.exp(v - max_val) for v in log_values))

log_probs = [-1000, -1001, -1002]
print(f"logsumexp: {logsumexp(log_probs)}")
print(f"numpy:     {np.logaddexp.reduce(log_probs)}")
```

## Error Propagation

Understanding how errors compound through calculations.

### 1. Forward Error Analysis

Track how input errors affect output.

```python
import math

def propagate_error(f, x, dx):
    """
    Estimate output error given input error.
    Uses first-order Taylor expansion.
    """
    # Numerical derivative
    h = 1e-8 * max(abs(x), 1)
    df_dx = (f(x + h) - f(x - h)) / (2 * h)
    
    # Error propagation: dy ≈ |f'(x)| * dx
    dy = abs(df_dx) * dx
    
    return f(x), dy

# Example: sin(x) near x = 0
x = 0.001
dx = 1e-10

y, dy = propagate_error(math.sin, x, dx)
print(f"sin({x}) = {y:.10e}")
print(f"Input error:  {dx:.2e}")
print(f"Output error: {dy:.2e}")
print(f"Amplification: {dy/dx:.2f}x")

# Example: sin(x) near x = π/2 (derivative near 0)
x = math.pi / 2 - 0.001
y, dy = propagate_error(math.sin, x, dx)
print(f"\nsin({x:.4f}) = {y:.10f}")
print(f"Output error: {dy:.2e}")
print(f"Amplification: {dy/dx:.2f}x")
```

### 2. Condition Number

Measures sensitivity of a problem to input perturbations.

$$\kappa = \left| \frac{x f'(x)}{f(x)} \right|$$

```python
import math

def condition_number(f, x, h=1e-8):
    """Compute condition number of f at x."""
    fx = f(x)
    if fx == 0:
        return float('inf')
    
    # Numerical derivative
    df = (f(x + h) - f(x - h)) / (2 * h)
    
    return abs(x * df / fx)

# Well-conditioned: sqrt
print(f"sqrt(100) condition: {condition_number(math.sqrt, 100):.2f}")

# Ill-conditioned: x - 1 near x = 1
print(f"(x-1) at x=1.001 condition: {condition_number(lambda x: x-1, 1.001):.2f}")

# Very ill-conditioned: tan near π/2
print(f"tan near π/2 condition: {condition_number(math.tan, 1.57):.2f}")
```

### 3. Backward Error Analysis

Characterize computed result as exact result of perturbed input.

```python
def backward_error(f, x, computed_result):
    """
    Find perturbation δ such that f(x + δ) = computed_result exactly.
    Uses Newton's method.
    """
    # Find x_perturbed such that f(x_perturbed) = computed_result
    x_pert = x
    for _ in range(10):
        fx = f(x_pert)
        h = 1e-10 * max(abs(x_pert), 1)
        df = (f(x_pert + h) - f(x_pert - h)) / (2 * h)
        if abs(df) < 1e-15:
            break
        x_pert = x_pert - (fx - computed_result) / df
    
    return abs(x_pert - x)

# Example: computed sqrt with small error
import math
x = 2.0
exact = math.sqrt(x)
computed = exact + 1e-10  # Simulate small error

delta = backward_error(math.sqrt, x, computed)
print(f"sqrt({x}) computed with error 1e-10")
print(f"Backward error (input perturbation): {delta:.2e}")
print(f"Relative backward error: {delta/x:.2e}")
```

## Mitigation Strategies

Techniques to minimize numerical error impact.

### 1. Algorithm Selection

Choose stable algorithms for sensitive operations.

```python
import numpy as np

# Solving linear system Ax = b
np.random.seed(42)
n = 100

# Well-conditioned system
A_good = np.eye(n) + 0.1 * np.random.randn(n, n)
b = np.random.randn(n)

# Methods comparison
x_solve = np.linalg.solve(A_good, b)
x_lstsq = np.linalg.lstsq(A_good, b, rcond=None)[0]
x_inv = np.linalg.inv(A_good) @ b  # Don't do this!

# Check residuals
print("Residual norms:")
print(f"  solve:  {np.linalg.norm(A_good @ x_solve - b):.2e}")
print(f"  lstsq:  {np.linalg.norm(A_good @ x_lstsq - b):.2e}")
print(f"  inv:    {np.linalg.norm(A_good @ x_inv - b):.2e}")
```

### 2. Scaling

Normalize data to avoid extreme magnitudes.

```python
import numpy as np

# Problem: dot product of large vectors
a = np.array([1e150, 1e150, 1e150])
b = np.array([1e150, 1e150, 1e150])

# Direct computation overflows
direct = np.dot(a, b)
print(f"Direct dot product: {direct}")  # inf

# Scaled computation
scale_a = np.linalg.norm(a)
scale_b = np.linalg.norm(b)
a_normalized = a / scale_a
b_normalized = b / scale_b

scaled_dot = np.dot(a_normalized, b_normalized) * scale_a * scale_b
print(f"Scaled dot product: {scaled_dot:.2e}")
```

### 3. Extended Precision

Use higher precision for critical calculations.

```python
from decimal import Decimal, getcontext

# Set high precision
getcontext().prec = 50

# Standard float fails
a = 0.1 + 0.2
print(f"Float: 0.1 + 0.2 = {a}")
print(f"Float: 0.1 + 0.2 == 0.3? {a == 0.3}")

# Decimal succeeds
a_dec = Decimal('0.1') + Decimal('0.2')
print(f"\nDecimal: 0.1 + 0.2 = {a_dec}")
print(f"Decimal: 0.1 + 0.2 == 0.3? {a_dec == Decimal('0.3')}")

# High-precision calculation
pi_approx = sum(Decimal((-1)**k) / Decimal(2*k + 1) for k in range(1000)) * 4
print(f"\nπ approximation: {pi_approx}")
```

### 4. Interval Arithmetic

Track error bounds explicitly.

```python
class Interval:
    """Simple interval arithmetic."""
    def __init__(self, lo, hi=None):
        self.lo = lo
        self.hi = hi if hi is not None else lo
    
    def __add__(self, other):
        return Interval(self.lo + other.lo, self.hi + other.hi)
    
    def __mul__(self, other):
        products = [self.lo * other.lo, self.lo * other.hi,
                   self.hi * other.lo, self.hi * other.hi]
        return Interval(min(products), max(products))
    
    def __repr__(self):
        return f"[{self.lo:.6f}, {self.hi:.6f}]"

# Represent 0.1 with its actual bounds
eps = 2**-53
x = Interval(0.1 - eps, 0.1 + eps)
y = Interval(0.2 - eps, 0.2 + eps)

result = x + y
print(f"0.1 + 0.2 ∈ {result}")
print(f"Contains 0.3? {result.lo <= 0.3 <= result.hi}")
```


---

## Exercises


**Exercise 1.**
Demonstrate catastrophic cancellation by computing `(1 + 1e-16) - 1` and comparing it to the expected result `1e-16`. How many significant digits are lost?

??? success "Solution to Exercise 1"

    ```python
    result = (1 + 1e-16) - 1
    expected = 1e-16
    print(f"Computed: {result}")
    print(f"Expected: {expected}")
    print(f"Relative error: {abs(result - expected) / expected:.2%}")
    ```

    The result is `0.0` instead of `1e-16`. Adding `1e-16` to `1.0` does not change the float because the value falls below machine epsilon. All significant digits are lost.

---

**Exercise 2.**
Implement Kahan summation and compare it against the built-in `sum()` when adding `[0.1] * 10000`. Report the error of each relative to the expected value `1000.0`.

??? success "Solution to Exercise 2"

    ```python
    def kahan_sum(values):
        total = 0.0
        compensation = 0.0
        for x in values:
            y = x - compensation
            t = total + y
            compensation = (t - total) - y
            total = t
        return total

    values = [0.1] * 10000
    expected = 1000.0

    builtin_result = sum(values)
    kahan_result = kahan_sum(values)

    print(f"sum():  {builtin_result:.15f}, error: {abs(builtin_result - expected):.2e}")
    print(f"kahan:  {kahan_result:.15f}, error: {abs(kahan_result - expected):.2e}")
    ```

    Kahan summation tracks a compensation term that captures the low-order bits lost during each addition, producing a result much closer to the true value.

---

**Exercise 3.**
Show that floating-point addition is not associative by finding three values `a`, `b`, `c` where `(a + b) + c != a + (b + c)`. Print both results and their difference.

??? success "Solution to Exercise 3"

    ```python
    a = 1e16
    b = -1e16
    c = 1.0

    left = (a + b) + c
    right = a + (b + c)

    print(f"(a + b) + c = {left}")   # 1.0
    print(f"a + (b + c) = {right}")  # 0.0
    print(f"Difference: {abs(left - right)}")  # 1.0
    ```

    `b + c` equals `-1e16` because `c = 1.0` is too small relative to `-1e16` to affect the sum. So `a + (b + c) = 0.0`. But `(a + b) = 0.0`, then `0.0 + c = 1.0`.
