# Namespace Hierarchies

!!! tip "Mental Model"
    Picture namespaces as layered transparent sheets stacked Local-Enclosing-Global-Built-in. When Python looks up a name, it reads downward through the stack and stops at the first sheet where the name appears. Assignment always writes to the top sheet unless `global` or `nonlocal` redirects it.

## Four Levels

### 1. LEGB Rule

Lookup order:
1. **L**ocal
2. **E**nclosing
3. **G**lobal
4. **B**uilt-in

```python
x = "global"

def outer():
    x = "enclosing"
    
    def inner():
        x = "local"
        print(x)  # "local"
    
    inner()

outer()
```

## Local Scope

### 1. Function Local

```python
def function():
    x = 10  # Local scope
    print(x)

function()
# print(x)  # NameError
```

### 2. Method Local

```python
class MyClass:
    def method(self):
        x = 10  # Method local
        print(x)

obj = MyClass()
obj.method()
```

## Enclosing Scope

### 1. Nested Functions

```python
def outer():
    x = 10  # Enclosing for inner
    
    def inner():
        print(x)  # Access enclosing
    
    inner()

outer()  # 10
```

### 2. Multiple Levels

```python
def level1():
    x = 1
    
    def level2():
        # x from level1 is enclosing
        
        def level3():
            print(x)  # Access level1's x
        
        level3()
    
    level2()

level1()  # 1
```

## Global Scope

### 1. Module Level

```python
# Module-level = global
x = 10

def function():
    print(x)  # Access global

function()  # 10
```

### 2. Global Keyword

```python
x = 10

def function():
    global x
    x = 20  # Modify global

function()
print(x)  # 20
```

## Built-in Scope

### 1. Python Built-ins

```python
# Built-in functions
print(len([1, 2, 3]))
print(type(42))

# Always accessible
```

### 2. Shadowing Built-ins

```python
# Can shadow (but don't!)
len = 42

# print(len([1, 2, 3]))  # TypeError

# Restore
del len
print(len([1, 2, 3]))  # 3
```

## Lookup Examples

### 1. All Levels

```python
x = "global"

def outer():
    x = "enclosing"
    
    def inner():
        # Local x shadows all
        x = "local"
        print(x)  # "local"
    
    inner()

outer()
```

### 2. Skip Levels

```python
x = "global"

def outer():
    # No x here
    
    def inner():
        print(x)  # Skip enclosing, use global
    
    inner()

outer()  # "global"
```

## Class Namespace

### 1. Separate Hierarchy

```python
class MyClass:
    x = 10  # Class namespace
    
    def method(self):
        # Access via self
        print(self.x)

obj = MyClass()
obj.method()  # 10
```

### 2. Instance vs Class

```python
class MyClass:
    x = "class"
    
    def __init__(self):
        self.x = "instance"

obj = MyClass()
print(obj.x)  # "instance"
print(MyClass.x)  # "class"
```

## Summary

### 1. LEGB Order

```python
x = "builtin (if shadowed)"
x = "global"

def outer():
    x = "enclosing"
    
    def inner():
        x = "local"
        # Lookup: local → enclosing → global → builtin
```

### 2. Key Points

- Lookup goes L → E → G → B
- First match wins
- Can skip levels
- Classes separate

## Exercises

**Exercise 1.**
Predict the output and trace the LEGB lookup for each `print(x)`:

```python
x = "global"

def outer():
    x = "enclosing"

    def inner():
        print(x)

    inner()
    print(x)

outer()
print(x)
```

Which namespace does each `print(x)` resolve from? What would change if `inner()` had `x = "local"` as its first line?

??? success "Solution to Exercise 1"
    Output:

    ```text
    enclosing
    enclosing
    global
    ```

    - `inner()` prints `x`: `inner` has no local `x`. LEGB lookup: Local (none) -> Enclosing (`outer`'s `x = "enclosing"`) -> found. Prints `"enclosing"`.
    - `outer()` prints `x`: `outer` has local `x = "enclosing"`. LEGB: Local (found). Prints `"enclosing"`.
    - Top-level `print(x)`: Global `x = "global"`. Prints `"global"`.

    If `inner()` had `x = "local"` as its first line, the first `print(x)` would show `"local"` (local scope found first). The other two prints would be unchanged because each function's local scope is independent.

---

**Exercise 2.**
Explain why this code raises an `UnboundLocalError` instead of printing `10`:

```python
x = 10

def f():
    print(x)
    x = 20

f()
```

Python does not execute functions line-by-line for scoping decisions. When does Python decide that `x` is local? Why does the `print(x)` fail even though it comes before `x = 20`?

??? success "Solution to Exercise 2"
    Python determines variable scope at **compile time** (when the function is defined), not at runtime. Because `x = 20` appears anywhere in `f`, Python classifies `x` as a **local variable** for the entire function body. This decision is made before any code executes.

    When `print(x)` runs, Python looks for `x` in the local scope (because it was classified as local). But `x = 20` has not executed yet, so the local `x` has no value. This raises `UnboundLocalError: local variable 'x' referenced before assignment`.

    The key insight: scope is determined by the presence of assignment **anywhere** in the function, not by the order of statements. If `x` is assigned anywhere in the function, it is local everywhere in that function -- even on lines before the assignment.

    To read the global `x` while also assigning a local `x`, you would need `global x` declaration.

---

**Exercise 3.**
The `global` and `nonlocal` keywords explicitly change which namespace a name binds to. Predict the output:

```python
count = 0

def increment():
    global count
    count += 1

increment()
increment()
print(count)
```

What would happen without the `global` declaration? Why does Python require explicit `global` instead of allowing functions to modify global variables by default?

??? success "Solution to Exercise 3"
    Output: `2`

    The `global count` declaration tells Python that `count` inside `increment` refers to the **global** variable, not a local one. Without it, `count += 1` would try to read and assign a local `count`, raising `UnboundLocalError` (same issue as Exercise 2 -- the assignment makes `count` local, but it is read before being assigned locally).

    Python requires explicit `global` because **implicit global mutation would be dangerous**. If functions could silently modify global variables, it would be nearly impossible to reason about program state -- any function call could change any global variable. The explicit `global` declaration makes the intent clear and makes global modification grep-able and auditable.

    This is a deliberate design choice favoring explicitness: Python wants you to know when a function modifies state outside its local scope.
