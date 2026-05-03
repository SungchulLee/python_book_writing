
# str Operators and Membership

Strings support several important operators:

- concatenation with `+`
- repetition with `*`
- membership tests with `in` and `not in`

These operations allow programs to combine, repeat, and inspect text.

```mermaid
flowchart TD
    A[String operations]
    A --> B[Concatenation]
    A --> C[Repetition]
    A --> D[Membership]
````

!!! tip "Mental Model"
    `+` glues strings end to end, `*` repeats a string a given number of times, and `in` checks whether one string appears inside another. Because strings are immutable, `+` and `*` always create new string objects. For building strings from many pieces, prefer `"".join(parts)` or f-strings over repeated `+`, which creates unnecessary intermediate objects.

---

## 1. Concatenation

Concatenation joins strings together.

```python
a = "Hello"
b = "World"

print(a + " " + b)
```

Output:

```text
Hello World
```

The `+` operator creates a new string.

---

## 2. Repetition

The `*` operator repeats a string.

```python
print("ha" * 3)
```

Output:

```text
hahaha
```

This is useful for simple pattern generation.

```python
print("=" * 10)
```

Output:

```text
==========
```

---

## 3. Membership Testing

The `in` operator checks whether a substring appears inside a string.

```python
text = "Python programming"

print("Python" in text)
print("java" in text)
```

Output:

```text
True
False
```

The `not in` operator checks for absence.

```python
print("java" not in text)
```

Output:

```text
True
```

---

## 4. Membership Works on Characters and Substrings

Membership is not limited to single characters.

```python
word = "banana"

print("a" in word)
print("ana" in word)
```

Output:

```text
True
True
```

---

## 5. Operators Produce New Strings

Concatenation and repetition do not modify the original string.

```python
name = "Py"
new_name = name + "thon"

print(name)
print(new_name)
```

Output:

```text
Py
Python
```

---

## 6. Worked Examples

### Example 1: build a filename

```python
base = "report"
ext = ".txt"

filename = base + ext
print(filename)
```

### Example 2: repeated pattern

```python
print("-" * 20)
```

### Example 3: substring test

```python
email = "user@example.com"

if "@" in email:
    print("looks valid")
```

---

## 7. Common Pitfalls

### Concatenating strings and numbers directly

```python
# "Age: " + 25   # TypeError
```

Convert the number first.

```python
print("Age: " + str(25))
```

### Assuming `in` tests whole-word meaning

It checks substring presence, not linguistic word boundaries.

---


## 8. Summary

Key ideas:

* `+` joins strings
* `*` repeats strings
* `in` and `not in` test for substring presence
* string operators return new strings

These operations form the foundation of many basic text-processing tasks.


## Exercises

**Exercise 1.**
String concatenation with `+` inside a loop creates a new string each time. Predict the time complexity and explain the performance problem:

```python
result = ""
for i in range(n):
    result = result + str(i)
```

Why is this O(n^2) in the worst case? What is the efficient alternative and why does it avoid this problem?

??? success "Solution to Exercise 1"
    Each iteration creates a **new** string by copying all characters from `result` plus the new characters from `str(i)`. On iteration `k`, the copy involves roughly `k` characters. The total work is `1 + 2 + 3 + ... + n = O(n^2)`.

    The efficient alternative is `str.join()`:

    ```python
    result = "".join(str(i) for i in range(n))
    ```

    `join()` pre-calculates the total length needed, allocates a single string of that size, and copies each piece once. Total work is O(n). The key difference: concatenation creates `n` intermediate string objects, while `join()` creates just one.

    Note: CPython has an optimization that can sometimes make `+=` concatenation O(n) when the string has a reference count of 1, but this is an implementation detail, not a language guarantee. Using `join()` is always correct and portable.

---

**Exercise 2.**
The `in` operator for strings checks substring presence, not element presence. Predict the output:

```python
print("" in "hello")
print("" in "")
print("hello" in "hello world")
print("Hello" in "hello world")
```

Why is `"" in "hello"` `True`? What property of substrings makes the empty string a substring of every string?

??? success "Solution to Exercise 2"
    Output:

    ```text
    True
    True
    True
    False
    ```

    `"" in "hello"` is `True` because the empty string is a substring of every string. Mathematically, a string `s` is a substring of `t` if there exists a position where `s` matches a contiguous section of `t`. The empty string matches at every position (including the beginning) because there is nothing to fail to match.

    `"" in ""` is `True` for the same reason -- the empty string is a substring of itself.

    `"Hello" in "hello world"` is `False` because substring matching is **case-sensitive**. `"H"` does not match `"h"`. To do case-insensitive matching, convert both strings: `"Hello".lower() in "hello world".lower()`.

---

**Exercise 3.**
A programmer writes:

```python
name = "Alice"
greeting = "Hello, " + name + "! You have " + str(3) + " messages."
```

This works but involves four concatenation operations. Explain why f-strings are preferred:

```python
greeting = f"Hello, {name}! You have {3} messages."
```

What advantages do f-strings have over concatenation in terms of readability, performance, and type handling?

??? success "Solution to Exercise 3"
    F-strings have several advantages:

    1. **Readability**: The template reads like natural text with placeholders. With concatenation, the actual sentence is broken into fragments separated by `+` operators, making it hard to see the final output.

    2. **Automatic type conversion**: F-strings call `str()` on expressions automatically. `f"{3}"` works directly, while concatenation requires explicit `str(3)`. Forgetting `str()` in concatenation causes `TypeError`.

    3. **Performance**: F-strings are compiled to efficient bytecode. The interpreter knows at compile time that it needs to format a string, so it can optimize the operation. Multiple `+` concatenations create intermediate string objects that are immediately discarded.

    4. **Expression support**: F-strings can embed arbitrary expressions: `f"{len(items)} items"`. With concatenation, you need temporary variables or nested function calls within the `+` chain.

    F-strings (introduced in Python 3.6) are the recommended approach for string formatting in modern Python.
