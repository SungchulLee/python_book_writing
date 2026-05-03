# Character Classes

!!! tip "Mental Model"
    A character class is a single-character menu: `[aeiou]` means "match exactly one character, and it must be one of these." Ranges like `[a-z]` and shorthands like `\d` (digits) are just compact ways to define the menu. Negation (`[^...]`) flips the menu into "match anything *except* these."

## What Is a Character Class?

A **character class** (also called a character set) matches **one character** from a defined set. Character classes are enclosed in square brackets `[...]`.

```python
import re

# Match any vowel
re.findall(r'[aeiou]', 'Hello World')
# ['e', 'o', 'o']

# Match any digit
re.findall(r'[0123456789]', 'Room 404')
# ['4', '0', '4']
```

## Ranges

Use a hyphen `-` inside brackets to specify a range of characters:

```python
import re

text = "Agent 007 has clearance Level-A3"

# Digit range (equivalent to \d)
re.findall(r'[0-9]', text)
# ['0', '0', '7', '3']

# Lowercase letters
re.findall(r'[a-z]+', text)
# ['gent', 'has', 'clearance', 'evel']

# Uppercase letters
re.findall(r'[A-Z]+', text)
# ['A', 'L', 'A']

# Letters and digits combined
re.findall(r'[a-zA-Z0-9]+', text)
# ['Agent', '007', 'has', 'clearance', 'Level', 'A3']
```

Multiple ranges can be combined in a single class:

```python
# Hexadecimal digits
re.findall(r'[0-9a-fA-F]+', '0xFF 0x1A 255 0xGG')
# ['0', 'FF', '0', '1A', '255', '0', 'GG' won't match fully]
# Actually:
re.findall(r'[0-9a-fA-F]+', '0xFF 0x1A 255 0xGG')
# ['0', 'FF', '0', '1A', '255', '0']
```

## Negated Character Classes

A caret `^` at the **beginning** of a character class negates it — matching any character **not** in the set:

```python
import re

# Match non-digits
re.findall(r'[^0-9]+', 'Room 404 is on Floor 4')
# ['Room ', ' is on Floor ']

# Match non-vowels
re.findall(r'[^aeiouAEIOU]+', 'Hello World')
# ['H', 'll', ' W', 'rld']

# Match non-whitespace (similar to \S)
re.findall(r'[^ \t\n]+', 'hello   world')
# ['hello', 'world']
```

!!! note "Caret Position Matters"
    The `^` only negates when it appears as the **first** character inside `[...]`. Elsewhere, it matches a literal caret: `[a^b]` matches `a`, `^`, or `b`.

## Special Characters Inside Classes

Most metacharacters lose their special meaning inside character classes. Only a few remain special:

| Character | Special inside `[...]`? | How to use literally |
|---|---|---|
| `]` | Yes — closes the class | `\]` or place first: `[]abc]` |
| `\` | Yes — escape character | `\\` |
| `^` | Yes — negation (only if first) | Place after first position: `[a^b]` |
| `-` | Yes — range operator | `\-` or place first/last: `[-abc]` or `[abc-]` |

```python
import re

# Match literal special characters
re.findall(r'[\[\]]', 'array[0] = list[1]')
# ['[', ']', '[', ']']

# Hyphen at end — matches literal hyphen
re.findall(r'[a-z-]+', 'well-known self-driving')
# ['well-known', 'self-driving']

# Dot inside class — just a literal dot
re.findall(r'[.]', 'version 3.14')
# ['.']
```

## Shorthand Classes vs Bracket Notation

The shorthand classes `\d`, `\w`, `\s` and their negations can be used inside character classes:

```python
import re

# Digits or hyphens (for phone numbers)
re.findall(r'[\d-]+', 'Call 555-123-4567 today')
# ['555-123-4567']

# Word characters or dots (for filenames)
re.findall(r'[\w.]+', 'file_v2.py and data.csv')
# ['file_v2.py', 'and', 'data.csv']

# Digits and whitespace
re.findall(r'[\d\s]+', 'score: 42 out of 50')
# [' 42 ', ' 50']
```

## POSIX-like Classes (Unicode)

Python's `\d`, `\w`, and `\s` match Unicode characters by default. Use the `re.ASCII` flag to restrict to ASCII:

```python
import re

# \d matches Unicode digits by default
re.findall(r'\d+', '123 ١٢٣ ୧୨୩')
# ['123', '١٢٣', '୧୨୩']

# Restrict to ASCII digits
re.findall(r'\d+', '123 ١٢٣ ୧୨୩', re.ASCII)
# ['123']
```

## Practical Examples

### Matching Identifiers

A valid Python identifier starts with a letter or underscore, followed by letters, digits, or underscores:

```python
import re

text = "x = 42; _name = 'hello'; 3bad = True"
re.findall(r'[a-zA-Z_]\w*', text)
# ['x', '_name', 'hello', 'bad', 'True']
```

### Extracting Vowels and Consonants

```python
import re

word = "Mississippi"
vowels = re.findall(r'[aeiouAEIOU]', word)
consonants = re.findall(r'[^aeiouAEIOU]', word)

print(f"Vowels: {vowels}")       # ['i', 'i', 'i', 'i']
print(f"Consonants: {consonants}")  # ['M', 's', 's', 's', 's', 'p', 'p']
```

### Matching Hex Color Codes

```python
import re

css = "color: #FF5733; background: #0a0; border: #12ab"
# Full 6-digit or 3-digit hex codes
re.findall(r'#[0-9a-fA-F]{3,6}\b', css)
# ['#FF5733', '#0a0', '#12ab']

# Strictly 6-digit or 3-digit
re.findall(r'#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b', css)
# ['#FF5733', '#0a0']
```

## Summary

| Concept | Key Takeaway |
|---|---|
| `[abc]` | Matches one character: `a`, `b`, or `c` |
| `[a-z]` | Matches one character in the range `a` to `z` |
| `[^abc]` | Matches one character **not** in the set |
| `-` in class | Range operator; literal if first or last |
| `^` in class | Negation only if first character |
| Metacharacters | Most lose special meaning inside `[...]` |
| `\d \w \s` | Can be used inside character classes |

---

## Runnable Example: `character_classes_tutorial.py`

```python
"""
Python Regular Expressions - Tutorial 02: Character Classes
===========================================================

LEARNING OBJECTIVES:
-------------------
1. Understand character classes and their syntax
2. Use predefined character classes (\d, \w, \s, etc.)
3. Create custom character classes with [...]
4. Use character ranges [a-z], [0-9]
5. Understand negated character classes [^...]
6. Combine character classes for complex matching

PREREQUISITES:
-------------
- Tutorial 01: Regex Basics
- Understanding of re.match(), re.search(), re.findall()

DIFFICULTY: BEGINNER
"""

import re

# ==============================================================================
# SECTION 1: INTRODUCTION TO CHARACTER CLASSES
# ==============================================================================

if __name__ == "__main__":

    """
    CHARACTER CLASSES allow you to match one character from a set of characters.
    Instead of matching exact text, you can match "any digit" or "any letter".

    Basic Syntax:
    - [abc]   : Matches 'a', 'b', OR 'c' (any single character from the set)
    - [^abc]  : Matches any character EXCEPT 'a', 'b', or 'c'
    - [a-z]   : Matches any lowercase letter from 'a' to 'z'
    - [0-9]   : Matches any digit from '0' to '9'

    This is much more powerful than literal matching!
    """

    print("="*70)
    print("SECTION 1: BASIC CHARACTER CLASSES")
    print("="*70)

    # Example 1: Simple character class
    # ---------------------------------
    # Match a single vowel
    pattern1 = r"[aeiou]"  # Matches any single vowel
    text1 = "hello world"

    vowels = re.findall(pattern1, text1)
    print(f"Text: '{text1}'")
    print(f"Pattern: '{pattern1}' (matches any vowel)")
    print(f"Matches found: {vowels}")
    print(f"Total vowels: {len(vowels)}")

    print()

    # Example 2: Matching specific characters
    # ---------------------------------------
    # Match only the letters 'c', 'a', 't'
    pattern2 = r"[cat]"
    text2 = "the cat sat on the mat"

    matches = re.findall(pattern2, text2)
    print(f"Text: '{text2}'")
    print(f"Pattern: '{pattern2}' (matches 'c', 'a', or 't')")
    print(f"Matches: {matches}")
    print(f"Count: {len(matches)}")

    print()

    # ==============================================================================
    # SECTION 2: CHARACTER RANGES
    # ==============================================================================

    """
    RANGES allow you to specify a sequence of characters without listing them all.

    Common ranges:
    - [a-z]   : All lowercase letters
    - [A-Z]   : All uppercase letters
    - [0-9]   : All digits
    - [a-zA-Z]: All letters (upper and lower)
    - [a-z0-9]: All lowercase letters and digits
    """

    print("="*70)
    print("SECTION 2: CHARACTER RANGES")
    print("="*70)

    # Example 3: Matching lowercase letters
    # -------------------------------------
    pattern3 = r"[a-z]"
    text3 = "Hello World 123"

    lowercase = re.findall(pattern3, text3)
    print(f"Text: '{text3}'")
    print(f"Pattern: '{pattern3}' (any lowercase letter)")
    print(f"Lowercase letters found: {lowercase}")

    print()

    # Example 4: Matching digits
    # --------------------------
    pattern4 = r"[0-9]"
    text4 = "Room 101, Floor 5, Building A"

    digits = re.findall(pattern4, text4)
    print(f"Text: '{text4}'")
    print(f"Pattern: '{pattern4}' (any digit)")
    print(f"Digits found: {digits}")

    print()

    # Example 5: Combining ranges
    # ---------------------------
    # Match any alphanumeric character (letter or digit)
    pattern5 = r"[a-zA-Z0-9]"
    text5 = "User123! #Password456"

    alphanum = re.findall(pattern5, text5)
    print(f"Text: '{text5}'")
    print(f"Pattern: '{pattern5}' (any letter or digit)")
    print(f"Alphanumeric characters: {alphanum}")
    print(f"Total: {len(alphanum)}")

    print()

    # ==============================================================================
    # SECTION 3: PREDEFINED CHARACTER CLASSES
    # ==============================================================================

    """
    Python regex provides SHORTHAND notations for common character classes:

    \d  : Digit [0-9]
    \D  : Non-digit [^0-9]
    \w  : Word character [a-zA-Z0-9_] (letters, digits, underscore)
    \W  : Non-word character [^a-zA-Z0-9_]
    \s  : Whitespace [ \t\n\r\f\v] (space, tab, newline, etc.)
    \S  : Non-whitespace [^ \t\n\r\f\v]

    These are very commonly used and make patterns more readable.
    """

    print("="*70)
    print("SECTION 3: PREDEFINED CHARACTER CLASSES")
    print("="*70)

    # Example 6: Using \d for digits
    # ------------------------------
    pattern6 = r"\d"  # Equivalent to [0-9]
    text6 = "I have 3 cats and 2 dogs"

    digits = re.findall(pattern6, text6)
    print(f"Text: '{text6}'")
    print(f"Pattern: '\\d' (any digit)")
    print(f"Digits: {digits}")

    print()

    # Example 7: Using \w for word characters
    # ---------------------------------------
    pattern7 = r"\w"  # Matches letters, digits, and underscore
    text7 = "hello_world123!@#"

    word_chars = re.findall(pattern7, text7)
    print(f"Text: '{text7}'")
    print(f"Pattern: '\\w' (word characters)")
    print(f"Word characters: {word_chars}")

    print()

    # Example 8: Using \s for whitespace
    # ----------------------------------
    pattern8 = r"\s"  # Matches spaces, tabs, newlines
    text8 = "hello\tworld\ntest"

    spaces = re.findall(pattern8, text8)
    print(f"Text: 'hello\\tworld\\ntest'")
    print(f"Pattern: '\\s' (whitespace)")
    print(f"Whitespace characters found: {len(spaces)}")
    print(f"Types: {repr(spaces)}")  # repr() shows special characters

    print()

    # Example 9: Using \D, \W, \S (negated versions)
    # ----------------------------------------------
    text9 = "hello123"

    # \D matches anything that's NOT a digit
    non_digits = re.findall(r"\D", text9)
    print(f"Text: '{text9}'")
    print(f"Pattern: '\\D' (non-digits)")
    print(f"Non-digit characters: {non_digits}")

    # \W matches anything that's NOT a word character
    text10 = "hello-world!"
    non_word = re.findall(r"\W", text10)
    print(f"\nText: '{text10}'")
    print(f"Pattern: '\\W' (non-word chars)")
    print(f"Non-word characters: {non_word}")

    # \S matches anything that's NOT whitespace
    text11 = "a b c"
    non_space = re.findall(r"\S", text11)
    print(f"\nText: '{text11}'")
    print(f"Pattern: '\\S' (non-whitespace)")
    print(f"Non-whitespace characters: {non_space}")

    print()

    # ==============================================================================
    # SECTION 4: NEGATED CHARACTER CLASSES
    # ==============================================================================

    """
    NEGATED CHARACTER CLASSES match any character EXCEPT those in the class.
    Syntax: [^characters]

    The ^ symbol at the START of a character class means "not".
    Note: This is different from ^ as an anchor (which we'll learn later).
    """

    print("="*70)
    print("SECTION 4: NEGATED CHARACTER CLASSES")
    print("="*70)

    # Example 10: Matching non-vowels
    # -------------------------------
    pattern10 = r"[^aeiou]"  # Matches anything that's NOT a vowel
    text10 = "hello"

    non_vowels = re.findall(pattern10, text10)
    print(f"Text: '{text10}'")
    print(f"Pattern: '[^aeiou]' (not a vowel)")
    print(f"Non-vowels: {non_vowels}")

    print()

    # Example 11: Matching non-digits
    # -------------------------------
    pattern11 = r"[^0-9]"  # Same as \D
    text11 = "Room 404"

    non_digits_custom = re.findall(pattern11, text11)
    print(f"Text: '{text11}'")
    print(f"Pattern: '[^0-9]' (not a digit)")
    print(f"Non-digits: {non_digits_custom}")

    print()

    # Example 12: Excluding specific characters
    # -----------------------------------------
    # Match any character except spaces and punctuation
    pattern12 = r"[^., ]"  # Not period, comma, or space
    text12 = "Hello, World. Test."

    chars = re.findall(pattern12, text12)
    print(f"Text: '{text12}'")
    print(f"Pattern: '[^., ]' (not period, comma, or space)")
    print(f"Characters: {chars}")

    print()

    # ==============================================================================
    # SECTION 5: THE DOT (.) METACHARACTER
    # ==============================================================================

    """
    The DOT (.) is a special metacharacter that matches ANY character except newline.
    It's like a wildcard - use it carefully!

    . : Matches any single character (except \n by default)
    """

    print("="*70)
    print("SECTION 5: THE DOT METACHARACTER")
    print("="*70)

    # Example 13: Using dot to match any character
    # --------------------------------------------
    pattern13 = r"c.t"  # 'c', followed by ANY character, followed by 't'
    text13 = "cat cut cot c t c9t"

    matches = re.findall(pattern13, text13)
    print(f"Text: '{text13}'")
    print(f"Pattern: 'c.t' ('c' + any char + 't')")
    print(f"Matches: {matches}")

    print()

    # Example 14: Dot doesn't match newline by default
    # ------------------------------------------------
    text14 = "hello\nworld"
    pattern14 = r"hello.world"

    match = re.search(pattern14, text14)
    print(f"Text: 'hello\\nworld'")
    print(f"Pattern: 'hello.world'")
    print(f"Match found: {match is not None}")
    print("(The dot doesn't match the newline by default)")

    print()

    # Example 15: Matching a literal dot
    # ----------------------------------
    # To match an actual period, escape it with backslash
    pattern15 = r"\."  # Matches a literal period
    text15 = "3.14 is pi"

    periods = re.findall(pattern15, text15)
    print(f"Text: '{text15}'")
    print(f"Pattern: '\\.' (literal period)")
    print(f"Periods found: {periods}")

    print()

    # ==============================================================================
    # SECTION 6: PRACTICAL EXAMPLES
    # ==============================================================================

    print("="*70)
    print("SECTION 6: PRACTICAL EXAMPLES")
    print("="*70)

    # Example 16: Extracting all words from text
    # ------------------------------------------
    text16 = "Hello, World! This is a test-123."

    # Match sequences of word characters
    words = re.findall(r"\w+", text16)  # \w+ means one or more word characters
    print(f"Text: '{text16}'")
    print(f"Words extracted: {words}")

    print()

    # Example 17: Finding phone number digits
    # ---------------------------------------
    text17 = "Call me at 555-1234 or 555-5678"

    # Extract all digit sequences
    numbers = re.findall(r"\d+", text17)  # \d+ means one or more digits
    print(f"Text: '{text17}'")
    print(f"Number sequences: {numbers}")

    print()

    # Example 18: Identifying non-alphanumeric characters
    # ---------------------------------------------------
    text18 = "email@domain.com"

    # Find all characters that are not letters or digits
    special_chars = re.findall(r"[^a-zA-Z0-9]", text18)
    print(f"Text: '{text18}'")
    print(f"Special characters: {special_chars}")

    print()

    # Example 19: Matching hex digits
    # -------------------------------
    # Hex digits are 0-9 and A-F (or a-f)
    pattern19 = r"[0-9A-Fa-f]"
    text19 = "Color: #FF5733, #00AAFF"

    hex_digits = re.findall(pattern19, text19)
    print(f"Text: '{text19}'")
    print(f"Hex digits: {hex_digits}")
    print(f"Total: {len(hex_digits)}")

    print()

    # Example 20: Validating single character input
    # ---------------------------------------------
    def validate_grade(grade):
        """
        Check if input is a valid letter grade (A, B, C, D, F).
        """
        # ^[ABCDF]$ would check if ENTIRE string is one of these letters
        # But we'll use match for simplicity here
        pattern = r"[ABCDF]"
        match = re.match(pattern, grade)
        return match is not None and len(grade) == 1

    # Test the function
    test_grades = ["A", "B", "C", "D", "F", "E", "Z", "AB"]
    print("Grade validation:")
    for grade in test_grades:
        result = "Valid" if validate_grade(grade) else "Invalid"
        print(f"  '{grade}': {result}")

    print()

    # ==============================================================================
    # SECTION 7: COMBINING CHARACTER CLASSES
    # ==============================================================================

    print("="*70)
    print("SECTION 7: COMBINING CHARACTER CLASSES")
    print("="*70)

    # Example 21: Complex character class
    # -----------------------------------
    # Match letters, digits, and specific symbols
    pattern21 = r"[a-zA-Z0-9_\-.]"  # Letters, digits, underscore, hyphen, period
    text21 = "user_name-123@domain.com"

    valid_chars = re.findall(pattern21, text21)
    print(f"Text: '{text21}'")
    print(f"Pattern: '[a-zA-Z0-9_\\-.]'")
    print(f"Valid characters: {valid_chars}")

    print()

    # Example 22: Using multiple character classes in one pattern
    # ----------------------------------------------------------
    # Match: digit, followed by any letter, followed by digit
    pattern22 = r"\d[a-zA-Z]\d"
    text22 = "Room 3A5, 4B7, and 2Z9"

    matches = re.findall(pattern22, text22)
    print(f"Text: '{text22}'")
    print(f"Pattern: '\\d[a-zA-Z]\\d' (digit-letter-digit)")
    print(f"Matches: {matches}")

    print()

    # ==============================================================================
    # SECTION 8: COMMON MISTAKES TO AVOID
    # ==============================================================================

    print("="*70)
    print("SECTION 8: COMMON MISTAKES TO AVOID")
    print("="*70)

    # Mistake 1: Forgetting to escape special characters in character class
    # --------------------------------------------------------------------
    print("Mistake 1: Special characters in character classes")

    # If you want to match a literal hyphen in a character class,
    # put it at the start or end, or escape it
    pattern_wrong = r"[a-z-0-9]"  # This is interpreted as range 'a' to 'z-0' to '9'
    pattern_right = r"[a-z0-9\-]"  # Escaped hyphen
    pattern_right2 = r"[-a-z0-9]"  # Hyphen at start

    text = "hello-world123"
    print(f"Text: '{text}'")
    print(f"Pattern '[a-z0-9\\-]': {re.findall(pattern_right, text)}")

    print()

    # Mistake 2: Confusing [^...] with \^
    # -----------------------------------
    print("Mistake 2: Understanding negation")
    print("  [^abc] means: match anything EXCEPT a, b, or c")
    print("  \\^ means: match a literal ^ character")

    text = "^hello"
    pattern_neg = r"[^h]"  # Matches anything except 'h'
    pattern_literal = r"\^"  # Matches literal ^

    print(f"Text: '{text}'")
    print(f"[^h]: {re.findall(pattern_neg, text)}")
    print(f"\\^: {re.findall(pattern_literal, text)}")

    print()

    # Mistake 3: Thinking . matches newline
    # -------------------------------------
    print("Mistake 3: The dot doesn't match newline by default")
    text_multiline = "line1\nline2"
    print(f"Text: 'line1\\nline2'")
    print(f"Pattern '.+': {re.findall(r'.+', text_multiline)}")
    print("(Each line matched separately, newline not included)")

    print()

    # ==============================================================================
    # SECTION 9: SUMMARY AND CHEAT SHEET
    # ==============================================================================

    print("="*70)
    print("SUMMARY: CHARACTER CLASS CHEAT SHEET")
    print("="*70)

    cheat_sheet = """
    BASIC CHARACTER CLASSES:
      [abc]         Match 'a', 'b', or 'c'
      [a-z]         Match any lowercase letter
      [A-Z]         Match any uppercase letter
      [0-9]         Match any digit
      [a-zA-Z]      Match any letter
      [a-zA-Z0-9]   Match any letter or digit

    NEGATED CLASSES:
      [^abc]        Match anything EXCEPT 'a', 'b', or 'c'
      [^0-9]        Match anything that's not a digit

    PREDEFINED CLASSES:
      \\d           Digit [0-9]
      \\D           Non-digit [^0-9]
      \\w           Word character [a-zA-Z0-9_]
      \\W           Non-word character
      \\s           Whitespace (space, tab, newline, etc.)
      \\S           Non-whitespace
      .            Any character except newline

    SPECIAL NOTES:
      - Always use raw strings: r"pattern"
      - Escape special chars in classes: [\\-\\.]
      - Put hyphen at start or end to match literally: [-abc] or [abc-]
      - ^ at START of class means negation: [^abc]
      - ^ elsewhere is literal: [a^bc]
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

    1. Write a pattern to match all vowels (both upper and lowercase)
    2. Extract all punctuation marks from a string
    3. Find all hexadecimal numbers (0-9, A-F, a-f)
    4. Match all characters that are NOT spaces or punctuation
    5. Create a pattern to match DNA sequences (only A, T, G, C)
    6. Extract all word characters followed by a digit
    7. Match all characters except vowels

    Solutions in exercises_01_basics.py
    """

    # ==============================================================================
    # END OF TUTORIAL 02
    # ==============================================================================

    print("\n" + "="*70)
    print("END OF TUTORIAL - Character Classes mastered!")
    print("Next: Tutorial 03 - Quantifiers")
    print("="*70)
```

---

## Exercises

**Exercise 1.**
Write a regex pattern that matches any string containing only lowercase letters and digits (no spaces, uppercase, or special characters). Test it against `"hello123"`, `"Hello"`, `"test!"`, and `"abc"`.

??? success "Solution to Exercise 1"

    ```python
    import re

    pattern = r'^[a-z0-9]+$'

    tests = ["hello123", "Hello", "test!", "abc"]
    for t in tests:
        match = re.fullmatch(pattern, t)
        print(f"'{t}': {'Match' if match else 'No match'}")
    # 'hello123': Match
    # 'Hello': No match
    # 'test!': No match
    # 'abc': Match
    ```

---

**Exercise 2.**
Write a regex pattern using a negated character class to find all characters in a string that are NOT alphanumeric or whitespace. For example, in `"Hello, World! #2024"`, it should find `[',', '!', '#']`.

??? success "Solution to Exercise 2"

    ```python
    import re

    text = "Hello, World! #2024"
    non_alnum = re.findall(r'[^\w\s]', text)
    print(non_alnum)  # [',', '!', '#']
    ```

---

**Exercise 3.**
Write a regex pattern that matches a valid hex color code: `#` followed by exactly 6 hexadecimal characters (digits and letters a-f, case-insensitive). Test against `"#FF5733"`, `"#abc"`, `"#12345G"`, and `"#aabbcc"`.

??? success "Solution to Exercise 3"

    ```python
    import re

    pattern = r'^#[0-9a-fA-F]{6}$'

    tests = ["#FF5733", "#abc", "#12345G", "#aabbcc"]
    for t in tests:
        match = re.fullmatch(pattern, t)
        print(f"'{t}': {'Valid' if match else 'Invalid'}")
    # '#FF5733': Valid
    # '#abc': Invalid (only 3 chars)
    # '#12345G': Invalid (G not hex)
    # '#aabbcc': Valid
    ```
