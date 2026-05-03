# Bad Practices

!!! tip "Mental Model"
    Every bad naming practice boils down to one mistake: choosing a name that collides with something Python already uses. Shadowing `list`, `type`, or `id` with your own variable hides the built-in silently and causes confusing errors later. If your editor highlights a name as a built-in, pick a different name.

## Shadowing Built-ins

### 1. Common Mistakes

```python
# Really bad!
print(sorted([3, 1, 2]))
sorted = 1  # Shadows built-in!

# Later...
# sorted([3, 1, 2])  # TypeError!
```

### 2. Recovery

```python
# Once shadowed
list = [1, 2, 3]

# Recover
del list
new_list = list(range(5))  # Works
```

### 3. Don't Shadow

```python
# Never shadow:
# list, dict, set, tuple
# str, int, float
# print, input
# len, range
# sum, min, max
# sorted, filter, map
# type, id
```

## Function Shadowing

### 1. Example

```python
def f():
    return 1

f = 100  # Shadows function!
# f()  # TypeError!
```

### 2. Namespace Pollution

```python
# Bad
def count():
    return 42

count = count()  # Now int!
# count()  # TypeError!
```

## Misleading Names

### 1. Wrong Convention

```python
# Bad: looks constant
MAX_SIZE = [1, 2, 3]  # Mutable!

# Better
max_size = [1, 2, 3]
MAX_SIZE = 100  # Constant
```

### 2. Name vs Content

```python
# Bad
count = "not a count"
total = [1, 2, 3]

# Better  
label = "not a count"
numbers = [1, 2, 3]
```

## Single Letter Issues

### 1. Avoid Confusion

```python
# Bad: l looks like 1
l = 1          # Don't use
O = 0          # Don't use
I = 1          # Don't use

# Better
length = 1
offset = 0
index = 1
```

## Prevention

### 1. Check First

```python
import keyword
import builtins

def is_safe_name(name):
    if keyword.iskeyword(name):
        return False
    if hasattr(builtins, name):
        return False
    return name.isidentifier()

print(is_safe_name("user"))   # True
print(is_safe_name("list"))   # False
```

### 2. Use Linters

Tools that catch shadowing:
- pylint
- flake8
- pycodestyle

---

## Exercises


**Exercise 1.**
Identify three naming problems in the following code and fix them.

```python
l = [1, 2, 3]
str = "hello"
def f(x):
    O = x + 1
    return O
```

??? success "Solution to Exercise 1"

        ```python
        # Fixed version
        numbers = [1, 2, 3]           # 'l' looks like '1'
        greeting = "hello"             # 'str' shadows built-in
        def increment(value):          # 'f' is not descriptive
            result = value + 1         # 'O' looks like '0'
            return result
        ```

    Avoid single-letter names that look like digits (`l`, `O`), shadowing built-ins (`str`), and non-descriptive function names (`f`).

---

**Exercise 2.**
Explain why using `list`, `dict`, `str`, `type`, or `id` as variable names is dangerous. Write a code example that breaks because of shadowing a built-in.

??? success "Solution to Exercise 2"

        ```python
        list = [1, 2, 3]

        try:
            new_list = list("hello")
        except TypeError as e:
            print(f"Error: {e}")  # 'list' object is not callable

        del list  # Restore built-in
        print(list("hello"))  # ['h', 'e', 'l', 'l', 'o']
        ```

    Shadowing built-ins makes them inaccessible in the current scope, causing confusing errors.

---

**Exercise 3.**
Rewrite the following code with descriptive variable names.

```python
def p(d, r, t):
    return d * (1 + r) ** t
```

??? success "Solution to Exercise 3"

        ```python
        def compound_interest(principal, annual_rate, years):
            return principal * (1 + annual_rate) ** years

        print(compound_interest(1000, 0.05, 10))  # 1628.89...
        ```

    Descriptive names make the formula self-documenting without needing comments.
