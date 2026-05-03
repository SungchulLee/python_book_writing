
# str Examples

This section gathers practical examples showing how string operations work together.

!!! tip "Mental Model"
    These examples show how individual string skills---formatting, slicing, methods, membership testing---combine to solve real tasks. Each example is a small program that uses multiple string operations together, building the habit of thinking in terms of composable string tools rather than isolated methods.

---

## 1. Greeting Message

```python
name = "Alice"
message = f"Hello, {name}!"

print(message)
````

Output:

```text
Hello, Alice!
```

---

## 2. Username Validation

```python
username = "user123"

if username.isalnum():
    print("valid username")
else:
    print("invalid username")
```

---

## 3. Word Count

```python
sentence = "Python is fun"
words = sentence.split()

print(len(words))
```

Output:

```text
3
```

---

## 4. Reverse a String

```python
text = "Python"
print(text[::-1])
```

Output:

```text
nohtyP
```

---

## 5. CSV-Like Parsing

```python
line = "red,green,blue"
colors = line.split(",")

print(colors)
```

Output:

```text
['red', 'green', 'blue']
```

---

## 6. Rebuilding Text

```python
words = ["Python", "is", "readable"]
sentence = " ".join(words)

print(sentence)
```

Output:

```text
Python is readable
```

---

## 7. Case Normalization

```python
a = "PYTHON"
b = "python"

if a.lower() == b.lower():
    print("same word")
```

---

## 8. Path Example with Raw String

```python
path = r"C:\Users\student\notes.txt"
print(path)
```

---

## 9. Summary

These examples show that strings are used for:

* storing text
* formatting messages
* validating input
* parsing data
* transforming textual information

String processing is one of the most important programming skills in Python.

## Exercises

**Exercise 1.**
Predict the output of each expression, then verify in the REPL.

```python
>>> "Python"[0] + "Python"[-1]
>>> "hello world".title()
>>> "abcabc".count("bc")
>>> "  spaces  ".strip()
```

??? success "Solution to Exercise 1"
    ```python
    >>> "Python"[0] + "Python"[-1]
    'Pn'
    >>> "hello world".title()
    'Hello World'
    >>> "abcabc".count("bc")
    2
    >>> "  spaces  ".strip()
    'spaces'
    ```

    `"Python"[0]` is `'P'` and `"Python"[-1]` is `'n'`; concatenation gives `'Pn'`. The `title()` method capitalizes the first letter of each word. `count("bc")` finds two non-overlapping occurrences. `strip()` removes leading and trailing whitespace.

---

**Exercise 2.**
Write a function `is_palindrome(s)` that returns `True` if the string `s` reads the same forwards and backwards (case-insensitive, ignoring spaces). Test with `"Race Car"` and `"Hello"`.

??? success "Solution to Exercise 2"
    ```python
    def is_palindrome(s):
        cleaned = s.lower().replace(" ", "")
        return cleaned == cleaned[::-1]

    print(is_palindrome("Race Car"))  # True
    print(is_palindrome("Hello"))     # False
    ```

    The function converts to lowercase and removes spaces, then compares the string with its reverse using the `[::-1]` slice. `"racecar"` reversed is `"racecar"`, so it is a palindrome. `"hello"` reversed is `"olleh"`, so it is not.

---

**Exercise 3.**
Given the string `data = "Alice:30:Paris,Bob:25:London,Carol:35:Tokyo"`, write code that parses it into a list of dictionaries with keys `"name"`, `"age"`, and `"city"`.

??? success "Solution to Exercise 3"
    ```python
    data = "Alice:30:Paris,Bob:25:London,Carol:35:Tokyo"
    records = []

    for entry in data.split(","):
        name, age, city = entry.split(":")
        records.append({"name": name, "age": int(age), "city": city})

    print(records)
    ```

    Output:

    ```
    [{'name': 'Alice', 'age': 30, 'city': 'Paris'},
     {'name': 'Bob', 'age': 25, 'city': 'London'},
     {'name': 'Carol', 'age': 35, 'city': 'Tokyo'}]
    ```

    The outer `split(",")` separates the records. The inner `split(":")` separates the fields within each record. `int(age)` converts the age string to an integer.

---

**Exercise 4.**
Explain why `"python" < "java"` evaluates to `False` even though `"python"` comes after `"java"` alphabetically. What comparison does Python actually perform?

??? success "Solution to Exercise 4"
    ```python
    >>> "python" < "java"
    False
    ```

    Python compares strings **lexicographically** using the Unicode code points of each character, comparing character by character from left to right.

    - `'p'` has Unicode code point 112
    - `'j'` has Unicode code point 106

    Since `112 > 106`, `"python"` is **greater than** `"java"` in lexicographic order, so `"python" < "java"` is `False`.

    This comparison does correspond to alphabetical order for lowercase ASCII letters because their code points are in alphabetical sequence (`a=97, b=98, ..., z=122`). However, uppercase letters have lower code points (`A=65, ..., Z=90`), so `"Java" < "python"` would be `True` because `'J'` (74) < `'p'` (112).

---

**Exercise 5.**
Write a function `censor(text, word)` that replaces every occurrence of `word` in `text` with asterisks of the same length. For example, `censor("the cat sat on the mat", "cat")` should return `"the *** sat on the mat"`.

??? success "Solution to Exercise 5"
    ```python
    def censor(text, word):
        return text.replace(word, "*" * len(word))

    print(censor("the cat sat on the mat", "cat"))
    print(censor("banana banana", "banana"))
    ```

    Output:

    ```
    the *** sat on the mat
    ****** ******
    ```

    `"*" * len(word)` creates a string of asterisks with the same length as the censored word. `str.replace` substitutes all occurrences. For `"cat"` (length 3), the replacement is `"***"`. For `"banana"` (length 6), the replacement is `"******"`.

