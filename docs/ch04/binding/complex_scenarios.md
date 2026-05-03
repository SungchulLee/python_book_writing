# Complex Scenarios

!!! tip "Mental Model"
    When closures, classes, and nested scopes interact, the key question is always the same: which namespace does this name resolve in, and when? Tracing the LEGB chain at call time -- not definition time -- reveals why late binding and `nonlocal`/`global` behave the way they do.

## Nested Functions

### 1. Closure Binding

```python
def outer():
    x = 10
    
    def inner():
        return x  # Binds to outer's x
    
    return inner

f = outer()
print(f())  # 10
```

### 2. Multiple Levels

```python
def level1():
    x = 1
    
    def level2():
        x = 2
        
        def level3():
            return x  # Binds to level2's x
        
        return level3()
    
    return level2()

print(level1())  # 2
```

## Class Attributes

### 1. Instance Binding

```python
class MyClass:
    def __init__(self):
        self.x = 10  # Instance attribute

obj = MyClass()
print(obj.x)  # 10
```

### 2. Class Binding

```python
class MyClass:
    x = 10  # Class attribute
    
    def __init__(self):
        self.y = 20  # Instance attribute

obj = MyClass()
print(obj.x)  # 10 (class)
print(obj.y)  # 20 (instance)
```

## Late Binding

### 1. Loop Problem

```python
# Common mistake
funcs = []
for i in range(3):
    funcs.append(lambda: i)

# All return 2!
print([f() for f in funcs])  # [2, 2, 2]
```

### 2. Solution

```python
# Capture with default
funcs = []
for i in range(3):
    funcs.append(lambda x=i: x)

print([f() for f in funcs])  # [0, 1, 2]
```

## Shadowing

### 1. Local Shadows Global

```python
x = 10  # Global

def function():
    x = 20  # Local shadows global
    print(x)  # 20

function()
print(x)  # 10
```

### 2. Parameter Shadowing

```python
x = 10

def function(x):  # Parameter shadows global
    print(x)

function(20)  # 20
```

## Nonlocal Binding

### 1. Modify Enclosing

```python
def outer():
    x = 10
    
    def inner():
        nonlocal x
        x = 20
    
    inner()
    print(x)  # 20

outer()
```

### 2. Multiple Levels

```python
def level1():
    x = 1
    
    def level2():
        nonlocal x
        x = 2
        
        def level3():
            nonlocal x
            x = 3
        
        level3()
    
    level2()
    print(x)  # 3

level1()
```

## Comprehensions

### 1. Own Scope

```python
x = 10

# Comprehension has own scope
result = [x for x in range(3)]

print(x)  # 10 (unchanged)
```

### 2. Variable Leak

```python
# In Python 2, leaked
# In Python 3, doesn't leak
[i for i in range(3)]

# print(i)  # NameError in Python 3
```

## Dynamic Binding

### 1. Runtime Creation

```python
# Create binding at runtime
name = "x"
value = 42

globals()[name] = value
print(x)  # 42
```

### 2. exec()

```python
# Dynamic code execution
code = "y = 100"
exec(code)

print(y)  # 100
```

## Summary

### 1. Complex Cases

- Closures
- Class attributes
- Late binding
- Shadowing
- Nonlocal

### 2. Best Practices

- Avoid shadowing
- Use defaults for loops
- Be explicit with nonlocal
- Limit dynamic binding

---

## Exercises

**Exercise 1.**
Closures with `nonlocal` can modify enclosing variables. Predict the output:

```python
def counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

c1 = counter()
c2 = counter()

print(c1())
print(c1())
print(c2())
print(c1())
```

Why do `c1` and `c2` maintain independent counts? What happens if you remove the `nonlocal` declaration?

??? success "Solution to Exercise 1"
    Output:

    ```text
    1
    2
    1
    3
    ```

    Each call to `counter()` creates a **new** frame with its own `count = 0`. The returned `increment` function captures that specific frame's `count` via a cell object. `c1` and `c2` point to different cell objects containing independent `count` variables.

    Without `nonlocal`, `count += 1` would raise `UnboundLocalError`. The `+=` makes `count` a local variable (because it includes assignment), but the local `count` has no value yet when the `+= 1` tries to read it. `nonlocal` tells Python to use the enclosing scope's `count` instead of creating a new local.

---

**Exercise 2.**
Class attribute vs instance attribute binding follows different lookup rules. Predict the output:

```python
class Shared:
    data = []

a = Shared()
b = Shared()

a.data.append(1)
print(b.data)

a.data = [99]
print(b.data)
print(a.data)
print(a.__dict__)
print(b.__dict__)
```

Why does `a.data.append(1)` affect `b.data`, but `a.data = [99]` does not? What is the difference between mutating a class attribute and rebinding an instance attribute?

??? success "Solution to Exercise 2"
    Output:

    ```text
    [1]
    [1]
    [99]
    {'data': [99]}
    {}
    ```

    `a.data.append(1)` **mutates** the class attribute `Shared.data`. Since `a` has no instance attribute named `data`, Python looks up the class and finds `Shared.data`. The `.append()` modifies this shared list in place, so `b.data` sees the change.

    `a.data = [99]` **creates an instance attribute** on `a` that shadows the class attribute. Now `a.__dict__` contains `{'data': [99]}`, while `b` still has no instance `data` and falls through to `Shared.data` (which is `[1]`).

    The rule: attribute **read** walks instance → class → bases. Attribute **write** always writes to the instance (unless using descriptors). Mutation via method calls does not create a new binding.

---

**Exercise 3.**
Name shadowing can cause subtle bugs. Predict the output:

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        print(x)
    inner()

    def inner2():
        print(x)
        x = "local"
    inner2()

outer()
```

Why does `inner()` work but `inner2()` raise `UnboundLocalError`? At what point does Python decide that `x` in `inner2` is a local variable?

??? success "Solution to Exercise 3"
    `inner()` prints `"enclosing"` successfully. `inner2()` raises `UnboundLocalError: local variable 'x' referenced before assignment`.

    Python's compiler (not the runtime) scans the entire function body at **compile time**. Because `inner2` contains `x = "local"`, the compiler marks `x` as a **local variable** in `inner2`'s scope. This decision is made before any code runs. When `print(x)` executes, Python looks for `x` in the local scope (because the compiler said it's local) but finds it hasn't been assigned yet.

    This is a fundamental aspect of Python's scoping: the scope of a variable is determined statically by the compiler based on assignment statements anywhere in the function body, not by the order of execution.
