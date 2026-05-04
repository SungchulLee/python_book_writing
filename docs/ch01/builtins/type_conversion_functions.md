


# Type Conversion Functions

Type conversion functions operate at the **boundary between data representations**---they transform a value from one type to another. These are essential when working with input data (which arrives as strings) or performing operations that require specific types.

| Function | Description |
|---|---|
| int() | convert to integer |
| float() | convert to floating point |
| str() | convert to string |
| bool() | convert to boolean |
| list() | convert to list |
| tuple() | convert to tuple |
| set() | convert to set |

Conversion can fail when the input cannot be interpreted in the target type:

```python
int("abc")  # ValueError: invalid literal for int() with base 10: 'abc'
```

This makes type conversion both a **transformation** and a **validation boundary**---it connects directly to exception handling.

!!! tip "Mental Model"
    Type conversion functions are translators between representations. `int("42")` does not just relabel the string---it parses the text and builds a new integer object. Conversion can fail when the input has no valid interpretation in the target type, which is why conversion and error handling often go hand in hand.

---

## Conversion vs Interpretation

Some conversions simply change type:

```python
float(3)   # 3 → 3.0
```

Others **interpret structure**:

```python
int("10")     # parses digits → 10
list("abc")   # splits string → ['a', 'b', 'c']
```

These are not just type changes---they interpret the input.

---

## int()

```python
x = int("10")
print(x)
````

Output

```
10
```

---

## float()

```python
y = float("3.14")
print(y)
```

---

## str()

```python
value = 100
text = str(value)

print(text)
```

---

## bool()

In general, a value is falsy if it represents "zero" or "empty." Common falsy values include:

```
0
None
False
""
[]
{}
```

Example

```python
print(bool(0))
print(bool(42))
```

---

## Practical Example

```python
# Parsing user input safely
user_input = "42"

try:
    value = int(user_input)
    print(value + 10)   # 52
except ValueError:
    print("Invalid number")
```

---



---

## Notebook Examples

```python
print(int("10"))
```

```python
print(str(10))
```

```python
print(float(10)) # explict conversion
```

```python
print(1 + 1.0) # implict conversion; casting
```

---

## Exercises

**Exercise 1.**
Type conversion functions are also constructors for their types. Predict the output:

```python
print(int())
print(float())
print(str())
print(bool())
print(list())
print(tuple())
print(set())
```

What is the "zero value" or "empty value" for each type? Why does calling these constructors with no arguments produce these defaults?

??? success "Solution to Exercise 1"
    Output:

    ```text
    0
    0.0
    ''
    False
    []
    ()
    set()
    ```

    (Note: `str()` returns `''`, an empty string, which prints as a blank line.)

    Each type has a natural "zero" or "empty" value: `0` for `int`, `0.0` for `float`, `""` for `str`, `False` for `bool`, `[]` for `list`, `()` for `tuple`, `set()` for `set`.

    These are the defaults because each type's constructor, when called with no arguments, returns a natural "zero" or empty value for that type. This is a consistent design: every type has a well-defined default.

---

**Exercise 2.**
`bool()` applies truthiness rules. Predict the output:

```python
print(bool(0), bool(1), bool(-1))
print(bool(""), bool(" "), bool("False"))
print(bool([]), bool([0]), bool([[]]))
```

Why is `bool("False")` `True`? Why is `bool([0])` `True`? What is the general rule Python uses to determine truthiness?

??? success "Solution to Exercise 2"
    Output:

    ```text
    False True True
    False True True
    False True True
    ```

    `bool("False")` is `True` because `"False"` is a **non-empty string**. Python does not parse the string content -- it only checks whether the string is empty. Any non-empty string is truthy, regardless of what it says.

    `bool([0])` is `True` because the list is **non-empty** (it contains one element). The truthiness of containers depends on their length, not their contents.

    The general rule: a value is falsy if it is a "zero" or "empty" value: `0`, `0.0`, `""`, `None`, `False`, `[]`, `()`, `{}`, `set()`. Everything else is truthy. Custom classes can define `__bool__()` or `__len__()` to customize this behavior.

---

**Exercise 3.**
Some type conversions lose information. For each conversion, state whether information is preserved or lost:

```python
print(int(3.9))
print(float(3))
print(str(42))
print(int("42"))
print(list("abc"))
print(tuple([1, 2, 3]))
print(set([1, 2, 2, 3]))
```

Which conversions are **reversible** (you can convert back and get the original value)? Which are **lossy** (information is permanently lost)?

??? success "Solution to Exercise 3"
    | Conversion | Reversible? | Notes |
    |-----------|------------|-------|
    | `int(3.9)` = `3` | **Lossy** | The fractional part `.9` is permanently lost |
    | `float(3)` = `3.0` | Reversible (in this case) | `int(3.0)` gives `3` |
    | `str(42)` = `"42"` | Reversible | `int("42")` gives `42` |
    | `int("42")` = `42` | Reversible | `str(42)` gives `"42"` |
    | `list("abc")` = `["a", "b", "c"]` | Reversible | `"".join(["a", "b", "c"])` gives `"abc"` |
    | `tuple([1, 2, 3])` = `(1, 2, 3)` | Reversible | `list((1, 2, 3))` gives `[1, 2, 3]` |
    | `set([1, 2, 2, 3])` = `{1, 2, 3}` | **Lossy** | Duplicates and order are permanently lost |

    The lossy conversions are `int(float)` (truncation loses fractional part) and `set(list)` (deduplication loses duplicates and ordering). These are one-way operations -- you cannot recover the original value.
