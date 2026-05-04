

# str Methods: Case and Checks

Python strings provide many useful methods for:

- changing case
- testing properties

These methods help analyze and normalize text.

```mermaid
flowchart TD
    A[String methods]
    A --> B[case methods]
    A --> C[check methods]
````

!!! tip "Mental Model"
    Case methods (`.upper()`, `.lower()`, `.title()`) transform text into a standard form; check methods (`.isdigit()`, `.isalpha()`, `.isspace()`) test what kind of characters a string contains. Both return new values without modifying the original string. Use case methods to normalize user input and check methods to validate it.

---

## 1. Case Methods

Common case-related methods include:

| Method         | Purpose                    |
| -------------- | -------------------------- |
| `lower()`      | convert to lowercase       |
| `upper()`      | convert to uppercase       |
| `title()`      | title-case words           |
| `capitalize()` | capitalize first character |
| `swapcase()`   | swap upper and lower case  |

Example:

```python
text = "pYtHoN"

print(text.lower())
print(text.upper())
print(text.title())
print(text.swapcase())
```

---

## 2. Case Methods Return New Strings

Because strings are immutable, these methods do not modify the original string.

```python
text = "Python"
lowered = text.lower()

print(text)
print(lowered)
```

---

## 3. Check Methods

Check methods return Boolean values.

Common examples:

| Method      | Meaning                        |
| ----------- | ------------------------------ |
| `isalpha()` | all alphabetic characters      |
| `isdigit()` | all digits                     |
| `isalnum()` | alphanumeric only              |
| `islower()` | all cased characters lowercase |
| `isupper()` | all cased characters uppercase |
| `isspace()` | all whitespace                 |

Example:

```python
print("Python".isalpha())
print("123".isdigit())
print("abc123".isalnum())
```

Output:

```text
True
True
True
```

---

## 4. Validation Use Cases

These methods are often used for simple input validation.

```python
code = "12345"

if code.isdigit():
    print("numeric code")
```

Another example:

```python
name = "Alice"

if name.isalpha():
    print("letters only")
```

---

## 5. Worked Examples

### Example 1: normalize for comparison

```python
a = "HELLO"
b = "hello"

print(a.lower() == b.lower())
```

### Example 2: check digits

```python
text = "2025"
print(text.isdigit())
```

### Example 3: title case

```python
title = "python programming"
print(title.title())
```

Output:

```text
Python Programming
```

---

## 6. Common Pitfalls

### Assuming methods modify in place

They return new strings.

### Overtrusting simple checks

Methods such as `isdigit()` are useful, but real-world validation often needs additional rules.

---


## 7. Summary

Key ideas:

* case methods transform strings
* check methods test textual properties
* all string methods return new strings
* these methods are useful for normalization and validation

Case and check methods are among the most frequently used string tools in Python.




---

## Notebook Examples

```python
a = "Hi Bob"
print( a ) # "Hi Bob"
print( a.upper() ) # "HI BOB"
print( str.upper(a) ) # "HI BOB"
print( a ) # "Hi Bob"
```

```python
a = "Hi Bob"
print( a ) # "Hi Bob"
a = a.upper()
print( a ) # "HI BOB"
```

---

## Exercises

**Exercise 1.**
A programmer writes a case-insensitive comparison:

```python
user_input = "YES"
if user_input.lower() == "yes":
    print("Confirmed")
```

This works for English, but explain why `.lower()` is not always sufficient for case-insensitive comparison in Unicode. What does `"ß".lower() == "ss"` return? What is the correct general approach for case-insensitive matching (`casefold`)?

??? success "Solution to Exercise 1"
    `"ß".lower()` returns `"ß"` (unchanged), not `"ss"`. So `"ß".lower() == "ss"` is `False`. But in German, `"ß"` is considered equivalent to `"ss"` for case-insensitive comparison.

    The correct approach is `casefold()`:

    ```python
    print("ß".casefold())  # "ss"
    print("ß".casefold() == "ss".casefold())  # True
    ```

    `casefold()` performs aggressive case folding as defined by Unicode. It handles special characters like `ß` (German sharp s), `ſ` (long s), and other locale-specific equivalences. For ASCII-only text, `lower()` and `casefold()` are identical. For internationalized text, always use `casefold()` for case-insensitive comparison.

---

**Exercise 2.**
Predict the output and explain each result:

```python
print("".isalpha())
print("".isdigit())
print("".isspace())
print(" \t\n".isspace())
print("123".isalpha())
print("abc123".isalnum())
```

Why do empty strings return `False` for all `is*()` methods? What is the common pattern these methods follow?

??? success "Solution to Exercise 2"
    Output:

    ```text
    False
    False
    False
    True
    False
    True
    ```

    Empty strings return `False` for all `is*()` methods. The common pattern: these methods return `True` if the string is **non-empty** and **every character** satisfies the condition. An empty string has no characters to satisfy the condition, so it returns `False`.

    `" \t\n".isspace()` is `True` because the string is non-empty and every character (space, tab, newline) is whitespace.

    `"123".isalpha()` is `False` because digits are not alphabetic. `"abc123".isalnum()` is `True` because every character is either alphabetic or numeric.

---

**Exercise 3.**
String methods return new strings, not modify in place. A programmer writes:

```python
name = "  alice  "
name.strip()
name.capitalize()
print(name)
```

Predict the output and explain the bug. Then show how to fix it using method chaining. Why does Python make string methods return new strings instead of modifying in place?

??? success "Solution to Exercise 3"
    Output: `  alice  ` (unchanged).

    The bug: `strip()` and `capitalize()` return **new strings**, but the return values are discarded. The original `name` is never modified because strings are immutable.

    Fixed with method chaining:

    ```python
    name = "  alice  "
    name = name.strip().capitalize()
    print(name)  # "Alice"
    ```

    Method chaining works because each method returns a new string, and the next method is called on that new string. `name.strip()` returns `"alice"`, and `.capitalize()` is called on `"alice"`, returning `"Alice"`.

    Python makes string methods return new strings (instead of modifying in place) because strings are **immutable**. Immutability means strings can be safely used as dictionary keys, shared between variables without defensive copying, and used safely across threads. The trade-off is that every "modification" creates a new object, but this is the fundamental design decision that makes strings reliable and predictable.
