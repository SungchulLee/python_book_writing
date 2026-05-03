
# str Formatting and Docstrings

Strings are often used not just as data, but also as a way to present information and document programs.

This section covers:

- f-strings
- `format()`
- simple formatting ideas
- docstrings

```mermaid
flowchart TD
    A[String formatting]
    A --> B[f-strings]
    A --> C[format()]
    A --> D[docstrings]
````

!!! tip "Mental Model"
    String formatting is about embedding dynamic values into text templates. f-strings (`f"Hello, {name}"`) are the modern, preferred approach---they evaluate expressions inline and read naturally. The older `.format()` method works similarly but is more verbose. Both replace manual string concatenation with a cleaner, more readable pattern.

---

## 1. f-Strings

An f-string allows expressions to be embedded directly inside a string literal.

```python
name = "Alice"
age = 25

print(f"{name} is {age} years old.")
```

Output:

```text
Alice is 25 years old.
```

This is often the clearest modern formatting method.

---

## 2. Formatting Expressions

Expressions can appear inside braces.

```python
x = 5
y = 7

print(f"{x} + {y} = {x + y}")
```

Output:

```text
5 + 7 = 12
```

---

## 3. format()

Python also supports the `format()` method.

```python
name = "Bob"
score = 92

print("{} scored {}".format(name, score))
```

Output:

```text
Bob scored 92
```

Named fields are also possible.

```python
print("{name} scored {score}".format(name="Bob", score=92))
```

---

## 4. Simple Numeric Formatting

Formatting can control appearance.

```python
pi = 3.14159
print(f"{pi:.2f}")
```

Output:

```text
3.14
```

---

## 5. Docstrings

A docstring is a triple-quoted string placed immediately inside a module, function, class, or method definition.

```python
def area(length, width):
    """Return the area of a rectangle."""
    return length * width
```

Docstrings are used for documentation and are accessible at runtime.

```python
print(area.__doc__)
```

Output:

```text
Return the area of a rectangle.
```

---

## 6. Multiline Docstrings

Docstrings can span multiple lines.

```python
def greet(name):
    """
    Return a greeting message.

    Args:
        name: person's name
    """
    return f"Hello, {name}"
```

---

## 7. Worked Examples

### Example 1: f-string

```python
language = "Python"
version = 3.12

print(f"{language} {version}")
```

### Example 2: format method

```python
print("x = {}, y = {}".format(3, 4))
```

### Example 3: function docstring

```python
def square(x):
    """Return x squared."""
    return x * x

print(square.__doc__)
```

---

## 8. Common Pitfalls

### Forgetting the `f` in f-strings

```python
# "{name}"   # literal text, not formatted
```

### Confusing ordinary multiline strings with docstrings

A string becomes a docstring only when placed as the first statement in a module, function, class, or method body.

---


## 9. Summary

Key ideas:

* f-strings are a powerful formatting tool
* `format()` provides an older but still useful formatting style
* docstrings document code objects
* triple-quoted strings are often used for docstrings

Formatting and documentation make string usage much more practical and expressive.


## Exercises

**Exercise 1.**
F-strings can contain arbitrary expressions. Predict the output:

```python
x = 10
print(f"{x}")
print(f"{x!r}")
print(f"{x:05d}")
print(f"{x:>10}")
print(f"{'hello':*^20}")
```

Explain the difference between `!r` and `:05d`. What is the general syntax inside an f-string brace `{expression!conversion:format_spec}`?

??? success "Solution to Exercise 1"
    Output:

    ```text
    10
    10
    00010
         10
    *******hello********
    ```

    - `{x}`: inserts the string representation of `x`.
    - `{x!r}`: the `!r` conversion calls `repr(x)` instead of `str(x)`. For integers, `str(10)` and `repr(10)` are the same. The difference shows with strings: `f"{'hi'!r}"` produces `"'hi'"` (with quotes).
    - `{x:05d}`: format spec `05d` means "decimal integer, 5 characters wide, zero-padded."
    - `{x:>10}`: right-align within 10 characters.
    - `{'hello':*^20}`: center `"hello"` in 20 characters, fill with `*`.

    The general syntax is `{expression!conversion:format_spec}` where `!conversion` is optional (`!s` for `str()`, `!r` for `repr()`, `!a` for `ascii()`), and `format_spec` controls width, alignment, fill, precision, and type.

---

**Exercise 2.**
A programmer writes a docstring for a function but cannot access it later:

```python
def compute(x):
    # Compute the square of x
    return x * x

print(compute.__doc__)
```

What does this print? Why? Then explain: what makes a string a docstring vs. an ordinary comment? Are docstrings stored at runtime, and if so, where?

??? success "Solution to Exercise 2"
    This prints `None`.

    A comment (`# Compute the square of x`) is not a docstring. Comments are stripped by the parser and never stored at runtime. A **docstring** must be a **string literal** (not a comment) placed as the **first statement** in the function body:

    ```python
    def compute(x):
        """Compute the square of x."""
        return x * x
    ```

    Now `compute.__doc__` returns `"Compute the square of x."`.

    Docstrings are stored at runtime in the `__doc__` attribute of the function/class/module object. This is what allows `help(compute)` to display documentation interactively. Comments are purely for human readers of the source code and have no runtime existence.

---

**Exercise 3.**
Python has three formatting approaches: f-strings, `.format()`, and `%`-formatting. Compare them:

```python
name = "Alice"
age = 30
print(f"{name} is {age}")
print("{} is {}".format(name, age))
print("%s is %d" % (name, age))
```

All three produce the same output. When should each be used? Why are f-strings generally preferred in modern Python? Give one scenario where `.format()` is necessary and f-strings cannot be used.

??? success "Solution to Exercise 3"
    All three produce: `Alice is 30`.

    - **F-strings** (Python 3.6+): preferred for most cases. They are concise, readable, and evaluated at runtime with direct access to local variables. They are also the fastest because the format is compiled into bytecode.
    - **`.format()`** (Python 2.6+): useful when the template is not a literal -- e.g., loaded from a configuration file or database: `template = "{name} is {age}"; template.format(name=name, age=age)`. F-strings cannot do this because the expression must be a literal at the call site.
    - **`%`-formatting**: the oldest style, modeled after C's `printf`. Still seen in legacy code and in `logging` module format strings. Generally avoided in new code.

    One scenario where `.format()` is necessary: when the template string is not known at write time. For example:

    ```python
    templates = {"en": "Hello, {name}!", "es": "Hola, {name}!"}
    lang = "es"
    print(templates[lang].format(name="Alice"))
    ```

    You cannot use an f-string here because the template is a variable, not a literal.
