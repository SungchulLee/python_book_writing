# Assignment vs Mutation

Understanding the difference between rebinding a name and modifying an object is fundamental to Python.

!!! tip "Mental Model"
    Assignment moves the name tag to a different object; mutation changes the object the tag is already attached to. Check `id()` before and after: if it changed, you rebound; if it stayed the same, you mutated.

---

## Core Difference

### Assignment (Rebinding)

Assignment creates a new binding from a name to an object:

```python
x = [1, 2, 3]
print(id(x))  # 140234567890

x = [4, 5, 6]  # New binding - different object
print(id(x))  # 140234567999 (different!)
```

The original list `[1, 2, 3]` still exists (until garbage collected), but `x` no longer refers to it.

### Mutation (In-Place Modification)

Mutation modifies the object itself:

```python
x = [1, 2, 3]
print(id(x))  # 140234567890

x.append(4)   # Same object, modified
print(id(x))  # 140234567890 (same!)
print(x)      # [1, 2, 3, 4]
```

---

## Visual Comparison

```
Assignment (x = [4, 5, 6]):
    Before: x ──→ [1, 2, 3]
    After:  x ──→ [4, 5, 6]
            (old list orphaned)

Mutation (x.append(4)):
    Before: x ──→ [1, 2, 3]
    After:  x ──→ [1, 2, 3, 4]
            (same list, modified)
```

---

## Immutable Types

Immutable types (int, str, tuple, frozenset) cannot be mutated:

```python
x = "hello"
# x[0] = "H"        # TypeError: strings are immutable

x = "H" + x[1:]     # Must create new string and reassign
print(x)            # "Hello"
```

```python
x = (1, 2, 3)
# x.append(4)       # AttributeError: tuple has no append

x = x + (4,)        # Must create new tuple
print(x)            # (1, 2, 3, 4)
```

---

## Mutable Types

Mutable types (list, dict, set) support both mutation and reassignment:

### Mutation Methods

```python
lst = [1, 2, 3]
lst.append(4)       # [1, 2, 3, 4]
lst.extend([5, 6])  # [1, 2, 3, 4, 5, 6]
lst.insert(0, 0)    # [0, 1, 2, 3, 4, 5, 6]
lst.pop()           # [0, 1, 2, 3, 4, 5]
lst[0] = 99         # [99, 1, 2, 3, 4, 5]
```

### Reassignment

```python
lst = [1, 2, 3]
lst = lst + [4, 5]  # New object created
lst = [4, 5, 6]     # New object created
```

---

## Why It Matters: Aliasing

When two names refer to the same object, mutation affects both:

```python
a = [1, 2, 3]
b = a  # b refers to same object

b.append(4)  # Mutation
print(a)     # [1, 2, 3, 4] - a sees the change!

b = [5, 6, 7]  # Assignment (rebinding)
print(a)       # [1, 2, 3, 4] - a unchanged
```

### Assignment is Safe

```python
a = [1, 2, 3]
b = a
a = [4, 5, 6]   # Rebind a to new object

print(b)        # [1, 2, 3] - b still refers to original
```

### Mutation Affects All References

```python
a = [1, 2, 3]
b = a
a.append(4)     # Mutate the shared object

print(b)        # [1, 2, 3, 4] - b sees the change
```

---

## Augmented Assignment (`+=`, `*=`, etc.)

Augmented assignment behaves differently for mutable vs immutable types:

### Mutable (list) — Mutation

```python
x = [1, 2]
y = x

x += [3, 4]      # Calls x.__iadd__, modifies in place
print(y)         # [1, 2, 3, 4] - y sees change
print(x is y)    # True - same object
```

### Immutable (int, str, tuple) — Rebinding

```python
x = 10
y = x

x += 5           # Creates new int, rebinds x
print(y)         # 10 - y unchanged
print(x is y)    # False - different objects
```

### `+` Always Creates New Object

```python
lst = [1, 2]
original_id = id(lst)

lst = lst + [3, 4]  # Always creates new list
print(id(lst) == original_id)  # False
```

---

## Function Parameters

### Reassignment Inside Function

```python
def reassign(lst):
    lst = [4, 5, 6]  # Rebinds local name only

original = [1, 2, 3]
reassign(original)
print(original)      # [1, 2, 3] - unchanged
```

### Mutation Inside Function

```python
def mutate(lst):
    lst.append(4)    # Modifies the actual object

original = [1, 2, 3]
mutate(original)
print(original)      # [1, 2, 3, 4] - changed!
```

---

## Assignment Examples

### Simple Assignment

```python
x = 42
name = "Alice"
pi = 3.14159
```

### Multiple Assignment (Unpacking)

```python
a, b, c = 1, 2, 3
x, y = "hello", "world"
first, *rest = [1, 2, 3, 4]  # first=1, rest=[2, 3, 4]
```

### Chained Assignment

```python
x = y = z = 0
# All three refer to the same object
print(x is y is z)  # True
```

### Swap Values

```python
a, b = 10, 20
a, b = b, a
print(a, b)  # 20, 10
```

### Index/Slice Assignment

```python
lst = [1, 2, 3, 4, 5]
lst[0] = 10          # Index assignment (mutation)
lst[1:3] = [20, 30]  # Slice assignment (mutation)
```

### Attribute Assignment

```python
class Point:
    pass

p = Point()
p.x = 10  # Assigns to object attribute
p.y = 20
```

---

## Common Patterns

### Initialize Multiple Variables

```python
# Same value (same object for immutables)
x = y = z = 0

# Different values
x, y, z = 0, 0, 0
```

### Conditional Assignment

```python
# Ternary
result = value if condition else default

# Or pattern (for falsy defaults)
name = user_input or "Anonymous"
```

### Increment/Decrement

```python
count = 0
count += 1  # Increment (rebinding for int)
count -= 1  # Decrement (rebinding for int)
```

---

## Quick Reference

| Operation | Mutation? | New Object? | Example |
|-----------|-----------|-------------|---------|
| `x = value` | No | Depends | `x = [1, 2]` |
| `x.append(3)` | Yes | No | List method |
| `x.update({})` | Yes | No | Dict method |
| `x += [3]` (list) | Yes | No | In-place |
| `x += 1` (int) | No | Yes | Rebinding |
| `x = x + [3]` | No | Yes | Always new |

---

## Summary

| Aspect | Assignment | Mutation |
|--------|------------|----------|
| What changes | Name binding | Object contents |
| Object identity | May change | Stays same |
| Other references | Unaffected | See changes |
| Works on | Any type | Mutable types only |

**Key Takeaways**:

- **Assignment** changes what a name refers to
- **Mutation** changes the object itself
- Aliased names share mutations but not reassignments
- Augmented assignment (`+=`) behavior depends on mutability
- Use `id()` to check if you have the same object
- Be careful when passing mutable objects to functions

## Exercises

**Exercise 1.**
Predict the output and trace the object identity at each step:

```python
a = [1, 2, 3]
b = a
print(id(a) == id(b))

a = a + [4]
print(id(a) == id(b))
print(a)
print(b)
```

Now compare with:

```python
a = [1, 2, 3]
b = a
a += [4]
print(id(a) == id(b))
print(a)
print(b)
```

Why does `a = a + [4]` give different aliasing behavior than `a += [4]`?

??? success "Solution to Exercise 1"
    **First version** (`a = a + [4]`):

    ```text
    True
    False
    [1, 2, 3, 4]
    [1, 2, 3]
    ```

    `a + [4]` creates a **new list** object. `a = a + [4]` rebinds `a` to this new list. `b` still refers to the original. Different objects, different ids.

    **Second version** (`a += [4]`):

    ```text
    True
    [1, 2, 3, 4]
    [1, 2, 3, 4]
    ```

    `a += [4]` calls `list.__iadd__`, which **mutates** the existing list in place and returns the same object. `a` and `b` still refer to the same (now modified) list. Same object, same id.

    The difference: `a = a + [4]` always creates a new object (uses `__add__`). `a += [4]` tries `__iadd__` first (in-place if mutable). For mutable types, `+=` is fundamentally different from `= ... +`.

---

**Exercise 2.**
A function receives a list and is supposed to return a sorted version without modifying the original:

```python
def get_sorted(items):
    items.sort()
    return items

original = [3, 1, 2]
result = get_sorted(original)
print(original)
print(result)
print(original is result)
```

Predict the output. Explain why this function is buggy. What is the correct approach -- and why does understanding assignment vs. mutation matter here?

??? success "Solution to Exercise 2"
    Output:

    ```text
    [1, 2, 3]
    [1, 2, 3]
    True
    ```

    `items.sort()` **mutates** the list in place. Since `items` and `original` are aliases for the same list, `original` is modified. `result` is also the same object (`original is result` is `True`).

    The bug: the function was supposed to return a sorted version **without modifying the original**, but `.sort()` mutates in place.

    Correct approach:

    ```python
    def get_sorted(items):
        return sorted(items)  # sorted() creates a NEW list
    ```

    `sorted()` returns a new list, leaving the original unchanged. Understanding mutation vs. new-object creation is essential for writing functions that do not have unintended side effects on their arguments.

---

**Exercise 3.**
Explain why the following code produces different results for integers and lists:

```python
def increment(x):
    x += 1

def append_item(lst):
    lst += [4]

a = 10
increment(a)
print(a)

b = [1, 2, 3]
append_item(b)
print(b)
```

Both functions use `+=`, but the effect on the caller's variable is different. Why?

??? success "Solution to Exercise 3"
    Output:

    ```text
    10
    [1, 2, 3, 4]
    ```

    In `increment`: `x += 1` for an integer calls `int.__iadd__`, but integers are immutable. This creates a new `int` object `11` and rebinds the **local** name `x` to it. The caller's `a` is unaffected because rebinding a local name never affects the caller.

    In `append_item`: `lst += [4]` for a list calls `list.__iadd__`, which **mutates** the list in place. The local name `lst` and the caller's `b` refer to the same list object. The mutation is visible through `b`.

    The crucial difference: `+=` on immutable types **rebinds** (local effect only); `+=` on mutable types **mutates** (visible to all aliases). This asymmetry is one of the most important subtleties in Python's object model.
