# Object Interning

Python optimizes memory usage by reusing identical immutable objects through interning and caching.

!!! tip "Mental Model"
    Interning is a space-time trade-off: instead of creating duplicate immutable objects, Python keeps a single canonical copy and hands out references to it. This makes identity checks (`is`) fast and saves memory, but the rules for when interning happens are CPython-specific and should never be relied upon for correctness.

## String Interning

### Concept

String interning shares identical strings in memory, reducing memory usage and enabling fast identity comparisons.

```python
a = "hello"
b = "hello"
print(a is b)  # True (same object)
print(id(a) == id(b))  # True
```

### Auto-Interning Rules

Python automatically interns strings that look like identifiers:

```python
# Auto-interned (identifier-like)
a = "hello"
b = "hello"
print(a is b)  # True

a = "hello_world"
b = "hello_world"
print(a is b)  # True
```

Strings with spaces or special characters may not be auto-interned:

```python
# May not be interned
a = "hello world!"
b = "hello world!"
print(a is b)  # May be False
print(a == b)  # Always True (same value)
```

### Explicit Interning

Use `sys.intern()` to force interning:

```python
import sys

s1 = sys.intern("any string with spaces!")
s2 = sys.intern("any string with spaces!")
print(s1 is s2)  # True (forced interning)
```

### When to Use Explicit Interning

```python
import sys

# Useful for repeated string comparisons
keys = [sys.intern(key) for key in many_keys]

# Fast identity check instead of value comparison
if key is interned_key:  # Faster than key == interned_key
    pass
```

---

## Integer Caching

### CPython Caching Range

CPython caches small integers in the range **[-5, 256]**:

```python
# Cached integers
a = 100
b = 100
print(a is b)  # True (same cached object)

a = 256
b = 256
print(a is b)  # True (still cached)

# Non-cached integers
a = 257
b = 257
print(a is b)  # May be False (different objects)
print(a == b)  # True (same value)

a = -6
b = -6
print(a is b)  # May be False
```

### Why This Range?

Small integers are used frequently in programs (loop counters, indices, etc.), so caching them:
- Reduces memory usage
- Improves performance
- Avoids repeated object creation

### Important Warning

**Never rely on integer caching for logic!**

```python
# WRONG - Don't do this
if x is 100:  # May not work as expected
    pass

# CORRECT - Always use ==
if x == 100:  # Always works correctly
    pass
```

---

## Other Cached Objects

### Singletons

```python
# None, True, False are singletons
a = None
b = None
print(a is b)  # Always True

a = True
b = True
print(a is b)  # Always True
```

### Empty Immutables

```python
# Empty tuple is cached
a = ()
b = ()
print(a is b)  # True

# Empty frozenset is cached
a = frozenset()
b = frozenset()
print(a is b)  # True
```

---

## Summary

| Type | Interning/Caching | Range/Condition |
|------|-------------------|-----------------|
| Strings | Auto/Explicit | Identifier-like / `sys.intern()` |
| Integers | Auto | [-5, 256] |
| None | Always | Singleton |
| True/False | Always | Singletons |
| Empty tuple | Auto | `()` |

Key points:
- Interning saves memory by sharing objects
- Use `==` for value comparison, `is` for identity
- Don't rely on caching in program logic
- Use `sys.intern()` for explicit string interning
- Caching is an implementation detail, not guaranteed

## Exercises

**Exercise 1.**
Predict the result of each `is` comparison and explain why:

```python
a = 256
b = 256
print(a is b)

c = 257
d = 257
print(c is d)

e = "hello"
f = "hello"
print(e is f)

g = "hello world"
h = "hello world"
print(g is h)
```

Which results are guaranteed by the Python language, and which depend on the CPython implementation?

??? success "Solution to Exercise 1"
    In CPython:

    ```text
    True   (256 is in the interned range [-5, 256])
    True or False  (257 is outside the range; depends on context)
    True   ("hello" is a simple identifier-like string, typically interned)
    True or False  ("hello world" contains a space, may or may not be interned)
    ```

    **None** of these `is` results are guaranteed by the Python language specification. The language only guarantees:

    - `None is None` (singleton)
    - `True is True`, `False is False` (singletons)

    Integer interning in the range [-5, 256] is a CPython implementation detail. String interning for simple identifier-like strings is also CPython-specific. Other implementations (PyPy, Jython, GraalPython) may intern different ranges or use different strategies.

    The only reliable use of `is` is for singletons (`None`, `True`, `False`) and explicitly interned objects. For all other comparisons, use `==`.

---

**Exercise 2.**
A programmer writes tests like this:

```python
result = compute_something()
assert result is True
```

They find that the test passes when `compute_something()` returns `True` but fails when it returns `1` (even though `1 == True`). Explain why `is True` and `== True` differ. When is `is` appropriate for boolean checks, and when should `==` be used instead?

??? success "Solution to Exercise 2"
    `is True` checks **identity**: is this the exact same object as the `True` singleton? `== True` checks **equality**: does this value equal `True`?

    `1 == True` is `True` because `bool` is a subclass of `int`, and `True` has integer value `1`. But `1 is True` is `False` because `1` and `True` are different objects (different types, even though they compare equal).

    Use `is True` or `is False` only when you specifically need to distinguish between `True` and other truthy values (like `1`). In most cases, use the idiomatic truthiness check:

    ```python
    if result:          # Checks truthiness -- usually what you want
    if result == True:  # Checks value equality -- rarely needed
    if result is True:  # Checks identity -- only for "must be exactly True"
    ```

    For `None` checks, always use `is None` (because `None` is a singleton and `==` can be overridden).

---

**Exercise 3.**
Explain why interning is an *optimization* and not a *language feature*. What would break if a programmer wrote code that depended on interning behavior? Give a concrete example of code that works on CPython but might fail on PyPy or a future Python version.

??? success "Solution to Exercise 3"
    Interning is an optimization because it saves memory and speeds up certain operations (identity checks are faster than equality checks). The language specification does not require it -- it only says that integers with the same value must compare equal with `==`.

    Code that depends on interning:

    ```python
    # WRONG: depends on integer interning
    def check_status(code):
        if code is 200:  # Works in CPython for 200 (in [-5, 256])
            return "OK"
        if code is 404:  # FAILS! 404 > 256, not interned
            return "Not Found"
    ```

    This code would work for status code 200 on CPython (200 is in the interned range) but fail for 404. On PyPy (which may intern a different range or no integers at all), even 200 might fail.

    The correct code uses `==`:

    ```python
    def check_status(code):
        if code == 200:
            return "OK"
        if code == 404:
            return "Not Found"
    ```

    The general rule: never rely on implementation-specific optimizations in program logic. Use `==` for values, `is` only for guaranteed singletons.
