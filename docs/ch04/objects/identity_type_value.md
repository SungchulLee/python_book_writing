# Identity Type Value

!!! tip "Mental Model"
    Every Python object carries exactly three things: an identity (its unique address, checked with `is`), a type (its blueprint, checked with `type()`), and a value (its data, checked with `==`). Identity and type are fixed at creation; only the value can change, and only if the type is mutable.

## Three Characteristics

### 1. Every Object

```python
x = [1, 2, 3]

print(id(x))        # Identity
print(type(x))      # Type
print(x)            # Value
```

## Identity

### 1. Unique ID

```python
a = [1, 2, 3]
b = [1, 2, 3]

print(id(a) != id(b))  # True
```

**CPython note**: `id()` returns the memory address:

```python
x = [1, 2, 3]
print(id(x))       # e.g., 140234567890
print(hex(id(x)))  # e.g., '0x7f8b2c3d4e50'
```

Other implementations (PyPy, Jython) may return a different unique token.

### 2. Constant

```python
x = [1, 2, 3]
original_id = id(x)

x.append(4)
print(id(x) == original_id)  # True
```

### 3. Identity Check

```python
a = [1, 2, 3]
b = a
c = [1, 2, 3]

print(a is b)       # True
print(a is c)       # False
```

## Type

### 1. Determines Behavior

```python
x = 42
y = "42"

print(type(x))      # <class 'int'>
print(type(y))      # <class 'str'>
```

### 2. Type Immutable

```python
x = [1, 2, 3]
# Cannot change type
```

## Value

### 1. Object Data

```python
x = [1, 2, 3]
print(x)            # [1, 2, 3]
```

### 2. Mutable Values

```python
x = [1, 2, 3]
x[0] = 100
print(x)            # [100, 2, 3]
```


## Summary

| Property | Check | Example |
|----------|-------|---------|
| Identity | `is` | `id(x)` |
| Type | `isinstance()` | `type(x)` |
| Value | `==` | `x[:]` |


## Exercises

**Exercise 1.**
Every Python object has three characteristics: identity, type, and value. For the object created by `x = [1, 2, 3]`, explain what each characteristic is, how to inspect it, and which can change during the object's lifetime.

??? success "Solution to Exercise 1"
    For `x = [1, 2, 3]`:

    - **Identity**: The unique identifier of this specific list object. Checked with `id(x)` or compared with `is`. In CPython, this is the memory address. Identity is **fixed** for the lifetime of the object -- it never changes.
    - **Type**: `list`. Checked with `type(x)` or `isinstance(x, list)`. The type of an object is also **fixed** -- a list cannot become a string.
    - **Value**: `[1, 2, 3]`. Checked with `==` or by inspecting contents. For mutable objects like lists, the value **can change** (e.g., `x.append(4)` changes the value to `[1, 2, 3, 4]`). For immutable objects like integers, the value is fixed.

    Summary: identity and type never change; value can change only for mutable objects.

---

**Exercise 2.**
Predict the output and explain which of the three properties (identity, type, value) changed at each step:

```python
x = [1, 2, 3]
print(id(x), type(x), x)

x.append(4)
print(id(x), type(x), x)

x = "hello"
print(id(x), type(x), x)
```

??? success "Solution to Exercise 2"
    ```text
    140234... <class 'list'> [1, 2, 3]   # Original object
    140234... <class 'list'> [1, 2, 3, 4] # Same id, same type, different VALUE
    140567... <class 'str'>  hello        # Different id, different TYPE, different VALUE
    ```

    - After `x.append(4)`: **Only value changed.** Identity (same `id`) and type (`list`) are unchanged. `append` mutates the existing object.
    - After `x = "hello"`: The name `x` is rebound to a completely **different object**. All three properties are different because we are looking at a new object. The original list still exists (if something else references it) with its identity, type, and value unchanged.

    The key distinction: `x.append(4)` modifies the object (value changes, identity preserved). `x = "hello"` rebinds the name to a new object (all properties appear to change because it is a different object).

---

**Exercise 3.**
Why is `isinstance(x, int)` generally preferred over `type(x) == int` for type checking? Give an example where they produce different results. How does this relate to Python's object model and inheritance?

??? success "Solution to Exercise 3"
    `type(x) == int` checks for the **exact type**. `isinstance(x, int)` checks whether `x` is an instance of `int` **or any subclass** of `int`.

    Example where they differ:

    ```python
    x = True
    print(type(x) == int)       # False (type is bool, not int)
    print(isinstance(x, int))   # True (bool is a subclass of int)
    ```

    `True` has type `bool`, which is a subclass of `int`. `type(x) == int` returns `False` because `bool` is not `int`. `isinstance(x, int)` returns `True` because `bool` inherits from `int`.

    `isinstance` is preferred because it respects Python's inheritance hierarchy. Code that uses `type(x) == int` would reject `True` and `False`, even though they are valid integers. Using `isinstance` follows the principle of "duck typing" -- if an object behaves like an `int` (because it inherits from `int`), it should be accepted as one.
