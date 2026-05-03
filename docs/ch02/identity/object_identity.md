
# Object Identity

Every Python object carries three fundamental properties: a **type**, a **value**, and an **identity**. The first two are familiar -- you already know that `42` has type `int` and value `42`. Identity is the third property, and it answers a different question: not *what* the object is, but *which* object it is.

Think of identity as an object's **address in memory**. Just as every house on a street has a unique address regardless of how similar it looks to its neighbors, every object in a running Python program has a unique identity regardless of its value.

!!! tip "Mental Model"
    Every object has a unique identity -- a numeric label returned by `id()` -- that stays fixed for the object's entire lifetime. Identity tells you *which* object you have, not *what* it contains, and it is the foundation for understanding aliasing, the `is` operator, and how Python manages objects behind the scenes.

---

## 1. The `id()` Function

Python exposes an object's identity through the built-in `id()` function.

```python
x = [1, 2, 3]
print(id(x))
```

Output (the exact number varies per run):

```text
140234866534400
```

In CPython (the standard Python implementation), `id()` returns the object's memory address as an integer. Other implementations may use a different scheme, but the guarantee is the same: no two objects that exist at the same time will share the same `id()`.

```python
a = "hello"
b = [1, 2, 3]
print(id(a))
print(id(b))
```

Output:

```text
140234866122032
140234866534400
```

The two objects have different identities because they are different objects in memory.

---

## 2. Identity is Fixed for an Object's Lifetime

Once an object is created, its identity never changes. This holds for both mutable and immutable objects.

```python
x = [10, 20, 30]
print(id(x))

x.append(40)
print(id(x))
```

Output:

```text
140234866534400
140234866534400
```

The list was mutated (a new element was appended), but the identity remained the same. The object itself did not move -- its contents changed in place.

However, **rebinding** a name to a new object gives a new identity:

```python
x = [10, 20, 30]
print(id(x))

x = [10, 20, 30, 40]
print(id(x))
```

Output:

```text
140234866534400
140234866789568
```

The second assignment creates an entirely new list object. The name `x` now refers to a different object with a different identity, even though the values look related.

---

## 3. Small Integer Caching

CPython pre-creates and caches integer objects in the range **-5 to 256**. Any time your program uses an integer in this range, Python reuses the same object rather than creating a new one.

```python
a = 100
b = 100
print(a is b)
print(id(a) == id(b))
```

Output:

```text
True
True
```

Both `a` and `b` refer to the same cached integer object. Now compare with an integer outside the cached range:

```python
a = 300
b = 300
print(a is b)
```

Output (may vary by context):

```text
False
```

Here, `a` and `b` hold the same value but may be different objects. This is an **implementation detail** of CPython, not a language guarantee. You should never rely on identity comparisons for integers.

The caching range and its boundaries:

| Range     | Cached? | `a is b` reliable? |
| --------- | ------- | ------------------- |
| -5 to 256 | Yes     | Always `True`       |
| < -5      | No      | Unpredictable       |
| > 256     | No      | Unpredictable       |

---

## 4. String Interning

Python also caches certain strings, a process called **interning**. Strings that look like valid identifiers (composed of letters, digits, and underscores) are often interned automatically.

```python
a = "hello"
b = "hello"
print(a is b)
```

Output:

```text
True
```

But strings with spaces or special characters may not be interned:

```python
a = "hello world"
b = "hello world"
print(a is b)
```

Output (may vary):

```text
False
```

You can explicitly intern a string using `sys.intern()`:

```python
import sys

a = sys.intern("hello world")
b = sys.intern("hello world")
print(a is b)
```

Output:

```text
True
```

Like integer caching, string interning is an optimization detail. It exists to save memory and speed up comparisons, but code correctness should never depend on it.

---

## 5. Why Identity Matters

Identity becomes important in several contexts:

- **Detecting aliasing**: two names pointing to the same object (covered in the next topic).
- **Checking for `None`**: `x is None` is the correct idiom because `None` is a singleton -- there is exactly one `None` object, and identity is the right test.
- **Understanding mutation**: if two names share the same identity, mutating through one name affects the other.

```python
x = None
print(x is None)
print(id(x) == id(None))
```

Output:

```text
True
True
```

---

## 6. Summary

Key ideas:

- Every Python object has a unique identity, accessible via `id()`.
- In CPython, `id()` returns the object's memory address.
- Identity is assigned at creation and never changes during the object's lifetime.
- Rebinding a name to a new object gives a new identity; mutating an existing object does not.
- CPython caches small integers (-5 to 256) and certain strings, causing some objects with equal values to share identity.
- These caching behaviors are implementation details -- never rely on them for program correctness.


## Exercises

**Exercise 1.**
Predict the output of the following code. Explain each result in terms of object identity and integer caching.

```python
a = 256
b = 256
print(a is b)

c = 257
d = 257
print(c is d)

e = -5
f = -5
print(e is f)

g = -6
h = -6
print(g is h)
```

??? success "Solution to Exercise 1"
    ```text
    True
    False  (or True, depending on context)
    True
    False  (or True, depending on context)
    ```

    `a is b` is `True` because `256` falls within CPython's cached integer range (-5 to 256). Both `a` and `b` refer to the same pre-created object.

    `c is d` may be `False` in the interactive interpreter because `257` is outside the cached range, so Python may create two separate objects. However, in a script file, the compiler may optimize and reuse the object within the same code block, making it `True`. This inconsistency is precisely why you should never use `is` to compare integers.

    `e is f` is `True` because `-5` is the lower boundary of the cached range.

    `g is h` follows the same logic as `c is d` -- `-6` is outside the cached range, so the result is context-dependent.

    The key lesson: `is` tests identity (same object), not equality (same value). Use `==` for value comparisons.

---

**Exercise 2.**
A student claims that "appending to a list creates a new list object." Design an experiment using `id()` to prove this claim wrong. Then show an operation on a list that *does* create a new object.

??? success "Solution to Exercise 2"
    Disproving the claim -- `append` mutates in place:

    ```python
    original = [1, 2, 3]
    original_id = id(original)

    original.append(4)
    print(id(original) == original_id)  # True
    print(original)                      # [1, 2, 3, 4]
    ```

    The identity is unchanged after `append`. The list object was modified in place, not replaced.

    An operation that creates a new object -- concatenation with `+`:

    ```python
    original = [1, 2, 3]
    original_id = id(original)

    new_list = original + [4]
    print(id(new_list) == original_id)  # False
    print(new_list)                      # [1, 2, 3, 4]
    ```

    The `+` operator creates a brand-new list object. The original list is untouched, and `new_list` has a different identity.

    Other operations that create new objects: slicing (`original[:]`), `sorted(original)`, and list comprehensions (`[x for x in original]`). Operations that mutate in place: `append`, `extend`, `insert`, `sort`, `reverse`.

---

**Exercise 3.**
Explain the difference between the following two code snippets. Use `id()` to verify your explanation.

Snippet A:

```python
x = "hello"
y = "hello"
```

Snippet B:

```python
x = "hello world!"
y = "hello world!"
```

Under what circumstances would `x is y` be `True` in each snippet? What does this tell you about relying on `is` for string comparisons?

??? success "Solution to Exercise 3"
    In Snippet A, `x is y` is almost always `True`:

    ```python
    x = "hello"
    y = "hello"
    print(x is y)   # True
    print(id(x), id(y))  # Same id
    ```

    The string `"hello"` looks like a valid Python identifier (only letters, no spaces or special characters), so CPython interns it automatically. Both `x` and `y` refer to the same cached string object.

    In Snippet B, `x is y` may be `True` or `False` depending on context:

    ```python
    x = "hello world!"
    y = "hello world!"
    print(x is y)  # May be True or False
    ```

    The string `"hello world!"` contains a space and an exclamation mark, so CPython does not automatically intern it. In the interactive interpreter, Python may create two separate objects (`False`). In a script, the compiler may optimize string literals within the same code block and reuse the object (`True`).

    The lesson: **never use `is` to compare strings**. Always use `==` for value comparison. String interning is an optimization that varies by implementation, Python version, and execution context. Code that depends on `is` for strings is fragile and unreliable.
