# Scoping Rules

클로저와 관련된 Python의 스코프 규칙입니다.

!!! tip "Mental Model"
    Python 3 comprehensions, generator expressions, and class bodies each create their own scope -- loop variables do not leak out. This is different from Python 2 and from bare `for` loops. Understanding which constructs create scopes and which do not is the key to predicting where a name is visible.

## Comprehension Scoping (Python 3+)

### List Comprehension Has Own Scope

```python
x = "outer"
result = [x for x in range(3)]

print(x)  # "outer" (unchanged)
print(result)  # [0, 1, 2]
```

Python 3에서 comprehension의 루프 변수는 **leak하지 않습니다**.

### Dict/Set Comprehensions — Same Behavior

```python
x = 10
d = {x: x**2 for x in range(3)}

print(x)  # 10 (unchanged)
print(d)  # {0: 0, 1: 1, 2: 4}
```

### Nested Comprehensions

```python
matrix = [[j for j in range(3)] for i in range(3)]
# i and j don't leak
```

---

## Generator Scoping

### Generator Expressions Have Own Scope

```python
x = 10
gen = (x for x in range(3))

print(x)  # 10 (unchanged)
print(list(gen))  # [0, 1, 2]
```

### Generators Can Close Over Variables

```python
def make_counter(start):
    count = start
    
    def counter():
        nonlocal count
        while True:
            count += 1
            yield count
    
    return counter()

gen = make_counter(0)
print(next(gen))  # 1
print(next(gen))  # 2
```

---

## Lambda vs def

### Both Support Closures Identically

```python
def outer():
    x = 10
    
    # Lambda closure
    f1 = lambda: x
    
    # Def closure
    def f2():
        return x
    
    return f1, f2

a, b = outer()
print(a())  # 10
print(b())  # 10
```

### Differences

| Feature | `lambda` | `def` |
|---------|----------|-------|
| Body | Single expression | Multiple statements |
| Name | Anonymous (`<lambda>`) | Named |
| Docstring | No | Yes |
| Decorators | No | Yes |
| Closures | ✅ Same | ✅ Same |

### When to Use Each

```python
# Lambda: simple, inline
sorted(items, key=lambda x: x.name)

# Def: complex logic, needs name
def process_item(item):
    """Process and validate item."""
    if not item.valid:
        raise ValueError("Invalid")
    return item.transform()
```

---

## Nested Closures

### Multiple Levels

```python
def outer():
    x = 1
    
    def middle():
        y = 2
        
        def inner():
            return x + y  # Captures from both levels
        
        return inner
    
    return middle()

f = outer()
print(f())  # 3
```

### Closure Composition

```python
def add(x):
    def adder(y):
        return x + y
    return adder

add5 = add(5)
add10 = add(10)

print(add5(3))   # 8
print(add10(3))  # 13
```

---

## Advanced: Scope Interaction

### global vs nonlocal

```python
x = "global"

def outer():
    x = "outer"
    
    def use_global():
        global x
        return x
    
    def use_nonlocal():
        nonlocal x
        return x
    
    print(use_global())    # "global"
    print(use_nonlocal())  # "outer"

outer()
```

| Keyword | Refers To |
|---------|-----------|
| `global` | Module-level variable |
| `nonlocal` | Nearest enclosing function's variable |

### Class Scope Is Not Enclosing

```python
class MyClass:
    x = 10
    
    def method(self):
        # x is NOT accessible here without self or MyClass
        # print(x)  # NameError
        print(MyClass.x)  # Works
        print(self.x)     # Works
```

Class body는 enclosing scope로 작동하지 않습니다.

---

## Python 2 vs 3 Differences

| Feature | Python 2 | Python 3 |
|---------|----------|----------|
| List comprehension leak | Yes | No |
| `nonlocal` keyword | No | Yes |
| Workaround for rebinding | Mutable container | `nonlocal` |

```python
# Python 2 style (still works in 3)
def counter():
    count = [0]
    def inc():
        count[0] += 1
        return count[0]
    return inc

# Python 3 style (preferred)
def counter():
    count = 0
    def inc():
        nonlocal count
        count += 1
        return count
    return inc
```

---

## Summary

| Scope Type | Creates Own Namespace | Variables Leak |
|------------|----------------------|----------------|
| Function | Yes | No |
| Comprehension (Py3) | Yes | No |
| Generator expression | Yes | No |
| Class body | Yes (but not enclosing) | N/A |
| Loop (for/while) | No | Yes |

**Key Points:**
- Comprehensions and generators have isolated scopes in Python 3
- Lambda and def have identical closure behavior
- Use `nonlocal` for rebinding, `global` for module-level
- Class bodies don't create enclosing scopes for methods

---

## Exercises


**Exercise 1.**
Without running the code, predict the output. Then verify.

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        print(x)
    inner()

outer()
print(x)
```

??? success "Solution to Exercise 1"

        ```
        enclosing
        global
        ```

    `inner()` finds `x` in the enclosing scope (`"enclosing"`). The global `x` remains `"global"` because neither function modifies it.

---

**Exercise 2.**
Write a function `outer()` that defines a variable `data = []` and returns two closures: `add(item)` (which appends to `data`) and `get()` (which returns a copy of `data`). Demonstrate that both closures share the same `data`.

??? success "Solution to Exercise 2"

        ```python
        def outer():
            data = []
            def add(item):
                data.append(item)
            def get():
                return data.copy()
            return add, get

        add, get = outer()
        add("a")
        add("b")
        print(get())  # ['a', 'b']
        add("c")
        print(get())  # ['a', 'b', 'c']
        ```

    Both closures capture the same `data` list. `add` mutates it (no `nonlocal` needed for mutation), and `get` returns a copy for safety.

---

**Exercise 3.**
Explain what happens when you read a global variable inside a function versus when you assign to it. Why does assignment create a local variable?

??? success "Solution to Exercise 3"

    When Python compiles a function, it scans for all assignment targets. If a variable name appears on the left side of an assignment (e.g., `x = ...`), Python treats it as a local variable for the entire function. This means even reading `x` before the assignment raises `UnboundLocalError`.

        ```python
        x = 10

        def read_only():
            print(x)       # Works: reads global x

        def assigns():
            print(x)       # UnboundLocalError!
            x = 20         # This makes x local for entire function

        read_only()        # 10
        # assigns()        # UnboundLocalError
        ```

    To modify a global variable, use `global x`. To modify an enclosing variable, use `nonlocal x`.
