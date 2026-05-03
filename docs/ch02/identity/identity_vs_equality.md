
# Identity vs Equality

Python has two ways to ask whether things are "the same," and they answer fundamentally different questions. Confusing them is a common source of subtle bugs. Before looking at syntax, build this mental model:

- **Identity** asks: "Are these the **same object** in memory?"
- **Equality** asks: "Do these objects have the **same value**?"

Two identical twins might look the same (equal) but they are still two different people (different identity). Conversely, the same person seen from two different angles is both equal to and identical with themselves.

!!! tip "Mental Model"
    Equality (`==`) asks whether two objects carry the same value; identity (`is`) asks whether they are literally the same object in memory. Two objects can be equal without being identical, but every object is always both equal to and identical with itself.

---

## 1. The `is` Operator

The `is` operator tests **identity**. It returns `True` if and only if the two operands refer to the exact same object in memory.

```python
a = [1, 2, 3]
b = a

print(a is b)
print(a is not b)
```

Output:

```text
True
False
```

Because `b = a` creates an alias, both names refer to the same object. The `is` check confirms this.

```python
a = [1, 2, 3]
b = [1, 2, 3]

print(a is b)
```

Output:

```text
False
```

Even though `a` and `b` contain the same values, they are two separate list objects created independently. They are equal but not identical.

Under the hood, `a is b` is equivalent to `id(a) == id(b)`.

---

## 2. The `==` Operator

The `==` operator tests **equality**. It returns `True` if the two objects have the same value, as determined by the object's `__eq__` method.

```python
a = [1, 2, 3]
b = [1, 2, 3]

print(a == b)
print(a is b)
```

Output:

```text
True
False
```

The lists are equal (same contents) but not identical (different objects). This is the common case: most of the time you care about values, not identity.

---

## 3. When to Use Each

The rule is simple:

| Test | Operator | Use when |
| ---- | -------- | -------- |
| Identity | `is` | Checking for singletons (`None`, `True`, `False`) |
| Equality | `==` | Comparing values (almost everything else) |

In practice, `==` is the default choice. Use `is` only in specific situations where you need to know whether two names point to the exact same object.

### Correct uses of `is`

```python
# Checking for None
x = None
if x is None:
    print("No value assigned")

# Checking for True/False (rare, but sometimes needed)
result = True
if result is True:
    print("Exactly True, not just truthy")
```

### Incorrect uses of `is`

```python
# Do not use 'is' for numbers
a = 1000
b = 1000
if a is b:       # Unreliable!
    print("Same")

# Do not use 'is' for strings
name = "hello"
if name is "hello":  # Unreliable!
    print("Match")

# Use == instead
if a == b:
    print("Same value")
if name == "hello":
    print("Match")
```

---

## 4. None Checks with `is`

`None` is a **singleton** -- there is exactly one `None` object in the entire Python runtime. This makes `is` the correct operator for `None` checks:

```python
def find(items, target):
    for item in items:
        if item == target:
            return item
    return None

result = find([1, 2, 3], 99)

if result is None:
    print("Not found")
```

Output:

```text
Not found
```

Why not use `==`? Because `==` calls `__eq__`, which can be overridden by any class:

```python
class AlwaysEqual:
    def __eq__(self, other):
        return True

obj = AlwaysEqual()
print(obj == None)
print(obj is None)
```

Output:

```text
True
False
```

The object falsely claims to be equal to `None` via its custom `__eq__`. The `is` check correctly reports that it is not `None`. This is why PEP 8 mandates `is None` and `is not None`.

---

## 5. Why `is` with Integers Can Be Misleading

CPython caches small integers in the range -5 to 256. Within this range, `is` appears to work for value comparison:

```python
a = 100
b = 100
print(a is b)
print(a == b)
```

Output:

```text
True
True
```

This gives a false sense of reliability. Outside the cached range, the behavior changes:

```python
a = 300
b = 300
print(a is b)
print(a == b)
```

Output (in interactive interpreter):

```text
False
True
```

The values are equal, but the objects are different. Code that uses `is` for integer comparison works for small numbers (by coincidence) and fails for large numbers (by design). This is a trap because it passes tests with small values and breaks in production with real data.

The same issue applies to other cached or interned objects (strings, small tuples). The caching is an implementation optimization, not a language guarantee.

---

## 6. The `__eq__` Method

The `==` operator is implemented by the `__eq__` special method. Every class can define its own notion of equality:

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

p1 = Point(3, 4)
p2 = Point(3, 4)

print(p1 == p2)
print(p1 is p2)
```

Output:

```text
True
False
```

The two `Point` objects are equal (same coordinates) but not identical (different objects).

### Default `__eq__`

If a class does not define `__eq__`, it inherits the default from `object`, which behaves like `is`:

```python
class Thing:
    pass

a = Thing()
b = Thing()

print(a == b)
print(a is b)
```

Output:

```text
False
False
```

Without a custom `__eq__`, two instances are considered equal only if they are the same object. This default is safe but often not what you want for value-oriented classes.

### Returning `NotImplemented`

When `__eq__` receives an argument it does not know how to compare, it should return `NotImplemented` (not `False`). This tells Python to try the other operand's `__eq__`:

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    def __eq__(self, other):
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.celsius == other.celsius

t = Temperature(100)
print(t == 100)
print(t == Temperature(100))
```

Output:

```text
False
True
```

The comparison `t == 100` first tries `Temperature.__eq__(t, 100)`, which returns `NotImplemented`. Python then tries `int.__eq__(100, t)`, which also returns `NotImplemented`. Since neither side can handle the comparison, Python defaults to `False`.

---

## 7. Summary

Key ideas:

- `is` tests identity (same object in memory); `==` tests equality (same value).
- Use `is` for singletons: `None`, `True`, `False`.
- Use `==` for everything else: numbers, strings, collections, custom objects.
- `None` checks must use `is` because `==` can be overridden by custom `__eq__` methods.
- Integer caching makes `is` appear to work for small numbers, but this is an unreliable implementation detail.
- Classes define equality through `__eq__`. Without it, the default is identity comparison.
- Return `NotImplemented` from `__eq__` when the comparison type is unsupported.


## Exercises

**Exercise 1.**
Predict the output of the following code. For each comparison, state whether it tests identity or equality and explain why the result is what it is.

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)
print(a is b)
print(a == c)
print(a is c)
print(b == c)
print(b is c)
```

??? success "Solution to Exercise 1"
    ```text
    True
    False
    True
    True
    True
    False
    ```

    - `a == b` is `True`: equality test. Both lists contain `[1, 2, 3]`, so their values are equal.
    - `a is b` is `False`: identity test. `a` and `b` were created by separate list literals, so they are different objects in memory.
    - `a == c` is `True`: equality test. Since `c` is an alias of `a`, they refer to the same object, which is trivially equal to itself.
    - `a is c` is `True`: identity test. `c = a` made `c` an alias. They are the same object.
    - `b == c` is `True`: equality test. `b` is `[1, 2, 3]` and `c` (alias of `a`) is `[1, 2, 3]`. Same values.
    - `b is c` is `False`: identity test. `b` is a separate object from `a`/`c`.

    The pattern: `==` compares contents; `is` compares memory addresses. Two objects can be equal without being identical.

---

**Exercise 2.**
Write a class `Fraction` that represents a simple fraction with a numerator and denominator. Implement `__eq__` so that two fractions are considered equal if they represent the same mathematical value (e.g., `Fraction(1, 2)` should equal `Fraction(2, 4)`). Demonstrate that two equal `Fraction` objects are not identical.

??? success "Solution to Exercise 2"
    ```python
    from math import gcd

    class Fraction:
        def __init__(self, numerator, denominator):
            if denominator == 0:
                raise ValueError("Denominator cannot be zero")
            # Normalize sign: keep denominator positive
            if denominator < 0:
                numerator = -numerator
                denominator = -denominator
            # Reduce to lowest terms
            common = gcd(abs(numerator), denominator)
            self.numerator = numerator // common
            self.denominator = denominator // common

        def __eq__(self, other):
            if not isinstance(other, Fraction):
                return NotImplemented
            return (self.numerator == other.numerator and
                    self.denominator == other.denominator)

        def __repr__(self):
            return f"Fraction({self.numerator}, {self.denominator})"

    f1 = Fraction(1, 2)
    f2 = Fraction(2, 4)
    f3 = Fraction(3, 4)

    print(f1 == f2)    # True -- same mathematical value
    print(f1 is f2)    # False -- different objects
    print(f1 == f3)    # False -- different values
    ```

    Output:

    ```text
    True
    False
    False
    ```

    The `__eq__` method reduces both fractions to lowest terms during initialization, then compares numerators and denominators. `Fraction(1, 2)` and `Fraction(2, 4)` both reduce to `1/2`, so they are equal. But they are distinct objects created by separate constructor calls, so `is` returns `False`.

    Returning `NotImplemented` when `other` is not a `Fraction` ensures that comparisons like `Fraction(1, 2) == 0.5` do not incorrectly return `False` by accident -- Python will attempt the reverse comparison via `float.__eq__`, which also returns `NotImplemented`, producing a final result of `False` through the standard protocol.

---

**Exercise 3.**
Explain why the following function has a subtle bug. What happens when the cache stores a result of `None`? Fix the function.

```python
_cache = {}

def expensive_lookup(key):
    result = _cache.get(key)
    if result == None:
        result = perform_database_query(key)
        _cache[key] = result
    return result
```

??? success "Solution to Exercise 3"
    The bug is using `== None` instead of `is None`.

    The `dict.get()` method returns `None` when the key is not found. The intent is to detect this missing-key case and perform the database query. However, `== None` has two problems:

    1. **Cached `None` values are ignored.** If `perform_database_query(key)` legitimately returns `None` (e.g., the record does not exist), that `None` is stored in the cache. On the next lookup, `result` is `None` (from the cache), and `result == None` is `True`, so the function queries the database again. The cache is useless for `None` results.

    2. **Custom `__eq__` can mislead.** If the cached value is an object whose `__eq__` method returns `True` when compared to `None`, the function will incorrectly re-query the database.

    The fix uses `is None` and a sentinel to distinguish "key not in cache" from "key maps to None":

    ```python
    _cache = {}
    _MISSING = object()  # unique sentinel

    def expensive_lookup(key):
        result = _cache.get(key, _MISSING)
        if result is _MISSING:
            result = perform_database_query(key)
            _cache[key] = result
        return result
    ```

    The sentinel `_MISSING` is a unique object that can never appear as a real cached value. Using `is` for the check is both correct and safe: it tests identity against the sentinel, which cannot be faked by a custom `__eq__`.

    This pattern -- using a sentinel with `is` -- is standard practice in Python for distinguishing "absent" from "present but None."
