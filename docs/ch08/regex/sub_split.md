# sub and split

!!! tip "Mental Model"
    `re.sub` is find-and-replace powered by regex — it locates every match and swaps it with a replacement string (or the return value of a callback function). `re.split` is `str.split` on steroids — it splits a string on a regex pattern instead of a fixed delimiter. Together they handle the two most common text-transformation tasks: replacing and splitting.

## `re.sub()` — Substitution

`re.sub(pattern, repl, string, count=0, flags=0)` replaces all occurrences of the pattern with a replacement string:

```python
import re

text = "Hello World Hello Python"
re.sub(r'Hello', 'Hi', text)
# 'Hi World Hi Python'
```

### Basic Replacement

```python
import re

# Remove all digits
re.sub(r'\d', '', 'Room 404, Floor 3')
# 'Room , Floor '

# Replace whitespace sequences with a single space
re.sub(r'\s+', ' ', 'too   many     spaces')
# 'too many spaces'

# Remove HTML tags
re.sub(r'<[^>]+>', '', '<p>Hello <b>world</b></p>')
# 'Hello world'
```

### Limiting Replacements with `count`

The `count` parameter limits the number of replacements:

```python
import re

text = "aaa bbb ccc aaa bbb"
re.sub(r'aaa', 'xxx', text, count=1)
# 'xxx bbb ccc aaa bbb'
```

### Backreferences in Replacement

The replacement string can reference captured groups using `\1`, `\2`, etc., or `\g<name>` for named groups:

```python
import re

# Swap first and last name
text = "Smith, John"
re.sub(r'(\w+), (\w+)', r'\2 \1', text)
# 'John Smith'

# Using named groups
re.sub(r'(?P<last>\w+), (?P<first>\w+)', r'\g<first> \g<last>', text)
# 'John Smith'

# Surround numbers with brackets
re.sub(r'(\d+)', r'[\1]', 'error 404 at line 52')
# 'error [404] at line [52]'
```

### Function as Replacement

When `repl` is a callable, it receives a `Match` object and returns the replacement string. This enables dynamic replacements:

```python
import re

# Double all numbers
def double_match(match):
    return str(int(match.group()) * 2)

re.sub(r'\d+', double_match, 'score: 42, bonus: 15')
# 'score: 84, bonus: 30'

# Lambda version
re.sub(r'\d+', lambda m: str(int(m.group()) * 2), 'score: 42, bonus: 15')
# 'score: 84, bonus: 30'
```

More complex transformations:

```python
import re

# Convert snake_case to camelCase
def to_camel(match):
    return match.group(1).upper()

text = "my_variable_name"
re.sub(r'_([a-z])', to_camel, text)
# 'myVariableName'

# Censor certain words
words_to_censor = {'bad', 'ugly'}
def censor(match):
    word = match.group()
    if word.lower() in words_to_censor:
        return '*' * len(word)
    return word

re.sub(r'\b\w+\b', censor, 'The bad and the ugly')
# 'The *** and the ****'
```

### `re.subn()`

`re.subn()` works like `re.sub()` but returns a tuple of `(new_string, count)`:

```python
import re

result, count = re.subn(r'\d+', 'NUM', 'error 404 at line 52')
print(result)  # 'error NUM at line NUM'
print(count)   # 2
```

## `re.split()` — Splitting

`re.split(pattern, string, maxsplit=0, flags=0)` splits a string by pattern matches. Unlike `str.split()`, it accepts regex patterns as delimiters.

### Basic Splitting

```python
import re

# Split on one or more whitespace characters
re.split(r'\s+', 'hello   world   python')
# ['hello', 'world', 'python']

# Split on commas with optional surrounding whitespace
re.split(r'\s*,\s*', 'a, b ,c , d')
# ['a', 'b', 'c', 'd']

# Split on multiple delimiter types
re.split(r'[;,\s]+', 'a,b; c  d,e')
# ['a', 'b', 'c', 'd', 'e']
```

### `re.split()` vs `str.split()`

```python
# str.split() — fixed string delimiter
'a, b, c'.split(', ')
# ['a', 'b', 'c']

# But fails with inconsistent spacing
'a, b ,c , d'.split(', ')
# ['a', 'b ,c ', 'd']  — messy!

# re.split() — pattern delimiter handles variation
import re
re.split(r'\s*,\s*', 'a, b ,c , d')
# ['a', 'b', 'c', 'd']  — clean
```

### Limiting Splits with `maxsplit`

```python
import re

re.split(r'\s+', 'one two three four five', maxsplit=2)
# ['one', 'two', 'three four five']
```

### Keeping the Delimiters

When the pattern contains a **capturing group**, the delimiter text is included in the result:

```python
import re

# Without capturing group — delimiters dropped
re.split(r'\d+', 'abc123def456ghi')
# ['abc', 'def', 'ghi']

# With capturing group — delimiters kept
re.split(r'(\d+)', 'abc123def456ghi')
# ['abc', '123', 'def', '456', 'ghi']
```

This is useful when you need to reconstruct the original string or process delimiters:

```python
import re

# Split sentences but keep the punctuation
text = "Hello! How are you? I'm fine."
parts = re.split(r'([.!?])\s*', text)
print(parts)
# ['Hello', '!', 'How are you', '?', "I'm fine", '.', '']
```

### Edge Cases

```python
import re

# Empty strings at boundaries
re.split(r',', ',a,,b,')
# ['', 'a', '', 'b', '']

# Pattern at start/end produces empty strings
re.split(r'\d+', '123abc456')
# ['', 'abc', '']
```

## Practical Examples

### Cleaning Text Data

```python
import re

raw = "  Hello,   World!  This  is   messy   text.  "

# Normalize whitespace
cleaned = re.sub(r'\s+', ' ', raw).strip()
print(cleaned)  # 'Hello, World! This is messy text.'
```

### Parsing CSV with Quoted Fields

```python
import re

line = 'John,"New York, NY",42,"He said ""hello"""'
# Split on commas not inside quotes (simplified)
fields = re.findall(r'(?:"([^"]*(?:""[^"]*)*)"|([^,]+))', line)
print(fields)
```

### Redacting Sensitive Information

```python
import re

text = "SSN: 123-45-6789, Phone: 555-123-4567"

# Redact SSN (keep last 4)
redacted = re.sub(r'\b\d{3}-\d{2}-(\d{4})\b', r'***-**-\1', text)
print(redacted)  # 'SSN: ***-**-6789, Phone: 555-123-4567'
```

### Tokenizing Expressions

```python
import re

expr = "3 + 42 * (x - 7)"
tokens = re.findall(r'\d+|[a-zA-Z_]\w*|[+\-*/()]', expr)
print(tokens)
# ['3', '+', '42', '*', '(', 'x', '-', '7', ')']
```

## Summary

| Function | Purpose | Key Feature |
|---|---|---|
| `re.sub()` | Replace matches | Supports backreferences and callable replacement |
| `re.subn()` | Replace matches | Returns `(result, count)` tuple |
| `re.split()` | Split by pattern | More flexible than `str.split()` |
| `count` param | Limit replacements | `re.sub(..., count=1)` for first only |
| Capturing in split | Keep delimiters | `re.split(r'(\d+)', ...)` |

---

## Exercises

**Exercise 1.**
Use `re.sub` to convert a string from camelCase to snake_case. For example, `"myVariableName"` should become `"my_variable_name"`. Hint: insert an underscore before each uppercase letter and lowercase everything.

??? success "Solution to Exercise 1"

    ```python
    import re

    def camel_to_snake(name):
        result = re.sub(r'([A-Z])', r'_\1', name)
        return result.lower().lstrip('_')

    # Test
    print(camel_to_snake("myVariableName"))   # my_variable_name
    print(camel_to_snake("HTMLParser"))        # h_t_m_l_parser
    print(camel_to_snake("simpleTest"))        # simple_test
    ```

---

**Exercise 2.**
Use `re.split` to split a mathematical expression string into tokens (numbers and operators). For example, `"3+42*7-10/2"` should return `["3", "+", "42", "*", "7", "-", "10", "/", "2"]`. Use a capturing group in the split pattern to keep the delimiters.

??? success "Solution to Exercise 2"

    ```python
    import re

    expression = "3+42*7-10/2"
    tokens = re.split(r'([+\-*/])', expression)
    print(tokens)
    # ['3', '+', '42', '*', '7', '-', '10', '/', '2']
    ```

---

**Exercise 3.**
Use `re.sub` with a replacement function to censor specific words in a text by replacing them with asterisks of the same length. Write a function `censor` that takes a text and a list of words to censor. For example, `censor("The password is secret123", ["password", "secret123"])` should return `"The ******** is *********"`.

??? success "Solution to Exercise 3"

    ```python
    import re

    def censor(text, words):
        for word in words:
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            text = pattern.sub(lambda m: '*' * len(m.group()), text)
        return text

    # Test
    print(censor("The password is secret123", ["password", "secret123"]))
    # The ******** is *********
    ```
