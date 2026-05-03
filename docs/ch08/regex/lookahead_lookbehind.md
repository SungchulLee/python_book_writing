# Lookahead and Lookbehind

!!! tip "Mental Model"
    Lookarounds are invisible checkpoints in a pattern. A lookahead peeks at what comes *after* the current position, and a lookbehind peeks at what came *before* — but neither consumes any characters. They let you assert context without including it in the match, which is essential for tasks like "find a number only if it is followed by a dollar sign."

## What Are Lookarounds?

Lookarounds are **zero-width assertions** — they check whether a pattern exists before or after the current position without consuming any characters. The matched text is not included in the result.

| Syntax | Name | Meaning |
|---|---|---|
| `(?=...)` | Positive lookahead | Followed by `...` |
| `(?!...)` | Negative lookahead | NOT followed by `...` |
| `(?<=...)` | Positive lookbehind | Preceded by `...` |
| `(?<!...)` | Negative lookbehind | NOT preceded by `...` |

```
         Lookbehind          Lookahead
         (?<=...) (?<!...)   (?=...) (?!...)
                    ↓            ↓
    ... [before] [current pos] [after] ...
```

## Positive Lookahead `(?=...)`

Matches a position where the lookahead pattern **exists** ahead, without consuming it:

```python
import re

# Find "Python" only when followed by a space and a version number
re.findall(r'Python(?=\s\d)', 'Python 3 and Python are great')
# ['Python']  — only the first "Python" (followed by " 3")

# Find words followed by a comma
re.findall(r'\w+(?=,)', 'apple, banana, cherry')
# ['apple', 'banana']
```

The key insight is that the lookahead text is **not consumed**:

```python
import re

# Without lookahead — "ing" is consumed
re.findall(r'\w+ing', 'running jumping sitting')
# ['running', 'jumping', 'sitting']

# With lookahead — "ing" is checked but not part of the match
re.findall(r'\w+(?=ing)', 'running jumping sitting')
# ['runn', 'jump', 'sitt']
```

## Negative Lookahead `(?!...)`

Matches a position where the lookahead pattern does **not** exist:

```python
import re

# Match "foo" NOT followed by "bar"
re.findall(r'foo(?!bar)', 'foobar foobaz foo')
# ['foo', 'foo']  — the 'foo' in 'foobaz' and standalone 'foo'

# Match numbers NOT followed by a percent sign
re.findall(r'\d+(?!%)', '42% 100 85% 7')
# ['4', '10', '8', '7']  — careful with greedy matching!

# Better: use word boundary
re.findall(r'\b\d+\b(?!%)', '42% 100 85% 7')
# ['100', '7']
```

### Password Validation Example

Negative lookahead is often used for validation logic (checking that something is absent):

```python
import re

def validate_password(pw):
    """
    Requires:
    - At least 8 characters
    - At least one digit
    - At least one uppercase letter
    - At least one lowercase letter
    - No spaces
    """
    pattern = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).{8,}$'
    return bool(re.fullmatch(pattern, pw))

print(validate_password("Abc12345"))     # True
print(validate_password("abc12345"))     # False — no uppercase
print(validate_password("ABC12345"))     # False — no lowercase
print(validate_password("Abcdefgh"))     # False — no digit
print(validate_password("Ab 12345"))     # False — contains space
print(validate_password("Ab12"))         # False — too short
```

Multiple lookaheads at position 0 act as **AND conditions**: each must be satisfied independently.

## Positive Lookbehind `(?<=...)`

Matches a position where the lookbehind pattern **exists** before:

```python
import re

# Find numbers preceded by a dollar sign
re.findall(r'(?<=\$)\d+', 'Price: \$42, €50, \$100')
# ['42', '100']

# Find words preceded by "@" (mentions)
re.findall(r'(?<=@)\w+', 'Hello @alice and @bob')
# ['alice', 'bob']
```

!!! warning "Fixed-Width Lookbehind"
    In Python, lookbehind patterns must match a **fixed-length** string. Variable-length patterns like `(?<=\d+)` are not allowed and raise `re.error`. However, alternations of different fixed lengths are permitted: `(?<=ab|cde)` works.

```python
import re

# Fixed-width — OK
re.findall(r'(?<=\$)\d+', '\$42')          # ['42']
re.findall(r'(?<=USD\s)\d+', 'USD 42')    # ['42']

# Variable-width — ERROR
try:
    re.findall(r'(?<=\$\d+\.)\d+', '\$3.50')
except re.error as e:
    print(e)  # look-behind requires fixed-width pattern

# Alternation of fixed widths — OK
re.findall(r'(?<=\$|€)\d+', '\$42 €50')    # ['42', '50']
```

## Negative Lookbehind `(?<!...)`

Matches a position where the lookbehind pattern does **not** exist:

```python
import re

# Match numbers NOT preceded by a dollar sign
re.findall(r'(?<!\$)\b\d+', 'Price: $42, quantity: 100, code: \$7')
# ['100']

# Match "test" NOT preceded by "unit"
re.findall(r'(?<!unit)test', 'unittest test mytest')
# ['test', 'test']
```

## Combining Lookarounds

Lookarounds can be combined for precise matching:

```python
import re

# Find numbers that are both preceded by $ and followed by a decimal point
re.findall(r'(?<=\$)\d+(?=\.)', '\$42.99 \$100 €50.00')
# ['42']

# Find words surrounded by underscores (like _word_) 
# without including the underscores in the match
re.findall(r'(?<=_)\w+(?=_)', 'This is _bold_ and _italic_ text')
# ['bold', 'italic']
```

### Overlapping Matches

Since lookarounds don't consume characters, they enable finding "overlapping" patterns:

```python
import re

# Find all positions where "aa" occurs (including overlapping)
text = "aaa"

# Without lookahead — non-overlapping only
re.findall(r'aa', text)
# ['aa']  — finds only one

# With lookahead — overlapping
re.findall(r'(?=(aa))', text)
# ['aa', 'aa']  — finds both positions (0 and 1)
```

## Practical Examples

### Number Formatting (Thousands Separator)

```python
import re

def add_commas(n):
    """Add thousand separators: 1234567 → '1,234,567'"""
    s = str(n)
    # Insert comma before groups of 3 digits from the right
    # Positive lookahead: followed by groups of exactly 3 digits to the end
    # Positive lookbehind: preceded by a digit
    return re.sub(r'(?<=\d)(?=(\d{3})+$)', ',', s)

print(add_commas(1234567))     # '1,234,567'
print(add_commas(1000000000))  # '1,000,000,000'
print(add_commas(42))          # '42'
```

### Extracting Values After Labels

```python
import re

text = "Name: Alice  Age: 30  City: Seoul"

# Extract values after specific labels
labels = re.findall(r'(?<=Name:\s)\w+', text)    # ['Alice']
ages = re.findall(r'(?<=Age:\s)\d+', text)        # ['30']
cities = re.findall(r'(?<=City:\s)\w+', text)     # ['Seoul']
```

### Splitting Without Losing Context

```python
import re

# Split before uppercase letters (camelCase → words)
text = "camelCaseVariableName"
re.split(r'(?=[A-Z])', text)
# ['camel', 'Case', 'Variable', 'Name']

# Split after digits
re.split(r'(?<=\d)(?=[a-zA-Z])', 'abc123def456ghi')
# ['abc123', 'def456', 'ghi']
```

### URL Protocol Check

```python
import re

urls = [
    "https://example.com",
    "http://test.org",
    "ftp://files.example.com",
    "example.com",
]

# Match URLs that do NOT start with https
for url in urls:
    if re.match(r'(?!https://)\S+', url) and '://' in url:
        print(f"Not HTTPS: {url}")
# Not HTTPS: http://test.org
# Not HTTPS: ftp://files.example.com
```

## Summary

| Lookaround | Syntax | Meaning | Width |
|---|---|---|---|
| Positive lookahead | `(?=...)` | Must be followed by | Zero |
| Negative lookahead | `(?!...)` | Must NOT be followed by | Zero |
| Positive lookbehind | `(?<=...)` | Must be preceded by | Zero (fixed-width only) |
| Negative lookbehind | `(?<!...)` | Must NOT be preceded by | Zero (fixed-width only) |
| Combined | Stack multiple | AND conditions at a position | Zero |

---

## Runnable Example: `lookahead_lookbehind_tutorial.py`

```python
"""
Python Regular Expressions - Tutorial 06: Lookahead and Lookbehind
==================================================================

LEARNING OBJECTIVES:
-------------------
1. Understand lookahead assertions (?=...) and (?!...)
2. Master lookbehind assertions (?<=...) and (?<!...)
3. Combine lookarounds with other patterns
4. Apply lookarounds to complex validation scenarios
5. Understand zero-width assertions

PREREQUISITES:
-------------
- Tutorials 01-05 (all previous tutorials)

DIFFICULTY: ADVANCED
"""

import re

# ==============================================================================
# SECTION 1: INTRODUCTION TO LOOKAROUNDS
# ==============================================================================

if __name__ == "__main__":

    """
    LOOKAROUNDS are zero-width assertions - they match a position, not characters.
    They CHECK if a pattern exists ahead or behind, without consuming characters.

    Types:
      (?=...)   Positive lookahead: must be followed by ...
      (?!...)   Negative lookahead: must NOT be followed by ...
      (?<=...)  Positive lookbehind: must be preceded by ...
      (?<!...)  Negative lookbehind: must NOT be preceded by ...

    Key concept: They don't capture or consume characters!
    """

    print("="*70)
    print("SECTION 1: POSITIVE LOOKAHEAD (?=...)")
    print("="*70)

    # Example 1: Basic positive lookahead
    # -----------------------------------
    """
    Match a pattern only if it's followed by another pattern.
    """

    text1 = "read reading reader"

    # Match "read" only if followed by "ing"
    pattern1 = r"read(?=ing)"
    matches1 = re.findall(pattern1, text1)

    print(f"Text: '{text1}'")
    print(f"Pattern: 'read(?=ing)' (read followed by ing)")
    print(f"Matches: {matches1}")
    print("(Note: 'ing' is not included in the match)")

    print()

    # Example 2: Lookahead for validation
    # -----------------------------------
    """
    Check if a number is followed by a specific unit.
    """

    text2 = "100kg 200g 300ml"

    # Match numbers followed by "kg"
    pattern2 = r"\d+(?=kg)"
    matches2 = re.findall(pattern2, text2)

    print(f"Text: '{text2}'")
    print(f"Pattern: '\\d+(?=kg)' (numbers before kg)")
    print(f"Matches: {matches2}")

    print()

    # ==============================================================================
    # SECTION 2: NEGATIVE LOOKAHEAD (?!...)
    # ==============================================================================

    """
    Match only if NOT followed by a pattern.
    """

    print("="*70)
    print("SECTION 2: NEGATIVE LOOKAHEAD (?!...)")
    print("="*70)

    # Example 3: Negative lookahead
    # -----------------------------
    text3 = "cat cats dog dogs"

    # Match "cat" not followed by "s"
    pattern3 = r"cat(?!s)"
    matches3 = re.findall(pattern3, text3)

    print(f"Text: '{text3}'")
    print(f"Pattern: 'cat(?!s)' (cat not followed by s)")
    print(f"Matches: {matches3}")

    print()

    # Example 4: Excluding specific suffixes
    # --------------------------------------
    text4 = "test.txt test.py test.md readme.txt"

    # Match filenames not ending with .txt
    pattern4 = r"\w+(?!\.txt)\.\w+"
    matches4 = re.findall(pattern4, text4)

    print(f"Text: '{text4}'")
    print(f"Non-.txt files: {matches4}")

    print()

    # ==============================================================================
    # SECTION 3: POSITIVE LOOKBEHIND (?<=...)
    # ==============================================================================

    """
    Match only if preceded by a pattern.
    """

    print("="*70)
    print("SECTION 3: POSITIVE LOOKBEHIND (?<=...)")
    print("="*70)

    # Example 5: Basic lookbehind
    # ---------------------------
    text5 = "$100 €200 £300"

    # Match numbers preceded by $
    pattern5 = r"(?<=\$)\d+"
    matches5 = re.findall(pattern5, text5)

    print(f"Text: '{text5}'")
    print(f"Pattern: '(?<=\\$)\\d+' (numbers after $)")
    print(f"Matches: {matches5}")

    print()

    # Example 6: Extracting values after labels
    # -----------------------------------------
    text6 = "Price: $50 Tax: $10 Total: $60"

    # Match numbers that come after "Total: $"
    pattern6 = r"(?<=Total: \$)\d+"
    total = re.search(pattern6, text6)

    print(f"Text: '{text6}'")
    if total:
        print(f"Total amount: ${total.group()}")

    print()

    # ==============================================================================
    # SECTION 4: NEGATIVE LOOKBEHIND (?<!...)
    # ==============================================================================

    """
    Match only if NOT preceded by a pattern.
    """

    print("="*70)
    print("SECTION 4: NEGATIVE LOOKBEHIND (?<!...)")
    print("="*70)

    # Example 7: Negative lookbehind
    # ------------------------------
    text7 = "123 456 789 012"

    # Match 3-digit numbers NOT preceded by "0"
    pattern7 = r"(?<!0)\d{3}"
    matches7 = re.findall(pattern7, text7)

    print(f"Text: '{text7}'")
    print(f"Pattern: '(?<!0)\\d{{3}}' (3 digits not after 0)")
    print(f"Matches: {matches7}")

    print()

    # ==============================================================================
    # SECTION 5: COMBINING LOOKAROUNDS
    # ==============================================================================

    print("="*70)
    print("SECTION 5: COMBINING LOOKAROUNDS")
    print("="*70)

    # Example 8: Password validation
    # ------------------------------
    """
    Validate password:
    - At least 8 characters
    - Contains at least one digit
    - Contains at least one letter
    - Contains at least one special character
    """

    def validate_password(password):
        # Check minimum length
        if len(password) < 8:
            return False, "Too short"

        # Use lookaheads to check all requirements
        pattern = r"^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$"

        if re.match(pattern, password):
            return True, "Valid password"
        return False, "Missing required characters"

    passwords = [
        "password",      # No digit or special char
        "pass123",       # No special char
        "Pass@123",      # Valid!
        "12345678",      # No letters or special
        "P@ss1"          # Too short
    ]

    print("Password validation:")
    for pwd in passwords:
        valid, msg = validate_password(pwd)
        status = "✓" if valid else "✗"
        print(f"  {status} '{pwd}': {msg}")

    print()

    # Example 9: Finding words between specific patterns
    # --------------------------------------------------
    text9 = "start apple banana end start cherry date end"

    # Match words that are after "start" and before "end"
    pattern9 = r"(?<=start )\w+(?= \w* end)"
    matches9 = re.findall(pattern9, text9)

    print(f"Text: '{text9}'")
    print(f"Words after 'start': {matches9}")

    print()

    # ==============================================================================
    # SECTION 6: PRACTICAL APPLICATIONS
    # ==============================================================================

    print("="*70)
    print("SECTION 6: PRACTICAL APPLICATIONS")
    print("="*70)

    # Example 10: Currency conversion validation
    # ------------------------------------------
    text10 = "$100.00 €200.50 £300.75 ¥400"

    # Extract amounts in dollars only
    dollar_pattern = r"(?<=\$)\d+\.\d{2}"
    dollar_amounts = re.findall(dollar_pattern, text10)

    print(f"Text: '{text10}'")
    print(f"Dollar amounts: {['$' + amt for amt in dollar_amounts]}")

    print()

    # Example 11: Extracting @mentions (not in emails)
    # ------------------------------------------------
    text11 = "Hi @john! Email: user@example.com, @alice says hi"

    # Match @username but not when it's part of an email
    pattern11 = r"(?<!\w)@\w+(?![\w.])"
    mentions = re.findall(pattern11, text11)

    print(f"Text: '{text11}'")
    print(f"Mentions: {mentions}")
    print("(Excludes @example.com because it's part of email)")

    print()

    # Example 12: Matching numbers not in equations
    # ---------------------------------------------
    text12 = "Age: 25, Score: 3+7=10, Price: 30"

    # Match standalone numbers (not part of equations)
    pattern12 = r"(?<![+=])\d+(?![+=])"
    standalone = re.findall(pattern12, text12)

    print(f"Text: '{text12}'")
    print(f"Standalone numbers: {standalone}")

    print()

    # ==============================================================================
    # SECTION 7: ADVANCED PATTERNS
    # ==============================================================================

    print("="*70)
    print("SECTION 7: ADVANCED LOOKAROUND PATTERNS")
    print("="*70)

    # Example 13: Remove duplicate words but keep one
    # -----------------------------------------------
    text13 = "the the cat sat sat on the mat mat"

    # Remove only the second occurrence of duplicates
    pattern13 = r"\b(\w+)\s+(?=\1\b)"
    result13 = re.sub(pattern13, "", text13)

    print(f"Original: '{text13}'")
    print(f"Deduplicated: '{result13}'")

    print()

    # Example 14: Validate hex color codes
    # ------------------------------------
    """
    Valid: #FFF, #FFFFFF
    Invalid: #FF, #FFFFFFF
    """

    colors = ["#FFF", "#FFFFFF", "#123ABC", "#GG", "#12345"]

    pattern14 = r"^#(?:[0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$"

    print("Hex color validation:")
    for color in colors:
        valid = bool(re.match(pattern14, color))
        status = "✓" if valid else "✗"
        print(f"  {status} {color}")

    print()

    # ==============================================================================
    # SECTION 8: SUMMARY
    # ==============================================================================

    print("="*70)
    print("LOOKAROUND CHEAT SHEET")
    print("="*70)

    cheat_sheet = """
    LOOKAHEAD (looks forward):
      (?=...)     Positive: must be followed by ...
      (?!...)     Negative: must NOT be followed by ...

    LOOKBEHIND (looks backward):
      (?<=...)    Positive: must be preceded by ...
      (?<!...)    Negative: must NOT be preceded by ...

    KEY FEATURES:
      - Zero-width: don't consume characters
      - Don't capture: not included in match
      - Multiple lookarounds can be combined
      - Lookbehind must be fixed-width in Python

    COMMON PATTERNS:
      (?=.*\d)               Contains at least one digit
      (?!.*admin)            Doesn't contain "admin"
      (?<=\$)\d+             Number after $
      (?<!@)\w+              Word not preceded by @

    PASSWORD VALIDATION:
      ^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$
      - At least 8 chars
      - Has lowercase, uppercase, and digit

    CAUTION:
      - Lookbehind must have fixed width
      - Can impact performance
      - Sometimes simpler alternatives exist
    """

    print(cheat_sheet)

    print("\n" + "="*70)
    print("END OF TUTORIAL - Lookahead and Lookbehind mastered!")
    print("Next: Tutorial 07 - Practical Applications")
    print("="*70)
```

---

## Exercises

**Exercise 1.**
Write a regex using a positive lookahead to find all words that are followed by a comma. For example, in `"apple, banana, cherry and grape"`, match `"apple"` and `"banana"` but not `"cherry"` or `"grape"`.

??? success "Solution to Exercise 1"

    ```python
    import re

    pattern = r'\w+(?=,)'
    text = "apple, banana, cherry and grape"
    matches = re.findall(pattern, text)
    print(matches)  # ['apple', 'banana']
    ```

---

**Exercise 2.**
Write a regex using a positive lookbehind to find all numbers that are preceded by a dollar sign `$`. For example, in `"Cost: $50, Tax: $7.50, Count: 100"`, match `"50"` and `"7.50"` but not `"100"`. Use `re.findall`.

??? success "Solution to Exercise 2"

    ```python
    import re

    pattern = r'(?<=\$)\d+\.?\d*'
    text = "Cost: $50, Tax: $7.50, Count: 100"
    matches = re.findall(pattern, text)
    print(matches)  # ['50', '7.50']
    ```

---

**Exercise 3.**
Write a password validation regex that uses lookaheads to enforce all of these rules simultaneously: at least 8 characters, at least one uppercase letter, at least one lowercase letter, at least one digit, and at least one special character from `!@#$%`. Test with several passwords.

??? success "Solution to Exercise 3"

    ```python
    import re

    pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%]).{8,}$'

    passwords = ["Abc123!x", "abc123!x", "ABCDEF1!", "Ab1!", "Password1!"]
    for pw in passwords:
        valid = bool(re.match(pattern, pw))
        print(f"'{pw}': {'Valid' if valid else 'Invalid'}")
    # 'Abc123!x': Valid
    # 'abc123!x': Invalid (no uppercase)
    # 'ABCDEF1!': Invalid (no lowercase)
    # 'Ab1!': Invalid (too short)
    # 'Password1!': Valid
    ```
