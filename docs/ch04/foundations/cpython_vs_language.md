# CPython vs Language

!!! tip "Mental Model"
    The Python language specification is a contract that every implementation must honor; CPython is just one implementation that fulfills that contract. If a behavior is not in the spec -- like small-integer caching -- it is an implementation detail you must never rely on in portable code.

## Language Guarantees

### 1. Semantic Behavior

Python's **language specification** defines guaranteed behavior that all implementations must follow:

- Variable assignment creates name-to-object bindings
- Object identity (`id()`) remains constant during object lifetime
- Immutable objects cannot be modified after creation
- Mutable objects can be modified in-place

```python
# Guaranteed: identity stability
x = [1, 2, 3]
original_id = id(x)
x.append(4)
assert id(x) == original_id  # Always True
```

### 2. Implementation Freedom

Language spec allows freedom in:

- Memory layout and allocation strategies
- Garbage collection algorithms
- Optimization techniques
- Internal data structures

## CPython Specifics

### 1. Reference Counting

⚙️ **CPython-specific**: Uses reference counting as primary memory management

```python
import sys

x = [1, 2, 3]
print(sys.getrefcount(x))  # CPython: shows refcount
# PyPy, Jython: may use different GC
```

### 2. Integer Caching

⚙️ **CPython-specific**: Caches integers in range `[-5, 256]`

```python
a = 42
b = 42
print(a is b)  # True in CPython (cached)

a = 257
b = 257
print(a is b)  # May be False (not guaranteed)
```

### 3. GIL Implementation

⚙️ **CPython-specific**: Single-threaded bytecode execution

```python
import threading

# CPython: threads don't run Python code in parallel
# PyPy/Jython: may have different threading models
```

## Key Distinctions

### 1. What's Guaranteed

| Aspect | Language Guarantee | Example |
|--------|-------------------|---------|
| Equality | `==` compares values | `[1,2] == [1,2]` → True |
| Identity | `is` checks object identity | Behavior defined |
| Mutability | Types have fixed mutability | `list` always mutable |
| Assignment | Creates name binding | Defined semantics |

### 2. What's Not

| Aspect | CPython Behavior | Other Implementations |
|--------|-----------------|---------------------|
| `id()` value | Memory address | May be different |
| Small int caching | `[-5, 256]` | May cache differently |
| String interning | Automatic for some | May vary |
| `is` for literals | Often True | Implementation-dependent |

## Practical Implications

### 1. Write Portable Code

```python
# Good: relies on language guarantees
if x == y:  # Value comparison
    pass

# Bad: relies on CPython specifics
if id(x) < id(y):  # Memory address comparison
    pass
```

### 2. Use `is` Correctly

```python
# Good: singleton comparison
if x is None:
    pass

# Bad: relying on implementation detail
if x is 42:  # Works in CPython, not guaranteed
    pass
```

### 3. Debug Carefully

```python
import sys

# CPython-specific debugging
def debug_refcount(obj):
    # Only works in CPython
    return sys.getrefcount(obj)
```

## Documentation Tags

When documenting behavior:

- **Language-level**: Guaranteed across all implementations
- **⚙️ CPython**: Specific to CPython implementation
- **Implementation-dependent**: May vary

```python
# Language-level: guaranteed
x = [1, 2]
x.append(3)  # Always works

# ⚙️ CPython: implementation detail
import sys
sys.getrefcount(x)  # CPython-specific

# Implementation-dependent
a = 1000
b = 1000
# a is b may be True or False
```

## Exercises

**Exercise 1.**
Classify each of the following as "language-level guarantee" or "CPython implementation detail":

1. Lists are ordered and mutable
2. `sys.getrefcount(x)` returns the reference count of `x`
3. Small integers (-5 to 256) are cached and reused
4. `dict` maintains insertion order (Python 3.7+)
5. Objects are destroyed immediately when their reference count reaches zero

Explain why the distinction matters for writing portable Python code.

??? success "Solution to Exercise 1"

    1. **Language-level guarantee** -- the Python language specification defines lists as ordered, mutable sequences.
    2. **CPython implementation detail** -- `sys.getrefcount` only exists because CPython uses reference counting. PyPy does not use reference counting, and while it provides `sys.getrefcount` for compatibility, the values may differ.
    3. **CPython implementation detail** -- the language says nothing about caching integers. This is a CPython memory optimization.
    4. **Language-level guarantee** (as of Python 3.7) -- dict insertion order is guaranteed by the language spec. (In 3.6, it was a CPython implementation detail.)
    5. **CPython implementation detail** -- the language does not specify when objects are destroyed, only that they will eventually be garbage-collected. CPython's reference counting gives immediate destruction, but other implementations may delay it.

    The distinction matters because code relying on implementation details may break when run on PyPy, GraalPython, or future CPython versions. Portable code relies only on language-level guarantees.

---

**Exercise 2.**
CPython uses reference counting for memory management, while PyPy uses a tracing garbage collector. Explain how this implementation difference could affect the following code:

```python
f = open("data.txt", "w")
f.write("hello")
# f goes out of scope here -- when is the file closed?
```

Why does this code "work" on CPython but may fail on PyPy? What is the correct way to write this code?

??? success "Solution to Exercise 2"
    On CPython: when `f` goes out of scope, its reference count drops to zero. CPython immediately destroys the file object, which triggers `f.close()` as part of the destructor (`__del__`). The file is reliably closed.

    On PyPy: the tracing garbage collector does not destroy objects immediately when they become unreachable. The file object may remain open for an indeterminate time. This means the `"hello"` data may not be flushed to disk, or the file handle may remain locked, potentially causing resource exhaustion.

    **Correct code:**

    ```python
    with open("data.txt", "w") as f:
        f.write("hello")
    # File is guaranteed closed here, regardless of implementation
    ```

    The `with` statement calls `f.close()` deterministically when the block exits, regardless of how the garbage collector works. This is the only portable way to manage resources.

---

**Exercise 3.**
A programmer says: "I tested my code on CPython and it works, so it is correct Python." Explain why this reasoning is flawed. Give two examples of code that passes all tests on CPython but would behave differently on another implementation.

??? success "Solution to Exercise 3"
    The reasoning is flawed because CPython has specific behaviors that are not part of the language specification. Code that relies on these behaviors "works" on CPython by coincidence, not by correctness.

    **Example 1 -- integer identity:**

    ```python
    x = 100
    y = 100
    assert x is y  # Passes on CPython (interned), may fail on PyPy
    ```

    **Example 2 -- deterministic destruction:**

    ```python
    class Logger:
        def __del__(self):
            print("destroyed")

    def f():
        obj = Logger()  # Created
    f()  # On CPython, prints "destroyed" immediately
         # On PyPy, may not print until later (or at all)
    ```

    To write correct Python, rely on language-level guarantees: use `==` for value comparison, `with` for resource management, and explicit cleanup rather than `__del__`.
