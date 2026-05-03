# Late Binding and Closure Capture

When a nested function references variables from its enclosing scope, Python creates a closure. Understanding how closures capture variables—and the "late binding" behavior—is essential for avoiding subtle bugs.

!!! tip "Mental Model"
    Closures capture variables by reference, not by value -- they hold a pointer to the name, not a snapshot of its current value. This means the closure always sees the variable's latest value at the time it is called. When closures are created inside a loop, they all share the same loop variable and all see its final value -- the classic late-binding trap.

---

## What is a Closure?

A closure is a function that remembers values from its enclosing scope, even after that scope has finished executing.

```python
def make_multiplier(n):
    def multiplier(x):
        return x * n  # n is captured from enclosing scope
    return multiplier

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))  # 10
print(triple(5))  # 15
```

The inner function `multiplier` "closes over" the variable `n`.

---

## How Capture Works

Python captures **variables by reference**, not by value. The closure stores a reference to the variable, not a copy of its value.

```python
def make_counter():
    count = 0
    
    def counter():
        nonlocal count
        count += 1
        return count
    
    return counter

c = make_counter()
print(c())  # 1
print(c())  # 2
print(c())  # 3
```

Each call modifies the same `count` variable.

---

## Inspecting Closures

You can examine captured variables through `__closure__`:

```python
def outer(x):
    def inner():
        return x
    return inner

f = outer(10)

print(f.__closure__)           # (<cell at 0x...>,)
print(f.__closure__[0].cell_contents)  # 10
```

---

## Late Binding Explained

Python uses **late binding** for closures—the value is looked up when the function is **called**, not when it's **defined**.

```python
def outer():
    x = 10
    def inner():
        return x  # x is looked up when inner() is called
    x = 20  # Change x after defining inner
    return inner

f = outer()
print(f())  # 20 (not 10!)
```

The closure sees the final value of `x`.

---

## The Loop Variable Gotcha

The most common closure pitfall involves loops:

```python
funcs = []
for i in range(3):
    funcs.append(lambda: i)

print([f() for f in funcs])  # [2, 2, 2] — NOT [0, 1, 2]!
```

**All functions return 2!** Why? All lambdas reference the same variable `i`, and when called, `i` is 2.

### Visualizing the Problem

```
Loop iteration 0: lambda captures reference to i (i=0)
Loop iteration 1: lambda captures reference to i (i=1)
Loop iteration 2: lambda captures reference to i (i=2)

After loop: i = 2

Call all lambdas: all look up i → all get 2
```

### With def Statement

```python
def create_functions():
    functions = []
    for i in range(3):
        def f():
            return i
        functions.append(f)
    return functions

funcs = create_functions()
print(funcs[0]())  # 2 (expected 0)
print(funcs[1]())  # 2 (expected 1)
print(funcs[2]())  # 2 (expected 2)
```

### List Comprehension Version

```python
# Same problem
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])  # [2, 2, 2]
```

---

## Solutions

### Solution 1: Default Parameter (Most Common)

Capture the current value using a default parameter:

```python
funcs = []
for i in range(3):
    funcs.append(lambda x=i: x)  # x=i evaluated NOW

print([f() for f in funcs])  # [0, 1, 2] ✓
```

Default parameters use **early binding**—the value is captured when the function is defined.

```python
# List comprehension version
funcs = [lambda x=i: x for i in range(3)]
print([f() for f in funcs])  # [0, 1, 2] ✓
```

### Solution 2: Factory Function

Create a separate scope for each iteration:

```python
def make_func(val):
    return lambda: val  # val is local to each call

funcs = [make_func(i) for i in range(3)]
print([f() for f in funcs])  # [0, 1, 2] ✓
```

Each call to `make_func` creates a new scope with its own `val`.

### Solution 3: functools.partial

Use `partial` to bind the current value:

```python
from functools import partial

def return_val(x):
    return x

funcs = [partial(return_val, i) for i in range(3)]
print([f() for f in funcs])  # [0, 1, 2] ✓
```

### Solution 4: Closure Factory (IIFE Pattern)

Immediately invoked function expression:

```python
funcs = [(lambda x: lambda: x)(i) for i in range(3)]
print([f() for f in funcs])  # [0, 1, 2] ✓
```

---

## Solution Comparison

| Method | Pros | Cons |
|--------|------|------|
| Default parameter `x=i` | Simple, idiomatic | Changes function signature |
| Factory function | Clear intent | More verbose |
| `functools.partial` | No signature change | Import required |
| IIFE `(lambda x: ...)(i)` | Inline | Less readable |

### When to Use Each

- **Simple cases**: Default parameter `x=i`
- **Complex logic**: Factory function
- **Existing functions**: `functools.partial`

---

## Early Binding with Defaults

Default parameters use **early binding**—the value is captured when the function is defined:

```python
def outer():
    x = 10
    def inner(x=x):  # x captured NOW (value 10)
        return x
    x = 20  # Too late, inner already captured x=10
    return inner

f = outer()
print(f())  # 10
```

---

## Common Pitfalls

### Pitfall 1: Event Handlers

```python
# Bug: All buttons do the same thing
buttons = []
for i in range(3):
    btn = Button(command=lambda: print(i))
    buttons.append(btn)
# All buttons print 2

# Fix
for i in range(3):
    btn = Button(command=lambda x=i: print(x))
    buttons.append(btn)
```

### Pitfall 2: Callbacks

```python
# Bug
callbacks = {}
for name in ['a', 'b', 'c']:
    callbacks[name] = lambda: print(name)

callbacks['a']()  # Prints 'c'!

# Fix
for name in ['a', 'b', 'c']:
    callbacks[name] = lambda n=name: print(n)
```

### Pitfall 3: Threading

```python
import threading

# Bug
for i in range(3):
    threading.Thread(target=lambda: print(i)).start()
# Output unpredictable, likely all same value

# Fix
for i in range(3):
    threading.Thread(target=lambda x=i: print(x)).start()
```

### Pitfall 4: Nested Loops

The gotcha compounds with nested loops:

```python
# Bug
matrix = []
for i in range(3):
    row = []
    for j in range(3):
        row.append(lambda: (i, j))
    matrix.append(row)

print(matrix[0][0]())  # (2, 2) - Wrong!

# Fix
matrix = []
for i in range(3):
    row = []
    for j in range(3):
        row.append(lambda i=i, j=j: (i, j))
    matrix.append(row)

print(matrix[0][0]())  # (0, 0) - Correct!
```

---

## Memory Consideration

Default parameters capture references, not copies:

```python
# Mutable object caution
data = [1, 2, 3]
f = lambda x=data: x

data.append(4)
print(f())  # [1, 2, 3, 4] — reference, not copy!

# If you need a copy:
f = lambda x=data.copy(): x
# or
f = lambda x=list(data): x
```

---

## Summary

| Binding Type | When Value is Captured | Syntax |
|--------------|------------------------|--------|
| Late binding | When function is called | `def f(): return x` |
| Early binding | When function is defined | `def f(x=x): return x` |

| Issue | Cause | Solution |
|-------|-------|----------|
| All closures return same value | Late binding | Capture value at definition time |
| Loop variable captured | Same variable shared | Use `x=i` default parameter |
| Callback returns wrong value | Reference to final loop value | Factory function or partial |

**Key Takeaways**:

1. Closures capture **variables by reference**, not by value
2. Loop variables change, but all closures share the same reference
3. Use **default parameters** to capture the current value
4. Or use a **factory function** to create separate scopes
5. This applies to `def`, `lambda`, and comprehensions

**Golden Rule**: When creating closures in a loop, always **capture the value** at definition time.

---

## Exercises


**Exercise 1.**
Without running the code, predict the output. Then verify.

```python
funcs = [lambda x: x + i for i in range(3)]
print([f(10) for f in funcs])
```

??? success "Solution to Exercise 1"

        ```python
        funcs = [lambda x: x + i for i in range(3)]
        print([f(10) for f in funcs])  # [12, 12, 12]
        ```

    All lambdas share the same `i` variable. By the time they are called, the loop has finished and `i` is `2`, so each returns `10 + 2 = 12`.

---

**Exercise 2.**
Rewrite the list comprehension from Exercise 1 so that each lambda correctly captures its own value of `i`, producing `[10, 11, 12]`.

??? success "Solution to Exercise 2"

        ```python
        funcs = [lambda x, i=i: x + i for i in range(3)]
        print([f(10) for f in funcs])  # [10, 11, 12]
        ```

    The default argument `i=i` captures the current value of `i` at each iteration.

---

**Exercise 3.**
Explain why using `functools.partial` can also solve the late-binding problem. Rewrite the list comprehension from Exercise 1 using `functools.partial`.

??? success "Solution to Exercise 3"

        ```python
        from functools import partial

        def add(x, i):
            return x + i

        funcs = [partial(add, i=i) for i in range(3)]
        print([f(10) for f in funcs])  # [10, 11, 12]
        ```

    `functools.partial` creates a new function with `i` bound to a specific value. Unlike closures, `partial` stores the value directly rather than referencing a variable, so late binding is not an issue.
