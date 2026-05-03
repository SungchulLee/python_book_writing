# Names vs Objects

!!! tip "Mental Model"
    A Python name is a sticky note, not a box. You stick it on an object that lives on the heap; you can peel it off and stick it on a different object at any time. Multiple sticky notes can point to the same object, which is why changes through one name are visible through another.

## Core Distinction

### 1. Python Model

Names are references to objects, not containers holding values:

```python
x = [1, 2, 3]
# x is a name pointing to list object in heap
```

```
x ───► [1, 2, 3]   (heap object)
       │
       ├── id: 0x7f...
       ├── type: list
       └── value: [1, 2, 3]
```

The arrow (`→`) is a **pointer/reference**, not a copy.

### 2. Key Insight

```python
x = [1, 2, 3]
y = x
z = x

# Multiple names, one object
print(x is y is z)  # True
```

```
x ─┬──► [1, 2, 3]
   │
y ─┤
   │
z ─┘
```

## Object Properties

### 1. Three Characteristics

```python
x = [1, 2, 3]

print(id(x))        # Identity
print(type(x))      # Type
print(x)            # Value
```

### 2. Identity Persists

```python
x = [1, 2, 3]
original_id = id(x)

x.append(4)
print(id(x) == original_id)  # True
```

## Name Binding

### 1. Assignment

```python
x = [1, 2, 3]
y = x

print(id(x) == id(y))  # True
```

### 2. Rebinding

```python
x = [1, 2, 3]
y = x

x = [4, 5, 6]

print(x is y)       # False
```


## Summary

### 1. Key Points

- Names are references
- Objects have identity/type/value
- Assignment binds names
- Multiple names → one object


## Exercises

**Exercise 1.**
A student from a C/Java background says: "Variables are boxes that store values." Explain why this mental model is incorrect in Python. What is the correct model? Use the following code to illustrate the difference:

```python
a = [1, 2, 3]
b = a
a = [4, 5, 6]
print(b)
```

If variables were "boxes," what would `b` contain? What does it actually contain, and why?

??? success "Solution to Exercise 1"
    Output: `[1, 2, 3]`

    If variables were "boxes," then `a = [1, 2, 3]` would put the list in box `a`. `b = a` would copy the contents into box `b`. `a = [4, 5, 6]` would replace the contents of box `a`. `b` would still contain `[1, 2, 3]` -- which happens to be correct here, but for the **wrong reason**.

    The correct Python model: `a = [1, 2, 3]` creates a list object and binds the **name** `a` to it. `b = a` binds the name `b` to the **same object** (not a copy). `a = [4, 5, 6]` creates a new list object and **rebinds** the name `a` to it. `b` still refers to the original list.

    The "box" model fails for mutation: if we instead did `a.append(4)` (without rebinding `a`), the list itself changes, and `b` would see `[1, 2, 3, 4]` -- impossible if `b` were an independent "box."

---

**Exercise 2.**
Predict the output and explain:

```python
a = "hello"
b = a
a = a + " world"
print(b)
print(a is b)
```

Why does `b` still contain `"hello"` even though `a` was originally bound to the same object? What happened to the name `a` when `a + " world"` was computed?

??? success "Solution to Exercise 2"
    Output:

    ```text
    hello
    False
    ```

    Initially, `a` and `b` both refer to the same `str` object `"hello"`. The expression `a + " world"` creates a **new** `str` object `"hello world"` (because strings are immutable -- concatenation always produces a new object). The assignment `a = a + " world"` rebinds `a` to this new object.

    `b` was never modified -- it still refers to the original `"hello"` object. The name `a` was rebound to a different object, which does not affect `b`. `a is b` is `False` because they now refer to different objects.

    This is the fundamental difference between rebinding (changing which object a name refers to) and mutation (changing an object's contents). Immutable types like `str` can only be "changed" through rebinding, which never affects other names.

---

**Exercise 3.**
Explain the difference between "the object is deleted" and "the name is deleted" in Python. What does `del x` actually do? Consider:

```python
a = [1, 2, 3]
b = a
del a
print(b)
```

Is the list object destroyed when `del a` executes? Why or why not?

??? success "Solution to Exercise 3"
    `del a` removes the **name** `a` from the current namespace. It does NOT destroy the object that `a` referred to. After `del a`, accessing `a` would raise `NameError`.

    Output: `[1, 2, 3]`

    The list object is NOT destroyed because `b` still refers to it. Python uses **reference counting** (and a garbage collector) to manage object lifetimes. Each object tracks how many names/references point to it. When `del a` executes, the reference count of the list decreases from 2 to 1 (only `b` refers to it now). The object is only destroyed when its reference count reaches 0 -- meaning no name or container holds a reference to it.

    `del` removes bindings (names), not objects. Objects are destroyed automatically when they become unreachable.
