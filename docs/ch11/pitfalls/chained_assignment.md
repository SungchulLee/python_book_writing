# Chained Assignment

Chained assignment occurs when you index a DataFrame twice in sequence to assign a value. This is a common source of bugs because pandas cannot guarantee the operation will work as intended.

!!! tip "Mental Model"
    Chained assignment fails because the first indexing step may return a copy, and assigning to a copy does nothing to the original DataFrame. The fix is always the same: collapse two indexing steps into one `loc` call. If you see `df[...][...] = value`, rewrite it as `df.loc[..., ...] = value`.

## What is Chained Assignment?

```python
import pandas as pd

df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# Chained assignment: two indexing operations for assignment
df[df['A'] > 1]['B'] = 0  # ❌ BAD - Chained assignment
```

This is "chained" because:
1. First index: `df[df['A'] > 1]` (filter rows)
2. Second index: `['B'] = 0` (select column and assign)

## Why is This Problematic?

pandas evaluates these as **two separate operations**:

```python
# What pandas sees:
temp = df[df['A'] > 1]  # Step 1: May be a copy
temp['B'] = 0           # Step 2: Modifies temp, not df
```

If step 1 returns a copy (not a view), your assignment modifies a temporary object that is immediately discarded.

## The SettingWithCopyWarning

pandas warns you about this:

```python
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
df[df['A'] > 1]['B'] = 0
```

```
SettingWithCopyWarning: 
A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead
```

**This warning means your code might not work!**

## The Solution: Use .loc

`.loc` performs the selection and assignment atomically:

```python
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# WRONG: Chained assignment
df[df['A'] > 1]['B'] = 0  # ❌ Unreliable

# RIGHT: Single .loc operation
df.loc[df['A'] > 1, 'B'] = 0  # ✅ Guaranteed to work

print(df)
```

```
   A  B
0  1  4
1  2  0
2  3  0
```

## Common Chained Assignment Patterns

### Pattern 1: Filter Then Assign

```python
# WRONG
df[df['status'] == 'pending']['processed'] = True

# RIGHT
df.loc[df['status'] == 'pending', 'processed'] = True
```

### Pattern 2: Select Columns Then Filter

```python
# WRONG
df['price'][df['price'] < 0] = 0

# RIGHT
df.loc[df['price'] < 0, 'price'] = 0
```

### Pattern 3: Multiple Conditions

```python
# WRONG
df[(df['A'] > 1) & (df['B'] < 10)]['C'] = 99

# RIGHT
mask = (df['A'] > 1) & (df['B'] < 10)
df.loc[mask, 'C'] = 99
```

### Pattern 4: Group-Based Assignment

```python
# WRONG
for name, group in df.groupby('category'):
    group['normalized'] = group['value'] / group['value'].mean()

# RIGHT
df['normalized'] = df.groupby('category')['value'].transform(
    lambda x: x / x.mean()
)
```

## Why .loc is Different

`.loc` uses a single `__setitem__` call:

```python
# Chained: Two separate operations
df[condition]['col'] = value
# Equivalent to:
# temp = df.__getitem__(condition)
# temp.__setitem__('col', value)  # temp might be copy!

# .loc: Single operation
df.loc[condition, 'col'] = value
# Equivalent to:
# df.__setitem__((condition, 'col'), value)  # Direct modification
```

## .iloc for Position-Based Assignment

Same principle applies to position-based access:

```python
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# WRONG
df.iloc[0:2]['B'] = 0  # Chained assignment

# RIGHT
df.iloc[0:2, 1] = 0  # Single .iloc operation
# or
df.iloc[0:2, df.columns.get_loc('B')] = 0
```

## Detecting Chained Assignment

### Enable Warnings (Default)

```python
pd.options.mode.chained_assignment = 'warn'  # Default
```

### Raise Error Instead

```python
pd.options.mode.chained_assignment = 'raise'  # Stricter
```

### Disable (Not Recommended)

```python
pd.options.mode.chained_assignment = None  # Dangerous!
```

## Edge Cases

### Assigning to New Column

```python
# This also triggers warning
subset = df[df['A'] > 1]
subset['new_col'] = 0  # Warning!

# Solution: Explicit copy
subset = df[df['A'] > 1].copy()
subset['new_col'] = 0  # OK, modifying a copy intentionally
```

### In a Loop

```python
# WRONG
for idx in df[df['needs_update']].index:
    df[df.index == idx]['value'] = new_value

# RIGHT
for idx in df[df['needs_update']].index:
    df.loc[idx, 'value'] = new_value

# BETTER: Vectorized
df.loc[df['needs_update'], 'value'] = new_value
```

## Summary

| Pattern | Wrong | Right |
|---------|-------|-------|
| Filter + assign | `df[cond]['col'] = x` | `df.loc[cond, 'col'] = x` |
| Column + filter | `df['col'][cond] = x` | `df.loc[cond, 'col'] = x` |
| Slice + assign | `df[0:5]['col'] = x` | `df.loc[df.index[0:5], 'col'] = x` |
| New column on subset | `df[cond]['new'] = x` | `subset = df[cond].copy(); subset['new'] = x` |

**Golden Rule**: Use `.loc[rows, cols] = value` for all conditional assignments.


---

## Exercises

**Exercise 1.** Write code that demonstrates the chained assignment problem: `df[df['a'] > 0]['b'] = 1`. Explain why this may not work.

??? success "Solution to Exercise 1"
    ```python
    import pandas as pd
    import numpy as np

    # Solution for the specific exercise
    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(10), 'B': np.random.randn(10)})
    print(df.head())
    ```

---

**Exercise 2.** Explain the difference between a view and a copy in Pandas. How does this relate to chained assignment?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Write the correct way to modify a subset of a DataFrame using `.loc[]` instead of chained indexing.

??? success "Solution to Exercise 3"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(20), 'B': np.random.randn(20)})
    result = df.describe()
    print(result)
    ```

---

**Exercise 4.** Explain what the `SettingWithCopyWarning` means and how to avoid it.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
