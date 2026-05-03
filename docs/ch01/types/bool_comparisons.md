

# bool Comparisons

Comparisons test relationships between values and produce Boolean results.

These results are central to decision making in Python.

Common comparison operators include:

| Operator | Meaning |
|---|---|
| `==` | equal to |
| `!=` | not equal to |
| `<` | less than |
| `>` | greater than |
| `<=` | less than or equal to |
| `>=` | greater than or equal to |

```mermaid
flowchart TD
    A[Two values] --> B[comparison operator]
    B --> C[Boolean result]
````

!!! tip "Mental Model"
    A comparison is a question that always returns `True` or `False`. `==` asks "are these values equal?" while `is` asks "are these the exact same object in memory?" Most of the time you want `==` for value equality. Comparisons are the inputs that drive `if` statements, loops, and every other decision your program makes.

---

## 1. Equality and Inequality

Equality checks whether two values are the same.

```python
print(5 == 5)
print(5 != 3)
```

Output:

```text
True
True
```

These comparisons work across many types.

```python
print("a" == "a")
print([1, 2] == [1, 2])
```

---

## 2. Ordering Comparisons

Ordering operators compare relative size.

```python
print(3 < 5)
print(10 > 7)
print(4 <= 4)
print(8 >= 10)
```

Output:

```text
True
True
True
False
```

These are especially common in loops and conditions.

---

## 3. Chained Comparisons

Python supports chained comparisons.

```python
x = 7
print(0 < x < 10)
```

Output:

```text
True
```

This is equivalent to:

```python
print(0 < x and x < 10)
```

but is often more readable.

---

## 4. Comparing Different Types

Some comparisons between unlike types are allowed, while others are not.

```python
print(3 == 3.0)
```

Output:

```text
True
```

But ordering unrelated types may fail.

```python
# "3" < 4   # TypeError
```

Python does not impose arbitrary ordering across unrelated types.

---

## 5. Identity vs Equality

Python distinguishes equality from identity.

```python
a = [1, 2]
b = [1, 2]

print(a == b)
print(a is b)
```

Output:

```text
True
False
```

* `==` checks whether values are equal
* `is` checks whether two names refer to the same object

This distinction is especially important with `None`.

---

## 6. Membership Comparisons

Python also provides membership tests.

| Operator | Meaning          |
| -------- | ---------------- |
| `in`     | value is present |
| `not in` | value is absent  |

Example:

```python
print("a" in "cat")
print(5 in [1, 2, 5])
```

Output:

```text
True
True
```

---

## 7. Worked Examples

### Example 1: password check

```python
password = "secret"

print(password == "secret")
```

Output:

```text
True
```

### Example 2: numeric range

```python
score = 82

if 80 <= score < 90:
    print("B range")
```

### Example 3: membership

```python
colors = ["red", "green", "blue"]

if "green" in colors:
    print("found")
```

---

## 8. Common Pitfalls

### Using `is` instead of `==`

For value comparison, use `==`, not `is`.

### Comparing unrelated types with ordering operators

Expressions like `"10" < 20` are invalid.

---


## 9. Summary

Key ideas:

* comparisons produce Boolean results
* equality and ordering comparisons are fundamental to control flow
* chained comparisons improve readability
* `==` and `is` have different meanings
* membership tests also produce Boolean values

Comparison operators allow Python programs to reason about relationships between values.


## Exercises

**Exercise 1.**
Python supports chained comparisons like `1 < x < 10`. Predict the output of each expression and explain how Python evaluates them:

```python
print(1 < 2 < 3)
print(1 < 2 > 0)
print(1 < 3 > 2 < 5)
print((1 < 2) < 3)
```

Why does the last expression produce a different result than `1 < 2 < 3`? What hidden operation does Python perform when you write `(1 < 2) < 3`?

??? success "Solution to Exercise 1"
    Output:

    ```text
    True
    True
    True
    True
    ```

    Wait -- the last one requires careful analysis. `1 < 2 < 3` is a chained comparison: Python evaluates it as `1 < 2 and 2 < 3`, which is `True and True` = `True`.

    `1 < 2 > 0` is `1 < 2 and 2 > 0` = `True and True` = `True`.

    `1 < 3 > 2 < 5` is `1 < 3 and 3 > 2 and 2 < 5` = `True and True and True` = `True`.

    `(1 < 2) < 3` is NOT a chained comparison because of the parentheses. `(1 < 2)` evaluates to `True`. Then `True < 3` compares a boolean to an integer. Since `bool` is a subclass of `int` and `True == 1`, this becomes `1 < 3`, which is `True`.

    The difference is subtle: if we had `(1 < 2) < 1`, it would be `True < 1`, which is `1 < 1` = `False`. But the unchained version `1 < 2 < 1` would be `1 < 2 and 2 < 1` = `True and False` = `False`. In this particular case both happen to be `False`, but the mechanism differs.

---

**Exercise 2.**
A programmer checks whether two lists are equal:

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)
print(a is b)
print(a == c)
print(a is c)
```

Predict all four outputs. Then explain: if `a == b` is `True`, why would you ever need `is`? Give the one case where `is` should always be used instead of `==`.

??? success "Solution to Exercise 2"
    Output:

    ```text
    True
    False
    True
    True
    ```

    `a == b` is `True` because both lists contain the same values in the same order -- `==` compares **values**. `a is b` is `False` because `a` and `b` are two separate list objects in memory -- `is` compares **identity** (whether they are the same object).

    `a == c` is `True` (same values) and `a is c` is also `True` because `c = a` makes `c` point to the **same object** as `a`.

    The one case where `is` should always be used: comparing to `None`. Write `if x is None:`, not `if x == None:`. This is because `None` is a **singleton** -- there is exactly one `None` object. Using `is` is both faster (identity check vs value comparison) and safer (a class could define `__eq__` to return `True` when compared with `None`, making `==` unreliable).

---

**Exercise 3.**
Python allows `==` between different types but restricts `<` and `>`. Predict which expressions succeed and which raise errors:

```python
print(3 == 3.0)
print(3 == "3")
print(True == 1)
print(True == 1.0)
print("abc" < "abd")
print([1, 2] < [1, 3])
print(1 < "2")
```

Why does Python allow `3 == 3.0` but forbid `1 < "2"`? What design principle does this reflect?

??? success "Solution to Exercise 3"
    Results:

    ```text
    True       # 3 == 3.0 succeeds: cross-type numeric equality
    False      # 3 == "3" succeeds: different types, not equal
    True       # True == 1 succeeds: bool is subclass of int
    True       # True == 1.0 succeeds: numeric promotion
    True       # string comparison: 'c' < 'd' lexicographically
    True       # list comparison: element-by-element, 2 < 3
    TypeError  # 1 < "2" fails: no ordering between int and str
    ```

    Python allows `3 == 3.0` because equality can always safely return `False` for incompatible types -- if two objects are of unrelated types, they are simply "not equal." No harm done.

    But `1 < "2"` is forbidden because ordering between unrelated types has no meaningful interpretation. Is `1` less than `"2"`? There is no sensible answer. Python 2 allowed this (using arbitrary but consistent type-based ordering), and it was a major source of bugs. Python 3 explicitly rejects meaningless comparisons, following the principle: "Errors should never pass silently."
