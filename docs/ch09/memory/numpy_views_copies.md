# Views vs Copies in NumPy

NumPy's handling of views and copies differs significantly from Python lists and other languages like MATLAB and R. Understanding this is crucial for memory efficiency and avoiding unexpected bugs.

!!! tip "Mental Model"
    A view is a different window into the same memory buffer; a copy is a completely separate buffer. Slicing returns views (cheap, but mutations propagate), while fancy indexing and most dtype conversions return copies (safe, but use extra memory). When in doubt, check `b.base is a` -- if it returns `True`, `b` is a view of `a`.

!!! note "The NumPy Array Model"
    Every NumPy array is three things: a **data buffer** (contiguous block of typed memory), a **shape** (dimensions), and **strides** (byte jumps per axis). A view shares the same data buffer but may have different shape and strides. A copy allocates a new data buffer. Contiguity determines whether a view is possible for a given reshaping.

    Every operation maps onto this model:

    | Operation | What changes | Buffer copied? |
    |-----------|-------------|----------------|
    | **View** (slice, reshape, transpose) | shape and/or strides | No — same buffer |
    | **Copy** (`.copy()`, fancy index, arithmetic) | everything | Yes — new buffer |
    | **Transpose** | swaps strides | No |
    | **Reshape** | reinterprets strides | No (if contiguous) |
    | **Slice** | adjusts offset + strides | No |
    | **ravel** | flattens via strides | No (if contiguous) |

    This single model — buffer + shape + strides — explains everything in this section.

---

## Core Concept

### View Definition

A **view** shares the same underlying data buffer with the original array. Mutations propagate to both.

### Copy Definition

A **copy** allocates new, independent memory. Mutations are isolated from the original.

### Default Behavior

NumPy prefers views for fast computation and efficient memory usage.

---

## The Key Difference

| Operation | Python List | NumPy Array |
|-----------|-------------|-------------|
| Slicing | Returns **copy** | Returns **view** |
| Assignment | Creates alias | Creates alias |

```python
# Python list: slicing creates copy
lst = [1, 2, 3, 4, 5]
lst_slice = lst[1:4]
lst_slice[0] = 99
print(lst)          # [1, 2, 3, 4, 5] (unchanged)

# NumPy: slicing creates view
import numpy as np
arr = np.array([1, 2, 3, 4, 5])
arr_slice = arr[1:4]
arr_slice[0] = 99
print(arr)          # [ 1 99  3  4  5] (changed!)
```

---

## Visual Comparison

### View Diagram

```
Original Array:  [1, 2, 3, 4, 5]
                      ↑
                 (shared memory)
                      ↓
View:               [2, 3, 4]
```

### Copy Diagram

```
Original Array:  [1, 2, 3, 4, 5]
                 (separate memory)
Copy:               [2, 3, 4]
```

---

## Views: Shared Memory

A **view** shares the same underlying data buffer:

```python
arr = np.array([1, 2, 3, 4, 5])
view = arr[1:4]

print(np.shares_memory(arr, view))  # True
print(view.base is arr)             # True
```

### Operations That Return Views

| Operation | Returns |
|-----------|---------|
| `arr[1:4]` | View |
| `arr[::2]` | View |
| `arr.reshape(2, 3)` | View (usually) |
| `arr.T` | View |
| `arr.ravel()` | View (if contiguous) |
| `arr.view(dtype)` | View |

```python
arr = np.arange(6)
reshaped = arr.reshape(2, 3)
reshaped[0, 0] = 99
print(arr)          # [99  1  2  3  4  5] (affected!)
```

---

## Copies: Independent Memory

A **copy** has its own data buffer:

```python
arr = np.array([1, 2, 3, 4, 5])
copied = arr.copy()

print(np.shares_memory(arr, copied))  # False
print(copied.base)                    # None

copied[0] = 99
print(arr)          # [1 2 3 4 5] (unchanged)
```

### Operations That Return Copies

| Operation | Returns |
|-----------|---------|
| `arr.copy()` | Copy |
| `np.copy(arr)` | Copy |
| `arr.flatten()` | Copy (always) |
| `arr[[0, 2, 4]]` | Copy (fancy indexing) |
| `arr[arr > 2]` | Copy (boolean indexing) |

```python
arr = np.array([1, 2, 3, 4, 5])

# Fancy indexing: copy
fancy = arr[[0, 2, 4]]
fancy[0] = 99
print(arr)          # [1 2 3 4 5] (unchanged)

# Boolean indexing: copy
mask = arr > 2
filtered = arr[mask]
filtered[0] = 99
print(arr)          # [1 2 3 4 5] (unchanged)
```

---

## Checking View vs Copy

```python
arr = np.arange(10)

# Method 1: Check .base attribute
slice_view = arr[2:5]
print(slice_view.base is arr)   # True (view)

fancy_copy = arr[[2, 3, 4]]
print(fancy_copy.base)          # None (copy)

# Method 2: np.shares_memory()
print(np.shares_memory(arr, slice_view))   # True
print(np.shares_memory(arr, fancy_copy))   # False
```

---

## Why Views Exist

Views provide significant performance benefits:

1. **Memory Efficiency**: No data duplication means lower memory consumption
2. **Speed**: Avoiding memory allocation and copying is faster
3. **Large Arrays**: Critical when working with gigabyte-scale datasets
4. **In-place Operations**: Modify subsets directly

```python
# Process large array efficiently
data = np.random.randn(1_000_000)

# View: no memory overhead
subset = data[::100]          # Every 100th element
subset *= 2                   # Modify in-place (affects data!)

# If you need independence:
subset = data[::100].copy()
subset *= 2                   # data unchanged
```

---

## When to Copy

Explicit copies protect data integrity:

1. **Data Preservation**: Copy when you need to preserve the original unchanged
2. **Multi-threaded Code**: Copy to avoid race conditions in parallel processing
3. **Function Returns**: Copy when returning array subsets from functions

---

## Comparison: NumPy vs MATLAB vs R

### Copy-on-Write Semantics

| Language | Default Behavior | Copy Trigger |
|----------|------------------|--------------|
| **NumPy** | View (slicing) | Explicit `.copy()` |
| **MATLAB** | Lazy copy | On modification |
| **R** | Copy-on-modify | On modification |

### MATLAB: Lazy Copy

MATLAB uses **copy-on-write**:

```matlab
% MATLAB
A = [1 2 3 4 5];
B = A;           % No copy yet (shares memory)
B(1) = 99;       % Copy triggered here
% A is [1 2 3 4 5], B is [99 2 3 4 5]
```

### R: Copy-on-Modify

R also uses **copy-on-modify**:

```r
# R
a <- c(1, 2, 3, 4, 5)
b <- a           # No copy yet
b[1] <- 99       # Copy triggered here
# a is [1 2 3 4 5], b is [99 2 3 4 5]
```

### NumPy: Explicit Views

NumPy is **explicit** — views are intentional:

```python
# NumPy
a = np.array([1, 2, 3, 4, 5])
b = a            # Alias (same object)
b[0] = 99        # Modifies a too!
# Both are [99 2 3 4 5]

# To avoid:
b = a.copy()     # Explicit copy
```

---

## Summary Comparison Table

| Scenario | NumPy | MATLAB | R |
|----------|-------|--------|---|
| `b = a` | Alias | Lazy copy | Lazy copy |
| `b = a[1:4]` | **View** | Copy | Copy |
| `b[0] = x` after slice | Modifies `a` | Independent | Independent |
| Explicit copy | `.copy()` | Not needed | Not needed |
| Memory efficiency | High (views) | Medium | Medium |
| Accidental mutation risk | **High** | Low | Low |

---

## Common Pitfalls

### Pitfall 1: Unexpected Modification

```python
def process(arr):
    sub = arr[:5]
    sub[0] = 0      # Modifies original!
    return sub

data = np.arange(10)
result = process(data)
print(data)         # [0 1 2 3 4 5 6 7 8 9] — modified!
```

**Fix**: Copy if you need independence:

```python
def process(arr):
    sub = arr[:5].copy()
    sub[0] = 0
    return sub
```

### Pitfall 2: Stale Views

```python
arr = np.array([1, 2, 3])
view = arr[:]
arr = np.array([4, 5, 6])   # arr now points to new array
print(view)                  # [1 2 3] — still points to old data
```

---

## Best Practices

1. **Be explicit**: Use `.copy()` when you need independence
2. **Check with `np.shares_memory()`** when uncertain
3. **Document intent**: Comment when views are intentional
4. **Defensive copying**: Copy input arrays in functions if modifying

```python
def safe_normalize(arr):
    """Normalize array without modifying original."""
    arr = arr.copy()  # Defensive copy
    arr -= arr.mean()
    arr /= arr.std()
    return arr
```

---

## Quick Reference

| Need | Action |
|------|--------|
| Check if view | `arr.base is not None` or `np.shares_memory(a, b)` |
| Force copy | `arr.copy()` or `np.copy(arr)` |
| Flatten (always copy) | `arr.flatten()` |
| Flatten (view if possible) | `arr.ravel()` |

---

## Key Takeaways

- NumPy slicing returns **views** (unlike Python lists)
- Views share memory — modifications propagate
- Use `.copy()` for independent copies
- Fancy/boolean indexing returns **copies**
- MATLAB and R use copy-on-write; NumPy uses explicit views
- Check with `np.shares_memory()` or `.base` attribute
- Defensive copying in functions prevents accidental mutation

---

## Exercises

**Exercise 1.**
Create `a = np.arange(12).reshape(3, 4)`. Create a view `v = a[1:3, 1:3]` and a copy `c = a[1:3, 1:3].copy()`. Modify both and check which changes propagate back to `a`.

??? success "Solution to Exercise 1"

        import numpy as np

        a = np.arange(12).reshape(3, 4)
        v = a[1:3, 1:3]
        c = a[1:3, 1:3].copy()

        v[0, 0] = 99
        print(f"a after view mod: a[1,1] = {a[1, 1]}")  # 99

        c[0, 0] = 88
        print(f"a after copy mod: a[1,1] = {a[1, 1]}")  # still 99

---

**Exercise 2.**
Write a function that takes an array and returns `True` if it is a view (has a base) and `False` if it owns its data. Test it on a slice, a reshape result, a `.copy()`, and a boolean-indexed result.

??? success "Solution to Exercise 2"

        import numpy as np

        def is_view(arr):
            return arr.base is not None

        a = np.arange(12).reshape(3, 4)
        print(f"Slice: {is_view(a[1:3])}")       # True
        print(f"Reshape: {is_view(a.reshape(4, 3))}") # True
        print(f"Copy: {is_view(a.copy())}")       # False
        print(f"Boolean: {is_view(a[a > 5])}")    # False

---

**Exercise 3.**
Create a large array `a = np.random.randn(10000)`. Create a view `v = a[::2]` and a copy `c = a[::2].copy()`. Compare their `nbytes` and verify that the view shares memory with `a` by checking `np.shares_memory(a, v)`.

??? success "Solution to Exercise 3"

        import numpy as np

        a = np.random.randn(10000)
        v = a[::2]
        c = a[::2].copy()

        print(f"View nbytes: {v.nbytes}")
        print(f"Copy nbytes: {c.nbytes}")
        print(f"Shares memory (view): {np.shares_memory(a, v)}")
        print(f"Shares memory (copy): {np.shares_memory(a, c)}")
