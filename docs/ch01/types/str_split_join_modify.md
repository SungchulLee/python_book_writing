
# str Split, Join, and Modify

Strings often need to be broken apart, recombined, or cleaned up.

This section covers:

- `split()`
- `join()`
- common modification methods

```mermaid
flowchart LR
    A[String] --> B[split()]
    C[List of strings] --> D[join()]
    A --> E[strip/replace methods]
````

!!! tip "Mental Model"
    `split()` and `join()` are inverses: `split()` breaks a string into a list of pieces at a delimiter, and `join()` reassembles a list of strings with a separator between them. Together they form the standard pattern for parsing and rebuilding text. Methods like `.strip()` and `.replace()` handle cleanup by removing whitespace or swapping substrings.

---

## 1. split()

`split()` breaks a string into parts.

```python
text = "red green blue"
parts = text.split()

print(parts)
```

Output:

```text
['red', 'green', 'blue']
```

A separator can also be specified.

```python
data = "a,b,c"
print(data.split(","))
```

Output:

```text
['a', 'b', 'c']
```

---

## 2. join()

`join()` combines a sequence of strings into one string.

```python
words = ["red", "green", "blue"]
result = " ".join(words)

print(result)
```

Output:

```text
red green blue
```

The separator is the string before `.join()`.

```python
print("-".join(words))
```

Output:

```text
red-green-blue
```

---

## 3. strip()

`strip()` removes leading and trailing whitespace.

```python
text = "   hello   "
print(text.strip())
```

You can also use:

* `lstrip()`
* `rstrip()`

---

## 4. replace()

`replace()` substitutes one substring with another.

```python
text = "I like cats"
print(text.replace("cats", "dogs"))
```

Output:

```text
I like dogs
```

---

## 5. Worked Examples

### Example 1: parse CSV-like input

```python
line = "Alice,Bob,Charlie"
names = line.split(",")
print(names)
```

### Example 2: rebuild sentence

```python
words = ["Python", "is", "fun"]
sentence = " ".join(words)
print(sentence)
```

### Example 3: clean input

```python
raw = "   data   "
clean = raw.strip()
print(clean)
```

---

## 6. Common Pitfalls

### Joining non-strings

`join()` requires strings.

```python
# ",".join([1, 2, 3])   # TypeError
```

Convert first if necessary.

### Expecting `split()` to preserve exact formatting

Whitespace splitting collapses runs of spaces when no separator is specified.

---


## 7. Summary

Key ideas:

* `split()` breaks strings into lists
* `join()` combines lists of strings into one string
* `strip()` removes outer whitespace
* `replace()` substitutes text

These methods are central to practical string processing.


## Exercises

**Exercise 1.**
`split()` behaves differently with and without an argument. Predict the output:

```python
text = "  hello   world  "
print(text.split())
print(text.split(" "))
```

Explain why the outputs differ. How does `split()` without arguments handle multiple consecutive spaces and leading/trailing whitespace?

??? success "Solution to Exercise 1"
    Output:

    ```text
    ['hello', 'world']
    ['', '', 'hello', '', '', 'world', '', '']
    ```

    `split()` without arguments uses a special whitespace-splitting algorithm: it strips leading and trailing whitespace, then splits on any run of whitespace characters (spaces, tabs, newlines). Multiple consecutive spaces are treated as a single separator.

    `split(" ")` treats each single space as a separator literally. Multiple consecutive spaces produce empty strings between them. Leading spaces produce empty strings at the start. This is why the second output contains empty strings.

    Rule of thumb: use `split()` (no argument) when you want to split on whitespace in a human-friendly way. Use `split(sep)` with an explicit separator when the exact delimiter matters (e.g., CSV processing).

---

**Exercise 2.**
`split()` and `join()` are inverse operations. Explain why the following does NOT always hold:

```python
text = "  hello   world  "
print(" ".join(text.split()) == text)
```

Under what conditions is `sep.join(s.split(sep)) == s` guaranteed to be `True`? What information is lost when you split and rejoin?

??? success "Solution to Exercise 2"
    Output: `False`.

    `text.split()` gives `['hello', 'world']`, and `" ".join(...)` gives `"hello world"`. The original `"  hello   world  "` had leading spaces, trailing spaces, and multiple spaces between words -- all of this information is lost during `split()`.

    `sep.join(s.split(sep)) == s` is guaranteed to be `True` only when using an **explicit separator**: `",".join("a,b,c".split(","))` gives `"a,b,c"`. With an explicit separator, `split()` preserves all fields including empty ones, and `join()` reconstructs the original exactly.

    With no-argument `split()`, the information lost includes: the exact whitespace characters, the number of consecutive spaces, and any leading/trailing whitespace. This is by design -- no-argument `split()` is a normalization operation, not a lossless parse.

---

**Exercise 3.**
A programmer wants to clean and transform a CSV line:

```python
line = " Alice , 25 , New York "
```

Write code that produces `["Alice", "25", "New York"]` (a list of stripped values). Then write code that produces `"Alice|25|New York"` (values joined by `|`). Explain why you need both `split()` and `strip()` here, and why `split(",")` alone is not sufficient.

??? success "Solution to Exercise 3"
    ```python
    line = " Alice , 25 , New York "

    # Split by comma, then strip each value
    values = [v.strip() for v in line.split(",")]
    print(values)  # ['Alice', '25', 'New York']

    # Rejoin with pipe
    result = "|".join(values)
    print(result)  # "Alice|25|New York"
    ```

    `split(",")` alone gives `[' Alice ', ' 25 ', ' New York ']` -- each value retains its surrounding spaces. The spaces are part of the substrings because `split(",")` only splits on commas, not on whitespace. `strip()` is needed on each value to remove the surrounding spaces.

    The list comprehension `[v.strip() for v in line.split(",")]` is the idiomatic pattern for parsing delimited data where fields may have padding whitespace.
