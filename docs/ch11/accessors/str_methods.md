# String Methods Reference

Complete reference for all string methods available through the pandas `str` accessor.

!!! tip "Mental Model"
    This page is a lookup table: given a string task (change case, find a substring, split, pad), find the matching `.str` method. Every method here mirrors a built-in Python string method but operates on an entire Series at once, with automatic NaN handling baked in.

## Case Methods

| Method | Description | Example |
|--------|-------------|---------|
| `str.lower()` | Convert to lowercase | `'HELLO'` → `'hello'` |
| `str.upper()` | Convert to uppercase | `'hello'` → `'HELLO'` |
| `str.title()` | Titlecase (capitalize each word) | `'hello world'` → `'Hello World'` |
| `str.capitalize()` | Capitalize first character | `'hello'` → `'Hello'` |
| `str.swapcase()` | Swap case | `'Hello'` → `'hELLO'` |
| `str.casefold()` | Aggressive lowercase (for caseless matching) | `'STRASSE'` → `'strasse'` |

```python
import pandas as pd

s = pd.Series(['hello WORLD', 'PYTHON pandas'])

print(s.str.lower())      # hello world, python pandas
print(s.str.upper())      # HELLO WORLD, PYTHON PANDAS
print(s.str.title())      # Hello World, Python Pandas
print(s.str.capitalize()) # Hello world, Python pandas
print(s.str.swapcase())   # HELLO world, python PANDAS
```

## Alignment Methods

| Method | Description | Parameters |
|--------|-------------|------------|
| `str.center(width)` | Center align | `width`, `fillchar=' '` |
| `str.ljust(width)` | Left align | `width`, `fillchar=' '` |
| `str.rjust(width)` | Right align | `width`, `fillchar=' '` |
| `str.zfill(width)` | Pad with zeros on left | `width` |
| `str.pad(width)` | Pad string | `width`, `side='left'`, `fillchar=' '` |

```python
s = pd.Series(['a', 'bb', 'ccc'])

print(s.str.center(5, '_'))  # __a__, _bb__, _ccc_
print(s.str.ljust(5, '_'))   # a____, bb___, ccc__
print(s.str.rjust(5, '_'))   # ____a, ___bb, __ccc
print(s.str.zfill(5))        # 0000a, 000bb, 00ccc
```

## Splitting Methods

| Method | Description | Parameters |
|--------|-------------|------------|
| `str.split(pat)` | Split by delimiter | `pat`, `n=-1`, `expand=False` |
| `str.rsplit(pat)` | Split from right | `pat`, `n=-1`, `expand=False` |
| `str.partition(sep)` | Split at first occurrence | `sep` |
| `str.rpartition(sep)` | Split at last occurrence | `sep` |

```python
s = pd.Series(['a-b-c-d', 'x-y-z'])

# Split all
print(s.str.split('-'))
# [['a', 'b', 'c', 'd'], ['x', 'y', 'z']]

# Split with limit
print(s.str.split('-', n=2))
# [['a', 'b', 'c-d'], ['x', 'y', 'z']]

# Expand into columns
print(s.str.split('-', expand=True))
#    0  1     2     3
# 0  a  b     c     d
# 1  x  y     z  None
```

## Joining Methods

| Method | Description | Parameters |
|--------|-------------|------------|
| `str.join(sep)` | Join list elements | `sep` |
| `str.cat()` | Concatenate strings | `others`, `sep`, `na_rep` |

```python
# Join lists
s = pd.Series([['a', 'b', 'c'], ['x', 'y']])
print(s.str.join('-'))  # a-b-c, x-y

# Concatenate all strings
s = pd.Series(['A', 'B', 'C'])
print(s.str.cat(sep='-'))  # A-B-C

# Concatenate with another Series
s1 = pd.Series(['A', 'B', 'C'])
s2 = pd.Series(['1', '2', '3'])
print(s1.str.cat(s2, sep='-'))  # A-1, B-2, C-3
```

## Stripping Methods

| Method | Description | Parameters |
|--------|-------------|------------|
| `str.strip()` | Strip both sides | `to_strip=None` |
| `str.lstrip()` | Strip left side | `to_strip=None` |
| `str.rstrip()` | Strip right side | `to_strip=None` |

```python
s = pd.Series(['  hello  ', '***world***'])

print(s.str.strip())      # 'hello', '***world***'
print(s.str.strip('* '))  # 'hello', 'world'
print(s.str.lstrip('* ')) # 'hello  ', 'world***'
```

## Search Methods

| Method | Description | Returns |
|--------|-------------|---------|
| `str.contains(pat)` | Contains pattern | bool Series |
| `str.startswith(pat)` | Starts with pattern | bool Series |
| `str.endswith(pat)` | Ends with pattern | bool Series |
| `str.match(pat)` | Match regex at start | bool Series |
| `str.fullmatch(pat)` | Full string matches regex | bool Series |
| `str.find(sub)` | Find substring position | int Series (-1 if not found) |
| `str.rfind(sub)` | Find from right | int Series |
| `str.index(sub)` | Find (raises if not found) | int Series |
| `str.rindex(sub)` | Find from right (raises) | int Series |
| `str.count(pat)` | Count occurrences | int Series |

```python
s = pd.Series(['apple', 'banana', 'cherry'])

print(s.str.contains('an'))    # False, True, False
print(s.str.startswith('a'))   # True, False, False
print(s.str.endswith('a'))     # False, True, False
print(s.str.find('a'))         # 0, 1, -1
print(s.str.count('a'))        # 1, 3, 0
```

### contains() Parameters

```python
s = pd.Series(['Apple', 'BANANA', None, 'cherry'])

# Case sensitivity
print(s.str.contains('a', case=True))   # False, False, NaN, True
print(s.str.contains('a', case=False))  # True, True, NaN, True

# Handle NA
print(s.str.contains('a', na=False))    # False, False, False, True
print(s.str.contains('a', na=True))     # False, False, True, True

# Regex
print(s.str.contains(r'^[A-Z]', regex=True))  # True, True, NaN, False
```

## Replacement Methods

| Method | Description | Parameters |
|--------|-------------|------------|
| `str.replace(pat, repl)` | Replace pattern | `pat`, `repl`, `n=-1`, `case=None`, `regex=True` |
| `str.translate(table)` | Translate via mapping | `table` |
| `str.slice_replace()` | Replace positional slice | `start`, `stop`, `repl` |

```python
s = pd.Series(['apple-pie', 'banana-split'])

# Simple replace
print(s.str.replace('-', '_'))
# apple_pie, banana_split

# Regex replace
print(s.str.replace(r'-\w+', '', regex=True))
# apple, banana

# Replace with callable
print(s.str.replace(r'(\w+)-(\w+)', lambda m: m.group(2), regex=True))
# pie, split
```

## Extraction Methods

| Method | Description | Returns |
|--------|-------------|---------|
| `str.extract(pat)` | Extract first match | DataFrame |
| `str.extractall(pat)` | Extract all matches | DataFrame (MultiIndex) |
| `str.findall(pat)` | Find all matches | Series of lists |

```python
s = pd.Series(['A-123', 'B-456', 'C-789'])

# Extract with groups
print(s.str.extract(r'([A-Z])-(\d+)'))
#    0    1
# 0  A  123
# 1  B  456
# 2  C  789

# Find all digits
s = pd.Series(['a1b2c3', 'x9'])
print(s.str.findall(r'\d'))
# [['1', '2', '3'], ['9']]
```

## Slicing Methods

| Method | Description | Parameters |
|--------|-------------|------------|
| `str[start:stop]` | Slice by position | start, stop, step |
| `str.slice(start, stop)` | Slice by position | `start`, `stop`, `step` |
| `str.get(i)` | Get character at position | `i` |

```python
s = pd.Series(['hello', 'world'])

print(s.str[0])       # h, w
print(s.str[:3])      # hel, wor
print(s.str[-2:])     # lo, ld
print(s.str.get(0))   # h, w (NaN-safe)
```

## Length and Size

| Method | Description | Returns |
|--------|-------------|---------|
| `str.len()` | Length of string | int Series |

```python
s = pd.Series(['hello', 'world', 'python'])
print(s.str.len())  # 5, 5, 6
```

## Encoding Methods

| Method | Description | Parameters |
|--------|-------------|------------|
| `str.encode(encoding)` | Encode to bytes | `encoding`, `errors` |
| `str.decode(encoding)` | Decode from bytes | `encoding`, `errors` |

```python
s = pd.Series(['hello', 'world'])
encoded = s.str.encode('utf-8')
print(encoded)  # b'hello', b'world'
```

## Checking Methods

| Method | Description | Returns |
|--------|-------------|---------|
| `str.isalpha()` | All alphabetic | bool Series |
| `str.isalnum()` | All alphanumeric | bool Series |
| `str.isdigit()` | All digits | bool Series |
| `str.isnumeric()` | All numeric | bool Series |
| `str.isdecimal()` | All decimal | bool Series |
| `str.isspace()` | All whitespace | bool Series |
| `str.islower()` | All lowercase | bool Series |
| `str.isupper()` | All uppercase | bool Series |
| `str.istitle()` | Titlecase | bool Series |

```python
s = pd.Series(['hello', 'HELLO', 'Hello', '12345', 'hello123'])

print(s.str.isalpha())    # True, True, True, False, False
print(s.str.isalnum())    # True, True, True, True, True
print(s.str.isdigit())    # False, False, False, True, False
print(s.str.islower())    # True, False, False, False, True
print(s.str.isupper())    # False, True, False, False, False
print(s.str.istitle())    # False, False, True, False, False
```

## Wrapping and Normalization

| Method | Description | Parameters |
|--------|-------------|------------|
| `str.wrap(width)` | Wrap text | `width` |
| `str.normalize(form)` | Unicode normalization | `form` (NFC, NFD, NFKC, NFKD) |

```python
s = pd.Series(['This is a very long string that needs to be wrapped'])
print(s.str.wrap(20))
```

## Regular Expression Flags

For methods that support regex, you can use flags:

```python
import re

s = pd.Series(['Hello World', 'HELLO world'])

# Case insensitive
print(s.str.contains('hello', flags=re.IGNORECASE))  # True, True

# Multiline, dotall, etc.
s = pd.Series(['line1\nline2'])
print(s.str.contains('^line2', flags=re.MULTILINE))  # True
```

## Handling Missing Data

All str methods handle NaN gracefully:

```python
s = pd.Series(['hello', None, 'world'])

print(s.str.upper())
# HELLO, NaN, WORLD

print(s.str.len())
# 5, NaN, 5
```

## Method Chaining Example

```python
# Complex text processing pipeline
s = pd.Series(['  JOHN DOE  ', '  jane SMITH  ', '  BOB wilson  '])

result = (s
    .str.strip()           # Remove whitespace
    .str.title()           # Titlecase
    .str.replace(' ', '_') # Replace spaces
)
print(result)
# John_Doe, Jane_Smith, Bob_Wilson
```

## Performance Notes

1. **Vectorized operations** are faster than apply() with lambda
2. **Avoid chaining** too many operations; intermediate Series are created
3. **Use `regex=False`** when not needed for better performance
4. **Consider `str.contains(..., regex=False)`** for literal string search

---

## Exercises

**Exercise 1.**
Given a Series of product descriptions, use `.str.extract()` with a regex pattern to pull out all numeric values (prices) embedded in strings like `'Widget costs 29.99 dollars'` and `'Gadget is 14.50 on sale'`.

??? success "Solution to Exercise 1"
    Use `.str.extract()` with a pattern for decimal numbers.

        import pandas as pd

        descriptions = pd.Series([
            'Widget costs 29.99 dollars',
            'Gadget is 14.50 on sale',
            'Tool priced at 5.00'
        ])
        prices = descriptions.str.extract(r'(\d+\.\d+)')[0].astype(float)
        print(prices)

---

**Exercise 2.**
Given a Series of full addresses like `'123 Main St, New York, NY 10001'`, use `.str.split(',')` to break each address into parts. Then use `.str.get()` or bracket indexing to extract only the city (second element) and strip whitespace from it.

??? success "Solution to Exercise 2"
    Split on comma and extract the second element.

        import pandas as pd

        addresses = pd.Series([
            '123 Main St, New York, NY 10001',
            '456 Oak Ave, Los Angeles, CA 90001',
            '789 Pine Rd, Chicago, IL 60601'
        ])
        cities = addresses.str.split(',').str[1].str.strip()
        print(cities)

---

**Exercise 3.**
Given a Series of filenames like `['report_2024.pdf', 'data_2023.csv', 'notes_2024.txt']`, use `.str.endswith()` to filter only `.csv` files, and use `.str.replace()` with regex to extract the year from each filename.

??? success "Solution to Exercise 3"
    Combine `.str.endswith()` for filtering and `.str.extract()` for the year.

        import pandas as pd

        filenames = pd.Series(['report_2024.pdf', 'data_2023.csv', 'notes_2024.txt'])
        csv_files = filenames[filenames.str.endswith('.csv')]
        print("CSV files:", csv_files.tolist())

        years = filenames.str.extract(r'(\d{4})')[0]
        print("Years:", years.tolist())
