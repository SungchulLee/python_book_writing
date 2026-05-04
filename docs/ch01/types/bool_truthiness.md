
# bool Truthiness

In Python, many values can be interpreted as either **true** or **false** in a Boolean context.

This behavior is called **truthiness**.

Truthiness is used in:

- `if` statements
- `while` loops
- logical expressions
- built-in functions such as `any()` and `all()`

```mermaid
flowchart TD
    A[Python value] --> B{Boolean context}
    B -->|truthy| C[treated as True]
    B -->|falsy| D[treated as False]
````

!!! tip "Mental Model"
    In Python, "empty means false." Zero, empty strings, empty collections, and `None` are all falsy; everything else is truthy. This is why `if my_list:` works as a check for a non-empty list. Truthiness lets you write concise conditions without explicit comparisons like `if len(my_list) > 0`.

---

## 1. Truthy and Falsy Values

A value does not have to be of type `bool` to behave like `True` or `False`.

### Common falsy values

```python
False
None
0
0.0
0j
""
[]
()
{}
set()
range(0)
```

Everything else is generally truthy.

Example:

```python
if []:
    print("non-empty")
else:
    print("empty")
```

Output:

```text
empty
```

---

## 2. Empty vs Non-Empty Containers

Containers are falsy when empty and truthy when non-empty.

```python
print(bool([]))
print(bool([1, 2, 3]))
print(bool(""))
print(bool("Python"))
```

Output:

```text
False
True
False
True
```

This allows very readable code.

```python
items = [1, 2, 3]

if items:
    print("List has elements")
```

---

## 3. Numeric Truthiness

Numbers follow a simple rule:

* zero is falsy
* nonzero values are truthy

```python
print(bool(0))
print(bool(42))
print(bool(-7))
print(bool(0.0))
```

Output:

```text
False
True
True
False
```

This applies to `int`, `float`, and `complex`.

---

## 4. Truthiness in Conditions

Truthy and falsy values are often used directly in `if` statements.

```python
name = ""

if name:
    print("Hello", name)
else:
    print("No name provided")
```

Output:

```text
No name provided
```

This is often cleaner than writing explicit comparisons.

---

## 5. Truthiness and while Loops

Truthiness also controls loops.

```python
data = [1, 2, 3]

while data:
    print(data.pop())
```

The loop continues while `data` is non-empty.

---

## 6. Worked Examples

### Example 1: empty string

```python
password = ""

if password:
    print("Password entered")
else:
    print("Missing password")
```

### Example 2: numeric test

```python
x = 0

if x:
    print("nonzero")
else:
    print("zero")
```

Output:

```text
zero
```

### Example 3: list test

```python
values = [10]

if values:
    print("List is not empty")
```

---

## 7. Common Pitfalls

### Confusing `None` with `False`

`None` is falsy, but it is not the same object as `False`.

### Overusing explicit checks

Instead of:

```python
if len(items) > 0:
    ...
```

Python often prefers:

```python
if items:
    ...
```

---


## 8. Summary

Key ideas:

* many Python values have truthiness
* empty containers are falsy
* zero numeric values are falsy
* non-empty containers and nonzero numbers are truthy
* truthiness makes conditions concise and expressive

Understanding truthiness makes Python control flow more natural and readable.




---

## Notebook Examples

```python
obj = 1

if obj: # int ---> bool (casting)
    print("interpreted as true")
else:
    print("interpreted as false")
```

```python
obj = 0

if obj: # int ---> bool (casting)
    print("interpreted as true")
else:
    print("interpreted as false")
```

```python
obj = -10

if obj: # int ---> bool (casting)
    print("interpreted as true")
else:
    print("interpreted as false")
```

```python
a = 1
b = 1.0
c = a + b

print(c, type(c))
```

```python
obj = 1.

if obj: # float ---> bool (casting)
    print("interpreted as true")
else:
    print("interpreted as false")
```

```python
obj = 0.

if obj: # float ---> bool (casting)
    print("interpreted as true")
else:
    print("interpreted as false")
```

```python
obj = -10.

if obj: # float ---> bool (casting)
    print("interpreted as true")
else:
    print("interpreted as false")
```

```python
obj = []

if obj: # list ---> bool (casting)
    print("interpreted as true")
else:
    print("interpreted as false")
```

```python
obj = [0]

if obj: # list ---> bool (casting)
    print("interpreted as true")
else:
    print("interpreted as false")

print( bool(obj) )
```

---

## Exercises

**Exercise 1.**
Predict the output of each line and explain why:

```python
print(bool([]))
print(bool([0]))
print(bool(""))
print(bool(" "))
print(bool(0.0))
print(bool(None))
```

A common mistake is thinking `[0]` is falsy because it contains zero, or that `" "` is falsy because it "looks empty." Why are these truthy?

??? success "Solution to Exercise 1"
    Output:

    ```text
    False
    True
    False
    True
    False
    False
    ```

    - `bool([])` is `False`: an **empty** list is falsy.
    - `bool([0])` is `True`: the list contains one element. Truthiness of a container depends on whether the container **has elements**, not on the truthiness of those elements. `[0]` has length 1, so it is truthy.
    - `bool("")` is `False`: an empty string is falsy.
    - `bool(" ")` is `True`: a string containing a space has length 1. It is not empty. Truthiness checks length, not visual appearance.
    - `bool(0.0)` is `False`: zero float is falsy (like zero int).
    - `bool(None)` is `False`: `None` is always falsy.

    The rule is simple: for containers, empty = falsy, non-empty = truthy. For numbers, zero = falsy, nonzero = truthy. The truthiness of a container does not depend on its contents' truthiness.

---

**Exercise 2.**
Python's `or` and `and` operators use truthiness, not just booleans. Explain the pattern used in this idiom:

```python
username = input_name or "Anonymous"
```

How does truthiness make this work? What values of `input_name` would cause `"Anonymous"` to be used? Why might this idiom be surprising if `input_name` is `0` (an integer)?

??? success "Solution to Exercise 2"
    The `or` operator returns the first truthy operand (or the last operand if all are falsy). So `input_name or "Anonymous"` returns `input_name` if it is truthy, otherwise `"Anonymous"`.

    This works because a non-empty string (the user typed something) is truthy, while an empty string `""` (the user typed nothing) is falsy.

    Values that would trigger `"Anonymous"`: `""`, `None`, `0`, `False`, `[]`, and any other falsy value.

    The surprise with `0`: if `input_name` is the integer `0` (perhaps a valid user ID), it is falsy. The expression would return `"Anonymous"` even though `0` is a legitimate value, not a missing value. This is why the idiom should only be used when all falsy values genuinely indicate "missing." For more precise control, use `input_name if input_name is not None else "Anonymous"`.

---

**Exercise 3.**
A function returns `None` when no result is found and an empty list `[]` when the search succeeds but finds nothing. A programmer writes:

```python
result = find_items(query)
if not result:
    print("No results")
```

Explain why this code conflates two different situations. How do `None` and `[]` differ semantically, even though both are falsy? What is a more precise way to handle each case?

??? success "Solution to Exercise 3"
    `None` and `[]` are both falsy, so `not result` is `True` for both. But they have different meanings:

    - `None` means "the search could not be performed" or "no result exists" -- the function found nothing.
    - `[]` means "the search succeeded and returned a valid result that happens to be empty" -- the function found an empty collection.

    The code treats both identically, which may hide errors. A more precise approach:

    ```python
    result = find_items(query)
    if result is None:
        print("Search failed or no results available")
    elif len(result) == 0:
        print("Search succeeded but found nothing")
    else:
        print(f"Found {len(result)} items")
    ```

    This illustrates a general principle: truthiness is convenient for quick checks, but when `None` and empty containers have different semantic meanings, use explicit checks (`is None` for None, `len() == 0` for empty containers) rather than relying on truthiness.
