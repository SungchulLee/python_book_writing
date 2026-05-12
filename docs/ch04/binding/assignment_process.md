# Assignment Process

Understanding how Python executes assignment statements and binds names to objects.

!!! tip "Mental Model"
    Think of assignment as a two-phase operation: first Python evaluates the right side to produce an object, then it attaches a name tag to that object. The name never "holds" the value -- it only points to where the object lives in memory.

## Assignment Steps

When Python executes an assignment statement, it follows these steps:

### Step 1: Evaluate the Right-Hand Side (RHS)

The expression on the right side is evaluated first:

```python
x = 2 + 3
# 1. Evaluate 2 + 3 → 5
# 2. Bind x to 5
```

```python
y = len([1, 2, 3]) * 2
# 1. Evaluate len([1, 2, 3]) → 3
# 2. Evaluate 3 * 2 → 6
# 3. Bind y to 6
```

### Step 2: Create/Update Binding

The name is bound to the resulting object in the appropriate namespace:

```python
x = 42  # Creates binding in local namespace
# Equivalent to: locals()['x'] = 42
```

## Basic Binding Operations

### Create Binding

```python
x = 42
# Name 'x' now bound to 42
print(x)  # 42
```

### Rebinding

Assigning to an existing name creates a new binding:

```python
x = 42
x = "hello"  # x now refers to a different object
```

The old object (`42`) is not modified—`x` simply points to a new object.

### Delete Binding

```python
x = 42
print(x)  # 42

del x
# print(x)  # NameError
```

Note that `del` removes the binding, not the object:

```python
x = [1, 2, 3]
y = x

del x
print(y)  # [1, 2, 3] - object still exists
```

## Multiple Assignment

### Simultaneous (Tuple Unpacking)

```python
a, b = 1, 2
# Equivalent to:
# temp = (1, 2)
# a = temp[0]
# b = temp[1]
```

```python
x, y, z = 1, 2, 3
print(x, y, z)  # 1 2 3
```

### Chained Assignment

```python
x = y = z = 0
# All three names bound to the same object
print(x is y is z)  # True
```

### Swap Values

```python
a, b = b, a
# RHS evaluated first: (b, a) tuple created
# Then unpacked to a, b
```

## Namespace and Scope

### Local Namespace

```python
def function():
    x = 10  # Binds in local namespace
    y = 20
    print(locals())  # {'x': 10, 'y': 20}

function()
# print(x)  # NameError - not in scope
```

### Global Namespace

```python
x = 10  # Module-level binding

def function():
    print(x)  # Access global

function()  # 10
print('x' in globals())  # True
```

### Namespace Updates

Assignment modifies the appropriate namespace:

```python
x = 10  # Updates globals()

def func():
    y = 20  # Updates locals()
    global z
    z = 30  # Updates globals()
```

## Special Binding Forms

### Import Bindings

```python
import math
# 'math' bound in namespace
print('math' in dir())  # True

from math import pi
# 'pi' bound in namespace
print(pi)  # 3.14159...
```

### Function and Class Bindings

```python
def greet():
    return "Hello"

# 'greet' bound to function object
print(type(greet))  # <class 'function'>
```

```python
class MyClass:
    pass

# 'MyClass' bound to class object
print(type(MyClass))  # <class 'type'>
```

### Walrus Operator

```python
x = (a := 5) + (b := 10)
# 1. Evaluate (a := 5) → assigns 5 to a, returns 5
# 2. Evaluate (b := 10) → assigns 10 to b, returns 10
# 3. Evaluate 5 + 10 → 15
# 4. Bind x to 15
```

## Summary

| Step | Description |
|------|-------------|
| 1 | Evaluate right-hand side expression |
| 2 | Create object (if needed) |
| 3 | Bind name to object in namespace |

### Binding Operations

| Operation | Syntax | Effect |
|-----------|--------|--------|
| Create | `x = value` | New binding |
| Update | `x = new_value` | Rebind name |
| Delete | `del x` | Remove binding |
| Access | `x` | Lookup in namespace |

Key points:

- RHS always evaluated first
- Assignment binds names, doesn't copy values
- Multiple assignment uses unpacking
- Namespace determines scope of binding
- `del` removes bindings, not objects

## Exercises

**Exercise 1.**
Predict the output by tracing the evaluation order:

```python
a = 5
b = 10
a, b = b, a + b
print(a, b)
```

In what order are the right-hand side expressions evaluated? When does the binding happen? Why does Python's rule of "evaluate the entire RHS first, then bind" matter for swap operations?

??? success "Solution to Exercise 1"
    Output: `10 15`

    Python evaluates the entire right-hand side **before** any binding occurs:

    1. Evaluate `b` -> `10`
    2. Evaluate `a + b` -> `5 + 10` -> `15`
    3. Pack into a tuple: `(10, 15)`
    4. Unpack and bind: `a = 10`, `b = 15`

    The "evaluate RHS first" rule is critical: `a + b` uses the **old** values of `a` and `b` (5 and 10), not the new ones. This is why `a, b = b, a` works as a swap -- both old values are captured before any rebinding occurs.

    In languages where assignment happens left-to-right (like some C expressions), `a, b = b, a + b` would use the already-updated `a` in the second expression, producing a different result.

---

**Exercise 2.**
Explain what `del x` does vs. what it does NOT do. Predict the output:

```python
a = [1, 2, 3]
b = a
del a
print(b)
# print(a)  # What would this do?
```

Does `del a` destroy the list? Does it affect `b`? What exactly is removed?

??? success "Solution to Exercise 2"
    Output: `[1, 2, 3]`

    `del a` removes the **name** `a` from the current namespace. It does NOT destroy the list object. After `del a`, the name `a` no longer exists -- `print(a)` would raise `NameError: name 'a' is not defined`.

    `b` is unaffected because `del a` only removes the binding between the name `a` and the object. The list object still exists because `b` still references it (reference count goes from 2 to 1, not to 0).

    `del` removes **bindings** (name-to-object associations), not objects. Objects are destroyed automatically by the garbage collector when no references to them remain.

---

**Exercise 3.**
Consider this chained assignment:

```python
a = b = [1, 2, 3]
a.append(4)
print(b)
```

Predict the output. Is `a = b = [1, 2, 3]` equivalent to `a = [1, 2, 3]; b = [1, 2, 3]`? Why or why not? How many list objects are created?

??? success "Solution to Exercise 3"
    Output: `[1, 2, 3, 4]`

    `a = b = [1, 2, 3]` creates **one** list object and binds both `a` and `b` to it. This is NOT equivalent to `a = [1, 2, 3]; b = [1, 2, 3]`, which creates **two** separate list objects.

    The chained assignment evaluates the RHS once (creating one list), then binds all target names to that single object, from left to right. Since `a` and `b` refer to the same list, `a.append(4)` mutates the shared object, and `b` sees the change.

    Only **one** list object is created. `a is b` is `True`.
