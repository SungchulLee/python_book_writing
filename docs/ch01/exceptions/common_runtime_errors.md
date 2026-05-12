
# Common Runtime Errors

Runtime errors are not random---they reflect different kinds of failure. Most fall into a few fundamental categories:

1. **Type mismatch** --- wrong kind of object (`TypeError`)
2. **Invalid value** --- right type, wrong data (`ValueError`)
3. **Lookup failure** --- missing element (`IndexError`, `KeyError`)
4. **State error** --- invalid operation (`ZeroDivisionError`, `AttributeError`)

These categories reflect different kinds of assumptions being violated: type assumptions, value constraints, data availability, and valid program state. They map directly to how Python defines exception classes, making the hierarchy predictable rather than arbitrary. Understanding them helps predict and diagnose errors, rather than memorizing individual exception types.

```mermaid
flowchart TD
    A[Runtime Errors]
    A --> B[TypeError]
    A --> C[ValueError]
    A --> D[IndexError]
    A --> E[KeyError]
    A --> F[ZeroDivisionError]
````

!!! tip "Mental Model"
    Every runtime error is a violated assumption: you assumed the type was right (`TypeError`), the value was valid (`ValueError`), the element existed (`KeyError`, `IndexError`), or the operation was legal (`ZeroDivisionError`). Reading the exception name tells you which assumption broke, which points you directly to the fix.

---

## 1. TypeError

Occurs when an operation is applied to incompatible types.

Example:

```python
"hello" + 5
```

Output:

```text
TypeError: can only concatenate str (not "int") to str
```

---

## 2. ValueError

Occurs when a function receives a value of the correct type but an inappropriate value.

Example:

```python
int("hello")
```

Output:

```text
ValueError: invalid literal for int()
```

---

## 3. IndexError

Occurs when accessing an invalid index in a sequence.

```python
numbers = [1, 2, 3]
print(numbers[10])
```

Output:

```text
IndexError: list index out of range
```

---

## 4. KeyError

Occurs when accessing a missing dictionary key.

```python
data = {"a": 1}
print(data["b"])
```

Output:

```text
KeyError: 'b'
```

---

## 5. ZeroDivisionError

Occurs when dividing by zero.

```python
print(10 / 0)
```

Output:

```text
ZeroDivisionError
```

---

## 6. NameError

Occurs when a variable name is not defined.

```python
print(x)
```

Output:

```text
NameError: name 'x' is not defined
```

---

## 7. AttributeError

Occurs when accessing a nonexistent attribute.

```python
x = 5
x.append(3)
```

Output:

```text
AttributeError: 'int' object has no attribute 'append'
```

---

## 8. Worked Examples

### Example 1: safe dictionary access

```python
data = {"a": 1}

print(data.get("b"))
```

Output:

```text
None
```

### Example 2: checking length before indexing

```python
values = [1, 2]

if len(values) > 3:
    print(values[3])
```

---


## 9. Summary

Key ideas:

* runtime errors occur during execution
* different exception types describe different problems
* recognizing common exceptions helps with debugging
* careful checks can prevent some errors

These errors can be handled using `try/except`, discussed in the next section.


## Exercises

**Exercise 1.**
For each code snippet, predict the exact exception type and explain why that specific exception (not a different one) is raised:

```python
# A
len(42)

# B
int("3.14")

# C
{"a": 1}["b"]

# D
[1, 2, 3][5]
```

What is the difference between `TypeError` and `ValueError`? Both indicate "wrong input" -- how does Python decide which one to raise?

??? success "Solution to Exercise 1"

    - **A**: `TypeError: object of type 'int' has no len()`. The type `int` does not support `len()`. The **type** is wrong for this operation.
    - **B**: `ValueError: invalid literal for int() with base 10: '3.14'`. The type is correct (`str`), but the **value** is inappropriate (contains a decimal point).
    - **C**: `KeyError: 'b'`. The key `"b"` does not exist in the dictionary.
    - **D**: `IndexError: list index out of range`. Index `5` is beyond the list's valid range.

    The distinction between `TypeError` and `ValueError`: `TypeError` means the **type** of the argument is fundamentally incompatible with the operation -- no value of that type would work. `ValueError` means the **type** is correct, but this particular **value** is invalid. For example, `int("42")` works (correct type and value), `int("hello")` raises `ValueError` (correct type, wrong value), and `int([1, 2])` raises `TypeError` (wrong type entirely).

---

**Exercise 2.**
A programmer writes code that could raise multiple different exceptions:

```python
def process(data, index):
    item = data[index]
    return int(item)

process(["10", "hello", "30"], 5)
```

What exception is raised? What if you change the call to `process(["10", "hello", "30"], 1)`? What is the order of operations that determines which error occurs first?

??? success "Solution to Exercise 2"
    `process(["10", "hello", "30"], 5)` raises `IndexError: list index out of range` because `data[5]` is evaluated first, and the list only has 3 elements.

    `process(["10", "hello", "30"], 1)` raises `ValueError: invalid literal for int() with base 10: 'hello'` because `data[1]` successfully returns `"hello"`, but then `int("hello")` fails.

    The order of operations matters: Python evaluates expressions left-to-right, and the first error encountered is the one raised. In the first case, the indexing fails before `int()` is ever called. In the second case, the indexing succeeds but the conversion fails. This is why the same function can raise different exceptions depending on the input.

---

**Exercise 3.**
`NameError` and `AttributeError` both involve failed name lookups. Explain the difference:

```python
# NameError
print(undefined_variable)

# AttributeError
x = 42
print(x.append)
```

Why are these different exception types and not just the same error? How does Python's name resolution process determine which one to raise?

??? success "Solution to Exercise 3"
    `NameError` occurs when Python cannot find a **bare name** in any accessible scope (local, enclosing, global, built-in -- the LEGB rule). The name `undefined_variable` does not exist anywhere.

    `AttributeError` occurs when Python finds the **object** (`x = 42`) but the object does not have the requested **attribute** (`.append`). The name `x` is found successfully, but the `int` object it refers to does not have an `append` attribute.

    They are different exceptions because they represent different failure points in name resolution:

    - `NameError`: the name itself cannot be resolved to any object.
    - `AttributeError`: the name resolves to an object, but the attribute lookup on that object fails.

    This distinction is important for debugging: `NameError` means "this variable does not exist" (likely a typo or missing import), while `AttributeError` means "this variable exists but is the wrong type for this operation" (likely a logic error).
