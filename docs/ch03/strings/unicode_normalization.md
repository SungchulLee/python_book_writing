# Unicode Normalization

Unicode allows multiple internal representations for text that looks identical.

For example, the character `é` may be stored in two different ways:

- as a single precomposed character: `U+00E9`
- as two code points: `U+0065` (`e`) followed by `U+0301` (combining acute accent)

These forms look the same to humans, but Python treats them as different strings:
```python
from unicodedata import normalize

s1 = "caf\u00e9"   # precomposed: é is one character (U+00E9)
s2 = "cafe\u0301"  # decomposed:  e + combining accent (two code points)

print(s1 == s2)    # False
print(len(s1))     # 4
print(len(s2))     # 5
```

The two strings look identical when printed, but have different lengths -- proof
that they are internally different.

!!! tip "Mental Model"
    Unicode normalization collapses equivalent representations into a single canonical form. NFC composes characters (e + accent becomes one code point), NFD decomposes them (one accented character becomes base + accent). Always normalize before comparing or hashing strings from external sources, because two visually identical strings may have different code point sequences.

---

## Why This Happens

Unicode separates **visual appearance** from **code point sequence**. Two strings
may render identically while having entirely different internal representations:

| String | Internal Representation   |
|--------|---------------------------|
| `café` | `c a f U+00E9`            |
| `café` | `c a f U+0065 U+0301`     |

Because the code point sequences differ, direct comparison with `==` fails.

---

## Normalization Forms

**Unicode normalization** converts text into a standard form so equivalent strings
compare reliably. Python provides this through `unicodedata.normalize()`.

Unicode defines four normalization forms:

| Form   | Meaning                                          |
|--------|--------------------------------------------------|
| `NFC`  | Canonical decomposition, then recomposition      |
| `NFD`  | Canonical decomposition only                     |
| `NFKC` | Compatibility decomposition, then recomposition  |
| `NFKD` | Compatibility decomposition only                 |

For most string comparison tasks, **NFC** is the most useful form.

### NFC

NFC produces **precomposed characters** — it collapses decomposed sequences into
a single code point where possible:
```python
print(normalize("NFC", "cafe\u0301"))  # café  (length 4)
```

### NFD

NFD produces **decomposed characters** — it expands precomposed characters into
base character + combining marks:
```python
print(normalize("NFD", "caf\u00e9"))  # café  (length 5, e + U+0301)
```

Both render as `café`, but their internal lengths differ.

---

## Unicode-Aware Comparison

With normalization, visually identical strings compare equal:
```python
s1 = "caf\u00e9"
s2 = "cafe\u0301"

print(normalize("NFC", s1) == normalize("NFC", s2))  # True
```

For convenience, wrap this in a helper:
```python
def nfc_equal(s1, s2):
    return normalize("NFC", s1) == normalize("NFC", s2)

print(nfc_equal("café", "cafe\u0301"))  # True
```

Note that `nfc_equal()` is still case-sensitive — `"Café"` and `"CAFÉ"` are not equal.
For case-insensitive comparison, see [Unicode Case Folding](unicode_case_folding.md).

---

## Key Takeaways

- Unicode strings that look identical may have different internal representations.
- `normalize("NFC", s)` converts to a consistent precomposed form.
- Always normalize before comparing Unicode strings from external sources.

---

## Exercises


**Exercise 1.**
Create two strings that look identical when printed (`"cafe\u0301"` and `"caf\u00e9"`) and show that `==` returns `False`. Then use `unicodedata.normalize("NFC", ...)` to make them compare equal.

??? success "Solution to Exercise 1"

    ```python
    from unicodedata import normalize

    s1 = "caf\u00e9"    # precomposed
    s2 = "cafe\u0301"   # decomposed

    print(s1 == s2)       # False
    print(normalize("NFC", s1) == normalize("NFC", s2))  # True
    ```

    The two strings have different internal code point sequences despite looking identical. NFC normalization converts both to the same precomposed form.

---

**Exercise 2.**
Write a function `normalize_and_compare(s1, s2)` that returns `True` if two strings are equivalent after NFC normalization. Test it with both precomposed and decomposed forms of accented characters.

??? success "Solution to Exercise 2"

    ```python
    from unicodedata import normalize

    def normalize_and_compare(s1, s2):
        return normalize("NFC", s1) == normalize("NFC", s2)

    print(normalize_and_compare("caf\u00e9", "cafe\u0301"))  # True
    print(normalize_and_compare("nai\u0308ve", "na\u00efve"))  # True
    print(normalize_and_compare("hello", "world"))              # False
    ```

    Normalizing both strings to NFC before comparison ensures equivalent representations match.

---

**Exercise 3.**
Demonstrate the difference between NFC and NFD normalization by showing the `len()` of the same accented string after applying each form.

??? success "Solution to Exercise 3"

    ```python
    from unicodedata import normalize

    s = "caf\u00e9"
    nfc = normalize("NFC", s)
    nfd = normalize("NFD", s)

    print(f"NFC: '{nfc}', length: {len(nfc)}")  # 4
    print(f"NFD: '{nfd}', length: {len(nfd)}")  # 5
    ```

    NFC produces precomposed characters (fewer code points), while NFD decomposes characters into base character plus combining marks (more code points). Both render identically.
