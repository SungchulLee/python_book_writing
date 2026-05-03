# Groups and Capturing

!!! tip "Mental Model"
    Parentheses in regex do double duty: they *group* tokens so quantifiers and alternation apply to the whole unit, and they *capture* the matched text so you can extract it later. Named groups (`(?P<name>...)`) add a label for clarity. If you only need grouping without capturing, use `(?:...)` to avoid cluttering your match results.

## Capturing Groups

Parentheses `(...)` serve two purposes in regex: **grouping** (treating multiple tokens as a unit) and **capturing** (extracting the matched substring).

```python
import re

text = "2024-01-15"
match = re.search(r'(\d{4})-(\d{2})-(\d{2})', text)

print(match.group(0))   # '2024-01-15'  — full match
print(match.group(1))   # '2024'        — first group (year)
print(match.group(2))   # '01'          — second group (month)
print(match.group(3))   # '15'          — third group (day)
print(match.groups())   # ('2024', '01', '15')
```

Groups are numbered left to right by their **opening parenthesis**:

```python
import re

# Groups numbered by opening parenthesis position
#       1         2    3
match = re.search(r'((a)(b))', 'ab')
print(match.group(1))  # 'ab'  — outer group
print(match.group(2))  # 'a'   — first inner
print(match.group(3))  # 'b'   — second inner
```

## `findall()` with Groups

When a pattern contains capturing groups, `re.findall()` returns the **group contents** instead of the full match:

```python
import re

text = "2024-01-15 and 2024-12-31"

# No groups — returns full matches
re.findall(r'\d{4}-\d{2}-\d{2}', text)
# ['2024-01-15', '2024-12-31']

# One group — returns list of strings (the group)
re.findall(r'(\d{4})-\d{2}-\d{2}', text)
# ['2024', '2024']

# Multiple groups — returns list of tuples
re.findall(r'(\d{4})-(\d{2})-(\d{2})', text)
# [('2024', '01', '15'), ('2024', '12', '31')]
```

!!! warning "`findall()` Behavior Changes with Groups"
    This is a common source of confusion. If you want the full match but also need groups, use `re.finditer()` and access both `.group(0)` and `.groups()`.

## Non-Capturing Groups

Use `(?:...)` when you need grouping for quantifiers or alternation but do **not** need to capture:

```python
import re

text = "gray grey"

# Capturing group — findall returns group content
re.findall(r'gr(a|e)y', text)
# ['a', 'e']

# Non-capturing group — findall returns full match
re.findall(r'gr(?:a|e)y', text)
# ['gray', 'grey']
```

Non-capturing groups are useful for applying quantifiers to a sub-pattern:

```python
import re

# Match repeated word patterns
re.findall(r'(?:ha)+', 'hahaha haha ha')
# ['hahaha', 'haha', 'ha']

# Optional prefix
re.findall(r'(?:un)?happy', 'happy unhappy')
# ['happy', 'unhappy']
```

## Named Groups

Named groups use the syntax `(?P<name>...)` and can be accessed by name via `.group('name')` or `.groupdict()`:

```python
import re

text = "2024-01-15"
match = re.search(r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})', text)

print(match.group('year'))   # '2024'
print(match.group('month'))  # '01'
print(match.group('day'))    # '15'
print(match.groupdict())     # {'year': '2024', 'month': '01', 'day': '15'}
```

Named groups improve readability, especially in complex patterns:

```python
import re

log = '192.168.1.100 - - [15/Jan/2024:10:30:45] "GET /index.html HTTP/1.1" 200 1234'

pattern = r'(?P<ip>[\d.]+) .+ \[(?P<date>[^\]]+)\] "(?P<method>\w+) (?P<path>\S+)'
match = re.search(pattern, log)

if match:
    info = match.groupdict()
    print(info)
    # {'ip': '192.168.1.100', 'date': '15/Jan/2024:10:30:45',
    #  'method': 'GET', 'path': '/index.html'}
```

## Backreferences

Backreferences match the **same text** that was previously captured by a group. Use `\1`, `\2`, etc. (or `(?P=name)` for named groups):

```python
import re

# Find repeated words
text = "the the cat sat on on the mat"
re.findall(r'\b(\w+)\s+\1\b', text)
# ['the', 'on']

# Find matching HTML tags
html = '<b>bold</b> <i>italic</i> <b>mismatch</i>'
re.findall(r'<(\w+)>.*?</\1>', html)
# ['b', 'i']  — only properly closed tags
```

Named backreference:

```python
import re

# Detect repeated words using named groups
text = "the the quick quick fox"
re.findall(r'\b(?P<word>\w+)\s+(?P=word)\b', text)
# ['the', 'quick']
```

## Groups with Quantifiers

When a group is inside a quantifier, only the **last** iteration is captured:

```python
import re

# Only the last repetition is captured
match = re.search(r'(\d)+', '12345')
print(match.group(0))  # '12345' — full match
print(match.group(1))  # '5'     — only the last digit captured

# To capture all, put the quantifier inside the group
match = re.search(r'(\d+)', '12345')
print(match.group(1))  # '12345'
```

## Practical Examples

### Parsing Key-Value Pairs

```python
import re

config = "host=localhost port=5432 db=mydb user=admin"
pairs = re.findall(r'(\w+)=(\S+)', config)
print(pairs)
# [('host', 'localhost'), ('port', '5432'), ('db', 'mydb'), ('user', 'admin')]
print(dict(pairs))
# {'host': 'localhost', 'port': '5432', 'db': 'mydb', 'user': 'admin'}
```

### Swapping Name Order

```python
import re

names = "Smith, John\nDoe, Jane\nLee, Alice"
# Swap "Last, First" to "First Last"
result = re.sub(r'(\w+), (\w+)', r'\2 \1', names)
print(result)
# John Smith
# Jane Doe
# Alice Lee
```

### Extracting URLs

```python
import re

text = "Visit https://example.com or http://test.org/page?q=1"
urls = re.findall(r'https?://\S+', text)
print(urls)
# ['https://example.com', 'http://test.org/page?q=1']

# With named groups for parts
pattern = r'(?P<scheme>https?)://(?P<host>[\w.]+)(?P<path>/\S*)?'
for m in re.finditer(pattern, text):
    print(m.groupdict())
# {'scheme': 'https', 'host': 'example.com', 'path': None}
# {'scheme': 'http', 'host': 'test.org', 'path': '/page?q=1'}
```

## Summary

| Concept | Syntax | Key Takeaway |
|---|---|---|
| Capturing group | `(...)` | Groups and captures; accessed by number |
| Non-capturing | `(?:...)` | Groups without capturing |
| Named group | `(?P<name>...)` | Capture accessible by name |
| Backreference | `\1` or `(?P=name)` | Matches same text as a previous group |
| `findall` + groups | — | Returns group contents, not full match |
| `groupdict()` | — | Dictionary of named groups |

---

## Runnable Example: `groups_capturing_tutorial.py`

```python
"""
Python Regular Expressions - Tutorial 05: Groups and Capturing
==============================================================

LEARNING OBJECTIVES:
-------------------
1. Understand capturing groups () and their uses
2. Use non-capturing groups (?:) for grouping without capture
3. Work with named groups (?P<name>) for readability
4. Extract data using groups with match.group()
5. Use backreferences to match repeated patterns
6. Apply groups in re.sub() for replacements

PREREQUISITES:
-------------
- Tutorials 01-04 (Basics through Anchors)

DIFFICULTY: INTERMEDIATE
"""

import re

# ==============================================================================
# SECTION 1: INTRODUCTION TO GROUPS
# ==============================================================================

if __name__ == "__main__":

    """
    GROUPS allow you to:
    1. Capture parts of a match for extraction
    2. Apply quantifiers to multiple characters
    3. Create alternatives with | (OR operator)
    4. Reference captured text later (backreferences)

    Syntax:
      (pattern)         Capturing group
      (?:pattern)       Non-capturing group  
      (?P<name>pattern) Named capturing group
    """

    print("="*70)
    print("SECTION 1: BASIC CAPTURING GROUPS")
    print("="*70)

    # Example 1: Simple capturing group
    # ---------------------------------
    text1 = "My phone is 555-1234"

    # Capture the phone number
    pattern1 = r"(\d{3}-\d{4})"
    match = re.search(pattern1, text1)

    if match:
        print(f"Text: '{text1}'")
        print(f"Full match: '{match.group(0)}'")  # group(0) is always the full match
        print(f"Group 1: '{match.group(1)}'")     # group(1) is first captured group

    print()

    # Example 2: Multiple capturing groups
    # ------------------------------------
    text2 = "John Doe, age 30"

    # Capture first name, last name, and age
    pattern2 = r"(\w+) (\w+), age (\d+)"
    match2 = re.search(pattern2, text2)

    if match2:
        print(f"Text: '{text2}'")
        print(f"Full match: '{match2.group(0)}'")
        print(f"First name (group 1): '{match2.group(1)}'")
        print(f"Last name (group 2): '{match2.group(2)}'")
        print(f"Age (group 3): '{match2.group(3)}'")

        # Can also use groups() to get all groups as tuple
        print(f"All groups: {match2.groups()}")

    print()

    # Example 3: Using groups with findall()
    # --------------------------------------
    """
    When using findall() with groups:
    - If pattern has groups, findall() returns tuples of groups
    - If no groups, findall() returns list of strings
    """

    text3 = "Emails: john@example.com, alice@test.org"

    # Pattern with groups: username and domain
    pattern3 = r"(\w+)@([\w.]+)"
    matches = re.findall(pattern3, text3)

    print(f"Text: '{text3}'")
    print("Email parts (username, domain):")
    for username, domain in matches:
        print(f"  {username} @ {domain}")

    print()

    # ==============================================================================
    # SECTION 2: NON-CAPTURING GROUPS
    # ==============================================================================

    """
    NON-CAPTURING GROUPS (?:...) group elements but don't capture them.
    Use when you need grouping for quantifiers or alternatives,
    but don't need to extract the matched text.
    """

    print("="*70)
    print("SECTION 2: NON-CAPTURING GROUPS")
    print("="*70)

    # Example 4: Capturing vs non-capturing
    # -------------------------------------
    text4 = "cat dog cat"

    # With capturing group
    pattern_capture = r"(cat|dog)"
    matches_capture = re.findall(pattern_capture, text4)
    print("With capturing group (cat|dog):")
    print(f"  Result: {matches_capture}")

    # With non-capturing group
    pattern_no_capture = r"(?:cat|dog)"
    matches_no_capture = re.findall(pattern_no_capture, text4)
    print("With non-capturing group (?:cat|dog):")
    print(f"  Result: {matches_no_capture}")
    print("  (Same result, but more efficient)")

    print()

    # Example 5: Practical use of non-capturing groups
    # -----------------------------------------------
    """
    Extract phone numbers, but don't capture area code separately
    when you only care about the full number.
    """

    text5 = "Call 800-555-1234 or 888-555-5678"

    # Capture only the full number, group area code without capturing
    pattern5 = r"((?:\d{3})-\d{3}-\d{4})"
    matches5 = re.findall(pattern5, text5)

    print(f"Text: '{text5}'")
    print(f"Phone numbers: {matches5}")
    print("(Area code grouped but not captured separately)")

    print()

    # ==============================================================================
    # SECTION 3: NAMED GROUPS
    # ==============================================================================

    """
    NAMED GROUPS (?P<name>...) let you refer to groups by name instead of number.
    This makes patterns more readable and maintainable.

    Syntax: (?P<name>pattern)
    Access: match.group('name')
    """

    print("="*70)
    print("SECTION 3: NAMED CAPTURING GROUPS")
    print("="*70)

    # Example 6: Basic named groups
    # -----------------------------
    text6 = "2024-03-15"

    # Named groups for date parts
    pattern6 = r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})"
    match6 = re.search(pattern6, text6)

    if match6:
        print(f"Date: '{text6}'")
        print(f"Year: {match6.group('year')}")
        print(f"Month: {match6.group('month')}")
        print(f"Day: {match6.group('day')}")

        # Can also access by number
        print(f"Year (by index): {match6.group(1)}")

        # Get dict of all named groups
        print(f"As dict: {match6.groupdict()}")

    print()

    # Example 7: Practical parsing with named groups
    # ----------------------------------------------
    log_line = "2024-03-15 14:30:45 ERROR User authentication failed"

    # Parse log entry with named groups
    log_pattern = r"(?P<date>\S+) (?P<time>\S+) (?P<level>\w+) (?P<message>.+)"
    log_match = re.search(log_pattern, log_line)

    if log_match:
        print("Log entry parsing:")
        log_data = log_match.groupdict()
        for key, value in log_data.items():
            print(f"  {key}: {value}")

    print()

    # ==============================================================================
    # SECTION 4: BACKREFERENCES
    # ==============================================================================

    """
    BACKREFERENCES let you match the same text that was captured earlier.
    - \\1, \\2, etc.: Reference captured groups by number
    - (?P=name): Reference named groups

    Useful for finding repeated patterns, palindromes, matching tags, etc.
    """

    print("="*70)
    print("SECTION 4: BACKREFERENCES")
    print("="*70)

    # Example 8: Finding repeated words
    # ---------------------------------
    text8 = "the the cat sat on the the mat"

    # Match repeated words
    pattern8 = r"\b(\w+)\s+\1\b"  # \1 refers to group 1
    matches8 = re.findall(pattern8, text8)

    print(f"Text: '{text8}'")
    print(f"Repeated words: {matches8}")

    print()

    # Example 9: Matching HTML/XML tags
    # ---------------------------------
    html = "<div>Content</div> <span>Text</span> <p>Wrong</div>"

    # Match properly closed tags
    pattern9 = r"<(\w+)>.*?</\1>"  # \1 matches the same tag name
    proper_tags = re.findall(pattern9, html)

    print(f"HTML: {html}")
    print(f"Properly closed tags: {proper_tags}")

    print()

    # Example 10: Named group backreferences
    # --------------------------------------
    text10 = "hello hello world world"

    # Using named groups and backreferences
    pattern10 = r"\b(?P<word>\w+)\s+(?P=word)\b"
    matches10 = re.finditer(pattern10, text10)

    print(f"Text: '{text10}'")
    print("Repeated words (using named groups):")
    for match in matches10:
        print(f"  {match.group('word')}")

    print()

    # ==============================================================================
    # SECTION 5: GROUPS IN SUBSTITUTION
    # ==============================================================================

    """
    Groups are very powerful in re.sub() for transforming text.
    You can reference captured groups in the replacement string.
    """

    print("="*70)
    print("SECTION 5: USING GROUPS IN re.sub()")
    print("="*70)

    # Example 11: Swapping parts of text
    # ----------------------------------
    text11 = "Doe, John"

    # Swap last name and first name
    pattern11 = r"(\w+), (\w+)"
    result11 = re.sub(pattern11, r"\2 \1", text11)  # \2 \1 swaps the groups

    print(f"Original: '{text11}'")
    print(f"Swapped: '{result11}'")

    print()

    # Example 12: Formatting phone numbers
    # ------------------------------------
    text12 = "800-555-1234 and 888-555-5678"

    # Change format from XXX-XXX-XXXX to (XXX) XXX-XXXX
    pattern12 = r"(\d{3})-(\d{3})-(\d{4})"
    result12 = re.sub(pattern12, r"(\1) \2-\3", text12)

    print(f"Original: '{text12}'")
    print(f"Formatted: '{result12}'")

    print()

    # Example 13: Using named groups in substitution
    # ----------------------------------------------
    text13 = "Price: $100.00"

    # Extract and reformat using named groups
    pattern13 = r"\$(?P<dollars>\d+)\.(?P<cents>\d{2})"
    result13 = re.sub(pattern13, r"\g<dollars> dollars and \g<cents> cents", text13)

    print(f"Original: '{text13}'")
    print(f"Converted: '{result13}'")
    print("(Note: Use \\g<name> for named groups in replacement)")

    print()

    # ==============================================================================
    # SECTION 6: PRACTICAL APPLICATIONS
    # ==============================================================================

    print("="*70)
    print("SECTION 6: PRACTICAL APPLICATIONS")
    print("="*70)

    # Example 14: Parsing email addresses
    # -----------------------------------
    def parse_email(email):
        pattern = r"(?P<user>[\w.+-]+)@(?P<domain>[\w.-]+)\.(?P<tld>\w+)"
        match = re.match(pattern, email)
        if match:
            return match.groupdict()
        return None

    emails = ["john.doe@example.com", "user+tag@test.co.uk"]
    print("Email parsing:")
    for email in emails:
        parts = parse_email(email)
        if parts:
            print(f"  {email}:")
            print(f"    User: {parts['user']}")
            print(f"    Domain: {parts['domain']}")
            print(f"    TLD: {parts['tld']}")

    print()

    # Example 15: Extracting URLs components
    # --------------------------------------
    url = "https://www.example.com:8080/path/to/page?query=value#section"

    url_pattern = r"(?P<protocol>https?://)?(?P<subdomain>www\.)?(?P<domain>[\w.-]+)(?::(?P<port>\d+))?(?P<path>/[\w/.-]*)?(?:\?(?P<query>[\w=&]+))?(?:#(?P<fragment>\w+))?"

    match = re.search(url_pattern, url)
    if match:
        print(f"URL: {url}")
        print("Components:")
        for key, value in match.groupdict().items():
            if value:
                print(f"  {key}: {value}")

    print()

    # ==============================================================================
    # SECTION 7: SUMMARY
    # ==============================================================================

    print("="*70)
    print("GROUPS CHEAT SHEET")
    print("="*70)

    cheat_sheet = """
    CAPTURING GROUPS:
      (pattern)              Capture matched text
      \1, \2, \3             Reference captured groups
      match.group(1)         Access group 1
      match.groups()         Get all groups as tuple

    NON-CAPTURING GROUPS:
      (?:pattern)            Group without capturing

    NAMED GROUPS:
      (?P<name>pattern)      Named capturing group
      (?P=name)              Named backreference
      match.group('name')    Access named group
      match.groupdict()      Get dict of named groups

    IN SUBSTITUTION:
      \1, \2, \3             Reference numbered groups
      \g<name>               Reference named groups
      \g<1>                  Alternative numeric reference

    COMMON USES:
      (cat|dog)              Alternatives
      (\w+)\s+\1             Repeated words
      <(\w+)>.*?</\1>        Matching tags
      (\d{3})-(\d{4})        Capture phone parts

    KEY POINTS:
      - Group 0 is always the full match
      - Groups are numbered from 1
      - Use (?:...) when you don't need to capture
      - Named groups improve readability
      - Backreferences match the same text again
    """

    print(cheat_sheet)

    print("\n" + "="*70)
    print("END OF TUTORIAL - Groups and Capturing mastered!")
    print("Next: Tutorial 06 - Lookahead and Lookbehind")
    print("="*70)
```

---

## Exercises

**Exercise 1.**
Write a regex with named groups to parse a log entry in the format `"[2024-12-25 14:30:00] ERROR: Connection timeout"`. Capture the date, time, level, and message as named groups. Test with `re.search` and access each group by name.

??? success "Solution to Exercise 1"

    ```python
    import re

    pattern = r'\[(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d{2}:\d{2}:\d{2})\] (?P<level>\w+): (?P<message>.+)'
    log = "[2024-12-25 14:30:00] ERROR: Connection timeout"
    match = re.search(pattern, log)

    if match:
        print(f"Date: {match.group('date')}")     # 2024-12-25
        print(f"Time: {match.group('time')}")     # 14:30:00
        print(f"Level: {match.group('level')}")   # ERROR
        print(f"Message: {match.group('message')}")  # Connection timeout
    ```

---

**Exercise 2.**
Write a regex that uses a non-capturing group to match URLs that start with either `http` or `https`, and a capturing group to extract the domain name. For example, from `"https://www.example.com/path"`, capture `"www.example.com"`.

??? success "Solution to Exercise 2"

    ```python
    import re

    pattern = r'(?:https?)://([^/]+)'
    urls = [
        "https://www.example.com/path",
        "http://api.test.org/data",
    ]
    for url in urls:
        match = re.search(pattern, url)
        if match:
            print(f"Domain: {match.group(1)}")
    # Domain: www.example.com
    # Domain: api.test.org
    ```

---

**Exercise 3.**
Write a regex that uses backreferences to find repeated words in a text (e.g., `"the the"` or `"is is"`). The pattern should match a word followed by whitespace and then the same word again. Test with `"The the cat sat on on the mat"`.

??? success "Solution to Exercise 3"

    ```python
    import re

    pattern = r'\b(\w+)\s+\1\b'
    text = "The the cat sat on on the mat"
    matches = re.findall(pattern, text, re.IGNORECASE)
    print(matches)  # ['The', 'on']
    ```
