# Key Terms

!!! tip "Mental Model"
    Python's core vocabulary -- binding, namespace, scope, closure -- all describe one underlying mechanism: names are entries in dictionaries, and those dictionaries are organized in a chain. Mastering the terminology is mastering the lookup rules.

## Core Concepts

### 1. Binding

**Definition**: The association of a name with an object in a namespace

```python
x = 42  # Binds name 'x' to integer object 42
```

**Key Properties**:

- Names stored in namespaces (dictionaries)
- Objects stored in heap memory
- Multiple names can bind to same object

### 2. Namespace

**Definition**: A mapping from names to objects (implemented as dictionaries)

```python
# Module namespace
globals()  # Returns global namespace dict

# Function namespace
def f():
    x = 1
    return locals()  # Returns local namespace dict
```

**Types**:

- **Local**: Function/method scope
- **Enclosing**: Nested function scopes
- **Global**: Module level
- **Built-in**: Python built-ins

### 3. Closure

**Definition**: A function that captures variables from its enclosing scope

```python
def outer():
    x = 10
    def inner():
        return x  # Captures 'x' from outer
    return inner

f = outer()
print(f())  # 10 - closure remembers x
```

### 4. Frame Object

**Definition**: Runtime structure containing execution context and local variables

```python
import inspect

def example():
    frame = inspect.currentframe()
    print(frame.f_locals)  # Local namespace
    print(frame.f_globals)  # Global namespace

example()
```

## Memory Management

### 1. Interning

**Definition**: Optimization where identical immutable objects share memory

```python
# String interning
s1 = "hello"
s2 = "hello"
print(s1 is s2)  # True - same object

# Integer caching (CPython: -5 to 256)
a = 42
b = 42
print(a is b)  # True - cached
```

### 2. Reference Count

**Definition**: Number of names/variables pointing to an object

```python
import sys

x = [1, 2, 3]
y = x
print(sys.getrefcount(x))  # 3 (x, y, temp in getrefcount)
```

### 3. GC Generation

**Definition**: Age-based grouping for garbage collection efficiency

```python
import gc

# CPython uses generational GC
# Generation 0: Young objects
# Generation 1: Survived one collection
# Generation 2: Long-lived objects

print(gc.get_count())  # (count0, count1, count2)
```

### 4. Environment

**Definition**: Formal term for namespace context in language semantics

In formal semantics:

- Environment: Γ (gamma)
- Binding: Γ[x ↦ v] means "bind x to value v in Γ"

## Object Model

### 1. Identity

**Definition**: Unique identifier for object's memory location

```python
x = [1, 2, 3]
print(id(x))  # Object identity (address in CPython)
```

### 2. Type

**Definition**: Determines operations on the object

```python
x = 42
print(type(x))  # <class 'int'>
```

### 3. Value

**Definition**: The actual data stored in the object

```python
x = [1, 2, 3]
# Identity: id(x)
# Type: list
# Value: [1, 2, 3]
```

## Scoping Terms

### 1. Free Variable

**Definition**: Variable referenced in function but not defined locally

```python
x = 10
def f():
    return x  # x is free variable
```

### 2. Cell Object

**Definition**: CPython structure storing values for free variables

```python
def outer():
    x = 42
    def inner():
        return x
    print(inner.__closure__[0].cell_contents)  # 42
    return inner
```

### 3. LEGB

**Definition**: Scope resolution order: Local, Enclosing, Global, Built-in

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print(x)  # "local" (finds in Local first)
    inner()

outer()
```

## Quick Reference

| Term | One-Line Definition |
|------|-------------------|
| **Binding** | Name → Object association |
| **Namespace** | Name → Object mapping |
| **Closure** | Function + captured vars |
| **Frame** | Execution context |
| **Interning** | Sharing immutables |
| **Refcount** | # of refs to object |
| **Environment** | Formal namespace |
| **Free Variable** | Non-local variable |
| **Cell** | Closure var container |
| **LEGB** | Scope lookup order |

---

## Exercises

**Exercise 1.**
Closures capture variables by reference, not by value. Predict the output:

```python
def make_functions():
    funcs = []
    for i in range(3):
        def f():
            return i
        funcs.append(f)
    return funcs

results = [f() for f in make_functions()]
print(results)
```

Why do all three functions return `2`? What does "capture by reference" mean in terms of the cell object that stores the variable `i`? How would you fix this to get `[0, 1, 2]`?

??? success "Solution to Exercise 1"
    Output:

    ```text
    [2, 2, 2]
    ```

    All functions return `2` because they all reference the **same cell object** containing the variable `i`. The closure does not capture the value of `i` at the time `f` is defined -- it captures a reference to the variable itself. By the time any `f()` is called, the loop has finished and `i` is `2`.

    Internally, CPython stores closure variables in **cell objects**. All three functions' `__closure__` tuples point to the same cell, which holds whatever `i`'s current value is.

    Fix: capture `i` by value using a default argument: `def f(i=i): return i`. Default arguments are evaluated at function definition time, so each function gets its own snapshot of `i`.

---

**Exercise 2.**
Namespaces are dictionaries. Predict the output:

```python
x = 10

def f():
    y = 20
    print("y" in locals())
    print("x" in locals())
    print("x" in globals())

f()
print(type(globals()))
```

Why is `x` not in `f`'s `locals()` even though `f` can access `x`? What is the relationship between LEGB lookup and the actual dictionary objects returned by `locals()` and `globals()`?

??? success "Solution to Exercise 2"
    Output:

    ```text
    True
    False
    True
    <class 'dict'>
    ```

    `y` is in `f`'s locals because it is assigned inside `f`. `x` is **not** in `f`'s locals because `f` never assigns to `x` -- it only reads `x` from the global scope.

    `locals()` returns only the names bound in the **current** scope. LEGB lookup is a chain of dictionary lookups: Python first checks `locals()`, then enclosing scopes, then `globals()`, then `builtins`. The fact that `f` can access `x` does not make `x` part of `f`'s local namespace. `globals()` is always a `dict`, and `locals()` inside a function returns a snapshot of the fast-locals array as a dict.

---

**Exercise 3.**
Reference counting determines when objects are freed. Predict the output:

```python
import sys

a = [1, 2, 3]
print(sys.getrefcount(a))

b = a
print(sys.getrefcount(a))

c = [a, a]
print(sys.getrefcount(a))

del b
print(sys.getrefcount(a))
```

Why does `sys.getrefcount` always show one more than expected? What happens to `a`'s reference count when it is placed inside a list?

??? success "Solution to Exercise 3"
    Output:

    ```text
    2
    3
    5
    4
    ```

    `sys.getrefcount(a)` shows one extra because the function call itself creates a temporary reference to `a` as an argument.

    - After `a = [1, 2, 3]`: 1 reference from `a`, + 1 from `getrefcount` = 2
    - After `b = a`: 2 references (`a`, `b`), + 1 = 3
    - After `c = [a, a]`: 4 references (`a`, `b`, `c[0]`, `c[1]`), + 1 = 5
    - After `del b`: 3 references (`a`, `c[0]`, `c[1]`), + 1 = 4

    Placing `a` inside a list increments its reference count because the list stores a reference to the object. Each slot in `c` holds a separate reference, so `[a, a]` adds 2 to the count.
