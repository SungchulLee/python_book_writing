# String Interning

!!! tip "Mental Model"
    CPython automatically shares a single copy of short, identifier-like strings so that dictionary lookups and attribute access can use pointer comparison instead of character-by-character comparison. Think of it as a global string cache -- but since the caching rules are implementation-specific, always use `==` for string comparison.

## What Is Interning

### 1. Concept

Share memory for identical strings:

```python
s1 = "hello"
s2 = "hello"
print(s1 is s2)         # Often True
print(id(s1) == id(s2)) # Often True
```

### 2. Why Intern

```python
# Without interning:
names = ["hello"] * 1000
# 1000 separate objects

# With interning:
# All share one object
```

## CPython Rules

### 1. Identifier-Like

Automatically interned:

```python
# Identifier-like
s1 = "hello"
s2 = "hello"
print(s1 is s2)         # True

s1 = "hello_world"
s2 = "hello_world"
print(s1 is s2)         # True
```

### 2. Not Interned

```python
# Contains spaces/special chars
s1 = "hello world"
s2 = "hello world"
print(s1 is s2)         # May be False

s1 = "hello!"
s2 = "hello!"
print(s1 is s2)         # May be False
```

## Force Interning

### 1. sys.intern()

```python
import sys

# Force interning
s1 = sys.intern("hello world")
s2 = sys.intern("hello world")
print(s1 is s2)         # True
```

### 2. Use Case

```python
# Many duplicate strings
data = ["user_id"] * 10000

# Intern keys
data_interned = [
    sys.intern("user_id")
    for _ in range(10000)
]

# All same object
print(data_interned[0] is data_interned[9999])
```

## Best Practices

### 1. Never Rely On

```python
# Bad: assumes interning
def bad(s):
    if s is "hello":    # Don't!
        return True

# Good: use ==
def good(s):
    if s == "hello":    # Correct
        return True
```

### 2. Explicit Intern

```python
# When many duplicates
import sys

class Config:
    def __init__(self):
        self.USER_ID = sys.intern("user_id")
        
    def check(self, key):
        if key is self.USER_ID:  # Fast
            return "id"
```

## Summary

### 1. CPython

- Auto-interns identifier-like
- Can force with sys.intern()
- Performance optimization
- Not guaranteed by spec

### 2. Portable Code

```python
# Always use ==
if name == "admin":
    pass

# Never use is for strings
# except explicit interning
admin_key = sys.intern("admin")
if name is admin_key:   # OK
    pass
```

---

## Exercises

**Exercise 1.**
CPython auto-interns identifier-like strings. Predict the output:

```python
a = "hello"
b = "hello"
print(a is b)

c = "hello world"
d = "hello world"
print(c is d)

e = "hello_world"
f = "hello_world"
print(e is f)
```

What makes a string "identifier-like"? Why does CPython intern `"hello"` and `"hello_world"` but not `"hello world"`?

??? success "Solution to Exercise 1"
    Output (CPython):

    ```text
    True
    True
    True
    ```

    Note: the second result may vary. In recent CPython versions, compile-time string constants are often shared via the constant pool even if they contain spaces. However, dynamically constructed strings with spaces would not be interned.

    A string is "identifier-like" if it matches the pattern for Python identifiers: only letters, digits, and underscores. CPython automatically interns these because they frequently appear as attribute names, variable names, and dictionary keys in Python's own internals. `"hello"` and `"hello_world"` match this pattern; `"hello world"` (with a space) does not.

    The interning rule is a CPython implementation detail, not a language guarantee. Different Python versions may change the criteria.

---

**Exercise 2.**
`sys.intern()` forces interning for any string. Predict the output:

```python
import sys

a = "hello world"
b = "hello world"
print(a is b)

a = sys.intern("hello world")
b = sys.intern("hello world")
print(a is b)

c = "hello world"
print(a is c)
```

Why is `a is c` still `False` even after `a` was interned? What must be true of **both** strings for `is` to return `True`?

??? success "Solution to Exercise 2"
    Output (CPython):

    ```text
    False (or True, depending on compile-time optimization)
    True
    False
    ```

    `sys.intern()` returns the canonical interned copy of a string. If you pass the same string content twice, both calls return the **same object**. But this only works if **both** lookups go through `sys.intern()`.

    `a is c` is `False` because `c = "hello world"` creates a regular (non-interned) string object. The interning table remembers `a`, but `c` was never looked up in it. For `is` to return `True`, **both** strings must be the interned version. This is why `sys.intern` is an opt-in optimization, not a transparent one.

---

**Exercise 3.**
String interning affects performance for dictionary lookups. Predict which lookup is faster and why:

```python
import sys

# Scenario: looking up keys in a dict 1 million times
key = sys.intern("user_id")
d = {key: 42}

# Fast: identity check first
result = d[sys.intern("user_id")]

# Slower: must compare characters
other_key = "".join(["user", "_", "id"])
result2 = d[other_key]
```

Why is the interned lookup faster? What does Python's dictionary implementation check **before** comparing string characters?

??? success "Solution to Exercise 3"
    The interned lookup is faster because Python's dictionary implementation uses a two-step comparison:

    1. **Identity check** (`is`): Compare memory addresses. This is a single pointer comparison -- O(1).
    2. **Equality check** (`==`): Compare characters one by one. This is O(n) where n is string length.

    When both the key in the dict and the lookup key are the same interned object, step 1 succeeds immediately, and step 2 is never reached. With non-interned strings (like `other_key` constructed by `"".join(...)`), step 1 fails (different objects), and Python falls through to the O(n) character comparison.

    For dictionaries with many lookups against the same keys (like JSON parsing, attribute access, or configuration management), interning the keys can provide a measurable speedup.
