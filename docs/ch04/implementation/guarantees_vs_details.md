# Guarantees vs Details

!!! tip "Mental Model"
    Draw a sharp line between what the language promises (immutability, identity stability, type semantics) and what CPython happens to do (integer caching, reference counting). Write code that depends only on guarantees, and treat everything else as an optimization you observe but never rely on.

## Language Guarantees

### 1. Semantic Behavior

Always guaranteed:

```python
# Assignment creates binding
x = 42

# Identity stable
lst = [1, 2, 3]
original_id = id(lst)
lst.append(4)
# Guaranteed: id(lst) == original_id
```

### 2. Type Behavior

```python
# Immutable behavior
x = "hello"
# x[0] = "H"  # TypeError (guaranteed)

# Mutable behavior  
lst = [1, 2, 3]
lst[0] = 100        # Works (guaranteed)
```

## Implementation Details

### 1. Not Guaranteed

CPython specifics (marked with note):

```python
# Small int caching (CPython)
a = 42
b = 42
# a is b may be True (NOT guaranteed)

# Large ints
x = 1000
y = 1000
# x is y may be False
```

### 2. Memory Layout

```python
# id() returns address in CPython
x = [1, 2, 3]
print(id(x))  # Address (CPython)

# Other implementations may differ
```

## Comparison Table

| Aspect | Guaranteed | Not Guaranteed |
|--------|-----------|----------------|
| Equality check | Yes | - |
| Identity for None | Yes | - |
| Small int identity | No | CPython: True |
| id() = address | No | CPython: Yes |
| String interning | No | CPython: Sometimes |

## Best Practices

### 1. Rely on Guarantees

```python
# Good: language guarantees
if x == y:              # Value comparison
    pass

if x is None:           # Singleton
    pass

# Bad: implementation details
if id(x) < id(y):       # Address comparison
    pass
```

### 2. Portable Code

```python
# Use == for values
if count == 0:
    pass

# Use is only for singletons
if result is None:
    pass
```

## Summary

### 1. Depend On

- Equality (==)
- Identity for None/True/False
- Mutability behavior
- Type semantics

### 2. Don't Depend On

- Small integer caching
- String interning
- id() being address
- Reference counts
- GIL existence

---

## Exercises

**Exercise 1.**
Some behaviors are language guarantees, others are CPython implementation details. For each, state whether it is guaranteed or an implementation detail:

```python
# (a)
x = [1, 2, 3]
x.append(4)
print(id(x) == id(x))  # Same id after mutation?

# (b)
a = 100
b = 100
print(a is b)           # Same object?

# (c)
s = "hello"
# s[0] = "H"            # Would this raise TypeError?

# (d)
print(id(42))           # Is this a memory address?
```

Which of these can you safely rely on in portable Python code?

??? success "Solution to Exercise 1"
    - **(a) Guaranteed.** Mutating a mutable object does not change its identity. `id(x)` is stable across mutations for the lifetime of the object. This is a language guarantee.
    - **(b) Implementation detail.** Small integer caching (`-5` to `256`) is a CPython optimization. Other implementations may not cache these values, so `a is b` could be `False`.
    - **(c) Guaranteed.** String immutability is a language guarantee. `s[0] = "H"` raises `TypeError` in every Python implementation.
    - **(d) Implementation detail.** In CPython, `id()` returns the memory address. In PyPy, it returns an arbitrary unique integer. The language only guarantees that `id()` returns a unique integer for the object's lifetime.

    Safe to rely on: (a) and (c). Fragile: (b) and (d).

---

**Exercise 2.**
The `is` operator should only be used for singletons. Predict which comparisons are safe and which are fragile:

```python
# Safe or fragile?
x = None
print(x is None)

y = 256
print(y is 256)

z = 257
print(z is 257)

w = True
print(w is True)
```

Why is `x is None` safe but `y is 256` fragile, even if both happen to return `True` in CPython?

??? success "Solution to Exercise 2"
    Output in CPython:

    ```text
    True
    True
    True (or False, depends on context)
    True
    ```

    `x is None` is **safe** because `None` is a **singleton** -- the language guarantees there is exactly one `None` object. `is` is the correct way to check for `None`.

    `y is 256` is **fragile** because it relies on CPython's small integer cache. In CPython, integers `-5` to `256` are pre-allocated singletons, so `256 is 256` happens to be `True`. But `257 is 257` may be `True` or `False` depending on context (same code object may or may not constant-fold). In PyPy, the caching range is different.

    `w is True` is **safe** because `True` and `False` are singletons (language guarantee). However, `if w is True` is usually unnecessary -- `if w:` is more Pythonic.

    Rule: use `is` only for `None`, `True`, `False`, and sentinel objects. Use `==` for all value comparisons.

---

**Exercise 3.**
Code that relies on implementation details can break across Python implementations. Predict whether each pattern works in CPython, PyPy, and MicroPython:

```python
import sys

# Pattern A: Reference counting for cleanup
f = open("test.txt", "w")
f.write("data")
del f  # File closed immediately?

# Pattern B: id() for hashing
d = {}
x = [1, 2]
d[id(x)] = "found"

# Pattern C: Small integer caching
a = 5
b = 5
assert a is b
```

Why is Pattern A particularly dangerous? What is the correct alternative?

??? success "Solution to Exercise 3"
    **Pattern A** (reference counting cleanup):
    - CPython: works (file closed immediately on `del` because refcount drops to 0)
    - PyPy: **broken** (PyPy uses a tracing garbage collector, not reference counting; `del` does not guarantee immediate cleanup)
    - The correct alternative: `with open("test.txt", "w") as f: f.write("data")`. Context managers guarantee cleanup regardless of the garbage collection strategy.

    **Pattern B** (id for hashing):
    - Works in all implementations but is **semantically wrong**. After `del x`, a new object could reuse the same `id()`, causing stale lookups. Use the object itself or a proper hash.

    **Pattern C** (small integer caching):
    - CPython: works for `-5` to `256`
    - PyPy: may work with a different range
    - MicroPython: may not cache at all
    - Fragile across implementations. Use `==` instead of `is`.
