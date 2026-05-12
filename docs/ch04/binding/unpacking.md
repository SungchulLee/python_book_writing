# Unpacking and Destructuring

Python provides powerful syntax for extracting values from sequences and assigning them to multiple variables.

!!! tip "Mental Model"
    Unpacking is just parallel assignment: Python iterates through the right-hand side and binds each element to the corresponding name on the left. The star (`*`) operator acts like a catch-all bucket that collects whatever the named targets don't claim.

## Basic Unpacking

### Tuple Unpacking

```python
point = (10, 20)
x, y = point

print(x, y)  # 10 20
```

### List Unpacking

```python
data = [1, 2, 3]
a, b, c = data

print(a, b, c)  # 1 2 3
```

### String Unpacking

```python
chars = "ABC"
a, b, c = chars

print(a, b, c)  # A B C
```

## Star Unpacking (Extended Unpacking)

### Collect Remaining Elements

```python
first, *rest = [1, 2, 3, 4, 5]
print(first)  # 1
print(rest)   # [2, 3, 4, 5]
```

### First and Last

```python
first, *middle, last = [1, 2, 3, 4, 5]
print(first)   # 1
print(middle)  # [2, 3, 4]
print(last)    # 5
```

### Ignore with Underscore

```python
first, *_, last = range(10)
print(first, last)  # 0 9
```

### Head and Tail Pattern

```python
head, *tail = [1, 2, 3, 4, 5]
# head = 1
# tail = [2, 3, 4, 5]
```

## Nested Unpacking

### Nested Tuples

```python
data = [(1, 2), (3, 4)]
(a, b), (c, d) = data

print(a, b, c, d)  # 1 2 3 4
```

### Mixed Structures

```python
data = (1, [2, 3], 4)
a, [b, c], d = data

print(a, b, c, d)  # 1 2 3 4
```

### Deep Nesting

```python
data = [(1, 2), (3, 4), (5, 6)]
(a, b), (c, d), (e, f) = data

print(a, b, c, d, e, f)  # 1 2 3 4 5 6
```

---

## Destructuring Patterns

### Function Return Values

```python
def get_coords():
    return 10, 20, 30

x, y, z = get_coords()
print(x, y, z)  # 10 20 30
```

### Ignore Unwanted Values

```python
def stats():
    return 100, 50, 75  # mean, min, max

mean, _, _ = stats()  # Only want mean
print(mean)  # 100
```

### Dictionary Access

```python
person = {'name': 'Alice', 'age': 30}

# Extract specific values
name, age = person['name'], person['age']

# Or use .values() if order is guaranteed (Python 3.7+)
name, age = person.values()
```

### Loop Destructuring

```python
points = [(1, 2), (3, 4), (5, 6)]

for x, y in points:
    print(f"x={x}, y={y}")
```

### Enumerate Destructuring

```python
items = ['a', 'b', 'c']

for i, item in enumerate(items):
    print(f"{i}: {item}")
```

### Dictionary Items

```python
person = {'name': 'Alice', 'age': 30}

for key, value in person.items():
    print(f"{key}: {value}")
```

---

## Dictionary Unpacking

### Function Arguments

```python
def func(a, b, c):
    return a + b + c

data = {'a': 1, 'b': 2, 'c': 3}
result = func(**data)  # Unpack dict as keyword args
print(result)  # 6
```

### Merging Dictionaries

```python
dict1 = {'a': 1, 'b': 2}
dict2 = {'c': 3, 'd': 4}

merged = {**dict1, **dict2}
print(merged)  # {'a': 1, 'b': 2, 'c': 3, 'd': 4}
```

---

## Walrus Operator (`:=`)

The walrus operator (Python 3.8+) assigns a value and returns it in a single expression.

### Basic Syntax

```python
# := assigns AND returns value
if (n := len(data)) > 10:
    print(f"Long list: {n} items")
```

### Avoiding Repeated Computation

```python
# Before (computes len twice)
data = input()
if len(data) > 5:
    print(f"Long: {len(data)}")

# After (computes once)
if (n := len(data)) > 5:
    print(f"Long: {n}")
```

### While Loops

```python
# Read until empty
while (line := input("Enter: ")) != "":
    print(f"You entered: {line}")
```

### List Comprehensions

```python
# Reuse computed value
results = [y for x in data if (y := expensive(x)) > 0]
```

### Pattern Matching

```python
import re

if (match := re.search(r'\d+', text)):
    print(f"Found number: {match.group()}")
```

### If-Elif Chains

```python
if (match := pattern1.search(text)):
    handle_pattern1(match)
elif (match := pattern2.search(text)):
    handle_pattern2(match)
else:
    handle_no_match()
```

---

## Summary

| Pattern | Syntax | Example |
|---------|--------|---------|
| Basic unpacking | `a, b = iterable` | `x, y = (1, 2)` |
| Star unpacking | `first, *rest = iterable` | `head, *tail = [1,2,3]` |
| Nested | `(a, b), (c, d) = nested` | `(x, y), z = ((1,2), 3)` |
| Ignore values | `a, _, c = iterable` | `first, *_, last = data` |
| Dict unpacking | `**dict` | `func(**kwargs)` |
| Walrus | `(name := expr)` | `if (n := len(x)) > 0:` |

Key points:

- Use unpacking to extract values cleanly
- `*` collects remaining elements into a list
- `_` is convention for ignored values
- Walrus operator combines assignment and expression
- Works in loops, comprehensions, and conditions

## Exercises

**Exercise 1.**
Predict the output of each unpacking:

```python
first, *middle, last = [1, 2, 3, 4, 5]
print(first, middle, last)

a, *b = [1]
print(a, b)

*c, d = [1]
print(c, d)
```

What type is the `*` variable always? What happens when there are not enough elements for the starred variable?

??? success "Solution to Exercise 1"
    Output:

    ```text
    1 [2, 3, 4] 5
    1 []
    [] 1
    ```

    The `*` variable is always a **list**, even if it captures zero elements. This is guaranteed by the language -- it never produces a tuple or other type.

    - `first, *middle, last`: `first` gets `1`, `last` gets `5`, `*middle` gets everything in between as `[2, 3, 4]`.
    - `a, *b = [1]`: `a` gets `1`, `*b` gets the remaining (nothing) as `[]`.
    - `*c, d = [1]`: `d` gets `1` (the last element), `*c` gets the remaining (nothing) as `[]`.

    If there are not enough elements for the non-starred variables, Python raises `ValueError`. For example, `a, b, *c = [1]` would fail because `a` and `b` need at least two elements.

---

**Exercise 2.**
Python's swap idiom `a, b = b, a` works without a temporary variable. Explain *why* this works by describing the evaluation order. What would happen in a language that evaluates assignments left-to-right?

??? success "Solution to Exercise 2"
    `a, b = b, a` works because Python evaluates the **entire right-hand side** before performing any binding:

    1. Evaluate `b` -> gets current value of `b`
    2. Evaluate `a` -> gets current value of `a`
    3. Pack into tuple: `(old_b, old_a)`
    4. Unpack and bind: `a = old_b`, `b = old_a`

    The old values are captured in step 1-2 before any reassignment happens in step 4.

    In a language with left-to-right assignment (pseudocode: `a = b; b = a`), the swap would fail: after `a = b`, `a` already holds `b`'s value, so `b = a` assigns `b`'s own old value back to itself. You would need a temporary variable: `temp = a; a = b; b = temp`.

    Python's "evaluate RHS completely first" rule makes multi-target assignment and swaps work correctly without temporaries.

---

**Exercise 3.**
Nested unpacking lets you destructure complex structures in one step:

```python
data = ("Alice", (95, 87, 92))
name, (score1, score2, score3) = data
print(name, score1, score2, score3)
```

Predict the output. Then explain what would happen if the structure does not match -- for example, if `data = ("Alice", (95, 87))` (only two scores instead of three).

??? success "Solution to Exercise 3"
    Output: `Alice 95 87 92`

    Nested unpacking matches the **structure** of the right-hand side. The outer tuple has two elements: a string and a tuple. The inner `(score1, score2, score3)` matches the three-element inner tuple.

    If `data = ("Alice", (95, 87))` (only two scores), Python would raise `ValueError: not enough values to unpack (expected 3, got 2)` because the inner unpacking expects three values but finds only two.

    Unpacking requires the structure to match exactly. The number of targets on each nesting level must equal the number of elements in the corresponding part of the data structure. This strictness catches structural mismatches immediately rather than producing silent errors.
