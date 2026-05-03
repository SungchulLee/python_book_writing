# Variable Assignment

!!! tip "Mental Model"
    Assignment in Python does not put a value into a box. It attaches a name tag to an object that already exists on the heap. `a = 543` creates the integer object `543` and sticks the label `a` on it. Reassigning `a = "boy"` just moves the label to a different object -- the old integer is untouched and may be garbage-collected.

## Basic Assignment

### 1. Simple Assignment

```python
a = 543
print(f"{a = }")        # a = 543
print(f"{id(a) = }")    # Memory address
```

### 2. Type Changes

```python
a = 543      # Integer
print(type(a))  # <class 'int'>

a = 'boy'    # String
print(type(a))  # <class 'str'>
```

### 3. What Happens

Each assignment:
1. Creates/retrieves object
2. Binds name to object
3. Increments reference count

```python
x = 42
# 1. Integer object 42 created/retrieved
# 2. Name 'x' bound to object
# 3. Refcount of 42 incremented
```

## Multiple Assignment

### 1. Simultaneous

```python
a, b = 1, 2
print(f"{a = }, {b = }")  # a = 1, b = 2
```

**Process**:
```python
# Step 1: Create tuple (1, 2)
# Step 2: Unpack to a, b
```

### 2. Unpacking

```python
# With starred expressions
numbers = list(range(10))
first, *middle, last = numbers
print(f"{first = }")   # first = 0
print(f"{middle = }")  # middle = [1,2,3,4,5,6,7,8]
print(f"{last = }")    # last = 9
```

### 3. Throwaway Values

```python
# Using _ for unused variables
_, status_code, _ = ("HTTP", 200, "OK")
print(f"Status: {status_code}")  # Status: 200
```

## Chained Assignment

### 1. Basic Chaining

```python
a = b = c = 1
print(f"{a = }, {b = }, {c = }")  # All are 1
```

### 2. Execution Order

```python
# Evaluated right-to-left
# But assigned left-to-right
x = 42
original_id = id(x)

# All names point to same object
y = z = x
print(id(x) == id(y) == id(z))  # True
```

### 3. Not Equivalent

```python
# a = b = c = 1
# Is NOT exactly:
# c = 1; b = c; a = b

# Because:
a = b = c = [1, 2, 3]
# All refer to SAME list

# vs
c = [1, 2, 3]
b = c.copy()
a = b.copy()
# Three DIFFERENT lists
```

## Identity Check

### 1. Same Object

```python
x = 42
y = 42
print(f"{x is y = }")  # May be True (interning)
print(f"{id(x) == id(y) = }")  # May be True
```

### 2. Different Objects

```python
x = [1, 2, 3]
y = [1, 2, 3]
print(f"{x is y = }")  # False
print(f"{x == y = }")  # True
```

## Assignment Patterns

### 1. Swapping

```python
# Pythonic swap
a, b = 10, 20
a, b = b, a
print(f"{a = }, {b = }")  # a = 20, b = 10
```

### 2. Walrus Operator

```python
# Python 3.8+
data = [1, 2, 3, 4, 5]
if (n := len(data)) > 3:
    print(f"Large dataset: {n} items")
```

### 3. Conditional

```python
# Ternary assignment
x = 10
result = "positive" if x > 0 else "non-positive"
print(result)  # positive
```

## Common Mistakes

### 1. Tuple Creation

```python
# Automatic tuple packing
a = 1, 2, 3
print(type(a))  # <class 'tuple'>

# Explicit
b = (1, 2, 3)
print(type(b))  # <class 'tuple'>
```

### 2. List vs Tuple

```python
# List unpacking
[a, b, c] = [1, 2, 3]

# Tuple unpacking (more common)
a, b, c = 1, 2, 3

# Both work the same
```


---

## Exercises


**Exercise 1.**
Create a variable `x = [1, 2, 3]` and assign `y = x`. Modify `y` by appending `4`. Print both `x` and `y` and explain why `x` also changed.

??? success "Solution to Exercise 1"

    ```python
    x = [1, 2, 3]
    y = x
    y.append(4)
    print(x)  # [1, 2, 3, 4]
    print(y)  # [1, 2, 3, 4]
    ```

    `y = x` does not copy the list. Both `x` and `y` are names pointing to the same object. Modifying through either name affects the shared object.

---

**Exercise 2.**
Use tuple unpacking to swap two variables `a = 10` and `b = 20` without using a temporary variable. Then use starred unpacking to extract the first and last elements from a list of 10 numbers.

??? success "Solution to Exercise 2"

    ```python
    a, b = 10, 20
    a, b = b, a
    print(f"{a=}, {b=}")  # a=20, b=10

    numbers = list(range(10))
    first, *middle, last = numbers
    print(f"{first=}, {last=}")  # first=0, last=9
    ```

    Swap works by creating a tuple `(b, a)` on the right side and unpacking it. The starred expression `*middle` collects all elements between first and last.

---

**Exercise 3.**
Demonstrate the difference between chained assignment (`a = b = [1,2,3]`) and separate assignment (`a = [1,2,3]; b = [1,2,3]`). Show that chained assignment creates shared references while separate assignment creates independent objects.

??? success "Solution to Exercise 3"

    ```python
    # Chained: same object
    a = b = [1, 2, 3]
    a.append(4)
    print(b)  # [1, 2, 3, 4] (shared reference)

    # Separate: different objects
    a = [1, 2, 3]
    b = [1, 2, 3]
    a.append(4)
    print(b)  # [1, 2, 3] (independent)
    ```

    Chained assignment binds all names to the same object. Separate assignments create distinct objects, even if the values are identical.
