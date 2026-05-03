
# str Literals and Escaping

Python provides several ways to write string literals.

This section covers:

- single-quoted strings
- double-quoted strings
- escape characters
- multiline strings
- raw strings

```mermaid
flowchart TD
    A[String literals]
    A --> B[single quotes]
    A --> C[double quotes]
    A --> D[triple quotes]
    A --> E[raw strings]
    A --> F[escape sequences]
````

!!! tip "Mental Model"
    String literals are how you write text in source code. Single and double quotes are interchangeable---choose whichever avoids internal escaping. Backslash `\` is the escape character that gives special meaning to the next character (`\n` for newline, `\t` for tab). Raw strings (`r"..."`) disable escaping entirely, which is invaluable for regex patterns and Windows file paths.

---

## 1. Single and Double Quotes

Strings can be written with either single quotes or double quotes.

```python
'a'
"hello"
```

These are equivalent in meaning.

```python
print('Python')
print("Python")
```

Use whichever form improves readability.

For example, double quotes are convenient when the string contains an apostrophe:

```python
print("Don't panic")
```

---

## 2. Escape Characters

Some characters cannot be written directly inside a string literal without special syntax.

Python uses **escape sequences** beginning with `\`.

| Escape | Meaning      |
| ------ | ------------ |
| `\'`   | single quote |
| `\"`   | double quote |
| `\\`   | backslash    |
| `\n`   | newline      |
| `\t`   | tab          |

Example:

```python
print("Line 1\nLine 2")
print("A\tB\tC")
print("He said: \"hello\"")
```

Output:

```text
Line 1
Line 2
A	B	C
He said: "hello"
```

---

## 3. Multiline Strings

Triple quotes allow strings to span multiple lines.

```python
text = """This is
a multiline
string."""
print(text)
```

Triple single quotes also work:

```python
text = '''another
multiline
string'''
```

Multiline strings are useful for:

* long text
* embedded examples
* templates
* docstrings

---

## 4. Raw Strings

A raw string treats backslashes literally.

```python
path = r"C:\new_folder\test.txt"
print(path)
```

Output:

```text
C:\new_folder\test.txt
```

Without the `r` prefix, sequences like `\n` would be interpreted as escapes.

Raw strings are especially useful for:

* file paths
* regular expressions
* Windows path examples

---

## 5. Choosing a Literal Style

Common guideline:

* use single or double quotes for ordinary strings
* use triple quotes for multiline text
* use raw strings when backslashes should remain literal

---

## 6. Worked Examples

### Example 1: newline

```python
print("Hello\nWorld")
```

### Example 2: quote inside string

```python
quote = "She said, \"Python is fun\"."
print(quote)
```

### Example 3: raw path

```python
path = r"C:\Users\name\Documents"
print(path)
```

---

## 7. Common Pitfalls

### Forgetting escapes

```python
# "C:\new"   # contains \n
```

This may produce an unintended newline.

### Confusing raw strings with ordinary strings

Raw strings still have syntax rules and are not magical text containers.

---


## 8. Summary

Key ideas:

* Python supports multiple string literal forms
* escape sequences represent special characters
* triple quotes allow multiline strings
* raw strings preserve backslashes literally

Understanding string literals is the first step toward working with text correctly.


## Exercises

**Exercise 1.**
Predict the output and explain each difference:

```python
print("hello\nworld")
print(r"hello\nworld")
print("hello\\nworld")
```

When would you use a raw string versus an escaped backslash? Why can a raw string not end with an odd number of backslashes (e.g., `r"path\"`)?

??? success "Solution to Exercise 1"
    Output:

    ```text
    hello
    world
    hello\nworld
    hello\nworld
    ```

    - `"hello\nworld"`: `\n` is interpreted as a newline escape sequence.
    - `r"hello\nworld"`: the `r` prefix makes it a raw string -- `\n` is two literal characters, backslash and `n`.
    - `"hello\\nworld"`: `\\` is the escape sequence for a literal backslash, followed by the letter `n`. The result is the same as the raw string.

    Use raw strings for **regular expressions** (`r"\d+\.\d+"`) and **file paths** where backslashes appear frequently. Use escaped backslashes when you need a specific escape within a string that also contains literal backslashes.

    A raw string cannot end with an odd number of backslashes because the parser still processes the quote character after a backslash. In `r"path\"`, the `\"` is interpreted as an escaped quote (even in raw mode, backslash-quote prevents the string from ending), leaving no closing quote. This is a limitation of Python's string parser.

---

**Exercise 2.**
A programmer writes a file path and gets unexpected behavior:

```python
path = "C:\new_folder\test.txt"
print(path)
```

Explain what Python does with `\n` and `\t` in this string. Show two correct ways to write this path. Which approach is preferred for Windows paths in practice?

??? success "Solution to Exercise 2"
    Output (approximately):

    ```text
    C:
    ew_folder	est.txt
    ```

    Python interprets `\n` as a newline and `\t` as a tab. The string contains a newline where `\n` appears and a tab where `\t` appears, completely mangling the intended path.

    Two correct approaches:

    ```python
    path = r"C:\new_folder\test.txt"    # raw string
    path = "C:\\new_folder\\test.txt"    # escaped backslashes
    ```

    In practice, the **best** approach for paths is to use `pathlib`:

    ```python
    from pathlib import Path
    path = Path("C:/new_folder/test.txt")
    ```

    Forward slashes work on all platforms (including Windows), and `pathlib` handles path manipulation correctly.

---

**Exercise 3.**
Python treats single quotes, double quotes, and triple quotes as equivalent for string creation. Explain why all three exist:

```python
a = 'hello'
b = "hello"
c = """hello"""
d = '''hello'''
```

When is each form most appropriate? Then explain: what is the relationship between triple-quoted strings and docstrings? Are they fundamentally different objects, or the same thing used in different contexts?

??? success "Solution to Exercise 3"
    - **Single quotes** (`'hello'`): useful when the string contains double quotes: `'She said "hi"'`.
    - **Double quotes** (`"hello"`): useful when the string contains apostrophes: `"Don't panic"`.
    - **Triple quotes** (`"""hello"""` or `'''hello'''`): useful for strings that span multiple lines or contain both single and double quotes.

    All four forms create identical `str` objects. `a == b == c == d` is `True`, and all have `type(x) == str`.

    **Docstrings** are just triple-quoted strings placed as the first statement in a module, class, or function. They are not a special type -- they are ordinary `str` objects. Python stores them in the `__doc__` attribute. The only difference is **context**: when a string literal is the first expression in a definition body, Python treats it as documentation and makes it accessible via `__doc__`. In every other way, a docstring is just a string.
