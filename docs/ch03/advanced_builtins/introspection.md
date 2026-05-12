# `id()`, `type()`, `isinstance()`

These built-ins support **introspection**, allowing programs to examine objects at runtime.

!!! tip "Mental Model"
    Every Python object carries an invisible ID card. `id()` reads its unique serial number, `type()` reads its class label, and `isinstance()` checks whether it belongs to a particular family. Together they let your code ask "what am I looking at?" at runtime without knowing in advance.

---

## `id()`

Returns a unique identifier for an object during its lifetime:

```python
x = []
id(x)
```

Conceptually corresponds to a memory address.

### What does id() actually represent?

In CPython, `id(obj)` returns the object's identity, which corresponds to its **virtual memory address**.

From Python's perspective:

- The object is allocated once.
- Its identity (`id`) remains constant for its lifetime.
- The object itself is not relocated.

However, this should not be confused with physical memory.

From the operating system's perspective:

- Memory is managed using **virtual memory**.
- The OS may remap a virtual address to different physical memory locations over time (e.g., paging, swapping).
- This remapping is completely transparent to Python.

Additionally, some objects (like lists) manage internal storage separately:

- When a list grows beyond its capacity, Python allocates a new internal buffer and copies elements.
- The list object itself remains at the same virtual address.
- Only its internal storage changes.

Key ideas:

- `id()` reflects the object's identity (virtual address).
- The object itself does not move.
- Internal storage may be reallocated independently.
- Physical memory mapping may change, but this is handled by the OS and irrelevant to Python semantics.

---

## `type()`

Returns the type of an object:

```python
type(3)        # <class 'int'>
type([1, 2])   # <class 'list'>
```

---

## `isinstance()`

Checks whether an object is an instance of a type:

```python
isinstance(3, int)
isinstance(True, int)   # True
```

Supports tuples of types:

```python
isinstance(x, (int, float))
```

---

## `dir()`

Returns a list of names (attributes and methods) of an object:

```python
name = "hello"
print(dir(name))  # List of string methods
```

Without arguments, returns names in current scope:

```python
x = 10
print(dir())  # Includes 'x'
```

Useful for exploration and debugging.

---

## `help()`

Displays documentation for an object:

```python
help(str.lower)
help(len)
```

Shows the docstring and signature. In interactive sessions, provides paginated output.

---

## `del`

Deletes references to objects:

```python
# Delete a variable
x = 10
del x
# x is no longer defined

# Delete from a list
my_list = [1, 2, 3]
del my_list[1]  # [1, 3]

# Delete from a dict
my_dict = {'a': 1, 'b': 2}
del my_dict['a']  # {'b': 2}

# Delete an attribute
del obj.attribute
```

Memory is freed by the garbage collector when no references remain.

---

## Best practices

- Use `isinstance()` instead of `type(x) == T`.
- Avoid excessive type checking; prefer polymorphism.

---

## Key takeaways

- `id()` returns object identity (virtual address)
- `type()` returns object type
- `isinstance()` is the correct type-checking tool
- `dir()` lists available attributes and methods
- `help()` displays documentation
- `del` removes references (not the object itself)

---

## Exercises

**Exercise 1.**
Predict the output and explain each result:

```python
a = [1, 2, 3]
b = a
c = [1, 2, 3]

print(id(a) == id(b))
print(id(a) == id(c))
print(isinstance(a, list))
print(type(a) == type(c))
```

??? success "Solution to Exercise 1"
    Output:

    ```text
    True
    False
    True
    True
    ```

    `b = a` makes `b` refer to the same object as `a`, so `id(a) == id(b)` is `True`. `c` is a separate list with the same contents, so it has a different identity: `id(a) == id(c)` is `False`. Both `isinstance` and `type` confirm they are lists, but identity and equality are different concepts.

---

**Exercise 2.**
`isinstance()` respects inheritance, while `type()` does not. Predict the output:

```python
print(type(True) == bool)
print(type(True) == int)
print(isinstance(True, bool))
print(isinstance(True, int))
```

Why does `type(True) == int` return `False` while `isinstance(True, int)` returns `True`?

??? success "Solution to Exercise 2"
    Output:

    ```text
    True
    False
    True
    True
    ```

    `type(True)` returns `<class 'bool'>`, not `<class 'int'>`. So `type(True) == int` is `False`---it checks the exact type. But `isinstance(True, int)` is `True` because `bool` is a **subclass** of `int`. `isinstance` walks the inheritance chain; `type` does not. This is why `isinstance` is preferred for type checking.

---

**Exercise 3.**
A programmer uses `del` and expects the object to be immediately destroyed. Predict the output:

```python
a = [1, 2, 3]
b = a
del a

print(b)
print(type(b))
```

Is the list object destroyed when `del a` executes? How can you verify?

??? success "Solution to Exercise 3"
    Output:

    ```text
    [1, 2, 3]
    <class 'list'>
    ```

    The list is NOT destroyed. `del a` removes the name `a` from the namespace, but `b` still references the same list object. An object is only garbage-collected when its reference count drops to zero (no names or other references point to it). You can verify the object survives by printing `b`---it still works. After `del a`, only `print(a)` would raise `NameError`.
