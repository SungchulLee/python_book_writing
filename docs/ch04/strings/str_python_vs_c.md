# `str`: Python vs C

Python strings differ fundamentally from C strings in storage, safety, and semantics.

!!! tip "Mental Model"
    A C string is a raw byte array terminated by a null character -- fast but dangerous. A Python string is an immutable, length-aware, Unicode-native object that trades raw speed for safety and expressiveness. The key difference: C trusts you to manage memory; Python manages it for you.

---

## C Strings

### 1. Null Termination

C strings are character arrays terminated by `\0`:

```c
char str[] = "Hello";  // Actually 6 bytes: H e l l o \0
```

This leads to:

- Buffer overflow vulnerabilities
- Manual length tracking required
- Undefined behavior on missing null

### 2. No Length Storage

C has no built-in string length:

```c
// Must scan for null terminator
size_t len = strlen(str);
```

---

## Python Strings

### 1. Explicit Length

Python stores length explicitly, no null terminator:

```python
s = "Hello, world!"
length = len(s)
print("Length of the string:", length)  # 13
```

### 2. Object-Based

Python strings are immutable objects:

```python
s = "finance"
print(len(s))   # 7
print(type(s))  # <class 'str'>
```

---

## Immutability

### 1. Cannot Modify

Strings cannot be changed in place:

```python
s = "abc"
# s[0] = "A"  # TypeError: 'str' does not support item assignment
s = "A" + s[1:]  # Create new string instead
```

### 2. Benefits

Immutability enables:

- Thread safety
- Use as dictionary keys
- Efficient string interning
- Predictable behavior

---

## Unicode Support

### 1. Native Unicode

Python handles Unicode naturally:

```python
s = "π ≈ 3.14"
print(s)  # π ≈ 3.14
```

### 2. International Text

```python
# Multiple scripts in one string
text = "Hello 世界 مرحبا"
print(len(text))  # Character count, not bytes
```

---

## Comparison Table

| Feature | C | Python |
|---------|---|--------|
| Termination | Null byte | Length stored |
| Mutability | Mutable | Immutable |
| Unicode | Manual | Native |
| Safety | Buffer risks | Safe |
| Length | `strlen()` | `len()` |

---


## Key Takeaways

- Python strings store length explicitly.
- No null terminator needed in Python.
- Immutability provides safety and hashability.
- Unicode support is built-in.


## Exercises

**Exercise 1.**
Python strings are immutable objects, while C strings are mutable character arrays. Predict the output:

```python
s = "hello"
t = s.replace("h", "H")

print(s)
print(t)
print(s is t)
print(id(s) == id(t))
```

Why is `s` unchanged after calling `.replace()`? What does immutability mean in terms of the object in memory?

??? success "Solution to Exercise 1"
    Output:

    ```text
    hello
    Hello
    False
    False
    ```

    `s` is unchanged because Python strings are **immutable** -- no operation can modify a string object in place. `.replace()` creates a **new** string object with the substitution applied. The original object at `id(s)` still contains `"hello"`.

    Immutability means the bytes that make up the string's value in memory cannot be altered after creation. Every string "modification" method (`replace`, `upper`, `strip`, etc.) returns a new string object. This is why `s is t` is `False` -- they are different objects.

---

**Exercise 2.**
Python strings store their length, while C strings use null termination. Predict the output:

```python
s = "hello\x00world"
print(len(s))
print(s)
print(repr(s))
```

Why does Python report a length of 11? In C, what would `strlen("hello\x00world")` return, and why?

??? success "Solution to Exercise 2"
    Output:

    ```text
    11
    hello world
    'hello\x00world'
    ```

    (The `print` output may vary by terminal -- some terminals display `\x00` as a space or invisible character.)

    Python reports length 11 because Python strings store their length explicitly and can contain any Unicode character, including null bytes (`\x00`). The null byte is just another character with no special meaning.

    In C, `strlen("hello\x00world")` returns `5` because C strings use null termination: `strlen` scans forward until it finds `\0` and stops. The `"world"` part is invisible to `strlen`. This is a fundamental difference: Python strings are **length-prefixed** (safe), while C strings are **null-terminated** (vulnerable to buffer overflows and truncation).

---

**Exercise 3.**
Immutability enables strings to be dictionary keys and set members. Predict the output:

```python
d = {}
d["hello"] = 1
d["hello"] = 2
print(d)
print(len(d))

try:
    d[[1, 2, 3]] = "list key"
except TypeError as e:
    print(e)
```

Why can strings be dictionary keys but lists cannot? What property must an object have to be usable as a dictionary key, and how does immutability guarantee this?

??? success "Solution to Exercise 3"
    Output:

    ```text
    {'hello': 2}
    1
    unhashable type: 'list'
    ```

    Dictionary keys must be **hashable**: they must implement `__hash__()` and the hash must remain constant for the object's lifetime. Immutable types (strings, ints, tuples of immutables) are hashable because their value never changes, so their hash never changes.

    Lists are **mutable**, so Python makes them unhashable by design. If lists were hashable, you could add a list as a key, then mutate the list, changing its hash -- the dictionary would be corrupted because the key would be in the wrong hash bucket.

    Immutability guarantees **hash stability**: since the value cannot change, the hash computed at insertion time remains valid forever. This is why immutability and hashability are deeply connected in Python's design.
