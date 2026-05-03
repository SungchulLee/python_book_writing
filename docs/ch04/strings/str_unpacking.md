# String Unpacking

Strings are iterable sequences, allowing their characters to be unpacked into individual variables using Python's assignment syntax.

!!! tip "Mental Model"
    A string is just a sequence of single-character strings, so unpacking works exactly like list or tuple unpacking. Each character becomes a separate name binding, and the star operator (`*`) collects leftover characters into a list -- not a string.

## Basic Unpacking

Assign each character of a string to separate variables.

### 1. Simple Assignment

The number of variables must match the string length.

```python
word = "hello"
a, b, c, d, e = word

print(a)  # h
print(b)  # e
print(c)  # l
print(d)  # l
print(e)  # o
```

### 2. Length Mismatch

Unpacking fails if variable count doesn't match string length.

```python
word = "hi"

# Too many variables - ValueError
# a, b, c = word

# Too few variables - ValueError
# a = word  # This works (single assignment)
# a, = word  # ValueError: too many values

# Correct
a, b = word
print(a, b)  # h i
```

### 3. Tuple Context

Parentheses are optional but can improve readability.

```python
word = "abc"

# Without parentheses
a, b, c = word

# With parentheses (equivalent)
(a, b, c) = word

# In expressions
first, second, third = "xyz"
print(first, second, third)  # x y z
```

## Underscore Placeholder

Use `_` to ignore unwanted characters during unpacking.

### 1. Ignoring Positions

Convention uses `_` for values you don't need.

```python
word = "hippo"

# Only need middle character
_, _, c, _, _ = word
print(c)  # p

# Only need first and last
first, _, _, _, last = word
print(first, last)  # h o
```

### 2. Multiple Ignores

Each `_` is a valid variable that gets reassigned.

```python
word = "abcde"

_, _, middle, _, _ = word
print(middle)  # c

# Note: _ is reassigned each time
a, _, _, _, e = word
print(_)  # d (last assigned value)
```

### 3. Readability Trade-off

Too many underscores reduce readability; consider slicing instead.

```python
word = "hello"

# Unpacking approach
_, _, c, d, _ = word

# Slicing approach (often clearer)
c, d = word[2], word[3]
# Or
c, d = word[2:4]
```

## Star Unpacking

Use `*` to collect multiple characters into a list.

### 1. Collect Remaining

Star captures remaining elements as a list.

```python
word = "hello"

first, *rest = word
print(first)  # h
print(rest)   # ['e', 'l', 'l', 'o']

*start, last = word
print(start)  # ['h', 'e', 'l', 'l']
print(last)   # o
```

### 2. Middle Collection

Place star in any position to collect middle elements.

```python
word = "hippo"

first, *middle, last = word
print(first)   # h
print(middle)  # ['i', 'p', 'p']
print(last)    # o

a, b, *rest = word
print(a, b)    # h i
print(rest)    # ['p', 'p', 'o']
```

### 3. Star with Underscore

Combine `*_` to ignore multiple characters.

```python
word = "hello"

# Get only first and last
first, *_, last = word
print(first, last)  # h o

# Get specific positions
_, _, *middle, _ = word
print(middle)  # ['l', 'l']

# Ignore everything except last two
*_, second_last, last = word
print(second_last, last)  # l o
```

## Type Behavior

Understand what unpacking produces.

### 1. Variables Are Strings

Individual unpacked characters are single-character strings.

```python
word = "abc"
a, b, c = word

print(type(a))  # <class 'str'>
print(len(a))   # 1
print(a == "a") # True
```

### 2. Star Produces List

Star unpacking always produces a list, not a string.

```python
word = "hello"

first, *rest = word
print(type(rest))  # <class 'list'>
print(rest)        # ['e', 'l', 'l', 'o']

# Convert back to string if needed
rest_str = "".join(rest)
print(rest_str)    # ello
```

### 3. Empty Star Result

Star can capture zero elements, producing empty list.

```python
word = "ab"

first, *middle, last = word
print(first)   # a
print(middle)  # [] (empty list)
print(last)    # b

# Minimum: star needs at least 0 elements
a, *b, c = "xy"
print(b)  # []
```

## Practical Patterns

Common use cases for string unpacking.

### 1. Swap Characters

Unpack and repack to rearrange.

```python
def swap_ends(s):
    """Swap first and last characters."""
    if len(s) < 2:
        return s
    first, *middle, last = s
    return last + "".join(middle) + first

print(swap_ends("hello"))  # oellh
print(swap_ends("ab"))     # ba
```

### 2. Parse Fixed Format

Unpack strings with known structure.

```python
# Date string YYYYMMDD
date_str = "20250112"
y1, y2, y3, y4, m1, m2, d1, d2 = date_str
year = y1 + y2 + y3 + y4
month = m1 + m2
day = d1 + d2
print(f"{year}-{month}-{day}")  # 2025-01-12

# Simpler with slicing for this case
year, month, day = date_str[:4], date_str[4:6], date_str[6:]
```

### 3. Iteration Unpacking

Unpack during iteration over strings.

```python
pairs = ["ab", "cd", "ef"]

for first, second in pairs:
    print(f"{first} -> {second}")
# a -> b
# c -> d
# e -> f

# With enumerate
word = "abc"
for i, char in enumerate(word):
    print(f"{i}: {char}")
```

## Limitations

Understand unpacking constraints.

### 1. Single Star Only

Only one starred expression is allowed.

```python
word = "hello"

# Valid
first, *middle, last = word

# Invalid - multiple stars
# *start, middle, *end = word  # SyntaxError
```

### 2. Minimum Variables

Need at least as many non-star variables as required.

```python
# Need minimum 2 characters for this pattern
first, *middle, last = "ab"  # Works
# first, *middle, last = "a"   # ValueError

# Star alone works with any length
*all_chars, = "a"
print(all_chars)  # ['a']
```

### 3. Performance Note

Unpacking creates new objects; for large strings, consider slicing.

```python
# For large strings, slicing is more efficient
large = "a" * 10000

# Creates 10000 string objects
# a, *rest = large  # Slow

# Creates just one new string
first = large[0]
rest = large[1:]   # Fast
```

---

## Exercises

**Exercise 1.**
String unpacking treats each character as a separate element. Predict the output:

```python
a, b, c = "abc"
print(a, b, c)
print(type(a))

x, *y = "hello"
print(x)
print(y)
print(type(y))
```

Why is `type(a)` `str` and not `char`? Why is `type(y)` `list` even though we unpacked a string?

??? success "Solution to Exercise 1"
    Output:

    ```text
    a b c
    <class 'str'>
    h
    ['e', 'l', 'l', 'o']
    <class 'list'>
    ```

    Python has no `char` type. When you index or unpack a string, each element is a **string of length 1**. `"abc"[0]` is `"a"` (a `str`), not a character primitive.

    `*y` produces a **list** because starred unpacking always creates a list, regardless of the source type. Even though we unpacked a string, `y` is `['e', 'l', 'l', 'o']`. This is a design choice: the starred variable needs to be a mutable container that can hold any number of elements, and `list` is the natural choice.

---

**Exercise 2.**
Unpacking can fail if the number of variables does not match. Predict which lines succeed and which raise errors:

```python
# Line 1
a, b = "hi"

# Line 2
a, b, c = "hi"

# Line 3
a, *b = "hi"

# Line 4
*a, = "h"

# Line 5
a, b = "h"
```

What is the minimum number of characters needed for each unpacking pattern?

??? success "Solution to Exercise 2"
    - Line 1: **Succeeds**. `"hi"` has 2 characters, 2 variables.
    - Line 2: **ValueError**: not enough values to unpack. `"hi"` has 2 characters, 3 variables needed.
    - Line 3: **Succeeds**. `a = "h"`, `b = ["i"]`. Starred variables absorb remaining elements.
    - Line 4: **Succeeds**. `a = ["h"]`. A lone starred variable with a trailing comma unpacks everything into a list.
    - Line 5: **ValueError**: not enough values to unpack. `"h"` has 1 character, 2 variables needed.

    Minimum characters: for `n` non-starred variables, you need exactly `n` characters (without `*`) or at least `n` characters (with `*`). The starred variable can absorb zero or more elements.

---

**Exercise 3.**
Extended unpacking with `*` always produces a list. Predict the output:

```python
first, *middle, last = "abcde"
print(first, middle, last)

first, *middle, last = "ab"
print(first, middle, last)

# Can you unpack into a single starred variable?
*everything, = "abc"
print(everything)
print("".join(everything))
```

Why does `*middle` produce `[]` when unpacking `"ab"`? What is the relationship between starred unpacking and slicing?

??? success "Solution to Exercise 3"
    Output:

    ```text
    a ['b', 'c', 'd'] e
    a [] b
    ['a', 'b', 'c']
    abc
    ```

    `*middle` produces `[]` when unpacking `"ab"` because `first` claims `"a"` and `last` claims `"b"`, leaving nothing for `middle`. The starred variable gracefully handles the empty case by producing an empty list.

    Starred unpacking is conceptually similar to slicing: `first, *middle, last = s` is like `first = s[0]; middle = list(s[1:-1]); last = s[-1]`. The difference is that unpacking also works with arbitrary iterables (not just sequences) and always produces a list for the starred variable.
