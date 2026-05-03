# Quantifiers and Anchors

!!! tip "Mental Model"
    Quantifiers answer "how many?" — `*` means zero or more, `+` means one or more, `?` means zero or one, and `{n,m}` means between n and m. Anchors answer "where?" — `^` pins to the start of the string and `$` to the end. Together they let you specify not just *what* to match but *how much* and *where*.

## Quantifiers

Quantifiers specify **how many times** the preceding element must occur for a match. By default, quantifiers are **greedy** — they match as much text as possible.

### Basic Quantifiers

| Quantifier | Meaning | Example | Matches |
|---|---|---|---|
| `*` | Zero or more | `ab*c` | `ac`, `abc`, `abbc`, `abbbc` |
| `+` | One or more | `ab+c` | `abc`, `abbc`, `abbbc` (not `ac`) |
| `?` | Zero or one | `colou?r` | `color`, `colour` |
| `{n}` | Exactly *n* | `\d{4}` | `2024` (exactly 4 digits) |
| `{n,}` | At least *n* | `\d{2,}` | `42`, `007`, `12345` |
| `{n,m}` | Between *n* and *m* | `\d{2,4}` | `42`, `007`, `2024` |

```python
import re

# * — zero or more
re.findall(r'go*d', 'gd god good goood')
# ['gd', 'god', 'good', 'goood']

# + — one or more
re.findall(r'go+d', 'gd god good goood')
# ['god', 'good', 'goood']

# ? — zero or one
re.findall(r'colou?r', 'color and colour')
# ['color', 'colour']

# {n} — exactly n
re.findall(r'\b\d{3}\b', '1 12 123 1234')
# ['123']

# {n,m} — between n and m
re.findall(r'\b\d{2,4}\b', '1 12 123 1234 12345')
# ['12', '123', '1234']
```

### Greedy vs Lazy Quantifiers

By default, quantifiers are **greedy** — they consume as much text as possible. Adding `?` after a quantifier makes it **lazy** (also called non-greedy or reluctant) — it matches as little as possible.

| Greedy | Lazy | Behavior |
|---|---|---|
| `*` | `*?` | Zero or more (prefer fewer) |
| `+` | `+?` | One or more (prefer fewer) |
| `?` | `??` | Zero or one (prefer zero) |
| `{n,m}` | `{n,m}?` | Between n and m (prefer fewer) |

```python
import re

html = '<b>bold</b> and <i>italic</i>'

# Greedy — matches from first < to LAST >
re.findall(r'<.*>', html)
# ['<b>bold</b> and <i>italic</i>']

# Lazy — matches from first < to NEXT >
re.findall(r'<.*?>', html)
# ['<b>', '</b>', '<i>', '</i>']
```

This distinction is critical when parsing structured text:

```python
import re

text = '"first" and "second" and "third"'

# Greedy: matches from first " to last "
re.findall(r'".*"', text)
# ['"first" and "second" and "third"']

# Lazy: matches each quoted string
re.findall(r'".*?"', text)
# ['"first"', '"second"', '"third"']
```

!!! tip "When to Use Lazy Quantifiers"
    Use lazy quantifiers when you want to match the **shortest** possible substring, especially with delimiters like quotes, tags, or brackets. For simple patterns without ambiguity, greedy quantifiers work fine.

### Possessive Quantifiers (Python 3.11+)

Python 3.11 introduced **possessive quantifiers** (`*+`, `++`, `?+`, `{n,m}+`). These are greedy but never backtrack, which can improve performance:

```python
import re

# Possessive + (Python 3.11+)
# Fails fast — no backtracking
try:
    re.search(r'[a-z]++[a-z]', 'abcdef')  # None — possessive consumed all
except Exception:
    pass  # Older Python versions
```

Possessive quantifiers are an optimization tool; in most cases, greedy and lazy are sufficient.

## Anchors

Anchors match **positions** in the string, not characters. They have zero width — they don't consume any characters.

### String Anchors

| Anchor | Matches |
|---|---|
| `^` | Start of string (or line with `re.M`) |
| `$` | End of string (or line with `re.M`) |
| `\A` | Start of string (ignores `re.M`) |
| `\Z` | End of string (ignores `re.M`) |

```python
import re

text = "line one\nline two\nline three"

# ^ matches start of string only
re.findall(r'^line', text)
# ['line']

# ^ with MULTILINE matches start of each line
re.findall(r'^line', text, re.M)
# ['line', 'line', 'line']

# \A always matches start of string, regardless of flags
re.findall(r'\Aline', text, re.M)
# ['line']
```

### Word Boundaries

| Anchor | Matches |
|---|---|
| `\b` | Boundary between word and non-word character |
| `\B` | Position that is **not** a word boundary |

```python
import re

text = "cat concatenate scattered"

# \b — word boundary
re.findall(r'\bcat\b', text)   # ['cat']
re.findall(r'\bcat', text)     # ['cat', 'cat']

# \B — NOT a word boundary
re.findall(r'\Bcat', text)     # ['cat']  — the 'cat' inside 'scattered'
re.findall(r'cat\B', text)     # ['cat', 'cat']  — 'cat' not at end of word
```

Word boundaries are essential for matching **whole words**:

```python
import re

text = "I like Java but not JavaScript"

# Without boundary — matches both
re.findall(r'Java', text)
# ['Java', 'Java']

# With boundary — matches only the standalone word
re.findall(r'\bJava\b', text)
# ['Java']
```

## Combining Quantifiers and Anchors

Quantifiers and anchors work together to create precise patterns:

```python
import re

# Match lines that contain only digits
text = "123\nabc\n456\na1b"
re.findall(r'^\d+$', text, re.M)
# ['123', '456']

# Validate a string is exactly 5 uppercase letters
def is_valid_code(s):
    return bool(re.fullmatch(r'[A-Z]{5}', s))

print(is_valid_code("HELLO"))   # True
print(is_valid_code("Hello"))   # False
print(is_valid_code("HELLOO"))  # False
```

### Validating Input Formats

```python
import re

# Simple integer validation (optional sign)
def is_integer(s):
    return bool(re.fullmatch(r'[+-]?\d+', s))

print(is_integer("42"))    # True
print(is_integer("-17"))   # True
print(is_integer("3.14"))  # False

# Simple float validation
def is_float(s):
    return bool(re.fullmatch(r'[+-]?\d*\.?\d+', s))

print(is_float("3.14"))   # True
print(is_float(".5"))     # True
print(is_float("42"))     # True
print(is_float(""))       # False
```

## Summary

| Concept | Key Takeaway |
|---|---|
| `* + ?` | Zero+, one+, zero-or-one repetitions |
| `{n}` `{n,m}` | Exact or range repetitions |
| Greedy | Default — match as much as possible |
| Lazy (`*?` `+?`) | Match as little as possible |
| `^` / `$` | Start/end of string (or line with `re.M`) |
| `\A` / `\Z` | Start/end of string (always, ignoring `re.M`) |
| `\b` / `\B` | Word boundary / not a word boundary |
| `re.fullmatch()` | Anchor the entire string (like `^...$`) |

---

## Runnable Example: `quantifiers_tutorial.py`

```python
"""
Python Regular Expressions - Tutorial 03: Quantifiers
=====================================================

LEARNING OBJECTIVES:
-------------------
1. Understand repetition with quantifiers (*, +, ?, {m,n})
2. Learn the difference between greedy and non-greedy matching
3. Apply quantifiers to character classes
4. Use quantifiers for practical pattern matching
5. Combine quantifiers with previously learned concepts

PREREQUISITES:
-------------
- Tutorial 01: Regex Basics
- Tutorial 02: Character Classes

DIFFICULTY: INTERMEDIATE
"""

import re

# ==============================================================================
# SECTION 1: INTRODUCTION TO QUANTIFIERS
# ==============================================================================

if __name__ == "__main__":

    """
    QUANTIFIERS specify how many times a pattern should match.
    Instead of matching a single character, you can match multiple repetitions.

    Basic Quantifiers:
      *     : 0 or more occurrences (zero to infinity)
      +     : 1 or more occurrences (at least one)
      ?     : 0 or 1 occurrence (optional)
      {m}   : Exactly m occurrences
      {m,n} : Between m and n occurrences (inclusive)
      {m,}  : m or more occurrences

    Quantifiers apply to the character or group immediately before them.
    """

    print("="*70)
    print("SECTION 1: BASIC QUANTIFIERS")
    print("="*70)

    # Example 1: The * quantifier (zero or more)
    # ------------------------------------------
    # * matches the preceding element 0 or more times

    pattern1 = r"ab*c"  # 'a', followed by zero or more 'b', followed by 'c'
    test_strings1 = ["ac", "abc", "abbc", "abbbc", "axc"]

    print(f"Pattern: '{pattern1}' (a + zero or more b + c)")
    for text in test_strings1:
        match = re.search(pattern1, text)
        result = f"✓ Matches" if match else "✗ No match"
        print(f"  '{text}': {result}")

    print()

    # Example 2: The + quantifier (one or more)
    # -----------------------------------------
    # + matches the preceding element 1 or more times

    pattern2 = r"ab+c"  # 'a', followed by one or more 'b', followed by 'c'
    test_strings2 = ["ac", "abc", "abbc", "abbbc"]

    print(f"Pattern: '{pattern2}' (a + one or more b + c)")
    for text in test_strings2:
        match = re.search(pattern2, text)
        result = f"✓ Matches" if match else "✗ No match"
        print(f"  '{text}': {result}")

    print()

    # Example 3: The ? quantifier (optional)
    # --------------------------------------
    # ? makes the preceding element optional (0 or 1)

    pattern3 = r"colou?r"  # 'colo', followed by optional 'u', followed by 'r'
    test_strings3 = ["color", "colour", "colouur"]

    print(f"Pattern: '{pattern3}' (optional 'u')")
    for text in test_strings3:
        match = re.search(pattern3, text)
        result = f"✓ Matches" if match else "✗ No match"
        print(f"  '{text}': {result}")

    print()

    # ==============================================================================
    # SECTION 2: QUANTIFIERS WITH CHARACTER CLASSES
    # ==============================================================================

    """
    Quantifiers work great with character classes!
    This is where their real power shines.
    """

    print("="*70)
    print("SECTION 2: QUANTIFIERS WITH CHARACTER CLASSES")
    print("="*70)

    # Example 4: Matching multiple digits
    # -----------------------------------
    pattern4 = r"\d+"  # One or more digits
    text4 = "I have 3 cats, 12 dogs, and 100 fish"

    numbers = re.findall(pattern4, text4)
    print(f"Text: '{text4}'")
    print(f"Pattern: '\\d+' (one or more digits)")
    print(f"Numbers found: {numbers}")

    print()

    # Example 5: Matching multiple word characters
    # --------------------------------------------
    pattern5 = r"\w+"  # One or more word characters (forms words)
    text5 = "Hello, World! This is Python-3.9"

    words = re.findall(pattern5, text5)
    print(f"Text: '{text5}'")
    print(f"Pattern: '\\w+' (one or more word chars)")
    print(f"Words found: {words}")

    print()

    # Example 6: Matching optional whitespace
    # ---------------------------------------
    pattern6 = r"\d+\s*\w+"  # Digits, optional spaces, then word
    text6 = "3cats 12 dogs 100    fish"

    matches = re.findall(pattern6, text6)
    print(f"Text: '{text6}'")
    print(f"Pattern: '\\d+\\s*\\w+' (number, optional spaces, word)")
    print(f"Matches: {matches}")

    print()

    # ==============================================================================
    # SECTION 3: SPECIFIC REPETITION WITH {m,n}
    # ==============================================================================

    """
    CURLY BRACES allow you to specify exact repetition counts:
      {m}   : Exactly m times
      {m,n} : From m to n times (inclusive)
      {m,}  : m or more times
      {,n}  : Up to n times (0 to n)
    """

    print("="*70)
    print("SECTION 3: SPECIFIC REPETITION COUNTS")
    print("="*70)

    # Example 7: Exactly m occurrences {m}
    # ------------------------------------
    pattern7 = r"\d{3}"  # Exactly 3 digits
    text7 = "1 12 123 1234"

    matches = re.findall(pattern7, text7)
    print(f"Text: '{text7}'")
    print(f"Pattern: '\\d{{3}}' (exactly 3 digits)")
    print(f"Matches: {matches}")

    print()

    # Example 8: Range {m,n}
    # ----------------------
    pattern8 = r"\d{2,4}"  # Between 2 and 4 digits
    text8 = "1 12 123 1234 12345"

    matches = re.findall(pattern8, text8)
    print(f"Text: '{text8}'")
    print(f"Pattern: '\\d{{2,4}}' (2 to 4 digits)")
    print(f"Matches: {matches}")

    print()

    # Example 9: Minimum repetitions {m,}
    # -----------------------------------
    pattern9 = r"\d{3,}"  # 3 or more digits
    text9 = "1 12 123 1234 12345"

    matches = re.findall(pattern9, text9)
    print(f"Text: '{text9}'")
    print(f"Pattern: '\\d{{3,}}' (3 or more digits)")
    print(f"Matches: {matches}")

    print()

    # Example 10: Phone number matching
    # ---------------------------------
    # US phone number: XXX-XXX-XXXX
    pattern10 = r"\d{3}-\d{3}-\d{4}"
    text10 = "Call me at 555-123-4567 or 800-555-0199"

    phone_numbers = re.findall(pattern10, text10)
    print(f"Text: '{text10}'")
    print(f"Pattern: '\\d{{3}}-\\d{{3}}-\\d{{4}}' (phone format)")
    print(f"Phone numbers: {phone_numbers}")

    print()

    # ==============================================================================
    # SECTION 4: GREEDY VS NON-GREEDY MATCHING
    # ==============================================================================

    """
    GREEDY MATCHING (default):
    - Quantifiers (*, +, {m,n}) match as MUCH text as possible
    - They try to consume the maximum amount of characters

    NON-GREEDY (or LAZY) MATCHING:
    - Add ? after the quantifier: *?, +?, {m,n}?
    - They match as LITTLE text as possible
    - They try to consume the minimum amount of characters
    """

    print("="*70)
    print("SECTION 4: GREEDY VS NON-GREEDY MATCHING")
    print("="*70)

    # Example 11: Greedy matching demonstration
    # -----------------------------------------
    text11 = "<html><head><title>Page</title></head></html>"

    # Greedy: matches from first < to last >
    greedy_pattern = r"<.*>"
    greedy_match = re.search(greedy_pattern, text11)

    print(f"Text: '{text11}'")
    print(f"Greedy pattern: '<.*>' (. repeated, greedy)")
    if greedy_match:
        print(f"Matched: '{greedy_match.group()}'")
        print("(Matches everything from first < to last >)")

    print()

    # Example 12: Non-greedy matching demonstration
    # ---------------------------------------------
    # Non-greedy: matches from < to the nearest >
    non_greedy_pattern = r"<.*?>"
    non_greedy_matches = re.findall(non_greedy_pattern, text11)

    print(f"Text: '{text11}'")
    print(f"Non-greedy pattern: '<.*?>' (. repeated, non-greedy)")
    print(f"All matches: {non_greedy_matches}")
    print("(Each match is minimal - from < to nearest >)")

    print()

    # Example 13: Practical example - extracting quoted strings
    # ---------------------------------------------------------
    text13 = 'He said "Hello" and then "Goodbye"'

    # Greedy version - wrong!
    greedy_quotes = r'".*"'
    greedy_result = re.search(greedy_quotes, text13)

    print(f"Text: {text13}")
    print(f"\nGreedy '\".*\"':")
    if greedy_result:
        print(f"  Matched: {greedy_result.group()}")
        print("  (Oops! Got everything from first to last quote)")

    # Non-greedy version - correct!
    non_greedy_quotes = r'".*?"'
    non_greedy_results = re.findall(non_greedy_quotes, text13)

    print(f"\nNon-greedy '\".*?\"':")
    print(f"  Matched: {non_greedy_results}")
    print("  (Perfect! Got each quoted string separately)")

    print()

    # ==============================================================================
    # SECTION 5: COMBINING QUANTIFIERS
    # ==============================================================================

    print("="*70)
    print("SECTION 5: COMBINING QUANTIFIERS")
    print("="*70)

    # Example 14: Complex pattern with multiple quantifiers
    # -----------------------------------------------------
    # Match: one or more letters, optional spaces, one or more digits
    pattern14 = r"[a-zA-Z]+\s*\d+"
    text14 = "Room123 Building 456 Floor7"

    matches = re.findall(pattern14, text14)
    print(f"Text: '{text14}'")
    print(f"Pattern: '[a-zA-Z]+\\s*\\d+' (letters, optional space, digits)")
    print(f"Matches: {matches}")

    print()

    # Example 15: Email pattern (simplified)
    # --------------------------------------
    # Basic email: word chars, optional dots/underscores, @, domain
    pattern15 = r"[\w.]+@\w+\.\w+"
    text15 = "Contact: john.doe@example.com or alice_smith@test.org"

    emails = re.findall(pattern15, text15)
    print(f"Text: '{text15}'")
    print(f"Pattern: '[\\w.]+@\\w+\\.\\w+' (simple email)")
    print(f"Emails: {emails}")

    print()

    # Example 16: URL pattern (very simplified)
    # -----------------------------------------
    # Basic URL: http(s)://, optional www., domain, optional path
    pattern16 = r"https?://(?:www\.)?[\w.-]+\.[\w]+"
    text16 = "Visit https://example.com or http://www.test.org"

    urls = re.findall(pattern16, text16)
    print(f"Text: '{text16}'")
    print(f"URLs found: {urls}")

    print()

    # ==============================================================================
    # SECTION 6: PRACTICAL APPLICATIONS
    # ==============================================================================

    print("="*70)
    print("SECTION 6: PRACTICAL APPLICATIONS")
    print("="*70)

    # Example 17: Extracting prices
    # -----------------------------
    text17 = "Items: $12.99, $5.50, $100.00, and $0.99"

    # Pattern: dollar sign, digits, dot, two digits
    price_pattern = r"\$\d+\.\d{2}"
    prices = re.findall(price_pattern, text17)

    print(f"Text: '{text17}'")
    print(f"Prices found: {prices}")

    print()

    # Example 18: Matching dates (MM/DD/YYYY)
    # ---------------------------------------
    text18 = "Events: 01/15/2024, 12/31/2023, 06/01/2024"

    # Pattern: 2 digits / 2 digits / 4 digits
    date_pattern = r"\d{2}/\d{2}/\d{4}"
    dates = re.findall(date_pattern, text18)

    print(f"Text: '{text18}'")
    print(f"Dates found: {dates}")

    print()

    # Example 19: Extracting hashtags
    # -------------------------------
    text19 = "Love this! #python #coding #AI #MachineLearning"

    # Pattern: # followed by word characters
    hashtag_pattern = r"#\w+"
    hashtags = re.findall(hashtag_pattern, text19)

    print(f"Text: '{text19}'")
    print(f"Hashtags: {hashtags}")

    print()

    # Example 20: Validating password strength
    # ----------------------------------------
    def check_password_strength(password):
        """
        Check if password meets minimum requirements:
        - At least 8 characters
        - Contains at least one digit
        - Contains at least one letter
        """
        # Check length
        if len(password) < 8:
            return False, "Too short (minimum 8 characters)"

        # Check for at least one digit
        if not re.search(r"\d", password):
            return False, "Must contain at least one digit"

        # Check for at least one letter
        if not re.search(r"[a-zA-Z]", password):
            return False, "Must contain at least one letter"

        return True, "Password is strong enough"

    # Test passwords
    test_passwords = ["pass", "password", "pass123", "Pass123!", "12345678"]

    print("Password strength check:")
    for pwd in test_passwords:
        valid, message = check_password_strength(pwd)
        status = "✓" if valid else "✗"
        print(f"  {status} '{pwd}': {message}")

    print()

    # ==============================================================================
    # SECTION 7: COMMON PATTERNS
    # ==============================================================================

    print("="*70)
    print("SECTION 7: COMMON PATTERNS WITH QUANTIFIERS")
    print("="*70)

    common_patterns = {
        "Integer": r"\d+",
        "Decimal number": r"\d+\.\d+",
        "Word": r"\w+",
        "Line of text": r".+",
        "Whitespace sequence": r"\s+",
        "Variable name": r"[a-zA-Z_]\w*",
        "HTML tag": r"<\w+>",
        "IP address (simplified)": r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
    }

    print("Common regex patterns:")
    for name, pattern in common_patterns.items():
        print(f"  {name:25} : {pattern}")

    print()

    # ==============================================================================
    # SECTION 8: PERFORMANCE CONSIDERATIONS
    # ==============================================================================

    print("="*70)
    print("SECTION 8: PERFORMANCE AND BEST PRACTICES")
    print("="*70)

    """
    PERFORMANCE TIPS:

    1. Be as specific as possible
       - Use \d instead of [0-9]
       - Use \w instead of [a-zA-Z0-9_]

    2. Avoid excessive backtracking
       - BAD:  (a+)*     (nested quantifiers can be slow)
       - GOOD: a+        (single quantifier)

    3. Use non-greedy when appropriate
       - Helps avoid catastrophic backtracking
       - More predictable behavior

    4. Compile patterns for reuse
       - Use re.compile() for patterns used multiple times

    5. Use specific quantifiers
       - {3,5} is better than .{1,100} when you know the range
    """

    # Example 21: Compiling patterns for better performance
    # -----------------------------------------------------
    import time

    # Pattern to match email addresses
    email_pattern_string = r"[\w.+-]+@[\w-]+\.[\w.-]+"

    # Sample text with many emails
    text21 = "emails: " + " ".join([f"user{i}@example.com" for i in range(1000)])

    # Method 1: Without compilation
    start = time.time()
    matches1 = re.findall(email_pattern_string, text21)
    time1 = time.time() - start

    # Method 2: With compilation
    compiled_pattern = re.compile(email_pattern_string)
    start = time.time()
    matches2 = compiled_pattern.findall(text21)
    time2 = time.time() - start

    print("Performance comparison (finding 1000 emails):")
    print(f"  Without compilation: {time1:.6f} seconds")
    print(f"  With compilation:    {time2:.6f} seconds")
    print(f"  Speedup: {time1/time2:.2f}x faster")

    print()

    # ==============================================================================
    # SECTION 9: SUMMARY
    # ==============================================================================

    print("="*70)
    print("QUANTIFIER CHEAT SHEET")
    print("="*70)

    cheat_sheet = """
    BASIC QUANTIFIERS:
      *          0 or more (greedy)
      +          1 or more (greedy)
      ?          0 or 1 (optional)
      {m}        Exactly m times
      {m,n}      m to n times (inclusive)
      {m,}       m or more times
      {,n}       Up to n times

    NON-GREEDY (LAZY) VERSIONS:
      *?         0 or more (non-greedy)
      +?         1 or more (non-greedy)
      ??         0 or 1 (non-greedy)
      {m,n}?     m to n times (non-greedy)

    COMMON COMBINATIONS:
      \d+        One or more digits (number)
      \w+        One or more word characters (word)
      \s+        One or more whitespace
      .*         Any characters (greedy)
      .*?        Any characters (non-greedy)
      [a-z]+     One or more lowercase letters
      \d{3}      Exactly 3 digits
      \d{2,4}    2 to 4 digits

    KEY PRINCIPLES:
      1. Quantifiers apply to the element immediately before them
      2. Greedy quantifiers match as much as possible
      3. Non-greedy quantifiers match as little as possible
      4. Use specific quantifiers when you know the count
      5. Compile patterns for repeated use
    """

    print(cheat_sheet)

    # ==============================================================================
    # PRACTICE EXERCISES
    # ==============================================================================

    print("="*70)
    print("PRACTICE CHALLENGES")
    print("="*70)

    """
    Try these exercises:

    1. Match all words with 3-5 letters
    2. Extract all numbers (integers and decimals) from text
    3. Find all hashtags that are at least 3 characters long
    4. Match phone numbers in format: (XXX) XXX-XXXX
    5. Extract all HTML/XML tags (both opening and closing)
    6. Find all URLs starting with http:// or https://
    7. Match valid variable names (start with letter/underscore, then word chars)
    8. Extract all quoted strings (handle both single and double quotes)
    9. Find all email addresses in a document
    10. Match credit card numbers (XXXX-XXXX-XXXX-XXXX or 16 digits)

    Solutions in exercises_02_intermediate.py
    """

    # ==============================================================================
    # END OF TUTORIAL 03
    # ==============================================================================

    print("\n" + "="*70)
    print("END OF TUTORIAL - Quantifiers mastered!")
    print("Next: Tutorial 04 - Anchors and Boundaries")
    print("="*70)
```

---

## Exercises

**Exercise 1.**
Write a regex pattern that matches strings containing between 2 and 4 consecutive digits, but not more. For example, `"ab12cd"` should match the `"12"`, `"test1234end"` should match `"1234"`, but in `"12345"` the match should only capture `"1234"` (greedy) or `"12"` (lazy). Test both greedy and lazy versions.

??? success "Solution to Exercise 1"

    ```python
    import re

    # Greedy: matches as many digits as possible (up to 4)
    greedy = re.findall(r'\d{2,4}', "ab12cd test1234end 12345")
    print(f"Greedy: {greedy}")  # ['12', '1234', '1234']

    # Lazy: matches as few digits as possible (at least 2)
    lazy = re.findall(r'\d{2,4}?', "ab12cd test1234end 12345")
    print(f"Lazy: {lazy}")  # ['12', '12', '34', '12', '34']
    ```

---

**Exercise 2.**
Write a regex using `^` and `$` anchors to validate that a string is a valid username: 3-16 characters long, containing only letters, digits, underscores, and hyphens. Test against `"alice"`, `"a"`, `"valid_user-123"`, and `"invalid user"`.

??? success "Solution to Exercise 2"

    ```python
    import re

    pattern = r'^[a-zA-Z0-9_-]{3,16}$'

    tests = ["alice", "a", "valid_user-123", "invalid user", "ab"]
    for t in tests:
        valid = bool(re.fullmatch(pattern, t))
        print(f"'{t}': {'Valid' if valid else 'Invalid'}")
    # 'alice': Valid
    # 'a': Invalid (too short)
    # 'valid_user-123': Valid
    # 'invalid user': Invalid (contains space)
    # 'ab': Invalid (too short)
    ```

---

**Exercise 3.**
Write a regex using `\b` word boundaries to find all occurrences of words that are exactly 3 letters long in a text. For example, in `"The big cat sat on the mat"`, find `["The", "big", "cat", "sat", "the", "mat"]`.

??? success "Solution to Exercise 3"

    ```python
    import re

    pattern = r'\b\w{3}\b'
    text = "The big cat sat on the mat"
    matches = re.findall(pattern, text)
    print(matches)  # ['The', 'big', 'cat', 'sat', 'the', 'mat']
    ```
