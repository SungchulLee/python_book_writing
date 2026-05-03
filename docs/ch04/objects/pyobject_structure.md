# PyObject Structure

!!! tip "Mental Model"
    In CPython, every object starts with the same two-field header: a reference count and a type pointer. The reference count tracks how many names point to the object (reaching zero means deletion), and the type pointer tells Python what operations the object supports. Everything else is type-specific payload.

## CPython Internal

### 1. Base Structure

Every object has:
- Reference count
- Type pointer
- Value data

### 2. Reference Count

```python
import sys

x = [1, 2, 3]
print(sys.getrefcount(x))

y = x
print(sys.getrefcount(x))  # Increased
```

## Type Object

### 1. Type Info

```python
x = [1, 2, 3]

# Type determines behavior
print(type(x).__name__)
```

## Object Data

### 1. Type-Specific

```python
x = 42              # Integer data
s = "hello"         # String data
lst = [1, 2, 3]     # List items
```

## Memory Layout

### 1. Heap Allocation

```python
# All objects on heap
x = 42
y = [1, 2, 3]
z = "hello"
```

## Three Properties

### 1. In Python

```python
x = [1, 2, 3]

print(id(x))        # Identity
print(type(x))      # Type
print(x)            # Value
```

## Summary

### 1. Every Object

- Reference count
- Type pointer
- Value data

### 2. Enables

- Auto memory management
- Dynamic typing
- Efficient sharing

---

## Exercises

**Exercise 1.**
Every object has a reference count that determines when it is freed. Predict the output:

```python
import sys

a = "hello"
print(sys.getrefcount(a))

b = a
print(sys.getrefcount(a))

del b
print(sys.getrefcount(a))

c = [a, a, a]
print(sys.getrefcount(a))
```

Why is the initial reference count higher than 1? What happens to the reference count when `a` is placed inside a list multiple times?

??? success "Solution to Exercise 1"
    The exact numbers depend on CPython internals and string interning, but the pattern is:

    ```text
    N       (some base count > 1 due to interning/getrefcount)
    N+1     (b adds a reference)
    N       (del b removes it)
    N+3     (three list slots each hold a reference)
    ```

    The initial count is higher than 1 because `sys.getrefcount` itself creates a temporary reference (the function argument), and short strings may be interned (shared by multiple internal references).

    Each slot in the list `[a, a, a]` holds an independent reference to the same object, adding 3 to the count. Reference counting is the fundamental mechanism: when the count reaches 0, CPython immediately frees the object's memory.

---

**Exercise 2.**
The type pointer determines what operations an object supports. Predict the output:

```python
x = 42
print(type(x) is int)
print(type(type(x)))
print(type(type(type(x))))
```

What does the chain `type(type(type(x)))` reveal about Python's type system? What is `type` itself?

??? success "Solution to Exercise 2"
    Output:

    ```text
    True
    <class 'type'>
    <class 'type'>
    ```

    `type(42)` is `int`. `type(int)` is `type`. `type(type)` is `type`. The chain terminates because `type` is its own type -- it is an instance of itself.

    In Python's object model, `type` is the **metaclass**: the class of all classes. Every class (including `int`, `str`, `list`) is an instance of `type`. And `type` itself is an instance of `type`. This self-referential relationship is bootstrapped at interpreter startup and is the foundation of Python's type system.

---

**Exercise 3.**
Identity, type, and value are an object's three defining properties. Predict the output:

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(id(a) == id(b))
print(id(a) == id(c))
print(type(a) == type(b))
print(a == b)
print(a is b)
print(a is c)
```

Why are `a` and `b` equal (`==`) but not identical (`is`)? Why are `a` and `c` both equal and identical?

??? success "Solution to Exercise 3"
    Output:

    ```text
    False
    True
    True
    True
    False
    True
    ```

    `a` and `b` are **equal** (`==`) because they contain the same values. But they are **not identical** (`is`) because they are two separate objects at different memory locations -- `id(a) != id(b)`.

    `a` and `c` are both equal and identical because `c = a` does not create a new list. It creates a new **name** that refers to the **same object**. `id(a) == id(c)` because `a` and `c` point to the same memory location.

    This is the key distinction: `==` compares **values** (by calling `__eq__`), while `is` compares **identity** (memory address in CPython).
