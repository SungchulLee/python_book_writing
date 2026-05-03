# Integer Caching

!!! tip "Mental Model"
    CPython pre-allocates integer objects for -5 through 256 at startup, so every use of `42` points to the same object. Outside this range, each expression creates a fresh object. This is a performance shortcut, not a language rule -- always compare integers with `==`, never `is`.

## CPython Behavior

### 1. Small Integers

CPython caches [-5, 256]:

```python
# Cached range
a = 100
b = 100
print(a is b)           # True
print(id(a) == id(b))   # True
```

### 2. Outside Range

```python
# Not cached
x = 1000
y = 1000
print(x is y)           # Usually False
print(x == y)           # True
```

## Why Cache

### 1. Performance

```python
# Without caching:
# Every loop creates new objects
for i in range(100):
    total += i          # 100 objects

# With caching:
# Reuses same 100 objects
```

### 2. Memory

```python
# Without caching
numbers = [1, 2, 3, 1, 2, 3]
# 6 separate objects

# With caching
# Only 3 objects shared
```

## Best Practices

### 1. Never Rely On

```python
# Bad: assumes caching
def bad(x):
    if x is 42:         # Don't!
        return True

# Good: use ==
def good(x):
    if x == 42:         # Correct
        return True
```

### 2. Singletons Only

```python
# Use 'is' only for:
if x is None:           # OK
    pass

if x is True:           # OK
    pass

# Not for integers:
# if x is 0:            # Bad!
```

## Summary

### 1. CPython

- Caches [-5, 256]
- Automatic optimization
- Not part of language spec

### 2. Write Portable

```python
# Always use ==
if count == 0:
    pass

# Only is for singletons
if result is None:
    pass
```

---

## Exercises

**Exercise 1.**
Integer caching behavior depends on context in CPython. Predict the output:

```python
a = 256
b = 256
print(a is b)

c = 257
d = 257
print(c is d)

e, f = 1000, 1000
print(e is f)
```

Why might `e is f` return `True` even though `1000` is outside the cached range? What compile-time optimization can cause this?

??? success "Solution to Exercise 1"
    Output (CPython):

    ```text
    True
    False
    True
    ```

    `a is b` is `True` because `256` is within the cached range `[-5, 256]`. `c is d` is `False` because `257` is outside this range, so two separate objects are created.

    `e is f` is likely `True` because CPython's **peephole optimizer** (or AST optimizer) recognizes that `e` and `f` are assigned in the same statement from the same constant. The compiler stores `1000` once in the code object's constant pool, so both names reference the same object. This is a **compile-time** optimization, separate from the runtime small-integer cache.

    This demonstrates why `is` for integers is unreliable: the result depends on compile-time optimizations that vary between Python versions and contexts.

---

**Exercise 2.**
Integer identity can change with how the integer is produced. Predict the output:

```python
a = 100
b = 50 + 50
c = int("100")

print(a is b)
print(a is c)
print(a == b == c)
```

Why is `a is b` likely `True` while `a is c` may or may not be `True`? What does this tell you about the relationship between integer value and object identity?

??? success "Solution to Exercise 2"
    Output (CPython):

    ```text
    True
    True
    True
    ```

    All three are `True` in CPython because `100` is within the cached range `[-5, 256]`. The expression `50 + 50` evaluates to the integer `100`, and the cache ensures the same object is returned. Similarly, `int("100")` produces the cached `100` object.

    However, for values outside the cache range, `a = 500` and `c = int("500")` would likely produce different objects (`a is c` would be `False`). The key lesson: **value equality** (`==`) is always reliable, but **identity** (`is`) depends on whether the implementation happens to reuse objects. Never use `is` for integer comparison.

---

**Exercise 3.**
Caching exists for performance. Predict which is faster and explain why:

```python
import sys

# How much memory does a single int use?
print(sys.getsizeof(0))
print(sys.getsizeof(1))
print(sys.getsizeof(2**30))

# Without caching, this loop would create 100 new int objects per iteration:
total = 0
for i in range(100):
    total += i
```

Why does Python cache small integers but not large ones? What is the trade-off between caching more integers and the memory cost of pre-allocating them?

??? success "Solution to Exercise 3"
    Output (approximate, varies by platform):

    ```text
    28
    28
    32
    ```

    Even a small integer like `0` takes 28 bytes in CPython (object header: reference count + type pointer + value). Larger integers need more space for additional digits.

    Python caches integers `[-5, 256]` because these appear extremely frequently in typical programs (loop counters, indices, return codes, flag values). Pre-allocating 262 integer objects costs about 262 * 28 = ~7 KB, which is negligible. Without caching, a simple `for i in range(100)` would allocate and deallocate 100 integer objects per iteration.

    The trade-off: caching more integers saves allocation time but costs memory upfront. The range `[-5, 256]` was chosen empirically to cover the vast majority of commonly used integers. Caching up to, say, 10,000 would cost ~280 KB with diminishing returns, since larger integers appear less frequently.
