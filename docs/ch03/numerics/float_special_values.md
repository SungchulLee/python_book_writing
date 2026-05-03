# Float Special Values

Python floats include special values for infinity and undefined results. Understanding these values is essential for robust numerical code.

!!! tip "Mental Model"
    IEEE 754 reserves special bit patterns for three edge cases: positive infinity, negative infinity, and NaN ("not a number"). Infinity behaves like a mathematical limit -- it is greater than every finite number. NaN is the toxic value: any arithmetic with NaN produces NaN, and `NaN != NaN` is `True`, making it the only Python value not equal to itself.

## Infinity

Representing unbounded values.

### 1. Creating Infinity

Multiple ways to create infinite values.

```python
import math

# From string
pos_inf = float('inf')
neg_inf = float('-inf')

print(pos_inf)   # inf
print(neg_inf)   # -inf

# Using math module
print(math.inf)   # inf
print(-math.inf)  # -inf

# Check type
print(type(pos_inf))  # <class 'float'>
```

### 2. Infinity Comparisons

Infinity compares as expected.

```python
import math

inf = float('inf')

# Greater than any finite number
print(inf > 1e308)       # True
print(inf > 10**1000)    # Error: int too large

# Comparison between infinities
print(float('inf') == float('inf'))   # True
print(float('inf') > float('-inf'))   # True

# Check for infinity
print(math.isinf(inf))        # True
print(math.isinf(-inf))       # True
print(math.isinf(1e308))      # False
```

### 3. Infinity Arithmetic

Operations with infinity.

```python
import math

inf = float('inf')

# Arithmetic results
print(inf + 1)        # inf
print(inf + inf)      # inf
print(inf * 2)        # inf
print(inf * -1)       # -inf
print(1 / inf)        # 0.0
print(-1 / inf)       # -0.0

# Undefined operations produce NaN
print(inf - inf)      # nan
print(inf / inf)      # nan
print(0 * inf)        # nan
```

## Not a Number

Representing undefined or unrepresentable values.

### 1. Creating NaN

Ways to produce NaN values.

```python
import math

# From string
nan = float('nan')
print(nan)           # nan

# Using math module
print(math.nan)      # nan

# From undefined operations
print(float('inf') - float('inf'))  # nan
print(0.0 / 0.0)     # Error! ZeroDivisionError
```

### 2. NaN Comparisons

NaN has unusual comparison behavior.

```python
import math

nan = float('nan')

# NaN is not equal to anything, including itself
print(nan == nan)        # False
print(nan != nan)        # True
print(nan < 1)           # False
print(nan > 1)           # False
print(nan == float('nan'))  # False

# Check for NaN
print(math.isnan(nan))   # True
```

### 3. NaN Propagation

NaN propagates through operations.

```python
import math

nan = float('nan')

# Any operation with NaN produces NaN
print(nan + 1)        # nan
print(nan * 0)        # nan
print(nan ** 0)       # 1.0 (special case!)
print(max(1, 2, nan)) # nan

# Comparison functions return False
print(min(1, nan))    # nan (unexpected behavior)
```

## Checking Special Values

Functions for detecting special values.

### 1. math Functions

Built-in checking functions.

```python
import math

values = [1.0, float('inf'), float('-inf'), float('nan')]

for v in values:
    print(f"{str(v):5} | "
          f"isinf: {math.isinf(v)} | "
          f"isnan: {math.isnan(v)} | "
          f"isfinite: {math.isfinite(v)}")

# Output:
# 1.0   | isinf: False | isnan: False | isfinite: True
# inf   | isinf: True  | isnan: False | isfinite: False
# -inf  | isinf: True  | isnan: False | isfinite: False
# nan   | isinf: False | isnan: True  | isfinite: False
```

### 2. NumPy Functions

Array-aware checking.

```python
import numpy as np

arr = np.array([1.0, np.inf, -np.inf, np.nan])

print(np.isinf(arr))     # [False  True  True False]
print(np.isnan(arr))     # [False False False  True]
print(np.isfinite(arr))  # [ True False False False]

# Count special values
print(np.sum(np.isnan(arr)))  # 1
print(np.sum(np.isinf(arr)))  # 2
```

### 3. Filtering Values

Remove or replace special values.

```python
import numpy as np

arr = np.array([1.0, 2.0, np.nan, 4.0, np.inf])

# Filter out non-finite values
clean = arr[np.isfinite(arr)]
print(clean)  # [1. 2. 4.]

# Replace NaN with a value
filled = np.nan_to_num(arr, nan=0.0, posinf=999.0)
print(filled)  # [1. 2. 0. 4. 999.]
```

## Signed Zero

Positive and negative zero.

### 1. Creating Signed Zero

Both +0.0 and -0.0 exist.

```python
pos_zero = 0.0
neg_zero = -0.0

print(pos_zero)      # 0.0
print(neg_zero)      # -0.0

# They are equal
print(pos_zero == neg_zero)  # True
```

### 2. Distinguishing Zeros

Using math.copysign to detect sign.

```python
import math

pos_zero = 0.0
neg_zero = -0.0

# copysign reveals the sign
print(math.copysign(1, pos_zero))   # 1.0
print(math.copysign(1, neg_zero))   # -1.0

# Division behavior differs
print(1 / pos_zero)   # inf
print(1 / neg_zero)   # -inf
```

### 3. When Sign Matters

Practical implications of signed zero.

```python
import math

# atan2 distinguishes signed zero
print(math.atan2(0.0, -1))    # π (3.14159...)
print(math.atan2(-0.0, -1))   # -π (-3.14159...)

# Logarithm of zero
# print(math.log(0.0))   # ValueError
# print(math.log(-0.0))  # ValueError
```

## Edge Cases

Handling boundary conditions.

### 1. Overflow to Infinity

Large values become infinity.

```python
import sys

# Approaching maximum
large = sys.float_info.max
print(large)           # 1.7976931348623157e+308

# Overflow
print(large * 2)       # inf
print(1e308 * 10)      # inf
```

### 2. Underflow to Zero

Small values become zero.

```python
import sys

# Approaching minimum
small = sys.float_info.min
print(small)           # 2.2250738585072014e-308

# Underflow
print(small / 1e10)    # 2.225e-318 (subnormal)
print(small / 1e308)   # 0.0 (underflow)
```

### 3. Division by Zero

Float division by zero produces infinity.

```python
# Float division by zero
print(1.0 / 0.0)    # ZeroDivisionError in Python!

# But some operations work
import numpy as np
np.seterr(divide='ignore')
print(np.float64(1.0) / np.float64(0.0))  # inf

# Integer division always raises
# print(1 / 0)      # ZeroDivisionError
```

## Defensive Programming

Safe handling of special values.

### 1. Input Validation

Check inputs before operations.

```python
import math

def safe_divide(a, b):
    """Division with special value handling."""
    if math.isnan(a) or math.isnan(b):
        return float('nan')
    if b == 0:
        if a == 0:
            return float('nan')
        return math.copysign(float('inf'), a * b)
    return a / b

print(safe_divide(1, 2))       # 0.5
print(safe_divide(1, 0))       # inf
print(safe_divide(float('nan'), 1))  # nan
```

### 2. Result Validation

Check outputs after operations.

```python
import math

def compute_with_check(func, *args):
    """Execute function and validate result."""
    result = func(*args)
    
    if math.isnan(result):
        raise ValueError("Computation produced NaN")
    if math.isinf(result):
        raise OverflowError("Computation produced infinity")
    
    return result

# Usage
try:
    result = compute_with_check(math.sqrt, -1)
except ValueError as e:
    print(f"Error: {e}")  # Error: Computation produced NaN
```

### 3. Graceful Defaults

Provide fallback values.

```python
import math

def safe_log(x, default=float('-inf')):
    """Logarithm with fallback for invalid input."""
    if x <= 0 or math.isnan(x):
        return default
    return math.log(x)

print(safe_log(10))     # 2.302...
print(safe_log(0))      # -inf
print(safe_log(-1))     # -inf

def safe_mean(values, default=0.0):
    """Mean with fallback for empty input."""
    finite = [v for v in values if math.isfinite(v)]
    if not finite:
        return default
    return sum(finite) / len(finite)

print(safe_mean([1, 2, float('nan'), 4]))  # 2.333...
print(safe_mean([]))     # 0.0
```


---

## Exercises


**Exercise 1.**
Write a function `classify_float(x)` that returns `"positive infinity"`, `"negative infinity"`, `"NaN"`, or `"finite"` for any given float value. Use the `math` module.

??? success "Solution to Exercise 1"

    ```python
    import math

    def classify_float(x):
        if math.isnan(x):
            return "NaN"
        elif math.isinf(x):
            return "positive infinity" if x > 0 else "negative infinity"
        else:
            return "finite"

    print(classify_float(float('inf')))   # positive infinity
    print(classify_float(float('nan')))   # NaN
    print(classify_float(3.14))           # finite
    print(classify_float(float('-inf')))  # negative infinity
    ```

    Check NaN first because `math.isinf(nan)` returns `False`, but NaN also fails all comparison operators.

---

**Exercise 2.**
Demonstrate that `float('nan') != float('nan')` is `True`. Then write a function `safe_equal(a, b)` that correctly handles NaN comparisons (two NaN values should be considered equal).

??? success "Solution to Exercise 2"

    ```python
    import math

    # NaN is not equal to itself
    print(float('nan') != float('nan'))  # True

    def safe_equal(a, b):
        if math.isnan(a) and math.isnan(b):
            return True
        return a == b

    print(safe_equal(float('nan'), float('nan')))  # True
    print(safe_equal(1.0, 1.0))                    # True
    print(safe_equal(1.0, 2.0))                    # False
    ```

    The standard `==` operator returns `False` for NaN comparisons. The workaround uses `math.isnan()` to detect NaN values explicitly.

---

**Exercise 3.**
Create a list containing `[1.0, float('inf'), float('nan'), -2.5, float('-inf')]`. Write code that filters out all non-finite values and computes the mean of the remaining finite values.

??? success "Solution to Exercise 3"

    ```python
    import math

    values = [1.0, float('inf'), float('nan'), -2.5, float('-inf')]

    finite_values = [x for x in values if math.isfinite(x)]
    mean = sum(finite_values) / len(finite_values)

    print(finite_values)  # [1.0, -2.5]
    print(mean)           # -0.75
    ```

    `math.isfinite()` returns `True` only for values that are neither infinity nor NaN.
