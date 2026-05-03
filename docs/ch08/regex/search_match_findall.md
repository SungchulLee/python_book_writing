# search, match, findall

!!! tip "Mental Model"
    `search` scans the entire string for the first match anywhere. `match` only checks at the very beginning of the string. `findall` collects every non-overlapping match into a list. Choosing the right function is the first decision in any regex task: "Do I need the first occurrence, a start-of-string check, or all occurrences?"

## Overview

Python's `re` module provides several functions for finding patterns in text. The three most commonly used are `search()`, `match()`, and `findall()`, each with distinct behavior.

| Function | Searches Where | Returns | Use Case |
|---|---|---|---|
| `re.search()` | Anywhere in string | First `Match` or `None` | Find first occurrence |
| `re.match()` | Beginning of string only | `Match` or `None` | Validate string start |
| `re.fullmatch()` | Entire string | `Match` or `None` | Validate entire string |
| `re.findall()` | Entire string | List of strings/tuples | Extract all occurrences |
| `re.finditer()` | Entire string | Iterator of `Match` objects | Process matches one by one |

## `re.search()`

`re.search()` scans the **entire string** and returns the **first** match:

```python
import re

text = "Error 404: Page not found at 14:30"

# Finds the first sequence of digits
match = re.search(r'\d+', text)
print(match.group())  # '404'
print(match.span())   # (6, 9)
```

If no match exists, it returns `None`:

```python
match = re.search(r'\d+', 'no numbers here')
print(match)  # None
```

### Common Pattern: Guard with `if`

```python
import re

text = "Temperature: 72.5°F"
match = re.search(r'([\d.]+)°([FC])', text)

if match:
    value = float(match.group(1))
    unit = match.group(2)
    print(f"{value} degrees {unit}")  # 72.5 degrees F
```

### Walrus Operator (Python 3.8+)

The walrus operator `:=` combines the search and check in one expression:

```python
import re

text = "Price: \$42.99"
if m := re.search(r'\$(\d+\.\d{2})', text):
    print(f"Found price: {m.group(1)}")  # Found price: 42.99
```

## `re.match()`

`re.match()` checks for a match **only at the beginning** of the string:

```python
import re

# Matches — pattern is at the start
re.match(r'\d+', '123abc')
# <re.Match object; span=(0, 3), match='123'>

# No match — digits are not at the start
re.match(r'\d+', 'abc123')
# None
```

### `match()` vs `search()` with `^`

`re.match()` is equivalent to `re.search()` with a `^` anchor:

```python
import re

text = "hello world"

# These are equivalent
re.match(r'hello', text)          # Match
re.search(r'^hello', text)        # Match

# These differ
re.match(r'world', text)          # None — not at start
re.search(r'world', text)         # Match — found in string
```

!!! tip "When to Use `match()` vs `search()`"
    Use `re.match()` when you specifically need to validate the **beginning** of a string. Use `re.search()` for general-purpose pattern finding anywhere in the string. In practice, `re.search()` is more commonly used.

## `re.fullmatch()`

`re.fullmatch()` requires the pattern to match the **entire string** (equivalent to anchoring with `^...$`):

```python
import re

# Validate that the entire string is a date
re.fullmatch(r'\d{4}-\d{2}-\d{2}', '2024-01-15')
# <re.Match object; match='2024-01-15'>

re.fullmatch(r'\d{4}-\d{2}-\d{2}', '2024-01-15 extra')
# None — extra text after the date
```

`fullmatch()` is ideal for **input validation**:

```python
import re

def is_valid_email_simple(email):
    """Basic email format check (not production-grade)."""
    return bool(re.fullmatch(r'[\w.+-]+@[\w-]+\.[\w.]+', email))

print(is_valid_email_simple("user@example.com"))     # True
print(is_valid_email_simple("not an email"))          # False
print(is_valid_email_simple("user@example.com foo"))  # False
```

## `re.findall()`

`re.findall()` returns a **list** of all non-overlapping matches:

```python
import re

text = "Prices: \$10, \$25, $100, and \$3.50"

# No groups — returns list of full matches
re.findall(r'\$[\d.]+', text)
# ['\$10', '\$25', '\$100', '\$3.50']

# One group — returns list of group contents
re.findall(r'\$([\d.]+)', text)
# ['10', '25', '100', '3.50']

# Multiple groups — returns list of tuples
re.findall(r'\$(\d+)\.?(\d*)', text)
# [('10', ''), ('25', ''), ('100', ''), ('3', '50')]
```

### `findall()` with No Match

If no matches are found, `findall()` returns an empty list (not `None`):

```python
result = re.findall(r'\d+', 'no numbers')
print(result)       # []
print(len(result))  # 0
print(bool(result)) # False
```

## `re.finditer()`

`re.finditer()` returns an **iterator** of `Match` objects, giving you access to all match metadata (position, groups):

```python
import re

text = "Alice: 85, Bob: 92, Carol: 78"

for match in re.finditer(r'(\w+): (\d+)', text):
    name = match.group(1)
    score = int(match.group(2))
    pos = match.span()
    print(f"{name} scored {score} (at position {pos})")
# Alice scored 85 (at position (0, 9))
# Bob scored 92 (at position (11, 17))
# Carol scored 78 (at position (19, 28))
```

### `finditer()` vs `findall()`

Use `finditer()` when you need:

- The **position** of each match (`.start()`, `.end()`, `.span()`)
- Named groups (`.groupdict()`)
- Memory efficiency with large texts (lazy iteration)
- Both the full match and group contents

```python
import re

text = "2024-01-15 and 2024-12-31"

# findall — only group contents
re.findall(r'(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})', text)
# [('2024', '01', '15'), ('2024', '12', '31')]

# finditer — full Match objects
for m in re.finditer(r'(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})', text):
    print(m.group(0), m.groupdict())
# 2024-01-15 {'y': '2024', 'm': '01', 'd': '15'}
# 2024-12-31 {'y': '2024', 'm': '12', 'd': '31'}
```

## Comparison Table

```python
import re

text = "cat bat hat"
pattern = r'[cbh]at'

# search — first match only
re.search(pattern, text).group()        # 'cat'

# findall — all matches as list
re.findall(pattern, text)               # ['cat', 'bat', 'hat']

# finditer — all matches as Match objects
[m.group() for m in re.finditer(pattern, text)]  # ['cat', 'bat', 'hat']

# match — beginning of string only
re.match(pattern, text).group()         # 'cat'

# fullmatch — entire string
re.fullmatch(pattern, text)             # None (text has spaces)
re.fullmatch(pattern, 'cat')           # <re.Match ...>
```

## Summary

| Function | Scope | Returns | Best For |
|---|---|---|---|
| `search()` | First match anywhere | `Match` / `None` | Finding first occurrence |
| `match()` | Start of string | `Match` / `None` | Validating beginning |
| `fullmatch()` | Entire string | `Match` / `None` | Input validation |
| `findall()` | All matches | `list` | Extracting all occurrences |
| `finditer()` | All matches | Iterator of `Match` | Position-aware extraction |

---

## Exercises

**Exercise 1.**
Write a function `validate_email` that uses `re.fullmatch` to check if a string is a valid email address (simplified pattern). Return `True` or `False`. Test with `"user@example.com"`, `"@invalid.com"`, `"user@.com"`, and `"name@domain.org"`.

??? success "Solution to Exercise 1"

    ```python
    import re

    def validate_email(email):
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return bool(re.fullmatch(pattern, email))

    # Test
    print(validate_email("user@example.com"))  # True
    print(validate_email("@invalid.com"))       # False
    print(validate_email("user@.com"))          # False
    print(validate_email("name@domain.org"))    # True
    ```

---

**Exercise 2.**
Write a function `find_all_hashtags` that uses `re.findall` to extract all hashtags from a social media post. A hashtag starts with `#` followed by one or more word characters. For example, `"Love #Python and #coding! #100DaysOfCode"` should return `["#Python", "#coding", "#100DaysOfCode"]`.

??? success "Solution to Exercise 2"

    ```python
    import re

    def find_all_hashtags(text):
        return re.findall(r'#\w+', text)

    # Test
    post = "Love #Python and #coding! #100DaysOfCode"
    print(find_all_hashtags(post))
    # ['#Python', '#coding', '#100DaysOfCode']
    ```

---

**Exercise 3.**
Write a function `search_vs_match_demo` that takes a pattern and a string, and returns a dictionary with keys `"search"`, `"match"`, and `"fullmatch"`, each containing `True` or `False` depending on whether the respective function found a match. Demonstrate with the pattern `r"\d+"` and the string `"abc123"`.

??? success "Solution to Exercise 3"

    ```python
    import re

    def search_vs_match_demo(pattern, text):
        return {
            "search": bool(re.search(pattern, text)),
            "match": bool(re.match(pattern, text)),
            "fullmatch": bool(re.fullmatch(pattern, text)),
        }

    # Test
    result = search_vs_match_demo(r"\d+", "abc123")
    print(result)
    # {'search': True, 'match': False, 'fullmatch': False}

    result2 = search_vs_match_demo(r"\d+", "123")
    print(result2)
    # {'search': True, 'match': True, 'fullmatch': True}
    ```
