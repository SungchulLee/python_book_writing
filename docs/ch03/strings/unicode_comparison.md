# Unicode Comparison Strategies

Python provides three levels of string comparison, each appropriate for
different situations.

!!! tip "Mental Model"
    String comparison has three levels of strictness: exact (`==`), normalized (same visual form), and case-folded (case-insensitive). Each level handles more real-world variation but requires more processing. Choose the simplest level that matches your requirements -- exact for internal keys, normalized for user input, case-folded for search.

---

## Level 1: Exact Comparison

Use `==` when both strings are known to be in the same Unicode form and
case matters:
```python
s1 = "café"
s2 = "café"

print(s1 == s2)  # True
```

This is the fastest approach but fails silently if the strings come from
different sources with different internal representations.

---

## Level 2: Unicode-Aware Case-Sensitive Comparison

Use `normalize()` when strings may have different internal representations
but case still matters:
```python
from unicodedata import normalize

def nfc_equal(s1, s2):
    return normalize("NFC", s1) == normalize("NFC", s2)

print(nfc_equal("café", "cafe\u0301"))  # True
print(nfc_equal("Café", "café"))        # False  (case-sensitive)
```

Typical use cases: comparing database keys, filenames, identifiers.

---

## Level 3: Unicode-Aware Case-Insensitive Comparison

Use `normalize()` combined with `casefold()` when strings may differ in
both representation and case:
```python
def fold_equal(s1, s2):
    return normalize("NFC", s1).casefold() == normalize("NFC", s2).casefold()

print(fold_equal("Café", "CAFÉ"))         # True
print(fold_equal("café", "cafe\u0301"))  # True
print(fold_equal("ß", "SS"))              # True
```

Typical use cases: user authentication, search queries, international names.

---

## Summary

| Level | Approach | Use When |
|-------|----------|----------|
| 1 | `s1 == s2` | Strings are ASCII or already normalized |
| 2 | `nfc_equal(s1, s2)` | Case matters, but representation may vary |
| 3 | `fold_equal(s1, s2)` | User-facing input, case and representation may vary |

Each level adds robustness at a small performance cost. For user-facing
comparison, always prefer Level 3.

---

## See Also

- [Unicode Normalization](unicode_normalization.md)
- [Unicode Case Folding](unicode_case_folding.md)

---

## Exercises


**Exercise 1.**
Demonstrate the three levels of Unicode string comparison (exact, normalized, fold-equal) by comparing `"Cafe\u0301"` with `"cafe"` at each level.

??? success "Solution to Exercise 1"

    ```python
    from unicodedata import normalize

    a = "Cafe\u0301"
    b = "cafe"

    # Level 1: Exact
    print(a == b)  # False

    # Level 2: Normalized (case-sensitive)
    print(normalize("NFC", a) == normalize("NFC", b))  # False

    # Level 3: Fold-equal (case-insensitive)
    print(normalize("NFC", a).casefold() == normalize("NFC", b).casefold())  # True
    ```

    Level 1 fails because representations differ. Level 2 fails because case differs. Level 3 succeeds by handling both differences.

---

**Exercise 2.**
Write a function that takes a list of Unicode strings and returns them deduplicated using NFC normalization. For example, `["cafe\u0301", "caf\u00e9"]` should return a single entry.

??? success "Solution to Exercise 2"

    ```python
    from unicodedata import normalize

    def deduplicate(strings):
        seen = set()
        result = []
        for s in strings:
            normalized = normalize("NFC", s)
            if normalized not in seen:
                seen.add(normalized)
                result.append(s)
        return result

    strings = ["cafe\u0301", "caf\u00e9", "hello", "cafe\u0301"]
    print(deduplicate(strings))  # Two unique entries
    ```

    By normalizing strings before adding to the set, visually identical strings with different internal representations are treated as duplicates.

---

**Exercise 3.**
Explain when you would use Level 1 (exact), Level 2 (normalized), and Level 3 (fold-equal) comparison. Give a practical example for each level.

??? success "Solution to Exercise 3"

    Level 1 (exact `==`): comparing strings you control, like dictionary keys that were all created in the same way. Example: checking if a config key matches a known constant.

    Level 2 (normalized): comparing identifiers or filenames from different sources where case matters but representation may vary. Example: matching database keys.

    Level 3 (fold-equal): user-facing search or authentication where both case and representation can vary. Example: searching a user directory by name.
