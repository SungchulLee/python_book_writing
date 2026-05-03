
# str Comparison

Strings can be compared for equality and ordering.

Python compares strings **lexicographically**, character by character.

This is similar to dictionary ordering, but it is based on Unicode code points.

```mermaid
flowchart LR
    A[String A] --> C[character-by-character comparison]
    B[String B] --> C
    C --> D[Boolean result]
````

!!! tip "Mental Model"
    String comparison works character by character, left to right, using Unicode code points. The first differing character decides the result. This means uppercase letters sort before lowercase ones (`"A" < "a"`) and digits sort before letters. When case-insensitive comparison is needed, normalize both strings first with `.lower()` or `.casefold()`.

---

## 1. Equality Comparison

Two strings are equal if they contain exactly the same characters in the same order.

```python
print("cat" == "cat")
print("cat" == "Cat")
```

Output:

```text
True
False
```

String comparison is case-sensitive.

---

## 2. Inequality Comparison

```python
print("cat" != "dog")
```

Output:

```text
True
```

---

## 3. Ordering Comparison

Strings can be ordered with `<`, `>`, `<=`, and `>=`.

```python
print("apple" < "banana")
print("cat" > "car")
```

Output:

```text
True
True
```

Comparison proceeds from left to right until a differing character is found.

---

## 4. Case Matters

Uppercase and lowercase letters have different Unicode values.

```python
print("Z" < "a")
```

This may produce a result that surprises beginners.

For user-facing comparisons, normalization is often needed.

```python
print("Cat".lower() == "cat".lower())
```

Output:

```text
True
```

---

## 5. Prefix Effects

Shorter strings can be smaller when one is a prefix of the other.

```python
print("app" < "apple")
```

Output:

```text
True
```

---

## 6. Worked Examples

### Example 1: exact password check

```python
password = "secret"
print(password == "secret")
```

### Example 2: alphabetical order

```python
print("ant" < "bat")
```

### Example 3: case-insensitive comparison

```python
a = "Python"
b = "python"

print(a.lower() == b.lower())
```

---

## 7. Common Pitfalls

### Assuming comparisons ignore case

They do not unless you normalize explicitly.

### Confusing human alphabetical order with Unicode order

Unicode-based comparison is precise, but not always what human sorting expects.

---


## 8. Summary

Key ideas:

* strings support equality and ordering comparisons
* comparisons are lexicographic
* case affects comparison results
* normalization is often needed for user-oriented comparisons

String comparison is essential in searching, sorting, validation, and conditional logic.


## Exercises

**Exercise 1.**
Python compares strings lexicographically by Unicode code point. Predict the output and explain each result:

```python
print("a" < "b")
print("Z" < "a")
print("apple" < "banana")
print("apple" < "application")
print("10" < "9")
```

Why is `"Z" < "a"` `True`? Why is `"10" < "9"` `True`? What common mistake do these results reveal about sorting strings that contain numbers?

??? success "Solution to Exercise 1"
    Output:

    ```text
    True
    True
    True
    True
    True
    ```

    `"a" < "b"`: `ord("a")` = 97, `ord("b")` = 98. 97 < 98, so `True`.

    `"Z" < "a"`: `ord("Z")` = 90, `ord("a")` = 97. All uppercase letters (65-90) have lower code points than lowercase letters (97-122). This is counterintuitive if you expect alphabetical order to be case-insensitive.

    `"apple" < "banana"`: comparison proceeds character by character. `"a"` (97) < `"b"` (98), so the result is determined at the first character.

    `"apple" < "application"`: first 4 characters match. At index 4, `"e"` (101) < `"i"` (105).

    `"10" < "9"`: string comparison compares character by character. `"1"` (49) < `"9"` (57), so `"10"` is "less than" `"9"` as a string. This is why sorting numeric strings alphabetically produces wrong numeric order: `["1", "10", "2", "9"]` instead of `["1", "2", "9", "10"]`. To sort numerically, convert to integers first: `sorted(items, key=int)`.

---

**Exercise 2.**
A programmer sorts a list of names:

```python
names = ["alice", "Bob", "Charlie", "dave"]
print(sorted(names))
print(sorted(names, key=str.lower))
```

Predict both outputs. Why do the results differ? Explain what `key=str.lower` does and why it produces a more intuitive ordering.

??? success "Solution to Exercise 2"
    Output:

    ```text
    ['Bob', 'Charlie', 'alice', 'dave']
    ['alice', 'Bob', 'Charlie', 'dave']
    ```

    The first `sorted()` uses default lexicographic order. Uppercase letters have lower code points than lowercase letters, so `"B"` (66) < `"C"` (67) < `"a"` (97) < `"d"` (100). All capitalized names come before all lowercase names.

    `key=str.lower` tells `sorted()` to compare the lowercase versions of the strings. `"alice"`, `"bob"`, `"charlie"`, `"dave"` are compared, giving alphabetical order. Importantly, the **original** strings (with original capitalization) are returned -- `key` only affects the comparison, not the output.

---

**Exercise 3.**
`==` compares string values, but `is` compares identity. Predict the output:

```python
a = "hello"
b = "hello"
c = "hel" + "lo"
d = "".join(["h", "e", "l", "l", "o"])

print(a == b, a is b)
print(a == c, a is c)
print(a == d, a is d)
```

Why might `a is b` be `True` while `a is d` is `False`, even though all four variables contain `"hello"`? What Python optimization is at work, and why should you never rely on it?

??? success "Solution to Exercise 3"
    Output (CPython):

    ```text
    True True
    True True
    True False
    ```

    All `==` comparisons are `True` because all four variables contain `"hello"`.

    `a is b` is likely `True` because CPython **interns** string literals that look like identifiers. Both `"hello"` literals in the source code are compiled to the same object.

    `a is c` is likely `True` because `"hel" + "lo"` is a compile-time constant expression -- the compiler folds it into `"hello"` and reuses the interned string.

    `a is d` is `False` because `"".join(...)` constructs the string at runtime. The runtime `join()` call creates a new string object that is not interned.

    You should **never** rely on string interning because it is a CPython optimization, not a language guarantee. Other implementations (PyPy, Jython) may intern differently. Always use `==` to compare string values.
