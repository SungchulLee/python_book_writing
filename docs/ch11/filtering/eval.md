# eval() Method

The `eval()` method provides fast, memory-efficient expression evaluation for column operations. It uses NumExpr under the hood when available, enabling optimized computation.

!!! tip "Mental Model"
    `eval()` takes a string expression like `"A + B * C"` and evaluates it without creating intermediate arrays. For large DataFrames this saves memory because the NumExpr engine fuses operations into a single pass. Think of it as a compiled calculator for column arithmetic -- same result as normal pandas math, but more memory-efficient at scale.

## Basic Syntax

```python
DataFrame.eval(expr, inplace=False)
```

**Parameters:**

- `expr`: String expression to evaluate
- `inplace`: If True, modify DataFrame in place

## Why Use eval()?

### Problem: Standard Operations Create Intermediate Arrays

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'A': np.random.randn(1_000_000),
    'B': np.random.randn(1_000_000),
    'C': np.random.randn(1_000_000)
})

# Standard approach: creates temporary arrays
df['D'] = df['A'] + df['B'] * df['C']
```

This creates intermediate arrays for `df['B'] * df['C']`, consuming extra memory.

### Solution: eval() Does One-Pass Evaluation

```python
# eval approach: single-pass, less memory
df.eval('D = A + B * C', inplace=True)
```

## Creating New Columns

```python
# Single column
df.eval('D = A + B', inplace=True)

# Multiple columns in one call
df.eval('''
    D = A + B
    E = A - B
    F = A * B
''', inplace=True)
```

## Supported Operations

### Arithmetic

```python
df.eval('result = A + B - C * D / E', inplace=True)
df.eval('power = A ** 2', inplace=True)
df.eval('floor_div = A // B', inplace=True)
df.eval('modulo = A % B', inplace=True)
```

### Comparisons

```python
# Returns boolean Series
mask = df.eval('A > B')
high_values = df.eval('A > 0.5 and B > 0.5')
```

### Boolean Logic

```python
# Use 'and', 'or', 'not' (not &, |, ~)
df.eval('flag = (A > 0) and (B < 0)', inplace=True)
df.eval('either = (A > 0) or (B > 0)', inplace=True)
df.eval('neither = not ((A > 0) or (B > 0))', inplace=True)
```

### Parentheses for Complex Expressions

```python
df.eval('result = (A + B) / (C - D)', inplace=True)
df.eval('complex = ((A + B) * C) / (D - E)', inplace=True)
```

## Using Local Variables

Reference local Python variables with `@`:

```python
threshold = 0.5
multiplier = 2.0

# Use @ to reference local variables
df.eval('scaled = A * @multiplier', inplace=True)
df.eval('above_threshold = A > @threshold', inplace=True)

# Multiple local variables
mean_a = df['A'].mean()
std_a = df['A'].std()
df.eval('z_score = (A - @mean_a) / @std_a', inplace=True)
```

## Combining with query()

Use `eval()` for computation, `query()` for filtering:

```python
# Compute
df.eval('ratio = A / B', inplace=True)

# Filter
high_ratio = df.query('ratio > 2')
```

## Performance Comparison

```python
import time

n = 5_000_000
df = pd.DataFrame({
    'A': np.random.randn(n),
    'B': np.random.randn(n),
    'C': np.random.randn(n)
})

# Standard approach
start = time.time()
df['D'] = df['A'] + df['B'] * df['C'] - df['A'] / df['B']
standard_time = time.time() - start

# Reset
df = df.drop('D', axis=1)

# eval approach
start = time.time()
df.eval('D = A + B * C - A / B', inplace=True)
eval_time = time.time() - start

print(f"Standard: {standard_time:.3f}s")
print(f"eval(): {eval_time:.3f}s")
print(f"Speedup: {standard_time/eval_time:.1f}x")
```

Typical results on large DataFrames:
```
Standard: 0.089s
eval(): 0.034s
Speedup: 2.6x
```

## Limitations

### Cannot Use

```python
# Method calls
# df.eval('D = A.abs()')  # Error

# String operations
# df.eval('D = A.str.upper()')  # Error

# Custom functions
# df.eval('D = my_func(A)')  # Error

# Aggregations
# df.eval('D = A.sum()')  # Error
```

### Workarounds

```python
# For method calls, compute first
abs_A = df['A'].abs()
df.eval('D = @abs_A + B', inplace=True)

# Or use standard pandas
df['D'] = df['A'].abs() + df['B']
```

## pd.eval() for Non-DataFrame Operations

Use `pd.eval()` for standalone expressions:

```python
# Evaluate expression on Series
a = pd.Series(np.random.randn(1000))
b = pd.Series(np.random.randn(1000))

result = pd.eval('a + b * 2')
```

## Return vs Inplace

```python
# Return new value (default)
result = df.eval('A + B')  # Returns Series

# Modify in place
df.eval('D = A + B', inplace=True)  # Returns None, modifies df
```

## Practical Examples

### Financial Calculations

```python
portfolio = pd.DataFrame({
    'price': np.random.uniform(10, 100, 100000),
    'shares': np.random.randint(1, 1000, 100000),
    'cost_basis': np.random.uniform(5, 50, 100000)
})

# Calculate multiple metrics efficiently
portfolio.eval('''
    market_value = price * shares
    total_cost = cost_basis * shares
    profit = market_value - total_cost
    return_pct = (profit / total_cost) * 100
''', inplace=True)
```

### Conditional Calculations

```python
# Combine with numpy where for conditionals
df['sign'] = np.where(df.eval('A > 0'), 1, -1)

# Or use boolean eval
df.eval('is_positive = A > 0', inplace=True)
df.eval('is_both_positive = (A > 0) and (B > 0)', inplace=True)
```

### Rolling Metrics with eval

```python
# Compute rolling mean first, then use in eval
df['rolling_mean'] = df['A'].rolling(20).mean()
df.eval('deviation = A - rolling_mean', inplace=True)
```

## Summary

| Feature | Standard Pandas | eval() |
|---------|-----------------|--------|
| Memory usage | Creates intermediates | Single-pass |
| Speed (large data) | Baseline | 2-3x faster |
| Readability | Verbose | Compact |
| Method calls | Supported | Not supported |
| Local variables | Direct use | Use @ prefix |

**When to use eval():**

- Large DataFrames (>100K rows)
- Complex arithmetic expressions
- Memory-constrained environments
- Multiple column operations

**When to use standard pandas:**

- Small DataFrames
- Need method calls (`.abs()`, `.str`, etc.)
- Custom functions required
- Debugging (easier to step through)

---

## Exercises

**Exercise 1.**
Create a DataFrame with columns `'revenue'` and `'cost'`. Use `df.eval('profit = revenue - cost')` to add a new `'profit'` column without modifying the original DataFrame (use `inplace=False`).

??? success "Solution to Exercise 1"
    Use `eval` to create a computed column.

        import pandas as pd

        df = pd.DataFrame({
            'revenue': [100, 200, 300],
            'cost': [60, 120, 180]
        })
        result = df.eval('profit = revenue - cost')
        print(result)

---

**Exercise 2.**
Use `pd.eval()` to compute an expression involving two DataFrames: given `df1` and `df2` each with a column `'value'`, compute `df1['value'] + df2['value']` using `pd.eval('df1.value + df2.value')`.

??? success "Solution to Exercise 2"
    Use `pd.eval()` for cross-DataFrame operations.

        import pandas as pd

        df1 = pd.DataFrame({'value': [10, 20, 30]})
        df2 = pd.DataFrame({'value': [1, 2, 3]})
        result = pd.eval('df1.value + df2.value')
        print(result)

---

**Exercise 3.**
Use `df.eval()` with the `@` syntax to reference a local variable. Given a tax rate stored in a Python variable, compute `after_tax = salary * (1 - @tax_rate)` inside eval.

??? success "Solution to Exercise 3"
    Reference local variables with the `@` prefix.

        import pandas as pd

        df = pd.DataFrame({'salary': [50000, 60000, 70000]})
        tax_rate = 0.25
        result = df.eval('after_tax = salary * (1 - @tax_rate)')
        print(result)
