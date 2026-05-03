# Pattern Syntax Basics

!!! tip "Mental Model"
    A regex pattern is read left to right, one token at a time. Most characters match themselves literally; special characters (`.` `*` `+` `?` `^` `$` `|` `\` `[` `]` `(` `)`) have meta-meaning. If you need a special character to match literally, escape it with a backslash. Master these few meta-characters and you can read any regex.

## Literal Characters

The simplest regex patterns are literal characters that match themselves exactly:

```python
import re

re.search(r'cat', 'The cat sat on the mat')
# <re.Match object; span=(4, 7), match='cat'>

re.findall(r'at', 'The cat sat on the mat')
# ['at', 'at', 'at']
```

Most characters match themselves, but certain characters have special meaning in regex and must be escaped with a backslash to match literally.

## Metacharacters

These characters have special meaning in regex:

```
.  ^  $  *  +  ?  {  }  [  ]  \  |  (  )
```

| Metacharacter | Meaning |
|---|---|
| `.` | Match any character except newline |
| `^` | Match the start of the string |
| `$` | Match the end of the string |
| `*` | Zero or more repetitions |
| `+` | One or more repetitions |
| `?` | Zero or one repetition |
| `{m,n}` | Between *m* and *n* repetitions |
| `[]` | Character class (set of characters) |
| `\` | Escape character |
| `\|` | Alternation (OR) |
| `()` | Grouping and capturing |

### The Dot (`.`)

The dot matches **any single character** except a newline:

```python
import re

re.findall(r'c.t', 'cat cot cut c\nt c9t')
# ['cat', 'cot', 'cut', 'c9t']
```

With `re.DOTALL`, the dot also matches newlines:

```python
re.findall(r'c.t', 'cat c\nt', re.DOTALL)
# ['cat', 'c\nt']
```

### Anchors (`^` and `$`)

Anchors match **positions**, not characters:

```python
import re

text = "hello world"

re.search(r'^hello', text)   # Matches — 'hello' is at start
re.search(r'^world', text)   # None — 'world' is not at start
re.search(r'world$', text)   # Matches — 'world' is at end
re.search(r'hello$', text)   # None — 'hello' is not at end
```

With `re.MULTILINE`, `^` and `$` match at the start/end of each **line**:

```python
text = "first line\nsecond line\nthird line"

re.findall(r'^\w+', text)              # ['first']
re.findall(r'^\w+', text, re.M)        # ['first', 'second', 'third']
re.findall(r'\w+$', text, re.M)        # ['line', 'line', 'line']
```

### Alternation (`|`)

The pipe acts as a logical OR:

```python
import re

re.findall(r'cat|dog', 'I have a cat and a dog')
# ['cat', 'dog']

# Alternation applies to the whole expression on each side
re.findall(r'gray|grey', 'gray and grey')
# ['gray', 'grey']

# Use parentheses to limit alternation scope
re.findall(r'gr(a|e)y', 'gray and grey')
# ['a', 'e']  — returns captured groups!

# Non-capturing group to get full match
re.findall(r'gr(?:a|e)y', 'gray and grey')
# ['gray', 'grey']
```

## Escaping Metacharacters

To match a metacharacter literally, precede it with a backslash:

```python
import re

# Match a literal dot
re.findall(r'\.', 'version 3.14.1')
# ['.', '.']

# Match a literal dollar sign
re.search(r'\$\d+', 'Price: \$25')
# <re.Match object; span=(7, 10), match='\$25'>

# Match literal parentheses
re.search(r'\(.*?\)', 'func(arg)')
# <re.Match object; span=(4, 9), match='(arg)'>
```

You can also use `re.escape()` to escape all metacharacters in a string:

```python
special = "price is \$5.00 (USD)"
escaped = re.escape(special)
print(escaped)
# price\ is\ \$5\.00\ \(USD\)
```

This is useful when building patterns from user input.

## Shorthand Character Classes

These shortcuts match common character categories:

| Shorthand | Meaning | Equivalent Class |
|---|---|---|
| `\d` | Any digit | `[0-9]` |
| `\D` | Any non-digit | `[^0-9]` |
| `\w` | Any word character | `[a-zA-Z0-9_]` |
| `\W` | Any non-word character | `[^a-zA-Z0-9_]` |
| `\s` | Any whitespace | `[ \t\n\r\f\v]` |
| `\S` | Any non-whitespace | `[^ \t\n\r\f\v]` |

```python
import re

text = "Agent 007 arrived at 14:30"

re.findall(r'\d+', text)    # ['007', '14', '30']
re.findall(r'\w+', text)    # ['Agent', '007', 'arrived', 'at', '14', '30']
re.findall(r'\s+', text)    # [' ', ' ', ' ', ' ']
```

### Word Boundary (`\b`)

`\b` matches the **boundary** between a word character and a non-word character (or start/end of string). It matches a position, not a character:

```python
import re

text = "cat concatenate category"

re.findall(r'cat', text)     # ['cat', 'cat', 'cat'] — matches inside words
re.findall(r'\bcat\b', text) # ['cat'] — only the standalone word
re.findall(r'\bcat', text)   # ['cat', 'cat'] — words starting with 'cat'
re.findall(r'cat\b', text)   # ['cat', 'cat'] — words ending with 'cat'
```

!!! warning "Word Boundary and Raw Strings"
    Always use raw strings with `\b`. In a regular Python string, `\b` is the backspace character (ASCII 8), not a word boundary.

## Building Patterns Incrementally

Complex patterns are best built step by step:

```python
import re

# Goal: match a date like "2024-01-15"
# Step 1: match four digits
r'\d{4}'

# Step 2: add a hyphen and two digits
r'\d{4}-\d{2}'

# Step 3: complete the pattern
r'\d{4}-\d{2}-\d{2}'

text = "Date: 2024-01-15, updated: 2024-12-31"
re.findall(r'\d{4}-\d{2}-\d{2}', text)
# ['2024-01-15', '2024-12-31']
```

## Summary

| Concept | Key Takeaway |
|---|---|
| Literal characters | Match themselves exactly |
| Metacharacters | `. ^ $ * + ? { } [ ] \ \| ( )` have special meaning |
| `.` (dot) | Matches any character except newline |
| `^` / `$` | Match start/end of string (or line with `re.M`) |
| `\|` | Alternation — logical OR |
| `\` escape | Precede metacharacters with `\` to match literally |
| `\d \w \s` | Shorthand for digit, word, whitespace classes |
| `\b` | Word boundary (position, not character) |

---

## Exercises

**Exercise 1.**
Write a regex pattern that matches a simple IP address format: four groups of 1-3 digits separated by dots (e.g., `192.168.1.1`). Use the dot metacharacter properly (escaped). Test against `"192.168.1.1"`, `"256.1.1.1"`, and `"10.0.0.1"`.

??? success "Solution to Exercise 1"

    ```python
    import re

    pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'

    tests = ["192.168.1.1", "256.1.1.1", "10.0.0.1", "1.2.3"]
    for t in tests:
        match = re.fullmatch(pattern, t)
        print(f"'{t}': {'Match' if match else 'No match'}")
    # Note: this matches format only, not valid ranges (0-255)
    ```

---

**Exercise 2.**
Write a regex using alternation (`|`) that matches either `"cat"`, `"dog"`, or `"bird"` as whole words only. Test it against `"I have a cat and a category"` -- it should match `"cat"` but not the `"cat"` in `"category"`.

??? success "Solution to Exercise 2"

    ```python
    import re

    pattern = r'\b(?:cat|dog|bird)\b'
    text = "I have a cat and a category and a dog"
    matches = re.findall(pattern, text)
    print(matches)  # ['cat', 'dog']
    ```

---

**Exercise 3.**
Write a regex that matches a simple Python variable name: starts with a letter or underscore, followed by zero or more letters, digits, or underscores. Test against `"my_var"`, `"_private"`, `"2invalid"`, `"class"`, and `"hello_world_123"`.

??? success "Solution to Exercise 3"

    ```python
    import re

    pattern = r'^[a-zA-Z_]\w*$'

    tests = ["my_var", "_private", "2invalid", "class", "hello_world_123"]
    for t in tests:
        match = re.fullmatch(pattern, t)
        print(f"'{t}': {'Valid name' if match else 'Invalid'}")
    # 'my_var': Valid name
    # '_private': Valid name
    # '2invalid': Invalid
    # 'class': Valid name (syntactically valid, even if keyword)
    # 'hello_world_123': Valid name
    ```
