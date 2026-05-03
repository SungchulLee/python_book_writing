# Namespace Implementation

!!! tip "Mental Model"
    Under the hood, every namespace is literally a Python dictionary mapping name strings to object references. `globals()` hands you that dictionary directly; understanding this makes dynamic variable creation, `exec`, and metaprogramming far less mysterious.

## Dictionary Storage

### 1. Namespace is Dict

```python
# Namespace = dictionary
x = 10
y = 20

print(locals())
# {'x': 10, 'y': 20, ...}
```

### 2. Access

```python
# Direct access
namespace = locals()
print(namespace['x'])  # 10

# Equivalent to
print(x)  # 10
```

## Local Namespace

### 1. Function Locals

```python
def function():
    x = 10
    y = 20
    
    # View namespace
    print(locals())
    # {'x': 10, 'y': 20}

function()
```

### 2. Fast Locals

CPython optimization:

```python
# Local variables stored in array
# locals() creates dict copy

def f():
    x = 10
    # x stored in fast locals (array)
    # Not in dict initially
```

## Global Namespace

### 1. Module Dict

```python
x = 10

# Module __dict__
print(globals()['x'])  # 10

# Same as
print(x)  # 10
```

### 2. Module Attributes

```python
import sys

# Current module
this_module = sys.modules[__name__]

# Access via attribute
x = 10
print(this_module.x)  # 10
```

## Built-in Namespace

### 1. Builtins Module

```python
import builtins

# Access built-ins
print(builtins.len)
print(builtins.print)

# Check existence
print(hasattr(builtins, 'len'))  # True
```

## Dynamic Access

### 1. vars()

```python
x = 10
y = 20

# Get namespace dict
namespace = vars()
print(namespace['x'])  # 10
```

### 2. getattr()

```python
import sys

# Get attribute dynamically
module = sys.modules[__name__]
value = getattr(module, 'x', None)
```

## Frame Namespace

### 1. Frame Locals

```python
import inspect

def function():
    x = 10
    
    frame = inspect.currentframe()
    print(frame.f_locals)
    # {'x': 10, 'frame': ...}

function()
```

### 2. Frame Globals

```python
import inspect

def function():
    frame = inspect.currentframe()
    print('x' in frame.f_globals)

function()
```

## Class Namespace

### 1. Class Dict

```python
class MyClass:
    x = 10
    y = 20

# Class __dict__
print(MyClass.__dict__['x'])  # 10
```

### 2. Instance Dict

```python
class MyClass:
    def __init__(self):
        self.x = 10

obj = MyClass()
print(obj.__dict__)  # {'x': 10}
```

## Modification

### 1. Direct Modification

```python
# Add to namespace
globals()['new_var'] = 42
print(new_var)  # 42
```

### 2. Warning

```python
# locals() modification doesn't work!
def f():
    locals()['x'] = 10
    # print(x)  # NameError

# Use normal assignment
def g():
    x = 10  # Correct
```

## Summary

### 1. Implementation

- Namespaces are dicts
- Fast locals optimization
- Module __dict__
- Class/instance __dict__

### 2. Access

- locals() / globals()
- vars()
- Frame objects
- Direct dict access

---

## Exercises

**Exercise 1.**
`locals()` inside a function returns a snapshot, not a live reference. Predict the output:

```python
def f():
    x = 10
    d = locals()
    x = 20
    print(d['x'])
    print(locals()['x'])

f()
```

Why does the first `d['x']` print `10` while the second `locals()['x']` prints `20`? What does "snapshot" mean in this context?

??? success "Solution to Exercise 1"
    Output:

    ```text
    10
    20
    ```

    `locals()` creates a **new dictionary** each time it is called, populated from the current state of the fast-locals array. `d = locals()` captures the state when `x` is `10`. After `x = 20`, calling `locals()` again creates a new dictionary reflecting the updated state.

    The dictionary `d` is not connected to the live local variables. CPython stores local variables in a C-level array (fast locals) for performance. `locals()` copies from this array into a fresh dict. Modifying `d` does not affect the fast locals, and modifying the fast locals does not retroactively update `d`.

---

**Exercise 2.**
Modifying `globals()` creates real bindings, but modifying `locals()` does not. Predict the output:

```python
globals()['dynamic_var'] = 42
print(dynamic_var)

def g():
    locals()['phantom'] = 99
    try:
        print(phantom)
    except NameError as e:
        print(e)

g()
```

Why does modifying `globals()` work while modifying `locals()` inside a function has no effect? What CPython optimization explains this asymmetry?

??? success "Solution to Exercise 2"
    Output:

    ```text
    42
    name 'phantom' is not defined
    ```

    `globals()` returns the **actual module namespace dictionary**. Writing to it genuinely creates a new binding in the global namespace, so `dynamic_var` becomes a real global variable.

    `locals()` inside a function returns a **copy** of the fast-locals array. Writing to this copy does nothing because CPython's function locals are stored in a fixed-size C array, not in a dictionary. The `locals()` dictionary is created on demand and is not used for actual variable lookup. This optimization (called "fast locals") is why local variable access is faster than global access.

---

**Exercise 3.**
Class and instance namespaces are separate `__dict__` objects. Predict the output:

```python
class MyClass:
    x = "class"

obj = MyClass()
print("x" in obj.__dict__)
print("x" in MyClass.__dict__)

obj.x = "instance"
print("x" in obj.__dict__)
print(obj.x)
print(MyClass.x)
```

Why is `x` not in `obj.__dict__` initially? After `obj.x = "instance"`, why does `MyClass.x` remain `"class"`?

??? success "Solution to Exercise 3"
    Output:

    ```text
    False
    True
    True
    instance
    class
    ```

    Initially, `obj.__dict__` is empty (`{}`). `x` is defined in `MyClass.__dict__`, not on the instance. When you access `obj.x`, Python's attribute lookup checks `obj.__dict__` first, finds nothing, then checks `type(obj).__dict__` (i.e., `MyClass.__dict__`) and finds `"class"`.

    After `obj.x = "instance"`, Python creates an entry in `obj.__dict__`: `{'x': 'instance'}`. Now `obj.x` finds `"instance"` in the instance dict and never reaches the class dict. But `MyClass.x` directly accesses `MyClass.__dict__['x']`, which is still `"class"`. Instance and class namespaces are completely separate dictionaries.
