# F-String Debugging

Python 3.8 introduced the **`=` specifier** for f-strings, allowing expressions to display **both their source and value**.

This feature simplifies debugging by eliminating the need to manually write variable names.

```python
x = 42
print(f"{x=}")   # x=42
```

The output automatically includes the expression:

```text
x=42
```

!!! tip "Mental Model"
    The `=` inside an f-string brace is a "show your work" button. `f"{expr=}"` prints both the expression text and its result, saving you from writing `print(f"expr={expr}")` manually. It works with any expression, not just variable names -- `f"{len(data)=}"` prints `len(data)=42`.

---

## Basic Usage

The `=` specifier prints the expression and its evaluated value.

```python
count = 100
name = "Bob"
active = True

print(f"{count=}")   # count=100
print(f"{name=}")    # name='Bob'
print(f"{active=}")  # active=True
```

---

## Expressions

The debug specifier works with **any Python expression**, not only variables.

```python
x = 5

print(f"{x + 10=}")       # x + 10=15
print(f"{x * 2=}")        # x * 2=10
print(f"{x ** 2=}")       # x ** 2=25

items = [1, 2, 3]
print(f"{len(items)=}")   # len(items)=3
print(f"{sum(items)=}")   # sum(items)=6
```

It also works with **function calls and attributes**:

```python
def add(a, b):
    return a + b

print(f"{add(2,3)=}")   # add(2,3)=5
```

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(3,4)
print(f"{p.x=}, {p.y=}")   # p.x=3, p.y=4
```

---

## Combining with Format Specifiers

The `=` specifier can be combined with **format specifiers**.

```python
value = 123.456789

print(f"{value=}")        # value=123.456789
print(f"{value=:.2f}")    # value=123.46
print(f"{value=:10.2f}")  # value=    123.46
```

Numeric formatting works as expected:

```python
large = 1234567

print(f"{large=:,}")   # large=1,234,567
print(f"{large=:_}")   # large=1_234_567
```

---

## Spaces Around `=`

Whitespace inside the f-string is preserved.

```python
x = 42

print(f"{x=}")     # x=42
print(f"{x =}")    # x =42
print(f"{x= }")    # x= 42
print(f"{x = }")   # x = 42
```

This allows you to control readability.

```python
a, b, c = 1, 2, 3

print(f"{a=},{b=},{c=}")        # compact
print(f"{a = }, {b = }, {c = }")  # readable
```

---

## Practical Debugging Patterns

### Inspect multiple variables

```python
def calculate(a, b, c):
    result = (a + b) * c
    print(f"{a=}, {b=}, {c=}, {result=}")
    return result
```

---

### Debug loops

```python
items = ["apple", "banana", "cherry"]

for i, item in enumerate(items):
    print(f"{i=}, {item=}")
```

---

### Debug intermediate values

```python
def complex_function(x, y):
    print(f"ENTER: {x=}, {y=}")

    intermediate = x * y
    print(f"{intermediate=}")

    result = intermediate ** 2
    print(f"EXIT: {result=}")

    return result
```

---

## String Representation

By default the debug specifier uses **`repr()`**.

```python
name = "Alice"

print(f"{name=}")    # name='Alice'
```

You can override this behavior:

```python
print(f"{name=!s}")  # name=Alice
print(f"{name=!r}")  # name='Alice'
```

---

## ASCII Representation

Use `!a` for ASCII-safe output.

```python
text = "Héllo"

print(f"{text=}")    # text='Héllo'
print(f"{text=!a}")  # text='H\\xe9llo'
```

---

## Limitations

The `=` specifier works **only in f-strings**.

```python
x = 42

print(f"{x=}")   # works
```

It does not work with `str.format()`:

```python
fmt = "{x=}"
# fmt.format(x=42)  # does not produce debug output
```

Also note:

```text
f"{x=}" requires Python 3.8+
```

---

## Key Takeaways

* The `=` specifier prints both an expression and its value.
* It works with variables, expressions, function calls, and attributes.
* Format specifiers can still be applied after `=`.
* The output uses `repr()` by default.
* `!s`, `!r`, and `!a` control string representation.
* The feature is available **only in Python 3.8+**.
* It provides a concise way to add debugging output.


---

## Exercises


**Exercise 1.**
Use the `=` specifier in an f-string to debug-print the values of `x = 10`, `y = 20`, and their sum `x + y` in a single print statement.

??? success "Solution to Exercise 1"

    ```python
    x = 10
    y = 20
    print(f"{x=}, {y=}, {x + y=}")
    # x=10, y=20, x + y=30
    ```

    The `=` specifier automatically includes both the expression text and its value, which is ideal for quick debugging.

---

**Exercise 2.**
Combine the `=` specifier with a format specifier to print a float variable with 2 decimal places in debug format. For example, `pi = 3.14159` should output something like `pi=3.14`.

??? success "Solution to Exercise 2"

    ```python
    pi = 3.14159
    print(f"{pi=:.2f}")
    # pi=3.14
    ```

    The format specifier (`.2f`) is placed after the `=` to control how the value is displayed while still showing the variable name.

---

**Exercise 3.**
Show the difference between `f"{name=}"`, `f"{name=!s}"`, and `f"{name=!r}"` when `name = "Alice"`. Explain when you would use each form.

??? success "Solution to Exercise 3"

    ```python
    name = "Alice"
    print(f"{name=}")     # name='Alice'  (repr by default)
    print(f"{name=!s}")   # name=Alice    (str conversion)
    print(f"{name=!r}")   # name='Alice'  (explicit repr)
    ```

    By default, `=` uses `repr()`, which adds quotes around strings. Use `!s` for human-readable output (no quotes) and `!r` for unambiguous representation (with quotes).
