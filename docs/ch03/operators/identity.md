# Identity Operators

Identity operators compare **memory addresses** of objects, not their values.

!!! tip "Mental Model"
    `is` asks "are these the exact same object in memory?" while `==` asks "do these objects have the same value?" Two lists with identical contents are `==` but not `is`. The only common use for `is` is comparing against singletons: `x is None`, `x is True`, `x is False`. For everything else, use `==`.

| Operator | Description | Example |
|----------|-------------|---------|
| `is` | Same object in memory | `x is y` |
| `is not` | Different objects | `x is not y` |


## `==` vs `is`

- `==` compares **values** (equality)
- `is` compares **identity** (same object in memory)

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)   # True (same value)
print(a is b)   # False (different objects)
print(a is c)   # True (same object)

print(id(a))    # e.g., 140234567890
print(id(b))    # e.g., 140234567920 (different)
print(id(c))    # e.g., 140234567890 (same as a)
```


## Mutable vs Immutable Objects

### Mutable Objects (list, dict, set)

Each creation produces a **new object**:

```python
a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)   # True
print(a is b)   # False (different objects)

a = {1: 'one'}
b = {1: 'one'}
print(a == b)   # True
print(a is b)   # False

a = {1, 2, 3}
b = {1, 2, 3}
print(a == b)   # True
print(a is b)   # False
```

### Immutable Objects

Python may reuse immutable objects (interning):

```python
# Small integers are cached
a = 5
b = 5
print(a is b)   # True (same object)

# Strings may be interned
a = "hello"
b = "hello"
print(a is b)   # True (typically)

# Booleans are singletons
a = True
b = True
print(a is b)   # True

# None is a singleton
a = None
b = None
print(a is b)   # True
```

**Warning**: Don't rely on `is` for immutable objects except `None`, `True`, `False`.


## When to Use `is`

### Use `is` for Singletons

```python
# Checking for None
if x is None:
    print("x is None")

# Checking for True/False (rare)
if flag is True:
    print("flag is exactly True")
```

### Use `==` for Values

```python
# Comparing values
if x == 5:
    print("x equals 5")

if name == "Alice":
    print("name is Alice")

if my_list == [1, 2, 3]:
    print("lists have same elements")
```


## Mutation and Shared References

### Separate Objects

Modifying one does not affect the other:

```python
a = [1, 2, 3]
b = [1, 2, 3]
a[0] = "one"

print(a)  # ['one', 2, 3]
print(b)  # [1, 2, 3]
```

### Shared Reference

Both names point to the same object:

```python
a = [1, 2, 3]
b = a
a[0] = "one"

print(a)  # ['one', 2, 3]
print(b)  # ['one', 2, 3]  (same object!)
```


## Common Pitfall: Integer Caching

Python caches small integers (-5 to 256):

```python
a = 256
b = 256
print(a is b)   # True (cached)

a = 257
b = 257
print(a is b)   # False (not cached, usually)
```

**Never use `is` to compare integers** — use `==`.


## `is not` Operator

```python
a = [1, 2]
b = [1, 2]

print(a is not b)     # True (different objects)
print(a != b)         # False (same value)
```


## Practical Example

```python
def process(data=None):
    if data is None:  # Correct: check for None singleton
        data = []
    # NOT: if data == None (works but not idiomatic)
    return data
```


## Custom Equality with `__eq__`

Classes can override `==` behavior:

```python
class Point:
    def __init__(self, x):
        self.x = x
    
    def __eq__(self, other):
        return self.x == other.x

p1 = Point(3)
p2 = Point(3)

print(p1 == p2)  # True (custom equality)
print(p1 is p2)  # False (different objects)
```

- `==` returns `True` due to custom `__eq__`
- `is` still returns `False` — different instances


## Hashability Contract

If you override `__eq__`, you must also override `__hash__`:

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))
```

**The contract**: If `a == b`, then `hash(a) == hash(b)`.

Without `__hash__`, objects become unhashable:

```python
class NoHash:
    def __eq__(self, other):
        return True

hash(NoHash())  # TypeError: unhashable type: 'NoHash'
```


## Summary

| Operator | Compares | Use For |
|----------|----------|---------|
| `==` | Value equality | Most comparisons |
| `is` | Object identity | `None`, `True`, `False` |

- Use `is` only for singleton comparisons
- Use `==` for value comparisons
- Mutable objects: `is` almost always `False` for separate creations
- Don't rely on integer/string interning behavior


---

## Exercises


**Exercise 1.**
Create two empty lists using separate expressions. Verify that they are equal (`==`) but not identical (`is`). Then assign one to the other and verify they become identical.

??? success "Solution to Exercise 1"

    ```python
    a = []
    b = []
    print(a == b)   # True  (same contents)
    print(a is b)   # False (different objects)

    c = a
    print(a is c)   # True  (same object)
    ```

    Each `[]` literal creates a new list object. After `c = a`, both names refer to the same object.

---

**Exercise 2.**
Demonstrate Python's integer caching by showing that `a is b` is `True` for `a = b = 256` but may be `False` for `a = b = 257`. Explain why you should never rely on this behavior.

??? success "Solution to Exercise 2"

    ```python
    a = 256
    b = 256
    print(a is b)   # True (cached)

    a = 257
    b = 257
    print(a is b)   # May be False (not cached)
    ```

    CPython caches integers from -5 to 256. Beyond that range, each creation may produce a new object. Never use `is` to compare integer values -- always use `==`.

---

**Exercise 3.**
Write a function `process(data=None)` that creates a new empty list when no argument is passed. Explain why the check uses `is None` rather than `== None`.

??? success "Solution to Exercise 3"

    ```python
    def process(data=None):
        if data is None:
            data = []
        data.append("processed")
        return data

    print(process())           # ['processed']
    print(process([1, 2, 3]))  # [1, 2, 3, 'processed']
    ```

    `is None` checks identity against the `None` singleton. Using `== None` would work but is not idiomatic, and a custom class could override `__eq__` to return `True` when compared to `None`, leading to unexpected behavior.
