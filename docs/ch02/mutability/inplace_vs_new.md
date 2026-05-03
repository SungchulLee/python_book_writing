
# In-Place vs New Object Operations

Python draws a sharp line between two kinds of operations: those that **modify an object in
place** and those that **create and return a new object**. Understanding which category an
operation falls into prevents a class of bugs that silently discard results or accidentally
share state.

The mental model is straightforward. An in-place operation is like editing a document---the
document itself changes, and everyone who has a reference to it sees the update. A new-object
operation is like photocopying a document with edits---the original stays untouched, and you
get a fresh copy.

!!! tip "Mental Model"
    Every operation either changes an existing object or produces a new one -- never both. In-place methods (like `list.sort()`) modify the object and return `None`; constructive functions (like `sorted()`) leave the original alone and hand you a fresh result. Mixing them up leads to "lost result" bugs or unintended shared-state mutations.

---

## 1. In-Place Operations on Lists

Lists are mutable, so many of their methods modify the list directly and return `None`.

```python
nums = [3, 1, 2]
result = nums.sort()

print(nums)
print(result)
```

Output:

```text
[1, 2, 3]
None
```

`sort()` rearranges the list in place. It returns `None` by convention to signal that no new
object was created. The same pattern applies to other mutating list methods.

| Method | Mutates in place | Returns |
| -------------- | ---------------- | ------- |
| `append(x)` | Yes | `None` |
| `extend(iter)` | Yes | `None` |
| `insert(i, x)` | Yes | `None` |
| `remove(x)` | Yes | `None` |
| `sort()` | Yes | `None` |
| `reverse()` | Yes | `None` |
| `clear()` | Yes | `None` |

---

## 2. New-Object Operations

Built-in functions like `sorted()` and operators like `+` do not modify their inputs. They
produce new objects.

```python
nums = [3, 1, 2]
ordered = sorted(nums)

print(nums)
print(ordered)
print(nums is ordered)
```

Output:

```text
[3, 1, 2]
[1, 2, 3]
False
```

`sorted()` returns a **new list**. The original `nums` is unchanged. The `is` check confirms
that `ordered` is a different object.

---

## 3. sort() vs sorted()

This is one of the most common points of confusion for beginners.

| | `list.sort()` | `sorted(iterable)` |
| -------------- | ---------------------- | ---------------------- |
| Modifies input | Yes | No |
| Returns | `None` | New list |
| Works on | Lists only | Any iterable |
| Memory | No extra list created | Creates a new list |

Choose `sort()` when you no longer need the original order and want to save memory. Choose
`sorted()` when you need to preserve the original or when working with non-list iterables.

```python
# sort() modifies in place
data = [5, 2, 8]
data.sort()
print(data)

# sorted() creates a new list
data = [5, 2, 8]
new_data = sorted(data)
print(data)
print(new_data)
```

Output:

```text
[2, 5, 8]
[5, 2, 8]
[2, 5, 8]
```

---

## 4. The None Trap

Because in-place methods return `None`, assigning their result to a variable loses the data.

```python
nums = [3, 1, 2]
nums = nums.sort()

print(nums)
```

Output:

```text
None
```

The list was sorted in place, but then `nums` was rebound to the return value of `sort()`,
which is `None`. The sorted list is lost. This is a frequent bug.

The fix: do not assign the result of an in-place operation.

```python
nums = [3, 1, 2]
nums.sort()

print(nums)
```

Output:

```text
[1, 2, 3]
```

---

## 5. Dictionary In-Place Methods

Dictionaries follow the same convention. Methods that modify the dictionary return `None`.

```python
config = {"host": "localhost"}
result = config.update({"port": 8080})

print(config)
print(result)
```

Output:

```text
{'host': 'localhost', 'port': 8080}
None
```

The `|` operator (Python 3.9+), by contrast, returns a **new** dictionary.

```python
a = {"x": 1}
b = {"y": 2}
c = a | b

print(a)
print(c)
```

Output:

```text
{'x': 1}
{'x': 1, 'y': 2}
```

The in-place counterpart is `|=`, which modifies the left operand.

```python
a = {"x": 1}
a |= {"y": 2}

print(a)
```

Output:

```text
{'x': 1, 'y': 2}
```

---

## 6. String Methods Always Return New Objects

Strings are immutable, so every string method returns a new string. The original is never
modified.

```python
name = "alice"
upper_name = name.upper()

print(name)
print(upper_name)
```

Output:

```text
alice
ALICE
```

This makes string methods safe to chain because each step produces a new string.

```python
result = "  Hello, World!  ".strip().lower().replace(",", "")
print(result)
```

Output:

```text
hello world!
```

---

## 7. Chaining and the None Problem

Because in-place methods return `None`, they **cannot** be chained.

```python
# This does NOT work
nums = [3, 1, 2]
result = nums.sort().reverse()
```

Output:

```text
AttributeError: 'NoneType' object has no attribute 'reverse'
```

`nums.sort()` returns `None`, and calling `.reverse()` on `None` fails. To apply multiple
in-place operations, use separate statements.

```python
nums = [3, 1, 2]
nums.sort()
nums.reverse()

print(nums)
```

Output:

```text
[3, 2, 1]
```

Or use a single call: `nums.sort(reverse=True)`.

New-object functions, on the other hand, can be chained because they return usable values.

```python
result = sorted([3, 1, 2], reverse=True)
print(result)
```

Output:

```text
[3, 2, 1]
```

---

## 8. Set In-Place vs New-Object Operations

Sets follow the same pattern.

```python
s = {1, 2, 3}
s.add(4)           # in-place, returns None
print(s)

t = s | {5, 6}     # new set
print(s)
print(t)
```

Output:

```text
{1, 2, 3, 4}
{1, 2, 3, 4}
{1, 2, 3, 4, 5, 6}
```

| Operation | In-place method | New-object operator |
| ---------- | --------------- | ------------------- |
| Union | `s.update(t)` | `s \| t` |
| Intersection | `s.intersection_update(t)` | `s & t` |
| Difference | `s.difference_update(t)` | `s - t` |

---

## 9. Summary

Key ideas:

- In-place methods (`sort`, `append`, `update`, `add`, `reverse`, `clear`) modify the object
  and return `None`.
- New-object functions and operators (`sorted`, `+`, `|`, string methods) leave the original
  unchanged and return a fresh object.
- Assigning the result of an in-place method to a variable is a common bug---you get `None`.
- In-place methods cannot be chained because `None` has no useful methods.
- When in doubt, check whether the operation returns `None` (in-place) or a new value
  (new object).

---

## Exercises

**Exercise 1.**
A programmer writes this code to get a sorted, reversed list:

```python
data = [4, 1, 7, 2]
result = data.sort().reverse()
print(result)
```

Explain why this fails. Rewrite the code in two ways: (a) using in-place methods correctly,
and (b) using new-object functions to produce the result in a single expression.

??? success "Solution to Exercise 1"
    The code fails with:

    ```text
    AttributeError: 'NoneType' object has no attribute 'reverse'
    ```

    `data.sort()` sorts the list in place and returns `None`. Calling `.reverse()` on `None`
    raises an error.

    **(a) Using in-place methods:**

    ```python
    data = [4, 1, 7, 2]
    data.sort()
    data.reverse()
    print(data)  # [7, 4, 2, 1]
    ```

    Or more concisely:

    ```python
    data = [4, 1, 7, 2]
    data.sort(reverse=True)
    print(data)  # [7, 4, 2, 1]
    ```

    **(b) Using new-object functions:**

    ```python
    data = [4, 1, 7, 2]
    result = sorted(data, reverse=True)
    print(result)  # [7, 4, 2, 1]
    print(data)    # [4, 1, 7, 2]  (original unchanged)
    ```

    The key difference: approach (a) modifies `data` in place, while approach (b) preserves
    the original list and produces a new sorted list.

---

**Exercise 2.**
Predict the output of each `print` call:

```python
a = [1, 2, 3]
b = a + [4, 5]
a.extend([6, 7])

print(a)
print(b)
print(a is b)
```

Explain the difference between `+` and `extend()` in terms of object identity.

??? success "Solution to Exercise 2"
    Output:

    ```text
    [1, 2, 3, 6, 7]
    [1, 2, 3, 4, 5]
    False
    ```

    `a + [4, 5]` creates a **new list** and binds it to `b`. The original list `a` is not
    modified. `a` and `b` are different objects, so `a is b` is `False`.

    `a.extend([6, 7])` modifies `a` **in place**. It adds elements to the existing list
    object. No new list is created.

    The `+` operator is a new-object operation: it always produces a fresh list. `extend()` is
    an in-place operation: it mutates the existing list and returns `None`. If you had other
    references to `a`, they would all see the extended contents. References to `b` would not
    be affected by changes to `a` because `b` is an independent object.

---

**Exercise 3.**
Consider this function:

```python
def clean_text(text):
    text.strip()
    text.lower()
    text.replace("  ", " ")
    return text

result = clean_text("  Hello  World  ")
print(repr(result))
```

The programmer expects `'hello world'` but gets something different. Predict the actual output,
explain the bug, and write a corrected version.

??? success "Solution to Exercise 3"
    Output:

    ```text
    '  Hello  World  '
    ```

    The text is returned completely unmodified. The bug is that **string methods do not modify
    the string in place**---strings are immutable. Each method (`strip()`, `lower()`,
    `replace()`) returns a **new** string, but the code discards those return values. The
    original `text` is never changed.

    Corrected version:

    ```python
    def clean_text(text):
        text = text.strip()
        text = text.lower()
        text = text.replace("  ", " ")
        return text

    result = clean_text("  Hello  World  ")
    print(repr(result))  # 'hello world'
    ```

    Or using method chaining (since each string method returns a new string):

    ```python
    def clean_text(text):
        return text.strip().lower().replace("  ", " ")
    ```

    The corrected code captures the return value of each method call. This is the standard
    pattern for working with immutable types: always use the returned value.
