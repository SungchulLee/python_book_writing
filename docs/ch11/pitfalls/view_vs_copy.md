# View vs Copy

One of the most common sources of bugs in pandas is confusion between views and copies. Understanding when pandas returns a view (reference to original data) vs a copy (independent duplicate) is essential for avoiding silent data corruption.

!!! tip "Mental Model"
    A view shares memory with the original -- modifying the view modifies the original. A copy is independent -- modifying it leaves the original untouched. The problem is that pandas does not guarantee which one you get from slicing. The safe rule: call `.copy()` explicitly when you want independence, and use `.loc` for in-place assignment on the original.

## The Problem

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# Is this a view or a copy?
subset = df[df['A'] > 1]
subset['B'] = 99  # Does this modify df?

print(df)  # Is df changed?
```

The answer depends on pandas internals and can vary between versions. **This unpredictability is the problem.**

## What is a View?

A **view** shares memory with the original DataFrame:

```python
# Arrays can have views
arr = np.array([1, 2, 3, 4, 5])
view = arr[1:4]  # This is a view

view[0] = 999
print(arr)  # [1, 999, 3, 4, 5] - Original changed!
```

## What is a Copy?

A **copy** is independent - modifying it doesn't affect the original:

```python
arr = np.array([1, 2, 3, 4, 5])
copy = arr[1:4].copy()  # Explicit copy

copy[0] = 999
print(arr)  # [1, 2, 3, 4, 5] - Original unchanged
```

## When Does pandas Return a View?

### Likely View (But Not Guaranteed)

```python
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# Single column selection - often a view
col = df['A']

# Slice of rows - sometimes a view
rows = df[0:2]
```

### Likely Copy

```python
# Boolean indexing - usually a copy
subset = df[df['A'] > 1]

# Multiple column selection - usually a copy
cols = df[['A', 'B']]

# Chained indexing - definitely problematic
result = df[df['A'] > 1]['B']
```

## The Danger: Silent Bugs

### Bug Example 1: Modification Doesn't Persist

```python
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# This might not work as expected
subset = df[df['A'] > 1]
subset['B'] = 0  # Modifying a copy

print(df)  # df might be unchanged
```

### Bug Example 2: Unintended Modification

```python
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# Get a "view"
col = df['A']

# Modify through the view
col[0] = 999  # This might change df!

print(df)  # df might be changed
```

## The Solution: Be Explicit

### Rule 1: Use .copy() When You Want Independence

```python
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# Explicit copy - safe to modify
subset = df[df['A'] > 1].copy()
subset['B'] = 0

print(df)  # Definitely unchanged
print(subset)  # Has your changes
```

### Rule 2: Use .loc for Direct Modification

```python
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# Direct modification - guaranteed to work
df.loc[df['A'] > 1, 'B'] = 0

print(df)  # Definitely modified
```

## SettingWithCopyWarning

pandas tries to warn you about ambiguous situations:

```python
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

subset = df[df['A'] > 1]
subset['B'] = 0  # SettingWithCopyWarning!
```

```
SettingWithCopyWarning: 
A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead
```

**Never ignore this warning!**

## Safe Patterns

### Pattern 1: Filter and Modify (Using .loc)

```python
# WRONG
df[df['A'] > 1]['B'] = 0

# RIGHT
df.loc[df['A'] > 1, 'B'] = 0
```

### Pattern 2: Create Modified Subset

```python
# WRONG
subset = df[df['A'] > 1]
subset['new_col'] = subset['B'] * 2

# RIGHT
subset = df[df['A'] > 1].copy()
subset['new_col'] = subset['B'] * 2
```

### Pattern 3: Process and Return

```python
def process_data(df):
    # WRONG - might modify original
    result = df[df['A'] > 1]
    result['processed'] = True
    return result
    
    # RIGHT - explicit copy
    result = df[df['A'] > 1].copy()
    result['processed'] = True
    return result
```

### Pattern 4: Chain Operations Safely

```python
# Using method chaining (creates copies automatically)
result = (df
    .query('A > 1')
    .assign(B_doubled=lambda x: x['B'] * 2)
    .sort_values('B_doubled')
)
```

## Checking If It's a View

```python
# Check if two arrays share memory
def shares_memory(a, b):
    return np.shares_memory(a.values, b.values)

df = pd.DataFrame({'A': [1, 2, 3]})
col = df['A']

print(shares_memory(df, col))  # Might be True
```

## Copy-on-Write (pandas 2.0+)

pandas 2.0 introduced Copy-on-Write (CoW) mode:

```python
pd.options.mode.copy_on_write = True

df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
subset = df[df['A'] > 1]

# With CoW, this creates a copy automatically when needed
subset['B'] = 0

print(df)  # Original unchanged
```

## Summary: Golden Rules

| Situation | Safe Pattern |
|-----------|--------------|
| Modify subset | `df.loc[condition, col] = value` |
| Create independent subset | `df[condition].copy()` |
| Add column to subset | `subset = df[...].copy(); subset['new'] = ...` |
| Function that modifies | `def f(df): df = df.copy(); ...` |
| Chained operations | Method chaining with `.assign()` |

**When in doubt, use `.copy()`!**


---

## Exercises

**Exercise 1.** Write code that demonstrates the difference between a view and a copy when slicing a DataFrame.

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

**Exercise 2.** Explain when `df[['col']]` returns a copy vs when `df['col']` returns a view. How can you tell?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Write code using `.copy()` to explicitly create a copy and avoid the `SettingWithCopyWarning`.

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

**Exercise 4.** Explain the Copy-on-Write (CoW) behavior introduced in newer versions of Pandas. How does it change the view/copy semantics?

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
