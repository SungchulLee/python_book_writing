
# Mutable vs Immutable Types

Every Python object has a fixed identity (its address in memory) and a type. Some types allow
the object's internal state to change after creation; others do not. This distinction---**mutable**
versus **immutable**---is one of the most important mental models in the language.

Think of it this way: a mutable object is like a whiteboard. You can erase parts, write new
content, and the board itself remains the same physical object. An immutable object is like a
printed page. To "change" it, you must create an entirely new page; the original stays as it was.

!!! tip "Mental Model"
    Mutable objects can be changed after creation; immutable objects cannot. When you "modify" an immutable value like a string, Python actually creates a brand-new object and rebinds the name to it. This single distinction determines whether aliases share changes and whether a type can serve as a dictionary key.

---

## 1. Classification of Built-in Types

Python's core types split cleanly into two groups.

| Mutable | Immutable |
| ------- | --------- |
| `list` | `int` |
| `dict` | `float` |
| `set` | `str` |
| `bytearray` | `tuple` |
| | `frozenset` |
| | `bytes` |
| | `bool` |

The rule is simple: if the type provides methods or operations that modify the object in place,
it is mutable. If every "modification" produces a new object, it is immutable.

---

## 2. What Immutability Means Precisely

An immutable object's **state cannot change after creation**. The object continues to exist at
the same memory address, but no operation can alter its contents.

```python
s = "hello"
print(id(s))

s = s + " world"
print(id(s))
```

Output:

```text
140234866482992
140234866483056
```

The two `id` values differ. The string `"hello"` was never modified. Instead, `s + " world"`
created a brand-new string object, and the name `s` was rebound to point at it. The original
`"hello"` object still exists unchanged (until garbage collected).

---

## 3. Attempting to Modify an Immutable Object

Trying to mutate an immutable object raises a `TypeError`.

```python
t = (1, 2, 3)
t[0] = 99
```

Output:

```text
TypeError: 'tuple' object does not support item assignment
```

The same applies to strings.

```python
s = "hello"
s[0] = "H"
```

Output:

```text
TypeError: 'str' object does not support item assignment
```

Python does not silently ignore the attempt---it raises an error immediately.

---

## 4. Mutable Objects Can Change in Place

Mutable objects support operations that alter their internal state without creating a new object.

```python
nums = [10, 20, 30]
print(id(nums))

nums.append(40)
print(id(nums))
print(nums)
```

Output:

```text
140234866520000
140234866520000
[10, 20, 30, 40]
```

The `id` stays the same. The list object itself was modified; no new list was created.

---

## 5. The Subtlety: Tuples Containing Mutable Elements

A tuple is immutable, meaning you cannot add, remove, or reassign its elements. However, if one
of those elements is itself a mutable object, the mutable object's contents can still change.

```python
pair = ([1, 2], [3, 4])
pair[0].append(99)
print(pair)
```

Output:

```text
([1, 2, 99], [3, 4])
```

The tuple `pair` still holds the **same two list objects** it held at creation. The tuple itself
has not changed---it still contains references to the same objects at the same memory addresses.
But the list that `pair[0]` refers to is mutable, so its contents can change.

This is a common source of confusion. The tuple's guarantee is about its own structure (which
slots point to which objects), not about the internal state of the objects in those slots.

What you **cannot** do is reassign a slot in the tuple.

```python
pair = ([1, 2], [3, 4])
pair[0] = [10, 20]
```

Output:

```text
TypeError: 'tuple' object does not support item assignment
```

---

## 6. Augmented Assignment and Tuples

The `+=` operator on a tuple element that is a list reveals this subtlety in a surprising way.

```python
t = ([1, 2],)
try:
    t[0] += [3]
except TypeError as e:
    print(e)
print(t)
```

Output:

```text
'tuple' object does not support item assignment
([1, 2, 3],)
```

Both things happen: the list is mutated in place (because `list.__iadd__` extends the list),
**and** a `TypeError` is raised (because the tuple rejects the assignment back to slot 0). The
list ends up modified even though the operation raised an error.

---

## 7. Checking Mutability with id

A practical way to test whether an operation mutates an object or creates a new one is to compare
`id` values before and after.

```python
# Immutable: id changes
x = 10
print(id(x))
x += 1
print(id(x))

# Mutable: id stays the same
y = [10]
print(id(y))
y.append(20)
print(id(y))
```

Output:

```text
140234866389008
140234866389040
140234866520064
140234866520064
```

For the integer, `x += 1` created a new `int` object. For the list, `y.append(20)` modified
the existing object.

---

## 8. Summary

Key ideas:

- Immutable types (`int`, `str`, `tuple`, `frozenset`, `bytes`, `bool`, `float`) cannot be
  changed after creation. Any "modification" produces a new object.
- Mutable types (`list`, `dict`, `set`, `bytearray`) can be changed in place. The object's
  identity stays the same.
- A tuple is immutable in its structure, but if it contains mutable elements, those elements
  can still be modified.
- Attempting to mutate an immutable object raises `TypeError`.
- Use `id()` to verify whether an operation creates a new object or modifies the existing one.

---

## Exercises

**Exercise 1.**
Predict the output of the following code. Explain why the `id` comparison produces the result
it does.

```python
a = "Python"
b = a
a = a.upper()

print(a)
print(b)
print(a is b)
```

??? success "Solution to Exercise 1"
    Output:

    ```text
    PYTHON
    Python
    False
    ```

    Strings are immutable. `a.upper()` does not modify the original string `"Python"`. Instead,
    it creates a **new** string `"PYTHON"` and rebinds the name `a` to point at it. The name `b`
    still refers to the original `"Python"` object. Since `a` and `b` now point to different
    objects, `a is b` evaluates to `False`.

---

**Exercise 2.**
Consider this code:

```python
t = (1, [2, 3], "hello")
t[1].append(4)
print(t)
```

Does this raise a `TypeError`? Why or why not? What would happen if you tried `t[2] = "world"`
instead?

??? success "Solution to Exercise 2"
    No, it does **not** raise a `TypeError`. The output is:

    ```text
    (1, [2, 3, 4], 'hello')
    ```

    The tuple `t` is immutable---you cannot reassign its elements. But `t[1]` is a **list**, which
    is mutable. Calling `t[1].append(4)` modifies the list object that the tuple references. The
    tuple's structure has not changed: slot 1 still points to the same list object (same `id`).
    Only the list's internal contents have changed.

    If you tried `t[2] = "world"`, Python would raise:

    ```text
    TypeError: 'tuple' object does not support item assignment
    ```

    This fails because it attempts to change which object the tuple's slot 2 refers to, which
    is exactly what tuple immutability prevents.

---

**Exercise 3.**
A programmer writes this function intended to toggle a flag stored as an integer and also
append to a log list:

```python
def update(flag, log):
    flag += 1
    log.append("updated")

flag = 0
log = []
update(flag, log)

print(flag)
print(log)
```

Predict the output. Explain why `flag` is unchanged after the call but `log` is not.

??? success "Solution to Exercise 3"
    Output:

    ```text
    0
    ['updated']
    ```

    Inside the function, `flag += 1` creates a **new** integer object (because `int` is
    immutable) and binds the local name `flag` to it. The caller's `flag` variable still points
    to the original integer `0`. Rebinding a local name has no effect on the caller.

    In contrast, `log.append("updated")` **mutates** the existing list object (because `list` is
    mutable). Both the caller's `log` and the function's `log` refer to the same list object, so
    the change is visible after the function returns.

    This is a critical distinction: passing a mutable object to a function allows the function to
    modify it in place, while passing an immutable object does not. Python's calling convention
    is "pass by object reference"---the function receives a reference to the same object, but
    rebinding the local name does not affect the caller.
