

# str Built-in Functions

Several built-in functions work naturally with strings.

These functions help inspect, transform, and analyze text.

Common examples include:

- `len()`
- `str()`
- `sorted()`
- `reversed()`
- `enumerate()`
- `ord()`
- `chr()`

```mermaid
flowchart TD
    A[Built-ins for strings]
    A --> B[len]
    A --> C[sorted]
    A --> D[reversed]
    A --> E[enumerate]
    A --> F[ord/chr]
````

!!! tip "Mental Model"
    Because strings are sequences, every built-in that works on sequences---`len()`, `sorted()`, `reversed()`, `enumerate()`---also works on strings, treating each character as an element. `ord()` and `chr()` bridge between characters and their numeric Unicode code points, revealing that every character is ultimately a number.

---

## 1. len()

Returns the number of characters in a string.

```python
text = "Python"
print(len(text))
```

Output:

```text
6
```

---

## 2. str()

Converts values to strings.

```python
x = 42
print(str(x))
```

Output:

```text
42
```

---

## 3. sorted()

Returns a sorted list of characters.

```python
text = "cab"
print(sorted(text))
```

Output:

```text
['a', 'b', 'c']
```

---

## 4. reversed()

Returns characters in reverse order.

```python
text = "abc"
print(list(reversed(text)))
```

Output:

```text
['c', 'b', 'a']
```

---

## 5. enumerate()

Pairs indexes with characters.

```python
for i, ch in enumerate("cat"):
    print(i, ch)
```

Output:

```text
0 c
1 a
2 t
```

---

## 6. ord() and chr()

`ord()` converts a character to its Unicode code point.

`chr()` converts a code point back to a character.

```python
print(ord("A"))
print(chr(65))
```

Output:

```text
65
A
```

---

## 7. Worked Examples

### Example 1: count letters using len

```python
word = "banana"
print(len(word))
```

### Example 2: alphabetical characters

```python
print(sorted("python"))
```

### Example 3: character code

```python
print(ord("z"))
```

---


## 8. Summary

Key ideas:

* many built-ins work naturally with strings
* `len()` measures strings
* `sorted()` and `reversed()` operate on characters
* `enumerate()` pairs indexes with characters
* `ord()` and `chr()` connect characters to Unicode integers

Built-in functions complement string methods and expand what can be done with text.


## Exercises

**Exercise 1.**
`ord()` and `chr()` convert between characters and Unicode code points. Using these functions, explain why `"A" < "a"` is `True` and predict the output:

```python
print(ord("A"), ord("Z"), ord("a"), ord("z"))
print(chr(ord("a") + 3))
print(chr(ord("A") + 32))
```

What is the relationship between uppercase and lowercase ASCII letters in terms of their code points?

??? success "Solution to Exercise 1"
    Output:

    ```text
    65 90 97 122
    d
    a
    ```

    - `ord("A")` = 65, `ord("Z")` = 90: uppercase letters occupy code points 65-90.
    - `ord("a")` = 97, `ord("z")` = 122: lowercase letters occupy code points 97-122.
    - `chr(ord("a") + 3)` = `chr(100)` = `"d"`: shifting by 3 gives the letter 3 positions later.
    - `chr(ord("A") + 32)` = `chr(97)` = `"a"`: the difference between any uppercase and its corresponding lowercase is always 32.

    The relationship: lowercase letters have code points exactly 32 higher than their uppercase counterparts. This is a deliberate ASCII design. `"A" < "a"` is `True` because 65 < 97.

---

**Exercise 2.**
`len()` counts Unicode code points, not visual characters or bytes. Predict the output:

```python
print(len("hello"))
print(len("café"))
print(len("cafe\u0301"))
print(len("hello".encode("utf-8")))
print(len("café".encode("utf-8")))
```

Why do `"café"` and `"cafe\u0301"` display identically but have different lengths? What does `len()` actually count in each context (string vs bytes)?

??? success "Solution to Exercise 2"
    Output:

    ```text
    5
    4
    5
    5
    5
    ```

    `len("hello")` = 5: five ASCII characters, five code points.

    `len("café")` = 4: four code points. The `é` is a single code point (U+00E9, precomposed form).

    `len("cafe\u0301")` = 5: five code points. `\u0301` is a combining acute accent, a separate code point that displays combined with the preceding `e`. Visually identical to `"café"` but one more code point.

    `len("hello".encode("utf-8"))` = 5: five bytes (ASCII characters are one byte each in UTF-8).

    `len("café".encode("utf-8"))` = 5: five bytes. `c`, `a`, `f` are one byte each, but `é` (U+00E9) encodes as two bytes in UTF-8.

    `len()` counts **code points** for `str` objects and **bytes** for `bytes` objects. Neither necessarily corresponds to the number of visual characters (grapheme clusters).

---

**Exercise 3.**
`sorted()` applied to a string returns a list of characters. Explain why `sorted("Banana")` does not produce alphabetical order and predict the output:

```python
print(sorted("Banana"))
print(sorted("Banana", key=str.lower))
print("".join(sorted("Banana", key=str.lower)))
```

Why does `sorted()` return a list instead of a string? How does `"".join(sorted(...))` convert the result back to a string?

??? success "Solution to Exercise 3"
    Output:

    ```text
    ['B', 'a', 'a', 'a', 'n', 'n']
    ['a', 'a', 'a', 'B', 'n', 'n']
    aaaBnn
    ```

    `sorted("Banana")` puts `"B"` first because `ord("B")` = 66 is less than `ord("a")` = 97. Uppercase letters sort before all lowercase letters.

    `sorted("Banana", key=str.lower)` compares `"b"`, `"a"`, `"a"`, `"a"`, `"n"`, `"n"` (lowercase versions), giving alphabetical order. The original characters (including the uppercase `"B"`) are preserved in the output.

    `sorted()` returns a list because strings are immutable -- `sorted()` works on any iterable and always returns a list. `"".join(sorted(...))` converts the list of characters back into a single string by joining them with an empty separator.
