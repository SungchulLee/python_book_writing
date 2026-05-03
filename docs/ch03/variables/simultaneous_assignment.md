# Simultaneous Assign

!!! tip "Mental Model"
    `a, b = 1, 2` first builds the tuple `(1, 2)` on the right side, then unpacks it into `a` and `b` on the left. Because the right side is fully evaluated before any assignment, `a, b = b, a` swaps values without a temporary variable. The starred expression (`*rest`) captures any leftovers into a list.

## Basic Unpacking

### 1. Simple Case

```python
a, b = 1, 2
print(f"{a = }, {b = }")  # a = 1, b = 2
```

**Process**:
1. Right side: Create tuple `(1, 2)`
2. Left side: Unpack to `a` and `b`

### 2. Tuple Creation

```python
# Tuple is created
x = 1, 2
print(type(x))  # <class 'tuple'>

# Internally
a, b = 1, 2
# (1, 2) created, then unpacked
```

## Advanced Unpacking

### 1. Starred Expression

```python
numbers = list(range(10))
first, *middle, last = numbers

print(f"{first = }")   # first = 0
print(f"{middle = }")  # middle = [1,2,...,8]
print(f"{last = }")    # last = 9
```

### 2. Position Matters

```python
*start, last = [1, 2, 3, 4]
print(f"{start = }")  # start = [1, 2, 3]
print(f"{last = }")   # last = 4

first, *end = [1, 2, 3, 4]
print(f"{first = }")  # first = 1
print(f"{end = }")    # end = [2, 3, 4]
```

## Throwaway Variables

### 1. Underscore

```python
# Ignoring values
_, status_code, _ = ("HTTP", 200, "OK")
print(f"Status: {status_code}")
```

### 2. With Star

```python
first, *_, last = range(10)
print(f"{first = }")  # first = 0
print(f"{last = }")   # last = 9
```

## Swapping Pattern

### 1. Elegant Swap

```python
a, b = 10, 20
print(f"Before: {a = }, {b = }")

a, b = b, a
print(f"After: {a = }, {b = }")
# Before: a = 10, b = 20
# After: a = 20, b = 10
```

### 2. How It Works

```python
# Internally:
# 1. Create tuple (b, a) = (20, 10)
# 2. Unpack to a, b
# No temp variable needed!
```

### 3. Multiple Swap

```python
a, b, c = 1, 2, 3
a, b, c = c, a, b
print(f"{a = }, {b = }, {c = }")
# a = 3, b = 1, c = 2
```

## Function Returns

### 1. Multiple Returns

```python
def get_coordinates():
    return 10, 20, 30

x, y, z = get_coordinates()
print(f"{x = }, {y = }, {z = }")
```

### 2. Partial Unpacking

```python
def get_data():
    return "name", 25, "city"

name, *rest = get_data()
print(f"{name = }")  # name = 'name'
print(f"{rest = }")  # rest = [25, 'city']
```

## Nested Unpacking

### 1. Nested Tuples

```python
data = (1, (2, 3), 4)
a, (b, c), d = data
print(f"{a = }, {b = }, {c = }, {d = }")
# a = 1, b = 2, c = 3, d = 4
```

## Iteration Patterns

### 1. Enumerate

```python
items = ['a', 'b', 'c']
for i, item in enumerate(items):
    print(f"{i}: {item}")
# 0: a
# 1: b
# 2: c
```

### 2. Dictionary Items

```python
data = {'x': 10, 'y': 20}
for key, value in data.items():
    print(f"{key} = {value}")
```

### 3. Zip

```python
names = ['Alice', 'Bob']
ages = [25, 30]

for name, age in zip(names, ages):
    print(f"{name} is {age}")
```

## Common Mistakes

### 1. Length Mismatch

```python
# Too many values
try:
    a, b = 1, 2, 3
except ValueError as e:
    print(e)  # too many values

# Too few values
try:
    a, b, c = 1, 2
except ValueError as e:
    print(e)  # not enough values
```

### 2. Star Required

```python
# This fails
# a, b = [1, 2, 3, 4, 5]
# ValueError

# This works
a, *b = [1, 2, 3, 4, 5]
print(f"{a = }, {b = }")
# a = 1, b = [2, 3, 4, 5]
```


---

## Exercises


**Exercise 1.**
Use simultaneous assignment to swap three variables `a = 1, b = 2, c = 3` so that `a` gets `c`'s value, `b` gets `a`'s value, and `c` gets `b`'s value. Do it in one line.

??? success "Solution to Exercise 1"

    ```python
    a, b, c = 1, 2, 3
    a, b, c = c, a, b
    print(f"{a=}, {b=}, {c=}")
    # a=3, b=1, c=2
    ```

    The right side creates a tuple `(c, a, b)` = `(3, 1, 2)` before any assignments happen, then unpacks it to the left side.

---

**Exercise 2.**
Write a function that returns three values (name, age, city). Use tuple unpacking to capture the results. Then use starred unpacking to capture only the first value and collect the rest.

??? success "Solution to Exercise 2"

    ```python
    def get_info():
        return "Alice", 30, "NYC"

    # Full unpacking
    name, age, city = get_info()
    print(f"{name=}, {age=}, {city=}")

    # Starred unpacking
    name, *rest = get_info()
    print(f"{name=}, {rest=}")  # rest=[30, 'NYC']
    ```

    Python functions return tuples implicitly when using comma-separated values. The caller unpacks them directly.

---

**Exercise 3.**
Demonstrate nested unpacking by extracting values from the structure `((1, 2), (3, 4), (5, 6))` into six separate variables in a single assignment.

??? success "Solution to Exercise 3"

    ```python
    data = ((1, 2), (3, 4), (5, 6))
    (a, b), (c, d), (e, f) = data
    print(f"{a=}, {b=}, {c=}, {d=}, {e=}, {f=}")
    # a=1, b=2, c=3, d=4, e=5, f=6
    ```

    Nested parentheses on the left side match the structure of the nested tuples on the right, unpacking each level.
