# Identity and Equality

Understanding the difference between `is` (identity) and `==` (equality) operators.

!!! tip "Mental Model"
    `is` asks "are these the same object in memory?" while `==` asks "do these objects have the same value?" Two identical-looking lists can be equal (`==`) yet distinct (`is` returns `False`), just like two copies of the same book are equal in content but physically separate.

## Identity (`is`)

The `is` operator checks if two names refer to the **same object** in memory:

```python
a = [1, 2, 3]
b = a

print(a is b)  # True (same object)
print(id(a) == id(b))  # True (same id)
```

### Different Objects

```python
a = [1, 2, 3]
b = [1, 2, 3]

print(a is b)  # False (different objects)
print(id(a))   # 140234567890
print(id(b))   # 140234567999
```

Even though `a` and `b` have the same values, they are different objects in memory.

## Equality (`==`)

The `==` operator checks if two objects have the **same value**:

```python
a = [1, 2, 3]
b = [1, 2, 3]

print(a == b)  # True (same values)
print(a is b)  # False (different objects)
```

## When to Use Each

### Use `is` for Singletons

```python
# For None
if x is None:
    print("x is None")

if x is not None:
    print("x has a value")

# For True/False (rare, but valid)
if flag is True:
    pass

if flag is False:
    pass
```

### Use `==` for Values

```python
# For comparing values
if x == 42:
    pass

if name == "Alice":
    pass

if items == [1, 2, 3]:
    pass
```

## Common Pitfall: Integer Caching

Python caches small integers (-5 to 256), which can cause confusion:

```python
# Small integers are cached
a = 256
b = 256
print(a is b)  # True (cached)

# Large integers are not
a = 257
b = 257
print(a is b)  # False (different objects)
print(a == b)  # True (same value)
```

**Rule**: Always use `==` for comparing values, even integers.

## String Interning

Similar caching happens with some strings:

```python
a = "hello"
b = "hello"
print(a is b)  # True (interned)

a = "hello world!"
b = "hello world!"
print(a is b)  # May be False
print(a == b)  # True (same value)
```

---

## Special Cases

### Augmented Assignment

Augmented assignment behaves differently based on mutability:

```python
# Mutable: modifies in place
x = [1, 2]
y = x
x += [3, 4]
print(x is y)  # True (same object)

# Immutable: creates new object
x = 10
y = x
x += 5
print(x is y)  # False (different objects)
```

### None Comparison

Always use `is` for `None`:

```python
# Correct
if result is None:
    pass

# Incorrect (works but not recommended)
if result == None:
    pass
```

### Boolean Context

For boolean checks, often no comparison needed:

```python
# Instead of
if flag == True:
    pass

# Prefer
if flag:
    pass

# Instead of
if len(items) == 0:
    pass

# Prefer
if not items:
    pass
```

---

## Summary Table

| Operator | Checks | Use For | Example |
|----------|--------|---------|---------|
| `is` | Identity (same object) | `None`, singletons | `x is None` |
| `==` | Equality (same value) | Values, objects | `x == 42` |
| `is not` | Not same object | `None` check | `x is not None` |
| `!=` | Not same value | Value comparison | `x != 0` |

## Key Takeaways

- `is` checks if two names point to the **same object**
- `==` checks if two objects have the **same value**
- Use `is` for `None`, `True`, `False`
- Use `==` for all value comparisons
- Don't rely on integer/string caching
- Identity implies equality, but not vice versa

## Exercises

**Exercise 1.**
The statement "identity implies equality, but not vice versa" is a fundamental principle. Explain what this means. Then explain the ONE exception in Python: `float('nan')`. Predict the output:

```python
x = float('nan')
print(x == x)
print(x is x)
```

Why is `NaN` the exception to "identity implies equality"?

??? success "Solution to Exercise 1"
    Output:

    ```text
    False
    True
    ```

    "Identity implies equality" means: if `a is b` is `True` (same object), then `a == b` should also be `True` (same value). This makes intuitive sense -- an object should be equal to itself.

    `NaN` violates this: `x is x` is `True` (it is the same object in memory), but `x == x` is `False` (IEEE 754 defines `NaN != NaN`).

    This exception exists because `NaN` represents an **undefined result** -- it is not a number, so it has no meaningful value to compare. The IEEE 754 committee decided that `NaN` should not equal anything, including itself, to prevent undefined results from silently "matching" in equality checks. Python respects this standard, even though it violates the general principle of identity implying equality.

---

**Exercise 2.**
A junior developer writes this helper:

```python
def is_empty(container):
    if container is []:
        return True
    return False
```

This function always returns `False`, even for empty lists. Explain why. What is the correct way to check for an empty container?

??? success "Solution to Exercise 2"
    `container is []` checks whether `container` is the **same object** as a freshly created empty list `[]`. Every time `[]` is written, Python creates a **new** list object. So `container is []` compares `container`'s identity with this brand-new object, which is never the same object as `container` (even if `container` is also an empty list).

    Correct approaches:

    ```python
    # Pythonic: use truthiness
    if not container:
        return True

    # Explicit length check
    if len(container) == 0:
        return True

    # Value comparison (works but less idiomatic)
    if container == []:
        return True
    ```

    The Pythonic way (`if not container`) leverages the fact that empty containers are falsy.

---

**Exercise 3.**
Predict the output and explain:

```python
a = [1, 2, 3]
b = a
c = a[:]

print(a == b, a is b)
print(a == c, a is c)

a.append(4)
print(a == b, a is b)
print(a == c, a is c)
```

How do `==` and `is` behave differently after mutation?

??? success "Solution to Exercise 3"
    Output:

    ```text
    True True
    True False
    True True
    False False
    ```

    Before mutation:

    - `a == b` and `a is b`: `b` is an alias for `a` -- same object, same value. Both `True`.
    - `a == c` and `a is c`: `c` is a copy -- different object, same value. `==` is `True`, `is` is `False`.

    After `a.append(4)`:

    - `a == b` and `a is b`: still the same object. Both are now `[1, 2, 3, 4]`. Both `True`.
    - `a == c` and `a is c`: `a` is `[1, 2, 3, 4]`, `c` is still `[1, 2, 3]`. Different values, different objects. Both `False`.

    This demonstrates: `is` relationships are stable (once aliased, always aliased until rebinding), while `==` relationships can change through mutation.
