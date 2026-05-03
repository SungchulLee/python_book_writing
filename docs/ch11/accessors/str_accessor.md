# String Accessor (str)

The `str` accessor in pandas provides vectorized string operations on Series containing string data. This allows you to apply string methods to entire columns without explicit loops.

!!! tip "Mental Model"
    Python's built-in string methods work on one string at a time. The `.str` accessor broadcasts those same methods over an entire column, automatically skipping NaN values. Think of it as lifting `str.upper()`, `str.contains()`, and friends from scalar operations to column-wide operations.

## Overview

```python
import pandas as pd

s = pd.Series(['Alice', 'Bob', 'Charlie'])

# Access string methods via .str accessor
print(s.str.upper())
```

```
0      ALICE
1        BOB
2    CHARLIE
dtype: object
```

## Why Use the str Accessor?

1. **Vectorized Operations**: Apply string methods to all elements at once
2. **Automatic NaN Handling**: Missing values are handled gracefully
3. **Method Chaining**: Chain multiple string operations together
4. **Performance**: Optimized for pandas data structures

```python
# Without str accessor (slow, verbose)
result = [x.upper() if pd.notna(x) else x for x in s]

# With str accessor (fast, concise)
result = s.str.upper()
```

## Case Transformation

### upper() and lower()

```python
s = pd.Series(['Hello', 'World', 'Python'])

print(s.str.upper())  # HELLO, WORLD, PYTHON
print(s.str.lower())  # hello, world, python
```

### capitalize()

Capitalize first character, lowercase the rest.

```python
s = pd.Series(['alice', 'JOHN', 'mARY', 'bOB'])
print(s.str.capitalize())
```

```
0    Alice
1     John
2     Mary
3      Bob
dtype: object
```

**Practical Example (LeetCode 1667)**: Fix names in a table.

```python
users = pd.DataFrame({
    'user_id': [1, 2, 3, 4],
    'name': ['alice', 'john', 'MARY', 'bOB']
})

users['name'] = users['name'].str.capitalize()
print(users)
```

```
   user_id   name
0        1  Alice
1        2   John
2        3   Mary
3        4    Bob
```

### title()

Capitalize first character of each word.

```python
s = pd.Series(['hello world', 'PYTHON PANDAS'])
print(s.str.title())
```

```
0    Hello World
1    Python Pandas
dtype: object
```

### swapcase()

```python
s = pd.Series(['Hello World'])
print(s.str.swapcase())  # hELLO wORLD
```

## String Length

### len()

```python
s = pd.Series(['Hello', 'World', 'Python'])
print(s.str.len())
```

```
0    5
1    5
2    6
dtype: int64
```

**Practical Example (LeetCode 1683)**: Find tweets longer than 15 characters.

```python
tweets = pd.DataFrame({
    'tweet_id': [1, 2, 3, 4],
    'content': ['Hello world!', 'This is a very long tweet!', 'Short', 'Another tweet']
})

# Filter tweets with content > 15 characters
long_tweets = tweets[tweets['content'].str.len() > 15]
print(long_tweets)
```

```
   tweet_id                     content
1         2  This is a very long tweet!
```

## Substring Operations

### Indexing with []

```python
s = pd.Series(['Alice', 'Bob', 'Charlie'])

print(s.str[0])      # First character: A, B, C
print(s.str[-1])     # Last character: e, b, e
print(s.str[:3])     # First 3 characters: Ali, Bob, Cha
```

### slice()

```python
s = pd.Series(['Apple', 'Banana', 'Cherry'])
print(s.str.slice(0, 3))  # App, Ban, Che
```

### get()

Get character at position (like indexing but safer with NaN).

```python
s = pd.Series(['Alice', None, 'Charlie'])
print(s.str.get(0))  # A, NaN, C
```

## Searching and Matching

### contains()

Check if pattern is contained in each string.

```python
s = pd.Series(['apple', 'banana', 'cherry', 'date'])
print(s.str.contains('an'))
```

```
0    False
1     True
2    False
3    False
dtype: bool
```

**Practical Example (LeetCode 620)**: Find movies without "boring" in description.

```python
cinema = pd.DataFrame({
    'id': [1, 2, 3, 4, 5],
    'description': ['A thrilling adventure', 'A boring documentary', 
                    'An exciting drama', 'A slow and boring tale', 'A great comedy']
})

# Filter out boring movies (case-insensitive)
not_boring = cinema[~cinema['description'].str.contains('boring', case=False)]
print(not_boring)
```

```
   id            description
0   1  A thrilling adventure
2   3      An exciting drama
4   5         A great comedy
```

### startswith() and endswith()

```python
s = pd.Series(['Apple', 'Apricot', 'Banana', 'Avocado'])

print(s.str.startswith('A'))   # True, True, False, True
print(s.str.endswith('a'))     # False, False, True, False
```

**Practical Example (LeetCode 1873)**: Find employees whose names don't start with 'M'.

```python
employees = pd.DataFrame({
    'employee_id': [1, 2, 3, 4, 5],
    'name': ['Alice', 'Bob', 'Mike', 'Molly', 'Eve']
})

# Employees with odd ID and name not starting with 'M'
bonus_eligible = employees[
    (employees['employee_id'] % 2 != 0) & 
    (~employees['name'].str.startswith('M'))
]
print(bonus_eligible)
```

```
   employee_id   name
0            1  Alice
4            5    Eve
```

### match()

Match regular expression pattern at the start of string.

```python
s = pd.Series(['alice@example.com', 'bob@test.org', 'invalid-email'])

# Check valid email format
pattern = r'^[a-zA-Z][a-zA-Z0-9._-]*@[a-zA-Z]+\.[a-zA-Z]+$'
print(s.str.match(pattern))
```

```
0     True
1     True
2    False
dtype: bool
```

**Practical Example (LeetCode 1517)**: Find users with valid emails.

```python
users = pd.DataFrame({
    'user_id': [1, 2, 3],
    'mail': ['alice@leetcode.com', 'bob@leet?com.com', '123@example.com']
})

# Valid email pattern: starts with letter, domain is @leetcode.com
valid_pattern = r'^[A-Za-z][A-Za-z0-9_.\-]*@leetcode\.com$'
valid_users = users[users['mail'].str.match(valid_pattern)]
print(valid_users)
```

### find() and rfind()

Find position of substring.

```python
s = pd.Series(['hello world', 'world hello', 'no match'])
print(s.str.find('world'))  # 6, 0, -1
```

## String Replacement

### replace()

Replace occurrences of pattern.

```python
s = pd.Series(['apple-pie', 'banana-split', 'cherry-tart'])
print(s.str.replace('-', '_'))
```

```
0      apple_pie
1    banana_split
2     cherry_tart
dtype: object
```

### With Regex

```python
s = pd.Series(['price: $100', 'cost: $200', 'value: \$300'])

# Remove dollar amounts
print(s.str.replace(r'\$\d+', 'XXX', regex=True))
```

```
0    price: XXX
1     cost: XXX
2    value: XXX
dtype: object
```

## Splitting and Joining

### split()

```python
s = pd.Series(['a-b-c', 'x-y-z'])
print(s.str.split('-'))
```

```
0    [a, b, c]
1    [x, y, z]
dtype: object
```

### split() with expand

Create multiple columns from split.

```python
s = pd.Series(['John Doe', 'Jane Smith', 'Bob Wilson'])
names = s.str.split(' ', expand=True)
names.columns = ['first', 'last']
print(names)
```

```
  first   last
0  John    Doe
1  Jane  Smith
2   Bob Wilson
```

### join()

Join lists in each element.

```python
s = pd.Series([['a', 'b', 'c'], ['x', 'y', 'z']])
print(s.str.join('-'))
```

```
0    a-b-c
1    x-y-z
dtype: object
```

### cat()

Concatenate strings with separator.

```python
s = pd.Series(['A', 'B', 'C'])
print(s.str.cat(sep='-'))  # A-B-C
```

## Stripping Whitespace

### strip(), lstrip(), rstrip()

```python
s = pd.Series(['  hello  ', '  world  '])

print(s.str.strip())   # 'hello', 'world'
print(s.str.lstrip())  # 'hello  ', 'world  '
print(s.str.rstrip())  # '  hello', '  world'
```

## Padding

### pad(), ljust(), rjust(), center()

```python
s = pd.Series(['a', 'bb', 'ccc'])

print(s.str.pad(5, fillchar='_'))       # ____a, ___bb, __ccc
print(s.str.ljust(5, fillchar='_'))     # a____, bb___, ccc__
print(s.str.center(5, fillchar='_'))    # __a__, _bb__, _ccc_
```

### zfill()

Pad with zeros.

```python
s = pd.Series(['1', '12', '123'])
print(s.str.zfill(5))  # 00001, 00012, 00123
```

## Extracting Data

### extract()

Extract groups from regex pattern.

```python
s = pd.Series(['A-123', 'B-456', 'C-789'])

# Extract letter and number
extracted = s.str.extract(r'([A-Z])-(\d+)')
extracted.columns = ['letter', 'number']
print(extracted)
```

```
  letter number
0      A    123
1      B    456
2      C    789
```

### extractall()

Extract all matches (returns MultiIndex).

```python
s = pd.Series(['a1b2c3', 'x9y8z7'])
print(s.str.extractall(r'(\d)'))
```

## Handling Missing Values

The str accessor handles NaN values gracefully.

```python
s = pd.Series(['Hello', None, 'World'])

print(s.str.upper())
```

```
0    HELLO
1      NaN
2    WORLD
dtype: object
```

### Explicit NA Handling

```python
# Some methods have na parameter
s = pd.Series(['Apple', None, 'Banana'])
print(s.str.contains('a', na=False))  # False for NaN
print(s.str.contains('a', na=True))   # True for NaN
```

## Method Chaining

String methods can be chained together.

```python
s = pd.Series(['  HELLO WORLD  ', '  PYTHON PANDAS  '])

result = (s
    .str.strip()
    .str.lower()
    .str.replace(' ', '_')
)
print(result)
```

```
0      hello_world
1    python_pandas
dtype: object
```

## Financial Example: Ticker Cleaning

```python
# Raw ticker data with inconsistencies
tickers = pd.Series(['  aapl  ', 'MSFT', 'googl ', ' AMZN'])

# Clean and standardize
clean_tickers = (tickers
    .str.strip()
    .str.upper()
)
print(clean_tickers)
```

```
0    AAPL
1    MSFT
2    GOOGL
3    AMZN
dtype: object
```

## Summary of Common Methods

| Method | Purpose | Example |
|--------|---------|---------|
| `upper()`, `lower()` | Case conversion | `s.str.upper()` |
| `capitalize()` | Capitalize first char | `s.str.capitalize()` |
| `len()` | String length | `s.str.len()` |
| `contains()` | Pattern search | `s.str.contains('pat')` |
| `startswith()` | Prefix check | `s.str.startswith('A')` |
| `replace()` | String replacement | `s.str.replace('a', 'b')` |
| `split()` | Split strings | `s.str.split('-')` |
| `strip()` | Remove whitespace | `s.str.strip()` |
| `extract()` | Regex extraction | `s.str.extract(r'(\d+)')` |
| `match()` | Regex matching | `s.str.match(r'^[A-Z]')` |

---

## Exercises

**Exercise 1.**
Given a Series of full names like `['Alice Smith', 'Bob Jones', 'Carol Lee']`, use the `.str` accessor to extract only the first names (everything before the space) into a new Series.

??? success "Solution to Exercise 1"
    Use `.str.split()` and access the first element.

        import pandas as pd

        names = pd.Series(['Alice Smith', 'Bob Jones', 'Carol Lee'])
        first_names = names.str.split(' ').str[0]
        print(first_names)

---

**Exercise 2.**
Given a Series of email addresses, use `.str.contains()` to create a boolean mask that identifies emails from the domain `'gmail.com'`. Then filter the Series to show only Gmail addresses.

??? success "Solution to Exercise 2"
    Use `.str.contains()` with `case=False` for safety.

        import pandas as pd

        emails = pd.Series(['alice@gmail.com', 'bob@yahoo.com', 'carol@gmail.com', 'dave@outlook.com'])
        gmail_mask = emails.str.contains('gmail.com')
        gmail_only = emails[gmail_mask]
        print(gmail_only)

---

**Exercise 3.**
Given a Series of messy product codes like `['  AB-123  ', 'cd-456', '  EF-789']`, chain `.str` methods to (1) strip whitespace, (2) convert to uppercase, and (3) replace the hyphen with an underscore. The result should be `['AB_123', 'CD_456', 'EF_789']`.

??? success "Solution to Exercise 3"
    Chain `strip()`, `upper()`, and `replace()`.

        import pandas as pd

        codes = pd.Series(['  AB-123  ', 'cd-456', '  EF-789'])
        cleaned = codes.str.strip().str.upper().str.replace('-', '_')
        print(cleaned)
